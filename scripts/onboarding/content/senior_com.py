"""Senior (grades 11-12) slot banks for Accountancy, Business, Economics and Applied Mathematics.

Shared items with keyword refs (dsl.K) per board; {board: S(...)} entries are board swaps. Grade 11 prerequisites
point at grade 10 subjects (CBSE and IB Social Science, Cambridge Geography or Maths), grade 12 at grade 11.
IB has no Accountancy, so accountancy refs carry only CBSE and Cambridge.
"""
from dsl import S, K

SS10 = {'cbse': 'social-science', 'cambridge': 'geography', 'ib': 'social-science'}
ACC10 = {'cbse': 'social-science', 'cambridge': 'maths'}
APPLIED11 = {'cbse': 'applied-maths', 'cambridge': 'maths', 'ib': 'applied-maths'}

# ---------------------------------------------------------------- Accountancy
ACCOUNTANCY_PRE_G11 = [
    S(K(10, ACC10, {'cbse': 'credit', 'cambridge': 'interest|money'}), 'Interest on loans and savings', [
        ('A loan of 20 000 is taken at 10% simple interest per year. How much interest is due after 2 years?', '4 000',
         ['2 000', '24 000', '4 200'], '20 000 x 0.10 x 2'),
    ]),
    S(K(10, ACC10, {'cbse': 'credit|money', 'cambridge': 'profit|money'}), 'Profit, loss and percentages', [
        ('A trader buys goods for 800 and sells them for 1 000. What is the profit?', '200', ['1 800', '20%', '80'], 'Selling price - cost price'),
        ('Goods costing 1 200 are sold at a 25% profit. What is the selling price?', '1 500', ['1 225', '900', '1 250'], '1 200 x 1.25'),
    ]),
    S(K(10, ACC10, {'cbse': 'formal and informal|credit', 'cambridge': 'money|managing'}), 'Banks, credit and collateral', [
        ('Something a borrower pledges to a lender as security for a loan is called', 'collateral', ['interest', 'a deposit', 'a cheque'],
         'The lender can sell it if the loan is not repaid'),
        ('Why do formal lenders such as banks usually charge less interest than informal moneylenders?', 'They are regulated and can spread risk across many borrowers',
         ['They lend only to friends', 'They never need repayment', 'They print their own money'], 'Regulation limits interest rates'),
        ('A family borrows from a moneylender at 5% per month. Roughly what annual rate is this?', 'about 60% a year',
         ['5% a year', '12% a year', '0.4% a year'], '5 x 12 months'),
    ]),
    S(K(10, {'cbse': 'maths', 'cambridge': 'maths'}, {'cbse': 'mean of grouped|mean', 'cambridge': 'frequency|histogram'}), 'Reading data and averages', [
        ('A shop sold 12, 15, 9 and 14 items over four days. What is the mean daily sale?', '12.5', ['12', '50', '14'], '50 ÷ 4'),
        ('Sales rose from 40 000 to 50 000. What is the percentage increase?', '25%', ['20%', '10%', '80%'], '10 000 ÷ 40 000'),
        ('Monthly costs were 30, 30, 30 and 90 (thousands). Why is the median a better summary than the mean here?', 'The single large value pulls the mean up',
         ['The median is always larger', 'The mean cannot be calculated', 'There are too few values for a mean'], 'Medians resist outliers'),
    ]),
]

ACCOUNTANCY_CUR_G11 = [
    S(K(11, 'accountancy', 'accounting equation|double-entry|double entry|accounting system'), 'The accounting equation', [
        ('The accounting equation is', 'Assets = Liabilities + Capital', ['Assets = Capital - Liabilities', 'Capital = Assets + Liabilities',
                                                                           'Liabilities = Assets + Capital'], 'What the business owns is financed by others or the owner'),
        ('A business has assets of 90 000 and liabilities of 25 000. What is the capital?', '65 000', ['115 000', '25 000', '90 000'],
         '90 000 - 25 000'),
        ('The owner introduces 10 000 cash into the business. What happens to the equation?', 'Assets and capital both rise by 10 000',
         ['Assets rise, liabilities fall', 'Only capital rises', 'Assets fall by 10 000'], 'Both sides change equally'),
    ]),
    S(K(11, 'accountancy', 'debit and credit|rules of debit|ledger|double'), 'Rules of debit and credit', [
        ('An increase in an asset is recorded as a', 'debit', ['credit', 'neither', 'liability'], 'Assets increase on the debit side'),
        ('Goods are bought on credit from Ravi. Which account is credited?', "Ravi's account", ['Purchases account', 'Cash account', 'Sales account'],
         'Ravi becomes a creditor'),
        ('Rent of 5 000 is paid by cheque. What is the double entry?', 'Debit Rent, credit Bank', ['Debit Bank, credit Rent', 'Debit Rent, credit Cash',
                                                                                                 'Debit Capital, credit Rent'],
         'Expense increases, bank decreases'),
    ]),
    S(K(11, 'accountancy', 'journal|books of prime entry|prime entry|cash book'), 'Books of original entry', [
        ('Credit sales of goods are first recorded in the', 'sales journal (sales day book)', ['purchases journal', 'cash book', 'trial balance'],
         'A book of prime entry'),
        ('Which book records both cash and bank receipts and payments?', 'a two-column cash book', ['the general journal only', 'the sales journal', 'the balance sheet'],
         'It acts as both a journal and a ledger'),
        ('A contra entry in a two-column cash book occurs when', 'cash is deposited into or withdrawn from the bank',
         ['goods are sold on credit', 'a debtor pays by cheque', 'depreciation is charged'], 'Both sides are within the cash book'),
    ]),
    S(K(11, 'accountancy', 'trial balance'), 'The trial balance and errors', [
        ('A trial balance is prepared to', 'check that total debits equal total credits', ['calculate profit', 'pay taxes', 'record sales'],
         'An arithmetical check of the ledger'),
        ('Which error will NOT be revealed by a trial balance?', 'An entry completely omitted from the books', ['A debit entered as 500 and credit as 50',
                                                                                                                 'A balance left out of the trial balance', 'A ledger total added wrongly'],
         'Errors of omission keep the totals equal'),
        ('Repairs to machinery of 3 000 were debited to the Machinery account. What type of error is this?', 'error of principle',
         ['error of omission', 'compensating error', 'error of original entry'], 'Revenue expenditure was treated as capital'),
    ]),
]

