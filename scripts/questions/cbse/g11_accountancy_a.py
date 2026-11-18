"""CBSE class 11 accountancy (NCERT Financial Accounting Part I) families: ch01-ch02."""
from __future__ import annotations

from qbank import mcq, inr, num_distractors
from g11_accountancy_kit import facts, FF, ctx, person, firm, amt

S = 'cbse-g11-accountancy-ch'

USERS = ['Owners', 'Management', 'Banks and financial institutions', 'Investors and potential investors',
         'Creditors (suppliers)', 'Government and tax authorities', 'Labour unions', 'Researchers']

CH01_ST1 = dict(
    cat='accounting term',
    terms=[
        ('Accounting', 'The process of identifying, measuring, recording and communicating the required information relating to economic events of an organisation to interested users.'),
        ('Book keeping', 'The recording of financial data relating to business operations in a significant and orderly manner; the first, clerical stage of accounting.'),
        ('Identifying', 'Deciding which events are economic events that are relevant to the business and should be recorded.'),
        ('Measuring', 'Quantifying business transactions in a common unit of money.'),
        ('Recording', 'Writing the identified and measured events in the books of account in chronological order.'),
        ('Communicating', 'Presenting accounting information in reports to internal and external users in a form they can use.'),
        ('Classifying', 'Grouping transactions of a similar nature at one place in separate accounts in the ledger.'),
        ('Summarising', 'Presenting classified data in a form useful to users, as in the trial balance and financial statements.'),
        ('Internal users', 'Persons inside the business, such as the owners and managers, who use accounting information to run it.'),
        ('External users', 'Persons outside the business, such as lenders, investors and tax authorities, who rely on its published reports.'),
    ],
    lists=[
        ('internal', 'internal users of accounting information', [
            ('Owners', 'They want to know the profit earned and the safety of the capital invested.'),
            ('Chief executive and managers', 'They need information for planning, controlling and decision making.'),
            ('Plant and store managers', 'They need cost and sales information about their units.'),
            ('Business unit heads', 'They compare the performance of their units with targets.')], 'external'),
        ('external', 'external users of accounting information', [
            ('Banks and financial institutions', 'They judge the firm\'s ability to repay loans and pay interest.'),
            ('Present and potential investors', 'They judge profitability and the safety of their investment.'),
            ('Creditors (suppliers)', 'They check whether the firm can pay its dues on time.'),
            ('Tax authorities', 'They assess the tax payable on the profit or turnover.'),
            ('Regulatory agencies such as SEBI and the Registrar of Companies', 'They check that the law and disclosure rules are followed.'),
            ('Labour unions', 'They use profit figures in wage and bonus negotiations.'),
            ('Customers', 'They want to know whether the firm will continue to supply goods and honour warranties.')], 'internal'),
        ('process', 'steps in the accounting process as described by NCERT', [
            ('Identifying economic events', 'Only events of a financial character relating to the business are taken up.'),
            ('Measuring them in money', 'Each event is quantified in rupees, the common unit of measurement.'),
            ('Recording', 'The events are written in the books of account (journal) in order of date.'),
            ('Communicating', 'The recorded information is reported to users through financial statements and reports.')], None),
    ],
    pairs=[('book keeping', 'accounting', [
        ('scope', 'it is limited to recording and classifying transactions', 'it includes summarising, analysing, interpreting and communicating as well'),
        ('stage', 'it is the primary (first) stage', 'it is the secondary stage that begins where book keeping ends'),
        ('objective', 'to maintain systematic records of transactions', 'to ascertain results and financial position and communicate them'),
        ('persons doing it', 'done by junior staff (book keepers)', 'done by senior staff (accountants)'),
        ('analytical skill', 'little analytical skill is needed', 'high analytical skill and judgement are needed'),
        ('decision making', 'it does not help directly in decision making', 'it provides information for decision making')])],
    scen=[('Identify the user of accounting information described.', USERS, [
        ('{f} has applied to a bank for a loan of ₹25 lakh. The bank studies its accounts before deciding.', 'Banks and financial institutions', 'A lender needs to judge the ability to repay the loan with interest.'),
        ('{p} plans to buy shares of a listed company and studies its profit record and dividend history.', 'Investors and potential investors', 'Investors judge profitability and safety of the investment.'),
        ('A wholesaler is asked to supply goods worth ₹3 lakh on 60 days\' credit to {f} and first checks its short-term position.', 'Creditors (suppliers)', 'Suppliers need to know whether dues will be paid on time.'),
        ('The income tax department examines the profit shown by {f} for the year.', 'Government and tax authorities', 'Tax authorities use accounts to assess tax liability.'),
        ('{p}, the proprietor of {f}, checks whether {his} capital invested is earning an adequate return.', 'Owners', 'Owners want to know the profit and the safety of their capital.'),
        ('The plant manager of {f} compares this month\'s cost of production with the budget to control wastage.', 'Management', 'Managers use accounting information for planning and control.'),
        ('Workers of {f} use the reported profit figures while negotiating their annual bonus.', 'Labour unions', 'Labour unions use profit figures in wage and bonus negotiations.'),
        ('A university scholar studies the accounts of several {g} firms to write a paper on the industry.', 'Researchers', 'Researchers use published accounts for study and analysis.')], None)],
    ars=[
        ('Accounting is called the language of business.', 'Accounting communicates the financial results and position of a business to its users.', 'a', 'Both true; communicating financial information is why it is called the language of business.'),
        ('Book keeping and accounting mean the same thing.', 'Book keeping is concerned only with recording and classifying transactions.', 'd', 'A is false: accounting is wider than book keeping. R is true.'),
        ('Only transactions that can be measured in money are recorded in accounting.', 'Accounting records events of a financial character relating to the business.', 'a', 'Both true; the financial character of events is why only money-measurable events are recorded.'),
        ('Tax authorities are internal users of accounting information.', 'Tax authorities use accounting information to assess the tax liability of a business.', 'd', 'A is false: tax authorities are external users. R is true.'),
        ('Banks study a firm\'s accounts before sanctioning a loan.', 'Banks need to know whether the firm will be able to repay the loan with interest.', 'a', 'Both true and R explains A.'),
        ('Accounting is an information system.', 'Accounting collects and processes data and communicates the results to decision makers.', 'a', 'Both true; R explains why it is an information system.')],
    tf=('accounting and its users', [
        'Accounting records only those events which are of a financial character.',
        'Management is an internal user of accounting information.',
        'Book keeping is the first stage of the accounting process.',
        'Communicating information to users is a part of accounting.',
        'Banks are external users of accounting information.'], [
        'Accounting records all events of a business, whether or not they can be measured in money.',
        'Book keeping includes the analysis and interpretation of financial statements.',
        'Creditors are internal users of accounting information.',
        'Accounting information is meant only for the owner of the business.',
        'Measuring means writing transactions in the journal in order of date.']),
    cases=[
        ('C4', 'D4', 4, '{p} runs {f}, a {g} business in {c}. {He} keeps a diary of cash received and paid but no other record. {His} bank has asked for the profit figure and a statement of assets and liabilities before renewing {his} loan, and a supplier wants to know if she can pay on time.',
         [('Name the two external users mentioned and the information each needs.', 'The bank: profit and repaying capacity; the supplier: short-term liquidity (ability to pay dues on time).'),
          ('Why is {his} cash diary not enough? Suggest what {he} should do.', 'A cash diary records only cash; it cannot show profit, credit transactions or financial position. {He} should maintain a complete double entry system and prepare financial statements.')]),
        ('C4', 'D3', 4, '{f} of {c} has three people who use its accounts: the owner {p}, the store manager {p2}, and the State Bank of India which has given it a cash credit limit.',
         [('Classify each of them as an internal or external user.', 'Owner {p}: internal; store manager {p2}: internal; bank: external.'),
          ('State one item of information each would look for.', 'Owner: net profit and return on capital; manager: sales and cost of stock for control; bank: liquidity and repaying capacity.')]),
        ('C4', 'D5', 6, '{p} says, "I am small. My book keeper writes every transaction in the books, so I already have accounting." {His} accountant friend {p2} disagrees.',
         [('Is {p} right? Explain with reference to the stages of accounting.', 'No. Book keeping covers only identifying and recording (and classifying); accounting also summarises, analyses, interprets and communicates the results.'),
          ('List four things accounting would give {him} that book keeping alone does not.', 'Profit or loss for the year; financial position (balance sheet); analysis of trends and ratios for decisions; reports for banks, tax authorities and other users.'),
          ('Who in {his} business should do each stage?', 'Book keeping by a junior book keeper; summarising, analysis and reporting by a qualified accountant.')]),
    ],
)

