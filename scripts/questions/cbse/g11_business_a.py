"""CBSE class 11 business studies (NCERT Business Studies XI, 054) families: ch01-ch03.

Every subtopic is a fact table turned into families by g11_accountancy_kit.facts().
"""
from __future__ import annotations

from g11_accountancy_kit import facts

S = 'cbse-g11-business-ch'

# ---------------- ch01 Business, Trade and Commerce

HUNDI = ['Dhani-jog', 'Sah-jog', 'Firman-jog', 'Dekhan-har', 'Darshani', 'Muddati']
CH01_ST1 = dict(
    cat='term from the history of Indian trade',
    terms=[
        ('Hundi', 'A financial instrument of the indigenous banking system, used as a written order to pay money and for remittance and credit in trade.'),
        ('Dhani-jog hundi', 'A hundi payable to any person, with no liability attached to it.'),
        ('Sah-jog hundi', 'A hundi payable to a specific person who is respectable (a "sah"), responsible for the payment.'),
        ('Darshani hundi', 'A hundi payable at sight, which had to be presented for payment within a specified time.'),
        ('Muddati hundi', 'A hundi payable after a specified period of time.'),
        ('Dekhan-har hundi', 'A hundi payable to the presenter or bearer.'),
        ('Firman-jog hundi', 'A hundi payable to order.'),
        ('Merchant guilds (shreni)', 'Associations of merchants and craftsmen that regulated trade, settled disputes and protected the interests of their members.'),
        ('Uttarapatha', 'The ancient northern trade route that connected the north-west of the subcontinent with the Gangetic plains.'),
        ('Dakshinapatha', 'The ancient southern trade route that linked the north with the Deccan and south India.'),
    ],
    lists=[
        ('banking', 'features of the indigenous banking system in ancient and medieval India', [
            ('Use of hundis for remittance and credit', 'Hundis allowed money to be transferred and credit to be given across distant markets.'),
            ('Bankers who accepted deposits and gave loans', 'Indigenous bankers kept deposits and lent money to traders.'),
            ('Use of chitti and similar instruments', 'Written instruments helped trade without carrying cash.'),
            ('Bankers financing trade and crops', 'Traders and farmers obtained credit for business and harvest.')], None),
        ('inter', 'reasons for the rise of intermediaries in Indian trade', [
            ('Growth of long-distance trade', 'Distant markets needed agents to link buyers and sellers.'),
            ('Need for finance and credit', 'Intermediaries provided credit and advances to producers and traders.'),
            ('Need to bear risk', 'Middlemen took on the risk of storing and moving goods.'),
            ('Commission agents and brokers', 'Specialised agents bought and sold on behalf of others for a commission.')], None),
    ],
    scen=[('Which type of hundi is described?', HUNDI, [
        ('A trader in ancient {c} issued a hundi that could be paid to any person, with no liability attached.', 'Dhani-jog', 'A hundi payable to anyone with no liability is dhani-jog.'),
        ('A hundi was to be paid only to a respectable merchant named on it, who took responsibility for payment.', 'Sah-jog', 'Payable to a specific respectable person (sah).'),
        ('A hundi was to be paid immediately when it was presented to the banker.', 'Darshani', 'Payable at sight.'),
        ('A hundi was payable only after ninety days from its date.', 'Muddati', 'Payable after a specified period.'),
        ('A hundi was payable to whoever presented it.', 'Dekhan-har', 'Payable to the presenter or bearer.'),
        ('A hundi was payable to the order of the person named in it.', 'Firman-jog', 'Payable to order.')], None)],
    ars=[
        ('Hundis played an important role in trade in ancient and medieval India.', 'Hundis were used for remittance of money and for giving credit.', 'a', 'Both true and R explains A.'),
        ('A Darshani hundi was payable after a fixed period.', 'A Muddati hundi was payable after a specified period.', 'd', 'A is false: a darshani hundi was payable at sight. R is true.'),
        ('Merchant guilds were important in ancient Indian trade.', 'Guilds settled disputes and protected the interests of their members.', 'a', 'Both true and R explains A.'),
        ('Intermediaries grew in importance as trade expanded to distant markets.', 'Commission agents and brokers linked distant buyers and sellers.', 'a', 'Both true and R explains A.')],
    tf=('the history of trade and commerce in India', [
        'Hundis were used as instruments of remittance and credit.',
        'Merchant guilds regulated trade and settled disputes among members.',
        'Uttarapatha and Dakshinapatha were ancient trade routes.'], [
        'Hundis were coins issued by kings.',
        'A darshani hundi was payable after one year.',
        'Indigenous bankers did not give loans to traders.',
        'Intermediaries disappeared as trade grew.']),
    cases=[('C4', 'D4', 4, 'In a project on medieval trade, {p} reads that a merchant of {c} sent goods to a distant port and received payment there without carrying any coins, through a written instrument drawn on a banker.',
            [('Name the instrument and the system it belonged to.', 'Hundi, part of the indigenous banking system.'),
             ('State two advantages it gave to traders.', 'Safe transfer of money over long distances without carrying cash; credit for trade (payment could be deferred).')]),
           ('C4', 'D5', 4, '{p} argues that middlemen only add to prices and played no useful role in Indian trade history.',
            [('Do you agree? Give two roles intermediaries played.', 'No. They linked distant buyers and sellers, provided finance and credit, bore risk of storage and transport.'),
             ('Name two kinds of intermediaries that arose.', 'Commission agents, brokers, distributors (any two).')])],
)

ACT = ['Business', 'Profession', 'Employment', 'Non-economic activity']
FEAT_ACT = {
    'Business': ['established by the entrepreneur\'s decision and legal formalities', 'reward is profit', 'capital is needed according to size and nature', 'profits are uncertain and risk is present', 'interest can be transferred with some formalities'],
    'Profession': ['membership of a professional body and a certificate of practice are needed', 'reward is a professional fee', 'expertise and training are required', 'a professional code of conduct must be followed'],
    'Employment': ['appointment letter and service agreement', 'reward is salary or wages', 'fixed and regular pay with little or no risk', 'no capital is required', 'norms of behaviour are laid down by the employer'],
}
CH01_ST2 = dict(
    cat='concept',
    terms=[
        ('Business', 'An economic activity involving regular production or purchase and sale of goods and services with the object of earning profit.'),
        ('Profession', 'An occupation involving rendering of personalised services of a specialised nature based on professional knowledge, education and training.'),
        ('Employment', 'An occupation in which people work for others and get remunerated in return.'),
        ('Economic activity', 'An activity undertaken to earn a livelihood or money.'),
        ('Non-economic activity', 'An activity undertaken out of love, sympathy, religion or patriotism, not for money.'),
    ],
    lists=[
        ('char', 'characteristics of business', [
            ('An economic activity', 'It is undertaken to earn money or livelihood.'),
            ('Production or procurement of goods and services', 'Goods are made or bought before they are sold.'),
            ('Sale or exchange of goods and services', 'Goods are sold to customers for value.'),
            ('Dealings on a regular basis', 'A single isolated sale is not business.'),
            ('Profit earning', 'Profit is the main purpose.'),
            ('Uncertainty of return', 'Profit is never certain and losses are possible.'),
            ('Element of risk', 'Every business faces risks from many causes.')], 'noneco'),
        ('noneco', 'features of non-economic activities', [
            ('Done out of love or affection', 'For example, a mother cooking for her family.'),
            ('Done for religious reasons', 'For example, serving in a place of worship.'),
            ('Done out of patriotism', 'For example, helping flood victims as a volunteer.'),
            ('No money or reward is expected', 'There is no aim of earning money.')], 'char'),
        ('obj', 'objectives of business in its key result areas', [
            ('Market standing', 'Standing of the firm relative to its competitors; offering competitive products.'),
            ('Innovation', 'Introducing new ideas or methods of doing things.'),
            ('Productivity', 'Ratio of output to input; a measure of efficiency.'),
            ('Physical and financial resources', 'Acquiring and using resources such as plant, machinery and finance well.'),
            ('Earning profits', 'Earning a reasonable return on capital invested.'),
            ('Manager performance and development', 'Motivating and developing managers.'),
            ('Worker performance and attitude', 'Improving workers\' performance and positive attitude.'),
            ('Social responsibility', 'Obligations towards society while doing business.')], None),
    ],
    pairs=[('business', 'profession', [
        ('mode of establishment', 'entrepreneur\'s decision and legal formalities, if any', 'membership of a professional body and a certificate of practice'),
        ('nature of work', 'provision of goods and services to the public', 'rendering of personalised, expert services'),
        ('qualification', 'no minimum qualification is necessary', 'expertise and training in the specific field are necessary'),
        ('reward or return', 'profit earned', 'professional fee'),
        ('capital investment', 'needed as per size and nature of the business', 'limited capital needed for establishment'),
        ('risk', 'profits are uncertain and irregular; risk is present', 'fee is generally regular and certain; some risk'),
        ('transfer of interest', 'transfer possible with some formalities', 'not possible'),
        ('code of conduct', 'no code of conduct is prescribed', 'professional code of conduct is to be followed')]),
        ('profession', 'employment', [
        ('mode of establishment', 'membership of a professional body and a certificate of practice', 'appointment letter and service agreement'),
        ('nature of work', 'rendering of personalised, expert services', 'performing work as per the service contract or rules of service'),
        ('reward or return', 'professional fee', 'salary or wages'),
        ('capital investment', 'limited capital needed for establishment', 'no capital required'),
        ('risk', 'fee is generally regular and certain; some risk', 'fixed and regular pay; no or little risk'),
        ('code of conduct', 'professional code of conduct is to be followed', 'norms of behaviour laid down by the employer')])],
    scen=[('Identify the economic activity.', ACT, [
        ('{p} runs a {g} shop in {c} and keeps the profit after paying all expenses.', 'Business', 'Regular sale of goods for profit is business.'),
        ('{p} is a chartered accountant in {c} who charges fees for auditing the accounts of firms. {He} is a member of the ICAI.', 'Profession', 'Personalised expert service for a fee, with membership of a professional body.'),
        ('{p} works as an accounts clerk in {f} and gets a fixed salary every month.', 'Employment', 'Working for another for salary under a service contract.'),
        ('{p}, a lawyer enrolled with the Bar Council, appears in court for clients and charges a fee.', 'Profession', 'Legal services for a fee with membership of a professional body.'),
        ('{p} buys handicrafts from artisans of {c} and sells them online regularly to earn a profit.', 'Business', 'Regular purchase and sale for profit.'),
        ('{p} joined {f} as a sales executive after receiving an appointment letter.', 'Employment', 'Appointment letter and salary make it employment.'),
        ('Dr {p} runs a clinic in {c} and treats patients for a consultation fee.', 'Profession', 'Medical services by a qualified, registered doctor for a fee.'),
        ('{p} manufactures {g} in a small unit and supplies them to retailers across {c}.', 'Business', 'Production and sale of goods for profit.')], 'act'),
        ('Is the activity economic or non-economic?', ['Economic activity', 'Non-economic activity', 'Both economic and non-economic', 'Neither'], [
        ('{p} teaches students at a coaching centre and is paid ₹40,000 a month.', 'Economic activity', 'Undertaken to earn money.'),
        ('{p} teaches {his} own children at home every evening.', 'Non-economic activity', 'Done out of love and affection, not for money.'),
        ('{p} volunteers at a flood relief camp in {c} without payment.', 'Non-economic activity', 'Done for social or patriotic reasons, not for money.'),
        ('{p} cooks meals for a hostel and charges the hostel a monthly fee.', 'Economic activity', 'Done for money.')], None)],
    feat={'act': FEAT_ACT},
    ars=[
        ('Profit is the main objective of business.', 'Profit is needed for survival and growth of a business.', 'a', 'Both true and R explains A.'),
        ('A single sale of a personal car at a profit is a business activity.', 'Business requires dealings in goods on a regular basis.', 'd', 'A is false: an isolated sale is not business. R is true.'),
        ('Business involves an element of risk.', 'Business profits are uncertain because of factors beyond the control of the businessman.', 'a', 'Both true and R explains A.'),
        ('A doctor working in a hospital for a monthly salary is in employment.', 'Employment means working for others for a salary under a service agreement.', 'a', 'Both true and R explains A.'),
        ('Business needs no capital investment.', 'Capital is needed as per the size and nature of the business.', 'd', 'A is false; R is true.')],
    tf=('business, profession and employment', [
        'The reward in a profession is a professional fee.',
        'Transfer of interest is not possible in a profession.',
        'Employment requires an appointment letter or service agreement.',
        'Uncertainty of return is a characteristic of business.'], [
        'Every profession requires a large capital investment.',
        'An employee earns profit as reward.',
        'Business has a professional code of conduct prescribed by law for all businessmen.',
        'Non-economic activities are undertaken to earn money.']),
    cases=[('C4', 'D4', 4, '{p} completed a law degree and enrolled with the Bar Council. {He} has two offers: to join {f} as its legal officer on a monthly salary, or to set up {his} own practice in {c}.',
            [('Identify the economic activity in each option.', 'Joining {f} is employment; own practice is a profession.'),
             ('Compare the two on the basis of reward and risk.', 'Employment: fixed salary, little risk. Profession: professional fee, generally regular but with some risk.')]),
           ('C4', 'D5', 6, '{p} quit {his} salaried job to start a {g} business in {c}. In the first year the business made a loss, but {he} continued because {he} believed in its future.',
            [('Name the activity {p} left and the one {he} started.', 'Left employment; started business.'),
             ('Which characteristics of business does the first-year loss illustrate?', 'Uncertainty of return and element of risk.'),
             ('Suggest two objectives {he} should set beyond profit.', 'Market standing, innovation, productivity, social responsibility (any two) with a line on each.')])],
)

