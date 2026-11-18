"""CBSE class 12 Economics: numerical and data families for Introductory Macroeconomics (answers computed in code).

FAMILIES maps subtopic id -> extra qbank families, added to the fact-table families of g12_economics_a.py.
"""
from __future__ import annotations

from fractions import Fraction

from qbank import F, mcq, inr, num, name, CITIES

S = 'cbse-g12-economics-ch'
Q3 = dict(marks=3, minutes=5)
Q4 = dict(marks=4, minutes=6)
CASE = dict(marks=4, minutes=7, kinds=('case',), gap='G7')
R = ['i', 'ii', 'iii', 'iv']


def cr(x):
    """Rupee crore amount with Indian grouping and the true minus sign."""
    return f'{inr(x)} crore'


def pct(x, dp=2):
    return f'{num(round(float(x), dp), dp)}%'


def wrongs(ans, cands, fmt=cr):
    out, seen = [], {fmt(ans)}
    for c in cands:
        s = fmt(c)
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def m4(r, stem, ans, cands, key, fmt=cr):
    w = wrongs(ans, list(cands) + [ans + 10, ans - 10, ans * 2, ans + 25], fmt)
    return mcq(stem, fmt(ans), w[:3], key, r)


def lines(rows):
    return '\n'.join(f'{k}: {v}' for k, v in rows)


def sub(parts):
    return '\n'.join(f'({R[i]}) {p}' for i, p in enumerate(parts))


def firm(r):
    return r.choice(['a bakery', 'a textile mill', 'a tyre factory', 'a furniture unit', 'a rice mill', 'a printing press',
                     'a dairy plant', 'a cycle factory', 'a shoe factory', 'a paper mill', 'a cement plant', 'a toy factory'])


# ---------------------------------------------------------------- ch02 national income

STOCKS = ['wealth of a household', 'capital stock of a firm', 'money supply on 31 March', 'foreign exchange reserves on a given date',
          'population of a country on 1 March', 'stock of rice in a godown on 1 April', 'balance in a savings account on a date',
          'number of machines in a factory', 'inventory held on 31 December', 'public debt outstanding on 31 March']
FLOWS = ['national income', 'investment', 'depreciation', 'exports during a year', 'consumption expenditure', 'interest paid on a loan in a year',
         'change in the capital stock', 'monthly salary', 'production of wheat in a year', 'rent received per month', 'imports during a quarter',
         'saving during a year', 'change in inventories during a year', 'tax revenue in a year']


def stock_flow(r):
    want = r.choice(['stock', 'flow'])
    good = r.choice(STOCKS if want == 'stock' else FLOWS)
    bad = r.sample(FLOWS if want == 'stock' else STOCKS, 3)
    o = mcq(f'Which of the following is a {want} variable?', good[0].upper() + good[1:], [b[0].upper() + b[1:] for b in bad], '', r)
    o['key'] = f'{good[0].upper() + good[1:]} is a {want} as it is measured ' + ('at a point of time.' if want == 'stock' else 'over a period of time.') + \
        f' The others are {"flows" if want == "stock" else "stocks"}.'
    return o


GOODS = [('Flour bought by a bakery', 'intermediate'), ('Bread bought by a household', 'final'), ('A machine bought by a factory', 'final'),
         ('Cotton yarn bought by a weaving mill', 'intermediate'), ('A car bought by a family', 'final'), ('Steel bought by a car maker', 'intermediate'),
         ('Electricity used by a factory', 'intermediate'), ('Electricity used at home', 'final'), ('Milk bought by a sweet shop', 'intermediate'),
         ('Milk bought by a family for consumption', 'final'), ('A computer bought by a school for its office', 'final'),
         ('Paper bought by a printing press', 'intermediate'), ('Seeds bought by a farmer for sowing', 'intermediate'),
         ('A tractor bought by a farmer', 'final'), ('Fuel used by a transport company', 'intermediate'), ('Furniture bought by a household', 'final'),
         ('Tyres bought by a scooter manufacturer', 'intermediate'), ('A mobile phone bought by a student', 'final'),
         ('Leather bought by a shoe factory', 'intermediate'), ('Uniforms bought by the government for the police', 'final')]


def fin_int(r):
    want = r.choice(['final', 'intermediate'])
    good = r.choice([g for g, c in GOODS if c == want])
    bad = r.sample([g for g, c in GOODS if c != want], 3)
    stem = f'Which of the following is an example of {"a final" if want == "final" else "an intermediate"} good?'
    o = mcq(stem, good, bad, '', r)
    o['key'] = f'{good}: {want} good by its end use. The others are {"intermediate" if want == "final" else "final"} goods.'
    return o


