"""CBSE class 11 entrepreneurship (066) families: chapters 3 (st2-st4), 5, 6 and 7, and the FAMILIES map for chapters 3-7.

New fact tables here: legal compliances for a start-up (ch03-st4), market and market structures, market research,
segmentation-targeting-positioning (ch05-st1..st3), types of resources, human resources and professionals, bank
and other start-up finance, and government schemes (ch07). Topics shared with the class 12 syllabus use the copied
tables in g11_entrepreneurship_c.py; chapter 6 uses the computed families in g11_entrepreneurship_num.py.
"""
from __future__ import annotations

from g11_accountancy_kit import FF
from g12_business_a import spec
from g11_entrepreneurship_a import efacts, S
import g11_entrepreneurship_c as C
import g11_entrepreneurship_num as N

# ================================================================ ch03 st4 legal compliances (with copied forms of business)

CH03_ST4_LEGAL = spec('''
T: Udyam registration | The free online registration of micro, small and medium enterprises with the Ministry of MSME, which gives an Udyam Registration Number.
T: GST registration | Registration under the Goods and Services Tax law, needed when turnover crosses the threshold or for inter-state supply, which gives a GSTIN.
T: PAN | The Permanent Account Number issued by the Income Tax Department, needed by every business for tax purposes.
T: FSSAI licence | The registration or licence from the Food Safety and Standards Authority of India needed by every food business.
T: Shop and establishment registration | The registration of shops, offices and other establishments under the state's shops and establishments law.
T: Certificate of incorporation | The certificate issued by the Registrar of Companies that brings a company into existence as a legal person.
L: comp | legal compliances for a new start-up | -
- Choosing and registering the legal form | Registering as a partnership, LLP or company, or operating as a proprietorship.
- PAN and TAN | Obtaining tax identity numbers for income tax and tax deducted at source.
- GST registration | Registering for GST when required by turnover or nature of supply.
- Shop and establishment registration | Registering the premises under the state's law.
- Trade or industry-specific licences | Such as an FSSAI licence for food or a drug licence for medicines.
- Udyam registration | Registering as an MSME to get access to schemes and priority lending.
- Intellectual property protection | Registering trademarks, patents or designs where needed.
L: why | reasons for following legal compliances | -
- Avoid penalties | Non-compliance leads to fines, closure or prosecution.
- Build trust | Customers, suppliers and banks prefer registered businesses.
- Access to finance and schemes | Banks and government schemes ask for registrations.
- Smooth operations | Licences prevent interruptions by authorities.
- Protection of the business | Registration of IP and contracts protects the venture's rights.
Q: Which registration or licence does the start-up need? | FSSAI licence; Udyam registration; Certificate of incorporation; Trademark registration; GST registration | -
- {p} is opening a cloud kitchen in {c} that will sell meals online. | FSSAI licence | Every food business needs FSSAI registration or a licence.
- {p}'s small manufacturing unit wants to be recognised as an MSME to get priority-sector loans. | Udyam registration | Udyam registration identifies the unit as an MSME.
- {p} and {p2} want their start-up to become a private limited company. | Certificate of incorporation | A company comes into existence when the Registrar issues the certificate.
- {f} wants exclusive rights over its brand name 'GreenCup'. | Trademark registration | It protects the brand name.
- {f} has started selling goods to buyers in other states. | GST registration | Inter-state supply of goods requires GST registration.
A: A food business must obtain FSSAI registration or a licence. | Food safety law requires every food business to be registered or licensed. | a | Both true; R explains A.
A: Legal compliance is a waste of time for start-ups. | Non-compliance can lead to fines and closure. | d | A is false: compliance protects the business. R is true.
A: Udyam registration helps MSMEs access government schemes. | Many schemes and priority loans are open to registered MSMEs. | a | Both true; R explains A.
A: A company comes into existence on getting the certificate of incorporation. | The certificate is issued by the Registrar of Companies. | b | Both are true, but R only names the issuing authority and does not explain why the company comes into existence then.
TT: legal compliances for a start-up
S+: Every business needs a PAN for tax purposes.
S+: A food business needs FSSAI registration or a licence.
S+: Udyam registration is done online.
S+: A company is incorporated by the Registrar of Companies.
S-: A start-up never needs any licence.
S-: GST registration is issued by the FSSAI.
S-: A trademark is registered by the Registrar of Companies.
S-: Legal compliance increases the risk of penalties.
K: C4 D4 5 | {p} and {p2} plan to start a packaged-juice company in {c}, sell in several states, and use the brand name 'FreshSip'. They want limited liability and later plan to bring in investors. | Suggest a suitable legal form. => Private limited company (limited liability; can issue shares to investors). || List four registrations or licences they need. => Certificate of incorporation; PAN and TAN; GST registration (inter-state supply); FSSAI licence; trademark registration for 'FreshSip'; Udyam registration (any four).
K: C3 D3 3 | {p} has started a small tailoring shop in {c} without any registration. | State three risks of not following legal compliances. => Penalties or closure; difficulty in getting bank loans or schemes; loss of customer and supplier trust (any three).
''', cat='term')

