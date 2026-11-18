"""Cambridge IGCSE Biology 0610 Extended (2026-28), CUP coursebook chapters 11-20 (grade 10).

Chapter order 1-10 here = coursebook 11 (respiration and gas exchange) ... 20 (biotechnology and GM).
Uses the knowledge-pack builders and the Alternative-to-Practical engine from g9_biology.py.
"""
import math
from ._lib import compose, sf, sci, person, city  # noqa: F401
from .g9_biology import cap, low, fx, Q, MQ, NQ, T, facts, mcqs, explain, shorts, longs, myths, pct, add_practical, trend_text  # noqa: F401

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}


def big(x):
    return f'{int(round(x)):,}'.replace(',', ' ')

# ===================================================================== 1 Respiration and gas exchange
USES = ['muscle contraction', 'protein synthesis', 'cell division', 'active transport', 'growth', 'the passage of nerve impulses', 'the maintenance of a constant body temperature']
t = T('Aerobic respiration: uses of energy and word and balanced equations', 'aerobic respiration', 'uses of energy')
facts(t, [('respiration', 'the chemical reactions in cells that break down nutrient molecules and release energy for metabolism'),
          ('aerobic respiration', 'the chemical reactions in cells that use oxygen to break down nutrient molecules to release energy'),
          ('mitochondria', 'the organelles in which most of the reactions of aerobic respiration take place'), ('metabolism', 'all the chemical reactions that take place in an organism'),
          ('respirometer', 'apparatus used to measure the rate of respiration of small organisms by their oxygen uptake')])
