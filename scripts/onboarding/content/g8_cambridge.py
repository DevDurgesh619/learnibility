"""Design g8-cambridge: Cambridge Lower Secondary Stage 9 (Maths 0862, Science 0893, English 0861, Humanities 0839)."""
from dsl import S, G
from content.shared_g8 import MATHS_PRE_G8, SCIENCE_PRE_G8, ENGLISH_PRE_G8
from content.shared_intl import SOCIAL_PRE_INTL_G8

MATHS_CUR = [
    S('cambridge-g8-maths:1:1', 'Irrational numbers', [
        ('Which of these numbers is irrational?', '√2', ['0.75', '3/8', '√49'], '√49 = 7; only √2 cannot be written as a fraction'),
        ('Which statement is true?', '√12 lies between 3 and 4', ['√12 lies between 2 and 3', '√12 lies between 4 and 5', '√12 is rational'],
         '3² = 9 and 4² = 16, and 12 is between them'),
        ('Which of these products is a rational number?', '√8 x √2', ['√3 x √2', '√5 x 2', 'π x 2'], '√8 x √2 = √16 = 4'),
    ]),
    S('cambridge-g8-maths:1:2', 'Standard form', [
        ('Write 45 000 in standard form.', '4.5 x 10⁴', ['45 x 10³', '4.5 x 10³', '0.45 x 10⁵'],
         'Standard form is A x 10ⁿ with 1 ≤ A < 10'),
        ('Write 0.000 36 in standard form.', '3.6 x 10⁻⁴', ['3.6 x 10⁻³', '36 x 10⁻⁵', '3.6 x 10⁴'],
         'Move the decimal point 4 places to the right'),
        ('Work out (3 x 10⁵) x (4 x 10³). Give your answer in standard form.', '1.2 x 10⁹', ['12 x 10⁸', '1.2 x 10⁸', '7 x 10⁸'],
         '3 x 4 = 12 and 10⁵ x 10³ = 10⁸; 12 x 10⁸ = 1.2 x 10⁹'),
    ]),
    S('cambridge-g8-maths:1:3', 'Zero and negative indices', [
        ('Write the value of 7⁰.', '1', ['0', '7', '70'], 'Any non-zero number to the power 0 is 1'),
        ('Write 2⁻³ as a fraction.', '1/8', ['-8', '-6', '1/6'], '2⁻³ = 1/2³ = 1/8'),
        ('Simplify (x⁴)³ ÷ x⁵.', 'x⁷', ['x²', 'x¹²', 'x¹⁷'], '(x⁴)³ = x¹²; x¹² ÷ x⁵ = x⁷'),
    ]),
    S('cambridge-g8-maths:2:3', 'Expanding the product of two linear expressions', [
        ('Expand 3(x + 4).', '3x + 12', ['3x + 4', 'x + 12', '3x + 7'], 'Multiply both terms by 3'),
        ('Expand and simplify (x + 3)(x + 5).', 'x² + 8x + 15', ['x² + 15x + 8', 'x² + 8x + 8', '2x + 8'],
         'x² + 5x + 3x + 15'),
        ('Expand and simplify (2x - 3)(x + 4).', '2x² + 5x - 12', ['2x² - 5x - 12', '2x² + 11x - 12', '2x² + 5x + 12'],
         '2x² + 8x - 3x - 12'),
    ]),
]

