"""Grade 8 prerequisite slots shared by all three boards (grade 7 skills are the same everywhere).

Grade 7 is not in the curriculum map, so each slot points at the grade 8 subtopic that needs the
skill and carries a prerequisiteNote. Contexts are neutral (no currency, no country) so the same
item works on every board.
"""
from dsl import S

MATHS_PRE_G8 = [
    S({'cbse': 'cbse-g8-maths:1:1', 'cambridge': 'cambridge-g8-maths:1:1', 'ib': 'ib-g8-maths:2:2'},
      'Squares of whole numbers', note='Grade 7: multiplication facts and squares of numbers', items=[
        ('Which of these numbers is a perfect square?', '196', ['250', '300', '420'],
         '14 x 14 = 196; the others are not the square of any whole number'),
    ]),
    S({'cbse': 'cbse-g8-maths:1:2', 'cambridge': 'cambridge-g8-maths:1:1', 'ib': 'ib-g8-maths:2:2'},
      'Prime factorisation', note='Grade 6-7: factors, primes and prime factorisation', items=[
        ('Which shows 36 written as a product of prime factors?', '2 x 2 x 3 x 3', ['4 x 9', '2 x 3 x 6', '6 x 6'],
         '4, 6 and 9 are not prime; 36 = 2 x 2 x 3 x 3'),
        ('The prime factorisation of 180 is', '2² x 3² x 5', ['2 x 3² x 10', '2² x 45', '2³ x 3 x 5'],
         '180 = 4 x 45 = 2 x 2 x 3 x 3 x 5'),
    ]),
    S({'cbse': 'cbse-g8-maths:2:1', 'cambridge': 'cambridge-g8-maths:1:3', 'ib': 'ib-g8-maths:2:1'},
      'Exponents as repeated multiplication', note='Grade 7: exponents and powers', items=[
        ('5⁴ means', '5 x 5 x 5 x 5', ['5 x 4', '4 x 4 x 4 x 4 x 4', '5 + 5 + 5 + 5'],
         'The exponent 4 says how many 5s are multiplied'),
        ('What is the value of 2⁵?', '32', ['10', '25', '64'], '2 x 2 x 2 x 2 x 2 = 32'),
        ('Which is greater, 3⁴ or 4³, and by how much?', '3⁴, by 17', ['4³, by 17', '3⁴, by 1', 'They are equal'],
         '3⁴ = 81 and 4³ = 64; 81 - 64 = 17'),
    ]),
    S({'cbse': 'cbse-g8-maths:3:2', 'cambridge': 'cambridge-g8-maths:8:3', 'ib': 'ib-g8-maths:1:2'},
      'Operations on integers and fractions', note='Grade 7: integers and fractions, four operations', items=[
        ('(-8) + 5 = ?', '-3', ['3', '-13', '13'], 'Start at -8 and move 5 to the right on the number line'),
        ('3/4 - 2/3 = ?', '1/12', ['1/7', '5/12', '1/4'], 'Common denominator 12: 9/12 - 8/12 = 1/12'),
        ('A jug holds 2 1/2 litres of milk. 3/4 litre is used for tea and 1 1/3 litres for a pudding. How much milk is left?',
         '5/12 litre', ['7/12 litre', '1 5/12 litres', '1/2 litre'],
         '30/12 - 9/12 - 16/12 = 5/12 litre'),
    ]),
]

SCIENCE_PRE_G8 = [
    S({'cbse': 'cbse-g8-science:12:1', 'cambridge': 'cambridge-g8-science:1:1', 'ib': 'ib-g8-science:5:3'},
      'Photosynthesis needs light', note='Grade 7: nutrition in plants (photosynthesis)', items=[
        ('A potted plant is kept in a dark cupboard for 3 days. One leaf is then tested with iodine. What do you expect, and why?',
         'No blue-black colour, because no starch was made without light',
         ['Blue-black colour, because leaves always store starch',
          'No blue-black colour, because iodine reacts only with sugar',
          'Blue-black colour, because the plant made starch from soil water'],
         'Iodine turns blue-black with starch; without light the plant uses up its starch and cannot make more'),
    ]),
    S({'cbse': 'cbse-g8-science:4:1', 'cambridge': 'cambridge-g8-science:9:1', 'ib': 'ib-g8-science:12:1'},
      'Electric circuits, conductors and insulators', note='Grade 7: electric circuits and their components', items=[
        ('In a circuit diagram, a long line drawn next to a short line stands for', 'A cell',
         ['A switch', 'A bulb', 'A wire joint'], 'The long line is the positive terminal of a cell'),
        ('A bulb does not glow when a rubber eraser closes the gap in a circuit, but glows with a steel key. This shows that',
         'steel is a conductor and rubber is an insulator',
         ['rubber is a conductor and steel is an insulator', 'both are conductors but rubber is weaker', 'the bulb is fused'],
         'Current flows through conductors such as metals, not through insulators such as rubber'),
    ]),
    S({'cbse': 'cbse-g8-science:1:3', 'cambridge': 'cambridge-g8-science:8:1', 'ib': 'ib-g8-science:1:2'},
      'Fair tests and variables', note='Grade 7: planning a fair investigation', items=[
        ('In an experiment, the factor you deliberately change is called the', 'independent variable',
         ['dependent variable', 'controlled variable', 'conclusion'], 'You change the independent variable and measure the dependent one'),
        ('A student wants to test whether salt makes ice melt faster. What must stay the same in both cups?',
         'The size of the ice cubes and the room temperature',
         ['The amount of salt', 'Only the time she checks the result', 'Nothing; any differences are fine'],
         'Only one factor (salt) should change; everything else is controlled'),
        ('A student says plants grow taller with music. He plays music to one plant on a sunny window and keeps another plant, without music, in a dark corner. What is wrong with his test?',
         'Two factors (music and light) changed, so he cannot tell which caused the difference',
         ['He should have used three plants with music', 'Plants cannot hear, so no test is needed',
          'He should measure the leaves, not the height'],
         'A fair test changes one variable at a time'),
    ]),
    S({'cbse': 'cbse-g8-science:3:1', 'cambridge': 'cambridge-g8-science:4:3', 'ib': 'ib-g8-science:3:2'},
      'Human digestion', note='Grade 7: nutrition in animals (human digestive system)', items=[
        ('Digestion of starch begins in the', 'mouth', ['stomach', 'large intestine', 'liver'],
         'Saliva contains an enzyme that starts breaking starch down'),
        ('Why is the inner wall of the small intestine covered with finger-like villi?',
         'They increase the surface area for absorbing digested food',
         ['They produce bile', 'They push food back to the stomach', 'They store undigested food'],
         'More surface means faster absorption into the blood'),
        ('A person whose gall bladder was removed is advised to eat less oily food. Which reason fits best?',
         'Bile, which breaks fat into small droplets, is no longer stored and released in large amounts',
         ['The stomach can no longer make acid', 'Fat is digested only in the gall bladder', 'Villi stop absorbing water'],
         'The gall bladder stores bile; without it less bile is available at mealtimes to emulsify fat'),
    ]),
]

