"""CBSE class 11 business studies (NCERT Business Studies XI, 054) families: ch04-ch06.

Every subtopic is a fact table turned into families by g11_accountancy_kit.facts().
"""
from __future__ import annotations

from g11_accountancy_kit import facts

S = 'cbse-g11-business-ch'

# ---------------- ch04 Business Services

SERV = ['Banking', 'Insurance', 'Transportation', 'Warehousing', 'Communication']
WH = ['Private warehouse', 'Public warehouse', 'Bonded warehouse', 'Government warehouse', 'Cooperative warehouse']
FEAT_WH = {
    'Private warehouse': ['owned and operated by the firm for its own goods', 'designed to suit the firm\'s own needs', 'used by large manufacturers and wholesalers'],
    'Public warehouse': ['available to any business on payment of rent', 'operated under a licence from the government', 'useful for small firms that cannot own warehouses'],
    'Bonded warehouse': ['licensed to store imported goods before customs duty is paid', 'importer may pay duty in instalments as goods are taken out', 'goods can be packed, graded and re-exported without paying duty'],
    'Government warehouse': ['owned and managed by the government or a public corporation', 'for example the Central Warehousing Corporation and the Food Corporation of India', 'used by both the government and private businesses'],
    'Cooperative warehouse': ['owned and managed by marketing cooperative societies or agricultural cooperatives', 'provide storage to members at economical rates'],
}
CH04_ST1 = dict(
    cat='term',
    terms=[
        ('Service', 'An essentially intangible activity which provides satisfaction of wants and is not necessarily linked to the sale of a product.'),
        ('Business services', 'Services used by business enterprises for the conduct of their activities, such as banking, insurance, transport, warehousing and communication.'),
        ('Social services', 'Services generally provided voluntarily to achieve social goals, such as health care and education run by NGOs.'),
        ('Personal services', 'Services experienced differently by different customers, such as tourism, recreation and restaurants.'),
        ('Warehousing', 'The holding and preservation of goods until they are dispatched to consumers.'),
        ('Bonded warehouse', 'A warehouse licensed by the government to store imported goods before payment of customs duty.'),
    ],
    lists=[
        ('nature', 'features of services', [
            ('Intangibility', 'Services cannot be touched; they are experiential and quality cannot be judged before use.'),
            ('Inconsistency', 'The same service can differ from customer to customer and time to time because demands differ.'),
            ('Inseparability', 'Production and consumption of a service happen at the same time.'),
            ('Inventory (less)', 'Services cannot be stored for future use; only the capacity to deliver them can be kept ready.'),
            ('Involvement', 'The customer takes part in the delivery process and can modify the service.')], 'goods'),
        ('goods', 'features of goods', [
            ('Tangible', 'Goods are physical products that can be touched and seen.'),
            ('Can be stored', 'Goods can be kept in inventory for future sale.'),
            ('Production separate from consumption', 'Goods are produced first and consumed later.'),
            ('Homogeneous', 'Standardised goods are the same for every customer.')], 'nature'),
        ('whfn', 'functions of warehousing', [
            ('Consolidation', 'Materials from various plants are combined and dispatched together, saving transport cost.'),
            ('Break the bulk', 'Large quantities are divided into smaller lots to suit customer orders.'),
            ('Stockpiling', 'Seasonal goods are stored so that they are available throughout the year.'),
            ('Value-added services', 'Grading, packaging and labelling are done in the warehouse.'),
            ('Price stabilisation', 'Goods are released when supply is short and stored when it is excess, so prices stay steady.'),
            ('Financing', 'Warehouse receipts can be used as security to obtain loans.')], None),
    ],
    pairs=[('goods', 'services', [
        ('nature', 'a physical, tangible product', 'an intangible activity or process'),
        ('type', 'homogeneous and standardised', 'heterogeneous; differs from customer to customer'),
        ('inventory', 'can be stored', 'cannot be stored'),
        ('simultaneous production and consumption', 'production and consumption are separate', 'production and consumption happen together'),
        ('involvement of customer', 'customer is not involved at the time of production', 'customer takes part in delivery'),
        ('tangibility', 'can be touched and seen before purchase', 'cannot be touched; only experienced')])],
    scen=[('Which feature of services is illustrated?', ['Intangibility', 'Inconsistency', 'Inseparability', 'Inventory (less)', 'Involvement'], [
        ('Unsold seats on a {c} to {c2} flight cannot be kept for sale on another day.', 'Inventory (less)', 'Services cannot be stored; an unsold seat is lost.'),
        ('A haircut is produced and consumed at the same time, with the customer in the chair.', 'Inseparability', 'Production and consumption are simultaneous.'),
        ('The same doctor gives different advice to two patients with similar symptoms.', 'Inconsistency', 'Services are not standardised; each delivery differs.'),
        ('{p} cannot check the quality of a hotel stay before experiencing it.', 'Intangibility', 'A service cannot be touched or seen before use.'),
        ('At a restaurant {p} asks for the dish to be made less spicy and the chef changes it.', 'Involvement', 'The customer takes part in and modifies the service.'),
        ('A cinema hall cannot sell yesterday\'s empty seats today.', 'Inventory (less)', 'Service capacity unused at one time is lost.')], None),
        ('Which type of warehouse is described?', WH, [
        ('{f} built its own godown near its factory in {c} to store only its own {g}.', 'Private warehouse', 'Owned and used by the firm for its own goods.'),
        ('Small traders of {c} rent space in a licensed warehouse open to any business.', 'Public warehouse', 'Available to any business on payment of rent.'),
        ('An importer stores goods in a licensed warehouse and pays customs duty only when the goods are taken out.', 'Bonded warehouse', 'Imported goods are stored before payment of customs duty.'),
        ('Food grains are stored in godowns of the Food Corporation of India.', 'Government warehouse', 'Owned and managed by a government corporation.'),
        ('Farmers who are members of a marketing society store their produce in the society\'s godown at low rates.', 'Cooperative warehouse', 'Run by cooperative societies for members.')], 'wh'),
        ('Which type of service is it?', ['Business services', 'Social services', 'Personal services', 'Not a service'], [
        ('An NGO runs a free health camp for villagers near {c}.', 'Social services', 'Provided voluntarily to achieve social goals.'),
        ('{f} takes a loan from a bank to buy machinery.', 'Business services', 'Banking is a business service used to conduct business.'),
        ('{p} takes a holiday package to {c} from a tour operator.', 'Personal services', 'Tourism is a personal service experienced differently by each customer.'),
        ('{f} insures its factory against fire.', 'Business services', 'Insurance is a business service.'),
        ('{p} dines at a restaurant with {his} family.', 'Personal services', 'Restaurant service is a personal service.')], None)],
    feat={'wh': FEAT_WH},
    ars=[
        ('Services cannot be stored for future use.', 'Production and consumption of services are simultaneous.', 'a', 'Both true and R explains A.'),
        ('Warehousing helps in price stabilisation.', 'Goods are stored when supply is in excess and released when it is short.', 'a', 'Both true and R explains A.'),
        ('Services are standardised in the same way as goods.', 'The customer participates in the delivery of a service.', 'd', 'A is false: services are inconsistent. R is true.'),
        ('Bonded warehouses are useful to importers.', 'Bonded warehouses store only domestic goods.', 'c', 'A is true; R is false: they store imported goods before customs duty is paid.')],
    tf=('services and warehousing', [
        'Intangibility is a feature of services.',
        'Bonded warehouses store imported goods before payment of customs duty.',
        'Warehouse receipts can be used to obtain loans.'], [
        'Services can be stored like goods.',
        'Public warehouses can be used only by the government.',
        'Production of a service always happens before it is consumed.',
        'Warehousing has no role in price stabilisation.']),
    cases=[('C4', 'D4', 4, '{f} of {c} produces winter jackets all year but sells most of them between October and January. It has only a small storage room and its retailers order in small lots.',
            [('Which business service would help {f}? Name two of its functions involved.', 'Warehousing: stockpiling of seasonal goods and break the bulk into smaller lots.'),
             ('Suggest a type of warehouse if {f} cannot build its own.', 'Public warehouse (rent space), or a cooperative warehouse if a member of a society.')]),
           ('C4', 'D5', 6, '{p} runs a hotel in {c}. Guests complain that service differs between staff and that rooms left empty on weekdays are a loss.',
            [('Name the features of services shown by the two complaints.', 'Inconsistency (service varies) and inventory (less): empty rooms cannot be stored.'),
             ('Suggest one step for each.', 'Train staff and set service standards; offer weekday discounts or packages to fill capacity.'),
             ('Why is a hotel stay intangible?', 'It cannot be touched or tested before use; the guest only experiences it.')])],
)

