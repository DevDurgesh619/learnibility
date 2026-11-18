"""CBSE class 11 entrepreneurship (066) families: theory fact tables for chapters 1, 2, 3 (st1) and 4.

Fact text uses g12_business_a.spec() (line format documented there). `efacts()` is a copy of the adapter written
for the class 12 entrepreneurship bank: it wraps g11_accountancy_kit.facts() for the entrepreneurship paper
(1, 2, 3 and 5 marks), drops the 4- and 6-mark generators, adds 2-mark "explain one point" and "two bases" items
and 5-mark "explain any five" items, and tags cases by marks.
Mock kinds: 'mcq', 'ar', 'm2'/'m3'/'m5' (explain and list items) and 'm2c'/'m3c'/'m5c' (scenario, case and
computed application items).
"""
from __future__ import annotations

from g11_accountancy_kit import FF, facts, Cyc, ctx, fill
from g12_business_a import spec

S = 'cbse-g11-entrepreneurship-ch'
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
    for (k, title, pts, con) in sp.get('lists') or []:
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


# ================================================================ ch01 Entrepreneurship: concept and functions

CH01_ST1 = spec('''
T: Entrepreneurship | The process of identifying an opportunity, mobilising resources and creating a new enterprise while bearing risk, in order to create value.
T: Entrepreneur | A person who sees an opportunity, takes the initiative, bears the risk and organises resources to start and run a new venture.
T: Enterprise | The business unit or organisation that is created as a result of entrepreneurship.
T: Value creation | Producing goods or services that are worth more to customers than the resources used to make them.
T: Uncertainty | A situation in which future outcomes cannot be predicted or insured against, which the entrepreneur must face.
L: char | characteristics of entrepreneurship | -
- Economic and dynamic activity | It creates and runs enterprises that produce value, and it keeps changing with the environment.
- Related to innovation | It involves new products, methods or markets, or new ways of doing things.
- Profit potential | It is undertaken with the expectation of earning a reward for the effort and risk.
- Risk bearing | The entrepreneur bears the risk of loss when outcomes are uncertain.
- Purposeful activity | It is directed at a goal, such as meeting a need in the market.
- Creative response to the environment | It turns changes and problems in the environment into opportunities.
- Gap filling | It fills gaps in the market, such as a product or service that is missing.
L: proc | stages of entrepreneurship as a process | -
- Discovery of an opportunity | Spotting an unmet need or a problem that can be solved.
- Concept development | Turning the idea into a clear plan of what will be offered and to whom.
- Resourcing | Arranging finance, people, materials and technology.
- Actualisation | Starting the venture and running its operations.
- Harvesting | Reaping the rewards, expanding, or exiting the venture.
P: entrepreneurship | entrepreneur
- meaning | the process of creating a new venture | the person who carries out the process
- nature | an activity or function | an individual (or a team)
- relationship | the result of the entrepreneur's actions | the actor whose actions create entrepreneurship
Q: Which characteristic of entrepreneurship is shown most clearly? | Risk bearing; Related to innovation; Gap filling; Creative response to the environment; Profit potential | -
- {p} invested all {his} savings in a new food truck, knowing it might fail. | Risk bearing | The outcome was uncertain and {p} could lose the money invested.
- {p} found that no shop in {his} town repaired hearing aids, so {he} started one. | Gap filling | It fills a gap in the market.
- {p} developed a new method of making paper from banana stems. | Related to innovation | It is a new method of production.
- When schools moved online during the lockdown, {p} began renting out laptops to students. | Creative response to the environment | A change in the environment was turned into an opportunity.
- {p} left a salaried job to start a firm because {he} expected to earn much more than {his} salary. | Profit potential | The venture was started in the hope of a reward for effort and risk.
A: Entrepreneurship involves risk bearing. | The future outcomes of a new venture are uncertain. | a | Both true; R explains A.
A: Entrepreneurship is a static activity. | Entrepreneurs respond to changes in the environment. | d | A is false: it is a dynamic activity. R is true.
A: Entrepreneurship is a purposeful activity. | It is directed at goals such as meeting a need in the market. | a | Both true; R explains A.
A: An entrepreneur only manages an existing business. | Entrepreneurship involves creating a new venture. | d | A is false: the entrepreneur creates the venture. R is true.
TT: the concept of entrepreneurship
S+: Entrepreneurship is a process of creating value.
S+: Entrepreneurship involves risk and uncertainty.
S+: The enterprise is the result of entrepreneurship.
S+: Entrepreneurship responds creatively to changes in the environment.
S-: Entrepreneurship involves no risk.
S-: Entrepreneurship is the same as getting a salaried job.
S-: Entrepreneurship is a one-time act with no stages.
S-: Entrepreneurship never involves innovation.
K: C4 D4 5 | {p} noticed that farmers near {c} threw away tonnes of tomatoes when prices fell. {He} borrowed money, set up a small unit to make tomato puree, hired four workers and sold the puree to hotels. In the first year {he} made a loss, but {he} did not give up. | Identify three characteristics of entrepreneurship shown in the case. => Gap filling or creative response (turning waste into a product); risk bearing (borrowed money, first-year loss); profit potential and purposeful activity (selling to hotels) (any three). || Which stages of the entrepreneurial process can you identify? => Discovery of an opportunity; resourcing (borrowing, hiring); actualisation (production and sale).
K: C3 D3 3 | {p} has an idea for a mobile app that books slots at crowded government offices. | Name three stages {he} must go through to turn it into a venture. => Concept development; resourcing; actualisation (and later harvesting).
''', cat='term')