CH01_ST2 = dict(
    lists=[
        ('obj', 'objectives of accounting', [
            ('Maintaining records of business transactions', 'All transactions are recorded systematically so that nothing depends on memory.'),
            ('Calculating profit or loss', 'Revenues and expenses of a period are matched to find the profit or loss.'),
            ('Depicting the financial position', 'A balance sheet shows the assets, liabilities and capital on a date.'),
            ('Providing accounting information to users', 'Information is communicated to owners, managers, lenders and others for decisions.')], None),
        ('adv', 'advantages of accounting', [
            ('Provides information about financial performance', 'Profit and financial position are known at regular intervals.'),
            ('Helps in comparative study', 'Results of different years or firms can be compared.'),
            ('Replaces memory', 'Systematic records remove dependence on the memory of the owner.'),
            ('Serves as evidence in legal matters', 'Properly kept books are accepted as evidence by courts.'),
            ('Helps in settlement of tax liability', 'Tax authorities accept properly kept accounts while assessing income tax and GST.'),
            ('Helps in the sale of a business', 'The value of a business can be determined from its accounts.'),
            ('Assists management in decision making', 'Information on costs, sales and profits helps in planning and control.')], 'lim'),
        ('lim', 'limitations of accounting', [
            ('Ignores qualitative elements', 'Items such as staff skill, morale or quality of management cannot be expressed in money and are left out.'),
            ('Ignores price level changes', 'Assets are shown at historical cost, so the effect of inflation is not shown.'),
            ('Based on estimates', 'Depreciation, provisions and similar items involve estimates and personal judgement.'),
            ('Can be manipulated (window dressing)', 'Figures may be arranged to show a better position than the real one.'),
            ('Historical in nature', 'It records past transactions and does not by itself predict the future.')], 'adv'),
        ('role', 'roles of accounting described in NCERT', [
            ('Language of business', 'It communicates financial information about the business to its users.'),
            ('Historical record', 'It records transactions in order of date as a history of the business.'),
            ('Current economic reality', 'It shows the current financial position on which decisions are based.'),
            ('Information system', 'It collects, processes and communicates economic information to decision makers.'),
            ('Service to users', 'It meets the information needs of various internal and external users.')], None),
    ],
    scen=[('Which limitation of accounting does this illustrate?', ['Ignores qualitative elements', 'Ignores price level changes', 'Based on estimates', 'Can be manipulated (window dressing)', 'Historical in nature'], [
        ('{f} bought land in {c} in 1995 for ₹8 lakh. Its balance sheet still shows ₹8 lakh, although the land would sell for ₹1.2 crore today.', 'Ignores price level changes', 'Assets stay at historical cost; the rise in prices is not shown.'),
        ('The highly skilled and loyal sales team of {f} is its biggest strength, but it appears nowhere in the accounts.', 'Ignores qualitative elements', 'Things that cannot be measured in money are left out of accounts.'),
        ('Two accountants of {f} estimate the useful life of the same machine as 8 and 12 years, giving different profits.', 'Based on estimates', 'Depreciation depends on estimated life, so figures involve judgement.'),
        ('Just before the year end, {f} delayed payments to suppliers so that its cash balance would look large to the bank.', 'Can be manipulated (window dressing)', 'Figures were arranged to show a better position than the real one.'),
        ('An investor complains that the latest accounts of {f} tell him what happened last year, not what will happen next year.', 'Historical in nature', 'Accounting records past transactions and does not predict the future.')], None),
        ('Which objective or advantage of accounting is served here?', ['Serves as evidence in legal matters', 'Helps in settlement of tax liability', 'Helps in comparative study', 'Helps in the sale of a business', 'Replaces memory', 'Calculating profit or loss'], [
        ('A dispute with a customer of {f} reached court; the firm produced its ledger account with the customer as proof.', 'Serves as evidence in legal matters', 'Properly kept books are accepted as evidence.'),
        ('{p} wants to sell {his} shop {f} and the buyer agrees a price on the basis of its accounts.', 'Helps in the sale of a business', 'Accounts help to determine the value of a business.'),
        ('{p} compares the sales and profits of {f} for the last five years to see the trend.', 'Helps in comparative study', 'Recorded results of different years can be compared.'),
        ('The GST officer accepted the returns of {f} because its books were properly maintained.', 'Helps in settlement of tax liability', 'Properly kept accounts are accepted by tax authorities.'),
        ('{p} no longer has to remember which customers owe {him} money, since every credit sale is in the books.', 'Replaces memory', 'Records remove dependence on memory.'),
        ('At the end of the year {p} matches the revenues and expenses of {f} to see how much {he} earned.', 'Calculating profit or loss', 'Matching revenues and expenses gives the profit or loss.')], None)],
    ars=[
        ('Accounting does not show the effect of inflation.', 'Assets are recorded at historical cost.', 'a', 'Both true; recording at historical cost is why price changes are ignored.'),
        ('Accounting information is completely free from personal judgement.', 'Depreciation and provisions are based on estimates.', 'd', 'A is false: estimates bring judgement into accounts. R is true.'),
        ('Accounting records are accepted as evidence in courts.', 'Accounting replaces the memory of the owner.', 'b', 'Both true, but R does not explain why records are legal evidence (that is because they are systematic, dated records).'),
        ('Ascertaining profit or loss is an objective of accounting.', 'The balance sheet shows the profit or loss of a business.', 'c', 'A is true. R is false: profit is shown by the profit and loss account; the balance sheet shows the financial position.')],
    tf=('objectives and limitations of accounting', [
        'Accounting ignores qualitative elements such as the efficiency of management.',
        'Depicting the financial position of a business is an objective of accounting.',
        'Accounting records help in the settlement of tax liability.',
        'Window dressing is a limitation of accounting.'], [
        'Accounting shows the current market value of every asset.',
        'Accounting figures are never affected by estimates.',
        'Accounting can predict the future profit of a business accurately.',
        'Accounting records cannot be used as evidence in a court of law.']),
    cases=[
        ('C4', 'D4', 4, '{p} owns {f}, {c}. A competitor shows a higher profit than {f}, but {p} knows the competitor bought its machinery 20 years ago at low prices, while {f} bought new machinery last year. The competitor also has a famous brand that does not appear in its balance sheet.',
         [('Identify two limitations of accounting illustrated here.', 'Ignores price level changes (old machinery at historical cost gives low depreciation); ignores qualitative elements (brand value not recorded).'),
          ('Explain why {p} should be careful while comparing the two profits.', 'Profits are based on historical costs and leave out non-money factors, so they are not strictly comparable.')]),
    ],
)