BANKS = ['Commercial bank', 'Cooperative bank', 'Specialised bank', 'Central bank']
EB = ['Internet banking', 'Electronic Fund Transfer (NEFT/RTGS)', 'Debit card', 'Credit card', 'ATM']
DEP = ['Current account', 'Savings account', 'Fixed deposit account', 'Recurring deposit account']
CH04_ST2 = dict(
    cat='banking term',
    terms=[
        ('Bank', 'An institution that accepts deposits from the public and lends money, and provides related services.'),
        ('Overdraft', 'A facility that allows a current account holder to withdraw more than the balance in the account, up to an agreed limit.'),
        ('Cash credit', 'An arrangement under which a customer can borrow up to a limit against current assets such as stock.'),
        ('Discounting of bills', 'Paying the holder of a bill of exchange before its due date after deducting a charge.'),
        ('Bank draft', 'An order issued by a bank on its own branch to pay a specified sum to a named person, used for remittance.'),
        ('E-banking', 'Banking through electronic channels such as the internet, which lets customers transact without visiting a branch.'),
        ('RTGS', 'An electronic system that transfers funds individually and immediately (real-time gross settlement), used mainly for large amounts.'),
        ('Central bank', 'The apex bank that issues currency and controls the banking system of a country; in India, the Reserve Bank of India.'),
    ],
    lists=[
        ('fn', 'functions of commercial banks', [
            ('Acceptance of deposits', 'Banks accept deposits in current, savings and fixed deposit accounts.'),
            ('Lending of funds', 'Banks lend through overdraft, cash credit, loans and discounting of bills.'),
            ('Cheque facility', 'Cheques let customers make payments safely without handling cash.'),
            ('Remittance of funds', 'Banks transfer funds from one place to another through drafts and electronic transfers.'),
            ('Allied services', 'Bill payment, lockers, underwriting and buying or selling securities for customers.')], 'cbfn'),
        ('cbfn', 'functions of the central bank', [
            ('Issue of currency notes', 'Only the central bank issues currency notes.'),
            ('Banker to the government', 'It keeps government accounts and manages public debt.'),
            ('Banker\'s bank', 'It holds reserves of commercial banks and lends to them.'),
            ('Controller of credit', 'It regulates the supply of money and credit in the economy.')], 'fn'),
        ('eben', 'benefits of e-banking', [
            ('24 hours a day, 365 days a year', 'Customers can bank at any time.'),
            ('Anywhere banking', 'Transactions can be made from home, office or while travelling.'),
            ('Financial discipline', 'Every transaction is recorded, giving a clear trail.'),
            ('Lower load on branches', 'Branches handle fewer routine transactions.'),
            ('Lower cost for banks and customers', 'Electronic transactions cost less than counter transactions.')], None),
    ],
    pairs=[('current account', 'savings account', [
        ('purpose', 'for businesses with frequent transactions', 'for individuals to save money'),
        ('interest', 'generally no interest is paid', 'interest is paid on the balance'),
        ('number of withdrawals', 'no restriction', 'may be restricted'),
        ('overdraft', 'overdraft facility is available', 'overdraft is not usually available')])],
    scen=[('Which type of bank is it?', BANKS, [
        ('A bank in {c} accepts deposits from the public and gives loans to traders for profit.', 'Commercial bank', 'Accepting deposits and lending for profit is commercial banking.'),
        ('A bank registered under a cooperative societies Act lends to farmers and small traders who are its members.', 'Cooperative bank', 'Registered under cooperative law and serves members.'),
        ('A bank provides long-term finance to industries for setting up new plants.', 'Specialised bank', 'Industrial and development banks are specialised banks.'),
        ('The bank issues currency notes and acts as banker to the government.', 'Central bank', 'These are functions of the central bank (RBI).'),
        ('A bank deals mainly in financing foreign trade and foreign exchange.', 'Specialised bank', 'Foreign exchange banks are specialised banks.')], None),
        ('Which e-banking facility is used?', EB, [
        ('{p} logs in to the bank\'s website from home in {c} and pays {his} electricity bill.', 'Internet banking', 'Transactions through the bank\'s website are internet banking.'),
        ('{f} transfers ₹5 crore to a supplier immediately and individually through the bank\'s electronic system.', 'Electronic Fund Transfer (NEFT/RTGS)', 'Large immediate transfers use RTGS, an EFT system.'),
        ('{p} pays at a shop with a card that deducts the amount from {his} savings account at once.', 'Debit card', 'A debit card draws directly from the account balance.'),
        ('{p} buys a phone on a card and pays the bank later, within the credit period.', 'Credit card', 'A credit card lets the holder buy now and pay later.'),
        ('{p} withdraws cash from a machine at night when the branch is closed.', 'ATM', 'An automated teller machine allows withdrawals at any time.')], None),
        ('Which type of deposit account suits the need?', DEP, [
        ('{f} has hundreds of payments and receipts every day.', 'Current account', 'Current accounts allow unlimited transactions and overdraft.'),
        ('{p}, a student, wants to keep some savings and earn interest while withdrawing occasionally.', 'Savings account', 'Savings accounts pay interest and allow limited withdrawals.'),
        ('{p} has ₹2 lakh that {he} will not need for three years and wants the highest interest.', 'Fixed deposit account', 'A lump sum for a fixed period earns higher interest.'),
        ('{p} wants to deposit ₹2,000 every month for five years.', 'Recurring deposit account', 'Fixed monthly deposits for a period form a recurring deposit.')], None)],
    ars=[
        ('Commercial banks create credit.', 'Banks lend a part of the deposits they receive.', 'a', 'Both true and R explains A.'),
        ('E-banking provides a sense of financial discipline.', 'Every e-banking transaction is recorded.', 'a', 'Both true and R explains A.'),
        ('The Reserve Bank of India is a commercial bank.', 'The Reserve Bank of India issues currency notes.', 'd', 'A is false: RBI is the central bank. R is true.'),
        ('Overdraft is available to savings account holders as a rule.', 'Overdraft allows withdrawal beyond the balance up to a limit.', 'd', 'A is false: overdraft is generally given on current accounts. R is true.'),
        ('Cheques are a convenient way to make payments.', 'Cheques can be issued only by the Reserve Bank of India.', 'c', 'A is true; R is false: account holders issue cheques.')],
    tf=('banking', [
        'Commercial banks accept deposits and lend money.',
        'Overdraft is generally given to current account holders.',
        'E-banking allows banking at any time.',
        'Bank drafts are used to remit money.'], [
        'Commercial banks issue currency notes.',
        'A savings account pays no interest.',
        'E-banking can be used only during branch hours.',
        'Discounting of bills means the bank pays more than the face value of the bill.']),
    cases=[('C4', 'D4', 4, '{p} runs a {g} business in {c}. {He} needs short-term funds to buy stock before the festive season and wants to pay suppliers in other cities without carrying cash.',
            [('Suggest two ways a commercial bank can lend to {him}.', 'Overdraft on current account; cash credit against stock (also discounting of bills, short-term loan).'),
             ('Suggest two ways to remit money.', 'Bank draft; electronic fund transfer (NEFT/RTGS) or internet banking.')]),
           ('C4', 'D5', 6, 'The manager of a bank branch in {c} finds long queues for deposits, withdrawals and bill payments. Staff costs are rising.',
            [('Suggest a solution.', 'Encourage e-banking: internet banking, ATMs, debit cards and electronic fund transfer.'),
             ('Give three benefits of it to customers.', 'Banking 24 x 7, anywhere banking, record of every transaction (financial discipline).'),
             ('Give one benefit to the bank.', 'Lower load on branches and lower cost per transaction.')])],
)

