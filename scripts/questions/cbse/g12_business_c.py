"""CBSE class 12 business studies (NCERT Business Studies XII Part II, 054) families: ch09-ch12.

Fact tables use g12_business_a.spec() and g11_accountancy_kit.facts(); ch09 st4 adds computed trading-on-equity
problems (EPS under alternative capital structures, interest coverage ratio).
"""
from __future__ import annotations

from fractions import Fraction as Fr

from g11_accountancy_kit import FF, facts, ctx, fill
from g12_business_a import spec, S
from qbank import inr, mcq

# ================================================================ ch09 Financial management

CH09_ST1 = spec('''
T: Business finance | The money required for carrying out business activities.
T: Financial management | The management of the flow of funds: optimal procurement as well as usage of finance.
T: Wealth maximisation | The primary aim of financial management: maximising the market price of the company's equity shares.
T: Capital budgeting decision | The decision on investing funds in long-term assets for a long period.
T: Working capital decision | The decision on the level of current assets and their financing.
T: Financial risk | The chance that a firm cannot meet its fixed financial charges such as interest and repayment of debt.
L: role | aspects of a firm affected by financial management (its role) | -
- Size and composition of fixed assets | The capital budgeting decision decides the quantum of investment in fixed assets.
- Quantum of current assets and its break-up | Working capital decisions decide the amount of cash, inventory and receivables.
- Amount of long-term and short-term financing | The proportion of long-term and short-term funds affects liquidity and profitability.
- Break-up of long-term financing into debt and equity | The capital structure decides how much is raised from owners and how much is borrowed.
- All items in the profit and loss account | Interest, depreciation and other expenses depend on financial decisions.
L: tasks | tasks of financial management | -
- Ensuring availability of sufficient funds at reasonable cost | Funds must be available when needed and at a low cost.
- Ensuring effective utilisation of funds | Funds should be invested where returns exceed their cost.
- Ensuring safety of funds | Funds must be protected through proper planning and control.
- Achieving the objective of wealth maximisation | Decisions are taken so that the market value of equity shares rises.
Q: Which concept of financial management is applied? | Wealth maximisation; Capital budgeting decision; Working capital decision; Financial risk | -
- {f} accepts only those projects whose benefits exceed their cost, so that the market price of its equity shares rises. | Wealth maximisation | Decisions that add value raise the share price.
- {f} has to decide whether to buy a new plant costing ₹5 crore for making {g}. | Capital budgeting decision | It is a long-term investment in a fixed asset.
- {f} is deciding how much stock of {g} and cash to keep for day-to-day operations. | Working capital decision | It concerns the level of current assets.
- {f} has borrowed heavily and fears it may not be able to pay interest if sales fall. | Financial risk | Fixed financial charges may not be met.
- The finance manager of {f} says every decision must aim at increasing shareholders' wealth. | Wealth maximisation | This is the primary objective of financial management.
- {f} is choosing between two machines with different lives and cash flows for its {g} unit. | Capital budgeting decision | It is a choice of long-term assets.
- {f} decides how much credit to allow to its dealers of {g}. | Working capital decision | Receivables are current assets.
P: business finance | financial management
- meaning | the money required for business activities | the management of procurement and use of that money
- nature | a resource | a managerial activity
- concern | availability of funds | optimal procurement and utilisation of funds
A: The objective of financial management is to maximise the wealth of equity shareholders. | Wealth is reflected in the market price of equity shares. | a | Both true; R explains A.
A: Financial management affects every item of the profit and loss account. | Interest, depreciation and other expenses depend on financial decisions. | a | Both true; R explains A.
A: Financial management is concerned only with raising funds. | It deals with the optimal procurement as well as usage of finance. | d | A is false: it covers both procurement and use. R is true.
A: Every business needs finance. | Funds are needed to buy fixed assets and to meet day-to-day expenses. | a | Both true; R explains A.
A: A decision is in the interest of shareholders only if it increases their wealth. | A decision is beneficial when the benefit exceeds the cost. | b | Both true, but R gives the condition for a good decision, not why the shareholders' interest is measured by wealth.
TT: financial management
S+: Financial management covers both the procurement and the use of funds.
S+: The primary objective of financial management is wealth maximisation.
S+: Financial decisions affect the size and composition of fixed assets.
S+: Wealth of shareholders is reflected in the market price of equity shares.
S-: Financial management is concerned only with raising funds.
S-: The objective of financial management is to minimise the number of shareholders.
S-: Financial management does not affect the profit and loss account.
S-: Financial management deals only with the accounting records of a firm.
K: C4 D4 4 | {p}, finance manager of {f}, invests only in projects whose returns exceed their cost, keeps just enough stock of {g}, and raises funds at the lowest cost. | State the objective of financial management that {p} is pursuing. => Wealth maximisation: maximising the market price of equity shares. || Identify two tasks of financial management performed by {him}. => Ensuring effective utilisation of funds; ensuring availability of funds at reasonable cost.
K: C4 D5 6 | {f} is planning to expand. Its finance manager {p} must decide the size of the new plant, the stock of {g} to keep, the share of borrowed funds, and how much interest and depreciation the firm will bear. | Explain how financial management affects any three of these aspects of the firm. => Size and composition of fixed assets (capital budgeting); quantum of current assets (working capital decision); break-up of long-term financing into debt and equity (capital structure); items of the profit and loss account (interest, depreciation). || Why is wealth maximisation preferred as the objective? => It considers the market value of shares, which reflects the benefit to owners of every decision.
''', cat='term in financial management')

CH09_ST2 = spec('''
T: Investment decision | The decision on how the firm's funds are invested in different assets.
T: Financing decision | The decision on the quantum of finance to be raised from various long-term sources.
T: Dividend decision | The decision on how much of the profit is distributed to shareholders and how much is retained.
T: Floatation cost | The cost of raising funds, such as underwriting fees and brokerage.
T: Retained earnings | Profits kept in the business and not distributed as dividend.
T: Stable dividend | A dividend per share that is kept steady over the years.
L: inv | factors affecting capital budgeting (investment) decisions | div
- Cash flows of the project | The series of cash receipts and payments over the life of the project.
- Rate of return | Projects with a higher expected return, after considering risk, are preferred.
- Investment criteria involved | Capital budgeting techniques compare the amount invested, interest rate, cash flows and rate of return.
L: fin | factors affecting the financing decision | div
- Cost | The cost of raising funds from different sources differs; the cheapest suitable source is chosen.
- Risk | Debt is riskier for the firm than equity because interest and repayment are compulsory.
- Floatation costs | The higher the cost of raising a source, the less attractive it is.
- Cash flow position of the company | A strong cash flow position makes debt financing more viable.
- Fixed operating cost | A firm with high fixed operating costs should reduce fixed financing charges.
- Control considerations | Issue of more equity may dilute control; debt does not.
- State of the capital market | In a boom equity can be issued easily; in a depression debt may be used.
L: div | factors affecting the dividend decision | inv
- Amount of earnings | Dividends are paid out of current and past earnings.
- Stability of earnings | A company with stable earnings can declare higher dividends.
- Stability of dividends | Companies try to keep the dividend per share steady.
- Growth opportunities | Companies with good growth opportunities retain more and pay less dividend.
- Cash flow position | Payment of dividend needs cash.
- Shareholders' preference | The wishes of shareholders for a regular dividend are considered.
- Taxation policy | A higher tax on dividends may lead to lower payouts.
- Stock market reaction | An increase in dividend is usually taken as good news and the share price rises.
- Access to capital market | Companies that can easily raise funds may pay higher dividends.
- Legal constraints | The Companies Act places restrictions on the payment of dividend.
- Contractual constraints | Loan agreements may restrict dividend payments.
Q: Which financial decision is being taken? | Investment decision; Financing decision; Dividend decision; Working capital decision | -
- {f} is deciding whether to buy a new machine for its {g} plant or upgrade the old one. | Investment decision | It decides where funds are invested.
- {f} is deciding whether to raise ₹10 crore by issuing equity shares or debentures. | Financing decision | It concerns the sources of finance.
- The board of {f} is deciding how much of this year's profit to distribute among shareholders. | Dividend decision | It divides profit between dividend and retained earnings.
- {f} is deciding how much stock of {g} to hold and how much credit to give customers. | Working capital decision | It concerns current assets.
- {f} plans to open a new factory in {c}. | Investment decision | It is a long-term investment (capital budgeting).
- {f} decided to retain its entire profit this year to finance an expansion. | Dividend decision | It decided the payout and retention of profit.
- {f} is choosing between a bank loan and retained earnings to finance its expansion. | Financing decision | It is a choice of sources of funds.
Q: Which factor affecting the financing decision is highlighted? | Cost; Risk; Floatation costs; Cash flow position of the company; Fixed operating cost; Control considerations; State of the capital market | fin
- The promoters of {f} do not want to issue more equity shares as they may lose their hold over the company. | Control considerations | More equity can dilute control.
- {f} chose debentures because interest on debt is lower than the return expected by shareholders. | Cost | The cheapest suitable source is chosen.
- With the stock market booming, {f} found it easy to raise funds through a public issue of equity shares. | State of the capital market | In a boom equity is easy to raise.
- {f} has very high rent and salary commitments, so it avoids raising more debt. | Fixed operating cost | High fixed operating costs call for low fixed financing charges.
- {f} has steady and large cash inflows from {g}, so it can easily service a loan. | Cash flow position of the company | A strong cash flow supports debt.
- {f} dropped the idea of a public issue because underwriting and brokerage would be too costly. | Floatation costs | High raising costs make a source less attractive.
- {f} avoided more borrowing as it would increase the chance of default on interest and repayment. | Risk | Debt carries the risk of default.
Q: Which factor affecting the dividend decision is highlighted? | Amount of earnings; Stability of earnings; Stability of dividends; Growth opportunities; Cash flow position; Shareholders' preference; Taxation policy; Stock market reaction; Access to capital market; Legal constraints; Contractual constraints | div
- {f} paid a low dividend because it plans to set up two new plants for {g} next year. | Growth opportunities | Funds are retained for growth.
- A loan agreement of {f} with a bank says no dividend can be paid until the loan is repaid. | Contractual constraints | The lender restricts dividends.
- {f} has a steady demand for {g} every year, so it pays a regular and high dividend. | Stability of earnings | Stable earnings support higher dividends.
- {f} raised its dividend and its share price rose the next day. | Stock market reaction | A rise in dividend is taken as good news.
- {f} has made good profits but has little cash in hand, so it declared a lower dividend. | Cash flow position | Payment of dividend requires cash.
- {f} keeps its dividend at ₹5 per share every year even when profits vary a little. | Stability of dividends | Companies try to smooth dividend per share.
- Most shareholders of {f} are retired people who want a regular income, so it pays a steady dividend. | Shareholders' preference | The wishes of shareholders are considered.
- {f} can raise funds easily from the market at any time, so it distributes a large part of its profit. | Access to capital market | Easy access to funds allows higher dividends.
- A higher tax on dividends led {f} to reduce its dividend payout. | Taxation policy | Higher tax on dividends lowers payouts.
F: fin | Control considerations | debt does not dilute control; equity carries voting rights; promoters keep their hold through debt
F: fin | Cost | interest on debt is tax-deductible; debt is usually cheaper than equity; the cheapest suitable source is chosen
F: fin | Risk | debt carries compulsory interest and repayment; equity has no obligation to pay dividend; too much debt increases financial risk
F: div | Growth opportunities | more earnings are retained; retained earnings are a cheap internal source; dividend payout falls
F: div | Stability of earnings | stable earnings support higher dividends; firms with volatile earnings pay less; regular dividends become possible
P: investment decision | dividend decision
- concern | where the funds are to be invested | how much profit is to be distributed and how much retained
- effect | determines the size and composition of assets | determines retained earnings available for growth
- example | buying a new machine | declaring a dividend of 20%
P: equity | debt
- cost | relatively costlier | cheaper as interest is tax-deductible
- risk to the company | no fixed obligation to pay dividend | interest and repayment are compulsory
- control | may dilute control | does not dilute control
- return to investors | dividend depends on profit | fixed rate of interest
A: Debt is considered the cheapest source of finance. | Interest on debt is a tax-deductible expense. | a | Both true; R explains A.
A: Companies with good growth opportunities pay lower dividends. | They retain more of their earnings to finance growth. | a | Both true; R explains A.
A: A company with high fixed operating costs should use more debt. | Fixed operating costs increase business risk. | d | A is false: such a company should reduce fixed financing charges. R is true.
A: Issue of more equity shares may dilute control of the existing shareholders. | Equity shareholders have voting rights. | a | Both true; R explains A.
A: Dividend can be paid even if the company has no cash. | Dividends are paid out of profits. | d | A is false: payment of dividend needs cash. R is true.
A: Capital budgeting decisions are irreversible except at a huge cost. | They involve investment in long-term assets. | a | Both true; R explains A.
TT: financial decisions
S+: The financing decision is about the sources of long-term funds.
S+: A company with stable earnings can declare higher dividends.
S+: Debt is cheaper than equity because interest is tax-deductible.
S+: Loan agreements may restrict the payment of dividends.
S-: A dividend decision is about choosing a new plant.
S-: Debt does not involve any risk for the company.
S-: Companies with many growth opportunities usually pay high dividends.
S-: Floatation cost is the interest paid on borrowed funds.
K: C4 D4 4 | {f}, a {g} company, made a large profit. It has two new projects lined up, its promoters do not want to dilute control, and the stock market is in a slump. | Should {f} pay a high dividend? Give two reasons. => No: growth opportunities need retained earnings; the slump makes raising fresh equity difficult. || Which source of finance should it use if retained earnings are not enough? Why? => Debt (loan or debentures): it does not dilute control and is cheaper because interest is tax-deductible.
K: C4 D5 6 | The directors of {f} must decide: (a) whether to set up a new {g} unit in {c}; (b) whether to finance it with debentures or equity; (c) how much of this year's profit to distribute. | Name the financial decision in each of (a), (b) and (c). => (a) Investment (capital budgeting) decision; (b) financing decision; (c) dividend decision. || State one factor affecting each of these decisions. => (a) Cash flows of the project / rate of return; (b) cost / risk / control considerations; (c) amount of earnings / growth opportunities / cash flow position.
''', cat='financial term')

