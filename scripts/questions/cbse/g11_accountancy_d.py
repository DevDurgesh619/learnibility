"""CBSE class 11 accountancy families, ch08-ch09 (Financial Statements I and II, sole proprietorship)."""
from __future__ import annotations

from qbank import mcq, inr
from g11_accountancy_kit import facts, FF, ctx, amt, entry

S = 'cbse-g11-accountancy-ch'

STAKE = ['Owners', 'Management', 'Banks and lenders', 'Investors', 'Creditors (suppliers)', 'Government and tax authorities', 'Employees']
CH08_ST1 = dict(
    cat='term',
    terms=[('Financial statements', 'The end products of the accounting process: the trading and profit and loss account (statement of profit and loss) and the balance sheet, showing results and financial position.'),
           ('Trading and profit and loss account', 'The statement that shows the gross profit and the net profit or loss of a business for an accounting period.'),
           ('Balance sheet', 'A statement of the assets, liabilities and capital of a business on a particular date.'),
           ('Stakeholders', 'Persons and groups interested in the business, such as owners, lenders, investors, employees and the government, who use its financial statements.')],
    lists=[('obj', 'objectives of preparing financial statements', [
        ('To ascertain the result of operations', 'Gross profit and net profit or loss for the period are found.'),
        ('To show the financial position', 'Assets, liabilities and capital on the closing date are shown.'),
        ('To provide information to users', 'Stakeholders get information for their decisions.'),
        ('To help in planning and control', 'Management compares results with plans and takes action.')], None),
        ('imp', 'points of importance of financial statements', [
        ('Basis for decisions by owners and investors', 'Profitability and safety of investment can be judged.'),
        ('Assessment of creditworthiness by lenders', 'Banks judge the ability to repay loans.'),
        ('Basis for tax assessment', 'Tax authorities compute income tax and verify GST.'),
        ('Comparison of performance', 'Results can be compared over years and with other firms.')], None)],
    scen=[('Which stakeholder is using the financial statements here?', STAKE, [
        ('{p} owns {f} and wants to know whether the return on {his} capital is better than a fixed deposit.', 'Owners', 'Owners judge profitability of their capital.'),
        ('A bank in {c} studies the balance sheet of {f} before sanctioning a cash credit limit.', 'Banks and lenders', 'Lenders check liquidity and repaying capacity.'),
        ('A supplier checks the current assets of {f} before allowing 60 days\' credit.', 'Creditors (suppliers)', 'Suppliers check short-term solvency.'),
        ('The income tax officer examines the profit and loss account of {f}.', 'Government and tax authorities', 'Tax is assessed on the profit shown.'),
        ('Workers of {f} want to know whether the firm can afford a higher bonus.', 'Employees', 'Employees look at profitability and stability.'),
        ('The manager of {f} compares this year\'s expenses with last year\'s to cut costs.', 'Management', 'Managers use statements for planning and control.')], None)],
    ars=[
        ('Financial statements are prepared at the end of the accounting period.', 'They show the results of the period and the position at its end.', 'a', 'Both true and R explains A.'),
        ('The balance sheet is an account.', 'The balance sheet shows the financial position on a date.', 'd', 'A is false: it is a statement. R is true.'),
        ('Banks are interested in the financial statements of a business.', 'Banks want to judge the ability of the business to repay loans.', 'a', 'Both true and R explains A.')],
    tf=('financial statements', [
        'The balance sheet is prepared on a particular date.',
        'The trading and profit and loss account is prepared for a period.',
        'Financial statements are the end products of the accounting process.'], [
        'The balance sheet shows the profit for the year.',
        'The trading account shows the net profit.',
        'Only the owner uses the financial statements.',
        'Financial statements are prepared before the trial balance.']),
    cases=[('C4', 'D4', 4, '{f}, {c}, has applied to a bank for a loan of ₹10 lakh. The bank asks for its trading and profit and loss account and its balance sheet for the last three years. A supplier and the owner {p} also study the same statements.',
            [('What will the bank look for in each statement?', 'Profit and loss account: profitability and ability to pay interest; balance sheet: liquidity, existing debts and assets available as security.'),
             ('State one need each of the supplier and the owner.', 'Supplier: ability to pay dues on time (current assets vs current liabilities). Owner: profit earned and return on capital.')]),
           ('C4', 'D5', 4, '{p} runs {f} and says, "My business is small; I know my profit from my cash box, so I do not need financial statements."',
            [('Explain why the cash box cannot show the profit.', 'Cash ignores credit sales and purchases, outstanding and prepaid items, stock and depreciation; profit is not the same as cash.'),
             ('Give two other reasons why {he} needs financial statements.', 'To get bank loans and supplier credit; for income tax and GST assessment; to compare performance over years.')])],
)

CAPREV = [('Purchase of machinery', 'Capital expenditure'), ('Wages paid for installation of a new machine', 'Capital expenditure'),
          ('Legal charges on purchase of land', 'Capital expenditure'), ('Construction of a new building', 'Capital expenditure'),
          ('Purchase of a delivery van', 'Capital expenditure'), ('Cost of extension of factory shed', 'Capital expenditure'),
          ('Freight paid on a new machine', 'Capital expenditure'), ('Purchase of a patent', 'Capital expenditure'),
          ('Salaries paid to staff', 'Revenue expenditure'), ('Repairs and maintenance of machinery', 'Revenue expenditure'),
          ('Rent of the office', 'Revenue expenditure'), ('Wages paid to factory workers', 'Revenue expenditure'),
          ('Purchase of goods for resale', 'Revenue expenditure'), ('Insurance premium on stock', 'Revenue expenditure'),
          ('Electricity bill of the shop', 'Revenue expenditure'), ('Depreciation on furniture', 'Revenue expenditure'),
          ('Heavy advertisement to launch a new product (benefit over several years)', 'Deferred revenue expenditure'),
          ('Large expenditure on research for a new product', 'Deferred revenue expenditure'),
          ('Sale proceeds of goods', 'Revenue receipt'), ('Commission received', 'Revenue receipt'), ('Interest received on investments', 'Revenue receipt'),
          ('Rent received from a tenant', 'Revenue receipt'), ('Capital introduced by the owner', 'Capital receipt'),
          ('Loan taken from a bank', 'Capital receipt'), ('Sale of old machinery', 'Capital receipt'), ('Sale of land', 'Capital receipt')]
CR_OPTS = ['Capital expenditure', 'Revenue expenditure', 'Deferred revenue expenditure', 'Capital receipt', 'Revenue receipt']


def c8s2_classify(r):
    it, cls = r.choice(CAPREV)
    exp = 'expenditure' in cls
    pool = ['Capital expenditure', 'Revenue expenditure', 'Deferred revenue expenditure', 'Capital receipt'] if exp else ['Capital receipt', 'Revenue receipt', 'Capital expenditure', 'Revenue expenditure']
    if cls not in pool:
        pool = pool[:3] + [cls]
    return mcq(f'"{it}" is a …', cls, [p for p in pool if p != cls][:3], f'{it}: {cls.lower()}.', r)


