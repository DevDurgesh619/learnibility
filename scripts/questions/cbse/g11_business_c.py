"""CBSE class 11 business studies (NCERT Business Studies XI, 054) families: ch07-ch10.

Every subtopic is a fact table turned into families by g11_accountancy_kit.facts().
Exact MSME investment/turnover limits and scheme numbers that change often are deliberately not asked.
"""
from __future__ import annotations

from g11_accountancy_kit import facts

S = 'cbse-g11-business-ch'

# ---------------- ch07 Sources of Business Finance

PERIOD = ['Long-term source', 'Medium-term source', 'Short-term source', 'Not a source of finance']
CH07_ST1 = dict(
    cat='finance term',
    terms=[
        ('Business finance', 'The money required for carrying out business activities, for both fixed and working capital needs.'),
        ('Fixed capital requirements', 'Funds needed to buy fixed assets such as land, building, plant and machinery.'),
        ('Working capital requirements', 'Funds needed for day-to-day operations such as buying raw materials and paying wages.'),
        ('Owners\' funds', 'Funds provided by the owners of the business, which stay in the business for a long period and carry the risk of the business.'),
        ('Borrowed funds', 'Funds raised through loans or borrowings, on which interest is paid and which must be repaid.'),
        ('Internal sources', 'Funds generated from within the business, such as retained earnings and collection of receivables.'),
        ('External sources', 'Funds raised from outside the business, such as shares, debentures and loans.'),
        ('Factoring', 'A financial service in which a factor buys the trade receivables of a firm and provides it with ready funds.'),
        ('Commercial paper', 'An unsecured promissory note issued by a firm to raise short-term funds, for a period of up to one year.'),
    ],
    lists=[
        ('need', 'reasons why a business needs finance', [
            ('To buy fixed assets', 'Land, building, plant and machinery need fixed capital.'),
            ('To meet working capital needs', 'Raw materials, wages and day-to-day expenses need funds.'),
            ('For growth and expansion', 'New products, markets and plants need funds.'),
            ('For modernisation', 'Replacing old machines with new technology needs funds.')], None),
        ('lt', 'long-term sources of finance', [
            ('Equity shares', 'Ownership capital with no repayment during the life of the company.'),
            ('Retained earnings', 'Profits kept in the business instead of being distributed.'),
            ('Preference shares', 'Shares with preferential rights to dividend and repayment.'),
            ('Debentures', 'Long-term borrowing at a fixed rate of interest.'),
            ('Loans from financial institutions', 'Long-term loans from specialised institutions.')], 'st'),
        ('st', 'short-term sources of finance', [
            ('Trade credit', 'Credit given by suppliers for purchases.'),
            ('Factoring', 'Sale of trade receivables to a factor for ready cash.'),
            ('Short-term loans from commercial banks', 'Cash credit, overdraft and bill discounting.'),
            ('Commercial paper', 'Unsecured promissory notes for up to one year.')], 'lt'),
    ],
    pairs=[('owners\' funds', 'borrowed funds', [
        ('nature', 'capital provided by owners', 'loans and borrowings'),
        ('return', 'dividend or share in profit, not fixed', 'interest at a fixed rate'),
        ('repayment', 'not repaid during the life of the business', 'repaid after a fixed period'),
        ('control', 'gives voting rights and control', 'no voting rights'),
        ('security', 'no security is needed', 'usually secured on assets'),
        ('risk to the business', 'no fixed burden of payment', 'fixed burden of interest and repayment')])],
    scen=[('Classify the source of finance by period.', PERIOD, [
        ('{f} issues equity shares to build a new factory.', 'Long-term source', 'Equity is long-term ownership capital.'),
        ('{f} buys raw material from a supplier and pays after 60 days.', 'Short-term source', 'Trade credit is a short-term source.'),
        ('{f} accepts public deposits for two years.', 'Medium-term source', 'Public deposits for one to five years are medium-term.'),
        ('{f} issues debentures repayable after ten years.', 'Long-term source', 'Debentures are a long-term source.'),
        ('{f} sells its trade receivables to a factor for immediate cash.', 'Short-term source', 'Factoring is a short-term source.'),
        ('{f} issues commercial paper for 90 days.', 'Short-term source', 'Commercial paper is short-term.'),
        ('{f} takes a four-year loan from a bank for new equipment.', 'Medium-term source', 'Loans for one to five years are medium-term.')], None),
        ('Is it owners\' funds or borrowed funds?', ['Owners\' funds', 'Borrowed funds', 'Neither', 'Both owners\' and borrowed funds'], [
        ('{f} raises money by issuing equity shares.', 'Owners\' funds', 'Equity shareholders are owners.'),
        ('{f} keeps ₹5 crore of profit in the business.', 'Owners\' funds', 'Retained earnings belong to owners.'),
        ('{f} issues debentures to the public.', 'Borrowed funds', 'Debenture holders are creditors.'),
        ('{f} takes a term loan from a commercial bank.', 'Borrowed funds', 'A bank loan is borrowed.'),
        ('{f} raises money from public deposits.', 'Borrowed funds', 'Deposits are borrowings that must be repaid.')], None),
        ('Is it an internal or external source?', ['Internal source', 'External source', 'Neither', 'International source'], [
        ('{f} finances expansion from its retained profits.', 'Internal source', 'Retained earnings come from within.'),
        ('{f} speeds up collection from its debtors to raise cash.', 'Internal source', 'Collection of receivables is internal.'),
        ('{f} sells surplus inventory to raise funds.', 'Internal source', 'Disposal of surplus inventory is internal.'),
        ('{f} borrows from a commercial bank.', 'External source', 'Bank loans come from outside the business.'),
        ('{f} issues preference shares.', 'External source', 'Share issue raises funds from outsiders.')], None)],
    ars=[
        ('Business needs finance for fixed as well as working capital.', 'Fixed assets and day-to-day operations both need funds.', 'a', 'Both true and R explains A.'),
        ('Retained earnings are an internal source of finance.', 'Retained earnings are profits ploughed back into the business.', 'a', 'Both true and R explains A.'),
        ('Trade credit is a long-term source of finance.', 'Trade credit is given by suppliers for purchases.', 'd', 'A is false: it is short-term. R is true.'),
        ('Borrowed funds carry a fixed burden of interest.', 'Borrowed funds give lenders voting rights.', 'c', 'A is true; R is false.')],
    tf=('sources of business finance', [
        'Equity shares are a long-term source of finance.',
        'Trade credit is a short-term source.',
        'Retained earnings are an internal source.',
        'Interest must be paid on borrowed funds.'], [
        'Debentures are owners\' funds.',
        'Commercial paper is a long-term secured source.',
        'Owners\' funds must be repaid after a fixed period.',
        'Factoring is a source of long-term finance.']),
    cases=[('C4', 'D4', 4, '{f} of {c} needs funds to build a new plant and to buy raw material for the coming season.',
            [('Classify the two needs.', 'Plant: fixed capital requirement; raw material: working capital requirement.'),
             ('Suggest one suitable source for each.', 'Plant: equity shares, debentures or loans from financial institutions; raw material: trade credit, bank overdraft or cash credit.')]),
           ('C4', 'D5', 6, 'The finance manager of {f} lists: equity shares, trade credit, retained earnings, debentures, factoring and public deposits.',
            [('Classify each by period.', 'Long-term: equity, retained earnings, debentures; medium-term: public deposits; short-term: trade credit, factoring.'),
             ('Classify each by ownership.', 'Owners\' funds: equity, retained earnings; borrowed funds: trade credit, debentures, factoring, public deposits.'),
             ('Which are internal sources?', 'Retained earnings only.')])],
)

SHARES = ['Equity shares', 'Preference shares', 'Retained earnings', 'Debentures']
FEAT_SH = {
    'Equity shares': ['permanent capital', 'no fixed burden of dividend', 'voting rights and control', 'residual claim on income and assets', 'higher cost and dilution of control'],
    'Preference shares': ['fixed rate of dividend', 'preference over equity in dividend and repayment of capital', 'usually no voting rights', 'may be cumulative or convertible'],
    'Retained earnings': ['no explicit cost', 'no dilution of control', 'permanent source', 'reduces dividend to shareholders'],
    'Debentures': ['fixed rate of interest', 'debenture holders are creditors', 'no voting rights', 'interest is tax deductible', 'fixed burden of interest and redemption'],
}
CH07_ST2 = dict(
    cat='term relating to owners\' funds',
    terms=[
        ('Equity shares', 'Shares whose holders are the owners of the company, with voting rights and a residual claim on income and assets.'),
        ('Preference shares', 'Shares that carry a preferential right to dividend at a fixed rate and to repayment of capital on winding up.'),
        ('Retained earnings', 'The part of net profit that is not distributed as dividend but kept for reinvestment (ploughing back of profit).'),
        ('Cumulative preference shares', 'Shares on which unpaid dividend accumulates and is paid in later years before equity dividend.'),
        ('Participating preference shares', 'Shares whose holders share in the surplus profit after the equity dividend at a fixed rate.'),
        ('Convertible preference shares', 'Shares that can be converted into equity shares within a specified period.'),
        ('Trading on equity', 'Use of fixed-cost sources such as debt and preference capital to increase the return to equity shareholders.'),
    ],
    lists=[
        ('eqm', 'merits of equity shares', [
            ('Suitable for investors willing to take risk for higher returns', 'Equity attracts risk-takers.'),
            ('No fixed burden of dividend', 'Dividend is paid only if there are profits.'),
            ('Permanent capital', 'Repayable only on liquidation.'),
            ('Provides credit-worthiness', 'Lenders feel secure when equity is large.'),
            ('Funds can be raised without creating a charge on assets', 'Assets remain free for other borrowing.'),
            ('Democratic control', 'Voting rights give holders a say in management.')], 'eql'),
        ('eql', 'limitations of equity shares', [
            ('Not suited to investors who want steady income', 'Dividends are uncertain.'),
            ('Higher cost', 'Equity is costlier than other sources.'),
            ('Dilution of control', 'New issues reduce the control of existing holders.'),
            ('More formalities and delays', 'Issue of equity involves many legal steps.')], 'eqm'),
        ('rem', 'merits of retained earnings', [
            ('Permanent source of funds', 'Profits ploughed back stay in the business.'),
            ('No explicit cost', 'No interest, dividend or flotation cost is paid.'),
            ('No dilution of control', 'No new shares are issued.'),
            ('Increases credit-worthiness', 'Larger reserves raise the firm\'s capacity to borrow.'),
            ('Helps absorb unexpected losses', 'Reserves cushion bad years.'),
            ('May increase the market price of equity shares', 'Reinvestment can raise future earnings.')], 'rel'),
        ('rel', 'limitations of retained earnings', [
            ('May cause dissatisfaction among shareholders', 'They receive lower dividends.'),
            ('Uncertain source', 'Profits fluctuate from year to year.'),
            ('Opportunity cost is often ignored', 'Funds may be used less carefully because they seem free.')], 'rem'),
        ('pref', 'types of preference shares', [
            ('Cumulative and non-cumulative', 'Unpaid dividend accumulates or lapses.'),
            ('Participating and non-participating', 'Holders may or may not share in surplus profit.'),
            ('Convertible and non-convertible', 'Shares may or may not be converted into equity.'),
            ('Redeemable', 'Shares are repaid after a fixed period.')], None),
    ],
    pairs=[('equity shares', 'preference shares', [
        ('dividend', 'not fixed; paid after preference dividend', 'paid at a fixed rate, before equity'),
        ('voting rights', 'full voting rights', 'usually no voting rights'),
        ('repayment of capital on winding up', 'repaid last, after all others', 'repaid before equity shareholders'),
        ('risk', 'highest risk', 'lower risk'),
        ('suitable for', 'investors willing to take risk', 'investors who want steady income with less risk'),
        ('convertibility', 'cannot be converted', 'may be convertible into equity')])],
    scen=[('Which source of owners\' funds or alternative is described?', SHARES, [
        ('{f} keeps 40% of this year\'s profit in the business to buy new machines instead of paying it as dividend.', 'Retained earnings', 'Ploughing back of profit.'),
        ('Investors in {f} will receive a fixed 8% dividend before any dividend is paid to owners with voting rights.', 'Preference shares', 'Fixed preferential dividend.'),
        ('{f} issues shares whose holders vote at meetings and get whatever is left after all claims.', 'Equity shares', 'Voting rights and residual claim.'),
        ('{f} raises ₹10 crore at a fixed 9% interest, repayable after seven years, with no voting rights to the holders.', 'Debentures', 'Fixed interest and repayment make it debt, not owners\' funds.'),
        ('{p} wants an investment in {f} with steady income and priority in repayment over owners.', 'Preference shares', 'Fixed dividend and priority in repayment.'),
        ('{p} is willing to take high risk in the hope of high returns and wants a say in management of {f}.', 'Equity shares', 'Risk-takers with voting rights prefer equity.')], 'sh')],
    feat={'sh': FEAT_SH},
    ars=[
        ('Equity shares are a permanent source of capital.', 'Equity capital is repaid only on liquidation of the company.', 'a', 'Both true and R explains A.'),
        ('Retained earnings do not dilute control.', 'No new shares are issued when profits are ploughed back.', 'a', 'Both true and R explains A.'),
        ('Preference shareholders have full voting rights on all matters.', 'Preference shareholders get a fixed rate of dividend.', 'd', 'A is false: they usually have no voting rights. R is true.'),
        ('Retained earnings have no explicit cost.', 'Retained earnings are a borrowed fund.', 'c', 'A is true; R is false: they are owners\' funds.'),
        ('Equity shareholders bear the highest risk.', 'They have a residual claim on income and assets.', 'a', 'Both true and R explains A.')],
    tf=('equity shares, preference shares and retained earnings', [
        'Equity shareholders have voting rights.',
        'Preference shares carry a fixed rate of dividend.',
        'Retained earnings are an internal source.',
        'Issue of equity shares may dilute control.'], [
        'Equity dividend is fixed in advance.',
        'Preference shareholders are paid after equity shareholders on winding up.',
        'Retained earnings have a high flotation cost.',
        'Cumulative preference dividend lapses if not paid.']),
    cases=[('C4', 'D4', 4, 'The promoters of {f} want to raise ₹50 crore but do not want to lose control or carry a fixed burden of payment. The company has large accumulated profits.',
            [('Which source suits them best and why?', 'Retained earnings: no dilution of control, no fixed burden, no explicit cost.'),
             ('Give one limitation of this source.', 'Shareholders may be unhappy with lower dividends; it is uncertain and limited by profit.')]),
           ('C4', 'D5', 6, '{p} has ₹5 lakh to invest. {He} wants steady income and is not interested in voting. {p2} wants a higher return and a voice in management.',
            [('Which type of shares suits each?', '{p}: preference shares; {p2}: equity shares.'),
             ('Give two reasons for each choice.', 'Preference: fixed dividend, priority in dividend and repayment. Equity: higher return in good years, voting rights.'),
             ('State one risk {p2} faces.', 'Dividend is uncertain and equity is repaid last on winding up.')])],
)

