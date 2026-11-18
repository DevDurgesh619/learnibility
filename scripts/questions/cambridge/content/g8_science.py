"""Cambridge Lower Secondary Science 0893, Stage 9 (CUP Learner's Book 9, 2nd ed.) - grade 8 bank.

Chapters: 1 Photosynthesis and the carbon cycle, 2 Properties of materials, 3 Forces and energy,
4 Maintaining life, 5 Reactivity, 6 Sound and space, 7 Genes and inheritance, 8 Rates of reaction,
9 Electricity.

One Topic per W2 subtopic (name = subtopic name). Fixed C1/C2 lists carry recall and explanation
(auto-paired into two-part items); "spot the error" lists add C2 variety; parameterised data and
calculation templates scale with D; compose() builds Checkpoint-style structured questions with
"[n]" part marks. Helpers Q/FX/compose/numq/g come from g9_physics (not edited).
"""
import math
from ._lib import topic, mcq, person, city, relation, sci
from .g9_physics import Q, FX, compose, numq, g, cap, t12_reg, t12_irreg, t12_liquid, t12_float, t12_err, _dens_c4

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def F(s):
    """Formula with subscripts: digits after a letter or ')' become subscripts."""
    out = ''
    for i, ch in enumerate(s):
        if ch.isdigit() and i > 0 and (s[i - 1].isalpha() or s[i - 1] in ')₀₁₂₃₄₅₆₇₈₉' or (s[i - 1].isdigit() and out and out[-1] in '₀₁₂₃₄₅₆₇₈₉')):
            out += ch.translate(_SUB)
        else:
            out += ch
    return out


def mq(r, stem, correct, pool, key):
    opts, a = mcq(r, correct, [p for p in pool if p != correct])
    return Q(stem, a, key, opts=opts)


def misc(t, C, D, items):
    """Spot-the-error items: (claim, correction, key with [n])."""
    def fn(r, D_):
        claim, corr, key = r.choice(items)
        p = person(r)
        fr = r.choice([0, 1, 2])
        if fr == 0:
            stem = f'{p} says: "{claim}" Explain why {p} is wrong.'
        elif fr == 1:
            stem = f'In a test, {p} writes: "{claim}" Identify the error and give the correct science.'
        else:
            stem = f'{p} claims: "{claim}" Do you agree? Explain your answer.'
        ans = ('No. ' if fr == 2 else '') + corr
        return Q(stem, ans, key, 'explain')
    fn.__name__ = 'misc'
    t.add(C, D, 'explain')(fn)


def art(w):
    return 'an' if w[0].lower() in 'aeiou' or w.startswith('LED') else 'a'


def pct(a, b):
    return (b - a) / a * 100


# =========================================================== 1 Photosynthesis and the carbon cycle
N11 = 'Photosynthesis: word and symbol equations and the role of chlorophyll and light'
t11 = topic(N11, N11.lower(), 'photosynthesis')
FX(t11, 'C1', (1, 2), [
    ('Which is the word equation for photosynthesis?', 'carbon dioxide + water → glucose + oxygen', 'Reactants carbon dioxide and water; products glucose and oxygen; light energy absorbed by chlorophyll.',
     ['glucose + oxygen → carbon dioxide + water', 'carbon dioxide + oxygen → glucose + water', 'water + oxygen → glucose + carbon dioxide']),
    ('Which is the balanced symbol equation for photosynthesis?', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'Six CO₂ and six H₂O give one glucose and six O₂; atoms balance on both sides.',
     ['C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 3O₂', 'CO₂ + H₂O → C₆H₁₂O₆ + O₂']),
    ('What is the function of chlorophyll in photosynthesis?', 'It absorbs light energy', 'Chlorophyll is the green pigment in chloroplasts that absorbs light energy for photosynthesis.',
     ['It absorbs carbon dioxide from the air', 'It stores glucose as starch', 'It carries water up to the leaf']),
    ('In which part of a plant cell does photosynthesis take place?', 'Chloroplast', 'Chloroplasts contain chlorophyll and are where photosynthesis happens.', ['Nucleus', 'Cell wall', 'Vacuole']),
    ('Which gas is given off by a plant photosynthesising in bright light?', 'Oxygen', 'Oxygen is a product of photosynthesis and is released into the air or water.', ['Carbon dioxide', 'Nitrogen', 'Hydrogen']),
    ('Which reagent is used to test a leaf for starch?', 'Iodine solution', 'Iodine solution turns from orange-brown to blue-black when starch is present.', ['Limewater', 'Universal indicator', 'Ethanol']),
    ('What colour is iodine solution when starch is present?', 'Blue-black', 'Iodine changes from orange-brown to blue-black with starch.', ['Orange-brown', 'Milky white', 'Pale green']),
    ('In photosynthesis, light energy is transferred to', 'chemical energy stored in glucose', 'Light energy is absorbed and stored as chemical (potential) energy in glucose.', ['thermal energy stored in water', 'kinetic energy of oxygen', 'sound energy']),
    ('State the two reactants needed for photosynthesis.', 'Carbon dioxide and water.', 'carbon dioxide [1]; water [1] [2]'),
    ('Name the green pigment in leaves that absorbs light.', 'Chlorophyll.', 'chlorophyll [1]'),
    ('State the two products of photosynthesis.', 'Glucose and oxygen.', 'glucose [1]; oxygen [1] [2]'),
])
FX(t11, 'C2', (1, 2, 3), [
    ('Explain why a plant is kept in the dark for 48 hours before one of its leaves is tested for starch.', 'To destarch it: without light the plant cannot photosynthesise and uses up its stored starch, so any starch found later must have been made during the experiment.', 'stored starch used up / destarched [1]; so starch found later was made during the experiment [1] [2]'),
    ('A variegated leaf has green and white areas. After testing with iodine, only the green areas turn blue-black. Explain this result.', 'Only the green areas contain chlorophyll, so only they absorb light and photosynthesise, making glucose that is stored as starch.', 'green areas have chlorophyll [1]; photosynthesis / starch only where chlorophyll is present [1] [2]'),
    ('During a starch test the leaf is placed in hot ethanol. Explain why.', 'Ethanol dissolves the chlorophyll and removes the green colour, so the colour change of the iodine can be seen clearly.', 'removes chlorophyll [1]; so the iodine colour change is visible [1] [2]'),
    ('Explain why ethanol is heated in a water bath and not directly over a Bunsen flame.', 'Ethanol is very flammable; a water bath heats it without a naked flame close to the ethanol.', 'ethanol is flammable [1]; no naked flame in contact [1] [2]'),
    ('Explain why plants need light to make glucose.', 'Making glucose from carbon dioxide and water needs energy; light provides this energy, which is absorbed by chlorophyll.', 'light is the energy source [1]; absorbed by chlorophyll to build glucose [1] [2]'),
    ('Explain how the shape of a typical leaf helps photosynthesis.', 'It is broad, giving a large surface area to absorb light, and thin, so carbon dioxide only diffuses a short distance to the cells.', 'broad / large surface area for light [1]; thin / short diffusion distance for CO₂ [1] [2]'),
    ('Describe two ways in which a plant uses the glucose it makes.', 'In respiration to release energy; changed to starch for storage (or to cellulose for cell walls, or to proteins using nitrates).', 'any two uses [1] each [2]'),
    ('Explain why the number of chloroplasts is greatest in cells near the upper surface of a leaf.', 'These cells receive the most light, so having many chloroplasts there absorbs as much light as possible for photosynthesis.', 'most light near upper surface [1]; more chloroplasts absorb more light / more photosynthesis [1] [2]'),
])
misc(t11, 'C2', (2, 3, 4), [
    ('Plants get their food from the soil through their roots.', 'Plants make their own food (glucose) by photosynthesis in the leaves; roots take in water and mineral ions, not food.', 'food made by photosynthesis [1]; roots absorb water and minerals only [1] [2]'),
    ('Plants photosynthesise in the day and respire only at night.', 'Plants respire all the time, day and night; in the light photosynthesis is usually faster than respiration, so the respiration is hidden.', 'respiration continuous [1]; photosynthesis faster than respiration in light [1] [2]'),
    ('Chlorophyll makes the oxygen in photosynthesis.', 'Chlorophyll only absorbs light energy; the oxygen comes from the reactants (water) during the reaction.', 'chlorophyll absorbs light [1]; oxygen is a product formed from the reactants [1] [2]'),
    ('The glucose made in photosynthesis contains energy that came from the soil.', 'The energy stored in glucose comes from light absorbed by chlorophyll, not from the soil.', 'energy comes from light [1]; transferred to chemical energy in glucose [1] [2]'),
])
PLANTS = ['pondweed (Elodea)', 'Cabomba pondweed', 'Canadian pondweed']


@t11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_bubbles(r, D):
    plant = r.choice(PLANTS)
    base = r.choice([30, 36, 42, 48, 54, 60, 66])
    dists = r.choice([(10, 20, 30, 40, 50), (5, 15, 25, 35, 45), (15, 25, 35, 45, 55), (10, 25, 40, 55, 70)])
    T = r.choice([2, 3, 4, 5])
    counts = [round(base * f) + r.choice([-1, 0, 1]) for f in (1, .65, .42, .28, .19)]
    p = person(r)

    def setup(cs):
        tab = '; '.join(f'{d} cm → {c}' for d, c in zip(dists, cs))
        return f'{p} puts {plant} in a boiling tube of water and counts the oxygen bubbles given off in {T} minutes with a lamp at different distances (distance → number of bubbles): {tab}.'
    if D <= 1:
        return mq(r, setup(counts) + ' What do the results show?', 'The rate of photosynthesis decreases as the lamp is moved further away',
                  ['The rate of photosynthesis increases as the lamp is moved further away', 'The distance of the lamp has no effect on photosynthesis', 'The plant stops photosynthesising as soon as the lamp is moved'],
                  'Fewer bubbles at greater distance: lower light intensity, so slower photosynthesis.')
    i = r.randrange(5)
    rate = counts[i] / T
    if D == 2:
        return Q(setup(counts) + f' Calculate the rate of bubble production, in bubbles per minute, with the lamp at {dists[i]} cm.', f'{g(rate)} bubbles per minute',
                 f'rate = {counts[i]} ÷ {T} [1]; = {g(rate)} bubbles per minute [1] [2]')
    j = 4 if i != 4 else 0
    if D == 3:
        return Q(setup(counts) + f' (a) Describe the pattern in the results. (b) Calculate the rate, in bubbles per minute, at {dists[i]} cm and at {dists[j]} cm.',
                 f'(a) The further away the lamp, the fewer bubbles are given off. (b) {g(rate)} and {g(counts[j] / T)} bubbles per minute.',
                 f'(a) further away → fewer bubbles [1] (b) {counts[i]} ÷ {T} = {g(rate)} [1]; {counts[j]} ÷ {T} = {g(counts[j] / T)} bubbles per minute [1] [3]', 'multi_step')
    k = r.choice([1, 2, 3])
    cs = counts[:]
    cs[k] = counts[k - 1] + r.choice([3, 5, 7])
    s = setup(cs) + f' (a) Identify the anomalous result. (b) Suggest one possible cause of this anomalous result. (c) Explain the overall pattern in terms of light energy.'
    a = f'(a) {cs[k]} bubbles at {dists[k]} cm (more than at {dists[k - 1]} cm). (b) Miscounting, bubbles of different sizes, or the plant not given time to adjust to the new light level. (c) Further away, less light reaches the leaves, so less light energy is absorbed by chlorophyll and photosynthesis (oxygen production) is slower.'
    key = f'(a) {cs[k]} at {dists[k]} cm [1] (b) any sensible cause [1] (c) less light / lower light intensity [1]; less energy absorbed, slower photosynthesis [1]'
    if D == 4:
        return Q(s, a, key + ' [4]', 'multi_step')
    return Q(s + ' (d) The lamp also heats the water. Suggest how to stop this affecting the results.', a + ' (d) Use an LED lamp or put a beaker of water (heat shield) between the lamp and the tube; check the temperature with a thermometer.',
             key + ' (d) heat shield / LED / water bath [1] [5]', 'multi_step')


def _ps_c4(r, D):
    p = person(r)
    plant = r.choice(PLANTS)
    d1, d2 = sorted(r.sample([10, 15, 20, 25, 30, 40, 50], 2))
    n1 = r.choice([40, 44, 48, 52, 56, 60, 64])
    n2 = max(4, round(n1 * (d1 / d2) ** 1.5))
    T = r.choice([2, 3, 4, 5])
    fr = r.randrange(3)
    intro = [f'{p} investigates how light intensity affects photosynthesis in {plant}. With a lamp {d1} cm away, {n1} bubbles are counted in {T} minutes; with the lamp {d2} cm away, {n2} bubbles are counted in {T} minutes.',
             f'In a school laboratory in {city(r)}, a class adds sodium hydrogencarbonate to the water around some {plant} and counts bubbles for {T} minutes: {n1} bubbles with a lamp at {d1} cm and {n2} bubbles with the lamp at {d2} cm.',
             f'A greenhouse grower in {city(r)} tests whether extra lighting is worthwhile. In a model experiment with {plant}, {n1} bubbles are released in {T} minutes with a lamp at {d1} cm, but only {n2} bubbles with the lamp at {d2} cm.'][fr]
    parts = [
        lambda r: ('Name the gas in the bubbles.', 'Oxygen.', 'oxygen [1]'),
        lambda r: ('State the independent variable and the dependent variable.', 'Independent: distance of the lamp (light intensity). Dependent: number of bubbles (rate of photosynthesis).', 'independent: lamp distance / light intensity [1]; dependent: number of bubbles [1] [2]'),
        lambda r: (f'Calculate the rate of bubbling at {d1} cm and at {d2} cm, in bubbles per minute.', f'{g(n1 / T)} and {g(n2 / T)} bubbles per minute', f'{n1} ÷ {T} = {g(n1 / T)} [1]; {n2} ÷ {T} = {g(n2 / T)} [1] [2]'),
        lambda r: ('Explain why fewer bubbles are produced when the lamp is further away.', 'Lower light intensity reaches the plant, so less light energy is absorbed by chlorophyll; photosynthesis is slower and less oxygen is released.', 'lower light intensity [1]; less energy absorbed / slower photosynthesis [1]; less oxygen released [1] [3]'),
        lambda r: ('Name two variables that should be kept the same and explain why.', 'Temperature of the water and the same piece of plant (or amount of carbon dioxide); so that only light intensity affects the rate (fair test).', 'two control variables [1]; fair test reason [1] [2]'),
        lambda r: ('Suggest a more accurate way to measure the gas than counting bubbles, and explain why it is better.', 'Collect the gas in a gas syringe or an inverted measuring cylinder and measure its volume, because bubbles may be different sizes.', 'measure volume (syringe / cylinder) [1]; bubbles vary in size [1] [2]'),
        lambda r: ('Write the balanced symbol equation for photosynthesis.', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'correct formulae [1]; correctly balanced [1] [2]'),
    ]
    if fr == 1:
        parts.insert(4, lambda r: ('Suggest why sodium hydrogencarbonate is added to the water.', 'It releases carbon dioxide, so the plant does not run short of carbon dioxide for photosynthesis.', 'supplies carbon dioxide [1]; so CO₂ is not in short supply / does not limit the rate [1] [2]'))
    if fr == 2:
        parts.insert(4, lambda r: ('Use the results to advise the grower about placing lamps in the greenhouse.', 'Place lamps close to the plants (high light intensity) because photosynthesis, and so growth, is faster; but balance this against heating and electricity cost.', 'lamps close / high light intensity [1]; faster photosynthesis / growth [1]; cost or heating consideration [1] [3]'))
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t11.add('C4', (2, 3, 4, 5), 'multi_step')(_ps_c4)
t11.add('C3', (3, 4), 'multi_step')(_ps_c4)

N12 = 'The importance of water and minerals to plants: nitrate and magnesium ions'
t12 = topic(N12, N12.lower(), 'water and minerals', 'nitrate and magnesium')
FX(t12, 'C1', (1, 2), [
    ('Which mineral ion do plants need to make chlorophyll?', 'Magnesium ions', 'Magnesium is part of the chlorophyll molecule.', ['Nitrate ions', 'Chloride ions', 'Sodium ions']),
    ('Which mineral ion do plants need to make proteins for growth?', 'Nitrate ions', 'Nitrate supplies the nitrogen needed to make proteins (amino acids) for new cells.', ['Magnesium ions', 'Calcium ions', 'Chloride ions']),
    ('A plant grown without nitrate ions is most likely to show', 'stunted growth and yellow older leaves', 'Little protein is made, so growth is poor; older leaves turn yellow.', ['large, dark green leaves', 'very fast growth', 'thick, strong stems']),
    ('A plant short of magnesium ions develops yellow leaves because it cannot make enough', 'chlorophyll', 'Without magnesium, chlorophyll cannot be made, so leaves turn yellow (chlorosis).', ['cellulose', 'starch', 'water']),
    ('Through which cells do plants absorb most of their water and mineral ions?', 'Root hair cells', 'Root hair cells have a large surface area in contact with soil water.', ['Palisade cells', 'Guard cells', 'Leaf epidermis cells']),
    ('In what form do plants absorb mineral ions from the soil?', 'Dissolved in soil water', 'Mineral ions are dissolved in the water around soil particles and enter the root hair cells.', ['As solid particles of rock', 'As gases in the soil air', 'As part of glucose from the leaves']),
    ('Water is a reactant in which plant process?', 'Photosynthesis', 'Water combines with carbon dioxide in photosynthesis to make glucose and oxygen.', ['Respiration', 'Excretion', 'Decomposition']),
    ('State two reasons why plants need water.', 'Any two: reactant for photosynthesis; keeps cells firm to support the plant; transports dissolved mineral ions; cools leaves by evaporation.', 'any two reasons [1] each [2]'),
    ('State what a plant uses nitrate ions for and what it uses magnesium ions for.', 'Nitrate: making proteins for growth. Magnesium: making chlorophyll.', 'nitrate → proteins [1]; magnesium → chlorophyll [1] [2]'),
])
FX(t12, 'C2', (1, 2, 3), [
    ('Explain why a plant growing in soil that lacks magnesium grows slowly.', 'It cannot make enough chlorophyll, so it absorbs less light, photosynthesises less and makes less glucose for growth.', 'less chlorophyll [1]; less photosynthesis / glucose [1]; less energy and materials for growth [1] [3]'),
    ('Explain why plants need nitrate ions even though they make their own glucose.', 'Glucose contains only carbon, hydrogen and oxygen; proteins also contain nitrogen, which the plant must absorb as nitrate ions.', 'glucose has no nitrogen [1]; nitrogen from nitrate needed to make proteins [1] [2]'),
    ('Farmers add fertilisers to their fields. Explain how this can increase crop yield.', 'Fertilisers supply mineral ions such as nitrate and magnesium that may be in short supply, so crops can make more protein and chlorophyll and grow larger.', 'fertiliser supplies mineral ions [1]; more protein / chlorophyll so more growth [1] [2]'),
    ('Explain why a plant wilts when it is short of water.', 'Its cells lose water and are no longer firm, so they cannot hold up the leaves and stem.', 'cells lose water / no longer firm [1]; support lost so plant droops [1] [2]'),
    ('Explain how root hair cells are adapted to absorb water and mineral ions.', 'Each has a long, thin extension giving a large surface area in contact with soil water, and a thin wall so substances pass in easily.', 'large surface area [1]; thin wall / close contact with soil water [1] [2]'),
    ('Suggest why growing the same crop in the same field every year can lead to yellow, stunted plants.', 'Each crop removes the same mineral ions (such as nitrate and magnesium), so the soil becomes short of them unless fertiliser is added.', 'same minerals removed every year [1]; soil becomes deficient [1] [2]'),
])
misc(t12, 'C2', (2, 3, 4), [
    ('Fertiliser is plant food.', 'Fertiliser supplies mineral ions; plants make their own food (glucose) by photosynthesis.', 'fertiliser = mineral ions [1]; food made by photosynthesis [1] [2]'),
    ('A plant with yellow leaves just needs more water.', 'Yellow leaves often show a shortage of mineral ions such as magnesium (no chlorophyll) or nitrate, not water.', 'yellowing linked to mineral deficiency [1]; magnesium for chlorophyll / nitrate [1] [2]'),
    ('Plants need magnesium ions to make proteins.', 'Magnesium is needed to make chlorophyll; nitrate ions are needed to make proteins.', 'magnesium → chlorophyll [1]; nitrate → proteins [1] [2]'),
])


@t12.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_growth(r, D):
    m0 = r.choice([2.0, 2.4, 2.5, 3.0, 3.2, 4.0])
    fac = {'complete mineral solution': r.choice([2.5, 2.8, 3.0, 3.4]), 'solution lacking nitrate': r.choice([1.2, 1.25, 1.3, 1.4]), 'solution lacking magnesium': r.choice([1.5, 1.6, 1.75, 1.8])}
    ends = {k: round(m0 * v, 1) for k, v in fac.items()}
    days = r.choice([14, 21, 28, 30])
    p = person(r)
    tab = '; '.join(f'{k}: {g(m0)} g → {g(v)} g' for k, v in ends.items())
    setup = f'{p} grows three groups of identical seedlings in different solutions for {days} days. Mean mass of a seedling (start → end): {tab}.'
    if D <= 1:
        return mq(r, setup + ' Which solution gave the least growth?', 'solution lacking nitrate', list(ends) + ['all three gave the same growth'], 'Least increase in mass without nitrate: proteins for new cells cannot be made.')
    k = r.choice(list(ends))
    inc = pct(m0, ends[k])
    if D == 2:
        return Q(setup + f' Calculate the percentage increase in mass for the seedlings in the {k}.', f'{g(inc)}%', f'increase = {g(ends[k])} − {g(m0)} = {g(ends[k] - m0)} g [1]; ÷ {g(m0)} × 100 = {g(inc)}% [1] [2]')
    ln = pct(m0, ends['solution lacking nitrate'])
    if D == 3:
        return Q(setup + ' (a) Calculate the percentage increase in mass for the seedlings lacking nitrate. (b) Explain why these seedlings grew least.',
                 f'(a) {g(ln)}% (b) Without nitrate the seedlings cannot make proteins, so they cannot make new cells and grow.',
                 f'(a) ({g(ends["solution lacking nitrate"])} − {g(m0)}) ÷ {g(m0)} × 100 [1] = {g(ln)}% [1] (b) nitrate needed for proteins / new cells [1] [3]', 'multi_step')
    lm = pct(m0, ends['solution lacking magnesium'])
    s = setup + ' (a) Calculate the percentage increase in mass for the seedlings lacking magnesium. (b) Describe and explain how the leaves of these seedlings would look. (c) Explain why the mean mass of several seedlings is used rather than one seedling.'
    a = f'(a) {g(lm)}% (b) Yellow leaves (between the veins), because magnesium is needed to make chlorophyll. (c) Seedlings vary naturally; a mean reduces the effect of one unusual seedling and makes the result more reliable.'
    key = f'(a) ({g(ends["solution lacking magnesium"])} − {g(m0)}) ÷ {g(m0)} × 100 [1] = {g(lm)}% [1] (b) yellow leaves [1]; no magnesium → no chlorophyll [1]'
    if D == 4:
        return Q(s.replace(' (c) Explain why the mean mass of several seedlings is used rather than one seedling.', ''), a.split(' (c)')[0], key + ' [4]', 'multi_step')
    return Q(s, a, key + ' (c) natural variation / reliability [1] [5]', 'multi_step')


def _min_c4(r, D):
    c = city(r)
    conc = r.choice([2, 2.5, 4, 5, 8, 10])
    V = r.choice([50, 80, 120, 150, 200, 250])
    intro = r.choice([f'A rooftop farm in {c} grows lettuces with their roots in a nutrient solution instead of soil (hydroponics). The instructions say to add {g(conc)} cm³ of concentrated nutrient to every litre of water.',
                      f'{person(r)} grows tomato plants in water tanks in a greenhouse in {c}. A concentrated mineral feed containing nitrate and magnesium ions is diluted at {g(conc)} cm³ per litre of water.',
                      f'A school in {c} sets up a hydroponic tank of herbs. The label on the mineral feed reads: "Dilute {g(conc)} cm³ in each litre of water."'])
    parts = [
        lambda r: (f'Calculate the volume of concentrated nutrient needed for a tank holding {V} litres of water.', f'{g(conc * V)} cm³', f'{g(conc)} × {V} [1] = {g(conc * V)} cm³ [1] [2]'),
        lambda r: ('Explain why the nutrient solution must contain nitrate ions.', 'Nitrate supplies nitrogen to make proteins needed for growth of new cells.', 'nitrate → proteins [1]; needed for growth [1] [2]'),
        lambda r: ('Describe what would happen to the leaves if magnesium ions were left out, and explain why.', 'Leaves would turn yellow because magnesium is needed to make chlorophyll; less photosynthesis so slower growth.', 'yellow leaves [1]; magnesium needed for chlorophyll [1]; less photosynthesis / growth [1] [3]'),
        lambda r: ('Suggest why air is bubbled through the solution around the roots.', 'Root cells need oxygen for respiration, to release energy for absorbing mineral ions.', 'oxygen for respiration [1]; energy for root cells / uptake [1] [2]'),
        lambda r: ('Give two reasons why the plants also need water from the solution.', 'Water is a reactant in photosynthesis; it keeps cells firm for support (and carries mineral ions).', 'any two reasons [1] each [2]'),
        lambda r: ('Suggest one advantage of growing crops this way in a crowded city.', 'Mineral supply can be controlled exactly so growth is fast; needs little land (can be stacked or on rooftops) and uses less water.', 'valid advantage [1] with reason [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12.add('C4', (2, 3, 4, 5), 'multi_step')(_min_c4)
t12.add('C3', (3, 4), 'multi_step')(_min_c4)

N13 = 'The carbon cycle: photosynthesis, respiration, combustion and decomposition'
t13 = topic(N13, N13.lower(), 'carbon cycle')
FX(t13, 'C1', (1, 2), [
    ('Which process removes carbon dioxide from the atmosphere?', 'Photosynthesis', 'Plants take in carbon dioxide for photosynthesis.', ['Respiration', 'Combustion', 'Decomposition']),
    ('Which organisms break down dead material and release carbon dioxide?', 'Decomposers such as bacteria and fungi', 'Decomposers feed on dead organisms and waste and respire, releasing CO₂.', ['Producers such as grass', 'Herbivores such as rabbits', 'Carnivores such as foxes']),
    ('How is carbon passed from plants to animals?', 'By animals eating the plants', 'Carbon compounds in plants are eaten and digested by animals.', ['By photosynthesis', 'By combustion', 'By diffusion through the soil']),
    ('Fossil fuels such as coal were formed from', 'the remains of organisms buried and compressed over millions of years', 'Dead organisms that did not decay were buried; heat and pressure formed coal, oil and gas.', ['volcanic rock that cooled quickly', 'carbon dioxide dissolved in rain', 'sand heated by the Sun']),
    ('Which process releases carbon dioxide when fossil fuels are burned?', 'Combustion', 'Burning a fuel in oxygen is combustion; carbon in the fuel becomes CO₂.', ['Photosynthesis', 'Decomposition', 'Evaporation']),
    ('In what form is carbon stored in the bodies of living things?', 'Carbon compounds such as carbohydrates, proteins and fats', 'Organisms are built of carbon compounds.', ['Pure carbon (graphite)', 'Carbon dioxide gas', 'Carbonate rock']),
    ('Which process happens in all living organisms and releases carbon dioxide?', 'Respiration', 'All living cells respire, releasing CO₂.', ['Photosynthesis', 'Combustion', 'Fossilisation']),
    ('Name two processes that release carbon dioxide into the atmosphere.', 'Any two of: respiration, combustion, decomposition.', 'any two [1] each [2]'),
])
FX(t13, 'C2', (1, 2, 3), [
    ('Explain how a carbon atom breathed out by a cow could end up in the cow’s muscles again.', 'Grass absorbs the CO₂ in photosynthesis and makes glucose and other carbon compounds; the cow eats the grass and digests it; the carbon compounds are used to build muscle.', 'photosynthesis by grass [1]; cow eats grass [1]; compounds used to build muscle [1] [3]'),
    ('Explain why decomposers are important in the carbon cycle.', 'They break down dead organisms and waste and respire, returning carbon to the air as CO₂ for plants to use again; otherwise carbon stays locked in dead material.', 'break down dead material and respire [1]; return CO₂ for photosynthesis [1] [2]'),
    ('Explain why cutting down and burning large areas of forest increases the carbon dioxide in the atmosphere.', 'Burning the wood releases CO₂ by combustion, and with fewer trees less CO₂ is removed by photosynthesis.', 'combustion releases CO₂ [1]; less photosynthesis removing CO₂ [1] [2]'),
    ('Explain why the carbon dioxide concentration of the air stayed roughly constant for thousands of years before industry developed.', 'Processes adding CO₂ (respiration, decomposition) were balanced by processes removing it (photosynthesis, dissolving in the oceans).', 'adding processes named [1]; balanced by removal / photosynthesis [1] [2]'),
    ('Explain why the carbon in coal was not part of the carbon cycle for millions of years.', 'The organisms were buried before they could decay (no decomposers / no oxygen), so their carbon was locked away until the coal is burned.', 'buried without decomposition [1]; carbon stored until combustion [1] [2]'),
    ('Explain why there is more carbon dioxide in the air of a forest at night than in the middle of the day.', 'At night there is no photosynthesis, but plants and animals still respire, so CO₂ builds up; in daylight photosynthesis removes it.', 'no photosynthesis at night [1]; respiration continues adding CO₂ [1] [2]'),
])
ARROWS = [('the atmosphere', 'green plants', 'photosynthesis'), ('green plants', 'the atmosphere', 'respiration'), ('animals', 'the atmosphere', 'respiration'),
          ('dead organisms and waste', 'the atmosphere', 'decomposition (respiration by decomposers)'), ('fossil fuels', 'the atmosphere', 'combustion'),
          ('green plants', 'animals', 'feeding (eating and digestion)'), ('dead organisms', 'fossil fuels', 'fossilisation (burial and compression over millions of years)'),
          ('wood from forests', 'the atmosphere', 'combustion')]
PROC = ['photosynthesis', 'respiration', 'combustion', 'decomposition', 'feeding', 'fossilisation']


@t13.add('C1', (1, 2, 3))
def t13_arrow(r, D):
    a, b, pr = r.choice(ARROWS)
    stem = r.choice([f'In a carbon cycle diagram, an arrow goes from {a} to {b}. Which process does this arrow show?', f'Which process moves carbon from {a} to {b}?'])
    if D <= 2:
        return mq(r, stem, pr.split(' (')[0], PROC, f'{cap(a)} → {b}: {pr}.')
    return Q(stem.replace('Which process', 'Name the process that') if 'Which process moves' in stem else stem.replace('Which process does this arrow show?', 'Name the process shown by this arrow.'), cap(pr) + '.', f'{pr} [1]', 'short')


@t13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_budget(r, D):
    P = r.choice([120, 150, 180, 200, 240])
    A = round(P * r.choice([0.4, 0.45, 0.5]))
    B = round(P * r.choice([0.35, 0.4, 0.45]))
    Cc = r.choice([20, 25, 30, 36, 40, 48])
    net = A + B + Cc - P
    reg = r.choice(['a forested region', 'a model island ecosystem', 'a grassland region', 'a tropical region'])
    s = (f'Scientists model the carbon flows in {reg} each year (thousand tonnes of carbon): photosynthesis removes {P}; respiration by plants and animals releases {A}; '
         f'decomposition releases {B}; combustion of fuels releases {Cc}.')
    word = 'increases' if net > 0 else 'decreases' if net < 0 else 'stays the same'
    if D <= 1:
        return mq(r, s + ' What is the total carbon released into the atmosphere each year?', f'{A + B + Cc} thousand tonnes', [f'{P} thousand tonnes', f'{A + B} thousand tonnes', f'{abs(net)} thousand tonnes', f'{P + A + B + Cc} thousand tonnes'],
                  f'{A} + {B} + {Cc} = {A + B + Cc}.')
    if D == 2:
        return Q(s + ' Calculate the net change in carbon in the atmosphere each year.', f'{"+" if net > 0 else ""}{net} thousand tonnes ({word})',
                 f'released = {A} + {B} + {Cc} = {A + B + Cc} [1]; net = {A + B + Cc} − {P} = {net} thousand tonnes [1] [2]')
    if D == 3:
        return Q(s + ' (a) Calculate the net change in atmospheric carbon each year. (b) State whether the carbon dioxide in the air increases or decreases, and name the process that is unbalancing the cycle.',
                 f'(a) {net} thousand tonnes (b) It {word}; combustion of fuels adds extra carbon.', f'(a) {A + B + Cc} − {P} [1] = {net} [1] (b) {word} with combustion identified [1] [3]', 'multi_step')
    cut = r.choice([10, 20, 25, 30])
    P2 = P * (100 - cut) / 100
    net2 = A + B + Cc - P2
    s2 = s + f' (a) Calculate the net change each year. (b) Deforestation then reduces photosynthesis by {cut}%. Calculate the new net change.'
    a = f'(a) {net} thousand tonnes (b) photosynthesis = {g(P2)}; net = {g(net2)} thousand tonnes'
    k = f'(a) {A + B + Cc} − {P} = {net} [1] (b) {P} × {100 - cut}/100 = {g(P2)} [1]; {A + B + Cc} − {g(P2)} = {g(net2)} [1]'
    if D == 4:
        return Q(s2 + ' (c) Explain why this change matters for the climate.', a + ' (c) More CO₂ stays in the atmosphere; CO₂ is a greenhouse gas, so global warming increases.', k + ' (c) more CO₂ / greenhouse effect [1] [4]', 'multi_step')
    return Q(s2 + ' (c) Explain why this change matters for the climate. (d) Suggest two actions that would bring the cycle back towards balance.',
             a + ' (c) More CO₂ stays in the atmosphere, increasing the greenhouse effect and global warming. (d) Replant forests; burn less fossil fuel (use renewable energy).', k + ' (c) greenhouse effect [1] (d) two valid actions [1] [5]', 'multi_step')


TUBES = [('a piece of pondweed', 'in bright light', 'purple', 'photosynthesis is faster than respiration, so carbon dioxide is removed'),
         ('a piece of pondweed', 'wrapped in foil (dark)', 'yellow', 'no photosynthesis, but respiration adds carbon dioxide'),
         ('a small water snail', 'in bright light', 'yellow', 'the snail respires and cannot photosynthesise, so carbon dioxide increases'),
         ('a small water snail', 'wrapped in foil (dark)', 'yellow', 'the snail respires, adding carbon dioxide'),
         ('nothing (a control)', 'in bright light', 'red (no change)', 'no organism, so carbon dioxide stays the same')]


def _ind_c4(r, D):
    tubes = r.sample(TUBES, 3)
    p = person(r)
    desc = '; '.join(f'tube {L} contains {c} {w}' for L, (c, w, _, _) in zip('ABC', tubes))
    intro = (f'{p} uses hydrogencarbonate indicator, which is red at normal carbon dioxide levels, yellow when carbon dioxide increases and purple when carbon dioxide decreases. '
             f'Each sealed tube contains indicator: {desc}. The tubes are left for 4 hours.')
    parts = []
    for L, (c, w, col, why) in zip('ABC', tubes):
        parts.append(lambda r, L=L, col=col, why=why: (f'Predict the colour of the indicator in tube {L} and explain your prediction.', f'{cap(col)}: {why}.', f'{col} [1]; reason [1] [2]'))
    parts += [
        lambda r: ('Explain why one tube should contain no organism.', 'It is a control: it shows that any colour change is caused by the organisms and not by light or the indicator itself.', 'control [1]; shows change is due to organisms [1] [2]'),
        lambda r: ('Name the process that adds carbon dioxide in every tube containing an organism.', 'Respiration.', 'respiration [1]'),
        lambda r: ('Explain how this experiment models part of the carbon cycle.', 'Plants remove CO₂ from the surroundings by photosynthesis in light while all organisms return CO₂ by respiration, as happens in the atmosphere.', 'photosynthesis removes CO₂ [1]; respiration adds CO₂ [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t13.add('C4', (2, 3, 4, 5), 'multi_step')(_ind_c4)
t13.add('C3', (3, 4), 'multi_step')(_ind_c4)

N14 = 'Climate change: carbon dioxide, the greenhouse effect and human impact'
t14 = topic(N14, N14.lower(), 'climate change', 'greenhouse effect')
FX(t14, 'C1', (1, 2), [
    ('Which greenhouse gas is increased most by burning fossil fuels?', 'Carbon dioxide', 'Combustion of fossil fuels releases CO₂.', ['Oxygen', 'Nitrogen', 'Argon']),
    ('Which statement describes the greenhouse effect?', 'Gases in the atmosphere trap some of the thermal energy radiated by the Earth', 'Greenhouse gases absorb infrared radiated by the Earth and re-emit some back, keeping the Earth warmer.',
     ['Gases in the atmosphere let all thermal energy escape to space', 'The atmosphere blocks all sunlight from reaching the ground', 'Ozone gas reflects sunlight back into space']),
    ('Which is a likely effect of climate change?', 'Rising sea levels', 'Warming melts land ice and expands sea water, so sea levels rise.', ['Thicker ice at both poles', 'Fewer floods and droughts worldwide', 'A fall in average global temperature']),
    ('Which human activity increases the carbon dioxide in the atmosphere?', 'Clearing forests by burning', 'Burning adds CO₂ and fewer trees remove less by photosynthesis.', ['Planting new forests', 'Using solar panels', 'Using wind turbines']),
    ('Which source releases large amounts of the greenhouse gas methane?', 'Cattle farming and rice paddy fields', 'Cattle digestion and waterlogged rice fields release methane.', ['Solar farms', 'Wind turbines', 'Photosynthesis in forests']),
    ('Which type of radiation is emitted by the warm Earth’s surface and absorbed by greenhouse gases?', 'Infrared', 'The Earth radiates infrared; CO₂, methane and water vapour absorb it.', ['Ultraviolet', 'X-rays', 'Gamma rays']),
    ('State two effects of climate change on the environment.', 'Any two: rising sea levels; more extreme weather (floods, droughts, storms); melting ice; loss of habitats and species.', 'any two effects [1] each [2]'),
])
FX(t14, 'C2', (1, 2, 3), [
    ('Explain how greenhouse gases cause the Earth to be warmer than it would otherwise be.', 'Sunlight warms the surface; the surface radiates infrared; greenhouse gases absorb some infrared and re-emit some back towards the Earth, so less energy escapes to space.', 'surface emits infrared [1]; absorbed by greenhouse gases [1]; re-emitted back / less escapes [1] [3]'),
    ('Explain why melting of ice on land causes sea levels to rise.', 'Water from glaciers and ice sheets on land flows into the sea, adding to its volume (warmer sea water also expands).', 'water added to oceans from land [1]; expansion of warmer water [1] [2]'),
    ('Explain how planting large numbers of trees can help to slow climate change.', 'Trees remove carbon dioxide from the air by photosynthesis and store the carbon in wood, so less CO₂ remains to trap heat.', 'photosynthesis removes CO₂ [1]; carbon stored / less greenhouse effect [1] [2]'),
    ('Suggest why scientists use temperature data from many places over many years, rather than one hot summer, as evidence of climate change.', 'Weather varies from year to year and place to place; long-term averages from many places show the real trend and are more reliable.', 'weather varies [1]; long-term / many places shows trend [1] [2]'),
    ('Explain why burning biofuel made from crops grown each year adds less carbon dioxide overall than burning coal.', 'The CO₂ released was taken in by the crops in photosynthesis only recently, so it is largely balanced; coal releases carbon locked away for millions of years.', 'biofuel CO₂ recently absorbed [1]; coal adds stored carbon [1] [2]'),
    ('Explain why a rise in sea temperature can harm coral reefs.', 'Warmer water stresses coral, causing it to lose the algae that feed it (bleaching), so the coral may die and habitats are lost.', 'coral stressed / bleaching [1]; habitat / species loss [1] [2]'),
])
misc(t14, 'C2', (2, 3, 4), [
    ('The greenhouse effect is caused by the hole in the ozone layer.', 'The greenhouse effect is caused by gases such as CO₂ and methane absorbing infrared; the ozone hole lets in more ultraviolet and is a different problem.', 'greenhouse gases absorb infrared [1]; ozone hole is a separate issue (UV) [1] [2]'),
    ('The greenhouse effect is always harmful, so we should remove all the carbon dioxide from the air.', 'A natural greenhouse effect keeps the Earth warm enough for life; the problem is the extra greenhouse gas from human activity (and plants need CO₂).', 'natural greenhouse effect needed for life [1]; problem is enhanced effect [1] [2]'),
    ('One very cold winter proves that global warming is not happening.', 'Weather in one place and one year varies; climate change is about long-term average temperatures across the world, which are rising.', 'weather vs climate [1]; long-term global average rising [1] [2]'),
])
CO2 = {1960: 317, 1970: 326, 1980: 339, 1990: 354, 2000: 370, 2010: 390, 2020: 414}


@t14.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_co2(r, D):
    ys = sorted(CO2)
    y1, y2 = sorted(r.sample(ys, 2))
    c1, c2 = CO2[y1], CO2[y2]
    tab = ', '.join(f'{y}: {CO2[y]} ppm' for y in ys)
    s = f'The table shows the mean concentration of carbon dioxide in the air measured at an observatory: {tab}.'
    inc = c2 - c1
    rate = inc / (y2 - y1)
    if D <= 1:
        return mq(r, s + f' By how much did the concentration increase between {y1} and {y2}?', f'{inc} ppm', [f'{c2} ppm', f'{c1} ppm', f'{inc + 10} ppm', f'{max(1, inc - 10)} ppm', f'{c1 + c2} ppm'], f'{c2} − {c1} = {inc} ppm.')
    if D == 2:
        return Q(s + f' Calculate the mean increase per year between {y1} and {y2}.', f'{g(rate)} ppm per year', f'{c2} − {c1} = {inc} ppm [1]; ÷ {y2 - y1} years = {g(rate)} ppm per year [1] [2]')
    if D == 3:
        return Q(s + f' Calculate the percentage increase in carbon dioxide concentration from {y1} to {y2}, and suggest one reason for the increase.', f'{g(pct(c1, c2))}%; more burning of fossil fuels (or deforestation).',
                 f'({c2} − {c1}) ÷ {c1} [1] × 100 = {g(pct(c1, c2))}% [1]; fossil fuels / deforestation [1] [3]', 'multi_step')
    r1 = (354 - 317) / 30
    r2 = (414 - 354) / 30
    s4 = s + f' (a) Calculate the mean rate of increase from 1960 to 1990 and from 1990 to 2020. (b) Describe what these rates show.'
    a = f'(a) {g(r1)} ppm per year and {g(r2)} ppm per year (b) The concentration is rising and the rate of increase is getting faster.'
    k = f'(a) 37 ÷ 30 = {g(r1)} [1]; 60 ÷ 30 = {g(r2)} [1] (b) rising [1]; rate increasing / accelerating [1]'
    if D == 4:
        return Q(s4, a, k + ' [4]', 'multi_step')
    r3 = (414 - 390) / 10
    return Q(s4 + f' (c) Use the 2010–2020 rate to predict the concentration in 2030 and comment on how reliable this prediction is.',
             a + f' (c) 414 + 10 × {g(r3)} = {g(414 + 10 * r3)} ppm; only an estimate, because the rate has been increasing and depends on future human actions.',
             k + f' (c) {g(414 + 10 * r3)} ppm with comment on reliability [1] [5]', 'multi_step')


def _cc_c4(r, D):
    c = city(r)
    n = r.choice([200, 250, 400, 500, 800, 1200])
    e = r.choice([60, 75, 80, 90, 100])
    cut = r.choice([40, 50, 60, 70, 75])
    tot = n * e
    saved = tot * cut / 100
    intro = r.choice([f'The council in {c} runs {n} diesel buses, each releasing about {e} tonnes of carbon dioxide a year. It plans to replace them with electric buses, which would cut these emissions by {cut}%.',
                      f'A transport company in {c} has {n} buses that each emit about {e} tonnes of CO₂ per year. Switching to electric buses is expected to reduce the fleet’s emissions by {cut}%.'])
    parts = [
        lambda r: ('Calculate the total carbon dioxide released by the diesel buses each year.', f'{g(tot)} tonnes', f'{n} × {e} [1] = {g(tot)} tonnes [1] [2]'),
        lambda r: ('Calculate the mass of carbon dioxide saved each year by the switch.', f'{g(saved)} tonnes', f'{g(tot)} × {cut}/100 [1] = {g(saved)} tonnes [1] [2]'),
        lambda r: ('Explain how reducing carbon dioxide emissions helps to slow climate change.', 'Less CO₂ in the atmosphere means less infrared is absorbed and re-emitted to Earth, so the enhanced greenhouse effect and warming are reduced.', 'less greenhouse gas [1]; less infrared trapped / less warming [1] [2]'),
        lambda r: ('Evaluate whether electric buses always give large savings in carbon dioxide.', 'Only if the electricity comes from low-carbon sources such as solar, wind or hydro; if it comes from coal or gas power stations, CO₂ is released there instead. Making batteries also releases CO₂.', 'depends on source of electricity [1]; fossil-fuel power stations still emit CO₂ [1]; battery manufacture / balanced conclusion [1] [3]'),
        lambda r: ('Suggest two other actions the city could take to reduce its contribution to climate change.', 'Any two: plant trees; encourage cycling and walking; use solar or wind power; insulate buildings; reduce waste.', 'two valid actions [1] each [2]'),
        lambda r: ('Name one greenhouse gas other than carbon dioxide and give a source.', 'Methane, from cattle, rice fields or landfill (or water vapour / nitrous oxide).', 'gas [1]; source [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t14.add('C4', (2, 3, 4, 5), 'multi_step')(_cc_c4)
t14.add('C3', (3, 4), 'multi_step')(_cc_c4)
CHAPTERS[1] = [t11, t12, t13, t14]


# =========================================================== 2 Properties of materials
ELS = [('hydrogen', 'H', 1, 1), ('helium', 'He', 2, 4), ('lithium', 'Li', 3, 7), ('beryllium', 'Be', 4, 9), ('boron', 'B', 5, 11), ('carbon', 'C', 6, 12),
       ('nitrogen', 'N', 7, 14), ('oxygen', 'O', 8, 16), ('fluorine', 'F', 9, 19), ('neon', 'Ne', 10, 20), ('sodium', 'Na', 11, 23), ('magnesium', 'Mg', 12, 24),
       ('aluminium', 'Al', 13, 27), ('silicon', 'Si', 14, 28), ('phosphorus', 'P', 15, 31), ('sulfur', 'S', 16, 32), ('chlorine', 'Cl', 17, 35), ('argon', 'Ar', 18, 40),
       ('potassium', 'K', 19, 39), ('calcium', 'Ca', 20, 40)]
EL = {e[2]: e for e in ELS}


def shells(Z):
    out = []
    for cap_ in (2, 8, 8, 2):
        if Z <= 0:
            break
        out.append(min(Z, cap_))
        Z -= min(Z, cap_)
    return out


def arr(Z):
    return ','.join(map(str, shells(Z)))


def group_of(Z):
    o = shells(Z)[-1]
    if Z in (2, 10, 18):
        return 0
    return o


N21 = 'Atomic structure: protons, neutrons, electrons and the Rutherford model'
t21 = topic(N21, N21.lower(), 'atomic structure', 'rutherford model')
FX(t21, 'C1', (1, 2), [
    ('What is the relative charge of a proton?', '+1', 'Proton +1, neutron 0, electron −1.', ['0', '−1', '+2']),
    ('Which particle has a relative charge of 0?', 'Neutron', 'Neutrons are neutral.', ['Proton', 'Electron', 'Ion']),
    ('Where is most of the mass of an atom found?', 'In the nucleus', 'Protons and neutrons (mass 1 each) are in the nucleus; electrons have almost no mass.', ['In the electron shells', 'Spread evenly through the atom', 'In the empty space around the nucleus']),
    ('In Rutherford’s gold foil experiment, most alpha particles passed straight through the foil. What did this show?', 'Most of the atom is empty space', 'Particles passed through without hitting anything, so the atom is mostly empty space.',
     ['The atom is a solid ball of positive charge', 'Electrons are positively charged', 'The nucleus fills most of the atom']),
    ('In Rutherford’s experiment, a very few alpha particles bounced back. What did this show?', 'The atom has a tiny, dense, positively charged nucleus', 'Only a small, massive, positive centre could repel alpha particles straight back.',
     ['Electrons are spread evenly through the atom', 'Gold atoms have no charge', 'Alpha particles are negatively charged']),
    ('Which particles are found in the nucleus of an atom?', 'Protons and neutrons', 'The nucleus contains protons and neutrons; electrons are in shells around it.', ['Protons and electrons', 'Neutrons and electrons', 'Electrons only']),
    ('Which model of the atom did Rutherford’s results replace?', 'The plum pudding model', 'Thomson’s plum pudding model (electrons in a sphere of positive charge) could not explain the deflections.', ['The nuclear model', 'The electron shell model', 'The particle model of gases']),
    ('The atomic number of an element is the number of', 'protons in the nucleus of each atom', 'Atomic (proton) number = number of protons, which identifies the element.', ['neutrons in the nucleus', 'protons plus neutrons', 'electron shells']),
    ('State the relative masses of a proton, a neutron and an electron.', 'Proton 1, neutron 1, electron about 1/2000 (almost 0).', 'proton and neutron 1 [1]; electron very small / ≈ 1/1840 [1] [2]'),
    ('State what is meant by the mass number of an atom.', 'The total number of protons and neutrons in the nucleus.', 'protons + neutrons [1]'),
])
FX(t21, 'C2', (1, 2, 3), [
    ('Explain why an atom has no overall charge.', 'It has equal numbers of protons (+1 each) and electrons (−1 each), so the charges cancel.', 'equal numbers of protons and electrons [1]; charges cancel [1] [2]'),
    ('Explain why some alpha particles were deflected through large angles in Rutherford’s experiment.', 'Alpha particles are positive; those passing very close to the small positive nucleus were strongly repelled.', 'alpha particles and nucleus both positive [1]; repelled when passing close [1] [2]'),
    ('Describe the plum pudding model and explain how it differs from the nuclear model.', 'Plum pudding: a ball of positive charge with electrons scattered through it. Nuclear model: positive charge and most mass in a tiny central nucleus, electrons around it, mostly empty space.', 'plum pudding described [1]; nucleus small, dense, positive [1]; mostly empty space [1] [3]'),
    ('Explain how atoms of two different elements differ.', 'They have different numbers of protons (different atomic numbers), and so different numbers of electrons.', 'different number of protons [1]; so different atomic number / electrons [1] [2]'),
    ('Explain why scientists accepted Rutherford’s model in place of the plum pudding model.', 'It explained all the results, including the large deflections that the plum pudding model could not, and other scientists could repeat the experiment.', 'explains the deflections [1]; repeatable evidence [1] [2]'),
    ('Explain why the electrons in an atom do not fly away from the nucleus.', 'Electrons are negative and the nucleus is positive, so they are attracted to the nucleus.', 'opposite charges [1]; attraction [1] [2]'),
])
misc(t21, 'C2', (2, 3, 4), [
    ('Electrons are found in the nucleus with the protons.', 'Electrons are in shells around the nucleus; the nucleus contains protons and neutrons.', 'electrons in shells [1]; nucleus = protons and neutrons [1] [2]'),
    ('The mass number tells you the number of neutrons.', 'Mass number = protons + neutrons; neutrons = mass number − atomic number.', 'mass number definition [1]; neutrons = A − Z [1] [2]'),
    ('Atoms are solid all the way through.', 'Rutherford showed that atoms are mostly empty space, because most alpha particles passed straight through gold foil.', 'mostly empty space [1]; evidence from alpha particles passing through [1] [2]'),
])


@t21.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_count(r, D):
    nm, sy, Z, A = r.choice(ELS[2:])
    n = A - Z
    if D <= 1:
        return mq(r, f'An atom of {nm} has atomic number {Z} and mass number {A}. How many neutrons does it have?', str(n), [str(x) for x in (Z, A, A + Z, n + 1, n - 1)],
                  f'neutrons = mass number − atomic number = {A} − {Z} = {n}.')
    if D == 2:
        return Q(f'An atom of {nm} ({sy}) has atomic number {Z} and mass number {A}. State the numbers of protons, neutrons and electrons in the atom.', f'{Z} protons, {n} neutrons, {Z} electrons',
                 f'protons = electrons = {Z} [1]; neutrons = {A} − {Z} = {n} [1] [2]')
    if D == 3:
        return Q(f'An atom of {nm} has atomic number {Z} and mass number {A}. (a) Calculate the number of neutrons. (b) Give the number of electrons and their arrangement in shells.', f'(a) {n} (b) {Z} electrons arranged {arr(Z)}',
                 f'(a) {A} − {Z} = {n} [1] (b) {Z} electrons [1]; arrangement {arr(Z)} [1] [3]', 'multi_step')
    nm2, sy2, Z2, A2 = r.choice([e for e in ELS[2:] if e[2] != Z])
    gr, gr2 = group_of(Z), group_of(Z2)
    s = f'Atom X has atomic number {Z} and mass number {A}; atom Y has atomic number {Z2} and mass number {A2}.'
    s += ' (a) Calculate the number of neutrons in each atom. (b) Give the electron arrangement of each atom. (c) Deduce, with a reason, the group of the Periodic Table for each element.'
    a = f'(a) X {n}, Y {A2 - Z2} (b) X {arr(Z)}, Y {arr(Z2)} (c) X Group {gr if gr else "0 (8)"}, Y Group {gr2 if gr2 else "0 (8)"}, from the number of outer-shell electrons (full outer shell = Group 0).'
    k = f'(a) {A} − {Z} = {n} and {A2} − {Z2} = {A2 - Z2} [1] (b) {arr(Z)} and {arr(Z2)} [1] (c) groups from outer electrons [1]'
    if D == 4:
        return Q(s, a, k + '; both groups correct [1] [4]', 'multi_step')
    mets = [x for x, zz in ((nm, Z), (nm2, Z2)) if zz in (3, 4, 11, 12, 13, 19, 20)]
    mtxt = (' and '.join(mets) + (' are metals.' if len(mets) == 2 else ' is a metal.')) if mets else 'neither is a metal.'
    return Q(s + ' (d) Identify elements X and Y, and state which of them, if any, is a metal.', a + f' (d) X is {nm}, Y is {nm2}; {mtxt}',
             k + '; both groups correct [1] (d) both identified with metal stated [1] [5]', 'multi_step')


@t21.add('C3', (1, 2, 3, 4))
def t21_ident(r, D):
    nm, sy, Z, A = r.choice(ELS[1:])
    n = A - Z
    s = f'An atom has {Z} protons and {n} neutrons.'
    if D <= 1:
        return mq(r, s + ' Which element is it?', nm, [e[0] for e in ELS if abs(e[2] - Z) <= 3 and e[2] != Z] + [EL[n][0] if n in EL and n != Z else 'argon'], f'The element is identified by its number of protons: {Z} → {nm}.')
    if D == 2:
        return Q(s + ' Identify the element and state its mass number.', f'{cap(nm)}; mass number {A}', f'{nm} (from {Z} protons) [1]; mass number = {Z} + {n} = {A} [1] [2]')
    return Q(s + ' (a) Identify the element. (b) State its mass number. (c) Draw or describe the arrangement of electrons in the atom.', f'(a) {cap(nm)} (b) {A} (c) {Z} electrons: {arr(Z)}',
             f'(a) {nm} [1] (b) {A} [1] (c) {arr(Z)} [1] [3]', 'multi_step')


def _ruth_c4(r, D):
    N = r.choice([20000, 40000, 50000, 80000, 100000])
    back = r.choice([2, 3, 4, 5, 6, 8])
    small = r.choice([40, 60, 75, 120, 150, 200])
    thru = N - back - small
    intro = r.choice([f'In a repeat of Rutherford’s experiment, {N} alpha particles are fired at a thin gold foil. {thru} pass straight through, {small} are deflected through small angles and {back} bounce back.',
                      f'A computer simulation of the gold foil experiment fires {N} alpha particles at gold atoms: {thru} go straight through, {small} are slightly deflected and {back} are reflected back.'])
    parts = [
        lambda r: ('Calculate the percentage of alpha particles that passed straight through.', f'{g(thru / N * 100, 4)}%', f'{thru} ÷ {N} × 100 [1] = {g(thru / N * 100, 4)}% [1] [2]'),
        lambda r: ('Explain what the particles that passed straight through show about atoms.', 'Most of the atom is empty space.', 'mostly empty space [1]'),
        lambda r: ('Explain what the particles that bounced back show about the nucleus.', 'The nucleus is very small (few hits), dense/massive and positively charged (repels the positive alpha particles).', 'small [1]; positive / dense, repels alpha particles [1] [2]'),
        lambda r: ('Explain why the plum pudding model cannot explain these results.', 'In that model positive charge is spread out thinly, so it could not deflect alpha particles strongly or turn them back.', 'positive charge spread out [1]; could not cause large deflection / bounce back [1] [2]'),
        lambda r: ('Suggest why the experiment uses a very thin foil.', 'So that each alpha particle meets only a few layers of atoms and is not absorbed; deflections from single nuclei can be seen.', 'avoid absorption / few atoms in the way [1]; single deflections observed [1] [2]'),
        lambda r: ('State the charge on an alpha particle.', 'Positive (+2).', 'positive [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t21.add('C4', (2, 3, 4, 5), 'multi_step')(_ruth_c4)
t21.add('C3', (3, 4), 'multi_step')(_ruth_c4)

N22 = 'Trends in groups of the Periodic Table: Group 1, Group 7 and Group 8/0'
t22 = topic(N22, N22.lower(), 'trends in groups', 'periodic table')
FX(t22, 'C1', (1, 2), [
    ('What name is given to the elements in Group 1?', 'Alkali metals', 'Group 1 metals react with water to form alkaline solutions.', ['Halogens', 'Noble gases', 'Transition metals']),
    ('What name is given to the elements in Group 7?', 'Halogens', 'Group 7: fluorine, chlorine, bromine, iodine.', ['Alkali metals', 'Noble gases', 'Alkaline earth metals']),
    ('Why are the noble gases very unreactive?', 'Their atoms have full outer electron shells', 'A full outer shell is stable, so they do not need to gain, lose or share electrons.', ['They are all solids', 'They have no electrons', 'Their atoms have one outer electron']),
    ('How does the reactivity of Group 1 metals change down the group?', 'It increases', 'Li < Na < K < Rb < Cs in reactivity.', ['It decreases', 'It stays the same', 'It increases then decreases']),
    ('How does the reactivity of the halogens change down Group 7?', 'It decreases', 'F > Cl > Br > I in reactivity.', ['It increases', 'It stays the same', 'It decreases then increases']),
    ('How many electrons are in the outer shell of a Group 7 atom?', '7', 'Group number = number of outer-shell electrons for Groups 1 to 7.', ['1', '8', '2']),
    ('Which gas is produced when sodium reacts with water?', 'Hydrogen', 'sodium + water → sodium hydroxide + hydrogen.', ['Oxygen', 'Chlorine', 'Carbon dioxide']),
    ('Which halogen is a red-brown liquid at room temperature?', 'Bromine', 'Fluorine and chlorine are gases, bromine a liquid, iodine a solid.', ['Chlorine', 'Iodine', 'Fluorine']),
    ('State why elements in the same group have similar chemical reactions.', 'Their atoms have the same number of electrons in the outer shell.', 'same number of outer electrons [1]'),
])
FX(t22, 'C2', (1, 2, 3), [
    ('Explain why sodium and potassium are stored under oil.', 'They react quickly with oxygen and water vapour in the air; oil keeps air and water away.', 'react with air / water [1]; oil excludes air and water [1] [2]'),
    ('Explain why helium is used to fill party balloons and airships.', 'It is much less dense than air, so the balloon floats, and it is unreactive, so it will not burn (unlike hydrogen).', 'low density [1]; unreactive / non-flammable [1] [2]'),
    ('Explain why argon is used inside filament lamps.', 'Argon is unreactive, so the hot filament does not react with it (it would burn in oxygen).', 'unreactive [1]; filament does not react / burn [1] [2]'),
    ('Explain why potassium reacts more vigorously with water than lithium.', 'Potassium’s outer electron is further from the nucleus, so it is lost more easily; potassium is more reactive.', 'outer electron further from nucleus [1]; lost more easily [1] [2]'),
    ('Explain why the solution formed when lithium reacts with water turns universal indicator purple.', 'Lithium hydroxide is formed, which is an alkali, so the solution has a high pH.', 'lithium hydroxide formed [1]; alkaline / high pH [1] [2]'),
    ('Describe what you would see when a small piece of sodium is placed on water.', 'It floats, melts into a silvery ball, fizzes and moves around on the surface, getting smaller until it disappears.', 'floats / melts into ball [1]; fizzes / moves / disappears [1] [2]'),
])
misc(t22, 'C2', (2, 3, 4), [
    ('Reactivity increases down every group, so iodine is more reactive than chlorine.', 'In Group 7 reactivity decreases down the group, so chlorine is more reactive than iodine; the increase applies to Group 1.', 'Group 7 reactivity decreases down [1]; chlorine more reactive [1] [2]'),
    ('Noble gases do not react because they are gases.', 'Other gases (oxygen, chlorine) are reactive; noble gases are unreactive because their atoms have full outer shells.', 'other gases react [1]; full outer shell [1] [2]'),
    ('Group 1 metals are hard and dense like iron.', 'Group 1 metals are soft (can be cut with a knife) and have low densities; lithium, sodium and potassium float on water.', 'soft [1]; low density [1] [2]'),
])
G1 = [('lithium', 181), ('sodium', 98), ('potassium', 63), ('rubidium', 39), ('caesium', 28)]
G7 = [('fluorine', -220, -188), ('chlorine', -101, -34), ('bromine', -7, 59), ('iodine', 114, 184)]
G0 = [('helium', -269), ('neon', -246), ('argon', -186), ('krypton', -153), ('xenon', -108), ('radon', -62)]


def _deg(x):
    return f'−{abs(x)}' if x < 0 else str(x)


@t22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_trend(r, D):
    which = r.choice(['g1', 'g7', 'g0'])
    if which == 'g1':
        data, q, lab = [(a, b) for a, b in G1], 'melting point', 'Group 1 metals'
    elif which == 'g7':
        data, q, lab = [(a, c) for a, b, c in G7], 'boiling point', 'Group 7 elements'
    else:
        data, q, lab = G0, 'boiling point', 'noble gases'
    i = r.randrange(1, len(data) - 1)
    lo, hi = sorted([data[i - 1][1], data[i + 1][1]])
    tab = ', '.join(f'{n} {"?" if j == i else _deg(v) + " °C"}' for j, (n, v) in enumerate(data))
    s = f'The {q}s of some {lab} are: {tab}.'
    trend = 'decreases' if data[0][1] > data[-1][1] else 'increases'
    if D <= 1:
        bands = [(lo, hi), (hi + 1, hi + 60), (lo - 60, lo - 1), (lo - 200, lo - 120)]
        opts = [f'between {_deg(a)} °C and {_deg(b)} °C' for a, b in bands]
        return mq(r, s + f' Which is the best estimate for the {q} of {data[i][0]}?', opts[0], opts[1:], f'The {q} {trend} down the group, so {data[i][0]} lies between its neighbours (actual {_deg(data[i][1])} °C).')
    if D == 2:
        return Q(s + f' Describe the trend in {q} down the group and estimate the {q} of {data[i][0]}.', f'The {q} {trend} down the group; estimate between {_deg(lo)} and {_deg(hi)} °C (actual {_deg(data[i][1])} °C).',
                 f'{trend} down the group [1]; value between {_deg(lo)} and {_deg(hi)} °C [1] [2]')
    if which == 'g1':
        ext = (' Francium is below caesium. Predict how francium would react with water compared with caesium, and give a reason.', 'More vigorously (explosively), because reactivity increases down Group 1 (outer electron further from the nucleus).', 'more vigorous [1]; reactivity increases down group / reason [1]')
    elif which == 'g7':
        ext = (' Astatine is below iodine. Predict its state at room temperature and how its reactivity compares with iodine.', 'A solid (melting and boiling points increase down the group); less reactive than iodine.', 'solid [1]; less reactive [1]')
    else:
        ext = (' Explain why the noble gases are all used where an unreactive gas is needed.', 'Their atoms have full outer shells, so they do not form compounds easily.', 'full outer shells [1]; do not react [1]')
    if D == 3:
        return Q(s + f' (a) Estimate the missing value. (b) {ext[0].strip()}', f'(a) between {_deg(lo)} and {_deg(hi)} °C (actual {_deg(data[i][1])} °C) (b) {ext[1]}', f'(a) in range [1] (b) {ext[2]} [3]', 'multi_step')
    s2 = s + f' (a) Describe the trend. (b) Estimate the missing value. (c) {ext[0].strip()}'
    a = f'(a) The {q} {trend} down the group. (b) between {_deg(lo)} and {_deg(hi)} °C (actual {_deg(data[i][1])} °C) (c) {ext[1]}'
    k = f'(a) {trend} [1] (b) in range [1] (c) {ext[2]}'
    if D == 4:
        return Q(s2, a, k + ' [4]', 'multi_step')
    st = 'liquid' if which == 'g7' else 'gas' if which == 'g0' else 'solid'
    return Q(s2 + ' (d) State why a single value in such a table can be used to predict others.', a + ' (d) Elements in a group have the same number of outer electrons, so their properties change gradually and in a regular pattern.',
             k + ' (d) same outer electrons / regular pattern [1] [5]', 'multi_step')


HAL = [('chlorine', 'chloride', 'pale green'), ('bromine', 'bromide', 'orange'), ('iodine', 'iodide', 'brown')]


@t22.add('C2', (1, 2, 3, 4))
def t22_disp(r, D):
    i, j = r.sample(range(3), 2)
    h, _, _ = HAL[i]
    _, ide, _ = HAL[j]
    react = i < j
    p = person(r)
    s = f'{p} adds {h} water to a solution of potassium {ide}.'
    if D <= 1:
        return mq(r, s + ' What happens?', 'A displacement reaction occurs' if react else 'No reaction occurs',
                  ['A displacement reaction occurs', 'No reaction occurs', 'Hydrogen gas is given off', 'A white solid of potassium forms'],
                  f'{cap(h)} is {"more" if react else "less"} reactive than {HAL[j][0]}, so {"it displaces it" if react else "no displacement"}.')
    if react:
        a = f'Yes: {h} is more reactive than {HAL[j][0]}, so it displaces it. {h} + potassium {ide} → potassium {HAL[i][1]} + {HAL[j][0]}; the solution turns {HAL[j][2]}.'
        k = f'reaction occurs [1]; reason: {h} more reactive [1]' + (f'; word equation / colour {HAL[j][2]} [1] [3]' if D >= 3 else ' [2]')
    else:
        a = f'No reaction: {h} is less reactive than {HAL[j][0]}, so it cannot displace it from its compound.'
        k = 'no reaction [1]; ' + (f'{h} less reactive than {HAL[j][0]} [1]; reactivity decreases down Group 7 [1] [3]' if D >= 3 else f'{h} less reactive [1] [2]')
    return Q(s + (' Predict whether a reaction takes place and explain your answer.' if D < 3 else ' Predict whether a reaction takes place, explain why, and if it does, write the word equation and give the colour change.'), a, k, 'explain')


def _grp_c4(r, D):
    p = person(r)
    m1, m2 = sorted(r.sample(range(3), 2))
    met = ['lithium', 'sodium', 'potassium']
    intro = r.choice([f'{p} watches a teacher add small pieces of {met[m1]} and {met[m2]} to separate troughs of water containing universal indicator.',
                      f'In a demonstration in {city(r)}, a teacher drops a rice-grain-sized piece of {met[m1]} into water, then repeats with {met[m2]}. Universal indicator is in the water.'])
    parts = [
        lambda r: (f'Predict which metal reacts more vigorously and explain why.', f'{cap(met[m2])}: it is lower in Group 1; its outer electron is further from the nucleus and is lost more easily.', f'{met[m2]} [1]; outer electron further / lost more easily [1] [2]'),
        lambda r: (f'Write the word equation for the reaction of {met[m1]} with water.', f'{met[m1]} + water → {met[m1]} hydroxide + hydrogen', 'hydroxide [1]; hydrogen [1] [2]'),
        lambda r: ('State and explain the final colour of the universal indicator.', 'Purple (or blue): the metal hydroxide formed is an alkali.', 'purple / blue [1]; alkali formed [1] [2]'),
        lambda r: ('Describe a test for the gas given off.', 'Hold a lighted splint at the mouth of a test tube of the gas: it burns with a squeaky pop (hydrogen).', 'lighted splint [1]; squeaky pop [1] [2]'),
        lambda r: ('Give two safety precautions the teacher should take.', 'Use only a tiny piece; use safety screen and eye protection; handle with tongs, not fingers.', 'any two [1] each [2]'),
        lambda r: ('Explain why caesium is not used in school demonstrations.', 'Caesium is even further down Group 1 so it reacts explosively with water.', 'more reactive down group [1]; explosive / dangerous [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t22.add('C4', (2, 3, 4, 5), 'multi_step')(_grp_c4)
t22.add('C3', (3, 4), 'multi_step')(_grp_c4)

N23 = 'Why elements react: ionic and covalent bonding'
t23 = topic(N23, N23.lower(), 'ionic and covalent bonding', 'why elements react')
FX(t23, 'C1', (1, 2), [
    ('What is an ionic bond?', 'The attraction between oppositely charged ions', 'Ionic bond: electrostatic attraction between positive and negative ions formed by electron transfer.',
     ['A shared pair of electrons between two atoms', 'The attraction between two neutrons', 'A bond between two noble gas atoms']),
    ('What is a covalent bond?', 'A shared pair of electrons between two atoms', 'Covalent: non-metal atoms share pairs of electrons.', ['The transfer of electrons from a metal to a non-metal', 'The attraction between oppositely charged ions', 'The attraction between protons and neutrons']),
    ('Ionic bonding usually happens between', 'a metal and a non-metal', 'Metals lose electrons; non-metals gain them.', ['two non-metals', 'two noble gases', 'two metals in a solution']),
    ('When a sodium atom becomes a sodium ion it', 'loses one electron', 'Na (2,8,1) loses one electron to become Na⁺ (2,8).', ['gains one electron', 'loses one proton', 'gains one proton']),
    ('What is the charge on a chloride ion?', '1−', 'Cl (2,8,7) gains one electron to give Cl⁻ (2,8,8).', ['1+', '2−', '0']),
    ('Atoms react to form bonds in order to', 'obtain a full outer shell of electrons', 'A full outer shell (like a noble gas) is stable.', ['increase their number of protons', 'become radioactive', 'gain more neutrons']),
    ('How many pairs of electrons are shared in a molecule of water, H₂O?', '2', 'Oxygen shares one pair with each hydrogen atom: 2 single covalent bonds.', ['1', '3', '4']),
    ('State the type of bonding in methane, CH₄, and explain why.', 'Covalent, because carbon and hydrogen are both non-metals and share electrons.', 'covalent [1]; both non-metals share electrons [1] [2]'),
])
FX(t23, 'C2', (1, 2, 3), [
    ('Explain why a sodium ion has a charge of 1+.', 'It has 11 protons but only 10 electrons after losing one electron, so there is one more positive charge than negative.', '11 protons, 10 electrons [1]; one extra positive charge [1] [2]'),
    ('Explain why noble gas atoms do not usually form bonds.', 'They already have full outer shells, so they do not need to gain, lose or share electrons.', 'full outer shell [1]; no need to gain/lose/share [1] [2]'),
    ('Explain why magnesium oxide has the formula MgO.', 'Magnesium loses two electrons to form Mg²⁺ and oxygen gains two to form O²⁻; one of each balances the charges.', 'Mg²⁺ and O²⁻ [1]; charges balance 1:1 [1] [2]'),
    ('Describe the difference between ionic and covalent bonding.', 'Ionic: electrons are transferred from a metal to a non-metal, forming oppositely charged ions that attract. Covalent: non-metal atoms share pairs of electrons.', 'ionic = transfer and ions attract [1]; covalent = sharing pairs [1] [2]'),
    ('Explain why the formula of magnesium chloride is MgCl₂.', 'Magnesium loses two electrons (Mg²⁺) but each chlorine atom can gain only one (Cl⁻), so two chloride ions are needed to balance the charge.', 'Mg²⁺ and Cl⁻ [1]; two Cl⁻ balance 2+ [1] [2]'),
    ('Explain why there are two shared pairs between the atoms in an oxygen molecule, O₂.', 'Each oxygen atom has 6 outer electrons and needs 2 more; sharing two pairs (a double bond) gives each a full outer shell of 8.', '6 outer electrons, needs 2 [1]; two pairs shared / double bond [1] [2]'),
])
misc(t23, 'C2', (2, 3, 4), [
    ('In sodium chloride the sodium and chlorine atoms share a pair of electrons.', 'Sodium transfers an electron to chlorine, forming Na⁺ and Cl⁻ ions held by ionic bonds; sharing happens only in covalent bonds between non-metals.', 'electron transferred [1]; ions attract (ionic) [1] [2]'),
    ('A magnesium ion is positive because it gains protons.', 'The number of protons never changes in a reaction; magnesium loses two electrons, leaving more protons than electrons.', 'protons unchanged [1]; loses electrons [1] [2]'),
    ('Chlorine atoms gain an electron to become Cl⁺ ions.', 'Gaining an electron (negative) gives a negative ion, Cl⁻.', 'gaining electron gives negative charge [1]; Cl⁻ [1] [2]'),
])
METALS_Z = [3, 11, 19, 12, 20]
NONM_Z = [8, 9, 16, 17]
COV_Z = [6, 7, 8, 9, 16, 17]
_SUBD = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def _form(x, nx, y, ny):
    return f'{x}{"" if nx == 1 else str(nx).translate(_SUBD)}{y}{"" if ny == 1 else str(ny).translate(_SUBD)}'


def ionic_info(Zm, Zn):
    cm = shells(Zm)[-1]
    an = 8 - shells(Zn)[-1]
    l = cm * an // math.gcd(cm, an)
    return cm, an, l // cm, l // an


@t23.add('C3', (1, 2, 3, 4, 5))
def t23_ionic(r, D):
    Zm, Zn = r.choice(METALS_Z), r.choice(NONM_Z)
    cm, an, nm_, nn = ionic_info(Zm, Zn)
    m, n = EL[Zm], EL[Zn]
    ion_n = {8: 'oxide', 9: 'fluoride', 16: 'sulfide', 17: 'chloride'}[Zn]
    name = f'{m[0]} {ion_n}'
    fm = _form(m[1], nm_, n[1], nn)
    sup = {1: '⁺', 2: '²⁺'}[cm]
    nsup = {1: '⁻', 2: '²⁻'}[an]
    if D <= 1:
        return mq(r, f'What is the formula of {name}?', fm, sorted({_form(m[1], 1, n[1], 1), _form(m[1], 2, n[1], 1), _form(m[1], 1, n[1], 2), _form(m[1], 2, n[1], 3)} - {fm}),
                  f'{m[1]}{sup} and {n[1]}{nsup}: charges balance in {fm}.')
    s = f'{cap(m[0])} (atomic number {Zm}) reacts with {n[0]} (atomic number {Zn}) to form {name}.'
    if D == 2:
        return Q(s + ' State how many electrons each metal atom loses and give the charges on the two ions.', f'{cm} electron{"s" if cm > 1 else ""} lost; {m[1]}{sup} and {n[1]}{nsup}',
                 f'{cm} lost [1]; ions {m[1]}{sup} and {n[1]}{nsup} [1] [2]')
    if D == 3:
        return Q(s + ' (a) Give the electron arrangements of both atoms. (b) Describe what happens to the electrons when they react. (c) Deduce the formula of the compound.',
                 f'(a) {m[0]} {arr(Zm)}; {n[0]} {arr(Zn)} (b) each {m[0]} atom loses {cm} electron{"s" if cm > 1 else ""} and each {n[0]} atom gains {an}, forming {m[1]}{sup} and {n[1]}{nsup} (c) {fm}',
                 f'(a) both arrangements [1] (b) transfer described with charges [1] (c) {fm} [1] [3]', 'multi_step')
    s2 = s + f' (a) Give the electron arrangements of the atoms and of the ions formed. (b) Explain how the ions are held together. (c) Deduce the formula, showing how the charges balance.'
    a = (f'(a) {m[0]} {arr(Zm)} → {m[1]}{sup} {arr(Zm - cm)}; {n[0]} {arr(Zn)} → {n[1]}{nsup} {arr(Zn + an)} (b) strong electrostatic attraction between oppositely charged ions (ionic bonds) '
         f'(c) {nm_} × ({cm}+) = {nn} × ({an}−), so {fm}')
    k = '(a) atoms [1]; ions with full outer shells [1] (b) attraction between opposite ions [1] (c) ' + f'{fm} with charge balance [1]'
    if D == 4:
        return Q(s2, a, k + ' [4]', 'multi_step')
    return Q(s2 + ' (d) Suggest why this compound has a high melting point.', a + ' (d) It is a giant ionic lattice with many strong attractions in all directions, needing a lot of energy to break.', k + ' (d) giant lattice / many strong bonds [1] [5]', 'multi_step')


@t23.add('C3', (1, 2, 3, 4))
def t23_cov(r, D):
    Z = r.choice(COV_Z)
    nm, sy, _, _ = EL[Z]
    o = shells(Z)[-1]
    v = 8 - o
    fm = _form(sy, 1, 'H', v)
    names = {6: 'methane', 7: 'ammonia', 8: 'water', 9: 'hydrogen fluoride', 16: 'hydrogen sulfide', 17: 'hydrogen chloride'}
    if D <= 1:
        return mq(r, f'How many covalent bonds does one {nm} atom form with hydrogen atoms in {names[Z]}?', str(v), [str(x) for x in (1, 2, 3, 4, 5) if x != v], f'{nm} has {o} outer electrons, needs {v} more: {v} shared pairs, {fm}.')
    s = f'{cap(nm)} (atomic number {Z}) forms a covalent compound with hydrogen.'
    if D == 2:
        return Q(s + f' State the number of electrons in the outer shell of {art(nm)} {nm} atom and deduce the formula of the compound.', f'{o} outer electrons; {fm}', f'{o} [1]; {fm} ({v} shared pairs) [1] [2]')
    tail = f' (a) Give the electron arrangement of {nm}. (b) Explain how many hydrogen atoms bond to each {nm} atom. (c) Name the compound and give its formula.'
    return Q(s + tail, f'(a) {arr(Z)} (b) {v}: it needs {v} more electrons for a full outer shell and shares one pair with each hydrogen (c) {names[Z]}, {fm}',
             f'(a) {arr(Z)} [1] (b) {v} with reason [1] (c) name and formula [1]' + (' [3]' if D == 3 else '; each H gains a full shell of 2 [1] [4]'), 'multi_step')


@t23.add('C2', (1, 2, 3, 4))
def t23_classify(r, D):
    pool = [('potassium chloride', 'ionic'), ('carbon dioxide', 'covalent'), ('magnesium oxide', 'ionic'), ('ammonia', 'covalent'), ('calcium fluoride', 'ionic'), ('methane', 'covalent'),
            ('lithium oxide', 'ionic'), ('hydrogen chloride', 'covalent'), ('sodium sulfide', 'ionic'), ('water', 'covalent'), ('sulfur dioxide', 'covalent'), ('calcium chloride', 'ionic')]
    a, b = r.sample(pool, 2)
    why = {'ionic': 'a metal and a non-metal, so electrons are transferred to form ions', 'covalent': 'only non-metals, so electrons are shared'}
    return Q(f'State whether the bonding in {a[0]} and in {b[0]} is ionic or covalent. Give a reason for each.', f'{cap(a[0])}: {a[1]} ({why[a[1]]}). {cap(b[0])}: {b[1]} ({why[b[1]]}).',
             f'{a[0]} {a[1]} with reason [1]; {b[0]} {b[1]} with reason [1] [2]', 'explain')


def _bond_c4(r, D):
    Zm, Zn = r.choice(METALS_Z), r.choice(NONM_Z)
    Zc = r.choice(COV_Z)
    cm, an, nm_, nn = ionic_info(Zm, Zn)
    fm = _form('X', nm_, 'Y', nn)
    vc = 8 - shells(Zc)[-1]
    intro = r.choice([f'Element X has atomic number {Zm}, element Y has atomic number {Zn} and element Z has atomic number {Zc}.',
                      f'{person(r)} is given three mystery elements: X (atomic number {Zm}), Y (atomic number {Zn}) and Z (atomic number {Zc}).'])
    parts = [
        lambda r: ('Give the electron arrangement of each element.', f'X {arr(Zm)}; Y {arr(Zn)}; Z {arr(Zc)}', 'all three correct [2]; two correct [1] [2]'),
        lambda r: ('State which element is a metal and explain how you know.', f'X: it has {cm} outer electron{"s" if cm > 1 else ""}, which it loses easily (Group {cm}).', f'X [1]; few outer electrons / Group {cm} [1] [2]'),
        lambda r: ('Describe how X and Y bond together and give the formula of the compound.', f'X loses {cm} electron{"s" if cm > 1 else ""} to form X{"⁺" if cm == 1 else "²⁺"}; Y gains {an} to form Y{"⁻" if an == 1 else "²⁻"}; ionic bonding; formula {fm}.', f'electron transfer with charges [1]; ionic attraction [1]; {fm} [1] [3]'),
        lambda r: ('Predict the type of bond formed between Z and hydrogen and the number of hydrogen atoms that bond to one Z atom.', f'Covalent; {vc} hydrogen atom{"s" if vc > 1 else ""}.', f'covalent [1]; {vc} [1] [2]'),
        lambda r: ('Explain why neither X nor Y forms a bond with argon.', 'Argon has a full outer shell (2,8,8), so it does not gain, lose or share electrons.', 'full outer shell [1]; no electron transfer or sharing [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t23.add('C4', (2, 3, 4, 5), 'multi_step')(_bond_c4)

N24 = 'Simple and giant structures and their properties'
t24 = topic(N24, N24.lower(), 'simple and giant structures')
FX(t24, 'C1', (1, 2), [
    ('Which substance has a giant covalent structure?', 'Diamond', 'Diamond: each carbon atom covalently bonded to four others in a giant structure.', ['Water', 'Methane', 'Sodium chloride']),
    ('Which substance has a simple molecular structure?', 'Carbon dioxide', 'CO₂ exists as small separate molecules.', ['Diamond', 'Silicon dioxide', 'Magnesium oxide']),
    ('Why does a simple molecular substance have a low melting point?', 'The forces between the molecules are weak', 'Only weak intermolecular forces are overcome on melting; the covalent bonds do not break.',
     ['The covalent bonds inside the molecules are weak', 'It contains ions', 'It has a giant structure']),
    ('When does an ionic compound conduct electricity?', 'When molten or dissolved in water', 'Ions must be free to move; in the solid they are fixed in the lattice.', ['Only when solid', 'Never', 'Only when cold']),
    ('Which form of carbon conducts electricity?', 'Graphite', 'Graphite has electrons that are free to move between its layers.', ['Diamond', 'Carbon dioxide', 'Methane']),
    ('Which property is typical of a giant ionic structure?', 'A high melting point', 'Strong attractions between ions in all directions need a lot of energy to overcome.', ['A low boiling point', 'Conducts electricity when solid', 'Exists as small molecules']),
    ('State two properties of diamond.', 'Very hard; very high melting point (does not conduct electricity).', 'any two [1] each [2]'),
])
FX(t24, 'C2', (1, 2, 3), [
    ('Explain why diamond is very hard.', 'Each carbon atom is joined to four others by strong covalent bonds in a giant 3-D structure, so a lot of force is needed to break it.', 'four strong covalent bonds per atom [1]; giant rigid structure [1] [2]'),
    ('Explain why graphite is soft and slippery and is used in pencils.', 'It is made of layers of carbon atoms with weak forces between the layers, so the layers slide over each other and rub off onto paper.', 'layers [1]; weak forces between layers so they slide [1] [2]'),
    ('Explain why solid sodium chloride does not conduct electricity but molten sodium chloride does.', 'In the solid the ions are held in fixed positions; when molten they are free to move and carry charge.', 'ions fixed in solid [1]; free to move when molten [1] [2]'),
    ('Explain why water boils at a much lower temperature than sand (silicon dioxide).', 'Water is simple molecular with weak forces between molecules; sand is giant covalent, so many strong covalent bonds must be broken.', 'water weak forces between molecules [1]; sand giant covalent strong bonds [1] [2]'),
    ('Explain why graphite conducts electricity but diamond does not.', 'In graphite each carbon bonds to three others, leaving one electron per atom free to move; in diamond all four outer electrons are used in bonds.', 'graphite: free (delocalised) electrons [1]; diamond: all electrons in bonds [1] [2]'),
    ('Explain why iodine turns to a gas at a low temperature even though the atoms in an iodine molecule are joined by a covalent bond.', 'Only the weak forces between I₂ molecules are overcome; the covalent bonds inside the molecules do not break.', 'weak forces between molecules overcome [1]; covalent bond not broken [1] [2]'),
])
misc(t24, 'C2', (2, 3, 4), [
    ('When water boils, the covalent bonds between hydrogen and oxygen atoms break.', 'Boiling only overcomes the weak forces between water molecules; the O–H covalent bonds stay intact (steam is still H₂O).', 'forces between molecules overcome [1]; covalent bonds unbroken [1] [2]'),
    ('All covalent substances have low melting points.', 'Simple molecular substances do, but giant covalent substances such as diamond and silicon dioxide have very high melting points.', 'giant covalent example [1]; high melting point due to many strong bonds [1] [2]'),
    ('Salt conducts electricity because it contains metal atoms.', 'Salt contains ions, and conducts only when molten or dissolved because the ions can then move; solid salt does not conduct.', 'ions must move [1]; only molten or dissolved [1] [2]'),
])
STRUCT = {
    'giant ionic': (lambda r: r.choice([614, 680, 734, 801, 858, 996, 1418, 2614, 2852]), 'no', 'yes'),
    'giant covalent': (lambda r: r.choice([1410, 1610, 1710, 2072, 2730, 3550]), 'no', 'no'),
    'simple molecular': (lambda r: r.choice([-218, -182, -114, -78, -23, 5, 44, 80, 114, 119]), 'no', 'no'),
}


@t24.add('C3', (1, 2, 3, 4, 5))
def t24_unknown(r, D):
    kinds = r.sample(list(STRUCT), 3)
    rows = []
    for L, kk in zip('PQR', kinds):
        f, cs, cl = STRUCT[kk]
        rows.append((L, kk, f(r), cs, cl))
    tab = '; '.join(f'{L}: melting point {_deg(mp)} °C, conducts as solid: {cs}, conducts when molten: {cl}' for L, kk, mp, cs, cl in rows)
    s = f'{person(r)} tests three unknown substances. {tab}.'
    why = {'giant ionic': 'high melting point and conducts only when molten (ions free to move)', 'giant covalent': 'very high melting point and does not conduct even when molten',
           'simple molecular': 'low melting point (weak forces between molecules) and does not conduct'}
    L, kk, mp, _, _ = r.choice(rows)
    if D <= 1:
        return mq(r, s + f' Which type of structure does {L} have?', kk, list(STRUCT) + ['giant metallic'], f'{L}: {why[kk]}.')
    if D == 2:
        return Q(s + f' Identify the structure of substance {L} and give a reason.', f'{cap(kk)}: {why[kk]}.', f'{kk} [1]; reason from data [1] [2]')
    ans = ' '.join(f'{x[0]}: {x[1]}.' for x in rows)
    if D == 3:
        return Q(s + ' Identify the type of structure of each substance.', ans, 'one mark each for P, Q and R [3]', 'multi_step')
    s4 = s + ' (a) Identify the type of structure of each substance. (b) Explain why the substance with the lowest melting point melts so easily.'
    lowest = min(rows, key=lambda x: x[2])
    a = ans + f' (b) {lowest[0]} has a {"simple molecular structure: only weak forces between molecules need to be overcome" if lowest[1] == "simple molecular" else "lower melting point because fewer or weaker bonds need breaking"}.'
    if D == 4:
        return Q(s4, a, 'P, Q, R [1] each (b) weak forces between molecules / explanation [1] [4]', 'multi_step')
    return Q(s4 + ' (c) Explain why the giant ionic substance conducts when molten but not when solid.', a + ' (c) Its ions are fixed in the solid lattice but free to move and carry charge when molten.',
             'P, Q, R [1] each (b) explanation [1] (c) ions fixed in solid, mobile when molten [1] [5]', 'multi_step')


USES24 = [('the tips of drill bits', 'diamond', 'it is the hardest substance (strong covalent bonds in a giant structure)'),
          ('electrodes in electrolysis', 'graphite', 'it conducts electricity and has a very high melting point'),
          ('pencil “lead”', 'graphite', 'its layers slide over each other and rub off onto paper'),
          ('lining furnaces', 'magnesium oxide', 'it has a very high melting point (giant ionic)'),
          ('making glass', 'silicon dioxide (sand)', 'it has a giant covalent structure and a high melting point, so glass is hard and heat-resistant'),
          ('a lubricant in machinery', 'graphite', 'its layers slide easily')]


def _str_c4(r, D):
    use, mat, why = r.choice(USES24)
    other = r.choice([u for u in USES24 if u[1] != mat])
    intro = r.choice([f'An engineering company in {city(r)} uses {mat} for {use} and {other[1]} for {other[0]}.',
                      f'{person(r)} reads that {mat} is used for {use}, while {other[1]} is used for {other[0]}.'])
    parts = [
        lambda r: (f'Explain why {mat} is suitable for {use}.', cap(why) + '.', 'property [1]; linked to structure [1] [2]'),
        lambda r: (f'Explain why {other[1]} is suitable for {other[0]}.', cap(other[2]) + '.', 'property [1]; linked to structure [1] [2]'),
        lambda r: ('Diamond and graphite are both pure carbon. Explain why they have such different properties.', 'Their atoms are arranged differently: diamond has each atom bonded to four others in a rigid 3-D network; graphite has layers (three bonds per atom) with weak forces between layers and free electrons.', 'different arrangement [1]; diamond 4 bonds 3-D [1]; graphite layers / free electrons [1] [3]'),
        lambda r: ('Explain why a simple molecular substance such as wax would be unsuitable for this work.', 'It has a low melting point and is soft, because only weak forces act between its molecules.', 'low melting point / soft [1]; weak forces between molecules [1] [2]'),
        lambda r: ('Suggest one property, other than melting point, that should be tested before choosing a material.', 'Hardness, electrical conductivity, cost, or how it reacts with substances it touches.', 'valid property with reason [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t24.add('C4', (2, 3, 4, 5), 'multi_step')(_str_c4)
t24.add('C3', (3, 4), 'multi_step')(_str_c4)
CHAPTERS[2] = [t21, t22, t23, t24]

# =========================================================== 3 Forces and energy
N31 = 'Density: calculating and comparing densities and floating and sinking'
t31 = topic(N31, N31.lower(), 'density', 'floating and sinking')
FX(t31, 'C1', (1, 2), [
    ('Which equation is used to calculate density?', 'density = mass ÷ volume', 'Density is mass per unit volume.', ['density = volume ÷ mass', 'density = mass × volume', 'density = mass + volume']),
    ('Which unit could be used for density?', 'g/cm³', 'Mass in g ÷ volume in cm³ gives g/cm³ (or kg/m³).', ['g/cm²', 'N/cm³', 'cm³/g']),
    ('The density of water is 1.0 g/cm³. Which object will float in water?', 'A block of wood of density 0.7 g/cm³', 'Objects less dense than water float.', ['A steel nail of density 7.8 g/cm³', 'A glass marble of density 2.5 g/cm³', 'A stone of density 2.7 g/cm³']),
    ('Which method is used to find the volume of an irregular stone?', 'Displacement of water in a measuring cylinder', 'The rise in water level equals the volume of the stone.', ['Measuring its length, width and height', 'Weighing it on a balance', 'Timing how long it takes to sink']),
    ('Two liquids that do not mix are poured into a jar. Which liquid forms the bottom layer?', 'The one with the higher density', 'Denser liquids sink below less dense ones.', ['The one with the larger volume', 'The one poured in first', 'The one with the smaller mass']),
    ('A piece of iron is cut in half. What happens to the density of each half?', 'It stays the same', 'Density is a property of the material: both mass and volume halve.', ['It halves', 'It doubles', 'It becomes zero']),
    ('State the two measurements needed to calculate the density of an object.', 'Its mass and its volume.', 'mass [1]; volume [1] [2]'),
])
FX(t31, 'C2', (1, 2, 3), [
    ('A block of wood and a block of iron have the same mass. Explain which has the larger volume.', 'The wood, because it is less dense; for the same mass a lower density means a larger volume.', 'wood [1]; lower density so larger volume [1] [2]'),
    ('Explain why a steel ship floats although steel is denser than water.', 'The ship is hollow and contains air, so its average density (total mass ÷ total volume) is less than that of water.', 'hollow / contains air [1]; average density less than water [1] [2]'),
    ('Explain, using the particle model, why most substances are less dense as gases than as solids.', 'The same particles (same mass) are much further apart in a gas, so the volume is much bigger and density is lower.', 'same mass [1]; particles far apart / larger volume [1] [2]'),
    ('Explain why ice floats on water.', 'Ice is less dense than liquid water, because water expands when it freezes.', 'ice less dense [1]; water expands on freezing [1] [2]'),
    ('Explain why a hot-air balloon rises.', 'Heating the air makes it expand so it becomes less dense than the cooler air around it; the less dense balloon rises.', 'hot air expands / less dense [1]; less dense than surrounding air so rises [1] [2]'),
    ('Describe how to find the density of a liquid such as cooking oil.', 'Find the mass of an empty measuring cylinder, add a measured volume of oil and find the mass again; mass of oil = difference; density = mass ÷ volume.', 'masses empty and full [1]; volume read [1]; density = m ÷ V [1] [3]'),
])
misc(t31, 'C2', (2, 3, 4), [
    ('Heavy objects always sink and light objects always float.', 'Floating depends on density, not mass: a heavy log floats while a light steel pin sinks.', 'depends on density [1]; counter-example [1] [2]'),
    ('If I cut a cork in half, each half has half the density.', 'Mass and volume both halve, so density stays the same.', 'mass and volume both halve [1]; density unchanged [1] [2]'),
    ('A big block of ice has a larger density than a small ice cube.', 'Density is the same for the same material; the big block has more mass and more volume.', 'same material same density [1]; both mass and volume larger [1] [2]'),
])
for fn_ in (t12_reg, t12_irreg, t12_liquid):
    t31.add('C3', (1, 2, 3, 4, 5), 'numerical')(fn_)
for fn_ in (t12_float, t12_err):
    t31.add('C2', (2, 3, 4), 'explain')(fn_)
t31.add('C4', (2, 3, 4, 5), 'multi_step')(_dens_c4)
LAY = [('honey', 1.42), ('golden syrup', 1.38), ('glycerol', 1.26), ('washing-up liquid', 1.06), ('water', 1.00), ('vegetable oil', 0.92), ('lamp oil', 0.80)]
OBJ = [('a grape', 1.08), ('a plastic bead', 0.95), ('a cherry tomato', 0.99), ('a cork', 0.24), ('a steel bolt', 7.8), ('a rubber ball', 1.15), ('a small candle piece', 0.90), ('a piece of pasta', 1.30)]


@t31.add('C3', (1, 2, 3, 4, 5))
def t31_column(r, D):
    liqs = sorted(r.sample(LAY, 3), key=lambda x: -x[1])
    while abs(liqs[0][1] - liqs[1][1]) < 0.05 or abs(liqs[1][1] - liqs[2][1]) < 0.05:
        liqs = sorted(r.sample(LAY, 3), key=lambda x: -x[1])
    sh = liqs[:]
    r.shuffle(sh)
    ob, od = r.choice([o for o in OBJ if all(abs(o[1] - l[1]) > 0.02 for l in liqs)])
    p = person(r)
    s = f'{p} carefully pours three liquids, one at a time, down the side of a tall jar so that they form separate layers: ' + ', '.join(f'{n} (density {g(d, 3)} g/cm³)' for n, d in sh) + '.'
    order = ', '.join(n for n, d in liqs)
    if D <= 1:
        return mq(r, s + ' Which liquid forms the bottom layer?', liqs[0][0], [x[0] for x in sh if x[0] != liqs[0][0]] + ['whichever liquid is poured in first'], f'Densest liquid ({liqs[0][0]}) sinks to the bottom.')
    if D == 2:
        return Q(s + ' List the liquids from the bottom layer to the top layer and explain the order.', f'{order}; the densest liquid sinks to the bottom and the least dense floats on top.', f'correct order [1]; density explanation [1] [2]')
    above = [n for n, d in liqs if d > od]
    below = [n for n, d in liqs if d < od]
    if od > liqs[0][1]:
        where = 'It sinks to the bottom of the jar, because it is denser than all three liquids.'
    elif od < liqs[-1][1]:
        where = 'It floats on top of the top layer, because it is less dense than all three liquids.'
    else:
        lower = min([l for l in liqs if l[1] > od], key=lambda l: l[1])
        upper = max([l for l in liqs if l[1] < od], key=lambda l: l[1])
        where = f'It sinks through the {upper[0]} and floats on the {lower[0]}, at the boundary between them, because it is denser than {upper[0]} but less dense than {lower[0]}.'
    s3 = s + f' (a) List the liquids from bottom to top. (b) {p} then drops in {ob} (density {g(od, 3)} g/cm³). Predict where it comes to rest and explain why.'
    if D == 3:
        return Q(s3, f'(a) {order} (b) {where}', '(a) correct order [1] (b) position [1]; density comparison [1] [3]', 'multi_step')
    m = r.choice([20, 25, 30, 40, 50])
    V = m / od
    s4 = s3 + f' (c) The {ob.split(" ", 1)[1]} has a mass of {m} g. Calculate its volume.'
    a = f'(a) {order} (b) {where} (c) V = m ÷ ρ = {m} ÷ {g(od, 3)} = {g(V)} cm³'
    k = f'(a) order [1] (b) position with reason [1] (c) V = m/ρ [1]; {g(V)} cm³ [1]'
    if D == 4:
        return Q(s4, a, k + ' [4]', 'multi_step')
    vb = r.choice([10, 20, 25, 50])
    return Q(s4 + f' (d) Calculate the mass of {vb} cm³ of the {liqs[0][0]}.', a + f' (d) m = ρ × V = {g(liqs[0][1], 3)} × {vb} = {g(liqs[0][1] * vb, 3)} g', k + f' (d) {g(liqs[0][1] * vb, 3)} g [1] [5]', 'multi_step')


N32 = 'Heat and temperature: thermal energy, temperature and moving from hot to cold'
t32 = topic(N32, N32.lower(), 'heat and temperature', 'thermal energy')
FX(t32, 'C1', (1, 2), [
    ('In which unit is temperature usually measured in the laboratory?', 'degrees Celsius (°C)', 'Temperature in °C, measured with a thermometer.', ['joules (J)', 'newtons (N)', 'watts (W)']),
    ('In which unit is thermal energy measured?', 'joules (J)', 'Energy, including thermal energy, is measured in joules.', ['degrees Celsius (°C)', 'kilograms (kg)', 'metres (m)']),
    ('Thermal energy always moves', 'from a hotter object to a cooler object', 'Energy transfers from hot to cold until temperatures are equal.', ['from a cooler object to a hotter object', 'from a larger object to a smaller object', 'only from solids to liquids']),
    ('What does the temperature of a substance tell us about its particles?', 'How fast they are moving on average', 'Higher temperature = greater average kinetic energy of particles.', ['How many particles there are', 'How heavy each particle is', 'How far apart the particles are']),
    ('A bath of water at 40 °C and a cup of tea at 80 °C. Which statement is correct?', 'The bath has more thermal energy but a lower temperature', 'The bath has far more particles, so more total thermal energy, even though they move more slowly on average.',
     ['The cup has more thermal energy and a higher temperature', 'They have the same thermal energy', 'The bath has a higher temperature']),
    ('When two objects reach the same temperature, what happens to the net transfer of thermal energy between them?', 'It stops', 'At the same temperature there is no net transfer (thermal equilibrium).', ['It increases', 'It reverses direction', 'It doubles']),
    ('State two factors that affect the amount of thermal energy stored in an object.', 'Any two: its mass; its temperature; the material it is made of.', 'any two [1] each [2]'),
])
FX(t32, 'C2', (1, 2, 3), [
    ('Explain the difference between heat (thermal energy) and temperature.', 'Thermal energy is the total energy of all the particles, measured in J; temperature is a measure of the average kinetic energy of the particles, measured in °C.', 'thermal energy = total energy (J) [1]; temperature = average energy of particles (°C) [1] [2]'),
    ('Explain why a swimming pool at 25 °C contains more thermal energy than a cup of coffee at 75 °C.', 'The pool has a much larger mass (many more particles); total energy depends on mass as well as temperature.', 'much greater mass / more particles [1]; total energy depends on mass and temperature [1] [2]'),
    ('A cup of hot chocolate is left on a table. Explain why it cools down and then stops cooling.', 'Thermal energy moves from the hot drink to the cooler surroundings until the drink reaches room temperature; then there is no temperature difference so no net transfer.', 'energy flows hot → cold [1]; stops at room temperature / no difference [1] [2]'),
    ('Describe what happens to the particles of a metal spoon when it is placed in hot water.', 'The particles gain energy and vibrate faster, so the temperature of the spoon rises.', 'particles gain energy [1]; vibrate faster / temperature rises [1] [2]'),
    ('Explain why holding an ice cube makes your hand feel cold.', 'Thermal energy moves from your warmer hand into the ice, so your hand loses energy and its temperature falls.', 'energy from hand to ice [1]; hand cools [1] [2]'),
    ('Explain why a large pan of water takes longer to boil than a small one on the same cooker.', 'More mass of water needs more thermal energy to reach the same temperature, and the cooker supplies energy at the same rate.', 'more mass needs more energy [1]; same rate of supply / takes longer [1] [2]'),
])
misc(t32, 'C2', (2, 3, 4), [
    ('Cold flows from the ice cube into my drink.', 'There is no “cold” flowing: thermal energy flows from the warmer drink into the ice, so the drink cools.', 'energy flows hot → cold [1]; drink loses energy [1] [2]'),
    ('Heat and temperature mean the same thing.', 'Thermal energy (heat) is total energy in joules; temperature measures average particle energy in °C.', 'distinguish energy (J) [1]; temperature (°C) [1] [2]'),
    ('A blanket keeps you warm because it makes heat.', 'A blanket supplies no energy; it is an insulator that slows the transfer of thermal energy from your body.', 'no energy produced [1]; insulator reduces transfer [1] [2]'),
])


@t32.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t32_cool(r, D):
    T0 = r.choice([70, 75, 80, 85, 90, 95])
    Tr = r.choice([18, 20, 22, 25, 28])
    kk = r.choice([0.06, 0.08, 0.1, 0.12])
    step = r.choice([2, 4, 5])
    ts = [step * i for i in range(6)]
    Ts = [round(Tr + (T0 - Tr) * math.exp(-kk * t)) for t in ts]
    drink = r.choice(['a cup of tea', 'a beaker of hot water', 'a mug of hot soup', 'a flask lid of coffee'])
    p = person(r)
    tab = ', '.join(f'{t} min: {T} °C' for t, T in zip(ts, Ts))
    s = f'{p} measures the temperature of {drink} as it cools in a room at {Tr} °C: {tab}.'
    d1 = Ts[0] - Ts[1]
    d5 = Ts[4] - Ts[5]
    if D <= 1:
        return mq(r, s + ' What will the temperature of the drink be after a very long time?', f'{Tr} °C', ['0 °C', f'{Ts[-1]} °C', '100 °C', f'{(T0 + Tr) // 2} °C'], f'It cools until it reaches room temperature, {Tr} °C.')
    if D == 2:
        return Q(s + f' Calculate the fall in temperature in the first {step} minutes and in the last {step} minutes.', f'{d1} °C and {d5} °C', f'{Ts[0]} − {Ts[1]} = {d1} °C [1]; {Ts[4]} − {Ts[5]} = {d5} °C [1] [2]')
    s3 = s + f' (a) Calculate the temperature fall in the first {step} minutes and in the last {step} minutes. (b) Explain why the drink cools more slowly later on.'
    a = f'(a) {d1} °C and {d5} °C (b) The temperature difference between the drink and the room gets smaller, so thermal energy is transferred more slowly.'
    k = f'(a) {d1} and {d5} °C [1] (b) smaller temperature difference [1]; slower transfer of energy [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (c) Predict the final temperature of the drink.', a + f' (c) {Tr} °C (room temperature).', k + f' (c) {Tr} °C [1] [4]', 'multi_step')
    return Q(s3 + ' (c) Predict the final temperature of the drink. (d) Suggest one change that would make the drink cool more slowly.', a + f' (c) {Tr} °C (d) Put a lid on it or use an insulated (double-walled) cup.',
             k + f' (c) {Tr} °C [1] (d) lid / insulation [1] [5]', 'multi_step')


@t32.add('C3', (2, 3, 4, 5), 'numerical')
def t32_mix(r, D):
    T1 = r.choice([10, 15, 20, 24])
    T2 = r.choice([60, 70, 80, 90])
    if D <= 3:
        m = r.choice([100, 150, 200, 250])
        Tf = (T1 + T2) / 2
        return Q(f'{person(r)} mixes {m} g of water at {T1} °C with {m} g of water at {T2} °C in an insulated cup. Assuming no energy is lost, calculate the final temperature and explain your answer.',
                 f'{g(Tf)} °C; the hot water loses as much energy as the cold water gains, and as the masses are equal the temperature change is the same for both.',
                 f'{g(Tf)} °C [1]; energy lost by hot = energy gained by cold [1]' + (' [2]' if D == 2 else '; equal masses so equal temperature changes [1] [3]'))
    m1 = r.choice([100, 200, 300])
    m2 = r.choice([100, 200, 300, 400])
    Tf = (m1 * T1 + m2 * T2) / (m1 + m2)
    return Q(f'{person(r)} mixes {m1} g of water at {T1} °C with {m2} g of water at {T2} °C in an insulated flask. (a) Calculate the final temperature, assuming no energy is lost. (b) State which water has the larger temperature change and explain why. (c) Explain why the real final temperature will be slightly lower.',
             f'(a) ({m1} × {T1} + {m2} × {T2}) ÷ {m1 + m2} = {g(Tf)} °C (b) The {"cold" if m1 < m2 else "hot" if m1 > m2 else "two waters change equally;"} {"water, because it has the smaller mass" if m1 != m2 else "masses are equal"} (c) Some thermal energy is transferred to the flask and the surroundings.',
             '(a) weighted method [1]; ' + f'{g(Tf)} °C [1] (b) correct with reason [1] (c) energy lost to surroundings [1] [4]', 'multi_step')


def _heat_c4(r, D):
    T1 = r.choice([5, 8, 10, 12])
    T2 = r.choice([60, 65, 70, 80])
    Tr = r.choice([20, 22, 25])
    intro = r.choice([f'A can of cold drink at {T1} °C is placed in a bowl of hot water at {T2} °C. The room is at {Tr} °C.',
                      f'{person(r)} puts a metal block at {T1} °C into a beaker of water at {T2} °C on a bench in a laboratory in {city(r)}, where the air is at {Tr} °C.'])
    parts = [
        lambda r: ('State the direction in which thermal energy is transferred between the two objects.', 'From the hot water to the colder object.', 'hot → cold [1]'),
        lambda r: ('Describe what happens to the movement of the particles in each object.', 'Particles in the colder object speed up (gain energy); particles in the hot water slow down (lose energy).', 'cold object particles speed up [1]; hot water particles slow down [1] [2]'),
        lambda r: ('Explain why the final temperature of both objects will be the same.', 'Energy transfers until there is no temperature difference; then there is no net transfer (thermal equilibrium).', 'transfer until equal temperature [1]; no net transfer after [1] [2]'),
        lambda r: (f'Explain why, after a long time, both end up at {Tr} °C.', f'The water also loses energy to the cooler room until everything reaches room temperature, {Tr} °C.', f'energy lost to surroundings [1]; reaches {Tr} °C [1] [2]'),
        lambda r: ('Suggest how to measure the temperatures accurately.', 'Use a thermometer or temperature probe, stir the water, read at eye level and wait for the reading to become steady.', 'any two good points [1] each [2]'),
        lambda r: ('Explain why the hot water has more thermal energy than the cold object even if they had the same mass.', 'It is at a higher temperature, so its particles have more kinetic energy on average.', 'higher temperature [1]; more particle energy [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t32.add('C4', (2, 3, 4, 5), 'multi_step')(_heat_c4)

N33 = 'Conservation of energy and energy dissipation'
t33 = topic(N33, N33.lower(), 'conservation of energy', 'energy dissipation')
FX(t33, 'C1', (1, 2), [
    ('Which statement is the law of conservation of energy?', 'Energy cannot be created or destroyed, only transferred or stored', 'Total energy stays the same; it is only transferred between stores.',
     ['Energy is used up when a device works', 'Energy can be created by machines', 'Energy is destroyed as thermal energy']),
    ('What is meant by “dissipated” energy?', 'Energy that spreads out into the surroundings and is less useful', 'Dissipated energy is wasted energy, usually spread out as thermal energy in the surroundings.',
     ['Energy that is destroyed', 'Energy that is stored in a battery', 'Energy that increases the useful output']),
    ('In a filament lamp, most of the wasted energy is transferred as', 'thermal energy to the surroundings', 'A filament lamp gets very hot; most input energy heats the surroundings.', ['sound', 'kinetic energy', 'chemical energy']),
    ('Which energy store decreases when a ball falls?', 'Gravitational potential energy', 'As it falls, gravitational potential energy is transferred to kinetic energy.', ['Kinetic energy', 'Elastic potential energy', 'Chemical energy']),
    ('An electric motor is supplied with 100 J of energy and transfers 70 J as kinetic energy. How much energy is dissipated?', '30 J', '100 − 70 = 30 J dissipated (thermal and sound).', ['70 J', '170 J', '0 J']),
    ('A bouncing ball rises less high after each bounce because', 'some energy is dissipated as thermal energy and sound', 'Energy is not destroyed; some is transferred to the surroundings at each bounce.', ['energy is destroyed at each bounce', 'gravity gets stronger', 'the ball gains mass']),
    ('State the useful energy output and one wasted energy output of an electric kettle.', 'Useful: thermal energy of the water. Wasted: thermal energy to the surroundings (or sound).', 'useful [1]; wasted [1] [2]'),
])
FX(t33, 'C2', (1, 2, 3), [
    ('Explain why a car engine gets hot when it is running.', 'Not all the chemical energy from the fuel is transferred to kinetic energy; some is dissipated as thermal energy because of friction and the burning fuel.', 'not all energy useful [1]; dissipated as thermal energy (friction / burning) [1] [2]'),
    ('Explain how lubricating the moving parts of a bicycle reduces energy dissipation.', 'Oil reduces friction between moving parts, so less energy is transferred as thermal energy and sound.', 'less friction [1]; less thermal energy and sound wasted [1] [2]'),
    ('Explain why LED lamps are replacing filament lamps.', 'An LED transfers a much larger proportion of its input energy to light, so less is dissipated as heat; it needs less energy for the same light.', 'more light per joule / less wasted heat [1]; uses less energy for same light [1] [2]'),
    ('A swinging pendulum gradually comes to rest. Explain where its energy has gone.', 'Its energy is transferred to the surroundings as thermal energy by air resistance and friction at the pivot; the total energy is conserved but spread out.', 'air resistance / friction [1]; thermal energy in surroundings, not destroyed [1] [2]'),
    ('Explain why dissipated energy is difficult to use again.', 'It is spread out thinly into the surroundings at a low temperature, so it cannot easily be collected to do useful work.', 'spread out [1]; low temperature / hard to collect [1] [2]'),
    ('Describe the energy changes when a person climbs a flight of stairs.', 'Chemical energy in the body (from food) is transferred to gravitational potential energy, with some dissipated as thermal energy.', 'chemical → gravitational potential [1]; some thermal energy [1] [2]'),
])
misc(t33, 'C2', (2, 3, 4), [
    ('When my phone battery goes flat, the energy has been used up and no longer exists.', 'Energy is not destroyed; it has been transferred from the chemical store of the battery to the surroundings, mostly as thermal energy.', 'energy conserved [1]; transferred to surroundings / thermal [1] [2]'),
    ('An efficient machine creates more energy than it takes in.', 'No machine can create energy; output energy can never be greater than input energy, and an efficient machine just wastes less.', 'energy cannot be created [1]; output ≤ input [1] [2]'),
    ('The bouncing ball loses energy so the total energy decreases.', 'The ball’s energy decreases, but the energy is transferred to the surroundings as thermal energy and sound; total energy stays the same.', 'energy transferred not lost [1]; total conserved [1] [2]'),
])
DEV = [('filament lamp', 'electrical', 'light', 'thermal energy in the surroundings', (0.05, 0.1)), ('LED lamp', 'electrical', 'light', 'thermal energy in the surroundings', (0.4, 0.5)),
       ('electric motor', 'electrical', 'kinetic energy', 'thermal energy and sound', (0.6, 0.75, 0.8)), ('kettle', 'electrical', 'thermal energy of the water', 'thermal energy of the surroundings and sound', (0.8, 0.85, 0.9)),
       ('car engine', 'chemical energy of the fuel', 'kinetic energy', 'thermal energy and sound', (0.25, 0.3)), ('loudspeaker', 'electrical', 'sound', 'thermal energy', (0.02, 0.05)),
       ('hair dryer', 'electrical', 'thermal energy of the air and kinetic energy of the air', 'sound', (0.9, 0.95)), ('wind turbine', 'kinetic energy of the wind', 'electrical', 'thermal energy and sound', (0.35, 0.4, 0.45)),
       ('solar cell', 'light', 'electrical', 'thermal energy', (0.15, 0.2))]


@t33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t33_waste(r, D):
    dv, inp, use, waste, effs = r.choice(DEV)
    Ein = r.choice([200, 400, 500, 800, 1000, 1200, 1500, 2000, 2500])
    eff = r.choice(effs)
    Eu = Ein * eff
    Ew = Ein - Eu
    s = f'{cap(art(dv))} {dv} is supplied with {g(Ein)} J of {inp} energy'.replace('energy energy', 'energy').replace('of the fuel energy', 'of the fuel').replace('of the wind energy', 'of the wind') + f' and transfers {g(Eu)} J as useful {use}.'
    if D <= 1:
        return numq(r, D, s, 'energy dissipated', Ew, ' J', f'{g(Ein)} − {g(Eu)}', [Ein + Eu, Eu, Ein])
    if D == 2:
        return Q(s + ' Calculate the energy dissipated and state the main form of the wasted energy.', f'{g(Ew)} J, mainly as {waste}', f'{g(Ein)} − {g(Eu)} = {g(Ew)} J [1]; {waste} [1] [2]')
    if D == 3:
        return Q(s + ' (a) Calculate the energy dissipated. (b) Calculate the percentage of the input energy that is useful.', f'(a) {g(Ew)} J (b) {g(eff * 100)}%',
                 f'(a) {g(Ew)} J [1] (b) {g(Eu)} ÷ {g(Ein)} × 100 [1] = {g(eff * 100)}% [1] [3]', 'multi_step')
    t_ = r.choice([10, 20, 30, 60])
    s4 = (f'{cap(art(dv))} {dv} transfers {g(Ein / t_, 3)} J of energy every second. In {t_} s it transfers {g(Eu)} J usefully as {use}. (a) Calculate the total energy supplied in {t_} s. '
          f'(b) Calculate the energy dissipated. (c) Calculate the percentage of the energy that is wasted.')
    a = f'(a) {g(Ein / t_, 3)} × {t_} = {g(Ein)} J (b) {g(Ew)} J (c) {g((1 - eff) * 100)}%'
    k = f'(a) {g(Ein)} J [1] (b) {g(Ein)} − {g(Eu)} = {g(Ew)} J [1] (c) {g(Ew)} ÷ {g(Ein)} × 100 [1] = {g((1 - eff) * 100)}% [1]'
    if D == 4:
        return Q(s4, a, k + ' [4]', 'multi_step')
    return Q(s4 + ' (d) Explain why the total energy output is equal to the energy supplied.', a + ' (d) Energy cannot be created or destroyed, so useful + wasted energy must equal the input (conservation of energy).',
             k + ' (d) conservation of energy [1] [5]', 'multi_step')


@t33.add('C3', (2, 3, 4, 5), 'numerical')
def t33_bounce(r, D):
    h1 = r.choice([1.0, 1.2, 1.5, 2.0, 2.4, 3.0])
    f = r.choice([0.5, 0.6, 0.64, 0.7, 0.75, 0.8])
    h2 = h1 * f
    ball = r.choice(['a tennis ball', 'a rubber ball', 'a basketball', 'a golf ball', 'a table-tennis ball'])
    s = f'{person(r)} drops {ball} from a height of {g(h1)} m. It bounces back up to {g(h2)} m.'
    if D == 2:
        return Q(s + ' Explain why the ball does not return to its starting height.', 'At the bounce some energy is dissipated as thermal energy (and sound), so the ball has less energy and less gravitational potential energy at the top.',
                 'energy transferred to thermal / sound [1]; less GPE so lower height [1] [2]')
    s3 = s + ' (a) Describe the energy changes from the moment of release to the top of the bounce. (b) The gravitational potential energy is proportional to height. Calculate the percentage of the original energy the ball still has at the top of the bounce.'
    a = f'(a) Gravitational potential → kinetic as it falls; at impact some kinetic is dissipated as thermal and sound, and some stored as elastic energy then back to kinetic; kinetic → gravitational potential as it rises. (b) {g(h2)} ÷ {g(h1)} × 100 = {g(f * 100)}%'
    k = f'(a) GPE → KE [1]; dissipation at bounce [1] (b) {g(h2)} ÷ {g(h1)} × 100 = {g(f * 100)}% [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    h3 = h2 * f
    return Q(s3 + ' (c) Predict the height of the second bounce if the same fraction of energy is kept.', a + f' (c) {g(h2)} × {g(f)} = {g(h3)} m', k + f' (c) {g(h3)} m [1] [4]' if D == 4 else k + f' (c) {g(h3)} m [2] [5]', 'multi_step')


def _en_c4(r, D):
    dv, inp, use, waste, effs = r.choice(DEV)
    Ein = r.choice([500, 1000, 2000, 2500])
    eff = r.choice(effs)
    Eu = Ein * eff
    intro = r.choice([f'{cap(art(dv))} {dv} in a home in {city(r)} is supplied with {g(Ein)} J of energy. {g(Eu)} J is transferred usefully as {use}.',
                      f'{person(r)} investigates {art(dv)} {dv}. For every {g(Ein)} J supplied, {g(Eu)} J is transferred as useful {use}.'])
    parts = [
        lambda r: ('Calculate the energy wasted.', f'{g(Ein - Eu)} J', f'{g(Ein)} − {g(Eu)} = {g(Ein - Eu)} J [1]'),
        lambda r: ('Name the main form of the wasted energy and where it goes.', f'{cap(waste)}, spreading into the surroundings.', 'form [1]; surroundings [1] [2]'),
        lambda r: ('Calculate the percentage of the input energy that is useful.', f'{g(eff * 100)}%', f'{g(Eu)} ÷ {g(Ein)} × 100 [1] = {g(eff * 100)}% [1] [2]'),
        lambda r: ('Draw or describe an energy flow (Sankey) diagram for the device.', f'An arrow {g(Ein)} J wide splitting into a useful arrow of {g(Eu)} J ({use}) and a wasted arrow of {g(Ein - Eu)} J; widths in proportion.', 'input splits into useful and wasted [1]; widths in proportion and labelled [1] [2]'),
        lambda r: ('Explain how the total energy output compares with the energy supplied.', 'They are equal: energy is conserved, so useful + wasted = input.', 'equal [1]; conservation of energy [1] [2]'),
        lambda r: ('Suggest one way to reduce the wasted energy.', 'Reduce friction by lubrication, use insulation, or use a more efficient design (e.g. LED).', 'valid method [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t33.add('C4', (2, 3, 4, 5), 'multi_step')(_en_c4)

N34 = 'Ways of transferring thermal energy: conduction, convection and radiation'
t34 = topic(N34, N34.lower(), 'conduction convection radiation', 'transferring thermal energy')
FX(t34, 'C1', (1, 2), [
    ('In which state of matter does conduction mainly take place?', 'Solids', 'Particles in solids are close together and pass vibrations on.', ['Gases', 'A vacuum', 'Liquids only']),
    ('Convection can take place in', 'liquids and gases', 'Convection needs particles that can move (fluids).', ['solids only', 'a vacuum', 'solids and liquids only']),
    ('Which method of thermal energy transfer can take place through a vacuum?', 'Radiation', 'Infrared radiation is a wave and needs no particles.', ['Conduction', 'Convection', 'Evaporation']),
    ('Which surface is the best emitter of infrared radiation?', 'Dull black', 'Dark, matt surfaces are the best emitters and absorbers.', ['Shiny silver', 'Shiny white', 'Polished metal']),
    ('Which material is the best thermal conductor?', 'Copper', 'Metals are good conductors; copper is one of the best.', ['Wood', 'Plastic', 'Air']),
    ('Why are many insulating materials full of trapped air?', 'Air is a poor conductor and trapped air cannot form convection currents', 'Still air conducts poorly and cannot circulate.', ['Air is a good conductor', 'Air absorbs all radiation', 'Air makes the material heavier']),
    ('Name the three ways in which thermal energy can be transferred.', 'Conduction, convection and radiation.', 'all three [2]; two [1] [2]'),
])
FX(t34, 'C2', (1, 2, 3), [
    ('Explain how a convection current forms in a pan of water heated from below.', 'Water at the bottom is heated, expands and becomes less dense so it rises; cooler, denser water sinks to take its place, forming a circulating current.', 'heated water expands / less dense [1]; rises [1]; cooler denser water sinks [1] [3]'),
    ('Explain why metals are good conductors of thermal energy.', 'They have free electrons that move quickly and carry energy, as well as vibrating particles passing energy to neighbours.', 'free electrons carry energy [1]; vibrations passed on [1] [2]'),
    ('Explain why houses in hot countries are often painted white.', 'White surfaces reflect most infrared radiation and absorb little, so the house heats up less.', 'white reflects radiation [1]; absorbs less so stays cooler [1] [2]'),
    ('Explain how a vacuum flask keeps a drink hot.', 'The vacuum stops conduction and convection; the silvered walls reflect infrared radiation back; the stopper reduces convection and evaporation.', 'vacuum stops conduction and convection [1]; silvered surface reduces radiation [1] [2]'),
    ('Explain why the heating element of an electric kettle is at the bottom.', 'Water heated at the bottom becomes less dense and rises, setting up convection currents that heat all the water.', 'heated water rises [1]; convection heats whole kettle [1] [2]'),
    ('Explain why the Sun’s energy reaches the Earth by radiation and not by conduction or convection.', 'Space is a vacuum with no particles, so conduction and convection cannot happen; radiation needs no medium.', 'space is a vacuum / no particles [1]; radiation needs no medium [1] [2]'),
])
misc(t34, 'C2', (2, 3, 4), [
    ('Heat rises.', 'Hot fluids (air or water) rise because they are less dense; thermal energy itself can move in any direction, e.g. by conduction or radiation downwards.', 'it is hot fluid that rises (density) [1]; energy can travel in any direction [1] [2]'),
    ('A metal bench feels colder than a wooden bench because the metal is at a lower temperature.', 'Both are at the same temperature; metal is a better conductor so it takes energy from your hand faster, making it feel colder.', 'same temperature [1]; metal conducts energy away faster [1] [2]'),
    ('Shiny surfaces are good at absorbing radiation.', 'Shiny surfaces reflect most infrared and are poor absorbers; dull black surfaces are the best absorbers.', 'shiny reflects [1]; dull black best absorber [1] [2]'),
])
COND = [('copper', 400), ('aluminium', 240), ('brass', 110), ('iron', 80), ('steel', 50)]


@t34.add('C3', (1, 2, 3, 4, 5))
def t34_rods(r, D):
    ms = r.sample(COND, 4)
    k = r.choice([2400, 3000, 3600, 4800])
    ts = {m: round(k / c) for m, c in ms}
    p = person(r)
    sh = ms[:]
    r.shuffle(sh)
    tab = ', '.join(f'{m} {ts[m]} s' for m, c in sh)
    s = f'{p} fixes a drawing pin with wax to the end of rods of different metals, all the same length and thickness. The other ends are heated equally. Times for the pins to fall: {tab}.'
    best = max(ms, key=lambda x: x[1])[0]
    rank = ', '.join(m for m, c in sorted(ms, key=lambda x: -x[1]))
    if D <= 1:
        return mq(r, s + ' Which metal is the best thermal conductor?', best, [m for m, c in ms if m != best] + ['wood'], f'Shortest time ({ts[best]} s) = best conductor: {best}.')
    if D == 2:
        return Q(s + ' Put the metals in order from best to worst conductor and explain how you decided.', f'{rank}; the shorter the time for the pin to fall, the faster energy is conducted.', 'correct order [1]; shorter time = better conductor [1] [2]')
    s3 = s + ' (a) Put the metals in order from best to worst conductor. (b) Name two variables that must be kept the same. (c) Explain, in terms of particles, how energy travels along the rod.'
    a = f'(a) {rank} (b) Length and thickness of the rods (or amount of wax, distance of pin, heating). (c) Particles at the hot end vibrate more and pass energy to neighbouring particles; free electrons also carry energy along.'
    k = '(a) order [1] (b) two control variables [1] (c) vibrating particles pass energy on [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k + '; free electrons [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Suggest which metal should be used for the base of a cooking pan and why.', a + f' (d) {cap(best)}, because it conducts energy to the food fastest (copper bases spread heat evenly).',
             k + '; free electrons [1] (d) best conductor with reason [1] [5]', 'multi_step')


SURF = [('dull black', 1.0), ('dull grey', 0.8), ('shiny white', 0.55), ('shiny silver', 0.35)]


@t34.add('C3', (1, 2, 3, 4, 5))
def t34_cans(r, D):
    ss = r.sample(SURF, 3)
    T0 = r.choice([70, 75, 80, 85])
    tmin = r.choice([10, 15, 20])
    base = r.choice([20, 22, 24, 26])
    drops = {n: round(base * f) for n, f in ss}
    sh = ss[:]
    r.shuffle(sh)
    tab = ', '.join(f'{n} can: {T0 - drops[n]} °C' for n, f in sh)
    s = f'{person(r)} fills three identical metal cans, painted different colours, with water at {T0} °C. After {tmin} minutes the temperatures are: {tab}.'
    best = max(ss, key=lambda x: x[1])[0]
    if D <= 1:
        return mq(r, s + ' Which surface is the best emitter of infrared radiation?', best, [n for n, f in SURF if n != best], f'Biggest temperature fall: {best} can emitted energy fastest.')
    n1 = r.choice(ss)[0]
    if D == 2:
        return Q(s + f' Calculate the fall in temperature of the {n1} can and state which surface emits radiation best.', f'{drops[n1]} °C; {best}', f'{T0} − {T0 - drops[n1]} = {drops[n1]} °C [1]; {best} [1] [2]')
    s3 = s + ' (a) Calculate the temperature fall for each can. (b) State which surface is the best emitter and explain how the results show this. (c) State two variables that must be controlled.'
    a = '(a) ' + ', '.join(f'{n} {drops[n]} °C' for n, f in sh) + f' (b) {best}: it lost the most energy in the same time (largest fall). (c) Volume and starting temperature of water, size of can, time (any two).'
    k = '(a) all three falls [1] (b) correct surface with reason [1] (c) two variables [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    s4 = s3 + ' (d) Suggest why a lid should be placed on each can.'
    a4 = a + ' (d) To reduce energy lost by evaporation and convection from the water surface, so only radiation from the sides is compared.'
    if D == 4:
        return Q(s4, a4, k + ' (d) reduces evaporation / convection [1] [4]', 'multi_step')
    return Q(s4 + ' (e) Use the results to suggest a colour for the pipes of a solar water heater.', a4 + ' (e) Dull black, because good emitters are also good absorbers of infrared from the Sun.', k + ' (d) [1] (e) dull black with reason [1] [5]', 'multi_step')


def _tr_c4(r, D):
    c = city(r)
    intro = r.choice([f'A family in {c} wants to keep their home warm in winter and cool in summer.', f'{person(r)} is designing a cool box to keep drinks cold at a beach in {c}.',
                      f'An engineer in {c} is designing a solar water heater with black pipes behind a glass cover.'])
    if 'cool box' in intro:
        parts = [
            lambda r: ('Suggest a material for the walls and explain your choice.', 'Polystyrene foam: it traps air, a poor conductor, and the air cannot form convection currents.', 'foam / trapped air [1]; poor conductor / no convection [1] [2]'),
            lambda r: ('Suggest a colour for the outside of the box and explain why.', 'White or shiny: it reflects infrared radiation from the Sun, so less energy is absorbed.', 'white / shiny [1]; reflects radiation [1] [2]'),
            lambda r: ('Explain why the lid must fit tightly.', 'It stops warm air entering by convection and reduces energy transfer into the box.', 'stops convection / air exchange [1]; less energy in [1] [2]'),
            lambda r: ('Explain why ice packs are best placed at the top of the box.', 'Air cooled by the ice becomes denser and sinks, so convection currents carry cold air down over the drinks.', 'cold air denser, sinks [1]; convection cools all drinks [1] [2]'),
        ]
    elif 'solar' in intro:
        parts = [
            lambda r: ('Explain why the pipes are painted dull black.', 'Dull black surfaces are the best absorbers of infrared radiation from the Sun.', 'black best absorber [1]; of infrared [1] [2]'),
            lambda r: ('Explain why the pipes are made of copper.', 'Copper is a good conductor, so energy absorbed at the surface passes quickly to the water inside.', 'good conductor [1]; energy to water [1] [2]'),
            lambda r: ('Explain why the hot water tank is placed above the panel.', 'Heated water is less dense and rises by convection into the tank, while cooler water sinks back to the panel.', 'hot water rises (convection) [1]; cooler water sinks [1] [2]'),
            lambda r: ('Explain why the back of the panel is covered with insulating foam.', 'Foam traps air, a poor conductor, reducing energy lost by conduction and convection from the back.', 'trapped air poor conductor [1]; reduces loss [1] [2]'),
        ]
    else:
        parts = [
            lambda r: ('Explain how loft insulation made of fibre reduces energy loss.', 'The fibres trap air, which is a poor conductor and cannot circulate, so conduction and convection through the roof are reduced.', 'traps air [1]; reduces conduction and convection [1] [2]'),
            lambda r: ('Explain how double glazing reduces energy transfer.', 'The gap between the panes contains air or a vacuum; air is a poor conductor and the narrow gap limits convection.', 'gap with air / vacuum [1]; poor conductor / limited convection [1] [2]'),
            lambda r: ('Explain why a room heater is usually placed low down near the floor.', 'Air warmed by the heater becomes less dense and rises, and cooler air sinks to replace it, setting up a convection current around the room.', 'warm air rises [1]; convection current [1] [2]'),
            lambda r: ('Suggest why light-coloured curtains help keep the house cool in summer.', 'Light colours reflect infrared radiation from the Sun, so less energy is absorbed into the room.', 'reflect radiation [1]; less absorbed [1] [2]'),
        ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t34.add('C4', (2, 3, 4, 5), 'multi_step')(_tr_c4)

N35 = 'Cooling by evaporation'
t35 = topic(N35, N35.lower(), 'evaporation')
FX(t35, 'C1', (1, 2), [
    ('Which particles escape from the surface of a liquid during evaporation?', 'The particles with the most energy', 'The fastest-moving particles near the surface escape.', ['The particles with the least energy', 'Particles from the bottom of the liquid', 'All the particles at once']),
    ('Why does a liquid cool when it evaporates?', 'The particles left behind have a lower average energy', 'Losing the most energetic particles lowers the average kinetic energy, so temperature falls.', ['The particles left behind gain energy', 'Evaporation adds cold particles', 'The liquid absorbs cold from the air']),
    ('Which change increases the rate of evaporation?', 'Blowing air across the surface', 'Moving air carries vapour away so more particles can escape.', ['Covering the liquid', 'Lowering the temperature', 'Making the surface area smaller']),
    ('Evaporation differs from boiling because evaporation', 'happens only at the surface and at any temperature', 'Boiling happens throughout the liquid at the boiling point.', ['happens throughout the liquid', 'happens only at 100 °C', 'needs bubbles to form']),
    ('How does sweating help to cool the body?', 'Sweat evaporates, taking thermal energy from the skin', 'Evaporation of sweat removes energy from the skin.', ['Sweat is colder than the body', 'Sweat reflects sunlight', 'Sweat stops the body producing heat']),
    ('State two factors that increase the rate of evaporation of a puddle.', 'Any two: higher temperature; wind; larger surface area; lower humidity.', 'any two [1] each [2]'),
])
FX(t35, 'C2', (1, 2, 3), [
    ('Explain, in terms of particles, why evaporation cools a liquid.', 'The most energetic particles escape from the surface, so the average kinetic energy of those left falls, and the temperature drops.', 'most energetic escape [1]; average energy of remaining falls [1] [2]'),
    ('Explain why you feel cold when you get out of a swimming pool on a windy day.', 'Water on your skin evaporates quickly in the wind, taking thermal energy from your skin.', 'evaporation [1]; wind increases rate / energy taken from skin [1] [2]'),
    ('Explain why sweating does not cool you as well on a very humid day.', 'The air already contains a lot of water vapour, so sweat evaporates slowly and less energy is removed.', 'humid air / much vapour [1]; slower evaporation [1] [2]'),
    ('Explain why dogs pant on hot days.', 'Panting moves air over the wet tongue and mouth, increasing evaporation, which removes thermal energy.', 'air over wet surfaces [1]; evaporation cools [1] [2]'),
    ('Explain why washing dries faster when it is spread out than when it is folded.', 'Spreading it increases the surface area, so more water particles can escape at once.', 'larger surface area [1]; more particles escape [1] [2]'),
])
misc(t35, 'C2', (2, 3, 4), [
    ('Water only evaporates when it is heated to 100 °C.', 'Evaporation happens at any temperature, at the surface; 100 °C is the boiling point of water.', 'evaporation at any temperature [1]; boiling at 100 °C [1] [2]'),
    ('Sweat cools you because it is cold.', 'Sweat is at body temperature; it cools you by evaporating and taking thermal energy from the skin.', 'sweat not cold [1]; evaporation removes energy [1] [2]'),
])


@t35.add('C3', (1, 2, 3, 4, 5))
def t35_wet(r, D):
    Tr = r.choice([22, 24, 25, 26, 28, 30])
    fall = r.choice([3, 4, 5, 6])
    fall2 = fall + r.choice([2, 3, 4])
    t = r.choice([5, 8, 10])
    p = person(r)
    liq = r.choice(['water', 'ethanol']) if D >= 3 else 'water'
    s = (f'{p} places two thermometers in a room at {Tr} °C. The bulb of thermometer B is wrapped in cotton wool soaked in {liq}; thermometer A is dry. After {t} minutes A reads {Tr} °C and B reads {Tr - fall} °C. '
         f'A fan is then switched on and B falls to {Tr - fall2} °C.')
    if D <= 1:
        return mq(r, s + ' Why does thermometer B show a lower temperature?', f'{cap(liq)} evaporating from the cotton wool takes thermal energy from the bulb', ['The cotton wool is a good conductor', f'The {liq} was colder than the room', 'Thermometer A is faulty'],
                  'Evaporation removes the most energetic particles, cooling the bulb.')
    if D == 2:
        return Q(s + ' Calculate the extra cooling caused by the fan and explain it.', f'{fall2 - fall} °C; the moving air removes vapour so the {liq} evaporates faster, removing energy faster.', f'{fall2} − {fall} = {fall2 - fall} °C [1]; faster evaporation in moving air [1] [2]')
    s3 = s + ' (a) Explain why thermometer B reads lower than A. (b) Explain why the fan lowers the reading further. (c) Explain why thermometer A is included.'
    a = '(a) Evaporation from the wet cotton removes the most energetic particles, so energy is taken from the bulb. (b) The fan carries vapour away so evaporation is faster. (c) It is a control, showing the room temperature.'
    k = '(a) evaporation removes energy [1] (b) faster evaporation [1] (c) control / comparison [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    return Q(s3 + ' (d) Predict, with a reason, how the result would change in very humid air.', a + ' (d) B would fall less, because humid air slows evaporation.', k + ' (d) less cooling with reason [1]' + (' [4]' if D == 4 else ' (e) [1] [5]'), 'multi_step') if D == 4 else \
        Q(s3 + ' (d) Predict, with a reason, how the result would change in very humid air. (e) Suggest why ethanol on the skin feels colder than water at the same temperature.', a + ' (d) B would fall less, because humid air slows evaporation. (e) Ethanol evaporates faster than water, so it removes energy from the skin faster.',
          k + ' (d) less cooling with reason [1] (e) ethanol evaporates faster [1] [5]', 'multi_step')


def _ev_c4(r, D):
    c = city(r)
    Tout = r.choice([32, 35, 38, 40])
    Tin = Tout - r.choice([8, 10, 12, 14])
    intro = r.choice([f'In hot, dry areas near {c}, people keep vegetables in a “pot-in-pot” cooler: a small clay pot inside a larger one, with wet sand between them. On a day at {Tout} °C, the inner pot stays at about {Tin} °C.',
                      f'A shop in {c} uses an evaporative cooler: a fan blows hot air at {Tout} °C through wet pads, and the air comes out at about {Tin} °C.'])
    parts = [
        lambda r: ('Calculate the temperature drop produced.', f'{Tout - Tin} °C', f'{Tout} − {Tin} = {Tout - Tin} °C [1]'),
        lambda r: ('Explain, using ideas about particles, how the cooler works.', 'Water evaporates; the most energetic water particles escape, so the average energy of what remains falls and thermal energy is taken from the inside / the air.', 'evaporation [1]; most energetic particles leave [1]; energy taken from inside / air [1] [3]'),
        lambda r: ('Explain why the cooler works better in dry air than in humid air.', 'Dry air contains little water vapour so evaporation is faster, giving more cooling.', 'dry air faster evaporation [1]; more cooling [1] [2]'),
        lambda r: ('Explain why the cooler must be refilled with water regularly.', 'Water is continually lost by evaporation; without water no evaporation, so no cooling.', 'water evaporates away [1]; no water no cooling [1] [2]'),
        lambda r: ('Suggest why the cooler works better when placed in a breeze.', 'Moving air removes water vapour from the surface so evaporation continues faster.', 'breeze removes vapour [1]; faster evaporation [1] [2]'),
        lambda r: ('Evaluate one advantage and one disadvantage of this cooler compared with an electric refrigerator.', 'Advantage: needs no electricity, cheap. Disadvantage: cannot reach very low temperatures and works poorly in humid weather; needs water.', 'advantage [1]; disadvantage [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t35.add('C4', (2, 3, 4, 5), 'multi_step')(_ev_c4)
CHAPTERS[3] = [t31, t32, t33, t34, t35]


# =========================================================== 4 Maintaining life
N41 = 'Plants and water: water uptake and transport in xylem'
t41 = topic(N41, N41.lower(), 'plants and water', 'xylem')
FX(t41, 'C1', (1, 2), [
    ('Which tissue carries water from the roots to the leaves?', 'Xylem', 'Xylem vessels carry water and mineral ions upwards.', ['Phloem', 'Epidermis', 'Cortex']),
    ('Which cells take in most of the water entering a plant?', 'Root hair cells', 'Root hairs give a large surface area in contact with soil water.', ['Guard cells', 'Palisade cells', 'Xylem cells in the leaf']),
    ('Which statement describes xylem vessels?', 'Long, hollow tubes made of dead cells with no end walls', 'Xylem cells are dead, lose their end walls and form continuous tubes strengthened by lignin.',
     ['Living cells full of chloroplasts', 'Short cells with large nuclei', 'Tubes that carry sugars down to the roots']),
    ('Which substance strengthens the walls of xylem vessels?', 'Lignin', 'Lignin makes xylem walls strong and waterproof, helping support the plant.', ['Starch', 'Chlorophyll', 'Glucose']),
    ('As well as water, xylem transports', 'mineral ions', 'Mineral ions are dissolved in the water carried in the xylem.', ['glucose made in the leaves', 'oxygen from the air', 'starch grains']),
    ('Through which openings does most water leave a leaf?', 'Stomata', 'Water vapour diffuses out through the stomata, mainly on the lower surface.', ['Xylem vessels', 'Root hairs', 'Chloroplasts']),
    ('State the pathway taken by water from the soil to the air.', 'Soil → root hair cell → root cells → xylem in root, stem and leaf → leaf cells → evaporates and leaves through stomata.', 'root hair to xylem [1]; xylem to leaf and out through stomata [1] [2]'),
])
FX(t41, 'C2', (1, 2, 3), [
    ('Explain how root hair cells are adapted for taking in water.', 'Each has a long, thin extension that gives a large surface area in close contact with soil water, so more water can enter.', 'large surface area [1]; more water absorbed / contact with soil water [1] [2]'),
    ('A celery stalk is stood in water containing red dye. After a few hours, red dots are seen when the stalk is cut across. Explain this observation.', 'The dyed water has travelled up the xylem vessels; the dots are the xylem vessels arranged in bundles.', 'dye carried in xylem [1]; dots are xylem vessels / bundles [1] [2]'),
    ('Explain how the structure of xylem helps it to transport water.', 'It forms continuous hollow tubes with no end walls, so water can flow without obstruction; lignin keeps the tubes open and strong.', 'continuous hollow tubes / no end walls [1]; lignin keeps them open [1] [2]'),
    ('Explain why a plant often wilts after it is moved from one pot to another.', 'Root hairs are easily damaged during transplanting, so the plant absorbs less water and its cells lose firmness.', 'root hairs damaged [1]; less water absorbed so wilting [1] [2]'),
    ('Explain what “pulls” water up the xylem of a tall tree.', 'Water evaporates from the leaves and leaves through stomata; this pulls a continuous column of water up the xylem from the roots.', 'evaporation / loss from leaves [1]; pulls water column up [1] [2]'),
    ('Suggest why xylem tissue is found in the veins of leaves.', 'To deliver water and mineral ions to all the leaf cells for photosynthesis and to keep them firm.', 'delivers water to leaf cells [1]; for photosynthesis / support [1] [2]'),
])
misc(t41, 'C2', (2, 3, 4), [
    ('Xylem carries food made in the leaves down to the roots.', 'Xylem carries water and mineral ions up from the roots; sugars are carried by phloem.', 'xylem carries water and minerals up [1]; phloem carries sugars [1] [2]'),
    ('Water enters a plant through its leaves.', 'Water is absorbed mainly through the root hair cells; leaves lose water through stomata.', 'root hairs absorb water [1]; leaves lose water [1] [2]'),
    ('Xylem cells are alive so that they can pump water upwards.', 'Xylem cells are dead and hollow; water is pulled up by evaporation from the leaves, not pumped.', 'xylem dead / hollow [1]; water pulled by transpiration [1] [2]'),
])


@t41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t41_dye(r, D):
    t = r.choice([20, 30, 40, 45, 60])
    d1 = r.choice([24, 30, 36, 42, 48, 54, 60])
    f = r.choice([0.4, 0.5, 0.6])
    d2 = round(d1 * f)
    p = person(r)
    plant = r.choice(['celery stalks', 'white carnation stems', 'stems of busy lizzie plants', 'white rose stems'])
    c1, c2 = r.choice([('in a warm, bright, breezy room', 'in a cool, dark room'), ('in sunlight', 'in a dark cupboard'), ('next to a fan', 'in still air')])
    s = f'{p} stands two {plant} in water containing blue dye, one {c1} and one {c2}. After {t} minutes the dye has risen {d1} mm in the first and {d2} mm in the second.'
    r1, r2 = d1 / t, d2 / t
    if D <= 1:
        return numq(r, D, s, 'rate of dye movement in the first stem', r1, ' mm/min', f'{d1} ÷ {t}', [t / d1, d1 * t, r2])
    if D == 2:
        return Q(s + ' Calculate the rate of movement of the dye in each stem in mm per minute.', f'{g(r1)} mm/min and {g(r2)} mm/min', f'{d1} ÷ {t} = {g(r1)} [1]; {d2} ÷ {t} = {g(r2)} mm/min [1] [2]')
    s3 = s + ' (a) Calculate the rate of movement in each stem. (b) Name the tissue the dye moves through. (c) Explain the difference between the two results.'
    a = f'(a) {g(r1)} and {g(r2)} mm/min (b) Xylem (c) Conditions {c1} increase evaporation of water from the leaves (transpiration), which pulls water up the xylem faster.'
    k = f'(a) both rates [1] (b) xylem [1] (c) more evaporation / transpiration [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    k4 = k + '; pulls water up faster [1]'
    if D == 4:
        return Q(s3, a, k4 + ' [4]', 'multi_step')
    return Q(s3 + ' (d) Suggest how to make the results more reliable.', a + ' (d) Use several stems in each condition, the same length and type, and calculate a mean.', k4 + ' (d) repeats / mean [1] [5]', 'multi_step')


def _xy_c4(r, D):
    c = city(r)
    h = r.choice([20, 30, 40, 60, 80])
    intro = r.choice([f'A florist in {c} receives cut roses that have been out of water for several hours. Some droop even after being placed in a vase.',
                      f'A gardener in {c} notices that a {h} m tall tree must move large volumes of water from its roots to its highest leaves every day.',
                      f'{person(r)} investigates water movement in plants using celery stalks and coloured water.'])
    parts = [
        lambda r: ('Name the tissue that carries water up the stem and describe two features that suit it to this job.', 'Xylem: long hollow tubes with no end walls; walls strengthened with lignin.', 'xylem [1]; two features [1] [2]'),
        lambda r: ('Describe how water enters the plant from the soil.', 'Water moves from the soil into root hair cells, which have a large surface area, then through root cells to the xylem.', 'root hair cells [1]; to xylem through root [1] [2]'),
        lambda r: ('Explain how water is moved up to the leaves.', 'Water evaporates from leaf cells and diffuses out through stomata; this pulls a continuous column of water up the xylem.', 'evaporation / transpiration from leaves [1]; pulls water up xylem [1] [2]'),
        lambda r: ('Suggest why florists cut the bottom of stems under water before placing them in a vase.', 'Air bubbles can enter and block the xylem; cutting under water keeps the water column continuous so water can be taken up.', 'air blocks xylem [1]; cutting under water prevents this [1] [2]'),
        lambda r: ('Give two reasons why leaves need a constant supply of water.', 'Water is a reactant in photosynthesis; it keeps cells firm for support; it cools leaves as it evaporates.', 'any two [1] each [2]'),
        lambda r: ('Describe how to show which tissue in a stem carries water.', 'Stand the stem in coloured dye for some hours, cut across it and look with a hand lens: the coloured spots show the xylem.', 'dye method [1]; cut and observe coloured xylem [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t41.add('C4', (2, 3, 4, 5), 'multi_step')(_xy_c4)

N42 = 'Transpiration and factors affecting its rate'
t42 = topic(N42, N42.lower(), 'transpiration')
FX(t42, 'C1', (1, 2), [
    ('What is transpiration?', 'The loss of water vapour from the leaves of a plant', 'Water evaporates from leaf cells and diffuses out, mainly through stomata.', ['The uptake of water by roots', 'The transport of sugar in phloem', 'The making of glucose in leaves']),
    ('Which condition increases the rate of transpiration?', 'Higher temperature', 'Warmer air speeds up evaporation and diffusion of water vapour.', ['Higher humidity', 'Darkness', 'Still air']),
    ('Which cells open and close the stomata?', 'Guard cells', 'A pair of guard cells surrounds each stoma.', ['Root hair cells', 'Palisade cells', 'Xylem cells']),
    ('On which surface of most leaves are most stomata found?', 'The lower surface', 'More stomata underneath reduces water loss from direct sunlight.', ['The upper surface', 'Equally on both', 'On the veins only']),
    ('Which apparatus is used to measure the rate of water uptake by a leafy shoot?', 'A potometer', 'A potometer measures water uptake, which is almost equal to transpiration.', ['A gas syringe', 'A thermometer', 'A burette']),
    ('Why does transpiration decrease in humid air?', 'There is less difference in water vapour concentration between the leaf and the air', 'Humid air already holds much water vapour, so diffusion out of the leaf is slower.',
     ['The stomata absorb water', 'Light intensity increases', 'The roots stop working']),
    ('State four environmental factors that affect the rate of transpiration.', 'Temperature, light intensity, wind speed (air movement) and humidity.', 'four factors [2]; two or three [1] [2]'),
])
FX(t42, 'C2', (1, 2, 3), [
    ('Explain why transpiration is faster on a windy day.', 'Wind blows away water vapour from around the leaf, keeping a steep concentration gradient so water vapour diffuses out faster.', 'vapour removed [1]; steeper gradient / faster diffusion [1] [2]'),
    ('Explain why transpiration is faster in bright light.', 'Stomata open wider in light (for photosynthesis), so more water vapour can diffuse out.', 'stomata open [1]; more water vapour lost [1] [2]'),
    ('Explain why the shoot for a potometer is cut under water.', 'To stop air entering the xylem, which would block the flow of water and give false readings.', 'prevents air bubbles in xylem [1]; flow not blocked [1] [2]'),
    ('Explain why plants in hot, dry places often close their stomata in the middle of the day.', 'To reduce water loss by transpiration and stop the plant wilting, although this also reduces carbon dioxide uptake.', 'reduce water loss [1]; less CO₂ / photosynthesis as a cost [1] [2]'),
    ('Explain why a potometer measures water uptake rather than exactly the rate of transpiration.', 'Some of the water taken up is used by the plant (e.g. in photosynthesis or to keep cells firm) and is not lost.', 'some water used by plant [1]; uptake ≠ loss exactly [1] [2]'),
    ('Explain why transpiration is useful to a plant.', 'It pulls water and mineral ions up the xylem to the leaves, and evaporation cools the leaves.', 'transport of water and minerals [1]; cooling [1] [2]'),
])
misc(t42, 'C2', (2, 3, 4), [
    ('Transpiration happens fastest on cold, still, humid nights.', 'These conditions slow transpiration: it is fastest when warm, bright, windy and dry.', 'conditions given slow it [1]; correct fast conditions [1] [2]'),
    ('Plants transpire through their roots.', 'Transpiration is loss of water vapour from the leaves, mainly through stomata; roots absorb water.', 'loss from leaves / stomata [1]; roots absorb [1] [2]'),
])
COND42 = [('in still air', 'with a fan blowing'), ('in the shade', 'in bright light'), ('at 15 °C', 'at 30 °C'), ('inside a plastic bag (humid)', 'in open, dry air')]


@t42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t42_pot(r, D):
    a, b = r.choice(COND42)
    t = r.choice([2, 4, 5, 10])
    d1 = r.choice([8, 10, 12, 15, 18, 20])
    d2 = d1 * r.choice([2, 2.5, 3])
    p = person(r)
    s = f'{p} sets up a potometer with a leafy shoot. The air bubble moves {g(d1)} mm in {t} minutes {a} and {g(d2)} mm in {t} minutes {b}.'
    r1, r2 = d1 / t, d2 / t
    if D <= 1:
        return numq(r, D, s, f'rate of bubble movement {b}', r2, ' mm/min', f'{g(d2)} ÷ {t}', [t / d2, d2 * t, r1])
    if D == 2:
        return Q(s + ' Calculate the rate of bubble movement in each condition in mm per minute.', f'{g(r1)} and {g(r2)} mm/min', f'{g(d1)} ÷ {t} = {g(r1)} [1]; {g(d2)} ÷ {t} = {g(r2)} mm/min [1] [2]')
    s3 = s + f' (a) Calculate both rates. (b) Explain why the rate is higher {b}.'
    why = {'with a fan blowing': 'moving air removes water vapour from around the leaves, so water vapour diffuses out faster', 'in bright light': 'stomata open wider, so more water vapour can diffuse out',
           'at 30 °C': 'water evaporates and diffuses faster because particles have more energy', 'in open, dry air': 'dry air has less water vapour, so the concentration gradient is steeper and diffusion is faster'}[b]
    a = f'(a) {g(r1)} and {g(r2)} mm/min (b) {cap(why)}.'
    k = '(a) both rates [1] (b) correct factor [1]; explanation [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    rad = r.choice([0.5, 1.0])
    V = math.pi * rad ** 2 * d2
    s4 = s3 + f' (c) The capillary tube has a radius of {g(rad)} mm. Calculate the volume of water taken up in {t} minutes {b} (volume = π × radius² × distance).'
    a4 = a + f' (c) π × {g(rad)}² × {g(d2)} = {g(V)} mm³'
    k4 = k + f' (c) {g(V)} mm³ [1]'
    if D == 4:
        return Q(s4, a4, k4 + ' [4]', 'multi_step')
    return Q(s4 + ' (d) Explain why the shoot is left for a few minutes in each new condition before readings are taken.', a4 + ' (d) To let the shoot adjust (stomata respond) so the rate becomes steady.', k4 + ' (d) time to adjust / steady rate [1] [5]', 'multi_step')


def _vas_c4(r, D):
    m0 = [r.choice([2.0, 2.2, 2.4, 2.5, 2.8]) for _ in range(4)]
    fr = [r.choice([0.30, 0.34, 0.38]), r.choice([0.24, 0.26, 0.28]), r.choice([0.08, 0.10, 0.12]), r.choice([0.02, 0.03])]
    m1 = [round(a * (1 - f), 2) for a, f in zip(m0, fr)]
    lab = ['A (no petroleum jelly)', 'B (upper surface coated)', 'C (lower surface coated)', 'D (both surfaces coated)']
    tab = '; '.join(f'{l}: {g(a, 3)} g → {g(b, 3)} g' for l, a, b in zip(lab, m0, m1))
    h = r.choice([24, 36, 48])
    intro = f'{person(r)} coats four similar leaves with petroleum jelly (which blocks stomata) and hangs them up for {h} hours. Mass of each leaf at the start → end: {tab}.'
    i = r.randrange(4)
    pc = (m0[i] - m1[i]) / m0[i] * 100
    parts = [
        lambda r: (f'Calculate the percentage loss in mass of leaf {"ABCD"[i]}.', f'{g(pc)}%', f'({g(m0[i], 3)} − {g(m1[i], 3)}) ÷ {g(m0[i], 3)} × 100 [1] = {g(pc)}% [1] [2]'),
        lambda r: ('Explain why percentage loss is used instead of the loss in grams.', 'The leaves started with different masses, so percentage change allows a fair comparison.', 'different starting masses [1]; fair comparison [1] [2]'),
        lambda r: ('Explain why leaf C lost much less mass than leaf B.', 'Most stomata are on the lower surface; coating it blocks most of the routes for water vapour to leave.', 'most stomata on lower surface [1]; blocked so less water lost [1] [2]'),
        lambda r: ('Suggest why leaf D still lost a small amount of mass.', 'Some water evaporates through the waxy cuticle or through gaps in the coating.', 'loss through cuticle / imperfect coating [1]'),
        lambda r: ('Name the process by which the leaves lose mass.', 'Transpiration (evaporation and diffusion of water vapour).', 'transpiration [1]'),
        lambda r: ('Predict how the results would change if the leaves were hung in front of a fan, and explain why.', 'All uncoated surfaces would lose mass faster, because moving air removes water vapour and steepens the gradient.', 'faster loss [1]; vapour removed [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t42.add('C4', (2, 3, 4, 5), 'multi_step')(_vas_c4)
t42.add('C3', (3, 4), 'multi_step')(_vas_c4)

N43 = 'Excretion in humans: the kidneys and removal of urea'
t43 = topic(N43, N43.lower(), 'excretion', 'kidneys', 'urea')
FX(t43, 'C1', (1, 2), [
    ('Where in the body is urea made?', 'In the liver', 'The liver breaks down excess amino acids and makes urea.', ['In the kidneys', 'In the bladder', 'In the stomach']),
    ('Urea is made from the breakdown of', 'excess amino acids', 'Amino acids not needed are broken down; the nitrogen-containing part becomes urea.', ['excess glucose', 'fats', 'starch']),
    ('Which tube carries urine from a kidney to the bladder?', 'Ureter', 'Each kidney has a ureter leading to the bladder.', ['Urethra', 'Renal artery', 'Renal vein']),
    ('Which blood vessel carries blood into a kidney?', 'Renal artery', 'Renal artery in; renal vein out.', ['Renal vein', 'Ureter', 'Vena cava']),
    ('What is excretion?', 'The removal of waste products of metabolism from the body', 'Excretion removes waste made by cells (e.g. urea, CO₂); egestion removes undigested food.',
     ['The removal of undigested food from the body', 'The taking in of food', 'The release of energy from glucose']),
    ('Which substance is normally found in the blood entering the kidney but not in urine of a healthy person?', 'Glucose', 'Glucose is filtered but all is reabsorbed into the blood.', ['Urea', 'Water', 'Salts']),
    ('Which organ excretes carbon dioxide?', 'The lungs', 'CO₂ from respiration is excreted by the lungs.', ['The kidneys', 'The liver', 'The bladder']),
    ('Name three substances found in urine.', 'Water, urea and salts.', 'all three [2]; two [1] [2]'),
])
FX(t43, 'C2', (1, 2, 3), [
    ('Explain why the blood in the renal vein contains less urea than the blood in the renal artery.', 'The kidneys filter urea out of the blood into the urine, so blood leaving the kidney has less urea.', 'kidneys filter / remove urea [1]; into urine [1] [2]'),
    ('Explain why a healthy person’s urine contains no glucose even though glucose is filtered from the blood.', 'All the filtered glucose is reabsorbed back into the blood because the body needs it for respiration.', 'glucose reabsorbed [1]; needed for respiration [1] [2]'),
    ('Explain why urine is darker and more concentrated on a hot day.', 'More water is lost in sweat, so the kidneys reabsorb more water and produce a smaller volume of concentrated urine.', 'water lost in sweat [1]; more water reabsorbed / less urine [1] [2]'),
    ('Describe the difference between excretion and egestion.', 'Excretion removes waste made by cells (urea, CO₂); egestion removes undigested food (faeces) that was never inside cells.', 'excretion = metabolic waste [1]; egestion = undigested food [1] [2]'),
    ('Explain why kidney failure is life-threatening if untreated.', 'Urea, excess water and salts build up in the blood; urea is toxic and water/salt balance is lost.', 'urea builds up / toxic [1]; water and salt balance lost [1] [2]'),
    ('Describe the path of urine from where it is made to where it leaves the body.', 'Kidney → ureter → bladder (stored) → urethra → out of the body.', 'kidney to bladder via ureter [1]; bladder to outside via urethra [1] [2]'),
])
misc(t43, 'C2', (2, 3, 4), [
    ('The kidneys make urea.', 'Urea is made in the liver; the kidneys remove it from the blood into the urine.', 'liver makes urea [1]; kidneys remove it [1] [2]'),
    ('Faeces are an example of excretion.', 'Faeces are mostly undigested food that never entered cells, so their removal is egestion, not excretion.', 'faeces = egestion [1]; excretion is waste of metabolism [1] [2]'),
    ('Urine is made in the bladder.', 'Urine is made in the kidneys; the bladder only stores it.', 'made in kidneys [1]; bladder stores [1] [2]'),
])


@t43.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t43_filter(r, D):
    rate = r.choice([100, 110, 120, 125])
    F = rate * 60 * 24 / 1000
    U = r.choice([1.2, 1.5, 1.6, 1.8, 2.0])
    reab = (F - U) / F * 100
    p = person(r)
    if D <= 1:
        return numq(r, D, f'The kidneys of {p} filter {g(F, 4)} litres of fluid from the blood each day and produce {g(U)} litres of urine.', 'volume of water reabsorbed each day', F - U, ' litres', f'{g(F)} − {g(U)}', [F + U, F, U * 10])
    if D == 2:
        return Q(f'The kidneys filter {g(F, 4)} litres of fluid from the blood each day; {g(U)} litres leave the body as urine. Calculate the percentage of the filtered fluid that is reabsorbed.', f'{g(reab)}%',
                 f'reabsorbed = {g(F, 4)} − {g(U)} = {g(F - U, 4)} litres [1]; {g(F - U, 4)} ÷ {g(F, 4)} × 100 = {g(reab)}% [1] [2]')
    s = f'The kidneys of an adult filter about {rate} cm³ of fluid from the blood every minute.'
    s3 = s + f' (a) Calculate the volume filtered in one day, in litres. (b) The person produces {g(U)} litres of urine a day. Calculate the percentage of the filtered fluid that is reabsorbed.'
    a = f'(a) {rate} × 60 × 24 = {g(rate * 1440)} cm³ = {g(F, 4)} litres (b) {g(reab)}%'
    k = f'(a) {rate} × 1440 [1] = {g(F, 4)} litres [1] (b) ({g(F, 4)} − {g(U)}) ÷ {g(F, 4)} × 100 = {g(reab)}% [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (c) Explain why it is important that most of the filtered fluid is reabsorbed.', a + ' (c) Otherwise the body would lose huge amounts of water (and glucose and salts) and quickly become dehydrated.', k + ' (c) prevents dehydration / keeps useful substances [1] [4]', 'multi_step')
    return Q(s3 + ' (c) Explain why it is important that most of the filtered fluid is reabsorbed. (d) Suggest how the volume of urine would change on a day of heavy exercise in hot weather, and why.',
             a + ' (c) Otherwise the body would lose huge amounts of water and useful substances. (d) Less urine, because more water is lost as sweat so more is reabsorbed.',
             k + ' (c) [1] (d) less urine with reason [1] [5]', 'multi_step')


@t43.add('C3', (2, 3, 4, 5), 'numerical')
def t43_balance(r, D):
    drink = r.choice([1200, 1400, 1500, 1600, 1800])
    food = r.choice([700, 800, 900])
    resp = r.choice([300, 350, 400])
    sweat = r.choice([400, 500, 600, 900, 1200])
    breath = r.choice([300, 350, 400])
    faeces = r.choice([100, 150])
    urine = drink + food + resp - sweat - breath - faeces
    if urine < 300:
        return None
    p = person(r)
    s = f'In one day {p} gains water from drinks ({drink} cm³), food ({food} cm³) and respiration ({resp} cm³), and loses water in sweat ({sweat} cm³), breath ({breath} cm³), faeces ({faeces} cm³) and urine.'
    if D == 2:
        return Q(s + ' Calculate the volume of urine produced if the water gained equals the water lost.', f'{urine} cm³', f'gain = {drink + food + resp} cm³ [1]; urine = {drink + food + resp} − {sweat + breath + faeces} = {urine} cm³ [1] [2]')
    s3 = s + ' (a) Calculate the volume of urine needed to balance the water gained and lost. (b) Name the organs that control the volume of urine.'
    a = f'(a) {urine} cm³ (b) The kidneys.'
    k = f'(a) total gain {drink + food + resp} [1]; urine {urine} cm³ [1] (b) kidneys [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    ex = [x for x in (300, 400, 500, 800, 1000) if urine - x >= 200]
    if not ex:
        return Q(s3, a, k + ' [3]', 'multi_step')
    extra = r.choice(ex)
    s4 = s3 + f' (c) On a hotter day sweat loss increases by {extra} cm³ with no change in drinking. Calculate the new urine volume and describe how the urine would look.'
    nu = urine - extra
    a4 = a + f' (c) {nu} cm³; a smaller volume of darker, more concentrated urine.'
    k4 = k + ' (c) new volume / comment [1]'
    if D == 4:
        return Q(s4, a4, k4 + ' [4]', 'multi_step')
    return Q(s4 + ' (d) Explain why urine is still produced even when the body is short of water.', a4 + ' (d) Urea is toxic and must be removed, and it needs some water to dissolve it.', k4 + ' (d) urea must be removed in solution [1] [5]', 'multi_step')


def _kid_c4(r, D):
    ua, uv = r.choice([(0.30, 0.03), (0.35, 0.04), (0.28, 0.02), (0.40, 0.05)])
    uu = r.choice([18, 20, 22, 25])
    intro = r.choice([f'A doctor in {city(r)} measures the concentration of urea in a patient: renal artery {g(ua)} g/dm³, renal vein {g(uv)} g/dm³, urine {uu} g/dm³.',
                      f'Data from a healthy volunteer, {person(r)}: urea concentration in blood entering the kidney {g(ua)} g/dm³; blood leaving the kidney {g(uv)} g/dm³; urine {uu} g/dm³.'])
    parts = [
        lambda r: ('Calculate how many times more concentrated urea is in the urine than in the blood entering the kidney.', f'{g(uu / ua)} times', f'{uu} ÷ {g(ua)} [1] = {g(uu / ua)} [1] [2]'),
        lambda r: ('Explain why the urea concentration is lower in the renal vein than in the renal artery.', 'The kidney filters urea out of the blood and passes it into the urine.', 'urea filtered out [1]; into urine [1] [2]'),
        lambda r: ('Explain why urea is much more concentrated in urine than in blood.', 'Most of the water filtered is reabsorbed into the blood, but urea is not, so it becomes concentrated.', 'water reabsorbed [1]; urea left behind [1] [2]'),
        lambda r: ('State where urea is made and from what.', 'In the liver, from the breakdown of excess amino acids.', 'liver [1]; excess amino acids [1] [2]'),
        lambda r: ('Suggest what would happen to the urea concentration in the blood if both kidneys failed, and how this can be treated.', 'It would rise to toxic levels; treatment by dialysis (a machine filters the blood) or a kidney transplant.', 'urea rises / toxic [1]; dialysis or transplant [1] [2]'),
        lambda r: ('Name the tube that carries urine away from each kidney.', 'Ureter.', 'ureter [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t43.add('C4', (2, 3, 4, 5), 'multi_step')(_kid_c4)

N44 = 'Keeping a fetus healthy: placenta, nutrition and harmful substances'
t44 = topic(N44, N44.lower(), 'fetus', 'placenta')
FX(t44, 'C1', (1, 2), [
    ('What is the main function of the placenta?', 'Exchange of substances between the mother’s blood and the fetus’s blood', 'Oxygen and nutrients pass to the fetus; carbon dioxide and urea pass to the mother.',
     ['Making eggs', 'Producing milk', 'Protecting the fetus from knocks']),
    ('Which substance passes from the fetus to the mother across the placenta?', 'Carbon dioxide', 'Waste such as CO₂ and urea pass to the mother’s blood.', ['Oxygen', 'Glucose', 'Amino acids']),
    ('Which structure connects the fetus to the placenta?', 'The umbilical cord', 'The cord carries the fetus’s blood to and from the placenta.', ['The uterus wall', 'The cervix', 'The oviduct']),
    ('What is the function of the amniotic fluid?', 'It cushions and protects the fetus', 'The fluid-filled amniotic sac absorbs shocks.', ['It carries oxygen to the fetus', 'It digests food for the fetus', 'It removes urea']),
    ('Which harmful substance in cigarette smoke reduces the oxygen carried by the blood?', 'Carbon monoxide', 'CO binds to haemoglobin so less oxygen reaches the fetus.', ['Oxygen', 'Glucose', 'Nitrogen']),
    ('Which nutrient should a pregnant woman eat more of to help make the fetus’s blood?', 'Iron', 'Iron is needed for haemoglobin in red blood cells.', ['Fibre only', 'Salt', 'Caffeine']),
    ('Name two substances that pass from the mother to the fetus across the placenta.', 'Any two: oxygen, glucose, amino acids, water, minerals, vitamins (also alcohol, nicotine or some viruses).', 'any two [1] each [2]'),
])
FX(t44, 'C2', (1, 2, 3), [
    ('Explain why babies of mothers who smoke during pregnancy tend to have a lower birth mass.', 'Carbon monoxide reduces the oxygen carried in the mother’s blood and nicotine narrows blood vessels, so the fetus gets less oxygen and nutrients and grows less.', 'less oxygen (CO) [1]; less nutrient supply / narrowed vessels [1]; slower growth [1] [3]'),
    ('Explain why a pregnant woman is advised not to drink alcohol.', 'Alcohol crosses the placenta into the fetus’s blood and can damage the developing brain and organs.', 'crosses placenta [1]; damages development [1] [2]'),
    ('Explain how the placenta is adapted for exchange of substances.', 'It has a very large surface area (many villi), thin walls between the two blood supplies and a good blood supply, so diffusion is fast.', 'large surface area [1]; thin barrier / good blood supply [1] [2]'),
    ('Explain why it is important that the blood of the mother and fetus do not mix.', 'The mother’s blood pressure would damage the fetus’s vessels, the blood groups may differ, and the barrier stops many harmful pathogens and substances.', 'any two reasons [1] each [2]'),
    ('Explain why a pregnant woman needs extra calcium in her diet.', 'Calcium is needed to build the bones and teeth of the developing fetus.', 'calcium for bones / teeth [1]; of fetus [1] [2]'),
    ('Suggest why some medicines that are safe for adults can harm a fetus.', 'They can cross the placenta and affect cells that are dividing and developing rapidly into organs.', 'crosses placenta [1]; affects developing organs [1] [2]'),
])
misc(t44, 'C2', (2, 3, 4), [
    ('The placenta stops all harmful substances reaching the baby.', 'Many harmful substances such as alcohol, nicotine, some drugs and some viruses can cross the placenta.', 'not all blocked [1]; examples that cross [1] [2]'),
    ('A pregnant woman should eat for two, so she needs double the food.', 'She needs only a little more energy, but more of certain nutrients (protein, iron, calcium, folic acid); a balanced diet matters more than quantity.', 'only slightly more energy [1]; specific nutrients / balance [1] [2]'),
])


@t44.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t44_birth(r, D):
    base = r.choice([3.4, 3.45, 3.5, 3.55])
    drops = [0, r.choice([0.15, 0.18, 0.2]), r.choice([0.28, 0.3, 0.32]), r.choice([0.38, 0.4, 0.45])]
    cats = ['non-smokers', '1–9 cigarettes a day', '10–19 cigarettes a day', '20 or more cigarettes a day']
    ms = [round(base - d, 2) for d in drops]
    tab = '; '.join(f'{c}: {g(m, 3)} kg' for c, m in zip(cats, ms))
    s = f'A hospital in {city(r)} records the mean birth mass of babies grouped by how much their mothers smoked during pregnancy: {tab}.'
    diff = ms[0] - ms[3]
    if D <= 1:
        return mq(r, s + ' What pattern do the data show?', 'The more cigarettes smoked, the lower the mean birth mass', ['The more cigarettes smoked, the higher the mean birth mass', 'Smoking has no effect on birth mass', 'Only smoking 1–9 cigarettes affects birth mass'],
                  'Birth mass falls steadily as the number of cigarettes increases.')
    if D == 2:
        return Q(s + ' Calculate the difference in mean birth mass between babies of non-smokers and of mothers smoking 20 or more a day.', f'{g(diff, 3)} kg', f'{g(ms[0], 3)} − {g(ms[3], 3)} [1] = {g(diff, 3)} kg [1] [2]')
    pc = diff / ms[0] * 100
    s3 = s + ' (a) Calculate the percentage decrease in mean birth mass for mothers smoking 20 or more a day compared with non-smokers. (b) Explain how smoking causes this effect.'
    a = f'(a) {g(pc)}% (b) Carbon monoxide reduces the oxygen the blood carries and nicotine narrows blood vessels, so the fetus gets less oxygen and nutrients across the placenta.'
    k = f'(a) {g(diff, 3)} ÷ {g(ms[0], 3)} × 100 [1] = {g(pc)}% [1] (b) less oxygen / nutrients reach fetus [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k + '; CO or nicotine named [1] [4]', 'multi_step')
    return Q(s3 + ' (c) Suggest why these data alone do not prove that smoking causes lower birth mass.', a + ' (c) Other factors (diet, age, income, alcohol) may differ between the groups; a correlation does not prove cause.',
             k + '; CO or nicotine named [1] (c) other variables / correlation [1] [5]', 'multi_step')


def _fet_c4(r, D):
    c = city(r)
    intro = r.choice([f'A health clinic in {c} is preparing a leaflet for pregnant women about keeping the fetus healthy.', f'{person(r)}, who is pregnant, asks a nurse in {c} how her diet and lifestyle affect her baby.'])
    parts = [
        lambda r: ('Describe how the fetus obtains oxygen and nutrients.', 'They diffuse from the mother’s blood into the fetus’s blood in the placenta and are carried along the umbilical cord.', 'diffusion across placenta [1]; via umbilical cord [1] [2]'),
        lambda r: ('Explain why the leaflet should advise against smoking.', 'Carbon monoxide reduces oxygen supply and nicotine narrows blood vessels, so the baby may be small or born early.', 'CO / nicotine effect [1]; low birth mass / premature [1] [2]'),
        lambda r: ('Explain why the leaflet should advise eating foods rich in protein and iron.', 'Protein is needed to build new cells for growth; iron is needed to make haemoglobin for the fetus’s red blood cells.', 'protein for growth [1]; iron for haemoglobin [1] [2]'),
        lambda r: ('Name two substances other than nicotine that can cross the placenta and harm the fetus.', 'Any two: alcohol, carbon monoxide, some medicines or drugs, some viruses (e.g. rubella).', 'any two [1] each [2]'),
        lambda r: ('Explain how waste substances made by the fetus are removed.', 'Carbon dioxide and urea diffuse from the fetus’s blood into the mother’s blood in the placenta; the mother excretes them.', 'diffuse into mother’s blood [1]; excreted by mother’s lungs / kidneys [1] [2]'),
        lambda r: ('Suggest why advice on alcohol is “none at all” rather than “drink a little”.', 'No safe level is known; even small amounts reach the developing brain, so the safest advice is to avoid it completely.', 'no known safe level [1]; small amounts can harm developing organs [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t44.add('C4', (2, 3, 4, 5), 'multi_step')(_fet_c4)
t44.add('C3', (3, 4), 'multi_step')(_fet_c4)
CHAPTERS[4] = [t41, t42, t43, t44]

# =========================================================== 5 Reactivity
SERIES = ['potassium', 'sodium', 'calcium', 'magnesium', 'aluminium', 'zinc', 'iron', 'lead', 'copper', 'silver', 'gold']
RANK = {m: i for i, m in enumerate(SERIES)}
DMET = ['magnesium', 'zinc', 'iron', 'lead', 'copper']
SALTS = {'magnesium': 'magnesium sulfate', 'zinc': 'zinc sulfate', 'iron': 'iron sulfate', 'lead': 'lead nitrate', 'copper': 'copper sulfate', 'silver': 'silver nitrate'}
ANION = {'magnesium': 'sulfate', 'zinc': 'sulfate', 'iron': 'sulfate', 'lead': 'nitrate', 'copper': 'sulfate', 'silver': 'nitrate'}
LOOK = {'copper': 'a pink-brown coating of copper forms and the blue colour fades', 'silver': 'grey-silver crystals of silver form', 'lead': 'a grey coating of lead forms',
        'iron': 'a dark grey coating of iron forms and the pale green colour fades', 'zinc': 'a grey coating of zinc forms', 'magnesium': ''}


def disp(m, s):
    """metal m added to salt solution of metal s."""
    return RANK[m] < RANK[s]


def disp_eq(m, s):
    return f'{m} + {SALTS[s]} → {m} {ANION[s]} + {s}'


N51 = 'Reactivity and displacement reactions'
t51 = topic(N51, N51.lower(), 'displacement reactions')
FX(t51, 'C1', (1, 2), [
    ('What is a displacement reaction?', 'A more reactive metal takes the place of a less reactive metal in a compound', 'The more reactive metal pushes the less reactive one out of its compound.',
     ['A less reactive metal takes the place of a more reactive metal', 'A metal reacts with oxygen', 'Two metals melt together']),
    ('Which metal would displace copper from copper sulfate solution?', 'Zinc', 'Zinc is above copper in the reactivity series.', ['Silver', 'Gold', 'Copper']),
    ('An iron nail is placed in copper sulfate solution. What is seen?', 'A pink-brown coating forms on the nail', 'Iron displaces copper, which coats the nail; the blue colour fades.', ['Bubbles of oxygen form', 'The nail turns silver', 'Nothing happens']),
    ('Which pair would NOT react?', 'Copper and zinc sulfate solution', 'Copper is less reactive than zinc, so it cannot displace it.', ['Zinc and copper sulfate solution', 'Magnesium and iron sulfate solution', 'Iron and copper sulfate solution']),
    ('Which is the most reactive of these metals?', 'Magnesium', 'Order: magnesium > zinc > iron > copper.', ['Zinc', 'Iron', 'Copper']),
    ('Displacement reactions between metals and metal salt solutions are usually', 'exothermic', 'They release thermal energy; the temperature rises.', ['endothermic', 'neither exothermic nor endothermic', 'only possible at very high temperatures']),
    ('Write the word equation for the reaction between zinc and copper sulfate solution.', 'zinc + copper sulfate → zinc sulfate + copper', 'products zinc sulfate [1]; copper [1] [2]'),
])
FX(t51, 'C2', (1, 2, 3), [
    ('Explain why the blue colour of copper sulfate solution fades when magnesium is added.', 'Magnesium displaces the copper; blue copper ions are replaced by colourless magnesium ions in the solution.', 'magnesium displaces copper [1]; blue copper compound replaced by colourless magnesium sulfate [1] [2]'),
    ('Explain why silver does not react with copper sulfate solution.', 'Silver is less reactive than copper, so it cannot displace copper from its compound.', 'silver less reactive [1]; cannot displace [1] [2]'),
    ('Explain how displacement reactions can be used to place metals in order of reactivity.', 'Add each metal to solutions of salts of the others; the metal that displaces the most others is the most reactive.', 'test each metal with others’ salts [1]; more displacements = more reactive [1] [2]'),
    ('Explain why the temperature rise is larger when magnesium, rather than iron, is added to copper sulfate solution.', 'Magnesium is much further above copper than iron is, so the reaction is more vigorous and releases more energy.', 'magnesium more reactive [1]; bigger difference in reactivity / more energy released [1] [2]'),
    ('Explain why an iron container should not be used to store copper sulfate solution.', 'Iron is more reactive than copper, so it would displace copper and the container would corrode away.', 'iron displaces copper [1]; container damaged [1] [2]'),
])
misc(t51, 'C2', (2, 3, 4), [
    ('Copper will displace zinc from zinc sulfate because copper is a stronger metal.', 'Copper is less reactive than zinc, so no reaction occurs; zinc would displace copper instead.', 'copper less reactive [1]; no reaction [1] [2]'),
    ('In a displacement reaction the less reactive metal ends up in the solution.', 'The more reactive metal ends up in the compound (solution); the less reactive metal is pushed out as the element.', 'more reactive in compound [1]; less reactive metal released [1] [2]'),
])


@t51.add('C3', (1, 2, 3, 4, 5))
def t51_pred(r, D):
    m = r.choice(DMET)
    s = r.choice([x for x in SALTS if x != m])
    rx = disp(m, s)
    p = person(r)
    st = f'{p} adds a piece of {m} to {SALTS[s]} solution.'
    if D <= 1:
        return mq(r, st + ' What happens?', f'{m} displaces {s}' if rx else 'no reaction', [f'{m} displaces {s}', 'no reaction', f'{s} displaces {m}', 'hydrogen gas is produced'],
                  f'{cap(m)} is {"more" if rx else "less"} reactive than {s}.')
    if not rx:
        return Q(st + ' Predict whether a reaction occurs and explain your answer.', f'No reaction, because {m} is less reactive than {s}.', f'no reaction [1]; {m} below {s} in reactivity series [1] [2]', 'explain')
    if D == 2:
        return Q(st + ' Write the word equation for the reaction.', disp_eq(m, s), f'{m} {ANION[s]} [1]; {s} [1] [2]')
    a = f'Yes: {m} is more reactive than {s}. {disp_eq(m, s)}. Observation: {LOOK[s]}.'
    k = f'reaction occurs with reason [1]; word equation [1]; observation [1]'
    if D == 3:
        return Q(st + ' Predict whether a reaction occurs, explain why, write the word equation and describe what you would see.', a, k + ' [3]', 'multi_step')
    m2 = r.choice([x for x in DMET if x != m and x != s])
    rx2 = disp(m2, s)
    st4 = f'{p} adds {m} to one tube of {SALTS[s]} solution and {m2} to another. (a) For each tube, predict whether a reaction occurs and explain why. (b) Write a word equation for any reaction.'
    a4 = f'(a) {m}: reacts ({m} more reactive than {s}); {m2}: {"reacts" if rx2 else "no reaction"} ({m2} {"more" if rx2 else "less"} reactive than {s}). (b) {disp_eq(m, s)}' + (f'; {disp_eq(m2, s)}' if rx2 else '')
    k4 = '(a) each prediction with reason [1] [1] (b) word equation(s) [1]'
    if D == 4:
        return Q(st4 + ' (c) Describe one observation.', a4 + f' (c) {cap(LOOK[s])}.', k4 + ' (c) observation [1] [4]', 'multi_step')
    return Q(st4 + ' (c) Describe one observation. (d) Suggest which tube shows the larger temperature rise and why.', a4 + f' (c) {cap(LOOK[s])}. (d) The tube with the metal furthest above {s} in the series ({min([x for x in (m, m2) if disp(x, s)], key=lambda x: RANK[x])}), because the more vigorous reaction releases more energy.',
             k4 + ' (c) [1] (d) correct tube with reason [1] [5]', 'multi_step')


def _grid(r, mets):
    rows = []
    for m in mets:
        cells = []
        for s in mets:
            if s == m:
                cells.append('—')
            else:
                cells.append('✓' if disp(m, s) else '✗')
        rows.append(cells)
    return rows


def _disp_c4(r, D):
    mets = r.sample(['magnesium', 'zinc', 'iron', 'copper', 'lead'], 3) + ['silver'] if r.random() < 0.3 else r.sample(['magnesium', 'zinc', 'iron', 'copper', 'lead'], 4)
    mets = mets[:4]
    letters = 'WXYZ'
    lab = dict(zip(mets, letters))
    rows = _grid(r, mets)
    desc = '; '.join(f'metal {lab[m]} displaced ' + (', '.join(lab[s] for s in mets if s != m and disp(m, s)) or 'none of the others') for m in mets)
    order = ' > '.join(lab[m] for m in sorted(mets, key=lambda x: RANK[x]))
    intro = r.choice([f'{person(r)} adds four metals, W, X, Y and Z, to solutions of each other’s salts. Results: {desc}.', f'A student in {city(r)} tests four unknown metals W, X, Y and Z with solutions of each other’s nitrates. Results: {desc}.'])
    top = sorted(mets, key=lambda x: RANK[x])
    parts = [
        lambda r: ('Put the metals in order of reactivity, most reactive first.', order, f'{order} [2]'),
        lambda r: ('Explain how you used the results to decide the order.', 'The metal that displaced the most others is the most reactive; the one that displaced none is the least reactive.', 'number of displacements [1]; most / none linked to order [1] [2]'),
        lambda r: (f'The metals are {", ".join(sorted(mets))}. Suggest which letter is which metal.', '; '.join(f'{lab[m]} = {m}' for m in mets), 'all correct [2]; two correct [1] [2]'),
        lambda r: ('Explain why the experiment does not need a test of each metal with its own salt.', 'A metal cannot displace itself, so there would be no reaction and no information.', 'no reaction with own salt [1]'),
        lambda r: ('Suggest one other observation, apart from a coating forming, that shows a reaction has happened.', 'A temperature rise, or a change in the colour of the solution.', 'temperature rise / colour change [1]'),
        lambda r: (f'Predict whether {top[-1]} would react with a solution of a {top[0]} salt.', f'No: {top[-1]} is less reactive than {top[0]}.', 'no reaction [1]; reason [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t51.add('C4', (2, 3, 4, 5), 'multi_step')(_disp_c4)

N52 = 'Using the reactivity series to predict reactions'
t52 = topic(N52, N52.lower(), 'reactivity series', 'predict reactions')
FX(t52, 'C1', (1, 2), [
    ('Which metal reacts most vigorously with cold water?', 'Potassium', 'Potassium is at the top of the reactivity series.', ['Calcium', 'Magnesium', 'Copper']),
    ('Which metal does not react with dilute hydrochloric acid?', 'Copper', 'Copper is below hydrogen in the reactivity series.', ['Zinc', 'Magnesium', 'Iron']),
    ('Which metal is found uncombined (native) in the Earth’s crust?', 'Gold', 'Gold is so unreactive that it is found as the element.', ['Sodium', 'Magnesium', 'Aluminium']),
    ('Which gas is given off when a metal reacts with dilute acid?', 'Hydrogen', 'metal + acid → salt + hydrogen.', ['Oxygen', 'Carbon dioxide', 'Chlorine']),
    ('Which list is in order of decreasing reactivity?', 'magnesium, zinc, iron, copper', 'Mg > Zn > Fe > Cu.', ['copper, iron, zinc, magnesium', 'zinc, magnesium, copper, iron', 'iron, copper, magnesium, zinc']),
    ('Which metal reacts with cold water to form an alkaline solution and hydrogen?', 'Sodium', 'Na + water → sodium hydroxide + hydrogen.', ['Copper', 'Silver', 'Gold']),
    ('Name two metals that are less reactive than iron.', 'Any two: lead, copper, silver, gold.', 'any two [1] each [2]'),
])
FX(t52, 'C2', (1, 2, 3), [
    ('Explain why gold is used for jewellery that is worn every day.', 'Gold is very unreactive, so it does not corrode or tarnish when in contact with air, water or sweat.', 'unreactive [1]; does not corrode / tarnish [1] [2]'),
    ('Explain why copper is used for water pipes but sodium could never be.', 'Copper does not react with water; sodium reacts vigorously with water, producing hydrogen and an alkali.', 'copper unreactive with water [1]; sodium reacts violently [1] [2]'),
    ('Explain why magnesium fizzes faster than zinc in the same dilute acid.', 'Magnesium is more reactive than zinc, so it reacts faster and gives off hydrogen faster.', 'magnesium more reactive [1]; hydrogen produced faster [1] [2]'),
    ('Explain how the reactivity series can be used to predict whether a metal reacts with dilute acid.', 'Metals above hydrogen in the series react with dilute acid to give hydrogen; those below hydrogen (copper, silver, gold) do not.', 'above hydrogen react [1]; below do not [1] [2]'),
    ('Suggest why the most reactive metals were discovered much later in history than gold and copper.', 'Reactive metals are always found in compounds and are hard to extract; unreactive metals are found native or extracted easily.', 'reactive metals in compounds [1]; hard to extract [1] [2]'),
])
misc(t52, 'C2', (2, 3, 4), [
    ('All metals react with dilute acids to make hydrogen.', 'Only metals above hydrogen in the reactivity series do; copper, silver and gold do not react with dilute acids.', 'not all [1]; Cu / Ag / Au do not react [1] [2]'),
    ('Aluminium must be very unreactive because it does not corrode.', 'Aluminium is quite reactive; a thin layer of aluminium oxide forms on its surface and protects it from further reaction.', 'aluminium fairly reactive [1]; protective oxide layer [1] [2]'),
])
ACIDMET = ['magnesium', 'zinc', 'iron', 'copper', 'calcium', 'lead', 'silver']
OBS_ACID = {'calcium': 'very rapid fizzing', 'magnesium': 'rapid fizzing', 'zinc': 'steady fizzing', 'iron': 'slow fizzing', 'lead': 'very slow (hardly any) bubbles', 'copper': 'no reaction', 'silver': 'no reaction'}


@t52.add('C3', (1, 2, 3, 4, 5))
def t52_temp(r, D):
    mets = r.sample(['magnesium', 'zinc', 'iron', 'lead'], 3)
    base = {'magnesium': r.choice([34, 38, 42]), 'zinc': r.choice([18, 20, 22]), 'iron': r.choice([9, 10, 12]), 'lead': r.choice([3, 4])}
    T0 = r.choice([19, 20, 21, 22])
    letters = 'ABC'
    lab = dict(zip(mets, letters))
    sh = mets[:]
    r.shuffle(sh)
    tab = ', '.join(f'metal {lab[m]}: {T0} °C → {T0 + base[m]} °C' for m in sh)
    s = f'{person(r)} adds equal masses of powdered metals A, B and C to separate 25 cm³ portions of copper sulfate solution and records the temperature: {tab}.'
    order = sorted(mets, key=lambda m: -base[m])
    if D <= 1:
        return mq(r, s + ' Which metal is the most reactive?', f'metal {lab[order[0]]}', ['metal A', 'metal B', 'metal C', 'they are equally reactive'], f'Largest temperature rise ({base[order[0]]} °C) = most reactive.')
    if D == 2:
        return Q(s + ' Calculate the temperature rise for each metal and put the metals in order of reactivity.', ', '.join(f'{lab[m]} {base[m]} °C' for m in sh) + '; order ' + ' > '.join(lab[m] for m in order),
                 'temperature rises [1]; order (largest rise = most reactive) [1] [2]')
    s3 = s + f' (a) Put the metals in order of reactivity. (b) Explain why a larger temperature rise shows a more reactive metal. (c) The metals are {", ".join(sorted(mets))}. Identify A, B and C.'
    a = '(a) ' + ' > '.join(lab[m] for m in order) + ' (b) A more reactive metal reacts more vigorously with copper sulfate and releases more thermal energy (exothermic). (c) ' + '; '.join(f'{lab[m]} = {m}' for m in mets)
    k = '(a) order [1] (b) more vigorous / more energy released [1] (c) all identified [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) State two variables that must be kept the same.', a + ' (d) Mass and particle size of metal, volume and concentration of copper sulfate solution (any two).', k + ' (d) two variables [1] [4]', 'multi_step')
    return Q(s3 + ' (d) State two variables that must be kept the same. (e) Predict the temperature change if silver powder were used, and explain.', a + ' (d) Mass of metal, volume and concentration of solution. (e) No change: silver is less reactive than copper, so no reaction.',
             k + ' (d) [1] (e) no change with reason [1] [5]', 'multi_step')


@t52.add('C2', (1, 2, 3, 4))
def t52_acid(r, D):
    a, b = r.sample(ACIDMET, 2)
    acid = r.choice(['dilute hydrochloric acid', 'dilute sulfuric acid'])
    s = f'Pieces of {a} and {b} of the same size are added to separate test tubes of {acid}.'
    if D <= 1:
        more = a if RANK[a] < RANK[b] else b
        return mq(r, s + ' Which metal reacts faster?', more, [a, b, 'both react at the same rate', 'neither reacts'], f'{cap(more)} is higher in the reactivity series.')
    return Q(s + ' Predict what you would see in each tube and explain your predictions.', f'{cap(a)}: {OBS_ACID[a]}; {b}: {OBS_ACID[b]}. The higher a metal is in the reactivity series, the faster it reacts with acid; metals below hydrogen do not react.',
             f'{a} observation [1]; {b} observation [1]' + ('; reason using reactivity series [1] [3]' if D >= 3 else ' [2]'), 'explain')


def _pred_c4(r, D):
    m = r.choice(['zinc', 'iron', 'magnesium'])
    c = city(r)
    intro = r.choice([f'A factory in {c} wants to store a solution of copper sulfate and also coat steel with {m} to protect it.', f'An engineer in {c} is choosing metals for different jobs using the reactivity series: potassium, sodium, calcium, magnesium, aluminium, zinc, iron, lead, copper, silver, gold.'])
    parts = [
        lambda r: ('Explain why the copper sulfate solution must not be stored in a tank made of iron.', 'Iron is more reactive than copper, so it would displace copper and the tank would be eaten away.', 'iron more reactive [1]; displaces copper / tank corrodes [1] [2]'),
        lambda r: ('Suggest a metal from the series that could safely be used to line the tank, and explain your choice.', 'Silver or gold (or copper itself), because they are not more reactive than copper so no displacement occurs.', 'suitable metal [1]; reason [1] [2]'),
        lambda r: (f'Predict how {m} reacts with dilute hydrochloric acid, and write the word equation.', f'It fizzes, giving off hydrogen. {m} + hydrochloric acid → {m} chloride + hydrogen', 'fizzing / hydrogen [1]; word equation [1] [2]'),
        lambda r: ('Explain why potassium must never be used in contact with water.', 'It is at the top of the series and reacts violently with water, producing hydrogen that can ignite.', 'very reactive [1]; violent reaction / hydrogen [1] [2]'),
        lambda r: ('Explain why gold is used for electrical contacts in computers even though it is expensive.', 'It is very unreactive, so it does not corrode and keeps a good electrical contact.', 'unreactive / no corrosion [1]; reliable contact [1] [2]'),
        lambda r: (f'Explain whether {m} would displace lead from lead nitrate solution.', f'Yes: {m} is above lead in the reactivity series.', 'yes [1]; reason [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t52.add('C4', (2, 3, 4, 5), 'multi_step')(_pred_c4)
t52.add('C3', (3, 4), 'multi_step')(_pred_c4)

ACIDS = {'hydrochloric acid': 'chloride', 'sulfuric acid': 'sulfate', 'nitric acid': 'nitrate'}
SMET = ['magnesium', 'zinc', 'iron', 'calcium']
BASES = [('copper oxide', 'copper'), ('magnesium oxide', 'magnesium'), ('zinc oxide', 'zinc'), ('sodium hydroxide', 'sodium'), ('potassium hydroxide', 'potassium'), ('calcium hydroxide', 'calcium')]

N53 = 'Salts: making salts from acids and metals or bases'
t53 = topic(N53, N53.lower(), 'salts', 'acids and metals or bases')
FX(t53, 'C1', (1, 2), [
    ('What is a salt?', 'A compound formed when the hydrogen of an acid is replaced by a metal', 'Salts form when acids react with metals, bases or carbonates.', ['Any compound that dissolves in water', 'A compound that contains only non-metals', 'An acid mixed with water']),
    ('Which salt is formed when zinc reacts with sulfuric acid?', 'Zinc sulfate', 'Sulfuric acid gives sulfates.', ['Zinc chloride', 'Zinc nitrate', 'Zinc oxide']),
    ('Which acid is used to make chloride salts?', 'Hydrochloric acid', 'Hydrochloric → chloride; sulfuric → sulfate; nitric → nitrate.', ['Sulfuric acid', 'Nitric acid', 'Citric acid']),
    ('What are the products when a metal oxide reacts with an acid?', 'A salt and water', 'base + acid → salt + water (neutralisation).', ['A salt and hydrogen', 'A salt, water and carbon dioxide', 'An alkali and oxygen']),
    ('What are the products when magnesium reacts with hydrochloric acid?', 'Magnesium chloride and hydrogen', 'metal + acid → salt + hydrogen.', ['Magnesium chloride and water', 'Magnesium oxide and hydrogen', 'Magnesium chloride and carbon dioxide']),
    ('Which is the test for hydrogen gas?', 'A lighted splint gives a squeaky pop', 'Hydrogen burns with a squeaky pop.', ['A glowing splint relights', 'Limewater turns milky', 'Damp litmus paper is bleached']),
    ('A base that dissolves in water is called', 'an alkali', 'Soluble bases (e.g. sodium hydroxide) are alkalis.', ['an acid', 'a salt', 'an indicator']),
    ('Name the salt formed when copper oxide reacts with sulfuric acid.', 'Copper sulfate.', 'copper sulfate [1]'),
])
FX(t53, 'C2', (1, 2, 3), [
    ('Explain why copper sulfate cannot be made by adding copper metal to dilute sulfuric acid.', 'Copper is below hydrogen in the reactivity series, so it does not react with dilute acids; copper oxide must be used instead.', 'copper does not react with dilute acid [1]; use copper oxide / carbonate [1] [2]'),
    ('Explain why the reaction between an acid and a base is called neutralisation.', 'The base cancels out the acid: the H⁺ ions of the acid react to form water, so the solution becomes neutral (pH 7).', 'acid cancelled / water formed [1]; pH moves to 7 [1] [2]'),
    ('Explain why potassium is not used to make potassium chloride from hydrochloric acid in a school laboratory.', 'Potassium is so reactive that it reacts violently (explosively) with acid; potassium hydroxide is used instead.', 'violent reaction [1]; use the hydroxide instead [1] [2]'),
    ('Explain how you know when all the acid has reacted when making a salt from magnesium and acid.', 'Fizzing stops and some magnesium is left unreacted (excess) at the bottom.', 'fizzing stops [1]; excess metal remains [1] [2]'),
    ('Describe how to show that a solution of sodium chloride made by neutralisation is neutral.', 'Add a few drops of universal indicator; it should turn green (pH 7). Or use a pH meter.', 'universal indicator / pH meter [1]; green / pH 7 [1] [2]'),
])
misc(t53, 'C2', (2, 3, 4), [
    ('Metal oxides react with acids to give a salt and hydrogen.', 'Metal oxides (bases) react with acids to give a salt and water; hydrogen is made only when a metal reacts with an acid.', 'base + acid → salt + water [1]; hydrogen from metal + acid [1] [2]'),
    ('Salt just means sodium chloride.', 'A salt is any compound in which the hydrogen of an acid is replaced by a metal, e.g. copper sulfate, potassium nitrate.', 'general definition [1]; another example [1] [2]'),
])


@t53.add('C3', (1, 2, 3, 4, 5))
def t53_name(r, D):
    acid = r.choice(list(ACIDS))
    kind = r.choice(['metal', 'base'])
    if kind == 'metal':
        acid = r.choice(['hydrochloric acid', 'sulfuric acid'])
        m = r.choice(SMET)
        reac = m
        salt = f'{m} {ACIDS[acid]}'
        other = 'hydrogen'
    else:
        reac, m = r.choice(BASES)
        salt = f'{m} {ACIDS[acid]}'
        other = 'water'
    eq = f'{reac} + {acid} → {salt} + {other}'
    if D <= 1:
        wrong = [f'{m} {x}' for x in ACIDS.values() if x != ACIDS[acid]] + [f'{m} oxide', f'{m} hydroxide']
        return mq(r, f'Which salt is formed when {reac} reacts with {acid}?', salt, [w for w in wrong if w != reac], f'{cap(acid)} forms {ACIDS[acid]}s: {eq}.')
    if D == 2:
        return Q(f'Write the word equation for the reaction between {reac} and {acid}.', eq, f'{salt} [1]; {other} [1] [2]')
    s = f'{person(r)} reacts {reac} with {acid}.'
    if D == 3:
        return Q(s + ' (a) Write the word equation. (b) Describe what you would see. (c) State the type of reaction.',
                 f'(a) {eq} (b) ' + ('fizzing (bubbles of hydrogen) and the metal gets smaller' if kind == 'metal' else ('the black solid dissolves and the solution turns blue' if 'copper' in reac else 'the solid dissolves to give a colourless solution' if 'oxide' in reac else 'no visible change; the temperature rises')) + f' (c) {"reaction of a metal with an acid, giving a salt and hydrogen" if kind == "metal" else "neutralisation"}',
                 '(a) word equation [1] (b) observation [1] (c) type [1] [3]', 'multi_step')
    s4 = s + f' (a) Write the word equation. (b) {"Describe the test for the gas produced." if kind == "metal" else "Explain why this is a neutralisation reaction."} (c) Name the acid needed to make {m} nitrate instead, and explain why the method might need to change.'
    a = f'(a) {eq} (b) ' + ('lighted splint → squeaky pop (hydrogen)' if kind == 'metal' else 'the base reacts with the acid to form a salt and water, cancelling the acidity (pH towards 7)') + \
        f' (c) Nitric acid; ' + ('nitric acid reacts with metals in other ways (not giving hydrogen), so use the oxide or carbonate instead.' if kind == 'metal' else 'the same method works because the base reacts with any acid to give a salt and water.')
    k = '(a) equation [2] (b) [1] (c) nitric acid with comment [1]'
    if D == 4:
        return Q(s4, a, k + ' [4]', 'multi_step')
    return Q(s4 + ' (d) Suggest how to obtain a dry sample of the salt from its solution.', a + ' (d) Heat the solution to evaporate some water, leave it to cool and crystallise, then filter and dry the crystals.', k + ' (d) evaporate / crystallise [1] [5]', 'multi_step')


def _salt_c4(r, D):
    m = r.choice(['magnesium', 'zinc', 'iron'])
    acid = r.choice(['hydrochloric acid', 'sulfuric acid'])
    salt = f'{m} {ACIDS[acid]}'
    ms = r.choice([0.5, 1.0, 1.2, 1.5, 2.0])
    left = round(ms * r.choice([0.1, 0.2, 0.25]), 2)
    intro = r.choice([f'{person(r)} adds {g(ms)} g of {m} to 50 cm³ of {acid} until the fizzing stops. {g(left)} g of {m} is left unreacted.',
                      f'A class in {city(r)} makes {salt} by adding {m} to {acid} in excess. They start with {g(ms)} g of metal and {g(left)} g remains at the end.'])
    parts = [
        lambda r: ('Write the word equation for the reaction.', f'{m} + {acid} → {salt} + hydrogen', f'{salt} [1]; hydrogen [1] [2]'),
        lambda r: ('Calculate the mass of metal that reacted.', f'{g(ms - left)} g', f'{g(ms)} − {g(left)} = {g(ms - left)} g [1]'),
        lambda r: ('Explain why excess metal is used.', 'To make sure all the acid reacts, so the salt solution contains no leftover acid.', 'all acid used up [1]; pure salt solution [1] [2]'),
        lambda r: ('Describe how to remove the unreacted metal.', 'Filter the mixture; the metal stays on the filter paper and the salt solution passes through as the filtrate.', 'filtration [1]; metal residue, salt in filtrate [1] [2]'),
        lambda r: ('Describe the test for the gas given off and the result.', 'Hold a lighted splint at the mouth of the tube: a squeaky pop shows hydrogen.', 'lighted splint [1]; squeaky pop [1] [2]'),
        lambda r: ('Describe how to get crystals of the salt from the filtrate.', 'Heat to evaporate some water until crystals start to form, leave to cool so crystals grow, then filter and dry them between filter papers.', 'evaporate some water [1]; cool to crystallise and dry [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t53.add('C4', (2, 3, 4, 5), 'multi_step')(_salt_c4)

CARB = [('calcium carbonate', 'calcium'), ('copper carbonate', 'copper'), ('magnesium carbonate', 'magnesium'), ('zinc carbonate', 'zinc'), ('sodium carbonate', 'sodium')]
N54 = 'Other ways of making salts: acids and carbonates, and preparing a pure salt'
t54 = topic(N54, N54.lower(), 'acids and carbonates', 'preparing a pure salt')
FX(t54, 'C1', (1, 2), [
    ('What are the products when a metal carbonate reacts with an acid?', 'A salt, water and carbon dioxide', 'carbonate + acid → salt + water + carbon dioxide.', ['A salt and hydrogen', 'A salt and water only', 'A metal oxide and hydrogen']),
    ('Which is the test for carbon dioxide?', 'It turns limewater milky', 'CO₂ bubbled through limewater gives a white (milky) precipitate.', ['It gives a squeaky pop with a lighted splint', 'It relights a glowing splint', 'It bleaches damp litmus paper']),
    ('Why is excess copper carbonate added when making copper sulfate?', 'To make sure all the acid is used up', 'Excess solid guarantees no acid is left; the excess is then filtered off.', ['To make the crystals bigger', 'To produce more carbon dioxide gas', 'To make the solution acidic']),
    ('Which method removes excess solid from a salt solution?', 'Filtration', 'The insoluble excess stays on the filter paper.', ['Evaporation', 'Chromatography', 'Distillation']),
    ('Why is the filtrate only partly evaporated before it is left to crystallise?', 'So that larger, well-formed crystals grow as it cools slowly', 'Evaporating to dryness gives a powder and can decompose some salts.', ['To remove all the water at once', 'To make the salt react again', 'To make more carbon dioxide']),
    ('What would you see when zinc carbonate is added to hydrochloric acid?', 'Fizzing as the solid dissolves', 'Carbon dioxide bubbles form and the carbonate reacts.', ['A squeaky pop', 'A pink coating', 'No change']),
    ('Write the word equation for the reaction between calcium carbonate and hydrochloric acid.', 'calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide', 'calcium chloride [1]; water and carbon dioxide [1] [2]'),
])
FX(t54, 'C2', (1, 2, 3), [
    ('Explain why the mass of a flask containing marble chips and acid decreases during the reaction.', 'Carbon dioxide gas is produced and escapes from the open flask, so mass is lost.', 'carbon dioxide produced [1]; gas escapes [1] [2]'),
    ('Explain how you can tell when enough copper carbonate has been added to the acid.', 'No more fizzing occurs and some green solid remains undissolved (in excess).', 'fizzing stops [1]; solid left over [1] [2]'),
    ('Explain why the acid is warmed before the copper oxide is added when making copper sulfate.', 'Warming speeds up the reaction so the base reacts and dissolves faster.', 'faster reaction [1]; base dissolves more quickly [1] [2]'),
    ('Explain why the crystals are dried between filter papers rather than in a hot oven.', 'Some salts contain water of crystallisation or decompose when heated strongly, so gentle drying keeps the crystals intact.', 'heat can damage / decompose crystals [1]; gentle drying [1] [2]'),
    ('Suggest why antacid tablets often contain magnesium carbonate.', 'It neutralises excess hydrochloric acid in the stomach, producing a salt, water and carbon dioxide.', 'neutralises stomach acid [1]; products named [1] [2]'),
])
misc(t54, 'C2', (2, 3, 4), [
    ('When marble reacts with acid the mass decreases, so mass is destroyed in the reaction.', 'Mass is conserved; the missing mass is carbon dioxide gas that escapes into the air.', 'mass conserved [1]; CO₂ escapes [1] [2]'),
    ('To get crystals of copper sulfate you should boil the solution until it is completely dry.', 'Evaporate only part of the water, then let the solution cool slowly so crystals form; boiling to dryness gives powder and can decompose the salt.', 'partial evaporation then cooling [1]; reason [1] [2]'),
])
STEPS = ['Warm some dilute sulfuric acid in a beaker', 'Add copper carbonate a little at a time, stirring, until no more fizzes and some solid remains', 'Filter to remove the excess copper carbonate',
         'Heat the filtrate to evaporate about half of the water', 'Leave the solution to cool so that crystals form', 'Filter off the crystals and dry them between filter papers']


@t54.add('C3', (1, 2, 3, 4, 5))
def t54_name(r, D):
    carb, m = r.choice(CARB)
    acid = r.choice(list(ACIDS))
    if carb == 'calcium carbonate' and acid == 'sulfuric acid':
        acid = 'hydrochloric acid'
    salt = f'{m} {ACIDS[acid]}'
    eq = f'{carb} + {acid} → {salt} + water + carbon dioxide'
    if D <= 1:
        return mq(r, f'Which products form when {carb} reacts with {acid}?', f'{salt}, water and carbon dioxide', [f'{salt} and hydrogen', f'{salt} and water only', f'{m} oxide and carbon dioxide', f'{m} and carbon dioxide'], eq + '.')
    if D == 2:
        return Q(f'Write the word equation for the reaction between {carb} and {acid}.', eq, f'{salt} [1]; water and carbon dioxide [1] [2]')
    mc = r.choice([2.0, 2.5, 4.0, 5.0, 10.0])
    loss = round(mc * {'calcium': 0.44, 'copper': 0.356, 'magnesium': 0.524, 'zinc': 0.352, 'sodium': 0.415}[m], 2)
    m0 = r.choice([98.4, 105.2, 112.6, 120.3])
    s = f'{person(r)} puts a flask of {acid} on a balance (total mass {m0:.2f} g) and adds {mc:.2f} g of {carb} (the acid is in excess). When the reaction has finished the reading is {m0 + mc - loss:.2f} g.'
    s3 = s + ' (a) Write the word equation. (b) Calculate the mass of carbon dioxide given off. (c) Describe a test to show the gas is carbon dioxide.'
    a = f'(a) {eq} (b) {m0 + mc:.2f} − {m0 + mc - loss:.2f} = {loss:.2f} g (c) Bubble the gas through limewater: it turns milky.'
    k = f'(a) equation [1] (b) {loss:.2f} g [1] (c) limewater turns milky [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Explain why the total mass of all the products is the same as the total mass of the reactants.', a + ' (d) Atoms are not created or destroyed, only rearranged (conservation of mass); the balance reading falls only because the gas escapes.',
                 k + ' (d) conservation of mass / gas escapes [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Explain why the total mass of the products equals the mass of the reactants. (e) Suggest how the experiment could be changed so that the balance reading does not change.', a + ' (d) Atoms are only rearranged; mass is conserved but the gas escapes. (e) Carry out the reaction in a sealed container (or with a balloon over the flask) so the gas cannot escape.',
             k + ' (d) [1] (e) sealed system [1] [5]', 'multi_step')


@t54.add('C2', (1, 2, 3, 4))
def t54_order(r, D):
    idx = list(range(6))
    sh = idx[:]
    while sh == idx:
        r.shuffle(sh)
    lettered = '; '.join(f'{"ABCDEF"[i]}: {STEPS[j]}' for i, j in enumerate(sh))
    correct = ''.join("ABCDEF"[sh.index(j)] for j in idx)
    s = f'The steps for making pure copper sulfate crystals from copper carbonate are given in the wrong order. {lettered}.'
    if D <= 1:
        wrong = set()
        while len(wrong) < 3:
            w = list(correct)
            i, j = r.sample(range(6), 2)
            w[i], w[j] = w[j], w[i]
            if ''.join(w) != correct:
                wrong.add(''.join(w))
        return mq(r, s + ' Which is the correct order?', correct, sorted(wrong), 'Warm acid → add excess carbonate → filter → evaporate partly → cool to crystallise → filter and dry.')
    return Q(s + (' Put the steps in the correct order.' if D == 2 else ' Put the steps in the correct order and explain why the excess copper carbonate is filtered off before evaporating.'),
             correct + ('' if D == 2 else '. Filtering removes the unreacted solid so the crystals are pure copper sulfate.'), 'correct order [2]; one pair swapped [1]' + (' [2]' if D == 2 else '; filtering removes excess so crystals are pure [1] [3]'), 'explain')


def _pure_c4(r, D):
    base = r.choice([('copper oxide', 'copper', 'black', 'blue'), ('copper carbonate', 'copper', 'green', 'blue'), ('zinc oxide', 'zinc', 'white', 'colourless'), ('magnesium carbonate', 'magnesium', 'white', 'colourless')])
    acid = r.choice(['sulfuric acid', 'hydrochloric acid'])
    salt = f'{base[1]} {ACIDS[acid]}'
    exp = r.choice([4.0, 5.0, 6.0, 8.0, 10.0])
    got = round(exp * r.choice([0.6, 0.7, 0.75, 0.8, 0.85]), 1)
    intro = r.choice([f'{person(r)} makes crystals of {salt} from {base[0]} (a {base[2]} solid) and dilute {acid}. The expected mass of crystals is {g(exp)} g but only {g(got)} g are collected.',
                      f'A school laboratory in {city(r)} prepares {salt} by reacting {base[0]} with {acid}. From the quantities used, {g(exp)} g of salt should form; the class obtains {g(got)} g.'])
    isc = 'carbonate' in base[0]
    parts = [
        lambda r: ('Write the word equation for the reaction.', f'{base[0]} + {acid} → {salt} + water' + (' + carbon dioxide' if isc else ''), 'salt [1]; other product(s) [1] [2]'),
        lambda r: (f'Describe the colour change of the mixture as the {base[0]} reacts.', f'The {base[2]} solid disappears and the solution becomes {base[3]}.', 'solid disappears [1]; solution colour [1] [2]'),
        lambda r: ('Describe how to make sure that all of the acid has reacted.', f'Add {base[0]} in small portions with stirring until some solid remains undissolved' + (' and no more fizzing occurs.' if isc else '.'), 'add in excess [1]; solid remains / fizzing stops [1] [2]'),
        lambda r: ('Calculate the percentage yield.', f'{g(got / exp * 100)}%', f'{g(got)} ÷ {g(exp)} × 100 [1] = {g(got / exp * 100)}% [1] [2]'),
        lambda r: ('Suggest two reasons why the mass of crystals is less than expected.', 'Some solution left on the filter paper or in the beaker; not all the salt crystallised (some stays in solution); some crystals lost when transferring.', 'any two [1] each [2]'),
        lambda r: ('Explain why the solution is filtered before it is evaporated.', f'To remove the excess unreacted {base[0]}, so the crystals are pure.', 'removes excess solid [1]; pure product [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t54.add('C4', (2, 3, 4, 5), 'multi_step')(_pure_c4)
t54.add('C3', (3, 4), 'multi_step')(_pure_c4)

AR = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'Na': 23, 'Mg': 24, 'S': 32, 'Cl': 35.5, 'K': 39, 'Ca': 40, 'Fe': 56, 'Cu': 64, 'Zn': 65, 'Br': 80}


def atoms(f):
    """Count atoms in a formula such as Ca(OH)2 or H2SO4."""
    import re as _re
    def parse(s, i=0):
        cnt = {}
        while i < len(s):
            if s[i] == '(':
                sub, i = parse(s, i + 1)
                m = _re.match(r'\d+', s[i:])
                k = int(m.group()) if m else 1
                i += len(m.group()) if m else 0
                for e, n in sub.items():
                    cnt[e] = cnt.get(e, 0) + n * k
            elif s[i] == ')':
                return cnt, i + 1
            else:
                m = _re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
                e, n = m.group(1), int(m.group(2) or 1)
                cnt[e] = cnt.get(e, 0) + n
                i += len(m.group())
        return cnt, i
    return parse(f)[0]


def Mr(f):
    return sum(AR[e] * n for e, n in atoms(f).items())


EQS = [
    ('magnesium + hydrochloric acid → magnesium chloride + hydrogen', [(1, 'Mg'), (2, 'HCl')], [(1, 'MgCl2'), (1, 'H2')]),
    ('magnesium + oxygen → magnesium oxide', [(2, 'Mg'), (1, 'O2')], [(2, 'MgO')]),
    ('methane + oxygen → carbon dioxide + water', [(1, 'CH4'), (2, 'O2')], [(1, 'CO2'), (2, 'H2O')]),
    ('hydrogen + oxygen → water', [(2, 'H2'), (1, 'O2')], [(2, 'H2O')]),
    ('calcium carbonate → calcium oxide + carbon dioxide', [(1, 'CaCO3')], [(1, 'CaO'), (1, 'CO2')]),
    ('zinc + sulfuric acid → zinc sulfate + hydrogen', [(1, 'Zn'), (1, 'H2SO4')], [(1, 'ZnSO4'), (1, 'H2')]),
    ('copper oxide + sulfuric acid → copper sulfate + water', [(1, 'CuO'), (1, 'H2SO4')], [(1, 'CuSO4'), (1, 'H2O')]),
    ('sodium hydroxide + hydrochloric acid → sodium chloride + water', [(1, 'NaOH'), (1, 'HCl')], [(1, 'NaCl'), (1, 'H2O')]),
    ('calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide', [(1, 'CaCO3'), (2, 'HCl')], [(1, 'CaCl2'), (1, 'H2O'), (1, 'CO2')]),
    ('sodium + chlorine → sodium chloride', [(2, 'Na'), (1, 'Cl2')], [(2, 'NaCl')]),
    ('sodium + oxygen → sodium oxide', [(4, 'Na'), (1, 'O2')], [(2, 'Na2O')]),
    ('iron + copper sulfate → iron sulfate + copper', [(1, 'Fe'), (1, 'CuSO4')], [(1, 'FeSO4'), (1, 'Cu')]),
    ('sodium + water → sodium hydroxide + hydrogen', [(2, 'Na'), (2, 'H2O')], [(2, 'NaOH'), (1, 'H2')]),
    ('carbon + oxygen → carbon dioxide', [(1, 'C'), (1, 'O2')], [(1, 'CO2')]),
    ('copper + oxygen → copper oxide', [(2, 'Cu'), (1, 'O2')], [(2, 'CuO')]),
    ('calcium + oxygen → calcium oxide', [(2, 'Ca'), (1, 'O2')], [(2, 'CaO')]),
    ('calcium + water → calcium hydroxide + hydrogen', [(1, 'Ca'), (2, 'H2O')], [(1, 'Ca(OH)2'), (1, 'H2')]),
    ('nitrogen + hydrogen → ammonia', [(1, 'N2'), (3, 'H2')], [(2, 'NH3')]),
    ('chlorine + potassium bromide → potassium chloride + bromine', [(1, 'Cl2'), (2, 'KBr')], [(2, 'KCl'), (1, 'Br2')]),
    ('hydrogen peroxide → water + oxygen', [(2, 'H2O2')], [(2, 'H2O'), (1, 'O2')]),
    ('zinc + hydrochloric acid → zinc chloride + hydrogen', [(1, 'Zn'), (2, 'HCl')], [(1, 'ZnCl2'), (1, 'H2')]),
    ('magnesium oxide + hydrochloric acid → magnesium chloride + water', [(1, 'MgO'), (2, 'HCl')], [(1, 'MgCl2'), (1, 'H2O')]),
    ('sodium hydroxide + sulfuric acid → sodium sulfate + water', [(2, 'NaOH'), (1, 'H2SO4')], [(1, 'Na2SO4'), (2, 'H2O')]),
    ('magnesium + sulfuric acid → magnesium sulfate + hydrogen', [(1, 'Mg'), (1, 'H2SO4')], [(1, 'MgSO4'), (1, 'H2')]),
]
AR['H'] = 1
for _w, _l, _rr in EQS:
    _a, _b = {}, {}
    for c, f in _l:
        for e, n in atoms(f).items():
            _a[e] = _a.get(e, 0) + c * n
    for c, f in _rr:
        for e, n in atoms(f).items():
            _b[e] = _b.get(e, 0) + c * n
    assert _a == _b, _w


def side(lst, show=True):
    return ' + '.join((f'{c}' if (c > 1 and show) else '') + F(f) for c, f in lst)


def eqn(l, rr, show=True):
    return side(l, show) + ' → ' + side(rr, show)


def count_side(lst, e):
    return sum(c * atoms(f).get(e, 0) for c, f in lst)


N55 = 'Rearranging atoms: word and balanced symbol equations'
t55 = topic(N55, N55.lower(), 'balanced symbol equations', 'rearranging atoms')
FX(t55, 'C1', (1, 2), [
    ('In a chemical reaction, what happens to the atoms?', 'They are rearranged to form new substances', 'Atoms are not created or destroyed; they join up differently.', ['They are destroyed', 'New atoms are created', 'They change into different elements']),
    ('What does the 2 in 2H₂O mean?', 'Two molecules of water', 'The large number in front multiplies the whole formula.', ['Two hydrogen atoms only', 'Two oxygen atoms', 'Water is heated twice']),
    ('How many atoms are in one molecule of H₂SO₄?', '7', '2 H + 1 S + 4 O = 7 atoms.', ['3', '6', '4']),
    ('Why must a symbol equation be balanced?', 'Atoms cannot be created or destroyed, so there must be the same number of each atom on both sides', 'Balancing shows conservation of mass.',
     ['To make the reaction go faster', 'So that the products are heavier', 'Because the reactants are always gases']),
    ('When balancing an equation, what must you NOT change?', 'The small subscript numbers in formulae', 'Changing subscripts changes the substance; only the large numbers in front may change.', ['The numbers in front of formulae', 'The order of the products', 'The arrow']),
    ('What is the total mass of products when 12 g of magnesium reacts completely with 8 g of oxygen?', '20 g', 'Conservation of mass: 12 + 8 = 20 g.', ['4 g', '12 g', '96 g']),
    ('State the law of conservation of mass.', 'In a chemical reaction the total mass of the products equals the total mass of the reactants.', 'mass of products = mass of reactants [1]'),
])
FX(t55, 'C2', (1, 2, 3), [
    ('Explain why the equation H₂ + O₂ → H₂O is not balanced, and balance it.', 'There are 2 oxygen atoms on the left but only 1 on the right. Balanced: 2H₂ + O₂ → 2H₂O.', 'oxygen atoms unequal [1]; 2H₂ + O₂ → 2H₂O [1] [2]'),
    ('Explain why a student cannot balance H₂ + O₂ → H₂O by writing H₂ + O₂ → H₂O₂.', 'Changing the subscript changes the substance: H₂O₂ is hydrogen peroxide, not water; only the numbers in front can be changed.', 'changes the substance [1]; only coefficients can change [1] [2]'),
    ('Explain why burning magnesium in an open crucible gives a product heavier than the magnesium.', 'The magnesium combines with oxygen from the air; the mass of oxygen is added to the magnesium.', 'combines with oxygen [1]; oxygen mass added [1] [2]'),
    ('Explain what a word equation tells you that a balanced symbol equation does not, and vice versa.', 'A word equation names the substances; a balanced symbol equation also shows the formulae and the numbers of each particle reacting.', 'word: names [1]; symbol: formulae and ratios [1] [2]'),
    ('Explain why the mass in a sealed flask stays the same when two solutions react to form a precipitate.', 'No atoms enter or leave the sealed flask; they are only rearranged, so total mass is conserved.', 'nothing escapes [1]; atoms rearranged / mass conserved [1] [2]'),
])
misc(t55, 'C2', (2, 3, 4), [
    ('In 2Mg + O₂ → 2MgO there are more atoms on the right because the product is heavier.', 'There are 2 Mg and 2 O atoms on each side; the equation is balanced and mass is conserved.', 'atom count equal [1]; mass conserved [1] [2]'),
    ('A balanced equation must have the same number of molecules on each side.', 'It must have the same number of each type of atom; the number of molecules can differ (e.g. 2H₂ + O₂ → 2H₂O has 3 then 2).', 'atoms not molecules [1]; example [1] [2]'),
])


@t55.add('C3', (1, 2, 3, 4, 5))
def t55_bal(r, D):
    w, l, rr = r.choice([e for e in EQS if any(c > 1 for c, _ in e[1] + e[2])])
    bal = eqn(l, rr)
    unb = eqn(l, rr, show=False)
    if D <= 1:
        wrong = []
        for _ in range(12):
            l2 = [(max(1, c + r.choice([-1, 0, 1])), f) for c, f in l]
            r2 = [(max(1, c + r.choice([-1, 0, 1])), f) for c, f in rr]
            e2 = eqn(l2, r2)
            if e2 != bal and e2 not in wrong:
                wrong.append(e2)
        wrong.append(unb)
        return mq(r, f'Which is the correctly balanced equation for: {w}?', bal, wrong, f'Balanced: {bal}; atoms of each element are equal on both sides.')
    if D == 2:
        return Q(f'Balance this equation: {unb}', bal, f'correct numbers in front of formulae [1]; atoms equal on both sides [1] [2]')
    els = sorted({e for c, f in l for e in atoms(f)})
    e = r.choice(els)
    if D == 3:
        return Q(f'The word equation is: {w}. (a) Balance the symbol equation {unb}. (b) State the number of {e} atoms on each side of the balanced equation.', f'(a) {bal} (b) {count_side(l, e)} on each side',
                 f'(a) balanced [2] (b) {count_side(l, e)} [1] [3]', 'multi_step')
    k_ = r.choice([0.1, 0.2, 0.25, 0.5, 1, 2])
    masses = [(c, f, c * Mr(f) * k_) for c, f in l + rr]
    hide = r.randrange(len(masses))
    shown = '; '.join(f'{F(f)} {g(mm, 4)} g' for i, (c, f, mm) in enumerate(masses) if i != hide)
    s = f'The word equation is: {w}. (a) Balance the symbol equation {unb}. (b) In one experiment the masses are: {shown}. Calculate the mass of {F(masses[hide][1])}.'
    tot_l = sum(mm for c, f, mm in masses[:len(l)])
    a = f'(a) {bal} (b) {g(masses[hide][2], 4)} g'
    k = f'(a) balanced [2] (b) mass of reactants = mass of products (total {g(tot_l, 4)} g) [1]; {g(masses[hide][2], 4)} g [1]'
    if D == 4:
        return Q(s, a, k + ' [4]', 'multi_step')
    return Q(s + ' (c) State the law used in (b).', a + ' (c) Conservation of mass: atoms are rearranged, not created or destroyed.', k + ' (c) conservation of mass [1] [5]', 'multi_step')


@t55.add('C2', (1, 2, 3, 4))
def t55_count(r, D):
    w, l, rr = r.choice(EQS)
    bal = eqn(l, rr)
    els = sorted({e for c, f in l for e in atoms(f)})
    e = r.choice(els)
    n = count_side(l, e)
    if D <= 1:
        return mq(r, f'How many {e} atoms are shown on the left-hand side of {bal}?', str(n), [str(x) for x in (n + 1, n + 2, n + 3, max(1, n - 1), 2 * n) if x != n], f'Multiply each subscript by the number in front: {n}.')
    tot_l = sum(c * sum(atoms(f).values()) for c, f in l)
    tot_r = sum(c * sum(atoms(f).values()) for c, f in rr)
    return Q(f'For the balanced equation {bal}: (a) count the atoms of each element on each side; (b) explain how this shows that mass is conserved.',
             '(a) ' + '; '.join(f'{x}: {count_side(l, x)} and {count_side(rr, x)}' for x in els) + f' (b) The same atoms appear on both sides (just rearranged), so the total mass is the same.',
             '(a) all counts correct [1] (b) same atoms rearranged so mass unchanged [1] [2]' if D <= 2 else '(a) all counts correct [2] (b) same atoms rearranged so mass unchanged [1] [3]', 'explain')


def _eq_c4(r, D):
    w, l, rr = r.choice([e for e in EQS if len(e[1]) == 2])
    bal = eqn(l, rr)
    unb = eqn(l, rr, show=False)
    k_ = r.choice([0.1, 0.2, 0.5, 1])
    mr = sum(c * Mr(f) * k_ for c, f in l)
    intro = r.choice([f'{person(r)} studies the reaction: {w}.', f'In a laboratory in {city(r)}, a technician carries out the reaction: {w}.'])
    gas = any(f in ('H2', 'CO2', 'O2') for c, f in rr)
    cf = r.choice([f for c, f in l + rr if sum(atoms(f).values()) > 2] or [l[0][1]])
    parts = [
        lambda r: (f'Balance the symbol equation {unb}.', bal, 'correct coefficients [1]; atoms balanced [1] [2]'),
        lambda r: (f'Calculate the total mass of products formed when a total of {g(mr, 4)} g of reactants react completely.', f'{g(mr, 4)} g', 'conservation of mass [1]; same mass [1] [2]'),
        lambda r: ('Explain, in terms of atoms, why mass is conserved in this reaction.', 'Atoms are not created or destroyed, only rearranged into new substances, so the total mass stays the same.', 'atoms not created / destroyed [1]; rearranged [1] [2]'),
        lambda r: (('Explain why the mass shown on a balance would decrease if the reaction were done in an open beaker.' if gas else 'Predict what would happen to the reading on a balance if the reaction were done in a sealed flask.'),
                   ('A gas is produced and escapes into the air, so its mass is no longer measured.' if gas else 'It would stay the same, because no atoms can enter or leave.'), ('gas formed [1]; escapes [1] [2]' if gas else 'no change [1]; nothing enters or leaves [1] [2]')),
        lambda r: (f'State the total number of atoms in one particle of {F(cf)}.', f'{sum(atoms(cf).values())}', f'{sum(atoms(cf).values())} [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t55.add('C4', (2, 3, 4, 5), 'multi_step')(_eq_c4)
CHAPTERS[5] = [t51, t52, t53, t54, t55]


# =========================================================== 6 Sound and space

N61 = 'Loudness and pitch of sound: amplitude, frequency and oscilloscope traces'
t61 = topic(N61, N61.lower(), 'loudness and pitch', 'oscilloscope traces')
FX(t61, 'C1', (1, 2), [
    ('Which property of a sound wave determines its pitch?', 'Frequency', 'Higher frequency = higher pitch.', ['Amplitude', 'Speed', 'Loudness']),
    ('Which property of a sound wave determines its loudness?', 'Amplitude', 'Larger amplitude = louder sound.', ['Frequency', 'Wavelength only', 'Pitch']),
    ('What is the unit of frequency?', 'hertz (Hz)', '1 Hz = one vibration per second.', ['decibel (dB)', 'metre (m)', 'second (s)']),
    ('What is the normal range of human hearing?', '20 Hz to 20 000 Hz', 'Humans hear about 20 Hz – 20 kHz; the upper limit falls with age.', ['2 Hz to 200 Hz', '200 Hz to 2000 Hz', '20 000 Hz to 200 000 Hz']),
    ('On an oscilloscope trace, how does a louder sound of the same pitch appear?', 'The waves are taller but the same distance apart', 'Larger amplitude, same frequency.', ['The waves are closer together', 'The waves are further apart and shorter', 'The trace becomes a flat line']),
    ('Sound with a frequency above 20 000 Hz is called', 'ultrasound', 'Ultrasound is above the range of human hearing.', ['infrasound', 'an echo', 'a decibel']),
    ('What is frequency?', 'The number of complete waves (vibrations) per second', 'Measured in hertz.', ['The height of a wave', 'The speed of a wave', 'The time for one wave']),
    ('State what happens to the pitch and the loudness of a guitar note when the string is plucked harder.', 'The loudness increases; the pitch stays the same.', 'louder (bigger amplitude) [1]; pitch unchanged [1] [2]'),
])
FX(t61, 'C2', (1, 2, 3), [
    ('Explain why a shorter guitar string produces a higher-pitched note.', 'A shorter string vibrates faster, giving a higher frequency, and higher frequency means higher pitch.', 'vibrates faster / higher frequency [1]; higher pitch [1] [2]'),
    ('Explain why a sound gets quieter as you move away from the source.', 'The energy spreads out over a larger area and some is absorbed, so the amplitude of the vibrations reaching you is smaller.', 'energy spreads / absorbed [1]; smaller amplitude [1] [2]'),
    ('Explain why a dog can hear a whistle that its owner cannot.', 'The whistle’s frequency is above 20 000 Hz, outside human hearing range, but within the dog’s range.', 'frequency above human range [1]; dogs hear higher frequencies [1] [2]'),
    ('Describe how two oscilloscope traces would differ for a quiet high note and a loud low note.', 'Quiet high note: small amplitude, waves close together. Loud low note: large amplitude, waves further apart.', 'high note more waves / closer [1]; loud note taller waves [1] [2]'),
    ('Explain how a drummer makes a louder sound.', 'Hitting the drum harder makes the skin vibrate with a larger amplitude, so the sound wave has a larger amplitude and more energy.', 'larger amplitude vibration [1]; more energy / louder [1] [2]'),
    ('Explain why tightening a guitar string raises the pitch.', 'A tighter string vibrates at a higher frequency, which we hear as a higher pitch.', 'higher frequency [1]; higher pitch [1] [2]'),
])
misc(t61, 'C2', (2, 3, 4), [
    ('A high-pitched sound is always louder than a low-pitched sound.', 'Pitch depends on frequency and loudness on amplitude; a high note can be quiet and a low note loud.', 'pitch = frequency, loudness = amplitude [1]; independent [1] [2]'),
    ('Louder sounds travel faster through air.', 'The speed of sound depends on the medium, not on amplitude; loud and quiet sounds travel at the same speed in air.', 'speed set by medium [1]; same speed [1] [2]'),
    ('On an oscilloscope, the taller the waves, the higher the pitch.', 'Taller waves mean a larger amplitude (louder); higher pitch is shown by more waves across the screen (higher frequency).', 'height = loudness [1]; spacing = pitch [1] [2]'),
])


@t61.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t61_osc(r, D):
    tb = r.choice([0.5, 1, 2, 5])
    n = r.choice([2, 2.5, 4, 5, 8])
    T = n * tb
    f = 1000 / T
    if not (20 <= f <= 20000):
        return None
    a = r.choice([1.5, 2, 2.5, 3, 4])
    p = person(r)
    src = r.choice(['a tuning fork', 'a signal generator and loudspeaker', 'a flute', 'a recorder', 'a singer'])
    s = f'{p} connects a microphone to an oscilloscope to display the sound from {src}. The time-base is set to {g(tb)} ms per division, and one complete wave covers {g(n)} divisions. The trace is {g(a)} divisions high from the centre line to a peak.'
    if D <= 1:
        return numq(r, D, s, 'time period of the wave', T, ' ms', f'{g(n)} × {g(tb)}', [n / tb, tb, n])
    if D == 2:
        return Q(s + ' Calculate the time for one wave (the period) and the frequency.', f'{g(T)} ms; {g(f)} Hz', f'T = {g(n)} × {g(tb)} = {g(T)} ms [1]; f = 1 ÷ {g(T / 1000)} s = {g(f)} Hz [1] [2]')
    s3 = s + f' (a) Calculate the frequency of the sound. (b) The sound is made louder but the pitch is unchanged. Describe how the trace changes.'
    a3 = f'(a) T = {g(T)} ms = {g(T / 1000)} s; f = {g(f)} Hz (b) The waves become taller (larger amplitude) but stay the same width ({g(n)} divisions per wave).'
    k3 = f'(a) T = {g(T)} ms [1]; f = 1/T = {g(f)} Hz [1] (b) taller, same spacing [1]'
    if D == 3:
        return Q(s3, a3, k3 + ' [3]', 'multi_step')
    f2 = f * 2
    s4 = s3 + f' (c) The frequency is doubled to {g(f2)} Hz. State how many divisions one wave now covers.'
    a4 = a3 + f' (c) {g(n / 2)} divisions.'
    if D == 4:
        return Q(s4, a4, k3 + f' (c) {g(n / 2)} divisions [1] [4]', 'multi_step')
    return Q(s4 + ' (d) State whether a human could hear the new sound and explain.', a4 + (f' (d) Yes: {g(f2)} Hz is within the range 20 Hz – 20 000 Hz.' if f2 <= 20000 else f' (d) No: {g(f2)} Hz is above 20 000 Hz (ultrasound).'),
             k3 + f' (c) {g(n / 2)} divisions [1] (d) correct with range [1] [5]', 'multi_step')


@t61.add('C2', (1, 2, 3, 4))
def t61_compare(r, D):
    n1, n2 = r.sample([2, 3, 4, 5, 6, 8], 2)
    a1, a2 = r.sample([1, 1.5, 2, 2.5, 3, 4], 2)
    s = f'Two sounds are shown on the same oscilloscope settings. Trace P shows {n1} complete waves across the screen with a height of {g(a1)} squares; trace Q shows {n2} complete waves with a height of {g(a2)} squares.'
    hp = 'P' if n1 > n2 else 'Q'
    ld = 'P' if a1 > a2 else 'Q'
    if D <= 1:
        return mq(r, s + ' Which statement is correct?', f'{hp} has the higher pitch and {ld} is louder', [f'{"Q" if hp == "P" else "P"} has the higher pitch and {ld} is louder', f'{hp} has the higher pitch and {"Q" if ld == "P" else "P"} is louder', 'Both have the same pitch and loudness', f'{"Q" if hp == "P" else "P"} has the higher pitch and {"Q" if ld == "P" else "P"} is louder'],
                  'More waves = higher frequency (pitch); taller waves = larger amplitude (louder).')
    return Q(s + ' State which sound has the higher pitch and which is louder. Explain how you can tell from the traces.', f'{hp} has the higher pitch (more waves across the screen, higher frequency); {ld} is louder (taller waves, larger amplitude).',
             f'{hp} higher pitch [1]; {ld} louder [1]' + ('; frequency and amplitude reasons [1] [3]' if D >= 3 else ' [2]'), 'explain')


def _snd_c4(r, D):
    f = r.choice([256, 320, 384, 440, 512])
    tb = r.choice([1, 2])
    n = 1000 / f / tb
    intro = r.choice([f'A music teacher in {city(r)} uses a microphone and oscilloscope to show students the note from a tuning fork marked {f} Hz. The time-base is {tb} ms per division.',
                      f'{person(r)} records a {f} Hz note from a keyboard on an oscilloscope set to {tb} ms per division.'])
    parts = [
        lambda r: ('Calculate the period of the sound wave in milliseconds.', f'{g(1000 / f)} ms', f'T = 1/f = 1/{f} s [1] = {g(1000 / f)} ms [1] [2]'),
        lambda r: ('Calculate how many divisions one complete wave covers on the screen.', f'{g(n)} divisions', f'{g(1000 / f)} ÷ {tb} = {g(n)} [1]'),
        lambda r: ('Describe how the trace would change for a note one octave higher (double the frequency).', 'Twice as many waves across the screen (each wave half as wide); height unchanged if loudness is the same.', 'waves closer / twice as many [1]; same height [1] [2]'),
        lambda r: ('Describe how the trace would change if the note were played more quietly.', 'The waves would be shorter (smaller amplitude) but the same width.', 'smaller amplitude [1]; same spacing [1] [2]'),
        lambda r: ('Explain how the sound travels from the source to the microphone.', 'The source vibrates and pushes on air particles, creating compressions and rarefactions that pass through the air as a longitudinal wave.', 'vibrations passed through air particles [1]; compressions and rarefactions [1] [2]'),
        lambda r: ('Explain why the sound could not be detected if the source were in a vacuum.', 'Sound needs particles to travel through; there are none in a vacuum.', 'needs a medium [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t61.add('C4', (2, 3, 4, 5), 'multi_step')(_snd_c4)
t61.add('C3', (3, 4), 'multi_step')(_snd_c4)

N62 = 'Interference of sound waves'
t62 = topic(N62, N62.lower(), 'interference')
FX(t62, 'C1', (1, 2), [
    ('What happens when two sound waves meet in step (peak meets peak)?', 'They add up to give a louder sound', 'Constructive interference: amplitudes add.', ['They cancel to give silence', 'They change into light', 'They stop moving']),
    ('What happens when two identical sound waves meet exactly out of step (peak meets trough)?', 'They cancel out, giving a quiet sound', 'Destructive interference: amplitudes subtract.', ['They add to give a louder sound', 'They double their frequency', 'They reflect']),
    ('Noise-cancelling headphones work by', 'producing a sound wave that is out of step with the noise', 'The inverted wave cancels the noise by destructive interference.', ['making the noise louder', 'absorbing all sound with foam only', 'changing the pitch of the noise']),
    ('Two loudspeakers play the same note. A person walking in front of them hears', 'alternate loud and quiet regions', 'Interference pattern of constructive and destructive regions.', ['the same loudness everywhere', 'the pitch rise and fall', 'only silence']),
    ('Two waves of amplitude 3 units meet in step. What is the resulting amplitude?', '6 units', 'In step: amplitudes add, 3 + 3 = 6.', ['0 units', '3 units', '9 units']),
    ('State what is meant by interference of waves.', 'When two waves meet, they combine (add together) to give a bigger or smaller wave.', 'waves meet and combine / superpose [1]'),
])
FX(t62, 'C2', (1, 2, 3), [
    ('Explain why there are quiet spots in a room where two loudspeakers play the same note.', 'At those spots the waves from the two speakers arrive out of step, so a compression meets a rarefaction and they cancel.', 'waves arrive out of step [1]; cancel / destructive interference [1] [2]'),
    ('Explain how noise-cancelling headphones reduce the noise of an aircraft engine.', 'A microphone detects the noise and the headphones produce a wave of the same amplitude exactly out of step; the two cancel by destructive interference.', 'same amplitude, out of step [1]; destructive interference cancels noise [1] [2]'),
    ('Explain why switching off one of two loudspeakers removes the quiet spots.', 'With only one source there are no two waves to interfere, so there is no cancellation.', 'only one wave [1]; no interference [1] [2]'),
    ('Explain why noise-cancelling headphones work best on steady, low-pitched noise.', 'Steady sounds can be predicted and matched easily with an out-of-step wave; rapidly changing sounds are harder to cancel.', 'steady noise easy to match [1]; changing sounds hard [1] [2]'),
    ('Explain why the loud spots do not mean that energy has been created.', 'Energy is only redistributed: more energy arrives at loud spots and less at quiet spots; the total is unchanged.', 'energy redistributed [1]; total conserved [1] [2]'),
])
misc(t62, 'C2', (2, 3, 4), [
    ('Two sounds always make a louder sound than one sound.', 'If the waves arrive out of step they cancel (destructive interference) and the sound can be quieter.', 'can cancel [1]; out of step / destructive [1] [2]'),
    ('In a quiet spot the sound energy has been destroyed.', 'Energy is not destroyed; it is redistributed, so the loud spots receive more.', 'energy redistributed [1]; conserved [1] [2]'),
])


@t62.add('C3', (1, 2, 3, 4, 5))
def t62_path(r, D):
    f, lam = r.choice([(340, 1.0), (680, 0.5), (170, 2.0), (850, 0.4), (425, 0.8), (1700, 0.2)])
    mult = r.choice([0.5, 1, 1.5, 2, 2.5, 3])
    d1 = r.choice([3.0, 4.0, 5.0, 6.0])
    d2 = d1 + mult * lam
    loud = mult == int(mult)
    s = f'Two loudspeakers connected to the same signal generator emit a {f} Hz note in step. Point X is {g(d1)} m from one speaker and {g(d2)} m from the other. (Speed of sound = 340 m/s.)'
    if D <= 1:
        a1, a2 = sorted(r.sample([1.5, 2, 2.5, 3, 4], 2), reverse=True)
        return mq(r, f'Two sound waves with amplitudes of {g(a1)} cm and {g(a2)} cm on an oscilloscope screen meet exactly out of step. What is the amplitude of the combined wave?', f'{g(a1 - a2)} cm', [f'{g(a1 + a2)} cm', '0 cm', f'{g(a1)} cm'],
                  f'Out of step: amplitudes subtract, {g(a1)} − {g(a2)} = {g(a1 - a2)} cm.')
    if D == 2:
        return Q(s + ' Calculate the wavelength of the sound.', f'{g(lam)} m', f'λ = v ÷ f = 340 ÷ {f} [1] = {g(lam)} m [1] [2]')
    s3 = s + ' (a) Calculate the wavelength. (b) Calculate the path difference at X and state how many wavelengths it is. (c) Predict whether X is a loud or a quiet spot.'
    a = f'(a) {g(lam)} m (b) {g(d2)} − {g(d1)} = {g(mult * lam)} m = {g(mult)} wavelengths (c) {"Loud: whole number of wavelengths, waves arrive in step" if loud else "Quiet: odd number of half wavelengths, waves arrive out of step"}.'
    k = f'(a) {g(lam)} m [1] (b) {g(mult)} λ [1] (c) {"loud" if loud else "quiet"} with reason [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k + '; in step / out of step explained [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Explain what you would hear if one speaker were disconnected.', a + ' (d) A steady sound at X with no quiet spots, because there is no second wave to interfere.', k + '; in step / out of step [1] (d) no interference [1] [5]', 'multi_step')


def _int_c4(r, D):
    c = city(r)
    intro = r.choice([f'Engineers in {c} test noise-cancelling headphones for airline pilots. The cockpit noise is a steady hum.',
                      f'In a school hall in {c}, two loudspeakers play the same steady note. {person(r)} walks slowly across the front of the hall.'])
    if 'headphones' in intro:
        parts = [
            lambda r: ('Explain how the headphones cancel the hum.', 'A microphone picks up the hum; the headphones play a wave of the same frequency and amplitude, exactly out of step; destructive interference cancels it.', 'same frequency and amplitude [1]; out of step [1]; destructive interference [1] [3]'),
            lambda r: ('Explain why the cancelling wave must have the same amplitude as the hum.', 'Only equal amplitudes cancel completely; otherwise some sound remains.', 'equal amplitudes cancel fully [1]'),
            lambda r: ('Suggest why the pilots can still hear the radio voices clearly.', 'The headphones cancel only the steady hum; the voices are not matched by an inverse wave, so they are not cancelled.', 'only hum is cancelled [1]; voices not matched [1] [2]'),
            lambda r: ('Evaluate the use of noise-cancelling headphones compared with ear plugs.', 'They reduce steady noise while letting speech through, but need power and do not block sudden loud sounds well; ear plugs block all sounds.', 'advantage [1]; disadvantage [1] [2]'),
        ]
    else:
        parts = [
            lambda r: ('Describe what the person hears as they walk.', 'The sound gets alternately louder and quieter.', 'loud and quiet regions [1]'),
            lambda r: ('Explain why some places are loud.', 'Waves from both speakers arrive in step (compression with compression) and add up.', 'in step [1]; add / constructive [1] [2]'),
            lambda r: ('Explain why some places are quiet.', 'Waves arrive out of step (compression with rarefaction) and cancel.', 'out of step [1]; cancel / destructive [1] [2]'),
            lambda r: ('Predict what happens to the spacing of the loud spots if the frequency is increased.', 'They get closer together, because the wavelength is shorter.', 'closer [1]; shorter wavelength [1] [2]'),
        ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t62.add('C4', (2, 3, 4, 5), 'multi_step')(_int_c4)

N63 = 'Formation of the Moon: the collision theory and evidence'
t63 = topic(N63, N63.lower(), 'formation of the moon', 'collision theory')
FX(t63, 'C1', (1, 2), [
    ('According to the collision theory, how did the Moon form?', 'A Mars-sized body collided with the young Earth and debris joined together', 'Giant impact about 4.5 billion years ago; debris orbiting Earth clumped to form the Moon.',
     ['The Moon was captured by Earth’s gravity as it passed by', 'The Moon formed from a comet', 'The Moon broke away from the Sun']),
    ('What name is often given to the body that collided with the early Earth?', 'Theia', 'The hypothetical Mars-sized planet is called Theia.', ['Pangaea', 'Gaia', 'Andromeda']),
    ('About how long ago is the Moon thought to have formed?', 'About 4.5 billion years ago', 'Shortly after the formation of the Earth (4.6 billion years ago).', ['About 4.5 million years ago', 'About 65 million years ago', 'About 10 000 years ago']),
    ('Which evidence supports the collision theory?', 'Moon rocks have a very similar composition to rocks in Earth’s mantle', 'Similar oxygen isotopes suggest a shared origin.', ['The Moon has a large iron core like the Earth', 'The Moon has a thick atmosphere', 'The Moon is made of ice']),
    ('Why does the Moon have a lower average density than the Earth?', 'It has only a small iron core', 'Debris came mainly from the outer, rocky layers; most iron stayed in Earth’s core.', ['It is made mostly of gas', 'It is hollow', 'It has no gravity']),
    ('Where did scientists get samples of Moon rock to test?', 'From the Apollo missions and meteorites from the Moon', 'Astronauts brought back samples; some lunar meteorites reach Earth.', ['From telescopes only', 'From the Sun', 'From volcanoes on Earth']),
    ('State two pieces of evidence that support the collision theory.', 'Any two: Moon rocks similar to Earth’s mantle; Moon has a small iron core / low density; Moon rocks show they were once molten; few volatile substances in Moon rock.', 'any two [1] each [2]'),
])
FX(t63, 'C2', (1, 2, 3), [
    ('Explain how the similarity between Moon rocks and Earth’s mantle rocks supports the collision theory.', 'If the Moon formed from material thrown out of Earth’s mantle, the rocks would be expected to be similar, which they are.', 'Moon material came from Earth’s mantle [1]; prediction matches evidence [1] [2]'),
    ('Explain why the low density of the Moon supports the collision theory.', 'The impact threw out mainly lighter mantle rock; Earth’s dense iron core stayed behind, so the Moon has little iron and a lower density.', 'debris mainly from mantle [1]; little iron so low density [1] [2]'),
    ('Explain why the collision theory is still called a theory.', 'No one observed the event; it is the best explanation of the evidence and could change if new evidence is found.', 'not directly observed [1]; best explanation / could change [1] [2]'),
    ('Explain why the Moon’s surface has many more craters than the Earth’s.', 'The Moon has no atmosphere to burn up meteoroids and no weathering, erosion or plate movement to remove craters.', 'no atmosphere [1]; no erosion / tectonics [1] [2]'),
    ('Explain why evidence that Moon rocks were once molten supports the collision theory.', 'A giant impact would release enormous energy, melting the debris that formed the Moon (a magma ocean).', 'impact releases energy [1]; melts debris [1] [2]'),
])
misc(t63, 'C2', (2, 3, 4), [
    ('The Moon is made of the same material as the Earth’s core.', 'Moon rock resembles Earth’s mantle; the Moon has only a small iron core, so it is less dense than the Earth.', 'similar to mantle [1]; small iron core [1] [2]'),
    ('Because nobody saw the Moon form, scientists have no way of testing the theory.', 'Scientists test predictions of the theory against evidence such as Moon rock composition, density and computer models.', 'predictions tested [1]; example of evidence [1] [2]'),
])
BODIES = [('the Moon', 7.35e22, 2.20e19), ('the Earth', 5.97e24, 1.08e21), ('Mars', 6.42e23, 1.63e20), ('Mercury', 3.30e23, 6.08e19)]


@t63.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t63_dens(r, D):
    nm, M, V = r.choice(BODIES)
    rho = M / V
    s = f'{cap(nm)} has a mass of {sci(M)} kg and a volume of {sci(V)} m³.'
    if D <= 1:
        opts, a = mcq(r, f'{g(rho)} kg/m³', [f'{g(rho * 10)} kg/m³', f'{g(rho / 10)} kg/m³', f'{g(V / M * 1e7)} kg/m³'])
        return Q(s + ' What is its mean density?', a, f'ρ = M/V = {g(rho)} kg/m³.', opts=opts)
    if D == 2:
        return Q(s + ' Calculate its mean density.', f'{g(rho)} kg/m³', f'ρ = M ÷ V [1] = {g(rho)} kg/m³ [1] [2]')
    em = 5530
    s3 = (f'The Moon has a mass of {sci(7.35e22)} kg and a volume of {sci(2.20e19)} m³. Rocks from the Earth’s mantle have a density of about 3300 kg/m³ and the Earth’s mean density is {em} kg/m³. '
          '(a) Calculate the mean density of the Moon. (b) Explain how this result supports the collision theory.')
    mr = 7.35e22 / 2.20e19
    a = f'(a) {g(mr)} kg/m³ (b) It is close to the density of mantle rock and much less than the Earth’s mean density, so the Moon is probably made mostly of mantle material with little iron.'
    k = f'(a) ρ = M/V [1] = {g(mr)} kg/m³ [1] (b) similar to mantle / less than Earth [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k + '; little iron / material from mantle [1] [4]', 'multi_step')
    return Q(s3 + ' (c) Suggest one other measurement that would help to test the theory.', a + ' (c) Compare the chemical composition or isotopes of Moon rocks with Earth rocks; measure the size of the Moon’s core using seismometers.',
             k + '; little iron [1] (c) sensible measurement [1] [5]', 'multi_step')


THEORIES = [('capture theory', 'the Moon formed elsewhere and was captured by Earth’s gravity', 'it does not explain why Moon rocks are so similar to Earth’s mantle'),
            ('fission theory', 'the Moon spun off from a fast-spinning early Earth', 'the Earth could not have spun fast enough, and it does not explain the lack of volatile substances'),
            ('co-formation theory', 'the Earth and Moon formed together from the same cloud of material', 'it does not explain why the Moon has such a small iron core compared with the Earth')]


def _moon_c4(r, D):
    nm, idea, prob = r.choice(THEORIES)
    intro = r.choice([f'Some scientists once supported the {nm}: {idea}. Most scientists now support the collision theory.',
                      f'{person(r)} reads about two ideas for the origin of the Moon: the collision theory and the {nm} ({idea}).'])
    parts = [
        lambda r: ('Describe the collision theory.', 'About 4.5 billion years ago a Mars-sized body (Theia) hit the young Earth; material from the outer layers was thrown into orbit and clumped together to form the Moon.', 'Mars-sized body hits Earth [1]; debris orbits and forms Moon [1] [2]'),
        lambda r: (f'Give one weakness of the {nm}.', cap(prob) + '.', 'valid weakness [1]'),
        lambda r: ('Describe two pieces of evidence that support the collision theory.', 'Moon rocks are chemically very similar to Earth’s mantle; the Moon has a small iron core (low density); Moon rocks show they were once molten.', 'two pieces of evidence [1] each [2]'),
        lambda r: ('Explain why scientists changed their minds as new evidence became available.', 'Apollo samples and computer models gave evidence that fitted the collision theory better than the older ideas; scientific ideas change when evidence does not fit.', 'new evidence (samples / models) [1]; better fit [1] [2]'),
        lambda r: ('Evaluate whether the collision theory can be proved.', 'It cannot be proved absolutely because no one saw it happen; but it explains most of the evidence, so it is the best accepted theory and could be changed by new evidence.', 'cannot be proved directly [1]; explains evidence [1]; open to change [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t63.add('C4', (2, 3, 4, 5), 'multi_step')(_moon_c4)
t63.add('C3', (3, 4), 'multi_step')(_moon_c4)

N64 = 'Nebulae and the formation of stars and planets'
t64 = topic(N64, N64.lower(), 'nebulae', 'formation of stars and planets')
FX(t64, 'C1', (1, 2), [
    ('What is a nebula?', 'A huge cloud of dust and gas in space', 'Nebulae are mainly hydrogen and helium gas with dust.', ['A small rocky planet', 'A type of galaxy', 'The centre of a star']),
    ('Which two elements make up most of a nebula?', 'Hydrogen and helium', 'About three-quarters hydrogen and a quarter helium by mass.', ['Oxygen and nitrogen', 'Carbon and iron', 'Iron and nickel']),
    ('Which force pulls the material in a nebula together to form a star?', 'Gravity', 'Gravity makes the cloud collapse.', ['Friction', 'Magnetism', 'Air resistance']),
    ('What process begins in the core of a new star and releases huge amounts of energy?', 'Nuclear fusion of hydrogen into helium', 'Fusion starts when the core is hot and dense enough.', ['Combustion of hydrogen', 'Evaporation of helium', 'Nuclear fission of iron']),
    ('How do planets form around a young star?', 'Dust and gas in a spinning disc clump together', 'Particles collide and stick (accretion), growing into planets.', ['They are thrown out of the star', 'They are captured from other galaxies', 'They form from the star’s core']),
    ('Why are the inner planets of the Solar System rocky?', 'Near the hot young Sun, only rock and metal could stay solid', 'Lighter, icy and gaseous material was pushed outwards.', ['They were formed first', 'They are further from the Sun', 'They are made of hydrogen']),
    ('State the order of the stages in the formation of a star.', 'Nebula → gravity pulls material together → protostar heats up → nuclear fusion starts → star.', 'nebula and collapse [1]; protostar then fusion [1] [2]'),
])
FX(t64, 'C2', (1, 2, 3), [
    ('Explain why the centre of a collapsing nebula gets hotter.', 'As gravity pulls particles inwards they speed up and collide more often; the gravitational potential energy is transferred to thermal energy.', 'particles pulled in / speed up [1]; energy transferred to thermal [1] [2]'),
    ('Explain why the planets in our Solar System all orbit in the same direction.', 'They formed from the same spinning disc of dust and gas around the young Sun.', 'formed from rotating disc [1]; same direction as disc spun [1] [2]'),
    ('Explain why the outer planets are large and made mostly of gas.', 'Far from the Sun it was cold enough for ices and gases to remain, so these planets gathered large amounts of hydrogen and helium.', 'cold far from Sun [1]; collected gases [1] [2]'),
    ('Explain why some nebulae contain heavy elements such as iron.', 'They contain material from earlier stars that exploded as supernovae, spreading heavy elements made in those stars.', 'earlier stars exploded [1]; heavy elements spread into nebula [1] [2]'),
    ('Describe how astronomers can learn about star formation even though it takes millions of years.', 'They observe many nebulae and young stars at different stages and piece the stages together.', 'observe many objects at different stages [1]; build up sequence [1] [2]'),
])
misc(t64, 'C2', (2, 3, 4), [
    ('Stars burn hydrogen like a giant fire.', 'Stars do not burn (combust); energy is released by nuclear fusion of hydrogen into helium in the core.', 'not combustion [1]; nuclear fusion [1] [2]'),
    ('The planets formed first and then the Sun formed in the middle.', 'The Sun formed first at the centre of the collapsing cloud; planets formed later from the leftover disc of material.', 'Sun forms first [1]; planets from leftover disc [1] [2]'),
])
NEB = [('the Orion Nebula', 1340), ('the Eagle Nebula', 5700), ('the Crab Nebula', 6500), ('the Ring Nebula', 2300), ('the Horsehead Nebula', 1375), ('the Lagoon Nebula', 4100), ('the Carina Nebula', 8500)]
LY = 9.46e12


@t64.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t64_calc(r, D):
    if r.random() < 0.5 or D <= 1:
        M = r.choice([50, 100, 200, 500, 1000, 2000])
        pH, pHe = 74, 24
        s = f'A nebula has a mass of about {M} times the mass of the Sun. By mass it is {pH}% hydrogen, {pHe}% helium and {100 - pH - pHe}% other elements.'
        if D <= 1:
            return numq(r, D, s, 'mass of hydrogen in solar masses', M * pH / 100, ' solar masses', f'{M} × {pH}/100', [M * pHe / 100, M * 2 / 100, M])
        if D == 2:
            return Q(s + ' Calculate the mass of helium in the nebula, in solar masses.', f'{g(M * pHe / 100)} solar masses', f'{M} × {pHe} ÷ 100 [1] = {g(M * pHe / 100)} [1] [2]')
        n = r.choice([5, 10, 20, 25, 40])
        if n > M:
            n = M // 10
        s3 = s + f' (a) Calculate the mass of hydrogen. (b) If 20% of the nebula’s mass forms stars, calculate how many stars of 1 solar mass could form. (c) Explain why stars form where the gas is densest.'
        a = f'(a) {g(M * pH / 100)} solar masses (b) {g(M * 0.2)} stars (c) Gravity is strongest where there is most mass, so these regions collapse fastest.'
        k = f'(a) {g(M * pH / 100)} [1] (b) {M} × 0.2 = {g(M * 0.2)} [1] (c) more mass / stronger gravity [1]'
        if D == 3:
            return Q(s3, a, k + ' [3]', 'multi_step')
        return Q(s3 + ' (d) Name the process by which hydrogen is changed into helium in the new stars.', a + ' (d) Nuclear fusion.', k + ' (d) fusion [1]' + (' [4]' if D == 4 else '; energy released [1] [5]'), 'multi_step')
    nm, ly = r.choice(NEB)
    d = ly * LY
    s = f'{cap(nm)} is about {ly} light-years from Earth. One light-year is {sci(LY)} km.'
    if D == 2:
        return Q(s + ' Calculate its distance from Earth in kilometres.', f'{sci(d)} km', f'{ly} × {sci(LY)} [1] = {sci(d)} km [1] [2]')
    s3 = s + ' (a) Calculate its distance in kilometres. (b) State how long ago the light we see now left the nebula. (c) Explain why we are seeing the nebula as it was in the past.'
    a = f'(a) {sci(d)} km (b) {ly} years ago (c) Light takes {ly} years to travel that distance, so it shows the nebula when the light left it.'
    k = f'(a) {sci(d)} km [1] (b) {ly} years [1] (c) light takes time to travel [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    return Q(s3 + ' (d) Suggest why astronomers use light-years rather than kilometres for such distances.', a + ' (d) The numbers in kilometres are enormous and hard to compare; light-years give smaller, more manageable numbers.', k + ' (d) numbers too large [1]' + (' [4]' if D == 4 else '; easier comparison [1] [5]'), 'multi_step')


STAGES = ['A cloud of dust and gas (nebula) exists in space', 'Gravity pulls the gas and dust together and the cloud starts to collapse', 'The centre becomes hot and dense, forming a protostar',
          'Nuclear fusion starts and a star is born', 'Leftover material forms a spinning disc around the star', 'Dust and rock in the disc clump together to form planets']


@t64.add('C2', (1, 2, 3, 4))
def t64_order(r, D):
    idx = list(range(len(STAGES)))
    sh = idx[:]
    while sh == idx:
        r.shuffle(sh)
    lettered = '; '.join(f'{"PQRSTU"[i]}: {STAGES[j]}' for i, j in enumerate(sh))
    correct = ''.join("PQRSTU"[sh.index(j)] for j in idx)
    s = f'These statements describe the formation of a star and its planets, in the wrong order. {lettered}.'
    if D <= 1:
        wrong = set()
        while len(wrong) < 3:
            w = list(correct)
            i, j = r.sample(range(6), 2)
            w[i], w[j] = w[j], w[i]
            wrong.add(''.join(w))
        return mq(r, s + ' Which is the correct order?', correct, sorted(wrong), 'Nebula → collapse → protostar → fusion → disc → planets.')
    return Q(s + (' Put the statements in the correct order.' if D == 2 else ' Put the statements in the correct order and explain the role of gravity.'), correct + ('' if D == 2 else '. Gravity pulls the material together to make the star and also makes dust clump into planets.'),
             'correct order [2]; one pair swapped [1]' + (' [2]' if D == 2 else '; gravity role [1] [3]'), 'explain')


def _neb_c4(r, D):
    nm, ly = r.choice(NEB)
    intro = r.choice([f'Astronomers using a space telescope photograph {nm}, about {ly} light-years away. They see dark, dense clumps of gas and dust with young stars inside.',
                      f'{person(r)} reads that {nm} is a “stellar nursery” where new stars are forming, about {ly} light-years from Earth.'])
    parts = [
        lambda r: ('Describe what a nebula is made of.', 'Mainly hydrogen and helium gas with some dust.', 'hydrogen and helium [1]; dust [1] [2]'),
        lambda r: ('Explain how a star forms from a dense clump in the nebula.', 'Gravity pulls the material together; it collapses and heats up to form a protostar; when the core is hot and dense enough, nuclear fusion of hydrogen begins.', 'gravity collapse [1]; heats / protostar [1]; fusion begins [1] [3]'),
        lambda r: ('Explain how planets could form around one of these young stars.', 'Leftover dust and gas form a spinning disc; particles collide and stick together, growing into planets.', 'disc of material [1]; particles clump / accretion [1] [2]'),
        lambda r: ('Explain why the photographs show the nebula as it was long ago.', f'Light takes {ly} years to reach us, so we see the light that left {ly} years ago.', 'light travel time [1]'),
        lambda r: ('Suggest why the same process is thought to have formed our Sun and Solar System.', 'The Sun and planets formed about 4.6 billion years ago; planets orbit in one plane and direction, matching a spinning disc from a nebula.', 'planets in one plane / same direction [1]; matches disc model [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t64.add('C4', (2, 3, 4, 5), 'multi_step')(_neb_c4)

N65 = 'Tectonics: plate movement and evidence for continental drift'
t65 = topic(N65, N65.lower(), 'tectonics', 'continental drift')
FX(t65, 'C1', (1, 2), [
    ('Who proposed the theory of continental drift in 1912?', 'Alfred Wegener', 'Wegener suggested the continents were once joined as Pangaea.', ['Charles Darwin', 'Isaac Newton', 'Ernest Rutherford']),
    ('What name did Wegener give to the single supercontinent?', 'Pangaea', 'Pangaea broke up about 200 million years ago.', ['Gondwana Ocean', 'Atlantis', 'Theia']),
    ('What causes tectonic plates to move?', 'Convection currents in the mantle', 'Heat from the core drives slow convection in the mantle.', ['The Moon’s gravity', 'Winds in the atmosphere', 'Ocean waves']),
    ('About how fast do tectonic plates move?', 'A few centimetres per year', 'Typical rates are 2–10 cm per year.', ['A few metres per day', 'A few kilometres per year', 'They do not move']),
    ('Which evidence supports continental drift?', 'Fossils of the same land reptile found in South America and Africa', 'Mesosaurus could not swim across an ocean, so the continents were once joined.', ['The Moon has craters', 'The oceans are salty', 'Mountains are high']),
    ('Earthquakes and volcanoes are most common', 'at the boundaries between plates', 'Plates moving past, towards or away from each other cause these events.', ['in the middle of plates', 'only near the Equator', 'only in the oceans']),
    ('State three types of evidence for continental drift.', 'Any three: jigsaw fit of coastlines; matching fossils; matching rock types and mountain ranges; evidence of past climates (e.g. coal in Antarctica, glacial deposits in India).', 'three types [2]; two [1] [2]'),
])
FX(t65, 'C2', (1, 2, 3), [
    ('Explain why the shapes of the coastlines of South America and Africa support continental drift.', 'They fit together like jigsaw pieces, suggesting they were once joined and have moved apart.', 'fit together [1]; were once joined [1] [2]'),
    ('Explain why scientists did not accept Wegener’s ideas when he first proposed them.', 'He could not explain what force could move continents; there was no mechanism and little evidence from the sea floor at the time.', 'no mechanism [1]; insufficient evidence then [1] [2]'),
    ('Explain how coal found in Antarctica supports the idea that continents move.', 'Coal forms from plants in warm, swampy places; Antarctica must once have been nearer the Equator.', 'coal from warm-climate plants [1]; Antarctica moved [1] [2]'),
    ('Explain how convection currents in the mantle move tectonic plates.', 'Hot mantle rock rises, spreads sideways under the plates and sinks as it cools; the moving mantle drags the plates along.', 'hot rock rises and cool sinks [1]; drags plates [1] [2]'),
    ('Explain why rocks get older with distance from a mid-ocean ridge.', 'New crust forms at the ridge as magma rises and the plates move apart, so the oldest rock has been carried furthest away.', 'new crust at ridge [1]; plates move apart carrying older rock [1] [2]'),
])
misc(t65, 'C2', (2, 3, 4), [
    ('The continents float on a liquid core.', 'The plates rest on the mantle, which is mostly solid but flows very slowly; the outer core is far deeper.', 'plates on mantle [1]; mantle flows slowly [1] [2]'),
    ('Wegener’s theory was rejected because it was wrong.', 'His idea was largely correct, but rejected at first because he could not explain the mechanism; later evidence (sea-floor spreading) supported it.', 'idea later supported [1]; rejected due to lack of mechanism [1] [2]'),
])


@t65.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t65_rate(r, D):
    rate = r.choice([2, 2.5, 3, 4, 5, 7, 10])
    where = r.choice(['The Atlantic Ocean is widening', 'Two plates in the Pacific are moving apart', 'The Indian plate is moving north', 'Two plates along a mid-ocean ridge are spreading apart'])
    if D <= 1:
        N = r.choice([1, 2, 5, 10])
        return numq(r, D, f'{where} at about {g(rate)} cm per year.', f'distance moved in {N} million years in km', rate * N * 10, ' km', f'{g(rate)} cm/yr × {N} × 10⁶ yr = {g(rate * N * 1e6)} cm', [rate * N, rate * N * 100, rate * N * 1000])
    if D == 2:
        N = r.choice([1, 2, 5, 10, 20])
        return Q(f'{where} at about {g(rate)} cm per year. Calculate how far it moves in {N} million years, in kilometres.', f'{g(rate * N * 10)} km',
                 f'{g(rate)} × {N} × 10⁶ = {g(rate * N * 1e6)} cm [1]; ÷ 100 000 = {g(rate * N * 10)} km [1] [2]')
    dist = r.choice([1500, 2000, 3000, 4000, 5000])
    t_ = dist * 1e5 / rate
    s = f'{where} at about {g(rate)} cm per year. (a) Calculate the time taken, in millions of years, for the plates to move {dist} km apart. (b) Explain why we do not notice plate movement in everyday life.'
    a = f'(a) {dist} km = {g(dist * 1e5)} cm; {g(dist * 1e5)} ÷ {g(rate)} = {g(t_)} years = {g(t_ / 1e6)} million years (b) A few centimetres a year is far too slow to notice (about as fast as fingernails grow).'
    k = f'(a) km → cm [1]; ÷ rate = {g(t_ / 1e6)} million years [1] (b) movement very slow [1]'
    if D == 3:
        return Q(s, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s + ' (c) Name the process in the mantle that drives this movement.', a + ' (c) Convection currents.', k + ' (c) convection currents [1] [4]', 'multi_step')
    return Q(s + ' (c) Name the process in the mantle that drives this movement. (d) Suggest why plate movement can still cause sudden events such as earthquakes.', a + ' (c) Convection currents. (d) Plates can stick at boundaries; stress builds up and is released suddenly when they slip.',
             k + ' (c) [1] (d) stress builds and releases suddenly [1] [5]', 'multi_step')


EVID = [('fossils of the reptile Mesosaurus are found in both South America and southern Africa', 'Mesosaurus lived in fresh water and could not have crossed an ocean, so the continents were joined'),
        ('fossils of the fern Glossopteris are found in India, Africa, Australia and Antarctica', 'its heavy seeds could not cross oceans, so these continents were once joined'),
        ('rock layers and mountain ranges in Scotland match those in eastern Canada', 'the matching rocks formed together before the continents separated'),
        ('glacial scratches in rocks are found in India and Africa, now near the Equator', 'these areas were once near the South Pole and have moved'),
        ('coal seams are found in Antarctica', 'coal forms from tropical swamp plants, so Antarctica was once in a warmer place')]


def _tec_c4(r, D):
    e1, e2 = r.sample(EVID, 2)
    intro = r.choice([f'In 1912 Alfred Wegener proposed that the continents were once joined. Evidence includes: (i) {e1[0]}; (ii) {e2[0]}.',
                      f'{person(r)} is preparing a talk on continental drift. Two pieces of evidence are: (i) {e1[0]}; (ii) {e2[0]}.'])
    parts = [
        lambda r: ('Explain how evidence (i) supports continental drift.', cap(e1[1]) + '.', 'valid reasoning about the evidence [1]; so the continents were once joined / have moved [1] [2]'),
        lambda r: ('Explain how evidence (ii) supports continental drift.', cap(e2[1]) + '.', 'valid reasoning about the evidence [1]; so the continents were once joined / have moved [1] [2]'),
        lambda r: ('Explain why many scientists rejected Wegener’s idea at first.', 'He could not explain how continents could move; there was no known mechanism.', 'no mechanism [1]'),
        lambda r: ('Describe the evidence from the ocean floor that later convinced scientists.', 'Sea-floor spreading: new rock forms at mid-ocean ridges and gets older with distance from the ridge, with matching magnetic stripes on each side.', 'new rock at ridges / age pattern [1]; symmetrical magnetic stripes [1] [2]'),
        lambda r: ('Explain what drives the movement of the plates.', 'Convection currents in the mantle, caused by heat from the core, slowly drag the plates.', 'convection currents in mantle [1]; heat from core [1] [2]'),
        lambda r: ('Explain why this is a good example of how scientific ideas change.', 'An idea that was rejected was later accepted when new evidence and a mechanism were found.', 'new evidence changed opinion [1]; ideas tested and revised [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t65.add('C4', (2, 3, 4, 5), 'multi_step')(_tec_c4)
t65.add('C3', (3, 4), 'multi_step')(_tec_c4)
CHAPTERS[6] = [t61, t62, t63, t64, t65]

# =========================================================== 7 Genes and inheritance
CHROMO = [('dog', 78), ('cat', 38), ('chimpanzee', 48), ('fruit fly', 8), ('horse', 64), ('chicken', 78), ('rice plant', 24), ('potato plant', 48), ('onion', 16), ('mouse', 40), ('cow', 60), ('garden pea', 14), ('maize (corn)', 20)]

N71 = 'Chromosomes, genes and DNA'
t71 = topic(N71, N71.lower(), 'chromosomes genes dna')
FX(t71, 'C1', (1, 2), [
    ('Where are chromosomes found in a cell?', 'In the nucleus', 'Chromosomes are long DNA molecules inside the nucleus.', ['In the cytoplasm', 'In the cell membrane', 'In the vacuole']),
    ('What are chromosomes made of?', 'DNA', 'Each chromosome is a very long DNA molecule (with proteins).', ['Starch', 'Cellulose', 'Fat']),
    ('What is a gene?', 'A short section of DNA that carries the information for one characteristic', 'Each chromosome carries many genes.', ['A whole chromosome', 'A type of cell', 'The nucleus of a cell']),
    ('How many chromosomes are in a normal human body cell?', '46', '23 pairs.', ['23', '44', '92']),
    ('Which scientists published the double-helix model of DNA in 1953?', 'Watson and Crick', 'They used X-ray images produced by Rosalind Franklin and Maurice Wilkins.', ['Darwin and Wallace', 'Newton and Hooke', 'Mendel and Pasteur']),
    ('What shape is a DNA molecule?', 'A double helix', 'Two strands twisted around each other.', ['A single straight line', 'A sphere', 'A flat sheet']),
    ('Whose X-ray image of DNA was important evidence for the double-helix model?', 'Rosalind Franklin', 'Photo 51 showed the helical structure.', ['Marie Curie', 'Charles Darwin', 'Alfred Wegener']),
    ('State the relationship between a chromosome, a gene and DNA.', 'A chromosome is a long molecule of DNA; a gene is a short section of that DNA.', 'chromosome made of DNA [1]; gene is a section of DNA [1] [2]'),
])
FX(t71, 'C2', (1, 2, 3), [
    ('Explain why chromosomes in body cells are found in pairs.', 'One chromosome of each pair comes from the mother (egg) and one from the father (sperm).', 'one from each parent [1]; via egg and sperm [1] [2]'),
    ('Explain why identical twins have the same genes.', 'They develop from one fertilised egg that splits into two, so both have the same DNA.', 'one fertilised egg splits [1]; same DNA [1] [2]'),
    ('Explain why mature human red blood cells cannot pass on genetic information.', 'They have no nucleus, so they contain no chromosomes or DNA.', 'no nucleus [1]; no DNA [1] [2]'),
    ('Explain how Watson and Crick used the work of other scientists.', 'They used Franklin and Wilkins’ X-ray images and other chemical data to build their model; science builds on shared evidence.', 'used X-ray evidence [1]; collaboration / building on others [1] [2]'),
    ('Explain why a gene can affect a characteristic such as eye colour.', 'The gene carries the instructions for making a protein (e.g. pigment), which produces the characteristic.', 'instructions for a protein [1]; protein gives characteristic [1] [2]'),
])
misc(t71, 'C2', (2, 3, 4), [
    ('A gene is bigger than a chromosome.', 'A chromosome contains many genes; a gene is a small section of a chromosome’s DNA.', 'chromosome contains many genes [1]; gene is a section [1] [2]'),
    ('Organisms with more chromosomes are always more complex.', 'Chromosome number does not match complexity: a potato has 48, a human 46 and a dog 78.', 'no link [1]; example [1] [2]'),
])


@t71.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t71_count(r, D):
    org, n = r.choice(CHROMO)
    if D <= 1:
        return mq(r, f'A body cell of {art(org)} {org} contains {n} chromosomes. How many chromosomes are in one of its gametes?', str(n // 2), [str(n), str(n * 2), str(n // 2 + 1), str(n - 2)], f'Gametes have half: {n} ÷ 2 = {n // 2}.')
    if D == 2:
        return Q(f'A body cell of {art(org)} {org} has {n} chromosomes. State the number of chromosomes in its sperm or egg cells and in a fertilised egg.', f'{n // 2} in a gamete; {n} in a fertilised egg',
                 f'{n // 2} [1]; {n} [1] [2]')
    s = f'A body cell of {art(org)} {org} has {n} chromosomes.'
    s3 = s + ' (a) State the number of pairs of chromosomes. (b) State the number in a gamete. (c) Explain why gametes must have half the number of chromosomes.'
    a = f'(a) {n // 2} pairs (b) {n // 2} (c) At fertilisation two gametes fuse, so the fertilised egg gets the full number ({n}) and the number stays the same each generation.'
    k = f'(a) {n // 2} [1] (b) {n // 2} [1] (c) fusion restores full number [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k + '; number constant each generation [1] [4]', 'multi_step')
    return Q(s3 + f' (d) Predict, with a reason, the number of chromosomes if a gamete with the normal number fused with a body cell by mistake.', a + f' (d) {n // 2 + n}: the extra chromosomes would not halve, so the cell would have too many.',
             k + f'; constant [1] (d) {n // 2 + n} with reason [1] [5]', 'multi_step')


def _dna_c4(r, D):
    org, n = r.choice(CHROMO)
    intro = r.choice([f'A biology class in {city(r)} looks at cells from {art(org)} {org} under a microscope. Each body cell contains {n} chromosomes.',
                      f'{person(r)} reads that the body cells of {art(org)} {org} each contain {n} chromosomes, and human body cells contain 46.'])
    parts = [
        lambda r: ('State where the chromosomes are found in the cell.', 'In the nucleus.', 'nucleus [1]'),
        lambda r: (f'State how many chromosomes are in {art(org)} {org} sperm or egg cell.', f'{n // 2}', f'{n // 2} [1]'),
        lambda r: ('Describe the structure of a chromosome.', 'A long, coiled molecule of DNA (a double helix) carrying many genes along its length.', 'long DNA molecule [1]; carries many genes [1] [2]'),
        lambda r: ('Explain what a gene does.', 'It is a section of DNA that carries the instructions for a characteristic (by coding for a protein).', 'section of DNA [1]; instructions for a characteristic [1] [2]'),
        lambda r: ('Describe the contribution of Rosalind Franklin to the discovery of the structure of DNA.', 'She produced X-ray images of DNA (Photo 51) showing it was a helix; Watson and Crick used this to build their model.', 'X-ray images [1]; used by Watson and Crick [1] [2]'),
        lambda r: ('Explain why offspring are similar to, but not identical to, either parent.', 'They receive half their chromosomes (genes) from each parent, giving a new combination.', 'half from each parent [1]; new combination [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t71.add('C4', (2, 3, 4, 5), 'multi_step')(_dna_c4)
t71.add('C3', (3, 4), 'multi_step')(_dna_c4)

N72 = 'Gametes and inheritance including sex determination'
t72 = topic(N72, N72.lower(), 'gametes and inheritance', 'sex determination')
FX(t72, 'C1', (1, 2), [
    ('Which pair of sex chromosomes does a human female have?', 'XX', 'Females XX, males XY.', ['XY', 'YY', 'X only']),
    ('Which sex chromosomes can a human sperm cell carry?', 'Either X or Y', 'Half of sperm carry X, half carry Y.', ['Always X', 'Always Y', 'Both X and Y']),
    ('Which sex chromosome does every human egg cell carry?', 'X', 'Females are XX, so every egg carries an X.', ['Y', 'Either X or Y', 'Both X and Y']),
    ('What is the probability that a baby will be a boy?', '0.5 (50%)', 'Half of sperm carry Y.', ['0.25 (25%)', '0.75 (75%)', '1 (100%)']),
    ('What are gametes?', 'Sex cells such as sperm and egg cells', 'Gametes carry half the normal number of chromosomes.', ['Body cells with two sets of chromosomes', 'Cells of the placenta', 'Red blood cells']),
    ('What happens at fertilisation?', 'The nucleus of a sperm fuses with the nucleus of an egg', 'The fertilised egg has a full set of chromosomes.', ['Two eggs fuse together', 'The egg divides into gametes', 'The sperm swims back to the testes']),
    ('How many chromosomes are in a human egg cell?', '23', 'Half of 46.', ['46', '22', '92']),
    ('State which parent determines the sex of a child and explain why.', 'The father, because his sperm can carry either X or Y; the egg always carries X.', 'father [1]; sperm X or Y, egg always X [1] [2]'),
])
FX(t72, 'C2', (1, 2, 3), [
    ('Explain why approximately equal numbers of boys and girls are born.', 'Half of the sperm carry X and half carry Y, and each has an equal chance of fertilising the egg, so XX and XY are equally likely.', 'half sperm X, half Y [1]; equal chance of fertilising [1] [2]'),
    ('Explain why brothers and sisters with the same parents are not identical.', 'Each gamete carries a different combination of the parents’ chromosomes, so each child inherits a different mix.', 'gametes differ [1]; different combinations inherited [1] [2]'),
    ('Explain why a child has some features of the mother and some of the father.', 'Half of the chromosomes (genes) come from the mother’s egg and half from the father’s sperm.', 'half from each parent [1]; genes control features [1] [2]'),
    ('Describe how to show sex determination using a genetic diagram.', 'Write the parents as XX and XY, their gametes as X (egg) and X or Y (sperm), and combine them in a grid to give XX and XY in a 1 : 1 ratio.', 'parents and gametes shown [1]; offspring 1 : 1 [1] [2]'),
    ('Explain why gametes must carry only one chromosome from each pair.', 'So that when two gametes fuse the fertilised egg has the normal number (pairs), not double.', 'fusion of two gametes [1]; restores normal number [1] [2]'),
])
misc(t72, 'C2', (2, 3, 4), [
    ('Our family already has three girls, so our next baby is very likely to be a boy.', 'Each pregnancy is independent; the chance of a boy is still 0.5 (50%) every time.', 'independent events [1]; 0.5 each time [1] [2]'),
    ('The mother decides whether the baby is a boy or a girl because the baby grows inside her.', 'Every egg carries X; the sperm carries X or Y, so the father’s sperm determines the sex.', 'egg always X [1]; sperm X or Y determines sex [1] [2]'),
    ('A boy gets his X chromosome from his father.', 'A boy (XY) gets his Y from his father and his X from his mother.', 'Y from father [1]; X from mother [1] [2]'),
])


@t72.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t72_prob(r, D):
    n = r.choice([2, 3, 4])
    N = r.choice([100, 200, 500, 1000, 2400, 5000])
    if D <= 1:
        return mq(r, f'A couple are expecting their {["", "", "second", "third", "fourth"][n]} child. ' + ('Their first child is a girl.' if n == 2 else f'Their first {["", "", "", "two", "three"][n]} children are all girls.') + ' What is the probability that the next child is a boy?', '0.5', ['0.25', '0.75', '1', f'{g(1 / n, 2)}'],
                  'Each birth is independent: probability of a boy = 0.5.')
    if D == 2:
        return Q(f'A hospital in {city(r)} expects {N} births this year. Estimate how many babies will be boys and explain your answer.', f'About {N // 2}', f'{N} × 0.5 = {N // 2} [1]; half of sperm carry Y / chance 0.5 [1] [2]')
    p = 0.5 ** n
    s = f'A couple plan to have {n} children. (a) Draw or describe a genetic diagram to show the chance of each child being a girl. (b) Calculate the probability that ' + ('both children are girls.' if n == 2 else f'all {n} children are girls.')
    a = f'(a) XX × XY → gametes X and X, Y → offspring XX : XY = 1 : 1, so 0.5 girl each time (b) 0.5^{n} = {g(p)} (1 in {2 ** n})'
    k = f'(a) gametes [1]; 1 : 1 ratio [1] (b) 0.5^{n} = {g(p)} [1]'
    if D == 3:
        return Q(s, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s + ' (c) Explain why the probability for the next child is unchanged even after several girls.', a + ' (c) Each fertilisation is a separate event; the chance of an X or Y sperm is always 0.5.', k + ' (c) independent events [1] [4]', 'multi_step')
    return Q(s + f' (c) Explain why the probability for the next child is unchanged even after several girls. (d) In a large survey of {N} families each with one child, how many would you expect to have a boy?', a + f' (c) Each fertilisation is a separate event with chance 0.5. (d) About {N // 2}.',
             k + f' (c) independent [1] (d) {N // 2} [1] [5]', 'multi_step')


def _sex_c4(r, D):
    N = r.choice([1200, 1500, 2000, 2400, 3000])
    boys = N // 2 + r.choice([-40, -24, -16, 12, 20, 36, 48])
    intro = r.choice([f'Records at a hospital in {city(r)} show {N} births in one year: {boys} boys and {N - boys} girls.', f'{person(r)} studies birth records for a town: of {N} babies born, {boys} were boys.'])
    parts = [
        lambda r: ('Calculate the percentage of babies that were boys.', f'{g(boys / N * 100)}%', f'{boys} ÷ {N} × 100 [1] = {g(boys / N * 100)}% [1] [2]'),
        lambda r: ('Explain, using a genetic diagram, why about half of babies are boys.', 'Mother XX makes eggs all X; father XY makes sperm X or Y in equal numbers; fertilisation gives XX : XY = 1 : 1.', 'parents XX and XY [1]; gametes [1]; 1 : 1 offspring [1] [3]'),
        lambda r: ('Suggest why the numbers are not exactly 50% boys and 50% girls.', 'Fertilisation is random (chance), so small differences from the expected ratio occur, especially in small samples.', 'chance / random [1]; sample size [1] [2]'),
        lambda r: ('State the number of chromosomes in a human sperm cell and the sex chromosome(s) it may carry.', '23; either X or Y.', '23 [1]; X or Y [1] [2]'),
        lambda r: ('Describe what happens at fertilisation.', 'The nucleus of a sperm fuses with the nucleus of an egg, giving a fertilised egg with 46 chromosomes in 23 pairs.', 'nuclei fuse [1]; 46 / 23 pairs [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t72.add('C4', (2, 3, 4, 5), 'multi_step')(_sex_c4)
t72.add('C3', (3, 4), 'multi_step')(_sex_c4)

N73 = 'Variation: continuous and discontinuous and its causes'
t73 = topic(N73, N73.lower(), 'variation', 'continuous and discontinuous')
CONT = ['height', 'body mass', 'hand span', 'foot length', 'leaf length', 'arm length', 'heart rate']
DISC = ['blood group', 'ability to roll the tongue', 'attached or free earlobes', 'eye colour', 'flower colour in pea plants', 'sex (male or female)']
FX(t73, 'C1', (1, 2), [
    ('Which is an example of continuous variation?', 'Height', 'Height can take any value within a range.', ['Blood group', 'Tongue rolling', 'Attached or free earlobes']),
    ('Which is an example of discontinuous variation?', 'Blood group', 'Blood groups fall into distinct categories (A, B, AB, O).', ['Body mass', 'Height', 'Hand span']),
    ('Which type of graph is best for showing continuous variation?', 'A histogram', 'Continuous data are grouped into classes with no gaps between bars.', ['A bar chart with gaps', 'A pie chart only', 'A scatter graph of one variable']),
    ('Which characteristic is caused by genes only?', 'Blood group', 'Blood group is inherited and not affected by environment.', ['Spoken language', 'A scar', 'Body mass']),
    ('Which characteristic is caused mainly by the environment?', 'A scar on the knee', 'Scars come from injuries, not genes.', ['Blood group', 'Natural eye colour', 'Tongue-rolling ability']),
    ('Identical twins grow up in different countries and have different masses. This is caused by', 'the environment', 'They have identical genes, so differences come from diet, exercise, etc.', ['their genes', 'their blood groups', 'their chromosomes being different']),
    ('State the difference between continuous and discontinuous variation.', 'Continuous: any value in a range (e.g. height). Discontinuous: distinct groups with no in-between values (e.g. blood group).', 'continuous described [1]; discontinuous described [1] [2]'),
])
FX(t73, 'C2', (1, 2, 3), [
    ('Explain why height is affected by both genes and the environment.', 'Genes set the possible range of height; diet, health and exercise affect how tall a person actually grows.', 'genes set potential [1]; environment (diet etc.) affects outcome [1] [2]'),
    ('Explain why studies of identical twins are useful for finding the causes of variation.', 'Identical twins have the same genes, so any differences between them must be caused by the environment.', 'same genes [1]; differences due to environment [1] [2]'),
    ('Explain why a bar chart is used for blood group data but a histogram is used for heights.', 'Blood groups are separate categories (discontinuous); heights are continuous data that must be grouped into touching classes.', 'blood group categories [1]; height continuous / grouped [1] [2]'),
    ('Explain why plants of the same variety grown in the shade are often taller but paler than those in sunlight.', 'The environment (light) affects growth: shaded plants grow taller to reach light and make less chlorophyll; their genes are the same.', 'environmental cause [1]; light affects growth / colour [1] [2]'),
    ('Explain why variation within a species is important.', 'Some individuals may be better suited to changes in the environment and survive, so the species is less likely to die out.', 'some individuals better adapted [1]; species survives change [1] [2]'),
])
misc(t73, 'C2', (2, 3, 4), [
    ('Eye colour is continuous variation because there are lots of shades.', 'Eye colour is usually treated as discontinuous, sorted into distinct groups such as brown, blue and green; height is an example of continuous variation.', 'eye colour grouped / discontinuous [1]; correct continuous example [1] [2]'),
    ('All variation is caused by genes.', 'Variation can be caused by genes, by the environment (e.g. scars, language) or by both (e.g. height, mass).', 'environmental causes exist [1]; example [1] [2]'),
])


@t73.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t73_data(r, D):
    feat = r.choice(['hand span', 'height', 'foot length', 'leaf length'])
    unit = {'hand span': 'cm', 'height': 'cm', 'foot length': 'cm', 'leaf length': 'mm'}[feat]
    rng = {'hand span': (16, 23), 'height': (148, 172), 'foot length': (21, 27), 'leaf length': (42, 78)}[feat]
    n = r.choice([8, 9, 10])
    vals = [r.randint(*rng) for _ in range(n)]
    who = 'students in a class' if feat != 'leaf length' else 'leaves from one tree'
    s = f'{person(r)} measures the {feat} of {n} {who} ({unit}): {", ".join(map(str, vals))}.'
    mean = sum(vals) / n
    if D <= 1:
        return mq(r, s + ' What type of variation does this show?', 'Continuous variation', ['Discontinuous variation', 'No variation', 'Variation caused only by genes'], f'{cap(feat)} can take any value in a range.')
    if D == 2:
        return Q(s + ' Calculate the range and the mean.', f'range {max(vals) - min(vals)} {unit}; mean {g(mean)} {unit}', f'range = {max(vals)} − {min(vals)} = {max(vals) - min(vals)} [1]; mean = {sum(vals)} ÷ {n} = {g(mean)} [1] [2]')
    s3 = s + ' (a) Calculate the mean. (b) State the type of variation and the type of graph you would use to display a larger set of these data. (c) Suggest one environmental factor that could affect this characteristic.'
    env = {'hand span': 'diet / nutrition during growth', 'height': 'diet, illness or exercise', 'foot length': 'diet during growth', 'leaf length': 'amount of light or water'}[feat]
    a = f'(a) {g(mean)} {unit} (b) Continuous; histogram (c) {cap(env)}.'
    k = f'(a) {g(mean)} [1] (b) continuous and histogram [1] (c) valid factor [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Explain why a larger sample would give a more reliable mean.', a + ' (d) Unusual individual values have less effect, so the mean is closer to the true population mean.', k + ' (d) reduces effect of extremes [1] [4]', 'multi_step')
    return Q(s3 + f' (d) Explain why a larger sample would give a more reliable mean. (e) Group the data into classes of equal width.', a + ' (d) Unusual values have less effect. (e) Any sensible equal-width classes covering all values with correct tallies.',
             k + ' (d) [1] (e) equal classes and tallies [1] [5]', 'multi_step')


@t73.add('C2', (1, 2, 3, 4))
def t73_classify(r, D):
    c = r.choice(CONT)
    d = r.choice(DISC)
    if D <= 1:
        return mq(r, f'Which characteristic shows discontinuous variation?', d, CONT, f'{cap(d)} falls into distinct groups.')
    return Q(f'Classify {c} and {d} as continuous or discontinuous variation, giving a reason for each.', f'{cap(c)}: continuous (any value within a range). {cap(d)}: discontinuous (distinct categories).',
             'each correct with reason [1] [1] [2]' if D <= 2 else f'each correct with reason [1] [1]; suitable graph for each (histogram / bar chart) [1] [3]', 'explain')


def _var_c4(r, D):
    ns = r.choice([12, 15, 20])
    m1 = r.choice([46, 50, 54, 58])
    m2 = m1 + r.choice([10, 12, 15, 18])
    intro = r.choice([f'{person(r)} grows {ns} seedlings from the same parent plant in bright light and {ns} in shade. After four weeks the mean leaf length is {m1} mm in bright light and {m2} mm in the shade.',
                      f'In a school garden in {city(r)}, {ns} cuttings from one plant (so with identical genes) are planted in shade and {ns} in full sun. The mean leaf length is {m2} mm in shade and {m1} mm in sun.'])
    parts = [
        lambda r: ('Calculate the difference in mean leaf length.', f'{m2 - m1} mm', f'{m2} − {m1} = {m2 - m1} mm [1]'),
        lambda r: ('Explain whether this variation is caused by genes or by the environment.', 'The environment, because the plants have the same genes (same parent / cuttings); only the light differs.', 'environment [1]; same genes so difference due to light [1] [2]'),
        lambda r: ('State the type of variation shown by leaf length and give a reason.', 'Continuous, because leaf length can take any value within a range.', 'continuous [1]; any value in range [1] [2]'),
        lambda r: ('Suggest why the plants in the shade grow larger leaves.', 'Larger leaves have a bigger surface area to absorb the limited light for photosynthesis.', 'larger surface area [1]; absorb more light [1] [2]'),
        lambda r: ('Suggest two variables that should be kept the same in this investigation.', 'Any two: type of soil, amount of water, temperature, pot size, age of plants.', 'two variables [1] each [2]'),
        lambda r: ('Explain why a mean of many plants is used.', 'Individual plants vary; a mean reduces the effect of unusual plants and is more reliable.', 'natural variation [1]; more reliable [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t73.add('C4', (2, 3, 4, 5), 'multi_step')(_var_c4)

N74 = 'Natural selection and evolution'
t74 = topic(N74, N74.lower(), 'natural selection', 'evolution')
FX(t74, 'C1', (1, 2), [
    ('Who proposed the theory of evolution by natural selection?', 'Charles Darwin', 'Darwin (with Alfred Russel Wallace) published in 1858–1859.', ['Gregor Mendel', 'Alfred Wegener', 'Isaac Newton']),
    ('In natural selection, which individuals are most likely to survive?', 'Those best adapted to their environment', 'Better-adapted individuals survive, breed and pass on their genes.', ['The largest individuals always', 'The oldest individuals', 'Those that move the least']),
    ('What do surviving individuals pass on to their offspring?', 'Their genes, including those for the useful characteristic', 'Offspring inherit the advantageous genes.', ['Characteristics they gained during life, such as strong muscles from exercise', 'Their food supply', 'Nothing at all']),
    ('Why did dark peppered moths become more common in polluted areas in the 1800s?', 'They were better camouflaged on soot-blackened trees, so fewer were eaten', 'Birds ate more pale moths, so dark moths survived and bred.', ['Soot turned pale moths dark', 'Dark moths were stronger fliers', 'Pale moths moved to the cities']),
    ('What is evolution?', 'The gradual change in the characteristics of a species over many generations', 'Natural selection causes evolution.', ['A change in one animal during its life', 'The death of all members of a species', 'The growth of a fetus']),
    ('Bacteria that survive an antibiotic are', 'resistant to that antibiotic', 'Resistant bacteria survive and multiply.', ['killed by it more quickly', 'always harmless', 'unable to reproduce']),
    ('State the four main steps in natural selection.', 'Variation exists; competition / struggle for survival; best-adapted individuals survive and reproduce; they pass on their genes, so the useful feature becomes more common.', 'variation and competition [1]; survival, reproduction and inheritance [1] [2]'),
])
FX(t74, 'C2', (1, 2, 3), [
    ('Explain how antibiotic-resistant bacteria become common.', 'A few bacteria have a mutation giving resistance; the antibiotic kills the others; the resistant ones survive, reproduce and pass on the resistance gene.', 'variation / mutation [1]; non-resistant killed [1]; resistant survive and reproduce [1] [3]'),
    ('Explain why giraffes have long necks, according to natural selection.', 'Giraffes varied in neck length; those with longer necks reached more food, survived and bred more, passing on genes for long necks over many generations.', 'variation [1]; survival and breeding of longer-necked [1]; genes passed on over generations [1] [3]'),
    ('Explain why patients are told to finish a course of antibiotics.', 'To kill all the bacteria, including the slightly more resistant ones, so resistant bacteria do not survive and multiply.', 'kill all bacteria [1]; prevent resistant survivors [1] [2]'),
    ('Explain why fossils provide evidence for evolution.', 'Fossils in rocks of different ages show that organisms have changed gradually over time.', 'fossils in different rock ages [1]; show gradual change [1] [2]'),
    ('Explain why natural selection is slow in large animals but fast in bacteria.', 'Bacteria reproduce in minutes, so many generations pass quickly; large animals take years per generation.', 'generation time [1]; bacteria very short [1] [2]'),
])
misc(t74, 'C2', (2, 3, 4), [
    ('Giraffes stretched their necks to reach leaves, and their babies were born with longer necks.', 'Characteristics acquired during life are not inherited; giraffes with genes for longer necks survived and passed those genes on.', 'acquired features not inherited [1]; selection of genetic variation [1] [2]'),
    ('Bacteria become resistant because they get used to the antibiotic.', 'Individual bacteria do not adapt; resistant ones already exist due to mutation and survive, so they multiply.', 'resistance already present by mutation [1]; selected by antibiotic [1] [2]'),
    ('Natural selection means the strongest animal always wins.', 'It means the best-adapted individuals survive and reproduce; that could be the best camouflaged, not the strongest.', 'best adapted, not strongest [1]; example [1] [2]'),
])


@t74.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t74_moth(r, D):
    rel_p = r.choice([200, 300, 400, 500, 600])
    rel_d = r.choice([200, 300, 400, 500, 600])
    wood = r.choice(['polluted', 'clean'])
    if wood == 'polluted':
        fp, fd = r.choice([0.10, 0.12, 0.14]), r.choice([0.25, 0.28, 0.3])
    else:
        fp, fd = r.choice([0.12, 0.14, 0.16]), r.choice([0.05, 0.06, 0.08])
    cp, cd = round(rel_p * fp), round(rel_d * fd)
    s = f'Scientists released {rel_p} pale and {rel_d} dark peppered moths in a {wood} wood with {"soot-darkened" if wood == "polluted" else "pale, lichen-covered"} tree trunks. Later they recaptured {cp} pale and {cd} dark moths.'
    pp, pd = cp / rel_p * 100, cd / rel_d * 100
    better = 'dark' if pd > pp else 'pale'
    if D <= 1:
        return mq(r, s + ' Which moths survived better?', f'{better} moths', ['pale moths', 'dark moths', 'both survived equally', 'neither survived'], f'Recapture: pale {g(pp)}%, dark {g(pd)}%.')
    if D == 2:
        return Q(s + ' Calculate the percentage of each type recaptured.', f'pale {g(pp)}%; dark {g(pd)}%', f'{cp} ÷ {rel_p} × 100 = {g(pp)}% [1]; {cd} ÷ {rel_d} × 100 = {g(pd)}% [1] [2]')
    s3 = s + ' (a) Calculate the percentage of each type recaptured. (b) Explain why percentages are compared rather than numbers. (c) Explain the results in terms of natural selection.'
    a = f'(a) pale {g(pp)}%, dark {g(pd)}% (b) Different numbers of each type were released. (c) {cap(better)} moths were better camouflaged on these trunks, so birds ate fewer of them; more survived to breed and pass on their genes.'
    k = '(a) both percentages [1] (b) different numbers released [1] (c) camouflage → fewer eaten [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k + '; survive, breed, pass on genes [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Predict how the proportion of dark moths would change over many generations after air pollution is reduced, and explain why.', a + ' (d) It would fall: trunks become paler, so pale moths are better camouflaged and survive to breed more.',
             k + '; pass on genes [1] (d) prediction with reason [1] [5]', 'multi_step')


@t74.add('C3', (2, 3, 4, 5), 'numerical')
def t74_bact(r, D):
    N = r.choice([1e6, 2e6, 5e6, 1e7])
    p = r.choice([0.01, 0.02, 0.05, 0.1])
    surv = N * p
    gens = r.choice([3, 4, 5, 6])
    s = f'A patient has an infection of {sci(N, 2)} bacteria. {g(p * 100)}% of them carry a gene for resistance to an antibiotic. The antibiotic kills all the bacteria that are not resistant.'
    if D <= 2:
        return Q(s + ' Calculate the number of bacteria that survive.', f'{sci(surv, 2)}', f'{sci(N, 2)} × {g(p)} [1] = {sci(surv, 2)} [1] [2]')
    after = surv * 2 ** gens
    s3 = s + f' (a) Calculate the number that survive. (b) The survivors double in number every 20 minutes. Calculate the number after {gens * 20} minutes. (c) Explain why the antibiotic will no longer cure the infection.'
    a = f'(a) {sci(surv, 2)} (b) {sci(surv, 2)} × 2^{gens} = {sci(after, 2)} (c) All the new bacteria have inherited the resistance gene, so the antibiotic cannot kill them.'
    k = f'(a) {sci(surv, 2)} [1] (b) {gens} doublings → {sci(after, 2)} [1] (c) all resistant / inherited [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Suggest one way doctors can reduce the spread of resistance.', a + ' (d) Prescribe antibiotics only when needed, make patients finish the course, or use a different antibiotic.', k + ' (d) valid way [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Suggest one way doctors can reduce the spread of resistance. (e) Explain why this is an example of natural selection.', a + ' (d) Avoid unnecessary prescriptions; finish courses. (e) There was variation; the antibiotic selected the resistant bacteria, which survived and reproduced, passing on the gene.',
             k + ' (d) [1] (e) variation, selection, inheritance [1] [5]', 'multi_step')


def _ns_c4(r, D):
    b1 = r.choice([9.2, 9.4, 9.6, 9.8])
    b2 = round(b1 + r.choice([0.4, 0.5, 0.6]), 1)
    intro = r.choice([f'On a Galápagos island, the mean beak depth of a population of finches was {b1} mm. After a severe drought, when only large, hard seeds were left, the mean beak depth of the survivors’ offspring was {b2} mm.',
                      f'Scientists studying ground finches recorded a mean beak depth of {b1} mm before a drought. The drought killed most plants with small seeds. In the next generation the mean beak depth was {b2} mm.'])
    parts = [
        lambda r: ('Calculate the percentage increase in mean beak depth.', f'{g(pct(b1, b2))}%', f'({b2} − {b1}) ÷ {b1} × 100 [1] = {g(pct(b1, b2))}% [1] [2]'),
        lambda r: ('Explain how natural selection caused this change.', 'Beak depth varied; birds with deeper beaks could crack the large hard seeds, so they survived and bred; they passed on genes for deep beaks, so the mean increased.', 'variation [1]; deep-beaked birds survive [1]; breed and pass on genes [1] [3]'),
        lambda r: ('Explain why the change can only happen if beak depth is at least partly controlled by genes.', 'Only genetic characteristics are passed to offspring; features caused only by the environment are not inherited.', 'genes inherited [1]; environmental features not passed on [1] [2]'),
        lambda r: ('Predict what might happen to beak depth if several wet years produce plenty of small seeds.', 'Mean beak depth may decrease again, as smaller-beaked birds feed efficiently and survive well.', 'decrease [1]; reason [1] [2]'),
        lambda r: ('Suggest why Darwin’s observations of finches helped him develop his theory.', 'Different islands had finches with beaks suited to the local food, suggesting they had adapted from a common ancestor by natural selection.', 'beaks match food [1]; common ancestor adapted [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t74.add('C4', (2, 3, 4, 5), 'multi_step')(_ns_c4)
CHAPTERS[7] = [t71, t72, t73, t74]


# =========================================================== 8 Rates of reaction
REACT8 = [('marble chips (calcium carbonate)', 'dilute hydrochloric acid', 'carbon dioxide'), ('magnesium ribbon', 'dilute hydrochloric acid', 'hydrogen'),
          ('zinc granules', 'dilute sulfuric acid', 'hydrogen'), ('limestone chips', 'dilute hydrochloric acid', 'carbon dioxide')]


def _curve(r, Vmax, k, step, n=7):
    ts = [step * i for i in range(n)]
    vs = [round(Vmax * (1 - math.exp(-k * t))) for t in ts]
    return ts, vs


N81 = 'Measuring the rate of reaction: gas volume and mass loss'
t81 = topic(N81, N81.lower(), 'measuring the rate of reaction', 'gas volume and mass loss')
FX(t81, 'C1', (1, 2), [
    ('Which apparatus is used to measure the volume of gas produced in a reaction?', 'A gas syringe', 'A gas syringe collects and measures gas volume (or an inverted measuring cylinder).', ['A thermometer', 'A pipette', 'A Bunsen burner']),
    ('Why does the mass of a flask of marble chips and acid decrease during the reaction?', 'Carbon dioxide gas escapes', 'The gas leaves through the cotton wool plug, so mass falls.', ['The acid evaporates completely', 'The marble chips are destroyed', 'Mass is destroyed in reactions']),
    ('What is the rate of a reaction?', 'How quickly reactants are used up or products are formed', 'Rate = amount of product formed (or reactant used) ÷ time.', ['How much product is formed in total', 'The temperature of the reaction', 'The colour of the products']),
    ('Which unit could be used for the rate of a reaction that produces a gas?', 'cm³/s', 'Volume of gas per unit time.', ['cm³', 's/cm³', 'g/cm³']),
    ('On a graph of gas volume against time, when is the reaction fastest?', 'At the start, where the curve is steepest', 'Steepest gradient = fastest rate.', ['At the end, where the curve is flat', 'Halfway through', 'The rate is always the same']),
    ('Why does a reaction eventually stop?', 'One of the reactants is used up', 'When a reactant runs out, no more product forms.', ['The products get too hot', 'The gas syringe is full', 'The catalyst is used up']),
    ('Name two measurements that can be used to follow the rate of a reaction that gives off a gas.', 'The volume of gas produced over time; the loss in mass over time.', 'gas volume [1]; mass loss [1] [2]'),
])
FX(t81, 'C2', (1, 2, 3), [
    ('Explain why the rate of reaction between marble chips and acid decreases as the reaction goes on.', 'The reactants are being used up, so there are fewer acid particles and less marble to collide; collisions become less frequent.', 'reactants used up [1]; fewer collisions [1] [2]'),
    ('Explain why a cotton wool plug is placed in the neck of the flask when measuring mass loss.', 'It lets the gas escape but stops acid spray escaping, so only the mass of gas lost is measured.', 'gas escapes [1]; acid spray retained [1] [2]'),
    ('Explain why a gas syringe gives more accurate results than counting bubbles.', 'It measures the actual volume of gas; bubbles vary in size and fast bubbling is hard to count.', 'measures volume [1]; bubbles vary / hard to count [1] [2]'),
    ('Explain why the graph of gas volume against time becomes horizontal.', 'The reaction has stopped because one reactant has been used up, so no more gas is produced.', 'reaction stopped [1]; reactant used up [1] [2]'),
    ('Explain how you can use a graph to compare the rates of two reactions.', 'The steeper curve shows the faster reaction; the one that reaches its final volume sooner is faster.', 'steeper = faster [1]; finishes sooner [1] [2]'),
])
misc(t81, 'C2', (2, 3, 4), [
    ('The reaction is fastest at the end because the most gas has been collected by then.', 'The total volume is largest at the end, but the rate (gas per second) is greatest at the start, where the graph is steepest.', 'total vs rate [1]; steepest at start [1] [2]'),
    ('The balance reading falls because the marble disappears and mass is destroyed.', 'Mass is conserved; it falls because carbon dioxide gas escapes from the flask.', 'mass conserved [1]; gas escapes [1] [2]'),
])


@t81.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t81_gas(r, D):
    solid, acid, gas = r.choice(REACT8)
    Vmax = r.choice([48, 60, 72, 80, 90, 96])
    k = r.choice([0.04, 0.05, 0.06, 0.08])
    step = r.choice([10, 15, 20])
    ts, vs = _curve(r, Vmax, k, step)
    tab = ', '.join(f'{t} s: {v} cm³' for t, v in zip(ts, vs))
    p = person(r)
    s = f'{p} adds {solid} to {acid} and collects the {gas} in a gas syringe: {tab}.'
    i = r.choice([1, 2, 3])
    rate = vs[i] / ts[i]
    if D <= 1:
        return numq(r, D, s, f'mean rate of reaction over the first {ts[i]} s', rate, ' cm³/s', f'{vs[i]} ÷ {ts[i]}', [ts[i] / vs[i], vs[i] * ts[i] / 100, vs[-1] / ts[-1]])
    if D == 2:
        return Q(s + f' Calculate the mean rate of reaction over the first {ts[i]} s.', f'{g(rate)} cm³/s', f'{vs[i]} ÷ {ts[i]} [1] = {g(rate)} cm³/s [1] [2]')
    r2 = (vs[i + 2] - vs[i + 1]) / step
    s3 = s + f' (a) Calculate the mean rate over the first {ts[1]} s and between {ts[i + 1]} s and {ts[i + 2]} s. (b) Explain why the rate changes.'
    a = f'(a) {g(vs[1] / ts[1])} cm³/s and {g(r2)} cm³/s (b) The rate decreases because the reactants are being used up, so collisions become less frequent.'
    k_ = f'(a) {vs[1]} ÷ {ts[1]} = {g(vs[1] / ts[1])} [1]; ({vs[i + 2]} − {vs[i + 1]}) ÷ {step} = {g(r2)} [1] (b) reactants used up / fewer collisions [1]'
    if D == 3:
        return Q(s3, a, k_ + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (c) Describe how the graph of these results would look.', a + ' (c) A curve that is steep at the start, becomes less steep and levels off.', k_ + ' (c) steep then levels off [1] [4]', 'multi_step')
    return Q(s3 + ' (c) Describe how the graph of these results would look. (d) Suggest why the final volume might be slightly less than expected.', a + ' (c) A curve that is steep at the start, becomes less steep and levels off.' + f' (d) Some {gas} escaped before the bung was fitted, or some dissolved in the solution.',
             k_ + ' (c) [1] (d) gas lost / dissolved [1] [5]', 'multi_step')


@t81.add('C3', (2, 3, 4, 5), 'numerical')
def t81_mass(r, D):
    m0 = r.choice([152.40, 168.75, 175.20, 183.60, 196.35])
    loss = r.choice([1.2, 1.6, 2.0, 2.4, 3.0])
    k = r.choice([0.3, 0.4, 0.5])
    ts = [0, 1, 2, 3, 4, 5, 6]
    ms = [round(m0 - loss * (1 - math.exp(-k * t)), 2) for t in ts]
    tab = ', '.join(f'{t} min: {mm:.2f} g' for t, mm in zip(ts, ms))
    s = f'{person(r)} places a flask of dilute hydrochloric acid and marble chips on a balance: {tab}.'
    l2 = m0 - ms[2]
    if D == 2:
        return Q(s + ' Calculate the mass lost in the first 2 minutes and the mean rate of mass loss in g/min.', f'{l2:.2f} g; {g(l2 / 2)} g/min', f'{m0:.2f} − {ms[2]:.2f} = {l2:.2f} g [1]; ÷ 2 = {g(l2 / 2)} g/min [1] [2]')
    tot = m0 - ms[-1]
    s3 = s + ' (a) Calculate the total mass lost. (b) Name the substance responsible for the mass loss. (c) Calculate the mean rate of mass loss in the first minute and in the last minute.'
    a = f'(a) {tot:.2f} g (b) Carbon dioxide gas escaping (c) {m0 - ms[1]:.2f} g/min and {ms[5] - ms[6]:.2f} g/min'
    k_ = f'(a) {tot:.2f} g [1] (b) carbon dioxide [1] (c) both rates [1]'
    if D == 3:
        return Q(s3, a, k_ + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Explain the difference between the two rates.', a + ' (d) Fewer reacting particles remain later, so there are fewer collisions per second.', k_ + ' (d) fewer particles / collisions [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Explain the difference between the two rates. (e) Write the word equation for the reaction.', a + ' (d) Fewer reacting particles remain, so collisions are less frequent. (e) calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide',
             k_ + ' (d) [1] (e) word equation [1] [5]', 'multi_step')


def _rate_c4(r, D):
    solid, acid, gas = r.choice(REACT8)
    Vmax = r.choice([60, 72, 80, 90])
    ts, vs = _curve(r, Vmax, r.choice([0.05, 0.06, 0.08]), r.choice([10, 20]))
    tab = ', '.join(f'{t} s: {v} cm³' for t, v in zip(ts, vs))
    intro = r.choice([f'A class in {city(r)} reacts {solid} with {acid} and measures the {gas} given off: {tab}.', f'{person(r)} follows the reaction of {solid} with {acid} using a gas syringe: {tab}.'])
    fin = next((t for t, v in zip(ts, vs) if v >= vs[-1] - 1), ts[-1])
    parts = [
        lambda r: ('Draw a labelled diagram, or describe, the apparatus used.', f'Conical flask with the reactants and a bung connected by a delivery tube to a gas syringe; a stopwatch.', 'flask and bung [1]; gas syringe / measuring cylinder [1] [2]'),
        lambda r: (f'Calculate the mean rate of reaction in the first {ts[1]} s.', f'{g(vs[1] / ts[1])} cm³/s', f'{vs[1]} ÷ {ts[1]} [1] = {g(vs[1] / ts[1])} cm³/s [1] [2]'),
        lambda r: ('State the total volume of gas produced and estimate when the reaction finished.', f'{vs[-1]} cm³; at about {fin} s', 'total volume [1]; time [1] [2]'),
        lambda r: ('Explain, in terms of particles, why the rate decreases over time.', 'Reacting particles are used up, so there are fewer particles to collide and fewer successful collisions per second.', 'particles used up [1]; fewer collisions per second [1] [2]'),
        lambda r: ('Describe a test to identify the gas.', 'Carbon dioxide: turns limewater milky.' if gas == 'carbon dioxide' else 'Hydrogen: a lighted splint gives a squeaky pop.', 'test [1]; result [1] [2]'),
        lambda r: ('Suggest one source of error and how to reduce it.', 'Gas escapes while the bung is put in: use a divided flask or tie the solid in a bag so the reaction starts after sealing.', 'error [1]; improvement [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t81.add('C4', (2, 3, 4, 5), 'multi_step')(_rate_c4)

N82 = 'Surface area and the rate of reaction'
t82 = topic(N82, N82.lower(), 'surface area')
FX(t82, 'C1', (1, 2), [
    ('Which form of calcium carbonate reacts fastest with acid?', 'Powder', 'Powder has the largest surface area.', ['Large lumps', 'Small chips', 'One single block']),
    ('Increasing the surface area of a solid reactant', 'increases the rate of reaction', 'More particles exposed, more frequent collisions.', ['decreases the rate of reaction', 'has no effect', 'stops the reaction']),
    ('Why does powder react faster than lumps of the same mass?', 'More particles are exposed for collisions', 'A larger surface area gives more frequent collisions.', ['Powder particles are hotter', 'Powder has more mass', 'Powder is a catalyst']),
    ('Breaking a cube into eight smaller cubes makes the total surface area', 'twice as large', 'Each small cube has 1/4 the face area; 8 × 1/4 = 2 times.', ['eight times as large', 'half as large', 'the same']),
    ('Why can flour dust in a mill explode?', 'The fine powder has a huge surface area, so it burns extremely quickly', 'Very fast combustion of dust can cause an explosion.', ['Flour is radioactive', 'Flour contains water', 'The dust is very heavy']),
    ('Explain in one sentence why chewing food helps digestion.', 'Chewing breaks food into smaller pieces with a larger surface area, so enzymes can act faster.', 'larger surface area [1]; faster digestion [1] [2]'),
])
FX(t82, 'C2', (1, 2, 3), [
    ('Explain, using the particle model, why powdered marble reacts faster with acid than marble chips.', 'Powder has a larger surface area, so more calcium carbonate particles are exposed to acid particles, giving more frequent collisions.', 'larger surface area [1]; more frequent collisions [1] [2]'),
    ('Explain why the total volume of gas is the same for chips and powder if the same mass is used with excess acid.', 'The same amount of reactant is present, so the same amount of product forms; only the rate differs.', 'same amount of reactant [1]; only rate changes [1] [2]'),
    ('Explain why small pieces of wood (kindling) are used to start a fire.', 'Small pieces have a large surface area, so they react with oxygen faster and catch fire more easily.', 'large surface area [1]; faster reaction with oxygen [1] [2]'),
    ('Explain why indigestion tablets that are crushed work faster than whole ones.', 'Crushing increases the surface area, so the tablet reacts with stomach acid faster.', 'larger surface area [1]; faster neutralisation [1] [2]'),
    ('Explain why a fair test comparing chips and powder must use the same mass of solid.', 'Changing the mass would change the amount of reactant, which also affects the rate and the volume of gas; only surface area should change.', 'mass affects result [1]; only one variable changed [1] [2]'),
])
misc(t82, 'C2', (2, 3, 4), [
    ('Powder reacts faster because it has more mass than the lumps.', 'The masses are the same; powder reacts faster because it has a larger surface area, so collisions are more frequent.', 'same mass [1]; surface area / collisions [1] [2]'),
    ('Powder gives off more gas in total than chips.', 'With the same mass and excess acid, both give the same total volume; powder just produces it faster.', 'same total [1]; faster [1] [2]'),
])


@t82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t82_cube(r, D):
    n = r.choice([2, 3])
    L = r.choice([x for x in (2, 3, 4, 6) if x % n == 0])
    A1 = 6 * L * L
    A2 = A1 * n
    s = f'A cube of calcium carbonate has sides of {L} cm.'
    if D <= 1:
        return numq(r, D, s, 'total surface area of the cube', A1, ' cm²', f'6 × {L} × {L}', [L * L, L ** 3, 4 * L * L])
    if D == 2:
        return Q(s + ' Calculate its total surface area.', f'{A1} cm²', f'one face = {L} × {L} = {L * L} cm² [1]; × 6 = {A1} cm² [1] [2]')
    s3 = s + f' It is cut into {n ** 3} identical smaller cubes, each with sides of {g(L / n)} cm. (a) Calculate the surface area of the large cube. (b) Calculate the total surface area of all the small cubes. (c) Explain how this affects the rate of reaction with acid.'
    a = f'(a) {A1} cm² (b) {n ** 3} × 6 × {g(L / n)}² = {g(A2)} cm² ({n} times larger) (c) Larger surface area exposes more particles, so collisions are more frequent and the reaction is faster.'
    k = f'(a) {A1} [1] (b) {g(A2)} cm² [1] (c) more collisions / faster [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k.replace('(b) ', '(b) method [1]; ') + ' [4]', 'multi_step')
    return Q(s3 + ' (d) State whether the total volume of gas produced changes, and explain.', a + ' (d) No: the mass of calcium carbonate is the same, so the same amount of gas forms, just faster.', k.replace('(b) ', '(b) method [1]; ') + ' (d) [1] [5]', 'multi_step')


@t82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t82_times(r, D):
    V = r.choice([40, 50, 60, 80, 100])
    tl = r.choice([180, 200, 240, 300])
    ts = r.choice([90, 100, 120, 150])
    tp = r.choice([20, 25, 30, 40])
    p = person(r)
    s = f'{p} reacts 5 g of calcium carbonate with excess acid and times how long it takes to collect {V} cm³ of carbon dioxide: large lumps {tl} s, small chips {ts} s, powder {tp} s.'
    if D <= 1:
        return mq(r, s + ' Which form has the largest surface area?', 'powder', ['large lumps', 'small chips', 'they all have the same surface area'], 'Fastest reaction (shortest time) = largest surface area: powder.')
    rl, rp = V / tl, V / tp
    if D == 2:
        return Q(s + ' Calculate the mean rate of reaction for the lumps and for the powder.', f'{g(rl)} cm³/s and {g(rp)} cm³/s', f'{V} ÷ {tl} = {g(rl)} [1]; {V} ÷ {tp} = {g(rp)} cm³/s [1] [2]')
    s3 = s + ' (a) Calculate the mean rate for each form. (b) Calculate how many times faster the powder reacts than the lumps. (c) Explain the results using the particle model.'
    a = f'(a) lumps {g(rl)}, chips {g(V / ts)}, powder {g(rp)} cm³/s (b) {g(rp / rl)} times (c) The powder has the largest surface area, so more particles are exposed and collisions with acid particles are more frequent.'
    k = '(a) all three rates [1] (b) ' + f'{g(rp / rl)} [1] (c) surface area → more frequent collisions [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Name two variables kept constant.', a + ' (d) Mass of calcium carbonate, volume, concentration and temperature of the acid (any two).', k + ' (d) two variables [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Name two variables kept constant. (e) Suggest why the powder result is the least accurate.', a + ' (d) Mass, acid volume and concentration, temperature. (e) The time is short, so reaction-time errors in starting and stopping the clock are a larger fraction of it.',
             k + ' (d) [1] (e) short time / timing error [1] [5]', 'multi_step')


def _sa_c4(r, D):
    c = city(r)
    intro = r.choice([f'A factory in {c} makes a fizzy indigestion remedy. The engineers must decide whether to sell it as a powder, as granules or as whole tablets.',
                      f'In a flour mill in {c}, a safety officer warns that fine flour dust in the air could explode.', f'{person(r)} compares how quickly whole and crushed antacid tablets react with dilute acid.'])
    parts = [
        lambda r: ('Explain why the powder form reacts fastest.', 'It has the largest surface area, so more particles are exposed for collisions.', 'surface area [1]; more frequent collisions [1] [2]'),
        lambda r: ('Describe an experiment to compare the rates for the different forms.', 'Add the same mass of each form to the same volume and concentration of acid at the same temperature; measure the gas volume (or mass loss) at regular intervals.', 'same mass / acid / temperature [1]; measure gas or mass over time [1]; compare rates [1] [3]'),
        lambda r: ('Explain why fine dust burns much faster than a solid block of the same material.', 'Dust has a huge surface area in contact with oxygen, so combustion is extremely fast and can be explosive.', 'huge surface area [1]; very fast combustion [1] [2]'),
        lambda r: ('Suggest one advantage and one disadvantage of a fast-acting powder.', 'Advantage: relieves symptoms quickly. Disadvantage: harder to measure a dose, may fizz over, absorbs moisture from air.', 'advantage [1]; disadvantage [1] [2]'),
        lambda r: ('Explain whether the total volume of gas produced depends on the form used.', 'No: the same mass contains the same amount of reactant, so the total is the same; only the rate changes.', 'same total [1]; same amount of reactant [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t82.add('C4', (2, 3, 4, 5), 'multi_step')(_sa_c4)

N83 = 'Temperature and the rate of reaction: particle collisions'
t83 = topic(N83, N83.lower(), 'temperature and the rate of reaction', 'particle collisions')
FX(t83, 'C1', (1, 2), [
    ('What happens to the rate of most reactions when the temperature is increased?', 'It increases', 'Particles move faster and collide more often and with more energy.', ['It decreases', 'It stays the same', 'The reaction stops']),
    ('Why do particles collide more often at a higher temperature?', 'They move faster', 'More kinetic energy → faster movement → more frequent collisions.', ['They become larger', 'They become heavier', 'There are more particles']),
    ('For a reaction to happen, particles must', 'collide with enough energy', 'Only collisions with enough energy are successful.', ['be the same colour', 'be stationary', 'be at room temperature']),
    ('Food is kept in a fridge because', 'reactions that spoil food are slower at low temperature', 'Lower temperature slows the reactions of decay microorganisms.', ['cold kills all bacteria instantly', 'cold adds nutrients', 'light is blocked']),
    ('As a rough rule, a 10 °C rise in temperature makes many reactions go about', 'twice as fast', 'Rate approximately doubles per 10 °C rise.', ['ten times as fast', 'half as fast', 'at the same speed']),
    ('Give two reasons why reactions are faster at higher temperatures.', 'Particles collide more often; more collisions have enough energy to react.', 'more frequent collisions [1]; more energetic / successful collisions [1] [2]'),
])
FX(t83, 'C2', (1, 2, 3), [
    ('Explain, in terms of particles, why magnesium reacts faster with warm acid than with cold acid.', 'At a higher temperature the acid particles move faster, so they collide with the magnesium more often and more collisions have enough energy to react.', 'faster particles / more frequent collisions [1]; more energetic collisions [1] [2]'),
    ('Explain why food cooks faster in a pressure cooker, where water boils at about 120 °C.', 'The higher temperature makes the cooking reactions faster.', 'higher temperature [1]; faster reactions [1] [2]'),
    ('Explain why a reaction mixture is placed in a water bath during a rate investigation.', 'To keep the temperature constant, because temperature affects the rate.', 'constant temperature [1]; temperature affects rate [1] [2]'),
    ('Explain why the disappearing cross experiment uses the same depth of solution each time.', 'The time for the cross to disappear depends on how much liquid it is viewed through; same depth keeps it a fair test.', 'depth affects visibility [1]; fair test [1] [2]'),
    ('Explain why a reaction that is safe at 20 °C may become dangerous if heated strongly.', 'The rate increases a lot, so gas or heat may be produced too fast to control.', 'rate increases greatly [1]; gas/heat released too fast [1] [2]'),
])
misc(t83, 'C2', (2, 3, 4), [
    ('Heating speeds up reactions because the particles get bigger.', 'Particles do not change size; they move faster, colliding more often and with more energy.', 'size unchanged [1]; faster particles / collisions [1] [2]'),
    ('Raising the temperature increases the amount of product made.', 'It increases the rate; the amount of product depends on the amount of reactants.', 'rate not amount [1]; amount set by reactants [1] [2]'),
])


@t83.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t83_cross(r, D):
    t20 = r.choice([120, 140, 160, 180, 200])
    temps = [20, 30, 40, 50, 60]
    times = [round(t20 / 2 ** ((T - 20) / 10) * r.choice([0.95, 1, 1.05])) for T in temps]
    p = person(r)
    tab = ', '.join(f'{T} °C: {t} s' for T, t in zip(temps, times))
    s = f'{p} mixes sodium thiosulfate solution with dilute hydrochloric acid in a flask over a cross drawn on paper and times how long it takes for the cross to disappear: {tab}.'
    if D <= 1:
        return mq(r, s + ' At which temperature is the reaction fastest?', '60 °C', ['20 °C', '30 °C', '40 °C', '50 °C'], 'Shortest time = fastest rate.')
    i = r.randrange(5)
    rt = 1000 / times[i]
    if D == 2:
        return Q(s + f' The relative rate is found as 1000 ÷ time taken. Calculate the relative rate at {temps[i]} °C.', f'{g(rt)}', f'1000 ÷ {times[i]} [1] = {g(rt)} [1] [2]')
    s3 = s + ' (a) Describe the relationship between temperature and the time taken. (b) Explain why the cross disappears. (c) Explain the effect of temperature using the particle model.'
    a = '(a) As temperature increases, the time decreases (roughly halving for every 10 °C rise), so the rate increases. (b) A yellow precipitate of sulfur forms and makes the mixture cloudy. (c) Particles move faster, so they collide more often and more collisions have enough energy to react.'
    k = '(a) higher temperature, shorter time [1] (b) precipitate / sulfur [1] (c) faster particles, more frequent and energetic collisions [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Predict the time at 70 °C.', a + f' (d) about {round(times[-1] / 2)} s', k + f' (d) about {round(times[-1] / 2)} s [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Predict the time at 70 °C. (e) Suggest why the reaction is not done above 70 °C in school.', a + f' (d) about {round(times[-1] / 2)} s (e) The reaction would be too fast to time accurately, and more sulfur dioxide gas (toxic) would be released.',
             k + ' (d) [1] (e) too fast to time / toxic gas [1] [5]', 'multi_step')


def _temp_c4(r, D):
    t1 = r.choice([90, 100, 120])
    T1 = r.choice([20, 25])
    T2 = T1 + 20
    t2 = round(t1 / 4)
    intro = r.choice([f'{person(r)} reacts a 3 cm length of magnesium ribbon with dilute hydrochloric acid. At {T1} °C the fizzing stops after {t1} s; at {T2} °C it stops after {t2} s.',
                      f'A food scientist in {city(r)} finds that milk goes sour in about 2 days at 20 °C but in about 8 days at 5 °C. In a separate test, magnesium reacts with acid in {t1} s at {T1} °C and in {t2} s at {T2} °C.'])
    parts = [
        lambda r: (f'Calculate how many times faster the magnesium reaction is at {T2} °C than at {T1} °C.', f'{g(t1 / t2)} times', f'{t1} ÷ {t2} [1] = {g(t1 / t2)} [1] [2]'),
        lambda r: ('Explain the effect of temperature on rate using the particle model.', 'At higher temperature particles have more kinetic energy, move faster, collide more often and more collisions have enough energy to react.', 'faster particles [1]; more frequent collisions [1]; more collisions with enough energy [1] [3]'),
        lambda r: ('Describe how to keep the temperature constant during each test.', 'Stand the flask in a thermostatically controlled water bath and check with a thermometer.', 'water bath [1]; thermometer check [1] [2]'),
        lambda r: ('State two other variables that must be kept the same.', 'Length (mass) of magnesium, volume and concentration of acid.', 'two variables [1] each [2]'),
        lambda r: ('Explain why food lasts longer in a refrigerator.', 'Low temperature slows the reactions (of microorganisms and enzymes) that spoil food.', 'low temperature [1]; slower reactions [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t83.add('C4', (2, 3, 4, 5), 'multi_step')(_temp_c4)
t83.add('C3', (3, 4), 'multi_step')(_temp_c4)

N84 = 'Concentration and the rate of reaction'
t84 = topic(N84, N84.lower(), 'concentration')
FX(t84, 'C1', (1, 2), [
    ('What happens to the rate of reaction when the concentration of an acid is increased?', 'It increases', 'More acid particles in the same volume → more frequent collisions.', ['It decreases', 'It stays the same', 'The reaction stops']),
    ('A more concentrated solution has', 'more particles in the same volume', 'Concentration = amount of solute per unit volume.', ['bigger particles', 'faster particles at the same temperature', 'fewer particles in the same volume']),
    ('Why does concentrated acid react faster with magnesium than dilute acid?', 'Acid particles collide with the magnesium more often', 'Higher concentration → higher collision frequency.', ['The acid particles are hotter', 'The magnesium is larger', 'The acid particles are heavier']),
    ('20 cm³ of acid is mixed with 20 cm³ of water. What happens to the concentration?', 'It halves', 'Same amount of acid in twice the volume.', ['It doubles', 'It stays the same', 'It becomes zero']),
    ('Which change would NOT increase the rate of reaction between marble and acid?', 'Using more dilute acid', 'Diluting lowers the concentration and slows the reaction.', ['Using more concentrated acid', 'Warming the acid', 'Using marble powder']),
    ('State how increasing concentration affects the frequency of collisions.', 'It increases the frequency of collisions (more collisions per second).', 'more frequent collisions [1]'),
])
FX(t84, 'C2', (1, 2, 3), [
    ('Explain, in terms of particles, why marble chips react faster in more concentrated acid.', 'There are more acid particles in the same volume, so they collide with the marble surface more often.', 'more particles per volume [1]; more frequent collisions [1] [2]'),
    ('Explain why diluting acid with water slows its reaction with magnesium.', 'The acid particles are more spread out, so collisions with magnesium are less frequent.', 'particles more spread out [1]; fewer collisions [1] [2]'),
    ('Explain why the total volume of water plus acid is kept the same when making different concentrations.', 'So that only the concentration changes; a different total volume would change the amount of acid or the depth.', 'only concentration varies [1]; fair test [1] [2]'),
    ('Explain why a reaction between marble and acid slows down even though the marble is in excess.', 'The acid is used up, so its concentration falls and collisions become less frequent.', 'acid concentration falls [1]; fewer collisions [1] [2]'),
    ('Explain why concentrated acids are more hazardous than dilute ones.', 'They react faster and more vigorously with skin and materials, causing more damage more quickly.', 'faster reaction [1]; more damage [1] [2]'),
])
misc(t84, 'C2', (2, 3, 4), [
    ('Concentrated acid reacts faster because its particles move faster.', 'At the same temperature the particles move at the same speed; there are simply more of them in each cm³, so collisions are more frequent.', 'same speed at same temperature [1]; more particles per volume [1] [2]'),
    ('Doubling the concentration doubles the total volume of gas, even if the acid is in excess.', 'If the acid is in excess, the total gas depends on the other reactant; concentration changes only the rate.', 'total set by limiting reactant [1]; rate changes [1] [2]'),
])


@t84.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t84_dil(r, D):
    tot = r.choice([40, 50, 100])
    acid_vols = {40: [40, 30, 20, 10], 50: [50, 40, 30, 20, 10], 100: [100, 80, 60, 40, 20]}[tot]
    c0 = r.choice([1.0, 2.0, 0.5])
    p = person(r)
    av = r.choice(acid_vols[1:])
    w = tot - av
    c = c0 * av / tot
    s = f'{p} has hydrochloric acid of concentration {g(c0)} mol/dm³. To make weaker solutions, the acid is mixed with water so that the total volume is always {tot} cm³.'
    if D <= 1:
        return numq(r, D, s + f' {av} cm³ of acid is mixed with {w} cm³ of water.', 'concentration of the new solution', c, ' mol/dm³', f'{g(c0)} × {av}/{tot}', [c0 * w / tot, c0, c0 * tot / av])
    if D == 2:
        return Q(s + f' Calculate the volume of water needed with {av} cm³ of acid, and the new concentration.', f'{w} cm³ of water; {g(c)} mol/dm³', f'{tot} − {av} = {w} cm³ [1]; {g(c0)} × {av} ÷ {tot} = {g(c)} mol/dm³ [1] [2]')
    b0 = r.choice([24, 28, 30, 32])
    times = [round(b0 * tot / v * r.choice([0.97, 1, 1.03])) for v in acid_vols]
    tab = ', '.join(f'{v} cm³ acid + {tot - v} cm³ water: {t} s' for v, t in zip(acid_vols, times))
    s3 = s + f' A 2 cm strip of magnesium is added to each mixture and the time for fizzing to stop is recorded: {tab}. (a) Calculate the concentration of the mixture with {av} cm³ of acid. (b) Describe the pattern in the results. (c) Explain the pattern using the particle model.'
    a = f'(a) {g(c)} mol/dm³ (b) The more concentrated the acid, the shorter the time (faster reaction). (c) More acid particles per cm³ collide with the magnesium more often.'
    k = f'(a) {g(c)} [1] (b) higher concentration, shorter time [1] (c) more frequent collisions [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Explain why the total volume is kept constant.', a + ' (d) So only the concentration changes; it is a fair test.', k + ' (d) fair test [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Explain why the total volume is kept constant. (e) Calculate the mean rate as 1000 ÷ time for the most concentrated mixture.', a + f' (d) Fair test. (e) 1000 ÷ {times[0]} = {g(1000 / times[0])}',
             k + f' (d) [1] (e) {g(1000 / times[0])} [1] [5]', 'multi_step')


def _conc_c4(r, D):
    c1 = r.choice([0.5, 1.0])
    c2 = c1 * 2
    t1 = r.choice([80, 96, 120, 144])
    t2 = t1 // 2
    V = r.choice([30, 40, 50, 60])
    intro = r.choice([f'{person(r)} reacts marble chips with hydrochloric acid of two concentrations. With {g(c1)} mol/dm³ acid it takes {t1} s to collect {V} cm³ of gas; with {g(c2)} mol/dm³ acid it takes {t2} s.',
                      f'A technician in {city(r)} compares two bottles of acid, {g(c1)} mol/dm³ and {g(c2)} mol/dm³. Using the same marble chips, {V} cm³ of carbon dioxide is collected in {t1} s and {t2} s respectively.'])
    parts = [
        lambda r: ('Calculate the mean rate for each concentration.', f'{g(V / t1)} cm³/s and {g(V / t2)} cm³/s', f'{V} ÷ {t1} = {g(V / t1)} [1]; {V} ÷ {t2} = {g(V / t2)} [1] [2]'),
        lambda r: ('Describe the relationship between concentration and rate shown.', 'Doubling the concentration doubles the rate (rate is proportional to concentration here).', 'doubling conc doubles rate [1]'),
        lambda r: ('Explain the result in terms of particles.', 'The more concentrated acid has twice as many acid particles per cm³, so collisions with the marble are twice as frequent.', 'more particles per volume [1]; more frequent collisions [1] [2]'),
        lambda r: ('State two variables that must be controlled.', 'Mass and size of marble chips, volume of acid, temperature (any two).', 'two variables [1] each [2]'),
        lambda r: ('Sketch or describe the graph of volume against time for both concentrations if the marble is in excess.', 'Both curves start at zero; the higher concentration curve is steeper and levels off sooner; the higher concentration gives twice the final volume because more acid is present.', 'steeper for higher conc [1]; final volumes reflect acid amount [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t84.add('C4', (2, 3, 4, 5), 'multi_step')(_conc_c4)
CHAPTERS[8] = [t81, t82, t83, t84]

# =========================================================== 9 Electricity
N91 = 'Parallel circuits and drawing circuit diagrams'
t91 = topic(N91, N91.lower(), 'parallel circuits', 'circuit diagrams')
FX(t91, 'C1', (1, 2), [
    ('What is a parallel circuit?', 'A circuit with more than one path (branch) for the current', 'Components are on separate branches.', ['A circuit with only one path for the current', 'A circuit with no cells', 'A circuit with only one component']),
    ('How is an ammeter connected in a circuit?', 'In series with the component', 'The current must pass through the ammeter.', ['In parallel with the component', 'Across the cell only', 'It is not connected']),
    ('How is a voltmeter connected to measure the voltage across a lamp?', 'In parallel with the lamp', 'A voltmeter is connected across the component.', ['In series with the lamp', 'Between two cells', 'In the main circuit only']),
    ('In a parallel circuit of two lamps, one lamp breaks. What happens to the other lamp?', 'It stays lit', 'It is on a separate complete branch.', ['It goes out', 'It gets brighter then explodes', 'It flickers on and off']),
    ('Why are the lights in a house wired in parallel?', 'Each light can be switched on and off independently', 'Each branch has its own switch and full voltage.', ['So they all go off together', 'To use less wire', 'So the current is the same in all of them']),
    ('Which symbol in a circuit diagram represents a cell?', 'A long thin line and a short thick line side by side', 'The longer line is the positive terminal.', ['A circle with a cross inside', 'A rectangle', 'A circle with an A inside']),
    ('What does a circle containing the letter V represent in a circuit diagram?', 'A voltmeter', 'V = voltmeter; A = ammeter.', ['An ammeter', 'A lamp', 'A switch']),
    ('State two advantages of connecting lamps in parallel rather than in series.', 'If one lamp breaks the others stay on; each lamp can be switched separately; each lamp gets the full supply voltage so is brighter.', 'any two [1] each [2]'),
])
FX(t91, 'C2', (1, 2, 3), [
    ('Explain why two lamps in parallel are brighter than the same two lamps in series with the same battery.', 'In parallel each lamp gets the full battery voltage; in series the voltage is shared, so each lamp gets less.', 'full voltage in parallel [1]; shared in series [1] [2]'),
    ('Explain why a switch in the main part of a parallel circuit turns off all the lamps.', 'All the current passes through the main part; opening the switch breaks the circuit for every branch.', 'all current through main part [1]; every branch broken [1] [2]'),
    ('Explain why a switch on one branch of a parallel circuit controls only the lamp on that branch.', 'Opening it breaks only that branch; the other branches still form complete circuits with the cell.', 'breaks only that branch [1]; others complete [1] [2]'),
    ('Explain why circuit diagrams use standard symbols.', 'So that anyone anywhere can read and build the circuit without confusion.', 'universally understood [1]; clear / no confusion [1] [2]'),
    ('Explain why an ammeter must have a very low resistance.', 'It is in series, so a high resistance would reduce the current it is measuring.', 'in series [1]; would reduce current [1] [2]'),
])
misc(t91, 'C2', (2, 3, 4), [
    ('In a parallel circuit, the lamp closest to the cell gets the electricity first and is brightest.', 'Identical lamps in parallel each get the full supply voltage and are equally bright; position does not matter.', 'equal brightness [1]; same voltage across each branch [1] [2]'),
    ('A voltmeter should be connected in series so the current can flow through it.', 'A voltmeter is connected in parallel (across) the component to measure the voltage across it.', 'voltmeter in parallel [1]; measures across component [1] [2]'),
])


@t91.add('C2', (1, 2, 3, 4))
def t91_switch(r, D):
    lamps = r.choice([['P', 'Q'], ['P', 'Q', 'R']])
    br = r.choice(lamps)
    s1 = r.choice(['open', 'closed'])
    s2 = r.choice(['open', 'closed'])
    desc = f'A cell is connected to {len(lamps)} lamps, {", ".join(lamps[:-1])} and {lamps[-1]}, each on its own parallel branch. Switch S1 is in the main circuit next to the cell. Switch S2 is on the branch with lamp {br} only.'
    on = [L for L in lamps if s1 == 'closed' and (L != br or s2 == 'closed')]

    def say(ls):
        return 'No lamps are on.' if not ls else (f'Only lamp {ls[0]} is on.' if len(ls) == 1 else 'Lamps ' + ' and '.join(ls) + ' are on.')
    ans = say(on)
    if D <= 1:
        opts = sorted({say([]), say(lamps), say([x for x in lamps if x != br]), say([br]), ans})
        return mq(r, desc + f' S1 is {s1} and S2 is {s2}. Which lamps are on?', ans, opts, f'S1 controls all lamps; S2 controls only {br}.')
    why = 'S1 is open, so the main circuit is broken and no current flows in any branch.' if s1 == 'open' else (f'S1 is closed; S2 is open so only the branch with {br} is broken.' if s2 == 'open' else 'Both switches are closed, so every branch is a complete circuit.')
    return Q(desc + f' S1 is {s1} and S2 is {s2}. State which lamps are on and explain why.', ans + ' ' + why, 'correct lamps [1]; explanation [1]' + (' [2]' if D <= 2 else '; S1 controls all, S2 only its branch [1] [3]'), 'explain')


@t91.add('C3', (1, 2, 3, 4, 5))
def t91_design(r, D):
    n = r.choice([2, 3])
    use = r.choice(['a model house with a light in each room', 'the lights on a bicycle (front and back)', 'the headlamps of a toy car', 'a set of decorative lights for a festival'])
    s = f'{person(r)} is designing the circuit for {use}, using a battery, {n} lamps and switches.'
    if D <= 1:
        return mq(r, s + ' Which arrangement lets each lamp be switched on and off separately?', 'Lamps in parallel, each with its own switch', ['Lamps in series with one switch', 'Lamps in series with a switch between each pair', 'Lamps in parallel with one switch in the main circuit only'], 'Each parallel branch with its own switch is independent.')
    s2 = s + ' Describe the circuit, including where the switches go, so that each lamp can be controlled separately and all lamps can be turned off at once.'
    a = f'Connect the {n} lamps in parallel, each branch with its own switch; put a master switch in the main circuit next to the battery.'
    k = 'lamps in parallel [1]; switch on each branch [1]'
    if D == 2:
        return Q(s2, a, k + ' [2]', 'explain')
    if D == 3:
        return Q(s2, a, k + '; master switch in main circuit [1] [3]', 'multi_step')
    s4 = s2 + ' Explain where to place an ammeter to measure the total current and a voltmeter to measure the voltage across one lamp.'
    a4 = a + ' Ammeter in series in the main circuit next to the battery; voltmeter in parallel across one lamp.'
    if D == 4:
        return Q(s4, a4, k + '; master switch [1]; meter positions [1] [4]', 'multi_step')
    return Q(s4 + ' Explain one advantage of this design over a series circuit.', a4 + ' If one lamp fails the others stay on, and each lamp gets the full battery voltage.', k + '; master switch [1]; meters [1]; advantage [1] [5]', 'multi_step')


def _par_c4(r, D):
    c = city(r)
    intro = r.choice([f'An electrician in {c} wires the lights in a new flat in parallel.', f'{person(r)} builds a circuit with a 6 V battery and three identical lamps in parallel for a school project.'])
    parts = [
        lambda r: ('Draw or describe a circuit diagram for three lamps in parallel with one switch controlling all of them.', 'Battery with a switch in the main circuit; three separate branches each containing one lamp, connected across the battery.', 'three branches [1]; switch in main circuit [1] [2]'),
        lambda r: ('Explain what happens to the other lamps if one lamp breaks.', 'They stay lit, because each is on a separate complete branch.', 'stay lit [1]; separate branches [1] [2]'),
        lambda r: ('State the voltage across each lamp if the supply is 6 V.', '6 V', 'each branch has supply voltage [1]'),
        lambda r: ('Explain why houses use parallel rather than series circuits for lighting.', 'Lights can be switched independently and one failing does not switch the others off; each gets full mains voltage.', 'independent switching [1]; one fails others stay on / full voltage [1] [2]'),
        lambda r: ('Describe how to connect an ammeter to measure the current in one lamp only.', 'Put the ammeter in series with that lamp, on its branch.', 'series [1]; on that branch [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t91.add('C4', (2, 3, 4, 5), 'multi_step')(_par_c4)
t91.add('C3', (3, 4), 'multi_step')(_par_c4)

N92 = 'Current and voltage in parallel circuits'
t92 = topic(N92, N92.lower(), 'current and voltage in parallel circuits')
FX(t92, 'C1', (1, 2), [
    ('In a parallel circuit, the current from the cell is', 'equal to the sum of the currents in the branches', 'Current splits at a junction and rejoins: I = I₁ + I₂.', ['the same in every branch', 'zero', 'always less than the current in one branch']),
    ('In a parallel circuit, the voltage across each branch is', 'the same as the supply voltage', 'Each branch is connected directly across the supply.', ['shared equally between the branches', 'always zero', 'double the supply voltage']),
    ('Two branches carry 0.2 A and 0.3 A. What is the current from the cell?', '0.5 A', '0.2 + 0.3 = 0.5 A.', ['0.1 A', '0.06 A', '0.3 A']),
    ('In a series circuit, the current is', 'the same everywhere', 'There is only one path.', ['bigger near the cell', 'shared between components', 'zero after each lamp']),
    ('What is the unit of current?', 'ampere (A)', 'Current is measured in amperes with an ammeter.', ['volt (V)', 'ohm (Ω)', 'watt (W)']),
    ('What is the unit of voltage?', 'volt (V)', 'Voltage (potential difference) is measured in volts.', ['ampere (A)', 'ohm (Ω)', 'joule (J)']),
    ('State the rule for current at a junction in a parallel circuit.', 'The current into a junction equals the total current out of it.', 'current in = current out [1]'),
])
FX(t92, 'C2', (1, 2, 3), [
    ('Explain why the current from the cell increases when another lamp is added in parallel.', 'The new branch carries its own current, and the cell current is the sum of all branch currents.', 'extra branch current [1]; total = sum [1] [2]'),
    ('Explain why identical lamps in parallel are all equally bright.', 'Each has the same voltage (the supply voltage) across it and so the same current.', 'same voltage [1]; same current / brightness [1] [2]'),
    ('Explain why a battery runs down faster when more lamps are connected in parallel.', 'The total current drawn from the battery is larger, so it transfers its energy more quickly.', 'larger total current [1]; energy transferred faster [1] [2]'),
    ('Explain why the voltage across two identical lamps in series is shared equally.', 'The supply voltage is divided between components in series; identical lamps get equal shares.', 'shared in series [1]; equal for identical lamps [1] [2]'),
    ('Explain why a lamp with a higher resistance in a parallel branch carries a smaller current.', 'All branches have the same voltage; a higher resistance allows less current for the same voltage (I = V/R).', 'same voltage [1]; I = V/R so less current [1] [2]'),
])
misc(t92, 'C2', (2, 3, 4), [
    ('Current gets used up by each lamp, so less comes back to the cell.', 'Current is not used up: the same current that leaves the cell returns to it; energy is transferred by the lamps.', 'current not used up [1]; energy transferred [1] [2]'),
    ('In a parallel circuit the voltage is shared between the branches.', 'Each branch has the full supply voltage; it is the current that is shared.', 'same voltage on each branch [1]; current shared [1] [2]'),
])


@t92.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t92_current(r, D):
    nb = 2 if D <= 3 else 3
    Is = [r.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]) for _ in range(nb)]
    V = r.choice([1.5, 3, 4.5, 6, 9, 12])
    tot = sum(Is)
    s = f'A {g(V)} V battery is connected to {nb} lamps in parallel. The currents in the branches are ' + ', '.join(f'{g(i)} A' for i in Is) + '.'
    if D <= 1:
        return numq(r, D, s, 'current from the battery', tot, ' A', ' + '.join(g(i) for i in Is), [Is[0], abs(Is[0] - Is[1]) or 0.05, Is[0] * Is[1]])
    if D == 2:
        hid = r.randrange(nb)
        s2 = f'A {g(V)} V battery is connected to two lamps in parallel. The ammeter next to the battery reads {g(tot)} A and the current in one lamp is {g(Is[1 - hid])} A.'
        return Q(s2 + ' Calculate the current in the other lamp and state the voltage across it.', f'{g(Is[hid])} A; {g(V)} V', f'{g(tot)} − {g(Is[1 - hid])} = {g(Is[hid])} A [1]; {g(V)} V (same as supply) [1] [2]')
    if D == 3:
        return Q(s + ' (a) Calculate the current from the battery. (b) State the voltage across each lamp. (c) Explain your answer to (b).', f'(a) {g(tot)} A (b) {g(V)} V (c) Each branch is connected directly across the battery.',
                 f'(a) {g(tot)} A [1] (b) {g(V)} V [1] (c) branches across supply [1] [3]', 'multi_step')
    R = [V / i for i in Is]
    j = r.randrange(nb)
    s4 = s + f' (a) Calculate the current from the battery. (b) State the voltage across each lamp. (c) Calculate the resistance of the lamp carrying {g(Is[j])} A.'
    a = f'(a) {g(tot)} A (b) {g(V)} V (c) R = V/I = {g(V)}/{g(Is[j])} = {g(R[j])} Ω'
    k = f'(a) {g(tot)} A [1] (b) {g(V)} V [1] (c) R = V/I [1] = {g(R[j])} Ω [1]'
    if D == 4:
        return Q(s4, a, k + ' [4]', 'multi_step')
    return Q(s4 + ' (d) Predict how the current from the battery changes if one lamp is removed.', a + f' (d) It falls by the current of that lamp (e.g. to {g(tot - Is[0])} A if the {g(Is[0])} A lamp is removed).', k + ' (d) falls by branch current [1] [5]', 'multi_step')


@t92.add('C3', (2, 3, 4, 5), 'numerical')
def t92_series(r, D):
    V = r.choice([3, 4.5, 6, 9, 12])
    v1 = r.choice([x for x in (1, 1.5, 2, 2.5, 3, 4, 5) if x < V])
    I = r.choice([0.1, 0.2, 0.25, 0.3, 0.5])
    s = f'A {g(V)} V battery is connected in series with two lamps, X and Y. The voltage across X is {g(v1)} V and the ammeter reads {g(I)} A.'
    if D == 2:
        return Q(s + ' State the voltage across Y and the current through Y.', f'{g(V - v1)} V; {g(I)} A', f'{g(V)} − {g(v1)} = {g(V - v1)} V [1]; same current {g(I)} A [1] [2]')
    s3 = s + f' (a) Calculate the voltage across Y. (b) State the current in Y. (c) The lamps are reconnected in parallel to the same battery. State the voltage across each lamp now.'
    a = f'(a) {g(V - v1)} V (b) {g(I)} A (c) {g(V)} V each'
    k = f'(a) {g(V - v1)} V [1] (b) {g(I)} A [1] (c) {g(V)} V [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) Explain why the lamps are brighter in parallel.', a + ' (d) Each now has the full battery voltage, so more current flows through each.', k + ' (d) more voltage / current each [1] [4]', 'multi_step')
    return Q(s3 + ' (d) Explain why the lamps are brighter in parallel. (e) Calculate the resistance of X in the series circuit.', a + f' (d) Full voltage across each. (e) R = {g(v1)}/{g(I)} = {g(v1 / I)} Ω', k + f' (d) [1] (e) {g(v1 / I)} Ω [1] [5]', 'multi_step')


def _iv_c4(r, D):
    V = r.choice([6, 9, 12])
    I1, I2 = r.sample([0.2, 0.3, 0.4, 0.5, 0.6], 2)
    intro = r.choice([f'{person(r)} connects a motor and a lamp in parallel to a {V} V battery. Ammeter A1 in the lamp branch reads {g(I1)} A and ammeter A2 in the motor branch reads {g(I2)} A.',
                      f'In a toy made in {city(r)}, a {V} V battery powers an LED unit and a buzzer in parallel. The LED branch carries {g(I1)} A and the buzzer branch {g(I2)} A.'])
    parts = [
        lambda r: ('Calculate the current drawn from the battery.', f'{g(I1 + I2)} A', f'{g(I1)} + {g(I2)} = {g(I1 + I2)} A [1]'),
        lambda r: ('State the voltage across each component and explain.', f'{V} V across each, because each branch is connected directly across the battery.', f'{V} V [1]; parallel branches across supply [1] [2]'),
        lambda r: ('Calculate the resistance of the component carrying the larger current.', f'{g(V / max(I1, I2))} Ω', f'R = V/I = {V}/{g(max(I1, I2))} [1] = {g(V / max(I1, I2))} Ω [1] [2]'),
        lambda r: ('Explain what happens to the current in the other branch if one component is disconnected.', 'It stays the same, because its branch still has the full battery voltage.', 'unchanged [1]; same voltage [1] [2]'),
        lambda r: ('Describe where to connect a voltmeter to check the voltage across one component.', 'In parallel, directly across that component.', 'in parallel across component [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t92.add('C4', (2, 3, 4, 5), 'multi_step')(_iv_c4)

N93 = 'Resistance: R = V/I and factors affecting it'
t93 = topic(N93, N93.lower(), 'resistance', 'r = v/i')
FX(t93, 'C1', (1, 2), [
    ('Which equation links resistance R, voltage V and current I?', 'R = V ÷ I', 'Resistance = voltage ÷ current.', ['R = V × I', 'R = I ÷ V', 'R = V + I']),
    ('What is the unit of resistance?', 'ohm (Ω)', '1 Ω = 1 V per A.', ['ampere (A)', 'volt (V)', 'watt (W)']),
    ('How does the resistance of a wire change if its length is doubled?', 'It doubles', 'Resistance is proportional to length.', ['It halves', 'It stays the same', 'It quadruples']),
    ('How does the resistance of a wire change if a thicker wire of the same material and length is used?', 'It decreases', 'A larger cross-sectional area gives a lower resistance.', ['It increases', 'It stays the same', 'It becomes zero']),
    ('A lamp has 6 V across it and a current of 0.5 A. What is its resistance?', '12 Ω', '6 ÷ 0.5 = 12 Ω.', ['3 Ω', '0.083 Ω', '6.5 Ω']),
    ('Which material is commonly used for connecting wires because it has a low resistance?', 'Copper', 'Copper is a very good conductor.', ['Nichrome', 'Rubber', 'Glass']),
    ('State three factors that affect the resistance of a wire.', 'Length, thickness (cross-sectional area) and material (also temperature).', 'three factors [2]; two [1] [2]'),
])
FX(t93, 'C2', (1, 2, 3), [
    ('Explain why increasing the resistance in a circuit reduces the current, if the voltage stays the same.', 'I = V/R, so with V constant a larger R gives a smaller I; the components oppose the flow of charge more.', 'I = V/R [1]; larger R smaller I [1] [2]'),
    ('Explain why a longer wire has a greater resistance.', 'The electrons collide with more metal ions along a longer path, so there is more opposition to the current.', 'longer path / more collisions [1]; more opposition [1] [2]'),
    ('Explain why a thicker wire has a lower resistance.', 'There is more space (more paths) for the electrons to flow through, so more current flows for the same voltage.', 'more paths for charge [1]; lower resistance [1] [2]'),
    ('Explain why heating elements are made from nichrome rather than copper.', 'Nichrome has a high resistance, so it heats up a lot when current flows; it also does not oxidise easily.', 'high resistance heats up [1]; resists oxidation / high melting point [1] [2]'),
    ('Describe how to measure the resistance of a wire in the laboratory.', 'Connect the wire in series with an ammeter and a cell; connect a voltmeter across the wire; read V and I and calculate R = V/I.', 'ammeter in series, voltmeter across [1]; R = V/I [1] [2]'),
])
misc(t93, 'C2', (2, 3, 4), [
    ('A thicker wire has more resistance because there is more metal in the way.', 'A thicker wire has lower resistance, because there are more paths for the charge to flow.', 'thicker = lower R [1]; more paths [1] [2]'),
    ('Resistance is the same thing as current.', 'Resistance is the opposition to current, measured in ohms; current is the flow of charge, measured in amperes.', 'distinct definitions [1]; units [1] [2]'),
])
relation(t93, 'C2', (2, 3, 4), 'resistance ∝ length / area', 'resistance', {'length': 1, 'cross-sectional area': -1},
         ['A student tests a nichrome wire in a circuit.', 'An engineer chooses a copper cable for a house.', 'A resistance wire is used in a school experiment.', 'A wire is used as a heating element in a toaster.'])


@t93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t93_rvi(r, D):
    comp = r.choice(['lamp', 'resistor', 'heating coil', 'motor', 'buzzer', 'length of nichrome wire'])
    V = r.choice([1.5, 3, 4.5, 6, 9, 12, 230])
    I = r.choice([0.1, 0.2, 0.25, 0.3, 0.5, 0.75, 1.5, 2])
    R = V / I
    q = 'R' if D <= 1 else r.choice(['R', 'I', 'V']) if D == 2 else r.choice(['I', 'V'])
    if q == 'R':
        return numq(r, D, f'The current in a {comp} is {g(I)} A when the voltage across it is {g(V)} V.', 'resistance', R, ' Ω', f'R = V ÷ I = {g(V)} ÷ {g(I)}', [V * I, I / V, V + I])
    if q == 'I':
        if D == 2:
            return Q(f'A {comp} of resistance {g(R)} Ω has {g(V)} V across it. Calculate the current.', f'{g(I)} A', f'I = V ÷ R = {g(V)} ÷ {g(R)} [1] = {g(I)} A [1] [2]')
        mA = I * 1000
        if D == 3:
            return Q(f'A {comp} of resistance {g(R)} Ω has {g(V)} V across it. Calculate the current in milliamperes (mA).', f'{g(mA)} mA', f'I = V ÷ R [1] = {g(I)} A [1] = {g(mA)} mA [1] [3]')
        return Q(f'A {comp} of resistance {g(R)} Ω has {g(V)} V across it. (a) Calculate the current in milliamperes (mA). (b) The voltage is halved. Assuming the resistance stays the same, state the new current and explain.',
                 f'(a) {g(mA)} mA (b) {g(mA / 2)} mA, because I = V/R so the current is proportional to the voltage.', f'(a) I = V ÷ R [1] = {g(mA)} mA [1] (b) {g(mA / 2)} mA [1]; I ∝ V for constant R [1] [4]', 'multi_step')
    if D == 2:
        return Q(f'A current of {g(I)} A flows through a {comp} of resistance {g(R)} Ω. Calculate the voltage across it.', f'{g(V)} V', f'V = I × R = {g(I)} × {g(R)} [1] = {g(V)} V [1] [2]')
    I2 = I * r.choice([2, 0.5])
    return Q(f'A current of {g(I)} A flows through a {comp} of resistance {g(R)} Ω. (a) Calculate the voltage across it. (b) The voltage is changed so that the current becomes {g(I2)} A. Assuming the resistance is constant, calculate the new voltage.',
             f'(a) {g(V)} V (b) {g(I2 * R)} V', f'(a) V = IR = {g(V)} V [1] (b) V = {g(I2)} × {g(R)} [1] = {g(I2 * R)} V [1]' + (' [3]' if D == 3 else '; resistance constant so V ∝ I [1] [4]'), 'multi_step')


@t93.add('C3', (2, 3, 4, 5), 'numerical')
def t93_wire(r, D):
    L0 = r.choice([20, 25, 40, 50])
    rpc = r.choice([0.1, 0.2, 0.25, 0.4])
    Ls = [L0 * k for k in (1, 2, 3, 4)]
    V = 1.5
    Is = [V / (rpc * L) for L in Ls]
    tab = ', '.join(f'{L} cm: {g(i)} A' for L, i in zip(Ls, Is))
    s = f'{person(r)} connects different lengths of nichrome wire to a 1.5 V cell and measures the current: {tab}.'
    j = r.randrange(4)
    Rj = V / Is[j]
    if D == 2:
        return Q(s + f' Calculate the resistance of the {Ls[j]} cm length.', f'{g(Rj)} Ω', f'R = 1.5 ÷ {g(Is[j])} [1] = {g(Rj)} Ω [1] [2]')
    s3 = s + ' (a) Calculate the resistance of each length. (b) Describe the relationship between length and resistance. (c) Predict the resistance of a 100 cm length.'
    a = '(a) ' + ', '.join(f'{L} cm: {g(rpc * L)} Ω' for L in Ls) + f' (b) Resistance is directly proportional to length (doubling length doubles resistance). (c) {g(rpc * 100)} Ω'
    k = '(a) resistances [1] (b) proportional [1] (c) ' + f'{g(rpc * 100)} Ω [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3 + ' (d) State two variables that must be kept the same.', a + ' (d) Thickness and material of the wire, temperature, voltage of cell (any two).', k + ' (d) two variables [1] [4]', 'multi_step')
    return Q(s3 + ' (d) State two variables that must be kept the same. (e) Explain why the circuit should be switched off between readings.', a + ' (d) Thickness and material of wire, temperature. (e) The wire heats up, which increases its resistance and would affect later readings.',
             k + ' (d) [1] (e) heating changes resistance [1] [5]', 'multi_step')


def _res_c4(r, D):
    rows = []
    Rt = r.choice([4, 5, 8, 10, 12, 15, 20])
    for V in (1.5, 3.0, 4.5, 6.0):
        rows.append((V, V / Rt))
    tab = ', '.join(f'{g(V)} V: {g(I)} A' for V, I in rows)
    intro = r.choice([f'{person(r)} measures the current through a resistor at different voltages: {tab}.', f'A technician in {city(r)} tests a resistor and records: {tab}.'])
    parts = [
        lambda r: ('Calculate the resistance from one pair of readings.', f'{g(Rt)} Ω', f'R = V/I [1] = {g(Rt)} Ω [1] [2]'),
        lambda r: ('Describe the shape of the graph of current against voltage.', 'A straight line through the origin, showing current is proportional to voltage.', 'straight line [1]; through origin [1] [2]'),
        lambda r: ('Predict the current at 9 V.', f'{g(9 / Rt)} A', f'I = 9 ÷ {g(Rt)} = {g(9 / Rt)} A [1]'),
        lambda r: ('Draw or describe the circuit used.', 'Cell (variable supply) in series with the resistor and an ammeter; voltmeter connected in parallel across the resistor.', 'ammeter in series [1]; voltmeter in parallel [1] [2]'),
        lambda r: ('Explain why a filament lamp would not give a straight-line graph.', 'As the current increases the filament gets hotter and its resistance increases, so current rises less than proportionally.', 'filament heats [1]; resistance increases [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t93.add('C4', (2, 3, 4, 5), 'multi_step')(_res_c4)

N94 = 'Practical circuits: switches, fuses and designing circuits'
t94 = topic(N94, N94.lower(), 'practical circuits', 'fuses')
FUSES = [1, 3, 5, 13]
FX(t94, 'C1', (1, 2), [
    ('What is the purpose of a fuse?', 'To break the circuit if the current is too large', 'The fuse wire melts, cutting off the current to prevent overheating and fire.', ['To increase the current', 'To store charge', 'To measure voltage']),
    ('What happens inside a fuse when the current is too large?', 'The thin wire heats up and melts', 'The wire melts and breaks the circuit.', ['The wire becomes thicker', 'The fuse lights up', 'The current reverses']),
    ('Where is a fuse placed in a circuit?', 'In series with the appliance', 'All the current must pass through the fuse.', ['In parallel with the appliance', 'Across the battery terminals', 'Anywhere outside the circuit']),
    ('Two switches are connected in series with a lamp. When does the lamp light?', 'Only when both switches are closed', 'Series switches: both must be closed (AND).', ['When either switch is closed', 'When both switches are open', 'Always']),
    ('Two switches are connected in parallel with each other, in series with a lamp. When does the lamp light?', 'When either switch (or both) is closed', 'Parallel switches: either completes the circuit (OR).', ['Only when both are closed', 'Never', 'Only when both are open']),
    ('What is an advantage of a circuit breaker over a fuse?', 'It can be reset instead of replaced', 'A circuit breaker switches off and can be reset.', ['It costs less', 'It allows a larger current always', 'It needs no wiring']),
    ('State why a fuse with too high a rating should not be used.', 'It would not melt if a dangerous current flowed, so wires could overheat and cause a fire.', 'would not melt in a fault [1]; overheating / fire risk [1] [2]'),
])
FX(t94, 'C2', (1, 2, 3), [
    ('Explain how a fuse protects an appliance and its wiring.', 'If a fault causes a large current, the fuse wire heats and melts, breaking the circuit before the wires overheat.', 'large current melts fuse [1]; circuit broken before overheating [1] [2]'),
    ('Explain why a fuse rating should be just above the normal working current.', 'So it does not melt in normal use but melts quickly if the current rises in a fault.', 'not melt normally [1]; melts in fault [1] [2]'),
    ('Explain how a two-way switch system lets a stair light be switched from the top or the bottom of the stairs.', 'Each switch can connect the lamp to either of two wires; changing either switch completes or breaks the circuit.', 'either switch changes the circuit [1]; completes or breaks path [1] [2]'),
    ('Explain why safety machines such as paper guillotines need two buttons pressed at the same time.', 'The buttons are in series, so the machine works only when both are pressed; the operator’s hands are kept away from the blade.', 'series switches [1]; both hands away from blade [1] [2]'),
    ('Explain why the fuse is placed in the live wire.', 'If it melts, the appliance is disconnected from the high voltage, so it is safe to touch.', 'disconnects live voltage [1]; appliance safe [1] [2]'),
])
misc(t94, 'C2', (2, 3, 4), [
    ('If a fuse keeps blowing, I should replace it with a bigger one.', 'A blowing fuse shows a fault or too much current; a bigger fuse would not protect the wires and could cause a fire. Find and fix the fault.', 'fuse indicates fault [1]; larger fuse unsafe [1] [2]'),
    ('A fuse works by making the current smaller.', 'A fuse does not reduce the current; it melts and breaks the circuit if the current becomes too large.', 'does not reduce current [1]; melts to break circuit [1] [2]'),
])


@t94.add('C3', (1, 2, 3, 4, 5))
def t94_fuse(r, D):
    V = 230
    R = r.choice([20, 25, 46, 60, 92, 115, 230, 460])
    I = V / R
    app = r.choice(['kettle', 'fan heater', 'electric oven'] if I >= 8 else ['hair dryer', 'toaster', 'steam iron', 'microwave oven'] if I >= 2 else ['table lamp', 'television', 'laptop charger', 'radio'])
    fuse = next((f for f in FUSES if f > I), None)
    if fuse is None:
        return None
    if D <= 1:
        return mq(r, f'A {app} normally takes a current of {g(I)} A. Which fuse should be fitted?', f'{fuse} A', [f'{f} A' for f in FUSES if f != fuse] + ['30 A'], f'Choose the smallest fuse rating above the normal current: {fuse} A.')
    if D == 2:
        return Q(f'A {app} normally takes a current of {g(I)} A. Fuses of 1 A, 3 A, 5 A and 13 A are available. Choose the best fuse and explain your choice.', f'{fuse} A: it is the smallest rating above {g(I)} A, so it will not blow in normal use but will blow in a fault.',
                 f'{fuse} A [1]; just above normal current [1] [2]')
    s = f'A {app} connected to the {V} V mains has a resistance of {g(R)} Ω when working. Fuses of 1 A, 3 A, 5 A and 13 A are available.'
    s3 = s + ' (a) Calculate the current in the appliance. (b) Choose the most suitable fuse. (c) Explain why a fuse of a much higher rating should not be used.'
    a = f'(a) I = V/R = {V}/{g(R)} = {g(I)} A (b) {fuse} A (c) It would not melt if a fault caused too large a current, so the cable could overheat and start a fire.'
    k = f'(a) {g(I)} A [1] (b) {fuse} A [1] (c) would not blow / fire risk [1]'
    if D == 3:
        return Q(s3, a, k + ' [3]', 'multi_step')
    if D == 4:
        return Q(s3, a, k.replace('(a) ', '(a) I = V/R [1]; ') + ' [4]', 'multi_step')
    return Q(s3 + ' (d) Suggest one advantage of using a circuit breaker instead.', a + ' (d) It can be reset after a fault and acts faster.', k.replace('(a) ', '(a) I = V/R [1]; ') + ' (d) reset / faster [1] [5]', 'multi_step')


@t94.add('C2', (1, 2, 3, 4))
def t94_logic(r, D):
    ctx = r.choice([('a car’s interior light that comes on when either front door is opened', 'parallel'), ('a machine that runs only when the guard is closed and the start button is pressed', 'series'),
                    ('a doorbell that can be rung from the front door or the back door', 'parallel'), ('a bank vault alarm that sounds only if both of two sensors are triggered', 'series'),
                    ('a fan in a bathroom that runs if the light switch or a humidity switch is on', 'parallel'), ('a lift that moves only when both the inner and outer doors are shut', 'series')])
    use, how = ctx
    if D <= 1:
        return mq(r, f'How should two switches be connected for {use}?', f'In {how} with each other', ['In series with each other', 'In parallel with each other', 'One switch is enough', 'With no cell in the circuit'],
                  'Either switch → parallel (OR); both switches → series (AND).')
    return Q(f'Describe how two switches should be connected in the circuit for {use}, and explain why.', f'In {how}: ' + ('either switch on its own completes the circuit.' if how == 'parallel' else 'the circuit is complete only when both switches are closed.'),
             f'{how} [1]; reason [1]' + (' [2]' if D <= 2 else '; describes the complete circuit with cell and device [1] [3]'), 'explain')


def _prac_c4(r, D):
    c = city(r)
    I = r.choice([0.4, 0.5, 2.0, 2.5, 4.0, 6.0])
    fuse = next(f for f in FUSES if f > I)
    intro = r.choice([f'{person(r)} designs a night light for a child’s bedroom in {c}. It should switch on from either the door or the bed, and draws {g(I)} A.',
                      f'An engineer in {c} designs a safety circuit for a workshop machine that draws {g(I)} A. The machine must run only when a safety guard is closed and the start switch is pressed.'])
    both = 'safety guard' in intro
    parts = [
        lambda r: ('Describe how the two switches should be connected and explain why.', ('In series: the machine runs only when both are closed.' if both else 'In parallel: either switch can complete the circuit.'), ('series' if both else 'parallel') + ' [1]; reason [1] [2]'),
        lambda r: ('Choose a fuse rating from 1 A, 3 A, 5 A and 13 A and explain your choice.', f'{fuse} A: the smallest rating above {g(I)} A.', f'{fuse} A [1]; just above working current [1] [2]'),
        lambda r: ('Explain how the fuse protects the user if a fault develops.', 'A fault causes a large current; the fuse wire melts and breaks the circuit, preventing overheating or electric shock.', 'fuse melts with large current [1]; circuit broken [1] [2]'),
        lambda r: ('Draw or describe a circuit diagram for the design.', 'Supply, fuse and device in series with the switch arrangement described (' + ('two switches in series' if both else 'two switches in parallel with each other') + ').', 'correct switch arrangement [1]; fuse in series [1] [2]'),
        lambda r: ('Suggest one further safety feature.', 'Use a circuit breaker, earth the metal case, or use double insulation.', 'valid feature [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t94.add('C4', (2, 3, 4, 5), 'multi_step')(_prac_c4)
t94.add('C3', (3, 4), 'multi_step')(_prac_c4)
CHAPTERS[9] = [t91, t92, t93, t94]
