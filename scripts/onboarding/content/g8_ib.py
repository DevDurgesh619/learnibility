"""Design g8-ib: IB MYP Year 3 (Mathematics, Sciences, Language and Literature, Individuals and Societies).
Stems use MYP command terms (identify, outline, explain, analyse, evaluate)."""
from dsl import S, G
from content.shared_g8 import MATHS_PRE_G8, SCIENCE_PRE_G8, ENGLISH_PRE_G8
from content.shared_intl import SOCIAL_PRE_INTL_G8

MATHS_CUR = [
    S('ib-g8-maths:1:1', 'Rational numbers: ordering and comparing', [
        ('Identify the rational number.', '-3/5', ['√3', 'π', '√7'], 'A rational number can be written as a fraction of integers'),
        ('Order from smallest to largest: -0.5, 1/3, -2/3, 0.3', '-2/3, -0.5, 0.3, 1/3',
         ['-0.5, -2/3, 0.3, 1/3', '-2/3, -0.5, 1/3, 0.3', '0.3, 1/3, -0.5, -2/3'], '-2/3 ≈ -0.67 and 1/3 ≈ 0.33'),
        ('Which is larger, 5/8 or 0.6, and by how much?', '5/8, by 0.025', ['0.6, by 0.025', '5/8, by 0.25', 'They are equal'],
         '5/8 = 0.625; 0.625 - 0.6 = 0.025'),
    ]),
    S('ib-g8-maths:2:4', 'Laws of exponents and scientific notation', [
        ('Simplify 10³ x 10².', '10⁵', ['10⁶', '100⁵', '20⁵'], 'Same base: add the exponents'),
        ('The distance from Earth to the Sun is about 150 000 000 km. Write this in scientific notation.', '1.5 x 10⁸ km',
         ['1.5 x 10⁷ km', '15 x 10⁷ km', '1.5 x 10⁹ km'], 'Move the decimal point 8 places'),
        ('Light travels about 3 x 10⁵ km every second. About how long does sunlight take to travel 1.5 x 10⁸ km to Earth?',
         '500 seconds', ['50 seconds', '5000 seconds', '4.5 x 10¹³ seconds'], '1.5 x 10⁸ ÷ 3 x 10⁵ = 0.5 x 10³ = 500'),
    ]),
    S('ib-g8-maths:3:1', 'Percentages and percentage change', [
        ('What is 15% of 200?', '30', ['15', '20', '300'], '0.15 x 200 = 30'),
        ('A jacket costs 80 euros and is reduced by 25%. What is the new price?', '60 euros', ['55 euros', '20 euros', '75 euros'],
         '25% of 80 is 20; 80 - 20 = 60'),
        ("A town's population grew from 40 000 to 46 000. What is the percentage increase?", '15%', ['6%', '13%', '46%'],
         'Increase 6 000 ÷ original 40 000 = 0.15'),
    ]),
    S('ib-g8-maths:5:2', 'Solving linear equations', [
        ('Solve x + 7 = 12.', '5', ['19', '7', '-5'], 'Subtract 7 from both sides'),
        ('Solve 3x - 4 = 11.', '5', ['7/3', '15', '3'], 'Add 4: 3x = 15, so x = 5'),
        ('Solve 2(x + 3) = 4x - 8.', '7', ['1', '-7', '3.5'], '2x + 6 = 4x - 8, so 14 = 2x'),
    ]),
]