BOR = ['Debentures', 'Loans from commercial banks', 'Loans from financial institutions', 'Trade credit', 'Public deposits']
FEAT_BOR = {
    'Debentures': ['fixed rate of interest', 'no dilution of control', 'interest is tax deductible', 'fixed burden of interest and redemption'],
    'Loans from commercial banks': ['timely funds as needed', 'secrecy is maintained', 'flexible amount', 'generally for short periods; strict conditions'],
    'Loans from financial institutions': ['long-term finance', 'financial, managerial and technical advice', 'repayment in easy instalments', 'restrictive terms and lengthy procedure'],
    'Trade credit': ['convenient and continuous source', 'readily available to creditworthy firms', 'no charge on assets', 'limited amount; may induce overtrading'],
    'Public deposits': ['simple procedure', 'cost lower than bank loans', 'no charge on assets', 'no dilution of control'],
}
CH07_ST3 = dict(
    cat='borrowed fund',
    terms=[
        ('Debentures', 'Instruments acknowledging a debt, issued to raise long-term funds at a fixed rate of interest.'),
        ('Trade credit', 'Credit extended by one trader to another when goods and services are bought, shown as sundry creditors or accounts payable.'),
        ('Public deposits', 'Deposits raised by organisations directly from the public, usually at a rate higher than bank deposit rates.'),
        ('Secured debentures', 'Debentures on which a charge is created on the assets of the company.'),
        ('Convertible debentures', 'Debentures that are converted into equity shares after a specified period.'),
        ('Term loan', 'A loan from a bank or financial institution for a fixed period, repaid in instalments.'),
        ('Financial institutions', 'Specialised institutions set up by central and state governments to provide medium- and long-term finance to business.'),
    ],
    lists=[
        ('debm', 'merits of debentures', [
            ('Preferred by investors who want fixed income at less risk', 'Interest is fixed and secured.'),
            ('No dilution of control', 'Debenture holders have no voting rights.'),
            ('Less costly than equity', 'Interest is tax deductible.'),
            ('Suitable when sales and earnings are stable', 'The firm can pay fixed interest easily.')], 'debl'),
        ('debl', 'limitations of debentures', [
            ('Fixed charge on the company', 'Interest must be paid even in bad years.'),
            ('Burden of redemption', 'The company must repay on the due date.'),
            ('Reduces borrowing capacity', 'Assets are charged, limiting further loans.')], 'debm'),
        ('bank', 'merits of loans from commercial banks', [
            ('Timely assistance', 'Funds are available when needed.'),
            ('Secrecy', 'Information given to the bank is kept confidential.'),
            ('Easier source', 'No prospectus or underwriting is needed.'),
            ('Flexible amount', 'Loans can be increased or repaid early.')], 'debl'),
        ('fi', 'merits of loans from financial institutions', [
            ('Long-term finance', 'Funds not available from banks can be obtained.'),
            ('Financial, managerial and technical advice', 'Institutions also guide the borrower.'),
            ('Increases goodwill of the borrower', 'Other lenders trust a firm backed by the institution.'),
            ('Easy instalments', 'Repayment does not burden the firm much.'),
            ('Available even in depression', 'Funds come when capital markets are weak.')], None),
        ('tcm', 'merits of trade credit', [
            ('Convenient and continuous source', 'Comes with regular purchases.'),
            ('Readily available to creditworthy firms', 'Suppliers grant it to known buyers.'),
            ('Helps increase sales', 'Firms can stock more and sell more.'),
            ('Finances building up of inventory', 'Stock can be bought before payment.'),
            ('No charge on assets', 'No security is required.')], 'tcl'),
        ('tcl', 'limitations of trade credit', [
            ('May induce overtrading', 'Easy credit can tempt the firm to buy beyond its capacity.'),
            ('Limited amount', 'Only a limited sum can be raised.'),
            ('Costly compared to other sources', 'Cash discount is lost when credit is used.')], 'tcm'),
        ('pdm', 'merits of public deposits', [
            ('Simple procedure', 'Fewer formalities than shares or debentures.'),
            ('Lower cost than bank loans', 'Interest is lower than on bank loans.'),
            ('No charge on assets', 'Deposits are generally unsecured.'),
            ('No dilution of control', 'Depositors have no voting rights.')], None),
    ],
    pairs=[('debentures', 'shares', [
        ('status of holder', 'creditor of the company', 'owner of the company'),
        ('return', 'interest at a fixed rate', 'dividend'),
        ('voting rights', 'no voting rights', 'voting rights (equity)'),
        ('security', 'usually secured on assets', 'not secured'),
        ('repayment', 'repaid after a fixed period', 'equity not repaid during the life of the company'),
        ('tax treatment of return', 'interest is a tax-deductible expense', 'dividend is an appropriation of profit')])],
    scen=[('Which borrowed fund is described?', BOR, [
        ('{f} issues instruments carrying 9% interest, secured on its plant, repayable after eight years.', 'Debentures', 'Fixed-interest debt instruments are debentures.'),
        ('{f} buys {g} from a supplier and is allowed 45 days to pay.', 'Trade credit', 'Credit from suppliers on purchases.'),
        ('{f} invites the public to deposit money with it for two years at 8.5% interest.', 'Public deposits', 'Deposits raised directly from the public.'),
        ('{f} gets cash credit against its stock from a bank in {c}.', 'Loans from commercial banks', 'Cash credit is bank lending.'),
        ('{f} gets a 12-year loan and technical advice from a state financial corporation.', 'Loans from financial institutions', 'Long-term loans with advice come from financial institutions.'),
        ('{f} wants funds quickly without making its plans public and approaches its banker.', 'Loans from commercial banks', 'Bank loans are timely and secret.')], 'bor')],
    feat={'bor': FEAT_BOR},
    ars=[
        ('Debentures do not dilute the control of equity shareholders.', 'Debenture holders do not have voting rights.', 'a', 'Both true and R explains A.'),
        ('Trade credit may induce a firm to overtrade.', 'Credit is easily available from suppliers.', 'a', 'Both true and R explains A.'),
        ('Interest on debentures is paid only when the company earns profit.', 'Debenture holders are creditors of the company.', 'd', 'A is false: interest is payable even in a loss. R is true.'),
        ('Financial institutions provide long-term finance.', 'Financial institutions accept deposits only from the public on demand.', 'c', 'A is true; R is false.'),
        ('Public deposits do not dilute control.', 'Depositors are not owners and have no voting rights.', 'a', 'Both true and R explains A.')],
    tf=('borrowed funds', [
        'Debenture holders are creditors of the company.',
        'Trade credit appears as sundry creditors in the books of the buyer.',
        'Interest on debentures is a tax-deductible expense.',
        'Financial institutions also give managerial and technical advice.'], [
        'Debenture holders have voting rights.',
        'Trade credit is a long-term source of finance.',
        'Public deposits always require a charge on assets.',
        'Interest on debentures need not be paid in a year of loss.']),
    cases=[('C4', 'D4', 4, '{f} has stable sales and earnings. It needs ₹20 crore for ten years but its promoters do not want to give up control.',
            [('Suggest a suitable source and justify.', 'Debentures (or a long-term loan from financial institutions): fixed interest, no dilution of control, suits stable earnings.'),
             ('State one limitation of the source.', 'Fixed charge of interest even in bad years, burden of redemption, reduced borrowing capacity (any one).')]),
           ('C4', 'D5', 6, '{f}, a {g} trader in {c}, has a festival order. It needs funds for 60 days to buy stock and has good relations with suppliers and its bank.',
            [('Suggest two suitable sources.', 'Trade credit from suppliers; overdraft or cash credit from its bank.'),
             ('Give two merits of each.', 'Trade credit: convenient, readily available, no charge on assets. Bank credit: timely, flexible, secret.'),
             ('Why would debentures be unsuitable?', 'They are a long-term source with formalities and fixed interest; the need is short-term.')])],
)

INTL = ['ADR', 'GDR', 'FCCB', 'IDR', 'Loan from international agencies']
CH07_ST4 = dict(
    cat='international source of finance',
    terms=[
        ('GDR', 'A depository receipt issued in a foreign currency against the shares of an Indian company, listed and traded on a stock exchange outside the USA (global depository receipt).'),
        ('ADR', 'A depository receipt issued by a company that can be issued only to American citizens and traded on American stock exchanges (American depository receipt).'),
        ('IDR', 'A depository receipt denominated in Indian rupees, issued in India by a foreign company (Indian depository receipt).'),
        ('FCCB', 'An equity-linked debt instrument issued in a foreign currency, carrying a fixed interest rate, that can be converted into shares at a predetermined price (foreign currency convertible bond).'),
        ('International agencies', 'Bodies such as the International Finance Corporation and the Asian Development Bank that provide long-term finance for development.'),
    ],
    lists=[
        ('src', 'international sources of finance', [
            ('Commercial banks', 'Foreign commercial banks give foreign currency loans for business.'),
            ('International agencies and development banks', 'Bodies such as IFC, EXIM Bank and ADB provide long- and medium-term loans.'),
            ('International capital markets: GDRs', 'Depository receipts traded on stock exchanges outside the USA.'),
            ('International capital markets: ADRs', 'Depository receipts traded in the USA.'),
            ('International capital markets: FCCBs', 'Convertible bonds issued in foreign currency.')], None),
        ('gdr', 'features of GDRs', [
            ('Issued in foreign currency against shares of an Indian company', 'The shares are held by a depository bank.'),
            ('Listed and traded on stock exchanges outside the USA', 'For example in London or Luxembourg.'),
            ('Holders get dividends like shareholders', 'Dividends are paid in rupees and converted.'),
            ('No voting rights', 'GDR holders do not vote.'),
            ('Can be converted into shares', 'The holder can cancel the GDR and hold the underlying shares.')], None),
    ],
    pairs=[('GDR', 'ADR', [
        ('where traded', 'stock exchanges outside the USA, such as London or Luxembourg', 'American stock exchanges'),
        ('who can buy', 'investors in many countries', 'only American citizens'),
        ('regulation', 'the rules of the country where listed', 'US securities rules'),
        ('currency', 'usually US dollars or other foreign currency', 'US dollars')]),
        ('FCCB', 'GDR', [
        ('nature', 'debt that can be converted into equity', 'equity-based depository receipt'),
        ('return before conversion', 'fixed interest (coupon)', 'dividend'),
        ('conversion', 'converted into shares at a predetermined price', 'can be exchanged for the underlying shares'),
        ('obligation', 'company must repay if not converted', 'no repayment obligation')])],
    scen=[('Which international source of finance is used?', INTL, [
        ('An Indian company issues receipts in US dollars against its shares and lists them on the London Stock Exchange.', 'GDR', 'Depository receipts listed outside the USA are GDRs.'),
        ('An Indian IT company issues depository receipts that are traded on the New York Stock Exchange and bought only by American citizens.', 'ADR', 'Receipts traded in the USA are ADRs.'),
        ('{f} issues bonds in euros at 2% interest, convertible into its shares at a fixed price after three years.', 'FCCB', 'Equity-linked foreign currency convertible bonds.'),
        ('A foreign company issues rupee-denominated depository receipts to investors in India.', 'IDR', 'Rupee receipts issued in India by a foreign company are IDRs.'),
        ('{f} receives a long-term loan from the Asian Development Bank for a power project.', 'Loan from international agencies', 'ADB is an international development agency.')], None)],
    ars=[
        ('GDR holders do not have voting rights.', 'GDRs are issued against the shares of a company held by a depository.', 'b', 'Both true, but R does not explain the absence of voting rights.'),
        ('ADRs can be bought by investors of any country.', 'ADRs are traded on American stock exchanges.', 'd', 'A is false: ADRs can be issued only to American citizens. R is true.'),
        ('FCCBs are equity-linked debt instruments.', 'FCCBs carry fixed interest and can be converted into shares.', 'a', 'Both true and R explains A.'),
        ('IDRs are issued by Indian companies abroad.', 'IDRs are denominated in Indian rupees.', 'd', 'A is false: foreign companies issue IDRs in India. R is true.')],
    tf=('international sources of finance', [
        'GDRs are traded on stock exchanges outside the USA.',
        'ADRs can be issued only to American citizens.',
        'FCCBs carry a fixed rate of interest until conversion.'], [
        'GDR holders have full voting rights.',
        'ADRs are traded on the Bombay Stock Exchange.',
        'FCCBs can never be converted into shares.',
        'IDRs are issued in US dollars.']),
    cases=[('C4', 'D4', 4, '{f}, an Indian company, wants foreign investors to buy into it without listing directly abroad. It is choosing between London and New York.',
            [('Name the instrument for each market.', 'London: GDR; New York: ADR.'),
             ('State one difference between them.', 'GDRs are traded outside the USA and open to investors in many countries; ADRs are traded in the USA and only Americans can buy them.')]),
           ('C4', 'D5', 4, '{f} needs foreign currency funds at low interest now but is willing to give equity later if its share price rises.',
            [('Suggest an instrument.', 'FCCB (foreign currency convertible bond).'),
             ('Explain why it suits {f}.', 'It carries a low fixed interest now and converts into shares at a predetermined price later, so the company may not have to repay.')])],
)

