"""Design g10-cbse: CBSE Class 10 (NCERT Mathematics, Science, First Flight, India and the Contemporary World II)."""
from dsl import S, G
from content.shared_g10 import MATHS_PRE_G10, SCIENCE_PRE_G10, ENGLISH_PRE_G10

MATHS_CUR = [
    S('cbse-g10-maths:1:2', 'HCF and LCM by prime factorisation', [
        ('What is the HCF of 12 and 18?', '6', ['36', '3', '2'], '12 = 2² x 3 and 18 = 2 x 3², so HCF = 2 x 3'),
        ('The HCF of two numbers is 6 and their LCM is 72. One number is 18. What is the other?', '24', ['12', '36', '432'],
         'HCF x LCM = product, so 6 x 72 ÷ 18 = 24'),
        ('Two bells ring every 12 and 20 minutes. They ring together at 9:00. When do they next ring together?', '10:00',
         ['9:32', '9:04', '13:00'], 'LCM(12, 20) = 60 minutes'),
    ]),
    S('cbse-g10-maths:1:4', 'Proving numbers irrational', [
        ('Which of these numbers is irrational?', '√3', ['√49', '0.75', '7/3'], '3 is not a perfect square'),
        ('If √2 is irrational, which of these must also be irrational?', '5 + √2', ['√2 - √2', '√2 x √2', '(√2)⁴'],
         'Rational + irrational is irrational; the others equal 0, 2 and 4'),
        ('To prove √5 is irrational, we assume √5 = a/b in lowest terms. Which step follows?', '5b² = a², so 5 divides a',
         ['a = b, so √5 = 1', 'a and b must both be even', '√5 is a terminating decimal'],
         'Squaring gives a² = 5b², leading to a contradiction'),
    ]),
    S('cbse-g10-maths:2:3', 'Zeroes and coefficients of a quadratic polynomial', [
        ('What are the zeroes of x² - 5x + 6?', '2 and 3', ['-2 and -3', '1 and 6', '5 and 6'], '(x - 2)(x - 3)'),
        ('For x² - 7x + 10, what is the sum of the zeroes?', '7', ['-7', '10', '-10'], 'Sum = -b/a = 7'),
        ('Which quadratic polynomial has zeroes whose sum is 4 and product is -5?', 'x² - 4x - 5',
         ['x² + 4x - 5', 'x² - 5x + 4', 'x² + 4x + 5'], 'x² - (sum)x + product'),
    ]),
    S('cbse-g10-maths:3:4', 'Solving a pair of linear equations by elimination', [
        ('Solve x + y = 10 and x - y = 2.', 'x = 6, y = 4', ['x = 4, y = 6', 'x = 8, y = 2', 'x = 5, y = 5'],
         'Adding gives 2x = 12'),
        ('Solve 2x + 3y = 13 and x + 3y = 8.', 'x = 5, y = 1', ['x = 1, y = 5', 'x = 2, y = 3', 'x = 3, y = 2'],
         'Subtracting gives x = 5'),
        ('Two pens and three notebooks cost 110. Four pens and one notebook cost 70. What does one notebook cost?', '30',
         ['10', '20', '35'], 'Double the first: 4p + 6n = 220; subtract to get 5n = 150'),
    ]),
]

SCIENCE_CUR = [
    S('cbse-g10-science:1:2', 'Writing and balancing chemical equations', [
        ('In a chemical equation, the substances on the left of the arrow are the', 'reactants',
         ['products', 'catalysts', 'precipitates'], 'Reactants change into products'),
        ('Balance: Mg + O₂ → MgO', '2Mg + O₂ → 2MgO', ['Mg + O₂ → MgO₂', 'Mg + 2O₂ → 2MgO', '2Mg + 2O₂ → 2MgO'],
         'Two O atoms on the left need two MgO on the right'),
        ('What does the symbol (aq) mean in NaCl(aq)?', 'Dissolved in water', ['A solid', 'A gas', 'A pure liquid'],
         'Aqueous means in water solution'),
    ]),
    S('cbse-g10-science:1:3', 'Types of chemical reactions', [
        ('CaO + H₂O → Ca(OH)₂ is a', 'combination reaction', ['decomposition reaction', 'displacement reaction', 'double displacement reaction'],
         'Two substances join to make one'),
        ('An iron nail placed in copper sulfate solution turns brown and the blue colour fades. What type of reaction is this?',
         'Displacement', ['Combination', 'Decomposition', 'Neutralisation only'], 'Iron is more reactive and displaces copper'),
        ('Silver chloride turns grey in sunlight. Which type of reaction is this?', 'Photolytic decomposition',
         ['Thermal decomposition', 'Combination', 'Double displacement'], 'Light breaks AgCl into silver and chlorine'),
    ]),
    S('cbse-g10-science:2:3', 'The pH scale', [
        ('A solution with pH 2 is', 'strongly acidic', ['neutral', 'weakly basic', 'strongly basic'], 'pH below 7 is acidic'),
        ('Why does an antacid relieve acidity in the stomach?', 'It is a mild base that neutralises excess acid',
         ['It is an acid that adds to the stomach acid', 'It kills all bacteria', 'It raises body temperature'],
         'Bases neutralise acids'),
        ('Tooth decay starts when the pH in the mouth falls below about 5.5. Why does this happen after eating sugary food?',
         'Bacteria break down sugar and produce acids', ['Sugar is a strong base', 'Sugar dissolves tooth enamel directly',
                                                        'Saliva becomes acidic by itself'], 'Acid attacks the enamel'),
    ]),
    S('cbse-g10-science:3:2', 'The reactivity series of metals', [
        ('Which metal reacts most vigorously with cold water?', 'potassium', ['copper', 'iron', 'gold'],
         'Potassium is at the top of the series'),
        ('Why is gold used in jewellery?', 'It is very unreactive and does not tarnish', ['It reacts quickly with air', 'It is the hardest metal',
                                                                                         'It is cheap'], 'Gold is at the bottom of the series'),
        ('Zinc is added to copper sulfate solution and copper is added to zinc sulfate solution. What happens?',
         'Only the first mixture reacts', ['Only the second mixture reacts', 'Both react', 'Neither reacts'],
         'Zinc is more reactive than copper and displaces it'),
    ]),
]