SCIENCE_CUR = [
    S('ib-g8-science:2:2', 'Cells: structures and functions', [
        ('Identify the structure found in plant cells but not in animal cells.', 'Cell wall', ['Cell membrane', 'Nucleus', 'Cytoplasm'],
         'Plant cells have a cellulose cell wall (and chloroplasts and a large vacuole)'),
        ('Outline the function of mitochondria.', 'They release energy from glucose in respiration',
         ['They make proteins', 'They control what enters the cell', 'They store water'], 'Mitochondria are the site of aerobic respiration'),
        ('Root cells of a plant have no chloroplasts. Explain why.', 'Roots are underground without light, so they cannot photosynthesise',
         ['Chloroplasts are only made in flowers', 'Roots need to stay white to be strong', 'Chloroplasts would block water uptake'],
         'Chloroplasts are only useful where light reaches'),
    ]),
    S('ib-g8-science:4:1', 'Body systems: the circulatory system', [
        ('Which blood vessels carry blood away from the heart?', 'arteries', ['veins', 'capillaries', 'valves'],
         'Arteries carry blood away; veins return it'),
        ('Explain why the wall of the left ventricle is thicker than the wall of the right ventricle.',
         'It pumps blood around the whole body, which needs more force',
         ['It holds more blood', 'It pumps blood only to the lungs', 'It receives blood from the body'],
         'The right ventricle only pumps to the nearby lungs'),
        ('During exercise your heart rate increases. Which explanation is best?',
         'Muscles need oxygen and glucose delivered faster for respiration',
         ['The heart needs to cool down', 'Blood becomes thicker', 'The lungs stop working during exercise'],
         'Working muscles respire faster'),
    ]),
    S('ib-g8-science:6:1', 'The particle model of matter', [
        ('In which state are particles closest together and only vibrating in fixed positions?', 'solid', ['liquid', 'gas', 'plasma'],
         'Solids have a fixed shape because particles cannot move past each other'),
        ('Explain why a gas can be compressed but a solid cannot easily be compressed.', 'Gas particles have large spaces between them',
         ['Gas particles are smaller', 'Solid particles move faster', 'Gases have no mass'], 'Compression pushes particles into the gaps'),
        ('A balloon left in a hot car expands. Explain this using the particle model.',
         'The particles gain kinetic energy, move faster and hit the balloon wall harder and more often',
         ['The particles grow larger when heated', 'Heat adds new particles to the balloon', 'The rubber shrinks in the heat'],
         'Particles do not change size; their motion changes'),
    ]),
    S('ib-g8-science:10:2', 'Forces and motion: speed and balanced forces', [
        ('Speed is calculated as', 'distance ÷ time', ['time ÷ distance', 'distance x time', 'mass x distance'], 'v = d / t'),
        ('A cyclist travels 18 km in 45 minutes. What is the average speed?', '24 km/h', ['0.4 km/h', '13.5 km/h', '40 km/h'],
         '45 minutes = 0.75 h; 18 ÷ 0.75 = 24'),
        ('A moving box is pushed to the right with 50 N while friction acts to the left with 50 N. Describe its motion.',
         'It keeps moving at a constant speed', ['It stops immediately', 'It speeds up', 'It moves to the left'],
         'Balanced forces mean no change in motion'),
    ]),
]

ENGLISH_CUR = [
    S('ib-g8-english:2:2', 'Narrative point of view', [
        ("A story narrated by a character who uses 'I' is written in", 'the first-person point of view',
         ['the third-person omniscient point of view', 'the second-person point of view', 'an objective point of view'],
         "'I' marks a first-person narrator"),
        ('What is the main difference between a third-person limited narrator and a third-person omniscient narrator?',
         "A limited narrator follows one character's thoughts; an omniscient narrator can reveal any character's thoughts",
         ["A limited narrator uses 'I'; an omniscient narrator uses 'you'", 'Omniscient narrators are always unreliable',
          'There is no difference'], 'Omniscient means all-knowing'),
        ("Read: 'Of course I wasn't jealous, I told myself, slamming the door a little harder than I meant to.' Analyse what this reveals about the narrator.",
         'The narrator is unreliable: their action contradicts what they claim',
         ['The narrator is calm and honest', 'The door was broken', 'The narrator is talking to a friend'],
         "'I told myself' and the slammed door show self-deception"),
    ]),
    S('ib-g8-english:6:2', 'Tone and mood', [
        ('In a text, tone means', "the writer's attitude towards the subject", ['the length of the text', 'the number of characters', 'the setting'],
         'Tone is shown through word choice'),
        ("Which word best describes the tone of: 'Oh wonderful, another rainy holiday. Just what I wanted.'?", 'sarcastic',
         ['joyful', 'fearful', 'neutral'], 'The speaker says the opposite of what they mean'),
        ("A writer describes a market as 'a riot of colour, voices tumbling over each other'. Which mood is created?",
         'Lively, busy excitement', ['Quiet sadness', 'Danger and fear', 'Boredom'],
         "'Riot of colour' and 'tumbling' voices suggest energy"),
    ]),
    S('ib-g8-english:4:1', 'Non-literary texts: purpose and audience', [
        ('The main purpose of most advertisements is to', 'persuade', ['inform only', 'entertain only', 'record history'],
         'Adverts aim to make you buy, join or act'),
        ('A poster uses bright cartoons, simple words and a chance to win a toy. Who is the most likely target audience?', 'Young children',
         ['Business executives', 'Retired scientists', 'University lecturers'], 'Every feature suits young readers'),
        ("A charity website tells one child's story instead of showing national statistics. Evaluate why the creators chose this.",
         'A personal story creates an emotional connection that can make readers more likely to donate',
         ['Statistics are always false', 'Websites cannot show numbers', 'One story is more accurate than data'],
         'Pathos often persuades more strongly than numbers'),
    ]),
    S('ib-g8-english:3:3', 'Poetry: form and structure', [
        ('A group of lines forming a section of a poem is called a', 'stanza', ['paragraph', 'chapter', 'caption'],
         'Stanzas are the paragraphs of poetry'),
        ('Why might a poet repeat the same line at the end of every stanza?', 'To emphasise a key idea and create rhythm',
         ['To fill space', 'Because poems must repeat lines', 'To confuse the reader'], 'A refrain reinforces meaning'),
        ("In a poem, the lines get shorter and shorter as a character falls asleep. Analyse the effect of this structure.",
         'The shrinking lines mirror the character slowing down and drifting off',
         ['It shows the poet ran out of ideas', 'It makes the poem louder', 'It has no effect on meaning'],
         'Form can enact meaning'),
    ]),
]