SCIENCE_CUR = [
    S('cambridge-g8-science:1:1', 'Photosynthesis', [
        ('Which word equation represents photosynthesis?', 'carbon dioxide + water → glucose + oxygen',
         ['glucose + oxygen → carbon dioxide + water', 'oxygen + water → glucose + carbon dioxide',
          'carbon dioxide + oxygen → glucose + water'], 'Light energy turns carbon dioxide and water into glucose and oxygen'),
        ('Why do greenhouse plants often grow faster when extra carbon dioxide is added to the air?',
         'Carbon dioxide is a raw material for photosynthesis, so more glucose can be made',
         ['Carbon dioxide gives plants energy directly', 'Carbon dioxide warms the soil', 'Plants absorb carbon dioxide through their roots'],
         'More raw material raises the rate when carbon dioxide is the limiting factor'),
        ('Pondweed gives off 12 bubbles per minute with a lamp 10 cm away and 4 bubbles per minute with the lamp 40 cm away. Which conclusion is best supported?',
         'The rate of photosynthesis falls as light intensity falls',
         ['Pondweed photosynthesises only when the lamp is at 10 cm', 'The bubbles are carbon dioxide',
          'Temperature has no effect on photosynthesis'],
         'Moving the lamp away lowers light intensity; fewer oxygen bubbles means a lower rate'),
    ]),
    S('cambridge-g8-science:1:3', 'The carbon cycle', [
        ('Which process removes carbon dioxide from the atmosphere?', 'photosynthesis', ['respiration', 'combustion', 'decomposition'],
         'The other three release carbon dioxide'),
        ('Fossil fuels contain carbon because', 'they formed from the remains of organisms that took in carbon millions of years ago',
         ['carbon dioxide soaks into rocks every day', 'they are made in factories from carbon', 'they absorb carbon from the air when burned'],
         'Coal, oil and gas are ancient plant and plankton remains'),
        ('Large areas of forest are cut down and burned. What happens to the amount of carbon dioxide in the atmosphere, and why?',
         'It rises: burning releases carbon dioxide and fewer trees are left to absorb it',
         ['It falls, because ash absorbs carbon dioxide', 'It stays the same, because grass replaces the trees at once',
          'It rises only because animals respire more'], 'Two effects add up: more released, less removed'),
    ]),
    S('cambridge-g8-science:2:1', 'Atomic structure and the Periodic Table', [
        ('Which particle in an atom has a negative charge?', 'electron', ['proton', 'neutron', 'nucleus'],
         'Protons are positive, neutrons neutral'),
        ('An atom has 11 protons and 12 neutrons. How many electrons does the neutral atom have?', '11', ['12', '23', '1'],
         'A neutral atom has as many electrons as protons'),
        ('Elements in the same group of the Periodic Table have similar chemical properties because',
         'they have the same number of electrons in their outer shell',
         ['they have the same number of neutrons', 'they have the same mass', 'they were discovered at the same time'],
         'Outer-shell electrons decide how an element reacts'),
    ]),
    S('cambridge-g8-science:3:1', 'Density', [
        ('Density is calculated as', 'mass ÷ volume', ['volume ÷ mass', 'mass x volume', 'weight ÷ area'], 'ρ = m / V'),
        ('A block has a mass of 240 g and a volume of 80 cm³. What is its density?', '3 g/cm³',
         ['0.33 g/cm³', '320 g/cm³', '160 g/cm³'], '240 ÷ 80 = 3'),
        ('A solid has a density of 0.8 g/cm³; water has a density of 1.0 g/cm³. What happens when the solid is put in water, and why?',
         'It floats, because it is less dense than water',
         ['It sinks, because it is less dense than water', 'It floats, because it is heavier than water',
          'It sinks, because density does not affect floating'], 'Objects less dense than a liquid float in it'),
    ]),
]

ENGLISH_CUR = [
    S('cambridge-g8-english:1:2', 'Fiction: narrative viewpoint', [
        ("'I opened the door slowly and saw that the room was empty.' This sentence is written in the", 'first person',
         ['second person', 'third person', 'passive voice'], "The narrator uses 'I'"),
        ('Why might a writer tell a mystery story in the first person?',
         'The reader only knows what the narrator knows, which builds suspense',
         ['It makes the story shorter', 'First person is always more formal', "It shows every character's thoughts"],
         'Limited knowledge keeps the reader guessing'),
        ("Read: 'Marcus said he was fine. His hands, however, would not stop shaking.' What does the writer suggest by putting these sentences together?",
         'Marcus is hiding how anxious he really is',
         ['Marcus is cold', 'Marcus is lying about his name', 'Marcus is excited about good news'],
         "'However' signals that his body contradicts his words"),
    ]),
    S('cambridge-g8-english:1:1', "Fiction: writers' use of language", [
        ("In 'The thunder growled over the hills', which word creates the strongest sense of threat?", 'growled',
         ['over', 'hills', 'thunder'], "'Growled' makes the thunder sound like a dangerous animal"),
        ("Read: 'The corridor stretched on, endless and silent.' What effect do the words 'endless and silent' create?",
         'A feeling of isolation and unease', ['A cheerful, busy mood', 'A sense of humour', 'A feeling of speed'],
         'No end and no sound make the place feel empty and eerie'),
        ("A writer uses very short sentences in a chase scene: 'He ran. Faster. The gate. Locked.' Why?",
         "To build pace and tension that mirror the character's panic",
         ['Because the writer ran out of words', 'To make the scene more formal', 'To slow the story down'],
         'Short, broken sentences speed up reading and feel breathless'),
    ]),
    S('cambridge-g8-english:4:2', 'Non-fiction: fact, opinion and persuasion', [
        ('Which sentence is a fact?', 'The museum opens at 9 a.m. on weekdays.',
         ['The museum is the most exciting place in the city.', 'Everyone should visit the museum.',
          "The museum's cafe serves the best coffee."], 'A fact can be checked'),
        ("An advert says: 'Join thousands of happy customers who already love SparkClean!' Which persuasive technique is this?",
         'Appeal to popularity (bandwagon)', ['Rhetorical question', 'Statistics from an expert', 'Personal anecdote'],
         'It suggests you should buy it because many others do'),
        ("A leaflet about a planned park includes only residents' positive comments and no costs. What should a careful reader conclude?",
         'The leaflet is one-sided, so more evidence is needed before judging',
         ['Everyone supports the park', 'The park will be free', 'The leaflet is a news report'],
         'Missing costs and opposing views signal bias'),
    ]),
    S('cambridge-g8-english:3:1', 'Poetry: imagery and sound', [
        ("'The stars were diamonds scattered on velvet' is an example of", 'a metaphor', ['a simile', 'onomatopoeia', 'a pun'],
         "The stars are said to BE diamonds, without 'like' or 'as'"),
        ('Which line uses onomatopoeia?', 'The bees buzzed among the roses.',
         ['The bees were busy workers.', 'The roses were as red as blood.', 'Roses rose in rows.'],
         "'Buzzed' imitates the sound it describes"),
        ("A poem describes a city at night as 'a sleeping giant, breathing slow'. What impression is created?",
         'The city seems huge, calm and alive even while quiet',
         ['The city is dangerous and violent', 'The city is small and empty', 'The poet dislikes giants'],
         'A giant suggests size; sleeping and breathing suggest calm life'),
    ]),
]