FACT = ['Cost', 'Financial strength and stability of operations', 'Form of business organisation and legal status', 'Purpose and time period', 'Risk profile', 'Control', 'Effect on creditworthiness', 'Flexibility and ease', 'Tax benefits']
CH07_ST5 = dict(
    lists=[('fac', 'factors affecting the choice of source of funds', [
        ('Cost', 'Both the cost of raising funds (procurement) and the cost of using them should be considered.'),
        ('Financial strength and stability of operations', 'A firm with stable earnings can pay fixed charges; others should avoid them.'),
        ('Form of business organisation and legal status', 'A partnership cannot issue shares; a company can.'),
        ('Purpose and time period', 'Short-term needs use short-term sources; long-term needs use long-term sources.'),
        ('Risk profile', 'Equity carries least risk to the firm; debt carries a fixed burden.'),
        ('Control', 'Equity issue may dilute control; debt does not.'),
        ('Effect on creditworthiness', 'Some sources, such as secured debentures, reduce the firm\'s capacity to borrow further.'),
        ('Flexibility and ease', 'Restrictive terms and lengthy procedures make some sources less attractive.'),
        ('Tax benefits', 'Interest on debt is tax deductible while dividend is not.')], None)],
    scen=[('Which factor affecting the choice of source of funds is considered?', FACT, [
        ('{f} prefers debentures to preference shares because interest is tax deductible.', 'Tax benefits', 'Interest on debt reduces taxable profit.'),
        ('The promoters of {f} refuse to issue more equity because they do not want to lose their majority.', 'Control', 'Equity issue may dilute control.'),
        ('{f} has very irregular earnings and avoids sources with a fixed charge.', 'Financial strength and stability of operations', 'Unstable firms should avoid fixed burdens.'),
        ('{p} and {p2}, partners in a firm, realise they cannot issue shares.', 'Form of business organisation and legal status', 'Only companies can issue shares.'),
        ('{f} uses trade credit for raw material but issues shares for its new factory.', 'Purpose and time period', 'The source should match the period of need.'),
        ('{f} compares the floatation costs and interest of each option before choosing.', 'Cost', 'Cost of procurement and use of funds is compared.'),
        ('{f} rejects a loan because the lender wants to approve all its future borrowings.', 'Flexibility and ease', 'Restrictive conditions reduce flexibility.'),
        ('{f} avoids secured debentures because charging its assets would make banks reluctant to lend later.', 'Effect on creditworthiness', 'Some sources reduce future borrowing capacity.')], None)],
    ars=[
        ('Interest on debt gives a tax benefit.', 'Interest is a tax-deductible expense.', 'a', 'Both true and R explains A.'),
        ('A firm with unstable earnings should prefer equity to debt.', 'Equity does not carry a fixed burden of payment.', 'a', 'Both true and R explains A.'),
        ('Issue of debentures dilutes the control of existing owners.', 'Debenture holders are creditors without voting rights.', 'd', 'A is false; R is true.'),
        ('A partnership firm can raise funds by issuing equity shares.', 'Form of organisation affects the choice of source.', 'd', 'A is false: only companies issue shares. R is true.')],
    tf=('factors affecting choice of source of funds', [
        'Cost of raising and using funds affects the choice of source.',
        'Interest on borrowed funds is tax deductible.',
        'Equity issue may dilute control.'], [
        'A partnership can issue shares to the public.',
        'Firms with unstable earnings should rely on fixed-charge sources.',
        'Short-term needs should be met by issuing equity shares.',
        'Debt never affects a firm\'s creditworthiness.']),
    cases=[('C4', 'D4', 4, '{f} needs ₹30 crore for expansion. Its earnings are stable, its promoters want to keep control and it pays tax at a high rate.',
            [('Which source would you recommend, debentures or equity?', 'Debentures.'),
             ('Name three factors that support your choice.', 'Control (no dilution), tax benefits (interest deductible), financial strength and stability (can bear fixed interest).')]),
           ('C4', 'D5', 6, 'Compare the suitability of equity and debentures for: (a) a new start-up with uncertain earnings, (b) a mature company with steady profits.',
            [('Suggest the source for each.', '(a) Equity; (b) debentures.'),
             ('Give the factors that decide each case.', '(a) Risk profile and stability: no fixed burden. (b) Cost, tax benefit and control.')])],
)

# ---------------- ch08 Small Business and Entrepreneurship Development

FUND = ['Bootstrapping', 'Crowdfunding', 'Angel investment', 'Venture capital', 'Business incubators']
CH08_ST1 = dict(
    cat='term',
    terms=[
        ('Entrepreneurship', 'The process of setting up one\'s own business as distinct from pursuing any other economic activity, be it employment or profession.'),
        ('Entrepreneur', 'The person who sets up his or her own business.'),
        ('Enterprise', 'The business unit set up by an entrepreneur.'),
        ('Startup India', 'A government scheme launched in 2016 to build an ecosystem that supports startups through simplification, funding and incubation.'),
        ('Bootstrapping', 'Starting a business with one\'s own savings and early revenues, without external funding.'),
        ('Crowdfunding', 'Raising small amounts of money from a large number of people, usually through online platforms.'),
        ('Angel investors', 'Wealthy individuals who invest their own money in early-stage startups in return for equity.'),
        ('Venture capital', 'Professionally managed funds invested in startups with high growth potential in return for equity.'),
    ],
    lists=[
        ('char', 'characteristics of entrepreneurship', [
            ('Systematic activity', 'It needs knowledge, skills and competencies that can be learnt.'),
            ('Lawful and purposeful activity', 'It is undertaken within the law to create value and earn profit.'),
            ('Innovation', 'It creates new products, processes or markets.'),
            ('Organisation of production', 'The entrepreneur brings together land, labour and capital.'),
            ('Risk-taking', 'The entrepreneur bears the risk of the business.')], None),
        ('need', 'reasons why entrepreneurship is needed in an economy', [
            ('Creates employment', 'New ventures provide jobs for others.'),
            ('Promotes innovation', 'Entrepreneurs bring new products and processes.'),
            ('Increases national income', 'New production adds to GDP.'),
            ('Balanced regional development', 'Enterprises can be set up in backward areas.'),
            ('Improves standard of living', 'New goods and services become available.')], None),
        ('plan', 'action points of the Startup India scheme', [
            ('Simplification and handholding', 'Easier compliance and a single point of contact for startups.'),
            ('Funding support and incentives', 'A fund of funds and tax benefits for eligible startups.'),
            ('Industry-academia partnership and incubation', 'Incubators and research parks in academic institutions.')], None),
        ('ways', 'ways to fund a startup', [
            ('Bootstrapping', 'Using one\'s own savings and early revenue.'),
            ('Crowdfunding', 'Pooling small contributions from many people online.'),
            ('Angel investment', 'Individuals invest their own money for equity.'),
            ('Venture capital', 'Professional funds invest in high-growth firms.'),
            ('Business incubators and accelerators', 'Support early-stage firms with space, mentoring and funds.'),
            ('Microfinance and NBFCs', 'Small loans for those without access to banks.')], None),
    ],
    pairs=[('entrepreneurship', 'employment', [
        ('nature', 'setting up one\'s own business', 'working for others'),
        ('reward', 'profit, which is uncertain', 'salary or wages, which are fixed'),
        ('risk', 'the entrepreneur bears risk', 'little or no risk'),
        ('decision making', 'the entrepreneur decides', 'employee follows instructions'),
        ('capital', 'needed', 'not needed')])],
    scen=[('How is the startup being funded?', FUND, [
        ('{p} started a {g} business using {his} own savings and reinvested every rupee of early sales.', 'Bootstrapping', 'Own savings and revenue, no outside funds.'),
        ('{p} raised small amounts from 2,000 people on an online platform to launch {his} product.', 'Crowdfunding', 'Many small contributions online.'),
        ('A retired businessman invested ₹25 lakh of his own money in {f} for a 10% stake.', 'Angel investment', 'An individual invests own money for equity.'),
        ('A professionally managed fund invested ₹20 crore in {f} because of its high growth potential.', 'Venture capital', 'Professional funds investing for equity.'),
        ('{p}\'s startup got office space, mentoring and seed money from a centre run by an engineering college.', 'Business incubators', 'Incubators support early-stage startups.')], None),
        ('Which characteristic of entrepreneurship is shown?', ['Innovation', 'Risk-taking', 'Organisation of production', 'Systematic activity', 'Lawful and purposeful activity'], [
        ('{p} invented a low-cost water filter and started selling it in villages near {c}.', 'Innovation', 'A new product creates value.'),
        ('{p} put all {his} savings into a new venture knowing it might fail.', 'Risk-taking', 'The entrepreneur bears the risk.'),
        ('{p} brought together land, workers and machines to start a {g} unit.', 'Organisation of production', 'Combining factors of production.'),
        ('{p} attended a training course to learn how to plan and run a business before starting one.', 'Systematic activity', 'Entrepreneurship needs skills that can be learnt.')], None)],
    ars=[
        ('Entrepreneurship involves risk-taking.', 'The entrepreneur\'s return depends on the success of the business.', 'a', 'Both true and R explains A.'),
        ('Entrepreneurship is a systematic activity.', 'Entrepreneurial skills can be learnt.', 'a', 'Both true and R explains A.'),
        ('An entrepreneur is assured a fixed salary.', 'Entrepreneurs set up their own businesses.', 'd', 'A is false: the reward is uncertain profit. R is true.'),
        ('Startup India aims to support new enterprises.', 'Startup India funds only large established companies.', 'c', 'A is true; R is false.')],
    tf=('entrepreneurship and Startup India', [
        'Entrepreneurship involves setting up one\'s own business.',
        'Innovation is a characteristic of entrepreneurship.',
        'Crowdfunding raises small amounts from many people.',
        'Startup India includes funding support and incubation.'], [
        'An entrepreneur bears no risk.',
        'Entrepreneurship skills cannot be learnt.',
        'Angel investors are banks that give loans to startups.',
        'Startup India was launched to support only foreign companies.']),
    cases=[('C4', 'D4', 4, '{p}, an engineering student in {c}, has an idea for a solar-powered water pump. {He} has little money and no business experience.',
            [('Suggest two ways {he} could fund the startup.', 'Bootstrapping, crowdfunding, angel investors, incubators (any two).'),
             ('How can Startup India help?', 'Simplified compliance and handholding, funding support, incubation through industry-academia partnership.')]),
           ('C4', 'D5', 6, '{p} left a salaried job to start {f}, which makes eco-friendly packaging from farm waste.',
            [('Compare {his} old and new occupations on reward and risk.', 'Employment: fixed salary, little risk. Entrepreneurship: uncertain profit, risk is borne.'),
             ('Identify two characteristics of entrepreneurship in the case.', 'Innovation (new product from waste), risk-taking, organisation of production (any two).'),
             ('How does such enterprise help the economy?', 'Creates jobs, adds to national income, reduces waste, balanced regional development.')])],
)