CLASS = ['Primary industry', 'Secondary industry', 'Tertiary industry', 'Trade', 'Auxiliaries to trade']
SUB = ['Extractive industry', 'Genetic industry', 'Manufacturing industry', 'Construction industry']
MANU = ['Analytical', 'Synthetical', 'Processing', 'Assembling']
AUX = ['Transport', 'Banking and finance', 'Insurance', 'Warehousing', 'Advertising']
TRADE = ['Internal trade', 'Import trade', 'Export trade', 'Entrepot trade']
CH01_ST3 = dict(
    cat='business activity',
    terms=[
        ('Extractive industry', 'Industry that extracts or draws out products from natural sources, such as mining, fishing and farming.'),
        ('Genetic industry', 'Industry that rears and breeds plants and animals for further reproduction, such as nurseries and poultry farms.'),
        ('Manufacturing industry', 'Industry that converts raw materials or semi-finished products into finished goods.'),
        ('Construction industry', 'Industry engaged in the construction of buildings, dams, bridges, roads and similar works.'),
        ('Tertiary industry', 'Industry that provides support services to primary and secondary industries and to trade.'),
        ('Trade', 'Buying and selling of goods.'),
        ('Entrepot trade', 'Importing goods for the purpose of re-exporting them to other countries.'),
        ('Auxiliaries to trade', 'Activities such as transport, banking, insurance, warehousing and advertising that help trade.'),
        ('Commerce', 'Trade and the auxiliaries to trade, which together remove hindrances in the exchange of goods.'),
    ],
    lists=[('hind', 'auxiliaries to trade with the hindrance each removes', [
        ('Transport', 'Removes the hindrance of place.'),
        ('Banking and finance', 'Removes the hindrance of finance.'),
        ('Insurance', 'Removes the hindrance of risk.'),
        ('Warehousing', 'Removes the hindrance of time (storage).'),
        ('Advertising', 'Removes the hindrance of information.')], None),
        ('manu', 'types of manufacturing industries', [
        ('Analytical industry', 'Separates different elements from the same material, as in an oil refinery.'),
        ('Synthetical industry', 'Combines various ingredients into a new product, as in cement.'),
        ('Processing industry', 'Takes products through successive stages, as in sugar and paper.'),
        ('Assembling industry', 'Assembles component parts into a new product, as in televisions and cars.')], None)],
    scen=[('Identify the type of industry.', SUB, [
        ('{f} operates a coal mine in Jharkhand.', 'Extractive industry', 'It extracts coal from natural sources.'),
        ('{f} runs a poultry farm near {c} that breeds chickens.', 'Genetic industry', 'It rears and breeds animals.'),
        ('{f} makes {g} from raw materials in its factory.', 'Manufacturing industry', 'It converts raw materials into finished goods.'),
        ('{f} has a contract to build a flyover in {c}.', 'Construction industry', 'It constructs roads, bridges and buildings.'),
        ('{f} catches fish off the coast of Kerala.', 'Extractive industry', 'Fishing extracts products from nature.'),
        ('{f} runs a plant nursery that grows saplings for sale.', 'Genetic industry', 'It breeds plants for reproduction.'),
        ('{f} builds dams and canals for state governments.', 'Construction industry', 'It constructs large works.')], None),
        ('Identify the type of manufacturing industry.', MANU, [
        ('An oil refinery near {c} separates petrol, diesel and kerosene from crude oil.', 'Analytical', 'Different elements are separated from the same material.'),
        ('A cement plant combines limestone, clay and gypsum.', 'Synthetical', 'Ingredients are combined into a new product.'),
        ('A sugar mill crushes cane, boils and refines the juice in successive stages.', 'Processing', 'The product passes through successive stages.'),
        ('{f} puts together engines, bodies and tyres bought from suppliers to make cars.', 'Assembling', 'Components are assembled into a new product.'),
        ('A paper mill turns bamboo into pulp and then into paper through several stages.', 'Processing', 'Successive stages of production.')], None),
        ('Which auxiliary to trade removes the hindrance here?', AUX, [
        ('Apples grown in Shimla must reach customers in {c}.', 'Transport', 'Transport removes the hindrance of place.'),
        ('{f} produces woollens all year but sells them mainly in winter.', 'Warehousing', 'Warehousing removes the hindrance of time.'),
        ('{f} needs funds to buy raw material before it gets paid by customers.', 'Banking and finance', 'Banks remove the hindrance of finance.'),
        ('{f} fears its stock may be destroyed by fire.', 'Insurance', 'Insurance removes the hindrance of risk.'),
        ('Customers in {c} do not know about the new {g} launched by {f}.', 'Advertising', 'Advertising removes the hindrance of information.')], None),
        ('Identify the type of trade.', TRADE, [
        ('{f} of {c} buys tea from Assam and sells it in Gujarat.', 'Internal trade', 'Buying and selling within the country.'),
        ('{f} buys machinery from Germany for its factory in {c}.', 'Import trade', 'Buying from another country.'),
        ('{f} sells basmati rice to buyers in the UAE.', 'Export trade', 'Selling to another country.'),
        ('{f} imports dates from Iran and sells the same lot to buyers in Nepal.', 'Entrepot trade', 'Importing for re-export.')], None)],
    ars=[
        ('Transport is an auxiliary to trade.', 'Transport removes the hindrance of place.', 'a', 'Both true and R explains A.'),
        ('Warehousing removes the hindrance of risk.', 'Warehousing helps in storing goods until they are needed.', 'd', 'A is false: warehousing removes the hindrance of time; insurance removes risk. R is true.'),
        ('Commerce includes trade and auxiliaries to trade.', 'Commerce links producers with consumers.', 'a', 'Both true and R explains A.'),
        ('A cement industry is an analytical industry.', 'Synthetical industries combine various ingredients into a new product.', 'd', 'A is false: cement is a synthetical industry. R is true.'),
        ('Mining is a primary industry.', 'Primary industries are connected with the extraction and production of natural resources.', 'a', 'Both true and R explains A.')],
    tf=('the classification of business activities', [
        'Fishing is an extractive industry.',
        'Re-export of imported goods is called entrepot trade.',
        'Insurance removes the hindrance of risk.',
        'An oil refinery is an analytical industry.'], [
        'A poultry farm is an extractive industry.',
        'Trade means only buying of goods.',
        'Warehousing removes the hindrance of finance.',
        'Assembling industries separate elements from raw materials.']),
    cases=[('C4', 'D4', 4, '{f} grows organic vegetables near {c}, packs them in its own unit, keeps them in a cold storage, and sells them through retailers in Delhi after advertising on social media. It has insured its cold storage.',
            [('Identify the primary industry and two auxiliaries to trade involved.', 'Primary: agriculture (extractive/genetic). Auxiliaries: warehousing (cold storage), advertising, insurance, transport (any two).'),
             ('State the hindrance removed by each auxiliary you named.', 'Warehousing: time; advertising: information; insurance: risk; transport: place.')]),
           ('C4', 'D5', 6, 'A group of farmers in {c} complain that they cannot sell their mangoes in distant cities, do not have money to buy cartons in advance, lose fruit when it rots, and fear crop loss due to hailstorms.',
            [('Identify the four hindrances they face.', 'Place, finance, time, risk.'),
             ('Suggest the auxiliary to trade that removes each.', 'Transport, banking, warehousing (cold storage), insurance.'),
             ('Explain how commerce links them with consumers.', 'Commerce (trade plus auxiliaries) removes these hindrances so that goods move from producers to consumers when and where needed.')])],
)

