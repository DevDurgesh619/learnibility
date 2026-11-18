"""IB DP Economics SL/HL (first assessment 2022) - ib-g12-economics, year 2 (Unit 3 Macroeconomics, Unit 4 Global economy).

Assessment model mirrored in the items:
  Paper 1 extended response: (a) explain, with a diagram [10] and (b) evaluate with real-world examples [15].
  Paper 2 data response: definitions [2], data/diagram analysis [4], calculations (HL) and an evaluation
          using the text and the student's own knowledge [15].
  Paper 3 (HL) policy paper: quantitative questions with computed answers and a policy recommendation [10].
Command terms follow the IB guide (define, outline, describe, explain, distinguish, analyse, calculate,
evaluate, discuss, to what extent, justify, recommend). Numerical items are parametric and compute their
answers (GDP/GNI, real GDP, multiplier, growth, unemployment, CPI/inflation, Gini, tax rates, money creation,
budget/debt, comparative advantage, tariff welfare areas, trade creation, exchange rates, BoP, terms of trade,
HDI); markschemes award [1] for valid working and [1] for the correct answer with units, as in IB.
Data in parametric items is for hypothetical economies; real-world figures in cases and sources are rounded.
Key concepts: scarcity, choice, efficiency, equity, economic well-being, sustainability, change,
interdependence, intervention.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names, CITIES  # noqa: F401

CONFIG = {'minutesPerMark': 2.0, 'mcqMinutes': 1.5}

# One HL mock = Paper 1 (2 parts) + Paper 2 (3 parts) + Paper 3 (2 parts): 7 questions, 60 marks.
MOCK = [
    dict(section='Paper 1 (a) - Explain, using a diagram', count=1, c=['C3'], d=[4], type='long', marks=10, style='p1a'),
    dict(section='Paper 1 (b) - Evaluate, using real-world examples', count=1, c=['C4'], d=[5], type='long', marks=15, style='p1b'),
    dict(section='Paper 2 (a) - Definition', count=1, c=['C1'], d=[2], type='short', marks=2),
    dict(section='Paper 2 (b) - Data / diagram analysis', count=1, c=['C3'], d=[3], type='case', marks=4),
    dict(section='Paper 2 (c) - Evaluate using the text and own knowledge', count=1, c=['C4'], d=[5], type='long', marks=15, style='p2'),
    dict(section='Paper 3 (a) - Calculation', count=1, c=['C3'], d=[4], type='numerical', marks=4, style='calc'),
    dict(section='Paper 3 (b) - Policy recommendation', count=1, c=['C4'], d=[4], type='long', marks=10, style='p3'),
]

MB15 = ('IB Paper 1(b)/2(c) markbands [15]: Level 5 (13-15) relevant terms defined; theory explained clearly with an accurate, '
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

ECON = ['Country X', 'Zedland', 'Nordavia', 'Kalimar', 'Estoria', 'Pacifica', 'Lumeria', 'Sundara', 'Varnia', 'Oskaria',
        'Montego', 'Arvenia', 'Tarsia', 'Belloria', 'Kestria', 'Halvania']
CUR = [('$', ''), ('€', ''), ('£', ''), ('', ' Kenyan shillings'), ('', ' pesos'), ('', ' rupees'), ('', ' rand'),
       ('', ' baht'), ('', ' zloty')]
CURNAME = ['Zed dollar (ZD)', 'Nordavian krone (NK)', 'Kalimar rupee (KR)', 'Estorian peso (EP)', 'Pacifica franc (PF)',
           'Lumerian mark (LM)', 'Sundaran ringgit (SR)', 'Varnian lira (VL)']


def init(subject_id):
    pass


def cap(s):
    return s[0].upper() + s[1:]


def S(key, diag=(), **kw):
    """Register a subtopic fact pack plus Paper 1(a) diagram questions (phrase, answer)."""
    if 'cases' in kw:
        kw['cases'] = [(c, w, k, cap(h)) for c, w, k, h in kw['cases']]
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
            if slot.style == 'p1a' or slot.d >= 4:
                stem = rng.choice([f'Using an appropriate diagram, explain {phrase}.',
                                   f'Explain, with the help of a fully labelled diagram, {phrase}.'])
                m = 10
            else:
                stem = rng.choice([f'Draw a diagram to illustrate {phrase}, and outline what it shows.',
                                   f'With the help of a labelled diagram, outline {phrase}.'])
                m = 6
            return dict(stem=stem, answer=ans, type='long', marks=m,
                        markingKey=f'Indicative content: {ans} {MB10 if m == 10 else "Award up to 2 marks for an accurate, fully labelled diagram and up to 4 for the explanation linked to it."}')
        out.append(T('C3', (3, 5), diag, 'long', 'p1a', 'diag'))
    if f and f.why:
        def p1a(rng, slot, f=f):
            if slot.style != 'p1a':
                return None
            q, a = rng.choice(f.why)
            body = q[0].lower() + q[1:]
            stem = rng.choice([f'Using an appropriate diagram, {body} [10]', f'With the help of a diagram where relevant, {body} [10]'])
            return dict(stem=stem, answer=a, type='long', marks=10,
                        markingKey=f'Indicative content: {a} A relevant AD/AS, market or other diagram should be drawn, labelled and explained. {MB10}')
        out.append(T('C3', (3, 5), p1a, 'long', 'p1a', 'p1a'))
    if f and f.evaluate:
        srcs = f.sources
        cases = f.cases

        def p1b(rng, slot, f=f):
            if slot.style != 'p1b':
                return None
            claim, pro, con, judge = rng.choice(f.evaluate)
            stem = rng.choice([f'Using real-world examples, evaluate the view that {lc(claim)} [15]',
                               f'Using real-world examples, discuss the claim that {lc(claim)} [15]',
                               f'"{claim}" Using real-world examples, to what extent do you agree with this statement? [15]'])
            key = ('Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) +
                   f'. Supported judgement: {judge} {MB15}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=15, gap='G5')
        out.append(T('C4', (4, 5), p1b, 'long', 'p1b', 'p1b'))

        def p2(rng, slot, f=f, skey=key):
            claim, pro, con, judge = rng.choice(f.evaluate)
            pool = [f'{src}\n— {attr}' for src, attr, _, _ in srcs] + [what for _, what, _, _ in cases]
            if not pool:
                return None
            if len(pool) > 1 and rng.random() < 0.6:
                a, b = rng.sample(pool, 2)
                pool = [f'{a}\n\n{b}']
            text = rng.choice(pool)
            stem = (f'Read the extract below.\n\n{text}\n\nUsing information from the extract and your knowledge of '
                    f'economics, evaluate the view that {lc(claim)}')
            key = ('Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) +
                   f'. Judgement: {judge} Reward explicit use of the extract. {MB15}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=15, gap='G7')
        out.append(T('C4', (4, 5), p2, 'long', 'p2', 'p2'))

        def p3(rng, slot, f=f):
            claim, pro, con, judge = rng.choice(f.evaluate)
            role = rng.choice(['an economist advising the government', 'a policy adviser to the ministry of finance',
                               'an adviser to the central bank', 'an analyst at a regional development bank',
                               'an economist at the trade ministry'])
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


def bn(v, unit=' bn'):
    """Signed money amount: −$52 bn / $52 bn."""
    v = round(v, 1)
    txt = f'{abs(v):,.1f}'.rstrip('0').rstrip('.') if abs(v - round(v)) > 1e-9 else f'{int(abs(round(v))):,}'
    return ('−' if v < 0 else '') + '$' + txt + unit


def r1(x):
    return f'{x:.1f}'.replace('-', '−')


def r2(x):
    s = f'{x:.2f}'
    return s.rstrip('0').rstrip('.') if '.' in s else s


def pct(new, old):
    return 100.0 * (new - old) / old


def ec(rng):
    return rng.choice(ECON)


def calc(key, c=('C3',), d=(1, 5), ty='numerical'):
    """Register a numerical generator (style 'calc' so Paper 3 (a) mock slots prefer it)."""
    cc = c if isinstance(c, tuple) else (c,)

    def deco(fn):
        R.t.setdefault(key, []).append(T(cc if len(cc) > 1 else cc[0], d, fn, ty, 'calc', fn.__name__))
        return fn
    return deco


def nmcq(rng, stem, v, wrongs, key, f=r2):
    """Numeric MCQ: v correct, wrongs raw numbers; formatted with f."""
    a = f(v)
    ws = []
    for w in wrongs:
        s = f(w)
        if s != a and s not in ws:
            ws.append(s)
    if len(ws) < 3:
        return None
    return mcq(rng, stem, a, ws[:3], key)


def MK(steps, ans):
    """IB-style markscheme for a calculation."""
    return f'{steps} [M1] for correct method/working; [A1] for {ans}. Award [A1] only with correct units/notation where relevant.'


# =============================================================================================
# ch01 Unit 3.1 Measuring economic activity
# =============================================================================================
GDP_FRAMES = [
    'The national statistics office of {e} publishes the following expenditure data for last year (in $ billion): consumption {C}, investment {I}, government spending {G}, exports {X}, imports {M}.',
    'A Paper 2 extract reports that in {e} household spending was ${C} bn, gross fixed capital formation ${I} bn, government purchases ${G} bn, export revenue ${X} bn and import spending ${M} bn.',
    'Spending in {e} last year was: C = ${C} bn, I = ${I} bn, G = ${G} bn, X = ${X} bn and M = ${M} bn.',
    'An IMF country report on {e} lists the components of aggregate expenditure (in $ bn): private consumption {C}; investment {I}; general government consumption {G}; exports of goods and services {X}; imports of goods and services {M}.',
]


@calc('ch01-st1', 'C3', (1, 5))
def gdp_expenditure(rng, slot):
    C = rng.randint(150, 900)
    I = rng.randint(30, 250)
    G = rng.randint(40, 300)
    X = rng.randint(50, 400)
    M = rng.randint(50, 420)
    gdp = C + I + G + X - M
    if gdp <= 0:
        return None
    e = ec(rng)
    intro = rng.choice(GDP_FRAMES).format(e=e, C=C, I=I, G=G, X=X, M=M)
    if slot.d <= 2:
        return dict(stem=intro + '\nCalculate the value of GDP.', answer=f'${gdp} bn',
                    markingKey=MK(f'GDP = C + I + G + (X − M) = {C} + {I} + {G} + ({X} − {M}) = {gdp}.', f'${gdp} bn'), marks=2)
    nfi = rng.choice([-40, -25, -15, -8, 6, 12, 20, 35])
    gni = gdp + nfi
    if gni <= 0 or gdp < 60:
        return None
    if slot.d == 3:
        word = 'receive' if nfi > 0 else 'pay'
        return dict(stem=intro + f'\nResidents of {e} {word} a net ${abs(nfi)} bn in income from (to) the rest of the world. Calculate (i) GDP and (ii) GNI.',
                    answer=f'(i) GDP = ${gdp} bn; (ii) GNI = ${gni} bn',
                    markingKey=MK(f'GDP = {C} + {I} + {G} + {X} − {M} = {gdp}; GNI = GDP + net income from abroad = {gdp} {"+" if nfi > 0 else "−"} {abs(nfi)} = {gni}.', f'GDP ${gdp} bn and GNI ${gni} bn'), marks=3)
    pop = rng.choice([8, 12, 25, 40, 55, 64, 90])
    pc = gni * 1000 / pop
    return dict(stem=intro + f'\nNet income from abroad is {bn(nfi)} and the population is {pop} million. Calculate GNI per capita, and explain why GNI per capita may be a better indicator of living standards than total GDP.',
                answer=f'GNI = ${gni} bn; GNI per capita ≈ ${pc:,.0f}. Per capita measures adjust for population size, and GNI counts income that residents actually receive (it excludes profits repatriated by foreign firms).',
                markingKey=MK(f'GDP = {gdp}; GNI = {gdp} + ({nfi}) = {gni} bn; per capita = {gni} × 10⁹ / ({pop} × 10⁶) = ${pc:,.0f}.', f'≈ ${pc:,.0f}') + ' [R1][R1] for the two explanation points (population; income received by residents).', marks=4 if slot.d == 4 else 6)


@calc('ch01-st1', 'C3', (2, 4))
def ppp_convert(rng, slot):
    e = ec(rng)
    cname = rng.choice(CURNAME)
    code = cname.split('(')[1].rstrip(')')
    gdppc_local = rng.choice([120_000, 240_000, 360_000, 480_000, 600_000, 900_000])
    mer = rng.choice([40, 60, 80, 100, 120, 150])
    ppp = mer * rng.choice([0.25, 0.4, 0.5, 0.6, 0.75])
    a = gdppc_local / mer
    b = gdppc_local / ppp
    frame = rng.choice([
        f'GDP per capita in {e} is {gdppc_local:,} {code} (the {cname}). The market exchange rate is {mer} {code} = $1 and the PPP conversion factor is {r2(ppp)} {code} per international dollar.',
        f'In {e}, average output per person is worth {gdppc_local:,} {code}. One US dollar buys {mer} {code} on the foreign exchange market, but the same basket of goods costing $1 in the USA costs only {r2(ppp)} {code} in {e}.',
        f'World Bank data for {e}: GDP per capita {gdppc_local:,} {code}; official exchange rate {mer} {code}/$; PPP conversion factor {r2(ppp)} {code}/int$.'])
    return dict(stem=frame + f' Calculate GDP per capita at (i) the market exchange rate and (ii) purchasing power parity, and explain the difference.',
                answer=f'(i) ${a:,.0f}; (ii) int${b:,.0f}. PPP is higher because prices of non-traded goods and services are lower in {e}, so each unit of currency buys more domestically.',
                markingKey=MK(f'(i) {gdppc_local:,}/{mer} = ${a:,.0f}; (ii) {gdppc_local:,}/{r2(ppp)} = int${b:,.0f}.', f'${a:,.0f} and int${b:,.0f}') + ' [R1] PPP adjusts for differences in the cost of living, which are typically lower in lower-income economies.', marks=4)


@calc('ch01-st1', 'C1', (1, 3), 'mcq')
def gdp_mcq(rng, slot):
    C, I, G, X, M = rng.randint(200, 600), rng.randint(40, 150), rng.randint(60, 200), rng.randint(80, 250), rng.randint(80, 260)
    g = C + I + G + X - M
    return nmcq(rng, f'An economy has C = {C}, I = {I}, G = {G}, X = {X} and M = {M} ($ bn). What is GDP?', g,
                [C + I + G + X + M, C + I + G, C + I + G + X, g + 2 * M - 2 * X], f'GDP = C + I + G + X − M = {g}.', f=lambda v: f'${int(v)} bn')


S('ch01-st1',
  diag=[('the circular flow of income model with leakages and injections', 'Households supply factors and receive incomes; firms produce output; leakages (S, T, M) and injections (I, G, X); income = output = expenditure; national income rises when injections exceed leakages.'),
        ('how the output, income and expenditure methods of measuring national income must give the same value', 'Circular flow: the value of output equals the incomes paid to factors and the spending on that output; diagram with households, firms, government, financial sector and foreign sector.')],
  terms=[('gross domestic product (GDP)', 'the total market value of all final goods and services produced within a country in a given time period, usually a year'),
         ('gross national income (GNI)', 'GDP plus net income from abroad: the total income earned by a country\'s residents and factors of production, wherever they are located'),
         ('nominal GDP', 'GDP measured at current prices, not adjusted for inflation'),
         ('real GDP', 'GDP adjusted for changes in the price level, measured at constant prices of a base year'),
         ('GDP per capita', 'GDP divided by the population, giving average output (income) per person'),
         ('purchasing power parity (PPP)', 'an exchange rate that equalises the purchasing power of currencies so that the same basket of goods costs the same in each country'),
         ('net income from abroad', 'income earned by residents from factors of production abroad minus income paid to foreign owners of factors located in the country')],
  facts=[('Which of the following is counted in GDP?', 'A new car produced in the country and sold to a household', ['The sale of a second-hand house', 'A government pension payment', 'Shares bought on the stock exchange'], 'Only final goods and services produced in the period count; transfers and second-hand or financial transactions are excluded.'),
         ('Which of the following is the expenditure method formula for GDP?', 'C + I + G + (X − M)', ['C + S + T', 'C + I + G + X + M', 'Wages + rent + interest − profit'], 'GDP = consumption + investment + government spending + net exports.'),
         ('Which of the following explains why Ireland\'s GNI is far below its GDP?', 'Large profits earned by foreign multinationals in Ireland are paid to owners abroad', ['Irish residents earn large incomes abroad', 'Ireland has a very high rate of inflation', 'Irish GDP excludes services'], 'Repatriated multinational profits are included in GDP but not in GNI; Ireland even created a modified measure, GNI*.'),
         ('Which of the following is the best indicator for comparing average living standards across countries?', 'GNI per capita at purchasing power parity', ['Nominal GDP at market exchange rates', 'Total real GDP', 'The GDP deflator'], 'Per capita PPP measures adjust for population and for differences in price levels.')],
  why=[('Explain why national income can be measured by the output, income and expenditure methods.', 'Every unit of spending on final output becomes income for the factors that produced it, so in the circular flow total output = total income = total expenditure (allowing for statistical discrepancy).'),
       ('Explain why intermediate goods are excluded from GDP.', 'Their value is already included in the price of the final good; counting them again would be double counting and overstate output. The value-added approach avoids this.'),
       ('Explain why GDP per capita at PPP gives a better comparison of living standards than GDP per capita at market exchange rates.', 'Market exchange rates do not reflect differences in domestic price levels, especially of non-traded services; PPP values the same basket at the same prices, so it measures real purchasing power.'),
       ('Explain why GNI may differ from GDP for a country with many foreign-owned firms.', 'Profits earned by foreign-owned firms are part of domestic output (GDP) but are paid to non-residents, so they are subtracted from GNI; if outflows exceed inflows of factor income, GNI < GDP.'),
       ('Explain why transfer payments such as unemployment benefits are not included in GDP.', 'They are a redistribution of income, not payment for current production of goods or services, so including them would overstate output.')],
  contrast=[('GDP', 'GNI', 'GDP measures output produced within the country\'s borders; GNI measures income earned by the country\'s residents, so it adds income received from abroad and subtracts income paid to non-residents.'),
            ('nominal GDP', 'real GDP', 'Nominal GDP is valued at current prices and rises with inflation; real GDP is valued at constant prices, so it changes only when the volume of output changes.'),
            ('total GDP', 'GDP per capita', 'Total GDP is the size of the whole economy; GDP per capita divides by population, so it shows average output per person and allows living-standard comparisons.')],
  misc=[('India has a higher GDP than Switzerland, so Indians enjoy higher living standards.', 'Total GDP ignores population: India has around 1.4 billion people, so its GDP per capita is a small fraction of Switzerland\'s, even at PPP.'),
        ('When a family sells its old car to a neighbour, GDP rises by the price of the car.', 'Second-hand sales are not new production; only any dealer\'s commission (a service) would count.'),
        ('Nominal GDP rose by 8% so the economy produced 8% more goods and services.', 'Nominal GDP includes price changes; if inflation was, say, 6%, real output rose only by about 2%.')],
  cases=[('Ireland\'s 26% GDP growth in 2015', 'Irish GDP was revised up by about 26% for 2015 after multinationals moved intellectual property and aircraft leasing assets to Ireland; employment and household incomes did not jump.', 'the difference between GDP and GNI as indicators', 'the output was recorded in Ireland but the profits flowed to foreign owners, so the Central Statistics Office introduced GNI*, which strips out these effects and better reflects residents\' incomes'),
         ('the comparison of China and the USA using PPP', 'At market exchange rates US GDP is larger than China\'s, but the IMF estimates China\'s GDP at PPP has exceeded the USA\'s since about 2016.', 'purchasing power parity', 'lower prices of non-traded goods in China mean each yuan buys more, so PPP raises China\'s measured output relative to market-rate figures'),
         ('Nigeria\'s 2014 GDP rebasing', 'In 2014 Nigeria updated its GDP base year from 1990 to 2010, adding sectors such as telecoms and film (Nollywood); measured GDP rose by about 89% overnight.', 'the accuracy of national income statistics', 'out-of-date base years and weights can miss new industries, so GDP figures depend on statistical methods as well as real activity')],
  sources=[('In 2023 Luxembourg had one of the highest GDP per capita figures in the world, above $120,000. However, almost half of its workforce are cross-border commuters from France, Belgium and Germany, whose output is counted in Luxembourg\'s GDP although they live and spend much of their income elsewhere.', 'Adapted from Eurostat and World Bank commentary',
            'Using the extract, explain why GDP per capita may overstate the living standards of Luxembourg\'s residents.', 'Output of cross-border commuters is in the numerator (GDP) but they are not in the population denominator, so GDP per capita is inflated; GNI per capita (which subtracts income paid to non-residents) is lower and better reflects residents\' income.')],
  evaluate=[('GNI per capita at PPP is the most useful single measure for comparing living standards between countries.', ['adjusts for population size', 'adjusts for price-level differences', 'includes net income from abroad, reflecting residents\' incomes'],
             ['ignores distribution of income', 'excludes non-market and informal output', 'ignores environmental costs, leisure and quality of life', 'PPP estimates rely on price surveys that may be inaccurate'], 'It is the best single monetary measure, but comparisons should be supplemented by composite indicators such as the HDI and by inequality data.'),
            ('Official GDP statistics significantly understate economic activity in developing countries.', ['large informal sectors are hard to record', 'subsistence agriculture and household production are unmeasured', 'out-of-date base years (e.g. Nigeria before 2014)'],
             ['statistical offices estimate informal output using surveys', 'some activity is also overstated (e.g. MNC transfer pricing)', 'understatement also exists in high-income countries'], 'GDP is likely understated where informality is high, so comparisons over time are more reliable than comparisons of levels between countries.')],
  extended=[('Country X has GDP of $50 bn, net income from abroad of −$4 bn and a population of 20 million. Country Y has GDP of $46 bn, net income from abroad of +$3 bn and a population of 14 million. Calculate GNI per capita for each country and explain which data you would use to judge which has the higher living standards.', 'GNI X = $46 bn → $2,300 per person; GNI Y = $49 bn → $3,500 per person. Y appears better off; but use PPP-adjusted figures, distribution (Gini) and non-income indicators (HDI) before concluding.', 6, 'multi_step')],
  )

DEFL_FRAMES = [
    '{e}\'s nominal GDP in {y} was ${N} bn and the GDP deflator (base year = 100) was {D}.',
    'Statistics for {e}, {y}: nominal GDP ${N} bn; price deflator {D} (base year 100).',
    'A central bank bulletin reports that in {y} {e} produced output worth ${N} bn at current prices, when the GDP deflator stood at {D}.',
    'In {y}, the value of all final output in {e} at current prices was ${N} bn. The price index used to deflate GDP was {D} (base year = 100).',
]


@calc('ch01-st2', 'C3', (1, 5))
def real_gdp(rng, slot):
    e = ec(rng)
    y1 = rng.randint(2015, 2021)
    N1 = rng.randint(200, 900)
    D1 = rng.choice([100, 104, 106, 110, 112, 115, 120])
    R1 = N1 * 100 / D1
    intro = rng.choice(DEFL_FRAMES).format(e=e, y=y1, N=N1, D=D1)
    if slot.d <= 2:
        return dict(stem=intro + ' Calculate real GDP.', answer=f'${R1:.1f} bn',
                    markingKey=MK(f'Real GDP = nominal GDP × 100 / deflator = {N1} × 100 / {D1} = {R1:.1f}.', f'${R1:.1f} bn'), marks=2)
    g = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
    infl = rng.choice([1, 2, 3, 5, 6, 8, 9])
    N2 = round(N1 * (1 + g / 100))
    D2 = round(D1 * (1 + infl / 100), 1)
    R2 = N2 * 100 / D2
    rg = pct(R2, R1)
    if slot.d == 3:
        return dict(stem=intro + f' In {y1 + 1} nominal GDP was ${N2} bn and the deflator was {D2}. Calculate real GDP in both years and the real growth rate.',
                    answer=f'Real GDP {y1}: ${R1:.1f} bn; {y1 + 1}: ${R2:.1f} bn; real growth ≈ {rg:.1f}%',
                    markingKey=MK(f'{N1}×100/{D1} = {R1:.1f}; {N2}×100/{D2} = {R2:.1f}; ({R2:.1f} − {R1:.1f})/{R1:.1f} × 100 = {rg:.1f}%.', f'{rg:.1f}%'), marks=3)
    p1 = rng.choice([10, 15, 20, 30, 45])
    p2 = round(p1 * (1 + rng.choice([-1, 0, 1, 2, 3]) / 100), 2)
    pc1, pc2 = R1 * 1000 / p1, R2 * 1000 / p2
    pg = pct(pc2, pc1)
    return dict(stem=intro + f' In {y1 + 1} nominal GDP was ${N2} bn and the deflator was {D2}. The population was {p1} million in {y1} and {p2} million in {y1 + 1}. Calculate the percentage change in real GDP per capita and comment on what it suggests about living standards.',
                answer=f'Real GDP per capita: ${pc1:,.0f} → ${pc2:,.0f}, a change of {pg:.1f}%. {"Average real output per person rose, suggesting higher material living standards (but distribution and non-income factors are unknown)." if pg > 0 else "Average real output per person fell, suggesting lower material living standards despite rising nominal GDP."}',
                markingKey=MK(f'Real GDP {R1:.1f} and {R2:.1f}; per capita ${pc1:,.0f} and ${pc2:,.0f}; change = {pg:.1f}%.', f'{pg:.1f}%') + ' [R1] comment linked to the sign of the change and a limitation.', marks=4 if slot.d == 4 else 6)


@calc('ch01-st2', 'C3', (2, 4))
def deflator_find(rng, slot):
    e = ec(rng)
    R = rng.randint(300, 800)
    D = rng.choice([103, 105, 108, 110, 115, 118, 125])
    N = round(R * D / 100)
    Dx = N * 100 / R
    frame = rng.choice([f'In {e}, nominal GDP is ${N} bn and real GDP (at base-year prices) is ${R} bn.',
                        f'An economist finds that {e}\'s output at current prices is ${N} bn, while the same output at constant base-year prices is ${R} bn.',
                        f'Data for {e}: GDP at current prices ${N} bn; GDP at constant prices ${R} bn.'])
    return dict(stem=frame + ' Calculate the GDP deflator and state what it shows about the price level since the base year.',
                answer=f'Deflator = {Dx:.1f}; the average price level of domestic output is about {Dx - 100:.1f}% higher than in the base year.',
                markingKey=MK(f'Deflator = nominal/real × 100 = {N}/{R} × 100 = {Dx:.1f}.', f'{Dx:.1f}') + ' [R1] interpretation relative to base year = 100.', marks=3)


@calc('ch01-st2', 'C1', (1, 3), 'mcq')
def real_mcq(rng, slot):
    N = rng.choice([220, 330, 440, 550, 660, 770, 880, 990])
    D = rng.choice([110, 120, 125, 150])
    v = N * 100 / D
    return nmcq(rng, f'Nominal GDP is ${N} bn and the GDP deflator is {D}. What is real GDP?', v,
                [N * D / 100, N - (D - 100), N, N / D], f'Real GDP = {N} × 100 / {D} = {r2(v)}.', f=lambda v: f'${r2(v)} bn')


S('ch01-st2',
  terms=[('GDP deflator', 'a price index of all domestically produced final goods and services, used to convert nominal GDP into real GDP'),
         ('base year', 'the reference year whose prices are used to value output in constant-price (real) series, with the price index set to 100'),
         ('real GDP per capita', 'real GDP divided by the population; average inflation-adjusted output per person'),
         ('constant prices', 'prices of a fixed base year used to value output so that only changes in quantity are measured')],
  facts=[('Which of the following is the formula for real GDP?', 'Nominal GDP × 100 / price deflator', ['Nominal GDP × price deflator / 100', 'Nominal GDP − inflation rate', 'Nominal GDP / population'], 'Dividing by the deflator (÷100) removes the effect of price changes.'),
         ('If nominal GDP rises by 5% and the price level rises by 7%, which of the following is true?', 'Real GDP has fallen by about 2%', ['Real GDP has risen by about 12%', 'Real GDP has risen by 2%', 'Real GDP is unchanged'], 'Real growth ≈ nominal growth − inflation = 5 − 7 = −2%.'),
         ('In the base year, which of the following is true of the GDP deflator?', 'It equals 100, so nominal and real GDP are equal', ['It equals 0', 'It equals the inflation rate', 'It equals real GDP growth'], 'By definition the index = 100 in the base year.')],
  why=[('Explain why economists use real rather than nominal GDP to measure economic growth.', 'Nominal GDP can rise purely because prices rise; real GDP removes inflation so changes reflect changes in the volume of goods and services produced.'),
       ('Explain why real GDP per capita can fall even when real GDP rises.', 'If population grows faster than real output, the same output is shared among more people, so average output per person falls.'),
       ('Explain why the choice of base year can affect measured real GDP growth.', 'Real GDP weights each good by base-year prices; goods whose relative prices have fallen sharply (e.g. electronics) get too much or too little weight if the base year is old, so statistical agencies rebase or use chain-linked indices.')],
  contrast=[('the GDP deflator', 'the consumer price index', 'The GDP deflator covers the prices of all domestically produced final output (including investment and government goods, excluding imports); the CPI covers a fixed basket of goods and services bought by typical households, including imports.')],
  misc=[('If the GDP deflator rises from 100 to 110, real GDP must have fallen by 10%.', 'The deflator shows the price level; real GDP depends on nominal GDP as well. If nominal GDP rose by more than 10%, real GDP rose.'),
        ('Real GDP is always smaller than nominal GDP.', 'Only after the base year when prices have risen; before the base year, or if prices fall (deflation), real GDP can exceed nominal GDP.'),
        ('A rise in real GDP per capita proves that everyone is better off.', 'It is an average: the gains may go to a small group, and it ignores leisure, the environment and non-market output.')],
  cases=[('Zimbabwe in 2008', 'With annual inflation estimated in the hundreds of millions of per cent in 2008, nominal values became meaningless while real output collapsed.', 'the importance of distinguishing real from nominal values', 'nominal GDP soared while real GDP fell, so only deflated data showed the true fall in production'),
         ('Japan in the late 1990s and 2000s', 'Japan experienced mild deflation for long periods, so the GDP deflator fell year after year.', 'the relationship between nominal and real GDP', 'with falling prices, real GDP grew faster than nominal GDP, the reverse of the usual case'),
         ('Nigeria\'s population growth', 'Nigeria\'s population has grown by around 2.5% a year, while real GDP growth in 2016-2023 often averaged below that rate.', 'real GDP per capita', 'when population growth exceeds real GDP growth, real GDP per capita falls even though the economy is growing')],
  evaluate=[('Real GDP per capita is an adequate measure of changes in a country\'s economic well-being over time.', ['removes inflation and population effects', 'data are widely available and comparable over time', 'strongly correlated with health and education outcomes'],
             ['ignores distribution', 'ignores environmental degradation and resource depletion', 'excludes unpaid and informal work', 'ignores leisure and quality of goods'], 'It is a necessary but not sufficient measure; changes in inequality, sustainability and non-income indicators must also be considered.')],
  extended=[('In 2022 nominal GDP was $600 bn with a deflator of 120; in 2023 nominal GDP was $660 bn with a deflator of 126. The population grew from 30 million to 30.6 million. Calculate the change in real GDP per capita and comment on the result.', 'Real GDP 500 → 523.8 bn (+4.76%); per capita $16,667 → $17,118, a rise of about 2.7%. Nominal growth of 10% overstated the improvement; per capita real growth is more modest.', 6, 'multi_step')],
  )


@calc('ch01-st3', 'C3', (2, 5))
def cycle_data(rng, slot):
    e = ec(rng)
    for _ in range(50):
        g = [round(rng.uniform(-1.5, 2.0), 1) for _ in range(8)]
        neg = [i for i in range(7) if g[i] < 0 and g[i + 1] < 0]
        if neg and all(x != 0 for x in g):
            break
    else:
        return None
    qs = [f'Q{(i % 4) + 1} {2022 + i // 4}' for i in range(8)]
    tab = '; '.join(f'{q}: {x:+.1f}%' for q, x in zip(qs, g))
    i = neg[0]
    j = i
    while j + 1 < 8 and g[j + 1] < 0:
        j += 1
    frame = rng.choice([f'Quarterly real GDP growth rates for {e} were: {tab}.',
                        f'The table shows quarter-on-quarter changes in real GDP for {e} — {tab}.',
                        f'{e}\'s statistics agency publishes the following real GDP growth data (quarter on quarter): {tab}.'])
    return dict(stem=frame + ' Using the common definition, identify when the economy entered recession, and explain which phase of the business cycle the economy was in at the end of the period.',
                answer=f'A recession (two consecutive quarters of negative real GDP growth) began in {qs[i]} and lasted to {qs[j]}. At the end ({qs[-1]}, growth {g[-1]:+.1f}%) the economy was in {"an expansion/recovery phase" if g[-1] > 0 else "a contraction"}.',
                markingKey=f'[A1] recession identified from {qs[i]} (first of two consecutive negative quarters); [R1] definition stated; [A1][R1] final phase: {"positive growth means output is rising – recovery/expansion" if g[-1] > 0 else "negative growth means contraction"}.', marks=4)


@calc('ch01-st3', 'C3', (2, 5))
def output_gap(rng, slot):
    e = ec(rng)
    pot = rng.randint(400, 1200)
    gap = rng.choice([-6, -4, -3, -2, 2, 3, 5])
    act = round(pot * (1 + gap / 100))
    g = 100 * (act - pot) / pot
    kind = 'positive (inflationary) output gap' if g > 0 else 'negative (deflationary/recessionary) output gap'
    frame = rng.choice([f'The OECD estimates that {e}\'s potential output is ${pot} bn, while actual real GDP is ${act} bn.',
                        f'{e}: actual real GDP ${act} bn; estimated potential (trend) GDP ${pot} bn.',
                        f'The finance ministry of {e} estimates that, at full employment, the economy could produce ${pot} bn; actual output this year is ${act} bn.'])
    return dict(stem=frame + ' Calculate the output gap as a percentage of potential output, and state what type of gap it is and one likely consequence.',
                answer=f'Output gap = ({act} − {pot})/{pot} × 100 = {g:.1f}%: a {kind}. {"Likely consequence: inflationary pressure as resources are over-used." if g > 0 else "Likely consequence: cyclical unemployment and spare capacity."}',
                markingKey=MK(f'({act} − {pot})/{pot} × 100 = {g:.1f}%.', f'{g:.1f}%') + f' [A1] {kind}; [R1] consequence.', marks=4)


S('ch01-st3',
  diag=[('the business cycle, showing the long-term growth trend and the phases of expansion, peak, contraction and trough', 'Real GDP on the y-axis against time; fluctuating line around an upward-sloping trend line; label peak, contraction (recession), trough, expansion (recovery); explain that actual output deviates from potential output, creating positive and negative output gaps.')],
  terms=[('business cycle', 'the short-term fluctuations of real GDP around its long-term growth trend, consisting of expansion, peak, contraction and trough'),
         ('recession', 'a fall in real GDP for at least two consecutive quarters'),
         ('long-term growth trend', 'the average rate of growth of real GDP over a long period, reflecting the growth of potential output'),
         ('output gap', 'the difference between actual real GDP and potential real GDP, as a percentage of potential GDP'),
         ('potential output', 'the real GDP an economy could produce when all its resources are fully employed at the natural rate of unemployment')],
  facts=[('Which of the following occurs during the contraction phase of the business cycle?', 'Real GDP falls and cyclical unemployment rises', ['Inflationary pressure increases strongly', 'Firms run short of skilled labour', 'Tax revenues rise faster than GDP'], 'Falling output reduces demand for labour.'),
         ('Which of the following describes a peak?', 'The highest point of real GDP before a contraction begins', ['The lowest point of the cycle', 'The point where the trend line begins', 'Two quarters of negative growth'], 'At the peak the economy is usually operating above potential.'),
         ('Which of the following would shift the long-term growth trend upwards?', 'An increase in the quantity or quality of factors of production', ['A temporary rise in consumer confidence', 'A fall in interest rates for one quarter', 'A one-off rise in exports'], 'The trend reflects growth in potential output (LRAS).'),
         ('Which statement about a negative output gap is correct?', 'Actual output is below potential output and there is spare capacity', ['Actual output is above potential output', 'Inflation is rising rapidly', 'Unemployment is below its natural rate'], 'A negative (deflationary) gap implies unemployed resources.')],
  why=[('Explain why unemployment tends to rise during the contraction phase of the business cycle.', 'Falling AD reduces firms\' sales; as labour is a derived demand, firms cut output and jobs, so cyclical (demand-deficient) unemployment rises.'),
       ('Explain why inflation tends to accelerate near the peak of the business cycle.', 'Output is above potential, resources are scarce, firms bid up wages and input prices and can pass costs on as demand is strong, so demand-pull and cost pressures build.'),
       ('Explain why the long-term growth trend can be shown on a PPC diagram as an outward shift.', 'The trend reflects increases in productive capacity from more or better factors of production and technology, which shift the production possibilities curve outward (and LRAS to the right).')],
  contrast=[('short-term fluctuations in real GDP', 'long-term economic growth', 'Short-term fluctuations are movements of actual output around potential, mainly caused by changes in AD; long-term growth is the increase in potential output caused by more or better resources and technology.'),
            ('actual growth', 'potential growth', 'Actual growth is the increase in real GDP produced; potential growth is the increase in the economy\'s capacity to produce, shown by an outward PPC shift or rightward LRAS shift.')],
  misc=[('A recession means that real GDP is negative.', 'A recession means that real GDP growth is negative (output falls) for two consecutive quarters; the level of GDP remains positive.'),
        ('When growth slows from 4% to 1%, the economy is in recession.', 'Output is still rising, so this is a slowdown, not a recession; a recession requires falling real GDP.'),
        ('During an expansion the economy is always above its long-term trend.', 'An expansion begins at a trough below trend; output may still be below potential (negative output gap) for much of the recovery.')],
  cases=[('the 2008-2009 global financial crisis', 'Real GDP in the USA fell for four consecutive quarters from mid-2008 and unemployment rose from under 5% to 10% by October 2009.', 'the contraction phase of the business cycle', 'the fall in household wealth and credit reduced C and I, AD fell, output fell below potential and cyclical unemployment rose'),
         ('the UK economy in 2020', 'UK real GDP fell by about 10% in 2020, the largest annual fall in over 300 years, before rebounding by more than 8% in 2021.', 'fluctuations around the long-term trend', 'a sharp fall in AD and supply during lockdowns created a deep trough, followed by a rapid expansion as restrictions were lifted'),
         ('China\'s growth since 1980', 'China averaged close to 10% annual real GDP growth from 1980 to 2010, slowing to around 5% in the 2020s.', 'the long-term growth trend', 'rapid accumulation of capital, rural-urban migration and technology transfer raised potential output, but the trend rate slows as catch-up opportunities shrink')],
  evaluate=[('Governments should aim to eliminate the business cycle.', ['recessions cause unemployment, lost output and hysteresis', 'booms cause inflation and asset bubbles', 'stable growth improves business confidence and investment'],
             ['cycles are partly caused by supply shocks governments cannot control', 'policy has time lags and may destabilise', 'some fluctuation reallocates resources to more productive uses'], 'Governments should aim to smooth rather than eliminate the cycle, using automatic stabilisers and credible monetary policy.')],
  extended=[('Real GDP of an economy was $500 bn in 2020, $490 bn in 2021, $505 bn in 2022 and $530 bn in 2023, while potential output grew by 2% a year from $510 bn in 2020. Calculate the output gap in 2020 and 2023 and describe how the economy moved through the business cycle.', '2020: (500 − 510)/510 = −2.0%; potential 2023 = 510 × 1.02³ ≈ 541.2, gap = (530 − 541.2)/541.2 ≈ −2.1%. Contraction in 2021 (−2%), trough 2021, then recovery/expansion in 2022-23, but output remains below potential (negative gap).', 6, 'multi_step')],
  )

S('ch01-st4',
  terms=[('OECD Better Life Index', 'an interactive composite index that compares well-being across OECD countries using 11 dimensions such as housing, income, jobs, community, education, environment, health and life satisfaction'),
         ('Happiness Index', 'the World Happiness Report ranking of countries by average life evaluations (the Cantril ladder), explained by GDP per capita, social support, healthy life expectancy, freedom, generosity and perceived corruption'),
         ('Happy Planet Index (HPI)', 'an index that combines life expectancy and well-being with the ecological footprint, measuring how efficiently countries achieve long, happy lives'),
         ('green GDP', 'GDP adjusted by subtracting the value of environmental degradation and natural resource depletion')],
  facts=[('Which of the following is excluded from GDP and is therefore a limitation of it as a measure of well-being?', 'Unpaid caring and household work', ['Government spending on schools', 'Exports of services', 'Business investment'], 'Non-market production is not valued in GDP.'),
         ('Which country is known for using Gross National Happiness as an official development goal?', 'Bhutan', ['Singapore', 'Qatar', 'Luxembourg'], 'Bhutan\'s constitution (2008) commits the state to promote Gross National Happiness.'),
         ('Which of the following does the Happy Planet Index include that GDP does not?', 'The ecological footprint', ['Net exports', 'The GDP deflator', 'Gross fixed capital formation'], 'HPI divides well-being × life expectancy by ecological footprint.'),
         ('Which country introduced a "Wellbeing Budget" in 2019 that judged spending against well-being indicators?', 'New Zealand', ['Germany', 'Brazil', 'South Korea'], 'New Zealand\'s 2019 budget prioritised mental health, child poverty and environmental goals.')],
  why=[('Explain why GDP may be an inaccurate indicator of economic well-being.', 'It excludes non-market output, the informal economy, leisure and the quality of goods; it ignores distribution and counts "defensive" spending (e.g. pollution clean-up) and environmental depletion as positive output.'),
       ('Explain why a natural disaster can raise measured GDP.', 'Reconstruction spending adds to GDP, but the destroyed capital and lost welfare are not subtracted, so GDP can rise even though well-being has fallen.'),
       ('Explain why the Happy Planet Index can rank a middle-income country such as Costa Rica above high-income countries.', 'HPI rewards high well-being and life expectancy achieved with a small ecological footprint; Costa Rica achieves high life satisfaction and long lives with low resource use, while many rich countries have very large footprints.')],
  contrast=[('GDP', 'the OECD Better Life Index', 'GDP is a single monetary measure of market output; the Better Life Index is a multidimensional measure of well-being across 11 dimensions, which users can weight according to their own priorities.')],
  misc=[('Countries with the highest GDP per capita always have the happiest citizens.', 'Happiness rises with income but at a diminishing rate; social support, freedom, health and trust matter too, so the World Happiness Report ranking differs from the GDP ranking (e.g. Finland ranks first though not richest).'),
        ('Because GDP ignores the environment, it should never be used.', 'GDP remains useful for measuring output, cycles and tax capacity; the point is to supplement it with environmental and well-being indicators.')],
  cases=[('Finland\'s top ranking in the World Happiness Report', 'Finland has ranked first in the World Happiness Report every year from 2018 to 2025, despite a GDP per capita lower than those of Norway, Switzerland or the USA.', 'the limitations of GDP as a measure of well-being', 'high social trust, social support, low corruption and strong public services raise life evaluations beyond what income alone predicts'),
         ('China\'s attempt to publish a green GDP in 2006', 'China\'s first green GDP report estimated environmental costs at about 3% of GDP in 2004, but the project was shelved after provincial officials objected.', 'alternative measures that account for the environment', 'subtracting pollution costs lowers measured growth, revealing the trade-off between rapid growth and environmental quality'),
         ('Bhutan\'s Gross National Happiness', 'Bhutan measures progress through a GNH index across nine domains, including psychological well-being, ecological diversity and good governance.', 'well-being indicators beyond GDP', 'policy is judged by broad well-being, not only income growth, for example by protecting forests and culture')],
  evaluate=[('Composite indicators such as the Happy Planet Index should replace GDP as the main measure of economic success.', ['capture well-being, health and sustainability', 'encourage sustainable policy', 'GDP counts harmful activity as positive'],
             ['weighting of components is subjective', 'subjective well-being surveys are culturally biased', 'GDP is needed for macro policy, tax and debt analysis', 'composite measures are published infrequently'], 'They should complement, not replace, GDP: a dashboard of indicators gives the fullest picture.')],
  )


# =============================================================================================
# ch02 Unit 3.2 Aggregate demand and aggregate supply
# =============================================================================================
@calc('ch02-st1', 'C3', (1, 4))
def ad_change(rng, slot):
    e = ec(rng)
    dC = rng.choice([-30, -20, -12, -8, 6, 10, 15, 25])
    dI = rng.choice([-25, -15, -10, -5, 4, 8, 12])
    dG = rng.choice([-10, -5, 0, 8, 15, 20])
    dX = rng.choice([-20, -10, -6, 5, 9, 14])
    dM = rng.choice([-12, -6, 4, 8, 11])
    net = dC + dI + dG + dX - dM
    def s(v):
        return f'rose by ${v} bn' if v > 0 else f'fell by ${-v} bn' if v < 0 else 'was unchanged'
    frame = rng.choice([f'Over the past year in {e}, consumption {s(dC)}, investment {s(dI)}, government spending {s(dG)}, exports {s(dX)} and imports {s(dM)}.',
                        f'A briefing on {e} reports: household spending {s(dC)}; business investment {s(dI)}; public spending {s(dG)}; export sales {s(dX)}; spending on imports {s(dM)}.',
                        f'In {e}: C {s(dC)}, I {s(dI)}, G {s(dG)}, X {s(dX)} and M {s(dM)} compared with the previous year.'])
    return dict(stem=frame + ' Calculate the change in aggregate demand and state the direction in which the AD curve shifts.',
                answer=f'ΔAD = {dC} + {dI} + {dG} + {dX} − ({dM}) = {bn(net)}; AD shifts to the {"right" if net > 0 else "left" if net < 0 else "neither side"}.',
                markingKey=MK(f'ΔAD = ΔC + ΔI + ΔG + ΔX − ΔM = {net}.', f'{bn(net)}') + ' [A1] direction of shift.', marks=3)


S('ch02-st1',
  diag=[('the effect of a fall in consumer confidence on aggregate demand and real output', 'AD/AS diagram: AD shifts left from AD1 to AD2 along SRAS; real GDP falls from Y1 to Y2 and the price level from P1 to P2; explain lower C via precautionary saving.'),
        ('why the AD curve slopes downwards', 'Price level against real GDP; downward-sloping AD explained by the wealth effect, interest-rate effect and international trade effect (not the substitution effect for a single good).')],
  terms=[('aggregate demand (AD)', 'the total planned spending on an economy\'s goods and services at each possible price level in a given period: C + I + G + (X − M)'),
         ('consumption (C)', 'total spending by households on goods and services'),
         ('investment (I)', 'spending by firms on capital goods such as machinery, buildings and technology, plus changes in inventories'),
         ('net exports (X − M)', 'the value of exports minus the value of imports'),
         ('wealth effect', 'the change in consumption caused by a change in the real value of households\' wealth, for example when the price level or asset prices change')],
  facts=[('Which of the following would shift the AD curve to the right?', 'A fall in interest rates that encourages borrowing', ['A rise in the price level', 'An increase in income tax', 'An appreciation of the currency'], 'Lower interest rates raise C and I.'),
         ('Which of the following causes a movement along the AD curve rather than a shift?', 'A change in the average price level', ['A change in consumer confidence', 'A change in government spending', 'A change in foreign incomes'], 'The price level is on the axis; other determinants shift AD.'),
         ('Which of the following is usually the largest component of AD in high-income economies?', 'Consumption', ['Investment', 'Government spending', 'Net exports'], 'Household consumption is typically 50-70% of GDP.'),
         ('Which of the following would reduce net exports?', 'Faster income growth in the country than in its trading partners', ['A depreciation of the currency', 'Higher incomes abroad', 'Lower domestic inflation than abroad'], 'Rising domestic incomes raise imports.')],
  why=[('Explain why the AD curve slopes downwards from left to right.', 'A lower price level raises the real value of wealth (wealth effect), lowers interest rates as less money is needed for transactions (interest-rate effect), and makes exports more competitive (trade effect), so real spending rises.'),
       ('Explain why a fall in house prices can reduce aggregate demand.', 'Households feel poorer (negative wealth effect) and have less collateral for borrowing, so they cut consumption; residential investment also falls.'),
       ('Explain why an increase in business confidence can shift AD to the right.', 'Firms expect higher future sales and profits, so they invest more in capital goods, raising I and therefore AD at every price level.'),
       ('Explain why an appreciation of the currency tends to reduce aggregate demand.', 'Exports become more expensive to foreigners and imports cheaper to domestic buyers, so (X − M) falls, shifting AD to the left.')],
  contrast=[('a movement along the AD curve', 'a shift of the AD curve', 'A movement is caused only by a change in the average price level; a shift is caused by a change in any determinant of C, I, G or X − M at a given price level.'),
            ('consumption', 'investment', 'Consumption is household spending on goods and services for current use; investment is firms\' spending on capital goods that add to productive capacity.')],
  misc=[('The AD curve slopes down because consumers buy more of a good when its price falls.', 'That is the substitution effect for a single good; AD slopes down because of the wealth, interest-rate and international trade effects when the overall price level changes.'),
        ('Buying shares on the stock market counts as investment in AD.', 'In economics, investment means spending on new capital goods; buying shares is a financial transaction (saving), not investment.'),
        ('Higher imports increase aggregate demand because people are spending more.', 'Imports are spending on foreign output, so they are subtracted: higher M reduces AD for domestic output.')],
  cases=[('the Covid-19 shock to consumption in 2020', 'In 2020 household saving rates in the euro area rose to about 25% of disposable income in Q2 as lockdowns and uncertainty cut spending.', 'determinants of consumption', 'lower confidence and restricted opportunities to spend increased saving, so C and AD fell sharply'),
         ('China\'s property slowdown after 2021', 'After the Evergrande crisis, property investment in China fell for several consecutive years and house prices declined.', 'the role of investment and wealth in AD', 'falling construction investment and a negative wealth effect on households reduced AD and contributed to slower growth'),
         ('Germany\'s export dependence', 'Exports of goods and services are close to half of German GDP, so slower growth in China and the euro area hit German manufacturing in 2023.', 'net exports as a component of AD', 'lower foreign incomes reduced demand for German exports, shifting AD left')],
  evaluate=[('Consumer confidence is the most important determinant of aggregate demand.', ['C is the largest component of AD', 'confidence changes amplify cycles through saving', 'confidence also affects investment'],
             ['investment is more volatile and drives cycles', 'in open economies exports matter more (e.g. Germany, Ireland)', 'confidence often follows rather than causes changes in income', 'interest rates and fiscal policy shape spending'], 'Confidence is important because C is large, but the most important determinant depends on the economy and the shock; in small open economies foreign demand often dominates.')],
  extended=[('Using the components of aggregate demand, explain how a 2-percentage-point rise in interest rates could affect AD in an economy where most mortgages have variable rates.', 'Higher mortgage payments reduce disposable income and C; borrowing for durables falls; firms\' cost of borrowing rises so I falls; higher rates may attract hot money, appreciating the currency and reducing X − M; AD shifts left. Effect larger with variable-rate mortgages.', 6, 'explain')],
  )

S('ch02-st2',
  diag=[('the effect of a sharp rise in oil prices on short-run aggregate supply', 'AD/AS diagram: SRAS shifts left from SRAS1 to SRAS2; price level rises and real GDP falls (stagflation); explain higher costs of production.')],
  terms=[('short-run aggregate supply (SRAS)', 'the total quantity of real output firms plan to produce at each price level in the short run, when wages and other resource prices are fixed'),
         ('supply shock', 'an unexpected event that changes the costs of production and shifts SRAS'),
         ('sticky wages', 'money wages that do not adjust quickly to changes in the price level because of contracts and other factors'),
         ('costs of production', 'the prices firms pay for factors of production such as wages, raw materials, energy and imported inputs')],
  facts=[('Which of the following would shift the SRAS curve to the left?', 'A rise in the price of imported raw materials', ['A fall in nominal wages', 'A government subsidy to firms', 'An improvement in technology'], 'Higher input costs reduce the output firms supply at each price level.'),
         ('Why does the SRAS curve slope upwards?', 'In the short run output prices rise while wages and other costs are fixed, so profits and production rise', ['Consumers buy more at higher prices', 'Higher prices reduce costs', 'Firms always operate at full capacity'], 'With sticky resource prices, higher output prices raise profitability.'),
         ('Which of the following would shift SRAS to the right?', 'A cut in indirect taxes on business inputs', ['An increase in the minimum wage', 'A depreciation that raises import prices', 'A drought that destroys crops'], 'Lower business costs increase SRAS.')],
  why=[('Explain why a rise in the minimum wage could shift the SRAS curve to the left.', 'Wages are a cost of production; higher labour costs reduce the profitability of each level of output, so firms supply less at every price level.'),
       ('Explain why a depreciation of the currency can shift SRAS to the left.', 'Imported raw materials, components and energy become more expensive in domestic currency, raising firms\' costs of production.'),
       ('Explain why the SRAS curve becomes steeper as output approaches full capacity.', 'Spare resources run out; firms must pay overtime and higher prices to attract scarce labour and inputs, so further output is only supplied at much higher prices.')],
  contrast=[('a change in the price level', 'a change in costs of production', 'A change in the price level causes a movement along SRAS; a change in costs of production (wages, raw materials, taxes, subsidies) shifts the SRAS curve.')],
  misc=[('A fall in AD shifts the SRAS curve to the left.', 'A fall in AD moves the economy along the SRAS curve to lower output and price level; SRAS shifts only when costs of production change.'),
        ('A new subsidy for firms shifts AD to the right because firms have more money.', 'A production subsidy lowers firms\' costs, so it shifts SRAS to the right (it may also affect AD indirectly).')],
  cases=[('the 1973-74 oil crisis', 'OPEC\'s oil embargo quadrupled oil prices; many Western economies experienced rising inflation and falling output (stagflation).', 'a negative supply shock', 'higher energy costs raised costs of production across industries, shifting SRAS left, raising the price level and lowering real GDP'),
         ('European energy prices in 2022', 'After Russia\'s invasion of Ukraine, wholesale gas prices in Europe rose to more than ten times their pre-pandemic levels in August 2022.', 'determinants of SRAS', 'energy-intensive firms faced much higher costs, some cut production, and inflation in the euro area peaked at 10.6% in October 2022'),
         ('global shipping costs during 2021', 'The cost of shipping a container from Asia to Europe rose more than five-fold in 2021 because of port congestion and container shortages.', 'cost-push pressure on SRAS', 'higher transport costs raised input costs for importers and producers, shifting SRAS left')],
  evaluate=[('Supply shocks are a more serious problem for policymakers than demand shocks.', ['create a trade-off: rising inflation and falling output', 'demand-side policy cannot fix both', 'may raise inflation expectations'],
             ['demand shocks can cause deep recessions (2008)', 'supply shocks are often temporary', 'credible central banks can look through temporary price rises'], 'Negative supply shocks are harder to manage because they create stagflation, but their seriousness depends on duration and on whether inflation expectations stay anchored.')],
  )

S('ch02-st3',
  diag=[('the monetarist/new classical LRAS curve at the full-employment level of output', 'Vertical LRAS at Yp; AD shifts change only the price level in the long run because wages and prices are flexible; SRAS adjusts.'),
        ('the Keynesian AS curve with its three sections', 'Horizontal section (spare capacity: output rises with no price rise), upward-sloping section (bottlenecks) and vertical section at full employment Yf; explain why AD increases affect output and price differently in each section.')],
  terms=[('long-run aggregate supply (LRAS)', 'the real output an economy can produce when all resources are fully employed and wages and prices have fully adjusted; in the monetarist view a vertical line at potential output'),
         ('Keynesian AS curve', 'an aggregate supply curve with a horizontal section at low output, an upward-sloping section and a vertical section at full-employment output'),
         ('full employment level of output', 'the real GDP produced when unemployment is at its natural rate'),
         ('wage and price flexibility', 'the ability of wages and prices to adjust downwards and upwards in response to market conditions')],
  facts=[('In the monetarist/new classical model, what happens in the long run after an increase in AD?', 'The price level rises but real output returns to potential output', ['Real output rises permanently', 'The price level falls', 'Unemployment falls permanently'], 'LRAS is vertical; wages adjust to the higher price level.'),
         ('In the Keynesian model, what happens if AD increases when the economy is on the horizontal section of the AS curve?', 'Real output rises with no increase in the price level', ['Only the price level rises', 'Output falls', 'The AS curve shifts left'], 'Spare capacity allows output to rise without cost pressure.'),
         ('Which of the following shifts the LRAS curve to the right?', 'Improvements in the quality of education and training', ['An increase in consumer spending', 'A fall in the price level', 'A cut in interest rates'], 'Better human capital raises potential output.'),
         ('Why did Keynes argue that the economy could remain in a deflationary gap for a long time?', 'Wages and prices are sticky downwards', ['Wages are perfectly flexible', 'Saving always equals investment', 'Supply creates its own demand'], 'Money wages rarely fall, so markets do not clear quickly.')],
  why=[('Explain why the monetarist LRAS curve is vertical.', 'In the long run wages and prices are flexible, so any change in the price level is matched by changes in costs; output is determined by the quantity and quality of resources and technology, not the price level.'),
       ('Explain why the Keynesian AS curve has a horizontal section.', 'With high unemployment and spare capacity, firms can expand output by using idle labour and capital without bidding up wages or input prices.'),
       ('Explain why both monetarists and Keynesians agree that improvements in technology raise potential output.', 'Technology increases the productivity of factors of production, shifting the vertical LRAS (or the vertical section of the Keynesian AS) to the right in both models.')],
  contrast=[('the monetarist/new classical view of LRAS', 'the Keynesian view of AS', 'Monetarists see LRAS as vertical at potential output because wages and prices are flexible, so the economy self-corrects; Keynesians see a horizontal section where output can stay below full employment because wages are sticky, so demand management is needed.')],
  misc=[('In the Keynesian model, an increase in AD always causes inflation.', 'On the horizontal section of the Keynesian AS curve, higher AD increases real output without raising the price level.'),
        ('Monetarists believe that AD has no effect on the economy at all.', 'Monetarists accept AD affects output in the short run along SRAS; in the long run only the price level is affected.')],
  cases=[('the Great Depression of the 1930s', 'US unemployment reached about 25% in 1933 and stayed above 14% for most of the decade.', 'the Keynesian view of aggregate supply', 'the economy did not quickly self-correct; prices fell but output stayed far below full employment, which supported Keynes\'s case for government spending'),
         ('the US recovery after the 2008 crisis', 'After 2009 US unemployment took until 2016 to return to about 5%, and core inflation stayed below 2% for most of the period.', 'spare capacity in the Keynesian model', 'output could expand for years without inflationary pressure, consistent with a flat section of the AS curve')],
  evaluate=[('Economies will always return to full employment without government intervention.', ['wages and prices adjust over time', 'falling prices raise real wealth and AD', 'intervention may cause crowding out and inflation'],
             ['wages are sticky downwards, so adjustment can take years', 'hysteresis: long-term unemployment reduces potential output', 'deflation can reduce AD further (debt-deflation)', 'the 1930s and 2010s show slow recoveries'], 'Self-correction may occur in the long run, but the costs of waiting can be high, which justifies counter-cyclical policy in deep recessions.')],
  )

S('ch02-st4',
  diag=[('a deflationary (recessionary) gap in the monetarist/new classical model and how it is eliminated in the long run', 'Short-run equilibrium where AD meets SRAS at Y1 < Yp; unemployment pushes down wages, SRAS shifts right until it meets AD on LRAS at Yp with a lower price level.'),
        ('an inflationary gap in the Keynesian model', 'AD intersects the vertical section of the Keynesian AS curve; further increases in AD raise only the price level; the gap is the excess of AD over the level needed for full employment output.'),
        ('long-run equilibrium in the monetarist model', 'AD, SRAS and LRAS intersect at potential output Yp and price level P; no output gap; unemployment at the natural rate.')],
  terms=[('short-run equilibrium', 'the level of real output and price level where AD intersects SRAS'),
         ('long-run equilibrium', 'the point where AD, SRAS and LRAS intersect, so output equals potential output'),
         ('deflationary (recessionary) gap', 'the situation where equilibrium real GDP is below potential output, leaving unemployed resources'),
         ('inflationary gap', 'the situation where equilibrium real GDP is above potential output, putting upward pressure on the price level'),
         ('stagflation', 'the combination of rising inflation and falling (or stagnant) real output with rising unemployment')],
  facts=[('In the monetarist model, how is a deflationary gap eliminated without intervention?', 'Unemployment lowers wages, shifting SRAS to the right until output returns to potential', ['AD shifts left until the gap closes', 'LRAS shifts left', 'The price level rises'], 'Flexible wages restore full employment.'),
         ('Which of the following describes an inflationary gap?', 'Real GDP is above potential output and unemployment is below the natural rate', ['Real GDP is below potential output', 'The price level is falling', 'LRAS is to the right of SRAS'], 'Excess demand puts pressure on prices.'),
         ('What is the effect of a fall in AD in the short run in the AD/SRAS model?', 'Real GDP and the price level both fall', ['Real GDP falls and the price level rises', 'Only the price level falls', 'Real GDP rises'], 'Movement down along SRAS.')],
  why=[('Explain why an inflationary gap in the monetarist model eventually closes through higher prices rather than more output.', 'Above potential, labour is scarce, so wages rise; higher costs shift SRAS left until output returns to potential at a higher price level.'),
       ('Explain why a negative supply shock can create stagflation.', 'SRAS shifts left, so at the new equilibrium the price level is higher and real output is lower, meaning inflation and unemployment rise together.'),
       ('Explain why Keynesian economists argue that a deflationary gap may persist.', 'Wages are sticky downwards and falling incomes reduce spending further, so the economy can remain in equilibrium below full employment without AD-boosting policy.')],
  contrast=[('a deflationary gap', 'an inflationary gap', 'A deflationary gap is where equilibrium output is below potential (spare capacity, cyclical unemployment); an inflationary gap is where output is above potential (excess demand, rising prices).'),
            ('short-run equilibrium', 'long-run equilibrium', 'Short-run equilibrium is where AD = SRAS at any output; long-run equilibrium also requires output to equal potential, so AD = SRAS = LRAS.')],
  misc=[('In long-run equilibrium unemployment is zero.', 'Unemployment is at the natural rate (frictional + structural), which is positive.'),
        ('An increase in AD always closes a deflationary gap without any inflation.', 'In the monetarist and in the upward-sloping section of the Keynesian model, higher AD also raises the price level.')],
  cases=[('the US economy in 2021-2022', 'Large fiscal transfers and low interest rates boosted demand; by 2022 US unemployment was about 3.5% and CPI inflation peaked at 9.1% in June 2022.', 'an inflationary gap', 'AD rose above the level consistent with potential output, so prices rose rapidly'),
         ('the euro area in 2012-2014', 'Euro-area unemployment peaked above 12% in 2013 and inflation fell below 1%.', 'a deflationary gap', 'weak AD after the sovereign debt crisis left output below potential, creating spare capacity and low inflation')],
  evaluate=[('Closing a deflationary gap is best left to market forces.', ['avoids fiscal deficits and debt', 'avoids policy errors and lags', 'wage flexibility restores equilibrium'],
             ['slow adjustment raises long-term unemployment', 'hysteresis lowers potential output', 'falling prices can deepen recession'], 'In shallow gaps market forces may suffice; deep and persistent gaps justify active fiscal and monetary support.')],
  )

MULT_FRAMES = [
    'In {e} the marginal propensity to consume is {mpc}.',
    'Households in {e} spend {mpcp}% of every extra dollar of income on domestic goods and services and save the rest.',
    'An economist estimates that in {e}, out of each additional $1 of income, ${mpc} is consumed on domestic output.',
]


@calc('ch02-st5', 'C3', (1, 5))
def multiplier(rng, slot):
    e = ec(rng)
    inj = rng.choice([5, 8, 10, 12, 15, 20, 25, 40])
    what = rng.choice(['government spending on infrastructure', 'investment in a new car plant', 'export orders',
                       'government spending on schools and hospitals', 'investment by a foreign mining company'])
    if slot.d <= 2:
        mpc = rng.choice([0.5, 0.6, 0.75, 0.8, 0.9])
        k = 1 / (1 - mpc)
        stem = rng.choice(MULT_FRAMES).format(e=e, mpc=mpc, mpcp=int(mpc * 100)) + f' Calculate the value of the multiplier and the final change in real GDP following a ${inj} bn increase in {what}.'
        dY = k * inj
        return dict(stem=stem, answer=f'k = 1/(1 − {mpc}) = {r2(k)}; ΔY = {r2(k)} × {inj} = ${r2(dY)} bn',
                    markingKey=MK(f'k = 1/(1 − MPC) = 1/{r2(1 - mpc)} = {r2(k)}; ΔY = k × ΔJ = {r2(dY)}.', f'${r2(dY)} bn'), marks=2)
    mps = rng.choice([0.1, 0.15, 0.2])
    mpt = rng.choice([0.1, 0.15, 0.2, 0.25])
    mpm = rng.choice([0.05, 0.1, 0.15, 0.2, 0.25])
    leak = round(mps + mpt + mpm, 2)
    k = 1 / leak
    dY = k * inj
    intro = rng.choice([f'In {e}, the marginal propensity to save is {mps}, the marginal rate of tax is {mpt} and the marginal propensity to import is {mpm}.',
                        f'For every extra $1 of national income in {e}, {int(mps * 100)} cents are saved, {int(mpt * 100)} cents are paid in tax and {int(mpm * 100)} cents are spent on imports.',
                        f'Data for {e}: MPS = {mps}, MPT = {mpt}, MPM = {mpm}.'])
    if slot.d == 3:
        return dict(stem=intro + f' Calculate the multiplier and the change in real GDP if {what} rises by ${inj} bn.',
                    answer=f'k = 1/({mps} + {mpt} + {mpm}) = {r2(k)}; ΔY = ${r2(dY)} bn',
                    markingKey=MK(f'k = 1/(MPS + MPT + MPM) = 1/{leak} = {r2(k)}; ΔY = {r2(k)} × {inj} = {r2(dY)}.', f'${r2(dY)} bn'), marks=3)
    gap = rng.choice([20, 30, 40, 50, 60])
    need = gap / k
    if slot.d == 4:
        return dict(stem=intro + f' Real GDP is ${gap} bn below potential output. Calculate the increase in government spending needed to close the deflationary gap, assuming no crowding out.',
                    answer=f'k = {r2(k)}; required ΔG = {gap}/{r2(k)} = ${r2(need)} bn',
                    markingKey=MK(f'k = 1/{leak} = {r2(k)}; ΔG = gap / k = {gap} / {r2(k)} = {r2(need)}.', f'${r2(need)} bn'), marks=4)
    mpc = round(1 - leak, 2)
    return dict(stem=intro + f' The government plans an increase in {what} of ${inj} bn. (a) Calculate the marginal propensity to consume domestic output. (b) Calculate the final change in real GDP. (c) Explain two reasons why the actual change may be smaller than your answer to (b).',
                answer=f'(a) MPC (domestic) = 1 − {leak} = {mpc}; (b) ΔY = {inj} × {r2(k)} = ${r2(dY)} bn; (c) crowding out of private investment via higher interest rates; time lags; leakages may rise (e.g. higher saving if confidence is low); the economy may be near capacity so prices rise instead of output.',
                markingKey=MK(f'(a) 1 − ({mps}+{mpt}+{mpm}) = {mpc}; (b) k = {r2(k)}, ΔY = {r2(dY)}.', f'MPC {mpc}, ΔY ${r2(dY)} bn') + ' (c) [R1][R1] two reasons explained.', marks=6)


@calc('ch02-st5', 'C1', (1, 3), 'mcq')
def mult_mcq(rng, slot):
    leak = rng.choice([0.2, 0.25, 0.4, 0.5])
    k = 1 / leak
    inj = rng.choice([10, 20, 30, 40])
    frame = rng.choice([f'If the sum of the marginal propensities to save, tax and import is {leak}, what is the effect on real GDP of a ${inj} bn increase in investment?',
                        f'The marginal propensity to withdraw is {leak}. By how much does national income rise after a ${inj} bn rise in exports?'])
    return nmcq(rng, frame, k * inj, [inj * leak, inj, inj * (1 - leak) * 10, inj / (1 - leak)], f'k = 1/{leak} = {r2(k)}; ΔY = {r2(k * inj)}.', f=lambda v: f'${r2(v)} bn')


S('ch02-st5',
  diag=[('the Keynesian multiplier effect of an increase in government spending', 'Keynesian AS with AD shifting from AD1 to AD2 by the initial injection and further to AD3 through induced consumption; final change in output is k times the injection; on the horizontal section the price level is unchanged.')],
  terms=[('Keynesian multiplier', 'the ratio of the final change in real GDP to the initial change in an injection (I, G or X): k = 1/(1 − MPC) = 1/(MPS + MPT + MPM)'),
         ('marginal propensity to consume (MPC)', 'the fraction of additional income that is spent on domestic consumption'),
         ('marginal propensity to save (MPS)', 'the fraction of additional income that is saved'),
         ('marginal propensity to import (MPM)', 'the fraction of additional income that is spent on imports'),
         ('marginal rate of tax (MRT/MPT)', 'the fraction of additional income that is paid in taxes')],
  facts=[('If MPC = 0.8 in a closed economy with no government, what is the value of the multiplier?', '5', ['0.8', '1.25', '8'], 'k = 1/(1 − 0.8) = 5.'),
         ('Which of the following would increase the size of the multiplier?', 'A fall in the marginal propensity to import', ['A rise in the marginal rate of tax', 'A rise in the marginal propensity to save', 'A rise in interest rates'], 'Smaller leakages mean more income is re-spent.'),
         ('Why is the multiplier usually smaller in small open economies such as Singapore?', 'A large share of extra income is spent on imports', ['They have no taxes', 'Their MPC is equal to 1', 'Their governments spend nothing'], 'A high MPM is a large leakage.')],
  why=[('Explain why an increase in government spending can raise real GDP by more than the initial amount spent.', 'The spending becomes income for workers and firms, who spend a fraction (MPC) of it, creating further rounds of income and spending; the total change is the injection multiplied by k.'),
       ('Explain why the multiplier process eventually stops.', 'At each round a fraction of income leaks out of the circular flow as saving, taxes and imports, so successive rounds of spending become smaller until the total converges.'),
       ('Explain why the multiplier effect may be smaller in practice than the simple formula suggests.', 'Crowding out, rising prices if the economy is near capacity, time lags, and rising leakages (e.g. higher saving in uncertain times) reduce the effect on real output.')],
  contrast=[('the marginal propensity to consume', 'the average propensity to consume', 'The MPC is the share of an additional dollar of income consumed; the APC is total consumption divided by total income.')],
  misc=[('If the multiplier is 4, a $10 bn tax cut raises GDP by $40 bn, exactly the same as a $10 bn rise in government spending.', 'Part of a tax cut is saved or spent on imports in the first round, so its initial injection is smaller than $10 bn; the effect of the tax cut is smaller than that of an equal rise in G.'),
        ('A high marginal propensity to save makes the multiplier larger because savings fund investment.', 'Saving is a leakage from the circular flow; a higher MPS reduces the multiplier (k = 1/MPW).')],
  cases=[('the US American Recovery and Reinvestment Act of 2009', 'The $787 bn package of spending and tax cuts aimed to offset the fall in AD after the financial crisis; the Congressional Budget Office estimated multipliers between about 0.4 and 2.5 for different components.', 'the multiplier', 'spending on infrastructure and transfers to low-income households (high MPC) had larger estimated multipliers than tax cuts for high earners'),
         ('the IMF\'s 2013 reassessment of fiscal multipliers', 'In 2013 IMF economists found that during the euro-area crisis fiscal multipliers had been well above the 0.5 previously assumed, closer to 0.9-1.7.', 'the size of the multiplier', 'with interest rates near zero and spare capacity, spending cuts reduced output far more than expected')],
  evaluate=[('A large multiplier means that fiscal policy is always an effective way to close a deflationary gap.', ['large k means a small injection has a big effect', 'effective when there is spare capacity', 'effective when monetary policy is at the zero lower bound'],
             ['multiplier is uncertain and hard to estimate', 'time lags in implementation', 'crowding out and debt concerns', 'open economies leak spending through imports'], 'A large multiplier strengthens the case for fiscal policy in a deep recession, but uncertainty, lags and debt constraints limit its reliability.')],
  extended=[('In an economy, MPS = 0.15, MPT = 0.25 and MPM = 0.1. A government cuts spending by $12 bn as part of austerity. Calculate the change in real GDP and explain one consequence for the budget deficit.', 'k = 1/0.5 = 2; ΔY = −$24 bn. Lower income reduces tax revenue (0.25 × 24 = $6 bn) and raises benefit payments, so the deficit falls by less than the $12 bn cut.', 6, 'multi_step')],
  )


# =============================================================================================
# ch03 Economic growth
# =============================================================================================
S('ch03-st1',
  diag=[('how an increase in the quantity and quality of factors of production leads to long-term economic growth', 'PPC shifting outward and LRAS (vertical) shifting right from Yp1 to Yp2; explain investment in physical capital, human capital (education, health), technology and institutions.'),
        ('how an increase in aggregate demand can cause short-term economic growth', 'AD shifts right along SRAS (or the Keynesian AS) from Y1 to Y2; movement from inside the PPC towards it; growth through using spare capacity.')],
  terms=[('economic growth', 'an increase in real GDP (or real GDP per capita) over time'),
         ('human capital', 'the skills, knowledge, experience and health of the workforce that raise its productivity'),
         ('labour productivity', 'output per worker or per hour worked'),
         ('physical capital', 'manufactured resources such as machinery, equipment, buildings and infrastructure used to produce goods and services'),
         ('natural capital', 'the stock of natural resources such as land, forests, fisheries, water and minerals')],
  facts=[('Which of the following is most likely to increase potential output?', 'Investment in transport infrastructure and broadband', ['A temporary cut in VAT', 'A rise in consumer confidence', 'A fall in the exchange rate'], 'Infrastructure raises productive capacity, shifting LRAS right.'),
         ('Short-term economic growth caused by an increase in AD is shown on a PPC diagram as:', 'a movement from a point inside the PPC towards the curve', ['an outward shift of the PPC', 'an inward shift of the PPC', 'a movement along the PPC'], 'Spare resources are brought into use.'),
         ('Which of the following is a source of growth through improved quality of labour?', 'Better health care reducing working days lost to illness', ['A rise in the retirement age', 'Immigration of workers', 'Lower interest rates'], 'Health raises productivity; immigration raises quantity.')],
  why=[('Explain why investment in education can lead to long-term economic growth.', 'Education raises human capital and labour productivity, increasing the quality of a factor of production; more output can be produced from the same labour force, shifting LRAS and the PPC outwards.'),
       ('Explain why growth based only on increases in AD cannot be sustained indefinitely.', 'Once the economy reaches potential output, further AD increases mainly raise the price level; sustained growth requires increases in productive capacity.'),
       ('Explain why technological progress is considered the most important source of long-run growth.', 'Capital accumulation faces diminishing returns, but new technology raises the productivity of all factors, allowing output per worker to keep rising.')],
  contrast=[('actual economic growth', 'potential economic growth', 'Actual growth is an increase in real GDP produced, possibly from using spare capacity; potential growth is an increase in the capacity to produce, from more or better factors of production.')],
  misc=[('Any increase in investment immediately increases potential output.', 'Investment adds to AD immediately, but it raises potential output only when the new capital becomes productive, and only net of depreciation.'),
        ('Countries rich in natural resources always grow faster.', 'The "resource curse" shows resource-rich countries can grow slowly because of corruption, volatile prices and Dutch disease; human capital and institutions matter more.')],
  cases=[('South Korea\'s growth since the 1960s', 'South Korea\'s GDP per capita rose from under $200 in 1960 to over $33,000 by 2023, with heavy investment in education, export industries and R&D.', 'sources of long-term growth', 'improvements in human capital and technology raised productivity, shifting LRAS outward over decades'),
         ('Ethiopia\'s public investment-led growth', 'Ethiopia averaged close to 10% annual growth between 2004 and 2019, driven by public investment in roads, dams and industrial parks.', 'growth through increases in physical capital', 'infrastructure raised capacity, but reliance on borrowing increased debt risks'),
         ('Ireland\'s growth in the 1990s (the "Celtic Tiger")', 'Irish real GDP grew at around 6-9% a year in the late 1990s, attracting FDI with a low corporation tax rate, an educated English-speaking workforce and EU single-market access.', 'the role of FDI and human capital in growth', 'foreign firms brought capital and technology while a skilled workforce raised productivity')],
  evaluate=[('Investment in human capital is the most effective way to achieve long-term economic growth.', ['raises productivity of labour', 'complements technology adoption', 'reduces inequality and improves health'],
             ['long time lags', 'brain drain may export the gains', 'physical capital and institutions are also required', 'graduate unemployment if demand for skills is lacking'], 'Human capital is necessary for sustained growth, but it is most effective combined with infrastructure, good institutions and open markets.')],
  )

S('ch03-st2',
  diag=[('how economic growth may lead to negative environmental consequences, using a diagram of negative externalities of production', 'MSC above MPC; market output Qm exceeds socially optimal Q*; welfare loss; explain pollution and resource depletion that accompany growth.')],
  terms=[('living standards', 'the level of material well-being of a population, often measured by real GDP per capita, along with health, education and access to goods and services'),
         ('trickle-down effect', 'the theory that the benefits of growth for high earners eventually spread to lower-income groups through higher spending and employment'),
         ('environmental sustainability', 'meeting present needs without compromising the ability of future generations to meet their needs, through maintaining natural capital'),
         ('Kuznets curve', 'the hypothesis that income inequality first rises and then falls as an economy develops')],
  facts=[('Which of the following is a possible negative consequence of rapid economic growth?', 'Demand-pull inflation if AD grows faster than potential output', ['Lower tax revenues', 'Higher cyclical unemployment', 'Lower average incomes'], 'Rapid AD growth can create inflationary gaps.'),
         ('Which of the following explains why growth usually reduces unemployment?', 'Labour is a derived demand, so higher output requires more workers', ['Growth reduces the labour force', 'Growth always raises wages faster than prices', 'Growth eliminates structural unemployment'], 'More production needs more labour (cyclical unemployment falls).'),
         ('Why might economic growth worsen income inequality?', 'Gains may accrue mainly to owners of capital and highly skilled workers', ['Growth always raises the incomes of the poor most', 'Growth reduces profits', 'Growth abolishes poverty traps'], 'Skill-biased technical change and returns to capital can widen gaps.')],
  why=[('Explain why economic growth can improve government finances.', 'Higher incomes and spending raise tax revenues while lower unemployment reduces benefit payments, allowing more spending on public services or lower deficits.'),
       ('Explain why economic growth may not improve living standards for everyone.', 'Growth is an average; if gains are concentrated among high-income groups or regions, many households may see stagnant real incomes, and environmental damage may reduce quality of life.'),
       ('Explain why economic growth may have negative effects on the current account of the balance of payments.', 'Rising incomes increase spending on imports (MPM), so imports may grow faster than exports, worsening the current account balance.')],
  contrast=[('economic growth', 'economic development', 'Growth is an increase in real output; development is a broader improvement in living standards, including health, education, freedom and reduced poverty.')],
  misc=[('Economic growth always reduces poverty.', 'Growth can reduce absolute poverty, but if its benefits are unevenly distributed, relative poverty and inequality may rise.'),
        ('Economic growth must always harm the environment.', 'Growth based on services, renewable energy and efficiency can decouple output from emissions; several high-income countries have cut emissions while growing.')],
  cases=[('China\'s poverty reduction since 1980', 'The World Bank estimates that close to 800 million people in China moved out of extreme poverty between 1980 and 2020.', 'consequences of economic growth for living standards', 'sustained rapid growth raised incomes and created jobs in manufacturing and services, sharply reducing absolute poverty'),
         ('air pollution in Delhi', 'Delhi regularly records some of the world\'s highest levels of PM2.5 air pollution during winter, associated with vehicles, industry, construction and crop burning.', 'environmental consequences of growth', 'rapid urban and industrial growth generated negative externalities that reduce health and well-being'),
         ('income inequality in the USA since 1980', 'The share of US pre-tax national income going to the top 1% roughly doubled from about 10% in 1980 to around 20% in recent years.', 'the distributional consequences of growth', 'the gains from growth were concentrated at the top, so median incomes grew much more slowly than average incomes')],
  evaluate=[('The benefits of economic growth outweigh its costs.', ['higher incomes and lower absolute poverty', 'more tax revenue for public services', 'lower unemployment'],
             ['environmental degradation and climate change', 'rising inequality', 'inflation and current-account pressures', 'non-renewable resource depletion'], 'Benefits usually outweigh costs for low-income countries, but for all countries the quality (inclusive and sustainable) of growth matters as much as its rate.')],
  )

GROWTH_FRAMES = [
    'Real GDP in {e} was ${a} bn in {y1} and ${b} bn in {y2}.',
    'According to the national statistics office, {e}\'s output at constant prices rose from ${a} bn ({y1}) to ${b} bn ({y2}).',
    'World Bank data show that {e}\'s real GDP was ${a} bn in {y1}; by {y2} it had reached ${b} bn.',
]


@calc('ch03-st3', 'C3', (1, 5))
def growth_rate(rng, slot):
    e = ec(rng)
    a = rng.randint(80, 900)
    if slot.d <= 2:
        g = rng.choice([-3, -2, 1.5, 2, 2.5, 3, 4, 5, 6.5, 7])
        b = round(a * (1 + g / 100), 1)
        y1 = rng.randint(2014, 2023)
        gr = pct(b, a)
        stem = rng.choice(GROWTH_FRAMES).format(e=e, a=a, b=b, y1=y1, y2=y1 + 1) + ' Calculate the rate of economic growth.'
        return dict(stem=stem, answer=f'{gr:.1f}%', markingKey=MK(f'({b} − {a})/{a} × 100 = {gr:.1f}%.', f'{gr:.1f}%'), marks=2)
    if slot.d == 3:
        n = rng.choice([3, 4, 5, 10])
        g = rng.choice([2, 3, 4, 5, 6])
        b = round(a * (1 + g / 100) ** n, 1)
        y1 = rng.randint(2005, 2012)
        cagr = ((b / a) ** (1 / n) - 1) * 100
        stem = rng.choice(GROWTH_FRAMES).format(e=e, a=a, b=b, y1=y1, y2=y1 + n) + f' Calculate (i) the total percentage increase in real GDP and (ii) the average annual growth rate over the {n} years.'
        tot = pct(b, a)
        return dict(stem=stem, answer=f'(i) {tot:.1f}%; (ii) ≈ {cagr:.1f}% a year (compound)',
                    markingKey=MK(f'(i) ({b} − {a})/{a} × 100 = {tot:.1f}%; (ii) ({b}/{a})^(1/{n}) − 1 = {cagr:.1f}%. Accept simple average {tot / n:.1f}% with [M1] only.', f'{cagr:.1f}%'), marks=3)
    if slot.d == 4:
        g = rng.choice([2, 3.5, 5, 7, 10])
        yrs = 70 / g
        pop = rng.choice([p for p in [0.5, 1, 1.5, 2, 2.5, 3] if p < g - 0.4])
        pcg = g - pop
        frame = rng.choice([f'{e}\'s real GDP is growing at {g}% a year and its population at {pop}% a year.',
                            f'A development report on {e} forecasts annual real GDP growth of {g}% and population growth of {pop}%.'])
        return dict(stem=frame + ' Using the rule of 70, estimate how long it takes real GDP to double, and approximately how long it takes real GDP per capita to double.',
                    answer=f'Real GDP doubles in ≈ 70/{g} = {yrs:.1f} years; per capita growth ≈ {g} − {pop} = {pcg:.1f}%, so real GDP per capita doubles in ≈ {70 / pcg:.1f} years.',
                    markingKey=MK(f'70/{g} = {yrs:.1f}; per capita growth ≈ {pcg:.1f}%; 70/{pcg:.1f} = {70 / pcg:.1f}.', 'both doubling times'), marks=4)
    ng = rng.choice([6, 8, 10, 12, 15])
    inf = rng.choice([2, 3, 4, 5, 7, 9])
    pop = rng.choice([0.5, 1, 1.5, 2])
    rg = ((1 + ng / 100) / (1 + inf / 100) - 1) * 100
    rpc = ((1 + rg / 100) / (1 + pop / 100) - 1) * 100
    frame = rng.choice([f'In {e}, nominal GDP grew by {ng}% last year, the GDP deflator rose by {inf}% and the population grew by {pop}%.',
                        f'An IMF Article IV report states that {e}\'s nominal GDP increased by {ng}%, prices (GDP deflator) by {inf}% and population by {pop}%.'])
    return dict(stem=frame + ' Calculate the growth of real GDP and of real GDP per capita, and explain what this suggests about changes in living standards.',
                answer=f'Real GDP growth ≈ {rg:.1f}%; real GDP per capita growth ≈ {rpc:.1f}%. {"Average real income per person rose" if rpc > 0 else "Average real income per person fell"}, but distribution, informal output and non-income factors must also be considered.',
                markingKey=MK(f'(1.{ng:02d}/1.{inf:02d} − 1) × 100 = {rg:.1f}% (accept approximation {ng - inf}%); (1 + {rg:.1f}%)/(1 + {pop}%) − 1 = {rpc:.1f}%.', f'{rg:.1f}% and {rpc:.1f}%') + ' [R1] interpretation.', marks=6)


@calc('ch03-st3', 'C1', (1, 3), 'mcq')
def growth_mcq(rng, slot):
    a = rng.choice([200, 250, 400, 500, 800])
    g = rng.choice([2, 4, 5, 8])
    b = a * (1 + g / 100)
    return nmcq(rng, f'Real GDP rises from ${a} bn to ${r2(b)} bn. What is the growth rate?', g, [g / 10, b - a, g * 2, 100 + g],
                f'({r2(b)} − {a})/{a} × 100 = {g}%.', f=lambda v: f'{r2(v)}%')


S('ch03-st3',
  terms=[('rate of economic growth', 'the percentage change in real GDP over a period, usually a year'),
         ('rule of 70', 'an approximation that the number of years for a variable to double equals 70 divided by its annual percentage growth rate'),
         ('index number', 'a number that expresses the value of a variable relative to a base period set equal to 100'),
         ('compound growth', 'growth in which each period\'s percentage increase is applied to the previous period\'s (larger) value')],
  facts=[('If real GDP growth falls from 5% to 2%, which of the following is true?', 'Real GDP is still rising, but more slowly', ['Real GDP has fallen', 'The economy is in recession', 'Prices are falling'], 'A positive growth rate means output is still increasing.'),
         ('Using the rule of 70, how long does it take for an economy growing at 7% a year to double its real GDP?', 'About 10 years', ['About 7 years', 'About 70 years', 'About 14 years'], '70/7 = 10.'),
         ('Real GDP per capita growth is approximately equal to:', 'real GDP growth minus population growth', ['nominal GDP growth minus inflation', 'real GDP growth plus population growth', 'nominal GDP growth divided by population'], 'Per capita growth ≈ g(Y) − g(N).')],
  why=[('Explain why a fall in the rate of economic growth does not necessarily mean that real GDP is falling.', 'The growth rate measures the speed of change; as long as it is positive, real GDP is still rising, only more slowly.'),
       ('Explain why small differences in growth rates have large effects on living standards over long periods.', 'Growth compounds: at 1% a year real GDP doubles in about 70 years, at 3.5% in about 20 years, so over a generation the higher-growth economy becomes several times richer.'),
       ('Explain why growth data for developing countries should be interpreted with caution.', 'Large informal sectors, out-of-date base years, changes in methodology and political pressures can make official real GDP figures inaccurate.')],
  contrast=[('a fall in the level of real GDP', 'a fall in the rate of growth of real GDP', 'A fall in the level means output is lower than before (negative growth); a fall in the rate means output is still growing but more slowly.')],
  misc=[('Real GDP grew by 3% in 2022 and 3% in 2023, so it grew by exactly 6% over the two years.', 'Growth compounds: 1.03 × 1.03 = 1.0609, so the total increase is 6.09%.'),
        ('An index of real GDP rising from 120 to 132 means a 12% increase.', 'The change is 12 index points, but the percentage change is 12/120 × 100 = 10%.')],
  cases=[('India\'s growth in 2021-2024', 'India\'s real GDP grew by over 9% in 2021-22 after a 5.8% contraction in 2020-21, then by around 7-8% a year.', 'interpreting growth data', 'part of the very high 2021-22 rate was a rebound from a low base (base effect), so growth rates must be read alongside levels'),
         ('Argentina\'s volatile growth', 'Argentina\'s real GDP growth swung between large contractions (e.g. about −10% in 2020) and rebounds of over 10% in 2021.', 'growth rates and the business cycle', 'volatile growth with frequent recessions meant the level of real GDP per capita in the early 2020s was similar to that of a decade earlier')],
  sources=[('Nigeria\'s real GDP grew by an average of about 2% a year between 2015 and 2023, while its population grew by around 2.5% a year. Over the same period, inflation averaged more than 13% a year.', 'Adapted from World Bank data',
            'Using the data, explain what happened to Nigeria\'s real GDP per capita, and why nominal GDP figures would be misleading.', 'Real GDP per capita fell (≈ 2% − 2.5% = −0.5% a year), so average real incomes declined; nominal GDP rose rapidly because of high inflation, which would wrongly suggest strong growth.')],
  evaluate=[('A high rate of economic growth is the best indicator of a successful economy.', ['higher incomes and employment', 'more resources for public services', 'easy to measure and compare'],
             ['may be a rebound from a low base', 'may come with inflation, inequality or environmental damage', 'per capita growth matters more than total', 'stability and sustainability matter too'], 'Growth is important, but success should be judged by sustainable, inclusive growth in real GDP per capita together with other indicators.')],
  )


# =============================================================================================
# ch04 Low unemployment
# =============================================================================================
@calc('ch04-st1', 'C3', (1, 5))
def unemp_rate(rng, slot):
    e = ec(rng)
    emp = rng.randint(2_000, 40_000)
    ur = rng.choice([3, 4.5, 5, 6, 7.5, 8, 10, 12, 15])
    U = round(emp * ur / (100 - ur))
    lf = emp + U
    r = 100 * U / lf
    unit = 'thousand'
    frame = rng.choice([f'In {e}, {emp:,} {unit} people are employed and {U:,} {unit} are unemployed (actively seeking work).',
                        f'A labour force survey in {e} finds {U:,} {unit} people without a job but looking for one, and {emp:,} {unit} people in paid work.',
                        f'Data from {e}\'s labour ministry: employed {emp:,} {unit}; unemployed and available for work {U:,} {unit}.'])
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the unemployment rate.', answer=f'{r:.1f}%',
                    markingKey=MK(f'Labour force = {emp:,} + {U:,} = {lf:,}; rate = {U:,}/{lf:,} × 100 = {r:.1f}%.', f'{r:.1f}%'), marks=2)
    wap = round(lf / rng.choice([0.55, 0.6, 0.65, 0.7]))
    part = 100 * lf / wap
    if slot.d == 3:
        return dict(stem=frame + f' The working-age population is {wap:,} {unit}. Calculate (i) the unemployment rate and (ii) the labour force participation rate.',
                    answer=f'(i) {r:.1f}%; (ii) {part:.1f}%',
                    markingKey=MK(f'LF = {lf:,}; (i) {U:,}/{lf:,} = {r:.1f}%; (ii) {lf:,}/{wap:,} = {part:.1f}%.', 'both rates'), marks=3)
    disc = rng.choice([200, 300, 500, 800])
    disc = min(disc, emp // 4)
    r2_ = 100 * (U + disc) / (lf + disc)
    return dict(stem=frame + f' A further {disc:,} {unit} people want a job but have stopped searching (discouraged workers). Calculate the official unemployment rate and an adjusted rate that includes discouraged workers, and explain why the official rate may understate the true extent of unemployment.',
                answer=f'Official: {r:.1f}%; adjusted: {r2_:.1f}%. Discouraged workers, underemployed part-time workers and people in informal or hidden unemployment are not counted.',
                markingKey=MK(f'Official {U:,}/{lf:,} = {r:.1f}%; adjusted ({U:,}+{disc:,})/({lf:,}+{disc:,}) = {r2_:.1f}%.', 'both rates') + ' [R1][R1] hidden unemployment explained (discouraged workers; underemployment).', marks=4 if slot.d == 4 else 6)


S('ch04-st1',
  terms=[('unemployment', 'the situation of people of working age who are willing and able to work and actively seeking work but do not have a job'),
         ('unemployment rate', 'the number of unemployed people as a percentage of the labour force'),
         ('labour force', 'the number of people of working age who are employed or unemployed and seeking work'),
         ('hidden unemployment', 'unemployment not captured by official statistics, such as discouraged workers who have stopped looking and underemployed workers'),
         ('underemployment', 'the situation of people who work part-time but want full-time work, or who work in jobs below their skill level')],
  facts=[('Which of the following people is counted as unemployed in a labour force survey?', 'A graduate actively applying for jobs who has not found one', ['A retired teacher', 'A full-time student not seeking work', 'A worker on paid sick leave'], 'Must be without work, available and actively seeking work.'),
         ('Which of the following would cause the official unemployment rate to understate true unemployment?', 'Discouraged workers stop looking for work', ['Students take part-time jobs', 'Workers move between jobs', 'More people enter the labour force and find jobs'], 'Discouraged workers leave the labour force.'),
         ('The ILO measure of unemployment is based on:', 'a labour force survey of households', ['claims for unemployment benefit only', 'company payroll data', 'tax returns'], 'Surveys capture people not eligible for benefits.')],
  why=[('Explain why the unemployment rate can fall even when the number of people in work does not increase.', 'If unemployed people stop searching (discouraged workers) or leave the labour force, the number counted as unemployed falls, lowering the rate without any job creation.'),
       ('Explain why unemployment statistics may be inaccurate in economies with a large informal sector.', 'Many people work informally in unrecorded jobs or are underemployed in subsistence activities, so surveys and official records poorly capture who is working or seeking work.'),
       ('Explain why an average national unemployment rate may hide important differences.', 'Unemployment varies by region, age, gender, ethnicity and skill; for example youth unemployment is often double the national rate.')],
  contrast=[('the unemployment rate', 'the labour force participation rate', 'The unemployment rate is the unemployed as a share of the labour force; the participation rate is the labour force as a share of the working-age population.')],
  misc=[('Someone who is not working is unemployed.', 'Only those who are available and actively seeking work are unemployed; retirees, full-time students and carers not seeking work are economically inactive.'),
        ('A falling unemployment rate always means the labour market is getting healthier.', 'It may fall because discouraged workers leave the labour force, or because of rising underemployment in part-time jobs.')],
  cases=[('South Africa\'s unemployment', 'South Africa\'s official unemployment rate has exceeded 30% in recent years; the expanded definition including discouraged workers is around 40%.', 'hidden unemployment', 'many people want work but have stopped searching, so the official measure understates labour market slack'),
         ('Spain\'s youth unemployment', 'Spain\'s youth (under-25) unemployment rate peaked at over 55% in 2013 when the overall rate was about 26%.', 'differences hidden by the national unemployment rate', 'young people with less experience and on temporary contracts were hit hardest, so the average understated their situation'),
         ('India\'s informal labour market', 'Around 80-90% of India\'s workforce is estimated to work in the informal economy.', 'difficulties in measuring unemployment', 'informal and self-employed work is difficult to record, so open unemployment rates appear low while underemployment is widespread')],
  evaluate=[('The official unemployment rate is an accurate measure of spare capacity in the labour market.', ['based on internationally comparable ILO definition', 'regular and timely surveys', 'tracks cyclical changes well'],
             ['excludes discouraged and underemployed workers', 'ignores informal work', 'averages hide regional and youth differences', 'sample survey errors'], 'It is a useful headline indicator but should be read together with underemployment, participation and broader measures.')],
  )

S('ch04-st2',
  diag=[('demand-deficient (cyclical) unemployment using an AD/AS diagram', 'AD falls from AD1 to AD2; real GDP falls from Yp to Y2, creating a deflationary gap; firms reduce employment as labour is a derived demand.'),
        ('structural unemployment using a labour market diagram', 'In a declining industry, the demand for labour shifts left; with wage rigidity, the quantity of labour supplied exceeds demand; or a minimum wage set above equilibrium creates unemployment.'),
        ('real-wage (classical) unemployment using a labour market diagram', 'Aggregate labour demand and supply against the real wage; a real wage W1 above equilibrium W* creates excess supply of labour (unemployment) equal to Qs − Qd.')],
  terms=[('structural unemployment', 'unemployment caused by a mismatch between workers\' skills or locations and the jobs available, often due to changes in the structure of the economy, technology or labour market rigidities'),
         ('frictional unemployment', 'short-term unemployment of people moving between jobs or entering the labour market and searching for work'),
         ('seasonal unemployment', 'unemployment that occurs because demand for labour varies with the seasons, for example in tourism, agriculture and construction'),
         ('cyclical (demand-deficient) unemployment', 'unemployment caused by a fall in aggregate demand during the contraction phase of the business cycle'),
         ('occupational immobility', 'the difficulty workers face in moving between occupations because they lack the skills required')],
  facts=[('A coal miner loses her job when the mine closes and lacks the skills for local jobs in software. This is an example of:', 'structural unemployment', ['frictional unemployment', 'seasonal unemployment', 'cyclical unemployment'], 'A permanent change in the structure of demand and a skills mismatch.'),
         ('Which policy is most appropriate to reduce cyclical unemployment?', 'Expansionary fiscal or monetary policy to raise AD', ['Retraining schemes', 'Better job-matching websites', 'Relocation grants'], 'Cyclical unemployment is caused by insufficient AD.'),
         ('A ski instructor in the Alps without work in summer is experiencing:', 'seasonal unemployment', ['structural unemployment', 'cyclical unemployment', 'disguised unemployment'], 'Demand varies with the season.'),
         ('Which of the following is likely to reduce frictional unemployment?', 'Improved information about job vacancies through online job platforms', ['Higher interest rates', 'A rise in the minimum wage', 'A fall in AD'], 'Better information reduces search time.')],
  why=[('Explain why technological change can cause structural unemployment.', 'Automation reduces demand for some skills (e.g. routine manufacturing, checkout operators) while increasing demand for others; workers who lack the new skills or live in the wrong place cannot fill new vacancies.'),
       ('Explain why a fall in aggregate demand causes cyclical unemployment.', 'Lower spending reduces firms\' sales; since labour demand is derived from demand for output, firms cut production and lay off workers.'),
       ('Explain why frictional unemployment can never be eliminated completely.', 'There will always be people changing jobs, entering the labour force or relocating, and it takes time to search and match with suitable vacancies.'),
       ('Explain why minimum wage legislation may increase structural unemployment.', 'If the minimum wage is set above the equilibrium wage for low-skilled labour, quantity supplied exceeds quantity demanded, so some workers cannot find jobs.')],
  contrast=[('structural unemployment', 'cyclical unemployment', 'Structural unemployment results from long-term changes in the economy and mismatches, and persists in booms; cyclical unemployment results from a fall in AD and falls as the economy recovers.'),
            ('frictional unemployment', 'structural unemployment', 'Frictional unemployment is short-term job search by people with employable skills; structural unemployment is longer-term, due to skills or location mismatch with available jobs.')],
  misc=[('Structural unemployment can be solved by cutting interest rates.', 'Lower rates raise AD and reduce cyclical unemployment, but structural unemployment requires supply-side measures such as retraining and improving labour mobility.'),
        ('Frictional unemployment is always harmful to the economy.', 'Some search time improves job matching, raising productivity; the aim is to reduce excessive search time, not eliminate it.')],
  cases=[('the closure of UK coal mines in the 1980s and 1990s', 'Employment in UK coal mining fell from about 230,000 in 1980 to under 10,000 by the 2000s, concentrated in regions such as South Wales and Yorkshire.', 'structural unemployment', 'the decline of an industry combined with occupational and geographical immobility left many former miners unemployed for long periods'),
         ('job losses in the USA in 2009', 'US unemployment rose from 5% in early 2008 to 10% in October 2009 as AD collapsed after the financial crisis.', 'cyclical unemployment', 'falling consumer and investment spending reduced the derived demand for labour across most sectors'),
         ('tourism employment in Thailand', 'Thailand\'s tourism employment fluctuates between high and low seasons, and collapsed in 2020 when international arrivals fell by over 80%.', 'seasonal and demand-deficient unemployment', 'normal seasonal swings were overtaken by a large fall in demand, adding cyclical unemployment')],
  evaluate=[('Supply-side policies are the most effective way to reduce unemployment.', ['tackle structural and frictional unemployment', 'raise potential output without inflation', 'long-lasting effects'],
             ['ineffective against cyclical unemployment', 'long time lags', 'costly to the government', 'market-based reforms may increase inequality'], 'The best policy depends on the type of unemployment: demand management for cyclical, supply-side for structural and frictional unemployment.')],
  )

S('ch04-st3',
  terms=[('natural rate of unemployment (NRU)', 'the rate of unemployment that exists when the labour market is in equilibrium at potential output; the sum of frictional, structural and seasonal unemployment'),
         ('hysteresis', 'the effect by which long periods of cyclical unemployment raise the natural rate, as unemployed workers lose skills and motivation'),
         ('opportunity cost of unemployment', 'the output that could have been produced by unemployed workers, shown as a point inside the PPC'),
         ('long-term unemployment', 'unemployment lasting for 12 months or more')],
  facts=[('Which of the following is an economic cost of unemployment to the government?', 'Lower income tax revenue and higher spending on benefits', ['Higher corporate profits', 'Lower interest payments', 'Higher import spending'], 'The fiscal cost of unemployment.'),
         ('The natural rate of unemployment includes:', 'frictional, structural and seasonal unemployment', ['only cyclical unemployment', 'cyclical and structural unemployment', 'only frictional unemployment'], 'At potential output cyclical unemployment is zero.'),
         ('Which of the following is a personal cost of long-term unemployment?', 'Loss of skills and higher rates of depression', ['Higher pension contributions', 'Lower inflation', 'Faster productivity growth'], 'Social and psychological costs.')],
  why=[('Explain why unemployment represents a loss of potential output for the economy.', 'Unemployed workers are idle resources; the economy produces inside its PPC, so goods and services that could have been produced are permanently lost.'),
       ('Explain why long-term unemployment may raise the natural rate of unemployment.', 'Long-term unemployed workers lose skills, contacts and motivation and employers see them as risky, so they become structurally unemployed even when AD recovers (hysteresis).'),
       ('Explain why unemployment can increase income inequality.', 'Unemployment is concentrated among low-skilled and young workers, whose income falls to benefits (if any), widening the gap with those in work.')],
  contrast=[('the natural rate of unemployment', 'cyclical unemployment', 'The natural rate is the unemployment that exists when output is at potential (frictional and structural); cyclical unemployment is the extra unemployment caused by a deflationary gap.')],
  misc=[('At the natural rate of unemployment nobody is unemployed.', 'There is still frictional, structural and seasonal unemployment; only cyclical unemployment is absent.'),
        ('Unemployment only affects the people who lose their jobs.', 'It also affects families, communities (crime, poorer health), firms (lower demand) and the government (lower tax revenue, higher spending).')],
  cases=[('youth unemployment in southern Europe after 2010', 'Many young Spaniards, Italians and Greeks faced years of unemployment after the euro crisis, and hundreds of thousands emigrated.', 'consequences of unemployment', 'long spells reduced lifetime earnings and caused a loss of human capital through emigration (brain drain)'),
         ('the fall in US labour force participation after 2008', 'US labour force participation fell from about 66% in 2008 to about 63% by 2015.', 'hysteresis and hidden costs of unemployment', 'some long-term unemployed workers left the labour force entirely, reducing potential output')],
  evaluate=[('The costs of unemployment are mainly economic rather than social.', ['lost output and lower GDP', 'lower tax revenue and higher benefits', 'lost human capital'],
             ['mental and physical health problems', 'crime and social exclusion', 'family breakdown', 'intergenerational effects'], 'The social costs are at least as serious and are often longer lasting; both justify policies to keep unemployment low.')],
  )


# =============================================================================================
# ch05 Low and stable inflation
# =============================================================================================
BASKETS = [
    [('food', 'food and non-alcoholic beverages'), ('housing', 'housing and utilities'), ('transport', 'transport'), ('recreation', 'recreation and culture')],
    [('food', 'food'), ('energy', 'energy'), ('clothing', 'clothing and footwear'), ('services', 'other services')],
    [('rent', 'rent'), ('food', 'food'), ('fuel', 'fuel'), ('health', 'health care')],
]


@calc('ch05-st1', 'C3', (1, 5))
def cpi_calc(rng, slot):
    e = ec(rng)
    if slot.d <= 2:
        p0 = rng.choice([80, 96, 110, 125, 140, 160, 200])
        p1 = round(p0 * (1 + rng.choice([-1, 2, 3, 4, 6, 8, 10, 12]) / 100), 1)
        y = rng.randint(2016, 2024)
        inf = pct(p1, p0)
        frame = rng.choice([f'The consumer price index in {e} was {p0} in {y} and {p1} in {y + 1}.',
                            f'{e}\'s CPI rose from {p0} ({y}) to {p1} ({y + 1}).',
                            f'In {y} the CPI of {e} stood at {p0}; a year later it was {p1}.'])
        return dict(stem=frame + ' Calculate the rate of inflation.', answer=f'{inf:.1f}%',
                    markingKey=MK(f'({p1} − {p0})/{p0} × 100 = {inf:.1f}%.', f'{inf:.1f}%'), marks=2)
    bk = rng.choice(BASKETS)
    ws = rng.choice([[30, 35, 20, 15], [25, 40, 15, 20], [20, 30, 30, 20], [35, 25, 25, 15]])
    idx = [rng.choice([100, 102, 104, 105, 108, 110, 112, 115, 120, 125]) for _ in bk]
    cpi = sum(w * i for w, i in zip(ws, idx)) / 100
    rows = '; '.join(f'{lab}: weight {w}%, price index {i}' for (_, lab), w, i in zip(bk, ws, idx))
    frame = rng.choice([f'A simplified CPI for {e} uses the following categories (base year = 100): {rows}.',
                        f'The statistics office of {e} compiles its CPI from four groups. This year: {rows}.',
                        f'Household budget survey weights and current price indices for {e} are — {rows}.'])
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the weighted price index and the inflation rate since the base year.',
                    answer=f'Weighted CPI = {cpi:.1f}; inflation since base year = {cpi - 100:.1f}%',
                    markingKey=MK('CPI = Σ(weight × index)/Σweights = ' + ' + '.join(f'{w}×{i}' for w, i in zip(ws, idx)) + f' ÷ 100 = {cpi:.1f}.', f'{cpi:.1f}'), marks=3)
    wage0 = rng.choice([1500, 2000, 2400, 3000, 3600])
    wg = rng.choice([2, 3, 4, 5, 6, 8])
    wage1 = round(wage0 * (1 + wg / 100))
    real = wage1 * 100 / cpi
    rw = pct(real, wage0)
    return dict(stem=frame + f' Over the same period the average monthly wage rose from ${wage0:,} to ${wage1:,}. Calculate the weighted price index and the percentage change in the real wage, and explain one limitation of the CPI as a measure of the cost of living.',
                answer=f'CPI = {cpi:.1f}; real wage = {wage1:,} × 100/{cpi:.1f} = ${real:,.0f}, a change of {rw:.1f}%. Limitation: fixed weights ignore substitution, quality changes and new products, and households with different spending patterns face different inflation rates.',
                markingKey=MK(f'CPI {cpi:.1f}; real wage {real:,.0f}; ({real:,.0f} − {wage0:,})/{wage0:,} = {rw:.1f}%.', f'{rw:.1f}%') + ' [R1] one limitation explained.', marks=4 if slot.d == 4 else 6)


@calc('ch05-st1', 'C3', (2, 4))
def price_level_change(rng, slot):
    e = ec(rng)
    i1, i2 = rng.choice([2, 3, 4, 5, 8]), rng.choice([1, 2, 6, 7, 10])
    base = 100
    p1 = base * (1 + i1 / 100)
    p2 = p1 * (1 + i2 / 100)
    tot = p2 - 100
    frame = rng.choice([f'Inflation in {e} was {i1}% in year 1 and {i2}% in year 2.',
                        f'{e}\'s central bank reports annual CPI inflation of {i1}% followed by {i2}%.'])
    return dict(stem=frame + ' Taking the CPI as 100 at the start of year 1, calculate the CPI at the end of year 2 and the total percentage increase in the price level.',
                answer=f'CPI = 100 × {1 + i1 / 100:.2f} × {1 + i2 / 100:.2f} = {p2:.1f}; total increase {tot:.1f}% (not {i1 + i2}%)',
                markingKey=MK(f'100 × (1 + {i1}/100) × (1 + {i2}/100) = {p2:.1f}.', f'{tot:.1f}%'), marks=3)


S('ch05-st1',
  terms=[('inflation', 'a sustained increase in the general (average) price level, measured as the percentage change in a price index'),
         ('consumer price index (CPI)', 'an index measuring the average change in the prices of a fixed basket of goods and services bought by a typical household, weighted by expenditure shares'),
         ('core inflation', 'inflation measured excluding volatile items such as food and energy prices'),
         ('producer price index (PPI)', 'an index of the prices of inputs and outputs of producers, often a leading indicator of consumer price inflation'),
         ('deflation', 'a sustained fall in the general price level (negative inflation)'),
         ('disinflation', 'a fall in the rate of inflation, while prices are still rising')],
  facts=[('How are the weights in a CPI basket determined?', 'By the share of household spending on each category from household expenditure surveys', ['By the number of items in each category', 'By the government\'s policy priorities', 'Equally for all items'], 'Weights reflect expenditure shares.'),
         ('If the CPI rises from 120 to 126, what is the rate of inflation?', '5%', ['6%', '26%', '4.8%'], '(126 − 120)/120 × 100 = 5%.'),
         ('Why do central banks often monitor core inflation?', 'It removes volatile food and energy prices to show the underlying trend', ['It includes asset prices', 'It is always higher than headline inflation', 'It measures only imported goods'], 'Core inflation reflects persistent pressures.'),
         ('Which of the following is a limitation of the CPI?', 'It may not reflect the spending patterns of particular groups, such as pensioners', ['It measures real GDP', 'It ignores all services', 'It is not published regularly'], 'Different households have different baskets.')],
  why=[('Explain why the CPI may overstate the true rise in the cost of living.', 'It uses a fixed basket, so it ignores consumers switching to cheaper substitutes, improvements in quality and the introduction of new products, all of which reduce the effective cost of living.'),
       ('Explain why a weighted price index is used rather than a simple average of price changes.', 'Households spend different shares of income on different goods; a 10% rise in rent matters more than a 10% rise in the price of salt, so weights by expenditure share reflect the impact on the cost of living.'),
       ('Explain why different households experience different rates of inflation.', 'Their spending patterns differ: low-income households spend a larger share on food and energy, so when those prices rise quickly, their personal inflation rate exceeds the CPI average.')],
  contrast=[('deflation', 'disinflation', 'Deflation is a fall in the general price level (negative inflation); disinflation is a fall in the rate of inflation while prices continue to rise.'),
            ('headline inflation', 'core inflation', 'Headline inflation covers the whole CPI basket; core inflation excludes volatile items such as food and energy to show the underlying trend.')],
  misc=[('If inflation falls from 6% to 3%, prices are falling.', 'Prices are still rising, but more slowly (disinflation). Prices fall only with negative inflation (deflation).'),
        ('A 10% rise in the price of petrol means the inflation rate rises by 10%.', 'Petrol has a small weight in the CPI; if its weight is 4%, it adds only about 0.4 percentage points to inflation.')],
  cases=[('UK CPI inflation in 2022', 'UK CPI inflation peaked at 11.1% in October 2022, driven by energy and food prices; lower-income households, who spend more on these items, faced higher personal inflation rates.', 'limitations of the CPI', 'a single average rate hid the much larger rise in the cost of living for low-income households'),
         ('Argentina\'s inflation in 2023', 'Annual inflation in Argentina exceeded 200% by the end of 2023.', 'measuring inflation', 'rapid price changes required frequent price collection and reduced the usefulness of fixed-weight baskets'),
         ('the US Boskin Commission (1996)', 'The Boskin Commission estimated that the US CPI overstated inflation by about 1.1 percentage points a year, mainly through substitution and quality bias.', 'biases in the CPI', 'the fixed basket ignored consumers switching to cheaper goods and quality improvements')],
  evaluate=[('The consumer price index is an accurate measure of changes in the cost of living.', ['based on large, regular price surveys', 'weights updated with expenditure surveys', 'internationally comparable methodology'],
             ['substitution, quality and new-product biases', 'average household may not represent any real household', 'excludes or poorly measures housing costs in some countries', 'informal markets omitted'], 'It is a reasonable measure of average price changes, but it is less accurate for specific groups and during rapid structural change.')],
  extended=[('A basket has three items: food (weight 50, price index 112), energy (weight 20, index 140) and services (weight 30, index 104). Calculate the CPI, then explain how the inflation rate experienced by a low-income household spending 70% on food and energy would differ.', 'CPI = (50×112 + 20×140 + 30×104)/100 = 115.2 (15.2% inflation). A low-income household with heavier weights on food and energy faces higher inflation, since those indices rose fastest.', 6, 'multi_step')],
  )

S('ch05-st2',
  diag=[('demand-pull inflation', 'AD shifts right from AD1 to AD2 along an upward-sloping SRAS (or towards the vertical section of the Keynesian AS); the price level rises from P1 to P2; caused by rising C, I, G or X.'),
        ('cost-push inflation', 'SRAS shifts left from SRAS1 to SRAS2; the price level rises and real GDP falls; caused by rising wages, energy or import prices.')],
  terms=[('demand-pull inflation', 'inflation caused by increases in aggregate demand that are not matched by increases in aggregate supply'),
         ('cost-push inflation', 'inflation caused by increases in costs of production, such as wages, energy or imported raw materials, which shift SRAS to the left'),
         ('wage-price spiral', 'a process in which rising prices lead workers to demand higher wages, which raise firms\' costs and lead to further price rises'),
         ('menu costs', 'the costs to firms of frequently changing prices, such as reprinting price lists and updating systems'),
         ('hyperinflation', 'extremely rapid inflation, often defined as more than 50% a month')],
  facts=[('Which of the following is most likely to cause demand-pull inflation?', 'A large rise in government spending when the economy is near full employment', ['A rise in world oil prices', 'Higher wage costs', 'A drought that reduces harvests'], 'Excess demand at full capacity.'),
         ('Which group is most likely to gain from unexpected inflation?', 'Borrowers with fixed-interest-rate loans', ['Savers with fixed-rate deposits', 'Pensioners on fixed incomes', 'Lenders'], 'The real value of debt falls.'),
         ('Why can deflation be harmful?', 'Consumers delay purchases expecting lower prices, reducing AD', ['It increases the real value of savings', 'It makes exports less competitive', 'It reduces the real value of debt'], 'Delayed spending and rising real debt burdens.'),
         ('Which is a consequence of high inflation for international competitiveness?', 'Exports become less price competitive if inflation is higher than in trading partners', ['Exports become cheaper', 'Imports become more expensive', 'The current account always improves'], 'Relative inflation affects competitiveness.')],
  why=[('Explain why inflation reduces the purchasing power of people on fixed incomes.', 'If nominal incomes do not rise with prices, each unit of income buys fewer goods and services, so real income falls.'),
       ('Explain why inflation creates uncertainty that may reduce investment.', 'When inflation is high and variable, firms cannot predict future costs, prices and real returns, so they postpone long-term investment.'),
       ('Explain why deflation can lead to a deflationary spiral.', 'Falling prices encourage consumers to delay spending and raise the real value of debts; AD falls, firms cut output and wages, which reduces incomes and pushes prices down further.'),
       ('Explain why a depreciation of the currency can cause cost-push inflation.', 'Imported raw materials, components and energy become more expensive in domestic currency, raising costs of production, shifting SRAS left and raising the price level.')],
  contrast=[('demand-pull inflation', 'cost-push inflation', 'Demand-pull inflation comes from AD rising faster than AS (output rises with prices); cost-push inflation comes from higher production costs shifting SRAS left (output falls as prices rise).')],
  misc=[('Inflation always harms everyone equally.', 'Inflation redistributes: borrowers with fixed-rate debt gain, while savers, lenders and people on fixed incomes lose.'),
        ('Deflation is always good because goods become cheaper.', 'Good deflation from productivity gains can be benign, but demand-led deflation reduces spending, raises real debt burdens and can deepen recessions.')],
  cases=[('Zimbabwe\'s hyperinflation', 'Zimbabwe\'s monthly inflation was estimated at about 79.6 billion per cent in November 2008, after rapid money printing to finance government spending; the country abandoned its currency in 2009.', 'consequences of very high inflation', 'money ceased to be a store of value or medium of exchange, savings were wiped out and the economy dollarised'),
         ('Japan\'s deflation', 'Japan experienced falling or flat consumer prices for much of 1998-2012, with weak growth and very low interest rates.', 'consequences of deflation', 'expectations of falling prices reduced spending and investment, and real debt burdens rose'),
         ('energy-driven inflation in the euro area in 2022', 'Euro-area inflation reached 10.6% in October 2022, with energy prices up over 40% year on year.', 'cost-push inflation', 'higher energy costs shifted SRAS left, raising prices while growth slowed')],
  evaluate=[('Deflation is more harmful to an economy than inflation.', ['deflationary spiral reduces AD and output', 'increases real debt burdens', 'monetary policy is constrained at the zero lower bound'],
             ['high inflation erodes savings and creates uncertainty', 'hyperinflation can destroy a currency', 'benign deflation from productivity is not harmful'], 'Persistent demand-led deflation is usually more damaging than moderate inflation, which is why central banks target low positive inflation of about 2%.')],
  )

S('ch05-st3',
  diag=[('the short-run Phillips curve and the effect of an increase in AD', 'Inflation (y-axis) against unemployment (x-axis); downward-sloping SRPC; an increase in AD moves the economy up the curve from A to B: lower unemployment, higher inflation.'),
        ('the long-run Phillips curve and the natural rate of unemployment', 'Vertical LRPC at the NRU; a series of SRPCs for different expected inflation rates; attempts to keep unemployment below the NRU cause accelerating inflation as expectations adjust.')],
  terms=[('short-run Phillips curve (SRPC)', 'a curve showing an inverse relationship between the inflation rate and the unemployment rate in the short run'),
         ('long-run Phillips curve (LRPC)', 'a vertical line at the natural rate of unemployment, showing no long-run trade-off between inflation and unemployment'),
         ('inflationary expectations', 'the rate of inflation that firms, workers and consumers expect in the future, which influences wage and price setting'),
         ('stagflation', 'simultaneously high inflation and high unemployment, shown by an outward shift of the SRPC')],
  facts=[('According to the expectations-augmented Phillips curve, what happens if the government keeps unemployment below the natural rate?', 'Inflation accelerates as expectations adjust upwards', ['Inflation falls', 'The natural rate falls permanently', 'Unemployment falls permanently with stable inflation'], 'LRPC is vertical at the NRU.'),
         ('Which event in the 1970s challenged the original Phillips curve?', 'Stagflation after the oil price shocks', ['The Great Depression', 'The dot-com boom', 'The creation of the euro'], 'High inflation and unemployment together.'),
         ('A negative supply shock causes the short-run Phillips curve to:', 'shift outwards (upwards to the right)', ['shift inwards', 'become vertical', 'remain unchanged'], 'Higher inflation at every unemployment rate.')],
  why=[('Explain why the short-run Phillips curve slopes downwards.', 'When AD rises, firms expand output and hire more workers, reducing unemployment; tighter labour and product markets push up wages and prices, so lower unemployment is associated with higher inflation.'),
       ('Explain why the long-run Phillips curve is vertical at the natural rate of unemployment.', 'Once workers adjust their inflation expectations, real wages return to equilibrium and unemployment returns to the natural rate, at a higher inflation rate; there is no lasting trade-off.'),
       ('Explain why supply-side policies can shift the long-run Phillips curve to the left.', 'They reduce structural and frictional unemployment (e.g. training, better job matching), lowering the natural rate of unemployment.')],
  contrast=[('the short-run Phillips curve', 'the long-run Phillips curve', 'The SRPC shows a trade-off between inflation and unemployment for given expectations; the LRPC is vertical at the NRU, showing no trade-off once expectations adjust.')],
  misc=[('The Phillips curve shows that governments can permanently reduce unemployment by accepting higher inflation.', 'The expectations-augmented model shows that the trade-off is only short-run; in the long run unemployment returns to the natural rate with higher inflation.'),
        ('A movement along the SRPC is caused by a supply shock.', 'Movements along the SRPC are caused by changes in AD; supply shocks and changes in expectations shift the SRPC.')],
  cases=[('stagflation in the USA in the 1970s', 'US inflation exceeded 13% in 1980 while unemployment rose above 7%, contradicting the stable trade-off suggested by the original Phillips curve.', 'shifts of the short-run Phillips curve', 'oil shocks and rising expectations shifted the SRPC outwards, so inflation and unemployment rose together'),
         ('the "flat" Phillips curve of the 2010s', 'In the late 2010s US unemployment fell to around 3.5% while inflation stayed close to 2%.', 'the Phillips curve and anchored expectations', 'credible inflation targeting anchored expectations, so falling unemployment caused only a small rise in inflation')],
  evaluate=[('There is no trade-off between inflation and unemployment.', ['vertical LRPC once expectations adjust', '1970s stagflation', 'credible central banks anchor expectations'],
             ['short-run trade-off clearly exists', 'post-2021 inflation rose as labour markets tightened', 'hysteresis may make the NRU depend on past unemployment'], 'There is a short-run trade-off but no stable long-run trade-off; policy can only lower unemployment permanently by reducing the NRU.')],
  )

S('ch05-st4',
  terms=[('policy conflict', 'a situation where achieving one macroeconomic objective makes achieving another more difficult'),
         ('trade-off', 'a situation where more of one objective can only be achieved by accepting less of another'),
         ('macroeconomic objectives', 'the main goals of macroeconomic policy: economic growth, low unemployment, low and stable inflation, a sustainable balance of payments and an equitable distribution of income'),
         ('sustainable growth', 'growth that can be maintained without creating inflation, unsustainable debt or environmental damage')],
  facts=[('Which of the following is an example of a conflict between macroeconomic objectives?', 'Rapid growth increases imports and worsens the current account', ['Lower unemployment raises tax revenue', 'Low inflation improves competitiveness', 'Higher investment raises potential output'], 'Growth raises import demand.'),
         ('Raising interest rates to reduce inflation is likely to conflict with which objective?', 'Low unemployment', ['Low inflation', 'Price stability', 'A stronger currency'], 'Higher rates reduce AD and employment.'),
         ('Why might economic growth conflict with environmental sustainability?', 'More production can increase pollution and resource depletion', ['Growth always reduces emissions', 'Growth reduces consumption', 'Growth lowers energy use'], 'Negative externalities increase with output.')],
  why=[('Explain why there may be a conflict between low unemployment and low inflation.', 'Policies that raise AD to reduce unemployment move the economy up the SRPC: as spare capacity falls, wages and prices rise, increasing inflation.'),
       ('Explain why economic growth may conflict with an equitable distribution of income.', 'Growth may favour owners of capital and highly skilled workers; market-based supply-side policies that boost growth, such as lower top tax rates, can widen inequality.'),
       ('Explain why economic growth may worsen the current account balance.', 'Higher incomes raise spending on imports, and if domestic demand grows faster than exports, the current account deficit widens.')],
  contrast=[('a short-run policy conflict', 'a long-run policy conflict', 'Short-run conflicts arise mainly from demand management (e.g. the SRPC trade-off); in the long run supply-side improvements can achieve growth with low inflation, but conflicts with sustainability and equity may persist.')],
  misc=[('Macroeconomic objectives always conflict, so governments must choose only one.', 'Some objectives are complementary: supply-side growth can reduce unemployment and inflation together; conflicts are mainly short-run trade-offs.')],
  cases=[('the US Federal Reserve\'s rate rises in 2022-2023', 'The Fed raised its policy rate from near zero in March 2022 to 5.25-5.50% by July 2023 to bring down inflation from 9.1%.', 'conflict between low inflation and growth', 'higher rates reduced inflation but risked slowing growth and raising unemployment, although the labour market stayed strong'),
         ('China\'s growth and emissions', 'China became the world\'s largest emitter of CO₂, accounting for around 30% of global emissions, during decades of rapid industrial growth.', 'conflict between growth and environmental sustainability', 'energy-intensive, coal-powered growth raised output and incomes but caused large negative environmental externalities')],
  evaluate=[('Low inflation should be the main priority of macroeconomic policy.', ['provides stability for investment', 'protects real incomes of the poor', 'credible inflation targets anchor expectations'],
             ['may sacrifice growth and employment in the short run', 'unemployment has large human costs', 'sustainability and equity also matter'], 'Low inflation is a necessary foundation, but rigid prioritisation can cause avoidable unemployment; a flexible approach that balances objectives is preferable.')],
  )


# =============================================================================================
# ch06 Inequality and poverty
# =============================================================================================
@calc('ch06-st1', 'C3', (2, 5))
def gini_quintiles(rng, slot):
    e = ec(rng)
    for _ in range(100):
        q = sorted(rng.sample(range(3, 60), 4))
        q.append(100 - sum(q))
        q = sorted(q)
        if 2 <= q[0] and q[-1] <= 65 and len(set(q)) == 5:
            break
    else:
        return None
    cum = [0]
    for s in q:
        cum.append(cum[-1] + s)
    B = sum(0.2 * (cum[i] + cum[i + 1]) / 2 for i in range(5)) / 100
    G = 1 - 2 * B
    tab = ', '.join(f'Q{i + 1} {s}%' for i, s in enumerate(q))
    frame = rng.choice([f'The shares of total income received by each quintile (poorest 20% first) in {e} are: {tab}.',
                        f'A household income survey in {e} shows the following quintile income shares, from the poorest to the richest fifth — {tab}.',
                        f'In {e}, income is distributed as follows: {tab} (Q1 = poorest 20% of households).'])
    if slot.d <= 3:
        return dict(stem=frame + ' State the cumulative share of income received by the poorest 60% of households, and calculate the ratio of the income share of the richest 20% to that of the poorest 20%.',
                    answer=f'Poorest 60% receive {cum[3]}%; S80/S20 ratio = {q[4]}/{q[0]} = {q[4] / q[0]:.1f}',
                    markingKey=MK(f'{q[0]} + {q[1]} + {q[2]} = {cum[3]}%; {q[4]}/{q[0]} = {q[4] / q[0]:.1f}.', 'both values'), marks=3)
    return dict(stem=frame + ' Using the trapezium rule for the area under the Lorenz curve, calculate the Gini coefficient, and comment on the degree of inequality.',
                answer=f'Cumulative shares 0, {", ".join(str(c) for c in cum[1:])}; area B = {B:.3f}; Gini = 1 − 2B = {G:.2f}. {"Relatively low inequality (similar to Nordic countries)." if G < 0.3 else "Moderate inequality." if G < 0.4 else "High inequality (similar to Brazil or South Africa)."}',
                markingKey=MK(f'B = Σ 0.2 × (L(i−1) + L(i))/2 = {B:.3f}; Gini = A/(A + B) = (0.5 − B)/0.5 = {G:.2f}.', f'Gini ≈ {G:.2f}') + ' [R1] comment comparing with real-world values.', marks=4 if slot.d == 4 else 6)


S('ch06-st1',
  diag=[('a Lorenz curve and how the Gini coefficient is derived from it', 'Cumulative % of population (x) against cumulative % of income (y); 45° line of perfect equality; Lorenz curve below it; Gini = A/(A + B), where A is the area between the line of equality and the Lorenz curve; a curve further from the diagonal means more inequality.')],
  terms=[('Lorenz curve', 'a curve showing the cumulative percentage of income (or wealth) received by cumulative percentages of the population, ranked from poorest to richest'),
         ('Gini coefficient', 'a measure of inequality from 0 (perfect equality) to 1 (perfect inequality), calculated as the area between the line of equality and the Lorenz curve divided by the total area under the line of equality'),
         ('income inequality', 'the unequal distribution of income (a flow) among households or individuals in an economy'),
         ('wealth inequality', 'the unequal distribution of the stock of assets, such as property, shares and savings, net of debts'),
         ('Palma ratio', 'the income share of the richest 10% divided by the share of the poorest 40%')],
  facts=[('A Gini coefficient of 0 indicates:', 'perfect equality, with every household receiving the same income', ['perfect inequality', 'no data available', 'zero poverty'], 'The Lorenz curve coincides with the line of equality.'),
         ('Which of these countries has one of the highest income Gini coefficients in the world?', 'South Africa', ['Slovenia', 'Norway', 'Japan'], 'South Africa\'s Gini is about 0.63 (World Bank).'),
         ('If the Lorenz curve moves further away from the line of equality, which of the following is true?', 'Inequality has increased and the Gini coefficient has risen', ['Inequality has decreased', 'Poverty has disappeared', 'The Gini coefficient has fallen'], 'Area A increases.'),
         ('Why is wealth usually distributed more unequally than income?', 'Wealth accumulates over time and is passed on through inheritance', ['Wealth is taxed more heavily', 'Income includes inheritances', 'Wealth is easier to measure'], 'Returns on wealth compound.')],
  why=[('Explain why the Gini coefficient increases when the Lorenz curve moves away from the line of equality.', 'The Gini is A/(A + B); as the Lorenz curve bows further out, area A between it and the line of equality grows while A + B is fixed, so the ratio rises.'),
       ('Explain why two countries with the same Gini coefficient may have different patterns of inequality.', 'The Gini is a single summary number; Lorenz curves can cross, so one country may have a very poor bottom 20% and the other a very rich top 1%, yet the same area A.'),
       ('Explain why wealth inequality is generally greater than income inequality.', 'Wealth is a stock built up over time; high earners save more, returns on assets compound and assets are inherited, whereas many households have little or negative net wealth.')],
  contrast=[('income', 'wealth', 'Income is a flow of earnings over a period (wages, rent, interest, profit); wealth is a stock of assets owned at a point in time, net of debts.')],
  misc=[('A country with a lower Gini coefficient must have less poverty.', 'The Gini measures relative inequality; a poor country can have a low Gini but many people in absolute poverty.'),
        ('The Gini coefficient of 0.35 means that 35% of people are poor.', 'The Gini is a ratio of areas on the Lorenz diagram, not a percentage of the population; it says nothing directly about the number of poor people.')],
  cases=[('inequality in Brazil', 'Brazil\'s Gini coefficient fell from about 0.59 in 2001 to about 0.52 by 2015, partly due to Bolsa Família and minimum wage rises, and remains among the highest in the world.', 'measurement of income inequality', 'a falling Gini shows the Lorenz curve moving closer to the line of equality as low incomes grew faster'),
         ('Nordic income distribution', 'Denmark, Finland and Norway have income Gini coefficients of around 0.26-0.28 after taxes and transfers.', 'the Gini coefficient as a comparison tool', 'progressive taxes and generous transfers bring the Lorenz curve closer to equality than in most countries'),
         ('global wealth concentration', 'Credit Suisse/UBS Global Wealth Reports estimate the richest 1% of adults own close to 45% of global household wealth.', 'wealth inequality', 'wealth is far more concentrated than income because of compounding returns and inheritance')],
  evaluate=[('The Gini coefficient is the best measure of inequality.', ['single, comparable summary of the whole distribution', 'widely published', 'easy to track over time'],
             ['insensitive to where inequality occurs', 'crossing Lorenz curves can give equal Ginis', 'depends on income vs consumption data', 'ignores wealth and non-income dimensions'], 'It is the most widely used single measure, but it should be supplemented with quintile ratios, the Palma ratio and wealth data.')],
  )


@calc('ch06-st2', 'C3', (1, 4))
def poverty_line(rng, slot):
    e = ec(rng)
    med = rng.choice([12_000, 15_000, 18_000, 24_000, 30_000, 36_000])
    share = rng.choice([50, 60])
    line = med * share / 100
    incomes = sorted(rng.sample(range(int(med * 0.3) // 100, int(med * 1.8) // 100), 10))
    incomes = [i * 100 for i in incomes]
    below = [i for i in incomes if i < line]
    hh = ', '.join(f'${i:,}' for i in incomes)
    frame = rng.choice([f'In {e} the median household disposable income is ${med:,} a year, and the government defines relative poverty as income below {share}% of the median.',
                        f'{e} uses a relative poverty line of {share}% of median income; median disposable income is ${med:,}.'])
    return dict(stem=frame + f' Ten households in a survey have incomes of {hh}. Calculate the poverty line and the percentage of these households in relative poverty.',
                answer=f'Poverty line = {share}% × ${med:,} = ${line:,.0f}; {len(below)} of 10 households ({len(below) * 10}%) are below it.',
                markingKey=MK(f'Line = {share/100} × {med:,} = {line:,.0f}; households below: {", ".join(f"${b:,}" for b in below) or "none"}.', f'{len(below) * 10}%'), marks=3)


S('ch06-st2',
  terms=[('absolute poverty', 'a condition in which household income is below a level needed to meet basic needs such as food, shelter and clothing, measured by an international poverty line'),
         ('relative poverty', 'a condition in which household income is below a given proportion (usually 50% or 60%) of the median income in that country'),
         ('Multidimensional Poverty Index (MPI)', 'a UNDP/OPHI index measuring acute poverty through deprivations in health, education and living standards (10 indicators); a person is poor if deprived in at least one-third of weighted indicators'),
         ('international poverty line', 'the World Bank threshold for extreme poverty, $2.15 a day at 2017 PPP, updated to $3.00 a day at 2021 PPP in 2025'),
         ('poverty trap', 'a self-reinforcing situation in which poor people cannot escape poverty because low income prevents investment in health, education and capital')],
  facts=[('Which of the following is a measure of relative poverty?', 'The percentage of households with income below 60% of the median', ['The number of people living on less than $3.00 a day', 'The Human Development Index', 'GDP per capita'], 'Relative poverty is relative to national incomes.'),
         ('What three dimensions does the Multidimensional Poverty Index cover?', 'Health, education and living standards', ['Income, wealth and consumption', 'Employment, inflation and growth', 'Gender, environment and governance'], 'MPI uses 10 indicators across these dimensions.'),
         ('Why might relative poverty increase even when all incomes are rising?', 'Median income rises faster than the incomes of the poorest households', ['Absolute poverty is rising', 'Prices are falling', 'The poverty line is fixed in dollars'], 'The relative line moves with the median.')],
  why=[('Explain why the Multidimensional Poverty Index may give a more complete picture of poverty than income measures.', 'Income measures miss deprivations that money alone does not capture, such as access to clean water, electricity, schooling and nutrition; the MPI measures these directly and shows the intensity of overlapping deprivations.'),
       ('Explain why relative poverty exists in high-income countries even though few people are in absolute poverty.', 'Relative poverty is defined in relation to median income, so households with incomes well above international lines can still be unable to participate fully in society\'s normal living standards.'),
       ('Explain why poverty lines are set in PPP terms.', 'Prices of basic goods differ between countries; PPP conversion ensures that the line represents a similar real standard of living everywhere.')],
  contrast=[('absolute poverty', 'relative poverty', 'Absolute poverty is income below the level needed for basic needs, the same real threshold everywhere; relative poverty is income below a percentage of the national median, so it rises with the country\'s income level.')],
  misc=[('Relative poverty can be eliminated by economic growth alone.', 'If growth raises all incomes proportionally, relative poverty is unchanged; it only falls if the incomes of the poor rise faster than the median.'),
        ('A country with no one below $3.00 a day has no poverty.', 'People may still be in relative poverty, or multidimensionally poor, lacking health, education or decent housing.')],
  cases=[('the 2025 revision of the World Bank poverty line', 'In 2025 the World Bank raised the international extreme poverty line from $2.15 (2017 PPP) to $3.00 a day (2021 PPP), raising the global count of extreme poor.', 'measuring absolute poverty', 'updated price data changed the line, showing that poverty counts depend on methodological choices'),
         ('the global MPI', 'The 2024 global MPI estimated about 1.1 billion people in acute multidimensional poverty, over half of them in sub-Saharan Africa.', 'multidimensional measures of poverty', 'many people are deprived in health, education and living standards simultaneously, not only in income'),
         ('child poverty in the UK', 'Around 4 million UK children (about 30%) lived in relative poverty after housing costs in 2022-23.', 'relative poverty in high-income countries', 'despite high average incomes, many households fall below 60% of median income, particularly after paying high rents')],
  evaluate=[('Relative poverty is a more useful measure than absolute poverty.', ['reflects social exclusion within a society', 'relevant in high-income countries', 'captures distribution'],
             ['can rise as the economy grows', 'does not show material deprivation', 'absolute measures are essential for global comparisons (SDG 1)'], 'Both are needed: absolute measures for global extreme poverty, relative measures for inclusion in high-income economies, supplemented by the MPI.')],
  )

S('ch06-st3',
  terms=[('inequality of opportunity', 'differences in people\'s chances of success caused by circumstances beyond their control, such as family background, gender, ethnicity or place of birth'),
         ('intergenerational mobility', 'the extent to which children\'s incomes and social positions differ from those of their parents'),
         ('Great Gatsby curve', 'the observed positive relationship between income inequality and low intergenerational mobility across countries'),
         ('skill-biased technological change', 'technological progress that raises the demand for, and wages of, highly skilled workers relative to low-skilled workers')],
  facts=[('Which of the following is a cause of income inequality?', 'Differences in education and human capital', ['A progressive income tax', 'Universal free schooling', 'Unemployment benefits'], 'Higher skills command higher wages.'),
         ('According to the "Great Gatsby curve", countries with higher inequality tend to have:', 'lower intergenerational income mobility', ['higher intergenerational mobility', 'lower GDP per capita', 'lower unemployment'], 'Inequality of outcome reinforces inequality of opportunity.'),
         ('Which of the following is a consequence of high inequality?', 'Lower social mobility and weaker social cohesion', ['Higher tax revenues from the poor', 'Faster growth in all cases', 'Lower crime rates'], 'High inequality is linked to lower mobility and trust.')],
  why=[('Explain why globalisation and technological change may increase income inequality within high-income countries.', 'They raise the demand for highly skilled workers while low-skilled jobs are automated or offshored to low-wage countries, increasing the wage gap between skill groups.'),
       ('Explain why high inequality may reduce economic growth.', 'Poor households under-invest in education and health, wasting human capital; high inequality can reduce AD (the rich have lower MPC), and political instability may deter investment.'),
       ('Explain why inequality of wealth tends to persist across generations.', 'Wealth generates income (rent, dividends) and can be inherited; wealthy families invest more in education and networks, so advantages are passed on.'),
       ('Explain why discrimination can be a cause of poverty.', 'Groups facing discrimination in labour markets, education or credit (by gender, ethnicity or caste) receive lower wages and fewer opportunities, reducing their incomes regardless of ability.')],
  contrast=[('equality', 'equity', 'Equality means everyone receives the same; equity means fairness, which may require unequal treatment to give everyone a fair opportunity.')],
  misc=[('Inequality is caused only by differences in effort.', 'Circumstances beyond individual control—family wealth, location, gender, discrimination and health—strongly shape incomes.'),
        ('Inequality is always harmful to an economy.', 'Some inequality provides incentives to work, train and innovate; the problem is excessive inequality and inequality of opportunity.')],
  cases=[('the Great Gatsby curve (Miles Corak)', 'Miles Corak and Alan Krueger showed that countries with high inequality, such as the USA and the UK, have lower intergenerational earnings mobility than Denmark or Finland.', 'consequences of inequality', 'unequal outcomes in one generation reduce opportunities for the next, perpetuating inequality'),
         ('caste and income in India', 'Studies find that Scheduled Caste and Scheduled Tribe households in India have significantly lower average incomes and wealth than other groups.', 'discrimination as a cause of inequality and poverty', 'social exclusion limits access to education, land and well-paid jobs'),
         ('the gender pay gap', 'The OECD average gender gap in median earnings for full-time employees is around 11-12%.', 'causes of income inequality', 'occupational segregation, motherhood penalties and discrimination reduce women\'s earnings')],
  evaluate=[('High levels of income inequality are an inevitable result of economic growth.', ['Kuznets curve: inequality rises in early industrialisation', 'returns to skills rise with technology', 'globalisation rewards capital'],
             ['Nordic countries combine growth with low inequality', 'policy choices (taxes, transfers, education) matter', 'East Asian tigers grew with relatively low inequality'], 'Inequality is not inevitable; its level reflects institutions and policies as much as growth itself.')],
  )

S('ch06-st4',
  diag=[('the effect of a minimum wage on the labour market', 'Labour market diagram; minimum wage Wmin above equilibrium W*; quantity supplied Qs exceeds quantity demanded Qd; unemployment Qs − Qd; those employed receive higher wages.'),
        ('how progressive taxation and transfer payments shift the Lorenz curve', 'Lorenz curve for pre-tax income further from the line of equality and post-tax-and-transfer Lorenz curve closer to it; Gini falls.')],
  terms=[('progressive tax', 'a tax in which the average tax rate rises as income rises, so higher earners pay a larger proportion of their income'),
         ('regressive tax', 'a tax in which the average tax rate falls as income rises, so it takes a larger proportion of the income of low earners'),
         ('transfer payments', 'payments from the government to individuals, such as pensions and unemployment benefits, with no good or service provided in return'),
         ('universal basic income (UBI)', 'a regular, unconditional cash payment made by the government to every citizen regardless of income or employment'),
         ('conditional cash transfer', 'a cash payment to poor households made on condition that they meet requirements such as sending children to school or attending health check-ups')],
  facts=[('Which tax is usually regressive?', 'A value added tax (VAT) on most goods', ['A progressive income tax', 'A wealth tax', 'A tax on capital gains'], 'Low-income households spend a larger share of income.'),
         ('Brazil\'s Bolsa Família is an example of:', 'a conditional cash transfer', ['a universal basic income', 'a progressive income tax', 'a minimum wage law'], 'Payments require school attendance and health checks.'),
         ('Which of the following is a possible disadvantage of a high minimum wage?', 'It may increase unemployment among low-skilled workers', ['It reduces the income of all workers', 'It increases inequality', 'It reduces government revenue'], 'Excess supply of labour at the higher wage.'),
         ('Which country ran a two-year basic income experiment for 2,000 unemployed people in 2017-2018?', 'Finland', ['Germany', 'Canada', 'Japan'], 'Finland paid €560 a month unconditionally.')],
  why=[('Explain why a progressive income tax reduces income inequality.', 'Higher earners pay a higher proportion of their income in tax, so post-tax incomes are more equal; the revenue can fund transfers to low-income households.'),
       ('Explain why conditional cash transfers may reduce poverty in the long run as well as the short run.', 'They raise current income, and the conditions (school attendance, health care) build children\'s human capital, raising their future earning power and breaking poverty traps.'),
       ('Explain why universal basic income could reduce the disincentive effects of means-tested benefits.', 'Means-tested benefits are withdrawn as income rises, creating high effective marginal tax rates; a UBI is not withdrawn, so recipients keep more of each extra dollar earned.'),
       ('Explain why high income tax rates may create disincentives.', 'They reduce the after-tax return to work, saving and enterprise, so some people may work fewer hours, avoid or evade tax, or move abroad.')],
  contrast=[('progressive taxation', 'regressive taxation', 'Under progressive taxation the average tax rate rises with income; under regressive taxation it falls, taking a larger share from low-income earners.'),
            ('universal basic income', 'means-tested benefits', 'A UBI is paid to everyone unconditionally; means-tested benefits are targeted at households whose income or wealth is below a threshold and are withdrawn as income rises.')],
  misc=[('A flat-rate VAT is fair because everyone pays the same rate.', 'Low-income households spend a larger proportion of income on taxed goods, so VAT takes a larger share of their income: it is regressive.'),
        ('A minimum wage always increases unemployment.', 'If set moderately, or where employers have monopsony power, minimum wages can raise pay with little or no loss of jobs, as many UK and US studies have found.')],
  cases=[('Brazil\'s Bolsa Família', 'Launched in 2003, Bolsa Família reached about a quarter of Brazil\'s population at a cost of about 0.5% of GDP, with conditions on school attendance and vaccination.', 'policies to reduce poverty and inequality', 'targeted transfers raised incomes of the poorest and contributed to a fall in Brazil\'s Gini coefficient'),
         ('Finland\'s basic income experiment', 'In 2017-2018 Finland paid 2,000 unemployed people €560 a month unconditionally; employment effects were small but recipients reported better well-being and less stress.', 'universal basic income', 'the trial suggested UBI improves well-being but is not a strong tool for raising employment'),
         ('the UK National Living Wage', 'The UK raised its National Living Wage to £12.21 an hour for workers aged 21 and over from April 2025, targeting two-thirds of median earnings.', 'minimum wages as a policy against poverty', 'large rises raised low pay with limited evidence of job losses, though some firms cut hours or raised prices')],
  evaluate=[('A universal basic income is the most effective policy for reducing poverty.', ['simple, low administrative cost', 'no stigma or benefit traps', 'security in an age of automation'],
             ['very expensive or too small to lift people out of poverty', 'untargeted: much goes to the non-poor', 'may require large tax rises', 'limited evidence on employment'], 'A UBI could complement but probably not replace targeted transfers, public services and education policies.'),
            ('Progressive taxation is the best way to reduce income inequality.', ['directly reduces the gap in post-tax incomes', 'raises revenue for transfers and services', 'automatic stabiliser'],
             ['disincentives to work and invest', 'tax avoidance and capital flight', 'does not address inequality of opportunity', 'education and health spending tackle root causes'], 'Progressive taxation is effective at reducing post-tax inequality, but long-run reductions require investment in human capital and fair labour markets.')],
  )

TAX_SYS = [
    [(0, 10_000, 0), (10_000, 40_000, 20), (40_000, 100_000, 40), (100_000, None, 45)],
    [(0, 12_000, 0), (12_000, 50_000, 15), (50_000, 120_000, 30), (120_000, None, 40)],
    [(0, 8_000, 0), (8_000, 30_000, 10), (30_000, 80_000, 25), (80_000, None, 35)],
    [(0, 15_000, 5), (15_000, 45_000, 20), (45_000, 90_000, 35), (90_000, None, 50)],
]


def tax_due(inc, sysm):
    t = 0.0
    for lo, hi, r in sysm:
        if inc > lo:
            top = inc if hi is None else min(inc, hi)
            t += (top - lo) * r / 100
    return t


def tax_desc(sysm):
    parts = []
    for lo, hi, r in sysm:
        parts.append(f'${lo:,}–${hi:,}: {r}%' if hi else f'above ${lo:,}: {r}%')
    return '; '.join(parts)


@calc('ch06-st5', 'C3', (1, 5))
def tax_rates(rng, slot):
    e = ec(rng)
    sysm = rng.choice(TAX_SYS)
    inc = rng.choice([18_000, 25_000, 36_000, 48_000, 60_000, 75_000, 95_000, 130_000, 150_000])
    t = tax_due(inc, sysm)
    avg = 100 * t / inc
    mtr = next(r for lo, hi, r in sysm if inc > lo and (hi is None or inc <= hi))
    who = name(rng)
    frame = rng.choice([f'{e} has the following income tax bands on annual taxable income: {tax_desc(sysm)}.',
                        f'The income tax schedule in {e} is: {tax_desc(sysm)} (each rate applies only to income within its band).',
                        f'In {e} income tax is charged at these marginal rates: {tax_desc(sysm)}.'])
    if slot.d <= 2:
        return dict(stem=frame + f' {who} earns ${inc:,} a year. State {who}\'s marginal tax rate and calculate the total tax paid.',
                    answer=f'Marginal tax rate = {mtr}%; tax = ${t:,.0f}',
                    markingKey=MK('Tax = sum over bands of (income in band × rate).', f'${t:,.0f} and MTR {mtr}%'), marks=2)
    if slot.d == 3:
        return dict(stem=frame + f' {who} earns ${inc:,} a year. Calculate the tax paid and the average tax rate, and state whether the system is progressive.',
                    answer=f'Tax = ${t:,.0f}; average rate = {avg:.1f}%; progressive, because the average (and marginal) rate rises with income.',
                    markingKey=MK(f'Tax by bands = {t:,.0f}; ATR = {t:,.0f}/{inc:,} × 100 = {avg:.1f}%.', f'{avg:.1f}%') + ' [R1] progressive.', marks=3)
    inc2 = inc + rng.choice([5_000, 10_000, 20_000])
    t2 = tax_due(inc2, sysm)
    eff = 100 * (t2 - t) / (inc2 - inc)
    avg2 = 100 * t2 / inc2
    return dict(stem=frame + f' {who}\'s income rises from ${inc:,} to ${inc2:,}. Calculate the average tax rate at each income, and the effective marginal tax rate on the extra income. Explain the difference between the average and marginal tax rate.',
                answer=f'ATR: {avg:.1f}% → {avg2:.1f}%; tax rises by ${t2 - t:,.0f}, so the marginal rate on the increase = {eff:.1f}%. The marginal rate applies to the last dollar earned; the average rate is total tax/total income, lower because of lower bands.',
                markingKey=MK(f'Tax {t:,.0f} → {t2:,.0f}; ATR {avg:.1f}% and {avg2:.1f}%; MTR = Δtax/Δincome = {t2 - t:,.0f}/{inc2 - inc:,} = {eff:.1f}%.', 'all rates') + ' [R1] distinction explained.', marks=4 if slot.d == 4 else 6)


@calc('ch06-st5', 'C1', (1, 3), 'mcq')
def tax_mcq(rng, slot):
    inc = rng.choice([40_000, 50_000, 80_000])
    t = rng.choice([6_000, 8_000, 10_000, 12_000])
    avg = 100 * t / inc
    return nmcq(rng, f'A person earning ${inc:,} pays ${t:,} in income tax. What is the average tax rate?', avg,
                [avg * 2, 100 - avg, t / 1000, avg / 2], f'ATR = {t:,}/{inc:,} × 100 = {r2(avg)}%.', f=lambda v: f'{r2(v)}%')


S('ch06-st5',
  terms=[('marginal tax rate', 'the percentage of tax paid on an additional unit of income'),
         ('average tax rate', 'total tax paid divided by total income, expressed as a percentage'),
         ('tax band (bracket)', 'a range of income to which a particular marginal tax rate applies'),
         ('proportional (flat) tax', 'a tax in which the average tax rate stays the same at all income levels')],
  facts=[('In a progressive income tax system, which of the following is true?', 'The marginal tax rate is above the average tax rate for higher earners', ['The average tax rate falls as income rises', 'Everyone pays the same percentage of income', 'The marginal rate is always zero'], 'Higher bands pull the average up towards the marginal rate.'),
         ('Under a proportional tax, the marginal tax rate is:', 'equal to the average tax rate', ['greater than the average tax rate', 'less than the average tax rate', 'zero'], 'A constant rate on all income.'),
         ('If income rises from $50,000 to $60,000 and tax rises from $9,000 to $12,000, what is the marginal tax rate?', '30%', ['20%', '18%', '12%'], '$3,000/$10,000 = 30%.')],
  why=[('Explain why a person moving into a higher tax band does not lose income overall.', 'The higher marginal rate applies only to income above the band threshold, not to all income, so after-tax income still rises with each extra dollar (unless benefits are withdrawn).'),
       ('Explain why the average tax rate is always below the top marginal rate in a progressive system.', 'Income in lower bands is taxed at lower (or zero) rates, which pulls total tax divided by total income below the rate applied to the top slice.')],
  contrast=[('the marginal tax rate', 'the average tax rate', 'The marginal rate is the tax on the last (additional) dollar of income; the average rate is total tax as a percentage of total income.')],
  misc=[('If I move into the 40% tax band, I will pay 40% tax on all my income.', 'Only the income above the threshold is taxed at 40%; income in lower bands is still taxed at the lower rates.'),
        ('A flat tax of 20% on all income is progressive because higher earners pay more dollars in tax.', 'Progressivity depends on the average rate rising with income; with a flat 20% the average rate is constant, so the tax is proportional (unless there is a tax-free allowance).')],
  cases=[('Estonia\'s flat income tax', 'Estonia has used a flat personal income tax since 1994 (currently 22% in 2025), with a basic tax-free allowance.', 'average and marginal tax rates', 'with a tax-free allowance, a flat marginal rate still produces an average rate that rises with income, so the system is mildly progressive'),
         ('the UK personal allowance taper', 'In the UK the £12,570 personal allowance is withdrawn by £1 for every £2 earned above £100,000, creating an effective marginal rate of 60% between £100,000 and £125,140.', 'effective marginal tax rates', 'withdrawing an allowance adds to the statutory rate, so the effective marginal rate exceeds the headline 40%')],
  evaluate=[('Very high top marginal tax rates are an effective way to reduce inequality.', ['raise revenue from those most able to pay', 'reduce post-tax inequality', 'discourage excessive executive pay'],
             ['tax avoidance and migration of high earners', 'disincentives to work and enterprise', 'revenue may fall if rates exceed the revenue-maximising level (Laffer curve)'], 'Moderately higher top rates can reduce inequality, but very high rates may raise little revenue; closing loopholes and taxing wealth may be more effective.')],
  extended=[('A tax system has a 0% rate on the first $10,000, 20% on $10,001–$40,000 and 40% above $40,000. Calculate the tax and average tax rate for incomes of $30,000 and $80,000, and explain whether the system is progressive.', '$30,000: tax $4,000, ATR 13.3%; $80,000: tax $6,000 + $16,000 = $22,000, ATR 27.5%. The ATR rises with income, so the system is progressive.', 6, 'multi_step')],
  )


# =============================================================================================
# ch07 Monetary policy
# =============================================================================================
S('ch07-st1',
  terms=[('monetary policy', 'the use of interest rates, the money supply and other tools by the central bank to influence aggregate demand, mainly to achieve low and stable inflation'),
         ('central bank', 'the institution that manages a country\'s currency, money supply and interest rates, acts as banker to the government and commercial banks and as lender of last resort'),
         ('inflation targeting', 'a monetary policy framework in which the central bank publicly commits to keep inflation at a stated target, such as 2%, and adjusts interest rates to meet it'),
         ('central bank independence', 'the freedom of the central bank to set monetary policy without political interference'),
         ('lender of last resort', 'the central bank\'s role of lending to commercial banks that face a liquidity crisis to prevent the banking system from collapsing')],
  facts=[('What is the inflation target of the Bank of England and the European Central Bank?', '2%', ['0%', '4%', '5%'], 'Both target 2% CPI inflation (the ECB symmetrically over the medium term).'),
         ('Which of the following is a function of a central bank?', 'Acting as lender of last resort to commercial banks', ['Collecting income taxes', 'Setting the government budget', 'Running state-owned enterprises'], 'Central banks provide emergency liquidity.'),
         ('The Reserve Bank of India\'s inflation target is:', '4% CPI inflation within a band of 2-6%', ['2% with no band', '0-1%', '10%'], 'India adopted flexible inflation targeting in 2016.'),
         ('Why do many governments make their central banks independent?', 'To make the commitment to low inflation more credible', ['To allow the government to print money', 'To raise tax revenue', 'To fix the exchange rate'], 'Independence reduces political business cycles.')],
  why=[('Explain why central bank independence can help keep inflation low.', 'Politicians may cut interest rates before elections to boost growth; an independent central bank focused on a target is more credible, so inflation expectations are anchored and wage and price setting moderate.'),
       ('Explain why central banks target a low positive rate of inflation rather than zero.', 'A small positive rate gives a buffer against deflation, allows real wages to adjust without nominal cuts, allows for measurement bias in the CPI and keeps interest rates above the zero lower bound.'),
       ('Explain why anchoring inflation expectations is important for monetary policy.', 'If people expect inflation to stay at the target, wage and price settings follow, so temporary shocks are less likely to create a wage-price spiral.')],
  contrast=[('monetary policy', 'fiscal policy', 'Monetary policy is run by the central bank using interest rates and the money supply; fiscal policy is run by the government using taxation and spending.')],
  misc=[('The central bank sets the interest rate on every loan in the economy.', 'It sets a policy (base) rate for lending to commercial banks; market rates follow it but also depend on risk, competition and term.'),
        ('An inflation target means the central bank only cares about inflation.', 'Most targeting is flexible: central banks also consider output and employment (the Fed has a dual mandate of maximum employment and stable prices).')],
  cases=[('the Bank of England\'s independence in 1997', 'The UK government gave the Bank of England operational independence in 1997 to set interest rates to meet an inflation target set by the government.', 'central bank independence and inflation targeting', 'removing short-term political influence helped anchor inflation expectations close to target for more than a decade'),
         ('the US Federal Reserve\'s dual mandate', 'The Fed is required by law to pursue maximum employment and stable prices, interpreted as 2% PCE inflation.', 'the goals of monetary policy', 'the Fed balances inflation and employment, for example keeping rates low in 2020-21 to support jobs'),
         ('Türkiye\'s monetary policy in 2021-2023', 'Türkiye cut interest rates in 2021-22 despite rising inflation, which exceeded 80% in late 2022, before sharply reversing course in mid-2023.', 'the importance of central bank credibility', 'perceived political pressure on the central bank damaged credibility, leading to currency depreciation and very high inflation')],
  evaluate=[('Inflation targeting is the best framework for monetary policy.', ['clear, transparent, anchors expectations', 'accountable central bank', 'record of low inflation since the 1990s'],
             ['may neglect output, employment and financial stability', 'struggles with supply shocks', 'zero lower bound limits it in deep recessions'], 'Flexible inflation targeting has worked well, but central banks also need tools for financial stability and deep recessions.')],
  )

S('ch07-st2',
  diag=[('how a cut in the central bank\'s policy interest rate affects aggregate demand', 'AD/AS diagram: lower interest rates raise C (cheaper borrowing, lower saving incentive) and I (cheaper finance), and may depreciate the currency raising X − M; AD shifts right, real GDP and the price level rise.'),
        ('how the central bank uses open market operations to change the money supply and interest rates', 'Money market diagram: vertical money supply MS and downward-sloping money demand; buying bonds increases MS from MS1 to MS2 and lowers the interest rate from i1 to i2.')],
  terms=[('open market operations', 'the buying and selling of government bonds by the central bank to change the money supply and influence interest rates'),
         ('minimum reserve requirements', 'the minimum proportion of deposits that commercial banks must hold as reserves with the central bank'),
         ('quantitative easing (QE)', 'a policy where the central bank creates money to buy large amounts of government bonds and other financial assets, to lower long-term interest rates and raise the money supply'),
         ('policy (base) interest rate', 'the interest rate set by the central bank at which it lends to commercial banks, which influences other interest rates in the economy'),
         ('expansionary monetary policy', 'monetary policy that lowers interest rates or increases the money supply to raise aggregate demand')],
  facts=[('Which of the following is an expansionary monetary policy?', 'The central bank buys government bonds from commercial banks', ['The central bank raises the reserve requirement', 'The central bank raises its policy rate', 'The government raises income tax'], 'Buying bonds increases bank reserves and the money supply.'),
         ('Quantitative easing was used by the Federal Reserve, ECB and Bank of England mainly because:', 'short-term interest rates were already close to zero', ['inflation was very high', 'governments had budget surpluses', 'exchange rates were fixed'], 'QE works when conventional rate cuts are exhausted.'),
         ('An increase in the minimum reserve requirement will:', 'reduce the amount banks can lend', ['increase the money supply', 'lower interest rates', 'increase AD'], 'More deposits must be kept as reserves.')],
  why=[('Explain why a cut in the policy interest rate can increase consumption.', 'Borrowing for durables and housing becomes cheaper, saving is less rewarding, mortgage payments fall raising disposable income, and asset prices rise (wealth effect), so households spend more.'),
       ('Explain why quantitative easing can lower long-term interest rates.', 'Central bank purchases of bonds raise bond prices; since yields move inversely to prices, long-term interest rates fall, encouraging borrowing and investment.'),
       ('Explain why selling government bonds through open market operations is contractionary.', 'Buyers pay with money from bank reserves, reducing the money supply and banks\' ability to lend, which raises interest rates and reduces AD.')],
  contrast=[('expansionary monetary policy', 'contractionary monetary policy', 'Expansionary policy lowers interest rates or increases the money supply to raise AD; contractionary policy raises rates or reduces money supply to reduce AD and inflation.'),
            ('open market operations', 'quantitative easing', 'Open market operations are routine purchases and sales of short-term bonds to keep the policy rate at target; QE is large-scale asset purchases, including long-term bonds, when the policy rate is near zero.')],
  misc=[('Quantitative easing means the government prints money to pay for its spending.', 'Under QE the central bank buys existing bonds in financial markets to lower yields; it is a monetary operation, not direct financing of government spending.'),
        ('Raising interest rates increases AD because savers earn more.', 'Higher rates usually reduce AD: borrowing and investment fall and the currency appreciates; the income gain to savers is usually smaller.')],
  cases=[('the Bank of England\'s QE programme', 'Between 2009 and 2021 the Bank of England bought £895 bn of assets, mainly government bonds.', 'quantitative easing', 'large-scale bond purchases lowered long-term yields and supported AD when Bank Rate was near zero'),
         ('the Federal Reserve\'s tightening in 2022-2023', 'The Fed raised the federal funds target range by 5.25 percentage points between March 2022 and July 2023, the fastest pace since the 1980s.', 'contractionary monetary policy', 'higher interest rates raised borrowing costs for mortgages and businesses, reducing AD to bring inflation down from 9.1% to about 3% by mid-2023'),
         ('China\'s use of reserve requirement cuts', 'The People\'s Bank of China repeatedly cut banks\' reserve requirement ratios in 2022-2024 to support lending.', 'reserve requirements as a tool', 'lower required reserves free funds for banks to lend, increasing the money supply')],
  evaluate=[('Quantitative easing is an effective policy tool in a deep recession.', ['lowers long-term rates when policy rates are at zero', 'stabilises financial markets (e.g. 2008, 2020)', 'raises asset prices and confidence'],
             ['benefits asset holders, worsening wealth inequality', 'weak transmission if banks and households do not want to borrow', 'difficult to reverse; risk of future inflation', 'may create asset bubbles'], 'QE helped prevent deeper recessions, but its effect on real activity is uncertain and its distributional side effects are significant.')],
  )

S('ch07-st3',
  diag=[('the effect of contractionary monetary policy on an inflationary gap', 'AD/AS diagram: higher interest rates shift AD left from AD1 to AD2; output falls back towards Yp and the price level falls (or rises more slowly); inflationary gap closed.')],
  terms=[('liquidity trap', 'a situation in which interest rates are close to zero and further increases in the money supply fail to lower rates or stimulate spending'),
         ('zero lower bound', 'the constraint that nominal interest rates cannot fall much below zero, limiting the use of rate cuts'),
         ('transmission mechanism', 'the channels through which changes in interest rates affect aggregate demand, output and inflation'),
         ('time lags of monetary policy', 'the delay, often 18-24 months, between a change in interest rates and its full effect on inflation and output')],
  facts=[('Why might cutting interest rates fail to increase AD during a deep recession?', 'Low confidence means households and firms do not want to borrow and spend', ['Interest rates have no effect on borrowing', 'Rate cuts always raise inflation', 'Banks cannot lend'], 'Pushing on a string.'),
         ('Monetary policy is usually considered more flexible than fiscal policy because:', 'interest rates can be changed quickly at regular meetings', ['it affects only exports', 'it has no time lags', 'it does not affect inflation'], 'Rate decisions do not need legislation.'),
         ('A liquidity trap is most associated with:', 'Japan in the 1990s and 2000s', ['Germany in the 1920s', 'the USA in the 1970s', 'Zimbabwe in 2008'], 'Rates near zero failed to revive spending.')],
  why=[('Explain why monetary policy may be ineffective in a liquidity trap.', 'With interest rates close to zero they cannot be cut much further, and with very low confidence extra money is hoarded rather than spent, so AD does not rise.'),
       ('Explain why monetary policy is less effective at dealing with cost-push inflation.', 'Raising rates reduces AD, which lowers inflation only by reducing output and employment further; the cause (higher costs) is on the supply side.'),
       ('Explain why monetary policy operates with long time lags.', 'Firms and households take time to change spending plans, many loans have fixed rates, and investment projects take time; the full impact on inflation can take 18-24 months.'),
       ('Explain why a single interest rate may not suit every region of a monetary union.', 'Regions may be at different points of the cycle; a rate appropriate for a booming region may be too high for a region in recession.')],
  contrast=[('the strengths of monetary policy', 'the constraints on monetary policy', 'Strengths: fast decisions, independence, incremental changes, no direct effect on debt. Constraints: time lags, the zero lower bound and liquidity traps, weak effect when confidence is low, and conflicts with growth and exchange-rate goals.')],
  misc=[('Lowering interest rates will always end a recession quickly.', 'Rate cuts may not work if confidence is very low or banks will not lend, and their effect takes 18-24 months; in a liquidity trap they can be ineffective.')],
  cases=[('Japan\'s liquidity trap', 'The Bank of Japan cut rates to near zero in 1999 and introduced negative rates (−0.1%) in 2016, but inflation stayed below its 2% target for most of this period.', 'constraints on monetary policy', 'with rates at the zero lower bound and weak confidence, further monetary easing had limited effects on AD'),
         ('the ECB\'s negative interest rates', 'The ECB\'s deposit rate was negative from June 2014 to July 2022, reaching −0.5%.', 'the zero lower bound', 'central banks pushed rates slightly below zero, but negative rates squeezed bank profits and had limited effects on lending'),
         ('the ECB\'s policy for the whole euro area', 'In 2022 inflation varied from about 6% in France to over 20% in Estonia, but the ECB set one interest rate for all members.', 'limits of a single monetary policy', 'one policy rate cannot suit economies with very different inflation and growth')],
  evaluate=[('Monetary policy is more effective than fiscal policy at managing aggregate demand.', ['quick to change, set by independent experts', 'no impact on government debt', 'effective at controlling demand-pull inflation'],
             ['weak in liquidity traps and deep recessions', 'long and variable time lags', 'cannot target specific sectors or regions', 'blunt and affects distribution'], 'Monetary policy is generally the main tool for demand management, but in deep recessions or at the zero lower bound fiscal policy is more effective.')],
  )


@calc('ch07-st4', 'C3', (1, 5))
def money_creation(rng, slot):
    e = ec(rng)
    if slot.d <= 2 or rng.random() < 0.5:
        nom = rng.choice([0.5, 1, 2, 3.5, 4, 5, 6, 8])
        inf = rng.choice([1, 2, 3, 4, 6, 7, 9])
        real = nom - inf
        frame = rng.choice([f'A savings account in {e} pays a nominal interest rate of {nom}% while inflation is {inf}%.',
                            f'The central bank of {e} sets its policy rate at {nom}%; annual CPI inflation is {inf}%.',
                            f'{name(rng)} takes out a loan in {e} at a nominal interest rate of {nom}% when inflation is {inf}%.'])
        return dict(stem=frame + ' Calculate the real interest rate and explain what it means for savers and borrowers.',
                    answer=f'Real interest rate = {nom} − {inf} = {r1(real)}%. {"Negative real rates erode the real value of savings and reduce the real cost of debt." if real < 0 else "Positive real rates increase the purchasing power of savings and raise the real cost of borrowing."}',
                    markingKey=MK(f'Real rate ≈ nominal − inflation = {nom} − {inf} = {r1(real)}%.', f'{r1(real)}%') + ' [R1] interpretation.', marks=2 if slot.d <= 2 else 3)
    rr = rng.choice([5, 8, 10, 12.5, 20, 25])
    dep = rng.choice([1_000, 5_000, 10_000, 50_000, 100_000])
    mult = 100 / rr
    tot = dep * mult
    loans = tot - dep
    frame = rng.choice([f'In {e}, commercial banks must hold {rr}% of deposits as reserves. A customer deposits ${dep:,} of new cash.',
                        f'{name(rng)} deposits ${dep:,} in a bank in {e}, where the reserve requirement is {rr}%.',
                        f'The central bank of {e} sets a reserve requirement of {rr}%. A new deposit of ${dep:,} enters the banking system.'])
    return dict(stem=frame + ' Calculate the money (deposit) multiplier, the maximum increase in total deposits and the maximum new lending, and explain why actual money creation is likely to be smaller.',
                answer=f'Multiplier = 1/{rr / 100} = {r2(mult)}; maximum deposits = ${tot:,.0f}; maximum new loans = ${loans:,.0f}. Actual creation is smaller because banks hold excess reserves, people hold cash (leakages) and demand for loans may be weak.',
                markingKey=MK(f'1/rr = 1/{rr / 100} = {r2(mult)}; {dep:,} × {r2(mult)} = {tot:,.0f}; loans = {tot:,.0f} − {dep:,} = {loans:,.0f}.', 'all three values') + ' [R1][R1] reasons.', marks=4 if slot.d == 4 else 6)


S('ch07-st4',
  terms=[('real interest rate', 'the nominal interest rate minus the rate of inflation; the return on saving or cost of borrowing in terms of purchasing power'),
         ('nominal interest rate', 'the interest rate stated on a loan or deposit, not adjusted for inflation'),
         ('money multiplier (deposit multiplier)', 'the maximum change in the money supply resulting from a change in bank reserves: 1 / reserve requirement'),
         ('fractional reserve banking', 'a banking system in which banks hold only a fraction of deposits as reserves and lend out the rest, thereby creating money')],
  facts=[('If the nominal interest rate is 3% and inflation is 5%, the real interest rate is:', '−2%', ['8%', '2%', '0.6%'], 'Real ≈ 3 − 5 = −2%.'),
         ('With a reserve requirement of 10%, a new deposit of $1,000 can increase total deposits by a maximum of:', '$10,000', ['$1,000', '$100', '$9,000'], 'Multiplier = 1/0.1 = 10.'),
         ('How do commercial banks create money?', 'By making loans, which create new deposits in borrowers\' accounts', ['By printing banknotes', 'By buying gold', 'By collecting taxes'], 'Loans create deposits.')],
  why=[('Explain why commercial banks are able to create money.', 'Banks keep only a fraction of deposits as reserves; when they lend the rest, the loan is spent and redeposited in other banks, which lend again, so total deposits (money) increase by a multiple of the initial deposit.'),
       ('Explain why real rather than nominal interest rates affect investment decisions.', 'Firms compare the expected real return on a project with the real cost of borrowing; if inflation is high, a high nominal rate may represent a low real cost.'),
       ('Explain why negative real interest rates may encourage borrowing.', 'If inflation exceeds the nominal rate, the real value of the debt falls over time, so borrowers repay less in purchasing power than they borrowed.')],
  contrast=[('the nominal interest rate', 'the real interest rate', 'The nominal rate is the stated rate; the real rate subtracts inflation, showing the change in purchasing power of money saved or borrowed.')],
  misc=[('A nominal interest rate of 5% always rewards savers.', 'If inflation is above 5% the real interest rate is negative, and the purchasing power of savings falls.'),
        ('With a 10% reserve requirement banks will always create exactly ten times any new deposit.', 'That is a maximum; banks may hold excess reserves, borrowers may not want loans and people may hold cash.')],
  cases=[('negative real interest rates in 2022', 'In 2022 US inflation reached 9.1% while the policy rate was below 2.5% for most of the year, so real policy rates were deeply negative.', 'the real interest rate', 'savers lost purchasing power, while the real value of fixed-rate debts fell'),
         ('the Bank of England\'s 2014 explanation of money creation', 'In 2014 the Bank of England published "Money creation in the modern economy", explaining that most money in the UK is created by commercial banks making loans.', 'money creation by commercial banks', 'lending decisions create new deposits, so the money supply depends heavily on banks\' willingness to lend and on demand for loans')],
  evaluate=[('Central banks fully control the money supply.', ['set reserve requirements and policy rates', 'can create reserves through QE', 'act as lender of last resort'],
             ['most money is created by commercial bank lending', 'demand for loans depends on confidence', 'banks may hoard reserves (2009-2015)', 'cash holdings and capital rules matter'], 'Central banks influence but do not fully control the money supply; commercial banks\' lending decisions and the demand for credit are crucial.')],
  extended=[('A central bank sets a reserve requirement of 8%. An initial $2 million of new reserves enters the banking system. Calculate the maximum increase in the money supply and explain how a rise in the reserve requirement to 10% would affect it.', 'Multiplier = 1/0.08 = 12.5, so maximum money supply increase = $25 million. At 10% the multiplier falls to 10, so the maximum increase falls to $20 million: banks can lend less of each deposit.', 4, 'multi_step')],
  )


# =============================================================================================
# ch08 Fiscal policy
# =============================================================================================
@calc('ch08-st1', 'C3', (1, 5))
def budget_balance(rng, slot):
    e = ec(rng)
    gdp = rng.choice([200, 400, 650, 800, 1200, 2500])
    rev = round(gdp * rng.choice([0.25, 0.3, 0.35, 0.4, 0.45]))
    exp_ = round(rev * rng.choice([0.9, 0.95, 1.05, 1.1, 1.15, 1.2]))
    bal = rev - exp_
    pc = 100 * bal / gdp
    frame = rng.choice([f'In {e} government revenue last year was ${rev} bn and government expenditure was ${exp_} bn. GDP was ${gdp} bn.',
                        f'The budget statement of {e} shows tax and other receipts of ${rev} bn and total public spending of ${exp_} bn, with nominal GDP of ${gdp} bn.',
                        f'{e}\'s finance ministry reports revenue of ${rev} bn, outlays of ${exp_} bn and GDP of ${gdp} bn.'])
    kind = 'deficit' if bal < 0 else 'surplus' if bal > 0 else 'balanced budget'
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the budget balance and state whether it is a deficit or a surplus.',
                    answer=f'Balance = {rev} − {exp_} = {bn(bal)}: a budget {kind}.',
                    markingKey=MK(f'Revenue − expenditure = {rev} − {exp_} = {bal}.', f'{bn(bal)} ({kind})'), marks=2)
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the budget balance as a percentage of GDP and state whether it would meet the EU Stability and Growth Pact deficit limit.',
                    answer=f'Balance = {bn(bal)} = {pc:.1f}% of GDP; {"meets" if pc >= -3 else "breaches"} the 3% deficit limit.',
                    markingKey=MK(f'{bal}/{gdp} × 100 = {pc:.1f}%.', f'{pc:.1f}%') + ' [A1] comparison with −3%.', marks=3)
    interest = round(rev * rng.choice([0.05, 0.08, 0.1, 0.12]))
    prim = bal + interest
    return dict(stem=frame + f' Expenditure includes ${interest} bn of interest payments on government debt. Calculate the overall and primary budget balance as a percentage of GDP, and explain why the primary balance is useful for assessing fiscal policy.',
                answer=f'Overall balance {bn(bal)} ({pc:.1f}% of GDP); primary balance = {bal} + {interest} = {bn(prim)} ({100 * prim / gdp:.1f}% of GDP). The primary balance excludes interest on past debt, showing whether current tax and spending decisions are adding to debt.',
                markingKey=MK(f'Overall {bal}/{gdp} = {pc:.1f}%; primary = overall + interest = {prim}, {100 * prim / gdp:.1f}%.', 'both balances') + ' [R1] explanation.', marks=4 if slot.d == 4 else 6)


S('ch08-st1',
  terms=[('fiscal policy', 'the use of government spending and taxation to influence aggregate demand and the economy'),
         ('budget deficit', 'the amount by which government expenditure exceeds government revenue in a given year'),
         ('budget surplus', 'the amount by which government revenue exceeds government expenditure in a given year'),
         ('direct tax', 'a tax paid directly to the government by the person or firm on whom it is levied, such as income tax and corporation tax'),
         ('indirect tax', 'a tax on spending on goods and services, such as VAT or excise duties, collected from sellers'),
         ('current expenditure', 'government spending on day-to-day items, such as wages of public sector workers and supplies'),
         ('capital expenditure', 'government spending on assets such as roads, schools and hospitals that add to the capital stock')],
  facts=[('Which of the following is a source of government revenue?', 'Income from state-owned enterprises and the sale of assets', ['Unemployment benefits', 'Interest paid on government debt', 'Public sector wages'], 'Besides taxes, governments earn revenue from SOEs and privatisation.'),
         ('Which of the following is a transfer payment?', 'A state pension', ['Teachers\' salaries', 'Spending on a new bridge', 'Military equipment purchases'], 'No good or service is provided in return.'),
         ('A budget deficit is financed mainly by:', 'government borrowing through issuing bonds', ['raising the reserve requirement', 'running a current account surplus', 'cutting interest rates'], 'Deficits add to the national debt.')],
  why=[('Explain why a government\'s budget deficit tends to increase during a recession.', 'Tax revenues fall as incomes, spending and profits fall, while spending on unemployment benefits rises; these automatic stabilisers widen the deficit even without policy changes.'),
       ('Explain why governments distinguish between current and capital expenditure.', 'Capital spending creates assets that raise future productive capacity and can generate future revenue, so borrowing for it is easier to justify than borrowing for day-to-day current spending.'),
       ('Explain why indirect taxes are often regressive.', 'Low-income households spend a larger proportion of their income on taxed goods, so the tax represents a larger share of their income.')],
  contrast=[('a budget deficit', 'government debt', 'A deficit is a flow: the shortfall of revenue relative to spending in one year; debt is a stock: the accumulated total of past borrowing not yet repaid.'),
            ('direct taxes', 'indirect taxes', 'Direct taxes are levied on income and wealth and paid directly by the taxpayer (income tax); indirect taxes are levied on spending and collected through sellers (VAT).')],
  misc=[('A budget surplus means the government has no debt.', 'A surplus means revenue exceeds spending this year; the stock of debt from past deficits remains, though a surplus can be used to reduce it.'),
        ('Transfer payments are counted as government spending (G) in aggregate demand.', 'Transfers redistribute income and are not payment for current output, so they are excluded from G; they affect AD indirectly through consumption.')],
  cases=[('the UK budget deficit in 2020-21', 'UK public sector net borrowing reached about 15% of GDP in 2020-21, the highest since the Second World War, because of the furlough scheme and lower tax revenue.', 'the government budget and deficits', 'a collapse in revenue and large emergency spending created a record peacetime deficit'),
         ('Norway\'s budget surpluses', 'Norway has run large budget surpluses for decades and saves oil revenue in its sovereign wealth fund, worth over $1.7 trillion (about 20,000 billion kroner) in 2025.', 'budget surpluses', 'revenue from oil exceeds government spending, so surpluses are invested for future generations')],
  evaluate=[('Governments should always aim to balance their budgets.', ['avoids growing debt and interest payments', 'reduces crowding out', 'builds credibility with markets'],
             ['prevents automatic stabilisers from working', 'deficits are appropriate in recessions', 'borrowing for productive investment raises future growth'], 'Budgets should be balanced over the cycle rather than every year, allowing deficits in recessions and surpluses in booms.')],
  )

S('ch08-st2',
  diag=[('the effect of expansionary fiscal policy on a deflationary gap in the Keynesian model', 'Keynesian AS; AD shifts right from AD1 to AD2 through higher G or lower taxes; on the horizontal/upward-sloping section, real GDP rises towards Yf with little rise in the price level; multiplier amplifies the shift.'),
        ('the effect of contractionary fiscal policy on an inflationary gap', 'AD/AS: lower G or higher taxes shift AD left; output falls back to Yp and inflationary pressure is reduced.')],
  terms=[('expansionary fiscal policy', 'an increase in government spending and/or a decrease in taxes to increase aggregate demand'),
         ('contractionary fiscal policy', 'a decrease in government spending and/or an increase in taxes to reduce aggregate demand'),
         ('discretionary fiscal policy', 'deliberate changes in government spending or taxation decided by the government'),
         ('fiscal stimulus', 'a package of increased government spending and tax cuts intended to boost aggregate demand in a downturn')],
  facts=[('Which of the following is an example of expansionary fiscal policy?', 'Increasing spending on infrastructure projects', ['Raising VAT', 'Raising interest rates', 'Selling government bonds through open market operations'], 'Higher G raises AD.'),
         ('Contractionary fiscal policy is most appropriate when:', 'there is an inflationary gap', ['there is a deep recession', 'unemployment is high and rising', 'inflation is below target'], 'Reduces excess demand.'),
         ('Why might a cut in income tax have a smaller effect on AD than an equal rise in government spending?', 'Part of the tax cut is saved or spent on imports', ['Tax cuts have no effect on AD', 'Government spending has no multiplier', 'Taxes do not affect disposable income'], 'Only the MPC share is spent in the first round.')],
  why=[('Explain how expansionary fiscal policy can reduce cyclical unemployment.', 'Higher G or lower taxes increase AD directly and through the multiplier; firms increase output and, since labour is a derived demand, hire more workers.'),
       ('Explain why fiscal policy can be used to target specific sectors or regions.', 'Spending can be directed to particular projects (e.g. infrastructure in a depressed region, subsidies for green energy) and taxes can be changed for particular groups, unlike interest rates.'),
       ('Explain why fiscal policy can affect both AD and LRAS.', 'Spending on infrastructure, education and health raises AD in the short run and increases productive capacity (LRAS) in the long run.')],
  contrast=[('discretionary fiscal policy', 'automatic stabilisers', 'Discretionary policy involves deliberate decisions to change spending or tax rates; automatic stabilisers change tax revenue and benefit spending automatically with the business cycle.')],
  misc=[('Expansionary fiscal policy always causes inflation.', 'If there is a large deflationary gap (horizontal Keynesian AS), higher AD raises output with little effect on the price level.')],
  cases=[('the US CARES Act (2020)', 'The $2.2 trillion CARES Act in March 2020 included direct payments to households, expanded unemployment benefits and loans to firms.', 'expansionary fiscal policy', 'the package supported household incomes and AD during lockdowns, helping a rapid recovery in consumption'),
         ('China\'s 2008 stimulus package', 'In November 2008 China announced a 4 trillion yuan stimulus (about 12% of GDP) focused on infrastructure.', 'fiscal policy and AD', 'large spending on railways and roads sustained growth above 9% in 2009, though it raised local government debt'),
         ('Greek austerity after 2010', 'Greece cut spending and raised taxes under its bailout programmes; real GDP fell by about a quarter between 2008 and 2013 and unemployment exceeded 27%.', 'contractionary fiscal policy', 'large cuts reduced AD sharply, deepening the recession through the multiplier')],
  evaluate=[('Expansionary fiscal policy is the most effective way to end a recession.', ['directly raises AD; multiplier effects', 'effective when monetary policy is at the zero lower bound', 'can target sectors and regions', 'infrastructure raises LRAS'],
             ['time lags in planning and approval', 'crowding out', 'rising debt and interest burdens', 'may be politically hard to reverse'], 'Fiscal policy is most effective in deep recessions with low interest rates and spare capacity, especially when well targeted and temporary.')],
  )

S('ch08-st3',
  terms=[('automatic stabilisers', 'features of the tax and benefit system, such as progressive taxes and unemployment benefits, that automatically reduce fluctuations in AD over the business cycle'),
         ('crowding out', 'the reduction in private investment (and consumption) caused by higher government borrowing that raises interest rates'),
         ('time lags of fiscal policy', 'delays in recognising a problem, deciding on, implementing and feeling the effects of a change in fiscal policy'),
         ('political constraints on fiscal policy', 'limits on fiscal policy arising from elections, opposition to tax rises or spending cuts, and legislative approval')],
  facts=[('Which of the following is an automatic stabiliser?', 'Unemployment benefits that rise during recessions', ['A new infrastructure programme', 'A cut in the central bank rate', 'A temporary VAT cut announced in a budget'], 'Benefits rise automatically when unemployment increases.'),
         ('Crowding out occurs when:', 'government borrowing raises interest rates and reduces private investment', ['private investment raises government spending', 'imports replace domestic output', 'tax cuts raise consumption'], 'Competition for loanable funds.'),
         ('Crowding out is least likely to be significant when:', 'the economy is in a deep recession with low interest rates', ['the economy is at full employment', 'interest rates are rising quickly', 'the government has very high debt'], 'Idle savings mean little competition for funds.')],
  why=[('Explain how progressive income taxes act as an automatic stabiliser.', 'In a boom, incomes rise and people move into higher bands, so tax revenue rises faster than income, restraining consumption; in a recession revenue falls faster, cushioning disposable income.'),
       ('Explain why crowding out may reduce the effectiveness of expansionary fiscal policy.', 'Higher government borrowing increases the demand for loanable funds, raising interest rates; private investment and interest-sensitive consumption fall, offsetting some of the rise in G.'),
       ('Explain why time lags can make discretionary fiscal policy destabilising.', 'By the time a recession is recognised, a policy is approved and spending takes place, the economy may already be recovering, so the stimulus adds to inflationary pressure.')],
  contrast=[('crowding out', 'crowding in', 'Crowding out is the reduction in private spending caused by government borrowing raising interest rates; crowding in is when government spending, especially on infrastructure in a recession, raises confidence and profitability, increasing private investment.')],
  misc=[('Automatic stabilisers require the government to pass new laws in each recession.', 'They work automatically through existing tax and benefit rules; no new decision is needed.')],
  cases=[('automatic stabilisers in Germany in 2009', 'Germany\'s Kurzarbeit (short-time work) scheme supported about 1.5 million workers at its peak in 2009, and unemployment barely rose despite a 5.7% fall in GDP.', 'automatic stabilisers', 'payments to workers on reduced hours automatically supported incomes and AD while keeping workers attached to firms'),
         ('the UK\'s 2022 "mini-budget"', 'In September 2022 the UK announced £45 bn of unfunded tax cuts; gilt yields rose sharply and the pound fell to a record low against the dollar, and most measures were reversed.', 'constraints on fiscal policy', 'markets\' fear about debt sustainability raised borrowing costs, showing that credibility limits expansionary policy')],
  evaluate=[('Automatic stabilisers are more useful than discretionary fiscal policy for stabilising the economy.', ['no recognition or decision lags', 'no political bargaining', 'reverse automatically in booms'],
             ['too small to offset deep shocks such as 2008 or 2020', 'cannot target specific sectors', 'weaker in countries with small welfare states'], 'Automatic stabilisers are the first line of defence, but large shocks require timely, temporary and targeted discretionary measures.')],
  )


@calc('ch08-st4', 'C3', (2, 5))
def debt_ratio(rng, slot):
    e = ec(rng)
    gdp = rng.choice([400, 500, 800, 1000, 1500])
    d0 = round(gdp * rng.choice([0.45, 0.6, 0.8, 0.95, 1.1, 1.3]))
    defp = rng.choice([1, 2, 3, 4, 5, 6])
    gg = rng.choice([0, 2, 3, 4, 5, 6])
    gdp1 = gdp * (1 + gg / 100)
    deficit = gdp1 * defp / 100
    d1 = d0 + deficit
    r0, r1_ = 100 * d0 / gdp, 100 * d1 / gdp1
    frame = rng.choice([f'At the start of the year {e}\'s government debt is ${d0} bn and nominal GDP is ${gdp} bn. During the year nominal GDP grows by {gg}% and the government runs a budget deficit of {defp}% of (new) GDP.',
                        f'{e} has public debt of ${d0} bn and GDP of ${gdp} bn. Over the next year nominal GDP is forecast to rise by {gg}%, and the deficit is projected at {defp}% of next year\'s GDP.'])
    return dict(stem=frame + ' Calculate the debt-to-GDP ratio at the start and at the end of the year, and explain whether the debt is becoming more or less sustainable.',
                answer=f'Start: {r0:.1f}%; deficit = ${deficit:.1f} bn, end debt ${d1:.1f} bn, GDP ${gdp1:.1f} bn → {r1_:.1f}%. The ratio {"rises, so debt is becoming less sustainable" if r1_ > r0 else "falls, because nominal GDP grows faster than debt, so debt is becoming more sustainable"}.',
                markingKey=MK(f'{d0}/{gdp} = {r0:.1f}%; new GDP {gdp1:.1f}; deficit {deficit:.1f}; debt {d1:.1f}; ratio {r1_:.1f}%.', 'both ratios') + ' [R1] link between deficit, growth and the ratio.', marks=4)


S('ch08-st4',
  terms=[('government (public) debt', 'the total amount owed by the government as a result of past borrowing, usually expressed as a percentage of GDP'),
         ('debt-to-GDP ratio', 'government debt as a percentage of GDP, used to assess debt sustainability'),
         ('debt servicing', 'the payment of interest and repayment of principal on debt'),
         ('credit rating', 'an assessment by agencies such as Moody\'s, S&P and Fitch of a borrower\'s ability to repay debt, which affects the interest rate it must pay'),
         ('sovereign default', 'a failure by a government to repay its debt or interest on time')],
  facts=[('Which of these countries has a government debt-to-GDP ratio of over 200%?', 'Japan', ['Germany', 'Australia', 'Chile'], 'Japan\'s gross debt is about 230-250% of GDP.'),
         ('Why can Japan sustain very high government debt at low interest rates?', 'Most of its debt is held domestically and in its own currency, much of it by the Bank of Japan', ['It has no debt interest', 'It uses the US dollar', 'It has a fixed exchange rate'], 'Domestic holders and own currency reduce default risk.'),
         ('Which of the following would reduce the debt-to-GDP ratio?', 'Nominal GDP growing faster than the stock of debt', ['A larger budget deficit', 'Higher interest rates on debt', 'A recession'], 'The denominator grows faster than the numerator.')],
  why=[('Explain why high levels of government debt may reduce future economic growth.', 'Rising interest payments divert spending from productive investment; future tax rises may reduce incentives; markets may demand higher interest rates, crowding out private investment.'),
       ('Explain why a downgrade in a country\'s credit rating can make its debt problem worse.', 'Investors demand higher yields to hold riskier bonds, raising debt-servicing costs and widening the deficit, which can further raise the debt ratio.'),
       ('Explain why debt in a foreign currency is riskier than debt in the domestic currency.', 'If the domestic currency depreciates, the value of foreign-currency debt rises in domestic terms, and the government cannot print foreign currency to repay it.')],
  contrast=[('sustainable debt', 'unsustainable debt', 'Debt is sustainable when the government can service it without large adjustments, typically when the interest rate is below nominal growth and primary deficits are moderate; it is unsustainable when the debt ratio rises without limit and creditors fear default.')],
  misc=[('Government debt is like household debt and must always be fully repaid.', 'Governments can roll over debt indefinitely, borrowing anew to repay maturing bonds; what matters is whether the debt-to-GDP ratio is stable and servicing costs are manageable.'),
        ('Any debt above 60% of GDP will cause a crisis.', 'Sustainability depends on interest rates, growth, who holds the debt and the currency; Japan has very high debt without a crisis, while some countries defaulted at much lower levels.')],
  cases=[('the Greek debt crisis', 'Greek government debt exceeded 170% of GDP by 2011; Greece needed three bailouts (2010, 2012, 2015) and a restructuring that imposed losses of over 50% on private creditors in 2012.', 'consequences of unsustainable government debt', 'loss of market confidence raised borrowing costs to unaffordable levels, forcing austerity and default'),
         ('Sri Lanka\'s default in 2022', 'Sri Lanka defaulted on its foreign debt in May 2022 after foreign exchange reserves ran out, causing shortages of fuel, food and medicine.', 'debt in foreign currency', 'without foreign reserves the government could not service dollar-denominated debt, leading to default and a severe recession'),
         ('Japan\'s high public debt', 'Japan\'s gross public debt is around 230-250% of GDP, yet ten-year bond yields stayed below 1.5% through 2024.', 'debt sustainability', 'domestic ownership, the central bank\'s bond purchases and low interest rates kept debt servicing affordable')],
  evaluate=[('High government debt is a serious threat to an economy.', ['rising interest payments crowd out public services', 'risk of loss of confidence and crisis', 'burden on future generations'],
             ['debt used for investment can raise growth', 'own-currency debt with low interest rates is manageable', 'reducing debt too quickly can cause recession (austerity)'], 'High debt is risky if it is in foreign currency, held by foreigners and rising faster than GDP; otherwise gradual stabilisation is preferable to rapid austerity.')],
  )


# =============================================================================================
# ch09 Supply-side policies
# =============================================================================================
S('ch09-st1',
  diag=[('how market-based supply-side policies affect long-run aggregate supply', 'LRAS shifts right from LRAS1 to LRAS2 (or the vertical section of the Keynesian AS shifts right); potential output rises; with constant AD, the price level falls (or inflation is lower) and real GDP rises.')],
  terms=[('supply-side policies', 'policies that aim to increase the productive capacity of the economy (LRAS) by improving the quantity and quality of factors of production and the efficiency of markets'),
         ('market-based supply-side policies', 'policies that reduce government intervention to make markets work more freely and efficiently, such as labour market reforms, deregulation and lower taxes'),
         ('labour market reforms', 'changes such as reducing trade union power, minimum wage changes, lowering unemployment benefits or easing hiring and firing rules to increase labour market flexibility'),
         ('competition policy', 'measures to increase competition, such as deregulation, privatisation, anti-monopoly regulation and trade liberalisation'),
         ('incentive-related policies', 'tax cuts on personal income, corporate profits or capital gains intended to increase incentives to work, save, invest and take risks')],
  facts=[('Which of the following is a market-based supply-side policy?', 'Cutting corporate tax rates to encourage investment', ['Increasing spending on public education', 'Building new state-owned railways', 'Raising unemployment benefits'], 'Incentive-related tax cuts are market-based.'),
         ('Which of the following is an example of a labour market reform?', 'Reducing restrictions on hiring and firing workers', ['Raising tariffs on imports', 'Building new hospitals', 'Increasing reserve requirements'], 'Increases labour market flexibility.'),
         ('Germany\'s Hartz reforms (2003-2005) mainly involved:', 'changes to unemployment benefits and job-centre services', ['nationalisation of banks', 'tariffs on Chinese imports', 'a new central bank'], 'Benefit reductions and activation policies.'),
         ('Privatisation is intended to improve efficiency because:', 'private firms face profit incentives and competition', ['it always lowers prices', 'it guarantees universal service', 'it eliminates all monopolies'], 'Profit motive encourages cost control.')],
  why=[('Explain why reducing unemployment benefits might reduce the natural rate of unemployment.', 'Lower benefits increase the incentive to search for and accept jobs, reducing the duration of frictional unemployment and voluntary unemployment.'),
       ('Explain why deregulation can increase LRAS.', 'Removing unnecessary rules lowers firms\' costs and barriers to entry; more competition encourages efficiency and innovation, raising productive capacity.'),
       ('Explain why lower corporate tax rates may increase long-term growth.', 'Higher post-tax profits increase the return on investment and retained earnings, and may attract FDI, raising the capital stock and productivity.')],
  contrast=[('market-based supply-side policies', 'interventionist supply-side policies', 'Market-based policies reduce government intervention (deregulation, tax cuts, labour market reform); interventionist policies involve active government spending and direction (education, infrastructure, R&D, industrial policy).')],
  misc=[('Supply-side policies only affect aggregate supply.', 'Many also affect AD: tax cuts raise consumption and investment, and government spending on infrastructure adds to AD in the short run.'),
        ('Cutting income tax always increases the amount people work.', 'There is a substitution effect (work pays more) but also an income effect (people can afford more leisure), so the net effect on hours is uncertain.')],
  cases=[('Thatcher-era reforms in the UK', 'In the 1980s the UK cut the top income tax rate from 83% to 40%, privatised firms such as British Telecom (1984) and British Gas (1986) and reduced trade union power.', 'market-based supply-side policies', 'the reforms aimed to increase incentives and competition, raising productivity, though inequality rose sharply'),
         ('India\'s 1991 liberalisation', 'In 1991 India abolished most industrial licensing ("licence Raj"), cut tariffs and opened to FDI.', 'competition policy and deregulation', 'reducing barriers to entry and trade increased competition and investment, contributing to faster growth'),
         ('Germany\'s Hartz reforms', 'The Hartz reforms of 2003-2005 merged benefits, reduced long-term unemployment benefits and reformed job centres; unemployment fell from about 11% in 2005 to under 6% by 2015.', 'labour market reforms', 'stronger work incentives and better job matching reduced long-term unemployment, though low-paid "mini-jobs" increased')],
  evaluate=[('Market-based supply-side policies are the best way to achieve long-term economic growth.', ['increase incentives and efficiency', 'no direct cost to the budget (deregulation)', 'can lower the natural rate of unemployment'],
             ['may increase inequality and job insecurity', 'tax cuts may not raise work effort and reduce revenue', 'privatised monopolies may need regulation', 'long time lags'], 'Market-based reforms can raise efficiency, but they work best combined with interventionist investment in skills and infrastructure, and with measures to protect equity.')],
  )

S('ch09-st2',
  terms=[('interventionist supply-side policies', 'government policies that directly invest in and support factors of production, such as education and training, healthcare, infrastructure, R&D and industrial policy'),
         ('industrial policy', 'government policies to support the development of particular industries, for example through subsidies, tax credits or public investment'),
         ('infrastructure', 'the physical and organisational structures an economy needs, such as transport, energy, water and communications networks'),
         ('research and development (R&D)', 'investment in creating new knowledge, products and processes')],
  facts=[('Which of the following is an interventionist supply-side policy?', 'Government spending on vocational training programmes', ['Reducing trade union power', 'Privatising state-owned firms', 'Cutting the top rate of income tax'], 'Direct investment in human capital.'),
         ('The US CHIPS and Science Act (2022) is an example of:', 'industrial policy supporting semiconductor production', ['a cut in interest rates', 'a tariff on Chinese goods', 'deregulation of banking'], 'About $52 bn of support for chip manufacturing and research.'),
         ('Singapore\'s SkillsFuture programme gives citizens credits for:', 'lifelong learning and training courses', ['buying houses', 'starting businesses only', 'paying taxes'], 'It funds training to upgrade skills.')],
  why=[('Explain why government spending on education is considered a supply-side policy.', 'Education raises human capital and labour productivity, increasing the quality of labour and shifting LRAS to the right in the long run.'),
       ('Explain why the market may under-provide research and development.', 'R&D creates positive externalities (knowledge spillovers) that the firm cannot fully capture, so private firms invest less than the socially optimal amount.'),
       ('Explain why infrastructure investment can increase both AD and LRAS.', 'Construction spending raises AD in the short run; once completed, better roads, ports and broadband reduce costs and raise productivity, shifting LRAS right.')],
  contrast=[('education and training', 'infrastructure investment', 'Education and training improve the quality of labour (human capital); infrastructure improves physical capital that lowers costs and connects markets.')],
  misc=[('Interventionist supply-side policies have no cost to the government.', 'They require public spending (education, infrastructure, subsidies), creating an opportunity cost and possibly higher taxes or borrowing.'),
        ('Industrial policy always works because governments can pick the winning industries.', 'Governments may lack information and face lobbying, so support can go to inefficient firms ("picking losers"); success depends on design and accountability.')],
  cases=[('South Korea\'s investment in education', 'South Korea raised tertiary enrolment to among the highest in the OECD (around 70% of young adults) and spends about 5% of GDP on R&D.', 'interventionist supply-side policies', 'investment in human capital and R&D supported its shift to high-technology industries'),
         ('the US Inflation Reduction Act (2022)', 'The IRA offers tax credits worth hundreds of billions of dollars for clean energy, electric vehicles and batteries.', 'industrial policy', 'subsidies aim to expand domestic green industries, but critics argue they distort trade and may waste resources'),
         ('China\'s high-speed rail network', 'China built over 45,000 km of high-speed rail between 2008 and 2024, the world\'s largest network.', 'infrastructure as a supply-side policy', 'faster transport reduced travel time and connected labour markets, though some lines have low usage and high debts')],
  evaluate=[('Government investment in education is the most effective supply-side policy.', ['raises productivity and potential output', 'reduces inequality of opportunity', 'positive externalities'],
             ['very long time lags', 'expensive', 'brain drain', 'quality matters more than quantity'], 'Education is one of the most effective long-run policies, but it should be combined with infrastructure and labour market policies to deliver results.')],
  )

S('ch09-st3',
  terms=[('time lag', 'the delay between implementing a policy and its effect on the economy'),
         ('equity', 'fairness in the distribution of income, wealth and opportunities'),
         ('crowding in', 'an increase in private investment encouraged by public investment or improved business conditions'),
         ('potential output', 'the level of real GDP achievable when resources are fully employed, shown by the position of LRAS')],
  facts=[('Which of the following is a strength of supply-side policies compared with demand-side policies?', 'They can increase output without causing inflation', ['They work very quickly', 'They are always cheap', 'They always reduce inequality'], 'LRAS shifts right, raising output with lower price pressure.'),
         ('Which supply-side policy is most likely to have the longest time lag?', 'Investment in primary education', ['Cutting corporate tax', 'Removing a regulation', 'A job-matching website'], 'Children educated today join the workforce in 10-20 years.'),
         ('Which supply-side policy is most likely to increase inequality?', 'Cutting top income tax rates', ['Free early childhood education', 'Public health spending', 'Training for long-term unemployed workers'], 'Gains go mainly to high earners.')],
  why=[('Explain why supply-side policies may take a long time to affect the economy.', 'Increasing human capital, building infrastructure or developing new technology takes years before productive capacity rises.'),
       ('Explain why supply-side policies can help reduce inflation in the long run.', 'By shifting LRAS to the right, they allow output to grow without excess demand, reducing pressure on the price level.'),
       ('Explain why some market-based supply-side policies may worsen equity.', 'Tax cuts favour high earners and labour market deregulation may reduce job security and wages for low-skilled workers, widening inequality.')],
  contrast=[('the effect of supply-side policies on AD', 'their effect on LRAS', 'Many supply-side policies raise AD immediately (government spending, tax cuts), while their effect on LRAS occurs only after a time lag when productive capacity increases.')],
  misc=[('Supply-side policies are always better than demand-side policies.', 'They do not address cyclical unemployment from a sudden fall in AD, and their long time lags mean demand management is still needed for short-term stabilisation.')],
  cases=[('Japan\'s "third arrow" under Abenomics', 'After 2013, Japan\'s structural reforms (the "third arrow") aimed to raise female labour participation and deregulate sectors; female participation rose sharply but productivity growth stayed weak.', 'evaluating supply-side policies', 'some reforms raised the quantity of labour but the impact on productivity was limited and slow'),
         ('labour market flexibility in the UK', 'The UK has among the least regulated labour markets in Europe, with zero-hours contracts for around a million workers.', 'trade-offs in market-based supply-side policies', 'flexibility helped keep unemployment low but created insecure jobs and weak productivity growth')],
  evaluate=[('The benefits of supply-side policies outweigh their costs.', ['increase LRAS and growth without inflation', 'reduce natural rate of unemployment', 'improve international competitiveness'],
             ['long time lags', 'high fiscal cost for interventionist policies', 'equity concerns for market-based policies', 'environmental costs of growth'], 'Usually yes in the long run, but the costs depend on design: a mix of interventionist and market-based measures with attention to equity is most effective.')],
  )


# =============================================================================================
# ch10 International trade and protection
# =============================================================================================
@calc('ch10-st1', 'C3', (1, 5))
def comp_adv(rng, slot):
    a, b = rng.sample(ECON, 2)
    g1, g2 = rng.choice([('wheat', 'cloth'), ('rice', 'textiles'), ('coffee', 'machinery'), ('wine', 'cars'),
                         ('bananas', 'smartphones'), ('fish', 'software'), ('copper', 'computers')])
    for _ in range(50):
        a1, a2, b1, b2 = rng.randint(2, 20), rng.randint(2, 20), rng.randint(2, 20), rng.randint(2, 20)
        if a1 * b2 != a2 * b1 and len({a1, a2, b1, b2}) >= 3:
            break
    oc_a = a2 / a1  # units of g2 given up per unit g1 in A
    oc_b = b2 / b1
    ca1 = a if oc_a < oc_b else b
    ca2 = b if ca1 == a else a
    frame = rng.choice([f'With the same quantity of resources, {a} can produce {a1} units of {g1} or {a2} units of {g2}, while {b} can produce {b1} units of {g1} or {b2} units of {g2}.',
                        f'The table shows the maximum output per worker per day. {a}: {g1} {a1}, {g2} {a2}. {b}: {g1} {b1}, {g2} {b2}.',
                        f'One unit of resources in {a} produces either {a1} {g1} or {a2} {g2}; in {b} the same resources produce either {b1} {g1} or {b2} {g2}.'])
    if slot.d <= 2:
        ab1 = a if a1 > b1 else b if b1 > a1 else 'neither'
        return dict(stem=frame + f' Identify which country has the absolute advantage in {g1} and calculate the opportunity cost of one unit of {g1} in each country.',
                    answer=f'Absolute advantage in {g1}: {ab1}. Opportunity cost of 1 {g1}: {a} {r2(oc_a)} {g2}; {b} {r2(oc_b)} {g2}.',
                    markingKey=MK(f'OC in {a} = {a2}/{a1} = {r2(oc_a)}; OC in {b} = {b2}/{b1} = {r2(oc_b)}.', 'both opportunity costs') + ' [A1] absolute advantage.', marks=3)
    lo, hi = sorted([oc_a, oc_b])
    stem = frame + f' (a) Calculate the opportunity cost of each good in each country. (b) Identify which country has the comparative advantage in each good. (c) State a range of terms of trade (units of {g2} per unit of {g1}) at which both countries gain from trade.'
    return dict(stem=stem,
                answer=f'(a) 1 {g1} costs {r2(oc_a)} {g2} in {a} and {r2(oc_b)} {g2} in {b}; 1 {g2} costs {r2(1 / oc_a)} {g1} in {a} and {r2(1 / oc_b)} {g1} in {b}. (b) {ca1} has the comparative advantage in {g1} (lower OC) and {ca2} in {g2}. (c) Any terms of trade between {r2(lo)} and {r2(hi)} {g2} per {g1}.',
                markingKey=MK(f'OCs computed as ratios of outputs; comparative advantage where OC is lower; mutually beneficial ToT lies between the two OCs ({r2(lo)}–{r2(hi)}).', 'correct specialisation and range'), marks=4 if slot.d <= 4 else 6)


S('ch10-st1',
  diag=[('how two countries gain from specialisation and trade according to comparative advantage, using PPCs', 'Two straight-line PPCs with different slopes (opportunity costs); each country specialises in the good with lower opportunity cost; trade at terms between the two OCs allows consumption outside each PPC.')],
  terms=[('absolute advantage', 'the ability of a country to produce more of a good than another country using the same quantity of resources'),
         ('comparative advantage', 'the ability of a country to produce a good at a lower opportunity cost than another country'),
         ('opportunity cost', 'the value of the next best alternative forgone when a choice is made'),
         ('specialisation', 'the concentration of a country\'s resources on producing the goods in which it has a comparative advantage'),
         ('terms of trade (in the Ricardian model)', 'the rate at which one good is exchanged for another in international trade')],
  facts=[('According to the theory of comparative advantage, a country should specialise in the good in which it has:', 'the lowest opportunity cost', ['the highest output per worker', 'the largest market', 'the highest price'], 'Comparative, not absolute, advantage determines gains.'),
         ('Who developed the theory of comparative advantage?', 'David Ricardo', ['Adam Smith', 'John Maynard Keynes', 'Milton Friedman'], 'Ricardo (1817), with England and Portugal producing cloth and wine.'),
         ('If country A can produce 10 cars or 20 tonnes of rice, and country B 5 cars or 20 tonnes of rice, which country has the comparative advantage in cars?', 'Country A', ['Country B', 'Neither', 'Both'], 'In A 1 car costs 2 rice; in B 1 car costs 4 rice.'),
         ('Which of the following is a source of comparative advantage?', 'Differences in factor endowments such as land, labour and capital', ['Identical technology in all countries', 'Equal wages everywhere', 'Tariffs'], 'Heckscher-Ohlin explanation.')],
  why=[('Explain why both countries can gain from trade even if one has an absolute advantage in both goods.', 'Opportunity costs differ; if each specialises in the good with lower OC and they trade at terms between their OCs, each obtains the other good more cheaply than producing it, so total output and consumption rise.'),
       ('Explain why comparative advantage can change over time.', 'Investment in human and physical capital, technology and changes in factor prices alter opportunity costs; e.g. South Korea moved from textiles to semiconductors.'),
       ('Explain why the gains from trade depend on the terms of trade.', 'Gains are shared according to the exchange ratio; terms closer to one country\'s domestic opportunity cost give most of the gain to the other country.')],
  contrast=[('absolute advantage', 'comparative advantage', 'Absolute advantage is producing more output with the same resources; comparative advantage is producing at a lower opportunity cost. Trade benefits depend on comparative advantage.')],
  misc=[('A country with no absolute advantage in anything cannot gain from trade.', 'It still has a comparative advantage in the good where its relative disadvantage is smallest (lowest OC), and both countries gain by specialising accordingly.'),
        ('Comparative advantage means that everybody in a country gains from free trade.', 'The country gains overall, but workers and firms in import-competing industries may lose; gains are not automatically shared.')],
  cases=[('Bangladesh\'s garment exports', 'Ready-made garments make up over 80% of Bangladesh\'s merchandise exports, and Bangladesh is the world\'s second-largest garment exporter after China.', 'comparative advantage', 'abundant low-cost labour gives Bangladesh a low opportunity cost in labour-intensive clothing production'),
         ('Taiwan\'s semiconductor industry', 'TSMC in Taiwan produces over 90% of the world\'s most advanced chips.', 'how comparative advantage can be created', 'decades of investment in skills, R&D and capital created a comparative advantage in high-tech manufacturing')],
  evaluate=[('The theory of comparative advantage provides a convincing case for free trade.', ['specialisation raises world output and consumption', 'lower prices and more choice', 'competition raises efficiency'],
             ['assumes full employment and mobile factors', 'ignores transport costs and economies of scale', 'gains unevenly distributed', 'may lock developing countries into primary products'], 'It provides a strong theoretical case, but real-world assumptions do not hold fully, so trade gains must be combined with adjustment policies.')],
  extended=[('Country A: 1 worker produces 6 tonnes of rice or 3 machines. Country B: 1 worker produces 4 tonnes of rice or 4 machines. Show that both countries gain if A specialises in rice and B in machines and they trade at 1 machine = 1.5 tonnes of rice.', 'OC of 1 machine: A 2 rice, B 1 rice. B has comparative advantage in machines, A in rice. At ToT 1.5 rice per machine: A pays 1.5 rice instead of 2; B gets 1.5 rice instead of 1. Both gain.', 6, 'multi_step')],
  )

S('ch10-st2',
  terms=[('World Trade Organization (WTO)', 'an international organisation of 166 members, established in 1995, which administers trade rules, negotiates trade liberalisation and settles trade disputes'),
         ('free trade', 'international trade without government-imposed barriers such as tariffs, quotas and subsidies'),
         ('most-favoured-nation principle', 'the WTO rule that a trade advantage given to one member must be given to all members'),
         ('dispute settlement', 'the WTO process for resolving trade disagreements between members through panels and the Appellate Body'),
         ('trade liberalisation', 'the reduction or removal of barriers to international trade')],
  facts=[('The WTO was established in 1995 to replace:', 'the General Agreement on Tariffs and Trade (GATT)', ['the IMF', 'the World Bank', 'the European Union'], 'GATT (1947) became part of the WTO framework.'),
         ('Which of the following is an objective of the WTO?', 'Reducing barriers to trade and settling trade disputes', ['Lending to countries with BoP problems', 'Setting exchange rates', 'Providing development aid'], 'Lending is the IMF\'s role.'),
         ('Why has the WTO\'s dispute settlement system been weakened since December 2019?', 'The USA blocked appointments to the Appellate Body', ['China left the WTO', 'The WTO was dissolved', 'The EU refused to pay its fees'], 'Without enough judges, the Appellate Body could not hear appeals.'),
         ('Which round of WTO negotiations, launched in 2001, has largely stalled?', 'The Doha Development Round', ['The Uruguay Round', 'The Kennedy Round', 'The Tokyo Round'], 'Disagreements over agriculture, especially subsidies.')],
  why=[('Explain why free trade can lead to lower prices for consumers.', 'Imports from lower-cost producers and greater competition force domestic firms to cut costs and prices, and economies of scale in larger markets reduce average costs.'),
       ('Explain why free trade can increase economic efficiency.', 'Resources move to industries with comparative advantage (allocative efficiency) and competition encourages firms to cut waste and innovate (productive and dynamic efficiency).'),
       ('Explain why developing countries have criticised the WTO.', 'High-income countries maintain agricultural subsidies and tariffs on processed goods while pressing developing countries to open markets; negotiation capacity is unequal.')],
  contrast=[('the WTO', 'a regional trade agreement', 'The WTO sets multilateral rules for all 166 members on a non-discriminatory (MFN) basis; a regional trade agreement liberalises trade only among its members, discriminating against non-members.')],
  misc=[('The WTO forces all countries to have zero tariffs.', 'Members negotiate bound maximum tariff rates; tariffs can remain positive, and developing countries have special and differential treatment.')],
  cases=[('China\'s accession to the WTO in 2001', 'After joining the WTO in 2001, China\'s exports grew from about $270 bn in 2001 to over $3.3 trillion by 2022.', 'the case for free trade', 'lower barriers allowed China to specialise according to comparative advantage, raising output and incomes'),
         ('the US-EU Airbus-Boeing dispute', 'The WTO ruled that both the EU and the USA had given illegal subsidies to aircraft makers, authorising tariffs; the two sides agreed a five-year truce in 2021.', 'the role of the WTO', 'dispute settlement provided legal rulings and authorised retaliation, encouraging a negotiated settlement')],
  evaluate=[('The WTO has been successful in promoting free trade.', ['average tariffs have fallen greatly since 1947', 'rules-based system and dispute settlement', 'membership of 166 countries'],
             ['Doha Round stalled', 'Appellate Body paralysed since 2019', 'rise of US-China tariffs and industrial subsidies', 'agriculture remains highly protected'], 'The WTO was successful in reducing tariffs historically, but its effectiveness has weakened as major economies turn to unilateral measures and regional deals.')],
  )


@calc('ch10-st3', 'C3', (2, 5))
def tariff_welfare(rng, slot):
    good = rng.choice(['steel', 'sugar', 'rice', 'cars', 'washing machines', 'solar panels', 'shoes'])
    e = ec(rng)
    for _ in range(200):
        b = rng.choice([1, 2, 4, 5])
        d = rng.choice([1, 2, 3, 4, 5])
        Pw = rng.randint(4, 12)
        t = rng.randint(1, 5)
        a = rng.randint(60, 200)
        c = rng.choice([-20, -10, 0, 10])
        Qd0, Qs0 = a - b * Pw, c + d * Pw
        P1 = Pw + t
        Qd1, Qs1 = a - b * P1, c + d * P1
        Pe = (a - c) / (b + d)
        if Qs0 >= 0 and Qd1 > Qs1 > Qs0 and P1 < Pe:
            break
    else:
        return None
    M0, M1 = Qd0 - Qs0, Qd1 - Qs1
    rev = t * M1
    cs = t * (Qd1 + Qd0) / 2
    ps = t * (Qs0 + Qs1) / 2
    dwl = 0.5 * t * (Qs1 - Qs0) + 0.5 * t * (Qd0 - Qd1)
    D = f'Qd = {a} − {b}P' if b != 1 else f'Qd = {a} − P'
    dd = '' if d == 1 else str(d)
    S_ = f'Qs = {c} + {dd}P' if c > 0 else (f'Qs = {dd}P' if c == 0 else f'Qs = −{-c} + {dd}P')
    frame = rng.choice([f'The domestic market for {good} in {e} is described by {D} and {S_} (P in $, Q in thousand units). The world price is ${Pw} and {e} can import any quantity at that price. The government imposes a tariff of ${t} per unit.',
                        f'In {e}, demand for {good} is {D} and domestic supply is {S_}, with P in dollars and Q in thousands. Under free trade the price is the world price of ${Pw}. To protect domestic producers, a specific tariff of ${t} is introduced.',
                        f'{e} is a small importer of {good}. Domestic demand: {D}; domestic supply: {S_}; world price ${Pw}; proposed tariff ${t} per unit (Q in thousands).'])
    if slot.d <= 3:
        return dict(stem=frame + ' Calculate the quantity of imports before and after the tariff, and the government\'s tariff revenue.',
                    answer=f'Before: Qd = {Qd0}, Qs = {Qs0}, imports = {M0} thousand. After (P = ${P1}): Qd = {Qd1}, Qs = {Qs1}, imports = {M1} thousand. Revenue = ${t} × {M1} thousand = ${rev:,} thousand.',
                    markingKey=MK(f'At ${Pw}: imports {Qd0} − {Qs0} = {M0}; at ${P1}: {Qd1} − {Qs1} = {M1}; revenue = {t} × {M1} = {rev}.', 'imports and revenue'), marks=4)
    return dict(stem=frame + ' Calculate (i) the change in consumer surplus, (ii) the change in producer surplus, (iii) tariff revenue and (iv) the welfare (deadweight) loss. Explain who gains and who loses from the tariff.',
                answer=f'(i) CS falls by ${cs:,.1f} thousand; (ii) domestic PS rises by ${ps:,.1f} thousand; (iii) revenue = ${rev:,} thousand; (iv) welfare loss = ${dwl:,.1f} thousand. Domestic producers and the government gain; consumers lose more than these gains, and foreign producers sell less.',
                markingKey=MK(f'Price rises {Pw} → {P1}. ΔCS = {t} × ({Qd0} + {Qd1})/2 = {cs:.1f}; ΔPS = {t} × ({Qs0} + {Qs1})/2 = {ps:.1f}; revenue = {t} × {M1} = {rev}; DWL = ½×{t}×({Qs1}−{Qs0}) + ½×{t}×({Qd0}−{Qd1}) = {dwl:.1f}.', 'all four values') + ' [R1] stakeholders.', marks=6)


S('ch10-st3',
  diag=[('the effects of a tariff on a small importing economy', 'Domestic D and S with world price Pw (horizontal world supply); tariff raises price to Pw + t; domestic output rises, consumption falls, imports fall; label consumer surplus loss, producer surplus gain, government revenue and the two welfare-loss triangles.'),
        ('the effects of an import quota', 'Domestic D and S with world price; quota limits imports, shifting supply to S + quota; price rises above Pw; domestic producers gain, consumers lose; quota rent goes to import licence holders; welfare loss.'),
        ('the effects of a production subsidy to domestic firms facing import competition', 'Domestic supply shifts right (S to S + subsidy); price stays at Pw; domestic output rises, imports fall, consumption unchanged; cost to government; welfare loss triangle.')],
  terms=[('tariff', 'a tax on imported goods'),
         ('import quota', 'a legal limit on the quantity or value of a good that can be imported'),
         ('production subsidy', 'a payment by the government to domestic producers, lowering their costs so they can compete with imports'),
         ('administrative barriers', 'non-tariff barriers such as complex customs procedures, strict standards, licensing and health and safety regulations that make importing more difficult'),
         ('welfare (deadweight) loss', 'the loss of total surplus due to the misallocation of resources caused by trade protection')],
  facts=[('Which of the following groups gains from a tariff?', 'Domestic producers of the protected good', ['Domestic consumers', 'Foreign producers', 'Firms that use the good as an input'], 'Higher domestic price raises their output and surplus.'),
         ('Unlike a tariff, a production subsidy:', 'does not raise the price paid by consumers', ['raises revenue for the government', 'reduces domestic output', 'raises the price to consumers'], 'Price stays at the world price.'),
         ('In 2018 the USA imposed tariffs of 25% on imports of:', 'steel', ['rice', 'coffee', 'tea'], 'Section 232 tariffs: 25% on steel, 10% on aluminium.'),
         ('With an import quota, the revenue that would have gone to the government under a tariff goes to:', 'holders of import licences (quota rent)', ['domestic consumers', 'the WTO', 'nobody'], 'Licence holders buy at Pw and sell at the higher domestic price.')],
  why=[('Explain why a tariff creates a welfare loss.', 'Higher-cost domestic producers replace cheaper imports (production inefficiency) and consumers who valued the good above the world price no longer buy it (consumption loss); these surplus losses are not gained by anyone.'),
       ('Explain why a tariff may harm domestic firms that use the protected good as an input.', 'They must pay a higher price for the input, raising costs, reducing competitiveness and possibly employment in user industries (e.g. US car makers after steel tariffs).'),
       ('Explain why administrative barriers can be as restrictive as tariffs.', 'Long customs procedures, unusual standards and licensing raise the cost and uncertainty of importing, reducing trade without collecting revenue.')],
  contrast=[('a tariff', 'an import quota', 'A tariff raises the price of imports and generates government revenue, but the quantity of imports can vary; a quota fixes the quantity of imports, and the extra revenue goes to licence holders rather than the government.'),
            ('a production subsidy', 'a tariff', 'A subsidy lowers domestic producers\' costs, keeping the price at the world level and costing the government money; a tariff raises the price paid by consumers and raises revenue.')],
  misc=[('A tariff is paid by foreign exporters, so it does not harm domestic consumers.', 'The tariff is paid by importers and largely passed on in higher prices; studies of the 2018 US tariffs found almost full pass-through to US prices.'),
        ('Quotas are better than tariffs because they do not raise prices.', 'Quotas restrict supply, so domestic prices rise; unlike tariffs, they generate no government revenue.')],
  cases=[('the US tariffs on washing machines in 2018', 'After the USA imposed safeguard tariffs on washing machines in 2018, their prices rose by about 12%, and the prices of dryers (not subject to tariffs) also rose.', 'the effects of a tariff', 'consumers paid higher prices; estimates suggested a cost of over $800,000 per job created'),
         ('US-China tariffs from 2018', 'The USA imposed tariffs on about $370 bn of Chinese goods in 2018-2019 and China retaliated against US exports such as soybeans.', 'tariffs and retaliation', 'tariffs raised costs for US importers and consumers while retaliation hurt US farmers, requiring government support payments'),
         ('Japan\'s rice protection', 'Japan protects its rice farmers with a tariff-rate quota; imports above the quota face a tariff of 341 yen per kg, often equivalent to several hundred per cent.', 'tariffs and quotas', 'very high protection keeps domestic prices far above world prices, benefiting farmers at consumers\' expense')],
  evaluate=[('Tariffs are an effective way to protect domestic jobs.', ['protect jobs in import-competing industries in the short run', 'raise government revenue', 'can buy time for adjustment'],
             ['jobs lost in user industries and exporters hit by retaliation', 'high cost per job saved', 'consumers pay higher prices', 'reduce incentives to become efficient'], 'Tariffs may save some jobs in the protected industry but often cost more jobs elsewhere; adjustment assistance is usually more efficient.')],
  )

S('ch10-st4',
  terms=[('infant industry argument', 'the argument that new industries need temporary protection until they grow large enough to benefit from economies of scale and compete internationally'),
         ('dumping', 'selling goods in a foreign market at a price below their cost of production or below the price in the home market'),
         ('anti-dumping duty', 'a tariff imposed on imports judged to be dumped, to raise their price to a fair level'),
         ('national security argument', 'the argument for protecting strategic industries such as defence, energy, food and semiconductors to avoid dependence on other countries'),
         ('retaliation', 'the imposition of trade barriers by a country in response to barriers imposed by another')],
  facts=[('Which of the following is the infant industry argument for protection?', 'New industries need temporary protection to achieve economies of scale', ['Protection reduces prices for consumers', 'Old industries need permanent protection', 'Tariffs increase competition'], 'Protection until mature.'),
         ('Which of the following is an argument against trade protection?', 'It may lead to retaliation and trade wars', ['It protects jobs', 'It raises government revenue', 'It protects infant industries'], 'Retaliation harms exporters.'),
         ('Anti-dumping duties are permitted by the WTO when:', 'imports are sold below normal value and cause material injury to domestic industry', ['any import becomes popular', 'the exporting country has lower wages', 'a country has a trade deficit'], 'WTO Anti-Dumping Agreement.')],
  why=[('Explain why protection may lead to inefficiency in domestic industries.', 'Protected firms face less competition, so they have weaker incentives to cut costs and innovate, resulting in productive and dynamic inefficiency.'),
       ('Explain why the infant industry argument is difficult to apply in practice.', 'Governments struggle to identify which industries will become competitive, and protected industries lobby to keep protection, so "infants" may never grow up.'),
       ('Explain why some countries argue for protection on grounds of national security.', 'Dependence on imports of strategic goods such as food, energy, medical supplies or semiconductors could be exploited by other countries in a crisis.')],
  contrast=[('arguments for trade protection', 'arguments against trade protection', 'For: protecting infant industries, jobs, national security, anti-dumping, raising revenue, correcting BoP deficits. Against: higher prices, inefficiency, misallocation of resources, retaliation and reduced export competitiveness.')],
  misc=[('Protection is always justified to protect domestic jobs.', 'Protection may save some jobs in protected industries but destroy jobs in industries using imported inputs or facing retaliation, and consumers pay higher prices.')],
  cases=[('South Korea\'s use of infant industry protection', 'South Korea protected and subsidised industries such as steel, shipbuilding and cars in the 1960s-1980s while requiring firms to export.', 'the infant industry argument', 'temporary protection combined with export targets helped firms like Hyundai and POSCO become globally competitive'),
         ('EU anti-dumping duties on Chinese solar panels', 'In 2013 the EU imposed anti-dumping duties on Chinese solar panels, later replaced by minimum import prices until 2018.', 'anti-dumping as an argument for protection', 'protecting EU producers from below-cost imports raised the cost of solar installations for European consumers'),
         ('US tariffs announced in 2025', 'In April 2025 the US government announced a baseline 10% tariff on most imports, with higher rates for many countries, citing trade deficits and national security.', 'arguments for and against protection', 'supporters cited jobs and security; critics warned of higher consumer prices, supply-chain disruption and retaliation')],
  evaluate=[('The arguments for trade protection outweigh the arguments against it.', ['infant industries', 'national security in strategic goods', 'anti-dumping', 'protecting jobs during adjustment'],
             ['higher prices and welfare loss', 'retaliation', 'inefficiency', 'harm to developing-country exporters'], 'Most economists conclude that the costs of protection usually outweigh its benefits, except for narrow cases such as genuine dumping or strategic security concerns.')],
  )


# =============================================================================================
# ch11 Economic integration
# =============================================================================================
S('ch11-st1',
  terms=[('preferential trade agreement (PTA)', 'an agreement between countries to lower trade barriers on some goods from member countries, giving them preferential access'),
         ('free trade area', 'an agreement in which member countries remove trade barriers among themselves but each keeps its own barriers against non-members'),
         ('customs union', 'a free trade area in which members also adopt a common external tariff against non-members'),
         ('common market', 'a customs union that also allows free movement of factors of production, such as labour and capital, among members'),
         ('rules of origin', 'rules in a free trade area that determine whether a good counts as produced within the area and therefore qualifies for tariff-free trade'),
         ('bilateral trade agreement', 'a trade agreement between two countries')],
  facts=[('Which of the following is a customs union?', 'Mercosur', ['USMCA', 'ASEAN Free Trade Area', 'CPTPP'], 'Mercosur has a common external tariff.'),
         ('USMCA, which replaced NAFTA in 2020, is an example of:', 'a free trade area', ['a customs union', 'a common market', 'a monetary union'], 'Members keep separate external tariffs.'),
         ('Which feature distinguishes a common market from a customs union?', 'Free movement of labour and capital', ['A common external tariff', 'Zero tariffs among members', 'A common currency'], 'The EU single market (1993) is the key example.'),
         ('The African Continental Free Trade Area (AfCFTA), which began trading in 2021, aims to:', 'create a single market for goods and services across African Union members', ['create a single African currency immediately', 'raise tariffs on intra-African trade', 'replace the WTO'], 'It is the largest FTA by number of countries.')],
  why=[('Explain why free trade areas need rules of origin but customs unions do not.', 'In an FTA members have different external tariffs, so without rules of origin goods could enter through the lowest-tariff member and be re-exported tariff-free (trade deflection); a common external tariff removes this incentive.'),
       ('Explain why countries join trading blocs.', 'Access to larger markets, economies of scale, increased competition and efficiency, more FDI and greater bargaining power in international negotiations.'),
       ('Explain why trading blocs may conflict with the aims of the WTO.', 'They discriminate against non-members, breaking the most-favoured-nation principle and possibly diverting trade from more efficient outside producers.')],
  contrast=[('a free trade area', 'a customs union', 'In a free trade area members remove barriers among themselves but keep their own external tariffs; a customs union also adopts a common external tariff and usually negotiates trade as a bloc.'),
            ('a customs union', 'a common market', 'A common market goes beyond a customs union by allowing free movement of factors of production (labour and capital), not just goods.')],
  misc=[('In a free trade area all members must charge the same tariff on imports from outside.', 'That describes a customs union; FTA members set their own external tariffs.'),
        ('Brexit means the UK no longer trades freely with the EU at all.', 'The UK-EU Trade and Cooperation Agreement (2021) keeps zero tariffs and quotas on goods meeting rules of origin, but the UK left the customs union and single market, so non-tariff barriers increased.')],
  cases=[('the European single market', 'Launched in 1993, the EU single market allows free movement of goods, services, capital and people among 27 member states (plus EEA members).', 'a common market', 'removing barriers to factor movements as well as goods deepened integration beyond a customs union'),
         ('Brexit and UK-EU trade', 'Since leaving the EU single market and customs union in 2021, UK exporters face customs declarations, rules of origin and regulatory checks, and studies estimate UK goods trade with the EU is around 15% lower than otherwise.', 'the difference between an FTA and a common market', 'moving from a common market to an FTA introduced non-tariff barriers, reducing trade'),
         ('ASEAN\'s free trade area', 'The ASEAN Free Trade Area has reduced tariffs on almost all intra-ASEAN trade to 0-5% for its ten members.', 'a free trade area', 'members liberalised trade among themselves while keeping separate external tariffs')],
  evaluate=[('Regional trading blocs are a stepping stone towards global free trade.', ['liberalise trade among many countries', 'deeper integration than WTO rules (services, standards)', 'build institutions and support for openness'],
             ['trade diversion harms outsiders', 'complex "spaghetti bowl" of rules of origin', 'reduce interest in multilateral negotiations', 'can become rival blocs'], 'Blocs can be building blocks if open and WTO-consistent, but proliferation of overlapping agreements and diversion may also make them stumbling blocks.')],
  )

S('ch11-st2',
  terms=[('monetary union', 'a group of countries that share a single currency and a single central bank with one monetary policy'),
         ('European Central Bank (ECB)', 'the central bank of the eurozone, which sets the single interest rate for all member countries with a mandate of price stability (2% inflation)'),
         ('asymmetric shock', 'an economic shock that affects one member of a monetary union differently from the others'),
         ('optimal currency area', 'a region where the benefits of a single currency outweigh the costs, typically because of labour mobility, flexible wages, fiscal transfers and similar business cycles')],
  facts=[('When were euro banknotes and coins introduced?', '2002', ['1993', '1999', '2008'], 'The euro was introduced electronically in 1999 and as cash in 2002.'),
         ('Which country became the 20th member of the eurozone in 2023?', 'Croatia', ['Poland', 'Sweden', 'Denmark'], 'Croatia adopted the euro on 1 January 2023.'),
         ('Which of the following is an advantage of monetary union?', 'Elimination of transaction costs and exchange-rate risk on trade among members', ['Each member can set its own interest rate', 'Members can devalue to restore competitiveness', 'Fiscal policy becomes unnecessary'], 'Single currency removes exchange costs.'),
         ('Which of the following is a disadvantage of monetary union?', 'Loss of independent monetary policy', ['More exchange-rate risk', 'Higher transaction costs', 'Less price transparency'], 'One interest rate for all members.')],
  why=[('Explain why a member of a monetary union may find it harder to recover from a recession.', 'It cannot cut its own interest rates or devalue its currency; it must rely on fiscal policy (limited by deficit rules) or falling wages and prices (internal devaluation), which is slow and painful.'),
       ('Explain why a single currency can increase trade among member countries.', 'It removes currency conversion costs and exchange-rate uncertainty, and makes prices transparent, encouraging cross-border trade and investment.'),
       ('Explain why labour mobility is important for the success of a monetary union.', 'If one region suffers an asymmetric shock, workers can move to regions with jobs, reducing unemployment without exchange-rate adjustment.')],
  contrast=[('a common market', 'a monetary union', 'A common market allows free movement of goods, services and factors; a monetary union adds a single currency and a single monetary policy.')],
  misc=[('In a monetary union each country\'s central bank chooses its own interest rate.', 'There is one interest rate set by a single central bank (the ECB) for all members.')],
  cases=[('the euro-area sovereign debt crisis', 'Between 2010 and 2012 Greece, Ireland, Portugal, Spain and Cyprus needed financial assistance; without their own currencies they could not devalue and had to cut wages and spending.', 'disadvantages of monetary union', 'asymmetric shocks and the loss of independent monetary and exchange-rate policy forced painful internal devaluation'),
         ('Germany\'s gains from the euro', 'Germany\'s current account surplus rose to about 8% of GDP in the mid-2010s.', 'the effects of a single currency', 'a euro valued for the whole area was weaker than a German mark would have been, boosting German export competitiveness'),
         ('Estonia\'s adoption of the euro in 2011', 'Estonia joined the euro in 2011 despite the recent crisis and later experienced inflation above 20% in 2022, the highest in the euro area.', 'one monetary policy for different economies', 'the ECB\'s interest rate was set for the whole area and was too low for Estonia\'s overheating economy')],
  evaluate=[('The benefits of the euro have outweighed its costs for member countries.', ['lower transaction costs and exchange risk', 'price transparency and competition', 'low inflation and credibility for previously high-inflation members', 'deeper capital markets'],
             ['loss of independent monetary policy and exchange-rate adjustment', 'asymmetric shocks and the 2010-2012 crisis', 'limited fiscal transfers and labour mobility', 'divergence between core and periphery'], 'Benefits have been greater for open, well-synchronised economies; for periphery economies costs were large during crises, so the outcome depends on convergence and on fiscal and banking union.')],
  )


@calc('ch11-st3', 'C3', (2, 5))
def trade_creation(rng, slot):
    a, b, c = rng.sample(ECON, 3)
    good = rng.choice(['bicycles', 'televisions', 'shirts', 'tablet computers', 'tyres', 'refrigerators'])
    for _ in range(100):
        dom = rng.randint(60, 120)
        world = rng.randint(30, 70)
        partner = rng.randint(world + 2, world + 30)
        tar = rng.choice([25, 40, 50, 60, 80, 100])
        wt = world * (1 + tar / 100)
        pt = partner * (1 + tar / 100)
        if slot.d >= 4:
            ok = wt < dom and partner < wt
        else:
            ok = wt > dom and partner < dom
        if ok and partner < dom:
            break
    else:
        return None
    frame = rng.choice([f'{a} can produce {good} domestically at ${dom} each. {b} can supply them at ${partner} and {c} at ${world} (the lowest-cost producer). {a} charges a tariff of {tar}% on all imports.',
                        f'The cost of a unit of {good}: domestic producers in {a} ${dom}; producers in {b} ${partner}; producers in {c} ${world}. {a} has an ad valorem tariff of {tar}% on imports.'])
    stem = frame + f' {a} then forms a customs union with {b}, removing the tariff on imports from {b} but keeping it on {c}. Determine where {a} buys {good} before and after the customs union, and state whether this is trade creation or trade diversion.'
    if wt > dom:
        ans = f'Before: domestic ${dom} < {b} ${pt:.0f} and {c} ${wt:.0f} with tariff, so {a} produces domestically. After: {b} sells at ${partner} < ${dom}, so {a} imports from {b} – trade creation (higher-cost domestic output replaced by lower-cost imports).'
    else:
        ans = f'Before: {c}\'s price with tariff = ${wt:.0f}, lower than domestic ${dom} and {b} ${pt:.0f}, so {a} imports from {c}. After: {b} sells tariff-free at ${partner} < ${wt:.0f}, so {a} imports from {b} – trade diversion (from the lowest-cost producer {c} to the higher-cost partner {b}); the government also loses tariff revenue.'
    return dict(stem=stem, answer=ans,
                markingKey=f'[M1] tariff-inclusive prices: {c} ${wt:.0f}, {b} ${pt:.0f}; [A1] source before; [A1] source after; [R1] correct classification. ' + ans, marks=4)


S('ch11-st3',
  terms=[('trade creation', 'the replacement of higher-cost domestic production (or higher-cost imports) by lower-cost imports from a member of a trading bloc, increasing efficiency'),
         ('trade diversion', 'the replacement of lower-cost imports from a non-member by higher-cost imports from a member of a trading bloc, because of the common external tariff'),
         ('common external tariff', 'a single tariff imposed by all members of a customs union on imports from non-members'),
         ('static effects of integration', 'immediate effects on resource allocation, such as trade creation and trade diversion')],
  facts=[('Trade diversion occurs when:', 'imports switch from a low-cost non-member to a higher-cost member', ['domestic production is replaced by cheaper imports from a member', 'a country leaves a customs union', 'tariffs on all countries are removed'], 'Efficiency falls.'),
         ('Trade creation increases welfare because:', 'lower-cost producers replace higher-cost producers', ['tariff revenue increases', 'imports from outside rise', 'domestic producers expand'], 'Better allocation of resources.'),
         ('Which of the following makes trade diversion more likely?', 'A high common external tariff', ['A low common external tariff', 'Free trade with all countries', 'Low transport costs from non-members'], 'High outside tariffs make the partner relatively cheaper.')],
  why=[('Explain why trade diversion reduces world efficiency.', 'Production shifts from the lowest-cost producer outside the bloc to a higher-cost producer inside it, so more resources are used to produce the same goods.'),
       ('Explain why a customs union may cause both trade creation and trade diversion.', 'Removing internal tariffs lets members replace costly domestic output with cheaper partner imports (creation), but the external tariff may make a partner cheaper than a more efficient outsider (diversion).')],
  contrast=[('trade creation', 'trade diversion', 'Trade creation replaces higher-cost domestic production with lower-cost imports from a partner, raising efficiency; trade diversion replaces lower-cost non-member imports with higher-cost partner imports, reducing efficiency.')],
  misc=[('Joining a customs union always increases economic efficiency.', 'If trade diversion outweighs trade creation, efficiency and welfare can fall.')],
  cases=[('the UK joining the EEC in 1973', 'When the UK joined the EEC, it adopted the Common External Tariff, and imports of food such as butter and lamb shifted from New Zealand and Australia towards European producers.', 'trade diversion', 'lower-cost Commonwealth suppliers were replaced by higher-cost European producers protected by the common tariff and CAP'),
         ('Mercosur and Brazilian car trade', 'After Mercosur was formed, Argentina\'s imports of cars and parts shifted strongly towards Brazil.', 'trade creation and diversion', 'some trade replaced costly domestic production (creation), while some replaced cheaper imports from outside the bloc (diversion)')],
  evaluate=[('Customs unions generally create more trade than they divert.', ['members are often natural trading partners', 'dynamic gains: economies of scale, competition, FDI', 'evidence from the EU single market'],
             ['high external tariffs encourage diversion', 'outsiders lose market access', 'CAP-type policies divert agricultural trade'], 'The balance depends on the height of the common external tariff and on whether members are already efficient producers; dynamic gains often matter more than static effects.')],
  )


# =============================================================================================
# ch12 Exchange rates
# =============================================================================================
@calc('ch12-st1', 'C3', (1, 5))
def fx_convert(rng, slot):
    e = ec(rng)
    cname = rng.choice(CURNAME)
    code = cname.split('(')[1].rstrip(')')
    r0 = rng.choice([2, 4, 5, 8, 10, 12.5, 16, 20, 25, 40, 80, 120])
    if slot.d <= 2:
        price = rng.choice([50, 120, 300, 750, 1200, 4000])
        usd = price / r0
        frame = rng.choice([f'The exchange rate is ${1} = {r0} {code}.', f'One US dollar buys {r0} units of the {cname}.',
                            f'On the foreign exchange market, 1 USD = {r0} {code}.'])
        return dict(stem=frame + f' A good costs {price:,} {code} in {e}. Calculate its price in US dollars, and the value of 1 {code} in dollars.',
                    answer=f'Price = {price:,}/{r0} = ${usd:,.2f}; 1 {code} = ${1 / r0:.4f}',
                    markingKey=MK(f'{price:,} ÷ {r0} = {usd:,.2f}; 1/{r0} = {1 / r0:.4f}.', 'both values'), marks=2)
    ch = rng.choice([-25, -20, -15, -10, 10, 15, 20, 25])
    r1_ = r0 * (1 + ch / 100)
    pc = pct(1 / r1_, 1 / r0)
    exp_price = rng.choice([500, 1000, 2000, 5000])
    frame = rng.choice([f'The exchange rate of the {cname} moves from $1 = {r0} {code} to $1 = {r2(r1_)} {code}.',
                        f'Over a year, the price of one US dollar in {e} changes from {r0} {code} to {r2(r1_)} {code}.'])
    if slot.d == 3:
        return dict(stem=frame + f' State whether the {code} has appreciated or depreciated, and calculate the percentage change in the value of the {code} against the dollar.',
                    answer=f'The {code} has {"depreciated" if ch > 0 else "appreciated"}; 1 {code} was worth ${1 / r0:.4f} and is now ${1 / r1_:.4f}, a change of {pc:.1f}%.',
                    markingKey=MK(f'Value of {code} in $: 1/{r0} → 1/{r2(r1_)}; % change = {pc:.1f}%.', f'{pc:.1f}%') + ' [A1] direction (more units per dollar = depreciation).', marks=3)
    p0, p1 = exp_price / r0, exp_price / r1_
    return dict(stem=frame + f' An exporter in {e} sells machines priced at {exp_price:,} {code}. Calculate the dollar price of a machine before and after the change, and explain the likely effect on the volume of {e}\'s exports.',
                answer=f'Before ${p0:,.2f}; after ${p1:,.2f}. The {code} has {"depreciated, so exports are cheaper in dollars and export volumes are likely to rise (depending on PED)" if ch > 0 else "appreciated, so exports are dearer in dollars and export volumes are likely to fall (depending on PED)"}.',
                markingKey=MK(f'{exp_price:,}/{r0} = {p0:,.2f}; {exp_price:,}/{r2(r1_)} = {p1:,.2f}.', 'both prices') + ' [R1][R1] effect on exports linked to price competitiveness and PED.', marks=4 if slot.d == 4 else 6)


@calc('ch12-st1', 'C3', (2, 4))
def cross_rate(rng, slot):
    a, b = rng.sample(CURNAME, 2)
    ca, cb = a.split('(')[1].rstrip(')'), b.split('(')[1].rstrip(')')
    ra, rb = rng.choice([2, 4, 5, 8, 10]), rng.choice([3, 6, 12, 15, 20])
    cross = rb / ra
    return dict(stem=f'The exchange rates are $1 = {ra} {ca} and $1 = {rb} {cb}. Calculate the cross rate between the {a} and the {b} (how many {cb} per 1 {ca}), and the cost in {ca} of a product priced at {rb * 50:,} {cb}.',
                answer=f'1 {ca} = {rb}/{ra} = {r2(cross)} {cb}; cost = {rb * 50:,}/{r2(cross)} = {rb * 50 / cross:,.2f} {ca}',
                markingKey=MK(f'Cross rate = {rb}/{ra} = {r2(cross)}; {rb * 50:,}/{r2(cross)} = {rb * 50 / cross:,.2f}.', 'both values'), marks=3)


S('ch12-st1',
  diag=[('how a freely floating exchange rate is determined', 'Price of currency (in foreign currency) on the y-axis against quantity of currency; demand from foreigners buying exports, FDI and financial assets; supply from residents buying imports and foreign assets; equilibrium exchange rate where D = S.'),
        ('the effect of an increase in foreign demand for a country\'s exports on its exchange rate', 'Demand for the currency shifts right from D1 to D2; the exchange rate rises (appreciates) from e1 to e2 and quantity traded rises.')],
  terms=[('exchange rate', 'the value of one currency expressed in terms of another currency'),
         ('freely floating exchange rate', 'an exchange rate determined only by the demand for and supply of the currency on the foreign exchange market, with no government or central bank intervention'),
         ('appreciation', 'an increase in the value of a currency in a floating exchange rate system'),
         ('depreciation', 'a decrease in the value of a currency in a floating exchange rate system'),
         ('foreign exchange market', 'the market in which currencies are bought and sold')],
  facts=[('Which of the following increases the demand for a country\'s currency?', 'Foreign tourists visiting the country', ['Domestic residents buying imports', 'Domestic firms investing abroad', 'Domestic residents holidaying abroad'], 'Tourists must buy the currency.'),
         ('If the exchange rate changes from £1 = $1.30 to £1 = $1.20, the pound has:', 'depreciated against the dollar', ['appreciated against the dollar', 'been revalued', 'remained unchanged'], 'Each pound buys fewer dollars.'),
         ('If $1 = 150 yen, how many dollars does 30,000 yen buy?', '$200', ['$4,500,000', '$300', '$150'], '30,000 / 150 = 200.'),
         ('The supply of a country\'s currency on the foreign exchange market comes from:', 'residents buying imports and foreign assets', ['foreigners buying the country\'s exports', 'foreign direct investment into the country', 'foreign tourists'], 'Residents sell domestic currency to buy foreign currency.')],
  why=[('Explain why an increase in a country\'s interest rates may lead to an appreciation of its currency.', 'Higher rates increase the return on financial assets in that country, attracting inflows of hot money; demand for the currency rises, shifting D right and raising the exchange rate.'),
       ('Explain why an increase in imports causes a currency to depreciate under a floating system.', 'To pay for imports, residents sell domestic currency to buy foreign currency, increasing the supply of the domestic currency and lowering its price.'),
       ('Explain why a depreciation of one currency is an appreciation of another.', 'An exchange rate is a relative price; if fewer dollars are needed to buy a euro, then more euros are needed to buy a dollar.')],
  contrast=[('appreciation', 'depreciation', 'Appreciation is a rise in a currency\'s value in a floating system (it buys more foreign currency); depreciation is a fall in its value (it buys less).')],
  misc=[('If the exchange rate goes from $1 = 100 yen to $1 = 120 yen, the yen has appreciated.', 'More yen are needed to buy a dollar, so the yen has depreciated (and the dollar appreciated).')],
  cases=[('the fall of the Japanese yen in 2022-2024', 'The yen fell from about ¥115 per dollar in early 2022 to over ¥150 in late 2022 and around ¥160 in mid-2024, as US rates rose while the Bank of Japan kept rates near zero.', 'the determination of floating exchange rates', 'the interest-rate differential reduced demand for yen assets and increased supply of yen, causing depreciation'),
         ('the pound after the Brexit referendum', 'The pound fell from about $1.48 to $1.32 the day after the June 2016 referendum, its largest one-day fall in decades.', 'expectations and exchange rates', 'expected lower future growth and investment reduced demand for sterling assets, causing a sharp depreciation')],
  evaluate=[('A freely floating exchange rate is the best exchange-rate system for a small open economy.', ['automatic adjustment to BoP imbalances', 'independent monetary policy', 'no need for large reserves'],
             ['volatility creates uncertainty for traders', 'speculation can cause overshooting', 'imported inflation after depreciation'], 'A float suits economies with credible institutions and deep financial markets; very small, trade-dependent economies may prefer a managed or fixed rate.')],
  )

S('ch12-st2',
  diag=[('the effect of speculation that a currency will depreciate', 'Supply of the currency shifts right (holders sell) and demand shifts left (fewer buyers); the exchange rate falls, possibly by more than fundamentals justify (overshooting).')],
  terms=[('hot money', 'short-term capital that moves between countries seeking the highest interest rates or speculative gains'),
         ('speculation', 'buying or selling currencies in the expectation of profiting from future changes in exchange rates'),
         ('relative inflation', 'the inflation rate in one country compared with that in its trading partners, which affects the competitiveness of its goods'),
         ('foreign direct investment (FDI)', 'long-term investment by a firm in productive assets in another country, such as building a factory'),
         ('remittances', 'money sent home by migrant workers to their families')],
  facts=[('Higher inflation in a country than in its trading partners will tend to:', 'depreciate its currency', ['appreciate its currency', 'have no effect', 'raise demand for its exports'], 'Exports become less competitive, imports more attractive.'),
         ('A large inflow of FDI into a country will tend to:', 'appreciate its currency', ['depreciate its currency', 'raise its interest rates', 'reduce its exports'], 'Foreign firms buy the currency to invest.'),
         ('If speculators expect a currency to appreciate, they will:', 'buy the currency now, increasing demand and causing appreciation', ['sell the currency now', 'stop trading altogether', 'demand fixed exchange rates'], 'Self-fulfilling expectations.')],
  why=[('Explain why a rise in incomes abroad can lead to an appreciation of a country\'s currency.', 'Foreigners demand more of the country\'s exports, so they need more of its currency to pay, increasing demand and the exchange rate.'),
       ('Explain why speculation can cause large and sudden changes in exchange rates.', 'Expectations of change lead speculators to buy or sell huge sums quickly; their actions shift demand or supply and can make the expected change happen (self-fulfilling), even overshooting.'),
       ('Explain why a fall in the price of a country\'s main commodity export can cause its currency to depreciate.', 'Export revenues fall, so foreign demand for the currency falls, and investors may expect lower growth.')],
  contrast=[('hot money flows', 'foreign direct investment', 'Hot money is short-term financial capital that moves quickly in response to interest rates and expectations; FDI is long-term investment in productive assets, less volatile.')],
  misc=[('A country\'s currency always appreciates when its interest rates rise.', 'Usually, but if the rise is expected or seen as a sign of crisis, or rates rise more elsewhere, the currency may not appreciate.')],
  cases=[('the US dollar in 2022', 'The US dollar index rose by about 15-20% to a 20-year high in September 2022 as the Federal Reserve raised interest rates faster than other central banks.', 'interest rates and exchange rates', 'higher US interest rates attracted capital inflows, increasing demand for dollars'),
         ('George Soros and Black Wednesday', 'On 16 September 1992 speculators, including George Soros, sold sterling heavily, forcing the UK to leave the European Exchange Rate Mechanism; Soros reportedly made about $1 bn.', 'speculation', 'massive selling of pounds increased supply so much that the Bank of England could not defend the rate'),
         ('the Australian dollar and commodity prices', 'The Australian dollar rose above US$1 in 2011 during the mining boom and fell to around US$0.70 by 2015 as iron ore prices collapsed.', 'trade flows as a cause of exchange-rate changes', 'changes in export prices altered demand for the Australian dollar')],
  evaluate=[('Interest rates are the most important determinant of exchange rates.', ['hot money responds quickly to rate differentials', 'examples: dollar in 2022, yen 2022-24', 'central banks use rates to defend currencies'],
             ['trade flows and commodity prices matter (Australia)', 'expectations and confidence (Brexit)', 'relative inflation in the long run (PPP)', 'FDI and political risk'], 'Interest-rate differentials dominate in the short run, but trade, inflation and confidence determine exchange rates over longer periods.')],
  )

S('ch12-st3',
  terms=[('imported inflation', 'inflation caused by rising prices of imported goods and raw materials, often after a depreciation'),
         ('international competitiveness', 'the ability of a country\'s firms to sell goods and services in international markets, influenced by relative prices, quality and exchange rates'),
         ('current account balance', 'the difference between a country\'s export revenues and import expenditure on goods and services, plus net income and net transfers'),
         ('SPICED/WPIDEC', 'mnemonics for the effects of exchange rates: a strong pound (currency) makes imports cheaper and exports dearer')],
  facts=[('A depreciation of a country\'s currency is likely to:', 'make its exports cheaper abroad and imports more expensive at home', ['make its exports more expensive abroad', 'reduce inflation', 'reduce the price of imported raw materials'], 'Change in relative prices.'),
         ('Which group is most likely to benefit from an appreciation of the domestic currency?', 'Domestic consumers buying imported goods', ['Exporters', 'Domestic firms competing with imports', 'The tourism industry'], 'Imports become cheaper.'),
         ('An appreciation of the currency tends to:', 'reduce inflationary pressure', ['increase inflation', 'increase AD', 'improve the current account'], 'Cheaper imports and lower AD.')],
  why=[('Explain why a depreciation can increase inflation.', 'Imported goods, raw materials and energy become more expensive in domestic currency (cost-push), and higher demand for exports raises AD (demand-pull).'),
       ('Explain why a depreciation may increase economic growth and employment.', 'Exports become more competitive and imports dearer, so net exports and AD rise, increasing real GDP and the derived demand for labour, especially in export industries.'),
       ('Explain why an appreciation may harm a country\'s current account.', 'Exports become more expensive to foreign buyers and imports cheaper, so export revenues fall and import spending rises, depending on price elasticities.')],
  contrast=[('the effects of a depreciation on exporters', 'its effects on importers', 'Exporters gain because their goods become cheaper to foreign buyers; importers lose because foreign goods and inputs cost more in domestic currency.')],
  misc=[('A depreciation always improves the current account immediately.', 'In the short run demand is price inelastic, so the current account may worsen first (J-curve); it improves only if the Marshall-Lerner condition holds.')],
  cases=[('the Swiss franc in January 2015', 'When the Swiss National Bank removed its cap of 1.20 francs per euro on 15 January 2015, the franc appreciated by about 20% in a day.', 'consequences of exchange-rate changes', 'Swiss exporters and tourism became less competitive, while consumers paid less for imports and inflation turned negative'),
         ('the Egyptian pound devaluations', 'Egypt\'s pound lost more than half its value in 2016 and again weakened sharply in 2022-2024; inflation exceeded 35% in 2023.', 'imported inflation', 'a weaker currency raised the cost of imported food and fuel, driving inflation'),
         ('UK inflation after 2016', 'After the pound depreciated by about 15-20% following the Brexit vote, UK CPI inflation rose from 0.5% in 2016 to 3.1% in late 2017.', 'the effect of depreciation on inflation', 'higher import prices were passed on to consumers, raising inflation and reducing real wages')],
  evaluate=[('A depreciation of the currency is beneficial for an economy.', ['boosts exports, growth and employment', 'may reduce a current account deficit', 'helps economies in recession'],
             ['imported inflation reduces real incomes', 'higher cost of foreign-currency debt', 'J-curve: short-run worsening', 'lowers incentives for productivity improvement'], 'A depreciation can help an economy with spare capacity and price-elastic trade, but if it causes imported inflation or debt problems it may harm living standards.')],
  )


@calc('ch12-st4', 'C3', (2, 4))
def devaluation(rng, slot):
    e = ec(rng)
    cname = rng.choice(CURNAME)
    code = cname.split('(')[1].rstrip(')')
    r0 = rng.choice([3.75, 5, 7.8, 10, 20, 40, 100])
    dv = rng.choice([10, 15, 20, 25, 30, 50])
    r1_ = r0 / (1 - dv / 100)
    frame = rng.choice([f'{e} pegs the {cname} at $1 = {r0} {code}. The central bank announces a {dv}% devaluation of the {code} against the dollar.',
                        f'The {cname} is fixed at {r0} {code} per US dollar. The government decides to reduce the dollar value of the {code} by {dv}%.'])
    return dict(stem=frame + f' Calculate the new official exchange rate (in {code} per $) and explain one reason why a government might devalue its currency.',
                answer=f'Value of 1 {code}: ${1 / r0:.4f} → ${(1 / r0) * (1 - dv / 100):.4f}; new rate $1 = {r2(r1_)} {code}. Reasons: to improve export competitiveness and the current account, or because reserves are insufficient to defend the peg.',
                markingKey=MK(f'New $ value = (1/{r0}) × {1 - dv / 100:.2f}; rate = {r0}/{1 - dv / 100:.2f} = {r2(r1_)}.', f'{r2(r1_)} {code}/$') + ' [R1] reason.', marks=3)


S('ch12-st4',
  diag=[('how a central bank maintains a fixed exchange rate when there is downward pressure on the currency', 'Currency market: supply rises from S1 to S2, which would lower the rate below the peg; the central bank buys its own currency using foreign reserves (shifting D right) or raises interest rates to keep the rate at the fixed level.')],
  terms=[('fixed exchange rate', 'an exchange rate set and maintained by the government or central bank at a particular level against another currency or basket'),
         ('managed exchange rate (managed float)', 'an exchange rate that floats but with periodic central bank intervention to influence its value'),
         ('devaluation', 'a decrease in the value of a currency in a fixed exchange rate system, decided by the government'),
         ('revaluation', 'an increase in the value of a currency in a fixed exchange rate system, decided by the government'),
         ('foreign exchange reserves', 'holdings of foreign currencies and other assets by the central bank, used to intervene in the currency market'),
         ('currency board', 'an arrangement in which the domestic currency is fully backed by foreign reserves and fixed to an anchor currency')],
  facts=[('Which of the following currencies is pegged to the US dollar?', 'The Hong Kong dollar', ['The euro', 'The Japanese yen', 'The British pound'], 'Hong Kong has a currency board with a band of HK$7.75-7.85 per US$.'),
         ('To prevent its currency from falling below a fixed rate, a central bank can:', 'buy its own currency using foreign exchange reserves', ['sell its own currency', 'cut interest rates', 'print more money'], 'Buying raises demand for the currency.'),
         ('In 2015 the Swiss National Bank abandoned a policy of:', 'capping the franc\'s value at 1.20 per euro', ['pegging the franc to the dollar', 'using the euro', 'negative inflation targeting'], 'It had been selling francs to keep them from appreciating.'),
         ('Saudi Arabia pegs the riyal to the US dollar at about:', '3.75 riyals per dollar', ['1 riyal per dollar', '7.8 riyals per dollar', '100 riyals per dollar'], 'The peg has been held since 1986.')],
  why=[('Explain why a fixed exchange rate can reduce uncertainty for firms involved in international trade.', 'Firms know the future rate at which they will convert export revenues and pay for imports, making costs and revenues predictable and encouraging trade and investment.'),
       ('Explain why maintaining a fixed exchange rate can limit a country\'s monetary policy.', 'Interest rates must be set to defend the peg rather than domestic objectives; raising rates to support the currency may cause recession.'),
       ('Explain why a fixed exchange rate may become unsustainable.', 'If the peg is above the market rate, the central bank must keep selling reserves; when reserves run low or speculators attack, the peg collapses (e.g. UK 1992, Argentina 2002).')],
  contrast=[('devaluation', 'depreciation', 'Devaluation is a deliberate reduction in a fixed exchange rate by the government; depreciation is a fall in a floating exchange rate due to market forces.'),
            ('a fixed exchange rate', 'a managed float', 'A fixed rate is held at a set level by intervention; a managed float is mainly market-determined but the central bank intervenes occasionally to smooth or guide movements.')],
  misc=[('Under a fixed exchange rate, the central bank never needs to intervene.', 'The central bank must constantly buy or sell currency or adjust interest rates to keep the rate at the peg when demand or supply changes.')],
  cases=[('Argentina\'s currency board collapse', 'Argentina pegged the peso 1:1 to the US dollar under a currency board from 1991; in January 2002 it abandoned the peg and the peso lost about 70% of its value within months.', 'unsustainable fixed exchange rates', 'recession, debt and loss of reserves made the peg impossible to defend'),
         ('China\'s managed exchange rate', 'China moved from a dollar peg to a managed float in 2005, allowing the yuan to appreciate by about 30% against the dollar by 2014 while the central bank sets a daily reference rate.', 'managed exchange rate systems', 'the authorities allowed gradual market-driven movement while intervening to limit volatility'),
         ('Argentina\'s devaluation in December 2023', 'In December 2023 Argentina devalued its official exchange rate from about 366 to 800 pesos per dollar.', 'devaluation', 'a large official cut in the currency\'s value aimed to close the gap with parallel market rates and boost exports, but it raised inflation')],
  evaluate=[('A fixed exchange rate system is better than a floating system for a developing economy.', ['stability for trade and FDI', 'anchor for inflation expectations', 'discipline on macro policy'],
             ['requires large reserves', 'loss of independent monetary policy', 'vulnerable to speculative attack', 'misalignment harms competitiveness'], 'A fixed rate can help small, open economies with credible policies, but many developing economies benefit from a managed float that allows adjustment while limiting volatility.')],
  )


# =============================================================================================
# ch13 Balance of payments
# =============================================================================================
@calc('ch13-st1', 'C3', (1, 5))
def bop_calc(rng, slot):
    e = ec(rng)
    xg, mg = rng.randint(80, 400), rng.randint(80, 420)
    xs, ms = rng.randint(20, 150), rng.randint(20, 150)
    pi = rng.randint(-40, 30)
    si = rng.randint(-20, 15)
    tg = xg - mg
    ts = xs - ms
    ca = tg + ts + pi + si
    frame = rng.choice([f'Balance of payments data for {e} ($ bn): exports of goods {xg}; imports of goods {mg}; exports of services {xs}; imports of services {ms}; net primary income {pi}; net secondary income (transfers) {si}.',
                        f'{e}\'s central bank publishes: goods exported ${xg} bn, goods imported ${mg} bn, services exported ${xs} bn, services imported ${ms} bn, net income from abroad ${pi} bn and net current transfers ${si} bn.'])
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the balance of trade in goods and the balance of trade in services.',
                    answer=f'Goods: {xg} − {mg} = {bn(tg)}; services: {xs} − {ms} = {bn(ts)}',
                    markingKey=MK(f'Goods {tg}; services {ts}.', 'both balances'), marks=2)
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the current account balance and state whether it is in deficit or surplus.',
                    answer=f'CA = ({tg}) + ({ts}) + ({pi}) + ({si}) = {bn(ca)}: a {"deficit" if ca < 0 else "surplus"}.',
                    markingKey=MK(f'CA = trade in goods + trade in services + primary income + secondary income = {ca}.', f'{bn(ca)}'), marks=3)
    kab = rng.randint(-5, 5)
    err = rng.randint(-4, 4)
    fa = -(ca + kab + err)
    return dict(stem=frame + f' The capital account balance is {bn(kab)} and net errors and omissions are {bn(err)}. Calculate the current account balance and the financial account balance, and explain why the balance of payments must balance.',
                answer=f'CA = {bn(ca)}; FA = −(CA + KA + errors) = −({ca} + {kab} + {err}) = {bn(fa)}. Every transaction has a matching entry: a current account deficit must be financed by net inflows on the financial (and capital) accounts, so CA + KA + FA + errors = 0.',
                markingKey=MK(f'CA = {ca}; FA = {fa} (sign convention: CA + KA + FA + errors = 0).', 'CA and FA') + ' [R1][R1] double-entry explanation.', marks=4 if slot.d == 4 else 6)


S('ch13-st1',
  terms=[('balance of payments', 'a record of all transactions between the residents of a country and the rest of the world over a period of time'),
         ('current account', 'the part of the balance of payments recording trade in goods and services, primary income (wages, interest, profits, dividends) and secondary income (current transfers)'),
         ('capital account', 'the part of the balance of payments recording capital transfers (such as debt forgiveness) and the purchase or sale of non-produced, non-financial assets'),
         ('financial account', 'the part of the balance of payments recording direct investment, portfolio investment and changes in reserve assets'),
         ('primary income', 'income from factors of production: compensation of employees, interest, profits and dividends received from or paid abroad'),
         ('secondary income', 'current transfers such as workers\' remittances and foreign aid, with nothing given in return')],
  facts=[('In which account is a payment by a Japanese firm to build a factory in Thailand recorded?', 'The financial account (direct investment)', ['The current account', 'The capital account', 'The trade in services balance'], 'FDI is a financial account flow.'),
         ('Remittances sent home by migrant workers are recorded as:', 'secondary income in the current account', ['primary income in the current account', 'portfolio investment', 'the capital account'], 'They are current transfers.'),
         ('A current account deficit must be matched by:', 'a surplus on the capital and financial accounts', ['a deficit on the financial account', 'a budget deficit', 'a fall in the exchange rate'], 'The BoP balances.'),
         ('Interest paid to foreign holders of government bonds is recorded as:', 'a debit in primary income', ['a credit in services', 'secondary income', 'a capital account credit'], 'Investment income paid abroad.')],
  why=[('Explain why the balance of payments always balances.', 'It uses double-entry accounting: each transaction creates both a credit and a debit; a deficit on the current account must be financed by net inflows of capital or by using reserves, so the accounts sum to zero (with errors and omissions).'),
       ('Explain why a country with a current account deficit is a net borrower from the rest of the world.', 'It spends more on foreign goods, services and income than it earns, so it must finance the gap by selling assets or borrowing from abroad (financial account surplus).'),
       ('Explain why an inflow of foreign direct investment can later worsen the current account.', 'Foreign-owned firms repatriate profits and dividends, which are debits in primary income on the current account.')],
  contrast=[('the current account', 'the financial account', 'The current account records trade in goods and services and income flows; the financial account records flows of investment (direct, portfolio) and reserves.'),
            ('primary income', 'secondary income', 'Primary income is a return to factors of production (wages, interest, profits); secondary income is transfers with nothing given in return (remittances, aid).')],
  misc=[('A current account deficit means a country has an overall balance of payments deficit.', 'The BoP as a whole always balances; a current account deficit is matched by surpluses on the capital and financial accounts.')],
  cases=[('remittances to the Philippines', 'Personal remittances to the Philippines were about $39 bn in 2023, around 9% of GDP.', 'the structure of the current account', 'remittances are secondary income credits that offset much of the Philippines\' goods trade deficit'),
         ('the US current account deficit', 'The USA has run a current account deficit every year since 1992, around 3-4% of GDP recently, financed by foreign purchases of US assets.', 'the link between the current and financial accounts', 'the deficit is matched by a financial account surplus, as foreigners buy US bonds, shares and companies')],
  evaluate=[('A current account deficit is always a problem for an economy.', ['implies growing foreign debt', 'may reflect lack of competitiveness', 'vulnerable to sudden stops of capital'],
             ['may reflect high investment that raises future capacity', 'financed by FDI is more sustainable', 'USA has run deficits for decades'], 'A deficit is a problem when it is large, persistent and financed by short-term borrowing for consumption, not when it reflects productive investment financed by FDI.')],
  )

S('ch13-st2',
  terms=[('current account deficit', 'a situation where the value of a country\'s debits on the current account exceeds its credits'),
         ('current account surplus', 'a situation where the value of a country\'s credits on the current account exceeds its debits'),
         ('expenditure-switching policies', 'policies, such as depreciation or protection, that switch spending from imports to domestically produced goods'),
         ('expenditure-reducing policies', 'contractionary fiscal and monetary policies that reduce AD and hence spending on imports'),
         ('sudden stop', 'an abrupt halt in capital inflows that forces a country to reduce its current account deficit rapidly')],
  facts=[('Which of the following is an expenditure-switching policy to reduce a current account deficit?', 'Allowing the currency to depreciate', ['Raising income tax', 'Cutting government spending', 'Raising interest rates'], 'Switches demand from imports to domestic goods.'),
         ('Which country has run one of the world\'s largest current account surpluses in recent years?', 'Germany', ['USA', 'UK', 'Türkiye'], 'Germany\'s surplus has often been 6-8% of GDP.'),
         ('A disadvantage of using contractionary fiscal policy to reduce a current account deficit is that it:', 'reduces growth and increases unemployment', ['increases imports', 'raises inflation', 'appreciates the currency'], 'It works by reducing total spending.')],
  why=[('Explain why a persistent current account deficit may lead to a depreciation of the currency.', 'Imports exceed exports, so supply of the domestic currency on the foreign exchange market exceeds demand from trade; unless offset by capital inflows, the currency falls.'),
       ('Explain why a large current account surplus may be a problem.', 'It implies low domestic consumption and investment relative to saving, may cause currency appreciation and inflation pressure, and contributes to global imbalances and trade tensions.'),
       ('Explain why supply-side policies may be the best long-term way to correct a current account deficit.', 'They raise productivity and quality, improving non-price and price competitiveness of exports without reducing growth.')],
  contrast=[('expenditure-switching policies', 'expenditure-reducing policies', 'Expenditure switching changes the composition of spending away from imports (depreciation, tariffs); expenditure reducing lowers total spending, including on imports (contractionary fiscal or monetary policy).')],
  misc=[('Any current account deficit should be eliminated as quickly as possible.', 'Rapid correction via contractionary policy can cause recession; a modest deficit financed by FDI for productive investment can be sustainable.')],
  cases=[('Germany\'s current account surplus', 'Germany\'s current account surplus peaked at about 8.6% of GDP in 2015, drawing criticism from the IMF, the EU Commission and the US government.', 'consequences of persistent surpluses', 'high saving and weak domestic investment created surpluses that contributed to global imbalances'),
         ('Sri Lanka\'s current account and reserves crisis', 'Sri Lanka\'s large current account deficits and falling tourism after 2019 drained foreign reserves to almost zero by 2022.', 'consequences of current account deficits', 'without capital inflows to finance the deficit, the country could not pay for essential imports and defaulted'),
         ('the Asian financial crisis of 1997', 'Thailand had current account deficits of about 8% of GDP in 1995-96, financed by short-term borrowing; when capital fled in 1997 the baht collapsed.', 'the risks of financing deficits with short-term capital', 'a sudden stop forced a sharp currency depreciation and recession')],
  evaluate=[('Depreciation of the currency is the most effective way to reduce a current account deficit.', ['makes exports cheaper and imports dearer', 'does not directly reduce growth', 'works if Marshall-Lerner holds'],
             ['J-curve: short-run worsening', 'imported inflation', 'competitors may retaliate', 'does not fix non-price competitiveness'], 'Depreciation can help in the short to medium term, but lasting correction requires supply-side improvements in competitiveness.')],
  )


@calc('ch13-st3', 'C3', (2, 5))
def marshall_lerner(rng, slot):
    e = ec(rng)
    px = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.1])
    pm = rng.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9])
    s_ = px + pm
    frame = rng.choice([f'Economists estimate that in {e} the price elasticity of demand for exports is {px} and for imports is {pm}.',
                        f'Research by {e}\'s central bank finds PEDx = {px} and PEDm = {pm} (absolute values).'])
    return dict(stem=frame + ' Using the Marshall-Lerner condition, explain whether a depreciation of the currency would improve the current account.',
                answer=f'PEDx + PEDm = {px} + {pm} = {r2(s_)}. {"This is greater than 1, so the condition is satisfied: a depreciation should improve the current account (after any J-curve delay)." if s_ > 1 else "This is less than 1, so the condition is not satisfied: a depreciation would worsen the current account because demand is too price inelastic."}',
                markingKey=f'[M1] sum of elasticities = {r2(s_)}; [A1] comparison with 1; [R1] explanation of why revenue/spending changes; [R1] J-curve/time caveat.', marks=4)


S('ch13-st3',
  diag=[('the J-curve effect following a depreciation', 'Current account balance (y-axis) against time; depreciation at t0; the balance first worsens because demand is price inelastic in the short run (existing contracts), then improves as elasticities rise, forming a J shape.')],
  terms=[('Marshall-Lerner condition', 'the condition that a depreciation will improve the current account only if the sum of the price elasticities of demand for exports and imports is greater than one'),
         ('J-curve', 'the tendency of the current account to worsen immediately after a depreciation before improving, because demand for exports and imports is price inelastic in the short run'),
         ('price elasticity of demand for exports', 'the responsiveness of the quantity of exports demanded to a change in their price in foreign currency'),
         ('price elasticity of demand for imports', 'the responsiveness of the quantity of imports demanded to a change in their price in domestic currency')],
  facts=[('If PEDx = 0.4 and PEDm = 0.3, a depreciation will:', 'worsen the current account', ['improve the current account', 'have no effect', 'improve it immediately and permanently'], '0.4 + 0.3 = 0.7 < 1.'),
         ('The J-curve occurs because:', 'in the short run demand for exports and imports is price inelastic', ['the currency appreciates after a depreciation', 'exports always fall', 'the Marshall-Lerner condition always holds'], 'Contracts and habits take time to change.'),
         ('The Marshall-Lerner condition is satisfied when:', 'PEDx + PEDm > 1', ['PEDx + PEDm < 1', 'PEDx = PEDm', 'PEDx > PEDm'], 'Then a depreciation raises net export revenue.')],
  why=[('Explain why a depreciation can worsen the current account in the short run.', 'Import volumes do not fall quickly because of contracts and lack of substitutes, so higher import prices raise import spending; export volumes rise only slowly, so the deficit widens before it narrows.'),
       ('Explain why the Marshall-Lerner condition is more likely to be satisfied in the long run.', 'Over time consumers and firms find substitutes and switch suppliers, and exporters expand capacity and marketing, so demand becomes more price elastic.')],
  contrast=[('the Marshall-Lerner condition', 'the J-curve', 'The Marshall-Lerner condition states when a depreciation will improve the current account (PEDx + PEDm > 1); the J-curve describes the time path, with an initial worsening before improvement as elasticities rise.')],
  misc=[('A depreciation always improves the current account because exports become cheaper.', 'If demand is price inelastic (PEDx + PEDm < 1), the fall in export prices and rise in import prices reduce net revenue, worsening the current account.')],
  cases=[('the UK devaluation of 1967', 'After the pound was devalued by 14.3% in November 1967, the UK current account worsened in 1968 before moving into surplus in 1969-1971.', 'the J-curve', 'inelastic short-run demand meant the balance worsened first, then improved as volumes adjusted'),
         ('the US dollar depreciation after 1985', 'After the Plaza Accord in 1985 the dollar fell sharply, but the US trade deficit kept widening until 1987 before narrowing.', 'the J-curve and Marshall-Lerner condition', 'the delayed improvement suggests elasticities were low in the short run and higher later')],
  evaluate=[('A depreciation will always improve a country\'s current account in the long run.', ['elasticities rise over time', 'empirical evidence for many countries', 'J-curve eventually turns up'],
             ['commodity exporters face inelastic world demand', 'imported inflation erodes competitiveness', 'quality and non-price factors matter', 'trading partners may retaliate'], 'In most diversified economies the Marshall-Lerner condition holds in the long run, but the improvement may be small and temporary if inflation erodes the competitive gain.')],
  )


@calc('ch13-st4', 'C3', (1, 5))
def terms_of_trade(rng, slot):
    e = ec(rng)
    xp0, mp0 = 100, 100
    xp1 = rng.choice([85, 90, 95, 104, 110, 120, 130])
    mp1 = rng.choice([96, 100, 105, 108, 115, 125])
    tot1 = 100 * xp1 / mp1
    y0 = rng.randint(2014, 2020)
    frame = rng.choice([f'In {e}, the index of average export prices rose from 100 in {y0} to {xp1} in {y0 + 3}, while the index of average import prices moved from 100 to {mp1}.',
                        f'Trade statistics for {e} (base year {y0} = 100): export price index {xp1}, import price index {mp1} in {y0 + 3}.',
                        f'{e} mainly exports copper and imports manufactured goods. Between {y0} and {y0 + 3} its export price index changed from 100 to {xp1} and its import price index from 100 to {mp1}.'])
    if slot.d <= 2:
        return dict(stem=frame + f' Calculate the terms of trade index for {y0 + 3}.', answer=f'{tot1:.1f}',
                    markingKey=MK(f'ToT = (index of average export prices / index of average import prices) × 100 = {xp1}/{mp1} × 100 = {tot1:.1f}.', f'{tot1:.1f}'), marks=2)
    kind = 'improvement (favourable)' if tot1 > 100 else 'deterioration (unfavourable)'
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the terms of trade index and explain whether this represents an improvement or deterioration.',
                    answer=f'ToT = {tot1:.1f}: a {kind}, since each unit of exports now buys {"more" if tot1 > 100 else "fewer"} imports.',
                    markingKey=MK(f'{xp1}/{mp1} × 100 = {tot1:.1f}.', f'{tot1:.1f}') + ' [R1] interpretation.', marks=3)
    chg = tot1 - 100
    return dict(stem=frame + ' Calculate the terms of trade index and the percentage change since the base year. Explain one possible cause and one consequence of this change for the economy.',
                answer=f'ToT = {tot1:.1f}, a change of {chg:.1f}% ({kind}). {"Cause: rising world demand for commodities; consequence: higher export revenue, possible currency appreciation, current account improvement if demand is inelastic." if tot1 > 100 else "Cause: falling world commodity prices or rising import prices; consequence: lower export revenue, worse current account and lower national income for a commodity exporter."}',
                markingKey=MK(f'{xp1}/{mp1} × 100 = {tot1:.1f}; change = {chg:.1f}%.', f'{tot1:.1f}') + ' [R1] cause; [R1] consequence.', marks=4 if slot.d == 4 else 6)


S('ch13-st4',
  terms=[('terms of trade', 'the ratio of the index of average export prices to the index of average import prices, multiplied by 100'),
         ('improvement in the terms of trade', 'a rise in the terms of trade index, meaning a given quantity of exports buys more imports'),
         ('deterioration in the terms of trade', 'a fall in the terms of trade index, meaning a given quantity of exports buys fewer imports'),
         ('Prebisch-Singer hypothesis', 'the hypothesis that the terms of trade of primary commodity exporters tend to deteriorate over the long run relative to manufactured goods')],
  facts=[('If the export price index is 120 and the import price index is 150, the terms of trade index is:', '80', ['125', '30', '180'], '120/150 × 100 = 80.'),
         ('Which of the following would improve Chile\'s terms of trade?', 'A rise in the world price of copper', ['A fall in the world price of copper', 'A rise in the price of imported oil', 'A depreciation of the peso'], 'Chile is a major copper exporter.'),
         ('An improvement in the terms of trade means:', 'a given volume of exports pays for a larger volume of imports', ['the trade balance must improve', 'export volumes must rise', 'the currency must depreciate'], 'It is a price ratio, not a balance.')],
  why=[('Explain why commodity-exporting developing countries may suffer from a long-term deterioration in their terms of trade.', 'Demand for primary products is income inelastic, so as world incomes grow demand rises slowly; productivity gains and new supply lower commodity prices relative to manufactured goods (Prebisch-Singer).'),
       ('Explain why an improvement in the terms of trade does not necessarily improve the current account.', 'If export prices rise and demand is price elastic, export volumes may fall enough to reduce export revenue; the effect depends on the cause and on elasticities.'),
       ('Explain why short-term volatility of commodity prices can harm developing economies.', 'Export revenue, government tax revenue and incomes swing sharply, making planning, investment and debt service difficult.')],
  contrast=[('the terms of trade', 'the balance of trade', 'The terms of trade is a ratio of export to import prices; the balance of trade is the value of exports minus the value of imports (prices × volumes).')],
  misc=[('A deterioration in the terms of trade always makes a country worse off.', 'If it is caused by productivity gains that lower export prices and raise export volumes, export revenue and income may rise.')],
  cases=[('Australia\'s mining boom', 'Australia\'s terms of trade roughly doubled between 2003 and 2011 as China\'s demand for iron ore and coal soared.', 'causes and consequences of terms of trade changes', 'higher export prices raised national income, government revenue and the Australian dollar'),
         ('Zambia and copper prices', 'Copper accounts for about 70% of Zambia\'s export earnings; when copper prices fell by about half between 2011 and 2016, the kwacha depreciated sharply and growth slowed.', 'terms of trade volatility', 'dependence on one commodity made export revenues and the exchange rate highly sensitive to world prices'),
         ('oil importers in 2022', 'When oil prices rose above $100 a barrel in 2022, oil-importing countries such as India and Pakistan faced a deterioration in their terms of trade.', 'a deterioration in the terms of trade', 'higher import prices meant more exports were needed to pay for the same imports, worsening the current account')],
  evaluate=[('Developing countries should reduce their dependence on primary commodity exports.', ['Prebisch-Singer long-run decline', 'price volatility', 'diversification creates higher-value jobs'],
             ['commodities are a real comparative advantage', 'commodity booms raise incomes (Australia, Botswana)', 'diversification is costly and slow', 'industrial policy can fail'], 'Diversification is desirable over time, but commodity revenues managed well (stabilisation funds, investment in education) can finance it.')],
  )


# =============================================================================================
# ch14 Sustainable development, measuring development, barriers and strategies
# =============================================================================================
@calc('ch14-st1', 'C3', (2, 5))
def hdi_calc(rng, slot):
    e = ec(rng)
    le = rng.choice([55, 60, 64, 68, 72, 76, 80, 83])
    eys, mys = rng.choice([8, 10, 12, 14, 16, 18]), rng.choice([3, 5, 7, 9, 11, 13])
    gni = rng.choice([1200, 2500, 5000, 12000, 25000, 45000])
    hi = (le - 20) / (85 - 20)
    ei = (min(eys, 18) / 18 + min(mys, 15) / 15) / 2
    ii = (math.log(gni) - math.log(100)) / (math.log(75000) - math.log(100))
    hdi = (hi * ei * ii) ** (1 / 3)
    lvl = 'very high' if hdi >= 0.8 else 'high' if hdi >= 0.7 else 'medium' if hdi >= 0.55 else 'low'
    frame = rng.choice([f'{e} has life expectancy at birth of {le} years, expected years of schooling of {eys}, mean years of schooling of {mys} and GNI per capita of ${gni:,} (PPP).',
                        f'UNDP data for {e}: life expectancy {le} years; expected schooling {eys} years; mean schooling {mys} years; GNI per capita (2017 PPP $) {gni:,}.'])
    if slot.d <= 3:
        return dict(stem=frame + ' The health index is (LE − 20)/(85 − 20). Calculate the health index and the education index (the average of expected schooling/18 and mean schooling/15).',
                    answer=f'Health index = ({le} − 20)/65 = {hi:.3f}; education index = ({eys}/18 + {mys}/15)/2 = {ei:.3f}',
                    markingKey=MK(f'HI = {hi:.3f}; EI = {ei:.3f}.', 'both indices'), marks=3)
    return dict(stem=frame + ' Using the UNDP method (health index = (LE − 20)/65; education index = mean of EYS/18 and MYS/15; income index = (ln GNI − ln 100)/(ln 75,000 − ln 100); HDI = geometric mean of the three), calculate the HDI and state the development category.',
                answer=f'HI = {hi:.3f}; EI = {ei:.3f}; II = {ii:.3f}; HDI = ({hi:.3f} × {ei:.3f} × {ii:.3f})^(1/3) = {hdi:.3f}: {lvl} human development.',
                markingKey=MK(f'Indices {hi:.3f}, {ei:.3f}, {ii:.3f}; geometric mean {hdi:.3f}.', f'HDI ≈ {hdi:.3f} ({lvl})') + ' Categories: ≥0.800 very high; 0.700–0.799 high; 0.550–0.699 medium; <0.550 low.', marks=4 if slot.d == 4 else 6)


S('ch14-st1',
  terms=[('sustainable development', 'development that meets the needs of the present without compromising the ability of future generations to meet their own needs (Brundtland Report, 1987)'),
         ('Sustainable Development Goals (SDGs)', 'the 17 goals adopted by all UN member states in 2015 for achievement by 2030, including ending poverty, zero hunger, quality education, gender equality and climate action'),
         ('Human Development Index (HDI)', 'a UNDP composite index of a long and healthy life (life expectancy), knowledge (expected and mean years of schooling) and a decent standard of living (GNI per capita at PPP)'),
         ('Inequality-adjusted HDI (IHDI)', 'the HDI adjusted for inequality in the distribution of each dimension across the population'),
         ('Gender Inequality Index (GII)', 'a UNDP index measuring gender inequality in reproductive health, empowerment and labour market participation'),
         ('economic development', 'a broad, multidimensional improvement in living standards, including reductions in poverty and inequality and improvements in health, education, freedom and choice')],
  facts=[('How many Sustainable Development Goals were adopted in 2015?', '17', ['8', '10', '25'], 'The SDGs replaced the 8 Millennium Development Goals.'),
         ('Which three dimensions does the HDI measure?', 'Health, education and standard of living', ['Income, wealth and inequality', 'Growth, inflation and unemployment', 'Gender, environment and governance'], 'Life expectancy, schooling and GNI per capita (PPP).'),
         ('Why does the IHDI usually have a lower value than the HDI?', 'It adjusts each dimension for inequality across the population', ['It excludes education', 'It uses nominal GNI', 'It includes only urban areas'], 'Loss due to inequality.'),
         ('Which country ranked top of the UNDP Human Development Index in the 2023-24 report?', 'Switzerland', ['USA', 'Singapore', 'Japan'], 'Switzerland, Norway and Iceland ranked highest.')],
  why=[('Explain why the HDI may be a better indicator of development than GNI per capita alone.', 'Development is multidimensional; the HDI includes health and education outcomes as well as income, so it captures whether income is translated into longer, better-educated lives.'),
       ('Explain why two countries with similar GNI per capita may have very different HDI values.', 'They may spend different amounts and with different effectiveness on health and education, or have different income distributions, so life expectancy and schooling differ.'),
       ('Explain why sustainable development requires maintaining natural capital.', 'Depleting forests, fisheries, soils and the climate reduces future productive capacity and well-being, so present growth may be at the expense of future generations.')],
  contrast=[('the HDI', 'the IHDI', 'The HDI averages achievements in health, education and income; the IHDI discounts each dimension for inequality, showing the loss in human development due to unequal distribution.'),
            ('single indicators of development', 'composite indicators', 'Single indicators measure one aspect (e.g. GNI per capita, life expectancy); composite indicators such as the HDI combine several dimensions into one index.')],
  misc=[('A country with a high HDI must have low inequality.', 'The HDI uses national averages; the IHDI shows that high-HDI countries such as the USA lose a significant share of their HDI to inequality.')],
  cases=[('the Gulf states and the HDI', 'Qatar\'s GNI per capita ranks among the highest in the world, but its HDI rank is noticeably lower than its GNI rank.', 'composite indicators of development', 'very high income has not been matched by equally high education outcomes, so the HDI gives a broader picture than income alone'),
         ('Cuba and Costa Rica', 'Cuba and Costa Rica have life expectancies close to those of the USA despite much lower GNI per capita.', 'the difference between growth and development', 'investment in primary health care and education achieved high human development at modest income levels'),
         ('progress on the SDGs', 'The UN\'s 2024 SDG report found that only about 17% of SDG targets were on track for 2030.', 'sustainable development goals', 'Covid-19, conflict and climate shocks have slowed progress, showing that development can be reversed')],
  evaluate=[('The HDI is the most useful measure of development.', ['multidimensional', 'widely available and comparable', 'simple to interpret'],
             ['ignores inequality (hence IHDI), gender (GII), environment', 'equal weights are arbitrary', 'ignores freedom, security and quality of education', 'data quality problems'], 'The HDI is more useful than GNI per capita alone, but development should be assessed using a range of indicators, including the IHDI, MPI and GII.')],
  )

S('ch14-st2',
  terms=[('poverty cycle (trap)', 'a situation where low incomes lead to low saving and investment in physical and human capital, keeping productivity and incomes low'),
         ('corruption', 'the abuse of public office for private gain, such as bribery, which diverts resources and discourages investment'),
         ('informal economy', 'economic activities that are not registered, regulated or taxed by the government'),
         ('capital flight', 'the transfer of large amounts of money out of a country by residents, often in response to political or economic instability'),
         ('debt overhang', 'a situation where a country\'s foreign debt is so large that debt service absorbs resources needed for investment and development'),
         ('gender inequality as a barrier to development', 'the unequal treatment of women in education, employment, property rights and political power, which reduces the productive potential of the economy')],
  facts=[('Which of the following is an example of a poverty trap?', 'Low income → low saving → low investment → low productivity → low income', ['High saving → high investment → high growth', 'Low inflation → high investment', 'Free trade → specialisation'], 'A self-reinforcing cycle.'),
         ('Why can a lack of formal property rights be a barrier to development?', 'People cannot use their land or homes as collateral to borrow', ['It raises tax revenue', 'It encourages foreign investment', 'It reduces corruption'], 'Hernando de Soto\'s argument on dead capital.'),
         ('Which of the following is a barrier related to international trade?', 'Over-dependence on primary commodity exports', ['Diversified manufacturing exports', 'Low tariffs in rich-country markets', 'Stable commodity prices'], 'Volatile and declining terms of trade.'),
         ('Transparency International\'s Corruption Perceptions Index ranks which country among the least corrupt?', 'Denmark', ['Somalia', 'Venezuela', 'South Sudan'], 'Denmark has topped the CPI for several years.')],
  why=[('Explain why poor infrastructure is a barrier to economic development.', 'Unreliable electricity, poor roads and limited internet raise costs, reduce productivity, limit access to markets and deter FDI.'),
       ('Explain why corruption can reduce economic growth.', 'Bribes raise the cost of doing business, public funds are diverted from health, education and infrastructure, and uncertainty deters domestic and foreign investment.'),
       ('Explain why gender inequality acts as a barrier to development.', 'Excluding women from education, finance and work wastes human capital and reduces output; educated women have healthier, better-educated children, so inequality also slows future development.'),
       ('Explain why high levels of foreign debt can be a barrier to development.', 'Large debt-service payments use scarce foreign exchange and government revenue that could fund health, education and infrastructure.')],
  contrast=[('economic barriers to development', 'political and social barriers', 'Economic barriers include poverty traps, poor infrastructure, low human capital, debt and commodity dependence; political and social barriers include corruption, weak institutions, conflict, gender inequality and lack of property rights.')],
  misc=[('Poor countries are poor mainly because their people do not work hard enough.', 'People in low-income countries often work long hours; low productivity reflects lack of capital, infrastructure, technology, institutions and access to markets.')],
  cases=[('electricity access in sub-Saharan Africa', 'The IEA estimates that about 600 million people in sub-Saharan Africa lacked access to electricity in 2022.', 'infrastructure as a barrier to development', 'without reliable power, firms cannot use modern machinery and children study less, limiting productivity and human capital'),
         ('the Democratic Republic of the Congo', 'The DRC has vast mineral wealth (including about 70% of world cobalt output), yet over 60% of its population lives in extreme poverty.', 'the resource curse and weak institutions', 'conflict, corruption and weak governance prevent resource revenues from funding development'),
         ('Zambia\'s debt default in 2020', 'Zambia became the first African country to default during the pandemic in November 2020 and took until 2024 to agree a debt restructuring.', 'debt as a barrier to development', 'heavy debt service and the default crowded out spending on development')],
  evaluate=[('Corruption is the most significant barrier to economic development.', ['diverts public resources', 'deters investment', 'undermines trust and institutions'],
             ['some fast-growing economies had corruption (e.g. China)', 'geography, disease, conflict and debt also matter', 'poverty traps and lack of infrastructure are fundamental'], 'Corruption is a major barrier, but the most significant barrier varies by country; often several barriers reinforce each other.')],
  )

S('ch14-st3',
  terms=[('foreign direct investment (FDI)', 'long-term investment by multinational corporations in productive assets in another country'),
         ('official development assistance (ODA)', 'aid given by governments of high-income countries to low- and middle-income countries on concessional terms'),
         ('microfinance', 'the provision of small loans, savings and insurance services to people on low incomes who lack access to formal banking'),
         ('export-led growth', 'a growth strategy based on producing goods for export, often in manufacturing, to exploit comparative advantage and larger markets'),
         ('import substitution', 'a strategy of protecting domestic industries with tariffs and quotas so that they replace imported goods'),
         ('good governance', 'transparent, accountable and effective government, with the rule of law, low corruption and protection of property rights')],
  facts=[('Who founded the Grameen Bank in Bangladesh and won the Nobel Peace Prize in 2006?', 'Muhammad Yunus', ['Amartya Sen', 'Joseph Stiglitz', 'Kofi Annan'], 'Grameen pioneered microcredit to poor women.'),
         ('Which strategy did South Korea and Taiwan mainly follow from the 1960s?', 'Export-led growth', ['Import substitution only', 'Closing their economies to trade', 'Collectivised agriculture'], 'Export promotion of manufactures.'),
         ('M-Pesa, launched in Kenya in 2007, is an example of:', 'mobile money increasing financial inclusion', ['a tariff on imports', 'foreign aid', 'a sovereign wealth fund'], 'It allows money transfers by mobile phone.'),
         ('The UN target for official development assistance from high-income countries is:', '0.7% of GNI', ['7% of GNI', '0.07% of GNI', '2% of GDP'], 'Few donors meet it (e.g. Norway, Sweden, Luxembourg).')],
  why=[('Explain how FDI can contribute to economic development.', 'MNCs bring capital, technology and management skills, create jobs, train workers, raise tax revenue and export earnings, and may generate linkages with local suppliers.'),
       ('Explain why microfinance may help reduce poverty.', 'Poor people without collateral can borrow small amounts to start or expand businesses, raising incomes; group lending and women\'s access to credit improve repayment and household welfare.'),
       ('Explain why aid may fail to promote development.', 'It may be tied to donor goods, diverted by corruption, create dependency, crowd out local producers or fund projects that do not match local needs.'),
       ('Explain why good governance is considered essential for development.', 'It protects property rights and contracts, reduces corruption, ensures public spending reaches health, education and infrastructure, and encourages investment.')],
  contrast=[('export-led growth', 'import substitution', 'Export-led growth opens the economy and promotes industries that compete in world markets; import substitution protects domestic industries to replace imports, which often leads to inefficiency.'),
            ('humanitarian aid', 'development aid', 'Humanitarian aid provides short-term relief in emergencies (food, shelter, medicine); development aid finances long-term projects in health, education and infrastructure.')],
  misc=[('Microfinance has been proven to lift most borrowers out of poverty.', 'Randomised trials (e.g. Banerjee, Duflo et al., 2015) found modest effects on business activity and no transformative effect on average incomes; it is helpful but not a cure.'),
        ('FDI always benefits the host country.', 'MNCs may repatriate profits, use transfer pricing to avoid tax, create few local linkages, exploit lax labour or environmental standards, or crowd out local firms.')],
  cases=[('China\'s special economic zones', 'Shenzhen became China\'s first special economic zone in 1980; it grew from a town of about 30,000 people to a city of over 17 million.', 'export-led growth and FDI', 'tax incentives and openness attracted FDI and export manufacturing, transforming the economy'),
         ('Botswana\'s diamond revenues', 'Botswana used diamond revenues, managed through a joint venture with De Beers and prudent fiscal rules, to fund education, health and infrastructure, becoming an upper-middle-income country.', 'good governance as a development strategy', 'strong institutions turned resource wealth into development, avoiding the resource curse'),
         ('M-Pesa in Kenya', 'A 2016 study by Suri and Jack estimated that access to M-Pesa lifted about 2% of Kenyan households out of extreme poverty.', 'financial inclusion as a development strategy', 'mobile money lowered the cost of transfers and saving, helping households manage risk and move into business')],
  evaluate=[('Foreign direct investment is the most effective strategy for promoting economic development.', ['capital, technology and skills transfer', 'jobs and export earnings', 'tax revenue'],
             ['profit repatriation and tax avoidance', 'enclave production with few linkages', 'environmental and labour exploitation', 'requires good infrastructure and institutions first'], 'FDI can be powerful (China, Vietnam, Ireland) but its benefits depend on absorptive capacity, linkages and governance; it works best as part of a broader strategy.'),
            ('Foreign aid does more harm than good for developing countries.', ['dependency and corruption (Moyo\'s "Dead Aid")', 'tied aid benefits donors', 'may reduce incentives for reform'],
             ['aid-funded vaccination and health programmes save millions of lives', 'humanitarian aid in emergencies', 'well-targeted aid to good governments raises growth'], 'Badly designed aid can harm, but targeted, untied aid for health, education and infrastructure has clear benefits.')],
  )

S('ch14-st4',
  terms=[('IA commentary', 'an IB internal assessment piece of up to 800 words that applies economic theory to a recent news article, using a key concept as a lens'),
         ('key concept (IB Economics)', 'one of the nine concepts — scarcity, choice, efficiency, equity, economic well-being, sustainability, change, interdependence and intervention — used to frame IA commentaries'),
         ('commentary criteria', 'the IB IA criteria: diagrams, terminology, application and analysis, key concept, evaluation, plus portfolio rubric requirements'),
         ('primary source article', 'a news article published no more than one year before the commentary is written, used as the basis for an IA commentary')],
  facts=[('How many commentaries are in the IB Economics IA portfolio?', 'Three', ['Two', 'Four', 'Five'], 'Each based on a different unit (excluding Unit 1) and a different key concept.'),
         ('What is the maximum word count for each IA commentary?', '800 words', ['1,500 words', '400 words', '2,000 words'], 'Words in diagrams, labels and the cover sheet are not counted.'),
         ('Which of the following is one of the nine IB Economics key concepts?', 'Interdependence', ['Globalisation', 'Innovation', 'Strategy'], 'The nine concepts are scarcity, choice, efficiency, equity, economic well-being, sustainability, change, interdependence and intervention.'),
         ('How recent must the article used for an IA commentary be?', 'Published no more than one year before the commentary is written', ['Up to five years old', 'Any date', 'Published in the last week'], 'IB requirement for currency.')],
  why=[('Explain why using the key concept of interdependence can strengthen an IA commentary on an exchange-rate article.', 'It links the article to how economies are connected through trade and capital flows, so the analysis explains spillovers (e.g. a depreciation affecting trading partners), giving the commentary a coherent focus.'),
       ('Explain why a relevant diagram must be explained, not only drawn, in an IA commentary.', 'Marks for diagrams require that the diagram is accurate, labelled and explicitly linked to the article\'s situation; an unexplained diagram does not demonstrate application.'),
       ('Explain why evaluation in a macroeconomic commentary should consider short-run and long-run effects.', 'Policies such as interest-rate rises or supply-side reforms have different impacts over time (time lags, J-curves), so weighing them shows balanced judgement.')],
  contrast=[('application in a commentary', 'evaluation in a commentary', 'Application links theory and diagrams to the specific facts of the article; evaluation weighs consequences, stakeholders, assumptions and priorities to reach a supported judgement.')],
  misc=[('A good IA commentary should summarise the whole article in detail.', 'Description earns few marks; the commentary should select the relevant issue, apply theory and diagrams, and evaluate, quoting the article only as evidence.')],
  cases=[('a news article on a central bank raising interest rates', 'A 2025 article reports a central bank raising rates by 0.5 percentage points as inflation reaches 6%.', 'how to structure an IA commentary on monetary policy', 'a commentary would define terms, draw an AD/AS diagram showing AD shifting left, use the key concept of choice or intervention, and evaluate effects on growth, unemployment and borrowers'),
         ('a news article on new tariffs on steel imports', 'An article describes a government imposing a 25% tariff on steel imports to protect domestic producers.', 'how to apply the key concept of intervention in an IA', 'the commentary would use a tariff diagram to identify welfare effects and evaluate impacts on consumers, steel users, producers and trading partners')],
  evaluate=[('An IA commentary is most effective when it focuses on one economic issue analysed in depth.', ['allows full use of diagrams and theory', 'clear link to one key concept', 'room for balanced evaluation within 800 words'],
             ['some articles involve linked issues', 'narrow focus may miss important stakeholders', 'examiners reward breadth of terminology'], 'A focused commentary is usually stronger; linked issues should be mentioned only where they support the main analysis.')],
  )


# =============================================================================================
# extra content for cells with less variety
# =============================================================================================
def more(key, **kw):
    f = R.f[key]
    if 'cases' in kw:
        kw['cases'] = [(c, w, k, cap(h)) for c, w, k, h in kw['cases']]
    for k, v in kw.items():
        getattr(f, k).extend(v)


more('ch04-st3',
     cases=[('long-term unemployment in Greece', 'In 2014 about 70% of Greece\'s unemployed had been out of work for over a year, and youth unemployment exceeded 50%.', 'the costs of long-term unemployment', 'long spells eroded skills and attachment to the labour market, raising the risk of hysteresis and permanent loss of potential output')],
     apply=[('A town loses 3,000 jobs when its car plant closes. Identify two costs to the local community and two costs to the government, and explain how hysteresis could make the problem persist.', 'Community: lower spending in local shops (negative multiplier), rising crime/poorer health. Government: lower tax revenue, higher benefit spending. Hysteresis: workers lose skills and motivation, employers see them as less employable, so unemployment stays high even after recovery.', 4),
            ('Unemployment in an economy is 7%, of which 2% is frictional, 2.5% structural and 0.5% seasonal. Calculate the natural rate of unemployment and the cyclical unemployment rate, and state the type of output gap.', 'NRU = 2 + 2.5 + 0.5 = 5%; cyclical = 7 − 5 = 2%; a negative (deflationary) output gap.', 3)])
more('ch05-st4',
     cases=[('the Bank of England\'s dilemma in 2022-2023', 'In 2022-23 the Bank of England raised Bank Rate from 0.1% to 5.25% while the UK economy was close to recession.', 'conflicts between macroeconomic objectives', 'tightening to cut inflation from 11.1% risked higher unemployment and slower growth')],
     apply=[('An economy has inflation of 6% and unemployment of 3.5%, below its estimated natural rate of 4.5%. Identify which macroeconomic objective is not being met and explain one policy conflict the central bank faces.', 'Low and stable inflation is not being met (6% above a typical 2% target). Raising interest rates would reduce inflation but lower AD, raising unemployment towards (or above) the NRU and slowing growth.', 3),
            ('A government wants faster growth and a smaller current account deficit. Explain why expansionary fiscal policy might make one objective harder to achieve, and suggest a policy that could help both.', 'Higher AD raises incomes and import spending, worsening the current account. Supply-side policies that raise productivity and export competitiveness can support growth and improve the current account.', 4)])
more('ch08-st2',
     why=[('Explain why a government might use contractionary fiscal policy even though it may increase unemployment.', 'To reduce an inflationary gap or excessive deficits and debt: lower AD reduces inflationary pressure and borrowing, but output and employment fall in the short run.')],
     misc=[('A tax cut and an equal increase in government spending always have the same effect on AD.', 'Part of a tax cut is saved or spent on imports, so the first-round injection is smaller; an equal rise in G usually has a larger multiplier effect.')])
more('ch08-st3',
     cases=[('crowding out debates in the USA after 2023', 'With US federal deficits around 6% of GDP in 2023-24, ten-year Treasury yields rose above 4.5%, prompting warnings of crowding out of private investment.', 'crowding out', 'large borrowing near full employment competes for loanable funds, raising interest rates and reducing private investment')],
     apply=[('A government increases spending by $20 bn when the economy is close to full employment, financed by borrowing. Explain two ways in which its effect on real GDP may be smaller than expected.', 'Crowding out: higher borrowing raises interest rates and reduces private investment and consumption. Near full employment the AS curve is steep, so much of the AD increase raises the price level rather than output; time lags may also delay the effect.', 4)])
more('ch09-st3',
     why=[('Explain why supply-side policies may not reduce cyclical unemployment.', 'Cyclical unemployment is caused by insufficient AD; raising productive capacity does not create demand for the extra output, so firms will not hire more workers.')],
     misc=[('Supply-side policies always reduce inflation immediately.', 'They shift LRAS only after long time lags, and many (infrastructure spending, tax cuts) raise AD first, which can increase inflation in the short run.')],
     cases=[('India\'s Goods and Services Tax (2017)', 'India replaced a complex set of state and central indirect taxes with a single GST in 2017, creating a national market but causing disruption to small firms in its first year.', 'the time lags and trade-offs of supply-side reforms', 'long-run efficiency gains came with short-run costs and compliance problems for small businesses')],
     apply=[('A government must choose between cutting the top rate of income tax and spending the same amount on vocational training. Compare the likely effects of each on LRAS, the time lag and equity.', 'Tax cut: quicker incentive effects, uncertain impact on work effort, benefits high earners (less equitable). Training: longer lag, raises human capital and LRAS, reduces structural unemployment, more equitable.', 6)])
more('ch10-st2',
     cases=[('the WTO Trade Facilitation Agreement', 'The WTO Trade Facilitation Agreement entered into force in 2017 to simplify customs procedures; the WTO estimated it could cut trade costs by about 14% on average.', 'the case for free trade', 'reducing administrative barriers lowers trade costs, especially for developing countries')],
     apply=[('A small country removes a 20% tariff on imported clothing after joining the WTO. Identify two groups that gain and one group that loses, explaining each.', 'Gainers: consumers (lower prices, more choice); firms using imported inputs; exporters (lower costs, possible reciprocal access). Losers: domestic clothing producers and their workers, who face more competition.', 3)])
more('ch11-st1',
     apply=[('Countries A, B and C form a free trade area. A has a 5% tariff on imported steel from outside, B has a 25% tariff. Explain why the FTA needs rules of origin, and why a customs union would not.', 'Without rules of origin, outside steel would enter via A (5%) and move tariff-free to B (trade deflection). A customs union has a common external tariff, so the entry point does not matter.', 3)],
     cases=[('the Regional Comprehensive Economic Partnership (RCEP)', 'RCEP entered into force in 2022 among 15 Asia-Pacific economies, including China, Japan, South Korea, Australia and the ASEAN members, covering about 30% of world GDP.', 'forms of economic integration', 'as a free trade agreement it lowers tariffs among members while each keeps its own external tariffs')])
more('ch11-st2',
     why=[('Explain why the eurozone has fiscal rules such as the Stability and Growth Pact.', 'With a single currency, one member\'s excessive borrowing can raise interest rates or threaten financial stability for all, so rules limit deficits (3% of GDP) and debt (60%).'),
          ('Explain why a single currency increases price transparency.', 'Prices of goods in different member countries are quoted in the same currency, so consumers and firms can compare them easily, increasing competition.')],
     misc=[('Joining a monetary union guarantees that inflation will be the same in every member country.', 'There is one policy rate, but inflation differs because of different growth, wage settlements, energy mixes and tax changes (e.g. 2022: France about 6% vs Estonia over 20%).')],
     cases=[('the ECB\'s "whatever it takes" speech', 'In July 2012 ECB President Mario Draghi pledged to do "whatever it takes" to preserve the euro, and bond yields in Spain and Italy fell sharply.', 'the role of the single central bank in a monetary union', 'a credible commitment to act as backstop reduced fears of break-up and lowered borrowing costs for weaker members')])
more('ch11-st3',
     why=[('Explain why a lower common external tariff reduces the likelihood of trade diversion.', 'With a lower tariff the price of imports from efficient outsiders is closer to their true cost, so higher-cost partners are less able to undercut them.')],
     misc=[('Trade diversion is good for the importing country because it pays a lower price than before.', 'Consumers may pay slightly less, but the government loses tariff revenue and resources are used less efficiently, so national welfare can fall.')])
more('ch12-st1',
     why=[('Explain why an increase in inward foreign direct investment causes a currency to appreciate.', 'Foreign firms must buy the domestic currency to build factories or buy firms, increasing demand for the currency and raising its price.')],
     misc=[('A strong currency is always good for an economy.', 'A strong currency lowers import prices and inflation but makes exports less competitive, which can reduce growth and employment in export industries.')])
more('ch14-st4',
     apply=[('You choose an article about a government subsidising electric-vehicle production. Identify an appropriate diagram, key concept and two points of evaluation for your IA commentary.', 'Diagram: subsidy in a market (S shifts right; lower price; higher quantity) or positive externality diagram. Key concept: sustainability or intervention. Evaluation: cost to taxpayers/opportunity cost; effectiveness depends on PED; stakeholder effects (consumers, producers, foreign firms); short vs long run.', 4)],
     cases=[('a news article on rising youth unemployment', 'A 2025 article reports that youth unemployment in a country has risen to 18% while the overall rate is 6%.', 'how to apply the key concept of equity in an IA commentary', 'the commentary would distinguish types of unemployment, use an AD/AS or labour market diagram, and evaluate policies such as training subsidies for fairness and effectiveness')])
