"""Design g9-cbse: CBSE Class 9 (new NCERT Ganita Manjari, Exploration, Kaveri, Understanding Society)."""
from dsl import S, G
from content.shared_g9 import MATHS_PRE_G9, SCIENCE_PRE_G9, ENGLISH_PRE_G9

MATHS_CUR = [
    S('cbse-g9-maths:1:1', 'Cartesian plane: quadrants and plotting points', [
        ('In which quadrant does the point (-3, 4) lie?', 'Second', ['First', 'Third', 'Fourth'], 'x negative, y positive'),
        ('Point P lies on the x-axis, 5 units to the left of the origin. What are its coordinates?', '(-5, 0)',
         ['(0, -5)', '(5, 0)', '(-5, -5)'], 'Points on the x-axis have y = 0'),
        ('Three vertices of a rectangle are (1, 1), (5, 1) and (5, 4). What is the fourth vertex?', '(1, 4)',
         ['(4, 1)', '(4, 5)', '(5, 5)'], 'Opposite sides are parallel to the axes'),
    ]),
    S('cbse-g9-maths:1:2', 'Distance between two points using the Baudhayana-Pythagoras theorem', [
        ('What is the distance between (0, 0) and (3, 4)?', '5', ['7', '25', '12'], '√(3² + 4²) = 5'),
        ('What is the distance between (2, 3) and (8, 11)?', '10', ['14', '100', '8'], '√(6² + 8²) = √100 = 10'),
        ('A(0, 0), B(4, 0) and C(0, 3) form a triangle. Is it right-angled, and how long is BC?', 'Yes, and BC = 5',
         ['No, and BC = 7', 'Yes, and BC = 7', 'No, and BC = 5'], 'The angle at A is 90°; BC = √(16 + 9) = 5'),
    ]),
    S('cbse-g9-maths:2:2', 'Linear polynomials: value and zero', [
        ('Which of these is a linear polynomial?', '3x + 2', ['x² + 1', '1/x + 2', 'x³'], 'The highest power of x is 1'),
        ('What is the zero of p(x) = 2x - 6?', '3', ['-3', '6', '1/3'], '2x - 6 = 0 gives x = 3'),
        ('If p(x) = ax + 5 and p(2) = 11, what is a?', '3', ['8', '2', '5.5'], '2a + 5 = 11'),
    ]),
    S('cbse-g9-maths:3:3', 'Irrational numbers', [
        ('Which of these numbers is irrational?', '√5', ['√16', '0.25', '22/7'], '√16 = 4; 22/7 is a fraction'),
        ('The decimal expansion of an irrational number is', 'non-terminating and non-recurring',
         ['terminating', 'non-terminating and recurring', 'always zero after five places'], 'Recurring decimals are rational'),
        ('Which of these numbers is rational?', '(3 + √2) - √2', ['2 + √3', '√2 x √3', 'π + 1'], 'The √2 terms cancel, leaving 3'),
    ]),
]