CH01_ST2 = spec('''
T: Innovation | The introduction of something new, such as a new product, method, market, source of supply or organisation.
T: Risk bearing | Accepting the possibility of loss in return for the chance of profit.
T: Organising | Bringing together and arranging land, labour, capital and other resources for production.
T: Managing | Planning, directing and controlling the activities of the enterprise to achieve its goals.
T: Creative destruction | Schumpeter's idea that innovations replace old products and methods, driving economic change.
L: func | functions of an entrepreneur | -
- Innovation | Introducing new products, methods, markets or forms of organisation.
- Risk bearing | Bearing the risk of loss in an uncertain environment.
- Organising | Combining resources such as land, labour, capital and technology.
- Managing | Planning, coordinating and controlling the enterprise.
- Decision-making | Choosing what to produce, how, where and for whom.
- Discovery of an idea | Spotting and evaluating an opportunity.
- Determining the business objectives | Setting clear goals for the venture.
L: inn | forms of innovation described by Schumpeter | -
- New product | Introducing a good that is new to customers or of a new quality.
- New method of production | Using a new process or technology.
- New market | Opening a market that the firm has not entered before.
- New source of supply | Finding a new source of raw materials or parts.
- New organisation | Creating a new structure in an industry.
Q: Which function of the entrepreneur is shown? | Innovation; Risk bearing; Organising; Managing; Decision-making | -
- {p} launched the first sugar-free ice cream made from dates in {c}. | Innovation | A new product was introduced.
- {p} put {his} house as security for a loan to start {his} factory. | Risk bearing | {p} accepted the possibility of losing the house.
- {p} rented a shed, bought machines, hired ten workers and arranged raw material for {his} unit. | Organising | Resources were brought together for production.
- Every week {p} sets sales targets, checks progress and corrects problems in {his} shop. | Managing | It involves planning, directing and controlling.
- {p} had to choose whether to make the product in {c} or buy it from a supplier. | Decision-making | {p} is choosing how and where to produce.
- {p} began exporting {his} handloom sarees to Dubai for the first time. | Innovation | Opening a new market is a form of innovation.
A: Innovation is regarded as a key function of an entrepreneur. | Schumpeter saw the entrepreneur as an innovator who introduces new combinations. | a | Both true; R explains A.
A: Opening a new market is a form of innovation. | Schumpeter listed new markets among the forms of innovation. | a | Both true; R explains A.
A: Risk bearing is avoided by entrepreneurs. | Entrepreneurs accept uncertainty in the hope of profit. | d | A is false: risk bearing is a function of the entrepreneur. R is true.
A: Organising is a function of an entrepreneur. | The entrepreneur brings together land, labour and capital. | a | Both true; R explains A.
A: Managing is the only function of an entrepreneur. | An entrepreneur plans, directs and controls the enterprise. | d | A is false: innovation, risk bearing and organising are also functions. R is true.
TT: the functions of an entrepreneur
S+: Schumpeter described the entrepreneur as an innovator.
S+: Opening a new market is a form of innovation.
S+: Organising means bringing together resources for production.
S+: The entrepreneur bears the risk of loss.
S-: An entrepreneur never makes decisions.
S-: Innovation means only inventing a new machine.
S-: Risk bearing is a function of the customer.
S-: Organising means advertising the product.
K: C4 D4 5 | {p} found a supplier of cheap bamboo in Assam and started making bamboo toothbrushes in {c}. {He} took a bank loan, hired six workers, set monthly targets and reviewed them every week. Later {he} began selling the brushes in Europe. | Identify the functions of the entrepreneur in the case. => New source of supply and new product (innovation); bank loan (risk bearing); hiring workers and arranging material (organising); setting and reviewing targets (managing). || Which form of innovation does selling in Europe show? => New market.
K: C3 D3 3 | {p} runs a small dhaba. {He} decided to deliver food through an app and use a new solar cooker that cut fuel costs. | Name the forms of innovation. => New method of production (solar cooker); new market or new way of reaching customers (app delivery). || Who is associated with this view of innovation? => Joseph Schumpeter.
''', cat='term')

CH01_ST3 = spec('''
T: Economic development | A sustained rise in the output and living standards of an economy, along with structural change.
T: Employment generation | Creating jobs for oneself and for others through new enterprises.
T: Balanced regional development | The growth of enterprises in backward as well as developed regions, reducing regional inequality.
T: Capital formation | The mobilisation of savings into productive investment.
T: Per capita income | The average income per person in an economy.
L: imp | points of importance of entrepreneurship for economic development | -
- Employment generation | New enterprises create jobs for the entrepreneur and for others.
- Capital formation | Entrepreneurs mobilise savings into productive investment.
- Balanced regional development | Enterprises set up in backward areas spread growth more evenly.
- Increase in per capita income | Higher output and employment raise incomes.
- Improvement in living standards | New and cheaper goods and services become available.
- Innovation and technological progress | Entrepreneurs introduce new products and methods.
- Promotion of exports | Enterprises that sell abroad earn foreign exchange.
L: need | reasons why India needs more entrepreneurs | -
- Large and growing workforce | Salaried jobs alone cannot employ everyone.
- Use of local resources | Entrepreneurs turn local raw materials and skills into products.
- Reducing regional inequality | Enterprises in rural and backward areas bring growth there.
- Solving social problems | Entrepreneurs find solutions for health, education and environmental problems.
- Self-reliance | Local production reduces dependence on imports.
Q: Which contribution of entrepreneurship to the economy is shown? | Employment generation; Capital formation; Balanced regional development; Promotion of exports; Improvement in living standards | -
- {p} set up a food-processing unit in {his} village and employed 40 local youths. | Employment generation | It created jobs for others.
- {p} persuaded friends and relatives to invest their savings in {his} new factory. | Capital formation | Savings were turned into productive investment.
- {p} chose a backward district for {his} new textile unit instead of a big city. | Balanced regional development | Growth reaches a backward area.
- {f} began shipping its handicrafts to buyers in Europe and the USA. | Promotion of exports | Selling abroad earns foreign exchange.
- {p} started a low-cost clinic so that villagers no longer had to travel 50 km to see a doctor. | Improvement in living standards | A needed service became available at low cost.
A: Entrepreneurship promotes balanced regional development. | Enterprises set up in backward areas bring jobs and incomes there. | a | Both true; R explains A.
A: Entrepreneurship helps in capital formation. | Entrepreneurs mobilise idle savings into productive investment. | a | Both true; R explains A.
A: Entrepreneurship reduces employment. | New enterprises create jobs for the entrepreneur and others. | d | A is false: it generates employment. R is true.
A: Entrepreneurs help raise living standards. | They offer new and cheaper goods and services. | a | Both true; R explains A.
TT: entrepreneurship and economic development
S+: Entrepreneurs create jobs for others.
S+: Entrepreneurship can reduce regional inequality.
S+: Exporting enterprises earn foreign exchange.
S+: Entrepreneurs mobilise savings into investment.
S-: Entrepreneurship has no effect on employment.
S-: Entrepreneurship increases regional inequality in all cases.
S-: Entrepreneurs only consume and never invest.
S-: Economic development means only a rise in population.
K: C4 D4 5 | {p} returned to {his} village in a backward district after studying food technology. {He} set up a unit that makes millet snacks, buys millets from 300 local farmers, employs 25 women and now sells to supermarkets in three states and to buyers abroad. | Explain five ways in which {p}'s enterprise contributes to economic development. => Employment generation (25 women); balanced regional development (backward district); higher incomes for farmers (per capita income); use of local resources and self-reliance; promotion of exports; capital formation (investment in the unit).
K: C3 D3 3 | A state government offers subsidies to people who set up small units in its hill districts. | Why does the government do this? Give three reasons. => Balanced regional development; employment generation in those districts; use of local resources; reducing migration to cities (any three).
''', cat='term')

