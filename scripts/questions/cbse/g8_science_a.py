"""CBSE class 8 science (NCERT Curiosity) families, chapters 1-4."""
from __future__ import annotations

from qbank import name, two_names, num, num_distractors, mcq
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap

S = 'cbse-g8-science-ch'

# ======================= ch01 Exploring the Investigative World of Science
# st1 Science as a way of asking questions
c1s1_defs = [
    ('an observation', 'information gathered directly using our senses or instruments, such as seeing that a leaf is yellow'),
    ('an inference', 'a conclusion or explanation we draw from observations, such as guessing that a yellow leaf lacks water'),
    ('a testable question', 'a question that can be answered by doing an experiment or collecting evidence'),
    ('evidence', 'observations and measurements that support or reject an idea'),
    ('curiosity', 'the urge to wonder and ask why and how things happen'),
    ('a prediction', 'a statement of what we expect to happen in a test, based on our idea'),
]
c1s1_cats = {
    'a testable question': ['Does salt dissolve faster in hot water than in cold water?',
                            'Do seeds germinate without water?',
                            'Does a ball bounce higher on a cement floor than on grass?',
                            'Does a plant kept in the dark stay green?',
                            'Does sugar dissolve faster when stirred?',
                            'Does a wet cloth dry faster in the sun than in the shade?'],
    'a question that cannot be tested in an experiment': ['Which colour is the most beautiful?',
                                                         'Is cricket a better game than football?',
                                                         'Which festival is the most enjoyable?',
                                                         'Is a rose nicer than a lotus?'],
}
c1s1_obs = {
    'an observation': ['The milk has turned sour and smells bad.', 'The thermometer reads 38 °C.',
                       'The leaves of the plant are drooping.', 'The iron nail has a brown coating.',
                       'The candle flame went out when covered with a glass.', 'The puddle was smaller by evening.'],
    'an inference': ['The milk was left out too long and microbes spoiled it.', 'The child has a fever.',
                     'The plant has not been watered for days.', 'The nail rusted because it was kept in moist air.',
                     'The flame needs air to keep burning.', 'The water of the puddle evaporated in the heat.'],
}
c1s1_mc = [
    ('Which of these is the best first step when you notice something puzzling in nature?', 'Ask a clear question about it',
     'Write the final conclusion', 'Ignore it if the textbook does not mention it', 'Ask a friend to guess the answer',
     'Science begins with observing carefully and asking a clear question.'),
    ('Science is best described as:', 'a way of finding out about the world through questions, observation and evidence',
     'a fixed list of facts that never changes', 'a collection of opinions of famous people', 'only the work done in big laboratories',
     'Science is a process; ideas are tested and revised when new evidence appears.'),
    ('Which statement about scientific ideas is correct?', 'They can change when new evidence is found',
     'They never change once written in a book', 'They are accepted only if a famous scientist says so', 'They do not need any evidence',
     'Scientific knowledge is open to revision with new evidence.'),
    ('Riya says, "Plants grow towards light." What should she do to check her idea scientifically?', 'Test it by keeping a potted plant near a window and observing it',
     'Ask her classmates to vote on it', 'Write it in her notebook as a fact', 'Search for a picture of a plant',
     'An idea is checked by testing and collecting evidence.'),
]
c1s1_why = [
    ('Why is "Which flower is the prettiest?" not a scientific question?', 'Its answer depends on personal opinion; it cannot be tested or measured with evidence.',
     '1 mark: depends on opinion/taste. 1 mark: cannot be tested or measured.'),
    ('Why do scientists repeat an observation or an experiment several times?', 'To make sure the result is reliable and not due to chance or a mistake.',
     '1 mark: reliability/consistency. 1 mark: rules out chance or errors.'),
    ('Why should observations be recorded immediately and honestly, even if they are unexpected?', 'Memory is unreliable, and unexpected results are also evidence that may change our idea.',
     '1 mark: accurate record. 1 mark: unexpected results are useful evidence.'),
    ('Explain the difference between an observation and an inference with one example.', 'An observation is what we notice with our senses (the road is wet); an inference is an explanation drawn from it (it rained).',
     '1 mark: difference. 1 mark: correct example pair.'),
]
c1s1_ar = [
    ('Scientific knowledge can change over time.', 'New observations and evidence can show that an earlier idea was incomplete or wrong.', 'a',
     'Both true; new evidence is the reason ideas change.'),
    ('"Does a plant need sunlight to stay green?" is a testable question.', 'A testable question can be answered by an experiment or by collecting evidence.', 'a',
     'We can keep one plant in light and one in the dark and compare; R explains why it is testable.'),
    ('An inference is the same as an observation.', 'An inference is an explanation based on observations.', 'd',
     'A is false: an observation is what we sense; R is true.'),
    ('Asking questions is an important part of science.', 'Scientists only read books and never do experiments.', 'c',
     'A is true; R is false because scientists test ideas by experiments.'),
]
c1s1_apply = [
    ('Tanvi notices that the ants in her kitchen always gather near the sugar jar. Write one observation, one question and one testable prediction she can make.',
     'Observation: ants gather near the sugar jar. Question: Are ants attracted to sweet food? Prediction: if sugar and salt are kept side by side, more ants will go to the sugar.',
     '1 mark each: observation, testable question, prediction.'),
    ('Kabir sees that the iron gate at his school rusts faster during the monsoon. Frame a testable question and say what he could compare.',
     'Question: Does moisture make iron rust faster? Compare two iron nails, one kept in a dry closed bottle and one in moist air, for a week.',
     '1 mark: testable question. 1 mark: a fair comparison.'),
    ('Convert this vague question into a testable one: "Why are some fruits better?"',
     'For example: "Does a banana kept in the refrigerator stay fresh longer than one kept at room temperature?"',
     '1 mark: question names what is changed and what is observed/measured.'),
]
c1s1_case = [
    ('Read: Meera saw that curd sets quickly in summer but takes much longer in winter. She wondered why. Her grandmother said curd needs warmth.\n'
     '(i) Write Meera\'s observation. (ii) Frame a testable question. (iii) Suggest a simple test using two bowls of milk with a spoon of curd each. (iv) What result would support her grandmother\'s idea?',
     '(i) Curd sets faster in summer. (ii) Does temperature affect how fast curd sets? (iii) Keep one bowl in a warm place and one in the refrigerator for 8 hours. (iv) Curd sets in the warm bowl but not (or less) in the cold one.',
     '1 mark for each part.'),
]

# st2 Steps of scientific investigation
c1s2_steps = ['observe', 'ask a question', 'form a hypothesis', 'test it with an experiment', 'analyse the results', 'draw a conclusion', 'share the findings']
c1s2_defs = [
    ('a hypothesis', 'a possible explanation or answer to a question that can be tested'),
    ('an experiment', 'a planned test carried out to check whether a hypothesis is supported'),
    ('a conclusion', 'a statement, based on the results, that says whether the hypothesis was supported'),
    ('analysis of results', 'looking for patterns in recorded data, often using tables and graphs'),
    ('a variable', 'any factor that can change in an experiment'),
    ('peer review', 'checking of a scientist\'s work by other scientists before it is accepted'),
]
c1s2_inv = [
    ('Ananya thinks that seeds need water to germinate.', 'Seeds need water to germinate.', 'Keep moong seeds on dry cotton and on wet cotton for three days and compare.'),
    ('Aarav thinks a dark coloured cloth heats up faster in sunlight.', 'Dark cloth absorbs more heat than white cloth.', 'Wrap two identical bottles of water in black and white cloth, keep them in the sun and measure the temperature after 30 minutes.'),
    ('Ishita thinks that sugar dissolves faster in hot water.', 'Sugar dissolves faster in hot water than in cold water.', 'Add one spoon of sugar to equal amounts of hot and cold water and time how long it takes to dissolve.'),
    ('Rohan thinks that plants grow better in sunlight.', 'Plants need sunlight to grow well.', 'Grow two similar pots of seedlings, one in sunlight and one in a dark cupboard, water both equally and compare after a week.'),
    ('Diya thinks that a cut apple turns brown faster in air.', 'Air makes a cut apple turn brown.', 'Keep one cut piece in open air and one wrapped tightly in cling film; compare after an hour.'),
    ('Vihaan thinks that a ball bounces higher on a hard floor.', 'Balls bounce higher on hard surfaces.', 'Drop the same ball from the same height onto cement and onto a mattress and measure the bounce height.'),
    ('Kavya thinks that salt water freezes more slowly than plain water.', 'Salt slows down freezing.', 'Keep equal cups of plain and salt water in the freezer and check them every 15 minutes.'),
    ('Arjun thinks that a wet cloth dries faster in wind.', 'Wind speeds up drying.', 'Hang two identical wet handkerchiefs, one in front of a fan and one in still air, and time how long each takes to dry.'),
]


def c1s2_hyp(r):
    who, hyp, test = r.choice(c1s2_inv)
    wrong = [x[1] for x in c1s2_inv if x[1] != hyp]
    stem = f'{who} Which of these is the hypothesis being tested?'
    return mcq(stem, hyp, r.sample(wrong, 3), f'The hypothesis is the testable idea: "{hyp}"', r)


def c1s2_design(r):
    who, hyp, test = r.choice(c1s2_inv)
    return {'stem': f'{who} Describe a simple experiment to test this idea.', 'answer': test,
            'key': '1 mark: two set-ups differing in only one factor. 1 mark: what is observed or measured and compared.'}


def c1s2_order(r):
    k = r.randint(4, 6)
    start = r.randint(0, len(c1s2_steps) - k)
    seq = c1s2_steps[start:start + k]
    sh = seq[:]
    while sh == seq:
        r.shuffle(sh)
    letters = 'PQRSTU'
    lab = {s: letters[i] for i, s in enumerate(sh)}
    ans = ' → '.join(lab[s] for s in seq)
    wrong = set()
    while len(wrong) < 3:
        w = seq[:]
        r.shuffle(w)
        ws = ' → '.join(lab[s] for s in w)
        if ws != ans:
            wrong.add(ws)
    stem = 'Arrange these steps of a scientific investigation in the correct order: ' + '; '.join(f'{lab[s]} – {s}' for s in sh) + '.'
    return mcq(stem, ans, list(wrong), f'Order: {" → ".join(seq)}.', r)


c1s2_mc = [
    ('What should a scientist do if the results of an experiment do not support the hypothesis?', 'Revise the hypothesis and test again',
     'Change the results so that they match', 'Stop the investigation and hide the results', 'Announce the hypothesis as correct anyway'),
    ('Which step comes immediately after forming a hypothesis?', 'Testing it by an experiment', 'Drawing the conclusion', 'Sharing the findings', 'Asking the first question'),
    ('Why is it useful to share findings with others?', 'Others can check, repeat and build on the work', 'It makes the experiment unnecessary',
     'It guarantees the result is correct', 'It avoids the need to record data'),
    ('A good hypothesis must be:', 'testable', 'always correct', 'very long', 'based on opinion only'),
    ('Which tool is most useful for spotting a pattern in measurements?', 'A table or graph of the data', 'A drawing of the apparatus', 'The title of the experiment', 'A list of materials'),
]
c1s2_why = [
    ('Why is a hypothesis not the same as a guess?', 'A hypothesis is based on observations and can be tested by an experiment; a random guess need not be.',
     '1 mark: based on observation/prior knowledge. 1 mark: testable.'),
    ('Why should a conclusion be based only on the results of the experiment?', 'Otherwise the conclusion reflects opinion or expectation instead of evidence.',
     '1 mark: evidence. 1 mark: avoids bias.'),
    ('A result that does not support the hypothesis is still useful. Explain.', 'It tells us the idea needs to be changed, and leads to a better hypothesis.',
     '1 mark: rejects/refines idea. 1 mark: leads to new test.'),
    ('Why do scientists keep a detailed record of how they did an experiment?', 'So that others can repeat it exactly and check whether they get the same results.',
     '1 mark: repeatability. 1 mark: checking.'),
]
c1s2_ar = [
    ('A hypothesis must be testable.', 'Only a testable idea can be supported or rejected by evidence from an experiment.', 'a', 'R explains A.'),
    ('An experiment always proves the hypothesis right.', 'Experiments are designed to test whether a hypothesis is supported.', 'd',
     'A is false: results may reject the hypothesis; R is true.'),
    ('Scientists share their findings with others.', 'Other scientists can repeat the experiment and check the results.', 'a', 'R explains why findings are shared.'),
    ('Drawing a conclusion comes before testing.', 'A conclusion is based on the results of the test.', 'd', 'A is false: testing comes first; R is true.'),
]
c1s2_long = [
    ('Sneha noticed that her tulsi plant on the balcony was growing towards the railing side where sunlight comes. Describe all the steps of a scientific investigation she could follow, from observation to sharing her findings.',
     'Observation: plant bends towards light. Question: Do plants grow towards light? Hypothesis: plant shoots grow towards the light source. Experiment: keep a seedling in a box with a hole on one side; another box fully open as comparison; same water and soil. Results: record the direction of bending daily. Conclusion: if the shoot bends towards the hole, the hypothesis is supported. Share: present the record to the class.',
     '1 mark each for observation + question, hypothesis, fair experiment, recording/analysis, conclusion and sharing (max 5).'),
]