ENGLISH_CUR = [
    S('cbse-g10-english:1:2', 'A Letter to God: faith and irony', [
        ('Why did Lencho write a letter to God?', 'A hailstorm had destroyed his crop and he needed money',
         ['He wanted to thank God for rain', 'He wanted to complain about the postmaster', 'He wished to sell his land'],
         'He had faith that God would help'),
        ('Why did the postmaster send Lencho money?', 'He did not want to shake Lencho\'s faith in God',
         ['God told him to', 'Lencho owed him money', 'He wanted to keep the letter'], 'He was moved by Lencho\'s faith'),
        ('What is ironic about the end of the story?', 'Lencho thanks God but calls the post office employees crooks',
         ['Lencho never receives any money', 'The postmaster asks Lencho for money', 'The hailstorm returns'],
         'He suspects the very people who helped him'),
    ]),
    S('cbse-g10-english:1:3', 'Tenses and sequence of tenses', [
        ('Choose the correct form: Lencho ___ the field every morning.', 'checks', ['check', 'checking', 'have checked'],
         'Simple present with a singular subject'),
        ('Choose the correct form: By the time the rain stopped, the hail ___ the crop.', 'had destroyed',
         ['destroys', 'has destroyed', 'will destroy'], 'Past perfect for the earlier of two past actions'),
        ('Find the error: "He said that he will write to God the next day."', "'will' should be 'would'",
         ["'said' should be 'says'", "'write' should be 'wrote'", "'next' should be 'last'"], 'Reported past needs would'),
    ]),
    S('cbse-g10-english:2:2', 'Dust of Snow: symbolism and change of mood', [
        ('In Dust of Snow, what falls on the poet?', 'dust of snow from a hemlock tree', ['a hemlock leaf', 'rain from a cloud', 'a feather'],
         'A crow shakes it down'),
        ('The crow and the hemlock usually suggest', 'gloom and sorrow', ['joy and celebration', 'wealth and power', 'spring and growth'],
         'Frost uses unusual symbols of sadness'),
        ("What is the poem's central message?", 'A small moment of nature can change a bad mood',
         ['Crows are dangerous', 'Winter is the best season', 'Hemlock trees are poisonous'],
         "The day is 'saved' from regret"),
    ]),
    S('cbse-g10-english:3:2', 'Fire and Ice: symbolism and understatement', [
        ("In 'Fire and Ice', fire stands for", 'desire', ['hatred', 'warmth', 'happiness'], 'Fire is linked to desire'),
        ('What does ice symbolise in the poem?', 'hatred', ['peace', 'cold weather', 'purity'],
         'Ice stands for cold, indifferent hatred'),
        ("When Frost says ice 'would suffice' to destroy the world, the line is an example of", 'understatement',
         ['hyperbole', 'simile', 'onomatopoeia'], 'Destruction of the world is described in a calm, mild word'),
    ]),
]

