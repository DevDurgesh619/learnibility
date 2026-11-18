"""Design g10-cambridge: Cambridge IGCSE year 2 (Maths 0580, Physics, Chemistry, Biology, English 0500, History, Geography)."""
from dsl import S, G
from content.shared_g10 import MATHS_PRE_G10, SCIENCE_PRE_G10, ENGLISH_PRE_G10

MATHS_CUR = [
    S('cambridge-g10-maths:1:3', 'Upper and lower bounds', [
        ('A length is 8 cm, correct to the nearest cm. What is its lower bound?', '7.5 cm', ['7 cm', '7.9 cm', '8.5 cm'],
         'Half a unit below'),
        ('A mass is 2.4 kg, correct to 1 decimal place. What are its bounds?', '2.35 kg and 2.45 kg',
         ['2.3 kg and 2.5 kg', '2.39 kg and 2.41 kg', '2.4 kg and 2.5 kg'], 'Half of 0.1 either side'),
        ('A rectangle measures 6 cm by 4 cm, each to the nearest cm. What is the upper bound of its area?', '29.25 cm²',
         ['24 cm²', '30 cm²', '25.5 cm²'], '6.5 x 4.5 = 29.25'),
    ]),
    S('cambridge-g10-maths:2:2', 'Solving quadratics with the formula', [
        ('Solve x² - 9 = 0.', 'x = 3 or x = -3', ['x = 3 only', 'x = 9 or x = -9', 'x = 4.5'], 'x² = 9'),
        ('In the quadratic formula for 2x² + 3x - 5 = 0, what is the value of b² - 4ac?', '49', ['-31', '1', '29'],
         '9 - 4(2)(-5) = 9 + 40'),
        ('Solve x² - 4x - 1 = 0, giving answers to 2 decimal places.', 'x = 4.24 or x = -0.24',
         ['x = 2.24 or x = -2.24', 'x = 4.24 or x = 0.24', 'x = 5 or x = -1'], 'x = (4 ± √20) ÷ 2'),
    ]),
    S('cambridge-g10-maths:3:2', 'Right-angled trigonometry: SOH CAH TOA', [
        ('In a right-angled triangle, tan of an angle equals', 'opposite ÷ adjacent', ['adjacent ÷ hypotenuse', 'opposite ÷ hypotenuse',
                                                                                     'hypotenuse ÷ opposite'], 'TOA'),
        ('A right-angled triangle has hypotenuse 10 cm and angle 30°. How long is the side opposite the 30° angle?', '5 cm',
         ['8.66 cm', '10 cm', '17.3 cm'], 'sin 30° = 0.5, and 0.5 x 10 = 5'),
        ('A right-angled triangle has opposite side 7 cm and adjacent side 7 cm. What is the angle?', '45°',
         ['30°', '60°', '90°'], 'tan θ = 1'),
    ]),
    S('cambridge-g10-maths:3:3', 'Angles of elevation and depression', [
        ('Looking up from the ground at the top of a tower, the angle with the horizontal is the angle of', 'elevation',
         ['depression', 'reflection', 'rotation'], 'Elevation is measured upwards'),
        ('From 20 m away, the angle of elevation of the top of a tree is 45°. How tall is the tree?', '20 m',
         ['10 m', '28.3 m', '45 m'], 'tan 45° = 1'),
        ('From the top of a 50 m cliff, the angle of depression of a boat is 30°. How far is the boat from the foot of the cliff?',
         '86.6 m', ['28.9 m', '25 m', '100 m'], 'tan 30° = 50 ÷ d, so d = 50 ÷ 0.577'),
    ]),
]

