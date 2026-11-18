"""Design g10-ib: IB MYP Year 5 (Mathematics, Sciences, Language and Literature, Individuals and Societies)."""
from dsl import S, G
from content.shared_g10 import MATHS_PRE_G10, SCIENCE_PRE_G10, ENGLISH_PRE_G10

MATHS_CUR = [
    S('ib-g10-maths:1:2', 'Rational exponents and surds', [
        ('What is 9^(1/2)?', '3', ['4.5', '81', '1/3'], 'A power of ½ is a square root'),
        ('Simplify √50.', '5√2', ['25√2', '2√5', '10√5'], '√50 = √25 x √2'),
        ('What is 8^(2/3)?', '4', ['16/3', '2', '64'], 'Cube root of 8 is 2, then square it'),
    ]),
    S('ib-g10-maths:2:1', 'Arithmetic sequences', [
        ('What is the next term of 5, 9, 13, 17, ...?', '21', ['20', '22', '25'], 'The common difference is 4'),
        ('An arithmetic sequence starts 3, 8, 13, ... What is the 20th term?', '98', ['100', '103', '63'],
         'u₂₀ = 3 + 19 x 5'),
        ('What is the sum of the first 10 terms of 2, 5, 8, ...?', '155', ['29', '145', '290'],
         'S = 10/2 x (2 x 2 + 9 x 3) = 5 x 31'),
    ]),
    S('ib-g10-maths:2:3', 'Compound interest and depreciation', [
        ('1000 is invested at 10% compound interest per year. What is it worth after 2 years?', '1210', ['1200', '1100', '1221'],
         '1000 x 1.1²'),
        ('A phone worth 20 000 loses 20% of its value each year. What is it worth after 2 years?', '12 800',
         ['12 000', '16 000', '8 000'], '20 000 x 0.8²'),
        ('Which grows faster over 10 years: 5% simple interest or 5% compound interest on the same amount?',
         'Compound, because interest is earned on earlier interest',
         ['Simple, because it is added every year', 'They are always equal', 'Simple, because the rate is fixed'],
         'Compound growth multiplies'),
    ]),
    S('ib-g10-maths:3:2', 'Solving quadratic equations and the discriminant', [
        ('Solve (x - 4)(x + 1) = 0.', 'x = 4 or x = -1', ['x = -4 or x = 1', 'x = 4 only', 'x = 3'], 'Set each bracket to zero'),
        ('How many real solutions does x² + 2x + 5 = 0 have?', 'none', ['one', 'two', 'infinitely many'],
         'Discriminant 4 - 20 = -16 < 0'),
        ('For what value of k does x² - 6x + k = 0 have exactly one solution?', '9', ['6', '36', '3'],
         'Discriminant 36 - 4k = 0'),
    ]),
]

SCIENCE_CUR = [
    S('ib-g10-science:1:2', 'Natural selection', [
        ('Natural selection depends on', 'variation within a population', ['all individuals being identical', 'animals choosing to change',
                                                                            'parents passing on scars'], 'Without variation there is nothing to select'),
        ('Why are individuals with useful variations more likely to pass them on?', 'They are more likely to survive and reproduce',
         ['They live in larger groups', 'They decide to have more offspring', 'They mutate on purpose'], 'Survival of the fittest'),
        ("Peppered moths became mostly dark in industrial areas of 19th-century England. What best explains this?",
         'Dark moths were better camouflaged on sooty trees, so fewer were eaten by birds',
         ['Soot dyed the moths', 'The moths chose to turn dark', 'Light moths migrated to cities'], 'Selection by predation'),
    ]),
    S('ib-g10-science:1:5', 'Antibiotic resistance', [
        ('Antibiotics are used to treat infections caused by', 'bacteria', ['viruses', 'all diseases', 'allergies'],
         'They do not work on viruses'),
        ('Why should a patient finish a full course of antibiotics?', 'To kill all the bacteria so resistant ones do not survive and spread',
         ['To make the medicine taste better', 'To build immunity to antibiotics', 'Because it cures viruses'],
         'Stopping early leaves the toughest bacteria'),
        ('MRSA is a strain of bacteria resistant to many antibiotics. How did it most likely arise?',
         'Random mutations gave some bacteria resistance, and antibiotic use selected them',
         ['Bacteria learned to resist on purpose', 'Antibiotics made bacteria grow larger', 'Patients became resistant'],
         'Natural selection in action'),
    ]),
    S('ib-g10-science:2:2', 'Energy flow and ecological pyramids', [
        ('In a food chain, plants are', 'producers', ['primary consumers', 'decomposers', 'predators'], 'They make food by photosynthesis'),
        ('Why are food chains rarely longer than five links?', 'Energy is lost at each trophic level, mostly as heat',
         ['Animals stop eating', 'Plants run out of sunlight', 'Predators are too small'], 'Only about 10% passes on'),
        ('A field has 10 000 kJ of energy in its grass. About how much reaches the secondary consumers?', '100 kJ',
         ['1 000 kJ', '5 000 kJ', '10 kJ'], 'About 10% per step, twice'),
    ]),
    S('ib-g10-science:2:3', 'The carbon cycle', [
        ('Which process removes carbon dioxide from the air?', 'photosynthesis', ['respiration', 'combustion', 'decay'],
         'Plants take in CO₂'),
        ('How do decomposers return carbon to the atmosphere?', 'They respire as they break down dead matter, releasing CO₂',
         ['They photosynthesise', 'They store it as fossil fuels instantly', 'They absorb it from the soil'],
         'Decay is respiration by microbes'),
        ('Why does large-scale deforestation increase atmospheric CO₂?', 'Fewer trees remove CO₂, and burning or decay of the trees releases it',
         ['Trees produce CO₂ in daylight', 'Soil absorbs more CO₂', 'Animals breathe less'], 'Two effects add up'),
    ]),
]

