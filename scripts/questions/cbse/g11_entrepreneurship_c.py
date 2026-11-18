"""CBSE class 11 entrepreneurship (066): theory fact tables shared with the class 12 syllabus.

Copied verbatim from scripts/questions/cbse/g12_entrepreneurship_a.py (validated with its own accuracy pass) so that
this bank does not import another subject's module. Topics: idea generation and feasibility, forms of business
organisation, the business plan, the marketing mix and start-up funding.
"""
from g12_business_a import spec

X12_CH01_ST3 = spec('''
T: Problem identification | Finding out a difficulty faced by people that a product or service could solve.
T: Brainstorming | A group technique in which members freely suggest as many ideas as possible without criticism.
T: Mind-mapping | A diagram that places a central idea in the middle with related ideas branching out from it.
T: Idea generation | The process of producing new ideas for products, services or businesses.
T: Screening of ideas | Comparing ideas against criteria to drop the weak ones and keep the promising ones.
T: Creativity | The ability to produce new and useful ideas.
L: rules | rules of brainstorming | -
- No criticism of ideas | Judgement is postponed so that people speak freely.
- Quantity is welcome | The more ideas, the better the chance of a good one.
- Wild ideas are encouraged | Unusual ideas can lead to new solutions.
- Build on the ideas of others | Ideas are combined and improved.
L: src | sources of ideas for a new venture | -
- Customers' complaints and feedback | Complaints show needs that are not met.
- Existing products and services | Gaps in them suggest improvements.
- Trade fairs and exhibitions | New products and technologies are on display.
- Media and the internet | News and trends point to opportunities.
- Research and development | New technology leads to new products.
- Personal experience and hobbies | Problems faced by the entrepreneur suggest solutions.
L: sel | criteria for selecting a business idea | -
- Demand for the product | There must be enough customers willing to pay.
- Availability of resources | Raw material, skills and funds must be available.
- Profitability | The idea must earn a reasonable return.
- Competition | The level of competition must be manageable.
- Personal interest and skills | The idea should match the entrepreneur's interest and ability.
- Risk involved | The risk must be within limits.
Q: Which technique of idea generation is being used? | Brainstorming; Mind-mapping; Survey of customers; Screening of ideas | -
- {p} and {his} friends sat together and called out as many ideas as possible for a college start-up, writing all of them on a board without judging any. | Brainstorming | Free group suggestion without criticism.
- {p} wrote 'healthy snacks' in the centre of a page and drew branches for millets, packaging, school canteens and gyms. | Mind-mapping | A central idea with branches.
- {p} asked 200 shoppers in {c} what they disliked about local grocery stores. | Survey of customers | Customers are asked about their needs.
- {p} compared ten ideas on demand, cost and risk, and kept only two. | Screening of ideas | Weak ideas are dropped against criteria.
- During a team meeting at {f}, one member's odd suggestion was built upon by others into a workable plan. | Brainstorming | Members build on each other's ideas.
- {p} drew a diagram with 'eco-friendly travel' in the middle and linked it to cycles, electric scooters and car-pooling. | Mind-mapping | Related ideas branch from the central idea.
A: Criticism is not allowed during brainstorming. | Criticism discourages people from suggesting ideas freely. | a | Both true; R explains A.
A: In brainstorming, quality of ideas is more important than quantity. | Wild ideas are encouraged in brainstorming. | d | A is false: quantity is welcome. R is true.
A: Customer complaints are a good source of business ideas. | Complaints show needs that are not being met. | a | Both true; R explains A.
A: Mind-mapping shows links between ideas. | It places a central idea in the middle with related ideas branching out. | a | Both true; R explains A.
A: An idea should be screened before it is selected. | Screening keeps every idea for later use. | c | A is true; R is false: screening drops weak ideas.
TT: idea generation
S+: Brainstorming encourages wild ideas.
S+: A mind map has a central idea with branches.
S+: Customer complaints can be a source of ideas.
S+: Screening helps drop weak ideas.
S-: Ideas are criticised immediately during brainstorming.
S-: A mind map is a list of ideas in alphabetical order.
S-: Demand is not considered while selecting an idea.
S-: Brainstorming aims at a small number of ideas.
K: C4 D4 5 | Students of a school in {c} wanted to start a small business. They first listed every idea anyone could think of without judging, then drew a chart around 'school needs', and finally compared the ideas on demand, resources and profit. | Identify the three steps or techniques used. => Brainstorming; mind-mapping; screening and selection of ideas. || State two rules of the first technique. => No criticism; quantity is welcome; wild ideas encouraged; build on others' ideas (any two). || State one more criterion they could use. => Competition / risk involved / personal interest and skills.
K: C3 D3 3 | {p} kept getting complaints from customers that {his} paper bags tear when wet. {He} began developing a bag with a thin waterproof coating. | What source of idea did {p} use? => Customers' complaints and feedback. || Which step of the process does this show? => Problem identification leading to idea generation.
''', cat='term')