# ================================================================ ch05 Understanding the market

CH05_ST1 = spec('''
T: Market | A set of buyers and sellers of a product, and the arrangements through which they exchange it.
T: Perfect competition | A market with a very large number of buyers and sellers of an identical product, where no single firm can influence the price.
T: Monopoly | A market with a single seller of a product that has no close substitute, with barriers to entry.
T: Monopolistic competition | A market with many sellers of differentiated products, such as brands of soap or restaurants.
T: Oligopoly | A market with a few large sellers, each of whose decisions affects the others, such as telecom services.
T: Product differentiation | Making a product different from rivals' products through brand, design, quality or service.
L: types | classifications of markets | -
- On the basis of area | Local, regional, national and international markets.
- On the basis of time | Very short period, short period and long period markets.
- On the basis of nature of goods | Consumer goods markets and industrial goods markets.
- On the basis of competition | Perfect competition, monopolistic competition, oligopoly and monopoly.
- On the basis of mode of transaction | Physical markets and online markets.
L: pc | features of perfect competition | -
- Very large number of buyers and sellers | No single buyer or seller can influence the price.
- Homogeneous product | All sellers sell identical products.
- Free entry and exit | Firms can join or leave the industry freely.
- Perfect knowledge | Buyers and sellers know the market price.
- Uniform price | One price prevails in the market.
P: monopoly | perfect competition
- number of sellers | one seller | a very large number of sellers
- nature of product | no close substitute | identical (homogeneous) products
- control over price | the seller has considerable control | no single seller can influence the price
- entry of new firms | barriers to entry | free entry and exit
Q: Which market structure is described? | Perfect competition; Monopoly; Monopolistic competition; Oligopoly | -
- Hundreds of farmers sell the same variety of wheat in a large mandi, and none can change the price. | Perfect competition | Many sellers of an identical product.
- Only one company is allowed to supply electricity in {c}, and there is no substitute. | Monopoly | A single seller with no close substitute.
- Many restaurants in {c} each offer their own menu, ambience and brand. | Monopolistic competition | Many sellers of differentiated products.
- Three large companies supply most of the mobile telephone services in the country and watch each other's prices. | Oligopoly | A few large interdependent sellers.
- Dozens of brands of toothpaste compete with different flavours and claims. | Monopolistic competition | Many sellers with product differentiation.
- Two airlines operate almost all flights on a route and react to each other's fares. | Oligopoly | A few interdependent sellers.
A: A firm under perfect competition cannot influence the market price. | There are a very large number of sellers of an identical product. | a | Both true; R explains A.
A: A monopolist faces many close competitors. | A monopolist is the single seller of a product with no close substitute. | d | A is false; R is true.
A: Advertising is common under monopolistic competition. | Firms sell differentiated products and try to attract buyers to their brand. | a | Both true; R explains A.
A: Firms in an oligopoly are interdependent. | Each of the few large firms is affected by the decisions of the others. | a | Both true; R explains A.
TT: markets and market structures
S+: Perfect competition has a very large number of sellers.
S+: A monopolist is the single seller of a product.
S+: Monopolistic competition involves product differentiation.
S+: An oligopoly has a few large sellers.
S-: A monopoly has many sellers of identical products.
S-: Products are differentiated under perfect competition.
S-: An oligopoly has only one seller.
S-: Online markets are not markets.
K: C4 D4 5 | {p} plans to open a café in {c}, where there are already many cafés, each with its own style, menu and loyal customers. {His} cousin wants to sell rice in a large wholesale market where hundreds of traders sell the same variety at one price. | Identify the market structure each will face. => {p}: monopolistic competition (many sellers, differentiated products); cousin: perfect competition (many sellers, identical product, uniform price). || What should {p} do to succeed? => Differentiate the café (theme, menu, service) and promote the brand. || Can the cousin charge a higher price? => No; under perfect competition one price prevails and buyers will go elsewhere.
K: C3 D3 3 | A handicraft seller in {c} has moved from a weekly local fair to selling across India and abroad on an online marketplace. | Classify both markets on the basis of area and mode of transaction. => Local and physical market; national/international and online market. || State one advantage of the change. => Wider customer base; sales at any time; lower cost of reaching distant buyers (any one).
''', cat='term')