CH01_ST4 = spec('''
T: Myth | A widely held but false belief.
T: Startup ecosystem | The network of founders, investors, incubators, mentors, universities, government and markets that supports new ventures.
T: Startup India | The Government of India initiative launched in January 2016 to promote start-ups through recognition, funding and easier compliance.
T: Incubator | An organisation that helps early-stage start-ups with workspace, mentoring and contacts.
T: Fear of failure | The anxiety about losing money or social standing that stops many people from starting a business.
L: myth | myths about entrepreneurship | -
- Entrepreneurs are born, not made | Entrepreneurial skills can be learned through education, training and experience.
- Entrepreneurship needs a lot of money | Many ventures start small, and funds can be raised from many sources.
- Entrepreneurs are gamblers | They take calculated, moderate risks, not blind gambles.
- An entrepreneur must have a new invention | Many succeed by improving existing products or serving new markets.
- Only young people can be entrepreneurs | People of any age can start ventures.
- Entrepreneurship is only for people from business families | First-generation entrepreneurs succeed in many fields.
L: obs | obstacles to entrepreneurship in India | -
- Lack of finance | Banks often ask for security that new entrepreneurs do not have.
- Fear of failure and social attitudes | Failure is seen as a stigma, and salaried jobs are preferred.
- Complex regulations | Licences, registrations and compliance take time and money.
- Lack of skills and training | Many lack business, technical or marketing skills.
- Poor infrastructure | Power, transport and internet may be inadequate in some areas.
- Difficulty in reaching markets | Small firms find it hard to compete with large brands.
Q: Which myth about entrepreneurship is being expressed? | Entrepreneurs are born, not made; Entrepreneurship needs a lot of money; Entrepreneurs are gamblers; Only young people can be entrepreneurs; An entrepreneur must have a new invention | -
- {p}'s uncle says, "You cannot learn to be an entrepreneur; either it is in your blood or it is not." | Entrepreneurs are born, not made | Entrepreneurial skills can be learned.
- {p} says {he} cannot start a business until {he} has saved ₹50 lakh. | Entrepreneurship needs a lot of money | Many ventures start small and raise funds from different sources.
- {p}'s friends say that starting a business is like betting at a race. | Entrepreneurs are gamblers | Entrepreneurs take calculated, moderate risks.
- {p}, aged 55, is told that it is too late to start a business. | Only young people can be entrepreneurs | People of any age can start ventures.
- {p} thinks {he} can never start a business because {he} has not invented anything new. | An entrepreneur must have a new invention | Improving existing products can also succeed.
A: Entrepreneurship can be learned. | Training, education and experience develop entrepreneurial skills. | a | Both true; R explains A.
A: Entrepreneurs are reckless gamblers. | Entrepreneurs take calculated risks. | d | A is false: they take moderate, calculated risks. R is true.
A: Lack of finance is an obstacle for new entrepreneurs. | Banks often require security that new entrepreneurs lack. | a | Both true; R explains A.
A: Startup India was launched to promote start-ups. | It offers recognition, funding support and easier compliance. | a | Both true; R explains A.
TT: entrepreneurship in India
S+: Entrepreneurial skills can be developed through training.
S+: Many ventures start with small capital.
S+: Fear of failure stops many people from starting a business.
S+: Startup India was launched in 2016.
S-: Entrepreneurs are always born into business families.
S-: Every entrepreneur needs crores of rupees to start.
S-: Entrepreneurs take blind risks like gamblers.
S-: Startup India was launched in 1991.
K: C4 D4 5 | {p}, a first-generation college graduate in {c}, wants to start a small organic-soap business. {His} parents say that business is only for people from business families, that it needs huge capital and that it is a gamble. Banks have asked for security {he} does not have. | Identify the myths in the parents' views and correct them. => Entrepreneurs come only from business families – first-generation entrepreneurs succeed; needs huge capital – ventures can start small; a gamble – entrepreneurs take calculated risks. || Identify the obstacle {he} faces and suggest one way to overcome it. => Lack of finance; approach schemes such as MUDRA loans, angel investors, or start small with own savings.
K: C3 D3 3 | {p}'s start-up in {c} got office space, a mentor and introductions to investors at an incubator in a college. | Name the part of the startup ecosystem that helped. => Incubator. || Name two other parts of the startup ecosystem. => Investors (angels, venture capital); government schemes such as Startup India; mentors; universities; markets and customers (any two).
''', cat='term')

# ================================================================ ch02 An entrepreneur

CH02_ST1 = spec('''
T: Innovative entrepreneur | An entrepreneur who introduces new products, methods or markets.
T: Imitating entrepreneur | An entrepreneur who copies successful innovations made by others, often adapting them to local needs.
T: Fabian entrepreneur | A cautious entrepreneur who adopts change only when failure to do so would cause losses.
T: Drone entrepreneur | An entrepreneur who refuses to change even at the cost of falling profits.
T: Social entrepreneur | An entrepreneur whose main aim is to solve a social problem while running a sustainable venture.
T: Techno-entrepreneur | An entrepreneur who builds a venture on science or technology.
T: Rural entrepreneur | An entrepreneur who sets up a venture in a rural area, often using local resources.
L: types | types of entrepreneurs according to Clarence Danhof | -
- Innovative | Introduces new goods, methods or markets.
- Imitating (adoptive) | Copies successful innovations of others.
- Fabian | Cautious and sceptical; changes only when forced.
- Drone | Refuses to change even when profits fall.
L: oth | other types of entrepreneurs | -
- Social entrepreneur | Aims at solving a social problem in a sustainable way.
- Woman entrepreneur | A woman or group of women who start and run an enterprise.
- Rural entrepreneur | Sets up a venture in a rural area using local resources.
- Techno-entrepreneur | Builds a venture on science and technology.
- Agri-entrepreneur | Runs a venture in agriculture or allied activities.
P: innovative entrepreneur | imitating entrepreneur
- approach | introduces new products or methods | copies successful products or methods
- risk | high risk | lower risk
- where common | more common in developed and fast-changing industries | more common in developing economies
Q: Which type of entrepreneur is this? | Innovative entrepreneur; Imitating entrepreneur; Fabian entrepreneur; Drone entrepreneur; Social entrepreneur; Techno-entrepreneur | -
- {p} was the first to sell sugarcane juice in tetra packs in {c}. | Innovative entrepreneur | {p} introduced a new product.
- After seeing cloud kitchens succeed in Bengaluru, {p} opened one in {his} town. | Imitating entrepreneur | {p} copied a successful idea.
- {p} started selling online only after {his} offline sales fell sharply. | Fabian entrepreneur | {p} adopted change only when forced.
- {p} refuses to accept digital payments even though customers are going to other shops. | Drone entrepreneur | {p} refuses to change despite losses.
- {p} runs a venture that trains and employs visually impaired people to make candles. | Social entrepreneur | The main aim is to solve a social problem.
- {p}, an engineer, set up a firm that makes sensors to detect leaks in water pipes. | Techno-entrepreneur | The venture is built on technology.
A: Imitating entrepreneurs are important in developing economies. | They adapt innovations made elsewhere to local needs. | a | Both true; R explains A.
A: A drone entrepreneur readily adopts new methods. | A drone entrepreneur refuses to change even at the cost of losses. | d | A is false: drones resist change. R is true.
A: A Fabian entrepreneur is very cautious. | A Fabian entrepreneur adopts change only when failure to do so would cause losses. | a | Both true; R explains A.
A: Social entrepreneurs ignore financial sustainability. | Their main aim is solving a social problem. | d | A is false: they run sustainable ventures. R is true.
TT: types of entrepreneurs
S+: Clarence Danhof classified entrepreneurs as innovative, imitating, Fabian and drone.
S+: An innovative entrepreneur introduces new goods or methods.
S+: A drone entrepreneur refuses to change.
S+: A social entrepreneur aims to solve a social problem.
S-: A Fabian entrepreneur is always the first to try new ideas.
S-: An imitating entrepreneur invents completely new products.
S-: A drone entrepreneur welcomes change.
S-: Social entrepreneurs never earn revenue.
K: C4 D4 5 | Four shopkeepers in {c}: A started the town's first app-based grocery delivery; B copied it a year later; C began delivery only after losing half his customers; D still refuses to deliver even though his sales keep falling. | Identify the type of entrepreneur each represents according to Danhof, with a reason. => A – innovative (first to introduce); B – imitating (copied a successful idea); C – Fabian (changed only when forced by losses); D – drone (refuses to change despite losses). || Which type is most useful in a developing economy and why? => Imitating, because they spread proven innovations quickly at lower risk.
K: C3 D3 3 | {p} and three other women of a self-help group in a village started making jute bags and selling them in nearby towns. | Identify two types of entrepreneurs they represent. => Women entrepreneurs; rural entrepreneurs. || Give one feature of each. => Women entrepreneurs – enterprise started and run by women; rural – set up in a village using local resources.
''', cat='term')