def c8s2_total(r):
    d = ctx(r)
    items = r.sample([x for x in CAPREV if 'expenditure' in x[1] and 'Deferred' not in x[1]], 6)
    vals = [(it, c, amt(r, 2000, 200000, 500)) for it, c in items]
    if len({c for _, c, _ in vals}) < 2:
        raise ValueError
    cap = sum(v for _, c, v in vals if c.startswith('Capital'))
    rev = sum(v for _, c, v in vals if c.startswith('Revenue'))
    lines = '; '.join(f'{it.lower()} {inr(v)}' for it, _, v in vals)
    return {'stem': f'From the following items of {d["f"]}, find the total capital expenditure and the total revenue expenditure: {lines}.',
            'answer': f'Capital {inr(cap)}; revenue {inr(rev)}',
            'key': 'Capital: ' + ', '.join(it.lower() for it, c, _ in vals if c.startswith('Capital')) + f' = {inr(cap)}; revenue: ' + ', '.join(it.lower() for it, c, _ in vals if c.startswith('Revenue')) + f' = {inr(rev)}.'}


CH08_ST2 = dict(
    pairs=[('capital expenditure', 'revenue expenditure', [
        ('purpose', 'to acquire or improve fixed assets or increase earning capacity', 'to maintain the business and its assets in working order'),
        ('benefit', 'spread over several years', 'consumed within the year'),
        ('nature', 'non-recurring', 'recurring'),
        ('treatment', 'shown as an asset in the balance sheet', 'charged to the trading or profit and loss account'),
        ('example', 'purchase of machinery', 'repairs to machinery'),
        ('effect on profit', 'does not reduce the current year\'s profit directly (only through depreciation)', 'reduces the current year\'s profit')])],
    scen=[('Classify the item.', CR_OPTS, [
        ('{f} paid ₹15,000 as carriage on a new machine bought for its factory.', 'Capital expenditure', 'It is part of the cost of bringing the asset into use.'),
        ('{f} spent ₹4,000 to repair a broken window of its shop.', 'Revenue expenditure', 'It maintains an existing asset; benefit is short-term.'),
        ('{f} spent ₹12 lakh on advertising to launch a new {g} brand expected to benefit three years.', 'Deferred revenue expenditure', 'Revenue in nature but its benefit extends over several years.'),
        ('{f} sold an old delivery van for ₹1,20,000.', 'Capital receipt', 'Sale of a fixed asset is a capital receipt.'),
        ('{f} received ₹30,000 as commission from a supplier.', 'Revenue receipt', 'It is a normal, recurring income.'),
        ('{p} brought additional capital of ₹2,00,000 into {f}.', 'Capital receipt', 'Capital introduced by the owner is a capital receipt.'),
        ('{f} paid ₹60,000 to overhaul a second-hand machine just bought, before using it.', 'Capital expenditure', 'Making an asset ready for use is part of its cost.'),
        ('{f} paid ₹9,000 as electricity bill for the month.', 'Revenue expenditure', 'A recurring operating expense.')], None)],
    ars=[
        ('Wages paid for installation of machinery are capital expenditure.', 'They are incurred to bring the asset into working condition.', 'a', 'Both true and R explains A.'),
        ('Repairs to machinery are capital expenditure.', 'Repairs maintain the asset in working condition.', 'd', 'A is false: they are revenue expenditure. R is true.'),
        ('Sale of old furniture is a revenue receipt.', 'Sale of a fixed asset does not arise from normal operations.', 'd', 'A is false: it is a capital receipt. R is true.'),
        ('Capital expenditure appears in the balance sheet.', 'Its benefit extends beyond the current accounting period.', 'a', 'Both true and R explains A.')],
)