CH05_ST2 = spec('''
T: Market research | The systematic collection and analysis of information about customers, competitors and the market to support business decisions.
T: Primary data | Data collected first-hand by the researcher for a specific purpose, such as through surveys or interviews.
T: Secondary data | Data already collected by others, such as census reports, government publications, trade journals and websites.
T: Questionnaire | A set of written questions used to collect information from respondents.
T: Focus group | A small group of people led by a moderator in a discussion about a product or idea.
T: Sample | A small group selected from the population to represent it in a survey.
L: meth | methods of collecting primary data | -
- Survey | Asking a sample of people a set of questions, in person, by phone or online.
- Personal interview | A face-to-face conversation to get detailed views.
- Observation | Watching how customers behave, for example in a shop.
- Focus group discussion | A guided discussion with a small group of target customers.
- Test marketing | Selling the product in a small area to see how it is received.
L: sec | sources of secondary data | -
- Census and government reports | Population, income and industry data.
- Trade journals and magazines | Information on industry trends.
- Websites and online databases | Data on competitors and markets.
- Reports of industry associations | Statistics and studies of an industry.
- Company records | Past sales and customer records of the firm itself.
P: primary data | secondary data
- source | collected first-hand by the researcher | already collected by others
- cost and time | more costly and time-consuming | cheaper and quicker
- suitability | collected for the specific purpose, so highly suitable | may not fully suit the present purpose
Q: Which method of market research is being used? | Survey; Personal interview; Observation; Focus group discussion; Test marketing; Secondary data | -
- {p} gave a printed set of ten questions to 300 college students in {c} about their snack habits. | Survey | A sample is asked a set of questions.
- {p} stood in a supermarket for a week noting which juice brands shoppers picked up first. | Observation | Customer behaviour is watched.
- {p} invited eight young mothers to discuss what they want in a baby-food brand, with {him} guiding the discussion. | Focus group discussion | A small group discusses with a moderator.
- {f} sold its new biscuit only in one city for three months before launching it nationally. | Test marketing | The product is tried in a small area first.
- {p} used census figures and a government report to estimate the number of elderly people in {his} district. | Secondary data | Data already collected by others is used.
- {p} met the owner of a large hotel and talked for an hour about what the hotel looks for in a laundry service. | Personal interview | A detailed face-to-face conversation.
A: Secondary data is cheaper to obtain than primary data. | It has already been collected by others. | a | Both true; R explains A.
A: Primary data is always out of date. | Primary data is collected first-hand for the present purpose. | d | A is false: primary data is current. R is true.
A: Test marketing reduces the risk of a national launch. | It shows how customers react in a small area first. | a | Both true; R explains A.
A: Market research helps an entrepreneur take better decisions. | It provides facts about customers and competitors. | a | Both true; R explains A.
TT: market research
S+: A survey collects primary data.
S+: Census reports are a source of secondary data.
S+: Observation means watching customer behaviour.
S+: A focus group is a small guided discussion.
S-: Secondary data is collected first-hand by the researcher.
S-: Market research is done only after the business fails.
S-: A questionnaire is a source of secondary data.
S-: Test marketing means selling the product in every city at once.
K: C4 D4 5 | {p} wants to launch a protein drink for gym-goers in {c}. {He} first reads industry reports on the health-drink market, then asks 200 gym members to fill in a short form, watches what members buy at gym counters, and finally sells the drink in two gyms for a month. | Identify the market research methods used. => Secondary data (industry reports); survey (form filled by 200 members); observation (watching purchases); test marketing (two gyms for a month). || State one advantage and one limitation of primary data. => Advantage – suited to the purpose and current; limitation – costly and time-consuming.
K: C3 D3 3 | {p} has little money and wants to know how many households in {his} town might buy solar water heaters. | Suggest one source of secondary data and one primary method. => Census or government reports / electricity board data; a small survey of households. || Why start with secondary data? => It is cheaper and quicker.
''', cat='term')