CH09_ST3 = spec('''
T: Financial planning | Preparation of a financial blueprint of an organisation's future operations.
T: Financial plan | A statement estimating the amount of funds needed, their timing and their sources.
T: Short-term financial plan | A financial plan covering a period of up to one year, such as a budget.
T: Long-term financial plan | A financial plan for a period of three to five years.
L: obj | objectives of financial planning | -
- To ensure availability of funds whenever required | It estimates the funds needed, the timing and the sources.
- To see that the firm does not raise resources unnecessarily | Excess funding adds to cost; shortage hampers operations.
L: imp | points of importance of financial planning | -
- Helps in forecasting what may happen in future | It prepares the firm for different business situations.
- Helps in avoiding business shocks and surprises | It anticipates financial needs in advance.
- Helps in coordinating various business functions | It links sales, production and finance through clear policies.
- Reduces waste, duplication of efforts and gaps in planning | Detailed plans make clear who does what.
- Tries to link the present with the future | It plans today for the needs of tomorrow.
- Provides a link between investment and financing decisions | It matches the funds needed with their sources.
- Makes evaluation of actual performance easier | Detailed objectives make comparison of actual results possible.
Q: Which point of importance of financial planning is shown? | Helps in forecasting what may happen in future; Helps in avoiding business shocks and surprises; Helps in coordinating various business functions; Reduces waste, duplication of efforts and gaps in planning; Links the present with the future; Makes evaluation of actual performance easier | -
- {f} prepared three estimates of its fund needs: for high, normal and low sales of {g}. | Helps in forecasting what may happen in future | It prepares for different situations.
- Because {f} had arranged a credit line in advance, a sudden rise in raw material prices did not stop production. | Helps in avoiding business shocks and surprises | Needs were anticipated in advance.
- The sales and production plans of {f} were matched with its funds through one financial plan. | Helps in coordinating various business functions | Functions are linked through clear policies.
- The finance plan of {f} makes clear which department raises which funds, so no two departments raise loans for the same purpose. | Reduces waste, duplication of efforts and gaps in planning | Clarity avoids duplication.
- {f} compared its actual expenditure with its financial plan at the end of the year. | Makes evaluation of actual performance easier | Detailed objectives are a standard for comparison.
- Today {f} sets aside funds for the machines it will need to replace in five years. | Links the present with the future | Present action prepares for future needs.
A: Financial planning ensures that the firm does not raise resources unnecessarily. | Excess funding adds to the cost of capital. | a | Both true; R explains A.
A: Financial planning helps in avoiding business shocks and surprises. | It anticipates financial needs in advance. | a | Both true; R explains A.
A: Financial planning is concerned only with raising funds. | It also aims at ensuring funds are available whenever required. | d | A is false: it covers estimating needs, timing and sources. R is true.
A: Financial planning makes evaluation of actual performance easier. | It spells out detailed objectives for the various business segments. | a | Both true; R explains A.
TT: financial planning
S+: Financial planning prepares a financial blueprint of future operations.
S+: Financial planning aims at ensuring availability of funds whenever required.
S+: Financial planning links investment and financing decisions.
S-: Financial planning encourages raising as much money as possible.
S-: Financial planning deals only with the past performance of the firm.
S-: Financial planning has no link with sales and production plans.
S-: A long-term financial plan usually covers a period of one month.
K: C4 D4 4 | {f} often ran out of cash to buy raw material for {g}, while at other times it had idle funds earning nothing. | What concept of financial management can solve this problem? => Financial planning. || State its two objectives. => To ensure availability of funds whenever required; to see that the firm does not raise resources unnecessarily.
K: C4 D5 6 | {p}, the CFO of {f}, prepared a five-year plan estimating fund needs for different levels of sales of {g}, matched them with sources, and gave each department a clear target against which results are compared. | Identify the concept. => Financial planning. || Explain three points of its importance seen in the case. => Helps forecast what may happen (different levels of sales); links investment and financing decisions (needs matched with sources); makes evaluation of actual performance easier (targets for comparison).
''', cat='term')

CH09_ST4 = spec('''
T: Capital structure | The mix between owners' funds and borrowed funds.
T: Financial leverage | The proportion of debt in the overall capital of a firm.
T: Trading on equity | An increase in profit per equity share due to the use of sources of finance with a fixed financial charge.
T: Debt-equity ratio | Debt divided by equity, a measure of the capital structure.
T: Interest coverage ratio | The number of times earnings before interest and tax cover the interest obligation.
T: Debt service coverage ratio | A ratio of cash profits to the interest and principal repayments due.
L: cs | factors affecting the choice of capital structure | -
- Cash flow position | Debt is used only if cash flows are enough to meet fixed payments.
- Interest coverage ratio | The higher the ratio, the more debt the company can use.
- Debt service coverage ratio | A higher ratio means a better ability to service debt.
- Return on investment | If ROI is higher than the rate of interest, debt can be used to increase EPS.
- Cost of debt | When debt can be raised at a low rate, more debt can be used.
- Tax rate | A higher tax rate makes debt cheaper as interest is tax-deductible.
- Cost of equity | Too much debt raises shareholders' risk and their expected return.
- Floatation costs | The cost of a public issue affects the choice of source.
- Risk consideration | Total risk (business plus financial) must stay within limits.
- Flexibility | Some borrowing capacity is kept unused for the future.
- Control | Debt does not dilute control; equity does.
- Regulatory framework | Issue of shares and debentures must follow SEBI guidelines.
- Stock market conditions | In a boom equity is easy to issue; in a depression debt may be used.
- Capital structure of other companies | Industry norms are used as a guide.
Q: Which factor affecting capital structure is highlighted? | Cash flow position; Interest coverage ratio; Return on investment; Cost of debt; Tax rate; Flexibility; Control; Regulatory framework; Stock market conditions; Capital structure of other companies | cs
- {f} earns a return of 18% on its investment while banks lend at 10%, so it raised more debt. | Return on investment | ROI above the cost of debt favours debt.
- {f} keeps part of its borrowing capacity unused to meet emergencies. | Flexibility | Unused capacity gives room for the future.
- The EBIT of {f} is 8 times its interest, so lenders readily give it more loans. | Interest coverage ratio | A high ratio supports more debt.
- {f} studied the debt-equity ratios of other {g} makers before deciding its own. | Capital structure of other companies | Industry norms act as a guide.
- {f} preferred debentures as the promoters did not want to share voting power. | Control | Debt does not dilute control.
- A rise in the corporate tax rate made borrowing more attractive for {f}. | Tax rate | Interest is tax-deductible, so debt becomes cheaper.
- {f} has irregular cash inflows from {g}, so it avoids heavy borrowing. | Cash flow position | Fixed payments need regular cash.
- {f} could borrow at only 7% because of falling interest rates, so it raised more debt. | Cost of debt | Cheap debt can be used more.
- {f} issued equity shares when the stock market was booming. | Stock market conditions | Equity is easy to raise in a boom.
- {f} had to follow SEBI guidelines while issuing debentures to the public. | Regulatory framework | Issues must follow the law.
A: Trading on equity is favourable only when the rate of return on investment is higher than the rate of interest. | The fixed interest is then less than the earnings on borrowed funds. | a | Both true; R explains A.
A: Debt is a cheaper source of finance than equity. | Interest on debt is tax-deductible. | a | Both true; R explains A.
A: A company with a high interest coverage ratio can use more debt. | A higher interest coverage ratio means a lower risk of default on interest. | a | Both true; R explains A.
A: Increasing debt always increases earnings per share. | Debt carries a fixed rate of interest. | d | A is false: EPS rises only if ROI exceeds the cost of debt. R is true.
A: A higher proportion of debt increases financial risk. | Interest and repayment are compulsory obligations. | a | Both true; R explains A.
TT: capital structure
S+: Capital structure is the mix of owners' funds and borrowed funds.
S+: Trading on equity is favourable when ROI is higher than the rate of interest.
S+: Interest on debt is a tax-deductible expense.
S+: A higher proportion of debt increases financial risk.
S-: Debt is costlier than equity because interest is not tax-deductible.
S-: Issue of debentures dilutes the control of equity shareholders.
S-: Trading on equity always increases EPS.
S-: Financial leverage is the proportion of equity in total capital.
K: C4 D4 4 | {f} has a total capital of ₹50 lakh, all in equity. It earns 15% on investment and can borrow at 9%. The tax rate is low and its cash flows from {g} are steady. | Should {f} use debt in its capital structure? Explain using two factors. => Yes: ROI (15%) is higher than the cost of debt (9%), so trading on equity will raise EPS; steady cash flows can meet the interest. || Name the concept and state one risk of too much debt. => Trading on equity (financial leverage); too much debt raises financial risk and the risk of default.
K: C4 D5 6 | {f} wants to raise ₹20 crore. Its promoters want to keep control, its interest coverage ratio is high, and the stock market is in a slump, but it also wants to keep some borrowing capacity for the future. | Identify four factors affecting capital structure in the case. => Control; interest coverage ratio; stock market conditions; flexibility. || Which source would you recommend and why? => Mainly debt: it keeps control, the high ICR shows it can be serviced, and equity is hard to raise in a slump; but not to the full extent, to keep flexibility.
''', cat='term')


