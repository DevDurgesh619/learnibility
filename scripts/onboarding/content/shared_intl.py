"""Prerequisite slots shared by Cambridge and IB humanities in grade 8 (international contexts)."""
from dsl import S

SOCIAL_PRE_INTL_G8 = [
    S({'cambridge': 'cambridge-g8-social-science:1:3', 'ib': 'ib-g8-social-science:1:1'}, 'Map skills: scale and distance',
      note='Grade 7: map scale, grid references and distance', items=[
        ('On a map with a scale of 1 : 50 000, two towns are 4 cm apart. What is the real distance between them?', '2 km',
         ['20 km', '200 m', '4 km'], '4 x 50 000 = 200 000 cm = 2 km'),
    ]),
    S({'cambridge': 'cambridge-g8-social-science:1:1', 'ib': 'ib-g8-social-science:4:1'}, 'Chronology and timelines',
      note='Grade 7: chronology, centuries and timelines', items=[
        ('A century is a period of', '100 years', ['10 years', '1000 years', '50 years'], 'Centuries are 100-year periods'),
        ('Which order is correct, earliest first?',
         'Building of the Egyptian pyramids, the Roman Empire, the Industrial Revolution, the First World War',
         ['The Roman Empire, the Egyptian pyramids, the First World War, the Industrial Revolution',
          'The Industrial Revolution, the Roman Empire, the Egyptian pyramids, the First World War',
          'The Egyptian pyramids, the Industrial Revolution, the Roman Empire, the First World War'],
         'About 2500 BCE, about 27 BCE to 476 CE, about 1760 to 1840, 1914 to 1918'),
    ]),
    S({'cambridge': 'cambridge-g8-social-science:1:2', 'ib': 'ib-g8-social-science:5:3'}, 'Primary and secondary sources',
      note='Grade 7: using sources as evidence', items=[
        ('Which is a primary source about the First World War?', "A soldier's letter written in 1916",
         ['A textbook written in 2020', 'A film made in 2019', 'A website summary of the war'],
         'A primary source was made at the time by someone involved'),
        ("Why might a wartime newspaper be an unreliable source about the enemy country?",
         'It may be biased to support its own side',
         ['Newspapers never report wars', 'It was printed on old paper', 'It is too detailed'],
         'Wartime papers were often censored or used for propaganda'),
        ('Two historians disagree about why an empire collapsed. What is the best explanation?',
         'They use different evidence and give different weight to each cause',
         ['One of them must be lying', 'Empires collapse for only one reason', 'History cannot be studied'],
         'Interpretations differ because evidence is selected and weighed differently'),
    ]),
    S({'cambridge': 'cambridge-g8-social-science:7:2', 'ib': 'ib-g8-social-science:8:1'}, 'People, settlement and needs',
      note='Grade 7: human needs and why settlements grow where they do', items=[
        ('Which of these is a basic human need?', 'Clean water', ['A smartphone', 'Designer clothes', 'A car'],
         'Needs are essential for survival; the others are wants'),
        ('Why have many large cities grown up next to rivers or coasts?', 'For water supply, transport and trade',
         ['Rivers make the weather colder', 'Coasts have no natural hazards', 'It is cheaper to build on water'],
         'Water routes carried goods and people'),
        ('A country has an ageing population. Which challenge is it most likely to face?',
         'More spending on pensions and healthcare, with fewer people of working age',
         ['Too many schools', 'A shortage of retired people', 'Less need for doctors'],
         'Older people need more care while the workforce shrinks'),
    ]),
]
