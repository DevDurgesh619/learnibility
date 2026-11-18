"""CBSE class 9 social science fact tables, chapters 6-10 (with computed economics items)."""
from qbank import mcq, name, inr, num, num_distractors

CROPS = [('wheat', 'mustard'), ('paddy', 'soyabean'), ('sugarcane', 'cotton'), ('potatoes', 'peas'), ('maize', 'groundnut')]
GOODS = [('notebooks', 'per dozen'), ('mangoes', 'per kg'), ('LED bulbs', 'per piece'), ('school bags', 'per piece'), ('tomatoes', 'per kg')]


# ---------------- ch08 computed items
def opp_cost_crop(r):
    a, b = r.choice(CROPS)
    who = name(r)
    x = r.randrange(40, 95) * 1000
    y = x - r.randrange(5, 30) * 1000
    z = y - r.randrange(3, 15) * 1000
    return {'stem': (f'{who}, a farmer in Haryana, can use one acre of land to grow {a} (expected income {inr(x)}), {b} (expected income {inr(y)}) '
                     f'or vegetables (expected income {inr(z)}). {who} decides to grow {a}. What is the opportunity cost of this decision?'),
            'answer': f'{inr(y)} (the income from {b}, the next best alternative)',
            'key': f'Opportunity cost = value of the next best alternative given up = income from {b} = {inr(y)}. The third option is not counted.',
            'distractors': [inr(z), inr(x), inr(y + z)]}