SCIENCE_CUR = [
    S('cambridge-g10-physics:1:2', 'The wave equation v = fλ', [
        ('The number of waves passing a point each second is the', 'frequency', ['amplitude', 'wavelength', 'speed'],
         'Measured in hertz'),
        ('A wave has frequency 50 Hz and wavelength 4 m. What is its speed?', '200 m/s', ['12.5 m/s', '54 m/s', '0.08 m/s'],
         'v = fλ = 50 x 4'),
        ('Sound travels at 340 m/s. What is the wavelength of a 170 Hz note?', '2 m', ['0.5 m', '57 800 m', '510 m'],
         'λ = v ÷ f'),
    ]),
    S('cambridge-g10-physics:2:1', 'The electromagnetic spectrum', [
        ('Which of these is NOT part of the electromagnetic spectrum?', 'sound', ['X-rays', 'microwaves', 'visible light'],
         'Sound is a mechanical wave'),
        ('Which type of electromagnetic radiation has the shortest wavelength?', 'gamma rays', ['radio waves', 'infrared', 'ultraviolet'],
         'Gamma rays have the highest frequency'),
        ('All electromagnetic waves travel through a vacuum at', 'the same speed, about 3 x 10⁸ m/s',
         ['speeds that increase with wavelength', 'the speed of sound', 'zero speed'], 'They differ in frequency, not speed'),
    ]),
    S('cambridge-g10-chemistry:2:2', 'Group I alkali metals', [
        ('When lithium reacts with water, one product is', 'hydrogen', ['oxygen', 'chlorine', 'carbon dioxide'],
         'Metal + water → hydroxide + hydrogen'),
        ('Going down Group I, the metals become', 'more reactive', ['less reactive', 'harder', 'denser and unreactive'],
         'The outer electron is lost more easily'),
        ('Rubidium is below potassium in Group I. Predict how rubidium reacts with water.', 'Even more violently than potassium',
         ['It does not react', 'More slowly than lithium', 'Only when heated strongly'], 'Reactivity increases down the group'),
    ]),
    S('cambridge-g10-biology:1:2', 'Anaerobic respiration', [
        ('Anaerobic respiration happens', 'without oxygen', ['only in plants', 'only at night', 'with extra oxygen'],
         'An- means without'),
        ('During hard exercise, muscles respire anaerobically and produce', 'lactic acid', ['ethanol', 'glucose', 'oxygen'],
         'Ethanol is made by yeast'),
        ('Why does a sprinter keep breathing hard after finishing a race?', 'To repay the oxygen debt and break down lactic acid',
         ['To cool the lungs', 'To make more glucose', 'Because the heart has stopped'], 'Extra oxygen is needed after anaerobic respiration'),
    ]),
]