CH08_ST2 = dict(
    cat='term relating to small business',
    terms=[
        ('MSMED Act, 2006', 'The law that defines micro, small and medium enterprises in India and provides for their promotion and development.'),
        ('Micro, small and medium enterprises', 'Enterprises classified as micro, small or medium on the basis of limits on investment and turnover laid down by the government.'),
        ('Cottage industries', 'Industries organised by individuals with private resources, using family labour and simple equipment, often at home.'),
        ('Village industries', 'Industries located in rural areas that produce goods or render services using local resources.'),
        ('Ancillary unit', 'A small unit that supplies parts and components to a large industry.'),
    ],
    lists=[
        ('role', 'roles of small business in India', [
            ('Large source of employment', 'Small industries are the second largest employer after agriculture.'),
            ('Balanced regional development', 'They can be set up in rural and backward areas.'),
            ('Wide variety of products', 'They make many goods, from soaps to readymade garments and electronics.'),
            ('Contribution to exports', 'They account for a large share of India\'s exports.'),
            ('Support to large industries', 'They supply parts and components as ancillary units.'),
            ('Opportunities for entrepreneurship', 'Low capital needs let many people start businesses.'),
            ('Low cost of production', 'Local resources and low overheads keep costs low.'),
            ('Quick decision-making and personalised service', 'Small size allows flexibility and close contact with customers.')], None),
        ('rural', 'roles of small business in rural areas', [
            ('Employment in rural areas', 'Jobs for artisans and rural people near their homes.'),
            ('Reduces migration to cities', 'Rural jobs check movement to towns.'),
            ('Use of local resources and skills', 'Local raw materials and crafts are used.'),
            ('Increases rural incomes', 'Families earn more from non-farm work.')], None),
        ('cottage', 'features of cottage industries', [
            ('Organised by individuals with private resources', 'The owner provides the capital.'),
            ('Use of family labour and local talent', 'Family members do the work.'),
            ('Simple equipment', 'Simple tools are used.'),
            ('Small capital investment', 'Little money is needed.'),
            ('Simple products, often made at home', 'Products are simple and made with indigenous technology.')], None),
    ],
    scen=[('Which role of small business is illustrated?', ['Large source of employment', 'Balanced regional development', 'Support to large industries', 'Contribution to exports', 'Low cost of production'], [
        ('Small units in a backward district near {c} have brought jobs and income to the area.', 'Balanced regional development', 'Industries spread to backward areas.'),
        ('A small unit in {c} makes brake parts for a large car maker.', 'Support to large industries', 'Ancillary units supply large industries.'),
        ('Handicraft units of {c} sell most of their output to buyers abroad.', 'Contribution to exports', 'Small units earn foreign exchange.'),
        ('Thousands of small {g} units together employ more people than the few large factories in {c}.', 'Large source of employment', 'Small business is labour intensive.'),
        ('A small unit uses local materials and has low overheads, so it sells at lower prices than big brands.', 'Low cost of production', 'Local resources and low overheads cut costs.')], None)],
    ars=[
        ('Small industries help in balanced regional development.', 'They can be set up in rural and backward areas.', 'a', 'Both true and R explains A.'),
        ('Small units can give personalised service to customers.', 'Small units are in close contact with their customers.', 'a', 'Both true and R explains A.'),
        ('Small industries need very large capital investment.', 'Small industries are labour intensive.', 'd', 'A is false: they need small capital. R is true.'),
        ('Cottage industries use family labour.', 'Cottage industries always use advanced imported technology.', 'c', 'A is true; R is false: they use simple, indigenous technology.')],
    tf=('small business in India', [
        'Small industries are an important source of employment.',
        'The MSMED Act, 2006 provides for the definition and development of MSMEs.',
        'Cottage industries use simple equipment and family labour.'], [
        'Small industries cannot be set up in rural areas.',
        'Small industries make no contribution to exports.',
        'Cottage industries need very large capital.',
        'Ancillary units compete with large industries and never supply them.']),
    cases=[('C4', 'D4', 4, 'The government of a state plans to promote small units in its backward districts rather than one large steel plant.',
            [('Give two reasons why small units suit this aim.', 'They create more jobs per rupee of capital; they can be set up in rural and backward areas (balanced regional development); they use local resources.'),
             ('Name one problem these units may face.', 'Finance, raw materials, marketing, managerial skill, technology (any one).')]),
           ('C4', 'D5', 6, '{p} makes handloom sarees at home in a village near {c} with the help of {his} family, using simple looms.',
            [('What kind of industry is this? Give two features.', 'Cottage industry: family labour, simple equipment, small capital, made at home (any two).'),
             ('State two ways such industries help rural areas.', 'Rural employment, reduced migration, use of local skills, higher rural incomes (any two).'),
             ('Suggest one form of help {p} could seek.', 'Credit from banks or NABARD-supported schemes; marketing help from government agencies; training through the DIC.')])],
)

AGENCY = ['NSIC', 'DIC', 'NABARD', 'SIDBI']
CH08_ST3 = dict(
    cat='term',
    terms=[
        ('NSIC', 'National Small Industries Corporation, set up in 1955 to promote, aid and foster the growth of small business units.'),
        ('DIC', 'District Industries Centre, the institution at the district level that provides all services and support to small entrepreneurs under a single roof.'),
        ('NABARD', 'National Bank for Agriculture and Rural Development, set up in 1982 to promote integrated rural development, including small rural industries.'),
        ('SIDBI', 'Small Industries Development Bank of India, set up in 1990 as the principal institution for financing and developing small-scale industry.'),
        ('Sickness of small units', 'A situation in which a small unit cannot meet its obligations and runs at a loss because of internal or external problems.'),
    ],
    lists=[
        ('prob', 'problems of small business', [
            ('Finance', 'Lack of adequate funds; small units find it hard to borrow.'),
            ('Raw materials', 'They buy in small quantities, pay higher prices and get poor quality.'),
            ('Managerial skills', 'The owner may lack all the skills needed to run the business.'),
            ('Marketing', 'They depend on middlemen and cannot advertise widely.'),
            ('Quality', 'They may not follow standard quality controls.'),
            ('Capacity utilisation', 'Lack of demand leads to idle capacity and higher cost.'),
            ('Technology', 'Outdated technology lowers productivity.'),
            ('Sickness', 'Many units become sick due to internal and external problems.'),
            ('Global competition', 'They face competition from large and foreign firms.')], None),
        ('nsic', 'functions of NSIC', [
            ('Supplies indigenous and imported machines on hire-purchase', 'Small units get machines on easy terms.'),
            ('Procures and supplies raw materials', 'It arranges scarce and imported raw materials.'),
            ('Helps export of products', 'It promotes export of small units\' products.'),
            ('Provides marketing support and consultancy', 'It helps small units sell and advises them.'),
            ('Supports technology upgradation', 'It helps units adopt better technology.')], None),
        ('dic', 'functions of DICs', [
            ('Identify potential entrepreneurs', 'Find and guide people who can start units.'),
            ('Prepare feasibility reports', 'Advise on viable industries in the district.'),
            ('Arrange credit', 'Help entrepreneurs get loans from banks.'),
            ('Arrange raw materials and machinery', 'Help procure inputs.'),
            ('Training and marketing support', 'Train entrepreneurs and help them sell.')], None),
    ],
    scen=[('Which institution would help?', AGENCY, [
        ('{p}, a small manufacturer, wants to buy a machine on hire-purchase and get help in exporting {his} products.', 'NSIC', 'NSIC supplies machines on hire-purchase and helps exports.'),
        ('{p} wants advice, a feasibility report and help with a bank loan, all at one office in {his} district.', 'DIC', 'The DIC provides support to small entrepreneurs at the district level under one roof.'),
        ('A cooperative of rural artisans near {c} needs credit for a village industry project.', 'NABARD', 'NABARD supports rural industries and artisans.'),
        ('A small-scale unit needs refinance and development support from the principal bank for small industry.', 'SIDBI', 'SIDBI is the principal institution for financing small industry.')], None),
        ('Which problem of small business is it?', ['Finance', 'Raw materials', 'Marketing', 'Technology', 'Global competition', 'Managerial skills'], [
        ('{f}, a small unit, cannot get a bank loan because it has no assets to offer as security.', 'Finance', 'Lack of credit and collateral.'),
        ('{f} buys inputs in small lots and pays more than large firms for poorer quality.', 'Raw materials', 'Small purchases mean high prices and poor quality.'),
        ('{f} depends on middlemen to sell its {g} and cannot afford advertising.', 'Marketing', 'Weak marketing and dependence on middlemen.'),
        ('{f} still uses machines that are thirty years old, so its output per worker is low.', 'Technology', 'Outdated technology lowers productivity.'),
        ('Cheap imported {g} are taking away customers from small units in {c}.', 'Global competition', 'Competition from foreign firms.'),
        ('The owner of {f} is a skilled craftsman but has no idea of accounts or planning.', 'Managerial skills', 'Lack of managerial skills.')], None)],
    ars=[
        ('Small units find it difficult to raise finance.', 'They lack assets to offer as security and have low creditworthiness.', 'a', 'Both true and R explains A.'),
        ('DICs provide support to small entrepreneurs at the district level.', 'DICs act as a single window for small industries in the district.', 'a', 'Both true and R explains A.'),
        ('Small units get raw materials at lower prices than large units.', 'Small units buy in small quantities.', 'd', 'A is false: they pay higher prices. R is true.'),
        ('NSIC helps small units in exporting.', 'NSIC was set up to regulate the stock market.', 'c', 'A is true; R is false: it was set up to promote small industries.')],
    tf=('problems of small business and government assistance', [
        'Small units often depend on middlemen for marketing.',
        'NSIC supplies machines to small units on hire-purchase.',
        'DICs provide support to small entrepreneurs at the district level.'], [
        'Small units get the cheapest raw materials in the market.',
        'NABARD finances only large urban industries.',
        'Small units never face competition from large firms.',
        'DICs work only at the national level.']),
    cases=[('C4', 'D4', 4, '{p} runs a small {g} unit near {c}. {He} faces three problems: no bank will lend to {him}, {his} machines are old, and {he} sells only through middlemen.',
            [('Name the three problems.', 'Finance, technology and marketing.'),
             ('Suggest an institution for each.', 'Finance: SIDBI or DIC help with bank credit; technology: NSIC technology support or hire-purchase of machines; marketing: NSIC marketing support.')]),
           ('C4', 'D5', 6, 'A group of young people in a backward district wants to start small units but does not know what to make, how to get loans or how to sell.',
            [('Which institution should they approach first and why?', 'The DIC: it identifies entrepreneurs, prepares feasibility reports, arranges credit and marketing at the district level.'),
             ('Name two other institutions that could help, with one function each.', 'NSIC: machines on hire-purchase, marketing; NABARD: rural credit; SIDBI: finance for small industry (any two).')])],
)

IPR = ['Copyright', 'Trademark', 'Patent', 'Geographical indication', 'Design', 'Plant variety']
CH08_ST4 = dict(
    cat='type of intellectual property',
    terms=[
        ('Intellectual property', 'Creations of the human mind, such as inventions, literary and artistic works, designs, symbols and names used in commerce.'),
        ('Intellectual property rights', 'Legal rights given to the creators of intellectual property to protect their creations from use by others without permission.'),
        ('Patent', 'An exclusive right granted for an invention, which in India lasts for twenty years.'),
        ('Copyright', 'The right given to creators of literary, dramatic, musical and artistic works and producers of films and sound recordings.'),
        ('Trademark', 'A word, name, symbol or design that distinguishes the goods or services of one enterprise from those of others.'),
        ('Geographical indication', 'An indication used on products that come from a particular place and have qualities or a reputation due to that origin.'),
        ('Design', 'The features of shape, pattern or ornament applied to an article, which appeal to the eye.'),
        ('Plant variety', 'A new variety of plant developed by a breeder, protected so that the breeder has rights over it.'),
    ],
    lists=[
        ('types', 'types of intellectual property recognised in India', [
            ('Copyright', 'Protects literary, artistic, musical works, films and software.'),
            ('Trademark', 'Protects brand names, logos and symbols.'),
            ('Geographical indication', 'Protects products linked to a place, such as Darjeeling tea.'),
            ('Patent', 'Protects inventions.'),
            ('Design', 'Protects the look of an article.'),
            ('Plant variety', 'Protects new plant varieties.'),
            ('Semiconductor integrated circuit layout design', 'Protects layout designs of chips.')], None),
        ('need', 'reasons why IPR matters to entrepreneurs', [
            ('Rewards creativity', 'Creators can earn from their work.'),
            ('Prevents copying', 'Others cannot use the creation without permission.'),
            ('Builds brand value', 'Protected trademarks build goodwill.'),
            ('Encourages investment in research', 'Firms are willing to spend on innovation.')], None),
    ],
    scen=[('Which type of intellectual property right protects it?', IPR, [
        ('{p} wrote a novel and wants no one to print it without {his} permission.', 'Copyright', 'Literary works are protected by copyright.'),
        ('{f} registers the name and logo under which it sells its {g}.', 'Trademark', 'Brand names and logos are trademarks.'),
        ('{p} invented a new type of water pump and wants exclusive rights to make it.', 'Patent', 'Inventions are protected by patents.'),
        ('Only tea grown in a particular hill region may be sold as Darjeeling tea.', 'Geographical indication', 'A product linked to its place of origin.'),
        ('{f} wants to protect the unique shape of its new perfume bottle.', 'Design', 'The look and shape of an article is a design.'),
        ('A scientist develops a new drought-resistant variety of rice.', 'Plant variety', 'New plant varieties have their own protection.'),
        ('A software firm in {c} wants to stop others from copying its computer program.', 'Copyright', 'Software is protected as a literary work by copyright.'),
        ('Silk sarees woven in Kanchipuram carry a registered label linked to their place of origin.', 'Geographical indication', 'Kanchipuram silk is a GI.')], None)],
    ars=[
        ('A patent gives exclusive rights to an invention.', 'Patents encourage investment in research.', 'b', 'Both true, but R gives a benefit of patents, not the meaning in A.'),
        ('Darjeeling tea is protected as a geographical indication.', 'Its qualities are linked to the region where it is grown.', 'a', 'Both true and R explains A.'),
        ('A trademark protects an invention.', 'A trademark distinguishes the goods of one firm from others.', 'd', 'A is false: a patent protects an invention. R is true.'),
        ('Copyright protects literary and artistic works.', 'Copyright protects new plant varieties.', 'c', 'A is true; R is false.')],
    tf=('intellectual property rights', [
        'A patent in India lasts for twenty years.',
        'A trademark distinguishes the goods of one enterprise from others.',
        'Copyright protects literary and artistic works.'], [
        'A geographical indication protects inventions.',
        'Copyright protects brand logos only.',
        'Intellectual property cannot be protected by law.',
        'A patent protects the name of a product.']),
    cases=[('C4', 'D4', 4, '{p} has started {f}, which sells herbal skin-care products under a new brand name. {He} has also invented a new extraction machine and written a recipe book.',
            [('Name the IPR that protects each: the brand name, the machine and the book.', 'Brand name: trademark; machine: patent; book: copyright.'),
             ('Why are these rights important to {him}?', 'They prevent copying, reward creativity, build brand value and encourage further research.')])],
)