ACCOUNTANCY_PRE_G12 = [
    S(K(11, 'accountancy', 'trial balance'), 'Trial balance', [
        ('In a trial balance, which balance appears on the credit side?', 'capital', ['drawings', 'machinery', 'rent paid'],
         'Capital is owed to the owner'),
    ]),
    S(K(11, 'accountancy', 'depreciation'), 'Depreciation', [
        ('Depreciation is', 'the fall in value of a fixed asset over its useful life', ['an increase in asset value', 'a cash payment to the bank',
                                                                                        'a type of income'], 'Matching cost to periods'),
        ('A machine costs 50 000, will last 5 years and has no scrap value. What is the straight-line depreciation per year?', '10 000',
         ['5 000', '50 000', '25 000'], '50 000 ÷ 5'),
    ]),
    S(K(11, 'accountancy', 'financial statements|final accounts|income statement|trading'), 'Financial statements', [
        ('Gross profit is', 'sales minus cost of goods sold', ['sales minus all expenses', 'assets minus liabilities', 'capital plus drawings'],
         'From the trading account'),
        ('Sales are 200 000, cost of sales 120 000 and expenses 50 000. What is the net profit?', '30 000', ['80 000', '70 000', '150 000'],
         'Gross profit 80 000 minus expenses'),
        ('Why does the balance sheet always balance?', 'Every transaction has equal debit and credit effects on the accounting equation',
         ['Accountants add a balancing figure', 'Profit is always zero', 'Assets always equal sales'], 'Double entry'),
    ]),
    S(K(11, 'accountancy', 'accrual|prepayment|adjustment|bank reconciliation'), 'Adjustments: accruals and prepayments', [
        ('Rent owing at the year end is an', 'accrued expense (a liability)', ['asset', 'income', 'capital'], 'It has been used but not yet paid'),
        ('Insurance of 12 000 is paid for 12 months on 1 October. The year ends 31 December. How much is prepaid?', '9 000',
         ['3 000', '12 000', '6 000'], '9 months relate to next year'),
        ('Why are accruals and prepayments adjusted at the year end?', 'So that income and expenses match the period they belong to',
         ['To reduce tax to zero', 'To hide losses', 'Because the bank asks for it'], 'The matching (accruals) concept'),
    ]),
]

ACCOUNTANCY_CUR_G12 = [
    S(K(12, 'accountancy', 'partnership deed|profit sharing|partnership'), 'Partnership basics', [
        ('In the absence of a partnership deed, profits are shared', 'equally', ['in the ratio of capitals', 'by age', 'only by the senior partner'],
         'Default rule'),
        ('A and B share profits 3:2. The profit is 50 000. What is B\'s share?', '20 000', ['30 000', '25 000', '10 000'], '2/5 of 50 000'),
        ('A has capital of 100 000 and interest on capital is 8%. Profit before appropriation is only 5 000. What does A receive as interest?',
         '5 000', ['8 000', '0', '13 000'], 'Interest on capital is limited to available profit unless the deed says otherwise'),
    ]),
    S(K(12, 'accountancy', 'goodwill'), 'Goodwill', [
        ('Goodwill is', 'the value of a business\'s reputation and customer base', ['cash in hand', 'a current liability', 'the value of stock'],
         'An intangible asset'),
        ('Average profits are 40 000. Goodwill is valued at 2 years\' purchase. What is goodwill?', '80 000', ['20 000', '40 000', '42 000'],
         '40 000 x 2'),
        ('Why is goodwill usually valued when a new partner is admitted?', 'Existing partners are compensated for the profits the business already earns',
         ['To increase the tax bill', 'Because it is required every year', 'To reduce capital'], 'The newcomer shares future profits'),
    ]),
    S(K(12, 'accountancy', 'admission|revaluation|reconstitution|partnership changes'), 'Admission of a partner', [
        ('When a new partner joins, the old partnership is', 'reconstituted', ['dissolved and closed', 'converted to a company', 'unchanged'],
         'A new agreement begins'),
        ('A and B share 1:1. C joins for a 1/4 share, taken equally from A and B. What is the new ratio A:B:C?', '3 : 3 : 2',
         ['1 : 1 : 1', '2 : 2 : 1', '3 : 3 : 1'], 'Each keeps 3/8; C has 2/8'),
        ('Assets are revalued on admission because', 'gains and losses up to that date belong to the old partners',
         ['the new partner sets the values', 'it is a tax rule', 'assets always increase'], 'Revaluation account'),
    ]),
    S(K(12, 'accountancy', 'share capital|shares|limited compan|issue of shares'), 'Company share capital', [
        ('Owners of a company are its', 'shareholders', ['debenture holders', 'creditors', 'directors only'], 'They hold its shares'),
        ('1 000 shares of 10 each are issued at a premium of 2. How much goes to the securities premium?', '2 000', ['10 000', '12 000', '1 000'],
         '1 000 x 2'),
        ('Why is a debenture different from a share?', 'Debenture holders are lenders paid fixed interest; shareholders are owners paid dividends',
         ['Debentures give voting rights', 'Shares must be repaid on a fixed date', 'They are the same'], 'Debt versus equity'),
    ]),
]

