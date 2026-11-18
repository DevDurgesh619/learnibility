"""CBSE class 11 Economics families: Statistics for Economics chapters 1-4."""
from __future__ import annotations

from qbank import mcq, ar, num, inr, name, two_names, num_distractors, CITIES, GIRLS
from g11_economics_lib import M, W, AR, G, classify, pick_example, odd_one, cp, table, series, f2

S = 'cbse-g11-economics-ch'

# ====================================================================== ch01 Introduction
ACTS = [('A farmer grows wheat to sell in the mandi', 'Production'), ('A tailor stitches shirts for customers', 'Production'),
        ('A bakery makes bread for sale', 'Production'), ('A software engineer writes code for a client', 'Production'),
        ('A family buys a refrigerator for its own use', 'Consumption'), ('A student buys and eats a samosa', 'Consumption'),
        ('A household pays the electricity bill for home use', 'Consumption'), ('A tourist pays for a hotel stay on holiday', 'Consumption'),
        ('A worker receives monthly wages from a factory', 'Distribution'), ('A landlord receives rent for his shop', 'Distribution'),
        ('A depositor earns interest on a bank deposit', 'Distribution'), ('An entrepreneur earns profit from her business', 'Distribution'),
        ('A mother cooks food for her own family', 'Non-economic activity'), ('A student plays cricket with friends for fun', 'Non-economic activity'),
        ('A volunteer teaches children free of charge on Sundays', 'Non-economic activity')]
C1_FACT = [
    ('The basic economic problem that arises because resources are limited relative to wants is called', 'scarcity', ['inflation', 'unemployment', 'distribution'],
     'Scarcity: limited resources with alternative uses against unlimited wants.'),
    ('Which of the following best describes the subject matter of economics?', 'How people make choices in using scarce resources to satisfy wants',
     ['How to earn maximum money', 'How to collect data', 'How the government makes laws'], 'Economics studies choice under scarcity.'),
    ('The study of how national income is divided as wages, rent, interest and profit is called', 'distribution', ['consumption', 'production', 'exchange'],
     'Distribution deals with the sharing of income among factors of production.'),
    ('Using goods and services to satisfy wants directly is called', 'consumption', ['production', 'distribution', 'investment'], 'Consumption = direct satisfaction of wants.'),
    ('A person who buys goods and services for her own use is a', 'consumer', ['producer', 'service holder', 'seller'], 'NCERT: a consumer buys for own use.'),
    ('A person who is employed by someone else and is paid for the work is a', 'service holder', ['consumer', 'producer', 'landlord'], 'NCERT: such a person is a service holder.'),
    ('Activities that are undertaken for earning income are called', 'economic activities', ['non-economic activities', 'social activities', 'leisure activities'],
     'Economic activities are undertaken for monetary gain.'),
]
C1_AR = [
    ('Every economy faces the problem of choice.', 'Resources are scarce and have alternative uses.', 'a', 'Scarcity of resources with alternative uses forces choice.'),
    ('Paying wages to workers is a part of distribution.', 'Distribution deals with how national income is shared among factors of production.', 'a', 'Wages are the factor income of labour.'),
    ('A mother cooking for her family is an economic activity.', 'Economic activities are undertaken for monetary gain.', 'd', 'A is false: no monetary gain is involved; R is true.'),
    ('Scarcity exists only in poor countries.', 'Wants are unlimited everywhere while resources are limited.', 'd', 'A is false: scarcity is universal; R is true.'),
    ('A consumer and a producer are both economic agents.', 'Both take economic decisions about the use of resources.', 'a', 'R explains why both are economic agents.'),
]
C1_WR = [
    ('Explain why scarcity is the root of all economic problems.', 'Wants are unlimited but resources are limited and have alternative uses; so people must choose what to produce, how and for whom. Without scarcity there would be no need to economise or choose.',
     '1 mark: meaning of scarcity; 1 mark: alternative uses; 1 mark: link to choice.'),
    ('Distinguish between consumption and production with one example each.', 'Consumption: using goods/services to satisfy wants directly (a family eating bread). Production: making goods/services for sale (a baker baking bread).',
     '1 mark each for meaning; 1 mark for examples.'),
    ('What is meant by distribution in economics? Give two examples of factor incomes.', 'Distribution: how national income is shared among factors of production; e.g. wages to labour, rent to land, interest to capital, profit to entrepreneur.',
     '1 mark: meaning; 2 marks: two correct examples.'),
    ('"Economics is the study of choice." Explain with an example from a household.', 'A household with a fixed income must choose between alternatives, e.g. spending ₹5,000 on school fees or a new mobile; choosing one means giving up the other.',
     '1 mark: choice due to scarcity; 1 mark: example; 1 mark: opportunity given up.'),
]


def c1_classify(r):
    x, c = cp('c1act', r, ACTS)
    cats = ['Production', 'Consumption', 'Distribution', 'Non-economic activity']
    return mcq(f'Classify the activity: "{x}".', c, [k for k in cats if k != c], f'{x}: {c}.', r)


def c1_budget(r):
    who = name(r)
    inc = r.choice([18000, 22000, 25000, 30000, 35000])
    left = inc - 10000
    for _ in range(50):
        a, b = r.sample([('school fees', 6000), ('a new phone', 9000), ('a family trip', 12000), ('a bicycle', 7000), ('a laptop', 15000), ('a sewing machine', 8000)], 2)
        if a[1] <= left and b[1] <= left and a[1] + b[1] > left:
            break
    else:
        raise ValueError('budget')
    return {'stem': (f'{who}\'s family has a monthly income of {inr(inc)}. After spending {inr(10000)} on essentials, it can spend the rest on either {a[0]} ({inr(a[1])}) '
                     f'or {b[0]} ({inr(b[1])}), but not both. (i) Which economic problem does the family face? (ii) What is the opportunity cost if it chooses {a[0]}? '
                     f'(iii) Why must the family choose?'),
            'answer': f'(i) Scarcity and choice (ii) {b[0]} ({inr(b[1])}), the next best alternative given up (iii) Remaining income {inr(left)} is limited relative to wants.',
            'key': '1 mark each for (i), (ii) and (iii).'}


# st2 meaning and scope of statistics
STAT_SENSE = [('Statistics of unemployment in India for 2023', 'Plural sense (numerical data)'), ('Statistics of rainfall in Kerala over ten years', 'Plural sense (numerical data)'),
              ('Statistics of crime in Delhi', 'Plural sense (numerical data)'), ('Statistics of births and deaths in a district', 'Plural sense (numerical data)'),
              ('Statistics is a science of collecting and analysing data', 'Singular sense (a subject/method)'),
              ('Statistics deals with organisation and presentation of data', 'Singular sense (a subject/method)'),
              ('Statistics helps in drawing conclusions from numerical facts', 'Singular sense (a subject/method)'),
              ('Statistics is studied as a subject in Class 11', 'Singular sense (a subject/method)')]
C2_FACT = [
    ('In the plural sense, statistics means', 'numerical facts or data collected for a purpose', ['the science of collecting data', 'a single number', 'a branch of accounting'],
     'Plural sense: data (e.g., statistics of population).'),
    ('In the singular sense, statistics refers to', 'the methods of collection, organisation, presentation, analysis and interpretation of data', ['a single table of numbers',
     'only the collection of data', 'only graphs and charts'], 'Singular sense: statistical methods.'),
    ('Which is the correct order of stages in a statistical study?', 'Collection → Organisation → Presentation → Analysis → Interpretation',
     ['Analysis → Collection → Presentation → Interpretation → Organisation', 'Presentation → Collection → Analysis → Organisation → Interpretation',
      'Interpretation → Analysis → Organisation → Collection → Presentation'], 'Data are first collected, then organised, presented, analysed and interpreted.'),
    ('Statistics helps an economist mainly by', 'presenting economic facts in a precise and definite form', ['making all economic problems disappear', 'replacing economic theory',
     'deciding moral questions'], 'NCERT: statistics presents facts precisely and helps condense data.'),
    ('Which statement is not a use of statistics in economics?', 'It gives exact results for every individual', ['It helps in policy formulation', 'It helps find relationships between variables',
     'It helps in forecasting'], 'Statistics deals with aggregates, not individuals.'),
]
C2_WR = [
    ('Explain the meaning of statistics in the singular and plural sense with an example of each.', 'Plural: numerical data, e.g. statistics of India\'s population. Singular: the science of collection, organisation, presentation, analysis and interpretation of data.',
     '1 mark each for meaning in both senses; 1 mark for examples.'),
    ('Give any three reasons why statistics is important in economics.', 'Presents facts precisely; condenses mass data into summary measures; helps find relationships (e.g. between price and demand); helps in policy formulation and forecasting.',
     '1 mark each for any three.'),
    ('How does statistics help the government in making economic policy? Give an example.', 'Data on prices, employment, output, poverty help identify problems and design policy; e.g. rising CPI data help decide measures to control inflation.',
     '2 marks: role of data; 1 mark: example.'),
    ('"Statistics helps in understanding economic problems." Explain with reference to unemployment.', 'Data on unemployment by age, region and education show the size and nature of the problem and where action is needed.',
     '1 mark: link; 2 marks: explanation with data.'),
]
C2_AR = [
    ('Statistics helps in formulating economic policies.', 'Policies need facts about the economy presented in numerical form.', 'a', 'Data are the basis of policy.'),
    ('In the plural sense statistics refers to statistical methods.', 'In the plural sense statistics means numerical data.', 'd', 'A is false; plural sense = data.'),
    ('Statistics condenses a mass of data into a few numbers.', 'Averages and percentages summarise large data sets.', 'a', 'R explains A.'),
    ('Interpretation is the first stage of a statistical study.', 'Data must be collected before they can be analysed.', 'd', 'A is false; collection comes first.'),
]