# ---------------- ch09 Internal Trade

RET = ['Peddlers and hawkers', 'Market traders', 'Street traders', 'Cheap jacks', 'General stores', 'Speciality shops', 'Second-hand goods shops', 'Single line stores']
FEAT_RET = {
    'Peddlers and hawkers': ['carry goods on bicycles, carts or heads', 'move from place to place', 'small investment', 'deal in goods of daily use'],
    'Market traders': ['open shops at different places on fixed days', 'sell in weekly markets', 'deal in goods of daily use or a variety of goods'],
    'Street traders': ['found at places of heavy footfall such as railway stations and bus stands', 'sell items of common use', 'no permanent shop'],
    'Cheap jacks': ['have independent shops of a temporary nature', 'change locality depending on business', 'deal in consumer items and repair services'],
    'General stores': ['found in residential areas', 'sell a variety of goods of daily use', 'often give credit to regular customers'],
    'Speciality shops': ['sell one type of product', 'for example, children\'s garments or men\'s wear', 'usually in central locations'],
    'Second-hand goods shops': ['deal in used goods', 'prices are low', 'sell items such as furniture, books and clothes'],
    'Single line stores': ['sell a single line of products with variety', 'for example, garments or footwear', 'located in central places'],
}
CH09_ST1 = dict(
    cat='trade term',
    terms=[
        ('Internal trade', 'Buying and selling of goods and services within the boundaries of a nation.'),
        ('Wholesale trade', 'Buying and selling of goods in large quantities, for resale or for intermediate use.'),
        ('Retail trade', 'Buying and selling of goods in small quantities to the ultimate consumers.'),
        ('Wholesaler', 'A trader who buys goods in bulk from manufacturers and sells them in smaller lots to retailers and industrial users.'),
        ('Retailer', 'A trader who buys goods from wholesalers or manufacturers and sells them to the ultimate consumers.'),
    ],
    lists=[
        ('wm', 'services of wholesalers to manufacturers', [
            ('Facilitating large-scale production', 'Wholesalers place bulk orders, so manufacturers can produce on a large scale.'),
            ('Bearing risk', 'They take delivery in their own name and bear the risk of fall in price, theft and spoilage.'),
            ('Financial assistance', 'They pay manufacturers in cash and sometimes give advances.'),
            ('Expert advice', 'They pass on information about customer tastes and market conditions.'),
            ('Help in marketing function', 'They distribute goods to many retailers.'),
            ('Facilitate continuity', 'Goods are bought as they are produced, keeping production going.'),
            ('Storage', 'They store goods, so manufacturers need less warehousing.')], 'wr'),
        ('wr', 'services of wholesalers to retailers', [
            ('Availability of goods', 'Retailers get a variety of goods from different producers in one place.'),
            ('Marketing support', 'Wholesalers advertise and promote sales.'),
            ('Grant of credit', 'They give goods on credit.'),
            ('Specialised knowledge', 'They advise retailers on new products and demand.'),
            ('Risk sharing', 'Retailers buy in small lots and avoid the risk of large stocks.')], 'wm'),
        ('rm', 'services of retailers to manufacturers and wholesalers', [
            ('Help in distribution of goods', 'Retailers make goods available to scattered consumers.'),
            ('Personal selling', 'They sell goods face to face with customers.'),
            ('Enabling large-scale operations', 'Producers and wholesalers are freed from selling to consumers.'),
            ('Collecting market information', 'They pass on consumer preferences.'),
            ('Help in promotion', 'They display goods and distribute promotional material.')], 'rc'),
        ('rc', 'services of retailers to consumers', [
            ('Regular availability of products', 'Goods are available when needed.'),
            ('New products information', 'Retailers tell consumers about new products.'),
            ('Convenience in buying', 'Shops are near residential areas and open long hours.'),
            ('Wide selection', 'Goods of many brands are stocked.'),
            ('After-sales services', 'Home delivery, spare parts and attention to customers.'),
            ('Provide credit facilities', 'Regular customers may buy on credit.')], 'rm'),
    ],
    pairs=[('wholesale trade', 'retail trade', [
        ('quantity', 'large quantities', 'small quantities'),
        ('sold to', 'retailers and industrial users', 'ultimate consumers'),
        ('capital required', 'large capital', 'small capital'),
        ('variety', 'deals in a few lines of products', 'deals in a variety of products'),
        ('price', 'lower, wholesale prices', 'higher, retail prices'),
        ('credit', 'gives credit to retailers', 'may give credit to some regular customers')])],
    scen=[('Which service of a wholesaler or retailer is illustrated?', ['Bearing risk', 'Financial assistance', 'Grant of credit', 'Storage', 'After-sales services', 'Collecting market information'], [
        ('A wholesaler buys {g} from {f} in its own name and bears the loss when prices fall.', 'Bearing risk', 'Wholesalers take delivery in their own name and bear risk.'),
        ('A wholesaler pays {f} in cash at once and sometimes gives it advances.', 'Financial assistance', 'Wholesalers finance manufacturers.'),
        ('A wholesaler allows retailers in {c} to pay for goods after 30 days.', 'Grant of credit', 'Wholesalers give credit to retailers.'),
        ('A wholesaler keeps stocks of {g} in its godown so that {f} need not build one.', 'Storage', 'Wholesalers store goods for manufacturers.'),
        ('A retailer in {c} delivers a refrigerator home and arranges repairs during the warranty.', 'After-sales services', 'Retailers provide after-sales services.'),
        ('A retailer tells the wholesaler that customers now prefer smaller packs of {g}.', 'Collecting market information', 'Retailers pass on consumer preferences.')], None)],
    ars=[
        ('Wholesalers help manufacturers produce on a large scale.', 'Wholesalers buy goods in large quantities.', 'a', 'Both true and R explains A.'),
        ('Retailers provide after-sales services to consumers.', 'Retailers are in direct contact with consumers.', 'a', 'Both true and R explains A.'),
        ('Customs duty is levied on internal trade.', 'Internal trade takes place within the boundaries of a country.', 'd', 'A is false: no customs duty is levied on internal trade. R is true.'),
        ('Wholesalers give credit to retailers.', 'Wholesalers sell goods directly to ultimate consumers.', 'c', 'A is true; R is false: wholesalers sell to retailers.')],
    tf=('internal trade', [
        'Internal trade takes place within the boundaries of a country.',
        'No customs duty is levied on internal trade.',
        'Wholesalers bear the risk of storing goods.',
        'Retailers are the final link between producers and consumers.'], [
        'Wholesalers sell only to ultimate consumers.',
        'Retailers buy goods in very large quantities.',
        'Wholesalers give no credit to retailers.',
        'Payment in internal trade is made in foreign currency.']),
    cases=[('C4', 'D4', 4, '{f} makes {g} in {c}. It wants to sell all over the state but does not want to deal with thousands of small shops or build warehouses.',
            [('Which middleman should it use and why?', 'Wholesalers: they buy in bulk, distribute to many retailers and store goods.'),
             ('State two more services this middleman gives to {f}.', 'Bearing risk, financial assistance, expert advice, facilitating continuity (any two).')]),
           ('C4', 'D5', 6, '{p} argues that retailers only add to prices and consumers would be better off buying directly from factories.',
            [('Do you agree? Give three services retailers give consumers.', 'No. Regular availability, convenience in buying, wide selection, new product information, after-sales service, credit (any three).'),
             ('Give two services retailers give manufacturers.', 'Distribution, personal selling, collecting market information, help in promotion (any two).')])],
)

CH09_ST2 = dict(
    cat='type of retailer',
    terms=[
        ('Itinerant retailers', 'Traders who do not have a fixed place of business and move from place to place to sell their goods.'),
        ('Peddlers and hawkers', 'Small producers or traders who carry goods on bicycles, hand carts or heads and sell from door to door.'),
        ('Market traders', 'Small retailers who open shops at different places on fixed days or dates, such as weekly markets.'),
        ('Street traders', 'Small retailers found at places of heavy footfall, such as railway stations and bus stands, selling items of common use.'),
        ('Cheap jacks', 'Petty retailers with independent shops of a temporary nature who change their locality depending on business.'),
        ('Fixed shop retailers', 'Retailers who maintain permanent establishments to sell their goods.'),
        ('Speciality shop', 'A fixed shop that sells a particular type of product, such as children\'s garments.'),
    ],
    lists=[
        ('itin', 'features of itinerant retailers', [
            ('Small traders with limited resources', 'They work on a small scale.'),
            ('Deal in consumer goods of daily use', 'Such as fruits, vegetables, toys and household items.'),
            ('Greater emphasis on customer services', 'Goods are offered at the customer\'s doorstep.'),
            ('No permanent place of business', 'They keep moving from place to place.')], 'fixed'),
        ('fixed', 'features of fixed shop retailers', [
            ('Permanent establishment', 'They sell from a fixed place.'),
            ('Greater resources', 'They operate on a larger scale than itinerant traders.'),
            ('Deal in durable as well as non-durable goods', 'They stock a wider range.'),
            ('Greater credibility', 'Customers know where to find them.')], 'itin'),
    ],
    pairs=[('itinerant retailers', 'fixed shop retailers', [
        ('place of business', 'no fixed place; move from place to place', 'permanent establishment'),
        ('resources', 'limited resources', 'greater resources'),
        ('goods', 'mainly goods of daily use', 'durable and non-durable goods'),
        ('credibility', 'low; customers may not find them again', 'high; customers know the shop')])],
    scen=[('Which type of retailer is it?', RET, [
        ('{p} sells vegetables from a hand cart, going from street to street in {c}.', 'Peddlers and hawkers', 'Moves door to door with a cart.'),
        ('{p} sets up a stall at a different village market each day of the week.', 'Market traders', 'Shops at different places on fixed days.'),
        ('{p} sells newspapers and snacks outside the bus stand in {c}.', 'Street traders', 'Found at places of heavy footfall.'),
        ('{p} runs a temporary shop repairing watches and moves to another locality when business falls.', 'Cheap jacks', 'Temporary shops that change locality.'),
        ('A shop in a residential colony of {c} sells groceries, toiletries and stationery and gives credit to regular customers.', 'General stores', 'Variety of daily-use goods in a residential area.'),
        ('A shop sells only children\'s garments.', 'Speciality shops', 'Sells one particular type of product.'),
        ('A shop in {c} sells used furniture and old books at low prices.', 'Second-hand goods shops', 'Deals in used goods.'),
        ('A shop sells only footwear, but in many styles and sizes.', 'Single line stores', 'A single line of products with variety.')], 'ret')],
    feat={'ret': FEAT_RET},
    ars=[
        ('Itinerant retailers do not have a fixed place of business.', 'They move from place to place to sell goods.', 'a', 'Both true and R explains A.'),
        ('Cheap jacks change their locality depending on business.', 'Their shops are of a temporary nature.', 'a', 'Both true and R explains A.'),
        ('Speciality shops sell a wide variety of unrelated products.', 'Speciality shops are fixed shop retailers.', 'd', 'A is false: they sell one type of product. R is true.'),
        ('Street traders are found at places of heavy footfall.', 'Street traders always own large showrooms.', 'c', 'A is true; R is false.')],
    tf=('itinerant and fixed shop retailers', [
        'Peddlers and hawkers carry goods from door to door.',
        'Market traders open shops at different places on fixed days.',
        'General stores are usually found in residential areas.'], [
        'Itinerant retailers have permanent shops.',
        'Cheap jacks never change their locality.',
        'Speciality shops sell goods of every kind.',
        'Street traders sell only luxury goods.']),
    cases=[('C4', 'D4', 4, '{p} sells toys from a cart near schools in {c}. {p2} runs a shop in the same street that sells only children\'s clothes.',
            [('Identify the type of retailer in each case.', '{p}: itinerant retailer (hawker); {p2}: fixed shop retailer (speciality shop).'),
             ('Give two differences between them.', 'Fixed place vs moving; greater vs limited resources; higher vs lower credibility (any two).')])],
)