CH05_ST3 = spec('''
T: Market segmentation | Dividing a market into distinct groups of customers with similar needs, characteristics or behaviour.
T: Targeting | Choosing one or more segments that the enterprise will serve.
T: Positioning | Creating a clear and distinct image of the product in the minds of target customers compared with rivals.
T: Customer persona | A detailed, imaginary profile of a typical customer in the target segment, including age, needs, habits and problems.
T: Niche market | A small, well-defined segment with specific needs that larger firms often ignore.
T: Psychographic segmentation | Dividing customers by lifestyle, values, interests and personality.
L: bases | bases of market segmentation | -
- Geographic | By region, city, rural or urban area, or climate.
- Demographic | By age, gender, income, occupation, education or family size.
- Psychographic | By lifestyle, values, interests and personality.
- Behavioural | By usage rate, benefits sought, loyalty or occasion of purchase.
L: tgt | targeting strategies | -
- Undifferentiated marketing | One offer for the whole market.
- Differentiated marketing | Different offers for different segments.
- Concentrated (niche) marketing | Focus on one small segment.
- Micro-marketing | Tailoring offers to local areas or even individuals.
P: segmentation | positioning
- meaning | dividing the market into groups | creating an image of the product in customers' minds
- focus | the customers | the product as perceived by customers
- order | done first | done after choosing the target segment
Q: Which basis of segmentation is used? | Geographic; Demographic; Psychographic; Behavioural | -
- {f} sells woollen clothes only in the hill states and in north India during winter. | Geographic | Region and climate are used.
- {f} makes a separate range of shoes for children aged 5 to 12. | Demographic | Age is used.
- {f} designs trekking gear for people who love adventure and the outdoors. | Psychographic | Lifestyle and interests are used.
- {f} offers a discount card to customers who buy from it every week. | Behavioural | Usage rate and loyalty are used.
- {f} sells low-priced sachets of shampoo for low-income buyers. | Demographic | Income is used.
- {f} sells special gift packs of sweets only before Diwali. | Behavioural | The occasion of purchase is used.
A: Market segmentation helps a small firm use its resources well. | It focuses efforts on the customers most likely to buy. | a | Both true; R explains A.
A: Positioning is done before identifying the target segment. | Positioning creates an image in the minds of target customers. | d | A is false: the target segment is chosen first. R is true.
A: A customer persona helps in designing the product. | It describes the needs, habits and problems of a typical customer. | a | Both true; R explains A.
A: Concentrated marketing suits an enterprise with limited resources. | It focuses on one small segment. | a | Both true; R explains A.
TT: segmentation, targeting and positioning
S+: Age and income are demographic bases.
S+: Lifestyle is a psychographic basis.
S+: Positioning creates an image in customers' minds.
S+: A customer persona is a profile of a typical customer.
S-: Geographic segmentation uses lifestyle.
S-: Targeting means dividing the market into segments.
S-: A niche market is the whole market.
S-: Positioning has nothing to do with competitors.
K: C4 D4 5 | {p} plans a range of healthy tiffin meals in {c}. {He} imagines a typical customer: "Riya, 28, software engineer, lives alone, works long hours, wants low-oil home-style food, orders through apps." {He} will serve only young working professionals and advertise the meals as 'Ghar ka khana, office pe'. | What is the description of Riya called, and why is it useful? => Customer persona; it helps design the product, price and promotion for real needs. || Identify the bases of segmentation used. => Demographic (age, occupation); psychographic or behavioural (lifestyle, ordering habit). || Identify the targeting strategy and the positioning. => Concentrated (niche) marketing to young professionals; positioned as home-style food delivered at the office.
K: C3 D3 3 | {f} sells the same plain notebook to everyone, while its rival sells separate notebooks for school children, college students and artists. | Name the targeting strategy of each. => {f}: undifferentiated marketing; rival: differentiated marketing. || Give one advantage of the rival's strategy. => Meets the needs of each segment better, increasing sales and loyalty.
''', cat='term')

# ================================================================ ch07 Resource mobilisation