# st3 Fair tests, variables and tables
c1s3_exp = [
    ('how the amount of water given affects the height of bean plants', 'amount of water given each day', 'height of the plants',
     ['type of plant', 'size of pot', 'amount of sunlight', 'type of soil']),
    ('how the temperature of water affects the time taken by sugar to dissolve', 'temperature of water', 'time taken to dissolve',
     ['amount of sugar', 'volume of water', 'type of sugar', 'stirring']),
    ('how the height of a ramp affects how far a toy car rolls', 'height of the ramp', 'distance rolled by the car',
     ['the same toy car', 'surface of the floor', 'length of the ramp', 'starting point on the ramp']),
    ('how the length of a pendulum affects the time of one oscillation', 'length of the thread', 'time for one oscillation',
     ['mass of the bob', 'angle of release', 'type of thread', 'stopwatch used']),
    ('how the surface affects the distance a marble rolls', 'type of surface', 'distance rolled',
     ['the same marble', 'height of release', 'slope of the ramp', 'starting point']),
    ('how the number of batteries affects the brightness of a bulb', 'number of cells', 'brightness of the bulb',
     ['the same bulb', 'length of wires', 'type of wire', 'the switch used']),
    ('how the colour of a container affects how fast the water in it warms in sunlight', 'colour of the container', 'rise in water temperature',
     ['volume of water', 'size and material of container', 'time kept in the sun', 'starting temperature']),
    ('how the amount of salt affects the freezing time of water', 'amount of salt added', 'time taken to freeze',
     ['volume of water', 'freezer used', 'type of container', 'starting temperature']),
]


def c1s3_ind(r):
    aim, ind, dep, ctrl = r.choice(c1s3_exp)
    who = name(r)
    return mcq(f'{who} is investigating {aim}. Which is the variable that {who} changes (independent variable)?', ind,
               [dep] + r.sample(ctrl, 2), f'The factor deliberately changed is the {ind}; the {dep} is measured.', r)


def c1s3_dep(r):
    aim, ind, dep, ctrl = r.choice(c1s3_exp)
    who = name(r)
    return mcq(f'In an experiment to find {aim}, what does {who} measure (dependent variable)?', dep,
               [ind] + r.sample(ctrl, 2), f'The {dep} is the result that is measured.', r)


def c1s3_ctrl(r):
    aim, ind, dep, ctrl = r.choice(c1s3_exp)
    k = r.choice(ctrl)
    return mcq(f'For a fair test of {aim}, which of these must be kept the same?', k,
               [ind, dep, 'none of the factors'], f'{cap(k)} is a controlled variable; only the {ind} is changed.', r)


def c1s3_unfair(r):
    aim, ind, dep, ctrl = r.choice(c1s3_exp)
    a, b = two_names(r)
    k = r.choice(ctrl)
    return {'stem': f'{a} and {b} tested {aim}. They changed the {ind}, but they also changed the {k} at the same time. Explain why their test is not fair and how to correct it.',
            'answer': f'Two factors changed, so we cannot tell whether the {ind} or the {k} caused the change in the {dep}. Keep the {k} the same and change only the {ind}.',
            'key': '1 mark: two variables changed so effect cannot be linked to one. 1 mark: keep all except one factor the same.'}


def c1s3_plan(r):
    aim, ind, dep, ctrl = r.choice(c1s3_exp)
    return {'stem': f'Plan a fair test to find {aim}. Name the variable you will change, the variable you will measure and any two variables you will keep the same.',
            'answer': f'Change: {ind}. Measure: {dep}. Keep the same: {ctrl[0]} and {ctrl[1]} (also {ctrl[2]}).',
            'key': '1 mark each: independent variable, dependent variable, two controlled variables.'}


def c1s3_avg(r):
    who = name(r)
    item = r.choice([('time for 20 oscillations of a pendulum', 's', (14.0, 18.0)), ('distance rolled by a toy car', 'cm', (60, 140)),
                     ('height of a bean seedling after 7 days', 'cm', (5.0, 12.0)), ('time for a sugar cube to dissolve', 's', (40, 90))])
    lo, hi = item[2]
    vals = [round(r.uniform(lo, hi), 1) for _ in range(3)]
    avg = round(sum(vals) / 3, 1)
    return {'stem': f'{who} measured the {item[0]} three times and recorded {vals[0]} {item[1]}, {vals[1]} {item[1]} and {vals[2]} {item[1]}. Find the average (mean) value and say why repeating is useful.',
            'answer': f'{num(avg, 1)} {item[1]}',
            'key': f'({vals[0]} + {vals[1]} + {vals[2]}) ÷ 3 = {num(sum(vals), 1)} ÷ 3 = {num(avg, 1)} {item[1]} (1 mark); repeating reduces the effect of errors and makes the result reliable (1 mark).',
            'distractors': num_distractors(avg, sum(vals), max(vals), min(vals), dp=1)}


def c1s3_table(r):
    temps = sorted(r.sample([10, 20, 30, 40, 50, 60, 70], 4))
    base = r.randint(150, 200)
    step = r.randint(15, 30)
    times = [base - step * i - r.randint(0, 5) for i in range(4)]
    rows = '; '.join(f'{t} °C – {s} s' for t, s in zip(temps, times))
    return {'stem': f'A class recorded the time taken for 5 g of sugar to dissolve in 100 mL of water at different temperatures: {rows}. (i) Name the independent and dependent variables. (ii) What pattern do you see? (iii) Predict the time at a temperature higher than {temps[-1]} °C.',
            'answer': f'(i) Independent: water temperature; dependent: time to dissolve. (ii) The higher the temperature, the less time sugar takes to dissolve. (iii) Less than {times[-1]} s.',
            'key': '1 mark each part.'}


c1s3_defs = [
    ('a fair test', 'an experiment in which only one factor is changed and all others are kept the same'),
    ('the independent variable', 'the factor that the investigator deliberately changes in an experiment'),
    ('the dependent variable', 'the factor that is measured or observed to see the effect of the change'),
    ('controlled variables', 'the factors that are kept the same so that the test is fair'),
    ('a control set-up', 'the set-up kept without the change being tested, used for comparison'),
    ('a reliable result', 'a result that comes out about the same when the experiment is repeated'),
]
c1s3_ar = [
    ('In a fair test only one factor is changed at a time.', 'If two factors are changed together, we cannot tell which one caused the result.', 'a', 'R explains A.'),
    ('Repeating a measurement and taking the average gives a more reliable value.', 'Random errors in single readings tend to cancel out in the average.', 'a', 'R explains A.'),
    ('A control set-up is not needed in an experiment.', 'A control set-up allows us to compare results with and without the factor being tested.', 'd', 'A is false; R is true.'),
    ('Results should be recorded in a table.', 'A table makes it easy to see patterns and compare readings.', 'a', 'R explains A.'),
]
c1s3_case = [
    ('Read: Kunal wanted to know whether fertiliser helps wheat seedlings grow. He took two pots. Pot A had garden soil and fertiliser and was kept in the sun. Pot B had sand without fertiliser and was kept indoors. After two weeks, Pot A seedlings were taller.\n'
     '(i) Is this a fair test? (ii) Name two factors other than fertiliser that differed. (iii) Can Kunal conclude that fertiliser made the seedlings taller? (iv) How should he redo the test?',
     '(i) No. (ii) Type of soil (soil vs sand) and sunlight. (iii) No, because the height difference may be due to soil or sunlight. (iv) Use the same soil, pot size, water and sunlight for both pots; add fertiliser only to one.',
     '1 mark for each part.'),
    ('Read: Pooja timed how long ice cubes took to melt on plates made of steel, plastic and wood, all kept in the same room. Steel: 18 min; plastic: 31 min; wood: 35 min.\n'
     '(i) What was the independent variable? (ii) What was measured? (iii) Which material conducts heat best? Give a reason. (iv) Name two things she must keep the same.',
     '(i) Material of the plate. (ii) Time for the ice to melt. (iii) Steel, because ice melted fastest on it, so heat reached the ice fastest. (iv) Size of ice cube, room temperature, size/thickness of plate (any two).',
     '1 mark for each part.'),
]

# ======================= ch02 The Invisible Living World
# st1 Microscope and observing cells
c2s1_parts = [
    ('eyepiece', 'the lens at the top of the microscope through which we look'),
    ('objective lens', 'the lens close to the slide that forms the first magnified image'),
    ('stage', 'the flat platform on which the slide is placed'),
    ('coarse adjustment knob', 'the knob used to bring the object roughly into focus'),
    ('fine adjustment knob', 'the knob used to make the image sharp'),
    ('mirror or light source', 'the part that directs light through the specimen'),
    ('diaphragm', 'the part that controls the amount of light passing through the specimen'),
    ('clips', 'the parts that hold the slide in place on the stage'),
]
c2s1_mc = [
    ('Which stain is commonly used to observe onion peel cells under a microscope?', 'Safranin (or iodine)', 'Methylene blue only', 'Lime water', 'Phenolphthalein',
     'Onion peel is stained with safranin or iodine solution; cheek cells with methylene blue.'),
    ('Which stain is used to observe human cheek cells?', 'Methylene blue', 'Safranin', 'Lime water', 'Copper sulphate', 'Methylene blue stains the nucleus of cheek cells.'),
    ('Why is a drop of glycerine put on the onion peel on a slide?', 'To prevent the peel from drying', 'To kill the cells', 'To magnify the cells', 'To colour the cell wall'),
    ('Why is the coverslip lowered gently at an angle on to the slide?', 'To avoid trapping air bubbles', 'To stain the cells', 'To increase the magnification', 'To keep the cells warm'),
    ('Why must the specimen on a slide be very thin?', 'So that light can pass through it', 'So that it stains less', 'So that it dries quickly', 'So that the slide does not break'),
    ('The first person to observe and name cells, in a thin slice of cork, was:', 'Robert Hooke', 'Antonie van Leeuwenhoek', 'Louis Pasteur', 'Alexander Fleming',
     'Robert Hooke observed cork cells in 1665 and called them cells.'),
    ('Who first observed living microorganisms in pond water using a simple microscope he made himself?', 'Antonie van Leeuwenhoek', 'Robert Hooke', 'Edward Jenner', 'Robert Koch'),
]


def c2s1_mag(r):
    e = r.choice([5, 10, 15])
    o = r.choice([4, 10, 40, 45, 100])
    who = name(r)
    m = e * o
    return {'stem': f'{who} uses a microscope with a {e}× eyepiece and a {o}× objective lens. What is the total magnification?',
            'answer': f'{m}×', 'key': f'Total magnification = eyepiece × objective = {e} × {o} = {m}×.',
            'distractors': [f'{e + o}×', f'{m * 10}×', f'{max(e, o)}×']}


def c2s1_size(r):
    e = r.choice([10, 15])
    o = r.choice([10, 40])
    m = e * o
    real = r.choice([0.02, 0.025, 0.04, 0.05, 0.1])
    img = round(real * m, 3)
    return {'stem': f'A cell appears {num(img, 3)} mm long when seen through a microscope with a {e}× eyepiece and a {o}× objective. What is its actual length?',
            'answer': f'{num(real, 3)} mm',
            'key': f'Magnification = {e} × {o} = {m}. Actual size = image size ÷ magnification = {num(img, 3)} ÷ {m} = {num(real, 3)} mm.',
            'distractors': [f'{num(img * m, 3)} mm', f'{num(img / e, 3)} mm', f'{num(img / o, 3)} mm']}


c2s1_why = [
    ('Why do we stain cells before observing them under a microscope?', 'Most cell parts are colourless; stains colour parts such as the nucleus so they become clearly visible.',
     '1 mark: parts are transparent/colourless. 1 mark: stain makes nucleus/parts visible.'),
    ('Why should we start focusing with the low-power objective lens?', 'It shows a larger area so the specimen is easy to find; it is also less likely to hit and break the slide.',
     '1 mark: wider field to locate specimen. 1 mark: safety of slide/lens.'),
    ('Why are cheek cells collected by gently scraping the inner side of the cheek with a clean toothpick or spoon?', 'The inner lining of the cheek sheds cells easily; gentle scraping collects them without injury, and clean tools avoid contamination.',
     '1 mark: cells come off easily. 1 mark: hygiene/no injury.'),
]
c2s1_steps = [
    ('Write the steps to prepare a temporary slide of onion peel.', 'Peel a thin transparent layer from the inner side of an onion scale; place it in a drop of water on a slide; add a drop of safranin/iodine; remove extra stain; add a drop of glycerine; lower a coverslip gently with a needle; observe under low then high power.',
     '½ mark each for thin peel, water drop, stain, glycerine, coverslip without bubbles, low-power first (max 3).'),
    ('Write the steps to prepare a temporary slide of human cheek cells.', 'Rinse mouth; gently scrape the inner cheek with a clean toothpick; spread the scraping in a drop of water on a slide; add a drop of methylene blue; add glycerine; place a coverslip at an angle; observe under the microscope.',
     '½ mark each step (max 3).'),
]
c2s1_ar = [
    ('A thin peel of onion is used to make a slide.', 'Light must pass through the specimen for it to be seen under a microscope.', 'a', 'R explains A.'),
    ('Glycerine is added to a slide preparation.', 'Glycerine stains the nucleus dark blue.', 'c', 'A true (prevents drying); R false.'),
    ('The total magnification of a microscope is the sum of eyepiece and objective magnifications.', 'The objective forms a magnified image that the eyepiece magnifies again.', 'd',
     'A false: magnifications multiply; R true.'),
]