ENGLISH_CUR = [
    S('cambridge-g10-english:1:3', 'Precise vocabulary and register for audience', [
        ('Which word is the most formal way to say "get"?', 'obtain', ['grab', 'snag', 'pick up'], 'Formal register suits official writing'),
        ('Which opening suits a letter to a newspaper editor?', 'Dear Editor, I am writing to express my concern about...',
         ['Hey! Guess what happened...', 'Yo editor, listen up...', 'Dearest friend, I miss you...'],
         'Formal audience, formal register'),
        ('Which sentence uses the most precise vocabulary?', 'The toddler toppled off the swing.',
         ['The kid fell off the thing.', 'The child went down.', 'Something happened at the swing.'], 'Specific nouns and verbs'),
    ]),
    S('cambridge-g10-english:2:3', 'Form, voice and register for directed writing', [
        ('A speech to your school assembly should usually', 'address the audience directly and use a clear, engaging voice',
         ['use only bullet points', 'be written in text-message language', 'avoid any opinion'], 'Speeches speak to listeners'),
        ('You are asked to write a report for the head teacher. Which feature fits the form best?', 'Clear subheadings and a recommendation',
         ['A rhyming scheme', 'Dialogue between characters', 'Exclamations in every line'], 'Reports are organised and formal'),
        ('Writing as a resident objecting to a new road, which sentence best balances passion and register?',
         'While progress matters, this road would destroy the only park our children have.',
         ['This road is the worst idea ever, end of.', 'I suppose it does not really matter either way.',
          'Roads are made of tarmac and stone.'], 'Concede, then argue firmly in formal language'),
    ]),
    S('cambridge-g10-english:3:2', 'Sensory detail and imagery in description', [
        ('Which sentence appeals mainly to the sense of smell?', 'The scent of frying onions drifted from the stall.',
         ['The stall was painted bright red.', 'A drum boomed in the distance.', 'The pavement was rough underfoot.'],
         'Scent is smell'),
        ('Which description best shows a busy market rather than telling it?', 'Vendors shouted prices over the clatter of carts and the hiss of oil.',
         ['The market was very busy.', 'There were lots of people.', 'It was a crowded and busy market.'],
         'Specific sounds create the scene'),
        ("What does the 'zoom-in' technique do in descriptive writing?", 'It moves from a wide scene to one small, telling detail',
         ['It tells the story in reverse', 'It uses only dialogue', 'It lists every object equally'],
         'Like a camera focusing'),
    ]),
    S('cambridge-g10-english:3:4', 'Avoiding cliché and overwriting', [
        ("Which phrase is a cliché?", 'as cold as ice', ['frost furred the window', 'breath hung like smoke', 'the chill bit at her fingers'],
         'An overused comparison'),
        ('What is wrong with "The dark, gloomy, shadowy, black night was very extremely dark"?', 'It is overwritten with repeated adjectives',
         ['It has no verb', 'It is too short', 'It uses the first person'], 'Too many adjectives weaken the image'),
        ('Which revision of "It was a dark and stormy night" is most original?', 'Rain needled the streetlights and the wind rattled every gate.',
         ['It was a very dark and stormy night.', 'It was a dark night with a storm.', 'The night was dark like the dark.'],
         'Fresh verbs replace the stock phrase'),
    ]),
]

SOCIAL_PRE = [
    S('cambridge-g9-history:3:3', 'Terms of the Treaty of Versailles', [
        ('Under the Treaty of Versailles, Germany had to accept', 'blame for the war (the war guilt clause)',
         ['control of Austria', 'a larger army', 'new colonies in Africa'], 'Article 231'),
    ]),
    S('cambridge-g9-history:4:5', 'The League of Nations in the 1930s', [
        ('In 1931, which country invaded Manchuria?', 'Japan', ['Italy', 'Germany', 'Britain'], 'The Mukden Incident'),
        ("Why did the League's sanctions against Italy over Abyssinia fail?", 'Oil was not banned and the Suez Canal stayed open',
         ['Italy left Europe', 'The USA enforced them strictly', 'Abyssinia surrendered first'],
         'Britain and France feared losing Italy as an ally'),
    ]),
    S('cambridge-g9-geography:2:1', 'Types of plate boundary', [
        ('At a constructive plate boundary, the plates', 'move apart', ['collide', 'slide past each other', 'stay still'],
         'New crust forms'),
        ('Fold mountains such as the Himalayas form where', 'two continental plates collide', ['plates move apart', 'plates slide past',
                                                                                              'oceanic crust is created'],
         'Neither plate sinks, so the crust buckles'),
        ('Why are earthquakes at conservative boundaries often very damaging even without volcanoes?',
         'Plates lock and then slip suddenly, releasing large amounts of energy near the surface',
         ['Magma erupts there', 'The plates move very slowly all the time with no friction', 'They only occur under oceans'],
         'Built-up stress is released suddenly'),
    ]),
    S('cambridge-g9-geography:3:3', 'River landforms', [
        ('A waterfall forms where', 'a river flows over a band of hard rock lying on softer rock',
         ['a river meets the sea', 'a river deposits sand', 'a river freezes'], 'Soft rock erodes faster, undercutting the hard rock'),
        ('An ox-bow lake forms when', 'a meander neck is cut through and the old loop is sealed off',
         ['a glacier melts', 'a delta grows', 'a waterfall retreats'], 'Erosion on outer bends narrows the neck'),
        ('Why does a delta form at a river mouth?', 'The river slows on entering the sea and deposits its load faster than tides remove it',
         ['The river speeds up and erodes', 'Waves carry sand inland', 'The river flows over hard rock'],
         'Loss of energy causes deposition'),
    ]),
]

