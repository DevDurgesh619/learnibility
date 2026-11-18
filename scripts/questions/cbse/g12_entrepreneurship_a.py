"""CBSE class 12 entrepreneurship (066) families: theory fact tables for units 1-4 and 6 (st2-st4).

Fact text uses g12_business_a.spec() (line format documented there). `efacts()` wraps g11_accountancy_kit.facts()
for the entrepreneurship paper (1, 2, 3 and 5 marks): it drops the 4- and 6-mark generators, adds 2-mark
"explain one point" and "two bases" items and 5-mark "explain any five" items, and tags 5-mark cases 'm5'.
Mock kinds: 'mcq', 'ar', 'm2'/'m3'/'m5' (explain and list items) and 'm2c'/'m3c'/'m5c' (scenario, case and
computed application items), so that each mock section mixes recall with application.
"""
from __future__ import annotations

from g11_accountancy_kit import FF, facts, Cyc, ctx, fill
from g12_business_a import spec

S = 'cbse-g12-entrepreneurship-ch'
DROP = {'two', 'long_', 'pair4', 'pair6', 'scen_two', 'scen_feat'}
_ORD = ['(i)', '(ii)', '(iii)', '(iv)', '(v)', '(vi)']


def efacts(sp: dict) -> list:
    out = []
    for f in facts(sp):
        n = f.gen.__name__
        if n in DROP:
            continue
        if n == 'case':
            f.kinds = ({5: 'm5c', 3: 'm3c', 2: 'm2c'}[int(f.marks)], 'case')
        elif n == 'scen_just':
            f.kinds = ('m3c',)
        out.append(f)
    lists = sp.get('lists') or []
    for (k, title, pts, con) in lists:
        if len(pts) >= 2:
            cy = Cyc(pts)

            def one(r, title=title, cy=cy):
                p, e = cy.next(r)
                return {'stem': f'Explain "{p}" with reference to the {title}.', 'answer': f'{p}: {e}',
                        'key': f'1 mark for the point and 1 mark for the explanation: {e}'}
            out.append(FF('C2', 'D2', 'explain', one, marks=2, kinds=('m2',)))
        if len(pts) >= 5:
            def five(r, title=title, pts=pts):
                body = ' '.join(f'{_ORD[i] if i < 6 else ""} {p}: {e}'.strip() for i, (p, e) in enumerate(pts[:6]))
                rest = '; '.join(p for p, e in pts[6:])
                if rest:
                    body += f' Other valid points: {rest}.'
                return {'stem': f'Explain any five {title}.', 'answer': body,
                        'key': f'Any five points, 1 mark each (point with a line of explanation): {body}'}
            out.append(FF('C2', 'D4', 'long', five, marks=5, kinds=('m5',)))
    for (X, Y, bases) in sp.get('pairs') or []:
        if len(bases) >= 3:
            def two(r, X=X, Y=Y, bases=bases):
                a, b = r.sample(bases, 2)
                body = f'(i) {a[0][0].upper() + a[0][1:]}: {X}: {a[1]}; {Y}: {a[2]}. (ii) {b[0][0].upper() + b[0][1:]}: {X}: {b[1]}; {Y}: {b[2]}.'
                return {'stem': f'Differentiate between {X} and {Y} with reference to {a[0]} and {b[0]}.', 'answer': body,
                        'key': f'1 mark for each basis: {body}'}
            out.append(FF('C2', 'D3', 'explain', two, marks=2, kinds=('m2',)))
    for (q, pool, items, fk) in sp.get('scen') or []:
        if len(items) >= 4 and sp.get('scen2', True):
            cy = Cyc(items)

            def sc2(r, q=q, cy=cy):
                text, ans, why = cy.next(r)
                d = ctx(r)
                return {'stem': f'Read the situation and answer. {fill(text, d)} (a) {q} (b) Give one reason in support of your answer.',
                        'answer': f'(a) {ans} (b) {fill(why, d)}',
                        'key': f'(a) {ans}, 1 mark; (b) reason, 1 mark: {fill(why, d)}'}
            out.append(FF('C3', 'D3', 'explain', sc2, marks=2, kinds=('m2c',)))
    return out


# ================================================================ Unit 1 Entrepreneurial opportunity

CH01_ST1 = spec('''
T: Entrepreneurial opportunity | A favourable set of circumstances that creates a need for a new product, service or business.
T: Sensing opportunities | The ability to notice unmet needs and changes in the environment that can be turned into a business.
T: Idea field | A broad area, such as natural resources, knowledge or trends, in which business ideas can be found.
T: Trend | A general direction in which something is developing or changing over time, such as the rise of online shopping.
T: Knowledge-based idea | A business idea that grows out of special knowledge, skill, research or technology.
T: Opportunity window | The period during which an opportunity remains open before competitors or changes close it.
L: fac | factors involved in sensing entrepreneurial opportunities | -
- Market and customer needs | Unmet or poorly met needs of customers point to opportunities.
- Changes in the environment | Economic, social, technological and legal changes create new needs.
- Creativity of the entrepreneur | Creative people see new uses and combinations.
- Knowledge and experience | Familiarity with an industry helps spot gaps.
- Networks and contacts | Contacts provide information about needs and resources.
- Availability of resources | Access to raw material, skills and funds makes an idea workable.
L: field | idea fields for spotting business ideas | -
- Natural resources | Ideas based on local raw materials, such as fruit processing, bamboo crafts or herbal products.
- Knowledge | Ideas based on expertise, research or technology, such as software or consultancy.
- Trends | Ideas based on changes in lifestyle and society, such as fitness, online services or eco-friendly goods.
- Existing products and services | Ideas that improve or add features to products already in use.
- Demand and market gaps | Ideas that meet demand which is not being met in an area.
Q: Which idea field has the entrepreneur used? | Natural resources; Knowledge; Trends; Existing products and services; Demand and market gaps | -
- {p} of {c} started making jam and pickles from the mangoes grown in {his} village. | Natural resources | The idea is based on a locally available raw material.
- {p}, a software engineer, started a firm that builds billing apps for small shops. | Knowledge | The idea is based on technical expertise.
- Seeing more people work from home, {p} started a business renting ergonomic office chairs. | Trends | The idea is based on a change in lifestyle.
- {p} added a built-in water filter to an ordinary steel bottle and sold it as a new product. | Existing products and services | It improves an existing product.
- {p} found there was no repair shop for mobile phones in {his} town and opened one. | Demand and market gaps | It meets demand not being met in the area.
- {p} uses bamboo from the forests of the North-East to make furniture. | Natural resources | Local raw material is used.
- {p}, a dietician, runs online diet-planning classes. | Knowledge | The idea is based on professional expertise.
- Noticing the growing demand for plant-based food, {p} started a vegan bakery in {c}. | Trends | The idea follows a social trend.
A: Changes in the environment create entrepreneurial opportunities. | New laws, technologies and lifestyles create new needs. | a | Both true; R explains A.
A: Natural resources can be a source of business ideas. | Ideas such as fruit processing use locally available raw material. | a | Both true; R explains A.
A: Every idea is an entrepreneurial opportunity. | An opportunity needs a real demand that can be met profitably. | d | A is false: only ideas with real demand and workable resources are opportunities. R is true.
A: An opportunity remains open for an unlimited period. | Competitors may enter and close the opportunity window. | d | A is false; R is true.
A: Knowledge can be an idea field for business. | All knowledge-based businesses need large factories. | c | A is true; R is false: many knowledge-based businesses, such as consultancy, need little physical capital.
TT: sensing entrepreneurial opportunities
S+: Unmet customer needs are a source of opportunities.
S+: Natural resources, knowledge and trends are idea fields.
S+: Changes in technology can create new opportunities.
S+: An opportunity window does not remain open for ever.
S-: Every idea is automatically a business opportunity.
S-: Opportunities exist only in large cities.
S-: Trends have no effect on business opportunities.
S-: Knowledge cannot be the basis of a business.
K: C4 D4 5 | {p} noticed that many working parents in {c} had no time to cook healthy meals. Being a trained nutritionist, {he} started a subscription service delivering balanced lunch boxes, using vegetables from nearby farms. | Identify the idea fields {p} used. => Trends (busy lifestyles); knowledge (nutrition); natural resources (local vegetables). || State three factors that helped {him} sense the opportunity. => Market and customer needs; knowledge and experience; availability of resources; creativity (any three).
K: C3 D3 3 | {p} found that tourists visiting {his} hill town could not find locally made souvenirs. {He} started a shop selling wooden crafts made by local artisans. | Which idea field is shown? => Demand and market gaps (also natural resources: local wood). || What made it an opportunity and not just an idea? => There was real unmet demand from tourists, and resources (artisans, wood) were available.
''', cat='term')