# st2 Cell structure
c2s2_defs = [
    ('a cell', 'the basic structural and functional unit of all living organisms'),
    ('the cell membrane', 'the thin outer covering of a cell that controls the entry and exit of substances'),
    ('cytoplasm', 'the jelly-like substance between the cell membrane and the nucleus in which other parts are found'),
    ('the nucleus', 'the control centre of the cell that contains the genetic material'),
    ('the cell wall', 'the rigid outer layer outside the cell membrane in plant cells, made mainly of cellulose'),
    ('chloroplasts', 'green bodies in plant cells that contain chlorophyll and carry out photosynthesis'),
    ('a vacuole', 'a space in the cytoplasm filled with cell sap; it is large in plant cells'),
    ('a unicellular organism', 'an organism whose body is made of a single cell'),
]
c2s2_cats = {
    'found in plant cells but not in animal cells': ['cell wall', 'chloroplasts', 'a large central vacuole'],
    'found in both plant and animal cells': ['cell membrane', 'cytoplasm', 'nucleus', 'mitochondria'],
}
c2s2_org = {
    'a unicellular organism': ['Amoeba', 'Paramecium', 'Chlamydomonas', 'yeast', 'bacteria', 'Euglena'],
    'a multicellular organism': ['mango tree', 'earthworm', 'human being', 'mushroom', 'frog', 'grass'],
}
c2s2_mc = [
    ('Which part of the cell controls all its activities?', 'Nucleus', 'Cell membrane', 'Cytoplasm', 'Vacuole'),
    ('Which part allows only some substances to pass in and out of the cell?', 'Cell membrane', 'Cell wall', 'Nucleus', 'Chloroplast'),
    ('The cell wall of plant cells is made mainly of:', 'cellulose', 'protein', 'fat', 'starch'),
    ('Which cell part is found in a leaf cell but not in a cheek cell?', 'Chloroplast', 'Nucleus', 'Cytoplasm', 'Cell membrane'),
    ('A nerve cell is long and branched. This shape helps it to:', 'carry messages over long distances', 'store food', 'make food', 'fight germs'),
    ('Which of these cells is shaped like a disc and carries oxygen?', 'Red blood cell', 'Nerve cell', 'Muscle cell', 'Guard cell'),
    ('The largest single cell known is the:', 'egg of an ostrich', 'red blood cell', 'nerve cell of a frog', 'cell of a bacterium'),
]
c2s2_why = [
    ('Why do plant cells need a cell wall while animal cells do not?', 'Plants do not have a skeleton and cannot move away from harsh conditions; the rigid wall gives shape, support and protection.',
     '1 mark: support/shape. 1 mark: protection (animals have skeletons/other support).'),
    ('Why is the cell called the basic unit of life?', 'All living things are made of cells, and all life activities such as nutrition, respiration and growth take place in cells.',
     '1 mark: all organisms made of cells. 1 mark: functions occur in cells.'),
    ('Why are onion peel cells not green, even though they are plant cells?', 'Onion bulb scales grow underground away from light and do not make food, so they lack chlorophyll-containing chloroplasts.',
     '1 mark: no chloroplasts. 1 mark: no light/no photosynthesis.'),
    ('An Amoeba keeps changing its shape. Explain why.', 'It has no rigid cell wall; it pushes out finger-like pseudopodia to move and capture food.',
     '1 mark: no cell wall. 1 mark: pseudopodia for movement/feeding.'),
]
c2s2_ar = [
    ('Plant cells have a definite shape.', 'Plant cells have a rigid cell wall outside the cell membrane.', 'a', 'R explains A.'),
    ('Cheek cells contain chloroplasts.', 'Animal cells do not make their own food.', 'd', 'A false; R true.'),
    ('An elephant has more cells than a mouse.', 'Bigger organisms are made of a larger number of cells, not bigger cells.', 'a', 'Both true; R explains A.'),
    ('Nerve cells are long and branched.', 'Their shape suits their function of carrying messages.', 'a', 'Shape is related to function; R explains A.'),
    ('The nucleus is called the control centre of the cell.', 'The nucleus contains the genetic material that directs the activities of the cell.', 'a', 'R explains A.'),
]
c2s2_compare = [
    ('Give three differences between a plant cell and an animal cell.', 'Plant cell has a cell wall, chloroplasts and a large central vacuole; animal cell has no cell wall, no chloroplasts and small or no vacuoles.',
     '1 mark per correct difference (max 3).'),
    ('Draw a labelled diagram of a plant cell (describe it in words) and mark the parts not found in animal cells.', 'Labelled parts: cell wall, cell membrane, cytoplasm, nucleus, chloroplasts, large vacuole. Cell wall, chloroplasts and large vacuole are absent in animal cells.',
     '2 marks: correct labels; 1 mark: parts absent in animal cells identified.'),
]
c2s2_long = [
    ('Describe the structure of a cell with the help of its three main parts, state the function of each, and explain how a plant cell differs from an animal cell. Name one unicellular organism from each group (plant-like and animal-like).',
     'Cell membrane: outer boundary, controls entry and exit of substances. Cytoplasm: jelly-like, site of many life activities. Nucleus: controls activities, contains genetic material. Plant cells also have a cell wall, chloroplasts and a large vacuole. Examples: Chlamydomonas (plant-like), Amoeba or Paramecium (animal-like).',
     '3 marks: parts and functions; 1 mark: plant–animal differences; 1 mark: examples.'),
]
c2s2_case = [
    ('Read: Zoya observed two slides. Slide X showed brick-shaped cells with thick boundaries and many green bodies. Slide Y showed irregular flat cells with a darkly stained centre and thin boundaries.\n'
     '(i) Which slide is from a leaf? (ii) Name the green bodies. (iii) Which part made the boundary thick in X? (iv) Which stain could she have used for Y?',
     '(i) Slide X. (ii) Chloroplasts. (iii) Cell wall. (iv) Methylene blue (Y is cheek cells).', '1 mark each.'),
]

# st3 Microorganisms
c2s3_groups = {
    'a bacterium': ['Lactobacillus', 'Rhizobium', 'the cholera germ (Vibrio)', 'the tuberculosis germ'],
    'a fungus': ['yeast', 'bread mould (Rhizopus)', 'Penicillium', 'mushroom'],
    'a protozoan': ['Amoeba', 'Paramecium', 'Plasmodium', 'Euglena'],
    'an alga': ['Chlamydomonas', 'Spirogyra', 'diatoms', 'Volvox'],
    'a virus': ['the common cold virus', 'the polio virus', 'the measles virus', 'the influenza virus'],
}
c2s3_defs = [
    ('microorganisms', 'living organisms too small to be seen with the naked eye, seen only with a microscope'),
    ('a virus', 'a microbe that can reproduce only inside the cells of a living host'),
    ('a protozoan', 'a single-celled, animal-like microorganism such as Amoeba or Paramecium'),
    ('algae', 'simple plant-like organisms that contain chlorophyll and make their own food'),
    ('fungi', 'organisms such as yeast, moulds and mushrooms that do not have chlorophyll and absorb food from their surroundings'),
    ('a colony', 'a visible group of many microbes that have grown from one or a few cells'),
]
c2s3_mc = [
    ('Which group of microbes is considered to lie on the boundary between living and non-living?', 'Viruses', 'Bacteria', 'Fungi', 'Algae',
     'Viruses show life only inside host cells.'),
    ('Where can microorganisms be found?', 'Almost everywhere: in air, water, soil and inside other organisms', 'Only in dirty water', 'Only inside the human body', 'Only in hot springs'),
    ('Which of these microorganisms can make its own food?', 'Chlamydomonas', 'Amoeba', 'Yeast', 'Rhizopus'),
    ('Bread mould grows on moist bread as a cotton-like mass. It belongs to:', 'fungi', 'bacteria', 'protozoa', 'algae'),
    ('Bacteria are classified by shape. A spiral-shaped bacterium is called:', 'spirillum', 'coccus', 'bacillus', 'vibrio only'),
    ('Which microbe is visible to the naked eye as a group, though each is microscopic?', 'A patch of mould on bread', 'A single bacterium', 'A single virus', 'A single Amoeba'),
]
c2s3_why = [
    ('Why are viruses not grown on bread or in plain nutrient broth like bacteria?', 'Viruses can reproduce only inside living host cells; outside a host they are inactive.',
     '1 mark: need living host cell. 1 mark: inactive outside host.'),
    ('Why are microorganisms found almost everywhere, even in hot springs and icy regions?', 'They are very small, multiply rapidly and many kinds can survive extreme conditions, some forming protective spores.',
     '1 mark: small size and rapid multiplication. 1 mark: tolerance/spores.'),
    ('Why do slices of bread left in a moist, warm place develop mould faster?', 'Mould spores present in air need moisture, warmth and food to grow; these are available on moist bread.',
     '1 mark: spores in air. 1 mark: moisture/warmth favour growth.'),
]
c2s3_ar = [
    ('Viruses are called the link between living and non-living.', 'Viruses reproduce only inside the cells of a host organism.', 'a', 'R explains A.'),
    ('Algae are grouped with plant-like microbes.', 'Algae contain chlorophyll and make their own food.', 'a', 'R explains A.'),
    ('Yeast is a bacterium.', 'Yeast is a single-celled fungus.', 'd', 'A false; R true.'),
    ('Amoeba is a protozoan.', 'Amoeba has a rigid cell wall.', 'c', 'A true; R false: Amoeba has no cell wall.'),
]
c2s3_case = [
    ('Read: Students left three dishes open in the school lab for 30 minutes: one with boiled potato slice, one with moist bread, and one with dry rice. After four days in a warm cupboard, fuzzy coloured patches appeared on the potato and bread, but not on the rice.\n'
     '(i) What are the fuzzy patches? (ii) Where did they come from? (iii) Why did the dry rice not show them? (iv) Suggest one safety precaution while observing them.',
     '(i) Colonies of moulds (fungi) and bacteria. (ii) Spores and microbes present in the air. (iii) Microbes need moisture to grow. (iv) Do not open the covered dish or smell it; wash hands; dispose of it safely.',
     '1 mark each.'),
]
c2s3_hots = [
    ('A single bacterium divides into two every 20 minutes. Explain why food left out at room temperature for a few hours can become unsafe, even if it was clean at first.',
     'In 3 hours there are 9 doublings, so one bacterium becomes 2⁹ = 512; a few bacteria become thousands, enough to spoil food or cause illness.',
     '1 mark: doubling idea. 1 mark: number grows rapidly (e.g. 512 from one). 1 mark: link to spoilage/food poisoning.'),
]


def c2s3_double(r):
    t = r.choice([15, 20, 30])
    hrs = r.choice([1, 2, 3])
    start = r.choice([1, 2, 5, 10, 100])
    n = (hrs * 60) // t
    tot = start * 2 ** n
    return {'stem': f'A bacterium divides into two every {t} minutes under ideal conditions. If {start} bacteri{"um is" if start == 1 else "a are"} present at the start, how many will there be after {hrs} hour{"s" if hrs > 1 else ""}?',
            'answer': f'{tot:,}'.replace(',', ' ') if tot >= 10000 else str(tot),
            'key': f'Number of divisions = {hrs * 60} ÷ {t} = {n}; number = {start} × 2^{n} = {tot}.',
            'distractors': [str(start * 2 * n), str(start * n * n), str(start * 2 ** (n - 1))]}


# st4 Useful microorganisms
c2s4_use = {
    'Lactobacillus': 'setting milk into curd',
    'yeast': 'making bread and idli batter rise',
    'Rhizobium': 'fixing nitrogen in the root nodules of legumes',
    'Penicillium': 'producing the antibiotic penicillin',
    'decomposer bacteria and fungi': 'breaking down dead plants and animals into manure',
    'blue-green algae (cyanobacteria)': 'fixing nitrogen in paddy fields',
    'weakened or killed microbes': 'making vaccines',
}
c2s4_defs = [
    ('fermentation', 'the conversion of sugar into alcohol and carbon dioxide (or acids) by microorganisms such as yeast'),
    ('an antibiotic', 'a medicine made from microorganisms that kills or stops the growth of bacteria'),
    ('nitrogen fixation', 'the conversion of nitrogen gas of the air into nitrogen compounds that plants can use'),
    ('decomposition', 'the breaking down of dead plants and animals into simple substances by microbes'),
    ('a vaccine', 'a preparation of dead or weakened microbes that trains the body to fight a disease'),
    ('compost', 'manure formed when microbes decompose plant and animal wastes'),
]


def c2s4_match(r):
    k = r.choice(list(c2s4_use))
    wrong = [v for kk, v in c2s4_use.items() if kk != k]
    return mcq(f'Which of these is a use of {k}?', c2s4_use[k], r.sample(wrong, 3), f'{cap(k)}: {c2s4_use[k]}.', r)


def c2s4_which(r):
    k = r.choice(list(c2s4_use))
    wrong = [kk for kk in c2s4_use if kk != k]
    return mcq(f'Which microorganism is responsible for {c2s4_use[k]}?', k, r.sample(wrong, 3), f'{cap(k)} is responsible for {c2s4_use[k]}.', r)