PRIN = ['Utmost good faith', 'Insurable interest', 'Indemnity', 'Proximate cause', 'Subrogation', 'Contribution', 'Mitigation of loss']
INS = ['Life insurance', 'Fire insurance', 'Marine insurance', 'Health insurance']
FEAT_INS = {
    'Life insurance': ['a contract of assurance, not of indemnity', 'insurable interest must exist at the time of the contract', 'sum assured is paid on death or maturity', 'policies include whole life, endowment, joint life and annuity'],
    'Fire insurance': ['a contract of indemnity', 'insurable interest must exist at the time of contract and at the time of loss', 'loss must be caused by actual fire and the fire must be accidental', 'usually for one year'],
    'Marine insurance': ['a contract of indemnity', 'covers the ship (hull), the cargo and the freight', 'insurable interest must exist at the time of loss', 'covers perils of the sea'],
    'Health insurance': ['covers medical and hospitalisation expenses', 'premium is paid regularly to keep the cover', 'reimburses or pays cashless for treatment up to the sum insured'],
}
CH04_ST3 = dict(
    cat='insurance principle or term',
    terms=[
        ('Insurance', 'A contract in which one party agrees to compensate another for a loss in return for a payment called premium.'),
        ('Premium', 'The consideration paid by the insured to the insurer for the cover.'),
        ('Utmost good faith', 'Both parties must disclose all material facts fully and honestly (uberrimae fidei).'),
        ('Insurable interest', 'The insured must have a financial interest in the subject matter so that its loss would cause financial loss to the insured.'),
        ('Indemnity', 'The insured is compensated only to the extent of actual loss, so that no profit is made from the claim.'),
        ('Subrogation', 'After compensating the insured, the insurer steps into the shoes of the insured and gets the rights over the damaged property.'),
        ('Contribution', 'When the same property is insured with more than one insurer, the insurers share the loss in proportion to their policies.'),
        ('Proximate cause', 'The loss is paid only if the nearest or immediate cause is an insured peril (causa proxima).'),
        ('Mitigation of loss', 'The insured must take reasonable steps to reduce the loss once the insured event happens.'),
    ],
    lists=[
        ('fn', 'functions of insurance', [
            ('Providing certainty', 'Insurance provides certainty of payment for an uncertain loss.'),
            ('Protection', 'It protects against the financial effects of probable losses.'),
            ('Risk sharing', 'The loss is shared by all who are exposed to the same risk, through premium.'),
            ('Assist in capital formation', 'Premiums collected are invested in productive activities.')], None),
        ('prin', 'principles of insurance', [
            ('Utmost good faith', 'Both parties must disclose all material facts.'),
            ('Insurable interest', 'The insured must stand to lose financially from the loss.'),
            ('Indemnity', 'Compensation equals actual loss; no profit from a claim.'),
            ('Proximate cause', 'The nearest cause of loss must be an insured peril.'),
            ('Subrogation', 'The insurer takes over the insured\'s rights after paying the claim.'),
            ('Contribution', 'Insurers share the loss when there is double insurance.'),
            ('Mitigation of loss', 'The insured must try to reduce the loss.')], None),
        ('marine', 'types of marine insurance', [
            ('Ship or hull insurance', 'Covers the ship against perils of the sea.'),
            ('Cargo insurance', 'Covers the goods carried in the ship.'),
            ('Freight insurance', 'Covers the shipping company\'s loss of freight if goods do not reach the destination.')], None),
        ('life', 'types of life insurance policies', [
            ('Whole life policy', 'Sum assured is paid to the beneficiaries on the death of the insured.'),
            ('Endowment life assurance policy', 'Sum assured is paid at the end of a fixed period or on earlier death.'),
            ('Joint life policy', 'Two or more lives are insured; sum is paid on the first death.'),
            ('Annuity policy', 'Sum assured is paid in monthly, quarterly or yearly instalments after a certain age.'),
            ('Children\'s endowment policy', 'Provides money for a child\'s education or marriage.')], None),
    ],
    pairs=[('life insurance', 'fire insurance', [
        ('nature of contract', 'a contract of assurance', 'a contract of indemnity'),
        ('insurable interest', 'must exist at the time of the contract', 'must exist at the time of contract and at the time of loss'),
        ('period', 'usually for a long period', 'usually for one year'),
        ('amount payable', 'the sum assured on death or maturity', 'actual loss up to the sum insured'),
        ('investment element', 'has an element of saving or investment', 'no investment element')])],
    scen=[('Which principle of insurance applies?', PRIN, [
        ('{p} hid the fact that {he} had a heart condition when taking a life policy; the insurer later refused the claim.', 'Utmost good faith', 'Material facts must be disclosed; concealment makes the contract voidable.'),
        ('{p} tried to insure a neighbour\'s house against fire, but the insurer refused.', 'Insurable interest', '{p} would suffer no financial loss if the neighbour\'s house burnt.'),
        ('A shop insured for ₹10 lakh suffered fire damage of ₹4 lakh; the insurer paid ₹4 lakh.', 'Indemnity', 'Compensation equals actual loss, not the sum insured.'),
        ('After paying for a car damaged in an accident, the insurer sued the driver who caused it.', 'Subrogation', 'The insurer takes over the rights of the insured after paying.'),
        ('A godown insured with two companies suffered a loss; both companies shared the claim.', 'Contribution', 'Insurers share the loss in proportion to their policies.'),
        ('Goods insured against fire were damaged by water used to put out the fire; the claim was paid.', 'Proximate cause', 'The immediate cause, the fire, is an insured peril.'),
        ('When fire broke out in {his} shop, {p} called the fire brigade and moved goods to safety at once.', 'Mitigation of loss', 'The insured must take reasonable steps to reduce the loss.')], None),
        ('Which type of insurance is needed?', INS, [
        ('{f} sends a consignment of {g} by ship from Mumbai to Dubai and wants cover against perils of the sea.', 'Marine insurance', 'Goods carried by sea are covered by cargo (marine) insurance.'),
        ('{p} wants {his} family to get money if {he} dies early.', 'Life insurance', 'Life insurance pays the sum assured on death.'),
        ('{f} wants cover against loss of its factory from accidental fire.', 'Fire insurance', 'Fire insurance covers loss caused by accidental fire.'),
        ('{p} wants hospital bills for {his} family to be covered.', 'Health insurance', 'Health insurance covers medical and hospital expenses.')], 'ins')],
    feat={'ins': FEAT_INS},
    ars=[
        ('Life insurance is not a contract of indemnity.', 'The loss of a human life cannot be measured in money.', 'a', 'Both true and R explains A.'),
        ('Insurance helps in capital formation.', 'Premiums collected are invested in productive activities.', 'a', 'Both true and R explains A.'),
        ('An insured person can make a profit from a fire insurance claim.', 'Fire insurance is a contract of indemnity.', 'd', 'A is false: indemnity rules out profit. R is true.'),
        ('A person can insure the life of a stranger.', 'Insurable interest is essential for an insurance contract.', 'd', 'A is false: there is no insurable interest. R is true.'),
        ('Both parties to an insurance contract must disclose material facts.', 'Subrogation is one of the principles of insurance.', 'b', 'Both are true but R does not explain A; A follows from the principle of utmost good faith.')],
    tf=('principles and types of insurance', [
        'Life insurance is a contract of assurance.',
        'Insurable interest must exist in every insurance contract.',
        'Subrogation applies after the insurer pays the claim.',
        'Marine insurance can cover the hull, cargo and freight.'], [
        'Under indemnity the insured always receives the full sum insured.',
        'Utmost good faith applies only to the insurer.',
        'Fire insurance covers loss from any cause, even if no fire occurred.',
        'Contribution applies when property is insured with only one insurer.']),
    cases=[('C4', 'D4', 4, '{p} insured {his} {g} shop in {c} for ₹20 lakh with two insurers, ₹10 lakh each. A fire caused a loss of ₹6 lakh.',
            [('How much will {p} receive in total, and on what principle?', '₹6 lakh in total, by the principle of indemnity (actual loss only).'),
             ('How will the two insurers share it?', 'By contribution in proportion to their policies: ₹3 lakh each.')]),
           ('C4', 'D5', 6, '{f} imports machinery by sea. During the voyage the ship ran aground and part of the cargo was damaged. The ship also needed repairs.',
            [('Which types of insurance cover the cargo and the ship?', 'Cargo insurance and ship (hull) insurance: both marine insurance.'),
             ('When must insurable interest exist in marine insurance?', 'At the time of loss.'),
             ('State two other principles that will apply to the claim.', 'Indemnity, proximate cause, subrogation, utmost good faith (any two).')])],
)