# ---------------------------------------------------------------- Business
BUSINESS_PRE_G11 = [
    S(K(10, SS10, {'cbse': 'sectors', 'cambridge': 'employment structure|sectors', 'ib': 'globalisation|trade'}), 'Sectors of economic activity', [
        ('A bank and a hospital belong to which sector?', 'tertiary (services)', ['primary', 'secondary', 'quaternary only'], 'They provide services'),
    ]),
    S(K(10, SS10, {'cbse': 'globalisation', 'cambridge': 'transnational|globalisation', 'ib': 'globalisation'}), 'Globalisation and multinational companies', [
        ('A company that owns or controls production in more than one country is a', 'multinational corporation (MNC)',
         ['sole trader', 'cooperative society', 'public sector unit only'], 'Also called a TNC'),
        ('Why do MNCs often set up factories in countries with lower wages?', 'To reduce production costs and stay competitive',
         ['To pay more tax', 'Because they must by law', 'To avoid selling there'], 'Cost advantage'),
    ]),
    S(K(10, SS10, {'cbse': 'consumer', 'cambridge': 'transnational|globalisation', 'ib': 'trade|fair'}), 'Consumers and fair trade', [
        ('A product label must show its MRP in India. MRP stands for', 'maximum retail price', ['minimum resale price', 'market rate price',
                                                                                                  'monthly retail payment'], 'Consumers cannot be charged more'),
        ('Why do consumers need protection laws?', 'Sellers may know more than buyers and could mislead them',
         ['Consumers always have full information', 'Prices are fixed by nature', 'Shops are owned by the state'], 'Information gaps'),
        ('Fair-trade labelling mainly aims to', 'guarantee producers in poorer countries a fair price', ['make goods cheaper for buyers',
                                                                                                         'ban imports', 'increase advertising'],
         'Ethical trade'),
    ]),
    S(K(10, SS10, {'cbse': 'credit|money', 'cambridge': 'development', 'ib': 'development'}), 'Development and living standards', [
        ('Which indicator best measures average income in a country?', 'GNI (or GDP) per capita', ['total population', 'land area', 'number of cities'],
         'Income per person'),
        ('Why is HDI considered a broader measure of development than income alone?', 'It also includes health and education',
         ['It counts only rich people', 'It ignores income', 'It measures only exports'], 'Life expectancy, schooling and income'),
        ('Country A has higher income per head than B, but lower life expectancy and literacy. What does this suggest?',
         'Income alone does not show overall well-being', ['A is more developed in every way', 'B must be poorer in all respects',
                                                           'Data must be wrong'], 'Development is multi-dimensional'),
    ]),
]

BUSINESS_CUR_G11 = [
    S(K(11, 'business', 'business activit|classification of business|enterprise|introduction to business'), 'Business activity and enterprise', [
        ('A person who takes the risk of starting a business is an', 'entrepreneur', ['employee', 'auditor', 'consumer'], 'They combine resources'),
        ('Which is an example of a secondary-sector business?', 'a car factory', ['a fish farm', 'a bank', 'a school'], 'Manufacturing'),
        ('Why do many new businesses fail in their first years?', 'Poor cash flow and a lack of experience or market research',
         ['They make too much profit', 'They have too many customers', 'Governments ban them'], 'Cash and planning problems'),
    ]),
    S(K(11, 'business', 'sole proprietor|sole trader|forms of business|business structure|types of business'), 'Forms of business organisation', [
        ('A business owned and run by one person is a', 'sole proprietorship (sole trader)', ['partnership', 'public company', 'cooperative'],
         'One owner'),
        ('What does limited liability mean?', 'Owners can lose only what they invested', ['Owners pay unlimited debts', 'The business cannot borrow',
                                                                                          'Profits are limited by law'], 'Personal assets are protected'),
        ('Why might a growing partnership convert into a private limited company?', 'To raise more capital and protect owners with limited liability',
         ['To pay more tax', 'To have only one owner', 'To avoid keeping accounts'], 'Growth and risk'),
    ]),
    S(K(11, 'business', 'objective'), 'Business objectives', [
        ('The most common objective of a new small business is', 'survival', ['market leadership', 'social responsibility only', 'global expansion'],
         'It must first stay open'),
        ('A SMART objective must be', 'specific, measurable, achievable, realistic and time-bound', ['simple and short', 'secret',
                                                                                                     'set only by employees'], 'Clear targets'),
        ('Why might a social enterprise not aim to maximise profit?', 'Its main aim is a social or environmental goal',
         ['It is not allowed to make any profit', 'It has no customers', 'It is owned by the government'], 'Profit supports the mission'),
    ]),
    S(K(11, 'business', {'cbse': 'social responsibilit', 'cambridge': 'stakeholder', 'ib': 'stakeholder'}), 'Stakeholders', [
        ('Which group is an internal stakeholder?', 'employees', ['customers', 'suppliers', 'the government'], 'They are inside the business'),
        ('Why might local residents object to a new factory?', 'Noise, traffic and pollution could affect them', ['They will get jobs', 'Prices will fall',
                                                                                                                'They own shares'], 'External costs'),
        ('Shareholders want higher dividends and workers want higher pay. This is an example of', 'stakeholder conflict',
         ['stakeholder agreement', 'diversification', 'vertical integration'], 'Objectives clash'),
    ]),
]