c2s4_mc = [
    ('Who discovered fermentation by yeast in 1857?', 'Louis Pasteur', 'Alexander Fleming', 'Robert Hooke', 'Edward Jenner'),
    ('Penicillin was discovered by Alexander Fleming in the year:', '1929', '1857', '1665', '1796'),
    ('Which gas makes bread dough rise?', 'Carbon dioxide', 'Oxygen', 'Nitrogen', 'Hydrogen'),
    ('A little curd is added to warm milk to make curd because it:', 'contains Lactobacillus bacteria that multiply in milk', 'adds sugar to the milk', 'cools the milk quickly', 'kills all bacteria'),
    ('Root nodules of pea and gram plants contain:', 'nitrogen-fixing bacteria', 'disease-causing fungi', 'protozoa', 'viruses'),
    ('Antibiotics are NOT effective against:', 'the common cold', 'typhoid', 'tuberculosis', 'cholera', 'The common cold is caused by a virus; antibiotics act on bacteria.'),
]
c2s4_why = [
    ('Why does idli or dosa batter rise and smell sour when left overnight?', 'Microbes (yeast and bacteria) ferment the batter, producing carbon dioxide, which makes it rise, and acids, which make it sour.',
     '1 mark: fermentation by microbes. 1 mark: CO₂ rises, acid sours.'),
    ('Why do farmers grow legumes such as moong or gram between two cereal crops?', 'Rhizobium in legume root nodules fixes nitrogen and enriches the soil, so less fertiliser is needed.',
     '1 mark: Rhizobium/nitrogen fixation. 1 mark: soil fertility restored.'),
    ('Why should antibiotics be taken only on a doctor\'s advice and the full course completed?', 'Unnecessary or incomplete use lets bacteria survive and become resistant; antibiotics also kill useful bacteria in the gut.',
     '1 mark: resistance. 1 mark: harm to useful bacteria/side effects.'),
    ('Why is the role of microorganisms in decomposition important for nature?', 'They return nutrients from dead bodies and wastes to the soil for plants, and clean the environment.',
     '1 mark: recycling nutrients. 1 mark: cleaning wastes.'),
]
c2s4_ar = [
    ('Curd can be made by adding a small amount of curd to lukewarm milk.', 'Lactobacillus in curd multiplies in milk and converts it into curd.', 'a', 'R explains A.'),
    ('Antibiotics cure viral infections.', 'Antibiotics kill bacteria or stop their growth.', 'd', 'A false; R true.'),
    ('Leguminous plants improve soil fertility.', 'Rhizobium in their root nodules fixes atmospheric nitrogen.', 'a', 'R explains A.'),
    ('Bread is soft and spongy.', 'Carbon dioxide released by yeast during fermentation fills the dough.', 'a', 'R explains A.'),
]
c2s4_case = [
    ('Read: Harleen\'s mother mixed sugar and a little yeast in warm water, then added flour to make dough. After two hours in a warm place, the dough had doubled in size. Another batch made with very hot water did not rise.\n'
     '(i) Why did the first dough rise? (ii) Name this process. (iii) Why did the second batch not rise? (iv) What is the role of sugar?',
     '(i) Yeast released carbon dioxide which got trapped in the dough. (ii) Fermentation. (iii) Very hot water killed the yeast. (iv) Sugar is food for yeast.',
     '1 mark each.'),
    ('Read: In a village, the panchayat set up a pit where kitchen peels, leaves and cow dung were dumped and covered with soil. In two months, it turned into dark, crumbly manure.\n'
     '(i) What is this manure called? (ii) Which organisms made it? (iii) Why should plastics not be put in the pit? (iv) Give one benefit to farmers.',
     '(i) Compost. (ii) Decomposers—bacteria and fungi (with earthworms). (iii) Plastics are not decomposed by microbes. (iv) Adds nutrients to soil cheaply; reduces need for chemical fertilisers.',
     '1 mark each.'),
]

# st5 Harmful microorganisms and food preservation
c2s5_dis = {
    'bacteria': ['cholera', 'typhoid', 'tuberculosis', 'anthrax', 'citrus canker'],
    'viruses': ['common cold', 'chickenpox', 'polio', 'measles', 'yellow vein mosaic of bhindi'],
    'protozoa': ['malaria', 'amoebic dysentery'],
    'fungi': ['rust of wheat', 'ringworm'],
}
c2s5_pres = [
    ('salting', 'raw mango pickle, fish and amla', 'salt removes water from microbes and food, so microbes cannot grow'),
    ('adding sugar', 'jams, jellies and murabba', 'sugar reduces moisture, so microbes cannot grow'),
    ('using oil and vinegar', 'pickles and sauces', 'microbes cannot survive in oil and in the acid of vinegar'),
    ('pasteurisation', 'milk', 'milk is heated to about 70 °C for 15 to 30 seconds and suddenly chilled, which kills most microbes'),
    ('refrigeration', 'vegetables, milk and cooked food', 'low temperature slows down the growth of microbes'),
    ('drying', 'papad, raisins and red chillies', 'microbes need moisture to grow'),
    ('adding chemical preservatives', 'squashes and jams (sodium benzoate, sodium metabisulphite)', 'the chemicals check the growth of microbes'),
    ('airtight packing', 'dry fruits and chips', 'keeps out air, moisture and microbes'),
]


def c2s5_method(r):
    m, foods, why = r.choice(c2s5_pres)
    wrong = [x[0] for x in c2s5_pres if x[0] != m]
    return mcq(f'Which method of preservation is commonly used for {foods}?', m, r.sample(wrong, 3), f'{cap(m)}: {why}.', r)


def c2s5_how(r):
    m, foods, why = r.choice(c2s5_pres)
    return {'stem': f'How does {m} help to preserve food? Name one food preserved this way.', 'answer': f'{cap(why)}. Example: {foods}.',
            'key': '1 mark: how microbial growth is checked. 1 mark: example.'}


c2s5_mc = [
    ('Malaria is spread by the bite of the female:', 'Anopheles mosquito', 'Aedes mosquito', 'housefly', 'cockroach'),
    ('Which disease of animals is caused by bacteria?', 'Anthrax', 'Rust', 'Malaria', 'Polio'),
    ('Who discovered the bacterium that causes anthrax?', 'Robert Koch', 'Louis Pasteur', 'Robert Hooke', 'Alexander Fleming'),
    ('Food poisoning is caused by:', 'toxins produced by microbes growing in food', 'eating too much food', 'drinking boiled water', 'cold weather'),
    ('Pasteurised milk is heated to about:', '70 °C for 15–30 seconds and then chilled quickly', '100 °C for 1 hour', '40 °C for 2 hours', '0 °C for 1 day'),
    ('Carriers such as houseflies spread disease by:', 'carrying germs from dirt on to uncovered food', 'biting people', 'producing antibiotics', 'cleaning wastes'),
]
c2s5_why = [
    ('Why should we cover food kept on the dining table?', 'Flies and dust carry microbes that settle on uncovered food and can cause food poisoning or diseases like cholera.',
     '1 mark: carriers/dust bring microbes. 1 mark: illness from contaminated food.'),
    ('Why is milk boiled before storing it at home?', 'Boiling kills most microbes present in milk, so it does not spoil quickly.', '1 mark: kills microbes. 1 mark: delays spoilage.'),
    ('Why do pickles last for months without spoiling?', 'The salt, oil and acid (vinegar or lemon) in pickles do not allow microbes to grow.', '1 mark: salt/oil/acid named. 1 mark: microbes cannot grow.'),
    ('Why does stagnant water near houses increase cases of malaria and dengue?', 'Mosquitoes breed in stagnant water and spread the disease-causing microbes when they bite.', '1 mark: breeding site. 1 mark: vector spreads disease.'),
]
c2s5_ar = [
    ('Food kept in a refrigerator stays fresh for longer.', 'Microbes grow very slowly at low temperatures.', 'a', 'R explains A.'),
    ('Jams do not spoil easily.', 'Sugar in large amounts reduces the moisture available to microbes.', 'a', 'R explains A.'),
    ('Malaria is caused by a virus.', 'Malaria is spread by the female Anopheles mosquito.', 'd', 'A false (caused by the protozoan Plasmodium); R true.'),
    ('All microorganisms are harmful.', 'Some microorganisms cause diseases.', 'd', 'A false: many are useful; R true.'),
]
c2s5_case = [
    ('Read: After a wedding feast in Patna, several guests fell ill with vomiting and stomach pain. The leftover rice and paneer curry had been kept uncovered at room temperature for about 10 hours before being served again.\n'
     '(i) Name the illness. (ii) What caused it? (iii) Give two ways in which the food could have been kept safe. (iv) Why should one not taste food to check whether it is spoilt?',
     '(i) Food poisoning. (ii) Microbes grew in the food and produced toxins. (iii) Refrigerate within two hours; cover the food; reheat thoroughly. (iv) Toxins can be harmful even in small amounts and may not change the taste.',
     '1 mark each (iii: any two).'),
]
c2s5_long = [
    ('Explain with examples how microorganisms can harm (a) human beings, (b) plants and (c) our food. Describe any two methods of preserving food and how each works.',
     '(a) Cause diseases such as cholera, typhoid (bacteria), common cold (virus), malaria (protozoa). (b) Citrus canker (bacteria), rust of wheat (fungi), yellow vein mosaic of bhindi (virus). (c) Spoil food and cause food poisoning by producing toxins. Preservation: salting removes water; pasteurisation (70 °C for 15–30 s, then chilled) kills microbes; refrigeration slows their growth.',
     '1 mark each for (a), (b), (c); 1 mark each for two preservation methods with reason.'),
]

# ======================= ch03 Health
c3s1_defs = [
    ('health', 'a state of physical, mental and social well-being, not merely the absence of disease'),
    ('a balanced diet', 'a diet that contains all nutrients in the right amounts along with roughage and water'),
    ('hygiene', 'practices such as washing hands and keeping surroundings clean that help to maintain health and prevent disease'),
    ('a deficiency disease', 'a disease caused by the lack of a nutrient in the diet over a long time'),
    ('roughage', 'dietary fibre from plant foods that helps the body get rid of undigested food'),
    ('malnutrition', 'a condition caused by a diet with too little or too much of some nutrients'),
]
c3s1_def_dis = {
    'vitamin A': ('night blindness', 'carrots, papaya, green leafy vegetables, milk'),
    'vitamin C': ('scurvy (bleeding gums)', 'amla, lemon, orange, guava'),
    'vitamin D': ('rickets (soft, bent bones)', 'sunlight, milk, fish, eggs'),
    'iron': ('anaemia', 'green leafy vegetables, jaggery, dates'),
    'iodine': ('goitre', 'iodised salt, seafood'),
    'vitamin B1': ('beriberi', 'whole grains, pulses'),
    'calcium': ('weak bones and teeth', 'milk, curd, ragi'),
    'protein': ('kwashiorkor', 'pulses, milk, eggs, soybean'),
}


def c3s1_dd(r):
    n = r.choice(list(c3s1_def_dis))
    d, src = c3s1_def_dis[n]
    wrong = [v[0] for k, v in c3s1_def_dis.items() if k != n]
    return mcq(f'Lack of {n} in the diet causes:', d, r.sample(wrong, 3), f'{cap(n)} deficiency causes {d}. Sources: {src}.', r)


def c3s1_src(r):
    n = r.choice(list(c3s1_def_dis))
    d, src = c3s1_def_dis[n]
    who = name(r)
    return {'stem': f'A doctor tells {who} that the symptoms point to {d}. Which nutrient is lacking, and name two foods that {who} should eat more?',
            'answer': f'{cap(n)}; {src}.', 'key': '1 mark: nutrient. 1 mark: two correct food sources.'}


c3s1_food = {
    'rich in carbohydrates': ['rice', 'wheat chapati', 'potato', 'sugarcane jaggery', 'bajra roti'],
    'rich in proteins': ['dal (pulses)', 'paneer', 'eggs', 'soybean', 'fish'],
    'rich in fats': ['ghee', 'groundnut oil', 'butter', 'coconut', 'cashew nuts'],
}
c3s1_mc = [
    ('Which of these habits helps to keep us healthy?', 'Washing hands with soap before eating', 'Eating street food left uncovered', 'Skipping breakfast daily', 'Sleeping only four hours a night'),
    ('Mental well-being is part of health. Which activity supports it?', 'Talking to friends and family about worries', 'Staying alone all the time', 'Playing mobile games late into the night', 'Skipping meals'),
    ('Which is the best source of roughage?', 'Whole fruits, vegetables and whole grains', 'Refined sugar', 'Butter', 'Plain water'),
    ('Iodised salt is used to prevent:', 'goitre', 'scurvy', 'rickets', 'night blindness'),
]
c3s1_why = [
    ('Why is roughage important in our diet even though it gives no nutrients?', 'It adds bulk and helps the movement of food in the intestine, preventing constipation.', '1 mark: bulk/movement. 1 mark: prevents constipation.'),
    ('Why do growing children need more proteins?', 'Proteins are body-building foods needed for growth and repair of tissues.', '1 mark: body building. 1 mark: growth/repair.'),
    ('Why is it said that health is more than just being free of disease?', 'Health includes physical fitness, mental well-being and good social relationships.', '1 mark: physical. 1 mark: mental and social.'),
    ('Why should we not eat cut fruits sold uncovered at roadsides?', 'Flies and dust carry germs that settle on them and can cause diseases like cholera and typhoid.', '1 mark: contamination. 1 mark: disease.'),
]
c3s1_ar = [
    ('A person who eats only rice and potatoes may suffer from deficiency diseases.', 'Such a diet lacks proteins, vitamins and minerals.', 'a', 'R explains A.'),
    ('Water is an important part of a balanced diet.', 'Water helps the body absorb nutrients and remove wastes.', 'a', 'R explains A.'),
    ('Fats should be eaten in very large amounts.', 'Fats give more energy per gram than carbohydrates.', 'd', 'A false; R true.'),
]
c3s1_case = [
    ('Read: Om, a class 8 student in Lucknow, eats chips and noodles daily, rarely eats fruits or vegetables and plays mobile games till midnight. He often feels tired and has bleeding gums.\n'
     '(i) Which vitamin does he probably lack? (ii) Name the disease. (iii) Suggest two foods he should add. (iv) Suggest one change other than diet to improve his health.',
     '(i) Vitamin C. (ii) Scurvy. (iii) Amla, oranges, guava, lemon (any two). (iv) Sleep 8–9 hours / play outdoors / exercise.', '1 mark each.'),
]