mcqs(t, [('Which is the balanced equation for aerobic respiration?', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 'Glucose + oxygen → carbon dioxide + water (energy released).', ['6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'C₆H₁₂O₆ + O₂ → CO₂ + H₂O']),
         ('Which process in the body does not use energy from respiration?', 'Diffusion of oxygen into the blood', 'Diffusion is passive; muscle contraction, protein synthesis and active transport all need energy.', ['Muscle contraction', 'Protein synthesis', 'Active transport']),
         ('Where in the cell does aerobic respiration mainly take place?', 'Mitochondria', 'Most reactions of aerobic respiration occur in mitochondria.', ['Nucleus', 'Ribosomes', 'Cell membrane'])])
shorts(t, [('Write the word equation for aerobic respiration.', 'glucose + oxygen → carbon dioxide + water', 'reactants [1]; products [1] [2]'), ('State four uses of energy released by respiration in the human body.', ', '.join(USES[:4]) + '.', 'any four [2]; two or three [1] [2]')])
explain(t, [('Explain why germinating seeds release heat.', 'They respire rapidly to provide energy for growth; some energy released by respiration is lost as heat.', 'respiration [1]; energy released as heat [1] [2]'),
            ('Explain why a respirometer containing germinating seeds needs soda lime.', 'Soda lime absorbs carbon dioxide released, so any change in volume is due to oxygen uptake only.', 'absorbs CO₂ [1]; volume change = oxygen used [1] [2]'),
            ('Explain why the control in a vacuum-flask experiment uses boiled seeds washed in disinfectant.', 'Boiled seeds are dead and cannot respire; disinfectant kills microorganisms that would respire and release heat, so any temperature rise in the test flask is due to the seeds.', 'dead seeds [1]; microorganisms killed [1] [2]'),
            ('Explain why cells in the body need a continuous supply of oxygen and glucose.', 'Aerobic respiration needs both to release energy continuously for processes such as muscle contraction, active transport and protein synthesis.', 'reactants of respiration [1]; continuous energy needs [1] [2]'),
            ('Explain why respiration is described as a series of enzyme-controlled reactions.', 'Each step is catalysed by a specific enzyme, so the rate depends on temperature and pH like other enzyme reactions.', 'enzymes catalyse steps [1]; affected by temperature / pH [1] [2]')])
myths(t, [('Respiration makes energy.', 'Respiration releases energy from nutrient molecules; energy cannot be made.'), ('Only animals respire; plants photosynthesise instead.', 'All living cells, including plant cells, respire continuously.'),
           ('Respiration happens in the lungs.', 'Respiration happens in every living cell; gas exchange happens in the lungs.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def resp_moles(r, D):
    n = r.choice([2, 3, 4, 5, 6, 8, 10])
    if D == 1:
        return NQ(r, f'Using C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O, how many molecules of oxygen are needed to respire {fx(n)} molecules of glucose completely?', 6 * n, [n, 2 * n, 12 * n, 3 * n], '', f'1 glucose : 6 O₂, so {fx(n)} × 6 = {fx(6 * n)}.', f=lambda v: fx(v, 2))
    m = r.choice([18, 36, 90, 180])
    st = f'Use the balanced equation for aerobic respiration, C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O. (a) State the number of molecules of carbon dioxide produced from {fx(n)} molecules of glucose. (b) The Mr of glucose is 180 and of CO₂ is 44. Calculate the mass of carbon dioxide released when {m} g of glucose is respired.'
    co2 = m / 180 * 6 * 44
    return Q(st, f'(a) {fx(6 * n)} (b) {fx(co2, 1)} g', f'(a) {fx(6 * n)} [1] (b) {m} ÷ 180 = {fx(m / 180, 3)} mol glucose [1]; × 6 × 44 = {fx(co2, 1)} g [1] [3]', 'short', 3)


@t.add('C3', (1, 2, 3), 'short')
def resp_use(r, D):
    cases = [('a sperm cell swimming towards an egg', 'muscle contraction / movement of the flagellum'), ('a root hair cell absorbing nitrate ions from dilute soil water', 'active transport'),
             ('a growing child', 'growth / cell division / protein synthesis'), ('a bird keeping warm on a cold night', 'maintaining a constant body temperature'),
             ('a pancreas cell making insulin', 'protein synthesis'), ('a runner sprinting', 'muscle contraction'), ('a neurone carrying impulses', 'passage of nerve impulses'),
             ('cells in the skin dividing to repair a cut', 'cell division')]
    x, u = r.choice(cases)
    if D <= 2:
        return MQ(r, f'For which use of energy from respiration is {x} an example?', u, [c[1] for c in cases if c[1] != u], f'{cap(x)}: energy used for {u}.')
    x2, u2 = r.choice([c for c in cases if c[1] != u])
    return Q(f'State how energy from respiration is used in each case: (i) {x} (ii) {x2}.', f'(i) {u} (ii) {u2}', f'(i) {u} [1]; (ii) {u2} [1] [2]', 'short', 2)


RESPIRO = {'setup': lambda r, p: f'{p} set up a respirometer containing germinating peas and soda lime in a water bath, and measured the distance moved by a drop of coloured liquid in a capillary tube in 10 minutes at different temperatures.',
           'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 15, 20, 25, 30], [15, 20, 25, 30, 35], [5, 10, 20, 30, 40]]),
           'dv': ('distance moved by liquid', 'mm'), 'y': lambda x, k: k * 4 * 2 ** (x / 10), 'dp': 0,
           'controls': ['mass / number of peas', 'mass of soda lime', 'time allowed', 'diameter of capillary tube', 'time allowed to equilibrate'],
           'why': ('As temperature increases, the enzymes controlling respiration work faster (more kinetic energy, more collisions), so more oxygen is used; CO₂ is absorbed by soda lime so the volume of gas falls and the liquid moves further.', 'enzymes / kinetic energy [1]; more oxygen used [1]; CO₂ absorbed so gas volume falls [1] [3]'),
           'improve': ['use a syringe to reset the liquid position between readings', 'leave the apparatus to equilibrate in the water bath for 5 minutes before each reading'],
           'control': 'Use a tube with an equal volume of glass beads (or boiled peas) instead of live peas; it shows that changes in volume are caused by respiring peas, not by temperature or pressure changes.',
           'extra': [lambda r, d: ('The capillary tube has a cross-sectional area of 0.8 mm². Calculate the volume of oxygen used per minute at the highest temperature.', f'{fx(d["means"][-1] * 0.8 / 10, 2)} mm³/min', f'volume = {fx(d["means"][-1], 2)} × 0.8 = {fx(d["means"][-1] * 0.8, 2)} mm³ [1]; ÷ 10 = {fx(d["means"][-1] * 0.8 / 10, 2)} mm³/min [1] [2]'),
                     lambda r, d: ('Explain why the liquid moves towards the peas.', 'The peas take in oxygen, and the carbon dioxide they release is absorbed by soda lime, so the volume and pressure of gas in the tube fall.', 'O₂ taken in [1]; CO₂ absorbed / pressure falls [1] [2]')]}
add_practical(t, RESPIRO, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (3, 4, 5), 'multi_step')
def flask_case(r, D):
    t0 = 20.0
    rise = round(r.uniform(4, 11), 1)
    days = r.choice([2, 3, 4])
    intro = f'{person(r)} placed germinating mung beans in vacuum flask A and boiled, disinfected mung beans in flask B. Both started at {fx(t0)} °C. After {days} days, flask A was at {fx(t0 + rise)} °C and flask B was still at {fx(t0)} °C.'
    parts = [lambda r: ('Calculate the mean rate of temperature rise in flask A in °C per day.', f'{fx(rise / days, 2)} °C/day', f'{fx(rise)} ÷ {days} [1] = {fx(rise / days, 2)} °C/day [1] [2]'),
             lambda r: ('Explain the temperature rise in flask A.', 'The germinating beans respire aerobically, releasing energy; some energy is released as heat, and the vacuum flask reduces heat loss.', 'respiration [1]; heat released [1]; insulation [1] [3]'),
             lambda r: ('Explain why the beans in flask B were boiled and washed in disinfectant.', 'Boiling kills the beans (no respiration); disinfectant kills microorganisms, which would respire and release heat.', '[2]'),
             lambda r: ('Explain why the flasks were plugged with cotton wool rather than sealed with a rubber bung.', 'Cotton wool lets oxygen in for aerobic respiration and carbon dioxide out, while still reducing heat loss.', '[2]'),
             lambda r: ('Write the balanced equation for aerobic respiration.', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe aerobic respiration and explain how the energy released is used in the human body.', 'Glucose + oxygen → carbon dioxide + water in mitochondria, catalysed by enzymes, releasing energy. Uses: muscle contraction, protein synthesis, cell division, active transport, growth, nerve impulses, maintaining body temperature.',
           'equation [2]; mitochondria / enzymes [1]; three uses [3] [6]')])
t11a = t

t = T('Anaerobic respiration in muscles and yeast; oxygen debt and lactic acid', 'anaerobic respiration', 'oxygen debt', 'lactic acid')
facts(t, [('anaerobic respiration', 'the chemical reactions in cells that break down nutrient molecules to release energy without using oxygen'), ('lactic acid', 'the product of anaerobic respiration in muscles'),
          ('oxygen debt', 'the extra oxygen needed after exercise to break down the lactic acid built up during anaerobic respiration'), ('fermentation', 'anaerobic respiration in yeast, producing ethanol and carbon dioxide'),
          ('ethanol', 'the alcohol produced by anaerobic respiration in yeast')])
mcqs(t, [('What are the products of anaerobic respiration in yeast?', 'Ethanol and carbon dioxide', 'Glucose → ethanol + carbon dioxide.', ['Lactic acid only', 'Carbon dioxide and water', 'Lactic acid and carbon dioxide']),
         ('Why does anaerobic respiration release less energy than aerobic respiration per glucose molecule?', 'Glucose is only partly broken down', 'Lactic acid / ethanol still contain much chemical energy.', ['It happens faster', 'It uses more oxygen', 'It happens in mitochondria']),
         ('Which is the balanced equation for anaerobic respiration in yeast?', 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'Glucose → 2 ethanol + 2 carbon dioxide.', ['C₆H₁₂O₆ → 2C₃H₆O₃', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 'C₆H₁₂O₆ → 6CO₂ + 6H₂O'])])
shorts(t, [('Write the word equation for anaerobic respiration in muscles.', 'glucose → lactic acid', '[1]'), ('State two ways in which anaerobic respiration differs from aerobic respiration.', 'No oxygen used; less energy released per glucose; different products (lactic acid or ethanol + CO₂, no water).', 'any two [2]')])
explain(t, [('Explain why a sprinter continues to breathe heavily after a race.', 'During the sprint muscles respired anaerobically, producing lactic acid; extra oxygen (the oxygen debt) is needed to break down the lactic acid in the liver, so heart and breathing rates stay high.', 'anaerobic during race [1]; lactic acid [1]; oxygen debt repaid / lactic acid broken down [1] [3]'),
            ('Explain why muscles become fatigued (painful) during long vigorous exercise.', 'Not enough oxygen reaches muscles, so they respire anaerobically; lactic acid builds up, causing fatigue / cramp.', 'insufficient oxygen [1]; lactic acid build-up [1] [2]'),
            ('Explain how lactic acid is removed after exercise.', 'It diffuses into the blood and is carried to the liver, where it is broken down using oxygen (aerobic respiration).', 'blood transport to liver [1]; broken down with oxygen [1] [2]'),
            ('Explain why yeast is used in bread making.', 'Yeast respires anaerobically in the dough, producing carbon dioxide gas which forms bubbles and makes the dough rise; ethanol evaporates during baking.', 'CO₂ produced [1]; dough rises [1] [2]')])
myths(t, [('Anaerobic respiration produces more energy because it is faster.', 'Anaerobic respiration releases much less energy per glucose molecule than aerobic respiration.'), ('Humans produce alcohol during anaerobic respiration.', 'Human muscles produce lactic acid; yeast produces ethanol.')])

YEAST = {'setup': lambda r, p: f'{p} mixed yeast with sugar solution at different temperatures and counted the bubbles of carbon dioxide released through a delivery tube in 2 minutes.',
         'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[15, 25, 35, 45, 55], [20, 30, 40, 50, 60], [10, 20, 30, 40, 50]]),
         'dv': ('number of bubbles', 'bubbles in 2 min'), 'y': lambda x, k: max(1, k * 40 * math.exp(-((x - 37) ** 2) / 180)), 'dp': 0, 'noise': 0.05,
         'controls': ['mass of yeast', 'volume and concentration of sugar solution', 'type of sugar', 'time allowed to equilibrate'],
         'why': ('Up to about 35–40 °C the enzymes in yeast respiration work faster (more kinetic energy and collisions), so more CO₂ is released; above that the enzymes are denatured and the rate falls.', 'faster enzyme activity [1]; optimum [1]; denaturation above optimum [1] [3]'),
         'improve': ['collect the gas in a gas syringe or measuring cylinder to measure volume', 'add a layer of oil over the mixture to keep it anaerobic'],
         'control': 'Use boiled yeast with sugar solution; no bubbles should be produced, showing that living yeast causes the gas production.',
         'extra': [lambda r, d: ('Describe a test to show that the gas is carbon dioxide.', 'Bubble it through limewater, which turns milky / cloudy.', '[2]')]}
add_practical(t, YEAST, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'numerical')
def lactate(r, D):
    rest = round(r.uniform(0.8, 1.5), 1)
    peak = round(r.uniform(8, 14), 1)
    rec = r.choice([20, 30, 40, 60])
    if D == 1:
        return NQ(r, f'Blood lactic acid rose from {rest} mmol/dm³ at rest to {peak} mmol/dm³ after exercise. By how much did it increase?', peak - rest, [peak + rest, peak, rest, peak / rest], ' mmol/dm³', f'{peak} − {rest} = {fx(peak - rest, 1)}.', f=lambda v: fx(v, 1))
    st = f'An athlete in {city(r)} had a blood lactic acid concentration of {rest} mmol/dm³ at rest and {peak} mmol/dm³ immediately after a 400 m race. It took {rec} minutes to return to the resting level. (a) Calculate the percentage increase. (b) Explain why lactic acid concentration increased during the race.'
    ans = f'(a) {fx(pct(rest, peak), 0)}% (b) Oxygen could not be delivered fast enough, so muscles respired anaerobically, producing lactic acid.'
    key = f'(a) ({peak} − {rest}) ÷ {rest} × 100 = {fx(pct(rest, peak), 0)}% [2] (b) insufficient oxygen [1]; anaerobic respiration produces lactic acid [1]'
    m = 4
    if D >= 3:
        st += f' (c) Calculate the mean rate of fall of lactic acid during recovery. (d) Explain how it is removed.'
        ans += f' (c) {fx((peak - rest) / rec, 3)} mmol/dm³ per min (d) Carried in blood to the liver and broken down using oxygen (oxygen debt).'
        key += f' (c) ({peak} − {rest}) ÷ {rec} = {fx((peak - rest) / rec, 3)} [1] (d) liver [1]; aerobic breakdown / oxygen debt [1]'
        m = 7
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def anaer_case(r, D):
    intro = f'A baker in {city(r)} mixes yeast, flour, sugar and warm water to make dough, then leaves it in a warm place for an hour before baking.'
    parts = [lambda r: ('Write the word equation for anaerobic respiration in yeast.', 'glucose → ethanol + carbon dioxide', '[2]'),
             lambda r: ('Explain why the dough rises.', 'Yeast respires anaerobically, producing carbon dioxide gas that is trapped as bubbles in the dough.', '[2]'),
             lambda r: ('Explain why the dough rises more slowly in a cold room.', 'Respiration is controlled by enzymes, which work more slowly at low temperature (less kinetic energy).', '[2]'),
             lambda r: ('Suggest what happens to the ethanol during baking.', 'It evaporates in the heat of the oven.', '[1]'),
             lambda r: ('Compare anaerobic respiration in yeast and in human muscle.', 'Both release less energy than aerobic and use no oxygen; yeast produces ethanol and CO₂, muscle produces lactic acid only.', 'similarity [1]; difference in products [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare aerobic and anaerobic respiration in humans, and explain the oxygen debt.', 'Aerobic: uses oxygen, glucose → CO₂ + water, much energy, mitochondria. Anaerobic: no oxygen, glucose → lactic acid, little energy, in cytoplasm, used in vigorous exercise. Oxygen debt: extra oxygen needed after exercise to remove lactic acid in the liver; continued fast heart and breathing rates.',
           'two comparisons [2]; equations [1]; oxygen debt defined [1]; lactic acid to liver [1]; elevated heart / breathing [1] [6]')])
t11b = t

AIR = {'oxygen': (21, 16), 'carbon dioxide': (0.04, 4), 'nitrogen': (78, 78), 'water vapour': ('variable', 'saturated')}
t = T('Gas exchange surfaces and structure of the breathing system', 'gas exchange surfaces', 'structure of the breathing system')
facts(t, [('alveolus', 'a tiny air sac in the lungs where gas exchange takes place'), ('trachea', 'the windpipe, supported by rings of cartilage, carrying air to the bronchi'),
          ('bronchus', 'one of two tubes branching from the trachea into each lung'), ('bronchiole', 'a small branching tube in the lung ending in alveoli'),
          ('gas exchange surface', 'a surface where oxygen enters and carbon dioxide leaves the blood, adapted to make diffusion fast'), ('larynx', 'the voice box at the top of the trachea')])
mcqs(t, [('Why is the trachea supported by rings of cartilage?', 'To keep it open so air can flow', 'Cartilage prevents collapse when pressure falls during inhalation.', ['To make mucus', 'To carry out gas exchange', 'To contract and pump air']),
         ('Which feature of alveoli increases the rate of gas exchange?', 'A very large total surface area', 'Large surface area, thin walls, good blood supply and ventilation all help.', ['Thick walls', 'A small blood supply', 'Few capillaries']),
         ('What percentage of exhaled air is carbon dioxide, approximately?', '4%', 'Inhaled 0.04%; exhaled about 4%.', ['0.04%', '16%', '21%'])])
shorts(t, [('State four features of gas exchange surfaces in animals.', 'Large surface area; thin surface (short distance); good blood supply; good ventilation with air.', 'four [2]; two or three [1] [2]'), ('Name, in order, the structures that air passes through from the nose to the alveoli.', 'Nasal cavity, larynx, trachea, bronchus, bronchiole, alveolus.', '[2]')])
explain(t, [('Explain why exhaled air contains less oxygen and more carbon dioxide than inhaled air.', 'Oxygen diffuses from alveoli into the blood to be used in respiration; carbon dioxide produced by respiration diffuses from the blood into the alveoli.', 'oxygen absorbed for respiration [1]; CO₂ released from respiration [1] [2]'),
            ('Explain why exhaled air is warmer and wetter than inhaled air.', 'Air is warmed by the body and water evaporates from the moist alveolar surfaces into the air.', '[2]'),
            ('Explain how the alveoli are adapted for efficient gas exchange.', 'Millions of alveoli give a huge surface area; walls one cell thick give short diffusion distance; dense capillary network and ventilation maintain steep concentration gradients; moist lining dissolves gases.', 'any three [3]'),
            ('Describe how limewater can be used to compare the carbon dioxide content of inhaled and exhaled air.', 'Breathe in through one tube of limewater and out through another; the exhaled-air tube turns milky faster, showing more CO₂.', 'method [1]; exhaled tube milky faster [1] [2]'),
            ('Explain why smoking damages the gas exchange system.', 'Tar paralyses cilia and causes mucus to build up (bronchitis); smoke damages alveolar walls, reducing surface area (emphysema); tar contains carcinogens (lung cancer).', 'any two effects explained [2]')])
myths(t, [('Exhaled air contains no oxygen.', 'Exhaled air still contains about 16% oxygen.'), ('Gas exchange takes place in the trachea and bronchi.', 'Gas exchange takes place in the alveoli.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def air_pct(r, D):
    o_in, o_out = 21, round(r.uniform(15.5, 17), 1)
    c_in, c_out = 0.04, round(r.uniform(3.5, 4.5), 1)
    if D == 1:
        return NQ(r, f'Inhaled air contains {o_in}% oxygen and exhaled air contains {o_out}%. What percentage of the inhaled oxygen is absorbed? (percentage of oxygen removed = change ÷ inhaled × 100)', (o_in - o_out) / o_in * 100,
                  [o_in - o_out, o_out / o_in * 100, (o_in - o_out) / o_out * 100, 100 - o_out], '%', f'({o_in} − {o_out}) ÷ {o_in} × 100 = {fx((o_in - o_out) / o_in * 100, 1)}%.', f=lambda v: fx(v, 1))
    st = f'Inhaled air contains {o_in}% oxygen and {c_in}% carbon dioxide. Exhaled air contains {o_out}% oxygen and {c_out}% carbon dioxide. (a) Calculate the percentage decrease in oxygen. (b) Calculate how many times greater the carbon dioxide concentration is in exhaled air.'
    ans = f'(a) {fx((o_in - o_out) / o_in * 100, 1)}% (b) {fx(c_out / c_in, 0)} times'
    key = f'(a) ({o_in} − {o_out}) ÷ {o_in} × 100 = {fx((o_in - o_out) / o_in * 100, 1)}% [2] (b) {c_out} ÷ {c_in} = {fx(c_out / c_in, 0)} [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain these changes.'
        ans += ' (c) Oxygen diffuses into the blood and is used in respiration; carbon dioxide from respiration diffuses into the alveoli.'
        key += ' (c) O₂ used in respiration [1]; CO₂ produced [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'short')
def gex_compare(r, D):
    cases = [('the gills of a fish', 'many filaments and lamellae give a large surface area; thin; dense capillaries; water flows over continuously'),
             ('a leaf', 'large flat surface; air spaces in spongy mesophyll; stomata; thin'), ('the skin of a frog', 'thin, moist and well supplied with capillaries'),
             ('the alveoli of a human lung', 'huge surface area; walls one cell thick; capillary network; ventilation')]
    a, b = r.choice(cases)
    return Q(f'Describe how {a} {"is" if a.startswith("a ") else "are"} adapted for efficient gas exchange.', cap(b) + '.', 'three features linked to fast diffusion [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def lung_case(r, D):
    a1 = r.choice([70, 75, 80])
    a2 = round(a1 * r.uniform(0.35, 0.6))
    intro = f'A doctor in {city(r)} compares lung tissue from a non-smoker and a long-term smoker with emphysema. The total alveolar surface area is about {a1} m² in the non-smoker and {a2} m² in the smoker.'
    parts = [lambda r: ('Calculate the percentage reduction in surface area.', f'{fx((a1 - a2) / a1 * 100, 1)}%', f'({a1} − {a2}) ÷ {a1} × 100 [1] = {fx((a1 - a2) / a1 * 100, 1)}% [1] [2]'),
             lambda r: ('Explain why the smoker becomes breathless during mild exercise.', 'Smaller surface area means less oxygen diffuses into the blood, so less is available for aerobic respiration in muscles.', 'less diffusion [1]; less oxygen for respiration [1] [2]'),
             lambda r: ('Describe how the cilia and mucus normally protect the lungs, and how smoking affects them.', 'Mucus traps pathogens and dust; cilia sweep it up and out. Smoke paralyses / destroys cilia, so mucus builds up, causing coughing and infections.', 'normal function [1]; effect of smoking [1] [2]'),
             lambda r: ('Name two other components of tobacco smoke and state their effects.', 'Nicotine: addictive, raises heart rate; carbon monoxide: combines with haemoglobin, reducing oxygen transport; tar: carcinogen.', 'two components with effects [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of the human breathing system and explain how the alveoli are adapted for gas exchange.', 'Larynx, trachea with cartilage rings, bronchi, bronchioles, alveoli; ribs, intercostal muscles, diaphragm. Alveoli: large surface area, thin walls, capillaries, moist, ventilation maintains gradient.',
           'structures named in order [2]; cartilage / ribs / muscles [1]; three adaptations [3] [6]')])
t11c = t

t = T('Mechanism of ventilation: intercostal muscles, diaphragm and the effect of physical activity on breathing', 'mechanism of ventilation', 'intercostal muscles, diaphragm', 'effect of physical activity on breathing')
facts(t, [('ventilation', 'the movement of air into and out of the lungs'), ('diaphragm', 'a sheet of muscle below the lungs that contracts and flattens during inhalation'),
          ('external intercostal muscles', 'muscles between the ribs that contract to raise the ribcage during inhalation'), ('internal intercostal muscles', 'muscles between the ribs that contract to pull the ribcage down during forced exhalation'),
          ('tidal volume', 'the volume of air breathed in or out in one normal breath'), ('breathing rate', 'the number of breaths taken per minute')])
mcqs(t, [('What happens during inhalation?', 'The diaphragm contracts and flattens and the ribs move up and out', 'Volume of thorax increases, pressure falls below atmospheric, air enters.', ['The diaphragm relaxes and domes upwards', 'The ribs move down and in', 'The pressure in the lungs rises']),
         ('Why does the breathing rate increase during exercise?', 'To remove extra carbon dioxide and supply more oxygen to muscles', 'The brain detects the rise in CO₂ concentration in the blood.', ['To cool the body', 'To remove lactic acid through the lungs', 'To decrease heart rate']),
         ('Which detects the increase in carbon dioxide concentration in the blood during exercise?', 'The brain', 'Receptors in the brain respond to CO₂ concentration and increase breathing rate and depth.', ['The lungs', 'The diaphragm', 'The stomach'])])
shorts(t, [('State two changes to breathing during exercise.', 'Breathing rate increases; depth of breathing (tidal volume) increases.', '[2]'), ('State the role of the internal intercostal muscles.', 'They contract during forced exhalation to pull the ribs down and in.', '[1]')])
explain(t, [('Explain how air is drawn into the lungs.', 'External intercostals contract, raising the ribs; diaphragm contracts and flattens; volume of the thorax increases and pressure falls below atmospheric pressure, so air flows in.', 'muscles contract [1]; volume increases [1]; pressure falls / air flows in [1] [3]'),
            ('Explain why breathing rate stays high for some time after exercise.', 'Carbon dioxide concentration is still high and oxygen debt must be repaid to break down lactic acid, so the brain keeps breathing rate high.', 'CO₂ still high [1]; oxygen debt / lactic acid [1] [2]'),
            ('Explain how the increase in carbon dioxide during exercise leads to deeper and faster breathing.', 'More CO₂ is produced by respiring muscles; the brain detects the increased CO₂ concentration in the blood and sends impulses to the intercostal muscles and diaphragm to contract faster and more strongly.', 'CO₂ rises [1]; detected by brain [1]; impulses to muscles [1] [3]'),
            ('Explain how exhalation happens at rest.', 'The external intercostals and diaphragm relax; the ribs move down and in and the diaphragm domes up; thorax volume decreases, pressure increases above atmospheric and air is forced out.', 'relaxation [1]; volume decreases / pressure increases [1] [2]')])
myths(t, [('Air is sucked into the lungs because the lungs expand by themselves.', 'The intercostal muscles and diaphragm increase the volume of the thorax, lowering the pressure so air flows in.'), ('The diaphragm moves up during inhalation.', 'The diaphragm contracts and flattens (moves down) during inhalation.')])

BREATH = {'setup': lambda r, p: f'{p} measured the breathing rate of a student at rest and at the end of each minute of running on a treadmill at increasing speed.',
          'iv': ('time running', 'min'), 'xs': lambda r: [0, 1, 2, 3, 4, 5], 'dv': ('breathing rate', 'breaths/min'), 'y': lambda x, k: 14 * (0.9 + 0.1 * k) + 26 * k * (1 - math.exp(-x / 1.6)), 'dp': 0, 'noise': 0.04,
          'controls': ['same student', 'temperature of the room', 'method of counting breaths (same time interval)', 'treadmill gradient'],
          'why': ('Running muscles respire faster and produce more CO₂; the brain detects the higher CO₂ concentration and increases breathing rate (and depth) to remove CO₂ and supply more oxygen. The rate levels off as supply meets demand.', 'more respiration / CO₂ [1]; brain detects CO₂ [1]; more O₂ supplied / CO₂ removed [1] [3]'),
          'improve': ['use several students and calculate a mean', 'measure depth of breathing as well, using a spirometer'],
          'extra': [lambda r, d: ('Each breath at 5 minutes had a volume of 1.8 dm³. Calculate the volume of air breathed per minute at 5 minutes.', f'{fx(d["means"][-1] * 1.8, 1)} dm³/min', f'{fx(d["means"][-1], 2)} × 1.8 [1] = {fx(d["means"][-1] * 1.8, 1)} dm³/min [1] [2]')]}
add_practical(t, BREATH, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'numerical')
def vent_calc(r, D):
    br = r.choice([12, 14, 15, 16, 18])
    tv = r.choice([0.4, 0.5, 0.6])
    br2 = r.choice([30, 36, 40, 45])
    tv2 = r.choice([1.5, 2.0, 2.5])
    v1, v2 = br * tv, br2 * tv2
    if D == 1:
        return NQ(r, f'A person takes {br} breaths per minute, each of {tv} dm³. What volume of air is breathed per minute?', v1, [br + tv, br / tv, v1 * 10, tv * 60], ' dm³', f'{br} × {tv} = {fx(v1, 2)} dm³.', f=lambda v: fx(v, 2))
    st = f'At rest a person takes {br} breaths per minute with a tidal volume of {tv} dm³. During exercise this changes to {br2} breaths per minute and {tv2} dm³. (a) Calculate the volume of air breathed per minute at rest and during exercise. (b) Calculate the percentage increase.'
    ans = f'(a) {fx(v1, 2)} dm³/min and {fx(v2, 2)} dm³/min (b) {fx(pct(v1, v2), 0)}%'
    key = f'(a) {br} × {tv} = {fx(v1, 2)} [1]; {br2} × {tv2} = {fx(v2, 2)} [1] (b) ({fx(v2, 2)} − {fx(v1, 2)}) ÷ {fx(v1, 2)} × 100 = {fx(pct(v1, v2), 0)}% [1]'
    m = 3
    if D >= 4:
        st += ' (c) Explain why both breathing rate and depth increase.'
        ans += ' (c) To supply more oxygen to respiring muscles and remove more CO₂; detected by brain from CO₂ concentration.'
        key += ' (c) more O₂ / remove CO₂ [1]; CO₂ detected by brain [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def bell_case(r, D):
    intro = 'A teacher demonstrates breathing using a bell jar model: balloons attached to a Y-tube represent the lungs, the bell jar represents the thorax, and a rubber sheet at the bottom represents the diaphragm.'
    parts = [lambda r: ('Describe and explain what happens to the balloons when the rubber sheet is pulled down.', 'They inflate: the volume inside the jar increases, pressure falls below atmospheric, so air flows into the balloons.', 'inflate [1]; volume up / pressure down [1] [2]'),
             lambda r: ('State one way in which the model is not like the real thorax.', 'It has no ribs or intercostal muscles; the walls cannot move; the diaphragm is pulled, not contracted; balloons are not alveoli.', '[1]'),
             lambda r: ('Describe the role of the intercostal muscles during inhalation.', 'External intercostals contract, moving the ribcage up and out, increasing thorax volume.', '[2]'),
             lambda r: ('Explain why pressure changes cause air to move.', 'Air moves from a region of higher pressure to lower pressure.', '[1]'),
             lambda r: ('Describe how forced exhalation differs from exhalation at rest.', 'At rest exhalation is passive (muscles relax); in forced exhalation the internal intercostals and abdominal muscles contract to push air out.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how the diaphragm and intercostal muscles bring about inhalation and exhalation, and how breathing changes during exercise.', 'Inhale: external intercostals contract, ribs up/out; diaphragm contracts, flattens; volume up, pressure down, air in. Exhale: relax, volume down, pressure up, air out; internal intercostals in forced exhalation. Exercise: more CO₂ detected by brain; faster and deeper breathing.',
           'inhalation [2]; exhalation [2]; exercise and CO₂ / brain [2] [6]')])
t11d = t
CHAPTERS[1] = [t11a, t11b, t11c, t11d]


# ===================================================================== 2 Coordination and response
t = T('Nervous system: neurones, reflex arcs and synapses', 'nervous system', 'reflex arcs', 'synapses')
facts(t, [('reflex action', 'a means of automatically and rapidly integrating and coordinating stimuli with the responses of effectors'), ('synapse', 'a junction between two neurones'),
          ('sensory neurone', 'a neurone that carries impulses from a receptor to the central nervous system'), ('relay neurone', 'a neurone in the central nervous system that connects sensory and motor neurones'),
          ('motor neurone', 'a neurone that carries impulses from the central nervous system to an effector'), ('neurotransmitter', 'a chemical released at a synapse that diffuses across the gap and binds to receptors on the next neurone'),
          ('effector', 'a muscle or gland that carries out a response')])
mcqs(t, [('What is the correct order of structures in a reflex arc?', 'receptor → sensory neurone → relay neurone → motor neurone → effector', 'Stimulus detected by receptor; impulse passes through CNS via relay neurone; effector responds.', ['receptor → motor neurone → relay neurone → sensory neurone → effector', 'effector → sensory neurone → relay neurone → motor neurone → receptor', 'receptor → relay neurone → sensory neurone → effector → motor neurone']),
         ('Why can impulses only travel in one direction across a synapse?', 'Neurotransmitter is released only from one side and receptors are only on the other', 'Vesicles are in the presynaptic neurone; receptor proteins are on the postsynaptic membrane.', ['The synapse is a solid connection', 'Impulses travel by osmosis', 'The second neurone has no membrane']),
         ('What makes up the central nervous system?', 'The brain and spinal cord', 'The CNS is brain + spinal cord; nerves form the peripheral nervous system.', ['The brain and nerves', 'The spinal cord and muscles', 'All neurones in the body'])])
shorts(t, [('State the two parts of the human nervous system.', 'Central nervous system (brain and spinal cord) and peripheral nervous system (nerves).', '[2]'), ('Give two examples of reflex actions.', 'Withdrawing a hand from a hot object; pupil reflex; knee-jerk; blinking.', '[2]')])
explain(t, [('Explain why reflex actions are important for survival.', 'They are automatic and very fast, so the body responds to danger (e.g. heat, bright light) before damage occurs, without conscious thought.', 'fast / automatic [1]; prevents harm [1] [2]'),
            ('Describe the events at a synapse when an impulse arrives.', 'The impulse causes vesicles to release neurotransmitter into the gap; it diffuses across and binds to receptor molecules on the next neurone, starting a new impulse.', 'vesicles release neurotransmitter [1]; diffuses across gap [1]; binds receptors / new impulse [1] [3]'),
            ('Explain why some drugs that block receptor proteins at synapses can cause paralysis.', 'Neurotransmitter cannot bind, so impulses are not passed to motor neurones / muscles; muscles cannot contract.', 'blocks binding [1]; no impulse to muscle [1] [2]'),
            ('Explain why the relay neurone is found in the spinal cord in a reflex arc.', 'The impulse passes from sensory to motor neurone through the spinal cord without first going to the brain, which makes the response quicker.', 'shortest pathway / via spinal cord [1]; faster response [1] [2]')])
myths(t, [('In a reflex arc, the brain decides how to respond.', 'Reflexes are automatic; the impulse is passed through the spinal cord (or brain) without conscious decision.'), ('Impulses jump across synapses as electricity.', 'Neurotransmitter chemicals diffuse across the synaptic gap.')])

RULER = {'setup': lambda r, p: f'{p} measured reaction time by catching a falling ruler. The distance the ruler fell before being caught was recorded for five attempts each after different numbers of practice attempts.',
         'iv': ('number of practice attempts', ''), 'xs': lambda r: [0, 5, 10, 15, 20], 'dv': ('distance fallen', 'cm'), 'y': lambda x, k: k * (8 + 12 * math.exp(-x / 8)), 'dp': 1, 'noise': 0.06,
         'controls': ['same hand used', 'same starting position of fingers', 'same person dropping the ruler', 'no warning before the drop', 'same ruler'],
         'trend': lambda d: 'As the number of practice attempts increases, the distance fallen decreases (reaction time gets shorter), levelling off.',
         'why': ('With practice, the brain becomes more efficient at processing the visual stimulus and sending impulses along motor neurones to the hand muscles, so the response is faster; there is a minimum time for impulses to travel and cross synapses.', 'faster processing / pathway [1]; impulses to muscles [1]; limit set by nerve / synapse transmission [1] [3]'),
         'improve': ['use a computer reaction timer for more precise times', 'test several people and calculate a mean'],
         'extra': [lambda r, d: ('Calculate the reaction time for the first set of results using t = √(2d ÷ 9.8), with d in metres.', f'{fx(math.sqrt(2 * d["means"][0] / 100 / 9.8), 3)} s', f'd = {fx(d["means"][0] / 100, 4)} m [1]; t = √(2 × {fx(d["means"][0] / 100, 4)} ÷ 9.8) = {fx(math.sqrt(2 * d["means"][0] / 100 / 9.8), 3)} s [1] [2]'),
                   lambda r, d: ('Explain why catching the ruler is not a reflex action.', 'It involves conscious thought / the brain making a decision, and it is learned rather than automatic.', '[2]')],
         'xfmt': lambda v: f'{v} practice attempts', 'prep': 'after'}
add_practical(t, RULER, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'short')
def reflex_lab(r, D):
    cases = [('touching a hot pan', 'heat / temperature receptors in the skin', 'muscles in the arm (biceps)', 'hand pulled away'), ('bright light shining in the eye', 'light receptors (rods and cones) in the retina', 'circular muscles of the iris', 'pupil constricts'),
             ('a tap below the knee', 'stretch receptors in the thigh muscle', 'thigh muscle (quadriceps)', 'lower leg kicks'), ('dust touching the cornea', 'touch receptors in the cornea', 'eyelid muscles', 'blinking'),
             ('stepping on a sharp object', 'pain receptors in the foot', 'leg muscles', 'foot lifted')]
    s_, rec, eff, resp = r.choice(cases)
    if D <= 2:
        return MQ(r, f'In the reflex response to {s_}, what is the effector?', eff, [c[2] for c in cases if c[2] != eff], f'Stimulus {s_}; receptor {rec}; effector {eff}; response: {resp}.')
    return Q(f'For the reflex response to {s_}, name (a) the stimulus, (b) the receptor, (c) the effector and (d) describe the pathway of the impulse from receptor to effector.',
             f'(a) {s_} (b) {rec} (c) {eff} (d) receptor → sensory neurone → relay neurone (CNS) → motor neurone → effector',
             f'(a) [1] (b) {rec} [1] (c) {eff} [1] (d) correct sequence of three neurone types [2] [5]', 'short', 5)


@t.add('C3', (2, 3, 4), 'numerical')
def impulse_speed(r, D):
    dist = r.choice([0.8, 1.0, 1.2, 1.5])
    tm = r.choice([0.01, 0.015, 0.02, 0.025])
    v = dist / tm
    st = f'An impulse travels {fx(dist)} m along a motor neurone from the spinal cord to a foot muscle in {fx(tm * 1000)} milliseconds. Calculate the speed of the impulse in m/s.'
    key = f'{fx(tm * 1000)} ms = {fx(tm, 3)} s [1]; {fx(dist)} ÷ {fx(tm, 3)} = {fx(v, 1)} m/s [1]'
    m = 2
    if D >= 4:
        st += ' Suggest why a reflex involving two synapses takes longer than the time for the impulse to travel along the neurones.'
        key += '; time taken for neurotransmitter to be released, diffuse and bind at each synapse [1]'
        m = 3
    return Q(st, f'{fx(v, 1)} m/s', key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def nerve_case(r, D):
    intro = f'{person(r)} accidentally touches a cactus spine in a garden in {city(r)} and pulls the hand away before feeling any pain.'
    parts = [lambda r: ('Name the type of response and explain why it is useful.', 'A reflex action: rapid and automatic, reducing damage.', '[2]'),
             lambda r: ('Describe the pathway of the nerve impulse.', 'Pain receptor → sensory neurone → relay neurone in spinal cord → motor neurone → muscle in arm (effector).', '[3]'),
             lambda r: ('Explain why the pain is felt after the hand has moved.', 'The impulse also travels up the spinal cord to the brain, a longer pathway; conscious awareness takes longer than the reflex.', '[2]'),
             lambda r: ('Describe how an impulse passes across a synapse.', 'Neurotransmitter released from vesicles, diffuses across the gap, binds to receptors on next neurone.', '[3]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


longs(t, [('Describe the structure of a reflex arc and explain how a synapse ensures that impulses travel in one direction.', 'Receptor, sensory neurone, relay neurone in CNS, motor neurone, effector. Synapse: vesicles of neurotransmitter only in presynaptic neurone, released by impulse, diffuse across gap, bind receptors only on postsynaptic membrane.',
           'arc components in order [3]; neurotransmitter release / diffusion [1]; receptors on one side only [1] [5]')])
t12a = t

EYE = [('cornea', 'refracts (bends) light entering the eye'), ('iris', 'controls how much light enters the pupil'), ('lens', 'focuses light onto the retina'),
       ('retina', 'contains light receptors (rods and cones)'), ('optic nerve', 'carries impulses from the retina to the brain'), ('blind spot', 'where the optic nerve leaves the retina; no receptors'),
       ('fovea', 'part of the retina with many cones, giving detailed colour vision'), ('ciliary muscles', 'contract or relax to change the shape of the lens'), ('suspensory ligaments', 'attach the lens to the ciliary muscles')]
t = T('Sense organs: structure and function of the eye, accommodation and pupil reflex', 'sense organs', 'structure and function of the eye', 'accommodation', 'pupil reflex')
facts(t, EYE[:7] + [('accommodation', 'changing the shape of the lens to focus on near or distant objects'), ('sense organ', 'a group of receptor cells responding to specific stimuli such as light, sound, touch, temperature or chemicals')])
mcqs(t, [('In bright light, what happens to the muscles of the iris?', 'Circular muscles contract and radial muscles relax', 'Pupil constricts, reducing light entering.', ['Radial muscles contract and circular muscles relax', 'Both sets of muscles relax', 'Ciliary muscles contract']),
         ('To focus on a near object, the lens becomes', 'more rounded (fatter)', 'Ciliary muscles contract, suspensory ligaments slacken, lens rounds up and refracts more.', ['thinner and flatter', 'cloudy', 'larger in diameter only']),
         ('Which cells in the retina allow colour vision?', 'Cones', 'Cones (three types) work in bright light; rods are sensitive in dim light.', ['Rods', 'Ciliary cells', 'Optic nerve cells'])])
shorts(t, [('State the difference between rods and cones.', 'Rods are sensitive to dim light and give black-and-white vision; cones need bright light and give colour vision.', '[2]'), ('State the function of the optic nerve.', 'Carries impulses from the retina to the brain.', '[1]')])
explain(t, [('Explain how the eye focuses on a distant object.', 'Ciliary muscles relax, suspensory ligaments are pulled tight, the lens is pulled thin, refracting light less so it focuses on the retina.', 'ciliary relax [1]; ligaments tight [1]; lens thin [1] [3]'),
            ('Explain why the pupil reflex is important.', 'It protects the retina from damage by bright light and lets more light in when it is dim so we can still see.', '[2]'),
            ('Explain why we cannot see colours well in dim light.', 'Cones need bright light to work; in dim light only rods respond, and rods do not distinguish colour.', '[2]'),
            ('Explain why an image falling on the blind spot is not seen.', 'There are no rods or cones there, because the optic nerve leaves the eye at that point.', '[2]')])
myths(t, [('The pupil gets smaller in dim light.', 'The pupil dilates (gets larger) in dim light to let more light in.'), ('The lens is the only part of the eye that bends light.', 'The cornea refracts light the most; the lens adjusts focus.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def eye_id(r, D):
    a, b = r.choice(EYE)
    if D <= 2:
        return MQ(r, f'Which part of the eye {b}?', a, [x[0] for x in EYE if x[0] != a], f'{cap(a)}: {b}.')
    cond = r.choice([('walks from a dark room into bright sunlight', 'circular muscles of the iris contract, radial relax; pupil constricts'), ('walks from bright sunlight into a dark cinema', 'radial muscles contract, circular relax; pupil dilates'),
                     ('looks up from a book to a distant mountain', 'ciliary muscles relax, suspensory ligaments tighten, lens becomes thinner'), ('looks down from a distant bus to a phone screen', 'ciliary muscles contract, suspensory ligaments slacken, lens becomes fatter')])
    return Q(f'{person(r)} {cond[0]}. Describe the changes that occur in the eye and explain why they are needed.', cap(cond[1]) + '; this adjusts the light entering / keeps the image focused on the retina.', 'muscle changes [2]; structure change [1]; reason [1] [4]', 'short', 4)


@t.add('C3', (2, 3, 4), 'case')
def pupil_data(r, D):
    lux = [10, 100, 500, 1000, 5000]
    base = r.uniform(6.5, 7.5)
    vals = [round(base - 1.05 * math.log10(x) + r.uniform(-0.1, 0.1), 1) for x in lux]
    tab = ', '.join(f'{l} lux: {v} mm' for l, v in zip(lux, vals))
    st = f'Pupil diameter was measured at different light intensities: {tab}. (a) Describe the trend. (b) Name the muscles that contract to make the pupil smaller. (c) Calculate the percentage decrease in diameter from {lux[0]} to {lux[-1]} lux.'
    return Q(st, f'(a) As light intensity increases, pupil diameter decreases (from {vals[0]} to {vals[-1]} mm). (b) circular muscles of the iris (c) {fx((vals[0] - vals[-1]) / vals[0] * 100, 1)}%',
             f'(a) trend with data [1] (b) circular muscles [1] (c) ({vals[0]} − {vals[-1]}) ÷ {vals[0]} × 100 = {fx((vals[0] - vals[-1]) / vals[0] * 100, 1)}% [2] [4]', 'case', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def eye_case(r, D):
    intro = f'An optometrist in {city(r)} tests a patient\'s vision. The patient reads a chart 6 m away and then a card held 25 cm from the eyes.'
    parts = [lambda r: ('Describe the changes in the eye when the patient changes focus from the chart to the card.', 'Ciliary muscles contract, suspensory ligaments slacken, lens becomes more rounded, refracts light more.', '[3]'),
             lambda r: ('Explain why the optometrist dims the lights before examining the retina.', 'In dim light the pupil dilates (radial muscles contract), so more of the retina can be seen.', '[2]'),
             lambda r: ('State where light should be focused for the sharpest colour image and why.', 'On the fovea, which has the most cones.', '[2]'),
             lambda r: ('Explain how information from the retina reaches the brain.', 'Rods and cones generate impulses carried along sensory neurones in the optic nerve to the brain.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t12b = t

GLANDS = [('adrenal glands', 'adrenaline'), ('pancreas', 'insulin and glucagon'), ('testes', 'testosterone'), ('ovaries', 'oestrogen and progesterone'), ('pituitary gland', 'FSH, LH and ADH'), ('thyroid gland', 'thyroxine')]
t = T('Hormones in humans: endocrine glands and adrenaline; comparing nervous and hormonal control', 'hormones in humans', 'endocrine glands and adrenaline', 'comparing nervous and hormonal control')
facts(t, [('hormone', 'a chemical substance, produced by a gland and carried by the blood, which alters the activity of one or more specific target organs'), ('endocrine gland', 'a ductless gland that secretes hormones directly into the blood'),
          ('adrenaline', 'a hormone from the adrenal glands that prepares the body for fight or flight'), ('target organ', 'an organ whose activity is changed by a particular hormone'), ('fight or flight', 'the response to danger or stress controlled by adrenaline')])
mcqs(t, [('Which is an effect of adrenaline?', 'Increased heart rate', 'Adrenaline increases breathing rate, heart rate, blood glucose and pupil diameter.', ['Decreased blood glucose', 'Constricted pupils', 'Slower breathing']),
         ('How are hormones transported to their target organs?', 'In the blood plasma', 'Endocrine glands secrete hormones into the blood.', ['Along neurones', 'Through ducts', 'In the lymph only']),
         ('Which statement compares hormonal and nervous control correctly?', 'Hormonal effects are slower but last longer', 'Nervous: electrical, fast, short-lived, precise. Hormonal: chemical in blood, slower, longer-lasting, widespread.', ['Hormonal effects are faster', 'Nervous impulses travel in the blood', 'Both use only chemical signals in the blood'])])
shorts(t, [('Name the hormone produced by each gland: adrenal gland, testes, ovaries.', 'Adrenaline; testosterone; oestrogen.', '[3]'), ('State three effects of adrenaline on the body.', 'Increased breathing rate, increased heart rate, wider pupils, increased blood glucose concentration.', 'any three [3]')])
explain(t, [('Explain how the effects of adrenaline help a person escape danger.', 'Higher heart and breathing rates deliver more oxygen and glucose to muscles; blood glucose rises (glycogen breakdown); more respiration and energy release for muscle contraction.', 'more O₂ / glucose to muscles [1]; more respiration / energy [1] [2]'),
            ('Explain why the response to a hormone is slower than a nervous response.', 'Hormones are carried in the blood, which takes time to reach target organs; nerve impulses travel rapidly along neurones.', '[2]'),
            ('Explain why a hormone only affects its target organs although it travels throughout the body.', 'Only target cells have receptors with a shape complementary to the hormone.', '[2]')])
myths(t, [('Hormones travel along nerves to their target organs.', 'Hormones are carried by the blood plasma.'), ('Adrenaline slows the heart to save energy in an emergency.', 'Adrenaline increases heart rate and breathing rate.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def gland_q(r, D):
    g, h = r.choice(GLANDS)
    if D <= 2:
        return MQ(r, f'Which gland secretes {h}?', g, [x[0] for x in GLANDS if x[0] != g], f'{cap(g)} → {h}.')
    feat = r.sample([('speed', 'fast', 'slower'), ('form of signal', 'electrical impulses', 'chemicals (hormones)'), ('pathway', 'neurones', 'blood'), ('duration of effect', 'short', 'longer-lasting'), ('area affected', 'localised / precise', 'can be widespread')], 3)
    return Q('Compare nervous and hormonal control under these headings: ' + ', '.join(f[0] for f in feat) + '.', '; '.join(f'{f[0]}: nervous {f[1]}, hormonal {f[2]}' for f in feat), '; '.join(f'{f[0]} [1]' for f in feat) + ' [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'case')
def adren_data(r, D):
    hr0 = r.randrange(65, 80)
    hr1 = round(hr0 * r.uniform(1.4, 1.8))
    g0 = round(r.uniform(4.5, 5.5), 1)
    g1 = round(g0 * r.uniform(1.3, 1.6), 1)
    st = f'Before a parachute jump, a student\'s heart rate rose from {hr0} to {hr1} beats/min and blood glucose rose from {g0} to {g1} mmol/dm³. (a) Calculate the percentage increase in heart rate. (b) Name the hormone responsible and the gland that secretes it. (c) Explain the advantage of the rise in blood glucose.'
    return Q(st, f'(a) {fx(pct(hr0, hr1), 0)}% (b) adrenaline; adrenal glands (c) more glucose for respiration in muscles, releasing more energy for fight or flight.',
             f'(a) ({hr1} − {hr0}) ÷ {hr0} × 100 = {fx(pct(hr0, hr1), 0)}% [2] (b) adrenaline [1]; adrenal glands [1] (c) glucose for respiration / energy for muscles [1] [5]', 'case', 5)


@t.add('C4', (3, 4, 5), 'multi_step')
def horm_case(r, D):
    intro = f'A student in {city(r)} hears a loud bang behind her. She jumps immediately, and for several minutes afterwards her heart pounds and her hands shake.'
    parts = [lambda r: ('Explain why the jump happens immediately but the pounding heart lasts for several minutes.', 'The jump is a nervous response (fast impulses); the pounding heart is due to adrenaline in the blood, which takes time to be broken down, so its effect lasts longer.', 'nervous fast [1]; hormone in blood, lasts longer [1] [2]'),
             lambda r: ('Name the gland that releases adrenaline and state how adrenaline reaches the heart.', 'Adrenal glands; carried in the blood plasma.', '[2]'),
             lambda r: ('Describe two other effects of adrenaline on the body.', 'Increased breathing rate; dilated pupils; increased blood glucose.', '[2]'),
             lambda r: ('Compare nervous and hormonal control, giving three differences.', 'Nervous: electrical impulses, along neurones, fast, short-lived. Hormonal: chemicals, in blood, slower, longer-lasting.', '[3]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t12c = t

t = T('Tropic responses in plants: gravitropism, phototropism and auxin', 'tropic responses in plants', 'gravitropism', 'phototropism', 'auxin')
facts(t, [('gravitropism', 'a response in which parts of a plant grow towards or away from gravity'), ('phototropism', 'a response in which parts of a plant grow towards or away from the direction from which light is coming'),
          ('auxin', 'a plant hormone made in the shoot tip that diffuses through the plant and stimulates cell elongation'), ('positive tropism', 'growth towards a stimulus'),
          ('clinostat', 'a slowly rotating device used to remove the effect of a one-sided stimulus such as gravity on a plant')])
mcqs(t, [('A shoot grows towards light from one side. What causes the bending?', 'More auxin on the shaded side causes cells there to elongate more', 'Auxin moves to the shaded side; shoot cells elongate more there.', ['More auxin on the lit side stops growth there', 'Light destroys all auxin', 'Cells on the lit side divide faster']),
         ('Roots grow downwards. This is', 'positive gravitropism', 'Growth towards gravity is positive gravitropism.', ['negative gravitropism', 'positive phototropism', 'negative phototropism']),
         ('Where is auxin made in a shoot?', 'In the shoot tip', 'Auxin is made in the tip and diffuses back.', ['In the roots only', 'In the leaves only', 'In the flowers'])])
shorts(t, [('State the type of tropism shown by a shoot growing upwards in the dark.', 'Negative gravitropism.', '[1]'), ('State the effect of auxin on shoot cells.', 'It stimulates cell elongation.', '[1]')])
explain(t, [('Explain how auxin causes a shoot to bend towards light.', 'Auxin is made in the tip and moves to the shaded side; it stimulates cell elongation there, so the shaded side grows faster and the shoot bends towards the light.', 'auxin to shaded side [1]; cell elongation [1]; unequal growth / bending [1] [3]'),
            ('Explain the advantage of positive phototropism to a seedling.', 'Leaves receive more light for photosynthesis, so more glucose is made for growth.', '[2]'),
            ('Explain why a seedling placed on its side on a clinostat grows straight.', 'Rotation means gravity acts equally on all sides, so auxin is evenly distributed and growth is even.', '[2]'),
            ('A shoot tip is covered with a foil cap and lit from one side. Explain why the shoot does not bend.', 'The tip detects light; with the tip covered, auxin is not redistributed to one side, so growth is even.', '[2]')])
myths(t, [('Plants grow towards light because light pulls them.', 'Auxin redistribution causes the shaded side to grow faster, so the shoot bends towards the light.'), ('Auxin makes cells divide faster on the lit side.', 'Auxin moves to the shaded side, where it stimulates cell elongation.')])

PHOTO = {'setup': lambda r, p: f'{p} grew cress seedlings in boxes with a hole on one side, and measured the angle of bending of the shoots towards the light after 3 days at different distances from a lamp.',
         'iv': ('distance of lamp', 'cm'), 'xs': lambda r: r.choice([[20, 40, 60, 80, 100], [25, 50, 75, 100]]), 'dv': ('angle of bending', '°'), 'y': lambda x, k: k * 60 * math.exp(-x / 70) + 2, 'dp': 0,
         'controls': ['type and age of seedlings', 'temperature', 'water given', 'time of exposure', 'size of the hole'],
         'why': ('With brighter light (closer lamp) the difference in light between the two sides is greater; more auxin moves to the shaded side, causing more cell elongation there and greater bending.', 'auxin on shaded side [1]; cell elongation [1]; greater one-sided light causes more bending [1] [3]'),
         'improve': ['use a protractor on photographs to measure angles more accurately', 'use more seedlings per box and calculate the mean'],
         'control': 'Seedlings grown in a box with light from all sides (or in darkness) — they grow straight, showing bending is caused by one-sided light.'}
add_practical(t, PHOTO, C3D=(2, 3, 4), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'short')
def tropism_pred(r, D):
    cases = [('a shoot tip covered with a foil cap, light from the left', 'grows straight up', 'the tip, which detects light, is covered so auxin is not redistributed'),
             ('a shoot with its tip removed, light from the left', 'does not grow / grows very little', 'no tip, so no auxin is made'),
             ('a shoot lit from the left with a mica sheet inserted vertically below the tip on the shaded side', 'grows straight / little bending', 'mica stops auxin moving down the shaded side'),
             ('a root placed horizontally', 'bends downwards', 'positive gravitropism (auxin accumulates on the lower side and inhibits elongation in roots)'),
             ('a shoot placed horizontally in the dark', 'bends upwards', 'negative gravitropism: auxin collects on the lower side and stimulates elongation'),
             ('a shoot on a slowly rotating clinostat, lit from one side', 'grows straight', 'all sides receive light equally')]
    a, b, c = r.choice(cases)
    if D <= 2:
        return MQ(r, f'Predict the growth of {a}.', b, [x[1] for x in cases if x[1] != b] + ['bends towards the light'], f'{cap(b)}: {c}.')
    return Q(f'Predict and explain the growth of {a}.', f'{cap(b)}: {c}.', 'prediction [1]; explanation referring to auxin / tip [2] [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def trop_case(r, D):
    intro = f'Bean seeds were germinated in damp cotton wool in a dark cupboard in {city(r)}. Some were placed horizontally; some were placed on a clinostat.'
    parts = [lambda r: ('Describe the growth of the root and shoot of the horizontal seeds.', 'Root bends downwards (positive gravitropism); shoot bends upwards (negative gravitropism).', '[2]'),
             lambda r: ('Explain why the seeds on the clinostat grow horizontally.', 'Rotation means gravity acts on all sides equally, so there is no unequal auxin distribution.', '[2]'),
             lambda r: ('Explain why the experiment was carried out in the dark.', 'To remove the effect of light (phototropism), so only gravity affects the direction of growth.', '[2]'),
             lambda r: ('Explain the advantage of gravitropism to the root of a germinating seed.', 'Roots grow down into the soil to anchor the plant and reach water and mineral ions.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12d = t
CHAPTERS[2] = [t12a, t12b, t12c, t12d]

# ===================================================================== 3 Excretion and homeostasis
t = T('Excretion: kidney structure, nephron, ultrafiltration and selective reabsorption', 'excretion', 'kidney structure', 'nephron', 'ultrafiltration', 'selective reabsorption')
facts(t, [('excretion', 'the removal of waste products of metabolism and substances in excess of requirements'), ('nephron', 'a kidney tubule where blood is filtered and urine is formed'),
          ('ultrafiltration', 'filtration of blood under high pressure in the glomerulus, forcing small molecules into the Bowman\'s capsule'),
          ('selective reabsorption', 'the absorption of useful substances such as glucose, some salts and much water from the filtrate back into the blood'),
          ('glomerulus', 'a knot of capillaries inside the Bowman\'s capsule where ultrafiltration happens'), ('ureter', 'the tube that carries urine from a kidney to the bladder')])
mcqs(t, [('Which substance is filtered into the Bowman\'s capsule but is normally completely reabsorbed?', 'Glucose', 'All glucose is reabsorbed in the proximal convoluted tubule.', ['Urea', 'Protein', 'Red blood cells']),
         ('Why are proteins not found in the filtrate?', 'They are too large to pass through the glomerulus wall', 'Only small molecules are filtered.', ['They are reabsorbed', 'They are broken down in the kidney', 'They are converted to urea in the nephron']),
         ('What is the order of structures in a nephron?', 'Bowman\'s capsule → proximal tubule → loop of Henle → distal tubule → collecting duct', 'Filtrate flows from capsule along the tubule to the collecting duct.', ['loop of Henle → Bowman\'s capsule → collecting duct → proximal tubule', 'collecting duct → loop of Henle → Bowman\'s capsule → distal tubule', 'proximal tubule → collecting duct → Bowman\'s capsule → loop of Henle'])])
shorts(t, [('Name three substances found in urine.', 'Water, urea, salts (ions).', '[2]'), ('State the function of the bladder.', 'Stores urine.', '[1]')])
explain(t, [('Explain how ultrafiltration happens in the glomerulus.', 'The vessel leaving the glomerulus is narrower than the one entering, creating high pressure that forces water, glucose, salts and urea through the capillary walls into the Bowman\'s capsule; large proteins and cells stay in the blood.', 'high pressure [1]; small molecules forced out [1]; large proteins / cells remain [1] [3]'),
            ('Explain why glucose in the urine can indicate diabetes.', 'Normally all glucose is reabsorbed; very high blood glucose means more is filtered than can be reabsorbed, so some appears in urine.', '[2]'),
            ('Explain why a person produces more dilute urine after drinking a lot of water.', 'Less water is reabsorbed in the collecting ducts so that excess water is excreted, keeping the water potential of the blood constant.', 'less reabsorbed [1]; excess removed [1] [2]'),
            ('Explain why the kidneys are described as organs of excretion.', 'They remove urea (a waste product of metabolism) and excess water and ions from the blood.', '[2]')])
myths(t, [('The kidney filters out all the glucose so it is lost in urine.', 'Glucose is filtered but all of it is normally reabsorbed back into the blood.'), ('Urea is made in the kidneys.', 'Urea is made in the liver by deamination; the kidneys excrete it.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def kid_data(r, D):
    filt = r.choice([150, 170, 180])
    urine = round(r.uniform(1.2, 2.0), 1)
    pl_u, ur_u = 0.03, round(r.uniform(1.8, 2.2), 1)
    reab = (filt - urine) / filt * 100
    if D == 1:
        return NQ(r, f'The kidneys filter {filt} dm³ of fluid per day and produce {urine} dm³ of urine. What percentage of the filtered water is reabsorbed?', reab, [urine / filt * 100, 100 - reab / 2, filt - urine, reab / 10], '%', f'({filt} − {urine}) ÷ {filt} × 100 = {fx(reab, 1)}%.', f=lambda v: fx(v, 1))
    st = (f'The kidneys of an adult filter {filt} dm³ of plasma each day and produce {urine} dm³ of urine. The urea concentration is {pl_u} g/100 cm³ in plasma and {ur_u} g/100 cm³ in urine. '
          '(a) Calculate the percentage of filtered water that is reabsorbed. (b) Calculate how many times more concentrated urea is in urine than in plasma.')
    ans = f'(a) {fx(reab, 1)}% (b) {fx(ur_u / pl_u, 0)} times'
    key = f'(a) ({filt} − {urine}) ÷ {filt} × 100 = {fx(reab, 1)}% [2] (b) {ur_u} ÷ {pl_u} = {fx(ur_u / pl_u, 0)} [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain why the concentration of urea increases along the nephron.'
        ans += ' (c) Water is reabsorbed but urea is not (or little is), so urea becomes more concentrated.'
        key += ' (c) water reabsorbed [1]; urea left behind [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'case')
def kid_table(r, D):
    rows = [('protein', 8.0, 0, 0), ('glucose', 0.1, 0.1, 0), ('urea', 0.03, 0.03, 2.0), ('salts', 0.72, 0.72, 1.5)]
    pick = r.sample(rows, 3)
    tab = '; '.join(f'{n}: plasma {a}, filtrate {b}, urine {c}' for n, a, b, c in pick)
    st = f'Concentrations (g per 100 cm³) in blood plasma, glomerular filtrate and urine: {tab}. For each substance, explain the differences between the three values.'
    expl = {'protein': 'too large to be filtered, so absent from filtrate and urine', 'glucose': 'filtered but all reabsorbed, so absent from urine',
            'urea': 'filtered; water reabsorbed but not urea, so concentrated in urine', 'salts': 'filtered; some reabsorbed, excess excreted; more concentrated in urine as water is reabsorbed'}
    return Q(st, '; '.join(f'{n}: {expl[n]}' for n, _, _, _ in pick), '; '.join(f'{n} [2]' for n, _, _, _ in pick) + ' [6]', 'case', 6)


@t.add('C4', (3, 4, 5), 'multi_step')
def kid_case(r, D):
    intro = f'A patient in {city(r)} has kidney failure and is treated by dialysis three times a week, while waiting for a kidney transplant.'
    parts = [lambda r: ('Explain why kidney failure is life-threatening if untreated.', 'Urea and excess salts and water build up in the blood; urea is toxic and the water potential of blood changes, damaging cells.', '[2]'),
             lambda r: ('Describe how ultrafiltration produces filtrate in a healthy kidney.', 'High pressure in the glomerulus forces small molecules (water, glucose, urea, salts) into the Bowman\'s capsule.', '[2]'),
             lambda r: ('Describe what happens to glucose and water as filtrate passes along the nephron.', 'All glucose is reabsorbed (active transport) in the proximal tubule; much water is reabsorbed by osmosis along the nephron and collecting duct.', '[2]'),
             lambda r: ('Name the blood vessel that carries blood into the kidney and the tube that carries urine to the bladder.', 'Renal artery; ureter.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the kidney produces urine from blood.', 'Renal artery brings blood; glomerulus — ultrafiltration under high pressure into Bowman\'s capsule (water, glucose, urea, salts; not proteins/cells); proximal tubule reabsorbs all glucose, some salts, water; loop of Henle / collecting duct reabsorb water; urine (urea, water, salts) to ureter and bladder.',
           'ultrafiltration [2]; selective reabsorption of glucose [1]; water reabsorption [1]; urine composition / pathway [2] [6]')])
t13a = t

t = T('Deamination in the liver and formation of urea', 'deamination', 'formation of urea')
facts(t, [('deamination', 'the removal of the nitrogen-containing part of amino acids to form urea'), ('urea', 'a nitrogenous waste substance made in the liver and excreted by the kidneys'),
          ('liver', 'the organ in which excess amino acids are deaminated, glycogen is stored and bile is made'), ('assimilation', 'the use of absorbed nutrients by cells, e.g. amino acids built into proteins')])
mcqs(t, [('Where does deamination take place?', 'Liver', 'Excess amino acids are deaminated in the liver.', ['Kidney', 'Small intestine', 'Pancreas']),
         ('What happens to the nitrogen-containing part removed from an amino acid?', 'It is converted to urea', 'Ammonia formed is converted to less toxic urea.', ['It is stored as protein', 'It is respired', 'It is excreted through the lungs']),
         ('How is urea carried from the liver to the kidneys?', 'Dissolved in blood plasma', 'Urea is soluble and transported in plasma.', ['Inside red blood cells', 'Through the bile duct', 'Along neurones'])])
shorts(t, [('State what happens to the rest of the amino acid after deamination.', 'It is used in respiration (or converted to glycogen / fat).', '[1]'), ('Name the organ that makes urea and the organ that excretes it.', 'Liver; kidneys.', '[2]')])
explain(t, [('Explain why excess amino acids cannot be stored in the body.', 'There is no store for amino acids or proteins, so the excess must be deaminated and the nitrogen removed as urea.', '[2]'),
            ('Explain why a diet very high in protein increases the amount of urea in urine.', 'More excess amino acids are deaminated in the liver, producing more urea for the kidneys to excrete.', '[2]'),
            ('Explain why carbon dioxide and urea must be excreted.', 'They are toxic in high concentrations: CO₂ lowers blood pH; urea damages cells; they are waste products of metabolism.', '[2]')])
myths(t, [('Urea is produced when the kidneys break down proteins.', 'Urea is produced in the liver by deamination of excess amino acids.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def urea_calc(r, D):
    prot = r.choice([60, 80, 100, 120, 150])
    need = r.choice([50, 55, 60])
    ex = prot - need
    if ex <= 0:
        return None
    frac = 0.16
    st = f'A person eats {prot} g of protein per day but needs only {need} g. (a) Calculate the mass of excess protein. (b) About 16% of the mass of protein is nitrogen. Calculate the mass of nitrogen that must be removed by deamination each day.'
    if D == 1:
        return NQ(r, f'A person eats {prot} g of protein per day but needs only {need} g. What mass of excess amino acids must be deaminated?', ex, [prot, need, prot + need, ex / 2], ' g', f'{prot} − {need} = {ex} g.', f=lambda v: fx(v, 1))
    return Q(st, f'(a) {ex} g (b) {fx(ex * frac, 2)} g', f'(a) {prot} − {need} = {ex} g [1] (b) {ex} × 0.16 = {fx(ex * frac, 2)} g [1] [2]', 'numerical', 2)


@t.add('C4', (3, 4, 5), 'multi_step')
def deam_case(r, D):
    intro = f'A bodybuilder in {city(r)} eats a diet very high in protein shakes. A urine test shows high urea concentration.'
    parts = [lambda r: ('Describe what happens to excess amino acids in the body.', 'They are deaminated in the liver; the nitrogen-containing part is converted to urea; the rest is used for respiration or stored as glycogen/fat.', '[3]'),
             lambda r: ('Describe the route taken by urea from where it is made to where it leaves the body.', 'Liver → hepatic vein → blood → renal artery → kidney (filtered) → ureter → bladder → urethra.', '[2]'),
             lambda r: ('Suggest why the bodybuilder is advised to drink more water.', 'More water is needed to dissolve and excrete the extra urea in urine.', '[1]'),
             lambda r: ('Explain why the body needs some amino acids every day.', 'To make new proteins for growth, repair, enzymes and antibodies.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t13b = t

t = T('Homeostasis and negative feedback: control of blood glucose by insulin and glucagon; type 1 diabetes', 'homeostasis', 'negative feedback', 'insulin and glucagon', 'type 1 diabetes')
facts(t, [('homeostasis', 'the maintenance of a constant internal environment'), ('negative feedback', 'a control mechanism in which a change from the set point causes responses that return conditions to the set point'),
          ('insulin', 'a hormone secreted by the pancreas when blood glucose is high, causing the liver to convert glucose to glycogen'), ('glucagon', 'a hormone secreted by the pancreas when blood glucose is low, causing the liver to break down glycogen to glucose'),
          ('type 1 diabetes', 'a condition in which the pancreas does not produce enough insulin, so blood glucose is not controlled'), ('glycogen', 'the storage carbohydrate made from glucose in the liver and muscles')])
mcqs(t, [('After a meal, blood glucose rises. Which response occurs?', 'The pancreas secretes insulin and the liver converts glucose to glycogen', 'Insulin lowers blood glucose.', ['The pancreas secretes glucagon', 'The liver converts glycogen to glucose', 'The kidney stores glucose']),
         ('Which treatment is used for type 1 diabetes?', 'Insulin injections and monitoring the diet', 'The pancreas makes little or no insulin.', ['Antibiotics', 'Glucagon tablets only', 'Vaccination']),
         ('What is the set point for blood glucose?', 'The normal value around which it is kept', 'Negative feedback returns glucose to the set point.', ['The highest value possible', 'The value after a meal', 'The value at which glucose appears in urine'])])
shorts(t, [('State two symptoms of type 1 diabetes.', 'High blood glucose; glucose in urine; thirst; tiredness; weight loss; frequent urination.', 'any two [2]'), ('Name the organ that secretes insulin and the organ in which glycogen is stored.', 'Pancreas; liver (and muscles).', '[2]')])
explain(t, [('Explain how negative feedback keeps blood glucose concentration constant.', 'If glucose rises above the set point, the pancreas secretes insulin and the liver stores glucose as glycogen, lowering it; if it falls, glucagon is secreted and glycogen is broken down, raising it.', 'rise → insulin → glycogen [1]; fall → glucagon → glucose [1]; returns to set point [1] [3]'),
            ('Explain why a person with type 1 diabetes must not inject too much insulin.', 'Too much insulin lowers blood glucose too far (hypoglycaemia); brain cells lack glucose for respiration, causing confusion or coma.', '[2]'),
            ('Explain why a person with diabetes is advised to eat regular meals with complex carbohydrates.', 'Starchy foods release glucose slowly, avoiding large rises in blood glucose that the body cannot control without insulin.', '[2]'),
            ('Explain why blood glucose must be kept within narrow limits.', 'Too high: water leaves cells by osmosis (lower water potential of blood); too low: cells (especially brain) lack glucose for respiration.', '[2]')])
myths(t, [('Insulin breaks down glycogen into glucose.', 'Insulin causes glucose to be converted to glycogen; glucagon causes glycogen to be broken down.'), ('Glucagon and glycogen are the same thing.', 'Glucagon is a hormone; glycogen is a storage carbohydrate.')])


@t.add('C3', (1, 2, 3, 4, 5), 'case')
def glucose_data(r, D):
    base = round(r.uniform(4.5, 5.2), 1)
    peak_n = round(base + r.uniform(2.0, 3.0), 1)
    peak_d = round(base + r.uniform(8, 12), 1)
    tpk = r.choice([30, 45])
    if D == 1:
        return MQ(r, f'After a glucose drink, blood glucose rose to {peak_n} mmol/dm³ in person A and {peak_d} mmol/dm³ in person B. Both started at {base}. Which person is likely to have type 1 diabetes?', 'Person B',
                  ['Person A', 'Both people', 'Neither person', 'It cannot be either'], 'Person B: blood glucose rises much higher because little insulin is made.')
    st = (f'Two people drank a glucose solution. Both had blood glucose of {base} mmol/dm³ at the start. After {tpk} minutes person A had {peak_n} mmol/dm³ and person B had {peak_d} mmol/dm³. After 2 hours person A was back to {base} but person B was still at {round(peak_d - 1.5, 1)}. '
          '(a) Calculate the percentage increase in blood glucose for person B. (b) Suggest which person has type 1 diabetes and explain your answer.')
    ans = f'(a) {fx(pct(base, peak_d), 0)}% (b) Person B: glucose rises much higher and does not return to normal because the pancreas produces little insulin, so the liver does not convert glucose to glycogen.'
    key = f'(a) ({peak_d} − {base}) ÷ {base} × 100 = {fx(pct(base, peak_d), 0)}% [2] (b) person B [1]; little / no insulin [1]; glucose not converted to glycogen [1]'
    m = 5
    if D >= 4:
        st += ' (c) Explain how blood glucose returned to normal in person A.'
        ans += ' (c) The pancreas secreted insulin; the liver (and muscles) converted glucose to glycogen; negative feedback.'
        key += ' (c) insulin [1]; glucose → glycogen in liver [1]'
        m = 7
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def diabetes_case(r, D):
    intro = f'A 12-year-old in {city(r)} has been very thirsty, tired and losing weight. A test shows glucose in the urine and high blood glucose. The doctor diagnoses type 1 diabetes.'
    parts = [lambda r: ('Explain the cause of type 1 diabetes.', 'The insulin-secreting cells of the pancreas are destroyed (by the immune system), so little or no insulin is produced.', '[2]'),
             lambda r: ('Explain why glucose appears in the urine.', 'Blood glucose is so high that more glucose is filtered than can be reabsorbed in the kidney.', '[2]'),
             lambda r: ('Describe how type 1 diabetes is treated.', 'Regular insulin injections (or pump), monitoring blood glucose, controlling carbohydrate intake and exercise.', '[2]'),
             lambda r: ('Describe the role of glucagon when blood glucose falls during exercise.', 'Pancreas secretes glucagon; liver breaks glycogen down to glucose, raising blood glucose.', '[2]'),
             lambda r: ('Explain why the child is losing weight.', 'Without insulin cells cannot take up and use glucose well, so fat and protein are respired instead.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the concentration of glucose in the blood is controlled by negative feedback.', 'Set point; rise detected by pancreas → insulin → liver and muscles take up glucose and convert to glycogen → falls. Fall detected → glucagon → liver breaks glycogen to glucose → rises. Responses reverse the change.',
           'set point / negative feedback [1]; insulin route [2]; glucagon route [2]; liver role [1] [6]')])
t13c = t

t = T('Control of body temperature: skin, sweating, vasodilation and vasoconstriction', 'control of body temperature', 'sweating', 'vasodilation and vasoconstriction')
facts(t, [('vasodilation', 'widening of arterioles supplying skin capillaries, so more blood flows near the surface and more heat is lost'), ('vasoconstriction', 'narrowing of arterioles supplying skin capillaries, reducing blood flow near the surface to reduce heat loss'),
          ('sweating', 'secretion of sweat by sweat glands; evaporation of sweat from the skin removes heat'), ('shivering', 'rapid involuntary contraction of muscles that releases heat by respiration'),
          ('hypothalamus', 'the part of the brain that monitors blood temperature and coordinates temperature control')])
mcqs(t, [('How does sweating cool the body?', 'Evaporation of water from sweat removes heat from the skin', 'Latent heat for evaporation comes from the body.', ['Sweat is cold', 'Sweat reflects sunlight', 'Sweating reduces blood flow']),
         ('What happens to skin arterioles when the body is too cold?', 'They constrict (vasoconstriction)', 'Less blood flows near the surface, so less heat is lost by radiation.', ['They dilate', 'They burst', 'They fill with sweat']),
         ('Which part of the brain controls body temperature?', 'Hypothalamus', 'The hypothalamus detects blood temperature and coordinates responses.', ['Cerebellum', 'Medulla', 'Spinal cord'])])
shorts(t, [('State three responses of the body to a fall in core temperature.', 'Vasoconstriction; shivering; reduced sweating; hairs raised (goose bumps).', 'any three [3]'), ('State the normal core body temperature of humans.', 'About 37 °C.', '[1]')])
explain(t, [('Explain how vasodilation helps to cool the body.', 'Arterioles supplying skin capillaries widen, so more blood flows close to the skin surface and more heat is lost by radiation.', 'arterioles widen [1]; more blood near surface [1]; more heat lost [1] [3]'),
            ('Explain why it is harder to keep cool in humid weather.', 'Sweat evaporates more slowly when the air already contains much water vapour, so less heat is removed.', '[2]'),
            ('Explain how shivering warms the body.', 'Rapid muscle contractions increase respiration, which releases energy as heat.', '[2]'),
            ('Explain why a layer of fat under the skin helps animals in cold climates.', 'Fat is a good insulator and reduces heat loss from the body.', '[2]'),
            ('Explain why temperature control is an example of negative feedback.', 'A change from 37 °C is detected by the hypothalamus, which triggers responses that reverse the change and return temperature to the set point.', '[2]')])
myths(t, [('Blood vessels move closer to the skin surface when we are hot.', 'Blood vessels do not move; arterioles dilate so more blood flows through capillaries near the surface.'), ('Sweat cools us because it is colder than the skin.', 'Sweat cools by evaporation, which removes heat from the skin.')])

COOL = {'setup': lambda r, p: f'{p} filled identical test tubes with water at 70 °C, wrapped them in different numbers of layers of cotton wool (as a model of fat or fur insulation) and measured the temperature drop over 10 minutes.',
        'iv': ('number of layers of insulation', ''), 'xs': lambda r: [0, 1, 2, 3, 4], 'dv': ('temperature drop', '°C'), 'y': lambda x, k: k * (6 + 18 * math.exp(-x / 1.4)), 'dp': 1,
        'controls': ['starting temperature of water', 'volume of water', 'size of test tube', 'room temperature', 'type of insulating material'],
        'why': ('More layers trap more air, a poor conductor, so less heat is lost by conduction and convection; this models how fat and fur reduce heat loss in animals.', 'trapped air / insulation [1]; less heat lost [1]; link to fat or fur [1] [3]'),
        'improve': ['use a lid on each tube to reduce heat loss from the top', 'use a data logger to record temperatures continuously'],
        'xfmt': lambda v: f'{v} layers', 'prep': 'with'}
add_practical(t, COOL, C3D=(2, 3, 4), C4D=(3, 4, 5))


@t.add('C3', (2, 3, 4, 5), 'case')
def temp_data(r, D):
    core = [37.0, 37.1, 37.3, 37.4, 37.2]
    skin0 = round(r.uniform(31, 33), 1)
    skin = [skin0, round(skin0 + 1.2, 1), round(skin0 + 2.3, 1), round(skin0 + 3.0, 1), round(skin0 + 2.0, 1)]
    sw = [0, r.randrange(5, 12), r.randrange(15, 30), r.randrange(30, 45), r.randrange(10, 20)]
    tab = '; '.join(f'{i * 10} min: core {c} °C, skin {s} °C, sweat {w} g' for i, (c, s, w) in enumerate(zip(core, skin, sw)))
    st = f'A cyclist exercised for 30 minutes and then rested. Data: {tab}. (a) Describe the changes in skin temperature. (b) Explain why skin temperature rose although core temperature changed very little.'
    ans = f'(a) Skin temperature rose from {skin[0]} to {skin[3]} °C during exercise then fell to {skin[4]} °C during rest. (b) Vasodilation: more blood flows through skin capillaries, so skin warms and loses heat; sweating cools by evaporation, keeping core temperature close to 37 °C.'
    key = '(a) rise then fall with data [2] (b) vasodilation / more blood to skin [1]; heat lost from skin [1]; sweating [1]'
    m = 5
    if D >= 4:
        st += ' (c) Calculate the rate of sweat production between 0 and 30 minutes, in g per minute.'
        ans += f' (c) {fx(sw[3] / 30, 2)} g/min'
        key += f' (c) {sw[3]} ÷ 30 = {fx(sw[3] / 30, 2)} [1]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def tempc_case(r, D):
    intro = f'A hiker in the mountains near {city(r)} is caught in a snowstorm. Her core body temperature begins to fall.'
    parts = [lambda r: ('Name the part of the brain that detects the fall in blood temperature.', 'Hypothalamus.', '[1]'),
             lambda r: ('Describe and explain three responses that reduce heat loss or increase heat production.', 'Vasoconstriction reduces blood flow to skin (less heat lost); shivering increases respiration and heat release; sweating stops; hairs stand up to trap air.', 'three responses with explanations [3] [3]'),
             lambda r: ('Explain why these responses are an example of negative feedback.', 'The change (fall in temperature) triggers responses that reverse it, returning to the set point.', '[2]'),
             lambda r: ('Suggest why the hiker\'s fingers and toes may suffer damage first.', 'Vasoconstriction reduces blood supply to extremities, which have a large surface area to volume ratio and lose heat fastest.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


longs(t, [('Describe how the skin is involved in maintaining a constant body temperature when the body is too hot and too cold.', 'Too hot: vasodilation of arterioles, more blood near surface, heat lost by radiation; sweat glands secrete sweat, evaporation cools; hairs lie flat. Too cold: vasoconstriction; no sweating; shivering; hairs raised; fat insulation. Hypothalamus coordinates; negative feedback.',
           'too hot two points [2]; too cold two points [2]; hypothalamus / negative feedback [1]; explanation of heat loss mechanism [1] [6]')])
t13d = t
CHAPTERS[3] = [t13a, t13b, t13c, t13d]


# ===================================================================== 4 Reproduction in plants
t = T('Asexual and sexual reproduction: advantages and disadvantages', 'asexual and sexual reproduction', 'advantages and disadvantages')
facts(t, [('asexual reproduction', 'a process resulting in the production of genetically identical offspring from one parent'), ('sexual reproduction', 'a process involving the fusion of the nuclei of two gametes to form a zygote and the production of offspring that are genetically different from each other'),
          ('gamete', 'a sex cell, such as a sperm, egg, pollen nucleus or ovule nucleus, with a haploid nucleus'), ('zygote', 'the diploid cell formed when two gametes fuse at fertilisation'), ('clone', 'a genetically identical copy of an organism')])
mcqs(t, [('Which is an advantage of asexual reproduction?', 'Only one parent is needed and it is fast', 'No need to find a mate or pollinator; many offspring quickly.', ['Offspring show variation', 'It helps species adapt to change', 'Seeds are dispersed widely']),
         ('Which is an example of asexual reproduction in plants?', 'Potato tubers forming new plants', 'Tubers, runners and bulbs are asexual.', ['Pollination of a sunflower', 'Fertilisation in an ovule', 'Seed formation in a bean']),
         ('Why can sexual reproduction help a species survive environmental change?', 'Offspring are genetically varied, so some may be adapted to new conditions', 'Variation allows natural selection.', ['All offspring are identical', 'It needs only one parent', 'It is faster than asexual reproduction'])])
shorts(t, [('State two disadvantages of asexual reproduction.', 'No variation, so a disease or environmental change can kill all individuals; offspring may compete for resources near the parent.', '[2]'), ('State two disadvantages of sexual reproduction.', 'Needs two parents / pollinators; slower; uses more energy (flowers, nectar).', '[2]')])
explain(t, [('Explain why farmers often grow crops such as bananas from cuttings rather than seeds.', 'Cuttings produce clones with the same desirable characteristics (e.g. yield, taste); it is quick and reliable.', '[2]'),
            ('Explain why a field of genetically identical plants is at risk from a new disease.', 'If one plant is susceptible, all are, since there is no genetic variation; the disease could destroy the whole crop.', '[2]'),
            ('Explain why offspring from sexual reproduction are genetically different from each other.', 'Gametes are produced by meiosis, giving different combinations of alleles, and fertilisation combines alleles from two parents randomly.', '[2]')])
myths(t, [('Asexual reproduction involves fertilisation of an egg by one parent.', 'Asexual reproduction involves no gametes or fertilisation.'), ('All offspring from sexual reproduction are identical to one parent.', 'Sexual reproduction produces genetically varied offspring.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def repro_type(r, D):
    cases = [('a strawberry plant producing runners', 'asexual'), ('a spider plant producing plantlets', 'asexual'), ('a gardener growing a geranium from a cutting', 'asexual'), ('a potato tuber growing new shoots', 'asexual'),
             ('an onion bulb producing new bulbs', 'asexual'), ('bees carrying pollen between apple flowers and seeds forming', 'sexual'), ('a maize plant producing grains after wind pollination', 'sexual'), ('bacteria dividing by binary fission', 'asexual'),
             ('a bean plant producing seeds in pods', 'sexual')]
    x, k = r.choice(cases)
    if D <= 2:
        return MQ(r, f'Which type of reproduction is shown by {x}?', k, ['asexual', 'sexual', 'both', 'neither'], f'{cap(x)}: {k} reproduction.')
    return Q(f'{cap(x)}. (a) State the type of reproduction. (b) Give one advantage and one disadvantage of this type of reproduction for the plant.', f'(a) {k} (b) ' + ('advantage: fast, one parent, offspring keep good features; disadvantage: no variation / vulnerable to disease.' if k == 'asexual' else 'advantage: variation, adaptation to change, seed dispersal; disadvantage: needs pollinators / slower / more energy.'),
             f'(a) {k} [1] (b) advantage [1]; disadvantage [1] [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def repro_case(r, D):
    crop = r.choice(['banana', 'cassava', 'potato', 'sugar cane'])
    intro = f'In a region near {city(r)}, most farmers grow the same variety of {crop}, propagated asexually from cuttings. A new fungal disease has started to spread.'
    parts = [lambda r: ('Explain why asexual propagation is popular with farmers.', 'Quick; offspring identical, so they keep high yield and quality; no pollination needed.', '[2]'),
             lambda r: ('Explain why the new disease is a serious threat.', 'All plants are genetically identical so none has resistance; disease can spread through the whole crop.', '[2]'),
             lambda r: ('Suggest how scientists could use sexual reproduction to help.', 'Cross-breed varieties to produce varied offspring and select those resistant to the disease.', '[2]'),
             lambda r: ('Evaluate the use of asexual reproduction for this crop.', 'Advantages: uniform, fast, reliable. Disadvantages: no variation, vulnerable to disease and climate change. Best to keep a variety of strains / use sexual breeding to introduce resistance.', 'advantage [1]; disadvantage [1]; conclusion [1] [3]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t14a = t

FLOWER = [('sepal', 'protects the flower bud'), ('petal', 'often brightly coloured and scented to attract insects'), ('anther', 'produces pollen'), ('filament', 'supports the anther'),
          ('stigma', 'receives pollen during pollination'), ('style', 'connects the stigma to the ovary; the pollen tube grows down it'), ('ovary', 'contains ovules and develops into the fruit'), ('ovule', 'contains the female gamete and develops into the seed')]
POLL = {'insect': ['large, brightly coloured petals', 'scent and nectar', 'anthers inside the flower', 'stigma inside the flower, sticky', 'small amounts of large, sticky or spiky pollen'],
        'wind': ['small, dull or no petals', 'no scent or nectar', 'anthers hanging outside the flower on long filaments', 'large feathery stigmas outside the flower', 'large amounts of small, light, smooth pollen']}
t = T('Flower structure; insect- and wind-pollination', 'flower structure', 'insect- and wind-pollination')
facts(t, FLOWER[:6] + [('pollination', 'the transfer of pollen grains from an anther to a stigma'), ('self-pollination', 'the transfer of pollen from an anther to a stigma of the same flower or another flower on the same plant'),
                       ('cross-pollination', 'the transfer of pollen from an anther of a flower to the stigma of a flower on a different plant of the same species')])
mcqs(t, [('Which feature is typical of a wind-pollinated flower?', 'Feathery stigmas outside the flower', 'Feathery stigmas catch pollen from the air.', ['Brightly coloured petals', 'Nectar', 'Sticky pollen']),
         ('Which parts make up the stamen?', 'Anther and filament', 'Stamen = male part; carpel = stigma, style, ovary.', ['Stigma and style', 'Ovary and ovule', 'Sepal and petal']),
         ('Why do wind-pollinated plants produce large amounts of pollen?', 'Most pollen is lost because it is carried randomly by the wind', 'Very little reaches a stigma.', ['Insects eat most of it', 'Pollen is heavy', 'It attracts insects'])])
shorts(t, [('Name the parts of the carpel.', 'Stigma, style, ovary (containing ovules).', '[2]'), ('State one advantage of cross-pollination over self-pollination.', 'More genetic variation in offspring.', '[1]')])
explain(t, [('Explain how the structure of an insect-pollinated flower is adapted to pollination.', 'Bright petals and scent attract insects; nectar is a reward; anthers and sticky stigma positioned so the insect brushes against them; sticky/spiky pollen sticks to insects.', 'attraction [1]; positions of anther/stigma [1]; pollen type [1] [3]'),
            ('Explain why grasses do not have brightly coloured petals.', 'They are wind-pollinated, so they do not need to attract insects; energy is saved.', '[2]'),
            ('Explain why self-pollination may be a disadvantage to a species.', 'Less genetic variation, so the population is less able to adapt to changes such as new diseases.', '[2]')])
myths(t, [('Pollination is the same as fertilisation.', 'Pollination is the transfer of pollen; fertilisation is the fusion of the pollen nucleus with the ovule nucleus.'), ('Wind-pollinated flowers have nectar to attract the wind.', 'Wind-pollinated flowers have no nectar or scent; they have exposed anthers and feathery stigmas.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def poll_id(r, D):
    k = r.choice(['insect', 'wind'])
    fs = r.sample(POLL[k], 3)
    if D <= 2:
        ans = 'by insects' if k == 'insect' else 'by wind'
        return MQ(r, f'A flower has {", ".join(fs)}. How is it pollinated?', ans, ['by insects', 'by wind', 'by water', 'by self-fertilisation only'], f'{"; ".join(POLL[k])} → {k}-pollinated.')
    other = 'wind' if k == 'insect' else 'insect'
    return Q(f'A plant found near {city(r)} has flowers with {", ".join(fs)}. (a) Suggest how the flower is pollinated. (b) Explain how two of these features help pollination. (c) Describe how the anthers would differ in a flower pollinated by {"wind" if other == "wind" else "insects"}.',
             f'(a) {k} pollination (b) ' + ('features attract insects / pollen sticks to insect' if k == 'insect' else 'pollen is blown easily / stigmas catch airborne pollen') + f' (c) {POLL[other][2]}',
             f'(a) {k} [1] (b) two features explained [2] (c) {POLL[other][2]} [1] [4]', 'short', 4)


@t.add('C3', (1, 2, 3), 'short')
def flower_part(r, D):
    a, b = r.choice(FLOWER)
    if D <= 2:
        return MQ(r, f'Which part of a flower {b}?', a, [x[0] for x in FLOWER if x[0] != a], f'{cap(a)}: {b}.')
    xs = r.sample(FLOWER, 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('State the function of each part of a flower: ' + ', '.join(f'{labs[i]} {x[0]}' for i, x in enumerate(xs)) + '.', ' '.join(f'{labs[i]} {x[1]}' for i, x in enumerate(xs)), '; '.join(f'{labs[i]} [1]' for i, _ in enumerate(xs)) + ' [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def pollen_count(r, D):
    a = r.randrange(200, 900)
    w = round(a * r.uniform(15, 250), -2)
    st = f'Scientists counted pollen grains produced per anther: an insect-pollinated flower produced {big(a)} and a wind-pollinated grass produced {big(w)}. Calculate how many times more pollen the grass produced, and explain the difference.'
    return Q(st, f'{fx(w / a, 0)} times; wind pollination is random, so most pollen never reaches a stigma; insects carry pollen directly between flowers.', f'{big(w)} ÷ {big(a)} = {fx(w / a, 0)} [1]; random dispersal / most lost [1]; insects more targeted [1] [3]', 'numerical', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def flower_case(r, D):
    a, b = r.choice(['hibiscus', 'sunflower', 'orchid', 'mango']), r.choice(['maize', 'rice', 'grass', 'wheat'])
    if r.random() < 0.5:
        a, b = b, a
    ka = 'wind' if a in ('maize', 'rice', 'grass', 'wheat') else 'insect'
    kb = 'wind' if b in ('maize', 'rice', 'grass', 'wheat') else 'insect'
    intro = f'A student compares flowers of {a} ({ka}-pollinated) and {b} ({kb}-pollinated).'
    parts = [lambda r: (f'Describe two features you would expect to see in the {a} flower.', '; '.join(POLL[ka][:2]) + '.', '[2]'),
             lambda r: (f'Explain how the stigma of the {b} flower is adapted.', POLL[kb][3] + ('— catches pollen from the air.' if kb == 'wind' else '— pollen sticks to it when insects brush past.'), '[2]'),
             lambda r: ('Distinguish between self-pollination and cross-pollination.', 'Self: pollen to stigma of same flower / same plant. Cross: pollen to stigma of a different plant of the same species.', '[2]'),
             lambda r: ('Describe what happens after a pollen grain lands on a compatible stigma.', 'A pollen tube grows down the style to the ovule; the male nucleus travels down and fuses with the female nucleus (fertilisation).', '[3]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


longs(t, [('Compare the structure of insect-pollinated and wind-pollinated flowers, explaining how each is adapted to its method of pollination.', 'Insect: large bright petals, scent, nectar, anthers/stigma inside, sticky stigma, small amount of sticky/spiky pollen. Wind: small/no petals, no scent/nectar, anthers hang outside, feathery stigma outside, large amounts of light smooth pollen.',
           'three comparisons [3]; explanations linked to pollination [2] [5]')])
t14b = t

t = T('Fertilisation, seed formation and conditions for germination', 'fertilisation, seed formation', 'conditions for germination')
facts(t, [('fertilisation', 'the fusion of the nuclei of a male gamete and a female gamete'), ('germination', 'the start of growth of a seed into a seedling'), ('pollen tube', 'a tube that grows from a pollen grain down the style to carry the male nucleus to the ovule'),
          ('seed', 'a structure that develops from a fertilised ovule, containing an embryo and a food store'), ('fruit', 'a structure that develops from the ovary after fertilisation and contains seeds')])
mcqs(t, [('Which conditions are needed for germination?', 'Water, oxygen and a suitable temperature', 'Light is not needed for most seeds to germinate.', ['Light, carbon dioxide and soil', 'Light only', 'Fertiliser and light']),
         ('After fertilisation, what does the ovule develop into?', 'Seed', 'Ovule → seed; ovary → fruit.', ['Fruit', 'Petal', 'Anther']),
         ('Why do seeds need oxygen to germinate?', 'For aerobic respiration to release energy for growth', 'Germinating seeds respire rapidly.', ['For photosynthesis', 'To soften the seed coat', 'To make chlorophyll'])])
shorts(t, [('State the role of water in germination.', 'Activates enzymes and allows the seed to swell; transports dissolved food to the embryo.', '[2]'), ('Describe how a pollen nucleus reaches the ovule.', 'A pollen tube grows from the pollen grain down through the style into the ovary and through the micropyle into the ovule.', '[2]')])
explain(t, [('Explain why seeds do not germinate in very cold soil.', 'Enzymes that break down food stores and control respiration work very slowly at low temperature.', '[2]'),
            ('Explain why seeds sown in waterlogged soil may not germinate.', 'Water fills the air spaces, so there is too little oxygen for aerobic respiration.', '[2]'),
            ('Explain why a seed needs a food store.', 'The embryo cannot photosynthesise until leaves are above ground; the food store provides energy (by respiration) and materials for growth.', '[2]')])
myths(t, [('Seeds need light to germinate.', 'Most seeds germinate in the dark; they need water, oxygen and a suitable temperature.'), ('The fruit develops from the petals.', 'The fruit develops from the ovary wall.')])

GERM = {'setup': lambda r, p: f'{p} placed 20 cress seeds on damp cotton wool in each of several dishes at different temperatures and counted the number that germinated after 5 days.',
        'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[5, 10, 15, 20, 25, 30], [0, 10, 20, 30, 40], [10, 15, 20, 25, 30, 35]]), 'dv': ('number of seeds germinated', ''),
        'y': lambda x, k: max(0, 19 * math.exp(-((x - 24 * k) ** 2) / 200)), 'dp': 0, 'noise': 0.04, 'neg': True,
        'controls': ['number and type of seeds', 'volume of water', 'light conditions', 'time allowed'],
        'why': ('Germination is controlled by enzymes; as temperature rises enzymes work faster up to an optimum; at high temperatures enzymes are denatured; at very low temperatures enzymes work too slowly.', 'enzymes [1]; optimum [1]; denaturation / slow at low temperature [1] [3]'),
        'improve': ['use more seeds in each dish', 'keep each dish in an incubator at the exact temperature'],
        'extra': [lambda r, d: ('Calculate the mean percentage germination at the temperature with the highest mean number of seeds germinated.', f'{fx(max(d["means"]) / 20 * 100, 1)}%', f'{fx(max(d["means"]), 2)} ÷ 20 [1] × 100 = {fx(max(d["means"]) / 20 * 100, 1)}% [1] [2]')]}
add_practical(t, GERM, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'case')
def germ_cond(r, D):
    tubes = [('A', 'dry cotton wool, 20 °C, air', 'no', 'no water'), ('B', 'damp cotton wool, 20 °C, air', 'yes', 'water, oxygen and suitable temperature'),
             ('C', 'damp cotton wool, 4 °C (fridge), air', 'no (or very few)', 'too cold for enzymes'), ('D', 'boiled water with oil layer, 20 °C', 'no', 'no oxygen'),
             ('E', 'damp cotton wool, 20 °C, in darkness', 'yes', 'light not needed for germination')]
    pick = sorted(r.sample(tubes, 3 if D <= 2 else 4))
    st = 'Bean seeds were set up in tubes: ' + '; '.join(f'tube {a}: {b}' for a, b, _, _ in pick) + '.'
    if D == 1:
        a, b, g, why = pick[0]
        return MQ(r, st + f' Would the seeds in tube {a} germinate?', g, ['yes', 'no', 'no (or very few)', 'only in light'], f'Tube {a}: {g} — {why}.')
    return Q(st + ' Predict whether the seeds in each tube germinate, and explain each prediction.', '; '.join(f'{a}: {g} — {why}' for a, _, g, why in pick), '; '.join(f'{a} [1]' for a, _, _, _ in pick) + f'; reasons [{len(pick)}] [{2 * len(pick)}]'.replace(f'; reasons [{len(pick)}] [', f'; reasons, 1 each [{len(pick)}] ['), 'case', 2 * len(pick))


@t.add('C4', (3, 4, 5), 'multi_step')
def fert_case(r, D):
    nov = r.choice([8, 10, 12, 15, 20])
    nseed = r.randrange(nov // 2, nov)
    intro = f'A pea flower ovary contains {nov} ovules. After pollination, the pod develops {nseed} seeds.'
    parts = [lambda r: ('Calculate the percentage of ovules that were fertilised.', f'{fx(nseed / nov * 100, 1)}%', f'{nseed} ÷ {nov} × 100 [1] = {fx(nseed / nov * 100, 1)}% [1] [2]'),
             lambda r: ('Describe how fertilisation occurs in a flower.', 'Pollen grain on stigma grows a pollen tube down the style to an ovule; male nucleus passes down the tube and fuses with the female nucleus in the ovule.', '[3]'),
             lambda r: ('Suggest why not all the ovules became seeds.', 'Not enough pollen grains landed / some pollen tubes did not reach ovules, so some ovules were not fertilised.', '[1]'),
             lambda r: ('State what the pod (ovary wall) develops into.', 'The fruit.', '[1]'),
             lambda r: ('State the conditions the seeds need to germinate and explain the need for one of them.', 'Water, oxygen, suitable temperature; e.g. oxygen for aerobic respiration to release energy for growth.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t14c = t
CHAPTERS[4] = [t14a, t14b, t14c]

# ===================================================================== 5 Reproduction in humans
MREP = [('testis', 'produces sperm and testosterone'), ('scrotum', 'holds the testes outside the body at a lower temperature'), ('sperm duct', 'carries sperm from the testis to the urethra'),
        ('prostate gland', 'adds fluid containing nutrients to sperm to form semen'), ('urethra', 'carries semen (or urine) out of the body through the penis'),
        ('ovary', 'produces eggs and the hormones oestrogen and progesterone'), ('oviduct', 'carries the egg to the uterus; site of fertilisation'), ('uterus', 'where the fetus develops'),
        ('cervix', 'ring of muscle at the base of the uterus'), ('vagina', 'receives sperm during intercourse; birth canal')]
t = T('Male and female reproductive systems and gametes', 'male and female reproductive systems', 'gametes')
facts(t, MREP[:8])
mcqs(t, [('Where does fertilisation usually take place in humans?', 'In the oviduct', 'Sperm meet the egg in the oviduct.', ['In the uterus', 'In the ovary', 'In the vagina']),
         ('Which is a correct comparison of sperm and egg cells?', 'Sperm are smaller and made in larger numbers', 'Sperm are small, motile, numerous; eggs are large, non-motile, fewer, with food stores.', ['Eggs can swim, sperm cannot', 'Sperm have a larger food store', 'Eggs are made in larger numbers']),
         ('What is the function of the acrosome of a sperm?', 'It contains enzymes that digest the jelly coat of the egg', 'Enzymes let the sperm head penetrate the egg.', ['It stores food', 'It contains mitochondria', 'It is the flagellum'])])
shorts(t, [('State three adaptations of a sperm cell.', 'Flagellum for swimming; many mitochondria for energy; acrosome with enzymes; haploid nucleus.', 'any three [3]'), ('State two adaptations of an egg cell.', 'Large cytoplasm with energy stores; jelly coat that changes after fertilisation to stop more sperm entering.', '[2]')])
explain(t, [('Explain why the testes are held outside the body in the scrotum.', 'Sperm production needs a temperature slightly lower than core body temperature.', '[2]'),
            ('Explain why many more sperm are produced than eggs.', 'Most sperm die or fail to reach the egg in the female tract, so large numbers increase the chance of fertilisation.', '[2]'),
            ('Explain how the egg is moved along the oviduct.', 'Cilia lining the oviduct beat, and muscles in the wall contract (peristalsis), moving the egg towards the uterus.', '[2]')])
myths(t, [('The egg is fertilised in the uterus.', 'Fertilisation usually happens in the oviduct.'), ('Sperm are produced in the prostate gland.', 'Sperm are produced in the testes; the prostate adds fluid to make semen.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def rep_org(r, D):
    a, b = r.choice(MREP)
    if D <= 2:
        return MQ(r, f'Which structure {b}?', a, [x[0] for x in MREP if x[0] != a], f'{cap(a)}: {b}.')
    xs = r.sample(MREP, 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('State the function of each structure: ' + ', '.join(f'{labs[i]} {x[0]}' for i, x in enumerate(xs)) + '.', ' '.join(f'{labs[i]} {x[1]}' for i, x in enumerate(xs)), '; '.join(f'{labs[i]} [1]' for i in range(3)) + ' [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def gamete_size(r, D):
    egg = r.choice([100, 110, 120, 130])
    sp_head = r.choice([4, 5, 5.5, 6])
    img = r.choice([40, 50, 60])
    M = img * 1000 / egg
    st = f'A human egg cell has a diameter of {egg} μm and a sperm head is {sp_head} μm long. (a) Calculate how many times wider the egg is than the sperm head. (b) A photograph shows the egg {img} mm wide. Calculate the magnification of the photograph.'
    return Q(st, f'(a) {fx(egg / sp_head, 1)} times (b) ×{fx(M, 0)}', f'(a) {egg} ÷ {sp_head} = {fx(egg / sp_head, 1)} [1] (b) {img} mm = {img * 1000} μm [1]; {img * 1000} ÷ {egg} = ×{fx(M, 0)} [1] [3]', 'numerical', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def gamete_case(r, D):
    intro = 'An electron micrograph shows a human sperm cell and part of an egg cell.'
    parts = [lambda r: ('Compare sperm and egg cells in terms of size, number produced and mobility.', 'Sperm: small, millions produced, swim with flagellum. Egg: large, one per month, not mobile (moved by cilia).', '[3]'),
             lambda r: ('Explain how the structure of the sperm is adapted for reaching and fertilising the egg.', 'Flagellum for swimming; mitochondria release energy; acrosome enzymes digest jelly coat; streamlined head.', '[3]'),
             lambda r: ('Explain why the egg has a large cytoplasm.', 'It contains energy stores (food) for the early embryo before implantation.', '[2]'),
             lambda r: ('State the number of chromosomes in the nucleus of each gamete and explain why.', '23 (haploid), so that the zygote has 46 (diploid) after fertilisation.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t15a = t

t = T('Fertilisation, implantation and development of the fetus; role of the placenta', 'fertilisation, implantation', 'development of the fetus', 'role of the placenta')
facts(t, [('implantation', 'the embedding of the embryo into the lining of the uterus'), ('placenta', 'the organ through which substances are exchanged between the blood of the mother and fetus'),
          ('umbilical cord', 'the cord containing blood vessels that connects the fetus to the placenta'), ('amniotic fluid', 'the liquid in the amniotic sac that protects the fetus from mechanical shock'),
          ('embryo', 'the ball of cells formed by division of the zygote, which develops into a fetus')])
mcqs(t, [('Which substance passes from the fetus to the mother across the placenta?', 'Urea', 'Wastes (urea, CO₂) pass to the mother; nutrients and oxygen pass to the fetus.', ['Glucose', 'Oxygen', 'Amino acids']),
         ('What is the function of the amniotic fluid?', 'To protect the fetus from mechanical shock', 'It cushions the fetus and allows movement.', ['To supply oxygen', 'To remove urea', 'To produce hormones']),
         ('Why should pregnant women avoid smoking?', 'Nicotine and carbon monoxide cross the placenta and harm fetal development', 'Low birth mass, premature birth.', ['Smoke kills the placenta immediately', 'Smoking improves fetal oxygen', 'It has no effect on the fetus'])])
shorts(t, [('State three substances that pass from mother to fetus across the placenta.', 'Glucose, amino acids, oxygen, water, ions, antibodies.', 'any three [3]'), ('Name two substances that pass from fetus to mother across the placenta.', 'Carbon dioxide and urea.', '[2]')])
explain(t, [('Explain how the placenta is adapted for exchange.', 'It has many villi giving a large surface area, a thin barrier between maternal and fetal blood and a good blood supply, so diffusion is fast.', 'large surface area [1]; thin [1]; blood supply [1] [3]'),
            ('Explain why the blood of the mother and fetus do not mix.', 'They are separated by a thin barrier in the placenta; mixing could cause damage from different blood pressures and blood groups, and pathogens could pass.', '[2]'),
            ('Explain why some viruses, such as rubella, are dangerous in early pregnancy.', 'They can cross the placenta and damage developing organs of the fetus.', '[2]')])
myths(t, [("The mother's blood flows through the fetus's body.", 'The blood systems are separate; substances are exchanged across the placenta.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def fetus_growth(r, D):
    wk = [12, 20, 28, 36, 40]
    mass = [r.randrange(14, 25), r.randrange(280, 360), r.randrange(1000, 1300), r.randrange(2500, 2900), r.randrange(3200, 3600)]
    tab = ', '.join(f'week {w}: {m} g' for w, m in zip(wk, mass))
    i = r.randrange(1, 4)
    gain = (mass[i + 1] - mass[i]) / (wk[i + 1] - wk[i])
    if D == 1:
        return NQ(r, f'A fetus has a mass of {mass[i]} g at week {wk[i]} and {mass[i + 1]} g at week {wk[i + 1]}. What is the mean increase in mass per week?', gain, [mass[i + 1] - mass[i], gain * 2, mass[i + 1] / wk[i + 1], gain / 7], ' g/week', f'({mass[i + 1]} − {mass[i]}) ÷ {wk[i + 1] - wk[i]} = {fx(gain, 1)} g/week.', f=lambda v: fx(v, 1))
    st = f'Mean fetal mass during pregnancy: {tab}. (a) Calculate the mean rate of growth between week {wk[i]} and week {wk[i + 1]}. (b) Calculate the percentage increase in mass between week 28 and week 40.'
    ans = f'(a) {fx(gain, 1)} g per week (b) {fx(pct(mass[2], mass[4]), 0)}%'
    key = f'(a) ({mass[i + 1]} − {mass[i]}) ÷ {wk[i + 1] - wk[i]} = {fx(gain, 1)} [2] (b) ({mass[4]} − {mass[2]}) ÷ {mass[2]} × 100 = {fx(pct(mass[2], mass[4]), 0)}% [2]'
    m = 4
    if D >= 4:
        st += ' (c) Explain how the fetus obtains the materials it needs for this growth.'
        ans += ' (c) Glucose, amino acids, oxygen, ions diffuse from mother\'s blood across the placenta into fetal blood in the umbilical vein.'
        key += ' (c) placenta [1]; diffusion of named nutrients [1]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def preg_case(r, D):
    intro = f'A midwife in {city(r)} explains the early stages of pregnancy to a couple, from fertilisation to the development of the placenta.'
    parts = [lambda r: ('Describe what happens between fertilisation and implantation.', 'Zygote divides by mitosis to form a ball of cells (embryo) as it moves along the oviduct; it embeds in the uterus lining (implantation).', '[3]'),
             lambda r: ('Describe the role of the umbilical cord.', 'Contains blood vessels carrying fetal blood to and from the placenta.', '[2]'),
             lambda r: ('Explain why antibodies crossing the placenta are useful.', 'They give the baby passive immunity to diseases for its first months.', '[2]'),
             lambda r: ('Suggest why alcohol and drugs should be avoided during pregnancy.', 'They cross the placenta and can damage the developing fetus (e.g. brain development, low birth mass).', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t15b = t

t = T('Sex hormones and the menstrual cycle', 'sex hormones', 'menstrual cycle')
facts(t, [('testosterone', 'the male sex hormone, made in the testes, that causes male secondary sexual characteristics'), ('oestrogen', 'a female sex hormone made in the ovaries that causes female secondary sexual characteristics and repairs the uterus lining'),
          ('progesterone', 'a hormone made by the ovary (corpus luteum) that maintains the uterus lining'), ('FSH', 'follicle-stimulating hormone from the pituitary gland that causes an egg to mature in a follicle'),
          ('LH', 'luteinising hormone from the pituitary gland that triggers ovulation'), ('ovulation', 'the release of an egg from an ovary, around day 14 of the cycle'), ('menstruation', 'the breakdown and loss of the uterus lining at the start of the cycle')])
mcqs(t, [('Which hormone triggers ovulation?', 'LH', 'A surge of LH around day 14 causes ovulation.', ['FSH', 'Progesterone', 'Testosterone']),
         ('Which hormone maintains the lining of the uterus after ovulation?', 'Progesterone', 'Progesterone from the corpus luteum keeps the lining thick.', ['FSH', 'LH', 'Testosterone']),
         ('Why does menstruation begin at the end of a cycle with no pregnancy?', 'Progesterone levels fall', 'Without progesterone the lining breaks down.', ['Oestrogen rises sharply', 'LH rises', 'FSH stops being made permanently'])])
shorts(t, [('State two secondary sexual characteristics in females caused by oestrogen.', 'Breast development; widening of hips; start of menstrual cycle; growth of pubic hair.', '[2]'), ('State two secondary sexual characteristics in males caused by testosterone.', 'Growth of facial / body hair; deepening voice; increased muscle; testes start producing sperm.', '[2]')])
explain(t, [('Explain why the lining of the uterus thickens before ovulation.', 'Oestrogen causes the lining to repair and thicken so that it is ready for an embryo to implant.', '[2]'),
            ('Explain why progesterone levels stay high if pregnancy occurs.', 'Progesterone maintains the uterus lining so the embryo can stay implanted; later the placenta produces progesterone.', '[2]'),
            ('Explain how FSH and oestrogen interact in the menstrual cycle.', 'FSH causes a follicle to mature and produce oestrogen; rising oestrogen inhibits FSH production and stimulates LH.', '[2]')])
myths(t, [('Ovulation happens during menstruation.', 'Ovulation usually happens around day 14, about halfway through the cycle.'), ('FSH is made in the ovaries.', 'FSH is made in the pituitary gland.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def cycle_q(r, D):
    L = r.choice([26, 28, 30, 32])
    start = r.choice([1, 3, 5, 8, 12])
    ov = L - 14
    stage = r.choice([('day 1 to 5', 'menstruation: the uterus lining breaks down and is lost'), (f'day 6 to {ov - 1}', 'the uterus lining repairs and thickens (oestrogen); a follicle matures (FSH)'),
                      (f'day {ov}', 'ovulation (LH surge)'), (f'day {ov + 1} to {L}', 'progesterone maintains the thick lining')])
    if D <= 2:
        return MQ(r, f'In a {L}-day menstrual cycle, what happens around {stage[0]}?', stage[1], ['menstruation: the uterus lining breaks down and is lost', 'the uterus lining repairs and thickens (oestrogen); a follicle matures (FSH)', 'ovulation (LH surge)', 'progesterone maintains the thick lining', 'implantation always occurs'],
                  f'{L}-day cycle: ovulation about day {ov} (14 days before the next period).')
    def dt(n):
        return f'{n} June' if n <= 30 else f'{n - 30} July'
    o_d, n_d = start + ov - 1, start + L
    return Q(f'A woman has a regular {L}-day cycle. Her period started on {dt(start)}. (a) Predict the date of her next ovulation. (b) Predict the date her next period starts. (c) Name the hormone that triggers ovulation and the gland that produces it.',
             f'(a) {dt(o_d)} (b) {dt(n_d)} (c) LH; pituitary gland', f'(a) ovulation about 14 days before the next period, i.e. cycle day {ov} → {dt(o_d)} [1] (b) {start} June + {L} days → {dt(n_d)} [1] (c) LH [1]; pituitary [1] [4]', 'short', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def cycle_case(r, D):
    intro = 'A graph shows the concentrations of FSH, LH, oestrogen and progesterone in the blood during a 28-day menstrual cycle in which no pregnancy occurs.'
    parts = [lambda r: ('Describe the changes in progesterone concentration during the cycle and explain their effect.', 'Low in first half; rises after ovulation (from corpus luteum) to a peak around day 21; falls before day 28, causing menstruation.', '[3]'),
             lambda r: ('State the day on which ovulation is most likely and the hormone surge that causes it.', 'Around day 14; LH.', '[2]'),
             lambda r: ('Explain why FSH concentration is high at the start of the cycle.', 'To stimulate a follicle in the ovary to mature an egg and produce oestrogen.', '[2]'),
             lambda r: ('Explain why oestrogen concentration rises between day 5 and day 13.', 'The developing follicle secretes oestrogen, which repairs and thickens the uterus lining.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


longs(t, [('Describe the roles of FSH, LH, oestrogen and progesterone in the menstrual cycle.', 'FSH (pituitary): follicle matures, stimulates oestrogen. Oestrogen (ovary): thickens lining, inhibits FSH, stimulates LH. LH (pituitary): ovulation ~day 14, corpus luteum forms. Progesterone (corpus luteum): maintains lining; falls → menstruation.',
           'one role each [4]; sources [1]; feedback / sequence [1] [6]')])
t15c = t

t = T('Sexually transmitted infections: HIV and its control', 'sexually transmitted infections', 'hiv and its control')
facts(t, [('sexually transmitted infection', 'an infection transmitted through sexual contact'), ('HIV', 'human immunodeficiency virus, which infects and destroys lymphocytes and can lead to AIDS'),
          ('AIDS', 'acquired immune deficiency syndrome: the stage of HIV infection when the immune system is so weakened that other infections develop'), ('lymphocyte', 'a white blood cell that produces antibodies; the main target of HIV')])
mcqs(t, [('How does HIV weaken the immune system?', 'It destroys lymphocytes', 'Fewer lymphocytes means fewer antibodies against other pathogens.', ['It destroys red blood cells', 'It blocks the trachea', 'It digests platelets']),
         ('Which is a method of reducing the spread of HIV?', 'Using condoms during sexual intercourse', 'Barrier contraception prevents contact with body fluids.', ['Taking antibiotics', 'Using mosquito nets', 'Avoiding shaking hands']),
         ('How can HIV be transmitted?', 'By sharing needles used to inject drugs', 'HIV is spread in blood and other body fluids.', ['By kissing on the cheek', 'By sharing cups', 'By mosquito bites'])])
shorts(t, [('State three ways in which HIV can be transmitted.', 'Unprotected sexual intercourse; sharing needles; infected blood transfusion; mother to baby (placenta, birth, breast milk).', 'any three [3]'), ('State why antibiotics cannot cure HIV.', 'HIV is a virus; antibiotics only act on bacteria.', '[1]')])
explain(t, [('Explain why people with AIDS often die from infections that are not usually serious.', 'HIV destroys lymphocytes, so few antibodies are made; the body cannot fight pathogens such as TB or pneumonia.', '[2]'),
            ('Explain how screening donated blood reduces HIV infections.', 'Infected blood is detected and discarded, so HIV is not transmitted in transfusions.', '[2]'),
            ('Explain why treating pregnant women who have HIV with antiviral drugs protects their babies.', 'The drugs reduce the amount of virus in the blood, lowering the chance of HIV crossing the placenta or passing during birth.', '[2]')])
myths(t, [('HIV can be spread by sharing cups and towels.', 'HIV is spread by blood and sexual fluids, not by casual contact.'), ('HIV and AIDS are the same thing.', 'HIV is the virus; AIDS is the condition that develops when the immune system is badly damaged.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def hiv_data(r, D):
    y0 = r.randrange(40000, 90000)
    y1 = round(y0 * r.uniform(0.3, 0.7))
    yr = r.choice([2005, 2008, 2010])
    pc = (y0 - y1) / y0 * 100
    if D == 1:
        return NQ(r, f'New HIV infections in a country fell from {big(y0)} to {big(y1)}. What was the percentage decrease?', pc, [y1 / y0 * 100, (y0 - y1) / y1 * 100, pc / 2, 100 - pc / 2], '%', f'({y0} − {y1}) ÷ {y0} × 100 = {fx(pc, 1)}%.', f=lambda v: fx(v, 1))
    st = f'In a country, new HIV infections fell from {big(y0)} in {yr} to {big(y1)} in {yr + 10}. (a) Calculate the percentage decrease. (b) Suggest two measures that could have caused this decrease.'
    return Q(st, f'(a) {fx(pc, 1)}% (b) e.g. condom distribution, education, needle exchange schemes, blood screening, antiviral drugs for pregnant women.', f'(a) ({y0} − {y1}) ÷ {y0} × 100 = {fx(pc, 1)}% [2] (b) two measures [2] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def hiv_case(r, D):
    intro = f'A health clinic in {city(r)} runs a programme to reduce the spread of HIV.'
    parts = [lambda r: ('Describe how HIV affects the body.', 'Infects and destroys lymphocytes, so fewer antibodies are made; the immune system weakens; other infections develop (AIDS).', '[3]'),
             lambda r: ('Suggest three ways the clinic could reduce transmission.', 'Free condoms; education; HIV testing; needle exchange; antiviral treatment.', '[3]'),
             lambda r: ('Explain why HIV testing is important even for people with no symptoms.', 'People can be infected for years without symptoms and pass on the virus; early treatment slows progression.', '[2]'),
             lambda r: ('Explain why there is still no simple vaccine for HIV.', 'The virus changes its antigens (mutates) rapidly and attacks the immune cells that vaccines rely on.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t15d = t
CHAPTERS[5] = [t15a, t15b, t15c, t15d]


# ===================================================================== 6 Inheritance
CHROM = [('human', 46), ('dog', 78), ('cat', 38), ('horse', 64), ('fruit fly', 8), ('potato', 48), ('onion', 16), ('chimpanzee', 48), ('rice', 24), ('maize', 20), ('chicken', 78), ('pea', 14)]
t = T('Chromosomes, genes and alleles; sex inheritance', 'chromosomes, genes and alleles', 'sex inheritance')
facts(t, [('chromosome', 'a thread-like structure of DNA, carrying genetic information in the form of genes'), ('gene', 'a length of DNA that codes for a protein'),
          ('allele', 'an alternative form of a gene'), ('inheritance', 'the transmission of genetic information from generation to generation'), ('sex chromosomes', 'the X and Y chromosomes, which determine sex: XX female, XY male')])
mcqs(t, [('What is the chance that a human baby will be a boy?', '50%', 'Mother gives X; father gives X or Y with equal probability.', ['25%', '75%', '100%']),
         ('Which parent determines the sex of a human child?', 'The father', 'Sperm carry either X or Y; eggs always carry X.', ['The mother', 'Both equally', 'Neither, it is random in the zygote']),
         ('What is the relationship between a gene and an allele?', 'An allele is one version of a gene', 'Genes can have different alleles, e.g. for eye colour.', ['A gene is part of an allele', 'They are the same thing', 'Alleles are found only in gametes'])])
shorts(t, [('State the sex chromosomes of a human male and a human female.', 'Male XY; female XX.', '[1]'), ('State where chromosomes are found in a cell.', 'In the nucleus.', '[1]')])
explain(t, [('Explain why the proportion of boys and girls born is approximately equal.', 'Half of sperm carry X and half carry Y; all eggs carry X; fertilisation is random, so there is a 1:1 ratio of XX and XY.', 'sperm X or Y in equal numbers [1]; eggs all X [1]; random fertilisation [1] [3]'),
            ('Explain why siblings with the same parents can look different.', 'Each inherits a different combination of alleles from each parent, because gametes differ (meiosis) and fertilisation is random.', '[2]'),
            ('Explain how a gene controls a characteristic such as eye colour.', 'The gene codes for a protein (e.g. an enzyme making pigment); different alleles code for different versions of the protein, giving different colours.', '[2]')])
myths(t, [('The mother determines whether a baby is a boy or a girl.', 'The father determines sex: sperm carry either X or Y.'), ('Each cell contains only one copy of each gene.', 'Body cells contain two copies of each gene (two alleles), one on each chromosome of a pair.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def sex_cross(r, D):
    n = r.choice([3, 4])
    if D == 1:
        return MQ(r, 'Which sex chromosomes are found in a human sperm cell?', 'Either X or Y', ['Always X', 'Always Y', 'XY', 'XX'], 'Sperm are haploid with one sex chromosome: X or Y.')
    st = 'Draw a genetic diagram to show how sex is inherited in humans, and state the probability that a child will be female.'
    if D >= 3:
        st = f'A couple already have {n} daughters. Use a genetic diagram to explain the probability that their next child will be a boy.'
        return Q(st, 'Parents XX × XY; gametes X, X and X, Y; offspring XX, XX, XY, XY; probability of a boy = 0.5 (50%), regardless of previous children.', 'parental genotypes [1]; gametes [1]; offspring [1]; 50% and independent of previous births [1] [4]', 'short', 4)
    return Q(st, 'XX × XY → gametes X, X / X, Y → XX, XX, XY, XY → probability female = 0.5 (50%).', 'parents [1]; gametes [1]; offspring and 50% [1] [3]', 'short', 3)


@t.add('C3', (1, 2, 3), 'short')
def chrom_count(r, D):
    org, n = r.choice(CHROM)
    if D <= 2:
        return NQ(r, f'{"An" if org[0] in "aeiou" else "A"} {org} body cell contains {n} chromosomes. How many chromosomes are in one of its gametes?', n // 2, [n, n * 2, n // 4, n - 2], '', f'Gametes are haploid: {n} ÷ 2 = {n // 2}.', f=lambda v: str(int(v)))
    return Q(f'{"An" if org[0] in "aeiou" else "A"} {org} body cell contains {n} chromosomes. State how many chromosomes are found in (a) a gamete, (b) a zygote, (c) a cell produced by mitosis of a skin cell, and (d) the number of pairs of chromosomes in a body cell.',
             f'(a) {n // 2} (b) {n} (c) {n} (d) {n // 2}', f'(a) {n // 2} (b) {n} (c) {n} (d) {n // 2}; 1 each [4]', 'short', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def chrom_case(r, D):
    intro = f'A genetic counsellor in {city(r)} uses a karyotype (a picture of all the chromosomes from one cell) to explain inheritance to a family.'
    parts = [lambda r: ('State the number of chromosomes in a normal human body cell and how many pairs this is.', '46; 23 pairs.', '[2]'),
             lambda r: ('Explain how you could tell from the karyotype whether the person is male or female.', 'Look at the sex chromosomes: XX female, XY male (Y is much smaller).', '[2]'),
             lambda r: ('Distinguish between the terms gene and allele.', 'A gene is a length of DNA coding for a protein; alleles are alternative forms of a gene.', '[2]'),
             lambda r: ('Explain why each chromosome in a pair can carry different alleles.', 'One chromosome comes from each parent, and the parents may have different alleles of the same gene.', '[2]'),
             lambda r: ('Use a genetic diagram to show the chance of the family having a girl.', 'XX × XY → XX, XX, XY, XY: 50%.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t16a = t

CODON = {'AUG': 'Met', 'UUU': 'Phe', 'GGC': 'Gly', 'GCA': 'Ala', 'UAC': 'Tyr', 'CCG': 'Pro', 'AAA': 'Lys', 'GAU': 'Asp', 'CUG': 'Leu', 'UGG': 'Trp', 'AGC': 'Ser', 'CAU': 'His'}
t = T('Protein synthesis: genetic code, mRNA and ribosomes', 'protein synthesis', 'genetic code, mrna and ribosomes')
facts(t, [('mRNA', 'a messenger molecule that carries a copy of the base sequence of a gene from the nucleus to the ribosome'), ('ribosome', 'the structure in the cytoplasm where amino acids are joined to make a protein'),
          ('genetic code', 'the sequence of bases in DNA, in which each set of three bases codes for one amino acid'), ('codon', 'a sequence of three bases that codes for one amino acid'),
          ('gene expression', 'the use of a gene to make its protein; different cells express different genes')])
mcqs(t, [('Where are proteins assembled in a cell?', 'On ribosomes in the cytoplasm', 'mRNA travels from the nucleus to ribosomes.', ['In the nucleus', 'In the cell membrane', 'In the vacuole']),
         ('How many bases code for one amino acid?', 'Three', 'A triplet of bases (codon) codes for one amino acid.', ['One', 'Two', 'Four']),
         ('Why is mRNA needed in protein synthesis?', 'DNA cannot leave the nucleus, so a copy of the gene is carried to the ribosome', 'mRNA is small enough to pass through nuclear pores.', ['mRNA joins amino acids together', 'mRNA is the protein', 'DNA is too small'])])
shorts(t, [('State the order of events in protein synthesis.', 'Gene copied into mRNA in the nucleus; mRNA moves to a ribosome; ribosome reads the bases and joins amino acids in the coded sequence.', '[3]'), ('State why all body cells contain the same genes but make different proteins.', 'Different genes are switched on (expressed) in different cells.', '[1]')])
explain(t, [('Explain how the sequence of bases in a gene determines the shape of a protein.', 'Each triplet codes for an amino acid, so the base sequence determines the order of amino acids; the order determines how the chain folds and so the shape and function of the protein.', 'triplets → amino acids [1]; order of amino acids [1]; folding / shape [1] [3]'),
            ('Explain how a change in one base of a gene could affect an enzyme.', 'It may change one amino acid, altering the folding and the shape of the active site so that the substrate no longer fits.', '[2]'),
            ('Explain why a nerve cell and a muscle cell from the same person contain the same genes but different proteins.', 'Only some genes are expressed in each cell type, depending on the cell\'s function.', '[2]')])
myths(t, [('Proteins are made in the nucleus.', 'Proteins are made on ribosomes in the cytoplasm using a copy of the gene (mRNA).'), ('Each base in DNA codes for one amino acid.', 'Three bases code for one amino acid.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def aa_count(r, D):
    n = r.choice([300, 450, 600, 900, 1200, 1500, 2100])
    if D == 1:
        return NQ(r, f'A gene contains {n} bases that code for a protein. How many amino acids are in the protein?', n // 3, [n, n // 2, n * 3, n // 4], '', f'3 bases per amino acid: {n} ÷ 3 = {n // 3}.', f=lambda v: str(int(v)))
    if D <= 3:
        return Q(f'A protein contains {n // 3} amino acids. Calculate the minimum number of bases in the gene that codes for it, and explain your answer.', f'{n} bases', f'3 bases per amino acid [1]; {n // 3} × 3 = {n} [1] [2]', 'numerical', 2)
    L = r.choice([4, 5, 6])
    cods = r.sample(list(CODON), L)
    seq = ''.join(cods)
    tab = ', '.join(f'{c} = {CODON[c]}' for c in r.sample(list(CODON), len(CODON)))
    return Q(f'Part of an mRNA molecule has the base sequence {seq}. Using the codon table ({tab}), give the sequence of amino acids coded for, and state how many bases would be needed in mRNA to code for a protein of 150 amino acids.',
             f'{"–".join(CODON[c] for c in cods)}; 450 bases', f'split into triplets [1]; {"–".join(CODON[c] for c in cods)} [2]; 150 × 3 = 450 [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def ps_case(r, D):
    prot = r.choice(['insulin', 'amylase', 'haemoglobin', 'keratin', 'an antibody'])
    intro = f'A cell in the human body produces {prot}. The gene for this protein is on one of the chromosomes in the nucleus.'
    parts = [lambda r: ('Describe how the information in the gene is used to make the protein.', 'Gene is copied into mRNA in the nucleus; mRNA passes to a ribosome in the cytoplasm; ribosome reads the base sequence in triplets and joins amino acids in that order.', '[4]'),
             lambda r: ('Explain why the order of amino acids is important.', 'It determines how the protein folds and its shape, so whether it can carry out its function.', '[2]'),
             lambda r: ('Suggest why only some cells make this protein.', 'Only certain cells express this gene, depending on their function.', '[1]'),
             lambda r: ('Explain why a mutation in the gene could prevent the protein working.', 'Changed base sequence → different amino acid(s) → different shape (e.g. active site / binding site) → no longer functions.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t16b = t

t = T('Mitosis and meiosis: haploid and diploid nuclei', 'mitosis and meiosis', 'haploid and diploid nuclei')
facts(t, [('mitosis', 'nuclear division giving rise to genetically identical cells'), ('meiosis', 'reduction division in which the chromosome number is halved from diploid to haploid, resulting in genetically different cells'),
          ('haploid nucleus', 'a nucleus containing a single set of unpaired chromosomes, as in gametes'), ('diploid nucleus', 'a nucleus containing two sets of chromosomes, as in body cells'),
          ('stem cell', 'an unspecialised cell that divides by mitosis to produce daughter cells that can become specialised')])
mcqs(t, [('Which process produces gametes in humans?', 'Meiosis', 'Meiosis halves the chromosome number and produces variation.', ['Mitosis', 'Fertilisation', 'Binary fission']),
         ('Which is a use of mitosis?', 'Repair of damaged tissues', 'Mitosis is used for growth, repair, replacement of cells and asexual reproduction.', ['Production of sperm', 'Production of eggs', 'Producing variation']),
         ('How many cells are produced when one cell divides by meiosis?', 'Four genetically different cells', 'Meiosis gives four haploid cells.', ['Two identical cells', 'Four identical cells', 'Two different cells'])])
shorts(t, [('State three uses of mitosis.', 'Growth; repair of tissues; replacement of cells; asexual reproduction.', 'any three [3]'), ('State what happens to chromosomes before mitosis.', 'They are copied (replicated) so each new cell gets a full set.', '[1]')])
explain(t, [('Explain why gametes must be haploid.', 'So that when two gametes fuse at fertilisation the zygote has the diploid number; otherwise the chromosome number would double each generation.', '[2]'),
            ('Explain why cells produced by meiosis are genetically different.', 'Chromosome pairs separate randomly (independent assortment), giving different combinations of alleles in each gamete.', '[2]'),
            ('Explain why cancer can result from uncontrolled mitosis.', 'Cells divide repeatedly without control, forming a tumour that can invade other tissues.', '[2]'),
            ('Compare mitosis and meiosis.', 'Mitosis: two cells, diploid, genetically identical, growth/repair. Meiosis: four cells, haploid, genetically different, gametes.', 'three comparisons [3]')])
myths(t, [('Meiosis is used to repair a broken bone.', 'Repair uses mitosis; meiosis produces gametes.'), ('Mitosis produces cells with half the number of chromosomes.', 'Mitosis produces cells with the same number of chromosomes; meiosis halves it.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def div_chrom(r, D):
    org, n = r.choice(CHROM)
    if D <= 2:
        k = r.randrange(2)
        if k == 0:
            return NQ(r, f'A {org} cell with {n} chromosomes divides by mitosis. How many chromosomes are in each daughter cell?', n, [n // 2, n * 2, n // 4, n + 2], '', f'Mitosis keeps the number: {n}.', f=lambda v: str(int(v)))
        return NQ(r, f'A {org} cell with {n} chromosomes divides by meiosis. How many chromosomes are in each cell produced?', n // 2, [n, n * 2, n // 4, n - 1], '', f'Meiosis halves the number: {n // 2}.', f=lambda v: str(int(v)))
    cyc = r.choice([20, 24, 30])
    hrs = cyc * r.choice([3, 4, 5])
    cells = 2 ** (hrs // cyc)
    nm = f'a {org} plant' if org in ('potato', 'onion', 'rice', 'maize', 'pea') else f'a {org}'
    st = f'Each body cell of {nm} contains {n} chromosomes. (a) State the number of chromosomes in a gamete nucleus and in a zygote. (b) A single cell divides by mitosis every {cyc} hours. Calculate the number of cells after {hrs} hours and the total number of chromosomes in all those cells.'
    return Q(st, f'(a) gamete {n // 2}; zygote {n} (b) {cells} cells; {big(cells * n)} chromosomes', f'(a) {n // 2} [1]; {n} [1] (b) {hrs} ÷ {cyc} = {hrs // cyc} divisions; 2^{hrs // cyc} = {cells} cells [1]; × {n} = {big(cells * n)} [1] [4]', 'short', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def div_case(r, D):
    org, n = r.choice(CHROM)
    intro = f'A scientist studies cell division in a {org}, which has {n} chromosomes in each body cell.'
    parts = [lambda r: ('State the number of chromosomes in a cell produced by mitosis and in a cell produced by meiosis.', f'mitosis {n}; meiosis {n // 2}', '[2]'),
             lambda r: ('Explain why the cells produced by mitosis are genetically identical.', 'Chromosomes are copied exactly before division and one copy of each goes into each new cell.', '[2]'),
             lambda r: ('Explain the importance of meiosis in sexual reproduction.', 'Halves chromosome number so the zygote is diploid; produces variation in gametes.', '[2]'),
             lambda r: ('State where meiosis happens in a flowering plant and in a mammal.', 'Plant: anthers and ovules / ovaries. Mammal: testes and ovaries.', '[2]'),
             lambda r: ('Describe the role of stem cells.', 'Unspecialised cells that divide by mitosis and can become specialised to replace or repair tissues.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t16c = t

TRAITS = [('pea plants', 'T', 't', 'tall', 'dwarf', 'height'), ('pea plants', 'R', 'r', 'round seeds', 'wrinkled seeds', 'seed shape'), ('guinea pigs', 'B', 'b', 'black fur', 'white fur', 'fur colour'),
          ('tomato plants', 'P', 'p', 'purple stems', 'green stems', 'stem colour'), ('fruit flies', 'N', 'n', 'normal wings', 'vestigial wings', 'wing shape'), ('cats', 'S', 's', 'short hair', 'long hair', 'hair length'),
          ('humans', 'F', 'f', 'no cystic fibrosis', 'cystic fibrosis', 'cystic fibrosis'), ('maize plants', 'G', 'g', 'green leaves', 'albino (white) leaves', 'leaf colour'),
          ('rabbits', 'E', 'e', 'brown eyes', 'red eyes', 'eye colour'), ('sunflowers', 'Y', 'y', 'yellow petals', 'orange petals', 'petal colour')]


def cross(p1, p2):
    kids = [a + b for a in p1 for b in p2]
    kids = [''.join(sorted(k, key=lambda c: (c.islower(), c))) for k in kids]
    return kids


def ratio(kids, A):
    dom = sum(1 for k in kids if A in k)
    return dom, 4 - dom


t = T('Monohybrid inheritance: genetic diagrams, Punnett squares and test crosses', 'monohybrid inheritance', 'genetic diagrams, punnett squares', 'test crosses')
facts(t, [('genotype', 'the genetic make-up of an organism in terms of the alleles present'), ('phenotype', 'the observable features of an organism'), ('homozygous', 'having two identical alleles of a particular gene'),
          ('heterozygous', 'having two different alleles of a particular gene'), ('dominant', 'an allele that is expressed if it is present in the genotype'), ('recessive', 'an allele that is only expressed when there is no dominant allele of the gene present'),
          ('test cross', 'crossing an organism showing the dominant phenotype with a homozygous recessive organism to find its genotype')])
mcqs(t, [('Two heterozygous plants are crossed. What is the expected ratio of dominant to recessive phenotypes?', '3 : 1', 'Aa × Aa → 1 AA : 2 Aa : 1 aa.', ['1 : 1', '1 : 2 : 1', 'All dominant']),
         ('An organism with genotype Bb is described as', 'heterozygous', 'Two different alleles.', ['homozygous dominant', 'homozygous recessive', 'haploid']),
         ('Why is a test cross carried out with a homozygous recessive organism?', 'Its gametes all carry the recessive allele, so the offspring phenotypes reveal the unknown alleles', 'Any recessive offspring show the unknown parent carries the recessive allele.', ['It makes all the offspring dominant', 'It doubles the chromosome number', 'It prevents mutation'])])
shorts(t, [('State the genotypes possible for an organism showing a dominant phenotype.', 'Homozygous dominant (AA) or heterozygous (Aa).', '[2]'), ('State what is meant by a pure-breeding organism.', 'Homozygous for the gene, so it produces offspring with the same phenotype when bred with similar individuals.', '[1]')])
explain(t, [('Explain why two brown-eyed parents can have a blue-eyed child (brown is dominant).', 'Both parents are heterozygous (Bb); each passes on the recessive allele b; the child is bb.', 'both heterozygous [1]; each passes recessive allele [1] [2]'),
            ('Explain why a genetic diagram gives only the probability of offspring phenotypes.', 'Fertilisation is random, so which gametes fuse is a matter of chance; actual numbers vary, especially with few offspring.', '[2]'),
            ('Explain why the observed ratio in a cross of 40 offspring may not be exactly 3 : 1.', 'Fertilisation is random; with small samples chance causes deviation from the expected ratio.', '[2]')])
myths(t, [('A dominant allele is always the most common allele in a population.', 'Dominant means it is expressed when present, not that it is more common.'), ('Heterozygous means having two recessive alleles.', 'Heterozygous means having two different alleles.')])


@t.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def mono(r, D):
    org, A, a, dp, rp, trait = r.choice(TRAITS)
    gts = [A + A, A + a, a + a]
    p1, p2 = r.choice([(A + a, A + a), (A + a, a + a), (A + A, a + a), (A + a, A + A)] if D >= 2 else [(A + a, A + a), (A + a, a + a)])
    kids = cross(p1, p2)
    d, rc = ratio(kids, A)
    gcount = {g: kids.count(g) for g in dict.fromkeys(sorted(kids, key=lambda k: (k.count(a), k)))}
    def ph(g):
        return dp if A in g else rp
    if D == 1:
        pr = rc / 4
        return NQ(r, f'In {org}, the allele for {dp} ({A}) is dominant to the allele for {rp} ({a}). Two {org} with genotypes {p1} and {p2} are crossed. What is the probability that an offspring has {rp}?', pr * 100, [x for x in (0, 25, 50, 75, 100) if x != pr * 100], '%', f'{p1} × {p2} → {", ".join(kids)}: {rc} of 4 have {rp}.', f=lambda v: fx(v, 0))
    gam1, gam2 = sorted(set(p1)), sorted(set(p2))
    st = (f'In {org}, {trait} is controlled by one gene. The allele for {dp} ({A}) is dominant to the allele for {rp} ({a}). A cross is made between parents with genotypes {p1} and {p2}. '
          '(a) State the phenotypes of the parents. (b) Draw a genetic diagram (Punnett square) to show the possible genotypes of the offspring. (c) State the expected ratio of phenotypes.')
    ans = f'(a) {ph(p1)} and {ph(p2)} (b) gametes {"/".join(gam1)} and {"/".join(gam2)}; offspring ' + ', '.join(f'{v} {g}' for g, v in gcount.items()) + f' (c) {d // math.gcd(d, rc)} {dp} : {rc // math.gcd(d, rc)} {rp}' if rc and d else \
        f'(a) {ph(p1)} and {ph(p2)} (b) gametes {"/".join(gam1)} and {"/".join(gam2)}; offspring all {kids[0]} (c) all {ph(kids[0])}'
    key = f'(a) both phenotypes [1] (b) gametes [1]; offspring genotypes {", ".join(kids)} [1] (c) ratio [1]'
    m = 4
    if D >= 4:
        N = r.choice([40, 60, 80, 120, 200, 360])
        st += f' (d) The cross produced {N} offspring. Calculate the expected number with {rp}.'
        ans += f' (d) {fx(N * rc / 4, 0)}'
        key += f' (d) {rc}/4 × {N} = {fx(N * rc / 4, 0)} [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'multi_step', m)


@t.add('C3', (2, 3, 4, 5), 'case')
def testcross(r, D):
    org, A, a, dp, rp, trait = r.choice(TRAITS[:6] + TRAITS[7:])
    het = r.random() < 0.5
    N = r.choice([20, 24, 30, 40, 48])
    nr = round(N * r.uniform(0.42, 0.58)) if het else 0
    st = f'A breeder has a {org[:-1] if org.endswith("s") else org} showing {dp} and wants to know its genotype. It is crossed with one showing {rp}. The offspring are {N - nr} with {dp} and {nr} with {rp}. (a) State the genotype of the parent with {rp}. (b) Deduce the genotype of the parent with {dp}. Explain your answer using a genetic diagram.'
    if het:
        ans = f'(a) {a}{a} (b) {A}{a}: some offspring have {rp} ({a}{a}), so the {dp} parent must carry {a}. {A}{a} × {a}{a} → {A}{a}, {A}{a}, {a}{a}, {a}{a} = 1 : 1.'
    else:
        ans = f'(a) {a}{a} (b) {A}{A}: all offspring show {dp}; if it were {A}{a} about half would be {rp}. {A}{A} × {a}{a} → all {A}{a}.'
    key = f'(a) {a}{a} [1] (b) correct genotype [1]; reasoning [1]; genetic diagram with gametes and offspring [1] [4]'
    return Q(st, ans, key, 'case', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def pedigree(r, D):
    org, A, a, dp, rp, trait = TRAITS[6] if r.random() < 0.5 else r.choice(TRAITS)
    intro = f'Two parents both have {dp} but their first child has {rp}. In {org} the allele for {dp} ({A}) is dominant to the allele for {rp} ({a}).'
    parts = [lambda r: ('Deduce the genotypes of the parents and explain.', f'Both {A}{a}: the child is {a}{a}, so each parent must carry {a}; they show {dp}, so they must also have {A}.', '[2]'),
             lambda r: ('Draw a genetic diagram to show the probability that their next child will also have this phenotype.', f'{A}{a} × {A}{a} → {A}{A}, {A}{a}, {A}{a}, {a}{a}; probability {rp} = 1/4 (25%).', 'gametes [1]; offspring [1]; probability [1] [3]'),
             lambda r: (f'State the probability that a child with {dp} from these parents is heterozygous.', '2/3', '2 of the 3 dominant-phenotype genotypes are heterozygous [1] [2]'),
             lambda r: ('Explain why the actual number of children with each phenotype in a family may differ from the expected ratio.', 'Each fertilisation is a random, independent event; with small numbers chance has a big effect.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


longs(t, [('Using a genetic diagram, explain how two heterozygous parents can produce offspring with the recessive phenotype, and how a test cross can identify a heterozygous individual.', 'Aa × Aa; gametes A, a; offspring AA, Aa, Aa, aa; 1 in 4 aa recessive. Test cross: unknown dominant × aa; if any offspring aa → unknown is Aa; if all dominant (large number) → AA.',
           'genetic diagram [2]; probability [1]; test cross method [1]; interpretation of both outcomes [2] [6]')])
t16d = t

t = T('Codominance, ABO blood groups and sex-linked characteristics', 'codominance', 'abo blood groups', 'sex-linked characteristics')
facts(t, [('codominance', 'a situation in which both alleles in heterozygous organisms contribute to the phenotype'), ('sex-linked characteristic', 'a feature in which the gene responsible is located on a sex chromosome, making it more common in one sex'),
          ('carrier', 'a person who is heterozygous for a recessive allele and does not show the phenotype but can pass it on'), ('ABO blood group', 'a characteristic controlled by three alleles, IA, IB and Io, in which IA and IB are codominant and Io is recessive'),
          ('red–green colour blindness', 'a sex-linked condition caused by a recessive allele on the X chromosome')])
mcqs(t, [('A person with blood group AB has the genotype', 'IAIB', 'IA and IB are codominant.', ['IAIo', 'IBIo', 'IoIo']),
         ('Why are sex-linked conditions such as colour blindness more common in males?', 'Males have only one X chromosome, so one recessive allele causes the condition', 'There is no second X to carry a dominant allele.', ['Males have two X chromosomes', 'The allele is on the Y chromosome only', 'Females cannot inherit X chromosomes']),
         ('Red and white snapdragons are crossed and all offspring are pink. This is an example of', 'codominance', 'Both alleles contribute to the phenotype of heterozygotes.', ['sex linkage', 'mutation', 'complete dominance'])])
shorts(t, [('State the possible genotypes of a person with blood group A.', 'IAIA or IAIo.', '[2]'), ('State the genotype of a female carrier of colour blindness.', 'XBXb.', '[1]')])
explain(t, [('Explain why a man cannot pass colour blindness to his son.', 'The son receives the Y chromosome from his father; the colour-blindness allele is on the X chromosome.', '[2]'),
            ('Explain why blood group O is described as recessive.', 'The Io allele is only expressed when no IA or IB allele is present (IoIo).', '[2]'),
            ('Explain how two parents with blood groups A and B could have a child with blood group O.', 'Both parents are heterozygous (IAIo and IBIo); each passes on Io; the child is IoIo.', '[2]')])
myths(t, [('A woman who carries one allele for colour blindness is colour blind.', 'A heterozygous woman is a carrier; she has a dominant allele on her other X and has normal vision.'), ('Blood group AB is caused by an AB allele.', 'Blood group AB results from inheriting both codominant alleles, IA and IB.')])

ABO = {'A': ['IAIA', 'IAIo'], 'B': ['IBIB', 'IBIo'], 'AB': ['IAIB'], 'O': ['IoIo']}


def abo_ph(g):
    s = set([g[:2], g[2:]])
    if s == {'IA', 'IB'}:
        return 'AB'
    if 'IA' in s:
        return 'A'
    if 'IB' in s:
        return 'B'
    return 'O'


def abo_cross(g1, g2):
    out = []
    for x in (g1[:2], g1[2:]):
        for y in (g2[:2], g2[2:]):
            order = {'IA': 0, 'IB': 1, 'Io': 2}
            a, b = sorted([x, y], key=lambda z: order[z])
            out.append(a + b)
    return out


@t.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def abo_q(r, D):
    g1 = r.choice(['IAIo', 'IAIA', 'IBIo', 'IAIB', 'IoIo', 'IBIB'])
    g2 = r.choice(['IBIo', 'IAIo', 'IoIo', 'IAIB'])
    kids = abo_cross(g1, g2)
    phs = {}
    for k in kids:
        phs[abo_ph(k)] = phs.get(abo_ph(k), 0) + 1
    if D == 1:
        return MQ(r, f'What is the blood group of a person with genotype {g1}?', abo_ph(g1), ['A', 'B', 'AB', 'O'], f'{g1}: blood group {abo_ph(g1)} (IA, IB codominant; Io recessive).')
    st = f'A mother has genotype {g1} and a father has genotype {g2}. (a) State the blood groups of the parents. (b) Draw a genetic diagram to show the possible genotypes and blood groups of their children. (c) State the probability of a child having each blood group.'
    ans = f'(a) {abo_ph(g1)} and {abo_ph(g2)} (b) {", ".join(f"{k} ({abo_ph(k)})" for k in kids)} (c) ' + ', '.join(f'{p}: {fx(v / 4 * 100, 0)}%' for p, v in phs.items())
    key = '(a) both [1] (b) gametes [1]; four genotypes [1] (c) probabilities [1]'
    return Q(st, ans, key + ' [4]', 'multi_step', 4)


@t.add('C3', (2, 3, 4, 5), 'multi_step')
def sexlink(r, D):
    cond, B, b = r.choice([('red–green colour blindness', 'XB', 'Xb'), ('haemophilia', 'XH', 'Xh')])
    mum = r.choice([f'{B}{b}', f'{B}{B}', f'{b}{b}'])
    dad = r.choice([f'{B}Y', f'{b}Y'])
    m1, m2 = mum[:2], mum[2:]
    d1, d2 = dad[:2], 'Y'
    kids = [m + d for m in (m1, m2) for d in (d1, d2)]

    def ph(k):
        if k.endswith('Y'):
            return ('affected son' if k.startswith(b) else 'unaffected son')
        return 'affected daughter' if k.count(b) == 2 else ('carrier daughter' if b in k else 'unaffected daughter')
    tally = {}
    for k in kids:
        tally[ph(k)] = tally.get(ph(k), 0) + 1
    st = f'{cap(cond)} is caused by a recessive allele on the X chromosome. A woman with genotype {mum} has children with a man with genotype {dad}. Draw a genetic diagram and state the probability that a son will have {cond}.'
    sons = [k for k in kids if k.endswith('Y')]
    pa = sum(1 for k in sons if k.startswith(b)) / len(sons)
    ans = f'Gametes {m1}, {m2} and {d1}, Y; children {", ".join(f"{k} ({ph(k)})" for k in kids)}; probability that a son is affected = {fx(pa * 100, 0)}%.'
    return Q(st, ans, 'parental gametes [1]; four offspring genotypes [1]; phenotypes [1]; probability for sons [1] [4]', 'multi_step', 4)


@t.add('C3', (2, 3, 4), 'multi_step')
def codom(r, D):
    org, R_, W_, rc, wc, mc = r.choice([('snapdragons', 'CR', 'CW', 'red', 'white', 'pink'), ('cattle', 'CR', 'CW', 'red', 'white', 'roan'), ('chickens', 'CB', 'CW', 'black', 'white', 'blue-grey'), ('four o\'clock plants', 'CR', 'CW', 'red', 'white', 'pink')])
    p = r.choice([(R_ + W_, R_ + W_), (R_ + R_, W_ + W_), (R_ + W_, W_ + W_), (R_ + W_, R_ + R_)])
    kids = [x + y for x in (p[0][:2], p[0][2:]) for y in (p[1][:2], p[1][2:])]

    def ph(g):
        return rc if g.count(R_) == 2 else (wc if g.count(W_) == 2 else mc)
    tally = {}
    for k in kids:
        tally[ph(k)] = tally.get(ph(k), 0) + 1
    st = f'In {org}, the alleles {R_} ({rc}) and {W_} ({wc}) are codominant; heterozygotes are {mc}. A {ph(p[0])} parent ({p[0]}) is crossed with a {ph(p[1])} parent ({p[1]}). Draw a genetic diagram and state the expected ratio of phenotypes in the offspring.'
    return Q(st, f'Offspring {", ".join(kids)}; ' + ' : '.join(f'{v} {k}' for k, v in tally.items()), 'gametes [1]; offspring genotypes [1]; phenotype ratio [1] [3]', 'multi_step', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def blood_case2(r, D):
    intro = f'A hospital in {city(r)} records the blood groups of a family. The mother is group A, the father is group B, and their first child is group O.'
    parts = [lambda r: ('Deduce the genotypes of the parents, explaining your answer.', 'Mother IAIo and father IBIo, because the child (IoIo) must have received Io from each parent.', '[2]'),
             lambda r: ('Draw a genetic diagram to show the possible blood groups of further children.', 'IAIo × IBIo → IAIB (AB), IAIo (A), IBIo (B), IoIo (O).', '[3]'),
             lambda r: ('State the probability that the next child will be blood group AB.', '25% (1 in 4).', '[1]'),
             lambda r: ('Explain why blood group is an example of discontinuous variation.', 'There are a few distinct categories (A, B, AB, O) with no intermediates; controlled by genes only.', '[2]'),
             lambda r: ('Explain what is meant by codominance, using this example.', 'IA and IB both contribute to the phenotype in a heterozygote, giving blood group AB.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t16e = t
CHAPTERS[6] = [t16a, t16b, t16c, t16d, t16e]

# ===================================================================== 7 Variation and selection

VFEAT = [('height', 'continuous'), ('body mass', 'continuous'), ('foot length', 'continuous'), ('leaf length', 'continuous'), ('hand span', 'continuous'), ('arm length', 'continuous'),
         ('ABO blood group', 'discontinuous'), ('ability to roll the tongue', 'discontinuous'), ('sex (male or female)', 'discontinuous'), ('seed shape in peas (round or wrinkled)', 'discontinuous'),
         ('flower colour in snapdragons', 'discontinuous'), ('presence of attached or free earlobes', 'discontinuous'), ('number of seeds in a pea pod', 'discontinuous'), ('shell length of limpets', 'continuous')]
t = T('Continuous and discontinuous variation; mutation as a source of new alleles', 'continuous and discontinuous variation', 'mutation as a source of new alleles')
facts(t, [('variation', 'differences between individuals of the same species'), ('continuous variation', 'variation that results in a range of phenotypes between two extremes, for example height'),
          ('discontinuous variation', 'variation that results in a limited number of distinct phenotypes with no intermediates, for example ABO blood group'),
          ('mutation', 'a genetic change'), ('gene mutation', 'a random change in the base sequence of DNA'), ('mutagen', 'a factor such as ionising radiation or certain chemicals that increases the rate of mutation')])
mcqs(t, [('Which type of variation is usually caused by genes only?', 'Discontinuous variation', 'Discontinuous variation (e.g. blood group) is caused by genes alone.', ['Continuous variation', 'Environmental variation', 'All variation']),
         ('Which graph should be drawn to display data showing continuous variation?', 'Histogram', 'Continuous data are grouped into classes and drawn as a histogram with touching bars.', ['Bar chart with gaps', 'Pie chart only', 'Line graph through each point']),
         ('Which factor increases the rate of mutation?', 'Ionising radiation', 'Ionising radiation (e.g. X-rays, gamma rays) is a mutagen.', ['Low temperature', 'Visible light from a lamp', 'Drinking water']),
         ('Which is the only source of new alleles?', 'Mutation', 'New alleles arise only by mutation; meiosis and fertilisation reshuffle existing alleles.', ['Meiosis', 'Fertilisation', 'Mitosis'])])
shorts(t, [('State two examples of continuous variation in humans.', 'Height; body mass (also hand span, foot length).', 'any two [2]'), ('State two types of mutagen.', 'Ionising radiation (X-rays, gamma rays, UV); certain chemicals (e.g. tar in tobacco smoke).', '[2]'),
           ('State two causes of continuous variation.', 'Genes (many genes) and the environment.', '[2]')])
explain(t, [('Explain why height in humans shows continuous variation.', 'Height is controlled by many genes and also influenced by the environment (diet, health), so there is a range of values between two extremes.', 'many genes [1]; environment [1] [2]'),
            ('Explain how a gene mutation can result in a different phenotype.', 'A change in the base sequence changes the sequence of amino acids, so the protein made has a different shape and may not work (or work differently).', 'base sequence changed [1]; amino acid sequence changed [1]; protein shape / function changed [1] [3]'),
            ('Explain why identical twins raised apart can have different body masses.', 'They have identical genes, so differences must be caused by the environment, such as diet and exercise.', 'same genes [1]; environment [1] [2]'),
            ('Explain why discontinuous variation is shown as a bar chart rather than a histogram.', 'The data fall into distinct categories with no intermediates, so bars are separate.', '[2]'),
            ('Explain why workers using X-ray machines stand behind lead screens.', 'X-rays are ionising radiation, a mutagen; reducing exposure lowers the risk of mutations (and cancer).', 'mutagen [1]; less risk of mutation / cancer [1] [2]')])
myths(t, [('Mutations are always harmful.', 'Most mutations are neutral or harmful, but some are beneficial and give an advantage.'), ('Blood group shows continuous variation because there are four groups.', 'Blood group shows discontinuous variation: a few distinct categories with no intermediates.'),
          ('Continuous variation is caused only by the environment.', 'Continuous variation is caused by many genes and the environment together.')])


@t.add('C3', (1, 2, 3), 'short')
def var_type(r, D):
    f, k = r.choice(VFEAT)
    if D == 1:
        return MQ(r, f'Which type of variation is shown by {f}?', cap(k) + ' variation', ['Continuous variation' if k == 'discontinuous' else 'Discontinuous variation', 'Inherited variation only', 'Mutation', 'Natural selection'],
                  f'{cap(f)}: {k} variation.')
    f2, k2 = r.choice([v for v in VFEAT if v[1] != k])
    gr = {'continuous': 'histogram', 'discontinuous': 'bar chart'}
    return Q(f'A student in {city(r)} collects data on {f} and {f2} from her class. For each feature, state the type of variation and the type of graph she should draw.',
             f'{cap(f)}: {k}, {gr[k]}; {f2}: {k2}, {gr[k2]}.', f'{k} + {gr[k]} [1]; {k2} + {gr[k2]} [1] [2]', 'short', 2)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def var_data(r, D):
    feat, u, lo, hi, dpx = r.choice([('height', 'cm', 148, 182, 0), ('hand span', 'cm', 16.0, 23.5, 1), ('foot length', 'cm', 21.0, 28.5, 1), ('leaf length', 'mm', 42, 96, 0), ('limpet shell length', 'mm', 18, 41, 0)])
    n = 8 if D <= 3 else 10
    vals = sorted(round(r.uniform(lo, hi), dpx) for _ in range(n))
    r.shuffle(vals)
    mean = sum(vals) / n
    st = f'{person(r)} measured the {feat} of {n} {"students" if feat in ("height", "hand span", "foot length") else "samples"} in {city(r)}: ' + ', '.join(f'{v:.{dpx}f}' for v in vals) + f' {u}. (a) Calculate the mean {feat}. (b) Calculate the range. (c) State the type of variation shown.'
    ans = f'(a) {fx(mean, dpx + 1)} {u} (b) {fx(max(vals) - min(vals), dpx)} {u} (c) continuous'
    key = f'(a) sum ÷ {n} [1] = {fx(mean, dpx + 1)} {u} [1] (b) {max(vals):.{dpx}f} − {min(vals):.{dpx}f} = {fx(max(vals) - min(vals), dpx)} {u} [1] (c) continuous [1] [4]'
    return Q(st, ans, key, 'numerical', 4)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def var_freq(r, D):
    cls = r.choice([['140–149', '150–159', '160–169', '170–179', '180–189'], ['15.0–16.9', '17.0–18.9', '19.0–20.9', '21.0–22.9', '23.0–24.9']])
    feat, u = ('height', 'cm') if cls[0].startswith('14') else ('hand span', 'cm')
    f = [r.randint(2, 6), r.randint(8, 14), r.randint(15, 24), r.randint(7, 13), r.randint(1, 5)]
    N = sum(f)
    i = r.randrange(5)
    modal = cls[f.index(max(f))]
    st = f'The {feat}s of {N} students at a school in {city(r)} were grouped into classes: ' + '; '.join(f'{c} {u}: {v}' for c, v in zip(cls, f)) + f'. (a) State the modal class. (b) Calculate the percentage of students in the class {cls[i]} {u}. (c) Explain whether this shows continuous or discontinuous variation.'
    p = f[i] / N * 100
    return Q(st, f'(a) {modal} {u} (b) {fx(p, 1)}% (c) continuous: a range of values between two extremes (data had to be grouped).',
             f'(a) {modal} [1] (b) {f[i]} ÷ {N} × 100 [1] = {fx(p, 1)}% [1] (c) continuous with reason [1] [4]', 'numerical', 4)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def mut_rate(r, D):
    doses = r.choice([[0, 1, 2, 3, 4], [0, 2, 4, 6, 8], [0, 5, 10, 15, 20]])
    base = r.choice([2, 3, 4, 5])
    k = r.uniform(1.5, 3.0) * 4 / doses[-1]
    m = [round(base + k * d * base, 0) for d in doses]
    i = r.randrange(1, 5)
    org = r.choice(['fruit flies', 'barley seeds', 'yeast cells', 'bacteria'])
    st = f'Scientists in {city(r)} exposed {org} to different doses of X-rays and counted the number of mutants per 10 000 offspring. Dose / arbitrary units: {", ".join(map(str, doses))}. Mutants per 10 000: {", ".join(fx(v) for v in m)}. (a) Calculate the percentage increase in the number of mutants between dose 0 and dose {doses[i]}. (b) Describe the relationship shown. (c) Explain why there are some mutants even at dose 0.'
    p = pct(m[0], m[i])
    return Q(st, f'(a) {fx(p, 0)}% (b) as dose increases, the number of mutants increases (roughly in proportion). (c) Mutations happen randomly / spontaneously (or from background radiation).',
             f'(a) ({fx(m[i])} − {fx(m[0])}) ÷ {fx(m[0])} × 100 [1] = {fx(p, 0)}% [1] (b) positive correlation [1] (c) spontaneous / background radiation [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def var_case(r, D):
    pl = r.choice(['sunflower', 'bean', 'maize'])
    intro = f'A group of students in {city(r)} grew {pl} plants from seeds of the same variety. Half were grown in fertile soil in full sun and half in poor soil in shade. The heights of all plants were measured after six weeks.'
    parts = [lambda r: ('State the type of variation shown by plant height and the type of graph used to display it.', 'Continuous variation; histogram.', '[2]'),
             lambda r: ('Explain why plants grown from the same variety still showed a range of heights within each group.', 'Genetic differences between seeds (alleles from sexual reproduction) and small differences in local environment.', 'genetic variation [1]; environmental variation [1] [2]'),
             lambda r: ('Suggest why the plants in fertile soil and full sun were taller on average.', 'More light and minerals (e.g. nitrate for protein) give more photosynthesis and growth; environment affects phenotype.', '[2]'),
             lambda r: ('Name one feature of these plants likely to show discontinuous variation and explain why.', 'Flower colour (or seed colour): controlled by one or a few genes, giving distinct categories.', '[2]'),
             lambda r: ('Explain how a mutation could produce a new flower colour in this species.', 'A random change in the base sequence of the gene changes the amino acid sequence of the pigment enzyme, so a different pigment is made.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare continuous and discontinuous variation, giving examples, and describe how mutation produces new alleles.', 'Continuous: range between extremes, many genes + environment, e.g. height, histogram. Discontinuous: distinct categories, genes only, e.g. blood group, bar chart. Mutation: random change in base sequence, rate increased by ionising radiation / chemicals; only source of new alleles.',
           'continuous described with example [2]; discontinuous described with example [2]; mutation and mutagens [2] [6]')])
t17a = t

ADAPT = [('thick waxy cuticle', 'xerophyte', 'reduces water loss by evaporation'), ('leaves reduced to spines', 'xerophyte', 'gives a smaller surface area for transpiration'),
         ('stomata sunk in pits', 'xerophyte', 'traps humid air, reducing the concentration gradient for water vapour'), ('rolled leaves', 'xerophyte', 'traps moist air inside, reducing water loss'),
         ('hairs on the leaf surface', 'xerophyte', 'traps a layer of moist air, reducing transpiration'), ('widespread shallow roots', 'xerophyte', 'absorbs rain water quickly over a large area'),
         ('very deep roots', 'xerophyte', 'reaches water deep underground'), ('thick fleshy stem that stores water', 'xerophyte', 'stores water for dry periods'),
         ('stomata on the upper surface of floating leaves', 'hydrophyte', 'allows gas exchange with the air'), ('large air spaces in stems and leaves', 'hydrophyte', 'keeps leaves afloat and allows oxygen to reach roots'),
         ('thin or absent cuticle', 'hydrophyte', 'saves materials, as water loss is not a problem'), ('small, poorly developed roots', 'hydrophyte', 'is enough, as water is absorbed across the whole surface'),
         ('flexible stems with little xylem', 'hydrophyte', 'lets the plant bend with water currents without damage, as water supports it'), ('large flat floating leaves', 'hydrophyte', 'absorbs maximum light at the water surface')]
t = T('Adaptive features of organisms (xerophytes and hydrophytes)', 'adaptive features of organisms', 'xerophytes and hydrophytes')
facts(t, [('adaptive feature', 'an inherited feature that helps an organism to survive and reproduce in its environment'), ('xerophyte', 'a plant adapted to live in dry conditions'),
          ('hydrophyte', 'a plant adapted to live in water or in very wet conditions'), ('fitness', 'the probability of an organism surviving and reproducing in the environment in which it is found'),
          ('cuticle', 'the waxy, waterproof layer covering the epidermis of a leaf')])
mcqs(t, [('Which feature of marram grass reduces water loss?', 'Leaves that roll up with stomata on the inner surface', 'Rolling traps humid air around the stomata.', ['Large air spaces in the stem', 'Stomata on the upper surface of floating leaves', 'A thin cuticle']),
         ('Why do water lilies have stomata on the upper surface of their leaves?', 'The lower surface is in contact with water, so gas exchange must happen with the air above', 'Upper stomata allow CO₂ in and O₂ out from the air.', ['To lose more water', 'To absorb minerals', 'To keep the leaf sinking']),
         ('Which is an adaptation of a cactus?', 'Leaves reduced to spines', 'Spines reduce surface area for transpiration and deter animals.', ['Large thin leaves', 'Many stomata on the upper surface', 'Air spaces to help it float'])])
shorts(t, [('State three adaptive features of a xerophyte.', 'Thick waxy cuticle; sunken stomata; leaves reduced to spines / rolled leaves; deep or widespread roots.', 'any three [3]'), ('State two adaptive features of a hydrophyte.', 'Large air spaces; stomata on upper surface of floating leaves; thin cuticle; small roots.', 'any two [2]')])
explain(t, [('Explain how sunken stomata reduce water loss in a xerophyte.', 'Humid air is trapped in the pit, so the concentration gradient of water vapour between the leaf and the air is reduced, slowing diffusion.', 'humid air trapped [1]; smaller gradient / slower diffusion [1] [2]'),
            ('Explain why a cactus can carry out photosynthesis even though its leaves are spines.', 'Its green stem contains chloroplasts and carries out photosynthesis.', '[2]'),
            ('Explain why hydrophytes have large air spaces in their stems.', 'Air spaces keep the plant buoyant so leaves float near light, and allow oxygen to diffuse to the submerged roots.', 'buoyancy / light [1]; oxygen to roots [1] [2]'),
            ('Explain how the fennec fox is adapted to living in hot deserts.', 'Large ears have a large surface area with many blood vessels to lose heat; pale fur reflects heat / camouflage; kidneys produce concentrated urine to save water.', 'any two adaptations with explanations [2] [3]'),
            ('Explain why adaptive features must be inherited to be important in evolution.', 'Only inherited features (alleles) can be passed to offspring, increasing in frequency over generations.', '[2]')])
myths(t, [('A cactus grows spines because it decides it needs to save water.', 'Spines are inherited adaptive features that arose by mutation and were selected because they increase survival.'),
          ('Hydrophytes have a thick waxy cuticle to keep water out.', 'Hydrophytes have a thin or absent cuticle; water loss is not a problem for them.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def adapt_id(r, D):
    f, k, why = r.choice(ADAPT)
    if D <= 2:
        env = {'xerophyte': 'Dry habitat (xerophyte)', 'hydrophyte': 'Water (hydrophyte)'}
        oth = 'hydrophyte' if k == 'xerophyte' else 'xerophyte'
        w3 = r.choice([a for a in ADAPT if a[1] == oth])[2]
        return MQ(r, f'A plant has {f}. In which habitat is it most likely to live, and why?', f'{env[k]}: this feature {why}',
                  [f'{env[oth]}: this feature {why}', f'{env[k]}: this feature {w3}', f'{env[oth]}: this feature {w3}'], f'{cap(f)} → {k}: {why}.')
    f2, k2, why2 = r.choice([a for a in ADAPT if a[0] != f])
    return Q(f'A botanist in {city(r)} describes two plants. Plant P has {f}. Plant Q has {f2}. For each plant, suggest whether it is a xerophyte or a hydrophyte and explain how the feature is adaptive.',
             f'P: {k} — {why}. Q: {k2} — {why2}.', f'P {k} [1] + explanation [1]; Q {k2} [1] + explanation [1] [4]', 'short', 4)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def stoma_dens(r, D):
    pl = r.choice([('marram grass', 'xerophyte'), ('oleander', 'xerophyte'), ('water lily', 'hydrophyte')])
    area = r.choice([0.1, 0.2, 0.25, 0.5])
    up = r.randint(0, 2) if pl[1] == 'xerophyte' else r.randint(40, 70)
    lo = r.randint(8, 25) if pl[1] == 'xerophyte' else r.randint(0, 2)
    mes = r.randint(15, 35)
    st = (f'A student counted stomata in a field of view of area {fx(area, 2)} mm² on leaves of {pl[0]} and of a bean plant (a mesophyte). {cap(pl[0])}: upper surface {up}, lower surface {lo}. Bean: upper surface {round(mes / 4)}, lower surface {mes}. '
          f'(a) Calculate the number of stomata per mm² on the lower surface of the {pl[0]}. (b) Calculate the total stomata per mm² (both surfaces) for each plant. (c) Suggest how the distribution of stomata in {pl[0]} is an adaptation to its habitat.')
    tot = (up + lo) / area
    totb = (round(mes / 4) + mes) / area
    adapt = ('few stomata, mostly on the lower surface (or inside rolled leaves), reducing water loss' if pl[1] == 'xerophyte' else 'stomata mainly on the upper surface, in contact with the air, for gas exchange; the lower surface touches water')
    return Q(st, f'(a) {fx(lo / area, 1)} per mm² (b) {pl[0]} {fx(tot, 1)}; bean {fx(totb, 1)} per mm² (c) {adapt}.',
             f'(a) {lo} ÷ {fx(area, 2)} = {fx(lo / area, 1)} [1] (b) {fx(tot, 1)} [1]; {fx(totb, 1)} [1] (c) {pl[1]} adaptation explained [2] [5]', 'numerical', 5)


XERO = {'setup': lambda r, p: f'{p} measured the percentage loss in mass of shoots of four plant species, each standing in a test-tube of water covered with oil, over 24 hours in the same conditions.',
        'iv': ('plant species', ''), 'xs': lambda r: r.sample(['cactus', 'marram grass', 'oleander', 'bean', 'sunflower', 'water lily'], 4),
        'dv': ('percentage loss in mass', '%'), 'y': lambda x, k: k * {'cactus': 0.6, 'marram grass': 1.5, 'oleander': 2.2, 'bean': 7.5, 'sunflower': 8.5, 'water lily': 11.0}[x], 'dp': 1, 'graph': False, 'prep': 'for',
        'controls': ['temperature', 'light intensity', 'humidity / air movement', 'time', 'initial mass or leaf area of the shoot'],
        'trend': lambda d: f'The {d["xs"][max(range(4), key=lambda i: d["means"][i])]} lost the highest percentage of mass and the {d["xs"][min(range(4), key=lambda i: d["means"][i])]} the lowest; xerophytes lost much less than other plants.',
        'why': ('Xerophytes (e.g. cactus, marram grass) have thick waxy cuticles, few or sunken stomata and small leaf surface area, so less water evaporates and diffuses out; non-xerophytes have larger leaves with more stomata.', 'xerophyte features named [1]; less evaporation / diffusion of water vapour [1]; comparison with other plants [1] [3]'),
        'improve': ['use percentage change in mass so shoots of different starting masses can be compared', 'measure the leaf surface area and express the loss per cm²'],
        'extra': [lambda r, d: ('State the type of graph that should be drawn to display these results and explain why.', 'A bar chart, because the independent variable (plant species) is categoric.', 'bar chart [1]; categoric variable [1] [2]'),
                  lambda r, d: ('Explain why a layer of oil was placed on the water in each test-tube.', 'To stop water evaporating from the surface of the water, so all mass lost is from the shoot.', '[2]')]}
add_practical(t, XERO, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (3, 4, 5), 'multi_step')
def adapt_case(r, D):
    intro = f'Marram grass grows on coastal sand dunes near {r.choice(["Liverpool", "Perth", "Cape Town", "Auckland", "Gdańsk", "Brest"])}. The sand drains quickly and the dunes are exposed to strong, dry winds. In dry weather its leaves roll up, with the stomata on the inner surface among many hairs.'
    parts = [lambda r: ('State the term for a plant adapted to dry conditions.', 'Xerophyte.', '[1]'),
             lambda r: ('Explain how rolling of the leaves reduces water loss.', 'Moist air is trapped inside the roll, so the water vapour concentration gradient is reduced and less water diffuses out of the stomata; less surface exposed to wind.', 'humid air trapped [1]; smaller diffusion gradient [1]; less exposure to wind [1] [3]'),
             lambda r: ('Suggest the advantage of very long roots to marram grass.', 'They reach water deep in the sand and anchor the plant in shifting sand.', '[2]'),
             lambda r: ('Explain why reducing water loss also reduces the rate of photosynthesis.', 'Closing or enclosing stomata reduces diffusion of carbon dioxide into the leaf, so less CO₂ for photosynthesis.', '[2]'),
             lambda r: ('Compare the adaptations of marram grass with those of a water lily.', 'Marram: thick cuticle, few sunken stomata on inner surface, rolled leaves; water lily: thin cuticle, stomata on upper surface, air spaces, large floating leaves.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe and explain the adaptive features of xerophytes and hydrophytes.', 'Xerophytes: thick waxy cuticle, sunken stomata, rolled leaves, hairs, spines, deep / widespread roots, water storage — reduce water loss or increase uptake. Hydrophytes: air spaces for buoyancy and oxygen, stomata on upper surface, thin cuticle, small roots, flexible stems.',
           'three xerophyte features explained [3]; three hydrophyte features explained [3] [6]')])
t17b = t

t = T('Natural selection and evolution; antibiotic resistance in bacteria', 'natural selection and evolution', 'antibiotic resistance in bacteria')
facts(t, [('natural selection', 'the process by which individuals with better adapted features are more likely to survive, reproduce and pass on their alleles'), ('evolution', 'the change in adaptive features of a population over time as a result of natural selection'),
          ('adaptation', 'the process, resulting from natural selection, by which populations become more suited to their environment over many generations'),
          ('antibiotic resistance', 'the ability of bacteria to survive treatment with an antibiotic that would normally kill them'),
          ('selection pressure', 'an environmental factor, such as a predator or an antibiotic, that affects which individuals survive and reproduce'), ('MRSA', 'a strain of Staphylococcus aureus bacteria that is resistant to many antibiotics')])
mcqs(t, [('What is the original source of the allele for antibiotic resistance in bacteria?', 'A random mutation', 'Resistance arises by chance mutation, before exposure to the antibiotic.', ['The antibiotic causes the bacteria to change', 'The bacteria learn to resist', 'The patient\'s white blood cells']),
         ('Why does overuse of antibiotics increase the number of resistant bacteria?', 'Non-resistant bacteria are killed, so resistant bacteria survive and reproduce with less competition', 'The antibiotic is a selection pressure.', ['Antibiotics cause mutations for resistance', 'Antibiotics feed the bacteria', 'Resistant bacteria are made by the immune system']),
         ('Which is required for natural selection to happen?', 'Variation within a population', 'Selection acts on variation that is inherited.', ['All individuals being identical', 'No competition', 'Asexual reproduction only'])])
shorts(t, [('State two ways in which the development of antibiotic-resistant bacteria can be reduced.', 'Use antibiotics only when essential; complete the full course; do not use them for viral infections; limit use in farming.', 'any two [2]'),
           ('State why antibiotics are not used to treat viral diseases.', 'Antibiotics do not affect viruses (they target bacterial structures).', '[1]')])
explain(t, [('Explain how a population of bacteria becomes resistant to an antibiotic.', 'A random mutation gives one bacterium resistance; when the antibiotic is used, non-resistant bacteria die; the resistant bacterium survives and reproduces rapidly by binary fission, passing on the allele, so the population becomes resistant.', 'mutation [1]; non-resistant killed [1]; resistant survive and reproduce [1]; pass on allele [1] [4]'),
            ('Explain why it is important for patients to finish a course of antibiotics.', 'Stopping early may leave the most resistant bacteria alive; these reproduce, increasing the proportion of resistant bacteria.', '[2]'),
            ('Explain why there is a struggle for survival in natural populations.', 'Organisms produce more offspring than the environment can support, so they compete for limited resources such as food, mates and space.', '[2]'),
            ('Explain why resistance spreads faster in bacteria than adaptations spread in mammals.', 'Bacteria reproduce very quickly (short generation time), so many generations occur in a short time.', '[2]')])
myths(t, [('Bacteria become resistant because they get used to the antibiotic.', 'Resistance comes from a random mutation; the antibiotic only selects resistant bacteria, which survive and reproduce.'),
          ('Individuals evolve during their lifetime to suit their environment.', 'Populations evolve over many generations; individuals do not evolve.'),
          ('Natural selection produces the mutations an organism needs.', 'Mutations are random; natural selection only changes how often existing alleles are passed on.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def resist_growth(r, D):
    g = r.choice([20, 30, 40])
    h = r.choice([2, 3, 4, 5])
    n = h * 60 // g
    st0 = r.choice([1, 2, 5, 10])
    final = st0 * 2 ** n
    if D <= 2:
        return NQ(r, f'A single resistant bacterium divides by binary fission every {g} minutes. Assuming all survive, how many bacteria will there be after {h} hours?', 2 ** n, [2 ** (n - 1), n * 2, 2 ** (n + 1), n ** 2], '', f'{h * 60} ÷ {g} = {n} generations; 2^{n} = {2 ** n}.', f=lambda v: f'{int(v):,}'.replace(',', ' '))
    kill = r.choice([99, 99.9, 95])
    N0 = r.choice([10000, 50000, 100000, 200000])
    surv = N0 * (100 - kill) / 100
    st = f'A patient in {city(r)} had {N0:,} bacteria in an infected wound. {fx(kill, 1)}% were killed by an antibiotic; the survivors were resistant. (a) Calculate the number of bacteria that survived. (b) The survivors divide every {g} minutes. Calculate the number of resistant bacteria after {h} hours. (c) Explain why the antibiotic will no longer be effective.'.replace(',', ' ')
    tot = surv * 2 ** n
    return Q(st, f'(a) {big(surv)} (b) {big(tot)} (c) all the bacteria now carry the resistance allele, inherited from the survivors.',
             f'(a) {big(N0)} × {fx((100 - kill) / 100, 3)} = {big(surv)} [1] (b) {n} generations [1]; {big(surv)} × 2^{n} = {big(tot)} [1] (c) offspring inherit resistance [1] [4]', 'numerical', 4)


@t.add('C3', (2, 3, 4, 5), 'case')
def moth_data(r, D):
    rel = [r.randint(80, 160), r.randint(80, 160)]
    rec = [round(rel[0] * r.uniform(0.25, 0.40)), round(rel[1] * r.uniform(0.08, 0.15))]
    st = (f'In a study near {city(r)}, scientists released {rel[0]} dark and {rel[1]} pale peppered moths in a polluted wood where tree bark was blackened by soot. After a week they recaptured {rec[0]} dark and {rec[1]} pale moths. '
          '(a) Calculate the percentage of each type recaptured. (b) Explain the difference using the theory of natural selection. (c) Suggest what happened to the proportion of dark moths after clean-air laws reduced soot.')
    p1, p2 = rec[0] / rel[0] * 100, rec[1] / rel[1] * 100
    return Q(st, f'(a) dark {fx(p1, 1)}%, pale {fx(p2, 1)}% (b) Dark moths were camouflaged on dark bark, so fewer were eaten by birds; they survived to reproduce and passed on the allele for dark colour. (c) It decreased, because pale moths were better camouflaged on clean bark.',
             f'(a) {rec[0]} ÷ {rel[0]} × 100 = {fx(p1, 1)}% [1]; {rec[1]} ÷ {rel[1]} × 100 = {fx(p2, 1)}% [1] (b) camouflage / predation [1]; survive and reproduce [1]; pass on allele [1] (c) decreased with reason [1] [6]', 'case', 6)


@t.add('C3', (2, 3, 4), 'numerical')
def mrsa_data(r, D):
    y0 = r.choice([2006, 2008, 2010, 2012])
    a = round(r.uniform(3, 9), 1)
    b = round(a * r.uniform(2.2, 4.5), 1)
    yrs = r.choice([8, 10, 12])
    st = f'In a hospital in {city(r)}, the percentage of Staphylococcus infections resistant to an antibiotic rose from {a}% in {y0} to {b}% in {y0 + yrs}. (a) Calculate the mean increase per year in percentage points. (b) Suggest two reasons for this increase.'
    return Q(st, f'(a) {fx((b - a) / yrs, 2)} percentage points per year (b) overuse of antibiotics / not completing courses / use in farming, selecting resistant bacteria.',
             f'(a) ({b} − {a}) ÷ {yrs} [1] = {fx((b - a) / yrs, 2)} [1] (b) any two reasons [2] [4]', 'numerical', 4)


ABX = {'setup': lambda r, p: f'{p} placed paper discs soaked in different concentrations of an antibiotic on an agar plate spread with bacteria, incubated it at 25 °C for 2 days and measured the diameter of the clear zone around each disc.',
       'iv': ('concentration of antibiotic', 'µg/cm³'), 'xs': lambda r: r.choice([[0, 5, 10, 20, 40], [0, 10, 20, 30, 40], [0, 2, 4, 8, 16]]), 'dv': ('diameter of clear zone', 'mm'),
       'y': lambda x, k: 6 + k * 14 * x / (x + 8 * (1 if x < 20 else 1.1)), 'dp': 0,
       'controls': ['volume of antibiotic solution on each disc', 'size of paper disc', 'type of bacteria', 'incubation temperature', 'time of incubation'],
       'why': ('Antibiotic diffuses out from the disc into the agar and kills bacteria; a higher concentration gives a steeper gradient and reaches killing concentration further from the disc, so the clear zone is wider.', 'diffusion from disc [1]; bacteria killed [1]; higher concentration diffuses further [1] [3]'),
       'improve': ['use more than one plate for each concentration', 'measure the diameter in two directions at right angles and take the mean'],
       'control': 'A disc soaked in sterile water (concentration 0) — any clear zone around it would show that the disc itself, not the antibiotic, affects the bacteria.',
       'extra': [lambda r, d: ('Calculate the area of the clear zone at the highest concentration (area = πr²).', f'{fx(math.pi * (d["means"][-1] / 2) ** 2, 0)} mm²', f'r = {fx(d["means"][-1] / 2, 2)} mm [1]; π × r² = {fx(math.pi * (d["means"][-1] / 2) ** 2, 0)} mm² [1] [2]'),
                 lambda r, d: ('State why the plates were incubated at 25 °C rather than 37 °C.', 'To reduce the risk of growing human pathogens.', '[1]')]}
add_practical(t, ABX, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (3, 4, 5), 'multi_step')
def natsel_case(r, D):
    org, feat, sel = r.choice([('rabbits', 'thicker fur', 'very cold winters'), ('giraffes', 'longer necks', 'competition for leaves high in trees'), ('snails', 'banded shells', 'thrush predation in hedgerows'), ('finches', 'larger, stronger beaks', 'a drought in which only hard seeds remained')])
    intro = f'In a population of {org}, some individuals have {feat}. During a period of {sel}, the proportion of {org} with {feat} increased over several generations.'
    parts = [lambda r: (f'Explain how the proportion of {org} with {feat} increased, using the theory of natural selection.', f'Variation exists (from mutation); individuals with {feat} are better adapted, so more survive {sel} and reproduce, passing on the alleles; over generations the allele frequency increases.', 'variation [1]; better adapted survive [1]; reproduce [1]; pass on alleles [1] [4]'),
             lambda r: ('State the original source of the variation.', 'Mutation (new alleles), with meiosis and random fertilisation producing new combinations.', '[1]'),
             lambda r: ('Explain why the change takes several generations.', 'Allele frequencies change only when individuals reproduce; each generation increases the proportion a little.', '[2]'),
             lambda r: ('Suggest what would happen if the environment changed back.', f'{cap(feat)} would no longer give an advantage, so the frequency of the allele may stay the same, or fall if the feature has a cost.', '[2]'),
             lambda r: ('Compare natural selection with selective breeding.', 'Natural selection: environment chooses, features that aid survival, slow; selective breeding: humans choose features useful to humans, faster.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how natural selection can lead to the development of antibiotic-resistant bacteria, and explain how this can be slowed.', 'Mutation gives resistance; antibiotic kills non-resistant bacteria; resistant ones survive, reproduce rapidly and pass on the allele; population becomes resistant (e.g. MRSA). Slow by limiting use, completing courses, not using for viruses, hygiene.',
           'mutation [1]; selection by antibiotic [1]; survival and reproduction [1]; inheritance / population change [1]; two control measures [2] [6]')])
t17c = t

SB = [('dairy cattle', 'milk yield', 'cows with the highest milk yield', 'L per lactation'), ('wheat', 'grain yield', 'plants with the largest ears of grain', 'tonnes per hectare'),
      ('chickens', 'egg production', 'hens laying the most eggs', 'eggs per year'), ('tomatoes', 'fruit mass', 'plants with the largest fruit', 'g per fruit'),
      ('sheep', 'wool yield', 'sheep with the most wool', 'kg per year'), ('rice', 'grain yield', 'plants with the most grain', 'tonnes per hectare')]
t = T('Selective breeding', 'selective breeding')
facts(t, [('selective breeding', 'the process of humans choosing individuals with desirable features to breed together, repeated over many generations'),
          ('artificial selection', 'another name for selective breeding, in which humans rather than the environment select which individuals breed'),
          ('variety', 'a group of plants within a species with particular features produced by selective breeding'), ('inbreeding', 'breeding closely related individuals, which reduces genetic variation'),
          ('disease resistance', 'an inherited feature that allows a crop or animal to resist infection by a pathogen')])
mcqs(t, [('What is the first step in selectively breeding a high-yielding variety of rice?', 'Select parent plants with the highest yield', 'Choose individuals with the desired feature to breed.', ['Insert a gene from another species', 'Expose plants to radiation', 'Grow plants in a fermenter']),
         ('Why is selective breeding repeated over many generations?', 'Each generation the desired feature becomes more common and more pronounced', 'Repeated selection increases the frequency of desirable alleles.', ['To produce new genes in each generation', 'To make all offspring identical immediately', 'To remove all variation']),
         ('Which is a disadvantage of selective breeding?', 'Reduced genetic variation, so the population may be vulnerable to new diseases', 'Inbreeding reduces variety of alleles.', ['It always takes only one generation', 'It increases genetic variation', 'It inserts genes from other species'])])
shorts(t, [('State two features that farmers might select for in crop plants.', 'High yield; disease resistance; drought tolerance; flavour; short stems.', 'any two [2]'), ('State two features selected for in dog breeding.', 'Temperament (gentleness); size; coat type; herding / hunting ability.', 'any two [2]')])
explain(t, [('Describe how a farmer could selectively breed cattle that produce more milk.', 'Select the cows with the highest milk yield and a bull from a high-yielding mother; breed them; select the best offspring and breed them; repeat over many generations.', 'select parents [1]; breed [1]; select offspring [1]; repeat over many generations [1] [4]'),
            ('Explain why selective breeding is faster than natural selection.', 'Humans choose the parents directly every generation, so only individuals with desired features breed.', '[2]'),
            ('Explain why genetic variation is reduced by selective breeding.', 'Only a few individuals with similar alleles are bred, so other alleles are lost from the population.', '[2]'),
            ('Explain why a crop variety that has been selectively bred for high yield may still be grown with fertilisers.', 'The phenotype depends on the environment as well as genes; minerals are needed for maximum growth.', '[2]')])
myths(t, [('Selective breeding creates new genes.', 'Selective breeding changes the frequency of existing alleles; new alleles come from mutation.'), ('Selective breeding gives the same result as genetic modification.', 'Selective breeding uses existing variation within a species over many generations; GM transfers specific genes, even between species.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sb_yield(r, D):
    org, feat, sel, u = r.choice(SB)
    base = {'dairy cattle': 4000, 'wheat': 2.5, 'chickens': 180, 'tomatoes': 60, 'sheep': 3.5, 'rice': 3.0}[org]
    v0 = base * r.uniform(0.9, 1.1)
    gens = r.choice([5, 6, 8, 10])
    v1 = v0 * r.uniform(1.25, 1.8)
    dp = 0 if base >= 60 else 1
    v0, v1 = round(v0, dp), round(v1, dp)
    if D == 1:
        return NQ(r, f'A farmer selectively bred {org} for {feat}. The mean value rose from {fx(v0, dp)} to {fx(v1, dp)} {u}. What was the increase?', v1 - v0, [v1 + v0, v1, (v1 - v0) / 2, v0], f' {u}', f'{fx(v1, dp)} − {fx(v0, dp)} = {fx(v1 - v0, dp)}.', f=lambda v: fx(v, dp))
    st = f'Breeders in {city(r)} selected {sel} for {gens} generations. The mean {feat} rose from {fx(v0, dp)} to {fx(v1, dp)} {u}. (a) Calculate the percentage increase. (b) Calculate the mean increase per generation. (c) Describe the procedure the breeders used.'
    p = pct(v0, v1)
    return Q(st, f'(a) {fx(p, 1)}% (b) {fx((v1 - v0) / gens, dp + 1)} {u} per generation (c) selected individuals with the highest {feat}, bred them, selected the best offspring and repeated each generation.',
             f'(a) ({fx(v1, dp)} − {fx(v0, dp)}) ÷ {fx(v0, dp)} × 100 [1] = {fx(p, 1)}% [1] (b) {fx(v1 - v0, dp)} ÷ {gens} = {fx((v1 - v0) / gens, dp + 1)} [1] (c) select, breed, repeat [2] [5]', 'numerical', 5)


@t.add('C3', (1, 2, 3, 4), 'short')
def sb_choice(r, D):
    cases = [('a farmer in a region with frequent droughts', 'maize', 'drought tolerance'), ('a dairy farmer', 'cattle', 'high milk yield'), ('a grower whose crops are attacked by rust fungus', 'wheat', 'disease resistance'),
             ('a family with small children', 'dogs', 'gentle temperament'), ('a farmer in a windy area', 'wheat', 'short, strong stems'), ('a florist', 'roses', 'large, scented flowers'),
             ('a beef farmer in a hot climate', 'cattle', 'heat tolerance'), ('a farmer whose rice fields flood', 'rice', 'tolerance of flooding')]
    who, org, feat = r.choice(cases)
    if D <= 2:
        return MQ(r, f'Which feature would {who} most want to select for in {org}?', cap(feat), [cap(c[2]) for c in cases if c[2] != feat], f'{cap(who)}: {feat}.')
    return Q(f'In {city(r)}, {who} plans to breed {org}. Suggest one feature to select for, and describe how selective breeding could be used to obtain it.',
             f'{cap(feat)}: choose parents showing {feat}, breed them, select offspring with the most {feat} and breed them; repeat for many generations.', 'suitable feature [1]; select parents [1]; breed and select offspring [1]; repeat over generations [1] [4]', 'short', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def sb_case(r, D):
    org, feat, sel, u = r.choice(SB)
    intro = f'Over 50 years, breeders in {city(r)} have produced varieties of {org} with much greater {feat} than wild types. Some of these varieties are now very similar to each other genetically.'
    parts = [lambda r: (f'Describe how selective breeding could have produced varieties of {org} with greater {feat}.', f'Select {sel}; breed them; choose offspring with the greatest {feat}; repeat over many generations.', '[3]'),
             lambda r: ('Explain one disadvantage of the varieties being genetically similar.', 'Reduced genetic variation means a new disease or environmental change could affect all of them; alleles for resistance may have been lost.', '[2]'),
             lambda r: ('Suggest why breeders keep some wild-type individuals or seeds.', 'They act as a store of alleles (genetic variation) that may be needed in future, e.g. for disease resistance.', '[2]'),
             lambda r: ('State two differences between selective breeding and natural selection.', 'Humans choose vs environment; features useful to humans vs features aiding survival; faster vs slower.', '[2]'),
             lambda r: ('Explain why selective breeding cannot produce a feature for which there is no allele in the population.', 'Selective breeding only changes frequencies of existing alleles; new alleles arise only by mutation.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how selective breeding is carried out and discuss its advantages and disadvantages.', 'Choose parents with desired features; breed; select best offspring; repeat for many generations. Advantages: higher yield, disease resistance, desired features. Disadvantages: reduced variation, inbreeding, susceptibility to disease, animal welfare problems, slow.',
           'procedure [3]; two advantages [1]; two disadvantages [2] [6]')])
t17d = t
CHAPTERS[7] = [t17a, t17b, t17c, t17d]

# ===================================================================== 8 Organisms and their environment
WEBS = [('a pond', {'algae': ['water fleas', 'pond snails'], 'pondweed': ['pond snails', 'tadpoles'], 'water fleas': ['dragonfly larvae', 'small fish'], 'pond snails': ['small fish'], 'tadpoles': ['dragonfly larvae', 'small fish'],
                    'dragonfly larvae': ['small fish'], 'small fish': ['herons']}),
        ('an African savanna', {'grass': ['zebras', 'gazelles', 'grasshoppers'], 'acacia trees': ['giraffes', 'gazelles'], 'grasshoppers': ['lizards', 'birds'], 'lizards': ['birds'], 'zebras': ['lions'], 'gazelles': ['lions', 'cheetahs'], 'giraffes': ['lions']}),
        ('a woodland', {'oak trees': ['caterpillars', 'aphids', 'deer'], 'grass': ['rabbits', 'deer'], 'caterpillars': ['blue tits', 'spiders'], 'aphids': ['ladybirds', 'blue tits'], 'ladybirds': ['blue tits'], 'spiders': ['blue tits'],
                        'blue tits': ['sparrowhawks'], 'rabbits': ['foxes']}),
        ('a rocky seashore', {'seaweed': ['limpets', 'periwinkles'], 'phytoplankton': ['mussels', 'barnacles'], 'limpets': ['crabs', 'gulls'], 'periwinkles': ['crabs', 'dog whelks'], 'mussels': ['dog whelks', 'gulls'], 'barnacles': ['dog whelks'],
                              'dog whelks': ['crabs'], 'crabs': ['gulls']}),
        ('a rice field', {'rice plants': ['grasshoppers', 'rats', 'planthoppers'], 'weeds': ['grasshoppers'], 'grasshoppers': ['frogs', 'spiders'], 'planthoppers': ['spiders', 'frogs'], 'spiders': ['frogs'], 'frogs': ['snakes'], 'rats': ['snakes', 'owls'], 'snakes': ['owls']})]


def web_info(web):
    prey = set(web)
    allo = set(prey) | {p for v in web.values() for p in v}
    eaten = {p for v in web.values() for p in v}
    prod = [o for o in web if o not in eaten]
    chains = []

    def dfs(o, path):
        if not web.get(o):
            chains.append(path)
            return
        for p in web[o]:
            dfs(p, path + [p])
    for p in prod:
        dfs(p, [p])
    tl = {}
    for c in chains:
        for i, o in enumerate(c):
            tl.setdefault(o, set()).add(i + 1)
    return prod, chains, tl, allo


MASS = {'pondweed', 'grass', 'seaweed', 'phytoplankton'}


def nn(x):
    return sci(x, 2) if 0 < abs(x) < 0.001 else sf(x * (1 + 1e-12), 3).replace(',', ' ')


ORD = {1: 'producer (first trophic level)', 2: 'primary consumer (second trophic level)', 3: 'secondary consumer (third trophic level)', 4: 'tertiary consumer (fourth trophic level)', 5: 'quaternary consumer (fifth trophic level)'}
t = T('Food chains, food webs and trophic levels; pyramids of number, biomass and energy', 'food chains, food webs and trophic levels', 'pyramids of number, biomass and energy')
facts(t, [('food chain', 'a diagram showing the transfer of energy from one organism to the next, beginning with a producer'), ('food web', 'a network of interconnected food chains'),
          ('producer', 'an organism that makes its own organic nutrients, usually using energy from sunlight through photosynthesis'), ('consumer', 'an organism that gets its energy by feeding on other organisms'),
          ('herbivore', 'an animal that gets its energy by eating plants'), ('carnivore', 'an animal that gets its energy by eating other animals'), ('decomposer', 'an organism that gets its energy from dead or waste organic material'),
          ('trophic level', 'the position of an organism in a food chain, food web, pyramid of numbers, biomass or energy')])
mcqs(t, [('What do the arrows in a food chain represent?', 'The direction of energy transfer', 'Arrows point from the organism eaten to the organism that eats it.', ['The direction the animals move', 'Which organism is bigger', 'The flow of oxygen']),
         ('A pyramid of numbers for oak tree → caterpillars → blue tits has a narrow base. Why?', 'One oak tree is very large and supports many caterpillars', 'Numbers do not account for size; biomass would give a normal pyramid.', ['Oak trees are not producers', 'Caterpillars are decomposers', 'Energy increases along the chain']),
         ('Which type of pyramid is always pyramid-shaped?', 'Pyramid of energy', 'Energy is lost at each level, so each bar is smaller than the one below.', ['Pyramid of numbers', 'Pyramid of biomass measured on one day', 'All pyramids can be inverted']),
         ('What is the original source of energy for almost all food chains?', 'Sunlight', 'Producers capture light energy by photosynthesis.', ['Soil', 'Decomposers', 'Water'])])
shorts(t, [('State the advantage of using a pyramid of biomass rather than a pyramid of numbers.', 'It takes the size (mass) of organisms into account.', '[1]'), ('State the meaning of the term secondary consumer.', 'An animal that feeds on primary consumers; third trophic level.', '[1]'),
           ('State two reasons why a pyramid of numbers may not be pyramid-shaped.', 'Producers may be very large (one tree); parasites may be very numerous.', '[2]')])
explain(t, [('Explain why a food web is a more accurate description of feeding relationships than a food chain.', 'Most organisms eat, and are eaten by, more than one type of organism; a web shows these interconnections.', '[2]'),
            ('Explain why a pyramid of energy is never inverted.', 'Energy is lost at each trophic level (respiration, heat, waste), so less is available to each level above.', 'energy lost at each level [1]; less passed on [1] [2]'),
            ('Explain why removing a species from a food web can affect organisms it does not eat.', 'Its predators may eat more of other prey, and its prey increase and compete with other species; effects pass through the web.', '[2]'),
            ('Explain why the pyramid of biomass for a sea can appear inverted when measured at one moment.', 'Phytoplankton reproduce very quickly and are eaten rapidly, so their standing biomass is small even though their production is large.', '[2]')])
myths(t, [('Arrows in a food chain show what eats what, pointing towards the food.', 'Arrows point from the food to the organism that eats it, showing energy transfer.'), ('A pyramid of biomass is the same as a pyramid of numbers.', 'A pyramid of biomass shows the total dry mass at each level, which accounts for the size of organisms.')])


@t.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def web_q(r, D):
    place, web = r.choice(WEBS)
    prod, chains, tl, allo = web_info(web)
    edges = '; '.join(f'{a} {"is" if a in MASS else "are"} eaten by {", ".join(b[:-1]) + " and " + b[-1] if len(b) > 1 else b[0]}' for a, b in web.items())
    intro = f'{person(r)} drew a food web for {place}: {edges}.'
    single = [o for o in tl if len(tl[o]) == 1 and min(tl[o]) >= 2]
    multi = [o for o in tl if len(tl[o]) > 1]
    if D == 1:
        o = r.choice(single)
        L = min(tl[o])
        return MQ(r, intro + f' What is the trophic position of the {o}?', cap(ORD[L]), [cap(v) for k_, v in ORD.items() if k_ != L], f'{cap(o)}: {ORD[L]}.')
    longest = max(chains, key=len)
    tops = [o for o in allo if not web.get(o)]
    parts = [lambda r: ('Name one producer in this food web.', prod[0] + (f' (or {prod[1]})' if len(prod) > 1 else ''), '[1]'),
             lambda r: ('State the number of food chains in this food web.', str(len(chains)), f'{len(chains)} [1]'),
             lambda r: ('Write out the longest food chain in this web.', ' → '.join(longest), f'{" → ".join(longest)} [1]')]
    if multi:
        o = r.choice(multi)
        parts.append(lambda r: (f'State all the trophic levels at which the {o} feed, and explain why.', ', '.join(str(x) for x in sorted(tl[o])) + f': they eat organisms at more than one level.', 'all levels correct [1]; eats at more than one level [1] [2]'))
    top = r.choice(tops)
    pr = [a for a, b in web.items() if top in b]
    v = r.choice(pr)
    parts.append(lambda r: (f'Suggest the immediate effect on the population of {v} if all the {top} were removed. Explain your answer.', f'The population of {v} increases, because fewer are eaten (less predation).', 'increases [1]; less predation [1] [2]'))
    parts.append(lambda r: ('State the original source of energy for this food web.', 'Sunlight (light energy captured by producers in photosynthesis).', '[1]'))
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


PYR = [('oak tree', 'caterpillars', 'blue tits', 'sparrowhawks', (1, 1), 2.0e6, 0.8, 11, 180), ('grass', 'rabbits', 'stoats', None, (200000, 600000), 2.0, 1500, 250, 0),
       ('rose bushes', 'aphids', 'ladybirds', None, (5, 15), 900, 0.002, 0.03, 0), ('phytoplankton', 'zooplankton', 'small fish', None, (10 ** 9, 3 * 10 ** 9), 1e-5, 0.005, 20, 0),
       ('maize plants', 'locusts', 'lizards', 'hawks', (400, 800), 300, 2, 40, 800)]


@t.add('C3', (2, 3, 4, 5), 'numerical')
def pyr_q(r, D):
    a, b, c, d, nr, m1, m2, m3, m4 = r.choice(PYR)
    n1 = r.randint(*nr)
    B1 = n1 * m1
    effs = [r.uniform(0.08, 0.15) for _ in range(3)]
    B2 = B1 * effs[0]
    n2 = max(2, round(B2 / m2))
    n3 = max(1, round(n2 * m2 * effs[1] / m3))
    lv = [(a, n1, m1), (b, n2, m2), (c, n3, m3)]
    if d and D >= 4:
        n4 = max(1, round(n3 * m3 * effs[2] / m4))
        lv.append((d, n4, m4))
    bio = [n * m for o, n, m in lv]
    while len(lv) > 3 and bio[-1] >= bio[-2]:
        lv, bio = lv[:-1], bio[:-1]
    if any(bio[i + 1] >= bio[i] for i in range(len(bio) - 1)):
        return None
    tab = '; '.join(f'{o}: number {big(n)}, mean dry mass {nn(m)} g' for o, n, m in lv)
    inv = lv[0][1] < lv[1][1]
    st = f'An ecologist in {city(r)} sampled a food chain: {tab}. (a) Calculate the total dry biomass at each trophic level. (b) Describe the shape of the pyramid of numbers. (c) Explain why the pyramid of biomass has a different shape from the pyramid of numbers.' if inv else \
        f'An ecologist in {city(r)} sampled a food chain: {tab}. (a) Calculate the total dry biomass at each trophic level. (b) Calculate the biomass at the second trophic level as a percentage of that at the first. (c) Explain why biomass decreases at each trophic level.'
    bs = '; '.join(f'{o} {nn(x)} g' for (o, n, m), x in zip(lv, bio))
    if inv:
        ans = f'(a) {bs} (b) narrow base (one or few large producers) with a wider second bar — not a true pyramid (c) biomass takes the mass of each organism into account; the producers are large, so the first trophic level has the greatest biomass and the biomass pyramid is a normal pyramid shape.'
        key = f'(a) n × mass at each level [1]; all correct [1] (b) inverted / narrow base [1] (c) size taken into account [1]; producer biomass largest [1] [5]'
    else:
        ans = f'(a) {bs} (b) {fx(bio[1] / bio[0] * 100, 1)}% (c) energy (and biomass) is lost at each level by respiration, as heat, and in faeces and uneaten parts.'
        key = f'(a) n × mass at each level [1]; all correct [1] (b) {nn(bio[1])} ÷ {nn(bio[0])} × 100 = {fx(bio[1] / bio[0] * 100, 1)}% [1] (c) respiration / heat [1]; waste / uneaten parts [1] [5]'
    return Q(st, ans, key, 'numerical', 5)


@t.add('C4', (3, 4, 5), 'multi_step')
def web_case(r, D):
    place, web = r.choice(WEBS)
    prod, chains, tl, allo = web_info(web)
    edges = '; '.join(f'{a} → {", ".join(b)}' for a, b in web.items())
    c = r.choice([x for x in chains if len(x) >= 4] or chains)
    intro = f'Students studied feeding relationships in {place}. Arrows show who is eaten by whom: {edges}.'
    parts = [lambda r: ('Write out one food chain from this web with four organisms and label the trophic level of each.', ' → '.join(f'{o} ({i + 1})' for i, o in enumerate(c[:4])), 'chain in correct order [1]; trophic levels [1] [2]'),
             lambda r: ('Explain why food chains rarely have more than five trophic levels.', 'Energy is lost at each level (about 90%), so too little energy remains to support further levels.', 'energy lost at each level [1]; not enough for more levels [1] [2]'),
             lambda r: (f'Sketch and explain the shape of a pyramid of energy for the chain {" → ".join(c[:3])}.', 'Each bar narrower than the one below; energy decreases at each level because of respiration, heat and waste.', 'pyramid shape [1]; explanation [1] [2]'),
             lambda r: ('Explain the role of decomposers in this ecosystem.', 'They break down dead organisms and waste, releasing carbon dioxide and mineral ions (e.g. nitrate) for producers.', '[2]'),
             lambda r: ('Suggest why a food web is more stable than a single food chain.', 'If one food source declines, consumers can eat other organisms, so populations are less affected.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe what is meant by a food chain and a food web, and compare pyramids of numbers, biomass and energy.', 'Chain: energy transfer from producer to consumers; web: interconnected chains. Numbers: count organisms, may be inverted. Biomass: total dry mass, usually pyramid. Energy: energy per unit area per year, always pyramid.',
           'chain and web [2]; numbers [1]; biomass [1]; energy [1]; comparison / why shapes differ [1] [6]')])
t18a = t

t = T('Energy flow and efficiency of energy transfer between trophic levels', 'energy flow', 'efficiency of energy transfer between trophic levels')
facts(t, [('energy flow', 'the transfer of energy from the Sun to producers, then to consumers and decomposers, finally lost as heat'), ('efficiency of energy transfer', 'the percentage of the energy at one trophic level that is passed to the next'),
          ('respiration loss', 'the energy released in respiration that is eventually lost to the surroundings as heat'), ('primary production', 'the energy captured by producers in photosynthesis and stored in biomass'),
          ('egestion', 'the passing out of undigested food (faeces) from the body')])
mcqs(t, [('Approximately what percentage of energy is usually passed from one trophic level to the next?', '10%', 'Typical efficiency is about 10% (range 5–20%).', ['90%', '50%', '100%']),
         ('Which is not a way energy is lost between trophic levels?', 'Photosynthesis', 'Energy is lost by respiration (heat), excretion, egestion and uneaten parts.', ['Heat from respiration', 'Undigested food in faeces', 'Parts of the organism not eaten']),
         ('Why is it more energy-efficient for humans to eat crop plants than to eat animals fed on crops?', 'There are fewer trophic levels, so less energy is lost', 'Each extra trophic level loses about 90% of the energy.', ['Plants contain more protein', 'Animals cannot digest crops', 'Energy increases along the chain'])])
shorts(t, [('State three ways in which energy is lost between trophic levels.', 'Heat from respiration; faeces (undigested material); excretion (urea); parts not eaten (bones, roots).', 'any three [3]'), ('State the form in which energy finally leaves an ecosystem.', 'Heat.', '[1]')])
explain(t, [('Explain why energy flow through an ecosystem is described as non-cyclical.', 'Energy enters as light and leaves as heat; it is not recycled, unlike nutrients such as carbon.', '[2]'),
            ('Explain why warm-blooded animals (mammals, birds) have a lower efficiency of energy transfer than fish.', 'They use much energy in respiration to keep a constant body temperature, and lose it as heat.', '[2]'),
            ('Explain why less energy is transferred to herbivores than to carnivores from their food.', 'Plant material contains a lot of cellulose, which herbivores cannot digest fully, so more energy is lost in faeces.', '[2]'),
            ('Explain why only a small percentage of the light energy falling on a field is captured by crop plants.', 'Some light misses the leaves, is reflected, or is the wrong wavelength; photosynthesis is limited by other factors.', '[2]')])
myths(t, [('Energy is recycled in an ecosystem like carbon.', 'Energy flows through the ecosystem and is lost as heat; only matter is recycled.'), ('Most of the energy eaten by an animal is used for growth.', 'Most is lost in respiration (heat), faeces and excretion; only about 10% goes into new biomass.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def eff_calc(r, D):
    c = r.choice([('grass', 'cattle', 'humans'), ('phytoplankton', 'zooplankton', 'herring'), ('maize', 'locusts', 'lizards'), ('algae', 'water fleas', 'small fish'), ('rice', 'rats', 'snakes')])
    E1 = r.choice([10000, 15000, 20000, 25000, 40000, 87000])
    e1, e2 = round(r.uniform(5, 18), 1), round(r.uniform(5, 18), 1)
    E2 = round(E1 * e1 / 100)
    E3 = round(E2 * e2 / 100)
    if D == 1:
        return NQ(r, f'The {c[0]} in an area contain {big(E1)} kJ/m²/year and the {c[1]} that eat them contain {big(E2)} kJ/m²/year. What is the efficiency of energy transfer?', E2 / E1 * 100, [E1 / E2, 100 - E2 / E1 * 100, E2 / E1], '%', f'{E2} ÷ {E1} × 100 = {fx(E2 / E1 * 100, 1)}%.', f=lambda v: fx(v, 1))
    st = f'In an ecosystem near {city(r)}, the energy in each trophic level was measured: {c[0]} {big(E1)} kJ/m²/year; {c[1]} {big(E2)} kJ/m²/year; {c[2]} {big(E3)} kJ/m²/year. (a) Calculate the efficiency of energy transfer from {c[0]} to {c[1]}. (b) Calculate the efficiency from {c[1]} to {c[2]}. (c) Calculate the energy lost between {c[0]} and {c[1]}, and state two ways it is lost.'
    a1, a2 = E2 / E1 * 100, E3 / E2 * 100
    return Q(st, f'(a) {fx(a1, 1)}% (b) {fx(a2, 1)}% (c) {big(E1 - E2)} kJ/m²/year; heat from respiration, faeces, uneaten parts, excretion.',
             f'(a) {E2} ÷ {E1} × 100 [1] = {fx(a1, 1)}% [1] (b) {E3} ÷ {E2} × 100 = {fx(a2, 1)}% [1] (c) {E1} − {E2} = {E1 - E2} [1]; two ways [1] [5]', 'numerical', 5)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def chain_energy(r, D):
    sun = r.choice([1.0e6, 1.5e6, 2.0e6, 3.0e6])
    cap_ = r.choice([1, 1.5, 2, 3])
    eff = r.choice([10, 12, 15, 20]) if D >= 4 else 10
    E1 = sun * cap_ / 100
    E2, E3 = E1 * eff / 100, E1 * (eff / 100) ** 2
    st = f'Sunlight falling on a field in {city(r)} delivers {sci(sun, 2)} kJ/m²/year. Crop plants capture {fx(cap_, 1)}% of this in photosynthesis. The efficiency of energy transfer between each later trophic level is {eff}%. (a) Calculate the energy in the producers. (b) Calculate the energy reaching the secondary consumers. (c) Suggest why only {fx(cap_, 1)}% of the light energy is captured by the plants.'
    return Q(st, f'(a) {nn(E1)} kJ/m²/year (b) {nn(E3)} kJ/m²/year (c) light reflected, transmitted, wrong wavelength or misses chloroplasts; photosynthesis limited by CO₂ / temperature.',
             f'(a) {sci(sun, 2)} × {fx(cap_ / 100, 3)} = {nn(E1)} [1] (b) {nn(E1)} × {eff / 100} = {nn(E2)} (primary) [1]; × {eff / 100} = {nn(E3)} [1] (c) any one reason [1] [4]', 'numerical', 4)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def fate_q(r, D):
    an = r.choice(['a cow', 'a sheep', 'a caterpillar', 'a goat'])
    eaten = r.choice([1000, 2000, 2500, 3000, 4000])
    gr = r.uniform(0.04, 0.15)
    ur = round(r.uniform(0.02, 0.06), 2)
    f = round(r.uniform(0.35, 0.6) * (1 - gr - ur), 2)
    resp = round(1 - gr - ur - f, 2)
    fa, re, u = round(eaten * f), round(eaten * resp), round(eaten * ur)
    g = eaten - fa - re - u
    st = f'{cap(an)} eats plant material containing {eaten} kJ of energy. {fa} kJ is lost in faeces, {re} kJ in respiration and {u} kJ in urine. (a) Calculate the energy used for growth (new biomass). (b) Calculate the percentage of the energy eaten that is used for growth. (c) Explain why so much energy is lost in the faeces of herbivores.'
    return Q(st, f'(a) {g} kJ (b) {fx(g / eaten * 100, 1)}% (c) plant cell walls contain cellulose, which is difficult to digest, so much remains undigested.',
             f'(a) {eaten} − ({fa} + {re} + {u}) = {g} kJ [1] (b) {g} ÷ {eaten} × 100 [1] = {fx(g / eaten * 100, 1)}% [1] (c) cellulose undigested [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def food_eff_case(r, D):
    E = r.choice([1.2e7, 2.0e7, 3.6e7, 4.8e7])
    need = r.choice([3.0e6, 3.5e6, 4.0e6])
    eff = r.choice([10, 12])
    p1 = E / need
    p2 = E * eff / 100 / need
    intro = f'A hectare of farmland in {city(r)} produces crops containing {sci(E, 2)} kJ of energy per year. One person needs about {sci(need, 2)} kJ per year. If the crops are fed to cattle, {eff}% of the energy is passed to beef.'
    parts = [lambda r: ('Calculate how many people could be fed for a year by eating the crops directly.', f'{fx(p1, 1)} people', f'{sci(E, 2)} ÷ {sci(need, 2)} [1] = {fx(p1, 1)} [1] [2]'),
             lambda r: ('Calculate how many people could be fed for a year by eating beef from cattle fed on the crops.', f'{fx(p2, 2)} people', f'{sci(E, 2)} × {eff / 100} = {sci(E * eff / 100, 2)} kJ [1]; ÷ {sci(need, 2)} = {fx(p2, 2)} [1] [2]'),
             lambda r: ('Explain why the number of people fed is smaller when they eat beef.', 'An extra trophic level: cattle lose most energy in respiration (heat), faeces and urine, so only a small fraction becomes beef.', 'extra trophic level [1]; energy lost by respiration / heat / waste [1] [2]'),
             lambda r: ('Suggest one advantage to people of eating some meat, despite the energy loss.', 'Meat provides protein with all essential amino acids, iron and vitamin B12; animals can graze land unsuitable for crops.', '[1]'),
             lambda r: ('Explain why keeping cattle indoors in warm sheds can increase the efficiency of energy transfer to beef.', 'Less energy is used in movement and keeping warm, so more energy goes into growth (biomass).', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how energy flows through an ecosystem and explain why energy transfer between trophic levels is inefficient.', 'Light → producers (photosynthesis, chemical energy) → consumers by feeding → decomposers; lost as heat. Losses: respiration (heat, movement), faeces, excretion, uneaten parts; ~10% passed on; limits chain length; eating lower in chain feeds more people.',
           'flow from Sun to producers to consumers [2]; three losses [3]; consequence (chain length / food production) [1] [6]')])
t18b = t

CPROC = [('photosynthesis', 'carbon dioxide is taken in by green plants and converted to glucose', 'carbon'), ('respiration', 'glucose is broken down in living cells, releasing carbon dioxide', 'carbon'),
         ('combustion', 'fossil fuels or wood are burned, releasing carbon dioxide', 'carbon'), ('decomposition', 'decomposers break down dead organisms, releasing carbon dioxide (and ammonium ions)', 'both'),
         ('fossilisation', 'dead organisms are buried and compressed over millions of years, forming coal, oil and gas', 'carbon'), ('feeding', 'carbon compounds in plants pass to animals when they eat', 'carbon'),
         ('nitrogen fixation', 'nitrogen gas is converted to ammonium or nitrate ions by bacteria (or by lightning)', 'nitrogen'), ('nitrification', 'ammonium ions are converted to nitrite and then nitrate ions by bacteria in the soil', 'nitrogen'),
         ('denitrification', 'nitrate ions are converted to nitrogen gas by bacteria in waterlogged, anaerobic soil', 'nitrogen'), ('absorption of nitrate', 'nitrate ions are taken up by root hair cells by active transport', 'nitrogen'),
         ('deamination', 'excess amino acids are broken down in the liver, forming urea', 'nitrogen')]
t = T('Carbon cycle and nitrogen cycle', 'carbon cycle', 'nitrogen cycle')
facts(t, [('nitrogen-fixing bacteria', 'bacteria that convert nitrogen gas from the air into compounds such as ammonium ions, some living in root nodules of legumes'),
          ('nitrifying bacteria', 'bacteria that convert ammonium ions to nitrite and then nitrate ions'), ('denitrifying bacteria', 'bacteria that convert nitrate ions to nitrogen gas in anaerobic conditions'),
          ('fossil fuel', 'a fuel such as coal, oil or natural gas formed from the remains of organisms over millions of years'), ('root nodules', 'swellings on the roots of legumes containing nitrogen-fixing bacteria'),
          ('carbon sink', 'a store, such as a forest, ocean or fossil fuel deposit, that removes and holds carbon from the atmosphere')])
mcqs(t, [('Which process removes carbon dioxide from the atmosphere?', 'Photosynthesis', 'Plants take in CO₂ to make glucose.', ['Respiration', 'Combustion', 'Decomposition']),
         ('Which bacteria convert ammonium ions into nitrate ions?', 'Nitrifying bacteria', 'Nitrification: ammonium → nitrite → nitrate.', ['Denitrifying bacteria', 'Nitrogen-fixing bacteria', 'Decomposers only']),
         ('Why do farmers plough waterlogged soils to aerate them?', 'To reduce denitrification by anaerobic bacteria', 'Aeration favours nitrifying bacteria, keeping nitrate in the soil.', ['To increase denitrification', 'To kill nitrogen-fixing bacteria', 'To stop photosynthesis']),
         ('Why do plants need nitrate ions?', 'To make amino acids and proteins', 'Nitrogen is needed for amino acids.', ['To make glucose', 'To make chlorophyll only from magnesium', 'To release energy'])])
shorts(t, [('State two processes that release carbon dioxide into the atmosphere.', 'Respiration; combustion; decomposition.', 'any two [2]'), ('Name the type of bacteria found in the root nodules of pea plants.', 'Nitrogen-fixing bacteria.', '[1]'),
           ('State two ways nitrogen gas can be converted into compounds that plants can use.', 'Nitrogen-fixing bacteria; lightning; the Haber process (fertiliser manufacture).', 'any two [2]')])
explain(t, [('Explain how the carbon in a dead tree is returned to the atmosphere.', 'Decomposers (bacteria and fungi) feed on the dead wood, digest it and respire, releasing carbon dioxide.', 'decomposers [1]; respiration releases CO₂ [1] [2]'),
            ('Explain why farmers grow legumes such as beans in rotation with other crops.', 'Root nodules contain nitrogen-fixing bacteria; when the plants are ploughed in, decomposition releases ammonium / nitrate, increasing soil fertility.', '[3]'),
            ('Explain how the nitrogen in protein in a dead animal becomes nitrate in the soil.', 'Decomposers break down protein to ammonium ions (ammonification); nitrifying bacteria convert ammonium to nitrite then nitrate.', 'decomposers / ammonium [1]; nitrifying bacteria [1]; nitrite → nitrate [1] [3]'),
            ('Explain why the concentration of carbon dioxide in the atmosphere has increased over the last 200 years.', 'Increased combustion of fossil fuels and deforestation (less photosynthesis, and burning releases CO₂).', '[2]')])
myths(t, [('Plants get their nitrogen directly from the air through their leaves.', 'Plants absorb nitrate ions from the soil through root hair cells; most cannot use nitrogen gas.'), ('Only animals release carbon dioxide; plants only absorb it.', 'Plants respire all the time and release CO₂; in light, photosynthesis may exceed respiration.'),
          ('Denitrifying bacteria add nitrate to the soil.', 'Denitrifying bacteria remove nitrate, converting it to nitrogen gas.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def cycle_proc(r, D):
    n, dsc, cyc = r.choice(CPROC)
    if D <= 2:
        return MQ(r, f'Which process is described: {dsc}?', cap(n), [cap(c[0]) for c in CPROC if c[0] != n], f'{cap(dsc)}: {n}.')
    o = r.sample([c for c in CPROC if c[0] != n], 2)
    return Q(f'Name the process in which: (i) {dsc}; (ii) {o[0][1]}; (iii) {o[1][1]}.', f'(i) {n} (ii) {o[0][0]} (iii) {o[1][0]}', f'(i) {n} [1] (ii) {o[0][0]} [1] (iii) {o[1][0]} [1] [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def co2_data(r, D):
    y0 = r.choice([1960, 1970, 1980, 1990])
    yrs = r.choice([20, 25, 30])
    c0 = {1960: 317, 1970: 326, 1980: 339, 1990: 354}[y0] + r.randint(-1, 1)
    c1 = round(c0 + yrs * r.uniform(1.6, 2.3))
    st = f'Measurements at an observatory showed the mean carbon dioxide concentration in the atmosphere was {c0} parts per million (ppm) in {y0} and {c1} ppm in {y0 + yrs}. (a) Calculate the percentage increase. (b) Calculate the mean rate of increase in ppm per year. (c) Suggest two human activities responsible for this increase.'
    return Q(st, f'(a) {fx(pct(c0, c1), 1)}% (b) {fx((c1 - c0) / yrs, 2)} ppm per year (c) burning fossil fuels; deforestation.',
             f'(a) ({c1} − {c0}) ÷ {c0} × 100 [1] = {fx(pct(c0, c1), 1)}% [1] (b) {c1 - c0} ÷ {yrs} = {fx((c1 - c0) / yrs, 2)} [1] (c) two activities [1] [4]', 'numerical', 4)


DECOMP = {'setup': lambda r, p: f'{p} put 5.0 g of dried leaf discs in mesh bags with soil, kept them at different temperatures for 4 weeks, then dried and reweighed them to find the percentage loss in mass.',
          'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[5, 15, 25, 35, 45], [10, 20, 30, 40, 50], [0, 10, 20, 30, 40]]), 'dv': ('percentage loss in mass', '%'),
          'y': lambda x, k: max(0.5, k * 40 * math.exp(-((x - 33) ** 2) / 260)), 'dp': 1,
          'controls': ['type and mass of leaves', 'type and mass of soil', 'moisture content', 'time', 'mesh size of bags'],
          'why': ('Decomposers (bacteria and fungi) use enzymes; up to about 30–35 °C, more kinetic energy means faster enzyme activity and respiration, so faster decay; at higher temperatures the enzymes are denatured.', 'decomposers / enzymes [1]; faster with more kinetic energy [1]; denaturation at high temperature [1] [3]'),
          'improve': ['dry the leaves to constant mass before weighing', 'use several bags at each temperature'],
          'control': 'Bags of leaves in sterilised (heated) soil — little decay should occur, showing that microorganisms cause the loss in mass.',
          'extra': [lambda r, d: ('Explain why the leaves were dried before weighing.', 'Water content varies; drying means only the mass of organic matter is compared.', '[2]'),
                    lambda r, d: ('State the role of decomposers in the carbon cycle.', 'They respire, releasing carbon dioxide from dead organic matter into the air.', '[1]')]}
add_practical(t, DECOMP, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (3, 4, 5), 'multi_step')
def ncycle_case(r, D):
    crop = r.choice(['maize', 'wheat', 'rice', 'cassava'])
    intro = f'A farmer in {city(r)} grows {crop} in a field that sometimes becomes waterlogged. In alternate years she grows clover (a legume) and ploughs it into the soil.'
    parts = [lambda r: ('Explain how growing and ploughing in clover increases the nitrate in the soil.', 'Clover has root nodules with nitrogen-fixing bacteria, which convert nitrogen gas to ammonium; when ploughed in, decomposers release ammonium, which nitrifying bacteria convert to nitrate.', 'nitrogen-fixing bacteria in nodules [1]; decomposition [1]; nitrification [1] [3]'),
             lambda r: ('Explain why nitrate is lost from the soil when it is waterlogged.', 'Waterlogged soil is anaerobic; denitrifying bacteria convert nitrate to nitrogen gas.', 'anaerobic [1]; denitrifying bacteria [1] [2]'),
             lambda r: (f'Explain why the {crop} needs nitrate ions.', 'To make amino acids and proteins for growth.', '[2]'),
             lambda r: ('Describe how nitrate ions are absorbed by the roots.', 'By active transport into root hair cells, using energy from respiration, against a concentration gradient.', '[2]'),
             lambda r: ('Describe one way the farmer could reduce waterlogging and explain the benefit.', 'Drain or plough the soil to aerate it; aerobic conditions favour nitrifying bacteria and reduce denitrification.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the carbon cycle and explain how human activities have changed the concentration of carbon dioxide in the atmosphere.', 'Photosynthesis removes CO₂; respiration, decomposition and combustion return it; feeding passes carbon along food chains; fossilisation stores it. Humans burn fossil fuels and cut down forests, increasing CO₂.',
           'photosynthesis [1]; respiration / decomposition [1]; feeding [1]; fossilisation / combustion [1]; human activities [2] [6]'),
          ('Describe the roles of microorganisms in the nitrogen cycle.', 'Nitrogen-fixing bacteria (soil and root nodules) convert N₂ to ammonium; decomposers convert protein / urea to ammonium; nitrifying bacteria convert ammonium to nitrite and nitrate; denitrifying bacteria convert nitrate to N₂ in anaerobic soil.',
           'nitrogen fixation [2]; decomposition [1]; nitrification [2]; denitrification [1] [6]')])
t18c = t

t = T('Populations: factors affecting population size and the sigmoid growth curve', 'populations', 'factors affecting population size', 'sigmoid growth curve')
facts(t, [('population', 'a group of organisms of one species, living in the same area at the same time'), ('community', 'all of the populations of different species in an ecosystem'),
          ('ecosystem', 'a unit containing the community of organisms and their environment, interacting together'), ('sigmoid growth curve', 'an S-shaped curve showing lag, exponential (log), stationary and death phases of population growth'),
          ('quadrat', 'a square frame of known area used to sample organisms that do not move'), ('limiting factor', 'something present in short supply that restricts the growth of a population')])
mcqs(t, [('In which phase of a sigmoid growth curve is the birth rate equal to the death rate?', 'Stationary phase', 'The population stays constant.', ['Lag phase', 'Exponential (log) phase', 'Death phase']),
         ('Which factor does not usually limit the size of a population?', 'The colour of the organisms', 'Food supply, predation and disease are limiting factors.', ['Food supply', 'Predation', 'Disease']),
         ('Why should quadrats be placed randomly?', 'To avoid bias, so the sample is representative', 'Random placement prevents choosing areas with more or fewer organisms.', ['To find the most organisms', 'To make counting quicker', 'To avoid trampling plants']),
         ('Why is there a lag phase when yeast is added to fresh sugar solution?', 'The cells are adjusting and making enzymes before dividing rapidly', 'Few cells and time to adapt to new conditions.', ['There is no food', 'Toxic waste has built up', 'All the cells are dying'])])
shorts(t, [('State three factors that affect the rate of growth of a population.', 'Food supply; competition; predation; disease.', 'any three [3]'), ('Name the four phases of a sigmoid population growth curve.', 'Lag, exponential (log), stationary, death.', 'all four [2]; two or three [1] [2]')])
explain(t, [('Explain why a population of bacteria in a flask stops increasing after a time.', 'Nutrients run out and toxic waste builds up (limiting factors), so the death rate rises to equal the birth rate.', 'nutrients used up [1]; toxic waste [1]; death rate = birth rate [1] [3]'),
            ('Explain why the human population has grown so rapidly over the last 250 years.', 'Better food supply, medicine, vaccination, sanitation and clean water reduced the death rate while birth rates stayed high.', '[3]'),
            ('Explain the shape of the exponential (log) phase of a yeast growth curve.', 'Plenty of food and space with little waste, so cells divide rapidly; birth rate much greater than death rate; numbers double at regular intervals.', '[2]'),
            ('Explain why the death phase occurs in a closed culture of yeast.', 'Food is used up and ethanol (toxic) accumulates, so the death rate exceeds the birth rate.', '[2]')])
myths(t, [('A population in the stationary phase has stopped reproducing.', 'Organisms still reproduce; the birth rate equals the death rate.'), ('Placing quadrats where there are most plants gives the best estimate.', 'Quadrats must be placed randomly to avoid bias.')])


@t.add('C3', (2, 3, 4, 5), 'case')
def quadrat(r, D):
    sp = r.choice(['daisies', 'dandelions', 'clover plants', 'buttercups', 'plantains', 'limpets'])
    qa = r.choice([0.25, 0.5, 1.0])
    L, W = r.choice([(20, 30), (40, 50), (25, 60), (50, 80), (100, 120)])
    n = 10
    lam = r.uniform(2, 9) * qa / 0.5
    counts = [max(0, round(r.gauss(lam, lam ** 0.5))) for _ in range(n)]
    tot = sum(counts)
    mean = tot / n
    dens = mean / qa
    pop = dens * L * W
    place = 'a rocky shore' if sp == 'limpets' else 'a school field'
    intro = f'{person(r)} estimated the population of {sp} on {place} in {city(r)} measuring {L} m × {W} m. {n} quadrats, each {fx(qa, 2)} m², were placed at random. Number of {sp} in each quadrat: {", ".join(map(str, counts))}.'
    parts = [lambda r: (f'Calculate the mean number of {sp} per quadrat.', fx(mean, 2), f'{tot} ÷ {n} [1] = {fx(mean, 2)} [1] [2]'),
             lambda r: (f'Calculate the estimated population of {sp} on the whole area.', big(pop), f'density = {fx(mean, 2)} ÷ {fx(qa, 2)} = {fx(dens, 2)} per m² [1]; area = {L * W} m² [1]; {fx(dens, 2)} × {L * W} = {big(pop)} [1] [3]'),
             lambda r: ('Describe how the quadrats could be placed at random.', 'Lay two tape measures at right angles as axes; use a random number generator to pick coordinates; place the quadrat at each.', 'tapes / grid [1]; random numbers for coordinates [1] [2]'),
             lambda r: ('Suggest how the estimate could be made more reliable.', 'Use more quadrats (and calculate the mean).', '[1]'),
             lambda r: (f'Suggest one environmental factor that could affect the distribution of {sp} and how it could be measured.', 'Light intensity (light meter); soil moisture or pH (meter / probe); trampling.', 'factor [1]; method [1] [2]'),
             lambda r: (f'Suggest why counting {sp} is easier with quadrats than counting animals such as beetles.', f'{cap(sp)} do not move (or move very slowly), so they are not counted twice or missed.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


@t.add('C3', (2, 3, 4, 5), 'multi_step')
def sigmoid(r, D):
    org = r.choice(['yeast cells', 'bacteria', 'duckweed fronds', 'Paramecium'])
    K = r.choice([400, 500, 600, 800, 1000])
    N0 = r.choice([5, 8, 10])
    rr = r.uniform(0.55, 0.8)
    ts = list(range(0, 16, 2))
    Ns = [round(K / (1 + (K / N0 - 1) * math.exp(-rr * t_))) for t_ in ts]
    death = D >= 5
    if death:
        ts += [16, 18]
        Ns += [round(Ns[-1] * 0.85), round(Ns[-1] * 0.6)]
    unit = 'hours' if org in ('yeast cells', 'bacteria') else 'days'
    st = f'A population of {org} was grown in a container in a laboratory in {city(r)}. Time / {unit}: {", ".join(map(str, ts))}. Number (thousands per cm³): {", ".join(map(str, Ns))}.' if unit == 'hours' else \
        f'A population of {org} was grown in a container in a laboratory in {city(r)}. Time / {unit}: {", ".join(map(str, ts))}. Number: {", ".join(map(str, Ns))}.'
    i = max(range(1, len(ts) - 1 - (2 if death else 0)), key=lambda j: Ns[j + 1] - Ns[j])
    rate = (Ns[i + 1] - Ns[i]) / 2
    st += f' (a) Calculate the rate of increase in number between {ts[i]} and {ts[i + 1]} {unit}. (b) Name the phase of growth between {ts[-3 if not death else -5]} and {ts[-1 if not death else -3]} {unit} and explain it. (c) Name the phase between {ts[i]} and {ts[i + 1]} {unit}.'
    ans = f'(a) {fx(rate, 1)} per {unit[:-1]} (b) stationary phase: limiting factors (food, space, waste) mean the birth rate equals the death rate (c) exponential (log) phase'
    key = f'(a) ({Ns[i + 1]} − {Ns[i]}) ÷ 2 [1] = {fx(rate, 1)} [1] (b) stationary [1]; limiting factor [1]; birth = death [1] (c) exponential [1]'
    m = 6
    if death:
        st += f' (d) Explain the change between 16 and 18 {unit}.'
        ans += ' (d) death phase: food has run out and toxic waste has built up, so the death rate exceeds the birth rate.'
        key += ' (d) death phase [1]; reason [1]'
        m = 8
    return Q(st, ans, key + f' [{m}]', 'multi_step', m)


@t.add('C3', (1, 2, 3), 'numerical')
def doubling(r, D):
    org, g = r.choice([('bacteria', 20), ('bacteria', 30), ('yeast cells', 90), ('bacteria', 25)])
    n0 = r.choice([10, 50, 100, 200])
    k = r.choice([3, 4, 5, 6])
    tm = g * k
    if D <= 2:
        return NQ(r, f'A population of {n0} {org} doubles every {g} minutes in ideal conditions. How many will there be after {tm} minutes?', n0 * 2 ** k, [n0 * 2 * k, n0 * 2 ** (k - 1), n0 * k, n0 * 2 ** (k + 1)], '', f'{k} doublings: {n0} × 2^{k} = {n0 * 2 ** k}.', f=lambda v: big(v))
    return Q(f'A population of {n0} {org} doubles every {g} minutes. (a) Calculate the number after {tm} minutes. (b) Explain why such growth cannot continue indefinitely in a flask.',
             f'(a) {big(n0 * 2 ** k)} (b) nutrients run out, toxic waste accumulates and space is limited, so the death rate increases.', f'(a) {k} doublings [1]; {big(n0 * 2 ** k)} [1] (b) limiting factor [1] [3]', 'numerical', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def human_pop(r, D):
    a, b = r.choice([(1.0, 1800), (1.6, 1900), (2.5, 1950)])
    c = 8.0
    intro = f'The world human population was about {a} billion in {b} and about {c} billion in 2023. A demographer in {city(r)} predicts it will level off later this century.'
    parts = [lambda r: ('Calculate the percentage increase in population.', f'{fx(pct(a, c), 0)}%', f'({c} − {a}) ÷ {a} × 100 [1] = {fx(pct(a, c), 0)}% [1] [2]'),
             lambda r: ('Calculate the mean increase in billions per year.', f'{fx((c - a) / (2023 - b), 3)} billion per year', f'{fx(c - a)} ÷ {2023 - b} [1] = {fx((c - a) / (2023 - b), 3)} [1] [2]'),
             lambda r: ('Explain two reasons for the rapid increase.', 'Improved food production; better medicine / vaccines / sanitation lowering death rates (especially infant mortality).', '[2]'),
             lambda r: ('Suggest two factors that could cause the population to level off.', 'Family planning / contraception lowering birth rate; limits of food, water and space; disease.', '[2]'),
             lambda r: ('State the phase of the sigmoid curve the human population has been in for the last 200 years.', 'Exponential (log) phase.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe and explain the shape of a sigmoid population growth curve for yeast grown in a flask of sugar solution.', 'Lag: few cells, adapting, slow growth. Exponential: plenty of food, rapid division, numbers double regularly. Stationary: limiting factors (food, space, toxins); birth = death. Death: food used up, ethanol toxic, death > birth.',
           'lag [1]; exponential with reason [2]; stationary with reason [2]; death phase [1] [6]')])
t18d = t
CHAPTERS[8] = [t18a, t18b, t18c, t18d]

# ===================================================================== 9 Human influences on ecosystems
t = T('Food supply: monocultures, intensive livestock production and use of fertilisers and pesticides', 'food supply', 'monocultures', 'intensive livestock production', 'use of fertilisers and pesticides')
facts(t, [('monoculture', 'a large area of land on which only one type of crop is grown'), ('intensive livestock production', 'rearing large numbers of animals in a small space, often indoors, with controlled food and conditions to maximise output'),
          ('fertiliser', 'a substance added to soil to provide mineral ions such as nitrate, phosphate and potassium for plant growth'), ('pesticide', 'a chemical that kills organisms that damage crops'),
          ('herbicide', 'a pesticide that kills weeds'), ('insecticide', 'a pesticide that kills insects'), ('bioaccumulation', 'the build-up of a persistent substance, such as a pesticide, in organisms at higher trophic levels of a food chain')])
mcqs(t, [('Which is a negative impact of monocultures?', 'Reduced biodiversity', 'Removing other plants and animals reduces the variety of species.', ['Increased number of habitats', 'More species of insects', 'Less need for pesticides']),
         ('Why do farmers add nitrate fertilisers to crops?', 'To provide nitrogen for making amino acids and proteins', 'Nitrate is needed for protein synthesis and growth.', ['To provide magnesium for chlorophyll', 'To kill pests', 'To increase soil acidity']),
         ('Which is a disadvantage of intensive livestock production?', 'Disease spreads easily between crowded animals', 'Crowding increases the spread of pathogens, so antibiotics are often used.', ['Animals use more energy moving', 'Meat production falls', 'Animals need more space']),
         ('Which has increased world food production most in the last century?', 'Agricultural machinery, fertilisers, pesticides and selective breeding', 'Modern technology raises yields.', ['Growing fewer crops', 'Removing irrigation', 'Using less land and no fertiliser'])])
shorts(t, [('State two reasons for famine.', 'Drought / climate change; war / conflict; rising population; poverty; crop failure due to pests or disease.', 'any two [2]'), ('State two advantages of using pesticides.', 'Fewer crops lost to pests; higher yield; better quality produce.', 'any two [2]')])
explain(t, [('Explain why monocultures are more likely to suffer pest outbreaks.', 'A large area of one crop provides abundant food for its pests, which can spread easily from plant to plant; predators have fewer habitats.', '[2]'),
            ('Explain how intensive livestock production increases the efficiency of meat production.', 'Animals are kept warm and their movement is restricted, so less energy is used in respiration for heat and movement; more goes into growth.', 'less movement / heat loss [1]; more energy to growth [1] [2]'),
            ('Explain how using pesticides on crops can harm organisms that are not pests.', 'They may kill beneficial insects such as pollinators and predators; persistent pesticides bioaccumulate along food chains and harm top predators.', '[3]'),
            ('Explain why using antibiotics routinely in intensive livestock farming is a concern.', 'It selects for antibiotic-resistant bacteria, which may spread to humans.', '[2]')])
myths(t, [('Adding more fertiliser always gives a proportionally bigger yield.', 'Yield increases less and less as fertiliser increases (another factor becomes limiting), and excess fertiliser is wasted and may cause pollution.'),
          ('Monocultures increase biodiversity because many crop plants grow.', 'Monocultures reduce biodiversity: only one species is grown and habitats are removed.')])

FERT = {'setup': lambda r, p: f'{p} grew duckweed in beakers of mineral solution containing different concentrations of nitrate fertiliser and counted the number of fronds after 14 days. Each beaker started with 10 fronds.',
        'iv': ('concentration of fertiliser', 'g/dm³'), 'xs': lambda r: r.choice([[0, 0.5, 1.0, 1.5, 2.0], [0, 1, 2, 3, 4], [0, 0.25, 0.5, 1.0, 2.0]]), 'dv': ('number of fronds', ''),
        'y': lambda x, k: 14 + k * 60 * x / (x + 0.6), 'dp': 0, 'noise': 0.05,
        'controls': ['volume of solution', 'temperature', 'light intensity', 'starting number of fronds', 'time'],
        'why': ('Nitrate is used to make amino acids and proteins for growth, so more fronds are produced; at high concentrations another factor (e.g. light, space) becomes limiting, so the increase levels off.', 'nitrate for proteins / growth [1]; more growth / fronds [1]; another limiting factor [1] [3]'),
        'improve': ['count the fronds in several beakers at each concentration', 'measure the dry mass of the duckweed instead of counting fronds'],
        'control': 'A beaker with no added fertiliser (distilled water / complete solution without nitrate) — shows the growth that occurs without the fertiliser.',
        'extra': [lambda r, d: ('Calculate the percentage increase in the number of fronds from 0 g/dm³ to the highest concentration.', f'{fx(pct(d["means"][0], d["means"][-1]), 0)}%', f'({fx(d["means"][-1], 1)} − {fx(d["means"][0], 1)}) ÷ {fx(d["means"][0], 1)} × 100 [1] = {fx(pct(d["means"][0], d["means"][-1]), 0)}% [1] [2]')]}
add_practical(t, FERT, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (2, 3, 4, 5), 'numerical')
def bioacc(r, D):
    chem = r.choice(['DDT', 'an insecticide', 'a mercury compound'])
    chain = r.choice([('water', 'plankton', 'small fish', 'large fish', 'fish-eating birds'), ('water', 'algae', 'water fleas', 'small fish', 'herons'), ('soil water', 'earthworms', 'thrushes', 'sparrowhawks', None)])
    w = r.choice([0.00002, 0.00005, 0.0001])
    f = [round(r.uniform(400, 1000)), round(r.uniform(8, 15)), round(r.uniform(5, 12)), round(r.uniform(5, 10))]
    vals = [w]
    for x in f:
        vals.append(vals[-1] * x)
    lv = [c for c in chain if c]
    vals = [float(sf(v, 3).replace(',', '')) for v in vals[:len(lv)]]
    tab = '; '.join(f'{o}: {nn(v)}' for o, v in zip(lv, vals))
    top = lv[-1]
    fac = vals[-1] / vals[1]
    st = f'The concentration of {chem} (parts per million) was measured in a food chain near {city(r)}: {tab}. (a) Calculate how many times greater the concentration is in the {top} than in the {lv[1]}. (b) Explain why the concentration increases along the food chain. (c) Suggest why the {top} may be harmed even though the concentration in the water is very low.'
    return Q(st, f'(a) {sf(fac, 3)} times (b) {chem} is persistent (not broken down or excreted); each organism eats many from the level below, so it accumulates (bioaccumulation). (c) It reaches toxic concentrations in top predators, e.g. thin eggshells or poisoning.',
             f'(a) {nn(vals[-1])} ÷ {nn(vals[1])} [1] = {sf(fac, 3)} [1] (b) not broken down / excreted [1]; many prey eaten [1] (c) toxic dose [1] [5]', 'numerical', 5)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def yield_q(r, D):
    crop = r.choice(['wheat', 'maize', 'rice', 'potatoes', 'soya beans'])
    y0 = round(r.uniform(2.0, 4.0), 1)
    y1 = round(y0 * r.uniform(1.3, 2.0), 1)
    area = r.choice([20, 50, 120, 250])
    if D == 1:
        return NQ(r, f'Using fertiliser increased the yield of {crop} from {y0} to {y1} tonnes per hectare. What is the percentage increase?', pct(y0, y1), [(y1 - y0), y1 / y0 * 100, pct(y1, y0) * -1], '%', f'({y1} − {y0}) ÷ {y0} × 100 = {fx(pct(y0, y1), 0)}%.', f=lambda v: fx(v, 0))
    st = f'A farm in {city(r)} grows {crop} on {area} hectares. Without fertiliser the yield was {y0} tonnes per hectare; with fertiliser it was {y1} tonnes per hectare. (a) Calculate the extra mass of {crop} produced on the whole farm. (b) Calculate the percentage increase in yield. (c) State one environmental risk of using too much fertiliser.'
    return Q(st, f'(a) {fx((y1 - y0) * area, 1)} tonnes (b) {fx(pct(y0, y1), 0)}% (c) fertiliser washes (leaches) into rivers and lakes, causing eutrophication.',
             f'(a) ({y1} − {y0}) × {area} [1] = {fx((y1 - y0) * area, 1)} t [1] (b) {fx(pct(y0, y1), 0)}% [1] (c) eutrophication / leaching [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def farm_case(r, D):
    crop = r.choice(['oil palm', 'soya', 'maize', 'wheat', 'rice'])
    intro = f'A large company near {city(r)} has replaced mixed farmland with a {crop} monoculture. It uses fertilisers, herbicides and insecticides, and also runs an intensive chicken unit housing 40 000 birds.'
    parts = [lambda r: ('Explain two negative impacts of the monoculture on the environment.', 'Reduced biodiversity (one species; habitats removed); pests spread easily so more pesticide used; soil minerals depleted; hedgerows removed.', 'two impacts explained [2] [2]'),
             lambda r: ('Explain why the company uses herbicides.', 'To kill weeds that compete with the crop for light, water and mineral ions, increasing yield.', '[2]'),
             lambda r: ('Explain why insecticides might reduce the number of birds in the area.', 'Insects that birds eat are killed; insecticide may bioaccumulate in birds.', '[2]'),
             lambda r: ('Describe two advantages and two disadvantages of the intensive chicken unit.', 'Advantages: cheap meat / eggs, efficient energy transfer, controlled feeding. Disadvantages: disease spread, antibiotic use, poor animal welfare, waste pollution.', '[4]'),
             lambda r: ('Suggest why there is concern about using large amounts of antibiotics in the chicken unit.', 'It selects for antibiotic-resistant bacteria that may infect humans.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Discuss how modern agricultural technology has increased food production, and describe the negative impacts of monocultures and intensive livestock production.', 'Machinery, fertilisers, pesticides, selective breeding increase yields. Monocultures: reduced biodiversity, pests, pesticide use, soil depletion. Intensive livestock: disease, antibiotic use and resistance, pollution from waste, welfare.',
           'technology increasing production [2]; monoculture impacts [2]; livestock impacts [2] [6]')])
t19a = t

t = T('Habitat destruction and deforestation', 'habitat destruction', 'deforestation')
facts(t, [('deforestation', 'the large-scale removal of forest, usually for timber, farmland or building'), ('habitat destruction', 'the damage or removal of the environment in which organisms live'),
          ('biodiversity', 'the number of different species that live in an area'), ('soil erosion', 'the removal of topsoil by wind or rain, especially when it is not held by plant roots'),
          ('extinction', 'the permanent loss of all members of a species')])
mcqs(t, [('Which is a reason for habitat destruction?', 'Clearing land for farming and housing', 'Land is cleared for agriculture, building and extraction.', ['Planting hedgerows', 'Creating nature reserves', 'Using seed banks']),
         ('Why does deforestation increase atmospheric carbon dioxide?', 'Less photosynthesis, and burning or decomposition of wood releases CO₂', 'Trees remove CO₂ and store carbon.', ['Trees release CO₂ by photosynthesis', 'Soil absorbs more CO₂', 'Animals stop respiring']),
         ('How can deforestation cause flooding?', 'Fewer roots hold soil and less water is taken up and transpired, so more runs off', 'Run-off increases and eroded soil blocks rivers.', ['Trees absorb rain from the air', 'More evaporation occurs', 'Soil becomes more compact and absorbent'])])
shorts(t, [('State three reasons why forests are cut down.', 'Timber; land for crops or cattle; building; mining; roads.', 'any three [3]'), ('State two effects of deforestation on soil.', 'Soil erosion; loss of nutrients (leaching).', '[2]')])
explain(t, [('Explain how deforestation can lead to extinction of species.', 'Habitats and food sources are destroyed; species that live only in the forest cannot survive or reproduce.', '[2]'),
            ('Explain how deforestation can change the local water cycle.', 'Less transpiration means less water vapour enters the air, so less rainfall; soil becomes drier.', '[2]'),
            ('Explain why soil in a deforested area becomes less fertile.', 'Without roots, rain washes away topsoil (erosion) and mineral ions are leached; there is no leaf litter for decomposers to recycle nutrients.', 'erosion [1]; leaching / no recycling [1] [2]'),
            ('Explain why habitat destruction reduces biodiversity even in nearby areas.', 'Remaining habitats become fragmented, so populations are small and isolated, food webs are disrupted, and species may be unable to find mates.', '[2]')])
myths(t, [('Deforestation reduces carbon dioxide because there are fewer trees respiring.', 'Deforestation increases CO₂: less photosynthesis, and burning or decay of wood releases CO₂.'), ('Cutting down forests only affects the trees.', 'It destroys habitats, reduces biodiversity, causes soil erosion and flooding and affects climate.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def forest_loss(r, D):
    reg = r.choice(['the Amazon basin', 'Borneo', 'the Congo basin', 'Madagascar', 'Sumatra', 'Central America'])
    a0 = r.choice([120, 250, 400, 650, 3000, 5400])
    y0 = r.choice([1990, 1995, 2000])
    yrs = r.choice([15, 20, 25])
    loss = r.uniform(0.08, 0.3)
    a1 = round(a0 * (1 - loss))
    if D == 1:
        return NQ(r, f'The forest area in {reg} fell from {a0} to {a1} thousand km². What is the percentage decrease?', (a0 - a1) / a0 * 100, [(a0 - a1) / a1 * 100, a1 / a0 * 100, (a0 - a1)], '%', f'({a0} − {a1}) ÷ {a0} × 100 = {fx((a0 - a1) / a0 * 100, 1)}%.', f=lambda v: fx(v, 1))
    rate = (a0 - a1) / yrs
    left = a1 / rate
    st = f'Satellite images show the forest area in {reg} fell from {a0} thousand km² in {y0} to {a1} thousand km² in {y0 + yrs}. (a) Calculate the percentage decrease. (b) Calculate the mean rate of loss per year. (c) Assuming this rate continues, calculate how many more years it would take for all the forest to be lost. (d) State two consequences of this deforestation.'
    return Q(st, f'(a) {fx((a0 - a1) / a0 * 100, 1)}% (b) {fx(rate, 2)} thousand km² per year (c) {fx(left, 0)} years (d) loss of habitats / extinction; soil erosion; flooding; increased CO₂.',
             f'(a) {a0 - a1} ÷ {a0} × 100 = {fx((a0 - a1) / a0 * 100, 1)}% [1] (b) {a0 - a1} ÷ {yrs} = {fx(rate, 2)} [1] (c) {a1} ÷ {fx(rate, 2)} = {fx(left, 0)} [1] (d) two consequences [2] [5]', 'numerical', 5)


@t.add('C3', (2, 3, 4, 5), 'case')
def runoff(r, D):
    f = round(r.uniform(4, 12), 1)
    c = round(f * r.uniform(3, 8), 1)
    s0, s1 = round(r.uniform(0.1, 0.6), 1), round(r.uniform(5, 20), 1)
    st = f'Two plots on a hillside near {city(r)} received the same rainfall. Plot A was forested; plot B had been cleared. Water run-off: A {f}%, B {c}% of rainfall. Soil lost: A {s0} tonnes per hectare, B {s1} tonnes per hectare per year. (a) Calculate how many times more soil was lost from plot B. (b) Explain the difference in run-off. (c) Explain why the soil lost from B could cause flooding further downstream.'
    return Q(st, f'(a) {fx(s1 / s0, 1)} times (b) In A, roots and leaf litter hold water and soil; trees take up and transpire water; B has no roots so water runs off. (c) Soil washes into rivers, raising the river bed so it overflows more easily.',
             f'(a) {s1} ÷ {s0} = {fx(s1 / s0, 1)} [1] (b) roots hold soil / absorb water [1]; transpiration / interception [1] (c) silt in rivers [1] [4]', 'case', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def defor_case(r, D):
    use = r.choice(['cattle ranching', 'oil palm plantations', 'soya farming', 'timber', 'gold mining'])
    intro = f'In a region of tropical rainforest, large areas are being cleared for {use}. Scientists report fewer species in the remaining forest, more frequent floods, and a fall in local rainfall.'
    parts = [lambda r: ('Explain why there are fewer species in the remaining forest.', 'Habitat loss and fragmentation; food webs disrupted; small isolated populations cannot find mates.', '[2]'),
             lambda r: ('Explain why local rainfall has fallen.', 'Fewer trees means less transpiration, so less water vapour enters the atmosphere to form clouds.', '[2]'),
             lambda r: ('Explain how clearing the forest contributes to climate change.', 'Less photosynthesis removing CO₂; burning and decay of trees release CO₂, an enhanced greenhouse effect.', '[3]'),
             lambda r: ('Explain why floods have become more frequent.', 'Without roots and leaf litter, rain runs off quickly; eroded soil silts up rivers.', '[2]'),
             lambda r: ('Suggest two ways of reducing the impact of deforestation.', 'Replant trees (reforestation); sustainable logging; protected areas; laws and education; buying certified products.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the reasons for habitat destruction and explain the undesirable effects of deforestation.', 'Reasons: farming, housing, extraction of resources (timber, minerals), roads, pollution of aquatic habitats. Effects: loss of habitats and biodiversity, extinction, soil erosion, flooding, increased CO₂ and climate change, less rainfall.',
           'two reasons [2]; four effects explained [4] [6]')])
t19b = t

t = T('Pollution: water pollution, eutrophication, non-biodegradable plastics and greenhouse gases', 'pollution', 'water pollution', 'eutrophication', 'non-biodegradable plastics', 'greenhouse gases')
EUTRO = ['fertiliser (nitrate / phosphate) leaches into the water', 'algae grow rapidly (algal bloom)', 'algae cover the surface and block light, so plants below die', 'decomposers (aerobic bacteria) feed on the dead plants and multiply',
         'the bacteria respire aerobically, using up dissolved oxygen', 'fish and other animals die from lack of oxygen']
facts(t, [('eutrophication', 'the process in which excess nutrients in water cause rapid growth of algae and, eventually, a fall in dissolved oxygen'), ('pollution', 'the release of substances into the environment that harm living organisms'),
          ('non-biodegradable', 'not broken down by decomposers'), ('greenhouse gas', 'a gas such as carbon dioxide or methane that absorbs heat radiated from the Earth and contributes to global warming'),
          ('enhanced greenhouse effect', 'the increase in the greenhouse effect caused by extra greenhouse gases from human activities, leading to climate change'), ('algal bloom', 'a rapid growth of algae in water rich in nutrients')])
mcqs(t, [('In eutrophication, what directly causes the fall in dissolved oxygen?', 'Respiration of decomposer bacteria feeding on dead plants', 'Aerobic bacteria use up the oxygen.', ['Photosynthesis by algae', 'Fertiliser reacting with oxygen', 'Fish respiration only']),
         ('Which gas is released by cattle and rice paddies and is a greenhouse gas?', 'Methane', 'Methane comes from cattle digestion, rice fields and landfill.', ['Oxygen', 'Nitrogen', 'Hydrogen']),
         ('Why are non-biodegradable plastics a problem in the sea?', 'They persist for a long time and can be eaten by or trap animals', 'Plastic is not broken down by decomposers.', ['They dissolve and add nutrients', 'They are decomposed quickly by bacteria', 'They increase dissolved oxygen']),
         ('Which human activity is the main source of extra carbon dioxide in the atmosphere?', 'Combustion of fossil fuels', 'Burning coal, oil and gas releases CO₂.', ['Planting trees', 'Photosynthesis by crops', 'Building wind turbines'])])
shorts(t, [('State two sources of water pollution.', 'Sewage; fertiliser run-off; chemical waste from factories; discarded plastics.', 'any two [2]'), ('Name two greenhouse gases.', 'Carbon dioxide; methane.', '[2]'),
           ('State two effects of climate change.', 'Rising sea levels; extreme weather; changes in species distribution; crop failure.', 'any two [2]')])
explain(t, [('Explain how untreated sewage can lead to the death of fish in a river.', 'Sewage provides nutrients and organic matter; bacteria feed on it and multiply, respiring aerobically and using up dissolved oxygen, so fish suffocate.', 'bacteria decompose sewage [1]; aerobic respiration uses oxygen [1]; fish die [1] [3]'),
            ('Explain how increased greenhouse gases lead to global warming.', 'Greenhouse gases absorb infrared (heat) radiation emitted from the Earth\'s surface and re-radiate it, so less heat escapes to space and the temperature rises.', '[3]'),
            ('Explain why discarded plastic can harm seabirds.', 'Birds mistake plastic for food; it fills the stomach so they starve, or they become entangled.', '[2]'),
            ('Explain why eutrophication is more likely after heavy rain on recently fertilised fields.', 'Rain dissolves soluble fertiliser and washes (leaches) it into rivers and lakes.', '[2]')])
myths(t, [('In eutrophication, fish die because the algae poison them.', 'Fish die because decomposer bacteria use up dissolved oxygen when they respire.'), ('The greenhouse effect is entirely caused by humans.', 'The natural greenhouse effect keeps the Earth warm; humans have enhanced it.'),
          ('Algae use up all the oxygen in eutrophication by photosynthesis.', 'Algae release oxygen when they photosynthesise; oxygen falls because decomposers respire.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def eutro_order(r, D):
    if D <= 2:
        i = r.randrange(1, 6)
        return MQ(r, f'In eutrophication, what happens immediately after this stage: "{EUTRO[i - 1]}"?', cap(EUTRO[i]), [cap(e) for j, e in enumerate(EUTRO) if j != i], f'Sequence: ' + ' → '.join(EUTRO) + '.')
    lab = list('ABCDEF')
    order = list(range(6))
    r.shuffle(order)
    st = 'The stages of eutrophication are listed in the wrong order: ' + '; '.join(f'{lab[k]} {EUTRO[j]}' for k, j in enumerate(order)) + '. Put the letters in the correct order.'
    corr = ''.join(lab[order.index(j)] for j in range(6))
    return Q(st, ' → '.join(corr), f'{" ".join(corr)}: all correct [3]; four or five in correct positions [2]; two or three [1] [3]', 'short', 3)


DO = {'setup': lambda r, p: f'{p} measured dissolved oxygen in a river at different distances downstream from a sewage outlet, taking three samples at each site.',
      'iv': ('distance downstream', 'm'), 'xs': lambda r: r.choice([[0, 100, 200, 400, 800, 1600], [0, 50, 100, 200, 400, 800], [0, 200, 400, 600, 800, 1000]]), 'dv': ('dissolved oxygen concentration', 'mg/dm³'),
      'y': lambda x, k: 9.5 - k * 6.5 * math.exp(-((x - 120) / 250) ** 2) if x > 0 else 9.0 - k * 2.0, 'dp': 1, 'noise': 0.03,
      'controls': ['time of day', 'depth of sampling', 'water temperature', 'method of measurement (same meter)'],
      'trend': lambda d: f'The dissolved oxygen falls just below the outlet to a minimum of about {fx(min(d["means"]), 1)} mg/dm³ at {d["xs"][min(range(len(d["means"])), key=lambda i: d["means"][i])]} m, then rises again further downstream.',
      'why': ('Sewage provides organic matter; bacteria multiply and respire aerobically, using up oxygen; further downstream the sewage has been broken down and oxygen dissolves from the air and is released by photosynthesis, so levels recover.', 'bacteria decompose sewage [1]; respiration uses oxygen [1]; recovery downstream [1] [3]'),
      'improve': ['take samples at the same time of day', 'measure the oxygen upstream of the outlet as a comparison'],
      'control': 'Take samples upstream of the outlet — shows the normal oxygen concentration without sewage.',
      'extra': [lambda r, d: ('Suggest which animals would be found where dissolved oxygen is lowest, and why.', 'Sludge worms / rat-tailed maggots / bloodworms (indicator species tolerant of low oxygen); fish and mayfly larvae need more oxygen.', '[2]'),
                lambda r, d: ('Explain why the oxygen concentration falls further on warm days.', 'Warm water holds less dissolved oxygen, and bacteria respire faster.', '[2]')]}
add_practical(t, DO, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (2, 3, 4, 5), 'numerical')
def plastic_q(r, D):
    items = [('plastic bag', 20), ('plastic bottle', 450), ('fishing line', 600), ('polystyrene cup', 50), ('paper towel', 0.05), ('cotton T-shirt', 0.5), ('banana peel', 0.1), ('drinks can (aluminium)', 200)]
    a, b = r.sample(items, 2)
    mass = r.choice([8, 10, 12, 15])
    frac = r.choice([20, 30, 40, 50])
    pop = r.choice([2.5, 4.0, 6.5, 9.0])
    st = (f'Estimated times to break down in the environment: {a[0]} {fx(a[1], 2)} years; {b[0]} {fx(b[1], 2)} years. (a) Explain why some items take hundreds of years to break down. '
          f'(b) A city of {pop} million people in {city(r)} produces {mass} kg of plastic waste per person per year, of which {frac}% is recycled. Calculate the mass of plastic not recycled each year, in tonnes.')
    tn = pop * 1e6 * mass * (100 - frac) / 100 / 1000
    return Q(st, f'(a) Plastics are non-biodegradable: decomposers have no enzymes to break them down. (b) {big(tn)} tonnes',
             f'(a) non-biodegradable / no enzymes in decomposers [2] (b) {pop} × 10⁶ × {mass} = {big(pop * 1e6 * mass)} kg [1]; × {fx((100 - frac) / 100, 2)} ÷ 1000 [1] = {big(tn)} t [1] [5]', 'numerical', 5)


@t.add('C3', (2, 3, 4), 'numerical')
def ghg_q(r, D):
    m0 = round(r.uniform(1.6, 1.75), 2)
    m1 = round(m0 * r.uniform(1.05, 1.16), 2)
    yrs = r.choice([20, 30, 35])
    st = f'The concentration of methane in the atmosphere rose from {m0} ppm to {m1} ppm over {yrs} years. (a) Calculate the percentage increase. (b) State two human activities that release methane. (c) Explain why an increase in methane contributes to climate change.'
    return Q(st, f'(a) {fx(pct(m0, m1), 1)}% (b) cattle farming; rice paddies; landfill sites; extraction of natural gas (c) methane is a greenhouse gas that absorbs infrared radiation, enhancing the greenhouse effect.',
             f'(a) ({m1} − {m0}) ÷ {m0} × 100 [1] = {fx(pct(m0, m1), 1)}% [1] (b) two sources [1] (c) absorbs heat / enhanced greenhouse effect [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def eutro_case(r, D):
    intro = f'After heavy rain on farmland near a lake in {city(r)}, the water turned green. Two weeks later the water became clear and brown, and many dead fish were seen.'
    parts = [lambda r: ('Explain why the water turned green.', 'Fertiliser (nitrate / phosphate) washed into the lake; algae grew rapidly (algal bloom).', '[2]'),
             lambda r: ('Explain why the fish died two weeks later.', 'Algae blocked light so plants died; algae also died; decomposer bacteria fed on dead material and respired aerobically, using up oxygen; fish suffocated.', 'plants / algae die [1]; decomposers multiply [1]; respiration uses oxygen [1]; fish lack oxygen [1] [4]'),
             lambda r: ('Suggest two ways farmers could reduce this problem.', 'Use less fertiliser or organic fertiliser; avoid spreading before heavy rain; leave buffer strips of vegetation near water.', '[2]'),
             lambda r: ('Suggest how the dissolved oxygen concentration would change over 24 hours during the algal bloom, and explain.', 'Higher during the day (photosynthesis), lower at night (only respiration).', '[2]'),
             lambda r: ('Name the process by which fertiliser enters the lake.', 'Leaching (run-off).', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the process of eutrophication and explain how it can be caused by fertilisers and sewage.', 'Fertiliser / sewage nutrients (nitrate, phosphate) enter water; algal bloom; light blocked, plants die; decomposers multiply and respire aerobically; oxygen falls; fish and animals die. Sewage also supplies organic matter directly to bacteria.',
           'source of nutrients [1]; algal growth [1]; plants die [1]; decomposers [1]; oxygen used in respiration [1]; animals die [1] [6]'),
          ('Explain how human activities increase the concentration of greenhouse gases and describe the consequences.', 'CO₂ from combustion of fossil fuels and deforestation; methane from cattle, rice, landfill. Absorb infrared and enhance the greenhouse effect; global warming; climate change: sea-level rise, extreme weather, habitat change, extinction.',
           'CO₂ sources [2]; methane sources [1]; mechanism [1]; two consequences [2] [6]')])
t19c = t

t = T('Conservation: sustainable resources, endangered species and seed banks', 'conservation', 'sustainable resources', 'endangered species', 'seed banks')
facts(t, [('sustainable resource', 'a resource that is produced as rapidly as it is removed from the environment so that it does not run out'), ('endangered species', 'a species at risk of becoming extinct'),
          ('seed bank', 'a store of seeds kept in cold, dry conditions to conserve plant species and their genetic variation'), ('captive breeding programme', 'breeding endangered animals in zoos so that they can later be released into the wild'),
          ('fishing quota', 'a limit on the mass or number of fish that may be caught in an area'), ('conservation', 'the protection of species, habitats and resources from damage or loss')])
mcqs(t, [('Why are seeds in seed banks kept cold and dry?', 'To slow respiration and enzyme activity so they stay viable for many years', 'Low temperature and water content keep seeds dormant.', ['To make them germinate quickly', 'To kill fungi only', 'To make them heavier']),
         ('Which is a method of making fishing sustainable?', 'Using nets with larger mesh so young fish escape', 'Young fish survive to breed.', ['Catching all fish in breeding grounds', 'Using smaller mesh nets', 'Removing all quotas']),
         ('Why is it important to maintain genetic variation in a small endangered population?', 'So that some individuals may survive new diseases or environmental change', 'Low variation increases risk of extinction.', ['So that all individuals are identical', 'To prevent reproduction', 'To increase inbreeding'])])
shorts(t, [('State three reasons why species become endangered.', 'Habitat destruction; hunting / poaching; pollution; introduced species; climate change.', 'any three [3]'), ('State two methods of conserving forests sustainably.', 'Replanting trees; selective felling; education; legal protection.', 'any two [2]'),
           ('State two reasons for conservation programmes.', 'Maintain biodiversity; reduce extinction; protect vulnerable ecosystems; maintain ecosystem functions; source of future medicines and foods.', 'any two [2]')])
explain(t, [('Explain how captive breeding programmes can help conserve endangered species.', 'Animals are bred in zoos, increasing numbers; individuals are chosen to maintain genetic variation; they can be released into protected habitats.', '[3]'),
            ('Explain why fish stocks can collapse if fishing is not controlled.', 'Fish are caught faster than they can reproduce; too few adults are left to breed, so the population cannot recover.', '[2]'),
            ('Explain why artificial insemination and IVF are used in conservation.', 'They allow breeding between individuals in different places, increasing genetic variation without transporting animals.', '[2]'),
            ('Explain the importance of seed banks.', 'They store seeds of many species and varieties, conserving genetic variation for future breeding or reintroduction if species become extinct in the wild.', '[2]')])
myths(t, [('A species with a large population can never become endangered.', 'Large populations can decline rapidly through habitat loss, hunting or disease.'), ('Keeping animals in zoos is conservation only if they stay in zoos forever.', 'Captive breeding aims to increase numbers and reintroduce animals to the wild.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def endangered(r, D):
    sp, place = r.choice([('tigers', 'India'), ('mountain gorillas', 'Rwanda and Uganda'), ('giant pandas', 'China'), ('black rhinos', 'Kenya'), ('orangutans', 'Borneo'), ('snow leopards', 'Nepal')])
    y = [r.choice([1990, 2000, 2005]), 0, 0]
    y[1], y[2] = y[0] + r.choice([8, 10]), y[0] + r.choice([18, 20, 23])
    n0 = r.choice([1800, 2400, 3600, 5000])
    n1 = round(n0 * r.uniform(0.45, 0.7))
    n2 = round(n1 * r.uniform(1.15, 1.6))
    if D == 1:
        return NQ(r, f'The number of {sp} in {place} fell from {n0} in {y[0]} to {n1} in {y[1]}. What was the percentage decrease?', (n0 - n1) / n0 * 100, [(n0 - n1) / n1 * 100, n1 / n0 * 100, (n0 - n1) / 100], '%', f'({n0} − {n1}) ÷ {n0} × 100 = {fx((n0 - n1) / n0 * 100, 1)}%.', f=lambda v: fx(v, 1))
    st = f'The population of {sp} in {place} was {n0} in {y[0]}, {n1} in {y[1]} and {n2} in {y[2]}, after a conservation programme began in {y[1]}. (a) Calculate the percentage decrease between {y[0]} and {y[1]}. (b) Calculate the percentage increase between {y[1]} and {y[2]}. (c) Suggest two causes of the decline. (d) Suggest two measures that may have caused the increase.'
    return Q(st, f'(a) {fx((n0 - n1) / n0 * 100, 1)}% (b) {fx(pct(n1, n2), 1)}% (c) habitat loss, poaching, conflict with farmers (d) protected reserves, anti-poaching patrols, captive breeding, education, legal protection.',
             f'(a) ({n0} − {n1}) ÷ {n0} × 100 = {fx((n0 - n1) / n0 * 100, 1)}% [1] (b) ({n2} − {n1}) ÷ {n1} × 100 = {fx(pct(n1, n2), 1)}% [1] (c) two causes [2] (d) two measures [2] [6]', 'numerical', 6)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def fish_quota(r, D):
    sp = r.choice(['cod', 'tuna', 'herring', 'anchovy', 'hake'])
    stock = [r.randint(800, 1200)]
    for _ in range(4):
        stock.append(round(stock[-1] * r.uniform(0.72, 0.9)))
    yrs = [2000 + 5 * i for i in range(5)]
    q = r.choice([10, 15, 20, 25])
    st = f'The breeding stock of {sp} in a fishing area (thousand tonnes): ' + ', '.join(f'{a}: {b}' for a, b in zip(yrs, stock)) + f'. (a) Calculate the percentage decrease from {yrs[0]} to {yrs[-1]}. (b) A quota allows {q}% of the {yrs[-1]} stock to be caught. Calculate the mass that may be caught. (c) Describe two other methods of making fishing sustainable.'
    return Q(st, f'(a) {fx((stock[0] - stock[-1]) / stock[0] * 100, 1)}% (b) {fx(stock[-1] * q / 100, 1)} thousand tonnes (c) larger mesh nets; closed seasons in breeding periods; protected areas; restocking from fish farms; education.',
             f'(a) ({stock[0]} − {stock[-1]}) ÷ {stock[0]} × 100 [1] = {fx((stock[0] - stock[-1]) / stock[0] * 100, 1)}% [1] (b) {stock[-1]} × {q / 100} = {fx(stock[-1] * q / 100, 1)} [1] (c) two methods [2] [5]', 'numerical', 5)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def seedbank(r, D):
    sp = r.choice(['wheat', 'barley', 'sorghum', 'a wild orchid', 'a rare lily', 'rice', 'millet'])
    n = r.choice([50, 80, 100, 120, 200])
    g = round(n * r.uniform(0.6, 0.95))
    yrs = r.choice([10, 20, 30, 40])
    if D == 1:
        return NQ(r, f'{n} seeds of {sp} stored in a seed bank for {yrs} years were tested and {g} germinated. What percentage germinated?', g / n * 100, [(n - g) / n * 100, g / n, n / g * 100], '%', f'{g} ÷ {n} × 100 = {fx(g / n * 100, 1)}%.', f=lambda v: fx(v, 1))
    return Q(f'A seed bank tested {n} seeds of {sp} after {yrs} years of storage at −20 °C; {g} germinated. (a) Calculate the percentage germination. (b) Explain why storage at low temperature and low humidity keeps seeds viable. (c) Explain why seed banks store seeds from many varieties of the same crop.',
             f'(a) {fx(g / n * 100, 1)}% (b) low temperature and little water slow enzyme activity and respiration, so food stores last and seeds do not germinate or decay. (c) To conserve genetic variation (alleles) that may be needed for future breeding, e.g. for disease or drought resistance.',
             f'(a) {g} ÷ {n} × 100 = {fx(g / n * 100, 1)}% [1] (b) slow respiration / enzymes [1]; no germination / fungal decay [1] (c) genetic variation for future breeding [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def conserve_case(r, D):
    sp = r.choice(['the Sumatran rhino', 'the Amur leopard', 'the vaquita porpoise', 'the kakapo parrot', 'the Philippine eagle'])
    n = r.choice([30, 50, 80, 100])
    intro = f'Fewer than {n} individuals of {sp} remain in the wild. A conservation group in {city(r)} is planning how to save the species.'
    parts = [lambda r: ('Suggest two reasons why the species became endangered.', 'Habitat destruction; hunting / poaching; pollution; introduced species; climate change.', '[2]'),
             lambda r: ('Explain why a very small population is at risk of extinction even if it is protected.', 'Low genetic variation (inbreeding), so a disease or environmental change could kill all of them; few mates.', '[2]'),
             lambda r: ('Describe how a captive breeding programme could help.', 'Breed in captivity to increase numbers; choose mates to maximise genetic variation (use studbooks, artificial insemination, IVF); release into protected habitat.', '[3]'),
             lambda r: ('Suggest two other conservation measures.', 'Protect and restore habitat; anti-poaching laws and patrols; education; monitoring; reducing pollution.', '[2]'),
             lambda r: ('Give two reasons why conservation of species is important.', 'Maintain biodiversity and food webs; possible medicines; ecosystem services; ethical / cultural reasons.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how resources such as forests and fish stocks can be managed sustainably, and describe the role of seed banks and captive breeding in conservation.', 'Forests: replanting, selective felling, education, laws. Fish: quotas, net mesh size, closed seasons, protected areas, restocking. Seed banks preserve genetic variation of plants; captive breeding, AI and IVF increase numbers and variation of endangered animals for release.',
           'forests [2]; fish [2]; seed banks [1]; captive breeding [1] [6]')])
t19d = t
CHAPTERS[9] = [t19a, t19b, t19c, t19d]

# ===================================================================== 10 Biotechnology and genetic modification
t = T('Bacteria in biotechnology; yeast in biofuels and bread making', 'bacteria in biotechnology', 'yeast in biofuels and bread making')
facts(t, [('biotechnology', 'the use of living organisms, usually microorganisms, to make useful products'), ('biofuel', 'a fuel, such as ethanol, made from biological material such as plants'),
          ('plasmid', 'a small circle of DNA found in bacteria, separate from the main chromosome'), ('fermentation', 'the anaerobic respiration of microorganisms such as yeast, used to make products such as ethanol'),
          ('proving', 'leaving bread dough in a warm place so yeast can respire and produce carbon dioxide, making the dough rise')])
mcqs(t, [('Why are bacteria useful in biotechnology and genetic modification?', 'They reproduce rapidly and can make complex molecules', 'Bacteria have no ethical concerns over their use and contain plasmids.', ['They reproduce slowly', 'They have a nucleus with many chromosomes', 'They cannot be grown in fermenters']),
         ('Which product of yeast respiration makes bread rise?', 'Carbon dioxide', 'CO₂ bubbles are trapped in the dough.', ['Ethanol', 'Oxygen', 'Water']),
         ('Which is the balanced equation for the production of ethanol by yeast?', 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'Anaerobic respiration in yeast.', ['C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 'C₆H₁₂O₆ → 2C₃H₆O₃', '2C₂H₅OH + 2CO₂ → C₆H₁₂O₆']),
         ('What happens to the ethanol produced by yeast in bread dough?', 'It evaporates during baking', 'High oven temperature drives off ethanol.', ['It makes the bread rise', 'It is digested by the yeast', 'It is converted to starch'])])
shorts(t, [('State two reasons why bacteria are useful in biotechnology.', 'Rapid reproduction; ability to make complex molecules; few ethical concerns; plasmids; genetic code shared with other organisms.', 'any two [2]'), ('Name the substances used as the raw material for making biofuel ethanol.', 'Sugar from crops such as sugar cane or maize (starch broken down to sugar).', '[1]')])
explain(t, [('Explain why bread dough rises when left in a warm place.', 'Yeast respires anaerobically, producing carbon dioxide; bubbles of gas are trapped in the dough, so it expands; warmth increases enzyme activity.', 'CO₂ from yeast respiration [1]; bubbles trapped [1]; warmth increases rate [1] [3]'),
            ('Explain why biofuels are described as more sustainable than fossil fuels.', 'The crops can be regrown each year, and the CO₂ released when they burn was taken in by photosynthesis while they grew.', '[2]'),
            ('Explain one disadvantage of growing crops for biofuels.', 'Land is used for fuel instead of food, raising food prices; forests may be cleared, reducing biodiversity.', '[2]'),
            ('Explain why yeast is grown in sugar solution without oxygen to produce ethanol.', 'Without oxygen yeast respires anaerobically, producing ethanol; with oxygen it would respire aerobically producing CO₂ and water.', '[2]')])
myths(t, [('Bread rises because yeast produces oxygen.', 'Yeast produces carbon dioxide, which makes the dough rise.'), ('Bread contains a lot of alcohol because yeast makes ethanol.', 'The ethanol evaporates during baking.')])

DOUGH = {'setup': lambda r, p: f'{p} put equal masses of bread dough containing yeast into measuring cylinders, kept them in water baths at different temperatures and measured the increase in volume after 30 minutes.',
         'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[15, 25, 35, 45, 55], [20, 30, 40, 50, 60], [10, 20, 30, 40, 50]]), 'dv': ('increase in volume', 'cm³'),
         'y': lambda x, k: max(1, k * 48 * math.exp(-((x - 37) ** 2) / 170)), 'dp': 0, 'noise': 0.05,
         'controls': ['mass of dough', 'mass of yeast and sugar in the dough', 'time', 'diameter of measuring cylinder', 'type of flour'],
         'why': ('Yeast respires anaerobically producing carbon dioxide, which is trapped in the dough; up to about 35–40 °C enzymes work faster, giving more CO₂; above this the enzymes are denatured and the yeast dies.', 'CO₂ from respiration [1]; faster enzyme activity to optimum [1]; denaturation above optimum [1] [3]'),
         'improve': ['press the dough to the bottom of the cylinder so the starting level is flat', 'use a thermometer to check the temperature inside the dough'],
         'control': 'Dough made with boiled (dead) yeast — any change in volume would not be due to yeast respiration.',
         'extra': [lambda r, d: ('Calculate the mean rate of increase in volume at the optimum temperature, in cm³ per minute.', f'{fx(max(d["means"]) / 30, 2)} cm³/min', f'{fx(max(d["means"]), 1)} ÷ 30 [1] = {fx(max(d["means"]) / 30, 2)} cm³/min [1] [2]')]}
add_practical(t, DOUGH, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ethanol_calc(r, D):
    m = r.choice([90, 180, 360, 450, 900, 1800])
    e = m / 180 * 2 * 46
    c = m / 180 * 2 * 44
    if D == 1:
        return NQ(r, f'Using C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂, how many molecules of ethanol are made from 5 molecules of glucose?', 10, [5, 2, 20, 12], '', '1 glucose → 2 ethanol, so 5 → 10.', f=lambda v: fx(v))
    yld = r.choice([80, 85, 90])
    st = f'A biofuel plant in {city(r)} ferments sugar from sugar cane: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂ (Mr glucose 180, ethanol 46, CO₂ 44). (a) Calculate the maximum mass of ethanol made from {m} kg of glucose. (b) Calculate the mass of carbon dioxide released. (c) In practice only {yld}% of this ethanol is obtained. Calculate the actual mass. (d) Suggest why the yield is less than 100%.'
    return Q(st, f'(a) {fx(e, 1)} kg (b) {fx(c, 1)} kg (c) {fx(e * yld / 100, 1)} kg (d) some glucose is used by yeast for growth / aerobic respiration; ethanol kills yeast at high concentration.',
             f'(a) {m} ÷ 180 × 2 × 46 [1] = {fx(e, 1)} kg [1] (b) {fx(c, 1)} kg [1] (c) {fx(e * yld / 100, 1)} kg [1] (d) glucose used for growth / yeast killed [1] [5]', 'numerical', 5)


@t.add('C4', (3, 4, 5), 'multi_step')
def biofuel_case(r, D):
    crop = r.choice(['sugar cane', 'maize', 'cassava', 'sugar beet'])
    intro = f'In {r.choice(["Brazil", "Indonesia", "Kenya", "India", "Thailand"])}, {crop} is grown and fermented by yeast to make ethanol, which is mixed with petrol for cars.'
    parts = [lambda r: ('Write the word equation for the production of ethanol by yeast.', 'glucose → ethanol + carbon dioxide', '[2]'),
             lambda r: ('Explain why the fermenter is kept free of oxygen.', 'So yeast respires anaerobically and produces ethanol, not carbon dioxide and water.', '[2]'),
             lambda r: (f'If starch from {crop} is used, explain why an enzyme is added before fermentation.', 'Amylase breaks down starch to sugars (maltose / glucose) that yeast can respire.', '[2]'),
             lambda r: ('Discuss one advantage and one disadvantage of using ethanol from crops as fuel.', 'Advantage: renewable / reduces fossil fuel use / CO₂ from burning was absorbed by photosynthesis. Disadvantage: uses land for fuel not food / deforestation / energy to process.', '[2]'),
             lambda r: ('Explain why fermentation stops when the ethanol concentration reaches about 15%.', 'Ethanol is toxic to yeast; high concentrations kill the yeast cells.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain why bacteria and yeast are useful in biotechnology, and describe how yeast is used to make bread and biofuel.', 'Bacteria: rapid reproduction, make complex molecules, plasmids, few ethical issues. Bread: yeast respires anaerobically in dough, CO₂ makes it rise, ethanol evaporates in baking. Biofuel: crops provide sugar, yeast ferments to ethanol anaerobically, distilled.',
           'bacteria features [2]; bread [2]; biofuel [2] [6]')])
t20a = t

t = T('Pectinase, biological washing powders and lactase production', 'pectinase', 'biological washing powders', 'lactase production')
facts(t, [('pectinase', 'an enzyme that breaks down pectin in plant cell walls, used to increase the yield and clarity of fruit juice'), ('biological washing powder', 'a detergent containing enzymes such as proteases and lipases that digest stains'),
          ('lactase', 'an enzyme that breaks down lactose into glucose and galactose'), ('lactose-free milk', 'milk treated with lactase so that the lactose has been broken down'),
          ('protease', 'an enzyme that breaks down protein into amino acids'), ('lipase', 'an enzyme that breaks down fats and oils into fatty acids and glycerol')])
mcqs(t, [('Why does pectinase increase the volume of juice extracted from apples?', 'It breaks down pectin, so cell walls break down and release juice', 'Pectin holds cells together; breaking it releases juice.', ['It adds water to the fruit', 'It breaks down sugar', 'It makes cells larger']),
         ('Why are biological washing powders effective at low temperatures?', 'Their enzymes work at relatively low temperatures, saving energy', 'Enzymes digest stains without hot water.', ['Enzymes work best at 90 °C', 'They contain no enzymes', 'Low temperatures denature the enzymes']),
         ('Lactase breaks lactose into', 'glucose and galactose', 'Lactose is a disaccharide of glucose and galactose.', ['two glucose molecules', 'amino acids', 'fatty acids and glycerol']),
         ('Which enzyme in a biological washing powder removes a grass or egg stain?', 'Protease', 'These stains contain protein.', ['Lipase', 'Amylase', 'Pectinase'])])
shorts(t, [('State why people with lactose intolerance can drink lactose-free milk.', 'The lactose has already been broken down by lactase, so it does not cause digestive symptoms.', '[1]'), ('State two advantages of using pectinase in juice production.', 'Greater volume of juice; clearer juice.', '[2]')])
explain(t, [('Explain why biological washing powders should not be used in very hot water.', 'High temperatures denature the enzymes, changing the shape of the active site so stains are not digested.', 'denatured [1]; active site shape changed [1] [2]'),
            ('Explain how enzymes in biological washing powders remove stains.', 'Proteases and lipases digest insoluble proteins and fats into small, soluble molecules that wash away in water.', '[2]'),
            ('Explain why the lactase used to make lactose-free milk is often immobilised on beads.', 'It can be reused, does not contaminate the milk, and the milk can flow over it continuously.', '[2]'),
            ('Explain why fruit juice treated with pectinase is clearer.', 'Pectin and cell wall debris that make juice cloudy are broken down into soluble substances.', '[2]')])
myths(t, [('Biological washing powders work best in boiling water.', 'Enzymes are denatured at high temperatures; they work best at moderate temperatures (e.g. 30–40 °C).'), ('Lactase breaks lactose down into amino acids.', 'Lactase breaks lactose into glucose and galactose.')])

PECT = {'setup': lambda r, p: f'{p} added pectinase to 50 g samples of chopped apple at different temperatures, left them for 15 minutes, then filtered each for 10 minutes and measured the volume of juice collected.',
        'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 20, 30, 40, 50, 60], [15, 25, 35, 45, 55], [20, 30, 40, 50, 60, 70]]), 'dv': ('volume of juice', 'cm³'),
        'y': lambda x, k: 6 + k * 20 * math.exp(-((x - 45) ** 2) / 220), 'dp': 1,
        'controls': ['mass of apple', 'volume and concentration of pectinase', 'time left before filtering', 'filtering time', 'size of apple pieces'],
        'why': ('Pectinase breaks down pectin in cell walls, releasing juice; up to about 45 °C more kinetic energy gives more enzyme–substrate collisions; above the optimum the enzyme is denatured and the active site changes shape.', 'pectin broken down [1]; more collisions to optimum [1]; denaturation [1] [3]'),
        'improve': ['bring the apple and enzyme to the test temperature before mixing', 'use a water bath with a thermostat'],
        'control': 'Apple with boiled (denatured) pectinase, or water instead of enzyme, at each temperature — shows how much juice is released without active enzyme.',
        'extra': [lambda r, d: ('Calculate the percentage increase in juice volume from the lowest temperature to the optimum.', f'{fx(pct(d["means"][0], max(d["means"])), 0)}%', f'({fx(max(d["means"]), 2)} − {fx(d["means"][0], 2)}) ÷ {fx(d["means"][0], 2)} × 100 [1] = {fx(pct(d["means"][0], max(d["means"])), 0)}% [1] [2]')]}
add_practical(t, PECT, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))

WASH = {'setup': lambda r, p: f'{p} placed squares of cloth stained with egg in biological washing powder solution at different temperatures and recorded the time taken for each stain to disappear.',
        'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[20, 30, 40, 50, 60], [10, 25, 40, 55, 70], [15, 30, 45, 60]]), 'dv': ('time for stain to disappear', 'min'),
        'y': lambda x, k: k * (8 + 0.025 * (x - 40) ** 2 + (30 if x >= 60 else 0)), 'dp': 0, 'noise': 0.06,
        'controls': ['size and age of stain', 'concentration and volume of washing powder solution', 'type of cloth', 'amount of stirring'],
        'why': ('Protease digests the egg protein into soluble amino acids; it works fastest near its optimum (about 40 °C); at low temperatures there are fewer collisions and at high temperatures the enzyme is denatured, so the time is longer.', 'protease digests protein [1]; optimum [1]; low collisions / denaturation [1] [3]'),
        'improve': ['use a colorimeter to judge when the stain has gone', 'stir each sample at the same rate'],
        'control': 'Use non-biological washing powder (or boiled biological powder) at each temperature — shows the effect of the enzymes.',
        'extra': [lambda r, d: ('Calculate the rate of stain removal at the optimum temperature (1 / time).', f'{fx(1 / min(d["means"]), 3)} per minute', f'1 ÷ {fx(min(d["means"]), 1)} [1] = {fx(1 / min(d["means"]), 3)} min⁻¹ [1] [2]')]}
add_practical(t, WASH, C3D=(3, 4, 5), C4D=(4, 5))


@t.add('C3', (1, 2, 3, 4), 'numerical')
def lactase_q(r, D):
    vol = r.choice([500, 1000, 2000])
    lac = round(r.uniform(4.4, 5.0), 1)
    conv = r.choice([70, 80, 90, 95])
    if D == 1:
        return MQ(r, 'Which test would show that lactase has acted on lactose in milk?', 'A glucose test strip changes colour', ['Biuret solution turns purple', 'Iodine solution turns blue-black', 'Ethanol emulsion test turns cloudy'], 'Lactose → glucose + galactose; glucose test strips detect glucose (lactose gives a weaker or no result).')
    m = vol / 100 * lac
    st = f'A dairy in {city(r)} makes lactose-free milk. Milk contains {lac} g lactose per 100 cm³. {vol} cm³ of milk is passed over immobilised lactase and {conv}% of the lactose is broken down. (a) Calculate the mass of lactose in {vol} cm³ of milk. (b) Calculate the mass of lactose remaining after treatment. (c) Name the products and describe a test to show that they are present.'
    return Q(st, f'(a) {fx(m, 1)} g (b) {fx(m * (100 - conv) / 100, 2)} g (c) glucose and galactose; glucose test strip / Benedict\'s test gives a colour change (more reducing sugar).',
             f'(a) {vol} ÷ 100 × {lac} = {fx(m, 1)} g [1] (b) {fx(m, 1)} × {fx((100 - conv) / 100, 2)} = {fx(m * (100 - conv) / 100, 2)} g [1] (c) glucose and galactose [1]; test [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def enzyme_case(r, D):
    intro = f'A food company in {city(r)} uses three enzymes: pectinase for apple juice, lactase for milk, and proteases and lipases in its own laundry for staff uniforms.'
    parts = [lambda r: ('Explain why pectinase increases the yield of apple juice.', 'Pectin in cell walls is broken down, so cells break apart and release more juice.', '[2]'),
             lambda r: ('Explain why lactose-free milk is useful for some people.', 'People with lactose intolerance lack lactase, so lactose in milk causes digestive problems; in treated milk it has already been broken down.', '[2]'),
             lambda r: ('Explain why the laundry uses biological washing powder at 40 °C rather than 90 °C.', 'Enzymes work well at 40 °C (near optimum), saving energy; at 90 °C they would be denatured.', '[2]'),
             lambda r: ('Name the substances produced when lipase digests a grease stain.', 'Fatty acids and glycerol.', '[1]'),
             lambda r: ('Suggest why enzymes used in industry are often obtained from microorganisms.', 'Microorganisms grow rapidly in fermenters, producing large quantities of enzyme cheaply.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the uses of pectinase, lactase and enzymes in biological washing powders, and explain how temperature affects their use.', 'Pectinase: breaks pectin, more and clearer juice. Lactase: lactose → glucose + galactose, lactose-free milk. Washing powders: proteases and lipases digest stains to soluble products. Optimum temperature: faster near optimum, denatured above, slow at low temperature.',
           'pectinase [1]; lactase [1]; washing powder [2]; temperature effects [2] [6]')])
t20b = t

t = T('Large-scale production in fermenters (penicillin, insulin)', 'large-scale production in fermenters', 'penicillin, insulin')
FERMP = [('temperature probe and water jacket', 'keeps the temperature at the optimum for enzymes; respiration releases heat, so cooling water removes it'), ('pH probe', 'keeps pH at the optimum for enzymes'),
         ('sterile air inlet', 'supplies oxygen for aerobic respiration'), ('stirring paddles', 'keep microorganisms, nutrients and oxygen evenly mixed and spread heat'),
         ('nutrient inlet', 'supplies glucose / nutrients for respiration and growth'), ('steam sterilisation', 'kills other microorganisms that would compete or contaminate the product'), ('waste gas outlet', 'removes carbon dioxide produced by respiration')]
facts(t, [('fermenter', 'a large vessel in which microorganisms are grown in controlled conditions to make a product'), ('penicillin', 'an antibiotic produced by the fungus Penicillium'),
          ('aseptic conditions', 'conditions free from unwanted microorganisms'), ('batch culture', 'a method in which microorganisms are grown in a closed fermenter and the product is collected at the end'),
          ('downstream processing', 'the separation and purification of the product from a fermenter')])
mcqs(t, [('Why is cooling water passed through the jacket of a fermenter?', 'Respiration of the microorganisms releases heat, which could denature enzymes', 'Temperature must be kept at the optimum.', ['To provide oxygen', 'To sterilise the contents', 'To dissolve nutrients']),
         ('Why is the fermenter sterilised with steam before use?', 'To kill unwanted microorganisms that would contaminate the product', 'Aseptic conditions prevent contamination.', ['To provide heat for growth', 'To add water', 'To make the enzymes active']),
         ('Why is sterile air bubbled into a Penicillium fermenter?', 'To provide oxygen for aerobic respiration', 'Penicillium respires aerobically.', ['To remove glucose', 'To cool the fermenter only', 'To lower the pH'])])
shorts(t, [('State four conditions that are controlled in a fermenter.', 'Temperature; pH; oxygen; nutrient supply; waste products; sterility.', 'any four [2]; two or three [1] [2]'), ('Name the organism that produces penicillin.', 'Penicillium (a fungus).', '[1]')])
explain(t, [('Explain why the pH in a fermenter must be monitored and controlled.', 'Enzymes in the microorganisms work best at an optimum pH; changes in pH (e.g. from CO₂ / waste) could denature enzymes and reduce growth and yield.', '[2]'),
            ('Explain why penicillin is collected after the fungus has stopped growing rapidly.', 'Penicillium makes most penicillin when nutrients start to run out, after the main growth phase.', '[2]'),
            ('Explain why stirring is necessary in a fermenter.', 'Keeps nutrients, oxygen and microorganisms evenly mixed and spreads heat evenly.', '[2]'),
            ('Explain why insulin from GM bacteria grown in fermenters is better than insulin from animal pancreases.', 'Large quantities produced quickly and cheaply; identical to human insulin so fewer allergic reactions; no ethical or religious objections.', '[3]')])
myths(t, [('A fermenter is heated all the time because microorganisms need warmth.', 'Respiration releases heat, so a fermenter usually needs cooling to keep the optimum temperature.'), ('Oxygen is added to all fermenters.', 'Oxygen is added only for aerobic microorganisms; anaerobic fermentations (e.g. ethanol) exclude it.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ferm_part(r, D):
    n, w = r.choice(FERMP)
    if D <= 2:
        i = FERMP.index((n, w))
        return MQ(r, f'What is the function of the {n} on a fermenter?', cap(w), [cap(FERMP[(i + j) % len(FERMP)][1]) for j in (1, 2, 3)], f'{cap(n)}: {w}.')
    o = r.sample([x for x in FERMP if x[0] != n], 2)
    return Q(f'Explain the purpose of each of these features of an industrial fermenter: (i) {n}; (ii) {o[0][0]}; (iii) {o[1][0]}.', f'(i) {w} (ii) {o[0][1]} (iii) {o[1][1]}', '(i) [1] (ii) [1] (iii) [1] [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ferm_yield(r, D):
    hrs = [0, 20, 40, 60, 80, 100, 120]
    K = r.choice([20, 24, 30])
    bm = [round(K / (1 + 30 * math.exp(-0.09 * h)), 1) for h in hrs]
    pen = [0, 0, round(r.uniform(0.1, 0.3), 1)]
    for _ in range(4):
        pen.append(round(pen[-1] + r.uniform(1.5, 3.0), 1))
    st = 'Biomass of Penicillium (g/dm³) and penicillin concentration (units) in a fermenter at times 0, 20, 40, 60, 80, 100, 120 hours: biomass ' + ', '.join(fx(b, 1) for b in bm) + '; penicillin ' + ', '.join(fx(p, 1) for p in pen) + '. (a) Calculate the mean rate of penicillin production between 60 and 120 hours. (b) Describe the relationship between growth and penicillin production. (c) Suggest why the manufacturer stops the batch at about 120 hours.'
    rate = (pen[-1] - pen[3]) / 60
    return Q(st, f'(a) {fx(rate, 3)} units per hour (b) penicillin is made mainly after rapid growth slows, when the fungus approaches the stationary phase. (c) Nutrients run out / production slows, so it is more economical to harvest and start again.',
             f'(a) ({fx(pen[-1], 1)} − {fx(pen[3], 1)}) ÷ 60 [1] = {fx(rate, 3)} [1] (b) made after main growth [1] (c) nutrients used up / yield levels off [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def ferm_case(r, D):
    prod = r.choice([('penicillin', 'the fungus Penicillium'), ('human insulin', 'genetically modified bacteria')])
    T_ = r.choice([24, 26, 30, 37])
    intro = f'A pharmaceutical company in {city(r)} makes {prod[0]} using {prod[1]} in a 100 000 dm³ fermenter kept at {T_} °C and pH 6.5. Sterile air is bubbled through the culture, and cooling water flows through a jacket.'
    parts = [lambda r: ('Explain why the fermenter needs a cooling jacket.', 'Respiration of the microorganisms releases heat; without cooling, the temperature would rise above the optimum and enzymes would be denatured.', '[2]'),
             lambda r: ('Explain why the air must be sterile.', 'Unwanted microorganisms would contaminate the culture, compete for nutrients or produce harmful substances.', '[2]'),
             lambda r: ('State the purpose of the stirring paddles.', 'Mix nutrients, oxygen and microorganisms evenly; distribute heat.', '[1]'),
             lambda r: (f'Suggest why the company keeps the culture at {T_} °C.', 'This is the optimum temperature for the enzymes of the microorganism, giving the fastest growth / highest yield.', '[1]'),
             lambda r: (f'Describe how the {prod[0]} is obtained after fermentation.', 'The culture is filtered to remove cells, then the product is extracted and purified (downstream processing).', '[2]'),
             lambda r: ('Explain why a probe is used to monitor the pH.', 'Waste products such as CO₂ change the pH; acid or alkali is added to keep the optimum pH for enzymes.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the conditions in an industrial fermenter are controlled for the large-scale production of penicillin, and explain why each is controlled.', 'Temperature (probe and water jacket) – optimum for enzymes, removes respiration heat; pH (probe, acid/alkali) – optimum; oxygen (sterile air) – aerobic respiration; nutrients – growth; stirring – mixing; aseptic (steam sterilisation) – prevent contamination; product extracted and purified.',
           'six conditions with reasons [6] [6]')])
t20c = t

GM = [('The human insulin gene is cut out of human DNA using restriction enzymes', 'cut'), ('A plasmid is cut open with the same restriction enzyme, leaving complementary sticky ends', 'open'),
      ('The insulin gene is inserted into the plasmid and joined with DNA ligase', 'ligase'), ('The recombinant plasmid is inserted into a bacterium', 'insert'),
      ('The bacteria multiply in a fermenter and express the gene, making human insulin', 'grow')]
t = T('Genetic modification: inserting human insulin gene into bacteria; GM crops and their pros and cons', 'genetic modification', 'inserting human insulin gene into bacteria', 'gm crops and their pros and cons')
facts(t, [('genetic modification', 'changing the genetic material of an organism by removing, changing or inserting individual genes'), ('restriction enzyme', 'an enzyme that cuts DNA at a specific base sequence, leaving sticky ends'),
          ('DNA ligase', 'an enzyme that joins pieces of DNA together'), ('sticky ends', 'short single-stranded lengths of DNA left after cutting with a restriction enzyme, which pair with complementary bases'),
          ('recombinant plasmid', 'a plasmid into which a gene from another organism has been inserted'), ('vector', 'something, such as a plasmid or virus, used to carry a gene into another organism')])
mcqs(t, [('Which enzyme joins the human insulin gene into a plasmid?', 'DNA ligase', 'Ligase joins sugar–phosphate backbones.', ['Restriction enzyme', 'Amylase', 'Protease']),
         ('Why is the same restriction enzyme used to cut the human DNA and the plasmid?', 'It produces complementary sticky ends that can pair up', 'Matching sticky ends allow the gene to fit into the plasmid.', ['It makes the plasmid larger', 'It joins the DNA', 'It kills the bacteria']),
         ('Which is an example of genetic modification?', 'Inserting a gene for herbicide resistance into soya plants', 'A gene is transferred into the crop.', ['Crossing two high-yield wheat plants', 'Adding fertiliser to maize', 'Growing yeast in sugar solution']),
         ('Why can bacteria make human insulin from a human gene?', 'The genetic code is universal, so bacteria read the same codons', 'All organisms use the same code for amino acids.', ['Bacteria have a nucleus', 'Insulin is made of DNA', 'Bacteria already contain human chromosomes'])])
shorts(t, [('State two examples of genetic modification.', 'Human insulin gene into bacteria; herbicide resistance or insect resistance into crops; extra vitamin A (Golden Rice).', 'any two [2]'), ('Name the two enzymes used to make a recombinant plasmid.', 'Restriction enzyme and DNA ligase.', '[2]')])
explain(t, [('Explain two advantages of GM crops that are resistant to insect pests.', 'Higher yield because less damage; less insecticide sprayed, so less harm to other insects and lower cost.', '[2]'),
            ('Explain two concerns about growing herbicide-resistant GM crops.', 'Genes may spread to wild relatives by pollen, producing herbicide-resistant weeds; more herbicide may be used, reducing biodiversity; seeds are expensive.', '[2]'),
            ('Explain why Golden Rice was developed.', 'It was genetically modified to produce beta-carotene (vitamin A precursor) to reduce vitamin A deficiency in countries where rice is the staple food.', '[2]'),
            ('Explain why bacteria are used as hosts for genes for human proteins.', 'They reproduce rapidly; contain plasmids; few ethical concerns; can be grown in fermenters on a large scale.', '[2]')])
myths(t, [('Genetic modification is just a faster form of selective breeding.', 'GM inserts specific genes, even from other species; selective breeding only uses existing alleles within a species over many generations.'),
          ('Eating GM food will change your genes.', 'Genes in food are digested; they do not become part of the consumer\'s DNA.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def gm_steps(r, D):
    if D <= 2:
        i = r.randrange(5)
        enz = {'cut': 'Restriction enzyme', 'open': 'Restriction enzyme', 'ligase': 'DNA ligase', 'insert': 'No enzyme: the plasmid is taken up by the bacterium', 'grow': 'Enzymes for protein synthesis inside the bacterium'}
        if GM[i][1] in ('cut', 'open', 'ligase'):
            return MQ(r, f'Which enzyme is used in this step of making human insulin by genetic modification: "{GM[i][0].split(" using")[0].split(" and joined")[0]}"?', enz[GM[i][1]], [e for e in ['Restriction enzyme', 'DNA ligase', 'Amylase', 'Lactase', 'Protease'] if e != enz[GM[i][1]]], f'{GM[i][0]}.')
        return MQ(r, 'What is the first step in producing human insulin from bacteria?', 'Cut the insulin gene out of human DNA with a restriction enzyme', ['Grow the bacteria in a fermenter', 'Insert the plasmid into the bacterium', 'Join the gene to the plasmid with ligase'], 'The gene must be isolated first.')
    lab = list('PQRST')
    order = list(range(5))
    r.shuffle(order)
    st = 'These steps in making human insulin using bacteria are in the wrong order: ' + '; '.join(f'{lab[k]} {GM[j][0].lower()}' for k, j in enumerate(order)) + '. (a) Put the letters in the correct order. (b) Explain why bacteria can make a human protein.'
    corr = ''.join(lab[order.index(j)] for j in range(5))
    return Q(st, f'(a) {" → ".join(corr)} (b) the genetic code is universal, so the bacterium translates the human gene into the same sequence of amino acids.', f'(a) {" ".join(corr)}: all correct [2]; three in correct positions [1] (b) universal genetic code [1] [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def gm_crop_data(r, D):
    crop, trait = r.choice([('cotton', 'insect resistance (Bt toxin)'), ('maize', 'insect resistance (Bt toxin)'), ('soya', 'insect resistance (Bt toxin)'), ('brinjal (aubergine)', 'insect resistance (Bt toxin)')])
    y0 = round(r.uniform(1.5, 3.5), 2)
    y1 = round(y0 * r.uniform(1.1, 1.45), 2)
    p0 = round(r.uniform(4, 9), 1)
    p1 = round(p0 * r.uniform(0.3, 0.7), 1)
    st = f'Farmers in {city(r)} compared non-GM {crop} with GM {crop} that has {trait}. Yield: non-GM {y0} t/ha, GM {y1} t/ha. Insecticide sprayed: non-GM {p0} kg/ha, GM {p1} kg/ha. (a) Calculate the percentage increase in yield. (b) Calculate the percentage decrease in insecticide used. (c) Suggest one environmental benefit and one possible risk of growing the GM crop.'
    return Q(st, f'(a) {fx(pct(y0, y1), 1)}% (b) {fx((p0 - p1) / p0 * 100, 1)}% (c) benefit: fewer non-pest insects killed / less pollution; risk: genes spread to wild plants by pollen, pests evolve resistance, reduced biodiversity.',
             f'(a) ({y1} − {y0}) ÷ {y0} × 100 [1] = {fx(pct(y0, y1), 1)}% [1] (b) ({p0} − {p1}) ÷ {p0} × 100 = {fx((p0 - p1) / p0 * 100, 1)}% [1] (c) benefit [1]; risk [1] [5]', 'numerical', 5)


@t.add('C3', (2, 3, 4), 'numerical')
def insulin_calc(r, D):
    g = r.choice([20, 30, 40])
    h = r.choice([4, 5, 6, 8])
    n0 = r.choice([1000, 5000, 10000])
    k = h * 60 // g
    st = f'{big(n0)} genetically modified bacteria containing the human insulin gene are added to a fermenter. They divide every {g} minutes. (a) Calculate the number of generations in {h} hours. (b) Calculate the number of bacteria after {h} hours. (c) Explain why each new bacterium can also make insulin.'
    return Q(st, f'(a) {k} (b) {big(n0 * 2 ** k)} (c) the plasmid with the insulin gene is copied and passed to both daughter cells in binary fission.',
             f'(a) {h * 60} ÷ {g} = {k} [1] (b) {big(n0)} × 2^{k} = {big(n0 * 2 ** k)} [1] (c) plasmid copied / inherited [1] [3]', 'numerical', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def gm_case(r, D):
    crop = r.choice(['rice', 'maize', 'cotton', 'soya', 'cassava'])
    intro = f'Scientists in {city(r)} have produced a GM {crop} variety containing a bacterial gene that makes a toxin harmful to insect pests. Some local groups oppose growing it.'
    parts = [lambda r: ('Describe how the bacterial gene could be inserted into the crop plant cells.', 'Cut the gene out with restriction enzymes; insert it into a vector (plasmid of a bacterium that infects plants) with ligase; the vector transfers the gene into plant cells, which are grown into plants.', '[3]'),
             lambda r: ('Explain two advantages of growing this GM crop.', 'Higher yields because less pest damage; less insecticide needed, saving money and reducing harm to other insects / people.', '[2]'),
             lambda r: ('Explain two concerns that the local groups might have.', 'Gene could spread to wild plants by pollen; harm to non-pest insects (e.g. pollinators); pests evolve resistance; seed costs / dependence on companies; reduced biodiversity.', '[2]'),
             lambda r: ('Explain how pests could become resistant to the toxin.', 'A random mutation gives some pests resistance; they survive and reproduce, passing on the allele (natural selection).', '[2]'),
             lambda r: ('Compare genetic modification with selective breeding.', 'GM: specific gene, can cross species, fast; selective breeding: whole genome, same species, many generations.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how bacteria can be genetically modified to produce human insulin.', 'Insulin gene cut from human DNA with restriction enzyme (sticky ends); plasmid cut with same enzyme; gene inserted and joined with DNA ligase; recombinant plasmid taken up by bacteria; bacteria multiply in fermenter; insulin extracted and purified.',
           'restriction enzyme [1]; sticky ends / same enzyme on plasmid [1]; ligase [1]; plasmid into bacterium [1]; fermenter [1]; extraction [1] [6]'),
          ('Discuss the advantages and disadvantages of genetically modifying crops such as soya, maize and rice.', 'Advantages: insect resistance (less insecticide, higher yield), herbicide resistance (easier weed control), improved nutrition (Golden Rice), drought tolerance. Disadvantages: gene transfer to wild species, reduced biodiversity, resistance in pests, cost of seed, possible health concerns.',
           'three advantages [3]; three disadvantages [3] [6]')])
t20d = t
CHAPTERS[10] = [t20a, t20b, t20c, t20d]
