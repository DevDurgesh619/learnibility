"""Cambridge IGCSE Geography 0460, year 2 (grade 10): human topics and geographical enquiry.

Paper 2-style resource-based structured questions (population, settlement, development, economic
activity, resources) with data described in words and answers computed in code, named case studies
with 7-mark levels-marked answers, and Paper 4 / coursework-style fieldwork items (hypotheses,
sampling, methods, presentation, analysis and evaluation).

Reuses the knowledge-pack builders from g9_geography.py (not modified here).
"""
import math
from ._lib import topic, mcq, compose, person, two_people, city, sf, fmt
from .g9_geography import (T, cap, low, an, build, add_case, add_cs, add_essay, add_mcqs, as_c4, mean, median, pct_change,
                           dp, nf, trend_words, MON, MONTHS, LEVELS7)

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
LETTERS = 'PQRSTUVW'

# ============================================================== CHAPTER 1: Population dynamics

c1a = T('Global population growth: birth rates, death rates and natural increase', 'birth rates death rates natural increase')
build(c1a, {
    'terms': [
        ('birth rate', 'the number of live births per 1000 people in a year'),
        ('death rate', 'the number of deaths per 1000 people in a year'),
        ('natural increase', 'the difference between the birth rate and the death rate when births exceed deaths, usually given as a percentage'),
        ('natural decrease', 'when the death rate is higher than the birth rate, so the population falls without migration'),
        ('fertility rate', 'the average number of children born to each woman during her lifetime'),
        ('infant mortality rate', 'the number of babies who die before their first birthday per 1000 live births'),
        ('life expectancy', 'the average number of years a person born in a country can expect to live'),
        ('population explosion', 'the very rapid growth of world population since about 1950, mainly in LICs'),
        ('demographic transition model', 'a model showing how birth rates, death rates and population change as a country develops, in five stages'),
        ('replacement level', 'a fertility rate of about 2.1 children per woman, at which a population replaces itself'),
    ],
    'mcq': [
        ('A country has a birth rate of 32 per 1000 and a death rate of 8 per 1000. What is its rate of natural increase?', '2.4%', ['24%', '4.0%', '0.24%'], '(32 − 8) ÷ 10 = 2.4%. [1]'),
        ('In which stage of the demographic transition model is the death rate falling rapidly while the birth rate stays high?', 'Stage 2', ['Stage 1', 'Stage 4', 'Stage 5'], '[1]'),
        ('About what was the world population in 2023?', 'About 8 billion', ['About 2 billion', 'About 4 billion', 'About 20 billion'], 'The UN estimated 8 billion in November 2022. [1]'),
        ('Which country is an example of stage 5 of the DTM, with natural decrease?', 'Japan', ['Niger', 'Bangladesh in the 1970s', 'Nigeria'], '[1]'),
        ('Which factor most directly lowers the death rate in a developing country?', 'Clean water and improved health care, such as vaccinations', ['More women working in factories', 'Higher cost of raising children', 'Later marriage'], '[1]'),
        ('A fertility rate of about 2.1 is known as', 'replacement level', ['natural decrease', 'zero growth', 'the infant mortality rate'], '[1]'),
    ],
    'explain': [
        ('Explain why death rates have fallen in many LICs.', 'Better health care and vaccinations, clean water and sanitation, improved food supply and nutrition, and education about hygiene.', '1 mark each developed reason up to [3]'),
        ('Explain why birth rates remain high in many LICs.', 'Children work on farms and support parents in old age; high infant mortality means more children are had; limited access to contraception; early marriage; religious or cultural traditions.', '1 mark each developed reason up to [3]'),
        ('Explain why birth rates fall as countries develop.', 'More women are educated and work; contraception is available; children cost more to raise and are in education rather than working; lower infant mortality; urban lifestyles.', '1 mark each up to [3]'),
        ('Explain why world population grew rapidly after 1950.', 'Death rates fell quickly in LICs because of medicine, vaccination and clean water, while birth rates stayed high, so natural increase was very large.', '1 mark falling death rate with reason; 1 mark high birth rate [2]'),
        ('Explain why some HICs have natural decrease.', 'Very low birth rates (career choices, cost of children, late marriage) and an ageing population with a rising death rate; e.g. Japan.', '1 mark low birth rate; 1 mark ageing [2]'),
    ],
    'claims': [
        ('Natural increase is the birth rate plus the death rate.', False, 'It is the birth rate minus the death rate.'),
        ('Most of the world’s population growth now takes place in LICs and MICs.', True, 'Countries in sub-Saharan Africa and South Asia have the highest natural increase.'),
        ('A country in stage 4 of the DTM has a rapidly growing population.', False, 'In stage 4 birth and death rates are both low, so growth is slow or stable.'),
        ('Migration does not affect a country’s rate of natural increase.', True, 'Natural increase only compares births and deaths; total population change also includes migration.'),
    ],
    'essays': [
        ('the main reason for rapid population growth in LICs is a high birth rate',
         ['High fertility (e.g. Niger about 6.7 children per woman) driven by farming needs, cultural factors and limited contraception.'],
         ['The fall in death rates due to medicine, vaccination and clean water created the gap; a young population structure means many future parents (population momentum).'],
         'Growth comes from the gap between births and deaths; falling death rates started it but high birth rates sustain it.',
         ['death rates', 'fertility', 'young population', 'DTM']),
    ],
})


COUNTRIES_BD = [('Niger', 45, 8), ('Nigeria', 36, 12), ('India', 16, 7), ('Bangladesh', 18, 5), ('Brazil', 12, 7), ('UK', 10, 9), ('Japan', 6, 13), ('Italy', 7, 12),
                ('Kenya', 27, 5), ('Egypt', 22, 6), ('Mexico', 15, 7), ('USA', 11, 10), ('Germany', 9, 12), ('Pakistan', 27, 7)]