RISKC = ['Natural causes', 'Human causes', 'Economic causes', 'Other causes']
CH01_ST4 = dict(
    cat='term',
    terms=[
        ('Business risk', 'The possibility of inadequate profits or even losses due to uncertainties or unexpected events.'),
        ('Speculative risk', 'A risk that involves the possibility of either profit or loss, such as changes in market price.'),
        ('Pure risk', 'A risk that involves only the possibility of loss or no loss, such as fire or theft.'),
        ('Uncertainty', 'A situation in which future events cannot be predicted with any reasonable accuracy.'),
    ],
    lists=[
        ('nature', 'features of business risk', [
            ('Business risks arise due to uncertainties', 'The future is unknown, so outcomes cannot be predicted.'),
            ('Risk is an essential part of every business', 'No business can avoid risk altogether.'),
            ('Degree of risk depends on the nature and size of business', 'Risk differs between industries and grows with size.'),
            ('Profit is the reward for risk taking', 'Higher risk carries the chance of higher profit.')], None),
        ('start', 'basic factors to be considered while starting a business', [
            ('Selection of the line of business', 'Decide the kind of business, based on demand, profit and technical knowledge.'),
            ('Size of the firm', 'Decide the scale of operations.'),
            ('Choice of form of ownership', 'Sole proprietorship, partnership or company.'),
            ('Location of the business enterprise', 'Consider raw material, labour, markets and transport.'),
            ('Financing the proposition', 'Arrange fixed and working capital.'),
            ('Physical facilities', 'Machinery, buildings and other facilities.'),
            ('Competent and committed workforce', 'Hire skilled and motivated people.'),
            ('Tax planning', 'Consider the tax burden of the form and location chosen.'),
            ('Launching the enterprise', 'Mobilise resources and start operations.')], None),
    ],
    scen=[('Identify the cause of business risk.', RISKC, [
        ('Floods in {c} washed away the stock of {f}.', 'Natural causes', 'Floods are natural calamities beyond human control.'),
        ('An employee of {f} ran away with the cash.', 'Human causes', 'Dishonesty of an employee is a human cause.'),
        ('Demand for the {g} sold by {f} fell sharply after a cheaper competitor entered.', 'Economic causes', 'Change in demand and competition are economic causes.'),
        ('A strike by workers stopped production at {f} for two weeks.', 'Human causes', 'Strikes are a human cause.'),
        ('A sudden rise in the price of raw materials cut the profits of {f}.', 'Economic causes', 'Price fluctuations are economic causes.'),
        ('Political disturbances in {c} forced {f} to close for several days.', 'Other causes', 'Political disturbance is listed among other causes.'),
        ('A fault in the main machine of {f} stopped production.', 'Other causes', 'Mechanical failure is among other causes.'),
        ('An earthquake damaged the factory of {f}.', 'Natural causes', 'Earthquakes are natural causes.'),
        ('Customers stopped buying the products of {f} because a new technology made them outdated.', 'Economic causes', 'Technological change affecting demand is an economic cause.'),
        ('A careless worker at {f} damaged goods while loading them.', 'Human causes', 'Carelessness or negligence of employees is a human cause.')], None)],
    ars=[
        ('Profit is the reward for risk-taking.', 'Business risks arise only from natural causes.', 'c', 'A is true; R is false: risks also arise from human, economic and other causes.'),
        ('Business risk can be completely eliminated.', 'Risk arises from uncertainties about the future.', 'd', 'A is false: risk can only be reduced, not eliminated. R is true.'),
        ('The degree of risk depends on the nature and size of business.', 'A large business usually faces more risk than a small one.', 'a', 'Both true and R explains A.'),
        ('Floods are a human cause of business risk.', 'Natural causes are beyond human control.', 'd', 'A is false: floods are a natural cause. R is true.')],
    tf=('business risk', [
        'Business risks arise due to uncertainties.',
        'Dishonesty of employees is a human cause of business risk.',
        'Risk is an essential part of every business.'], [
        'Business risk can be fully avoided by careful planning.',
        'Price fluctuations are a natural cause of risk.',
        'Small businesses face no risk.',
        'Higher risk always leads to lower profit.']),
    cases=[('C4', 'D4', 4, '{p} wants to open a {g} shop. {He} has ₹8 lakh, has not decided whether to take a partner, and is choosing between a busy market in {c} and a cheaper place outside the city.',
            [('Identify three basic factors {he} must consider.', 'Choice of form of ownership, location of the enterprise, financing the proposition (also size of the firm).'),
             ('What should {he} weigh while choosing the location?', 'Nearness to customers and suppliers, transport, rent and cost, competition.')]),
           ('C4', 'D5', 4, '{f} of {c} suffered losses this year: heavy rain damaged its stock, two key workers left, and a new rival cut prices.',
            [('Classify each cause of risk.', 'Rain: natural cause; workers leaving: human cause; rival cutting prices: economic cause (competition).'),
             ('Suggest one way to reduce each.', 'Insure stock; improve working conditions and retention; improve quality and efficiency to compete.')])],
)

# ---------------- ch02 Forms of Business Organisation