ENGLISH_PRE_G8 = [
    S({'cbse': 'cbse-g8-english:1:3', 'cambridge': 'cambridge-g8-english:9:3', 'ib': 'ib-g8-english:2:1'},
      'Vocabulary in context', note='Grade 7: working out word meaning from context', items=[
        ("Read: 'The old fort looked desolate; no one had visited it in years.' What does 'desolate' most likely mean?",
         'empty and lonely', ['crowded and noisy', 'newly painted', 'very tall'],
         "'No one had visited it in years' signals emptiness"),
    ]),
    S({'cbse': 'cbse-g8-english:1:4', 'cambridge': 'cambridge-g8-english:9:1', 'ib': 'ib-g8-english:2:2'},
      'Past tenses', note='Grade 7: simple past and past continuous', items=[
        ('Choose the correct word: Yesterday, Kabir ___ his bicycle to school.', 'rode', ['rides', 'ride', 'riding'],
         "'Yesterday' needs the simple past"),
        ('Choose the correct words: When the lights went out, we ___ dinner.', 'were having',
         ['are having', 'have had', 'will have'], 'An action in progress in the past uses the past continuous'),
    ]),
    S({'cbse': 'cbse-g8-english:1:4', 'cambridge': 'cambridge-g8-english:9:1', 'ib': 'ib-g8-english:2:4'},
      'Subject-verb agreement', note='Grade 7: subject-verb agreement', items=[
        ('Choose the correct word: Each of the students ___ a library card.', 'has', ['have', 'are having', 'having'],
         "'Each' is singular"),
        ('Choose the correct word: Neither the teacher nor the students ___ aware of the change.', 'were',
         ['was', 'is', 'has been'], "With 'neither ... nor', the verb agrees with the nearer subject, 'students'"),
        ('Which sentence is correct?', 'The bunch of keys was found under the sofa.',
         ['The bunch of keys were found under the sofa.', 'The bunch of keys have found under the sofa.',
          'The bunch of keys are find under the sofa.'],
         "The subject is 'bunch' (singular), not 'keys'"),
    ]),
    S({'cbse': 'cbse-g8-english:9:2', 'cambridge': 'cambridge-g8-english:2:3', 'ib': 'ib-g8-english:2:3'},
      'Main idea of a paragraph', note='Grade 7: reading for the main idea', items=[
        ('Read: "Bees visit flowers to collect nectar. As they move, pollen sticks to their bodies and is carried to other flowers. This helps plants make seeds." What is the passage mainly about?',
         'How bees help plants make seeds', ['Why nectar is sweet', 'How honey is sold', 'Why flowers are colourful'],
         'Every sentence builds towards pollination and seeds'),
        ('Read: "Arun practised the flute every evening, even when his friends called him out to play. At the school concert, the audience stood up and clapped for a long time." What is the main message?',
         'Steady practice leads to success', ['Playing outside is a waste of time', 'Concerts are long',
                                              'Friends are not important'],
         'The practice in the first sentence explains the applause in the second'),
        ('Read: "Many cities now have car-free Sundays. Streets fill with cyclists, skaters and families. Shopkeepers first complained, but many now report more customers on foot." Which statement best sums up the passage?',
         'Car-free days, though doubted at first, benefit people and some businesses',
         ['Shopkeepers dislike car-free Sundays', 'Cycling is the best exercise', 'Cars should be banned forever'],
         'The summary must include both the early doubt and the later benefit'),
    ]),
]