# st3 quantitative/qualitative; limitations
QQ = [('Monthly income of workers', 'Quantitative'), ('Height of students', 'Quantitative'), ('Marks in an economics test', 'Quantitative'),
      ('Price of wheat in different markets', 'Quantitative'), ('Number of members in a family', 'Quantitative'), ('Age of voters', 'Quantitative'),
      ('Gender of employees', 'Qualitative'), ('Honesty of shopkeepers', 'Qualitative'), ('Religion of respondents', 'Qualitative'),
      ('Colour of cars sold', 'Qualitative'), ('Literacy status (literate/illiterate)', 'Qualitative'), ('Beauty of paintings', 'Qualitative')]
LIMITS = [
    ('Statistics does not study individual cases; it deals with', 'aggregates (groups of observations)', ['single individuals only', 'qualitative attributes only', 'exact laws'],
     'Statistics studies aggregates.'),
    ('Which of the following is a limitation of statistics?', 'It ignores qualitative aspects that cannot be measured', ['It condenses data', 'It helps in forecasting',
     'It compares data'], 'Qualities like honesty cannot be measured directly.'),
    ('Statistical results are true', 'only on an average', ['for every single case', 'without any exception', 'only for qualitative data'], 'Statistical laws hold on average.'),
    ('Statistics can be misused when', 'data are collected or presented by people without proper care or with bias', ['data are homogeneous', 'experts analyse the data',
     'averages are used'], 'Misuse arises from careless or biased handling.'),
]
C3_WR = [
    ('Distinguish between quantitative and qualitative data with two examples each.', 'Quantitative: measurable in numbers (income, height). Qualitative: attributes not measured numerically (gender, honesty).',
     '1 mark: distinction; 2 marks: examples.'),
    ('State any three limitations of statistics.', 'Deals with aggregates not individuals; ignores qualitative aspects; results true only on average; can be misused; needs homogeneous data (any three).',
     '1 mark each.'),
    ('"Statistics is like clay; you can make a god or a devil out of it." Explain this limitation.', 'Statistics can be misused: the same data can be twisted by biased selection or presentation to support wrong conclusions.',
     '1 mark: meaning; 2 marks: explanation with example.'),
]
C3_AR = [
    ('Honesty of workers is qualitative data.', 'Qualitative data cannot be measured numerically.', 'a', 'R explains A.'),
    ('Statistics studies individual items.', 'Statistics deals with aggregates.', 'd', 'A is false; R is true.'),
    ('Statistical laws are true only on an average.', 'Statistics deals with groups and not individual cases.', 'a', 'Because results describe groups, they hold on average.'),
]


def c1_case(r):
    from qbank import GIRLS
    who = r.choice(GIRLS)
    city = r.choice(CITIES)
    n = r.choice([50, 60, 80, 100])
    return {'stem': (f'{who}, a Class 11 student in {city}, wants to study how families in her locality spend their income. She plans to ask {n} families about their monthly income, '
                     'the number of members, the type of house and their religion, and then present the data in tables and graphs.\n'
                     '(i) Which of these characteristics are quantitative and which are qualitative? (ii) Name the stages of the statistical study she will follow. '
                     '(iii) State one limitation of the results she will get.'),
            'answer': '(i) Quantitative: monthly income, number of members; qualitative: type of house, religion (ii) collection → organisation → presentation → analysis → interpretation '
                      '(iii) results describe the group on average, not each family; qualitative aspects are only counted.',
            'key': '(i) 2 marks; (ii) 1 mark; (iii) 1 mark.'}


# ====================================================================== ch02 Collection of Data
PS = [('Data collected by a student by interviewing 50 shopkeepers', 'Primary data'), ('Data on household spending gathered personally by an NGO worker', 'Primary data'),
      ('Marks noted by a teacher from her own test', 'Primary data'), ('Responses collected through the investigator\'s own questionnaire', 'Primary data'),
      ('Population figures taken from the Census of India report', 'Secondary data'), ('Employment data taken from an NSSO (NSO) survey report', 'Secondary data'),
      ('Price data taken from the Reserve Bank of India Bulletin', 'Secondary data'), ('GDP figures taken from the Economic Survey', 'Secondary data'),
      ('Data copied from a newspaper report', 'Secondary data')]
C4_FACT = [
    ('Primary data are', 'collected by the investigator for the first time', ['taken from published sources', 'always qualitative', 'always collected by the government'],
     'Primary = first-hand.'),
    ('Secondary data are', 'data already collected and processed by some other agency', ['collected for the first time', 'collected only by interviews', 'always inaccurate'],
     'Secondary = already available.'),
    ('Which of the following is a source of secondary data?', 'Census of India', ['Personal interview', 'Mailed questionnaire', 'Telephone interview'], 'Census reports are published sources.'),
    ('Primary data are more suitable when', 'specific information for a particular purpose is needed', ['very little time is available', 'no money is available',
     'published data fully meet the purpose'], 'Primary data are original and fit the purpose.'),
    ('An advantage of secondary data is that they', 'save time and money', ['are always more accurate', 'fit every purpose exactly', 'need no checking'], 'They are readily available.'),
]
C4_WR = [
    ('Distinguish between primary and secondary data. Give one source of each.', 'Primary: first-hand, original, collected by investigator (e.g. personal interview). Secondary: already collected by others (e.g. Census of India, NSSO reports).',
     '2 marks: two differences; 1 mark: sources.'),
    ('State any three precautions to be taken while using secondary data.', 'Check suitability for the purpose, adequacy, reliability of the agency, units and definitions used, time period (any three).', '1 mark each.'),
    ('Why might a researcher prefer secondary data? Give two reasons.', 'Saves time and cost; covers a large area/long period; collected by experts (any two).', '1½ marks each.'),
]
C4_AR = [
    ('Census reports are a source of secondary data for a researcher.', 'Census data are collected and published by the Registrar General and Census Commissioner of India.', 'a', 'Already published by another agency.'),
    ('Primary data are always cheaper than secondary data.', 'Primary data are collected first-hand.', 'd', 'A is false; primary data usually cost more; R is true.'),
    ('Secondary data must be used with care.', 'They may have been collected for a different purpose.', 'a', 'R explains why care is needed.'),
]
METHODS = [
    ('Which method of collecting data has the lowest cost and can cover a wide area?', 'Mailed questionnaire', ['Personal interview', 'Telephone interview', 'Direct observation'],
     'NCERT: mailed survey is least expensive and covers a wide area.'),
    ('Which method allows the investigator to explain questions and get the highest response rate?', 'Personal interview', ['Mailed questionnaire', 'Telephone interview', 'Secondary sources'],
     'Face-to-face contact gives clarification and high response.'),
    ('Which method cannot be used when respondents are illiterate?', 'Mailed questionnaire', ['Personal interview', 'Telephone interview', 'Group discussion led by an investigator'],
     'Respondents must read and write answers.'),
    ('A limitation of telephone interviews is that', 'they reach only people who have telephones and visual reactions cannot be seen', ['they are the most expensive method',
     'they need respondents to be literate', 'they take the longest time'], 'NCERT limitation of telephone interviews.'),
    ('The interviewer\'s presence may influence the answers in a', 'personal interview', ['mailed questionnaire', 'published report', 'secondary survey'], 'Interviewer bias in personal interviews.'),
    ('A pilot survey is', 'a try-out of the questionnaire on a small group before the main survey', ['the final survey', 'a survey of pilots', 'a census of the whole population'],
     'Pre-testing finds problems in the questionnaire.'),
]
BADQ = [('Don\'t you agree that smoking should be banned?', 'Leading question'), ('Is your school good and are its teachers helpful?', 'Double-barrelled question (two questions in one)'),
        ('How much do you spend on food?', 'Ambiguous question (no time period stated)'), ('What is your exact income and how much tax did you evade?', 'Personal/embarrassing question'),
        ('Shouldn\'t everyone use public transport to save fuel?', 'Leading question'), ('Do you like cricket and football?', 'Double-barrelled question (two questions in one)'),
        ('Do you travel often?', 'Ambiguous question (no time period stated)'), ('How many times did you fail an exam?', 'Personal/embarrassing question')]