SOCIAL_CUR = [
    S('cambridge-g8-social-science:2:1', 'History: the Industrial Revolution, causes and consequences', [
        ('The Industrial Revolution began in the 18th century in', 'Britain', ['China', 'Brazil', 'Japan'],
         'Coal, capital, colonies and inventions came together in Britain first'),
        ('Which was a major consequence of the Industrial Revolution?', 'Rapid growth of towns as people moved to work in factories',
         ['The end of all farming', 'A fall in population', 'The decline of coal mining'], 'Factory work drew people from the countryside'),
        ('Why did child labour in factories become common in the early 1800s?',
         'Children could be paid less and many families needed the income',
         ['Children were stronger than adults', 'Laws required children to work', 'Factories had no machines'],
         'Low wages and poverty drove it until factory laws were passed'),
    ]),
    S('cambridge-g8-social-science:6:2', 'Geography: weather and climate', [
        ('Climate means', 'the average weather of a place over a long period', ["today's weather", 'the temperature at noon', 'a sudden storm'],
         'Climate is usually averaged over about 30 years'),
        ('Why are places near the Equator generally hotter than places near the poles?', "The Sun's rays are more concentrated there",
         ['They are much closer to the Sun', 'They have more oceans', 'Their days are always longer'],
         'Near the Equator the Sun is high, so its energy falls on a smaller area'),
        ('Coastal cities often have milder winters than inland cities at the same latitude. Why?',
         'The sea heats and cools more slowly than land, so it keeps coastal temperatures moderate',
         ['Coasts get more sunshine', 'Cities produce their own heat', 'Inland areas are closer to the poles'],
         'Water has a high heat capacity'),
    ]),
    S('cambridge-g8-social-science:7:1', 'Geography: population and migration', [
        ('Population density means', 'the number of people per square kilometre',
         ['the total population of a country', 'the birth rate', 'the number of cities'], 'Density = people ÷ area'),
        ('Which factor most often pushes people to move from rural areas to cities?', 'Lack of jobs and services in the countryside',
         ['Better farmland in the countryside', 'A lower cost of living in cities', 'Fewer people in cities'],
         'Push factors drive people away; jobs in cities pull them in'),
        ('A country has a birth rate of 30 per 1000 and a death rate of 10 per 1000. What is its natural increase?',
         '20 per 1000 (2% a year)', ['40 per 1000', '3% a year', 'The population is falling'], 'Birth rate minus death rate'),
    ]),
    S('cambridge-g8-social-science:8:1', 'Citizenship: rights and responsibilities', [
        ('The United Nations adopted the Universal Declaration of Human Rights in', '1948', ['1918', '1776', '2000'],
         'It was adopted on 10 December 1948'),
        ('Which is a responsibility that comes with the right to free speech?', 'Not spreading lies that harm others',
         ['Speaking only when asked', 'Always agreeing with the government', 'Avoiding all debate'],
         'Rights are limited where they harm the rights of others'),
        ('A town must choose between building a road through a forest and keeping the forest. Which approach best balances different perspectives?',
         'Consult residents, businesses and environmental experts, then weigh the costs and benefits',
         ['Let the richest company decide', 'Build the road without discussion', 'Let only drivers vote'],
         'Good decisions consider several stakeholders and the evidence'),
    ]),
]

DESIGN = {
    'designId': 'g8-cambridge', 'grade': 8, 'stream': 'none', 'boards': ['cambridge'],
    'title': 'Cambridge Lower Secondary Stage 9 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G8, MATHS_CUR),
        G('science', 'Science', SCIENCE_PRE_G8, SCIENCE_CUR),
        G('english', 'English', ENGLISH_PRE_G8, ENGLISH_CUR),
        G('social-science', 'Humanities', SOCIAL_PRE_INTL_G8, SOCIAL_CUR),
    ],
}