SOCIAL_PRE = [
    S('cbse-g9-social-science:6:1', 'Features of democracy', [
        ('In a democracy, the final decision-making power rests with', 'representatives elected by the people',
         ['the army', 'one family', 'religious leaders only'], 'Rule by the people through elected representatives'),
    ]),
    S('cbse-g9-social-science:7:3', 'Election Commission and free and fair elections', [
        ('Who conducts elections to the Lok Sabha in India?', 'the Election Commission', ['the Prime Minister', 'the Supreme Court', 'the President alone'],
         'An independent constitutional body'),
        ('Why is the Model Code of Conduct important during elections?', 'It sets rules so that parties and candidates compete fairly',
         ['It decides who wins', 'It lets the ruling party campaign longer', 'It bans voting by young people'],
         'It prevents misuse of power during campaigns'),
    ]),
    S('cbse-g9-social-science:9:1', 'Demand: how buyers respond to price', [
        ('When the price of a good rises, other things staying the same, the quantity demanded usually', 'falls',
         ['rises', 'stays the same', 'doubles'], 'The law of demand'),
        ('Which of these would increase the demand for umbrellas?', 'The start of the monsoon', ['A fall in rainfall', 'A rise in umbrella prices',
                                                                                                 'A new tax on umbrellas'], 'A change in need shifts demand'),
        ('Petrol prices rise sharply. What is likely to happen to the demand for electric scooters?', 'It rises, because they are a substitute',
         ['It falls, because they are a complement', 'It is unaffected', 'It falls to zero'], 'Buyers switch to substitutes'),
    ]),
    S('cbse-g9-social-science:9:3', 'Market price: demand meets supply', [
        ('The price at which the quantity demanded equals the quantity supplied is the', 'market (equilibrium) price',
         ['maximum price', 'cost price', 'subsidy'], 'Demand and supply meet'),
        ('If the price is above the equilibrium, there will be a', 'surplus', ['shortage', 'balance', 'demand rise'],
         'Sellers offer more than buyers want'),
        ('A bad harvest cuts the supply of onions. What happens to the market price and quantity sold?', 'Price rises and quantity falls',
         ['Price falls and quantity rises', 'Both rise', 'Both stay the same'], 'Supply shifts left'),
    ]),
]

SOCIAL_CUR = [
    S('cbse-g10-social-science:1:3', 'Unification of Germany and Italy', [
        ('Who led the unification of Germany?', 'Otto von Bismarck', ['Giuseppe Garibaldi', 'Napoleon', 'Count Cavour'],
         'The Prussian chief minister'),
        ("Garibaldi's Red Shirts helped unify Italy by", 'conquering the Kingdom of the Two Sicilies in the south',
         ['defeating Prussia', 'writing the Napoleonic Code', 'ruling Austria'], 'They marched through southern Italy in 1860'),
        ("Bismarck's policy of 'blood and iron' meant that Germany was unified mainly through", 'wars led by Prussia',
         ['peaceful elections', 'a liberal revolution of the people', 'a treaty with Britain'],
         'Wars with Denmark, Austria and France'),
    ]),
    S('cbse-g10-social-science:2:1', 'Rowlatt Act, Jallianwala Bagh and satyagraha', [
        ("Gandhiji's method of mass agitation based on truth and non-violence is called", 'satyagraha',
         ['swaraj', 'swadeshi', 'boycott'], 'The power of truth'),
        ('The Rowlatt Act of 1919 was opposed because it', 'allowed political prisoners to be detained without trial',
         ['gave Indians the vote', 'abolished salt tax', 'granted dominion status'], 'It gave the government sweeping powers'),
        ('Why did the Jallianwala Bagh massacre turn many moderates against British rule?',
         'It showed the government would use brutal force against peaceful crowds',
         ['It ended the First World War', 'It was ordered by Indian leaders', 'It led to the Salt March the next day'],
         'General Dyer fired on an unarmed gathering'),
    ]),
    S('cbse-g10-social-science:2:3', 'Civil Disobedience and the Salt March', [
        ('The Salt March of 1930 ended at', 'Dandi', ['Champaran', 'Chauri Chaura', 'Amritsar'], 'Gandhiji walked from Sabarmati to Dandi'),
        ('Why did Gandhiji choose salt as the symbol of protest?', 'Salt was used by rich and poor alike, so the tax hurt everyone',
         ['Salt was only used by the British', 'Salt was a luxury good', 'Salt was made only in Britain'],
         'It united all sections of society'),
        ('How did the Civil Disobedience Movement differ from Non-Cooperation?', 'People were asked to break colonial laws, not just refuse to cooperate',
         ['It used violence', 'It was limited to students', 'It accepted British rule'],
         'Breaking the salt law was a direct challenge'),
    ]),
    S('cbse-g10-social-science:3:3', 'The Great Depression and India', [
        ('The Great Depression began around', '1929', ['1914', '1947', '1857'], 'With the Wall Street crash'),
        ('How did the Great Depression affect Indian farmers?', 'Crop prices fell sharply but land revenue demands stayed high',
         ['Crop prices doubled', 'Taxes were abolished', 'Exports of wheat rose sharply'],
         'Peasants fell into debt'),
        ('Why did the Depression help build support for the Civil Disobedience Movement in the countryside?',
         'Distressed peasants were angry about high revenue at a time of low prices',
         ['Farmers became richer and wanted more', 'Factories in India closed for good', 'The British cut all taxes'],
         'Economic hardship fed political protest'),
    ]),
]

DESIGN = {
    'designId': 'g10-cbse', 'grade': 10, 'stream': 'none', 'boards': ['cbse'],
    'title': 'CBSE Class 10 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G10, MATHS_CUR),
        G('science', 'Science', SCIENCE_PRE_G10, SCIENCE_CUR),
        G('english', 'English', ENGLISH_PRE_G10, ENGLISH_CUR),
        G('social-science', 'Social Science', SOCIAL_PRE, SOCIAL_CUR),
    ],
}