def _tp(r):
    os_ = amt(r, 20000, 150000, 500)
    pur = amt(r, 200000, 800000, 1000)
    pr = amt(r, 2000, pur // 20, 500)
    wages = amt(r, 10000, 80000, 500)
    carr = amt(r, 1000, 15000, 500)
    sales = pur + amt(r, 100000, 500000, 1000)
    sr = amt(r, 2000, sales // 25, 500)
    cs = amt(r, 20000, 150000, 500)
    cogs = os_ + pur - pr + wages + carr - cs
    gp = sales - sr - cogs
    return dict(os=os_, pur=pur, pr=pr, wages=wages, carr=carr, sales=sales, sr=sr, cs=cs, cogs=cogs, gp=gp)


def c8s3_gp(r):
    d = ctx(r)
    t = _tp(r)
    return {'stem': f'From the following, prepare the trading account of {d["f"]} for the year ended 31 March 2026 and find the gross profit: opening stock {inr(t["os"])}, purchases {inr(t["pur"])}, purchases return {inr(t["pr"])}, wages {inr(t["wages"])}, carriage inwards {inr(t["carr"])}, sales {inr(t["sales"])}, sales return {inr(t["sr"])}, closing stock {inr(t["cs"])}.',
            'answer': f'Gross {"profit" if t["gp"] >= 0 else "loss"} {inr(abs(t["gp"]))}',
            'key': f'Net sales {inr(t["sales"] - t["sr"])}; cost of goods sold = {inr(t["os"])} + {inr(t["pur"] - t["pr"])} + {inr(t["wages"])} + {inr(t["carr"])} − {inr(t["cs"])} = {inr(t["cogs"])}; gross profit = {inr(t["sales"] - t["sr"])} − {inr(t["cogs"])} = {inr(t["gp"])}.',
            'distractors': [inr(t['gp'] + 2 * t['cs']), inr(t['gp'] - t['wages']), inr(t['gp'] + t['pr'] + t['sr'])]}


def c8s3_cogs(r):
    t = _tp(r)
    return {'stem': f'Opening stock {inr(t["os"])}, net purchases {inr(t["pur"] - t["pr"])}, direct expenses {inr(t["wages"] + t["carr"])} and closing stock {inr(t["cs"])}. Calculate the cost of goods sold.',
            'answer': inr(t['cogs']), 'key': f'COGS = opening stock + net purchases + direct expenses − closing stock = {inr(t["cogs"])}.',
            'distractors': [inr(t['cogs'] + 2 * t['cs']), inr(t['cogs'] + t['cs']), inr(t['cogs'] - t['wages'] - t['carr'])]}


def c8s3_np(r):
    d = ctx(r)
    gp = amt(r, 100000, 400000, 1000)
    exps = [('salaries', amt(r, 20000, 80000, 500)), ('rent', amt(r, 10000, 40000, 500)), ('carriage outwards', amt(r, 1000, 10000, 500)),
            ('advertisement', amt(r, 2000, 20000, 500)), ('discount allowed', amt(r, 500, 5000, 100)), ('bad debts', amt(r, 500, 8000, 100))]
    exps = r.sample(exps, 4)
    inc = [('commission received', amt(r, 1000, 15000, 500)), ('discount received', amt(r, 500, 5000, 100)), ('interest received', amt(r, 1000, 10000, 500))]
    inc = r.sample(inc, 2)
    np_ = gp - sum(x for _, x in exps) + sum(x for _, x in inc)
    lines = ', '.join(f'{n} {inr(x)}' for n, x in exps + inc)
    return {'stem': f'{d["f"]} earned a gross profit of {inr(gp)}. Other items: {lines}. Prepare the profit and loss account and find the net profit.',
            'answer': f'Net {"profit" if np_ >= 0 else "loss"} {inr(abs(np_))}',
            'key': f'Net profit = {inr(gp)} − expenses {inr(sum(x for _, x in exps))} + incomes {inr(sum(x for _, x in inc))} = {inr(np_)}.',
            'distractors': [inr(gp - sum(x for _, x in exps) - sum(x for _, x in inc)), inr(gp + sum(x for _, x in exps)), inr(gp)]}


PLACE = [('Carriage inwards', 'Debit side of the trading account'), ('Wages', 'Debit side of the trading account'), ('Opening stock', 'Debit side of the trading account'),
         ('Freight on purchases', 'Debit side of the trading account'), ('Factory lighting', 'Debit side of the trading account'),
         ('Carriage outwards', 'Debit side of the profit and loss account'), ('Salaries', 'Debit side of the profit and loss account'),
         ('Bad debts', 'Debit side of the profit and loss account'), ('Advertisement', 'Debit side of the profit and loss account'),
         ('Office rent', 'Debit side of the profit and loss account'), ('Depreciation', 'Debit side of the profit and loss account'),
         ('Commission received', 'Credit side of the profit and loss account'), ('Discount received', 'Credit side of the profit and loss account'),
         ('Sales less returns', 'Credit side of the trading account'), ('Closing stock (adjusted outside the trial balance)', 'Credit side of the trading account')]
PLACES = ['Debit side of the trading account', 'Credit side of the trading account', 'Debit side of the profit and loss account', 'Credit side of the profit and loss account']


def c8s3_place(r):
    it, pl = r.choice(PLACE)
    return mcq(f'Where is "{it}" shown in the final accounts?', pl, [p for p in PLACES if p != pl], f'{it}: {pl.lower()}.', r)


def c8s3_gp_ratio(r):
    sales = amt(r, 200000, 1000000, 10000)
    pct = r.choice([20, 25, 30, 100 / 3])
    gp = sales * pct / 100
    cogs = sales - gp
    pct_s = '33⅓' if abs(pct - 100 / 3) < 1e-6 else f'{pct:g}'
    if abs(pct - 100 / 3) < 1e-6:
        gp = sales / 3
        cogs = sales - gp
        if sales % 3:
            raise ValueError
    os_ = amt(r, 20000, 100000, 1000)
    pur = cogs + amt(r, 10000, 80000, 1000) - os_
    cs = os_ + pur - cogs
    if pur <= 0 or cs <= 0:
        raise ValueError
    return {'stem': f'Sales were {inr(sales)} and the firm earns a gross profit of {pct_s}% on sales. Opening stock was {inr(os_)} and purchases {inr(pur)}. Find the closing stock.',
            'answer': inr(cs), 'key': f'GP = {pct_s}% of {inr(sales)} = {inr(gp)}; COGS = {inr(cogs)}; closing stock = {inr(os_)} + {inr(pur)} − {inr(cogs)} = {inr(cs)}.'}


CH08_ST3 = dict(
    cat='term',
    terms=[('Gross profit', 'The excess of net sales over the cost of goods sold.'),
           ('Net profit', 'The excess of gross profit plus other incomes over all indirect expenses and losses.'),
           ('Direct expenses', 'Expenses incurred on buying or making goods and bringing them to a saleable condition, such as wages and carriage inwards.'),
           ('Indirect expenses', 'Expenses of running the business, such as office, selling and distribution expenses, charged to the profit and loss account.'),
           ('Cost of goods sold', 'Opening stock plus net purchases plus direct expenses minus closing stock.')],
    ars=[
        ('Carriage inwards is debited to the trading account.', 'It is a direct expense incurred to bring goods to the business.', 'a', 'Both true and R explains A.'),
        ('Carriage outwards is debited to the trading account.', 'Carriage outwards is a selling expense.', 'd', 'A is false: it goes to the profit and loss account. R is true.'),
        ('Gross profit is transferred to the profit and loss account.', 'Net profit is found after deducting indirect expenses from gross profit.', 'a', 'Both true and R explains A.'),
        ('Closing stock given outside the trial balance appears in the trading account and the balance sheet.', 'Every adjustment is recorded at two places.', 'a', 'Both true and R explains A.')],
)


def c8s4_op(r):
    d = ctx(r)
    np_ = amt(r, 50000, 300000, 1000)
    loss_sale = amt(r, 1000, 20000, 500)
    int_loan = amt(r, 2000, 20000, 500)
    div = amt(r, 1000, 15000, 500)
    gain = amt(r, 1000, 15000, 500)
    op = np_ + loss_sale + int_loan - div - gain
    return {'stem': f'{d["f"]} shows a net profit of {inr(np_)} after considering: loss on sale of furniture {inr(loss_sale)}, interest on long-term loan {inr(int_loan)}, dividend received {inr(div)}, profit on sale of an old machine {inr(gain)}. Calculate the operating profit (EBIT basis: before interest and non-operating items).',
            'answer': inr(op),
            'key': f'Operating profit = net profit + non-operating expenses/losses − non-operating incomes/gains = {inr(np_)} + {inr(loss_sale)} + {inr(int_loan)} − {inr(div)} − {inr(gain)} = {inr(op)}.',
            'distractors': [inr(np_ - loss_sale - int_loan + div + gain), inr(np_), inr(np_ + loss_sale + int_loan + div + gain)]}


BS_ITEMS = [('Goodwill', 'Non-current asset'), ('Land and building', 'Non-current asset'), ('Plant and machinery', 'Non-current asset'), ('Furniture', 'Non-current asset'),
            ('Long-term investments', 'Non-current asset'), ('Stock', 'Current asset'), ('Debtors', 'Current asset'), ('Bills receivable', 'Current asset'),
            ('Prepaid expenses', 'Current asset'), ('Cash at bank', 'Current asset'), ('Creditors', 'Current liability'), ('Bills payable', 'Current liability'),
            ('Outstanding expenses', 'Current liability'), ('Bank overdraft', 'Current liability'), ('Loan from bank repayable after 5 years', 'Long-term liability'),
            ('Capital', 'Capital (owner\'s equity)')]


def c8s4_order(r):
    good = r.choice(['Goodwill, Land and building, Plant and machinery, Furniture, Stock, Debtors, Cash',
                     'Cash, Debtors, Stock, Furniture, Plant and machinery, Land and building, Goodwill'])
    liq = good.startswith('Cash')
    wrong = ['Stock, Cash, Goodwill, Debtors, Furniture, Land and building, Plant and machinery',
             'Debtors, Goodwill, Cash, Plant and machinery, Stock, Furniture, Land and building',
             'Land and building, Cash, Stock, Goodwill, Debtors, Plant and machinery, Furniture']
    return mcq(f'Which list shows assets marshalled in the order of {"liquidity" if liq else "permanence"}?', good, wrong,
               f'Order of {"liquidity: most liquid (cash) first" if liq else "permanence: most permanent (goodwill) first"}.', r)


def c8s4_class(r):
    it, cl = r.choice(BS_ITEMS)
    opts = ['Non-current asset', 'Current asset', 'Current liability', 'Long-term liability', 'Capital (owner\'s equity)']
    return mcq(f'In the balance sheet of a sole trader, "{it}" is grouped as …', cl, r.sample([o for o in opts if o != cl], 3), f'{it}: {cl.lower()}.', r)


def c8s4_bs(r):
    d = ctx(r)
    fa = [('Machinery', amt(r, 50000, 300000, 1000)), ('Furniture', amt(r, 10000, 80000, 1000))]
    ca = [('Stock', amt(r, 20000, 150000, 1000)), ('Debtors', amt(r, 20000, 150000, 1000)), ('Cash', amt(r, 5000, 60000, 1000))]
    cl = [('Creditors', amt(r, 20000, 120000, 1000)), ('Bills payable', amt(r, 5000, 30000, 1000))]
    loan = amt(r, 0, 100000, 10000)
    opcap = amt(r, 100000, 300000, 10000)
    np_ = amt(r, 20000, 120000, 1000)
    tot_a = sum(x for _, x in fa + ca)
    dr = opcap + np_ + loan + sum(x for _, x in cl) - tot_a
    if dr <= 0 or dr > np_:
        raise ValueError
    tot = tot_a
    lines = ', '.join(f'{n} {inr(x)}' for n, x in fa + ca + cl) + (f', long-term bank loan {inr(loan)}' if loan else '') + f', capital (1 April) {inr(opcap)}, net profit {inr(np_)}, drawings {inr(dr)}'
    return {'stem': f'Prepare the balance sheet of {d["f"]} as on 31 March 2026 from: {lines}. Find the closing capital and the balance sheet total.',
            'answer': f'Closing capital {inr(opcap + np_ - dr)}; total {inr(tot)}',
            'key': f'Capital {inr(opcap)} + profit {inr(np_)} − drawings {inr(dr)} = {inr(opcap + np_ - dr)}; liabilities side = capital + loan + creditors + bills payable = {inr(tot)}; assets side = {inr(tot)}.'}


CH08_ST4 = dict(
    cat='term',
    terms=[('Grouping', 'Putting items of a similar nature under a common heading in the balance sheet, such as current assets.'),
           ('Marshalling', 'Arranging assets and liabilities in a particular order, either of liquidity or of permanence.'),
           ('Order of liquidity', 'Assets listed starting from the most liquid (cash) and liabilities from those payable first.'),
           ('Order of permanence', 'Assets listed starting from the most permanent (goodwill, land) and liabilities from capital.'),
           ('Operating profit', 'Profit earned from the normal operations of the business, before interest and tax and excluding non-operating items.')],
    pairs=[('current assets', 'non-current assets', [
        ('purpose', 'held for conversion into cash within the operating cycle', 'held for long-term use in the business'),
        ('period', 'realised within a year', 'used for more than a year'),
        ('examples', 'stock, debtors, cash', 'land, machinery, furniture')])],
    ars=[
        ('Operating profit excludes interest on long-term loans.', 'Interest is a financing cost, not an operating expense.', 'a', 'Both true and R explains A.'),
        ('Goodwill is shown first when assets are marshalled in order of liquidity.', 'Goodwill is the least liquid asset.', 'd', 'A is false: it is shown last in order of liquidity. R is true.'),
        ('Net profit is added to capital in the balance sheet.', 'Profit belongs to the owner.', 'a', 'Both true and R explains A.')],
)


def c8s5_opening(r):
    d = ctx(r)
    assets = [('Cash', amt(r, 5000, 50000, 500)), ('Bank', amt(r, 10000, 100000, 1000)), ('Debtors', amt(r, 10000, 100000, 1000)),
              ('Stock', amt(r, 20000, 150000, 1000)), ('Furniture', amt(r, 10000, 80000, 1000)), ('Machinery', amt(r, 50000, 300000, 5000))]
    assets = r.sample(assets, 5)
    liabs = [('Creditors', amt(r, 10000, 90000, 1000)), ('Bills payable', amt(r, 5000, 30000, 1000))]
    cap = sum(x for _, x in assets) - sum(x for _, x in liabs)
    if cap <= 0:
        raise ValueError
    lines = ', '.join(f'{n} {inr(x)}' for n, x in assets + liabs)
    ent = entry([(f'{n} A/c', x) for n, x in assets], [(f'{n} A/c', x) for n, x in liabs] + [('Capital A/c', cap)])
    return {'stem': f'On 1 April 2025 the books of {d["f"]} showed: {lines}. Pass the opening entry and find the capital.',
            'answer': f'Capital {inr(cap)}. {ent}',
            'key': f'Assets debited, liabilities credited, capital is the balancing figure {inr(cap)}: {ent}.'}


def c8s5_closing(r):
    pairs = [('Trading A/c Dr; To Opening Stock A/c, Purchases A/c, Wages A/c, Carriage Inwards A/c', 'transfer of opening stock, purchases and direct expenses'),
             ('Sales A/c Dr; Closing Stock A/c Dr; To Trading A/c', 'transfer of sales and recording of closing stock'),
             ('Trading A/c Dr; To Profit and Loss A/c', 'transfer of gross profit'),
             ('Profit and Loss A/c Dr; To Salaries A/c, Rent A/c, Advertisement A/c', 'transfer of indirect expenses'),
             ('Commission Received A/c Dr; To Profit and Loss A/c', 'transfer of indirect incomes'),
             ('Profit and Loss A/c Dr; To Capital A/c', 'transfer of net profit'),
             ('Capital A/c Dr; To Drawings A/c', 'transfer of drawings')]
    e, p = r.choice(pairs)
    return mcq(f'Which closing entry is passed for {p}?', e, [x for x, y in r.sample([q for q in pairs if q[1] != p], 3)], f'{p[0].upper() + p[1:]}: {e}.', r)


CH08_ST5 = dict(
    cat='term',
    terms=[('Opening entry', 'The journal entry passed at the start of a new year to bring forward the balances of assets, liabilities and capital.'),
           ('Closing entries', 'Journal entries passed at the end of the year to transfer nominal accounts to the trading and profit and loss account.'),
           ('Adjusting entries', 'Entries passed at the end of the year to record outstanding, prepaid and accrued items, depreciation and provisions.'),
           ('Nominal accounts', 'Accounts of expenses, losses, incomes and gains, which are closed at the year end by transfer to the trading or profit and loss account.')],
    ars=[
        ('Nominal accounts are closed by closing entries.', 'Nominal accounts relate to one accounting period.', 'a', 'Both true and R explains A.'),
        ('Real and personal accounts are closed by transfer to the profit and loss account.', 'Their balances are carried forward to the next year.', 'd', 'A is false: they are balanced and carried forward. R is true.'),
        ('Capital is the balancing figure in an opening entry.', 'Capital is the excess of assets over liabilities.', 'a', 'Both true and R explains A.')],
    tf=('opening and closing entries', [
        'Drawings are transferred to the capital account at the end of the year.',
        'Net profit is transferred to the capital account.',
        'In the opening entry, assets are debited and liabilities credited.'], [
        'Asset accounts are closed by transfer to the trading account.',
        'Drawings are transferred to the profit and loss account.',
        'In the opening entry, capital is debited.',
        'Closing entries are passed at the beginning of the year.']),
)


# ---------------- ch09 adjustments

def c9s1_outstanding(r):
    d = ctx(r)
    paid = amt(r, 20000, 150000, 500)
    out = amt(r, 1000, paid // 6, 500)
    head = r.choice(['Salaries', 'Wages', 'Rent'])
    where = 'trading account' if head == 'Wages' else 'profit and loss account'
    return {'stem': f'The trial balance of {d["f"]} shows {head.lower()} paid {inr(paid)}. {head} of {inr(out)} are outstanding at the year end. What amount is charged to the {where} and how is the outstanding amount shown in the balance sheet?',
            'answer': f'{inr(paid + out)} to the {where}; {inr(out)} as a current liability',
            'key': f'{head} = {inr(paid)} + {inr(out)} = {inr(paid + out)} (debit {where}); outstanding {head.lower()} {inr(out)} on the liabilities side.',
            'distractors': [f'{inr(paid - out)} to the {where}; {inr(out)} as a current asset', f'{inr(paid)} to the {where}; {inr(out)} as a current liability',
                            f'{inr(paid + out)} to the {where}; {inr(out)} as a current asset']}


def c9s1_prepaid(r):
    d = ctx(r)
    m_pre = r.choice([3, 4, 6, 9])
    prem = amt(r, 12000, 120000, 1200)
    start = {3: '1 July 2025', 4: '1 August 2025', 6: '1 October 2025', 9: '1 January 2026'}[m_pre]
    pre = prem * m_pre / 12
    return {'stem': f'{d["f"]} paid an annual insurance premium of {inr(prem)} on {start} (year ends 31 March 2026). Find the prepaid insurance and the amount charged to the profit and loss account.',
            'answer': f'Prepaid {inr(pre)}; charged {inr(prem - pre)}',
            'key': f'Premium covers 12 months from {start}; {m_pre} months fall in the next year: prepaid = {inr(prem)} × {m_pre}/12 = {inr(pre)} (current asset); P&L = {inr(prem - pre)}.',
            'distractors': [f'Prepaid {inr(prem - pre)}; charged {inr(pre)}', f'Prepaid nil; charged {inr(prem)}', f'Prepaid {inr(pre)}; charged {inr(prem)}']}


def c9s1_closing_stock(r):
    d = ctx(r)
    cs = amt(r, 20000, 150000, 500)
    inside = r.random() < 0.5
    if inside:
        good = 'Only on the assets side of the balance sheet'
        txt = 'appears inside the trial balance (purchases already adjusted for it)'
    else:
        good = 'On the credit side of the trading account and on the assets side of the balance sheet'
        txt = 'is given as an adjustment outside the trial balance'
    wrong = ['Only on the credit side of the trading account', 'On the debit side of the trading account and the liabilities side of the balance sheet',
             'Only on the assets side of the balance sheet', 'On the credit side of the trading account and on the assets side of the balance sheet']
    return mcq(f'Closing stock of {inr(cs)} {txt}. Where will it be shown?', good, [w for w in wrong if w != good][:3],
               'An item inside the trial balance is shown once (balance sheet); an adjustment outside it is shown twice.', r)


CH09_ST1 = dict(
    cat='term',
    terms=[('Outstanding expenses', 'Expenses that relate to the current year but have not been paid by its end; shown as a current liability.'),
           ('Prepaid expenses', 'Expenses paid in advance for a future period; shown as a current asset.'),
           ('Closing stock', 'The value of unsold goods at the end of the year, at cost or net realisable value, whichever is lower.'),
           ('Adjustments', 'Changes made at the year end so that the final accounts show the true profit and the true financial position.')],
    lists=[('need', 'reasons why adjustments are needed in final accounts', [
        ('To follow the matching concept', 'Revenues and expenses of the year are matched.'),
        ('To follow the accrual basis', 'Incomes earned and expenses incurred are recorded whether or not received or paid.'),
        ('To show the true profit', 'Profit is neither overstated nor understated.'),
        ('To show the true financial position', 'Outstanding, prepaid and accrued items appear in the balance sheet.')], None)],
    ars=[
        ('Outstanding salary is added to salaries in the profit and loss account.', 'It is an expense of the current year that is still unpaid.', 'a', 'Both true and R explains A.'),
        ('Prepaid insurance is shown on the liabilities side.', 'Prepaid insurance gives benefit in the next year.', 'd', 'A is false: it is a current asset. R is true.'),
        ('Each adjustment appears at two places in the final accounts.', 'Adjustments follow the dual aspect concept.', 'a', 'Both true and R explains A.')],
)


def c9s2_accrued(r):
    d = ctx(r)
    if r.random() < 0.5:
        inv = amt(r, 50000, 300000, 10000)
        rate = r.choice([6, 8, 9, 10, 12])
        recd = inv * rate / 100 * r.choice([6, 9]) / 12
        due = inv * rate / 100
        acc_ = due - recd
        return {'stem': f'{d["f"]} holds investments of {inr(inv)} at {rate}% interest per annum. Interest received during the year is {inr(recd)}. Find the accrued interest and the amount credited to the profit and loss account.',
                'answer': f'Accrued {inr(acc_)}; P&L {inr(due)}',
                'key': f'Interest due for the year = {rate}% of {inr(inv)} = {inr(due)}; accrued = {inr(due)} − {inr(recd)} = {inr(acc_)} (current asset).'}
    rent = amt(r, 30000, 200000, 1200)
    adv = rent * r.choice([1, 2, 3]) / 12
    return {'stem': f'{d["f"]} received rent of {inr(rent + adv)} during the year, which includes {inr(adv)} for the next year. What amount is credited to the profit and loss account, and how is {inr(adv)} shown?',
            'answer': f'{inr(rent)}; {inr(adv)} as a current liability (income received in advance)',
            'key': f'Rent of the year = {inr(rent + adv)} − {inr(adv)} = {inr(rent)}; rent received in advance {inr(adv)} on the liabilities side.'}


def c9s2_mcq(r):
    good, wrong = r.choice([
        ('Current asset', 'accrued income'), ('Current liability', 'income received in advance'), ('Current asset', 'prepaid expenses'), ('Current liability', 'outstanding expenses')])
    others = ['Current asset', 'Current liability', 'Non-current asset', 'Capital']
    return mcq(f'In the balance sheet, {wrong} is shown as a …', good, [o for o in others if o != good], f'{wrong[0].upper() + wrong[1:]}: {good.lower()}.', r)


CH09_ST2 = dict(
    cat='term',
    terms=[('Accrued income', 'Income earned during the year but not yet received; shown as a current asset.'),
           ('Income received in advance', 'Income received during the year that relates to the next year; shown as a current liability.'),
           ('Outstanding expense', 'An expense of the current year that remains unpaid at its end.'),
           ('Prepaid expense', 'An expense paid during the year for a period falling in the next year.')],
    ars=[
        ('Accrued interest is shown on the assets side.', 'It is an amount receivable by the business.', 'a', 'Both true and R explains A.'),
        ('Rent received in advance is added to rent received in the profit and loss account.', 'It relates to the next year.', 'd', 'A is false: it is deducted. R is true.'),
        ('Income received in advance is a liability.', 'The business owes the service or goods for that amount.', 'a', 'Both true and R explains A.')],
    tf=('accrued and advance incomes', [
        'Accrued income is added to the income in the profit and loss account.',
        'Income received in advance is shown on the liabilities side.'], [
        'Accrued income is shown on the liabilities side.',
        'Income received in advance is added to the income of the year.',
        'Accrued income is income received for the next year.']),
)


def c9s3_pdd(r):
    d = ctx(r)
    deb = amt(r, 50000, 300000, 1000)
    bd = amt(r, 1000, 10000, 500)
    fbd = amt(r, 500, 5000, 500)
    rate = r.choice([2, 4, 5, 10])
    old = amt(r, 1000, 15000, 500)
    newp = (deb - fbd) * rate / 100
    charge = bd + fbd + newp - old
    net = deb - fbd - newp
    return {'stem': f'Trial balance of {d["f"]}: debtors {inr(deb)}, bad debts {inr(bd)}, provision for doubtful debts (old) {inr(old)}. Adjustments: write off further bad debts {inr(fbd)}; maintain a provision for doubtful debts at {rate}% on debtors. Find the amount charged to the profit and loss account and the net debtors in the balance sheet.',
            'answer': f'Charged {inr(charge)}{" (credit to P&L)" if charge < 0 else ""}; net debtors {inr(net)}',
            'key': f'New provision = {rate}% of ({inr(deb)} − {inr(fbd)}) = {inr(newp)}. P&L charge = bad debts {inr(bd)} + further {inr(fbd)} + new provision {inr(newp)} − old provision {inr(old)} = {inr(charge)}. Debtors {inr(deb)} − {inr(fbd)} − {inr(newp)} = {inr(net)}.'}


def c9s3_disc(r):
    deb = amt(r, 50000, 300000, 1000)
    rate = r.choice([5, 10])
    disc = r.choice([2, 2.5])
    pdd = deb * rate / 100
    pdisc = (deb - pdd) * disc / 100
    return {'stem': f'Debtors are {inr(deb)}. Create a provision for doubtful debts at {rate}% and a provision for discount on debtors at {disc:g}%. Calculate both provisions.',
            'answer': f'PDD {inr(pdd)}; provision for discount {inr(pdisc)}',
            'key': f'PDD = {rate}% of {inr(deb)} = {inr(pdd)}; discount provision on good debtors ({inr(deb - pdd)}) = {disc:g}% = {inr(pdisc)}.',
            'distractors': [f'PDD {inr(pdd)}; provision for discount {inr(deb * disc / 100)}', f'PDD {inr(pdd)}; provision for discount {inr(pdd * disc / 100)}',
                            f'PDD {inr(deb * disc / 100)}; provision for discount {inr(pdd)}']}


def c9s3_dep(r):
    d = ctx(r)
    m = amt(r, 100000, 500000, 10000)
    f = amt(r, 20000, 100000, 5000)
    rm, rf = r.choice([10, 15, 20]), r.choice([5, 10])
    dep = m * rm / 100 + f * rf / 100
    return {'stem': f'{d["f"]} shows machinery {inr(m)} and furniture {inr(f)} in its trial balance. Charge depreciation on machinery at {rm}% and on furniture at {rf}%. Find the total depreciation and the values shown in the balance sheet.',
            'answer': f'Depreciation {inr(dep)}; machinery {inr(m * (100 - rm) / 100)}, furniture {inr(f * (100 - rf) / 100)}',
            'key': f'Machinery {rm}% = {inr(m * rm / 100)}; furniture {rf}% = {inr(f * rf / 100)}; total {inr(dep)} to the P&L (debit); assets shown net.'}


CH09_ST3 = dict(
    cat='term',
    terms=[('Bad debts', 'Amounts due from debtors that cannot be recovered and are written off as a loss.'),
           ('Provision for doubtful debts', 'An amount set aside out of profits for debts that may not be recovered in future.'),
           ('Provision for discount on debtors', 'A provision for cash discount likely to be allowed to good debtors for prompt payment.'),
           ('Further bad debts', 'Bad debts discovered after the trial balance is prepared, given as an adjustment.')],
    ars=[
        ('Provision for doubtful debts is calculated after deducting further bad debts.', 'Only debts still considered recoverable need a provision.', 'a', 'Both true and R explains A.'),
        ('Provision for discount is calculated on total debtors before the provision for doubtful debts.', 'Discount is allowed only to debtors who pay.', 'd', 'A is false: it is calculated on good debtors. R is true.'),
        ('Creation of a provision for doubtful debts follows the conservatism concept.', 'Provision is made for expected losses.', 'a', 'Both true and R explains A.')],
)


def c9s4_mgr(r):
    d = ctx(r)
    np_ = amt(r, 110000, 600000, 1100)
    rate = r.choice([5, 10])
    after = r.random() < 0.5
    com = np_ * rate / (100 + rate) if after else np_ * rate / 100
    basis = 'after charging such commission' if after else 'before charging such commission'
    return {'stem': f'The net profit of {d["f"]} before charging the manager\'s commission is {inr(np_)}. The manager is entitled to {rate}% commission on net profit {basis}. Calculate the commission.',
            'answer': inr(round(com, 2)),
            'key': (f'Commission = {inr(np_)} × {rate}/{100 + rate} = {inr(round(com, 2))}' if after else f'Commission = {rate}% of {inr(np_)} = {inr(com)}') + '; debited to P&L, shown as outstanding commission if unpaid.',
            'distractors': [inr(round(np_ * rate / 100, 2)) if after else inr(round(np_ * rate / (100 + rate), 2)), inr(round(np_ * rate / (100 - rate), 2)), inr(round(np_ * rate / 50, 2))]}


def c9s4_ioc(r):
    d = ctx(r)
    cap = amt(r, 200000, 1000000, 10000)
    rate = r.choice([5, 6, 8, 10])
    drw = amt(r, 12000, 60000, 1200)
    rd = r.choice([5, 6, 10])
    ioc = cap * rate / 100
    iod = drw * rd / 100 * 6 / 12
    return {'stem': f'{d["p"]}, owner of {d["f"]}, had capital of {inr(cap)} on 1 April 2025. Interest on capital is allowed at {rate}% p.a. He withdrew {inr(drw)} evenly during the year (assume an average period of 6 months), with interest on drawings at {rd}% p.a. Calculate interest on capital and on drawings.',
            'answer': f'Interest on capital {inr(ioc)}; interest on drawings {inr(iod)}',
            'key': f'IOC = {rate}% of {inr(cap)} = {inr(ioc)} (debit P&L, credit capital). IOD = {inr(drw)} × {rd}% × 6/12 = {inr(iod)} (debit capital/drawings, credit P&L).'}


CH09_ST4 = dict(
    cat='term',
    terms=[('Interest on capital', 'Interest allowed on the owner\'s capital; an expense for the business and added to capital.'),
           ('Interest on drawings', 'Interest charged on amounts withdrawn by the owner; an income for the business and deducted from capital.'),
           ('Manager\'s commission', 'A share of profit paid to the manager as an incentive, calculated before or after charging the commission.'),
           ('Drawings', 'Cash or goods withdrawn by the proprietor for personal use, deducted from capital.')],
    ars=[
        ('Interest on drawings is credited to the profit and loss account.', 'It is a gain for the business, charged to the owner.', 'a', 'Both true and R explains A.'),
        ('Commission on net profit after charging it is calculated as rate/(100 + rate) of the profit before commission.', 'The commission itself reduces the profit on which it is paid.', 'a', 'Both true and R explains A.'),
        ('Interest on capital increases net profit.', 'Interest on capital is credited to the capital account.', 'd', 'A is false: it is an expense and reduces net profit. R is true.')],
)


def _fa(r):
    d = ctx(r)
    v = dict(os=amt(r, 20000, 100000, 1000), pur=amt(r, 200000, 600000, 1000), pr=amt(r, 2000, 10000, 500), wages=amt(r, 10000, 60000, 1000),
             carr=amt(r, 1000, 10000, 500), sal=amt(r, 20000, 80000, 1000), rent=amt(r, 10000, 40000, 1000), ins=amt(r, 2400, 24000, 1200),
             bd=amt(r, 500, 5000, 500), comm=amt(r, 1000, 10000, 500), deb=amt(r, 40000, 200000, 1000), cred=amt(r, 30000, 150000, 1000),
             cash=amt(r, 5000, 50000, 500), furn=amt(r, 10000, 60000, 1000), mach=amt(r, 50000, 300000, 10000), drw=amt(r, 10000, 50000, 1000))
    v['sales'] = v['pur'] + amt(r, 150000, 400000, 1000)
    v['sr'] = amt(r, 2000, 10000, 500)
    adj = dict(cs=amt(r, 30000, 150000, 1000), osw=amt(r, 1000, 8000, 500), pre=v['ins'] * r.choice([3, 6]) / 12, dep=r.choice([10, 15, 20]),
               pdd=r.choice([2, 5]), acc=amt(r, 500, 5000, 500))
    trial_dr = v['os'] + v['pur'] + v['sr'] + v['wages'] + v['carr'] + v['sal'] + v['rent'] + v['ins'] + v['bd'] + v['deb'] + v['cash'] + v['furn'] + v['mach'] + v['drw']
    trial_cr_wo = v['sales'] + v['pr'] + v['comm'] + v['cred']
    cap = trial_dr - trial_cr_wo
    if cap < 50000:
        raise ValueError
    gp = (v['sales'] - v['sr']) - (v['os'] + v['pur'] - v['pr'] + v['wages'] + adj['osw'] + v['carr'] - adj['cs'])
    depm = v['mach'] * adj['dep'] / 100
    pddv = v['deb'] * adj['pdd'] / 100
    np_ = gp + v['comm'] + adj['acc'] - (v['sal'] + v['rent'] + v['ins'] - adj['pre'] + v['bd'] + pddv + depm)
    assets = v['cash'] + v['deb'] - pddv + adj['cs'] + adj['pre'] + adj['acc'] + v['furn'] + v['mach'] - depm
    liab = v['cred'] + adj['osw'] + cap + np_ - v['drw']
    assert abs(assets - liab) < 0.01, (assets, liab)
    return d, v, adj, cap, gp, np_, assets, depm, pddv


def c9s5_full(r):
    d, v, adj, cap, gp, np_, tot, depm, pddv = _retry(_fa, r)
    tb = (f'Debit balances: opening stock {inr(v["os"])}, purchases {inr(v["pur"])}, sales return {inr(v["sr"])}, wages {inr(v["wages"])}, carriage inwards {inr(v["carr"])}, '
          f'salaries {inr(v["sal"])}, rent {inr(v["rent"])}, insurance {inr(v["ins"])}, bad debts {inr(v["bd"])}, debtors {inr(v["deb"])}, cash {inr(v["cash"])}, '
          f'furniture {inr(v["furn"])}, machinery {inr(v["mach"])}, drawings {inr(v["drw"])}. Credit balances: capital {inr(cap)}, sales {inr(v["sales"])}, '
          f'purchases return {inr(v["pr"])}, commission received {inr(v["comm"])}, creditors {inr(v["cred"])}.')
    ad = (f'Adjustments: (a) closing stock {inr(adj["cs"])}; (b) wages outstanding {inr(adj["osw"])}; (c) insurance prepaid {inr(adj["pre"])}; '
          f'(d) depreciation on machinery {adj["dep"]}%; (e) provision for doubtful debts {adj["pdd"]}% on debtors; (f) commission earned but not received {inr(adj["acc"])}.')
    return {'stem': f'From the following trial balance of {d["p"]} ({d["f"]}, {d["c"]}) as on 31 March 2026, prepare the trading and profit and loss account and the balance sheet. {tb} {ad}',
            'answer': f'Gross profit {inr(gp)}; net {"profit" if np_ >= 0 else "loss"} {inr(abs(np_))}; balance sheet total {inr(tot)}',
            'key': (f'Trading: net sales {inr(v["sales"] - v["sr"])}; debit side opening stock, net purchases {inr(v["pur"] - v["pr"])}, wages {inr(v["wages"] + adj["osw"])}, carriage {inr(v["carr"])}; '
                    f'closing stock {inr(adj["cs"])} credited; GP {inr(gp)} (2). P&L: salaries, rent, insurance {inr(v["ins"] - adj["pre"])}, bad debts {inr(v["bd"])}, PDD {inr(pddv)}, '
                    f'depreciation {inr(depm)}; commission {inr(v["comm"] + adj["acc"])}; NP {inr(np_)} (2). Balance sheet: capital {inr(cap)} + NP − drawings {inr(v["drw"])} = {inr(cap + np_ - v["drw"])}; '
                    f'total {inr(tot)} (2).')}


def c9s5_np_only(r):
    d, v, adj, cap, gp, np_, tot, depm, pddv = _retry(_fa, r)
    return {'stem': f'{d["f"]} has a gross profit of {inr(gp)}. Other balances: salaries {inr(v["sal"])}, rent {inr(v["rent"])}, insurance {inr(v["ins"])}, bad debts {inr(v["bd"])}, commission received {inr(v["comm"])}, debtors {inr(v["deb"])}, machinery {inr(v["mach"])}. '
                    f'Adjustments: insurance prepaid {inr(adj["pre"])}; depreciation on machinery {adj["dep"]}%; provision for doubtful debts {adj["pdd"]}% on debtors; commission accrued {inr(adj["acc"])}. Prepare the profit and loss account and find the net profit.',
            'answer': f'Net {"profit" if np_ >= 0 else "loss"} {inr(abs(np_))}',
            'key': f'Expenses: salaries {inr(v["sal"])} + rent {inr(v["rent"])} + insurance {inr(v["ins"] - adj["pre"])} + bad debts {inr(v["bd"])} + PDD {inr(pddv)} + depreciation {inr(depm)}; incomes: GP {inr(gp)} + commission {inr(v["comm"] + adj["acc"])}; NP {inr(np_)}.'}


def c9s5_effect(r):
    good, it = r.choice([
        ('Debit side of the profit and loss account and liabilities side of the balance sheet', 'Outstanding salary'),
        ('Deducted from the expense in the profit and loss account and shown on the assets side', 'Prepaid rent'),
        ('Credit side of the trading account and assets side of the balance sheet', 'Closing stock'),
        ('Added to income in the profit and loss account and shown on the assets side', 'Accrued interest'),
        ('Deducted from income in the profit and loss account and shown on the liabilities side', 'Rent received in advance'),
        ('Debit side of the profit and loss account and deducted from debtors in the balance sheet', 'Provision for doubtful debts')])
    opts = ['Debit side of the profit and loss account and liabilities side of the balance sheet', 'Deducted from the expense in the profit and loss account and shown on the assets side',
            'Credit side of the trading account and assets side of the balance sheet', 'Added to income in the profit and loss account and shown on the assets side',
            'Deducted from income in the profit and loss account and shown on the liabilities side', 'Debit side of the profit and loss account and deducted from debtors in the balance sheet']
    return mcq(f'How is the adjustment "{it}" (given outside the trial balance) treated in the final accounts?', good, r.sample([o for o in opts if o != good], 3), f'{it}: {good.lower()}.', r)


CH09_ST5 = dict(
    ars=[
        ('Adjustments given outside the trial balance are shown at two places in the final accounts.', 'Every adjustment has two aspects.', 'a', 'Both true and R explains A.'),
        ('Outstanding wages are added to wages in the trading account.', 'Wages are a direct expense.', 'b', 'Both true, but R explains only why wages go to the trading account, not why outstanding wages are added.'),
        ('An item that appears in the trial balance is shown at two places in the final accounts.', 'The trial balance contains both aspects of every transaction.', 'd', 'A is false: it is shown only once. R is true.')],
    cases=[('C4', 'D5', 4, '{p} prepared the final accounts of {f} without considering outstanding salary of ₹12,000, prepaid insurance of ₹3,000 and depreciation of ₹20,000. {He} reported a net profit of ₹1,50,000.',
            [('Find the correct net profit.', '₹1,50,000 − ₹12,000 + ₹3,000 − ₹20,000 = ₹1,21,000.'),
             ('Which accounting concepts did {he} ignore?', 'Matching and accrual concepts (and prudence for depreciation): expenses of the year were not matched with revenue.')])],
)


FAMILIES = {
    S + '08-st1': facts(CH08_ST1),
    S + '08-st2': facts(CH08_ST2) + [FF('C1', 'D1', 'mcq', c8s2_classify), FF('C2', 'D2', 'mcq', c8s2_classify), FF('C3', 'D3', 'numerical', c8s2_total, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c8s2_total, marks=3)],
    S + '08-st3': facts(CH08_ST3) + [FF('C2', 'D1', 'mcq', c8s3_place), FF('C2', 'D2', 'mcq', c8s3_place), FF('C3', 'D2', 'numerical', c8s3_cogs, marks=2),
                                     FF('C3', 'D3', 'numerical', c8s3_gp, marks=4, kinds=('m4',)), FF('C3', 'D3', 'numerical', c8s3_np, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'numerical', c8s3_gp_ratio, marks=3, kinds=('m3',)), FF('C4', 'D3', 'numerical', c8s3_np, marks=3),
                                     FF('C3', 'D1', 'numerical', c8s3_cogs, marks=1), FF('C4', 'D5', 'numerical', c8s3_gp_ratio, marks=4)],
    S + '08-st4': facts(CH08_ST4) + [FF('C1', 'D1', 'mcq', c8s4_class), FF('C2', 'D2', 'mcq', c8s4_order), FF('C3', 'D2', 'numerical', c8s4_op, marks=3, kinds=('m3',)),
                                     FF('C3', 'D4', 'multi_step', c8s4_bs, marks=4, kinds=('m4',)), FF('C4', 'D4', 'numerical', c8s4_op, marks=3),
                                     FF('C4', 'D3', 'multi_step', c8s4_bs, marks=4), FF('C2', 'D1', 'mcq', c8s4_class)],
    S + '08-st5': facts(CH08_ST5) + [FF('C2', 'D2', 'mcq', c8s5_closing), FF('C3', 'D3', 'multi_step', c8s5_opening, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c8s5_opening, marks=4, kinds=('m4',)), FF('C3', 'D2', 'mcq', c8s5_closing)],
    S + '09-st1': facts(CH09_ST1) + [FF('C2', 'D2', 'mcq', c9s1_closing_stock), FF('C3', 'D2', 'numerical', c9s1_outstanding, marks=2), FF('C3', 'D3', 'numerical', c9s1_prepaid, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c9s1_prepaid, marks=2), FF('C3', 'D1', 'numerical', c9s1_outstanding, marks=1), FF('C4', 'D4', 'numerical', c9s1_outstanding, marks=2)],
    S + '09-st2': facts(CH09_ST2) + [FF('C2', 'D1', 'mcq', c9s2_mcq), FF('C3', 'D2', 'numerical', c9s2_accrued, marks=2), FF('C3', 'D3', 'numerical', c9s2_accrued, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'numerical', c9s2_accrued, marks=3)],
    S + '09-st3': facts(CH09_ST3) + [FF('C3', 'D2', 'numerical', c9s3_disc, marks=2), FF('C3', 'D3', 'numerical', c9s3_pdd, marks=4, kinds=('m4',)), FF('C3', 'D2', 'numerical', c9s3_dep, marks=2),
                                     FF('C4', 'D4', 'numerical', c9s3_pdd, marks=4), FF('C4', 'D3', 'numerical', c9s3_disc, marks=2), FF('C2', 'D2', 'mcq', c9s3_disc), FF('C3', 'D1', 'mcq', c9s3_disc)],
    S + '09-st4': facts(CH09_ST4) + [FF('C3', 'D2', 'numerical', c9s4_mgr, marks=2), FF('C3', 'D3', 'numerical', c9s4_ioc, marks=3, kinds=('m3',)), FF('C4', 'D4', 'numerical', c9s4_mgr, marks=2),
                                     FF('C4', 'D3', 'numerical', c9s4_ioc, marks=3), FF('C2', 'D2', 'mcq', c9s4_mgr), FF('C3', 'D1', 'mcq', c9s4_mgr)],
    S + '09-st5': facts(CH09_ST5) + [FF('C2', 'D2', 'mcq', c9s5_effect), FF('C1', 'D1', 'mcq', c9s5_effect), FF('C3', 'D4', 'long', c9s5_full, marks=6, kinds=('m6',)),
                                     FF('C4', 'D4', 'long', c9s5_full, marks=6), FF('C3', 'D3', 'numerical', c9s5_np_only, marks=4, kinds=('m4',)),
                                     FF('C4', 'D5', 'long', c9s5_full, marks=6), FF('C4', 'D3', 'numerical', c9s5_np_only, marks=4)],
}


def _retry(f, *a):
    for _ in range(40):
        try:
            return f(*a)
        except ValueError:
            continue
    raise ValueError