FORMS = ['Sole proprietorship', 'Joint Hindu Family business', 'Partnership', 'Cooperative society', 'Joint stock company']
FEAT_FORMS = {
    'Sole proprietorship': ['owned and controlled by one person', 'unlimited liability', 'easy formation and closure', 'no separate legal entity', 'lack of business continuity'],
    'Joint Hindu Family business': ['membership by birth in the family', 'managed by the karta', 'liability of the karta is unlimited, of co-parceners limited', 'continues after the death of the karta'],
    'Partnership': ['formed by agreement', 'unlimited liability of partners', 'mutual agency', 'restricted continuity', 'shared decision making'],
    'Cooperative society': ['voluntary membership', 'one member one vote', 'limited liability', 'service motive', 'legal status on registration'],
    'Joint stock company': ['separate legal entity', 'limited liability of shareholders', 'perpetual succession', 'transferable shares (public company)', 'management by a board of directors'],
}
CH02_ST1 = dict(
    cat='term',
    terms=[
        ('Sole proprietorship', 'A form of business organisation owned, managed and controlled by one individual who is the recipient of all profits and bearer of all risks.'),
        ('Joint Hindu Family business', 'A form of business owned and carried on by the members of a Hindu Undivided Family, governed by the Hindu Succession Act, 1956.'),
        ('Karta', 'The eldest member who manages a Joint Hindu Family business.'),
        ('Co-parceners', 'Members of a Hindu Undivided Family who have an equal share in its ancestral property.'),
        ('Unlimited liability', 'Liability that extends to the personal assets of the owner if business assets are not enough to pay debts.'),
    ],
    lists=[
        ('sp_merit', 'merits of sole proprietorship', [
            ('Quick decision making', 'The proprietor decides alone, without consulting anyone.'),
            ('Confidentiality of information', 'Business information is not disclosed to others.'),
            ('Direct incentive', 'All profits go to the proprietor, which motivates hard work.'),
            ('Sense of accomplishment', 'Personal satisfaction from running one\'s own business.'),
            ('Ease of formation and closure', 'Few legal formalities are needed.')], 'sp_lim'),
        ('sp_lim', 'limitations of sole proprietorship', [
            ('Limited resources', 'Capital is limited to the owner\'s savings and borrowings.'),
            ('Limited life of a business concern', 'Death, illness or insolvency of the owner may end the business.'),
            ('Unlimited liability', 'Personal assets may be used to pay business debts.'),
            ('Limited managerial ability', 'One person cannot be an expert in every area.')], 'sp_merit'),
        ('jhf_merit', 'merits of Joint Hindu Family business', [
            ('Effective control', 'The karta has absolute decision-making power.'),
            ('Continued business existence', 'The business continues after the death of the karta.'),
            ('Limited liability of members', 'Co-parceners\' liability is limited to their share.'),
            ('Increased loyalty and cooperation', 'Members are bound by family ties.')], 'jhf_lim'),
        ('jhf_lim', 'limitations of Joint Hindu Family business', [
            ('Limited resources', 'Capital is limited to ancestral property.'),
            ('Unlimited liability of the karta', 'The karta\'s personal property is at risk.'),
            ('Dominance of the karta', 'Other members may resent his decisions.'),
            ('Limited managerial skills', 'The karta may not be an expert in all areas.')], 'jhf_merit'),
    ],
    pairs=[('sole proprietorship', 'Joint Hindu Family business', [
        ('ownership', 'one person', 'members of a Hindu Undivided Family'),
        ('membership', 'by setting up the business', 'by birth in the family'),
        ('management', 'by the proprietor', 'by the karta'),
        ('liability', 'unlimited liability of the proprietor', 'unlimited for the karta, limited for co-parceners'),
        ('continuity', 'affected by death or incapacity of the owner', 'continues after the death of the karta'),
        ('governing law', 'no specific Act', 'Hindu Succession Act, 1956')])],
    scen=[('Identify the form of business organisation.', FORMS, [
        ('{p} runs a small {g} shop in {c} alone, takes all decisions and keeps all profits.', 'Sole proprietorship', 'One person owns, manages and bears all risk.'),
        ('The {s} family of {c} runs a textile business inherited from their grandfather; the eldest male member manages it and grandchildren became members at birth.', 'Joint Hindu Family business', 'Membership by birth and management by the karta.'),
        ('{p} started a beauty parlour in {c} with {his} own savings and needs no partners.', 'Sole proprietorship', 'Owned and controlled by one person.'),
        ('After the karta of a family business in {c} died, his eldest son took over and the business continued.', 'Joint Hindu Family business', 'The business continues with the next eldest as karta.')], 'forms')],
    feat={'forms': FEAT_FORMS},
    ars=[
        ('A sole proprietor can take quick decisions.', 'He does not have to consult anyone.', 'a', 'Both true and R explains A.'),
        ('The liability of all members of a Joint Hindu Family business is unlimited.', 'The karta has unlimited liability.', 'd', 'A is false: only the karta\'s liability is unlimited; co-parceners\' is limited. R is true.'),
        ('A sole proprietorship has a separate legal entity.', 'The owner and the business are treated as one in law.', 'd', 'A is false; R is true.'),
        ('A Joint Hindu Family business enjoys continuity.', 'The death of the karta does not end the business.', 'a', 'Both true and R explains A.'),
        ('A sole proprietor gets a direct incentive to work hard.', 'All profits of the business belong to the proprietor.', 'a', 'Both true and R explains A.')],
    tf=('sole proprietorship and Joint Hindu Family business', [
        'A sole proprietor bears all the risk of the business.',
        'In a Joint Hindu Family business, membership is by birth.',
        'The karta manages the Joint Hindu Family business.'], [
        'A sole proprietorship enjoys perpetual succession.',
        'In a Joint Hindu Family business, all members have unlimited liability.',
        'A sole proprietorship requires a minimum of two members.',
        'A Joint Hindu Family business is governed by the Indian Partnership Act, 1932.']),
    cases=[('C4', 'D4', 4, '{p} runs a {g} shop in {c} as a sole proprietor. The shop is doing well, but {he} has no more savings to open a second branch, and {his} family worries about what will happen to the business if {he} falls ill.',
            [('Identify two limitations of sole proprietorship in this case.', 'Limited resources; limited life (lack of continuity).'),
             ('Suggest a form of organisation that would help and give one reason.', 'Partnership: more capital and shared management (or a company for continuity and limited liability).')]),
           ('C4', 'D5', 6, 'The karta of the {s} family business in {c} takes every decision himself. Younger members with management degrees feel ignored, and the business cannot raise money beyond the family property.',
            [('Identify two limitations of the Joint Hindu Family business here.', 'Dominance of the karta; limited resources (also limited managerial skills).'),
             ('Explain one merit the family should not lose if they change the form.', 'Continued existence or effective control or loyalty among members.'),
             ('Advise them, with a reason.', 'Consider converting to a company to raise capital and use professional skills while keeping family control through shareholding.')])],
)

PARTNERS = ['Active partner', 'Sleeping (dormant) partner', 'Secret partner', 'Nominal partner', 'Partner by estoppel', 'Partner by holding out']
CH02_ST2 = dict(
    cat='term',
    terms=[
        ('Partnership', 'The relation between persons who have agreed to share the profits of a business carried on by all or any of them acting for all (Indian Partnership Act, 1932).'),
        ('Partnership deed', 'The written agreement that specifies the terms and conditions governing a partnership.'),
        ('Mutual agency', 'Every partner is both an agent and a principal: he can bind the other partners and is bound by their acts.'),
        ('Partnership at will', 'A partnership that exists at the will of the partners and can be ended by any partner giving notice.'),
        ('Particular partnership', 'A partnership formed for a specific project or a fixed period, ending when it is completed.'),
        ('Limited partnership', 'A partnership in which the liability of at least one partner is unlimited while others may have limited liability.'),
    ],
    lists=[
        ('merit', 'merits of partnership', [
            ('Ease of formation and closure', 'Formed by agreement; registration is optional.'),
            ('Balanced decision making', 'Partners share decisions and use their different skills.'),
            ('More funds', 'Several partners contribute capital.'),
            ('Sharing of risks', 'Losses are borne by all partners.'),
            ('Secrecy', 'Accounts need not be published.')], 'lim'),
        ('lim', 'limitations of partnership', [
            ('Unlimited liability', 'Partners\' personal assets may be used to pay firm\'s debts.'),
            ('Limited resources', 'The number of partners is restricted, so funds are limited.'),
            ('Possibility of conflicts', 'Differences of opinion may arise among partners.'),
            ('Lack of continuity', 'Death, retirement or insolvency of a partner may end the firm.'),
            ('Lack of public confidence', 'Accounts are not published, so the public may not trust the firm.')], 'merit'),
        ('deed', 'contents of a partnership deed', [
            ('Name of the firm', 'The name under which business is carried on.'),
            ('Nature and location of business', 'What the firm will do and where.'),
            ('Duration of business', 'The period of the partnership, if any.'),
            ('Investment made by each partner', 'Capital to be contributed by each.'),
            ('Profit sharing ratio', 'How profits and losses will be shared.'),
            ('Salaries and drawings of partners', 'What partners may draw from the firm.'),
            ('Terms of admission, retirement and expulsion', 'Rules for changes in partners.'),
            ('Interest on capital and on drawings', 'Rates, if any.'),
            ('Procedure for dissolution', 'How the firm will be wound up.'),
            ('Method of solving disputes', 'How disagreements will be settled.')], None),
        ('nonreg', 'consequences of non-registration of a partnership firm', [
            ('A partner cannot file a suit against the firm or other partners', 'He cannot enforce his rights under the Act through a court.'),
            ('The firm cannot file a suit against third parties', 'It cannot recover dues through a court.'),
            ('The firm cannot file a case against its partners', 'Disputes cannot be taken to court by the firm.')], None),
    ],
    pairs=[('sole proprietorship', 'partnership', [
        ('number of owners', 'one', 'two or more, up to the legal maximum'),
        ('formation', 'no agreement needed', 'formed by an agreement among partners'),
        ('decision making', 'quick, by one person', 'shared among partners; may be slower'),
        ('resources', 'limited to one person\'s funds', 'larger, from several partners'),
        ('risk', 'borne by the proprietor alone', 'shared by all partners'),
        ('agency', 'no question of mutual agency', 'every partner is an agent of the others')])],
    scen=[('Identify the type of partner.', PARTNERS, [
        ('{p} invests capital in {f}, takes part in its daily management and shares profits.', 'Active partner', 'Contributes capital and takes part in management.'),
        ('{p} has invested ₹10 lakh in {f} and shares its profits, but does not take part in running it.', 'Sleeping (dormant) partner', 'Contributes capital but does not participate in management.'),
        ('{p} takes part in managing {f} and shares profits, but outsiders do not know that {he} is a partner.', 'Secret partner', 'His association is not disclosed to the public.'),
        ('A famous actor allows {f} to use his name as a partner but invests no money and takes no part in the business.', 'Nominal partner', 'Lends only his name; no capital, no management.'),
        ('{p}, through {his} own conduct, makes a supplier believe {he} is a partner of {f}, and the supplier gives credit on that belief.', 'Partner by estoppel', 'By his own conduct he represented himself as a partner and is liable.'),
        ('{f} declares {p} to be a partner in its letters to suppliers; {p} knows this but does not deny it.', 'Partner by holding out', 'Declared as a partner by others and does not deny it.')], None),
        ('Identify the type of partnership.', ['Partnership at will', 'Particular partnership', 'General partnership', 'Limited partnership'], [
        ('{p} and {p2} form a firm to build one housing complex in {c}; the firm will end when the project is complete.', 'Particular partnership', 'Formed for a specific project.'),
        ('{p} and {p2} run {f} with no fixed period; either can end it by notice.', 'Partnership at will', 'Continues at the will of partners.'),
        ('All partners of {f} have unlimited liability and all take part in management.', 'General partnership', 'Unlimited liability of all partners.'),
        ('In {f}, only {p} has unlimited liability; the other partners\' liability is limited to their capital and they do not take part in management.', 'Limited partnership', 'Some partners have limited liability.')], None)],
    ars=[
        ('Every partner can bind the firm by his acts done in the ordinary course of business.', 'There is mutual agency among partners.', 'a', 'Both true and R explains A.'),
        ('A sleeping partner has limited liability.', 'A sleeping partner does not take part in the management of the firm.', 'd', 'A is false: his liability is unlimited. R is true.'),
        ('Registration of a partnership firm is optional in India.', 'An unregistered firm cannot file a suit against third parties.', 'b', 'Both true, but R (a consequence of non-registration) does not explain why registration is optional.'),
        ('A nominal partner is liable to third parties.', 'He lends his name to the firm.', 'a', 'Both true; R explains why third parties may hold him liable.'),
        ('A partnership firm has perpetual succession.', 'Retirement or death of a partner may end the partnership.', 'd', 'A is false; R is true.')],
    tf=('partnership', [
        'Partnership is governed by the Indian Partnership Act, 1932.',
        'A partnership is formed by an agreement.',
        'Partners have unlimited liability in a general partnership.',
        'A minor can be admitted to the benefits of a partnership with the consent of all partners.'], [
        'Registration of a partnership firm is compulsory in India.',
        'A sleeping partner has limited liability.',
        'A partnership firm has a separate legal entity.',
        'A nominal partner contributes capital and manages the firm.']),
    cases=[('C4', 'D4', 4, '{p}, {p2} and {p3} run {f} in {c}. {p} manages the business, {p2} has only invested money, and {p3} allows the firm to use the name of a well-known family but has invested nothing.',
            [('Identify the type of each partner.', '{p}: active partner; {p2}: sleeping partner; {p3}: nominal partner.'),
             ('Which of them are liable to third parties for the firm\'s debts?', 'All three; in a general partnership each partner (including sleeping and nominal) is liable to outsiders.')]),
           ('C4', 'D5', 6, '{p} and {p2} started {f} without any written agreement and without registering it. After a quarrel about sharing profits, {p2} wants to file a suit against {p}, and a customer has refused to pay ₹2 lakh to the firm.',
            [('What problems arise from having no partnership deed?', 'No written terms on profit sharing, capital, salaries or dispute settlement, so disagreements are hard to resolve.'),
             ('What are the consequences of non-registration here?', '{p2} cannot file a suit against {p} or the firm; the firm cannot sue the customer to recover ₹2 lakh.'),
             ('Advise them on two steps.', 'Draw up a partnership deed covering profit sharing ratio and method of solving disputes; register the firm with the Registrar of Firms.')])],
)