CH02_ST2 = spec('''
T: Competency | An underlying characteristic, such as knowledge, skill or motive, that leads to effective performance.
T: Need for achievement | The desire to excel and accomplish challenging goals, which McClelland linked with entrepreneurship.
T: Initiative | Doing things before being asked or forced by events.
T: Persistence | Continuing to work towards a goal despite obstacles.
T: Self-confidence | Belief in one's own ability to complete a task or meet a challenge.
T: Calculated risk taking | Taking moderate risks after weighing the likely gains and losses.
L: comp | competencies of an entrepreneur | -
- Initiative | Acts before being asked or forced by events.
- Sees and acts on opportunities | Spots unusual opportunities and seizes them.
- Persistence | Keeps trying despite obstacles and setbacks.
- Information seeking | Gathers information from customers, suppliers and experts.
- Concern for high quality of work | Wants to do things better than others.
- Commitment to work | Makes personal sacrifices to complete a job.
- Systematic planning | Breaks large tasks into smaller steps and plans them.
- Problem solving | Finds new ideas to overcome problems.
- Self-confidence | Believes in own ability to succeed.
- Persuasion | Convinces others to buy, invest or support.
L: val | entrepreneurial values and attitudes | -
- Innovativeness and creativity | Willingness to try new ideas.
- Independence | Desire to be one's own boss and take decisions.
- Respect for work | Treating all work as worthy of effort.
- Openness to feedback and learning from failure | Using mistakes to improve.
- Ethical conduct | Honesty and fairness with customers, workers and society.
P: competency | trait
- meaning | an ability shown in performance that can be learned and developed | a relatively stable personal quality
- development | developed through training and practice | changes slowly, if at all
- example | systematic planning, information seeking | self-confidence, need for achievement
Q: Which competency is the entrepreneur showing? | Initiative; Persistence; Information seeking; Systematic planning; Persuasion; Concern for high quality of work | -
- Before launching {his} juice bar, {p} talked to 100 office workers about their drinks preferences. | Information seeking | Information was gathered from potential customers.
- {p}'s first two shops failed, but {he} studied the mistakes and opened a third. | Persistence | {p} kept trying despite setbacks.
- {p} convinced a bank manager to give a loan by showing {his} sales records and plans. | Persuasion | {p} convinced someone to support the venture.
- {p} divided {his} launch into weekly tasks with a deadline for each. | Systematic planning | A large task was broken into planned steps.
- {p} started a delivery service before any competitor thought of it, without waiting for anyone to ask. | Initiative | {p} acted without being asked or forced.
- {p} rejects any batch of pickles that does not meet {his} strict taste standard. | Concern for high quality of work | {p} insists on doing things better.
A: Entrepreneurs usually take calculated risks. | They weigh gains and losses before deciding. | a | Both true; R explains A.
A: Competencies can be developed through training. | They are abilities shown in performance, made up of knowledge, skills and motives. | a | Both true; R explains A.
A: McClelland linked entrepreneurship with the need for achievement. | People high in need for achievement like challenging goals and feedback. | a | Both true; R explains A.
A: Persistence means giving up at the first failure. | Entrepreneurs often face setbacks. | d | A is false: persistence means continuing despite obstacles. R is true.
TT: entrepreneurial competencies
S+: Information seeking is an entrepreneurial competency.
S+: Entrepreneurs usually take moderate, calculated risks.
S+: Competencies can be learned and developed.
S+: McClelland linked entrepreneurship with the need for achievement.
S-: Entrepreneurs avoid all information from customers.
S-: Competencies can never be developed.
S-: Entrepreneurs take only very high, blind risks.
S-: Persistence means stopping after the first failure.
K: C4 D4 5 | Before opening a cycle-repair and rental shop near a college in {c}, {p} met students to learn what they needed, prepared a month-by-month plan, and convinced {his} uncle to invest. When the first location failed, {he} moved to a better site and kept going. {He} checks every repaired cycle personally. | Identify five competencies shown by {p}, quoting the lines. => Information seeking (met students); systematic planning (month-by-month plan); persuasion (convinced uncle); persistence (kept going after failure); concern for high quality (checks every cycle).
K: C3 D3 3 | {p} always sets difficult sales targets for {his} shop and likes regular feedback on how {he} is doing. | Which motive is shown? => Need for achievement. || Who linked it with entrepreneurship? => David McClelland. || Give one other trait of entrepreneurs. => Self-confidence; calculated risk taking; initiative; persistence (any one).
''', cat='term')

