"""Design g9-ib: IB MYP Year 4 (Mathematics, Sciences, Language and Literature, Individuals and Societies)."""
from dsl import S, G
from content.shared_g9 import MATHS_PRE_G9, SCIENCE_PRE_G9, ENGLISH_PRE_G9

MATHS_CUR = [
    S('ib-g9-maths:1:2', 'Simplifying surds', [
        ('Simplify √12.', '2√3', ['3√2', '4√3', '6'], '√12 = √4 x √3'),
        ('Simplify √18 + √8.', '5√2', ['√26', '2√13', '10√2'], '3√2 + 2√2'),
        ('Rationalise the denominator of 6/√3.', '2√3', ['6√3', '√3/6', '3√2'], '6√3 / 3 = 2√3'),
    ]),
    S('ib-g9-maths:2:2', 'Fractional exponents and roots', [
        ('Evaluate 8^(1/3).', '2', ['4', '8/3', '24'], 'The cube root of 8'),
        ('Simplify (x⁶)^(1/2).', 'x³', ['x⁴', 'x^6.5', 'x¹²'], 'Multiply the exponents'),
        ('Solve 2^(x + 1) = 32.', '4', ['5', '16', '3'], '32 = 2⁵, so x + 1 = 5'),
    ]),
    S('ib-g9-maths:3:3', 'Factorising quadratic trinomials', [
        ('Factorise x² + 5x + 6.', '(x + 2)(x + 3)', ['(x + 1)(x + 6)', '(x + 5)(x + 1)', '(x - 2)(x - 3)'], '2 x 3 = 6 and 2 + 3 = 5'),
        ('Factorise x² - x - 12.', '(x - 4)(x + 3)', ['(x + 4)(x - 3)', '(x - 6)(x + 2)', '(x - 12)(x + 1)'], '-4 x 3 = -12, -4 + 3 = -1'),
        ('Factorise 2x² + 7x + 3.', '(2x + 1)(x + 3)', ['(2x + 3)(x + 1)', '(2x + 7)(x + 3)', '(2x - 1)(x - 3)'],
         '2x² + 6x + x + 3'),
    ]),
    S('ib-g9-maths:4:4', 'Simultaneous linear equations', [
        ('Solve x + y = 10 and x - y = 2.', 'x = 6, y = 4', ['x = 4, y = 6', 'x = 8, y = 2', 'x = 5, y = 5'], 'Add: 2x = 12'),
        ('Solve 2x + y = 7 and x + y = 4.', 'x = 3, y = 1', ['x = 1, y = 3', 'x = 2, y = 3', 'x = 4, y = 0'], 'Subtract: x = 3'),
        ('Two cinema tickets and three snacks cost 31; one ticket and two snacks cost 17. How much is one ticket?', '11',
         ['3', '8', '14'], '2t + 3s = 31 and t + 2s = 17 give s = 3, t = 11'),
    ]),
]

SCIENCE_CUR = [
    S('ib-g9-science:1:2', 'Mitosis and the cell cycle', [
        ('Mitosis produces', 'two genetically identical cells', ['four different cells', 'gametes', 'one larger cell'],
         'Mitosis is for growth and repair'),
        ('Explain why mitosis is important when you cut your skin.', 'It produces new identical cells to repair the tissue',
         ['It makes gametes', 'It stops bleeding by clotting', 'It kills bacteria'], 'New cells replace damaged ones'),
        ('A human body cell has 46 chromosomes. How many are in each cell produced by mitosis, and by meiosis?',
         '46 after mitosis, 23 after meiosis', ['23 after mitosis, 46 after meiosis', '46 after both', '92 after mitosis, 23 after meiosis'],
         'Meiosis halves the chromosome number for gametes'),
    ]),
    S('ib-g9-science:2:2', 'Monohybrid crosses and Punnett squares', [
        ('An allele that shows its effect whenever it is present is', 'dominant', ['recessive', 'codominant', 'a mutation'],
         'A dominant allele is expressed in heterozygotes'),
        ('Two Tt pea plants are crossed (T = tall, dominant). What fraction of the offspring is expected to be short?', '1/4',
         ['1/2', '3/4', '0'], 'Only tt plants are short: 1 in 4'),
        ('A brown-eyed parent (Bb) and a blue-eyed parent (bb) have a child. What is the probability that the child has blue eyes?',
         '50%', ['25%', '75%', '0%'], 'Bb x bb gives Bb and bb in equal numbers'),
    ]),
    S('ib-g9-science:3:2', 'The nervous system and reflex arcs', [
        ('The small gap between two neurones is called a', 'synapse', ['axon', 'dendrite', 'receptor'],
         'Chemicals cross the synapse to pass on the impulse'),
        ('What is the correct order of a reflex arc?', 'receptor → sensory neurone → relay neurone → motor neurone → effector',
         ['effector → motor neurone → relay neurone → sensory neurone → receptor',
          'receptor → motor neurone → relay neurone → sensory neurone → effector',
          'brain → receptor → effector → sensory neurone'], 'Stimulus in, response out'),
        ('Explain why reflex actions are faster than voluntary actions.',
         'The impulse passes through the spinal cord without needing a conscious decision in the brain',
         ['Reflexes use hormones', 'Reflex neurones are longer', 'Reflexes skip the receptor'], 'A shorter pathway saves time'),
    ]),
    S('ib-g9-science:4:3', 'Electron arrangement in shells', [
        ('What is the maximum number of electrons in the first shell?', '2', ['8', '18', '4'], 'The first shell holds 2'),
        ('What is the electron arrangement of sodium (atomic number 11)?', '2,8,1', ['2,9', '8,2,1', '2,8,8,1'],
         '2 + 8 + 1 = 11'),
        ('Explain why Group 1 metals are very reactive.', 'They lose their single outer electron easily to get a stable arrangement',
         ['They have full outer shells', 'They gain electrons easily', 'They have the largest masses'],
         'One electron to lose'),
    ]),
]