Q_RULES = [
    ('A good questionnaire should be', 'short, clear and in a logical order', ['long and detailed', 'full of technical terms', 'made of leading questions'], 'NCERT rules for a questionnaire.'),
    ('Questions in a questionnaire should move from', 'general to specific', ['specific to general', 'difficult to easy', 'personal to general'], 'General to specific; easy to difficult.'),
    ('Which type of question is easiest to tabulate?', 'Closed-ended (multiple choice) question', ['Open-ended question', 'Leading question', 'Double-barrelled question'],
     'Closed-ended answers are pre-coded.'),
]
C5_WR = [
    ('State any three advantages and two disadvantages of personal interviews.', 'Advantages: highest response rate, clarification of questions, supplementary information, observation of reactions. Disadvantages: costly, time-consuming, interviewer bias.',
     '3 marks for advantages, 1 mark for disadvantages (4 marks).'),
    ('Compare the mailed questionnaire and the telephone interview on cost, coverage and response.', 'Mailed: lowest cost, widest coverage, low response, no clarification. Telephone: cheaper than personal, quick, only telephone owners, no visual reactions.',
     '1 mark each for cost, coverage, response; 1 mark for one more point.'),
    ('Why is a pilot survey conducted before the main survey?', 'To test the questionnaire, find unclear questions, estimate time and cost, and train investigators.', '1 mark each for any three (3 marks).'),
    ('List any four rules for preparing a good questionnaire.', 'Short; simple language; logical order (general to specific); avoid leading, ambiguous, double-barrelled and personal questions; prefer closed-ended questions.',
     '1 mark each (4 marks).'),
]
C5_AR = [
    ('A mailed questionnaire gives a low response rate.', 'Many respondents do not return the questionnaire.', 'a', 'R explains A.'),
    ('Leading questions should be avoided in a questionnaire.', 'They suggest the answer to the respondent.', 'a', 'R explains A.'),
    ('Telephone interviews can be used for all households in rural India.', 'Telephone interviews are cheaper than personal interviews.', 'd', 'A is false: not all have phones; R is true.'),
    ('Personal interviews are the cheapest method.', 'The interviewer can clarify questions in a personal interview.', 'd', 'A is false: they are costly; R is true.'),
]


def c5_badq(r):
    q, t = cp('badq', r, BADQ)
    cats = sorted({x for _, x in BADQ})
    return mcq(f'What is wrong with this questionnaire item: "{q}"', t, [c for c in cats if c != t], f'It is a {t.lower()}.', r)


def c5_rewrite(r):
    q, t = cp('badq2', r, BADQ)
    fix = {'Leading question': 'Ask neutrally, e.g. "What is your opinion about banning ...? (Agree/Disagree/No opinion)"',
           'Double-barrelled question (two questions in one)': 'Split it into two separate questions.',
           'Ambiguous question (no time period stated)': 'State the period and units, e.g. "How much did your household spend on food last month (₹)?"',
           'Personal/embarrassing question': 'Avoid it or ask indirectly with ranges, e.g. income groups.'}[t]
    return {'stem': f'Identify the fault in the questionnaire item "{q}" and rewrite it correctly.', 'answer': f'Fault: {t}. Correction: {fix}',
            'key': '1 mark: fault identified; 2 marks: suitable rewritten question.'}


def c5_case(r):
    who = r.choice(GIRLS)
    n = r.choice([200, 300, 500, 800])
    city = r.choice(CITIES)
    lit = r.choice(['many respondents cannot read or write', 'most respondents are daily-wage workers with little time', 'respondents are spread across several villages'])
    return {'stem': (f'{who} is studying the use of LPG cylinders among {n} households in and around {city}. She has a small budget, and {lit}.\n'
                     '(i) Which method of collecting primary data would you suggest? (ii) Give two reasons. (iii) Suggest one question for her questionnaire that is clear and not leading.'),
            'answer': '(i) Personal interview (with a short questionnaire), possibly on a sample (ii) respondents may not fill forms themselves; clarification possible; high response '
                      '(iii) e.g. "Which fuel does your household mainly use for cooking? (LPG / wood / kerosene / other)"',
            'key': '(i) 1 mark; (ii) 2 marks; (iii) 1 mark.'}


# st3 census and sample
SAMP = [('Lottery method', 'Random sampling'), ('Using a table of random numbers', 'Random sampling'), ('Drawing names from a well-mixed box', 'Random sampling'),
        ('Selecting respondents the investigator thinks are typical', 'Non-random sampling'), ('Interviewing whoever passes by a shop', 'Non-random sampling'),
        ('Fixing a quota of 20 men and 20 women and picking anyone who fits', 'Non-random sampling'), ('Selecting only friends and neighbours', 'Non-random sampling')]
CENSUS = [
    ('In a census survey', 'every element of the population is covered', ['only a few elements are covered', 'only secondary data are used', 'only qualitative data are collected'],
     'Census = complete enumeration.'),
    ('In random sampling', 'every individual has an equal chance of being selected', ['the investigator chooses whom he likes', 'only the richest are chosen',
     'only the nearest people are chosen'], 'NCERT definition.'),
    ('A sample survey is preferred to a census when', 'the population is large and time and money are limited', ['complete accuracy for each unit is needed',
     'the population is very small', 'cost does not matter'], 'Sampling saves time and cost.'),
    ('The total group of items about which information is required is called the', 'population (universe)', ['sample', 'variable', 'questionnaire'], 'Population = universe.'),
    ('A good sample should be', 'representative of the population', ['as small as possible regardless of the population', 'chosen by convenience', 'chosen only from one area'],
     'Representative samples give reliable estimates.'),
]
C6_WR = [
    ('Distinguish between a census and a sample survey (any three points).', 'Census covers every unit, sample covers a part; census costly and slow, sample cheaper and quicker; census suitable for small/heterogeneous population; sample has sampling error.',
     '1 mark each.'),
    ('Explain the lottery method of random sampling.', 'Write the name/number of each unit on identical slips, mix them well in a box and draw the required number without looking; each unit has an equal chance.',
     '2 marks: steps; 1 mark: equal chance.'),
    ('Why is a sample survey generally preferred to a census? Give three reasons.', 'Less time and cost; fewer but better-trained investigators give more accurate data; suitable for large or infinite populations; necessary for destructive testing.',
     '1 mark each.'),
    ('Distinguish between random and non-random sampling.', 'Random: each unit has an equal chance, chosen by lottery/random numbers, no bias. Non-random: units chosen by judgement/convenience/quota; selection bias possible.',
     '1½ marks each.'),
]
C6_AR = [
    ('Random sampling is free from personal bias.', 'In random sampling every unit has an equal chance of selection.', 'a', 'R explains A.'),
    ('A census is suitable when the population is very large and time is short.', 'A census covers every unit of the population.', 'd', 'A is false; R is true.'),
    ('The Census of India is a complete enumeration.', 'It is conducted every ten years.', 'b', 'Both true; R does not explain A.'),
]


def c6_chance(r):
    N = r.choice([40, 50, 60, 80, 100, 120, 150, 200])
    n = r.choice([d for d in (2, 4, 5, 8, 10, 20, 25, 30) if d < N])
    from fractions import Fraction
    p = Fraction(n, N)
    return {'stem': f'A class has {N} students. A sample of {n} students is drawn by the lottery method. What is the chance that a particular student is selected?',
            'answer': f'{p.numerator}/{p.denominator}', 'key': f'Each student has an equal chance: {n}/{N} = {p.numerator}/{p.denominator}.',
            'distractors': [f'1/{N}', f'1/{n}', f'{n}/{N + n}' if (n, N + n) != (p.numerator, p.denominator) else f'{n + 1}/{N}']}


# st4 errors, census, NSSO
ERR = [('Difference between a sample estimate and the true population value', 'Sampling error'), ('Respondents refusing to answer', 'Non-sampling error'),
       ('Wrong recording of answers by the investigator', 'Non-sampling error'), ('Mistakes in tabulation and arithmetic', 'Non-sampling error'),
       ('Choosing a sample that does not represent the population (sampling bias)', 'Non-sampling error'), ('Errors caused by badly worded questions', 'Non-sampling error')]


def not_nonsamp(r):
    ns = [x for x, c in ERR if c == 'Non-sampling error']
    three = r.sample(ns, 3)
    good = ERR[0][0]
    return mcq('Which of the following is NOT a non-sampling error?', good, three, f'{good} is the sampling error; the others are non-sampling errors.', r)