LSR = ['Departmental store', 'Chain store', 'Shopping mall', 'Supermarket']
FEAT_LSR = {
    'Departmental store': ['wide variety of products under one roof', 'goods arranged in separate departments', 'centralised purchasing', 'located at a central place', 'many services such as restaurants and rest rooms'],
    'Chain store': ['network of retail shops with similar appearance', 'owned and operated by one manufacturer or intermediary', 'standardised and branded products', 'uniform prices and cash sales', 'centralised purchasing at head office'],
    'Shopping mall': ['large building housing many independent shops', 'food courts and entertainment', 'shopping and leisure in one place'],
    'Supermarket': ['large retail store selling a wide range of consumer goods', 'self-service', 'low prices due to bulk buying', 'cash and carry'],
}
CH09_ST3 = dict(
    cat='large-scale retailer',
    terms=[
        ('Departmental store', 'A large establishment offering a wide variety of products, classified into well-defined departments, that aims at satisfying practically every need of the customer under one roof.'),
        ('Chain store', 'A network of retail shops owned and operated by a manufacturer or intermediary, with similar appearance and dealing in standardised products (multiple shops).'),
        ('Shopping mall', 'A large building or group of buildings that houses many independent retail stores along with food courts and entertainment.'),
        ('Supermarket', 'A large retail store selling mainly food and household goods on a self-service basis at low prices.'),
    ],
    lists=[
        ('dsf', 'features of departmental stores', [
            ('Large establishment under one management', 'One organisation runs many departments.'),
            ('Located at a central place', 'They attract customers from a wide area.'),
            ('Wide variety of products', 'From pins to furniture, organised in departments.'),
            ('Combine retailing with warehousing', 'They buy directly from manufacturers and store goods.'),
            ('Centralised purchasing', 'Purchases for all departments are made centrally.'),
            ('Many customer services', 'Restaurants, rest rooms, travel and telephone booths.')], 'csf'),
        ('csf', 'features of chain stores', [
            ('Located in fairly populous localities', 'Shops are opened where many customers can be reached.'),
            ('Centralised manufacturing or procurement', 'Goods are bought or made at the head office.'),
            ('Each shop under a branch manager', 'Branch managers report daily to the head office.'),
            ('Controlled by the head office', 'Policies are formulated centrally.'),
            ('Uniform prices and cash sales', 'Goods are sold at fixed prices, for cash.'),
            ('Inspectors visit shops', 'They check that the shops follow instructions.')], 'dsf'),
        ('dsm', 'merits of departmental stores', [
            ('Attracts large number of customers', 'Central location draws many people.'),
            ('Convenience in buying', 'Everything is available under one roof.'),
            ('Attractive services', 'Many facilities for customers.'),
            ('Economy of large-scale operations', 'Bulk buying reduces cost.'),
            ('Promotion of sales', 'Large budgets for advertising.')], 'dsl'),
        ('dsl', 'limitations of departmental stores', [
            ('Lack of personal attention', 'Large size means less personal contact.'),
            ('High operating cost', 'More services mean higher costs and prices.'),
            ('High possibility of loss', 'Heavy overheads can lead to losses.'),
            ('Inconvenient location', 'A central location may be far from many homes.')], 'dsm'),
    ],
    pairs=[('departmental store', 'chain store', [
        ('location', 'a central place', 'many localities, close to customers'),
        ('range of products', 'wide variety of products', 'limited range of standardised products'),
        ('services offered', 'maximum services', 'limited services'),
        ('pricing', 'prices may differ between departments and may include discounts', 'uniform prices in all shops'),
        ('class of customers', 'mainly higher-income customers', 'customers of different income groups'),
        ('credit facilities', 'may be given to regular customers', 'sales are strictly for cash')])],
    scen=[('Which type of large-scale retailer is it?', LSR, [
        ('A large store in central {c} sells clothes, furniture, cosmetics and groceries in separate sections under one management, with a restaurant inside.', 'Departmental store', 'Wide variety in departments under one roof.'),
        ('{f} has 200 shops of the same look across India, all selling its own branded {g} at the same price.', 'Chain store', 'Network of similar shops with uniform prices.'),
        ('A large building in {c} houses a cinema, a food court and 150 independent shops.', 'Shopping mall', 'Many independent stores with entertainment.'),
        ('Customers pick groceries off shelves themselves and pay at the checkout counter, at low prices.', 'Supermarket', 'Self-service at low prices.'),
        ('A head office buys all goods centrally and branch managers report sales to it daily.', 'Chain store', 'Central control of branch shops.'),
        ('A store buys directly from manufacturers for all its departments through one central purchasing office.', 'Departmental store', 'Centralised purchasing for many departments.')], 'lsr')],
    feat={'lsr': FEAT_LSR},
    ars=[
        ('Departmental stores offer a wide variety of products under one roof.', 'Their products are arranged in well-defined departments.', 'a', 'Both true and R explains A.'),
        ('Chain stores sell at uniform prices.', 'All shops of a chain are controlled by a head office.', 'a', 'Both true and R explains A.'),
        ('Chain stores give liberal credit to customers.', 'Chain stores deal in standardised products.', 'd', 'A is false: sales are for cash. R is true.'),
        ('Departmental stores have high operating costs.', 'Departmental stores are located in remote villages.', 'c', 'A is true; R is false: they are centrally located.')],
    tf=('large-scale retailers', [
        'A departmental store offers a wide variety of products under one roof.',
        'Chain stores have uniform prices in all their shops.',
        'Purchasing in a departmental store is centralised.'], [
        'Chain stores are located only in remote areas.',
        'Departmental stores have low operating costs.',
        'Chain stores sell a very wide variety of unrelated goods.',
        'All sales in departmental stores must be on credit.']),
    cases=[('C4', 'D4', 4, '{f} sells its own branded {g}. It wants to reach customers across many towns, with the same look and prices everywhere and tight central control.',
            [('Which form of large-scale retailing suits it?', 'Chain stores (multiple shops).'),
             ('State two features that make it suitable.', 'Uniform prices, standardised products, centralised procurement, control by head office (any two).')]),
           ('C4', 'D5', 6, '{p} plans a large store in the centre of {c} where customers can buy everything from clothes to furniture, with restaurants and parking.',
            [('Identify the type of store.', 'Departmental store.'),
             ('Give two merits and two limitations.', 'Merits: convenience under one roof, attractive services, economies of bulk buying. Limitations: high operating cost, lack of personal attention, inconvenient location.'),
             ('How does it differ from a chain store in location and pricing?', 'Central location vs many localities; prices may vary vs uniform prices.')])],
)

GST = ['CGST', 'SGST', 'IGST', 'Not covered by GST']
CH09_ST4 = dict(
    cat='GST or trade term',
    terms=[
        ('GST', 'A destination-based tax on the supply of goods and services, introduced in India from 1 July 2017 (goods and services tax).'),
        ('CGST', 'The part of GST levied by the central government on intra-state supplies.'),
        ('SGST', 'The part of GST levied by the state government on intra-state supplies.'),
        ('IGST', 'GST levied by the central government on inter-state supplies and imports.'),
        ('Input tax credit', 'Credit for the tax paid on purchases that can be set off against the tax payable on sales.'),
        ('GST Council', 'The body of the Union Finance Minister and state finance ministers that recommends GST rates and rules.'),
        ('Chambers of commerce and industry', 'Associations of business firms that promote and protect the interests of their members and of trade and industry.'),
    ],
    lists=[
        ('ben', 'benefits of GST', [
            ('Removes the cascading effect of taxes', 'Input tax credit means tax is not charged on tax.'),
            ('One nation, one tax', 'Many indirect taxes are replaced by one tax.'),
            ('Common national market', 'Uniform tax makes inter-state trade easier.'),
            ('Online compliance', 'Registration, returns and payment are online.'),
            ('Simpler scheme for small businesses', 'A composition scheme reduces compliance for small taxpayers.')], None),
        ('chamb', 'roles of chambers of commerce and industry in promoting internal trade', [
            ('Transportation and inter-state movement', 'They help with movement of goods across states.'),
            ('Collection of local levies', 'They take up issues about local taxes with authorities.'),
            ('Harmonisation of taxes', 'They press for a uniform tax structure across states.'),
            ('Marketing of agro products', 'They help farmers and agro firms market their produce.'),
            ('Weights and measures and prevention of duplicate brands', 'They push for enforcement of laws to protect consumers and brands.'),
            ('Promoting sale of products', 'They organise fairs and exhibitions.'),
            ('Infrastructure development', 'They ask the government to develop roads, ports and power.'),
            ('Labour legislation', 'They negotiate with the government on labour laws.')], None),
    ],
    scen=[('Which tax under GST applies?', GST, [
        ('{f} in Maharashtra sells {g} to a customer in Gujarat.', 'IGST', 'Inter-state supply attracts IGST.'),
        ('{f} in {c} sells {g} to a buyer in the same state. Which part of GST on this sale goes to the central government?', 'CGST', 'Intra-state supply: the central share is CGST.'),
        ('{f} in {c} sells {g} to a buyer in the same state. Which part of GST on this sale goes to the state government?', 'SGST', 'Intra-state supply: the state share is SGST.'),
        ('{f} imports machinery from Germany into India.', 'IGST', 'Imports attract IGST.')], None),
        ('Which role of chambers of commerce is illustrated?', ['Promoting sale of products', 'Infrastructure development', 'Labour legislation', 'Marketing of agro products', 'Harmonisation of taxes'], [
        ('A chamber of commerce in {c} organises a trade fair for local manufacturers of {g}.', 'Promoting sale of products', 'Fairs and exhibitions promote sales.'),
        ('A chamber asks the state to build better roads and power supply to the industrial area near {c}.', 'Infrastructure development', 'Pressing for roads and power.'),
        ('A chamber negotiates with the government about changes to working hours under labour laws.', 'Labour legislation', 'Dealing with labour laws.'),
        ('A chamber helps fruit growers near {c} find buyers in other states.', 'Marketing of agro products', 'Helping farmers market produce.'),
        ('Before GST, chambers pressed for a uniform tax structure across states.', 'Harmonisation of taxes', 'Pressing for uniform taxes.')], None)],
    ars=[
        ('GST removes the cascading effect of taxes.', 'Input tax credit allows tax paid on purchases to be set off.', 'a', 'Both true and R explains A.'),
        ('IGST applies to inter-state supplies.', 'IGST is levied by the central government.', 'b', 'Both true, but R does not explain why it applies to inter-state supplies.'),
        ('GST is an origin-based tax.', 'GST is levied on the supply of goods and services.', 'd', 'A is false: GST is destination-based. R is true.'),
        ('Chambers of commerce promote internal trade.', 'Chambers of commerce are government departments.', 'c', 'A is true; R is false: they are associations of businesses.')],
    tf=('GST and chambers of commerce', [
        'GST was introduced in India from 1 July 2017.',
        'IGST is levied on inter-state supplies.',
        'Input tax credit removes the cascading effect of taxes.',
        'FICCI, CII and ASSOCHAM are national chambers of commerce and industry.'], [
        'GST is collected only by state governments.',
        'CGST is levied on imports only.',
        'Chambers of commerce are government departments.',
        'GST increased the number of indirect taxes.']),
    cases=[('C4', 'D4', 4, '{f}, a {g} manufacturer in {c}, sells both within its state and to other states.',
            [('Which taxes apply to each kind of sale?', 'Within the state: CGST and SGST; to other states: IGST.'),
             ('How does input tax credit help {f}?', 'Tax paid on its purchases can be set off against tax on its sales, avoiding tax on tax.')]),
           ('C4', 'D5', 6, 'Small traders of {c} face problems with poor roads, frequent changes in local levies and lack of buyers outside the state.',
            [('Which body could take up their problems?', 'A chamber of commerce and industry.'),
             ('Explain three roles it could play.', 'Infrastructure development, issues of local levies and tax harmonisation, promoting sales through fairs; also inter-state transport.')])],
)

# ---------------- ch10 International Business