c3s2_defs = [
    ('a communicable disease', 'a disease that spreads from an infected person to a healthy person'),
    ('a pathogen', 'a microorganism that causes disease'),
    ('a vector', 'an organism, such as a mosquito, that carries a pathogen from one host to another'),
    ('an infection', 'the entry and multiplication of a pathogen in the body'),
    ('an epidemic', 'a sudden spread of a disease to a large number of people in an area'),
    ('a pandemic', 'an epidemic that spreads across countries and continents'),
]
c3s2_mode = {
    'through air (coughing, sneezing)': ['tuberculosis', 'common cold', 'influenza', 'COVID-19', 'chickenpox', 'measles'],
    'through contaminated food and water': ['cholera', 'typhoid', 'hepatitis A', 'amoebic dysentery'],
    'through mosquito bites': ['malaria', 'dengue', 'chikungunya'],
}
c3s2_path = [('malaria', 'protozoan (Plasmodium)'), ('tuberculosis', 'bacterium'), ('cholera', 'bacterium'), ('typhoid', 'bacterium'),
             ('dengue', 'virus'), ('chickenpox', 'virus'), ('common cold', 'virus'), ('polio', 'virus'), ('ringworm', 'fungus')]


def c3s2_pathf(r):
    d, p = r.choice(c3s2_path)
    opts = ['bacterium', 'virus', 'fungus', 'protozoan (Plasmodium)']
    if p not in opts:
        opts[0] = p
    return mcq(f'{cap(d)} is caused by a:', p, [o for o in opts if o != p][:3], f'{cap(d)} is caused by a {p}.', r)


c3s2_mc = [
    ('Dengue is spread by the:', 'Aedes mosquito, which bites during the day', 'Anopheles mosquito, which bites at night', 'housefly', 'rat flea'),
    ('Which practice reduces the spread of tuberculosis?', 'Covering the mouth and nose while coughing', 'Sharing towels', 'Drinking water from a common glass', 'Living in crowded, closed rooms'),
    ('Which is a non-communicable disease?', 'Diabetes', 'Cholera', 'Malaria', 'Typhoid'),
    ('The housefly spreads disease mainly by:', 'carrying germs on its legs and body to uncovered food', 'biting humans', 'laying eggs in clean water', 'releasing toxins in air'),
    ('Which of these helps to control mosquito-borne diseases?', 'Not letting water collect in coolers, tyres and pots', 'Keeping garbage open', 'Sleeping without nets', 'Storing water in open drums'),
]
c3s2_why = [
    ('Why are cholera and typhoid more common during floods?', 'Sewage mixes with drinking water and spreads the bacteria that cause these water-borne diseases.', '1 mark: contamination. 1 mark: water-borne pathogens.'),
    ('Why is it advised to wear a mask in crowded places during a flu outbreak?', 'Flu spreads through droplets released when infected people cough or sneeze; a mask blocks them.', '1 mark: droplets. 1 mark: mask stops entry.'),
    ('Why is the female Anopheles mosquito called a vector?', 'It carries the malaria parasite from an infected person to a healthy person while sucking blood.', '1 mark: carrier. 1 mark: transfers pathogen.'),
]
c3s2_ar = [
    ('Covering the nose and mouth while sneezing prevents the spread of common cold.', 'Common cold spreads through droplets in air.', 'a', 'R explains A.'),
    ('Diabetes spreads from one person to another.', 'Diabetes is a non-communicable disease.', 'd', 'A false; R true.'),
    ('Mosquito nets help to prevent malaria.', 'Malaria is spread by contaminated food.', 'c', 'A true; R false: spread by mosquito bites.'),
]
c3s2_case = [
    ('Read: In a colony in Chennai, many people had high fever, body pain and low platelet counts after the rains. Health workers found water collected in old tyres, flower pots and coolers.\n'
     '(i) Which disease is likely? (ii) Name its vector. (iii) Why did cases increase after the rains? (iv) Give two control measures.',
     '(i) Dengue. (ii) Aedes mosquito. (iii) Stagnant water provided breeding sites. (iv) Empty/cover water containers, use nets/repellents, spray larvicide (any two).',
     '1 mark each.'),
]

c3s3_defs = [
    ('immunity', 'the ability of the body to resist and fight disease-causing microbes'),
    ('vaccination', 'giving a vaccine to a person to produce immunity against a disease'),
    ('antibodies', 'proteins made by white blood cells that fight specific pathogens'),
    ('an antibiotic', 'a medicine that kills bacteria or stops their growth'),
    ('immunisation', 'the process of making a person immune to a disease, usually by vaccination'),
    ('antibiotic resistance', 'the ability of bacteria to survive an antibiotic that once killed them'),
]
c3s3_mc = [
    ('Who developed the first vaccine, against smallpox, in 1796?', 'Edward Jenner', 'Louis Pasteur', 'Alexander Fleming', 'Robert Koch'),
    ('Which disease has been eradicated worldwide through vaccination?', 'Smallpox', 'Malaria', 'Tuberculosis', 'Dengue'),
    ('The BCG vaccine given to newborns protects against:', 'tuberculosis', 'polio', 'measles', 'diabetes'),
    ('Pulse Polio drives in India give children:', 'oral polio drops', 'antibiotic tablets', 'vitamin C syrup', 'insulin injections'),
    ('Which cells of the blood fight infection?', 'White blood cells', 'Red blood cells', 'Platelets', 'Plasma'),
    ('Antibiotics are useful against:', 'bacterial infections like typhoid', 'viral infections like common cold', 'all diseases', 'diabetes'),
]
c3s3_why = [
    ('A person who had chickenpox once rarely gets it again. Explain.', 'During the first infection the body made antibodies and memory cells; on a second attack it destroys the virus quickly.', '1 mark: antibodies formed. 1 mark: memory/quick response.'),
    ('How does a vaccine protect us without making us ill?', 'It contains dead or weakened microbes that cannot cause disease but make the body produce antibodies; these protect when the real microbe enters.', '1 mark: weakened/dead microbe. 1 mark: antibodies ready.'),
    ('Why should antibiotics not be used for a cold or flu?', 'These are caused by viruses, on which antibiotics have no effect; misuse also leads to antibiotic resistance.', '1 mark: viral cause. 1 mark: resistance.'),
    ('Why are vaccination drives important even for healthy children?', 'Vaccines prevent disease before infection; when most people are immune, the disease cannot spread in the community.', '1 mark: prevention. 1 mark: community protection.'),
]
c3s3_ar = [
    ('Vaccination protects us from some diseases.', 'Vaccines help the body to produce antibodies against specific microbes.', 'a', 'R explains A.'),
    ('Antibiotics should be taken for viral fever.', 'Antibiotics kill bacteria.', 'd', 'A false; R true.'),
    ('Taking the full course of an antibiotic is advised.', 'Stopping early may leave some bacteria alive, which can become resistant.', 'a', 'R explains A.'),
]
c3s3_case = [
    ('Read: Aditi\'s baby brother has a vaccination card listing BCG at birth, OPV drops, and MMR at 9 months. Her neighbour says vaccines are unnecessary because the baby looks healthy.\n'
     '(i) Which disease does BCG protect against? (ii) What does a vaccine contain? (iii) How does it protect? (iv) How would you reply to the neighbour?',
     '(i) Tuberculosis. (ii) Dead or weakened microbes. (iii) Makes the body produce antibodies so it is ready when the real microbe attacks. (iv) Vaccines prevent disease before it happens; healthy babies need them to stay protected.',
     '1 mark each.'),
]

c3s4_defs = [
    ('a non-communicable disease', 'a disease that does not spread from person to person, such as diabetes or heart disease'),
    ('a lifestyle disease', 'a disease linked to habits such as poor diet, lack of exercise, smoking or stress'),
    ('obesity', 'a condition of having too much body fat, which raises the risk of other diseases'),
    ('hypertension', 'a condition of persistently high blood pressure'),
    ('diabetes', 'a condition in which the blood sugar level stays high because the body does not make or use insulin properly'),
]
c3s4_cats = {
    'a communicable disease': ['tuberculosis', 'cholera', 'malaria', 'chickenpox', 'typhoid', 'dengue'],
    'a non-communicable disease': ['diabetes', 'hypertension', 'asthma', 'heart disease', 'cancer', 'obesity'],
}
c3s4_mc = [
    ('Which habit reduces the risk of lifestyle diseases?', 'At least one hour of physical activity daily', 'Eating fried snacks every day', 'Long hours in front of screens', 'Drinking sugary soft drinks often'),
    ('Smoking tobacco greatly increases the risk of:', 'lung cancer and heart disease', 'malaria', 'night blindness', 'cholera'),
    ('Which of these is a common cause of type 2 diabetes?', 'Lack of exercise and excess weight', 'Mosquito bites', 'Drinking boiled water', 'Lack of iodine'),
    ('Too much salt in the diet is linked to:', 'high blood pressure', 'anaemia', 'goitre', 'scurvy'),
]
c3s4_why = [
    ('Why are lifestyle diseases increasing among young people in cities?', 'Less outdoor play, long screen time, junk food rich in sugar, salt and fat, and stress.', '1 mark: inactivity. 1 mark: unhealthy diet/stress.'),
    ('Why can non-communicable diseases not be prevented by vaccines?', 'They are not caused by microbes; they result from lifestyle, heredity or environment.', '1 mark: not caused by pathogens. 1 mark: other causes.'),
    ('Why is regular exercise good for the heart?', 'It strengthens the heart muscle, helps control weight and blood pressure.', '1 mark: strengthens heart. 1 mark: controls weight/BP.'),
]
c3s4_ar = [
    ('Diabetes cannot be passed on by touching a patient.', 'Diabetes is a non-communicable disease.', 'a', 'R explains A.'),
    ('Junk food should be eaten daily for energy.', 'Junk food is high in fat, salt and sugar but low in other nutrients.', 'd', 'A false; R true.'),
    ('Yoga and exercise help reduce stress.', 'Stress has no effect on health.', 'c', 'A true; R false.'),
]
c3s4_case = [
    ('Read: A survey of 200 class 8 students in Indore found: 120 spend more than 3 hours daily on screens, 90 eat packaged snacks daily, and only 50 play outdoors for an hour.\n'
     '(i) What percentage of students play outdoors for an hour? (ii) Name two lifestyle diseases these habits may lead to. (iii) Suggest two changes the school can promote. (iv) Why is this a concern for the future?',
     '(i) 50/200 × 100 = 25%. (ii) Obesity, type 2 diabetes, hypertension (any two). (iii) Daily sports period, healthy canteen food, screen-time awareness (any two). (iv) Habits formed now continue into adulthood and raise the risk of heart disease and diabetes.',
     '1 mark each.'),
]
c3_long = [
    ('Distinguish between communicable and non-communicable diseases with two examples of each. Explain how a mosquito-borne disease spreads and suggest three ways to control it.',
     'Communicable: spread from person to person by pathogens (malaria, tuberculosis). Non-communicable: do not spread; caused by lifestyle/heredity (diabetes, hypertension). Malaria: female Anopheles bites an infected person, picks up Plasmodium and passes it to a healthy person. Control: remove stagnant water, use nets and repellents, spray larvicides.',
     '2 marks: distinction with examples; 1 mark: spread; 2 marks: control measures.'),
]