SCIENCE_CUR = [
    S('cbse-g9-science:1:3', 'Cell organelles', [
        ("Which organelle is called the 'powerhouse of the cell'?", 'mitochondria', ['ribosome', 'Golgi apparatus', 'lysosome'],
         'Mitochondria release energy as ATP'),
        ("Lysosomes are called 'suicide bags' because", "their enzymes can digest the cell's own parts if the cell is damaged",
         ['they store water', 'they make proteins', 'they trap sunlight'], 'Lysosomes hold digestive enzymes'),
        ('Cells of a gland that secretes large amounts of protein are likely to have many',
         'ribosomes and a well-developed ER and Golgi apparatus', ['chloroplasts', 'large vacuoles', 'cell walls'],
         'Proteins are made on ribosomes and packaged by the ER and Golgi'),
    ]),
    S('cbse-g9-science:1:2', 'Plasma membrane: diffusion and osmosis', [
        ('Movement of water across a selectively permeable membrane from a dilute to a concentrated solution is called',
         'osmosis', ['diffusion', 'transpiration', 'respiration'], 'Osmosis is the diffusion of water across a membrane'),
        ('Raisins left in water swell up because', 'water enters them by osmosis',
         ['sugar leaves them by osmosis', 'air enters them', 'they absorb salt'], 'The raisin cells are more concentrated than water'),
        ('Salt sprinkled on cucumber slices makes drops of water appear on them. Explain why.',
         'Water moves out of the cells by osmosis into the more concentrated salt solution',
         ['Salt melts into water', 'Cucumber cells make water when salted', 'The salt crystals burst'],
         'Water moves from dilute (cell sap) to concentrated (salt)'),
    ]),
    S('cbse-g9-science:3:2', 'Speed, velocity and average speed', [
        ('Displacement is different from distance because displacement', 'has a direction',
         ['is always larger', 'is measured in seconds', 'is a scalar'], 'Displacement is a vector'),
        ('A runner completes one full lap of a 400 m track in 80 s. What are her average speed and displacement?',
         '5 m/s and 0 m', ['5 m/s and 400 m', '0 m/s and 0 m', '80 m/s and 400 m'], 'She ends where she started'),
        ('A car travels 30 km at 60 km/h and then 30 km at 30 km/h. What is its average speed for the whole trip?', '40 km/h',
         ['45 km/h', '50 km/h', '35 km/h'], 'Total 60 km in 0.5 h + 1 h = 1.5 h'),
    ]),
    S('cbse-g9-science:3:3', 'Acceleration and the equations of motion', [
        ('A car speeds up from rest to 20 m/s in 5 s. What is its acceleration?', '4 m/s²', ['100 m/s²', '0.25 m/s²', '20 m/s²'],
         'a = (20 - 0) ÷ 5'),
        ('A bus moving at 15 m/s brakes with a uniform retardation of 3 m/s². How long does it take to stop?', '5 s',
         ['45 s', '12 s', '18 s'], 'v = u + at: 0 = 15 - 3t'),
        ('A ball is dropped from rest and falls 20 m (take a = 10 m/s²). Using v² = u² + 2as, how fast is it moving just before it lands?',
         '20 m/s', ['200 m/s', '400 m/s', '10 m/s'], 'v² = 0 + 2 x 10 x 20 = 400'),
    ]),
]

