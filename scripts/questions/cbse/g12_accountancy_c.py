"""CBSE class 12 accountancy families, ch07-ch10 (Part B: Financial Statements of a Company, Analysis of Financial
Statements, Accounting Ratios, Cash Flow Statement). Ratios and cash flows are computed from generated data."""
from __future__ import annotations

from fractions import Fraction as Fr

from qbank import mcq, inr, num
from g11_accountancy_kit import facts, FF, ctx, amt, Cyc
from g12_accountancy_a import I, money, retry, q
from g12_accountancy_b import company

S = 'cbse-g12-accountancy-ch'


def pct(x, base, dp=2):
    return num(round(float(Fr(x) * 100 / base), dp), dp) + '%'


def rt(x, dp=2):
    return num(round(float(x), dp), dp) + ':1'


def tm(x, dp=2):
    return num(round(float(x), dp), dp) + ' times'


# ================================================================ ch07 Financial statements of a company

CH07_ST1 = dict(
    cat='term',
    terms=[
        ('Financial statements', 'The balance sheet, statement of profit and loss, cash flow statement and notes that a company prepares at the end of an accounting period.'),
        ('Balance sheet', 'A statement showing the financial position of a company - its equity, liabilities and assets - on a particular date.'),
        ('Statement of profit and loss', 'A statement showing the revenue, expenses and profit or loss of a company for an accounting period.'),
        ('Recorded facts', 'Data in financial statements taken from the accounting records at historical cost.'),
        ('Personal judgements', 'Choices made by accountants, such as the method of depreciation or inventory valuation, that affect financial statements.'),
    ],
    lists=[('nature', 'points describing the nature of financial statements', [
        ('Recorded facts', 'They are based on figures in the books, at original cost.'),
        ('Accounting conventions', 'Conventions such as conservatism and materiality are followed.'),
        ('Postulates', 'Assumptions such as going concern and money measurement are made.'),
        ('Personal judgements', 'Judgements on depreciation, inventory and provisions affect the figures.')], None),
        ('obj', 'objectives of financial statements', [
        ('To provide information about economic resources and obligations', 'Shows assets and liabilities of the company.'),
        ('To provide information about earning capacity', 'Shows profit earned during the period.'),
        ('To provide information about cash flows', 'Helps users judge the ability to generate cash.'),
        ('To judge the effectiveness of management', 'Shows how well resources have been used.'),
        ('To provide information about social activities', 'Disclosure of activities affecting society.')], None)],
    scen=[('Which user of financial statements is described?', ['Shareholders', 'Lenders', 'Suppliers', 'Government', 'Employees'], [
        ('A bank in {c} studies the balance sheet of {f} Ltd before granting a term loan.', 'Lenders', 'Lenders judge repaying capacity and security.'),
        ('{p} holds equity shares of {f} Ltd and checks whether its profit is growing.', 'Shareholders', 'Owners judge profitability and growth.'),
        ('A trade union of {f} Ltd uses the annual report to negotiate a bonus.', 'Employees', 'Employees look at profits for bonus and wages.'),
        ('The tax department examines the statement of profit and loss of {f} Ltd.', 'Government', 'Government uses statements for taxation and policy.'),
        ('A raw material supplier checks the liquidity of {f} Ltd before extending credit.', 'Suppliers', 'Suppliers judge short-term solvency.')], None)],
    ars=[
        ('Financial statements are prepared on the basis of recorded facts.', 'Assets are shown at historical cost in the books.', 'a', 'Both true; R explains A.'),
        ('Financial statements show the exact financial position of a company.', 'They are influenced by personal judgements and conventions.', 'd', 'A is false: they are influenced by judgements, so not exact. R is true.'),
        ('A company must prepare its balance sheet in the form given in Schedule III.', 'Section 129 of the Companies Act, 2013 requires it.', 'a', 'Both true; R explains A.')],
    tf=('financial statements of a company', [
        'They are prepared according to Schedule III of the Companies Act, 2013.',
        'They include notes to accounts.',
        'They are affected by personal judgements.'], [
        'They show assets only at market value.',
        'They are prepared only for the shareholders.',
        'They are not affected by accounting conventions.',
        'The balance sheet is prepared for a period.']),
    cases=[('C4', 'D4', 4, '{p} wants to invest ₹2 lakh in shares of {f} Ltd. A friend says the annual report is enough to decide, because it contains the balance sheet and statement of profit and loss prepared under Schedule III.',
            [('Name two things {p} can learn from these statements.', 'Earning capacity (profit trend) and financial position (assets, liabilities, solvency).'),
             ('Why should {p} not rely on them alone?', 'They are based on historical cost and personal judgements and give no qualitative information such as quality of management.')])],
)

# (item, major head, sub-head)
BS = [
    ('Securities premium', 'Shareholders\' Funds', 'Reserves and Surplus'),
    ('General reserve', 'Shareholders\' Funds', 'Reserves and Surplus'),
    ('Capital reserve', 'Shareholders\' Funds', 'Reserves and Surplus'),
    ('Debit balance of the statement of profit and loss', 'Shareholders\' Funds', 'Reserves and Surplus'),
    ('Capital redemption reserve', 'Shareholders\' Funds', 'Reserves and Surplus'),
    ('Share forfeiture', 'Shareholders\' Funds', 'Share Capital'),
    ('Calls in arrears', 'Shareholders\' Funds', 'Share Capital'),
    ('Equity share capital', 'Shareholders\' Funds', 'Share Capital'),
    ('10% debentures (redeemable after five years)', 'Non-Current Liabilities', 'Long-term Borrowings'),
    ('Long-term loan from a bank', 'Non-Current Liabilities', 'Long-term Borrowings'),
    ('Public deposits (repayable after three years)', 'Non-Current Liabilities', 'Long-term Borrowings'),
    ('Provision for employee benefits (gratuity, long-term)', 'Non-Current Liabilities', 'Long-term Provisions'),
    ('Bank overdraft', 'Current Liabilities', 'Short-term Borrowings'),
    ('Loan repayable on demand', 'Current Liabilities', 'Short-term Borrowings'),
    ('Bills payable', 'Current Liabilities', 'Trade Payables'),
    ('Sundry creditors', 'Current Liabilities', 'Trade Payables'),
    ('Unpaid dividend', 'Current Liabilities', 'Other Current Liabilities'),
    ('Interest accrued on debentures', 'Current Liabilities', 'Other Current Liabilities'),
    ('Calls in advance', 'Current Liabilities', 'Other Current Liabilities'),
    ('Outstanding salaries', 'Current Liabilities', 'Other Current Liabilities'),
    ('Provision for tax', 'Current Liabilities', 'Short-term Provisions'),
    ('Land and building', 'Non-Current Assets', 'Property, Plant and Equipment and Intangible Assets'),
    ('Plant and machinery', 'Non-Current Assets', 'Property, Plant and Equipment and Intangible Assets'),
    ('Goodwill', 'Non-Current Assets', 'Property, Plant and Equipment and Intangible Assets'),
    ('Patents and trademarks', 'Non-Current Assets', 'Property, Plant and Equipment and Intangible Assets'),
    ('Capital work-in-progress', 'Non-Current Assets', 'Property, Plant and Equipment and Intangible Assets'),
    ('Investment in shares of another company held for the long term', 'Non-Current Assets', 'Non-current Investments'),
    ('Loose tools', 'Current Assets', 'Inventories'),
    ('Stock of finished goods', 'Current Assets', 'Inventories'),
    ('Stores and spares', 'Current Assets', 'Inventories'),
    ('Sundry debtors', 'Current Assets', 'Trade Receivables'),
    ('Bills receivable', 'Current Assets', 'Trade Receivables'),
    ('Cheques in hand', 'Current Assets', 'Cash and Cash Equivalents'),
    ('Cash at bank', 'Current Assets', 'Cash and Cash Equivalents'),
    ('Marketable securities held for a short period', 'Current Assets', 'Current Investments'),
    ('Prepaid expenses', 'Current Assets', 'Other Current Assets'),
    ('Accrued interest on investments', 'Current Assets', 'Other Current Assets'),
]
HEADS = ['Shareholders\' Funds', 'Non-Current Liabilities', 'Current Liabilities', 'Non-Current Assets', 'Current Assets']
SUBS = sorted({b[2] for b in BS})
bs_c1, bs_c2, bs_c3 = Cyc(BS), Cyc(BS), Cyc(BS)


def c7_sub(r):
    it, h, sb = bs_c1.next(r)
    same = [x for x in SUBS if x != sb]
    near = [b[2] for b in BS if b[1] == h and b[2] != sb]
    pool = list(dict.fromkeys(near + r.sample(same, len(same))))
    return mcq(f'Under which sub-head is "{it}" shown in the balance sheet of a company as per Schedule III?', sb, pool[:3], f'{it}: {h} → {sb}.', r)


def c7_head(r):
    it, h, sb = bs_c2.next(r)
    return mcq(f'Under which major head is "{it}" shown in the balance sheet of a company as per Schedule III?', h, r.sample([x for x in HEADS if x != h], 3), f'{it}: {h} → {sb}.', r)


def c7_classify3(r):
    its = r.sample(BS, 6)
    lst = ', '.join(f'({i + 1}) {b[0]}' for i, b in enumerate(its))
    ans = '; '.join(f'({i + 1}) {b[1]} – {b[2]}' for i, b in enumerate(its))
    return {'stem': f'Under which major heads and sub-heads will the following items be shown in the balance sheet of a company as per Schedule III of the Companies Act, 2013? {lst}.',
            'answer': ans, 'key': f'½ mark each: {ans}'}


def c7_reserves(r):
    co = company(r)
    sp = amt(r, 20000, 200000, 5000)
    gr = amt(r, 50000, 400000, 10000)
    plb = amt(r, 10000, 150000, 5000) * r.choice([1, 1, -1])
    cr_ = r.choice([0, amt(r, 5000, 40000, 1000)])
    tot = sp + gr + plb + cr_
    sc = amt(r, 500000, 3000000, 100000)
    items = [f'securities premium {inr(sp)}', f'general reserve {inr(gr)}', f'balance in the statement of profit and loss {"(debit) " + inr(-plb) if plb < 0 else inr(plb)}'] + ([f'capital reserve {inr(cr_)}'] if cr_ else [])
    r.shuffle(items)
    return {'stem': f'From the following, calculate the amount shown under "Reserves and Surplus" and under "Shareholders\' Funds" in the balance sheet of {co}: equity share capital {inr(sc)}, ' + ', '.join(items) + '.',
            'answer': f'Reserves and Surplus {inr(tot)}; Shareholders\' Funds {inr(tot + sc)}',
            'key': f'Reserves and Surplus = {inr(sp)} + {inr(gr)} {"−" if plb < 0 else "+"} {inr(abs(plb))}' + (f' + {inr(cr_)}' if cr_ else '') + f' = {inr(tot)}' + (' (a debit balance of the statement of P&L is shown as a negative item)' if plb < 0 else '') + f'; Shareholders\' Funds = {inr(sc)} + {inr(tot)} = {inr(tot + sc)}.',
            'distractors': [f'Reserves and Surplus {inr(tot + 2 * abs(plb))}; Shareholders\' Funds {inr(tot + sc + 2 * abs(plb))}', f'Reserves and Surplus {inr(tot - sp)}; Shareholders\' Funds {inr(tot + sc - sp)}', f'Reserves and Surplus {inr(tot)}; Shareholders\' Funds {inr(tot)}']}