QC = ['Reliability', 'Relevance', 'Understandability', 'Comparability']
CH01_ST3 = dict(
    cat='qualitative characteristic',
    terms=[
        ('Reliability', 'Users must be able to depend on the information; it should be verifiable, neutral and a faithful representation of facts.'),
        ('Relevance', 'Information should be available in time and should influence the decisions of users by helping them form predictions or confirm earlier ones.'),
        ('Understandability', 'Information should be presented so that users with reasonable knowledge can grasp its meaning in the same sense as the preparers.'),
        ('Comparability', 'Information should allow users to compare the performance of the firm over time and with other firms.'),
        ('Verifiability', 'Independent persons using the same methods would arrive at the same figures.'),
        ('Timeliness', 'Information is made available to decision makers before it loses its capacity to influence decisions.'),
    ],
    lists=[('qc', 'qualitative characteristics of accounting information', [
        ('Reliability', 'Information must be verifiable, free from bias and error, and faithfully represent what it claims to.'),
        ('Relevance', 'Information must be timely and help users predict or confirm outcomes.'),
        ('Understandability', 'Information must be presented in a form users can understand.'),
        ('Comparability', 'Information must allow inter-period (intra-firm) and inter-firm comparison.')], None)],
    pairs=[('intra-firm comparison', 'inter-firm comparison', [
        ('meaning', 'comparison of the same firm\'s results over different periods', 'comparison of one firm\'s results with those of other firms'),
        ('requirement', 'the same accounting methods must be followed year after year', 'similar accounting methods must be followed by the firms compared'),
        ('purpose', 'to study the trend of the firm\'s own performance', 'to judge the firm\'s position in its industry')])],
    scen=[('Which qualitative characteristic of accounting information is involved?', QC, [
        ('{f} publishes its annual accounts eleven months after the year end, by which time the bank has already rejected its loan application for want of data.', 'Relevance', 'Information that is not timely cannot influence decisions, so it lacks relevance.'),
        ('Two auditors examine the sales figure of {f} from its invoices and both arrive at exactly ₹48,60,000.', 'Reliability', 'The figure is verifiable from evidence, so it is reliable.'),
        ('{f} changes its method of stock valuation every year, so {p} cannot compare this year\'s profit with last year\'s.', 'Comparability', 'Frequent changes in method destroy comparability over time.'),
        ('The accounts of {f} use so many technical codes that even an educated shareholder cannot make out what they mean.', 'Understandability', 'Information must be presented in a form users can understand.'),
        ('An investor compares the profit margins of {f} and {f2}, which both follow the same accounting standards.', 'Comparability', 'Similar methods allow inter-firm comparison.'),
        ('The manager of {f} gets weekly sales reports in time to decide which products to reorder.', 'Relevance', 'Timely information that influences decisions is relevant.'),
        ('The accountant of {f} records sales at the invoice amount rather than at the figure the sales manager hopes to achieve.', 'Reliability', 'Recording supported, unbiased figures makes information reliable.'),
        ('{f} adds plain-language notes explaining each major item in its balance sheet for small shareholders.', 'Understandability', 'Clear presentation helps users understand the information.')], None)],
    ars=[
        ('Accounting information should be free from bias.', 'Reliable information must be neutral and faithfully represent facts.', 'a', 'Both true; neutrality is part of reliability, which explains A.'),
        ('Information given late may lose its relevance.', 'Relevant information must be available in time to influence decisions.', 'a', 'Both true and R explains A.'),
        ('Comparability requires a firm to change its accounting methods every year.', 'Comparability allows users to compare the results of different periods.', 'd', 'A is false: comparability needs consistent methods. R is true.'),
        ('Understandability means information must be presented for users with no knowledge of business at all.', 'Accounting information should be presented in a manner users can understand.', 'd', 'A is false: users are expected to have reasonable knowledge. R is true.')],
    tf=('qualitative characteristics', [
        'Reliable information should be verifiable.',
        'Timeliness is an aspect of relevance.',
        'Comparability includes both intra-firm and inter-firm comparison.'], [
        'Relevance means information must be verifiable by independent persons.',
        'Understandability requires accounts to avoid all numbers.',
        'Comparability is possible even if each firm follows a different method every year.',
        'Reliability means information should be produced as fast as possible.']),
    cases=[
        ('C4', 'D4', 4, 'The annual report of {f}, {c}, came out 10 months after the year end. It used a new depreciation method without saying so, and it was full of unexplained abbreviations.',
         [('Identify the three qualitative characteristics that are missing.', 'Relevance (not timely); comparability (method changed without disclosure); understandability (unexplained abbreviations).'),
          ('Suggest one improvement for each.', 'Publish within a few months; follow consistent methods and disclose changes; give clear headings and notes.')]),
        ('C4', 'D5', 4, '{p}, accountant of {f}, is under pressure from the owner to record an expected order of ₹5 lakh as sales this year so that the bank sees higher sales.',
         [('Which qualitative characteristic would be violated?', 'Reliability: the figure would not be supported by evidence and would be biased.'),
          ('What should {p} do and why?', 'Refuse; record sales only when they take place, since users such as the bank depend on faithful, verifiable figures.')]),
    ],
)

TERMS4 = [
    ('Business entity', 'An identifiable business enterprise, such as a sole proprietorship, partnership or company, treated as separate from its owner.'),
    ('Transaction', 'An event involving an exchange of money or money\'s worth between two or more parties.'),
    ('Capital', 'The amount invested by the owner in the business; it is a liability of the business towards the owner.'),
    ('Drawings', 'Cash or goods withdrawn by the owner from the business for personal use.'),
    ('Liabilities', 'Obligations or debts that the enterprise has to pay at some time in the future.'),
    ('Assets', 'Economic resources of an enterprise that can be expressed in money and have value or benefit for the future.'),
    ('Revenue', 'The amount a business earns by selling its products or providing services to customers.'),
    ('Expense', 'The cost incurred by a business in the process of earning revenue.'),
    ('Debtors', 'Persons or entities who owe an amount to the enterprise for goods or services supplied on credit.'),
    ('Creditors', 'Persons or entities to whom the enterprise owes an amount for goods or services bought on credit.'),
    ('Goods', 'Products in which the business deals, bought for resale or made for sale.'),
    ('Stock (inventory)', 'Goods, spares and other items in hand at the end of an accounting period.'),
    ('Voucher', 'Documentary evidence in support of a transaction, such as a cash memo, invoice or receipt.'),
    ('Trade discount', 'A reduction given on the list price at the time of sale; it is not recorded in the books.'),
    ('Cash discount', 'A reduction given for prompt payment of a debt; it is recorded in the books.'),
]
CH01_ST4 = dict(
    cat='basic accounting term',
    terms=TERMS4,
    lists=[
        ('ca', 'current assets', [('Cash in hand', 'Held for day-to-day payments.'), ('Debtors', 'Expected to be collected within a year.'),
                                  ('Stock of goods', 'Expected to be sold within the operating cycle.'), ('Bills receivable', 'Realised on maturity within a year.'),
                                  ('Prepaid expenses', 'Benefit is received within the next year.')], 'nca'),
        ('nca', 'non-current (fixed) assets', [('Land and building', 'Held for long-term use, not for sale.'), ('Plant and machinery', 'Used in production over many years.'),
                                               ('Furniture and fixtures', 'Used in the business for several years.'), ('Motor vehicles', 'Used for transport over several years.'),
                                               ('Patents and trademarks', 'Intangible assets giving long-term benefit.')], 'ca'),
        ('cl', 'current liabilities', [('Creditors', 'Payable for credit purchases within a short period.'), ('Bills payable', 'Payable on maturity within a year.'),
                                       ('Bank overdraft', 'Repayable on demand.'), ('Outstanding expenses', 'Expenses due but unpaid, payable shortly.')], 'ncl'),
        ('ncl', 'non-current (long-term) liabilities', [('Long-term loan from a bank', 'Repayable after more than a year.'), ('Debentures', 'Long-term borrowed funds.'),
                                                        ('Loan from a financial institution for 5 years', 'Repayable after several years.')], 'cl'),
    ],
    pairs=[('trade discount', 'cash discount', [
        ('purpose', 'given to promote sales or for bulk purchase', 'given to encourage prompt payment'),
        ('time', 'allowed at the time of sale', 'allowed at the time of payment'),
        ('recording', 'not recorded in the books; sale is recorded at net price', 'recorded in the books as discount allowed or received'),
        ('shown in invoice', 'deducted on the face of the invoice', 'not shown in the invoice')]),
        ('debtors', 'creditors', [
        ('meaning', 'persons who owe money to the business', 'persons to whom the business owes money'),
        ('arise from', 'credit sales of goods or services', 'credit purchases of goods or services'),
        ('balance sheet', 'shown as a current asset', 'shown as a current liability'),
        ('balance in ledger', 'their accounts show a debit balance', 'their accounts show a credit balance')])],
    scen=[('Identify the accounting term.', [t for t, _ in TERMS4], [
        ('{p} sold goods worth ₹40,000 on credit to {p2}. In the books of {p}, which term describes {p2}?', 'Debtors', '{p2} owes money to the business for goods bought on credit.'),
        ('{f} bought goods worth ₹60,000 on credit from {f2}. In the books of {f}, which term describes {f2}?', 'Creditors', 'The business owes {f2} for goods bought on credit.'),
        ('{p}, owner of {f}, took ₹5,000 from the cash box to pay {his} son\'s school fees. What is this amount called?', 'Drawings', 'Cash withdrawn by the owner for personal use is drawings.'),
        ('{p} started {f} by putting ₹3,00,000 of {his} savings into it. What is this amount called in the books of the business?', 'Capital', 'The amount invested by the owner is capital.'),
        ('At the end of the year {f} has unsold {g} worth ₹75,000 lying in the godown. What is this called?', 'Stock (inventory)', 'Goods in hand at the end of the period are stock.'),
        ('A cash memo issued by {f} for a sale of ₹2,400 is kept in the file as proof of the sale. What is this document called?', 'Voucher', 'Documentary evidence supporting a transaction is a voucher.'),
        ('{f} offers 10% off the list price of its {g} to a retailer who buys in bulk. What is this reduction called?', 'Trade discount', 'A reduction on list price at the time of sale is trade discount.'),
        ('{p2} owed {f} ₹10,000 and was allowed ₹200 off for paying within 7 days. What is the ₹200 called?', 'Cash discount', 'A reduction for prompt payment is cash discount.'),
        ('{f} earned ₹9,50,000 during the year from selling {g}. What is this amount called?', 'Revenue', 'Amount earned from selling goods is revenue.'),
        ('{f} paid ₹18,000 as salary to its staff in the year. Which term describes this amount?', 'Expense', 'Cost incurred in earning revenue is an expense.')], None)],
    ars=[
        ('Capital is treated as a liability of the business.', 'The business and its owner are treated as separate entities.', 'a', 'Both true; because of the separate entity, the business owes capital to the owner.'),
        ('Trade discount is not recorded in the books of account.', 'Trade discount is allowed at the time of payment.', 'c', 'A is true. R is false: trade discount is allowed at the time of sale; cash discount is allowed at the time of payment.'),
        ('Debtors are shown as current assets.', 'Debtors are expected to pay the amount within a short period.', 'a', 'Both true and R explains A.'),
        ('Goods withdrawn by the owner for personal use are treated as drawings.', 'Drawings reduce the capital of the owner.', 'b', 'Both true, but R (effect on capital) does not explain why the withdrawal is called drawings.'),
        ('Bank overdraft is a current liability.', 'A bank overdraft is repayable on demand.', 'a', 'Both true and R explains A.'),
        ('Cash discount is recorded in the books of account.', 'Cash discount is given to encourage prompt payment.', 'b', 'Both true, but the purpose of cash discount does not explain why it is recorded.')],
    tf=('basic accounting terms', [
        'Capital is the amount invested by the owner in the business.',
        'Trade discount is not recorded in the books of account.',
        'Debtors appear on the assets side of the balance sheet.',
        'Creditors are persons to whom the business owes money.'], [
        'Drawings increase the capital of the owner.',
        'Creditors are shown as current assets.',
        'Trade discount is given for prompt payment.',
        'A bank overdraft is a non-current liability.']),
    cases=[],
)