COOP = ["Consumer's cooperative society", "Producer's cooperative society", 'Marketing cooperative society', "Farmer's cooperative society", 'Credit cooperative society', 'Cooperative housing society']
CH02_ST3 = dict(
    cat='type of cooperative society',
    terms=[
        ("Consumer's cooperative society", 'Formed to protect the interests of consumers by buying in bulk and selling to members at reasonable prices, eliminating middlemen.'),
        ("Producer's cooperative society", 'Set up to protect small producers by supplying raw materials, equipment and other inputs.'),
        ('Marketing cooperative society', 'Set up to help small producers sell their products by pooling their output and selling it at the best price.'),
        ("Farmer's cooperative society", 'Formed so that farmers can jointly take up farming activities and get the benefits of large-scale farming.'),
        ('Credit cooperative society', 'Provides loans to members at low rates of interest and protects them from money lenders.'),
        ('Cooperative housing society', 'Helps people with limited income to construct houses at reasonable cost.'),
    ],
    lists=[
        ('feat', 'features of a cooperative society', [
            ('Voluntary membership', 'A person can join or leave at any time.'),
            ('Legal status', 'Registration gives it a separate identity.'),
            ('Limited liability', 'Liability of members is limited to their capital.'),
            ('Control by an elected managing committee', 'Members elect the board; one member one vote.'),
            ('Service motive', 'The main aim is to serve members, not to earn profit.')], None),
        ('merit', 'merits of a cooperative society', [
            ('Equality in voting status', 'One member one vote, regardless of capital.'),
            ('Limited liability', 'Members risk only their capital.'),
            ('Stable existence', 'Death or insolvency of a member does not affect it.'),
            ('Economy in operations', 'Members often serve voluntarily and middlemen are removed.'),
            ('Support from government', 'Low taxes, subsidies and low interest loans.'),
            ('Ease of formation', 'At least ten adult members can register it with simple formalities.')], 'lim'),
        ('lim', 'limitations of a cooperative society', [
            ('Limited resources', 'Members usually have limited means.'),
            ('Inefficiency in management', 'It may not afford expert managers.'),
            ('Lack of secrecy', 'Affairs are discussed openly in meetings.'),
            ('Government control', 'Accounts must be audited and returns filed.'),
            ('Differences of opinion', 'Internal quarrels may arise among members.')], 'merit'),
    ],
    scen=[('Identify the type of cooperative society.', COOP, [
        ('Residents of a colony in {c} form a society to buy groceries in bulk and sell them to members at fair prices.', "Consumer's cooperative society", 'It protects consumers and removes middlemen.'),
        ('Handloom weavers of {c} form a society that supplies them yarn and looms at low cost.', "Producer's cooperative society", 'It supplies inputs to small producers.'),
        ('Small dairy farmers of {c} pool their milk and sell it through their society at the best price.', 'Marketing cooperative society', 'It helps producers sell by pooling output.'),
        ('Farmers of a village near {c} join together to use tractors and better seeds on their combined land.', "Farmer's cooperative society", 'Benefits of large-scale farming.'),
        ('Small traders of {c} form a society that lends to members at low interest so they avoid money lenders.', 'Credit cooperative society', 'Loans at low interest to members.'),
        ('Government employees with limited income form a society to build flats for members in {c}.', 'Cooperative housing society', 'Houses at reasonable cost.')], None)],
    ars=[
        ('Each member of a cooperative society has one vote.', 'Cooperative societies follow democratic management.', 'a', 'Both true and R explains A.'),
        ('A cooperative society aims mainly at profit.', 'A cooperative society is formed to serve its members.', 'd', 'A is false: its main motive is service. R is true.'),
        ('A cooperative society has a stable existence.', 'It has a separate legal entity on registration.', 'a', 'Both true and R explains A.'),
        ('Cooperative societies may suffer from inefficient management.', 'They usually cannot pay high salaries to experts.', 'a', 'Both true and R explains A.')],
    tf=('cooperative societies', [
        'A cooperative society needs at least ten adult members to be formed.',
        'Members of a cooperative society have limited liability.',
        'A cooperative society is registered under the Cooperative Societies Act.'], [
        'Votes in a cooperative society are in proportion to capital.',
        'A cooperative society has unlimited liability of members.',
        'Membership of a cooperative society is compulsory for all residents of an area.',
        'Cooperative societies cannot get government support.']),
    cases=[('C4', 'D4', 4, 'Small potters of {c} find that traders buy their pots cheaply and resell them at high prices in cities. They also struggle to buy clay and kilns.',
            [('Suggest two types of cooperative societies that would help them.', "Marketing cooperative (to sell pooled output at better prices) and producer's cooperative (to supply clay and kilns)."),
             ('State two features of a cooperative society that would suit them.', 'Voluntary membership, one member one vote, limited liability, service motive (any two).')]),
           ('C4', 'D5', 4, 'Members of a consumer cooperative in {c} complain that it is badly run and the stock is often old. They decide to hire a professional manager but cannot afford one.',
            [('Which limitations of cooperatives are seen here?', 'Inefficiency in management; limited resources.'),
             ('Suggest one way out.', 'Seek government assistance or training, or raise funds by enrolling more members.')])],
)