MODE = ['Exporting', 'Contract manufacturing', 'Licensing', 'Franchising', 'Joint venture', 'Wholly owned subsidiary']
FEAT_MODE = {
    'Exporting': ['easiest way to enter foreign markets', 'needs less investment', 'less risk to foreign investment', 'freight and tariffs raise cost'],
    'Contract manufacturing': ['foreign firm makes goods to the specifications of the international firm', 'no investment in plant', 'local producer gets assured business', 'quality may not be maintained'],
    'Licensing': ['licensor allows use of patents, trademarks or technology for a fee (royalty)', 'little investment and risk', 'licensee may become a competitor', 'trade secrets may leak'],
    'Franchising': ['used for services', 'franchisor provides brand and business system', 'franchisee pays a fee', 'strict standards are followed'],
    'Joint venture': ['jointly owned by two or more firms', 'shared investment and risk', 'access to local partner\'s knowledge', 'conflicts between partners possible'],
    'Wholly owned subsidiary': ['parent company owns 100% equity', 'full control over operations', 'high investment and risk', 'not suited to small firms'],
}
CH10_ST1 = dict(
    cat='international business term',
    terms=[
        ('International business', 'Manufacturing and trade activities that cross national frontiers.'),
        ('Licensing', 'A contract in which a firm permits a foreign firm to use its patents, trademarks or technology in return for a fee called royalty.'),
        ('Franchising', 'A form of licensing used mainly for services, in which the franchisor allows the franchisee to use its brand and business system for a fee.'),
        ('Contract manufacturing', 'An arrangement in which a firm gets its products made by local manufacturers in a foreign country to its specifications.'),
        ('Joint venture', 'A firm jointly owned by two or more independent firms.'),
        ('Wholly owned subsidiary', 'A company in a foreign country in which the parent company holds 100 per cent of the equity.'),
        ('Entrepot trade', 'Importing goods for the purpose of re-exporting them, also called re-export.'),
    ],
    lists=[
        ('scope', 'components of the scope of international business', [
            ('Merchandise exports and imports', 'Trade in tangible goods.'),
            ('Service exports and imports', 'Trade in services such as tourism, transport and banking.'),
            ('Licensing and franchising', 'Allowing foreign firms to use patents, brands and systems for a fee.'),
            ('Foreign investments', 'Direct and portfolio investment in other countries.')], None),
        ('bn', 'benefits of international business to nations', [
            ('Earning of foreign exchange', 'Exports earn foreign exchange for imports.'),
            ('More efficient use of resources', 'Countries produce what they are best at.'),
            ('Improving growth prospects and employment', 'Larger markets create jobs.'),
            ('Increased standard of living', 'People get goods not made at home.')], 'bf'),
        ('bf', 'benefits of international business to firms', [
            ('Prospects for higher profits', 'Prices abroad may be higher.'),
            ('Increased capacity utilisation', 'Surplus capacity is used for export.'),
            ('Prospects for growth', 'Foreign markets offer growth when home demand slows.'),
            ('Way out of intense competition in the domestic market', 'Firms can find new markets.'),
            ('Improved business vision', 'Firms become more global in their thinking.')], 'bn'),
    ],
    pairs=[('domestic business', 'international business', [
        ('nationality of buyers and sellers', 'same country', 'different countries'),
        ('mobility of factors of production', 'relatively free', 'restricted between countries'),
        ('customer heterogeneity', 'more homogeneous customers', 'customers differ in language, tastes and habits'),
        ('business systems and practices', 'similar within the country', 'differ between countries'),
        ('political system and risks', 'familiar to the businessman', 'different and less predictable'),
        ('currency used', 'one currency', 'more than one currency')])],
    scen=[('Which mode of entry into international business is used?', MODE, [
        ('{f} of {c} sells its {g} directly to buyers in Germany.', 'Exporting', 'Selling goods abroad directly is exporting.'),
        ('A US firm gets local factories in Bangladesh to make shirts to its designs under its brand.', 'Contract manufacturing', 'Local producers make goods to the firm\'s specifications.'),
        ('{f} allows a firm in Kenya to use its patented process in return for a royalty.', 'Licensing', 'Permission to use a patent for a fee.'),
        ('A fast-food chain lets an Indian firm run outlets under its brand and system for a fee.', 'Franchising', 'Licensing of a service brand and system.'),
        ('{f} and a Japanese company set up a new firm in India, each holding 50% of its shares.', 'Joint venture', 'Jointly owned by two firms.'),
        ('{f} sets up a company in Singapore and holds all of its shares.', 'Wholly owned subsidiary', '100% equity held by the parent.')], 'mode'),
        ('Which benefit of international business is illustrated?', ['Earning of foreign exchange', 'Increased capacity utilisation', 'Prospects for higher profits', 'Way out of intense competition in the domestic market', 'Increased standard of living'], [
        ('{f} has spare capacity at its plant in {c} and uses it to make goods for export.', 'Increased capacity utilisation', 'Surplus capacity is used for export.'),
        ('Exports by Indian firms earn dollars that pay for oil imports.', 'Earning of foreign exchange', 'Exports bring foreign exchange.'),
        ('{f} finds it can sell its {g} abroad at a higher price than in India.', 'Prospects for higher profits', 'Higher prices abroad mean higher profits.'),
        ('Facing a price war at home, {f} turns to markets in Africa.', 'Way out of intense competition in the domestic market', 'Foreign markets reduce dependence on a crowded home market.')], None)],
    feat={'mode': FEAT_MODE},
    ars=[
        ('International business is more complex than domestic business.', 'Buyers and sellers in international business belong to different countries with different laws and currencies.', 'a', 'Both true and R explains A.'),
        ('Exporting is the easiest way to enter international business.', 'Exporting needs less investment than other modes.', 'a', 'Both true and R explains A.'),
        ('A wholly owned subsidiary involves low investment and risk.', 'The parent company holds all the equity of a wholly owned subsidiary.', 'd', 'A is false: investment and risk are high. R is true.'),
        ('Licensing involves little investment.', 'The licensee can never become a competitor.', 'c', 'A is true; R is false: the licensee may become a competitor.')],
    tf=('international business', [
        'International business includes trade in services.',
        'Licensing gives the licensor a royalty.',
        'A joint venture is jointly owned by two or more firms.',
        'Mobility of factors of production is restricted between countries.'], [
        'Franchising is used mainly for manufactured goods only.',
        'International business uses only one currency.',
        'A wholly owned subsidiary needs no investment.',
        'Contract manufacturing means owning factories abroad.']),
    cases=[('C4', 'D4', 4, '{f}, an Indian maker of water purifiers, wants to enter Europe. It has little capital and does not want to risk its money abroad, but has a well-known patented technology.',
            [('Suggest two suitable modes of entry.', 'Licensing its technology; exporting; contract manufacturing (any two).'),
             ('Give one limitation of each.', 'Licensing: licensee may become a competitor or leak secrets. Exporting: freight and tariffs raise cost. Contract manufacturing: quality may not be maintained.')]),
           ('C4', 'D5', 6, '{f} wants full control of its operations in a large foreign market and has ample funds.',
            [('Which mode of entry suits it?', 'Wholly owned subsidiary.'),
             ('Give two merits and two limitations.', 'Merits: full control, no sharing of profits or secrets. Limitations: high investment, full risk, not suited to small firms.'),
             ('How would a joint venture differ?', 'Ownership, investment and risk are shared with a partner, who also brings local knowledge.')])],
)

DOCS = ['Bill of lading', 'Mate\'s receipt', 'Shipping bill', 'Letter of credit', 'Certificate of origin', 'Bill of entry', 'Shipment advice', 'Import general manifest']
CH10_ST2 = dict(
    cat='export-import document',
    terms=[
        ('Bill of lading', 'A document issued by the shipping company acknowledging receipt of goods on board and undertaking to deliver them; it is also a document of title.'),
        ('Mate\'s receipt', 'A receipt issued by the commanding officer of the ship to the shipper after the cargo is loaded on board.'),
        ('Shipping bill', 'The main document on the basis of which customs permits export; it gives details of the goods and the exporter.'),
        ('Letter of credit', 'A guarantee issued by the importer\'s bank that it will honour payment up to a certain amount of export bills.'),
        ('Certificate of origin', 'A certificate that states the country in which the goods are produced.'),
        ('Bill of entry', 'A form filled in by the importer for customs clearance, giving details of the imported goods.'),
        ('Indent', 'An order placed by an importer with an exporter for supply of goods.'),
        ('Proforma invoice', 'A document containing details of quality, grade, price and terms, sent by the exporter in reply to an enquiry.'),
        ('IEC number', 'The Importer Exporter Code issued by the Directorate General of Foreign Trade, needed for exporting or importing.'),
    ],
    lists=[
        ('exp', 'steps in the export procedure', [
            ('Receipt of enquiry and sending quotations', 'The exporter replies with a proforma invoice.'),
            ('Receipt of order or indent', 'The importer places an order.'),
            ('Assessing creditworthiness and securing a guarantee for payment', 'Usually a letter of credit from the importer\'s bank.'),
            ('Obtaining an export licence', 'Including the IEC number and registration with the export promotion council.'),
            ('Obtaining pre-shipment finance', 'From a bank to produce or buy the goods.'),
            ('Production or procurement of goods', 'Goods are made or bought as per the order.'),
            ('Pre-shipment inspection', 'Goods are inspected by an authorised agency where required.'),
            ('Obtaining certificate of origin', 'Needed by the importer for tariff concessions.'),
            ('Reservation of shipping space', 'The exporter applies to the shipping company.'),
            ('Packing and forwarding', 'Goods are packed and sent to the port.'),
            ('Insurance of goods', 'Goods are insured against perils of the sea.'),
            ('Customs clearance', 'A shipping bill is prepared and goods are examined.'),
            ('Obtaining mate\'s receipt and paying freight for the bill of lading', 'The mate\'s receipt is exchanged for the bill of lading.'),
            ('Preparation of invoice and securing payment', 'Documents are sent through the bank to obtain payment.')], None),
        ('imp', 'steps in the import procedure', [
            ('Trade enquiry', 'The importer gathers information about exporters and terms.'),
            ('Procurement of import licence', 'Including the IEC number.'),
            ('Obtaining foreign exchange', 'The importer applies to a bank for foreign exchange.'),
            ('Placing order or indent', 'The importer places an order with the exporter.'),
            ('Obtaining letter of credit', 'The importer arranges it from a bank.'),
            ('Arranging for finance', 'Funds are arranged in advance to pay on arrival.'),
            ('Receipt of shipment advice', 'The exporter informs the importer of shipment.'),
            ('Retirement of import documents', 'The importer pays or accepts the bill to get the documents.'),
            ('Arrival of goods', 'Goods arrive at the port.'),
            ('Customs clearance and release of goods', 'A bill of entry is filed and duty paid.')], None),
    ],
    pairs=[('sight draft', 'usance draft', [
        ('when documents are released', 'on payment of the bill', 'on acceptance of the bill'),
        ('name of arrangement', 'documents against payment (D/P)', 'documents against acceptance (D/A)'),
        ('credit to importer', 'none; payment is immediate', 'credit for the usance period'),
        ('risk to exporter', 'lower', 'higher')])],
    scen=[('Which document is described?', DOCS, [
        ('The ship\'s commanding officer gives the shipper a receipt after the cargo is loaded.', 'Mate\'s receipt', 'Issued by the ship\'s officer after loading.'),
        ('The shipping company issues a document that acknowledges the goods on board and is a document of title.', 'Bill of lading', 'The bill of lading is a document of title.'),
        ('Customs permits {f} to export only after it files this document giving details of the goods.', 'Shipping bill', 'The shipping bill is the main document for customs clearance of exports.'),
        ('The importer\'s bank guarantees that it will pay the exporter\'s bills up to a stated amount.', 'Letter of credit', 'A bank guarantee of payment.'),
        ('A document states that the {g} were produced in India, so the importer can claim a tariff concession.', 'Certificate of origin', 'States the country of production.'),
        ('The importer files this form with customs giving details of the imported goods.', 'Bill of entry', 'Filed by the importer for customs clearance.'),
        ('The exporter sends the importer a letter giving details of the shipment, the ship and the expected date of arrival.', 'Shipment advice', 'Informs the importer of the shipment.'),
        ('The person in charge of the carrier delivers a document to the port listing the imported goods unloaded.', 'Import general manifest', 'Lists goods brought in by the carrier.')], None),
        ('Is it a step in the export procedure or the import procedure?', ['Export procedure', 'Import procedure', 'Both procedures', 'Neither procedure'], [
        ('{f} files a bill of entry and pays customs duty.', 'Import procedure', 'Bill of entry is filed by the importer.'),
        ('{f} obtains a mate\'s receipt and exchanges it for a bill of lading.', 'Export procedure', 'The exporter gets these after loading.'),
        ('{f} receives a shipment advice and retires the documents from its bank.', 'Import procedure', 'The importer receives shipment advice and retires documents.'),
        ('{f} obtains pre-shipment finance from its bank to buy raw materials.', 'Export procedure', 'Pre-shipment finance is for exporters.'),
        ('{f} obtains an IEC number from the DGFT.', 'Both procedures', 'IEC is needed by both exporters and importers.')], None)],
    ars=[
        ('The bill of lading is a document of title to goods.', 'It can be transferred by endorsement to pass ownership.', 'a', 'Both true and R explains A.'),
        ('A letter of credit reduces the exporter\'s risk of non-payment.', 'It is a guarantee of payment by the importer\'s bank.', 'a', 'Both true and R explains A.'),
        ('A bill of entry is filed by the exporter.', 'A bill of entry is used for customs clearance of imported goods.', 'd', 'A is false: the importer files it. R is true.'),
        ('A mate\'s receipt is exchanged for the bill of lading.', 'Mate\'s receipt is issued by the customs department.', 'c', 'A is true; R is false: it is issued by the ship\'s commanding officer.')],
    tf=('export-import documents', [
        'A mate\'s receipt is issued by the commanding officer of the ship.',
        'A shipping bill is needed for customs clearance of exports.',
        'A bill of entry is filed by the importer.',
        'Under a sight draft, documents are released on payment.'], [
        'A bill of lading is issued by the customs office.',
        'A letter of credit is issued by the exporter\'s government.',
        'A certificate of origin states the price of goods.',
        'Under a usance draft, documents are released only on payment.']),
    cases=[('C4', 'D4', 4, '{f} of {c} has received an order for {g} from a buyer in Canada whom it has never dealt with before.',
            [('How can {f} protect itself against non-payment?', 'Ask for a letter of credit from the importer\'s bank.'),
             ('Name the documents it will get after loading the goods.', 'Mate\'s receipt from the ship\'s officer, then the bill of lading from the shipping company after paying freight.')]),
           ('C4', 'D5', 6, '{p}, a new importer in {c}, wants to import machinery from Italy and asks you the steps after the goods are shipped.',
            [('List the steps.', 'Receipt of shipment advice, retirement of import documents, arrival of goods, customs clearance and release of goods.'),
             ('Which document is filed for customs clearance?', 'Bill of entry.'),
             ('What must {he} have before importing at all?', 'An IEC number (import licence) and foreign exchange arranged through a bank.')])],
)