ENGLISH_CUR = [
    S('cbse-g9-english:1:2', 'How I Taught My Grandmother to Read: literacy and determination', [
        ('Read: "Krishtakka, the narrator\'s grandmother, could not read. Each week she waited for her granddaughter to read the next part of a serialised novel aloud. When the girl went away for a few days, Krishtakka decided to learn to read herself." Why did she decide to learn?',
         'She could not follow the story while her granddaughter was away',
         ['Her teacher forced her', 'She wanted to become a writer', 'She needed to read bus timetables'],
         'Her dependence on the granddaughter became a problem when the girl left'),
        ('Read: "Krishtakka, the narrator\'s grandmother, could not read. When her granddaughter went away for a few days, she decided to learn to read herself, and asked the girl to teach her." What does this show about her?',
         'Determination: she believed it was never too late to learn', ['She was impatient', 'She disliked her granddaughter',
                                                                         'She preferred only listening'],
         'An elderly learner choosing to start shows resolve'),
        ('In the story, the granddaughter becomes her grandmother\'s teacher. What is the effect of this role reversal?',
         'It shows learning can flow from young to old and challenges the usual roles',
         ['It shows children are always wiser', 'It only makes the story funny', 'It shows the grandmother could not learn'],
         'The reversal carries the theme of respect for learning at any age'),
    ]),
    S('cbse-g9-english:1:3', 'Sequence of tenses', [
        ('Choose the correct word: She said that she ___ tired.', 'was', ['is', 'will be', 'has'],
         'A past reporting verb takes a past tense in the reported clause'),
        ('Choose the correct words: If it rains tomorrow, we ___ the match.', 'will postpone',
         ['would postpone', 'postponed', 'had postponed'], 'First conditional: if + present, will + verb'),
        ('Which sentence is correct?', 'He told me that he had finished his homework before dinner.',
         ['He told me that he has finished his homework before dinner.', 'He told me that he finish his homework before dinner.',
          'He told me that he will finished his homework before dinner.'], 'An earlier past action takes the past perfect'),
    ]),
    S('cbse-g9-english:2:3', 'Bharat Our Land: personification, alliteration and apostrophe', [
        ("'O mighty river, carry my song!' Speaking directly to a river is an example of", 'apostrophe',
         ['alliteration', 'simile', 'hyperbole'], 'Apostrophe addresses something absent or non-human'),
        ('Which line contains personification?', 'The mountains stand guard over the sleeping valley.',
         ['The mountains are very high.', 'The river is like a ribbon.', 'Big boulders bounce.'],
         'Standing guard and sleeping are human actions'),
        ("Why might a patriotic poem describe the land as a 'mother'?",
         'To suggest love, care and a bond of belonging between the people and the land',
         ['To show the land is old', "Because the poet's mother lived there", "To describe a mountain's shape"],
         'The metaphor carries emotional meaning'),
    ]),
    S('cbse-g9-english:3:4', 'Modal auxiliaries', [
        ('You ___ wear a helmet while riding a scooter; it is the law.', 'must', ['may', 'might', 'could'],
         "'Must' expresses obligation"),
        ('___ I borrow your pen, please?', 'May', ['Must', 'Should', 'Need'], "'May' asks politely for permission"),
        ('Which sentence expresses a strong deduction?', 'She must be at home; her bicycle is outside.',
         ['She may come tomorrow.', 'She should study more.', 'She can swim well.'],
         "'Must be' draws a confident conclusion from evidence"),
    ]),
]

SOCIAL_PRE = [
    S('cbse-g8-social-science:6:2', 'Parliament: Lok Sabha and Rajya Sabha', items=[
        ('Members of the Lok Sabha are', 'directly elected by the people', ['nominated by the President', 'elected by state legislatures',
                                                                            'appointed by the Prime Minister'],
         'Rajya Sabha members are elected by state legislatures'),
    ]),
    S('cbse-g8-social-science:4:5', 'The Revolt of 1857', items=[
        ('The Revolt of 1857 began among sepoys at', 'Meerut', ['Delhi', 'Kolkata', 'Mumbai'], 'It started on 10 May 1857'),
        ('Which was an immediate cause of the Revolt of 1857?', 'Rumours that new rifle cartridges were greased with cow and pig fat',
         ['The partition of Bengal', 'The Jallianwala Bagh massacre', 'The Salt Satyagraha'], 'The others came decades later'),
    ]),
    S('cbse-g8-social-science:9:3', 'Gandhian movements', items=[
        ('Who led the Dandi March (Salt Satyagraha) in 1930?', 'Mahatma Gandhi', ['Jawaharlal Nehru', 'Subhas Chandra Bose', 'Bhagat Singh'],
         'Gandhi walked from Sabarmati to Dandi'),
        ('The Quit India Movement was launched in', '1942', ['1920', '1930', '1947'], 'Launched in August 1942'),
        ('Why did Gandhi choose salt as the focus of a protest?', 'Everyone used salt, so the salt tax hurt rich and poor alike and united people',
         ['Salt was expensive in Britain', 'The British had banned eating salt', "Salt was India's main export"],
         'A universal grievance built mass participation'),
    ]),
    S('cbse-g8-social-science:7:2', 'Factors of production', items=[
        ('Which of these is a factor of production?', 'Labour', ['Profit', 'Prices', 'Tax'], 'Land, labour, capital and entrepreneurship'),
        ("A farmer's tractor is an example of", 'capital', ['land', 'labour', 'entrepreneurship'], 'Capital is human-made equipment'),
        ("Why does better education and health raise a country's production?", 'It increases human capital: skilled, healthy workers produce more',
         ['It increases the amount of land', 'It reduces the number of workers', 'It raises prices'], 'Human capital is productive'),
    ]),
]