CH02_ST3 = spec('''
T: Intrapreneur | An employee who acts like an entrepreneur within an existing organisation, developing new products or processes.
T: Manager | A person who plans, organises, directs and controls the work of others in an organisation to achieve its goals.
T: Ownership | The right to the assets and profits of a business, along with its risks.
T: Salary | A fixed payment received by an employee for work.
T: Profit | The reward that an entrepreneur receives for bearing risk, which may be uncertain.
P: entrepreneur | manager
- motive | to start a venture and create value | to run an existing organisation efficiently
- status | owner of the enterprise | employee of the enterprise
- risk | bears the risk and uncertainty | does not bear the risk of ownership
- reward | profit, which is uncertain | salary, which is fixed
- innovation | introduces new ideas and changes | carries out existing plans and policies
P: entrepreneur | intrapreneur
- dependence | independent, owns the venture | works within an organisation
- funds | raises funds personally | uses funds of the organisation
- risk | bears the full risk | the organisation bears most of the risk
- reward | profit | salary, bonus or recognition
L: intra | features of an intrapreneur | -
- Works within an organisation | An intrapreneur is an employee, not an owner.
- Innovative | Develops new products, services or processes for the organisation.
- Uses the organisation's resources | Funds, staff and facilities are provided by the employer.
- Limited risk | The organisation bears most of the financial risk.
- Driven by recognition and achievement | Rewards include bonuses, promotion and freedom to work on ideas.
Q: Who is this person? | Entrepreneur; Intrapreneur; Manager; Investor | -
- {p} left {his} job, used {his} savings and started a company making eco-friendly plates. | Entrepreneur | {p} owns the venture and bears the risk.
- {p}, an engineer at a large car company, proposed and led a team that developed a new electric scooter for the firm. | Intrapreneur | {p} innovated within an organisation using its resources.
- {p} is paid a salary to supervise 40 workers and ensure that daily production targets are met. | Manager | {p} runs existing operations for a salary.
- {p} took a loan in {his} own name to open a coaching centre. | Entrepreneur | {p} owns the venture and bears the risk.
- A bank employee, {p}, designed a new mobile app for the bank's farmer customers and was given a team to build it. | Intrapreneur | {p} innovated inside the organisation with its resources.
- {p} is employed to keep the accounts and the staff of a hotel running smoothly. | Manager | {p} runs existing operations for a salary.
A: An entrepreneur's reward is uncertain. | Profit depends on the success of the venture. | a | Both true; R explains A.
A: An intrapreneur bears the full financial risk of an idea. | An intrapreneur uses the funds of the organisation. | d | A is false: the organisation bears most of the risk. R is true.
A: An entrepreneur introduces new ideas and changes. | A manager receives a fixed salary. | b | Both are true, but R is about the manager's reward and does not explain A.
A: Intrapreneurs help large firms remain innovative. | They develop new products and processes inside the organisation. | a | Both true; R explains A.
TT: entrepreneurs, intrapreneurs and managers
S+: An intrapreneur works within an existing organisation.
S+: A manager receives a salary.
S+: An entrepreneur bears the risk of the venture.
S+: An entrepreneur's reward is profit, which is uncertain.
S-: A manager is always the owner of the business.
S-: An intrapreneur raises all funds personally.
S-: An entrepreneur receives a fixed salary.
S-: A manager bears the full risk of ownership.
K: C4 D4 5 | {p} works at a large food company in {c}. {He} suggested a millet-based breakfast cereal, and the company gave {him} a budget and a team to develop it. {His} friend {p2} left a similar job, borrowed money and started an independent snacks brand. A third friend supervises a factory for a fixed salary. | Identify the role of each person. => {p} – intrapreneur; {p2} – entrepreneur; third friend – manager. || Distinguish between {p} and {p2} on three bases. => Dependence: within the company vs independent owner; funds: company's vs own/borrowed; risk: borne mainly by the company vs fully by {p2}; reward: salary/bonus vs profit (any three).
K: C3 D3 3 | A software company lets its employees spend some of their working time on their own ideas for new products. | What type of behaviour is the company encouraging? => Intrapreneurship. || State two benefits to the company. => New products and processes; keeps talented employees; stays competitive and innovative (any two).
''', cat='term')

CH02_ST4 = spec('''
T: Motivation | The inner drive that moves a person to act towards a goal.
T: Push factors | Negative conditions, such as unemployment or job dissatisfaction, that force a person to start a business.
T: Pull factors | Attractive conditions, such as an opportunity, independence or high income, that draw a person into entrepreneurship.
T: Business ethics | Moral principles of right and wrong that guide the behaviour of a business.
T: Corporate social responsibility | The obligation of a business to act for the benefit of society beyond earning profit.
L: mot | motivating factors for entrepreneurs | -
- Need for achievement | The desire to accomplish something challenging.
- Desire for independence | Wanting to be one's own boss.
- Financial reward | The hope of earning more than a salary.
- Recognition and social status | Respect gained from success.
- Desire to solve a problem | Wanting to meet a need of society.
- Family background and role models | Inspiration from successful relatives or others.
L: eth | ethical practices an entrepreneur should follow | -
- Honesty with customers | Fair prices, correct weights and no false claims.
- Fair treatment of employees | Fair wages, safe conditions and no discrimination.
- Payment of taxes | Complying with tax and other laws.
- Protection of the environment | Avoiding pollution and waste.
- Fair competition | Not using unfair means against rivals.
- Honouring contracts | Keeping promises made to suppliers and partners.
P: push factors | pull factors
- nature | negative conditions that force a person into business | positive conditions that attract a person into business
- examples | unemployment, job loss, dissatisfaction with a job | an opportunity, independence, high income
- choice | entrepreneurship as a necessity | entrepreneurship as a choice
Q: Is this a push factor or a pull factor? | Push factor; Pull factor; Neither push nor pull factor; Both push and pull factors | -
- {p} lost {his} factory job when the plant closed and started a tea stall to support the family. | Push factor | Unemployment forced {p} into business.
- {p} left a well-paid job because {he} saw a big opportunity in electric-vehicle charging. | Pull factor | An attractive opportunity drew {p} into business.
- {p} started a business because {he} was unhappy with {his} boss and the long hours in the office. | Push factor | Dissatisfaction with the job pushed {p} out.
- {p} started {his} own design studio because {he} wanted to be independent and earn more. | Pull factor | Independence and income attracted {p}.
A: Need for achievement motivates many entrepreneurs. | Entrepreneurs like setting and meeting challenging goals. | a | Both true; R explains A.
A: Ethical behaviour harms a business in the long run. | Honest firms win the trust of customers. | d | A is false: ethics builds trust and long-term success. R is true.
A: Unemployment is a pull factor for entrepreneurship. | It forces people to start businesses for survival. | d | A is false: unemployment is a push factor. R is true.
A: Entrepreneurs should pay taxes honestly. | Payment of taxes is part of ethical conduct and legal compliance. | a | Both true; R explains A.
TT: entrepreneurial motivation and ethics
S+: Unemployment can push a person into entrepreneurship.
S+: An attractive opportunity is a pull factor.
S+: Ethical conduct builds the trust of customers.
S+: Fair treatment of employees is an ethical practice.
S-: Unemployment is a pull factor.
S-: Ethics means earning profit by any means.
S-: Entrepreneurs have no responsibility towards society.
S-: Selling underweight goods is an ethical practice.
K: C4 D4 5 | {p} started a spice-packing business in {c} because {he} wanted independence. {He} pays fair wages, gives correct weights, files taxes on time and has stopped using plastic packets. A rival suggested that {he} mix cheaper powder to raise profits, but {he} refused. | Is {p}'s motivation a push or a pull factor? => Pull factor (desire for independence). || Identify four ethical practices followed by {p}. => Fair treatment of employees; honesty with customers; payment of taxes; protection of the environment; refusing adulteration (any four).
K: C3 D3 3 | A shopkeeper in {c} sells fake branded shoes at full price. | Which ethical principle is violated? => Honesty with customers (no false claims). || Give two harms this can cause to the business. => Loss of customer trust and reputation; legal action and penalties; loss of future sales (any two).
''', cat='term')