X12_CH01_ST4 = spec('''
T: Feasibility study | A study to find whether a business idea can be carried out successfully and profitably.
T: Technical feasibility | Whether the technology, raw material, machinery, skills and location needed are available.
T: Financial feasibility | Whether the project can raise the funds needed and earn an adequate return.
T: Market feasibility | Whether there is enough demand for the product at a price that covers cost.
T: Opportunity assessment | Evaluating an idea's market, resources, risks and returns before committing to it.
L: tech | points examined in technical feasibility | -
- Availability of technology | The process and machines required must be available.
- Raw material | Its availability, quality and cost.
- Location | Nearness to market, raw material and transport.
- Plant capacity | The scale of production possible.
- Skilled manpower | Workers with the required skills.
L: fin | points examined in financial feasibility | -
- Total cost of the project | Fixed and working capital needed.
- Sources of funds | Owner's capital, loans and investors.
- Expected sales and profit | Projected income over the next few years.
- Break-even point | The level of sales at which there is no profit or loss.
- Return on investment | Whether the return justifies the money invested.
L: mkt | points examined in market feasibility | -
- Size of the market | The number of potential customers.
- Competition | The number and strength of competitors.
- Customer needs and preferences | What customers want and are willing to pay.
- Pricing | The price customers will accept.
- Distribution | How the product will reach customers.
Q: Which type of feasibility is being studied? | Technical feasibility; Financial feasibility; Market feasibility; Legal feasibility | -
- {p} checks whether the machines needed to make biodegradable plates are available in India. | Technical feasibility | Availability of technology is technical.
- {p} calculates whether {his} bakery will recover its investment within three years. | Financial feasibility | Return on investment is financial.
- {p} surveys colleges in {c} to estimate how many students would use a laundry app. | Market feasibility | Size of the market is examined.
- {p} studies how many rival gyms exist in {his} area and what they charge. | Market feasibility | Competition and pricing are examined.
- {p} estimates the total cost of {his} project and how much loan {he} can get. | Financial feasibility | Cost and sources of funds are examined.
- {p} checks whether skilled weavers and good-quality yarn are available near {his} proposed unit. | Technical feasibility | Raw material and manpower are examined.
- {p} checks which licences and registrations {his} food business will need. | Legal feasibility | Legal requirements are examined.
P: an idea | an opportunity
- meaning | a thought about a possible product or service | an idea with real demand that can be met profitably
- test | not yet tested | tested for feasibility
- value | may or may not be workable | commercially workable
A: A feasibility study should be carried out before investing in a project. | It shows whether the idea can be carried out successfully and profitably. | a | Both true; R explains A.
A: Market feasibility checks whether the right technology is available. | Market feasibility studies demand, competition and pricing. | d | A is false: technology is checked under technical feasibility. R is true.
A: Financial feasibility examines the break-even point. | It shows the level of sales at which there is no profit or loss. | a | Both true; R explains A.
A: An idea becomes an opportunity once it is shown to be feasible. | Every feasible idea is guaranteed to succeed. | c | A is true; R is false: feasibility lowers risk but does not guarantee success.
TT: feasibility of a business idea
S+: Technical feasibility examines technology and raw material.
S+: Market feasibility examines demand and competition.
S+: Financial feasibility examines cost, funds and returns.
S+: A feasibility study reduces the risk of failure.
S-: Market feasibility examines plant capacity.
S-: Financial feasibility examines only the colour of the product.
S-: A feasibility study is done after the business starts.
S-: Every idea is feasible.
K: C4 D4 5 | {p} wants to start a unit making millet-based snacks in {c}. {He} has found suppliers of millets and a suitable machine, estimates a project cost of ₹12 lakh, and believes health-conscious young people will buy the snacks. | Identify the three types of feasibility in the case. => Technical (suppliers, machine); financial (project cost); market (health-conscious buyers). || What else should {he} check under market feasibility? => Size of the market, competition, price customers will pay, distribution.
K: C3 D3 3 | {p} found that customers want low-cost solar lamps, but the solar cells {he} needs are not available locally and must be imported at a high cost. | Which type of feasibility is weak? => Technical feasibility (also financial, due to high cost). || Suggest one way to deal with it. => Find another supplier or technology, import in bulk, or tie up with a manufacturer.
''', cat='term')