BUSINESS_PRE_G12 = [
    S(K(11, 'business', {'cbse': 'social responsibilit', 'cambridge': 'stakeholder', 'ib': 'stakeholder'}), 'Stakeholders and conflict', [
        ('Which stakeholder is mainly interested in prompt payment for goods supplied?', 'suppliers', ['employees', 'shareholders', 'customers'],
         'They want to be paid on time'),
    ]),
    S(K(11, 'business', 'objective'), 'Business objectives and growth', [
        ('A merger is', 'two businesses joining to form one', ['a business closing', 'a new product launch', 'a price cut'], 'Combining firms'),
        ('A cement firm buys a limestone quarry. This is', 'backward vertical integration', ['horizontal integration', 'conglomerate integration',
                                                                                              'forward vertical integration'], 'Buying a supplier'),
    ]),
    S(K(11, 'business', 'human resource|motivation|hrm'), 'Human resource management and motivation', [
        ('Recruiting from within the business is called', 'internal recruitment', ['external recruitment', 'outsourcing', 'redundancy'],
         'Existing staff apply'),
        ("In Maslow's hierarchy, which need comes first?", 'physiological needs', ['self-actualisation', 'esteem', 'social needs'],
         'Food, water and shelter'),
        ("According to Herzberg, why may a pay rise alone not motivate workers for long?", 'Pay is a hygiene factor; motivation needs recognition and responsibility',
         ['Pay is a motivator that never fades', 'Workers dislike money', 'Pay is not part of his theory'], 'Hygiene factors prevent dissatisfaction'),
    ]),
    S(K(11, 'business', 'business services|finance|sources of finance|banking'), 'Business finance and services', [
        ('A short-term source of finance is', 'a bank overdraft', ['issuing shares', 'a 20-year mortgage', 'retained profits over decades'],
         'Flexible borrowing'),
        ('Insurance helps a business by', 'spreading the risk of loss for a premium', ['removing all risks', 'increasing sales', 'paying wages'],
         'Pooling of risk'),
        ('Why might a start-up prefer venture capital to a bank loan?', 'No fixed repayments, and investors bring expertise, in return for a share',
         ['Venture capital is free money', 'Banks never lend', 'It avoids sharing ownership'], 'Equity versus debt'),
    ]),
]

BUSINESS_CUR_G12 = [
    S(K(12, 'business', {'cbse': 'marketing mix|marketing', 'cambridge': 'marketing planning|marketing strategy', 'ib': 'marketing mix|seven ps|marketing'}), 'The marketing mix', [
        ('The 4 Ps of the marketing mix are product, price, place and', 'promotion', ['profit', 'people only', 'production'], 'Classic 4 Ps'),
        ('Selling a new product at a low price to win market share quickly is', 'penetration pricing', ['price skimming', 'cost-plus pricing',
                                                                                                         'premium pricing'], 'Low entry price'),
        ('Why might a luxury brand avoid discount retailers?', 'It could damage the premium image of the brand', ['Discount shops sell too much',
                                                                                                                   'It is illegal', 'It lowers costs'],
         'Place must fit the brand'),
    ]),
    S(K(12, 'business', 'market research|segment|sales forecast|concept of marketing|marketing'), 'Market research and segmentation', [
        ('Information collected first-hand by the business is', 'primary research', ['secondary research', 'desk research', 'published data'],
         'Surveys, interviews, observation'),
        ('Dividing a market into groups with similar needs is', 'market segmentation', ['market saturation', 'diversification', 'outsourcing'],
         'Target marketing'),
        ('A firm surveys only its existing loyal customers about a new product. What is the main problem?', 'The sample is biased',
         ['It is too expensive', 'It is secondary data', 'It is too random'], 'Non-customers are left out'),
    ]),
    S(K(12, 'business', {'cbse': 'principles of management|planning|management', 'cambridge': 'chain of command|hierarchy|delegation', 'ib': 'leadership|management|operations'}), 'Management and planning', [
        ('Deciding in advance what to do and how to do it is', 'planning', ['controlling', 'staffing', 'directing'], 'First function of management'),
        ("Fayol's principle of 'unity of command' means", 'each employee should receive orders from only one boss', ['everyone gives orders',
                                                                                                                    'all decisions are made by workers',
                                                                                                                    'there is one company goal'],
         'Avoids confusion'),
        ('Why might a manager choose a democratic leadership style for a creative team?', 'Involving staff in decisions can improve ideas and motivation',
         ['It is always fastest', 'It removes responsibility', 'It needs no communication'], 'Participation'),
    ]),
    S(K(12, 'business', 'business environment|external influences|steep|pest|international|external'), 'The external business environment', [
        ('A rise in interest rates is an example of which external factor?', 'economic', ['social', 'technological', 'legal'], 'PEST'),
        ('A weaker rupee usually helps', 'exporters', ['importers', 'all businesses equally', 'no businesses'], 'Exports become cheaper abroad'),
        ('Why might new data-protection laws increase costs for online retailers?', 'They must change systems and train staff to comply',
         ['They lose all customers', 'They must stop selling', 'Laws lower costs'], 'Compliance costs'),
    ]),
]

