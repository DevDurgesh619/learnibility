"""CBSE class 10 social science fact tables: Economics (Understanding Economic Development), chapters 18-22,
with computed items (average income, per capita income, literacy rate, GDP and value added, sector shares,
bank lending, cost of credit, import duty and consumer commission jurisdiction)."""
from qbank import name, inr, num

STATES = ['State A', 'State B', 'State C']


def _distinct(ans, ds):
    if len({str(x) for x in [ans] + list(ds)}) != len(ds) + 1:
        raise ValueError('repeated option')
    return ds


# ---------------- ch18 computed items
def average_income(r):
    while True:
        avg = r.randrange(8, 20) * 1000
        a = [avg + d for d in r.sample(range(-3000, 3001, 500), 5)]
        if sum(a) == 5 * avg and len(set(a)) == 5:
            break
    small = sorted(r.sample(range(500, 2001, 500), 4))
    b = small + [5 * avg - sum(small)]
    sa, sb = ', '.join(inr(x) for x in a), ', '.join(inr(x) for x in b)
    return {'stem': (f'Country P has five citizens with monthly incomes {sa}. Country Q also has five citizens with monthly incomes {sb}. '
                     f'Find the average income of each country. In which country would you prefer to live, and why?'),
            'answer': f'Both have an average of {inr(avg)}; Country P, because income is more equally distributed',
            'key': (f'Average P = {inr(sum(a))} ÷ 5 = {inr(avg)}; average Q = {inr(sum(b))} ÷ 5 = {inr(avg)} (1 mark each). '
                    f'Averages are equal, but in Q one person earns most of the income while four are very poor, so P is preferable (1 mark). '
                    f'Averages hide disparities.'),
            'marks': 3, 'minutes': 5}