POST = ['Speed post', 'Registered post', 'Money order', 'Business post', 'Courier service', 'Media post']
TEL = ['Cellular mobile services', 'Fixed line services', 'Radio paging services', 'Cable services', 'VSAT services', 'DTH services']
CH04_ST4 = dict(
    cat='communication service',
    terms=[
        ('Speed post', 'A postal service for fast, time-bound delivery of letters and parcels between specified cities.'),
        ('Money order', 'A postal service for transferring money from one place to another through the post office.'),
        ('Registered post', 'A mail service that gives proof of posting and of delivery, used for important documents.'),
        ('Business post', 'A postal service that undertakes pre-mailing activities such as collecting, inserting and addressing mail for bulk customers.'),
        ('Media post', 'A service that allows companies to advertise on postcards, letters and post boxes.'),
        ('VSAT', 'A satellite-based communication service (very small aperture terminal) that gives connectivity in remote areas.'),
        ('DTH', 'A satellite service that sends television signals directly to homes through a small dish antenna (direct to home).'),
        ('Courier service', 'A private service for door-to-door delivery of documents and parcels.'),
    ],
    lists=[
        ('post', 'services offered by India Post', [
            ('Financial facilities', 'Postal orders, money orders and savings schemes such as PPF, recurring deposits and savings bank.'),
            ('Mail facilities', 'Delivery of letters and parcels, with registration and insurance.'),
            ('Speed post', 'Fast delivery between major cities.'),
            ('Business post and media post', 'Bulk mailing and advertising for businesses.'),
            ('Greetings post and e-bill post', 'Greeting cards and collection of bills through post offices.'),
            ('Passport facilities', 'Post offices accept passport applications.')], 'tel'),
        ('tel', 'types of telecom services', [
            ('Cellular mobile services', 'Mobile voice and data services.'),
            ('Fixed line services', 'Landline voice and data services.'),
            ('Radio paging services', 'One-way messaging to a person on the move.'),
            ('Cable services', 'Linear television and data through cable networks.'),
            ('VSAT services', 'Satellite connectivity for remote areas.'),
            ('DTH services', 'Television directly to homes via satellite dish.')], 'post'),
    ],
    scen=[('Which postal service is used?', POST, [
        ('{f} sends an urgent tender document from {c} to {c2} and needs it delivered fast with tracking.', 'Speed post', 'Fast, time-bound delivery between cities.'),
        ('{p} sends a legal notice and wants proof that it was delivered.', 'Registered post', 'Registration gives proof of posting and delivery.'),
        ('{p} sends ₹3,000 to {his} parents in a village through the post office.', 'Money order', 'Money orders transfer money through the post office.'),
        ('A bank asks the post office to print addresses on and post 50,000 statements to its customers.', 'Business post', 'Pre-mailing activities for bulk mail.'),
        ('{f} advertises its {g} on postcards sold by the post office.', 'Media post', 'Advertising on postal stationery is media post.')], None),
        ('Which telecom service is used?', TEL, [
        ('A bank branch in a remote hill village connects to its head office via a small satellite dish.', 'VSAT services', 'Satellite connectivity for remote areas is VSAT.'),
        ('{p} watches television through a small dish on {his} roof, without a cable operator.', 'DTH services', 'Direct-to-home satellite television.'),
        ('{p} talks to clients while travelling, using {his} mobile phone.', 'Cellular mobile services', 'Mobile voice and data services.'),
        ('{f} uses landline telephones at its office in {c}.', 'Fixed line services', 'Landline services are fixed line services.')], None)],
    ars=[
        ('Communication services help business link with the outside world.', 'Business needs to exchange information with customers, suppliers and others.', 'a', 'Both true and R explains A.'),
        ('VSAT is useful in remote areas.', 'VSAT gives satellite-based connectivity where cables cannot reach.', 'a', 'Both true and R explains A.'),
        ('Post offices provide only mail services.', 'Post offices also offer savings schemes and money orders.', 'd', 'A is false; R is true.'),
        ('Registered post gives proof of delivery.', 'Registered post is used to send money.', 'c', 'A is true; R is false: money orders are used to send money.')],
    tf=('postal and telecom services', [
        'Money orders are used to transfer money through the post office.',
        'Speed post provides fast delivery between cities.',
        'DTH sends television signals directly to homes via satellite.'], [
        'Post offices do not offer any savings schemes.',
        'VSAT needs underground cables to reach villages.',
        'Media post is used to send money abroad.',
        'Registered post gives no proof of delivery.']),
    cases=[('C4', 'D4', 4, '{f}, a small exporter of {g} in {c}, wants to send samples to buyers quickly, collect payments from local agents and stay in touch with buyers by phone and internet.',
            [('Name one postal service for each of the first two needs.', 'Speed post or courier for samples; money order (or post office savings or e-payment services) for payments.'),
             ('Name two telecom services useful to it.', 'Cellular mobile services and fixed line or broadband services (VSAT if remote).')])],
)

# ---------------- ch05 Emerging Modes of Business

EB_TYPE = ['B2B commerce', 'B2C commerce', 'Intra-B commerce', 'C2C commerce']
CH05_ST1 = dict(
    cat='e-business term',
    terms=[
        ('E-business', 'Conduct of industry, trade and commerce using computer networks such as the internet.'),
        ('E-commerce', 'Buying and selling online, a part of e-business that covers a firm\'s interaction with customers and suppliers over the internet.'),
        ('B2B commerce', 'E-business in which both the parties are business firms.'),
        ('B2C commerce', 'E-business in which a business firm deals with consumers.'),
        ('Intra-B commerce', 'Use of electronic networks for interactions among departments and people within the same firm.'),
        ('C2C commerce', 'E-business in which consumers sell to other consumers, usually through a website.'),
    ],
    lists=[
        ('ben', 'benefits of e-business', [
            ('Ease of formation and lower investment', 'An online business can be set up easily with little investment in physical infrastructure.'),
            ('Convenience', 'It is available 24 hours a day, 7 days a week.'),
            ('Speed', 'Buying, selling and exchange of information happen quickly.'),
            ('Global reach or access', 'The market is the whole world.'),
            ('Movement towards a paperless society', 'Documents and records are kept and exchanged electronically.')], 'lim'),
        ('lim', 'limitations of e-business', [
            ('Low personal touch', 'Online dealings lack face-to-face contact.'),
            ('Incongruence between order taking and delivery speed', 'Orders are taken in seconds but goods take time to reach.'),
            ('Need for technology capability and competence', 'All parties must be comfortable with computers and the internet.'),
            ('Increased risk due to anonymity and non-traceability', 'Parties may not be sure of the identity of the other.'),
            ('People resistance', 'People may be slow to adjust to new technology.'),
            ('Ethical fallouts', 'Monitoring of email and computer use may invade privacy.')], 'ben'),
    ],
    pairs=[('traditional business', 'e-business', [
        ('ease of formation', 'difficult', 'simple'),
        ('physical presence', 'required', 'not required'),
        ('cost of setting up', 'high', 'low'),
        ('operating cost', 'high, because of fixed investment in property and equipment', 'low'),
        ('nature of contact with suppliers and customers', 'indirect, through intermediaries', 'direct'),
        ('internal communication', 'hierarchical', 'non-hierarchical, vertical, horizontal or diagonal'),
        ('response time', 'long', 'instantaneous'),
        ('shape of organisation', 'vertical or tall', 'horizontal or flat'),
        ('opportunity for personal touch', 'more', 'less'),
        ('product trial before purchase', 'possible', 'not possible'),
        ('global reach', 'less', 'more'),
        ('transaction risk', 'low, because of face-to-face contact', 'high, because of distance and anonymity')])],
    scen=[('Which type of e-business is it?', EB_TYPE, [
        ('{f} places orders for raw material with its suppliers through their online portal.', 'B2B commerce', 'Both parties are business firms.'),
        ('{p} buys {g} from the website of {f}.', 'B2C commerce', 'A firm sells to a consumer.'),
        ('The marketing and production departments of {f} share daily sales data through the company\'s intranet.', 'Intra-B commerce', 'Interaction within the same firm.'),
        ('{p} sells {his} old bicycle to {p2} through an online classifieds website.', 'C2C commerce', 'One consumer sells to another.'),
        ('A car maker coordinates with its dealers online to plan inventory.', 'B2B commerce', 'Manufacturer and dealer are both firms.'),
        ('A bank sends account statements and offers to customers by email.', 'B2C commerce', 'A firm interacts with consumers.'),
        ('Employees of {f} apply for leave and see their pay slips on the company\'s internal portal.', 'Intra-B commerce', 'Within-firm interaction with employees.')], None),
        ('Which benefit or limitation of e-business is illustrated?', ['Global reach or access', 'Convenience', 'Low personal touch', 'Incongruence between order taking and delivery speed', 'Ease of formation and lower investment'], [
        ('{p} in {c} sells handmade {g} to buyers in many countries through {his} website.', 'Global reach or access', 'The market is the whole world.'),
        ('{p} orders groceries at midnight from an app.', 'Convenience', 'E-business is available round the clock.'),
        ('{p} misses the advice and friendly talk {he} used to get from the shopkeeper.', 'Low personal touch', 'Online dealings lack face-to-face contact.'),
        ('{p} placed an online order in seconds but the goods took a week to arrive.', 'Incongruence between order taking and delivery speed', 'Information moves fast but goods take time.'),
        ('{p} started an online store from home without renting a shop.', 'Ease of formation and lower investment', 'No large investment in physical premises is needed.')], None)],
    ars=[
        ('E-business has a global reach.', 'The internet can be accessed from anywhere in the world.', 'a', 'Both true and R explains A.'),
        ('Transaction risk is higher in e-business.', 'Parties to an online deal may be anonymous and far apart.', 'a', 'Both true and R explains A.'),
        ('E-business requires a large investment in physical premises.', 'In e-business physical presence is not needed.', 'd', 'A is false; R is true.'),
        ('E-commerce is a wider term than e-business.', 'E-business covers e-commerce as well as other business functions done electronically.', 'd', 'A is false: e-business is wider. R is true.'),
        ('Response time is instantaneous in e-business.', 'E-business has a tall, hierarchical structure.', 'c', 'A is true; R is false: e-business organisations are flat.')],
    tf=('e-business', [
        'E-business is wider in scope than e-commerce.',
        'B2B commerce takes place between two business firms.',
        'E-business is available 24 x 7.',
        'Low personal touch is a limitation of e-business.'], [
        'E-business requires a larger investment than traditional business.',
        'C2C commerce takes place between a firm and its employees.',
        'Product trial before purchase is easier online.',
        'Response time in e-business is long.']),
    cases=[('C4', 'D4', 4, '{p} runs a traditional {g} shop in {c}. {His} son suggests selling online too, because customers now order from home.',
            [('Give two benefits {p} would gain from going online.', 'Global reach, convenience (24 x 7), lower cost of operation, speed (any two).'),
             ('Give two limitations {he} must be prepared for.', 'Low personal touch, delay between order and delivery, transaction risk, need for technical skills (any two).')]),
           ('C4', 'D5', 6, '{f} is deciding whether to open ten new showrooms or build an online store. Its products are standardised branded {g}.',
            [('Compare the two on cost of setting up, global reach and response time.', 'Online: lower cost, global reach, instantaneous response; showrooms: high cost, local reach, slower response.'),
             ('Which would you recommend and why?', 'Online store (perhaps with a few showrooms): standardised branded goods need little trial, so online selling suits them.'),
             ('Name one risk it must guard against.', 'Transaction risk or data security risk such as hacking.')])],
)