# ---------------------------------------------------------------- Economics
ECONOMICS_PRE_G11 = [
    S(K(10, SS10, {'cbse': 'development', 'cambridge': 'indicators of development|development', 'ib': 'measuring development|development'}),
      'Measuring development', [
        ('Per capita income is', 'total national income divided by population', ['income of the richest person', 'total exports',
                                                                                  'average price of goods'], 'Average income'),
    ]),
    S(K(10, SS10, {'cbse': 'sectors', 'cambridge': 'employment structure|sectors', 'ib': 'inequality|development'}), 'Sectors and employment', [
        ('Farming and mining are part of the', 'primary sector', ['secondary sector', 'tertiary sector', 'service sector'], 'Natural resources'),
        ('As countries develop, the share of workers in the tertiary sector usually', 'rises', ['falls to zero', 'stays exactly the same', 'disappears'],
         'Services grow'),
    ]),
    S(K(10, SS10, {'cbse': 'globalisation', 'cambridge': 'globalisation|transnational', 'ib': 'globalisation|trade'}), 'Trade and globalisation', [
        ('Goods bought from other countries are', 'imports', ['exports', 'subsidies', 'tariffs'], 'Coming in'),
        ('A tax on imported goods is a', 'tariff', ['quota', 'subsidy', 'dividend'], 'It makes imports dearer'),
        ('Why might cheaper imported toys harm small domestic toy makers?', 'Consumers may switch to the cheaper imports',
         ['Imports raise domestic prices', 'Domestic makers get subsidies automatically', 'Toys cannot be traded'], 'Competition'),
    ]),
    S(K(10, SS10, {'cbse': 'money', 'cambridge': 'development', 'ib': 'development|inequality'}), 'Money, credit and inequality', [
        ('Money solves the problem of the double coincidence of wants because it', 'is a medium of exchange', ['is made of paper', 'has no value',
                                                                                                                'is only used by banks'], 'Barter needs matching wants'),
        ('Which is a likely effect of rising inequality?', 'A larger gap between rich and poor households', ['Everyone earns the same', 'Prices fall for everyone',
                                                                                                             'Unemployment disappears'], 'Distribution widens'),
        ('Why can easy access to cheap credit help poor rural families?', 'They can invest in seeds or tools without falling into debt traps',
         ['It removes all risk', 'They never need to repay', 'It raises moneylender rates'], 'Formal credit is cheaper'),
    ]),
]

ECONOMICS_CUR_G11 = [
    S(K(11, 'economics', 'production possibilit|opportunity cost'), 'Scarcity, choice and the PPF', [
        ('The basic economic problem arises because', 'wants are unlimited but resources are scarce', ['resources are unlimited', 'money is scarce only',
                                                                                                         'people want nothing'], 'Scarcity forces choice'),
        ('The next best alternative given up when making a choice is the', 'opportunity cost', ['marginal cost', 'sunk cost', 'fixed cost'],
         'Cost of the forgone option'),
        ('A point inside a production possibility frontier shows', 'unemployed or inefficiently used resources', ['an unattainable output',
                                                                                                                    'maximum efficiency', 'economic growth'],
         'More could be produced'),
    ]),
    S(K(11, 'economics', 'demand'), 'Demand and its determinants', [
        ('The law of demand says that as price falls, quantity demanded', 'rises', ['falls', 'stays the same', 'becomes zero'], 'Other things equal'),
        ('A rise in income increases demand for a normal good. On a graph, this', 'shifts the demand curve to the right',
         ['moves along the curve', 'shifts the supply curve', 'has no effect'], 'A change in a non-price factor'),
        ('The price of tea rises. What happens to demand for coffee and for sugar?', 'Coffee demand rises; sugar demand falls',
         ['Both rise', 'Both fall', 'Coffee falls; sugar rises'], 'Coffee is a substitute, sugar a complement'),
    ]),
    S(K(11, 'economics', 'market equilibrium|equilibri'), 'Market equilibrium', [
        ('At equilibrium, quantity demanded', 'equals quantity supplied', ['exceeds supply', 'is zero', 'is less than supply'], 'Market clears'),
        ('If price is below equilibrium there is', 'excess demand (a shortage)', ['excess supply', 'equilibrium', 'a surplus'],
         'Buyers want more than is offered'),
        ('A government sets a maximum rent below the equilibrium. What is the likely result?', 'A shortage of rental housing',
         ['A surplus of housing', 'Rents rise above equilibrium', 'No effect'], 'Price ceiling'),
    ]),
    S(K(11, 'economics', 'elasticity'), 'Price elasticity', [
        ('If demand is price elastic, a price rise causes', 'a proportionately larger fall in quantity demanded',
         ['a smaller fall', 'no change', 'a rise in quantity demanded'], 'PED > 1'),
        ('Price rises by 10% and quantity demanded falls by 5%. What is PED?', '-0.5', ['-2', '-5', '-0.05'], '-5% ÷ 10%'),
        ('Why is demand for salt usually price inelastic?', 'It is a necessity with few substitutes and a small share of income',
         ['It is a luxury', 'It has many substitutes', 'It is very expensive'], 'Determinants of PED'),
    ]),
]