X12_CH02_ST1 = spec('''
T: Sole proprietorship | A business owned, managed and controlled by one person who bears all the risk and gets all the profit.
T: Partnership | A business owned by two or more persons who agree to share the profits of a business carried on by all or any of them acting for all.
T: Limited liability partnership | A partnership form under the LLP Act, 2008 in which partners' liability is limited to their agreed contribution.
T: One person company | A company with only one member, introduced by the Companies Act, 2013.
T: Private company | A company that restricts the transfer of shares and has at least two and at most 200 members.
T: Public company | A company that can invite the public to buy its shares and has at least seven members.
T: Cooperative society | A voluntary association of people who join together to protect their common economic interests.
L: fac | factors affecting the choice of a form of business organisation | -
- Cost and ease of setting up | A sole proprietorship is cheapest and easiest; a company is costly.
- Liability | Owners who want limited liability choose an LLP or a company.
- Continuity | A company has perpetual succession; a proprietorship may end with the owner.
- Management and control | A sole proprietor keeps full control; in a company control is shared.
- Capital required | Large capital needs favour a company.
- Nature of business | Small or personal-service businesses suit a proprietorship.
L: oprm | merits of a sole proprietorship | -
- Quick decision-making | The owner does not have to consult anyone.
- Confidentiality of information | Business details need not be disclosed.
- Direct incentive | The owner gets all the profit.
- Ease of formation and closure | Few legal formalities are needed.
L: llp | features of a limited liability partnership | -
- Limited liability | Partners' liability is limited to their agreed contribution.
- Separate legal entity | The LLP exists separately from its partners.
- Perpetual succession | Changes in partners do not affect its existence.
- Flexibility of a partnership | Partners can organise their internal working by agreement.
Q: Which form of business organisation is most suitable? | Sole proprietorship; Partnership; Limited liability partnership; One person company; Public company; Cooperative society | -
- {p} wants to open a small tea stall alone, with little capital and no legal formalities. | Sole proprietorship | It is easy and cheap to form.
- Two chartered accountants want to work together but limit their personal liability to their contribution. | Limited liability partnership | It gives limited liability with the flexibility of a partnership.
- {p} alone wants to own a business but also wants limited liability and a separate legal entity. | One person company | A single member with limited liability.
- A group of dairy farmers in a village want to sell their milk together to get a fair price. | Cooperative society | Members protect their common economic interest.
- {f} needs ₹500 crore for a steel plant and wants to raise it from the public. | Public company | It can invite the public to subscribe.
- {p} and {p2} want to combine their skills and capital in a small boutique, with few formalities. | Partnership | Two persons share profits with few formalities.
P: sole proprietorship | one person company
- liability | unlimited | limited
- legal status | no separate legal entity | separate legal entity
- continuity | may end with the owner | has perpetual succession
- formation | very few formalities | registration under the Companies Act, 2013
A: A sole proprietor has unlimited liability. | The owner and the business are not separate in law. | a | Both true; R explains A.
A: A public company is the best form for every small business. | A public company can raise large capital from the public. | d | A is false: it is costly and has many formalities. R is true.
A: A one person company gives limited liability to a single owner. | It is a separate legal entity. | a | Both true; R explains A.
A: A limited liability partnership has perpetual succession. | Its partners have unlimited liability. | c | A is true; R is false: partners' liability is limited.
A: A cooperative society is formed to earn maximum profit. | It is a voluntary association for mutual help. | d | A is false: its aim is service to members. R is true.
TT: forms of business organisation
S+: A one person company has a single member.
S+: A sole proprietor gets all the profit and bears all the risk.
S+: An LLP is a separate legal entity.
S+: A public company must have at least seven members.
S-: A sole proprietorship has limited liability.
S-: A private company can have any number of members without limit.
S-: A partnership needs only one person.
S-: A cooperative society aims at maximum profit for outsiders.
K: C4 D4 5 | {p} has developed a mobile app and wants to start a business. {He} wants to keep full control, limit {his} personal liability, and later bring in investors. | Which form of organisation would you suggest now, and why? => One person company: single owner, limited liability, separate legal entity. || Which form would suit later when investors join? => Private company, which can have up to 200 members and issue shares to investors. || State two other factors {he} should consider. => Cost and ease of formation; continuity; capital required; nature of business (any two).
K: C3 D3 3 | {p} and {p2}, both architects, plan to start a design firm. They want flexibility in running it but do not want to risk their personal property. | Suggest a suitable form. => Limited liability partnership. || Give two reasons. => Limited liability; flexibility of a partnership; separate legal entity (any two).
''', cat='form of business')