def c1s4_capital(r):
    who = person(r)
    a = amt(r, 200000, 1500000, 5000)
    l = amt(r, 20000, a // 2, 5000)
    return {'stem': f'{who}\'s business has total assets of {inr(a)} and total liabilities (excluding capital) of {inr(l)}. What is the owner\'s capital?',
            'answer': inr(a - l), 'key': f'Capital = Assets − Liabilities = {inr(a)} − {inr(l)} = {inr(a - l)}.',
            'distractors': [inr(a + l), inr(l), inr(a)]}


def c1s4_discounts(r):
    lp = amt(r, 20000, 200000, 1000)
    td = r.choice([5, 10, 15, 20])
    cd = r.choice([2, 3, 5])
    net = lp * (100 - td) // 100
    cdisc = net * cd / 100
    f1, f2 = firm(r), firm(r)
    return {'stem': f'{f1} sold goods with a list price of {inr(lp)} to {f2} at {td}% trade discount and {cd}% cash discount. {f2} paid immediately. Find (i) the amount of the invoice (ii) the cash discount (iii) the cash received.',
            'answer': f'(i) {inr(net)} (ii) {inr(cdisc)} (iii) {inr(net - cdisc)}',
            'key': f'Trade discount {td}% of {inr(lp)} = {inr(lp - net)}, invoice {inr(net)} (1); cash discount {cd}% of {inr(net)} = {inr(cdisc)} (1); cash received {inr(net - cdisc)} (1). Only the cash discount is recorded in the books.'}


def c1s4_classify(r):
    items = [('Cash in hand', 'Current asset'), ('Debtors', 'Current asset'), ('Stock', 'Current asset'), ('Bills receivable', 'Current asset'),
             ('Prepaid insurance', 'Current asset'), ('Machinery', 'Non-current asset'), ('Building', 'Non-current asset'), ('Furniture', 'Non-current asset'),
             ('Goodwill', 'Non-current asset'), ('Creditors', 'Current liability'), ('Bills payable', 'Current liability'), ('Bank overdraft', 'Current liability'),
             ('Outstanding salary', 'Current liability'), ('Loan from bank repayable after 5 years', 'Non-current liability'), ('Debentures', 'Non-current liability')]
    it, cls = r.choice(items)
    opts = ['Current asset', 'Non-current asset', 'Current liability', 'Non-current liability']
    return mcq(f'In the balance sheet of a trader, "{it}" is classified as a …', cls, [o for o in opts if o != cls],
               f'{it} is a {cls.lower()}.', r)


def c1s4_capital_change(r):
    who = person(r)
    op = amt(r, 200000, 800000, 10000)
    prof = amt(r, 30000, 200000, 1000)
    dr = amt(r, 10000, prof - 5000, 1000)
    add = r.choice([0, amt(r, 20000, 100000, 5000)])
    cl = op + prof - dr + add
    addtxt = f', introduced additional capital of {inr(add)}' if add else ''
    return {'stem': f'{who} started the year with a capital of {inr(op)}. During the year the business earned a profit of {inr(prof)}{addtxt}, and {who} withdrew {inr(dr)} for personal use. Find the capital at the end of the year.',
            'answer': inr(cl),
            'key': f'Closing capital = Opening capital + Profit + Additional capital − Drawings = {inr(op)} + {inr(prof)} + {inr(add)} − {inr(dr)} = {inr(cl)}.',
            'distractors': [inr(op + prof + dr + add), inr(op + prof - dr), inr(op - prof - dr + add)]}


def c1s4_profit_from_capital(r):
    who = person(r)
    op = amt(r, 200000, 800000, 10000)
    prof = amt(r, 40000, 250000, 1000)
    dr = amt(r, 10000, 60000, 1000)
    add = amt(r, 20000, 100000, 5000)
    cl = op + prof - dr + add
    return {'stem': f'{who}\'s capital was {inr(op)} on 1 April 2025 and {inr(cl)} on 31 March 2026. During the year {who} withdrew {inr(dr)} and introduced fresh capital of {inr(add)}. Calculate the profit for the year.',
            'answer': inr(prof),
            'key': f'Profit = Closing capital + Drawings − Additional capital − Opening capital = {inr(cl)} + {inr(dr)} − {inr(add)} − {inr(op)} = {inr(prof)}.'}


def c1s4_case(r):
    d = ctx(r)
    cap = amt(r, 300000, 900000, 10000)
    loan = amt(r, 50000, 200000, 10000)
    cred = amt(r, 20000, 90000, 1000)
    deb = amt(r, 15000, 80000, 1000)
    furn = amt(r, 40000, 150000, 5000)
    stock = amt(r, 50000, 200000, 5000)
    cash = cap + loan + cred - deb - furn - stock
    if cash <= 0:
        raise ValueError
    return {'stem': f'{d["p"]} started {d["f"]} in {d["c"]} with capital of {inr(cap)} and a bank loan of {inr(loan)} repayable in 4 years. At the end of the first month the business had furniture {inr(furn)}, stock {inr(stock)}, debtors {inr(deb)}, creditors {inr(cred)} and the rest in cash. Assume no profit or loss yet.\n(i) Find the cash balance. (ii) Classify each item as a current asset, non-current asset, current liability or non-current liability.',
            'answer': f'(i) Cash {inr(cash)} (ii) Furniture: non-current asset; stock, debtors, cash: current assets; creditors: current liability; bank loan: non-current liability; capital: owner\'s equity.',
            'key': f'(i) Assets = Liabilities + Capital: cash = {inr(cap)} + {inr(loan)} + {inr(cred)} − {inr(furn)} − {inr(stock)} − {inr(deb)} = {inr(cash)} (2 marks). (ii) classification (2 marks).'}


FAMILIES = {
    S + '01-st1': facts(CH01_ST1),
    S + '01-st2': facts(CH01_ST2),
    S + '01-st3': facts(CH01_ST3),
    S + '01-st4': facts(CH01_ST4) + [
        FF('C3', 'D2', 'numerical', c1s4_capital, marks=2), FF('C3', 'D3', 'numerical', c1s4_discounts, marks=3, kinds=('m3',)),
        FF('C2', 'D1', 'mcq', c1s4_classify), FF('C3', 'D3', 'numerical', c1s4_capital_change, marks=2),
        FF('C4', 'D4', 'numerical', c1s4_profit_from_capital, marks=3, kinds=('m3',)), FF('C4', 'D4', 'case', c1s4_case, marks=4, kinds=('m4', 'case'))],
}


# ---------------- ch02 Theory Base of Accounting ----------------

CH02_ST1 = dict(
    cat='term',
    terms=[
        ('Generally Accepted Accounting Principles (GAAP)', 'Rules or guidelines adopted for recording and reporting business transactions so as to bring uniformity in the preparation and presentation of financial statements.'),
        ('Basic accounting concepts', 'The fundamental ideas or basic assumptions underlying the theory and practice of financial accounting.'),
        ('Accounting conventions', 'Customs or practices, such as consistency and conservatism, followed by accountants because they are widely accepted.'),
        ('Accounting standards', 'Written statements of uniform accounting rules and guidelines issued by an expert body for preparing consistent financial statements.'),
    ],
    lists=[('need', 'reasons why GAAP are needed', [
        ('Uniformity in accounting', 'All firms record and report similar transactions in the same way.'),
        ('Comparability of financial statements', 'Results of different firms and periods can be compared meaningfully.'),
        ('Reliability for users', 'Users can depend on statements prepared on accepted principles.'),
        ('Reduced scope for manipulation', 'Accepted rules limit arbitrary choices by accountants.'),
        ('Basis for accounting standards and law', 'Standards and legal requirements build on accepted principles.')], None),
        ('qual', 'qualities that make an accounting principle generally accepted', [
        ('Relevance', 'It results in information that is meaningful and useful to users.'),
        ('Objectivity', 'It is based on facts and free from personal bias.'),
        ('Feasibility', 'It can be put into practice without undue complexity or cost.')], None)],
    scen=[('Which quality required of a generally accepted accounting principle is missing?', ['Relevance', 'Objectivity', 'Feasibility', 'Consistency'], [
        ('A proposed rule would require {f} to value every item of stock daily by an outside valuer, which is too costly for a small {g} shop.', 'Feasibility', 'A principle must be practicable without undue complexity or cost.'),
        ('A proposed rule lets the owner of {f} value assets at whatever figure he personally thinks fair.', 'Objectivity', 'A principle must be free from personal bias and based on facts.'),
        ('A proposed rule would make {f} report the number of tea breaks taken by staff, which no user needs.', 'Relevance', 'A principle must produce information that is useful to users.'),
        ('Under a suggested method, two accountants of {f} would arrive at different figures for the same transaction according to their personal views.', 'Objectivity', 'Results should not depend on the person preparing them.'),
        ('A rule requires {f} to prepare a 300-page report every week, which takes more effort than its value to anyone.', 'Feasibility', 'The cost and effort of applying a principle must be reasonable.'),
        ('A suggested disclosure would tell investors in {f} the colour of its delivery vans.', 'Relevance', 'The information would not influence any user\'s decision.')], None)],
    ars=[
        ('GAAP bring uniformity in financial statements.', 'GAAP are rules adopted for recording and reporting business transactions.', 'a', 'Both true and R explains A.'),
        ('Accounting principles are as rigid as the laws of physics.', 'Accounting principles are man-made and evolve with business needs.', 'd', 'A is false: accounting principles are man-made and change over time. R is true.'),
        ('Without GAAP, the accounts of two firms would be difficult to compare.', 'Each firm could then follow its own methods of recording and reporting.', 'a', 'Both true and R explains A.'),
        ('GAAP are issued by the Reserve Bank of India.', 'GAAP evolve through experience, practice and pronouncements of professional bodies.', 'd', 'A is false: GAAP are not issued by the RBI. R is true.')],
    tf=('Generally Accepted Accounting Principles', [
        'GAAP help in making financial statements comparable.',
        'Accounting principles are man-made and evolve over time.',
        'A principle should be relevant, objective and feasible to be generally accepted.'], [
        'GAAP are natural laws that never change.',
        'Every firm is free to adopt its own principles for its published accounts.',
        'GAAP apply only to sole proprietorships.',
        'GAAP make accounting information less reliable.']),
    cases=[
        ('C4', 'D4', 4, '{f} and {f2} are two {g} firms in {c}. {f} values its closing stock at cost while {f2} values it at selling price. An investor {p} wants to compare their profits.',
         [('Why will {p} find the comparison misleading?', 'The two firms use different principles for the same item, so their profits are not computed on the same basis.'),
          ('How do GAAP and accounting standards solve this problem?', 'They lay down uniform rules (stock at cost or net realisable value, whichever is lower), bringing uniformity and comparability.')]),
    ],
)

CONC = ['Business entity concept', 'Money measurement concept', 'Going concern concept', 'Accounting period concept', 'Cost concept', 'Dual aspect concept']
CONC_ALL = CONC + ['Revenue recognition concept', 'Matching concept', 'Full disclosure concept', 'Consistency concept', 'Conservatism concept', 'Materiality concept', 'Objectivity concept']
CH02_ST2 = dict(
    cat='accounting concept',
    terms=[
        ('Business entity concept', 'The business is treated as separate and distinct from its owner, so transactions are recorded from the point of view of the business.'),
        ('Money measurement concept', 'Only those transactions and events that can be expressed in terms of money are recorded in the books.'),
        ('Going concern concept', 'The business is assumed to continue its operations for a long period and not to be wound up in the near future.'),
        ('Accounting period concept', 'The life of the business is divided into smaller periods, usually a year, at the end of which results and position are ascertained.'),
        ('Cost concept', 'Assets are recorded at the price paid to acquire them, and this cost is the basis for all later accounting for the asset.'),
        ('Dual aspect concept', 'Every transaction has two aspects, a debit and a credit of equal amount, so that assets always equal liabilities plus capital.'),
    ],
    scen=[('Which accounting concept is applied?', CONC, [
        ('{p} paid {his} personal electricity bill from the cash of {f}. The amount is recorded as drawings, not as a business expense.', 'Business entity concept', 'The owner and the business are separate; personal payments are drawings.'),
        ('{f} has a very hardworking and loyal staff, but this is not recorded in the books.', 'Money measurement concept', 'Only events measurable in money are recorded.'),
        ('{f} bought a machine for ₹4,00,000 expected to last 10 years and charges depreciation every year instead of treating the whole cost as this year\'s expense.', 'Going concern concept', 'Because the business will continue, the cost is spread over the useful life.'),
        ('{f} prepares its profit and loss account for the year 1 April to 31 March every year.', 'Accounting period concept', 'The life of the business is divided into periods of one year.'),
        ('{f} bought land for ₹20 lakh. Its market value is now ₹35 lakh, but it is still shown at ₹20 lakh.', 'Cost concept', 'Assets are recorded and shown at their acquisition cost.'),
        ('{p} started {f} with ₹5,00,000. The business records cash of ₹5,00,000 and capital of ₹5,00,000.', 'Dual aspect concept', 'Each transaction has two equal aspects; assets = liabilities + capital.'),
        ('{p} gave ₹50,000 from {his} own savings to {his} brother as a gift. Nothing is recorded in the books of {f}.', 'Business entity concept', 'Personal transactions of the owner are not business transactions.'),
        ('{f} holds 500 kg of rice, 20 chairs and 3 computers. In the accounts all of them appear in rupees only.', 'Money measurement concept', 'Money is the common unit for recording dissimilar items.'),
        ('Prepaid insurance of {f} is shown as an asset because the business is expected to use the benefit next year.', 'Going concern concept', 'The business is assumed to continue, so future benefits are carried forward.'),
        ('{f} paid ₹6,00,000 for a machine and ₹40,000 for its installation; the machine is recorded at ₹6,40,000.', 'Cost concept', 'All costs of acquiring the asset and making it ready for use form its cost.'),
        ('The bank wants the results of {f} every year, not only when the business closes.', 'Accounting period concept', 'Results are measured for regular periods for users\' needs.'),
        ('Goods bought for ₹30,000 on credit increase stock by ₹30,000 and creditors by ₹30,000.', 'Dual aspect concept', 'Both aspects of the transaction are recorded for equal amounts.')], None)],
    pairs=[('business entity concept', 'money measurement concept', [
        ('meaning', 'the business is separate from its owner', 'only money-measurable events are recorded'),
        ('example', 'owner\'s personal expenses paid by the business are drawings', 'skill of employees is not recorded'),
        ('purpose', 'to find the true profit of the business, not of the owner', 'to express dissimilar items in a common unit')])],
    ars=[
        ('Capital is shown as a liability in the books of the business.', 'According to the business entity concept, the owner and the business are separate.', 'a', 'Both true and R explains A.'),
        ('Fixed assets are shown at cost less depreciation and not at their market value.', 'According to the going concern concept, fixed assets are held for use and not for sale.', 'a', 'Both true and R explains A.'),
        ('Every debit has an equal credit.', 'According to the dual aspect concept, every transaction affects two accounts.', 'a', 'Both true and R explains A.'),
        ('The quality of management is recorded in the books of account.', 'Only transactions that can be expressed in money are recorded.', 'd', 'A is false; R (money measurement) is true.'),
        ('Land is shown at its current market value in the balance sheet.', 'Assets are recorded at the price paid for them.', 'd', 'A is false under the cost concept; R is true.'),
        ('Financial statements are prepared at regular intervals, usually one year.', 'Users need information about the business periodically for decisions.', 'a', 'Both true; R explains the accounting period concept stated in A.'),
        ('The accounting equation always balances.', 'The going concern concept assumes the business will continue for a long time.', 'b', 'Both true, but the equation balances because of the dual aspect concept, not going concern.')],
    tf=('basic accounting concepts', [
        'Under the cost concept assets are recorded at their acquisition cost.',
        'The dual aspect concept is the basis of the accounting equation.',
        'The going concern concept justifies charging depreciation over the life of an asset.',
        'The money measurement concept excludes events that cannot be measured in money.'], [
        'Under the business entity concept, the owner\'s personal expenses are business expenses.',
        'The cost concept requires assets to be revalued every year at market price.',
        'The accounting period concept assumes the business will be closed at the end of each year.',
        'Under the money measurement concept, the health of the manager is recorded in the books.']),
    cases=[
        ('C4', 'D4', 4, '{p} owns {f} in {c}. During March: (a) {he} paid {his} daughter\'s college fees of ₹45,000 from the business bank account; (b) the business bought a building for ₹40 lakh, now worth ₹48 lakh; (c) the shop\'s friendly location is a big advantage but is not recorded.',
         [('Name the concept involved in each of (a), (b) and (c).', '(a) Business entity concept (b) Cost concept (c) Money measurement concept.'),
          ('How should (a) and (b) be shown in the books?', '(a) As drawings, reducing {his} capital (Drawings A/c Dr To Bank A/c ₹45,000). (b) Building at its cost of ₹40 lakh (less depreciation), not ₹48 lakh.')]),
        ('C4', 'D5', 6, '{p}, a new accountant at {f}, suggests three changes: (i) record the building at its present market value every year; (ii) show the proprietor\'s house rent as a business expense since the proprietor is the business; (iii) charge the entire cost of a 10-year machine to this year\'s profit.',
         [('Which concept does each suggestion violate?', '(i) Cost concept (ii) Business entity concept (iii) Going concern concept (and matching).'),
          ('Explain the correct treatment in each case.', '(i) Show the building at cost less depreciation. (ii) Treat the house rent as drawings. (iii) Spread the cost over 10 years by charging depreciation.'),
          ('What would happen to the reported profit if all three were accepted?', 'Profit would be distorted: understated by the full machine cost and the house rent, and asset values would fluctuate with the market, so statements would be unreliable and not comparable.')]),
    ],
)

CONC3 = ['Revenue recognition concept', 'Matching concept', 'Full disclosure concept', 'Consistency concept', 'Conservatism concept', 'Materiality concept', 'Objectivity concept']
CH02_ST3 = dict(
    cat='accounting concept',
    terms=[
        ('Revenue recognition concept', 'Revenue is recorded when a sale is made or a service is rendered, i.e. when the right to receive it is established, not necessarily when cash is received.'),
        ('Matching concept', 'Expenses incurred in a period are set against the revenues earned in that same period to find the profit.'),
        ('Full disclosure concept', 'All material and relevant facts about the financial performance and position must be disclosed completely in the financial statements and notes.'),
        ('Consistency concept', 'The same accounting policies and methods are followed from one period to the next so that results are comparable.'),
        ('Conservatism concept', 'Anticipate no profit but provide for all possible losses; also called the prudence concept.'),
        ('Materiality concept', 'Only items whose knowledge would influence the decisions of users need to be disclosed separately; trivial items may be treated simply.'),
        ('Objectivity concept', 'Accounting transactions are recorded in an objective manner, free from personal bias, and are supported by verifiable documents.'),
    ],
    scen=[('Which accounting concept is followed?', CONC3, [
        ('{f} delivered goods worth ₹80,000 to a customer on 28 March; payment will be received in May. The sale is recorded in March.', 'Revenue recognition concept', 'Revenue is recognised when the sale is made, not when cash is received.'),
        ('{f} records the salary of March, unpaid on 31 March, as an expense of the year ending 31 March.', 'Matching concept', 'Expenses of the period are matched with revenues of the same period.'),
        ('{f} values its closing stock at cost or net realisable value, whichever is lower.', 'Conservatism concept', 'Possible losses are provided for, but profits are not anticipated.'),
        ('{f} creates a provision for doubtful debts at 5% on its debtors.', 'Conservatism concept', 'A provision is made for possible losses.'),
        ('{f} has followed the straight line method of depreciation for many years and continues it this year.', 'Consistency concept', 'The same method is followed year after year.'),
        ('{f} treats a stapler costing ₹150 as an expense of the year instead of showing it as a fixed asset.', 'Materiality concept', 'The amount is too small to influence decisions.'),
        ('{f} gives notes in its accounts about a pending court case that could cost it ₹12 lakh.', 'Full disclosure concept', 'All material information is disclosed in the statements or notes.'),
        ('{f} records every purchase on the basis of the supplier\'s invoice, not the manager\'s estimate.', 'Objectivity concept', 'Recording is based on verifiable documents.'),
        ('Commission of ₹6,000 earned by {f} in March but received in April is shown as income of March.', 'Revenue recognition concept', 'Revenue is recorded in the period it is earned.'),
        ('{f} charges the cost of goods sold, not the cost of all goods purchased, against the year\'s sales.', 'Matching concept', 'Costs are matched with the revenue they helped to earn.'),
        ('{f} shows its debtors, creditors, loans and contingent liabilities separately in the balance sheet with notes.', 'Full disclosure concept', 'Complete and material information is disclosed.'),
        ('{f} does not record an expected rise in the price of its stock as profit.', 'Conservatism concept', 'Anticipated profits are not recorded.')], None)],
    pairs=[('consistency concept', 'conservatism concept', [
        ('meaning', 'the same methods are followed year after year', 'anticipate no profit but provide for all possible losses'),
        ('purpose', 'to make results of different periods comparable', 'to avoid overstating profit and assets'),
        ('example', 'continuing the same depreciation method every year', 'valuing stock at cost or market price, whichever is lower')])],
    ars=[
        ('Closing stock is valued at cost or net realisable value, whichever is lower.', 'The conservatism concept requires providing for all possible losses but not anticipating profits.', 'a', 'Both true and R explains A.'),
        ('Outstanding expenses are recorded at the end of the year.', 'Under the matching concept, expenses of a period are matched with its revenues.', 'a', 'Both true and R explains A.'),
        ('A firm should change its depreciation method every year to show higher profit.', 'The consistency concept requires the same accounting methods to be followed every year.', 'd', 'A is false; R is true.'),
        ('Revenue is recognised only when cash is received.', 'Revenue is recognised when the right to receive it is established.', 'd', 'A is false: revenue recognition does not wait for cash. R is true.'),
        ('A small item like a pencil sharpener is treated as an expense.', 'According to the materiality concept, items too small to influence decisions need not be treated strictly.', 'a', 'Both true and R explains A.'),
        ('Accounting records should be supported by vouchers.', 'The full disclosure concept requires all material facts to be disclosed.', 'b', 'Both true, but the support of vouchers follows from the objectivity concept, not full disclosure.')],
    tf=('accounting concepts', [
        'Conservatism means providing for all possible losses but not anticipating profits.',
        'Matching concept requires expenses of a period to be set against revenues of the same period.',
        'Consistency improves the comparability of financial statements.',
        'Objectivity requires transactions to be supported by verifiable evidence.'], [
        'Under revenue recognition, a credit sale is recorded only when payment is received.',
        'Conservatism allows a business to record expected profits.',
        'Materiality requires every small item to be shown separately in the balance sheet.',
        'Consistency means changing methods every year to suit the situation.']),
    cases=[
        ('C4', 'D4', 4, 'The accountant of {f}, {c}, (a) recorded as sales an order of ₹2,00,000 received on 30 March for delivery in May; (b) changed from the written down value method to the straight line method without any reason, increasing profit; (c) did not mention in the accounts a large claim filed against the firm.',
         [('Identify the concept violated in each case.', '(a) Revenue recognition (b) Consistency (c) Full disclosure.'),
          ('State the correct treatment of (a).', 'The order is not a sale; revenue is recognised in May when goods are delivered (right to receive arises).')]),
        ('C4', 'D5', 4, '{p}, owner of {f}, expects the price of the stock lying in {his} godown to rise by 20% next month and wants to show the expected gain as this year\'s profit. He also does not want to provide for a debtor who has become insolvent.',
         [('Which concept is he ignoring? Explain it.', 'Conservatism (prudence): anticipate no profit but provide for all possible losses.'),
          ('Advise {him} on both points.', 'Do not record the expected price rise; value stock at cost or net realisable value, whichever is lower. Write off or provide for the doubtful debt.')]),
    ],
)

CH02_ST4 = dict(
    cat='term',
    terms=[
        ('Cash basis of accounting', 'Entries are made only when cash is received or paid, so revenues and expenses are recorded in the period of receipt or payment.'),
        ('Accrual basis of accounting', 'Revenues and costs are recorded in the period in which they are earned or incurred, whether or not cash is received or paid.'),
        ('Accounting standards', 'Written policy documents issued by an expert accounting body or the government covering recognition, measurement, presentation and disclosure of transactions.'),
        ('Ind AS', 'Indian Accounting Standards converged with IFRS and notified by the Ministry of Corporate Affairs for specified companies.'),
        ('IFRS', 'International Financial Reporting Standards issued by the International Accounting Standards Board (IASB).'),
    ],
    pairs=[('cash basis of accounting', 'accrual basis of accounting', [
        ('recording', 'only cash receipts and payments are recorded', 'all revenues and expenses of the period are recorded whether or not cash is received or paid'),
        ('outstanding and prepaid items', 'no outstanding or prepaid items arise', 'outstanding and prepaid expenses and accrued incomes are recorded'),
        ('profit', 'does not show the true profit of the period', 'shows the true profit or loss of the period'),
        ('legal acceptance', 'not accepted under the Companies Act for companies', 'compulsory for companies under the Companies Act, 2013'),
        ('simplicity', 'simple and easy to follow', 'comparatively complex'),
        ('matching', 'does not follow the matching concept', 'follows the matching concept')])],
    lists=[('as_benefit', 'benefits of accounting standards', [
        ('Reliability of financial statements', 'Users can depend on statements prepared under standards.'),
        ('Eliminate variations', 'They reduce the choice of alternative treatments of the same item.'),
        ('Inter-firm and intra-firm comparison', 'Similar methods make results comparable.'),
        ('Assist auditors', 'Auditors can check whether standards have been followed.'),
        ('Help in determining managerial accountability', 'Results prepared on standard lines show the performance of managers.')], 'as_lim'),
        ('as_lim', 'limitations of accounting standards', [
        ('Difficulty in choosing between alternatives', 'Some standards still allow more than one treatment.'),
        ('Rigidity', 'Standards may be rigid and not suit every situation.'),
        ('Cannot override the law', 'Standards are framed within, and cannot override, the statute.')], 'as_benefit')],
    scen=[('Which basis of accounting is followed?', ['Cash basis of accounting', 'Accrual basis of accounting', 'Hybrid basis of accounting', 'Single entry system'], [
        ('Dr {p}, a doctor in {c}, records fees only when patients pay, and expenses only when {he} pays them.', 'Cash basis of accounting', 'Only actual cash receipts and payments are recorded.'),
        ('{f} records March rent of ₹20,000 as an expense of March although it will be paid in April.', 'Accrual basis of accounting', 'Expenses are recorded when incurred, whether paid or not.'),
        ('{f} shows commission earned but not yet received as income of the current year.', 'Accrual basis of accounting', 'Income is recorded when earned.'),
        ('A small tuition centre run by {p} records only money actually received from students and actual payments made.', 'Cash basis of accounting', 'Entries are made only on receipt or payment of cash.')], None)],
    ars=[
        ('Companies are required to follow the accrual basis of accounting.', 'The Companies Act, 2013 requires companies to maintain accounts on the accrual basis.', 'a', 'Both true and R explains A.'),
        ('Outstanding expenses do not arise under the cash basis of accounting.', 'Under the cash basis, expenses are recorded only when paid.', 'a', 'Both true and R explains A.'),
        ('IFRS are issued by the Institute of Chartered Accountants of India.', 'Ind AS are converged with IFRS.', 'd', 'A is false: IFRS are issued by the IASB. R is true.'),
        ('Accounting standards help in making financial statements comparable.', 'Accounting standards reduce the alternative treatments of the same item.', 'a', 'Both true and R explains A.'),
        ('The cash basis shows the true profit of a period.', 'The cash basis ignores outstanding and accrued items.', 'd', 'A is false: ignoring accrued items means the profit is not the true profit. R is true.')],
    tf=('bases of accounting and accounting standards', [
        'The Accounting Standards Board of the ICAI was set up in 1977.',
        'IFRS are issued by the International Accounting Standards Board.',
        'Ind AS are notified by the Ministry of Corporate Affairs.',
        'AS 2 deals with the valuation of inventories.',
        'AS 1 deals with the disclosure of accounting policies.'], [
        'Accounting standards can override the provisions of law.',
        'Under the cash basis, prepaid expenses are shown in the balance sheet.',
        'IFRS are issued by SEBI.',
        'AS 2 deals with cash flow statements.']),
    cases=[],
)


def c2s4_cash_vs_accrual(r):
    d = ctx(r)
    fees = amt(r, 300000, 900000, 5000)
    unrec = amt(r, 20000, 90000, 1000)
    adv = amt(r, 10000, 50000, 1000)
    exp_paid = amt(r, 100000, fees // 2, 5000)
    outst = amt(r, 10000, 60000, 1000)
    cash_profit = fees - exp_paid
    accr_profit = (fees - adv + unrec) - (exp_paid + outst)
    return {'stem': f'{d["p"]}, a chartered accountant in {d["c"]}, received fees of {inr(fees)} during the year, which include {inr(adv)} received in advance for next year. Fees of {inr(unrec)} earned this year are still to be received. Expenses paid were {inr(exp_paid)} and expenses of {inr(outst)} are outstanding. Find the profit under (i) the cash basis (ii) the accrual basis.',
            'answer': f'(i) {inr(cash_profit)} (ii) {inr(accr_profit)}',
            'key': f'(i) Cash basis: {inr(fees)} − {inr(exp_paid)} = {inr(cash_profit)} (1). (ii) Accrual: income = {inr(fees)} − {inr(adv)} + {inr(unrec)} = {inr(fees - adv + unrec)}; expenses = {inr(exp_paid)} + {inr(outst)} = {inr(exp_paid + outst)}; profit {inr(accr_profit)} (2).'}


def c2s4_accrual_income(r):
    d = ctx(r)
    rec = amt(r, 50000, 200000, 1000)
    acc_ = amt(r, 5000, 30000, 1000)
    adv = amt(r, 2000, 20000, 1000)
    ans = rec + acc_ - adv
    return {'stem': f'{d["f"]} received commission of {inr(rec)} in cash during the year. Of this, {inr(adv)} relates to next year. Commission of {inr(acc_)} earned this year has not yet been received. What commission is credited to the profit and loss account under the accrual basis?',
            'answer': inr(ans), 'key': f'{inr(rec)} − {inr(adv)} + {inr(acc_)} = {inr(ans)}.',
            'distractors': [inr(rec), inr(rec + acc_ + adv), inr(rec - acc_ - adv)]}


GST_HEADS = ['CGST and SGST', 'IGST', 'UTGST', 'Customs duty']
CH02_ST5 = dict(
    cat='GST term',
    terms=[
        ('CGST', 'Tax levied by the Central Government on intra-state supply of goods and services.'),
        ('SGST', 'Tax levied by a State Government on intra-state supply of goods and services within that state.'),
        ('IGST', 'Tax levied and collected by the Central Government on inter-state supply of goods and services and on imports.'),
        ('UTGST', 'Tax levied on supplies within a Union Territory without a legislature, in place of SGST.'),
        ('Input tax credit', 'Credit for the GST paid on purchases (inputs) that a registered dealer can set off against the GST payable on sales.'),
        ('GSTN', 'The not-for-profit company that provides the IT infrastructure for GST registration, returns and payments.'),
    ],
    lists=[('feat', 'features of GST', [
        ('One nation, one tax', 'It replaced many indirect taxes such as excise duty, VAT and service tax with a single tax.'),
        ('Destination-based tax', 'Tax accrues to the state where goods or services are consumed.'),
        ('Dual GST', 'Both the Centre (CGST) and the states (SGST) levy tax on intra-state supplies.'),
        ('Input tax credit across the chain', 'Tax paid on inputs is set off, removing the cascading (tax on tax) effect.'),
        ('IGST on inter-state supplies', 'The Centre collects IGST on supplies between states and shares it with the destination state.'),
        ('Online compliance through GSTN', 'Registration, returns and payments are made online.')], None)],
    scen=[('Which GST is charged on this supply?', GST_HEADS, [
        ('{f} of Jaipur (Rajasthan) sells {g} to a retailer in Udaipur (Rajasthan).', 'CGST and SGST', 'Seller and buyer are in the same state, so it is an intra-state supply.'),
        ('{f} of Pune (Maharashtra) sells {g} to a dealer in Indore (Madhya Pradesh).', 'IGST', 'Supply between two states is an inter-state supply.'),
        ('{f} of Lucknow (Uttar Pradesh) supplies {g} to a shop in Kanpur (Uttar Pradesh).', 'CGST and SGST', 'Both places are in Uttar Pradesh: intra-state supply.'),
        ('{f} of Kochi (Kerala) sends {g} to a buyer in Chennai (Tamil Nadu).', 'IGST', 'Kerala to Tamil Nadu is an inter-state supply.'),
        ('{f} of Chandigarh (Union Territory) sells {g} to a customer within Chandigarh.', 'UTGST', 'Within a Union Territory without a legislature, CGST and UTGST are charged; UTGST replaces SGST.'),
        ('{f} of Surat (Gujarat) sells {g} to a dealer in Ahmedabad (Gujarat).', 'CGST and SGST', 'Same state: intra-state supply.'),
        ('{f} of Patna (Bihar) supplies {g} to a firm in Guwahati (Assam).', 'IGST', 'Supply from Bihar to Assam is inter-state.')], None)],
    ars=[
        ('GST removes the cascading effect of taxes.', 'Input tax credit allows the tax paid on purchases to be set off against tax on sales.', 'a', 'Both true and R explains A.'),
        ('IGST is levied on intra-state supplies.', 'IGST is collected by the Central Government.', 'd', 'A is false: IGST is levied on inter-state supplies. R is true.'),
        ('Input CGST can be set off against output SGST.', 'CGST and SGST are levied by different governments.', 'd', 'A is false: CGST credit cannot be used for SGST. R is true.'),
        ('GST is a destination-based tax.', 'Under GST, tax revenue goes to the state where the goods are consumed.', 'a', 'Both true and R explains A.'),
        ('Input GST paid on purchases is debited to an Input GST account.', 'Input GST is an asset since it can be set off against output tax.', 'a', 'Both true and R explains A.')],
    tf=('Goods and Services Tax', [
        'GST was introduced in India from 1 July 2017.',
        'On an intra-state supply, CGST and SGST are charged at equal rates.',
        'Input tax credit of IGST can be used against IGST, CGST and SGST payable.',
        'GST is a destination-based consumption tax.'], [
        'IGST is charged on supplies within the same state.',
        'Input CGST can be adjusted against output SGST.',
        'GST is levied only by the Central Government.',
        'Under GST, input tax credit is not available to registered dealers.']),
    cases=[],
)


def c2s5_gst_amount(r):
    d = ctx(r)
    val = amt(r, 20000, 400000, 1000)
    rate = r.choice([5, 12, 18, 28])
    intra = r.random() < 0.5
    tax = val * rate / 100
    if intra:
        return {'stem': f'{d["f"]} of {d["c"]} sold goods worth {inr(val)} to a buyer in the same state. GST rate is {rate}%. Calculate the CGST, SGST and the total invoice value.',
                'answer': f'CGST {inr(tax / 2)}, SGST {inr(tax / 2)}, invoice {inr(val + tax)}',
                'key': f'Intra-state: CGST {rate / 2:g}% = {inr(tax / 2)}, SGST {rate / 2:g}% = {inr(tax / 2)}; invoice {inr(val)} + {inr(tax)} = {inr(val + tax)}.'}
    return {'stem': f'{d["f"]} of {d["c"]} sold goods worth {inr(val)} to a buyer in another state. GST rate is {rate}%. Calculate the tax charged and the total invoice value.',
            'answer': f'IGST {inr(tax)}, invoice {inr(val + tax)}',
            'key': f'Inter-state: IGST {rate}% of {inr(val)} = {inr(tax)}; invoice {inr(val + tax)}.'}


def c2s5_payable(r):
    d = ctx(r)
    rate = r.choice([12, 18])
    buy = amt(r, 50000, 300000, 5000)
    sell = buy + amt(r, 20000, 150000, 5000)
    half = rate / 2
    ic, os_ = buy * half / 100, sell * half / 100
    return {'stem': f'{d["f"]} of {d["c"]} bought goods for {inr(buy)} and sold them for {inr(sell)}, both within the same state. GST is {rate}% (CGST {half:g}% + SGST {half:g}%). Find the CGST and SGST payable after input tax credit.',
            'answer': f'CGST {inr(os_ - ic)}, SGST {inr(os_ - ic)}',
            'key': f'Output CGST = {inr(os_)}, input CGST = {inr(ic)}, payable {inr(os_ - ic)}; SGST the same: {inr(os_ - ic)}.',
            'distractors': [f'CGST {inr(os_)}, SGST {inr(os_)}', f'CGST {inr(ic)}, SGST {inr(ic)}', f'CGST {inr(2 * (os_ - ic))}, SGST nil']}


def c2s5_setoff(r):
    d = ctx(r)
    # IGST credit exceeds IGST output; excess used against CGST then SGST
    in_i = amt(r, 20000, 60000, 1000)
    out_i = amt(r, 5000, in_i - 5000, 1000)
    out_c = amt(r, 10000, 40000, 1000)
    out_s = out_c
    in_c = amt(r, 2000, out_c - 3000, 1000)
    in_s = in_c
    left = in_i - out_i
    c_after = out_c - in_c
    use_c = min(left, c_after)
    left2 = left - use_c
    c_pay = c_after - use_c
    s_after = out_s - in_s
    use_s = min(left2, s_after)
    s_pay = s_after - use_s
    carry = left2 - use_s
    tail = f'; IGST credit of {inr(carry)} carried forward' if carry else ''
    return {'stem': f'{d["f"]} has: output IGST {inr(out_i)}, output CGST {inr(out_c)}, output SGST {inr(out_s)}; input IGST {inr(in_i)}, input CGST {inr(in_c)}, input SGST {inr(in_s)}. Using the input tax credit rules (IGST credit first against IGST, then CGST, then SGST), find the net CGST and SGST payable.',
            'answer': f'IGST nil, CGST {inr(c_pay)}, SGST {inr(s_pay)}{tail}',
            'key': f'IGST credit {inr(in_i)} − output IGST {inr(out_i)} = {inr(left)} left. CGST: {inr(out_c)} − {inr(in_c)} = {inr(c_after)}, less IGST credit {inr(use_c)} = {inr(c_pay)}. SGST: {inr(out_s)} − {inr(in_s)} = {inr(s_after)}, less remaining IGST credit {inr(use_s)} = {inr(s_pay)}{tail}.'}


def c2s5_journal(r):
    d = ctx(r)
    val = amt(r, 20000, 200000, 1000)
    rate = r.choice([5, 12, 18])
    t = val * rate / 200
    sup_ = firm(r)
    return {'stem': f'Pass the journal entry in the books of {d["f"]}, {d["c"]}: purchased goods for {inr(val)} from {sup_} of the same state on credit, plus CGST and SGST at {rate / 2:g}% each.',
            'answer': f'Purchases A/c Dr {inr(val)}; Input CGST A/c Dr {inr(t)}; Input SGST A/c Dr {inr(t)}; To {sup_} {inr(val + 2 * t)}',
            'key': f'Purchases debited {inr(val)} (1); input CGST and SGST {inr(t)} each debited (1); supplier credited with {inr(val + 2 * t)} (1).'}


FAMILIES.update({
    S + '02-st1': facts(CH02_ST1),
    S + '02-st2': facts(CH02_ST2),
    S + '02-st3': facts(CH02_ST3),
    S + '02-st4': facts(CH02_ST4) + [FF('C3', 'D3', 'numerical', c2s4_cash_vs_accrual, marks=3, kinds=('m3',)),
                                      FF('C3', 'D2', 'numerical', c2s4_accrual_income, marks=2),
                                      FF('C4', 'D3', 'numerical', c2s4_cash_vs_accrual, marks=3)],
    S + '02-st5': facts(CH02_ST5) + [FF('C3', 'D2', 'numerical', c2s5_gst_amount, marks=2), FF('C3', 'D3', 'numerical', c2s5_payable, marks=2),
                                      FF('C4', 'D4', 'numerical', c2s5_setoff, marks=4, kinds=('m4',)), FF('C3', 'D3', 'numerical', c2s5_journal, marks=3, kinds=('m3',))],
})