CO_TYPES = ['Private company', 'Public company', 'One Person Company', 'Partnership']
CH02_ST4 = dict(
    cat='term',
    terms=[
        ('Joint stock company', 'An association of persons formed for carrying out business activities, having a legal status independent of its members, formed under the Companies Act.'),
        ('Perpetual succession', 'A company continues to exist irrespective of the death, insolvency or retirement of its members.'),
        ('Private company', 'A company that restricts the right of members to transfer shares, limits members to 200 (excluding employees) and prohibits inviting the public to subscribe to its securities.'),
        ('Public company', 'A company that is not a private company; it can invite the public to subscribe to its shares, which are freely transferable.'),
        ('One Person Company', 'A company with only one person as its member, introduced by the Companies Act, 2013.'),
        ('Board of directors', 'The body elected by the shareholders to manage the company.'),
    ],
    lists=[
        ('merit', 'merits of a joint stock company', [
            ('Limited liability', 'Shareholders\' liability is limited to the unpaid amount on their shares.'),
            ('Transfer of interest', 'Shares of a public company can be easily transferred.'),
            ('Perpetual existence', 'The company continues regardless of changes in members.'),
            ('Scope for expansion', 'Large funds can be raised from the public and banks.'),
            ('Professional management', 'It can employ experts in different fields.')], 'lim'),
        ('lim', 'limitations of a joint stock company', [
            ('Complexity in formation', 'Many legal formalities and time are needed.'),
            ('Lack of secrecy', 'Much information must be disclosed to the public.'),
            ('Impersonal work environment', 'Large size makes personal contact difficult.'),
            ('Numerous regulations', 'Many rules on audit, meetings and publication of accounts.'),
            ('Delay in decision making', 'Decisions pass through many levels.'),
            ('Oligarchic management', 'A few directors may control the company.'),
            ('Conflict in interests', 'Interests of shareholders, directors and employees may clash.')], 'merit'),
        ('feat', 'features of a joint stock company', [
            ('Artificial person', 'It is created by law and can own property and enter contracts.'),
            ('Separate legal entity', 'It is distinct from its members.'),
            ('Formation under the Companies Act', 'Registration is compulsory.'),
            ('Perpetual succession', 'Its life does not depend on its members.'),
            ('Control by a board of directors', 'Shareholders elect directors to manage it.'),
            ('Limited liability', 'Members\' liability is limited to their shares.'),
            ('Risk bearing by shareholders', 'Risk is spread over many shareholders.')], None),
    ],
    pairs=[('private company', 'public company', [
        ('minimum members', 'two', 'seven'),
        ('maximum members', '200, excluding present and past employees', 'no maximum limit'),
        ('transfer of shares', 'restricted', 'freely transferable'),
        ('invitation to the public', 'cannot invite the public to subscribe to its securities', 'can invite the public through a prospectus'),
        ('minimum directors', 'two', 'three'),
        ('name', 'ends with "Private Limited"', 'ends with "Limited"')]),
        ('partnership', 'joint stock company', [
        ('governing law', 'Indian Partnership Act, 1932', 'Companies Act, 2013'),
        ('legal status', 'no separate legal entity', 'separate legal entity'),
        ('liability', 'unlimited', 'limited'),
        ('continuity', 'may end on death or retirement of a partner', 'perpetual succession'),
        ('transfer of interest', 'not possible without consent of all partners', 'shares of a public company freely transferable'),
        ('registration', 'optional', 'compulsory')])],
    scen=[('Identify the type of business organisation.', CO_TYPES, [
        ('{f} Limited invites the public to buy its shares through a prospectus and its shares are traded on the stock exchange.', 'Public company', 'It can invite the public and shares are freely transferable.'),
        ('A family business in {c} registers as a company with 12 members who cannot sell their shares to outsiders without the board\'s approval.', 'Private company', 'Transfer of shares is restricted and the public is not invited.'),
        ('{p} registers a company in which {he} is the only member.', 'One Person Company', 'A company with a single member.'),
        ('{p} and {p2} run a business under an agreement; both are personally liable for its debts.', 'Partnership', 'Formed by agreement with unlimited liability.'),
        ('A company in {c} has 5 members and 2 directors and its name ends with "Private Limited".', 'Private company', 'Meets the minimum of 2 members and 2 directors of a private company.'),
        ('A company has 3,000 shareholders who freely buy and sell its shares.', 'Public company', 'No maximum on members; shares freely transferable.')], None)],
    ars=[
        ('A company can sue and be sued in its own name.', 'A company is a separate legal entity.', 'a', 'Both true and R explains A.'),
        ('A private company can invite the public to subscribe to its shares.', 'A private company restricts the transfer of its shares.', 'd', 'A is false; R is true.'),
        ('A company enjoys perpetual succession.', 'Death or insolvency of shareholders does not affect its existence.', 'a', 'Both true and R explains A.'),
        ('Shareholders of a company have unlimited liability.', 'A company can raise large funds from the public.', 'd', 'A is false: their liability is limited. R is true.'),
        ('A company has to comply with numerous regulations.', 'Companies must hold meetings, get accounts audited and file returns.', 'a', 'Both true and R explains A.')],
    tf=('joint stock companies', [
        'A public company must have at least seven members.',
        'A private company can have at most 200 members, excluding employees.',
        'A company is an artificial person created by law.',
        'A One Person Company has only one member.'], [
        'A private company must have at least seven members.',
        'Shares of a private company are freely transferable.',
        'A company comes to an end on the death of its largest shareholder.',
        'Registration of a company is optional.']),
    cases=[('C4', 'D4', 4, '{f}, a partnership in {c}, has grown rapidly. The partners need ₹50 crore to build a new plant and are worried that their personal property is at risk if the business fails.',
            [('Which form of organisation would you suggest? Why?', 'A public company: it can raise large funds from the public and shareholders have limited liability.'),
             ('State two limitations they should be prepared for.', 'Complexity in formation, numerous regulations, lack of secrecy, delay in decisions (any two).')]),
           ('C4', 'D5', 6, '{p} wants to start a technology venture alone but also wants limited liability and the ability to bring in investors later.',
            [('Which form can {he} use now? State its main feature.', 'A One Person Company: a company with a single member and limited liability.'),
             ('What form may {he} move to as investors join, and why?', 'A private company (minimum two members, up to 200), and later a public company to raise funds from the public.'),
             ('Give one difference between a private and a public company relevant to {him}.', 'A private company cannot invite the public and restricts share transfer; a public company can invite the public and shares are freely transferable.')])],
)

CH02_ST5 = dict(
    lists=[('factors', 'factors affecting the choice of form of business organisation', [
        ('Cost and ease in setting up', 'Sole proprietorship is the cheapest and easiest; a company is costly and complex.'),
        ('Liability', 'Owners who want limited liability may choose a company.'),
        ('Continuity', 'A company gives continuity; a sole proprietorship does not.'),
        ('Management ability', 'Partnership and company allow pooling of skills.'),
        ('Capital considerations', 'Large capital needs favour a company.'),
        ('Degree of control', 'A sole proprietor has full control; in a company ownership and management are separate.'),
        ('Nature of business', 'Direct personal contact suits a sole proprietorship; large-scale manufacturing suits a company.')], None)],
    scen=[('Which form of business organisation is most suitable?', ['Sole proprietorship', 'Partnership', 'Joint stock company', 'Cooperative society'], [
        ('{p} wants to open a small tailoring shop in {c} with low capital, full control and direct contact with customers.', 'Sole proprietorship', 'Low cost, easy formation, full control and personal contact.'),
        ('{p}, a skilled engineer, and {p2}, who has capital, want to start a {g} workshop together and share profits.', 'Partnership', 'Pooling of skills and capital with easy formation.'),
        ('A group plans a steel plant needing ₹500 crore and wants limited liability and continuity.', 'Joint stock company', 'Large capital, limited liability and perpetual succession.'),
        ('Fifty milk producers of a village near {c} want to sell their milk together and serve their own interests rather than earn profit.', 'Cooperative society', 'Service motive and pooling by producers.'),
        ('{p} wants to run a home bakery alone, keeping all the profits and decisions.', 'Sole proprietorship', 'Small scale and full control.'),
        ('Three doctors want to run a clinic together, sharing expenses and fees.', 'Partnership', 'Pooling of skills and sharing of profits.')], None)],
    ars=[
        ('A company is preferred when large capital is required.', 'A company can raise funds from a large number of investors.', 'a', 'Both true and R explains A.'),
        ('Sole proprietorship is suitable for businesses that need direct personal contact with customers.', 'In a sole proprietorship the owner is in touch with customers.', 'a', 'Both true and R explains A.'),
        ('A company is the cheapest form of organisation to set up.', 'Formation of a company involves many legal formalities.', 'd', 'A is false; R is true.')],
    tf=('the choice of form of organisation', [
        'Sole proprietorship is the easiest form to set up.',
        'A company provides continuity of existence.',
        'Owners who want limited liability may prefer a company.'], [
        'A partnership provides limited liability to all partners.',
        'A sole proprietorship is best for raising very large capital.',
        'Formation of a company is easier than that of a partnership.',
        'Degree of control has no bearing on the choice of form.']),
    cases=[('C4', 'D4', 4, '{p} and {p2} want to start a {g} business in {c}. They have ₹20 lakh, want to share work and profits, and do not want many legal formalities, but they worry about unlimited liability.',
            [('Which form would you suggest now, and why?', 'Partnership: easy to form, allows pooling of capital and skills and sharing of profits.'),
             ('Which factor might make them switch to a company later?', 'Need for large capital, limited liability or continuity as the business grows.')]),
           ('C4', 'D5', 6, 'Compare the suitability of a sole proprietorship, a partnership and a company for: (a) a neighbourhood grocery shop, (b) a firm of chartered accountants, (c) an automobile manufacturing unit.',
            [('Suggest the form for each.', '(a) Sole proprietorship (b) Partnership (c) Joint stock company.'),
             ('Give the deciding factor in each case.', '(a) Low cost and personal contact (b) pooling of professional skills (c) huge capital, limited liability and continuity.')])],
)

# ---------------- ch03 Private, Public and Global Enterprises