SOCIAL_CUR = [
    S('cambridge-g10-history:1:2', 'Stalemate on the Western Front', [
        ('Most fighting on the Western Front took place from', 'trenches', ['castles', 'aircraft carriers', 'mountain forts'],
         'A line of trenches ran from the Channel to Switzerland'),
        ('Why was it so hard to break through enemy lines?', 'Machine guns, barbed wire and artillery favoured the defenders',
         ['Soldiers refused to attack', 'There were no weapons', 'The weather was always perfect'], 'Defence was stronger than attack'),
        ('What was the main aim of the Battle of the Somme in 1916?', 'To relieve pressure on the French at Verdun and wear down German forces',
         ['To invade Britain', 'To capture Moscow', 'To end the war at sea'], 'It was planned partly to help Verdun'),
    ]),
    S('cambridge-g10-history:2:1', 'The Weimar Republic and its early crises', [
        ('The Weimar Republic was set up in Germany in', '1919', ['1933', '1914', '1945'], 'After the Kaiser abdicated'),
        ('Why was Article 48 of the Weimar Constitution a weakness?', 'It let the President rule by decree in an emergency',
         ['It banned elections', 'It gave the Kaiser power', 'It made Germany a monarchy'], 'Democracy could be bypassed'),
        ('Why did hyperinflation in 1923 damage support for the Republic?', 'Savings became worthless, especially for the middle classes',
         ['Prices fell sharply', 'Germany won new colonies', 'Wages became too valuable'], 'People blamed the government'),
    ]),
    S('cambridge-g10-geography:1:2', 'Population pyramids and dependency', [
        ('A population pyramid with a wide base shows', 'a high birth rate', ['a low birth rate', 'an ageing population', 'high life expectancy'],
         'Many young children'),
        ('Which group is counted as dependent in the dependency ratio?', 'children under 15 and people over 64',
         ['people aged 15 to 64', 'only unemployed adults', 'only migrants'], 'They depend on the working age group'),
        ('A country\'s pyramid narrows at the base and widens at the top. What challenge is it most likely to face?',
         'Paying for care and pensions for a growing elderly population',
         ['Building many new primary schools', 'Too many young workers', 'A rapidly rising birth rate'], 'Ageing population'),
    ]),
    S('cambridge-g10-geography:2:3', 'Rapid urbanisation and informal settlements', [
        ('Urbanisation means', 'an increasing proportion of people living in towns and cities',
         ['people moving to the countryside', 'building farms', 'the growth of forests'], 'A shift from rural to urban'),
        ('Which is a main push factor driving rural-to-urban migration in LICs?', 'Lack of jobs and services in rural areas',
         ['Better schools in villages', 'Cheaper housing in cities', 'Lower city wages'], 'Push factors drive people away'),
        ('Why do informal settlements often grow on steep slopes or flood plains?', 'The land is unused and unwanted, so migrants can build there',
         ['It is the safest land', 'The government reserves it for housing', 'It has the best water supply'],
         'Marginal land is the only space available'),
    ]),
]

DESIGN = {
    'designId': 'g10-cambridge', 'grade': 10, 'stream': 'none', 'boards': ['cambridge'],
    'title': 'Cambridge IGCSE year 2 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G10, MATHS_CUR),
        G('science', 'Sciences (Physics, Chemistry, Biology)', SCIENCE_PRE_G10, SCIENCE_CUR),
        G('english', 'English', ENGLISH_PRE_G10, ENGLISH_CUR),
        G('social-science', 'Humanities (History, Geography)', SOCIAL_PRE, SOCIAL_CUR),
    ],
}