PAY = ['Cash on delivery', 'Cheque', 'Net banking transfer', 'Credit or debit card', 'Digital cash']
RISK = ['Transaction risk', 'Data storage and transmission risk', 'Threat to intellectual property and privacy', 'No risk is involved']
CH05_ST2 = dict(
    cat='term',
    terms=[
        ('Cash on delivery', 'A payment method in which the buyer pays when the goods are delivered.'),
        ('Digital cash', 'A form of electronic currency held in electronic form, used to pay online.'),
        ('Encryption', 'Converting data into a coded form so that only the intended receiver can read it.'),
        ('Hacking', 'Unauthorised access to a computer system or data.'),
        ('Cyber crime', 'Any illegal activity committed using a computer or network.'),
        ('Computer virus', 'A program that damages data or the working of a computer system.'),
        ('Online transaction', 'Buying or selling of goods or services through the internet, from registration to payment and delivery.'),
    ],
    lists=[
        ('steps', 'steps in an online transaction', [
            ('Registration', 'The buyer registers with the online seller by filling a form.'),
            ('Placing an order', 'The buyer adds items to an online shopping cart and confirms the order.'),
            ('Payment mechanism', 'The buyer pays by cash on delivery, cheque, net banking, card or digital cash.'),
            ('Delivery', 'Goods are delivered physically, or online in the case of software, music and similar items.')], 'pay'),
        ('pay', 'methods of payment in online transactions', [
            ('Cash on delivery', 'Payment is made when goods are delivered.'),
            ('Cheque', 'A cheque is sent to the seller, who delivers after it is cleared.'),
            ('Net banking transfer', 'The buyer transfers money to the seller\'s account online.'),
            ('Credit or debit card', 'Card details are given online and the card account is charged.'),
            ('Digital cash', 'Electronic currency is used for payment.')], 'steps'),
        ('risk', 'risks of e-business', [
            ('Transaction risks', 'Default on order taking or giving, delivery, or payment.'),
            ('Data storage and transmission risks', 'Data can be stolen or changed through viruses and hacking.'),
            ('Risks of threat to intellectual property and privacy', 'Information put online may be copied or misused.')], None),
        ('safety', 'measures for safety of online transactions', [
            ('Encryption', 'Data is sent in coded form.'),
            ('Use of passwords and authentication', 'Only authorised users can access accounts.'),
            ('Antivirus software and firewalls', 'Protect systems against viruses and unauthorised access.'),
            ('Secure websites for payment', 'Card details are entered only on secure payment pages.'),
            ('Verifying the identity of parties', 'Reduces default and fraud due to anonymity.')], None),
    ],
    scen=[('Which payment method is used?', PAY, [
        ('{p} orders a book online and pays the delivery agent when the parcel arrives.', 'Cash on delivery', 'Payment at the time of delivery.'),
        ('{p} transfers money from {his} bank account to the seller through the bank\'s website.', 'Net banking transfer', 'Online transfer between bank accounts.'),
        ('{p} enters {his} card number and the one-time password on the seller\'s payment page.', 'Credit or debit card', 'Card details are used to pay online.'),
        ('{p} sends a cheque to {f}, which dispatches the goods after the cheque clears.', 'Cheque', 'Goods are delivered after the cheque is realised.'),
        ('{p} pays for an online game using electronic money held in electronic form.', 'Digital cash', 'Electronic currency is digital cash.')], None),
        ('Which risk of e-business is it?', RISK, [
        ('A customer of {f} denied having placed an order after the goods were delivered.', 'Transaction risk', 'Default on order giving is a transaction risk.'),
        ('A virus deleted the customer records stored on the computers of {f}.', 'Data storage and transmission risk', 'Data stored on systems was damaged.'),
        ('A rival copied the product designs that {f} had posted on its website.', 'Threat to intellectual property and privacy', 'Online information was copied and misused.'),
        ('A seller took payment online but never delivered the goods.', 'Transaction risk', 'Default on delivery is a transaction risk.'),
        ('Hackers stole card details while they were being sent to a website.', 'Data storage and transmission risk', 'Data was stolen during transmission.')], None)],
    ars=[
        ('Cash on delivery reduces risk for the buyer.', 'The buyer pays only when the goods reach.', 'a', 'Both true and R explains A.'),
        ('Encryption protects data during transmission.', 'Encrypted data can be read only by the intended receiver.', 'a', 'Both true and R explains A.'),
        ('Online transactions carry no transaction risk.', 'Parties to online deals are often unknown to each other.', 'd', 'A is false; R is true.'),
        ('Registration is the first step in an online transaction.', 'Delivery of goods always happens online.', 'c', 'A is true; R is false: most goods are delivered physically.')],
    tf=('online transactions and security', [
        'Registration is the first step in online buying.',
        'Hacking is a data storage and transmission risk.',
        'Encryption helps make online payments safe.'], [
        'All goods bought online are delivered online.',
        'Cash on delivery means paying before placing the order.',
        'A computer virus improves the security of data.',
        'Online transactions have no risk of default.']),
    cases=[('C4', 'D4', 4, '{p} plans to start an online store for {g}. {He} is worried that customers may not pay, that hackers may steal data, and that buyers in small towns do not use cards.',
            [('Identify the risks {he} is worried about.', 'Transaction risk (default on payment) and data storage and transmission risk.'),
             ('Suggest a payment method for small-town buyers and one safety measure.', 'Cash on delivery; encryption, passwords and antivirus or firewall (any one).')]),
           ('C4', 'D5', 6, 'Describe what happens when {p} buys {g} from an online store, from start to finish.',
            [('List the steps.', 'Registration, placing the order in a shopping cart, payment, delivery.'),
             ('Name three payment options.', 'Cash on delivery, net banking transfer, credit or debit card (also cheque, digital cash).'),
             ('State one way the store keeps payment details safe.', 'Encryption of data on secure payment pages.')])],
)