def _ri(r, lo, hi, step):
    return r.randrange(lo // step, hi // step + 1) * step


def _eps(r):
    """Trading on equity: EPS under two capital structures (face value ₹10, tax 30%, NCERT style)."""
    for _ in range(200):
        total = _ri(r, 2000000, 10000000, 1000000)
        roi = r.choice([8, 10, 12, 14, 15, 16, 18, 20])
        rate = r.choice([6, 7, 8, 9, 10, 11, 12, 13, 14])
        if rate == roi:
            continue
        tax = r.choice([30, 40])
        share = r.choice([2, 4, 5, 6, 8]) * total // 10   # debt in plan B
        ebit = total * roi // 100
        intr = share * rate // 100
        sa = total // 10
        sb = (total - share) // 10
        eps_a = Fr(ebit * (100 - tax), 100) / sa
        eps_b = Fr((ebit - intr) * (100 - tax), 100) / sb
        if (ebit - intr) <= 0:
            continue
        return total, roi, rate, tax, share, ebit, intr, sa, sb, eps_a, eps_b
    raise ValueError('no eps')


def _rs(x):
    return f'₹{float(x):.2f}'


def c9_eps(r):
    total, roi, rate, tax, debt, ebit, intr, sa, sb, ea, eb = _eps(r)
    d = ctx(r)
    fav = 'favourable' if roi > rate else 'unfavourable'
    better = 'Plan B' if eb > ea else 'Plan A'
    stem = (f'{d["f"]} needs {inr(total)} for a new {d["g"]} unit and expects earnings before interest and tax of '
            f'{inr(ebit)} (return on investment {roi}%). Plan A: raise the whole amount by equity shares of ₹10 each. '
            f'Plan B: raise {inr(debt)} by {rate}% debentures and the rest by equity shares of ₹10 each. The tax rate is {tax}%. '
            f'Calculate EPS under both plans and state whether trading on equity is favourable.')
    tb = (ebit - intr) * tax // 100
    ans = (f'Plan A: EBIT {inr(ebit)}, tax {inr(ebit * tax // 100)}, profit after tax {inr(ebit - ebit * tax // 100)}, '
           f'shares {_q(sa)}; EPS = {_rs(ea)}. Plan B: EBIT {inr(ebit)} less interest {inr(intr)} = {inr(ebit - intr)}, '
           f'tax {inr(tb)}, profit after tax {inr(ebit - intr - tb)}, shares {_q(sb)}; EPS = {_rs(eb)}. '
           f'ROI {roi}% is {"higher" if roi > rate else "lower"} than the rate of interest {rate}%, so trading on equity is {fav} '
           f'({better} gives the higher EPS).')
    return {'stem': stem, 'answer': ans,
            'key': f'1½ marks each for EPS under Plan A and Plan B; 1 mark for the conclusion. {ans}'}


def _q(n):
    s = str(n)
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ','.join(parts + [tail])


def c9_tradmcq(r):
    roi = r.choice([8, 10, 12, 14, 15, 16, 18, 20, 22])
    rate = r.choice([x for x in (6, 7, 8, 9, 10, 11, 12, 13, 14, 16) if x != roi])
    d = ctx(r)
    good = 'Trading on equity will increase EPS, as ROI is higher than the rate of interest' if roi > rate else \
        'Trading on equity will reduce EPS, as ROI is lower than the rate of interest'
    wrong = ['Trading on equity will reduce EPS, as ROI is lower than the rate of interest' if roi > rate else
             'Trading on equity will increase EPS, as ROI is higher than the rate of interest',
             'EPS will not be affected by the use of debt', 'Debt always reduces the EPS of a company']
    return mcq(f'{d["f"]} earns a return of {roi}% on its total investment and can borrow at {rate}% per annum. '
               f'What will be the effect of using more debt?', good, wrong,
               f'ROI {roi}% vs interest {rate}%: {good[0].lower() + good[1:]}.', r)


def c9_icr(r):
    i = _ri(r, 100000, 1500000, 50000)
    k = r.choice([Fr(3, 2), 2, Fr(5, 2), 3, 4, 5, 6, 8])
    ebit = int(i * k)
    d = ctx(r)
    kv = f'{float(k):g}'
    wrong = [f'{float(x):g} times' for x in {k + 1, k * 2, Fr(ebit - i, i), max(Fr(1, 2), k - Fr(1, 2))} if x != k][:3]
    if len(wrong) < 3:
        wrong.append(f'{float(k * 3):g} times')
    return mcq(f'{d["f"]} has earnings before interest and tax of {inr(ebit)} and interest of {inr(i)}. '
               f'What is its interest coverage ratio?', f'{kv} times', wrong[:3],
               f'ICR = EBIT ÷ interest = {inr(ebit)} ÷ {inr(i)} = {kv} times. A higher ratio means the firm can use more debt.', r)


CH09_ST5 = spec('''
T: Fixed capital | Investment in long-term assets such as plant, machinery and buildings.
T: Working capital | Investment in current assets such as cash, inventory and receivables.
T: Gross working capital | The total investment in current assets.
T: Net working capital | The excess of current assets over current liabilities.
T: Operating cycle | The time from the purchase of raw material to the realisation of cash from sales.
T: Capital budgeting | The management of fixed capital: decisions on investment in long-term assets.
L: fimp | reasons why fixed capital decisions are important | -
- Long-term growth | They affect the growth and profitability of the business over a long period.
- Large amount of funds involved | A large part of the funds is blocked in fixed assets.
- Risk involved | Wrong decisions can affect the firm's survival.
- Irreversible decisions | They cannot be reversed without a huge loss.
L: fix | factors affecting the requirement of fixed capital | -
- Nature of business | A manufacturing firm needs more fixed capital than a trading firm.
- Scale of operations | A larger scale needs more fixed capital.
- Choice of technique | A capital-intensive technique needs more fixed capital than a labour-intensive one.
- Technology upgradation | Industries where assets become obsolete fast need more fixed capital.
- Growth prospects | Higher growth plans need more fixed capital.
- Diversification | Entering new lines of business needs more fixed capital.
- Financing alternatives | Availability of leasing reduces the need for fixed capital.
- Level of collaboration | Sharing facilities with other firms reduces the requirement.
L: wc | factors affecting the requirement of working capital | -
- Nature of business | A trading firm needs more working capital than a service firm.
- Scale of operations | A larger scale needs more working capital.
- Business cycle | In a boom more working capital is needed than in a depression.
- Seasonal factors | More working capital is needed in the peak season.
- Production cycle | A longer production cycle needs more working capital.
- Credit allowed | Liberal credit to customers needs more working capital.
- Credit availed | Credit from suppliers reduces the working capital needed.
- Operating efficiency | Efficient firms need less working capital.
- Availability of raw material | Easy availability means less stock and less working capital.
- Growth prospects | Higher growth needs more working capital.
- Level of competition | Higher competition means larger stocks and more credit, so more working capital.
- Inflation | Rising prices increase the working capital needed.
Q: Which factor affecting the requirement of fixed capital is highlighted? | Nature of business; Scale of operations; Choice of technique; Technology upgradation; Growth prospects; Diversification; Financing alternatives; Level of collaboration | -
- {f} leases its machines for making {g} instead of buying them. | Financing alternatives | Leasing reduces the need to buy assets.
- {f} uses automated machines while its rival uses manual labour. | Choice of technique | A capital-intensive technique needs more fixed capital.
- {f}, a computer services firm, has to replace its hardware every few years. | Technology upgradation | Fast obsolescence raises fixed capital needs.
- {f}, which makes {g}, has decided to start a cement plant as well. | Diversification | A new line of business needs more fixed assets.
- {f} and {f2} share a common warehouse and testing laboratory. | Level of collaboration | Sharing facilities reduces fixed capital.
- {f} is a large steel plant, while {f2} is a small workshop. | Scale of operations | A larger scale needs more fixed capital.
- {f}, a manufacturer of {g}, needs more fixed capital than a retail store selling the same goods. | Nature of business | Manufacturing needs more fixed assets than trading.
Q: Which factor affecting the requirement of working capital is highlighted? | Business cycle; Seasonal factors; Production cycle; Credit allowed; Credit availed; Operating efficiency; Availability of raw material; Inflation; Level of competition | wc
- {f}, a maker of woollen garments, needs more working capital from September to December. | Seasonal factors | Peak-season sales need more stock and funds.
- {f} gets 90 days' credit from its suppliers but sells {g} for cash. | Credit availed | Supplier credit reduces working capital needs.
- {f} gives its dealers 120 days' credit to push the sales of {g}. | Credit allowed | Liberal credit locks up funds in receivables.
- {f} builds ships, which take more than a year to complete. | Production cycle | A long production cycle needs more working capital.
- Because prices of raw materials are rising fast, {f} needs more funds for the same output. | Inflation | Rising prices increase working capital needs.
- During the economic boom, {f} increased its stock of {g} and its credit sales. | Business cycle | A boom needs more working capital.
- {f} has to keep large stocks and allow generous credit because many rivals sell {g} in {c}. | Level of competition | Competition increases stock and credit.
- {f} uses its inventory and cash so efficiently that it needs less working capital than its rivals. | Operating efficiency | Efficiency reduces working capital.
- Raw material for {f} is available all year round in {c}, so it keeps small stocks. | Availability of raw material | Easy availability reduces stock needs.
F: wc | Seasonal factors | peak season needs more stock; more funds needed in busy months; requirement falls in the off-season
F: wc | Credit allowed | receivables increase; funds are blocked with customers; liberal credit policy raises working capital
F: wc | Production cycle | raw material and work-in-progress are held longer; longer cycle locks up more funds; working capital rises with cycle length
P: fixed capital | working capital
- meaning | investment in long-term assets | investment in current assets
- period | long term | short term
- decision | capital budgeting decision | working capital decision
- sources | long-term sources | mainly short-term sources
- examples | land, building, machinery | cash, inventory, receivables
A: A trading concern needs less fixed capital than a manufacturing concern. | A trading concern does not need plant and machinery for production. | a | Both true; R explains A.
A: A longer production cycle requires more working capital. | Funds remain blocked in raw material and work-in-progress for a longer time. | a | Both true; R explains A.
A: Credit availed from suppliers increases the working capital requirement. | Suppliers' credit allows the firm to pay later. | d | A is false: credit availed reduces the requirement. R is true.
A: Fixed capital decisions are irreversible. | They involve huge sums invested for a long period. | a | Both true; R explains A.
A: More working capital is needed during a boom. | Sales and production are higher during a boom. | a | Both true; R explains A.
A: Leasing increases the need for fixed capital. | A leased asset is used without buying it. | d | A is false: leasing reduces fixed capital needs. R is true.
TT: fixed and working capital
S+: Net working capital is current assets minus current liabilities.
S+: A manufacturing concern needs more fixed capital than a trading concern.
S+: Seasonal businesses need more working capital in the peak season.
S+: Capital budgeting decisions are generally irreversible.
S-: Working capital is invested in plant and machinery.
S-: Credit availed from suppliers increases working capital needs.
S-: A shorter production cycle needs more working capital.
S-: Fixed capital decisions involve small amounts of funds.
K: C4 D4 4 | {f} makes {g} using automated machines and sells mainly in the festive season, allowing dealers 90 days' credit. | Identify one factor raising its fixed capital need. => Choice of technique: capital-intensive (automated) production. || Identify two factors raising its working capital need. => Seasonal factors (festive season sales); credit allowed (90 days to dealers).
K: C4 D5 6 | {p} runs {f}, a {g} company that is expanding into a new state and also starting a hotel business. Raw material prices are rising, and competitors offer long credit to dealers. | Identify two factors affecting fixed capital in the case. => Growth prospects (expansion); diversification (hotel business). || Identify two factors affecting working capital in the case. => Inflation (rising prices); level of competition (long credit offered by rivals). || Why are fixed capital decisions important? => Long-term growth, large funds, high risk and irreversibility.
''', cat='term')

# ================================================================ ch10 Financial markets

CH10_ST1 = spec('''
T: Financial market | A market for the creation and exchange of financial assets.
T: Money market | A market for short-term funds that deals in instruments with a maturity of up to one year.
T: Treasury bill | A zero-coupon short-term instrument issued by the RBI on behalf of the Government of India, issued at a discount and repaid at par.
T: Commercial paper | A short-term unsecured promissory note, negotiable and transferable by endorsement and delivery, issued by large creditworthy companies.
T: Call money | Short-term finance repayable on demand, with a maturity of one day to fifteen days, used for inter-bank transactions.
T: Certificate of deposit | An unsecured, negotiable, short-term instrument in bearer form issued by commercial banks and development financial institutions.
T: Commercial bill | A bill of exchange used by firms to finance their working capital needs, which can be discounted with a bank.
T: Call rate | The interest rate paid on call money loans.
L: fn | functions of a financial market | -
- Mobilisation of savings and channelising them into the most productive uses | It links savers with investors.
- Facilitating price discovery | The price of a financial asset is decided by the demand and supply of funds.
- Providing liquidity to financial assets | Investors can easily convert assets into cash.
- Reducing the cost of transactions | It provides information about securities, saving time and money.
L: mm | instruments of the money market | cm
- Treasury bill | Zero-coupon government security issued at a discount and repaid at par.
- Commercial paper | Unsecured promissory note issued by large creditworthy companies for 15 days to one year.
- Call money | Inter-bank loan repayable on demand, for one to fifteen days.
- Certificate of deposit | Negotiable bearer instrument issued by banks during tight liquidity.
- Commercial bill | Bill of exchange discounted with banks to finance working capital.
L: cm | instruments of the capital market | mm
- Equity shares | Ownership securities of a company.
- Preference shares | Shares with preferential rights to dividend and repayment of capital.
- Debentures | Long-term debt instruments carrying a fixed rate of interest.
- Bonds | Long-term debt securities issued by companies or government.
Q: Which money market instrument is described? | Treasury bill; Commercial paper; Call money; Certificate of deposit; Commercial bill | -
- {f} needs funds for 90 days to meet a temporary need and, being a large creditworthy company, issues an unsecured promissory note. | Commercial paper | Large companies raise short-term funds through commercial paper.
- A bank short of funds to maintain its cash reserve ratio borrows from another bank for two days. | Call money | Inter-bank loans repayable on demand.
- The RBI issues an instrument on behalf of the Government of India for 182 days at a discount. | Treasury bill | It is a zero-coupon government instrument.
- {f} draws a bill on its buyer of {g}; the accepted bill is discounted with a bank to get cash. | Commercial bill | A trade bill discounted with a bank becomes a commercial bill.
- During a period of tight liquidity, a bank issues a negotiable bearer instrument to mobilise large funds. | Certificate of deposit | CDs are issued by banks when deposit growth is low.
- {f} raises funds for 120 days through a note, using them as bridge finance while its share issue is completed. | Commercial paper | CP is often used for bridge financing.
- An instrument with a minimum amount of ₹25,000 is issued at a discount by the government and repaid at par. | Treasury bill | T-bills are zero-coupon bonds.
A: A treasury bill is known as a zero-coupon bond. | It is issued at a discount and redeemed at par, so no interest is paid separately. | a | Both true; R explains A.
A: Call money is used mainly for inter-bank transactions. | Banks borrow to maintain their cash reserve ratio. | a | Both true; R explains A.
A: Commercial paper is a secured instrument. | It is issued by large and creditworthy companies. | d | A is false: commercial paper is unsecured. R is true.
A: A financial market helps in price discovery. | The price of financial assets is decided by the interaction of buyers and sellers. | a | Both true; R explains A.
A: The money market deals in long-term funds. | Money market instruments have a maturity of up to one year. | d | A is false; R is true.
TT: the money market
S+: Treasury bills are issued by the RBI on behalf of the Government of India.
S+: Commercial paper is an unsecured promissory note.
S+: Call money is repayable on demand.
S+: The money market deals in funds with a maturity of up to one year.
S-: Treasury bills are issued at a premium.
S-: Commercial paper is issued by small firms with poor credit ratings.
S-: Call money has a maturity of five years.
S-: Certificates of deposit are issued by the stock exchange.
K: C4 D4 4 | Bank A was short of cash on Friday and borrowed from Bank B until Monday. Meanwhile, {f}, a large creditworthy {g} company, issued an unsecured note for 90 days to meet its seasonal needs. | Identify the two money market instruments. => Call money (inter-bank loan repayable on demand); commercial paper (unsecured promissory note by a large company). || State one feature of each. => Call money: maturity of 1 to 15 days; commercial paper: negotiable and transferable by endorsement and delivery, 15 days to one year.
K: C4 D5 6 | {p} saves money in shares and bonds through a broker. The money reaches {f}, which uses it to build a new plant. {He} can sell the shares any time, the price is set by demand and supply, and brokerage is low. | Identify the market and four functions it performs in the case. => Financial market: mobilisation of savings and channelising them into productive uses; providing liquidity; facilitating price discovery; reducing the cost of transactions.
''', cat='money market term')

CH10_ST2 = spec('''
T: Capital market | A market for medium and long-term funds, dealing in instruments with a maturity of more than one year.
T: Primary market | The new issues market, where new securities are sold for the first time.
T: Secondary market | The stock market, where existing securities are bought and sold.
T: Offer through prospectus | Inviting subscription from the public through the issue of a prospectus.
T: Offer for sale | Securities are sold to an intermediary, such as an issuing house, which resells them to the public.
T: Private placement | Allotment of securities to institutional investors and some selected individuals.
T: Rights issue | Offer of new shares to existing shareholders in proportion to their holding.
T: e-IPO | A public issue of securities through the online system of a stock exchange.
L: meth | methods of floatation in the primary market | -
- Offer through prospectus | The public is invited to subscribe through a prospectus and advertisements.
- Offer for sale | An issuing house buys the securities and resells them to the public.
- Private placement | Securities are allotted to institutional investors and selected individuals.
- Rights issue | New shares are first offered to existing shareholders in proportion to their holding.
- e-IPOs | Securities are issued through the online system of a stock exchange.
Q: Which method of floatation is used? | Offer through prospectus; Offer for sale; Private placement; Rights issue; e-IPOs | -
- {f} offered one new share for every four shares held to its existing shareholders. | Rights issue | Existing shareholders get new shares in proportion to their holding.
- {f} sold its entire issue to an issuing house, which then sold the shares to the public at a higher price. | Offer for sale | The intermediary resells to the public.
- {f} allotted its shares to mutual funds and banks without going to the public. | Private placement | Securities go to selected institutional investors.
- {f} invited the public to subscribe to its shares through a prospectus and newspaper advertisements. | Offer through prospectus | The public subscribes through the prospectus.
- {f} issued its shares through the online system of the stock exchange, appointing registered brokers to accept applications. | e-IPOs | The issue is made online through the exchange.
- {f}, a newly listed company, raised funds quickly and cheaply by allotting shares to a few insurance companies. | Private placement | It avoids the cost of a public issue.
P: money market | capital market
- participants | RBI, banks, financial institutions and large companies | individuals, companies, banks, FIIs and mutual funds
- instruments | treasury bills, commercial paper, call money, CDs and commercial bills | equity shares, preference shares, debentures and bonds
- investment outlay | large sums are needed as instruments have high value | small amounts can be invested as securities have low value
- duration | up to one year | more than one year
- liquidity | highly liquid | marketable but less liquid
- safety | safer, with little risk of default | riskier as to both return and principal
- expected return | lower | higher
P: primary market | secondary market
- function | sale of new securities | trading of existing securities
- participants | companies sell to investors | investors trade among themselves
- location | no fixed geographical location | located at specified places (stock exchanges)
- price determination | fixed by the management of the company | determined by demand and supply
- capital formation | directly promotes capital formation | indirectly promotes capital formation
A: The primary market directly promotes capital formation. | New funds flow from investors to companies through it. | a | Both true; R explains A.
A: Prices in the secondary market are fixed by the company. | Prices in the secondary market depend on demand and supply. | d | A is false; R is true.
A: Capital market instruments are riskier than money market instruments. | They have a longer maturity. | a | Both true; R explains A.
A: A rights issue is offered to the general public. | In a rights issue new shares are offered to existing shareholders. | d | A is false; R is true.
A: Private placement is a cheaper method of floatation. | It avoids many of the costs of a public issue. | a | Both true; R explains A.
TT: the capital market
S+: The primary market deals in new securities.
S+: In the secondary market prices are determined by demand and supply.
S+: The capital market deals in funds for more than one year.
S+: A rights issue is made to existing shareholders.
S-: The secondary market directly provides funds to companies.
S-: The primary market has a fixed place of business.
S-: Capital market instruments are less risky than money market instruments.
S-: An offer for sale is made only to existing shareholders.
K: C4 D4 4 | {f} issued shares to the public for the first time. A year later, {p} bought 100 of those shares from another investor through a stock broker. | Identify the markets involved in the two transactions. => First issue: primary market; purchase from another investor: secondary market. || State two differences between them. => Primary deals in new securities, secondary in existing ones; primary prices are fixed by the company, secondary prices by demand and supply; primary directly promotes capital formation.
K: C4 D5 6 | {f} needs ₹50 crore for 10 years and ₹2 crore for 60 days. | In which market should each amount be raised? => ₹50 crore: capital market; ₹2 crore for 60 days: money market. || Distinguish between the two markets on four bases. => Duration (up to one year vs more than one year); instruments (CP, T-bills vs shares, debentures); liquidity (high vs lower); safety and return (safer, lower return vs riskier, higher return).
''', cat='term')

CH10_ST3 = spec('''
T: Stock exchange | An association, organisation or body of individuals established for assisting, regulating and controlling business in buying, selling and dealing in securities.
T: Dematerialisation | Holding securities in electronic form instead of physical certificates.
T: Depository | An institution that holds securities in electronic form, such as NSDL and CDSL.
T: Depository participant | An agent of a depository through whom an investor opens a demat account.
T: Rolling settlement | Settlement of trades a fixed number of working days after the trade date.
T: Screen-based trading | Electronic trading in which buyers and sellers interact through computers instead of on a trading floor.
L: fn | functions of a stock exchange | -
- Providing liquidity and marketability to existing securities | Investors can sell securities easily at any time.
- Pricing of securities | Prices are determined by the forces of demand and supply.
- Safety of transactions | Trading takes place under well-defined rules regulated by SEBI.
- Contributes to economic growth | Savings flow into the most productive investments.
- Spreading of equity cult | It encourages wider share ownership through investor education.
- Providing scope for speculation | It allows healthy speculation within the rules.
L: proc | steps in the trading and settlement procedure | -
- Selection of a broker | A SEBI-registered broker is chosen and a broker-client agreement is signed.
- Opening a demat account | A demat account is opened with a depository participant; PAN is needed.
- Placing the order | The investor gives clear instructions to the broker to buy or sell.
- Executing the order | The broker buys or sells on the screen-based system and issues a contract note.
- Settlement | Securities and funds are exchanged; shares are credited to the buyer's demat account.
Q: Which function of a stock exchange is highlighted? | Providing liquidity and marketability to existing securities; Pricing of securities; Safety of transactions; Contributes to economic growth; Spreading of equity cult; Providing scope for speculation | -
- {p} needed money urgently and sold {his} shares within minutes through the stock exchange. | Providing liquidity and marketability to existing securities | Securities can be converted into cash easily.
- The price of shares of {f} rose as more buyers wanted them after good results. | Pricing of securities | Prices depend on demand and supply.
- {p} is confident about trading because all members follow SEBI rules. | Safety of transactions | Trading is regulated by well-defined rules.
- The exchange runs investor awareness programmes in schools and colleges in {c}. | Spreading of equity cult | It encourages wider share ownership.
- Savings of thousands of investors reach growing companies such as {f} through the exchange. | Contributes to economic growth | Savings are channelled into productive investment.
- {p} buys shares expecting a price rise and sells them a week later, within the rules of the exchange. | Providing scope for speculation | Healthy speculation is allowed.
Q: Which step of the trading procedure is described? | Selection of a broker; Opening a demat account; Placing the order; Executing the order; Settlement | -
- {p} signed an agreement with a SEBI-registered broker and gave {his} PAN and KYC details. | Selection of a broker | A broker is chosen first.
- {p} opened an account with a depository participant to hold {his} shares electronically. | Opening a demat account | Shares are held in demat form.
- {p} told {his} broker to buy 50 shares of {f} at not more than ₹400 each. | Placing the order | Clear instructions are given to the broker.
- The broker bought the shares on the screen-based system and sent {p} a contract note. | Executing the order | The order is executed and confirmed.
- The shares bought by {p} were credited to {his} demat account and the payment was transferred. | Settlement | Securities and funds are exchanged.
P: NSE | BSE
- year of origin | recognised as a stock exchange in 1993 | set up in 1875, the oldest stock exchange in Asia
- main index | Nifty 50 (50 companies) | Sensex (30 companies)
- location of head office | Mumbai | Mumbai (Dalal Street)
A: A stock exchange provides liquidity to securities. | Investors can sell securities easily at any time. | a | Both true; R explains A.
A: Shares bought on a stock exchange today are held in electronic form. | Dematerialisation converts physical certificates into electronic holdings. | a | Both true; R explains A.
A: Prices on a stock exchange are fixed by SEBI. | SEBI regulates the working of stock exchanges. | d | A is false: prices are fixed by demand and supply. R is true.
A: The Bombay Stock Exchange is the oldest stock exchange in Asia. | It was set up in 1875. | a | Both true; R explains A.
A: A demat account is opened with a depository participant. | The depository participant is the agent of the depository. | a | Both true; R explains A.
TT: stock exchanges
S+: A stock exchange provides liquidity to existing securities.
S+: The Sensex is an index of the Bombay Stock Exchange.
S+: NSDL and CDSL are depositories in India.
S+: A demat account is opened with a depository participant.
S-: A stock exchange sells new shares directly for companies.
S-: The Nifty 50 is the index of the Bombay Stock Exchange.
S-: SEBI fixes the price of every share traded.
S-: Dematerialisation means printing share certificates.
K: C4 D4 4 | {p} wanted to buy shares of {f}. {He} chose a SEBI-registered broker, opened an account with a depository participant, and instructed the broker to buy 100 shares. | Identify the steps of the trading procedure followed. => Selection of a broker; opening a demat account; placing the order. || State the remaining two steps. => Executing the order (contract note issued); settlement (shares credited to the demat account and payment made).
K: C4 D5 6 | Explaining stock markets to {his} students in {c}, {p} said: investors can sell shares any time; prices reflect demand and supply; trading is safe under SEBI rules; savings reach growing companies; exchanges spread share ownership. | Identify five functions of a stock exchange mentioned. => Providing liquidity and marketability; pricing of securities; safety of transactions; contributes to economic growth; spreading of equity cult. || State one more function. => Providing scope for (healthy) speculation.
''', cat='term')

CH10_ST4 = spec('''
T: SEBI | The regulator of the securities market in India, set up in 1988 and given statutory powers on 30 January 1992.
T: Insider trading | Dealing in securities on the basis of unpublished price-sensitive information.
T: Price rigging | Manipulating the price of securities to inflate or depress the market price.
T: Merchant banker | An intermediary who manages public issues and must register with SEBI.
L: obj | objectives of SEBI | -
- To regulate stock exchanges and the securities industry to promote their orderly functioning | Markets work in an orderly manner.
- To protect the rights and interests of investors | Investors get information and protection, especially small investors.
- To prevent trading malpractices | It achieves a balance between self-regulation of business and statutory regulation.
- To regulate and develop a code of conduct and fair practices by intermediaries | Brokers, merchant bankers and others become competitive and professional.
L: prot | protective functions of SEBI | reg
- Prohibiting fraudulent and unfair trade practices | Misleading statements and manipulation are banned.
- Controlling insider trading | Penalties are imposed on insiders who use unpublished information.
- Checking price rigging | Manipulation of share prices is prevented.
- Undertaking steps for investor education | Investors are told how to evaluate securities.
- Promoting fair practices and a code of conduct | Rules are framed for the securities market.
L: dev | developmental functions of SEBI | reg
- Training of intermediaries | Intermediaries of the securities market are trained.
- Conducting research and publishing information | Useful information is published for market participants.
- Promoting a flexible and adaptable approach | For example, permitting internet trading through registered brokers.
- Making underwriting optional | It reduces the cost of issue.
L: reg | regulatory functions of SEBI | prot
- Registering brokers, sub-brokers and other intermediaries | They must be registered to operate.
- Registering collective investment schemes, including mutual funds | Mutual funds are regulated.
- Regulating takeover of companies | Takeovers follow SEBI regulations.
- Conducting inquiries and audit of stock exchanges | Exchanges are inspected.
- Levying fees or other charges | Fees are levied to carry out the purposes of the Act.
Q: Which function of SEBI is performed? | Protective function; Developmental function; Regulatory function; Advisory function | -
- SEBI penalised a director who sold shares of {f} using unpublished information about losses. | Protective function | Controlling insider trading protects investors.
- SEBI organised a training programme for stock brokers in {c}. | Developmental function | Training of intermediaries develops the market.
- SEBI registered a new mutual fund before it could collect money from the public. | Regulatory function | Registration of collective investment schemes is regulatory.
- SEBI permitted internet trading through registered stock brokers. | Developmental function | A flexible and adaptable approach develops the market.
- SEBI conducted an audit of a stock exchange. | Regulatory function | Inquiries and audit of exchanges are regulatory.
- SEBI ran a campaign to teach investors how to check the documents of a public issue. | Protective function | Investor education protects investors.
- SEBI framed regulations to govern the takeover of {f} by {f2}. | Regulatory function | Regulating takeovers is regulatory.
- SEBI acted against a group of brokers who manipulated the price of shares of {f}. | Protective function | Checking price rigging protects investors.
- SEBI made underwriting of public issues optional. | Developmental function | It reduces the cost of issue.
A: SEBI was given statutory powers in 1992. | The SEBI Act, 1992 gave it legal authority to regulate the securities market. | a | Both true; R explains A.
A: Controlling insider trading is a protective function of SEBI. | Insider trading harms ordinary investors who do not have the same information. | a | Both true; R explains A.
A: Registration of brokers is a developmental function of SEBI. | SEBI registers brokers and sub-brokers. | d | A is false: registration is a regulatory function. R is true.
A: SEBI protects the interests of investors. | SEBI is the regulator of the securities market in India. | b | Both true, but being the regulator does not by itself explain investor protection.
A: Permitting internet trading is a developmental function of SEBI. | It shows a flexible and adaptable approach. | a | Both true; R explains A.
TT: SEBI
S+: SEBI was set up in 1988 and given statutory powers in 1992.
S+: Controlling insider trading is a protective function of SEBI.
S+: Training of intermediaries is a developmental function of SEBI.
S+: Registering mutual funds is a regulatory function of SEBI.
S-: SEBI was set up in 1956.
S-: SEBI fixes the prices of shares on stock exchanges.
S-: Registration of brokers is a protective function of SEBI.
S-: SEBI is a private association of stock brokers.
K: C4 D4 4 | SEBI fined a company director for dealing in shares on the basis of unpublished price-sensitive information, and separately organised a workshop to train stock brokers. | Identify the malpractice and the function of SEBI in each action. => Insider trading: protective function; training brokers: developmental function. || State two objectives of SEBI. => Protect the rights and interests of investors; prevent trading malpractices; regulate stock exchanges; develop a code of conduct for intermediaries (any two).
K: C4 D5 6 | Recently SEBI (a) registered three new mutual funds, (b) penalised brokers for price rigging, (c) permitted internet trading, (d) audited a stock exchange, (e) ran investor education camps, and (f) published research on the bond market. | Classify each action as a protective, developmental or regulatory function. => (a) Regulatory; (b) protective; (c) developmental; (d) regulatory; (e) protective; (f) developmental.
''', cat='term')

# ================================================================ ch11 Marketing

CH11_ST1 = spec('''
T: Market | The set of actual and potential buyers of a product or service.
T: Marketing | A social process by which people obtain what they need and want through creating, offering and freely exchanging products and services of value.
T: Marketer | A person who takes more initiative in the exchange process and seeks a response from the other party.
T: Exchange | Obtaining a desired product from someone by offering something in return.
T: Customer value | The benefit a customer gets from a product compared with its cost.
T: Market offering | A complete offer of a product or service with details of size, quality, taste, price and place.
L: feat | features of marketing | -
- Needs and wants | Marketing helps individuals and groups obtain what they need and want.
- Creating a market offering | A complete offer is made with details of size, quality, price and availability.
- Customer value | The product must give greater value to the customer than its cost.
- Exchange mechanism | Marketing works through the exchange of products for money or something of value.
L: fn | functions of marketing | -
- Gathering and analysing market information | It helps identify needs and opportunities.
- Marketing planning | It sets marketing objectives and the action needed to achieve them.
- Product designing and development | The design makes the product attractive and useful.
- Standardisation and grading | Standards ensure uniform quality; grading sorts products into classes.
- Packaging and labelling | They protect, identify and promote the product.
- Branding | It gives the product a distinct identity.
- Customer support services | After-sales service and complaint handling build loyalty.
- Pricing of products | The price must suit the target market and the firm's objectives.
- Promotion | Customers are informed and persuaded to buy.
- Physical distribution | Goods reach customers through channels and logistics.
- Transportation | Goods are moved from the place of production to the place of sale.
- Storage or warehousing | Goods are stored until they are needed.
L: phil | marketing management philosophies | -
- Production concept | Customers favour products that are available and affordable, so focus on mass production.
- Product concept | Customers favour products of the best quality and features, so focus on product improvement.
- Selling concept | Customers will not buy enough unless persuaded, so focus on aggressive selling and promotion.
- Marketing concept | Identify customer needs and satisfy them better than competitors.
- Societal marketing concept | Satisfy customer needs while also caring for the long-term welfare of society.
Q: Which marketing management philosophy is followed? | Production concept; Product concept; Selling concept; Marketing concept; Societal marketing concept | -
- {f} believes customers will buy {g} if it is cheap and easily available, so it focuses on mass production. | Production concept | Availability and affordability are stressed.
- {f} keeps improving the quality and features of its {g}, believing a better product sells itself. | Product concept | Quality and features are stressed.
- {f} uses aggressive advertising and door-to-door salespeople to push its {g}. | Selling concept | Customers must be persuaded to buy.
- {f} surveys customers in {c} first and then designs {g} to meet their needs. | Marketing concept | Customer needs come first.
- {f} meets customer needs for {g} and also uses biodegradable packing to protect the environment. | Societal marketing concept | It cares for society's long-term welfare.
- {f} focuses on reducing production cost so that {g} can be sold at a low price everywhere. | Production concept | Availability and affordability are stressed.
- {f} studied what college students want in {g} and developed a product exactly for them. | Marketing concept | It identifies and satisfies customer needs.
Q: Which function of marketing is performed? | Gathering and analysing market information; Standardisation and grading; Branding; Customer support services; Pricing of products; Transportation; Storage or warehousing; Marketing planning | -
- {f} studied the buying habits of customers in {c} before launching its {g}. | Gathering and analysing market information | It helps find needs and opportunities.
- {f} sorts apples into A, B and C classes by size and quality. | Standardisation and grading | Grading sorts products into classes.
- {f} gives its {g} a distinctive name and logo. | Branding | It gives the product an identity.
- {f} runs a helpline to solve customer complaints about its {g}. | Customer support services | After-sales service builds loyalty.
- {f} keeps its stock of rice in a cold, dry godown until it is sold. | Storage or warehousing | Goods are stored until needed.
- {f} set a target of a 10% market share and listed the steps to achieve it. | Marketing planning | It sets objectives and actions.
- {f} moves its {g} by trucks from its factory in {c} to dealers across the state. | Transportation | Goods are moved to the place of sale.
- {f} studied its costs and competitors' prices before fixing the price of its {g}. | Pricing of products | The price must suit the market.
P: marketing | selling
- scope | a wider term covering many activities | a part of the marketing process
- focus | satisfying customer needs | transfer of title of goods
- profit | through customer satisfaction | through maximum sales
- beginning | begins before production | begins after production
- emphasis | customer needs | the product
- strategy | integrated marketing mix | pushing and promoting the product
A: The marketing concept focuses on the needs of customers. | It holds that the firm should identify and satisfy customer needs better than competitors. | a | Both true; R explains A.
A: Selling begins before production. | Selling aims at the transfer of title of goods. | d | A is false: selling begins after production. R is true.
A: The societal marketing concept goes beyond the marketing concept. | It also considers the long-term welfare of society. | a | Both true; R explains A.
A: Under the production concept, the focus is on aggressive selling. | Under the production concept, customers prefer products that are available and affordable. | d | A is false: the focus is on mass production. R is true.
A: Marketing is a wider term than selling. | Marketing includes many activities besides the transfer of goods. | a | Both true; R explains A.
TT: marketing
S+: Marketing begins before production.
S+: The societal marketing concept cares for the welfare of society.
S+: Grading means sorting products into classes by quality.
S+: Ideas, places and services can also be marketed.
S-: Marketing and selling mean the same thing.
S-: The product concept stresses aggressive selling.
S-: Marketing ends with the sale of goods.
S-: Customer value is the price charged for a product.
K: C4 D4 4 | {f} found that customers in {c} wanted low-sugar biscuits. It designed such a product, graded it by quality, and set up a helpline for complaints. | Which marketing philosophy is followed? Why? => Marketing concept: the firm first identifies customer needs and then satisfies them. || Identify two functions of marketing in the case. => Product designing and development; standardisation and grading; customer support services (any two).
K: C4 D5 6 | {p} started {f} to make {g}. At first {he} focused only on low cost and mass production; later on product quality; then on aggressive advertising. Now {he} studies customer needs and also uses eco-friendly packing. | Identify the five philosophies in the order followed. => Production concept; product concept; selling concept; marketing concept; societal marketing concept. || Which one is the best for the long run and why? => Societal marketing concept: it satisfies customers while protecting society's long-term welfare.
''', cat='marketing term')

CH11_ST2 = spec('''
T: Marketing mix | The set of marketing tools that a firm uses to pursue its marketing objectives in the target market: product, price, place and promotion.
T: Product | Anything of value that a firm offers to customers to satisfy their needs.
T: Brand | A name, term, sign, symbol, design or their combination used to identify the products of a seller.
T: Brand name | The part of a brand that can be spoken.
T: Brand mark | The part of a brand that can be recognised but not spoken, such as a symbol or design.
T: Trademark | A brand or part of a brand that is given legal protection.
T: Packaging | The act of designing and producing the container or wrapper for a product.
T: Labelling | Putting identification marks and information on the package of a product.
L: brand | characteristics of a good brand name | -
- Short, easy to pronounce, spell, recognise and remember | Customers can recall it easily.
- Suggests the product's benefits and qualities | It conveys what the product does.
- Distinctive | It stands apart from competitors' names.
- Adaptable to packing and labelling | It fits easily on any package or label.
- Versatile to accommodate new products | It can be used for new items in the product line.
- Capable of being registered and protected legally | It can become a trademark.
- Has staying power | It does not go out of date.
L: lab | functions of labelling | -
- Describes the product and specifies its contents | It tells the customer what is inside and how to use it.
- Identification of the product or brand | It helps the customer pick the right brand.
- Grading of products | Different grades are shown by different labels.
- Helps in promotion of products | Attractive labels persuade customers to buy.
- Providing information required by law | For example, statutory warnings and ingredients.
L: pack | functions and importance of packaging | -
- Product identification | Packaging helps identify the product.
- Product protection | It protects the product from spoilage, breakage and leakage.
- Facilitating use of the product | It makes the product easy to carry and use.
- Product promotion | Attractive packaging acts as a silent salesman.
- Rising standards of health and sanitation | Packed goods are less likely to be adulterated.
- Self-service outlets | In self-service stores the package must attract and inform buyers.
Q: Which level of packaging is described? | Primary package; Secondary packaging; Transportation packaging; Labelling | -
- The tube in which toothpaste is filled. | Primary package | It is the immediate container.
- The cardboard box in which the toothpaste tube is kept. | Secondary packaging | It is an additional layer of protection.
- Corrugated boxes in which 100 tubes of toothpaste are sent to the dealer. | Transportation packaging | It is used for storage and transport.
- The bottle that holds a cough syrup. | Primary package | It is the immediate container.
- The carton that holds a bottle of perfume. | Secondary packaging | It is an additional layer around the primary package.
- Large wooden crates used to send {g} from the factory to the warehouse. | Transportation packaging | It is used for storage and transport.
Q: Which element of the marketing mix is involved? | Product; Price; Place; Promotion | -
- {f} decides the features, design and packaging of its new {g}. | Product | It concerns what is offered to customers.
- {f} decides to sell its {g} at ₹10 less than its competitors. | Price | It concerns the amount charged.
- {f} decides to sell its {g} through retail stores and online platforms. | Place | It concerns the channels of distribution.
- {f} launches a television campaign for its {g}. | Promotion | It concerns communication with customers.
- {f} offers a discount of 10% for cash purchases of its {g}. | Price | Discounts are a part of pricing decisions.
- {f} plans warehouses and transport so that {g} reaches every town in {c}. | Place | Physical distribution is a part of place.
Q: Which type of product is it? | Convenience product; Shopping product; Specialty product; Industrial product | -
- Bread, soap and toothpaste that customers buy frequently with little effort. | Convenience product | Bought frequently with minimum effort.
- Furniture and clothes for which customers compare quality, price and style before buying. | Shopping product | Customers compare before buying.
- An expensive designer watch for which customers make a special effort. | Specialty product | It has unique features and customers make special efforts.
- Raw cotton bought by a textile mill. | Industrial product | It is used for producing other goods.
- Newspapers and toffees bought from the nearest shop. | Convenience product | Low-priced, bought frequently.
- A machine bought by a factory to make {g}. | Industrial product | It is used for producing other goods.
P: branding | labelling
- meaning | giving a name, sign or symbol to a product | putting identification marks and information on the package
- purpose | product differentiation and identity | describing the product and giving information
- legal requirement | a brand need not be registered | certain information on labels is required by law
A: Packaging is called a silent salesman. | Attractive packaging helps to promote the product. | a | Both true; R explains A.
A: A brand mark can be spoken. | A brand mark is a symbol or design. | d | A is false: a brand mark can be recognised but not spoken. R is true.
A: Branding helps in product differentiation. | A brand distinguishes a firm's product from those of competitors. | a | Both true; R explains A.
A: Labels may carry information required by law. | Statutory warnings are printed on packets of cigarettes. | a | Both true; R explains A.
A: A trademark is a brand that has been given legal protection. | A brand name is the part of a brand that can be spoken. | b | Both true, but R explains brand name, not trademark.
TT: product, branding, packaging and labelling
S+: A trademark is a legally protected brand.
S+: The tube of toothpaste is its primary package.
S+: Labels describe the product and specify its contents.
S+: Product, price, place and promotion are the four Ps of the marketing mix.
S-: A brand mark is the part of a brand that can be spoken.
S-: The cardboard box of toothpaste is its primary package.
S-: Packaging has no role in promotion.
S-: Every brand is automatically a trademark.
K: C4 D4 4 | {f} named its new soft drink 'Zing', short and easy to remember, put it in an attractive pack that keeps it fresh, and printed the date of manufacture and ingredients on the pack. | Identify two characteristics of a good brand name shown. => Short; easy to pronounce and remember (also distinctive). || Identify two functions of packaging and one function of labelling. => Packaging: product protection, product promotion; labelling: describes the product and specifies its contents / information required by law.
K: C4 D5 6 | {p} is launching a new {g} through {f}. {He} has to decide its features and brand, the price, where to sell it, and how to make it known. | Name the concept and its four elements. => Marketing mix: product, price, place (physical distribution) and promotion. || Explain any two elements with reference to the case. => Product: features, brand and packaging of the {g}; price: the amount charged considering cost, demand and competition; place: channels and logistics; promotion: advertising, sales promotion etc. (any two).
''', cat='term')

CH11_ST3 = spec('''
T: Price | The amount of money paid by buyers in consideration of the purchase of a product or service.
T: Pricing objective | The goal a firm wants to achieve through its pricing, such as profit maximisation or market share.
T: Price elasticity of demand | The responsiveness of the quantity demanded to a change in price.
T: Penetration pricing | Setting a low price to capture a large share of the market quickly.
L: fac | factors affecting price determination | -
- Product cost | The price must cover the cost of producing and selling the product.
- The utility and demand | The upper limit of price is set by the utility of the product and the demand for it.
- Extent of competition in the market | The price is affected by the prices of competitors.
- Government and legal regulations | The government may regulate prices of essential products.
- Pricing objectives | Profit maximisation, market share leadership, survival or product quality leadership.
- Marketing methods used | Distribution, advertising, packaging and services affect the price.
L: pobj | pricing objectives of a firm | -
- Profit maximisation | Earning the highest profit, in the short or long run.
- Obtaining market share leadership | A low price to capture a large share of the market.
- Surviving in a competitive market | Lowering prices to clear stock and survive.
- Attaining product quality leadership | A higher price to cover the cost of high quality and research.
Q: Which factor affecting price determination is highlighted? | Product cost; The utility and demand; Extent of competition in the market; Government and legal regulations; Pricing objectives; Marketing methods used | -
- {f} could not raise the price of its medicine because the government has fixed its maximum retail price. | Government and legal regulations | The government regulates prices of essential goods.
- {f} kept the price of its {g} close to that of its many rivals in {c}. | Extent of competition in the market | Competition limits the price.
- {f} raised the price of {g} because of a sharp rise in the cost of raw material. | Product cost | The price must cover cost.
- As demand for {g} is inelastic, {f} was able to charge a higher price. | The utility and demand | Inelastic demand allows a higher price.
- {f} charges more for {g} because it gives free home delivery and an extended warranty. | Marketing methods used | Services affect the price.
- {f} set a low price for its new {g} to capture a large share of the market. | Pricing objectives | Market share leadership is a pricing objective.
Q: Which pricing objective is being pursued? | Profit maximisation; Obtaining market share leadership; Surviving in a competitive market; Attaining product quality leadership | -
- {f} charges a high price to cover the cost of research behind its top-quality {g}. | Attaining product quality leadership | High quality needs a higher price.
- Facing a slump, {f} sold its {g} at very low prices to clear its stock. | Surviving in a competitive market | Low prices help the firm survive.
- {f} entered the market with low prices to become the largest seller of {g}. | Obtaining market share leadership | Low prices build market share.
- {f} sets its price to earn the highest possible profit in the long run. | Profit maximisation | Profit is the main objective.
A: Product cost sets the lower limit of price. | A firm cannot usually sell below cost for long. | a | Both true; R explains A.
A: When demand is inelastic, a firm can charge a higher price. | Inelastic demand means quantity demanded changes little with a change in price. | a | Both true; R explains A.
A: Firms are free to fix any price for every product. | The government may regulate the prices of essential products. | d | A is false; R is true.
A: Price is an important element of the marketing mix. | Price affects the demand for a product and the profit of the firm. | a | Both true; R explains A.
TT: price determination
S+: Product cost sets the lower limit of price.
S+: The government may regulate the prices of essential goods.
S+: Competition affects the price a firm can charge.
S+: A firm may charge a high price to maintain product quality leadership.
S-: Utility and demand set the lower limit of price.
S-: Competition has no effect on pricing.
S-: Price is not a part of the marketing mix.
S-: Firms seeking market share usually set very high prices.
K: C4 D4 4 | {f} wants to become the leading seller of {g} in {c}, but the cost of raw material has risen and many rivals sell similar products. | Identify three factors affecting the price of its {g}. => Pricing objectives (market share leadership); product cost; extent of competition. || What price policy would you suggest? => A low (penetration) price close to cost, as competition is high and the aim is market share.
K: C4 D5 6 | The price of {g} sold by {f} depends on its cost of production, the demand for it, prices of rivals, government rules, the firm's goal of quality leadership, and its free home delivery. | Explain any four factors affecting price determination shown. => Product cost (lower limit); utility and demand (upper limit); extent of competition; government regulation; pricing objectives (quality leadership); marketing methods (free delivery) (any four). || How does the objective of quality leadership affect price? => It calls for a higher price to cover the cost of high quality and research.
''', cat='term')

CH11_ST4 = spec('''
T: Physical distribution | The activities involved in making goods available to customers at the right place and time.
T: Channels of distribution | The routes through which goods and services move from producers to consumers.
T: Zero level channel | A channel in which the manufacturer sells directly to customers.
T: Order processing | Accurate and fast handling of customer orders.
T: Warehousing | Storing goods until they are needed by customers.
T: Inventory control | Deciding the level of stock to keep so that customer needs are met at minimum cost.
L: comp | components of physical distribution | -
- Order processing | Accurate and fast processing of orders satisfies customers.
- Transportation | Goods are moved from the place of production to the place of sale.
- Warehousing | Goods are stored until needed, creating time utility.
- Inventory control | The right level of stock is maintained at minimum cost.
L: ch | factors affecting the choice of channels of distribution | -
- Product-related factors | Perishable, technical and costly goods need short channels.
- Company characteristics | Firms with large funds and a desire for control can use shorter channels.
- Competitive factors | Firms may use the channels of competitors or avoid them.
- Market factors | Large, concentrated markets suit short channels; small, scattered ones suit long channels.
- Environmental factors | In a depression shorter and cheaper channels are used.
Q: Which channel of distribution is used? | Zero level; One level; Two level; Three level | -
- {f} sells its {g} directly to customers through its own website. | Zero level | Manufacturer to customer directly.
- {f} sells its cars through authorised dealers who sell to customers. | One level | Manufacturer, retailer, customer.
- {f} sells its {g} to wholesalers, who sell to retailers, who sell to customers. | Two level | Manufacturer, wholesaler, retailer, customer.
- {f} appoints agents, who sell to wholesalers, who sell to retailers, who sell to customers. | Three level | Manufacturer, agent, wholesaler, retailer, customer.
- {f} sells its {g} door to door through its own salespeople. | Zero level | Direct selling.
- {f} sells its {g} to large retail chains, which sell to customers. | One level | One middleman, the retailer.
- {f}, a soap maker, sells to wholesalers who supply grocery shops across {c}. | Two level | Two middlemen.
Q: Which component of physical distribution is highlighted? | Order processing; Transportation; Warehousing; Inventory control | comp
- {f} has introduced software that processes customer orders for {g} within one hour. | Order processing | Fast and accurate handling of orders.
- {f} uses trucks and rail to move {g} from its factory in {c} to markets. | Transportation | Movement of goods.
- {f} stores rice harvested in October and sells it through the year. | Warehousing | Storage creates time utility.
- {f} keeps enough stock of {g} to meet demand without blocking too much money. | Inventory control | The right level of stock at minimum cost.
- {f} has built cold storages to keep fruit fresh until sale. | Warehousing | Storage of perishables.
F: comp | Warehousing | stores goods until needed; creates time utility; protects goods from damage
F: comp | Inventory control | balances customer service and cost; avoids stock-outs; avoids blocking funds in excess stock
A: Perishable goods need a short channel of distribution. | They cannot be kept for long. | a | Both true; R explains A.
A: Warehousing creates time utility. | Goods are stored until they are needed. | a | Both true; R explains A.
A: A zero level channel has one middleman. | In a zero level channel goods move directly from the manufacturer to the customer. | d | A is false: it has no middleman. R is true.
A: Transportation is a component of physical distribution. | It moves goods from the place of production to the place of sale. | a | Both true; R explains A.
A: Technical products are usually sold through long channels. | They need demonstration and after-sales service. | d | A is false: they need short channels. R is true.
TT: physical distribution
S+: A zero level channel has no middlemen.
S+: Warehousing creates time utility.
S+: Perishable goods need short channels.
S+: Order processing, transportation, warehousing and inventory control are components of physical distribution.
S-: A two level channel has only a retailer.
S-: Technical goods are usually sold through long channels.
S-: Inventory control means keeping as much stock as possible.
S-: Transportation creates time utility.
K: C4 D4 4 | {f} makes fresh dairy products in {c} and sells them through its own outlets. It keeps them in cold storage and processes online orders within an hour. | Identify the channel of distribution and a factor explaining the choice. => Zero level (direct); the product is perishable, so a short channel is needed. || Identify two components of physical distribution in the case. => Warehousing (cold storage); order processing (online orders processed within an hour).
K: C4 D5 6 | {p} manages distribution at {f}, which sells {g} all over India. {He} must decide how orders are handled, how goods reach markets, where they are stored and how much stock to keep. | Name the four components of physical distribution. => Order processing; transportation; warehousing; inventory control. || Explain two factors affecting the choice of channel for {f}. => Market factors (large and scattered market suits longer channels); product-related factors (nature and value of the product); company characteristics; competitive factors; environmental factors (any two).
''', cat='term')

CH11_ST5 = spec('''
T: Promotion mix | The combination of promotional tools used by a firm: advertising, personal selling, sales promotion and public relations.
T: Advertising | An impersonal form of communication paid for by an identified sponsor to promote goods or services.
T: Personal selling | Oral presentation in a conversation with one or more prospective customers for the purpose of making sales.
T: Sales promotion | Short-term incentives to encourage the immediate purchase of a product.
T: Public relations | Managing communication with the public to build a favourable image of the organisation.
T: Publicity | Non-paid communication about a firm or its product in the media.
L: adm | merits of advertising | adl
- Mass reach | It reaches a large number of people over a wide area.
- Enhancing customer satisfaction and confidence | It creates confidence in the product.
- Expressiveness | Art, music and graphics make it attractive.
- Economy | The cost per person reached is low.
L: adl | limitations of advertising | adm
- Less forceful | It is impersonal, so customers feel less obliged to respond.
- Lack of feedback | Its effect on sales is hard to measure.
- Inflexibility | The message cannot be adjusted for each customer.
- Low effectiveness | Too many advertisements reduce the impact of each one.
L: obj | objections to advertising | -
- Adds to cost | The cost of advertising is passed on to customers.
- Undermines social values | It promotes materialism and creates unnecessary wants.
- Confuses buyers | Many similar claims confuse buyers.
- Encourages the sale of inferior products | Inferior goods may also be advertised.
- Some advertisements are in bad taste | Some advertisements offend people.
L: sp | techniques of sales promotion | -
- Rebate | Products are offered at a reduced price to clear stock.
- Discount | Products are sold at less than the list price.
- Refunds | A part of the price is refunded on showing proof of purchase.
- Product combinations | A gift of another product with the purchase.
- Quantity gift | Extra quantity of the product is given free.
- Instant draws and assigned gift | Scratch a card to win an instant prize.
- Lucky draw | Coupons with the purchase enter a draw for prizes.
- Usable benefit | A voucher for a free service or product on purchase.
- Full finance at 0% | Goods sold on easy instalments with no interest.
- Sampling | Free samples are given to try the product.
- Contests | Competitions with prizes for buyers.
L: pr | functions of public relations | -
- Press relations | Positive information about the firm is given to the media.
- Product publicity | Publicity is created for specific products.
- Corporate communication | Internal and external communication builds the firm's image.
- Lobbying | Dealing with legislators and government officials.
- Counselling | Advising management on public issues and the firm's image.
Q: Which technique of sales promotion is used? | Rebate; Discount; Refunds; Product combinations; Quantity gift; Lucky draw; Full finance at 0%; Sampling; Contests; Usable benefit | sp
- {f} gives a free bottle of shampoo with every pack of soap. | Product combinations | A gift of another product with the purchase.
- {f} offers 20% extra toothpaste in every tube at the same price. | Quantity gift | Extra quantity free.
- {f} distributes free sachets of its new shampoo door to door. | Sampling | Free samples to try the product.
- {f} sells smartphones on 12 easy instalments with no interest. | Full finance at 0% | No-interest instalments.
- {f} sells its {g} at 25% below the list price this week. | Discount | Price below list price.
- Each buyer of {g} from {f} gets a coupon for a monthly draw for a car. | Lucky draw | Coupons enter a draw.
- {f} returns ₹50 to buyers who send the empty wrapper of its chocolate bar. | Refunds | Part of the price refunded on proof of purchase.
- {f} reduced the price of old stock of {g} to clear it before the new model arrived. | Rebate | Reduced price to clear stock.
- Buyers of {g} from {f} can write a slogan and win a holiday. | Contests | Competition with prizes.
- On buying {g} worth ₹2,000, {f} gives a voucher for a free meal. | Usable benefit | A free service on purchase.
Q: Which element of the promotion mix is used? | Advertising; Personal selling; Sales promotion; Public relations | -
- {f} runs a television commercial for its {g} across India. | Advertising | Paid, impersonal communication.
- A salesperson of {f} visits doctors to explain the benefits of a new medicine. | Personal selling | Face-to-face oral presentation.
- {f} offers buy-one-get-one-free on its {g} this festive season. | Sales promotion | Short-term incentive.
- {f} releases a press note on its new solar plant and sponsors a city marathon in {c}. | Public relations | Building a favourable image.
- {f} puts hoardings for its {g} on highways. | Advertising | Paid, impersonal, identified sponsor.
- A salesperson of {f} demonstrates a vacuum cleaner at a customer's home. | Personal selling | Direct demonstration and persuasion.
P: advertising | personal selling
- form | impersonal | personal, face to face
- flexibility | inflexible message | flexible message suited to each customer
- reach | reaches a large number of people | reaches a limited number of people
- cost per person | low | high
- feedback | slow and difficult | immediate
- time | reaches people quickly | takes more time
F: sp | Product combinations | adds value to the purchase; introduces the free product; encourages immediate purchase
F: sp | Sampling | lets customers try the product; useful for new products; builds awareness
A: Advertising is an impersonal form of communication. | There is no face-to-face contact between the advertiser and the customer. | a | Both true; R explains A.
A: Personal selling is flexible. | The salesperson can adjust the presentation to the needs of each customer. | a | Both true; R explains A.
A: Sales promotion is used to build long-term loyalty. | Sales promotion consists of short-term incentives. | d | A is false: it aims at immediate sales. R is true.
A: Advertising is criticised for adding to the cost of products. | The cost of advertising is passed on to customers. | a | Both true; R explains A.
A: Publicity is a paid form of communication. | Publicity appears in the media as news. | d | A is false: publicity is not paid for. R is true.
TT: promotion
S+: Advertising is a paid form of communication.
S+: Personal selling gives immediate feedback.
S+: Sampling is a sales promotion technique.
S+: Public relations builds a favourable image of the firm.
S-: Advertising has an unidentified sponsor.
S-: Personal selling reaches millions of people at a low cost per person.
S-: Sales promotion gives long-term incentives.
S-: Publicity is paid for by the firm.
K: C4 D4 4 | {f} launched a new {g}. It gave free samples, put up advertisements on television, and sent salespeople to shops to explain its features. | Identify the elements of the promotion mix used. => Sales promotion (free samples); advertising (television); personal selling (salespeople). || State one merit and one limitation of advertising. => Merit: mass reach / economy / expressiveness; limitation: less forceful / lack of feedback / inflexibility / low effectiveness.
K: C4 D5 6 | People complain that advertisements for {g} by {f} raise prices, create unnecessary wants, confuse buyers with similar claims, and sometimes promote poor products. | Identify the objections to advertising raised. => Adds to cost; undermines social values; confuses buyers; encourages sale of inferior products. || Give one argument against each objection. => Advertising raises demand and lowers cost per unit through large-scale production; it informs people of better products and raises the standard of living; buyers can compare and choose; a poor product cannot be sold again to the same buyer through advertising.
''', cat='promotion term')

# ================================================================ ch12 Consumer protection

CH12_ST1 = spec('''
T: Consumer protection | Measures to protect consumers from unfair trade practices and to educate them about their rights and responsibilities.
T: Unfair trade practice | A deceptive method used to promote the sale of goods or services, such as a false claim about quality.
T: Adulteration | Mixing inferior or harmful substances with a product.
T: Consumer sovereignty | The idea that consumers decide what is produced through their choices.
L: cimp | reasons why consumer protection is important from the consumers' point of view | bimp
- Consumer ignorance | Most consumers are not aware of their rights and remedies.
- Unorganised consumers | Consumers are not organised and cannot fight exploitation alone.
- Widespread exploitation of consumers | Adulteration, false claims and poor service are common.
L: bimp | reasons why consumer protection is important from the point of view of business | cimp
- Long-term interest of business | Satisfied customers bring repeat sales and goodwill.
- Business uses society's resources | It must supply goods in the interest of society.
- Social responsibility | Business has a responsibility towards consumers as stakeholders.
- Moral justification | It is the moral duty of business to avoid exploitation.
- Government intervention | Exploiting consumers invites government action and damages the firm's image.
L: ways | ways and means of consumer protection | -
- Self-regulation by business | Firms set up customer service cells and follow ethical standards.
- Business associations | Bodies such as FICCI and CII lay down codes of conduct for members.
- Consumer awareness | An aware consumer can protect his or her own interests.
- Consumer organisations | They educate consumers and fight for their rights.
- Government | It passes laws such as the Consumer Protection Act, 2019.
Q: Which point of importance of consumer protection is shown? | Consumer ignorance; Unorganised consumers; Widespread exploitation of consumers; Long-term interest of business; Social responsibility; Government intervention | -
- {p} did not know {he} could complain about the defective {g} sold by {f}. | Consumer ignorance | Consumers are unaware of their rights.
- {f} treats customers fairly because satisfied customers come back and bring others. | Long-term interest of business | Satisfied customers mean repeat sales.
- Buyers of {g} in {c} were cheated, but each buyer alone could not fight the large seller. | Unorganised consumers | Individual consumers are weak.
- Many sellers in {c} sell adulterated spices and charge more than the printed price. | Widespread exploitation of consumers | Exploitation is common.
- {f} recognises its duty towards consumers as one of its stakeholders. | Social responsibility | Business is responsible to consumers.
- {f} changed its unfair practices after the government threatened legal action. | Government intervention | Exploitation invites government action.
A: Consumer protection is in the long-term interest of business. | Satisfied customers bring repeat sales and goodwill. | a | Both true; R explains A.
A: Consumers in India need protection. | Most consumers are unaware of their rights and are unorganised. | a | Both true; R explains A.
A: Business has no responsibility towards consumers. | Business uses the resources of society. | d | A is false: business is responsible to consumers. R is true.
A: Self-regulation by business helps consumer protection. | Firms set up customer service and grievance cells. | a | Both true; R explains A.
TT: consumer protection
S+: Consumer protection is in the long-term interest of business.
S+: Lack of awareness makes consumers vulnerable to exploitation.
S+: Business associations can lay down codes of conduct for their members.
S+: Business uses resources that belong to society.
S-: Consumer protection is against the interest of business.
S-: Consumers in India are well organised against exploitation.
S-: Only the government can protect consumers.
S-: Social responsibility does not cover consumers.
K: C4 D4 4 | {p} bought a pack of rice from {f} that was below the stated weight. {He} did not know where to complain, and other buyers in {c} faced the same problem but did nothing. | Identify two reasons why consumer protection is important from the consumers' point of view. => Consumer ignorance; unorganised consumers (also widespread exploitation). || Why should {f} protect consumers? Give two reasons. => Long-term interest of business; social responsibility; moral justification; to avoid government intervention (any two).
K: C4 D5 6 | Explain how consumers can be protected through business, business associations, consumers themselves, consumer organisations and the government. | Explain any four ways of consumer protection. => Self-regulation by business (service cells); business associations (codes of conduct, e.g. FICCI, CII); consumer awareness; consumer organisations (education, legal help); government (laws such as the Consumer Protection Act, 2019).
''', cat='term')

CH12_ST2 = spec('''
T: Consumer | A person who buys goods or hires services for a consideration, but not for resale or a commercial purpose.
T: Right to safety | The right to be protected against goods and services that are hazardous to life and property.
T: Right to be informed | The right to complete information about the product, such as ingredients, price, date of manufacture and quality.
T: Right to choose | The right to choose from a variety of products at competitive prices.
T: Right to be heard | The right to file a complaint and to have the grievance considered at appropriate forums.
T: Right to seek redressal | The right to get relief, such as replacement, refund or compensation, against unfair trade practices.
T: Right to consumer education | The right to acquire knowledge and skills to be an informed consumer.
L: rts | rights of a consumer under the Consumer Protection Act, 2019 | resp
- Right to safety | Protection against hazardous goods, such as poor-quality electrical appliances.
- Right to be informed | Complete information on the label about contents, price and expiry.
- Right to choose | Freedom to choose from a variety of products at competitive prices.
- Right to be heard | The right to file a complaint and have it considered.
- Right to seek redressal | Relief through replacement, refund, removal of defect or compensation.
- Right to consumer education | Knowledge to make informed choices.
L: resp | responsibilities of a consumer | rts
- Be aware of the various goods and services available | It helps in making a wise choice.
- Buy only standardised goods | Look for the ISI mark on electrical goods, FPO on food products and Hallmark on jewellery.
- Learn about the risks associated with products | Follow the manufacturer's instructions for safe use.
- Read labels carefully | Check price, ingredients, date of manufacture and expiry.
- Be assertive to get a fair deal | Insist on a fair price and quality.
- Be honest in dealings | Choose only legal goods and services.
- Ask for a cash memo | It is proof of purchase needed for a complaint.
- File a complaint in case of a shortcoming | Approach the appropriate forum.
- Form consumer societies | Help educate other consumers.
- Respect the environment | Avoid waste, littering and pollution.
Q: Which consumer right is involved? | Right to safety; Right to be informed; Right to choose; Right to be heard; Right to seek redressal; Right to consumer education | rts
- {p} got a new washing machine in place of the defective one sold by {f}, after the Commission's order. | Right to seek redressal | {He} got relief (replacement).
- An electric iron bought by {p} gave {him} a shock because it did not meet safety standards. | Right to safety | Protection against hazardous goods.
- The label on the pack of ready-to-eat noodles did not mention the expiry date. | Right to be informed | Complete product information must be given.
- A shopkeeper in {c} forced {p} to buy only one brand of cooking oil. | Right to choose | Freedom to choose among products.
- {f} set up a grievance cell so that complaints of customers can be considered. | Right to be heard | Grievances must be heard.
- The government ran the 'Jago Grahak Jago' campaign to make people aware. | Right to consumer education | Consumers must be educated.
- The packet of medicine bought by {p} did not show its date of manufacture and price. | Right to be informed | Details must be on the label.
Q: Which standard mark should the consumer look for? | ISI mark; FPO mark; Hallmark; Agmark | -
- {p} is buying an electric heater. | ISI mark | ISI is the standard mark for electrical and industrial goods.
- {p} is buying a gold necklace. | Hallmark | Hallmark certifies the purity of gold jewellery.
- {p} is buying a bottle of jam. | FPO mark | FPO is the mark for processed fruit products.
- {p} is buying a pack of honey. | Agmark | Agmark is the mark for agricultural products.
- {p} is buying an electric geyser. | ISI mark | It is an electrical appliance.
- {p} is buying pickles in a jar. | FPO mark | It is a processed fruit and vegetable product.
- {p} is buying pulses and spices graded for quality. | Agmark | Agmark is for agricultural products.
F: rts | Right to safety | protection against hazardous goods; standard marks such as ISI help ensure safety; covers life and property
F: rts | Right to be informed | label shows contents and price; date of manufacture and expiry; information helps in comparing products
F: rts | Right to seek redressal | replacement of defective goods; refund of price; compensation for loss or injury
A: A consumer has the right to be informed. | The label must give details such as price, ingredients and expiry date. | a | Both true; R explains A.
A: A person who buys goods for resale is a consumer under the Act. | A consumer buys goods or hires services for a consideration. | d | A is false: a buyer for resale is not a consumer. R is true.
A: Consumers should insist on a cash memo. | A cash memo is proof of purchase needed for a complaint. | a | Both true; R explains A.
A: Consumers should buy ISI-marked electrical goods. | The ISI mark ensures the product meets prescribed standards. | a | Both true; R explains A.
A: The right to choose means the consumer must buy only one brand. | The right to choose means freedom to choose from a variety of products. | d | A is false; R is true.
TT: consumer rights and responsibilities
S+: The right to safety protects consumers against hazardous goods.
S+: Hallmark is the quality mark for gold jewellery.
S+: A consumer should ask for a cash memo.
S+: The right to seek redressal allows consumers to get relief.
S-: A person who buys goods for resale is a consumer under the Act.
S-: Agmark is the standard mark for electrical goods.
S-: Consumers have no responsibility under consumer protection.
S-: The right to be informed allows the seller to hide the expiry date.
K: C4 D4 4 | {p} bought a pressure cooker without the ISI mark and without taking a bill. It burst and injured {him}. | Which right of the consumer was violated? => Right to safety. || State two responsibilities {p} failed to perform. => Buy only standardised goods (ISI mark); ask for a cash memo.
K: C4 D5 6 | {p} bought a packet of biscuits from a shop in {c}. The packet had no expiry date, the shopkeeper refused to let {him} choose another brand, and when the product turned out defective, the shopkeeper refused to listen. | Identify three rights of the consumer violated. => Right to be informed; right to choose; right to be heard. || Which right will help {p} get relief, and what reliefs can {he} get? => Right to seek redressal: replacement, refund of price or compensation.
''', cat='term')

CH12_ST3 = spec('''
T: District Commission | The consumer disputes redressal body at the district level, consisting of a President and not less than two members.
T: State Commission | The consumer disputes redressal body at the state level, consisting of a President and not less than four members.
T: National Commission | The consumer disputes redressal body at the national level, consisting of a President and not less than four members.
T: Complainant | A person or body that files a complaint before a consumer commission.
T: Deficiency in service | Any fault, imperfection or shortcoming in the quality or manner of a service.
L: who | persons who can file a complaint | -
- Any consumer | A person who bought the goods or hired the services.
- Any registered consumers' association | A voluntary consumer association registered under law.
- The Central Government or any State Government | In the interest of consumers.
- One or more consumers on behalf of numerous consumers with the same interest | A class action for many consumers.
- A legal heir or representative of a deceased consumer | On behalf of the consumer who has died.
- In the case of a minor, the parent or legal guardian | On behalf of the minor.
L: mach | features of the three-tier redressal machinery | -
- District Commission | Complaints where the value of goods or services paid as consideration is up to ₹1 crore (Act as enacted).
- State Commission | Value above ₹1 crore and up to ₹10 crore; also hears appeals against District Commission orders.
- National Commission | Value above ₹10 crore; also hears appeals against State Commission orders.
- Appeal from the District Commission | To the State Commission within 45 days of the order.
- Appeal from the State Commission | To the National Commission within 30 days of the order.
- Appeal from the National Commission | To the Supreme Court within 30 days of the order.
Q: Who can file a complaint in this situation? | Any consumer; Any registered consumers' association; The Central or a State Government; The legal heir of a deceased consumer; The parent or legal guardian of a minor | -
- {p}, aged 12, was injured by a defective toy. | The parent or legal guardian of a minor | A minor's complaint is filed by the parent or guardian.
- {p} died because of a spurious medicine; {his} family wants to file a complaint. | The legal heir of a deceased consumer | The legal heir can file on behalf of the deceased.
- {p} bought a defective {g} from {f} in {c}. | Any consumer | The buyer can file a complaint.
- A registered voluntary consumer group in {c} wants to file a complaint against adulteration. | Any registered consumers' association | Registered associations can file complaints.
- A state government wants to act against a firm selling unsafe {g} to many consumers. | The Central or a State Government | Governments can file complaints in the interest of consumers.
Q: Which body should hear the matter? | District Commission; State Commission; National Commission; Supreme Court | -
- {p} wants to appeal against an order of the District Commission. | State Commission | Appeals against District Commission orders go to the State Commission.
- A firm wants to appeal against an order of the National Commission. | Supreme Court | Appeals against National Commission orders go to the Supreme Court.
- {p} wants to appeal against an order of the State Commission. | National Commission | Appeals against State Commission orders go to the National Commission.
- {p} paid ₹40,000 for a defective {g} (Act as enacted). | District Commission | The value is within the District Commission's limit.
- A company paid ₹5 crore for defective machinery from {f} (Act as enacted). | State Commission | The value is above ₹1 crore and up to ₹10 crore.
- A firm paid ₹15 crore for a defective aircraft simulator (Act as enacted). | National Commission | The value is above ₹10 crore.
A: A legal heir can file a complaint on behalf of a deceased consumer. | The Act allows the legal heir or representative to file a complaint. | a | Both true; R explains A.
A: An appeal against an order of the District Commission can be filed with the National Commission. | The State Commission hears appeals against District Commission orders. | d | A is false: the appeal goes to the State Commission. R is true.
A: A registered consumers' association can file a complaint. | Consumers' associations work for the protection of consumers. | a | Both true; R explains A.
A: A complaint can be filed against a service provider. | A complaint can be filed in case of deficiency in service. | a | Both true; R explains A.
A: An appeal against an order of the National Commission lies with the Supreme Court. | The National Commission is the highest consumer commission. | a | Both true; R explains A.
TT: the redressal machinery under the Consumer Protection Act, 2019
S+: The redressal machinery has three tiers: District, State and National Commissions.
S+: An appeal against an order of the State Commission lies with the National Commission.
S+: A complaint can be filed against a seller, manufacturer or service provider.
S+: A parent can file a complaint on behalf of a minor.
S-: An appeal against an order of the District Commission lies with the Supreme Court.
S-: Only the consumer himself can file a complaint.
S-: The National Commission hears complaints of any value, however small.
S-: A complaint cannot be filed against a service provider.
K: C4 D4 4 | {p} bought a laptop for ₹70,000 from {f}; it stopped working in a week and {f} refused to repair it. {p} took the matter to the District Commission, but was not satisfied with its order. | Was {p} right to approach the District Commission? => Yes: the value of the goods was within the District Commission's limit. || Where can {he} appeal, and within what time? => To the State Commission, within 45 days of the order.
K: C4 D5 6 | A child was injured by a defective toy bought from {f}; a registered consumer group and the state government also want to act, as many children have been hurt. | Who can file complaints in the case? => The parent or legal guardian of the minor; the registered consumers' association; the State Government; one or more consumers on behalf of numerous consumers. || Describe the three-tier redressal machinery. => District Commission (value up to ₹1 crore as enacted), State Commission (₹1–10 crore, and appeals from District), National Commission (above ₹10 crore, and appeals from State); appeal from the National Commission to the Supreme Court.
''', cat='term')

CH12_ST4 = spec('''
T: Punitive damages | Compensation awarded to punish the wrongdoer, in addition to compensation for loss.
T: Corrective advertisement | An advertisement ordered by a Commission to remove the effect of a misleading advertisement.
T: Consumer organisation | A voluntary non-governmental body that works to protect and promote the interests of consumers.
T: Comparative testing | Testing consumer products in accredited laboratories to compare their quality.
T: Consumer Welfare Fund | A fund to which a trader may be ordered to pay a sum, used for the welfare of consumers.
L: rem | remedies available to the consumer | -
- To remove the defect in the product | The seller repairs the product.
- To replace the defective product | A new non-defective product is given.
- To refund the price paid | The money is returned to the consumer.
- To pay compensation for loss or injury | The consumer is compensated for loss suffered.
- To pay punitive damages in appropriate circumstances | Extra damages to punish the wrongdoer.
- To remove the deficiency in service | The service is corrected.
- To discontinue an unfair or restrictive trade practice | The practice is stopped.
- To stop the sale of hazardous goods | Hazardous goods are not offered for sale.
- To withdraw hazardous goods from sale | Goods already in the market are withdrawn.
- To issue a corrective advertisement | It neutralises the effect of a misleading advertisement.
L: ngo | functions of consumer organisations and NGOs | -
- Educating the public about consumer rights | By organising training programmes, seminars and workshops.
- Publishing periodicals and other publications | To spread knowledge about consumer problems and remedies.
- Comparative testing of consumer products | In accredited laboratories, with the results published.
- Encouraging consumers to protest against exploitation | They help consumers take action against unfair practices.
- Providing legal assistance to consumers | They help consumers obtain redressal.
- Filing complaints in consumer commissions on behalf of consumers | They act for consumers who cannot do so themselves.
- Filing cases in the interest of the general public | Not just for individual consumers.
Q: Which remedy has the Commission ordered? | To remove the defect in the product; To replace the defective product; To refund the price paid; To pay compensation for loss or injury; To pay punitive damages in appropriate circumstances; To issue a corrective advertisement; To withdraw hazardous goods from sale; To discontinue an unfair or restrictive trade practice | rem
- {f} was told to give {p} a new {g} in place of the faulty one. | To replace the defective product | A new product replaces the defective one.
- {f} was told to return the ₹12,000 paid by {p}. | To refund the price paid | The price is returned.
- {f} was told to repair the fault in the washing machine sold to {p}. | To remove the defect in the product | The defect is removed.
- {f} was told to pay {p} ₹50,000 for the injury caused by its defective {g}. | To pay compensation for loss or injury | Compensation for loss suffered.
- {f}, which falsely claimed its drink increases height, was told to publish a new advertisement correcting the claim. | To issue a corrective advertisement | It neutralises the misleading claim.
- {f} was told to recall from shops all packs of a toy found to contain toxic paint. | To withdraw hazardous goods from sale | Hazardous goods are withdrawn.
- {f} was ordered to stop forcing buyers of {g} to buy another product along with it. | To discontinue an unfair or restrictive trade practice | The practice must stop.
- Because {f} knowingly sold spurious medicines, the Commission ordered heavy damages beyond the actual loss. | To pay punitive damages in appropriate circumstances | Damages punish the wrongdoer.
Q: Which function of consumer organisations is performed? | Educating the public about consumer rights; Publishing periodicals and other publications; Comparative testing of consumer products; Providing legal assistance to consumers; Filing complaints in consumer commissions on behalf of consumers | ngo
- A consumer group in {c} tested ten brands of bottled water in an accredited laboratory and published the results. | Comparative testing of consumer products | Products are tested and compared.
- A consumer NGO held workshops in schools of {c} on consumer rights. | Educating the public about consumer rights | Education through seminars and workshops.
- A consumer organisation brings out a monthly magazine on consumer problems. | Publishing periodicals and other publications | Knowledge is spread through publications.
- A consumer group gave free legal advice to {p} to fight {his} case against {f}. | Providing legal assistance to consumers | Legal help is given.
- A consumer organisation filed a complaint on behalf of an elderly buyer who could not go to the Commission. | Filing complaints in consumer commissions on behalf of consumers | It acts on behalf of consumers.
F: rem | To issue a corrective advertisement | removes the effect of a misleading advertisement; paid for by the guilty party; protects other consumers
F: ngo | Comparative testing of consumer products | done in accredited laboratories; results are published; helps consumers choose
A: A Commission may order a firm to issue a corrective advertisement. | It neutralises the effect of a misleading advertisement. | a | Both true; R explains A.
A: Consumer organisations carry out comparative testing of products. | The results help consumers make informed choices. | a | Both true; R explains A.
A: Punitive damages are paid only for the actual loss suffered. | Punitive damages are meant to punish the wrongdoer. | d | A is false: they are over and above the actual loss. R is true.
A: Consumer organisations can file complaints on behalf of consumers. | Registered consumers' associations are allowed to file complaints. | a | Both true; R explains A.
A: A Commission can order the withdrawal of hazardous goods from sale. | Hazardous goods endanger life and safety. | a | Both true; R explains A.
TT: remedies and consumer organisations
S+: A Commission can order the refund of the price paid.
S+: Consumer organisations educate the public about consumer rights.
S+: A corrective advertisement neutralises the effect of a misleading advertisement.
S+: A Commission can order the withdrawal of hazardous goods.
S-: A Commission can only order an apology from the seller.
S-: Consumer organisations are government departments.
S-: Punitive damages are paid to the seller.
S-: Comparative testing is done by the manufacturer itself.
K: C4 D4 4 | {f} advertised that its herbal tonic cures all diseases, and sold faulty units to many buyers. The Commission ordered it to refund the price and to publish an advertisement correcting its claim. | Identify the two remedies ordered. => To refund the price paid; to issue a corrective advertisement. || State two other remedies available to consumers. => To replace the defective product; to remove the defect; to pay compensation; to pay punitive damages; to withdraw hazardous goods (any two).
K: C4 D5 6 | A consumer NGO in {c} runs workshops on consumer rights, publishes a magazine, tests brands of packaged milk in an accredited laboratory, gives free legal help, and files cases for consumers who cannot do so themselves. | Identify five functions of consumer organisations shown. => Educating the public; publishing periodicals; comparative testing; providing legal assistance; filing complaints on behalf of consumers. || State one more function. => Encouraging consumers to protest against exploitation / filing cases in the interest of the general public.
''', cat='term')

FAMILIES = {S + k: facts(v) for k, v in {
    '09-st1': CH09_ST1, '09-st2': CH09_ST2, '09-st3': CH09_ST3, '09-st4': CH09_ST4, '09-st5': CH09_ST5,
    '10-st1': CH10_ST1, '10-st2': CH10_ST2, '10-st3': CH10_ST3, '10-st4': CH10_ST4,
    '11-st1': CH11_ST1, '11-st2': CH11_ST2, '11-st3': CH11_ST3, '11-st4': CH11_ST4, '11-st5': CH11_ST5,
    '12-st1': CH12_ST1, '12-st2': CH12_ST2, '12-st3': CH12_ST3, '12-st4': CH12_ST4,
}.items()}

FAMILIES[S + '09-st4'] += [
    FF('C3', 'D4', 'numerical', c9_eps, marks=4, kinds=('m4',)),
    FF('C3', 'D2', 'mcq', c9_tradmcq),
    FF('C3', 'D2', 'mcq', c9_icr),
]