ENGLISH_CUR = [
    S('ib-g10-english:1:1', 'Ethos, pathos and logos', [
        ('An appeal to the audience\'s emotions is called', 'pathos', ['ethos', 'logos', 'kairos'], 'Pathos is emotion'),
        ("'As a doctor for twenty years, I have seen the harm smoking does.' Which appeal is this?", 'ethos',
         ['pathos', 'logos', 'hyperbole'], 'It builds the speaker\'s credibility'),
        ("A speaker says: 'Ninety per cent of plastic is never recycled. Picture a sea turtle tangled in it.' Which appeals are combined?",
         'logos then pathos', ['ethos then logos', 'pathos then ethos', 'logos only'], 'A statistic, then an emotional image'),
    ]),
    S('ib-g10-english:1:2', 'Rhetorical devices and their effects', [
        ("'We will fight, we will endure, we will win' uses", 'tricolon (a rule of three)', ['antithesis', 'onomatopoeia', 'simile'],
         'Three parallel parts'),
        ("Repeating 'I have a dream' at the start of several sentences is called", 'anaphora', ['alliteration', 'oxymoron', 'litotes'],
         'Repetition at the start of clauses'),
        ("What is the effect of the antithesis in 'Ask not what your country can do for you; ask what you can do for your country'?",
         'The reversal makes the call to duty memorable and challenges the audience',
         ['It confuses the audience on purpose', 'It lists facts about the country', 'It adds humour to a serious speech'],
         'Contrasting halves create emphasis'),
    ]),
    S('ib-g10-english:1:3', 'Audience, purpose and context of a speech', [
        ('The purpose of a persuasive speech is mainly to', 'convince the audience to think or act in a certain way',
         ['tell a fictional story', 'describe a place neutrally', 'list instructions'], 'Persuade'),
        ('A speech to a youth climate rally would most likely use', 'direct address, urgency and inclusive "we"',
         ['complex legal terms', 'a calm, neutral report style', 'very long technical tables'], 'Fit language to audience'),
        ('Why might the same speech be received differently 50 years after it was given?', 'The historical context and audience values have changed',
         ['The words physically change', 'Speeches lose all meaning over time', 'Audiences cannot read old speeches'],
         'Meaning depends on context'),
    ]),
    S('ib-g10-english:2:2', 'Narrative voice and point of view', [
        ("A story told using 'I' by a character in it has a", 'first-person narrator', ['third-person narrator', 'second-person narrator', 'omniscient chorus'],
         "The narrator is 'I'"),
        ('A narrator looking back on childhood as an adult is called a', 'retrospective narrator', ['unreliable narrator by default',
                                                                                                   'second-person narrator', 'chorus'],
         'They narrate with hindsight'),
        ('What is a key effect of a limited first-person narrator in a coming-of-age novel?',
         'Readers share the narrator\'s growing understanding and may see more than the narrator does',
         ['Readers know every character\'s thoughts', 'The story has no viewpoint', 'The narrator is always objective'],
         'Limited view creates dramatic irony'),
    ]),
]