ENGLISH_CUR = [
    S('ib-g9-english:1:1', 'Conventions of Gothic fiction', [
        ('Which setting is most typical of Gothic fiction?', 'A crumbling castle at night', ['A sunny beach', 'A busy shopping mall',
                                                                                          'A football stadium'],
         'Gothic settings are isolated, decaying and dark'),
        ('Why do Gothic writers often use storms and darkness?', "To build fear and reflect characters' inner turmoil",
         ['To describe the climate accurately', 'To make the story cheerful', 'Because they wrote in winter'],
         'Pathetic fallacy mirrors emotion'),
        ("'The portrait's eyes seemed to follow her, though she knew it was only paint.' Analyse how the uncanny is created.",
         'Something familiar becomes unsettling, leaving the reader unsure what is real',
         ['The painting is described in technical detail', 'The character is an art expert', 'It is a joke'],
         'The uncanny blends the ordinary and the strange'),
    ]),
    S('ib-g9-english:1:2', 'Creating tension through sentence structure and pacing', [
        ('In a tense scene, a run of short sentences usually', 'speeds up the pace', ['slows everything down', 'adds humour', 'confuses the timeline'],
         'Short sentences read quickly'),
        ('Why might a writer place one very short sentence straight after a long, flowing one?',
         'To build up and then jolt the reader with a sudden change', ['To show poor grammar', 'To fill space', 'To end the chapter'],
         'Contrast creates impact'),
        ("'She waited. And waited. Then, from somewhere below, a knock.' Analyse the effect of the fragments.",
         'They build suspense, making the reader pause on each moment before the knock',
         ['They are grammatical mistakes', 'They make the scene calm', 'They summarise the plot'],
         'Fragments isolate moments and delay the reveal'),
    ]),
    S('ib-g9-english:4:2', 'Propaganda versus protest: perspectives on war', [
        ('Propaganda is', 'information used to promote a particular cause or view, often one-sided',
         ['a neutral news report', 'a type of poem', 'a scientific fact'], 'Propaganda persuades rather than informs'),
        ("A 1914 recruitment poster shows smiling soldiers and the words 'Your country needs YOU'. What is its purpose?",
         'To persuade men to join the army', ['To warn about the horrors of war', 'To report casualty numbers', 'To sell newspapers'],
         'Direct address and positive images persuade'),
        ("How might a soldier-poet's view of war differ from that poster's, and why?",
         'More bitter and realistic, because the poet experienced the suffering first-hand',
         ['Exactly the same, since both were official', 'More cheerful, to raise money', 'There would be no difference'],
         'Perspective is shaped by experience and purpose'),
    ]),
    S('ib-g9-english:2:3', 'Symbols and recurring motifs', [
        ('In literature, a symbol is', 'an object or image that represents a bigger idea',
         ['the main character', 'the title page', 'a list of events'], 'Symbols carry meaning beyond the literal'),
        ('In many stories, a locked door is used to symbolise', 'a barrier, a secret or a lost opportunity',
         ['a holiday', 'good weather', 'wealth'], 'Doors suggest access and denial'),
        ('A novel mentions a caged bird every time the protagonist feels trapped. Analyse this motif.',
         "The caged bird mirrors the protagonist's lack of freedom and reinforces the theme",
         ['The author likes birds', 'It shows a pet shop', 'It is a random detail'], 'Repetition signals significance'),
    ]),
]