X12_CH02_ST2 = spec('''
T: Business plan | A written document that describes the business, its objectives, strategies, market and financial forecasts.
T: Executive summary | A brief overview of the business plan, placed at the beginning to catch the reader's interest.
T: Organisational plan | The part of a business plan that describes the form of ownership, management team and their roles.
T: Marketing plan | The part of a business plan that describes the target market, competition and the marketing mix.
T: Financial plan | The part of a business plan that shows the funds required, their sources and projected income and cash flows.
T: Production plan | The part of a business plan that describes the process, machinery, raw material and capacity.
L: comp | components of a business plan | -
- Executive summary | A brief overview of the whole plan.
- Description of the business | The product or service, vision and objectives.
- Organisational plan | Form of ownership, management team and roles.
- Marketing plan | Target market, competition, pricing, promotion and distribution.
- Production or operational plan | Process, location, machinery, raw material and capacity.
- Financial plan | Capital needed, sources of funds, projected income statement and cash flow.
- Human resource plan | Staff needed, their skills and how they will be hired.
L: imp | uses of a business plan | -
- Gives a road map | It sets out where the business is going and how.
- Helps raise funds | Banks and investors ask for it before lending or investing.
- Helps in coordination | Each department knows its part.
- Helps measure progress | Actual results are compared with the plan.
- Reduces risk | Problems are foreseen and planned for.
Q: Which part of the business plan contains this information? | Executive summary; Organisational plan; Marketing plan; Production or operational plan; Financial plan; Human resource plan | -
- The details of the target customers, competitors and promotion methods of {f}. | Marketing plan | It covers market and marketing mix.
- The projected income statement and cash flow of {f} for three years. | Financial plan | Financial forecasts are part of it.
- The legal form of {f}, the names of its directors and their roles. | Organisational plan | It covers ownership and management.
- The location of the factory of {f}, its machines and production capacity. | Production or operational plan | It covers the production process.
- A one-page overview of {f}'s idea, market and funding needs at the start of the plan. | Executive summary | It is a brief overview.
- The number of staff {f} will need, their skills and how they will be recruited. | Human resource plan | It covers staffing needs.
- The amount of loan {f} needs and how it will be repaid. | Financial plan | It covers funds and their sources.
A: An executive summary is placed at the beginning of a business plan. | Investors often read it first to decide whether to read further. | a | Both true; R explains A.
A: A business plan is useful only for raising loans. | A business plan gives a road map for the enterprise. | d | A is false: it has many uses. R is true.
A: The financial plan shows projected cash flows. | It tells whether the business will have enough cash to meet its needs. | a | Both true; R explains A.
A: The marketing plan describes the factory layout. | The marketing plan covers the target market and the marketing mix. | d | A is false; R is true.
TT: the business plan
S+: The executive summary gives a brief overview of the plan.
S+: The financial plan includes projected income and cash flow.
S+: The marketing plan describes the target market and competition.
S+: A business plan helps in raising funds.
S-: The organisational plan contains the advertising budget.
S-: A business plan is prepared after the business closes.
S-: The executive summary is placed at the end of the plan.
S-: A business plan has no use once funds are raised.
K: C4 D4 5 | {p} is preparing a business plan for an organic grocery store in {c}. {He} has written about the products, the customers {he} will target, the shop's layout and suppliers, and the loan {he} needs. | Identify four components {he} has covered. => Description of the business; marketing plan; operational plan; financial plan. || Which component should come first, and why? => Executive summary: it gives a quick overview that catches the investor's interest.
K: C3 D3 3 | A bank asked {p} for a business plan before giving a loan for {his} catering business. | Why does the bank need it? => It shows that the business is viable and how the loan will be used and repaid. || Which part will the bank study most closely? => The financial plan: projected income, cash flows and repayment.
''', cat='term')