CH07_ST1 = spec('''
T: Resources | The inputs, such as people, materials, money and knowledge, that an enterprise needs to produce and sell.
T: Human resources | The people who work in or for the enterprise, with their skills and knowledge.
T: Physical resources | Tangible assets such as land, buildings, machinery, equipment and raw material.
T: Financial resources | The money needed to start and run the enterprise, from owners, lenders and investors.
T: Intangible resources | Non-physical assets such as goodwill, brand, patents, technology, knowledge and networks.
T: Resource mobilisation | The process of identifying, obtaining and arranging the resources a venture needs.
L: types | types of resources needed by an enterprise | -
- Human resources | Employees, partners, mentors and professionals.
- Physical resources | Land, building, machinery, equipment and raw material.
- Financial resources | Owners' capital, loans and investors' funds.
- Intangible resources | Brand, goodwill, patents, technology and networks.
L: steps | steps in resource mobilisation | -
- Identifying the resources needed | Listing people, assets and funds required.
- Estimating the quantity and cost | Working out how much of each is needed and what it will cost.
- Finding sources | Locating suppliers, lenders, investors and staff.
- Acquiring the resources | Buying, hiring, leasing or raising them.
- Using resources efficiently | Avoiding waste and idle capacity.
P: physical resources | intangible resources
- nature | tangible assets that can be seen and touched | non-physical assets
- examples | machinery, building, raw material | brand, goodwill, patents, networks
- valuation | easier to value | harder to value
Q: Which type of resource is this? | Human resources; Physical resources; Financial resources; Intangible resources | -
- {p} bought two sewing machines and a stock of cloth for {his} boutique. | Physical resources | Machines and raw material are tangible assets.
- {p} hired a skilled chef and two helpers for {his} restaurant. | Human resources | People and their skills are human resources.
- {p} raised ₹10 lakh from a bank loan and {his} own savings. | Financial resources | Money is a financial resource.
- {f}'s well-known brand name helps it sell at a higher price. | Intangible resources | A brand is a non-physical asset.
- {p} has a patent on a new water purifier design. | Intangible resources | A patent is an intangible asset.
- {p} rented a shop and bought shelves and a billing machine. | Physical resources | Premises and equipment are tangible.
A: A brand is an intangible resource. | It is a non-physical asset that adds value. | a | Both true; R explains A.
A: Human resources include only the owner of the business. | Employees, partners and professionals are also human resources. | d | A is false; R is true.
A: Resource mobilisation begins with identifying the resources needed. | Resources cannot be arranged until the needs are known. | a | Both true; R explains A.
A: Machinery is a physical resource. | It is a tangible asset used in production. | a | Both true; R explains A.
TT: types of resources
S+: Machinery is a physical resource.
S+: Goodwill is an intangible resource.
S+: Bank loans are a financial resource.
S+: Employees are human resources.
S-: A patent is a physical resource.
S-: Raw material is an intangible resource.
S-: Resources are not needed to start a business.
S-: Human resources means only machines.
K: C4 D4 5 | {p} is starting a bakery in {c}. {He} has rented a shop, bought an oven, hired two bakers, taken a ₹5 lakh loan, and registered the brand name 'CrustCraft'. {His} mentor at an incubator introduces {him} to suppliers. | Classify the resources {p} has mobilised. => Physical: shop, oven; human: two bakers, mentor; financial: ₹5 lakh loan; intangible: brand 'CrustCraft', network of suppliers. || State two steps of resource mobilisation {he} followed. => Identifying resources needed; finding sources; acquiring them (any two).
K: C3 D3 3 | Two start-ups in {c} have the same machines and funds, but one has a respected brand and strong contacts with buyers. | Which type of resource gives it an advantage? => Intangible resources (brand and networks). || Why are such resources hard for rivals to copy? => They are built over time through reputation and relationships.
''', cat='term')

CH07_ST2 = spec('''
T: Recruitment | The process of searching for prospective employees and encouraging them to apply for jobs.
T: Selection | The process of choosing the most suitable candidates from among those who apply.
T: Job description | A statement of the duties, responsibilities and working conditions of a job.
T: Chartered accountant | A professional who handles accounts, audit, taxation and financial advice for a business.
T: Company secretary | A professional who handles company law compliance, board meetings and statutory filings.
T: Legal adviser | A lawyer who drafts contracts, protects intellectual property and handles legal disputes.
T: Banker | A person in a bank who arranges loans, accounts and other financial services for a business.
L: hr | steps in selecting and using human resources in a new venture | -
- Estimating staff requirements | Deciding the number and type of people needed.
- Job analysis | Preparing job descriptions and the qualifications needed.
- Recruitment | Finding candidates through referrals, job portals, advertisements and campus visits.
- Selection | Tests and interviews to choose the most suitable people.
- Training | Teaching new staff the skills and methods of the enterprise.
- Retention and motivation | Fair pay, recognition and growth to keep good staff.
L: prof | roles of professionals for an entrepreneur | -
- Chartered accountant | Accounts, audit, tax returns, GST and financial planning.
- Company secretary | Company law compliance, board meetings and statutory filings.
- Lawyer | Contracts, intellectual property, licences and disputes.
- Banker | Loans, working capital, accounts and payment services.
- Mentor | Guidance and advice based on business experience.
P: recruitment | selection
- meaning | searching for candidates and encouraging them to apply | choosing the most suitable candidates
- nature | positive process (increases applicants) | negative process (rejects unsuitable applicants)
- order | comes first | follows recruitment
Q: Which professional should the entrepreneur approach? | Chartered accountant; Company secretary; Lawyer; Banker | -
- {p} needs to file {his} firm's income tax return and GST returns. | Chartered accountant | Tax returns are handled by a chartered accountant.
- {f} needs an agreement drafted with its distributor and wants to register its logo. | Lawyer | Contracts and IP are handled by a lawyer.
- {p} needs a working capital loan to buy raw material before the festival season. | Banker | Loans are arranged through a banker.
- {f} must hold board meetings and file annual returns with the Registrar of Companies. | Company secretary | Company law compliance is handled by a company secretary.
- {p} wants {his} accounts audited before approaching an investor. | Chartered accountant | Audit is done by a chartered accountant.
- {p} is being sued by a supplier for non-payment. | Lawyer | Legal disputes are handled by a lawyer.
A: Recruitment comes before selection. | Candidates must first apply before the best can be chosen. | a | Both true; R explains A.
A: Selection is called a negative process. | It rejects candidates who are not suitable. | a | Both true; R explains A.
A: A small start-up never needs professionals. | Professionals help with tax, law and finance. | d | A is false: professionals help even small ventures. R is true.
A: Training is needed for new employees. | Training teaches them the skills and methods of the enterprise. | a | Both true; R explains A.
TT: human resources and professionals
S+: Recruitment means searching for candidates.
S+: A chartered accountant handles audit and tax.
S+: A lawyer drafts contracts.
S+: Selection follows recruitment.
S-: Selection comes before recruitment.
S-: A banker drafts legal contracts.
S-: Training is not needed for new staff.
S-: A company secretary audits accounts.
K: C4 D4 5 | {p} is starting a furniture company in {c}. {He} needs ten carpenters, a supervisor, a person to keep accounts and file taxes, someone to handle board meetings and filings, a contract with a timber supplier, and a loan for machines. | Outline the steps {he} should follow to hire the carpenters. => Estimate requirements; job analysis; recruitment (referrals, portals); selection (skill test, interview); training. || Name the professional for each other need. => Accounts and taxes – chartered accountant; board meetings and filings – company secretary; timber contract – lawyer; loan – banker.
K: C3 D3 3 | A start-up in {c} hired five sales staff through friends' referrals without any test, and three left within a month. | Which steps of human resource selection were weak? => Job analysis and selection (no tests or interviews). || Suggest two improvements. => Prepare job descriptions; use tests and interviews; train new staff; offer fair pay and recognition (any two).
''', cat='term')