CH05_ST3 = dict(
    cat='outsourcing term',
    terms=[
        ('Outsourcing', 'Contracting out of a firm\'s activities, usually non-core, to outside specialists.'),
        ('BPO', 'Outsourcing of business processes such as customer support, call centres, payroll and data entry (business process outsourcing).'),
        ('KPO', 'Outsourcing of knowledge-based work that needs specialised skills, such as research, analytics and legal services (knowledge process outsourcing).'),
        ('Core activities', 'Activities that are central to a firm\'s business and give it its competitive advantage.'),
        ('Offshoring', 'Outsourcing work to a provider in another country.'),
    ],
    lists=[
        ('need', 'benefits of outsourcing', [
            ('Focus on core activities', 'The firm can concentrate on what it does best.'),
            ('Quest for excellence', 'Work is done by specialists, improving quality.'),
            ('Cost reduction', 'Specialists produce at lower cost due to economies of scale.'),
            ('Growth through economies of scale', 'Saved resources can be used for growth.'),
            ('Fosters economic development', 'Outsourcing creates jobs and business in host countries.')], 'con'),
        ('con', 'concerns over outsourcing', [
            ('Confidentiality', 'Sharing information with outsiders may lead to leaks.'),
            ('Sweat-shopping', 'Work may be given to low-cost units that exploit labour.'),
            ('Ethical concerns', 'Use of child labour or unfair practices by the provider.'),
            ('Opposition in the home country', 'Workers may lose jobs when work moves abroad.')], 'need'),
        ('char', 'features of outsourcing', [
            ('Contracting out', 'Work is given to outside agencies.'),
            ('Usually of non-core activities', 'Firms outsource activities outside their core business, and sometimes core ones too.'),
            ('Long-term relationship', 'Outsourcing is usually a long-term contract.'),
            ('Within the country or abroad', 'The provider may be local or in another country.')], None),
    ],
    pairs=[('BPO', 'KPO', [
        ('nature of work', 'routine business processes', 'knowledge-based work needing expertise'),
        ('examples', 'call centres, payroll, data entry', 'research, analytics, legal and financial services'),
        ('skills required', 'process skills and communication', 'specialised knowledge and qualifications'),
        ('focus', 'cost and efficiency of processes', 'expertise and judgement')])],
    scen=[('Is it BPO or KPO?', ['BPO', 'KPO', 'Not outsourcing', 'Joint venture'], [
        ('A telecom company hires {f} to answer customer calls from its call centre.', 'BPO', 'Customer support is a business process.'),
        ('A drug maker hires {f} in {c} to analyse data from clinical trials.', 'KPO', 'Research and analytics need specialised knowledge.'),
        ('{f} gives its payroll processing to an outside agency.', 'BPO', 'Payroll is a routine business process.'),
        ('A US law firm hires Indian lawyers at {f} to do legal research.', 'KPO', 'Legal research is knowledge work.'),
        ('{f} sets up its own department to answer customer calls.', 'Not outsourcing', 'The work is done in-house, not contracted out.'),
        ('A bank hires an outside firm for data entry of loan applications.', 'BPO', 'Data entry is a business process.'),
        ('An investment firm hires analysts at {f} to prepare equity research reports.', 'KPO', 'Financial research is knowledge work.')], None),
        ('Which benefit of outsourcing is illustrated?', ['Focus on core activities', 'Quest for excellence', 'Cost reduction', 'Fosters economic development'], [
        ('{f}, a {g} maker, outsources its accounting so its managers can spend their time on product design.', 'Focus on core activities', 'Non-core work is given away to concentrate on the core.'),
        ('{f} outsources advertising to a top agency to get creative, high-quality campaigns.', 'Quest for excellence', 'Specialists deliver better quality.'),
        ('{f} finds that an outside courier delivers its parcels more cheaply than its own vans.', 'Cost reduction', 'Specialists have economies of scale.'),
        ('Outsourcing work to {c} has created thousands of jobs there.', 'Fosters economic development', 'Outsourcing creates jobs in host regions.')], None)],
    ars=[
        ('Outsourcing helps a firm focus on its core activities.', 'Non-core activities are contracted out to specialists.', 'a', 'Both true and R explains A.'),
        ('Outsourcing may lead to loss of confidentiality.', 'The firm has to share information with outside agencies.', 'a', 'Both true and R explains A.'),
        ('KPO involves only routine data entry work.', 'KPO requires specialised knowledge.', 'd', 'A is false; R is true.'),
        ('Outsourcing can reduce costs.', 'Outsourcing is always of core activities only.', 'c', 'A is true; R is false: it is usually of non-core activities.')],
    tf=('outsourcing', [
        'Outsourcing usually covers non-core activities.',
        'Call centres are an example of BPO.',
        'Confidentiality is a concern in outsourcing.'], [
        'KPO deals only with routine processes.',
        'Outsourcing always increases costs.',
        'Outsourcing can only be done within the country.',
        'Outsourcing has no ethical concerns.']),
    cases=[('C4', 'D4', 4, '{f}, a {g} manufacturer in {c}, spends a lot of management time on payroll, customer calls and market research.',
            [('Classify the three activities as BPO or KPO.', 'Payroll and customer calls: BPO; market research: KPO.'),
             ('Give two benefits of outsourcing them.', 'Focus on core activity of manufacturing; cost reduction; quality from specialists (any two).')]),
           ('C4', 'D5', 4, 'Employees of {f} protest when it outsources its customer service to a firm abroad. The firm also worries about customer data.',
            [('Name the two concerns over outsourcing shown here.', 'Opposition in the home country (job losses) and confidentiality.'),
             ('Suggest one way to address each.', 'Retrain and redeploy staff; strict confidentiality agreements and data security checks.')])],
)

# ---------------- ch06 Social Responsibility of Business and Business Ethics

SR_KIND = ['Economic responsibility', 'Legal responsibility', 'Ethical responsibility', 'Discretionary responsibility']
GROUPS = ['Shareholders or owners', 'Workers', 'Consumers', 'Government and community']
CH06_ST1 = dict(
    cat='concept',
    terms=[
        ('Social responsibility', 'The obligation of business to make decisions and perform actions that are desirable in terms of the objectives and values of society.'),
        ('Legal responsibility', 'The obligation of business to obey the laws of the land.'),
        ('Corporate social responsibility', 'Voluntary activities of a company that contribute to the well-being of society beyond what law requires.'),
        ('Business ethics', 'Socially determined moral principles that should govern business activities.'),
    ],
    lists=[
        ('for', 'arguments for social responsibility', [
            ('Justification for existence and growth', 'Business exists to provide goods and services that satisfy human needs.'),
            ('Long-term interest of the firm', 'A good public image earns support of society in the long run.'),
            ('Avoidance of government regulation', 'Voluntary responsibility reduces the need for government control.'),
            ('Maintenance of society', 'Responsible business helps maintain peace and order in society.'),
            ('Availability of resources with business', 'Business has finance and managerial talent to help solve social problems.'),
            ('Converting problems into opportunities', 'Business can turn social problems into profitable opportunities.'),
            ('Better environment for doing business', 'A healthy society provides a better environment for business.'),
            ('Holding business responsible for social problems', 'Business has caused some problems, such as pollution, and should help solve them.')], 'against'),
        ('against', 'arguments against social responsibility', [
            ('Violation of profit maximisation objective', 'Business exists only to maximise profit; social responsibility conflicts with it.'),
            ('Burden on consumers', 'Costs of social programmes are passed on to consumers through higher prices.'),
            ('Lack of social skills', 'Business people lack the understanding and training to solve social problems.'),
            ('Lack of broad public support', 'The public does not like business getting involved in social programmes.'),
            ('Lack of accountability', 'Business is not accountable to the people for social action.')], 'for'),
    ],
    pairs=[('social responsibility', 'legal responsibility', [
        ('nature', 'voluntary; goes beyond the law', 'compulsory; required by law'),
        ('scope', 'wider: includes legal and moral obligations', 'narrower: only what law requires'),
        ('consequence of non-fulfilment', 'loss of goodwill and public image', 'legal penalty or punishment'),
        ('basis', 'values and expectations of society', 'laws passed by the government')])],
    scen=[('Which argument about social responsibility is it?', ['Long-term interest of the firm', 'Avoidance of government regulation', 'Burden on consumers', 'Lack of social skills', 'Converting problems into opportunities', 'Violation of profit maximisation objective'], [
        ('{f} believes that helping the local community now will win it customer loyalty for years to come.', 'Long-term interest of the firm', 'A good image serves the firm in the long run.'),
        ('Industry leaders in {c} voluntarily cut pollution so that the government does not impose strict rules.', 'Avoidance of government regulation', 'Voluntary action reduces need for regulation.'),
        ('A critic says the cost of {f}\'s social schemes will only raise the price of its {g}.', 'Burden on consumers', 'Costs are passed on to consumers.'),
        ('A shareholder argues that managers of {f} are trained in business, not in solving social problems.', 'Lack of social skills', 'Business people lack skills for social problems.'),
        ('{f} turns farm waste into packaging material and sells it at a profit.', 'Converting problems into opportunities', 'A social problem becomes a business opportunity.'),
        ('{p} says the only job of {f} is to earn as much profit as possible for its owners.', 'Violation of profit maximisation objective', 'Argument that social responsibility conflicts with profit maximisation.')], None)],
    ars=[
        ('Social responsibility is in the long-term interest of business.', 'A good public image earns the support of society.', 'a', 'Both true and R explains A.'),
        ('Social responsibility is the same as legal responsibility.', 'Social responsibility includes voluntary actions beyond the law.', 'd', 'A is false; R is true.'),
        ('Some critics oppose social responsibility of business.', 'They argue that its cost is passed on to consumers.', 'a', 'Both true and R explains A.'),
        ('Business has the resources to help solve social problems.', 'Business has neither finance nor managerial talent.', 'c', 'A is true; R is false: business has both finance and managerial talent.')],
    tf=('social responsibility of business', [
        'Social responsibility is wider than legal responsibility.',
        'Social responsibility can help avoid government regulation.',
        'Burden on consumers is an argument against social responsibility.'], [
        'Social responsibility is compulsory under every law.',
        'Social responsibility only means earning profit.',
        'Lack of social skills is an argument for social responsibility.',
        'Social responsibility has no link with the long-term interest of the firm.']),
    cases=[('C4', 'D4', 4, 'At the annual meeting of {f}, one shareholder says spending on a school for workers\' children is a waste of profit. The chairperson replies that it will help the company in the long run.',
            [('Give the argument used by the shareholder and one by the chairperson.', 'Shareholder: violation of profit maximisation objective. Chairperson: long-term interest of the firm.'),
             ('Give one more argument the chairperson could use.', 'Better environment for business, maintenance of society, availability of resources with business (any one).')]),
           ('C4', 'D5', 6, 'A government plans strict new rules after several factories near {c} ignored public complaints. {f} instead voluntarily sets up a waste treatment plant and helps clean the river.',
            [('Is {f}\'s action legal or social responsibility? Why?', 'Social responsibility: it is voluntary, beyond what the law required at the time.'),
             ('Which argument for social responsibility does it show?', 'Avoidance of government regulation (also holding business responsible for problems it caused).'),
             ('State two arguments against such actions.', 'Burden on consumers, violation of profit maximisation, lack of social skills (any two).')])],
)