ECONOMICS_PRE_G12 = [
    S(K(11, 'economics', 'demand'), 'Shifts in demand and supply', [
        ('A bad harvest reduces the supply of wheat. What happens to price and quantity?', 'Price rises, quantity falls',
         ['Price falls, quantity rises', 'Both rise', 'Both fall'], 'Supply shifts left'),
    ]),
    S(K(11, 'economics', 'elasticity'), 'Elasticity', [
        ('A good with PED of -0.2 is', 'price inelastic', ['price elastic', 'unit elastic', 'perfectly elastic'], '|PED| < 1'),
        ('A firm faces inelastic demand. What happens to total revenue if it raises price?', 'It rises', ['It falls', 'It stays the same', 'It becomes zero'],
         'Quantity falls proportionately less'),
    ]),
    S(K(11, 'economics', 'production function|short-run and long-run|types of cost|factors of production|cost'), 'Costs and production', [
        ('Rent for a factory that does not change with output is a', 'fixed cost', ['variable cost', 'marginal cost', 'revenue'], 'Independent of output'),
        ('Total cost is 500 at 10 units and 560 at 11 units. What is the marginal cost of the 11th unit?', '60', ['56', '50', '1060'], '560 - 500'),
        ('Why does marginal product eventually fall as more workers are added to a fixed machine?', 'The law of diminishing returns',
         ['Workers become lazy', 'Machines get faster', 'Prices fall'], 'Fixed factor constrains output'),
    ]),
    S(K(11, 'economics', 'perfect competition|monopoly|market structure|resource allocation|theory of the firm'), 'Market structures and allocation', [
        ('In perfect competition, firms are', 'price takers', ['price makers', 'monopolies', 'state owned'], 'Many small firms, identical goods'),
        ('A market with only one seller is a', 'monopoly', ['oligopoly', 'perfect competition', 'duopoly'], 'Single supplier'),
        ('Why can a monopoly charge a higher price than a competitive firm?', 'It faces no close competitors, so buyers cannot switch easily',
         ['It has higher costs by law', 'Consumers prefer high prices', 'It must by regulation'], 'Market power'),
    ]),
]

ECONOMICS_CUR_G12 = [
    S(K(12, 'economics', 'national income|gdp|economic activity|circular flow'), 'National income and GDP', [
        ('GDP measures', 'the value of all final goods and services produced in a country in a year', ['only exports', 'government spending only',
                                                                                                        'money in banks'], 'Domestic output'),
        ('Why is real GDP better than nominal GDP for comparing output over time?', 'It removes the effect of price changes', ['It includes inflation',
                                                                                                                                 'It counts only services',
                                                                                                                                 'It is always larger'],
         'Adjusted for inflation'),
        ('Nominal GDP grows 8% while prices rise 5%. Roughly what is real growth?', '3%', ['13%', '8%', '1.6%'], '8% - 5%'),
    ]),
    S(K(12, 'economics', 'inflation'), 'Inflation', [
        ('Inflation is', 'a sustained rise in the general price level', ['a fall in prices', 'a rise in one price', 'an increase in output'],
         'Measured by a price index'),
        ('Inflation caused by rising costs of production is', 'cost-push inflation', ['demand-pull inflation', 'deflation', 'stagflation only'],
         'Higher input costs'),
        ('Why does unexpected inflation hurt savers with fixed interest?', 'The real value of their savings falls', ['Their savings grow faster',
                                                                                                                       'Prices stay the same', 'Banks pay more'],
         'Money buys less'),
    ]),
    S(K(12, 'economics', 'money and banking|monetary|central bank|money'), 'Money, banking and monetary policy', [
        ("India's central bank is the", 'Reserve Bank of India', ['State Bank of India', 'Finance Ministry', 'SEBI'], 'Bank of issue'),
        ('To reduce inflation, a central bank is likely to', 'raise interest rates', ['cut interest rates', 'print more money', 'lower reserve ratios'],
         'Contractionary monetary policy'),
        ('How does a higher cash reserve ratio reduce lending?', 'Banks must hold more deposits as reserves, leaving less to lend',
         ['It forces banks to lend more', 'It raises the money multiplier', 'It cuts interest rates'], 'Lower credit creation'),
    ]),
    S(K(12, 'economics', 'fiscal|government budget|government revenue|budget'), 'Fiscal policy and the budget', [
        ('A budget deficit occurs when', 'government spending exceeds revenue', ['revenue exceeds spending', 'exports exceed imports', 'prices fall'],
         'Government borrows'),
        ('Income tax is an example of a', 'direct tax', ['indirect tax', 'subsidy', 'tariff'], 'Paid directly on income'),
        ('In a recession, why might a government increase spending?', 'To boost aggregate demand and employment', ['To cause inflation on purpose',
                                                                                                                   'To reduce output', 'To raise interest rates'],
         'Expansionary fiscal policy'),
    ]),
]

