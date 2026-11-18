"""Design g9-cambridge: Cambridge IGCSE year 1 (Maths 0580, Physics 0625, Chemistry 0620, Biology 0610,
First Language English 0500, History 0470, Geography 0460). Science and humanities groups span several IGCSE subjects."""
from dsl import S, G
from content.shared_g9 import MATHS_PRE_G9, SCIENCE_PRE_G9, ENGLISH_PRE_G9

MATHS_CUR = [
    S('cambridge-g9-maths:1:1', 'Types of number', [
        ('Which of these numbers is prime?', '29', ['21', '27', '39'], '21 = 3 x 7, 27 = 3³, 39 = 3 x 13'),
        ('Which of these is both a square number and a cube number?', '64', ['16', '27', '36'], '64 = 8² = 4³'),
        ('What is the smallest square number that is a multiple of both 12 and 18?', '36', ['216', '144', '72'],
         'LCM(12, 18) = 36, which is already 6²'),
    ]),
    S('cambridge-g9-maths:1:2', 'Prime factors, HCF and LCM', [
        ('What is the HCF of 12 and 18?', '6', ['3', '36', '2'], 'The largest number dividing both'),
        ('Write 360 as a product of prime factors in index form.', '2³ x 3² x 5', ['2² x 3² x 10', '2³ x 45', '2 x 3 x 60'],
         '360 = 8 x 9 x 5'),
        ('Buses leave a station every 12 minutes and trains every 20 minutes. Both leave at 09:00. When do they next leave together?',
         '10:00', ['09:32', '09:40', '10:20'], 'LCM(12, 20) = 60 minutes'),
    ]),
    S('cambridge-g9-maths:2:3', 'Expanding brackets including products of binomials', [
        ('Expand 5(2x - 3).', '10x - 15', ['10x - 3', '7x - 15', '10x + 15'], 'Multiply each term by 5'),
        ('Expand and simplify (x - 4)(x + 6).', 'x² + 2x - 24', ['x² - 2x - 24', 'x² + 10x - 24', 'x² + 2x + 24'],
         'x² + 6x - 4x - 24'),
        ('Expand and simplify (x + 1)(x + 2)(x + 3).', 'x³ + 6x² + 11x + 6',
         ['x³ + 6x² + 6x + 6', 'x³ + 5x² + 11x + 6', 'x³ + 6x² + 11x + 5'], '(x² + 3x + 2)(x + 3)'),
    ]),
    S('cambridge-g9-maths:2:4', 'Laws of indices including fractional indices', [
        ('Simplify x⁵ ÷ x².', 'x³', ['x⁷', 'x^2.5', 'x¹⁰'], 'Subtract the indices'),
        ('Evaluate 27^(1/3).', '3', ['9', '81', '1/3'], 'The cube root of 27'),
        ('Evaluate 16^(-3/4).', '1/8', ['8', '-8', '1/12'], '16^(1/4) = 2, 2³ = 8, and the negative index gives 1/8'),
    ]),
]

SCIENCE_CUR = [
    S('cambridge-g9-physics:2:2', 'Physics: speed and distance-time graphs', [
        ('A cyclist covers 150 m in 30 s. What is her average speed?', '5 m/s', ['4500 m/s', '0.2 m/s', '120 m/s'], 'v = s / t'),
        ('On a distance-time graph, a horizontal line shows that the object is', 'stationary',
         ['moving at constant speed', 'accelerating', 'decelerating'], 'Distance is not changing'),
        ("A car's distance-time graph is a straight line from (0 s, 0 m) to (20 s, 300 m). What is its speed?", '15 m/s',
         ['6000 m/s', '0.067 m/s', '300 m/s'], 'Gradient = 300 ÷ 20'),
    ]),
    S('cambridge-g9-physics:2:3', 'Physics: acceleration and speed-time graphs', [
        ('Acceleration is', 'change in velocity ÷ time taken', ['distance ÷ time', 'force x mass', 'velocity x time'],
         'a = Δv / t'),
        ('A car speeds up from 10 m/s to 30 m/s in 4 s. What is its acceleration?', '5 m/s²', ['10 m/s²', '7.5 m/s²', '20 m/s²'],
         '(30 - 10) ÷ 4'),
        ('A speed-time graph rises steadily from 0 to 12 m/s in 6 s. How far does the object travel in that time?', '36 m',
         ['72 m', '2 m', '18 m'], 'Area of the triangle = ½ x 6 x 12'),
    ]),
    S('cambridge-g9-chemistry:2:2', 'Chemistry: proton number, mass number and isotopes', [
        ('The proton number of an atom is the number of', 'protons in its nucleus',
         ['neutrons in its nucleus', 'protons and neutrons together', 'electron shells'], 'Also called the atomic number'),
        ('An atom of sodium has proton number 11 and mass number 23. How many neutrons does it have?', '12', ['11', '23', '34'],
         '23 - 11 = 12'),
        ('Chlorine-35 and chlorine-37 are', 'isotopes: atoms with the same number of protons but different numbers of neutrons',
         ['different elements', 'ions with different charges', 'exactly the same atom'], 'Same element, different mass number'),
    ]),
    S('cambridge-g9-biology:2:1', 'Biology: animal, plant and bacterial cells', [
        ('Which structure is found in plant cells and bacterial cells but not in animal cells?', 'cell wall',
         ['nucleus', 'mitochondria', 'cell membrane'], 'Bacteria have walls but no nucleus'),
        ('Bacterial cells differ from plant and animal cells because their DNA is', 'not enclosed in a nucleus',
         ['found only in mitochondria', 'absent', 'inside chloroplasts'], 'Bacteria have a circular chromosome in the cytoplasm'),
        ('A cell has a cell wall, many chloroplasts and a large permanent vacuole. Where is it most likely from?',
         'the palisade layer of a leaf', ['a human cheek', 'a bacterium', 'a root hair'],
         'Root hair cells have no chloroplasts'),
    ]),
]