def per_capita(r):
    pop = r.randrange(2, 12) * 10        # lakh people
    pci = r.randrange(60, 250) * 1000
    tot = pop * pci                       # in lakh rupees
    st = r.choice(STATES)
    crore = tot / 100
    return {'stem': f'{st} has a population of {pop} lakh and a total annual income of {inr(crore)} crore. What is its per capita income?',
            'answer': inr(pci),
            'key': f'Per capita income = total income ÷ population = {inr(crore)} crore ÷ {pop} lakh = {inr(pci)} per year.',
            'distractors': [inr(pci * 10), inr(pci // 10), inr(pci * 2)]}


def literacy_rate(r):
    pop7 = r.randrange(20, 90) * 1000
    pct = r.randrange(55, 96)
    lit = pop7 * pct // 100
    pct_exact = lit * 100 / pop7
    if abs(pct_exact - pct) > 1e-9:
        raise ValueError
    st = r.choice(['a district', 'a town', 'a block'])
    return {'stem': f'In {st}, {lit:,} people out of {pop7:,} people aged 7 years and above can read and write. What is the literacy rate?',
            'answer': f'{pct} per cent',
            'key': f'Literacy rate = literate population aged 7 and above ÷ total population aged 7 and above × 100 = {lit} ÷ {pop7} × 100 = {pct} per cent.',
            'distractors': _distinct(f'{pct} per cent', [f'{100 - pct} per cent', f'{min(pct + 7, 99)} per cent', f'{pct - 9} per cent'])}


def bmi(r):
    who = name(r)
    h = r.choice([1.5, 1.6, 1.7, 1.8])
    b = r.choice([16.0, 18.0, 20.0, 22.0, 24.0, 26.0])
    w = round(b * h * h, 2)
    if w != round(w, 1):
        raise ValueError
    status = 'undernourished' if b < 18.5 else ('normal' if b <= 25 else 'overweight')
    return {'stem': f'{who} weighs {num(w, 1)} kg and is {num(h)} m tall. Calculate the Body Mass Index (BMI) and state whether {who} is undernourished, normal or overweight (BMI below 18.5 is undernourished, above 25 is overweight).',
            'answer': f'BMI = {num(b, 1)}; {status}',
            'key': f'BMI = weight in kg ÷ (height in m)² = {num(w, 1)} ÷ {num(h)}² = {num(w, 1)} ÷ {num(h * h, 2)} = {num(b, 1)} (1 mark); {status} (1 mark).',
            'marks': 2, 'minutes': 3}


# ---------------- ch19 computed items
def gdp_final(r):
    wheat = r.randrange(5, 15) * 100
    flour = wheat + r.randrange(2, 8) * 100
    bisc = flour + r.randrange(5, 15) * 100
    who = name(r)
    return {'stem': (f'{who}, a farmer, sells wheat worth {inr(wheat)} to a flour mill. The mill sells the flour to a biscuit company for {inr(flour)}. '
                     f'The company sells biscuits to consumers for {inr(bisc)}. What is the contribution of these transactions to GDP? Why are the earlier values not added?'),
            'answer': f'{inr(bisc)}; adding wheat and flour would be double counting since they are intermediate goods',
            'key': (f'Only the value of the final good counts: {inr(bisc)} (1 mark). Value added: {inr(wheat)} + {inr(flour - wheat)} + {inr(bisc - flour)} = {inr(bisc)} (1 mark). '
                    f'Adding {inr(wheat)} + {inr(flour)} + {inr(bisc)} = {inr(wheat + flour + bisc)} would count wheat and flour more than once (1 mark).'),
            'marks': 3, 'minutes': 5}


def gdp_mcq(r):
    a = r.randrange(5, 15) * 100
    b = a + r.randrange(2, 8) * 100
    c = b + r.randrange(5, 15) * 100
    return {'stem': f'Cotton worth {inr(a)} is made into yarn worth {inr(b)}, which is woven into cloth sold to consumers for {inr(c)}. What value is counted in GDP?',
            'answer': inr(c),
            'key': f'GDP counts only final goods: the cloth worth {inr(c)}. Cotton and yarn are intermediate goods.',
            'distractors': _distinct(inr(c), [inr(a + b + c), inr(a + b), inr(c - b)])}


def sector_share(r):
    p = r.randrange(15, 30)
    s = r.randrange(20, 35)
    t = 100 - p - s
    gdp = r.randrange(20, 60) * 100
    vals = [gdp * x // 100 for x in (p, s, t)]
    if sum(vals) != gdp or any(gdp * x % 100 for x in (p, s, t)):
        raise ValueError
    return {'stem': (f'In a year, a country produced goods and services worth: primary sector ₹{vals[0]:,} crore, secondary sector ₹{vals[1]:,} crore and tertiary sector ₹{vals[2]:,} crore. '
                     f'What is the share of the tertiary sector in GDP?'),
            'answer': f'{t} per cent',
            'key': f'GDP = {vals[0]} + {vals[1]} + {vals[2]} = ₹{gdp:,} crore; tertiary share = {vals[2]} ÷ {gdp} × 100 = {t} per cent.',
            'distractors': _distinct(f'{t} per cent', [f'{p} per cent', f'{s} per cent', f'{p + s} per cent'])}


# ---------------- ch20 computed items
def bank_lending(r):
    dep = r.randrange(10, 90) * 100
    keep = 15
    cash = dep * keep // 100
    if dep * keep % 100:
        raise ValueError
    return {'stem': f'A bank receives deposits of ₹{dep:,} crore. If it keeps about 15 per cent of its deposits as cash to meet withdrawals, how much can it use to extend loans?',
            'answer': f'₹{dep - cash:,} crore',
            'key': f'Cash kept = 15 per cent of {dep} = ₹{cash:,} crore; amount available for loans = {dep} − {cash} = ₹{dep - cash:,} crore.',
            'distractors': [f'₹{cash:,} crore', f'₹{dep:,} crore', f'₹{dep + cash:,} crore']}


def credit_cost(r):
    who = name(r)
    p = r.randrange(20, 100) * 1000
    bank = r.choice([8, 9, 10, 12])
    lender = r.choice([24, 30, 36, 48])
    t = r.choice([1, 2])
    ib, il = p * bank * t // 100, p * lender * t // 100
    yrs = f'{t} year{"s" if t > 1 else ""}'
    return {'stem': (f'{who}, a small farmer, needs {inr(p)} for {yrs}. A cooperative bank charges {bank} per cent simple interest per year but needs land papers as collateral; '
                     f'a moneylender charges {lender} per cent and asks for no collateral. Calculate the interest in each case and explain how the moneylender\'s loan can push {who} into a debt trap.'),
            'answer': f'Bank interest {inr(ib)}; moneylender interest {inr(il)}; the higher interest eats up income and may force fresh borrowing to repay',
            'key': (f'Bank: {inr(p)} × {bank} × {t} ÷ 100 = {inr(ib)} (1 mark); moneylender: {inr(p)} × {lender} × {t} ÷ 100 = {inr(il)} (1 mark). '
                    f'If the crop fails, {who} must repay {inr(p + il)}, may sell land or borrow again – a debt trap (1 mark).'),
            'marks': 3, 'minutes': 5}


# ---------------- ch21 computed items
def import_duty(r):
    price = r.randrange(200, 900, 50)
    duty = r.choice([10, 20, 25, 40, 50])
    local = price + r.randrange(-100, 101, 50)
    after = price * (100 + duty) // 100
    if price * duty % 100:
        raise ValueError
    cheaper = 'imported toy' if after < local else 'Indian toy'
    if after == local:
        raise ValueError
    return {'stem': (f'An imported toy costs {inr(price)} before tax. The government puts an import duty of {duty} per cent on it. A similar Indian toy costs {inr(local)}. '
                     f'What is the price of the imported toy after the duty, and which toy is cheaper for the buyer?'),
            'answer': f'{inr(after)}; the {cheaper} is cheaper',
            'key': f'Price after duty = {inr(price)} + {duty} per cent of {inr(price)} = {inr(after)} (1 mark). Compare with {inr(local)}: the {cheaper} is cheaper (1 mark). An import duty is a trade barrier that protects local producers.',
            'marks': 2, 'minutes': 3}


# ---------------- ch22 computed items
def commission(r):
    lakh = r.choice([r.randrange(5, 95), r.randrange(150, 950, 50), r.randrange(1200, 5000, 100)])
    amt = f'₹{num(lakh / 100)} crore' if lakh >= 100 else f'₹{lakh} lakh'
    if lakh <= 100:
        ans, why = 'the District Commission', 'claims up to ₹1 crore'
    elif lakh <= 1000:
        ans, why = 'the State Commission', 'claims between ₹1 crore and ₹10 crore'
    else:
        ans, why = 'the National Commission', 'claims above ₹10 crore'
    opts = ['the District Commission', 'the State Commission', 'the National Commission', 'the Supreme Court directly']
    who = name(r)
    return {'stem': f'Under the Consumer Protection Act, 2019, {who} wants to claim compensation of {amt} for a defective product. Where should the complaint be filed?',
            'answer': ans,
            'key': f'The District Commission hears claims up to ₹1 crore, the State Commission ₹1 crore to ₹10 crore and the National Commission above ₹10 crore; {amt} falls in {why}.',
            'distractors': [o for o in opts if o != ans]}


DATA = {
    # ---------------- ch18 Development
    '18-st1': dict(
        T=[('development', 'the process of improvement in people\'s lives, including income, equality, freedom, security and respect'),
           ('developmental goals', 'the aspirations that different people have for a better life, such as more income, equal treatment and freedom'),
           ('national development', 'the improvement of the country as a whole, considering what is fair and just for all'),
           ('conflicting goals', 'goals of one group that clash with what another group wants'),
           ('non-material things', 'things such as equal treatment, freedom, security and respect that cannot be easily measured but matter for development')],
        FB=[('What may be development for one may not be development for another; it may even be ___ for the other.', 'destructive', ['helpful', 'neutral', 'profitable']),
            ('Different persons can have different as well as ___ notions of a country\'s development.', 'conflicting', ['identical', 'permanent', 'fixed']),
            ('Besides income, people also seek things like equal treatment, freedom, security and ___.', 'respect from others', ['higher taxes', 'more pollution', 'fewer rights']),
            ('A dam may give electricity to industrialists but may ___ the land of people living there.', 'submerge', ['enrich', 'irrigate', 'level'])],
        EX=[('C2', 'D2', 'Why do different people have different developmental goals?', ['people come from different backgrounds and situations', 'they seek things that are most important to them, such as income for the poor or a pollution-free environment for others']),
            ('C2', 'D3', 'Why is income not the only goal that people seek?', ['people also want equal treatment, freedom, security and respect', 'many important things in life cannot be bought with money']),
            ('C3', 'D3', 'Give three examples of conflicting developmental goals.', ['industrialists want more electricity from dams, but people displaced by them do not', 'farmers want higher prices for crops, consumers want lower prices', 'factory owners want cheap labour, workers want higher wages']),
            ('C4', 'D4', '"Development for some may be destructive for others." Examine with examples.', ['a dam may provide power and irrigation but displace tribal people', 'mining may bring income but destroy forests and livelihoods', 'a new road may help traders but cut through farmland', 'development must consider what is fair and just for all'])],
        AR=[('People living in a river valley may oppose a big dam.', 'A big dam may submerge their land and disrupt their lives.', 'a', 'R explains A.')],
        SC=[('A rural girl wants as much freedom as her brother and does not want to be forced into marriage. What kind of developmental goal is this?', 'A non-material goal such as equality and freedom',
             ['A goal of higher income only', 'A goal of more consumer goods', 'A goal of industrial growth'], 'Freedom and equal treatment are non-material goals of development.')],
    ),
    '18-st2': dict(
        T=[('per capita income', 'the total income of a country divided by its total population; also called average income'),
           ('World Development Report', 'the report brought out by the World Bank that classifies countries by per capita income'),
           ('infant mortality rate', 'the number of children who die before the age of one year as a proportion of 1,000 live children born in that year'),
           ('literacy rate', 'the proportion of literate population in the 7 years and above age group'),
           ('net attendance ratio', 'the total number of children aged 14 and 15 attending school as a percentage of all children in that age group'),
           ('Body Mass Index', 'a measure of nourishment found by dividing weight in kg by the square of height in metres')],
        FB=[('The World Bank uses ___ as the main criterion for classifying countries.', 'per capita income', ['literacy rate', 'life expectancy', 'population']),
            ('Kerala has a lower infant mortality rate than many richer states because of adequate provision of basic health and ___ facilities.', 'educational', ['transport', 'banking', 'mining']),
            ('Per capita income is also called ___ income.', 'average', ['total', 'national', 'gross']),
            ('Per capita income does not tell us how income is ___ among people.', 'distributed', ['produced', 'taxed', 'measured'])],
        EX=[('C2', 'D2', 'Why is average income a useful but limited criterion of development?', ['it allows comparison between countries with different populations', 'it hides disparities, as it does not tell how income is distributed']),
            ('C2', 'D3', 'Why does Kerala have a lower infant mortality rate than Haryana despite lower per capita income?', ['Kerala has adequate provision of basic health facilities', 'it also has good educational facilities, so people are more aware']),
            ('C3', 'D3', 'Describe three indicators other than income used to compare development.', ['infant mortality rate', 'literacy rate', 'net attendance ratio', 'life expectancy at birth']),
            ('C4', 'D4', 'Evaluate per capita income as a measure of development.', ['it is easy to calculate and compare', 'it hides inequality among people', 'it does not measure health, education and freedom', 'so other indicators such as IMR, literacy and HDI are needed'])],
        AR=[('Average income is a useful measure for comparing countries.', 'Countries have different populations, so total income alone is misleading.', 'a', 'R explains A.'),
            ('A higher per capita income always means a lower infant mortality rate.', 'Infant mortality rate measures children dying before the age of one.', 'd', 'A is false – Kerala has lower income than Haryana but a lower IMR; R is true.')],
        GEN=[('C3', 'D3', 'multi_step', average_income, {'kinds': ('sa3',)}), ('C3', 'D2', 'mcq', per_capita), ('C3', 'D2', 'mcq', literacy_rate),
             ('C3', 'D3', 'numerical', bmi, {'kinds': ('sa2',)})],
    ),
    '18-st3': dict(
        T=[('public facilities', 'facilities such as health care, education, clean water and public distribution, best provided collectively by the government'),
           ('Human Development Index', 'the index published by the UNDP that combines life expectancy, education and per capita income'),
           ('sustainable development', 'development that meets present needs without harming the ability of future generations to meet theirs'),
           ('public distribution system', 'the system through which ration shops sell food grains to people at low prices'),
           ('Human Development Report', 'the report published by the UNDP that compares countries on educational levels, health status and per capita income')],
        FB=[('The Human Development Report is published by the ___.', 'UNDP', ['World Bank', 'IMF', 'WTO']),
            ('The HDI combines life expectancy, education and ___.', 'per capita income', ['military strength', 'population size', 'land area']),
            ('Ground water in many parts of India is being ___ faster than it is being replenished.', 'overused', ['recharged', 'saved', 'purified']),
            ('Crude oil reserves will last only a limited number of years, so it is a ___ resource.', 'non-renewable', ['renewable', 'inexhaustible', 'biotic'])],
        EX=[('C2', 'D2', 'Why are public facilities important for development?', ['many things such as health and education cannot be bought by individuals at low cost', 'it is cheaper and better to provide them collectively']),
            ('C2', 'D3', 'Why is sustainability of development important?', ['resources such as ground water and crude oil are being overused', 'future generations must also be able to meet their needs']),
            ('C3', 'D3', 'Describe three components of the Human Development Index.', ['life expectancy at birth', 'education – mean and expected years of schooling', 'per capita income']),
            ('C4', 'D4', 'Explain why development must be sustainable, with examples from India.', ['ground water is being overused in many parts of India', 'crude oil reserves are limited', 'environmental degradation crosses state and national boundaries', 'present development should not harm future generations'])],
        AR=[('The HDI is a better measure of development than per capita income alone.', 'It includes health and education along with income.', 'a', 'R explains A.')],
        CASE=[('Read the source and answer the questions.',
               'A comparison of two states showed that the one with lower per capita income had a much lower infant mortality rate and a higher literacy rate. Its people could buy less, but their children were healthier and more of them went to school, because the state government provided basic health and educational facilities widely.',
               [('Which indicator measures the number of children dying before the age of one?', 'Infant mortality rate.', 1),
                ('Why is income alone not enough to measure development?', 'It does not show health, education and the provision of public facilities.', 1),
                ('Give two public facilities that improve human development.', 'Health care, schools, clean drinking water, public distribution system.', 2)])],
    ),
    # ---------------- ch19 Sectors of the Indian Economy
    '19-st1': dict(
        T=[('primary sector', 'the sector that produces goods by exploiting natural resources, such as agriculture, dairy, fishing and forestry'),
           ('secondary sector', 'the sector in which natural products are changed into other forms through manufacturing'),
           ('tertiary sector', 'the sector of activities that help the development of primary and secondary sectors, such as transport, banking and trade'),
           ('service sector', 'another name for the tertiary sector, since it produces services rather than goods'),
           ('industrial sector', 'another name for the secondary sector')],
        FB=[('The primary sector is also called the agriculture and ___ sector.', 'related', ['service', 'industrial', 'organised']),
            ('Making sugar from sugarcane is an activity of the ___ sector.', 'secondary', ['primary', 'tertiary', 'public']),
            ('Transport, storage, communication and banking are activities of the ___ sector.', 'tertiary', ['primary', 'secondary', 'unorganised']),
            ('Fishing and forestry belong to the ___ sector.', 'primary', ['secondary', 'tertiary', 'service'])],
        EX=[('C2', 'D2', 'Why is the tertiary sector also called the service sector?', ['its activities do not produce a good themselves', 'they are aids or supports for the production process']),
            ('C2', 'D3', 'Why are the three sectors called interdependent?', ['the secondary sector depends on the primary sector for raw materials', 'both depend on the tertiary sector for transport, storage, banking and trade']),
            ('C3', 'D3', 'Classify the following into sectors: a farmer growing cotton, a mill making cloth, a truck carrying the cloth.', ['farmer growing cotton – primary', 'mill making cloth – secondary', 'truck carrying cloth – tertiary']),
            ('C4', 'D4', 'Explain with an example how the three sectors depend on one another.', ['a farmer grows sugarcane (primary)', 'a sugar mill buys it to make sugar (secondary)', 'trucks, banks and shops help the sugar reach consumers (tertiary)', 'a strike by transporters would affect both farmers and mills'])],
        AR=[('A strike by transporters affects farmers and factories.', 'The primary and secondary sectors depend on the tertiary sector.', 'a', 'R explains A.')],
        CAT=[('an activity of the tertiary sector', 'activities of the tertiary sector', ['banking', 'transport', 'teaching', 'trade'], ['fishing', 'mining', 'weaving cloth in a mill', 'making bricks'])],
    ),
    '19-st2': dict(
        T=[('gross domestic product', 'the value of all final goods and services produced within a country during a particular year'),
           ('final goods', 'goods that reach the consumers and are not used for further production'),
           ('intermediate goods', 'goods used up in producing final goods, such as wheat used for making flour'),
           ('double counting', 'counting the value of intermediate goods more than once while measuring production'),
           ('disguised unemployment', 'a situation in which more people are working than needed, so the work of some adds nothing to output'),
           ('underemployment', 'a situation in which people work less than their potential')],
        FB=[('Only the value of ___ goods and services is counted in GDP.', 'final', ['intermediate', 'raw', 'imported']),
            ('In India, the task of measuring GDP is done by a Union government ministry with the help of state and Union territory ___.', 'departments', ['courts', 'parties', 'banks']),
            ('Over the years, the ___ sector has emerged as the largest producing sector in India.', 'tertiary', ['primary', 'secondary', 'unorganised']),
            ('Even now, the largest share of workers in India is employed in the ___ sector.', 'primary', ['secondary', 'tertiary', 'organised']),
            ('Disguised unemployment is also called ___ unemployment.', 'hidden', ['open', 'seasonal', 'educated'])],
        EX=[('C2', 'D2', 'Why is only the value of final goods counted in GDP?', ['the value of final goods already includes the value of intermediate goods', 'counting both would lead to double counting']),
            ('C2', 'D3', 'Why has the tertiary sector become important in India?', ['basic services such as hospitals, schools, transport and banks are required by all', 'development of agriculture and industry and rising incomes increase demand for services such as IT, tourism and shopping']),
            ('C3', 'D3', 'Explain disguised unemployment with an example.', ['more people are working than needed', 'a small farm of five family members needs only three', 'if two move out, production does not fall']),
            ('C4', 'D4', 'Explain why the share of employment in the primary sector has not fallen as much as its share in production.', ['not enough jobs were created in the secondary and tertiary sectors', 'workers in agriculture are underemployed', 'many people lack skills for new jobs', 'so production shifted to services, but employment remained in agriculture'])],
        AR=[('Wheat sold to a flour mill is not counted separately in GDP.', 'Wheat is an intermediate good whose value is included in the final good.', 'a', 'R explains A.')],
        GEN=[('C3', 'D4', 'multi_step', gdp_final, {'kinds': ('sa3',)}), ('C3', 'D2', 'mcq', gdp_mcq), ('C3', 'D3', 'mcq', sector_share)],
    ),
    '19-st3': dict(
        T=[('organised sector', 'enterprises or places of work that are registered by the government and follow its rules, giving regular and assured work'),
           ('unorganised sector', 'small and scattered units, largely outside government control, with low-paid and irregular jobs'),
           ('MGNREGA', 'the Mahatma Gandhi National Rural Employment Guarantee Act, which guarantees 100 days of employment a year to rural households'),
           ('right to work', 'the guarantee of employment under MGNREGA, under which those who are not given work are given an unemployment allowance'),
           ('paid leave', 'leave for which workers get their salary, a benefit of the organised sector')],
        FB=[('MGNREGA was passed in ___.', '2005', ['1991', '1999', '2013']),
            ('Under MGNREGA, every rural household is guaranteed ___ days of employment in a year.', '100', ['30', '60', '200']),
            ('If the government fails to provide work under MGNREGA, it has to pay an unemployment ___.', 'allowance', ['tax', 'fine', 'loan']),
            ('Workers in the ___ sector enjoy security of employment, paid leave and provident fund.', 'organised', ['unorganised', 'informal', 'casual']),
            ('Laws such as the Factories Act, Minimum Wages Act and Payment of Gratuity Act apply to the ___ sector.', 'organised', ['unorganised', 'informal', 'household'])],
        EX=[('C2', 'D2', 'Why do workers in the unorganised sector need protection?', ['jobs are low-paid, irregular and without paid leave or holidays', 'there is no job security and workers can be asked to leave without reason']),
            ('C2', 'D3', 'Why was MGNREGA implemented?', ['to provide employment to rural households and reduce underemployment', 'the work, such as water conservation and land development, also raises production from land']),
            ('C3', 'D3', 'Distinguish between the organised and unorganised sectors.', ['organised: registered with the government and follows laws; unorganised: largely outside government control', 'organised: regular jobs with benefits; unorganised: low-paid, irregular jobs', 'organised: paid leave, provident fund and medical benefits; unorganised: none of these']),
            ('C4', 'D4', 'Suggest ways to protect workers in the unorganised sector.', ['enforcing minimum wages and fixing working hours', 'providing cheap loans to small producers', 'helping them with storage and marketing', 'providing social security such as health care and pensions'])],
        AR=[('Workers in the organised sector get paid leave.', 'Organised sector enterprises follow laws such as the Factories Act.', 'a', 'R explains A.'),
            ('MGNREGA guarantees 200 days of employment.', 'MGNREGA gives the right to work to rural households.', 'd', 'A is false – it guarantees 100 days; R is true.')],
        CASE=[('Read the source and answer the questions.',
               'Kanta works in an office and goes at 9.30 a.m. and returns at 5.30 p.m. She gets her salary regularly at the end of every month, along with provident fund, medical allowance and paid holidays. Her neighbour Kamal is a daily wage labourer who works only when work is available and gets no leave or medical benefit.',
               [('In which sector does Kanta work?', 'The organised sector.', 1), ('In which sector does Kamal work?', 'The unorganised sector.', 1),
                ('Give two benefits Kanta gets that Kamal does not.', 'Regular monthly salary; provident fund; medical allowance; paid holidays; job security.', 2)])],
    ),
    '19-st4': dict(
        T=[('public sector', 'the sector in which the government owns most of the assets and provides services'),
           ('private sector', 'the sector in which ownership of assets and delivery of services is in the hands of private individuals or companies'),
           ('profit motive', 'the aim of earning profits, which drives private sector activities'),
           ('public goods', 'facilities such as roads, bridges and railways that are needed by all but too costly for private firms to provide')],
        FB=[('Indian Railways and the post office are examples of the ___ sector.', 'public', ['private', 'unorganised', 'cooperative']),
            ('Tata Iron and Steel Company Limited (TISCO) and Reliance Industries Limited are ___ sector companies.', 'private', ['public', 'joint', 'cooperative']),
            ('Activities in the private sector are guided by the motive to earn ___.', 'profits', ['votes', 'taxes', 'loans']),
            ('The purpose of the public sector is not just to earn profits but to promote ___ welfare.', 'public', ['private', 'family', 'company'])],
        EX=[('C2', 'D2', 'Why does the government provide facilities such as roads and railways?', ['they need huge spending that private firms cannot afford', 'private firms cannot easily charge users enough to make a profit']),
            ('C2', 'D3', 'Why does the government sell electricity and water at low rates?', ['many small industries and the poor cannot afford high rates', 'the government bears part of the cost to promote public welfare']),
            ('C3', 'D3', 'Distinguish between the public and private sectors.', ['public: government owns assets; private: individuals or companies own assets', 'public: aims at public welfare; private: aims at profit', 'public: Indian Railways, post office; private: TISCO, Reliance Industries']),
            ('C4', 'D4', 'Explain the role of the public sector in the economic development of a country.', ['it provides infrastructure such as roads, bridges, railways and ports', 'it supplies electricity and water at low cost', 'it ensures health and education for all', 'it buys grains at fair prices and sells them through ration shops'])],
        AR=[('The government provides health and education facilities.', 'Many people cannot afford private hospitals and schools.', 'a', 'R explains A.')],
        CAT=[('a public sector enterprise or service', 'public sector enterprises or services', ['Indian Railways', 'post office', 'government hospitals', 'government schools'],
              ['Reliance Industries', 'TISCO', 'a private bus company', 'a private coaching centre'])],
    ),
    # ---------------- ch20 Money and Credit
    '20-st1': dict(
        T=[('double coincidence of wants', 'a situation in which what one person wishes to sell is exactly what the other wishes to buy'),
           ('barter system', 'a system in which goods are directly exchanged without the use of money'),
           ('medium of exchange', 'something that acts as an intermediate in exchanges, which is the role money plays'),
           ('demand deposits', 'deposits in bank accounts that can be withdrawn on demand'),
           ('cheque', 'a paper instructing the bank to pay a specific amount from the person\'s account to the person named on it'),
           ('currency', 'paper notes and coins, which are the modern form of money')],
        FB=[('In India, the ___ issues currency notes on behalf of the central government.', 'Reserve Bank of India', ['State Bank of India', 'Finance Commission', 'NITI Aayog']),
            ('Money acts as a ___ of exchange.', 'medium', ['measure only', 'barrier', 'tax']),
            ('Deposits in bank accounts that can be withdrawn on demand are called ___ deposits.', 'demand', ['fixed', 'time', 'credit']),
            ('Banks in India these days hold about ___ per cent of their deposits as cash.', '15', ['5', '50', '75']),
            ('Modern currency is accepted as a medium of exchange because it is authorised by the ___.', 'government', ['banks only', 'traders', 'moneylenders'])],
        EX=[('C2', 'D2', 'Why does money remove the problem of double coincidence of wants?', ['money acts as an intermediate in the exchange process', 'a person can sell goods for money and use that money to buy what he or she wants']),
            ('C2', 'D3', 'Why are demand deposits considered money?', ['they can be withdrawn on demand and used for payments', 'cheques against them are widely accepted as a means of payment']),
            ('C3', 'D3', 'Describe three modern forms of money.', ['currency – paper notes and coins issued by the RBI', 'deposits with banks that can be withdrawn on demand', 'payments by cheque and digital modes from bank accounts']),
            ('C4', 'D4', 'Explain the problems of the barter system and how money solves them.', ['barter needs double coincidence of wants', 'goods are hard to divide and store', 'there is no common measure of value', 'money is a medium of exchange, a measure of value and a store of value'])],
        AR=[('Currency is accepted as a medium of exchange in India.', 'The law legalises the use of rupees as a medium of payment.', 'a', 'R explains A.')],
    ),
    '20-st2': dict(
        T=[('credit', 'an agreement in which the lender supplies the borrower with money, goods or services in return for a promise of future payment'),
           ('collateral', 'an asset that the borrower owns, such as land or a building, and uses as a guarantee to the lender until the loan is repaid'),
           ('terms of credit', 'the interest rate, collateral, documentation and mode of repayment that together form a loan agreement'),
           ('debt trap', 'a situation in which a borrower cannot repay a loan and has to borrow again, getting deeper into debt'),
           ('interest rate', 'the extra amount that the borrower pays to the lender along with the principal')],
        FB=[('The asset used as a guarantee for a loan is called ___.', 'collateral', ['interest', 'deposit', 'cheque']),
            ('Banks use the major portion of deposits to extend ___.', 'loans', ['donations', 'taxes', 'salaries']),
            ('The difference between what banks charge borrowers and what they give depositors is their main source of ___.', 'income', ['expense', 'loss', 'tax']),
            ('When a borrower fails to repay, credit can push the borrower into a ___.', 'debt trap', ['surplus', 'profit', 'subsidy'])],
        EX=[('C2', 'D2', 'Why do lenders ask for collateral?', ['it is a guarantee that the loan will be repaid', 'if the borrower fails to repay, the lender can sell the collateral to recover the money']),
            ('C2', 'D3', 'Why can credit be useful for one person and harmful for another?', ['credit helps when it is used productively and the earnings are enough to repay', 'when crops fail or income falls, the borrower may have to sell assets, falling into a debt trap']),
            ('C3', 'D3', 'Describe the terms of credit.', ['interest rate', 'collateral', 'documentation required', 'mode of repayment']),
            ('C4', 'D4', 'Explain with an example how credit can push a person into a debt trap.', ['a small farmer borrows from a moneylender at high interest to grow crops', 'the crop fails because of drought or pests', 'the farmer cannot repay and borrows again', 'the debt grows and the farmer may have to sell land'])],
        AR=[('Credit helps people in many cases.', 'Credit allows people to meet ongoing expenses of production and increase earnings.', 'a', 'R explains A.')],
        GEN=[('C3', 'D3', 'mcq', bank_lending), ('C4', 'D4', 'multi_step', credit_cost, {'kinds': ('sa3',)})],
    ),
    '20-st3': dict(
        T=[('formal sources of credit', 'loans from banks and cooperatives, which are supervised by the Reserve Bank of India'),
           ('informal sources of credit', 'loans from moneylenders, traders, employers, relatives and friends, without government supervision'),
           ('cooperative society', 'an organisation in which members pool resources for cooperation in certain areas, such as giving loans to farmers'),
           ('Reserve Bank of India', 'the central bank of India, which supervises the functioning of formal sources of loans')],
        FB=[('The ___ supervises the functioning of formal sources of loans in India.', 'Reserve Bank of India', ['Supreme Court', 'Election Commission', 'Planning Commission']),
            ('Moneylenders and traders are ___ sources of credit.', 'informal', ['formal', 'public', 'cooperative']),
            ('Banks and cooperatives are ___ sources of credit.', 'formal', ['informal', 'illegal', 'private']),
            ('Banks are required to submit information to the RBI on how much they are ___ and to whom.', 'lending', ['saving', 'taxing', 'spending'])],
        EX=[('C2', 'D2', 'Why are formal sources of credit better than informal ones?', ['they charge lower interest rates', 'they are supervised by the RBI, so borrowers are not exploited']),
            ('C2', 'D3', 'Why do poor households still depend on informal sources of credit?', ['banks ask for collateral and documents that the poor lack', 'moneylenders know them personally and give loans quickly without collateral']),
            ('C3', 'D3', 'Describe three ways in which the RBI supervises banks.', ['banks must maintain a minimum cash balance out of deposits', 'the RBI sees that banks give loans to small cultivators, small industries and small borrowers, not just to profit-making businesses', 'banks must submit information on how much they lend, to whom and at what rate']),
            ('C4', 'D4', '"Cheap and affordable credit is crucial for the country\'s development." Explain.', ['cheap credit lets people start businesses and farms', 'it raises incomes and production', 'high interest from informal sources means more income goes to repay', 'formal credit should therefore reach the poor'])],
        AR=[('Rich households borrow mostly from formal sources.', 'They can offer collateral and documents that banks require.', 'a', 'R explains A.'),
            ('Moneylenders are supervised by the Reserve Bank of India.', 'Moneylenders give loans without collateral.', 'd', 'A is false – there is no organisation that supervises informal lenders; R is true.')],
        CAT=[('an informal source of credit', 'informal sources of credit', ['moneylenders', 'traders', 'employers', 'relatives and friends'], ['commercial banks', 'cooperative societies', 'regional rural banks', 'cooperative banks'])],
    ),
    '20-st4': dict(
        T=[('Self-Help Group', 'a group of 15-20 members, usually women from one neighbourhood, who pool their savings and give small loans to members'),
           ('Grameen Bank', 'the bank in Bangladesh that gives credit to the poor at reasonable rates'),
           ('microcredit', 'small loans to poor people who cannot get bank loans')],
        FB=[('A typical Self-Help Group has ___ members.', '15-20', ['2-5', '50-100', '200-300']),
            ('The Grameen Bank of Bangladesh was started by ___.', 'Muhammad Yunus', ['Amartya Sen', 'Sheikh Mujibur Rahman', 'Kofi Annan']),
            ('Muhammad Yunus received the Nobel Peace Prize in ___.', '2006', ['1998', '2001', '2014']),
            ('Members of Self-Help Groups are mostly ___.', 'women', ['industrialists', 'bankers', 'landlords'])],
        EX=[('C2', 'D2', 'Why do Self-Help Groups help the poor get credit?', ['the group as a whole is responsible for repayment, so no collateral is needed', 'banks are willing to lend to the group after it has saved regularly for a year or two']),
            ('C2', 'D3', 'Why are Self-Help Groups important for women?', ['they help women become financially self-reliant', 'regular meetings give a platform to discuss social issues such as health, nutrition and domestic violence']),
            ('C3', 'D3', 'Describe three features of Self-Help Groups.', ['15-20 members, usually women from one neighbourhood', 'members save regularly and give small loans to each other', 'decisions about loans are taken by the group, and banks lend to the group']),
            ('C4', 'D4', 'Explain how Self-Help Groups help solve the problem of lack of collateral for the poor.', ['the group takes responsibility for repaying loans', 'peer pressure ensures repayment', 'banks lend to the group without collateral', 'members get timely loans at reasonable interest, freeing them from moneylenders'])],
        AR=[('Banks give loans to Self-Help Groups without collateral.', 'The group as a whole is responsible for repaying the loan.', 'a', 'R explains A.')],
        CASE=[('Read the source and answer the questions.',
               'Seventeen women of a village formed a group and began to save ₹100 each month. After two years, the bank gave the group a loan. Rekha used her share to buy a sewing machine and began stitching clothes for the village. The group also discussed the village school and safe drinking water at its meetings.',
               [('What kind of group is described here?', 'A Self-Help Group (SHG).', 1), ('Why did the bank lend without collateral?', 'The group as a whole is responsible for repayment.', 1),
                ('Give two benefits Rekha and the group got.', 'Rekha started her own source of income; members became financially self-reliant; the group discussed social issues; freedom from moneylenders.', 2)])],
    ),
    # ---------------- ch21 Globalisation and the Indian Economy
    '21-st1': dict(
        T=[('multinational corporation', 'a company that owns or controls production in more than one nation'),
           ('investment', 'money spent on assets such as land, buildings, machines and equipment'),
           ('foreign investment', 'investment made by MNCs in another country'),
           ('joint production', 'production in which an MNC sets up a business together with a local company')],
        FB=[('Cargill Foods, an American MNC, bought over the Indian company ___.', 'Parakh Foods', ['Amul', 'Britannia', 'Dabur']),
            ('Ford Motors came to India in 1995 and set up a large plant near ___.', 'Chennai', ['Pune', 'Kolkata', 'Delhi']),
            ('Ford Motors set up its Indian plant in collaboration with ___.', 'Mahindra and Mahindra', ['Tata Motors', 'Maruti Suzuki', 'Bajaj Auto']),
            ('MNCs set up production where it is close to markets and where there is skilled and unskilled labour at ___ costs.', 'low', ['high', 'fixed', 'rising'])],
        EX=[('C2', 'D2', 'Why do MNCs set up production in countries like India?', ['labour is available at low costs', 'they are close to markets and the government policies are favourable']),
            ('C2', 'D3', 'Why do MNCs often buy up local companies?', ['buying local companies quickly expands their production', 'they get the local company\'s market, brand and distribution network']),
            ('C3', 'D3', 'Describe three ways in which MNCs spread their production across countries.', ['setting up partnerships with local companies, i.e. joint production', 'buying up local companies', 'placing orders with small producers in other countries']),
            ('C4', 'D4', 'Explain how MNCs are interlinking production across countries.', ['a product is designed in one country', 'parts are made in another and assembled elsewhere', 'it is sold in markets all over the world', 'e.g. a garment brand gets clothes made by small Indian producers and sells them abroad under its own name'])],
        AR=[('MNCs set up offices and factories in countries like India.', 'Cheap labour and nearness to markets lower their costs.', 'a', 'R explains A.')],
    ),
    '21-st2': dict(
        T=[('foreign trade', 'the exchange of goods and services between countries'),
           ('integration of markets', 'the joining of markets of different countries through trade and investment'),
           ('globalisation', 'the process of rapid integration or interconnection between countries'),
           ('choice for consumers', 'the wider range of goods available to buyers as a result of foreign trade')],
        FB=[('Foreign trade creates an opportunity for producers to reach beyond the ___ markets.', 'domestic', ['foreign', 'world', 'global']),
            ('Chinese toys became popular in India because they were cheaper and had new ___.', 'designs', ['taxes', 'brands only', 'labels only']),
            ('Globalisation is the process of rapid integration or interconnection between ___.', 'countries', ['villages', 'families', 'courts']),
            ('Besides goods and services, globalisation involves the movement of investment, technology and ___ between countries.', 'people', ['rivers', 'mountains', 'climates'])],
        EX=[('C2', 'D2', 'Why does foreign trade lead to the integration of markets?', ['goods produced in one country reach markets in others', 'prices of similar goods in different markets tend to become equal']),
            ('C2', 'D3', 'Why did Indian toy makers suffer when Chinese toys came to India?', ['Chinese toys were cheaper and had new designs', 'Indian toy makers faced losses as buyers had more choice']),
            ('C3', 'D3', 'Describe three ways in which countries are being interconnected through globalisation.', ['movement of goods and services through trade', 'movement of investment through MNCs', 'movement of technology and people between countries']),
            ('C4', 'D4', 'Explain how foreign trade benefits both producers and consumers.', ['producers can sell beyond domestic markets', 'buyers get a wider choice of goods', 'competition improves quality', 'prices of similar goods tend to become equal across markets'])],
        AR=[('Foreign trade increases the choice of goods for consumers.', 'Goods produced in other countries become available in local markets.', 'a', 'R explains A.')],
        GEN=[('C3', 'D3', 'numerical', import_duty, {'kinds': ('sa2',)})],
    ),
    '21-st3': dict(
        T=[('liberalisation', 'the removal of barriers or restrictions set by the government on trade and investment'),
           ('trade barrier', 'a restriction such as a tax on imports that a government uses to regulate foreign trade'),
           ('World Trade Organisation', 'the organisation that aims to liberalise international trade by establishing rules for it'),
           ('Special Economic Zones', 'industrial zones with world-class facilities set up to attract foreign companies'),
           ('information and communication technology', 'technology such as computers, telecommunications and the internet that has spread globalisation')],
        FB=[('In ___, the Indian government made far-reaching changes in economic policy that removed many trade barriers.', '1991', ['1947', '1975', '2005']),
            ('A tax on imports is an example of a ___.', 'trade barrier', ['subsidy', 'direct tax', 'public good']),
            ('The WTO aims to ___ international trade.', 'liberalise', ['restrict', 'stop', 'nationalise']),
            ('Rapid improvement in ___ technology has been a major factor in globalisation.', 'transportation and communication', ['handloom', 'cave painting', 'bullock cart'])],
        EX=[('C2', 'D2', 'Why did the Indian government put trade barriers after Independence?', ['to protect domestic producers from foreign competition', 'industries were just coming up and needed protection']),
            ('C2', 'D3', 'Why did India decide to remove barriers in 1991?', ['Indian producers were thought to be ready to compete with foreign producers', 'competition would improve the quality of Indian products']),
            ('C3', 'D3', 'Describe three factors that have enabled globalisation.', ['rapid improvement in transport technology', 'development of information and communication technology', 'liberalisation of foreign trade and investment policies']),
            ('C4', 'D4', '"The WTO rules have forced developing countries to liberalise, while developed countries retain barriers." Examine.', ['the WTO aims to liberalise trade for all', 'developing countries were pressed to remove trade barriers', 'developed countries continue to give large subsidies to their farmers', 'this makes trade unfair for poor countries'])],
        AR=[('A tax on imports is a trade barrier.', 'It makes imported goods more expensive and reduces their import.', 'a', 'R explains A.'),
            ('Liberalisation means putting more restrictions on trade.', 'In 1991 India changed its economic policy.', 'd', 'A is false – liberalisation removes restrictions; R is true.')],
        CHRON=[('India removes many trade barriers', 1991), ('World Trade Organisation set up', 1995), ('Special Economic Zones Act', 2005)],
    ),
    '21-st4': dict(
        T=[('fair globalisation', 'globalisation that creates opportunities for all and ensures that its benefits are better shared'),
           ('flexibility in labour laws', 'allowing employers to hire workers temporarily, so that they can be removed when there is less work'),
           ('competition', 'rivalry among producers that can lead to better quality and lower prices'),
           ('outsourcing', 'getting work done by companies or workers in other places or countries, such as call centres')],
        FB=[('Globalisation has benefited well-off consumers and skilled, educated and ___ producers.', 'wealthy', ['poor', 'small', 'unskilled']),
            ('Many small producers of batteries, capacitors and ___ have been hit hard by competition.', 'plastics', ['software', 'satellites', 'aircraft']),
            ('Some large Indian companies have themselves emerged as ___.', 'multinationals', ['cooperatives', 'NGOs', 'government departments']),
            ('Due to flexible labour laws, workers are increasingly employed on a ___ basis.', 'temporary', ['permanent', 'pensionable', 'government'])],
        EX=[('C2', 'D2', 'Why has globalisation not benefited everyone equally?', ['skilled and wealthy producers and well-off consumers gained more', 'small producers and many workers faced competition and job insecurity']),
            ('C2', 'D3', 'Why are workers\' jobs less secure under globalisation?', ['employers prefer to hire workers flexibly to cut costs', 'workers are employed temporarily and can be removed when there is less work']),
            ('C3', 'D3', 'Describe three positive impacts of globalisation on India.', ['greater choice and better quality for consumers', 'new jobs in industries and services', 'foreign investment and the rise of Indian MNCs']),
            ('C4', 'D4', 'Suggest steps the government can take to ensure fair globalisation.', ['protect workers through enforcing labour laws', 'support small producers to improve performance', 'use trade and investment barriers where necessary', 'negotiate at the WTO for fairer rules'])],
        AR=[('Some small manufacturers in India were hit hard by globalisation.', 'Cheaper imports increased competition in their markets.', 'a', 'R explains A.')],
        CASE=[('Read the source and answer the questions.',
               'Ravi set up a small factory making capacitors in Hosur. When cheaper imports arrived, his buyers began to buy the imported ones. He had to cut his workers\' wages and hire them only for short periods. Meanwhile, consumers in the city were happy with the wider choice of electronic goods at lower prices.',
               [('Who benefited from the change described here?', 'Consumers, who got wider choice at lower prices.', 1), ('Who was hurt by it?', 'Small producers like Ravi and their workers.', 1),
                ('Suggest two ways the government could help producers like Ravi.', 'Cheap credit; support for better technology; marketing help; use of trade barriers where necessary; better infrastructure.', 2)])],
    ),
    # ---------------- ch22 Consumer Rights
    '22-st1': dict(
        T=[('consumer', 'a person who buys goods and services for personal use'),
           ('consumer movement', 'the social force that arose out of consumers\' dissatisfaction with unfair practices of sellers'),
           ('consumer exploitation', 'unfair trade practices such as underweighing, adulteration, false information and high prices'),
           ('Consumers International', 'the umbrella body of over 240 consumer organisations from more than 100 countries'),
           ('adulteration', 'mixing inferior or harmful substances into goods such as food')],
        FB=[('The consumer movement in India arose in the ___ as a social force.', '1960s', ['1930s', '1980s', '2000s']),
            ('National Consumers\' Day is celebrated in India on ___.', '24 December', ['15 March', '15 August', '2 October']),
            ('World Consumer Rights Day is observed on ___.', '15 March', ['24 December', '26 January', '5 June']),
            ('In 1985 the United Nations adopted the UN Guidelines for ___.', 'Consumer Protection', ['Trade Barriers', 'Election Reform', 'Wildlife Protection'])],
        EX=[('C2', 'D2', 'Why are consumers often exploited in the market?', ['producers are few and powerful while consumers buy in small amounts and are scattered', 'consumers often lack information and awareness']),
            ('C2', 'D3', 'Why did the consumer movement begin in India?', ['there was widespread food shortage, hoarding, black marketing and adulteration', 'consumer groups were formed to fight these practices and later to get rights']),
            ('C3', 'D3', 'Describe three ways in which consumers are exploited.', ['underweighing and undermeasuring', 'adulteration and defective goods', 'false information and high prices', 'poor after-sales service']),
            ('C4', 'D4', 'Explain the role of consumer organisations in protecting consumers.', ['they make people aware of their rights', 'they write articles and hold exhibitions', 'they guide consumers in filing cases in consumer commissions', 'they represent consumers in government bodies'])],
        AR=[('Consumers need protection in the market.', 'Sellers can shift responsibility onto the buyer and indulge in unfair practices.', 'a', 'R explains A.')],
    ),
    '22-st2': dict(
        T=[('right to safety', 'the right of consumers to be protected against goods and services that are hazardous to life and property'),
           ('right to information', 'the right to know details of the product such as ingredients, price, batch number, date of manufacture and expiry date'),
           ('right to choose', 'the right to be assured access to a variety of goods at competitive prices'),
           ('right to seek redressal', 'the right to seek redressal against unfair trade practices and exploitation'),
           ('right to represent', 'the right to be heard and to represent consumers in consumer commissions'),
           ('Maximum Retail Price', 'the highest price at which a product can be sold, printed on its packet')],
        FB=[('Printing the date of expiry on a medicine packet is linked to the right to ___.', 'information', ['choose', 'represent', 'safety only']),
            ('The Right to Information Act was passed in ___.', '2005', ['1986', '1991', '2019']),
            ('A consumer can bargain with the seller if the price is lower than the ___ printed on the packet.', 'MRP', ['GST', 'ISI', 'PIN']),
            ('A gas supplier insisting that a stove must be bought along with a new connection violates the right to ___.', 'choose', ['safety', 'information', 'redressal'])],
        EX=[('C2', 'D2', 'Why is the right to information important for consumers?', ['it lets consumers know the details of the product they buy', 'they can complain and ask for compensation if the product proves defective']),
            ('C2', 'D3', 'Why is the right to safety important for consumers of electrical goods and vehicles?', ['such goods can cause serious harm if poorly made', 'manufacturers must follow safety rules and standards']),
            ('C3', 'D3', 'Describe three consumer rights.', ['right to safety', 'right to information', 'right to choose', 'right to seek redressal', 'right to represent']),
            ('C4', 'D4', 'Explain the duties a consumer should keep in mind while buying goods.', ['check the quality, MRP and expiry date', 'look for standardisation marks such as ISI and Agmark', 'ask for a bill and warranty card', 'complain about defects through proper channels'])],
        AR=[('A consumer has the right to seek redressal.', 'Consumers can claim compensation for exploitation and unfair practices.', 'a', 'R explains A.'),
            ('Printing the expiry date on a medicine packet is linked to the right to choose.', 'Consumers have the right to know the details of the products they buy.', 'd', 'A is false – it is linked to the right to information; R is true.')],
        SC=[('A shopkeeper refuses to sell toothpaste unless the customer also buys a toothbrush. Which consumer right is violated?', 'Right to choose',
             ['Right to safety', 'Right to represent', 'Right to education'], 'Forcing the customer to buy another product violates the right to choose.')],
    ),
    '22-st3': dict(
        T=[('COPRA', 'the Consumer Protection Act, first enacted in 1986 and replaced by a new Act in 2019'),
           ('consumer commission', 'a quasi-judicial body that settles consumer disputes at the district, state and national levels'),
           ('ISI mark', 'the certification mark given by the Bureau of Indian Standards to industrial and consumer goods'),
           ('Agmark', 'the certification mark for agricultural products'),
           ('Hallmark', 'the certification mark of the Bureau of Indian Standards for the purity of gold jewellery'),
           ('Bureau of Indian Standards', 'the national body that develops standards and certifies goods')],
        FB=[('The Consumer Protection Act was first enacted in ___.', '1986', ['1976', '1991', '2005']),
            ('The Consumer Protection Act was replaced by a new Act in ___.', '2019', ['2005', '2010', '2015']),
            ('Under COPRA, a three-tier quasi-judicial machinery works at the district, state and ___ levels.', 'national', ['village', 'block', 'international']),
            ('The mark used to certify agricultural products is ___.', 'Agmark', ['ISI', 'Hallmark', 'FSSAI barcode']),
            ('The ___ mark certifies the purity of gold jewellery.', 'Hallmark', ['Agmark', 'ISI', 'Ecomark'])],
        EX=[('C2', 'D2', 'Why were consumer commissions set up under COPRA?', ['to give consumers a simple and quick way to settle disputes', 'consumers need not go through lengthy and expensive civil courts']),
            ('C2', 'D3', 'Why are standardisation marks like ISI and Agmark useful for consumers?', ['they assure the quality of the products', 'they help consumers choose safe goods']),
            ('C3', 'D3', 'Describe the three-tier consumer dispute redressal machinery.', ['District Commission for claims up to ₹1 crore', 'State Commission for claims between ₹1 crore and ₹10 crore', 'National Commission for claims above ₹10 crore']),
            ('C4', 'D4', 'Evaluate the success of the consumer movement in India.', ['COPRA and consumer commissions were set up', 'awareness has increased through campaigns like "Jago Grahak Jago"', 'but the redressal process can be slow and costly', 'rules are not always enforced and consumer awareness is low in villages'])],
        AR=[('Consumer commissions give quick relief to consumers.', 'They work under COPRA with simpler procedures than civil courts.', 'a', 'R explains A.')],
        CHRON=[('UN Guidelines for Consumer Protection', 1985), ('first Consumer Protection Act', 1986), ('Right to Information Act', 2005), ('new Consumer Protection Act', 2019)],
        GEN=[('C3', 'D3', 'mcq', commission)],
        CASE=[('Read the source and answer the questions.',
               'Abhiram bought a new mobile phone with a one-year warranty. Within two months it stopped working. The shop refused to repair it, saying the fault was his. Abhiram filed a complaint at the District Commission with the bill and warranty card, and the commission ordered the company to replace the phone.',
               [('Which consumer right did Abhiram use?', 'The right to seek redressal.', 1), ('Under which law did the District Commission act?', 'The Consumer Protection Act (COPRA), 2019.', 1),
                ('Give two things a consumer should keep to file such a complaint.', 'The bill or cash memo; the warranty card; details of the product and defect.', 2)])],
    ),
}