CH07_ST3_LOANS = spec('''
T: Term loan | A loan from a bank for a fixed period, usually to buy fixed assets, repaid in instalments with interest.
T: Working capital loan | A short-term bank loan or cash credit to meet day-to-day expenses such as raw material and wages.
T: Collateral | An asset pledged as security for a loan.
T: CGTMSE | The Credit Guarantee Fund Trust for Micro and Small Enterprises, set up by the Government of India and SIDBI, which guarantees loans to micro and small enterprises given without collateral.
T: Equity | Funds raised by giving a share of ownership in the business.
T: Debt | Borrowed funds that must be repaid with interest, whatever the result of the business.
L: cf | types of crowdfunding | -
- Donation-based | People give money for a cause without expecting anything in return.
- Reward-based | Backers receive a product or reward in return for their money.
- Equity-based | Backers receive a share in the business.
- Debt-based (peer-to-peer lending) | Backers lend money and are repaid with interest.
L: fac | factors to consider while choosing a source of finance | -
- Amount needed | Large sums may need investors or banks.
- Cost of funds | Interest or share of ownership given up.
- Period of need | Long-term needs suit term loans or equity; short-term needs suit working capital loans.
- Control | Equity investors may want a say in management.
- Risk | Debt must be repaid even in a loss.
- Security available | Banks may ask for collateral.
P: debt | equity
- ownership | no share of ownership is given | investors get a share of ownership
- return | fixed interest must be paid | dividends or gains depend on profits
- repayment | must be repaid by a fixed date | not repayable while the business continues
- risk to the entrepreneur | higher, since interest is due even in a loss | lower, since no fixed payment is due
Q: Which source of finance is shown? | Term loan; Working capital loan; Crowdfunding; Bootstrapping; Angel investor | -
- {p} took a five-year bank loan to buy machinery, repayable in monthly instalments. | Term loan | A fixed-period loan for fixed assets.
- {f} uses a cash credit limit from its bank to buy raw material and pay wages each month. | Working capital loan | It meets day-to-day expenses.
- {p} raised money from 1,500 people online by promising each of them one of the first smart bottles. | Crowdfunding | Many small backers contributed online (reward-based).
- {p} started {his} coaching centre using only {his} savings and the fees earned. | Bootstrapping | No outside funds were used.
- A retired executive invested ₹20 lakh in {p}'s start-up for a 10% stake and offered to mentor {him}. | Angel investor | A wealthy individual invests personal money for equity.
A: Debt increases the financial risk of the entrepreneur. | Interest and repayment are due even if the business makes a loss. | a | Both true; R explains A.
A: Equity finance must be repaid on a fixed date. | Equity investors become part-owners of the business. | d | A is false: equity is not repayable on a fixed date. R is true.
A: CGTMSE helps small firms that lack security. | It guarantees collateral-free loans given to micro and small enterprises. | a | Both true; R explains A.
A: Reward-based crowdfunding gives backers a share in the company. | Backers in reward-based crowdfunding receive a product or reward. | d | A is false: they get a reward, not shares. R is true.
TT: sources of start-up finance
S+: A term loan is used to buy fixed assets.
S+: A working capital loan meets day-to-day expenses.
S+: Equity investors share in ownership.
S+: Crowdfunding raises small amounts from many people.
S-: Interest on debt is paid only when there is a profit.
S-: A working capital loan is used to buy land.
S-: Equity must be repaid with fixed interest.
S-: Crowdfunding means a loan from a single bank.
K: C4 D4 5 | {p} needs ₹30 lakh for machines and ₹5 lakh every month for raw material and wages for {his} new garment unit in {c}. {He} has no property to offer as security and does not want to give up ownership. | Suggest a source for each need, with reasons. => Machines – term loan (long-term, fixed assets), possibly under a CGTMSE guarantee since there is no collateral; monthly needs – working capital loan or cash credit. || Why not equity? => {He} does not want to give up ownership and control. || State one risk of debt. => Interest and instalments must be paid even in a loss.
K: C3 D3 3 | {p} has designed a smart lunchbox and wants to test demand before producing it. | Suggest a source of finance that also tests demand. => Reward-based crowdfunding. || Give two reasons. => Backers pre-order the product, showing demand; no loan or loss of ownership; publicity (any two).
''', cat='term')