CH01_ST2 = spec('''
T: Environment scanning | The process of collecting and analysing information about the external environment to spot opportunities and threats.
T: PESTLE analysis | A tool that studies the political, economic, social, technological, legal and environmental factors affecting a business.
T: SWOT analysis | A tool that assesses the strengths, weaknesses, opportunities and threats of a business or idea.
T: Strength | An internal factor that gives a business an advantage over others.
T: Weakness | An internal factor that puts a business at a disadvantage.
T: Opportunity | An external factor that the business can use to its advantage.
T: Threat | An external factor that could harm the business.
L: pestle | factors studied in PESTLE analysis | -
- Political | Government stability, policies, subsidies and trade restrictions.
- Economic | Inflation, interest rates, income levels and growth of the economy.
- Social | Population, lifestyles, culture, education and attitudes.
- Technological | New technology, automation, internet use and research.
- Legal | Laws on consumer protection, employment, licensing and safety.
- Environmental | Climate, pollution norms, waste management and sustainability.
L: imp | benefits of environment scanning for an entrepreneur | -
- Identifies opportunities | Changes in the environment point to new needs.
- Gives early warning of threats | The entrepreneur can prepare for changes in laws or competition.
- Helps in planning | Plans are based on facts about the environment.
- Improves decision-making | Choices are based on information, not guesswork.
- Helps the enterprise adapt | It keeps the business in tune with changing conditions.
Q: Which PESTLE factor is involved? | Political; Economic; Social; Technological; Legal; Environmental | -
- The government announced a subsidy for units making solar panels. | Political | It is a government policy.
- Rising interest rates increased the cost of loans for small firms in {c}. | Economic | Interest rates are an economic factor.
- More young people in {c} prefer to eat out on weekends. | Social | It is a change in lifestyle.
- Cheap mobile data has made online ordering easy even in villages. | Technological | It is a change in technology.
- A new law requires all food sellers to obtain an FSSAI licence. | Legal | It is a legal requirement.
- A ban on single-use plastic has increased the demand for cloth and paper bags. | Environmental | It relates to pollution norms.
- Inflation has reduced the purchasing power of families in {c}. | Economic | Inflation is an economic factor.
- An ageing population has increased demand for home health care. | Social | It is a demographic change.
Q: In a SWOT analysis, what type of factor is this? | Strength; Weakness; Opportunity; Threat | -
- {f} has a team of highly skilled designers. | Strength | It is an internal advantage.
- {f} has an old machine that often breaks down. | Weakness | It is an internal disadvantage.
- The government plans to build a highway next to the market of {f}. | Opportunity | It is a favourable external factor.
- A large retail chain is opening a store next to {f}. | Threat | It is an unfavourable external factor.
- {f} has very little working capital. | Weakness | It is an internal limitation.
- {f} owns a well-known local brand. | Strength | It is an internal advantage.
- Demand for organic products is rising across {c}. | Opportunity | It is a favourable external trend.
- New import rules make the main raw material of {f} costlier. | Threat | It is an unfavourable external change.
P: strengths and weaknesses | opportunities and threats
- source | internal to the business | external to the business
- control | largely within the control of the entrepreneur | outside the control of the entrepreneur
- example | skilled staff; poor location | rising demand; new competitor
A: Strengths and weaknesses are internal factors. | They arise within the business and can be controlled by it. | a | Both true; R explains A.
A: Opportunities and threats are internal factors. | They arise from the external environment. | d | A is false: they are external. R is true.
A: Environment scanning helps an entrepreneur spot opportunities. | Changes in the environment create new needs. | a | Both true; R explains A.
A: A ban on single-use plastic is an environmental factor in PESTLE. | Such bans are made through law. | b | Both true; R is true but does not explain why it is classed as environmental (it relates to pollution).
A: SWOT analysis helps an entrepreneur match strengths with opportunities. | SWOT studies only the competitors of a business. | c | A is true; R is false: SWOT studies the business itself and its environment.
TT: environment scanning
S+: In PESTLE, 'L' stands for legal factors.
S+: Strengths and weaknesses are internal factors.
S+: Opportunities and threats are external factors.
S+: Environment scanning gives early warning of threats.
S-: In PESTLE, 'E' stands only for economic factors.
S-: A new competitor is a weakness of the business.
S-: SWOT analysis studies only internal factors.
S-: Environment scanning is done only once, when the business starts.
K: C4 D4 5 | {p} plans a cloud kitchen in {c}. {He} has cooking skills but limited funds. Food delivery apps are growing fast, but two big chains have just opened outlets nearby, and new hygiene rules are coming. | Prepare a SWOT analysis for {p}'s idea. => Strength: cooking skills; weakness: limited funds; opportunity: growth of food delivery apps; threat: big chains nearby. || Which PESTLE factor do the new hygiene rules represent? => Legal.
K: C4 D5 5 | {p} wants to start an electric-scooter rental business in {c}. The government gives subsidies on electric vehicles, fuel prices are rising, young people prefer shared transport, battery technology is improving, and pollution norms are getting stricter. | Classify each fact under a PESTLE factor and say whether the environment favours the idea. => Political: subsidies; economic: rising fuel prices; social: preference for shared transport; technological: better batteries; environmental: stricter pollution norms. Yes, the environment is favourable.
''', cat='term')