X12_CH03_ST1 = spec('''
T: Marketing mix | The combination of product, price, place and promotion that a firm uses to reach its target market.
T: Target market | The group of customers an enterprise aims to serve.
T: Market segmentation | Dividing a market into groups of customers with similar needs.
T: Positioning | Creating a distinct image of the product in the minds of target customers.
T: Extended marketing mix | People, process and physical evidence, added to the four Ps for services.
L: goals | goals of marketing for an enterprise | -
- Creating awareness | Making customers know about the product.
- Increasing sales and market share | Selling more than before and more than rivals.
- Building the brand | Creating a positive image of the business.
- Customer satisfaction and loyalty | Keeping customers happy so that they come back.
- Earning profit | Covering costs and earning a return.
L: ps | elements of the extended marketing mix for services | -
- People | Staff who deal with customers.
- Process | The way the service is delivered.
- Physical evidence | The environment, such as the look of a shop or a uniform.
Q: Which element of the marketing mix is involved? | Product; Price; Place; Promotion; People; Process; Physical evidence | -
- {f} adds a new flavour to its range of ice creams. | Product | It concerns the offering itself.
- {f} offers its haircut at ₹150, lower than nearby salons. | Price | It concerns the amount charged.
- {f} starts selling its pickles through an online marketplace. | Place | It concerns the channel of distribution.
- {f} posts short videos about its handmade soaps on social media. | Promotion | It concerns communicating with customers.
- A café trains its waiters to greet every customer by name. | People | Staff are part of the service.
- A clinic lets patients book appointments online and get reports by e-mail. | Process | It is the way the service is delivered.
- A boutique in {c} redesigns its interiors to look elegant. | Physical evidence | The environment of the service.
Q: Which goal of marketing is being pursued? | Creating awareness; Increasing sales and market share; Building the brand; Customer satisfaction and loyalty | -
- {f} distributes leaflets in {c} to tell people about its new tuition centre. | Creating awareness | People are told about the service.
- {f} offers a loyalty card that gives every tenth coffee free. | Customer satisfaction and loyalty | Customers are encouraged to return.
- {f} aims to sell 20% more than its nearest rival this year. | Increasing sales and market share | It aims at sales and share.
- {f} uses the same logo, colours and slogan everywhere to build a strong image. | Building the brand | It creates a consistent image.
- {f} calls customers after every repair to check that they are satisfied. | Customer satisfaction and loyalty | It ensures satisfaction.
A: Services need an extended marketing mix. | Services are intangible and are produced and consumed together. | a | Both true; R explains A.
A: Place in the marketing mix refers to the location of the head office. | Place refers to how the product reaches customers. | d | A is false; R is true.
A: Customer loyalty is a goal of marketing. | Loyal customers buy again and recommend the product. | a | Both true; R explains A.
A: Market segmentation helps a small enterprise focus its efforts. | It divides the market into groups with similar needs. | a | Both true; R explains A.
A: Promotion is one of the four Ps. | Promotion means fixing the price of a product. | c | A is true; R is false: promotion is communication with customers.
TT: marketing for an enterprise
S+: The four Ps are product, price, place and promotion.
S+: People, process and physical evidence are added for services.
S+: Market segmentation divides customers into groups with similar needs.
S+: Customer satisfaction is a goal of marketing.
S-: Place means the price of the product.
S-: Marketing begins only after the product is sold.
S-: Physical evidence is one of the original four Ps.
S-: A small enterprise has no need for a target market.
K: C4 D4 5 | {p} runs a small yoga studio in {c}. {He} has trained, friendly instructors, offers online booking, a calm and clean studio, monthly plans at ₹1,200, and promotes the studio on social media. | Identify five elements of the marketing mix in the case. => People: friendly instructors; process: online booking; physical evidence: calm, clean studio; price: ₹1,200 monthly plans; promotion: social media (product: yoga classes).
K: C3 D3 3 | {f} makes millet cookies for health-conscious office workers and positions them as a 'guilt-free snack'. | Identify the target market. => Health-conscious office workers. || What is positioning? => Creating a distinct image of the product, here as a guilt-free snack, in the minds of target customers.
''', cat='term')