# ================================================================ ch03 st1 entrepreneurial journey

CH03_ST1 = spec('''
T: Entrepreneurial journey | The path from the first idea to a running and growing enterprise.
T: Self-discovery | Understanding one's own interests, skills and values before choosing a business.
T: Feasibility study | An analysis of whether an idea is technically, financially and commercially workable.
T: Launch | The start of commercial operations of a new venture.
T: Scaling up | Growing the size of operations, markets or products of the enterprise.
L: st | stages of the entrepreneurial journey | -
- Self-discovery | Knowing one's interests, strengths and goals.
- Identifying opportunities | Spotting unmet needs and problems in the market.
- Generating and selecting ideas | Producing many ideas and choosing the best after a feasibility study.
- Preparing a business plan | Writing down the goals, market, operations and finances of the venture.
- Mobilising resources | Arranging money, people, materials and permissions.
- Launching the enterprise | Starting operations and selling to customers.
- Growth and scaling up | Expanding operations, markets or products.
L: ch | challenges faced in the entrepreneurial journey | -
- Arranging finance | Raising money without a track record.
- Finding customers | Convincing people to try a new product.
- Competition | Rivals may react with lower prices or better products.
- Hiring the right people | Small firms find it hard to attract skilled staff.
- Uncertainty and failure | Ventures may fail; the entrepreneur must learn and adapt.
Q: Which stage of the entrepreneurial journey is shown? | Self-discovery; Identifying opportunities; Generating and selecting ideas; Preparing a business plan; Mobilising resources; Launching the enterprise; Growth and scaling up | -
- {p} took an aptitude test and listed {his} strengths and interests to decide what kind of business suits {him}. | Self-discovery | {p} is trying to understand {his} own interests and strengths.
- {p} noticed that people in {his} colony had no place to get their phones repaired. | Identifying opportunities | An unmet need is being spotted.
- {p} wrote a document describing {his} target customers, production method and projected profits. | Preparing a business plan | The plan of the venture is written down.
- {p} arranged a bank loan, hired two workers and obtained a trade licence. | Mobilising resources | Money, people and permissions are being arranged.
- {p} opened the doors of {his} bakery to customers for the first time. | Launching the enterprise | Operations have started.
- After three successful years, {p} opened branches in two more cities. | Growth and scaling up | The venture is expanding.
- {p} listed twenty ideas and then studied which three were workable. | Generating and selecting ideas | Ideas are generated and screened.
A: Self-discovery is the first step of the entrepreneurial journey. | Knowing one's strengths and interests helps in choosing a suitable venture. | a | Both true; R explains A.
A: A business plan is prepared after the launch. | The business plan guides the setting up of the venture. | d | A is false: the plan is prepared before the launch. R is true.
A: A feasibility study helps in selecting an idea. | It checks whether the idea is technically, financially and commercially workable. | a | Both true; R explains A.
A: Scaling up is a stage of the entrepreneurial journey. | A successful venture expands its operations and markets. | a | Both true; R explains A.
TT: the entrepreneurial journey
S+: Self-discovery comes before choosing a business.
S+: A feasibility study is used to select an idea.
S+: Resources are mobilised before the launch.
S+: Scaling up means expanding the venture.
S-: The business plan is written after the venture has grown.
S-: An entrepreneur needs no resources to launch a venture.
S-: The journey ends at the idea stage.
S-: Every idea is launched without any study.
K: C4 D4 5 | {p} loved cooking and was good with people. {He} noticed that office workers in {c} wanted home-style lunches. After comparing three ideas, {he} chose a tiffin service, wrote a plan, borrowed ₹2 lakh, hired two cooks and began deliveries in June. A year later {he} expanded to two more areas. | Identify the stages of the entrepreneurial journey in the case, in order. => Self-discovery (loved cooking, good with people); identifying opportunities (office workers' need); generating and selecting ideas (compared three ideas); preparing a business plan; mobilising resources (loan, cooks); launching (deliveries in June); growth and scaling up (two more areas).
K: C3 D3 3 | {p} has just launched a mobile repair shop in {c}. | State three challenges {he} may face in the coming months. => Finding customers; competition; arranging finance; hiring skilled staff; uncertainty (any three).
''', cat='term')

# ================================================================ ch04 Entrepreneurship as innovation and problem solving

CH04_ST1 = spec('''
T: Creativity | The ability to produce new and useful ideas.
T: Innovation | Turning a creative idea into a product, service or process that is used in practice.
T: Incremental innovation | A small improvement to an existing product or process.
T: Radical innovation | A major change that creates a completely new product or industry.
T: Process innovation | A new or improved method of producing or delivering a product.
T: Incubation | The stage of creativity in which the mind works on a problem unconsciously after preparation.
L: proc | stages of the creative process | -
- Preparation | Collecting information and studying the problem.
- Incubation | Letting the mind work on the problem unconsciously.
- Illumination | The moment when the idea suddenly appears.
- Verification | Testing and refining the idea to see if it works.
L: types | types of innovation | -
- Product innovation | A new or improved product.
- Process innovation | A new or improved way of producing or delivering.
- Marketing innovation | A new method of packaging, pricing, promotion or distribution.
- Organisational innovation | A new way of organising work or relations with others.
- Incremental innovation | Small improvements to existing offerings.
- Radical innovation | A major change that creates a new market or industry.
P: creativity | innovation
- meaning | producing new ideas | putting new ideas into practical use
- result | an idea | a product, process or service
- stage | comes first | follows creativity
Q: Which type of innovation is shown? | Product innovation; Process innovation; Marketing innovation; Organisational innovation; Radical innovation | -
- {f} began selling its pickles in single-use sachets at ₹5 each. | Marketing innovation | It is a new method of packaging and pricing.
- {f} started using robots to pack its biscuits, cutting time by half. | Process innovation | It is a new method of production.
- {p} launched a school bag that turns into a desk. | Product innovation | A new product was introduced.
- {f} let its workers form small teams that decide their own schedules. | Organisational innovation | It is a new way of organising work.
- The first mobile phone replaced the need for a fixed landline for millions of people. | Radical innovation | It created a completely new market.
A: Innovation follows creativity. | An idea must first be produced before it can be put to use. | a | Both true; R explains A.
A: All innovations are radical. | Small improvements are also innovations. | d | A is false: innovations may be incremental. R is true.
A: Incubation is a stage of the creative process. | After preparation the mind keeps working on the problem unconsciously. | a | Both true; R explains A.
A: Creativity alone is enough for business success. | An idea must be turned into a usable product or process. | d | A is false: creativity must be followed by innovation. R is true.
TT: creativity and innovation
S+: Creativity is the production of new ideas.
S+: Innovation puts new ideas to practical use.
S+: Preparation is the first stage of the creative process.
S+: A small improvement is an incremental innovation.
S-: Innovation comes before creativity.
S-: Only inventions of new machines count as innovation.
S-: Verification is the first stage of the creative process.
S-: Process innovation means a new advertisement.
K: C4 D4 5 | {p} kept reading about farmers who lose crops for lack of cold storage. After weeks of study, the idea of a solar-powered cold box came to {him} suddenly one morning. {He} built a model, tested it on two farms and improved it. Later {he} sold the boxes on rent to farmers at ₹50 a day. | Identify the stages of the creative process in the case. => Preparation (reading and study); incubation (weeks of working on it); illumination (idea came suddenly); verification (built a model, tested and improved). || Identify one product and one marketing innovation. => Product – solar-powered cold box; marketing – renting the boxes at ₹50 a day.
K: C3 D3 3 | A bakery in {c} began using a new oven that bakes twice as fast and also started selling cakes in jars. | Identify two types of innovation. => Process innovation (faster oven); product or marketing innovation (cakes in jars). || Distinguish creativity from innovation. => Creativity produces new ideas; innovation puts them into practical use.
''', cat='term')