SOCIAL_PRE = [
    S('ib-g8-social-science:7:1', 'Causes of the Industrial Revolution', items=[
        ('Which was a cause of the Industrial Revolution in Britain?', 'Plentiful coal and iron, and capital to invest',
         ['The Second World War', 'The invention of computers', 'The fall of Rome'], 'Resources plus investment'),
    ]),
    S('ib-g8-social-science:6:2', 'The Columbian Exchange', items=[
        ('The Columbian Exchange refers to', 'the transfer of plants, animals and diseases between the Americas and Europe, Africa and Asia after 1492',
         ['a bank founded by Columbus', 'a peace treaty', 'a trading company'], 'Named after Columbus\'s voyages'),
        ('Which crop was carried from the Americas to Europe and Asia in the Columbian Exchange?', 'potato',
         ['rice', 'wheat', 'tea'], 'Potatoes, maize and tomatoes came from the Americas'),
    ]),
    S('ib-g8-social-science:9:1', 'Rules, laws and types of government', items=[
        ('In a democracy, laws are made by', 'elected representatives', ['the army', 'a single ruler', 'religious leaders only'],
         'Representatives are accountable to voters'),
        ('Why do societies need laws?', 'To protect rights and settle disputes fairly',
         ['To make rulers rich', 'To stop all change', 'Because people dislike freedom'], 'Laws create order and fairness'),
        ("The UN Convention on the Rights of the Child includes the right to education. Who has the main duty to make sure this right is met?",
         'Governments', ['Children themselves', 'Private companies', 'Tourists'], 'States that ratify the convention are duty-bearers'),
    ]),
    S('ib-g8-social-science:8:1', 'Scarcity and opportunity cost', items=[
        ('Scarcity means that', 'wants are unlimited but resources are limited',
         ['there is too much of everything', 'prices are always low', 'money is not needed'], 'The basic economic problem'),
        ('Opportunity cost is', 'the next best alternative given up', ['the price of a good', 'the total cost of all choices', 'a tax'],
         'Every choice has a cost in what you give up'),
        ('A student goes to a concert instead of working a paid shift worth 40. What is the opportunity cost?',
         'The 40 she could have earned from the shift', ['Only the concert ticket price', 'Nothing', 'Only the bus fare'],
         'The forgone income is the next best alternative'),
    ]),
]

SOCIAL_CUR = [
    S('ib-g9-social-science:1:2', 'Causes of the French Revolution', [
        ('Before 1789, French society was divided into three', 'Estates', ['castes', 'political parties', 'guilds'],
         'Clergy, nobility and everyone else'),
        ('Which was a key cause of the French Revolution?', 'A financial crisis and unfair taxes that fell mostly on the Third Estate',
         ['The Industrial Revolution in France', 'An invasion by Britain', 'The Second World War'], 'Debt and inequality combined'),
        ('How did Enlightenment ideas contribute to the Revolution?', 'They challenged the divine right of kings and promoted equality and rights',
         ['They supported absolute monarchy', 'They banned books', 'They were only about science'],
         'Thinkers such as Rousseau questioned authority'),
    ]),
    S('ib-g9-social-science:1:1', 'Causes of the American Revolution', [
        ("'No taxation without representation' was a slogan of", 'American colonists protesting British taxes',
         ['French peasants', 'British factory workers', 'Indian nationalists'], 'The colonists had no MPs in Parliament'),
        ('The Boston Tea Party (1773) was a protest against', 'British taxes on tea', ['the price of coffee', 'slavery', 'the French'],
         'Colonists dumped tea into Boston Harbour'),
        ("Explain how the Seven Years' War helped cause the American Revolution.", "Britain's war debts led it to impose new taxes on the colonies",
         ['France conquered the colonies', 'It ended slavery', 'It created the United States'], 'The Stamp Act followed in 1765'),
    ]),
    S('ib-g9-social-science:2:1', 'What is nationalism?', [
        ('Nationalism is', "a strong sense of identity with, and loyalty to, one's nation",
         ['a type of government', 'trade between nations', 'rule by a king'], 'Shared language, history and symbols build it'),
        ('Who led the unification of Germany, completed in 1871?', 'Otto von Bismarck', ['Giuseppe Garibaldi', 'Napoleon Bonaparte', 'Giuseppe Mazzini'],
         'Garibaldi and Mazzini were Italian nationalists'),
        ('How can nationalism both unite and divide people?', 'It can unite those who share an identity but exclude or create conflict with others',
         ['It always brings peace', 'It only divides', 'It has no effect'], 'Balanced judgement needs both sides'),
    ]),
    S('ib-g9-social-science:4:2', 'Push and pull factors of rural-urban migration', [
        ('Which of these is a push factor in a rural area?', 'Lack of jobs', ['Better hospitals in the city', 'City nightlife', 'Higher wages in the city'],
         'Push factors are reasons to leave'),
        ('Why are many megacities growing fastest in lower-income countries today?', 'High rural-urban migration combined with natural increase',
         ['Falling birth rates', 'People leaving cities', 'No jobs in cities'], 'Both migration and births add people'),
        ('Evaluate the effects of rural-urban migration on a city.', 'More workers for industry and services, but pressure on housing and services',
         ['Only positive, with no problems', 'Only negative, with no benefits', "It reduces the city's population"],
         'Evaluation weighs both sides'),
    ]),
]

DESIGN = {
    'designId': 'g9-ib', 'grade': 9, 'stream': 'none', 'boards': ['ib'],
    'title': 'IB MYP Year 4 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G9, MATHS_CUR),
        G('science', 'Sciences', SCIENCE_PRE_G9, SCIENCE_CUR),
        G('english', 'Language and Literature', ENGLISH_PRE_G9, ENGLISH_CUR),
        G('social-science', 'Individuals and Societies', SOCIAL_PRE, SOCIAL_CUR),
    ],
}
