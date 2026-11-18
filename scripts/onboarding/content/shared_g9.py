"""Grade 9 prerequisite slots (grade 8 skills) shared by all three boards; refs point at each board's grade 8 map."""
from dsl import S

MATHS_PRE_G9 = [
    S({'cbse': 'cbse-g8-maths:13:3', 'cambridge': 'cambridge-g8-maths:4:1', 'ib': 'ib-g8-maths:5:2'},
      'Linear equations with unknowns on both sides', items=[
        ('Solve 5x - 7 = 3x + 9.', '8', ['1', '16', '-8'], '2x = 16'),
    ]),
    S({'cbse': 'cbse-g8-maths:9:2', 'cambridge': 'cambridge-g8-maths:5:4', 'ib': 'ib-g8-maths:8:1'},
      "Pythagoras' theorem", items=[
        ('A right-angled triangle has shorter sides 6 cm and 8 cm. How long is the hypotenuse?', '10 cm',
         ['14 cm', '48 cm', '100 cm'], '6² + 8² = 100, and √100 = 10'),
        ('A 13 m ladder leans against a wall with its foot 5 m from the wall. How high up the wall does it reach?', '12 m',
         ['8 m', '18 m', '14 m'], '13² - 5² = 144, and √144 = 12'),
    ]),
    S({'cbse': 'cbse-g8-maths:13:1', 'cambridge': 'cambridge-g8-maths:2:3', 'ib': 'ib-g8-maths:4:2'},
      'Simplifying and expanding expressions; identities', items=[
        ('Simplify 4a + 3b - a + 2b.', '3a + 5b', ['5a + 5b', '3a + b', '8ab'], 'Collect like terms'),
        ('Expand (a + b)².', 'a² + 2ab + b²', ['a² + b²', '2a + 2b', 'a² + ab + b²'], '(a + b)(a + b) = a² + ab + ab + b²'),
        ('Use an identity to work out 102 x 98.', '9996', ['10004', '9604', '9984'], '(100 + 2)(100 - 2) = 100² - 2² = 9996'),
    ]),
    S({'cbse': 'cbse-g8-maths:10:1', 'cambridge': 'cambridge-g8-maths:3:3', 'ib': 'ib-g8-maths:3:1'},
      'Percentages and percentage change', items=[
        ('Write 3/5 as a percentage.', '60%', ['35%', '53%', '6%'], '3/5 = 0.6 = 60%'),
        ('A price rises from 12 000 to 13 800. What is the percentage increase?', '15%', ['18%', '13.8%', '1.5%'],
         'Increase 1 800 ÷ 12 000 = 0.15'),
        ('After a 25% discount a book costs 450. What was the original price?', '600', ['562.5', '337.5', '475'],
         '450 is 75% of the original, and 450 ÷ 0.75 = 600'),
    ]),
]

SCIENCE_PRE_G9 = [
    S({'cbse': 'cbse-g8-science:7:1', 'cambridge': 'cambridge-g8-science:3:2', 'ib': 'ib-g8-science:6:4'},
      'Particles and diffusion', items=[
        ('Why does the smell of perfume spread across a still room?', 'Its particles diffuse, moving randomly from high to low concentration',
         ['Air pushes the perfume in one direction', 'The particles grow larger', 'Perfume is lighter than air, so it only rises'],
         'Random particle motion spreads the perfume out'),
    ]),
    S({'cbse': 'cbse-g8-science:8:2', 'cambridge': 'cambridge-g8-science:2:1', 'ib': 'ib-g8-science:7:3'},
      'Elements, compounds and mixtures', items=[
        ('Which of these is a compound?', 'water', ['oxygen', 'iron', 'air'], 'Water is hydrogen and oxygen chemically joined; air is a mixture'),
        ('Which statement about a mixture of iron filings and sulfur powder is true?', 'The iron can be separated with a magnet',
         ['It has a fixed formula', 'It is a new substance', 'It cannot be separated physically'],
         'In a mixture each substance keeps its own properties'),
    ]),
    S({'cbse': 'cbse-g8-science:6:1', 'cambridge': 'cambridge-g8-science:3:1', 'ib': 'ib-g8-science:10:5'},
      'Pressure as force per unit area', items=[
        ('Pressure is', 'force per unit area', ['mass per unit volume', 'force x distance', 'energy per second'], 'p = F / A'),
        ('Why is it easier to cut with a sharp knife than a blunt one?', 'The sharp edge has a smaller area, so the same force gives more pressure',
         ['The sharp knife is heavier', 'Blunt knives only have more friction', 'Sharp knives push with more force by themselves'],
         'Smaller area, larger pressure'),
        ('A box weighing 600 N rests on a base of area 0.5 m². What pressure does it exert on the floor?', '1200 Pa',
         ['300 Pa', '600 Pa', '0.0008 Pa'], '600 ÷ 0.5 = 1200 N/m²'),
    ]),
    S({'cbse': 'cbse-g8-science:2:2', 'cambridge': 'cambridge-g8-science:7:1', 'ib': 'ib-g8-science:2:2'},
      'Cell structure: plant and animal cells', items=[
        ('Which part of a cell controls its activities?', 'nucleus', ['cell membrane', 'cytoplasm', 'cell wall'],
         'The nucleus holds the genetic instructions'),
        ('Onion peel cells and cheek cells are viewed under a microscope. Which difference will you see?',
         'Onion cells have a cell wall and a regular shape; cheek cells do not',
         ['Cheek cells have chloroplasts', 'Onion cells have no nucleus', 'Cheek cells have a large central vacuole'],
         'Only plant cells have cell walls'),
        ('A cell placed in pure water swells but does not burst. Which cell is it most likely to be?',
         'A plant cell, because its cell wall resists bursting',
         ['An animal cell, because it has a cell membrane', 'A red blood cell', 'Any cell, since water never enters cells'],
         'Animal cells without a wall can burst in pure water'),
    ]),
]