CH07_ST4 = spec('''
T: Startup India | The Government of India initiative launched on 16 January 2016 to build a start-up ecosystem through recognition, tax benefits, easier compliance and funding support.
T: DPIIT recognition | Recognition of an eligible entity as a start-up by the Department for Promotion of Industry and Internal Trade, which opens Startup India benefits.
T: PMMY (MUDRA) | The Pradhan Mantri MUDRA Yojana, launched in 2015, under which banks and other lenders give collateral-free loans to non-farm micro enterprises.
T: Stand-Up India | The scheme launched in 2016 that facilitates bank loans between ₹10 lakh and ₹1 crore to at least one SC or ST borrower and at least one woman borrower per bank branch for a greenfield enterprise.
T: Fund of Funds for Startups | A fund managed by SIDBI under Startup India that invests in SEBI-registered venture funds, which in turn invest in start-ups.
T: Atal Innovation Mission | The NITI Aayog initiative that promotes innovation through Atal Tinkering Labs in schools and Atal Incubation Centres.
L: si | benefits under Startup India | -
- Recognition by DPIIT | Recognised start-ups can use the scheme's benefits.
- Self-certification | Start-ups can self-certify compliance under certain labour and environmental laws.
- Tax benefits | Eligible start-ups can get an income tax holiday for three consecutive years.
- Faster and cheaper patents | Patent applications get fast-tracking and fee rebates.
- Funding support | Fund of Funds managed by SIDBI and the Seed Fund Scheme.
- Easier exit | Faster winding up for start-ups under insolvency law.
L: mudra | categories of loans under MUDRA | -
- Shishu | The smallest loans, up to ₹50,000, for businesses just starting.
- Kishore | Loans above ₹50,000 and up to ₹5 lakh.
- Tarun | Larger loans above ₹5 lakh for established micro enterprises.
P: MUDRA | Stand-Up India
- purpose | loans to non-farm micro enterprises | loans for new (greenfield) enterprises of SC, ST and women entrepreneurs
- loan size | small loans in Shishu, Kishore and Tarun categories | between ₹10 lakh and ₹1 crore
- beneficiaries | any eligible micro-entrepreneur | SC or ST and women entrepreneurs
Q: Which scheme is most suitable? | Startup India; MUDRA (PMMY); Stand-Up India; Atal Innovation Mission | -
- {p}, a woman entrepreneur, wants a bank loan of ₹60 lakh to set up a new food-processing unit. | Stand-Up India | It supports greenfield enterprises of women and SC/ST entrepreneurs with loans of ₹10 lakh to ₹1 crore.
- {p} wants a loan of ₹40,000 to buy a sewing machine and start tailoring from home. | MUDRA (PMMY) | Small collateral-free loans (Shishu) are given to micro enterprises.
- {p}'s technology firm wants recognition, a tax holiday and fast-track patent filing. | Startup India | These benefits are given to DPIIT-recognised start-ups.
- A school in {c} wants a lab where students can build robots and prototypes. | Atal Innovation Mission | It sets up Atal Tinkering Labs in schools.
- {p} runs a tea stall and needs ₹2 lakh to open a small snack shop next to it. | MUDRA (PMMY) | Loans up to ₹5 lakh fall under the Kishore category.
A: MUDRA loans help micro enterprises. | They give collateral-free loans to non-farm micro enterprises. | a | Both true; R explains A.
A: Stand-Up India supports only large companies. | It facilitates loans to SC, ST and women entrepreneurs for greenfield enterprises. | d | A is false; R is true.
A: DPIIT recognition is important for a start-up. | Startup India benefits are available to recognised start-ups. | a | Both true; R explains A.
A: Atal Tinkering Labs promote innovation among school students. | They give students tools to build prototypes. | a | Both true; R explains A.
TT: government schemes for entrepreneurs
S+: Startup India was launched in January 2016.
S+: Shishu is the smallest category of MUDRA loans.
S+: Stand-Up India supports SC, ST and women entrepreneurs.
S+: The Fund of Funds for Startups is managed by SIDBI.
S-: MUDRA loans are only for large industries.
S-: Stand-Up India loans are for existing large firms only.
S-: Startup India was launched in 1991.
S-: Atal Tinkering Labs are set up in banks.
K: C4 D4 5 | Three friends in {c}: {p} wants ₹30,000 to start a mobile-recharge kiosk; {p2}, a woman, wants ₹75 lakh to set up a new garment factory; {p3} has a technology start-up and wants a tax holiday and help with patents. | Suggest the most suitable scheme for each, with a reason. => {p} – MUDRA Shishu loan (small collateral-free loan for a micro enterprise); {p2} – Stand-Up India (₹10 lakh to ₹1 crore for a woman's greenfield enterprise); {p3} – Startup India (DPIIT recognition, tax holiday, fast-track patents). || State two other benefits of Startup India. => Self-certification under some laws; Fund of Funds; easier exit (any two).
K: C3 D3 3 | {p} wants to open a small beauty parlour and needs ₹3 lakh but has no collateral. | Which scheme can help? => MUDRA (PMMY). || Under which category will the loan fall? => Kishore (above ₹50,000 and up to ₹5 lakh).
''', cat='term')