def c7_sharecap(r):
    co = company(r)
    auth = amt(r, 100000, 500000, 50000)
    iss = amt(r, auth // 2, auth, 10000)
    sub = amt(r, iss // 2, iss, 1000)
    arr = amt(r, 100, 3000, 100) * 2
    pu = sub * 10 - arr
    return {'stem': f'{co} has an authorised capital of {q(auth)} equity shares of ₹10 each. It issued {q(iss)} shares, of which {q(sub)} were subscribed and fully called up. Calls of ₹2 per share on {q(arr // 2)} shares remained unpaid. Show the share capital in the notes to accounts.',
            'answer': f'Authorised capital {inr(auth * 10)}; issued capital {inr(iss * 10)}; subscribed capital: subscribed and fully paid {q(sub - arr // 2)} shares {inr((sub - arr // 2) * 10)}' + (f', subscribed but not fully paid {q(arr // 2)} shares {inr(arr // 2 * 10)} less calls in arrears {inr(arr)} = {inr(arr // 2 * 10 - arr)}' if arr else '') + f'; total {inr(pu)}',
            'key': f'Authorised {q(auth)} × ₹10 = {inr(auth * 10)} (1 mark); issued {q(iss)} × ₹10 = {inr(iss * 10)} (1 mark); subscribed {inr(sub * 10)}' + (f' split into fully paid {inr((sub - arr // 2) * 10)} and not fully paid {inr(arr // 2 * 10)} less calls in arrears {inr(arr)}' if arr else '') + f' (1 mark); total subscribed and paid-up {inr(pu)} (1 mark).'}


PL = [
    ('Sales of goods less sales returns', 'Revenue from Operations'), ('Sale of scrap of a manufacturing company', 'Revenue from Operations'),
    ('Interest received on investments by a trading company', 'Other Income'), ('Dividend received by a manufacturing company', 'Other Income'),
    ('Profit on sale of machinery', 'Other Income'), ('Rent received by a manufacturing company', 'Other Income'),
    ('Raw materials consumed', 'Cost of Materials Consumed'), ('Purchases of goods for resale', 'Purchases of Stock-in-Trade'),
    ('Increase or decrease in stock of finished goods', 'Changes in Inventories of Finished Goods, Work-in-Progress and Stock-in-Trade'),
    ('Salaries and wages', 'Employee Benefits Expense'), ('Contribution to provident fund', 'Employee Benefits Expense'), ('Staff welfare expenses', 'Employee Benefits Expense'),
    ('Interest on debentures', 'Finance Costs'), ('Interest on bank loan', 'Finance Costs'),
    ('Depreciation on machinery', 'Depreciation and Amortisation Expense'), ('Amortisation of patents', 'Depreciation and Amortisation Expense'),
    ('Advertisement expenses', 'Other Expenses'), ('Rent and rates', 'Other Expenses'), ('Loss on sale of furniture', 'Other Expenses'), ('Audit fees', 'Other Expenses'),
]
PLH = sorted({x[1] for x in PL})
pl_c = Cyc(PL)


def c7_pl(r):
    it, h = pl_c.next(r)
    return mcq(f'Under which head is "{it}" shown in the statement of profit and loss of a company as per Schedule III?', h, r.sample([x for x in PLH if x != h], 3), f'{it}: {h}.', r)


def c7_revenue(r):
    co = company(r)
    s_ = amt(r, 1000000, 9000000, 10000)
    ret = amt(r, 10000, s_ // 10, 1000)
    scrap = r.choice([0, amt(r, 5000, 50000, 1000)])
    oi = amt(r, 5000, 80000, 1000)
    rev = s_ - ret + scrap
    return {'stem': f'{co}, a manufacturing company, had sales {inr(s_)}, sales returns {inr(ret)}' + (f', sale of scrap {inr(scrap)}' if scrap else '') + f' and interest received on investments {inr(oi)}. Calculate revenue from operations and other income.',
            'answer': f'Revenue from operations {inr(rev)}; other income {inr(oi)}',
            'key': f'Revenue from operations = {inr(s_)} − {inr(ret)}' + (f' + scrap {inr(scrap)}' if scrap else '') + f' = {inr(rev)}; interest on investments is other income {inr(oi)}.',
            'distractors': [f'Revenue from operations {inr(rev + oi)}; other income nil', f'Revenue from operations {inr(s_)}; other income {inr(oi)}', f'Revenue from operations {inr(rev + ret)}; other income {inr(oi + scrap)}']}


def c7_materials(r):
    o = amt(r, 50000, 300000, 5000)
    p = amt(r, 300000, 2000000, 10000)
    c = amt(r, 30000, 300000, 5000)
    cm = o + p - c
    return {'stem': f'Opening inventory of raw materials {inr(o)}, purchases of raw materials {inr(p)}, closing inventory of raw materials {inr(c)}. Calculate the cost of materials consumed.',
            'answer': inr(cm), 'key': f'{inr(o)} + {inr(p)} − {inr(c)} = {inr(cm)}.', 'distractors': [inr(p), inr(o + p + c), inr(p - c)]}


CH07_ST2 = dict(
    cat='term',
    terms=[
        ('Schedule III', 'The schedule of the Companies Act, 2013 that prescribes the form of the balance sheet and statement of profit and loss of a company.'),
        ('Current asset', 'An asset expected to be realised, sold or consumed within the operating cycle or twelve months, or held for trading.'),
        ('Operating cycle', 'The time between the acquisition of assets for processing and their realisation in cash or cash equivalents.'),
        ('Current liability', 'A liability expected to be settled within the operating cycle or twelve months after the reporting date.'),
        ('Contingent liability', 'A possible obligation that may or may not arise, disclosed by way of a note to accounts.'),
    ],
    ars=[
        ('Calls in arrears are shown as a deduction from subscribed capital.', 'They are amounts called up but not paid.', 'a', 'Both true; R explains A.'),
        ('Loose tools are shown under Inventories.', 'Schedule III lists loose tools under Inventories.', 'a', 'Both true; R explains A.'),
        ('A debit balance of the statement of profit and loss is shown as an asset.', 'It is shown as a negative figure under Reserves and Surplus.', 'd', 'A is false. R is true.'),
        ('Contingent liabilities are shown in the balance sheet totals.', 'They are disclosed in notes to accounts.', 'd', 'A is false: they are only disclosed in notes. R is true.'),
        ('Unpaid dividend is shown under Other Current Liabilities.', 'It is payable on demand to shareholders.', 'a', 'Both true; R explains A.')],
    tf=('the balance sheet as per Schedule III', [
        'Share forfeiture is added to paid-up capital under Share Capital.',
        'Bank overdraft is shown under Short-term Borrowings.',
        'Prepaid expenses are shown under Other Current Assets.'], [
        'Bills payable are shown under Short-term Borrowings.',
        'Goodwill is shown under Current Assets.',
        'Calls in advance are shown under Share Capital.',
        'Provision for tax is shown under Long-term Provisions.']),
)
CH07_ST3 = dict(
    cat='term',
    terms=[
        ('Revenue from operations', 'Revenue earned from the main operating activities of the company, such as sale of products and services, net of returns.'),
        ('Other income', 'Income from non-operating activities, such as interest, dividend and profit on sale of fixed assets.'),
        ('Finance costs', 'Interest and other borrowing costs, such as interest on debentures and loans.'),
        ('Employee benefits expense', 'Salaries, wages, bonus, contribution to provident fund and staff welfare.'),
        ('Changes in inventories', 'The difference between opening and closing inventories of finished goods, work-in-progress and stock-in-trade.'),
    ],
    ars=[
        ('Interest on debentures is shown under Finance Costs.', 'It is a borrowing cost.', 'a', 'Both true; R explains A.'),
        ('Dividend received by a manufacturing company is revenue from operations.', 'Dividend is not its main operating income.', 'd', 'A is false: it is other income. R is true.'),
        ('Contribution to provident fund is an employee benefits expense.', 'It is paid for the benefit of employees.', 'a', 'Both true; R explains A.')],
    tf=('the statement of profit and loss', [
        'Profit on sale of machinery is shown as other income.',
        'Depreciation is shown as a separate expense head.',
        'Interest on bank loan is a finance cost.'], [
        'Interest on debentures is shown under Other Expenses.',
        'Sales returns are added to revenue from operations.',
        'Dividend received by a manufacturing company is revenue from operations.',
        'Salaries are shown under Other Expenses.']),
)
CH07_ST4 = dict(
    cat='term',
    terms=[
        ('Notes to accounts', 'Detailed information supporting the items in the balance sheet and statement of profit and loss, forming part of the financial statements.'),
        ('Historical cost', 'The original cost at which an asset is recorded, ignoring changes in price level.'),
        ('Window dressing', 'Presenting financial statements to show a better position than the actual one.'),
        ('Qualitative information', 'Information such as efficiency of management or employee relations that financial statements cannot show.'),
    ],
    lists=[('lim', 'limitations of financial statements', [
        ('They do not reflect current situation', 'Figures are at historical cost and ignore price changes.'),
        ('Assets may not realise the stated values', 'Book values may differ from realisable values.'),
        ('They are affected by personal bias', 'Judgements on depreciation and inventory differ.'),
        ('They lack qualitative information', 'Quality of management and labour relations are not shown.'),
        ('They are only interim reports', 'Actual profit is known only on winding up.'),
        ('They are affected by window dressing', 'Figures may be manipulated to look better.')], None)],
    ars=[
        ('Financial statements ignore changes in price level.', 'Assets are recorded at historical cost.', 'a', 'Both true; R explains A.'),
        ('Notes to accounts form part of financial statements.', 'Schedule III requires detailed notes for many items.', 'a', 'Both true; R explains A.'),
        ('Financial statements show the qualitative aspects of a business.', 'They show only monetary information.', 'd', 'A is false. R is true.')],
    tf=('limitations of financial statements', [
        'They do not show qualitative information.',
        'They are based on historical cost.',
        'They may be affected by window dressing.'], [
        'They always show the realisable value of assets.',
        'They are free from personal judgement.',
        'They show the effect of inflation on assets.',
        'They show the efficiency of management directly.']),
    scen=[('Which limitation of financial statements is illustrated?', ['They do not reflect current situation', 'They lack qualitative information', 'They are affected by personal bias', 'They are affected by window dressing'], [
        ('Land bought by {f} Ltd in 1995 for ₹10 lakh is still shown at ₹10 lakh although it is now worth ₹2 crore.', 'They do not reflect current situation', 'Historical cost ignores price changes.'),
        ('The balance sheet of {f} Ltd says nothing about its excellent labour relations and skilled managers.', 'They lack qualitative information', 'Non-monetary factors are not shown.'),
        ('Two accountants of {f} Ltd charge depreciation by different methods and report different profits.', 'They are affected by personal bias', 'Choice of method changes the figures.'),
        ('{f} Ltd delays paying creditors at the year end so that its cash balance looks large.', 'They are affected by window dressing', 'Figures are made to look better.')], None)],
    cases=[('C4', 'D4', 4, '{f} Ltd shows a building bought twenty years ago at its cost less depreciation. Its managers are known for poor relations with workers, but the annual report shows a high profit.',
            [('Identify two limitations of financial statements here.', 'They do not reflect the current value of assets (historical cost); they lack qualitative information (labour relations).'),
             ('Why do notes to accounts help users?', 'They give details of items, accounting policies and contingent liabilities that support the figures.')])],
)

# ================================================================ ch08 Analysis

CH08_ST1 = dict(
    cat='term',
    terms=[
        ('Financial statement analysis', 'The process of identifying the financial strengths and weaknesses of a firm by establishing relationships between items of the financial statements.'),
        ('Horizontal analysis', 'Comparison of financial statements of a firm for a number of years, also called dynamic analysis.'),
        ('Vertical analysis', 'Analysis of the financial statements of a single year, relating items to a common base; also called static analysis.'),
        ('External analysis', 'Analysis done by outsiders such as investors and creditors, based on published statements.'),
        ('Internal analysis', 'Analysis done by persons inside the firm who have access to the books of account.'),
    ],
    lists=[('obj', 'objectives of analysis of financial statements', [
        ('To assess the earning capacity', 'Profitability of the firm is judged.'),
        ('To assess the managerial efficiency', 'Efficiency in using resources is judged.'),
        ('To assess the short-term and long-term solvency', 'Ability to pay current and long-term obligations is judged.'),
        ('To make inter-firm comparison', 'Performance is compared with other firms.'),
        ('To forecast and prepare budgets', 'Past trends help in planning.'),
        ('To understand complicated matter', 'Data are simplified for decision-making.')], 'lim'),
        ('lim', 'limitations of financial statement analysis', [
        ('Ignores price-level changes', 'Figures are at historical cost.'),
        ('Affected by window dressing', 'Manipulated figures distort the analysis.'),
        ('Ignores qualitative aspects', 'Non-monetary factors are not considered.'),
        ('Affected by personal bias', 'Analysis depends on the analyst\'s judgement.'),
        ('Inter-firm comparison is difficult', 'Firms follow different accounting policies.')], 'obj')],
    pairs=[('horizontal analysis', 'vertical analysis', [
        ('period', 'statements of several years are compared', 'statement of one year is analysed'),
        ('other name', 'dynamic analysis', 'static analysis'),
        ('tool', 'comparative statements and trend analysis', 'common-size statements'),
        ('purpose', 'to study changes over time', 'to study the relationship of items in one period')])],
    ars=[
        ('Analysis of financial statements helps in inter-firm comparison.', 'Ratios bring figures of different firms to a common base.', 'a', 'Both true; R explains A.'),
        ('Financial analysis is free from the limitations of financial statements.', 'Analysis is based on the figures in financial statements.', 'd', 'A is false: it shares their limitations. R is true.'),
        ('Vertical analysis is also called static analysis.', 'It studies statements of one year only.', 'a', 'Both true; R explains A.')],
    tf=('analysis of financial statements', [
        'Horizontal analysis compares several years.',
        'Common-size statements are a tool of vertical analysis.',
        'Analysis is affected by price-level changes.'], [
        'Vertical analysis compares several years.',
        'Analysis removes window dressing from statements.',
        'Analysis considers qualitative factors fully.',
        'Comparative statements are a tool of vertical analysis.']),
    scen=[('Which type of financial analysis is this?', ['Horizontal analysis', 'Vertical analysis', 'External analysis', 'Internal analysis'], [
        ('A bank examines the published balance sheet of {f} Ltd to decide on a loan.', 'External analysis', 'Done by an outsider from published statements.'),
        ('The finance manager of {f} Ltd analyses detailed cost records of each department.', 'Internal analysis', 'Done by insiders with access to the books.'),
        ('{p} compares the sales of {f} Ltd for 2023-24, 2024-25 and 2025-26.', 'Horizontal analysis', 'Several years are compared.'),
        ('{p} expresses each expense of {f} Ltd for 2025-26 as a percentage of revenue from operations.', 'Vertical analysis', 'One year\'s items related to a common base.')], None)],
    cases=[('C4', 'D4', 4, '{p}, a shareholder of {f} Ltd, finds that profit rose by ₹20 lakh this year but cannot tell whether this is good, because revenue doubled and the company issued new shares.',
            [('What kind of analysis will help {p}? Why?', 'Analysis using ratios and comparative statements, because absolute figures alone do not show relative performance.'),
             ('State two limitations {p} should keep in mind.', 'Price-level changes are ignored; window dressing and differences in accounting policies may distort results.')])],
)
CH08_ST4 = dict(
    cat='tool of analysis',
    terms=[
        ('Comparative statements', 'Statements showing figures of two or more periods side by side, with absolute and percentage changes.'),
        ('Common-size statements', 'Statements in which each item is shown as a percentage of a common base such as revenue from operations or total assets.'),
        ('Trend analysis', 'Computing the percentage of each year\'s figure to a base year to study the direction of change over several years.'),
        ('Ratio analysis', 'Calculating the relationship between two related items of financial statements to judge performance.'),
        ('Cash flow analysis', 'Analysing the inflows and outflows of cash and cash equivalents under operating, investing and financing activities.'),
    ],
    scen=[('Which tool of analysis is used?', ['Comparative statements', 'Common-size statements', 'Trend analysis', 'Ratio analysis', 'Cash flow analysis'], [
        ('The analyst of {f} Ltd shows each expense as a percentage of revenue from operations for 2025-26.', 'Common-size statements', 'Items are expressed as percentages of a common base.'),
        ('{p} places the balance sheets of 2024-25 and 2025-26 side by side and computes the change in each item.', 'Comparative statements', 'Two years are compared with absolute and percentage changes.'),
        ('{p} takes 2021-22 as the base year (100) and expresses sales of the next four years as percentages of it.', 'Trend analysis', 'Base-year percentages over several years.'),
        ('{p} divides current assets by current liabilities to judge the liquidity of {f} Ltd.', 'Ratio analysis', 'Relationship between two items.'),
        ('{p} studies cash generated from operations and cash spent on machinery during the year.', 'Cash flow analysis', 'Analysis of cash inflows and outflows.')], None)],
    ars=[
        ('Trend analysis is useful when data for several years are available.', 'It shows the direction of change over time.', 'a', 'Both true; R explains A.'),
        ('Common-size statements help compare firms of different sizes.', 'All items are converted to percentages of a common base.', 'a', 'Both true; R explains A.'),
        ('Ratio analysis is a tool of horizontal analysis only.', 'Ratios can be calculated for one year.', 'd', 'A is false: ratios are used in both. R is true.')],
    tf=('tools of financial analysis', [
        'Comparative statements show absolute and percentage changes.',
        'In a common-size balance sheet, total assets are taken as 100.',
        'Trend analysis uses a base year.'], [
        'In a common-size statement of profit and loss, net profit is taken as 100.',
        'Trend analysis needs data of only one year.',
        'Comparative statements show only percentages.',
        'Cash flow analysis is part of the statement of profit and loss.']),
    cases=[('C4', 'D4', 4, '{f} Ltd has five years of financial statements. The board wants to know (a) whether sales are growing steadily, and (b) how its cost structure compares with a much larger rival.',
            [('Which tool suits (a)? Why?', 'Trend analysis: base-year percentages show the direction of change over several years.'),
             ('Which tool suits (b)? Why?', 'Common-size statements: percentages of revenue make firms of different sizes comparable.')])],
)


def _cmp_pl(r):
    rev = [amt(r, 1000000, 5000000, 50000)]
    rev.append(I(Fr(rev[0] * r.choice([110, 120, 125, 80, 150]), 100)))
    ep = [r.choice([50, 60, 70]), r.choice([50, 60, 70, 75])]
    exp = [I(Fr(rv * e, 100)) for rv, e in zip(rev, ep)]
    oi = [amt(r, 20000, 200000, 10000) for _ in range(2)]
    tax = r.choice([25, 30, 40, 50])
    pbt = [rev[i] + oi[i] - exp[i] for i in range(2)]
    t = [I(Fr(p * tax, 100)) for p in pbt]
    pat = [pbt[i] - t[i] for i in range(2)]
    return rev, exp, oi, tax, pbt, t, pat


def c8_comparative(r):
    co = company(r)
    rev, exp, oi, tax, pbt, t, pat = retry(_cmp_pl, r)
    rows = [('Revenue from operations', rev), ('Other income', oi), ('Expenses', exp), ('Profit before tax', pbt), (f'Tax @ {tax}%', t), ('Profit after tax', pat)]
    body = '; '.join(f'{n}: {inr(v[0])}, {inr(v[1])}, change {"−" if v[1] < v[0] else ""}{inr(abs(v[1] - v[0]))} ({pct(v[1] - v[0], v[0])})' for n, v in rows)
    return {'stem': f'From the following information of {co}, prepare a comparative statement of profit and loss for 2024-25 and 2025-26: revenue from operations {inr(rev[0])} and {inr(rev[1])}; other income {inr(oi[0])} and {inr(oi[1])}; expenses {inr(exp[0])} and {inr(exp[1])}; tax rate {tax}%.',
            'answer': body,
            'key': f'For each line: 2024-25, 2025-26, absolute change, % change. {body}. (1 mark each for revenue/other income, expenses, PBT, tax and PAT lines.)'}


def c8_change_mcq(r):
    a = amt(r, 100000, 2000000, 10000)
    p_ = r.choice([10, 20, 25, 40, 50, -10, -20, 15, 30])
    b = I(Fr(a * (100 + p_), 100))
    it = r.choice(['Revenue from operations', 'Trade receivables', 'Inventories', 'Employee benefits expense', 'Long-term borrowings', 'Cash and cash equivalents'])
    ans = pct(b - a, a)
    return mcq(f'{it} were {inr(a)} in 2024-25 and {inr(b)} in 2025-26. In a comparative statement, the percentage change is:', ans,
               [pct(b - a, b), pct(b, a), pct(a - b, a) if b != a else '0%'], f'Change {inr(b - a)} ÷ base year {inr(a)} × 100 = {ans}.', r)


CH08_ST2 = dict(
    cat='term',
    terms=[
        ('Comparative balance sheet', 'A balance sheet showing the items of two or more dates side by side, with absolute and percentage changes.'),
        ('Comparative statement of profit and loss', 'A statement showing revenue and expenses of two or more years side by side with absolute and percentage changes.'),
        ('Absolute change', 'The difference in rupees between the current-year and previous-year figures of an item.'),
        ('Percentage change', 'Absolute change expressed as a percentage of the previous (base) year figure.'),
    ],
    ars=[
        ('In a comparative statement, the percentage change is computed on the previous year\'s figure.', 'The previous year is the base for comparison.', 'a', 'Both true; R explains A.'),
        ('Comparative statements are a tool of vertical analysis.', 'They compare two or more years.', 'd', 'A is false: they are a tool of horizontal analysis. R is true.'),
        ('A comparative statement shows the trend of change in items.', 'Figures of different years are placed side by side.', 'a', 'Both true; R explains A.')],
    tf=('comparative statements', [
        'Percentage change = absolute change ÷ previous year × 100.',
        'They are a tool of horizontal analysis.',
        'They show increase or decrease in each item.'], [
        'Percentage change is computed on the current year\'s figure.',
        'They are prepared for one year only.',
        'They show each item as a percentage of total assets.',
        'They are a tool of vertical analysis.']),
)
CH08_ST3 = dict(
    cat='term',
    terms=[
        ('Common-size statement of profit and loss', 'A statement in which each item is shown as a percentage of revenue from operations.'),
        ('Common-size balance sheet', 'A balance sheet in which each item is shown as a percentage of total assets (or total equity and liabilities).'),
        ('Common base', 'The figure taken as 100 in a common-size statement.'),
        ('Inter-firm comparison', 'Comparing the performance of different firms, made easier by common-size statements.'),
    ],
    ars=[
        ('In a common-size statement of profit and loss, revenue from operations is taken as 100.', 'Every item is expressed as a percentage of a common base.', 'a', 'Both true; R explains A.'),
        ('Common-size statements cannot be used for inter-firm comparison.', 'They express items as percentages.', 'd', 'A is false: percentages make firms comparable. R is true.'),
        ('In a common-size balance sheet, each asset is shown as a percentage of total assets.', 'Total assets are taken as the common base.', 'a', 'Both true; R explains A.')],
    tf=('common-size statements', [
        'Revenue from operations is the base in a common-size statement of profit and loss.',
        'Total assets are the base in a common-size balance sheet.',
        'They help inter-firm comparison.'], [
        'Net profit is the base in a common-size statement of profit and loss.',
        'Share capital is the base in a common-size balance sheet.',
        'They are a tool of horizontal analysis.',
        'They show absolute changes between two years.']),
)


def c8_commonsize(r):
    co = company(r)
    rev = amt(r, 1000000, 8000000, 100000)
    shares_ = [r.choice([40, 45, 50, 55, 60]), r.choice([5, 8, 10, 12]), r.choice([5, 8, 10, 15])]
    cogs, emp, oth = [I(Fr(rev * s_, 100)) for s_ in shares_]
    tax = r.choice([25, 30, 40, 50])
    pbt = rev - cogs - emp - oth
    t = I(Fr(pbt * tax, 100))
    pat = pbt - t
    if pbt <= 0:
        raise ValueError
    rows = [('Cost of materials consumed', cogs), ('Employee benefits expense', emp), ('Other expenses', oth), ('Profit before tax', pbt), ('Tax', t), ('Profit after tax', pat)]
    body = '; '.join(f'{n} {pct(v, rev)}' for n, v in rows)
    return {'stem': f'Prepare a common-size statement of profit and loss of {co}: revenue from operations {inr(rev)}, cost of materials consumed {inr(cogs)}, employee benefits expense {inr(emp)}, other expenses {inr(oth)}, tax rate {tax}%.',
            'answer': f'Revenue 100%; {body}',
            'key': f'Each item ÷ revenue from operations {inr(rev)} × 100: {body} (½ mark each; correct base 1 mark).'}


def c8_cs_mcq(r):
    tot = amt(r, 1000000, 9000000, 100000)
    p_ = r.choice([5, 8, 10, 12, 15, 20, 25, 30, 35, 40])
    x = I(Fr(tot * p_, 100))
    it = r.choice(['Inventories', 'Trade receivables', 'Long-term borrowings', 'Property, plant and equipment', 'Trade payables', 'Share capital'])
    ans = f'{p_}%'
    return mcq(f'In a common-size balance sheet, {it.lower()} of {inr(x)} with total assets of {inr(tot)} will be shown as:', ans,
               [f'{p_ * 2}%', f'{100 - p_}%', f'{p_ // 2 if p_ % 2 == 0 else p_ + 5}%'], f'{inr(x)} ÷ {inr(tot)} × 100 = {ans}.', r)


# ================================================================ ch09 Ratios

CH09_ST1 = dict(
    cat='term',
    terms=[
        ('Accounting ratio', 'A mathematical relationship between two related items of financial statements, expressed as a pure ratio, percentage or times.'),
        ('Ratio analysis', 'The computation and interpretation of accounting ratios to judge a firm\'s liquidity, solvency, activity and profitability.'),
        ('Liquidity ratios', 'Ratios that measure a firm\'s ability to meet its short-term obligations.'),
        ('Solvency ratios', 'Ratios that measure a firm\'s ability to meet its long-term obligations.'),
        ('Activity ratios', 'Ratios that measure how efficiently a firm uses its resources, also called turnover ratios.'),
        ('Profitability ratios', 'Ratios that measure the profit earned in relation to sales or capital employed.'),
    ],
    lists=[('obj', 'objectives of ratio analysis', [
        ('To know the areas of the business that need more attention', 'Weak areas are identified.'),
        ('To provide a deeper analysis of profitability, liquidity, solvency and efficiency', 'Ratios go beyond absolute figures.'),
        ('To provide information for making cross-sectional analysis', 'Comparison with other firms becomes possible.'),
        ('To provide information for making budgets', 'Past ratios help in planning.')], 'lim'),
        ('lim', 'limitations of ratio analysis', [
        ('Limitations of accounting data', 'Ratios inherit the limitations of financial statements.'),
        ('Ignores price-level changes', 'Inflation affects comparison over years.'),
        ('Ignores qualitative factors', 'Non-monetary aspects are left out.'),
        ('Variations in accounting practices', 'Different methods make comparison difficult.'),
        ('Lack of standard ratios', 'There are no universally accepted ideal ratios.')], 'obj')],
    scen=[('To which category does the ratio belong?', ['Liquidity ratio', 'Solvency ratio', 'Activity ratio', 'Profitability ratio'], [
        ('Current ratio', 'Liquidity ratio', 'Measures short-term solvency.'), ('Quick ratio', 'Liquidity ratio', 'Measures short-term solvency.'),
        ('Debt-equity ratio', 'Solvency ratio', 'Measures long-term solvency.'), ('Proprietary ratio', 'Solvency ratio', 'Measures long-term solvency.'),
        ('Interest coverage ratio', 'Solvency ratio', 'Measures ability to pay interest on long-term debt.'), ('Total assets to debt ratio', 'Solvency ratio', 'Measures long-term solvency.'),
        ('Inventory turnover ratio', 'Activity ratio', 'Measures efficiency of inventory use.'), ('Trade receivables turnover ratio', 'Activity ratio', 'Measures efficiency of collection.'),
        ('Working capital turnover ratio', 'Activity ratio', 'Measures efficiency of working capital.'), ('Gross profit ratio', 'Profitability ratio', 'Measures profit on revenue.'),
        ('Return on investment', 'Profitability ratio', 'Measures return on capital employed.'), ('Operating ratio', 'Profitability ratio', 'Measures operating cost relative to revenue.')], None)],
    ars=[
        ('Ratio analysis helps in inter-firm comparison.', 'Ratios reduce figures to a comparable form.', 'a', 'Both true; R explains A.'),
        ('Ratios are free from the limitations of financial statements.', 'Ratios are calculated from financial statements.', 'd', 'A is false. R is true.'),
        ('Interest coverage ratio is a solvency ratio.', 'It shows the ability to pay interest on long-term borrowings.', 'a', 'Both true; R explains A.')],
    tf=('ratio analysis', [
        'Current ratio is a liquidity ratio.',
        'Ratio analysis ignores price-level changes.',
        'Ratios may be expressed as pure ratios, percentages or times.'], [
        'Debt-equity ratio is a liquidity ratio.',
        'Ratio analysis takes qualitative factors fully into account.',
        'There are universally accepted ideal ratios for every industry.',
        'Inventory turnover ratio is a profitability ratio.']),
    cases=[('C4', 'D4', 4, '{f} Ltd has a current ratio of 4:1 while the industry average is 2:1. Its managers believe this shows excellent performance. Its inventory turnover is much lower than its rivals\'.',
            [('Is the high current ratio necessarily good? Explain.', 'No: it may indicate idle funds, excess inventory or slow collection.'),
             ('Which limitation of ratio analysis should the managers remember?', 'Ratios are only indicators; there is no universal ideal ratio and they ignore qualitative factors (any one with explanation).')])],
)


def _bs(r):
    inv = amt(r, 50000, 400000, 10000)
    tr = amt(r, 50000, 400000, 10000)
    cash = amt(r, 20000, 200000, 10000)
    pre = r.choice([0, amt(r, 5000, 30000, 5000)])
    ca = inv + tr + cash + pre
    cl = amt(r, ca // 4, ca, 10000)
    return inv, tr, cash, pre, ca, cl


def c9_current(r):
    inv, tr, cash, pre, ca, cl = _bs(r)
    cr = Fr(ca, cl)
    qa = ca - inv - pre
    qr = Fr(qa, cl)
    which = r.choice(['current', 'quick', 'both'])
    data = f'inventories {inr(inv)}, trade receivables {inr(tr)}, cash and cash equivalents {inr(cash)}' + (f', prepaid expenses {inr(pre)}' if pre else '') + f', current liabilities {inr(cl)}'
    ans = {'current': f'Current ratio {rt(cr)}', 'quick': f'Quick ratio {rt(qr)}', 'both': f'Current ratio {rt(cr)}; quick ratio {rt(qr)}'}[which]
    ask = {'current': 'the current ratio', 'quick': 'the quick ratio', 'both': 'the current ratio and the quick ratio'}[which]
    return {'stem': f'Calculate {ask} from: {data}.', 'answer': ans,
            'key': f'Current assets {inr(ca)}; current ratio = {inr(ca)}/{inr(cl)} = {rt(cr)}. Quick assets = {inr(ca)} − inventories {inr(inv)}' + (f' − prepaid {inr(pre)}' if pre else '') + f' = {inr(qa)}; quick ratio = {rt(qr)}.',
            'distractors': [f'Current ratio {rt(Fr(cl, ca))}' if which == 'current' else f'Quick ratio {rt(Fr(ca - inv, cl))}' if pre else f'Quick ratio {rt(Fr(qa + inv // 2, cl))}',
                            f'Current ratio {rt(Fr(qa, cl))}' if which == 'current' else f'Quick ratio {rt(cr)}',
                            f'Current ratio {rt(Fr(ca + cl, cl))}' if which == 'current' else f'Quick ratio {rt(Fr(cl, qa))}']}


def c9_current_mcq(r):
    v = c9_current(r)
    if ';' in v['answer']:
        raise ValueError
    return mcq(v['stem'].replace('Calculate', 'Find'), v['answer'], v['distractors'], v['key'], r)


def c9_reverse(r):
    cr = r.choice([Fr(2), Fr(5, 2), Fr(3), Fr(3, 2), Fr(9, 4), Fr(11, 4)])
    cl = amt(r, 50000, 500000, 20000)
    ca = I(cl * cr)
    wc = ca - cl
    mode = r.choice(['wc', 'qr'])
    if mode == 'wc':
        return {'stem': f'The current ratio of a company is {rt(cr)} and its working capital is {inr(wc)}. Calculate its current assets and current liabilities.',
                'answer': f'Current assets {inr(ca)}; current liabilities {inr(cl)}',
                'key': f'CA − CL = {inr(wc)} and CA = {num(float(cr))} CL, so {num(float(cr) - 1)} CL = {inr(wc)}; CL = {inr(cl)}; CA = {inr(ca)}.',
                'distractors': [f'Current assets {inr(wc)}; current liabilities {inr(cl)}', f'Current assets {inr(cl)}; current liabilities {inr(ca)}', f'Current assets {inr(ca + wc)}; current liabilities {inr(cl + wc)}']}
    qr = cr - Fr(r.choice([1, 2, 3]), 4)
    if qr <= Fr(1, 2):
        raise ValueError
    inv = I(cl * (cr - qr))
    return {'stem': f'A company has a current ratio of {rt(cr)} and a quick ratio of {rt(qr)}. Its inventories are {inr(inv)} (no prepaid expenses). Calculate its current liabilities and current assets.',
            'answer': f'Current liabilities {inr(cl)}; current assets {inr(ca)}',
            'key': f'Difference in ratios {num(float(cr - qr))} = inventories ÷ CL; CL = {inr(inv)} ÷ {num(float(cr - qr))} = {inr(cl)}; CA = {num(float(cr))} × CL = {inr(ca)}.',
            'distractors': [f'Current liabilities {inr(ca)}; current assets {inr(cl)}', f'Current liabilities {inr(inv)}; current assets {inr(I(inv * cr))}', f'Current liabilities {inr(cl)}; current assets {inr(ca - inv)}']}


# transactions: (text, dCA, dQA, dCL)
def _txs(x, y):
    return [
        (f'Purchased goods on credit for {inr(x)}', x, 0, x),
        (f'Paid trade payables {inr(x)}', -x, -x, -x),
        (f'Collected {inr(x)} from trade receivables', 0, 0, 0),
        (f'Issued equity shares for cash {inr(x)}', x, x, 0),
        (f'Purchased machinery for cash {inr(x)}', -x, -x, 0),
        (f'Raised a short-term bank loan of {inr(x)}', x, x, x),
        (f'Purchased inventory for cash {inr(x)}', 0, -x, 0),
        (f'Paid outstanding expenses of {inr(x)}', -x, -x, -x),
        (f'Sold goods costing {inr(x)} on credit for {inr(y)}', y - x, y, 0),
        (f'Redeemed debentures by paying cash {inr(x)}', -x, -x, 0),
        (f'Raised a long-term loan of {inr(x)}', x, x, 0),
        (f'Sold machinery (book value {inr(x)}) for cash at book value', x, x, 0),
    ]


def _eff(a, b):
    return 'Increase' if b > a else 'Decrease' if b < a else 'No change'


def c9_effect(r):
    inv, tr, cash, pre, ca, cl = _bs(r)
    qa = ca - inv - pre
    x = amt(r, 10000, min(cl, qa) // 2 + 10000, 5000)
    y = I(Fr(x * r.choice([120, 125, 150]), 100))
    t, dca, dqa, dcl = r.choice(_txs(x, y))
    if cl + dcl <= 0 or qa + dqa <= 0:
        raise ValueError
    which = r.choice(['current', 'quick'])
    if which == 'current':
        a, b = Fr(ca, cl), Fr(ca + dca, cl + dcl)
    else:
        a, b = Fr(qa, cl), Fr(qa + dqa, cl + dcl)
    if a == 1:
        raise ValueError
    ans = _eff(a, b)
    return mcq(f'The {which} ratio of a company is {rt(a)} (current assets {inr(ca)}, {"quick assets " + inr(qa) + ", " if which == "quick" else ""}current liabilities {inr(cl)}). Transaction: {t}. The {which} ratio will:',
               ans, [x_ for x_ in ['Increase', 'Decrease', 'No change', 'Become exactly 1:1'] if x_ != ans][:3],
               f'New {which} ratio = {rt(b)} (was {rt(a)}): {ans.lower()}.', r)


def c9_effect_explain(r):
    v = retry(c9_effect, r)
    return {'stem': v['stem'].replace(' will:', ' will increase, decrease or not change? Give reasons with calculation.'), 'answer': v['answer'],
            'key': f'Identification 1 mark; calculation and reason 2 marks: {v["key"][4:]}'}


CH09_ST2 = dict(
    cat='term',
    terms=[
        ('Current ratio', 'The ratio of current assets to current liabilities.'),
        ('Quick ratio', 'The ratio of quick (liquid) assets to current liabilities.'),
        ('Quick assets', 'Current assets excluding inventories and prepaid expenses.'),
        ('Working capital', 'The excess of current assets over current liabilities.'),
    ],
    ars=[
        ('Quick ratio is a more rigorous test of liquidity than current ratio.', 'Inventories and prepaid expenses are excluded from quick assets.', 'a', 'Both true; R explains A.'),
        ('A very high current ratio is always good for a business.', 'Excess current assets may mean idle funds.', 'd', 'A is false: too high a ratio indicates idle funds. R is true.'),
        ('Payment to a creditor increases a current ratio of 2:1.', 'Equal decrease in current assets and current liabilities raises a ratio above 1.', 'a', 'Both true; R explains A.'),
        ('Inventories are part of quick assets.', 'Inventories take time to convert into cash.', 'd', 'A is false. R is true.')],
    tf=('liquidity ratios', [
        'Quick assets exclude inventories and prepaid expenses.',
        'Current ratio = current assets ÷ current liabilities.',
        'Collection from debtors does not change the current ratio.'], [
        'Quick ratio = quick assets ÷ total liabilities.',
        'Inventories are included in quick assets.',
        'Purchase of goods for cash changes the current ratio.',
        'Working capital = current liabilities − current assets.']),
)


def _solv(r):
    sc = amt(r, 500000, 3000000, 100000)
    rs_ = amt(r, 50000, 1000000, 50000) * r.choice([1, 1, 1, -1])
    sf = sc + rs_
    ltd = amt(r, 200000, 2000000, 100000)
    cl = amt(r, 100000, 800000, 50000)
    ta = sf + ltd + cl
    if sf <= 0:
        raise ValueError
    return sc, rs_, sf, ltd, cl, ta


def c9_solvency(r):
    sc, rs_, sf, ltd, cl, ta = retry(_solv, r)
    k = r.choice(['de', 'tad', 'prop', 'ic'])
    data = f'equity share capital {inr(sc)}, reserves and surplus {"(debit balance of statement of P&L) −" if rs_ < 0 else ""}{inr(abs(rs_))}, long-term borrowings (debentures) {inr(ltd)}, current liabilities {inr(cl)}'
    if k == 'de':
        v = Fr(ltd, sf)
        return {'stem': f'Calculate the debt-equity ratio from: {data}.', 'answer': rt(v),
                'key': f'Debt = long-term borrowings {inr(ltd)}; equity = shareholders\' funds {inr(sc)} {"−" if rs_ < 0 else "+"} {inr(abs(rs_))} = {inr(sf)}; ratio = {rt(v)}.',
                'distractors': [rt(Fr(ltd + cl, sf)), rt(Fr(ltd, sc)), rt(Fr(sf, ltd))]}
    if k == 'tad':
        v = Fr(ta, ltd)
        return {'stem': f'Calculate the total assets to debt ratio from: {data}.', 'answer': rt(v),
                'key': f'Total assets = {inr(sf)} + {inr(ltd)} + {inr(cl)} = {inr(ta)}; debt {inr(ltd)}; ratio = {rt(v)}.',
                'distractors': [rt(Fr(ta - cl, ltd)), rt(Fr(ltd, ta)), rt(Fr(ta, ltd + cl))]}
    if k == 'prop':
        v = Fr(sf, ta)
        return {'stem': f'Calculate the proprietary ratio from: {data}.', 'answer': rt(v),
                'key': f'Proprietary ratio = shareholders\' funds {inr(sf)} ÷ total assets {inr(ta)} = {rt(v)}.',
                'distractors': [rt(Fr(sc, ta)), rt(Fr(sf, ltd + cl)), rt(Fr(ta, sf))]}
    rate = r.choice([8, 9, 10, 12])
    intr = I(Fr(ltd * rate, 100))
    npat = amt(r, intr, intr * 6, 10000)
    tax = r.choice([25, 30, 40, 50])
    npbt = I(Fr(npat * 100, 100 - tax))
    pbit = npbt + intr
    v = Fr(pbit, intr)
    return {'stem': f'A company has {rate}% debentures of {inr(ltd)}. Its net profit after interest and tax is {inr(npat)}; the tax rate is {tax}%. Calculate the interest coverage ratio.',
            'answer': tm(v),
            'key': f'Interest = {inr(intr)}; profit before tax = {inr(npat)} × 100/{100 - tax} = {inr(npbt)}; profit before interest and tax = {inr(pbit)}; ratio = {inr(pbit)}/{inr(intr)} = {tm(v)}.',
            'distractors': [tm(Fr(npat, intr)), tm(Fr(npbt, intr)), tm(Fr(npat + intr, intr))]}


def c9_solv_mcq(r):
    v = retry(c9_solvency, r)
    return mcq(v['stem'].replace('Calculate', 'Find'), v['answer'], v['distractors'], v['key'], r)


def c9_de_effect(r):
    x = amt(r, 50000, 500000, 10000)
    cases = [(f'Issue of equity shares for cash {inr(x)}', 'Decrease', 'Equity increases, debt unchanged.'),
             (f'Issue of debentures for cash {inr(x)}', 'Increase', 'Debt increases, equity unchanged.'),
             (f'Redemption of debentures of {inr(x)} in cash', 'Decrease', 'Debt decreases.'),
             (f'Conversion of debentures of {inr(x)} into equity shares', 'Decrease', 'Debt decreases and equity increases.'),
             (f'Purchase of machinery for cash {inr(x)}', 'No change', 'Neither long-term debt nor equity changes.'),
             (f'Issue of bonus shares of {inr(x)} out of general reserve', 'No change', 'Reserves become capital; shareholders\' funds unchanged.'),
             (f'Raising a long-term bank loan of {inr(x)}', 'Increase', 'Debt increases.'),
             (f'Purchase of machinery of {inr(x)} by issuing debentures', 'Increase', 'Debt increases.')]
    t, a, why = r.choice(cases)
    de = r.choice(['0.5:1', '0.8:1', '1.5:1', '2:1', '0.6:1'])
    return mcq(f'The debt-equity ratio of a company is {de}. What will be the effect of the following transaction on it? {t}.', a,
               [x_ for x_ in ['Increase', 'Decrease', 'No change', 'Become nil'] if x_ != a][:3], f'{a}: {why}', r)


CH09_ST3 = dict(
    cat='term',
    terms=[
        ('Debt-equity ratio', 'The ratio of long-term debts to shareholders\' funds (equity).'),
        ('Total assets to debt ratio', 'The ratio of total assets to long-term debts.'),
        ('Proprietary ratio', 'The ratio of shareholders\' funds to total assets.'),
        ('Interest coverage ratio', 'The ratio of net profit before interest and tax to interest on long-term debts.'),
        ('Shareholders\' funds', 'Share capital plus reserves and surplus (equity).'),
    ],
    ars=[
        ('A low debt-equity ratio indicates greater long-term solvency.', 'Creditors have a larger margin of safety when owners\' funds are high.', 'a', 'Both true; R explains A.'),
        ('Issue of bonus shares does not affect the debt-equity ratio.', 'Shareholders\' funds remain unchanged.', 'a', 'Both true; R explains A.'),
        ('A high interest coverage ratio is unfavourable to lenders.', 'It shows that interest is covered many times by profit.', 'd', 'A is false: it is favourable to lenders. R is true.'),
        ('Proprietary ratio + ratio of outside liabilities to total assets = 1.', 'Total assets are financed either by owners or by outsiders.', 'a', 'Both true; R explains A.')],
    tf=('solvency ratios', [
        'Debt-equity ratio = long-term debts ÷ shareholders\' funds.',
        'Interest coverage ratio uses profit before interest and tax.',
        'Proprietary ratio = shareholders\' funds ÷ total assets.'], [
        'Debt-equity ratio = current liabilities ÷ equity.',
        'Interest coverage ratio uses profit after tax.',
        'Issue of shares for cash increases the debt-equity ratio.',
        'Total assets to debt ratio = long-term debts ÷ total assets.']),
)


def c9_turnover(r):
    k = r.choice(['inv', 'tr', 'tp', 'wc'])
    if k == 'inv':
        o = amt(r, 50000, 300000, 10000)
        c = amt(r, 50000, 300000, 10000)
        avg = Fr(o + c, 2)
        t_ = r.choice([4, 5, 6, 8, 10, Fr(9, 2), Fr(15, 2)])
        cogs = I(avg * t_)
        gp = r.choice([20, 25, 30])
        rev = I(Fr(cogs * 100, 100 - gp))
        return {'stem': f'Revenue from operations is {inr(rev)} and the gross profit is {gp}% of revenue. Opening inventory was {inr(o)} and closing inventory {inr(c)}. Calculate the inventory turnover ratio.',
                'answer': tm(t_),
                'key': f'Cost of revenue from operations = {inr(rev)} − {gp}% = {inr(cogs)}; average inventory = ({inr(o)} + {inr(c)})/2 = {money(avg)}; ratio = {tm(t_)}.',
                'distractors': [tm(Fr(rev) / avg), tm(Fr(cogs, c)), tm(Fr(cogs, o + c))]}
    if k == 'tr':
        o = amt(r, 50000, 300000, 10000)
        c = amt(r, 50000, 300000, 10000)
        avg = Fr(o + c, 2)
        t_ = r.choice([4, 5, 6, 8, 10, 12])
        credit = I(avg * t_)
        cash = amt(r, 0, credit // 2, 10000)
        days = 365
        return {'stem': f'Total revenue from operations is {inr(credit + cash)}, of which cash sales are {inr(cash)}. Trade receivables were {inr(o)} at the beginning and {inr(c)} at the end of the year. Calculate the trade receivables turnover ratio and the average collection period (365 days).',
                'answer': f'{tm(t_)}; about {num(round(days / t_), 0)} days',
                'key': f'Credit revenue {inr(credit)}; average receivables {money(avg)}; ratio = {tm(t_)} (2 marks); collection period 365/{num(t_)} ≈ {num(round(days / t_), 0)} days (1 mark).',
                'distractors': [f'{tm(Fr(credit + cash) / avg)}; about {num(round(days * avg / (credit + cash)), 0)} days', f'{tm(Fr(credit, c))}; about {num(round(days * c / credit), 0)} days', f'{tm(t_ * 2)}; about {num(round(days / t_ / 2), 0)} days']}
    if k == 'tp':
        o = amt(r, 40000, 200000, 10000)
        c = amt(r, 40000, 200000, 10000)
        avg = Fr(o + c, 2)
        t_ = r.choice([4, 5, 6, 8])
        cp = I(avg * t_)
        cashp = amt(r, 0, cp // 3, 10000)
        return {'stem': f'Total purchases were {inr(cp + cashp)}, of which cash purchases were {inr(cashp)}. Trade payables were {inr(o)} at the beginning and {inr(c)} at the end of the year. Calculate the trade payables turnover ratio.',
                'answer': tm(t_), 'key': f'Net credit purchases {inr(cp)}; average trade payables {money(avg)}; ratio = {tm(t_)}.',
                'distractors': [tm(Fr(cp + cashp) / avg), tm(Fr(cp, c)), tm(Fr(cp, o))]}
    ca = amt(r, 200000, 1000000, 10000)
    cl = amt(r, 50000, ca - 50000, 10000)
    wc = ca - cl
    t_ = r.choice([2, 3, 4, 5, 6])
    rev = wc * t_
    return {'stem': f'Revenue from operations {inr(rev)}; current assets {inr(ca)}; current liabilities {inr(cl)}. Calculate the working capital turnover ratio.',
            'answer': tm(t_), 'key': f'Working capital = {inr(ca)} − {inr(cl)} = {inr(wc)}; ratio = {inr(rev)}/{inr(wc)} = {tm(t_)}.',
            'distractors': [tm(Fr(rev, ca)), tm(Fr(rev, cl)), tm(Fr(rev, ca + cl))]}


def c9_turn_mcq(r):
    v = retry(c9_turnover, r)
    ds = [d for d in dict.fromkeys(v['distractors']) if d != v['answer']]
    if len(ds) < 3 or ';' in v['answer']:
        raise ValueError
    return mcq(v['stem'].replace('Calculate', 'Find'), v['answer'], ds[:3], v['key'], r)


CH09_ST4 = dict(
    cat='term',
    terms=[
        ('Inventory turnover ratio', 'The ratio of cost of revenue from operations to average inventory.'),
        ('Trade receivables turnover ratio', 'The ratio of net credit revenue from operations to average trade receivables.'),
        ('Trade payables turnover ratio', 'The ratio of net credit purchases to average trade payables.'),
        ('Working capital turnover ratio', 'The ratio of revenue from operations to working capital.'),
        ('Average collection period', 'The average number of days taken to collect trade receivables, equal to days in a year ÷ receivables turnover.'),
    ],
    ars=[
        ('A high inventory turnover ratio generally indicates efficient inventory management.', 'Inventory is being sold quickly.', 'a', 'Both true; R explains A.'),
        ('Trade receivables turnover ratio is calculated on total revenue from operations.', 'Only credit sales give rise to receivables.', 'd', 'A is false: it uses net credit revenue. R is true.'),
        ('Inventory turnover ratio is calculated on cost of revenue from operations.', 'Inventory is valued at cost.', 'a', 'Both true; R explains A.')],
    tf=('activity ratios', [
        'Inventory turnover = cost of revenue from operations ÷ average inventory.',
        'Average inventory = (opening + closing inventory) ÷ 2.',
        'Working capital turnover = revenue from operations ÷ working capital.'], [
        'Inventory turnover = revenue from operations ÷ closing inventory always.',
        'Trade payables turnover uses credit sales.',
        'A lower receivables turnover means faster collection.',
        'Working capital turnover = revenue ÷ current assets.']),
)


def c9_profit(r):
    k = r.choice(['gp', 'np', 'op', 'roi'])
    rev = amt(r, 1000000, 9000000, 100000)
    if k == 'gp':
        cogs = amt(r, rev // 2, rev * 9 // 10, 10000)
        return {'stem': f'Revenue from operations {inr(rev)}; cost of revenue from operations {inr(cogs)}. Calculate the gross profit ratio.',
                'answer': pct(rev - cogs, rev), 'key': f'Gross profit {inr(rev - cogs)} ÷ {inr(rev)} × 100 = {pct(rev - cogs, rev)}.',
                'distractors': [pct(rev - cogs, cogs), pct(cogs, rev), pct(rev - cogs, rev + cogs)]}
    if k == 'np':
        npat = amt(r, rev // 20, rev // 5, 10000)
        return {'stem': f'Revenue from operations {inr(rev)}; net profit after tax {inr(npat)}. Calculate the net profit ratio.',
                'answer': pct(npat, rev), 'key': f'{inr(npat)} ÷ {inr(rev)} × 100 = {pct(npat, rev)}.',
                'distractors': [pct(npat * 2, rev), pct(rev - npat, rev), pct(npat, rev - npat)]}
    if k == 'op':
        cogs = amt(r, rev // 2, rev * 7 // 10, 10000)
        oe = amt(r, rev // 20, rev // 5, 10000)
        return {'stem': f'Revenue from operations {inr(rev)}; cost of revenue from operations {inr(cogs)}; operating expenses {inr(oe)}. Calculate the operating ratio and operating profit ratio.',
                'answer': f'Operating ratio {pct(cogs + oe, rev)}; operating profit ratio {pct(rev - cogs - oe, rev)}',
                'key': f'Operating cost = {inr(cogs)} + {inr(oe)} = {inr(cogs + oe)}; operating ratio = {pct(cogs + oe, rev)}; operating profit ratio = 100% − operating ratio = {pct(rev - cogs - oe, rev)}.',
                'distractors': [f'Operating ratio {pct(cogs, rev)}; operating profit ratio {pct(rev - cogs, rev)}', f'Operating ratio {pct(oe, rev)}; operating profit ratio {pct(rev - oe, rev)}', f'Operating ratio {pct(rev - cogs - oe, rev)}; operating profit ratio {pct(cogs + oe, rev)}']}
    sc, rs_, sf, ltd, cl, ta = retry(_solv, r)
    rate = r.choice([8, 9, 10, 12])
    intr = I(Fr(ltd * rate, 100))
    pbt = amt(r, 100000, 1000000, 10000)
    ce = sf + ltd
    pbit = pbt + intr
    return {'stem': f'Shareholders\' funds {inr(sf)}; {rate}% debentures {inr(ltd)}; current liabilities {inr(cl)}; profit before tax for the year {inr(pbt)}. Calculate the return on investment.',
            'answer': pct(pbit, ce),
            'key': f'Interest on debentures = {inr(intr)}; PBIT = {inr(pbt)} + {inr(intr)} = {inr(pbit)}; capital employed = {inr(sf)} + {inr(ltd)} = {inr(ce)}; ROI = {pct(pbit, ce)}.',
            'distractors': [pct(pbt, ce), pct(pbit, ce + cl), pct(pbit, sf)]}


def c9_profit_mcq(r):
    v = c9_profit(r)
    if ';' in v['answer']:
        raise ValueError
    ds = [d for d in dict.fromkeys(v['distractors']) if d != v['answer']]
    return mcq(v['stem'].replace('Calculate', 'Find'), v['answer'], ds[:3], v['key'], r)


def c9_multi(r):
    co = company(r)
    inv, tr, cash, pre, ca, cl = _bs(r)
    sc, rs_, sf, ltd, _cl, ta = retry(_solv, r)
    rev = amt(r, 1000000, 6000000, 100000)
    gp = r.choice([20, 25, 30, 40])
    cogs = I(Fr(rev * (100 - gp), 100))
    oinv = amt(r, 50000, 300000, 10000)
    avg = Fr(oinv + inv, 2)
    cr, qr, de = Fr(ca, cl), Fr(ca - inv - pre, cl), Fr(ltd, sf)
    it = Fr(cogs) / avg
    ans = f'Current ratio {rt(cr)}; quick ratio {rt(qr)}; debt-equity ratio {rt(de)}; inventory turnover {tm(it)}'
    return {'stem': f'From the following information of {co}, calculate (i) current ratio (ii) quick ratio (iii) debt-equity ratio (iv) inventory turnover ratio: inventories {inr(inv)} (opening {inr(oinv)}), trade receivables {inr(tr)}, cash {inr(cash)}'
                    + (f', prepaid expenses {inr(pre)}' if pre else '') + f', current liabilities {inr(cl)}, shareholders\' funds {inr(sf)}, long-term borrowings {inr(ltd)}, revenue from operations {inr(rev)}, gross profit {gp}% on revenue.',
            'answer': ans,
            'key': f'(i) {inr(ca)}/{inr(cl)} = {rt(cr)} (ii) quick assets {inr(ca - inv - pre)}/{inr(cl)} = {rt(qr)} (iii) {inr(ltd)}/{inr(sf)} = {rt(de)} (iv) cost of revenue {inr(cogs)} ÷ average inventory {money(avg)} = {tm(it)}. 1½ marks each.'}


CH09_ST5 = dict(
    cat='term',
    terms=[
        ('Gross profit ratio', 'Gross profit as a percentage of revenue from operations.'),
        ('Operating ratio', 'Cost of revenue from operations plus operating expenses, as a percentage of revenue from operations.'),
        ('Net profit ratio', 'Net profit as a percentage of revenue from operations.'),
        ('Return on investment', 'Profit before interest and tax as a percentage of capital employed.'),
        ('Operating profit ratio', 'Operating profit as a percentage of revenue from operations; equal to 100 minus the operating ratio.'),
    ],
    ars=[
        ('Operating ratio + operating profit ratio = 100%.', 'Operating profit is revenue less operating cost.', 'a', 'Both true; R explains A.'),
        ('Return on investment is calculated on profit after tax.', 'ROI measures the overall return on capital employed.', 'd', 'A is false: it uses profit before interest and tax. R is true.'),
        ('A rise in gross profit ratio may result from a rise in selling price.', 'Gross profit = revenue − cost of revenue from operations.', 'a', 'Both true; R explains A.')],
    tf=('profitability ratios', [
        'Gross profit ratio = gross profit ÷ revenue from operations × 100.',
        'Return on investment uses profit before interest and tax.',
        'Operating profit ratio = 100 − operating ratio.'], [
        'Net profit ratio uses gross profit.',
        'Return on investment uses profit after tax and interest.',
        'Operating ratio includes interest on debentures.',
        'Gross profit ratio is calculated on cost of revenue.']),
)

# ================================================================ ch10 Cash flow statement

CH10_ST1 = dict(
    cat='term',
    terms=[
        ('Cash flow statement', 'A statement showing the inflows and outflows of cash and cash equivalents of an enterprise during a period under operating, investing and financing activities.'),
        ('Cash equivalents', 'Short-term, highly liquid investments readily convertible into known amounts of cash, with insignificant risk of change in value and maturity of three months or less from acquisition.'),
        ('Cash flows', 'Inflows and outflows of cash and cash equivalents.'),
        ('AS 3 (Revised)', 'The accounting standard that prescribes the preparation of the cash flow statement.'),
        ('Non-cash transaction', 'A transaction that does not involve cash or cash equivalents, such as issue of shares to vendors, and is excluded from the cash flow statement.'),
    ],
    lists=[('obj', 'benefits of a cash flow statement', [
        ('Helps in short-term financial planning', 'Shows expected sources and uses of cash.'),
        ('Shows the ability to generate cash', 'Operating cash flows show the strength of the business.'),
        ('Helps assess liquidity and solvency', 'Users judge the ability to pay debts.'),
        ('Explains the difference between profit and cash', 'Profit and cash position can be reconciled.'),
        ('Helps in comparison over years', 'Cash flows of different periods can be compared.')], None)],
    scen=[('Is the item a cash equivalent?', ['Cash equivalent', 'Not a cash equivalent', 'Part of cash in hand', 'Investing activity, not cash'], [
        ('{f} Ltd bought 91-day treasury bills.', 'Cash equivalent', 'Maturity within three months of acquisition and insignificant risk.'),
        ('{f} Ltd bought equity shares of another company to sell when prices rise.', 'Not a cash equivalent', 'Equity shares carry significant risk of change in value.'),
        ('{f} Ltd made a fixed deposit with a bank maturing in 60 days.', 'Cash equivalent', 'Maturity of three months or less.'),
        ('{f} Ltd made a fixed deposit of one year with a bank.', 'Not a cash equivalent', 'Maturity exceeds three months.'),
        ('{f} Ltd bought short-term commercial paper maturing in two months.', 'Cash equivalent', 'Highly liquid with maturity within three months.')], None)],
    ars=[
        ('Equity shares are not cash equivalents.', 'Their value is subject to significant risk of change.', 'a', 'Both true; R explains A.'),
        ('Purchase of marketable securities with a 60-day maturity is shown as an investing activity.', 'They are cash equivalents.', 'd', 'A is false: movements between cash and cash equivalents are not cash flows. R is true.'),
        ('Issue of shares to vendors for machinery is not shown in the cash flow statement.', 'It is a non-cash transaction.', 'a', 'Both true; R explains A.')],
    tf=('the cash flow statement', [
        'It is prepared under AS 3 (Revised).',
        'Cash equivalents have a maturity of three months or less from acquisition.',
        'Non-cash transactions are excluded from it.'], [
        'Cash equivalents include investments maturing in one year.',
        'It replaces the statement of profit and loss.',
        'Issue of bonus shares is shown as a financing activity.',
        'It is prepared on the accrual basis.']),
)

CLS = [
    ('Cash receipts from sale of goods', 'Operating activity', 'any'), ('Cash paid to suppliers of goods', 'Operating activity', 'any'),
    ('Salaries and wages paid to employees', 'Operating activity', 'any'), ('Income tax paid', 'Operating activity', 'any'),
    ('Cash receipts from royalties, fees and commission', 'Operating activity', 'any'),
    ('Purchase of machinery', 'Investing activity', 'any'), ('Sale of land', 'Investing activity', 'any'), ('Purchase of goodwill', 'Investing activity', 'any'),
    ('Purchase of long-term investments', 'Investing activity', 'any'), ('Purchase of patents', 'Investing activity', 'any'),
    ('Interest received on investments', 'Investing activity', 'non-financial'), ('Dividend received on investments', 'Investing activity', 'non-financial'),
    ('Interest received on loans given', 'Operating activity', 'financial'), ('Dividend received on shares held', 'Operating activity', 'financial'),
    ('Interest paid on borrowings', 'Operating activity', 'financial'), ('Loans advanced to customers', 'Operating activity', 'financial'),
    ('Issue of equity shares for cash', 'Financing activity', 'any'), ('Issue of debentures for cash', 'Financing activity', 'any'),
    ('Redemption of preference shares', 'Financing activity', 'any'), ('Buy-back of equity shares', 'Financing activity', 'any'),
    ('Repayment of a long-term loan', 'Financing activity', 'any'), ('Interest paid on debentures', 'Financing activity', 'non-financial'),
    ('Dividend paid to shareholders', 'Financing activity', 'any'), ('Underwriting commission paid on issue of shares', 'Financing activity', 'any'),
    ('Issue of shares to vendors in exchange for machinery', 'Not shown (non-cash transaction)', 'any'),
    ('Conversion of debentures into equity shares', 'Not shown (non-cash transaction)', 'any'),
    ('Issue of bonus shares', 'Not shown (non-cash transaction)', 'any'),
]
ACT = ['Operating activity', 'Investing activity', 'Financing activity', 'Not shown (non-cash transaction)']
cls_c = Cyc(CLS)


def _who(r, scope):
    if scope == 'financial':
        return f'{r.choice(["a bank", "a finance company", "an investment company"])}'
    if scope == 'non-financial':
        return f'a {r.choice(["manufacturing", "trading", "non-financial"])} company'
    return r.choice(['a manufacturing company', 'a trading company', 'a non-financial company'])


def c10_class(r):
    it, a, scope = cls_c.next(r)
    w = _who(r, scope)
    return mcq(f'For {w}, "{it.lower()}" is classified in the cash flow statement as:', a, [x for x in ACT if x != a], f'{it} ({w}): {a}.', r)


def c10_class3(r):
    its = r.sample(CLS, 6)
    lst = '; '.join(f'({i + 1}) {it} ({_who(r, sc)})' for i, (it, a, sc) in enumerate(its))
    ans = '; '.join(f'({i + 1}) {a}' for i, (it, a, sc) in enumerate(its))
    return {'stem': f'Classify the following into operating, investing and financing activities, or say if not shown: {lst}.',
            'answer': ans, 'key': f'½ mark each: {ans}'}


CH10_ST2 = dict(
    cat='activity',
    terms=[
        ('Operating activities', 'The principal revenue-producing activities of an enterprise and other activities that are not investing or financing.'),
        ('Investing activities', 'The acquisition and disposal of long-term assets and other investments not included in cash equivalents.'),
        ('Financing activities', 'Activities that result in changes in the size and composition of the owners\' capital and borrowings of the enterprise.'),
        ('Financial enterprise', 'An enterprise such as a bank or finance company whose main business is lending, investing and borrowing.'),
    ],
    ars=[
        ('Interest received by a bank is an operating activity.', 'Lending is the main business of a bank.', 'a', 'Both true; R explains A.'),
        ('Dividend paid is a financing activity for every enterprise.', 'Dividend is a return to owners.', 'a', 'Both true; R explains A.'),
        ('Interest paid by a manufacturing company on debentures is an operating activity.', 'Debentures are a source of finance.', 'd', 'A is false: it is a financing activity. R is true.'),
        ('Purchase of shares by an investment company is an operating activity.', 'Investing in securities is its main business.', 'a', 'Both true; R explains A.')],
    tf=('classification of cash flows', [
        'Dividend received by a non-financial company is an investing activity.',
        'Income tax paid is generally an operating activity.',
        'Issue of debentures for cash is a financing activity.'], [
        'Interest received by a bank is an investing activity.',
        'Purchase of machinery is an operating activity.',
        'Dividend paid is an operating activity of a manufacturing company.',
        'Issue of bonus shares is a financing activity.']),
)


def _ocf(r, rich=False):
    npbt = amt(r, 100000, 1000000, 10000)
    dep = amt(r, 10000, 100000, 5000)
    adj = []
    if rich or r.random() < 0.5:
        adj.append(('Loss on sale of machinery', amt(r, 2000, 20000, 1000)))
    if rich or r.random() < 0.5:
        adj.append(('Interest on debentures', amt(r, 5000, 50000, 1000)))
    if rich or r.random() < 0.4:
        adj.append(('Profit on sale of investments', -amt(r, 2000, 20000, 1000)))
    if r.random() < 0.4:
        adj.append(('Goodwill written off', amt(r, 5000, 30000, 1000)))
    if r.random() < 0.4:
        adj.append(('Dividend received', -amt(r, 2000, 20000, 1000)))
    wc_items = [('Trade receivables', 'asset'), ('Inventories', 'asset'), ('Trade payables', 'liab'), ('Outstanding expenses', 'liab'), ('Prepaid expenses', 'asset')]
    wc = []
    for nm, kind in r.sample(wc_items, 4 if rich else 3):
        ch = amt(r, 2000, 60000, 1000) * r.choice([1, -1])
        eff = -ch if kind == 'asset' else ch
        wc.append((nm, ch, eff))
    tax = amt(r, 10000, npbt // 3, 1000)
    op_before = npbt + dep + sum(x for _, x in adj)
    cgo = op_before + sum(e for _, _, e in wc)
    ocf = cgo - tax
    return npbt, dep, adj, wc, tax, op_before, cgo, ocf


def _ocf_text(npbt, dep, adj, wc, tax):
    parts = [f'net profit before tax {inr(npbt)}', f'depreciation {inr(dep)}'] + [f'{n.lower()} {inr(abs(x))}' for n, x in adj]
    parts += [f'{n.lower()} {"increased" if ch > 0 else "decreased"} by {inr(abs(ch))}' for n, ch, _ in wc]
    parts.append(f'income tax paid {inr(tax)}')
    return '; '.join(parts)


def c10_ocf(r, rich=False):
    npbt, dep, adj, wc, tax, opb, cgo, ocf = _ocf(r, rich)
    key = (f'NPBT {inr(npbt)} + depreciation {inr(dep)} ' + ' '.join(f'{"+" if x > 0 else "−"} {n.lower()} {inr(abs(x))}' for n, x in adj)
           + f' = operating profit before working capital changes {inr(opb)}; ' + ' '.join(f'{"+" if e > 0 else "−"} {"increase" if ch > 0 else "decrease"} in {n.lower()} {inr(abs(ch))}' for n, ch, e in wc)
           + f' = cash generated from operations {inr(cgo)}; less tax {inr(tax)} = net cash {"from" if ocf >= 0 else "used in"} operating activities {inr(abs(ocf))}.')
    return {'stem': f'Calculate cash flow from operating activities: {_ocf_text(npbt, dep, adj, wc, tax)}.',
            'answer': f'Net cash {"from" if ocf >= 0 else "used in"} operating activities {inr(abs(ocf))}', 'key': key,
            'distractors': [f'Net cash from operating activities {inr(abs(ocf + 2 * sum(e for _, _, e in wc)))}', f'Net cash from operating activities {inr(abs(opb - tax))}', f'Net cash from operating activities {inr(abs(cgo))}']}


def c10_ocf_rich(r):
    return c10_ocf(r, True)


def c10_ocf_pl(r):
    a = amt(r, 50000, 400000, 10000)
    b = a + amt(r, 20000, 300000, 10000) * r.choice([1, 1, -1])
    if b < 0:
        raise ValueError
    g = r.choice([0, amt(r, 10000, 80000, 5000)])
    t = amt(r, 20000, 150000, 5000)
    npbt = (b - a) + g + t
    if npbt <= 0:
        raise ValueError
    return {'stem': f'The balance of the statement of profit and loss (surplus) was {inr(a)} on 31 March 2025 and {inr(b)} on 31 March 2026. During the year '
                    + (f'{inr(g)} was transferred to general reserve and ' if g else '') + f'a provision for tax of {inr(t)} was made. Calculate the net profit before tax.',
            'answer': inr(npbt), 'key': f'({inr(b)} − {inr(a)}) {"+ transfer to reserve " + inr(g) + " " if g else ""}+ provision for tax {inr(t)} = {inr(npbt)}.',
            'distractors': [inr(b - a) if b != a else inr(t), inr(b - a + t + 2 * g) if g else inr(b + t), inr(npbt + a)]}


def _icf(r):
    o = amt(r, 200000, 1000000, 10000)
    dep = amt(r, 20000, 100000, 5000)
    bv = amt(r, 10000, 80000, 5000)
    sale = bv + amt(r, 1000, 10000, 1000) * r.choice([1, -1])
    purchase = amt(r, 50000, 400000, 10000)
    c = o - dep - bv + purchase
    inv_bought = r.choice([0, amt(r, 20000, 100000, 10000)])
    intr = r.choice([0, amt(r, 2000, 20000, 1000)])
    icf = sale - purchase - inv_bought + intr
    return o, c, dep, bv, sale, purchase, inv_bought, intr, icf


def c10_icf(r):
    o, c, dep, bv, sale, purchase, ib, intr, icf = _icf(r)
    pl = sale - bv
    return {'stem': f'Machinery (net book value) was {inr(o)} on 31 March 2025 and {inr(c)} on 31 March 2026. Depreciation charged during the year was {inr(dep)}. A machine with a book value of {inr(bv)} was sold for {inr(sale)}.'
                    + (f' Long-term investments of {inr(ib)} were purchased.' if ib else '') + (f' Interest received on investments was {inr(intr)} (non-financial company).' if intr else '') + ' Calculate cash flow from investing activities.',
            'answer': f'Net cash {"used in" if icf < 0 else "from"} investing activities {inr(abs(icf))}',
            'key': f'Machinery purchased = closing {inr(c)} + depreciation {inr(dep)} + book value sold {inr(bv)} − opening {inr(o)} = {inr(purchase)}; sale proceeds {inr(sale)} ({"profit" if pl > 0 else "loss"} {inr(abs(pl))} adjusted in operating activities)'
                   + (f'; investments purchased {inr(ib)}' if ib else '') + (f'; interest received {inr(intr)}' if intr else '') + f'. Net = {"−" if icf < 0 else ""}{inr(abs(icf))}.',
            'distractors': [f'Net cash used in investing activities {inr(abs(c - o))}', f'Net cash used in investing activities {inr(purchase)}', f'Net cash used in investing activities {inr(abs(icf) + 2 * sale)}']}


def _fcf(r):
    sc0 = amt(r, 500000, 2000000, 100000)
    iss = amt(r, 0, 1000000, 100000)
    prem = I(Fr(iss * r.choice([0, 10, 20]), 100))
    deb0 = amt(r, 200000, 1000000, 100000)
    ddeb = amt(r, 0, deb0 // 100000, 1) * 100000 * r.choice([1, -1])
    rate = r.choice([8, 9, 10, 12])
    intr = I(Fr(deb0 * rate, 100))
    div = amt(r, 0, 200000, 10000)
    fcf = iss + prem + ddeb - intr - div
    return sc0, iss, prem, deb0, ddeb, rate, intr, div, fcf


def c10_fcf(r):
    sc0, iss, prem, deb0, ddeb, rate, intr, div, fcf = _fcf(r)
    t = (f'Equity share capital increased from {inr(sc0)} to {inr(sc0 + iss)} by issue of shares for cash' + (f' at a premium of {inr(prem)}' if prem else '') + '. ' if iss else f'Equity share capital remained {inr(sc0)}. ')
    t += (f'{rate}% debentures were {inr(deb0)} at the beginning and {inr(deb0 + ddeb)} at the end; ' + ('additional debentures were issued at par on 31 March 2026' if ddeb > 0 else 'debentures were redeemed at par on 31 March 2026' if ddeb < 0 else 'there was no change') + '. ')
    t += f'Interest on debentures for the year was paid in full. ' + (f'Dividend paid during the year {inr(div)}.' if div else 'No dividend was paid.')
    return {'stem': f'{t} Calculate cash flow from financing activities.',
            'answer': f'Net cash {"from" if fcf >= 0 else "used in"} financing activities {inr(abs(fcf))}',
            'key': ' '.join(x for x in [f'Issue of shares {inr(iss)}' if iss else '', f'+ premium {inr(prem)}' if prem else '', (f'+ issue of debentures {inr(ddeb)}' if ddeb > 0 else f'− redemption of debentures {inr(-ddeb)}' if ddeb < 0 else ''),
                                       f'− interest on debentures {inr(intr)} ({rate}% on {inr(deb0)})', f'− dividend {inr(div)}' if div else ''] if x) + f' = {"−" if fcf < 0 else ""}{inr(abs(fcf))}.',
            'distractors': [f'Net cash from financing activities {inr(abs(fcf + 2 * intr))}', f'Net cash from financing activities {inr(abs(iss + ddeb))}', f'Net cash used in financing activities {inr(abs(fcf - 2 * div - 1000))}']}


def sg(x):
    return inr(x) if x >= 0 else '−' + inr(-x)


def c10_full(r):
    co = company(r)
    npbt, dep, adj, wc, tax, opb, cgo, ocf = _ocf(r)
    o, c, dep, bv, sale, purchase, ib, intr_r, icf = _icf(r)
    sc0, iss, prem, deb0, ddeb, rate, intr, div, fcf = _fcf(r)
    given = [(n, x) for n, x in adj if n == 'Goodwill written off']
    pl = sale - bv
    derived = [('Loss on sale of machinery' if pl < 0 else 'Profit on sale of machinery', -pl), ('Interest on debentures', intr)]
    if intr_r:
        derived.append(('Interest received', -intr_r))
    adj = given + derived
    opb = npbt + dep + sum(x for _, x in adj)
    cgo = opb + sum(e for _, _, e in wc)
    ocf = cgo - tax
    net = ocf + icf + fcf
    cash0 = amt(r, 20000, 200000, 5000)
    cash1 = cash0 + net
    if cash1 < 0 or pl == 0:
        raise ValueError
    stem = (f'Prepare the cash flow statement of {co} for the year ended 31 March 2026 from: {_ocf_text(npbt, dep, given, wc, tax)}. '
            f'Machinery (net) was {inr(o)} at the start and {inr(c)} at the end; a machine of book value {inr(bv)} was sold for {inr(sale)}; depreciation as above.'
            + (f' Long-term investments of {inr(ib)} were purchased.' if ib else '') + (f' Interest received on investments {inr(intr_r)}.' if intr_r else '') + ' '
            + (f'Equity shares of {inr(iss)} were issued for cash' + (f' at a premium of {inr(prem)}' if prem else '') + '. ' if iss else '')
            + (f'{rate}% debentures ({inr(deb0)} at the start) ' + ('increased' if ddeb > 0 else 'decreased') + f' by {inr(abs(ddeb))} on 31 March 2026. ' if ddeb else f'{rate}% debentures of {inr(deb0)} were unchanged. ')
            + 'Interest on debentures was paid in full. ' + (f'Dividend paid {inr(div)}. ' if div else '') + f'Cash and cash equivalents at the beginning {inr(cash0)}.')
    ans = f'Operating {sg(ocf)}; investing {sg(icf)}; financing {sg(fcf)}; net change {sg(net)}; closing cash {inr(cash1)}'
    key = (f'Operating: NPBT {inr(npbt)} + depreciation {inr(dep)} ' + ' '.join(f'{"+" if x > 0 else "−"} {n.lower()} {inr(abs(x))}' for n, x in adj)
           + f' = {inr(opb)}; working capital changes ' + ', '.join(f'{"+" if e > 0 else "−"}{inr(abs(e))}' for _, _, e in wc) + f' → {inr(cgo)}; less tax {inr(tax)} = {sg(ocf)} (3 marks). '
           + f'Investing: sale {inr(sale)} − purchase of machinery {inr(purchase)} (closing + depreciation + book value sold − opening)' + (f' − investments {inr(ib)}' if ib else '') + (f' + interest {inr(intr_r)}' if intr_r else '')
           + f' = {sg(icf)} (1½ marks). Financing: ' + ' '.join(x for x in [f'shares {inr(iss + prem)}' if iss else '', f'{"+" if ddeb > 0 else "−"} debentures {inr(abs(ddeb))}' if ddeb else '', f'− interest {inr(intr)}', f'− dividend {inr(div)}' if div else ''] if x)
           + f' = {sg(fcf)} (1½ marks). Net change {sg(net)}; closing cash and cash equivalents {inr(cash1)}.')
    return {'stem': stem, 'answer': ans, 'key': key}


CH10_ST3 = dict(
    cat='term',
    terms=[
        ('Indirect method', 'Method of finding cash from operating activities by adjusting net profit for non-cash items, non-operating items and changes in working capital.'),
        ('Direct method', 'Method of finding cash from operating activities by showing gross cash receipts and payments.'),
        ('Operating profit before working capital changes', 'Net profit before tax adjusted for non-cash and non-operating items.'),
        ('Cash generated from operations', 'Operating profit before working capital changes adjusted for changes in current assets and current liabilities.'),
    ],
    scen=[('How is the item treated while calculating cash from operating activities by the indirect method?', ['Added to net profit', 'Deducted from net profit', 'Not adjusted', 'Shown under financing activities only'], [
        ('Depreciation charged on machinery.', 'Added to net profit', 'Non-cash expense.'),
        ('Increase in trade receivables during the year.', 'Deducted from net profit', 'An increase in a current asset uses cash.'),
        ('Decrease in inventories during the year.', 'Added to net profit', 'A decrease in a current asset releases cash.'),
        ('Increase in trade payables during the year.', 'Added to net profit', 'An increase in a current liability conserves cash.'),
        ('Profit on sale of machinery.', 'Deducted from net profit', 'Non-operating gain; the sale proceeds are investing.'),
        ('Loss on sale of investments.', 'Added to net profit', 'Non-operating loss.'),
        ('Goodwill written off.', 'Added to net profit', 'Non-cash expense.'),
        ('Decrease in outstanding expenses.', 'Deducted from net profit', 'A decrease in a current liability uses cash.'),
        ('Interest on debentures debited to the statement of profit and loss.', 'Added to net profit', 'A financing item, added back and shown under financing.')], None)],
    ars=[
        ('Depreciation is added back to net profit under the indirect method.', 'Depreciation is a non-cash expense.', 'a', 'Both true; R explains A.'),
        ('An increase in trade payables is deducted from net profit.', 'It is an increase in a current liability.', 'd', 'A is false: it is added. R is true.'),
        ('Profit on sale of fixed assets is deducted from net profit.', 'Sale proceeds are shown under investing activities.', 'a', 'Both true; R explains A.')],
    tf=('the indirect method', [
        'An increase in a current asset is deducted.',
        'A decrease in a current liability is deducted.',
        'Non-cash expenses are added back.'], [
        'An increase in inventories is added.',
        'Depreciation is deducted from net profit.',
        'Profit on sale of machinery is added to net profit.',
        'An increase in trade payables is deducted.']),
)
CH10_ST4 = dict(
    cat='term',
    terms=[
        ('Net cash from investing activities', 'Cash received from sale of long-term assets and investments less cash spent on acquiring them.'),
        ('Net cash from financing activities', 'Cash raised from shares and borrowings less cash paid for redemption, interest and dividend.'),
        ('Net increase in cash and cash equivalents', 'The total of net cash from operating, investing and financing activities.'),
        ('Closing cash and cash equivalents', 'Opening cash and cash equivalents plus the net increase (or less the net decrease) during the year.'),
    ],
    ars=[
        ('Purchase of machinery is calculated from the machinery account.', 'Closing balance + depreciation + book value sold − opening balance gives the purchase.', 'a', 'Both true; R explains A.'),
        ('Interest on debentures paid is shown as an investing activity.', 'Debentures are borrowings.', 'd', 'A is false: it is a financing activity. R is true.'),
        ('Issue of shares at a premium increases cash from financing activities by the issue price.', 'Both face value and premium are received in cash.', 'a', 'Both true; R explains A.')],
    tf=('investing and financing activities', [
        'Sale of machinery is an investing inflow.',
        'Redemption of debentures is a financing outflow.',
        'Dividend paid is a financing outflow.'], [
        'Purchase of machinery is a financing outflow.',
        'Issue of shares for cash is an investing inflow.',
        'Depreciation is shown under investing activities.',
        'Interest received by a manufacturing company is a financing inflow.']),
)


def mcqize(gen):
    def f(r):
        v = retry(gen, r)
        ds = [d for d in dict.fromkeys(v.get('distractors', [])) if d != v['answer']]
        if len(ds) < 3:
            raise ValueError
        st = v['stem'].replace('Calculate', 'Find')
        return mcq(st, v['answer'], ds[:3], v['key'], r)
    f.__name__ = gen.__name__ + '_mcq'
    return f


FAMILIES = {
    S + '07-st1': facts(CH07_ST1),
    S + '07-st2': facts(CH07_ST2) + [FF('C2', 'D2', 'mcq', c7_head), FF('C3', 'D2', 'mcq', c7_sub), FF('C3', 'D3', 'explain', c7_classify3, marks=3, kinds=('m3',)),
                                     FF('C3', 'D3', 'numerical', c7_reserves, marks=3, kinds=('m3',)), FF('C4', 'D3', 'numerical', c7_sharecap, marks=4, kinds=('m4',)),
                                     FF('C4', 'D4', 'numerical', c7_reserves, marks=3), FF('C2', 'D1', 'mcq', c7_head), FF('C3', 'D1', 'mcq', c7_sub), FF('C3', 'D4', 'numerical', c7_sharecap, marks=4)],
    S + '07-st3': facts(CH07_ST3) + [FF('C3', 'D2', 'mcq', c7_pl), FF('C2', 'D1', 'mcq', c7_pl), FF('C3', 'D3', 'numerical', c7_revenue, marks=3, kinds=('m3',)),
                                     FF('C3', 'D2', 'numerical', c7_materials, marks=2), FF('C4', 'D3', 'numerical', c7_revenue, marks=3), FF('C3', 'D2', 'mcq', mcqize(c7_materials))],
    S + '07-st4': facts(CH07_ST4),
    S + '08-st1': facts(CH08_ST1),
    S + '08-st2': facts(CH08_ST2) + [FF('C3', 'D2', 'mcq', c8_change_mcq), FF('C3', 'D3', 'multi_step', c8_comparative, marks=4, kinds=('m4',)),
                                     FF('C4', 'D4', 'multi_step', c8_comparative, marks=4), FF('C2', 'D1', 'mcq', c8_change_mcq), FF('C3', 'D4', 'multi_step', c8_comparative, marks=4)],
    S + '08-st3': facts(CH08_ST3) + [FF('C3', 'D2', 'mcq', c8_cs_mcq), FF('C3', 'D3', 'multi_step', c8_commonsize, marks=4, kinds=('m4',)),
                                     FF('C4', 'D4', 'multi_step', c8_commonsize, marks=4), FF('C2', 'D1', 'mcq', c8_cs_mcq), FF('C4', 'D3', 'multi_step', c8_commonsize, marks=3, kinds=('m3',))],
    S + '08-st4': facts(CH08_ST4),
    S + '09-st1': facts(CH09_ST1),
    S + '09-st2': facts(CH09_ST2) + [FF('C3', 'D2', 'mcq', c9_current_mcq), FF('C3', 'D3', 'numerical', c9_current, marks=3, kinds=('m3',)), FF('C3', 'D3', 'numerical', c9_reverse, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'mcq', c9_effect), FF('C4', 'D4', 'explain', c9_effect_explain, marks=3, kinds=('m3',)), FF('C4', 'D4', 'numerical', c9_reverse, marks=4, kinds=('m4',)),
                                     FF('C3', 'D1', 'mcq', c9_current_mcq), FF('C4', 'D5', 'explain', c9_effect_explain, marks=3), FF('C3', 'D4', 'mcq', c9_effect)],
    S + '09-st3': facts(CH09_ST3) + [FF('C3', 'D2', 'mcq', c9_solv_mcq), FF('C3', 'D3', 'numerical', c9_solvency, marks=3, kinds=('m3',)), FF('C4', 'D3', 'mcq', c9_de_effect),
                                     FF('C4', 'D4', 'long', c9_multi, marks=6, kinds=('m6',)), FF('C3', 'D4', 'numerical', c9_solvency, marks=3), FF('C3', 'D1', 'mcq', c9_de_effect)],
    S + '09-st4': facts(CH09_ST4) + [FF('C3', 'D2', 'mcq', c9_turn_mcq), FF('C3', 'D3', 'numerical', c9_turnover, marks=3, kinds=('m3',)), FF('C4', 'D3', 'numerical', c9_turnover, marks=4, kinds=('m4',)),
                                     FF('C4', 'D4', 'long', c9_multi, marks=6, kinds=('m6',)), FF('C2', 'D1', 'mcq', c9_turn_mcq)],
    S + '09-st5': facts(CH09_ST5) + [FF('C3', 'D2', 'mcq', c9_profit_mcq), FF('C3', 'D3', 'numerical', c9_profit, marks=3, kinds=('m3',)), FF('C4', 'D3', 'numerical', c9_profit, marks=4, kinds=('m4',)),
                                     FF('C3', 'D1', 'mcq', c9_profit_mcq), FF('C4', 'D4', 'long', c9_multi, marks=6)],
    S + '10-st1': facts(CH10_ST1) + [FF('C3', 'D2', 'mcq', c10_class), FF('C4', 'D3', 'explain', c10_class3, marks=3, kinds=('m3',))],
    S + '10-st2': facts(CH10_ST2) + [FF('C2', 'D2', 'mcq', c10_class), FF('C3', 'D2', 'mcq', c10_class), FF('C3', 'D3', 'explain', c10_class3, marks=3, kinds=('m3',)),
                                     FF('C2', 'D1', 'mcq', c10_class), FF('C4', 'D4', 'explain', c10_class3, marks=3), FF('C3', 'D4', 'mcq', c10_class)],
    S + '10-st3': facts(CH10_ST3) + [FF('C3', 'D3', 'numerical', c10_ocf, marks=3, kinds=('m3',)), FF('C3', 'D2', 'numerical', c10_ocf_pl, marks=2), FF('C3', 'D2', 'mcq', mcqize(c10_ocf_pl)),
                                     FF('C4', 'D4', 'multi_step', c10_ocf_rich, marks=4, kinds=('m4',)), FF('C4', 'D3', 'numerical', c10_ocf, marks=3), FF('C3', 'D4', 'multi_step', c10_ocf_rich, marks=4)],
    S + '10-st4': facts(CH10_ST4) + [FF('C3', 'D3', 'numerical', c10_icf, marks=3, kinds=('m3',)), FF('C3', 'D3', 'numerical', c10_fcf, marks=3, kinds=('m3',)),
                                     FF('C3', 'D2', 'mcq', mcqize(c10_icf)), FF('C4', 'D4', 'long', c10_full, marks=6, kinds=('m6',)), FF('C4', 'D5', 'long', c10_full, marks=6, kinds=('m6',)),
                                     FF('C4', 'D3', 'numerical', c10_fcf, marks=3), FF('C3', 'D4', 'numerical', c10_icf, marks=4, kinds=('m4',))],
}