CH04_ST2 = spec('''
T: Design thinking | A human-centred approach to problem solving that starts from the needs of users and moves through empathy, definition, ideas, prototypes and tests.
T: Empathy | Understanding the feelings, needs and problems of users from their point of view.
T: Problem statement | A clear description of the user's problem that the solution must address.
T: Prototype | A simple, early model of a solution used to test ideas quickly and cheaply.
T: Ideation | Generating many possible solutions to the defined problem.
T: User | The person who will use the product or service and whose needs are the focus of design thinking.
L: st | stages of design thinking | -
- Empathise | Observe and talk to users to understand their needs and feelings.
- Define | State the core problem clearly from the user's point of view.
- Ideate | Generate many possible solutions without judging them.
- Prototype | Build simple, low-cost models of the best ideas.
- Test | Try the prototypes with users and improve them using feedback.
L: ben | benefits of design thinking for an entrepreneur | -
- Focus on real needs | Solutions are based on what users actually need.
- Lower cost of failure | Cheap prototypes reveal problems early.
- Encourages creativity | Many ideas are explored before choosing.
- Better customer acceptance | Users help shape the product.
- Continuous improvement | Testing and feedback keep improving the solution.
Q: Which stage of design thinking is shown? | Empathise; Define; Ideate; Prototype; Test | -
- {p} spent a week with elderly people in {c} watching how they struggle to open medicine bottles. | Empathise | {p} is understanding users' needs by observing them.
- {p} wrote: "Elderly users with weak grip need a way to open medicine bottles without twisting." | Define | The core problem is stated clearly from the user's view.
- {p}'s team listed thirty ways to open bottles, without rejecting any. | Ideate | Many possible solutions are generated.
- {p} made a cardboard and rubber model of a push-to-open cap. | Prototype | A simple, low-cost model was built.
- {p} gave the model caps to twenty elderly users and changed the design after hearing their comments. | Test | The prototype is tried with users and improved.
A: Design thinking begins with empathy. | It focuses on understanding the needs of users. | a | Both true; R explains A.
A: Prototypes should be expensive and final. | Prototypes are early models used to test ideas. | d | A is false: prototypes are simple and low-cost. R is true.
A: Ideas are judged strictly during ideation. | Ideation aims to generate as many ideas as possible. | d | A is false: ideas are not judged during ideation. R is true.
A: Testing is part of design thinking. | Feedback from users helps to improve the solution. | a | Both true; R explains A.
TT: design thinking
S+: Design thinking is human-centred.
S+: Empathise is the first stage of design thinking.
S+: A prototype is a simple, early model.
S+: Testing gives feedback from users.
S-: Design thinking ignores the needs of users.
S-: A prototype must be the final product.
S-: The problem is defined after the product is sold.
S-: Ideation means choosing only one idea immediately.
K: C4 D4 5 | Students in {c} wanted to help street vendors who lose vegetables in the heat. They spent days with vendors, wrote down the problem as "vendors need a cheap way to keep vegetables fresh for a day without electricity", listed many ideas, built a clay-and-sand cooling box from waste material and tried it with five vendors, who suggested a larger lid. | Identify the five stages of design thinking in the case. => Empathise (spent days with vendors); define (wrote the problem statement); ideate (listed many ideas); prototype (built the clay-and-sand box); test (tried with five vendors and got feedback). || Why is the problem statement important? => It keeps the solution focused on the user's real need.
K: C3 D3 3 | {p} wants to design a better school bag for young children. | Explain how {he} can apply the empathise and test stages. => Empathise: observe and talk to children and parents about weight and comfort; test: give prototypes to children and improve using their feedback. || Why should {he} build a cheap prototype first? => To find problems early at low cost.
''', cat='term')