ENGLISH_CUR = [
    S('cambridge-g9-english:1:2', 'Audience, purpose and text type', [
        ('A text with headings, numbered steps and diagrams explaining how to set up a new phone is most likely',
         'an instruction manual', ['a diary entry', 'a poem', 'a short story'], 'Its purpose is to instruct'),
        ("A blog post uses informal language, jokes and the word 'you' a lot. What are its likely audience and purpose?",
         'Teenagers, to entertain and engage them', ['Lawyers, to set out a contract', 'Scientists, to report results',
                                                     'The government, to announce a law'], 'Tone and register suggest the reader'),
        ("A charity letter begins: 'Imagine walking six miles every day just to fetch water.' Why does it begin this way?",
         'To make the reader empathise and feel involved before asking for help',
         ['To give exact statistics', "To describe the writer's holiday", 'To instruct the reader how to walk'],
         'Second-person imagining draws the reader in'),
    ]),
    S('cambridge-g9-english:1:3', 'Meaning of unfamiliar vocabulary from context', [
        ("'The arid land had not seen rain for months.' 'Arid' means", 'very dry', ['very cold', 'fertile', 'flooded'],
         "'Not seen rain' is the clue"),
        ("'Despite the ominous clouds, the picnic went ahead.' 'Ominous' suggests the clouds", 'threatened bad weather',
         ['were beautiful', 'were disappearing', 'were very high'], "'Despite' signals a reason not to go ahead"),
        ("'His explanation was so convoluted that nobody could follow it.' 'Convoluted' means", 'complicated and hard to follow',
         ['short and clear', 'loud', 'untrue'], "'Nobody could follow it' is the clue"),
    ]),
    S('cambridge-g9-english:2:2', 'Implicit meaning: inferring thoughts and feelings', [
        ("'Mira slammed her books on the desk and refused to look at anyone.' How is Mira most likely feeling?", 'angry or upset',
         ['calm', 'sleepy', 'excited'], 'Actions reveal feelings'),
        ("'The house was spotless; every cushion stood to attention.' What does this suggest about the owner?",
         'They are very tidy, perhaps strict about order', ['They are lazy', 'They have just moved out', 'They have soldiers living there'],
         "'Stood to attention' suggests military neatness"),
        ("'Grandfather's chair stayed by the window, though no one sat in it any more.' What is implied?",
         'Grandfather has died or gone away, and the family keeps the chair in his memory',
         ['The chair is broken', 'Grandfather prefers the window', 'The family dislikes the chair'],
         "'No one sat in it any more' hints at absence"),
    ]),
    S('cambridge-g9-english:4:2', 'Connotations and effects of vocabulary', [
        ('Which word has the most positive connotation?', 'slim', ['skinny', 'bony', 'scrawny'], 'The others suggest unhealthiness'),
        ("A writer describes a crowd as 'a swarm'. What does this suggest?",
         'The crowd is large, fast-moving and perhaps threatening, like insects',
         ['The crowd is calm', 'The crowd is small', 'The crowd is singing'], 'Swarm brings insect associations'),
        ("Compare 'The old man shuffled' with 'The old man walked'. What does 'shuffled' add?",
         'It suggests he is frail or tired, moving slowly without lifting his feet',
         ['It shows he is in a hurry', 'It means he is dancing', 'Nothing; the two mean the same'], 'Precise verbs carry connotation'),
    ]),
]