C7_FACT = [
    ('The Census of India is conducted every', '10 years', ['5 years', '2 years', '15 years'], 'Decennial census.'),
    ('The Census of India is conducted by the', 'Office of the Registrar General and Census Commissioner, India', ['Reserve Bank of India', 'NITI Aayog', 'Election Commission'],
     'Registrar General and Census Commissioner.'),
    ('The National Sample Survey Office (NSSO) was set up in', '1950', ['1947', '1961', '1991'], 'NSS was established in 1950.'),
    ('NSSO conducts surveys mainly on', 'socio-economic issues such as employment, consumption and literacy', ['only population counts', 'only weather', 'only foreign trade'],
     'NSSO surveys cover socio-economic topics.'),
    ('Sampling error can be reduced by', 'increasing the size of the sample', ['reducing the sample size', 'using leading questions', 'ignoring non-response'],
     'Larger samples estimate the population better.'),
    ('The first complete (synchronous) census in India was held in', '1881', ['1872', '1901', '1951'], 'First synchronous census: 1881.'),
]
C7_AR = [
    ('Sampling error can be reduced by increasing the sample size.', 'A larger sample is closer to the population.', 'a', 'R explains A.'),
    ('Non-sampling errors occur only in sample surveys.', 'Non-sampling errors can occur in census as well as sample surveys.', 'd', 'A is false; R is true.'),
    ('Non-response is a non-sampling error.', 'It arises at the stage of data collection, not from the act of sampling.', 'a', 'R explains A.'),
]


def c7_samp_err(r):
    who = name(r)
    pop = sorted(r.sample(range(100, 900, 25), 5))
    while sum(pop) % 5:
        pop = sorted(r.sample(range(100, 900, 25), 5))
    mu = sum(pop) // 5
    for _ in range(50):
        smp = r.sample(pop, 2)
        if sum(smp) % 2 == 0:
            break
    else:
        raise ValueError('odd')
    m = sum(smp) // 2
    err = m - mu
    units = r.choice(['incomes (₹ per day)', 'weekly pocket money (₹)', 'daily wages (₹)'])
    return {'stem': f'The {units} of five workers are {series(pop)}. {who} takes a sample of two workers with values {smp[0]} and {smp[1]}. Find the sampling error of the sample mean.',
            'answer': f'Sampling error = {m} − {mu} = {num(err)}', 'key': f'Population mean = {sum(pop)}/5 = {mu}; sample mean = {sum(smp)}/2 = {m}; sampling error = sample mean − population mean = {num(err)}.',
            'distractors': num_distractors(err, -err, m, mu)}


# ====================================================================== ch03 Organisation of Data
CLS = [('Population of India in 1991, 2001 and 2011', 'Chronological classification'), ('Production of steel year by year from 2015 to 2024', 'Chronological classification'),
       ('Wheat production in Punjab, Haryana and Uttar Pradesh', 'Spatial classification'), ('Literacy rate in different states of India', 'Spatial classification'),
       ('Workers grouped as male and female', 'Qualitative classification'), ('Students grouped by religion', 'Qualitative classification'),
       ('Families grouped by income: ₹0–10,000, ₹10,000–20,000 …', 'Quantitative classification'), ('Students grouped by marks: 0–10, 10–20 …', 'Quantitative classification'),
       ('Rainfall in Mumbai month by month in 2023', 'Chronological classification'), ('Population of different districts of Kerala', 'Spatial classification'),
       ('Population grouped as literate and illiterate', 'Qualitative classification'), ('Workers grouped by age: 20–30, 30–40 …', 'Quantitative classification')]
VARS = [('Height of a student', 'Continuous variable'), ('Weight of a baby', 'Continuous variable'), ('Time taken to run 100 m', 'Continuous variable'),
        ('Temperature of a city', 'Continuous variable'), ('Monthly income measured to the paisa', 'Continuous variable'),
        ('Number of children in a family', 'Discrete variable'), ('Number of students in a class', 'Discrete variable'), ('Number of cars in a parking lot', 'Discrete variable'),
        ('Number of goals in a match', 'Discrete variable'), ('Number of rooms in a house', 'Discrete variable')]
C8_FACT = [
    ('Classification of data on the basis of time is called', 'chronological classification', ['spatial classification', 'qualitative classification', 'quantitative classification'], 'Time → chronological.'),
    ('Classification of data on the basis of place is called', 'spatial classification', ['chronological classification', 'qualitative classification', 'quantitative classification'], 'Place → spatial.'),
    ('Classification on the basis of an attribute such as gender is', 'qualitative classification', ['quantitative classification', 'spatial classification', 'chronological classification'], 'Attribute → qualitative.'),
    ('The main objective of classification is to', 'arrange raw data into groups with common characteristics so that they are easy to understand', ['collect new data', 'remove all data',
     'make data qualitative'], 'Classification condenses and organises raw data.'),
]
C8_WR = [
    ('What is classification of data? State its objectives.', 'Arranging data into groups/classes by common characteristics; objectives: condensation, comparison, highlighting similarities and differences, making analysis easy.',
     '1 mark: meaning; 2 marks: objectives.'),
    ('Distinguish between spatial and chronological classification with an example each.', 'Spatial: by place (rice output by state). Chronological: by time (India\'s population by census year).', '1½ marks each.'),
    ('Why is raw data difficult to use? How does classification help?', 'Raw data are unorganised and bulky; classification groups them, reduces bulk, and allows comparison and analysis.', '3 marks.'),
]
C9_FACT = [
    ('A variable that can take any value within a range, including fractions, is', 'a continuous variable', ['a discrete variable', 'an attribute', 'a constant'], 'Continuous: any value in a range.'),
    ('A variable that takes only whole-number values that jump from one to the next is', 'a discrete variable', ['a continuous variable', 'an attribute', 'a frequency'], 'Discrete: distinct values.'),
    ('A characteristic that cannot be measured numerically, such as gender, is called', 'an attribute', ['a variable', 'a frequency', 'a class mark'], 'Qualitative characteristic = attribute.'),
]
C9_AR = [
    ('Height is a continuous variable.', 'Height can take any value within a range, including fractional values.', 'a', 'R explains A.'),
    ('Number of students in a class is a continuous variable.', 'A discrete variable takes only whole-number values.', 'd', 'A is false; it is discrete; R is true.'),
    ('Age measured in completed years is often treated as discrete.', 'Age itself is a continuous variable.', 'b', 'Both true; R does not explain A.'),
]


def c10_mark(r):
    w = r.choice([5, 10, 20, 25, 50])
    lo = w * r.randint(1, 12)
    hi = lo + w
    return {'stem': f'Find the class mark (mid-value) of the class interval {lo}–{hi}.', 'answer': num((lo + hi) / 2),
            'key': f'Class mark = (lower limit + upper limit)/2 = ({lo} + {hi})/2 = {num((lo + hi) / 2)}.', 'distractors': num_distractors((lo + hi) / 2, hi - lo, lo + hi, hi)}


def c10_from_marks(r):
    w = r.choice([4, 5, 10, 20])
    m0 = w * r.randint(1, 6) + w / 2
    mids = [m0 + i * w for i in range(4)]
    lo = m0 - w / 2
    return {'stem': f'The mid-values of a frequency distribution are {", ".join(num(m) for m in mids)}. Find the class interval (width) and the first class.',
            'answer': f'Class width {w}; first class {num(lo)}–{num(lo + w)}', 'key': f'Width = difference of consecutive mid-values = {w}; first class = ({num(m0)} − {num(w / 2)}) to ({num(m0)} + {num(w / 2)}) = {num(lo)}–{num(lo + w)}.'}


def c10_inclusive(r):
    w = r.choice([5, 10])
    a = w * r.randint(0, 6)
    cls = [(a + i * w, a + (i + 1) * w - 1) for i in range(4)]
    adj = [(x - 0.5, y + 0.5) for x, y in cls]
    return {'stem': f'Convert the inclusive classes {", ".join(f"{x}–{y}" for x, y in cls)} into exclusive (continuous) classes.',
            'answer': ', '.join(f'{num(x)}–{num(y)}' for x, y in adj),
            'key': 'Gap between upper limit of one class and lower limit of the next = 1; subtract 0.5 from each lower limit and add 0.5 to each upper limit.'}


