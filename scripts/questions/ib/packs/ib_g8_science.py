"""IB MYP 3 Sciences (integrated) – ib-g8-science.

Criteria language: A knowing & understanding, B inquiring & designing (testable question, hypothesis, variables,
method), C processing & evaluating (tables, graphs, means, conclusions, reliability), D reflecting on the impacts of
science. Numerical items compute their own answers. Shared builders: ib_myp_science_common.py.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names  # noqa: F401
from ib_myp_science_common import MARKBAND_D, SUB, dataset as _dataset, evx, exx, g, inquiry as _inquiry  # noqa: F401

CONFIG = {'minutesPerMark': 1.2, 'mcqMinutes': 1.5}

# MYP 5 Sciences eAssessment-style on-screen exam, practised early in MYP 3: 20 items, 100 marks per mock.
MOCK = [
    dict(section='Task 1 – Knowing and understanding: quick-check items (criterion A)', count=6, c=['C1'], d=[1, 2, 2], type='mcq', marks=1),
    dict(section='Task 2 – Knowing and understanding: explain scientific knowledge (criterion A)', count=4, c=['C2'], d=[2, 3, 3], type='explain', marks=4),
    dict(section='Task 3 – Inquiring and designing: question, hypothesis, variables and method (criterion B)', count=4, c=['C3', 'C3', 'C4'], d=[3, 4], type='multi_step', marks=6, style='inquiry'),
    dict(section='Task 4 – Processing and evaluating: data, graphs and conclusions (criterion C)', count=4, c=['C3'], d=[3, 4], type='multi_step', marks=6, style='data'),
    dict(section='Task 5 – Reflecting on the impacts of science (criterion D)', count=2, c=['C4'], d=[5], type='long', marks=15),
]

R = Registry()
STYLE = {'eval_marks': 8, 'essay_marks': 15, 'markband': MARKBAND_D}


def init(subject_id):
    pass


def templates(st):
    return R.build(st, STYLE)


def inquiry(key, *a):
    _inquiry(R, key, *a)


def dataset(key, *a):
    _dataset(R, key, *a)


# =============================================================================================
# ch01 Scientific Investigation and Laboratory Skills
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('testable question', 'a question that can be answered by changing one variable and measuring the effect on another'),
           ('hypothesis', 'a prediction of the outcome of an investigation, with a scientific reason, that can be tested'),
           ('prediction', 'a statement of what you expect to happen in an experiment, often in the form "if … then …"'),
           ('research question', 'the focused question an investigation sets out to answer, naming the independent and dependent variables'),
           ('theory', 'a well-tested scientific explanation supported by a large body of evidence')],
    facts=[('Which of these is a testable scientific question?', 'Does the temperature of water affect how fast sugar dissolves?', ['Is chocolate the best flavour?', 'Why is the sky beautiful?', 'Should we visit Mars?'], 'It names a variable to change and one to measure.'),
           ('Which statement is a hypothesis rather than an observation?', 'If the light is brighter, then the plant will grow taller, because it can photosynthesise faster.', ['The plant is 12 cm tall.', 'The leaves are green.', 'The plant was watered on Monday.'], 'A hypothesis is a testable prediction with a reason.'),
           ('What should a good hypothesis include?', 'A prediction linking two variables and a scientific reason', ['Only the result of the experiment', 'A list of equipment', 'The conclusion'], 'It must be testable and justified.')],
    why=[('Explain why a hypothesis must be testable.', 'Science relies on evidence; if a hypothesis cannot be tested by measurement it cannot be supported or rejected by data.'),
         ('Explain why scientists still value an experiment whose results do not support their hypothesis.', 'The results are evidence; they show the prediction was wrong and lead to a better explanation or a new hypothesis.'),
         ('Explain why a research question should name both the independent and dependent variables.', 'It makes clear exactly what will be changed and what will be measured, so the investigation is focused and others can repeat it.')],
    contrast=[('a hypothesis', 'a theory', 'A hypothesis is a testable prediction for a particular investigation; a theory is a broad explanation that has been tested many times and is supported by lots of evidence.'),
              ('an observation', 'a hypothesis', 'An observation is something noticed or measured; a hypothesis is a testable prediction with a scientific reason that explains an observation.')],
    misc=[('A hypothesis is just a guess.', 'A hypothesis is an educated prediction based on scientific knowledge and includes a reason; it is testable.'),
          ('If the results support my hypothesis, it has been proved true.', 'Results can support a hypothesis, but further tests could disprove it; science does not prove ideas absolutely.')],
    cases=[('Ignaz Semmelweis and handwashing in Vienna (1847)', 'He noticed more mothers died in the ward run by doctors who came from dissections; he hypothesised that “cadaverous particles” caused fever and made doctors wash hands in chlorinated lime – deaths fell sharply.', 'forming and testing a hypothesis', 'An observation led to a testable prediction; changing one factor (handwashing) and measuring deaths tested it.'),
           ('Barry Marshall and stomach ulcers (1984)', 'Marshall hypothesised that bacteria (Helicobacter pylori), not stress, caused ulcers, and drank a culture to test it; he developed gastritis, which antibiotics cured.', 'testing a hypothesis against accepted ideas', 'Evidence from a test supported a new hypothesis and changed medical treatment; he shared the 2005 Nobel Prize.')],
    evaluate=[('Scientists should only publish experiments that support their hypothesis.', ['positive results seem more interesting and useful'], ['negative results stop others wasting time repeating failed ideas', 'hiding results biases the evidence (publication bias), e.g. in drug trials', 'honest reporting is a core scientific value'], 'All well-conducted results should be published; leaving out negative results distorts scientific knowledge.'),
              ('Citizen science projects, where members of the public collect data, produce useful science.', ['huge amounts of data over wide areas (e.g. bird counts, Galaxy Zoo)', 'engages people with science'], ['data quality may vary without training', 'needs careful checking by scientists'], 'With good design, training and checking, citizen science produces valuable data that professionals alone could not collect.')],
    extended=[('A student notices that bread goes mouldy faster in the kitchen than in the fridge. Write a testable research question, a hypothesis with a scientific reason, and state the independent and dependent variables for an investigation.', 'Question: How does temperature affect the time taken for mould to appear on bread? Hypothesis: if temperature is higher (up to about 30 °C), mould appears sooner, because fungal enzymes work faster and spores grow more quickly. IV: temperature; DV: days until mould is first visible (or area covered after 5 days).', 5)],
))


@R.add('ch01-st1', 'C3', (1, 4), 'short')
def rq_from_obs(rng, slot):
    obs, iv, dv, why = rng.choice([
        ('ice cubes melt faster on a metal tray than on a plastic tray', 'material of the tray', 'time for the ice cube to melt', 'metal is a better thermal conductor, transferring energy to the ice faster'),
        ('seedlings on a windowsill lean towards the window', 'direction of light', 'angle of bending of the seedling', 'shoots grow towards light (phototropism) to absorb more light for photosynthesis'),
        ('a ball bounces higher on the playground than on the grass', 'surface the ball is dropped on', 'bounce height', 'a soft surface absorbs more of the ball’s energy'),
        ('sugar disappears faster in hot tea than in iced tea', 'temperature of the water', 'time for the sugar to dissolve', 'particles move faster at higher temperature'),
        ('paper towels from different brands soak up different amounts of spilled water', 'brand of paper towel', 'volume of water absorbed', 'towels differ in thickness and in the spaces between fibres'),
        ('a bicycle tyre seems flatter on cold mornings', 'air temperature', 'tyre pressure', 'gas particles move more slowly when cold, so they hit the tyre walls less often and with less force'),
        ('cut apples turn brown faster when left in a warm room', 'temperature', 'time for the cut surface to turn brown', 'browning is caused by enzymes, which work faster when warmer (up to an optimum)')])
    who = name(rng)
    return dict(stem=f'{who} observes that {obs}. Write a testable research question and a hypothesis, with a scientific reason, that could be investigated.',
                answer=f'Research question: How does the {iv} affect the {dv}? Hypothesis: changing the {iv} will change the {dv}, because {why}.',
                markingKey=f'1 research question naming the IV ({iv}) and a measurable DV ({dv}); 1 testable prediction ("if … then …"); 1 scientific reason: {why}.', marks=3, gap='G4')


inquiry('ch01-st1',
        dict(ctx='how the temperature of water affects the time taken for a sugar cube to dissolve',
             iv='temperature of the water (°C)', dv='time for the sugar cube to dissolve completely – measured with a stopwatch',
             cvs=[('volume of water (100 cm³)', 'more water would dissolve the sugar faster'), ('type and size of sugar cube', 'smaller pieces dissolve faster'), ('stirring (none or the same rate)', 'stirring speeds dissolving'), ('type of container', 'affects heat loss')],
             hyp='If the water temperature increases, then the sugar will dissolve faster, because water particles move faster and collide with the sugar more often and with more energy.',
             method='Heat water and measure 100 cm³ into a beaker at 20, 30, 40, 50 and 60 °C (check with a thermometer); drop in one sugar cube and start the stopwatch; do not stir; stop when no solid remains; repeat three times at each temperature; calculate means and plot a line graph.',
             weak=('the sugar was stirred in some trials but not others', 'do not stir at all (or stir at the same rate with a magnetic stirrer) in every trial'),
             safety='hot water can scald – use a heat-proof mat and handle beakers with tongs'))
dataset('ch01-st1',
        dict(intro='{who} timed how long a sugar cube took to dissolve in 100 cm³ of water at different temperatures, without stirring.', iv=('Temperature', '°C'), xs=[20, 30, 40, 50, 60],
             dv=('Time to dissolve', 's'), f=lambda x: 9000 / (x + 10), dp=0, trend='The time to dissolve decreases as the water temperature increases.',
             why='At higher temperatures water particles move faster, so they collide with the sugar more often and break it apart more quickly.'))

R.facts('ch01-st2', F(
    terms=[('independent variable', 'the variable that the investigator deliberately changes'),
           ('dependent variable', 'the variable that is measured to see the effect of changing the independent variable'),
           ('control variable', 'a variable that is kept the same so that it does not affect the results'),
           ('fair test', 'an investigation in which only the independent variable is changed and all other variables are controlled'),
           ('control experiment', 'a version of the experiment without the factor being tested, used for comparison')],
    facts=[('In an investigation into how the height of a ramp affects the speed of a toy car, what is the dependent variable?', 'The speed of the car', ['The height of the ramp', 'The mass of the car', 'The length of the ramp'], 'It is what is measured.'),
           ('Why are control variables kept the same?', 'So that only the independent variable affects the dependent variable', ['To make the experiment faster', 'To change the results', 'Because they cannot be measured'], 'This makes it a fair test.'),
           ('A student tests how fertiliser affects plant growth. Which is a control variable?', 'Amount of water given to each plant', ['Amount of fertiliser', 'Height of the plant', 'Number of leaves grown'], 'Water affects growth so must be kept the same.'),
           ('Which type of graph is used when the independent variable is categoric (e.g. type of material)?', 'Bar chart', ['Line graph', 'Scatter graph', 'Pie chart'], 'Categoric data have no numerical order.')],
    why=[('Explain why changing two variables at once makes an investigation invalid.', 'If two variables are changed together, you cannot tell which one caused the change in the dependent variable.'),
         ('Explain why a control experiment is useful in an investigation into the effect of a fertiliser.', 'Plants grown without fertiliser show what happens without the factor, so any difference can be linked to the fertiliser.'),
         ('Explain why some variables, such as the weather in a field study, cannot be controlled, and what scientists do about them.', 'They cannot be set by the investigator; scientists monitor and record them, use large samples and repeat over time to reduce their effect.')],
    contrast=[('the independent variable', 'the dependent variable', 'The independent variable is what you change on purpose; the dependent variable is what you measure in response.'),
              ('a control variable', 'a control experiment', 'A control variable is a factor kept the same in every trial; a control experiment is a separate set-up without the factor being tested, used for comparison.'),
              ('continuous variables', 'categoric variables', 'Continuous variables have numerical values that can take any value (temperature, mass); categoric variables are names or groups (type of metal, colour).')],
    misc=[('The dependent variable is the one you control.', 'You change the independent variable; you measure the dependent variable; control variables are kept the same.'),
          ('A fair test means doing the experiment only once so nothing changes.', 'A fair test changes only the independent variable; repeating trials improves reliability.')],
    evaluate=[('Laboratory experiments are always better than field studies.', ['variables can be controlled', 'easier to repeat'], ['lab conditions may not reflect real life (e.g. animals behave differently)', 'some questions can only be studied in the field (ecosystems, weather)'], 'Each has strengths; labs give control, field studies give realism, and many investigations use both.'),
              ('Clinical drug trials should always include a control group given a placebo.', ['shows whether improvement is due to the drug or to expectation (placebo effect)', 'makes the comparison fair'], ['withholding treatment from very ill patients is unethical when an effective treatment exists – then the new drug is compared with the existing one'], 'Control groups are essential, but ethics decide whether they receive a placebo or the current best treatment.')],
    extended=[('A student investigates whether the type of surface affects how far a toy car rolls after leaving a ramp. Identify the independent variable, the dependent variable and three control variables, and state which type of graph should be drawn, with a reason.', 'IV: type of surface (categoric); DV: distance rolled (cm) measured with a tape measure; controls: ramp height, the same car, release from the same point without pushing (also ramp angle, length). Bar chart, because the IV is categoric.', 5)],
))


@R.add('ch01-st2', 'C3', (1, 4), 'short')
def name_vars(rng, slot):
    ctx, iv, dv, cv = rng.choice([
        ('how the number of coils in an electromagnet affects the number of paper clips it picks up', 'number of coils', 'number of paper clips picked up', 'current, the same nail core, the same type of clip'),
        ('how the length of a pendulum affects the time for 10 swings', 'length of the pendulum', 'time for 10 swings', 'mass of the bob, starting angle, the same timer'),
        ('how the concentration of salt water affects the mass change of potato chips', 'salt concentration', 'change in mass of the chips', 'size of chips, time in solution, volume of solution, temperature'),
        ('how the colour of light affects the rate of bubbling of pondweed', 'colour of light', 'number of bubbles per minute', 'light intensity, distance from lamp, temperature, the same piece of pondweed'),
        ('how the mass of a parachute’s load affects its falling time', 'mass of the load', 'time to fall to the floor', 'drop height, canopy size and material, string length'),
        ('how the type of insulation around a beaker affects how fast hot water cools', 'type of insulating material', 'temperature drop in 10 minutes', 'starting temperature, volume of water, thickness of insulation, room temperature'),
        ('how the surface area of a tablet affects how quickly it fizzes away in water', 'surface area of the tablet (whole, halves, quarters, powder)', 'time to stop fizzing', 'volume and temperature of water, brand of tablet')])
    who = name(rng)
    return dict(stem=f'{who} is investigating {ctx}. State the independent variable, the dependent variable and two control variables.',
                answer=f'IV: {iv}; DV: {dv}; controls: {cv}', markingKey=f'1 IV {iv}; 1 DV {dv}; 1-2 any two valid controls from: {cv}.', marks=4, gap='G4')


inquiry('ch01-st2',
        dict(ctx='how the length of a pendulum affects the time for one complete swing',
             iv='length of the pendulum string (cm)', dv='time period – time for 10 swings measured with a stopwatch, divided by 10',
             cvs=[('mass of the pendulum bob', 'keeps the test fair even if mass has little effect'), ('starting angle (e.g. 10°)', 'large angles change the period slightly'), ('the same stopwatch and person timing', 'reaction times differ'), ('a draught-free room', 'air movement can disturb the swing')],
             hyp='If the length increases, then the time for one swing will increase, because the bob has further to travel along a wider arc.',
             method='Hang a 50 g bob from a clamp; set length to 20 cm measured to the centre of the bob; pull to 10° using a protractor; release and time 10 swings; divide by 10; repeat three times; repeat for 40, 60, 80, 100 cm; plot period against length.',
             weak=('only one swing was timed each time', 'time 10 swings and divide by 10 so that reaction-time error is a much smaller fraction of the time'),
             safety='clamp the stand firmly so it does not topple'))
dataset('ch01-st2',
        dict(intro='{who} measured the time for 10 swings of a pendulum of different lengths and calculated the period of one swing.', iv=('Length', 'cm'), xs=[20, 40, 60, 80, 100],
             dv=('Period', 's'), f=lambda x: 2 * math.pi * math.sqrt(x / 100 / 9.8), dp=2, trend='The period increases as the length increases, but not in direct proportion – quadrupling the length doubles the period.',
             why='A longer pendulum swings through a longer arc; the period is proportional to the square root of the length.'))

R.facts('ch01-st3', F(
    terms=[('SI unit', 'an internationally agreed standard unit, e.g. metre (m), kilogram (kg), second (s), kelvin (K)'),
           ('meniscus', 'the curved surface of a liquid in a measuring cylinder; read at the bottom of the curve for water'),
           ('hazard symbol', 'an internationally recognised (GHS) pictogram warning of a danger, e.g. flammable, corrosive, toxic'),
           ('risk assessment', 'identifying hazards in an investigation, how likely and serious harm is, and the precautions to reduce the risk'),
           ('resolution', 'the smallest change an instrument can measure, e.g. 1 mm on a ruler')],
    facts=[('What is the SI unit of mass?', 'Kilogram (kg)', ['Gram (g)', 'Newton (N)', 'Litre (L)'], 'The kilogram is the base SI unit of mass.'),
           ('Which piece of apparatus measures 25 cm³ of liquid most accurately?', 'A 25 cm³ pipette', ['A 250 cm³ beaker', 'A 100 cm³ measuring cylinder', 'A conical flask'], 'Pipettes are calibrated to one volume.'),
           ('How should a Bunsen burner flame be left when it is not being used?', 'On the yellow safety flame', ['On the blue roaring flame', 'Turned off with gas still on', 'Covered with paper'], 'The yellow flame is easy to see.'),
           ('How many cm³ are in 1 dm³ (1 litre)?', '1000', ['100', '10', '1 000 000'], '1 dm = 10 cm, so 1 dm³ = 1000 cm³.'),
           ('What does the GHS pictogram of a flame mean?', 'Flammable', ['Corrosive', 'Toxic', 'Harmful to the environment'], 'Keep away from naked flames.')],
    why=[('Explain why you should read a measuring cylinder at eye level.', 'Looking from above or below causes parallax error, making the reading seem too high or too low.'),
         ('Explain why scientists around the world use SI units.', 'A common system means results can be compared and repeated anywhere, avoiding errors from converting between units (e.g. the 1999 Mars Climate Orbiter loss).'),
         ('Explain why eye protection must be worn when heating liquids.', 'Liquids can spit or boil over suddenly, and hot or corrosive liquid in the eye can cause serious injury.')],
    contrast=[('accuracy', 'precision', 'Accurate measurements are close to the true value; precise measurements are close to each other (small spread) but could all be wrong.'),
              ('a hazard', 'a risk', 'A hazard is something that could cause harm (e.g. hot water); a risk is the chance of harm happening and how serious it would be.')],
    misc=[('A beaker is the best apparatus for measuring 37 cm³ of water.', 'Beakers have rough scales; a 50 cm³ measuring cylinder (or burette) gives a much more accurate volume.'),
          ('Water in a measuring cylinder should be read at the top of the curved surface.', 'Read at the bottom of the meniscus, at eye level.')],
    cases=[('the loss of NASA’s Mars Climate Orbiter (1999)', 'One team used imperial units (pound-force seconds) and another used SI units (newton seconds); the spacecraft entered the atmosphere too low and was destroyed.', 'the importance of SI units', 'Mixing unit systems caused a calculation error worth US$125 million – using one agreed system avoids this.')],
    evaluate=[('School science should only use computer simulations to avoid laboratory hazards.', ['no risk of burns, cuts or chemical injury', 'cheaper and no waste'], ['students do not learn practical and safety skills', 'real experiments show real errors and surprises', 'hazards can be managed by risk assessment'], 'Simulations are useful, but managed hands-on practical work is essential for learning science.')],
    extended=[('Write a risk assessment for heating copper(II) sulfate solution in an evaporating basin over a Bunsen burner. Include three hazards, the risk from each and a precaution for each.', 'Hot apparatus/liquid – burns or scalds – use tongs, heat-proof mat, let cool; spitting solution – eye injury – wear eye protection, stop heating when crystals start to form; copper(II) sulfate is harmful/irritant – skin and eye irritation, harmful if swallowed – gloves, wash hands; Bunsen flame – hair or clothing catching fire – tie hair back, use safety flame when not heating.', 6, 'long')],
))


@R.add('ch01-st3', 'C3', (1, 5), 'numerical')
def units(rng, slot):
    k = rng.choice(['mass', 'vol', 'len', 'time', 'temp', 'mean'] if slot.d >= 3 else ['mass', 'vol', 'len', 'time'])
    if k == 'mass':
        v = rng.choice([250, 1250, 75, 4500, 32])
        return dict(stem=f'Convert {v} g into kilograms.', answer=f'{v / 1000:g} kg', markingKey=f'1000 g = 1 kg, so {v} ÷ 1000 = {v / 1000:g} kg (1).', marks=1)
    if k == 'vol':
        v = rng.choice([0.25, 1.5, 2.0, 0.075, 3.2])
        return dict(stem=f'A bottle holds {v} dm³ of water. How many cm³ is this?', answer=f'{v * 1000:g} cm³', markingKey=f'1 dm³ = 1000 cm³, so {v} × 1000 = {v * 1000:g} cm³ (1).', marks=1)
    if k == 'len':
        v = rng.choice([35, 128, 7, 250, 1650])
        return dict(stem=f'Convert {v} mm into (a) centimetres and (b) metres.', answer=f'(a) {v / 10:g} cm (b) {v / 1000:g} m', markingKey=f'(a) ÷ 10 = {v / 10:g} cm (1); (b) ÷ 1000 = {v / 1000:g} m (1).', marks=2)
    if k == 'time':
        mi, s = rng.randint(1, 9), rng.randint(5, 55)
        return dict(stem=f'A stopwatch shows {mi} min {s} s. Convert this time into seconds.', answer=f'{mi * 60 + s} s', markingKey=f'{mi} × 60 + {s} = {mi * 60 + s} s (1).', marks=1)
    if k == 'temp':
        c = rng.choice([-40, -10, 0, 25, 37, 100])
        return dict(stem=f'The SI unit of temperature is the kelvin. Convert {c} °C into kelvin (K = °C + 273).', answer=f'{c + 273} K', markingKey=f'{c} + 273 = {c + 273} K (1).', marks=1)
    vals = [round(rng.uniform(20, 30), 1) for _ in range(4)]
    m = sum(vals) / 4
    rngv = max(vals) - min(vals)
    who = name(rng)
    return dict(stem=f'{who} measured the volume of gas collected in four repeats: {", ".join(f"{v:.1f}" for v in vals)} cm³. Calculate the mean volume and the range of the results.',
                answer=f'mean {m:.2f} cm³; range {rngv:.1f} cm³', markingKey=f'M1 sum ÷ 4; A1 {m:.2f} cm³; A1 range {max(vals):.1f} − {min(vals):.1f} = {rngv:.1f} cm³.', marks=3)


@R.add('ch01-st3', 'C1', (1, 3), 'mcq')
def apparatus_mcq(rng, slot):
    task, right, wrong = rng.choice([
        ('measure the mass of a small rock', 'Top-pan balance', ['Newton meter only', 'Measuring cylinder', 'Thermometer']),
        ('measure the temperature of a liquid every 30 seconds', 'Thermometer (or temperature probe) and stopwatch', ['Balance and ruler', 'Ammeter and voltmeter', 'Measuring cylinder and beaker']),
        ('measure the volume of an irregular stone', 'Displacement in a measuring cylinder', ['Ruler only', 'Top-pan balance', 'Thermometer']),
        ('measure the force needed to pull a block', 'Newton meter (force meter)', ['Top-pan balance', 'Measuring cylinder', 'Voltmeter']),
        ('separate a solid from a liquid', 'Filter funnel and filter paper', ['Thermometer', 'Burette', 'Spatula only']),
        ('measure the diameter of a wire', 'Micrometer', ['Metre rule', 'Measuring tape', 'Beaker'])])
    return mcq(rng, f'Which apparatus would a student use to {task}?', right, wrong, f'{right} is designed for this measurement.')


inquiry('ch01-st3',
        dict(ctx='which type of measuring apparatus (beaker, measuring cylinder, burette) gives the most accurate measurement of 25 cm³ of water',
             iv='type of measuring apparatus', dv='mass of the water delivered, measured on a balance to 0.01 g (1.00 g = 1.00 cm³ of water)',
             cvs=[('temperature of the water', 'density changes slightly with temperature'), ('the same balance, zeroed', 'zero errors'), ('reading at eye level', 'parallax errors'), ('the same person measuring', 'different people read scales differently')],
             hyp='If a burette is used, then the measured volume will be closest to 25.00 cm³, because it has the finest scale divisions (0.1 cm³) and a narrow tube that makes small differences in level easy to see.',
             method='Measure 25 cm³ of water with each piece of apparatus and pour it into a beaker on a zeroed balance; record the mass; repeat five times for each; calculate the mean and the percentage difference from 25.00 g.',
             weak=('the mass of the beaker was included in the readings', 'zero (tare) the balance with the empty beaker before each measurement'),
             safety='mop up spills to avoid slipping; handle glass carefully'))
dataset('ch01-st3',
        dict(intro='{who} measured the temperature of a beaker of water heated on a hot plate every 2 minutes, repeating the experiment three times.', iv=('Time', 'min'), xs=[2, 4, 6, 8, 10],
             dv=('Temperature', '°C'), f=lambda x: 20 + 6 * x, dp=1, trend='The temperature increases steadily with time, by roughly the same amount every 2 minutes.',
             why='The hot plate transfers energy to the water at a constant rate, so the temperature rises at a roughly constant rate.'))

R.facts('ch01-st4', F(
    terms=[('results table', 'a table with the independent variable in the first column and the dependent variable (with repeats and mean) in the next columns, with units in the headings'),
           ('line of best fit', 'a straight line or smooth curve drawn through the data points, with points evenly spread on either side'),
           ('anomalous result', 'a result that does not fit the pattern of the other results'),
           ('conclusion', 'a statement of what the results show, using the data, and whether they support the hypothesis'),
           ('directly proportional', 'a relationship where doubling one variable doubles the other; the graph is a straight line through the origin')],
    facts=[('Where should the units be written in a results table?', 'In the column headings', ['After every number', 'At the bottom of the table', 'Units are not needed'], 'e.g. "Time / s".'),
           ('Which variable is normally plotted on the x-axis?', 'The independent variable', ['The dependent variable', 'The control variable', 'The anomalous result'], 'The variable you change goes on the horizontal axis.'),
           ('What should you do with an anomalous result when calculating a mean?', 'Leave it out and, if possible, repeat the measurement', ['Double it', 'Include it twice', 'Change it to match the others'], 'Anomalies would distort the mean.'),
           ('A graph is a straight line through the origin. What does this show?', 'The two variables are directly proportional', ['There is no relationship', 'The relationship is inversely proportional', 'The data are anomalous'], 'y = kx.')],
    why=[('Explain why the mean of repeated readings is used instead of a single reading.', 'Random errors make individual readings vary; averaging several readings reduces the effect of random error and gives a more reliable value.'),
         ('Explain why scales on a graph should use more than half of the grid.', 'Larger scales make it easier to plot and read values accurately and to see the pattern.'),
         ('Explain why a conclusion should quote data from the results.', 'Quoting values provides evidence for the trend described, so the conclusion is supported rather than just stated.')],
    contrast=[('a bar chart', 'a line graph', 'A bar chart is used when the independent variable is categoric (types); a line graph is used when both variables are continuous numbers.'),
              ('a positive correlation', 'a negative correlation', 'In a positive correlation the dependent variable increases as the independent variable increases; in a negative correlation it decreases.')],
    misc=[('A line of best fit must go through every point, joining them dot to dot.', 'A line of best fit is a single smooth line or curve with points scattered evenly either side; it does not join dot to dot.'),
          ('Correlation always means one variable causes the other.', 'A correlation shows a link; a third factor may cause both (e.g. ice-cream sales and sunburn both rise in hot weather).')],
    evaluate=[('Graphs in news reports always represent data honestly.', ['graphs make data easy to understand quickly'], ['axes that do not start at zero can exaggerate changes', 'selecting time periods can hide trends', 'correlation may be presented as causation'], 'Graphs can mislead; readers should check axes, scales and sources before drawing conclusions.')],
    extended=[('A student’s table of results has no units, the repeats are not averaged and the independent variable is in the last column. Describe four improvements to the table and explain how each makes the data easier to use.', 'Put the IV in the first column (it is what was chosen); add units to headings, e.g. "Temperature / °C" (values have meaning); add a mean column and calculate means (reduces effect of random errors); use a consistent number of decimal places matching the instrument (shows precision); highlight/exclude anomalies.', 5)],
))


@R.add('ch01-st4', 'C3', (1, 5), 'numerical')
def gradient_read(rng, slot):
    k = rng.choice(['grad', 'interp', 'prop'] if slot.d >= 2 else ['interp'])
    if k == 'grad':
        m = rng.choice([0.5, 1.5, 2.0, 2.5, 4.0])
        x1, x2 = rng.choice([(1, 5), (2, 8), (0, 10), (3, 9)])
        c = rng.choice([0, 2, 5])
        y1, y2 = m * x1 + c, m * x2 + c
        return dict(stem=f'A straight-line graph of extension (cm, y-axis) against load (N, x-axis) passes through ({x1} N, {y1:g} cm) and ({x2} N, {y2:g} cm). Calculate the gradient and give its units.', answer=f'{m:g} cm/N',
                    markingKey=f'M1 gradient = change in y ÷ change in x = ({y2:g} − {y1:g}) ÷ ({x2} − {x1}); A1 {m:g} cm/N.', marks=2)
    if k == 'interp':
        m = rng.choice([3, 4, 5, 6])
        x = rng.choice([2.5, 3.5, 4.5])
        return dict(stem=f'A graph shows that the temperature of a liquid rises by {m} °C every minute, starting from 20 °C. Use the relationship to predict the temperature after {x} minutes.', answer=f'{20 + m * x:g} °C',
                    markingKey=f'M1 20 + {m} × {x}; A1 {20 + m * x:g} °C.', marks=2)
    a = rng.choice([2, 3, 4, 5])
    xs = [1, 2, 3, 4]
    ys = [a * x for x in xs]
    return dict(stem=f'A student’s results: x = {", ".join(map(str, xs))}; y = {", ".join(map(str, ys))}. Show that y is directly proportional to x and predict y when x = 7.', answer=f'y/x = {a} for every pair (and the line passes through the origin); y = {7 * a}',
                markingKey=f'1 ratio y/x constant = {a} (or doubling x doubles y); 1 straight line through origin; 1 y = {a} × 7 = {7 * a}.', marks=3)


inquiry('ch01-st4',
        dict(ctx='how the mass hung on a spring affects the extension of the spring',
             iv='mass hung on the spring (100 g to 600 g in 100 g steps)', dv='extension – new length minus original length, measured with a metre rule to the nearest mm',
             cvs=[('the same spring', 'springs differ in stiffness'), ('reading the ruler at eye level with a pointer', 'parallax error'), ('not exceeding the elastic limit', 'permanent stretching would change later readings'), ('the ruler fixed vertically', 'a tilted ruler gives wrong lengths')],
             hyp='If the mass increases, then the extension will increase in direct proportion (up to the elastic limit), because each extra 100 g adds the same extra force.',
             method='Hang a spring from a clamp next to a vertical metre rule; record the unstretched length with a pointer; add 100 g masses one at a time up to 600 g, recording the length each time; calculate extension; remove masses and repeat twice; plot extension against mass with a line of best fit.',
             weak=('the ruler was read from above', 'read the pointer at eye level to avoid parallax error'),
             safety='wear eye protection in case the spring snaps; put a tray under the masses'))
dataset('ch01-st4',
        dict(intro='{who} hung masses on a spring and measured its extension, repeating each reading three times.', iv=('Mass', 'g'), xs=[100, 200, 300, 400, 500],
             dv=('Extension', 'cm'), f=lambda x: 0.02 * x, dp=1, trend='Extension increases in direct proportion to the mass added – doubling the mass doubles the extension.',
             why='Each 100 g adds about 1 N of force; the spring obeys Hooke’s law (extension ∝ force) below its elastic limit.'))

R.facts('ch01-st5', F(
    terms=[('reliability', 'how consistent results are when an investigation is repeated'),
           ('validity', 'whether an investigation measures what it claims to measure, i.e. it is a fair test with controlled variables'),
           ('random error', 'unpredictable variation in readings that makes repeats differ; reduced by repeating and averaging'),
           ('systematic error', 'an error that makes every reading wrong by the same amount or in the same direction, e.g. a balance not zeroed'),
           ('zero error', 'when an instrument does not read zero when it should, causing a systematic error')],
    facts=[('A balance reads 0.3 g with nothing on it. What type of error is this?', 'Zero (systematic) error', ['Random error', 'Anomaly', 'Parallax error only'], 'Every reading will be 0.3 g too high.'),
           ('How can the reliability of results be improved?', 'Repeat the measurements and calculate a mean', ['Change more variables', 'Use fewer readings', 'Round all the numbers'], 'Consistency is checked by repeating.'),
           ('Which change would improve the validity of an investigation into the effect of temperature on enzyme activity?', 'Keeping the pH constant with a buffer', ['Taking readings faster', 'Using a different enzyme each time', 'Writing the results in pen'], 'pH also affects enzymes.')],
    why=[('Explain why repeating readings does not remove a systematic error.', 'A systematic error shifts every reading by the same amount, so the repeats agree with each other but are all wrong; the cause (e.g. zero error) must be corrected.'),
         ('Explain why using light gates improves the measurement of a short time interval compared with a stopwatch.', 'Human reaction time (about 0.2 s) is large compared with short times; light gates start and stop automatically, removing this random error.'),
         ('Explain why scientists ask other scientists to repeat their experiments.', 'If independent scientists get the same results with different equipment, the results are reproducible and more likely to be correct.')],
    contrast=[('reliability', 'validity', 'Reliability is how consistent repeated results are; validity is whether the investigation is a fair test that actually answers the question.'),
              ('random error', 'systematic error', 'Random errors make readings scatter unpredictably and are reduced by repeats; systematic errors shift all readings the same way and need the cause correcting.')],
    misc=[('If all my repeat readings are the same, my results must be accurate.', 'They are precise and repeatable, but a systematic error could make them all wrong; accuracy means close to the true value.'),
          ('Human error means I made a mistake, so it should be in every evaluation.', 'Evaluations should name the specific source of error (e.g. reaction time when using a stopwatch) and suggest a specific improvement.')],
    cases=[('the 1989 “cold fusion” claim by Fleischmann and Pons', 'They announced nuclear fusion at room temperature in a simple cell; laboratories around the world could not reproduce the results.', 'reproducibility and reliability', 'Because independent repeats failed, the scientific community rejected the claim – results must be reproducible to be accepted.')],
    evaluate=[('Results from a single, very careful experiment are enough to draw a firm conclusion.', ['careful technique reduces errors'], ['random errors and anomalies can only be detected by repeating', 'other scientists must reproduce results', 'a single sample may not be representative'], 'A single experiment gives limited evidence; repeats and reproduction by others are needed for a firm conclusion.')],
    extended=[('A student measured how the height a ball is dropped from affects its bounce height, using a metre rule held by hand and judging the top of each bounce by eye, with one drop per height. Evaluate the method, identifying two sources of error and suggesting a specific improvement for each.', 'Judging the bounce top by eye is difficult (random error, parallax) – film the bounce in slow motion against a fixed scale; one drop per height gives unreliable data – repeat 3-5 times and calculate means, identifying anomalies; ruler held by hand may move – clamp it vertically. The conclusion would then be more reliable and valid.', 6, 'long')],
))


@R.add('ch01-st5', 'C3', (1, 5), 'numerical')
def pct_error(rng, slot):
    k = rng.choice(['pct', 'zero', 'spread'])
    if k == 'pct':
        true, meas = rng.choice([(9.81, round(rng.uniform(9.2, 10.4), 2)), (100.0, round(rng.uniform(97, 103), 1)), (340, rng.randint(320, 360)), (1.00, round(rng.uniform(0.93, 1.07), 2))])
        if meas == true:
            return None
        p = abs(meas - true) / true * 100
        q = {9.81: 'g (in m/s²)', 100.0: 'the boiling point of water (°C)', 340: 'the speed of sound (m/s)', 1.00: 'the density of water (g/cm³)'}[true]
        return dict(stem=f'A class measured {q} as {meas}. The accepted value is {true}. Calculate the percentage difference.', answer=f'{p:.1f}%',
                    markingKey=f'M1 |{meas} − {true}| ÷ {true} × 100; A1 {p:.1f}%.', marks=2)
    if k == 'zero':
        z = rng.choice([0.2, 0.3, 0.5, 1.0])
        vals = [round(rng.uniform(10, 40), 1) for _ in range(3)]
        return dict(stem=f'A balance reads {z} g when empty. A student records masses of {", ".join(f"{v:.1f}" for v in vals)} g without noticing. (a) Name this type of error. (b) Give the correct masses.', answer=f'(a) zero (systematic) error (b) ' + ', '.join(f'{v - z:.1f}' for v in vals) + ' g',
                    markingKey=f'(a) 1 zero/systematic error. (b) 1-2 subtract {z} g from each reading.', marks=3)
    a = [round(rng.uniform(4.0, 5.0), 2) for _ in range(3)]
    b = [round(rng.uniform(4.0, 5.0) if i else 4.5, 2) for i in range(3)]
    b = [round(4.5 + rng.uniform(-0.05, 0.05), 2) for _ in range(3)]
    ra, rb = max(a) - min(a), max(b) - min(b)
    return dict(stem=f'Two students timed the same trolley run three times. Student A: {", ".join(f"{v:.2f}" for v in a)} s. Student B (using light gates): {", ".join(f"{v:.2f}" for v in b)} s. Calculate the range for each and explain which set is more reliable.',
                answer=f'A range {ra:.2f} s; B range {rb:.2f} s; ' + ('B is more reliable (smaller spread)' if rb < ra else 'A has the smaller spread here'), markingKey=f'1 range A {ra:.2f} s; 1 range B {rb:.2f} s; 1 smaller range = more consistent/reliable, light gates remove reaction-time error.', marks=3)


inquiry('ch01-st5',
        dict(ctx='how the method of timing (hand-held stopwatch or light gates) affects the reliability of measuring the time for a ball to roll down a 1.0 m ramp',
             iv='timing method (stopwatch or light gates)', dv='spread (range) of 10 repeat times for each method',
             cvs=[('ramp angle and length', 'changes the true time'), ('the same ball released from rest', 'pushing changes the time'), ('the same person using the stopwatch', 'reaction times differ'), ('the same start and finish positions', 'distance must be the same')],
             hyp='If light gates are used, then the range of repeat times will be smaller, because they remove the variation caused by human reaction time.',
             method='Set up a 1.0 m ramp at a fixed angle; release the ball from rest at the start line 10 times, timing each run with a stopwatch; repeat 10 runs with light gates at the start and finish lines; calculate mean and range for each method; compare.',
             safety='catch the ball at the end of the ramp; keep the floor clear'))
dataset('ch01-st5',
        dict(intro='{who} and three classmates each timed a ball rolling down the same ramp with stopwatches, three times each, while the ramp height was changed.', iv=('Ramp height', 'cm'), xs=[10, 20, 30, 40, 50],
             dv=('Time', 's'), f=lambda x: 3.2 / math.sqrt(x / 10), dp=2, trend='The time decreases as the ramp height increases, with smaller decreases at greater heights.',
             why='A higher ramp gives the ball more gravitational potential energy to convert to kinetic energy, so it moves faster; the spread of repeats shows random timing error.'))


# =============================================================================================
# ch02 Cells – The Basic Unit of Life
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('organism', 'a living thing that carries out all seven life processes'),
           ('excretion', 'removal of waste products of metabolism, such as carbon dioxide and urea, from an organism'),
           ('respiration', 'the chemical reaction in cells that releases energy from glucose'),
           ('sensitivity', 'the ability to detect and respond to changes in the surroundings'),
           ('nutrition', 'taking in or making food for energy, growth and repair')],
    facts=[('What does the “E” in MRS GREN stand for?', 'Excretion', ['Energy', 'Eating', 'Evolution'], 'Removing waste made by the body’s reactions.'),
           ('Which life process do plants carry out by photosynthesis?', 'Nutrition', ['Excretion', 'Movement', 'Reproduction'], 'Plants make their own food.'),
           ('A car moves, takes in fuel and gives out waste gases. Why is it not alive?', 'It cannot grow, reproduce or respond as living things do', ['It does not move', 'It does not use energy', 'It is made of metal only'], 'It must show all seven processes.'),
           ('Which life process releases energy from food in every living cell?', 'Respiration', ['Breathing', 'Excretion', 'Growth'], 'Breathing is just moving air in and out.')],
    why=[('Explain why a crystal growing in a solution is not a living thing.', 'It only grows by adding particles on the outside; it does not respire, excrete, take in nutrients, reproduce or respond to stimuli.'),
         ('Explain why plants are said to move even though they stay in one place.', 'Parts of plants move – leaves turn to face light, flowers open and close, roots grow towards water.'),
         ('Explain why excretion is necessary for living organisms.', 'Cell reactions produce waste substances such as carbon dioxide and urea that are toxic if they build up, so they must be removed.')],
    contrast=[('respiration', 'breathing', 'Respiration is a chemical reaction in cells that releases energy from glucose; breathing is the movement of air into and out of the lungs.'),
              ('excretion', 'egestion', 'Excretion removes waste made by metabolism (CO₂, urea); egestion removes undigested food (faeces) that was never absorbed into cells.')],
    misc=[('Plants do not respire; they only photosynthesise.', 'Plants respire all the time, day and night, in every living cell; they photosynthesise only in the light.'),
          ('Seeds are dead because they do not seem to do anything.', 'Dormant seeds are alive; they respire very slowly and will grow when conditions are right.')],
    cases=[('Viruses – alive or not?', 'Viruses contain genetic material and can reproduce, but only inside a host cell; they do not respire, grow or excrete on their own.', 'characteristics of life', 'Viruses show some but not all of MRS GREN, so many biologists do not class them as living.')],
    evaluate=[('Robots that can repair themselves should be classified as living things.', ['they can move, sense surroundings and use energy'], ['they do not respire, grow from cells or reproduce biologically', 'they are not made of cells'], 'Robots show some features of life but not all seven processes, so they are not living.'),
              ('Searching for life on Mars should focus on finding signs of the life processes rather than finding animals.', ['microbes are much more likely than animals', 'chemical signs of respiration or excretion (gases) can be detected remotely'], ['some gases can be made by non-living processes too'], 'Looking for evidence of life processes is the most realistic approach, but results must be checked against non-living explanations.')],
    extended=[('Use MRS GREN to explain how you could decide whether an unknown object found in pond water is living. Give four observations or tests you could make.', 'Watch for movement under a microscope; check for growth over days; test for respiration (gas exchange, e.g. CO₂ produced / O₂ used, temperature rise); look for reproduction (dividing cells); test sensitivity (response to light or touch); presence of cells. Living things must show all seven processes.', 5)],
))
inquiry('ch02-st1',
        dict(ctx='how temperature affects the rate of respiration of germinating peas',
             iv='temperature of the water bath (°C)', dv='distance moved by a coloured liquid drop in a respirometer in 10 minutes',
             cvs=[('mass of peas (10 g)', 'more peas respire more'), ('type and age of peas', 'different seeds respire at different rates'), ('amount of soda lime', 'it must absorb all the CO₂'), ('time allowed', 'longer time gives more movement')],
             hyp='If temperature increases up to about 35 °C, then the drop will move further, because enzymes controlling respiration work faster.',
             method='Place 10 g germinating peas in a respirometer tube with soda lime under gauze; stand the tube in a water bath at 15 °C; leave 5 min to equilibrate; record drop movement over 10 min; repeat at 20, 25, 30 and 35 °C; repeat three times; use boiled (dead) peas as a control.',
             weak=('no control tube was used', 'set up an identical tube with boiled peas or glass beads to show that living peas cause the movement'),
             safety='soda lime is corrosive – do not touch it with bare skin; wear eye protection'))
dataset('ch02-st1',
        dict(intro='{who} measured the volume of carbon dioxide given off by 20 g of germinating seeds in 30 minutes at different temperatures.', iv=('Temperature', '°C'), xs=[10, 15, 20, 25, 30],
             dv=('Volume of CO₂', 'cm³'), f=lambda x: 0.6 * x + 1.5, dp=1, trend='The volume of carbon dioxide released increases as temperature increases.',
             why='Respiration is controlled by enzymes, which work faster as temperature rises (up to an optimum), so more glucose is respired.'))

R.facts('ch02-st2', F(
    terms=[('nucleus', 'the part of the cell that contains genetic material and controls the cell’s activities'),
           ('cell membrane', 'the thin layer around a cell that controls what enters and leaves'),
           ('cytoplasm', 'the jelly-like substance where most chemical reactions in the cell happen'),
           ('mitochondria', 'organelles where aerobic respiration takes place, releasing energy'),
           ('chloroplast', 'organelle containing chlorophyll that absorbs light for photosynthesis'),
           ('cell wall', 'a strong layer made of cellulose outside the membrane of plant cells that supports the cell'),
           ('vacuole', 'a large permanent space in plant cells filled with cell sap that keeps the cell firm')],
    facts=[('Which structure is found in plant cells but not in animal cells?', 'Cell wall', ['Cell membrane', 'Nucleus', 'Mitochondria'], 'Made of cellulose.'),
           ('Which structures are found in both plant and animal cells?', 'Nucleus, cytoplasm, cell membrane and mitochondria', ['Chloroplasts and cell wall', 'Vacuole and chloroplasts', 'Cell wall and nucleus only'], 'These are common to both.'),
           ('Root cells of a plant have no chloroplasts. Why?', 'They receive no light, so they cannot photosynthesise', ['They are animal cells', 'They contain too much water', 'They have no nucleus'], 'Chloroplasts would be useless underground.'),
           ('Which organelle releases energy by aerobic respiration?', 'Mitochondrion', ['Nucleus', 'Vacuole', 'Cell wall'], 'Cells that need much energy have many mitochondria.'),
           ('Which organelle is where proteins are made?', 'Ribosome', ['Vacuole', 'Chloroplast', 'Cell wall'], 'Ribosomes are tiny and found in the cytoplasm.')],
    why=[('Explain why muscle cells contain many mitochondria.', 'Muscle cells contract and need a lot of energy; mitochondria carry out aerobic respiration that releases this energy.'),
         ('Explain why plant cells keep their shape even without a skeleton.', 'The cellulose cell wall is rigid, and the full vacuole pushes the cytoplasm against the wall, making the cell firm (turgid).'),
         ('Explain why the nucleus is described as the control centre of the cell.', 'It contains DNA carrying the instructions for making proteins, which control the cell’s activities and characteristics.')],
    contrast=[('the cell wall', 'the cell membrane', 'The cell wall is a rigid cellulose layer outside plant cells that gives support and is fully permeable; the cell membrane is a thin flexible layer in all cells that controls which substances pass in and out.'),
              ('a plant cell', 'an animal cell', 'Plant cells have a cellulose cell wall, a large permanent vacuole and (in leaves) chloroplasts; animal cells have none of these and are usually irregular in shape.')],
    misc=[('All plant cells contain chloroplasts.', 'Only cells exposed to light, such as leaf and stem cells, contain chloroplasts; root cells do not.'),
          ('The cell wall controls what enters and leaves the cell.', 'The cell membrane controls what enters and leaves; the cell wall is fully permeable and gives support.')],
    cases=[('Robert Hooke’s cork cells (1665)', 'Hooke looked at thin slices of cork with an early microscope and saw tiny box-like spaces he called “cells”.', 'discovery of cells', 'It was the first description of cells and began cell biology; he actually saw the empty cell walls of dead plant cells.'),
           ('Cell theory (Schleiden and Schwann, 1838–39)', 'Schleiden concluded that all plants are made of cells and Schwann that animals are too; Virchow later added that cells come from existing cells.', 'cell theory', 'Cell theory unified biology: the cell is the basic unit of all living things.')],
    evaluate=[('Learning cell structure from 3D computer models is better than looking at real cells under a microscope.', ['models show organelles too small for a light microscope', 'can be rotated and labelled'], ['real cells show the variety and real appearance', 'microscope skills are needed for investigations'], 'Models help understanding, but real observation builds practical skills; both are useful.')],
    extended=[('Compare the structures found in a palisade leaf cell and a cheek cell, and explain how the differences relate to what each cell does.', 'Both: nucleus, cytoplasm, cell membrane, mitochondria, ribosomes. Palisade only: cellulose cell wall (support), large vacuole (turgidity), many chloroplasts (absorb light for photosynthesis – the leaf’s job). Cheek cell has none of these: it does not photosynthesise and is protected by surrounding tissues; it lines the mouth.', 6)],
))


@R.add('ch02-st2', 'C1', (1, 2), 'mcq')
def organelle_job(rng, slot):
    items = [('nucleus', 'contains genetic material and controls the cell'), ('mitochondrion', 'carries out aerobic respiration'),
             ('chloroplast', 'absorbs light for photosynthesis'), ('cell wall', 'supports and strengthens the plant cell'),
             ('cell membrane', 'controls what enters and leaves the cell'), ('ribosome', 'makes proteins'),
             ('permanent vacuole', 'stores cell sap and keeps the cell turgid')]
    o, j = rng.choice(items)
    return mcq(rng, f'What is the job of the {o}?', j, rng.sample([b for a, b in items if a != o], 3), 'B1 ' + j)


inquiry('ch02-st2',
        dict(ctx='whether onion cells from different layers of the bulb contain the same structures',
             iv='layer of the onion bulb (outer, middle, inner)', dv='presence and number of visible cell structures (nucleus, cell wall, vacuole) per field of view',
             cvs=[('stain used (iodine)', 'different stains show different structures'), ('magnification (×100 and ×400)', 'more detail is visible at higher magnification'), ('thickness of the epidermis peel (one layer)', 'thick layers overlap cells'), ('the same microscope', 'resolution may differ')],
             hyp='If cells from each layer are compared, then all will show a cell wall, nucleus and vacuole but no chloroplasts, because onion bulb cells are underground storage cells that receive no light.',
             method='Peel a thin layer of epidermis from each onion layer with forceps; lay it flat in a drop of iodine on a slide; lower a coverslip at an angle to avoid air bubbles; observe at ×100 then ×400; count cells with a visible nucleus in three fields of view; draw labelled diagrams.',
             weak=('air bubbles under the coverslip hid many cells', 'lower the coverslip slowly at an angle using a mounted needle'),
             safety='iodine stains and irritates – wear eye protection; take care with sharp forceps and glass slides'))
dataset('ch02-st2',
        dict(intro='{who} counted the number of chloroplasts in cells at different distances below the upper surface of a leaf, three cells at each depth.', iv=('Depth below surface', 'µm'), xs=[50, 100, 150, 200, 250],
             dv=('Chloroplasts per cell', ''), f=lambda x: 60 - 0.2 * x, dp=0, trend='The number of chloroplasts per cell decreases with depth below the upper surface.',
             why='Cells near the upper surface (palisade cells) receive the most light, so having more chloroplasts there allows more photosynthesis.'))

R.facts('ch02-st3', F(
    terms=[('magnification', 'how many times larger an image is than the real object'),
           ('resolution', 'the ability to distinguish two points close together as separate'),
           ('objective lens', 'the lens nearest the specimen, usually ×4, ×10 or ×40'),
           ('eyepiece lens', 'the lens you look through, usually ×10'),
           ('coarse focus', 'the large knob that moves the stage a long way to bring the image roughly into focus'),
           ('micrometre (µm)', 'one thousandth of a millimetre, the unit used to measure cells')],
    facts=[('An eyepiece is ×10 and the objective is ×40. What is the total magnification?', '×400', ['×50', '×30', '×4'], 'Multiply the two.'),
           ('Which lens should you start with when focusing a slide?', 'The lowest power objective', ['The highest power objective', 'Any lens', 'The ×40 lens only'], 'It is easier to find the specimen.'),
           ('Why is a specimen stained before viewing?', 'To make structures such as the nucleus easier to see', ['To kill bacteria', 'To make the cells bigger', 'To stop the slide breaking'], 'Most cell parts are colourless.'),
           ('How many micrometres are in 1 mm?', '1000', ['100', '10', '10 000'], '1 µm = 0.001 mm.'),
           ('Why should you not use the coarse focus with the ×40 objective?', 'The objective could hit and break the slide', ['The image becomes coloured', 'The lamp switches off', 'It changes the magnification'], 'Use the fine focus at high power.')],
    why=[('Explain why light microscopes cannot show ribosomes even at the highest magnification.', 'Ribosomes are smaller than the resolution limit of light (about 0.2 µm), so they cannot be distinguished; an electron microscope is needed.'),
         ('Explain why a specimen must be thin to be seen with a light microscope.', 'Light must pass through the specimen to reach the lenses; thick specimens block light and layers of cells overlap.'),
         ('Explain why you see fewer cells when you switch from the ×10 to the ×40 objective.', 'Higher magnification makes each cell look bigger, so a smaller area of the slide fits in the field of view.')],
    contrast=[('magnification', 'resolution', 'Magnification is how much bigger the image is; resolution is how much detail can be seen – magnifying without better resolution just gives a bigger blurred image.'),
              ('the coarse focus', 'the fine focus', 'The coarse focus moves the stage a long way to find the image at low power; the fine focus moves it a tiny amount to sharpen the image, especially at high power.')],
    misc=[('Using a higher magnification always shows more detail.', 'Above the limit of resolution, more magnification only makes a blurred image bigger.'),
          ('Image size and actual size are the same thing at ×1.', 'At ×1 they are the same, but magnification = image size ÷ actual size, so at any other magnification they differ.')],
    cases=[('Antonie van Leeuwenhoek (1670s)', 'A Dutch cloth merchant ground tiny single lenses magnifying about ×270 and saw bacteria, sperm cells and protists, which he called “animalcules”.', 'microscope technology', 'Better lenses revealed a whole world of single-celled organisms for the first time.')],
    evaluate=[('Every school should have electron microscopes rather than light microscopes.', ['much higher magnification and resolution', 'shows organelles'], ['extremely expensive and large', 'specimens must be dead and in a vacuum', 'light microscopes show living cells and colour'], 'Light microscopes are better value and suitable for school work; electron microscopes are for research.')],
    extended=[('Describe how to prepare a slide of onion epidermis cells and use a light microscope to produce a scientific drawing with a scale. Include magnification.', 'Peel thin epidermis; place flat in a drop of iodine on a slide; lower coverslip at an angle (no bubbles); place on stage, lowest objective; focus with coarse then fine focus; switch to higher objective, fine focus only; draw clear pencil outlines without shading, label with ruled lines; state total magnification = eyepiece × objective, and add a scale bar or actual size calculated from image size ÷ magnification.', 6)],
))


@R.add('ch02-st3', 'C3', (1, 5), 'numerical')
def magnification(rng, slot):
    k = rng.choice(['total', 'M', 'actual', 'image'] if slot.d >= 2 else ['total', 'M'])
    if k == 'total':
        e = rng.choice([5, 10, 15])
        o = rng.choice([4, 10, 40, 100])
        return dict(stem=f'A microscope has a ×{e} eyepiece and a ×{o} objective lens. Calculate the total magnification.', answer=f'×{e * o}',
                    markingKey=f'M1 eyepiece × objective = {e} × {o}; A1 ×{e * o}.', marks=2)
    cell, um = rng.choice([('red blood cell', 8), ('cheek cell', 60), ('onion epidermis cell', 250), ('pollen grain', 30), ('palisade cell', 80), ('yeast cell', 5)])
    M = rng.choice([100, 200, 400, 500, 1000])
    img_mm = um * M / 1000
    if k == 'M':
        return dict(stem=f'A {cell} is {um} µm wide. In a drawing its image is {g(img_mm)} mm wide. Calculate the magnification of the drawing.', answer=f'×{M}',
                    markingKey=f'M1 convert {g(img_mm)} mm = {g(img_mm * 1000)} µm; M1 magnification = image ÷ actual = {g(img_mm * 1000)} ÷ {um}; A1 ×{M}.', marks=3)
    if k == 'actual':
        return dict(stem=f'A photograph of a {cell} at a magnification of ×{M} shows the cell {g(img_mm)} mm wide. Calculate the actual width of the cell in micrometres.', answer=f'{um} µm',
                    markingKey=f'M1 actual = image ÷ magnification = {g(img_mm)} ÷ {M} = {g(img_mm / M)} mm; M1 × 1000 to convert to µm; A1 {um} µm.', marks=3)
    return dict(stem=f'A {cell} is {um} µm wide. How wide, in mm, will its image be at a magnification of ×{M}?', answer=f'{g(img_mm)} mm',
                markingKey=f'M1 image = actual × magnification = {um} × {M} = {g(um * M)} µm; M1 ÷ 1000; A1 {g(img_mm)} mm.', marks=3)


inquiry('ch02-st3',
        dict(ctx='how the magnification of the objective lens affects the number of cells visible in the field of view',
             iv='objective lens magnification (×4, ×10, ×40)', dv='number of whole cells counted in the field of view',
             cvs=[('the same slide and area of specimen', 'cell density varies across a slide'), ('the same eyepiece (×10)', 'it also changes magnification'), ('counting rule for cells cut by the edge', 'counts must be consistent'), ('light intensity', 'cells may be harder to see')],
             hyp='If the objective magnification increases, then fewer cells will be visible, because each cell appears larger so a smaller area of the specimen fits in the field of view.',
             method='Place a stained onion slide on the stage; with the ×4 objective, focus and count all whole cells in view; without moving the slide, switch to ×10 and refocus with fine focus, count again; repeat for ×40; move to two other areas and repeat; calculate means.',
             weak=('the slide was moved between counts', 'keep the slide clamped in the same place and only change the objective'),
             safety='carry the microscope with two hands; never use direct sunlight with a mirror – it can damage eyes'))
dataset('ch02-st3',
        dict(intro='{who} measured the width of the image of the same pollen grain at different magnifications (three measurements each).', iv=('Magnification', '×'), xs=[40, 100, 200, 400, 600],
             dv=('Image width', 'mm'), f=lambda x: 0.03 * x, dp=1, trend='The image width increases in direct proportion to the magnification.',
             why='Magnification = image size ÷ actual size; the actual size of the grain is constant (about 30 µm), so image size is proportional to magnification.'))

R.facts('ch02-st4', F(
    terms=[('specialised cell', 'a cell with structures adapted to carry out a particular function'),
           ('tissue', 'a group of similar cells working together to carry out a function'),
           ('organ', 'a group of different tissues working together to carry out a function'),
           ('organ system', 'a group of organs working together to perform a major function'),
           ('differentiation', 'the process by which a cell becomes specialised')],
    facts=[('Which is the correct order of organisation, from smallest to largest?', 'cell → tissue → organ → organ system → organism', ['tissue → cell → organ → organism → organ system', 'organ → tissue → cell → organism → organ system', 'cell → organ → tissue → organ system → organism'], 'Each level is made of the one before.'),
           ('Why does a sperm cell have a tail?', 'To swim to the egg', ['To store food', 'To absorb water', 'To carry oxygen'], 'Many mitochondria power it.'),
           ('Why do red blood cells have no nucleus?', 'To make more space for haemoglobin to carry oxygen', ['To help them divide', 'To store more glucose', 'To fight infection'], 'They are also biconcave.'),
           ('Which plant cell has a long extension to absorb water from soil?', 'Root hair cell', ['Palisade cell', 'Guard cell', 'Xylem vessel'], 'Large surface area.'),
           ('The heart is an example of which level of organisation?', 'Organ', ['Tissue', 'Cell', 'Organ system'], 'It contains muscle, nervous and connective tissue.')],
    why=[('Explain how a nerve cell is adapted to its function.', 'It is very long to carry impulses over long distances, and has many branched endings to connect with many other cells.'),
         ('Explain why a palisade cell has many chloroplasts and is found near the top of the leaf.', 'It is where most light falls, and many chloroplasts absorb more light energy for photosynthesis.'),
         ('Explain why multicellular organisms need specialised cells.', 'Large organisms have many jobs to do; dividing labour between specialised cells lets each carry out its job efficiently.')],
    contrast=[('a tissue', 'an organ', 'A tissue is a group of similar cells with the same function; an organ is made of several different tissues working together.'),
              ('a root hair cell', 'a palisade cell', 'A root hair cell has a long extension and no chloroplasts, to absorb water and minerals; a palisade cell is column-shaped with many chloroplasts, to photosynthesise.')],
    misc=[('All the cells in the body are the same.', 'Cells differentiate into many types – nerve, muscle, blood, bone – each with a shape and structures suited to its job.'),
          ('An organ is made of only one type of cell.', 'Organs contain several tissues, e.g. the stomach has muscle, glandular and lining tissue.')],
    cases=[('Ciliated cells and smoking', 'Cells lining the airways have tiny hairs (cilia) that sweep mucus and trapped dirt up out of the lungs; chemicals in cigarette smoke paralyse and destroy cilia.', 'specialised cells', 'Without working cilia, mucus builds up, causing “smoker’s cough” and more chest infections.')],
    evaluate=[('Lab-grown organs from a patient’s own cells will soon end the need for organ donors.', ['no rejection because the cells are the patient’s own', 'no waiting lists'], ['organs have many tissues and blood vessels that are very hard to grow', 'still experimental and expensive'], 'Lab-grown tissues are promising, but complex organs are years away, so donation remains essential.'),
              ('Specialised cells are more useful to an organism than unspecialised cells.', ['each does its job efficiently'], ['unspecialised (stem) cells are needed for growth and repair', 'specialised cells usually cannot divide or change job'], 'Organisms need both: specialised cells for function and unspecialised cells to replace them.')],
    extended=[('Choose three specialised cells (one plant, two animal). For each, describe one adaptation and explain how it helps the cell carry out its function.', 'e.g. Root hair cell: long projection gives large surface area for absorbing water and minerals. Red blood cell: no nucleus and biconcave shape – more haemoglobin and larger surface for oxygen. Sperm cell: tail to swim, many mitochondria for energy, acrosome with enzymes to digest egg membrane. Nerve cell: long axon carries impulses over distance.', 6)],
))
inquiry('ch02-st4',
        dict(ctx='how the length of root hair zone affects water uptake by cress seedlings',
             iv='age of the seedlings (2, 4, 6, 8 days), giving different lengths of root hair zone', dv='volume of water taken up in 24 hours – measured from a graduated tube',
             cvs=[('number of seedlings (20)', 'more seedlings take up more water'), ('temperature', 'affects evaporation from leaves'), ('light intensity', 'affects transpiration'), ('the same variety of cress', 'varieties differ')],
             hyp='If the seedlings are older, then more water will be taken up, because they have more root hair cells giving a larger surface area for absorption.',
             method='Grow cress on damp paper for 2, 4, 6 and 8 days; place 20 seedlings from each batch with roots in 10 cm³ water in a graduated tube sealed with cling film; keep at the same temperature and light for 24 h; record the volume lost; repeat three times; examine root hairs under a hand lens.',
             weak=('water also evaporated from the open tubes', 'seal the surface with a layer of oil and include a tube with no seedlings as a control'),
             safety='wash hands after handling seeds and soil; wipe up spills'))
dataset('ch02-st4',
        dict(intro='{who} counted the number of mitochondria in sections of different cells from a mouse, three sections per cell type, then ranked cells by how active they are.', iv=('Activity score', ''), xs=[1, 2, 3, 4, 5],
             dv=('Mitochondria per cell', ''), f=lambda x: 150 * x + 100, dp=0, trend='The more active the cell, the more mitochondria it contains.',
             why='Active cells (e.g. muscle and sperm cells) need more energy; mitochondria carry out aerobic respiration, which releases that energy.'))

R.facts('ch02-st5', F(
    terms=[('diffusion', 'the net movement of particles from a region of higher concentration to a region of lower concentration'),
           ('osmosis', 'the net movement of water molecules from a dilute solution to a more concentrated solution through a partially permeable membrane'),
           ('partially permeable membrane', 'a membrane that lets small molecules such as water through but not larger ones such as sugar'),
           ('concentration gradient', 'the difference in concentration between two regions'),
           ('turgid', 'describes a plant cell that is swollen and firm because it is full of water'),
           ('plasmolysed', 'describes a plant cell that has lost so much water that the cytoplasm pulls away from the cell wall')],
    facts=[('In which direction does oxygen diffuse between the air in the lungs and the blood?', 'From the air in the alveoli into the blood', ['From the blood into the alveoli', 'It does not move', 'Equally in both directions'], 'Higher concentration in the alveoli.'),
           ('What happens to a potato chip placed in a very concentrated sugar solution?', 'It loses water and mass by osmosis and becomes soft', ['It gains water and becomes firm', 'Its mass stays the same', 'It dissolves'], 'Water moves out to the more concentrated solution.'),
           ('Which change makes diffusion faster?', 'Increasing the temperature', ['Decreasing the concentration difference', 'Making the membrane thicker', 'Reducing the surface area'], 'Particles move faster.'),
           ('What happens to a red blood cell placed in pure water?', 'It swells and bursts', ['It shrinks', 'It stays the same', 'It becomes plasmolysed'], 'Animal cells have no cell wall.'),
           ('Which substance diffuses out of a respiring cell?', 'Carbon dioxide', ['Oxygen', 'Glucose', 'Starch'], 'It is made in the cell so is more concentrated there.')],
    why=[('Explain why a drop of ink spreads through still water without stirring.', 'Ink and water particles move randomly; the ink particles spread from where they are concentrated to where they are dilute until evenly mixed – diffusion.'),
         ('Explain why plants wilt when they are not watered.', 'Cells lose water by osmosis and evaporation; vacuoles shrink and cells become flaccid, so they no longer press against cell walls to support the plant.'),
         ('Explain why salt sprinkled on a slug harms it.', 'The concentrated salt solution on its skin draws water out of its cells by osmosis, dehydrating it.')],
    contrast=[('diffusion', 'osmosis', 'Diffusion is the net movement of any particles down a concentration gradient; osmosis is the diffusion of water only, across a partially permeable membrane.'),
              ('a turgid cell', 'a plasmolysed cell', 'A turgid cell is full of water and presses on its cell wall; a plasmolysed cell has lost water so the membrane pulls away from the wall.')],
    misc=[('Particles stop moving when diffusion is complete.', 'Particles keep moving randomly; there is just no net movement because concentration is equal everywhere.'),
          ('In osmosis, sugar moves across the membrane to balance concentrations.', 'Only water moves through the partially permeable membrane; sugar molecules are too large.')],
    cases=[('Oral rehydration therapy', 'A cheap drink of water with exact amounts of salt and glucose is used to treat dehydration from diarrhoea; glucose helps the gut absorb salt, and water follows by osmosis.', 'osmosis in medicine', 'ORT is estimated to have saved tens of millions of children’s lives, especially where cholera is common.')],
    evaluate=[('Salting meat and fish is a good way to preserve food.', ['salt draws water out of bacteria by osmosis so they cannot grow', 'cheap, no fridge needed'], ['high-salt diets raise blood pressure', 'changes taste and texture'], 'Salting is effective and useful where refrigeration is limited, but salty food should be eaten in moderation.')],
    extended=[('Describe an experiment using potato cylinders to find the concentration of sugar solution that is equal to the concentration inside potato cells. Explain how the results are processed.', 'Cut equal cylinders with a cork borer, blot and weigh; place in 0, 0.2, 0.4, 0.6, 0.8, 1.0 mol/dm³ sucrose for the same time and temperature; blot and reweigh; calculate % change in mass = (final − initial) ÷ initial × 100; plot % change against concentration; where the line crosses 0% change, there is no net osmosis – this is the concentration of the cell sap. Repeat three times and average.', 6)],
))


@R.add('ch02-st5', 'C3', (1, 5), 'numerical')
def osmosis_pct(rng, slot):
    m0 = rng.choice([2.40, 2.50, 3.20, 3.60, 4.00, 4.80])
    pct = rng.choice([-24, -18, -12, -8, -5, 6, 10, 14])
    m1 = round(m0 * (1 + pct / 100), 2)
    p = (m1 - m0) / m0 * 100
    sol = 'more concentrated' if p < 0 else 'more dilute'
    move = 'out of' if p < 0 else 'into'
    return dict(stem=f'A potato cylinder had a mass of {m0:.2f} g. After 30 minutes in a sugar solution its mass was {m1:.2f} g. Calculate the percentage change in mass and explain what this shows about the solution.',
                answer=f'{p:+.1f}%; the solution was {sol} than the cell sap, so water moved {move} the cells by osmosis',
                markingKey=f'M1 change = {m1:.2f} − {m0:.2f} = {m1 - m0:+.2f} g; M1 ÷ {m0:.2f} × 100; A1 {p:+.1f}%; B1 water moved {move} the potato cells by osmosis because the solution was {sol}.', marks=4)


inquiry('ch02-st5',
        dict(ctx='how the temperature affects the rate of diffusion of potassium permanganate in water',
             iv='temperature of the water (°C)', dv='time for the purple colour to reach the edge of a Petri dish',
             cvs=[('volume of water', 'deeper water changes the distance'), ('size of crystal', 'larger crystals release more dye'), ('no stirring or movement', 'currents would spread the dye'), ('dish size', 'changes the distance travelled')],
             hyp='If temperature increases, then diffusion will be faster, because particles have more kinetic energy and move faster.',
             method='Pour 20 cm³ water at 10, 20, 30, 40 and 50 °C into identical Petri dishes on white paper; drop one small crystal in the centre with forceps; start the stopwatch; record time for colour to reach a circle drawn 3 cm from the centre; repeat three times.',
             weak=('the dishes were bumped while the dye spread', 'place dishes on a still bench away from people walking past and do not touch them'),
             safety='potassium permanganate is an oxidiser and stains skin – use forceps, wear gloves and eye protection'))
dataset('ch02-st5',
        dict(intro='{who} placed potato cylinders in sugar solutions of different concentrations for 1 hour and recorded the percentage gain in mass (three cylinders each).', iv=('Sugar concentration', 'mol/dm³'), xs=[0.0, 0.1, 0.2, 0.3, 0.4],
             dv=('Gain in mass', '%'), f=lambda x: 15 - 30 * x, dp=1, trend='The percentage gain in mass decreases as sugar concentration increases; the gain becomes zero at about 0.5 mol/dm³ and would become a loss above that.',
             why='In dilute solutions water enters the cells by osmosis; as the solution becomes more concentrated there is less water moving in, and above the cell-sap concentration water moves out.'))


# =============================================================================================
# ch03 Digestion and Nutrition
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('carbohydrate', 'a nutrient such as starch or sugar that is the main source of energy'),
           ('protein', 'a nutrient made of amino acids, needed for growth and repair'),
           ('lipid', 'fats and oils, used as a store of energy and for insulation'),
           ('dietary fibre', 'indigestible plant material that adds bulk and keeps food moving through the gut'),
           ('vitamin', 'an organic substance needed in small amounts to stay healthy, e.g. vitamin C'),
           ('mineral', 'an inorganic element needed in small amounts, e.g. iron and calcium'),
           ('deficiency disease', 'an illness caused by a lack of a particular nutrient in the diet')],
    facts=[('Which nutrient is needed for growth and repair of tissues?', 'Protein', ['Carbohydrate', 'Fibre', 'Water'], 'Found in meat, fish, beans, eggs.'),
           ('Lack of vitamin C causes which deficiency disease?', 'Scurvy', ['Rickets', 'Anaemia', 'Goitre'], 'Bleeding gums, slow healing.'),
           ('Which mineral is needed to make haemoglobin in red blood cells?', 'Iron', ['Calcium', 'Sodium', 'Iodine'], 'Lack of iron causes anaemia.'),
           ('Lack of vitamin D or calcium can cause which disease?', 'Rickets', ['Scurvy', 'Anaemia', 'Kwashiorkor'], 'Soft, weak bones.'),
           ('Which food is the best source of dietary fibre?', 'Wholemeal bread and vegetables', ['Butter', 'Chicken', 'Sugar'], 'Fibre comes from plant cell walls.'),
           ('Which nutrient provides the most energy per gram?', 'Lipid (fat)', ['Protein', 'Carbohydrate', 'Fibre'], 'About 37 kJ/g, compared with about 17 kJ/g for carbohydrate.')],
    why=[('Explain why a teenager needs more energy each day than a 70-year-old of the same sex.', 'Teenagers are growing and usually more active, so their cells need more energy and materials for new tissue.'),
         ('Explain why fibre is needed in the diet even though it is not digested.', 'It adds bulk so the muscles of the intestine can push food along (peristalsis), preventing constipation.'),
         ('Explain why eating too much saturated fat can be harmful.', 'It can raise blood cholesterol, which can build up in arteries and increase the risk of heart disease, and excess energy is stored as fat (obesity).')],
    contrast=[('vitamins', 'minerals', 'Vitamins are organic compounds made by living things (e.g. vitamin C); minerals are inorganic elements taken from soil and water (e.g. iron, calcium); both are needed in small amounts.'),
              ('malnutrition', 'starvation', 'Malnutrition is any unbalanced diet – too much or too little of some nutrients; starvation is a severe lack of food energy overall.')],
    misc=[('A balanced diet means eating equal amounts of every food group.', 'A balanced diet contains all nutrients in the right proportions for your needs – more carbohydrate and vegetables, less fat and sugar.'),
          ('Fat is always bad for you.', 'Some fat is needed for energy storage, insulation, cell membranes and absorbing vitamins A and D; the problem is too much, especially saturated fat.')],
    cases=[('James Lind and scurvy (1747)', 'Lind gave groups of sick sailors different treatments; those given oranges and lemons recovered quickly.', 'one of the first controlled trials', 'It showed a dietary cause of scurvy (lack of vitamin C) and led to the Royal Navy issuing citrus juice.')],
    evaluate=[('Sugary drinks should be taxed to reduce obesity.', ['taxes have reduced sugary-drink sales in several countries', 'manufacturers reduced sugar content', 'money raised can fund school sport'], ['hits poorer families harder', 'people may switch to other high-sugar foods', 'obesity has many causes'], 'A sugar tax helps, but must be part of wider education and healthy-food policies.'),
              ('Food labels with traffic-light colours help people choose a balanced diet.', ['quick, easy to understand', 'shows fat, sugar and salt at a glance'], ['ignores vitamins and minerals', 'portion sizes may be unrealistic'], 'Traffic-light labels are a useful quick guide, but consumers still need nutrition knowledge.')],
    extended=[('A student eats crisps and fizzy drinks for lunch every day. Describe which nutrients are missing or in excess, and suggest and justify a better lunch.', 'Excess: fat, salt and sugar (risk of obesity, tooth decay, high blood pressure); lacking: protein (growth), fibre (constipation), vitamins and minerals (e.g. vitamin C, iron, calcium). Better: wholemeal sandwich with chicken or beans, fruit, vegetables, water or milk – provides starch for energy, protein, fibre, vitamins and calcium.', 6)],
))


@R.add('ch03-st1', 'C3', (1, 5), 'numerical')
def energy_need(rng, slot):
    k = rng.choice(['label', 'balance'])
    if k == 'label':
        per100 = rng.choice([1500, 1800, 2100, 380, 950])
        portion = rng.choice([30, 45, 60, 150, 250])
        e = per100 * portion / 100
        return dict(stem=f'A food label says the food contains {per100} kJ per 100 g. Calculate the energy in a {portion} g portion.', answer=f'{g(e)} kJ',
                    markingKey=f'M1 {per100} × {portion} ÷ 100; A1 {g(e)} kJ.', marks=2)
    need = rng.choice([9000, 10000, 11500, 12500])
    eaten = need + rng.choice([-1500, -800, 600, 1200, 2000])
    diff = eaten - need
    out = 'gain' if diff > 0 else 'lose'
    return dict(stem=f'A student needs {need} kJ per day but eats food containing {eaten} kJ per day. Calculate the difference and state what will happen to their body mass over time if this continues.', answer=f'{abs(diff)} kJ per day {"extra" if diff > 0 else "too little"}; they will {out} body mass',
                markingKey=f'M1 {eaten} − {need} = {diff:+d} kJ; A1 {abs(diff)} kJ; B1 they will {out} mass ({"excess stored as fat" if diff > 0 else "body uses fat stores"}).', marks=3)


inquiry('ch03-st1',
        dict(ctx='how the vitamin C content of orange juice changes when it is boiled for different times',
             iv='boiling time (0, 5, 10, 15, 20 min)', dv='volume of juice needed to decolourise 1 cm³ of DCPIP',
             cvs=[('volume of DCPIP (1 cm³)', 'more DCPIP needs more vitamin C'), ('concentration of DCPIP', 'stronger DCPIP needs more juice'), ('same carton of juice', 'brands differ in vitamin C'), ('shaking after each drop', 'mixing ensures the endpoint is seen')],
             hyp='If juice is boiled for longer, then more juice will be needed to decolourise DCPIP, because heat breaks down vitamin C.',
             method='Boil 50 cm³ samples of juice for each time and cool to room temperature; put 1 cm³ DCPIP in a test tube; add juice drop by drop from a burette or graduated pipette, shaking, until the blue colour disappears; record the volume; repeat three times for each time; calculate means.',
             weak=('the endpoint colour was judged differently each time', 'compare against a white tile and a colour standard; use the same person to judge'),
             safety='DCPIP is an irritant – wear eye protection; hot liquids scald'))
dataset('ch03-st1',
        dict(intro='{who} measured the volume of fruit juice needed to decolourise 1 cm³ of DCPIP after the juice had been stored for different numbers of days.', iv=('Storage time', 'days'), xs=[0, 2, 4, 6, 8],
             dv=('Volume of juice', 'cm³'), f=lambda x: 1.2 + 0.35 * x, dp=1, trend='More juice is needed to decolourise DCPIP the longer the juice is stored, so its vitamin C content falls with time.',
             why='Vitamin C is slowly broken down by oxygen (oxidised) during storage, so each cm³ of juice contains less vitamin C.'))

R.facts('ch03-st2', F(
    terms=[('digestion', 'the breakdown of large insoluble food molecules into small soluble molecules that can be absorbed'),
           ('peristalsis', 'waves of muscle contraction that push food along the gut'),
           ('absorption', 'the movement of digested food molecules from the small intestine into the blood'),
           ('villus', 'a finger-like projection of the small intestine wall that increases surface area for absorption'),
           ('bile', 'a liquid made in the liver and stored in the gall bladder that emulsifies fats and neutralises stomach acid'),
           ('oesophagus', 'the muscular tube that carries food from the mouth to the stomach')],
    facts=[('Where is most digested food absorbed into the blood?', 'Small intestine', ['Stomach', 'Large intestine', 'Oesophagus'], 'It has villi.'),
           ('What is the main job of the large intestine?', 'Absorbing water from undigested food', ['Digesting protein', 'Making bile', 'Absorbing glucose'], 'Faeces form there.'),
           ('Which organ produces hydrochloric acid?', 'Stomach', ['Pancreas', 'Liver', 'Small intestine'], 'Acid kills bacteria.'),
           ('What is the correct order of food passing through the gut?', 'mouth → oesophagus → stomach → small intestine → large intestine', ['mouth → stomach → oesophagus → large intestine → small intestine', 'mouth → small intestine → stomach → large intestine → oesophagus', 'mouth → oesophagus → large intestine → stomach → small intestine'], 'Food ends at the rectum and anus.'),
           ('What does bile do to fats?', 'Breaks them into small droplets (emulsifies them)', ['Digests them into glucose', 'Absorbs them into the blood', 'Turns them into protein'], 'This gives lipase a larger surface area.')],
    why=[('Explain why large food molecules such as starch must be digested.', 'They are too large and insoluble to pass through the wall of the small intestine into the blood; small soluble molecules can be absorbed.'),
         ('Explain how villi are adapted for absorption.', 'They give a huge surface area, have walls one cell thick for a short diffusion distance, and a good blood supply that carries absorbed food away, keeping a concentration gradient.'),
         ('Explain why chewing food helps digestion.', 'It breaks food into smaller pieces with a larger surface area for enzymes to act on and mixes it with saliva.')],
    contrast=[('mechanical digestion', 'chemical digestion', 'Mechanical digestion physically breaks food into smaller pieces (teeth, stomach churning); chemical digestion uses enzymes to break large molecules into small ones.'),
              ('absorption', 'assimilation', 'Absorption is the movement of digested food into the blood; assimilation is when cells use the absorbed molecules to build new substances.')],
    misc=[('Food is digested in the stomach and that is where it is absorbed.', 'The stomach starts protein digestion, but most digestion finishes, and almost all absorption happens, in the small intestine.'),
          ('Bile is an enzyme that digests fat.', 'Bile contains no enzymes; it emulsifies fat into droplets so lipase can work faster, and neutralises stomach acid.')],
    cases=[('William Beaumont and Alexis St Martin (1820s)', 'Beaumont studied a patient with a hole into his stomach from a gunshot wound, tying food on strings into the stomach and removing it later.', 'observing digestion', 'He showed that gastric juice digests food chemically, not just by grinding – though the ethics of the study are questioned today.')],
    evaluate=[('Gastric band surgery is a good solution to obesity.', ['large weight loss', 'reduces type 2 diabetes'], ['surgical risks and side effects', 'does not change eating habits', 'expensive for health services'], 'Surgery can help severely obese patients, but diet and lifestyle change are needed for most people.')],
    extended=[('Describe the journey of a mouthful of a cheese sandwich through the digestive system, naming where each nutrient is digested and absorbed.', 'Mouth: chewing, amylase in saliva starts starch digestion. Oesophagus: peristalsis. Stomach: acid and protease (pepsin) start protein digestion; churning. Small intestine: bile emulsifies fat; pancreatic amylase, protease, lipase finish digestion to sugars, amino acids, fatty acids and glycerol; absorbed through villi into blood. Large intestine: water absorbed; fibre egested as faeces.', 6)],
))


@R.add('ch03-st2', 'C3', (1, 4), 'numerical')
def gut_transit(rng, slot):
    k = rng.choice(['sa', 'time'])
    if k == 'sa':
        L = rng.choice([5, 6, 7])
        f = rng.choice([30, 60, 100])
        base = rng.choice([0.4, 0.5])
        return dict(stem=f'A model small intestine is a tube {L} m long with an inside surface area of {base} m². Villi and folds increase the surface area by a factor of {f}. Calculate the total absorbing surface area and explain why this is important.', answer=f'{g(base * f)} m²; a larger surface area allows faster absorption of digested food by diffusion',
                    markingKey=f'M1 {base} × {f}; A1 {g(base * f)} m²; B1 larger area → more absorption per second.', marks=3)
    d = rng.choice([25, 30, 40])
    t = rng.choice([5, 8, 10])
    return dict(stem=f'Food moves {d} cm through the oesophagus in {t} seconds by peristalsis. Calculate the average speed in cm/s.', answer=f'{g(d / t)} cm/s',
                markingKey=f'M1 speed = distance ÷ time = {d} ÷ {t}; A1 {g(d / t)} cm/s.', marks=2)


inquiry('ch03-st2',
        dict(ctx='how the pH affects the digestion of egg white protein by pepsin',
             iv='pH of the solution (1, 2, 4, 6, 8 using buffers)', dv='time for a cloudy egg-white suspension to become clear',
             cvs=[('volume and concentration of pepsin', 'more enzyme digests faster'), ('temperature (37 °C water bath)', 'enzyme activity depends on temperature'), ('volume of egg-white suspension', 'more substrate takes longer'), ('the same observer and white background', 'judging clearness')],
             hyp='If the pH is about 2, then digestion will be fastest, because pepsin works in the acidic stomach and its active site has the right shape at low pH.',
             method='Put 5 cm³ egg-white suspension and 2 cm³ buffer into tubes at each pH; warm in a 37 °C water bath for 5 min; add 1 cm³ pepsin, start the stopwatch; record time until clear against a black card; repeat three times; include a control with boiled enzyme.',
             weak=('the enzyme and substrate were at different temperatures when mixed', 'pre-warm both tubes separately in the water bath before mixing'),
             safety='acid buffers are irritants – wear eye protection; enzymes can cause allergies – avoid skin contact'))
dataset('ch03-st2',
        dict(intro='{who} placed visking tubing containing starch and amylase in water at 37 °C and measured the glucose concentration of the outside water over time.', iv=('Time', 'min'), xs=[5, 10, 15, 20, 25],
             dv=('Glucose concentration', 'mg/dm³'), f=lambda x: 4 * x + 2, dp=0, trend='The glucose concentration outside the tubing increases steadily with time.',
             why='Amylase digests starch into small sugar molecules that can pass through the partially permeable tubing (like the gut wall), while starch molecules are too large.'))

R.facts('ch03-st3', F(
    terms=[('enzyme', 'a protein that acts as a biological catalyst, speeding up reactions without being used up'),
           ('active site', 'the part of an enzyme where the substrate fits'),
           ('substrate', 'the molecule that an enzyme acts on'),
           ('amylase', 'an enzyme that breaks down starch into maltose (sugar)'),
           ('protease', 'an enzyme that breaks down protein into amino acids'),
           ('lipase', 'an enzyme that breaks down lipids into fatty acids and glycerol'),
           ('denatured', 'describes an enzyme whose active site has changed shape so the substrate no longer fits')],
    facts=[('What are the products of protein digestion?', 'Amino acids', ['Glucose', 'Fatty acids', 'Glycerol only'], 'Proteins are chains of amino acids.'),
           ('Where is amylase produced?', 'Salivary glands and pancreas', ['Stomach and liver', 'Gall bladder', 'Large intestine'], 'Starch digestion starts in the mouth.'),
           ('What happens to most human enzymes above about 45 °C?', 'They become denatured', ['They work faster forever', 'They are used up', 'They turn into substrate'], 'The active site changes shape.'),
           ('Which reagent shows that starch has been digested?', 'Iodine stays orange-brown instead of turning blue-black', ['Iodine turns blue-black', 'Biuret turns purple', 'Benedict’s stays blue'], 'No starch left.'),
           ('What is the optimum temperature for most human enzymes?', 'About 37 °C', ['0 °C', '60 °C', '100 °C'], 'Body temperature.')],
    why=[('Explain why each enzyme only acts on one substrate.', 'The active site has a specific shape that only fits one substrate (lock and key), so other molecules cannot bind.'),
         ('Explain why enzyme reactions slow down at low temperatures.', 'Molecules have less kinetic energy, so enzyme and substrate collide less often and fewer successful collisions happen each second.'),
         ('Explain why biological washing powders work best at 30–40 °C.', 'They contain enzymes (proteases, lipases) that work fastest near their optimum; hotter water denatures them.')],
    contrast=[('an enzyme being denatured', 'an enzyme being inactive at low temperature', 'At low temperature the enzyme is just slow and will work again when warmed; a denatured enzyme has its active site permanently changed and cannot work again.'),
              ('amylase', 'protease', 'Amylase breaks starch into sugars (mouth, small intestine); protease breaks proteins into amino acids (stomach, small intestine).')],
    misc=[('Enzymes are killed by high temperatures.', 'Enzymes are not alive so cannot be killed; they are denatured – the shape of the active site changes.'),
          ('Enzymes are used up in the reaction.', 'Enzymes are catalysts; they are unchanged and can be used again and again.')],
    cases=[('Enzymes in lactose-free milk', 'Lactase enzyme is added to milk to break lactose into glucose and galactose, so people with lactose intolerance can drink it.', 'enzymes in food technology', 'Using an enzyme outside the body solves a digestion problem for millions of people.')],
    evaluate=[('Enzymes should be used in more industrial processes instead of high-temperature chemical reactions.', ['work at low temperatures, saving energy', 'specific, so fewer waste products', 'biodegradable'], ['denatured easily by heat or wrong pH', 'can be expensive to produce and purify'], 'Enzymes are a greener option for many processes when conditions can be controlled.')],
    extended=[('Use the lock-and-key model to explain how temperature affects the rate of starch digestion by amylase from 10 °C to 70 °C.', 'Starch fits amylase active site (complementary shape). From 10 °C rate rises as particles move faster – more collisions and enzyme–substrate complexes; maximum at about 37 °C (optimum); above this vibrations change the active site shape – denatured – starch no longer fits, so the rate falls rapidly to zero by about 60–70 °C.', 6)],
))


@R.add('ch03-st3', 'C3', (1, 5), 'numerical')
def enzyme_rate(rng, slot):
    t = rng.choice([20, 30, 40, 50, 60, 80, 120])
    s = rng.choice([1, 2, 5])
    k = rng.choice(['rate', 'compare'] if slot.d >= 3 else ['rate'])
    if k == 'rate':
        return dict(stem=f'Iodine stopped turning blue-black after {t} s when amylase digested a starch solution. Calculate the rate of reaction as 1000 ÷ time, in s⁻¹.', answer=f'{g(1000 / t)} s⁻¹',
                    markingKey=f'M1 1000 ÷ {t}; A1 {g(1000 / t)} s⁻¹.', marks=2)
    t2 = t * 2
    return dict(stem=f'Starch was digested in {t} s at 35 °C and in {t2} s at 25 °C. Calculate the rate (1000/time) at each temperature and explain the difference.', answer=f'{g(1000 / t)} s⁻¹ at 35 °C and {g(1000 / t2)} s⁻¹ at 25 °C; the rate doubles because molecules collide more often at higher temperature',
                markingKey=f'M1 1000 ÷ {t} = {g(1000 / t)}; M1 1000 ÷ {t2} = {g(1000 / t2)}; B1 higher temperature – more kinetic energy – more frequent collisions between enzyme and starch.', marks=3)


inquiry('ch03-st3',
        dict(ctx='how temperature affects the time taken for amylase to digest starch',
             iv='temperature of the water bath (°C)', dv='time until a sample no longer turns iodine blue-black – tested every 30 s on a spotting tile',
             cvs=[('volume and concentration of amylase', 'more enzyme works faster'), ('volume and concentration of starch', 'more substrate takes longer to digest'), ('pH (buffer at pH 7)', 'pH affects enzyme shape'), ('time interval between samples', 'affects the precision of the time')],
             hyp='If the temperature increases up to 37 °C, then the starch will be digested faster, because molecules collide more often; above about 45 °C it will slow, because amylase is denatured.',
             method='Put a drop of iodine in each well of a spotting tile; warm 5 cm³ starch and 1 cm³ amylase in separate tubes in a water bath at 20 °C for 5 min; mix and start the stopwatch; every 30 s put a drop of the mixture into iodine; record the time when iodine stays orange; repeat at 30, 40, 50, 60 °C; repeat three times.',
             weak=('samples were tested only every 2 minutes', 'test every 30 s (or 10 s) to make the end-point time more precise'),
             safety='iodine solution irritates eyes and stains – wear eye protection; take care with hot water baths'))
dataset('ch03-st3',
        dict(intro='{who} measured how long a protease took to clear a cloudy milk suspension at different pH values.', iv=('pH', ''), xs=[1, 2, 3, 4, 5],
             dv=('Time to clear', 's'), f=lambda x: 60 + 25 * (x - 2) ** 2, dp=0, trend='The time is shortest at pH 2 and increases as pH moves away from 2 in either direction.',
             why='This protease (like pepsin) has an optimum pH of about 2; at other pH values the shape of the active site changes, so fewer substrate molecules fit.'))

R.facts('ch03-st4', F(
    terms=[('Benedict’s test', 'a test for reducing sugars: heated with Benedict’s solution, a positive result turns from blue to green, yellow or brick red'),
           ('iodine test', 'a test for starch: iodine turns from orange-brown to blue-black'),
           ('Biuret test', 'a test for protein: the solution turns from blue to purple'),
           ('emulsion test', 'a test for lipids: shaken with ethanol then water, a cloudy white emulsion forms'),
           ('calorimetry', 'measuring the energy released by burning a food, using the temperature rise of water')],
    facts=[('Which result shows protein is present in the Biuret test?', 'Purple colour', ['Brick-red precipitate', 'Blue-black colour', 'Cloudy white layer'], 'Biuret stays blue if no protein.'),
           ('Which food test must be heated in a water bath?', 'Benedict’s test for sugar', ['Iodine test for starch', 'Biuret test for protein', 'Emulsion test for fat'], 'About 80 °C for a few minutes.'),
           ('A food turns iodine blue-black. Which nutrient does it contain?', 'Starch', ['Sugar', 'Protein', 'Fat'], 'e.g. bread, potato.'),
           ('How much energy is needed to raise the temperature of 1 g of water by 1 °C?', '4.2 J', ['1 J', '42 J', '0.42 J'], 'Specific heat capacity of water.'),
           ('Why does burning food under a boiling tube give a lower energy value than food labels?', 'Much energy is lost to the surroundings', ['Food labels are always wrong', 'Water absorbs too much energy', 'The food gains mass'], 'Heat escapes to the air and the tube.')],
    why=[('Explain why the same volume of water should be used each time when comparing the energy in foods.', 'The temperature rise depends on the mass of water heated; using the same volume makes the comparison fair.'),
         ('Explain why a food may give a brick-red colour with Benedict’s solution but no blue-black colour with iodine.', 'It contains reducing sugar (e.g. glucose in fruit) but no starch.'),
         ('Explain why the emulsion test uses ethanol.', 'Fats dissolve in ethanol but not in water; when water is added the fat comes out of solution as tiny droplets, making the liquid cloudy.')],
    contrast=[('a qualitative food test', 'a quantitative measurement', 'A qualitative food test shows whether a nutrient is present (colour change); a quantitative measurement gives an amount, e.g. energy in kJ/g by calorimetry.'),
              ('the Benedict’s test', 'the Biuret test', 'Benedict’s detects reducing sugars and needs heating (blue → brick red); Biuret detects protein at room temperature (blue → purple).')],
    misc=[('If iodine stays orange, the food contains no nutrients.', 'It only shows there is no starch; the food may contain sugar, protein or fat.'),
          ('Burning a peanut measures exactly how much energy it contains.', 'Much energy is lost to the air, the tube and in incomplete burning, so the value is lower than the true value.')],
    evaluate=[('Calorie counting is the best way to stay healthy.', ['helps control body mass by matching energy in and out'], ['ignores vitamins, minerals, fibre and protein', 'can encourage unhealthy obsession with food'], 'Energy balance matters, but the quality and balance of nutrients matter just as much.')],
    extended=[('Plan an investigation to compare the energy content of three snack foods by burning them. Include a calculation and two ways to reduce energy losses.', 'Mass a food sample; 20 cm³ water in a boiling tube clamped above it; record initial temperature; ignite food on a mounted needle and hold under the tube until it burns out (relight if needed); record maximum temperature. Energy (J) = 20 × 4.2 × temperature rise; per gram = energy ÷ mass. Repeat three times. Reduce losses: insulate the tube/use a draught shield, keep food close to the tube, use a calorimeter with a metal can.', 6)],
))


@R.add('ch03-st4', 'C3', (1, 5), 'numerical')
def food_energy(rng, slot):
    food = rng.choice(['peanut', 'cashew nut', 'crisp', 'piece of bread', 'cracker', 'piece of popcorn'])
    v = rng.choice([10, 20, 25, 30])
    dt = rng.choice([12, 15, 18, 22, 27, 34])
    m = rng.choice([0.4, 0.5, 0.6, 0.8, 1.0])
    E = v * 4.2 * dt
    k = rng.choice(['E', 'per'] if slot.d >= 2 else ['E'])
    if k == 'E':
        return dict(stem=f'A burning {food} heated {v} g of water from 20 °C to {20 + dt} °C. Calculate the energy transferred to the water (4.2 J are needed to heat 1 g of water by 1 °C).', answer=f'{g(E)} J',
                    markingKey=f'M1 temperature rise = {dt} °C; M1 energy = {v} × 4.2 × {dt}; A1 {g(E)} J.', marks=3)
    return dict(stem=f'A {m} g {food} was burned under a tube of {v} g water. The temperature rose by {dt} °C. Calculate the energy released per gram of food (in J/g) and suggest why the value is lower than on the packet.', answer=f'{g(E / m)} J/g; energy was lost to the air and the tube (and burning was incomplete)',
                markingKey=f'M1 energy = {v} × 4.2 × {dt} = {g(E)} J; M1 ÷ {m}; A1 {g(E / m)} J/g; B1 heat lost to surroundings / incomplete combustion.', marks=4)


@R.add('ch03-st4', 'C1', (1, 2), 'mcq')
def food_test(rng, slot):
    tests = [('starch', 'iodine solution', 'orange-brown to blue-black'), ('reducing sugar', 'Benedict’s solution (heated)', 'blue to brick red'),
             ('protein', 'Biuret reagent', 'blue to purple'), ('lipid', 'ethanol then water (emulsion test)', 'clear to cloudy white')]
    n, r, c = rng.choice(tests)
    if rng.random() < 0.5:
        return mcq(rng, f'Which reagent is used to test a food for {n}?', r, [b for a, b, _ in tests if a != n], f'B1 {r}')
    return mcq(rng, f'Which colour change shows a positive test for {n}?', c, [x for a, _, x in tests if a != n], f'B1 {c}')


inquiry('ch03-st4',
        dict(ctx='how the type of nut affects the energy released when it burns',
             iv='type of nut (peanut, almond, cashew, walnut)', dv='temperature rise of 20 cm³ of water, used to calculate energy per gram',
             cvs=[('volume of water (20 cm³)', 'the temperature rise depends on the mass heated'), ('distance between nut and tube (1 cm)', 'more heat escapes if further away'), ('starting temperature of the water', 'affects heat loss'), ('the same boiling tube', 'glass thickness absorbs energy')],
             hyp='If the nut has a higher fat content (e.g. walnut), then it will release more energy per gram, because lipids store more energy per gram than carbohydrate or protein.',
             method='Weigh a nut; clamp a boiling tube containing 20 cm³ water; record the temperature; set the nut alight on a mounted needle and hold it 1 cm under the tube until it stops burning; record the highest temperature; calculate energy = 20 × 4.2 × rise and divide by mass; repeat with three nuts of each type.',
             weak=('the nut went out and was not relit', 'relight the nut until it no longer burns and check that only ash is left'),
             safety='nut allergies – check before the lesson; burning food is hot – use a heat-proof mat and tie back hair'))
dataset('ch03-st4',
        dict(intro='{who} burned different masses of the same crisp brand under 20 g of water and recorded the temperature rise.', iv=('Mass of crisps', 'g'), xs=[0.2, 0.4, 0.6, 0.8, 1.0],
             dv=('Temperature rise', '°C'), f=lambda x: 28 * x, dp=1, trend='The temperature rise increases in proportion to the mass of crisps burned.',
             why='Each gram of crisp releases about the same energy, so doubling the mass doubles the energy transferred to the water.'))


# =============================================================================================
# ch04 Circulation and Respiration
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('artery', 'a blood vessel with a thick muscular, elastic wall that carries blood away from the heart at high pressure'),
           ('vein', 'a blood vessel with a thin wall and valves that carries blood back to the heart at low pressure'),
           ('capillary', 'a tiny blood vessel with walls one cell thick where substances are exchanged with tissues'),
           ('double circulation', 'a system where blood passes through the heart twice for each complete circuit of the body'),
           ('atrium', 'an upper chamber of the heart that receives blood from veins'),
           ('ventricle', 'a lower chamber of the heart that pumps blood out into arteries'),
           ('valve', 'a flap of tissue that stops blood flowing backwards')],
    facts=[('Which blood vessel carries oxygenated blood from the lungs to the heart?', 'Pulmonary vein', ['Pulmonary artery', 'Aorta', 'Vena cava'], 'The only vein carrying oxygenated blood.'),
           ('Why is the wall of the left ventricle thicker than the right?', 'It pumps blood all around the body at higher pressure', ['It receives more blood', 'It carries deoxygenated blood', 'It contains valves'], 'The right ventricle pumps only to the lungs.'),
           ('Which vessel carries blood from the heart to the body?', 'Aorta', ['Vena cava', 'Pulmonary vein', 'Pulmonary artery'], 'The largest artery.'),
           ('Which vessels allow exchange of oxygen and glucose with body cells?', 'Capillaries', ['Arteries', 'Veins', 'Valves'], 'Thin walls, short diffusion distance.'),
           ('What do the valves in veins do?', 'Stop blood flowing backwards', ['Pump blood', 'Make blood clot', 'Add oxygen to blood'], 'Blood is at low pressure in veins.')],
    why=[('Explain why arteries have thick, elastic walls.', 'Blood leaves the heart at high pressure; thick muscle and elastic tissue withstand the pressure and stretch and recoil to smooth the flow.'),
         ('Explain the advantage of a double circulation.', 'Blood returns to the heart after the lungs to be pumped again at high pressure, so oxygen reaches body tissues quickly.'),
         ('Explain why capillaries are only one cell thick.', 'It gives a very short diffusion distance for oxygen, glucose and carbon dioxide between blood and cells.')],
    contrast=[('an artery', 'a vein', 'An artery carries blood away from the heart at high pressure and has a thick muscular wall and narrow lumen; a vein carries blood to the heart at low pressure, with a thin wall, wide lumen and valves.'),
              ('the pulmonary circuit', 'the systemic circuit', 'The pulmonary circuit takes blood from the heart to the lungs and back; the systemic circuit takes it from the heart to the rest of the body and back.')],
    misc=[('Arteries always carry oxygenated blood and veins always carry deoxygenated blood.', 'Arteries carry blood away from the heart; the pulmonary artery carries deoxygenated blood and the pulmonary vein oxygenated blood.'),
          ('Deoxygenated blood is blue.', 'Deoxygenated blood is dark red; veins only look blue through the skin.')],
    cases=[('William Harvey and circulation (1628)', 'Harvey calculated that the heart pumps far more blood each hour than the body could make from food, and showed with tourniquets that valves in veins only allow flow towards the heart.', 'evidence for circulation', 'He overturned the 1400-year-old idea of Galen that blood was made and used up, showing blood circulates.'),
           ('Artificial pacemakers', 'A small device under the skin sends electrical impulses to make the heart beat regularly when its natural pacemaker fails.', 'technology and the heart', 'Millions of people live normal lives with pacemakers, which have become smaller and longer-lasting.')],
    evaluate=[('Everyone over 40 should have a free heart check every year.', ['early detection of high blood pressure and cholesterol', 'prevents costly heart attacks later'], ['very expensive for health services', 'may cause anxiety and over-treatment'], 'Regular checks for at-risk groups are cost-effective; universal yearly checks may not be.')],
    extended=[('Describe the path of a red blood cell from the vena cava to the aorta, naming the chambers, valves and vessels, and explain where it gains oxygen.', 'Vena cava → right atrium → (tricuspid valve) → right ventricle → (semilunar valve) → pulmonary artery → capillaries of lungs: oxygen diffuses from alveoli into blood → pulmonary vein → left atrium → (bicuspid valve) → left ventricle → (semilunar valve) → aorta.', 6)],
))


@R.add('ch04-st1', 'C3', (1, 5), 'numerical')
def cardiac(rng, slot):
    hr = rng.choice([60, 65, 70, 72, 75, 80, 140, 160])
    sv = rng.choice([60, 70, 75, 80, 100, 110])
    co = hr * sv / 1000
    k = rng.choice(['co', 'hr', 'pulse'] if slot.d >= 2 else ['pulse'])
    if k == 'pulse':
        c = rng.choice([17, 18, 19, 20, 21, 32, 38])
        t = rng.choice([15, 20, 30])
        return dict(stem=f'A student counts {c} pulse beats in {t} seconds. Calculate the heart rate in beats per minute.', answer=f'{g(c * 60 / t)} bpm',
                    markingKey=f'M1 {c} × (60 ÷ {t}); A1 {g(c * 60 / t)} beats per minute.', marks=2)
    if k == 'co':
        return dict(stem=f'An athlete’s heart rate is {hr} beats per minute and each beat pumps {sv} cm³ of blood. Calculate the volume of blood pumped per minute, in dm³ (1 dm³ = 1000 cm³).', answer=f'{g(co)} dm³/min',
                    markingKey=f'M1 cardiac output = heart rate × stroke volume = {hr} × {sv} = {hr * sv} cm³/min; A1 {g(co)} dm³/min.', marks=3)
    return dict(stem=f'A heart pumps {g(co)} dm³ of blood per minute, with {sv} cm³ per beat. Calculate the heart rate.', answer=f'{hr} beats per minute',
                markingKey=f'M1 convert {g(co)} dm³ = {hr * sv} cm³; M1 heart rate = {hr * sv} ÷ {sv}; A1 {hr} bpm.', marks=3)


inquiry('ch04-st1',
        dict(ctx='how the duration of exercise affects heart rate',
             iv='time spent stepping on and off a step (0, 1, 2, 3, 4 min)', dv='heart rate in beats per minute measured immediately afterwards with a pulse sensor',
             cvs=[('step height', 'higher steps need more work'), ('stepping rate (set by a metronome)', 'faster stepping raises heart rate more'), ('the same person (or similar fitness)', 'fitness changes heart-rate response'), ('rest until heart rate returns to resting before each trial', 'previous exercise affects the next reading')],
             hyp='If exercise lasts longer, then heart rate will increase, because muscles respire faster and need more oxygen and glucose delivered by the blood.',
             method='Record resting heart rate with a pulse sensor; step on and off a 30 cm step at a metronome rate of 30 steps/min for 1 min; record heart rate immediately; rest until heart rate returns to resting; repeat for 2, 3 and 4 min; repeat three times; plot a line graph.',
             weak=('pulse was counted by hand for 6 s and multiplied by 10', 'use a pulse sensor or count for 30 s and double, to reduce counting errors'),
             safety='stop if dizzy or unwell; students with heart or breathing conditions should not take part; clear the area around the step'))
dataset('ch04-st1',
        dict(intro='{who} measured the time taken for heart rate to return to resting after 2 minutes of skipping, for students who exercise different numbers of hours per week.', iv=('Exercise per week', 'h'), xs=[1, 2, 4, 6, 8],
             dv=('Recovery time', 's'), f=lambda x: 300 - 25 * x, dp=0, trend='The recovery time decreases as the number of hours of exercise per week increases.',
             why='Regular exercise strengthens the heart muscle so it pumps more blood per beat, so the oxygen debt is repaid and heart rate returns to normal sooner.'))

R.facts('ch04-st2', F(
    terms=[('plasma', 'the yellow liquid part of blood that carries dissolved substances such as glucose, CO₂, urea and hormones'),
           ('red blood cell', 'a biconcave cell with no nucleus that contains haemoglobin and carries oxygen'),
           ('white blood cell', 'a blood cell that defends the body against pathogens'),
           ('platelet', 'a cell fragment that helps blood to clot'),
           ('haemoglobin', 'the red protein in red blood cells that combines with oxygen'),
           ('phagocyte', 'a white blood cell that engulfs and digests pathogens')],
    facts=[('Which blood component helps blood to clot at a cut?', 'Platelets', ['Red blood cells', 'Plasma', 'Lymphocytes'], 'They form a plug and help fibrin form.'),
           ('Which component of blood transports carbon dioxide and glucose?', 'Plasma', ['Platelets', 'White blood cells', 'Haemoglobin'], 'Dissolved in the liquid.'),
           ('What do lymphocytes produce?', 'Antibodies', ['Haemoglobin', 'Platelets', 'Glucose'], 'Antibodies target specific pathogens.'),
           ('Why are red blood cells biconcave?', 'To give a large surface area for oxygen to diffuse in and out', ['To help them clot', 'To store a nucleus', 'To engulf bacteria'], 'And to squeeze through capillaries.'),
           ('Which blood component is the most numerous?', 'Red blood cells', ['White blood cells', 'Platelets', 'Antibodies'], 'About 5 million per mm³.')],
    why=[('Explain why people living at high altitude develop more red blood cells.', 'There is less oxygen in each breath; more red blood cells (more haemoglobin) carry enough oxygen to the tissues.'),
         ('Explain why a person with too few platelets bruises easily.', 'Blood does not clot quickly, so small damaged vessels under the skin keep bleeding.'),
         ('Explain how phagocytes protect the body.', 'They move to infected areas, engulf pathogens and digest them with enzymes.')],
    contrast=[('red blood cells', 'white blood cells', 'Red blood cells carry oxygen, have haemoglobin and no nucleus; white blood cells defend against pathogens, have a nucleus and are much fewer.'),
              ('phagocytes', 'lymphocytes', 'Phagocytes engulf and digest pathogens; lymphocytes make antibodies that target specific pathogens.')],
    misc=[('Blood is just red liquid.', 'Blood is about 55% plasma (a liquid) and 45% cells and platelets.'),
          ('White blood cells attack all cells in the body.', 'They recognise and destroy foreign cells and pathogens, not the body’s own healthy cells (except in autoimmune diseases).')],
    cases=[('Karl Landsteiner and blood groups (1901)', 'Landsteiner found that mixing blood from different people sometimes caused clumping, and identified the A, B and O groups.', 'blood transfusion', 'Matching blood groups made blood transfusion safe and has saved millions of lives.')],
    evaluate=[('Blood donation should be compulsory for healthy adults.', ['blood banks often run short', 'saves lives in surgery and accidents'], ['bodily autonomy – forcing donation is unethical', 'religious objections', 'voluntary donors are more honest about health risks'], 'Donation should remain voluntary, with better campaigns to encourage it.')],
    extended=[('Describe the four components of blood and explain how each is adapted to its function.', 'Red blood cells: haemoglobin, no nucleus, biconcave – carry oxygen. White blood cells: phagocytes engulf pathogens (flexible membrane, enzymes), lymphocytes make antibodies. Platelets: fragments that release chemicals to form a clot (fibrin) – seal wounds. Plasma: liquid carrying dissolved glucose, amino acids, CO₂, urea, hormones and heat.', 6)],
))


@R.add('ch04-st2', 'C3', (1, 4), 'numerical')
def blood_count(rng, slot):
    k = rng.choice(['ratio', 'volume'])
    if k == 'ratio':
        r = rng.choice([4800000, 5000000, 5200000])
        w = rng.choice([6000, 7500, 8000])
        return dict(stem=f'A blood sample contains {r:,} red blood cells and {w:,} white blood cells per mm³. Calculate the ratio of red to white blood cells (to the nearest whole number) and comment.', answer=f'about {round(r / w)} : 1 – red blood cells are far more numerous',
                    markingKey=f'M1 {r:,} ÷ {w:,}; A1 ≈ {round(r / w)} : 1; B1 red blood cells greatly outnumber white.', marks=3)
    v = rng.choice([4.5, 5.0, 5.5])
    p = rng.choice([54, 55, 56])
    return dict(stem=f'An adult has {v} dm³ of blood, of which {p}% is plasma. Calculate the volume of plasma in dm³.', answer=f'{g(v * p / 100)} dm³',
                markingKey=f'M1 {v} × {p} ÷ 100; A1 {g(v * p / 100)} dm³.', marks=2)


inquiry('ch04-st2',
        dict(ctx='how altitude of training camps affects the red blood cell count of athletes',
             iv='altitude of the training camp (0, 1000, 2000, 3000 m)', dv='red blood cell count per mm³ from a blood test after 3 weeks',
             cvs=[('length of time at the camp (3 weeks)', 'red cell count rises gradually'), ('training programme', 'exercise intensity affects the result'), ('diet, especially iron', 'iron is needed for haemoglobin'), ('time of day of the blood test', 'hydration changes concentration')],
             hyp='If altitude is higher, then the red blood cell count will increase more, because there is less oxygen in the air so the body makes more red cells to carry enough oxygen.',
             method='Take blood tests from groups of 10 athletes before training; send groups to camps at each altitude for 3 weeks with the same training plan and diet; take blood tests at the same time of day; calculate mean increase in red cell count per group.',
             weak=('only two athletes were in each group', 'use larger groups (at least 10) to reduce the effect of individual variation'),
             safety='blood samples taken only by trained staff with sterile equipment; athletes must give informed consent'))
dataset('ch04-st2',
        dict(intro='{who} recorded the haemoglobin concentration of people living at different altitudes (three groups at each altitude).', iv=('Altitude', 'm'), xs=[0, 1000, 2000, 3000, 4000],
             dv=('Haemoglobin', 'g/dm³'), f=lambda x: 140 + 0.007 * x, dp=0, trend='The haemoglobin concentration increases with altitude.',
             why='At higher altitude there is less oxygen per breath, so the body makes more haemoglobin to carry enough oxygen to the tissues.'))

R.facts('ch04-st3', F(
    terms=[('alveoli', 'tiny air sacs in the lungs where gas exchange takes place'),
           ('diaphragm', 'a sheet of muscle under the lungs that contracts and flattens to help draw air in'),
           ('intercostal muscles', 'muscles between the ribs that move the ribcage during breathing'),
           ('trachea', 'the windpipe, held open by rings of cartilage, carrying air to the bronchi'),
           ('bronchiole', 'a small branching tube in the lungs leading to the alveoli'),
           ('gas exchange', 'the diffusion of oxygen into the blood and carbon dioxide out of the blood')],
    facts=[('What happens to the diaphragm during inhalation?', 'It contracts and flattens', ['It relaxes and domes upwards', 'It stays still', 'It moves the trachea'], 'Volume of the chest increases.'),
           ('Which gas is at a higher percentage in exhaled air than inhaled air?', 'Carbon dioxide', ['Oxygen', 'Nitrogen', 'Argon'], 'About 4% compared with 0.04%.'),
           ('Why does air move into the lungs when the chest volume increases?', 'The pressure inside falls below atmospheric pressure', ['Oxygen is attracted to blood', 'The lungs suck it in with muscles', 'The pressure inside rises'], 'Air flows from high to low pressure.'),
           ('What keeps the trachea open?', 'Rings of cartilage', ['Muscles', 'Mucus', 'Alveoli'], 'They stop it collapsing.'),
           ('What do the cilia in the airways do?', 'Sweep mucus and trapped dust up and out of the lungs', ['Absorb oxygen', 'Make mucus', 'Exchange gases'], 'Goblet cells make the mucus.')],
    why=[('Explain how the alveoli are adapted for efficient gas exchange.', 'Millions of alveoli give a huge surface area; walls one cell thick give a short diffusion distance; a rich capillary network and ventilation maintain a steep concentration gradient; moist surface lets gases dissolve.'),
         ('Explain why smoking makes people breathless.', 'Tar damages and destroys alveolar walls (emphysema) reducing surface area, and carbon monoxide binds to haemoglobin, so less oxygen reaches tissues.'),
         ('Explain why breathing rate increases during exercise.', 'Muscles respire faster and make more CO₂; breathing faster removes CO₂ and supplies more oxygen.')],
    contrast=[('breathing (ventilation)', 'gas exchange', 'Breathing is the movement of air in and out of the lungs by muscles; gas exchange is the diffusion of oxygen and CO₂ between alveoli and blood.'),
              ('inhalation', 'exhalation', 'In inhalation the intercostals and diaphragm contract, chest volume increases, pressure falls and air rushes in; in exhalation they relax, volume decreases, pressure rises and air is pushed out.')],
    misc=[('We breathe in oxygen and breathe out only carbon dioxide.', 'Exhaled air is still about 16% oxygen and mostly nitrogen; it contains about 4% CO₂.'),
          ('The lungs are muscles that pump air.', 'Lungs have no muscle of their own; the diaphragm and intercostal muscles change chest volume.')],
    cases=[('Smoking bans in public places', 'Many countries banned smoking in enclosed public places from the 2000s; studies showed fewer hospital admissions for heart attacks and asthma afterwards.', 'public health evidence', 'Reducing exposure to second-hand smoke had measurable health benefits within a few years.')],
    evaluate=[('E-cigarettes should be banned for everyone because they are unsafe.', ['contain addictive nicotine', 'long-term effects are not fully known', 'flavours attract young people'], ['far fewer harmful chemicals than tobacco smoke', 'help adult smokers quit'], 'They should be strictly controlled for young people, but may reduce harm for adult smokers trying to quit.'),
              ('Air quality in cities is a bigger threat to lung health than smoking.', ['affects everyone, including children, who cannot choose', 'linked to asthma and lung cancer'], ['smoking causes far more lung cancer per person exposed'], 'For individuals, smoking is the bigger risk, but air pollution affects many more people, so both need action.')],
    extended=[('Use the bell-jar model of the lungs to explain how inhalation happens, and give one limitation of the model.', 'Pulling the rubber sheet (diaphragm) down increases the volume inside the jar; pressure falls below atmospheric; air enters the balloons (lungs) through the tube (trachea), which inflate. Limitations: rigid jar does not move like ribs (no intercostal muscles); balloons are not elastic tissue with alveoli; no gas exchange shown.', 5)],
))


@R.add('ch04-st3', 'C3', (1, 5), 'numerical')
def breathing(rng, slot):
    k = rng.choice(['vent', 'pct'])
    if k == 'vent':
        bpm = rng.choice([12, 14, 16, 20, 30, 40])
        tv = rng.choice([0.5, 0.6, 1.2, 2.0, 2.5])
        return dict(stem=f'A person takes {bpm} breaths per minute with {tv} dm³ of air per breath. Calculate the volume of air breathed per minute.', answer=f'{g(bpm * tv)} dm³/min',
                    markingKey=f'M1 breathing rate × volume per breath = {bpm} × {tv}; A1 {g(bpm * tv)} dm³/min.', marks=2)
    vol = rng.choice([6, 8, 10, 12])
    o_in, o_out = 21, rng.choice([15, 16, 17])
    used = vol * (o_in - o_out) / 100
    return dict(stem=f'Inhaled air contains {o_in}% oxygen and exhaled air contains {o_out}% oxygen. A person breathes {vol} dm³ of air per minute. Calculate the volume of oxygen absorbed into the blood each minute.', answer=f'{g(used)} dm³',
                markingKey=f'M1 difference = {o_in - o_out}%; M1 {vol} × {o_in - o_out} ÷ 100; A1 {g(used)} dm³.', marks=3)


inquiry('ch04-st3',
        dict(ctx='how the number of minutes of exercise affects breathing rate',
             iv='duration of jogging on the spot (0, 1, 2, 3, 4 min)', dv='number of breaths per minute counted immediately after exercise',
             cvs=[('intensity of jogging (metronome)', 'faster jogging needs more energy'), ('the same person', 'fitness differs'), ('rest between trials until breathing is normal', 'previous exercise affects results'), ('room temperature', 'heat affects breathing')],
             hyp='If exercise lasts longer, then breathing rate will increase, because muscles respire faster, producing more CO₂ and needing more oxygen.',
             method='Sit still for 5 min and count breaths for 1 min; jog on the spot to a metronome for 1 min; count breaths for the next minute; rest until breathing returns to normal; repeat for 2, 3 and 4 min; repeat the whole set on three days; plot a line graph.',
             weak=('the person knew they were being counted and changed their breathing', 'count chest movements discreetly or use a chest-strap sensor'),
             safety='stop if dizzy; anyone with asthma should keep an inhaler nearby or not take part'))
dataset('ch04-st3',
        dict(intro='{who} measured the vital capacity (largest volume breathed out in one breath) of students of different heights, three blows each.', iv=('Height', 'cm'), xs=[140, 150, 160, 170, 180],
             dv=('Vital capacity', 'dm³'), f=lambda x: 0.045 * x - 3.5, dp=2, trend='Vital capacity increases as height increases.',
             why='Taller people generally have larger chest cavities and lungs, so they can hold and breathe out a larger volume of air.'))

R.facts('ch04-st4', F(
    terms=[('aerobic respiration', 'respiration using oxygen: glucose + oxygen → carbon dioxide + water, releasing a lot of energy'),
           ('anaerobic respiration', 'respiration without oxygen, releasing much less energy from glucose'),
           ('lactic acid', 'the product of anaerobic respiration in animal muscles'),
           ('oxygen debt', 'the extra oxygen needed after exercise to break down lactic acid'),
           ('fermentation', 'anaerobic respiration in yeast, producing ethanol and carbon dioxide')],
    facts=[('What is the word equation for aerobic respiration?', 'glucose + oxygen → carbon dioxide + water', ['carbon dioxide + water → glucose + oxygen', 'glucose → lactic acid', 'glucose → ethanol + carbon dioxide'], 'Energy is released.'),
           ('Where in the cell does aerobic respiration happen?', 'Mitochondria', ['Nucleus', 'Chloroplasts', 'Cell wall'], 'Anaerobic happens in the cytoplasm.'),
           ('What is produced by anaerobic respiration in yeast?', 'Ethanol and carbon dioxide', ['Lactic acid only', 'Oxygen and glucose', 'Water and carbon dioxide'], 'Used in bread and brewing.'),
           ('Why do muscles feel tired during a sprint?', 'Lactic acid builds up from anaerobic respiration', ['They run out of water', 'They make too much oxygen', 'They stop respiring'], 'Muscles fatigue.'),
           ('Which releases more energy per glucose molecule?', 'Aerobic respiration', ['Anaerobic respiration', 'They release the same', 'Fermentation'], 'About 19 times as much.')],
    why=[('Explain why you keep breathing hard after a race has finished.', 'You have an oxygen debt; extra oxygen is needed to break down the lactic acid made by anaerobic respiration.'),
         ('Explain why bread dough rises when left in a warm place.', 'Yeast respires anaerobically, producing carbon dioxide bubbles that are trapped in the dough; warmth speeds up the enzymes.'),
         ('Explain why muscles respire anaerobically during intense exercise.', 'The heart and lungs cannot supply oxygen fast enough for the energy needed, so some glucose is respired without oxygen.')],
    contrast=[('aerobic respiration', 'anaerobic respiration', 'Aerobic respiration uses oxygen, produces CO₂ and water and releases a lot of energy; anaerobic uses no oxygen, produces lactic acid (animals) or ethanol and CO₂ (yeast) and releases much less energy.'),
              ('respiration', 'photosynthesis', 'Respiration releases energy from glucose using oxygen in all living cells; photosynthesis uses light to make glucose and oxygen from CO₂ and water in green plants.')],
    misc=[('Respiration produces energy.', 'Energy cannot be created; respiration releases (transfers) energy stored in glucose.'),
          ('Only animals respire.', 'All living cells respire, including plants, fungi and bacteria.')],
    cases=[('Altitude training and Kenyan runners', 'Many champion distance runners train at 2000+ m in Kenya and Ethiopia; their bodies adapt with more red blood cells, improving aerobic respiration at sea level.', 'aerobic fitness', 'Shows how the body adapts to supply more oxygen to muscles.')],
    evaluate=[('Sports drinks containing glucose are necessary for everyone who exercises.', ['supply glucose for respiration during long events', 'replace salts lost in sweat'], ['most short exercise needs only water', 'high sugar adds unwanted energy and damages teeth'], 'Sports drinks help in long endurance events, but water is enough for most everyday exercise.')],
    extended=[('Compare what happens in a sprinter’s leg muscles during a 100 m race with what happens during a slow 5 km jog, using ideas about respiration.', 'Sprint: energy demand exceeds oxygen supply, so much anaerobic respiration: glucose → lactic acid, little energy per glucose; lactic acid builds up → fatigue; oxygen debt repaid after (heavy breathing). Jog: heart and lungs supply enough oxygen; aerobic respiration in mitochondria: glucose + oxygen → CO₂ + water, much more energy per glucose; can continue for a long time.', 6)],
))


@R.add('ch04-st4', 'C3', (1, 4), 'numerical')
def yeast_co2(rng, slot):
    b = rng.choice([12, 15, 18, 24, 30, 36])
    t = rng.choice([2, 3, 4, 5])
    return dict(stem=f'Yeast in sugar solution produced {b} bubbles of carbon dioxide in {t} minutes. Calculate the rate of respiration in bubbles per minute and state one reason counting bubbles is not very accurate.', answer=f'{g(b / t)} bubbles/min; bubbles are different sizes (or some may be missed)',
                markingKey=f'M1 {b} ÷ {t}; A1 {g(b / t)} bubbles/min; B1 bubbles vary in size / hard to count – use a gas syringe.', marks=3)


inquiry('ch04-st4',
        dict(ctx='how the temperature affects the rate of anaerobic respiration in yeast',
             iv='temperature of the water bath (°C)', dv='volume of carbon dioxide collected in a gas syringe in 10 minutes',
             cvs=[('mass of yeast', 'more yeast makes more CO₂'), ('concentration and volume of sugar solution', 'substrate amount affects the rate'), ('layer of oil on top', 'keeps oxygen out so respiration is anaerobic'), ('time for each reading', 'longer gives more gas')],
             hyp='If temperature increases up to about 35 °C, then more CO₂ will be produced, because enzymes in yeast work faster; above 45 °C the rate will fall because enzymes denature.',
             method='Mix 1 g yeast with 25 cm³ 5% glucose solution in a boiling tube; cover with a layer of oil; connect to a gas syringe; place in a water bath at 20 °C for 5 min; record the gas volume after 10 min; repeat at 30, 40, 50 °C; repeat three times.',
             weak=('the tube was not given time to reach the water-bath temperature', 'leave each tube in the bath for 5 min before starting the timing'),
             safety='take care with hot water; wash hands after handling yeast'))
dataset('ch04-st4',
        dict(intro='{who} measured the concentration of lactic acid in a runner’s blood after running at different speeds on a treadmill.', iv=('Running speed', 'km/h'), xs=[8, 10, 12, 14, 16],
             dv=('Lactic acid', 'mmol/dm³'), f=lambda x: 1 + 0.06 * (x - 6) ** 2, dp=1, trend='Lactic acid concentration increases with running speed, slowly at first and then much more steeply.',
             why='At high speeds the muscles need energy faster than oxygen can be delivered, so more anaerobic respiration happens, producing lactic acid.'))
evx(R, 'ch03-st2', ('Probiotic yoghurts are worth buying to keep the digestive system healthy.', ['some strains of bacteria can reduce diarrhoea after antibiotics', 'gut bacteria help digestion and immunity'], ['many health claims are not supported by good trials', 'expensive; a varied, high-fibre diet supports gut bacteria anyway'], 'Probiotics may help in specific cases, but a high-fibre balanced diet is better evidence-based value.'))


# =============================================================================================
# ch05 Ecosystems and Interdependence
# =============================================================================================
R.facts('ch05-st1', F(
    terms=[('habitat', 'the place where an organism lives'),
           ('population', 'all the organisms of one species living in a habitat at the same time'),
           ('community', 'all the populations of different species living in a habitat'),
           ('ecosystem', 'a community of organisms together with the non-living (abiotic) parts of their environment'),
           ('abiotic factor', 'a non-living factor that affects organisms, such as temperature, light or pH'),
           ('biotic factor', 'a living factor that affects organisms, such as predators, competition or disease')],
    facts=[('Which of these is an abiotic factor?', 'Soil pH', ['Number of predators', 'Disease', 'Competition for mates'], 'It is non-living.'),
           ('All the frogs of one species in a pond form a…', 'population', ['community', 'ecosystem', 'habitat'], 'One species only.'),
           ('A pond with its fish, plants, insects, water and mud is an example of a(n)…', 'ecosystem', ['population', 'community', 'organ system'], 'Living plus non-living.'),
           ('Which is a biotic factor that could reduce a rabbit population?', 'An increase in foxes', ['Lower rainfall', 'Colder temperatures', 'Change in soil pH'], 'Predators are living.')],
    why=[('Explain why the population of a species in a habitat cannot keep increasing forever.', 'Resources such as food, water and space are limited; as numbers rise, competition, predation and disease increase until births and deaths balance.'),
         ('Explain why two species that eat the same food may not be able to live in the same small habitat.', 'They compete for the same limited food; the better competitor may out-compete the other, reducing its population.'),
         ('Explain why light intensity is an important abiotic factor in a woodland.', 'Plants need light for photosynthesis; tall trees shade the ground, so only shade-tolerant plants grow beneath them, which affects the animals that eat them.')],
    contrast=[('a population', 'a community', 'A population is all the individuals of one species in a habitat; a community is all the populations of every species living there.'),
              ('a habitat', 'an ecosystem', 'A habitat is where an organism lives; an ecosystem is the whole system of living organisms and their non-living surroundings interacting.')],
    misc=[('An ecosystem is just the animals that live in an area.', 'An ecosystem includes plants, animals, microorganisms and the abiotic environment such as soil, water and light.'),
          ('Abiotic factors are not important because they are not alive.', 'Abiotic factors such as temperature, water and light control which organisms can survive in a habitat.')],
    cases=[('Wolves return to Yellowstone (1995)', 'Wolves were reintroduced after 70 years; they reduced elk numbers and changed where elk grazed, allowing willow and aspen to recover along rivers.', 'interactions in a community', 'Changing one population affected many others – birds, beavers and even riverbanks.')],
    evaluate=[('Building a new road through a forest should be allowed if a wildlife bridge is built.', ['bridges allow animals to cross safely', 'roads bring economic benefits'], ['habitat is still lost and fragmented', 'noise, pollution and road kill continue', 'not all species use bridges'], 'Wildlife bridges reduce harm but do not remove it; alternatives that avoid the forest should be considered first.'),
              ('Zoos are important for protecting populations of endangered species.', ['captive breeding (e.g. Arabian oryx reintroduced)', 'research and education'], ['animals may suffer stress in captivity', 'protecting habitats is more effective'], 'Good zoos support conservation, but saving wild habitats matters most.')],
    extended=[('A survey finds that the population of a butterfly in a meadow fell by 60% over 10 years. Suggest three biotic and abiotic factors that could explain this, and describe how a scientist could test one of them.', 'Abiotic: warmer/drier summers, pesticide use, loss of habitat (ploughing). Biotic: fewer food plants (nettles, flowers), new predator or parasite, disease, competition. Test: e.g. compare butterfly counts in meadows with and without pesticide use over several years, using transects with the same route, time and weather conditions.', 6)],
))
inquiry('ch05-st1',
        dict(ctx='how light intensity affects the number of daisy plants in different parts of a school field',
             iv='light intensity at ground level (lux, measured with a light meter)', dv='number of daisy plants per 0.25 m² quadrat',
             cvs=[('quadrat size', 'larger quadrats include more plants'), ('time of day of light readings', 'light changes during the day'), ('the same type of grass and mowing', 'mowing affects plant growth'), ('number of quadrats (10 per area)', 'more samples are more representative')],
             hyp='If light intensity is higher, then there will be more daisies, because daisies need light for photosynthesis and cannot grow well in shade.',
             method='Choose areas from shady (under trees) to open; in each area place 10 quadrats at random coordinates; count daisies in each; measure light intensity at ground level at the same time of day; calculate mean daisies per quadrat; plot against light.',
             weak=('quadrats were thrown over the shoulder', 'use a random number generator to choose grid coordinates'),
             safety='wash hands after fieldwork; watch out for stinging plants and allergies'))
dataset('ch05-st1',
        dict(intro='{who} counted the number of woodlice under logs at different distances from a stream (three logs at each distance).', iv=('Distance from stream', 'm'), xs=[1, 3, 5, 7, 9],
             dv=('Woodlice per log', ''), f=lambda x: 40 - 4 * x, dp=0, trend='The number of woodlice decreases as distance from the stream increases.',
             why='Woodlice lose water easily through their exoskeleton, so they live in damp places; soil is damper near the stream.'))

R.facts('ch05-st2', F(
    terms=[('producer', 'an organism that makes its own food by photosynthesis, at the start of a food chain'),
           ('primary consumer', 'an animal that eats producers (a herbivore)'),
           ('secondary consumer', 'an animal that eats primary consumers'),
           ('trophic level', 'the feeding level of an organism in a food chain'),
           ('food web', 'a network of linked food chains in an ecosystem'),
           ('decomposer', 'a microorganism (bacterium or fungus) that breaks down dead organisms and recycles nutrients'),
           ('pyramid of numbers', 'a diagram showing the number of organisms at each trophic level')],
    facts=[('What do the arrows in a food chain show?', 'The direction of energy transfer', ['What eats what, from predator to prey', 'The size of the organisms', 'Where the animals live'], 'Arrow points to the eater.'),
           ('In grass → rabbit → fox, which organism is the secondary consumer?', 'Fox', ['Rabbit', 'Grass', 'Sun'], 'It eats the primary consumer.'),
           ('About what percentage of energy is passed on from one trophic level to the next?', 'About 10%', ['About 90%', '100%', 'About 50%'], 'Most is lost.'),
           ('Where does almost all the energy in a food chain come from?', 'The Sun', ['The soil', 'Water', 'Decomposers'], 'Producers capture light energy.'),
           ('Why are food chains rarely longer than five links?', 'Too little energy remains at the top levels', ['Animals cannot eat more than five things', 'Plants stop growing', 'Decomposers eat the top predators'], 'Energy is lost at each level.')],
    why=[('Explain why energy is lost at each step of a food chain.', 'Organisms use energy for respiration, movement and keeping warm (lost as heat); some material is not eaten (bones, roots) or not digested (faeces).'),
         ('Explain why removing a predator from a food web can affect many other species.', 'Its prey may increase and overeat their food, reducing plant populations and other animals that depend on them.'),
         ('Explain why a pyramid of numbers can be an unusual shape.', 'It counts individuals regardless of size; one large tree can feed thousands of insects, so the producer bar is narrow.')],
    contrast=[('a food chain', 'a food web', 'A food chain shows one feeding pathway; a food web shows many interconnected food chains, which is more realistic because most animals eat more than one food.'),
              ('a herbivore', 'a carnivore', 'A herbivore (primary consumer) eats plants; a carnivore eats other animals.')],
    misc=[('Arrows in a food chain point from the eater to the food.', 'Arrows show energy flow, so they point from the food to the organism that eats it.'),
          ('Energy is recycled in an ecosystem.', 'Nutrients are recycled, but energy flows through and is eventually lost as heat; new energy comes from the Sun.')],
    cases=[('DDT in food chains (1950s–60s)', 'The insecticide DDT built up in fish and then in birds of prey such as ospreys; it thinned their eggshells and populations crashed until DDT was banned.', 'bioaccumulation through trophic levels', 'Rachel Carson’s book Silent Spring (1962) led to bans and the recovery of many bird species.')],
    evaluate=[('Eating less meat is a good way to feed more people from the same land.', ['far more energy is available eating plants directly (about 10× more)', 'less land and water used'], ['some land is only suitable for grazing', 'meat is an important source of protein, iron and B12 for some'], 'Eating less meat makes food production more efficient, though some grazing land and animal foods remain useful.')],
    extended=[('In a pond food web, algae are eaten by water fleas and snails; water fleas are eaten by small fish; snails and small fish are eaten by perch. Predict and explain what happens to the other populations if a disease kills most of the snails.', 'Perch eat more small fish (less food available) → small fish decrease → water fleas increase (less predation) → algae may decrease (more grazing by fleas) or increase short-term (fewer snails grazing). Perch may decrease due to less food. Effects depend on how much each species relies on the others.', 6)],
))


@R.add('ch05-st2', 'C3', (1, 5), 'numerical')
def energy_transfer(rng, slot):
    k = rng.choice(['eff', 'next', 'chain'] if slot.d >= 2 else ['eff', 'next'])
    a = rng.choice([20000, 25000, 40000, 50000, 80000])
    p = rng.choice([8, 10, 12, 15])
    b = a * p // 100
    if k == 'eff':
        return dict(stem=f'Grass in a field stores {a} kJ/m² per year. The rabbits that eat it gain {b} kJ/m² per year. Calculate the efficiency of energy transfer from grass to rabbits.', answer=f'{p}%',
                    markingKey=f'M1 efficiency = energy transferred ÷ energy available × 100 = {b} ÷ {a} × 100; A1 {p}%.', marks=2)
    if k == 'next':
        return dict(stem=f'Producers contain {a} kJ of energy. If {p}% is transferred to the primary consumers, how much energy do they receive?', answer=f'{b} kJ',
                    markingKey=f'M1 {a} × {p} ÷ 100; A1 {b} kJ.', marks=2)
    return dict(stem=f'In the chain plants → caterpillars → blue tits → sparrowhawk, plants store {a} kJ. 10% of the energy is passed on at each step. Calculate the energy reaching the sparrowhawks and explain why so little reaches them.', answer=f'{g(a * 0.001)} kJ; energy is lost at each step as heat from respiration, movement and in uneaten or undigested parts',
                markingKey=f'M1 {a} × 0.1 × 0.1 × 0.1; A1 {g(a * 0.001)} kJ; B1 losses by respiration/heat, movement, waste, uneaten parts.', marks=3)


inquiry('ch05-st2',
        dict(ctx='how the number of aphids on a plant affects the number of ladybirds feeding there',
             iv='number of aphids per plant (counted)', dv='number of ladybirds on the plant after 24 hours',
             cvs=[('species and size of plant', 'larger plants have more places to hide'), ('starting number of ladybirds released nearby', 'affects how many arrive'), ('temperature and weather', 'insects are less active when cold'), ('time of observation', 'activity varies with time of day')],
             hyp='If there are more aphids on a plant, then more ladybirds will be found there, because ladybirds are predators that move to where their food is most plentiful.',
             method='Set up 10 bean plants in a greenhouse with 0, 20, 40, 60 and 80 aphids (two plants each); release 20 ladybirds in the centre of the room; after 24 h count ladybirds on each plant; repeat three times with fresh insects; plot mean ladybirds against aphid number.',
             weak=('plants were placed at different distances from the release point', 'place plants in a circle at equal distances from the release point'),
             safety='handle insects gently with a soft paintbrush; wash hands after handling plants and soil'))
dataset('ch05-st2',
        dict(intro='{who} used published data to compare the mass of each trophic level in an ocean food chain (three surveys).', iv=('Trophic level', ''), xs=[1, 2, 3, 4, 5],
             dv=('Biomass', 'g/m²'), f=lambda x: 5000 * 0.1 ** (x - 1), dp=1, trend='The biomass decreases sharply at each higher trophic level.',
             why='Only about 10% of energy and biomass is passed to the next level, because much is lost through respiration, movement and waste.'))

R.facts('ch05-st3', F(
    terms=[('photosynthesis', 'the process in which plants use light energy to make glucose and oxygen from carbon dioxide and water'),
           ('chlorophyll', 'the green pigment in chloroplasts that absorbs light energy'),
           ('stomata', 'tiny pores, mainly on the underside of a leaf, that let carbon dioxide in and oxygen out'),
           ('limiting factor', 'a factor in short supply that stops the rate of photosynthesis increasing'),
           ('starch', 'the insoluble carbohydrate that plants make from glucose for storage')],
    facts=[('What is the word equation for photosynthesis?', 'carbon dioxide + water → glucose + oxygen', ['glucose + oxygen → carbon dioxide + water', 'oxygen + water → glucose + carbon dioxide', 'carbon dioxide + oxygen → glucose + water'], 'Light energy is absorbed by chlorophyll.'),
           ('Why is a leaf boiled in ethanol before testing it for starch?', 'To remove the chlorophyll so the iodine colour can be seen', ['To add starch', 'To kill bacteria', 'To make the leaf green'], 'Leaf turns white.'),
           ('A variegated leaf has white and green parts. Where is starch found after testing?', 'Only in the green parts', ['Only in the white parts', 'Everywhere', 'Nowhere'], 'Chlorophyll is needed.'),
           ('Which gas is produced by photosynthesis?', 'Oxygen', ['Carbon dioxide', 'Nitrogen', 'Hydrogen'], 'It can be collected from pondweed.'),
           ('Why does a plant kept in the dark for 48 hours give a negative starch test?', 'It used up its starch and could not make more without light', ['Darkness destroys iodine', 'It stored more starch', 'Starch turns into chlorophyll'], 'Destarching before an experiment.')],
    why=[('Explain why the rate of photosynthesis stops increasing at high light intensity.', 'Another factor such as carbon dioxide concentration or temperature becomes limiting, so extra light has no effect.'),
         ('Explain why farmers add carbon dioxide to greenhouses.', 'CO₂ is often the limiting factor; more CO₂ increases the rate of photosynthesis, so crops grow faster and give higher yields.'),
         ('Explain why plants produce oxygen during the day but take in oxygen at night.', 'In daylight photosynthesis is faster than respiration so there is a net release of oxygen; at night only respiration happens, which uses oxygen.')],
    contrast=[('photosynthesis', 'respiration in plants', 'Photosynthesis uses light, CO₂ and water to make glucose and oxygen in chloroplasts, only in light; respiration uses glucose and oxygen to release energy in mitochondria, all the time.'),
              ('glucose', 'starch', 'Glucose is the soluble sugar made in photosynthesis and used in respiration; starch is the insoluble storage form that does not affect osmosis.')],
    misc=[('Plants get their food from the soil.', 'Plants make their own food (glucose) by photosynthesis; the soil provides water and mineral ions, not food.'),
          ('Most of a tree’s mass comes from soil.', 'Most of a tree’s mass comes from carbon dioxide from the air, fixed by photosynthesis.')],
    cases=[('Jan van Helmont’s willow tree (1640s)', 'He grew a willow in a weighed pot of soil for 5 years, adding only water; the tree gained about 74 kg while the soil lost only 57 g.', 'evidence about plant growth', 'He concluded mass came from water (partly right); later scientists showed most comes from CO₂ in the air.'),
           ('Joseph Priestley’s mouse and mint (1771)', 'A mouse in a sealed jar died, but a mouse in a sealed jar with a mint plant survived; the plant “restored” the air.', 'plants produce oxygen', 'It was early evidence that plants produce the gas animals need – later identified as oxygen.')],
    evaluate=[('Artificial lighting in greenhouses to grow food all year is a good idea.', ['higher yields and local food in winter', 'less food transport'], ['electricity costs and greenhouse-gas emissions if from fossil fuels', 'only worthwhile for high-value crops'], 'Worthwhile with renewable electricity and high-value crops; otherwise the energy cost can outweigh the benefits.')],
    extended=[('Describe how to show that light is needed for photosynthesis using a destarched plant, a strip of foil and iodine. Explain the expected results.', 'Destarch a plant in the dark for 48 h; cover part of a leaf with a foil strip on both sides; place in light for several hours; remove leaf, dip in boiling water (kills cells), warm in ethanol in a water bath (removes chlorophyll; no flames), rinse; add iodine. Uncovered part turns blue-black (starch made); covered part stays orange-brown – no light, no photosynthesis.', 6)],
))


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def pondweed(rng, slot):
    k = rng.choice(['rate', 'inverse'] if slot.d >= 3 else ['rate'])
    if k == 'rate':
        b = rng.choice([18, 24, 30, 36, 45, 54])
        t = rng.choice([2, 3])
        return dict(stem=f'A piece of pondweed produced {b} bubbles of oxygen in {t} minutes. Calculate the rate of photosynthesis in bubbles per minute.', answer=f'{g(b / t)} bubbles per minute',
                    markingKey=f'M1 {b} ÷ {t}; A1 {g(b / t)} bubbles/min.', marks=2)
    d1, d2 = rng.choice([(10, 20), (20, 40), (15, 30)])
    r1 = rng.choice([40, 60, 80])
    r2 = r1 * (d1 / d2) ** 2
    return dict(stem=f'Light intensity is proportional to 1/d², where d is the distance from the lamp. Pondweed makes {r1} bubbles/min at {d1} cm. Assuming light is the only limiting factor, predict the rate at {d2} cm.', answer=f'{g(r2)} bubbles/min',
                markingKey=f'M1 doubling distance → light intensity × ¼ (({d1}/{d2})² = {g((d1 / d2) ** 2)}); M1 {r1} × {g((d1 / d2) ** 2)}; A1 {g(r2)} bubbles/min.', marks=3)


inquiry('ch05-st3',
        dict(ctx='how the distance of a lamp affects the rate of photosynthesis of pondweed',
             iv='distance of the lamp from the pondweed (10, 20, 30, 40, 50 cm)', dv='volume of oxygen collected in 5 minutes in a gas syringe',
             cvs=[('temperature (a beaker of water as a heat shield)', 'lamps also heat the water'), ('CO₂ concentration (add the same mass of sodium hydrogencarbonate)', 'CO₂ is a limiting factor'), ('the same piece and length of pondweed', 'leaf area affects rate'), ('background light (dark room)', 'other light changes intensity')],
             hyp='If the lamp is closer, then more oxygen will be produced, because light intensity is greater, so photosynthesis is faster.',
             method='Place a 10 cm piece of pondweed in 0.1% sodium hydrogencarbonate solution in a boiling tube; place a lamp 10 cm away behind a water heat shield in a dark room; leave 5 min to adjust; collect gas for 5 min in a gas syringe; repeat at each distance; repeat three times; plot volume against distance.',
             weak=('the lamp heated the water at short distances', 'use an LED lamp or put a beaker of water between lamp and tube and monitor temperature'),
             safety='keep water away from the lamp and electrical sockets; lamps get hot'))
dataset('ch05-st3',
        dict(intro='{who} counted bubbles from pondweed at different light intensities.', iv=('Light intensity', 'arbitrary units'), xs=[10, 20, 30, 40, 50],
             dv=('Bubbles per minute', ''), f=lambda x: 60 * x / (x + 25), dp=0, trend='The rate of bubbling increases with light intensity, but increases by less at higher intensities, starting to level off.',
             why='At low light, light is the limiting factor; at higher intensities another factor such as CO₂ concentration or temperature starts to limit the rate.'))

R.facts('ch05-st4', F(
    terms=[('adaptation', 'a feature that helps an organism survive and reproduce in its environment'),
           ('interdependence', 'the way organisms in a community depend on each other for food, shelter, pollination and seed dispersal'),
           ('competition', 'when organisms need the same limited resource, such as food, light or mates'),
           ('biodiversity', 'the variety of different species in an area'),
           ('eutrophication', 'the excess growth of algae in water caused by fertilisers, leading to oxygen loss and death of aquatic life')],
    facts=[('Why do cacti have spines instead of leaves?', 'To reduce water loss and protect from animals', ['To absorb more light', 'To attract pollinators', 'To store starch'], 'Less surface area for evaporation.'),
           ('Which adaptation helps a polar bear survive in the Arctic?', 'Thick layer of fat and dense fur', ['Large ears to lose heat', 'Thin skin', 'Dark fur to hide on snow'], 'Insulation reduces heat loss.'),
           ('Bees and flowering plants are interdependent because…', 'bees get nectar and the plants are pollinated', ['bees eat the plants', 'plants eat the bees', 'neither benefits'], 'Both benefit.'),
           ('What do plants compete for?', 'Light, water, space and mineral ions', ['Food and mates', 'Territory only', 'Oxygen only'], 'Animals compete for food, territory and mates.'),
           ('Which human activity most directly reduces biodiversity in rainforests?', 'Deforestation', ['Recycling', 'Planting hedgerows', 'Setting up nature reserves'], 'Habitats are destroyed.')],
    why=[('Explain why camels can survive in deserts.', 'They store fat in the hump (energy, and heat loss elsewhere), produce little urine and sweat, have wide feet for sand and long eyelashes against sand.'),
         ('Explain how fertiliser running off farmland can kill fish in a lake.', 'Algae grow rapidly and block light; plants die; bacteria decompose them and use up oxygen through respiration, so fish suffocate.'),
         ('Explain why the loss of one species of pollinating insect could affect many other species.', 'Plants that rely on it may not reproduce, reducing food and shelter for herbivores and the animals that eat them.')],
    contrast=[('a structural adaptation', 'a behavioural adaptation', 'A structural adaptation is a body feature (thick fur, webbed feet); a behavioural adaptation is something an organism does (migrating, hibernating, hunting at night).'),
              ('competition', 'predation', 'In competition organisms struggle for the same resource; in predation one organism kills and eats another.')],
    misc=[('Animals adapt during their lifetime because they need to.', 'Adaptations are inherited features that become common over many generations because individuals with them survive and reproduce better.'),
          ('Human impact on ecosystems is always harmful.', 'Some actions help biodiversity, such as nature reserves, hedgerows, breeding programmes and reducing pollution.')],
    cases=[('The great Pacific garbage patch', 'Ocean currents concentrate floating plastic debris in the North Pacific; seabirds and turtles eat plastic, and microplastics enter food chains.', 'human impact on ecosystems', 'It shows how waste far from its source harms marine animals and has led to campaigns to cut single-use plastic.')],
    evaluate=[('Palm oil should be banned to protect rainforests.', ['palm plantations replace rainforest, threatening orangutans', 'peat burning releases CO₂'], ['palm oil gives more oil per hectare than alternatives, so other crops could need more land', 'millions of farmers depend on it'], 'Certified sustainable palm oil is better than a total ban, which could shift damage elsewhere.'),
              ('Introducing a predator to control a pest is better than using pesticides.', ['targets one pest, less chemical pollution'], ['the predator may eat native species (e.g. cane toads in Australia)', 'hard to reverse'], 'Biological control can work but needs careful research before release.')],
    extended=[('Explain how intensive farming can reduce biodiversity and describe three ways farmers can reduce this impact.', 'Monocultures remove varied habitats; hedgerow removal destroys nesting sites and food; pesticides kill non-target insects; fertiliser run-off causes eutrophication. Reduce: replant hedgerows and field margins with wildflowers; crop rotation and organic or targeted pest control; buffer strips by rivers and careful fertiliser use; leave areas uncultivated.', 6)],
))
inquiry('ch05-st4',
        dict(ctx='how the thickness of fur (insulation) affects the cooling of a model animal',
             iv='number of layers of cotton wool around a flask (0, 1, 2, 3, 4)', dv='temperature drop of hot water in the flask after 15 minutes',
             cvs=[('starting temperature of water (60 °C)', 'hotter water cools faster'), ('volume of water', 'more water holds more energy'), ('size and type of flask', 'surface area affects cooling'), ('room temperature and draughts', 'affect heat loss')],
             hyp='If there are more layers of insulation, then the temperature drop will be smaller, because trapped air is a poor conductor and reduces heat loss – like thick fur on Arctic animals.',
             method='Fill identical conical flasks with 100 cm³ water at 60 °C; wrap with 0–4 layers of cotton wool held with elastic bands; insert a thermometer through a lid; record temperature after 15 min; repeat three times; plot temperature drop against number of layers.',
             weak=('the lids were left off some flasks', 'use identical insulated lids on all flasks'),
             safety='hot water can scald – fill flasks on a tray and handle carefully'))
dataset('ch05-st4',
        dict(intro='{who} counted mayfly larvae (which need well-oxygenated water) at points downstream from a farm drain where fertiliser enters a river.', iv=('Distance downstream', 'm'), xs=[50, 100, 200, 400, 800],
             dv=('Mayfly larvae per sample', ''), f=lambda x: 3 + 0.04 * x, dp=0, trend='The number of mayfly larvae increases with distance downstream from the drain.',
             why='Near the drain fertiliser causes eutrophication; decomposing algae lower oxygen levels, so mayfly larvae cannot survive; further downstream the fertiliser is diluted and oxygen levels recover.'))

R.facts('ch05-st5', F(
    terms=[('quadrat', 'a square frame used to sample plants or slow-moving animals in a known area'),
           ('transect', 'a line across a habitat along which samples are taken to show how organisms change with an abiotic factor'),
           ('random sampling', 'choosing sample positions by chance (e.g. random coordinates) to avoid bias'),
           ('percentage cover', 'the percentage of a quadrat’s area covered by a particular species'),
           ('pitfall trap', 'a container sunk into the ground to catch small crawling animals'),
           ('sweep net', 'a net swept through long grass to catch insects')],
    facts=[('Why are quadrats placed at random?', 'To avoid bias and get a representative sample', ['To find the most plants', 'To save time', 'To find the rarest species'], 'Random coordinates.'),
           ('Which sampling method is best for studying how plants change from a hedge into an open field?', 'A belt transect', ['Random quadrats', 'A pitfall trap', 'A sweep net only'], 'Change along a gradient.'),
           ('What is the area of a 50 cm × 50 cm quadrat?', '0.25 m²', ['2.5 m²', '0.5 m²', '25 m²'], '0.5 m × 0.5 m.'),
           ('Which method is best for sampling beetles on a woodland floor?', 'Pitfall traps', ['Quadrats', 'Sweep nets', 'Kick sampling'], 'They crawl in.')],
    why=[('Explain why many quadrats should be used rather than just one or two.', 'Organisms are not evenly spread; more samples give a more representative mean and a more reliable population estimate.'),
         ('Explain why pitfall traps should be checked often.', 'Trapped animals may die or predators may eat other animals in the trap, giving inaccurate results and harming wildlife.'),
         ('Explain why a transect is used rather than random sampling to study a sand dune system.', 'Conditions change gradually with distance from the sea; a transect samples along this gradient to show the pattern.')],
    contrast=[('a line transect', 'a belt transect', 'A line transect records organisms touching a line at intervals; a belt transect places quadrats at intervals along the line, giving more data.'),
              ('random sampling', 'systematic sampling', 'Random sampling uses chance positions to estimate population size; systematic sampling takes samples at regular intervals, e.g. along a transect, to show change.')],
    misc=[('Counting the number of plants in one quadrat gives the population of the whole field.', 'You must take many random quadrats, find the mean, then multiply by the total area ÷ quadrat area.'),
          ('Placing quadrats where there are lots of plants gives better results.', 'This introduces bias and overestimates the population; quadrats should be placed randomly.')],
    evaluate=[('Using apps to identify plants and animals makes field surveys as accurate as expert ecologists.', ['quick, free, encourages participation', 'large amounts of data'], ['misidentification, especially of similar species', 'experts can confirm with keys and specimens'], 'Apps are a helpful start, but accuracy improves when experts verify records.')],
    extended=[('Describe how you would estimate the number of dandelions on a 40 m × 60 m school field, and calculate an estimate if 20 quadrats of 0.25 m² contain 30 dandelions in total.', 'Lay two tapes along edges; use random number generator for coordinates; place 0.25 m² quadrats at 20 random points; count dandelions in each; mean = 30 ÷ 20 = 1.5 per quadrat = 6 per m²; field area = 2400 m²; estimate = 6 × 2400 = 14 400 dandelions.', 6)],
))


@R.add('ch05-st5', 'C3', (1, 5), 'numerical')
def quadrat_est(rng, slot):
    q = rng.choice([0.25, 1.0])
    n = rng.choice([10, 15, 20, 25])
    tot = n * rng.choice([2, 3, 4, 6]) // (2 if q == 0.25 else 1)
    L, W = rng.choice([(20, 30), (40, 50), (50, 80), (25, 40)])
    mean = tot / n
    dens = mean / q
    est = dens * L * W
    return dict(stem=f'A student placed {n} random quadrats, each {g(q)} m², in a {L} m × {W} m meadow and counted {tot} buttercups in total. Estimate the number of buttercups in the meadow.', answer=f'{g(est, 4)} buttercups',
                markingKey=f'M1 mean per quadrat = {tot} ÷ {n} = {g(mean)}; M1 per m² = {g(mean)} ÷ {g(q)} = {g(dens)}; M1 area = {L * W} m²; A1 {g(dens)} × {L * W} = {g(est, 4)}.', marks=4)


inquiry('ch05-st5',
        dict(ctx='how the percentage cover of moss changes with distance from a tree trunk',
             iv='distance from the tree trunk (0, 1, 2, 3, 4, 5 m along a transect)', dv='percentage cover of moss in a 0.25 m² quadrat with 100 small squares',
             cvs=[('the same tree and direction (north side)', 'shade and moisture differ around the tree'), ('quadrat size', 'changes the area sampled'), ('the same person estimating cover', 'judgement differs between people'), ('time of year', 'moss growth changes with season')],
             hyp='If the distance from the trunk increases, then moss cover will decrease, because further from the trunk there is less shade and the ground is drier.',
             method='Lay a tape measure from the trunk outwards; place a quadrat every 1 m; count the squares more than half covered with moss to give % cover; measure light intensity and soil moisture at each point; repeat on two other similar trees; calculate means.',
             weak=('the transect was only done once on one tree', 'repeat on several trees (or several transects) and calculate means'),
             safety='wear gloves when handling soil; wash hands; check for slippery or uneven ground'))
dataset('ch05-st5',
        dict(intro='{who} ran a belt transect up a beach from the low-tide mark and recorded the number of limpets per quadrat (three transects).', iv=('Distance from low-tide mark', 'm'), xs=[2, 4, 6, 8, 10],
             dv=('Limpets per quadrat', ''), f=lambda x: 33 - 3 * x, dp=0, trend='The number of limpets decreases further up the beach from the low-tide mark.',
             why='Higher up the beach, limpets are uncovered by the sea for longer, so they risk drying out and have less time to feed.'))


# =============================================================================================
# ch06 States of Matter and the Particle Model
# =============================================================================================
R.facts('ch06-st1', F(
    terms=[('particle model', 'the idea that all matter is made of tiny particles that are always moving'),
           ('solid', 'a state in which particles are closely packed in a regular arrangement and vibrate about fixed positions'),
           ('liquid', 'a state in which particles are close together but arranged randomly and can move past each other'),
           ('gas', 'a state in which particles are far apart, randomly arranged and move quickly in all directions'),
           ('forces of attraction', 'the forces that hold particles together; strongest in solids and weakest in gases')],
    facts=[('Why can a gas be compressed but a solid cannot?', 'Gas particles have large spaces between them', ['Gas particles are smaller', 'Solid particles move faster', 'Gases have no mass'], 'The particles can be pushed closer.'),
           ('Why do liquids take the shape of their container?', 'Their particles can move past each other', ['Their particles are fixed in place', 'They have no particles', 'Their particles are very far apart'], 'They flow.'),
           ('In which state do particles have the most energy?', 'Gas', ['Solid', 'Liquid', 'They all have the same'], 'Fastest movement.'),
           ('How are the particles arranged in a solid?', 'Closely packed in a regular pattern', ['Far apart and random', 'Close together and random', 'In a straight line'], 'They vibrate in place.'),
           ('What happens to particles when a substance is heated?', 'They gain energy and move or vibrate faster', ['They get bigger', 'They get heavier', 'They stop moving'], 'Particle size does not change.')],
    why=[('Explain, using the particle model, why solids have a fixed shape.', 'Particles are held in fixed positions by strong forces of attraction; they can only vibrate, so the shape does not change.'),
         ('Explain why gases fill any container they are put in.', 'Gas particles move quickly and randomly in all directions with very weak forces between them, so they spread out to fill the space.'),
         ('Explain why liquids cannot be easily compressed.', 'The particles are already touching, so there is almost no space to push them into.')],
    contrast=[('a liquid', 'a gas', 'In a liquid particles are close together and slide past each other, so it has a fixed volume; in a gas particles are far apart and move freely, so it fills any volume.'),
              ('a solid', 'a liquid', 'In a solid particles are in fixed, regular positions and vibrate; in a liquid they are still close but random and can move past each other, so it can flow.')],
    misc=[('Particles in a solid do not move.', 'Particles in a solid vibrate about fixed positions; they move faster as the solid is heated.'),
          ('Particles expand when a substance is heated.', 'The particles stay the same size; they move faster and further apart, so the substance expands.')],
    cases=[('Brownian motion (1827)', 'Robert Brown saw pollen grains in water jiggling randomly under a microscope; in 1905 Einstein explained this as water molecules bombarding the grains.', 'evidence for moving particles', 'It gave strong evidence that atoms and molecules exist and are constantly moving.')],
    evaluate=[('The simple particle model (particles as hard spheres) is good enough to explain everything about states of matter.', ['explains shape, flow, compression and diffusion'], ['does not show forces between particles or how particles are made of atoms', 'cannot explain why some substances are harder or have different melting points'], 'It is a useful model for many properties but has limits, so scientists use more detailed models when needed.')],
    extended=[('Draw (describe) and compare the arrangement, movement and forces between particles in ice, water and steam, and use these to explain one property of each.', 'Ice: regular, close-packed, vibrate, strong forces – fixed shape. Water: close, random, slide past each other, weaker forces – flows, takes container shape but fixed volume. Steam: far apart, random, fast in all directions, negligible forces – fills container, can be compressed.', 6)],
))
inquiry('ch06-st1',
        dict(ctx='how the temperature of a gas in a sealed syringe affects its volume',
             iv='temperature of the water bath around the syringe (°C)', dv='volume of air in the syringe read from the scale',
             cvs=[('starting volume of air', 'more air expands by more'), ('pressure (plunger free to move)', 'pressure affects volume'), ('time in the water bath (5 min)', 'the air must reach the water temperature'), ('the same syringe', 'friction differs')],
             hyp='If the temperature increases, then the volume of the gas will increase, because the particles move faster and push the plunger out further.',
             method='Seal a 50 cm³ syringe containing 30 cm³ of air; clamp it in a water bath at 10 °C for 5 min; tap the plunger and read the volume; repeat at 20, 30, 40, 50 and 60 °C; repeat three times; plot volume against temperature.',
             weak=('the plunger stuck because of friction', 'lubricate the plunger or use a glass syringe and tap it gently before reading'),
             safety='take care with hot water; clamp the syringe securely'))
dataset('ch06-st1',
        dict(intro='{who} heated a sealed flask of air and measured the pressure inside with a pressure sensor (three runs).', iv=('Temperature', '°C'), xs=[0, 20, 40, 60, 80],
             dv=('Pressure', 'kPa'), f=lambda x: 100 * (x + 273) / 273, dp=0, trend='The pressure increases steadily as temperature increases.',
             why='At higher temperature gas particles move faster, so they collide with the walls more often and with more force, increasing pressure.'))

R.facts('ch06-st2', F(
    terms=[('melting', 'the change from solid to liquid at the melting point'),
           ('boiling', 'rapid change from liquid to gas throughout the liquid at the boiling point'),
           ('evaporation', 'the change from liquid to gas at the surface, at any temperature'),
           ('condensation', 'the change from gas to liquid when a gas cools'),
           ('sublimation', 'the change from solid directly to gas without becoming a liquid'),
           ('freezing', 'the change from liquid to solid at the freezing point')],
    facts=[('What is the name of the change of state from gas to liquid?', 'Condensation', ['Evaporation', 'Sublimation', 'Melting'], 'e.g. water on a cold window.'),
           ('Which substance sublimes at room temperature?', 'Solid carbon dioxide (dry ice)', ['Ice', 'Salt', 'Iron'], 'It turns straight to gas.'),
           ('What is the boiling point of pure water at sea level?', '100 °C', ['0 °C', '37 °C', '212 °C'], 'It is lower at high altitude.'),
           ('Why does sweating cool you down?', 'Evaporation of sweat takes energy from the skin', ['Sweat is cold', 'Sweat reflects sunlight', 'It makes you lighter'], 'Fastest particles escape.'),
           ('A substance melts at −39 °C and boils at 357 °C. What state is it at 25 °C?', 'Liquid', ['Solid', 'Gas', 'Plasma'], 'This is mercury.')],
    why=[('Explain why puddles dry up even when the temperature is below 100 °C.', 'Water evaporates at any temperature: the fastest-moving particles at the surface have enough energy to escape.'),
         ('Explain why water condenses on the outside of a cold can of drink.', 'Water vapour in the air touches the cold surface, loses energy and condenses into droplets.'),
         ('Explain why salt is spread on icy roads.', 'Salt lowers the freezing point of water, so ice melts and water does not refreeze until the temperature is lower.')],
    contrast=[('evaporation', 'boiling', 'Evaporation happens only at the surface and at any temperature; boiling happens throughout the liquid, with bubbles, at a fixed boiling point.'),
              ('melting', 'dissolving', 'Melting is one substance changing from solid to liquid when heated; dissolving is a solute mixing with a solvent to form a solution.')],
    misc=[('Changes of state change the substance into a new substance.', 'Changes of state are physical changes; the particles are the same and the change is reversible.'),
          ('Steam is the white cloud you see above a kettle.', 'Steam is invisible water vapour; the white cloud is tiny droplets that have already condensed.')],
    cases=[('Freeze-drying coffee and space food', 'Food is frozen then put in a vacuum, where the ice sublimes straight to vapour, leaving a light, dry product that keeps for years.', 'sublimation in technology', 'NASA used freeze-dried food from the 1960s, and it is now used for coffee, medicines and camping food.')],
    evaluate=[('Using evaporative coolers instead of air conditioning is better in hot countries.', ['use much less electricity', 'cheap to run'], ['only work well in dry air – not in humid climates', 'use water, which may be scarce'], 'Evaporative coolers are a good low-energy choice in hot, dry places but not humid ones.')],
    extended=[('Explain, using particles and energy, what happens when an ice cube at −10 °C is heated until it becomes steam at 110 °C.', 'Solid: particles vibrate faster, temperature rises to 0 °C. Melting at 0 °C: energy breaks some forces, temperature constant, particles start to move past each other. Liquid warms to 100 °C: particles move faster. Boiling at 100 °C: energy overcomes remaining forces, particles escape as gas, temperature constant. Gas heats to 110 °C: particles move faster.', 6)],
))


@R.add('ch06-st2', 'C3', (1, 4), 'mcq')
def state_at_t(rng, slot):
    subs = [('oxygen', -218, -183), ('ethanol', -114, 78), ('iron', 1538, 2862), ('bromine', -7, 59), ('sodium chloride', 801, 1413), ('nitrogen', -210, -196), ('wax', 60, 370), ('gallium', 30, 2400)]
    n, mp, bp = rng.choice(subs)
    t = rng.choice([-200, -50, 0, 25, 50, 100, 500, 1000])
    st_ = 'solid' if t < mp else ('liquid' if t < bp else 'gas')
    return mcq(rng, f'{n.capitalize()} has a melting point of {mp} °C and a boiling point of {bp} °C. What state is it in at {t} °C?', st_, [x for x in ['solid', 'liquid', 'gas', 'it cannot exist at this temperature'] if x != st_][:3],
               f'B1 {st_}: below {mp} °C solid, between {mp} and {bp} °C liquid, above {bp} °C gas.')


inquiry('ch06-st2',
        dict(ctx='how the surface area of water affects the rate of evaporation',
             iv='surface area of the container (dishes of different diameters)', dv='mass of water lost in 24 hours, measured with a balance',
             cvs=[('starting volume of water (50 cm³)', 'more water may evaporate longer'), ('temperature and air movement', 'both speed up evaporation'), ('humidity of the room', 'damp air slows evaporation'), ('time (24 h)', 'longer time loses more')],
             hyp='If the surface area is larger, then more water will evaporate, because more particles are at the surface where they can escape.',
             method='Measure 50 cm³ water into five dishes with different diameters; calculate surface area (πr²); weigh each dish; leave them side by side in the same room for 24 h; reweigh; calculate mass lost; repeat three times; plot mass lost against surface area.',
             weak=('some dishes were placed near a sunny window', 'place all dishes together away from windows and heaters'),
             safety='wipe up spills to avoid slips; handle glass dishes carefully'))
dataset('ch06-st2',
        dict(intro='{who} measured the time taken for 10 cm³ of ethanol to evaporate completely from a dish with a fan at different speeds.', iv=('Fan speed setting', ''), xs=[1, 2, 3, 4, 5],
             dv=('Evaporation time', 'min'), f=lambda x: 30 / x + 4, dp=1, trend='The evaporation time decreases as fan speed increases, with smaller decreases at higher speeds.',
             why='Moving air carries away ethanol vapour above the surface, so escaped particles are less likely to return to the liquid and evaporation is faster.'))

R.facts('ch06-st3', F(
    terms=[('heating curve', 'a graph of temperature against time as a substance is heated'),
           ('cooling curve', 'a graph of temperature against time as a substance cools'),
           ('melting point', 'the temperature at which a solid melts; equal to the freezing point'),
           ('latent heat', 'energy taken in or given out during a change of state without a change in temperature'),
           ('plateau', 'a flat (horizontal) part of a heating or cooling curve where the state is changing')],
    facts=[('Why is there a flat section on a heating curve?', 'Energy is used to break forces between particles while the state changes', ['The heater has switched off', 'The particles stop moving', 'The thermometer is broken'], 'Temperature stays constant.'),
           ('On a cooling curve of stearic acid, the flat part is at 69 °C. What is this?', 'The freezing (melting) point', ['The boiling point', 'Room temperature', 'The heating rate'], 'It solidifies there.'),
           ('A pure substance melts at a sharp temperature. What does an impure substance do?', 'Melts over a range of temperatures', ['Never melts', 'Melts at exactly the same temperature', 'Boils instead of melting'], 'Impurities lower and widen the melting point.'),
           ('What happens to the temperature of boiling water if you heat it more strongly?', 'It stays at 100 °C but boils faster', ['It rises above 100 °C', 'It falls', 'It freezes'], 'Extra energy turns more water to steam.')],
    why=[('Explain why the temperature of a substance stays the same while it freezes, even though it is losing energy to the surroundings.', 'Forces of attraction form between particles as the liquid becomes solid, releasing energy that balances the energy lost.'),
         ('Explain why the boiling plateau on a heating curve of water is longer than the melting plateau.', 'Much more energy is needed to separate particles completely into a gas than to loosen them from a solid into a liquid.'),
         ('Explain how a melting point can be used to check the purity of a substance.', 'A pure substance melts at a sharp, known temperature; impurities lower the melting point and make it melt over a range.')],
    contrast=[('the sloping parts of a heating curve', 'the flat parts', 'On sloping parts the energy increases particle speed so temperature rises; on flat parts the energy breaks forces between particles so the state changes at constant temperature.'),
              ('a heating curve', 'a cooling curve', 'A heating curve shows temperature rising with plateaus at melting and boiling points; a cooling curve shows temperature falling with plateaus at condensing and freezing points.')],
    misc=[('If you keep heating, the temperature always keeps rising.', 'During a change of state the temperature stays constant even though energy is still being supplied.'),
          ('The melting point and freezing point of a substance are different temperatures.', 'For a pure substance they are the same temperature – it is the temperature at which solid and liquid can exist together.')],
    evaluate=[('A data logger is always better than a person reading a thermometer for drawing heating curves.', ['takes readings automatically at short intervals', 'no reading errors'], ['probes must be calibrated', 'can fail without anyone noticing', 'students learn less about reading scales'], 'Data loggers usually give better data for heating curves, if calibrated and checked.')],
    extended=[('Describe how to obtain a cooling curve for a sample of stearic acid and explain the shape you would expect.', 'Melt stearic acid in a boiling tube in a hot water bath (about 80 °C); remove, place thermometer/probe in the liquid; record temperature every 30 s for 15 min while it cools; plot temperature against time. Shape: falls quickly, then plateau at about 69 °C as it freezes (forces form, releasing energy), then falls again as the solid cools.', 6)],
))


@R.add('ch06-st3', 'C3', (1, 5), 'numerical')
def heating_curve(rng, slot):
    mp = rng.choice([44, 54, 63, 69, 80])
    r = rng.choice([2, 4, 5, 8])
    t0 = rng.choice([20, 25])
    k = rng.choice(['time', 'rate', 'energy'] if slot.d >= 2 else ['time'])
    if k == 'time':
        return dict(stem=f'A solid at {t0} °C is heated so that its temperature rises at {r} °C per minute until it starts to melt at {mp} °C. How long does it take to reach its melting point?', answer=f'{g((mp - t0) / r)} min',
                    markingKey=f'M1 temperature rise = {mp} − {t0} = {mp - t0} °C; M1 ÷ {r}; A1 {g((mp - t0) / r)} min.', marks=3)
    if k == 'rate':
        t = rng.choice([4, 5, 6, 8])
        return dict(stem=f'On a heating curve, a liquid’s temperature rises from {mp} °C to {mp + r * t} °C in {t} minutes. Calculate the rate of temperature rise.', answer=f'{r} °C/min',
                    markingKey=f'M1 ({mp + r * t} − {mp}) ÷ {t}; A1 {r} °C/min.', marks=2)
    P = rng.choice([30, 40, 50, 60])
    t = rng.choice([3, 4, 5, 6])
    return dict(stem=f'A {P} W heater supplies energy to melting ice. The temperature stays at 0 °C for {t} minutes. Calculate the energy supplied during melting (energy = power × time, time in seconds) and explain why the temperature stays constant.', answer=f'{P * t * 60} J; the energy breaks forces between particles rather than increasing their speed',
                markingKey=f'M1 time = {t} × 60 = {t * 60} s; M1 {P} × {t * 60}; A1 {P * t * 60} J; B1 energy used to break forces/change state.', marks=4)


inquiry('ch06-st3',
        dict(ctx='how the amount of salt dissolved in water affects its freezing point',
             iv='mass of salt dissolved in 50 cm³ of water (0, 2, 4, 6, 8 g)', dv='freezing point read from the plateau of a cooling curve',
             cvs=[('volume of water', 'affects the concentration'), ('the same freezing mixture (ice and salt)', 'cooling rate affects the curve'), ('stirring with the thermometer', 'keeps the temperature even'), ('reading interval (30 s)', 'affects precision of the plateau')],
             hyp='If more salt is dissolved, then the freezing point will be lower, because salt particles get in the way of water particles forming the regular arrangement of ice.',
             method='Dissolve each mass of salt in 50 cm³ water; place 10 cm³ in a boiling tube in a beaker of crushed ice and salt; stir with a thermometer and record temperature every 30 s until solid; plot cooling curves and read the plateau temperature; repeat three times.',
             weak=('the plateau was hard to see because readings were every 2 min', 'take readings every 15–30 s, or use a temperature probe and data logger'),
             safety='freezing mixtures can cause cold burns – handle with gloves'))
dataset('ch06-st3',
        dict(intro='{who} recorded the temperature of molten wax as it cooled in a boiling tube (three runs).', iv=('Time', 'min'), xs=[0, 2, 4, 6, 8],
             dv=('Temperature', '°C'), f=lambda x: 85 - 7 * x if x <= 2 else (71 if x <= 6 else 71 - 6 * (x - 6)), dp=0, trend='The temperature falls quickly for the first 2 minutes, stays almost constant between 2 and 6 minutes (a plateau), then falls again.',
             why='The plateau is where the wax freezes: forces form between particles, releasing energy that keeps the temperature constant.'))

R.facts('ch06-st4', F(
    terms=[('density', 'mass per unit volume of a substance: density = mass ÷ volume'),
           ('gas pressure', 'the force per unit area caused by gas particles colliding with the walls of a container'),
           ('displacement method', 'finding the volume of an irregular object by the rise in water level when it is submerged'),
           ('diffusion', 'the spreading out of particles from high to low concentration due to their random movement'),
           ('kg/m³', 'the SI unit of density; 1 g/cm³ = 1000 kg/m³')],
    facts=[('An object floats in water. What does this tell you about its density?', 'It is less than the density of water (1 g/cm³)', ['It is greater than 1 g/cm³', 'It is exactly 1 g/cm³', 'It has no density'], 'Less dense objects float.'),
           ('Why does gas pressure in a tyre increase when more air is pumped in?', 'More particles collide with the walls each second', ['The particles get bigger', 'The particles slow down', 'The tyre gets colder'], 'More collisions → more force.'),
           ('Why does the smell of perfume spread across a room?', 'Perfume particles diffuse through the air', ['Air particles are attracted to perfume', 'Perfume particles get bigger', 'The perfume freezes'], 'Random movement.'),
           ('Why does a gas diffuse faster than a liquid?', 'Gas particles move faster with more space between them', ['Gas particles are larger', 'Gas particles are heavier', 'Liquids have no particles'], ''),
           ('Which state of a substance usually has the lowest density?', 'Gas', ['Solid', 'Liquid', 'All states have the same density'], 'Particles are far apart.')],
    why=[('Explain why ice floats on water.', 'When water freezes its particles form an open structure with more space between them, so ice is less dense than liquid water.'),
         ('Explain why an aerosol can must not be heated.', 'Heating makes the gas particles move faster and hit the walls harder and more often; the pressure could rise enough to burst the can.'),
         ('Explain why a hot-air balloon rises.', 'Heated air expands so the same mass takes up more volume; it is less dense than the surrounding cooler air.')],
    contrast=[('mass', 'density', 'Mass is the amount of matter in an object (kg); density is mass per unit volume and depends on the material, not the size of the object.'),
              ('gas pressure in a container', 'atmospheric pressure', 'Gas pressure in a container is due to particles hitting its walls; atmospheric pressure is due to the weight of air above us pressing on all surfaces.')],
    misc=[('Heavy objects sink and light objects float.', 'Whether an object floats depends on its density compared with the liquid, not its mass – huge steel ships float because their overall density is less than water.'),
          ('Cutting an object in half halves its density.', 'Both mass and volume halve, so density stays the same.')],
    cases=[('Archimedes and the golden crown', 'According to legend, Archimedes compared the water displaced by a crown and by pure gold of the same mass to test if the crown was pure.', 'density and displacement', 'Displacement is still used to find the volume and density of irregular objects.')],
    evaluate=[('Density tests are a reliable way to detect fake gold coins.', ['gold is very dense (19.3 g/cm³), most fakes are less dense', 'quick and non-destructive'], ['tungsten has almost the same density as gold', 'need accurate measurement of volume'], 'Density is a useful first check, but further tests are needed for sophisticated fakes.')],
    extended=[('Describe how to find the density of an irregular stone and a regular block of wood, and explain how you would decide whether each floats in water.', 'Stone: measure mass on a balance; fill a displacement (eureka) can, lower stone in and collect displaced water in a measuring cylinder = volume; density = mass ÷ volume. Wood: mass on balance; measure length, width, height with a ruler; volume = l × w × h; density = mass ÷ volume. If density < 1.0 g/cm³ it floats; > 1.0 g/cm³ it sinks.', 6)],
))


@R.add('ch06-st4', 'C3', (1, 5), 'numerical')
def density(rng, slot):
    k = rng.choice(['rho', 'disp', 'mass', 'block'] if slot.d >= 2 else ['rho', 'block'])
    mat, rho = rng.choice([('aluminium', 2.7), ('copper', 8.9), ('granite', 2.6), ('oak', 0.75), ('ice', 0.92), ('iron', 7.9), ('glass', 2.5), ('cork', 0.24)])
    V = rng.choice([10, 20, 25, 40, 50, 80])
    m = rho * V
    fl = 'float' if rho < 1 else 'sink'
    if k == 'rho':
        return dict(stem=f'A piece of {mat} has a mass of {g(m)} g and a volume of {V} cm³. Calculate its density and state whether it will float or sink in water.', answer=f'{g(rho)} g/cm³; it will {fl}',
                    markingKey=f'M1 density = mass ÷ volume = {g(m)} ÷ {V}; A1 {g(rho)} g/cm³; B1 {fl} (water is 1.0 g/cm³).', marks=3)
    if k == 'disp':
        v0 = rng.choice([40, 50, 60])
        return dict(stem=f'A stone of mass {g(m)} g is lowered into a measuring cylinder. The water level rises from {v0} cm³ to {v0 + V} cm³. Calculate the density of the stone.', answer=f'{g(rho)} g/cm³',
                    markingKey=f'M1 volume = {v0 + V} − {v0} = {V} cm³; M1 {g(m)} ÷ {V}; A1 {g(rho)} g/cm³.', marks=3)
    if k == 'mass':
        return dict(stem=f'The density of {mat} is {g(rho)} g/cm³. Calculate the mass of a {V} cm³ piece.', answer=f'{g(m)} g',
                    markingKey=f'M1 mass = density × volume = {g(rho)} × {V}; A1 {g(m)} g.', marks=2)
    a, b, c = rng.choice([(2, 3, 4), (5, 2, 2), (4, 4, 2), (10, 2, 1), (3, 3, 3)])
    mm = round(rho * a * b * c, 1)
    return dict(stem=f'A block of {mat} measures {a} cm × {b} cm × {c} cm and has a mass of {g(mm)} g. Calculate its density.', answer=f'{g(mm / (a * b * c))} g/cm³',
                markingKey=f'M1 volume = {a} × {b} × {c} = {a * b * c} cm³; M1 {g(mm)} ÷ {a * b * c}; A1 {g(mm / (a * b * c))} g/cm³.', marks=3)


inquiry('ch06-st4',
        dict(ctx='how the concentration of salt water affects its density',
             iv='mass of salt dissolved in 100 cm³ of water (0, 5, 10, 15, 20 g)', dv='density of the solution – mass of 50 cm³ measured on a balance ÷ 50',
             cvs=[('volume of solution measured (50 cm³)', 'volume must be accurate'), ('temperature', 'density changes with temperature'), ('the same measuring cylinder and balance', 'equipment errors'), ('salt fully dissolved', 'undissolved salt adds mass but not to the solution')],
             hyp='If more salt is dissolved, then the density will increase, because the mass increases while the volume increases only slightly.',
             method='Dissolve each mass of salt in 100 cm³ water, stirring until clear; weigh an empty 50 cm³ measuring cylinder; add 50 cm³ solution (read meniscus at eye level) and reweigh; density = mass ÷ 50; repeat three times; plot density against mass of salt.',
             weak=('the meniscus was read from above', 'read the bottom of the meniscus at eye level'),
             safety='wipe up spills; salt solution can sting cuts or eyes'))
dataset('ch06-st4',
        dict(intro='{who} placed a drop of food colouring in water at different temperatures and timed how long it took to spread evenly through the beaker.', iv=('Temperature', '°C'), xs=[10, 20, 30, 40, 50],
             dv=('Time to spread', 's'), f=lambda x: 4800 / x, dp=0, trend='The time for the colour to spread decreases as temperature increases.',
             why='At higher temperatures particles move faster, so the colour particles diffuse through the water more quickly.'))


# =============================================================================================
# ch07 Elements, Compounds and Mixtures
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('atom', 'the smallest particle of an element that can exist'),
           ('element', 'a substance made of only one type of atom'),
           ('chemical symbol', 'a one- or two-letter code for an element, e.g. Na for sodium'),
           ('molecule', 'two or more atoms chemically joined together'),
           ('proton', 'a positive particle in the nucleus of an atom'),
           ('electron', 'a tiny negative particle that orbits the nucleus')],
    facts=[('What is the chemical symbol for sodium?', 'Na', ['S', 'So', 'Sd'], 'From the Latin natrium.'),
           ('What is the chemical symbol for iron?', 'Fe', ['Ir', 'I', 'In'], 'From the Latin ferrum.'),
           ('Which of these is an element?', 'Oxygen', ['Water', 'Carbon dioxide', 'Salt'], 'Made of only oxygen atoms.'),
           ('How many different elements are there approximately?', 'About 118', ['About 20', 'About 1000', 'About 50'], 'About 92 occur naturally.'),
           ('What is found in the nucleus of an atom?', 'Protons and neutrons', ['Electrons only', 'Protons and electrons', 'Molecules'], 'Electrons are outside the nucleus.')],
    why=[('Explain why an element cannot be broken down into simpler substances by chemical reactions.', 'It contains only one type of atom, so there is nothing simpler for it to break into chemically.'),
         ('Explain why oxygen gas is an element even though it is made of molecules.', 'Each O₂ molecule contains only oxygen atoms; the substance has only one type of atom.'),
         ('Explain why chemical symbols are useful to scientists around the world.', 'They are the same in every language, so scientists can communicate clearly and write formulae and equations.')],
    contrast=[('an atom', 'a molecule', 'An atom is a single particle of an element; a molecule is two or more atoms chemically bonded together (of the same or different elements).'),
              ('a proton', 'an electron', 'A proton is positive with relative mass 1 and is in the nucleus; an electron is negative with tiny mass and orbits the nucleus.')],
    misc=[('Atoms of all elements are the same, just in different amounts.', 'Each element has its own type of atom with a different number of protons.'),
          ('Molecules are always compounds.', 'Some molecules, such as O₂, H₂ and N₂, contain only one element and are elements.')],
    cases=[('John Dalton’s atomic theory (1803)', 'Dalton proposed that all matter is made of indivisible atoms, that atoms of one element are identical and that compounds form from atoms combining in fixed ratios.', 'development of atomic ideas', 'His model was later improved (atoms do contain smaller particles), showing how scientific models change with new evidence.')],
    evaluate=[('Dalton’s solid-sphere model of the atom should no longer be taught because it is wrong.', ['we now know atoms contain protons, neutrons and electrons'], ['still useful for explaining reactions and states of matter', 'shows how models develop'], 'Simple models remain useful when their limitations are understood.')],
    extended=[('Describe the structure of an atom and explain how the particles in it differ in charge, mass and position.', 'Tiny central nucleus containing protons (+1, mass 1) and neutrons (0, mass 1); electrons (−1, very small mass ≈ 1/1840) in shells around the nucleus; atom has equal protons and electrons so is neutral; most of the atom is empty space; number of protons identifies the element.', 5)],
))


@R.add('ch07-st1', 'C1', (1, 2), 'mcq')
def symbol(rng, slot):
    els = [('carbon', 'C'), ('calcium', 'Ca'), ('chlorine', 'Cl'), ('copper', 'Cu'), ('potassium', 'K'), ('lead', 'Pb'), ('silver', 'Ag'), ('gold', 'Au'), ('magnesium', 'Mg'), ('nitrogen', 'N'), ('sulfur', 'S'), ('zinc', 'Zn'), ('helium', 'He'), ('hydrogen', 'H'), ('neon', 'Ne'), ('aluminium', 'Al')]
    n, s = rng.choice(els)
    if rng.random() < 0.5:
        return mcq(rng, f'What is the chemical symbol for {n}?', s, rng.sample([b for a, b in els if b != s], 3), f'B1 {s}')
    return mcq(rng, f'Which element has the symbol {s}?', n, rng.sample([a for a, b in els if a != n], 3), f'B1 {n}')


inquiry('ch07-st1',
        dict(ctx='how the number of atoms in a model molecule affects its mass, using modelling kits as a model of real molecules',
             iv='number of carbon “atoms” (balls) in a model hydrocarbon chain (1 to 6)', dv='mass of the model measured on a balance',
             cvs=[('the same type of balls and connectors', 'different kits have different masses'), ('same number of hydrogen balls per carbon', 'ratio must stay the same'), ('balance zeroed', 'zero error'), ('model fully assembled', 'missing parts change mass')],
             hyp='If the number of carbon atoms increases, then the mass increases by the same amount each time, because each added CH₂ unit has the same mass.',
             method='Build models of CH₄ to C₆H₁₄ using one kit; zero the balance; weigh each model three times; calculate means; plot mass against number of carbon atoms; compare the pattern with real relative formula masses (16, 30, 44, …).',
             weak=('connectors were not counted', 'record the number of connectors and weigh one to correct for them'),
             safety='small parts – keep away from mouths; tidy up to avoid slips'))
dataset('ch07-st1',
        dict(intro='{who} measured the mass of different volumes of pure aluminium (an element) using a balance and a displacement can, three samples of each volume.', iv=('Volume', 'cm³'), xs=[2, 4, 6, 8, 10],
             dv=('Mass', 'g'), f=lambda x: 2.7 * x, dp=1, trend='The mass increases in direct proportion to the volume of aluminium.',
             why='An element contains only one type of atom; every aluminium atom has the same mass and the atoms are packed the same way, so doubling the volume doubles the number of atoms and the mass.'))

R.facts('ch07-st2', F(
    terms=[('periodic table', 'an arrangement of the elements in order of atomic number, with similar elements in vertical groups'),
           ('group', 'a vertical column of the periodic table containing elements with similar properties'),
           ('period', 'a horizontal row of the periodic table'),
           ('metal', 'an element that is usually shiny, malleable, ductile and a good conductor of heat and electricity'),
           ('non-metal', 'an element that is usually dull, brittle (if solid) and a poor conductor'),
           ('malleable', 'can be hammered into shape without breaking')],
    facts=[('Where are the metals found in the periodic table?', 'On the left and in the middle', ['On the right only', 'In the top row only', 'In the bottom row only'], 'Non-metals are on the right.'),
           ('Which property is typical of non-metals?', 'Poor conductor of electricity', ['Shiny', 'Malleable', 'High density'], 'Except graphite.'),
           ('Which non-metal is a liquid at room temperature?', 'Bromine', ['Mercury', 'Iodine', 'Chlorine'], 'Mercury is a metal.'),
           ('What do elements in the same group have in common?', 'Similar chemical properties', ['The same mass', 'The same melting point', 'The same colour'], 'Same number of outer electrons.'),
           ('Which element is a metal?', 'Magnesium', ['Sulfur', 'Carbon', 'Neon'], 'It is in group 2.'),
           ('What are the group 0 (group 18) elements called?', 'Noble gases', ['Alkali metals', 'Halogens', 'Transition metals'], 'Very unreactive.')],
    why=[('Explain why copper is used for electrical wires.', 'It is a very good electrical conductor and is ductile, so it can be drawn into thin wires.'),
         ('Explain why helium is used in balloons instead of hydrogen.', 'Both are less dense than air, but helium is unreactive (a noble gas) so it does not burn or explode.'),
         ('Explain why Mendeleev left gaps in his periodic table.', 'He arranged elements by properties and predicted that undiscovered elements would fill the gaps; when they were found they matched his predictions.')],
    contrast=[('a group', 'a period', 'A group is a vertical column of elements with similar properties; a period is a horizontal row across the table.'),
              ('metals', 'non-metals', 'Metals are shiny, malleable, good conductors with mostly high melting points; non-metals are dull, brittle, poor conductors with mostly low melting points.')],
    misc=[('All metals are solid and magnetic.', 'Mercury is a liquid, and only iron, nickel and cobalt (and some alloys) are magnetic.'),
          ('Elements are arranged in order of their mass.', 'The modern periodic table is arranged by atomic number (number of protons).')],
    cases=[('Mendeleev and gallium (1869–1875)', 'Mendeleev predicted “eka-aluminium” with density about 5.9 g/cm³; gallium was discovered in 1875 with density 5.9 g/cm³.', 'prediction in science', 'Correct predictions convinced scientists that his periodic table was a powerful scientific model.')],
    evaluate=[('Rare metals used in phones should be recycled by law.', ['limited supplies of metals like cobalt and indium', 'mining damages environments and can involve child labour'], ['recycling small amounts from devices is expensive and complex'], 'Recycling laws are justified because supplies are limited and mining causes harm, even if costs are high.')],
    extended=[('An unknown element is a shiny solid that conducts electricity and can be bent without breaking. Classify it, predict where it is in the periodic table and describe two other properties you would expect it to have.', 'It is a metal (shiny, conductor, malleable); found on the left or in the centre of the periodic table; expected: good thermal conductor, high melting point and density, forms basic oxides, sonorous, possibly reacts with acids to give hydrogen.', 5)],
))


@R.add('ch07-st2', 'C2', (1, 3), 'mcq')
def metal_or_not(rng, slot):
    props = [('shiny, conducts electricity, malleable', 'metal'), ('dull yellow solid, brittle, does not conduct', 'non-metal'),
             ('colourless gas that does not conduct', 'non-metal'), ('grey solid, high melting point, conducts heat well', 'metal'),
             ('red-brown liquid at room temperature, poor conductor', 'non-metal'), ('silvery liquid that conducts electricity', 'metal'),
             ('black solid that conducts electricity but is brittle and not shiny', 'non-metal (graphite is an exception)')]
    p, a = rng.choice(props)
    opts = ['metal', 'non-metal', 'noble gas', 'compound']
    corr = 'metal' if a == 'metal' else 'non-metal'
    return mcq(rng, f'An element is described as: {p}. Is it most likely a metal or a non-metal?', corr, [o for o in opts if o != corr], f'B1 {a}')


inquiry('ch07-st2',
        dict(ctx='how well different elements conduct electricity',
             iv='element tested (copper, iron, aluminium, carbon (graphite), sulfur, iodine)', dv='current in an ammeter in series with the sample',
             cvs=[('length and thickness of sample', 'both affect resistance'), ('voltage of the power supply', 'higher voltage gives higher current'), ('the same wires and crocodile clips', 'connections add resistance'), ('temperature', 'affects resistance')],
             hyp='If the element is a metal (or graphite), then a current will flow, because metals have free electrons that carry charge; non-metals like sulfur will not conduct.',
             method='Set up a circuit with a 3 V supply, ammeter and two crocodile clips; clamp each sample of the same length between the clips; record the current; repeat three times; classify each element.',
             weak=('samples were different thicknesses', 'use samples of the same length and cross-sectional area (or compare conduct/not conduct only)'),
             safety='iodine is harmful – handle in a sealed tube; do not touch hot wires'))
dataset('ch07-st2',
        dict(intro='{who} heated one end of a copper rod in a water bath at 80 °C and measured the temperature rise at the other end over time (three rods).', iv=('Time', 'min'), xs=[1, 2, 4, 6, 8],
             dv=('Temperature rise', '°C'), f=lambda x: 30 * (1 - math.exp(-x / 4)), dp=1, trend='The temperature at the far end rises quickly at first and then more slowly, levelling off.',
             why='Copper is a metal and a good thermal conductor – free electrons and vibrating ions transfer energy along the rod quickly; as the far end warms, the temperature difference and so the rate of transfer get smaller.'))

R.facts('ch07-st3', F(
    terms=[('compound', 'a substance made of two or more different elements chemically joined in fixed proportions'),
           ('chemical formula', 'symbols and numbers showing the elements and number of atoms in a substance, e.g. H₂O'),
           ('word equation', 'an equation showing the names of the reactants and products in a reaction'),
           ('reactant', 'a substance that reacts at the start of a chemical reaction'),
           ('product', 'a new substance made in a chemical reaction'),
           ('oxide', 'a compound of an element with oxygen')],
    facts=[('What is the formula of carbon dioxide?', 'CO₂', ['C₂O', 'CO', 'C₂O₂'], 'One carbon, two oxygen atoms.'),
           ('How many atoms are in one molecule of H₂O?', '3', ['2', '1', '4'], 'Two H and one O.'),
           ('What is the name of the compound formed when magnesium burns in oxygen?', 'Magnesium oxide', ['Magnesium oxygen', 'Magnesium dioxide', 'Oxygen magnesium'], 'Metal first, -ide ending.'),
           ('A compound ending in “-ate” contains which element as well as the others?', 'Oxygen', ['Hydrogen', 'Nitrogen', 'Carbon'], 'e.g. copper sulfate CuSO₄.'),
           ('Which is a compound?', 'Sodium chloride', ['Sodium', 'Chlorine', 'Oxygen'], 'Two elements chemically joined.')],
    why=[('Explain why the properties of a compound are different from the elements it is made from.', 'The atoms are chemically bonded into a new substance with a new arrangement, so it has new properties – e.g. sodium (reactive metal) and chlorine (toxic gas) form salt.'),
         ('Explain why a compound always has the same formula.', 'Elements combine in fixed proportions; e.g. water always has two hydrogen atoms for every oxygen atom.'),
         ('Explain why compounds can only be separated into their elements by chemical reactions.', 'The atoms are held by chemical bonds, which physical methods such as filtering or distilling cannot break.')],
    contrast=[('an element', 'a compound', 'An element contains only one type of atom; a compound contains two or more different elements chemically bonded in fixed proportions.'),
              ('a compound', 'a mixture', 'A compound has elements chemically joined in fixed proportions with new properties; a mixture has substances not chemically joined, in any proportion, keeping their own properties, and can be separated physically.')],
    misc=[('Iron sulfide is just iron and sulfur mixed together.', 'Iron sulfide is a compound; the iron and sulfur are chemically bonded and it is not magnetic, unlike a mixture of iron and sulfur.'),
          ('The small number in H₂O means there are two water molecules.', 'The subscript 2 applies to hydrogen: each molecule contains 2 hydrogen atoms and 1 oxygen atom.')],
    evaluate=[('Using chemical names is better than common names (like “salt” or “baking soda”) on food labels.', ['precise, avoids confusion', 'helps people with allergies'], ['many people do not understand chemical names', 'can make safe foods sound frightening'], 'Labels should give both: the chemical name for precision and the common name for understanding.')],
    extended=[('Iron and sulfur are heated together. Compare the mixture before heating with the product after heating, describing two tests and naming the product.', 'Before: grey iron filings and yellow sulfur visible; a magnet separates the iron; sulfur dissolves in some solvents. After heating: glows, black solid iron sulfide (a compound) forms; not attracted to magnet; fixed composition FeS; new properties. Word equation: iron + sulfur → iron sulfide.', 6)],
))


@R.add('ch07-st3', 'C3', (1, 5), 'short')
def count_atoms(rng, slot):
    f_ = rng.choice([('H₂SO₄', 'sulfuric acid', {'H': 2, 'S': 1, 'O': 4}), ('CaCO₃', 'calcium carbonate', {'Ca': 1, 'C': 1, 'O': 3}), ('NH₃', 'ammonia', {'N': 1, 'H': 3}),
                     ('C₆H₁₂O₆', 'glucose', {'C': 6, 'H': 12, 'O': 6}), ('CuSO₄', 'copper sulfate', {'Cu': 1, 'S': 1, 'O': 4}), ('NaOH', 'sodium hydroxide', {'Na': 1, 'O': 1, 'H': 1}),
                     ('CH₄', 'methane', {'C': 1, 'H': 4}), ('Mg(OH)₂', 'magnesium hydroxide', {'Mg': 1, 'O': 2, 'H': 2}), ('HNO₃', 'nitric acid', {'H': 1, 'N': 1, 'O': 3}), ('C₂H₅OH', 'ethanol', {'C': 2, 'H': 6, 'O': 1})])
    fm, nm, d = f_
    tot = sum(d.values())
    parts = ', '.join(f'{v} {k}' for k, v in d.items())
    return dict(stem=f'The formula of {nm} is {fm}. State the number of each type of atom in one unit of {fm} and the total number of atoms.', answer=f'{parts}; total {tot} atoms',
                markingKey=f'1 correct number of each element ({parts}); 1 total {tot}.', marks=2)


inquiry('ch07-st3',
        dict(ctx='how the mass of magnesium burned affects the mass of magnesium oxide formed',
             iv='mass of magnesium ribbon (0.1, 0.2, 0.3, 0.4, 0.5 g)', dv='mass of magnesium oxide formed – crucible and lid weighed before and after',
             cvs=[('heating until no further change', 'all magnesium must react'), ('lid lifted only slightly', 'prevents smoke (oxide) escaping'), ('the same crucible', 'crucibles differ in mass'), ('crucible cooled before weighing', 'hot objects give inaccurate readings')],
             hyp='If the mass of magnesium doubles, then the mass of oxide formed doubles, because magnesium and oxygen combine in a fixed ratio in the compound.',
             method='Weigh a crucible and lid; add coiled magnesium and reweigh; heat strongly, lifting the lid occasionally to let oxygen in; when no more glowing, heat for 2 more minutes; cool and reweigh; calculate oxide mass; repeat for each mass and plot mass of oxide against mass of magnesium.',
             weak=('white smoke escaped when the lid was lifted', 'lift the lid only slightly and briefly with tongs'),
             safety='do not look directly at burning magnesium; use tongs, a heatproof mat and eye protection; the crucible stays hot for a long time'))
dataset('ch07-st3',
        dict(intro='{who} heated different masses of copper powder in air until there was no further change and recorded the mass of copper oxide formed.', iv=('Mass of copper', 'g'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Mass of copper oxide', 'g'), f=lambda x: 1.25 * x, dp=2, trend='The mass of copper oxide is directly proportional to the mass of copper.',
             why='Copper and oxygen combine in a fixed ratio to form the compound copper oxide, so doubling the copper doubles the oxide formed.'))

R.facts('ch07-st4', F(
    terms=[('mixture', 'two or more substances mixed together but not chemically joined'),
           ('filtration', 'separating an insoluble solid from a liquid using filter paper'),
           ('crystallisation', 'obtaining a soluble solid from a solution by evaporating some solvent and leaving it to form crystals'),
           ('distillation', 'separating a liquid from a solution by evaporating it and condensing the vapour'),
           ('chromatography', 'separating dissolved substances, such as dyes, as a solvent moves up paper'),
           ('Rf value', 'distance moved by a substance ÷ distance moved by the solvent front in chromatography')],
    facts=[('Which method separates sand from water?', 'Filtration', ['Distillation', 'Chromatography', 'Crystallisation'], 'Sand is insoluble.'),
           ('Which method gets pure water from sea water?', 'Distillation', ['Filtration', 'Chromatography', 'Using a magnet'], 'Water evaporates and condenses.'),
           ('Which method separates the dyes in black ink?', 'Paper chromatography', ['Filtration', 'Distillation', 'Evaporation'], 'Dyes move different distances.'),
           ('Why is the start line in chromatography drawn in pencil?', 'Pencil does not dissolve in the solvent', ['Pencil is easier to see', 'Ink would dissolve the paper', 'Pencil helps dyes move'], 'Ink would separate too.'),
           ('Which method obtains copper sulfate crystals from its solution?', 'Crystallisation', ['Filtration', 'Chromatography', 'Fractional distillation'], 'Evaporate then cool.'),
           ('How can iron filings be separated from sulfur powder?', 'Using a magnet', ['Filtration', 'Distillation', 'Chromatography'], 'Iron is magnetic.')],
    why=[('Explain why a mixture of salt and sand can be separated by adding water, filtering and evaporating.', 'Salt dissolves in water but sand does not; filtration removes the sand; evaporating the filtrate leaves salt crystals.'),
         ('Explain why the dyes in ink separate in chromatography.', 'Dyes differ in solubility in the solvent and attraction to the paper; more soluble dyes are carried further up.'),
         ('Explain why a condenser is cooled with cold water in distillation.', 'The cold water cools the vapour so it condenses back into liquid that can be collected.')],
    contrast=[('evaporation to dryness', 'crystallisation', 'Evaporation to dryness removes all the solvent quickly, giving small crystals or powder; crystallisation removes some solvent and lets the solution cool slowly, giving larger, purer crystals.'),
              ('simple distillation', 'fractional distillation', 'Simple distillation separates a solvent from a solution; fractional distillation separates liquids with similar boiling points using a fractionating column.')],
    misc=[('Filtration can remove salt from sea water.', 'Salt is dissolved; dissolved particles pass through filter paper. Distillation is needed.'),
          ('In chromatography, a single spot that does not move must contain no dyes.', 'It may contain a dye that is insoluble in that solvent; try a different solvent.')],
    cases=[('Desalination in the Middle East', 'Countries such as Saudi Arabia and the UAE get much of their drinking water by distilling or using reverse osmosis on sea water.', 'separation on a large scale', 'It provides water in deserts but uses large amounts of energy and returns very salty brine to the sea.')],
    evaluate=[('Desalination is the best solution to water shortages.', ['unlimited sea water', 'reliable supply in dry regions'], ['very high energy use and cost', 'brine harms marine life', 'saving water and fixing leaks is cheaper'], 'Desalination is valuable in very dry coastal regions but should be combined with saving water and renewable energy.')],
    extended=[('Plan how to obtain pure, dry salt crystals from a mixture of rock salt (salt, sand and grit). Explain each step.', 'Grind with pestle and mortar (more surface); add warm water and stir (salt dissolves, sand doesn’t); filter (sand stays as residue, salt solution is filtrate); heat the filtrate in an evaporating basin until crystals start to form; leave to cool and crystallise; pat dry with filter paper or warm oven.', 6)],
))


@R.add('ch07-st4', 'C3', (1, 5), 'numerical')
def rf_value(rng, slot):
    sf = rng.choice([6.0, 8.0, 10.0, 12.0])
    r = rng.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8])
    d = sf * r
    if rng.random() < 0.6 or slot.d < 2:
        return dict(stem=f'In a chromatography experiment the solvent front moved {sf:g} cm and a red dye moved {d:g} cm. Calculate the Rf value of the red dye.', answer=f'{r:g}',
                    markingKey=f'M1 Rf = distance moved by dye ÷ distance moved by solvent = {d:g} ÷ {sf:g}; A1 {r:g} (no units).', marks=2)
    return dict(stem=f'A blue food dye has an Rf value of {r:g}. If the solvent front moves {sf:g} cm, how far would the dye move?', answer=f'{d:g} cm',
                markingKey=f'M1 distance = Rf × solvent distance = {r:g} × {sf:g}; A1 {d:g} cm.', marks=2)


inquiry('ch07-st4',
        dict(ctx='how the type of solvent affects how far the dyes in a felt-tip pen travel in chromatography',
             iv='solvent (water, ethanol, salt water, propanone)', dv='Rf value of each dye spot',
             cvs=[('type of chromatography paper', 'affects attraction of dyes'), ('size of ink spot', 'large spots smear'), ('start line above solvent level', 'dyes would dissolve into the solvent'), ('lid on the beaker', 'stops solvent evaporating')],
             hyp='If ethanol is used instead of water, then the dyes from a permanent pen will travel further, because they are more soluble in ethanol.',
             method='Draw a pencil line 2 cm from the bottom of four strips; add a small spot of ink; stand each strip in a different solvent below the line with a lid on; remove when the solvent is 1 cm from the top; mark the solvent front; measure distances and calculate Rf values; repeat twice.',
             weak=('the solvent level was above the start line', 'make sure the solvent level is below the pencil line'),
             safety='ethanol and propanone are flammable – no flames; use in a well-ventilated room'))
dataset('ch07-st4',
        dict(intro='{who} heated salt solution in an evaporating basin and recorded the mass of salt crystals obtained from different volumes of the same solution.', iv=('Volume of solution', 'cm³'), xs=[10, 20, 30, 40, 50],
             dv=('Mass of salt', 'g'), f=lambda x: 0.26 * x, dp=1, trend='The mass of salt obtained increases in proportion to the volume of solution evaporated.',
             why='The solution has a fixed concentration, so each cm³ contains the same mass of dissolved salt.'))

R.facts('ch07-st5', F(
    terms=[('solute', 'the substance that dissolves'),
           ('solvent', 'the liquid that the solute dissolves in'),
           ('solution', 'a mixture formed when a solute dissolves in a solvent'),
           ('soluble', 'able to dissolve in a solvent'),
           ('insoluble', 'not able to dissolve in a solvent'),
           ('saturated solution', 'a solution in which no more solute can dissolve at that temperature'),
           ('solubility', 'the maximum mass of solute that dissolves in 100 g of solvent at a given temperature')],
    facts=[('In salt water, what is the solvent?', 'Water', ['Salt', 'Salt water', 'Air'], 'The solute is salt.'),
           ('What happens to the solubility of most solids as temperature increases?', 'It increases', ['It decreases', 'It stays the same', 'It becomes zero'], 'More dissolves in hot water.'),
           ('What happens to the mass when 5 g of sugar dissolves in 100 g of water?', 'The solution has a mass of 105 g', ['The solution has a mass of 100 g', 'The mass decreases', 'The sugar disappears completely'], 'Mass is conserved.'),
           ('Which gas is less soluble in warm water than in cold water?', 'Oxygen', ['None – gases are more soluble when warm', 'Sugar', 'Salt'], 'Gas solubility falls as temperature rises.'),
           ('Which speeds up dissolving but does not change solubility?', 'Stirring', ['Heating', 'Changing the solvent', 'Adding more solute'], 'It only makes dissolving faster.')],
    why=[('Explain why the mass of a solution equals the mass of solute plus solvent.', 'No particles are lost or created; the solute particles spread out between the solvent particles.'),
         ('Explain why fizzy drinks go flat faster when warm.', 'Carbon dioxide is less soluble in warmer water, so it comes out of solution as bubbles more quickly.'),
         ('Explain why crushed sugar dissolves faster than a sugar cube.', 'Crushing increases the surface area in contact with the water, so more particles can be pulled into solution each second.')],
    contrast=[('dissolving', 'melting', 'Dissolving is a solute spreading out in a solvent to form a solution; melting is a solid turning into a liquid by heating.'),
              ('a dilute solution', 'a concentrated solution', 'A dilute solution has a small amount of solute in the solvent; a concentrated solution has a large amount of solute in the same volume.')],
    misc=[('When sugar dissolves it disappears.', 'The sugar particles are still there, spread between water particles; the mass is unchanged and you can taste it.'),
          ('Water can dissolve everything.', 'Many substances, such as sand, oil and plastics, are insoluble in water but may dissolve in other solvents.')],
    evaluate=[('Water is the most important solvent on Earth.', ['dissolves many substances, transporting nutrients in organisms and soils', 'life’s reactions take place in water'], ['many industrial and cleaning processes need other solvents (e.g. ethanol for perfumes)'], 'Water is the most important solvent for life, though other solvents are essential in industry.')],
    extended=[('Use particle ideas to explain what a saturated solution is, and describe how to make a saturated solution of potassium nitrate at 40 °C and find its solubility.', 'Saturated: no more solute can dissolve – solvent particles cannot surround any more solute particles at that temperature. Method: heat 50 g water to 40 °C in a water bath; add weighed potassium nitrate in small portions stirring until some remains undissolved; filter warm; weigh an evaporating basin, add a known mass of the solution, evaporate to dryness, weigh the solid; solubility = mass of solid ÷ mass of water × 100 g.', 6)],
))


@R.add('ch07-st5', 'C3', (1, 5), 'numerical')
def solubility(rng, slot):
    k = rng.choice(['per100', 'mass', 'crystals'] if slot.d >= 2 else ['per100', 'mass'])
    s = rng.choice([32, 36, 46, 64, 85, 110])
    if k == 'per100':
        w = rng.choice([25, 50, 200])
        return dict(stem=f'At 20 °C, a maximum of {g(s * w / 100)} g of a salt dissolves in {w} g of water. Calculate the solubility in g per 100 g of water.', answer=f'{s} g/100 g water',
                    markingKey=f'M1 {g(s * w / 100)} ÷ {w} × 100; A1 {s} g per 100 g water.', marks=2)
    if k == 'mass':
        a, b = rng.choice([(5, 100), (12, 150), (25, 200), (8, 50)])
        return dict(stem=f'{a} g of sugar is dissolved in {b} g of water. What is the mass of the solution and what is the percentage by mass of sugar?', answer=f'{a + b} g; {g(a / (a + b) * 100)}%',
                    markingKey=f'M1 {a} + {b} = {a + b} g; M1 {a} ÷ {a + b} × 100; A1 {g(a / (a + b) * 100)}%.', marks=3)
    s2 = s - rng.choice([10, 20, 25])
    return dict(stem=f'The solubility of a salt is {s} g/100 g water at 60 °C and {s2} g/100 g water at 20 °C. A saturated solution in 100 g water is cooled from 60 °C to 20 °C. What mass of crystals forms?', answer=f'{s - s2} g',
                markingKey=f'M1 {s} − {s2}; A1 {s - s2} g crystallise out.', marks=2)


inquiry('ch07-st5',
        dict(ctx='how the temperature of water affects the mass of potassium nitrate that dissolves in it',
             iv='temperature of the water (20, 30, 40, 50, 60 °C)', dv='mass of potassium nitrate that dissolves in 10 g of water before some remains undissolved',
             cvs=[('mass of water (10 g)', 'more water dissolves more'), ('stirring for the same time', 'ensures the solution is saturated'), ('adding in 0.5 g portions', 'affects the precision of the result'), ('the same batch of potassium nitrate', 'purity affects results')],
             hyp='If the temperature increases, then more potassium nitrate will dissolve, because water particles have more energy to separate the solute particles.',
             method='Put 10 g water in a boiling tube in a water bath at 20 °C; add 0.5 g portions of potassium nitrate, stirring for 1 min each, until some stays undissolved; record the total mass dissolved; repeat at each temperature; repeat three times; calculate solubility per 100 g water and plot a solubility curve.',
             weak=('the solution cooled while solid was being added', 'keep the tube in the water bath throughout and check the temperature'),
             safety='potassium nitrate is an oxidiser – keep away from flames; wear eye protection'))
dataset('ch07-st5',
        dict(intro='{who} measured the mass of a salt that dissolved in 100 g of water at different temperatures.', iv=('Temperature', '°C'), xs=[10, 20, 30, 40, 50],
             dv=('Solubility', 'g/100 g water'), f=lambda x: 20 + 0.02 * x ** 2 + 0.6 * x, dp=0, trend='The solubility increases as temperature increases, and increases more steeply at higher temperatures.',
             why='At higher temperatures water particles have more kinetic energy and can separate and surround more solute particles.'))
evx(R, 'ch06-st1', ('Scientists should replace the solid–liquid–gas model with a more complicated one in school science.', ['real substances include plasmas, gels and glasses that do not fit neatly'], ['the simple model explains most everyday observations', 'more complex models are hard to understand without the basics first'], 'The three-state particle model is a good starting point; its limits should be discussed as students meet substances it cannot explain.'))


# =============================================================================================
# ch08 Chemical Reactions
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('physical change', 'a change in which no new substance is formed and which is usually easy to reverse, e.g. melting'),
           ('chemical change', 'a change in which new substances are formed and which is usually hard to reverse'),
           ('precipitate', 'an insoluble solid formed when two solutions react'),
           ('effervescence', 'fizzing caused by a gas being produced in a reaction'),
           ('irreversible', 'cannot easily be changed back to the starting substances')],
    facts=[('Which is a chemical change?', 'Burning wood', ['Melting ice', 'Dissolving sugar', 'Boiling water'], 'New substances such as CO₂ and ash form.'),
           ('Which observation is a sign that a chemical reaction has happened?', 'A gas is given off from mixing two substances', ['Ice turns to water', 'Salt dissolves in water', 'Water evaporates from a puddle'], 'Other signs: colour change, precipitate, temperature change.'),
           ('Which is a physical change?', 'Chocolate melting', ['Iron rusting', 'Toast burning', 'Milk going sour'], 'It can be reversed by cooling.'),
           ('When two clear solutions are mixed, a cloudy yellow solid forms. What is the solid called?', 'A precipitate', ['A solvent', 'A filtrate', 'An alloy'], 'It is insoluble.')],
    why=[('Explain why a temperature change alone does not always prove a chemical reaction has happened.', 'Some physical changes, such as dissolving certain salts, also cause temperature changes; other evidence such as a new substance is needed.'),
         ('Explain why cooking an egg is a chemical change.', 'Heat changes the proteins permanently into new structures; the egg cannot be turned back to raw.'),
         ('Explain why dissolving salt in water is a physical change.', 'No new substance is made; the salt can be recovered by evaporating the water.')],
    contrast=[('a physical change', 'a chemical change', 'A physical change makes no new substance and is usually reversible (e.g. melting); a chemical change makes new substances and is usually hard to reverse (e.g. burning).'),
              ('effervescence', 'boiling', 'Effervescence is bubbles of a gas produced by a reaction (e.g. CO₂ from acid and carbonate); boiling is bubbles of the liquid’s own vapour forming when it is heated to its boiling point.')],
    misc=[('If something changes colour it must be a chemical reaction.', 'Colour change is a common sign, but physical changes (e.g. dissolving coloured crystals or heating iron until it glows) can also change colour.'),
          ('Physical changes can never be reversed.', 'Physical changes such as melting, freezing and dissolving are usually easy to reverse.')],
    cases=[('The Statue of Liberty’s green colour', 'The copper skin of the statue was originally shiny brown; over about 30 years it reacted with oxygen, water and carbon dioxide in the air to form a green patina.', 'a slow chemical change', 'The patina protects the copper underneath from further corrosion.')],
    evaluate=[('Cooking is mainly chemistry.', ['browning, baking and caramelising are chemical reactions that make new flavours', 'raising agents produce CO₂ by reactions'], ['melting butter, boiling water and dissolving sugar are physical changes'], 'Cooking combines physical and chemical changes; much of its flavour comes from chemical reactions.')],
    extended=[('Classify each change as physical or chemical and justify: (a) a candle burning, (b) wax melting, (c) a nail rusting, (d) salt dissolving. Explain why a burning candle involves both.', '(a) chemical – new substances CO₂, water, soot; irreversible; heat and light. (b) physical – no new substance, reversible on cooling. (c) chemical – iron oxide formed, colour change, irreversible. (d) physical – salt recovered by evaporation. Candle: wax melts (physical) and the vapour burns (chemical).', 6)],
))
inquiry('ch08-st1',
        dict(ctx='how the concentration of hydrochloric acid affects the time for a marble chip to stop fizzing',
             iv='concentration of hydrochloric acid (0.5, 1.0, 1.5, 2.0 mol/dm³)', dv='time until effervescence stops',
             cvs=[('volume of acid (25 cm³)', 'more acid reacts longer'), ('mass and size of marble chip', 'surface area affects rate'), ('temperature', 'heat speeds reactions'), ('swirling', 'mixing affects rate')],
             hyp='If the acid is more concentrated, then the fizzing will stop sooner, because there are more acid particles to collide with the marble each second.',
             method='Measure 25 cm³ of acid into a conical flask; add one 1 g marble chip; start a stopwatch; record time until no bubbles are seen; repeat with each concentration three times; keep temperature constant.',
             weak=('marble chips were different sizes', 'weigh chips and choose ones of similar mass and size, or use powder of a fixed mass'),
             safety='hydrochloric acid is an irritant – wear eye protection and wash spills off skin'))
dataset('ch08-st1',
        dict(intro='{who} measured the temperature change when different masses of magnesium powder were added to 25 cm³ of acid.', iv=('Mass of magnesium', 'g'), xs=[0.1, 0.2, 0.3, 0.4, 0.5],
             dv=('Temperature rise', '°C'), f=lambda x: 32 * x, dp=1, trend='The temperature rise increases in proportion to the mass of magnesium added.',
             why='The reaction releases energy; more magnesium reacting releases more energy, warming the acid more.'))

R.facts('ch08-st2', F(
    terms=[('conservation of mass', 'the total mass of reactants equals the total mass of products in a chemical reaction'),
           ('closed system', 'a system where no substances can enter or leave'),
           ('open system', 'a system where gases can escape or enter'),
           ('balanced equation', 'a symbol equation with the same number of each type of atom on both sides'),
           ('state symbols', '(s), (l), (g) and (aq) showing solid, liquid, gas and aqueous solution')],
    facts=[('Why does the mass of a beaker of acid and marble chips decrease during the reaction?', 'Carbon dioxide gas escapes into the air', ['Mass is destroyed', 'The marble evaporates', 'The acid becomes lighter'], 'In a closed flask the mass would stay the same.'),
           ('When magnesium burns in air, why does the mass of the solid increase?', 'Oxygen from the air combines with the magnesium', ['Magnesium atoms get heavier', 'Heat adds mass', 'Smoke is added to it'], 'Product: magnesium oxide.'),
           ('What is the state symbol for a substance dissolved in water?', '(aq)', ['(l)', '(s)', '(w)'], 'Aqueous.'),
           ('Which is the word equation for the reaction of zinc with sulfuric acid?', 'zinc + sulfuric acid → zinc sulfate + hydrogen', ['zinc + sulfuric acid → zinc oxide + water', 'zinc + sulfuric acid → zinc chloride + hydrogen', 'zinc + sulfuric acid → zinc sulfate + oxygen'], 'Metal + acid → salt + hydrogen.')],
    why=[('Explain why mass is conserved in a chemical reaction.', 'Atoms are not created or destroyed; they are only rearranged into new substances, so the total mass stays the same.'),
         ('Explain why a reaction must be done in a sealed container to show conservation of mass when a gas is produced.', 'Otherwise the gas escapes and its mass is not measured, so the products appear lighter.'),
         ('Explain why equations must be balanced.', 'The same atoms are present before and after the reaction, so each side must contain the same number of each type of atom.')],
    contrast=[('a word equation', 'a balanced symbol equation', 'A word equation gives names of reactants and products; a balanced symbol equation uses formulae and numbers to show the ratio of particles and the same atoms on both sides.'),
              ('an open system', 'a closed system', 'In an open system gases can escape or be taken in, so mass may appear to change; in a closed system nothing escapes, so mass is constant.')],
    misc=[('Mass is lost when wood burns because the ash is lighter.', 'The missing mass is in the gases (CO₂ and water vapour) that escape; including them, mass is conserved.'),
          ('To balance an equation you can change the small numbers in a formula.', 'You change only the large numbers in front of formulae; changing subscripts would change the substance.')],
    cases=[('Antoine Lavoisier (1770s)', 'Lavoisier carefully weighed reactants and products in sealed vessels and showed that mass is conserved; he also showed that burning is a reaction with oxygen.', 'law of conservation of mass', 'His careful measurements helped turn chemistry into a quantitative science.')],
    evaluate=[('Lavoisier’s method of weighing everything in sealed vessels was the most important step in modern chemistry.', ['led to the law of conservation of mass and the end of phlogiston theory', 'made chemistry quantitative'], ['other advances such as atomic theory and the periodic table were also essential'], 'It was one of several crucial steps; precise measurement made later theories possible.')],
    extended=[('A student heats 2.4 g of magnesium in a crucible and obtains 4.0 g of magnesium oxide. Explain the increase in mass using conservation of mass, calculate the mass of oxygen that reacted and write the word equation.', 'Mass increases because oxygen from the air (not originally weighed) combines with the magnesium; atoms are conserved. Oxygen = 4.0 − 2.4 = 1.6 g. magnesium + oxygen → magnesium oxide.', 4)],
))


@R.add('ch08-st2', 'C3', (1, 5), 'numerical')
def conserve(rng, slot):
    k = rng.choice(['gas', 'oxide', 'ppt'])
    if k == 'gas':
        a = rng.choice([150.0, 152.4, 160.5, 175.2])
        lost = rng.choice([0.8, 1.1, 1.6, 2.2])
        return dict(stem=f'A flask containing acid and marble chips had a mass of {a:.1f} g at the start. With no bung, the mass after the reaction was {a - lost:.1f} g. Calculate the mass of carbon dioxide produced and explain why the mass fell.', answer=f'{lost:.1f} g; the CO₂ gas escaped from the open flask (mass is still conserved)',
                    markingKey=f'M1 {a:.1f} − {a - lost:.1f}; A1 {lost:.1f} g; B1 gas escaped – atoms not destroyed.', marks=3)
    if k == 'oxide':
        m = rng.choice([1.2, 2.4, 3.6, 4.8])
        o = round(m * 2 / 3, 2)
        return dict(stem=f'{m} g of magnesium burns completely to form {g(m + o)} g of magnesium oxide. Calculate the mass of oxygen that reacted.', answer=f'{g(o)} g',
                    markingKey=f'M1 mass of oxygen = mass of oxide − mass of magnesium = {g(m + o)} − {m}; A1 {g(o)} g.', marks=2)
    a = rng.choice([25.0, 30.0, 40.0])
    b = rng.choice([20.0, 25.0])
    return dict(stem=f'{a:.1f} g of lead nitrate solution is mixed with {b:.1f} g of potassium iodide solution in a beaker on a balance. A yellow precipitate forms. Predict the total mass after mixing and explain.', answer=f'{a + b:.1f} g; no gas is produced and atoms are only rearranged, so mass is conserved',
                markingKey=f'1 {a + b:.1f} g; 1 no substance escapes / atoms rearranged, not created or destroyed.', marks=2)


@R.add('ch08-st2', 'C2', (1, 3), 'short')
def word_eq(rng, slot):
    r, p = rng.choice([('magnesium + hydrochloric acid', 'magnesium chloride + hydrogen'), ('copper oxide + sulfuric acid', 'copper sulfate + water'),
                       ('calcium carbonate + hydrochloric acid', 'calcium chloride + water + carbon dioxide'), ('sodium hydroxide + hydrochloric acid', 'sodium chloride + water'),
                       ('iron + sulfur', 'iron sulfide'), ('methane + oxygen', 'carbon dioxide + water'), ('zinc + copper sulfate', 'zinc sulfate + copper'),
                       ('sodium + water', 'sodium hydroxide + hydrogen')])
    return dict(stem=f'Complete the word equation: {r} → ?', answer=p, markingKey=f'1-2 {p} (1 mark per correct product).', marks=2)


inquiry('ch08-st2',
        dict(ctx='whether mass is conserved when sodium hydrogencarbonate reacts with vinegar in an open and a sealed container',
             iv='type of container (open flask or flask sealed with a balloon)', dv='change in total mass measured on a balance (to 0.01 g)',
             cvs=[('mass of sodium hydrogencarbonate (2 g)', 'more produces more gas'), ('volume of vinegar (50 cm³)', 'affects how much reacts'), ('the same balance', 'different balances may read differently'), ('time before reweighing', 'reaction must be complete')],
             hyp='If the flask is sealed, then the total mass will not change, because the carbon dioxide produced cannot escape, so all the atoms are still weighed.',
             method='Put 50 cm³ vinegar in a flask and 2 g sodium hydrogencarbonate in a balloon; weigh everything together; tip the powder in (sealed) or add to an open flask; after the fizzing stops, reweigh; repeat three times for each container; compare mass changes.',
             weak=('the balloon was not tied tightly and some gas leaked', 'secure the balloon with an elastic band or use a bung and gas syringe'),
             safety='wear eye protection; vinegar can sting eyes'))
dataset('ch08-st2',
        dict(intro='{who} heated copper carbonate in an open tube and recorded the mass of solid remaining after different heating times.', iv=('Heating time', 'min'), xs=[0, 2, 4, 6, 8],
             dv=('Mass of solid', 'g'), f=lambda x: 5.0 - 1.8 * (1 - math.exp(-x / 2.5)), dp=2, trend='The mass of solid decreases quickly at first and then levels off.',
             why='Copper carbonate decomposes into copper oxide and carbon dioxide; the gas escapes, so the solid loses mass until all the carbonate has decomposed.'))

R.facts('ch08-st3', F(
    terms=[('combustion', 'a reaction in which a substance burns in oxygen, releasing energy as heat and light'),
           ('oxidation', 'a reaction in which a substance gains oxygen'),
           ('thermal decomposition', 'the breaking down of a compound into simpler substances by heating'),
           ('fuel', 'a substance that releases energy when it burns'),
           ('fire triangle', 'the three things needed for burning: fuel, oxygen and heat'),
           ('incomplete combustion', 'burning with too little oxygen, producing carbon monoxide or soot')],
    facts=[('What are the products of complete combustion of a hydrocarbon fuel?', 'Carbon dioxide and water', ['Carbon monoxide and hydrogen', 'Oxygen and water', 'Carbon and oxygen'], 'Plenty of oxygen.'),
           ('Which gas is produced by the thermal decomposition of calcium carbonate?', 'Carbon dioxide', ['Oxygen', 'Hydrogen', 'Nitrogen'], 'Calcium oxide is also formed.'),
           ('Which test shows that a gas is carbon dioxide?', 'It turns limewater milky', ['It relights a glowing splint', 'It makes a squeaky pop', 'It bleaches litmus'], 'Calcium carbonate forms.'),
           ('Why is carbon monoxide dangerous?', 'It binds to haemoglobin so blood carries less oxygen', ['It is a strong acid', 'It smells very bad', 'It causes acid rain only'], 'Colourless, odourless and toxic.'),
           ('Rusting is an example of…', 'oxidation', ['decomposition', 'neutralisation', 'combustion'], 'Iron gains oxygen (with water present).')],
    why=[('Explain how a fire blanket puts out a chip-pan fire.', 'It cuts off the oxygen supply, removing one side of the fire triangle.'),
         ('Explain why gas boilers need to be serviced regularly.', 'A faulty boiler may have too little oxygen, causing incomplete combustion that produces toxic carbon monoxide.'),
         ('Explain why water should not be used on an oil or electrical fire.', 'Water sinks below burning oil and boils violently, spreading the fire; water conducts electricity and can cause electrocution.')],
    contrast=[('complete combustion', 'incomplete combustion', 'Complete combustion has plenty of oxygen and produces CO₂ and water with a blue flame; incomplete combustion has limited oxygen and produces carbon monoxide and soot with a yellow, smoky flame.'),
              ('thermal decomposition', 'combustion', 'Thermal decomposition breaks one compound into simpler substances using heat, without needing oxygen; combustion is a reaction of a fuel with oxygen that releases energy.')],
    misc=[('When something burns it is destroyed and loses mass.', 'Burning combines the fuel with oxygen; atoms are conserved, and the products (often gases) have the same total mass as the reactants.'),
          ('Oxygen is a fuel.', 'Oxygen is needed for burning, but it is not a fuel; the fuel is the substance that reacts with oxygen and releases energy.')],
    cases=[('Carbon monoxide alarms', 'After many deaths from faulty heaters, many countries now require CO alarms in homes with fuel-burning appliances.', 'dangers of incomplete combustion', 'Cheap detectors save lives because CO cannot be seen or smelled.')],
    evaluate=[('Homes should stop using gas for cooking and heating.', ['burning gas releases CO₂ (climate change) and indoor pollutants', 'risk of CO poisoning and explosions'], ['electric alternatives can be more expensive to install', 'electricity may also come from fossil fuels'], 'Moving away from gas reduces emissions and indoor pollution, especially with renewable electricity, but needs support with costs.')],
    extended=[('Describe how you could show that the products of burning a candle include water and carbon dioxide, and explain what happens if the air supply is reduced.', 'Draw combustion products from a burning candle through a cooled U-tube (water condenses – test with blue cobalt chloride paper turning pink or anhydrous copper sulfate turning blue), then through limewater (turns milky – CO₂). With less air: incomplete combustion – yellow sooty flame, carbon (soot) and toxic carbon monoxide form, less energy released.', 6)],
))


@R.add('ch08-st3', 'C3', (1, 4), 'numerical')
def decomposition_mass(rng, slot):
    m = rng.choice([5.0, 10.0, 20.0, 2.5])
    return dict(stem=f'When {m:g} g of calcium carbonate is heated strongly, {g(m * 0.56)} g of calcium oxide is left. Calculate the mass of carbon dioxide given off and write the word equation.', answer=f'{g(m * 0.44)} g; calcium carbonate → calcium oxide + carbon dioxide',
                markingKey=f'M1 {m:g} − {g(m * 0.56)}; A1 {g(m * 0.44)} g; B1 word equation.', marks=3)


inquiry('ch08-st3',
        dict(ctx='how the type of metal carbonate affects how quickly it thermally decomposes',
             iv='metal carbonate (copper, zinc, magnesium, calcium carbonate)', dv='time for the limewater to turn milky',
             cvs=[('mass of carbonate (1 g)', 'more carbonate gives more gas'), ('volume of limewater (5 cm³)', 'more limewater takes longer to go cloudy'), ('Bunsen flame (blue, same height)', 'heat input affects rate'), ('the same tubes and delivery tube', 'gas must travel the same path')],
             hyp='If copper carbonate is heated, then the limewater will go milky fastest, because carbonates of less reactive metals decompose more easily.',
             method='Put 1 g of carbonate in a boiling tube connected by a delivery tube to 5 cm³ of limewater; heat with a blue flame at a fixed height; start a stopwatch; stop when limewater is milky; remove the delivery tube from the limewater before stopping heating; repeat for each carbonate three times.',
             weak=('the limewater sucked back into the hot tube', 'lift the delivery tube out of the limewater before removing the flame'),
             safety='suck-back can crack hot glass – remove the delivery tube first; wear eye protection'))
dataset('ch08-st3',
        dict(intro='{who} burned different volumes of ethanol in a spirit burner under a can of water and recorded the temperature rise.', iv=('Volume of ethanol burned', 'cm³'), xs=[1, 2, 3, 4, 5],
             dv=('Temperature rise', '°C'), f=lambda x: 9 * x, dp=1, trend='The temperature rise increases in proportion to the volume of ethanol burned.',
             why='Combustion of ethanol releases energy; burning more fuel releases more energy, which heats the water more.'))

R.facts('ch08-st4', F(
    terms=[('exothermic reaction', 'a reaction that transfers energy to the surroundings, so the temperature rises'),
           ('endothermic reaction', 'a reaction that takes in energy from the surroundings, so the temperature falls'),
           ('energy level diagram', 'a diagram showing the energy of reactants and products'),
           ('activation energy', 'the minimum energy needed for a reaction to start'),
           ('hand warmer', 'a device using an exothermic reaction (often iron oxidation) to release heat')],
    facts=[('Which is an exothermic reaction?', 'Combustion', ['Thermal decomposition', 'Photosynthesis', 'Dissolving ammonium nitrate'], 'Fuels release heat.'),
           ('A reaction makes the test tube feel cold. What type of reaction is it?', 'Endothermic', ['Exothermic', 'Combustion', 'Neutral'], 'Energy is taken from the surroundings.'),
           ('Which product uses an endothermic process?', 'An instant cold pack', ['A self-heating can', 'A hand warmer', 'A firework'], 'Ammonium nitrate dissolving.'),
           ('In an energy level diagram for an exothermic reaction, where are the products?', 'Below the reactants', ['Above the reactants', 'At the same level', 'There are no products'], 'Energy has been released.')],
    why=[('Explain why neutralisation of an acid by an alkali is described as exothermic.', 'Energy is released to the surroundings, so the temperature of the solution rises.'),
         ('Explain why photosynthesis is an endothermic reaction.', 'It takes in energy from light to make glucose, which stores more chemical energy than CO₂ and water.'),
         ('Explain why a match needs to be struck before it burns even though combustion is exothermic.', 'Energy is needed to start the reaction (activation energy); once started, the energy released keeps it going.')],
    contrast=[('an exothermic change such as burning', 'an endothermic change such as thermal decomposition', 'An exothermic reaction gives out energy and the temperature rises (e.g. burning); an endothermic reaction takes in energy and the temperature falls (e.g. thermal decomposition).')],
    misc=[('Endothermic reactions make things colder because they produce cold.', 'They take in thermal energy from the surroundings; “cold” is not a substance.'),
          ('All reactions that need heating are endothermic.', 'Many exothermic reactions (e.g. burning) need heat to start; the overall energy change decides the type.')],
    cases=[('Self-heating cans', 'Some cans of coffee have a separate chamber of calcium oxide and water; pressing a button mixes them, an exothermic reaction heats the drink.', 'using exothermic reactions', 'Useful for campers and emergencies, though the cans are bulky and costly.')],
    evaluate=[('Reusable hand warmers are better than single-use ones.', ['less waste', 'cheaper over time'], ['must be reset by boiling, needing energy', 'single-use types last longer (hours)'], 'Reusable warmers are better for the environment for regular use, though single-use ones suit long trips.')],
    extended=[('Plan an investigation to find whether dissolving different salts is exothermic or endothermic, and explain how you would show the results.', 'Measure 25 cm³ water in a polystyrene cup (insulation); record start temperature; add 5 g salt, stir; record lowest or highest temperature; calculate change; repeat three times per salt; keep volume, mass, starting temperature the same; rise → exothermic, fall → endothermic; display as a bar chart of temperature change.', 6)],
))


@R.add('ch08-st4', 'C3', (1, 4), 'numerical')
def temp_change(rng, slot):
    a = rng.choice([18.5, 19.0, 20.0, 21.5, 22.0])
    d = rng.choice([-6.5, -4.0, -3.0, 5.5, 8.0, 12.5])
    b = a + d
    typ = 'exothermic' if d > 0 else 'endothermic'
    return dict(stem=f'The temperature of a solution changed from {a:.1f} °C to {b:.1f} °C during a reaction. Calculate the temperature change and state whether the reaction is exothermic or endothermic.', answer=f'{d:+.1f} °C; {typ}',
                markingKey=f'M1 {b:.1f} − {a:.1f}; A1 {d:+.1f} °C; B1 {typ} – {"energy released to surroundings" if d > 0 else "energy taken in from surroundings"}.', marks=3)


inquiry('ch08-st4',
        dict(ctx='how the mass of ammonium nitrate dissolved affects the temperature drop of the water',
             iv='mass of ammonium nitrate (1, 2, 3, 4, 5 g)', dv='temperature drop measured with a thermometer',
             cvs=[('volume of water (25 cm³)', 'larger volume cools less'), ('starting temperature', 'affects heat gained from surroundings'), ('stirring', 'ensures it dissolves fully'), ('polystyrene cup', 'insulation reduces heat transfer')],
             hyp='If more ammonium nitrate is dissolved, then the temperature drop will be larger, because more energy is taken in from the water.',
             method='Put 25 cm³ water in a polystyrene cup inside a beaker; record the temperature; add 1 g ammonium nitrate and stir; record the lowest temperature; repeat with 2–5 g; repeat three times; plot temperature drop against mass.',
             weak=('a glass beaker was used, which let heat in from the room', 'use an insulated polystyrene cup with a lid'),
             safety='ammonium nitrate is an oxidiser – keep away from flames; wear eye protection'))
dataset('ch08-st4',
        dict(intro='{who} added different masses of calcium oxide to 50 cm³ of water in a polystyrene cup and recorded the temperature rise.', iv=('Mass of calcium oxide', 'g'), xs=[1, 2, 3, 4, 5],
             dv=('Temperature rise', '°C'), f=lambda x: 5.5 * x, dp=1, trend='The temperature rise increases in proportion to the mass of calcium oxide added.',
             why='The reaction of calcium oxide with water is exothermic; more calcium oxide reacting releases more energy.'))

R.facts('ch08-st5', F(
    terms=[('reactivity series', 'a list of metals in order of how vigorously they react'),
           ('metal oxide', 'the compound formed when a metal reacts with oxygen'),
           ('metal hydroxide', 'the alkaline compound formed when a reactive metal reacts with water, with hydrogen'),
           ('displacement reaction', 'a reaction in which a more reactive metal takes the place of a less reactive metal in a compound'),
           ('hydrogen test', 'a lit splint gives a squeaky pop in hydrogen')],
    facts=[('What are the products when magnesium reacts with hydrochloric acid?', 'Magnesium chloride and hydrogen', ['Magnesium oxide and water', 'Magnesium chloride and water', 'Magnesium and chlorine'], 'Metal + acid → salt + hydrogen.'),
           ('Which metal reacts most vigorously with cold water?', 'Potassium', ['Copper', 'Iron', 'Zinc'], 'Group 1 metals are very reactive.'),
           ('Which metal does not react with dilute hydrochloric acid?', 'Copper', ['Magnesium', 'Zinc', 'Iron'], 'It is below hydrogen.'),
           ('What forms when sodium reacts with water?', 'Sodium hydroxide and hydrogen', ['Sodium oxide and oxygen', 'Sodium chloride and water', 'Sodium and hydrogen'], 'The solution is alkaline.'),
           ('Why is gold found as the pure metal in nature?', 'It is very unreactive', ['It is very reactive', 'It is magnetic', 'It is soluble in water'], 'It does not react with oxygen or water.')],
    why=[('Explain why potassium is stored under oil.', 'It reacts rapidly with oxygen and water vapour in the air; oil keeps air and water away.'),
         ('Explain why iron nails rust faster near the sea.', 'Salt water speeds up the oxidation of iron by oxygen and water.'),
         ('Explain why aluminium is used for window frames even though it is fairly reactive.', 'A thin, tough layer of aluminium oxide forms on the surface and protects the metal from further corrosion.')],
    contrast=[('the reaction of magnesium with water', 'its reaction with acid', 'Magnesium reacts very slowly with cold water, giving a few bubbles; it reacts vigorously with acid, fizzing quickly and getting hot.'),
              ('a reactive metal', 'an unreactive metal', 'A reactive metal (e.g. potassium) reacts quickly with water, oxygen and acids; an unreactive metal (e.g. gold) barely reacts and is found native.')],
    misc=[('All metals react with acids to make hydrogen.', 'Metals below hydrogen in the reactivity series, such as copper, silver and gold, do not react with dilute acids.'),
          ('Rusting only needs water.', 'Rusting needs both water and oxygen.')],
    cases=[('Galvanised steel and sacrificial protection', 'Steel is coated with zinc; because zinc is more reactive, it corrodes instead of the iron even if the coating is scratched.', 'using reactivity to prevent corrosion', 'Used for car bodies, lamp posts and ships’ hulls (with zinc or magnesium blocks).')],
    evaluate=[('Coating steel with zinc is the best way to prevent bridges from rusting.', ['protects even when scratched (sacrificial)', 'long-lasting'], ['costly for large structures', 'paint or stainless steel may be cheaper or more suitable', 'zinc slowly wears away'], 'Galvanising is excellent for many steel parts but engineers compare costs and conditions to choose the best protection.')],
    extended=[('Describe how to use reactions with dilute hydrochloric acid to put four metals (copper, iron, magnesium, zinc) in order of reactivity, including how to make it a fair test and what you expect to see.', 'Same volume and concentration of acid in test tubes; same mass/size and surface area of each metal; same temperature; observe bubbles and measure temperature rise or gas volume in a fixed time. Expect magnesium fastest (vigorous fizz, hot), then zinc, then iron (slow bubbles), copper no reaction. Test gas with lit splint – squeaky pop.', 6)],
))


@R.add('ch08-st5', 'C2', (1, 3), 'mcq')
def displace(rng, slot):
    order = ['potassium', 'sodium', 'calcium', 'magnesium', 'aluminium', 'zinc', 'iron', 'copper', 'silver']
    salts = {'zinc': 'zinc sulfate', 'iron': 'iron sulfate', 'copper': 'copper sulfate', 'silver': 'silver nitrate', 'magnesium': 'magnesium sulfate'}
    s = rng.choice(list(salts))
    m = rng.choice(['magnesium', 'zinc', 'iron', 'copper', 'silver'])
    while m == s:
        m = rng.choice(['magnesium', 'zinc', 'iron', 'copper', 'silver'])
    yes = order.index(m) < order.index(s)
    corr = f'Yes – {m} is more reactive than {s}, so it displaces {s}' if yes else f'No – {m} is less reactive than {s}'
    wr = [f'No – {m} is less reactive than {s}', f'Yes – {m} is more reactive than {s}, so it displaces {s}', 'Yes – all metals displace each other', 'No – metals never react with salt solutions']
    return mcq(rng, f'A piece of {m} is placed in {salts[s]} solution. Will a displacement reaction happen?', corr, [w for w in wr if w != corr][:3], f'B1 {corr}')


inquiry('ch08-st5',
        dict(ctx='how the reactivity of a metal affects the temperature rise when it reacts with hydrochloric acid',
             iv='metal (magnesium, zinc, iron, copper)', dv='temperature rise of the acid in 2 minutes',
             cvs=[('mass of metal (0.5 g powder)', 'more metal releases more energy'), ('volume and concentration of acid', 'both affect the amount reacting'), ('starting temperature', 'affects rate'), ('insulated cup', 'reduces heat loss')],
             hyp='If the metal is more reactive, then the temperature rise will be larger, because it reacts faster and releases energy more quickly.',
             method='Put 20 cm³ of 1 mol/dm³ hydrochloric acid in a polystyrene cup; record temperature; add 0.5 g metal powder and stir; record the highest temperature within 2 minutes; repeat three times for each metal; rank the metals.',
             weak=('metal ribbon was used for magnesium but lumps for iron', 'use powder of all metals so that surface area is similar'),
             safety='hydrogen is flammable – no flames nearby; wear eye protection; acid is an irritant'))
dataset('ch08-st5',
        dict(intro='{who} measured the volume of hydrogen produced in 1 minute when 0.1 g of magnesium ribbon reacted with hydrochloric acid of different concentrations.', iv=('Acid concentration', 'mol/dm³'), xs=[0.25, 0.5, 0.75, 1.0, 1.25],
             dv=('Volume of hydrogen', 'cm³'), f=lambda x: 40 * x, dp=0, trend='The volume of hydrogen produced in 1 minute increases as acid concentration increases.',
             why='More concentrated acid has more acid particles in the same volume, so they collide with the magnesium more often and the reaction is faster.'))


# =============================================================================================
# ch09 Acids, Alkalis and Indicators
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('acid', 'a substance with a pH less than 7 that turns blue litmus red'),
           ('alkali', 'a base that dissolves in water, giving a solution with pH greater than 7'),
           ('base', 'a substance that neutralises an acid, such as a metal oxide or hydroxide'),
           ('corrosive', 'a hazard meaning the substance can destroy living tissue and attack metals'),
           ('irritant', 'a hazard meaning the substance can cause inflammation or reddening of the skin or eyes'),
           ('hazard symbol', 'a pictogram warning of the danger of a substance')],
    facts=[('Which of these is an everyday acid?', 'Vinegar (ethanoic acid)', ['Toothpaste', 'Bleach', 'Soap'], 'Lemon juice and cola are also acidic.'),
           ('Which of these is an everyday alkali?', 'Oven cleaner (sodium hydroxide)', ['Lemon juice', 'Vinegar', 'Cola'], 'Strong alkalis are corrosive.'),
           ('What should you do if acid is splashed on the skin?', 'Wash with plenty of running water', ['Wipe with a dry cloth', 'Add alkali to it', 'Cover it with a plaster'], 'Dilute and remove it.'),
           ('Which acid is found in your stomach?', 'Hydrochloric acid', ['Sulfuric acid', 'Citric acid', 'Nitric acid'], 'It kills bacteria and helps pepsin work.'),
           ('What does the corrosive hazard symbol show?', 'Liquid dripping onto a hand and a surface, damaging them', ['A flame', 'A skull and crossbones', 'An exclamation mark'], 'It destroys tissue.')],
    why=[('Explain why concentrated acids are more dangerous than dilute acids.', 'They contain more acid particles in the same volume, so they react more vigorously with skin and materials.'),
         ('Explain why you should never taste substances in the laboratory to see if they are acidic.', 'Many are toxic or corrosive; indicators give a safe way to test.'),
         ('Explain why lemon juice and vinegar are safe to eat even though they are acids.', 'They are weak and dilute acids, so they do not damage tissues in small amounts.')],
    contrast=[('an acid', 'an alkali', 'An acid has pH below 7 and turns blue litmus red; an alkali has pH above 7, turns red litmus blue and is a soluble base.'),
              ('a base', 'an alkali', 'A base is any substance that neutralises an acid; an alkali is a base that dissolves in water.')],
    misc=[('All acids are dangerous and burn skin.', 'Many acids are weak and safe in food (citric acid, ethanoic acid); only strong, concentrated acids are corrosive.'),
          ('Alkalis are safe because they are the opposite of acids.', 'Strong alkalis such as sodium hydroxide are corrosive and can damage skin and eyes even more than many acids.')],
    evaluate=[('Household cleaning products containing strong alkalis should only be sold with child-proof caps.', ['prevent accidental poisoning and burns in children', 'cheap to do'], ['some adults find them hard to open', 'education and safe storage also needed'], 'Child-proof caps are justified for corrosive products, along with clear labelling and safe storage.')],
    extended=[('A bottle in the prep room has lost its label. Describe how you would safely find out if it is acidic, neutral or alkaline, and what safety precautions you would take.', 'Wear eye protection and gloves; treat it as hazardous; use a dropper to put one drop on universal indicator paper on a white tile or add a few drops of universal indicator to a small sample; compare colour with chart: red/orange/yellow acidic, green neutral, blue/purple alkaline; never smell directly or taste; wash spills with water; label once identified.', 5)],
))
inquiry('ch09-st1',
        dict(ctx='how the concentration of an everyday acid (vinegar) affects the time to dissolve an eggshell piece',
             iv='concentration of vinegar (25%, 50%, 75%, 100% diluted with water)', dv='time for a 1 cm² eggshell piece to stop fizzing',
             cvs=[('size of eggshell piece', 'surface area affects rate'), ('volume of vinegar (20 cm³)', 'more acid reacts longer'), ('temperature', 'affects reaction rate'), ('same brand of vinegar', 'acid content varies')],
             hyp='If the vinegar is more concentrated, then the eggshell will dissolve faster, because there are more acid particles to react with the calcium carbonate.',
             method='Make the dilutions with a measuring cylinder; pour 20 cm³ of each into a beaker; add one 1 cm² piece of eggshell; time until fizzing stops; repeat three times; compare means.',
             weak=('eggshell pieces had different amounts of membrane attached', 'remove the inner membrane and cut pieces with a template'),
             safety='vinegar stings eyes – wear eye protection; wash hands after handling eggshell (Salmonella)'))
dataset('ch09-st1',
        dict(intro='{who} measured the pH of a lemon juice sample diluted with different volumes of water (three readings with a pH meter).', iv=('Volume of water added', 'cm³'), xs=[0, 10, 50, 100, 500],
             dv=('pH', ''), f=lambda x: 2.2 + 0.5 * math.log10(1 + x / 2), dp=1, trend='The pH increases slowly as more water is added, but stays below 7.',
             why='Dilution lowers the concentration of acid particles, so the solution becomes less acidic, but it never becomes neutral or alkaline just by adding water.'))

R.facts('ch09-st2', F(
    terms=[('indicator', 'a substance that changes colour depending on whether a solution is acidic, neutral or alkaline'),
           ('litmus', 'an indicator that is red in acid and blue in alkali'),
           ('universal indicator', 'a mixture of indicators that shows a range of colours for pH 0–14'),
           ('pH scale', 'a scale from 0 to 14 that measures how acidic or alkaline a solution is'),
           ('neutral', 'pH 7, neither acidic nor alkaline'),
           ('pH meter', 'an electronic instrument that measures pH accurately')],
    facts=[('What colour is universal indicator in a neutral solution?', 'Green', ['Red', 'Purple', 'Yellow'], 'pH 7.'),
           ('A solution has pH 1. How would you describe it?', 'Strongly acidic', ['Weakly acidic', 'Neutral', 'Strongly alkaline'], 'The lower the pH, the more acidic.'),
           ('What colour does universal indicator turn in a strong alkali?', 'Purple', ['Red', 'Green', 'Orange'], 'pH 13–14.'),
           ('What colour does phenolphthalein turn in an alkali?', 'Pink', ['Colourless', 'Red', 'Blue'], 'It is colourless in acid.'),
           ('Why is a pH meter better than universal indicator for accurate measurements?', 'It gives a precise numerical value, not a judgement of colour', ['It changes colour faster', 'It works only in acids', 'It needs no calibration'], 'Colour judgement varies between people.')],
    why=[('Explain why red cabbage juice can be used as an indicator.', 'It contains pigments that change colour depending on pH – red in acid, purple in neutral and green/yellow in alkali.'),
         ('Explain why litmus cannot tell you how strong an acid is.', 'It only has two colours (red in acid, blue in alkali); it shows whether a solution is acidic but not the pH value.'),
         ('Explain why farmers test the pH of soil.', 'Crops grow best in particular pH ranges; if the soil is too acidic, nutrients are less available and farmers can add lime to raise pH.')],
    contrast=[('litmus', 'universal indicator', 'Litmus shows only acid (red) or alkali (blue); universal indicator shows a range of colours that give an approximate pH.'),
              ('a strong acid', 'a concentrated acid', 'A strong acid has a very low pH because it releases many H⁺ ions; a concentrated acid has a lot of acid dissolved in a small volume of water.')],
    misc=[('pH 6 is more acidic than pH 2.', 'Lower pH means more acidic; pH 2 is much more acidic than pH 6.'),
          ('The pH scale only goes from 1 to 10.', 'The usual pH scale runs from 0 to 14.')],
    cases=[('Hydrangea flowers', 'Hydrangea flowers are blue in acidic soil and pink in alkaline soil because the availability of aluminium ions changes with pH.', 'natural indicators', 'Gardeners can change flower colour by changing soil pH.')],
    evaluate=[('Universal indicator is good enough for all pH measurements in school.', ['cheap, quick, shows approximate pH'], ['colour judgement is subjective', 'cannot be used with coloured solutions', 'only to nearest whole number'], 'Universal indicator is fine for approximate pH; pH meters are needed for accurate work.')],
    extended=[('Describe how to make an indicator from red cabbage and test whether it can distinguish between acids and alkalis. Include a fair-test plan.', 'Chop red cabbage, boil or soak in hot water, filter to obtain purple juice. Add the same volume (5 drops) to 2 cm³ of solutions of known pH (e.g. pH 1, 4, 7, 10, 13) on a spotting tile; record colours to make a colour chart; then test unknown solutions and compare. Control volume of indicator and sample; use a white background; compare with universal indicator or pH meter.', 6)],
))


@R.add('ch09-st2', 'C1', (1, 3), 'mcq')
def ph_colour(rng, slot):
    ph = rng.choice([1, 2, 4, 6, 7, 8, 10, 13])
    col = {1: 'red', 2: 'red', 4: 'orange', 6: 'yellow', 7: 'green', 8: 'blue-green', 10: 'blue', 13: 'purple'}[ph]
    desc = 'strongly acidic' if ph <= 2 else 'weakly acidic' if ph < 7 else 'neutral' if ph == 7 else 'weakly alkaline' if ph <= 10 else 'strongly alkaline'
    return mcq(rng, f'A solution has pH {ph}. What colour will universal indicator turn, and how is the solution described?', f'{col}; {desc}',
               rng.sample([f'{c}; {d}' for c, d in [('red', 'strongly acidic'), ('green', 'neutral'), ('purple', 'strongly alkaline'), ('orange', 'weakly acidic'), ('blue', 'weakly alkaline')] if d != desc], 3), f'B1 {col}, {desc}')


inquiry('ch09-st2',
        dict(ctx='how the pH of a solution affects the colour of a homemade beetroot indicator',
             iv='pH of buffer solutions (2, 4, 6, 7, 8, 10, 12)', dv='colour of the indicator recorded against a colour chart (or absorbance with a colorimeter)',
             cvs=[('volume of indicator added (5 drops)', 'more indicator gives deeper colour'), ('volume of buffer (2 cm³)', 'affects concentration'), ('white background and lighting', 'affects how colour is seen'), ('the same batch of indicator', 'batches differ in strength')],
             hyp='If the pH increases, then the beetroot indicator will change from red to purple to yellow, because its pigments change structure in different pH conditions.',
             method='Prepare beetroot juice by boiling and filtering; put 2 cm³ of each buffer in wells of a white spotting tile; add 5 drops of indicator; record the colour; repeat three times; compare with universal indicator colours.',
             weak=('the colours were judged under a yellow lamp', 'use daylight or a white LED and a white background; or use a colorimeter'),
             safety='buffers at pH 2 and 12 are irritants – wear eye protection; hot liquid when boiling beetroot'))
dataset('ch09-st2',
        dict(intro='{who} measured the pH of soil samples taken at different distances from a limestone footpath (three samples at each distance).', iv=('Distance from path', 'm'), xs=[1, 5, 10, 20, 40],
             dv=('Soil pH', ''), f=lambda x: 7.8 - 0.08 * x if x < 20 else 6.2 - 0.02 * (x - 20), dp=1, trend='The soil pH decreases (becomes more acidic) with distance from the limestone path.',
             why='Limestone (calcium carbonate) dust from the path neutralises soil acids nearby, so the soil is less acidic close to the path.'))

R.facts('ch09-st3', F(
    terms=[('neutralisation', 'the reaction between an acid and a base that produces a salt and water'),
           ('salt', 'a compound formed when the hydrogen in an acid is replaced by a metal'),
           ('sulfate', 'a salt made from sulfuric acid'),
           ('chloride', 'a salt made from hydrochloric acid'),
           ('nitrate', 'a salt made from nitric acid'),
           ('titration', 'a method of adding one solution to another to find the exact volume needed for neutralisation')],
    facts=[('What is produced when an acid reacts with an alkali?', 'A salt and water', ['A salt and hydrogen', 'Carbon dioxide and water', 'An oxide only'], 'Neutralisation.'),
           ('Which salt forms when hydrochloric acid reacts with sodium hydroxide?', 'Sodium chloride', ['Sodium sulfate', 'Sodium nitrate', 'Sodium hydroxide'], 'Chloride from hydrochloric acid.'),
           ('What are the products when an acid reacts with a metal carbonate?', 'A salt, water and carbon dioxide', ['A salt and hydrogen', 'A salt only', 'Water and oxygen'], 'The gas turns limewater milky.'),
           ('What pH is a solution when an acid has been exactly neutralised by an alkali?', '7', ['1', '14', '10'], 'Neutral.'),
           ('Which salt forms when sulfuric acid reacts with copper oxide?', 'Copper sulfate', ['Copper chloride', 'Copper nitrate', 'Copper carbonate'], 'Blue solution.')],
    why=[('Explain why excess copper oxide is added to sulfuric acid when making copper sulfate crystals.', 'Excess ensures all the acid is used up; the unreacted solid is then removed by filtration, so the solution contains only the salt.'),
         ('Explain why the temperature rises during neutralisation.', 'Neutralisation is exothermic – energy is released when H⁺ and OH⁻ ions combine to form water.'),
         ('Explain why indicator is used in a titration.', 'Acid and alkali solutions are both colourless, so the indicator shows the exact point when the acid is neutralised.')],
    contrast=[('reacting an acid with an alkali', 'reacting an acid with a carbonate', 'Acid + alkali gives a salt and water only; acid + carbonate gives a salt, water and carbon dioxide (fizzing).'),
              ('a chloride', 'a sulfate', 'A chloride is a salt made from hydrochloric acid (e.g. NaCl); a sulfate is a salt made from sulfuric acid (e.g. CuSO₄).')],
    misc=[('“Salt” always means sodium chloride.', 'In chemistry a salt is any compound formed from an acid by replacing its hydrogen with a metal, e.g. copper sulfate, potassium nitrate.'),
          ('Neutralisation always gives a solution with pH 7.', 'Only if exactly the right amounts react; excess acid or alkali leaves the pH below or above 7.')],
    cases=[('Antacid tablets', 'Tablets containing magnesium hydroxide or calcium carbonate neutralise excess stomach acid that causes indigestion and heartburn.', 'neutralisation in medicine', 'A simple reaction relieves a common problem; overuse can affect the body’s mineral balance.')],
    evaluate=[('Antacids are a good long-term treatment for heartburn.', ['quick relief by neutralising acid', 'cheap and available'], ['treat symptoms, not causes (diet, weight, smoking)', 'long-term use may mask serious conditions'], 'Antacids are fine for occasional heartburn, but frequent symptoms need medical advice and lifestyle changes.')],
    extended=[('Describe how to prepare pure, dry crystals of copper chloride from copper oxide and an acid. Name the acid and write the word equation.', 'Warm dilute hydrochloric acid; add copper oxide a spatula at a time with stirring until some remains unreacted (excess); filter to remove unreacted copper oxide; heat filtrate gently to evaporate some water until crystals start to form; leave to cool and crystallise; filter and dry crystals between filter paper. copper oxide + hydrochloric acid → copper chloride + water.', 6)],
))


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def neutral_vol(rng, slot):
    v1 = rng.choice([10.0, 20.0, 25.0])
    c1 = rng.choice([0.1, 0.2, 0.5, 1.0])
    c2 = rng.choice([0.1, 0.2, 0.25, 0.5])
    v2 = v1 * c1 / c2
    k = rng.choice(['ratio', 'mean'] if slot.d >= 2 else ['mean'])
    if k == 'mean':
        t = [round(v2 + rng.choice([-0.1, 0.0, 0.05, 0.1]), 2) for _ in range(3)]
        return dict(stem=f'In a titration, the volumes of acid needed to neutralise 25.0 cm³ of alkali were {t[0]:.2f}, {t[1]:.2f} and {t[2]:.2f} cm³. Calculate the mean volume.', answer=f'{sum(t) / 3:.2f} cm³',
                    markingKey=f'M1 ({t[0]:.2f} + {t[1]:.2f} + {t[2]:.2f}) ÷ 3; A1 {sum(t) / 3:.2f} cm³.', marks=2)
    return dict(stem=f'{v1:g} cm³ of sodium hydroxide of concentration {c1:g} mol/dm³ is neutralised by hydrochloric acid of concentration {c2:g} mol/dm³. The acid and alkali react 1 : 1. What volume of acid is needed?', answer=f'{g(v2)} cm³',
                markingKey=f'M1 equal amounts react: {v1:g} × {c1:g} = V × {c2:g}; M1 V = {v1:g} × {c1:g} ÷ {c2:g}; A1 {g(v2)} cm³.', marks=3)


inquiry('ch09-st3',
        dict(ctx='how the volume of sodium hydroxide added affects the temperature of hydrochloric acid during neutralisation',
             iv='volume of sodium hydroxide added (0 to 40 cm³ in 5 cm³ portions)', dv='temperature of the mixture after each addition',
             cvs=[('volume and concentration of acid (25 cm³)', 'more acid reacts with more alkali'), ('concentration of alkali', 'affects the volume needed'), ('insulated polystyrene cup with lid', 'reduces heat loss'), ('stirring after each addition', 'mixes evenly')],
             hyp='If more alkali is added, then the temperature will rise until the acid is neutralised and then fall, because neutralisation is exothermic and extra alkali only cools the mixture.',
             method='Put 25 cm³ of acid in a polystyrene cup with a lid; record temperature; add sodium hydroxide 5 cm³ at a time from a burette, stirring; record the temperature after each addition; continue to 40 cm³; repeat; plot temperature against volume and find the maximum.',
             weak=('the temperature was read before mixing was complete', 'stir and wait for a steady reading (or use a data logger)'),
             safety='sodium hydroxide is corrosive – wear eye protection and gloves'))
dataset('ch09-st3',
        dict(intro='{who} measured the volume of 0.1 mol/dm³ hydrochloric acid needed to neutralise 25 cm³ of different antacid solutions (three titrations each).', iv=('Mass of antacid dissolved', 'g'), xs=[0.1, 0.2, 0.3, 0.4, 0.5],
             dv=('Volume of acid', 'cm³'), f=lambda x: 42 * x, dp=1, trend='The volume of acid needed increases in proportion to the mass of antacid.',
             why='More antacid means more base particles, so more acid is needed to neutralise it completely.'))

R.facts('ch09-st4', F(
    terms=[('acid rain', 'rain with a pH below about 5.6, caused by sulfur dioxide and nitrogen oxides dissolving in water in the air'),
           ('sulfur dioxide', 'a gas produced when fuels containing sulfur burn; it forms sulfuric acid in rain'),
           ('nitrogen oxides', 'gases formed in hot engines when nitrogen and oxygen react; they form nitric acid in rain'),
           ('liming', 'adding powdered limestone or lime to lakes or soils to neutralise acidity'),
           ('flue gas desulfurisation', 'removing sulfur dioxide from power station waste gases using a base such as calcium carbonate')],
    facts=[('Which gas from burning coal is a major cause of acid rain?', 'Sulfur dioxide', ['Carbon dioxide', 'Methane', 'Oxygen'], 'It forms sulfuric acid.'),
           ('Why do farmers spread lime on fields?', 'To neutralise acidic soil', ['To kill weeds', 'To add nitrogen', 'To make the soil acidic'], 'Crops grow poorly in acid soil.'),
           ('What effect does acid rain have on limestone buildings?', 'It reacts with the calcium carbonate and wears them away', ['It makes them stronger', 'It turns them green', 'No effect'], 'Carbon dioxide is released.'),
           ('Which treatment for a bee sting (acidic) is suitable?', 'A weak alkali such as bicarbonate of soda', ['Vinegar', 'Lemon juice', 'Strong sodium hydroxide'], 'Neutralises the acid.'),
           ('Where do nitrogen oxides in the air mainly come from?', 'Car engines and power stations', ['Plants', 'Volcanoes only', 'The sea'], 'High temperatures in engines.')],
    why=[('Explain why acid rain can kill fish in lakes.', 'The lake becomes more acidic; low pH damages fish gills and eggs and releases toxic aluminium ions from soil into the water.'),
         ('Explain why catalytic converters reduce acid rain.', 'They convert nitrogen oxides from car exhausts into harmless nitrogen and oxygen before they leave the exhaust.'),
         ('Explain why toothpaste is slightly alkaline.', 'Bacteria in the mouth produce acids from sugar that dissolve tooth enamel; the alkaline toothpaste neutralises them.')],
    contrast=[('the causes of acid rain', 'the causes of global warming', 'Acid rain is caused mainly by sulfur dioxide and nitrogen oxides forming acids; global warming is caused by greenhouse gases such as carbon dioxide and methane trapping heat.')],
    misc=[('Normal rain is neutral (pH 7).', 'Normal rain is slightly acidic (about pH 5.6) because carbon dioxide dissolves in it; acid rain is more acidic than this.'),
          ('Acid rain only affects the area where the pollution is made.', 'Winds carry pollutants hundreds of kilometres, so acid rain often falls in other countries.')],
    cases=[('Acid rain in Scandinavia and the 1979 Geneva Convention', 'Lakes in Norway and Sweden lost fish populations because of acid rain from pollution produced in other countries; this led to an international agreement to cut sulfur emissions.', 'international action on pollution', 'Sulfur dioxide emissions in Europe fell by over 80% and many lakes have started to recover.')],
    evaluate=[('International agreements are the most effective way to tackle acid rain.', ['pollution crosses borders, so cooperation is needed', 'European SO₂ emissions fell sharply after agreements'], ['some countries may not sign or enforce them', 'technology (desulfurisation, catalytic converters) did the actual reduction'], 'Agreements were crucial in driving technology and cutting emissions, though they rely on enforcement.')],
    extended=[('Explain how acid rain forms, describe two of its effects, and evaluate two ways of reducing it.', 'Burning fossil fuels with sulfur produces SO₂; high-temperature engines produce NOx; these dissolve in water in clouds forming sulfuric and nitric acid. Effects: kills fish and trees, damages limestone buildings and metal structures. Reduce: flue gas desulfurisation (effective but costly), catalytic converters (reduce NOx from cars), low-sulfur fuels, renewable energy (removes the cause). Liming lakes treats symptoms only.', 6)],
))


@R.add('ch09-st4', 'C3', (1, 4), 'numerical')
def lime_needed(rng, slot):
    a = rng.choice([2, 4, 5, 8])
    per = rng.choice([2.0, 2.5, 3.0])
    return dict(stem=f'A farmer needs {per:g} tonnes of lime per hectare to raise the pH of a field from 5.5 to 6.5. The field is {a} hectares. How much lime is needed, and why does raising the pH help crops?', answer=f'{g(a * per)} tonnes; most crops grow best in near-neutral soil where nutrients are more available',
                markingKey=f'M1 {a} × {per:g}; A1 {g(a * per)} tonnes; B1 neutralises soil acid / nutrients more available.', marks=3)


inquiry('ch09-st4',
        dict(ctx='how the pH of simulated acid rain affects the germination of cress seeds',
             iv='pH of the watering solution (3, 4, 5, 6, 7)', dv='percentage of 50 seeds that germinate in 5 days',
             cvs=[('number of seeds (50)', 'percentage needs the same total'), ('volume of solution added daily (5 cm³)', 'water affects germination'), ('temperature and light', 'both affect germination'), ('type of cotton wool or paper', 'absorbency affects water available')],
             hyp='If the pH is lower, then fewer seeds will germinate, because acidic conditions damage enzymes and cell membranes in the seeds.',
             method='Prepare solutions of dilute sulfuric acid at pH 3–7 (check with a pH meter); put 50 cress seeds on cotton wool in labelled Petri dishes; add 5 cm³ of solution each day; keep dishes together in the same place; count germinated seeds after 5 days; repeat with three dishes per pH.',
             weak=('the pH of the solutions was not checked', 'measure each solution’s pH with a calibrated pH meter before use'),
             safety='dilute sulfuric acid is an irritant – wear eye protection and wash hands'))
dataset('ch09-st4',
        dict(intro='{who} placed equal-sized marble chips in sulfuric acid solutions of different pH for one week and measured the percentage mass lost.', iv=('pH of solution', ''), xs=[2, 3, 4, 5, 6],
             dv=('Mass lost', '%'), f=lambda x: 24 / x ** 1.5, dp=1, trend='The percentage mass lost decreases as the pH increases (solution less acidic).',
             why='Lower pH means a higher concentration of acid, which reacts with the calcium carbonate in marble faster, dissolving more of it.'))


# =============================================================================================
# ch10 Forces and Motion
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('force', 'a push or a pull, measured in newtons (N)'),
           ('newton (N)', 'the unit of force'),
           ('friction', 'a contact force that opposes motion between surfaces in contact'),
           ('air resistance', 'friction caused by air acting against an object moving through it'),
           ('upthrust', 'the upward force exerted by a liquid or gas on an object in it'),
           ('force diagram', 'a diagram with arrows showing the size and direction of the forces acting on an object'),
           ('non-contact force', 'a force that acts at a distance, such as gravity, magnetism or electrostatic force')],
    facts=[('Which instrument measures force?', 'A newton meter (forcemeter)', ['A thermometer', 'A balance in grams', 'A stopwatch'], 'It contains a calibrated spring.'),
           ('Which of these is a non-contact force?', 'Magnetic force', ['Friction', 'Air resistance', 'Tension'], 'It acts at a distance.'),
           ('Which force keeps a boat floating?', 'Upthrust', ['Friction', 'Weight', 'Tension'], 'It balances the boat’s weight.'),
           ('In a force diagram, what does the length of an arrow show?', 'The size of the force', ['The speed of the object', 'The mass of the object', 'The time the force acts'], 'Arrow direction shows force direction.'),
           ('Which force acts in a stretched rope?', 'Tension', ['Upthrust', 'Friction', 'Magnetism'], 'It pulls equally at both ends.')],
    why=[('Explain why the tread on car tyres is important in wet weather.', 'The grooves push water away so the tyre stays in contact with the road, keeping enough friction for grip and braking.'),
         ('Explain why streamlined shapes are used for racing cars and fish.', 'They reduce air or water resistance, so less force is needed to move fast.'),
         ('Explain why friction can be useful and also a problem.', 'Useful: it allows walking, gripping and braking; a problem: it wears parts and wastes energy as heat in machines.')],
    contrast=[('contact forces', 'non-contact forces', 'Contact forces act when objects touch (friction, tension, air resistance); non-contact forces act at a distance (gravity, magnetism, electrostatic).'),
              ('friction', 'air resistance', 'Friction acts between solid surfaces sliding or gripping; air resistance is a type of friction from air on an object moving through it.')],
    misc=[('A moving object must have a force pushing it forward.', 'An object can keep moving at constant speed with no resultant force; forces are needed only to change speed or direction.'),
          ('Gravity only acts on objects that are falling.', 'Gravity acts on all objects with mass all the time, including those resting on a table.')],
    cases=[('Formula 1 aerodynamics', 'F1 cars use wings that push the car down onto the track (downforce), increasing friction between tyres and road so the car can corner faster.', 'using forces in design', 'Engineers balance downforce against air resistance using wind tunnels and computer models.')],
    evaluate=[('Reducing friction is always a good thing.', ['saves energy in machines', 'reduces wear'], ['friction is needed for walking, brakes, gripping and tyres on roads'], 'Friction should be reduced where it wastes energy but kept where it is needed for safety and grip.')],
    extended=[('A skydiver jumps from a plane. Draw (describe) force diagrams for the moment she leaves the plane, when falling at constant speed, and just after the parachute opens, and explain her motion at each stage.', 'Leaving: weight large downwards, tiny air resistance – accelerates. Constant (terminal) speed: weight = air resistance (balanced arrows) – constant speed. Parachute opens: air resistance much larger than weight – decelerates until a new, lower terminal speed when forces balance again.', 6)],
))


@R.add('ch10-st1', 'C3', (1, 4), 'numerical')
def newton_meter(rng, slot):
    a = rng.choice([2.0, 2.5, 3.5, 4.0, 6.0])
    b = rng.choice([0.5, 1.0, 1.5])
    return dict(stem=f'A newton meter reads {a:.1f} N when a wooden block is pulled at a steady speed across a desk. When sandpaper is placed under the block, it reads {a + b:.1f} N. By how much did the friction force increase, and why?', answer=f'{b:.1f} N; the rougher surface increases friction',
                markingKey=f'M1 {a + b:.1f} − {a:.1f}; A1 {b:.1f} N; B1 at steady speed pull = friction; rougher surface → more friction.', marks=3)


inquiry('ch10-st1',
        dict(ctx='how the type of surface affects the friction force on a sliding block',
             iv='surface (wood, carpet, sandpaper, plastic, rubber mat)', dv='force on a newton meter needed to pull the block at a steady speed',
             cvs=[('mass of the block', 'heavier blocks have more friction'), ('the same block and side', 'surface of the block affects friction'), ('pulling horizontally at a steady speed', 'angle and acceleration change the reading'), ('the same newton meter', 'meters differ')],
             hyp='If the surface is rougher (e.g. sandpaper), then the friction force will be larger, because the surfaces grip and interlock more.',
             method='Attach a newton meter to a 500 g block; pull it horizontally across each surface at a slow steady speed; read the force while it is moving; repeat three times per surface; calculate means; draw a bar chart.',
             weak=('the block was jerked so the reading kept changing', 'pull with a slow steady motion (or use a motor/pulley) and read while moving steadily'),
             safety='keep masses on the bench to avoid dropping them on feet'))
dataset('ch10-st1',
        dict(intro='{who} added masses on top of a block and measured the force needed to pull it at a steady speed across a bench.', iv=('Total mass', 'g'), xs=[200, 400, 600, 800, 1000],
             dv=('Friction force', 'N'), f=lambda x: 0.004 * x, dp=2, trend='The friction force increases in proportion to the total mass of the block.',
             why='A heavier block presses the surfaces together with a larger force, so friction increases.'))

R.facts('ch10-st2', F(
    terms=[('speed', 'the distance travelled per unit time: speed = distance ÷ time'),
           ('average speed', 'total distance travelled ÷ total time taken'),
           ('distance–time graph', 'a graph of distance against time; the gradient gives the speed'),
           ('stationary', 'not moving; shown by a horizontal line on a distance–time graph'),
           ('m/s', 'the SI unit of speed (metres per second)')],
    facts=[('What does a horizontal line on a distance–time graph show?', 'The object is stationary', ['Constant speed', 'Accelerating', 'Moving backwards'], 'Distance does not change.'),
           ('What does a steeper straight line on a distance–time graph show?', 'A faster constant speed', ['A slower speed', 'Stopping', 'Acceleration'], 'Gradient = speed.'),
           ('Which unit is used for speed?', 'm/s', ['N', 'kg', 'm/s²'], 'Also km/h.'),
           ('A curved line getting steeper on a distance–time graph shows…', 'the object is speeding up', ['the object is slowing down', 'the object is stationary', 'constant speed'], 'The gradient is increasing.'),
           ('How many seconds are in one hour?', '3600', ['60', '360', '1000'], '60 × 60.')],
    why=[('Explain why the speed shown on a car speedometer is different from the average speed for a journey.', 'The speedometer shows the instantaneous speed, which changes; the average speed is total distance ÷ total time, including stops.'),
         ('Explain why light gates give a more accurate speed than a stopwatch for a trolley.', 'They measure time automatically to a fraction of a millisecond, removing human reaction time.'),
         ('Explain how to use a distance–time graph to find speed.', 'Choose two points on a straight section; speed = change in distance ÷ change in time (the gradient).')],
    contrast=[('the speed of a car', 'its velocity', 'Speed is how fast something moves (distance per time); velocity is speed in a given direction.'),
              ('average speed', 'instantaneous speed', 'Average speed is total distance ÷ total time for a journey; instantaneous speed is the speed at one moment.')],
    misc=[('A line going down on a distance–time graph means the object is slowing down.', 'It means the object is moving back towards the start; slowing down is shown by a curve that becomes less steep.'),
          ('Faster objects always travel further.', 'Distance depends on both speed and time; a slower object moving for longer can travel further.')],
    cases=[('Average speed cameras', 'Pairs of cameras record a car’s number plate at two points a known distance apart; the time between gives average speed, catching drivers who slow only near single cameras.', 'speed = distance ÷ time in technology', 'They have reduced speeding and crashes on many roads.')],
    evaluate=[('Average speed cameras should replace all fixed speed cameras.', ['stop drivers braking just at cameras', 'smoother traffic and fewer crashes'], ['more expensive to install', 'privacy concerns about tracking cars'], 'They are more effective on long stretches of road, but cost and privacy must be balanced.')],
    extended=[('A cyclist rides 6 km in 20 min, stops for 10 min, then rides 9 km in 30 min. Describe the distance–time graph and calculate the speed for each section and the average speed in km/h.', 'Section 1: straight line rising 6 km in 20 min → 18 km/h. Stop: horizontal line for 10 min (0 km/h). Section 2: straight line rising 9 km in 30 min → 18 km/h (same gradient). Average = 15 km ÷ 1 h = 15 km/h.', 6)],
))


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def speed_calc(rng, slot):
    k = rng.choice(['v', 'd', 't', 'kmh'] if slot.d >= 2 else ['v', 'd'])
    who = name(rng)
    if k == 'v':
        d = rng.choice([100, 200, 400, 800, 1500])
        t = rng.choice([12.5, 25, 40, 50, 80, 100, 250])
        return dict(stem=f'{who} runs {d} m in {g(t)} s. Calculate the average speed.', answer=f'{g(d / t)} m/s', markingKey=f'M1 speed = distance ÷ time = {d} ÷ {g(t)}; A1 {g(d / t)} m/s.', marks=2)
    if k == 'd':
        v = rng.choice([1.5, 3, 4.5, 12, 20, 25])
        t = rng.choice([10, 30, 60, 120])
        return dict(stem=f'A {rng.choice(["toy train", "bus", "cyclist", "drone"])} travels at a steady {g(v)} m/s for {t} s. How far does it travel?', answer=f'{g(v * t)} m', markingKey=f'M1 distance = speed × time = {g(v)} × {t}; A1 {g(v * t)} m.', marks=2)
    if k == 't':
        d = rng.choice([300, 600, 900, 1200])
        v = rng.choice([1.5, 2, 3, 5])
        return dict(stem=f'{who} walks {d} m to school at an average speed of {g(v)} m/s. How long does the walk take, in minutes?', answer=f'{g(d / v / 60)} min',
                    markingKey=f'M1 time = distance ÷ speed = {d} ÷ {g(v)} = {g(d / v)} s; M1 ÷ 60; A1 {g(d / v / 60)} min.', marks=3)
    v = rng.choice([36, 54, 72, 90, 108])
    return dict(stem=f'A car travels at {v} km/h. Convert this speed to m/s.', answer=f'{g(v / 3.6)} m/s', markingKey=f'M1 {v} × 1000 ÷ 3600; A1 {g(v / 3.6)} m/s.', marks=2)


inquiry('ch10-st2',
        dict(ctx='how the height of a ramp affects the average speed of a toy car travelling down it',
             iv='height of the ramp’s raised end (10, 20, 30, 40, 50 cm)', dv='average speed = 1.0 m ÷ time measured with light gates',
             cvs=[('length of the ramp (1.0 m)', 'distance used in speed calculation'), ('the same car', 'mass and wheels affect speed'), ('release from rest without pushing', 'pushing adds speed'), ('surface of the ramp', 'friction affects speed')],
             hyp='If the ramp is higher, then the car will have a greater average speed, because more gravitational potential energy is converted to kinetic energy.',
             method='Set up a 1.0 m ramp with light gates at the top and bottom connected to a timer; raise the end to 10 cm; release the car from behind the top gate; record the time; calculate speed = 1.0 ÷ time; repeat three times for each height; plot speed against height.',
             weak=('the car hit the side of the ramp on some runs', 'add guide rails and discard runs where the car hits the sides'),
             safety='place a soft barrier to stop the car at the bottom; keep the floor clear'))
dataset('ch10-st2',
        dict(intro='{who} recorded the distance travelled by a cyclist every 10 s using a GPS app (three rides on the same route).', iv=('Time', 's'), xs=[10, 20, 30, 40, 50],
             dv=('Distance', 'm'), f=lambda x: 6 * x, dp=0, trend='The distance increases by about the same amount every 10 s, so the cyclist moves at a roughly constant speed of about 6 m/s.',
             why='Equal distances in equal times means a constant speed; on a distance–time graph this is a straight line whose gradient gives the speed.'))

R.facts('ch10-st3', F(
    terms=[('balanced forces', 'forces that are equal in size and opposite in direction, giving zero resultant force'),
           ('unbalanced forces', 'forces that do not cancel, giving a resultant force that changes the motion'),
           ('resultant force', 'the single force that has the same effect as all the forces acting on an object'),
           ('acceleration', 'the rate of change of velocity'),
           ('terminal velocity', 'the constant top speed reached when air resistance equals weight')],
    facts=[('A car moves at a constant speed in a straight line. What can you say about the forces?', 'They are balanced', ['They are unbalanced forwards', 'There are no forces', 'Only gravity acts'], 'No resultant force → no change in motion.'),
           ('Forces of 30 N right and 12 N left act on a box. What is the resultant force?', '18 N to the right', ['42 N to the right', '18 N to the left', '0 N'], 'Subtract opposite forces.'),
           ('What happens to a stationary object if the forces on it are balanced?', 'It stays still', ['It speeds up', 'It moves at constant speed', 'It changes direction'], 'Newton’s first law.'),
           ('What does an unbalanced force do to a moving object?', 'Changes its speed or direction', ['Keeps it at constant speed', 'Has no effect', 'Always stops it'], 'It accelerates.')],
    why=[('Explain why a skydiver reaches a terminal velocity.', 'As speed increases, air resistance increases until it equals weight; the resultant force is zero so the speed stays constant.'),
         ('Explain why a car needs to keep its engine running to travel at constant speed on a flat road.', 'Friction and air resistance act backwards; the engine provides a forward force that balances them.'),
         ('Explain why a ball thrown upwards slows down.', 'Weight (and air resistance) act downwards, opposite to its motion, giving a resultant force that decelerates it.')],
    contrast=[('balanced forces', 'unbalanced forces', 'Balanced forces give zero resultant force, so an object stays still or moves at constant velocity; unbalanced forces give a resultant that changes speed or direction.')],
    misc=[('If an object is moving, the forces on it must be unbalanced.', 'An object moving at constant velocity has balanced forces; unbalanced forces are needed only to change its motion.'),
          ('A stationary object has no forces acting on it.', 'Forces act on it (e.g. weight and reaction force) but they are balanced.')],
    cases=[('Isaac Newton’s laws of motion (1687)', 'In the Principia, Newton stated that an object stays at rest or constant velocity unless a resultant force acts, and that force causes acceleration.', 'laws of motion', 'His laws explained motion on Earth and of the planets and are still used to design vehicles and launch spacecraft.')],
    evaluate=[('Seat belts should be compulsory for all passengers in buses.', ['passengers keep moving forward when the bus stops suddenly (no force to stop them)', 'reduce injuries in crashes'], ['costly to fit in all buses', 'standing passengers cannot use them', 'buses are already relatively safe'], 'Seat belts make sense on long-distance coaches; for city buses, other safety measures may be more practical.')],
    extended=[('A rocket of weight 20 000 N has an engine thrust of 26 000 N at launch. Calculate the resultant force and describe and explain how the rocket’s motion and the forces change as it rises and burns fuel.', 'Resultant = 26 000 − 20 000 = 6000 N upwards – rocket accelerates upwards. As fuel burns, mass and weight decrease so resultant force increases (if thrust constant) – acceleration increases; air resistance increases with speed, reducing the resultant; higher up, air is thinner and gravity slightly weaker.', 6)],
))


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def resultant(rng, slot):
    a = rng.choice([20, 35, 50, 120, 400, 800])
    b = rng.choice([10, 15, 20, 50, 300, 800])
    who = name(rng)
    obj = rng.choice(['a sledge', 'a box', 'a boat', 'a trolley'])
    r = a - b
    if r == 0:
        desc = 'zero; the forces are balanced, so it stays still or moves at constant speed'
    else:
        desc = f'{abs(r)} N {"forwards" if r > 0 else "backwards"}; it {"speeds up" if r > 0 else "slows down (if moving forwards)"}'
    return dict(stem=f'{who} pulls {obj} forwards with a force of {a} N. Friction acts backwards with a force of {b} N. Calculate the resultant force and describe the effect on the motion of {obj}.', answer=desc,
                markingKey=f'M1 resultant = {a} − {b}; A1 {abs(r)} N {"(balanced)" if r == 0 else ("forwards" if r > 0 else "backwards")}; B1 effect on motion.', marks=3)


inquiry('ch10-st3',
        dict(ctx='how the area of a paper parachute affects its terminal velocity',
             iv='area of the parachute canopy (100, 200, 300, 400, 500 cm²)', dv='time to fall the last 1.0 m of a 2.5 m drop (used to calculate terminal velocity)',
             cvs=[('mass of the load (paper clips)', 'weight affects terminal velocity'), ('drop height', 'must be enough to reach terminal velocity'), ('material and string length', 'affects air resistance'), ('no draughts', 'air currents change the fall')],
             hyp='If the canopy area increases, then terminal velocity will decrease, because larger canopies have more air resistance, which balances the weight at a lower speed.',
             method='Make square paper canopies of each area with the same strings and two paper clips; drop from 2.5 m; time from the 1.0 m mark to the floor (or video it with a metre rule); speed = 1.0 ÷ time; repeat five times; plot terminal velocity against area.',
             weak=('times were very short and hard to measure with a stopwatch', 'film the fall and use the frame count, or increase the drop height'),
             safety='use a stable platform or stairwell with supervision; do not lean over balconies'))
dataset('ch10-st3',
        dict(intro='{who} used a data logger to record the speed of a falling cupcake case at different times after release.', iv=('Time', 's'), xs=[0.1, 0.2, 0.4, 0.6, 0.8],
             dv=('Speed', 'm/s'), f=lambda x: 1.2 * (1 - math.exp(-x / 0.15)), dp=2, trend='The speed increases quickly at first and then levels off at a constant (terminal) speed.',
             why='At first weight is larger than air resistance so it accelerates; air resistance increases with speed until it equals weight, and then the resultant force is zero.'))

R.facts('ch10-st4', F(
    terms=[('mass', 'the amount of matter in an object, measured in kilograms (kg)'),
           ('weight', 'the force of gravity on an object, measured in newtons (N)'),
           ('gravitational field strength (g)', 'the force of gravity on each kilogram; about 10 N/kg on Earth'),
           ('gravity', 'the force of attraction between all objects with mass')],
    facts=[('What is the weight of a 5 kg bag on Earth (g = 10 N/kg)?', '50 N', ['5 N', '0.5 N', '500 N'], 'W = m × g.'),
           ('What happens to your mass if you travel to the Moon?', 'It stays the same', ['It decreases to one-sixth', 'It becomes zero', 'It increases'], 'Weight changes, mass does not.'),
           ('Why do astronauts weigh less on the Moon?', 'The Moon’s gravitational field strength is smaller', ['They have less mass', 'There is no air', 'The Moon is further from the Sun'], 'g ≈ 1.6 N/kg.'),
           ('Which unit is used for weight?', 'Newton (N)', ['Kilogram (kg)', 'Gram (g)', 'N/kg'], 'Weight is a force.')],
    why=[('Explain why weight is a force but mass is not.', 'Weight is the pull of gravity on an object, so it has a direction and is measured in newtons; mass is the amount of matter and does not depend on gravity.'),
         ('Explain why an object’s weight is different on different planets.', 'Weight = mass × gravitational field strength, and g depends on the mass and size of the planet.'),
         ('Explain why a balance on Earth can be used to measure mass even though it really measures weight.', 'On Earth g is almost constant, so weight is proportional to mass and the scale is marked in kg.')],
    contrast=[('the mass of an astronaut', 'her weight', 'Mass is the amount of matter, in kg, and is the same everywhere; weight is the force of gravity on that mass, in N, and depends on the gravitational field strength.')],
    misc=[('Mass and weight are the same thing.', 'Mass is in kg and never changes with location; weight is a force in N that changes with gravity.'),
          ('There is no gravity in space.', 'Gravity acts throughout space; astronauts in orbit feel weightless because they are in free fall around the Earth.')],
    cases=[('Apollo 15 hammer and feather (1971)', 'Astronaut David Scott dropped a hammer and a feather on the Moon; with no air resistance, they hit the ground together.', 'gravity and air resistance', 'It confirmed Galileo’s idea that all objects fall with the same acceleration without air resistance.')],
    evaluate=[('Space tourism should be encouraged.', ['inspires interest in science', 'funds development of new technology'], ['huge fuel use and emissions per passenger', 'only for the very wealthy', 'safety risks'], 'Space tourism brings some benefits, but environmental and fairness concerns mean it should be regulated.')],
    extended=[('A 70 kg astronaut travels from Earth (g = 10 N/kg) to the Moon (g = 1.6 N/kg) and Mars (g = 3.7 N/kg). Calculate her weight on each, state her mass on each, and explain the differences.', 'Earth 700 N; Moon 112 N; Mars 259 N; mass 70 kg everywhere. Weight depends on g, which is smaller on the Moon and Mars because they have less mass than Earth; mass is the amount of matter and does not change.', 5)],
))


@R.add('ch10-st4', 'C3', (1, 5), 'numerical')
def weight(rng, slot):
    pl, gg = rng.choice([('Earth', 10), ('the Moon', 1.6), ('Mars', 3.7), ('Jupiter', 25), ('Venus', 8.9)])
    k = rng.choice(['W', 'm', 'g'] if slot.d >= 2 else ['W'])
    m = rng.choice([2, 5, 12, 45, 60, 80, 250])
    W = m * gg
    if k == 'W':
        return dict(stem=f'Calculate the weight of a {m} kg object on {pl}, where g = {g(gg)} N/kg.', answer=f'{g(W)} N', markingKey=f'M1 W = m × g = {m} × {g(gg)}; A1 {g(W)} N.', marks=2)
    if k == 'm':
        return dict(stem=f'A rover has a weight of {g(W)} N on {pl} (g = {g(gg)} N/kg). Calculate its mass.', answer=f'{m} kg', markingKey=f'M1 m = W ÷ g = {g(W)} ÷ {g(gg)}; A1 {m} kg.', marks=2)
    return dict(stem=f'A {m} kg probe has a weight of {g(W)} N on {pl}. Calculate the gravitational field strength there.', answer=f'{g(gg)} N/kg', markingKey=f'M1 g = W ÷ m = {g(W)} ÷ {m}; A1 {g(gg)} N/kg.', marks=2)


inquiry('ch10-st4',
        dict(ctx='how the mass of an object affects its weight',
             iv='mass hung on a newton meter (100, 200, 300, 400, 500 g)', dv='weight read from the newton meter',
             cvs=[('the same newton meter, zeroed', 'zero error'), ('reading at eye level', 'parallax error'), ('meter held still and vertical', 'swinging changes the reading'), ('masses checked on a balance', 'slotted masses can be inaccurate')],
             hyp='If the mass increases, then the weight will increase in direct proportion, because weight = mass × g and g is constant.',
             method='Zero a 10 N newton meter; hang 100 g and read the weight at eye level; add masses up to 500 g; repeat three times; convert mass to kg; plot weight against mass; gradient gives g.',
             weak=('masses were read from their labels only', 'check each mass on a calibrated balance'),
             safety='do not overload the newton meter; keep feet clear of falling masses'))
dataset('ch10-st4',
        dict(intro='{who} measured the weight of different masses with a newton meter, three times each.', iv=('Mass', 'kg'), xs=[0.1, 0.2, 0.3, 0.4, 0.5],
             dv=('Weight', 'N'), f=lambda x: 9.8 * x, dp=2, trend='Weight increases in direct proportion to mass.',
             why='Weight = mass × gravitational field strength; g (about 9.8 N/kg) is constant on Earth, so the graph is a straight line through the origin with gradient g.'))

R.facts('ch10-st5', F(
    terms=[('pressure', 'force per unit area: pressure = force ÷ area'),
           ('pascal (Pa)', 'the unit of pressure, equal to 1 N/m²'),
           ('moment', 'the turning effect of a force: moment = force × perpendicular distance from the pivot'),
           ('pivot', 'the point around which something turns'),
           ('principle of moments', 'for a balanced object, total clockwise moment = total anticlockwise moment'),
           ('lever', 'a rigid bar that turns about a pivot, used to multiply force')],
    facts=[('Why do snowshoes stop you sinking into snow?', 'They spread your weight over a larger area, reducing pressure', ['They make you lighter', 'They increase pressure', 'They melt the snow'], 'Same force, more area.'),
           ('What happens to water pressure as you go deeper?', 'It increases', ['It decreases', 'It stays the same', 'It becomes zero'], 'More water above pushes down.'),
           ('Why is a long spanner easier to use?', 'A larger distance from the pivot gives a larger moment for the same force', ['It is heavier', 'It reduces friction', 'It increases pressure'], 'Moment = F × d.'),
           ('What is the unit of a moment?', 'N m', ['N', 'Pa', 'N/m²'], 'Newton metres.'),
           ('Why does a sharp knife cut better than a blunt one?', 'The small area of the edge gives a large pressure', ['It has a larger area', 'It is heavier', 'It has less friction'], 'P = F/A.')],
    why=[('Explain why dams are built thicker at the bottom.', 'Water pressure increases with depth, so the bottom of the dam must withstand much greater pressure.'),
         ('Explain why a seesaw can balance a heavy adult and a light child.', 'The child sits further from the pivot, so child’s weight × distance can equal adult’s weight × smaller distance.'),
         ('Explain why camels have large flat feet.', 'They spread the camel’s weight over a large area, reducing pressure so they do not sink into sand.')],
    contrast=[('force', 'pressure', 'Force is a push or pull in N; pressure is how concentrated the force is – force per unit area, in Pa.'),
              ('clockwise moments', 'anticlockwise moments', 'Clockwise moments turn an object one way about the pivot and anticlockwise moments the other way; when they are equal the object balances.')],
    misc=[('A heavier person always exerts more pressure on the ground.', 'Pressure depends on area too; a lighter person in stiletto heels can exert more pressure than a heavier person in flat shoes.'),
          ('The moment only depends on how hard you push.', 'The moment also depends on the perpendicular distance from the pivot.')],
    cases=[('Archimedes and levers', 'Archimedes explained the law of the lever and is quoted as saying “Give me a place to stand and I will move the Earth.”', 'principle of moments', 'Levers are used in wheelbarrows, crowbars, scissors and the human arm.')],
    evaluate=[('High-heeled shoes should be banned in buildings with wooden floors.', ['small heel area creates very high pressure that dents floors', 'protects historic buildings'], ['personal freedom of choice', 'heel protectors can increase the area'], 'Requiring heel protectors is a reasonable compromise rather than a ban.')],
    extended=[('A 40 kg child sits 1.5 m from the pivot of a seesaw. Where must a 60 kg adult sit to balance it? Explain your working using the principle of moments, and explain why the seesaw tips if the adult moves further away. (g = 10 N/kg)', 'Child weight 400 N, moment = 400 × 1.5 = 600 N m anticlockwise. Adult weight 600 N; balance: 600 × d = 600 → d = 1.0 m. Moving further increases the adult’s moment above 600 N m, so clockwise > anticlockwise and the seesaw tips towards the adult.', 6)],
))


@R.add('ch10-st5', 'C3', (1, 5), 'numerical')
def pressure_moments(rng, slot):
    k = rng.choice(['p', 'mom', 'bal', 'pa'] if slot.d >= 2 else ['p', 'mom'])
    if k == 'p':
        F_ = rng.choice([500, 600, 750, 900, 1200])
        A = rng.choice([0.02, 0.03, 0.05, 0.1, 0.25])
        return dict(stem=f'A person with a weight of {F_} N stands on a total foot area of {A} m². Calculate the pressure on the floor.', answer=f'{g(F_ / A)} Pa',
                    markingKey=f'M1 p = F ÷ A = {F_} ÷ {A}; A1 {g(F_ / A)} Pa.', marks=2)
    if k == 'pa':
        F_ = rng.choice([20, 40, 60])
        a = rng.choice([2, 4, 5, 8])
        return dict(stem=f'A drawing pin is pushed with a force of {F_} N. The point has an area of 0.{a:02d} mm² = {a} × 10⁻⁸ m². Calculate the pressure at the point.', answer=f'{F_ / (a * 1e-8):.2e} Pa'.replace('e+0', ' × 10^').replace('e+', ' × 10^'),
                    markingKey=f'M1 p = {F_} ÷ ({a} × 10⁻⁸); A1 {F_ / (a * 1e-8):.2e} Pa'.replace('e+0', ' × 10^').replace('e+', ' × 10^') + '.', marks=2)
    if k == 'mom':
        F_ = rng.choice([20, 25, 40, 60, 80])
        d = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5])
        return dict(stem=f'A force of {F_} N is applied {g(d)} m from the pivot of a spanner. Calculate the moment of the force.', answer=f'{g(F_ * d)} N m',
                    markingKey=f'M1 moment = F × d = {F_} × {g(d)}; A1 {g(F_ * d)} N m.', marks=2)
    w1, d1 = rng.choice([(300, 2.0), (400, 1.5), (500, 1.2), (250, 2.4)])
    w2 = rng.choice([600, 750, 800, 1000])
    d2 = w1 * d1 / w2
    return dict(stem=f'A child of weight {w1} N sits {d1} m from the pivot of a seesaw. How far from the pivot must a person of weight {w2} N sit on the other side to balance it?', answer=f'{g(d2)} m',
                markingKey=f'M1 anticlockwise moment = {w1} × {d1} = {g(w1 * d1)} N m; M1 {w2} × d = {g(w1 * d1)}; A1 d = {g(d2)} m.', marks=3)


inquiry('ch10-st5',
        dict(ctx='how the depth of water affects the pressure at a point',
             iv='depth below the water surface (5, 10, 15, 20, 25 cm)', dv='distance a jet of water squirts horizontally from holes at each depth in a tall bottle',
             cvs=[('water level kept constant (top up)', 'level falls as water escapes'), ('size of holes', 'larger holes change the jet'), ('height of the bottle above the tray', 'affects where the jet lands'), ('the same bottle', 'shape affects flow')],
             hyp='If the hole is deeper, then the water will squirt further, because pressure increases with depth due to the weight of water above.',
             method='Make five holes of the same size at 5 cm intervals in a tall plastic bottle, covered with tape; fill with water and keep topped up; remove tape from all holes; measure horizontal distance of each jet at the tray level; repeat three times; plot distance against depth.',
             weak=('the water level dropped during the measurements', 'keep a hose running in so the level stays at the top mark'),
             safety='work over a tray or sink and mop spills; cut bottle holes carefully with a hot pin under supervision'))
dataset('ch10-st5',
        dict(intro='{who} balanced a metre rule on a pivot at its centre, hung a 2 N weight 20 cm to the left and found the force needed at different distances to the right (three trials each).', iv=('Distance on the right', 'cm'), xs=[10, 20, 25, 40, 50],
             dv=('Force needed to balance', 'N'), f=lambda x: 40 / x, dp=2, trend='The force needed decreases as the distance from the pivot increases; force × distance stays roughly constant at about 40 N cm.',
             why='The principle of moments: the clockwise moment (F × d) must equal the anticlockwise moment (2 N × 20 cm), so a larger distance needs a smaller force.'))


# =============================================================================================
# ch11 Energy
# =============================================================================================
R.facts('ch11-st1', F(
    terms=[('energy store', 'a way energy is held, such as kinetic, gravitational potential, chemical, elastic, thermal or nuclear'),
           ('kinetic energy', 'energy stored in a moving object'),
           ('gravitational potential energy', 'energy stored in an object because of its height above the ground'),
           ('elastic potential energy', 'energy stored in a stretched or squashed object'),
           ('energy pathway', 'how energy is transferred between stores: by forces (mechanically), by heating, by electricity or by radiation'),
           ('joule (J)', 'the unit of energy')],
    facts=[('Which energy store increases as a ball is lifted onto a shelf?', 'Gravitational potential', ['Kinetic', 'Elastic', 'Nuclear'], 'Higher position.'),
           ('What energy store is in food and fuels?', 'Chemical', ['Kinetic', 'Thermal', 'Elastic'], 'Released by reactions.'),
           ('What energy transfer happens when a stretched catapult is released?', 'Elastic potential → kinetic', ['Kinetic → elastic', 'Chemical → nuclear', 'Thermal → chemical'], 'The stone speeds up.'),
           ('Which pathway transfers energy from the Sun to Earth?', 'Radiation (light and infrared)', ['Electrical current', 'Conduction', 'Mechanical work'], 'It travels through space.'),
           ('What is the unit of energy?', 'Joule (J)', ['Watt (W)', 'Newton (N)', 'Volt (V)'], '1 kJ = 1000 J.')],
    why=[('Explain the energy changes when a person bungee jumps.', 'GPE → kinetic as she falls; the cord stretches, transferring kinetic to elastic potential; she slows, then the cord pulls her back up (elastic → kinetic → GPE); some energy is dissipated as heat.'),
         ('Explain why a moving car has more kinetic energy at higher speed.', 'Kinetic energy depends on the square of speed, so doubling speed quadruples the kinetic energy store.'),
         ('Explain why a battery-powered torch is described as transferring energy electrically.', 'The current transfers energy from the chemical store of the battery to the lamp, where it is transferred by light and heating to the surroundings.')],
    contrast=[('an energy store', 'an energy pathway', 'An energy store is where energy is held (kinetic, chemical, thermal …); a pathway is how energy moves between stores (by forces, heating, electricity, radiation).'),
              ('kinetic energy', 'gravitational potential energy', 'Kinetic energy is stored by moving objects and depends on mass and speed; GPE is stored due to height in a gravitational field and depends on mass, g and height.')],
    misc=[('Energy gets used up.', 'Energy is never destroyed; it is transferred to other stores, often spreading out as thermal energy in the surroundings.'),
          ('Only moving things have energy.', 'Still objects can store energy in chemical, gravitational, elastic, thermal or nuclear stores.')],
    evaluate=[('Gravity-powered lamps (a falling weight driving a generator) are a good solution for homes without electricity.', ['no fuel or batteries; safer than kerosene lamps', 'cheap to run'], ['need re-lifting every 20–30 minutes', 'low light output'], 'They are a useful, safe low-cost option for basic lighting where there is no grid, though limited in power.')],
    extended=[('Describe the energy stores and transfers for a pendulum swinging, and explain why it eventually stops.', 'At the highest point maximum GPE, zero KE; as it swings down GPE → KE (by gravity/forces), maximum KE at the bottom; then KE → GPE as it rises. Each swing some energy is transferred by friction at the pivot and air resistance to the thermal store of the surroundings, so the amplitude decreases until it stops. Total energy is conserved.', 6)],
))


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def ke_gpe(rng, slot):
    k = rng.choice(['ke', 'gpe', 'v'] if slot.d >= 3 else ['ke', 'gpe'])
    m = rng.choice([0.5, 2, 5, 40, 60, 1000])
    if k == 'ke':
        v = rng.choice([2, 3, 4, 10, 15, 20])
        return dict(stem=f'Calculate the kinetic energy of a {g(m)} kg object moving at {v} m/s (KE = ½mv²).', answer=f'{g(0.5 * m * v * v)} J', markingKey=f'M1 ½ × {g(m)} × {v}²; A1 {g(0.5 * m * v * v)} J.', marks=2)
    if k == 'gpe':
        h = rng.choice([1.5, 2, 5, 10, 25])
        return dict(stem=f'A {g(m)} kg object is lifted {g(h)} m. Calculate the gain in gravitational potential energy (GPE = mgh, g = 10 N/kg).', answer=f'{g(m * 10 * h)} J', markingKey=f'M1 {g(m)} × 10 × {g(h)}; A1 {g(m * 10 * h)} J.', marks=2)
    h = rng.choice([5, 20, 45, 80])
    v = math.sqrt(2 * 10 * h)
    return dict(stem=f'A ball is dropped from {h} m. Ignoring air resistance, calculate its speed just before it hits the ground (g = 10 N/kg).', answer=f'{g(v)} m/s',
                markingKey=f'M1 GPE lost = KE gained: mgh = ½mv²; M1 v = √(2 × 10 × {h}); A1 {g(v)} m/s.', marks=3)


inquiry('ch11-st1',
        dict(ctx='how the drop height of a ball affects its bounce height',
             iv='drop height (50, 100, 150, 200 cm)', dv='bounce height measured against a metre rule (or from a video)',
             cvs=[('the same ball', 'balls differ in elasticity'), ('surface (the same floor)', 'soft surfaces absorb energy'), ('dropped, not thrown', 'throwing adds kinetic energy'), ('measuring from the bottom of the ball', 'consistent reference point')],
             hyp='If the drop height increases, then the bounce height will increase in proportion, because more GPE is converted to KE and then back to GPE, with a similar fraction lost each time.',
             method='Fix a metre rule vertically; drop the ball from each height; film the bounce and use slow-motion playback to read the bounce height; repeat five times; calculate means and the ratio bounce ÷ drop height.',
             weak=('the bounce height was judged by eye in real time', 'film against a scale and use slow-motion playback'),
             safety='keep the area clear; do not stand on chairs – use a stable step'))
dataset('ch11-st1',
        dict(intro='{who} released a trolley from different heights on a ramp and measured its speed at the bottom with a light gate.', iv=('Release height', 'm'), xs=[0.1, 0.2, 0.3, 0.4, 0.5],
             dv=('Speed at bottom', 'm/s'), f=lambda x: 0.9 * math.sqrt(20 * x), dp=2, trend='The speed at the bottom increases with release height, but by less for each extra 0.1 m.',
             why='GPE (mgh) is transferred to KE (½mv²), so v² is proportional to h; friction transfers some energy to thermal stores, so speeds are a little below the ideal values.'))

R.facts('ch11-st2', F(
    terms=[('conservation of energy', 'energy cannot be created or destroyed, only transferred from one store to another'),
           ('useful energy', 'energy transferred to the store we want'),
           ('wasted energy', 'energy transferred to stores that are not wanted, usually thermal energy of the surroundings'),
           ('efficiency', 'the fraction of input energy that is usefully transferred: useful output ÷ total input × 100%'),
           ('dissipated', 'spread out to the surroundings so that it is less useful'),
           ('Sankey diagram', 'a diagram with arrow widths proportional to the energy transferred')],
    facts=[('A light bulb uses 100 J and gives out 20 J as light. What is its efficiency?', '20%', ['80%', '120%', '5%'], '20 ÷ 100 × 100.'),
           ('Why can no device be 100% efficient?', 'Some energy is always dissipated, usually as heat', ['Energy is destroyed', 'Devices create energy', 'Electricity is wasted in wires only'], 'Friction and resistance.'),
           ('In a Sankey diagram, what does a wider arrow show?', 'More energy transferred', ['Faster transfer', 'Less energy', 'More useful energy only'], 'Width ∝ energy.'),
           ('Which is a way to reduce wasted energy in a machine?', 'Lubricating moving parts', ['Adding more friction', 'Making it heavier', 'Using thinner wires'], 'Less friction → less heating.'),
           ('A motor is 75% efficient. How much useful energy does it give out from 400 J input?', '300 J', ['75 J', '325 J', '533 J'], '0.75 × 400.')],
    why=[('Explain why LED bulbs are more efficient than filament bulbs.', 'Filament bulbs transfer most energy by heating; LEDs transfer a much larger fraction of the electrical energy as light.'),
         ('Explain why the total energy output of a device equals its input.', 'Energy is conserved; it is only transferred, so useful plus wasted energy equals the input.'),
         ('Explain why wasted energy is hard to use.', 'It is dissipated – spread thinly into the surroundings as thermal energy at a low temperature.')],
    contrast=[('useful energy', 'wasted energy', 'Useful energy is transferred to the store we want (e.g. light from a lamp); wasted energy is transferred to unwanted stores, usually thermal energy of the surroundings.'),
              ('power', 'energy', 'Energy is the amount transferred, in J; power is how fast energy is transferred, in watts (J/s).')],
    misc=[('An efficient machine wastes no energy.', 'Even efficient machines waste some energy; efficiency is always less than 100%.'),
          ('Efficiency can be over 100% if the machine is very good.', 'That would mean creating energy, which breaks the law of conservation of energy.')],
    cases=[('Phasing out incandescent bulbs', 'From 2009 the EU and many other countries phased out filament bulbs, which waste about 90–95% of their energy as heat, in favour of LEDs and compact fluorescent lamps.', 'efficiency and policy', 'Lighting electricity use fell dramatically, reducing emissions and household bills.')],
    evaluate=[('Governments should ban inefficient appliances.', ['cuts energy use and emissions', 'saves money for households over time'], ['efficient models may cost more to buy', 'limits consumer choice'], 'Bans with clear labelling and support for low-income households have proven effective.')],
    extended=[('An electric kettle takes in 200 000 J and transfers 170 000 J to the water. Calculate its efficiency, describe where the wasted energy goes, draw (describe) a Sankey diagram, and suggest two improvements.', 'Efficiency = 170 000 ÷ 200 000 × 100 = 85%. Wasted 30 000 J: heats the kettle body, air, and sound. Sankey: input arrow 200 kJ splitting into a wide 170 kJ useful arrow and a narrow 30 kJ wasted arrow. Improvements: better insulation (double wall), only boil the water needed, lid to reduce evaporation.', 6)],
))


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def efficiency(rng, slot):
    dev, use = rng.choice([('motor', 'kinetic energy'), ('LED lamp', 'light'), ('kettle', 'thermal energy of the water'), ('loudspeaker', 'sound'), ('filament bulb', 'light'), ('solar panel', 'electrical energy')])
    inp = rng.choice([200, 500, 800, 1000, 2400, 5000])
    eff = rng.choice([5, 10, 20, 25, 40, 75, 80, 90])
    if dev == 'solar panel':
        eff = rng.choice([15, 18, 20, 22])
    out = inp * eff / 100
    k = rng.choice(['eff', 'out', 'waste'] if slot.d >= 2 else ['eff'])
    if k == 'eff':
        return dict(stem=f'A {dev} takes in {inp} J of energy and transfers {g(out)} J as {use}. Calculate its efficiency.', answer=f'{eff}%',
                    markingKey=f'M1 efficiency = useful ÷ total × 100 = {g(out)} ÷ {inp} × 100; A1 {eff}%.', marks=2)
    if k == 'out':
        return dict(stem=f'A {dev} is {eff}% efficient. How much energy is transferred as {use} for every {inp} J supplied?', answer=f'{g(out)} J',
                    markingKey=f'M1 {eff} ÷ 100 × {inp}; A1 {g(out)} J.', marks=2)
    return dict(stem=f'A {dev} is {eff}% efficient and is supplied with {inp} J. Calculate the energy wasted and state where most of it goes.', answer=f'{g(inp - out)} J; mostly dissipated as thermal energy in the surroundings',
                markingKey=f'M1 useful = {g(out)} J; M1 wasted = {inp} − {g(out)}; A1 {g(inp - out)} J; B1 thermal store of surroundings.', marks=4)


inquiry('ch11-st2',
        dict(ctx='how the load lifted by an electric motor affects its efficiency',
             iv='mass lifted (100, 200, 300, 400, 500 g)', dv='efficiency = GPE gained (mgh) ÷ electrical energy supplied (V × I × t) × 100',
             cvs=[('height lifted (1.0 m)', 'needed to calculate GPE'), ('voltage of the supply', 'affects the input power'), ('the same motor and string', 'different motors have different losses'), ('timing method', 'affects energy calculation')],
             hyp='If the load increases, then the efficiency will increase up to a point, because a larger fraction of the input energy goes into lifting rather than overcoming fixed losses such as friction.',
             method='Clamp a motor at the bench edge; attach a string to the load; connect a joulemeter (or ammeter and voltmeter); lift each load 1.0 m and record energy supplied (or V, I and time); calculate GPE = m × 10 × 1.0; efficiency = GPE ÷ input × 100; repeat three times.',
             weak=('the load swung and hit the bench', 'use a guide string or tube and stop timing at a marked line'),
             safety='keep fingers away from the spinning axle; place a soft pad under the load'))
dataset('ch11-st2',
        dict(intro='{who} measured the energy supplied to an electric kettle and the energy transferred to the water for different volumes of water.', iv=('Volume of water', 'cm³'), xs=[250, 500, 750, 1000, 1500],
             dv=('Efficiency', '%'), f=lambda x: 90 - 12000 / x, dp=0, trend='The efficiency increases as the volume of water increases, levelling off at large volumes.',
             why='Part of the energy is always used to heat the kettle itself and is lost from its surface; with more water this fixed loss is a smaller fraction of the total.'))

R.facts('ch11-st3', F(
    terms=[('conduction', 'transfer of thermal energy through a material by vibrating particles passing energy to neighbours'),
           ('convection', 'transfer of thermal energy in liquids and gases by the movement of warmer, less dense fluid'),
           ('radiation (infrared)', 'transfer of thermal energy by infrared waves, which can travel through a vacuum'),
           ('insulator', 'a material that is a poor conductor of thermal energy'),
           ('convection current', 'the circulation of fluid caused by warm fluid rising and cool fluid sinking')],
    facts=[('Why do metal spoons get hot in hot soup?', 'Metals are good thermal conductors', ['Metals are insulators', 'Convection in the spoon', 'The spoon reflects radiation'], 'Free electrons transfer energy quickly.'),
           ('Which surface is the best emitter and absorber of infrared radiation?', 'Matt black', ['Shiny silver', 'Shiny white', 'Gloss white'], 'Shiny surfaces reflect.'),
           ('How does thermal energy reach us from the Sun?', 'Radiation', ['Conduction', 'Convection', 'Evaporation'], 'Space is a vacuum.'),
           ('Why are radiators often put under windows?', 'To set up a convection current that warms the whole room', ['Because windows are hot', 'To absorb radiation from outside', 'To stop condensation only'], 'Warm air rises.'),
           ('Why does double glazing reduce heat loss?', 'The gap of trapped air or vacuum reduces conduction', ['Glass is a good conductor', 'It increases convection', 'It absorbs radiation'], 'Air is a poor conductor.')],
    why=[('Explain why convection cannot happen in solids.', 'Particles in solids are held in fixed positions so the material cannot flow; convection needs the warm fluid to move.'),
         ('Explain how a vacuum flask keeps drinks hot.', 'The vacuum stops conduction and convection; silvered walls reduce radiation; the stopper reduces convection and evaporation.'),
         ('Explain why loft insulation is made of fibreglass with lots of trapped air.', 'Air is a poor conductor and trapping it in small pockets prevents convection currents.')],
    contrast=[('conduction', 'convection', 'Conduction transfers energy through vibrating particles in contact, mostly in solids; convection transfers energy by the bulk movement of a fluid as warm, less dense regions rise.'),
              ('a good emitter of radiation', 'a good reflector', 'A good emitter (matt black) radiates and absorbs infrared well; a good reflector (shiny silver) reflects infrared and emits and absorbs it poorly.')],
    misc=[('Heat rises.', 'Hot fluids rise because they are less dense; thermal energy can be transferred in any direction by conduction and radiation.'),
          ('A woolly jumper makes you warm by giving out heat.', 'The jumper traps air, an insulator, reducing heat loss from your body; it does not produce heat.')],
    cases=[('Passive house design', 'Passive houses use thick insulation, triple glazing, airtight construction and heat-recovery ventilation, needing up to 90% less heating energy than typical homes.', 'reducing thermal energy transfer', 'Shows how controlling conduction, convection and radiation cuts energy use and emissions.')],
    evaluate=[('Governments should pay for insulation in all older homes.', ['cuts energy bills and carbon emissions', 'healthier warmer homes, fewer cold-related illnesses'], ['high upfront public cost', 'some old buildings are hard to insulate without damage (damp)'], 'Publicly funded insulation is a cost-effective climate measure, especially for low-income households, if done carefully.')],
    extended=[('Explain, using conduction, convection and radiation, how a house loses heat in winter, and evaluate three ways of reducing these losses.', 'Conduction through walls, roof, windows and floors; convection of warm air out through gaps and in cavities; radiation from walls and roof. Reduce: loft insulation (traps air – cheap, quick payback); cavity wall insulation (stops convection in cavity – moderate cost); double glazing (air gap reduces conduction – expensive, long payback); draught excluders (cheap, reduce convection).', 6)],
))


@R.add('ch11-st3', 'C3', (1, 4), 'numerical')
def cooling_rate(rng, slot):
    a = rng.choice([80, 75, 90, 70])
    d = rng.choice([12, 18, 24, 30])
    t = rng.choice([5, 10, 15])
    return dict(stem=f'Water in an uninsulated beaker cooled from {a} °C to {a - d} °C in {t} minutes. Calculate the average rate of cooling, and suggest one way to reduce it.', answer=f'{g(d / t)} °C/min; e.g. add a lid or wrap the beaker in insulation',
                markingKey=f'M1 ({a} − {a - d}) ÷ {t}; A1 {g(d / t)} °C/min; B1 lid (reduces convection/evaporation) or insulation (traps air, reduces conduction).', marks=3)


inquiry('ch11-st3',
        dict(ctx='how the colour of a can affects the rate at which hot water inside it cools',
             iv='colour of the can surface (matt black, shiny silver, white, matt grey)', dv='temperature drop in 10 minutes',
             cvs=[('starting temperature (70 °C)', 'hotter water cools faster'), ('volume of water (200 cm³)', 'more water cools more slowly'), ('size and material of can', 'surface area and conduction affect cooling'), ('lid on each can', 'stops evaporation and convection from the top')],
             hyp='If the can is matt black, then the water will cool fastest, because matt black surfaces are the best emitters of infrared radiation.',
             method='Paint or wrap identical cans; pour 200 cm³ water at 70 °C into each and fit lids with thermometers; record the temperature every minute for 10 minutes; repeat three times; compare temperature drops.',
             weak=('the cans were filled at different times so their starting temperatures differed', 'fill all cans from the same kettle at the same time and start when each reaches 70 °C'),
             safety='hot water scalds – pour carefully and use a tray'))
dataset('ch11-st3',
        dict(intro='{who} wrapped beakers of hot water in different numbers of layers of bubble wrap and measured the temperature drop in 15 minutes.', iv=('Layers of bubble wrap', ''), xs=[0, 1, 2, 3, 4],
             dv=('Temperature drop', '°C'), f=lambda x: 20 / (1 + 0.6 * x), dp=1, trend='The temperature drop decreases as the number of layers increases, with smaller improvements for each extra layer.',
             why='Bubble wrap traps air, which is a poor conductor; more layers reduce conduction and convection, so the water loses energy more slowly.'))

R.facts('ch11-st4', F(
    terms=[('renewable energy resource', 'a resource that is replenished naturally and will not run out, such as wind, solar or hydroelectric'),
           ('non-renewable energy resource', 'a resource that will run out because it is used faster than it forms, such as coal, oil, gas and uranium'),
           ('fossil fuel', 'coal, oil or natural gas formed over millions of years from the remains of living things'),
           ('greenhouse gas', 'a gas such as carbon dioxide or methane that traps heat in the atmosphere'),
           ('biofuel', 'a fuel made from plants or animal waste, such as bioethanol'),
           ('geothermal energy', 'energy from hot rocks underground')],
    facts=[('Which is a renewable energy resource?', 'Wind', ['Coal', 'Natural gas', 'Uranium'], 'It will not run out.'),
           ('Which energy resource is not available at night?', 'Solar', ['Hydroelectric', 'Geothermal', 'Nuclear'], 'Needs sunlight.'),
           ('Which gas released by burning fossil fuels contributes most to climate change?', 'Carbon dioxide', ['Oxygen', 'Nitrogen', 'Hydrogen'], 'A greenhouse gas.'),
           ('Why are fossil fuels non-renewable?', 'They take millions of years to form', ['They are made in factories', 'They come from the Sun', 'They can be reused'], 'Used faster than replaced.'),
           ('Which renewable resource is the most reliable throughout the day and year?', 'Geothermal', ['Wind', 'Solar', 'Waves'], 'Hot rocks are always hot.')],
    why=[('Explain why wind turbines alone cannot supply all of a country’s electricity.', 'Wind speed varies, so output is unreliable; storage or backup from other sources is needed when the wind is low.'),
         ('Explain why biofuels are sometimes described as carbon neutral.', 'Plants absorb CO₂ while growing, roughly equal to the CO₂ released when the fuel burns.'),
         ('Explain why fossil fuels are still widely used.', 'They are reliable, energy-dense, and existing power stations, cars and infrastructure are built to use them.')],
    contrast=[('renewable resources', 'non-renewable resources', 'Renewable resources are naturally replaced and will not run out (wind, solar, hydro); non-renewable resources are finite and will run out (coal, oil, gas, uranium).'),
              ('solar cells', 'solar water heaters', 'Solar cells transfer light energy into electricity; solar water heaters absorb infrared to heat water directly.')],
    misc=[('Renewable energy resources cause no environmental problems.', 'Renewables have impacts too – hydroelectric dams flood valleys, wind farms affect landscapes and birds, biofuel crops use land.'),
          ('Nuclear power is renewable because it produces no CO₂ when running.', 'Nuclear fuel (uranium) is finite, so it is non-renewable, even though it is low-carbon.')],
    cases=[('Iceland’s geothermal power', 'Iceland gets nearly all its electricity from hydroelectric and geothermal power and heats most homes with geothermal hot water.', 'using local renewable resources', 'It shows a country’s geography can make renewables the main supply – but not every country has these resources.')],
    evaluate=[('Every country should stop using fossil fuels within 10 years.', ['prevents dangerous climate change', 'improves air quality and health'], ['renewable capacity and storage take time and money to build', 'poorer countries may need fossil fuels to develop', 'jobs depend on fossil-fuel industries'], 'A rapid but planned transition is needed; 10 years may be too fast for some countries without support.'),
              ('Hydroelectric dams are the best renewable resource.', ['reliable and can respond quickly to demand', 'can store energy (pumped storage)'], ['flood valleys, destroying habitats and displacing people', 'only possible in suitable mountainous places'], 'Hydroelectricity is excellent where suitable, but local social and environmental costs must be weighed.')],
    extended=[('A small island community currently uses diesel generators for electricity. Evaluate replacing them with a mix of wind turbines and solar panels.', 'Benefits: no fuel costs or imports, no CO₂ or air pollution, renewable. Problems: output varies with weather and time – needs battery storage or keeping a diesel backup; high initial cost; visual impact; maintenance skills needed. Conclusion: a mix of wind and solar (complementary – windy winters, sunny summers) with batteries could supply most needs, with diesel as backup.', 6)],
))


@R.add('ch11-st4', 'C3', (1, 5), 'numerical')
def turbines_needed(rng, slot):
    need = rng.choice([20, 30, 50, 60, 120])
    each = rng.choice([2, 2.5, 3, 4])
    cf = rng.choice([25, 30, 40])
    avg = each * cf / 100
    n = math.ceil(need / avg)
    return dict(stem=f'A town needs an average power of {need} MW. Each wind turbine has a maximum output of {g(each)} MW but on average produces only {cf}% of this. How many turbines are needed? Explain why the average is less than the maximum.', answer=f'{n} turbines; the wind does not always blow at the ideal speed',
                markingKey=f'M1 average per turbine = {g(each)} × {cf}/100 = {g(avg)} MW; M1 {need} ÷ {g(avg)} = {g(need / avg)}; A1 round up to {n}; B1 wind speed varies.', marks=4)


inquiry('ch11-st4',
        dict(ctx='how the angle of a solar panel to the light affects its output',
             iv='angle between the panel and the light beam (0°, 30°, 45°, 60°, 90°)', dv='output voltage (or power) of a small solar panel measured with a voltmeter',
             cvs=[('distance from the lamp (30 cm)', 'light intensity falls with distance'), ('the same lamp and panel', 'outputs differ'), ('room darkened', 'other light adds to the output'), ('panel temperature (short exposures)', 'hot panels are less efficient')],
             hyp='If the panel faces the light directly (90°), then the output will be greatest, because more light energy falls on each square centimetre of the panel.',
             method='Fix a lamp 30 cm from a small solar panel on a protractor stand; connect a voltmeter (and a fixed resistor and ammeter for power); set each angle and record the reading after 10 s; repeat three times; plot output against angle.',
             weak=('the lamp heated the panel over time', 'use an LED lamp and switch off between readings'),
             safety='lamps get hot; do not look directly into bright lamps'))
dataset('ch11-st4',
        dict(intro='{who} measured the power output of a model wind turbine at different fan speed settings.', iv=('Wind speed', 'm/s'), xs=[2, 3, 4, 5, 6],
             dv=('Power output', 'mW'), f=lambda x: 0.8 * x ** 3, dp=0, trend='The power output increases rapidly as wind speed increases – much more than in proportion.',
             why='The kinetic energy of the air reaching the blades each second depends on the cube of the wind speed, so doubling the wind speed gives about eight times the power.'))


# =============================================================================================
# ch12 Electricity and Magnetism
# =============================================================================================
R.facts('ch12-st1', F(
    terms=[('series circuit', 'a circuit with only one path for the current'),
           ('parallel circuit', 'a circuit with two or more branches for the current'),
           ('cell', 'a single source of potential difference; a battery is two or more cells'),
           ('switch', 'a component that opens or closes a circuit'),
           ('circuit symbol', 'a standard drawing used to represent a component in a circuit diagram'),
           ('fuse', 'a thin wire that melts if the current is too large, breaking the circuit')],
    facts=[('In a series circuit with two lamps, what happens if one lamp breaks?', 'Both lamps go out', ['The other lamp gets brighter', 'Only the broken lamp goes out', 'Nothing changes'], 'There is only one path.'),
           ('Why are house lights wired in parallel?', 'Each light can be switched on and off independently', ['To make them dimmer', 'To use less wire', 'So all lights go out together'], 'Each has its own branch.'),
           ('What does the circuit symbol of a circle with a cross inside represent?', 'A lamp', ['A cell', 'A resistor', 'A motor'], 'Filament lamp.'),
           ('What happens to the brightness of lamps when more lamps are added in series?', 'They get dimmer', ['They get brighter', 'They stay the same', 'They all go out'], 'Resistance increases.'),
           ('What is the symbol for a cell?', 'A long thin line and a short thick line', ['A circle with a cross', 'A rectangle', 'A circle with a V'], 'The long line is positive.')],
    why=[('Explain why lamps in parallel stay bright when more lamps are added.', 'Each branch receives the full potential difference of the supply, so each lamp has the same pd and current as if it were alone.'),
         ('Explain why Christmas tree lights in series all go out if one bulb fails.', 'There is only one path; a broken filament breaks the circuit, so no current flows through any bulb.'),
         ('Explain why circuit diagrams use standard symbols.', 'Everyone can read them the same way, and they are quicker and clearer to draw than pictures.')],
    contrast=[('a series circuit', 'a parallel circuit', 'A series circuit has one path, so components share the pd and one break stops everything; a parallel circuit has separate branches, each with the full pd, so components work independently.'),
              ('an open switch', 'a closed switch', 'An open switch breaks the circuit so no current flows; a closed switch completes the circuit.')],
    misc=[('Current is used up by each lamp in a series circuit.', 'Current is the same everywhere in a series circuit; energy, not current, is transferred to the lamps.'),
          ('Adding more cells in parallel makes lamps brighter.', 'Identical cells in parallel give the same pd as one cell; they just last longer. Cells in series increase the pd.')],
    evaluate=[('Learning circuits with simulation software is as good as building real circuits.', ['safe, quick, no broken components', 'shows current and pd values clearly'], ['no practice handling real equipment or finding loose connections', 'real components behave less ideally'], 'Simulations are useful for understanding, but students also need hands-on practice.')],
    extended=[('Design a circuit for a model house with two rooms, where each room has a lamp with its own switch, and a main switch that turns everything off. Describe (draw) the circuit and explain your choices.', 'Main switch in series with the cell, before the branches; two parallel branches, each with a lamp and its own switch in series. Parallel: each lamp gets full pd (bright) and can be switched independently; the main switch in the main line breaks the whole circuit. A fuse in the main line adds safety.', 6)],
))


@R.add('ch12-st1', 'C3', (1, 4), 'numerical')
def cells_series(rng, slot):
    n = rng.choice([2, 3, 4, 6])
    v = rng.choice([1.5, 2.0])
    lamps = rng.choice([2, 3])
    return dict(stem=f'{n} cells, each {v:g} V, are connected in series to {lamps} identical lamps in series. Calculate the total pd of the battery and the pd across each lamp.', answer=f'{g(n * v)} V; {g(n * v / lamps)} V each',
                markingKey=f'M1 {n} × {v:g} = {g(n * v)} V; M1 shared equally between {lamps} lamps; A1 {g(n * v / lamps)} V.', marks=3)


inquiry('ch12-st1',
        dict(ctx='how the number of lamps in series affects the brightness of each lamp',
             iv='number of identical lamps in series (1, 2, 3, 4)', dv='brightness of one lamp measured with a light meter (lux) at 10 cm',
             cvs=[('supply voltage', 'higher pd gives brighter lamps'), ('identical lamps', 'different lamps have different resistance'), ('distance of light meter (10 cm)', 'brightness reading depends on distance'), ('darkened room', 'background light')],
             hyp='If more lamps are added in series, then each lamp will be dimmer, because the pd is shared between them and the current decreases.',
             method='Connect one lamp to a 6 V supply; measure the light intensity 10 cm from it with a light meter; add a second identical lamp in series and remeasure the first lamp; continue to four lamps; repeat three times; also measure current with an ammeter.',
             weak=('the light meter picked up light from the other lamps', 'shield the other lamps with card or measure in a box'),
             safety='lamps get hot – do not touch; switch off between readings; use low-voltage supplies only'))
dataset('ch12-st1',
        dict(intro='{who} measured the current from a 6 V supply when different numbers of identical lamps were connected in parallel.', iv=('Number of lamps', ''), xs=[1, 2, 3, 4, 5],
             dv=('Total current', 'A'), f=lambda x: 0.25 * x, dp=2, trend='The total current increases in proportion to the number of lamps in parallel.',
             why='Each lamp branch has the full 6 V and draws the same current, so the total current is the sum of the branch currents.'))

R.facts('ch12-st2', F(
    terms=[('current', 'the rate of flow of charge, measured in amperes (A)'),
           ('potential difference (voltage)', 'the energy transferred per unit charge between two points, measured in volts (V)'),
           ('ammeter', 'a meter connected in series to measure current'),
           ('voltmeter', 'a meter connected in parallel across a component to measure potential difference'),
           ('charge', 'a property of particles such as electrons; flowing charge forms a current'),
           ('ampere (A)', 'the unit of current')],
    facts=[('How is an ammeter connected in a circuit?', 'In series', ['In parallel', 'Across the cell', 'It is not connected'], 'Current flows through it.'),
           ('How is a voltmeter connected?', 'In parallel across the component', ['In series', 'Between two cells only', 'At the end of the circuit'], 'It compares two points.'),
           ('In a parallel circuit, the currents in two branches are 0.3 A and 0.5 A. What is the current from the cell?', '0.8 A', ['0.2 A', '0.4 A', '0.15 A'], 'Branch currents add.'),
           ('In a series circuit, the pd across two lamps is 2 V and 4 V. What is the supply pd?', '6 V', ['2 V', '4 V', '8 V'], 'Pds add in series.'),
           ('What is the unit of potential difference?', 'Volt (V)', ['Ampere (A)', 'Ohm (Ω)', 'Watt (W)'], '1 V = 1 J/C.')],
    why=[('Explain why the current is the same at all points in a series circuit.', 'There is only one path, and charge is not used up, so the same amount of charge passes every point each second.'),
         ('Explain why the potential differences across components in series add up to the supply pd.', 'The energy given to each unit of charge by the supply is all transferred to the components in turn.'),
         ('Explain why an ammeter must have a very low resistance.', 'It is placed in series, so a high resistance would reduce the current it is trying to measure.')],
    contrast=[('current', 'potential difference', 'Current is the rate of flow of charge through a component (A, measured in series); potential difference is the energy transferred per unit charge between two points (V, measured in parallel).'),
              ('an ammeter', 'a voltmeter', 'An ammeter measures current, is connected in series and has very low resistance; a voltmeter measures pd, is connected in parallel and has very high resistance.')],
    misc=[('Current gets used up as it goes round the circuit.', 'Current is the same before and after a component in series; energy is transferred, not charge.'),
          ('Voltage flows through a circuit.', 'Potential difference is between two points; it is current (charge) that flows.')],
    cases=[('Alessandro Volta’s pile (1800)', 'Volta stacked discs of zinc and copper separated by cloth soaked in salt water, making the first battery that produced a steady current.', 'source of potential difference', 'The volt is named after him, and his battery made the study of electric currents possible.')],
    evaluate=[('The water-in-pipes model is a good way to explain current and potential difference.', ['current like flow rate of water, pd like pressure difference – easy to picture'], ['water can leak from pipes, but charge does not leave wires', 'misleading for parallel circuits and for what pd really is'], 'Models such as water pipes help at first, but their limitations should be discussed.')],
    extended=[('In a parallel circuit, a 6 V battery supplies two branches: branch A has one lamp, branch B has two identical lamps in series. Predict the pd across each lamp and compare the currents, explaining your reasoning.', 'Each branch has the full 6 V; lamp in A: 6 V; each lamp in B: 3 V (shared in series). Branch B has twice the resistance so half the current of branch A; total current from the battery = sum of branch currents; lamps in B are dimmer.', 6)],
))


@R.add('ch12-st2', 'C3', (1, 5), 'numerical')
def pd_current(rng, slot):
    k = rng.choice(['par', 'ser', 'charge'] if slot.d >= 2 else ['par', 'ser'])
    if k == 'par':
        a, b = rng.choice([(0.2, 0.3), (0.15, 0.45), (0.6, 0.4), (1.2, 0.8)])
        c = rng.choice([0, 0.1, 0.25])
        tot = a + b + c
        br = f'{a} A, {b} A' + (f' and {c} A' if c else '')
        return dict(stem=f'In a parallel circuit the branch currents are {br}. What current flows from the supply?', answer=f'{g(tot)} A',
                    markingKey=f'M1 currents in parallel branches add: {" + ".join(str(x) for x in (a, b, c) if x)}; A1 {g(tot)} A.', marks=2)
    if k == 'ser':
        V = rng.choice([6, 9, 12])
        v1 = rng.choice([1.5, 2, 3, 4.5])
        v2 = rng.choice([1, 2, 2.5])
        return dict(stem=f'A {V} V battery is connected to three components in series. The pd across the first is {v1:g} V and across the second is {v2:g} V. What is the pd across the third?', answer=f'{g(V - v1 - v2)} V',
                    markingKey=f'M1 pds in series add up to the supply: {V} − {v1:g} − {v2:g}; A1 {g(V - v1 - v2)} V.', marks=2)
    I = rng.choice([0.2, 0.5, 1.5, 2])
    t = rng.choice([10, 30, 60, 120])
    return dict(stem=f'A current of {I:g} A flows through a lamp for {t} s. Calculate the charge that flows (Q = I × t).', answer=f'{g(I * t)} C',
                markingKey=f'M1 Q = {I:g} × {t}; A1 {g(I * t)} C.', marks=2)


inquiry('ch12-st2',
        dict(ctx='how the number of cells in series affects the current through a lamp',
             iv='number of 1.5 V cells in series (1, 2, 3, 4)', dv='current through the lamp measured with an ammeter in series',
             cvs=[('the same lamp', 'lamps differ in resistance'), ('the same wires and connections', 'add resistance'), ('cells all fresh and of the same type', 'old cells give lower pd'), ('switch off between readings', 'lamp heating changes resistance')],
             hyp='If more cells are added, then the current will increase, because the pd across the lamp increases and pushes more charge round per second.',
             method='Build a circuit with one cell, a switch, an ammeter in series and a lamp; connect a voltmeter across the lamp; close the switch and record current and pd; add cells one at a time; repeat three times; plot current against pd.',
             weak=('the ammeter was connected in parallel', 'connect the ammeter in series and the voltmeter in parallel across the lamp'),
             safety='do not exceed the lamp’s rated voltage; lamps get hot'))
dataset('ch12-st2',
        dict(intro='{who} measured the current through a fixed resistor for different potential differences across it.', iv=('Potential difference', 'V'), xs=[1.0, 2.0, 3.0, 4.0, 5.0],
             dv=('Current', 'A'), f=lambda x: 0.1 * x, dp=2, trend='The current increases in direct proportion to the potential difference.',
             why='At constant temperature a resistor has a constant resistance (Ohm’s law), so I = V ÷ R gives a straight line through the origin.'))

R.facts('ch12-st3', F(
    terms=[('resistance', 'how much a component opposes the current, measured in ohms (Ω)'),
           ('ohm (Ω)', 'the unit of resistance'),
           ('Ohm’s law', 'the current through a resistor at constant temperature is directly proportional to the potential difference across it (V = I × R)'),
           ('variable resistor', 'a resistor whose resistance can be changed to control the current'),
           ('thermistor', 'a resistor whose resistance decreases as temperature increases'),
           ('LDR', 'light-dependent resistor; its resistance decreases as light intensity increases')],
    facts=[('What is the resistance of a component with 6 V across it and 2 A through it?', '3 Ω', ['12 Ω', '0.33 Ω', '8 Ω'], 'R = V ÷ I.'),
           ('What happens to the resistance of a wire as it gets longer?', 'It increases', ['It decreases', 'It stays the same', 'It becomes zero'], 'Electrons collide with more ions.'),
           ('What happens to the resistance of an LDR in bright light?', 'It decreases', ['It increases', 'It stays the same', 'It becomes infinite'], 'Used in automatic night lights.'),
           ('Which component would be used in a fire alarm circuit to detect heat?', 'Thermistor', ['LDR', 'Fuse', 'Diode'], 'Resistance falls as it warms.'),
           ('Why does a filament lamp’s resistance increase as it gets brighter?', 'The filament heats up and ions vibrate more, obstructing electrons', ['The current decreases', 'The wire gets shorter', 'The lamp loses charge'], 'Its I–V graph curves.')],
    why=[('Explain why thicker wires are used for high-current appliances such as cookers.', 'Thicker wires have lower resistance, so less energy is wasted as heat and the wire does not overheat.'),
         ('Explain why a dimmer switch can control the brightness of a lamp.', 'It is a variable resistor; increasing its resistance decreases the current, so the lamp is dimmer.'),
         ('Explain why the I–V graph for a filament lamp is a curve, not a straight line.', 'As current increases the filament gets hotter and its resistance increases, so current rises less for each extra volt.')],
    contrast=[('a fixed resistor', 'a filament lamp', 'A fixed resistor has constant resistance at constant temperature, giving a straight-line I–V graph; a filament lamp’s resistance increases as it heats up, giving a curved graph.'),
              ('a thermistor', 'an LDR', 'A thermistor’s resistance falls as temperature rises; an LDR’s resistance falls as light intensity increases.')],
    misc=[('Resistance is the same as current.', 'Resistance opposes current; for a given pd, higher resistance means lower current.'),
          ('All components obey Ohm’s law.', 'Only ohmic conductors such as fixed resistors at constant temperature do; filament lamps, diodes and thermistors do not.')],
    cases=[('Superconductors and MRI scanners', 'Some materials lose all resistance when cooled below a critical temperature; MRI scanners use superconducting coils cooled by liquid helium to make strong magnetic fields.', 'resistance in technology', 'Zero resistance means huge currents with no heating, but cooling is expensive.')],
    evaluate=[('Research into room-temperature superconductors should be a top priority for funding.', ['would remove energy losses in power lines', 'cheaper MRI, faster computers, maglev trains'], ['may never be achieved; many claims have been false', 'money could go to proven technologies like renewables'], 'It is worth funding as long-term research, but alongside proven energy solutions.')],
    extended=[('Describe how to investigate how the length of a wire affects its resistance, including the circuit, measurements, calculation and how to make it a fair test.', 'Circuit: cell, ammeter in series with a length of constantan wire on a metre rule (crocodile clips), voltmeter across the wire. Vary length 10–100 cm; record I and V; R = V ÷ I; repeat; keep the same wire (material, thickness), low current and switch off between readings so temperature stays constant; plot R against length – expect straight line through origin.', 6)],
))


@R.add('ch12-st3', 'C3', (1, 5), 'numerical')
def ohms_law(rng, slot):
    k = rng.choice(['R', 'V', 'I'])
    R_ = rng.choice([2, 4, 5, 10, 12, 20, 47, 100])
    I = rng.choice([0.05, 0.1, 0.2, 0.25, 0.5, 1.5, 2])
    V = R_ * I
    if k == 'R':
        return dict(stem=f'A pd of {g(V)} V across a resistor produces a current of {g(I)} A. Calculate its resistance.', answer=f'{R_} Ω', markingKey=f'M1 R = V ÷ I = {g(V)} ÷ {g(I)}; A1 {R_} Ω.', marks=2)
    if k == 'V':
        return dict(stem=f'A current of {g(I)} A flows through a {R_} Ω resistor. Calculate the pd across it.', answer=f'{g(V)} V', markingKey=f'M1 V = I × R = {g(I)} × {R_}; A1 {g(V)} V.', marks=2)
    return dict(stem=f'A {R_} Ω resistor is connected to a {g(V)} V supply. Calculate the current.', answer=f'{g(I)} A', markingKey=f'M1 I = V ÷ R = {g(V)} ÷ {R_}; A1 {g(I)} A.', marks=2)


inquiry('ch12-st3',
        dict(ctx='how the length of a constantan wire affects its resistance',
             iv='length of wire between the crocodile clips (20, 40, 60, 80, 100 cm)', dv='resistance calculated from R = V ÷ I',
             cvs=[('diameter of the wire', 'thicker wire has lower resistance'), ('material (constantan)', 'materials differ in resistivity'), ('temperature (low current, switch off between readings)', 'heating increases resistance'), ('the same meters', 'calibration differences')],
             hyp='If the length doubles, then the resistance will double, because electrons collide with twice as many ions along the longer wire.',
             method='Tape the wire along a metre rule; connect a cell, switch and ammeter in series and a voltmeter across the wire; set the clips 20 cm apart; close the switch briefly and record I and V; repeat for each length; repeat three times; calculate R and plot against length.',
             weak=('the wire got warm because the switch was left on', 'close the switch only while taking readings and use a low current'),
             safety='the wire can get hot – keep currents low and do not touch it while current flows'))
dataset('ch12-st3',
        dict(intro='{who} measured the resistance of a thermistor at different temperatures in a water bath (three readings each).', iv=('Temperature', '°C'), xs=[10, 20, 30, 40, 50],
             dv=('Resistance', 'Ω'), f=lambda x: 2000 * math.exp(-0.04 * x), dp=0, trend='The resistance of the thermistor decreases as temperature increases, falling by a smaller amount each 10 °C.',
             why='In a thermistor, higher temperature releases more charge carriers, so it conducts more easily – its resistance falls.'))

R.facts('ch12-st4', F(
    terms=[('power', 'the rate of energy transfer, measured in watts (W): P = V × I'),
           ('kilowatt-hour (kWh)', 'the energy transferred by a 1 kW appliance in 1 hour; the unit on electricity bills'),
           ('earth wire', 'the green-and-yellow wire that carries current safely to earth if a metal case becomes live'),
           ('live wire', 'the brown wire that carries the alternating pd from the supply'),
           ('neutral wire', 'the blue wire that completes the circuit'),
           ('circuit breaker', 'a switch that automatically cuts off the current if it becomes too large')],
    facts=[('What is the colour of the earth wire in a UK-style plug?', 'Green and yellow', ['Brown', 'Blue', 'Red'], 'Brown is live, blue is neutral.'),
           ('What is the power of a kettle using 230 V and 10 A?', '2300 W', ['23 W', '240 W', '0.043 W'], 'P = V × I.'),
           ('Why is a fuse placed in the live wire?', 'To disconnect the appliance from the high pd if the current is too large', ['To make the appliance brighter', 'To save energy', 'To carry current to earth'], 'Prevents fires.'),
           ('What does a 3 kW heater used for 2 hours transfer?', '6 kWh', ['1.5 kWh', '5 kWh', '3 kWh'], 'kW × h.'),
           ('Why do appliances with plastic cases not need an earth wire?', 'They are double insulated – the case cannot become live', ['Plastic conducts', 'They use less current', 'They run on batteries'], 'Symbol: a square inside a square.')],
    why=[('Explain how the earth wire and fuse protect a person if a live wire touches a metal kettle case.', 'A large current flows from the live wire through the case to earth; this melts the fuse, disconnecting the live wire, so the case is no longer dangerous.'),
         ('Explain why the fuse rating should be just above the normal current of the appliance.', 'It must not blow in normal use, but must melt quickly if a fault causes a larger current.'),
         ('Explain why electricity bills use kWh rather than joules.', 'Joules are tiny; a typical home uses billions of joules a month, so kWh gives manageable numbers.')],
    contrast=[('a fuse', 'a circuit breaker', 'A fuse is a thin wire that melts and must be replaced; a circuit breaker is an automatic switch that trips faster and can be reset.'),
              ('power', 'energy', 'Power is the rate of transfer (W); energy is the total transferred (J or kWh) = power × time.')],
    misc=[('A higher-power appliance always costs more to run.', 'Cost depends on power and how long it is used; a 2 kW kettle used for 3 minutes costs less than a 100 W TV used all evening.'),
          ('The neutral wire is always completely safe to touch.', 'Faults can make the neutral wire carry a dangerous pd; never touch any wires in a live circuit.')],
    cases=[('Residual current devices (RCDs)', 'RCDs compare current in live and neutral wires and switch off within about 30 ms if there is a difference, such as current leaking through a person.', 'electrical safety', 'Required in new homes in many countries, they prevent many electrocutions, especially with outdoor equipment.')],
    evaluate=[('Smart meters help households save energy.', ['show real-time energy use and cost, encouraging changes', 'accurate bills without estimates'], ['savings are often small once novelty wears off', 'privacy concerns about usage data'], 'Smart meters can help, but savings depend on people changing their habits.')],
    extended=[('A family uses a 2.5 kW kettle for 30 minutes a day, a 0.1 kW TV for 5 hours a day and a 9 W LED lamp for 6 hours a day. Calculate the total energy in kWh per day and the weekly cost at 30p per kWh, and suggest which change would save the most.', 'Kettle 2.5 × 0.5 = 1.25 kWh; TV 0.1 × 5 = 0.5 kWh; lamp 0.009 × 6 = 0.054 kWh; total ≈ 1.80 kWh/day; week ≈ 12.6 kWh; cost ≈ £3.79. Biggest saving: boil only the water needed (kettle is largest use).', 6)],
))


@R.add('ch12-st4', 'C3', (1, 5), 'numerical')
def power_cost(rng, slot):
    k = rng.choice(['P', 'kwh', 'cost', 'fuse'] if slot.d >= 2 else ['P', 'kwh'])
    dev, P = rng.choice([('kettle', 2.4), ('hair dryer', 1.8), ('microwave', 0.8), ('electric heater', 3.0), ('TV', 0.12), ('washing machine', 2.0)])
    if k == 'P':
        V = 230
        I = round(P * 1000 / V, 1)
        return dict(stem=f'A {dev} draws a current of {I} A from the 230 V mains. Calculate its power.', answer=f'{g(V * I)} W', markingKey=f'M1 P = V × I = 230 × {I}; A1 {g(V * I)} W.', marks=2)
    t = rng.choice([0.5, 1.5, 2, 3, 4])
    E = P * t
    if k == 'kwh':
        return dict(stem=f'A {g(P)} kW {dev} is used for {g(t)} hours. Calculate the energy transferred in kWh.', answer=f'{g(E)} kWh', markingKey=f'M1 E = P × t = {g(P)} × {g(t)}; A1 {g(E)} kWh.', marks=2)
    if k == 'cost':
        c = rng.choice([15, 20, 25, 30, 34])
        return dict(stem=f'A {g(P)} kW {dev} is used for {g(t)} hours. Electricity costs {c}p per kWh. Calculate the cost.', answer=f'{g(E * c)}p',
                    markingKey=f'M1 energy = {g(P)} × {g(t)} = {g(E)} kWh; M1 × {c}p; A1 {g(E * c)}p.', marks=3)
    I = P * 1000 / 230
    fuse = next(f for f in [3, 5, 13] if f > I) if I < 13 else 13
    return dict(stem=f'A {g(P * 1000)} W {dev} runs on 230 V. Calculate the normal current and choose a fuse from 3 A, 5 A and 13 A.', answer=f'{g(I)} A; {fuse} A fuse',
                markingKey=f'M1 I = P ÷ V = {g(P * 1000)} ÷ 230; A1 {g(I)} A; B1 {fuse} A – the smallest rating above the normal current.', marks=3)


inquiry('ch12-st4',
        dict(ctx='how the power rating of an electric kettle affects the time it takes to boil 1 litre of water',
             iv='power rating of the kettle (1.0, 1.5, 2.0, 2.5, 3.0 kW)', dv='time for 1 dm³ of water to reach boiling (switch-off)',
             cvs=[('volume of water (1 dm³)', 'more water takes longer'), ('starting temperature of water', 'colder water takes longer'), ('kettle cooled between trials', 'a warm kettle needs less energy'), ('lid closed', 'reduces heat loss')],
             hyp='If the power rating increases, then the time to boil will decrease, because energy is transferred to the water faster (E = P × t).',
             method='Fill each kettle with 1 dm³ water from the same tap (check temperature); switch on and time until it switches off; empty and allow to cool to room temperature; repeat three times; plot time against power.',
             weak=('the kettles were different shapes and materials', 'use one variable-power kettle or note that shape/material is an uncontrolled variable'),
             safety='steam and boiling water scald – keep away from the spout; dry hands near mains sockets'))
dataset('ch12-st4',
        dict(intro='{who} used a plug-in energy monitor to measure the energy used by a fan heater running for different times.', iv=('Time', 'h'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Energy used', 'kWh'), f=lambda x: 2.0 * x, dp=2, trend='The energy used increases in direct proportion to the running time.',
             why='The heater transfers energy at a constant rate (power about 2 kW), so energy = power × time.'))

R.facts('ch12-st5', F(
    terms=[('static electricity', 'electric charge that builds up on an insulator and does not flow'),
           ('electron', 'the negatively charged particle that moves when objects are charged by friction'),
           ('magnetic field', 'the region around a magnet where a magnetic material or another magnet feels a force'),
           ('magnetic pole', 'the end of a magnet where the magnetic force is strongest (north or south)'),
           ('electromagnet', 'a coil of wire, usually around an iron core, that becomes magnetic when current flows'),
           ('magnetic material', 'a material attracted by a magnet: iron, nickel, cobalt and steel')],
    facts=[('What happens when two north poles are brought together?', 'They repel', ['They attract', 'Nothing', 'They become south poles'], 'Like poles repel.'),
           ('When a balloon is rubbed on hair, it becomes negatively charged. Why?', 'Electrons move from the hair to the balloon', ['Protons move to the balloon', 'Electrons move from the balloon to the hair', 'Air adds charge'], 'Only electrons move.'),
           ('Which metal is magnetic?', 'Nickel', ['Copper', 'Aluminium', 'Gold'], 'Iron, nickel and cobalt.'),
           ('How can an electromagnet be made stronger?', 'Increase the current or the number of turns', ['Use a copper core', 'Reduce the current', 'Use fewer turns'], 'An iron core also helps.'),
           ('What happens when two negatively charged objects are brought together?', 'They repel', ['They attract', 'They become neutral', 'They stick together'], 'Like charges repel.'),
           ('In which direction do magnetic field lines point outside a bar magnet?', 'From north to south', ['From south to north', 'Towards both poles', 'Away from both poles'], 'Shown by a plotting compass.')],
    why=[('Explain why you sometimes get a small electric shock from a car door after a journey.', 'Friction between your clothes and the seat transfers electrons, charging you; when you touch the metal door the charge flows suddenly through you to earth.'),
         ('Explain why electromagnets are used in scrapyards instead of permanent magnets.', 'They can be switched off to drop the scrap metal, and their strength can be changed by changing the current.'),
         ('Explain why a charged balloon sticks to a neutral wall.', 'The negative balloon repels electrons in the wall surface away, leaving the surface slightly positive, so the balloon is attracted.')],
    contrast=[('a permanent magnet', 'an electromagnet', 'A permanent magnet is always magnetic and has a fixed strength; an electromagnet is only magnetic when current flows and its strength can be changed.'),
              ('static electricity', 'current electricity', 'Static electricity is charge built up and held on an insulator; current electricity is a continuous flow of charge through a conductor.')],
    misc=[('All metals are magnetic.', 'Only iron, nickel, cobalt and some alloys such as steel are magnetic; copper, aluminium and gold are not.'),
          ('Rubbing gives objects positive charge by adding protons.', 'Only electrons move when objects are charged by friction; losing electrons leaves an object positive.')],
    cases=[('Maglev trains', 'Maglev trains in Shanghai and Japan use powerful electromagnets to lift the train above the track and push it forward, reaching over 400 km/h.', 'magnetism in transport', 'No wheel friction allows very high speeds, but the tracks are very expensive to build.')],
    evaluate=[('Maglev trains should replace high-speed rail.', ['faster, quieter, less wear and maintenance', 'no wheel friction'], ['very expensive dedicated tracks', 'cannot use existing railway network'], 'Maglev suits some busy routes between big cities, but conventional high-speed rail is usually more practical.')],
    extended=[('Plan an investigation into how the number of turns on an electromagnet affects its strength, and explain the expected results.', 'Wind 10, 20, 30, 40, 50 turns of insulated wire round the same iron nail; connect to a low-voltage supply with an ammeter and keep the current constant (variable resistor); count paper clips picked up (or measure force on a newton meter); repeat three times; switch off between trials (wire heats). Expect more turns → more clips, because each turn adds to the magnetic field.', 6)],
))
inquiry('ch12-st5',
        dict(ctx='how the current in an electromagnet affects the number of paper clips it can hold',
             iv='current through the coil (0.5, 1.0, 1.5, 2.0, 2.5 A)', dv='number of paper clips picked up',
             cvs=[('number of turns (30)', 'more turns make it stronger'), ('the same iron nail core', 'core material affects strength'), ('the same size paper clips', 'mass of clips varies'), ('switch off between readings', 'coil heating changes resistance and could burn')],
             hyp='If the current increases, then more paper clips will be picked up, because a larger current produces a stronger magnetic field.',
             method='Wind 30 turns of insulated wire around an iron nail; connect to a variable power supply, ammeter and variable resistor; set the current to 0.5 A; dip the nail into a tray of paper clips and lift; count clips held; switch off; repeat for each current three times; plot clips against current.',
             weak=('clips stayed slightly magnetised and stuck together', 'use fresh clips each trial or tap them apart; demagnetise the nail between trials'),
             safety='the coil can get hot – switch off between readings and do not exceed 3 A'))
dataset('ch12-st5',
        dict(intro='{who} measured the force between two magnets at different separations using a balance (three readings each).', iv=('Separation', 'cm'), xs=[1, 2, 3, 4, 5],
             dv=('Force', 'N'), f=lambda x: 2.4 / x ** 2, dp=2, trend='The force decreases rapidly as the separation increases – doubling the distance reduces the force to about a quarter.',
             why='The magnetic field gets weaker with distance from the magnets, so the force between them falls sharply.'))