CH01_ST3 = spec('''
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

CH01_ST4 = spec('''
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

# ================================================================ Unit 2 Entrepreneurial planning

CH02_ST1 = spec('''
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

CH02_ST2 = spec('''
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

CH02_ST3 = spec('''
T: Operational plan | The part of the business plan that describes how goods or services will be produced and delivered day to day.
T: Production planning | Deciding what to produce, how much, when and by what method.
T: Inventory planning | Deciding the stock of raw material, work-in-progress and finished goods to be kept.
T: Quality planning | Setting quality standards and the methods of checking and maintaining them.
T: Plant layout | The arrangement of machines, work areas and storage in a factory.
T: Capacity planning | Deciding the maximum output the unit can produce in a period.
L: prod | elements of production planning | -
- Product design | The features and specifications of the product.
- Choice of process | The method and technology of production.
- Capacity | The quantity to be produced in a period.
- Scheduling | When each job is to be done.
- Location and layout | Where the unit is and how machines are arranged.
L: inv | aims of inventory planning | -
- Avoid shortage of materials | Production does not stop for want of material.
- Avoid excess stock | Money is not blocked in idle stock.
- Reduce carrying cost | Storage, insurance and wastage costs are kept low.
- Meet customer orders on time | Enough finished goods are available.
L: qual | steps in quality planning | -
- Set quality standards | Decide the specifications the product must meet.
- Inspect materials and output | Check raw material and finished goods.
- Compare with standards | Find any deviations.
- Take corrective action | Remove the causes of defects.
- Obtain certification | Marks such as ISI, Agmark or FSSAI licence build trust.
Q: Which part of the operational plan is involved? | Production planning; Inventory planning; Quality planning; Plant layout | -
- {f} decides to produce 2,000 school bags in June and 3,000 in July. | Production planning | It decides how much and when to produce.
- {f} keeps enough cloth for 15 days of production but not more. | Inventory planning | It decides the stock of raw material.
- {f} checks every tenth packet of spices for weight and purity. | Quality planning | It inspects output against standards.
- {f} arranges its machines in the order of the production process to avoid back-and-forth movement. | Plant layout | It is the arrangement of machines.
- {f} applies for an FSSAI licence and sets standards for hygiene in its kitchen. | Quality planning | It sets and certifies standards.
- {f} decides to make soaps by the cold process and fixes the weekly output. | Production planning | It chooses the method and quantity.
- {f} reorders packaging boxes whenever the stock falls to 500. | Inventory planning | It sets the reorder level.
A: Inventory planning helps avoid both shortage and excess of stock. | Excess stock blocks money and shortage stops production. | a | Both true; R explains A.
A: Quality planning ends with setting standards. | Standards must be compared with actual output and corrective action taken. | d | A is false: it also includes inspection and correction. R is true.
A: A good plant layout reduces the movement of materials. | Machines are arranged in the order of operations. | a | Both true; R explains A.
A: Production planning decides what, how much and when to produce. | Production planning has nothing to do with the method of production. | c | A is true; R is false: it also decides the method.
TT: the operational plan
S+: Inventory planning aims at avoiding shortage and excess of stock.
S+: Quality planning includes setting standards and inspection.
S+: Plant layout is the arrangement of machines and work areas.
S+: Production planning decides what, how much and when to produce.
S-: Inventory planning means keeping as much stock as possible.
S-: Quality planning is not needed for small enterprises.
S-: Plant layout decides the price of the product.
S-: The operational plan deals only with advertising.
K: C4 D4 5 | {f}, a small furniture unit in {c}, often stops work because wood runs out, while at other times its store is overfull. Some chairs are returned for loose joints, and workers waste time moving parts between distant machines. | Identify three problems in the operational plan and suggest a solution for each. => Inventory planning: set minimum and reorder levels for wood. Quality planning: set standards and inspect joints before dispatch. Plant layout: arrange machines in the order of operations.
K: C3 D3 3 | {p} runs a bakery that must deliver 500 cakes for a festival next week. | State three decisions {he} must take under production planning. => What and how much to bake; when each batch is baked (scheduling); method, ovens and staff needed (process and capacity).
''', cat='term')

CH02_ST4 = spec('''
T: Project report | A detailed document about a proposed project, covering its technical, market and financial aspects, prepared mainly for lenders and authorities.
T: Pitching | Presenting a business idea to investors to persuade them to invest.
T: Elevator pitch | A very short presentation of a business idea, about 30 to 60 seconds long.
T: Pitch deck | A short set of slides used to present a business idea to investors.
T: Means of finance | The sources from which the cost of a project will be met.
L: rep | contents of a project report | -
- General information | Name, nature of the project and promoters' background.
- Project description | Product, process, location, land and buildings.
- Plant and machinery | Machines needed, their cost and suppliers.
- Raw material and manpower | Requirements and their availability.
- Market potential | Demand, competition and marketing strategy.
- Cost of project and means of finance | Total cost and sources of funds.
- Profitability and break-even analysis | Projected profit and the break-even point.
L: deck | elements of a good pitch deck | -
- Problem | The customer problem the business solves.
- Solution | The product or service and how it solves the problem.
- Market size | The number of potential customers and the value of the market.
- Business model | How the business will earn money.
- Competition | Rivals and the advantage over them.
- Team | The people behind the business.
- Financials and the ask | Projections and the amount of investment sought.
Q: Which element of the pitch deck is being presented? | Problem; Solution; Market size; Business model; Competition; Team; Financials and the ask | -
- {p} tells investors that 40% of small shops in {c} lose money because they cannot track credit sales. | Problem | It states the customer problem.
- {p} shows how {his} app records credit sales and sends reminders automatically. | Solution | It explains how the problem is solved.
- {p} says the app will earn through a monthly subscription of ₹99 per shop. | Business model | It shows how money will be earned.
- {p} says there are 1.2 crore small shops in India that could use the app. | Market size | It gives the number of potential customers.
- {p} introduces the co-founders and their experience in retail and software. | Team | It presents the people behind the business.
- {p} asks for ₹50 lakh in return for 10% equity. | Financials and the ask | It states the investment sought.
- {p} shows how {his} product is cheaper and simpler than two rival apps. | Competition | It compares with rivals.
P: business plan | project report
- purpose | a road map for running the business | a document for appraisal by banks and authorities
- focus | strategy and future direction | technical, market and financial details of a project
- users | the entrepreneur, partners and investors | mainly lenders and government agencies
A: An elevator pitch must be very short. | It should hold the listener's attention within a minute. | a | Both true; R explains A.
A: The project report includes the cost of the project and means of finance. | Lenders want to know how the project will be funded. | a | Both true; R explains A.
A: A pitch deck should include every detail of the business plan. | A pitch deck is a short set of slides. | d | A is false: it should be short and focused. R is true.
A: Investors look at the team presented in a pitch. | The success of a start-up depends a great deal on its people. | a | Both true; R explains A.
A: A project report contains break-even analysis. | Break-even analysis is not useful for lenders. | c | A is true; R is false: it shows lenders the risk of the project.
TT: project reports and pitching
S+: An elevator pitch lasts about 30 to 60 seconds.
S+: A project report includes the cost of project and means of finance.
S+: A pitch deck usually states the problem and the solution.
S+: The 'ask' is the amount of investment sought.
S-: A pitch deck should run to a hundred slides.
S-: A project report contains no financial information.
S-: An elevator pitch takes two hours.
S-: Investors do not care about the team.
K: C4 D4 5 | {p} has five minutes to present {his} start-up, which supplies fresh vegetables directly from farmers to restaurants in {c}, to a group of angel investors. | Suggest five slides {he} should include, with one line on each. => Problem: restaurants pay high prices for stale vegetables; solution: direct farm-to-restaurant supply; market size: number of restaurants in the city; business model: margin per kg / subscription; financials and the ask: projections and amount sought (also team, competition).
K: C3 D3 3 | {p} has applied for a bank loan for {his} paper-plate unit. The bank has asked for a project report. | State three contents of the project report the bank will look for. => Cost of project and means of finance; market potential; profitability and break-even analysis (also plant and machinery, raw material).
''', cat='term')

# ================================================================ Unit 3 Enterprise marketing

CH03_ST1 = spec('''
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

CH03_ST2 = spec('''
T: Unique selling proposition | A distinct benefit of a product that competitors do not offer and that is used to persuade customers to buy.
T: Brand | A name, term, sign, symbol or design that identifies the products of a seller and distinguishes them from those of competitors.
T: Packaging | Designing and producing the container or wrapper for a product.
T: Labelling | Putting information about the product on its package.
T: Tagline | A short, memorable phrase used with a brand to express its USP.
T: Trademark | A brand or part of a brand that is registered and legally protected.
L: usp | qualities of a good unique selling proposition | -
- Distinct | It is not offered by competitors.
- Customer-focused | It offers a benefit customers value.
- Simple and clear | It can be expressed in a few words.
- Believable | The business can actually deliver it.
- Hard to copy | Competitors cannot easily imitate it.
L: brand | benefits of branding for a small enterprise | -
- Product differentiation | It distinguishes the product from rivals.
- Customer loyalty | Customers ask for the brand again.
- Ease in introducing new products | New products can use the known brand.
- Premium pricing | A trusted brand can charge more.
- Easier advertising | Promotion is built around the brand.
L: lab | information usually given on a label | -
- Name and brand of the product | It identifies the product.
- Ingredients or contents | It tells what the product contains.
- Net weight or quantity | It tells how much is in the pack.
- Maximum retail price | It tells the highest price that can be charged.
- Dates of manufacture and expiry | They tell whether the product is safe to use.
- Name and address of the manufacturer | It tells who made the product.
Q: What is the USP being used? | Speed of delivery; Low price; Superior quality; Customisation; Eco-friendliness | -
- {f} promises to deliver groceries in {c} within 15 minutes. | Speed of delivery | The distinct benefit is fast delivery.
- {f} prints the customer's name and design on every T-shirt it sells. | Customisation | Each product is made to the customer's wishes.
- {f} sells soaps packed only in recycled paper, made from natural ingredients. | Eco-friendliness | The benefit is care for the environment.
- {f} claims its mobile covers are the cheapest in the market. | Low price | The benefit is a lower price.
- {f} uses only hand-picked, first-grade tea leaves and says no rival matches its taste. | Superior quality | The benefit is quality.
- {f} makes furniture to the exact size of each customer's room. | Customisation | Products are made to order.
P: packaging | labelling
- meaning | designing the container or wrapper of a product | putting information about the product on the package
- main function | protection and attraction | identification and information
- example | a glass jar for jam | the list of ingredients printed on the jar
A: A USP should be hard for competitors to copy. | A USP that is easily copied soon loses its distinctiveness. | a | Both true; R explains A.
A: Branding helps a small enterprise build customer loyalty. | Customers can identify and ask for the brand again. | a | Both true; R explains A.
A: Labels on packaged food must show the expiry date. | Customers need to know whether the product is safe to use. | a | Both true; R explains A.
A: Packaging has no role in promotion. | An attractive package draws customers' attention. | d | A is false: packaging helps promotion. R is true.
A: A trademark is a legally protected brand. | Every brand name is automatically a trademark. | c | A is true; R is false: a brand becomes a trademark only on registration.
TT: USP, branding, packaging and labelling
S+: A USP is a distinct benefit not offered by competitors.
S+: A trademark is a registered brand.
S+: Labels give information such as ingredients and expiry date.
S+: Packaging protects the product and attracts customers.
S-: A USP should be the same as the competitors' benefit.
S-: Labelling means designing the shape of the bottle.
S-: Branding makes it harder to introduce new products.
S-: Packaging is not important for food products.
K: C4 D4 5 | {p} has started making handmade chocolates in {c} with no added sugar. {He} has named them 'PureBite', packs them in recyclable boxes, and prints ingredients, net weight and expiry date on each box. | What is the USP of PureBite? => Chocolates with no added sugar (also eco-friendly packing). || State two benefits of branding to {p}. => Product differentiation; customer loyalty; premium pricing; ease of introducing new products (any two). || State two functions of the label. => Gives information about contents; tells the expiry date; identifies the product (any two).
K: C3 D3 3 | Two tiffin services in {c} offer similar food at similar prices. One of them promises meals cooked without oil. | What is the term for this promise? => Unique selling proposition. || State two qualities it must have to work. => Distinct, customer-focused, believable, hard to copy (any two).
''', cat='term')

CH03_ST3 = spec('''
T: Cost-based pricing | Fixing the price by adding a mark-up to the cost of the product.
T: Competition-based pricing | Fixing the price on the basis of competitors' prices.
T: Price skimming | Setting a high price at launch and lowering it over time.
T: Penetration pricing | Setting a low price at launch to capture market share quickly.
T: Psychological pricing | Setting prices such as ₹99 instead of ₹100 so that they appear lower.
T: Mark-up | The amount or percentage added to cost to arrive at the selling price.
L: fac | factors to consider while fixing a price | -
- Cost of the product | The price should cover cost in the long run.
- Demand and customers' capacity to pay | The price must be one customers will accept.
- Competitors' prices | The price must be in line with rivals unless the product is distinct.
- Objectives of the firm | Market share, profit or image affect the price.
- Government regulations | Some prices are controlled by law.
Q: Which pricing strategy is used? | Cost-based pricing; Competition-based pricing; Price skimming; Penetration pricing; Psychological pricing | -
- {f} launched a new smartwatch at ₹25,000 and cut the price to ₹15,000 after a year. | Price skimming | A high launch price lowered over time.
- {f} launched its new detergent at a very low price to win customers from established brands. | Penetration pricing | A low launch price to capture share.
- {f} adds 25% to the cost of each cake to fix its price. | Cost-based pricing | A mark-up is added to cost.
- {f} prices its school bags at ₹499 instead of ₹500. | Psychological pricing | The price appears lower.
- {f} keeps the price of its petrol the same as the pumps around it. | Competition-based pricing | The price follows competitors.
- A new streaming app offers its service at ₹29 a month for the first year to attract users. | Penetration pricing | A low price to build a customer base.
- {f} checks what other salons in {c} charge for a haircut and fixes a similar price. | Competition-based pricing | The price is based on rivals' prices.
- {f} sells its handmade candles at cost plus ₹40 per candle. | Cost-based pricing | A fixed mark-up is added to cost.
P: price skimming | penetration pricing
- launch price | high | low
- aim | to earn high profit from early buyers | to capture market share quickly
- suitable when | the product is new and unique with few rivals | demand is price-sensitive and rivals are many
- later price | lowered over time | may be raised once customers are won
A: Price skimming is suitable for an innovative product. | Early buyers are willing to pay a high price for something new. | a | Both true; R explains A.
A: Penetration pricing sets a high launch price. | Penetration pricing aims at capturing market share quickly. | d | A is false: the launch price is low. R is true.
A: A price of ₹999 is an example of psychological pricing. | It makes the price appear lower than ₹1,000. | a | Both true; R explains A.
A: Cost-based pricing ignores competitors' prices. | It fixes the price by adding a mark-up to cost. | a | Both true; R explains A.
A: Competition-based pricing is common for similar products. | Under competition-based pricing, cost is never considered. | c | A is true; R is false: cost still sets a lower limit.
TT: pricing strategies
S+: Price skimming starts with a high price.
S+: Penetration pricing starts with a low price.
S+: Cost-based pricing adds a mark-up to cost.
S+: ₹499 instead of ₹500 is psychological pricing.
S-: Price skimming starts with a low price.
S-: Penetration pricing is used to earn high profit from early buyers.
S-: Cost-based pricing ignores the cost of the product.
S-: Psychological pricing means charging double the cost.
K: C4 D4 5 | {p} is launching a new solar-powered phone charger in {c}. Few rivals make it, and early buyers are keen on new gadgets. {His} friend {p2} is launching a new brand of tea in a market with many established brands. | Suggest a pricing strategy for each, with reasons. => {p}: price skimming, since the product is new with few rivals and early buyers will pay more; {p2}: penetration pricing, to win customers from established brands. || State two other factors each must consider. => Cost of the product; demand and capacity to pay; competitors' prices; government regulations (any two).
K: C3 D3 3 | {f} set a low price for its new juice to win customers quickly, and later raised the price after building a loyal base. | Identify the pricing strategy. => Penetration pricing. || State one advantage and one risk. => Advantage: quick market share; risk: low profit at first, or customers may leave when the price rises.
''', cat='pricing term')

CH03_ST4 = spec('''
T: Advertising | Paid, impersonal communication about a product by an identified sponsor.
T: Sales promotion | Short-term incentives such as discounts and free samples that encourage immediate purchase.
T: Digital marketing | Promotion of products through digital channels such as social media, search engines, e-mail and websites.
T: Search engine optimisation | Improving a website so that it appears higher in search engine results.
T: Influencer marketing | Promotion through people with a large following on social media.
T: Direct channel | Selling to customers without any middlemen.
T: Indirect channel | Selling through middlemen such as wholesalers and retailers.
L: dig | advantages of digital marketing for a small enterprise | -
- Low cost | It costs much less than print or television advertising.
- Targeted reach | Messages can reach a chosen age group or area.
- Measurable results | Clicks, views and sales can be tracked.
- Two-way communication | Customers can comment and give feedback.
- Wide reach | Customers anywhere can be reached.
L: tools | tools of digital marketing | -
- Social media marketing | Promotion on platforms where customers spend time.
- Search engine optimisation | Making the website appear higher in search results.
- E-mail marketing | Sending offers and news to customers by e-mail.
- Content marketing | Sharing useful blogs, videos and guides to attract customers.
- Influencer marketing | Getting people with large followings to promote the product.
Q: Which promotion or distribution method is being used? | Advertising; Sales promotion; Social media marketing; Search engine optimisation; Influencer marketing; Direct channel; Indirect channel | -
- {f} pays a popular fitness blogger to review its protein bars. | Influencer marketing | A person with a large following promotes the product.
- {f} improves its website so that it appears on the first page when people search for 'bakery in {c}'. | Search engine optimisation | The website ranks higher in search.
- {f} gives a free mug with every purchase above ₹1,000 this week. | Sales promotion | It is a short-term incentive.
- {f} sells its honey only through its own website and farm shop. | Direct channel | No middlemen are used.
- {f} supplies its biscuits to wholesalers, who sell them to retail shops. | Indirect channel | Middlemen are used.
- {f} runs a paid advertisement in a local newspaper. | Advertising | Paid, impersonal communication.
- {f} posts daily photos and offers on its social media page and replies to comments. | Social media marketing | Promotion on social media platforms.
P: direct channel | indirect channel
- middlemen | none | wholesalers, retailers or agents
- control over sales | high | lower
- reach | limited by the firm's own capacity | wider through middlemen
- example | selling through own website or shop | selling through retail stores
A: Digital marketing is suitable for small enterprises. | It is low-cost and can be targeted. | a | Both true; R explains A.
A: Sales promotion builds long-term loyalty by itself. | Sales promotion offers short-term incentives. | d | A is false: it mainly boosts immediate sales. R is true.
A: A direct channel gives the producer more control over sales. | There are no middlemen between producer and customer. | a | Both true; R explains A.
A: The results of digital marketing can be measured. | Clicks, views and sales can be tracked. | a | Both true; R explains A.
A: Advertising is a paid form of communication. | Advertising always involves face-to-face contact. | c | A is true; R is false: advertising is impersonal.
TT: promotion and distribution
S+: Advertising has an identified sponsor.
S+: Search engine optimisation helps a website rank higher.
S+: A direct channel has no middlemen.
S+: Digital marketing allows two-way communication.
S-: Sales promotion gives long-term incentives only.
S-: An indirect channel has no middlemen.
S-: Digital marketing results cannot be measured.
S-: Influencer marketing means selling through wholesalers.
K: C4 D4 5 | {p} makes handcrafted jewellery at home in {c} and has a very small budget. {He} wants to reach young buyers across India. | Suggest a promotion plan and a distribution channel, giving reasons. => Promotion: social media marketing and influencer marketing (low cost, targeted at young buyers), SEO for the website, a launch discount (sales promotion). Distribution: direct channel through own website or online marketplace: wide reach, low cost, control over sales.
K: C3 D3 3 | {f} runs an online bakery in {c}. Most of its orders come from people who search for 'cakes near me'. | Which digital marketing tool should it focus on? => Search engine optimisation. || State two advantages of digital marketing for it. => Low cost; targeted reach; measurable results; two-way communication (any two).
''', cat='term')

# ================================================================ Unit 4 Enterprise growth strategies

CH04_ST1 = spec('''
T: Growth strategy | A plan for increasing the size, sales and reach of an enterprise.
T: Market penetration | Selling more of existing products in existing markets.
T: Market development | Selling existing products in new markets.
T: Product development | Selling new products in existing markets.
T: Diversification | Selling new products in new markets.
T: Internal growth | Growth through the firm's own resources, such as expanding capacity or opening branches.
T: External growth | Growth through combining with other firms, such as mergers, acquisitions, joint ventures or franchising.
L: need | reasons for the growth of an enterprise | -
- Economies of scale | Cost per unit falls as output rises.
- Survival in competition | A larger firm can face rivals better.
- Higher profit | More sales usually mean more profit.
- Larger market share | Growth increases the firm's share of the market.
- Spreading risk | More products or markets reduce dependence on one.
- Ambition of the entrepreneur | The desire to build a bigger business.
L: ext | methods of external growth | -
- Mergers | Two firms combine into one.
- Acquisitions | One firm buys control of another.
- Joint ventures | Two firms create a new enterprise together.
- Franchising | Others are allowed to use the firm's brand and system for a fee.
- Strategic alliances | Firms cooperate without combining ownership.
Q: Which growth strategy is being used? | Market penetration; Market development; Product development; Diversification | -
- {f}, a dairy in {c}, offers discounts to sell more milk to its existing customers. | Market penetration | Existing product, existing market.
- {f} starts selling its pickles, so far sold only in {c}, in the Gulf countries. | Market development | Existing product, new market.
- {f}, a bakery, starts making sugar-free cakes for its existing customers. | Product development | New product, existing market.
- {f}, a textile firm, starts a hotel in a hill station. | Diversification | New product, new market.
- {f}, a mobile repair shop, starts selling mobile accessories to the same customers. | Product development | New product, existing market.
- {f} runs a campaign to make its present customers buy its juice more often. | Market penetration | Existing product, existing market.
- {f}, which sells school uniforms in cities, now sells them in rural areas. | Market development | Existing product, new market.
P: internal growth | external growth
- method | expanding the firm's own capacity and branches | combining with or using other firms
- speed | slow | fast
- control | the owner keeps full control | control may be shared
- example | opening a new branch | acquiring a rival firm
A: Growth helps an enterprise reap economies of scale. | Cost per unit falls as output increases. | a | Both true; R explains A.
A: Diversification means selling existing products in existing markets. | Diversification spreads risk across products and markets. | d | A is false: it means new products in new markets. R is true.
A: External growth is faster than internal growth. | It uses the resources of other firms. | a | Both true; R explains A.
A: Market development means entering new markets with existing products. | Market development always requires a new product. | c | A is true; R is false.
TT: growth strategies
S+: Market penetration means selling more existing products in existing markets.
S+: Diversification means new products in new markets.
S+: Economies of scale are a reason for growth.
S+: Mergers and acquisitions are methods of external growth.
S-: Product development means existing products in new markets.
S-: Internal growth is faster than external growth.
S-: Opening a new branch is an example of a merger.
S-: Growth never reduces the cost per unit.
K: C4 D4 5 | {f} makes organic jams in {c}. This year it (a) offered combo packs to sell more to its customers, (b) began exporting jams to Singapore, (c) launched organic honey for its customers, and (d) opened a farm-stay resort. | Identify the growth strategy in each of (a) to (d). => (a) Market penetration; (b) market development; (c) product development; (d) diversification. || State one reason why {f} wants to grow. => Economies of scale / spreading risk / higher profit / larger market share.
K: C3 D3 3 | {p}'s bakery is popular in one area of {c}. {He} wants to grow quickly without investing much of {his} own money. | Suggest an external growth method and give two reasons. => Franchising (or a strategic alliance): fast expansion; little own capital needed; uses franchisees' resources and local knowledge.
''', cat='term')

CH04_ST2 = spec('''
T: Franchising | An arrangement in which a franchisor allows a franchisee to use its brand, products and business system in return for fees.
T: Franchisor | The firm that owns the brand and business system and grants the franchise.
T: Franchisee | The person or firm that buys the right to operate under the franchisor's brand.
T: Royalty | A continuing fee, usually a percentage of sales, paid by the franchisee to the franchisor.
T: Franchise fee | An initial one-time payment made by the franchisee for the right to operate.
T: Business format franchising | Franchising in which the franchisee gets the whole business system, such as brand, recipes, layout and training.
L: types | types of franchising | -
- Product or trade-name franchising | The franchisee sells the franchisor's products under its name, as in car dealerships.
- Business format franchising | The whole system of running the business is given, as in fast-food chains.
- Manufacturing franchising | The franchisee is allowed to make and sell the product, as in soft-drink bottling.
L: adv | advantages of franchising to the franchisee | lim
- Proven brand and system | Customers already know the brand.
- Training and support | The franchisor trains staff and helps in setting up.
- Lower risk of failure | The business model has already been tested.
- Benefit of national advertising | The franchisor advertises the brand.
L: advf | advantages of franchising to the franchisor | lim
- Rapid expansion with little capital | Franchisees invest their own money.
- Motivated operators | Franchisees work hard as they are owners.
- Steady income from fees and royalty | Income comes from many outlets.
- Local knowledge | Franchisees know their local markets.
L: lim | limitations of franchising | adv
- Loss of some control for the franchisor | Outlets are run by independent owners.
- Fees and royalty for the franchisee | A part of sales goes to the franchisor.
- Restrictions on the franchisee | Products, prices and methods are fixed by the franchisor.
- Risk to the brand | One poorly run outlet can harm the whole brand.
Q: Which type of franchising is shown? | Product or trade-name franchising; Business format franchising; Manufacturing franchising; Joint venture | -
- A fast-food chain gives its franchisees its recipes, store design, uniforms and training. | Business format franchising | The whole system is given.
- A soft-drink company allows a bottler in {c} to make and sell its drink using its formula. | Manufacturing franchising | The franchisee manufactures the product.
- A car company appoints a dealer in {c} to sell its cars under its name. | Product or trade-name franchising | The franchisee sells the franchisor's products.
- A tuition brand gives its franchisees course material, teaching methods and branding. | Business format franchising | A complete business system is given.
- A shoe company appoints exclusive outlets that sell only its shoes under its brand. | Product or trade-name franchising | Products are sold under the brand.
P: franchisor | franchisee
- role | owns and grants the brand and system | operates an outlet under the brand
- payment | receives fees and royalty | pays fees and royalty
- risk | low capital risk in expansion | invests own capital in the outlet
A: Franchising helps a firm expand rapidly with little capital. | The franchisees invest their own money in the outlets. | a | Both true; R explains A.
A: A franchisee has full freedom to change the products and prices. | The franchisor lays down the products, prices and methods. | d | A is false; R is true.
A: Royalty is usually a percentage of the franchisee's sales. | It is paid continuously for the use of the brand. | a | Both true; R explains A.
A: A poorly run franchise outlet can harm the whole brand. | Customers link every outlet with the same brand. | a | Both true; R explains A.
A: Franchising lowers the risk of failure for the franchisee. | The franchisee must develop its own brand from scratch. | c | A is true; R is false: the franchisee uses an established brand.
TT: franchising
S+: The franchisee pays fees and royalty to the franchisor.
S+: Business format franchising gives the whole system of running the business.
S+: Franchising lets the franchisor expand with little capital.
S+: A soft-drink bottling arrangement is manufacturing franchising.
S-: The franchisor pays royalty to the franchisee.
S-: A franchisee can change the brand name freely.
S-: Franchising needs the franchisor to invest in every outlet.
S-: Franchising has no limitations.
K: C4 D4 5 | {p} wants to open a juice bar in {c}. {He} is choosing between starting {his} own brand and taking a franchise of a well-known juice chain that charges an initial fee and a royalty of 6% on sales. | State three advantages of taking the franchise. => Proven brand; training and support; lower risk; benefit of national advertising (any three). || State two limitations. => Fees and royalty; restrictions on products and prices; risk from other outlets harming the brand (any two).
K: C3 D3 3 | {f}, a popular biryani restaurant in {c}, wants to open 50 outlets across India in two years. | Suggest a growth method. => Franchising (business format). || Give two reasons. => Rapid expansion with little capital; motivated owner-operators; local knowledge of franchisees; steady royalty income (any two).
''', cat='franchising term')

CH04_ST3 = spec('''
T: Merger | A combination of two or more firms into a single firm.
T: Acquisition | The purchase of a controlling interest in one firm by another.
T: Horizontal merger | A merger of firms producing the same product at the same stage of production.
T: Vertical merger | A merger of firms at different stages of the same supply chain.
T: Conglomerate merger | A merger of firms in unrelated businesses.
T: Hostile takeover | An acquisition made against the wishes of the target firm's management.
T: Synergy | The idea that the combined firm is worth more than the two firms separately.
L: why | reasons for mergers and acquisitions | -
- Economies of scale | Larger output lowers the cost per unit.
- Synergy | The combined firm creates more value than the parts.
- Access to new markets | The buyer gains the other firm's customers.
- Reduction of competition | Combining with a rival reduces competition.
- Access to technology and talent | The buyer gets new technology and skilled staff.
- Diversification | Entering new lines of business spreads risk.
L: lim | problems in mergers and acquisitions | -
- Clash of cultures | Staff of the two firms may not work well together.
- High cost | Buying a firm can be very expensive.
- Loss of key staff | Talented employees may leave.
- Regulatory approval | Large mergers need approval from authorities such as the Competition Commission of India.
Q: Which type of merger is it? | Horizontal merger; Vertical merger; Conglomerate merger; Acquisition | -
- Two cement companies combine into one company. | Horizontal merger | Same product, same stage.
- A tea company merges with a tea-plantation company that supplies its leaves. | Vertical merger | Different stages of the same supply chain.
- A software company merges with a hotel chain. | Conglomerate merger | Unrelated businesses.
- {f} buys 60% of the shares of {f2}, which continues to run under its own name. | Acquisition | One firm buys control of another.
- A shoe manufacturer merges with a chain of shoe stores. | Vertical merger | Production and retail stages combine.
- Two airlines combine their operations into one airline. | Horizontal merger | Same business, same stage.
- A steel maker merges with a company that runs cinemas. | Conglomerate merger | Unrelated businesses.
P: merger | acquisition
- meaning | two or more firms combine into one | one firm buys control of another
- identity | the firms usually lose their separate identity | the acquired firm may keep its identity
- nature | usually by mutual agreement | may be friendly or hostile
A: A vertical merger combines firms at different stages of a supply chain. | It helps secure supplies or outlets. | a | Both true; R explains A.
A: A conglomerate merger combines firms making the same product. | A conglomerate merger helps diversification. | d | A is false: it combines unrelated businesses. R is true.
A: Mergers can lead to economies of scale. | The combined firm produces on a larger scale. | a | Both true; R explains A.
A: In an acquisition, the acquired firm may continue to exist under its own name. | An acquisition always ends the identity of the acquired firm. | c | A is true; R is false.
TT: mergers and acquisitions
S+: A horizontal merger combines firms in the same line of business.
S+: A vertical merger combines firms at different stages of production.
S+: A hostile takeover is against the wishes of the target firm's management.
S+: Synergy means the combined firm is worth more than the parts.
S-: A conglomerate merger combines firms in the same industry.
S-: An acquisition always needs the consent of the target's management.
S-: Mergers never face problems of culture.
S-: A vertical merger combines two direct competitors.
K: C4 D4 5 | {f}, a maker of packaged juices, (a) merged with a fruit-processing firm that supplies its pulp, (b) acquired 70% of a rival juice brand, and (c) is planning to merge with a real-estate developer. | Identify the type of combination in each case and state two problems it may face. => Vertical merger; (b) acquisition (of a competitor, horizontal); (c) conglomerate merger. Problems: clash of cultures; high cost; loss of key staff; regulatory approval (any two).
K: C3 D3 3 | Two bus operators on the same route in {c} combine into one company to cut costs and stop price wars. | Identify the type of merger. => Horizontal merger. || State two reasons for it in the case. => Economies of scale (cost cutting); reduction of competition (no price war).
''', cat='term')

CH04_ST4 = spec('''
T: Value addition | Increasing the worth of a product through processing, packaging, branding or service so that customers pay more for it.
T: Product line | A group of closely related products sold by a firm.
T: Product-line expansion | Adding new items to an existing product line.
T: Line extension | Adding new varieties, flavours or sizes under the same brand.
T: Upward stretching | Adding higher-priced, premium items to a product line.
T: Downward stretching | Adding lower-priced items to a product line.
L: ways | ways of adding value to a product | -
- Processing | Turning raw produce into a finished product, such as tomatoes into ketchup.
- Packaging | Attractive and convenient packs, such as single-serve sachets.
- Branding | A trusted name lets the firm charge more.
- Grading and quality certification | Sorting and certifying quality, such as organic certification.
- After-sales service | Installation, repair and warranty.
- Customisation | Making the product to the customer's needs.
L: why | reasons for product-line expansion | -
- Meets varied customer needs | Different sizes and flavours suit different buyers.
- Uses spare capacity | Existing machines and staff are used more fully.
- Increases sales | More products bring more sales.
- Uses brand goodwill | New items gain from the known brand.
- Competes with rivals | Gaps in the line are filled before rivals do.
Q: How is value being added or the product line expanded? | Processing; Packaging; Branding; After-sales service; Line extension; Upward stretching; Downward stretching | -
- A farmer in {c} turns {his} tomatoes into ketchup and sells it at a higher price. | Processing | Raw produce is processed.
- {f} sells its shampoo in ₹2 sachets for rural buyers. | Packaging | Convenient small packs add value.
- {f} adds mango and strawberry flavours to its existing yoghurt brand. | Line extension | New flavours under the same brand.
- {f}, known for budget phones, launches a premium phone at ₹70,000. | Upward stretching | A higher-priced item is added.
- {f}, a luxury car maker, launches a smaller, cheaper model. | Downward stretching | A lower-priced item is added.
- {f} offers free installation and a three-year warranty on its water purifiers. | After-sales service | Service adds value.
- A group of weavers sells their sarees under a common registered brand name and gets better prices. | Branding | A trusted name raises value.
P: value addition | product-line expansion
- meaning | increasing the worth of an existing product | adding new items to the product line
- focus | the same product made more valuable | more products in the range
- example | turning milk into cheese | adding new flavours of ice cream
A: Processing raw produce adds value to it. | Customers pay more for a processed, ready-to-use product. | a | Both true; R explains A.
A: Product-line expansion helps use spare capacity. | Existing machines and staff can make the new items. | a | Both true; R explains A.
A: Downward stretching adds premium products to a line. | Downward stretching adds lower-priced products. | d | A is false; R is true.
A: Line extension uses the goodwill of an existing brand. | New varieties are sold under the same brand. | a | Both true; R explains A.
A: Packaging can add value to a product. | Packaging only adds to cost and never to value. | c | A is true; R is false.
TT: value addition and product lines
S+: Turning milk into cheese is value addition by processing.
S+: Adding new flavours under the same brand is line extension.
S+: Upward stretching adds premium products.
S+: After-sales service can add value to a product.
S-: Downward stretching adds premium products.
S-: Value addition always reduces the price of a product.
S-: Product-line expansion means removing products from the line.
S-: Packaging can never add value.
K: C4 D4 5 | Women of a self-help group in {c} used to sell raw turmeric at low prices. Now they dry and grind it, pack it in attractive 100 g pouches, sell it under the brand 'Haldi Gold', and have also added chilli and coriander powders. | Identify three ways in which value has been added. => Processing; packaging; branding. || What is the addition of new powders called, and what are two benefits? => Product-line expansion (line extension): meets varied needs; uses spare capacity; increases sales; uses brand goodwill (any two).
K: C3 D3 3 | {f}, which sells mid-priced watches, wants to launch a luxury range and also a budget range for students. | Name the two strategies. => Upward stretching; downward stretching. || State one risk of each. => Upward: customers may not accept the brand as premium; downward: may harm the brand's image.
''', cat='term')

# ================================================================ Unit 6 Resource mobilisation (st2-st4)

CH06_ST2 = spec('''
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

CH06_ST3 = spec('''
T: Initial public offer | The first sale of shares by an unlisted company to the public.
T: SME exchange | A separate platform of a stock exchange for listing small and medium enterprises, such as BSE SME and NSE Emerge.
T: Book building | A method of issue in which the price is discovered from bids made within a price band.
T: Fixed price issue | A method of issue in which the company states the price of the shares in advance.
T: Red herring prospectus | A prospectus that does not contain the final price or the number of shares, used in book-built issues.
T: Listing | Admission of a company's securities for trading on a stock exchange.
T: SEBI | The regulator of the securities market in India, which protects investors and regulates public issues.
L: adv | advantages of raising funds through an IPO | lim
- Large amount of capital | Funds can be raised from many investors.
- No repayment obligation | Equity capital need not be repaid.
- Liquidity for existing shareholders | Shares can be sold on the exchange.
- Better image and credibility | A listed company gains public trust.
- Easier future fund-raising | Further issues become easier.
L: lim | limitations of raising funds through an IPO | adv
- High cost of issue | Fees, advertising and legal costs are high.
- Dilution of control | Ownership is shared with many shareholders.
- Strict disclosure | Results and important information must be made public.
- Time-consuming process | Approvals and documents take time.
L: sebi | functions of SEBI in public issues | -
- Lays down eligibility norms | Only eligible companies can make a public issue.
- Reviews the offer document | The draft prospectus is filed with SEBI.
- Requires full disclosure | Investors get the information needed to decide.
- Protects investors | It acts against fraud and misleading statements.
- Regulates intermediaries | Merchant bankers and registrars must be registered.
Q: Which concept is being described? | Book building; Fixed price issue; SME exchange; Red herring prospectus; Listing | -
- {f} invited bids between ₹240 and ₹250 per share and fixed the final price from the bids. | Book building | Price is discovered from bids in a band.
- {f} offered its shares to the public at ₹100 each, stated in the offer document. | Fixed price issue | The price is known in advance.
- {f}, a small engineering firm, listed its shares on a platform meant for small and medium enterprises. | SME exchange | A separate platform for SMEs.
- The document filed by {f} before its book-built issue did not show the final price. | Red herring prospectus | It omits the final price.
- Shares of {f} were admitted for trading on the stock exchange after the issue. | Listing | Securities are admitted for trading.
P: book building | fixed price issue
- price | discovered from bids within a price band | stated in advance
- demand | known daily during the issue | known only after the issue closes
- prospectus | red herring prospectus without final price | prospectus with the price
A: An SME exchange helps small enterprises raise equity capital. | It has eligibility norms suited to small and medium enterprises. | a | Both true; R explains A.
A: SEBI regulates public issues of shares. | SEBI protects the interests of investors in the securities market. | a | Both true; R explains A.
A: In a fixed price issue the price is discovered from bids. | In book building investors bid within a price band. | d | A is false; R is true.
A: An IPO dilutes the control of existing owners. | New shareholders get ownership and voting rights. | a | Both true; R explains A.
A: A red herring prospectus is used in book-built issues. | A red herring prospectus contains the final issue price. | c | A is true; R is false: it does not contain the final price.
TT: raising funds through the stock market
S+: An IPO is the first sale of shares to the public.
S+: In book building the price is discovered from bids.
S+: SEBI regulates public issues.
S+: BSE SME and NSE Emerge are platforms for small and medium enterprises.
S-: In a fixed price issue the price is found from bids.
S-: Equity raised through an IPO must be repaid in five years.
S-: An IPO has no cost for the company.
S-: SEBI fixes the price of every IPO.
K: C4 D4 5 | {f}, a growing food-processing company in {c}, needs ₹40 crore for expansion. Its promoters are thinking of an IPO but worry about the cost, the need to disclose results and the loss of control. | State three advantages of an IPO for {f}. => Large capital; no repayment; liquidity; better image; easier future fund-raising (any three). || State two limitations shown in the case. => High cost of issue; strict disclosure; dilution of control (any two). || Name the regulator. => SEBI.
K: C3 D3 3 | {p}'s ten-year-old auto-parts firm is too small for the main board of the stock exchange but wants to raise equity from the public. | Suggest a platform. => An SME exchange (BSE SME or NSE Emerge). || Give two benefits. => Access to equity capital; liquidity for shareholders; better visibility and credibility.
''', cat='term')

CH06_ST4 = spec('''
T: Non-financial resources | Resources other than money that a start-up needs, such as technology, mentors, networks, people and infrastructure.
T: Incubator | An organisation that supports early-stage start-ups with space, mentoring, networks and services, often for a longer period.
T: Accelerator | A fixed-term programme that helps a group of start-ups grow fast through mentoring and investor connections.
T: Mentor | An experienced person who guides an entrepreneur with advice and contacts.
T: Networking | Building relationships with people and organisations that can help the business.
T: Technology transfer | Obtaining technology developed by another organisation, such as a research institute, for commercial use.
L: inc | services provided by incubators | -
- Workspace | Office space and shared facilities at low cost.
- Mentoring | Guidance from experienced entrepreneurs and experts.
- Access to networks | Contacts with investors, customers and suppliers.
- Business services | Help with legal, accounting and registration work.
- Access to funding | Seed grants or introductions to investors.
L: res | non-financial resources needed by a start-up | -
- Technology | Machines, software and know-how.
- Human resources | Skilled and committed team members.
- Mentors | Guidance from experienced people.
- Networks | Links with customers, suppliers and investors.
- Infrastructure | Workspace, utilities and logistics.
Q: Which non-financial resource is being mobilised? | Technology; Mentors; Networks; Incubator support; Human resources | -
- {p} licensed a water-purification process developed by a national research laboratory. | Technology | Technology transfer from a research institute.
- A retired CEO meets {p} every month to advise {him} on strategy. | Mentors | An experienced person gives guidance.
- {p} joined a business association in {c} to meet suppliers and buyers. | Networks | Relationships are built.
- {p}'s start-up got low-cost office space and legal help at a university centre for new ventures. | Incubator support | Space and services for early start-ups.
- {p} hired two engineers who share {his} vision and agreed to take part of their pay in shares. | Human resources | A committed team is built.
- {p} met three investors at a start-up conference. | Networks | Contacts are made through networking.
P: incubator | accelerator
- stage | very early, idea or prototype stage | start-ups with a product and early customers
- duration | longer and flexible | short, fixed term
- focus | building the business | rapid growth
A: Incubators help early-stage start-ups. | They provide workspace, mentoring and business services. | a | Both true; R explains A.
A: A mentor provides advice and contacts. | Mentors have experience that the entrepreneur may lack. | a | Both true; R explains A.
A: Non-financial resources are not important for start-ups. | Technology, people and networks are needed to run a business. | d | A is false; R is true.
A: Accelerators run fixed-term programmes. | Accelerators only provide office space for many years. | c | A is true; R is false.
TT: non-financial resources
S+: Incubators provide workspace and mentoring.
S+: Mentors guide entrepreneurs with advice and contacts.
S+: Networking helps in meeting investors and customers.
S+: Technology transfer brings research into commercial use.
S-: Incubators are banks that give loans.
S-: Networking is not useful for a start-up.
S-: Accelerators work only with ideas that have no product yet.
S-: A mentor is a person who buys the company.
K: C4 D4 5 | {p} has an idea for a low-cost prosthetic limb. {He} has a little money but no workspace, no business experience, no contacts with hospitals and no manufacturing know-how. | Suggest five non-financial resources {he} should mobilise and how each will help. => Incubator: workspace and services; mentor: business guidance; networks: contacts with hospitals and buyers; technology transfer: manufacturing know-how from a research lab; human resources: skilled engineers.
K: C3 D3 3 | {p}'s start-up was selected for a four-month programme that gave intensive mentoring and ended with a demo day before investors. | What kind of programme is this? => An accelerator. || How is it different from an incubator? => It is short and fixed-term, focuses on rapid growth, and works with start-ups that already have a product; incubators support earlier stages for longer.
''', cat='term')

THEORY = {
    '01-st1': CH01_ST1, '01-st2': CH01_ST2, '01-st3': CH01_ST3, '01-st4': CH01_ST4,
    '02-st1': CH02_ST1, '02-st2': CH02_ST2, '02-st3': CH02_ST3, '02-st4': CH02_ST4,
    '03-st1': CH03_ST1, '03-st2': CH03_ST2, '03-st3': CH03_ST3, '03-st4': CH03_ST4,
    '04-st1': CH04_ST1, '04-st2': CH04_ST2, '04-st3': CH04_ST3, '04-st4': CH04_ST4,
    '06-st2': CH06_ST2, '06-st3': CH06_ST3, '06-st4': CH06_ST4,
}

FAMILIES = {S + k: efacts(v) for k, v in THEORY.items()}