def opp_cost_time(r):
    who = name(r)
    w = r.choice([150, 200, 250, 300, 400])
    h = r.choice([2, 3, 4, 5])
    return {'stem': (f'{who} can earn {inr(w)} an hour giving tuition. On Sunday {who} spends {h} hours at a cricket match instead. '
                     f'What is the opportunity cost of watching the match?'),
            'answer': f'{inr(w * h)} of tuition income given up',
            'key': f'Opportunity cost = income forgone = {inr(w)} × {h} = {inr(w * h)}.',
            'distractors': [inr(w), inr(w * (h + 1)), inr(w * h // 2)]}


def ppf_cost(r):
    butter = r.choice([100, 120, 150, 200])
    steps = sorted(r.sample(range(5, 40, 5), 4))
    pts_ = [(0, butter)]
    b = butter
    for k, s in enumerate(steps):
        b -= s
        pts_.append((k + 1, b))
    if b < 0:
        raise ValueError
    i = r.randrange(1, 4)
    loss = pts_[i][1] - pts_[i + 1][1]
    table = '; '.join(f'{p} tractor{"" if p == 1 else "s"} and {q} tonnes of wheat' for p, q in pts_)
    return {'stem': (f'An economy can produce the following combinations: {table}. '
                     f'What is the opportunity cost of raising tractor output from {i} to {i + 1}, and what does the pattern of the table show?'),
            'answer': f'{loss} tonnes of wheat; the opportunity cost rises as more tractors are produced',
            'key': f'Wheat falls from {pts_[i][1]} to {pts_[i + 1][1]} tonnes, so the cost is {loss} tonnes (2 marks). Each extra tractor costs more wheat: increasing opportunity cost (1 mark).',
            'marks': 3, 'minutes': 5}


# ---------------- ch09 computed items
def _market(r):
    p = r.randrange(20, 80)
    b = r.choice([2, 3, 4, 5])
    d = r.choice([1, 2, 3])
    q = r.randrange(100, 400, 10)
    a = q + b * p
    c = q - d * p
    if c <= 0:
        raise ValueError
    return p, q, a, b, c, d


def equilibrium(r):
    p, q, a, b, c, d = _market(r)
    g, u = r.choice(GOODS)
    return {'stem': (f'In a local market for {g}, quantity demanded is Qd = {a} − {b}P and quantity supplied is Qs = {c} + {d}P, where P is the price in rupees {u}. '
                     f'Find the equilibrium price and quantity.'),
            'answer': f'P = ₹{p}, Q = {q}',
            'key': f'At equilibrium Qd = Qs: {a} − {b}P = {c} + {d}P → {b + d}P = {a - c} → P = {p}; Q = {a} − {b} × {p} = {q} (1 mark for equating, 1 for price, 1 for quantity).',
            'marks': 3, 'minutes': 5}


def excess(r):
    p, q, a, b, c, d = _market(r)
    g, u = r.choice(GOODS)
    low = r.random() < 0.5
    pp = p - r.randrange(3, 10) if low else p + r.randrange(3, 10)
    qd, qs = a - b * pp, c + d * pp
    if qd <= 0:
        raise ValueError
    kind = 'excess demand (shortage)' if qd > qs else 'excess supply (surplus)'
    move = 'rise' if qd > qs else 'fall'
    return {'stem': (f'For {g}, Qd = {a} − {b}P and Qs = {c} + {d}P (P in rupees {u}). If the price is fixed at ₹{pp}, is there excess demand or excess supply, of how much, '
                     f'and which way will the price move if the market is left free?'),
            'answer': f'{kind} of {abs(qd - qs)} units; price will {move} towards ₹{p}',
            'key': f'At ₹{pp}: Qd = {qd}, Qs = {qs}; gap = {abs(qd - qs)} ({kind}); price will {move} to the equilibrium ₹{p}.',
            'marks': 3, 'minutes': 5}


def demand_schedule(r):
    g, u = r.choice(GOODS)
    p0 = r.randrange(20, 60)
    step = r.choice([5, 10])
    q0 = r.randrange(80, 200, 10)
    dq = r.choice([10, 15, 20])
    prices = [p0 + i * step for i in range(4)]
    qty = [q0 - i * dq for i in range(4)]
    tab = ', '.join(f'₹{p}: {q}' for p, q in zip(prices, qty))
    return {'stem': f'A demand schedule for {g} ({u}) is: price ₹ / quantity demanded – {tab}. Which law does it show and what is the change in quantity demanded when the price rises from ₹{prices[1]} to ₹{prices[3]}?',
            'answer': f'The law of demand; quantity demanded falls by {2 * dq} units',
            'key': f'Price and quantity demanded move in opposite directions (law of demand, other things remaining constant); {qty[1]} − {qty[3]} = {2 * dq}.',
            'distractors': [f'The law of supply; quantity demanded rises by {2 * dq} units', f'The law of demand; quantity demanded rises by {2 * dq} units',
                            f'The law of demand; quantity demanded falls by {dq} units']}


def inflation_rate(r):
    a = r.randrange(120, 190)
    rate = r.choice([2, 3, 4, 5, 6, 7, 8, 10])
    b = round(a * (1 + rate / 100), 1)
    pct = (b - a) / a * 100
    return {'stem': f'The Consumer Price Index rose from {a} last year to {num(b, 1)} this year. Calculate the rate of inflation.',
            'answer': f'{num(pct, 1)} per cent',
            'key': f'Inflation = ({num(b, 1)} − {a}) ÷ {a} × 100 = {num(pct, 1)} per cent.',
            'distractors': [f'{num(b - a, 1)} per cent', f'{num(pct * 2, 1)} per cent', f'{num(pct / 2, 1)} per cent']}


def real_value(r):
    who = name(r)
    s = r.randrange(20, 60) * 1000
    rate = r.choice([5, 6, 8, 10])
    new = s * (1 + rate / 100)
    return {'stem': (f'{who}\'s monthly salary stays at {inr(s)} while prices rise by {rate} per cent in a year. How much money would {who} need next year to buy the same goods, '
                     f'and what has happened to the real value of the salary?'),
            'answer': f'{inr(new)}; real value (purchasing power) of the salary has fallen',
            'key': f'{inr(s)} × {100 + rate}/100 = {inr(new)} (1 mark); same money buys less, so real income falls (1 mark).',
            'marks': 2, 'minutes': 3}


DATA = {
    # ---------------- ch06 Democracy
    '06-st1': dict(
        T=[('democracy', 'a form of government in which the rulers are elected by the people'),
           ('one person, one vote, one value', 'the principle that every adult has one vote and every vote has equal value'),
           ('rule of law', 'the principle that everyone, including rulers, must obey the law'),
           ('military dictatorship', 'rule by army officers who take power by force, not by election')],
        FB=[('The word democracy comes from the Greek words demos and ___.', 'kratia', ['polis', 'logos', 'nomos']),
            ('"Government of the people, by the people, for the people" was said by ___.', 'Abraham Lincoln', ['George Washington', 'Winston Churchill', 'Mahatma Gandhi']),
            ('In 1999, General ___ took power in Pakistan through a military coup.', 'Pervez Musharraf', ['Zia-ul-Haq', 'Ayub Khan', 'Yahya Khan']),
            ('In China, the government is always formed by the ___.', 'Communist Party', ['Congress Party', 'Labour Party', 'Republican Party']),
            ('From 1930 to 2000, every presidential election in Mexico was won by the ___.', 'PRI', ['PAN', 'ZANU-PF', 'Communist Party'])],
        EX=[('C2', 'D2', 'Why is China not considered a democracy even though it holds elections?', ['voters do not have a real choice; only the Communist Party and its allies can contest', 'the government is always formed by the Communist Party']),
            ('C2', 'D3', 'Why is a "free and fair electoral competition" a key feature of democracy?', ['people must have a real choice among parties', 'those in power should be able to lose']),
            ('C3', 'D3', 'State the four key features of democracy.', ['major decisions are taken by elected representatives', 'elections offer a free and fair choice', 'each adult has one vote of equal value', 'government works within constitutional law and citizens\' rights']),
            ('C4', 'D4', 'A country holds regular elections, but the ruling party controls the media and jails opposition leaders. Is it a democracy? Justify.', ['no – elections are not free and fair', 'opposition cannot compete freely', 'citizens\' rights such as free speech are violated'])],
        AR=[('Pakistan under General Musharraf was not a democracy.', 'Final decision-making powers rested with army officials and the President, not elected representatives.', 'a', 'R explains A.'),
            ('Elections in China offer voters a real choice of parties.', 'The National People\'s Congress is elected in China.', 'd', 'A is false – only the Communist Party and its allies may contest; R is true.')],
        SC=[('In Country P, all adults vote, but only men of a certain religion can contest elections. Which feature of democracy is missing?', 'Free and fair electoral competition / political equality',
             ['Separation of the judiciary', 'Federal division of power', 'A written constitution'], 'Restricting who can contest denies equal political rights and real choice.')],
    ),
    '06-st2': dict(
        T=[('accountable government', 'a government that must answer to the people for its actions'),
           ('legitimate government', 'a government chosen through a fair process and accepted by the people'),
           ('dignity of citizens', 'the respect and equal worth that democracy gives to every individual')],
        FB=[('Amartya Sen pointed out that no large famine has occurred in independent India, unlike the famine in ___ in 1958–61.', 'China', ['Japan', 'Pakistan', 'Sri Lanka']),
            ('A major argument against democracy is that it causes ___ because many people must be consulted.', 'delays in decisions', ['wars', 'famines', 'dictatorship']),
            ('Democracy allows people to correct their own ___.', 'mistakes', ['constitutions', 'currencies', 'borders'])],
        EX=[('C2', 'D2', 'Why does democracy improve the quality of decision-making?', ['decisions are based on discussion and consultation', 'many people and ideas are involved, so mistakes are reduced']),
            ('C2', 'D3', 'Why does democracy allow us to correct our own mistakes?', ['public discussion brings mistakes into the open', 'people can change the government in the next election']),
            ('C3', 'D3', 'Give three arguments against democracy and one reply to each.', ['leaders keep changing – but change keeps governments responsive', 'it leads to corruption – but non-democracies are not free of corruption', 'it causes delays – but discussion leads to better decisions']),
            ('C4', 'D3', '"Democracy is better than any other form of government." Evaluate this claim.', ['it is accountable and responsive', 'it enhances dignity and equality', 'it manages differences peacefully', 'it is not perfect, but it allows correction of mistakes'])],
        AR=[('Democracy enhances the dignity of citizens.', 'It is based on political equality – the poorest and the richest have the same vote.', 'a', 'R explains A.')],
        CAT=[('an argument in favour of democracy', 'arguments in favour of democracy', ['it is more accountable', 'it improves decision-making', 'it enhances dignity of citizens', 'it allows correction of mistakes'],
              ['it causes instability', 'it leads to delays', 'leaders do not know the best interest of people', 'it encourages money power'])],
    ),
    '06-st3': dict(
        T=[('Preamble', 'the introduction to the Constitution that states its basic values and goals'),
           ('sovereign', 'a state that is free to take decisions on internal and external matters without outside control'),
           ('secular', 'a state that has no official religion and treats all religions equally'),
           ('republic', 'a state whose head is elected, not hereditary'),
           ('Constituent Assembly', 'the elected body that wrote the Constitution of India')],
        FB=[('The Constituent Assembly held its first meeting on 9 December ___.', '1946', ['1947', '1945', '1949']),
            ('The words "socialist" and "secular" were added to the Preamble by the ___ Amendment in 1976.', '42nd', ['44th', '1st', '86th']),
            ('The Preamble begins with the words "We, the ___ of India".', 'people', ['citizens', 'states', 'representatives']),
            ('The Constitution of India came into effect on 26 January ___.', '1950', ['1949', '1947', '1952']),
            ('The Constituent Assembly had ___ members after Partition.', '299', ['389', '545', '250'])],
        EX=[('C2', 'D2', 'Why is the Preamble called the soul of the Constitution?', ['it states the values on which the Constitution is based', 'it is used to understand the meaning of other provisions']),
            ('C3', 'D3', 'Explain how the Indian Constitution makes India a democracy.', ['universal adult franchise and regular elections', 'Fundamental Rights protected by courts', 'an independent Election Commission and judiciary', 'government works within the rule of law']),
            ('C4', 'D3', 'Explain the meaning of any three words in the Preamble and why they matter.', ['sovereign: India decides its own affairs', 'secular: no official religion, equal respect for all', 'republic: head of state is elected', 'justice, liberty, equality and fraternity: values for all citizens'])],
        AR=[('India is a republic.', 'The head of the state in India is elected and is not hereditary.', 'a', 'R explains A.'),
            ('The word "secular" was in the Preamble from 1950.', 'The Preamble begins with "We, the people of India".', 'd', 'A is false – it was added in 1976; R is true.')],
        CAT=[('a word in the Preamble of India', 'words in the Preamble of India', ['sovereign', 'socialist', 'secular', 'democratic', 'republic'], ['monarchy', 'federal union of kings', 'theocratic', 'imperial'])],
    ),
    '06-st4': dict(
        T=[('universal adult franchise', 'the right of all adults to vote'),
           ('military coup', 'the sudden seizure of power by the army'),
           ('veto', 'the power of a permanent member of the UN Security Council to stop a decision')],
        FB=[('The democratically elected President of Chile, ___, was overthrown in a military coup in 1973.', 'Salvador Allende', ['Augusto Pinochet', 'Michelle Bachelet', 'Fidel Castro']),
            ('The workers\' movement in Poland led by Lech Walesa was called ___.', 'Solidarity', ['Perestroika', 'Glasnost', 'Velvet']),
            ('Ghana became independent in 1957 under ___.', 'Kwame Nkrumah', ['Nelson Mandela', 'Jomo Kenyatta', 'Robert Mugabe']),
            ('The UN Security Council has ___ permanent members with veto power.', 'five', ['three', 'seven', 'ten']),
            ('Nepal became a democratic republic, abolishing its monarchy, in ___.', '2008', ['1990', '2001', '2015'])],
        EX=[('C2', 'D2', 'Why is the UN Security Council said to be undemocratic?', ['only five permanent members have veto power', 'one permanent member can block a decision supported by most countries']),
            ('C3', 'D3', 'Describe three challenges that democracies face today.', ['foundational challenge: making the transition to democracy', 'challenge of expansion: applying democracy to all regions and groups', 'challenge of deepening: strengthening institutions and reducing money power']),
            ('C4', 'D4', 'Trace how democracy expanded across the world in the twentieth century.', ['many colonies in Asia and Africa became independent democracies', 'military regimes in Latin America gave way to elected governments', 'communist rule ended in Eastern Europe after 1989', 'women and the poor won the right to vote'])],
        AR=[('Chile returned to democracy in 1990.', 'Pinochet lost a referendum in 1988 on continuing his rule.', 'a', 'R explains A.')],
        CHRON=[('Ghana becomes independent', 1957), ('military coup in Chile', 1973), ('Solidarity strike at Gdansk, Poland', 1980), ('end of military rule in Chile', 1990), ('Nepal abolishes monarchy', 2008)],
    ),
    # ---------------- ch07 Elections
    '07-st1': dict(
        T=[('election', 'the process by which people choose their representatives at regular intervals'),
           ('representative', 'a person chosen by voters to act and decide on their behalf'),
           ('electoral competition', 'the contest among parties and candidates for votes')],
        FB=[('In India, elections to the Lok Sabha are held every ___ years.', 'five', ['four', 'six', 'three']),
            ('An election held to fill a seat that falls vacant is called a ___.', 'by-election', ['mid-term poll', 'general election', 'referendum']),
            ('An election held for all constituencies at the same time is a ___ election.', 'general', ['by-', 'local', 'party'])],
        EX=[('C2', 'D2', 'Why are elections necessary in a large democracy?', ['all people cannot take decisions directly', 'elections let people choose and change representatives']),
            ('C2', 'D3', 'What makes an election democratic?', ['everyone has one vote of equal value and real choice among parties', 'elections are held regularly and are free and fair']),
            ('C3', 'D3', 'List three choices voters make through elections.', ['who will make laws for them', 'who will form the government and take major decisions', 'which party\'s policies will guide the government']),
            ('C4', 'D3', 'Electoral competition has demerits too. Analyse its merits and demerits.', ['merit: leaders must serve people to win again', 'merit: people can punish bad governments', 'demerit: it creates a sense of disunity and factionalism', 'demerit: parties may use dirty tricks to win'])],
        AR=[('Regular elections keep governments accountable.', 'A government that does not serve the people may lose the next election.', 'a', 'R explains A.')],
    ),
    '07-st2': dict(
        T=[('constituency', 'an area whose voters elect one representative'),
           ('reserved constituency', 'a constituency in which only candidates from the Scheduled Castes or Scheduled Tribes can contest'),
           ('voters\' list', 'the official list of people eligible to vote, also called the electoral roll'),
           ('delimitation', 'the drawing of the boundaries of constituencies'),
           ('affidavit', 'a signed legal declaration that candidates file about their assets, criminal cases and education')],
        FB=[('In the Lok Sabha, ___ seats are reserved for Scheduled Castes.', '84', ['47', '100', '62']),
            ('In the Lok Sabha, ___ seats are reserved for Scheduled Tribes.', '47', ['84', '30', '65']),
            ('A citizen must be ___ years old to contest a Lok Sabha election.', '25', ['18', '21', '30']),
            ('The voters\' list is also called the ___.', 'electoral roll', ['census register', 'gazette', 'ballot paper']),
            ('Boundaries of constituencies are drawn by the ___ Commission.', 'Delimitation', ['Finance', 'Planning', 'Law'])],
        EX=[('C2', 'D2', 'Why are some constituencies reserved for SCs and STs?', ['to ensure these weaker sections are represented', 'without reservation they might not win because of social and economic disadvantages']),
            ('C2', 'D3', 'Why do candidates have to file an affidavit about their background?', ['voters can know about their assets, education and criminal cases', 'it helps voters make an informed choice']),
            ('C3', 'D3', 'Explain how the voters\' list is prepared and kept up to date.', ['house-to-house survey and applications by eligible citizens', 'names of those who turn 18 are added', 'names of those who have died or moved are deleted']),
            ('C4', 'D4', 'Why are constituencies drawn so that each has roughly the same population?', ['every vote should have equal value', 'one person, one vote, one value requires similar population per seat', 'unequal constituencies would over-represent some people'])],
        AR=[('Constituencies are periodically redrawn.', 'Population changes over time and seats should have similar population.', 'a', 'R explains A.')],
    ),
    '07-st3': dict(
        T=[('Election Commission', 'the independent constitutional body that conducts elections in India'),
           ('Model Code of Conduct', 'rules that parties and candidates must follow during elections'),
           ('rigging', 'fraud and malpractice to increase one\'s votes'),
           ('booth capturing', 'forcible take-over of a polling booth to cast false votes')],
        FB=[('The Chief Election Commissioner is appointed by the ___.', 'President', ['Prime Minister', 'Chief Justice', 'Speaker']),
            ('The Chief Election Commissioner known for strict enforcement of election rules in the 1990s was ___.', 'T. N. Seshan', ['Sukumar Sen', 'S. Y. Quraishi', 'N. Gopalaswami']),
            ('During elections, government officers on election duty work under the control of the ___.', 'Election Commission', ['ruling party', 'Prime Minister\'s Office', 'District Collector alone']),
            ('The Election Commission can order a ___ if polling in a booth was unfair.', 're-poll', ['by-election everywhere', 'referendum', 'census'])],
        EX=[('C2', 'D2', 'Why is the Election Commission said to be very powerful in India?', ['it can take decisions on every aspect of conduct of elections', 'it can order re-polls and act against officers and parties']),
            ('C3', 'D3', 'Give three examples of the powers of the Election Commission.', ['implements the Model Code of Conduct', 'can order re-polls', 'controls officials on election duty', 'recognises parties and allots symbols']),
            ('C4', 'D3', 'List four signs that show Indian elections are largely free and fair.', ['ruling parties often lose elections', 'high voter turnout, especially of the poor', 'candidates accept the results', 'an independent Election Commission conducts elections'])],
        AR=[('Ruling parties often lose elections in India.', 'Indian elections are generally free and fair.', 'a', 'R explains A.')],
    ),
    '07-st4': dict(
        T=[('the cVIGIL app', 'the Election Commission app through which citizens can report violations of the Model Code of Conduct'),
           ('anti-defection law', 'the law under which an elected member who leaves the party can lose the seat'),
           ('electoral reforms', 'changes in rules and practices to make elections cleaner and fairer')],
        FB=[('The anti-defection law was added by the ___ Amendment in 1985.', '52nd', ['42nd', '61st', '73rd']),
            ('The Supreme Court struck down the electoral bond scheme in ___.', '2024', ['2018', '2019', '2014']),
            ('The paper trail attached to EVMs is called ___.', 'VVPAT', ['EPIC', 'NOTA', 'cVIGIL']),
            ('Since 2003, candidates have had to disclose their criminal cases and ___ in an affidavit.', 'assets', ['caste', 'religion', 'party membership'])],
        EX=[('C2', 'D2', 'Why is the role of money in elections a challenge?', ['rich candidates and parties get an unfair advantage', 'voters may be bribed']),
            ('C3', 'D3', 'Suggest three reforms to make elections fairer.', ['state funding or limits on election spending', 'barring candidates with serious criminal cases', 'greater transparency in party funding', 'awareness campaigns for voters']),
            ('C4', 'D4', 'Evaluate whether laws alone can ensure free and fair elections.', ['laws set rules, but enforcement matters', 'parties must follow the rules willingly', 'alert citizens and media must report misuse', 'voters must reject corrupt candidates'])],
        AR=[('Candidates must file affidavits about criminal cases.', 'Voters have a right to know the background of candidates.', 'a', 'R explains A.')],
    ),
    # ---------------- ch08 The Problem of Choice
    '08-st1': dict(
        T=[('scarcity', 'the situation in which resources are limited compared with human wants'),
           ('wants', 'desires for goods and services, which are unlimited'),
           ('economic problem', 'the problem of choosing how to use scarce resources to satisfy unlimited wants'),
           ('free goods', 'goods such as air that are available in plenty and have no price')],
        FB=[('Economics is said to be the study of choice under ___.', 'scarcity', ['abundance', 'surplus', 'luxury']),
            ('Human wants are ___.', 'unlimited', ['limited', 'fixed', 'always satisfied']),
            ('Resources that have alternative uses and are limited are called ___ resources.', 'scarce', ['free', 'unlimited', 'useless']),
            ('Air under normal conditions is an example of a ___ good.', 'free', ['scarce', 'capital', 'luxury'])],
        EX=[('C2', 'D2', 'Why does scarcity lead to the need to choose?', ['resources are limited but wants are unlimited', 'using a resource for one purpose means it cannot be used for another']),
            ('C2', 'D3', 'Why is scarcity a problem even for rich countries?', ['wants keep growing with income', 'resources such as land, time and clean water remain limited']),
            ('C3', 'D3', 'Give three examples of scarcity from your daily life.', ['limited pocket money for many things', 'limited time for study, play and sleep', 'limited water during summer']),
            ('C4', 'D3', 'Explain how scarcity affects a family\'s monthly budget decisions.', ['income is limited', 'the family must rank needs before wants', 'spending more on one item means less for others'])],
        AR=[('Every economy has to make choices.', 'Resources are limited while wants are unlimited.', 'a', 'Scarcity explains choice.')],
    ),
    '08-st2': dict(
        T=[('opportunity cost', 'the value of the next best alternative given up when a choice is made'),
           ('trade-off', 'giving up some of one thing to get more of another'),
           ('production possibility frontier', 'a curve showing the combinations of two goods an economy can produce with given resources')],
        FB=[('Opportunity cost is the value of the ___ alternative forgone.', 'next best', ['worst', 'cheapest', 'first']),
            ('A curve showing the maximum combinations of two goods that can be produced is called the ___.', 'production possibility frontier', ['demand curve', 'supply curve', 'budget line']),
            ('A point inside the production possibility frontier shows ___ of resources.', 'under-utilisation', ['full use', 'growth', 'impossible use'])],
        EX=[('C2', 'D2', 'Why does every choice have an opportunity cost?', ['resources and time are limited', 'choosing one option means giving up the next best one']),
            ('C4', 'D3', 'A government spends ₹500 crore on a new stadium instead of a hospital. Explain the opportunity cost and how it should decide.', ['opportunity cost: the hospital and its health benefits', 'it should compare benefits to society of both', 'priority to basic needs like health may be wiser'])],
        AR=[('A student who spends an evening watching a film gives up study time.', 'Every choice involves an opportunity cost.', 'a', 'R explains A.')],
        GEN=[('C3', 'D2', 'short', opp_cost_crop), ('C3', 'D3', 'short', opp_cost_time), ('C4', 'D4', 'multi_step', ppf_cost, {'kinds': ('sa3',)})],
    ),
    '08-st3': dict(
        T=[('what to produce', 'the central problem of deciding which goods and services, and how much of each, to produce'),
           ('how to produce', 'the central problem of choosing the technique of production, labour-intensive or capital-intensive'),
           ('for whom to produce', 'the central problem of deciding how output is distributed among people'),
           ('labour-intensive technique', 'a method of production that uses more workers and fewer machines')],
        FB=[('Deciding between using tractors or many farm workers deals with the problem of ___ to produce.', 'how', ['what', 'for whom', 'where']),
            ('Deciding whether to produce more food grains or more cars deals with the problem of ___ to produce.', 'what', ['how', 'for whom', 'why']),
            ('A country with many unemployed workers may prefer a ___ technique of production.', 'labour-intensive', ['capital-intensive', 'robot-based', 'import-based'])],
        EX=[('C2', 'D2', 'Why must every economy decide "for whom to produce"?', ['output is limited and cannot satisfy everyone fully', 'it decides how income and goods are shared among people']),
            ('C3', 'D3', 'Identify the central problem in each: (i) choosing between building schools or roads, (ii) using machines or workers in a factory, (iii) deciding subsidies for poor families.', ['(i) what to produce', '(ii) how to produce', '(iii) for whom to produce']),
            ('C4', 'D4', 'Why might India choose labour-intensive techniques in some industries while choosing capital-intensive ones in others?', ['labour is plentiful, so labour-intensive methods create jobs', 'some industries like steel need heavy machines', 'capital-intensive methods raise efficiency and quality'])],
        AR=[('India encourages labour-intensive industries such as textiles.', 'India has a large labour force that needs jobs.', 'a', 'R explains A.')],
    ),
    '08-st4': dict(
        T=[('market economy', 'an economy in which private individuals own resources and prices decide what, how and for whom to produce'),
           ('centrally planned economy', 'an economy in which the government owns resources and decides what, how and for whom to produce'),
           ('mixed economy', 'an economy in which both the government and private sector play important roles, as in India'),
           ('invisible hand', 'Adam Smith\'s idea that self-interest guided by prices leads markets to serve society')],
        FB=[('India is an example of a ___ economy.', 'mixed', ['pure market', 'centrally planned', 'barter']),
            ('The former Soviet Union was an example of a ___ economy.', 'centrally planned', ['market', 'mixed', 'traditional']),
            ('The Planning Commission of India was replaced by ___ in 2015.', 'NITI Aayog', ['Finance Commission', 'Reserve Bank', 'Election Commission']),
            ('India began major economic reforms of liberalisation in ___.', '1991', ['1951', '1975', '2001']),
            ('The idea of the "invisible hand" of the market was given by ___.', 'Adam Smith', ['Karl Marx', 'J. M. Keynes', 'Amartya Sen'])],
        EX=[('C2', 'D2', 'Why does India follow a mixed economy?', ['the private sector brings efficiency and growth', 'the government ensures welfare, basic services and fairness']),
            ('C3', 'D3', 'Compare a market economy and a centrally planned economy on three points.', ['ownership: private vs government', 'decisions: by prices and markets vs by the planning authority', 'aim: profit vs social welfare as decided by the state']),
            ('C4', 'D3', 'Evaluate one strength and one weakness each of market and centrally planned economies.', ['market: efficient and innovative', 'market: may ignore the poor and widen inequality', 'planned: can focus on basic needs', 'planned: often inefficient and slow to respond'])],
        AR=[('In a market economy, prices guide production decisions.', 'Producers produce goods that people are willing to pay for.', 'a', 'R explains A.')],
        CHRON=[('Planning Commission set up', 1950), ('economic reforms of liberalisation', 1991), ('NITI Aayog replaces the Planning Commission', 2015), ('Adam Smith\'s Wealth of Nations', 1776)],
    ),
    # ---------------- ch09 The Price Puzzle
    '09-st1': dict(
        T=[('demand', 'the quantity of a good that buyers are willing and able to buy at a given price in a given time'),
           ('law of demand', 'the rule that, other things remaining the same, quantity demanded falls when price rises'),
           ('substitute goods', 'goods that can be used in place of each other, such as tea and coffee'),
           ('complementary goods', 'goods used together, such as cars and petrol'),
           ('demand curve', 'a graph of price and quantity demanded that slopes downward from left to right')],
        FB=[('Other things remaining the same, when the price of a good rises, its quantity demanded ___.', 'falls', ['rises', 'stays the same', 'doubles']),
            ('The demand curve usually slopes ___ from left to right.', 'downward', ['upward', 'horizontally', 'vertically']),
            ('Tea and coffee are ___ goods.', 'substitute', ['complementary', 'free', 'capital']),
            ('Cars and petrol are ___ goods.', 'complementary', ['substitute', 'free', 'inferior']),
            ('If the price of coffee rises, the demand for tea is likely to ___.', 'rise', ['fall', 'stay unchanged', 'become zero'])],
        EX=[('C2', 'D2', 'Why do people buy more of a good when its price falls?', ['the good becomes cheaper than its substitutes', 'buyers can afford more with the same income']),
            ('C3', 'D3', 'State three factors other than price that affect the demand for a good.', ['income of buyers', 'prices of related goods (substitutes and complements)', 'tastes and preferences', 'expectations of future prices']),
            ('C4', 'D3', 'Explain why the demand for umbrellas rises in July even if their price does not change.', ['the monsoon changes needs and preferences', 'demand depends on factors other than price', 'the whole demand curve shifts to the right'])],
        AR=[('The demand for petrol cars may fall if petrol prices rise sharply.', 'Cars and petrol are complementary goods.', 'a', 'R explains A.')],
        GEN=[('C3', 'D2', 'mcq', demand_schedule)],
    ),
    '09-st2': dict(
        T=[('supply', 'the quantity of a good that sellers are willing to offer for sale at a given price in a given time'),
           ('law of supply', 'the rule that, other things remaining the same, quantity supplied rises when price rises'),
           ('supply curve', 'a graph of price and quantity supplied that slopes upward from left to right')],
        FB=[('Other things remaining the same, a rise in price leads to a ___ in quantity supplied.', 'rise', ['fall', 'no change', 'collapse']),
            ('The supply curve usually slopes ___ from left to right.', 'upward', ['downward', 'horizontally', 'vertically']),
            ('A rise in the cost of raw materials usually ___ supply at each price.', 'reduces', ['increases', 'does not affect', 'doubles']),
            ('Better technology usually ___ supply at each price.', 'increases', ['reduces', 'stops', 'freezes'])],
        EX=[('C2', 'D2', 'Why do sellers supply more when the price rises?', ['higher prices mean higher profit', 'more producers find it worthwhile to produce']),
            ('C3', 'D3', 'Give three factors other than price that affect supply.', ['cost of inputs such as raw materials and wages', 'technology', 'weather (for farm goods)', 'taxes and subsidies']),
            ('C4', 'D4', 'A drought hits onion-growing areas of Maharashtra. Explain its effect on the supply and price of onions across India.', ['onion output falls, so supply falls', 'at the old price, demand exceeds supply', 'the price of onions rises in markets across India'])],
        AR=[('The supply of vegetables falls during floods.', 'Floods damage crops and disrupt transport.', 'a', 'R explains A.')],
    ),
    '09-st3': dict(
        T=[('equilibrium price', 'the price at which quantity demanded equals quantity supplied'),
           ('excess demand', 'the situation in which quantity demanded is more than quantity supplied at a given price'),
           ('excess supply', 'the situation in which quantity supplied is more than quantity demanded at a given price'),
           ('minimum support price', 'the price announced by the government at which it buys certain crops from farmers')],
        FB=[('At the equilibrium price, quantity demanded is ___ quantity supplied.', 'equal to', ['greater than', 'less than', 'double']),
            ('When there is excess demand, the price tends to ___.', 'rise', ['fall', 'stay fixed', 'become zero']),
            ('When there is excess supply, the price tends to ___.', 'fall', ['rise', 'stay fixed', 'double']),
            ('The government announces a minimum support price for crops such as wheat and ___.', 'paddy', ['tea', 'coffee', 'rubber'])],
        EX=[('C2', 'D2', 'Why does the market price move towards equilibrium?', ['excess demand pushes prices up', 'excess supply pushes prices down']),
            ('C4', 'D3', 'Why does the government fix a minimum support price for wheat and paddy?', ['to protect farmers from a fall in prices at harvest', 'to give them an assured income and encourage production', 'to build food stocks for the public distribution system'])],
        AR=[('Prices of fruits often fall at the peak of the season.', 'There is excess supply when large quantities arrive in the market.', 'a', 'R explains A.')],
        GEN=[('C3', 'D3', 'numerical', equilibrium, {'kinds': ('sa3',)}), ('C4', 'D4', 'numerical', excess, {'kinds': ('sa3',)})],
    ),
    '09-st4': dict(
        T=[('inflation', 'a sustained rise in the general level of prices'),
           ('Consumer Price Index', 'an index that measures changes in the prices of a basket of goods and services bought by households'),
           ('purchasing power', 'the amount of goods and services that money can buy'),
           ('repo rate', 'the rate at which the Reserve Bank of India lends money to commercial banks')],
        FB=[('Inflation in India is mainly measured using the ___.', 'Consumer Price Index', ['Sensex', 'Human Development Index', 'GDP deflator alone']),
            ('The Reserve Bank of India has an inflation target of ___ per cent, with a band of 2 per cent on either side.', '4', ['2', '6', '10']),
            ('During inflation, people with fixed incomes are generally ___.', 'worse off', ['better off', 'unaffected', 'richer']),
            ('To control inflation, the RBI may ___ the repo rate.', 'raise', ['lower', 'abolish', 'freeze'])],
        EX=[('C2', 'D2', 'Why does inflation hurt people with fixed incomes?', ['their income stays the same while prices rise', 'they can buy fewer goods with the same money']),
            ('C3', 'D3', 'Explain three effects of rising prices on a household.', ['less money left for savings', 'cuts in spending on non-essential items', 'value of savings kept as cash falls']),
            ('C4', 'D4', 'Who gains and who loses from inflation? Analyse.', ['borrowers gain because they repay with money of lower value', 'lenders and savers lose', 'fixed-income earners lose', 'producers may gain if prices rise faster than costs'])],
        AR=[('Inflation reduces the purchasing power of money.', 'With the same money, fewer goods can be bought when prices rise.', 'a', 'R explains A.')],
        GEN=[('C3', 'D2', 'short', inflation_rate), ('C3', 'D3', 'explain', real_value, {'kinds': ('sa2',)})],
    ),
    # ---------------- ch10 Oceans and Life
    '10-st1': dict(
        T=[('continental shelf', 'the gently sloping, shallow submerged edge of a continent'),
           ('continental slope', 'the steep slope connecting the continental shelf with the deep ocean floor'),
           ('abyssal plain', 'the flat deep-sea plain of the ocean floor'),
           ('oceanic trench', 'a long, narrow and very deep depression in the ocean floor'),
           ('mid-oceanic ridge', 'an underwater chain of mountains where plates move apart')],
        FB=[('The shallowest part of the ocean floor is the ___.', 'continental shelf', ['continental slope', 'abyssal plain', 'oceanic trench']),
            ('The deepest known point in the oceans, the Challenger Deep, is in the ___.', 'Mariana Trench', ['Java Trench', 'Puerto Rico Trench', 'Mid-Atlantic Ridge']),
            ('Mumbai High, an oil field, lies on the ___.', 'continental shelf', ['abyssal plain', 'oceanic trench', 'mid-oceanic ridge']),
            ('A flat-topped submarine mountain is called a ___.', 'guyot', ['seamount', 'trench', 'atoll'])],
        EX=[('C2', 'D2', 'Why is the continental shelf important for people?', ['it is rich in fish', 'it contains deposits of oil and natural gas']),
            ('C3', 'D3', 'Name and describe the four main relief features of the ocean floor.', ['continental shelf – shallow edge of continents', 'continental slope – steep descent', 'deep-sea (abyssal) plain – flat deep floor', 'trenches – very deep narrow depressions']),
            ('C4', 'D4', 'Explain how plate tectonics forms ridges and trenches on the ocean floor.', ['where plates move apart, magma rises and forms ridges', 'where one plate sinks under another, deep trenches form', 'trenches are often near volcanoes and earthquake zones'])],
        AR=[('Most fishing grounds lie on continental shelves.', 'Shallow shelves get sunlight and nutrients that support plankton.', 'a', 'R explains A.')],
        MAP=[('the Mariana Trench', 'Mariana Trench', 'western Pacific Ocean', 'world'), ('the Mid-Atlantic Ridge', 'Mid-Atlantic Ridge', 'middle of the Atlantic Ocean', 'world'),
             ('the Grand Banks fishing ground', 'Grand Banks', 'off Newfoundland, Canada', 'world'), ('the Bay of Fundy', 'Bay of Fundy', 'between Canada\'s Nova Scotia and New Brunswick', 'world')],
    ),
    '10-st2': dict(
        T=[('salinity', 'the amount of salt in grams dissolved in 1,000 grams of sea water'),
           ('thermocline', 'the layer of ocean water in which temperature falls rapidly with depth'),
           ('isohaline', 'a line joining places of equal salinity')],
        FB=[('The average salinity of the oceans is about ___ parts per thousand.', '35', ['3.5', '100', '350']),
            ('The temperature of ocean water generally ___ with depth.', 'decreases', ['increases', 'stays the same', 'doubles']),
            ('Salinity is high where evaporation is high and rainfall is ___.', 'low', ['high', 'heavy', 'frequent']),
            ('The Baltic Sea has low salinity because of many rivers and ___.', 'low evaporation', ['high evaporation', 'volcanic activity', 'coral reefs']),
            ('The Dead Sea has very ___ salinity.', 'high', ['low', 'zero', 'average'])],
        EX=[('C2', 'D2', 'Why is the salinity of the Red Sea high?', ['high temperature causes heavy evaporation', 'little rainfall and few rivers bring fresh water']),
            ('C3', 'D3', 'Explain three factors that affect the salinity of sea water.', ['evaporation increases salinity', 'rainfall and river water reduce salinity', 'melting ice reduces salinity; freezing increases it', 'ocean currents mix water']),
            ('C4', 'D3', 'Why do surface waters near the equator have higher temperatures than those near the poles?', ['vertical rays of the Sun bring more insolation near the equator', 'polar waters get slanting rays and ice cover', 'warm and cold currents also modify temperature'])],
        AR=[('The Dead Sea has very high salinity.', 'It is an inland sea in a hot, dry region with high evaporation.', 'a', 'R explains A.')],
    ),
    '10-st3': dict(
        T=[('tides', 'the regular rise and fall of sea level caused mainly by the pull of the Moon and the Sun'),
           ('spring tide', 'a very high tide that occurs at full moon and new moon'),
           ('neap tide', 'a weaker tide that occurs when the Sun and Moon pull at right angles'),
           ('ocean current', 'a stream of water flowing in a definite direction in the ocean'),
           ('waves', 'up-and-down movements of the ocean surface caused mainly by wind')],
        FB=[('Tides are caused mainly by the gravitational pull of the ___.', 'Moon', ['Mars', 'Venus', 'Jupiter']),
            ('Spring tides occur on full moon and ___ days.', 'new moon', ['quarter moon', 'eclipse-free', 'equinox']),
            ('The Gulf Stream is a ___ current.', 'warm', ['cold', 'freshwater', 'polar']),
            ('The Labrador Current is a ___ current.', 'cold', ['warm', 'equatorial', 'monsoon']),
            ('The Humboldt (Peru) Current flows along the coast of ___.', 'South America', ['Africa', 'Australia', 'India']),
            ('The highest tides in the world occur in the Bay of ___.', 'Fundy', ['Bengal', 'Biscay', 'Khambhat'])],
        EX=[('C2', 'D2', 'Why are tides useful for navigation and ports?', ['high tides raise water level so ships can enter harbours', 'they help clear silt from river mouths']),
            ('C2', 'D3', 'Why do fishing grounds develop where warm and cold currents meet?', ['mixing of waters brings nutrients that support plankton', 'plankton attracts large numbers of fish']),
            ('C3', 'D3', 'Distinguish between waves, tides and currents.', ['waves: surface movements caused by wind', 'tides: daily rise and fall caused by the Moon and Sun', 'currents: steady flows of water in a definite direction']),
            ('C4', 'D4', 'Explain how ocean currents affect the climate of coastal areas, with examples.', ['warm currents raise temperatures, e.g. North Atlantic Drift keeps western Europe ports ice-free', 'cold currents lower temperature and cause dryness, e.g. Atacama desert near the Humboldt current', 'meeting of currents causes fog, e.g. near Newfoundland'])],
        AR=[('Ports of north-western Europe remain ice-free in winter.', 'The warm North Atlantic Drift flows along their coasts.', 'a', 'R explains A.'),
            ('Spring tides occur at the quarter moon.', 'Tides are caused mainly by the Moon\'s pull.', 'd', 'A is false – spring tides occur at full and new moon; R is true.')],
        CAT=[('a warm ocean current', 'warm ocean currents', ['Gulf Stream', 'Kuroshio', 'North Atlantic Drift', 'Brazil Current'], ['Labrador Current', 'Humboldt Current', 'Canary Current', 'Benguela Current'])],
    ),
    '10-st4': dict(
        T=[('Exclusive Economic Zone', 'the sea area up to 200 nautical miles from the coast where a country has rights over resources'),
           ('blue economy', 'sustainable use of ocean resources for growth, jobs and healthy ecosystems'),
           ('coral bleaching', 'the whitening of corals when warm water forces out the algae living in them'),
           ('polymetallic nodules', 'lumps on the deep sea floor containing manganese, nickel, copper and cobalt')],
        FB=[('A country\'s Exclusive Economic Zone extends up to ___ nautical miles from its coast.', '200', ['12', '50', '500']),
            ('Territorial waters extend up to ___ nautical miles from the coast.', '12', ['200', '24', '100']),
            ('A huge area of floating plastic waste in the North Pacific is called the Great Pacific ___.', 'Garbage Patch', ['Coral Reef', 'Trench', 'Ridge']),
            ('The world\'s largest coral reef system, the Great Barrier Reef, is off the coast of ___.', 'Australia', ['India', 'Brazil', 'Japan'])],
        EX=[('C2', 'D2', 'Why are oceans important for human life?', ['they give fish, salt, oil and minerals', 'they regulate climate and provide sea routes for trade']),
            ('C3', 'D3', 'Suggest three ways to reduce ocean pollution.', ['stop dumping plastics and untreated sewage', 'prevent oil spills from ships', 'promote recycling and beach clean-ups']),
            ('C4', 'D3', 'Analyse the threats to fisheries and marine life.', ['overfishing reduces fish stocks', 'plastic and oil pollution kill marine animals', 'warming seas cause coral bleaching', 'destruction of mangroves removes breeding grounds'])],
        AR=[('Coral bleaching is increasing.', 'Sea temperatures are rising because of global warming.', 'a', 'R explains A.')],
    ),
}