def c10_freq(r):
    w = r.choice([10, 20])
    k = 4
    lo = w * r.randint(0, 3)
    edges = [lo + i * w for i in range(k + 1)]
    data = [r.randrange(edges[0], edges[-1]) for _ in range(r.choice([16, 18, 20]))]
    fr = [sum(1 for x in data if edges[i] <= x < edges[i + 1]) for i in range(k)]
    cls = [f'{edges[i]}–{edges[i + 1]}' for i in range(k)]
    return {'stem': f'Marks of {len(data)} students are: {series(data)}. Prepare a frequency distribution using exclusive classes {", ".join(cls)}.',
            'answer': '; '.join(f'{c}: {f}' for c, f in zip(cls, fr)),
            'key': f'In exclusive classes the upper limit is excluded (e.g. {edges[1]} goes to {edges[1]}–{edges[2]}). Frequencies {series(fr)} add up to {len(data)}.'}


def c10_width(r):
    w = r.choice([5, 10, 15, 20, 25])
    lo = w * r.randint(2, 20)
    return {'stem': f'What is the class width (magnitude) of the class {lo}–{lo + w}?', 'answer': str(w), 'key': f'Width = upper limit − lower limit = {lo + w} − {lo} = {w}.',
            'distractors': num_distractors(w, lo + w, (2 * lo + w) / 2, w * 2)}


def c10_count_classes(r):
    lo = r.choice([0, 10, 20, 100])
    w = r.choice([5, 10, 20])
    k = r.randint(5, 9)
    hi = lo + k * w
    return {'stem': f'The smallest value in a data set is {lo} and the largest is {hi - 1}. If classes of width {w} starting at {lo} are used, how many classes are needed?',
            'answer': str(k), 'key': f'Range ≈ {hi} − {lo} = {k * w}; number of classes = {k * w}/{w} = {k}.', 'distractors': num_distractors(k, k + 1, k - 1, k * 2)}


C10_FACT = [
    ('In the exclusive method, the upper class limit of a class is', 'excluded from that class', ['included in that class', 'equal to the class mark', 'always zero'],
     'In 10–20, 20 is counted in 20–30.'),
    ('The inclusive method of classification is more suitable for', 'discrete data', ['continuous data', 'qualitative data', 'chronological data'], 'Both limits are included.'),
    ('The number of times a value occurs in a data set is its', 'frequency', ['class mark', 'class width', 'range'], 'Frequency = number of occurrences.'),
    ('Tally marks are used to', 'count frequencies of observations', ['draw graphs', 'compute averages', 'classify by place'], 'Each observation is marked by a stroke.'),
    ('The mid-point of a class is also called its', 'class mark', ['class limit', 'class frequency', 'class width'], 'Class mark = (lower + upper)/2.'),
    ('The difference between the upper and lower limits of a class is', 'class width', ['class mark', 'frequency', 'cumulative frequency'], 'Width = magnitude of class.'),
]
C10_AR = [
    ('In 10–20, 20–30 classes, the value 20 is counted in 20–30.', 'In the exclusive method the upper limit of a class is excluded.', 'a', 'R explains A.'),
    ('Too many classes make a frequency distribution easier to understand.', 'Classification aims to condense data.', 'd', 'A is false; too many classes defeat condensation; R is true.'),
    ('Inclusive classes are converted to exclusive classes before drawing a histogram.', 'A histogram needs continuous class intervals.', 'a', 'R explains A.'),
]


def c11_bivar(r):
    who = name(r)
    sales = ['115–125', '125–135', '135–145']
    ads = ['60–62', '62–64', '64–66']
    cells = [[r.randint(0, 6) for _ in ads] for _ in sales]
    rt = [sum(row) for row in cells]
    ct = [sum(cells[i][j] for i in range(3)) for j in range(3)]
    i, j = r.randrange(3), r.randrange(3)
    rows = [[s] + c + [t] for s, c, t in zip(sales, cells, rt)] + [['Total'] + ct + [sum(rt)]]
    return {'stem': (f'{who} recorded sales (₹ lakh) and advertisement expenditure (₹ thousand) of firms:\n'
                     + table(['Sales \\ Ad. exp.'] + ads + ['Total'], rows) +
                     f'\n(i) How many firms had sales {sales[i]} and advertisement expenditure {ads[j]}? (ii) How many firms had advertisement expenditure {ads[j]}? (iii) What is this kind of table called?'),
            'answer': f'(i) {cells[i][j]} (ii) {ct[j]} (iii) bivariate frequency distribution', 'key': '1 mark each (column total gives the marginal frequency).'}


C11_FACT = [
    ('A frequency distribution of two variables together is called', 'a bivariate frequency distribution', ['a univariate distribution', 'a time series', 'an ogive'], 'Two variables → bivariate.'),
    ('In a bivariate table the row and column totals are called', 'marginal frequencies', ['class marks', 'cumulative frequencies', 'relative frequencies'], 'Totals in the margins.'),
    ('An example of a bivariate distribution is', 'sales and advertisement expenditure of firms', ['heights of students only', 'rainfall in one city by month', 'number of cars sold'],
     'Two variables recorded together.'),
]


# ====================================================================== ch04 Presentation of Data
PARTS = [('the heading that tells what the table is about', 'Title'), ('the headings of the columns', 'Captions'), ('the headings of the rows', 'Stubs'),
         ('the main part that contains the numerical data', 'Body'), ('the place from which the data were obtained', 'Source'),
         ('the line that explains a special feature of the data, placed below the table', 'Note'), ('the number given to identify the table', 'Table number')]
C12_FACT = [
    ('Presenting data in the form of a paragraph is called', 'textual presentation', ['tabular presentation', 'diagrammatic presentation', 'graphic presentation'], 'Data in text.'),
    ('Which form of presentation is most suitable for a large amount of data needing exact values?', 'Tabular presentation', ['Textual presentation', 'Pie diagram', 'Pictogram'],
     'Tables show exact figures systematically.'),
    ('A table in which data are classified by time is a', 'temporal (chronological) table', ['spatial table', 'qualitative table', 'quantitative table'], 'Time-based.'),
    ('A table in which data are classified by place is a', 'spatial table', ['temporal table', 'qualitative table', 'quantitative table'], 'Place-based.'),
]
C12_WR = [
    ('Name the main parts of a table and state the role of any two.', 'Table number, title, captions, stubs, body, unit of measurement, source, note. E.g. captions are column headings; stubs are row headings.',
     '1 mark: parts; 2 marks: roles of two parts.'),
    ('State two advantages of tabular presentation over textual presentation.', 'Easy comparison; data presented concisely; exact figures; helps further analysis (any two).', '1½ marks each.'),
]


def c12_part(r):
    d, p = cp('c12part', r, PARTS)
    others = [x for _, x in PARTS if x != p]
    return mcq(f'In a statistical table, {d} {"are" if d.startswith("the headings") else "is"} called the', p.lower() if p not in ('Table number',) else p, [o.lower() if o != 'Table number' else o for o in r.sample(others, 3)],
               f'{p}: {d}.', r)


def c12_make_table(r):
    city = r.choice(CITIES)
    yrs = [2021, 2022, 2023]
    m = [r.randint(120, 260) for _ in yrs]
    f = [r.randint(100, 240) for _ in yrs]
    text = '; '.join(f'in {y}, {a} boys and {b} girls' for y, a, b in zip(yrs, m, f))
    return {'stem': f'Present the following in a table with a title, captions, stubs and totals: A school in {city} admitted {text}.',
            'answer': table(['Year', 'Boys', 'Girls', 'Total'], [[y, a, b, a + b] for y, a, b in zip(yrs, m, f)] + [['Total', sum(m), sum(f), sum(m) + sum(f)]]),
            'key': 'Marks shared equally among: title and table number; captions and stubs; correct figures; correct row and column totals.'}


DIAG = [('composition of a family budget (food, rent, education …)', 'Pie diagram'), ('India\'s exports year by year over 20 years', 'Arithmetic line graph'),
        ('frequency distribution of marks with continuous classes', 'Histogram'), ('comparison of rice and wheat output in five states', 'Multiple bar diagram'),
        ('population of four cities in one year', 'Simple bar diagram'), ('students in a school split by gender for each class, shown as parts of one bar', 'Sub-divided (component) bar diagram'),
        ('finding the median graphically', 'Ogive'), ('comparing the shape of two frequency distributions on one graph', 'Frequency polygon')]


def c13_choose(r):
    d, t = cp('c13diag', r, DIAG)
    others = sorted({x for _, x in DIAG if x != t})
    return mcq(f'Which diagram is most suitable to show the {d}?', t, r.sample(others, 3), f'{t} suits the {d}.', r)


def c13_pie(r):
    heads = r.choice([['Food', 'Housing', 'Education', 'Clothing', 'Others'], ['Rice', 'Wheat', 'Pulses', 'Oilseeds', 'Others'], ['Agriculture', 'Industry', 'Services']])
    for _ in range(200):
        pct = [r.randint(1, 12) * 5 for _ in heads]
        if sum(pct) == 100:
            break
    else:
        raise ValueError('no pie')
    i = r.randrange(len(heads))
    ang = pct[i] * 3.6
    who = name(r)
    return {'stem': f'{who}\'s data show the percentage shares: ' + ', '.join(f'{h} {p}%' for h, p in zip(heads, pct)) + f'. In a pie diagram, what angle will represent {heads[i]}?',
            'answer': f'{num(ang)}°', 'key': f'Angle = (percentage/100) × 360° = {pct[i]} × 3.6 = {num(ang)}°.', 'distractors': [f'{num(x)}°' for x in (pct[i], ang / 2, ang + 18) if num(x) != num(ang)]}