@c1a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1a_ni(r, D):
    k = 4 if D >= 3 else 3
    rows = r.sample(COUNTRIES_BD, k)
    # small jitter keeps tables fresh while staying realistic
    rows = [(n, b + r.choice([-1, 0, 0, 1]), d + r.choice([-1, 0, 0, 1])) for n, b, d in rows]
    stem = 'Table 1.1 shows birth and death rates (per 1000 per year) for selected countries. ' + ' '.join(f'{n}: birth rate {b}, death rate {d}.' for n, b, d in rows)
    ni = [(n, (b - d) / 10) for n, b, d in rows]
    if D == 1:
        n, b, d = rows[0]
        v = (b - d) / 10
        opts, a = mcq(r, f'{fmt(v, 1)}%', [f'{fmt(b - d, 1)}%', f'{fmt((b + d) / 10, 1)}%', f'{fmt(v * 2, 1)}%', f'{fmt(v / 10, 2)}%', f'{fmt(v + 0.5, 1)}%', f'{fmt(v - 0.3, 1)}%'])
        return {'stem': stem + f' What is the rate of natural increase for {n}?', 'options': opts, 'answer': a, 'key': f'({b} − {d}) ÷ 10 = {fmt(v, 1)}%. [1]'}
    hi = max(ni, key=lambda x: x[1])
    neg = [n for n, v in ni if v < 0]
    parts = [
        lambda r: ('Calculate the rate of natural increase (%) for each country.', '; '.join(f'{n} {fmt(v, 1)}%' for n, v in ni), '(birth rate − death rate) ÷ 10 for each; 1 mark for two correct, 2 marks all correct [2]'),
        lambda r: ('Identify the country with the fastest natural increase.', f'{hi[0]} ({fmt(hi[1], 1)}%)', '[1]') if [v for _, v in ni].count(hi[1]) == 1 else None,
        lambda r: ('Name a country in the table with natural decrease and suggest why.', (f'{neg[0]}: very low birth rate and an ageing population with a high death rate.' if neg else 'None of these countries has natural decrease; all have birth rates above death rates.'), '1 mark identification; 1 mark reason [2]'),
        lambda r: (f'Suggest which stage of the demographic transition model {hi[0]} is in. Give a reason.', ('Stage 2 or early stage 3: birth rate still high but death rate low.' if hi[1] >= 1.5 else 'Stage 3 or 4: birth rate falling towards the low death rate.'), '1 mark stage; 1 mark reason using data [2]'),
        lambda r: (f'Using the rule of 70, estimate how long the population of {hi[0]} would take to double.', (f'About {round(70 / hi[1])} years (70 ÷ {fmt(hi[1], 1)})' if hi[1] > 0 else 'It would not double.'), f'70 ÷ {fmt(hi[1], 1)} = {fmt(round(70 / hi[1], 1), 1) if hi[1] > 0 else "-"} [1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1a.add('C3', (2, 3, 4, 5), 'numerical')
def c1a_world(r, D):
    yrs = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    pop = [2.5, 3.0, 3.7, 4.4, 5.3, 6.1, 6.9, 7.8]
    stem = 'Fig. 1.1 is a line graph of world population (billions): ' + ', '.join(f'{y}: {fmt(p, 1)}' for y, p in zip(yrs, pop)) + '.'
    a, b = sorted(r.sample(range(len(yrs)), 2))
    pc = pct_change(pop[a], pop[b])
    parts = [
        lambda r: ('Describe the trend shown in Fig. 1.1. Use data.', 'Rapid, continuous growth from 2.5 billion in 1950 to 7.8 billion in 2020; it more than tripled; the increase per decade was largest in the 1980s (0.9 billion).', '1 mark trend; 1 mark rate; 1 mark data [3]'),
        lambda r: (f'Calculate the percentage increase between {yrs[a]} and {yrs[b]}.', f'{dp(pc)}%', f'({fmt(pop[b], 1)} − {fmt(pop[a], 1)}) ÷ {fmt(pop[a], 1)} × 100 = {dp(pc)}% [2]'),
        lambda r: ('Explain why world population grew so rapidly after 1950.', 'Death rates fell sharply in LICs because of vaccines, antibiotics, clean water and better food, while birth rates stayed high.', '1 mark falling death rates + reason; 1 mark high birth rates [2]'),
        lambda r: ('Suggest why the rate of growth has started to slow.', 'Falling fertility as more women are educated and use contraception, urbanisation, and policies such as family planning.', '1 mark each up to [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 1.2 population structure
c1b = T('Population structure: population pyramids and dependency ratios', 'population pyramids dependency ratios')
build(c1b, {
    'terms': [
        ('population structure', 'the make-up of a population by age group and sex'),
        ('population pyramid', 'a pair of horizontal bar graphs showing the percentage or number of males and females in each age group'),
        ('dependency ratio', 'the number of dependants (aged 0-14 and 65+) for every 100 people of working age (15-64)'),
        ('young dependants', 'people aged 0-14 who depend on the working population'),
        ('elderly dependants', 'people aged 65 and over who depend on the working population'),
        ('ageing population', 'a population in which the proportion of people aged 65 and over is increasing'),
        ('youthful population', 'a population with a high proportion of people aged under 15'),
        ('cohort', 'a group of people born in the same period, shown as one bar on a population pyramid'),
    ],
    'mcq': [
        ('A population pyramid with a wide base and a narrow top is typical of', 'an LIC with high birth and death rates', ['an HIC with an ageing population', 'a country with natural decrease', 'a country with very low fertility'], '[1]'),
        ('How is the dependency ratio calculated?', '(population aged 0-14 + 65 and over) ÷ population aged 15-64 × 100', ['population aged 15-64 ÷ total population × 100', '(population aged 0-14) ÷ (population aged 65+) × 100', 'births ÷ deaths × 100'], '[1]'),
        ('A bulge in the 25-40 age groups of males only in a Gulf country such as Qatar is caused by', 'migrant workers', ['a baby boom', 'a war', 'high life expectancy'], '[1]'),
        ('Which country has one of the oldest populations, with about 29% aged 65 and over?', 'Japan', ['Niger', 'Uganda', 'Afghanistan'], '[1]'),
    ],
    'explain': [
        ('Explain the problems of an ageing population for a country.', 'Higher costs of pensions, health care and care homes; fewer workers paying taxes; labour shortages; higher dependency ratio; possible need for migrant workers or a later retirement age.', '1 mark each developed point up to [3]'),
        ('Explain the problems of a youthful population for a country.', 'Need for more schools, teachers and health care for children; future need for jobs and housing; pressure on food and resources; high dependency ratio.', '1 mark each up to [3]'),
        ('Explain why a population pyramid for an HIC has straight, vertical sides.', 'Low birth and death rates mean each cohort is a similar size and most people survive to old age.', '1 mark low rates; 1 mark survival [2]'),
        ('Describe how a country’s population pyramid changes as it passes through the demographic transition.', 'Stage 2: very wide base, narrow concave top; stage 3: base narrows as birth rate falls; stage 4: straight sides; stage 5: base narrower than middle, wider top.', '1 mark each stage change up to [3]'),
    ],
    'claims': [
        ('A high dependency ratio always means a country has many elderly people.', False, 'It may be high because of many young dependants, as in most LICs.'),
        ('The dependency ratio assumes that everyone aged 15-64 is working.', True, 'In reality some are students, unemployed or caring, and many over 65 work, so it is only an estimate.'),
        ('An ageing population can bring benefits as well as problems.', True, 'Older people volunteer, care for grandchildren and spend savings (the “grey economy”).'),
    ],
    'cs': [
        ('a country with an ageing population', [
            ('Japan', {'impacts': 'About 29% of people are aged 65+ and the population has been falling since 2010; rising pension and health costs; labour shortages in care and farming; rural villages emptying; a declining number of taxpayers.',
                       'responses': 'Raising the retirement age; using robots and technology in care homes; encouraging women and older people to work; increased immigration of workers since 2019; incentives to have children.'}),
            ('Italy', {'impacts': 'About 24% aged 65+ and one of the world’s lowest fertility rates (about 1.2); high pension costs; empty villages in the south; shortages of workers.',
                       'responses': 'Pension reforms raising the retirement age to 67; baby bonuses; reliance on migrant care workers; some villages selling houses for €1 to attract residents.'}),
        ], [
            ('describe the problems caused by an ageing population', 'impacts', 'Pensions, health care, workforce, dependency ratio, rural depopulation – with figures.'),
            ('describe how the country is responding to its ageing population', 'responses', 'Retirement age, pensions, immigration, technology, pro-natalist measures.'),
        ]),
    ],
})


@c1b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1b_dep(r, D):
    kind = r.choice(['LIC', 'HIC', 'MIC'])
    if kind == 'LIC':
        y, o = r.randint(38, 48), r.randint(2, 4)
    elif kind == 'HIC':
        y, o = r.randint(12, 17), r.randint(18, 29)
    else:
        y, o = r.randint(22, 30), r.randint(6, 11)
    w = 100 - y - o
    dr = (y + o) / w * 100
    nm = r.choice(['Country P', 'Country Q', 'Country R'])
    stem = f'Fig. 1.2 is a population pyramid for {nm}. It shows that {y}% of the population is aged 0-14, {w}% is aged 15-64 and {o}% is aged 65 and over.'
    if D == 1:
        opts, a = mcq(r, dp(dr), [dp((y + o) / 100 * 100), dp(w / (y + o) * 100), dp(y / w * 100), dp(o / w * 100)])
        return {'stem': stem + ' What is the dependency ratio?', 'options': opts, 'answer': a, 'key': f'({y} + {o}) ÷ {w} × 100 = {dp(dr)}. [1]'}
    parts = [
        lambda r: ('Calculate the dependency ratio.', dp(dr), f'({y} + {o}) ÷ {w} × 100 = {dp(dr)} [2]'),
        lambda r: (f'State whether {nm} is more likely to be an LIC or an HIC. Give two pieces of evidence.', ('LIC: a large proportion of young people (' + str(y) + '%) and few elderly (' + str(o) + '%), showing high birth rates and low life expectancy.') if kind == 'LIC' else
                   ('HIC: few young people (' + str(y) + '%) and many elderly (' + str(o) + '%), showing low birth rates and long life expectancy.') if kind == 'HIC' else
                   ('Probably an MIC/NEE: falling proportion of young (' + str(y) + '%) and a moderate elderly share (' + str(o) + '%).'), '1 mark judgement; 1 mark each piece of evidence [3]'),
        lambda r: ('Describe the likely shape of the pyramid.', 'Wide base narrowing quickly to a small top (triangular).' if kind == 'LIC' else 'Narrow base, straight sides and a wide top.' if kind == 'HIC' else 'Base narrowing, wider in the middle ages, small but growing top.', '[2]'),
        lambda r: ('Explain one problem this population structure may cause.', 'Pressure on schools and future jobs; high young dependency.' if kind == 'LIC' else 'Rising pension and health-care costs with fewer taxpayers.' if kind == 'HIC' else 'Need to create jobs for a large working-age population; future ageing.', '1 mark problem; 1 mark development [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1b.add('C3', (2, 3, 4, 5), 'numerical')
def c1b_cohort(r, D):
    ages = ['0-14', '15-29', '30-44', '45-59', '60-74', '75+']
    m = [r.randint(4, 12) for _ in ages]
    f = [x + r.choice([-1, 0, 1]) for x in m]
    tot = sum(m) + sum(f)
    if tot != 100:
        f[-1] += 100 - tot
    if min(f) <= 0:
        return None
    nm = r.choice(['Country X', 'Country Y'])
    stem = f'Table 1.2 shows the population structure of {nm} (% of total population). ' + ' '.join(f'{a}: males {mm}%, females {ff}%.' for a, mm, ff in zip(ages, m, f))
    young = m[0] + f[0]
    old = m[4] + f[4] + m[5] + f[5]
    work = 100 - young - old
    parts = [
        lambda r: ('Calculate the percentage of the population aged 0-14.', f'{young}%', f'{m[0]} + {f[0]} = {young}% [1]'),
        lambda r: ('Calculate the percentage aged 60 and over.', f'{old}%', f'{m[4]} + {f[4]} + {m[5]} + {f[5]} = {old}% [1]'),
        lambda r: ('Calculate the dependency ratio, treating 15-59 as working age.', dp((young + old) / work * 100), f'({young} + {old}) ÷ {work} × 100 = {dp((young + old) / work * 100)} [2]'),
        lambda r: ('Compare the number of elderly males and females, and suggest a reason.', ('More elderly women than men: women have a higher life expectancy.' if f[5] > m[5] else 'Similar numbers of elderly men and women; usually women live longer, so this may reflect sampling or male migration back to the country.' if f[5] == m[5] else 'More elderly men than women here, which is unusual; it may reflect migration or the effects of rounding.'), '1 mark comparison; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 1.3 over/under-population and policies
c1c = T('Overpopulation, underpopulation and population policies', 'overpopulation underpopulation population policies')
build(c1c, {
    'terms': [
        ('overpopulation', 'when there are too many people for the resources and technology available to maintain a good standard of living'),
        ('underpopulation', 'when there are too few people to use the resources of an area efficiently'),
        ('optimum population', 'the number of people that gives the highest standard of living for the resources and technology available'),
        ('anti-natalist policy', 'a government policy that aims to reduce the birth rate'),
        ('pro-natalist policy', 'a government policy that aims to increase the birth rate'),
        ('carrying capacity', 'the largest population that the resources of an area can support'),
        ('family planning', 'the use of contraception and education to control the number and spacing of children'),
    ],
    'mcq': [
        ('China’s one-child policy began in', '1979', ['1949', '1999', '2015'], 'It was replaced by a two-child policy in 2016 and a three-child policy in 2021. [1]'),
        ('Which country is often given as an example of underpopulation?', 'Australia', ['Bangladesh', 'Haiti', 'Rwanda'], 'Large resources and few people; it encourages skilled immigration. [1]'),
        ('Which is an example of a pro-natalist measure?', 'Paying parents a “baby bonus” for each child', ['Free contraception', 'Fines for large families', 'Raising the legal age of marriage'], '[1]'),
        ('Singapore’s 1970s “Stop at Two” campaign was', 'an anti-natalist policy', ['a pro-natalist policy', 'a migration policy', 'a health policy for the elderly'], 'In 1987 it switched to pro-natalist (“Have three, or more if you can afford it”). [1]'),
    ],
    'explain': [
        ('Explain the difference between overpopulation and underpopulation.', 'Overpopulation: too many people for the resources and technology, leading to shortages and low living standards. Underpopulation: too few people to use resources fully, leading to labour shortages and unused resources.', '1 mark each [2]'),
        ('Explain the effects of China’s one-child policy.', 'Prevented an estimated 200-400 million births and slowed growth; but created an ageing population, a gender imbalance (more males), “4-2-1” families and labour shortages.', '1 mark each effect up to [3]'),
        ('Explain why some countries introduce pro-natalist policies.', 'Low birth rates and an ageing population lead to labour shortages and fewer taxpayers to pay for pensions; the population may decline.', '1 mark problem; 1 mark consequence [2]'),
        ('Describe the signs of overpopulation in an area.', 'Food and water shortages, unemployment, overcrowded housing and informal settlements, pressure on schools and health care, environmental damage.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('Overpopulation only depends on the number of people in a country.', False, 'It depends on the balance between people, resources and technology; a densely populated rich country may not be overpopulated.'),
        ('China’s one-child policy led to a gender imbalance.', True, 'A cultural preference for sons led to more males than females.'),
        ('Pro-natalist policies have always succeeded in raising birth rates.', False, 'Many (e.g. Singapore, South Korea) have had limited success because of high living costs and career pressures.'),
    ],
    'cs': [
        ('a country’s population policy', [
            ('China’s one-child policy', {'policy': 'Introduced in 1979: couples were allowed one child (exceptions for rural families and minorities); rewards such as free education and better housing for one-child families; fines, loss of jobs and forced abortions or sterilisation for some who broke the rule; relaxed to two children in 2016 and three in 2021.',
                                         'evaluate': 'Successful in slowing growth – fertility fell from about 2.8 to 1.7 – and helped economic growth; but it caused an ageing population, a sex ratio of about 117 boys per 100 girls at birth, human rights abuses and future labour shortages.'}),
            ('Singapore’s population policies', {'policy': 'Anti-natalist “Stop at Two” (1972) with free contraception and penalties for third children; then pro-natalist from 1987 (“Have three, or more if you can afford it”) with tax rebates, baby bonuses, longer maternity leave and childcare subsidies.',
                                                'evaluate': 'The first policy worked too well – fertility fell below replacement by 1977; pro-natalist policies have had limited success (fertility about 1.0) because of high costs of housing and education, so Singapore relies on immigration.'}),
        ], [
            ('describe the policy and how it was put into practice', 'policy', 'Aims, measures (rewards, penalties, incentives), dates.'),
            ('evaluate the success of the population policy', 'evaluate', 'Effects on birth/fertility rates, unintended consequences, social impacts, judgement.'),
        ]),
    ],
    'essays': [
        ('anti-natalist policies are the most effective way of reducing rapid population growth',
         ['China’s one-child policy cut fertility quickly.'],
         ['Education of women, better health care (lower infant mortality) and economic development reduce birth rates voluntarily and without abuses, e.g. Kerala, Bangladesh.', 'Coercive policies cause gender imbalance and ageing.'],
         'Development and education are usually more effective and sustainable than strict policies, though family planning programmes help.',
         ['China', 'education of women', 'contraception', 'human rights']),
    ],
})


@c1c.add('C3', (1, 2, 3, 4), 'numerical')
def c1c_res(r, D):
    nm = r.choice(['Country A', 'Country B', 'an island state'])
    pop = r.choice([4, 6, 8, 10, 12, 15])  # millions
    food = r.choice([3, 5, 6, 9, 12, 14, 18])  # millions of people that local food can feed
    water = r.choice([5, 8, 10, 14, 20])  # millions supported by water supply
    lim = min(food, water)
    stem = f'{cap(nm)} has a population of {pop} million. Its farmland can produce enough food for {food} million people and its water supply can support {water} million people.'
    over = pop > lim
    if D == 1:
        opts, a = mcq(r, 'Overpopulated' if over else 'Not overpopulated', ['Not overpopulated' if over else 'Overpopulated', 'Exactly at optimum population', 'It has no population'])
        return {'stem': stem + ' Based on these resources alone, is the country overpopulated?', 'options': opts, 'answer': a, 'key': f'The limiting resource supports {lim} million v population {pop} million. [1]'}
    parts = [
        lambda r: ('Identify the resource that limits the population most.', 'Food' if food < water else 'Water' if water < food else 'Food and water equally', f'Smaller of {food} and {water} million [1]'),
        lambda r: ('State whether the country is overpopulated, using the data.', ('Overpopulated: ' if over else 'Not overpopulated: ') + f'resources support {lim} million and the population is {pop} million.', '1 mark judgement; 1 mark data [2]'),
        lambda r: ('Calculate the surplus or shortfall in people supported by food.', f'{"surplus" if food >= pop else "shortfall"} of {abs(food - pop)} million', f'{food} − {pop} [1]'),
        lambda r: ('Suggest two ways the country could support more people without reducing the population.', 'Importing food; irrigation and higher-yielding crops; desalination or water recycling; reducing waste; trade using other resources.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


# --------------------------------------------------------------- 1.4 density and distribution
c1d = T('Population density and distribution: physical and human factors', 'population density distribution')
build(c1d, {
    'terms': [
        ('population distribution', 'the way people are spread out across an area'),
        ('population density', 'the average number of people per square kilometre'),
        ('densely populated', 'an area with many people per square kilometre'),
        ('sparsely populated', 'an area with few people per square kilometre'),
        ('physical factor', 'a natural feature such as relief, climate, soil or water supply that affects where people live'),
        ('human factor', 'a factor created by people, such as jobs, transport, services or government policy, that affects where people live'),
        ('dot map', 'a map using dots of equal value to show the distribution of people or features'),
    ],
    'mcq': [
        ('How is population density calculated?', 'Total population ÷ area in km²', ['Area ÷ population', 'Births − deaths', 'Population × area'], '[1]'),
        ('Which of these areas is likely to be sparsely populated?', 'The Sahara Desert', ['The Ganges valley', 'The Nile delta', 'The Pearl River delta'], '[1]'),
        ('Which of these is a human factor attracting high population density?', 'Employment in industry and services', ['Flat land', 'Fertile soil', 'Moderate climate'], '[1]'),
        ('About 95% of Egypt’s population lives', 'along the Nile valley and delta', ['in the Western Desert', 'on the Red Sea mountains', 'in Sinai'], '[1]'),
    ],
    'explain': [
        ('Explain why some areas are sparsely populated.', 'Extreme climates (too hot, cold or dry), steep or high relief, poor soils, dense forest, lack of water, few jobs and poor access.', '1 mark each factor with explanation up to [3]'),
        ('Explain why river valleys and deltas are often densely populated.', 'Flat, fertile alluvial soils for farming; water for drinking and irrigation; easy transport routes; ports and trade.', '1 mark each up to [3]'),
        ('Explain why population density is only an average.', 'It divides the total population by area, hiding the fact that people are concentrated in cities and some areas are almost empty.', '1 mark average of whole area; 1 mark hides variation [2]'),
        ('Explain how human factors can attract people to an area with a difficult physical environment.', 'Jobs in mining, oil or tourism, good transport, government investment and services can attract people, e.g. Dubai in the desert or Norilsk in the Arctic.', '1 mark factor; 1 mark example [2]'),
    ],
    'claims': [
        ('Densely populated countries are always poor.', False, 'Singapore and the Netherlands are very densely populated but wealthy.'),
        ('Population distribution is uneven in most countries.', True, 'People cluster in cities, valleys and coastal plains and avoid deserts, mountains and dense forest.'),
        ('Population density is calculated by dividing the area by the population.', False, 'It is the population divided by the area in km².'),
    ],
    'cases': [
        (['Fig. 1.3 describes population density in Brazil. The south-east coast around São Paulo and Rio de Janeiro has over 100 people per km²; the north-east coast 50-100; the interior plateau 10-50; the Amazon basin in the north-west fewer than 5 people per km².',
          'Study Fig. 1.3, a choropleth map of Brazil. Density is highest along the south-east coast (over 100 per km²), lower in the central plateau, and lowest in the Amazon rainforest (under 5 per km²).'],
         [('Describe the distribution of population in Brazil.', 'Uneven: densest on the south-east coast (over 100/km²), moderate on the north-east coast and plateau, sparse in the Amazon (under 5/km²).', '1 mark pattern; 1 mark data [2]'),
          ('Suggest physical reasons why the Amazon basin is sparsely populated.', 'Dense rainforest, hot humid climate, infertile soils, flooding and disease.', '1 mark each up to [3]'),
          ('Suggest human reasons why the south-east coast is densely populated.', 'Jobs in industry and services in São Paulo and Rio; ports and trade; good transport; historical colonial settlement; services and universities.', '1 mark each up to [3]'),
          ('Identify one disadvantage of a choropleth map for showing population density.', 'It suggests density is the same across each whole area and changes suddenly at boundaries.', '[1]')]),
    ],
})


def dd(x):
    return dp(x, 2 if x < 1 else 1)


@c1d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1d_density(r, D):
    regs = [('Region A', r.randint(5, 60) * 100000, r.randint(2, 30) * 1000), ('Region B', r.randint(1, 20) * 100000, r.randint(20, 200) * 1000),
            ('Region C', r.randint(20, 90) * 100000, r.randint(5, 20) * 1000), ('Region D', r.randint(1, 5) * 10000, r.randint(50, 300) * 1000)]
    k = 3 if D <= 2 else 4
    regs = regs[:k]
    dens = [(n, p / a) for n, p, a in regs]
    stem = 'Table 1.3 shows the population and area of regions in a country. ' + ' '.join(f'{n}: population {nf(p)}, area {nf(a)} km².' for n, p, a in regs)
    if D == 1:
        n, p, a = regs[0]
        opts, ans = mcq(r, f'{dd(p / a)} people per km²', [f'{dp(a / p, 3)} people per km²', f'{dp(p / a * 10)} people per km²', f'{dp(p / a / 10)} people per km²'])
        return {'stem': stem + f' What is the population density of {n}?', 'options': opts, 'answer': ans, 'key': f'{nf(p)} ÷ {nf(a)} = {dd(p / a)} per km². [1]'}
    hi = max(dens, key=lambda x: x[1])
    lo = min(dens, key=lambda x: x[1])
    parts = [
        lambda r: ('Calculate the population density of each region.', '; '.join(f'{n} {dd(d)} per km²' for n, d in dens), 'population ÷ area for each; 1 mark for two correct, 2 marks all correct [2]'),
        lambda r: ('Identify the most densely and the most sparsely populated regions.', f'Densest: {hi[0]}; sparsest: {lo[0]}', '1 mark each [2]'),
        lambda r: (f'Suggest physical factors that might explain the low density in {lo[0]}.', 'Mountains or steep slopes; desert or very cold climate; poor soils; dense forest; lack of water.', '1 mark each up to [2]'),
        lambda r: (f'Calculate the overall population density of the country shown.', f'{dp(sum(p for _, p, _ in regs) / sum(a for _, _, a in regs))} per km²', f'{nf(sum(p for _, p, _ in regs))} ÷ {nf(sum(a for _, _, a in regs))} [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 1.5 migration
c1e = T('Migration: types, causes and impacts', 'migration types causes impacts')
build(c1e, {
    'terms': [
        ('migration', 'the movement of people from one place to another to live, for at least a year'),
        ('push factor', 'a reason that makes people want to leave the place where they live'),
        ('pull factor', 'a reason that attracts people to move to a new place'),
        ('refugee', 'a person forced to leave their country because of war, persecution or natural disaster'),
        ('economic migrant', 'a person who moves voluntarily to find work or a better standard of living'),
        ('rural-urban migration', 'the movement of people from the countryside to towns and cities'),
        ('internal migration', 'movement of people within the same country'),
        ('international migration', 'movement of people from one country to another'),
        ('remittances', 'money sent home by migrants to their families'),
        ('net migration', 'the difference between the number of immigrants and the number of emigrants'),
        ('brain drain', 'the emigration of skilled and educated people from a country'),
    ],
    'mcq': [
        ('Which of these is a push factor?', 'Civil war and persecution', ['Better-paid jobs abroad', 'Good schools in the city', 'Family already living in the destination'], '[1]'),
        ('Which of these is forced migration?', 'Syrians fleeing civil war to Turkey', ['A Polish builder moving to the UK for higher wages', 'A retired couple moving to Spain', 'A student moving abroad to study'], '[1]'),
        ('Money sent home by migrants is called', 'remittances', ['tariffs', 'aid', 'taxes'], '[1]'),
        ('A country has 250 000 immigrants and 180 000 emigrants in a year. What is its net migration?', '+70 000', ['−70 000', '+430 000', '+250 000'], 'Immigrants − emigrants. [1]'),
        ('Which country hosted the largest number of Syrian refugees (about 3.5 million at its peak)?', 'Turkey', ['Germany', 'Canada', 'Brazil'], '[1]'),
    ],
    'explain': [
        ('Explain why people migrate from rural areas to cities in LICs.', 'Push: lack of jobs, low farm incomes, drought, few services. Pull: jobs in factories and services, higher wages, schools, health care and the perception of a better life.', '1 mark push; 1 mark pull; 1 mark development [3]'),
        ('Explain the benefits of migration for the country that migrants leave.', 'Remittances support families and the economy; reduced unemployment and pressure on services; returning migrants bring skills and savings.', '1 mark each up to [3]'),
        ('Explain the problems migration can cause for the country that migrants leave.', 'Loss of young, skilled workers (brain drain); ageing and unbalanced population; farms abandoned; families split.', '1 mark each up to [3]'),
        ('Explain the benefits and problems of immigration for a host country.', 'Benefits: fill labour shortages, pay taxes, cultural diversity. Problems: pressure on housing and services, possible tension, lower wages in some jobs.', '1 mark each benefit and problem up to [4]'),
    ],
    'claims': [
        ('Refugees move mainly to find better-paid jobs.', False, 'Refugees are forced to move by war, persecution or disaster; economic migrants move voluntarily for work.'),
        ('Remittances can be an important source of income for LICs.', True, 'In some countries, e.g. Nepal and Tajikistan, they equal a quarter or more of GDP.'),
        ('Most migrants move from HICs to LICs.', False, 'Most international migrants move to HICs or to richer neighbouring countries.'),
    ],
    'cs': [
        ('international migration', [
            ('migration from Mexico to the USA', {'causes': 'Push: low wages (several times lower than in the USA), unemployment, drug-related violence, poverty in rural states such as Oaxaca. Pull: jobs in farming, construction and services in California and Texas; higher wages; family already settled.',
                                                  'impacts': 'USA: fills low-paid jobs in farming and services, but pressure on services and political tension; border wall and patrols. Mexico: remittances of over US$60 billion a year (2023), but loss of young workers from rural areas.'}),
            ('Syrian refugees, 2011 onwards', {'causes': 'Civil war from 2011, bombing of cities such as Aleppo and Homs, persecution and the collapse of services forced over 6 million people to flee abroad and millions more to move within Syria.',
                                               'impacts': 'Turkey hosted about 3.5 million, Lebanon about 1.5 million (a quarter of its population), and Germany about 800 000; pressure on housing, schools and jobs; refugee camps such as Zaatari in Jordan; loss of skilled people from Syria.'}),
            ('migration from Poland to the UK after 2004', {'causes': 'Poland joined the EU in 2004, giving free movement; unemployment in Poland was about 19% and wages were much lower; UK had labour shortages in construction, farming and food processing.',
                                                           'impacts': 'UK: filled labour shortages and paid taxes; some pressure on housing and schools. Poland: remittances; loss of young workers; many returned with skills after 2008 and after Brexit (2016-2020).'}),
        ], [
            ('explain the causes of the migration', 'causes', 'Push and pull factors, economic, social, political, environmental, linked to named places.'),
            ('describe the impacts of the migration on the areas that people leave and the areas they move to', 'impacts', 'Impacts on origin and destination: economic, social, demographic, with figures.'),
        ]),
    ],
    'essays': [
        ('international migration brings more benefits than problems to host countries',
         ['Migrants fill labour shortages, pay taxes, start businesses and support ageing populations (e.g. Polish workers in the UK, migrant workers in the Gulf).'],
         ['Rapid inflows put pressure on housing, schools and health care; tension and exploitation of migrant workers; refugee crises strain poorer host countries such as Lebanon.'],
         'Usually the economic benefits outweigh the problems in the long run, especially for HICs, but sudden refugee flows can overwhelm poorer hosts.',
         ['labour shortages', 'services', 'refugees', 'ageing populations']),
    ],
})


@c1e.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1e_net(r, D):
    nm = r.choice(['Country P', 'Country Q', 'Country R', 'Country S'])
    pop = r.choice([5, 8, 12, 20, 30])  # millions
    imm = r.randint(40, 400) * 1000
    emi = r.randint(40, 400) * 1000
    if imm == emi:
        return None
    br, drt = r.randint(8, 30), r.randint(6, 12)
    net = imm - emi
    nat = (br - drt) * pop * 1000
    total = nat + net
    stem = f'{nm} has a population of {pop} million, a birth rate of {br} per 1000 and a death rate of {drt} per 1000. In one year {nf(imm)} people immigrated and {nf(emi)} emigrated.'
    if D == 1:
        opts, a = mcq(r, f'{"+" if net > 0 else "−"}{nf(abs(net))}', [f'{"−" if net > 0 else "+"}{nf(abs(net))}', f'+{nf(imm + emi)}', f'+{nf(imm)}'])
        return {'stem': stem + ' What was the net migration?', 'options': opts, 'answer': a, 'key': f'{nf(imm)} − {nf(emi)} = {net}. [1]'}
    parts = [
        lambda r: ('Calculate the net migration.', f'{"+" if net > 0 else "−"}{nf(abs(net))}', f'immigrants − emigrants = {nf(imm)} − {nf(emi)} = {"−" if net < 0 else ""}{nf(abs(net))} [1]'),
        lambda r: ('Calculate the natural increase in number of people for the year.', f'{nf(nat)}', f'({br} − {drt}) per 1000 × {pop} 000 000 = {nf(nat)} [2]'),
        lambda r: ('Calculate the total population change for the year.', f'{"+" if total >= 0 else "−"}{nf(abs(total))}', f'natural increase + net migration = {nf(nat)} + ({"−" if net < 0 else ""}{nf(abs(net))}) = {"−" if total < 0 else ""}{nf(abs(total))} [1]'),
        lambda r: ('State whether migration or natural increase contributed more to population change.', ('Natural increase' if abs(nat) > abs(net) else 'Migration') + f' ({nf(abs(nat))} v {nf(abs(net))}).', '[1]'),
        lambda r: ('Suggest one reason why people might emigrate from this country.', 'Lack of jobs or low wages; conflict or persecution; better education or family abroad.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1e.add('C2', (1, 2, 3), 'short')
def c1e_pp(r, D):
    facts = [('drought has destroyed crops for three years', 'push'), ('a new car factory offers well-paid jobs', 'pull'), ('there is civil war in the region', 'push'),
             ('schools and hospitals in the city are better', 'pull'), ('land is being divided between too many family members', 'push'), ('relatives already live in the city and can help', 'pull'),
             ('the government is persecuting religious minorities', 'push'), ('wages are five times higher abroad', 'pull'), ('flooding destroyed the village', 'push'), ('the city offers bright lights and entertainment', 'pull')]
    k = 4 if D <= 2 else 6
    pick = r.sample(facts, k)
    lab = 'ABCDEF'
    stem = f'{person(r)} is considering moving from a rural area to a city. Classify each statement as a push or a pull factor. ' + ' '.join(f'{lab[i]}: {cap(f)}.' for i, (f, _) in enumerate(pick))
    return {'stem': stem, 'answer': '; '.join(f'{lab[i]} {k_}' for i, (_, k_) in enumerate(pick)), 'key': f'1 mark for every two correct [{k // 2}]', 'marks': k // 2, 'type': 'short'}


CHAPTERS[1] = [c1a, c1b, c1c, c1d, c1e]


# ============================================================== CHAPTER 2: Settlement and urbanisation

SITE_FACTORS = [('a wet-point site', 'next to a reliable water supply such as a spring or river'), ('a dry-point site', 'on slightly raised land above a flood plain or marsh'),
                ('a defensive site', 'on a hill or in a meander loop that is easy to defend'), ('a bridging point', 'where a river is narrow or shallow enough to bridge or ford'),
                ('a gap town', 'in a gap through a line of hills, controlling a route'), ('a route centre', 'where several valleys or roads meet'),
                ('a natural harbour', 'on a sheltered coastal inlet with deep water for ships')]

c2a = T('Settlement sites, functions and hierarchies', 'settlement sites functions hierarchies')
build(c2a, {
    'terms': [
        ('site', 'the actual land on which a settlement is built'),
        ('situation', 'the location of a settlement in relation to the surrounding area, such as rivers, routes and other settlements'),
        ('function', 'the main economic activity or purpose of a settlement, such as a port, market town or tourist resort'),
        ('settlement hierarchy', 'the arrangement of settlements in order of size or importance, from isolated dwellings to megacities'),
        ('sphere of influence', 'the area served by a settlement or shop, from which people travel to use its services'),
        ('threshold population', 'the minimum number of people needed to support a service'),
        ('range', 'the maximum distance people are prepared to travel to use a service'),
        ('low-order goods', 'everyday, cheap goods such as bread and newspapers, bought frequently and close to home (convenience goods)'),
        ('high-order goods', 'expensive goods such as furniture and jewellery bought less often, for which people travel further (comparison goods)'),
        ('nucleated settlement', 'a settlement in which buildings are grouped closely around a central point'),
        ('linear settlement', 'a settlement in which buildings are strung out along a road, river or valley'),
        ('dispersed settlement', 'a pattern of isolated buildings spread out across an area'),
    ],
    'mcq': [
        ('Which service has the largest threshold population?', 'A university', ['A post office', 'A village shop', 'A primary school'], '[1]'),
        ('A settlement built on a hill inside a meander loop is most likely to have been chosen as', 'a defensive site', ['a wet-point site', 'a gap town', 'a route centre'], '[1]'),
        ('A settlement whose buildings are strung out along a main road is', 'linear', ['nucleated', 'dispersed', 'a conurbation'], '[1]'),
        ('Which is a high-order good?', 'A television', ['A newspaper', 'A loaf of bread', 'Milk'], '[1]'),
        ('As you move up the settlement hierarchy, the number of settlements', 'decreases while the number of services in each increases', ['increases', 'stays the same', 'decreases and each has fewer services'], '[1]'),
    ],
    'explain': [
        ('Explain the difference between the site and the situation of a settlement.', 'Site is the land the settlement is built on (e.g. a dry-point above a flood plain); situation is its location relative to surrounding features such as routes, rivers and other settlements.', '1 mark each [2]'),
        ('Explain why larger settlements have larger spheres of influence.', 'They have more high-order services with large thresholds and ranges, so people travel further to use them.', '1 mark more high-order services; 1 mark range [2]'),
        ('Explain why the functions of many villages have changed.', 'Farming employs fewer people; commuters and retired people have moved in; second homes and tourism; services such as shops and post offices have closed because of car ownership and online shopping.', '1 mark each up to [3]'),
        ('Explain why low-order services are found in almost every settlement.', 'They have small thresholds and short ranges, so even a small population can support them and people will not travel far for everyday goods.', '1 mark threshold; 1 mark range [2]'),
    ],
    'claims': [
        ('The situation of a settlement describes the land it is built on.', False, 'That is the site; situation is its location relative to surrounding features.'),
        ('A hamlet has more services than a town.', False, 'Hamlets are low in the hierarchy with very few or no services.'),
        ('Many original sites were chosen for water supply, defence or a bridging point.', True, 'These physical advantages mattered most when settlements were founded.'),
    ],
    'cases': [
        (['Fig. 2.1 describes part of a 1:50 000 map. Town M lies at a point where a river is crossed by two main roads; the old centre is on a low hill 20 m above the flood plain; a castle stands on the hill. The river is narrow here and is crossed by an old stone bridge. Railway and roads follow the valley through a gap in a ridge to the north.',
          'Study Fig. 2.1, a description of the site of a market town. The town grew around a castle on a small hill beside a river, at the lowest point where the river could be bridged. Roads from four directions meet at the bridge, and a railway runs through a gap in the hills.'],
         [('Identify three site or situation factors that helped the town to grow.', 'Any three: defensive hill with castle; dry-point site above flood plain; bridging point; route centre where roads meet; gap through the ridge; water supply from the river.', '1 mark each [3]'),
          ('Explain why a bridging point is a good site for a settlement.', 'Routes converge to cross the river, bringing trade and travellers; markets grow there.', '1 mark routes converge; 1 mark trade [2]'),
          ('Suggest two functions the town might have today.', 'Market town; service centre for surrounding villages; tourism (castle); commuter town; light industry.', '1 mark each [2]'),
          ('Explain why the town has a larger sphere of influence than nearby villages.', 'It has more high-order services (supermarkets, secondary school, hospital) and good road links, so people travel further to use it.', '1 mark services; 1 mark accessibility [2]')]),
    ],
})


@c2a.add('C2', (1, 2, 3), 'short')
def c2a_site(r, D):
    name, desc = r.choice(SITE_FACTORS)
    town = r.choice(['A village', 'A town', 'A small city'])
    if D == 1:
        opts, a = mcq(r, cap(name), [cap(n) for n, _ in SITE_FACTORS if n != name])
        return {'stem': f'{town} grew up {desc}. Which type of site is this?', 'options': opts, 'answer': a, 'key': f'{cap(name)}. [1]'}
    why = {'a wet-point site': 'water was needed for drinking, cooking and animals', 'a dry-point site': 'it avoided flooding and marshy ground', 'a defensive site': 'it could be defended against attack',
           'a bridging point': 'routes met to cross the river, bringing trade', 'a gap town': 'it controlled the route through the hills and attracted trade', 'a route centre': 'many routes met, so it was accessible and good for markets',
           'a natural harbour': 'ships could shelter and load, encouraging trade and fishing'}[name]
    return {'stem': f'{town} grew up {desc}. Name this type of site and explain why it was an advantage when the settlement was founded.', 'answer': f'{cap(name)}: {why}.', 'key': '1 mark name; 1 mark explanation [2]', 'marks': 2, 'type': 'explain'}


@c2a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2a_hier(r, D):
    names = ['City', 'Large town', 'Small town', 'Village', 'Hamlet']
    pops = [r.randint(200, 800) * 1000, r.randint(40, 150) * 1000, r.randint(5, 30) * 1000, r.randint(5, 30) * 100, r.randint(2, 9) * 10]
    serv = [r.randint(300, 900), r.randint(120, 280), r.randint(40, 110), r.randint(4, 30), r.randint(0, 3)]
    stem = 'Table 2.1 shows the population and number of services in settlements in one region. ' + ' '.join(f'{n}: population {nf(p)}, {s} services.' for n, p, s in zip(names, pops, serv))
    if D == 1:
        opts, a = mcq(r, 'The more people, the more services', ['The more people, the fewer services', 'No relationship', 'Villages have the most services'])
        return {'stem': stem + ' What relationship does the table show?', 'options': opts, 'answer': a, 'key': 'Positive correlation. [1]'}
    ratio = pops[2] / max(serv[2], 1)
    parts = [
        lambda r: ('Describe the relationship between population and number of services.', f'Positive: the city with {nf(pops[0])} people has {serv[0]} services while the hamlet with {pops[4]} has {serv[4]}.', '1 mark positive; 1 mark data [2]'),
        lambda r: ('Calculate the number of people per service in the small town.', f'about {round(ratio)} people per service', f'{nf(pops[2])} ÷ {serv[2]} = {dp(ratio)} [1]'),
        lambda r: ('Explain why the city has services not found in the small town.', 'High-order services (hospital, university, department stores) have large thresholds that only a large population can support, and people will travel far for them.', '1 mark threshold; 1 mark range [2]'),
        lambda r: ('Suggest a suitable graph to show these data and explain your choice.', 'A scatter graph with logarithmic scales, because both values cover a very wide range and the aim is to show a relationship.', '1 mark scatter; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 2.2 urban land use
c2b = T('Urban land use zones and change in cities', 'urban land use zones change cities')
build(c2b, {
    'terms': [
        ('central business district (CBD)', 'the commercial centre of a city with shops, offices, banks and high land values'),
        ('inner city', 'the zone around the CBD, often with older high-density housing and former industry'),
        ('suburbs', 'the outer residential areas of a city, often with lower-density housing built later'),
        ('rural-urban fringe', 'the zone at the edge of a city where urban and rural land uses mix'),
        ('land value', 'the cost of land, usually highest in the CBD where accessibility is greatest'),
        ('bid-rent theory', 'the idea that land users compete for land, and the price they will pay falls with distance from the centre'),
        ('urban sprawl', 'the uncontrolled spread of a city into the surrounding countryside'),
        ('gentrification', 'the improvement of run-down inner-city housing by wealthier people moving in'),
        ('counter-urbanisation', 'the movement of people from cities to rural areas or small towns'),
        ('brownfield site', 'land that has been built on before and can be redeveloped'),
        ('greenfield site', 'land that has not been built on before, usually on the edge of a city'),
    ],
    'mcq': [
        ('Where are land values usually highest in a city?', 'In the CBD', ['In the suburbs', 'At the rural-urban fringe', 'In the inner city'], 'Greatest accessibility. [1]'),
        ('Why are buildings tallest in the CBD?', 'Land is expensive, so firms build upwards to make the most of a small plot', ['The ground is softer', 'Laws require tall buildings', 'There is no traffic'], '[1]'),
        ('Building a new housing estate on farmland at the edge of a city is development on a', 'greenfield site', ['brownfield site', 'CBD site', 'derelict site'], '[1]'),
        ('Out-of-town retail parks are usually found', 'at the rural-urban fringe near main roads', ['in the CBD', 'in the inner city', 'on brownfield sites in the CBD'], '[1]'),
        ('In many LIC cities, the poorest people often live', 'in informal settlements on the edge of the city', ['in the CBD', 'in high-rise luxury flats', 'in the most accessible central areas'], '[1]'),
    ],
    'explain': [
        ('Explain why land values fall with distance from the CBD.', 'The CBD is the most accessible point, so demand for land from shops and offices is highest; further out accessibility falls, so less is paid and land uses change to housing and then farming.', '1 mark accessibility; 1 mark competition/demand [2]'),
        ('Explain why many CBDs have declined.', 'Out-of-town shopping centres with free parking, online shopping, congestion and high rents in the CBD; offices moving to business parks.', '1 mark each up to [3]'),
        ('Compare land use patterns in cities in HICs and LICs.', 'HICs: wealthy often live in suburbs and the poor in the inner city. LICs: wealthy live near the CBD in high-quality housing; poor live in informal settlements on the edge or on hazardous land.', '1 mark each; 1 mark comparison [3]'),
        ('Explain the advantages and disadvantages of building on brownfield sites.', 'Advantages: reuses derelict land, protects countryside, services already present, regenerates the inner city. Disadvantages: may need costly decontamination and clearance; less space for gardens.', '1 mark each side up to [3]'),
    ],
    'claims': [
        ('Inner-city areas always remain run-down.', False, 'Many have been redeveloped or gentrified, e.g. London Docklands.'),
        ('Rural-urban fringe land is often used for retail parks and business parks.', True, 'Land is cheaper, there is space for parking and good access to main roads.'),
        ('In LIC cities the richest people usually live furthest from the CBD.', False, 'In many LIC cities the wealthy live near the centre, with informal settlements on the edge.'),
    ],
})


@c2b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2b_transect(r, D):
    c = city(r)
    dists = [0, 1, 2, 3, 4, 6, 8]
    base = r.choice([2000, 3000, 4500])
    vals = [round(base * math.exp(-r.uniform(0.35, 0.55) * d) / 10) * 10 for d in dists]
    hts = [r.randint(12, 30), r.randint(6, 10), r.randint(3, 5), r.randint(2, 3), 2, 2, 1]
    vals = sorted(set(vals), reverse=True)
    if len(vals) < len(dists):
        return None
    stem = f'Students carried out a transect from the centre of {c} to its edge. Table 2.2 shows land value ($ per m²) and the mean height of buildings (storeys). ' + ' '.join(f'{d} km: ${v}, {h} storey{"" if h == 1 else "s"}.' for d, v, h in zip(dists, vals, hts))
    if D == 1:
        opts, a = mcq(r, 'Land value decreases with distance from the centre', ['Land value increases with distance from the centre', 'Land value stays the same', 'Land value is highest at 8 km'])
        return {'stem': stem + ' Which statement describes the pattern?', 'options': opts, 'answer': a, 'key': 'Negative correlation. [1]'}
    half = vals[0] / 2
    k = next(i for i, v in enumerate(vals) if v <= half)
    parts = [
        lambda r: ('Describe how land value changes with distance from the centre.', f'Land value falls rapidly from ${vals[0]} at the centre to ${vals[3]} at 3 km, then more slowly to ${vals[-1]} at 8 km.', '1 mark trend; 1 mark change in rate; 1 mark data [3]'),
        lambda r: ('Calculate the percentage fall in land value between 0 km and 2 km.', f'{dp(-pct_change(vals[0], vals[2]))}%', f'({vals[0]} − {vals[2]}) ÷ {vals[0]} × 100 = {dp(-pct_change(vals[0], vals[2]))}% [2]'),
        lambda r: ('State the first distance at which land value is half or less of the value at the centre.', f'{dists[k]} km (${vals[k]})', f'half of {vals[0]} = {fmt(half, 1)} [1]'),
        lambda r: ('Explain the link between land value and building height.', 'Where land is expensive, developers build upwards to fit more floor space on a small plot; where land is cheap, buildings are low and spread out.', '1 mark high value = tall; 1 mark reason [2]'),
        lambda r: ('Name the urban zone found at 0 km and the zone at 8 km.', 'CBD at 0 km; suburbs or rural-urban fringe at 8 km.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c2b.add('C2', (1, 2, 3, 4), 'explain')
def c2b_zone(r, D):
    zs = [('CBD', 'tall office blocks, department stores, banks and very high land values; little housing'),
          ('inner city', 'terraced houses or tenements built in the 19th century close to old factories, with high-density housing'),
          ('suburbs', 'semi-detached and detached houses with gardens, built in the 20th century, with parks and local shopping parades'),
          ('rural-urban fringe', 'a retail park, golf course, new housing estates, a sewage works and farmland near a motorway junction')]
    z, d = r.choice(zs)
    if D == 1:
        opts, a = mcq(r, z if z == 'CBD' else cap(z), [x if x == 'CBD' else cap(x) for x, _ in zs if x != z])
        return {'stem': f'A zone of a city in an HIC has {d}. Which zone is it?', 'options': opts, 'answer': a, 'key': f'{z}. [1]'}
    why = {'CBD': 'it is the most accessible point, so shops and offices outbid other users for expensive land',
           'inner city': 'housing was built close to factories when workers walked to work, before public transport',
           'suburbs': 'public transport and cars allowed people to live further out, where land was cheaper and more space was available',
           'rural-urban fringe': 'land is cheap and plentiful, close to main roads, so space-hungry uses locate there'}[z]
    return {'stem': f'A zone of a city in an HIC has {d}. Identify the zone and explain why these land uses are found there.', 'answer': f'{cap(z) if z != "CBD" else z}: {why}.',
            'key': '1 mark zone; 1 mark land value/accessibility; 1 mark historical or transport reason [3]', 'marks': 3}


# --------------------------------------------------------------- 2.3 rapid urbanisation in LICs
c2c = T('Rapid urbanisation in LICs and the growth of informal settlements', 'rapid urbanisation informal settlements')
build(c2c, {
    'terms': [
        ('urbanisation', 'the increase in the proportion of a country’s population living in towns and cities'),
        ('urban growth', 'the increase in the area or total population of towns and cities'),
        ('megacity', 'a city with a population of more than 10 million'),
        ('informal settlement', 'an area of unplanned, often illegally built housing that lacks basic services (also called a squatter settlement or slum)'),
        ('informal sector', 'jobs that are not officially recognised, taxed or regulated, such as street selling'),
        ('formal sector', 'regular jobs with a contract, a fixed wage and taxes paid'),
        ('site-and-service scheme', 'a scheme in which the government provides plots of land with water, sanitation and electricity for people to build their own homes'),
        ('self-help scheme', 'a scheme in which residents are given materials or loans to improve their own homes'),
    ],
    'mcq': [
        ('What proportion of the world’s population lived in urban areas by about 2020?', 'About 56%', ['About 15%', 'About 30%', 'About 90%'], 'UN estimate; projected to reach about 68% by 2050. [1]'),
        ('Dharavi, one of Asia’s largest informal settlements, is in', 'Mumbai, India', ['Rio de Janeiro, Brazil', 'Nairobi, Kenya', 'Cairo, Egypt'], '[1]'),
        ('Which is the main cause of urban growth in many LIC cities today?', 'Rural-urban migration and high natural increase', ['Counter-urbanisation', 'Low birth rates', 'Out-migration to rural areas'], '[1]'),
        ('Rocinha is a large favela in', 'Rio de Janeiro', ['Mumbai', 'Lagos', 'Lima'], '[1]'),
        ('Informal settlements are often built on', 'steep hillsides, flood plains or next to railways', ['the best land in the CBD', 'protected national parks only', 'land reserved for golf courses'], '[1]'),
    ],
    'explain': [
        ('Explain why informal settlements develop in LIC cities.', 'Rapid rural-urban migration and natural increase create demand for housing that the city cannot meet; migrants are poor and cannot afford formal housing, so they build on unused land on hillsides, flood plains or by railways.', '1 mark rapid growth; 1 mark poverty/cost; 1 mark unused land [3]'),
        ('Describe the problems faced by people living in informal settlements.', 'Overcrowding; lack of clean water and sanitation; disease; fire and flood risk; insecure tenure and eviction; crime; long journeys to work.', '1 mark each up to [3]'),
        ('Explain why urbanisation is happening faster in LICs than HICs.', 'LICs are urbanising rapidly because of rural poverty and high natural increase among young urban populations; HICs are already highly urbanised (about 80%).', '1 mark migration; 1 mark natural increase; 1 mark HICs already urban [3]'),
        ('Explain how self-help schemes improve informal settlements.', 'Residents are given low-cost loans, materials or legal ownership, so they upgrade their own homes with brick walls, water and sanitation; cheap and keeps communities together.', '1 mark how; 1 mark benefit [2]'),
    ],
    'claims': [
        ('Informal settlements have no economic activity.', False, 'Many have thriving informal economies; Dharavi has thousands of small businesses such as recycling, pottery and leatherwork.'),
        ('Most urban growth in LICs now comes from natural increase as well as migration.', True, 'Young migrants have children in the city, so natural increase adds to growth.'),
        ('Clearing informal settlements and building tower blocks always solves the housing problem.', False, 'Clearance breaks up communities and businesses, and rents may be too high for the poor.'),
    ],
    'cs': [
        ('an informal settlement in an LIC or MIC city', [
            ('Dharavi, Mumbai, India', {'conditions': 'About 1 million people in about 2.1 km² – one of the highest densities in the world; many share one toilet between hundreds of people; open drains and water from standpipes for a few hours a day; but an estimated 5000 businesses and 15 000 one-room factories (recycling, pottery, leather, textiles) with output worth over US$600 million a year.',
                                        'manage': 'The Dharavi Redevelopment Project plans to rehouse residents in high-rise blocks with free flats for eligible families and to build commercial space; critics fear loss of businesses and community ties, and many residents are not eligible.'}),
            ('Rocinha, Rio de Janeiro, Brazil', {'conditions': 'Brazil’s largest favela, with about 70 000-100 000 people (estimates vary) on a steep hillside; houses built of brick and concrete by residents; poor sanitation and landslide risk; drug gangs and crime; but many shops, services and a strong community.',
                                                'manage': 'The Favela-Bairro project upgraded favelas with paved roads, water, sewers and health centres; police pacification units (from 2008); a cable car was built in the nearby Complexo do Alemão; results have been mixed because of funding cuts and continuing violence.'}),
            ('Kibera, Nairobi, Kenya', {'conditions': 'Estimates range from about 250 000 to 1 million people; homes made of mud and corrugated iron; few toilets (“flying toilets”), shortages of clean water, high disease rates; informal jobs; residents often rent from absent landlords.',
                                       'manage': 'The Kenya Slum Upgrading Programme built new flats at Soweto East; NGOs provide water kiosks, bio-centre toilets and schools; but many moved residents sub-let flats and returned to Kibera.'}),
        ], [
            ('describe the living conditions in the settlement', 'conditions', 'Housing, density, water and sanitation, health, employment (formal/informal), with figures.'),
            ('evaluate attempts to improve the settlement', 'manage', 'Named schemes (upgrading, rehousing, self-help), what has worked and what has not, judgement.'),
        ]),
    ],
})


@c2c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2c_urb(r, D):
    nm = r.choice(['Country P', 'Country Q', 'Country R'])
    y = [1980, 2000, 2020]
    tot = [r.randint(20, 40), 0, 0]
    tot[1] = round(tot[0] * r.uniform(1.4, 1.8))
    tot[2] = round(tot[1] * r.uniform(1.3, 1.6))
    up = [r.randint(15, 30), 0, 0]
    up[1] = up[0] + r.randint(8, 15)
    up[2] = up[1] + r.randint(8, 15)
    urb = [round(t * p / 100, 1) for t, p in zip(tot, up)]
    stem = f'Table 2.3 shows population data for {nm}. ' + ' '.join(f'{yy}: total population {t} million, {p}% urban.' for yy, t, p in zip(y, tot, up))
    if D == 1:
        opts, a = mcq(r, f'{fmt(urb[2], 2)} million', [f'{up[2]} million', f'{fmt(urb[1], 1)} million', f'{fmt(tot[2] - urb[2], 1)} million', f'{tot[2]} million'])
        return {'stem': stem + ' How many people lived in urban areas in 2020?', 'options': opts, 'answer': a, 'key': f'{tot[2]} × {up[2]}% = {fmt(urb[2], 2)} million. [1]'}
    gr = pct_change(urb[0], urb[2])
    parts = [
        lambda r: ('Calculate the urban population in 1980 and in 2020.', f'1980: {fmt(urb[0], 2)} million; 2020: {fmt(urb[2], 2)} million', f'{tot[0]} × {up[0]}% and {tot[2]} × {up[2]}% [2]'),
        lambda r: ('Calculate the percentage increase in urban population from 1980 to 2020.', f'{dp(gr)}%', f'({fmt(urb[2], 2)} − {fmt(urb[0], 2)}) ÷ {fmt(urb[0], 2)} × 100 = {dp(gr)}% [2]'),
        lambda r: ('Explain the difference between urbanisation and urban growth, using the data.', f'Urbanisation is the rise in the urban share ({up[0]}% to {up[2]}%); urban growth is the rise in the number of urban people ({fmt(urb[0], 2)} to {fmt(urb[2], 2)} million).', '1 mark each with data [2]'),
        lambda r: ('Suggest two reasons for the changes shown.', 'Rural-urban migration (push: poverty, lack of services; pull: jobs, services) and high natural increase in cities.', '1 mark each [2]'),
        lambda r: ('Describe two problems that rapid urban growth may cause.', 'Informal settlements, shortage of housing, water and sanitation, traffic congestion, air pollution, unemployment and informal jobs.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 2.4 urban problems and solutions
c2d = T('Urban problems and sustainable solutions in HICs and LICs', 'urban problems sustainable solutions')
build(c2d, {
    'terms': [
        ('traffic congestion', 'when there are too many vehicles for the road space, causing slow journeys'),
        ('sustainable city', 'a city that meets the needs of its people today without harming the environment or the ability of future generations to meet their needs'),
        ('bus rapid transit (BRT)', 'a public transport system using bus-only lanes and stations to give fast, frequent services'),
        ('congestion charge', 'a fee that drivers pay to enter a busy city centre at certain times'),
        ('park and ride', 'a scheme in which people park cars on the edge of a city and take a bus or tram to the centre'),
        ('green belt', 'an area of protected open land around a city where building is restricted'),
        ('urban regeneration', 'improving run-down urban areas by redeveloping buildings, infrastructure and the economy'),
        ('urban heat island', 'the effect by which a city is warmer than the surrounding countryside'),
    ],
    'mcq': [
        ('Which city is famous for its bus rapid transit system, introduced in 1974?', 'Curitiba, Brazil', ['London, UK', 'Dubai, UAE', 'Kathmandu, Nepal'], '[1]'),
        ('London introduced a congestion charge in', '2003', ['1963', '1993', '2023'], '[1]'),
        ('What is the main purpose of a green belt?', 'To stop urban sprawl into the countryside', ['To build new factories', 'To increase traffic', 'To grow cities faster'], '[1]'),
        ('Which of these helps to reduce air pollution in a city?', 'Electric buses and cycle lanes', ['More car parks in the centre', 'Burning waste in the open', 'Building new motorways into the CBD'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of traffic congestion in cities.', 'Rising car ownership; many people commuting into the CBD at the same times; narrow old streets; poor or overcrowded public transport; road works and deliveries.', '1 mark each up to [3]'),
        ('Explain how a bus rapid transit system can make a city more sustainable.', 'Dedicated lanes make buses fast and reliable, encouraging people to leave cars at home; fewer cars reduce congestion, fuel use and air pollution; cheap fares help the poor reach jobs.', '1 mark how; 1 mark environmental benefit; 1 mark social benefit [3]'),
        ('Explain why air pollution is a serious problem in many LIC and MIC cities.', 'Rapid growth in old, poorly maintained vehicles; factories with few controls; burning of waste and fuels for cooking; weak enforcement; in some cities the relief traps smog.', '1 mark each up to [3]'),
        ('Explain the causes of the urban heat island effect.', 'Concrete and tarmac absorb heat by day and release it at night; heat from buildings, vehicles and industry; fewer plants mean less evapotranspiration; pollution traps heat.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('Building more roads always solves traffic congestion.', False, 'New roads often attract more traffic (induced demand); public transport and demand management are often more effective.'),
        ('Recycling and waste reduction help make cities more sustainable.', True, 'They save resources, energy and landfill space.'),
        ('Urban problems only occur in LIC cities.', False, 'HIC cities also have congestion, pollution, housing shortages and inequality.'),
    ],
    'cs': [
        ('a sustainable urban scheme', [
            ('Curitiba, Brazil', {'scheme': 'A bus rapid transit system (from 1974) with dedicated lanes and “tube” stations carries over 1 million passengers a day; parks on flood-prone land; a “green exchange” in which poor residents swap recyclable waste for food or bus tickets; about 70% of waste recycled; pedestrianised centre.',
                                  'evaluate': 'Lower car use and pollution than other Brazilian cities, more green space and cheap transport for the poor; but the BRT has become overcrowded as the city has grown to about 1.9 million, and informal settlements still exist on the edge.'}),
            ('London, UK', {'scheme': 'Congestion charge (2003) and Ultra Low Emission Zone (2019, expanded 2023); Oyster cards and an extensive Underground, bus and Overground network; cycle hire and superhighways; brownfield regeneration at Docklands and the Olympic Park in Stratford.',
                            'evaluate': 'Traffic in the charging zone fell by about 30% at first and air quality has improved; but congestion has returned because of delivery vans and taxis, and the charge is criticised as unfair to low-income drivers.'}),
        ], [
            ('describe the strategies used to make the city more sustainable', 'scheme', 'Transport, waste, green space, housing, energy – with named schemes and figures.'),
            ('evaluate how successful the strategies have been', 'evaluate', 'Evidence of success and of continuing problems; judgement.'),
        ]),
    ],
    'essays': [
        ('the problems of cities in LICs are more serious than the problems of cities in HICs',
         ['LIC cities face informal settlements, lack of clean water and sanitation, disease and rapid unplanned growth (e.g. Kibera, Dharavi).'],
         ['HIC cities have serious congestion, air pollution, homelessness, inequality and ageing infrastructure.', 'Some LIC/MIC cities (Curitiba) have found sustainable solutions.'],
         'Problems in LIC cities are generally more severe because of their speed of growth and lack of money, but HIC cities also face major challenges.',
         ['informal settlements', 'pollution', 'transport', 'funding']),
    ],
})


@c2d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2d_traffic(r, D):
    c = city(r)
    times = ['07:00', '08:00', '09:00', '10:00', '12:00', '14:00', '16:00', '17:00', '18:00']
    peak = r.randint(900, 1600)
    v = [round(peak * f) for f in (r.uniform(.5, .6), 1.0, r.uniform(.7, .8), r.uniform(.4, .5), r.uniform(.45, .55), r.uniform(.4, .5), r.uniform(.6, .7), r.uniform(.9, .98), r.uniform(.7, .8))]
    stem = f'A traffic count was carried out on a main road into the centre of {c}. Vehicles per hour: ' + ', '.join(f'{t} {x}' for t, x in zip(times, v)) + '.'
    if D == 1:
        opts, a = mcq(r, '08:00', ['12:00', '14:00', '10:00'])
        return {'stem': stem + ' At what time was traffic heaviest?', 'options': opts, 'answer': a, 'key': f'08:00 ({v[1]} vehicles). [1]'}
    parts = [
        lambda r: ('Describe the pattern of traffic through the day.', f'Two peaks: morning at 08:00 ({v[1]}) and evening at 17:00 ({v[7]}); lowest in the middle of the day ({min(v[3:6])}).', '1 mark two peaks; 1 mark data [2]'),
        lambda r: ('Calculate the mean number of vehicles per hour.', f'{dp(mean(v))}', f'{sum(v)} ÷ {len(v)} = {dp(mean(v))} [2]'),
        lambda r: ('Explain the pattern.', 'Commuters travel into the city for work and school in the morning and leave in the evening rush hour; fewer journeys during the day.', '1 mark commuting; 1 mark timing [2]'),
        lambda r: ('Suggest two strategies the city could use to reduce peak congestion.', 'Bus lanes or BRT; park and ride; congestion charge; staggered working hours or home working; cycle lanes.', '1 mark each [2]'),
        lambda r: ('Suggest how the reliability of the count could be improved.', 'Count on several different days and in different seasons, using the same length of count and site each time; use more than one counter.', '1 mark each up to [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


CHAPTERS[2] = [c2a, c2b, c2c, c2d]


# ============================================================== CHAPTER 3: Development

DEV = [  # name, GNI per capita US$ (approx, recent), life expectancy, HDI (approx)
    ('Norway', 95000, 83, 0.97), ('UK', 49000, 81, 0.94), ('Japan', 42000, 84, 0.92), ('Brazil', 9000, 76, 0.76), ('India', 2400, 70, 0.64),
    ('Bangladesh', 2700, 73, 0.67), ('Kenya', 2100, 63, 0.60), ('Nigeria', 2100, 54, 0.55), ('Niger', 600, 62, 0.39), ('Mexico', 11000, 75, 0.78), ('China', 13000, 78, 0.79)]

c3a = T('Indicators of development: GNI per capita, HDI and others', 'indicators of development gni hdi')
build(c3a, {
    'terms': [
        ('development', 'the progress of a country in improving the economy, living standards, health, education and freedom of its people'),
        ('gross national income (GNI) per capita', 'the total value of goods and services produced by a country plus income from abroad, divided by its population'),
        ('Human Development Index (HDI)', 'a composite measure of development from 0 to 1 combining life expectancy, years of schooling and GNI per capita'),
        ('purchasing power parity (PPP)', 'an adjustment to income figures that takes account of differences in the cost of living between countries'),
        ('literacy rate', 'the percentage of adults who can read and write'),
        ('infant mortality rate', 'the number of babies who die before their first birthday per 1000 live births'),
        ('HIC', 'a high-income country, with GNI per capita above about US$14 000 (World Bank)'),
        ('LIC', 'a low-income country, with GNI per capita below about US$1100 (World Bank)'),
        ('composite indicator', 'a measure that combines several indicators into one value, such as the HDI'),
    ],
    'mcq': [
        ('Which three measures are combined to calculate the HDI?', 'Life expectancy, education and GNI per capita', ['Birth rate, death rate and GDP', 'Literacy, car ownership and doctors per person', 'Population density, exports and imports'], '[1]'),
        ('Which country has one of the highest HDI values?', 'Norway', ['Niger', 'Chad', 'Haiti'], '[1]'),
        ('Why is the HDI often considered a better measure of development than GNI per capita alone?', 'It combines social and economic measures', ['It only measures wealth', 'It is always higher', 'It ignores health'], '[1]'),
        ('Which of these would you expect to fall as a country develops?', 'Infant mortality rate', ['Life expectancy', 'Literacy rate', 'GNI per capita'], '[1]'),
        ('GNI per capita figures are often adjusted for PPP because', 'the cost of living differs between countries', ['populations differ', 'exchange rates are fixed', 'it makes all countries equal'], '[1]'),
    ],
    'explain': [
        ('Explain why GNI per capita is not a perfect measure of development.', 'It is an average that hides inequality within a country; ignores the informal economy and subsistence farming; ignores quality of life such as health, education and freedom; affected by exchange rates.', '1 mark each up to [3]'),
        ('Explain why life expectancy is higher in HICs than in LICs.', 'Better health care, clean water and sanitation, better diet, vaccinations and safer working conditions.', '1 mark each up to [3]'),
        ('Explain how an increase in literacy can help a country develop.', 'Literate people can get better-paid skilled jobs, understand health information, start businesses and take part in decisions, raising productivity and incomes.', '1 mark each up to [2]'),
        ('Explain why a composite indicator such as the HDI gives a better picture of development.', 'It combines economic (income) and social (health, education) measures, so a country that is rich but has poor health or education is not ranked too highly.', '1 mark combines; 1 mark example/reason [2]'),
    ],
    'claims': [
        ('A country with a high GNI per capita always has a high quality of life for everyone.', False, 'GNI is an average; wealth may be very unevenly distributed and social measures may be poor.'),
        ('The HDI has a maximum value of 1.', True, 'It runs from 0 to 1; Norway and Switzerland score about 0.96-0.97.'),
        ('Infant mortality is usually higher in LICs than in HICs.', True, 'Poor health care, nutrition and sanitation cause more infant deaths.'),
    ],
})


@c3a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3a_table(r, D):
    rows = r.sample(DEV, 5 if D >= 3 else 4)
    stem = 'Table 3.1 shows development indicators for selected countries. ' + ' '.join(f'{n}: GNI per capita US${nf(g)}, life expectancy {l} years, HDI {fmt(h, 2)}.' for n, g, l, h in rows)
    hi = max(rows, key=lambda x: x[1])
    lo = min(rows, key=lambda x: x[1])
    if D == 1:
        opts, a = mcq(r, hi[0], [x[0] for x in rows if x[0] != hi[0]])
        return {'stem': stem + ' Which country has the highest GNI per capita?', 'options': opts, 'answer': a, 'key': f'{hi[0]}: US${nf(hi[1])}. [1]'}
    ratio = hi[1] / lo[1]
    byg = sorted(rows, key=lambda x: x[1])
    exc = [byg[i][0] for i in range(1, len(byg)) if byg[i][2] < byg[i - 1][2]]
    parts = [
        lambda r: ('Calculate how many times greater the highest GNI per capita is than the lowest.', f'{dp(ratio)} times', f'{nf(hi[1])} ÷ {nf(lo[1])} = {dp(ratio)} [2]'),
        lambda r: ('Describe the relationship between GNI per capita and life expectancy shown in Table 3.1.', 'Positive: countries with higher GNI per capita generally have higher life expectancy' + (f', though {exc[0]} is an exception.' if exc else '.'), '1 mark relationship; 1 mark data/exception [2]'),
        lambda r: ('Rank the countries by HDI from highest to lowest.', ', '.join(x[0] for x in sorted(rows, key=lambda x: -x[3])), '[1]'),
        lambda r: ('Suggest why a country may have a high GNI per capita but a lower life expectancy than expected.', 'Wealth is unequally distributed, little spent on health care, poor diet or lifestyle diseases, conflict or high HIV rates.', '1 mark each up to [2]'),
        lambda r: ('Suggest one other indicator that could be added to the table, and explain why.', 'Literacy rate, infant mortality, access to clean water or doctors per 1000 people – each shows social development not measured by income.', '1 mark indicator; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c3a.add('C3', (2, 3, 4, 5), 'numerical')
def c3a_spear(r, D):
    rows = r.sample(DEV, 6)
    n = len(rows)
    def ranks(vals):
        order = sorted(range(n), key=lambda i: -vals[i])
        rk = [0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk
    g = [x[1] for x in rows]
    l = [x[2] for x in rows]
    rg, rl = ranks(g), ranks(l)
    d2 = sum((a - b) ** 2 for a, b in zip(rg, rl))
    rs = 1 - 6 * d2 / (n * (n * n - 1))
    stem = 'A student tests the hypothesis “Countries with higher GNI per capita have higher life expectancy.” using six countries: ' + ' '.join(f'{x[0]}: US${nf(x[1])}, {x[2]} years.' for x in rows)
    parts = [
        lambda r: ('Rank the countries for GNI per capita and for life expectancy (1 = highest).', '; '.join(f'{x[0]} {fmt(a, 1)}/{fmt(b, 1)}' for x, a, b in zip(rows, rg, rl)), '1 mark each correct set of ranks (tied values share the mean rank) [2]'),
        lambda r: ('Calculate Spearman’s rank correlation coefficient using rs = 1 − 6Σd² ÷ (n³ − n).', f'rs = {fmt(round(rs, 2), 2)}', f'Σd² = {fmt(d2, 2)}; 1 − 6 × {fmt(d2, 2)} ÷ ({n}³ − {n}) = {fmt(round(rs, 2), 2)} [3]'),
        lambda r: ('State what the result shows about the hypothesis.', ('A strong positive correlation, so the hypothesis is supported.' if rs >= 0.7 else 'A weak to moderate positive correlation, so the hypothesis is only partly supported.' if rs > 0.3 else 'Little or no positive correlation, so the hypothesis is not supported.'), '1 mark interpretation linked to value [1]'),
        lambda r: ('Explain why a sample of six countries limits the conclusion.', 'A small sample may not be representative and the result could be due to chance; more countries from each income group are needed.', '1 mark small/unrepresentative; 1 mark improvement [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 3.2 inequality
c3b = T('Inequalities between and within countries', 'inequalities between within countries')
build(c3b, {
    'terms': [
        ('development gap', 'the widening difference in wealth and quality of life between the richest and poorest countries'),
        ('core region', 'a wealthy, economically advanced area of a country, often around the capital or main ports'),
        ('periphery', 'a poorer, often remote area of a country with less investment and lower incomes'),
        ('regional inequality', 'differences in wealth and quality of life between regions of the same country'),
        ('Gini coefficient', 'a measure of inequality of income from 0 (perfect equality) to 1 (one person has all income)'),
        ('fair trade', 'a system that guarantees producers in LICs a fair price and better working conditions'),
        ('bilateral aid', 'aid given directly from one government to another'),
        ('multilateral aid', 'aid given by many countries through an international organisation such as the World Bank'),
        ('microfinance', 'small loans to people on low incomes, often to start a small business'),
    ],
    'mcq': [
        ('Which region of Brazil is the wealthy core?', 'The south-east (São Paulo and Rio de Janeiro)', ['The north (Amazonas)', 'The north-east (Bahia, Maranhão)', 'The far west'], '[1]'),
        ('A Gini coefficient of 0.63 compared with 0.25 shows', 'greater income inequality', ['less inequality', 'higher GNI per capita', 'higher HDI'], 'South Africa has one of the highest Gini coefficients (about 0.63). [1]'),
        ('Which is an example of a physical cause of uneven development?', 'A landlocked location far from ports', ['Corruption', 'Civil war', 'Unfair trade rules'], '[1]'),
        ('The Grameen Bank in Bangladesh is known for', 'microfinance loans, mainly to women', ['building dams', 'oil exports', 'running factories for TNCs'], '[1]'),
    ],
    'explain': [
        ('Explain why there are inequalities within countries.', 'Core regions attract investment, jobs, services and skilled migrants (cumulative causation), while the periphery is remote, has poor infrastructure and loses young people; physical factors such as climate and relief also matter.', '1 mark core advantages; 1 mark periphery problems; 1 mark process [3]'),
        ('Explain how colonial history can help explain the development gap.', 'Colonies exported raw materials cheaply and imported manufactured goods; infrastructure was built for export, not development; borders and conflicts left after independence.', '1 mark each up to [3]'),
        ('Explain how fair trade helps to reduce inequality.', 'Farmers receive a guaranteed minimum price and a premium for community projects such as schools and clean water; better working conditions and stable incomes.', '1 mark price; 1 mark premium/community [2]'),
        ('Explain why debt can slow development.', 'Money spent repaying loans and interest cannot be spent on health, education and infrastructure.', '1 mark repayment; 1 mark opportunity cost [2]'),
    ],
    'claims': [
        ('Inequality only exists between countries, not within them.', False, 'Regions within countries differ greatly, e.g. south-east and north-east Brazil.'),
        ('Aid can sometimes increase dependency.', True, 'Long-term aid may discourage local production or tie countries to donors’ goods and policies.'),
        ('Landlocked countries often face extra barriers to development.', True, 'They depend on neighbours for access to ports, raising transport costs for trade.'),
    ],
    'essays': [
        ('aid is the most effective way to reduce the development gap',
         ['Emergency and long-term aid can fund health, education and infrastructure; debt relief frees money for services.'],
         ['Fair trade, investment by TNCs, good governance and microfinance can be more sustainable; aid may be misused or create dependency.'],
         'Aid helps most when targeted and combined with fair trade and investment; on its own it is rarely enough.',
         ['types of aid', 'fair trade', 'debt', 'investment']),
    ],
    'cs': [
        ('regional inequality within a country', [
            ('Brazil', {'pattern': 'The south-east (São Paulo, Rio) produces over half of Brazil’s GDP; GNI per capita there is about three times that of the north-east (e.g. Maranhão); life expectancy and literacy are lower in the north-east; the Amazon north is sparsely populated with few services.',
                        'causes': 'Colonial ports and coffee wealth in the south-east; industry and TNC investment concentrated near São Paulo; drought and poor soils in the north-east sertão; remoteness and rainforest in the north; migration of young people to the south-east.'}),
            ('India', {'pattern': 'States such as Kerala and Maharashtra have higher income, literacy and life expectancy; states such as Bihar and Uttar Pradesh have lower incomes and literacy; Mumbai and Bengaluru attract investment.',
                       'causes': 'Investment in ports and IT in western and southern states; better education and health spending in Kerala; high population density and reliance on farming in Bihar; poor infrastructure in rural states.'}),
        ], [
            ('describe the pattern of inequality', 'pattern', 'Core and periphery regions named, with income/health/education figures.'),
            ('explain why there are differences in development between regions', 'causes', 'Physical, historical, economic and social causes, cumulative causation.'),
        ]),
    ],
})


@c3b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3b_reg(r, D):
    regs = ['North', 'North-east', 'Centre', 'South-east', 'South']
    inc = [r.randint(3, 8) * 1000, r.randint(2, 6) * 1000, r.randint(6, 12) * 1000, r.randint(14, 22) * 1000, r.randint(10, 16) * 1000]
    lit = [r.randint(80, 90), r.randint(78, 88), r.randint(88, 94), r.randint(94, 98), r.randint(93, 97)]
    nm = r.choice(['Country P', 'a large MIC', 'an emerging economy'])
    stem = f'Table 3.2 shows mean income per person (US$) and adult literacy (%) by region in {nm}. ' + ' '.join(f'{g}: ${nf(i)}, {l}%.' for g, i, l in zip(regs, inc, lit))
    hi, lo = inc.index(max(inc)), inc.index(min(inc))
    if D == 1:
        opts, a = mcq(r, regs[hi], [x for x in regs if x != regs[hi]])
        return {'stem': stem + ' Which region is most likely to be the core region?', 'options': opts, 'answer': a, 'key': f'{regs[hi]}: highest income (${nf(inc[hi])}). [1]'}
    parts = [
        lambda r: ('Calculate the difference in income between the richest and poorest regions.', f'${nf(inc[hi] - inc[lo])}', f'{nf(inc[hi])} − {nf(inc[lo])} [1]'),
        lambda r: ('Calculate how many times greater income is in the richest region than the poorest.', f'{dp(inc[hi] / inc[lo])} times', f'{nf(inc[hi])} ÷ {nf(inc[lo])} [1]'),
        lambda r: ('Describe the relationship between income and literacy.', 'Generally positive: regions with higher income have higher literacy.', '1 mark relationship; 1 mark data [2]'),
        lambda r: ('Suggest why the core region is wealthier.', 'Ports, industry and services concentrated there; investment by TNCs and government; better infrastructure and education attract more investment (cumulative causation).', '1 mark each up to [3]'),
        lambda r: ('Suggest two ways the government could reduce the inequality.', 'Invest in roads, schools and health in poorer regions; tax incentives for firms to locate there; new capital or growth poles; cash-transfer schemes.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 3.3 employment structure
c3c = T('Employment structure and the sectors of industry', 'employment structure sectors of industry')
build(c3c, {
    'terms': [
        ('primary sector', 'jobs that extract raw materials from the land or sea, such as farming, fishing, forestry and mining'),
        ('secondary sector', 'jobs that process raw materials or make manufactured goods, such as car assembly'),
        ('tertiary sector', 'jobs that provide services, such as teaching, health care, retail and transport'),
        ('quaternary sector', 'jobs in research, information and high technology, such as software development and scientific research'),
        ('employment structure', 'the percentage of the workforce employed in each sector of the economy'),
        ('deindustrialisation', 'the decline of manufacturing industry in a country or region'),
        ('Clark-Fisher model', 'a model showing how employment shifts from primary to secondary and then to tertiary and quaternary as a country develops'),
        ('mechanisation', 'the replacement of human or animal labour by machines'),
    ],
    'mcq': [
        ('A software engineer developing artificial intelligence works in the', 'quaternary sector', ['primary sector', 'secondary sector', 'informal primary sector'], '[1]'),
        ('Which country is most likely to have over 60% of its workers in the primary sector?', 'Niger', ['UK', 'Japan', 'Singapore'], '[1]'),
        ('Which type of graph is used to plot employment in three sectors that add up to 100%?', 'Triangular graph', ['Climate graph', 'Wind rose', 'Population pyramid'], '[1]'),
        ('Why has primary employment fallen in HICs?', 'Mechanisation and cheaper imports', ['Population decline only', 'Higher wages in farming', 'More rainfall'], '[1]'),
    ],
    'explain': [
        ('Explain how employment structure changes as a country develops.', 'In LICs most work in the primary sector (farming); industrialisation increases secondary jobs; in HICs mechanisation and deindustrialisation reduce primary and secondary jobs, and most work in tertiary and quaternary services.', '1 mark each stage up to [3]'),
        ('Explain why manufacturing has grown in many NEEs such as China and Vietnam.', 'Cheap, plentiful labour; government incentives and special economic zones; investment by TNCs; improving infrastructure and ports; growing domestic markets.', '1 mark each up to [3]'),
        ('Explain why the tertiary sector grows as incomes rise.', 'People can afford more services such as leisure, tourism, health care and education; governments spend more on services.', '1 mark income; 1 mark demand for services [2]'),
        ('Explain the effects of deindustrialisation on a region.', 'Unemployment, loss of skills, derelict factories and land, out-migration of young people, decline of local shops and services.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('All tertiary jobs are low-paid.', False, 'The tertiary sector includes highly paid jobs such as doctors and lawyers as well as low-paid ones.'),
        ('Mechanisation reduces the number of workers needed in farming.', True, 'Machines do work that many labourers did, so primary employment falls.'),
        ('The quaternary sector is usually largest in LICs.', False, 'It is largest in HICs with well-educated workforces and research investment.'),
    ],
})


@c3c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3c_struct(r, D):
    kind = r.choice(['LIC', 'NEE', 'HIC'])
    if kind == 'LIC':
        p, s = r.randint(55, 75), r.randint(8, 15)
    elif kind == 'NEE':
        p, s = r.randint(20, 35), r.randint(25, 35)
    else:
        p, s = r.randint(1, 4), r.randint(15, 22)
    t = 100 - p - s
    nm = r.choice(['Country P', 'Country Q', 'Country R'])
    stem = f'In {nm}, {p}% of workers are employed in the primary sector and {s}% in the secondary sector. The rest work in the tertiary (and quaternary) sector.'
    if D == 1:
        opts, a = mcq(r, f'{t}%', [f'{p + s}%', f'{100 - p}%', f'{100 - s}%', f'{t + 10}%'])
        return {'stem': stem + ' What percentage work in the tertiary sector?', 'options': opts, 'answer': a, 'key': f'100 − {p} − {s} = {t}%. [1]'}
    workforce = r.choice([2, 5, 8, 12, 20])
    parts = [
        lambda r: ('Calculate the percentage employed in the tertiary sector.', f'{t}%', f'100 − {p} − {s} = {t}% [1]'),
        lambda r: (f'The workforce is {workforce} million. Calculate how many people work in the primary sector.', f'{fmt(workforce * p / 100, 2)} million', f'{workforce} × {p}% = {fmt(workforce * p / 100, 2)} million [1]'),
        lambda r: ('Is this country most likely to be an LIC, an NEE or an HIC? Give a reason.', {'LIC': f'LIC: most workers ({p}%) are in farming and few in industry.', 'NEE': f'NEE: a large secondary sector ({s}%) as industry grows, with primary falling ({p}%).', 'HIC': f'HIC: very few in primary ({p}%) and most in services ({t}%).'}[kind], '1 mark judgement; 1 mark use of data [2]'),
        lambda r: ('Explain how the employment structure may change in the next 30 years.', {'LIC': 'Primary share will fall as farming is mechanised and people move to cities; secondary and tertiary will grow with industrialisation and investment.',
                                                                                           'NEE': 'Secondary may peak then fall as wages rise and automation increases; tertiary and quaternary will grow.',
                                                                                           'HIC': 'Further growth of tertiary and quaternary jobs (digital, research); secondary continues to decline with automation and offshoring.'}[kind], '1 mark change; 1 mark reason [2]'),
        lambda r: ('Describe how these data would be plotted on a triangular graph.', 'Each side is a 0-100% scale for one sector; read primary, secondary and tertiary along their gridlines; the point where the three lines meet is plotted.', '1 mark three axes; 1 mark plotting point [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 3.4 globalisation and TNCs
c3d = T('Globalisation and transnational corporations: benefits and problems', 'globalisation transnational corporations')
build(c3d, {
    'terms': [
        ('globalisation', 'the increasing links and interdependence between countries through trade, investment, communication and culture'),
        ('transnational corporation (TNC)', 'a large company that operates in more than one country, often with headquarters in an HIC'),
        ('foreign direct investment (FDI)', 'investment by a company in another country, such as building a factory'),
        ('outsourcing', 'contracting work out to another company, often in another country with lower costs'),
        ('supply chain', 'the network of companies and places involved in producing and delivering a product'),
        ('export processing zone', 'an area with tax breaks and few regulations set up to attract foreign manufacturing for export'),
        ('multiplier effect', 'when an initial investment creates further jobs and income in related businesses (a knock-on effect)'),
        ('profit leakage', 'when profits made by a TNC leave the host country and return to its headquarters abroad'),
    ],
    'mcq': [
        ('Why do many TNCs locate factories in countries such as Vietnam and Bangladesh?', 'Lower labour costs', ['Higher wages', 'Stricter environmental laws', 'Colder climate'], '[1]'),
        ('Where are TNC headquarters usually located?', 'In HICs, near major cities', ['In remote rural areas of LICs', 'On offshore islands only', 'In the countries where products are sold most cheaply'], '[1]'),
        ('Which development has most helped globalisation since the 1990s?', 'The internet and cheaper communications', ['The decline of shipping', 'Higher trade barriers', 'Fewer airports'], '[1]'),
        ('The 2013 Rana Plaza factory collapse, which killed over 1100 garment workers, happened in', 'Bangladesh', ['India', 'Vietnam', 'Mexico'], '[1]'),
    ],
    'explain': [
        ('Explain the advantages TNCs can bring to host countries.', 'Jobs and regular wages; training and skills; investment in infrastructure; taxes; export earnings; a multiplier effect on local suppliers.', '1 mark each up to [3]'),
        ('Explain the disadvantages TNCs can bring to host countries.', 'Low wages and poor working conditions; profits leave the country; environmental pollution; local firms cannot compete; jobs can be lost if the TNC relocates.', '1 mark each up to [3]'),
        ('Explain why globalisation has increased.', 'Container shipping and air freight; the internet and telecommunications; trade agreements reducing tariffs; growth of TNCs and FDI; global finance.', '1 mark each up to [3]'),
        ('Explain what is meant by a global supply chain, using an example.', 'Different stages of production happen in different countries, e.g. a smartphone designed in the USA, with parts from South Korea and Japan, assembled in China or Vietnam and sold worldwide.', '1 mark meaning; 1 mark example [2]'),
    ],
    'claims': [
        ('TNCs only bring benefits to LICs.', False, 'They create jobs but can pay low wages, cause pollution and send profits abroad.'),
        ('Globalisation has increased trade between countries.', True, 'Lower tariffs, cheap shipping and the internet have increased world trade greatly.'),
        ('A TNC may close a factory if costs rise.', True, 'TNCs are “footloose” and may move production to cheaper locations.'),
    ],
    'cs': [
        ('a transnational corporation (TNC)', [
            ('Nike', {'operations': 'Headquarters in Oregon, USA, where design, research and marketing take place; shoes and clothing made by about 500 contract factories in about 35 countries employing about 1 million workers, mainly in Vietnam, China and Indonesia.',
                      'impacts': 'Benefits: jobs, wages higher than farm incomes, training and export earnings for Vietnam. Problems: criticism of low wages, long hours and poor conditions in contract factories (1990s), profits returned to the USA, factories may move to cheaper countries; Nike has since published factory lists and codes of conduct.'}),
            ('Samsung in Vietnam', {'operations': 'South Korean TNC; huge smartphone factories at Bac Ninh and Thai Nguyen in northern Vietnam since 2008, employing over 100 000 workers; Samsung accounts for about a fifth of Vietnam’s exports.',
                                    'impacts': 'Benefits: jobs, skills, infrastructure and a multiplier effect on local suppliers; export earnings. Problems: long hours, heavy reliance on one company, most profits and high-value parts remain in South Korea, environmental concerns.'}),
            ('Toyota in the UK', {'operations': 'Japanese TNC with a car factory at Burnaston near Derby (opened 1992) and an engine plant in Deeside, Wales; employs about 2500-3000 people directly and supports many local suppliers; cars exported mainly to Europe.',
                                  'impacts': 'Benefits: skilled jobs, investment in a region that lost traditional industry, multiplier effect, exports. Problems: profits return to Japan; the plant depends on trade rules (Brexit created uncertainty); greenfield site lost farmland.'}),
        ], [
            ('describe how the TNC operates in different countries', 'operations', 'Headquarters, research, manufacturing locations, workforce, global supply chain.'),
            ('evaluate the impacts of the TNC on the host country', 'impacts', 'Economic, social and environmental advantages and disadvantages with a judgement.'),
        ]),
    ],
    'essays': [
        ('the benefits of TNCs for host countries outweigh the problems',
         ['TNCs bring jobs, wages, skills, infrastructure and export earnings (e.g. Samsung in Vietnam); the multiplier effect helps local firms.'],
         ['Low wages and poor conditions (Rana Plaza 2013); profit leakage; pollution; dependence on footloose investment.'],
         'For many NEEs the benefits have outweighed the problems, provided governments regulate working conditions and the environment.',
         ['jobs and wages', 'working conditions', 'profits', 'environment']),
    ],
})


@c3d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3d_chain(r, D):
    price = r.choice([80, 100, 120, 150])
    shares = {'retailer': r.choice([35, 40, 45]), 'brand (TNC) profit and marketing': r.choice([20, 25, 30]), 'materials': r.choice([10, 12, 15]), 'transport and taxes': r.choice([8, 10])}
    shares['factory workers’ wages'] = 100 - sum(shares.values())
    if shares['factory workers’ wages'] <= 0:
        return None
    w = shares['factory workers’ wages']
    stem = f'Fig. 3.1 shows how the US${price} price of a pair of trainers made in Vietnam is shared: ' + ', '.join(f'{k} {v}%' for k, v in shares.items()) + '.'
    if D == 1:
        opts, a = mcq(r, f'US${fmt(price * w / 100, 2)}', [f'US${fmt(price * shares["retailer"] / 100, 2)}', f'US${w}', f'US${fmt(price * w / 10, 2)}', f'US${fmt(price * (w + 5) / 100, 2)}', f'US${fmt(price * w / 1000, 2)}'])
        return {'stem': stem + ' How much of the price goes to factory workers’ wages?', 'options': opts, 'answer': a, 'key': f'{w}% of {price} = {fmt(price * w / 100, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the amount paid to factory workers.', f'US${fmt(price * w / 100, 2)}', f'{w}% × {price} [1]'),
        lambda r: ('Calculate how many times more the retailer receives than the factory workers.', f'{dp(shares["retailer"] / w)} times', f'{shares["retailer"]} ÷ {w} [1]'),
        lambda r: ('Suggest why so little of the price goes to the workers.', 'Labour is cheap and plentiful in Vietnam; workers have little bargaining power; most value is added by design, branding and retailing in HICs.', '1 mark each up to [2]'),
        lambda r: ('Explain one benefit and one problem for Vietnam of making trainers for a TNC.', 'Benefit: jobs and regular wages, export earnings, skills. Problem: low wages and long hours, profits go abroad, factories could move to cheaper countries.', '1 mark each with development [4]'),
        lambda r: ('Suggest a suitable way of presenting these data.', 'A pie chart or divided bar, because the data are parts of a whole adding to 100%.', '1 mark technique; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


CHAPTERS[3] = [c3a, c3b, c3c, c3d]


# ============================================================== CHAPTER 4: Economic activity

FARMS = [
    ('a rice farm in the Ganges delta, Bangladesh', 'intensive subsistence arable', ['monsoon rain', 'flat, fertile alluvial soil', 'family labour', 'buffalo for ploughing', 'seeds'], ['ploughing', 'transplanting seedlings', 'weeding', 'harvesting by hand'], ['rice for the family', 'small surplus sold at market', 'straw for fuel']),
    ('a commercial wheat farm in East Anglia, UK', 'extensive commercial arable', ['flat land', 'fertile soil', 'machinery', 'fertilisers and pesticides', 'capital'], ['ploughing', 'drilling seed', 'spraying', 'combine harvesting'], ['wheat sold to mills', 'straw', 'profit']),
    ('a cattle ranch in the Pampas, Argentina', 'extensive commercial pastoral', ['large areas of grassland', 'cattle', 'few workers', 'capital'], ['grazing', 'rounding up', 'veterinary care', 'transport to market'], ['beef', 'leather', 'profit']),
    ('a tea estate in the Kenyan highlands', 'plantation (commercial)', ['reliable rainfall', 'well-drained slopes', 'cheap labour', 'capital from a large company'], ['planting', 'pruning', 'picking leaves by hand', 'drying and processing'], ['tea for export', 'jobs', 'profit for the company']),
    ('a Maasai herding family in southern Kenya', 'nomadic pastoral (subsistence)', ['grassland', 'cattle and goats', 'family labour', 'water holes'], ['moving herds with the seasons', 'milking', 'protecting animals'], ['milk, meat and blood for the family', 'animals traded']),
]

c4a = T('Agricultural systems: inputs, processes and outputs', 'agricultural systems inputs processes outputs')
build(c4a, {
    'terms': [
        ('farming system', 'a farm seen as a system with inputs, processes and outputs'),
        ('subsistence farming', 'farming to produce food for the farmer’s own family, with little or nothing left to sell'),
        ('commercial farming', 'farming to produce crops or animals for sale at a profit'),
        ('arable farming', 'growing crops'),
        ('pastoral farming', 'rearing animals'),
        ('mixed farming', 'growing crops and rearing animals on the same farm'),
        ('intensive farming', 'farming with high inputs of labour or capital per hectare to give high yields from a small area'),
        ('extensive farming', 'farming with low inputs per hectare over a large area'),
        ('irrigation', 'artificially supplying water to crops'),
        ('yield', 'the amount of crop produced per hectare'),
    ],
    'mcq': [
        ('Which of these is a physical input to a farm?', 'Rainfall', ['Machinery', 'Labour', 'Subsidies'], '[1]'),
        ('Which of these is a process on a farm?', 'Harvesting', ['Seeds', 'Milk sold', 'Sunshine'], '[1]'),
        ('Rice growing in the Ganges delta is an example of', 'intensive subsistence farming', ['extensive commercial farming', 'nomadic herding', 'plantation forestry'], '[1]'),
        ('Why is rice grown in flooded paddy fields in Bangladesh?', 'Monsoon rain and river floods provide the standing water rice needs', ['Rice needs frost', 'The soil is too dry for any other crop', 'Paddy fields keep pests away completely'], '[1]'),
        ('A farm that produces 18 tonnes of maize from 4 hectares has a yield of', '4.5 tonnes per hectare', ['72 tonnes per hectare', '0.22 tonnes per hectare', '22 tonnes per hectare'], '18 ÷ 4 = 4.5 t/ha. [1]'),
    ],
    'explain': [
        ('Explain the difference between intensive and extensive farming.', 'Intensive farming uses large inputs of labour or capital on a small area to get high yields per hectare; extensive farming uses low inputs over large areas, with lower yields per hectare.', '1 mark each [2]'),
        ('Explain how physical factors affect the type of farming in an area.', 'Climate (temperature, rainfall, growing season), relief and slope, and soil fertility and drainage determine which crops can grow and whether machinery can be used.', '1 mark each factor with explanation up to [3]'),
        ('Explain how human factors affect farming decisions.', 'Access to markets and transport, capital for machinery and fertiliser, government subsidies and policies, land ownership, labour supply and technology.', '1 mark each up to [3]'),
        ('Explain why irrigation is needed in many farming areas.', 'Rainfall is too low or unreliable, or falls in the wrong season; irrigation allows crops to grow, increases yields and allows more than one crop per year.', '1 mark low/unreliable rain; 1 mark benefit [2]'),
    ],
    'claims': [
        ('Subsistence farmers never sell any of their produce.', False, 'Most produce is eaten by the family, but small surpluses are often sold at local markets.'),
        ('Subsidies are a human input to farming.', True, 'They are money from governments that affects what farmers grow.'),
        ('Extensive farms always have high yields per hectare.', False, 'Extensive farms have low inputs and lower yields per hectare, although total output may be large.'),
    ],
    'cs': [
        ('a farming system', [
            ('rice farming in the Ganges delta, Bangladesh', {'system': 'Inputs: monsoon rain (over 2000 mm), high temperatures, flat alluvial soils renewed by floods, family labour, buffalo, seed; processes: ploughing, flooding paddy fields, transplanting seedlings by hand, weeding, harvesting; outputs: two or three rice crops a year, mostly eaten by the family, with some sold; intensive subsistence.',
                                                              'factors': 'Physical: monsoon rainfall and flooding, hot climate for a long growing season, fertile silt, flat land. Human: high population density and small plots, cheap family labour, limited capital, high-yielding varieties and irrigation pumps in some areas.'}),
            ('commercial arable farming in East Anglia, UK', {'system': 'Inputs: flat land, fertile loam soils, about 600 mm rain, sunny summers, capital, machinery, fertilisers, pesticides, few workers; processes: ploughing, drilling, spraying, combine harvesting, storage; outputs: wheat, barley, sugar beet and oilseed rape sold for profit; extensive commercial with high yields.',
                                                             'factors': 'Physical: flat land for machinery, fertile soils, dry sunny summers for ripening. Human: large farms, capital, government subsidies, good transport to markets and processing factories.'}),
        ], [
            ('describe the inputs, processes and outputs of the farming system', 'system', 'Physical and human inputs, processes, outputs, classification of the system.'),
            ('explain how physical and human factors influence the farming system', 'factors', 'Climate, relief, soil; labour, capital, markets, technology, government.'),
        ]),
    ],
})


@c4a.add('C2', (1, 2, 3, 4), 'explain')
def c4a_sys(r, D):
    farm, typ, ins, procs, outs = r.choice(FARMS)
    items = [(x, 'input') for x in ins] + [(x, 'process') for x in procs] + [(x, 'output') for x in outs]
    k = 4 if D <= 2 else 6
    pick = r.sample(items, k)
    if len({p[1] for p in pick}) < 3 and D > 2:
        return None
    lab = 'ABCDEF'
    stem = f'The following refer to {farm}. Classify each as an input, a process or an output' + (', and name the type of farming system.' if D >= 3 else '.') + ' ' + ' '.join(f'{lab[i]}: {cap(x)}.' for i, (x, _) in enumerate(pick))
    mk = k // 2 + (1 if D >= 3 else 0)
    return {'stem': stem, 'answer': '; '.join(f'{lab[i]} {c}' for i, (_, c) in enumerate(pick)) + (f'. Type: {typ}.' if D >= 3 else '.'),
            'key': '1 mark for every two correct classifications' + ('; 1 mark farming type' if D >= 3 else '') + f' [{mk}]', 'marks': mk, 'type': 'short' if D <= 2 else 'explain'}


@c4a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4a_yield(r, D):
    crop = r.choice(['rice', 'maize', 'wheat', 'potatoes'])
    ha1, ha2 = r.choice([2, 3, 4, 5, 8]), r.choice([1, 1.5, 2, 2.5])
    y1 = r.choice([2, 2.5, 3, 3.5, 4]) * ha1
    y2 = r.choice([5, 6, 7, 8]) * ha2
    f1, f2 = r.sample(['Farm A', 'Farm B', 'Farm C'], 2)
    stem = f'{f1} grows {fmt(y1, 1)} tonnes of {crop} on {fmt(ha1, 1)} hectares without irrigation. {f2} grows {fmt(y2, 1)} tonnes on {fmt(ha2, 1)} hectares using irrigation, high-yielding seeds and fertiliser.'
    a, b = y1 / ha1, y2 / ha2
    if D == 1:
        opts, ans = mcq(r, f'{fmt(a, 2)} t/ha', [f'{fmt(ha1 / y1, 2)} t/ha', f'{fmt(y1 * ha1, 1)} t/ha', f'{fmt(a * 2, 2)} t/ha'])
        return {'stem': stem + f' What is the yield of {f1}?', 'options': opts, 'answer': ans, 'key': f'{fmt(y1, 1)} ÷ {fmt(ha1, 1)} = {fmt(a, 2)} t/ha. [1]'}
    parts = [
        lambda r: ('Calculate the yield per hectare for each farm.', f'{f1}: {fmt(a, 2)} t/ha; {f2}: {fmt(b, 2)} t/ha', f'tonnes ÷ hectares [2]'),
        lambda r: (f'Calculate the percentage by which the yield of {f2} is greater than that of {f1}.', f'{dp(pct_change(a, b))}%', f'({fmt(b, 2)} − {fmt(a, 2)}) ÷ {fmt(a, 2)} × 100 [2]'),
        lambda r: (f'Explain why {f2} has a higher yield.', 'Irrigation provides reliable water; high-yielding varieties produce more grain; fertiliser adds nutrients – this is intensive, capital-based farming.', '1 mark each input explained up to [3]'),
        lambda r: (f'Suggest two problems {f2} might face from using these methods.', 'High costs and debt; fertiliser and pesticide pollution of water; salinisation from irrigation; lowering of the water table.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 4.2 food shortages
c4b = T('Food shortages: causes, impacts and solutions', 'food shortages causes impacts solutions')
build(c4b, {
    'terms': [
        ('food security', 'when all people at all times have access to enough safe, nutritious food'),
        ('food insecurity', 'when people do not have reliable access to enough affordable, nutritious food'),
        ('famine', 'a widespread, severe shortage of food causing hunger and death'),
        ('malnutrition', 'ill health caused by a diet lacking the right amount of nutrients'),
        ('undernutrition', 'not having enough food or calories to meet the body’s needs'),
        ('Green Revolution', 'the use of high-yielding varieties, irrigation, fertilisers and pesticides from the 1960s to increase crop yields in LICs'),
        ('high-yielding varieties (HYVs)', 'crop varieties bred to produce much more grain per hectare'),
        ('food aid', 'food given to countries or people facing shortages'),
        ('appropriate technology', 'technology suited to the needs, skills and wealth of local people, such as hand pumps or drip irrigation'),
    ],
    'mcq': [
        ('Which of these is a natural cause of food shortages?', 'Drought', ['Civil war', 'Low world crop prices', 'Poor transport'], '[1]'),
        ('The Green Revolution was most successful in', 'the Punjab region of India', ['the Sahara Desert', 'Antarctica', 'the Amazon rainforest'], '[1]'),
        ('About how many calories per day does an adult need on average?', 'About 2000-2500', ['About 500', 'About 10 000', 'About 1000'], '[1]'),
        ('Which is an example of appropriate technology for increasing food supply?', 'Small-scale drip irrigation using local materials', ['A large mechanised farm with GPS tractors', 'A nuclear power plant', 'A six-lane motorway'], '[1]'),
    ],
    'explain': [
        ('Explain the natural causes of food shortages.', 'Drought and unreliable rainfall; floods; pests such as locusts; crop diseases; soil erosion; tropical storms.', '1 mark each with explanation up to [3]'),
        ('Explain the human causes of food shortages.', 'War and conflict disrupt farming and transport; poverty; rapid population growth; poor infrastructure and storage; growing cash crops for export instead of food; high food prices.', '1 mark each up to [3]'),
        ('Explain the impacts of food shortages on people.', 'Malnutrition and stunted growth in children; disease; lower ability to work and learn; migration; social unrest; death in famine.', '1 mark each up to [3]'),
        ('Explain the advantages and disadvantages of the Green Revolution.', 'Advantages: much higher yields, more food, fewer famines (India became self-sufficient in grain). Disadvantages: costly seeds and fertiliser led to debt for poor farmers; pollution; falling water tables; loss of crop variety.', '1 mark each side up to [4]'),
    ],
    'claims': [
        ('Food shortages are caused only by drought.', False, 'Conflict, poverty, poor transport and storage, and population growth are also major causes.'),
        ('Food aid is useful in emergencies but can harm local farmers if it continues for too long.', True, 'Free food can lower local prices and discourage farmers from producing.'),
        ('The world produces enough food for everyone, yet many people are hungry.', True, 'Hunger is mainly caused by poverty, waste, conflict and unequal distribution.'),
    ],
    'cs': [
        ('a food shortage in a country or region', [
            ('the Horn of Africa (Somalia and Ethiopia), 2020-2023', {'causes': 'Five failed rainy seasons in a row (the worst drought in about 40 years); locust swarms in 2020; conflict in Somalia and northern Ethiopia (Tigray); rising world food prices after the war in Ukraine; poverty and reliance on rain-fed farming and herding.',
                                                                    'impacts': 'Millions of livestock died; over 20 million people faced acute food insecurity; child malnutrition rose sharply; over a million people were displaced; disease outbreaks such as cholera.',
                                                                    'solutions': 'Emergency food and cash aid from the World Food Programme and NGOs; feeding centres for malnourished children; longer-term water harvesting, drought-resistant crops and livestock insurance schemes.'}),
            ('the Sahel (e.g. Niger)', {'causes': 'Low and unreliable rainfall, drought, desertification and soil erosion, rapid population growth (fertility about 6.7), poverty, poor infrastructure and conflict in the region.',
                                       'impacts': 'Frequent food crises (2005, 2010, 2012); high child malnutrition and stunting; migration to cities and abroad; loss of livestock.',
                                       'solutions': 'Food aid and cash transfers; farmer-managed natural regeneration of trees; zaï pits and stone lines to conserve water; drought-tolerant millet and sorghum; the Great Green Wall initiative.'}),
        ], [
            ('explain the causes of the food shortage', 'causes', 'Physical and human causes with named detail.'),
            ('describe the impacts of the food shortage', 'impacts', 'Health, economic, social and demographic impacts with figures.'),
            ('evaluate attempts to reduce the food shortage', 'solutions', 'Short-term aid and long-term solutions; strengths and limitations.'),
        ]),
    ],
    'essays': [
        ('increasing food production is the best way to solve food shortages',
         ['The Green Revolution greatly increased yields in Asia; irrigation and HYVs reduce dependence on rain.'],
         ['Many shortages are caused by poverty, conflict, waste and poor distribution rather than lack of food.', 'Reducing waste, improving storage, transport, incomes and peace may be more effective; higher production can harm the environment.'],
         'Higher production helps, but tackling poverty, conflict, waste and access to food is usually more important.',
         ['Green Revolution', 'conflict', 'food waste', 'poverty']),
    ],
})


@c4b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4b_cal(r, D):
    cs = r.sample(['Country P', 'Country Q', 'Country R', 'Country S', 'Country T'], 4)
    cal = [r.randint(17, 36) * 100 for _ in cs]
    need = 2300
    stem = f'Table 4.1 shows the average daily calorie intake per person in four countries. ' + ' '.join(f'{c}: {nf(x)} kcal.' for c, x in zip(cs, cal)) + f' The recommended average intake is {nf(need)} kcal per person per day.'
    below = [c for c, x in zip(cs, cal) if x < need]
    if D == 1:
        opts, a = mcq(r, str(len(below)), [str(x) for x in range(5) if x != len(below)])
        return {'stem': stem + ' How many of these countries are below the recommended intake?', 'options': opts, 'answer': a, 'key': f'{", ".join(below) or "none"}. [1]'}
    lo = min(cal)
    parts = [
        lambda r: ('Identify the countries with an intake below the recommended level.', ', '.join(below) if below else 'None', '[1]'),
        lambda r: ('Calculate the shortfall of the lowest country as a percentage of the recommended intake.', (f'{dp((need - lo) / need * 100)}% below' if lo < need else 'No shortfall'), f'({need} − {lo}) ÷ {need} × 100 [2]'),
        lambda r: ('Calculate the mean calorie intake of the four countries.', f'{dp(mean(cal))} kcal', f'{sum(cal)} ÷ 4 [1]'),
        lambda r: ('Suggest why a national average may hide food insecurity.', 'Richer people may eat much more than the poor; rural and conflict areas may have far less; seasonal shortages are hidden.', '1 mark each up to [2]'),
        lambda r: ('Describe two effects of a diet below the recommended level.', 'Undernutrition and weight loss; stunted growth in children; weakened immunity and disease; tiredness reducing ability to work and study.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 4.3 industry location
c4c = T('Industrial systems and factors affecting the location of industry', 'industrial systems location of industry')
build(c4c, {
    'terms': [
        ('industrial system', 'an industry seen as a system with inputs (raw materials, labour, energy, capital), processes (manufacturing) and outputs (products, waste)'),
        ('raw material', 'a natural material used to make a product, such as iron ore or timber'),
        ('footloose industry', 'an industry that is not tied to raw materials and can locate in many places, such as electronics'),
        ('high-technology industry', 'an industry that uses advanced technology and research, such as computing and biotechnology'),
        ('science park', 'a group of high-technology firms located near a university to share research and skilled workers'),
        ('agglomeration', 'the clustering of related industries in one area so that they benefit from shared services and suppliers'),
        ('market', 'the place or people who buy the product'),
        ('greenfield site', 'land that has not been built on before, often on the edge of a town'),
        ('heavy industry', 'industry using large amounts of bulky raw materials and energy, such as steel making'),
    ],
    'mcq': [
        ('Why do high-technology industries often locate near universities?', 'To recruit skilled graduates and share research', ['To be near coalfields', 'Because land is most expensive there', 'To be near the sea for raw materials'], '[1]'),
        ('Which factor was most important for the location of early iron and steel works?', 'Nearness to coal and iron ore', ['Nearness to universities', 'Pleasant environment', 'Fast broadband'], '[1]'),
        ('Bengaluru in India is a major centre for', 'information technology and software', ['coal mining', 'rice farming', 'shipbuilding only'], '[1]'),
        ('A footloose industry is one that', 'is not tied to raw materials and can locate in many places', ['must be next to a coalfield', 'only locates in rural areas', 'cannot move once built'], '[1]'),
    ],
    'explain': [
        ('Explain why high-technology firms locate in science parks.', 'Near universities for research links and graduates; attractive environment for skilled workers; good motorway and airport access; sharing of ideas and services with other firms (agglomeration).', '1 mark each up to [3]'),
        ('Explain how the factors affecting industrial location have changed over time.', 'Early industry was tied to raw materials and power (coal); now transport, communications and electricity let footloose firms locate near markets, skilled labour and pleasant environments, or abroad where labour is cheap.', '1 mark past; 1 mark present; 1 mark reason [3]'),
        ('Explain why governments offer incentives to attract industry.', 'To create jobs, reduce regional inequality, encourage a multiplier effect and earn tax and export income.', '1 mark each up to [2]'),
        ('Explain the possible environmental impacts of a new factory.', 'Air and water pollution, noise and traffic, loss of farmland or habitats on a greenfield site, waste disposal; but modern factories may use cleaner technology.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('All industries must be located near their raw materials.', False, 'Footloose industries such as electronics can locate in many places; markets and labour are often more important.'),
        ('Agglomeration can reduce costs for firms.', True, 'Firms share suppliers, skilled labour, services and ideas.'),
        ('High-tech industries often prefer pleasant environments near motorways and airports.', True, 'These attract skilled workers and allow fast travel and distribution.'),
    ],
    'cs': [
        ('an industrial zone or high-technology industry', [
            ('Bengaluru, India (information technology)', {'factors': 'Large supply of English-speaking graduates from universities and institutes such as the Indian Institute of Science; government support from the 1980s and Electronics City and technology parks; lower wages than in HICs; time difference with the USA allowing 24-hour working; pleasant climate at about 900 m.',
                                                         'impacts': 'Hundreds of thousands of IT jobs and firms such as Infosys and Wipro; a growing middle class; but traffic congestion, water shortages, rising house prices and growth of informal settlements.'}),
            ('Cambridge Science Park, UK', {'factors': 'Founded by Trinity College in 1970; close links with the University of Cambridge for research and graduates; attractive landscaped site; access to the M11 and to London and Stansted Airport; clustering of biotech and computing firms.',
                                            'impacts': 'Thousands of skilled jobs; a cluster of over 100 firms and spin-offs; high house prices and congestion in Cambridge; pressure to build on green belt land.'}),
        ], [
            ('explain the factors that have influenced the location of the industry', 'factors', 'Labour/skills, research links, government, transport, environment, markets.'),
            ('describe the impacts of the industry on the local area', 'impacts', 'Jobs, multiplier effect, congestion, housing, environment.'),
        ]),
    ],
})


@c4c.add('C3', (2, 3, 4, 5), 'case')
def c4c_site(r, D):
    ind = r.choice(['a car assembly plant', 'a high-technology electronics firm', 'a steel works', 'a food-processing factory'])
    sites = {
        'Site A': 'next to a motorway junction on the edge of a city, flat greenfield land, 10 km from a university',
        'Site B': 'beside a deep-water port with rail links, on cheap reclaimed land far from housing',
        'Site C': 'in the city centre on a small brownfield plot with narrow streets and high land values',
    }
    best = {'a car assembly plant': 'Site A', 'a high-technology electronics firm': 'Site A', 'a steel works': 'Site B', 'a food-processing factory': 'Site A'}[ind]
    why = {'a car assembly plant': 'large flat site for a big factory; motorway access for parts (just-in-time) and distributing cars to markets',
           'a high-technology electronics firm': 'near a university for skilled graduates and research; motorway access; attractive greenfield environment',
           'a steel works': 'imported iron ore and coal arrive by sea; heavy bulky raw materials; space for a large plant away from housing because of pollution',
           'a food-processing factory': 'good road access to farms and supermarkets; flat land for the factory and lorries'}[ind]
    stem = f'A company wants to build {ind}. Fig. 4.2 describes three possible sites. ' + ' '.join(f'{k}: {v}.' for k, v in sites.items())
    parts = [
        lambda r: ('Choose the best site and justify your choice.', f'{best}: {why}.', '1 mark site; 2 marks justification [3]'),
        lambda r: ('Explain why Site C would be unsuitable.', 'Small plot with no room to expand; expensive land; congestion in narrow streets makes deliveries slow.', '1 mark each up to [2]'),
        lambda r: ('Describe the inputs and outputs of this industrial system.', 'Inputs: raw materials or components, labour, energy, capital, land. Outputs: finished products, waste, profit.', '1 mark inputs; 1 mark outputs [2]'),
        lambda r: ('Suggest how local people might react to the new factory.', 'Support: new jobs and income, multiplier effect. Oppose: noise, traffic, pollution, loss of open land.', '1 mark each side [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c4c.add('C2', (1, 2, 3), 'short')
def c4c_class(r, D):
    jobs = [('a coal miner in Australia', 'primary'), ('a worker assembling cars in Slovakia', 'secondary'), ('a nurse in Toronto', 'tertiary'), ('a software researcher developing AI in Bengaluru', 'quaternary'),
            ('a fisherman in Peru', 'primary'), ('a steel worker in South Korea', 'secondary'), ('a hotel receptionist in the Maldives', 'tertiary'), ('a scientist researching vaccines in Cambridge', 'quaternary'),
            ('a tea picker in Kenya', 'primary'), ('a textile machinist in Bangladesh', 'secondary'), ('a teacher in Lima', 'tertiary'), ('a forester in Canada', 'primary')]
    k = 4 if D <= 2 else 5
    pick = r.sample(jobs, k)
    lab = 'ABCDE'
    stem = 'Classify each job into the primary, secondary, tertiary or quaternary sector. ' + ' '.join(f'{lab[i]}: {cap(j)}.' for i, (j, _) in enumerate(pick))
    return {'stem': stem, 'answer': '; '.join(f'{lab[i]} {s}' for i, (_, s) in enumerate(pick)), 'key': f'1 mark for every two correct [{k // 2}]', 'marks': k // 2, 'type': 'short'}


# --------------------------------------------------------------- 4.4 tourism
c4d = T('Growth of tourism: benefits, problems and sustainable tourism', 'growth of tourism sustainable tourism')
build(c4d, {
    'terms': [
        ('mass tourism', 'large numbers of tourists visiting the same destination, often on package holidays'),
        ('ecotourism', 'small-scale tourism that conserves the environment and benefits local people'),
        ('sustainable tourism', 'tourism that meets the needs of visitors and hosts without damaging the environment or culture for the future'),
        ('honeypot site', 'a place of special interest that attracts large numbers of tourists'),
        ('carrying capacity', 'the maximum number of visitors a place can take without unacceptable damage'),
        ('leakage', 'the proportion of tourist spending that leaves the host country, for example to foreign tour operators and hotel chains'),
        ('package holiday', 'a holiday in which travel and accommodation are sold together at one price'),
    ],
    'mcq': [
        ('Which of these has most helped the growth of international tourism?', 'Cheaper air travel and budget airlines', ['Shorter paid holidays', 'Higher fuel prices', 'Fewer airports'], '[1]'),
        ('Money from tourism that leaves the host country is called', 'leakage', ['remittance', 'aid', 'subsidy'], '[1]'),
        ('Which is an example of ecotourism?', 'Staying in a locally owned lodge in a rainforest reserve with a local guide', ['A large all-inclusive resort owned by a foreign chain', 'A cruise ship visit for a few hours', 'A theme park in a city'], '[1]'),
        ('The Maasai Mara National Reserve, a major safari destination, is in', 'Kenya', ['Brazil', 'Thailand', 'Iceland'], '[1]'),
    ],
    'explain': [
        ('Explain why international tourism has grown.', 'Higher incomes and paid holidays; cheaper air travel; the internet for booking and information; package holidays; more interest in travel and new destinations.', '1 mark each up to [3]'),
        ('Explain the economic benefits of tourism for a country.', 'Jobs in hotels, transport and guiding; foreign exchange; taxes; multiplier effect on farmers, craftspeople and builders; investment in infrastructure.', '1 mark each up to [3]'),
        ('Explain the environmental problems caused by tourism.', 'Footpath erosion, litter, damage to coral reefs, disturbance of wildlife, water shortages, pollution from aircraft and sewage, building on coastlines.', '1 mark each up to [3]'),
        ('Explain how tourism can be made more sustainable.', 'Limit visitor numbers, use local guides and businesses, charge entry fees for conservation, educate visitors, use renewable energy and recycling, protect sensitive areas.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('All the money spent by tourists stays in the country they visit.', False, 'Much is lost through leakage to foreign airlines, tour operators and hotel chains.'),
        ('Tourism can help to protect wildlife by making it valuable.', True, 'Entry fees and jobs give an economic reason to conserve animals and habitats.'),
        ('Tourism only has positive effects on local cultures.', False, 'It can lead to loss of traditions, crime or conflict as well as pride and income.'),
    ],
    'cs': [
        ('tourism in an area', [
            ('Kenya', {'benefits': 'Tourism earns about 8-10% of GDP and employs over a million people directly and indirectly; safaris in the Maasai Mara and beaches near Mombasa; park fees fund conservation; Maasai earn money from conservancies, crafts and cultural visits.',
                       'problems': 'Minibuses disturb animals and erode tracks; leakage to foreign tour operators; Maasai were moved off land for parks; water shortages at coastal resorts; insecurity reduces visitor numbers.',
                       'manage': 'Community conservancies around the Maasai Mara pay Maasai landowners to keep land for wildlife; limits on vehicles around animals; ecolodges using solar power; KWS anti-poaching patrols.'}),
            ('the Maldives', {'benefits': 'Tourism provides about a quarter of GDP and most foreign income; about 2 million visitors a year (2023); resort islands provide jobs and taxes.',
                              'problems': 'Damage to coral reefs; waste disposed of at Thilafushi “rubbish island”; dependence on tourism; leakage to foreign-owned resorts; vulnerability to sea-level rise.',
                              'manage': 'One-island-one-resort policy; protected marine areas; green tax on tourists; limits on building heights; some resorts using solar power and desalination.'}),
        ], [
            ('describe the benefits of tourism to the area', 'benefits', 'Economic and social benefits with figures (GDP, jobs, conservation funding).'),
            ('explain the problems caused by tourism', 'problems', 'Environmental, social and economic problems.'),
            ('evaluate attempts to make tourism sustainable', 'manage', 'Named strategies and how effective they are.'),
        ]),
    ],
})


@c4d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4d_growth(r, D):
    dest = r.choice(['an island in the Caribbean', 'a national park in East Africa', 'a coastal resort in South-east Asia', 'a mountain region in Nepal'])
    yrs = [2000, 2005, 2010, 2015, 2020, 2023]
    v = [r.randint(100, 300)]
    for y in yrs[1:4]:
        v.append(round(v[-1] * r.uniform(1.1, 1.5)))
    v.append(round(v[-1] * r.uniform(0.15, 0.35)))  # 2020 pandemic collapse
    v.append(round(v[3] * r.uniform(0.85, 1.15)))
    spend = r.choice([400, 600, 800, 1200])
    leak = r.choice([30, 40, 50, 60, 70])
    stem = f'Fig. 4.3 shows international tourist arrivals (thousands) to {dest}: ' + ', '.join(f'{y}: {x}' for y, x in zip(yrs, v)) + f'. Tourists spend an average of US${spend} each; about {leak}% of this leaves the country (leakage).'
    if D == 1:
        opts, a = mcq(r, '2020', ['2005', '2015', '2023'])
        return {'stem': stem + ' In which year did arrivals fall sharply?', 'options': opts, 'answer': a, 'key': f'2020: {v[4]} thousand, due to the COVID-19 pandemic. [1]'}
    inc = v[3] * 1000 * spend * (100 - leak) / 100 / 1e6
    parts = [
        lambda r: ('Describe the changes in arrivals shown in Fig. 4.3.', f'Steady growth from {v[0]} 000 in 2000 to {v[3]} 000 in 2015, a sharp fall to {v[4]} 000 in 2020, then recovery to {v[5]} 000 in 2023.', '1 mark growth; 1 mark fall; 1 mark data [3]'),
        lambda r: ('Calculate the percentage change in arrivals from 2015 to 2020.', f'{dp(pct_change(v[3], v[4]))}%', f'({v[4]} − {v[3]}) ÷ {v[3]} × 100 [2]'),
        lambda r: ('Suggest a reason for the change in 2020.', 'The COVID-19 pandemic: border closures, flight cancellations and lockdowns.', '[1]'),
        lambda r: ('Calculate the income that stayed in the country from tourist spending in 2015, in US$ million.', f'US${dp(inc, 1)} million', f'{v[3]} 000 × {spend} × {100 - leak}% = {dp(inc, 1)} million [2]'),
        lambda r: ('Explain why leakage is high in many LIC destinations.', 'Hotels, airlines and tour companies are often foreign-owned; food, drink and equipment are imported; managers may be expatriates.', '1 mark each up to [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


CHAPTERS[4] = [c4a, c4b, c4c, c4d]


# ============================================================== CHAPTER 5: Resources and the environment

c5a = T('Energy resources: non-renewable and renewable sources', 'energy resources non-renewable renewable')
build(c5a, {
    'terms': [
        ('non-renewable energy', 'energy from sources that will run out because they cannot be replaced, such as coal, oil, natural gas and uranium'),
        ('renewable energy', 'energy from sources that are naturally replaced and will not run out, such as wind, solar and hydro-electric power'),
        ('fossil fuels', 'coal, oil and natural gas formed from the remains of plants and animals over millions of years'),
        ('hydro-electric power (HEP)', 'electricity generated by water flowing through turbines, usually from a reservoir behind a dam'),
        ('geothermal energy', 'heat from inside the Earth used to generate electricity or heat buildings'),
        ('nuclear power', 'electricity generated from heat released when uranium atoms are split'),
        ('biofuel', 'fuel made from plant or animal material, such as ethanol from sugar cane'),
        ('energy mix', 'the combination of different energy sources used by a country'),
        ('fuelwood', 'wood collected and burned for cooking and heating, an important energy source in many LICs'),
        ('energy security', 'having reliable, affordable access to enough energy'),
    ],
    'mcq': [
        ('Which country generates about 65-70% of its electricity from nuclear power?', 'France', ['Iceland', 'Nigeria', 'Norway'], '[1]'),
        ('Which is the main disadvantage of wind power?', 'Output varies with wind speed', ['It releases large amounts of CO₂', 'It will run out', 'It produces radioactive waste'], '[1]'),
        ('The Three Gorges Dam in China can generate about', '22.5 GW of electricity', ['2.25 MW', '225 GW', '0.5 GW'], 'The world’s largest power station by capacity. [1]'),
        ('Which energy source is used for most cooking in rural sub-Saharan Africa?', 'Fuelwood and charcoal', ['Nuclear power', 'Natural gas pipelines', 'Geothermal electricity'], '[1]'),
        ('Iceland uses geothermal energy because it lies on', 'a constructive plate boundary with volcanic activity', ['a coalfield', 'a desert', 'a conservative boundary with no heat'], '[1]'),
    ],
    'explain': [
        ('Explain the advantages and disadvantages of using fossil fuels.', 'Advantages: reliable, high energy output, existing infrastructure, relatively cheap. Disadvantages: non-renewable; release CO₂ causing climate change; air pollution and acid rain; oil spills; mining damage.', '1 mark each side up to [4]'),
        ('Explain the advantages and disadvantages of hydro-electric power.', 'Advantages: renewable, no CO₂ when running, reliable, reservoirs store water and control floods. Disadvantages: expensive to build; flooding of land and relocation of people; trapping of sediment; impact on fish; needs suitable valleys.', '1 mark each side up to [4]'),
        ('Explain why LICs often use a different energy mix from HICs.', 'LICs rely more on fuelwood and biomass because it is free or cheap and many rural people have no electricity; HICs use more fossil fuels, nuclear and renewables supplied through national grids.', '1 mark LIC; 1 mark HIC; 1 mark reason [3]'),
        ('Explain why the demand for energy is increasing globally.', 'Population growth; economic development and industrialisation in NEEs such as China and India; rising incomes leading to more cars, appliances and air conditioning; urbanisation.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('Nuclear power is renewable because it does not produce carbon dioxide.', False, 'Uranium is a finite resource, so nuclear is non-renewable, although it produces little CO₂.'),
        ('Solar power is most effective in places with clear skies and high sun angles.', True, 'Such places receive the most insolation, e.g. the Sahara or Rajasthan.'),
        ('Renewable energy has no environmental impacts.', False, 'HEP floods valleys, wind farms affect landscapes and birds, and biofuels use farmland.'),
    ],
    'cs': [
        ('an energy supply scheme', [
            ('the Three Gorges Dam, China (HEP)', {'scheme': 'Completed in 2006 (all turbines by 2012) on the Yangtze; 185 m high and 2.3 km wide; 32 turbines with a capacity of about 22.5 GW; reservoir about 600 km long.',
                                                  'evaluate': 'Benefits: large amount of renewable electricity, reducing coal use; flood control; navigation for large ships. Costs: about 1.3 million people relocated; archaeological sites and farmland flooded; sediment trapped; landslides; ecological damage; cost about US$30 billion.'}),
            ('geothermal energy in Iceland', {'scheme': 'Plants such as Hellisheiði and Nesjavellir use steam from hot rocks near the Mid-Atlantic Ridge; geothermal power provides about 25-30% of electricity and about 90% of home heating; hot water is piped to Reykjavík.',
                                             'evaluate': 'Benefits: cheap, renewable, low-carbon energy; greenhouses grow food; tourism (Blue Lagoon). Problems: high building costs; release of hydrogen sulphide; only possible in tectonically active areas.'}),
            ('wind power in Denmark', {'scheme': 'Wind turbines on land and offshore (e.g. Horns Rev in the North Sea) supply about half of Denmark’s electricity; many turbines are owned by local cooperatives; Danish firms such as Vestas export turbines.',
                                       'evaluate': 'Benefits: renewable, low carbon, jobs in manufacturing, energy security. Problems: variable output requires links to neighbouring grids and storage; visual impact; offshore farms are expensive.'}),
        ], [
            ('describe the energy scheme', 'scheme', 'Location, type of energy, scale (capacity, % of supply), dates.'),
            ('evaluate the advantages and disadvantages of the energy scheme', 'evaluate', 'Economic, social and environmental benefits and costs, judgement.'),
        ]),
    ],
    'essays': [
        ('renewable energy sources can meet all of the world’s future energy needs',
         ['Solar, wind, HEP and geothermal are growing rapidly and getting cheaper; Denmark gets about half its electricity from wind and Iceland nearly all from renewables.'],
         ['Output from wind and solar varies, so storage and backup are needed; HEP and geothermal depend on geography; demand is rising fast in NEEs; transport and industry still depend on oil and gas.'],
         'Renewables could meet most needs in the long term with storage, grids and efficiency, but fossil fuels and nuclear will remain important for some decades.',
         ['reliability', 'cost', 'geography', 'demand growth']),
    ],
})


@c5a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5a_mix(r, D):
    nm = r.choice(['Country P', 'Country Q', 'Country R'])
    srcs = ['coal', 'natural gas', 'oil', 'nuclear', 'hydro-electric', 'wind', 'solar']
    k = r.choice([4, 5])
    use = r.sample(srcs, k)
    cuts = sorted(r.sample(range(1, 20), k - 1))
    pc = [(b - a) * 5 for a, b in zip([0] + cuts, cuts + [20])]
    tot = r.choice([40, 60, 80, 120, 200])  # TWh
    stem = f'Fig. 5.1 shows the sources of electricity generated in {nm} in one year (total {tot} TWh): ' + ', '.join(f'{s} {p}%' for s, p in zip(use, pc)) + '.'
    ren = sum(p for s, p in zip(use, pc) if s in ('hydro-electric', 'wind', 'solar'))
    fos = sum(p for s, p in zip(use, pc) if s in ('coal', 'natural gas', 'oil'))
    if D == 1:
        opts, a = mcq(r, f'{ren}%', [f'{fos}%', f'{100 - ren}%', f'{ren + 10}%', f'{max(pc)}%', f'{ren + 5}%', f'{max(ren - 5, 1)}%'])
        return {'stem': stem + ' What percentage came from renewable sources?', 'options': opts, 'answer': a, 'key': f'Sum of hydro, wind and solar = {ren}%. [1]'}
    i = r.randrange(k)
    parts = [
        lambda r: ('Calculate the percentage of electricity from renewable sources.', f'{ren}%', 'sum of HEP, wind, solar [1]'),
        lambda r: ('Calculate the percentage from fossil fuels.', f'{fos}%', 'sum of coal, gas, oil [1]'),
        lambda r: (f'Calculate how much electricity (TWh) came from {use[i]}.', f'{fmt(tot * pc[i] / 100, 1)} TWh', f'{pc[i]}% × {tot} [1]'),
        lambda r: (f'Calculate the angle of the {use[i]} sector of a pie chart.', f'{fmt(pc[i] * 3.6, 1)}°', f'{pc[i]} × 3.6 [1]'),
        lambda r: ('Suggest two reasons why the country might want to increase its use of renewable energy.', 'Reduce greenhouse gas emissions and meet climate targets; improve energy security and reduce imports; fossil fuels will run out; less air pollution.', '1 mark each [2]'),
        lambda r: ('Explain one disadvantage of relying heavily on wind and solar power.', 'Output varies with weather and time of day, so backup power or storage is needed.', '1 mark problem; 1 mark development [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 5.2 water
c5b = T('Water supply and demand: shortages and management', 'water supply demand shortages management')
build(c5b, {
    'terms': [
        ('water stress', 'when demand for water exceeds the available supply, or poor quality restricts its use (below about 1700 m³ per person per year)'),
        ('water scarcity', 'a lack of enough clean water to meet the needs of people in an area'),
        ('aquifer', 'a layer of permeable rock that stores groundwater'),
        ('water table', 'the upper level of saturated ground below the surface'),
        ('desalination', 'removing salt from seawater to produce fresh water'),
        ('water transfer scheme', 'moving water from an area of surplus to an area of deficit by pipelines, canals or tunnels'),
        ('drip irrigation', 'a method that delivers small amounts of water directly to plant roots, reducing waste'),
        ('greywater', 'used water from sinks, showers and washing machines that can be reused for flushing or watering'),
        ('physical water scarcity', 'when there is not enough water to meet demand because of a dry climate'),
        ('economic water scarcity', 'when water exists but people cannot afford the infrastructure to use it'),
    ],
    'mcq': [
        ('Which sector uses about 70% of the world’s fresh water?', 'Agriculture (mainly irrigation)', ['Industry', 'Domestic use', 'Tourism'], '[1]'),
        ('Which country supplies about 40% of its water from desalination and NEWater recycling as part of its “Four National Taps”?', 'Singapore', ['Nepal', 'Norway', 'Brazil'], '[1]'),
        ('Lowering of the water table is most likely to be caused by', 'pumping more groundwater than is replaced by rainfall', ['heavy rainfall', 'planting forests', 'building reservoirs'], '[1]'),
        ('The Lesotho Highlands Water Project transfers water to', 'Gauteng (Johannesburg area), South Africa', ['Cairo, Egypt', 'Lagos, Nigeria', 'Nairobi, Kenya'], '[1]'),
    ],
    'explain': [
        ('Explain why demand for water is increasing.', 'Population growth; more irrigation to grow food; industrial growth; rising living standards (showers, washing machines, swimming pools); urbanisation and tourism.', '1 mark each up to [3]'),
        ('Explain the advantages and disadvantages of desalination.', 'Advantages: reliable supply independent of rainfall, unlimited seawater. Disadvantages: very expensive and energy-intensive; brine waste harms marine life; only practical near coasts.', '1 mark each side up to [3]'),
        ('Explain why many people in LICs lack access to safe water.', 'Lack of money for pipes, treatment and pumps (economic scarcity); dry climate; pollution of rivers; rapid growth of informal settlements; women and children walk long distances to wells.', '1 mark each up to [3]'),
        ('Explain how water can be managed more sustainably.', 'Drip irrigation; fixing leaks; water meters; rainwater harvesting; recycling greywater; education campaigns; protecting groundwater.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('Water shortages only happen in deserts.', False, 'Economic scarcity, pollution and over-use cause shortages in wetter regions too.'),
        ('Water transfer schemes can cause conflict between regions or countries.', True, 'The source area may lose water it needs, e.g. disputes over the Nile.'),
        ('Building more dams is always the most sustainable way to increase water supply.', False, 'Dams are costly, displace people and harm ecosystems; reducing demand and recycling may be more sustainable.'),
    ],
    'cs': [
        ('a water supply scheme', [
            ('the Lesotho Highlands Water Project', {'scheme': 'Dams in the mountains of Lesotho, such as Katse (1998) and Mohale (2002), store water from the Senqu (Orange) river and transfer it through tunnels to the Vaal River system and Gauteng, South Africa; also generates HEP for Lesotho at Muela; Polihali Dam under construction.',
                                                    'evaluate': 'Benefits: reliable water for about 12 million people in South Africa; royalties of millions of US$ a year and electricity for Lesotho. Problems: thousands of people relocated and farmland flooded; reduced flow downstream; corruption scandals; many rural Basotho still lack piped water.'}),
            ('Singapore’s Four National Taps', {'scheme': 'Water from local catchments and reservoirs (e.g. Marina Barrage); imported water from Johor, Malaysia; NEWater (recycled wastewater, up to about 40% of demand); desalination plants (up to about 25% of demand).',
                                               'evaluate': 'Benefits: greater independence from imports and a reliable supply despite little land. Problems: desalination and NEWater are energy-intensive and costly; water prices are high; the agreement with Malaysia expires in 2061.'}),
        ], [
            ('describe how the scheme increases water supply', 'scheme', 'Named dams/plants/transfers, dates, capacity, how water reaches users.'),
            ('evaluate the success of the scheme', 'evaluate', 'Economic, social and environmental advantages and disadvantages; judgement.'),
        ]),
    ],
})


@c5b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5b_use(r, D):
    cs = r.sample([('Country P', 'HIC'), ('Country Q', 'NEE'), ('Country R', 'LIC'), ('Country S', 'HIC'), ('Country T', 'LIC')], 3)
    rows = []
    for n, k in cs:
        if k == 'HIC':
            dom, ind = r.randint(12, 20), r.randint(35, 55)
        elif k == 'NEE':
            dom, ind = r.randint(8, 15), r.randint(15, 30)
        else:
            dom, ind = r.randint(5, 12), r.randint(2, 8)
        if ind == 100 - dom - ind:
            ind += 1
        rows.append((n, k, dom, ind, 100 - dom - ind))
    lpd = [(n, r.randint(150, 350) if k == 'HIC' else r.randint(60, 140) if k == 'NEE' else r.randint(10, 40)) for n, k, *_ in rows]
    stem = 'Table 5.1 shows water use by sector (%) and domestic water use per person per day. ' + ' '.join(f'{n}: domestic {d}%, industry {i}%, agriculture {a}%, {l} litres per person per day.' for (n, _, d, i, a), (_, l) in zip(rows, lpd))
    if D == 1:
        n, _, d, i, a = rows[0]
        opts, ans = mcq(r, f'{a}%', [f'{d + i}%', f'{100 - a}%', f'{a - 10}%', f'{i}%', f'{a + 5}%', f'{max(a - 5, 1)}%'])
        return {'stem': stem + f' What percentage of {n}’s water is used for agriculture?', 'options': opts, 'answer': ans, 'key': f'100 − {d} − {i} = {a}%. [1]'}
    hi = max(lpd, key=lambda x: x[1])
    lo = min(lpd, key=lambda x: x[1])
    parts = [
        lambda r: ('Check that the sectors for each country add up to 100%, and state the largest water-using sector in each country.', 'Each totals 100%; ' + '; '.join(f'{n}: ' + max((('domestic', d), ('industry', i), ('agriculture', a)), key=lambda x: x[1])[0] for n, _, d, i, a in rows) + '.', '1 mark check; 1 mark sectors [2]'),
        lambda r: ('Calculate how many times more water per person per day is used in the highest-use country than the lowest.', f'{dp(hi[1] / lo[1])} times', f'{hi[1]} ÷ {lo[1]} [1]'),
        lambda r: ('Calculate the domestic water use per person in a year for the highest-use country, in m³.', f'{dp(hi[1] * 365 / 1000)} m³', f'{hi[1]} × 365 ÷ 1000 [2]'),
        lambda r: ('Suggest why industry uses a larger share of water in richer countries.', 'More manufacturing, power stations (cooling) and processing; farming is a smaller share of the economy and often more efficient.', '1 mark each up to [2]'),
        lambda r: ('Suggest why domestic use per person is lower in LICs.', 'Fewer homes have piped water, flush toilets, showers and washing machines; water may be carried from wells; cost.', '1 mark each up to [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 5.3 environmental risks
c5c = T('Environmental risks of economic development: pollution, soil erosion and climate change', 'pollution soil erosion climate change')
build(c5c, {
    'terms': [
        ('enhanced greenhouse effect', 'the increased trapping of heat in the atmosphere caused by extra greenhouse gases released by human activity'),
        ('greenhouse gas', 'a gas such as carbon dioxide, methane or nitrous oxide that absorbs heat radiated from the Earth’s surface'),
        ('acid rain', 'rain made more acidic by sulphur dioxide and nitrogen oxides from burning fossil fuels'),
        ('eutrophication', 'excess nutrients from fertilisers or sewage in water that cause algal blooms and loss of oxygen'),
        ('soil erosion', 'the removal of topsoil by wind or water faster than it can form'),
        ('salinisation', 'the build-up of salt in soil, often caused by poorly managed irrigation in hot climates'),
        ('point source pollution', 'pollution from a single identifiable source such as a factory pipe'),
        ('carbon footprint', 'the total greenhouse gases produced by a person, organisation or product, measured as CO₂ equivalent'),
        ('smog', 'a mixture of smoke, fog and chemical pollutants that reduces air quality in cities'),
    ],
    'mcq': [
        ('Atmospheric CO₂ has risen from about 280 ppm before industrialisation to about', '420 ppm (2023)', ['290 ppm', '1000 ppm', '28 ppm'], '[1]'),
        ('Which gas is released mainly by rice paddies, cattle and landfill sites?', 'Methane', ['Oxygen', 'Nitrogen', 'Ozone'], '[1]'),
        ('Which disaster in 1984 released toxic gas from a pesticide factory, killing thousands?', 'Bhopal, India', ['Chernobyl, Ukraine', 'Fukushima, Japan', 'Aral Sea, Kazakhstan'], '[1]'),
        ('Which is an effect of eutrophication?', 'Algal blooms that reduce oxygen and kill fish', ['Clearer water and more fish', 'Lower nutrient levels', 'Higher river discharge'], '[1]'),
        ('The Aral Sea shrank mainly because', 'rivers feeding it were diverted to irrigate cotton', ['of earthquakes', 'of too much rainfall', 'of a tsunami'], '[1]'),
    ],
    'explain': [
        ('Explain how human activity enhances the greenhouse effect.', 'Burning fossil fuels releases CO₂; deforestation reduces CO₂ uptake and releases carbon; farming (cattle, rice) and landfill release methane; more greenhouse gases trap more outgoing heat, warming the atmosphere.', '1 mark each source; 1 mark mechanism [3]'),
        ('Explain the possible impacts of climate change.', 'Sea-level rise flooding low-lying coasts (Bangladesh, Maldives); more extreme weather (droughts, storms, heatwaves); changes in crop yields; melting glaciers affecting water supply; species loss; spread of disease.', '1 mark each up to [4]'),
        ('Explain how economic development can cause soil erosion.', 'Deforestation for farming, mining and roads removes vegetation; overgrazing and over-cultivation; ploughing up and down slopes; rain and wind then remove the exposed topsoil.', '1 mark cause; 1 mark process [2]'),
        ('Explain why air pollution is often severe in rapidly industrialising cities.', 'Growth of factories and coal power stations, increasing vehicles, weak regulation and enforcement; temperature inversions trap pollutants (e.g. Delhi, Beijing).', '1 mark each up to [3]'),
    ],
    'claims': [
        ('The greenhouse effect is entirely harmful.', False, 'The natural greenhouse effect keeps the Earth about 33 °C warmer and habitable; the problem is its enhancement by human activity.'),
        ('Fertiliser run-off can cause eutrophication in lakes and rivers.', True, 'Nitrates and phosphates feed algal blooms that use up oxygen.'),
        ('Pollution only affects the place where it is produced.', False, 'Air pollution, acid rain and greenhouse gases cross borders; river pollution flows downstream.'),
    ],
    'cs': [
        ('environmental damage caused by economic activity', [
            ('the Aral Sea, Kazakhstan and Uzbekistan', {'causes': 'From the 1960s the Soviet Union diverted the Amu Darya and Syr Darya rivers to irrigate cotton and rice in the desert; inefficient, unlined canals lost huge amounts of water.',
                                                         'impacts': 'The sea lost about 90% of its volume and split into parts; the fishing industry at Muynak collapsed; salt and pesticide dust storms caused respiratory disease; the local climate became more extreme; salinisation of farmland.'}),
            ('the Niger Delta, Nigeria (oil)', {'causes': 'Oil extraction since 1958 by TNCs such as Shell; leaking and sabotaged pipelines; illegal refining; gas flaring.',
                                                'impacts': 'Thousands of oil spills polluting mangroves, rivers and farmland; fishing and farming livelihoods destroyed; health problems from contaminated water and gas flaring; conflict and protests; clean-up of Ogoniland began only after a 2011 UN report.'}),
        ], [
            ('explain how economic activity caused the environmental damage', 'causes', 'Named activity, scale, processes leading to damage.'),
            ('describe the impacts of the environmental damage on people and the environment', 'impacts', 'Ecosystem, health, economic and social impacts.'),
        ]),
    ],
    'essays': [
        ('economic development will always damage the environment',
         ['Industrialisation, energy use, mining and intensive farming have caused pollution, soil erosion and climate change (Aral Sea, Niger Delta).'],
         ['Cleaner technology, renewable energy, regulation and international agreements allow growth with less damage; many HICs have cut pollution while growing.', 'Development can fund conservation.'],
         'Development has usually damaged the environment, but sustainable approaches show that damage is not inevitable.',
         ['pollution', 'renewable energy', 'regulation', 'sustainable development']),
    ],
})


@c5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5c_co2(r, D):
    yrs = [1960, 1970, 1980, 1990, 2000, 2010, 2020]
    ppm = [317, 326, 339, 354, 370, 390, 414]
    a, b = sorted(r.sample(range(len(yrs)), 2))
    stem = 'Fig. 5.2 shows the mean concentration of carbon dioxide in the atmosphere at Mauna Loa, Hawaii (ppm): ' + ', '.join(f'{y}: {p}' for y, p in zip(yrs, ppm)) + '.'
    rate = (ppm[b] - ppm[a]) / (yrs[b] - yrs[a])
    if D == 1:
        opts, ans = mcq(r, f'{ppm[-1] - ppm[0]} ppm', [f'{ppm[-1]} ppm', f'{ppm[-1] - 280} ppm', f'{ppm[3] - ppm[0]} ppm'])
        return {'stem': stem + ' By how much did CO₂ concentration rise from 1960 to 2020?', 'options': opts, 'answer': ans, 'key': f'{ppm[-1]} − {ppm[0]} = {ppm[-1] - ppm[0]} ppm. [1]'}
    parts = [
        lambda r: ('Describe the trend shown in Fig. 5.2.', 'A continuous increase from 317 ppm in 1960 to 414 ppm in 2020, with the rate of increase speeding up (about 9 ppm per decade in the 1960s, 24 ppm in the 2010s).', '1 mark trend; 1 mark accelerating; 1 mark data [3]'),
        lambda r: (f'Calculate the mean rate of increase per year between {yrs[a]} and {yrs[b]}.', f'{dp(rate, 2)} ppm per year', f'({ppm[b]} − {ppm[a]}) ÷ {yrs[b] - yrs[a]} [2]'),
        lambda r: ('Calculate the percentage increase from 1960 to 2020.', f'{dp(pct_change(ppm[0], ppm[-1]))}%', f'(414 − 317) ÷ 317 × 100 [2]'),
        lambda r: ('Explain why the concentration of CO₂ has increased.', 'Burning of fossil fuels for power, transport and industry; deforestation; cement production; growing populations and economies.', '1 mark each up to [3]'),
        lambda r: ('Suggest why Mauna Loa is a good place to measure CO₂.', 'It is remote and high, far from local sources of pollution, so readings represent the global atmosphere.', '1 mark remote; 1 mark representative [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 5.4 managing resources sustainably
c5d = T('Managing resources sustainably: conservation and international cooperation', 'managing resources sustainably conservation international cooperation')
build(c5d, {
    'terms': [
        ('sustainable development', 'development that meets the needs of the present without compromising the ability of future generations to meet their own needs'),
        ('conservation', 'the protection and careful management of natural resources and environments'),
        ('Paris Agreement', 'the 2015 international agreement to limit global warming to well below 2 °C and to try to limit it to 1.5 °C'),
        ('Montreal Protocol', 'the 1987 international agreement to phase out chemicals such as CFCs that damage the ozone layer'),
        ('carbon trading', 'a system in which companies or countries buy and sell permits to emit carbon dioxide'),
        ('recycling', 'processing used materials so that they can be made into new products'),
        ('Sustainable Development Goals (SDGs)', 'the 17 goals agreed by the United Nations in 2015 to end poverty and protect the planet by 2030'),
        ('national park', 'an area protected by law to conserve its landscape, wildlife and heritage'),
    ],
    'mcq': [
        ('Which international agreement has been most successful at protecting the ozone layer?', 'The Montreal Protocol (1987)', ['The Kyoto Protocol (1997)', 'The Paris Agreement (2015)', 'CITES (1973)'], '[1]'),
        ('The Paris Agreement aims to limit global warming to', 'well below 2 °C, aiming for 1.5 °C', ['5 °C', '0 °C', '3-4 °C'], '[1]'),
        ('Which of these is an example of conserving a resource?', 'Insulating homes to reduce energy use', ['Leaving lights on', 'Burning more coal', 'Throwing plastic into landfill'], '[1]'),
        ('How many Sustainable Development Goals did the UN agree in 2015?', '17', ['5', '8', '30'], '[1]'),
    ],
    'explain': [
        ('Explain why international cooperation is needed to tackle climate change.', 'Greenhouse gases mix globally, so one country’s emissions affect all; countries must share targets so none gains by polluting; richer countries can fund poorer ones; technology can be shared.', '1 mark each up to [3]'),
        ('Explain how individuals can help to manage resources sustainably.', 'Reduce, reuse and recycle; save energy and water; use public transport, walk or cycle; buy local or certified products; reduce food waste.', '1 mark each up to [3]'),
        ('Explain why it is difficult to reach international agreements on reducing emissions.', 'Countries have different levels of development and responsibility; NEEs argue they need to grow; costs of changing energy systems; political changes; no strong enforcement.', '1 mark each up to [3]'),
        ('Explain how recycling helps conserve resources.', 'It reduces the need to extract new raw materials, saves the energy used in processing, and reduces waste sent to landfill.', '1 mark each [3]'),
    ],
    'claims': [
        ('International agreements have never succeeded in solving environmental problems.', False, 'The Montreal Protocol phased out most CFCs and the ozone layer is recovering.'),
        ('Sustainable development considers the needs of future generations.', True, 'It meets present needs without compromising future ones.'),
        ('Recycling uses no energy at all.', False, 'Collecting and processing materials uses energy, though usually less than making new products.'),
    ],
    'cases': [
        (['Fig. 5.3 shows recycling rates of household waste in a city: 2010 15%, 2014 24%, 2018 33%, 2022 41%. In 2014 the city introduced separate bins for paper, glass and food waste and a charge for each bag of non-recycled rubbish.',
          'Study Fig. 5.3. A city’s household recycling rate rose from 15% in 2010 to 41% in 2022 after it introduced kerbside collection of recyclables, food-waste bins and a charge on general rubbish in 2014.'],
         [('Calculate the change in recycling rate between 2010 and 2022.', '+26 percentage points', '41 − 15 = 26 [1]'),
          ('Calculate the percentage increase in the recycling rate between 2010 and 2022.', f'{dp(pct_change(15, 41))}%', '(41 − 15) ÷ 15 × 100 [2]'),
          ('Explain how the measures introduced in 2014 may have increased recycling.', 'Separate bins made recycling easy; the charge on general rubbish gave a financial incentive to recycle.', '1 mark each [2]'),
          ('Suggest two benefits of increasing recycling.', 'Less waste to landfill; conserves raw materials; saves energy; reduces greenhouse gases; creates jobs.', '1 mark each [2]'),
          ('Suggest why the recycling rate has not reached 100%.', 'Some materials cannot be recycled; contamination of bins; lack of space or motivation; some residents do not take part.', '1 mark each up to [2]')]),
    ],
    'essays': [
        ('international agreements are more important than local actions in managing resources sustainably',
         ['Global problems such as climate change and ozone depletion need agreements (Paris 2015, Montreal 1987) because pollution crosses borders.'],
         ['Agreements only work if governments, businesses and individuals act locally: recycling, energy saving, community conservation and sustainable farming.', 'Agreements can be weak or ignored.'],
         'Both are needed: international agreements set targets and funding, but local actions deliver the changes.',
         ['Paris Agreement', 'Montreal Protocol', 'recycling', 'local communities']),
    ],
})


CHAPTERS[5] = [c5a, c5b, c5c, c5d]


# ============================================================== CHAPTER 6: Geographical enquiry and fieldwork

ENQ = [  # (context, hypothesis, primary methods, equipment, sampling, risk, presentation)
    ('Students are investigating how a river changes downstream near {c}.', 'The width, depth and velocity of the river increase with distance downstream.',
     'measuring width with a tape, depth at equal intervals with a metre rule and velocity by timing a float over 10 m', 'tape measure, metre rule, float, stopwatch, ranging poles',
     'systematic sampling: sites every 1 km along the river', 'drowning or slipping on wet rocks: work in groups, wear wellingtons, avoid fast or deep water, check the weather', 'scatter graphs of width, depth and velocity against distance, and cross-sections'),
    ('Students are investigating whether pedestrian numbers decrease with distance from the centre of the CBD of {c}.', 'Pedestrian numbers decrease with distance from the centre of the CBD.',
     'counting pedestrians passing a point for 10 minutes at each site and recording the time', 'tally sheet, clipboard, stopwatch, map', 'systematic sampling: sites every 100 m along a transect from the centre',
     'traffic and getting lost: stay on pavements, wear high-visibility vests, work in pairs, carry a phone', 'a located bar graph or proportional circles on a map, and a scatter graph against distance'),
    ('Students are investigating how environmental quality varies between different residential areas of {c}.', 'Environmental quality is higher in the suburbs than in the inner city.',
     'an environmental quality survey (EQS) scoring litter, noise, graffiti, green space and building condition from −2 to +2', 'EQS sheet, clipboard, camera, map',
     'stratified sampling: the same number of sites in each zone', 'personal safety and traffic: work in groups, avoid confrontations, stay in public areas', 'a bar graph of mean EQS scores for each area and a choropleth map'),
    ('Students are investigating how beach sediment changes along a beach affected by longshore drift near {c}.', 'Pebbles become smaller and more rounded in the direction of longshore drift.',
     'measuring the long axis of 10 pebbles at each site with callipers and classifying roundness using a Powers scale', 'callipers, ruler, quadrat, Powers roundness chart',
     'systematic sampling: sites every 50 m along the beach, random pebbles within a quadrat', 'tides and waves, cliff falls: check tide times, stay away from the cliff base and the water’s edge', 'a dispersion graph and a bar graph of mean size at each site'),
    ('Students are investigating the sphere of influence of a shopping centre in {c}.', 'Most shoppers travel less than 5 km to the shopping centre.',
     'a questionnaire asking shoppers where they have travelled from, how they travelled and how often they visit', 'questionnaire sheets, clipboard, map',
     'systematic sampling: asking every 10th person who passes, at different times of day', 'approaching strangers: work in pairs, ask permission, stay in public places', 'a desire-line map and a histogram of distances travelled'),
    ('Students are investigating how microclimate varies around their school in {c}.', 'Temperature is higher and wind speed lower in sheltered sites close to buildings.',
     'measuring air temperature with a digital thermometer and wind speed with a hand-held anemometer at the same height at each site', 'digital thermometer, anemometer, compass, site map',
     'stratified sampling: sites in each type of location (open field, car park, courtyard, beside buildings)', 'tripping and traffic in car parks: stay with the group, look out for vehicles', 'an isoline map of temperature and a bar graph of wind speed by site'),
    ('Students are investigating the impact of tourism on a honeypot site near {c}.', 'Footpath erosion increases closer to the visitor car park.',
     'measuring footpath width and depth of erosion at intervals, and counting visitors per hour', 'tape measure, metre rule, tally sheet, camera',
     'systematic sampling: measurements every 50 m along the main path from the car park', 'uneven ground and weather: wear suitable boots, carry waterproofs, stay on paths', 'a line graph of path width against distance and annotated photographs'),
    ('Students are investigating how traffic flow varies during the day on a main road in {c}.', 'Traffic flow is highest during the morning and evening rush hours.',
     'counting vehicles for 15 minutes every hour from 07:00 to 19:00, classifying them by type', 'tally sheet, stopwatch, clipboard', 'systematic (time) sampling: 15-minute counts every hour',
     'roadside traffic and pollution: stand well back from the kerb, wear high-visibility vests, work in pairs', 'a line graph of vehicles per hour against time, and a pie chart of vehicle types'),
]

c6a = T('Forming hypotheses and planning a geographical investigation', 'hypotheses planning geographical investigation')
build(c6a, {
    'terms': [
        ('hypothesis', 'a statement that can be tested by collecting and analysing data, which may be accepted or rejected'),
        ('null hypothesis', 'a statement that there is no relationship or difference between the variables being studied'),
        ('enquiry question', 'a question that sets out the aim of a geographical investigation'),
        ('primary data', 'data collected first-hand in the field by the investigator'),
        ('secondary data', 'data that has already been collected by someone else, such as census data, maps or websites'),
        ('pilot study', 'a small trial of the methods carried out before the main investigation to find and fix problems'),
        ('risk assessment', 'identifying the hazards of fieldwork and the steps taken to reduce them'),
        ('variable', 'a factor that can be measured and that changes, such as river velocity or pedestrian numbers'),
        ('qualitative data', 'non-numerical data such as photographs, sketches and opinions'),
        ('quantitative data', 'numerical data that can be counted or measured'),
    ],
    'mcq': [
        ('Which of these is the best hypothesis for a fieldwork investigation?', 'River velocity increases with distance downstream.', ['Rivers are interesting.', 'What happens to rivers?', 'Rivers change.'], 'A hypothesis is a testable statement that names variables. [1]'),
        ('Which is an example of secondary data?', 'Census data from a government website', ['A pedestrian count you carried out', 'Your own questionnaire results', 'River depth you measured'], '[1]'),
        ('Why should a pilot study be carried out?', 'To test the methods and correct any problems before the main data collection', ['To make the results support the hypothesis', 'To avoid a risk assessment', 'To replace the main investigation'], '[1]'),
        ('Which of these is qualitative data?', 'Annotated field sketches and photographs', ['A traffic count', 'River width in metres', 'Air temperature readings'], '[1]'),
        ('A null hypothesis for “Pedestrian numbers decrease with distance from the CBD” would be', 'There is no relationship between pedestrian numbers and distance from the CBD.', ['Pedestrian numbers increase with distance from the CBD.', 'The CBD has many shops.', 'Pedestrians walk faster away from the CBD.'], '[1]'),
    ],
    'explain': [
        ('Explain why a hypothesis must be testable.', 'It must name measurable variables so that data can be collected and analysed to show clearly whether it is supported or rejected.', '1 mark measurable variables; 1 mark accept/reject [2]'),
        ('Explain why investigators carry out a risk assessment before fieldwork.', 'To identify hazards (traffic, water, weather, strangers) and plan how to reduce them so that students are safe.', '1 mark identify hazards; 1 mark reduce risk [2]'),
        ('Explain the value of using both primary and secondary data in an investigation.', 'Primary data is specific to the hypothesis and up to date; secondary data gives context, a wider area or change over time and can be used to check primary results.', '1 mark primary; 1 mark secondary [2]'),
        ('Explain why it is important to collect data at the same time of day at each site.', 'Conditions such as pedestrian numbers, traffic or temperature change through the day, so collecting at the same time makes the results fair and comparable.', '1 mark conditions vary; 1 mark fair comparison [2]'),
    ],
    'claims': [
        ('A hypothesis that is rejected means the investigation has failed.', False, 'Rejecting a hypothesis is a valid conclusion; the evidence still tells us something about the area.'),
        ('Fieldwork should be planned so that the results can be compared fairly between sites.', True, 'The same methods, equipment, times and sample sizes are used at each site.'),
        ('A risk assessment is only needed when working near rivers.', False, 'All fieldwork has risks, such as traffic, weather or approaching strangers.'),
    ],
})


def _enq(r):
    e = list(r.choice(ENQ))
    e[0] = e[0].format(c=city(r))
    return e


@c6a.add('C3', (1, 2, 3, 4, 5), 'case')
def c6a_plan(r, D):
    ctx, hyp, meth, eq, samp, risk, pres = _enq(r)
    if D == 1:
        other = [x[1] for x in ENQ if x[1] != hyp]
        opts, a = mcq(r, hyp, r.sample(other, 3))
        return {'stem': ctx + ' Which is the most suitable hypothesis for this investigation?', 'options': opts, 'answer': a, 'key': 'The hypothesis must match the enquiry and be testable. [1]'}
    parts = [
        lambda r: ('Write a suitable hypothesis for this investigation.', hyp, '1 mark testable statement linked to the enquiry [1]'),
        lambda r: ('Describe a method of collecting primary data to test the hypothesis.', cap(meth) + '.', '1 mark method; 1 mark detail (how/where/when) [2]'),
        lambda r: ('List the equipment the students will need.', cap(eq) + '.', '1 mark for two items, 2 marks for three or more [2]'),
        lambda r: ('Describe and justify a suitable sampling strategy.', cap(samp) + ', which gives an even, unbiased spread of data that can be compared.', '1 mark strategy; 1 mark justification [2]'),
        lambda r: ('Identify one risk and explain how it could be reduced.', cap(risk) + '.', '1 mark risk; 1 mark reduction [2]'),
        lambda r: ('Suggest how the results could be presented.', cap(pres) + '.', '1 mark technique; 1 mark reason [2]'),
        lambda r: ('Suggest one source of secondary data that would help the investigation.', 'Maps, census or council data, Environment Agency or weather records, previous studies, websites or old photographs.', '[1]'),
    ]
    return compose(r, ctx, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c6a.add('C2', (1, 2, 3, 4), 'explain')
def c6a_bad(r, D):
    bad = [('Rivers are bigger downstream.', 'It is vague: “bigger” must be defined as measurable variables such as width, depth or discharge.'),
           ('What makes people visit the town centre?', 'It is a question, not a testable statement.'),
           ('The CBD is the best place in the city.', 'It is an opinion and cannot be measured objectively.'),
           ('Pollution is bad.', 'It is vague and does not name variables or a location to test.'),
           ('Some places have more shops.', 'It does not say which places or what relationship is expected, so it cannot be clearly accepted or rejected.'),
           ('Tourism has an effect.', 'It does not say what effect, where, or how it will be measured.')]
    s, why = r.choice(bad)
    better = r.choice(ENQ)[1]
    stem = f'A student writes the hypothesis: “{s}” Explain why this is not a good hypothesis' + (' and write an improved hypothesis for a fieldwork investigation.' if D >= 2 else '.')
    return {'stem': stem, 'answer': why + (f' Improved example: “{better}”' if D >= 2 else ''), 'key': '1 mark weakness' + ('; 1 mark testable improved hypothesis [2]' if D >= 2 else ' [1]'), 'marks': 2 if D >= 2 else 1}


@c6a.add('C4', (2, 3, 4, 5), 'case')
def c6a_design(r, D):
    ctx, hyp, meth, eq, samp, risk, pres = _enq(r)
    p = person(r)
    stem = f'{ctx} {p}’s group has one day for fieldwork and their hypothesis is “{hyp}”'
    parts = [
        lambda r: ('Plan the investigation: describe the methods, sampling and equipment the group should use.', f'{cap(meth)}; {samp}; equipment: {eq}.', '1 mark method; 1 mark sampling; 1 mark equipment; 1 mark detail of how to ensure fairness [4]'),
        lambda r: ('Explain why a pilot study would be useful.', 'To check that methods work, that questions or recording sheets are clear, and how long each site takes, so the day is used efficiently.', '1 mark each up to [2]'),
        lambda r: ('Identify two risks and explain how each would be managed.', cap(risk) + '; also weather: check forecast and carry suitable clothing.', '1 mark each risk; 1 mark each management [4]'),
        lambda r: ('Explain how the group could make sure their results are reliable.', 'Repeat measurements and take means, use the same equipment and times at each site, use a large enough sample, and have the same person record each measurement.', '1 mark each up to [3]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


# --------------------------------------------------------------- 6.2 sampling and data collection
c6b = T('Sampling and data collection methods: questionnaires, traffic counts and river measurements', 'sampling data collection questionnaires traffic counts river measurements')
build(c6b, {
    'terms': [
        ('random sampling', 'choosing sample points so that every member of the population has an equal chance of being selected, for example using random numbers'),
        ('systematic sampling', 'choosing samples at regular intervals, for example every 10th person or every 50 m'),
        ('stratified sampling', 'dividing the population into groups and sampling each group in proportion to its size'),
        ('opportunistic sampling', 'choosing people or sites that are convenient or willing to take part'),
        ('closed question', 'a question with a fixed set of answers to choose from, such as yes/no or tick boxes'),
        ('open question', 'a question that allows people to answer in their own words'),
        ('bias', 'a distortion of results caused by the way data is collected or the sample is chosen'),
        ('transect', 'a line along which measurements or observations are made at intervals'),
        ('quadrat', 'a square frame used to sample an area, for example of vegetation or beach sediment'),
        ('clinometer', 'an instrument used to measure the angle of a slope'),
    ],
    'mcq': [
        ('Asking every 10th person who walks past is an example of', 'systematic sampling', ['random sampling', 'stratified sampling', 'opportunistic sampling'], '[1]'),
        ('Which equipment is used to measure river velocity cheaply?', 'A float and a stopwatch over a measured distance', ['A clinometer', 'A quadrat', 'A rain gauge'], '[1]'),
        ('Which question is closed?', 'How often do you visit this shopping centre? Daily / Weekly / Monthly / Rarely', ['Why do you visit this shopping centre?', 'What do you think of the town?', 'Describe your journey here.'], '[1]'),
        ('Why should depth be measured at several points across a river channel?', 'The bed is uneven, so a mean depth is more accurate', ['To measure velocity', 'Because the river is always the same depth', 'To find the width'], '[1]'),
        ('Which sampling method best ensures each age group is represented in proportion to the population?', 'Stratified sampling', ['Opportunistic sampling', 'Asking only friends', 'Systematic sampling of one street'], '[1]'),
    ],
    'explain': [
        ('Explain one advantage and one disadvantage of random sampling.', 'Advantage: avoids bias because every point has an equal chance. Disadvantage: may miss important areas or give an uneven spread, and some points may be inaccessible.', '1 mark each [2]'),
        ('Explain how to measure the width and depth of a river.', 'Stretch a tape across the river from water edge to water edge to measure width; measure depth with a metre rule at equal intervals (e.g. every 50 cm) across the channel and calculate the mean.', '1 mark width; 1 mark depth at intervals; 1 mark mean [3]'),
        ('Explain how a questionnaire could be designed to avoid bias.', 'Use clear, neutral questions; mostly closed questions with an “other” option; avoid leading questions; sample at different times and places; pilot the questionnaire.', '1 mark each up to [3]'),
        ('Explain why the velocity of a river should be measured more than once at each site.', 'Floats can be caught by obstacles or wind, so repeating three times and taking the mean reduces the effect of anomalies and improves reliability.', '1 mark reason; 1 mark mean/reliability [2]'),
    ],
    'claims': [
        ('Opportunistic sampling is the least biased method.', False, 'It only includes people or places that are convenient, so it is often the most biased.'),
        ('Taking more readings at each site generally improves reliability.', True, 'Means of repeated readings reduce the effect of errors and anomalies.'),
        ('A pedestrian count of one minute at each site is enough to give reliable results.', False, 'Counts that short are easily affected by chance groups; 5-10 minutes repeated at different times is better.'),
    ],
})


@c6b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6b_river(r, D):
    w = round(r.uniform(1.6, 6.0), 1)
    n = 6 if D >= 3 else 5
    depths = [0] + [r.randint(8, 60) for _ in range(n - 2)] + [0]
    inner = depths[1:-1]
    md = mean(depths)
    times = [round(r.uniform(6, 30), 1) for _ in range(3)]
    dist = 10
    mt = mean(times)
    v = dist / mt
    area = w * md / 100
    Q = area * v
    stem = (f'Students measured a river at one site. Width = {fmt(w, 1)} m. Depths (cm) at equal intervals from bank to bank: ' + ', '.join(map(str, depths)) +
            f'. A float took ' + ', '.join(fmt(t, 1) for t in times) + f' seconds to travel {dist} m in three trials.')
    if D == 1:
        opts, a = mcq(r, f'{dp(md, 1)} cm', [f'{dp(mean(inner), 1)} cm', f'{max(depths)} cm', f'{dp(sum(depths) / 2, 1)} cm'])
        return {'stem': stem + ' What is the mean depth, including both banks?', 'options': opts, 'answer': a, 'key': f'{sum(depths)} ÷ {n} = {dp(md, 1)} cm. [1]'}
    parts = [
        lambda r: ('Calculate the mean depth in cm (include the zero readings at the banks).', f'{dp(md, 1)} cm', f'{sum(depths)} ÷ {n} = {dp(md, 1)} cm [1]'),
        lambda r: ('Calculate the mean time and then the velocity in m/s.', f'mean time {dp(mt, 1)} s; velocity {dp(v, 2)} m/s', f'({"+".join(fmt(t, 1) for t in times)}) ÷ 3 = {dp(mt, 1)} s; {dist} ÷ {dp(mt, 1)} = {dp(v, 2)} m/s [2]'),
        lambda r: ('Calculate the cross-sectional area in m².', f'{dp(area, 3)} m²', f'{fmt(w, 1)} m × {dp(md / 100, 3)} m = {dp(area, 3)} m² [2]'),
        lambda r: ('Calculate the discharge.', f'{dp(Q, 3)} m³/s', f'area × velocity = {dp(area, 3)} × {dp(v, 2)} = {dp(Q, 3)} cumecs [1]'),
        lambda r: ('Suggest two reasons why the float times varied.', 'The float was caught in eddies or by vegetation; wind; different paths across the channel; reaction time with the stopwatch.', '1 mark each [2]'),
        lambda r: ('Suggest one improvement to the method of measuring depth.', 'Take more readings at smaller intervals; use the same person to read the metre rule; read at the water surface at eye level.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6b_strat(r, D):
    grp = r.choice([('age group', ['under 18', '18-40', '41-64', '65 and over']), ('area of the town', ['CBD', 'inner city', 'suburbs', 'rural-urban fringe']),
                    ('land use type', ['woodland', 'farmland', 'urban', 'water'])])
    name, cats = grp
    pops = [r.randint(5, 40) * 100 for _ in cats]
    tot = sum(pops)
    n = r.choice([40, 50, 60, 80, 100])
    shares = [p / tot * n for p in pops]
    rounded = [round(s) for s in shares]
    stem = f'Students want a stratified sample of {n} people (or sites) from a population divided by {name}: ' + ', '.join(f'{c} {nf(p)}' for c, p in zip(cats, pops)) + f' (total {nf(tot)}).'
    i = r.randrange(len(cats))
    if D == 1:
        opts, a = mcq(r, str(rounded[i]), [str(x) for x in {rounded[i] + 3, max(1, rounded[i] - 2), n // len(cats), rounded[i] * 2} if x != rounded[i]])
        return {'stem': stem + f' How many should be sampled from “{cats[i]}”?', 'options': opts, 'answer': a, 'key': f'{nf(pops[i])} ÷ {nf(tot)} × {n} = {fmt(round(shares[i], 2), 2)} ≈ {rounded[i]}. [1]'}
    parts = [
        lambda r: (f'Calculate how many should be sampled from each {name}.', '; '.join(f'{c} {x}' for c, x in zip(cats, rounded)) + (f' (rounded; total {sum(rounded)})' if sum(rounded) != n else ''),
                   f'each group ÷ {nf(tot)} × {n}; 1 mark for two correct, 2 marks all correct [2]'),
        lambda r: ('Explain why stratified sampling is suitable here.', 'Each group is represented in proportion to its size, so the sample is more representative than random or opportunistic sampling.', '1 mark proportional; 1 mark representative [2]'),
        lambda r: ('Explain how the students could choose the individuals within each group without bias.', 'Use random numbers (or a systematic interval) within each group rather than choosing friends or convenient people.', '1 mark method; 1 mark avoids bias [2]'),
        lambda r: ('Suggest one problem the students may face in collecting this sample.', 'People may refuse to answer; some groups are harder to find at certain times; time constraints.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6b.add('C3', (1, 2, 3, 4), 'numerical')
def c6b_count(r, D):
    c = city(r)
    mins = r.choice([5, 10, 15])
    sites = [f'Site {i + 1}' for i in range(5)]
    counts = sorted((r.randint(4, 90) for _ in sites), reverse=True)
    if len(set(counts)) < 5:
        return None
    i = r.randrange(5)
    per_hr = counts[i] * 60 / mins
    stem = f'Students counted pedestrians for {mins} minutes at five sites along a transect away from the centre of {c}: ' + ', '.join(f'{s} {x}' for s, x in zip(sites, counts)) + '.'
    if D == 1:
        opts, a = mcq(r, fmt(per_hr, 1), [str(counts[i]), fmt(counts[i] * mins, 1), fmt(counts[i] / mins, 2)])
        return {'stem': stem + f' What is the equivalent number of pedestrians per hour at {sites[i]}?', 'options': opts, 'answer': a, 'key': f'{counts[i]} × 60 ÷ {mins} = {fmt(per_hr, 1)}. [1]'}
    parts = [
        lambda r: (f'Convert the count at {sites[i]} to pedestrians per hour.', fmt(per_hr, 1), f'{counts[i]} × (60 ÷ {mins}) [1]'),
        lambda r: ('Calculate the mean count per site.', dp(mean(counts)), f'{sum(counts)} ÷ 5 [1]'),
        lambda r: ('Suggest why the count should be repeated at different times of day.', 'Pedestrian numbers vary (e.g. lunchtime peaks), so repeating gives a fairer, more representative picture.', '[2]'),
        lambda r: ('Describe how the students should record their counts.', 'Using a tally chart on a recording sheet, noting site, time, date and weather, counting people passing in both directions past a fixed point.', '1 mark tally; 1 mark consistent rules [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


@c6b.add('C4', (2, 3, 4, 5), 'case')
def c6b_quest(r, D):
    c = city(r)
    qs = [('Q1: Don’t you agree that the new shopping centre is ugly?', 'It is a leading question that suggests the answer, causing bias; ask “What is your opinion of the new shopping centre?” with a rating scale.'),
          ('Q2: How old are you?', 'It may be sensitive; use age bands (e.g. under 18, 18-40, 41-64, 65+) instead.'),
          ('Q3: How far have you travelled?', 'Answers will be hard to compare; give distance bands (0-1 km, 1-5 km, over 5 km) or ask for the town or postcode.'),
          ('Q4: Why do you come here?', 'An open question giving answers that are hard to group; offer tick-box options plus “other”.'),
          ('Q5: How often do you visit? Often / Sometimes', 'Categories are vague and overlapping; use daily, weekly, monthly, less often.')]
    pick = r.sample(qs, 3)
    stem = f'Students in {c} designed a questionnaire to investigate the sphere of influence of a shopping centre. They asked the first 15 people they met outside one shop at 10:00 on a Monday. Their questions included: ' + ' '.join(q for q, _ in pick)
    parts = [
        lambda r: ('Identify a problem with each of the questions shown and suggest how it could be improved.', ' '.join(f'{q.split(":")[0]}: {w}' for q, w in pick), '1 mark problem and 1 mark improvement for each question [6]'),
        lambda r: ('Explain why their sampling method may give biased results.', 'Only 15 people, at one place, one time and one day: weekday morning shoppers (e.g. retired people) are over-represented; opportunistic sampling.', '1 mark each point up to [3]'),
        lambda r: ('Suggest an improved sampling strategy.', 'Systematic sampling of every 10th person at several entrances, at different times on weekdays and weekends, with a sample of at least 50.', '1 mark method; 1 mark times/places; 1 mark size [3]'),
        lambda r: ('Explain why a pilot study would help.', 'Testing the questionnaire on a few people would reveal unclear or leading questions before the main survey.', '[2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


# --------------------------------------------------------------- 6.3 presenting data
GRAPH_CHOICE = [
    ('the percentage of shoppers using each type of transport', 'pie chart or divided bar graph', 'the data are parts of a whole that add up to 100%'),
    ('river width at ten sites at increasing distances downstream', 'scatter graph (or line graph) of width against distance', 'it shows the relationship between two continuous variables'),
    ('the number of vehicles each hour from 07:00 to 19:00', 'line graph', 'the data are continuous over time and show change'),
    ('pedestrian counts at sites located across a town centre', 'located bar graphs or proportional circles on a map', 'they show both the values and their location, revealing the spatial pattern'),
    ('where shoppers have travelled from to reach a shopping centre', 'desire-line map', 'lines from each origin to the centre show direction and distance of journeys'),
    ('the percentage of workers in primary, secondary and tertiary jobs in several countries', 'triangular graph', 'three percentages that add to 100% can be plotted as one point per country'),
    ('the frequency of wind directions over a month', 'wind rose', 'it shows the number of days from each compass direction'),
    ('air temperatures recorded at many points across a school site', 'isoline map', 'lines join points of equal value to show a continuous pattern across an area'),
    ('environmental quality scores for each ward of a city', 'choropleth map', 'shading shows values for areas and the spatial pattern'),
]

c6c = T('Presenting fieldwork data: choosing and drawing suitable graphs and maps', 'presenting fieldwork data graphs maps')
build(c6c, {
    'terms': [
        ('located bar graph', 'a bar graph drawn on a map at the place where the data were collected'),
        ('proportional circles', 'circles drawn on a map whose areas are proportional to the values they represent'),
        ('desire-line map', 'a map with straight lines drawn from the origin to the destination of journeys'),
        ('isoline map', 'a map with lines joining places of equal value, such as temperature or pedestrian numbers'),
        ('dispersion graph', 'a graph that shows each value as a dot along a scale, showing the spread of the data'),
        ('cross-section diagram', 'a scaled side view of a river channel or slope drawn from measurements'),
        ('radar graph', 'a graph with axes radiating from a centre, used to compare several scores such as an environmental quality survey'),
        ('kite diagram', 'a graph showing how the percentage cover of species changes along a transect'),
    ],
    'mcq': [
        ('Which technique is best for showing the shape of a river channel?', 'A cross-section diagram drawn to scale', ['A pie chart', 'A wind rose', 'A desire-line map'], '[1]'),
        ('In a proportional circle map, the size of each circle is based on', 'the square root of the value, so the area represents the value', ['the value itself as the radius', 'the colour of the area', 'the number of sites'], '[1]'),
        ('Which graph best shows change in pedestrian numbers along a transect?', 'A line graph of count against distance', ['A pie chart', 'A triangular graph', 'A wind rose'], '[1]'),
        ('A pie chart sector representing 30% has an angle of', '108°', ['30°', '90°', '120°'], '30 × 3.6 = 108°. [1]'),
    ],
    'explain': [
        ('Explain why located bar graphs are useful for presenting fieldwork data.', 'They show the values and where they were collected, so spatial patterns such as a decrease away from the CBD can be seen.', '1 mark values + location; 1 mark pattern [2]'),
        ('Explain the rules for drawing an accurate graph.', 'A title; labelled axes with units; a regular, suitable scale; accurately plotted points; a key if needed; neat lines or bars.', '1 mark each up to [3]'),
        ('Explain one advantage and one disadvantage of proportional circles.', 'Advantage: show size and location clearly. Disadvantage: large circles can overlap and hide others, and areas are hard to compare accurately by eye.', '1 mark each [2]'),
        ('Explain why it is helpful to use more than one presentation technique.', 'Different techniques show different things – a map shows location and pattern, a scatter graph shows relationship – so together they give a fuller picture.', '1 mark each [2]'),
    ],
    'claims': [
        ('A line graph is suitable for data from unrelated categories such as types of shop.', False, 'Separate categories should be shown as a bar graph; a line implies continuity.'),
        ('A scatter graph can show whether two variables are related.', True, 'The pattern of points (and a best-fit line) shows the strength and direction of correlation.'),
        ('Pie charts are good for showing change over time.', False, 'Pie charts show parts of a whole at one time; line or bar graphs show change over time.'),
    ],
})


@c6c.add('C2', (1, 2, 3, 4), 'explain')
def c6c_choose(r, D):
    data, tech, why = r.choice(GRAPH_CHOICE)
    if D == 1:
        opts, a = mcq(r, cap(tech), [cap(t) for _, t, _ in r.sample([g for g in GRAPH_CHOICE if g[1] != tech], 3)])
        return {'stem': f'Which technique is most suitable for presenting {data}?', 'options': opts, 'answer': a, 'key': f'{cap(tech)}: {why}. [1]'}
    return {'stem': f'Suggest a suitable technique for presenting {data}, and justify your choice.', 'answer': f'{cap(tech)}, because {why}.', 'key': '1 mark technique; 1 mark justification [2]', 'marks': 2}


@c6c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6c_circles(r, D):
    sites = ['A', 'B', 'C', 'D']
    vals = r.sample([16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225], 4)
    k = r.choice([0.1, 0.2, 0.25])
    ref = max(vals)
    stem = f'Students plan to show pedestrian counts at four sites using proportional circles. Counts: ' + ', '.join(f'Site {s} {v}' for s, v in zip(sites, vals)) + f'. The radius (cm) will be calculated as {fmt(k, 2)} × √(count).'
    rad = [k * math.sqrt(v) for v in vals]
    i = r.randrange(4)
    if D == 1:
        opts, a = mcq(r, f'{fmt(round(rad[i], 2), 2)} cm', [f'{fmt(round(k * vals[i], 2), 2)} cm', f'{fmt(round(math.sqrt(vals[i]), 2), 2)} cm', f'{fmt(round(rad[i] * 2, 2), 2)} cm', f'{fmt(round(rad[i] * 1.5, 2), 2)} cm', f'{fmt(round(rad[i] / 2, 2), 2)} cm'])
        return {'stem': stem + f' What radius should the circle for Site {sites[i]} have?', 'options': opts, 'answer': a, 'key': f'√{vals[i]} = {fmt(math.sqrt(vals[i]), 0)}; × {fmt(k, 2)} = {fmt(round(rad[i], 2), 2)} cm. [1]'}
    parts = [
        lambda r: ('Calculate the radius of each circle.', '; '.join(f'Site {s} {fmt(round(x, 2), 2)} cm' for s, x in zip(sites, rad)), f'{fmt(k, 2)} × √count for each; 1 mark for two correct, 2 for all [2]'),
        lambda r: ('Explain why the radius is calculated from the square root of the count.', 'The area of a circle is proportional to the radius squared, so using the square root makes the area (what the eye sees) proportional to the count.', '1 mark area ∝ r²; 1 mark area represents value [2]'),
        lambda r: (f'Calculate how many times larger the area of the largest circle is than the smallest.', f'{dp(max(vals) / min(vals), 2)} times', f'{max(vals)} ÷ {min(vals)} [1]'),
        lambda r: ('Suggest one problem with proportional circles and how to avoid it.', 'Large circles may overlap or cover the map; place them carefully, use a smaller constant, or draw them beside the map with leader lines.', '1 mark problem; 1 mark solution [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6c_pie(r, D):
    cats = r.choice([['car', 'bus', 'walk', 'bicycle', 'train'], ['food', 'clothes', 'services', 'leisure'], ['under 1 km', '1-5 km', '5-10 km', 'over 10 km']])
    n = r.choice([40, 50, 60, 80])
    cuts = sorted(r.sample(range(1, n), len(cats) - 1))
    cnt = [b - a for a, b in zip([0] + cuts, cuts + [n])]
    stem = f'In a questionnaire, {n} shoppers answered one question. Results: ' + ', '.join(f'{c} {x}' for c, x in zip(cats, cnt)) + '.'
    ang = [x / n * 360 for x in cnt]
    pc = [x / n * 100 for x in cnt]
    i = r.randrange(len(cats))
    if D == 1:
        opts, a = mcq(r, f'{dp(ang[i])}°', [f'{cnt[i]}°', f'{dp(pc[i])}°', f'{dp(ang[i] / 2)}°'])
        return {'stem': stem + f' What angle should the “{cats[i]}” sector of a pie chart be?', 'options': opts, 'answer': a, 'key': f'{cnt[i]} ÷ {n} × 360 = {dp(ang[i])}°. [1]'}
    parts = [
        lambda r: ('Calculate the percentage for each category.', '; '.join(f'{c} {dp(p)}%' for c, p in zip(cats, pc)), f'count ÷ {n} × 100 [2]'),
        lambda r: ('Calculate the angle for each sector of a pie chart.', '; '.join(f'{c} {dp(a)}°' for c, a in zip(cats, ang)), f'count ÷ {n} × 360; check total 360° [2]'),
        lambda r: ('Describe how to draw the pie chart accurately.', 'Draw a circle and a radius from the centre to 12 o’clock; measure each angle clockwise with a protractor, largest first; label or shade each sector with a key and add a title.', '1 mark method; 1 mark labelling [2]'),
        lambda r: ('Suggest an alternative way of presenting these results.', 'A bar graph or divided bar graph, which is easier to draw and compare accurately.', '1 mark technique; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 6.4 analysing, concluding, evaluating
c6d = T('Analysing results, drawing conclusions and evaluating the enquiry', 'analysing results conclusions evaluating enquiry')
build(c6d, {
    'terms': [
        ('conclusion', 'a summary of what the results show, stating whether the hypothesis is supported, partly supported or rejected'),
        ('anomaly', 'a result that does not fit the general pattern of the other data'),
        ('reliability', 'how consistent the results are if the investigation were repeated in the same way'),
        ('accuracy', 'how close a measurement is to the true value'),
        ('evaluation', 'judging the strengths and weaknesses of the methods, data and conclusions and suggesting improvements'),
        ('correlation', 'a relationship between two variables, which can be positive, negative or absent'),
        ('Spearman’s rank correlation', 'a statistical test giving a value from −1 to +1 for the strength and direction of a relationship between two sets of ranked data'),
        ('limitation', 'a weakness of the investigation that reduces confidence in the conclusion'),
    ],
    'mcq': [
        ('If most results fit the hypothesis but one site does not, the best conclusion is', 'the hypothesis is largely supported, with one anomaly', ['the hypothesis is completely rejected', 'the data cannot be used', 'the hypothesis is proved true everywhere'], '[1]'),
        ('Which of these would most improve reliability?', 'Repeating the measurements on several days and calculating means', ['Using a different method at each site', 'Collecting data at one site only', 'Ignoring anomalies without checking them'], '[1]'),
        ('A Spearman’s rank value of −0.89 shows', 'a strong negative correlation', ['a weak positive correlation', 'no correlation', 'a strong positive correlation'], '[1]'),
        ('Which is a limitation of collecting data on only one day?', 'The results may not represent typical conditions', ['It makes the results more reliable', 'It removes all anomalies', 'It increases the sample size'], '[1]'),
    ],
    'explain': [
        ('Explain why it is important to identify anomalies in fieldwork results.', 'They may be caused by errors or unusual local conditions; identifying and explaining them prevents wrong conclusions and suggests where to re-measure.', '1 mark cause; 1 mark effect on conclusion [2]'),
        ('Explain the difference between accuracy and reliability.', 'Accuracy is how close a measurement is to the true value; reliability is whether the same results would be obtained if the investigation were repeated.', '1 mark each [2]'),
        ('Explain why the conclusion of a fieldwork enquiry should refer to the data.', 'Quoting values, trends and anomalies provides evidence for accepting or rejecting the hypothesis and shows the strength of the relationship.', '1 mark evidence; 1 mark judgement supported [2]'),
        ('Explain how the sample size can affect the conclusion of an enquiry.', 'A small sample may be unrepresentative and easily distorted by anomalies, so the conclusion is less reliable; a larger sample gives more confidence.', '1 mark small sample problem; 1 mark larger sample benefit [2]'),
    ],
    'claims': [
        ('A strong correlation proves that one variable causes the other.', False, 'Correlation shows a relationship; another factor could cause both.'),
        ('Evaluation should include suggestions for improving the investigation.', True, 'Improvements to methods, sampling and timing show understanding of the limitations.'),
        ('If a result does not fit the pattern it should always be deleted.', False, 'Anomalies should be checked and explained; deleting them without reason can bias the conclusion.'),
    ],
})


@c6d.add('C3', (2, 3, 4, 5), 'numerical')
def c6d_conclude(r, D):
    ctx = r.choice([('distance from the CBD (m)', 'pedestrians per 10 minutes', 'Pedestrian numbers decrease with distance from the centre of the CBD.', -1),
                    ('distance downstream (km)', 'river velocity (m/s × 100)', 'River velocity increases with distance downstream.', 1),
                    ('distance from the car park (m)', 'footpath width (cm)', 'Footpath erosion decreases with distance from the car park.', -1),
                    ('distance along the beach (m)', 'mean pebble length (mm)', 'Pebble size decreases in the direction of longshore drift.', -1)])
    x, y, hyp, sgn = ctx
    n = 8
    xs = [i * r.choice([50, 100, 1]) for i in range(1, n + 1)] if 'km' not in x else list(range(1, n + 1))
    base = r.randint(40, 120)
    step = r.randint(5, 12)
    ys = [max(2, base + sgn * step * i + r.randint(-4, 4)) for i in range(n)]
    anom = r.randrange(2, n - 1)
    ys[anom] += -sgn * r.randint(25, 40)
    ys[anom] = max(2, ys[anom])
    stem = f'A student tested the hypothesis “{hyp}” Results: ' + '; '.join(f'{x.split(" (")[0]} {xi}, {yi}' for xi, yi in zip(xs, ys)) + f' (units: {x.split("(")[1].rstrip(")")} and {y}).'
    trend_ok = (ys[-1] - ys[0]) * sgn > 0
    parts = [
        lambda r: ('Describe what the results show.', f'Generally {"an increase" if sgn > 0 else "a decrease"} in {y.split(" (")[0]} from {ys[0]} to {ys[-1]} as {x.split(" (")[0]} increases, with one result ({xs[anom]}, {ys[anom]}) not fitting the pattern.', '1 mark trend; 1 mark data; 1 mark anomaly [3]'),
        lambda r: ('Identify the anomaly and suggest a reason for it.', f'({xs[anom]}, {ys[anom]}): possibly a measurement or recording error, or a local factor (e.g. a shop entrance, tributary, path junction or groyne) at that site.', '1 mark anomaly; 1 mark plausible reason [2]'),
        lambda r: ('State a conclusion about the hypothesis. Use data to support your answer.', ('Largely supported: ' if trend_ok else 'Not supported: ') + f'{ys[0]} at the first site and {ys[-1]} at the last, apart from the anomaly.', '1 mark judgement; 1 mark supporting data [2]'),
        lambda r: ('Suggest two ways the student could improve the reliability of this investigation.', 'Repeat the data collection on several days or times; take more readings at each site and use means; increase the number of sites; use the same equipment and person throughout.', '1 mark each [2]'),
        lambda r: ('Explain why the conclusion should be treated with caution.', 'Only eight sites on one occasion; one anomaly; conditions may differ at other times; correlation does not prove cause.', '1 mark each up to [3]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6d.add('C3', (2, 3, 4, 5), 'numerical')
def c6d_spear(r, D):
    n = r.choice([6, 7, 8])
    xs = r.sample(range(1, 40), n)
    sgn = r.choice([1, -1])
    ys = [round(50 + sgn * 2 * x + r.uniform(-15, 15)) for x in xs]
    if len(set(ys)) < n:
        return None
    rx = {v: i + 1 for i, v in enumerate(sorted(xs, reverse=True))}
    ry = {v: i + 1 for i, v in enumerate(sorted(ys, reverse=True))}
    d2 = sum((rx[a] - ry[b]) ** 2 for a, b in zip(xs, ys))
    rs = 1 - 6 * d2 / (n ** 3 - n)
    lab = r.choice([('distance from the CBD (100 m)', 'number of shops'), ('distance from source (km)', 'channel width (dm)'), ('distance from the car park (×10 m)', 'litter count')])
    stem = f'A student calculated Spearman’s rank correlation for {lab[0]} (X) and {lab[1]} (Y) at {n} sites: ' + '; '.join(f'X {a}, Y {b}' for a, b in zip(xs, ys)) + '.'
    strength = 'strong' if abs(rs) >= 0.7 else 'moderate' if abs(rs) >= 0.4 else 'weak or no'
    direction = 'positive' if rs > 0 else 'negative'
    parts = [
        lambda r: ('Rank both sets of data (1 = highest) and calculate Σd².', f'Σd² = {d2}', 'ranks [1]; d² values and total [1] [2]'.replace('[1]; d² values and total [1] [2]', '1 mark ranks; 1 mark Σd² [2]')),
        lambda r: ('Calculate rs using rs = 1 − 6Σd² ÷ (n³ − n).', f'rs = {fmt(round(rs, 2), 2)}', f'1 − 6 × {d2} ÷ ({n}³ − {n}) = 1 − {6 * d2} ÷ {n ** 3 - n} = {fmt(round(rs, 2), 2)} [2]'),
        lambda r: ('Interpret the value of rs.', f'A {strength} {direction} correlation' + ('.' if strength != 'weak or no' else ' – little relationship.'), '1 mark strength; 1 mark direction [2]'),
        lambda r: ('Explain why a scatter graph should be drawn as well as calculating rs.', 'It shows the pattern visually, reveals anomalies and whether the relationship is linear, which a single number can hide.', '[2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6d.add('C4', (2, 3, 4, 5), 'case')
def c6d_eval(r, D):
    ctx, hyp, meth, eq, samp, risk, pres = _enq(r)
    p = person(r)
    issues = r.sample(['data were collected on one afternoon only', 'only four sites were used', 'different students measured at different sites', 'it rained heavily during the second half of the day',
                       'a sample of 12 people was used', 'readings were taken once at each site'], 2)
    stem = f'{ctx} {p}’s group tested the hypothesis “{hyp}” using {meth}. In their evaluation they note that ' + ' and '.join(issues) + '.'
    parts = [
        lambda r: ('Explain how each of these limitations may have affected the results.', ' '.join(f'Because {i}, the results may not be representative or consistent, which reduces reliability.' for i in issues), '1 mark each limitation explained [2]'),
        lambda r: ('Suggest improvements to the investigation.', 'Collect data on several days and times; use more sites and larger samples; repeat readings and use means; the same person and equipment at each site; avoid bad weather or record it.', '1 mark each improvement up to [3]'),
        lambda r: ('Explain why the group’s conclusion may still be useful.', 'If the pattern is clear and consistent across most sites, it gives evidence about the hypothesis, especially if it agrees with theory or secondary data.', '1 mark pattern evidence; 1 mark comparison with theory/secondary data [2]'),
        lambda r: ('Suggest one further investigation that would extend this enquiry.', 'Repeat in a different season or place; add another variable (e.g. compare with another river/town); use secondary data to compare with past years.', '1 mark suggestion; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


CHAPTERS[6] = [c6a, c6b, c6c, c6d]

# ============================================================== extra C4 multi-step items
for _t, _f in [(c1a, c1a_ni), (c1b, c1b_dep), (c1d, c1d_density), (c1e, c1e_net), (c2a, c2a_hier), (c2b, c2b_transect), (c2c, c2c_urb), (c2d, c2d_traffic),
               (c3a, c3a_table), (c3a, c3a_spear), (c3b, c3b_reg), (c3c, c3c_struct), (c3d, c3d_chain), (c4a, c4a_yield), (c4b, c4b_cal), (c4d, c4d_growth),
               (c5a, c5a_mix), (c5b, c5b_use), (c5c, c5c_co2), (c6b, c6b_river), (c6b, c6b_strat), (c6c, c6c_circles), (c6c, c6c_pie), (c6d, c6d_conclude), (c6d, c6d_spear)]:
    as_c4(_t, _f)