# ---------------------------------------------------------------- Applied mathematics (Commerce)
APPLIED_CUR_G11 = [
    S(K(11, 'applied-maths', {'cbse': 'logarithm', 'ib': 'scientific notation|approximation'}), 'Numbers: indices, logarithms and approximation', [
        ('Write 45 000 in standard form.', '4.5 x 10⁴', ['45 x 10³', '4.5 x 10³', '0.45 x 10⁵'], 'One digit before the decimal point'),
        ('What is log₁₀ 100 + log₁₀ 10?', '3', ['110', '1000', '20'], '2 + 1'),
        ('A measurement of 5.0 m has an error of 0.2 m. What is the percentage error?', '4%', ['0.04%', '20%', '2.5%'], '0.2 ÷ 5.0 x 100'),
    ]),
    S(K(11, 'applied-maths', 'geometric progression|geometric sequence|geometric'), 'Arithmetic and geometric sequences', [
        ('What is the 6th term of 2, 6, 18, ...?', '486', ['162', '1458', '36'], '2 x 3⁵'),
        ('A salary of 30 000 rises by 2 000 each year. What is it in year 5?', '38 000', ['40 000', '32 000', '10 000'], '30 000 + 4 x 2 000'),
        ('A town of 50 000 grows by 4% a year. Roughly what is its population after 3 years?', '56 243', ['56 000', '52 000', '50 120'],
         '50 000 x 1.04³'),
    ]),
    S(K(11, 'applied-maths', {'cbse': 'interest|financial|annuit|probability', 'ib': 'compound interest|financial'}),
      'Compound interest and depreciation', [
        ('10 000 is invested at 6% compound interest a year. What is it worth after 2 years?', '11 236', ['11 200', '10 600', '12 000'], '10 000 x 1.06²'),
        ('A car bought for 8 lakh depreciates 15% a year. Roughly what is it worth after 2 years?', '5.78 lakh', ['5.6 lakh', '6.8 lakh', '7.7 lakh'],
         '8 x 0.85²'),
        ('Which is better for a saver: 8% compounded yearly or 8% compounded quarterly?', 'Quarterly, because interest is added more often',
         ['Yearly, because the rate is the same', 'They always give the same amount', 'Yearly, because there are fewer payments'], 'Effective rate is higher'),
    ]),
    S(K(11, 'applied-maths', 'correlation|regression|standard deviation'), 'Correlation and spread', [
        ('A correlation coefficient of -0.9 shows', 'a strong negative relationship', ['no relationship', 'a weak positive relationship',
                                                                                         'a perfect positive relationship'], 'Close to -1'),
        ('Two data sets have the same mean, but A has a larger standard deviation. What does this mean?', 'A is more spread out',
         ['A has a higher mean', 'B has more values', 'A is more consistent'], 'Spread about the mean'),
        ('Ice-cream sales and drownings are strongly correlated. Why does this not prove one causes the other?', 'Both may be caused by hot weather',
         ['Correlation always proves causation', 'The data must be wrong', 'Ice cream causes drowning'], 'A third (lurking) variable'),
    ]),
]

APPLIED_PRE_G12 = [
    S(K(11, APPLIED11, 'geometric progression|geometric sequence|geometric'), 'Geometric growth', [
        ('An investment doubles every 6 years. Starting at 5 000, what is it worth after 18 years?', '40 000', ['15 000', '30 000', '20 000'],
         '5 000 x 2³'),
    ]),
    S(K(11, APPLIED11, 'probability'), 'Probability rules', [
        ('Two events A and B are independent, P(A) = 0.3 and P(B) = 0.5. What is P(A and B)?', '0.15', ['0.8', '0.2', '0.65'], 'Multiply'),
        ('P(rain) = 0.3 and P(late | rain) = 0.4. What is P(rain and late)?', '0.12', ['0.7', '0.1', '0.34'], 'P(A and B) = P(A) x P(B | A)'),
    ]),
    S(K(11, APPLIED11, 'standard deviation|variance|dispersion|measures of spread'), 'Measures of spread', [
        ('What is the range of 4, 9, 2, 15, 7?', '13', ['11', '15', '7.4'], '15 - 2'),
        ('What is the variance of 2, 4, 6?', '8/3', ['4', '2', '16/3'], 'Mean 4; (4 + 0 + 4) ÷ 3'),
        ('Every value in a data set is increased by 10. What happens to the standard deviation?', 'It stays the same',
         ['It increases by 10', 'It doubles', 'It falls by 10'], 'Spread does not change'),
    ]),
    S(K(11, APPLIED11, 'binomial distribution|discrete random|correlation|regression'), 'Discrete distributions and regression', [
        ('A fair coin is tossed 4 times. What is the expected number of heads?', '2', ['4', '1', '0.5'], 'np = 4 x 0.5'),
        ('For X ~ B(10, 0.2), what is the variance?', '1.6', ['2', '0.16', '8'], 'np(1 - p)'),
        ('A regression line is y = 2x + 5 for x between 1 and 10. Why is predicting y at x = 50 unreliable?', 'It is extrapolation beyond the data',
         ['The gradient is too small', 'The line passes through zero', 'Regression only works for x = 50'], 'Outside the observed range'),
    ]),
]