CH06_ST2 = dict(
    cat='kind of responsibility',
    terms=[
        ('Economic responsibility', 'The responsibility of a business to produce goods and services that society wants and sell them at a profit.'),
        ('Legal responsibility', 'The responsibility of a business to obey the laws of the land.'),
        ('Ethical responsibility', 'The responsibility to behave in ways society expects even if the law does not require it.'),
        ('Discretionary responsibility', 'Purely voluntary obligations such as charitable contributions to educational institutions or flood relief.'),
    ],
    lists=[
        ('kinds', 'kinds of social responsibility', [
            ('Economic responsibility', 'Produce goods and services society wants and sell them at a profit.'),
            ('Legal responsibility', 'Obey the laws of the land.'),
            ('Ethical responsibility', 'Behave in a morally right way, such as respecting religious sentiments in advertisements.'),
            ('Discretionary responsibility', 'Voluntary acts such as charity and help in disasters.')], None),
        ('shr', 'responsibilities of business towards shareholders or owners', [
            ('Provide a fair return on investment', 'Pay reasonable dividends.'),
            ('Ensure safety of investment', 'Use the capital carefully.'),
            ('Give accurate information', 'Share regular and correct information on financial position.'),
            ('Run the business efficiently', 'Use resources productively.')], 'cons'),
        ('wrk', 'responsibilities of business towards workers', [
            ('Fair wages', 'Pay wages that are fair and timely.'),
            ('Good working conditions', 'Provide safe and healthy workplaces.'),
            ('Opportunities to grow', 'Give training and chances of promotion.'),
            ('Respect for workers\' rights', 'Respect the right to form unions and treat workers with dignity.')], 'cons'),
        ('cons', 'responsibilities of business towards consumers', [
            ('Supply quality goods at reasonable prices', 'Provide safe, good quality products.'),
            ('No adulteration, black marketing or hoarding', 'Avoid unfair trade practices.'),
            ('Truthful advertising', 'Do not mislead consumers.'),
            ('Proper after-sales service', 'Handle complaints and grievances promptly.')], 'wrk'),
        ('gov', 'responsibilities of business towards the government and community', [
            ('Obey laws and pay taxes honestly', 'Act as a good citizen.'),
            ('Protect the environment', 'Avoid pollution and conserve resources.'),
            ('Help weaker sections and community development', 'Support schools, health care and welfare.'),
            ('Respect the values of society', 'Act in line with social norms.')], 'shr'),
    ],
    scen=[('Which kind of social responsibility is shown?', SR_KIND, [
        ('{f} makes {g} that people want and sells them at a fair profit.', 'Economic responsibility', 'Producing wanted goods at a profit is economic responsibility.'),
        ('{f} pays all its taxes on time and follows labour laws.', 'Legal responsibility', 'Obeying the law is legal responsibility.'),
        ('{f} withdraws an advertisement that hurt the religious feelings of a community, though no law required it.', 'Ethical responsibility', 'Morally right behaviour beyond law.'),
        ('{f} donates ₹50 lakh for flood relief in {c}.', 'Discretionary responsibility', 'A purely voluntary charitable act.'),
        ('{f} funds scholarships for poor students at a college in {c}.', 'Discretionary responsibility', 'Voluntary contribution to education.'),
        ('{f} follows the rules on minimum wages set by law.', 'Legal responsibility', 'Following law is legal responsibility.')], None),
        ('Towards which interest group is the responsibility?', GROUPS, [
        ('{f} pays a fair dividend and publishes accurate accounts every year.', 'Shareholders or owners', 'Fair return and correct information are owed to owners.'),
        ('{f} provides safety equipment and training to all its factory staff.', 'Workers', 'Safe conditions and training are owed to workers.'),
        ('{f} sells {g} at fair prices and replaces defective units promptly.', 'Consumers', 'Quality, fair prices and after-sales service are owed to consumers.'),
        ('{f} pays its taxes honestly and plants trees around its plant in {c}.', 'Government and community', 'Obeying laws and protecting the environment serve government and community.'),
        ('{f} does not hoard {g} to create an artificial shortage.', 'Consumers', 'Avoiding hoarding is a duty towards consumers.'),
        ('{f} respects the right of its employees to form a union.', 'Workers', 'Respecting workers\' rights.')], None)],
    ars=[
        ('Discretionary responsibility is purely voluntary.', 'No law requires charitable contributions by business.', 'a', 'Both true and R explains A.'),
        ('Truthful advertising is a responsibility towards consumers.', 'Misleading advertisements harm consumers\' interests.', 'a', 'Both true and R explains A.'),
        ('Paying fair wages is a responsibility towards shareholders.', 'Workers expect fair wages and good working conditions.', 'd', 'A is false: fair wages are owed to workers. R is true.'),
        ('Ethical responsibility is enforced by law.', 'Ethical responsibility includes behaviour that society expects but law does not require.', 'd', 'A is false; R is true.')],
    tf=('kinds of social responsibility', [
        'Economic responsibility means producing goods society wants and selling them at a profit.',
        'Obeying the laws of the land is legal responsibility.',
        'Charitable contribution is a discretionary responsibility.'], [
        'Ethical responsibility is required by law.',
        'Discretionary responsibility is compulsory.',
        'Fair dividends are a responsibility towards consumers.',
        'Business has no responsibility towards the community.']),
    cases=[('C4', 'D4', 4, '{f} of {c} pays fair wages, pays taxes on time, avoids misleading advertisements and sponsors a free eye camp every year.',
            [('Identify the interest groups served by each action.', 'Fair wages: workers; taxes: government; honest ads: consumers; eye camp: community.'),
             ('Which kind of responsibility is the eye camp?', 'Discretionary responsibility.')]),
           ('C4', 'D5', 6, '{f} found a defect in a batch of {g} already sold. No law forced a recall, but the company recalled the batch and replaced it free.',
            [('Which kind of responsibility did it fulfil? Justify.', 'Ethical responsibility: morally right action that the law did not require.'),
             ('To which interest group?', 'Consumers.'),
             ('State two more responsibilities towards this group.', 'Quality goods at reasonable prices; truthful advertising; no adulteration or hoarding; after-sales service (any two).')])],
)