PSE = ['Departmental undertaking', 'Statutory corporation', 'Government company', 'Private sector enterprise']
FEAT_PSE = {
    'Departmental undertaking': ['financed directly from the government treasury', 'staff are government employees', 'accountable to the concerned ministry', 'subject to the accounting and audit controls of government departments'],
    'Statutory corporation': ['set up under a special Act of Parliament or State Legislature', 'separate legal entity', 'financially independent', 'employees are not government servants'],
    'Government company': ['registered under the Companies Act, 2013', 'at least 51% of paid-up capital held by government', 'management by a board of directors', 'employees are not civil servants'],
    'Private sector enterprise': ['owned by individuals or groups of individuals', 'run for profit', 'not owned by the government'],
}
CH03_ST1 = dict(
    cat='term',
    terms=[
        ('Departmental undertaking', 'A public enterprise organised and managed as a department of a ministry, financed from and accountable to the government.'),
        ('Statutory corporation', 'A public enterprise brought into existence by a special Act of Parliament or a State Legislature, which defines its powers and functions.'),
        ('Government company', 'A company in which not less than 51% of the paid-up share capital is held by the Central Government, State Government(s), or both.'),
        ('Private sector', 'Business units owned by individuals or groups of individuals.'),
        ('Public sector', 'Business organisations owned and managed by the government, wholly or partly.'),
    ],
    lists=[
        ('du_merit', 'merits of departmental undertakings', [
            ('Effective control by Parliament', 'Parliament can discuss their working.'),
            ('High public accountability', 'They are answerable to the ministry and Parliament.'),
            ('Revenue goes to the treasury', 'Income is a source of government revenue.'),
            ('Suitable for national security', 'Strategic activities stay under direct government control.')], 'du_lim'),
        ('du_lim', 'limitations of departmental undertakings', [
            ('Lack of flexibility', 'They follow rigid government rules.'),
            ('Delays due to red tape', 'Decisions pass through many levels.'),
            ('Political interference', 'Ministers may interfere in operations.'),
            ('Insensitive to consumer needs', 'There is little competition to make them responsive.')], 'du_merit'),
        ('sc_merit', 'merits of statutory corporations', [
            ('Independence in operations', 'They enjoy considerable freedom within their Act.'),
            ('Freedom from government interference in finances', 'They are financially independent.'),
            ('Flexibility', 'They can run business on commercial lines.'),
            ('Own policies', 'They frame their own policies and procedures within the Act.')], None),
        ('gc_merit', 'merits of government companies', [
            ('Easy to form', 'Only the Companies Act procedure is needed.'),
            ('Separate legal entity', 'It can sue and be sued and enter contracts.'),
            ('Autonomy in management', 'It is run by a board on business principles.'),
            ('Control of unhealthy competition', 'It can curb unhealthy practices in the market.')], 'gc_lim'),
        ('gc_lim', 'limitations of government companies', [
            ('Companies Act provisions lose meaning', 'With the government as the main shareholder, many safeguards matter little.'),
            ('Evades constitutional responsibility', 'It is not directly answerable to Parliament.'),
            ('Management by government nominees', 'The board is often dominated by government officials.')], 'gc_merit'),
    ],
    pairs=[('departmental undertaking', 'statutory corporation', [
        ('formation', 'by a government order, as part of a ministry', 'by a special Act of Parliament or State Legislature'),
        ('legal status', 'no separate legal entity', 'separate legal entity'),
        ('finance', 'from the government treasury through the budget', 'financially independent; may borrow and raise funds'),
        ('employees', 'government servants', 'not government servants; recruited under the corporation\'s own rules'),
        ('accounting and audit', 'subject to government accounting and audit rules', 'not subject to the same accounting and audit procedures'),
        ('autonomy', 'little autonomy', 'considerable autonomy within the Act')]),
        ('statutory corporation', 'government company', [
        ('formation', 'special Act of Parliament or State Legislature', 'registration under the Companies Act, 2013'),
        ('ownership', 'wholly owned by the government', 'at least 51% of paid-up capital held by government'),
        ('powers', 'defined by its Act', 'defined by its memorandum and articles of association'),
        ('change in objectives', 'needs an amendment of the Act', 'needs a change in its memorandum')])],
    scen=[('Identify the form of public enterprise.', PSE[:3] + ['Private sector enterprise'], [
        ('Indian Railways is run by a ministry, financed through the budget, and its staff are government servants.', 'Departmental undertaking', 'Run as a ministry department, financed by the treasury.'),
        ('The Life Insurance Corporation of India was set up by a special Act of Parliament in 1956.', 'Statutory corporation', 'Created by a special Act.'),
        ('An enterprise in which the Central Government holds 74% of the paid-up capital is registered under the Companies Act.', 'Government company', 'At least 51% held by government and registered under the Companies Act.'),
        ('The postal service is run as part of a ministry and its staff are government employees.', 'Departmental undertaking', 'Part of a ministry; staff are government servants.'),
        ('{f} Limited is owned by the {s} family and its shares are held by the public, with no government holding.', 'Private sector enterprise', 'Owned by private individuals.'),
        ('The Food Corporation of India was created under a special Act to handle procurement and distribution of foodgrains.', 'Statutory corporation', 'Set up under a special Act of Parliament.'),
        ('A state government holds 51% and a private firm 49% of the shares of a power company registered under the Companies Act.', 'Government company', 'Government holds at least 51% of paid-up capital.')], 'pse')],
    feat={'pse': FEAT_PSE},
    ars=[
        ('Employees of a departmental undertaking are government servants.', 'A departmental undertaking is run as a part of a ministry.', 'a', 'Both true and R explains A.'),
        ('A statutory corporation is created by registering under the Companies Act.', 'A statutory corporation has a separate legal entity.', 'd', 'A is false: it is created by a special Act. R is true.'),
        ('In a government company, at least 51% of the paid-up capital is held by the government.', 'A government company is registered under the Companies Act.', 'b', 'Both true, but registration does not explain the 51% holding.'),
        ('Departmental undertakings are suitable for activities related to national security.', 'They are under the direct control of the government.', 'a', 'Both true and R explains A.'),
        ('Statutory corporations are financed from the government budget every year.', 'Statutory corporations are financially independent.', 'd', 'A is false; R is true.')],
    tf=('forms of public enterprises', [
        'A statutory corporation is set up by a special Act of Parliament or State Legislature.',
        'A government company is registered under the Companies Act, 2013.',
        'Departmental undertakings are financed by the government treasury.'], [
        'Employees of a statutory corporation are government servants.',
        'In a government company the government holds not more than 49% of the capital.',
        'A departmental undertaking has a separate legal entity.',
        'A statutory corporation can change its objectives without amending its Act.']),
    cases=[('C4', 'D4', 4, 'The government wants to set up an enterprise for defence production that must remain under its direct control, and another for manufacturing fertilisers that should work on commercial lines with private participation.',
            [('Suggest a suitable form for each.', 'Defence production: departmental undertaking. Fertilisers: government company.'),
             ('Give one reason for each choice.', 'Departmental undertaking suits national security and direct control; a government company is easy to form, autonomous and can have private shareholders.')]),
           ('C4', 'D5', 6, 'A public enterprise run as a department of a ministry in {c} has become slow, with files moving through many desks, frequent orders from ministers and poor service to customers.',
            [('Identify three limitations illustrated.', 'Red tape and delays; political interference; insensitivity to consumer needs (also lack of flexibility).'),
             ('Suggest a better form and two reasons.', 'Statutory corporation or government company: autonomy and flexibility; financial independence or board management on business lines.')])],
)

CH03_ST2 = dict(
    lists=[('role', 'roles of the public sector in India before 1991', [
        ('Development of infrastructure', 'Building railways, power, ports and heavy industries that private firms could not.'),
        ('Regional balance', 'Setting up industries in backward areas for balanced regional development.'),
        ('Economies of scale', 'Large plants such as steel and power gain from scale.'),
        ('Check over concentration of economic power', 'Preventing a few private houses from dominating.'),
        ('Import substitution', 'Producing at home goods that were earlier imported.')], 'reform'),
        ('reform', 'changes in the policy towards the public sector since 1991', [
            ('Reduction in industries reserved for the public sector', 'Most sectors were opened to private enterprise.'),
            ('Disinvestment', 'Sale of part of the government\'s equity in public enterprises to the private sector and the public.'),
            ('Policy on sick units', 'Sick public enterprises were referred to the BIFR for revival or closure.'),
            ('Memorandum of Understanding (MoU)', 'Performance targets agreed with the government in exchange for greater autonomy.')], 'role')],
    terms=[('Disinvestment', 'Sale of the government\'s equity in public sector enterprises to private investors or the public.'),
           ('Memorandum of Understanding (MoU)', 'An agreement between a public enterprise and the government fixing performance targets in return for more autonomy.'),
           ('New Industrial Policy, 1991', 'The policy that began liberalisation, privatisation and globalisation and reduced the role of the public sector.'),
           ('Privatisation', 'Transfer of ownership or management of public enterprises to the private sector.')],
    cat='term',
    scen=[('Which policy change since 1991 is illustrated?', ['Disinvestment', 'Reduction in industries reserved for the public sector', 'Policy on sick units', 'Memorandum of Understanding (MoU)'], [
        ('The government sold 10% of its shares in a public sector oil company to the public through the stock exchange.', 'Disinvestment', 'Sale of government equity.'),
        ('Private airlines and private banks were allowed in sectors that were earlier dominated by the government.', 'Reduction in industries reserved for the public sector', 'Sectors opened to private enterprise.'),
        ('A public sector unit agreed with its ministry to reach a sales target in return for freedom in taking decisions.', 'Memorandum of Understanding (MoU)', 'Targets in exchange for autonomy.'),
        ('Loss-making public enterprises were examined to decide whether they should be revived or closed.', 'Policy on sick units', 'Under the 1991 policy, sick public enterprises were referred to the Board for Industrial and Financial Reconstruction (BIFR) to decide on revival or closure.')], None)],
    ars=[
        ('The government has reduced the number of industries reserved for the public sector since 1991.', 'The New Industrial Policy, 1991 aimed at liberalisation.', 'a', 'Both true and R explains A.'),
        ('Disinvestment means the government buys shares of private companies.', 'Disinvestment involves sale of government equity in public enterprises.', 'd', 'A is false; R is true.'),
        ('MoU gives public enterprises more autonomy.', 'Under an MoU, management is held accountable for agreed targets.', 'a', 'Both true and R explains A.'),
        ('Public enterprises were set up in backward areas before 1991.', 'Balanced regional development was a goal of public sector policy.', 'a', 'Both true and R explains A.')],
    tf=('the changing role of the public sector', [
        'Disinvestment is sale of the government\'s equity in public enterprises.',
        'The New Industrial Policy was announced in 1991.',
        'MoUs set performance targets for public enterprises.'], [
        'Since 1991 more industries have been reserved for the public sector.',
        'Disinvestment means the government buys private companies.',
        'Public enterprises were never set up in backward areas.',
        'MoUs reduce the autonomy of public enterprises.']),
    cases=[('C4', 'D4', 4, 'A public sector company in {c} has made losses for years. The government plans to sell 49% of its shares to the public and sign an agreement with its management fixing targets for the next three years.',
            [('Identify the two policy measures.', 'Disinvestment; Memorandum of Understanding (MoU).'),
             ('State one benefit of each.', 'Disinvestment brings funds and market discipline; MoU gives autonomy with accountability for performance.')]),
           ('C4', 'D5', 6, 'Some people argue that after 1991 the public sector has no role left in India.',
            [('Do you agree? Give two roles it still plays.', 'No. Infrastructure development, balanced regional development, strategic sectors, check on concentration of economic power (any two).'),
             ('Explain two changes in policy since 1991.', 'Reduction of reserved industries; disinvestment; policy on sick units; MoUs (any two with a line each).'),
             ('Evaluate one risk of disinvestment.', 'Social objectives (jobs, regional balance) may be neglected if profit becomes the only aim.')])],
)