def c13_pie_val(r):
    tot = r.choice([20000, 24000, 36000, 40000, 48000, 60000, 72000])
    ang = r.choice([30, 45, 60, 72, 90, 120, 144])
    v = tot * ang / 360
    return {'stem': f'In a pie diagram of a family\'s monthly expenditure of {inr(tot)}, the sector for food has an angle of {ang}°. How much is spent on food?',
            'answer': inr(v), 'key': f'Expenditure = (angle/360°) × total = ({ang}/360) × {tot} = {inr(v)}.',
            'distractors': [inr(x) for x in (tot * ang / 100, v * 2, tot - v)]}


C13_FACT = [
    ('In a bar diagram, the width of the bars is', 'kept equal; only the length matters', ['proportional to the value', 'different for each bar', 'equal to the frequency'], 'Bars are one-dimensional.'),
    ('A pie diagram is a', 'circle divided into sectors in proportion to the values', ['set of bars of equal width', 'line joining mid-points', 'cumulative frequency curve'],
     'Angles are proportional to shares.'),
    ('In a pie diagram, the total of all angles is', '360°', ['180°', '100°', '90°'], 'Full circle.'),
    ('A multiple bar diagram is used to', 'compare two or more sets of data side by side', ['show a single value', 'show cumulative frequency', 'find the mode'], 'Groups of adjacent bars.'),
]
C13_AR = [
    ('A pie diagram is suitable to show the composition of a whole.', 'Each sector\'s angle is proportional to its share in the total.', 'a', 'R explains A.'),
    ('Bars in a bar diagram can have different widths to show values.', 'A bar diagram is one-dimensional; only length shows the value.', 'd', 'A is false; R is true.'),
    ('A component bar diagram shows parts of a total.', 'A bar is divided into segments for the parts.', 'a', 'R explains A.'),
]


def c14_cf(r):
    w = r.choice([10, 20])
    f = [r.randint(2, 15) for _ in range(5)]
    cls = [f'{i * w}–{(i + 1) * w}' for i in range(5)]
    lt = [sum(f[:i + 1]) for i in range(5)]
    mt = [sum(f[i:]) for i in range(5)]
    kind = r.choice(['less than', 'more than'])
    if kind == 'less than':
        ans = '; '.join(f'less than {(i + 1) * w}: {c}' for i, c in enumerate(lt))
        key = 'Less than ogive: plot cumulative frequencies against UPPER class limits.'
    else:
        ans = '; '.join(f'more than {i * w}: {c}' for i, c in enumerate(mt))
        key = 'More than ogive: plot cumulative frequencies (from the bottom) against LOWER class limits.'
    return {'stem': f'Classes {", ".join(cls)} have frequencies {series(f)}. Prepare the "{kind}" cumulative frequency table needed for a {kind} ogive.',
            'answer': ans, 'key': key + f' Total = {sum(f)}.'}


def c14_unequal(r):
    f1 = r.randint(4, 20)
    w = r.choice([10, 20])
    big = w * r.choice([2, 3, 4])
    fb = r.randint(10, 40)
    return {'stem': f'In a frequency distribution most classes have width {w}, but one class has width {big} and frequency {fb}. While drawing a histogram, what adjusted frequency (height) should be used for this class?',
            'answer': num(fb * w / big), 'key': f'Adjusted frequency = (frequency/its width) × normal width = ({fb}/{big}) × {w} = {num(fb * w / big)}.',
            'distractors': num_distractors(fb * w / big, fb, fb * big / w, fb / 2)}


C14_FACT = [
    ('A histogram is drawn for', 'a continuous frequency distribution', ['qualitative data', 'time series', 'a discrete series without classes'], 'Rectangles on continuous classes.'),
    ('In a histogram, the area of each rectangle is proportional to', 'the frequency of the class', ['the class mark', 'the cumulative frequency', 'the number of classes'], 'Area ∝ frequency.'),
    ('A frequency polygon is obtained by joining', 'the mid-points of the tops of the rectangles of a histogram', ['the upper limits with cumulative frequencies', 'the corners of the bars',
     'the lower limits with frequencies'], 'Mid-points of the tops.'),
    ('The less than ogive is drawn by plotting cumulative frequencies against', 'upper class limits', ['lower class limits', 'mid-points', 'frequencies'], 'Less than → upper limits.'),
    ('The point where the less than and more than ogives intersect gives the', 'median', ['mean', 'mode', 'range'], 'Intersection = median.'),
    ('The mode of a distribution can be located graphically using a', 'histogram', ['less than ogive', 'pie diagram', 'line graph'], 'From the highest rectangle.'),
]
C14_AR = [
    ('A histogram cannot be drawn for inclusive classes without adjustment.', 'A histogram needs continuous classes.', 'a', 'R explains A.'),
    ('The median can be found from the intersection of two ogives.', 'Half the items lie below the median.', 'a', 'At the intersection cf = N/2.'),
    ('In a histogram, gaps are left between rectangles.', 'Bar diagrams have equal gaps between bars.', 'd', 'A is false: histogram rectangles are adjacent; R is true.'),
]
C15_FACT = [
    ('In an arithmetic line graph (time series graph), time is shown on the', 'X-axis', ['Y-axis', 'both axes', 'neither axis'], 'Time on the horizontal axis.'),
    ('An arithmetic line graph is useful to show', 'changes in a variable over time', ['composition of a whole', 'frequency of classes', 'parts of a bar'], 'Trends over time.'),
    ('When the values to be plotted start far from zero, the vertical axis is broken using a', 'false base line', ['pie sector', 'tally mark', 'class mark'], 'False base line saves space.'),
    ('Two time series with different units can be shown on one graph using', 'two vertical scales (one on each side)', ['a pie diagram', 'a histogram', 'only one scale'], 'Double-axis line graph.'),
]


def c15_trend(r):
    y0 = r.choice([2016, 2017, 2018])
    vals = [r.randint(40, 90) for _ in range(5)]
    i = max(range(1, 5), key=lambda k: vals[k] - vals[k - 1])
    j = min(range(1, 5), key=lambda k: vals[k] - vals[k - 1])
    if vals[i] - vals[i - 1] == vals[j] - vals[j - 1]:
        raise ValueError('flat')
    item = r.choice(['exports (₹ thousand crore)', 'rice output (lakh tonnes)', 'sales of a firm (₹ lakh)'])
    return {'stem': f'Values of {item} for {y0}–{y0 + 4} are {series(vals)}. If these are drawn as an arithmetic line graph, between which two years does the line rise most steeply, and between which does it fall most (or rise least)?',
            'answer': f'Steepest rise: {y0 + i - 1}–{y0 + i} (change {num(vals[i] - vals[i - 1])}); lowest: {y0 + j - 1}–{y0 + j} (change {num(vals[j] - vals[j - 1])})',
            'key': 'Steepness on the graph equals the change between consecutive years; 1½ marks each.'}


C15_AR = [
    ('A line graph is suitable for time series data.', 'It clearly shows the trend of a variable over time.', 'a', 'R explains A.'),
    ('In a time series graph, time is shown on the Y-axis.', 'The dependent variable is shown on the Y-axis.', 'd', 'A is false; time goes on X-axis; R is true.'),
]


def c14_case(r):
    w = 10
    f = [r.randint(3, 12) for _ in range(5)]
    cls = [f'{20 + i * w}–{20 + (i + 1) * w}' for i in range(5)]
    i = max(range(5), key=lambda k: f[k])
    if f.count(f[i]) > 1:
        raise ValueError('tie')
    lt = [sum(f[:k + 1]) for k in range(5)]
    return {'stem': (f'Daily wages (₹ hundred) of {sum(f)} workers: classes {", ".join(cls)}, frequencies {series(f)}.\n'
                     '(i) Which diagram shows this distribution with adjacent rectangles? (ii) Which class has the tallest rectangle? (iii) Write the less than cumulative frequencies. '
                     '(iv) Which graph would you draw from (iii) to locate the median?'),
            'answer': f'(i) Histogram (ii) {cls[i]} (iii) {series(lt)} (iv) less than ogive (read the value at N/2 = {num(sum(f) / 2)})',
            'key': '1 mark each.'}