X12_CH06_ST2 = spec('''
T: Angel investor | A wealthy individual who invests personal money in an early-stage start-up in return for equity, often giving advice too.
T: Venture capital | Funds managed by professional firms that invest in high-growth start-ups in return for equity.
T: Bootstrapping | Starting and growing a business with the founder's own savings and revenue, without outside investors.
T: Seed funding | The first funding used to develop the idea and build a prototype.
T: Crowdfunding | Raising small amounts of money from a large number of people, usually through an online platform.
T: Exit | The way an investor sells its stake, such as through an IPO or a sale to another company.
T: Equity dilution | The fall in the founders' percentage ownership when new shares are issued to investors.
L: stages | stages of start-up funding | -
- Bootstrapping | The founder's own money, family and friends.
- Seed stage | Funds to develop the idea and build a prototype, often from angel investors.
- Early stage (Series A) | Funds to start operations and reach customers, often from venture capitalists.
- Growth or expansion stage (Series B, C) | Funds to scale up, enter new markets and add products.
- Exit stage | Investors sell their stake through an IPO or acquisition.
L: vc | features of venture capital | -
- Equity participation | The venture capitalist takes a share in ownership.
- High risk, high return | It invests in new, unproven but high-growth ideas.
- Long-term investment | Funds are locked in for several years.
- Active participation | The investor guides management and may sit on the board.
- Exit after growth | The investor sells its stake when the firm has grown.
P: angel investor | venture capitalist
- who invests | a wealthy individual | a professionally managed fund
- source of money | personal money | money pooled from many investors
- stage | usually seed or very early stage | usually early and growth stages
- amount | smaller amounts | larger amounts
Q: Which source or stage of funding is shown? | Bootstrapping; Seed stage; Early stage (Series A); Growth or expansion stage (Series B, C); Exit stage; Crowdfunding | -
- {p} started {his} app with ₹2 lakh of {his} own savings and reinvested every rupee earned. | Bootstrapping | No outside investors.
- A retired businessman gave {p} ₹15 lakh to build a prototype in return for 10% of the company. | Seed stage | Funds to build a prototype from an angel.
- A venture capital fund invested ₹10 crore in {f} to open offices in five more cities. | Growth or expansion stage (Series B, C) | Funds to scale up.
- {f} raised ₹30 lakh from 2,000 people through an online platform to make its first batch of products. | Crowdfunding | Many small contributions online.
- After {f} listed on the stock exchange, its venture capital investor sold its shares. | Exit stage | The investor exits through an IPO.
- {f}, which has a working product, raised its first round from a venture capital fund to start sales. | Early stage (Series A) | Funds to start operations and reach customers.
A: Venture capital is called high-risk capital. | It is invested in new and unproven businesses. | a | Both true; R explains A.
A: Angel investors usually invest at the seed stage. | They are willing to take risks on very early ideas. | a | Both true; R explains A.
A: Bootstrapping dilutes the founder's ownership. | In bootstrapping, the founder uses his or her own funds. | d | A is false: no outside equity is issued. R is true.
A: Venture capitalists often take part in management. | They want to protect and grow their investment. | a | Both true; R explains A.
A: Venture capitalists plan an exit. | Venture capitalists invest money only as loans. | c | A is true; R is false: they invest in equity.
TT: start-up funding
S+: An angel investor uses personal money.
S+: Venture capital funds are professionally managed.
S+: Bootstrapping uses the founder's own resources.
S+: An IPO can be an exit route for investors.
S-: Angel investors are banks that give loans.
S-: Venture capital is a short-term loan.
S-: Seed funding is raised after the IPO.
S-: Crowdfunding raises money from only one investor.
K: C4 D4 5 | {p} started a drone-repair business with {his} savings. A wealthy family friend then invested ₹20 lakh for 15% equity. Two years later a professional fund invested ₹8 crore to expand to ten cities, and plans to sell its stake when the company lists. | Identify the four stages of funding in the case and give two features of the fund's investment. => Bootstrapping; seed stage (angel investor); growth/expansion stage (venture capital); exit stage (sale after listing). Features: equity participation; high risk, high return; long-term; active participation; exit after growth (any two).
K: C3 D3 3 | {p} needs ₹25 lakh to build the first model of a smart water meter. Banks have refused a loan as there is no security. | Suggest a source of funds. => An angel investor (or crowdfunding). || Give two reasons. => Angels invest at the seed stage, take risk without security, and often give advice and contacts.
''', cat='funding term')