SOCIAL_PRE = [
    S('ib-g9-social-science:2:2', 'Unification of Italy and Germany', [
        ('Which leader is most associated with the unification of Germany in 1871?', 'Bismarck', ['Mazzini', 'Garibaldi', 'Cavour'],
         'Prussian chief minister'),
    ]),
    S('ib-g9-social-science:3:2', 'The Scramble for Africa', [
        ('The Berlin Conference of 1884-85 was held to', 'set rules for European powers claiming African territory',
         ['end slavery in America', 'unify Germany', 'create the League of Nations'], 'It divided Africa among Europeans'),
        ('Why were African borders drawn at the Berlin Conference later a source of conflict?',
         'They ignored ethnic and cultural groups living in those areas',
         ['They followed rivers exactly', 'Africans drew them themselves', 'They gave every group its own country'],
         'Arbitrary borders split and combined peoples'),
    ]),
    S('ib-g9-social-science:7:2', 'Price determination: equilibrium, shortages and surpluses', [
        ('When demand is greater than supply at the current price, there is a', 'shortage', ['surplus', 'balance', 'subsidy'],
         'Buyers want more than is available'),
        ('If there is a surplus of mangoes, what usually happens to the price?', 'It falls', ['It rises', 'It stays fixed', 'It doubles'],
         'Sellers cut prices to clear stock'),
        ('Concert tickets sell out within minutes and resell online for triple the price. What does this suggest?',
         'The original price was set below equilibrium', ['The price was too high', 'There was a surplus of tickets', 'Demand was very low'],
         'A shortage shows price below equilibrium'),
    ]),
    S('ib-g9-social-science:8:2', 'Electoral systems and representation', [
        ('In first past the post, a candidate wins a seat by', 'getting more votes than any other candidate',
         ['getting over 50% of all votes nationally', 'being chosen by the party', 'drawing lots'], 'A simple plurality'),
        ('Proportional representation aims to', 'give parties seats in proportion to their share of the vote',
         ['give all seats to the largest party', 'remove elections', 'let only one party stand'], 'Seats match votes'),
        ('Party A wins 40% of votes nationally but 60% of seats under first past the post. Why can this happen?',
         'It narrowly wins many constituencies, and votes for losing candidates win nothing',
         ['Votes are counted twice', 'Proportional representation is used', 'Smaller parties get bonus seats'],
         'Winner-takes-all in each seat'),
    ]),
]

SOCIAL_CUR = [
    S('ib-g10-social-science:1:1', 'Long-term causes of the First World War', [
        ('Which of these is a long-term cause of the First World War?', 'the alliance system', ['the Treaty of Versailles',
                                                                                              'the Great Depression', 'the Cold War'],
         'MAIN: militarism, alliances, imperialism, nationalism'),
        ('The naval race before 1914 was mainly between', 'Britain and Germany', ['France and Russia', 'Italy and Austria', 'Japan and the USA'],
         'Both built Dreadnought battleships'),
        ('How did the alliance system turn a local Balkan crisis into a world war?', 'Countries were bound to defend allies, so one war pulled in others',
         ['It prevented any country from joining', 'It made all countries neutral', 'It only involved Serbia'],
         'Commitments spread the conflict'),
    ]),
    S('ib-g10-social-science:1:4', 'The Treaty of Versailles: terms and reactions', [
        ('The Treaty of Versailles was signed in', '1919', ['1914', '1939', '1945'], 'After the armistice of 1918'),
        ('Which of these was a term of the treaty?', 'Germany had to pay reparations', ['Germany gained colonies', 'Germany kept a large navy',
                                                                                      'Germany united with Austria'], 'Payments for war damage'),
        ('Why did many Germans call the treaty a "Diktat"?', 'Germany was not allowed to negotiate the terms',
         ['They wrote it themselves', 'It was very generous', 'It was signed in Berlin'], 'A dictated peace'),
    ]),
    S('ib-g10-social-science:2:2', 'Democracy, communism, fascism and Nazism', [
        ('In a democracy, governments are chosen through', 'free elections', ['inheritance', 'military force', 'a single party'],
         'Power comes from the people'),
        ('Which ideology called for the state to own the means of production?', 'communism', ['fascism', 'liberal democracy', 'monarchy'],
         'Based on Marx'),
        ('What did fascism and communism have in common in the 1930s?', 'Both used one-party states and suppressed opposition',
         ['Both supported free elections', 'Both protected private enterprise equally', 'Both rejected propaganda'],
         'Both were authoritarian'),
    ]),
    S('ib-g10-social-science:2:4', "Stalin's USSR", [
        ("Stalin's plans to rapidly build industry were called", 'Five-Year Plans', ['the New Deal', 'the Marshall Plan', 'Perestroika'],
         'Targets set by the state'),
        ('Collectivisation meant', 'small farms were merged into large state-controlled farms', ['farms were sold to private owners',
                                                                                                  'farming was banned', 'only kulaks could farm'],
         'Land was taken into collective farms'),
        ('Why did collectivisation cause a famine in Ukraine in 1932-33?', 'Grain was seized for the state and resisting peasants were punished',
         ['There was too much grain', 'Farmers chose to stop eating', 'Industry used all the water'], 'Forced requisitioning'),
    ]),
]

DESIGN = {
    'designId': 'g10-ib', 'grade': 10, 'stream': 'none', 'boards': ['ib'],
    'title': 'IB MYP Year 5 onboarding test',
    'groups': [
        G('maths', 'Mathematics', MATHS_PRE_G10, MATHS_CUR),
        G('science', 'Sciences', SCIENCE_PRE_G10, SCIENCE_CUR),
        G('english', 'Language and Literature', ENGLISH_PRE_G10, ENGLISH_CUR),
        G('social-science', 'Individuals and Societies', SOCIAL_PRE, SOCIAL_CUR),
    ],
}