# ====================================================================== FAMILIES
FAMILIES = {
    S + '01-st1': [M('C1', 'D1', C1_FACT[3:]), M('C1', 'D2', C1_FACT[:3]), G('C2', 'D2', 'mcq', c1_classify), W('C2', 'D3', 'explain', C1_WR[:2], marks=3, kinds=('q3',)),
                   AR('C2', 'D2', C1_AR), G('C3', 'D2', 'mcq', c1_classify), G('C3', 'D3', 'case', c1_budget, marks=3, kinds=('q3',)), G('C3', 'D1', 'mcq', c1_classify),
                   W('C4', 'D3', 'explain', C1_WR[2:], marks=3, kinds=('q3',)), G('C4', 'D4', 'case', c1_budget, marks=3)],
    S + '01-st2': [M('C1', 'D1', C2_FACT[:2] + C2_FACT[3:4]), G('C1', 'D2', 'mcq', pick_example(STAT_SENSE, 'Plural sense (numerical data)', 'In which of the following is "statistics" used in the plural sense (numerical data)?')),
                   M('C2', 'D2', C2_FACT[2:]), W('C2', 'D3', 'explain', C2_WR[:2], marks=3, kinds=('q3',)), AR('C2', 'D3', C2_AR),
                   G('C3', 'D2', 'mcq', pick_example(STAT_SENSE, 'Singular sense (a subject/method)', 'In which of the following is "statistics" used in the singular sense (a method/subject)?')),
                   W('C3', 'D3', 'explain', C2_WR[2:], marks=3, kinds=('q3',)), G('C3', 'D4', 'case', c1_case, marks=4, kinds=('case',)),
                   W('C4', 'D3', 'explain', C2_WR[2:3] + C2_WR[1:2], marks=4, kinds=('q4',)), W('C4', 'D5', 'long', [('"Statistics is the backbone of economic planning." Discuss the importance and scope of statistics in economics.',
                                                                                                                      'Scope: collection, organisation, presentation, analysis, interpretation. Importance: presents facts precisely, condenses data, helps find relationships, policy making, forecasting, testing economic theories; examples from unemployment, inflation, poverty.',
                                                                                                                      '2 marks: meaning/scope; 3 marks: importance with examples; 1 mark: conclusion (6 marks).')], marks=6)],
    S + '01-st3': [G('C1', 'D1', 'mcq', pick_example(QQ, 'Qualitative', 'Which of the following is qualitative data?')), M('C1', 'D2', LIMITS[:2]),
                   G('C2', 'D2', 'mcq', pick_example(QQ, 'Quantitative', 'Which of the following is quantitative data?')), W('C2', 'D3', 'explain', C3_WR[:2], marks=3, kinds=('q3',)),
                   AR('C2', 'D2', C3_AR), M('C3', 'D2', LIMITS[2:]), G('C3', 'D3', 'mcq', odd_one(QQ)), G('C3', 'D4', 'case', c1_case, marks=4, kinds=('case',)),
                   W('C4', 'D3', 'explain', C3_WR[2:], marks=3, kinds=('q3',)), W('C4', 'D4', 'long', [('Explain the meaning of quantitative and qualitative data and discuss any four limitations of statistics with examples.',
                                                                                                         'Meaning with examples; limitations: aggregates only, ignores qualitative aspects, true on average, can be misused, needs homogeneous data, needs expert handling.',
                                                                                                         '2 marks: meaning; 4 marks: four limitations (6 marks).')], marks=6)],
    S + '02-st1': [M('C1', 'D1', C4_FACT[:3]), G('C1', 'D2', 'mcq', pick_example(PS, 'Secondary data', 'Which of the following is secondary data?')),
                   G('C2', 'D2', 'mcq', pick_example(PS, 'Primary data', 'Which of the following is primary data?')), W('C2', 'D3', 'explain', C4_WR[:2], marks=3, kinds=('q3',)),
                   AR('C2', 'D3', C4_AR), M('C3', 'D2', C4_FACT[3:]), G('C3', 'D3', 'mcq', odd_one(PS)), G('C3', 'D1', 'mcq', pick_example(PS, 'Primary data', 'Identify the primary data:')),
                   W('C4', 'D3', 'explain', C4_WR[1:], marks=3, kinds=('q3',)), G('C4', 'D4', 'case', c5_case, marks=4, kinds=('case',))],
    S + '02-st2': [M('C1', 'D2', METHODS[:3]), M('C1', 'D1', Q_RULES), G('C2', 'D2', 'mcq', c5_badq), G('C2', 'D3', 'mcq', c5_badq), AR('C2', 'D2', C5_AR),
                   M('C3', 'D2', METHODS[3:]), G('C3', 'D3', 'explain', c5_rewrite, marks=3, kinds=('q3',)), G('C3', 'D4', 'case', c5_case, marks=4, kinds=('case',)),
                   W('C4', 'D3', 'explain', C5_WR[:2], marks=4, kinds=('q4',)), W('C4', 'D4', 'explain', C5_WR[2:], marks=4, kinds=('q4',)),
                   W('C4', 'D5', 'long', [('You have to study the effect of online classes on students of your city. Explain which method of data collection you will use, how you will design the questionnaire and why you will conduct a pilot survey.',
                                           'Method: sample survey with personal interviews/online questionnaire, justified; questionnaire: short, clear, closed-ended, general to specific, no leading/double questions; pilot survey to test and correct the questionnaire, estimate time and cost.',
                                           '2 marks method; 2 marks questionnaire; 2 marks pilot survey (6 marks).')], marks=6)],
    S + '02-st3': [M('C1', 'D1', CENSUS[:2] + CENSUS[3:4]), G('C1', 'D2', 'mcq', pick_example(SAMP, 'Random sampling', 'Which of the following is a method of random sampling?')),
                   M('C2', 'D2', CENSUS[2:]), W('C2', 'D3', 'explain', C6_WR[:2], marks=3, kinds=('q3',)), AR('C2', 'D3', C6_AR),
                   G('C3', 'D2', 'numerical', c6_chance, marks=1), G('C3', 'D3', 'mcq', pick_example(SAMP, 'Non-random sampling', 'Which of the following is non-random sampling?')),
                   G('C3', 'D4', 'numerical', c6_chance, marks=1), W('C4', 'D3', 'explain', C6_WR[2:], marks=3, kinds=('q3',)),
                   W('C4', 'D4', 'long', [('Distinguish between census and sample methods of data collection. Explain why the sample method is more widely used, with two methods of random sampling.',
                                           'Census vs sample (coverage, cost, time, accuracy); reasons for sample method; lottery method and random number tables explained.',
                                           '2 marks distinction; 2 marks reasons; 2 marks methods (6 marks).')], marks=6)],
    S + '02-st4': [M('C1', 'D1', C7_FACT[:3] + C7_FACT[5:]), M('C1', 'D2', C7_FACT[3:5]), G('C2', 'D2', 'mcq', not_nonsamp),
                   W('C2', 'D3', 'explain', [('Distinguish between sampling and non-sampling errors with examples.', 'Sampling error: difference between sample estimate and population value, reduced by larger samples. Non-sampling errors: errors in data acquisition, non-response, sampling bias; occur in census too.',
                                              '1½ marks each.'),
                                             ('Name two important agencies that collect data at the national level and the kind of data they collect.', 'Census of India (population, literacy, occupation, every 10 years); NSSO/NSO (socio-economic surveys on employment, consumption, literacy, health).',
                                              '1½ marks each.')], marks=3, kinds=('q3',)),
                   AR('C2', 'D2', C7_AR), G('C3', 'D2', 'numerical', c7_samp_err, marks=3, kinds=('q3',)), G('C3', 'D3', 'numerical', c7_samp_err, marks=3),
                   G('C3', 'D1', 'mcq', pick_example(ERR, 'Sampling error', 'Which of the following is a sampling error?')), G('C4', 'D3', 'numerical', c7_samp_err, marks=3),
                   W('C4', 'D4', 'explain', [('A survey finds that average household consumption is 8% lower than the Census-based estimate. Suggest two possible sampling and two non-sampling reasons.',
                                              'Sampling: small sample, unrepresentative selection by chance. Non-sampling: non-response of rich households, wrong recording/recall errors, interviewer bias.',
                                              '1 mark each (4 marks).')], marks=4, kinds=('q4',))],
    S + '03-st1': [G('C1', 'D1', 'mcq', classify(CLS, 'Which type of classification is used in: "{x}"?')), M('C1', 'D2', C8_FACT), G('C2', 'D2', 'mcq', classify(CLS, 'Identify the classification: {x}.')),
                   W('C2', 'D3', 'explain', C8_WR[:2], marks=3, kinds=('q3',)),
                   AR('C2', 'D3', [('Data on wheat output by state is a spatial classification.', 'Spatial classification is based on place.', 'a', 'R explains A.'),
                                   ('Classifying workers by gender is a quantitative classification.', 'Gender is an attribute.', 'd', 'A is false: it is qualitative; R is true.'),
                                   ('Classification makes comparison easier.', 'Similar items are put in the same group.', 'a', 'R explains A.')]),
                   G('C3', 'D2', 'mcq', odd_one(CLS)), W('C3', 'D3', 'explain', C8_WR[2:], marks=3, kinds=('q3',)), G('C3', 'D4', 'mcq', classify(CLS, 'A table shows "{x}". Its classification is')),
                   W('C4', 'D3', 'explain', [('Give one example each of chronological, spatial, qualitative and quantitative classification from Indian economic data.',
                                              'E.g. India\'s GDP 2014–2024 (chronological); rice output by state (spatial); workers by gender (qualitative); farms by size in hectares (quantitative).', '1 mark each (4 marks).')],
                     marks=4, kinds=('q4',)), G('C4', 'D4', 'case', c11_bivar, marks=3)],
    S + '03-st2': [G('C1', 'D1', 'mcq', pick_example(VARS, 'Continuous variable', 'Which of the following is a continuous variable?')), M('C1', 'D2', C9_FACT),
                   G('C2', 'D2', 'mcq', pick_example(VARS, 'Discrete variable', 'Which of the following is a discrete variable?')),
                   W('C2', 'D3', 'explain', [('Distinguish between discrete and continuous variables with two examples each.', 'Discrete: only whole/distinct values (number of children, cars); continuous: any value in a range (height, weight).',
                                              '1 mark distinction; 2 marks examples.'),
                                             ('Why is the frequency distribution of a continuous variable always made with class intervals?', 'A continuous variable can take any value, so individual values rarely repeat; grouping into class intervals is needed.',
                                              '3 marks.')], marks=3, kinds=('q3',)),
                   AR('C2', 'D2', C9_AR), G('C3', 'D2', 'mcq', odd_one(VARS)),
                   G('C3', 'D3', 'mcq', pick_example(VARS, 'Continuous variable', 'Identify the continuous variable:')), G('C3', 'D1', 'mcq', pick_example(VARS, 'Discrete variable', 'Identify the discrete variable:')),
                   W('C4', 'D3', 'explain', [('"Age is a continuous variable, but age in completed years is recorded as discrete." Explain.', 'Age changes continuously over time, but when recorded in completed years only whole numbers occur, so the recorded data behave as discrete.',
                                              '3 marks.')], marks=3, kinds=('q3',)),
                   W('C4', 'D4', 'explain', [('A researcher records (a) number of mobile phones per household and (b) monthly mobile bill (₹). Classify each variable and state how each would be organised into a frequency distribution.',
                                              '(a) discrete: discrete frequency array (0, 1, 2, 3 …); (b) continuous: grouped frequency distribution with class intervals such as ₹0–200, 200–400 …',
                                              '2 marks each (4 marks).')], marks=4, kinds=('q4',))],
    S + '03-st3': [M('C1', 'D1', C10_FACT[2:]), M('C1', 'D2', C10_FACT[:2]), G('C2', 'D2', 'numerical', c10_mark, marks=1), G('C2', 'D3', 'numerical', c10_inclusive, marks=3, kinds=('q3',)),
                   AR('C2', 'D3', C10_AR), G('C3', 'D2', 'numerical', c10_width, marks=1), G('C3', 'D3', 'numerical', c10_freq, marks=4, kinds=('q4',)),
                   G('C3', 'D4', 'numerical', c10_from_marks, marks=3, kinds=('q3',)), G('C3', 'D1', 'numerical', c10_mark, marks=1), G('C3', 'D2', 'numerical', c10_count_classes, marks=1),
                   G('C4', 'D3', 'numerical', c10_freq, marks=4), G('C4', 'D4', 'numerical', c10_from_marks, marks=3),
                   W('C4', 'D5', 'long', [('Explain with examples the exclusive and inclusive methods of forming class intervals. Why must inclusive classes be adjusted before drawing a histogram? Show the adjustment for 10–19, 20–29, 30–39.',
                                           'Exclusive: upper limit excluded (10–20, 20–30); inclusive: both limits included (10–19, 20–29); histogram needs continuity; adjustment ±0.5 → 9.5–19.5, 19.5–29.5, 29.5–39.5.',
                                           '2 marks each method; 2 marks adjustment (6 marks).')], marks=6)],
    S + '03-st4': [M('C1', 'D1', C11_FACT[:2]), M('C1', 'D2', C11_FACT[1:]), G('C2', 'D2', 'case', c11_bivar, marks=3, kinds=('q3',)),
                   W('C2', 'D3', 'explain', [('What is a bivariate frequency distribution? Give one example from economics.', 'A frequency distribution of two variables together, e.g. income and expenditure of households, or sales and advertisement expenditure of firms.',
                                              '2 marks meaning; 1 mark example.')], marks=3),
                   AR('C2', 'D2', [('A bivariate table shows two variables together.', 'Its cells give the joint frequency of the two classes.', 'a', 'R explains A.'),
                                   ('Marginal totals of a bivariate table give univariate distributions.', 'Row totals give the distribution of the row variable.', 'a', 'R explains A.')]),
                   G('C3', 'D3', 'case', c11_bivar, marks=3), G('C4', 'D3', 'case', c11_bivar, marks=4, kinds=('case',))],
    S + '04-st1': [M('C1', 'D1', C12_FACT[:2]), G('C1', 'D2', 'mcq', c12_part), M('C2', 'D2', C12_FACT[2:]), W('C2', 'D3', 'explain', C12_WR, marks=3, kinds=('q3',)),
                   AR('C2', 'D3', [('A table is more suitable than text for large data.', 'Tables arrange data systematically in rows and columns.', 'a', 'R explains A.'),
                                   ('Stubs are column headings.', 'Captions are column headings.', 'd', 'A is false: stubs are row headings; R is true.'),
                                   ('The source of a table should always be stated.', 'It allows the reader to check the reliability of the data.', 'a', 'R explains A.')]),
                   G('C3', 'D2', 'mcq', c12_part), G('C3', 'D3', 'explain', c12_make_table, marks=3, kinds=('q3',)), G('C3', 'D4', 'explain', c12_make_table, marks=3),
                   G('C4', 'D3', 'explain', c12_make_table, marks=4, kinds=('q4',)), G('C3', 'D1', 'mcq', c12_part)],
    S + '04-st2': [M('C1', 'D1', C13_FACT[1:3]), M('C1', 'D2', C13_FACT[::3] + C13_FACT[1:2]), G('C2', 'D2', 'mcq', c13_choose), G('C2', 'D3', 'mcq', c13_choose), AR('C2', 'D2', C13_AR),
                   G('C3', 'D2', 'numerical', c13_pie, marks=1), G('C3', 'D3', 'numerical', c13_pie_val, marks=3, kinds=('q3',)), G('C3', 'D1', 'numerical', c13_pie, marks=1),
                   G('C4', 'D3', 'numerical', c13_pie, marks=3, kinds=('q3',)), G('C4', 'D4', 'numerical', c13_pie_val, marks=3)],
    S + '04-st3': [M('C1', 'D1', C14_FACT[:3]), M('C1', 'D2', C14_FACT[3:]), G('C2', 'D2', 'mcq', c13_choose), G('C2', 'D3', 'numerical', c14_cf, marks=3, kinds=('q3',)),
                   AR('C2', 'D3', C14_AR), G('C3', 'D2', 'numerical', c14_unequal, marks=1), G('C3', 'D3', 'numerical', c14_cf, marks=3), G('C3', 'D4', 'case', c14_case, marks=4, kinds=('case',)),
                   G('C3', 'D1', 'numerical', c14_unequal, marks=1), G('C4', 'D3', 'case', c14_case, marks=4, kinds=('case',)),
                   W('C4', 'D4', 'long', [('Explain how a histogram, a frequency polygon and ogives are constructed. How can the median and the mode be located graphically?',
                                           'Histogram: adjacent rectangles on continuous classes (adjust unequal widths); polygon: join mid-points of tops; ogives: less than (upper limits) and more than (lower limits); median at intersection of ogives (or at N/2 on one ogive); mode from the tallest rectangle of the histogram by joining diagonals.',
                                           '1 mark each construction (3); 3 marks graphical location (6 marks).')], marks=6)],
    S + '04-st4': [M('C1', 'D1', C15_FACT[:2]), M('C1', 'D2', C15_FACT[2:]), G('C2', 'D2', 'mcq', c13_choose), AR('C2', 'D3', C15_AR), G('C3', 'D2', 'numerical', c15_trend, marks=3),
                   G('C3', 'D3', 'numerical', c15_trend, marks=3, kinds=('q3',)), G('C4', 'D3', 'numerical', c15_trend, marks=4, kinds=('q4',))],
}