def net_inv(r):
    g = r.randrange(400, 3000, 20)
    d = r.randrange(40, g // 3, 10)
    if r.random() < 0.5:
        return m4(r, f'Gross investment in an economy is {cr(g)} and depreciation is {cr(d)}. Net investment is:', g - d, [g + d, d, g],
                  f'Net investment = gross investment − depreciation = {g} − {d} = {cr(g - d)}.')
    n = g - d
    return m4(r, f'Net investment in an economy is {cr(n)} and depreciation is {cr(d)}. Gross investment is:', g, [n - d, n, d],
              f'Gross investment = net investment + depreciation = {n} + {d} = {cr(g)}.')


def va_firm(r):
    sales = r.randrange(800, 5000, 20)
    ds = r.choice([1, -1]) * r.randrange(20, 200, 10)
    ic = r.randrange(sales // 4, sales // 2, 10)
    dep = r.randrange(20, 150, 5)
    nit = r.randrange(10, 120, 5)
    gva_mp = sales + ds - ic
    nva_fc = gva_mp - dep - nit
    f = firm(r)
    rows = [('Sales', cr(sales)), ('Change in stock', cr(ds)), ('Intermediate consumption', cr(ic)), ('Depreciation', cr(dep)),
            ('Net indirect taxes', cr(nit))]
    r.shuffle(rows)
    stem = f'From the following data about {f}, calculate net value added at factor cost (NVAFC):\n{lines(rows)}'
    ans = f'NVAFC = {cr(nva_fc)}'
    key = (f'Value of output = sales + change in stock = {sales} + ({ds}) = {sales + ds}; GVAMP = {sales + ds} − {ic} = {gva_mp}; '
           f'NVAFC = GVAMP − depreciation − NIT = {gva_mp} − {dep} − {nit} = {cr(nva_fc)}. (1 mark value of output, 1 mark GVAMP, 1 mark NVAFC.)')
    return {'stem': stem, 'answer': ans, 'key': key, 'distractors': [cr(gva_mp), cr(nva_fc + nit), cr(sales - ic - dep - nit)]}


def _ni_data(r):
    pfce = r.randrange(2000, 9000, 50)
    gfce = r.randrange(400, 2000, 25)
    gdcf = r.randrange(500, 3000, 25)
    nx = r.choice([1, -1]) * r.randrange(20, 300, 5)
    dep = r.randrange(100, 600, 10)
    nfia = r.choice([1, -1]) * r.randrange(10, 150, 5)
    nit = r.randrange(100, 700, 10)
    return pfce, gfce, gdcf, nx, dep, nfia, nit


def ni_exp(r):
    pfce, gfce, gdcf, nx, dep, nfia, nit = _ni_data(r)
    gdp = pfce + gfce + gdcf + nx
    nnpfc = gdp - dep + nfia - nit
    rows = [('Private final consumption expenditure', cr(pfce)), ('Government final consumption expenditure', cr(gfce)),
            ('Gross domestic capital formation', cr(gdcf)), ('Net exports', cr(nx)), ('Consumption of fixed capital', cr(dep)),
            ('Net factor income from abroad', cr(nfia)), ('Net indirect taxes', cr(nit))]
    r.shuffle(rows)
    stem = f'Calculate national income (NNPFC) by the expenditure method from the following data:\n{lines(rows)}'
    key = (f'GDPMP = PFCE + GFCE + GDCF + net exports = {pfce} + {gfce} + {gdcf} + ({nx}) = {gdp} (2 marks); '
           f'NNPFC = GDPMP − depreciation + NFIA − NIT = {gdp} − {dep} + ({nfia}) − {nit} = {cr(nnpfc)} (2 marks).')
    return {'stem': stem, 'answer': f'National income = {cr(nnpfc)}', 'key': key,
            'distractors': [cr(gdp), cr(gdp - dep - nit), cr(nnpfc + nit)]}


def ni_inc(r):
    coe = r.randrange(1500, 6000, 50)
    rent = r.randrange(100, 800, 10)
    intr = r.randrange(100, 800, 10)
    prof = r.randrange(200, 1500, 10)
    mixed = r.randrange(200, 1500, 10)
    dep = r.randrange(100, 500, 10)
    nfia = r.choice([1, -1]) * r.randrange(10, 150, 5)
    nit = r.randrange(100, 600, 10)
    ndpfc = coe + rent + intr + prof + mixed
    gnpmp = ndpfc + dep + nfia + nit
    rows = [('Compensation of employees', cr(coe)), ('Rent', cr(rent)), ('Interest', cr(intr)), ('Profit', cr(prof)),
            ('Mixed income of self-employed', cr(mixed)), ('Consumption of fixed capital', cr(dep)),
            ('Net factor income from abroad', cr(nfia)), ('Net indirect taxes', cr(nit))]
    r.shuffle(rows)
    stem = f'From the following data, calculate (i) net domestic product at factor cost and (ii) gross national product at market price:\n{lines(rows)}'
    ans = f'(i) NDPFC = {cr(ndpfc)}; (ii) GNPMP = {cr(gnpmp)}'
    key = (f'(i) NDPFC = COE + rent + interest + profit + mixed income = {coe} + {rent} + {intr} + {prof} + {mixed} = {cr(ndpfc)} (2 marks); '
           f'(ii) GNPMP = NDPFC + depreciation + NFIA + NIT = {ndpfc} + {dep} + ({nfia}) + {nit} = {cr(gnpmp)} (2 marks).')
    return {'stem': stem, 'answer': ans, 'key': key}


AGG = {
    'GNP at market price': lambda g, d, n, t: g + n,
    'NDP at market price': lambda g, d, n, t: g - d,
    'NNP at market price': lambda g, d, n, t: g - d + n,
    'GDP at factor cost': lambda g, d, n, t: g - t,
    'NNP at factor cost': lambda g, d, n, t: g - d + n - t,
    'NDP at factor cost': lambda g, d, n, t: g - d - t,
}
AGGF = {
    'GNP at market price': 'GDPMP + NFIA', 'NDP at market price': 'GDPMP − depreciation', 'NNP at market price': 'GDPMP − depreciation + NFIA',
    'GDP at factor cost': 'GDPMP − NIT', 'NNP at factor cost': 'GDPMP − depreciation + NFIA − NIT', 'NDP at factor cost': 'GDPMP − depreciation − NIT',
}


def agg_conv(r):
    g = r.randrange(5000, 20000, 100)
    d = r.randrange(200, 1200, 10)
    n = r.choice([1, -1]) * r.randrange(20, 300, 5)
    t = r.randrange(200, 1500, 10)
    tgt = r.choice(list(AGG))
    ans = AGG[tgt](g, d, n, t)
    cands = [AGG[k](g, d, n, t) for k in AGG if k != tgt] + [g + d + n, g - n]
    stem = (f'GDP at market price of a country is {cr(g)}, depreciation is {cr(d)}, net factor income from abroad is {cr(n)} '
            f'and net indirect taxes are {cr(t)}. The value of {tgt} is:')
    return m4(r, stem, ans, cands, f'{tgt} = {AGGF[tgt]} = {cr(ans)}.')


def nfia_find(r):
    g = r.randrange(5000, 20000, 100)
    d = r.randrange(200, 1200, 10)
    n = r.choice([1, -1]) * r.randrange(20, 300, 5)
    t = r.randrange(200, 1500, 10)
    nnpfc = g - d + n - t
    stem = (f'National income (NNPFC) of a country is {cr(nnpfc)}, GDP at market price is {cr(g)}, consumption of fixed capital is {cr(d)} '
            f'and net indirect taxes are {cr(t)}. Calculate net factor income from abroad and state what its sign tells us.')
    meaning = ('factor income earned by residents abroad exceeds that earned by non-residents in the domestic territory, so GNP > GDP'
               if n > 0 else 'non-residents earn more in the domestic territory than residents earn abroad, so GDP > GNP')
    key = (f'NNPFC = GDPMP − depreciation + NFIA − NIT, so NFIA = NNPFC − GDPMP + depreciation + NIT = {nnpfc} − {g} + {d} + {t} = {cr(n)} (2 marks); '
           f'{"positive" if n > 0 else "negative"}: {meaning} (1 mark).')
    return {'stem': stem, 'answer': f'NFIA = {cr(n)}; it is {"positive" if n > 0 else "negative"}', 'key': key}


def ni_case(r):
    pfce, gfce, gdcf, nx, dep, nfia, nit = _ni_data(r)
    gdp = pfce + gfce + gdcf + nx
    city = r.choice(CITIES)
    rows = [('Private final consumption expenditure', cr(pfce)), ('Government final consumption expenditure', cr(gfce)),
            ('Gross domestic capital formation', cr(gdcf)), ('Net exports', cr(nx)), ('Consumption of fixed capital', cr(dep)),
            ('Net factor income from abroad', cr(nfia)), ('Net indirect taxes', cr(nit))]
    gnp = gdp + nfia
    nnpfc = gdp - dep + nfia - nit
    parts = ['Calculate GDP at market price. (1)', 'Calculate GNP at market price. (1)',
             'Calculate national income and state whether net exports in the data show a trade surplus or deficit. (2)']
    stem = (f'A student team from {city} compiled the following estimates for an imaginary economy for a year. Study the data and answer the questions.\n'
            f'{lines(rows)}\n{sub(parts)}')
    ans = (f'(i) GDPMP = {cr(gdp)}; (ii) GNPMP = {cr(gnp)}; (iii) NNPFC = {cr(nnpfc)}; net exports {cr(nx)} show a '
           f'{"surplus" if nx > 0 else "deficit"}')
    key = (f'1+1+2 marks: (i) {pfce} + {gfce} + {gdcf} + ({nx}) = {gdp}; (ii) {gdp} + ({nfia}) = {gnp}; '
           f'(iii) {gdp} − {dep} + ({nfia}) − {nit} = {nnpfc} (1 mark), net exports {"positive – surplus" if nx > 0 else "negative – deficit"} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def deflator(r):
    real = r.randrange(2000, 9000, 100)
    d = r.choice([105, 110, 112, 115, 120, 125, 130, 140, 150, 160])
    nom = real * d // 100
    if (real * d) % 100:
        raise ValueError
    k = r.random()
    if k < 0.4:
        return m4(r, f'Nominal GDP of an economy is {cr(nom)} and real GDP is {cr(real)}. The GDP deflator is:', d,
                  [round(real * 100 / nom), d - 100, d + 10, 100], f'GDP deflator = nominal GDP ÷ real GDP × 100 = {nom} ÷ {real} × 100 = {d}.',
                  fmt=lambda x: num(x))
    if k < 0.7:
        return m4(r, f'Nominal GDP is {cr(nom)} and the GDP deflator is {d}. Real GDP is:', real, [nom * d // 100, nom - d, nom],
                  f'Real GDP = nominal GDP ÷ deflator × 100 = {nom} ÷ {d} × 100 = {cr(real)}.')
    return m4(r, f'Real GDP is {cr(real)} and the GDP deflator is {d}. Nominal GDP is:', nom, [real * 100 // d, real + d, real],
              f'Nominal GDP = real GDP × deflator ÷ 100 = {real} × {d} ÷ 100 = {cr(nom)}.')


def real_growth(r):
    for _ in range(100):
        r1 = r.randrange(2000, 8000, 100)
        g = r.choice([2, 4, 5, 6, 8, 10, 12, 15, -2, -4, -5])
        if (r1 * g) % 100:
            continue
        r2 = r1 + r1 * g // 100
        d1, d2 = r.choice([(100, 110), (110, 121), (100, 105), (120, 126), (100, 120), (125, 150), (100, 108), (105, 112)])
        if (r1 * d1) % 100 or (r2 * d2) % 100:
            continue
        n1, n2 = r1 * d1 // 100, r2 * d2 // 100
        break
    else:
        raise ValueError
    ng = Fraction(n2 - n1, n1) * 100
    stem = (f'Nominal GDP of an economy was {cr(n1)} in year 1 and {cr(n2)} in year 2. The GDP deflator was {d1} in year 1 and {d2} in year 2. '
            f'Calculate real GDP in both years and the growth rate of real GDP. Did the economy\'s output really grow as much as nominal GDP suggests?')
    ans = f'Real GDP: year 1 {cr(r1)}, year 2 {cr(r2)}; real growth {pct(g)}; nominal growth {pct(float(ng))}, so the difference is due to prices'
    key = (f'Real GDP = nominal ÷ deflator × 100: year 1 = {n1} × 100 ÷ {d1} = {r1}; year 2 = {n2} × 100 ÷ {d2} = {r2} (2 marks); '
           f'real growth = ({r2} − {r1}) ÷ {r1} × 100 = {pct(g)} (1 mark); nominal GDP grew {pct(float(ng))}, the rest reflects rising prices (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


# ---------------------------------------------------------------- ch03 money multiplier

LRRS = [Fraction(1, 5), Fraction(1, 10), Fraction(1, 4), Fraction(1, 8), Fraction(1, 20), Fraction(2, 25), Fraction(1, 2)]


def lrr_s(x):
    return pct(float(x * 100), 1)


def mm_basic(r):
    lrr = r.choice(LRRS)
    k = 1 / lrr
    if r.random() < 0.5:
        return m4(r, f'If the legal reserve ratio is {lrr_s(lrr)}, the value of the money multiplier is:', float(k),
                  [float(lrr * 100), float(1 - lrr), float(k) / 2, float(k) + 1],
                  f'Money multiplier = 1 ÷ LRR = 1 ÷ {num(float(lrr), 3)} = {num(float(k))}.', fmt=lambda x: num(x, 3))
    dep = r.randrange(100, 2000, 50)
    tot = dep * k
    if tot.denominator != 1:
        raise ValueError
    tot = int(tot)
    return m4(r, f'A bank receives an initial deposit of {cr(dep)}. If the legal reserve ratio is {lrr_s(lrr)}, the total deposits created in the banking system will be:',
              tot, [int(dep * (1 - lrr)), dep, tot - dep, int(dep * lrr)], f'Total deposits = initial deposit × 1/LRR = {dep} × {num(float(k))} = {cr(tot)}.')


def credit_total(r):
    lrr = r.choice(LRRS[:-1])
    dep = r.randrange(200, 3000, 50)
    k = 1 / lrr
    tot = dep * k
    first = dep * (1 - lrr)
    if tot.denominator != 1 or first.denominator != 1:
        raise ValueError
    who = name(r)
    stem = (f'{who} deposits {cr(dep)} in a commercial bank. The legal reserve ratio is {lrr_s(lrr)}. Calculate (i) the amount the bank can lend in the '
            f'first round, (ii) the money multiplier and (iii) the total deposits that can be created in the banking system.')
    ans = f'(i) {cr(int(first))}; (ii) {num(float(k))}; (iii) {cr(int(tot))}'
    key = (f'(i) Reserves = {lrr_s(lrr)} of {dep} = {num(float(dep * lrr))}, so loan = {dep} − {num(float(dep * lrr))} = {int(first)} (1 mark); '
           f'(ii) k = 1 ÷ LRR = {num(float(k))} (1 mark); (iii) total deposits = {dep} × {num(float(k))} = {cr(int(tot))} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def find_lrr(r):
    lrr = r.choice(LRRS)
    dep = r.randrange(200, 3000, 50)
    tot = dep / lrr
    if tot.denominator != 1:
        raise ValueError
    tot = int(tot)
    stem = (f'An initial deposit of {cr(dep)} leads to the creation of total deposits of {cr(tot)} in the banking system. '
            f'Calculate the money multiplier and the legal reserve ratio. What would happen to total deposits if the reserve ratio were raised?')
    ans = f'Money multiplier = {num(float(1 / lrr))}; LRR = {lrr_s(lrr)}; a higher LRR would reduce total deposits'
    key = (f'k = total deposits ÷ initial deposit = {tot} ÷ {dep} = {num(float(1 / lrr))} (1 mark); LRR = 1 ÷ k = {lrr_s(lrr)} (1 mark); '
           f'a higher LRR lowers k, so total deposits fall (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def find_initial(r):
    lrr, lrr2 = r.sample(LRRS, 2)
    dep = r.randrange(200, 3000, 50)
    tot = dep / lrr
    tot2 = dep / lrr2
    if tot.denominator != 1 or tot2.denominator != 1:
        raise ValueError
    tot, tot2 = int(tot), int(tot2)
    stem = (f'Total deposits of {cr(tot)} were created in the banking system when the legal reserve ratio was {lrr_s(lrr)}. '
            f'(i) Calculate the initial deposit. (ii) If the RBI changes the legal reserve ratio to {lrr_s(lrr2)}, what will be the total deposits created '
            f'from the same initial deposit? (iii) State whether this is an expansionary or contractionary measure.')
    kind = 'contractionary' if lrr2 > lrr else 'expansionary'
    ans = f'(i) {cr(dep)}; (ii) {cr(tot2)}; (iii) {kind}'
    key = (f'(i) Initial deposit = total deposits × LRR = {tot} × {num(float(lrr), 3)} = {cr(dep)} (1 mark); '
           f'(ii) new k = 1 ÷ {num(float(lrr2), 3)} = {num(float(1 / lrr2))}, total = {dep} × {num(float(1 / lrr2))} = {cr(tot2)} (2 marks); '
           f'(iii) the reserve ratio {"rises" if lrr2 > lrr else "falls"}, so credit {"contracts" if lrr2 > lrr else "expands"}: {kind} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


# ---------------------------------------------------------------- ch04 income determination

MPCS = [Fraction(1, 2), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(9, 10), Fraction(7, 10), Fraction(5, 6)]


def fr(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else num(float(x), 3) if x.denominator in (2, 4, 5, 8, 10, 20, 25) else f'{x.numerator}/{x.denominator}'


def co(x):
    """Coefficient of Y in a function: 0.8Y, (2/3)Y."""
    t = fr(x)
    return f'({t})' if '/' in t else t


def mpc_mps(r):
    b = r.choice(MPCS)
    dy = r.randrange(100, 2000, 50)
    dc = dy * b
    if dc.denominator != 1:
        raise ValueError
    dc = int(dc)
    if r.random() < 0.5:
        return m4(r, f'When income rises by {cr(dy)}, consumption rises by {cr(dc)}. The marginal propensity to save is:', 1 - b,
                  [b, (1 - b) / 2, Fraction(1), b / 2], f'MPC = ΔC/ΔY = {dc}/{dy} = {fr(b)}; MPS = 1 − MPC = {fr(1 - b)}.', fmt=fr)
    return m4(r, f'When income rises by {cr(dy)}, saving rises by {cr(dy - dc)}. The marginal propensity to consume is:', b,
              [1 - b, b / 2, Fraction(1), (1 - b) / 2], f'MPS = ΔS/ΔY = {dy - dc}/{dy} = {fr(1 - b)}; MPC = 1 − MPS = {fr(b)}.', fmt=fr)


def apc_table(r):
    for _ in range(100):
        b = r.choice(MPCS)
        y1 = r.randrange(500, 3000, 100)
        dy = r.randrange(100, 1000, 100)
        c1 = r.randrange(int(y1 * 0.6), int(y1 * 1.1), 10)
        dc = dy * b
        if dc.denominator == 1:
            break
    else:
        raise ValueError
    c2 = c1 + int(dc)
    y2 = y1 + dy
    apc1 = Fraction(c1, y1)
    stem = (f'When income is {cr(y1)}, consumption is {cr(c1)}. When income rises to {cr(y2)}, consumption rises to {cr(c2)}. '
            f'Calculate (i) APC and APS at the income of {cr(y1)}, and (ii) MPC and MPS.')
    ans = f'(i) APC = {num(float(apc1), 3)}, APS = {num(float(1 - apc1), 3)}; (ii) MPC = {fr(b)}, MPS = {fr(1 - b)}'
    key = (f'(i) APC = C/Y = {c1}/{y1} = {num(float(apc1), 3)}; APS = 1 − APC = {num(float(1 - apc1), 3)} (1½ marks); '
           f'(ii) MPC = ΔC/ΔY = {int(dc)}/{dy} = {fr(b)}; MPS = 1 − MPC = {fr(1 - b)} (1½ marks).')
    return {'stem': stem, 'answer': ans, 'key': key}


def cfun(r):
    b = r.choice(MPCS)
    a = r.randrange(50, 500, 10)
    y = r.randrange(500, 5000, 100)
    c = a + b * y
    be = Fraction(a) / (1 - b)
    if c.denominator != 1 or be.denominator != 1:
        raise ValueError
    c = int(c)
    stem = (f'The consumption function of an economy is C = {a} + {co(b)}Y (₹ crore). Calculate (i) consumption and saving at an income of {cr(y)}, '
            f'and (ii) the break-even level of income.')
    ans = f'(i) C = {cr(c)}, S = {cr(y - c)}; (ii) break-even income = {cr(int(be))}'
    key = (f'(i) C = {a} + {fr(b)} × {y} = {c}; S = Y − C = {y} − {c} = {y - c} (2 marks); '
           f'(ii) at break-even Y = C: Y = {a} + {co(b)}Y, so Y = {a} ÷ {co(1 - b)} = {cr(int(be))} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def saving_fn(r):
    s = 1 - r.choice(MPCS)
    a = r.randrange(50, 400, 10)
    be = Fraction(a) / s
    if be.denominator != 1:
        raise ValueError
    y = int(be) + r.randrange(100, 2000, 100)
    sv = -a + s * y
    if sv.denominator != 1:
        raise ValueError
    stem = (f'The saving function of an economy is S = −{a} + {co(s)}Y (₹ crore). (i) Derive the consumption function. (ii) Find the break-even level of income. '
            f'(iii) Find saving and APS at an income of {cr(y)}.')
    aps = Fraction(int(sv), y)
    ans = f'(i) C = {a} + {co(1 - s)}Y; (ii) {cr(int(be))}; (iii) S = {cr(int(sv))}, APS = {num(float(aps), 3)}'
    key = (f'(i) C = Y − S = {a} + {fr(1 - s)}Y (1 mark); (ii) S = 0 when Y = {a} ÷ {co(s)} = {int(be)} (1 mark); '
           f'(iii) S = −{a} + {fr(s)} × {y} = {int(sv)} (1 mark); APS = S/Y = {int(sv)}/{y} = {num(float(aps), 3)} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def _eq(r):
    for _ in range(200):
        b = r.choice(MPCS)
        a = r.randrange(50, 600, 10)
        i = r.randrange(50, 800, 10)
        y = Fraction(a + i) / (1 - b)
        if y.denominator == 1:
            return b, a, i, int(y)
    raise ValueError


def eq_income(r):
    b, a, i, y = _eq(r)
    c = a + b * y
    stem = (f'In an economy, C = {a} + {co(b)}Y and autonomous investment I = {i} (₹ crore). Calculate (i) the equilibrium level of income, '
            f'(ii) consumption at equilibrium and (iii) saving at equilibrium.')
    ans = f'(i) Y = {cr(y)}; (ii) C = {cr(int(c))}; (iii) S = {cr(y - int(c))} (= I)'
    key = (f'(i) Y = C + I: Y = {a} + {co(b)}Y + {i}, so Y = ({a} + {i}) ÷ {co(1 - b)} = {y} (1 mark); '
           f'(ii) C = {a} + {fr(b)} × {y} = {int(c)} (1 mark); (iii) S = Y − C = {y - int(c)}, equal to investment {i} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def eq_mcq(r):
    b, a, i, y = _eq(r)
    s = 1 - b
    stem = f'In an economy, the saving function is S = −{a} + {co(s)}Y and investment is {cr(i)}. The equilibrium level of income is:'
    return m4(r, stem, y, [int((a + i) * b), a + i, int(Fraction(i) / s), int(Fraction(abs(i - a)) / s)],
              f'At equilibrium S = I: −{a} + {co(s)}Y = {i}, so Y = ({a} + {i}) ÷ {co(s)} = {cr(y)}.')


def eq_check(r):
    b, a, i, y = _eq(r)
    y1 = y + r.choice([1, -1]) * r.randrange(1, 6) * 100
    if y1 <= 0:
        raise ValueError
    ad = a + b * y1 + i
    if ad.denominator != 1:
        raise ValueError
    ad = int(ad)
    if ad > y1:
        state, inv, move = 'AD exceeds output (excess of planned spending)', 'inventories fall below the planned level', 'firms increase output and income rises'
    else:
        state, inv, move = 'output exceeds AD', 'unplanned inventories pile up', 'firms reduce output and income falls'
    stem = (f'For an economy, C = {a} + {co(b)}Y and I = {i} (₹ crore). (i) Calculate aggregate demand when income is {cr(y1)}. '
            f'(ii) Is the economy in equilibrium at this income? Explain what will happen to inventories and output. (iii) Find the equilibrium income.')
    ans = f'(i) AD = {cr(ad)}; (ii) not in equilibrium: {state}, {inv}, {move}; (iii) Y = {cr(y)}'
    key = (f'(i) AD = {a} + {fr(b)} × {y1} + {i} = {ad} (1 mark); (ii) AD ≠ Y: {state}; {inv}; {move} (2 marks); '
           f'(iii) Y = ({a} + {i}) ÷ {co(1 - b)} = {y} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def k_mcq(r):
    b = r.choice(MPCS)
    k = 1 / (1 - b)
    if r.random() < 0.5:
        stem = f'If the marginal propensity to consume is {fr(b)}, the value of the investment multiplier is:'
        key = f'k = 1 ÷ (1 − MPC) = 1 ÷ {co(1 - b)} = {fr(k)}.'
    else:
        stem = f'If the marginal propensity to save is {fr(1 - b)}, the value of the investment multiplier is:'
        key = f'k = 1 ÷ MPS = 1 ÷ {co(1 - b)} = {fr(k)}.'
    return m4(r, stem, k, [1 / b, b, 1 - b, k + 1], key, fmt=fr)


def dY(r):
    b = r.choice(MPCS)
    k = 1 / (1 - b)
    di = r.randrange(50, 2000, 50)
    dy = di * k
    if dy.denominator != 1:
        raise ValueError
    dy = int(dy)
    stem = (f'In an economy, investment increases by {cr(di)} and the marginal propensity to consume is {fr(b)}. Calculate (i) the investment multiplier, '
            f'(ii) the increase in income and (iii) the increase in consumption.')
    ans = f'(i) k = {fr(k)}; (ii) ΔY = {cr(dy)}; (iii) ΔC = {cr(dy - di)}'
    key = (f'(i) k = 1 ÷ (1 − {fr(b)}) = {fr(k)} (1 mark); (ii) ΔY = k × ΔI = {fr(k)} × {di} = {dy} (1 mark); '
           f'(iii) ΔC = ΔY − ΔI = {dy} − {di} = {dy - di} (or MPC × ΔY) (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def dI(r):
    b = r.choice(MPCS)
    k = 1 / (1 - b)
    di = r.randrange(50, 2000, 50)
    dy = di * k
    if dy.denominator != 1:
        raise ValueError
    dy = int(dy)
    stem = (f'The government wants national income to rise by {cr(dy)}. If the marginal propensity to save is {fr(1 - b)}, how much additional investment is required? '
            f'Show your working and state how the multiplier would change if MPS rose.')
    ans = f'ΔI = {cr(di)} (k = {fr(k)}); a higher MPS would reduce the multiplier'
    key = (f'k = 1 ÷ MPS = 1 ÷ {co(1 - b)} = {fr(k)} (1 mark); ΔI = ΔY ÷ k = {dy} ÷ {fr(k)} = {cr(di)} (1 mark); '
           f'multiplier is inversely related to MPS, so it would fall (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def k_reverse(r):
    b = r.choice(MPCS)
    k = 1 / (1 - b)
    di = r.randrange(50, 1500, 50)
    dy = di * k
    if dy.denominator != 1:
        raise ValueError
    dy = int(dy)
    stem = (f'An increase in investment of {cr(di)} raises national income by {cr(dy)}. Calculate (i) the multiplier, (ii) MPC, (iii) MPS and '
            f'(iv) the change in saving.')
    ans = f'(i) k = {fr(k)}; (ii) MPC = {fr(b)}; (iii) MPS = {fr(1 - b)}; (iv) ΔS = {cr(di)}'
    key = (f'(i) k = ΔY/ΔI = {dy}/{di} = {fr(k)}; (ii) k = 1/(1 − MPC), so MPC = 1 − 1/k = {fr(b)}; (iii) MPS = 1 − MPC = {fr(1 - b)}; '
           f'(iv) ΔS = MPS × ΔY = {fr(1 - b)} × {dy} = {di}, equal to ΔI at the new equilibrium (1 mark each).')
    return {'stem': stem, 'answer': ans, 'key': key}


def k_rounds(r):
    b = r.choice([Fraction(1, 2), Fraction(3, 5), Fraction(3, 4), Fraction(4, 5), Fraction(9, 10), Fraction(7, 10)])
    di = r.randrange(100, 1000, 100)
    r1 = Fraction(di)
    r2 = r1 * b
    r3 = r2 * b
    tot = r1 / (1 - b)
    if tot.denominator != 1:
        raise ValueError
    who = name(r)
    stem = (f'{who} argues that an extra investment of {cr(di)} on a highway project will raise national income by exactly {cr(di)}. The MPC is {fr(b)}. '
            f'Show the increase in income in the first three rounds and the total increase in income, and evaluate {who}\'s claim.')
    ans = (f'Rounds: {num(float(r1))}, {num(float(r2))}, {num(float(r3))} (₹ crore); total ΔY = {cr(int(tot))}; the claim is wrong because spending of '
           f'each round becomes income in the next')
    key = (f'Round 1 = ΔI = {num(float(r1))}; round 2 = MPC × {num(float(r1))} = {num(float(r2))}; round 3 = {num(float(r3))} (2 marks); '
           f'total = {di} × 1/(1 − {fr(b)}) = {int(tot)} (1 mark); the claim ignores the multiplier – income rises by a multiple of investment (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def gap(r):
    b, a, i, y = _eq(r)
    yf = y + r.choice([1, -1]) * r.randrange(1, 8) * 100
    if yf <= 0:
        raise ValueError
    ad = a + b * yf + i
    if ad.denominator != 1:
        raise ValueError
    ad = int(ad)
    g = ad - yf
    typ = 'inflationary' if g > 0 else 'deflationary'
    stem = (f'In an economy, C = {a} + {co(b)}Y and I = {i} (₹ crore). The full-employment level of income is {cr(yf)}. '
            f'Calculate aggregate demand at full employment and identify the type and size of the gap.')
    ans = f'AD at full employment = {cr(ad)}; {typ} gap of {cr(abs(g))}'
    key = (f'AD = {a} + {fr(b)} × {yf} + {i} = {ad} (1 mark); AD {"exceeds" if g > 0 else "falls short of"} full-employment output {yf} (1 mark); '
           f'{typ} gap = {cr(abs(g))} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def gap_fix(r):
    b, a, i, y = _eq(r)
    k = 1 / (1 - b)
    for _ in range(50):
        dg = r.randrange(10, 400, 10) * r.choice([1, -1])
        dy = dg * k
        if dy.denominator == 1 and y + dy > 0:
            break
    else:
        raise ValueError
    yf = y + int(dy)
    typ = 'deficient demand (deflationary gap)' if yf > y else 'excess demand (inflationary gap)'
    stem = (f'An economy is in equilibrium at an income of {cr(y)}, while full-employment income is {cr(yf)}. The MPC is {fr(b)}. '
            f'(i) Identify the problem. (ii) Calculate the change in government expenditure needed to reach full employment. '
            f'(iii) Suggest one monetary measure that would work in the same direction.')
    mon = 'lower the repo rate or buy government securities' if yf > y else 'raise the repo rate or sell government securities'
    chg = f'{"increase" if dg > 0 else "reduce"} government expenditure by {cr(abs(int(dg)))}'
    ans = f'(i) {typ}; (ii) {chg}; (iii) RBI could {mon}'
    key = (f'(i) Equilibrium income {"below" if yf > y else "above"} full employment – {typ} (1 mark); (ii) k = 1 ÷ (1 − {fr(b)}) = {fr(k)}; '
           f'required ΔY = {yf} − {y} = {int(dy)}; ΔG = ΔY ÷ k = {int(dg)}, i.e. {chg} (2 marks); (iii) {mon} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def eq_case(r):
    b, a, i, y = _eq(r)
    k = 1 / (1 - b)
    di = r.randrange(5, 50) * 10
    dy = di * k
    if dy.denominator != 1:
        raise ValueError
    city = r.choice(CITIES)
    parts = ['State the value of the marginal propensity to save. (1)', 'Calculate the equilibrium level of income. (1)',
             f'If investment rises by {cr(di)}, calculate the new equilibrium income and explain the role of the multiplier. (2)']
    stem = (f'A policy brief prepared in {city} for an imaginary economy says: "Households consume {cr(a)} even at zero income and spend '
            f'{fr(b)} of every additional rupee of income. Firms plan an autonomous investment of {cr(i)}." Read the brief and answer the questions.\n{sub(parts)}')
    ans = f'(i) MPS = {fr(1 - b)}; (ii) Y = {cr(y)}; (iii) new Y = {cr(y + int(dy))} (ΔY = {fr(k)} × {di} = {int(dy)})'
    key = (f'1+1+2 marks: (i) MPS = 1 − {fr(b)} = {fr(1 - b)}; (ii) Y = ({a} + {i}) ÷ {co(1 - b)} = {y}; '
           f'(iii) k = {fr(k)}, ΔY = {int(dy)}, new Y = {y + int(dy)} (1 mark); spending in each round becomes income for others (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


# ---------------------------------------------------------------- ch05 deficits

def _budget(r):
    rr = r.randrange(800, 3000, 10)
    re = rr + r.randrange(50, 800, 10)
    ce = r.randrange(200, 1200, 10)
    rec = r.randrange(10, 150, 5)
    dis = r.randrange(10, 200, 5)
    intr = r.randrange(50, (re - rr) + ce, 10)
    return rr, re, ce, rec, dis, intr


def deficits(r):
    rr, re, ce, rec, dis, intr = _budget(r)
    rd = re - rr
    fd = re + ce - rr - rec - dis
    pd = fd - intr
    rows = [('Revenue receipts', cr(rr)), ('Revenue expenditure', cr(re)), ('Capital expenditure', cr(ce)), ('Recovery of loans', cr(rec)),
            ('Disinvestment proceeds', cr(dis)), ('Interest payments', cr(intr))]
    r.shuffle(rows)
    stem = f'From the following data of a government budget, calculate (i) revenue deficit, (ii) fiscal deficit and (iii) primary deficit:\n{lines(rows)}'
    ans = f'(i) RD = {cr(rd)}; (ii) FD = {cr(fd)}; (iii) PD = {cr(pd)}'
    key = (f'(i) RD = RE − RR = {re} − {rr} = {rd}; (ii) FD = total expenditure − (RR + recovery of loans + disinvestment) = ({re} + {ce}) − ({rr} + {rec} + {dis}) = {fd}; '
           f'(iii) PD = FD − interest = {fd} − {intr} = {pd} (1 mark each).')
    return {'stem': stem, 'answer': ans, 'key': key}


def def_mcq(r):
    rr, re, ce, rec, dis, intr = _budget(r)
    rd = re - rr
    fd = re + ce - rr - rec - dis
    pd = fd - intr
    t = r.choice(['fiscal', 'primary', 'revenue'])
    data = (f'revenue receipts {cr(rr)}, revenue expenditure {cr(re)}, capital expenditure {cr(ce)}, non-debt capital receipts {cr(rec + dis)} '
            f'and interest payments {cr(intr)}')
    if t == 'fiscal':
        return m4(r, f'A government has {data}. Its fiscal deficit is:', fd, [rd, pd, re + ce - rr, fd + intr],
                  f'FD = (RE + CE) − (RR + non-debt capital receipts) = ({re} + {ce}) − ({rr} + {rec + dis}) = {cr(fd)}.')
    if t == 'primary':
        return m4(r, f'A government has {data}. Its primary deficit is:', pd, [fd, rd - intr, fd + intr, rd],
                  f'FD = {fd}; PD = FD − interest = {fd} − {intr} = {cr(pd)}.')
    return m4(r, f'A government has {data}. Its revenue deficit is:', rd, [fd, pd, rd - intr, re + ce - rr],
              f'RD = RE − RR = {re} − {rr} = {cr(rd)}.')


def def_reverse(r):
    for _ in range(100):
        fd = r.randrange(200, 2000, 10)
        intr = r.randrange(50, fd - 20, 10)
        rd = r.randrange(20, fd, 10)
        if (rd * 100) % fd == 0:
            break
    else:
        raise ValueError
    pd = fd - intr
    share = rd * 100 // fd
    stem = (f'The fiscal deficit of a government is {cr(fd)}, its revenue deficit is {cr(rd)} and interest payments are {cr(intr)}. '
            f'(i) Calculate the primary deficit. (ii) What percentage of the borrowing is used to meet revenue expenditure? (iii) Comment on what this implies.')
    ans = f'(i) PD = {cr(pd)}; (ii) {share}% of borrowing; (iii) that part of borrowing finances consumption spending that creates no assets'
    key = (f'(i) PD = FD − interest = {fd} − {intr} = {pd} (1 mark); (ii) RD ÷ FD × 100 = {rd} ÷ {fd} × 100 = {share}% (1 mark); '
           f'(iii) borrowing used for revenue expenditure does not create assets to repay the debt; it raises future interest burden and risk of a debt trap (2 marks).')
    return {'stem': stem, 'answer': ans, 'key': key}


def budget_case(r):
    rr, re, ce, rec, dis, intr = _budget(r)
    rd = re - rr
    fd = re + ce - rr - rec - dis
    pd = fd - intr
    st = r.choice(['Rajasthan', 'Odisha', 'Kerala', 'Punjab', 'Assam', 'Karnataka', 'Bihar', 'Gujarat', 'Telangana', 'Haryana'])
    rows = [('Revenue receipts', cr(rr)), ('Revenue expenditure', cr(re)), ('Capital expenditure', cr(ce)),
            ('Non-debt capital receipts', cr(rec + dis)), ('Interest payments', cr(intr))]
    parts = ['Calculate the revenue deficit. (1)', 'Calculate the fiscal deficit. (1)',
             'Calculate the primary deficit and explain what it shows about the government\'s current fiscal position. (2)']
    stem = (f'The following figures are from a mock budget prepared by students in a commerce class in {st}. Study them and answer the questions.\n'
            f'{lines(rows)}\n{sub(parts)}')
    ans = f'(i) RD = {cr(rd)}; (ii) FD = {cr(fd)}; (iii) PD = {cr(pd)}'
    key = (f'1+1+2 marks: (i) {re} − {rr} = {rd}; (ii) ({re} + {ce}) − ({rr} + {rec + dis}) = {fd}; (iii) {fd} − {intr} = {pd} (1 mark); '
           f'primary deficit shows borrowing needed for current spending other than interest on past debt (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


# ---------------------------------------------------------------- ch06 BoP and exchange rate

def bot(r):
    x = r.randrange(1000, 5000, 10)
    m = x + r.choice([1, -1]) * r.randrange(50, 1500, 10)
    b = x - m
    word = 'surplus' if b > 0 else 'deficit'
    stem = f'Exports of goods of a country are {cr(x)} and imports of goods are {cr(m)}. The balance of trade shows a:'
    ans = f'{word} of {cr(abs(b))}'
    other = 'deficit' if b > 0 else 'surplus'
    w = [f'{other} of {cr(abs(b))}', f'{word} of {cr(x + m)}', f'{other} of {cr(x + m)}']
    return mcq(stem, ans, w, f'Balance of trade = exports − imports of goods = {x} − {m} = {cr(b)}, i.e. a {word}.', r)


def cab(r):
    x = r.randrange(1000, 5000, 10)
    m = x + r.randrange(100, 1500, 10)
    sv = r.randrange(100, 1200, 10)
    inc = r.choice([1, -1]) * r.randrange(20, 300, 10)
    tr = r.randrange(50, 800, 10)
    b = x - m
    ca = b + sv + inc + tr
    rows = [('Exports of goods', cr(x)), ('Imports of goods', cr(m)), ('Net exports of services', cr(sv)), ('Net income from abroad', cr(inc)),
            ('Net current transfers (remittances)', cr(tr))]
    r.shuffle(rows)
    stem = f'From the following data, calculate (i) the balance of trade and (ii) the balance on current account. State whether each is a surplus or a deficit.\n{lines(rows)}'
    ans = f'(i) BoT = {cr(b)} (deficit); (ii) CAB = {cr(ca)} ({"surplus" if ca > 0 else "deficit" if ca < 0 else "balanced"})'
    key = (f'(i) BoT = {x} − {m} = {b}, a deficit (1 mark); (ii) CAB = BoT + net services + net income + net transfers = {b} + {sv} + ({inc}) + {tr} = {ca} '
           f'(2 marks).')
    return {'stem': stem, 'answer': ans, 'key': key}


def overall(r):
    ca = r.choice([1, -1]) * r.randrange(50, 1500, 10)
    ka = r.choice([1, -1]) * r.randrange(50, 1500, 10)
    eo = r.choice([0, 0, r.randrange(-50, 50, 10)])
    ov = ca + ka + eo
    if ov == 0:
        raise ValueError
    stem = (f'A country has a current account balance of {cr(ca)}, a capital account balance (autonomous transactions) of {cr(ka)}'
            f'{" and errors and omissions of " + cr(eo) if eo else ""}. (i) Calculate the overall balance of payments. (ii) Is it a surplus or a deficit? '
            f'(iii) What will happen to the official foreign exchange reserves? (iv) Name the type of transaction that settles it.')
    word = 'surplus' if ov > 0 else 'deficit'
    res = 'rise' if ov > 0 else 'fall'
    ans = f'(i) {cr(ov)}; (ii) {word}; (iii) reserves {res} by {cr(abs(ov))}; (iv) accommodating (official reserve) transactions'
    key = (f'(i) Overall balance = CAB + KAB{" + errors and omissions" if eo else ""} = {ca} + ({ka}){" + (" + str(eo) + ")" if eo else ""} = {ov} (1 mark); '
           f'(ii) {word} (1 mark); (iii) reserves {res} by {abs(ov)} (1 mark); (iv) accommodating transactions below the line (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


def fx_change(r):
    for _ in range(100):
        a = r.randrange(60, 100)
        p = r.choice([2, 4, 5, 10, 20, 25])
        sign = r.choice([1, -1])
        if (a * p) % 100 == 0:
            b = a + sign * a * p // 100
            break
    else:
        raise ValueError
    dep = b > a
    stem = f'The exchange rate changes from ₹{a} = 1 US dollar to ₹{b} = 1 US dollar. Which of the following is correct?'
    ans = f'The rupee has {"depreciated" if dep else "appreciated"}; the rupee price of a dollar has {"risen" if dep else "fallen"} by {p}%'
    w = [f'The rupee has {"appreciated" if dep else "depreciated"}; the rupee price of a dollar has {"risen" if dep else "fallen"} by {p}%',
         f'The rupee has {"depreciated" if dep else "appreciated"}; the rupee price of a dollar has {"risen" if dep else "fallen"} by {abs(b - a)}%',
         f'The rupee has been {"devalued" if dep else "revalued"} by the RBI under a fixed exchange rate']
    return mcq(stem, ans, w, f'{"More" if dep else "Fewer"} rupees are now needed per dollar: change = ({b} − {a}) ÷ {a} × 100 = {sign * p}%, so the rupee has '
                             f'{"depreciated" if dep else "appreciated"} (under a flexible rate this is market-driven, not devaluation).', r)


GOODS_X = [('a handloom saree', 4000, 12000), ('a kilogram of Darjeeling tea', 1500, 4000), ('a bicycle', 5000, 12000), ('a pair of leather shoes', 2000, 6000),
           ('a set of brass lamps', 3000, 9000), ('a cricket bat', 2500, 8000), ('a box of basmati rice', 1000, 3000), ('a carpet', 8000, 30000)]


def fx_goods(r):
    g, lo, hi = r.choice(GOODS_X)
    a = r.randrange(70, 100)
    b = a + r.choice([1, -1]) * r.randrange(2, 12)
    d1 = r.randrange(lo // a + 1, hi // a)
    p = d1 * a
    d2 = round(p / b, 2)
    dep = b > a
    stem = (f'An Indian exporter sells {g} at ₹{p:,}. The exchange rate changes from ₹{a} = $1 to ₹{b} = $1. Calculate the dollar price before and after the change, '
            f'and explain the likely effect on the demand for Indian exports.')
    ans = (f'Before ${d1}, after about ${num(d2)}; the rupee has {"depreciated" if dep else "appreciated"}, so Indian exports become '
           f'{"cheaper" if dep else "costlier"} for foreigners and demand {"rises" if dep else "falls"}')
    key = (f'Dollar price = ₹{p:,} ÷ {a} = ${d1}; after = ₹{p:,} ÷ {b} ≈ ${num(d2)} (2 marks); rupee {"depreciated" if dep else "appreciated"}, '
           f'goods {"cheaper" if dep else "costlier"} for foreigners, demand for exports {"rises" if dep else "falls"} (1 mark).')
    return {'stem': stem, 'answer': ans, 'key': key}


import re as _re

_MINUS = _re.compile(r'(?<=[\s(=])-(?=\d)')


def _fix(gen):
    def g(r):
        v = gen(r)
        for k in ('stem', 'answer', 'key'):
            v[k] = _MINUS.sub('−', v[k])
        return v
    g.__name__ = gen.__name__
    return g


FAMILIES = {
    S + '02-st1': [F('C1', 'D1', 'mcq', stock_flow), F('C2', 'D2', 'mcq', fin_int), F('C2', 'D2', 'mcq', net_inv)],
    S + '02-st3': [F('C2', 'D3', 'numerical', va_firm, **Q3), F('C3', 'D3', 'numerical', ni_exp, **Q4), F('C3', 'D4', 'numerical', ni_inc, **Q4),
                   F('C2', 'D2', 'mcq', agg_conv), F('C3', 'D4', 'numerical', nfia_find, gap='G5', **Q3),
                   F('C4', 'D4', 'case', ni_case, **CASE)],
    S + '02-st4': [F('C2', 'D2', 'mcq', deflator), F('C3', 'D4', 'numerical', real_growth, gap='G5', **Q4)],
    S + '03-st2': [F('C2', 'D2', 'mcq', mm_basic), F('C2', 'D3', 'numerical', credit_total, **Q3), F('C3', 'D3', 'numerical', find_lrr, **Q3),
                   F('C3', 'D4', 'numerical', find_initial, gap='G5', **Q4)],
    S + '04-st1': [F('C2', 'D2', 'mcq', mpc_mps), F('C2', 'D3', 'numerical', apc_table, **Q3), F('C3', 'D3', 'numerical', cfun, **Q3),
                   F('C3', 'D4', 'numerical', saving_fn, gap='G5', **Q4)],
    S + '04-st2': [F('C2', 'D2', 'mcq', eq_mcq), F('C2', 'D3', 'numerical', eq_income, **Q3), F('C3', 'D4', 'numerical', eq_check, gap='G5', **Q4),
                   F('C4', 'D4', 'case', eq_case, **CASE)],
    S + '04-st3': [F('C2', 'D2', 'mcq', k_mcq), F('C2', 'D3', 'numerical', dY, **Q3), F('C3', 'D3', 'numerical', dI, **Q3),
                   F('C3', 'D4', 'numerical', k_reverse, gap='G5', **Q4), F('C4', 'D4', 'numerical', k_rounds, **Q4)],
    S + '04-st4': [F('C2', 'D3', 'numerical', gap, **Q3), F('C3', 'D4', 'numerical', gap_fix, gap='G5', **Q4)],
    S + '05-st3': [F('C2', 'D2', 'mcq', def_mcq), F('C2', 'D3', 'numerical', deficits, **Q3), F('C3', 'D4', 'numerical', def_reverse, gap='G5', **Q4),
                   F('C4', 'D4', 'case', budget_case, **CASE)],
    S + '06-st1': [F('C2', 'D2', 'mcq', bot), F('C3', 'D3', 'numerical', cab, **Q3)],
    S + '06-st2': [F('C3', 'D4', 'numerical', overall, gap='G5', **Q4)],
    S + '06-st3': [F('C2', 'D2', 'mcq', fx_change)],
    S + '06-st4': [F('C3', 'D3', 'numerical', fx_goods, **Q3)],
}

for _fs in FAMILIES.values():
    for _f in _fs:
        _f.gen = _fix(_f.gen)