def _merge(*specs):
    out = []
    for sp in specs:
        out += efacts(sp)
    return out


FAMILIES = {
    S + '03-st2': _merge(C.X12_CH01_ST3, C.X12_CH01_ST4),
    S + '03-st3': efacts(C.X12_CH02_ST2),
    S + '03-st4': _merge(C.X12_CH02_ST1, CH03_ST4_LEGAL),
    S + '05-st1': efacts(CH05_ST1),
    S + '05-st2': efacts(CH05_ST2),
    S + '05-st3': efacts(CH05_ST3),
    S + '05-st4': efacts(C.X12_CH03_ST1),
    S + '06-st1': efacts(N.CH05_ST1),
    S + '06-st2': efacts(N.CH05_ST2),
    S + '06-st3': efacts(N.CH05_ST3),
    S + '06-st4': efacts(N.CH05_ST4),
    S + '07-st1': efacts(CH07_ST1),
    S + '07-st2': efacts(CH07_ST2),
    S + '07-st3': _merge(C.X12_CH06_ST2, CH07_ST3_LOANS),
    S + '07-st4': efacts(CH07_ST4),
}

FAMILIES[S + '06-st1'] += [FF('C2', 'D2', 'mcq', N.u_margin_mcq), FF('C3', 'D3', 'numerical', N.u_cost2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', N.u_target3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', N.u_compare5, marks=5, kinds=('m5c',))]
FAMILIES[S + '06-st2'] += [FF('C2', 'D2', 'mcq', N.be_mcq), FF('C3', 'D2', 'numerical', N.be2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', N.mos3, marks=3, kinds=('m3c',)),
                           FF('C3', 'D4', 'numerical', N.target3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', N.be5, marks=5, kinds=('m5c',))]
FAMILIES[S + '06-st3'] += [FF('C2', 'D2', 'mcq', N.eoq_mcq), FF('C2', 'D2', 'mcq', N.stock_mcq), FF('C2', 'D2', 'mcq', N.nwc_mcq),
                           FF('C3', 'D3', 'numerical', N.eoq2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', N.stock3, marks=3, kinds=('m3c',)),
                           FF('C3', 'D4', 'numerical', N.fifo3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D5', 'numerical', N.wc5, marks=5, kinds=('m5c',))]
FAMILIES[S + '06-st4'] += [FF('C2', 'D2', 'mcq', N.cr_mcq), FF('C3', 'D2', 'numerical', N.roi2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', N.roe3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', N.ratios5, marks=5, kinds=('m5c',))]