APPLIED_CUR_G12 = [
    S(K(12, 'applied-maths', 'poisson|normal distribution|probability distribution|binomial|random variable'), 'Probability distributions', [
        ('A random variable that can take only whole-number values is', 'discrete', ['continuous', 'normal', 'constant'], 'Countable outcomes'),
        ('Calls arrive at a mean rate of 3 per hour. Which distribution models the number of calls in an hour?', 'Poisson', ['Binomial with n = 3',
                                                                                                                                'Uniform', 'Normal with mean 0'],
         'Random events at a constant average rate'),
        ('For a normal distribution with mean 50 and standard deviation 5, about what percentage of values lie between 45 and 55?', '68%',
         ['95%', '50%', '99.7%'], 'Within one standard deviation'),
    ]),
    S(K(12, 'applied-maths', 'sampl|estimat|confidence'), 'Sampling and estimation', [
        ('A sample in which every member of the population has an equal chance of selection is', 'a simple random sample',
         ['a convenience sample', 'a quota sample', 'a census'], 'Equal chance'),
        ('Why do larger samples give more reliable estimates of the mean?', 'The standard error falls as sample size increases',
         ['Larger samples are always biased', 'The mean changes', 'Variance increases'], 'σ/√n'),
        ('A 95% confidence interval for a mean is (48, 52). What is the best estimate of the population mean?', '50', ['48', '52', '95'],
         'The midpoint'),
    ]),
    S(K(12, 'applied-maths', 'hypothesis|t-test|chi'), 'Hypothesis testing', [
        ('The statement assumed true at the start of a hypothesis test is the', 'null hypothesis', ['alternative hypothesis', 'test statistic',
                                                                                                    'critical value'], 'H₀'),
        ('A test at the 5% level gives a p-value of 0.02. What should you conclude?', 'Reject the null hypothesis', ['Accept the null hypothesis',
                                                                                                                   'The test is invalid', 'Increase the p-value'],
         '0.02 < 0.05'),
        ('Rejecting a null hypothesis that is actually true is a', 'Type I error', ['Type II error', 'correct decision', 'sampling frame'],
         'A false positive'),
    ]),
    S(K(12, 'applied-maths', 'linear combination|expected value|expectation|random variable'),
      'Combining random variables and rates of change', [
        ('If E(X) = 4, what is E(3X + 2)?', '14', ['12', '6', '18'], '3 x 4 + 2'),
        ('If Var(X) = 5, what is Var(2X)?', '20', ['10', '5', '25'], 'Var(aX) = a² Var(X)'),
        ('X and Y are independent with Var(X) = 4 and Var(Y) = 9. What is Var(X - Y)?', '13', ['5', '-5', '36'], 'Variances add'),
    ]),
]

# Board swap: CBSE Class 11 Business Studies has no HRM unit (it is in Class 12), so probe forms of organisation instead.
_CBSE_BUS11_COMPANIES = S(K(11, 'business', {'cbse': 'joint stock|cooperative|forms of business'}), 'Companies and cooperatives', [
    ('A cooperative society is formed mainly to', 'serve the common interests of its members', ['maximise profit for one owner', 'run the government',
                                                                                                'sell shares on the stock exchange'], 'Mutual help'),
    ('Which feature belongs to a joint stock company?', 'perpetual succession', ['unlimited liability', 'one owner only', 'no legal identity'],
     'It continues even if members change'),
    ('Why do large projects such as steel plants usually use the company form?', 'It can raise huge capital from many shareholders with limited liability',
     ['It needs no registration', 'Profits go to one person', 'It is never regulated'], 'Scale of capital'),
])
BUSINESS_PRE_G12[2] = {'cbse': _CBSE_BUS11_COMPANIES, 'cambridge': BUSINESS_PRE_G12[2], 'ib': BUSINESS_PRE_G12[2]}

# Board swap: IB Mathematics AI Year 2 has no linear combinations of random variables; probe optimisation instead.
_IB_AI12_OPTIMISE = S(K(12, 'applied-maths', {'ib': 'optimisation|gradient is zero'}), 'Differentiation and optimisation', [
    ('What is the derivative of 5x²?', '10x', ['5x', '10x²', '2x'], 'Multiply by the power, reduce it by one'),
    ('Profit is P(x) = -2x² + 40x. At what output x is profit greatest?', '10', ['20', '40', '5'], "P'(x) = -4x + 40 = 0"),
    ('Why do we check the sign of the second derivative at a stationary point?', 'To tell whether it is a maximum or a minimum',
     ['To find the y-intercept', 'To make the gradient zero', 'Because the first derivative is always positive'], 'Negative means a maximum'),
])
APPLIED_CUR_G12[3] = {'cbse': APPLIED_CUR_G12[3], 'cambridge': APPLIED_CUR_G12[3], 'ib': _IB_AI12_OPTIMISE}