CH03_ST3 = dict(
    cat='term',
    terms=[('Global enterprise (MNC)', 'A huge industrial organisation that operates in a number of countries through branches and subsidiaries, with centralised control from its head office.'),
           ('Foreign collaboration', 'An agreement between an MNC and a domestic firm for sale of technology, brand names or manufacturing, often with financial participation.'),
           ('Centralised control', 'Control of all branches and subsidiaries of an MNC by its head office in the home country.'),
           ('Home country', 'The country where an MNC has its head office.')],
    lists=[('feat', 'features of global enterprises (MNCs)', [
        ('Huge capital resources', 'They can raise funds from many sources and countries.'),
        ('Foreign collaboration', 'They enter agreements with local firms for technology and brands.'),
        ('Advanced technology', 'They use superior technology and meet international standards.'),
        ('Product innovation', 'Research and development leads to new products.'),
        ('Marketing strategies', 'Aggressive advertising and brand promotion.'),
        ('Expansion of market territory', 'They operate in many countries through subsidiaries.'),
        ('Centralised control', 'The head office controls all branches.')], None)],
    scen=[('Which feature of a global enterprise is illustrated?', ['Huge capital resources', 'Foreign collaboration', 'Advanced technology', 'Product innovation', 'Marketing strategies', 'Expansion of market territory', 'Centralised control'], [
        ('A multinational soft drink company runs costly advertising campaigns in every Indian city.', 'Marketing strategies', 'Aggressive advertising and promotion.'),
        ('A foreign carmaker signs an agreement with an Indian firm to make its cars in India using its brand.', 'Foreign collaboration', 'Agreement with a domestic firm.'),
        ('All major decisions of the Indian subsidiary of a global electronics company are approved by its head office abroad.', 'Centralised control', 'Head office controls branches.'),
        ('A global pharmaceutical company spends heavily on research to launch new medicines every year.', 'Product innovation', 'R&D leads to new products.'),
        ('An MNC operates factories in 40 countries.', 'Expansion of market territory', 'Operations spread across many countries.'),
        ('An MNC raises billions of dollars from banks and stock markets in several countries.', 'Huge capital resources', 'Large funds from many sources.'),
        ('An MNC brings robots and automated systems to its Indian plant.', 'Advanced technology', 'Superior technology.')], None)],
    ars=[
        ('MNCs can raise huge funds.', 'MNCs can borrow from international banks and raise capital in several countries.', 'a', 'Both true and R explains A.'),
        ('Branches of an MNC are free to follow any policy they like.', 'MNCs have centralised control.', 'd', 'A is false; R is true.'),
        ('MNCs spend heavily on research and development.', 'Product innovation is a feature of MNCs.', 'a', 'Both true and R explains A.')],
    tf=('global enterprises', [
        'MNCs operate in several countries.',
        'MNCs are controlled centrally from their head office.',
        'MNCs usually have advanced technology.'], [
        'MNCs operate only in their home country.',
        'MNCs have very limited capital resources.',
        'Each branch of an MNC is completely independent of the head office.',
        'MNCs do not spend on research and development.']),
    cases=[('C4', 'D4', 4, 'A global electronics company enters India through an agreement with {f}, sets up a plant in {c} with automated machines, and runs a nationwide advertising campaign. All big decisions are taken at its head office in Seoul.',
            [('Identify four features of global enterprises in this case.', 'Foreign collaboration; advanced technology; marketing strategies; centralised control.'),
             ('State one benefit to India.', 'Employment, technology transfer, foreign investment or better products (any one).')]),
           ('C4', 'D5', 4, 'Small Indian {g} makers in {c} complain that a multinational\'s entry has made it hard for them to compete.',
            [('Which features of the MNC give it an edge?', 'Huge capital resources, advanced technology, product innovation and marketing strategies.'),
             ('Suggest one way small firms can respond.', 'Collaborate or specialise in niche products, improve quality, use local knowledge and cooperative marketing.')])],
)

CH03_ST4 = dict(
    cat='term',
    terms=[('Joint venture', 'An arrangement in which two or more businesses join together for a common purpose and mutual benefit, often by creating a new enterprise.'),
           ('Contractual joint venture', 'A joint venture in which partners work together under a contract without creating a new jointly owned entity.'),
           ('Equity-based joint venture', 'A joint venture in which a new, separate enterprise is jointly owned and managed by the partners.'),
           ('Public private partnership (PPP)', 'An arrangement in which the government and private sector partners share resources, risks and rewards in providing public infrastructure and services.')],
    lists=[('jv_ben', 'benefits of joint ventures', [
        ('Increased resources and capacity', 'Partners pool finance, people and facilities.'),
        ('Access to new markets and distribution networks', 'A foreign partner uses the local partner\'s network.'),
        ('Access to technology', 'Advanced technology is shared.'),
        ('Innovation', 'Partners combine ideas to develop new products.'),
        ('Low cost of production', 'Local inputs and labour reduce costs.'),
        ('Established brand name', 'A partner\'s well-known brand helps sales.')], None),
        ('ppp', 'features of public private partnership', [
            ('Relationship', 'A long-term relationship between government and private partners.'),
            ('Sectors', 'Used for infrastructure such as roads, power, water, ports and urban services.'),
            ('Sharing of risks and rewards', 'Risks and returns are shared between the partners.'),
            ('Role of government', 'The government sets policy and standards and may provide land or finance.')], None)],
    pairs=[('contractual joint venture', 'equity-based joint venture', [
        ('new entity', 'no new jointly owned entity is created', 'a new jointly owned entity is created'),
        ('ownership', 'partners do not share ownership of a new business', 'partners hold equity in the new enterprise'),
        ('control', 'each partner keeps its own control; cooperation is by contract', 'joint control by the partners through the new entity'),
        ('example', 'a franchise or technology agreement', 'two firms forming a new company in which both hold shares')])],
    scen=[('Identify the arrangement.', ['Contractual joint venture', 'Equity-based joint venture', 'Public private partnership (PPP)', 'Wholly owned subsidiary'], [
        ('An Indian firm and a Japanese firm form a new company in {c} in which each holds 50% of the shares.', 'Equity-based joint venture', 'A new jointly owned entity.'),
        ('A foreign brand allows {f} to make and sell its products under a contract, without forming any new company.', 'Contractual joint venture', 'Cooperation under a contract with no new entity.'),
        ('A state government and a private firm build and operate a toll highway, sharing costs and toll revenue.', 'Public private partnership (PPP)', 'Government and private partner share risks and rewards in infrastructure.'),
        ('A foreign company sets up a company in India in which it holds 100% of the shares.', 'Wholly owned subsidiary', 'Fully owned by the foreign parent.'),
        ('A city corporation and a private company jointly set up a metro rail system.', 'Public private partnership (PPP)', 'Partnership for public infrastructure.')], None)],
    ars=[
        ('Joint ventures give access to new markets.', 'A local partner already has distribution networks.', 'a', 'Both true and R explains A.'),
        ('A contractual joint venture creates a new jointly owned company.', 'In an equity-based joint venture partners hold equity in a new entity.', 'd', 'A is false; R is true.'),
        ('PPP is used to build public infrastructure.', 'The government and private partners share risks and rewards.', 'a', 'Both true and R explains A.')],
    tf=('joint ventures and PPP', [
        'In an equity-based joint venture a new enterprise is jointly owned.',
        'PPP involves sharing of risks between government and private partners.',
        'Joint ventures can reduce the cost of production.'], [
        'A joint venture always involves only one firm.',
        'In a PPP the private partner bears no risk.',
        'A contractual joint venture requires forming a new company.',
        'Joint ventures prevent access to new technology.']),
    cases=[('C4', 'D4', 4, 'A European {g} brand wants to enter India. It forms a new company with {f}, which has 300 dealers across India. The European firm brings technology and its brand; {f} brings local knowledge and a factory in {c}.',
            [('Identify the type of joint venture.', 'Equity-based joint venture.'),
             ('State three benefits each partner gets.', 'European firm: access to market and distribution, low cost of production, local knowledge. {f}: access to technology, established brand name, increased resources.')]),
           ('C4', 'D5', 6, 'A state government wants a new airport near {c} but lacks funds and expertise. A private company is ready to invest and run it for 30 years.',
            [('Suggest a suitable arrangement and describe it.', 'Public private partnership: government and private company share resources, risks and rewards.'),
             ('What role should the government keep?', 'Set standards and fares policy, provide land and approvals, monitor service quality.'),
             ('Give one benefit and one risk for the public.', 'Benefit: faster development with private efficiency. Risk: higher user charges or poor service if not regulated.')])],
)

FAMILIES = {S + k: facts(v) for k, v in {
    '01-st1': CH01_ST1, '01-st2': CH01_ST2, '01-st3': CH01_ST3, '01-st4': CH01_ST4,
    '02-st1': CH02_ST1, '02-st2': CH02_ST2, '02-st3': CH02_ST3, '02-st4': CH02_ST4, '02-st5': CH02_ST5,
    '03-st1': CH03_ST1, '03-st2': CH03_ST2, '03-st3': CH03_ST3, '03-st4': CH03_ST4}.items()}