ENGLISH_PRE_G9 = [
    S({'cbse': 'cbse-g8-english:7:4', 'cambridge': 'cambridge-g8-english:9:3', 'ib': 'ib-g8-english:6:1'},
      'Modals for deduction', items=[
        ('The ground is wet and people are carrying umbrellas. It ___ have rained.', 'must',
         ["can't", "shouldn't", "needn't"], "'Must have' expresses a confident deduction"),
    ]),
    S({'cbse': 'cbse-g8-english:3:4', 'cambridge': 'cambridge-g8-english:9:2', 'ib': 'ib-g8-english:5:2'},
      'Direct and indirect speech', items=[
        ('Which sentence is punctuated correctly as direct speech?', '"Close the window," said Mother.',
         ['Close the window, said Mother.', '"Close the window" said, Mother.', '"Close the window, said Mother."'],
         'Only the spoken words go inside the quotation marks, followed by a comma'),
        ("Change to indirect speech: She said, 'I will call you tomorrow.'", 'She said that she would call me the next day.',
         ['She said that I will call you tomorrow.', 'She said she will called me tomorrow.',
          'She told that she would calls me the next day.'], "'Will' becomes 'would', 'tomorrow' becomes 'the next day'"),
    ]),
    S({'cbse': 'cbse-g8-english:9:2', 'cambridge': 'cambridge-g8-english:2:3', 'ib': 'ib-g8-english:2:3'},
      'Summarising main points', items=[
        ('Which is the best title for a paragraph about saving water by fixing leaks, using buckets and reusing water?',
         'Simple Ways to Save Water', ['Water Is Wet', 'The History of Buckets', 'Rain in the Monsoon'],
         'A title should cover the main idea of the whole paragraph'),
        ('Read: "Mangroves grow along tropical coasts. Their tangled roots hold soil in place, slow down storm waves and shelter young fish. Many mangrove forests are being cleared for farms and buildings." Which summary is best?',
         'Mangroves protect coasts and wildlife but are being cleared', ['Mangroves have tangled roots', 'Fish live in the sea',
                                                                       'Farms are more important than mangroves'],
         'A summary keeps the main points and leaves out detail'),
        ('Which sentence would NOT belong in a summary of a text explaining how vaccines work?',
         'My cousin was scared of injections when he was little.',
         ['Vaccines train the immune system to recognise germs.', 'This prepares the body to fight infection quickly.',
          'Vaccination has reduced many diseases.'], 'Personal anecdotes are not main points'),
    ]),
    S({'cbse': 'cbse-g8-english:2:2', 'cambridge': 'cambridge-g8-english:3:2', 'ib': 'ib-g8-english:3:2'},
      'Figurative language and sound devices', items=[
        ("'Silent sea, softly sighing' mainly uses", 'alliteration', ['simile', 'metaphor', 'onomatopoeia'],
         "The repeated 's' sound"),
        ("'I have told you a million times!' is an example of", 'hyperbole', ['personification', 'simile', 'understatement'],
         'Deliberate exaggeration for effect'),
        ("What is the effect of the simile in 'Her words were as sharp as broken glass'?", 'It shows her words were hurtful',
         ['It shows she spoke clearly', 'It shows she made glass', 'It shows she spoke softly'],
         'Broken glass cuts, so the words wounded'),
    ]),
]