SOCIAL_PRE = [
    S('cambridge-g8-social-science:4:1', 'Causes of the First World War', items=[
        ('Which was a long-term cause of the First World War?', 'The alliance system that divided Europe into two armed camps',
         ['The Wall Street Crash', 'The Treaty of Versailles', 'The Cold War'], 'The other three came after 1918'),
    ]),
    S('cambridge-g8-social-science:5:1', 'Structure of the Earth and plate boundaries', items=[
        ("The Earth's thin, solid outer layer is the", 'crust', ['mantle', 'outer core', 'inner core'], 'The crust floats on the mantle'),
        ('At a constructive (divergent) plate boundary, the plates', 'move apart and magma rises',
         ['collide', 'slide past each other', 'stay still'], 'New crust forms, as in the mid-Atlantic'),
    ]),
    S('cambridge-g8-social-science:3:3', 'Empire and independence movements', items=[
        ('India became independent in', '1947', ['1857', '1919', '1950'], '15 August 1947'),
        ("Gandhi's method of non-violent resistance is known as", 'satyagraha', ['blitzkrieg', 'apartheid', 'perestroika'],
         "Satyagraha means 'holding firmly to truth'"),
        ('Why did many colonies gain independence after 1945?',
         'European powers were weakened by war and nationalist movements had grown stronger',
         ['The colonies asked to become part of Europe', 'The League of Nations ordered it', 'The colonies stopped trading'],
         'Both a weaker centre and stronger demands'),
    ]),
    S('cambridge-g8-social-science:6:3', 'Reading climate graphs and climate zones', items=[
        ('On a climate graph, rainfall is usually shown as', 'bars', ['a line', 'a pie chart', 'a map'],
         'Temperature is the line; rainfall is the bars'),
        ('A place is hot all year and gets over 2000 mm of rain a year. Its climate is most likely', 'tropical rainforest',
         ['hot desert', 'polar', 'Mediterranean'], 'Hot and wet all year'),
        ('Which pattern on a climate graph suggests a Mediterranean climate?', 'Hot, dry summers and mild, wet winters',
         ['Cold all year', 'Hot and wet every month', 'No rain at all'], 'Seasonal contrast in rainfall is the key'),
    ]),
]

SOCIAL_CUR = [
    S('cambridge-g9-history:2:1', 'History: empires and alliances before 1914', [
        ('The Triple Entente was made up of', 'Britain, France and Russia',
         ['Germany, Austria-Hungary and Italy', 'Britain, Germany and Russia', 'France, Italy and Japan'],
         'Germany, Austria-Hungary and Italy formed the Triple Alliance'),
        ('Where was Archduke Franz Ferdinand assassinated in June 1914?', 'Sarajevo', ['Berlin', 'Paris', 'Vienna'],
         'Sarajevo, in Bosnia'),
        ('Explain why a local crisis in the Balkans in 1914 became a wider war.', 'The alliance system drew the great powers in one after another',
         ['Every country wanted the Balkans', 'Britain invaded Serbia', 'The League of Nations failed'],
         'Austria-Hungary, Russia, Germany, France and Britain were bound by alliances; the League did not yet exist'),
    ]),
    S('cambridge-g9-history:3:3', 'History: terms of the Treaty of Versailles', [
        ('The Treaty of Versailles was signed in', '1919', ['1914', '1918', '1923'], 'Signed on 28 June 1919'),
        ('Which was a term of the Treaty of Versailles?', "Germany's army was limited to 100 000 men",
         ['Germany gained Alsace-Lorraine', 'Germany joined the League of Nations at once', 'Germany kept all its colonies'],
         'Alsace-Lorraine went to France; Germany lost its colonies'),
        ("Why did many Germans call the treaty a 'diktat'?", 'It was imposed on Germany without negotiation',
         ['It was written in German', 'It was very short', 'Germany wrote it'], 'Diktat means a dictated peace'),
    ]),
    S('cambridge-g9-geography:1:1', 'Geography: grid references, scale and direction', [
        ('A six-figure grid reference locates a point to the nearest', '100 metres', ['1 kilometre', '10 kilometres', '1 metre'],
         'On a 1:50 000 map each grid square is 1 km, split into tenths'),
        ('On a 1 : 25 000 map, 6 cm represents', '1.5 km', ['15 km', '150 m', '6 km'], '6 x 25 000 = 150 000 cm'),
        ('On a map, contour lines that are very close together show', 'a steep slope', ['flat land', 'a river', 'a gentle slope'],
         'Height changes quickly over a short distance'),
    ]),
    S('cambridge-g9-geography:2:1', 'Geography: types of plate boundary', [
        ('At a conservative plate boundary, the plates', 'slide past each other', ['move apart', 'collide head-on', 'sink together'],
         'As on the San Andreas Fault'),
        ('Why do volcanoes form at destructive plate boundaries?', 'The denser oceanic plate is subducted and melts, and the magma rises',
         ['The plates slide past each other', 'The crust is thickest there', 'There is no friction'], 'Subduction produces magma'),
        ('Iceland has many volcanoes but few deep earthquakes. Why?', 'It sits on a constructive boundary where magma rises as plates separate',
         ['It is on a destructive boundary', 'It is near the Equator', 'It is on a conservative boundary'],
         'Constructive boundaries give shallow quakes and frequent eruptions'),
    ]),
]

DESIGN = {
    'designId': 'g9-cambridge', 'grade': 9, 'stream': 'none', 'boards': ['cambridge'],
    'title': 'Cambridge IGCSE year 1 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G9, MATHS_CUR),
        G('science', 'Sciences (Physics, Chemistry, Biology)', SCIENCE_PRE_G9, SCIENCE_CUR),
        G('english', 'English', ENGLISH_PRE_G9, ENGLISH_CUR),
        G('social-science', 'Humanities (History, Geography)', SOCIAL_PRE, SOCIAL_CUR),
    ],
}