POLL = ['Air pollution', 'Water pollution', 'Land pollution', 'Noise pollution']
CH06_ST3 = dict(
    cat='environment term',
    terms=[
        ('Environment', 'The totality of man\'s surroundings, both natural and man-made.'),
        ('Pollution', 'The injection of harmful substances into the environment.'),
        ('Air pollution', 'The presence of harmful gases and particles in the air, caused mainly by industries and vehicles.'),
        ('Water pollution', 'Contamination of water bodies by chemicals and waste dumped by industries and others.'),
        ('Land pollution', 'Dumping of toxic waste onto land, which damages its quality and makes it unfit for use.'),
        ('Noise pollution', 'Unwanted sound from factories and vehicles that causes irritation and health problems.'),
    ],
    lists=[
        ('need', 'reasons for pollution control', [
            ('Reduction of health hazards', 'Pollution control reduces diseases such as cancer and heart and lung complaints.'),
            ('Reduced risk of liability', 'A firm may be held liable to pay compensation to people hurt by its pollution.'),
            ('Cost savings', 'Better control often means less waste and lower production cost.'),
            ('Improved public image', 'People see the firm as socially responsible.'),
            ('Other social benefits', 'Clearer visibility, cleaner buildings, better quality of life and natural products.')], 'role'),
        ('role', 'steps business can take to protect the environment', [
            ('Commitment by top management', 'Top management must be determined to protect the environment.'),
            ('Commitment of the whole workforce', 'All employees must share the commitment.'),
            ('Clear policies on raw materials, technology and waste disposal', 'Use good quality raw materials, superior technology and scientific waste disposal.'),
            ('Compliance with laws', 'Follow the laws for prevention of pollution.'),
            ('Participation in government programmes', 'Join programmes for management of hazardous substances and cleaning of rivers.'),
            ('Periodic assessment', 'Assess pollution control programmes regularly.'),
            ('Educating dealers and suppliers', 'Arrange training on pollution control for dealers and suppliers.')], 'need'),
    ],
    scen=[('Which type of pollution is caused?', POLL, [
        ('A chemical factory near {c} releases untreated effluent into a river.', 'Water pollution', 'Effluent in rivers is water pollution.'),
        ('Smoke from the chimneys of a thermal power plant spreads over {c}.', 'Air pollution', 'Smoke and gases cause air pollution.'),
        ('{f} dumps toxic waste on open land behind its plant.', 'Land pollution', 'Toxic dumping damages land.'),
        ('Machines and generators in a factory in a residential area run all night with loud sound.', 'Noise pollution', 'Unwanted loud sound is noise pollution.'),
        ('Exhaust from the delivery trucks of {f} adds to smog in {c}.', 'Air pollution', 'Vehicle exhaust causes air pollution.'),
        ('Plastic and industrial waste from {f} is buried in fields near {c}.', 'Land pollution', 'Waste dumped on land.')], None),
        ('Which reason for pollution control is highlighted?', ['Reduction of health hazards', 'Reduced risk of liability', 'Cost savings', 'Improved public image'], [
        ('After installing a filter, {f} recovered chemicals from its waste and reused them, cutting costs.', 'Cost savings', 'Less waste means lower production cost.'),
        ('A court ordered a factory to compensate villagers made ill by its waste; other firms took note.', 'Reduced risk of liability', 'Firms can be held liable for damage caused by pollution.'),
        ('Customers praised {f} for its clean production and its sales rose.', 'Improved public image', 'Society sees the firm as responsible.'),
        ('Cases of breathing problems in {c} fell after factories reduced smoke.', 'Reduction of health hazards', 'Pollution control reduces disease.')], None)],
    ars=[
        ('Pollution control can reduce costs for a firm.', 'Better control reduces waste in production.', 'a', 'Both true and R explains A.'),
        ('Business is a major cause of pollution.', 'Industries release effluents, smoke and waste into the environment.', 'a', 'Both true and R explains A.'),
        ('Pollution control is the responsibility of the government alone.', 'Businesses should comply with laws on pollution.', 'd', 'A is false: business also has a role. R is true.'),
        ('Noise pollution is caused by smoke from chimneys.', 'Noise pollution can cause health problems such as hearing loss.', 'd', 'A is false: smoke causes air pollution. R is true.')],
    tf=('business and environmental protection', [
        'Effluents from industries cause water pollution.',
        'Pollution control can improve a firm\'s public image.',
        'Commitment by top management is needed to protect the environment.'], [
        'Pollution control always increases a firm\'s costs and gives no benefit.',
        'Dumping toxic waste on land is a cause of noise pollution.',
        'Business has no role in protecting the environment.',
        'Periodic assessment of pollution control is unnecessary.']),
    cases=[('C4', 'D4', 4, '{f} runs a dyeing and printing plant on the banks of a river near {c}. Villagers complain about dirty water and loud noise at night.',
            [('Identify two types of pollution caused.', 'Water pollution and noise pollution.'),
             ('Suggest two steps {f} should take.', 'Treat effluent before release (scientific waste disposal); reduce or shift noisy operations; comply with pollution laws; periodic assessment (any two).')]),
           ('C4', 'D5', 6, 'The board of {f} sees pollution control only as a cost. A new director argues that it benefits the company too.',
            [('Give three benefits of pollution control the director could cite.', 'Reduction of health hazards, reduced risk of liability, cost savings, improved public image (any three).'),
             ('Suggest three steps to make pollution control effective.', 'Top management commitment, workforce commitment, clear policies on raw material and waste disposal, periodic assessment (any three).')])],
)

ELEM = ['Top management commitment', 'Publication of a code', 'Establishment of compliance mechanisms', 'Involving employees at all levels', 'Measuring results']
CH06_ST4 = dict(
    cat='term',
    terms=[
        ('Business ethics', 'The socially determined moral principles which should govern business activities.'),
        ('Code of conduct', 'A written statement of the ethical principles and rules that employees of a firm must follow.'),
        ('Compliance mechanism', 'A system set up to make sure that actual decisions and actions follow the firm\'s ethical standards.'),
        ('Ethics', 'Principles of right and wrong that guide the conduct of people.'),
    ],
    lists=[
        ('elem', 'elements of business ethics', [
            ('Top management commitment', 'The CEO and top managers must lead and be openly committed to ethical conduct.'),
            ('Publication of a code', 'A written code lays down principles such as fairness, honesty and quality.'),
            ('Establishment of compliance mechanisms', 'Systems such as careful hiring, training and reporting ensure the code is followed.'),
            ('Involving employees at all levels', 'Employees at every level must take part in ethics programmes.'),
            ('Measuring results', 'Ethical performance must be monitored and audited, though it is hard to measure exactly.')], None),
        ('unethical', 'examples of unethical business practices', [
            ('Adulteration', 'Mixing inferior substances in products.'),
            ('Misleading advertisements', 'Making false claims about products.'),
            ('Black marketing and hoarding', 'Holding back goods to raise prices.'),
            ('Tax evasion', 'Hiding income to avoid paying tax.'),
            ('Bribery', 'Offering money to officials for favours.')], None),
    ],
    scen=[('Which element of business ethics is illustrated?', ELEM, [
        ('The CEO of {f} announces at every meeting that honesty matters more than any sales target.', 'Top management commitment', 'Top managers openly lead on ethics.'),
        ('{f} prints and gives every employee a booklet listing its principles of honesty and fairness.', 'Publication of a code', 'A written code is published.'),
        ('{f} sets up a hotline where employees can report unethical behaviour in confidence.', 'Establishment of compliance mechanisms', 'Reporting systems ensure the code is followed.'),
        ('Workers, supervisors and managers of {f} all attend ethics workshops together.', 'Involving employees at all levels', 'Employees at every level take part.'),
        ('{f} audits each year whether its departments followed its ethical standards.', 'Measuring results', 'Ethical performance is monitored and audited.'),
        ('{f} checks the integrity of candidates before hiring and trains new staff on its values.', 'Establishment of compliance mechanisms', 'Careful hiring and training are compliance mechanisms.')], None)],
    ars=[
        ('Top management commitment is essential for business ethics.', 'Employees follow the example set by top managers.', 'a', 'Both true and R explains A.'),
        ('Business ethics and social responsibility are closely related.', 'Both are concerned with the conduct of business towards society.', 'a', 'Both true and R explains A.'),
        ('Ethical results can be measured exactly.', 'Firms can audit their ethical performance.', 'd', 'A is false: they are hard to measure exactly. R is true.'),
        ('Publication of a code is an element of business ethics.', 'A code removes the need for top management commitment.', 'c', 'A is true; R is false.')],
    tf=('business ethics', [
        'Business ethics are socially determined moral principles.',
        'Publication of a code is an element of business ethics.',
        'Employees at all levels should be involved in ethics programmes.'], [
        'Business ethics are the same as the laws of the land.',
        'Only top managers need to follow business ethics.',
        'Adulteration is an ethical business practice.',
        'Ethical results can be measured precisely like profits.']),
    cases=[('C4', 'D4', 4, 'After a scandal in which sales staff of {f} misled customers, the new CEO wants to make the company ethical.',
            [('Suggest three elements of business ethics to put in place.', 'Top management commitment, publication of a code, compliance mechanisms, involving employees, measuring results (any three).'),
             ('Which unethical practice did the staff follow?', 'Misleading customers through false claims (misleading advertising or selling).')]),
           ('C4', 'D5', 6, '{f} has a code of conduct, but employees say it is only on paper because managers ignore it and no one checks.',
            [('Which elements of business ethics are missing?', 'Top management commitment, compliance mechanisms and measuring results.'),
             ('Explain how each can be put in place.', 'Managers lead by example; set up hiring checks, training and reporting channels; conduct ethics audits.'),
             ('Why must employees at all levels be involved?', 'Ethics programmes succeed only when everyone takes part and owns them.')])],
)

FAMILIES = {S + k: facts(v) for k, v in {
    '04-st1': CH04_ST1, '04-st2': CH04_ST2, '04-st3': CH04_ST3, '04-st4': CH04_ST4,
    '05-st1': CH05_ST1, '05-st2': CH05_ST2, '05-st3': CH05_ST3,
    '06-st1': CH06_ST1, '06-st2': CH06_ST2, '06-st3': CH06_ST3, '06-st4': CH06_ST4,
}.items()}