ORG = ['Export Promotion Councils', 'Commodity Boards', 'Export Inspection Council', 'Indian Institute of Foreign Trade', 'Indian Institute of Packaging', 'India Trade Promotion Organisation']
INC = ['Duty drawback scheme', 'Export manufacturing under bond', 'Advance authorisation scheme', 'Export Promotion Capital Goods scheme', 'Special economic zone', 'Export-oriented unit']
CH10_ST3 = dict(
    cat='foreign trade promotion term',
    terms=[
        ('Special economic zone', 'A duty-free enclave treated as foreign territory for trade operations, duties and tariffs, set up to promote exports.'),
        ('Export-oriented unit', 'A unit that undertakes to export its entire production, except permitted sales in the domestic market, in return for incentives.'),
        ('Duty drawback scheme', 'A scheme under which customs and excise duties paid on inputs used in export goods are refunded to the exporter.'),
        ('Advance authorisation scheme', 'A scheme that allows duty-free import of inputs needed to make goods for export.'),
        ('Export Promotion Capital Goods scheme', 'A scheme that allows exporters to import capital goods at concessional or zero duty against an export obligation.'),
        ('Export manufacturing under bond', 'A facility that lets firms manufacture goods for export without paying excise duty, under a bond.'),
    ],
    lists=[
        ('inc', 'incentives and schemes for export promotion', [
            ('Duty drawback scheme', 'Refund of duties paid on inputs used in exports.'),
            ('Export manufacturing under bond', 'Manufacture for export without payment of excise duty.'),
            ('Exemption from payment of indirect taxes on exports', 'Exports are not taxed.'),
            ('Advance authorisation scheme', 'Duty-free import of inputs for export production.'),
            ('Export Promotion Capital Goods scheme', 'Import of capital goods at concessional duty.'),
            ('Special economic zones and export-oriented units', 'Enclaves and units with special incentives for export.')], 'org'),
        ('org', 'organisations set up by the government for export promotion', [
            ('Department of Commerce', 'The apex body responsible for India\'s foreign trade policy.'),
            ('Export Promotion Councils', 'Promote exports of particular products.'),
            ('Commodity Boards', 'Promote production and export of traditional commodities such as tea, coffee and spices.'),
            ('Export Inspection Council', 'Ensures quality control and pre-shipment inspection of exports.'),
            ('Indian Institute of Foreign Trade', 'Trains personnel and does research in international trade.'),
            ('Indian Institute of Packaging', 'Improves packaging standards for exports.'),
            ('India Trade Promotion Organisation', 'Organises trade fairs and exhibitions.')], 'inc'),
    ],
    pairs=[('special economic zone', 'export-oriented unit', [
        ('nature', 'a geographical enclave treated as foreign territory for trade purposes', 'an individual unit that can be set up anywhere in the country'),
        ('scale', 'an area housing many units, with its own infrastructure', 'a single unit'),
        ('export obligation', 'units must earn net foreign exchange', 'unit must export its entire production except permitted domestic sales')])],
    scen=[('Which export promotion scheme or facility is used?', INC, [
        ('{f} gets a refund of the customs duty it paid on imported fabric used to make garments for export.', 'Duty drawback scheme', 'Refund of duty on inputs used in exports.'),
        ('{f} imports raw materials without duty because they will be used to make goods for export.', 'Advance authorisation scheme', 'Duty-free import of inputs for exports.'),
        ('{f} imports new machinery at concessional duty and promises to export goods worth several times its value.', 'Export Promotion Capital Goods scheme', 'Capital goods at concessional duty against export obligation.'),
        ('{f} sets up a unit in an enclave that is treated as foreign territory for duties and tariffs.', 'Special economic zone', 'SEZs are duty-free enclaves.'),
        ('{f} sets up a factory near {c} that undertakes to export its entire output in return for incentives.', 'Export-oriented unit', 'EOUs export their entire production.'),
        ('{f} makes goods for export without paying excise duty, after giving a bond.', 'Export manufacturing under bond', 'Manufacture under bond without duty.')], None),
        ('Which organisation would help?', ORG, [
        ('{f}, a tea exporter, wants help in promoting Indian tea abroad.', 'Commodity Boards', 'The Tea Board is a commodity board.'),
        ('{f} wants its export consignment inspected for quality before shipment.', 'Export Inspection Council', 'Handles quality control and pre-shipment inspection.'),
        ('{p} wants a training course in international trade.', 'Indian Institute of Foreign Trade', 'IIFT trains people in international trade.'),
        ('{f} wants to improve the packaging of its export {g}.', 'Indian Institute of Packaging', 'IIP improves packaging standards.'),
        ('{f} wants to display its products at an international trade fair in New Delhi.', 'India Trade Promotion Organisation', 'ITPO organises trade fairs.'),
        ('Engineering exporters want a body that promotes exports of their particular products.', 'Export Promotion Councils', 'EPCs promote exports of specific products.')], None)],
    ars=[
        ('SEZs help to promote exports.', 'SEZs are treated as foreign territory for trade operations, duties and tariffs.', 'a', 'Both true and R explains A.'),
        ('The duty drawback scheme reduces the cost of exports.', 'Duties paid on inputs used in exports are refunded.', 'a', 'Both true and R explains A.'),
        ('EOUs sell their entire output in the domestic market.', 'EOUs get incentives for exporting.', 'd', 'A is false: they export their entire output except permitted domestic sales. R is true.'),
        ('Commodity Boards promote traditional commodities such as tea and coffee.', 'Commodity Boards conduct pre-shipment inspection of all exports.', 'c', 'A is true; R is false: that is the Export Inspection Council.')],
    tf=('foreign trade promotion', [
        'SEZs are duty-free enclaves.',
        'The duty drawback scheme refunds duties paid on inputs of exported goods.',
        'The Export Inspection Council ensures quality of exports.'], [
        'EOUs are required to sell all their output within India.',
        'Commodity Boards organise all international trade fairs in India.',
        'Exports are subject to heavy indirect taxes in India.',
        'SEZs are treated as domestic tariff areas.']),
    cases=[('C4', 'D4', 4, '{f} of {c} imports raw materials to make goods for export. It also plans to buy new imported machines. Duties make its products costly abroad.',
            [('Suggest two schemes that reduce its duty burden.', 'Advance authorisation (duty-free inputs) or duty drawback (refund); EPCG for machinery.'),
             ('Where could it set up a new plant for more incentives?', 'In a special economic zone, or as an export-oriented unit.')]),
           ('C4', 'D5', 6, 'A new exporter of {g} needs quality certification, better packaging, training for staff and a place to show products to foreign buyers.',
            [('Name an organisation for each need.', 'Export Inspection Council; Indian Institute of Packaging; Indian Institute of Foreign Trade; India Trade Promotion Organisation.'),
             ('Name one more body that would promote exports of its product line.', 'The export promotion council or commodity board for the product.')])],
)

WTOF = ['Most favoured nation treatment', 'National treatment', 'Dispute settlement', 'Trade policy review']
CH10_ST4 = dict(
    cat='WTO term',
    terms=[
        ('WTO', 'The international organisation, set up on 1 January 1995 as successor to GATT, that lays down and administers rules for trade between nations.'),
        ('GATT', 'The General Agreement on Tariffs and Trade, signed in 1947, which governed world trade before the WTO.'),
        ('Most favoured nation treatment', 'The principle that any trade advantage given to one member must be given to all members without discrimination.'),
        ('National treatment', 'The principle that imported goods, once they enter a market, are treated no less favourably than domestic goods.'),
        ('TRIPS', 'The WTO Agreement on Trade-Related Aspects of Intellectual Property Rights.'),
        ('GATS', 'The WTO General Agreement on Trade in Services.'),
    ],
    lists=[
        ('obj', 'objectives of the WTO', [
            ('Raise standards of living', 'Through expansion of trade.'),
            ('Ensure full employment and growth of real income', 'And effective demand in member countries.'),
            ('Expand production and trade of goods and services', 'By reducing trade barriers.'),
            ('Optimal use of world resources', 'In line with sustainable development.'),
            ('Help developing countries share in growth of trade', 'Through positive efforts for less developed countries.')], 'fn'),
        ('fn', 'functions of the WTO', [
            ('Promoting an environment for members to raise trade issues', 'Members negotiate trade matters.'),
            ('Administering trade agreements', 'Implementation and operation of the agreements.'),
            ('Settling trade disputes', 'Through its dispute settlement mechanism.'),
            ('Reviewing trade policies', 'Through the trade policy review mechanism.'),
            ('Cooperating with the IMF and the World Bank', 'For coherence in global economic policy.')], 'obj'),
        ('ben', 'benefits of WTO membership', [
            ('Reduction of trade barriers', 'Tariffs and quotas are lowered.'),
            ('Dispute settlement', 'Trade disputes are settled by rules.'),
            ('Non-discrimination', 'Most favoured nation and national treatment.'),
            ('Access to larger markets', 'Exporters reach more countries.')], None),
    ],
    pairs=[('GATT', 'WTO', [
        ('legal status', 'a set of rules or agreement, not an organisation', 'a permanent organisation with legal status'),
        ('scope', 'mainly trade in goods', 'goods, services and intellectual property'),
        ('dispute settlement', 'slow and weak', 'faster and binding'),
        ('year', 'signed in 1947', 'set up in 1995')])],
    scen=[('Which WTO principle or function is illustrated?', WTOF, [
        ('India lowers its import duty on a product from one WTO member and must lower it for all members.', 'Most favoured nation treatment', 'Advantages given to one member must be given to all.'),
        ('Once imported cars enter a country, they must face the same local taxes as domestic cars.', 'National treatment', 'Imports are treated like domestic goods after entry.'),
        ('Two member countries take their quarrel over steel duties to a WTO panel for a ruling.', 'Dispute settlement', 'The WTO settles trade disputes.'),
        ('The WTO examines a member\'s trade policies at regular intervals and publishes a report.', 'Trade policy review', 'Trade policy review mechanism.')], None)],
    ars=[
        ('The WTO replaced GATT.', 'The WTO was set up on 1 January 1995 as a permanent organisation.', 'a', 'Both true and R explains A.'),
        ('The WTO helps settle trade disputes between members.', 'It has a dispute settlement mechanism.', 'a', 'Both true and R explains A.'),
        ('India is not a member of the WTO.', 'The WTO has its headquarters at Geneva.', 'd', 'A is false: India is a founder member. R is true.'),
        ('The WTO covers trade in services.', 'GATT covered only trade in services.', 'c', 'A is true; R is false: GATT mainly covered goods.')],
    tf=('the WTO', [
        'The WTO was set up on 1 January 1995.',
        'The WTO headquarters is at Geneva.',
        'India is a founder member of the WTO.',
        'The WTO covers goods, services and intellectual property.'], [
        'The WTO was set up in 1947.',
        'The WTO covers only trade in goods.',
        'The WTO has no role in trade disputes.',
        'Most favoured nation treatment allows discrimination among members.']),
    cases=[('C4', 'D4', 4, 'Country X raises duties on {g} from India but not from other WTO members. Indian exporters complain.',
            [('Which WTO principle has been violated?', 'Most favoured nation treatment (non-discrimination).'),
             ('What can India do under the WTO?', 'Raise the issue through the WTO dispute settlement mechanism.')])],
)

FAMILIES = {S + k: facts(v) for k, v in {
    '07-st1': CH07_ST1, '07-st2': CH07_ST2, '07-st3': CH07_ST3, '07-st4': CH07_ST4, '07-st5': CH07_ST5,
    '08-st1': CH08_ST1, '08-st2': CH08_ST2, '08-st3': CH08_ST3, '08-st4': CH08_ST4,
    '09-st1': CH09_ST1, '09-st2': CH09_ST2, '09-st3': CH09_ST3, '09-st4': CH09_ST4,
    '10-st1': CH10_ST1, '10-st2': CH10_ST2, '10-st3': CH10_ST3, '10-st4': CH10_ST4,
}.items()}