SOCIAL_CUR = [
    S('ib-g8-social-science:10:1', 'Migration: causes and effects', [
        ('Migration means', 'people moving from one place to live in another',
         ['the birth rate of a country', 'seasonal changes in weather', 'trade between countries'], 'Migration is a change of home'),
        ('Which of these is a pull factor for migrants?', 'Better job opportunities', ['War in the home country', 'Drought', 'Unemployment at home'],
         'Pull factors attract people to a new place'),
        ('Explain one way migration can benefit the country that migrants leave.',
         'Migrants send money home (remittances) that supports families and the economy',
         ['It increases unemployment at home', 'It always reduces skills at home', 'It has no effects'],
         'Remittances are a major income source for many countries'),
    ]),
    S('ib-g8-social-science:12:3', 'Evaluating sources: origin, purpose, value, limitation', [
        ("The 'origin' of a source refers to", 'who made it, when and where', ['how long it is', 'its colour', 'its price'],
         'Origin helps judge reliability'),
        ('A government poster from 1940 asks citizens to save food for the war effort. What is one limitation of using it to find out how people actually felt?',
         'It shows what the government wanted people to think, not necessarily what they thought',
         ['It is too old to be useful', 'Posters never contain information', 'It was not made in 1940'],
         'Propaganda reveals intentions more than opinions'),
        ('Which set of sources gives the most balanced view of a protest?', "A police report, a protester's diary and a neutral newspaper",
         ['Three police reports', "Only the protester's diary", 'A film made 50 years later'],
         'Different perspectives can be cross-checked'),
    ]),
    S('ib-g8-social-science:11:3', 'Resources and sustainability', [
        ('Sustainability means', "meeting present needs without harming future generations' ability to meet theirs",
         ['using resources as fast as possible', 'only using fossil fuels', 'stopping all economic growth'],
         'This is the Brundtland definition'),
        ('Which is an example of a sustainable practice?', 'Replanting trees after logging', ['Overfishing', 'Burning crop waste', 'Draining wetlands for building'],
         'Replanting replaces what was used'),
        ('A fishing community limits how many fish can be caught each year. Evaluate this policy.',
         'It protects fish stocks for the future, though it may lower income in the short term',
         ['It has only benefits', 'It will make the fish extinct', 'It increases catches immediately'],
         'Evaluation weighs benefits against costs'),
    ]),
    S('ib-g8-social-science:10:2', 'Urbanisation', [
        ('Urbanisation is', 'the increasing share of people living in towns and cities',
         ['the building of new farms', 'people moving to the countryside', 'a fall in city populations'], 'Urban means towns and cities'),
        ('Which is a common problem in fast-growing cities?', 'Traffic congestion and housing shortages',
         ['Too much farmland', 'A lack of people', 'Too many forests'], 'Infrastructure struggles to keep up'),
        ('Suggest the most effective long-term way for a city to reduce traffic congestion.', 'Invest in reliable public transport and cycle lanes',
         ['Build more car parks in the centre', 'Lower fuel prices', 'Ban buses'], 'Giving people alternatives reduces car trips'),
    ]),
]

DESIGN = {
    'designId': 'g8-ib', 'grade': 8, 'stream': 'none', 'boards': ['ib'],
    'title': 'IB MYP Year 3 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G8, MATHS_CUR),
        G('science', 'Sciences', SCIENCE_PRE_G8, SCIENCE_CUR),
        G('english', 'Language and Literature', ENGLISH_PRE_G8, ENGLISH_CUR),
        G('social-science', 'Individuals and Societies', SOCIAL_PRE_INTL_G8, SOCIAL_CUR),
    ],
}