CH04_ST3 = spec('''
T: Social entrepreneurship | Using entrepreneurial methods to solve social problems in a financially sustainable way.
T: Frugal innovation | Developing good-quality products at very low cost by reducing complexity and using resources sparingly.
T: Jugaad | An Indian term for a clever, low-cost improvised solution to a problem.
T: Social impact | The positive change a venture brings to the lives of people or the environment.
T: Self-help group | A small group of people, often women, who save together and take up activities for mutual benefit.
L: feat | features of social entrepreneurship | -
- Social mission | The main aim is solving a social or environmental problem.
- Financial sustainability | The venture earns revenue to keep running.
- Innovation | It uses new and low-cost solutions.
- Measured by social impact | Success is judged by change in people's lives, not only by profit.
- Community participation | It involves the people it serves.
L: frug | features of frugal innovation | -
- Low cost | Products are affordable for low-income users.
- Simplicity | Only essential features are kept.
- Use of local resources | Locally available material and skills are used.
- Robustness | Products work in difficult conditions.
- Scalability | Solutions can reach large numbers of people.
P: social entrepreneur | business entrepreneur
- main aim | solving a social problem | earning profit
- measure of success | social impact | profit and growth
- use of surplus | reinvested in the social mission | distributed to owners or reinvested for growth
Q: Is this mainly an example of social entrepreneurship or frugal innovation? | Social entrepreneurship; Frugal innovation; Neither of these; Corporate social responsibility | -
- {p} designed a clay refrigerator that keeps food cool without electricity and sells it for a low price. | Frugal innovation | A low-cost, simple product using local material.
- {p} runs a venture that trains rural women to make sanitary pads and sell them at low prices in villages. | Social entrepreneurship | The main aim is a social problem, run sustainably.
- {p} made a low-cost water filter from sand, gravel and charcoal for villages. | Frugal innovation | A simple, low-cost product using local material.
- {p} started a firm that hires and trains former prisoners and sells their furniture. | Social entrepreneurship | It solves a social problem in a sustainable way.
A: Social enterprises aim to be financially sustainable. | They earn revenue so that they do not depend only on donations. | a | Both true; R explains A.
A: Frugal innovation means poor quality. | Frugal innovation keeps essential features at low cost. | d | A is false: it aims at good quality at low cost. R is true.
A: The success of a social enterprise is judged by social impact. | Its main aim is to solve a social problem. | a | Both true; R explains A.
A: Jugaad is an example of frugal problem solving. | It is a clever, low-cost improvised solution. | a | Both true; R explains A.
TT: social entrepreneurship and frugal innovation
S+: A social enterprise has a social mission.
S+: Frugal innovation reduces cost and complexity.
S+: Jugaad means a low-cost improvised solution.
S+: Social enterprises try to be financially sustainable.
S-: Social enterprises never earn revenue.
S-: Frugal innovation always means expensive products.
S-: Social impact is not important for a social enterprise.
S-: Frugal products must have as many features as possible.
K: C4 D4 5 | {p} saw that farmers in {his} district could not afford tractors. {He} fitted a motorcycle engine to a small plough, selling it at one-tenth the price of a tractor. {He} also trains village youths to repair it and reinvests most of {his} surplus in training more youths. | Identify the frugal features of the product. => Low cost; simplicity (only essential features); use of locally available parts; robustness for village use. || Is {p} a social entrepreneur? Give two reasons. => Yes: main aim is helping poor farmers and youths; surplus reinvested in the mission; success measured by social impact.
K: C3 D3 3 | A group of women in {c} make low-cost school uniforms and use the earnings to run a crèche for working mothers. | Identify the type of entrepreneurship. => Social entrepreneurship. || State two features shown. => Social mission; financial sustainability; community participation (any two).
''', cat='term')

CH04_ST4 = spec('''
T: Intellectual property | Creations of the mind, such as inventions, works of art and literature, symbols and designs, protected by law.
T: Patent | An exclusive right granted for an invention that is new, involves an inventive step and is capable of industrial application.
T: Copyright | The exclusive right of the creator of an original literary, dramatic, musical or artistic work, film or sound recording, including software.
T: Trademark | A word, name, symbol, logo or combination that distinguishes the goods or services of one business from those of others.
T: Geographical indication | A sign used on products that have a specific geographical origin and qualities or a reputation due to that origin, such as Darjeeling tea.
T: Industrial design | The shape, pattern or ornamentation applied to an article that appeals to the eye.
L: ipr | types of intellectual property rights | -
- Patent | Protects inventions; in India the term is 20 years from the date of filing.
- Copyright | Protects original creative works, including software.
- Trademark | Protects brand names and logos; registration lasts 10 years and can be renewed.
- Industrial design | Protects the appearance of a product.
- Geographical indication | Protects products linked to a place, such as Darjeeling tea.
L: ben | benefits of intellectual property rights to an entrepreneur | -
- Protection from copying | Rivals cannot legally copy the invention or brand.
- Exclusive use | The owner alone can use or sell the protected creation.
- Source of income | IP can be licensed or sold for royalty.
- Builds brand value | A protected trademark builds customer recognition.
- Attracts investors | Investors value ventures with protected technology or brands.
P: patent | copyright
- protects | inventions | original literary, artistic, musical and similar works
- need for registration | must be applied for and granted | exists from creation; registration is optional
- Indian law | Patents Act, 1970 | Copyright Act, 1957
Q: Which type of intellectual property right is the most suitable? | Patent; Copyright; Trademark; Industrial design; Geographical indication | -
- {p} has invented a new machine that peels coconuts automatically. | Patent | It is a new invention capable of industrial application.
- {p} has written a cookbook and wants to stop others from printing copies. | Copyright | It protects original literary works.
- {f} wants to stop others from using its brand name and logo. | Trademark | It protects names and logos that distinguish goods.
- {p} designed a uniquely shaped perfume bottle and wants to protect its look. | Industrial design | It protects the appearance of a product.
- Weavers of a region want to protect the name of a saree made only in their area. | Geographical indication | It protects products linked to a place.
- {p} wrote software for billing in shops. | Copyright | Computer programs are protected as literary works.
A: A patent gives its owner exclusive rights for a limited period. | In India a patent lasts 20 years from the date of filing. | a | Both true; R explains A.
A: Copyright protects ideas themselves. | Copyright protects the expression of ideas in original works. | d | A is false: copyright protects the expression, not the idea. R is true.
A: A trademark registration in India can be renewed. | A trademark registration lasts 10 years at a time. | a | Both true; R explains A.
A: Darjeeling tea is protected as a geographical indication. | Its qualities and reputation are due to its place of origin. | a | Both true; R explains A.
TT: intellectual property rights
S+: A patent protects an invention.
S+: Computer software is protected by copyright.
S+: A trademark distinguishes the goods of one business from others.
S+: Darjeeling tea is a registered geographical indication.
S-: A patent in India lasts for ever.
S-: A trademark protects new inventions.
S-: Copyright protects only machines.
S-: A geographical indication protects a company's logo.
K: C4 D4 5 | {p} of {c} invented a low-cost solar dryer for fruits, wrote a training manual for farmers on using it, and sells the dryer under the brand name 'SunDry' with a distinctive orange logo. | Name the intellectual property rights {p} should obtain for each, with a reason. => Patent for the dryer (new invention); copyright for the manual (original literary work); trademark for 'SunDry' and the logo (distinguishes the goods). || State two benefits of IPR to {p}. => Protection from copying; exclusive use; licensing income; brand value; attracts investors (any two).
K: C3 D3 3 | A rival firm in {c} started selling dryers with a logo almost identical to {f}'s registered logo. | Which right has been violated? => Trademark. || Under which Act is it protected in India? => Trade Marks Act, 1999. || How long does a registration last? => 10 years, renewable.
''', cat='term')

THEORY = {
    '01-st1': CH01_ST1, '01-st2': CH01_ST2, '01-st3': CH01_ST3, '01-st4': CH01_ST4,
    '02-st1': CH02_ST1, '02-st2': CH02_ST2, '02-st3': CH02_ST3, '02-st4': CH02_ST4,
    '03-st1': CH03_ST1,
    '04-st1': CH04_ST1, '04-st2': CH04_ST2, '04-st3': CH04_ST3, '04-st4': CH04_ST4,
}
FAMILIES = {S + k: efacts(v) for k, v in THEORY.items()}