# ======================= ch04 Electricity: magnetic and heating effects
c4s1_cats = {
    'a good conductor of electricity': ['copper wire', 'aluminium foil', 'iron nail', 'graphite (pencil lead)', 'silver spoon', 'steel key'],
    'an insulator': ['rubber band', 'plastic scale', 'dry wood', 'glass bangle', 'cotton thread', 'paper'],
}
c4s1_defs = [
    ('an electric circuit', 'a complete closed path through which electric current flows'),
    ('a conductor', 'a material that allows electric current to pass through it easily'),
    ('an insulator', 'a material that does not allow electric current to pass through it'),
    ('a switch', 'a device used to open or close an electric circuit'),
    ('a battery', 'a combination of two or more electric cells joined together'),
    ('a circuit diagram', 'a drawing of an electric circuit using standard symbols for its components'),
]
c4s1_mc = [
    ('In the symbol of an electric cell, the longer line represents the:', 'positive terminal', 'negative terminal', 'switch', 'bulb'),
    ('A bulb does not glow when the switch is OFF because:', 'the circuit is open', 'the cell becomes weak', 'the bulb is fused', 'current flows faster'),
    ('Why are electricians\' screwdrivers and pliers covered with plastic or rubber?', 'Plastic and rubber are insulators and protect from electric shock', 'They are conductors', 'To make the tools heavier', 'To increase current'),
    ('Which liquid conducts electricity?', 'Lemon juice', 'Distilled water', 'Vegetable oil', 'Kerosene'),
    ('When two cells are joined in a battery, the positive terminal of one is connected to the:', 'negative terminal of the next', 'positive terminal of the next', 'bulb directly', 'switch only'),
]
c4s1_why = [
    ('Why is copper used for electric wires while their covering is made of PVC plastic?', 'Copper is a good conductor and carries current easily; PVC is an insulator that prevents shocks and short circuits.', '1 mark: copper conducts. 1 mark: plastic insulates/safety.'),
    ('A bulb glows when a pencil lead is placed in a circuit, but not with a pencil\'s wooden part. Explain.', 'Graphite (pencil lead) conducts electricity; dry wood is an insulator.', '1 mark: graphite conducts. 1 mark: wood insulates.'),
    ('Why should we never touch switches with wet hands?', 'Impure water conducts electricity, so current can pass through the body and give a shock.', '1 mark: water conducts. 1 mark: shock.'),
]
c4s1_ar = [
    ('A bulb glows only when the circuit is closed.', 'Current flows only through a complete path.', 'a', 'R explains A.'),
    ('Pure distilled water is a good conductor.', 'Tap water contains dissolved salts.', 'd', 'A false: distilled water is a poor conductor; R true.'),
    ('Electric wires are coated with plastic.', 'Plastic is a good conductor of electricity.', 'c', 'A true; R false.'),
]


def c4s1_tester(r):
    objs = r.sample(c4s1_cats['a good conductor of electricity'], 2) + r.sample(c4s1_cats['an insulator'], 2)
    r.shuffle(objs)
    who = name(r)
    glow = [o for o in objs if o in c4s1_cats['a good conductor of electricity']]
    no = [o for o in objs if o not in glow]
    return {'stem': f'{who} made a conduction tester with a cell, a bulb and two free wire ends, and touched the free ends to each of these in turn: {", ".join(objs)}. For which objects will the bulb glow? Give a reason.',
            'answer': f'Bulb glows for {", ".join(sorted(glow))}; not for {", ".join(sorted(no))}.',
            'key': f'1 mark: correct list. 1 mark: {", ".join(glow)} are conductors and complete the circuit; the others are insulators.'}


c4s2_defs = [
    ('the heating effect of electric current', 'the production of heat when electric current passes through a wire'),
    ('a fuse', 'a safety device with a thin wire of low melting point that melts and breaks the circuit when excess current flows'),
    ('a miniature circuit breaker (MCB)', 'a switch that automatically turns off when the current in a circuit becomes too high'),
    ('a heating element', 'the coil of special wire, such as nichrome, in an appliance that becomes hot when current passes'),
    ('a short circuit', 'a fault in which live and neutral wires touch, so a very large current flows'),
    ('overloading', 'drawing too much current by connecting too many appliances to one socket'),
]
c4s2_cats = {
    'an appliance that works mainly on the heating effect of current': ['electric iron', 'room heater', 'immersion rod', 'toaster', 'electric kettle', 'soldering iron'],
    'an appliance that works mainly on the magnetic effect of current': ['electric bell', 'electric fan motor', 'loudspeaker', 'crane electromagnet', 'mixer grinder motor'],
}
c4s2_mc = [
    ('The heating element of an electric iron is usually made of:', 'nichrome', 'copper', 'aluminium', 'plastic'),
    ('A fuse wire must have a:', 'low melting point', 'very high melting point', 'thick insulating cover', 'high strength'),
    ('An ISI mark on an electrical appliance tells us that it:', 'meets safety standards of the Bureau of Indian Standards', 'is made in a foreign country', 'uses no electricity', 'is very cheap'),
    ('LED bulbs are preferred over filament bulbs because they:', 'waste less energy as heat', 'give out more heat', 'use more electricity', 'need no circuit'),
    ('The filament of an incandescent bulb is made of:', 'tungsten', 'nichrome', 'copper', 'iron'),
    ('Which change makes a wire heat up more when current passes?', 'Increasing the current', 'Switching off the circuit', 'Using a thicker copper wire', 'Cooling the wire'),
]
c4s2_why = [
    ('Why do filament bulbs waste electricity?', 'Most of the electrical energy is converted into heat instead of light.', '1 mark: heat produced. 1 mark: little light.'),
    ('Why is a fuse connected in the live wire and why must a fuse of the correct rating be used?', 'It cuts off supply at the point of entry; a fuse of higher rating would not melt when excess current flows.', '1 mark: live wire/cut-off. 1 mark: rating.'),
    ('Why are MCBs replacing fuses in many homes?', 'An MCB switches off automatically and can be reset with a switch; a fuse wire must be replaced.', '1 mark: auto off. 1 mark: reset.'),
    ('Why should one not replace a blown fuse with a thick copper wire?', 'Copper has a high melting point and will not melt during overloading, so wiring may overheat and catch fire.', '1 mark: does not melt. 1 mark: fire risk.'),
]
c4s2_ar = [
    ('A fuse protects household wiring.', 'A fuse wire melts and breaks the circuit when a large current flows.', 'a', 'R explains A.'),
    ('Electric heaters use nichrome wire.', 'Nichrome gets hot and does not melt easily when current passes.', 'a', 'R explains A.'),
    ('An LED bulb gets hotter than a filament bulb.', 'An LED converts more of the electrical energy into light.', 'd', 'A false; R true.'),
]
c4s2_case = [
    ('Read: In winter, Manish\'s family in Shimla plugged a room heater, an electric kettle and an iron into a single multi-plug socket. After a few minutes, the MCB tripped and the lights went off.\n'
     '(i) Why did the MCB trip? (ii) What could have happened without the MCB? (iii) Which effect of current do all three appliances use? (iv) Give one safe practice.',
     '(i) Overloading drew too much current. (ii) Wires could overheat and cause a fire. (iii) Heating effect. (iv) Do not run many high-power appliances from one socket; use separate sockets.',
     '1 mark each.'),
]

c4s3_defs = [
    ('an electromagnet', 'a coil of insulated wire wound on an iron core that behaves like a magnet when current flows'),
    ('the magnetic effect of current', 'the production of a magnetic field around a wire carrying electric current'),
    ('a soft iron core', 'the iron piece inside the coil of an electromagnet that makes it much stronger'),
]
c4s3_mc = [
    ('Who first observed that a wire carrying current deflects a nearby compass needle?', 'Hans Christian Oersted', 'Michael Faraday', 'Thomas Edison', 'Isaac Newton'),
    ('Which change makes an electromagnet stronger?', 'Increasing the number of turns of the coil', 'Removing the iron core', 'Using fewer cells', 'Using a plastic core'),
    ('Electromagnets are used in cranes in scrap yards because:', 'they can be switched on and off to lift and drop iron', 'they attract plastic', 'they never lose magnetism', 'they work without electricity'),
    ('When the current in an electromagnet is switched off, it:', 'loses most of its magnetism', 'becomes stronger', 'becomes a permanent magnet', 'gets very hot'),
    ('Which of these devices uses an electromagnet?', 'Electric bell', 'Torch bulb', 'Electric heater', 'Solar cell'),
    ('Reversing the direction of current in an electromagnet:', 'reverses its north and south poles', 'stops it from working', 'doubles its strength', 'makes it non-magnetic'),
]


def c4s3_strength(r):
    a, b = two_names(r)
    t1, t2 = r.sample([20, 30, 40, 50, 60, 80, 100], 2)
    c1, c2 = r.choice([1, 2]), r.choice([1, 2])
    if (t1 - t2) * (c1 - c2) < 0 or (t1 == t2 and c1 == c2):
        c2 = c1
    strong = a if (t1, c1) > (t2, c2) else b
    return {'stem': f'{a} wound {t1} turns of insulated wire on an iron nail and connected it to {c1} cell{"s" if c1 > 1 else ""}. {b} wound {t2} turns on an identical nail with {c2} cell{"s" if c2 > 1 else ""}. Whose electromagnet will pick up more pins? Explain.',
            'answer': f"{strong}'s electromagnet",
            'key': f'More turns (and more current from more cells) make an electromagnet stronger; {strong}\'s coil has {"more turns" if t1 != t2 else "the same turns but more cells"}.',
            'distractors': [f"{a if strong == b else b}'s electromagnet", 'Both pick up the same number', 'Neither picks up pins']}


c4s3_why = [
    ('Why is an iron nail used inside the coil of an electromagnet?', 'Iron gets magnetised strongly and concentrates the magnetic field, making the electromagnet much stronger.', '1 mark: iron magnetised. 1 mark: stronger field.'),
    ('Why is insulated wire used to make the coil of an electromagnet?', 'So that current flows through the whole length of the coil instead of jumping between touching turns.', '1 mark: prevents short between turns. 1 mark: current through all turns.'),
    ('Give one advantage of an electromagnet over a permanent magnet.', 'Its magnetism can be switched on and off, and its strength can be changed.', '1 mark: switchable. 1 mark: adjustable strength.'),
]
c4s3_ar = [
    ('An electromagnet can be switched off.', 'An electromagnet is magnetic only while current flows through its coil.', 'a', 'R explains A.'),
    ('A compass needle deflects near a current-carrying wire.', 'A current-carrying wire produces a magnetic field around it.', 'a', 'R explains A.'),
    ('An electromagnet attracts plastic beads.', 'Electromagnets attract magnetic materials such as iron.', 'd', 'A false; R true.'),
]
c4s3_case = [
    ('Read: Rahul wound wire around an iron nail and connected it to a cell. He counted the pins it could hold: 10 turns – 4 pins; 20 turns – 9 pins; 30 turns – 13 pins.\n'
     '(i) What pattern do you see? (ii) What was kept the same? (iii) Predict the pins for 40 turns. (iv) What would happen if he used two cells with 30 turns?',
     '(i) More turns, more pins: the electromagnet becomes stronger. (ii) The nail, the cell, the type of wire and pins. (iii) About 17–18 pins. (iv) It would pick up more than 13 pins because the current increases.',
     '1 mark each.'),
]

c4s4_defs = [
    ('earthing', 'connecting the metal body of an appliance to the earth by a wire so that leaked current flows safely to the ground'),
    ('an electric bell', 'a device in which an electromagnet repeatedly attracts an iron strip so that a hammer strikes a gong'),
    ('the contact screw', 'the part of an electric bell that touches the iron strip to complete the circuit'),
]
c4s4_mc = [
    ('In an electric bell, the circuit breaks each time the hammer strikes because:', 'the iron strip moves away from the contact screw', 'the cell runs down', 'the gong melts', 'the switch opens'),
    ('Which of these is an unsafe practice?', 'Pulling a plug out by its wire', 'Switching off the mains before repairs', 'Using ISI-marked appliances', 'Keeping water away from sockets'),
    ('The third pin in a three-pin plug is for:', 'earthing', 'extra current', 'switching', 'decoration'),
    ('If someone gets an electric shock, the first thing to do is:', 'switch off the mains or push them away with a dry wooden stick', 'pull them with bare hands', 'pour water on them', 'touch the wire to check'),
]
c4s4_why = [
    ('Explain why the hammer of an electric bell keeps striking the gong as long as the switch is pressed.', 'Current magnetises the electromagnet, which pulls the iron strip; this breaks contact at the screw, the magnet loses magnetism, the strip springs back, contact is made again and the cycle repeats.',
     '1 mark: attraction breaks circuit. 1 mark: strip returns and repeats.'),
    ('Why are appliances with metal bodies, such as a refrigerator, earthed?', 'If the live wire touches the metal body, the current flows to the earth instead of through a person touching it.', '1 mark: leaked current. 1 mark: path to earth avoids shock.'),
]
c4s4_ar = [
    ('An electric bell rings continuously while the switch is pressed.', 'The electromagnet repeatedly makes and breaks the circuit.', 'a', 'R explains A.'),
    ('We should never insert anything into a socket.', 'Sockets carry no current when the switch is ON.', 'c', 'A true; R false.'),
]
c4_long = [
    ('Describe how you would make an electromagnet using an iron nail, wire and a cell. Explain two ways to make it stronger, and describe how an electromagnet is used in an electric bell.',
     'Wind insulated copper wire tightly around an iron nail, connect the ends to a cell through a switch; it attracts pins when current flows. Stronger: more turns, more current (more cells). Bell: current magnetises the coil, which pulls an iron strip with a hammer that strikes the gong; this breaks the circuit at the contact screw, the strip returns and the cycle repeats.',
     '2 marks: making; 1 mark: two ways to strengthen; 2 marks: working of bell.'),
    ('Explain the heating effect of electric current. Name three appliances based on it, and describe how a fuse and an MCB protect a house. Why should we prefer LED bulbs?',
     'When current flows through a wire, heat is produced; more in wires like nichrome. Appliances: iron, heater, kettle, toaster. A fuse has a thin wire of low melting point in the live wire that melts when current is too large; an MCB switches off automatically and can be reset. LEDs give the same light using less electricity and waste less as heat.',
     '1 mark: effect; 1 mark: appliances; 2 marks: fuse/MCB; 1 mark: LED.'),
]