SOCIAL_CUR = [
    S('cbse-g9-social-science:1:2', 'Sources and evidence in social science', [
        ('Which is a primary source for studying the Harappan civilisation?', 'Seals excavated at Mohenjo-daro',
         ['A school textbook', 'A documentary film', 'A website article'], 'Primary sources come from the period itself'),
        ('Why do social scientists use more than one source?', 'To cross-check facts and reduce bias',
         ['Because sources are always false', 'To make reports longer', 'Because one source is not allowed'],
         'Corroboration strengthens conclusions'),
        ("A survey of only city residents is used to describe farmers' incomes. What is the main problem?",
         'The sample does not represent the group being studied',
         ['Surveys are never useful', 'City people cannot answer surveys', 'Incomes cannot be measured'],
         'Conclusions need a representative sample'),
    ]),
    S('cbse-g9-social-science:2:2', 'Plate tectonics: earthquakes and mountain building', [
        ('Most earthquakes occur', 'along plate boundaries', ['in the middle of oceans only', 'at the poles', 'where it rains most'],
         'Plates grind, collide or separate at boundaries'),
        ('The Himalayas were formed by', 'the collision of the Indian plate with the Eurasian plate',
         ['volcanic eruptions', 'river deposition', 'glacial erosion'], 'They are young fold mountains'),
        ('Why is the Himalayan region still prone to earthquakes?', 'The Indian plate is still pushing into the Eurasian plate',
         ['It has many rivers', 'It is very cold', 'It has dense forests'], 'Ongoing collision builds stress'),
    ]),
    S('cbse-g9-social-science:3:3', 'The Indian monsoon and seasons', [
        ("The south-west monsoon brings most of India's rain during", 'June to September',
         ['December to February', 'March to May', 'October to November'], 'This is the rainy season'),
        ('Why does Mawsynram in Meghalaya receive very heavy rainfall?', 'Moist winds from the Bay of Bengal are forced to rise over the Khasi Hills',
         ['It is on the Equator', 'It is in a desert', 'It is at sea level'], 'Rising air cools and releases rain (relief rainfall)'),
        ('Why does Tamil Nadu receive much of its rain in October and November?',
         'The retreating north-east monsoon picks up moisture over the Bay of Bengal',
         ['The south-west monsoon is strongest then', 'Western disturbances reach it', 'It is shielded from all monsoon winds'],
         'The Tamil Nadu coast lies in the rain shadow of the south-west monsoon'),
    ]),
    S('cbse-g9-social-science:4:3', 'Harappan Civilisation: cities, economy and trade', [
        ('Which Harappan city had the Great Bath?', 'Mohenjo-daro', ['Lothal', 'Kalibangan', 'Dholavira'], 'It is in present-day Sindh'),
        ('Lothal was an important Harappan site because it had', 'a dockyard used for trade',
         ['the Great Bath', 'a large royal palace', 'iron tools'], 'Lothal in Gujarat was a port'),
        ('Which evidence suggests that Harappan cities were planned?', 'Streets laid out in a grid and covered drains',
         ['Many large temples', 'Large royal tombs', 'Iron weapons'], 'Town planning shows central organisation'),
    ]),
]

DESIGN = {
    'designId': 'g9-cbse', 'grade': 9, 'stream': 'none', 'boards': ['cbse'],
    'title': 'CBSE Class 9 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G9, MATHS_CUR),
        G('science', 'Science', SCIENCE_PRE_G9, SCIENCE_CUR),
        G('english', 'English', ENGLISH_PRE_G9, ENGLISH_CUR),
        G('social-science', 'Social Science', SOCIAL_PRE, SOCIAL_CUR),
    ],
}