FAMILIES = {
    # ch01
    S + '01-st1': [TERM(c1s1_defs), DEF(c1s1_defs), CLS(c1s1_cats, 'Which of the following is {}?', C='C2', D='D2'),
                   CLS(c1s1_obs, 'Which of the following statements is {}?', C='C3', D='D2'), MC(c1s1_mc, C='C2', D='D2'),
                   SA(c1s1_why), ARF(c1s1_ar), SA(c1s1_apply, C='C3', D='D3'), CASE(c1s1_case),
                   SORT(c1s1_obs, 'Sort these statements into {A} and {B}: {L}', C='C3', D='D4', n=(2, 2))],
    S + '01-st2': [TERM(c1s2_defs), DEF(c1s2_defs), G('C2', 'D2', 'mcq', c1s2_hyp), MC(c1s2_mc, C='C2', D='D2'), SA(c1s2_why),
                   ARF(c1s2_ar), G('C3', 'D2', 'mcq', c1s2_order), G('C3', 'D3', 'explain', c1s2_design), G('C4', 'D4', 'mcq', c1s2_order),
                   LONG(c1s2_long)],
    S + '01-st3': [TERM(c1s3_defs), DEF(c1s3_defs), G('C1', 'D2', 'mcq', c1s3_ind), G('C2', 'D2', 'mcq', c1s3_dep), G('C2', 'D3', 'mcq', c1s3_ctrl),
                   ARF(c1s3_ar), G('C3', 'D2', 'numerical', c1s3_avg), G('C3', 'D3', 'explain', c1s3_unfair), G('C3', 'D4', 'multi_step', c1s3_plan),
                   G('C4', 'D3', 'case', c1s3_table, gap='G7'), CASE(c1s3_case, C='C4', D='D4'), G('C4', 'D5', 'multi_step', c1s3_plan)],
    # ch02
    S + '02-st1': [TERM(c2s1_parts), DEF(c2s1_parts, C='C1', D='D2'), MC(c2s1_mc, C='C1', D='D2'), SA(c2s1_why), ARF(c2s1_ar),
                   G('C3', 'D1', 'numerical', c2s1_mag), G('C3', 'D3', 'numerical', c2s1_size), SA(c2s1_steps, C='C2', D='D2', type='multi_step'),
                   G('C4', 'D4', 'numerical', c2s1_size)],
    S + '02-st2': [TERM(c2s2_defs), DEF(c2s2_defs), CLS(c2s2_cats, 'Which of the following is {}?', C='C2', D='D2'),
                   CLS(c2s2_org, 'Which of the following is {}?', C='C3', D='D1'), MC(c2s2_mc, C='C1', D='D2'), SA(c2s2_why), ARF(c2s2_ar),
                   SORT(c2s2_org, 'Classify the following into {A} and {B}: {L}.', C='C3', D='D2'), SA(c2s2_compare, C='C3', D='D3', type='multi_step'),
                   LONG(c2s2_long, C='C4', D='D4'), CASE(c2s2_case),
                   CLS(c2s2_org, 'Which of the following is {}?', C='C3', D='D3', neg=True)],
    S + '02-st3': [TERM(c2s3_defs), DEF(c2s3_defs), CLS(c2s3_groups, 'Which of the following is {}?', C='C2', D='D2'), MC(c2s3_mc, C='C1', D='D2'),
                   SA(c2s3_why), ARF(c2s3_ar), SORT(c2s3_groups, 'Classify these microorganisms as {A} or {B}: {L}.', C='C3', D='D3'),
                   CLS(c2s3_groups, 'Which of the following is {}?', C='C3', D='D2', neg=True), G('C3', 'D4', 'numerical', c2s3_double),
                   CASE(c2s3_case), SA(c2s3_hots, C='C4', D='D4', type='multi_step'), G('C4', 'D5', 'numerical', c2s3_double)],
    S + '02-st4': [TERM(c2s4_defs), DEF(c2s4_defs), G('C1', 'D2', 'mcq', c2s4_which), MC(c2s4_mc, C='C1', D='D2'), G('C2', 'D2', 'mcq', c2s4_match),
                   SA(c2s4_why), ARF(c2s4_ar), CASE(c2s4_case)],
    S + '02-st5': [MC(c2s5_mc, C='C1', D='D2'), CLS(c2s5_dis, 'Which of the following diseases is caused by {}?', C='C1', D='D1', verb='is caused by'),
                   G('C2', 'D2', 'mcq', c2s5_method), SA(c2s5_why), ARF(c2s5_ar), G('C3', 'D3', 'explain', c2s5_how),
                   SORT(c2s5_dis, 'Classify these diseases by the microbe that causes them — {A} or {B}: {L}.', C='C3', D='D2'),
                   CASE(c2s5_case), LONG(c2s5_long, C='C4', D='D4'), CLS(c2s5_dis, 'Which of the following diseases is caused by {}?', C='C3', D='D3', neg=True, verb='is caused by')],
    # ch03
    S + '03-st1': [TERM(c3s1_defs), DEF(c3s1_defs), G('C1', 'D2', 'mcq', c3s1_dd), CLS(c3s1_food, 'Which of these foods is {}?', C='C2', D='D2'),
                   MC(c3s1_mc, C='C2', D='D2'), SA(c3s1_why), ARF(c3s1_ar), G('C3', 'D3', 'explain', c3s1_src),
                   SORT(c3s1_food, 'Sort these foods into those {A} and those {B}: {L}.', C='C3', D='D2'), CASE(c3s1_case)],
    S + '03-st2': [TERM(c3s2_defs), DEF(c3s2_defs), G('C1', 'D2', 'mcq', c3s2_pathf), MC(c3s2_mc, C='C2', D='D2'),
                   CLS(c3s2_mode, 'Which of these diseases spreads {}?', C='C2', D='D3', verb='spreads'), SA(c3s2_why), ARF(c3s2_ar),
                   SORT(c3s2_mode, 'Group these diseases by how they spread — {A} or {B}: {L}.', C='C3', D='D3'),
                   CLS(c3s2_mode, 'Which of these diseases spreads {}?', C='C3', D='D2', neg=True, neg_tpl='Which of these diseases does NOT spread {}?', verb='spreads'), CASE(c3s2_case), LONG(c3_long, C='C4', D='D4')],
    S + '03-st3': [TERM(c3s3_defs), DEF(c3s3_defs), MC(c3s3_mc, C='C1', D='D2'), SA(c3s3_why), ARF(c3s3_ar),
                   CASE(c3s3_case)],
    S + '03-st4': [TERM(c3s4_defs), DEF(c3s4_defs), CLS(c3s4_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c3s4_mc, C='C1', D='D2'),
                   SA(c3s4_why), ARF(c3s4_ar), SORT(c3s4_cats, 'Classify these diseases as {A} or {B}: {L}.', C='C3', D='D3'),
                   CLS(c3s4_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True), CASE(c3s4_case)],
    # ch04
    S + '04-st1': [TERM(c4s1_defs), DEF(c4s1_defs), CLS(c4s1_cats, 'Which of the following is {}?', C='C1', D='D2'), MC(c4s1_mc, C='C2', D='D2'),
                   SA(c4s1_why), ARF(c4s1_ar), G('C3', 'D3', 'explain', c4s1_tester), CLS(c4s1_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True),
                   SORT(c4s1_cats, 'Classify as {A} or {B}: {L}.', C='C3', D='D1')],
    S + '04-st2': [TERM(c4s2_defs), DEF(c4s2_defs), MC(c4s2_mc, C='C1', D='D2'), CLS(c4s2_cats, 'Which of the following is {}?', C='C2', D='D2'),
                   SA(c4s2_why), ARF(c4s2_ar), SORT(c4s2_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3'),
                   CLS(c4s2_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True), CASE(c4s2_case), LONG(c4_long[1:], C='C4', D='D4')],
    S + '04-st3': [TERM(c4s3_defs + c4s2_defs[:2]), DEF(c4s3_defs), MC(c4s3_mc, C='C1', D='D2'), SA(c4s3_why), ARF(c4s3_ar),
                   G('C3', 'D3', 'explain', c4s3_strength), G('C3', 'D2', 'mcq', c4s3_strength), CASE(c4s3_case), LONG(c4_long[:1], C='C4', D='D4'),
                   G('C3', 'D4', 'explain', c4s3_strength)],
    S + '04-st4': [DEF(c4s4_defs), MC(c4s4_mc, C='C1', D='D2'), SA(c4s4_why), ARF(c4s4_ar), 
                   ],
}

# ----------------------------------------------------------------- higher-order (C4) items
H = {}
H['01-st1'] = [
    ('A TV advertisement claims, "Our toothpaste makes teeth 3 times stronger." What questions would a scientist ask before accepting this claim?',
     'Stronger compared with what? How was strength measured? How many people were tested, and was there a fair comparison with another toothpaste? Who did the test, and can it be repeated?',
     '1 mark each for any three valid questions about evidence, comparison, measurement or repeatability.'),
    ('Two students observe that a puddle dries up faster on a sunny day. One says, "The Sun sucks up the water." How would you turn this into a testable idea and check it?',
     'Testable idea: water evaporates faster when it is warmer. Test: keep equal amounts of water in identical plates in sun and shade and measure how long each takes to dry.',
     '1 mark: testable idea. 1 mark: fair comparison. 1 mark: what is measured.'),
    ('Nandini read online that eating carrots lets you see in total darkness. Explain how she could use science to judge this claim.',
     'Check the evidence and source; know that vitamin A in carrots prevents night blindness but cannot make eyes see without any light; a simple test in a dark room shows nobody can see with no light.',
     '1 mark: question the source/evidence. 1 mark: correct science. 1 mark: test or reasoning.'),
]
H['02-st1'] = [
    ('Yash sees only a dark circle with a thick black rim at the centre of his onion-peel slide, and no cells. Suggest what went wrong and how to correct it.',
     'An air bubble was trapped under the coverslip. Lower the coverslip gently at an angle using a needle so that air is pushed out.',
     '1 mark: air bubble identified. 1 mark: correct method.'),
    ('Under high power, Gauri sees only a blurred, very dark image of her cheek-cell slide. Give two possible reasons and the remedy for each.',
     'Too little light: open the diaphragm or adjust the mirror. Not focused: use the fine adjustment knob. (Also: specimen too thick—make a thinner smear.)',
     '1 mark per reason with remedy (any two).'),
]
H['02-st4'] = [
    ('A farmer grows wheat every year in the same field and finds the yield falling. Suggest how microorganisms can help him without buying more urea, and explain why.',
     'Grow a legume crop such as gram or moong between wheat crops (crop rotation); Rhizobium in root nodules fixes nitrogen and restores soil fertility. He can also add compost made by decomposers.',
     '1 mark: legume/crop rotation. 1 mark: Rhizobium fixes nitrogen. 1 mark: compost/other microbial method.'),
    ('Curd sets in 6 hours in summer in Chennai but takes much longer in winter in Shimla. Explain, and suggest how to set curd quickly in winter.',
     'Lactobacillus multiplies fastest in warmth; in cold it grows slowly. Keep the milk lukewarm and the bowl in a warm place (near a stove or in a casserole).',
     '1 mark: temperature affects bacterial growth. 1 mark: practical suggestion.'),
    ('Explain why a few spoons of yeast can raise a large amount of dough, but the dough stops rising if it is left in a refrigerator.',
     'Yeast cells multiply in the warm dough and each produces carbon dioxide, so a little yeast becomes a large population. In the cold, yeast activity slows down, so little gas is made.',
     '1 mark: multiplication. 1 mark: CO₂. 1 mark: low temperature slows yeast.'),
]
H['02-st5'] = [
    ('Milk packets from a dairy say "Pasteurised. Keep refrigerated. Use within 2 days." Explain why refrigeration is still needed after pasteurisation.',
     'Pasteurisation kills most but not all microbes; the few remaining or entering after opening can multiply at room temperature, so cold storage slows them down.',
     '1 mark: not all microbes killed. 1 mark: cold slows growth.'),
    ('Explain why the leaves of bhindi plants in a farm turned yellow with green veins, and why spraying an antibiotic did not help.',
     'Yellow vein mosaic is caused by a virus (spread by whiteflies); antibiotics act only on bacteria, so they have no effect on viruses.',
     '1 mark: viral disease. 1 mark: antibiotics do not act on viruses.'),
    ('A shopkeeper in a hilly town says he does not need to keep his jams in a refrigerator, but he keeps paneer in it. Justify his choice.',
     'Jam has a high sugar content, so microbes cannot grow; paneer is moist and rich in protein and spoils quickly unless kept cold.',
     '1 mark: sugar preserves jam. 1 mark: paneer perishable, needs cold.'),
]
H['03-st1'] = [
    ('A girl\'s diet is mostly rice, potato and tea. Predict two health problems she may face and plan one day\'s balanced meals for her.',
     'Problems: anaemia (iron), protein and vitamin deficiency, weakness. Meals: breakfast—poha with peanuts and milk; lunch—rice, dal, green leafy vegetable, curd; snack—fruit (guava/orange); dinner—roti, sprouts or paneer, salad.',
     '1 mark: two problems. 2 marks: meals include all nutrient groups.'),
    ('Why do doctors advise sunbathing in the morning for children with soft and bent bones?', 'Their bones are soft due to rickets (vitamin D deficiency); skin makes vitamin D in sunlight, which helps absorb calcium.',
     '1 mark: rickets/vitamin D. 1 mark: sunlight makes vitamin D.'),
    ('Compare the health effects of a meal of samosa and soft drink with a meal of roti, dal, sabzi and buttermilk.',
     'Samosa and soft drink: high fat, sugar and salt, little protein, vitamins or fibre; frequent use leads to obesity. Roti-dal meal: carbohydrates, proteins, vitamins, minerals, fibre and water—balanced.',
     '1 mark each comparison point (max 3).'),
]
H['03-st2'] = [
    ('Cases of diarrhoea rose in a village after a pipeline leaked near a drain. As a health worker, explain the cause and list three actions you would recommend.',
     'Sewage entered the drinking water and spread water-borne germs. Actions: boil or chlorinate drinking water; repair the leak; use ORS for patients; wash hands before eating.',
     '1 mark: cause. 2 marks: three actions.'),
    ('Why does a single person with tuberculosis in a crowded, poorly ventilated room pose a risk to many others?',
     'TB bacteria spread through droplets in air when the patient coughs; in a closed, crowded room the droplets stay and many people breathe them in.',
     '1 mark: airborne droplets. 1 mark: crowding/ventilation.'),
    ('A school reports chickenpox cases in one class. Should the whole school be closed? Give a reasoned answer.',
     'Not necessarily: infected children should stay at home until recovered, classmates watched for symptoms, rooms ventilated and hygiene improved; this breaks the spread without closing the school.',
     '1 mark: isolation of patients. 1 mark: other measures. 1 mark: reasoning.'),
]
H['03-st3'] = [
    ('A child is given an antibiotic for a bacterial infection, feels better after two days and stops taking it. A week later the illness returns and the same medicine does not work well. Explain.',
     'The surviving bacteria were the more resistant ones; they multiplied, so the infection returned and the antibiotic is now less effective (antibiotic resistance).',
     '1 mark: survivors. 1 mark: resistance develops.'),
    ('When almost every child in a city is vaccinated against measles, even the few unvaccinated babies are protected. Explain why.',
     'The virus cannot find enough people to infect, so it cannot spread in the community; this indirect protection is called herd immunity.',
     '1 mark: chain of spread broken. 1 mark: community/herd protection.'),
]
H['03-st4'] = [
    ('Explain how a family can reduce its risk of lifestyle diseases. Give three practical steps for a family in a city.',
     'Walk or cycle short distances, play outdoors daily; cook with less oil, salt and sugar; eat fruits and vegetables; limit screen time; regular health check-ups; avoid tobacco.',
     '1 mark per practical step (max 3).'),
    ('A healthy-looking person can have high blood pressure. Why are regular check-ups important even if one feels well?',
     'Non-communicable diseases such as hypertension and diabetes often show no early symptoms; check-ups detect them early so that lifestyle changes or treatment can prevent damage.',
     '1 mark: silent onset. 1 mark: early detection helps.'),
    ('Ravi\'s grandfather has diabetes. Ravi worries he can catch it by sharing meals. Explain why he cannot, and what can increase Ravi\'s own risk.',
     'Diabetes is non-communicable; it is not caused by germs. Ravi\'s own risk increases with family history, being overweight, lack of exercise and a diet high in sugar.',
     '1 mark: non-communicable. 1 mark: risk factors.'),
]
H['04-st1'] = [
    ('A torch does not glow even with new cells. List three faults you would check and explain why each would stop the torch from working.',
     'Cells put in the wrong way (circuit does not work); fused bulb (broken filament breaks the circuit); loose or rusted switch/spring contact (open circuit).',
     '1 mark per fault with reason.'),
    ('Diya says that since tap water conducts electricity, sea water must conduct even better. Is she right? Explain how you could test it.',
     'Yes, sea water has more dissolved salts so it conducts better. Test with a tester (cell, LED and wires): the LED glows brighter in salt water than in tap water.',
     '1 mark: correct prediction with reason. 1 mark: test.'),
]
H['04-st2'] = [
    ('A 1000 W heater and a 15 W LED are both used for 2 hours. Which uses more electrical energy and by how many times? Why does the heater cord feel warm?',
     'The heater: 1000 × 2 = 2000 Wh against 15 × 2 = 30 Wh, about 67 times more. The large current through the cord produces some heat (heating effect).',
     '1 mark: energy comparison. 1 mark: heating effect.'),
    ('Why does the coil of a heater glow red while the copper wires connecting it to the socket stay almost cold, though the same current flows through both?',
     'Nichrome has a much higher resistance than copper, so much more heat is produced in the coil; the copper wires are thick and have low resistance.',
     '1 mark: different materials. 1 mark: resistance/heat produced.'),
    ('Suggest why the electrical wiring of old houses sometimes catches fire when many new appliances are added.',
     'The old wires were not designed for large currents; overloading heats them, the insulation melts and a short circuit or fire can occur, especially if fuses were replaced with thick wire.',
     '1 mark: overloading. 1 mark: overheating and melted insulation.'),
]
H['04-st3'] = [
    ('Design a simple experiment to show that the strength of an electromagnet depends on the current. Name what you will change, measure and keep the same.',
     'Change: number of cells (1, 2, 3). Measure: number of pins lifted. Keep the same: number of turns, nail, wire and pins.',
     '1 mark each: change, measure, keep same.'),
    ('Why are electromagnets, not permanent magnets, used to separate iron scrap from other waste at recycling centres?',
     'The electromagnet lifts iron when switched on and drops it at the right place when switched off; its strength can be increased for heavy loads.',
     '1 mark: switch on/off to drop. 1 mark: adjustable strength.'),
]
H['04-st4'] = [
    ('Ananya\'s electric bell only buzzes once and then stays silent while she keeps the switch pressed. Suggest a fault and explain.',
     'The contact screw is not touching the iron strip again (badly adjusted or dirty), so after the first attraction the circuit stays broken and the hammer cannot repeat.',
     '1 mark: contact screw fault. 1 mark: circuit stays open.'),
    ('List three safety rules for using electricity at home and give the reason for each.',
     'Do not touch switches with wet hands (water conducts); do not overload sockets (wires overheat); use ISI-marked appliances and earthing (prevents shocks); switch off mains before repairs.',
     '1 mark per rule with reason (max 3).'),
    ('Why is it dangerous to fly kites near overhead electric wires, especially with metal-coated manja?',
     'A metal-coated or wet string can conduct electricity from the high-voltage line to the person, causing a severe shock or burns.',
     '1 mark: string conducts. 1 mark: shock danger.'),
]
for _k, _v in H.items():
    FAMILIES[S + _k].append(SA(_v, C='C4', D='D4', type='multi_step'))


# ----------------------------------------------------------------- data-based case generators
def c2_growth_case(r):
    who = name(r)
    t = r.choice([20, 30])
    start = r.choice([10, 20, 50, 100])
    temp = r.choice([('4 °C (refrigerator)', 'slower'), ('37 °C (warm room)', 'fastest')])
    vals = [start * 2 ** i for i in range(4)]
    return {'stem': (f'Read: {who} studied the growth of bacteria in a nutrient broth at 30 °C. The count was {vals[0]} at the start, {vals[1]} after {t} min, '
                     f'{vals[2]} after {2 * t} min and {vals[3]} after {3 * t} min.\n'
                     f'(i) How long do the bacteria take to double? (ii) Predict the count after {4 * t} min. (iii) Would growth be faster or slower at {temp[0]}? '
                     f'(iv) Use this to explain why cooked food should be refrigerated.'),
            'answer': f'(i) {t} min. (ii) {vals[3] * 2}. (iii) {"Slower" if temp[1] == "slower" else "Faster (near body temperature)"}. (iv) Cold slows bacterial multiplication, so food stays safe longer.',
            'key': '1 mark each part.'}


C3_MEASURE = {'dengue': 'Remove stagnant water from coolers, tyres and pots, and spray larvicide',
              'malaria': 'Drain stagnant water, spray insecticide and distribute mosquito nets',
              'typhoid': 'Supply chlorinated drinking water and check food sold in the open',
              'cholera': 'Supply safe chlorinated water and repair leaking pipes near drains',
              'common cold': 'Spread awareness about covering the mouth and nose while sneezing and washing hands',
              'tuberculosis': 'Screen people with long cough, ensure full treatment and good ventilation'}


def c3_survey_case(r):
    city = r.choice(['Indore', 'Patna', 'Kochi', 'Surat', 'Nagpur', 'Ranchi'])
    n = r.choice([200, 250, 400, 500])
    p = sorted(r.sample([10, 12, 15, 20, 24, 25, 30, 40], 3))
    d = r.sample([('dengue', 'mosquito bites'), ('typhoid', 'contaminated food and water'), ('common cold', 'air (droplets)'),
                  ('malaria', 'mosquito bites'), ('cholera', 'contaminated water'), ('tuberculosis', 'air (droplets)')], 3)
    rows = '; '.join(f'{x[0]} – {pp}%' for x, pp in zip(d, p))
    top = d[2]
    return {'stem': (f'Read: A health survey of {n} families in {city} after the monsoon recorded the percentage of families with at least one case of: {rows}.\n'
                     f'(i) How many families reported {top[0]}? (ii) How does {top[0]} spread? (iii) Which of these diseases are caused by bacteria? '
                     f'(iv) Suggest one measure the municipal body should take for {top[0]}.'),
            'answer': (f'(i) {p[2]}% of {n} = {p[2] * n // 100}. (ii) Through {top[1]}. '
                       f'(iii) {", ".join(x[0] for x in d if x[0] in ("typhoid", "cholera", "tuberculosis")) or "none of them"}. '
                       f'(iv) {C3_MEASURE[top[0]]}.'),
            'key': '1 mark each part.'}


def c4_magnet_case(r):
    who = name(r)
    per = r.choice([2, 3, 4])
    turns = [10, 20, 30, 40]
    pins = [per * t // 10 + r.choice([0, 0, 1]) for t in turns]
    return {'stem': (f'Read: {who} made an electromagnet with an iron nail and one cell and counted the pins it could hold for different numbers of turns: '
                     + '; '.join(f'{t} turns – {p} pins' for t, p in zip(turns, pins)) +
                     f'.\n(i) What is the independent variable? (ii) What pattern do you see? (iii) Predict the number of pins for 50 turns. (iv) Suggest one other way to make it stronger.'),
            'answer': f'(i) Number of turns. (ii) More turns, more pins (stronger electromagnet). (iii) About {per * 5} pins. (iv) Increase the current by using more cells.',
            'key': '1 mark each part.'}


FAMILIES[S + '02-st3'].append(G('C4', 'D4', 'case', c2_growth_case, gap='G7'))
FAMILIES[S + '03-st2'].append(G('C4', 'D3', 'case', c3_survey_case, gap='G7'))
FAMILIES[S + '04-st3'].append(G('C4', 'D3', 'case', c4_magnet_case, gap='G7'))

# ----------------------------------------------------------------- application items (C3) for subtopics without numericals
A3 = {}
A3['02-st4'] = [
    ('Kavya wants to make curd at home in winter. List the steps she should follow and explain the role of each.', 'Warm the milk till lukewarm (Lactobacillus grows best in warmth); add a spoon of curd (adds the bacteria); mix and cover; keep in a warm place for 6–8 hours (bacteria multiply and turn milk sour and thick).', '1 mark per step with reason (max 3).'),
    ('Which of these would be the best place to keep a compost pit for a school garden: a sunny dry corner, a shady moist corner, or a concrete-lined tank with no holes? Explain.', 'A shady, moist corner with soil contact: decomposers need moisture and moderate temperature and access to soil organisms; a sealed tank lacks air and drainage.', '1 mark: choice. 1 mark: reason.'),
    ('A farmer plans to grow wheat after harvesting a crop of moong. Explain why his wheat crop may need less urea.', 'Rhizobium in the root nodules of moong fixed atmospheric nitrogen into the soil, so some nitrogen is already available for wheat.', '1 mark: Rhizobium/nitrogen. 1 mark: soil enriched.'),
]
A3['03-st3'] = [
    ('A child has a viral fever. Her uncle suggests giving her leftover antibiotic tablets. What would you advise, and why?', 'Do not give them: antibiotics do not act on viruses; leftover doses may be wrong and can cause side effects and resistance. Consult a doctor; give rest, fluids.', '1 mark: advice. 1 mark: reason.'),
    ('Rahul cut his knee while playing. Two days later, the wound was red, swollen and warm. Explain what was happening in his body.', 'Germs entered the wound; white blood cells gathered to fight them, causing redness, swelling and warmth as part of the immune response.', '1 mark: infection. 1 mark: WBC response.'),
    ('Explain why polio drops are given to all young children in a pulse polio drive on the same day across India.', 'Vaccinating all children together builds immunity in the whole community at once, so the virus cannot find unprotected children to infect and spread.', '1 mark: all at once. 1 mark: stops spread.'),
]
A3['04-st4'] = [
    ('Describe how you would safely help a person who is stuck to a live wire after getting an electric shock.', 'Do not touch the person; switch off the main supply or pull out the plug; if not possible, push the wire away using a dry wooden stick or plastic; then call for medical help.', '1 mark: do not touch. 1 mark: cut supply/insulator. 1 mark: medical help.'),
    ('An electric bell rings very weakly. Suggest two reasons and how to fix them.', 'The cells are weak (replace them); the contact screw is loose or dirty (tighten/clean it); the gong is too far from the hammer (adjust it).', '1 mark per reason with fix (max 2).'),
]
for _k, _v in A3.items():
    FAMILIES[S + _k].append(SA(_v, C='C3', D='D3', type='explain'))
