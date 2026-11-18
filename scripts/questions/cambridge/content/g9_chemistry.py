"""Cambridge IGCSE Chemistry 0620 Extended (2026-28), CUP coursebook chapters 1-11 (grade 9).

Chapter order 1-11 = coursebook 1 (states of matter) ... 11 (acids and bases).
Data tables (substances, nuclides, isotopes, equations, electrolytes, bond energies, equilibria,
oxidation numbers, indicators, oxides) drive parameterised templates; compose() builds Paper 4 /
Paper 6 style structured items. Formula/equation helpers and ion tables are shared with
content/g10_chemistry.py (imported, not edited).
"""
import math
import re
from ._lib import topic, mcq, compose, sf, sci, sup, person, two_people, city, num_mcq
from .g10_chemistry import (F, E, AR, atoms, Mr, mr, g3, r3, cap, neg, CAT, AN, ACID, salt_f, salt_n, ppt_reagents,
                            EXCESS, base_name, excess_eq, ALK, neut_eq)

def mr(x):
    """Format an Mr / Ar / simple mass: 36.5, 58.5, 44."""
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else (f'{x:.2f}'.rstrip('0').rstrip('.'))


PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}


# ===================================================================== helpers
def T(name, *extra):
    """Topic named exactly as the W2 subtopic, with that name as its first keyword."""
    return topic(name, name, *extra)


def M(r, stem, correct, pool, key):
    try:
        o, a = mcq(r, correct, [p for p in pool if p != correct])
    except ValueError:
        return None
    return {'stem': stem, 'options': o, 'answer': a, 'key': key, 'marks': 1}


def NM(r, stem, val, wrong, unit, key, f=g3):
    extra = [val + 1, val + 3, val * 3, val - 1 if val > 1 else val + 5, val + 2]
    try:
        o, a = num_mcq(r, val, list(wrong) + extra, fmtf=f, unit=unit) if len({f(w) for w in wrong} - {f(val)}) < 3 else num_mcq(r, val, wrong, fmtf=f, unit=unit)
    except ValueError:
        return None
    return {'stem': stem, 'options': o, 'answer': a, 'key': key, 'marks': 1}


def Q(stem, answer, key, type=None, marks=None):
    d = {'stem': stem, 'answer': answer, 'key': key}
    if type:
        d['type'] = type
    if marks:
        d['marks'] = marks
    return d


LABS = ['a school laboratory', 'a college laboratory', 'a chemistry club', 'an IGCSE practical lesson', 'a quality-control laboratory', 'a science fair project', 'a water-testing laboratory', 'a teaching laboratory']


def lab(r):
    return r.choice(LABS)


def who(r):
    return f'{person(r)}, a student in {city(r)},'


def deg(x):
    return neg(f'{x:g}') + ' °C'


def n3(x):
    return g3(x)


VOL = 24.0  # dm³ per mole at r.t.p.
NA = 6.02e23
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def nuc(sym, A, Z):
    return f'{sup(A)}{str(Z).translate(SUB)}{sym}'


# equation parsing: '2Mg(s) + O2(g) -> 2MgO(s)'
_ST = re.compile(r'\((s|l|g|aq)\)$')


def species(tok):
    m = re.match(r'^(\d*)(.+)$', tok)
    n = int(m.group(1) or 1)
    rest = m.group(2)
    st = _ST.search(rest)
    state = st.group(1) if st else ''
    f = _ST.sub('', rest)
    return n, f, state


def parse_eq(s):
    arrow = '<=>' if '<=>' in s else '->'
    lhs, rhs = s.split(arrow)
    L = [species(x.strip()) for x in lhs.split(' + ')]
    R = [species(x.strip()) for x in rhs.split(' + ')]
    return L, R


def balanced(s):
    L, R = parse_eq(s)
    tot = lambda side: {el: sum(n * atoms(f).get(el, 0) for n, f, _ in side) for el in set(e for _, f, _ in side for e in atoms(f))}
    return tot(L) == tot(R)


def nostate(s):
    return re.sub(r'\((s|l|g|aq)\)', '', s)


def unbal(s):
    """Remove coefficients (and states)."""
    out = []
    for tok in nostate(s).split(' '):
        if tok in ('+', '->', '<=>'):
            out.append(tok)
        else:
            out.append(re.sub(r'^\d+', '', tok))
    return ' '.join(out)


def coeffs(s):
    L, R = parse_eq(s)
    return [n for n, _, _ in L + R]


# ===================================================================== Ch1 States of matter
# name, formula/description, mp, bp (°C)
SUBST = [('water', 'H2O', 0, 100), ('ethanol', 'C2H5OH', -114, 78), ('bromine', 'Br2', -7, 59), ('mercury', 'Hg', -39, 357),
         ('sodium chloride', 'NaCl', 801, 1413), ('iron', 'Fe', 1538, 2862), ('oxygen', 'O2', -218, -183), ('nitrogen', 'N2', -210, -196),
         ('sulfur', 'S', 115, 445), ('copper', 'Cu', 1085, 2562), ('aluminium', 'Al', 660, 2519), ('chlorine', 'Cl2', -101, -34),
         ('ammonia', 'NH3', -78, -33), ('methane', 'CH4', -182, -162), ('lead', 'Pb', 327, 1749), ('iodine', 'I2', 114, 184),
         ('hexane', 'C6H14', -95, 69), ('propanone', 'C3H6O', -95, 56), ('sodium', 'Na', 98, 883), ('argon', 'Ar', -189, -186),
         ('octane', 'C8H18', -57, 126), ('magnesium', 'Mg', 650, 1090), ('potassium bromide', 'KBr', 734, 1435), ('zinc', 'Zn', 420, 907)]


def state_at(Tc, mp, bp):
    if Tc < mp:
        return 'solid'
    if Tc < bp:
        return 'liquid'
    return 'gas'


PARTICLES = {
    'solid': ('closely packed in a regular arrangement (lattice)', 'vibrate about fixed positions', 'strong'),
    'liquid': ('close together but randomly arranged', 'move randomly, sliding past one another', 'weaker than in a solid'),
    'gas': ('far apart and randomly arranged', 'move rapidly and randomly in all directions', 'very weak (negligible)'),
}
PROPS = {'solid': 'fixed shape and fixed volume; cannot be compressed', 'liquid': 'fixed volume but takes the shape of its container; cannot be compressed; flows',
         'gas': 'no fixed shape or volume; fills its container; easily compressed'}


def _temp_away(r, mp, bp):
    """A temperature not too close to mp or bp."""
    for _ in range(40):
        lo, hi = min(mp - 80, -250), max(bp + 120, 30)
        Tc = r.choice(range(int(lo), int(hi), 1))
        if abs(Tc - mp) > 4 and abs(Tc - bp) > 4 and Tc >= -270:
            return Tc
    return mp - 20


def _fict(r):
    mp = r.choice(range(-150, 900, 7))
    bp = mp + r.choice(range(40, 700, 9))
    return (f'substance {r.choice("ABCDEJKLMQRXYZ")}', None, mp, bp)


t1a = T('Solids, liquids and gases: properties and the kinetic particle model', 'kinetic particle model', 'solids liquids gases')
t1a.fixed('C1', (1, 2), [
    ('Which statement describes the particles in a solid?', 'They are closely packed in a regular arrangement and vibrate about fixed positions.', 'Solid: regular lattice, particles touching, vibrate only.',
     ['They are far apart and move randomly at high speed.', 'They are close together but move randomly past one another.', 'They are closely packed in a regular arrangement and move freely past one another.']),
    ('Which property is shared by liquids and gases but not by solids?', 'They can flow and take the shape of their container.', 'Particles in liquids and gases can move past one another, so both flow.',
     ['They have a fixed volume.', 'They are easily compressed.', 'Their particles are far apart.']),
    ('Which state of matter has a fixed volume but no fixed shape?', 'liquid', 'Liquid particles are close together (fixed volume) but can move past each other (no fixed shape).', ['solid', 'gas', 'both solid and gas']),
    ('In which state are the forces of attraction between the particles weakest?', 'gas', 'Gas particles are far apart so attractive forces are negligible.', ['solid', 'liquid', 'they are equal in all three states']),
    ('Why can a gas be compressed easily?', 'There are large spaces between its particles.', 'Gas particles are far apart, so they can be pushed closer together.',
     ['Its particles are very small.', 'Its particles vibrate about fixed positions.', 'Its particles have no mass.']),
    ('Which describes the motion of the particles in a liquid?', 'They move randomly, sliding past one another.', 'Liquid particles are close together but free to move past each other.',
     ['They vibrate about fixed positions only.', 'They move rapidly in straight lines and are far apart.', 'They do not move at all.']),
    ('State two properties of a solid that can be explained by the kinetic particle model.', 'It has a fixed shape and a fixed volume (it cannot be compressed).', '1 mark each property [2]'),
    ('Name the state of matter in which the particles have the most kinetic energy at a given temperature.', 'gas', 'Gas particles move fastest / have most kinetic energy [1]'),
])
t1a.fixed('C2', (2, 3, 4), [
    ('Explain, in terms of particles, why a solid has a fixed shape.', 'The particles are held in fixed positions in a regular lattice by strong forces of attraction; they can only vibrate and cannot move past one another.', '1 mark: strong forces / fixed positions; 1 mark: particles only vibrate, cannot move past each other [2]'),
    ('Explain, using the kinetic particle model, why liquids cannot be compressed but gases can.', 'Liquid particles are already touching with almost no space between them; gas particles are far apart with large spaces, so they can be pushed closer together.', '1 mark: liquid particles close together / touching; 1 mark: gas particles far apart, spaces can be reduced [2]'),
    ('Explain why a gas spreads out to fill any container it is put in.', 'Gas particles move rapidly and randomly in all directions and the forces between them are negligible, so they spread into all the available space.', '1 mark: rapid random movement; 1 mark: negligible attractive forces [2]'),
    ('A student says, "The particles in a solid do not move." Explain why this statement is incorrect.', 'The particles in a solid vibrate about fixed positions; they have kinetic energy but cannot move from place to place.', '1 mark: particles vibrate; 1 mark: about fixed positions / do not change position [2]'),
    ('Explain why a gas has a much lower density than the same substance as a liquid.', 'In the gas the same mass of particles is spread over a much larger volume because the particles are far apart.', '1 mark: particles far apart in gas; 1 mark: same mass occupies larger volume [2]'),
    ('Compare the arrangement and the movement of the particles in a liquid and in a gas.', 'Liquid: particles close together, random arrangement, slide past each other. Gas: particles far apart, random arrangement, move rapidly in all directions.', '1 mark: liquid close/random; 1 mark: gas far apart; 1 mark: comparison of movement [3]'),
    ('Explain why the volume of a liquid stays the same when it is poured from a tall thin beaker into a wide dish.', 'The particles stay close together held by attractive forces, so the volume is fixed; they can move past one another so the shape changes to fit the container.', '1 mark: particles stay close / forces hold them; 1 mark: movement allows shape change [2]'),
])


@t1a.add('C1', (1, 2, 3))
def t1a_state(r, D):
    nm, f, mp, bp = r.choice(SUBST) if r.random() < 0.7 else _fict(r)
    Tc = _temp_away(r, mp, bp)
    st = state_at(Tc, mp, bp)
    stem = r.choice([f'The melting point of {nm} is {deg(mp)} and its boiling point is {deg(bp)}. What is the physical state of {nm} at {deg(Tc)}?',
                     f'{nm.capitalize()} melts at {deg(mp)} and boils at {deg(bp)}. In which state is it at {deg(Tc)}?',
                     f'A sample of {nm} (m.p. {deg(mp)}, b.p. {deg(bp)}) is kept at {deg(Tc)}. Which state is it in?'])
    why = f'{deg(Tc)} is below the melting point' if st == 'solid' else (f'{deg(Tc)} is between the melting point and boiling point' if st == 'liquid' else f'{deg(Tc)} is above the boiling point')
    return M(r, stem, st, ['solid', 'liquid', 'gas', 'a mixture of solid and gas'], f'{why}, so it is a {st}.')


@t1a.add('C3', (1, 2, 3, 4))
def t1a_table(r, D):
    n = 4 if D <= 2 else 5
    subs = r.sample(SUBST, n)
    Tc = r.choice([-50, -20, 0, 25, 25, 40, 70, 100, 150, 300, 500, 1000])
    rows = '; '.join(f'{s[0]}: m.p. {deg(s[2])}, b.p. {deg(s[3])}' for s in subs)
    want = r.choice(['liquid', 'solid', 'gas'])
    hits = [s[0] for s in subs if state_at(Tc, s[2], s[3]) == want]
    edge = [s for s in subs if Tc in (s[2], s[3])]
    if edge:
        return None
    if D == 1:
        if len(hits) != 1:
            return None
        return M(r, f'The table gives data for four substances. {rows}. Which substance is a {want} at {deg(Tc)}?', hits[0], [s[0] for s in subs],
                 f'A {want} at {deg(Tc)} needs ' + {'liquid': 'm.p. below and b.p. above', 'solid': 'm.p. above', 'gas': 'b.p. below'}[want] + f' {deg(Tc)}: {hits[0]}.')
    ans = '; '.join(f'{s[0]}: {state_at(Tc, s[2], s[3])}' for s in subs)
    stem = f'Data for {n} substances are shown. {rows}. Deduce the physical state of each substance at {deg(Tc)}.'
    key = f'{ans}. Solid if {deg(Tc)} < m.p.; liquid if between m.p. and b.p.; gas if > b.p. 1 mark per correct state [{n}]'
    if D >= 4:
        s = r.choice(subs)
        stem += f' State the range of temperature over which {s[0]} is a liquid and describe the movement of its particles in that range.'
        ans += f'. {cap(s[0])} is a liquid from {deg(s[2])} to {deg(s[3])}; particles move randomly, sliding past one another.'
        key = f'{ans}. 1 mark per correct state [{n}]; range [1]; movement [1]'
    return Q(stem, ans, key, 'short' if D <= 3 else 'case')


@t1a.add('C2', (2, 3, 4), 'explain')
def t1a_describe(r, D):
    nm, f, mp, bp = r.choice(SUBST)
    Tc = _temp_away(r, mp, bp)
    st = state_at(Tc, mp, bp)
    arr, mov, frc = PARTICLES[st]
    if D == 2:
        return Q(f'{nm.capitalize()} has a melting point of {deg(mp)} and a boiling point of {deg(bp)}. Describe the arrangement and movement of its particles at {deg(Tc)}.',
                 f'It is a {st}: particles are {arr} and {mov}.', f'1 mark: state ({st}) or arrangement ({arr}); 1 mark: movement ({mov}) [2]')
    return Q(f'At {deg(Tc)}, {nm} (m.p. {deg(mp)}, b.p. {deg(bp)}) is in one physical state. Identify the state, describe the arrangement, movement and attractive forces of its particles, and use these to explain one property of {nm} at this temperature.',
             f'{st.capitalize()}: particles {arr}; they {mov}; attractive forces are {frc}. Property: {PROPS[st]}.',
             f'1 mark: state; 1 mark: arrangement; 1 mark: movement' + ('; 1 mark: property linked to particles [4]' if D >= 4 else ' [3]'))


@t1a.add('C2', (2, 3))
def t1a_spot(r, D):
    errs = [('"Particles in a gas are bigger than particles in a solid."', 'The particles are the same size; in a gas they are further apart.'),
            ('"Solids expand when heated because their particles get bigger."', 'The particles vibrate more and move slightly further apart; they do not get bigger.'),
            ('"There is air between the particles in a liquid."', 'There is nothing (empty space) between particles; air is itself made of particles.'),
            ('"Liquid particles stop moving when the liquid is poured into a container."', 'Liquid particles are always moving randomly and sliding past each other.'),
            ('"Gas particles move slowly in straight lines."', 'Gas particles move rapidly and randomly, changing direction when they collide.'),
            ('"A solid has no gaps between its particles at all, so it cannot have any kinetic energy."', 'Solid particles vibrate about fixed positions, so they do have kinetic energy.'),
            ('"Particles in a liquid are far apart, which is why liquids can be poured."', 'Liquid particles are close together; liquids pour because the particles can slide past one another.')]
    s, fix = r.choice(errs)
    p = person(r)
    return Q(f'{p} writes in a revision note: {s} Identify the error and give the correct statement.', fix, '1 mark: error identified; 1 mark: correct particle explanation [2]')


def _t1a_c4(r, D):
    nm, f, mp, bp = r.choice(SUBST) if r.random() < 0.75 else _fict(r)
    T1, T2 = sorted([_temp_away(r, mp, bp) for _ in range(2)])
    p = person(r)
    intro = r.choice([f'{p} researches {nm}, which has a melting point of {deg(mp)} and a boiling point of {deg(bp)}.',
                      f'A data book in {city(r)} gives the melting point of {nm} as {deg(mp)} and its boiling point as {deg(bp)}.',
                      f'In {lab(r)}, a sealed sample of {nm} (m.p. {deg(mp)}, b.p. {deg(bp)}) is studied at different temperatures.'])
    s1, s2 = state_at(T1, mp, bp), state_at(T2, mp, bp)
    parts = [
        lambda r: (f'State the physical state of {nm} at {deg(T1)} and at {deg(T2)}.', f'{s1} at {deg(T1)}; {s2} at {deg(T2)}', '1 mark each [2]'),
        lambda r: (f'Describe the arrangement and movement of the particles at {deg(T2)}.', f'{PARTICLES[s2][0]}; {PARTICLES[s2][1]}', '1 mark arrangement; 1 mark movement [2]'),
        lambda r: (f'Describe how the motion of the particles changes as the sample is warmed from {deg(T1)} to {deg(T2)}.', 'Particles gain kinetic energy and move/vibrate faster' + ('; the arrangement changes as the substance changes state.' if s1 != s2 else '.'), '1 mark: more kinetic energy / faster; 1 mark: consequence (further apart / change of state) [2]'),
        lambda r: (f'Explain, in terms of particles, why {nm} at {deg(T2)} ' + {'solid': 'has a fixed shape.', 'liquid': 'takes the shape of its container but keeps a fixed volume.', 'gas': 'can be compressed.'}[s2],
                   {'solid': 'Strong forces hold particles in fixed positions; they only vibrate.', 'liquid': 'Particles are close together so the volume is fixed, but they move past one another so the shape changes.', 'gas': 'Particles are far apart with large spaces between them that can be reduced.'}[s2], '[2]'),
        lambda r: (f'Suggest a temperature at which {nm} would be a liquid.', f'any temperature between {deg(mp)} and {deg(bp)}, e.g. {deg(round((mp + bp) / 2))}', 'between m.p. and b.p. [1]'),
        lambda r: ('Predict whether the forces of attraction between the particles of this substance are strong or weak. Explain your answer using the data.',
                   ('Strong: the melting and boiling points are high, so much energy is needed to overcome the forces.' if bp > 300 else 'Weak: the melting and boiling points are low, so little energy is needed to overcome the forces.'), '1 mark: strong/weak; 1 mark: linked to m.p./b.p. data [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1a.add('C4', (2, 3, 4, 5), 'multi_step')(_t1a_c4)
t1a.add('C3', (3, 4, 5), 'multi_step')(_t1a_c4)


# ---------------------------------------------------------- 1.2 changes of state
PROC = {('solid', 'liquid'): ('melting', 'endothermic'), ('liquid', 'gas'): ('boiling or evaporation', 'endothermic'), ('gas', 'liquid'): ('condensation', 'exothermic'),
        ('liquid', 'solid'): ('freezing', 'exothermic'), ('solid', 'gas'): ('sublimation', 'endothermic'), ('gas', 'solid'): ('deposition (reverse sublimation)', 'exothermic')}
PROC_EX = {('solid', 'liquid'): ['ice turning to water on a warm day', 'chocolate softening in a hand', 'solder turning to liquid on a hot iron'],
           ('liquid', 'gas'): ['a puddle drying in the sun', 'water bubbling in a kettle', 'perfume spreading from an open bottle'],
           ('gas', 'liquid'): ['water droplets forming on a cold window', 'dew forming on grass at night', 'steam forming droplets on a bathroom mirror'],
           ('liquid', 'solid'): ['water turning to ice in a freezer', 'molten wax hardening on a candle', 'molten iron solidifying in a mould'],
           ('solid', 'gas'): ['solid carbon dioxide (dry ice) producing a fog', 'iodine crystals forming a purple vapour when warmed gently'],
           ('gas', 'solid'): ['frost forming on a car windscreen on a very cold night', 'iodine vapour forming crystals on a cold surface']}


def cooling_data(r, mp):
    start = mp + r.choice([20, 25, 30, 35, 40])
    s1 = r.choice([5, 6, 8, 10])
    temps = []
    t = start
    while t > mp:
        temps.append(t)
        t -= s1
    plateau = r.choice([3, 4, 5])
    temps += [mp] * plateau
    s2 = r.choice([4, 5, 6])
    for i in range(1, r.choice([3, 4]) + 1):
        temps.append(mp - s2 * i)
    return temps, plateau


CURVE_SUBS = [('stearic acid', 69), ('octadecanoic acid', 69), ('naphthalene', 80), ('paraffin wax', 56), ('salol (phenyl salicylate)', 42), ('lauric acid', 44),
              ('hexadecanol', 49), ('substance Y', 62), ('substance P', 57), ('ethanamide', 81)]


t1b = T('Changes of state: melting, boiling, evaporation, condensation and sublimation; heating and cooling curves', 'changes of state', 'heating and cooling curves', 'sublimation')
t1b.fixed('C1', (1, 2), [
    ('What is the name of the change of state from gas to liquid?', 'condensation', 'Gas → liquid is condensation; energy is released.', ['evaporation', 'sublimation', 'melting']),
    ('Which substance sublimes when it is warmed at atmospheric pressure?', 'solid carbon dioxide', 'Dry ice (solid CO₂) changes directly from solid to gas.', ['ice', 'sodium chloride', 'copper']),
    ('Which change of state releases energy to the surroundings?', 'freezing', 'Freezing and condensation are exothermic: attractive forces form.', ['melting', 'boiling', 'evaporation']),
    ('On a cooling curve, why does the temperature stay constant while a liquid freezes?', 'Energy is released as the forces of attraction between particles form.', 'Energy given out balances heat loss, so temperature is constant at the freezing point.',
     ['The particles stop moving.', 'The thermometer stops working.', 'Energy is taken in to break forces.']),
    ('Which statement about evaporation is correct?', 'It takes place only at the surface of a liquid and at temperatures below the boiling point.', 'Evaporation: surface only, any temperature; boiling: throughout the liquid at the boiling point.',
     ['It takes place throughout the liquid at the boiling point.', 'It releases energy to the surroundings.', 'It only happens to water.']),
    ('Define the term melting point.', 'The temperature at which a solid changes into a liquid (solid and liquid exist together).', '[1]'),
    ('Name the process in which a solid changes directly into a gas without becoming a liquid.', 'sublimation', '[1]'),
])
t1b.fixed('C2', (2, 3, 4), [
    ('Explain the difference between boiling and evaporation.', 'Boiling happens at a fixed temperature (the boiling point) throughout the liquid, with bubbles forming; evaporation happens only at the surface and at any temperature below the boiling point.', '1 mark: boiling at b.p. throughout liquid; 1 mark: evaporation at surface, below b.p. [2]'),
    ('Explain why the temperature stays constant while a pure solid is melting, even though it is still being heated.', 'The energy supplied is used to overcome the forces of attraction between the particles rather than to increase their kinetic energy.', '1 mark: energy overcomes attractive forces; 1 mark: not increasing kinetic energy / temperature [2]'),
    ('Explain why sweating cools the body.', 'Water in sweat evaporates; the particles that escape have the most energy, so the average kinetic energy (temperature) of what remains falls, taking energy from the skin.', '1 mark: evaporation needs energy / most energetic particles escape; 1 mark: energy taken from skin [2]'),
    ('Explain why a puddle dries faster on a warm, windy day than on a cold, still day.', 'Higher temperature gives more particles enough energy to escape from the surface; wind removes vapour so particles do not return to the liquid.', '1 mark: temperature effect; 1 mark: wind effect [2]'),
    ('Explain why melting is described as an endothermic change.', 'Energy must be taken in from the surroundings to overcome the forces of attraction holding the particles in the lattice.', '1 mark: energy taken in; 1 mark: to overcome forces between particles [2]'),
    ('Explain how a cooling curve can show that a substance is pure.', 'A pure substance freezes at a single fixed temperature, so the curve has a flat (horizontal) section; an impure substance freezes over a range so the curve slopes.', '1 mark: flat section at one temperature; 1 mark: impure freezes over a range [2]'),
    ('Describe what happens to the particles when steam condenses on a cold mirror.', 'Gas particles lose kinetic energy, slow down and move closer together; attractive forces form and they become a liquid, releasing energy.', '1 mark: lose energy / slow down; 1 mark: closer together / forces form [2]'),
])


@t1b.add('C1', (1, 2, 3))
def t1b_name(r, D):
    pair = r.choice(list(PROC))
    ex = r.choice(PROC_EX[pair])
    name, en = PROC[pair]
    corr = name
    pool = [v[0] for v in PROC.values()]
    if D >= 3:
        return M(r, f'Which row correctly names the change of state shown by {ex} and states whether it is endothermic or exothermic?', f'{name}; {en}',
                 [f'{v[0]}; {v[1]}' for k, v in PROC.items() if k != pair] + [f'{name}; {"exothermic" if en == "endothermic" else "endothermic"}'], f'{pair[0]} → {pair[1]} is {name}; it is {en}.')
    stem = r.choice([f'Which change of state takes place in this example: {ex}?', f'Name the change of state shown by {ex}. Which answer is correct?',
                     f'{person(r)} observes {ex}. Which process is this?'])
    return M(r, stem, corr, pool, f'{pair[0]} → {pair[1]} is {name}.')


@t1b.add('C3', (2, 3, 4, 5))
def t1b_curve(r, D):
    nm, mp = r.choice(CURVE_SUBS)
    temps, plat = cooling_data(r, mp)
    step = r.choice([0.5, 1, 1])
    times = [round(i * step, 1) for i in range(len(temps))]
    data = ', '.join(f'{fmt_t(t)} min: {x} °C' for t, x in zip(times, temps))
    i0 = temps.index(mp)
    tf = times[i0 + plat - 1] - times[i0]
    p = person(r)
    intro = f'{p} heats a sample of {nm} until it melts, then records the temperature as it cools. Results: {data}.'
    if D == 2:
        return Q(intro + ' Use the results to state the freezing point of the sample and the physical state(s) present at ' + f'{fmt_t(times[i0 + 1])} min.',
                 f'{mp} °C; liquid and solid together', '1 mark: freezing point; 1 mark: solid and liquid [2]', 'short')
    parts = [
        lambda r: ('State the freezing point of the sample.', f'{mp} °C', 'temperature of the flat section [1]'),
        lambda r: (f'State the physical state(s) present at {fmt_t(times[0])} min and at {fmt_t(times[i0 + 1])} min.', f'liquid; liquid and solid', '1 mark each [2]'),
        lambda r: ('Explain why the temperature stays constant for part of the experiment.', 'Energy is released as attractive forces form between particles during freezing; this balances the energy lost to the surroundings.', '1 mark: freezing / forces forming; 1 mark: energy released balances loss [2]'),
        lambda r: (f'Calculate how long the substance took to freeze completely, according to these readings.', f'about {fmt_t(tf)} min', f'{fmt_t(times[i0 + plat - 1])} − {fmt_t(times[i0])} = {fmt_t(tf)} min [1]'),
        lambda r: ('Describe how the movement of the particles changes during the first two minutes.', 'Particles lose kinetic energy and move more slowly (still sliding past each other as a liquid).', '[1]'),
        lambda r: ('Suggest how the shape of the cooling curve would differ if the sample contained an impurity.', 'Freezing would start at a lower temperature and take place over a range, so the curve would slope instead of being flat.', '1 mark: lower; 1 mark: over a range / no sharp flat section [2]'),
        lambda r: (f'Calculate the rate of cooling, in °C/min, before freezing starts.', f'{fmt_t(abs(temps[1] - temps[0]) / step)} °C/min', f'({temps[0]} − {temps[1]}) ÷ {fmt_t(step)} [1]'),
    ]
    if D <= 3:
        parts = parts[:5]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


def fmt_t(x):
    return str(int(x)) if abs(x - round(x)) < 1e-9 else f'{x:.1f}'


@t1b.add('C3', (1, 2, 3))
def t1b_heat(r, D):
    nm, f, mp, bp = r.choice(SUBST)
    seg = r.choice(['first rising section', 'first flat section', 'second rising section', 'second flat section', 'final rising section'])
    ans = {'first rising section': ('solid', 'solid warming up'), 'first flat section': ('solid and liquid', 'melting at ' + deg(mp)), 'second rising section': ('liquid', 'liquid warming up'),
           'second flat section': ('liquid and gas', 'boiling at ' + deg(bp)), 'final rising section': ('gas', 'gas warming up')}[seg]
    stem = f'A sample of {nm} is heated steadily from {deg(mp - 30)} to {deg(bp + 30)} and a heating curve is plotted. Which state(s) are present during the {seg} of the curve?'
    if D == 1:
        return M(r, stem, ans[0], ['solid', 'solid and liquid', 'liquid', 'liquid and gas', 'gas'], f'{cap(seg)}: {ans[1]}.')
    flat = ['first flat section', 'second flat section']
    return Q(stem + f' Give the temperature of the {r.choice(flat)} and explain why the temperature is constant there.',
             f'{ans[0]}; flat sections at {deg(mp)} (melting) and {deg(bp)} (boiling); energy supplied overcomes attractive forces instead of raising kinetic energy.',
             '1 mark: state(s); 1 mark: correct temperature; 1 mark: energy used to overcome forces [3]', 'short')


@t1b.add('C2', (2, 3, 4), 'explain')
def t1b_explain(r, D):
    pair = r.choice(list(PROC))
    ex = r.choice(PROC_EX[pair])
    name, en = PROC[pair]
    gain = en == 'endothermic'
    a = (f'{cap(name)}. Particles {"gain" if gain else "lose"} energy; ' + ('attractive forces are overcome and particles move further apart / more freely.' if gain else 'they slow down, move closer together and attractive forces form.'))
    return Q(f'Consider {ex}. Name the change of state and explain, in terms of particles and energy, what happens during this change.' + (' State whether the change is endothermic or exothermic.' if D >= 3 else ''),
             a + (f' It is {en}.' if D >= 3 else ''), '1 mark: name; 1 mark: energy change of particles; ' + ('1 mark: forces/arrangement; 1 mark: endo/exo [4]' if D >= 3 else '1 mark: forces/arrangement [3]'))


def _t1b_c4(r, D):
    nm, f, mp, bp = r.choice([s for s in SUBST if s[3] - s[2] > 40])
    p = person(r)
    intro = r.choice([f'{p} heats a solid sample of {nm} at a steady rate from {deg(mp - 40)} until it has all turned to gas at {deg(bp + 20)}.',
                      f'In {lab(r)}, a heating curve is plotted for {nm} (m.p. {deg(mp)}, b.p. {deg(bp)}) from {deg(mp - 40)} to {deg(bp + 20)}.'])
    parts = [
        lambda r: ('Describe the shape of the heating curve, naming the processes at each flat section.', f'rises (solid warms), flat at {deg(mp)} (melting), rises (liquid warms), flat at {deg(bp)} (boiling), rises (gas warms)', '1 mark: two flat sections; 1 mark: temperatures; 1 mark: named melting and boiling [3]'),
        lambda r: ('Explain why the flat section for boiling is usually longer than the one for melting.', 'More energy is needed to separate particles completely (overcome nearly all attractive forces) when boiling than to let them move past each other when melting.', '1 mark: more energy for boiling; 1 mark: forces overcome completely / particles separated [2]'),
        lambda r: (f'Describe the changes in the arrangement and movement of particles as the {nm} melts.', 'Particles go from a regular arrangement vibrating about fixed points to a random arrangement sliding past one another.', '1 mark arrangement; 1 mark movement [2]'),
        lambda r: (f'A second student finds that their sample melts between {deg(mp - 6)} and {deg(mp - 2)}. Suggest what this shows about their sample.', 'It is impure: impurities lower the melting point and make it melt over a range.', '1 mark: impure; 1 mark: lower / over a range [2]'),
        lambda r: ('State whether boiling is endothermic or exothermic and give a reason.', 'Endothermic: energy is taken in to overcome the attractive forces.', '[1]'),
        lambda r: (f'Explain why {nm} can evaporate at temperatures below {deg(bp)} but cannot boil.', 'Some surface particles have enough energy to escape at any temperature; boiling needs the vapour to form throughout the liquid, which only happens at the boiling point.', '1 mark: surface particles with enough energy escape; 1 mark: boiling throughout at b.p. [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1b.add('C4', (2, 3, 4, 5), 'multi_step')(_t1b_c4)


# ---------------------------------------------------------- 1.3 gas volume, temperature and pressure
GAS_CTX_T = [('a balloon is taken from a warm room into a freezer', 'decreases', 'cooled'), ('a sealed syringe of air is placed in a beaker of hot water', 'increases', 'heated'),
             ('a football is left in strong sunshine', 'increases', 'heated'), ('a weather balloon cools as it rises through the atmosphere at roughly constant pressure', 'decreases', 'cooled'),
             ('a gas syringe containing nitrogen is cooled in an ice bath', 'decreases', 'cooled'), ('a party balloon is held near a radiator', 'increases', 'heated'),
             ('a plastic bottle of air is moved from a hot car into an air-conditioned room', 'decreases', 'cooled'), ('a sample of helium in a syringe is warmed with a hair dryer', 'increases', 'heated')]
GAS_CTX_P = [('a diver releases a bubble of air deep under the sea and it rises to the surface', 'increases', 'decreases'), ('the plunger of a sealed syringe of air is pushed in', 'decreases', 'increases'),
             ('a sealed packet of crisps is taken up a high mountain', 'increases', 'decreases'), ('air is pumped into a fixed amount of gas in a cylinder with a movable piston, pressing the piston down', 'decreases', 'increases'),
             ('a weather balloon rises to a height where the air pressure is much lower', 'increases', 'decreases'), ('a gas in a syringe is squeezed by doubling the force on the plunger', 'decreases', 'increases')]
GASES = ['air', 'nitrogen', 'oxygen', 'helium', 'argon', 'carbon dioxide', 'hydrogen', 'methane']


t1c = T('Effect of temperature and pressure on the volume of a gas', 'volume of a gas', 'temperature and pressure')
t1c.fixed('C1', (1, 2), [
    ('A fixed mass of gas is heated at constant pressure. What happens to its volume?', 'It increases.', 'Particles move faster and hit the walls harder and more often, pushing them out.', ['It decreases.', 'It stays the same.', 'It becomes zero.']),
    ('The pressure on a fixed mass of gas is increased at constant temperature. What happens to its volume?', 'It decreases.', 'The particles are pushed closer together.', ['It increases.', 'It stays the same.', 'It doubles.']),
    ('What causes the pressure of a gas in a container?', 'Gas particles colliding with the walls of the container', 'Pressure comes from collisions of particles with the walls.', ['Gas particles colliding only with each other', 'The weight of the container', 'Gas particles expanding in size']),
    ('Why does a gas expand when it is heated at constant pressure?', 'Its particles move faster and collide with the walls more often and with more force.', 'Increased kinetic energy → more forceful, frequent collisions → volume increases to restore pressure.',
     ['Its particles get larger.', 'Its particles become lighter.', 'The forces between its particles become stronger.']),
    ('State what happens to the average speed of gas particles when the temperature of the gas is increased.', 'It increases.', '[1]'),
])
t1c.fixed('C2', (2, 3, 4), [
    ('Explain, in terms of particles, why the volume of a gas increases when it is heated at constant pressure.', 'Particles gain kinetic energy and move faster; they hit the walls harder and more often, so the gas pushes outwards and expands until the pressure inside equals the pressure outside.', '1 mark: particles move faster / more kinetic energy; 1 mark: more frequent / harder collisions with walls; 1 mark: gas expands [3]'),
    ('Explain, in terms of particles, why the volume of a gas decreases when the pressure on it is increased at constant temperature.', 'The particles are far apart, so they can be pushed closer together into a smaller space; the same particles then collide with the walls more often, matching the higher external pressure.', '1 mark: particles far apart can be pushed closer; 1 mark: more frequent collisions per unit area [2]'),
    ('Explain why car tyre pressures should be checked when the tyres are cold.', 'After driving the gas is warmer, its particles move faster and hit the tyre walls more often and harder, so the pressure reading is higher than the true cold value.', '1 mark: temperature raises pressure; 1 mark: particle explanation [2]'),
    ('Explain why an aerosol can must not be heated, even when it seems to be empty.', 'There is still gas inside; heating makes its particles move faster and collide with the walls more often and harder, so the pressure rises and the can may explode.', '1 mark: pressure increases; 1 mark: particles faster / more collisions [2]'),
    ('A student says, "When a gas is cooled, its particles shrink and so the volume goes down." Explain the error.', 'The particles do not change size; they move more slowly, collide with the walls less often and less hard, so the gas contracts at constant pressure.', '1 mark: particles stay same size; 1 mark: slower / fewer collisions [2]'),
    ('Explain why a gas can be compressed much more than a liquid when pressure is applied.', 'There are large spaces between gas particles that can be reduced; liquid particles are already touching.', '1 mark each [2]'),
])


@t1c.add('C1', (1, 2, 3))
def t1c_predict(r, D):
    if r.random() < 0.5:
        c, v, how = r.choice(GAS_CTX_T)
        k = f'When gas is {how} its particles move {"faster" if how == "heated" else "more slowly"} and the volume {v}.'
    else:
        c, v, how = r.choice(GAS_CTX_P)
        k = f'The pressure on the gas {how}, so the volume {v}.'
    return M(r, f'{cap(c)}. What happens to the volume of the gas inside?', f'It {v}.', ['It increases.', 'It decreases.', 'It stays the same.', 'It first increases then decreases.'], k)


@t1c.add('C2', (2, 3, 4), 'explain')
def t1c_ctx(r, D):
    if r.random() < 0.5:
        c, v, how = r.choice(GAS_CTX_T)
        a = f'The volume {v}: the gas is {how}, so its particles move {"faster" if how == "heated" else "more slowly"} and collide with the walls {"more" if how == "heated" else "less"} often and {"harder" if how == "heated" else "less hard"}' + ('; the gas expands until the pressure inside balances the pressure outside.' if how == 'heated' else '; the gas contracts.')
    else:
        c, v, how = r.choice(GAS_CTX_P)
        a = f'The volume {v}: the external pressure {how}, so the particles are ' + ('pushed closer together into a smaller space.' if how == 'increases' else 'able to spread further apart; fewer collisions are needed to balance the lower pressure.')
    lead_ = r.choice(['Predict and explain', 'Explain, in terms of particles,', 'Use the kinetic particle model to explain'])
    return Q(f'{cap(c)}. {lead_} what happens to the volume of the gas.', a,
             '1 mark: correct prediction; 1 mark: particle speed / spacing; ' + ('1 mark: collisions with walls [3]' if D >= 3 else 'total [2]'))


@t1c.add('C3', (2, 3, 4, 5))
def t1c_data(r, D):
    g = r.choice(GASES)
    V0 = r.choice([20.0, 25.0, 30.0, 40.0, 50.0, 60.0])
    T0 = r.choice([0, 10, 20])
    step = r.choice([10, 20, 25])
    Ts = [T0 + step * i for i in range(5)]
    Vs = [V0 * (t + 273) / (T0 + 273) for t in Ts]
    hide = r.choice([1, 2, 3])
    rows = ', '.join(f'{t} °C: {"?" if i == hide else sf(v, 3)} cm³' for i, (t, v) in enumerate(zip(Ts, Vs)))
    Tx = Ts[-1] + step
    Vx = V0 * (Tx + 273) / (T0 + 273)
    p = person(r)
    intro = f'{p} traps {g} in a gas syringe at constant pressure and measures its volume at different temperatures: {rows}.'
    parts = [
        lambda r: ('Describe the relationship between temperature and volume shown by the data.', 'As the temperature increases the volume increases (by equal amounts for equal temperature rises).', '1 mark: volume increases with temperature; 1 mark: steady / linear [2]'),
        lambda r: ('Estimate the missing volume.', f'{sf(Vs[hide], 3)} cm³ (accept ±0.2)', f'mid-way between neighbouring readings [1]'),
        lambda r: (f'Predict the volume at {Tx} °C.', f'{sf(Vx, 3)} cm³', f'continues the same increase of {sf(Vs[1] - Vs[0], 2)} cm³ per {step} °C [1]'),
        lambda r: ('Explain the trend in terms of particles.', 'Higher temperature → particles move faster → hit the plunger harder and more often → plunger pushed out until pressure balanced.', '1 mark: faster particles; 1 mark: more / harder collisions push plunger out [2]'),
        lambda r: ('State one variable that must be kept constant and explain why.', 'The pressure (or the amount/mass of gas, e.g. no leaks), because it also affects the volume.', '1 mark: variable; 1 mark: reason [2]'),
        lambda r: ('Suggest why the syringe plunger must move freely.', 'So that the pressure inside stays equal to atmospheric pressure (constant pressure).', '[1]'),
    ]
    if D <= 2:
        return compose(r, intro, parts[:3], k=(2,), type_='case')
    return compose(r, intro, parts, k=(3, 4) if D >= 4 else (2, 3), type_='case')


@t1c.add('C3', (2, 3, 4))
def t1c_pdata(r, D):
    g = r.choice(GASES)
    V0 = r.choice([60.0, 80.0, 96.0, 100.0, 120.0])
    P0 = r.choice([100, 100, 101])
    fs = [1, 1.25, 1.5, 2, 2.5] if r.random() < 0.5 else [1, 1.5, 2, 3, 4]
    rows = ', '.join(f'{sf(P0 * f, 3)} kPa: {sf(V0 / f, 3)} cm³' for f in fs)
    Px = P0 * fs[-1] * 2
    stem = f'A fixed mass of {g} is kept at constant temperature while the pressure on it is changed. Results: {rows}. Describe the relationship between pressure and volume shown, and predict the volume at {sf(Px, 3)} kPa.'
    a = f'As pressure increases the volume decreases; doubling the pressure halves the volume (pressure × volume is constant). At {sf(Px, 3)} kPa the volume would be {sf(V0 * P0 / Px, 3)} cm³.'
    key = '1 mark: volume decreases as pressure increases; 1 mark: inverse (doubling P halves V); 1 mark: prediction ' + sf(V0 * P0 / Px, 3) + ' cm³ [3]'
    if D >= 4:
        stem += ' Explain the trend in terms of particles.'
        a += ' The particles are pushed closer together, so they hit the walls more often per unit area.'
        key += '; particle explanation [1]'
    return Q(stem, a, key, 'case')


def _t1c_c4(r, D):
    g = r.choice(GASES)
    p = person(r)
    c, v, how = r.choice(GAS_CTX_T)
    intro = r.choice([f'{p} investigates how the volume of {g} changes. A sample is sealed in a gas syringe and placed in water baths at different temperatures, and then the plunger is pushed in at constant temperature.',
                      f'A company in {city(r)} stores {g} in cylinders and balloons for use at events. Engineers study how the gas behaves when it is heated, cooled and compressed.'])
    parts = [
        lambda r: ('Describe and explain what happens to the volume of the gas when it is heated at constant pressure.', 'Volume increases: particles gain kinetic energy, move faster and hit the walls harder and more often, pushing them out.', '1 mark: increases; 1 mark: faster particles; 1 mark: collisions with walls [3]'),
        lambda r: ('Describe and explain what happens to the volume when the pressure is increased at constant temperature.', 'Volume decreases: particles are far apart and are pushed closer together.', '1 mark: decreases; 1 mark: particles pushed closer / spaces reduced [2]'),
        lambda r: (f'Explain what happens when {c}.', f'The volume {v} because the gas is {how}; particles move {"faster" if how == "heated" else "more slowly"}.', '1 mark: prediction; 1 mark: particle reason [2]'),
        lambda r: ('Explain why a sealed rigid cylinder of gas could burst if it is left in a fire.', 'The volume cannot increase, so as particles move faster and collide with the walls more often and harder the pressure rises until the cylinder fails.', '1 mark: pressure rises at fixed volume; 1 mark: particle explanation [2]'),
        lambda r: ('Suggest why gases are stored under high pressure in cylinders.', 'A large amount (mass) of gas can be stored in a small volume because the particles can be pushed close together.', '[1]'),
        lambda r: ('State two variables that must be controlled when investigating the effect of temperature on volume.', 'pressure; mass/amount of gas (no leaks)', '1 mark each [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1c.add('C4', (2, 3, 4, 5), 'multi_step')(_t1c_c4)


# ---------------------------------------------------------- 1.4 diffusion
DGAS = [('ammonia', 'NH3'), ('hydrogen chloride', 'HCl'), ('hydrogen', 'H2'), ('helium', 'He'), ('methane', 'CH4'), ('oxygen', 'O2'), ('nitrogen', 'N2'),
        ('carbon dioxide', 'CO2'), ('chlorine', 'Cl2'), ('sulfur dioxide', 'SO2'), ('bromine', 'Br2'), ('nitrogen dioxide', 'NO2'), ('hydrogen sulfide', 'H2S'),
        ('neon', 'Ne'), ('argon', 'Ar'), ('hydrogen bromide', 'HBr'), ('fluorine', 'F2'), ('carbon monoxide', 'CO')]
AR.setdefault('He', 4)
AR.setdefault('Ne', 20)
AR.setdefault('Ar', 40)


t1d = T('Diffusion and the effect of relative molecular mass on rate of diffusion', 'diffusion', 'relative molecular mass')
t1d.fixed('C1', (1, 2), [
    ('What is meant by diffusion?', 'The net movement of particles from a region of higher concentration to a region of lower concentration as a result of their random motion', 'Diffusion: random motion causes net spreading from high to low concentration.',
     ['The movement of particles from low to high concentration', 'The dissolving of a solid in a liquid', 'The movement of particles only when a liquid is stirred']),
    ('Which gas diffuses fastest at the same temperature?', 'hydrogen', 'Lowest Mr (2) → fastest diffusion.', ['oxygen', 'carbon dioxide', 'chlorine']),
    ('In which state does diffusion happen fastest?', 'gas', 'Gas particles move fastest and are far apart.', ['solid', 'liquid', 'it is the same in all states']),
    ('Why does a purple colour spread slowly through still water when a crystal of potassium manganate(VII) is added?', 'The particles move randomly and spread from high to low concentration.', 'Diffusion due to random motion of particles.',
     ['The water particles are attracted to the crystal.', 'The crystal particles grow larger.', 'The water evaporates.']),
    ('What is the effect of increasing temperature on the rate of diffusion?', 'The rate increases because particles move faster.', 'Higher temperature → more kinetic energy → faster diffusion.', ['The rate decreases.', 'There is no effect.', 'The particles become heavier.']),
    ('State the factor relating to a gas molecule that determines how fast it diffuses at a given temperature.', 'its relative molecular mass (lower Mr diffuses faster)', '[1]'),
])
t1d.fixed('C2', (2, 3, 4), [
    ('Explain why the smell of perfume spreads across a room even when there is no draught.', 'Perfume particles evaporate and move randomly, colliding with air particles; there is a net movement from where the concentration is high to where it is low.', '1 mark: random movement; 1 mark: high to low concentration [2]'),
    ('Explain why diffusion is faster in gases than in liquids.', 'Gas particles move much faster and are far apart, so they collide less often with other particles; liquid particles are close together and move more slowly.', '1 mark: gas particles faster; 1 mark: fewer collisions / more space [2]'),
    ('Explain why ammonia diffuses faster than hydrogen chloride.', 'Ammonia has a lower relative molecular mass (17) than hydrogen chloride (36.5), so at the same temperature its molecules move faster.', '1 mark: Mr comparison; 1 mark: lighter molecules move faster [2]'),
    ('Explain why a coloured dye spreads more quickly through hot water than through cold water.', 'In hot water the particles have more kinetic energy and move faster, so they spread out more quickly.', '1 mark: more kinetic energy; 1 mark: faster movement / faster diffusion [2]'),
    ('A student says, "Diffusion stops when the particles are evenly spread out." Explain whether this is correct.', 'Particles keep moving randomly; there is no longer any net movement because the concentration is the same everywhere.', '1 mark: particles keep moving; 1 mark: no net movement [2]'),
    ('Explain why diffusion does not happen noticeably in solids.', 'Particles in a solid only vibrate about fixed positions, so they cannot move past one another.', '[2]'),
])


@t1d.add('C1', (1, 2, 3))
def t1d_fast(r, D):
    gs = r.sample(DGAS, 4)
    ms = [(Mr(f), n, f) for n, f in gs]
    if len(set(m for m, _, _ in ms)) < 4:
        return None
    want = r.choice(['fastest', 'slowest'])
    best = (min if want == 'fastest' else max)(ms)
    return M(r, f'Which of these gases diffuses {want} at room temperature: ' + ', '.join(f'{n} ({F(f)})' for _, n, f in ms) + '?', best[1], [n for _, n, _ in ms],
             'Mr: ' + ', '.join(f'{n} {mr(m)}' for m, n, _ in ms) + f'. Lower Mr → faster diffusion, so the {want} is {best[1]}.')


TUBE = [(('ammonia', 'NH3'), ('hydrogen chloride', 'HCl'), 'ammonium chloride', 'NH4Cl'), (('ammonia', 'NH3'), ('hydrogen bromide', 'HBr'), 'ammonium bromide', 'NH4Br')]


@t1d.add('C3', (2, 3, 4, 5))
def t1d_tube(r, D):
    (a, af), (b, bf), prod, pf = r.choice(TUBE)
    L = r.choice([50, 60, 80, 100, 120])
    p = person(r)
    sol_a = 'concentrated aqueous ammonia'
    sol_b = 'concentrated hydrochloric acid' if bf == 'HCl' else 'concentrated hydrobromic acid'
    ma, mb = Mr(af), Mr(bf)
    intro = f'{p} places cotton wool soaked in {sol_a} at one end of a {L} cm glass tube and cotton wool soaked in {sol_b} at the other end, then seals both ends. After a few minutes a white ring of {prod} forms inside the tube.'
    parts = [
        lambda r: (f'Calculate the relative molecular masses of {a} and {b}.', f'{F(af)} = {mr(ma)}; {F(bf)} = {mr(mb)}', '1 mark each [2]'),
        lambda r: ('State and explain which end of the tube the white ring forms nearer to.', f'Nearer the {b} end, because {a} has a lower Mr, so its molecules move faster and travel further in the same time.', '1 mark: nearer the ' + b + ' end; 1 mark: lower Mr ammonia diffuses faster [2]'),
        lambda r: ('Write a word equation and a symbol equation for the formation of the white ring.', f'{a} + {b} → {prod}; {E(f"{af}(g) + {bf}(g) -> {pf}(s)")}', '1 mark word; 1 mark symbol with states [2]'),
        lambda r: ('Explain why the tube is sealed at both ends.', 'To stop the gases escaping (and to stop air currents/draughts affecting the movement).', '[1]'),
        lambda r: ('Predict how the time taken for the ring to form would change if the tube were warmed, and explain your answer.', 'Shorter time: the particles have more kinetic energy and move faster.', '1 mark: shorter; 1 mark: particles faster [2]'),
        lambda r: (f'The experiment is repeated with a {L * 2} cm tube. Predict the effect on the time taken and on the relative position of the ring.', 'Takes longer (further to travel); the ring still forms nearer the ' + b + ' end at the same fraction of the length.', '1 mark: longer; 1 mark: same relative position [2]'),
    ]
    if D <= 2:
        return compose(r, intro, parts[:2], k=(1, 2), type_='case')
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@t1d.add('C3', (1, 2, 3, 4))
def t1d_compare(r, D):
    (n1, f1), (n2, f2) = r.sample(DGAS, 2)
    m1, m2 = Mr(f1), Mr(f2)
    if abs(m1 - m2) < 1:
        return None
    fast = n1 if m1 < m2 else n2
    els = sorted({el for f in (f1, f2) for el in atoms(f)})
    data = ', '.join(f'{el} = {mr(AR[el])}' for el in els)
    if D == 1:
        return M(r, f'Samples of {n1}, {F(f1)}, and {n2}, {F(f2)}, are released at the same time and temperature. Which statement is correct? (Ar: {data})',
                 f'{cap(fast)} diffuses faster because it has a lower Mr.', [f'{cap(n1 if fast == n2 else n2)} diffuses faster because it has a higher Mr.', 'Both diffuse at the same rate because they are both gases.',
                                                                            f'{cap(fast)} diffuses faster because its molecules are larger.', f'{cap(n1 if fast == n2 else n2)} diffuses faster because it has a lower Mr.'],
                 f'Mr({F(f1)}) = {mr(m1)}, Mr({F(f2)}) = {mr(m2)}: lower Mr → faster.')
    return Q(f'{who(r)} compares the rates of diffusion of {n1}, {F(f1)}, and {n2}, {F(f2)}, at the same temperature. Calculate the relative molecular mass of each gas and predict, with a reason, which diffuses faster. (Ar: {data})',
             f'Mr: {F(f1)} = {mr(m1)}, {F(f2)} = {mr(m2)}; {fast} diffuses faster because its molecules are lighter and move faster at the same temperature.',
             f'1 mark each Mr [2]; 1 mark: {fast}; 1 mark: lighter molecules move faster [1] total [4]' if D >= 3 else f'1 mark: Mr values; 1 mark: {fast} with reason [2]')


def _t1d_c4(r, D):
    p = person(r)
    liq = r.choice([('potassium manganate(VII)', 'purple'), ('copper(II) sulfate', 'blue'), ('a food dye', 'red'), ('ink', 'blue')])
    T1, T2 = sorted(r.sample([10, 15, 20, 30, 40, 50, 60], 2))
    t1 = r.choice([300, 360, 420, 480, 600])
    t2 = int(t1 * (T1 + 40) / (T2 + 40) // 10 * 10)
    intro = f'{p} drops a crystal of {liq[0]} into a beaker of still water at {T1} °C and times how long it takes for the {liq[1]} colour to spread evenly: {t1} s. The experiment is repeated with water at {T2} °C: {t2} s.'
    parts = [
        lambda r: ('Name the process by which the colour spreads.', 'diffusion', '[1]'),
        lambda r: ('Explain, in terms of particles, how the colour spreads through the water.', 'Particles of the solute and water move randomly and collide; there is net movement of coloured particles from high to low concentration until evenly spread.', '1 mark: random motion; 1 mark: high to low concentration [2]'),
        lambda r: ('Explain the difference between the two results.', f'At {T2} °C the particles have more kinetic energy and move faster, so diffusion is faster ({t2} s < {t1} s).', '1 mark: higher temperature faster; 1 mark: particles have more energy [2]'),
        lambda r: ('Suggest why the beaker must not be stirred or moved.', 'Stirring would mix the solution (convection), so the result would not measure diffusion alone.', '[1]'),
        lambda r: ('State two variables that should be kept the same in both experiments.', 'size/mass of crystal; volume of water (also same beaker, no stirring)', '1 mark each [2]'),
        lambda r: ('Predict, with a reason, whether ammonia gas would diffuse through air faster or slower than the coloured particles diffuse through water.', 'Faster: gas particles move faster and are further apart, so collide less often with other particles.', '1 mark: faster; 1 mark: reason [2]'),
        lambda r: ('Calculate the percentage decrease in the time taken.', f'{g3((t1 - t2) / t1 * 100)}%', f'({t1} − {t2}) / {t1} × 100 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1d.add('C4', (2, 3, 4, 5), 'multi_step')(_t1d_c4)
t1d.add('C3', (4, 5), 'multi_step')(_t1d_c4)

CHAPTERS[1] = [t1a, t1b, t1c, t1d]


# ===================================================================== Ch2 Atomic structure
CLASSIFY = {
    'element': ['oxygen', 'iron', 'sulfur', 'neon', 'copper', 'diamond', 'mercury', 'nitrogen', 'magnesium', 'chlorine', 'helium', 'aluminium', 'graphite', 'iodine'],
    'compound': ['water', 'sodium chloride', 'carbon dioxide', 'glucose', 'calcium carbonate', 'ammonia', 'methane', 'copper(II) oxide', 'ethanol', 'iron(II) sulfide', 'magnesium oxide', 'sulfuric acid (pure)'],
    'mixture': ['air', 'sea water', 'brass', 'petroleum (crude oil)', 'steel', 'orange juice', 'bronze', 'soil', 'granite', 'ink', 'a solution of salt in water', 'natural gas'],
}
FORMULA_OF = {'oxygen': 'O2', 'iron': 'Fe', 'sulfur': 'S', 'neon': 'Ne', 'copper': 'Cu', 'mercury': 'Hg', 'nitrogen': 'N2', 'magnesium': 'Mg', 'chlorine': 'Cl2', 'helium': 'He', 'aluminium': 'Al', 'iodine': 'I2',
              'water': 'H2O', 'sodium chloride': 'NaCl', 'carbon dioxide': 'CO2', 'glucose': 'C6H12O6', 'calcium carbonate': 'CaCO3', 'ammonia': 'NH3', 'methane': 'CH4', 'copper(II) oxide': 'CuO',
              'ethanol': 'C2H5OH', 'iron(II) sulfide': 'FeS', 'magnesium oxide': 'MgO'}
DEF = {'element': 'a substance made of only one type of atom', 'compound': 'two or more elements chemically combined in a fixed ratio', 'mixture': 'two or more substances not chemically combined'}
BOX = [('identical molecules, each made of two atoms of the same kind', 'element'), ('separate single atoms, all of the same kind', 'element'),
       ('identical molecules, each made of one atom of one kind joined to two atoms of another kind', 'compound'), ('identical molecules, each containing two different kinds of atom joined together', 'compound'),
       ('two kinds of separate single atoms, not joined to each other', 'mixture'), ('some molecules of two identical atoms and some single atoms of a different kind', 'mixture'),
       ('a regular lattice of two kinds of ion in a fixed ratio', 'compound'), ('two different kinds of molecule, each made of two identical atoms', 'mixture'),
       ('identical molecules each made of four atoms of one element', 'element'), ('a mixture of compound molecules and element molecules', 'mixture')]

t2a = T('Elements, compounds and mixtures', 'elements compounds mixtures')
t2a.fixed('C1', (1, 2), [
    ('Which substance is an element?', 'sulfur', 'Sulfur contains only one type of atom.', ['water', 'air', 'brass']),
    ('Which statement about a compound is correct?', 'It contains two or more elements chemically combined in a fixed ratio.', 'Definition of a compound.',
     ['It can be separated into its elements by filtration.', 'Its properties are the average of the properties of its elements.', 'Its composition can vary.']),
    ('Which of these is a mixture?', 'air', 'Air contains N₂, O₂, Ar, CO₂ etc. not chemically combined.', ['carbon dioxide', 'copper', 'sodium chloride']),
    ('Iron and sulfur powders are mixed. Which method separates the iron from the mixture?', 'using a magnet', 'Iron is magnetic; in a mixture each substance keeps its own properties.', ['heating', 'adding water and filtering', 'distillation']),
    ('Define the term element.', 'A substance made up of only one type of atom (cannot be broken down into simpler substances by chemical means).', '[1]'),
    ('Define the term mixture.', 'Two or more substances that are not chemically combined (and can be separated by physical methods).', '[1]'),
])
t2a.fixed('C2', (2, 3, 4), [
    ('Explain two differences between a mixture of iron and sulfur and the compound iron(II) sulfide.', 'In the mixture iron and sulfur keep their properties (iron is magnetic, can be separated by a magnet) and can be in any ratio; in iron(II) sulfide they are chemically combined in a fixed ratio, with new properties, separable only by chemical reaction.', '1 mark: separation/properties; 1 mark: fixed vs variable ratio [2]'),
    ('Explain why water is classified as a compound and not as a mixture of hydrogen and oxygen.', 'Hydrogen and oxygen atoms are chemically bonded in a fixed ratio (2:1); water has completely different properties from hydrogen and oxygen and cannot be separated by physical methods.', '1 mark: chemically combined fixed ratio; 1 mark: different properties / not separable physically [2]'),
    ('Explain why air is a mixture and not a compound.', 'Its composition can vary, its components are not chemically combined and keep their own properties, and they can be separated physically (fractional distillation of liquid air).', '1 mark each for two points [2]'),
    ('Explain why brass is described as a mixture even though it looks like a single metal.', 'Brass is an alloy of copper and zinc; the metals are not chemically combined and the proportions can vary.', '1 mark: alloy of Cu and Zn; 1 mark: not chemically combined / variable composition [2]'),
    ('A student says, "Sodium chloride is a mixture of sodium and chlorine." Explain why this is wrong.', 'Sodium chloride is a compound: sodium and chlorine are chemically combined (ionic bonding) in a fixed 1:1 ratio, and it has different properties from either element.', '1 mark: compound, chemically combined; 1 mark: fixed ratio / new properties [2]'),
    ('Explain why a compound usually has very different properties from the elements it is made from.', 'In a compound the atoms are chemically bonded into a new substance with a new structure, so its properties are not those of the separate elements (e.g. sodium chloride vs sodium and chlorine).', '[2]'),
])


@t2a.add('C1', (1, 2, 3))
def t2a_which(r, D):
    want = r.choice(['element', 'compound', 'mixture'])
    c = r.choice(CLASSIFY[want])
    others = [x for k, v in CLASSIFY.items() if k != want for x in v]
    stem = r.choice([f'Which substance is {"an" if want == "element" else "a"} {want}?', f'A teacher asks the class to choose {"an" if want == "element" else "a"} {want} from a list. Which one is correct?'])
    return M(r, stem, c, r.sample(others, 6), f'{cap(c)} is {"an" if want == "element" else "a"} {want}: {DEF[want]}.')


@t2a.add('C3', (1, 2, 3, 4))
def t2a_box(r, D):
    desc, kind = r.choice(BOX)
    if D <= 2:
        return M(r, f'A diagram of a box of particles shows {desc}. What does the box contain?', f'{"an" if kind == "element" else "a"} {kind}' if kind != 'mixture' else 'a mixture',
                 ['an element', 'a compound', 'a mixture'] + ['a single substance made of two elements that are not joined together'], f'{cap(desc)} → {kind} ({DEF[kind]}).')
    d2, k2 = r.choice([b for b in BOX if b[0] != desc])
    return Q(f'Two diagrams are drawn. Box 1 shows {desc}. Box 2 shows {d2}. Classify the contents of each box as an element, a compound or a mixture, giving a reason for each.',
             f'Box 1: {kind}; Box 2: {k2}.', f'1 mark: Box 1 {kind} with reason ({DEF[kind]}); 1 mark: Box 2 {k2} with reason [2]' if D == 3 else f'Box 1 {kind} [1] + reason [1]; Box 2 {k2} [1] + reason [1] total [4]',
             'short')


@t2a.add('C3', (2, 3, 4))
def t2a_sort(r, D):
    picks = [(k, x) for k in CLASSIFY for x in r.sample(CLASSIFY[k], 2)]
    r.shuffle(picks)
    picks = picks[:4 if D <= 2 else 6]
    stem = 'Classify each of these as an element, a compound or a mixture: ' + ', '.join(x for _, x in picks) + '.'
    ans = '; '.join(f'{x}: {k}' for k, x in picks)
    n = len(picks)
    key = f'{ans}. ' + (f'All {n} correct [2]; {n - 1} or {n - 2} correct [1] total [2]' if n == 4 else f'1 mark per two correct total [3]')
    if D >= 4:
        el = [x for k, x in picks if k == 'compound' and x in FORMULA_OF]
        if el:
            stem += f' Give the formula of {el[0]} and state how many different elements it contains.'
            f = FORMULA_OF[el[0]]
            ans += f'. {F(f)}; {len(atoms(f))} elements.'
            key = key.replace('total [3]', '') + f'formula [1]; number of elements [1] total [5]'
    return Q(stem, ans, key, 'short')


@t2a.add('C2', (2, 3, 4), 'explain')
def t2a_why(r, D):
    kind = r.choice(['element', 'compound', 'mixture'])
    x = r.choice(CLASSIFY[kind])
    reason = {'element': 'it contains only one type of atom and cannot be broken down into simpler substances by chemical reactions',
              'compound': 'it contains two or more elements chemically combined in a fixed ratio; it can only be separated by a chemical reaction and has properties different from its elements',
              'mixture': 'its components are not chemically combined, keep their own properties, can be present in any proportion and can be separated by physical methods'}[kind]
    return Q(f'Explain why {x} is classified as {"an" if kind == "element" else "a"} {kind}.', f'{cap(x)} is {"an" if kind == "element" else "a"} {kind} because {reason}.',
             '1 mark: correct definition applied; 1 mark: second supporting point [2]' if D <= 3 else '1 mark: classification; 1 mark: definition; 1 mark: how it could be separated / broken down [3]')


def _t2a_c4(r, D):
    p = person(r)
    mFe = r.choice([5.6, 2.8, 11.2, 8.4])
    mS = round(mFe * 32 / 56, 2)
    intro = r.choice([f'{p} mixes {mFe} g of iron filings with {fmt_s(mS)} g of powdered sulfur and then heats part of the mixture strongly in a test tube. It glows red and forms a black solid, iron(II) sulfide.',
                      f'In {lab(r)}, iron filings and sulfur powder are mixed and then heated. A teacher in {city(r)} uses {mFe} g of iron and {fmt_s(mS)} g of sulfur.'])
    parts = [
        lambda r: ('Describe a test that shows the unheated sample is a mixture.', 'Hold a magnet near it: iron is attracted and separated from the yellow sulfur.', '1 mark: magnet; 1 mark: iron separated, sulfur left [2]'),
        lambda r: ('Explain why the product cannot be separated by a magnet.', 'Iron and sulfur are chemically combined in iron(II) sulfide, which has different properties (not magnetic like iron).', '1 mark: chemically combined; 1 mark: new properties [2]'),
        lambda r: ('Write the word equation and the symbol equation for the reaction.', f'iron + sulfur → iron(II) sulfide; {E("Fe(s) + S(s) -> FeS(s)")}', '1 mark each [2]'),
        lambda r: ('Calculate the mass of iron(II) sulfide formed if all the iron and sulfur react.', f'{fmt_s(mFe + mS)} g', 'conservation of mass: ' + f'{mFe} + {fmt_s(mS)} [1]'),
        lambda r: ('State two differences between the mixture and the compound.', 'Mixture: components keep their properties / any ratio / separable physically. Compound: fixed ratio / new properties / separated only chemically.', '1 mark each [2]'),
        lambda r: ('Classify iron, sulfur and iron(II) sulfide as elements or compounds.', 'iron and sulfur are elements; iron(II) sulfide is a compound', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


def fmt_s(x):
    s = f'{x:.2f}'.rstrip('0').rstrip('.')
    return s


t2a.add('C4', (2, 3, 4, 5), 'multi_step')(_t2a_c4)


# ---------------------------------------------------------- 2.2 structure of the atom
ELEM = [  # Z, symbol, name, common A
    (1, 'H', 'hydrogen', 1), (2, 'He', 'helium', 4), (3, 'Li', 'lithium', 7), (4, 'Be', 'beryllium', 9), (5, 'B', 'boron', 11), (6, 'C', 'carbon', 12), (7, 'N', 'nitrogen', 14),
    (8, 'O', 'oxygen', 16), (9, 'F', 'fluorine', 19), (10, 'Ne', 'neon', 20), (11, 'Na', 'sodium', 23), (12, 'Mg', 'magnesium', 24), (13, 'Al', 'aluminium', 27), (14, 'Si', 'silicon', 28),
    (15, 'P', 'phosphorus', 31), (16, 'S', 'sulfur', 32), (17, 'Cl', 'chlorine', 35), (18, 'Ar', 'argon', 40), (19, 'K', 'potassium', 39), (20, 'Ca', 'calcium', 40)]
HEAVY = [(26, 'Fe', 'iron', 56), (29, 'Cu', 'copper', 63), (29, 'Cu', 'copper', 65), (30, 'Zn', 'zinc', 64), (35, 'Br', 'bromine', 79), (35, 'Br', 'bromine', 81), (47, 'Ag', 'silver', 107),
         (53, 'I', 'iodine', 127), (82, 'Pb', 'lead', 207), (92, 'U', 'uranium', 235), (92, 'U', 'uranium', 238), (6, 'C', 'carbon', 14), (17, 'Cl', 'chlorine', 37), (1, 'H', 'hydrogen', 2),
         (8, 'O', 'oxygen', 18), (12, 'Mg', 'magnesium', 26), (56, 'Ba', 'barium', 137), (50, 'Sn', 'tin', 119), (24, 'Cr', 'chromium', 52), (25, 'Mn', 'manganese', 55)]
IONS = [('Na', 1), ('Mg', 2), ('Al', 3), ('O', -2), ('F', -1), ('Cl', -1), ('S', -2), ('K', 1), ('Ca', 2), ('N', -3), ('Li', 1), ('Br', -1), ('Fe', 3), ('Cu', 2), ('Zn', 2)]
ZOF = {s: (z, n, a) for z, s, n, a in ELEM + HEAVY}
ZOF.update({s: (z, n, a) for z, s, n, a in ELEM})


def ion_sym(s, q):
    c = ('' if abs(q) == 1 else str(abs(q))) + ('+' if q > 0 else '-')
    return F(s + '^' + c)


t2b = T('Structure of the atom: protons, neutrons, electrons; proton number and mass number', 'structure of the atom', 'proton number and mass number')
t2b.fixed('C1', (1, 2), [
    ('Which row shows the relative charge of a proton, a neutron and an electron?', 'proton +1, neutron 0, electron −1', 'Relative charges: p +1, n 0, e −1.', ['proton −1, neutron 0, electron +1', 'proton +1, neutron −1, electron 0', 'proton 0, neutron +1, electron −1']),
    ('What is the relative mass of an electron?', '1/1836 (almost zero)', 'Electrons have negligible mass compared with protons and neutrons (relative mass 1).', ['1', '0', '−1']),
    ('Where is most of the mass of an atom found?', 'in the nucleus', 'Protons and neutrons (mass 1 each) are in the nucleus.', ['in the electron shells', 'spread evenly through the atom', 'in the outer shell']),
    ('What is the mass number of an atom?', 'the total number of protons and neutrons in the nucleus', 'Mass number (nucleon number) = protons + neutrons.', ['the number of protons only', 'the number of neutrons only', 'the number of protons and electrons']),
    ('What is the proton number of an atom?', 'the number of protons in the nucleus', 'Proton number (atomic number) = number of protons; it identifies the element.', ['the number of neutrons in the nucleus', 'the total number of particles in the atom', 'the number of electrons in the outer shell']),
    ('Why is an atom electrically neutral?', 'It has equal numbers of protons and electrons.', 'Charges +1 and −1 cancel when numbers are equal.', ['It has equal numbers of protons and neutrons.', 'Neutrons cancel the charge of the electrons.', 'The nucleus has no charge.']),
    ('State the name of the particle in an atom that has no charge.', 'neutron', '[1]'),
])
t2b.fixed('C2', (2, 3, 4), [
    ('Explain why the proton number, not the mass number, identifies an element.', 'All atoms of an element have the same number of protons; the number of neutrons, and so the mass number, can differ (isotopes).', '1 mark: same protons for an element; 1 mark: neutrons/mass number can vary [2]'),
    ('Explain why a sodium ion, Na⁺, has a positive charge.', 'A sodium atom has 11 protons and 11 electrons; it loses one electron to form Na⁺, so it has 11 protons and 10 electrons, giving an overall charge of +1.', '1 mark: loses one electron; 1 mark: one more proton than electrons [2]'),
    ('Compare an atom of chlorine-35 with a chloride ion formed from it, in terms of the numbers of sub-atomic particles.', 'Both have 17 protons and 18 neutrons; the atom has 17 electrons, the ion has 18 electrons.', '1 mark: same protons and neutrons; 1 mark: electrons 17 vs 18 [2]'),
    ('Explain why the mass of an atom is almost the same as the mass of its nucleus.', 'Protons and neutrons each have relative mass 1, electrons have relative mass of only about 1/1836, so electrons add almost nothing to the mass.', '[2]'),
    ('A student says, "The mass number is the number of particles in an atom." Explain why this is incorrect.', 'Mass number counts only protons and neutrons in the nucleus; electrons are not included.', '[2]'),
])


def _nuclide(r, D):
    if D >= 3 and r.random() < 0.5:
        return r.choice(HEAVY)
    return r.choice(ELEM)


@t2b.add('C1', (1, 2, 3))
def t2b_count(r, D):
    z, s, n, a = _nuclide(r, D)
    what = r.choice(['protons', 'neutrons', 'electrons'])
    val = {'protons': z, 'neutrons': a - z, 'electrons': z}[what]
    wrong = [z, a, a - z, a + z, z + 1, a - z - 1, 2 * z]
    return NM(r, f'How many {what} are there in an atom of {nuc(s, a, z)}?', val, wrong, '',
              f'Proton number {z} → {z} protons and {z} electrons; neutrons = {a} − {z} = {a - z}.', f=lambda x: str(int(x)))


@t2b.add('C3', (1, 2, 3, 4))
def t2b_ion(r, D):
    s, q = r.choice(IONS)
    z, nm, a = ZOF[s]
    e = z - q
    if D == 1:
        return NM(r, f'How many electrons are there in the ion {ion_sym(s, q)}? (Proton number of {nm} = {z}.)', e, [z, z + q, a - z, e + 1, e - 1], '',
                  f'{z} protons; charge {q:+d} → {"lost" if q > 0 else "gained"} {abs(q)} electron(s): {z} − ({q:+d}) = {e}.', f=lambda x: str(int(x)))
    stem = f'An ion of {nm} is written as {nuc(s, a, z)}{ion_sym("", q).strip()}. Deduce the numbers of protons, neutrons and electrons in this ion.'
    ans = f'protons {z}, neutrons {a - z}, electrons {e}'
    key = f'1 mark each: protons = {z}; neutrons = {a} − {z} = {a - z}; electrons = {z} {"−" if q > 0 else "+"} {abs(q)} = {e} [3]'
    if D >= 4:
        stem += ' Explain why the ion has this charge.'
        ans += f'; it has {abs(q)} {"more protons than electrons" if q > 0 else "more electrons than protons"}, so the charge is {q:+d}.'
        key += '; reason for charge [1]'
    return Q(stem, ans, key, 'short')


@t2b.add('C3', (2, 3, 4, 5))
def t2b_identify(r, D):
    pts = []
    for _ in range(3 if D <= 3 else 4):
        z, s, n, a = _nuclide(r, D)
        q = 0
        if r.random() < 0.4:
            ions = [x for x in IONS if x[0] == s]
            if ions:
                q = ions[0][1]
        pts.append((z, s, n, a, q))
    if len({(p[0], p[3], p[4]) for p in pts}) < len(pts):
        return None
    labs = 'PQRS'
    rows = '; '.join(f'particle {labs[i]}: {p[0]} protons, {p[3] - p[0]} neutrons, {p[0] - p[4]} electrons' for i, p in enumerate(pts))
    ans = '; '.join(f'{labs[i]} is {nuc(p[1], p[3], p[0])}' + (ion_sym('', p[4]) if p[4] else ' (atom)') for i, p in enumerate(pts))
    n = len(pts)
    key = ans + f'. Element from proton number; mass number = protons + neutrons; charge = protons − electrons. 1 mark each [{n}]'
    stem = f'The table shows the numbers of sub-atomic particles in {n} particles. {rows}. Identify each particle, writing its symbol with mass number, proton number and any charge.'
    if D >= 4:
        stem += ' State which particles, if any, are isotopes of the same element.'
        same = {}
        for i, p in enumerate(pts):
            same.setdefault(p[0], []).append(labs[i])
        iso = [v for z, v in same.items() if len(v) > 1 and len({pts[labs.index(x)][3] for x in v}) > 1]
        ans += '. Isotopes: ' + (', '.join(' and '.join(v) for v in iso) if iso else 'none (no two have the same proton number but different mass numbers)')
        key += '; isotopes identified [1]'
    return Q(stem, ans, key, 'short')


@t2b.add('C2', (2, 3, 4), 'explain')
def t2b_spot(r, D):
    z, s, n, a = r.choice(ELEM[2:] + HEAVY[:8])
    err = r.choice([('neutrons', a, a - z, f'mass number − proton number = {a} − {z}'), ('electrons', a - z, z, f'equal to the number of protons ({z}) in a neutral atom'),
                    ('protons', a - z, z, f'the proton number, {z}')])
    p = person(r)
    return Q(f'{p} says that an atom of {nm_(s)}-{a} ({nuc(s, a, z)}) contains {err[1]} {err[0]}. Explain {p}\'s error and give the correct number of {err[0]}.',
             f'The atom contains {err[2]} {err[0]}: {err[3]}.', f'1 mark: error explained; 1 mark: {err[2]} {err[0]} [2]')


def nm_(s):
    return ZOF[s][1]


def _t2b_c4(r, D):
    (z, s, n, a) = r.choice(ELEM[2:])
    ions = [x for x in IONS if x[0] == s]
    q = ions[0][1] if ions else 0
    p = person(r)
    intro = f'{p} is studying {n}, proton number {z}, mass number {a}.'
    parts = [
        lambda r: ('Give the numbers of protons, neutrons and electrons in one atom.', f'{z} protons, {a - z} neutrons, {z} electrons', '1 mark each [3]'),
        lambda r: ('State the relative mass and relative charge of each type of sub-atomic particle.', 'proton: 1, +1; neutron: 1, 0; electron: 1/1836, −1', '1 mark each particle [3]'),
        lambda r: ('Write the symbol of the atom showing its mass number and proton number.', nuc(s, a, z), '[1]'),
        lambda r: ('Explain why the atom has no overall charge.', f'It has equal numbers of protons ({z}) and electrons ({z}), so the charges cancel.', '[1]'),
        lambda r: ('Explain why almost all the mass of the atom is in the nucleus.', 'Protons and neutrons (relative mass 1 each) are in the nucleus; electrons have negligible mass.', '[2]'),
    ]
    if q:
        parts.append(lambda r: (f'{cap(n)} forms the ion {ion_sym(s, q)}. Deduce the number of electrons in this ion and explain how it forms.', f'{z - q} electrons; the atom {"loses" if q > 0 else "gains"} {abs(q)} electron(s).', '1 mark: number; 1 mark: lose/gain [2]'))
    z2 = z
    a2 = a + r.choice([1, 2]) if s not in ('Be', 'F', 'Na', 'Al', 'P') else a + 1
    parts.append(lambda r: (f'Another atom has {z2} protons and {a2 - z2} neutrons. State whether it is the same element and give its mass number.', f'Yes, same element (same proton number); mass number {a2}; it is an isotope.', '1 mark: same element; 1 mark: mass number [2]'))
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t2b.add('C4', (2, 3, 4, 5), 'multi_step')(_t2b_c4)


# ---------------------------------------------------------- 2.3 isotopes and Ar
ISO = [('chlorine', 'Cl', 17, [(35, 75.0), (37, 25.0)]), ('copper', 'Cu', 29, [(63, 69.2), (65, 30.8)]), ('boron', 'B', 5, [(10, 19.9), (11, 80.1)]),
       ('magnesium', 'Mg', 12, [(24, 79.0), (25, 10.0), (26, 11.0)]), ('lithium', 'Li', 3, [(6, 7.5), (7, 92.5)]), ('bromine', 'Br', 35, [(79, 50.7), (81, 49.3)]),
       ('neon', 'Ne', 10, [(20, 90.5), (21, 0.3), (22, 9.2)]), ('gallium', 'Ga', 31, [(69, 60.1), (71, 39.9)]), ('rubidium', 'Rb', 37, [(85, 72.2), (87, 27.8)]),
       ('silver', 'Ag', 47, [(107, 51.8), (109, 48.2)]), ('silicon', 'Si', 14, [(28, 92.2), (29, 4.7), (30, 3.1)]), ('potassium', 'K', 19, [(39, 93.3), (41, 6.7)]),
       ('antimony', 'Sb', 51, [(121, 57.2), (123, 42.8)]), ('iridium', 'Ir', 77, [(191, 37.3), (193, 62.7)]), ('europium', 'Eu', 63, [(151, 47.8), (153, 52.2)])]


def ar_of(isos):
    return sum(a * p for a, p in isos) / sum(p for _, p in isos)


t2c = T('Isotopes and calculating relative atomic mass from abundances', 'isotopes', 'relative atomic mass from abundances')
t2c.fixed('C1', (1, 2), [
    ('What are isotopes?', 'atoms of the same element with the same number of protons but different numbers of neutrons', 'Isotopes: same proton number, different mass number.',
     ['atoms of different elements with the same mass number', 'atoms of the same element with different numbers of electrons', 'atoms with the same number of neutrons but different numbers of protons']),
    ('Why do isotopes of the same element have the same chemical properties?', 'They have the same number of electrons in the outer shell (same electronic configuration).', 'Chemical properties depend on electrons.',
     ['They have the same number of neutrons.', 'They have the same mass.', 'They have the same density.']),
    ('Which pair of atoms are isotopes of each other?', '¹²₆C and ¹⁴₆C', 'Same proton number (6), different mass numbers.', ['¹⁴₆C and ¹⁴₇N', '¹⁶₈O and ¹⁹₉F', '⁴⁰₁₈Ar and ⁴⁰₂₀Ca']),
    ('Define relative atomic mass, Ar.', 'The average mass of the isotopes of an element compared with 1/12 of the mass of an atom of carbon-12.', '1 mark: average (weighted) mass of isotopes; 1 mark: relative to 1/12 of carbon-12 [2]'),
    ('Which property is different for two isotopes of chlorine?', 'their mass', 'Different numbers of neutrons → different masses (and densities of the element).', ['their proton number', 'their number of electrons', 'the way they react with sodium']),
])
t2c.fixed('C2', (2, 3, 4), [
    ('Explain why the relative atomic mass of chlorine is 35.5 even though no chlorine atom has a mass of 35.5.', 'Ar is a weighted average of the masses of the isotopes (chlorine-35 about 75% and chlorine-37 about 25%), so it need not be a whole number.', '1 mark: weighted average of isotopes; 1 mark: abundances of Cl-35 and Cl-37 [2]'),
    ('Explain why chlorine-35 and chlorine-37 react in the same way with sodium.', 'Both have 17 protons and 17 electrons with the same electronic configuration (2,8,7); chemical reactions involve electrons, so they react identically.', '1 mark: same electrons / configuration; 1 mark: reactions depend on electrons [2]'),
    ('Explain why the relative atomic mass of boron (10.8) is closer to 11 than to 10.', 'Boron-11 is much more abundant (about 80%) than boron-10 (about 20%), so the weighted average is nearer 11.', '[2]'),
    ('State and explain one physical property that differs between isotopes of an element.', 'Mass/density (also rate of diffusion of gases): isotopes have different numbers of neutrons, so their atoms have different masses.', '1 mark: property; 1 mark: different numbers of neutrons/mass [2]'),
    ('A student says, "Isotopes are different elements because they have different mass numbers." Explain why this is wrong.', 'Isotopes have the same proton number, and the proton number defines the element; only the number of neutrons differs.', '[2]'),
])


def _rand_iso(r, D):
    if D >= 4 and r.random() < 0.4:
        a = r.choice(range(20, 120))
        p1 = r.choice(range(55, 96))
        return (f'element X', 'X', None, [(a, float(p1)), (a + r.choice([1, 2]), float(100 - p1))])
    return r.choice(ISO)


@t2c.add('C3', (1, 2, 3, 4))
def t2c_ar(r, D):
    nm, s, z, isos = _rand_iso(r, D)
    ar = ar_of(isos)
    data = '; '.join(f'{s}-{a}: {fmt_s(p)}%' for a, p in isos)
    work = '(' + ' + '.join(f'({a} × {fmt_s(p)})' for a, p in isos) + f') ÷ {fmt_s(sum(p for _, p in isos))} = {fmt_s(round(sum(a * p for a, p in isos), 2))} ÷ {fmt_s(sum(p for _, p in isos))}'
    if D == 1:
        wrong = [sum(a for a, _ in isos) / len(isos), isos[0][0], isos[-1][0], ar + 0.5, ar - 0.4]
        return NM(r, f'The isotopic composition of a sample of {nm} is {data}. What is the relative atomic mass of {nm}?', ar, wrong, '', work, f=lambda x: sf(x, 3))
    stem = r.choice([f'A sample of {nm} has the following isotopic composition: {data}. Calculate the relative atomic mass of {nm} to one decimal place.',
                     f'{who(r)} is given data for the isotopes of {nm}: {data}. Calculate the relative atomic mass of {nm}, giving your answer to 1 decimal place.'])
    ans = f'{ar:.1f}'
    key = f'{work} [1]; = {ar:.1f} [1]'
    if D >= 3:
        stem += ' Explain why the answer is not a whole number.'
        ans += '; it is a weighted average of the masses of the isotopes.'
        key += '; weighted average explanation [1]'
    return Q(stem, ans, key, 'numerical')


@t2c.add('C3', (3, 4, 5))
def t2c_reverse(r, D):
    nm, s, z, isos = r.choice([i for i in ISO if len(i[3]) == 2])
    (a1, p1), (a2, p2) = isos
    ar = round(ar_of(isos), 2)
    x = (a2 - ar) / (a2 - a1) * 100
    stem = f'{cap(nm)} has two naturally occurring isotopes, {s}-{a1} and {s}-{a2}. Its relative atomic mass is {ar}. Calculate the percentage abundance of each isotope.'
    ans = f'{s}-{a1}: {x:.1f}%; {s}-{a2}: {100 - x:.1f}%'
    key = f'let % of {s}-{a1} = x: ({a1}x + {a2}(100 − x))/100 = {ar} [1]; x = {x:.1f}% [1]; {s}-{a2} = {100 - x:.1f}% [1]'
    if D >= 5:
        stem += f' Deduce the number of neutrons in each isotope (proton number {z}).'
        ans += f'; neutrons {a1 - z} and {a2 - z}'
        key += f'; neutrons {a1 - z} and {a2 - z} [1]'
    return Q(stem, ans, key, 'numerical')


@t2c.add('C1', (1, 2, 3))
def t2c_pair(r, D):
    z, s, n, a = r.choice(ELEM[5:] + HEAVY[:6])
    corr = f'{nuc(s, a, z)} and {nuc(s, a + 2, z)}'
    z2, s2, n2, a2 = r.choice([e for e in ELEM if e[0] != z])
    pool = [f'{nuc(s, a, z)} and {nuc(s2, a, z2)}', f'{nuc(s2, a2, z2)} and {nuc(s, a2, z)}', f'{nuc(s, a, z)} and {nuc(s2, a2 + 1, z2)}', f'{nuc(s2, a2, z2)} and {nuc(s, a, z)}']
    return M(r, 'Which pair of symbols represents two isotopes of the same element?', corr, pool, f'Isotopes have the same proton number ({z}) but different mass numbers.')


@t2c.add('C2', (2, 3, 4), 'explain')
def t2c_explain(r, D):
    nm, s, z, isos = r.choice(ISO)
    (a1, p1), (a2, p2) = isos[0], isos[1]
    ar = ar_of(isos)
    major = max(isos, key=lambda x: x[1])
    return Q(f'{cap(nm)} has isotopes including {s}-{a1} and {s}-{a2}, and its relative atomic mass is {sf(ar, 3)}. Explain what the isotopes have in common, how they differ, and why the Ar is closest to {major[0]}.',
             f'Same number of protons ({z}) and electrons; different numbers of neutrons ({a1 - z} and {a2 - z}); {s}-{major[0]} is the most abundant isotope ({fmt_s(major[1])}%), so the weighted average is nearest {major[0]}.',
             '1 mark: same protons/electrons; 1 mark: different neutrons with numbers; 1 mark: most abundant isotope dominates the weighted average [3]')


def _t2c_c4(r, D):
    nm, s, z, isos = _rand_iso(r, 4)
    ar = ar_of(isos)
    data = '; '.join(f'mass {a}: {fmt_s(p)}%' for a, p in isos)
    intro = r.choice([f'A mass spectrometer in {city(r)} analyses a sample of {nm}. The results show these isotopes: {data}.',
                      f'{person(r)} is given data for a sample of {nm}: {data}.'])
    zz = z if z else r.choice(range(10, 50))
    parts = [
        lambda r: ('Explain what is meant by the term isotopes.', 'Atoms of the same element with the same number of protons but different numbers of neutrons.', '1 mark: same protons; 1 mark: different neutrons [2]'),
        lambda r: ('Calculate the relative atomic mass of the sample, to one decimal place.', f'{ar:.1f}', ' + '.join(f'({a} × {fmt_s(p)})' for a, p in isos) + f' ÷ 100 [1]; = {ar:.1f} [1] total [2]'),
        lambda r: (f'The proton number of {nm} is {zz}. Give the number of neutrons in each isotope.', ', '.join(f'{a}: {a - zz}' for a, _ in isos), f'neutrons = mass number − {zz} [2]'),
        lambda r: ('Explain why the isotopes have identical chemical properties.', 'Same number and arrangement of electrons (same electronic configuration).', '[1]'),
        lambda r: ('Suggest one physical property that would differ between the isotopes.', 'mass / density / rate of diffusion (of gaseous compounds)', '[1]'),
        lambda r: (f'Another sample of {nm} from a different source has a slightly higher relative atomic mass. Suggest an explanation.', f'It contains a higher proportion of the heavier isotope ({isos[-1][0]}).', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t2c.add('C4', (2, 3, 4, 5), 'multi_step')(_t2c_c4)


# ---------------------------------------------------------- 2.4 electronic configuration
def config(z):
    out = []
    for cap_ in (2, 8, 8, 2):
        if z <= 0:
            break
        k = min(cap_, z)
        out.append(k)
        z -= k
    return out


def cfg(z):
    return ','.join(map(str, config(z)))


def group_of(z):
    c = config(z)
    if z == 2 or c[-1] == 8:
        return 'VIII'
    return ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][c[-1] - 1]


def period_of(z):
    return len(config(z))


t2d = T('Electronic configuration and its link to group and period number', 'electronic configuration', 'group and period number')
t2d.fixed('C1', (1, 2), [
    ('What is the maximum number of electrons in the first shell of an atom?', '2', 'First shell holds up to 2 electrons; second and third up to 8 (for elements 1–20).', ['8', '18', '1']),
    ('An element has the electronic configuration 2,8,3. In which group of the Periodic Table is it?', 'Group III', 'Number of outer-shell electrons = group number (3).', ['Group II', 'Group VIII', 'Group V']),
    ('An element is in Period 3. What does this tell you about its atoms?', 'They have three occupied electron shells.', 'Period number = number of occupied shells.', ['They have three outer-shell electrons.', 'They have three protons.', 'They form ions with a charge of 3+.']),
    ('Why do elements in the same group have similar chemical properties?', 'Their atoms have the same number of outer-shell electrons.', 'Reactions involve outer electrons.', ['Their atoms have the same number of shells.', 'They have the same mass number.', 'They have the same number of neutrons.']),
    ('Which electronic configuration is that of a noble gas?', '2,8,8', 'Full outer shell → Group VIII (argon).', ['2,8,7', '2,8,8,1', '2,7']),
    ('State why the noble gases are unreactive in terms of electrons.', 'They have a full outer shell of electrons (stable configuration).', '[1]'),
])
t2d.fixed('C2', (2, 3, 4), [
    ('Explain how the electronic configuration of an atom is linked to its position in the Periodic Table.', 'The number of occupied shells gives the period number; the number of outer-shell electrons gives the group number (Group VIII has a full outer shell).', '1 mark: shells → period; 1 mark: outer electrons → group [2]'),
    ('Explain why sodium and potassium have similar chemical reactions.', 'Both have one electron in their outer shell (2,8,1 and 2,8,8,1), and reactions depend on outer-shell electrons.', '1 mark: one outer electron each; 1 mark: chemistry depends on outer electrons [2]'),
    ('Explain why helium is placed in Group VIII even though it has only two electrons in its outer shell.', 'Its first (only) shell is full with two electrons, so like the other noble gases it has a stable full outer shell and is unreactive.', '[2]'),
    ('A student says, "Chlorine is in Period 7 because it has seven outer electrons." Explain the error.', 'Seven outer electrons means Group VII; chlorine (2,8,7) has three occupied shells so it is in Period 3.', '1 mark: 7 outer electrons = group; 1 mark: 3 shells = Period 3 [2]'),
    ('Explain why the elements in Period 2 all have two occupied electron shells but different chemical properties.', 'They have the same number of shells but a different number of outer-shell electrons (1 to 8), and outer electrons determine chemical properties.', '[2]'),
])


@t2d.add('C1', (1, 2, 3))
def t2d_cfg(r, D):
    z, s, n, a = r.choice(ELEM[2:])
    c = cfg(z)
    wrong = set()
    cc = config(z)
    for v in ([cc[0] + 1] + cc[1:], cc[:-1] + [cc[-1] + 1] if cc[-1] < 8 else cc[:-1] + [cc[-1] - 1], [2, 8, z - 10] if z > 10 else [2, z - 2, 0], [2] + [z - 2]):
        v = [x for x in v if x > 0]
        if sum(v) and ','.join(map(str, v)) != c:
            wrong.add(','.join(map(str, v)))
    wrong |= {cfg(z + 1), cfg(z - 1), cfg(z + 2) if z < 19 else '2,8,8,3'}
    wrong.discard(c)
    if len(wrong) < 3:
        return None
    return M(r, f'What is the electronic configuration of {"an atom of " if r.random() < 0.5 else ""}{n} (proton number {z})?', c, list(wrong), f'{z} electrons filled 2, then 8, then 8: {c}.')


@t2d.add('C3', (1, 2, 3, 4))
def t2d_place(r, D):
    z, s, n, a = r.choice(ELEM[2:])
    g, p = group_of(z), period_of(z)
    if D == 1:
        return M(r, f'An atom has the electronic configuration {cfg(z)}. In which group and period is the element?', f'Group {g}, Period {p}',
                 [f'Group {p if p <= 3 else "IV"}, Period {config(z)[-1]}', f'Group {g}, Period {config(z)[-1] if config(z)[-1] != p else p + 1}', f'Group {["I","II","III","IV","V","VI","VII","VIII"][(["I","II","III","IV","V","VI","VII","VIII"].index(g) + 1) % 8]}, Period {p}', f'Group {g}, Period {p - 1 if p > 1 else 4}'],
                 f'{len(config(z))} shells → Period {p}; {config(z)[-1]} outer electrons → Group {g}.')
    els = r.sample(ELEM[2:], 3 if D <= 3 else 4)
    stem = 'For each element, write the electronic configuration and state its group and period: ' + ', '.join(f'{e[2]} (proton number {e[0]})' for e in els) + '.'
    ans = '; '.join(f'{e[2]}: {cfg(e[0])}, Group {group_of(e[0])}, Period {period_of(e[0])}' for e in els)
    key = ans + f'. 1 mark each correct configuration; 1 mark for group and period of each [' + str(2 * len(els)) + ']' if D >= 4 else ans + f'. 1 mark per element (configuration with group and period) [{len(els)}]'
    return Q(stem, ans, key, 'short')


@t2d.add('C3', (2, 3, 4))
def t2d_ion(r, D):
    s, q = r.choice([x for x in IONS if ZOF[x[0]][0] <= 20])
    z = ZOF[s][0]
    e = z - q
    stem = f'Write the electronic configuration of the {ZOF[s][1]} atom (proton number {z}) and of the ion {ion_sym(s, q)}. Explain why the ion is stable.'
    return Q(stem, f'atom {cfg(z)}; ion {cfg(e)} — the ion has a full outer shell like the noble gas {[x for x in ELEM if x[0] == e][0][2]}.',
             f'1 mark atom {cfg(z)}; 1 mark ion {cfg(e)}; 1 mark full outer shell / noble gas configuration [3]', 'short')


@t2d.add('C2', (2, 3, 4), 'explain')
def t2d_similar(r, D):
    grp = r.choice([[3, 11, 19], [4, 12, 20], [9, 17], [8, 16], [2, 10, 18], [7, 15], [5, 13], [6, 14]])
    a, b = r.sample(grp, 2)
    na, nb = [x[2] for x in ELEM if x[0] == a][0], [x[2] for x in ELEM if x[0] == b][0]
    return Q(f'Use electronic configurations to explain why {na} (proton number {a}) and {nb} (proton number {b}) are in the same group but different periods.',
             f'{na}: {cfg(a)}; {nb}: {cfg(b)}. Both have {config(a)[-1]} outer-shell electron(s), so same group ({group_of(a)}); they have {period_of(a)} and {period_of(b)} occupied shells, so different periods.',
             '1 mark: both configurations; 1 mark: same outer electrons → same group; 1 mark: different number of shells → different period [3]')


def _t2d_c4(r, D):
    z, s, n, a = r.choice(ELEM[2:19])
    p = person(r)
    ions = [x for x in IONS if x[0] == s]
    intro = r.choice([f'{p} is given element E, which has {z} protons in each atom.', f'Element E (proton number {z}) is found in a mineral sample from {city(r)}.'])
    parts = [
        lambda r: ('Write the electronic configuration of an atom of E.', cfg(z), '[1]'),
        lambda r: ('State the group and period of E and explain how you deduced them.', f'Group {group_of(z)}, Period {period_of(z)}: {config(z)[-1]} outer electrons and {period_of(z)} occupied shells.', '1 mark: group; 1 mark: period; 1 mark: reasoning [3]'),
        lambda r: ('Identify E.', n, '[1]'),
        lambda r: ('Name another element with similar chemical properties to E and explain why.', 'any element in Group ' + group_of(z) + ' (same number of outer electrons)', '1 mark: element; 1 mark: same number of outer electrons [2]'),
        lambda r: (f'Describe the arrangement of electrons in an atom of E in shells.', ', '.join(f'shell {i + 1}: {k}' for i, k in enumerate(config(z))), '[1]'),
    ]
    if ions:
        q = ions[0][1]
        parts.append(lambda r: ('Predict the charge on the ion formed by E and give the configuration of this ion.', f'{q:+d}; {cfg(z - q)}', '1 mark charge; 1 mark configuration [2]'))
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t2d.add('C4', (2, 3, 4, 5), 'multi_step')(_t2d_c4)

CHAPTERS[2] = [t2a, t2b, t2c, t2d]


# ===================================================================== Ch3 Chemical bonding
METALS = {'Li': ('lithium', 3, 1), 'Na': ('sodium', 11, 1), 'K': ('potassium', 19, 1), 'Mg': ('magnesium', 12, 2), 'Ca': ('calcium', 20, 2), 'Al': ('aluminium', 13, 3)}
NONMET = {'F': ('fluorine', 'fluoride', 9, 1), 'Cl': ('chlorine', 'chloride', 17, 1), 'O': ('oxygen', 'oxide', 8, 2), 'S': ('sulfur', 'sulfide', 16, 2), 'N': ('nitrogen', 'nitride', 7, 3)}
IONIC_PAIRS = [(m, n) for m in METALS for n in NONMET if not (n == 'N' and m in ('Na', 'K', 'Al'))]


def ionic(m, n):
    a, b = METALS[m][2], NONMET[n][3]
    l = a * b // math.gcd(a, b)
    nm_, nn = l // a, l // b
    f = (m + (str(nm_) if nm_ > 1 else '')) + (n + (str(nn) if nn > 1 else ''))
    return f, nm_, nn, a, b


def ionic_name(m, n):
    return f'{METALS[m][0]} {NONMET[n][1]}'


def transfer_text(m, n):
    f, nm_, nn, a, b = ionic(m, n)
    zm, zn = METALS[m][1], NONMET[n][2]
    return (f'Each {METALS[m][0]} atom ({cfg(zm)}) loses {a} outer electron{"s" if a > 1 else ""} to form {ion_sym(m, a)} ({cfg(zm - a)}); '
            f'each {NONMET[n][0]} atom ({cfg(zn)}) gains {b} electron{"s" if b > 1 else ""} to form {ion_sym(n, -b)} ({cfg(zn + b)}). '
            + (f'{nm_} {METALS[m][0]} atom{"s" if nm_ > 1 else ""} transfer{"" if nm_ > 1 else "s"} electrons to {nn} {NONMET[n][0]} atom{"s" if nn > 1 else ""}, ' if (nm_ > 1 or nn > 1) else '')
            + f'and the oppositely charged ions attract (ionic bond), giving {F(f)}.')


t3a = T('Ionic bonding: formation of ions by electron transfer and dot-and-cross diagrams', 'ionic bonding', 'dot-and-cross diagrams', 'electron transfer')
t3a.fixed('C1', (1, 2), [
    ('What is an ionic bond?', 'the strong electrostatic attraction between oppositely charged ions', 'Ionic bond: electrostatic attraction between positive and negative ions.',
     ['a shared pair of electrons between two atoms', 'the attraction between positive ions and delocalised electrons', 'a weak force between molecules']),
    ('What happens to the electrons when magnesium reacts with oxygen to form magnesium oxide?', 'Each magnesium atom transfers two electrons to an oxygen atom.', 'Mg (2,8,2) → Mg²⁺; O (2,6) → O²⁻.',
     ['Each oxygen atom transfers two electrons to a magnesium atom.', 'Magnesium and oxygen share two pairs of electrons.', 'Each magnesium atom transfers one electron to an oxygen atom.']),
    ('Which type of element forms positive ions?', 'metals', 'Metal atoms lose outer electrons to form positive ions.', ['non-metals', 'noble gases', 'halogens']),
    ('What is the charge on an ion formed from an atom with the electronic configuration 2,8,7?', '1−', 'It gains one electron to reach 2,8,8.', ['7+', '1+', '7−']),
    ('Which pair of elements would form an ionic compound?', 'potassium and fluorine', 'Metal + non-metal → ionic.', ['carbon and oxygen', 'hydrogen and chlorine', 'nitrogen and hydrogen']),
    ('State what is meant by an ion.', 'An atom or group of atoms that has gained or lost one or more electrons and so carries a charge.', '[1]'),
])
t3a.fixed('C2', (2, 3, 4), [
    ('Explain why sodium forms an Na⁺ ion and not an Na²⁺ ion.', 'Sodium (2,8,1) loses its single outer electron to reach the stable configuration 2,8 of neon; removing a second electron from a full shell would need far more energy.', '1 mark: loses one outer electron; 1 mark: achieves full outer shell / noble gas configuration [2]'),
    ('Explain why the formula of calcium chloride is CaCl₂.', 'Calcium loses two electrons to form Ca²⁺; each chlorine atom gains only one electron to form Cl⁻, so two chloride ions are needed to balance the charge of one calcium ion.', '1 mark: Ca²⁺ and Cl⁻; 1 mark: charges balance 2 × (1−) [2]'),
    ('Describe what a dot-and-cross diagram for sodium chloride shows.', 'Na⁺ with a full outer shell (or no outer electrons shown) and Cl⁻ with eight outer electrons, seven of one symbol and one of the other showing the transferred electron; both ions in brackets with their charges.', '1 mark: Na⁺ shell; 1 mark: Cl⁻ with 8 including the transferred electron; 1 mark: charges [3]'),
    ('A student says, "In sodium chloride, sodium and chlorine share an electron." Explain the error.', 'In ionic bonding electrons are transferred, not shared: sodium loses one electron to chlorine, forming Na⁺ and Cl⁻ ions that attract each other.', '[2]'),
    ('Explain why ionic bonds form between metals and non-metals but not usually between two non-metals.', 'Metals have few outer electrons and lose them easily; non-metals have nearly full outer shells and gain electrons. Two non-metals both tend to gain electrons, so they share instead.', '1 mark: metals lose, non-metals gain; 1 mark: two non-metals share (covalent) [2]'),
])


@t3a.add('C1', (1, 2, 3))
def t3a_formula(r, D):
    m, n = r.choice(IONIC_PAIRS)
    f, nm_, nn, a, b = ionic(m, n)
    pool = {F(m + n), F(m + n + '2'), F(m + '2' + n), F(m + '2' + n + '3'), F(m + '3' + n + '2'), F(m + n + '3'), F(m + '3' + n)}
    pool.discard(F(f))
    if D <= 1:
        return M(r, f'{cap(METALS[m][0])} reacts with {NONMET[n][0]} to form an ionic compound. What is its formula?', F(f), list(pool),
                 f'{ion_sym(m, a)} and {ion_sym(n, -b)}: charges balance with {nm_}:{nn} → {F(f)}.')
    return M(r, f'Which row shows the ions formed and the formula of {ionic_name(m, n)}?', f'{ion_sym(m, a)} and {ion_sym(n, -b)}; {F(f)}',
             [f'{ion_sym(m, a)} and {ion_sym(n, -b)}; {x}' for x in list(pool)[:2]] + [f'{ion_sym(m, b)} and {ion_sym(n, -a)}; {F(f)}', f'{ion_sym(m, -a)} and {ion_sym(n, b)}; {F(f)}'],
             f'Metal loses {a} e⁻ → {ion_sym(m, a)}; non-metal gains {b} e⁻ → {ion_sym(n, -b)}; formula {F(f)}.')


@t3a.add('C3', (2, 3, 4, 5))
def t3a_describe(r, D):
    m, n = r.choice(IONIC_PAIRS)
    f, nm_, nn, a, b = ionic(m, n)
    zm, zn = METALS[m][1], NONMET[n][2]
    stem = r.choice([f'Describe, in terms of electrons, how {ionic_name(m, n)} forms when {METALS[m][0]} reacts with {NONMET[n][0]}.',
                     f'{who(r)} burns {METALS[m][0]} in {NONMET[n][0]} to make {ionic_name(m, n)}. Describe how the ions form, in terms of electron transfer.'])
    key = f'1 mark: {METALS[m][0]} loses {a} electron(s); 1 mark: {NONMET[n][0]} gains {b} electron(s); 1 mark: ions {ion_sym(m, a)} and {ion_sym(n, -b)}'
    marks = 3
    if D >= 3:
        stem += f' Include the electronic configurations of the atoms and ions (proton numbers: {METALS[m][0]} {zm}, {NONMET[n][0]} {zn}).'
        key += f'; 1 mark: configurations {cfg(zm)} → {cfg(zm - a)} and {cfg(zn)} → {cfg(zn + b)}'
        marks += 1
    if D >= 4:
        stem += ' Describe the dot-and-cross diagram for the compound and deduce its formula.'
        key += f'; 1 mark: diagram shows {nm_} × [{METALS[m][0]} ion]{sup(a)}⁺ and {nn} × [{NONMET[n][0]} ion] with 8 outer electrons and charge {b}−; 1 mark: formula {F(f)}'
        marks += 2
    return Q(stem, transfer_text(m, n), key + f' [{marks}]', 'explain')


@t3a.add('C2', (2, 3, 4), 'explain')
def t3a_why(r, D):
    m, n = r.choice(IONIC_PAIRS)
    f, nm_, nn, a, b = ionic(m, n)
    if nm_ == 1 and nn == 1:
        return Q(f'Explain why the formula of {ionic_name(m, n)} is {F(f)}, using the charges on its ions.', f'{ion_sym(m, a)} and {ion_sym(n, -b)} have equal and opposite charges, so they combine 1:1.',
                 '1 mark: both ion charges; 1 mark: charges cancel in 1:1 ratio [2]')
    return Q(f'Explain why the formula of {ionic_name(m, n)} is {F(f)} and not {F(m + n)}.', f'The ions are {ion_sym(m, a)} and {ion_sym(n, -b)}; {nm_} × ({a}+) = {nn} × ({b}−) so {nm_} {METALS[m][0]} ion(s) combine with {nn} {NONMET[n][1]} ion(s) for zero overall charge.',
             '1 mark: ion charges; 1 mark: ratio gives overall neutral compound [2]' if D <= 3 else '1 mark: metal ion charge from electrons lost; 1 mark: non-metal ion charge; 1 mark: ratio balancing charges [3]')


def _t3a_c4(r, D):
    m, n = r.choice(IONIC_PAIRS)
    f, nm_, nn, a, b = ionic(m, n)
    zm, zn = METALS[m][1], NONMET[n][2]
    p = person(r)
    intro = r.choice([f'{p} heats {METALS[m][0]} (proton number {zm}) in {NONMET[n][0]} (proton number {zn}). A white solid, {ionic_name(m, n)}, is formed.',
                      f'{cap(ionic_name(m, n))} is an ionic compound formed from {METALS[m][0]} (proton number {zm}) and {NONMET[n][0]} (proton number {zn}). A research group in {city(r)} is studying its structure.'])
    parts = [
        lambda r: ('Give the electronic configurations of both atoms.', f'{cfg(zm)}; {cfg(zn)}', '1 mark each [2]'),
        lambda r: ('Describe how the ions are formed.', f'{METALS[m][0]} loses {a} electron(s) to form {ion_sym(m, a)}; {NONMET[n][0]} gains {b} to form {ion_sym(n, -b)}.', '1 mark each ion with electrons lost/gained [2]'),
        lambda r: ('Describe the dot-and-cross diagram of the compound, showing outer shells only.', f'{nm_} {ion_sym(m, a)} ion(s) with empty/full outer shell and {nn} {ion_sym(n, -b)} ion(s) each with 8 outer electrons (including {b} of the other symbol); brackets and charges.', '1 mark: correct number of each ion; 1 mark: 8 electrons on anion with transferred electrons shown; 1 mark: charges [3]'),
        lambda r: ('Deduce the formula of the compound.', F(f), '[1]'),
        lambda r: ('Name the type of force holding the ions together and describe the structure of the solid.', 'Strong electrostatic attraction between oppositely charged ions; a giant ionic lattice with ions in a regular repeating arrangement.', '1 mark: electrostatic attraction; 1 mark: giant lattice [2]'),
        lambda r: ('Predict two physical properties of the compound and explain one of them.', 'High melting point (many strong electrostatic forces to overcome); conducts when molten or dissolved (ions free to move), not as a solid.', '1 mark each property; 1 mark explanation [3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t3a.add('C4', (2, 3, 4, 5), 'multi_step')(_t3a_c4)
t3a.add('C3', (4, 5), 'multi_step')(_t3a_c4)


# ---------------------------------------------------------- 3.2 giant ionic lattices
STRUCT = [  # name, mp °C, conducts solid, conducts molten, soluble/aq conducts, type
    ('sodium chloride', 801, 'no', 'yes', 'soluble; solution conducts', 'giant ionic'), ('magnesium oxide', 2852, 'no', 'yes', 'insoluble', 'giant ionic'),
    ('potassium bromide', 734, 'no', 'yes', 'soluble; solution conducts', 'giant ionic'), ('calcium chloride', 772, 'no', 'yes', 'soluble; solution conducts', 'giant ionic'),
    ('lithium fluoride', 845, 'no', 'yes', 'slightly soluble; solution conducts', 'giant ionic'), ('aluminium oxide', 2072, 'no', 'yes', 'insoluble', 'giant ionic'),
    ('sulfur', 115, 'no', 'no', 'insoluble', 'simple molecular'), ('iodine', 114, 'no', 'no', 'very slightly soluble; solution does not conduct', 'simple molecular'),
    ('glucose', 146, 'no', 'no', 'soluble; solution does not conduct', 'simple molecular'), ('paraffin wax', 55, 'no', 'no', 'insoluble', 'simple molecular'),
    ('ethanol', -114, 'no', 'no', 'soluble; solution does not conduct', 'simple molecular'), ('water', 0, 'no', 'no (pure)', 'n/a', 'simple molecular'),
    ('diamond', 3550, 'no', 'no', 'insoluble', 'giant covalent'), ('silicon(IV) oxide', 1710, 'no', 'no', 'insoluble', 'giant covalent'),
    ('graphite', 3652, 'yes', 'yes', 'insoluble', 'giant covalent'), ('silicon', 1414, 'slightly (semiconductor)', 'yes', 'insoluble', 'giant covalent'),
    ('copper', 1085, 'yes', 'yes', 'insoluble', 'metallic'), ('iron', 1538, 'yes', 'yes', 'insoluble', 'metallic'), ('aluminium', 660, 'yes', 'yes', 'insoluble', 'metallic'),
    ('magnesium', 650, 'yes', 'yes', 'insoluble (reacts slowly)', 'metallic'), ('zinc', 420, 'yes', 'yes', 'insoluble', 'metallic')]
STRUCT_WHY = {'giant ionic': 'high melting point and conducts only when molten or in solution (ions free to move)',
              'simple molecular': 'low melting point (weak intermolecular forces) and does not conduct in any state (no ions or free electrons)',
              'giant covalent': 'very high melting point (many strong covalent bonds) and does not conduct (except graphite)',
              'metallic': 'conducts electricity when solid and when liquid (delocalised electrons)'}
IONIC_CMP = [('sodium chloride', 'NaCl', 801), ('magnesium oxide', 'MgO', 2852), ('potassium chloride', 'KCl', 770), ('calcium oxide', 'CaO', 2613), ('lithium fluoride', 'LiF', 845),
             ('sodium fluoride', 'NaF', 993), ('potassium bromide', 'KBr', 734), ('calcium chloride', 'CaCl2', 772), ('magnesium chloride', 'MgCl2', 714), ('aluminium oxide', 'Al2O3', 2072)]

t3b = T('Giant ionic lattices and properties of ionic compounds', 'giant ionic lattices', 'properties of ionic compounds')
t3b.fixed('C1', (1, 2), [
    ('Which statement describes the structure of solid sodium chloride?', 'a giant lattice of alternating Na⁺ and Cl⁻ ions', 'Giant ionic lattice: regular arrangement of oppositely charged ions.',
     ['separate NaCl molecules held by weak forces', 'Na atoms and Cl atoms sharing electrons', 'positive ions in a sea of delocalised electrons']),
    ('Why does solid sodium chloride not conduct electricity?', 'Its ions are held in fixed positions and cannot move.', 'Ions in the lattice cannot move; when molten or dissolved they can.',
     ['It has no ions.', 'Its electrons are delocalised.', 'Its molecules are neutral.']),
    ('Why do ionic compounds have high melting points?', 'There are strong electrostatic attractions between oppositely charged ions throughout the lattice.', 'Much energy is needed to overcome the many strong ionic bonds.',
     ['There are weak forces between molecules.', 'The ions share electrons.', 'The electrons are free to move.']),
    ('Which property is typical of an ionic compound?', 'It conducts electricity when molten.', 'Ions become mobile when molten or aqueous.', ['It conducts electricity when solid.', 'It has a low melting point.', 'It is malleable.']),
    ('In a sodium chloride lattice, how many chloride ions surround each sodium ion?', '6', 'Each ion is surrounded by six of the opposite charge (cubic lattice).', ['4', '8', '1']),
    ('State the conditions under which an ionic compound conducts electricity.', 'when molten or dissolved in water (aqueous)', '[1]'),
])
t3b.fixed('C2', (2, 3, 4), [
    ('Explain why molten sodium chloride conducts electricity but solid sodium chloride does not.', 'In the solid the ions are held in fixed positions in the lattice; when molten the ions are free to move and carry charge.', '1 mark: solid ions fixed; 1 mark: molten ions mobile / carry charge [2]'),
    ('Explain why magnesium oxide has a much higher melting point than sodium chloride.', 'Mg²⁺ and O²⁻ carry double charges, so the electrostatic attraction between the ions is much stronger than between Na⁺ and Cl⁻; more energy is needed to overcome it.', '1 mark: higher charges on ions; 1 mark: stronger attraction → more energy [2]'),
    ('Describe the structure of a giant ionic lattice.', 'A regular three-dimensional repeating arrangement of alternating positive and negative ions, each held by strong electrostatic attraction to the oppositely charged ions around it.', '1 mark: regular 3D arrangement; 1 mark: alternating oppositely charged ions attracted in all directions [2]'),
    ('Explain why ionic crystals are brittle and shatter when hit.', 'A force shifts a layer of ions so that ions of the same charge line up next to each other; they repel and the crystal splits.', '1 mark: layers shift; 1 mark: like charges repel [2]'),
    ('A student says, "Sodium chloride solution conducts because electrons move through it." Explain the error.', 'In the solution it is the ions (Na⁺ and Cl⁻) that move and carry the charge, not electrons.', '[2]'),
])


@t3b.add('C3', (1, 2, 3, 4))
def t3b_identify(r, D):
    k = 1 if D <= 2 else (3 if D == 3 else 4)
    picks = r.sample(STRUCT, 6)
    types = []
    chosen = []
    for s in picks:
        if s[5] not in types:
            types.append(s[5]); chosen.append(s)
        if len(chosen) == k:
            break
    if len(chosen) < k:
        return None
    labs = 'WXYZ'
    rows = '; '.join(f'{labs[i]}: m.p. {deg(s[1])}, conducts when solid: {s[2]}, conducts when molten/liquid: {s[3]}, solubility in water: {s[4]}' for i, s in enumerate(chosen))
    if k == 1:
        s = chosen[0]
        return M(r, f'A substance has these properties: m.p. {deg(s[1])}; conducts when solid: {s[2]}; conducts when molten: {s[3]}; solubility: {s[4]}. What type of structure does it have?',
                 s[5], ['giant ionic', 'simple molecular', 'giant covalent', 'metallic'], f'{cap(s[5])}: {STRUCT_WHY[s[5]]}.')
    stem = f'The properties of {k} substances are given. {rows}. Deduce the type of structure of each substance, giving a reason for each.'
    ans = '; '.join(f'{labs[i]}: {s[5]}' for i, s in enumerate(chosen))
    key = '; '.join(f'{labs[i]} {s[5]} ({STRUCT_WHY[s[5]]})' for i, s in enumerate(chosen)) + f'. 1 mark per structure with reason [{k}]'
    return Q(stem, ans, key, 'case')


@t3b.add('C2', (2, 3, 4), 'explain')
def t3b_compare(r, D):
    (n1, f1, m1), (n2, f2, m2) = r.sample(IONIC_CMP, 2)
    q = lambda f: max(abs(CAT_Q.get(el, 0)) for el in atoms(f))
    hi = (n1, m1, f1) if m1 > m2 else (n2, m2, f2)
    lo = (n2, m2, f2) if m1 > m2 else (n1, m1, f1)
    return Q(f'The melting point of {n1}, {F(f1)}, is {deg(m1)} and that of {n2}, {F(f2)}, is {deg(m2)}. Explain why both melting points are high, and suggest why {hi[0]} has the higher melting point.',
             f'Both are giant ionic lattices with many strong electrostatic attractions between oppositely charged ions that need a lot of energy to overcome. {cap(hi[0])} has ' + ('ions with larger charges (and/or smaller ions), so the attraction between them is stronger.' if q(hi[2]) > q(lo[2]) else 'smaller ions that are closer together (or more ions per unit), so the attraction is stronger.'),
             '1 mark: giant ionic lattice; 1 mark: strong electrostatic attraction needs much energy; 1 mark: comparison (charge / size of ions) [3]')


CAT_Q = {'Na': 1, 'K': 1, 'Li': 1, 'Mg': 2, 'Ca': 2, 'Al': 3, 'O': 2, 'F': 1, 'Cl': 1, 'Br': 1}


@t3b.add('C1', (1, 2, 3))
def t3b_cond(r, D):
    n, f, m = r.choice(IONIC_CMP)
    st = r.choice(['solid', 'molten', 'aqueous'])
    if n in ('magnesium oxide', 'aluminium oxide', 'calcium oxide') and st == 'aqueous':
        st = 'molten'
    cond = st != 'solid'
    return M(r, f'Does {st} {n} conduct electricity, and why?', f'{"Yes" if cond else "No"}, because its ions {"are free to move" if cond else "are held in fixed positions"}.',
             [f'{"No" if cond else "Yes"}, because its ions {"are held in fixed positions" if cond else "are free to move"}.', f'{"Yes" if cond else "No"}, because its electrons {"are free to move" if cond else "are held in fixed positions"}.',
              'Yes, because it contains delocalised electrons.', f'No, because it {"has no ions" if cond else "contains molecules"}.'],
             f'Ionic compounds conduct only when molten or aqueous, when ions can move. {cap(st)} → {"conducts" if cond else "does not conduct"}.')


def _t3b_c4(r, D):
    n, f, m = r.choice(IONIC_CMP)
    p = person(r)
    intro = r.choice([f'{p} tests a sample of {n}, {F(f)}, which melts at {deg(m)}.', f'A ceramics company in {city(r)} uses {n}, {F(f)} (m.p. {deg(m)}), in its products.'])
    soluble_ = n not in ('magnesium oxide', 'aluminium oxide', 'calcium oxide')
    parts = [
        lambda r: (f'Describe the structure of solid {n}.', 'giant ionic lattice: regular 3D arrangement of alternating positive and negative ions', '1 mark: giant lattice; 1 mark: alternating oppositely charged ions [2]'),
        lambda r: ('Explain why it has a high melting point.', 'strong electrostatic attraction between oppositely charged ions throughout the lattice needs much energy to overcome', '1 mark: strong attraction between ions; 1 mark: many / need much energy [2]'),
        lambda r: ('Describe and explain its electrical conductivity when solid and when molten.', 'solid: does not conduct, ions fixed; molten: conducts, ions free to move', '1 mark each state with reason [2]'),
        lambda r: ('Explain why the crystals are brittle.', 'a force shifts layers so like-charged ions meet and repel, so the crystal cracks', '[2]'),
        lambda r: (f'Suggest one use of {n} that depends on its high melting point.' if not soluble_ else f'Suggest why a solution of {n} in water conducts electricity.',
                   'lining furnaces / refractory material' if not soluble_ else 'the ions separate and are free to move in the solution', '[1]'),
        lambda r: ('Name the ions present and give the ratio in which they are present.', ' and '.join(f'{el}' for el in atoms(f)) + ' ions in ratio ' + ':'.join(str(v) for v in atoms(f).values()), '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t3b.add('C4', (2, 3, 4, 5), 'multi_step')(_t3b_c4)


# ---------------------------------------------------------- 3.3 covalent bonding
MOLS = [  # name, formula, single, double, triple, lone pairs (total), central atom note
    ('hydrogen', 'H2', 1, 0, 0, 0), ('chlorine', 'Cl2', 1, 0, 0, 6), ('hydrogen chloride', 'HCl', 1, 0, 0, 3), ('water', 'H2O', 2, 0, 0, 2),
    ('methane', 'CH4', 4, 0, 0, 0), ('ammonia', 'NH3', 3, 0, 0, 1), ('oxygen', 'O2', 0, 1, 0, 4), ('nitrogen', 'N2', 0, 0, 1, 2),
    ('carbon dioxide', 'CO2', 0, 2, 0, 4), ('ethane', 'C2H6', 7, 0, 0, 0), ('ethene', 'C2H4', 4, 1, 0, 0), ('methanol', 'CH3OH', 5, 0, 0, 2)]
VAL = {'H': 1, 'C': 4, 'N': 5, 'O': 6, 'Cl': 7}
for _n, _f, _s, _d, _t, _l in MOLS:
    assert sum(VAL[e] * k for e, k in atoms(_f).items()) == 2 * (_s + 2 * _d + 3 * _t) + 2 * _l, _n
BP_SERIES = [[('methane', 'CH4', -162), ('ethane', 'C2H6', -89), ('propane', 'C3H8', -42), ('butane', 'C4H10', -1)],
             [('fluorine', 'F2', -188), ('chlorine', 'Cl2', -34), ('bromine', 'Br2', 59), ('iodine', 'I2', 184)],
             [('neon', 'Ne', -246), ('argon', 'Ar', -186), ('krypton', 'Kr', -153)],
             [('methanol', 'CH3OH', 65), ('ethanol', 'C2H5OH', 78), ('propanol', 'C3H7OH', 97)]]
AR.setdefault('Kr', 84)


def bond_desc(s, d, t):
    out = []
    if s:
        out.append(f'{s} single bond{"s" if s > 1 else ""}')
    if d:
        out.append(f'{d} double bond{"s" if d > 1 else ""}')
    if t:
        out.append(f'{t} triple bond')
    return ' and '.join(out)


t3c = T('Covalent bonding in simple molecules, including double and triple bonds', 'covalent bonding', 'simple molecules', 'double and triple bonds')
t3c.fixed('C1', (1, 2), [
    ('What is a covalent bond?', 'a pair of electrons shared between two atoms', 'Covalent bond: shared pair of electrons.', ['the transfer of electrons from one atom to another', 'the attraction between oppositely charged ions', 'the attraction between ions and delocalised electrons']),
    ('How many electrons are shared in the bond between the two atoms in a nitrogen molecule, N₂?', '6', 'N≡N triple bond: 3 shared pairs = 6 electrons.', ['2', '3', '4']),
    ('Which molecule contains a double bond?', 'oxygen, O₂', 'O=O: two shared pairs.', ['hydrogen, H₂', 'chlorine, Cl₂', 'methane, CH₄']),
    ('Why do simple molecular substances have low melting points?', 'The intermolecular forces between molecules are weak.', 'Melting overcomes weak forces between molecules, not covalent bonds.',
     ['The covalent bonds are weak.', 'They contain ions.', 'Their molecules are very large.']),
    ('Why does methane not conduct electricity?', 'It has no ions or free electrons.', 'Simple molecules are neutral with all electrons in bonds.', ['Its bonds are weak.', 'It is a gas.', 'Its ions are fixed.']),
    ('Between which types of element do covalent bonds usually form?', 'between non-metal atoms', 'Non-metals share electrons to complete outer shells.', ['between metal atoms', 'between a metal and a non-metal', 'between noble gas atoms']),
    ('State the number of covalent bonds formed by a carbon atom in a molecule of methane.', '4', '[1]'),
])
t3c.fixed('C2', (2, 3, 4), [
    ('Explain why boiling water does not break the covalent bonds in water molecules.', 'Boiling only overcomes the weak intermolecular forces between molecules; the strong covalent bonds within each molecule stay intact (steam is still H₂O).', '1 mark: intermolecular forces overcome; 1 mark: covalent bonds strong / not broken [2]'),
    ('Explain why the boiling point of bromine is higher than that of chlorine.', 'Bromine molecules are larger with a greater relative molecular mass, so the intermolecular forces between them are stronger and more energy is needed to separate them.', '1 mark: larger Mr / molecules; 1 mark: stronger intermolecular forces [2]'),
    ('Explain how the atoms in a hydrogen chloride molecule achieve stable electronic configurations.', 'H and Cl each share one electron in a single covalent bond; H then has 2 outer electrons (like He) and Cl has 8 (like Ar).', '1 mark: one shared pair; 1 mark: both achieve full outer shells [2]'),
    ('Explain why a nitrogen molecule is described as having a triple bond.', 'Each N atom (2,5) needs three more electrons, so the two atoms share three pairs of electrons.', '[2]'),
    ('A student says, "Simple molecular substances have low melting points because covalent bonds are weak." Explain the error.', 'Covalent bonds are strong; melting overcomes only the weak intermolecular forces between molecules.', '[2]'),
    ('Explain why ethanol dissolves in water but the solution does not conduct electricity.', 'Ethanol is made of neutral molecules; no ions form when it dissolves, so there are no mobile charged particles.', '[2]'),
])


@t3c.add('C1', (1, 2, 3))
def t3c_count(r, D):
    n, f, s, d, t, l = r.choice(MOLS)
    what = r.choice(['shared', 'lone', 'bonds'])
    if what == 'shared':
        v = 2 * (s + 2 * d + 3 * t)
        return NM(r, f'How many electrons in total are shared in covalent bonds in one molecule of {n}, {F(f)}?', v, [v // 2, v + 2, v - 2 if v > 2 else 4, 2 * v], '',
                  f'{bond_desc(s, d, t)} → {s + 2 * d + 3 * t} shared pairs = {v} electrons.', f=lambda x: str(int(x)))
    if what == 'lone':
        return NM(r, f'How many non-bonding (lone) pairs of outer-shell electrons are there in one molecule of {n}, {F(f)}?', l, [l + 1, l + 2, max(0, l - 1), 2 * l + 1, l + 3], '',
                  f'Outer electrons not used in bonding: {l} lone pair(s).', f=lambda x: str(int(x)))
    return M(r, f'Which describes the covalent bonds in a molecule of {n}, {F(f)}?', bond_desc(s, d, t),
             [bond_desc(*x) for x in [(s + d + t, 0, 0), (max(1, s - 1), d + 1, 0), (0, 0, 1), (0, 1, 0), (s, d, t + 1), (2, 0, 0), (1, 0, 0)] if bond_desc(*x) != bond_desc(s, d, t)],
             f'{F(f)} has {bond_desc(s, d, t)}.')


@t3c.add('C3', (2, 3, 4))
def t3c_dot(r, D):
    n, f, s, d, t, l = r.choice(MOLS[2:])
    at = atoms(f)
    stem = f'Describe the dot-and-cross diagram for a molecule of {n}, {F(f)}, showing outer-shell electrons only. State the number of bonding pairs and non-bonding pairs.'
    ans = f'{bond_desc(s, d, t)} ({s + 2 * d + 3 * t} bonding pairs) and {l} non-bonding pair(s); every atom has a full outer shell (H: 2; others: 8).'
    key = f'1 mark: {bond_desc(s, d, t)} shown as shared pairs (one dot + one cross each); 1 mark: {l} lone pair(s) correctly placed; 1 mark: each atom has full outer shell [3]'
    if D >= 4:
        stem += ' Explain why the substance has a low boiling point.'
        ans += ' Low b.p.: only weak intermolecular forces between molecules need to be overcome.'
        key = key.replace(' [3]', '; 1 mark: weak intermolecular forces [4]')
    return Q(stem, ans, key, 'short')


@t3c.add('C3', (2, 3, 4, 5))
def t3c_bp(r, D):
    ser = r.choice(BP_SERIES)
    k = 2 if D <= 2 else 3
    pick = sorted(r.sample(ser, min(k, len(ser))), key=lambda x: Mr(x[1]))
    rows = ', '.join(f'{n} ({F(f)}): {deg(b)}' for n, f, b in r.sample(pick, len(pick)))
    stem = f'Boiling points of some simple molecular substances: {rows}. Describe the trend in boiling point with relative molecular mass and explain it.'
    ans = f'Boiling point increases as Mr increases ({", ".join(f"{F(f)} {mr(Mr(f))}" for n, f, b in pick)}): larger molecules have stronger intermolecular forces, so more energy is needed to separate them.'
    key = '1 mark: Mr values / ordering; 1 mark: b.p. increases with Mr; 1 mark: stronger intermolecular forces need more energy [3]'
    if D >= 4:
        Tc = r.choice([-100, -50, 0, 25, 100])
        st = '; '.join(f'{n}: {"gas" if b < Tc else "liquid or solid"}' for n, f, b in pick)
        stem += f' State which of these substances are gases at {deg(Tc)}.'
        ans += f' At {deg(Tc)}: {st}.'
        key = key.replace(' [3]', '; 1 mark: states at the temperature [4]')
    return Q(stem, ans, key, 'case')


@t3c.add('C2', (2, 3, 4), 'explain')
def t3c_how(r, D):
    n, f, s, d, t, l = r.choice(MOLS)
    els = list(atoms(f))
    need = '; '.join(f'{e} needs {8 - VAL[e] if e != "H" else 1} more electron{"s" if (8 - VAL[e] if e != "H" else 1) > 1 else ""}' for e in els)
    return Q(f'Explain, in terms of electrons, how the atoms in {n}, {F(f)}, achieve stable electronic configurations by covalent bonding.',
             f'{need}. The atoms share electrons: {bond_desc(s, d, t)}, so each H has 2 outer electrons and every other atom has 8.',
             '1 mark: electrons needed by each atom; 1 mark: number/type of shared pairs; 1 mark: full outer shells [3]' if D >= 3 else '1 mark: shared pairs; 1 mark: full outer shells [2]')


def _t3c_c4(r, D):
    n, f, s, d, t, l = r.choice(MOLS[1:])
    p = person(r)
    data = next((x for x in SUBST if x[1] == f), None)
    intro = r.choice([f'{p} is studying {n}, {F(f)}, a simple molecular substance.', f'A chemistry textbook in {city(r)} uses {n}, {F(f)}, as an example of covalent bonding.'])
    parts = [
        lambda r: ('Describe the dot-and-cross diagram of the molecule (outer shells only).', f'{bond_desc(s, d, t)}; {l} lone pair(s); full outer shells', '1 mark: bonding pairs; 1 mark: lone pairs; 1 mark: full shells [3]'),
        lambda r: ('State the total number of electrons shared in one molecule.', str(2 * (s + 2 * d + 3 * t)), '[1]'),
        lambda r: ('Explain why the substance has a low melting point.', 'weak intermolecular forces between molecules are easily overcome (covalent bonds not broken)', '1 mark: weak intermolecular forces; 1 mark: little energy needed [2]'),
        lambda r: ('Explain why it does not conduct electricity.', 'molecules are neutral; no ions or delocalised electrons', '[1]'),
        lambda r: ('Calculate its relative molecular mass.', mr(Mr(f)), ' + '.join(f'{k} × {mr(AR[e])}' for e, k in atoms(f).items()) + ' [1]'),
        lambda r: ('Suggest how its boiling point would compare with a similar substance of much larger Mr, giving a reason.', 'lower: smaller molecules have weaker intermolecular forces', '1 mark: lower; 1 mark: reason [2]'),
    ]
    if data:
        parts.append(lambda r: (f'Its melting point is {deg(data[2])} and boiling point {deg(data[3])}. State its physical state at 25 °C.', state_at(25, data[2], data[3]), '[1]'))
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t3c.add('C4', (2, 3, 4, 5), 'multi_step')(_t3c_c4)


# ---------------------------------------------------------- 3.4 giant covalent
GC = [('diamond', 'is used in the tips of cutting tools and drills', 'each carbon atom is covalently bonded to four other carbon atoms in a rigid giant tetrahedral structure; many strong bonds must be broken, so it is very hard'),
      ('diamond', 'does not conduct electricity', 'all four outer electrons of each carbon atom are used in covalent bonds, so there are no delocalised electrons or ions'),
      ('diamond', 'has a very high melting point', 'a giant structure with very many strong covalent bonds which need a great deal of energy to break'),
      ('graphite', 'conducts electricity and is used for electrodes', 'each carbon atom forms only three covalent bonds; the fourth outer electron is delocalised and can move along the layers'),
      ('graphite', 'is soft and slippery and is used as a lubricant and in pencils', 'it has layers of hexagonally arranged carbon atoms held together by weak forces, so the layers slide over each other'),
      ('graphite', 'has a very high melting point', 'strong covalent bonds within the layers must be broken to melt it'),
      ('silicon(IV) oxide', 'has a very high melting point and is used to line furnaces', 'it is a giant covalent structure in which each Si atom is bonded to four O atoms and each O atom to two Si atoms; many strong covalent bonds must be broken'),
      ('silicon(IV) oxide', 'is hard and is used in sandpaper', 'a rigid three-dimensional network of strong covalent bonds, similar to diamond'),
      ('silicon(IV) oxide', 'does not conduct electricity', 'there are no delocalised electrons and no ions'),
      ('diamond', 'is insoluble in water', 'the strong covalent bonds of the giant structure are not broken by water')]

t3d = T('Giant covalent structures: diamond, graphite and silicon(IV) oxide', 'giant covalent structures', 'diamond graphite', 'silicon(iv) oxide')
t3d.fixed('C1', (1, 2), [
    ('How many other carbon atoms is each carbon atom covalently bonded to in diamond?', '4', 'Diamond: tetrahedral, 4 bonds per C.', ['2', '3', '6']),
    ('Why does graphite conduct electricity?', 'It has delocalised electrons that can move between the layers.', 'Each C uses 3 electrons in bonds; the fourth is delocalised.', ['It contains ions.', 'Its layers can slide.', 'It has weak covalent bonds.']),
    ('Which substance has a structure similar to diamond?', 'silicon(IV) oxide', 'SiO₂ is a giant covalent 3D network.', ['graphite', 'sodium chloride', 'carbon dioxide']),
    ('Why is graphite used as a lubricant?', 'Its layers are held by weak forces and slide over each other.', 'Weak forces between layers.', ['It has a low melting point.', 'It conducts electricity.', 'Each carbon forms four bonds.']),
    ('Which property is shared by diamond, graphite and silicon(IV) oxide?', 'very high melting point', 'All giant covalent: many strong covalent bonds.', ['conducts electricity when solid', 'soft and slippery', 'soluble in water']),
    ('State the formula of silicon(IV) oxide.', 'SiO₂', '[1]'),
])
t3d.fixed('C2', (2, 3, 4), [
    ('Explain why diamond is hard but graphite is soft, even though both contain only carbon atoms.', 'In diamond each C is bonded to 4 others in a rigid 3D network of strong covalent bonds; graphite has layers held by weak forces that slide over each other.', '1 mark: diamond rigid 3D 4 bonds; 1 mark: graphite layers with weak forces slide [2]'),
    ('Explain why silicon(IV) oxide has a much higher melting point than carbon dioxide, even though both are oxides of Group IV elements.', 'SiO₂ is a giant covalent structure – melting breaks many strong covalent bonds; CO₂ is simple molecular – melting/subliming overcomes only weak intermolecular forces.', '1 mark: SiO₂ giant covalent, strong bonds broken; 1 mark: CO₂ simple molecules, weak intermolecular forces [2]'),
    ('Explain why graphite conducts electricity but diamond does not.', 'In graphite each carbon forms 3 bonds, leaving one delocalised electron per atom free to move; in diamond all 4 outer electrons are in bonds.', '[2]'),
    ('Describe the structure of silicon(IV) oxide.', 'A giant covalent lattice in which each silicon atom is covalently bonded to four oxygen atoms and each oxygen atom to two silicon atoms.', '1 mark: giant covalent; 1 mark: Si to 4 O and O to 2 Si [2]'),
    ('A student says, "Graphite has a low melting point because its layers slide easily." Explain the error.', 'Melting requires breaking the strong covalent bonds within the layers, so graphite has a very high melting point; the weak forces between layers only explain its softness.', '[2]'),
])


@t3d.add('C1', (1, 2, 3))
def t3d_why(r, D):
    sub, prop, why = r.choice(GC)
    wrong = [w for s, p, w in GC if w != why]
    return M(r, f'{cap(sub)} {prop}. Which statement explains this?', cap(why) + '.', [cap(w) + '.' for w in r.sample(wrong, 4)], f'{cap(sub)}: {why}.')


@t3d.add('C2', (2, 3, 4), 'explain')
def t3d_explain(r, D):
    sub, prop, why = r.choice(GC)
    ctx = r.choice(['', f'A company in {city(r)} chooses {sub} because it {prop}. ', f'{person(r)} reads that {sub} {prop}. '])
    return Q(f'{ctx}Explain, in terms of structure and bonding, why {sub} {prop}.', cap(why) + '.',
             '1 mark: structure named / described; 1 mark: bonding linked to the property [2]' if D <= 3 else '1 mark: giant covalent structure; 1 mark: number of bonds per atom / layers; 1 mark: linked to the property [3]')


@t3d.add('C3', (2, 3, 4, 5))
def t3d_data(r, D):
    subs = r.sample([s for s in STRUCT if s[5] in ('giant covalent', 'simple molecular', 'metallic', 'giant ionic')], 3)
    if not any(s[5] == 'giant covalent' for s in subs):
        subs[0] = r.choice([s for s in STRUCT if s[5] == 'giant covalent'])
    if len({s[0] for s in subs}) < 3:
        return None
    labs = 'ABC'
    rows = '; '.join(f'{labs[i]}: m.p. {deg(s[1])}, conducts as solid: {s[2]}, conducts when molten: {s[3]}' for i, s in enumerate(subs))
    gc = [labs[i] for i, s in enumerate(subs) if s[5] == 'giant covalent']
    stem = f'Three solids are tested. {rows}. Identify which solid(s) have a giant covalent structure and explain your choice.'
    ans = f'{", ".join(gc)}: ' + '; '.join(f'{labs[i]} is {s[5]}' for i, s in enumerate(subs))
    key = f'1 mark: {", ".join(gc)}; 1 mark: very high m.p. (many strong covalent bonds); 1 mark: does not conduct (or graphite exception) / rules out others [3]'
    if D >= 4:
        stem += ' Suggest the identity of each solid.'
        ans += '. Identities: ' + ', '.join(f'{labs[i]} could be {s[0]}' for i, s in enumerate(subs))
        key += '; identities [1]'
    return Q(stem, ans, key, 'case')


def _t3d_c4(r, D):
    p = person(r)
    intro = r.choice([f'{p} compares three substances: diamond, graphite and silicon(IV) oxide.', f'An engineering company in {city(r)} must choose materials for drill tips, electrodes and furnace linings from diamond, graphite and silicon(IV) oxide.'])
    parts = [
        lambda r: ('Describe the structure of diamond.', 'giant covalent; each C bonded to 4 others tetrahedrally', '1 mark: giant covalent; 1 mark: four bonds per C [2]'),
        lambda r: ('Describe the structure of graphite and explain how it conducts electricity.', 'layers of hexagons, each C bonded to 3 others; one delocalised electron per atom moves along the layers', '1 mark: layers / 3 bonds; 1 mark: delocalised electrons move [2]'),
        lambda r: ('State and explain which substance is used for drill tips.', 'diamond: very hard because of the rigid 3D network of strong covalent bonds', '1 mark: diamond; 1 mark: reason [2]'),
        lambda r: ('Explain why silicon(IV) oxide is suitable for lining furnaces.', 'very high melting point: many strong covalent bonds in a giant structure; also does not react/burn', '[2]'),
        lambda r: ('Suggest why graphite is used for electrodes but diamond is not.', 'graphite conducts (delocalised electrons); diamond has none', '[2]'),
        lambda r: ('Explain why carbon dioxide, unlike silicon(IV) oxide, is a gas at room temperature.', 'CO₂ is simple molecular with weak intermolecular forces; SiO₂ is giant covalent with strong covalent bonds throughout', '1 mark each [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t3d.add('C4', (2, 3, 4, 5), 'multi_step')(_t3d_c4)


# ---------------------------------------------------------- 3.5 metallic bonding
METAL_USES = [('copper', 'electrical wiring', 'it is a very good conductor of electricity and is ductile (can be drawn into wires)'),
              ('aluminium', 'overhead power cables', 'it conducts electricity well and has a low density'),
              ('aluminium', 'saucepans and cooking foil', 'it conducts heat well and is malleable'),
              ('gold', 'jewellery', 'it is malleable, shiny and unreactive'),
              ('steel (iron alloy)', 'bridges and building frames', 'it is strong'),
              ('copper', 'water pipes', 'it is malleable, does not react with water and conducts heat'),
              ('aluminium', 'aircraft bodies', 'it has a low density and (as an alloy) is strong'),
              ('silver', 'electrical contacts', 'it is the best conductor of electricity'),
              ('tungsten', 'filament lamps', 'it has a very high melting point'),
              ('zinc', 'galvanising (coating) steel', 'it is more reactive than iron and forms a protective layer')]
METAL_PROPS = [('conducts electricity when solid', 'the delocalised electrons are free to move through the structure and carry charge'),
               ('is malleable (can be hammered into shape)', 'layers of positive ions can slide over each other without breaking the metallic bonds, because the delocalised electrons move with them'),
               ('has a high melting point', 'there is strong electrostatic attraction between the positive ions and the delocalised electrons, which needs a lot of energy to overcome'),
               ('is ductile (can be drawn into wires)', 'the layers of positive ions can slide past each other while the sea of delocalised electrons holds them together'),
               ('conducts heat well', 'the delocalised electrons move freely and transfer energy quickly through the lattice')]
METALS_L = ['copper', 'iron', 'aluminium', 'magnesium', 'zinc', 'silver', 'sodium', 'calcium', 'nickel', 'potassium']

t3e = T('Metallic bonding and properties of metals', 'metallic bonding', 'properties of metals')
t3e.fixed('C1', (1, 2), [
    ('What is metallic bonding?', 'the electrostatic attraction between positive metal ions and delocalised electrons', 'Metallic bond: lattice of positive ions in a sea of delocalised electrons.',
     ['the sharing of a pair of electrons between two metal atoms', 'the attraction between positive and negative ions', 'a weak force between metal molecules']),
    ('Which particles carry the current when a piece of copper conducts electricity?', 'delocalised electrons', 'Electrons move through the lattice; the ions stay fixed.', ['copper ions', 'protons', 'copper atoms']),
    ('Why are metals malleable?', 'The layers of ions can slide over each other without breaking the bonding.', 'Delocalised electrons keep holding the ions as layers slide.', ['The metal ions are free to move.', 'The bonds are weak.', 'Metals contain molecules.']),
    ('Which statement about a metal lattice is correct?', 'It contains positive ions in a regular arrangement surrounded by delocalised electrons.', 'Description of metallic structure.',
     ['It contains positive and negative ions in a regular arrangement.', 'It contains separate metal molecules.', 'It contains neutral atoms sharing pairs of electrons.']),
    ('State two physical properties typical of metals.', 'any two: good electrical conductors, good thermal conductors, malleable, ductile, high melting point, shiny', '1 mark each [2]'),
])
t3e.fixed('C2', (2, 3, 4), [
    ('Explain why metals conduct electricity when solid but ionic compounds do not.', 'Metals have delocalised electrons that move through the lattice; in a solid ionic compound the ions are fixed and there are no free electrons.', '1 mark: metal delocalised electrons move; 1 mark: ionic solid ions fixed [2]'),
    ('Describe the structure and bonding in a metal such as magnesium.', 'A giant lattice of Mg²⁺ ions in a regular arrangement surrounded by a sea of delocalised electrons (two from each atom); strong electrostatic attraction between the ions and the electrons.', '1 mark: lattice of positive ions; 1 mark: delocalised electrons; 1 mark: electrostatic attraction [3]'),
    ('Explain why metals usually have high melting points.', 'Strong electrostatic attraction between the positive ions and the delocalised electrons throughout the giant lattice requires much energy to overcome.', '[2]'),
    ('Compare the conduction of electricity by copper and by molten sodium chloride.', 'Copper: delocalised electrons move, no chemical change. Molten NaCl: ions move to the electrodes and are discharged (electrolysis).', '1 mark: electrons in copper; 1 mark: ions in molten NaCl [2]'),
    ('A student says, "Metals conduct electricity because their positive ions move." Explain the error.', 'The positive ions are fixed in the lattice; it is the delocalised electrons that move and carry the current.', '[2]'),
])


@t3e.add('C1', (1, 2, 3))
def t3e_prop(r, D):
    prop, why = r.choice(METAL_PROPS)
    m = r.choice(METALS_L)
    return M(r, f'{cap(m)} {prop}. Which statement explains this?', cap(why) + '.', [cap(w) + '.' for p, w in METAL_PROPS if w != why] + ['The metal contains ions that are free to move.', 'The metal atoms share pairs of electrons.'],
             f'{cap(why)}.')


@t3e.add('C2', (2, 3, 4), 'explain')
def t3e_use(r, D):
    m, use, why = r.choice(METAL_USES)
    prop, pwhy = r.choice(METAL_PROPS)
    return Q(f'{cap(m)} is used for {use}. Give the properties that make it suitable, and explain, using the model of metallic bonding, why metals such as {m.split(" ")[0]} {prop}.',
             f'{cap(why)}. A metal {prop} because {pwhy}.', '1 mark: suitable property; 1 mark: lattice of positive ions and delocalised electrons; 1 mark: link to the property [3]' if D >= 3 else '1 mark: property; 1 mark: explanation [2]')


@t3e.add('C3', (1, 2, 3, 4))
def t3e_data(r, D):
    met = [s for s in STRUCT if s[5] == 'metallic']
    other = [s for s in STRUCT if s[5] != 'metallic']
    pick = r.sample(met, 1) + r.sample(other, 3)
    r.shuffle(pick)
    labs = 'PQRS'
    rows = '; '.join(f'{labs[i]}: m.p. {deg(s[1])}, conducts as solid: {s[2]}, conducts when molten: {s[3]}' for i, s in enumerate(pick))
    mi = [labs[i] for i, s in enumerate(pick) if s[5] == 'metallic']
    if len(mi) != 1 or any(s[0] == 'graphite' for s in pick):
        return None
    if D <= 2:
        return M(r, f'Which substance is a metal? {rows}.', mi[0], list(labs), f'{mi[0]} conducts when solid and molten: delocalised electrons → metallic.')
    stem = f'Data for four substances: {rows}. Identify the metal and explain how the data support your answer. Describe the type of structure of each of the other substances.'
    ans = f'{mi[0]} is the metal (conducts as solid and liquid – delocalised electrons). ' + '; '.join(f'{labs[i]}: {s[5]}' for i, s in enumerate(pick) if s[5] != 'metallic')
    return Q(stem, ans, '1 mark: metal identified; 1 mark: conducts when solid due to delocalised electrons; 1 mark per two other structures correct up to [2] total [4]', 'case')


def _t3e_c4(r, D):
    m, use, why = r.choice(METAL_USES[:8])
    p = person(r)
    intro = r.choice([f'{p} investigates why {m} is chosen for {use}.', f'An engineer in {city(r)} explains to apprentices why {m} is used for {use}.'])
    parts = [
        lambda r: ('Describe the structure and bonding in a metal.', 'giant lattice of positive ions in a sea of delocalised electrons; electrostatic attraction between them', '1 mark: positive ions lattice; 1 mark: delocalised electrons; 1 mark: attraction [3]'),
        lambda r: (f'State the properties that make {m} suitable for {use}.', cap(why), '[2]'),
        lambda r: ('Explain why metals conduct electricity.', 'delocalised electrons move through the structure when a p.d. is applied', '[2]'),
        lambda r: ('Explain why metals can be bent and shaped without breaking.', 'layers of ions slide over each other; delocalised electrons keep the bonding', '[2]'),
        lambda r: ('Explain why metals have high melting points.', 'strong attraction between positive ions and delocalised electrons needs much energy to overcome', '[2]'),
        lambda r: ('Suggest why the alloy is often harder than the pure metal.', 'different-sized atoms disrupt the regular layers so they cannot slide easily', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t3e.add('C4', (2, 3, 4, 5), 'multi_step')(_t3e_c4)

CHAPTERS[3] = [t3a, t3b, t3c, t3d, t3e]


# ===================================================================== Ch4 Formulae and equations
CATS = dict(CAT)
ANS = dict(AN)
ANS.update({'O': ('oxide', 'O', 2), 'S': ('sulfide', 'S', 2), 'F': ('fluoride', 'F', 1), 'N': ('nitride', 'N', 3), 'PO4': ('phosphate', 'PO4', 3), 'HCO3': ('hydrogencarbonate', 'HCO3', 1)})
POLYS = {'NH4', 'NO3', 'SO4', 'CO3', 'OH', 'PO4', 'HCO3'}
FORMULA_PAIRS = [(c, a) for c in CATS for a in ANS if not ((c, a) in {('NH4', 'O'), ('NH4', 'S'), ('NH4', 'N'), ('Ag', 'OH'), ('Ag', 'CO3'), ('NH4', 'OH'), ('Al', 'CO3'), ('Fe3', 'CO3'),
                                                                     ('Ag', 'N'), ('Cu', 'N'), ('Pb', 'N'), ('Fe2', 'N'), ('Fe3', 'N'), ('Zn', 'N'), ('Ba', 'N'), ('K', 'N'), ('Na', 'N'), ('NH4', 'F'),
                                                                     ('Ag', 'HCO3'), ('Al', 'HCO3'), ('Fe3', 'HCO3'), ('Pb', 'HCO3'), ('Cu', 'HCO3'), ('Fe2', 'HCO3'), ('Zn', 'HCO3'), ('Al', 'S'), ('Fe3', 'S'), ('Al', 'N'), ('Fe3', 'PO4'), ('Al', 'PO4')})]


def fion(c, a):
    cq, aq = CATS[c][2], ANS[a][2]
    l = cq * aq // math.gcd(cq, aq)
    nc, na = l // cq, l // aq
    cs, as_ = CATS[c][1], ANS[a][1]
    left = (f'({cs}){nc}' if cs in POLYS else f'{cs}{nc}') if nc > 1 else cs
    right = (f'({as_}){na}' if as_ in POLYS else f'{as_}{na}') if na > 1 else as_
    return left + right


def nion(c, a):
    return f'{CATS[c][0]} {ANS[a][0]}'


def ionf(sym, q, neg_=False):
    c = ('' if q == 1 else str(q)) + ('-' if neg_ else '+')
    return F(sym + '^' + c)


COVAL = [('carbon', 'chlorine', 'CCl4', 'tetrachloromethane'), ('nitrogen', 'hydrogen', 'NH3', 'ammonia'), ('hydrogen', 'sulfur', 'H2S', 'hydrogen sulfide'),
         ('phosphorus', 'chlorine', 'PCl3', 'phosphorus trichloride'), ('silicon', 'oxygen', 'SiO2', 'silicon(IV) oxide'), ('carbon', 'oxygen', 'CO2', 'carbon dioxide'),
         ('silicon', 'chlorine', 'SiCl4', 'silicon tetrachloride'), ('nitrogen', 'chlorine', 'NCl3', 'nitrogen trichloride'), ('oxygen', 'fluorine', 'OF2', 'oxygen difluoride'),
         ('hydrogen', 'bromine', 'HBr', 'hydrogen bromide'), ('carbon', 'sulfur', 'CS2', 'carbon disulfide'), ('phosphorus', 'hydrogen', 'PH3', 'phosphine'),
         ('carbon', 'hydrogen', 'CH4', 'methane'), ('sulfur', 'chlorine', 'SCl2', 'sulfur dichloride')]
VALENCY = {'carbon': 4, 'silicon': 4, 'nitrogen': 3, 'phosphorus': 3, 'oxygen': 2, 'sulfur': 2, 'hydrogen': 1, 'chlorine': 1, 'fluorine': 1, 'bromine': 1}
COUNT_F = ['Ca(OH)2', 'Al2(SO4)3', '(NH4)2SO4', 'CuSO4.5H2O', 'Mg(NO3)2', 'Fe2(SO4)3', 'Ca3(PO4)2', 'C6H12O6', 'C2H5OH', 'CH3COOH', 'Na2CO3.10H2O', '(NH4)3PO4', 'Pb(NO3)2', 'K2Cr2O7',
           'Al(NO3)3', 'Ba(OH)2', 'MgSO4.7H2O', 'Cu(NO3)2', 'NH4NO3', 'C3H7OH', 'Fe(OH)3', 'Zn(NO3)2', 'CoCl2.6H2O', 'Na3PO4']
AR.update({k: v for k, v in {'Cr': 52, 'Co': 59, 'Kr': 84}.items() if k not in AR})
MOLDESC = [('two carbon atoms, six hydrogen atoms and one oxygen atom', 'C2H6O'), ('one sulfur atom and three oxygen atoms', 'SO3'), ('two nitrogen atoms and four oxygen atoms', 'N2O4'),
           ('six carbon atoms, twelve hydrogen atoms and six oxygen atoms', 'C6H12O6'), ('three carbon atoms and eight hydrogen atoms', 'C3H8'), ('one carbon atom and one oxygen atom', 'CO'),
           ('four phosphorus atoms and ten oxygen atoms', 'P4O10'), ('two hydrogen atoms and two oxygen atoms', 'H2O2'), ('one nitrogen atom and two oxygen atoms', 'NO2'),
           ('two carbon atoms, four hydrogen atoms and two oxygen atoms', 'C2H4O2'), ('one carbon atom, one hydrogen atom and three chlorine atoms', 'CHCl3'), ('four carbon atoms and ten hydrogen atoms', 'C4H10')]

t4a = T('Writing chemical formulae from ions, valency and models', 'writing chemical formulae', 'ions valency models')
t4a.fixed('C1', (1, 2), [
    ('What is the formula of aluminium oxide?', 'Al₂O₃', 'Al³⁺ and O²⁻: 2 × 3+ = 3 × 2−.', ['AlO', 'Al₃O₂', 'AlO₃']),
    ('What is the formula of the sulfate ion?', 'SO₄²⁻', 'Sulfate: SO₄²⁻.', ['SO₃²⁻', 'SO₄⁻', 'S²⁻']),
    ('What is the formula of ammonium sulfate?', '(NH₄)₂SO₄', 'NH₄⁺ and SO₄²⁻: two ammonium ions per sulfate.', ['NH₄SO₄', 'NH₄(SO₄)₂', '(NH₃)₂SO₄']),
    ('Which ion has a charge of 3−?', 'phosphate', 'PO₄³⁻ (also nitride N³⁻).', ['nitrate', 'sulfate', 'carbonate']),
    ('Which formula represents a molecule containing a total of five atoms?', 'CH₄', 'CH₄: 1 + 4 = 5 atoms.', ['H₂O', 'NH₃', 'CO₂']),
    ('State the formula of the nitrate ion.', 'NO₃⁻', '[1]'),
    ('State the formula of the hydroxide ion.', 'OH⁻', '[1]'),
])
t4a.fixed('C2', (2, 3, 4), [
    ('Explain why brackets are needed in the formula Ca(OH)₂ but not in NaOH.', 'Two hydroxide ions are needed to balance Ca²⁺; the bracket shows that the subscript 2 applies to the whole OH group. NaOH contains only one OH⁻, so no bracket is needed.', '1 mark: two OH⁻ to balance 2+; 1 mark: bracket applies subscript to whole group [2]'),
    ('A student writes the formula of magnesium chloride as MgCl. Explain the error and give the correct formula.', 'Mg forms Mg²⁺ and chloride is Cl⁻, so two chloride ions are needed: MgCl₂.', '1 mark: charges; 1 mark: MgCl₂ [2]'),
    ('Explain how the formula of a compound of iron(III) can be deduced from its name, using iron(III) sulfate as an example.', 'The Roman numeral shows the ion is Fe³⁺; sulfate is SO₄²⁻; the lowest ratio giving zero charge is 2 Fe³⁺ : 3 SO₄²⁻, so Fe₂(SO₄)₃.', '1 mark: Fe³⁺ from numeral; 1 mark: charge balance → Fe₂(SO₄)₃ [2]'),
    ('Explain the difference between the formulae 2H₂O and H₂O₂.', '2H₂O means two molecules of water (4 H and 2 O atoms in total); H₂O₂ is one molecule of hydrogen peroxide containing 2 H and 2 O atoms.', '[2]'),
    ('Explain how the valency of carbon and oxygen can be used to deduce the formula of carbon dioxide.', 'Carbon has valency 4 and oxygen valency 2, so one carbon combines with two oxygens (each forming a double bond): CO₂.', '[2]'),
])


@t4a.add('C1', (1, 2, 3))
def t4a_ionf(r, D):
    c, a = r.choice(FORMULA_PAIRS)
    f = fion(c, a)
    cs, as_ = CATS[c][1], ANS[a][1]
    wr = {F(cs + as_), F(f.replace('(', '').replace(')', '')) if '(' in f else F(cs + '2' + as_), F(f'{cs}({as_})2' if as_ in POLYS else cs + as_ + '2'), F(f'{cs}2{as_}' if cs not in POLYS else f'({cs})2{as_}'),
          F(f'{cs}{as_}3'), F(f'{cs}3{as_}2' if cs not in POLYS else f'({cs})3{as_}')}
    wr.discard(F(f))
    return M(r, r.choice([f'What is the formula of {nion(c, a)}?', f'A bottle is labelled "{nion(c, a)}". Which formula should also be on the label?']), F(f), list(wr),
             f'Ions: {ionf(cs, CATS[c][2])} and {ionf(as_, ANS[a][2], True)}; balance charges → {F(f)}.')


@t4a.add('C3', (1, 2, 3, 4))
def t4a_write(r, D):
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    ps = r.sample(FORMULA_PAIRS, k)
    stem = 'Use the charges on the ions to write the formula of each compound: ' + ', '.join(nion(*p) for p in ps) + '.'
    if D >= 3:
        stem = 'Use the ion charges given to write the formula of each compound: ' + ', '.join(f'{nion(*p)} ({ionf(CATS[p[0]][1], CATS[p[0]][2])}, {ionf(ANS[p[1]][1], ANS[p[1]][2], True)})' for p in ps) + '.'
        stem = stem.replace('Use the ion charges given', r.choice(['Use the ion charges given', 'Using the ion charges shown in brackets,']))
    ans = '; '.join(f'{nion(*p)}: {F(fion(*p))}' for p in ps)
    return Q(stem, ans, f'{ans}. 1 mark each [{k}]', 'short')


@t4a.add('C3', (1, 2, 3))
def t4a_count(r, D):
    f = r.choice(COUNT_F)
    at = atoms(f)
    tot = sum(at.values())
    if D == 1:
        return NM(r, f'How many atoms in total are shown in the formula {F(f)}?', tot, [tot - 1, tot + 1, tot + 2, len(at), tot - 2, tot + 3], '',
                  ', '.join(f'{e}: {n}' for e, n in at.items()) + f' → {tot}.', f=lambda x: str(int(x)))
    return Q(f'State the number of atoms of each element in the formula {F(f)}, and the total number of atoms.', ', '.join(f'{e} {n}' for e, n in at.items()) + f'; total {tot}',
             f'{", ".join(f"{e} {n}" for e, n in at.items())} [1]; total {tot} [1]', 'short')


@t4a.add('C2', (2, 3, 4), 'explain')
def t4a_valency(r, D):
    a, b, f, n = r.choice(COVAL)
    va, vb = VALENCY[a], VALENCY[b]
    if D <= 2:
        return Q(f'{cap(a)} has a valency of {va} and {b} a valency of {vb}. Deduce the formula of the compound they form and explain your reasoning.', F(f),
                 f'Combining powers must match: {F(f)} ({n}) [2]')
    return Q(f'{who(r)} is told that {a} has a valency of {va} and {b} has a valency of {vb}. Deduce the formula of the covalent compound formed and explain how many bonds each atom makes.',
             f'{F(f)} ({n}): each {a} atom forms {va} bond(s) and each {b} atom forms {vb}; the numbers of bonds must match.',
             f'1 mark: formula {F(f)}; 1 mark: bonds per atom = valency; 1 mark: ratio so total bonds match [3]')


@t4a.add('C1', (1, 2, 3))
def t4a_model(r, D):
    d, f = r.choice(MOLDESC)
    at = atoms(f)
    wrong = []
    keys = list(at)
    for i in range(len(keys)):
        alt = dict(at)
        alt[keys[i]] = alt[keys[i]] + 1
        wrong.append(''.join(e + (str(v) if v > 1 else '') for e, v in alt.items()))
    wrong.append(''.join(e for e in at))
    wrong.append(''.join(e + (str(v * 2) if v * 2 > 1 else '') for e, v in at.items()))
    return M(r, f'A model of a molecule shows {d}. What is the molecular formula?', F(f), [F(w) for w in wrong], f'Count atoms of each element → {F(f)}.')


def _t4a_c4(r, D):
    ps = r.sample(FORMULA_PAIRS, 3)
    p = person(r)
    intro = r.choice([f'{p} is labelling bottles of chemicals in {lab(r)}. The bottles contain {nion(*ps[0])}, {nion(*ps[1])} and {nion(*ps[2])}.',
                      f'A technician in {city(r)} needs formulae for three compounds: {nion(*ps[0])}, {nion(*ps[1])} and {nion(*ps[2])}.'])
    parts = [
        lambda r: ('Give the formula and charge of each ion present in the three compounds.', '; '.join(f'{ionf(CATS[c][1], CATS[c][2])}, {ionf(ANS[a][1], ANS[a][2], True)}' for c, a in ps), '1 mark per compound [3]'),
        lambda r: ('Write the formula of each compound.', '; '.join(F(fion(*x)) for x in ps), '1 mark each [3]'),
        lambda r: (f'State the total number of atoms in the formula of {nion(*ps[0])}.', str(sum(atoms(fion(*ps[0])).values())), '[1]'),
        lambda r: (f'Calculate the relative formula mass of {nion(*ps[1])}.', mr(Mr(fion(*ps[1]))), ' + '.join(f'{k} × {mr(AR[e])}' for e, k in atoms(fion(*ps[1])).items()) + ' [2]'),
        lambda r: ('Explain why the formula of a compound containing a polyatomic ion sometimes needs brackets.', 'to show that the subscript multiplies the whole group of atoms in the ion', '[1]'),
        lambda r: (f'Explain why the formula of {nion(*ps[2])} contains the ions in that ratio.', 'the total positive charge must equal the total negative charge (compound is neutral)', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t4a.add('C4', (2, 3, 4, 5), 'multi_step')(_t4a_c4)
t4a.add('C3', (4, 5), 'multi_step')(_t4a_c4)


# ---------------------------------------------------------- 4.2 equations
EQS = [  # word equation, balanced with states
    ('magnesium + oxygen → magnesium oxide', '2Mg(s) + O2(g) -> 2MgO(s)'),
    ('hydrogen + oxygen → water', '2H2(g) + O2(g) -> 2H2O(l)'),
    ('methane + oxygen → carbon dioxide + water', 'CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)'),
    ('sodium + water → sodium hydroxide + hydrogen', '2Na(s) + 2H2O(l) -> 2NaOH(aq) + H2(g)'),
    ('calcium carbonate → calcium oxide + carbon dioxide', 'CaCO3(s) -> CaO(s) + CO2(g)'),
    ('aluminium + oxygen → aluminium oxide', '4Al(s) + 3O2(g) -> 2Al2O3(s)'),
    ('iron + chlorine → iron(III) chloride', '2Fe(s) + 3Cl2(g) -> 2FeCl3(s)'),
    ('nitrogen + hydrogen → ammonia', 'N2(g) + 3H2(g) -> 2NH3(g)'),
    ('zinc + hydrochloric acid → zinc chloride + hydrogen', 'Zn(s) + 2HCl(aq) -> ZnCl2(aq) + H2(g)'),
    ('magnesium + hydrochloric acid → magnesium chloride + hydrogen', 'Mg(s) + 2HCl(aq) -> MgCl2(aq) + H2(g)'),
    ('calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide', 'CaCO3(s) + 2HCl(aq) -> CaCl2(aq) + H2O(l) + CO2(g)'),
    ('sodium hydroxide + sulfuric acid → sodium sulfate + water', '2NaOH(aq) + H2SO4(aq) -> Na2SO4(aq) + 2H2O(l)'),
    ('copper(II) oxide + sulfuric acid → copper(II) sulfate + water', 'CuO(s) + H2SO4(aq) -> CuSO4(aq) + H2O(l)'),
    ('propane + oxygen → carbon dioxide + water', 'C3H8(g) + 5O2(g) -> 3CO2(g) + 4H2O(l)'),
    ('ethane + oxygen → carbon dioxide + water', '2C2H6(g) + 7O2(g) -> 4CO2(g) + 6H2O(l)'),
    ('iron(III) oxide + carbon monoxide → iron + carbon dioxide', 'Fe2O3(s) + 3CO(g) -> 2Fe(l) + 3CO2(g)'),
    ('hydrogen peroxide → water + oxygen', '2H2O2(aq) -> 2H2O(l) + O2(g)'),
    ('sodium + chlorine → sodium chloride', '2Na(s) + Cl2(g) -> 2NaCl(s)'),
    ('potassium + water → potassium hydroxide + hydrogen', '2K(s) + 2H2O(l) -> 2KOH(aq) + H2(g)'),
    ('calcium + water → calcium hydroxide + hydrogen', 'Ca(s) + 2H2O(l) -> Ca(OH)2(aq) + H2(g)'),
    ('aluminium + hydrochloric acid → aluminium chloride + hydrogen', '2Al(s) + 6HCl(aq) -> 2AlCl3(aq) + 3H2(g)'),
    ('ethanol + oxygen → carbon dioxide + water', 'C2H5OH(l) + 3O2(g) -> 2CO2(g) + 3H2O(l)'),
    ('magnesium + steam → magnesium oxide + hydrogen', 'Mg(s) + H2O(g) -> MgO(s) + H2(g)'),
    ('copper(II) carbonate → copper(II) oxide + carbon dioxide', 'CuCO3(s) -> CuO(s) + CO2(g)'),
    ('lead(II) nitrate + potassium iodide → lead(II) iodide + potassium nitrate', 'Pb(NO3)2(aq) + 2KI(aq) -> PbI2(s) + 2KNO3(aq)'),
    ('silver nitrate + sodium chloride → silver chloride + sodium nitrate', 'AgNO3(aq) + NaCl(aq) -> AgCl(s) + NaNO3(aq)'),
    ('chlorine + potassium bromide → potassium chloride + bromine', 'Cl2(aq) + 2KBr(aq) -> 2KCl(aq) + Br2(aq)'),
    ('zinc + copper(II) sulfate → zinc sulfate + copper', 'Zn(s) + CuSO4(aq) -> ZnSO4(aq) + Cu(s)'),
    ('sodium carbonate + hydrochloric acid → sodium chloride + water + carbon dioxide', 'Na2CO3(s) + 2HCl(aq) -> 2NaCl(aq) + H2O(l) + CO2(g)'),
    ('ammonia + hydrogen chloride → ammonium chloride', 'NH3(g) + HCl(g) -> NH4Cl(s)'),
    ('iron + oxygen → iron(III) oxide', '4Fe(s) + 3O2(g) -> 2Fe2O3(s)'),
    ('magnesium + carbon dioxide → magnesium oxide + carbon', '2Mg(s) + CO2(g) -> 2MgO(s) + C(s)'),
    ('calcium oxide + water → calcium hydroxide', 'CaO(s) + H2O(l) -> Ca(OH)2(s)'),
    ('calcium hydroxide + hydrochloric acid → calcium chloride + water', 'Ca(OH)2(aq) + 2HCl(aq) -> CaCl2(aq) + 2H2O(l)'),
    ('lithium + oxygen → lithium oxide', '4Li(s) + O2(g) -> 2Li2O(s)'),
    ('potassium hydroxide + nitric acid → potassium nitrate + water', 'KOH(aq) + HNO3(aq) -> KNO3(aq) + H2O(l)'),
    ('magnesium + sulfuric acid → magnesium sulfate + hydrogen', 'Mg(s) + H2SO4(aq) -> MgSO4(aq) + H2(g)'),
    ('butane + oxygen → carbon dioxide + water', '2C4H10(g) + 13O2(g) -> 8CO2(g) + 10H2O(l)'),
    ('sulfur dioxide + oxygen → sulfur trioxide', '2SO2(g) + O2(g) -> 2SO3(g)'),
    ('iron(III) oxide + aluminium → aluminium oxide + iron', 'Fe2O3(s) + 2Al(s) -> Al2O3(s) + 2Fe(l)'),
    ('copper(II) oxide + hydrogen → copper + water', 'CuO(s) + H2(g) -> Cu(s) + H2O(l)'),
    ('zinc carbonate → zinc oxide + carbon dioxide', 'ZnCO3(s) -> ZnO(s) + CO2(g)'),
    ('barium chloride + sodium sulfate → barium sulfate + sodium chloride', 'BaCl2(aq) + Na2SO4(aq) -> BaSO4(s) + 2NaCl(aq)'),
    ('ammonia + sulfuric acid → ammonium sulfate', '2NH3(aq) + H2SO4(aq) -> (NH4)2SO4(aq)'),
    ('lithium + water → lithium hydroxide + hydrogen', '2Li(s) + 2H2O(l) -> 2LiOH(aq) + H2(g)'),
    ('carbon + oxygen → carbon monoxide', '2C(s) + O2(g) -> 2CO(g)'),
    ('glucose → ethanol + carbon dioxide', 'C6H12O6(aq) -> 2C2H5OH(aq) + 2CO2(g)'),
]
for _w, _e in EQS:
    assert balanced(_e), _e
STATE_W = {'s': 'solid', 'l': 'liquid', 'g': 'gas', 'aq': 'aqueous'}

t4b = T('Word equations and balanced symbol equations with state symbols', 'word equations', 'balanced symbol equations', 'state symbols')
t4b.fixed('C1', (1, 2), [
    ('What does the state symbol (aq) mean?', 'dissolved in water', '(aq) = aqueous solution.', ['a liquid', 'a gas', 'a solid']),
    ('Why must a chemical equation be balanced?', 'Atoms are not created or destroyed in a reaction.', 'Conservation of mass: same numbers of each atom on each side.',
     ['Molecules are not created or destroyed.', 'The volumes of gases must be equal.', 'The number of substances must be equal.']),
    ('Which state symbol should be used for water at room temperature?', '(l)', 'Water is a liquid at room temperature.', ['(aq)', '(s)', '(g)']),
    ('In the equation 2H₂ + O₂ → 2H₂O, how many hydrogen atoms are shown on the left?', '4', '2 × H₂ = 4 H atoms.', ['2', '6', '8']),
    ('When balancing an equation, what must not be changed?', 'the formulae of the substances', 'Only coefficients (numbers in front) may be changed.', ['the numbers in front of the formulae', 'the state symbols', 'the order of the products']),
    ('State the meaning of the state symbol (g).', 'gas', '[1]'),
])
t4b.fixed('C2', (2, 3, 4), [
    ('A student balances H₂ + O₂ → H₂O by writing H₂ + O₂ → H₂O₂. Explain why this is wrong and give the correct equation.', 'Changing H₂O to H₂O₂ changes the substance (hydrogen peroxide). Only coefficients may be changed: 2H₂ + O₂ → 2H₂O.', '1 mark: cannot change formula; 1 mark: correct equation [2]'),
    ('Explain why the total mass seems to decrease when calcium carbonate is heated in an open crucible.', 'Carbon dioxide gas is produced and escapes into the air; mass is conserved but the gas is not weighed.', '1 mark: CO₂ gas escapes; 1 mark: mass conserved overall [2]'),
    ('Explain why the total mass stays the same when silver nitrate solution is added to sodium chloride solution in a closed flask.', 'No atoms are gained or lost; all products, including the precipitate, stay in the flask.', '[2]'),
    ('Explain what the coefficient 2 in 2NaOH tells you.', 'There are two formula units of sodium hydroxide, i.e. 2 Na, 2 O and 2 H atoms (2 mol in mole terms).', '[2]'),
    ('Explain why magnesium increases in mass when it is burned in air.', 'Magnesium combines with oxygen from the air to form magnesium oxide; the oxygen atoms add to the mass.', '[2]'),
])


@t4b.add('C3', (1, 2, 3, 4))
def t4b_balance(r, D):
    w, e = r.choice(EQS)
    co = coeffs(e)
    if D == 1:
        L, R = parse_eq(e)
        allsp = L + R
        i = r.choice([j for j, (n, f, s) in enumerate(allsp) if True])
        n, f, s = allsp[i]
        shown = ' + '.join((('x' if j == i else (str(m) if m > 1 else '')) + F(g)) for j, (m, g, _) in enumerate(L)) + ' → ' + ' + '.join((('x' if j + len(L) == i else (str(m) if m > 1 else '')) + F(g)) for j, (m, g, _) in enumerate(R))
        return NM(r, f'The equation {shown} is balanced. What is the value of x?', n, [n + 1, n + 2, max(1, n - 1), 2 * n, n + 3, 1 if n != 1 else 4], '', f'Balanced: {E(nostate(e))}.', f=lambda x: str(int(x)))
    stem = f'Balance the equation: {E(unbal(e))}'
    ans = E(nostate(e))
    key = f'{ans} [2]' if max(co) > 2 else f'{ans} [1]'
    if D >= 3:
        stem = f'Write the balanced symbol equation, with state symbols, for the reaction: {w}.'
        ans = E(e)
        key = f'{ans}: 1 mark formulae; 1 mark balancing; 1 mark state symbols [3]'
    if D >= 4:
        L, R = parse_eq(e)
        nat = sum(n * sum(atoms(f).values()) for n, f, _ in L)
        stem += ' State the total number of atoms on each side of your equation.'
        ans += f'; {nat} atoms on each side'
        key = key.replace(' [3]', f'; 1 mark: {nat} atoms each side [4]')
    return Q(stem, ans, key, 'short')


@t4b.add('C1', (1, 2, 3))
def t4b_state(r, D):
    w, e = r.choice(EQS)
    L, R = parse_eq(e)
    n, f, s = r.choice(L + R)
    if f in ('H2O',) and s == 'l':
        pass
    return M(r, f'In the reaction {w}, which state symbol should be written after {F(f)}?', f'({s})', ['(s)', '(l)', '(g)', '(aq)'], f'{F(f)} is {STATE_W[s]} under these conditions: {E(e)}.')


@t4b.add('C3', (2, 3, 4, 5))
def t4b_mass(r, D):
    w, e = r.choice(EQS)
    L, R = parse_eq(e)
    k = r.choice([0.5, 1, 2, 0.25, 0.1, 0.2])
    masses = [(n * Mr(f) * k, f) for n, f, _ in L + R]
    hide = r.randrange(len(masses))
    if any(m != int(m) and abs(m * 10 - round(m * 10)) > 1e-9 for m, _ in masses):
        return None
    shown = '; '.join(f'{F(f)}: {"?" if i == hide else mr(m) + " g"}' for i, (m, f) in enumerate(masses))
    p = person(r)
    stem = f'{p} carries out the reaction {E(nostate(e))} in a closed container. The masses of the substances that react and are formed are: {shown}. Calculate the missing mass and state the law you used.'
    tot_l = sum(m for m, _ in masses[:len(L)])
    key = f'mass of reactants = mass of products (conservation of mass) [1]; missing mass = {mr(masses[hide][0])} g [1]'
    if D >= 4:
        stem += ' Explain, in terms of atoms, why this law applies.'
        key += '; atoms are rearranged, not created or destroyed [1]'
    return Q(stem, f'{mr(masses[hide][0])} g; conservation of mass (total mass of reactants {mr(tot_l)} g = total mass of products).', key, 'numerical')


@t4b.add('C2', (2, 3, 4), 'explain')
def t4b_error(r, D):
    w, e = r.choice([x for x in EQS if max(coeffs(x[1])) >= 2])
    L, R = parse_eq(e)
    wrong = E(unbal(e))
    p = person(r)
    return Q(f'{p} writes the equation for "{w}" as {wrong}. Explain why the equation is not acceptable and write it correctly with state symbols.',
             f'It is not balanced: the numbers of atoms of each element are not equal on both sides. Correct: {E(e)}.',
             '1 mark: not balanced / atoms not conserved; 1 mark: correct coefficients; 1 mark: state symbols [3]' if D >= 3 else '1 mark: not balanced; 1 mark: correct balanced equation [2]')


def _t4b_c4(r, D):
    w, e = r.choice(EQS)
    L, R = parse_eq(e)
    p = person(r)
    intro = r.choice([f'{p} investigates the reaction: {w}.', f'In {lab(r)} in {city(r)}, students study the reaction {w}.'])
    cmp_ = [x for x in L + R if sum(atoms(x[1]).values()) > 1 and len(atoms(x[1])) > 1]
    n0, f0, _ = cmp_[0] if cmp_ else L[0]
    parts = [
        lambda r: ('Write the balanced symbol equation, including state symbols.', E(e), '1 mark formulae; 1 mark balanced; 1 mark state symbols [3]'),
        lambda r: ('State the number of atoms of each element on the left-hand side.', ', '.join(f'{el} {sum(n * atoms(f).get(el, 0) for n, f, _ in L)}' for el in sorted({el for _, f, _ in L for el in atoms(f)})), '[1]'),
        lambda r: (f'Calculate the relative formula mass of {F(f0)}. {ar_data(f0)}', mr(Mr(f0)), mr_work(f0) + ' [1]'),
        lambda r: ('Explain why the total mass of the reactants equals the total mass of the products.', 'atoms are rearranged; none are created or destroyed', '[1]'),
        lambda r: ('Suggest why the mass of the reaction container may change if the reaction is done in an open beaker.', 'a gas is given off / taken in from the air' if any(s == 'g' for _, _, s in L + R) else 'no change expected: no gases are involved', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t4b.add('C4', (2, 3, 4, 5), 'multi_step')(_t4b_c4)


# ---------------------------------------------------------- 4.3 ionic equations
IONIC_EQS = [  # description, full equation, ionic equation, spectators
    ('neutralisation of hydrochloric acid by sodium hydroxide', 'HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)', 'H+(aq) + OH-(aq) -> H2O(l)', 'Na⁺ and Cl⁻'),
    ('neutralisation of nitric acid by potassium hydroxide', 'HNO3(aq) + KOH(aq) -> KNO3(aq) + H2O(l)', 'H+(aq) + OH-(aq) -> H2O(l)', 'K⁺ and NO₃⁻'),
    ('neutralisation of sulfuric acid by sodium hydroxide', 'H2SO4(aq) + 2NaOH(aq) -> Na2SO4(aq) + 2H2O(l)', 'H+(aq) + OH-(aq) -> H2O(l)', 'Na⁺ and SO₄²⁻'),
    ('reaction of zinc with copper(II) sulfate solution', 'Zn(s) + CuSO4(aq) -> ZnSO4(aq) + Cu(s)', 'Zn(s) + Cu2+(aq) -> Zn2+(aq) + Cu(s)', 'SO₄²⁻'),
    ('reaction of magnesium with copper(II) sulfate solution', 'Mg(s) + CuSO4(aq) -> MgSO4(aq) + Cu(s)', 'Mg(s) + Cu2+(aq) -> Mg2+(aq) + Cu(s)', 'SO₄²⁻'),
    ('reaction of iron with copper(II) sulfate solution', 'Fe(s) + CuSO4(aq) -> FeSO4(aq) + Cu(s)', 'Fe(s) + Cu2+(aq) -> Fe2+(aq) + Cu(s)', 'SO₄²⁻'),
    ('reaction of copper with silver nitrate solution', 'Cu(s) + 2AgNO3(aq) -> Cu(NO3)2(aq) + 2Ag(s)', 'Cu(s) + 2Ag+(aq) -> Cu2+(aq) + 2Ag(s)', 'NO₃⁻'),
    ('reaction of chlorine with potassium bromide solution', 'Cl2(aq) + 2KBr(aq) -> 2KCl(aq) + Br2(aq)', 'Cl2(aq) + 2Br-(aq) -> 2Cl-(aq) + Br2(aq)', 'K⁺'),
    ('reaction of chlorine with sodium iodide solution', 'Cl2(aq) + 2NaI(aq) -> 2NaCl(aq) + I2(aq)', 'Cl2(aq) + 2I-(aq) -> 2Cl-(aq) + I2(aq)', 'Na⁺'),
    ('reaction of bromine with potassium iodide solution', 'Br2(aq) + 2KI(aq) -> 2KBr(aq) + I2(aq)', 'Br2(aq) + 2I-(aq) -> 2Br-(aq) + I2(aq)', 'K⁺'),
    ('reaction of magnesium with hydrochloric acid', 'Mg(s) + 2HCl(aq) -> MgCl2(aq) + H2(g)', 'Mg(s) + 2H+(aq) -> Mg2+(aq) + H2(g)', 'Cl⁻'),
    ('reaction of zinc with sulfuric acid', 'Zn(s) + H2SO4(aq) -> ZnSO4(aq) + H2(g)', 'Zn(s) + 2H+(aq) -> Zn2+(aq) + H2(g)', 'SO₄²⁻'),
    ('reaction of sodium carbonate solution with hydrochloric acid', 'Na2CO3(aq) + 2HCl(aq) -> 2NaCl(aq) + H2O(l) + CO2(g)', '2H+(aq) + CO3^2-(aq) -> H2O(l) + CO2(g)', 'Na⁺ and Cl⁻'),
    ('precipitation of silver chloride from silver nitrate and sodium chloride', 'AgNO3(aq) + NaCl(aq) -> AgCl(s) + NaNO3(aq)', 'Ag+(aq) + Cl-(aq) -> AgCl(s)', 'Na⁺ and NO₃⁻'),
    ('precipitation of barium sulfate from barium chloride and sodium sulfate', 'BaCl2(aq) + Na2SO4(aq) -> BaSO4(s) + 2NaCl(aq)', 'Ba2+(aq) + SO4^2-(aq) -> BaSO4(s)', 'Na⁺ and Cl⁻'),
    ('precipitation of lead(II) iodide from lead(II) nitrate and potassium iodide', 'Pb(NO3)2(aq) + 2KI(aq) -> PbI2(s) + 2KNO3(aq)', 'Pb2+(aq) + 2I-(aq) -> PbI2(s)', 'K⁺ and NO₃⁻'),
    ('precipitation of copper(II) hydroxide from copper(II) sulfate and sodium hydroxide', 'CuSO4(aq) + 2NaOH(aq) -> Cu(OH)2(s) + Na2SO4(aq)', 'Cu2+(aq) + 2OH-(aq) -> Cu(OH)2(s)', 'Na⁺ and SO₄²⁻'),
    ('precipitation of iron(III) hydroxide from iron(III) chloride and sodium hydroxide', 'FeCl3(aq) + 3NaOH(aq) -> Fe(OH)3(s) + 3NaCl(aq)', 'Fe3+(aq) + 3OH-(aq) -> Fe(OH)3(s)', 'Na⁺ and Cl⁻'),
    ('precipitation of calcium carbonate from calcium chloride and sodium carbonate', 'CaCl2(aq) + Na2CO3(aq) -> CaCO3(s) + 2NaCl(aq)', 'Ca2+(aq) + CO3^2-(aq) -> CaCO3(s)', 'Na⁺ and Cl⁻'),
    ('precipitation of silver bromide from silver nitrate and potassium bromide', 'AgNO3(aq) + KBr(aq) -> AgBr(s) + KNO3(aq)', 'Ag+(aq) + Br-(aq) -> AgBr(s)', 'K⁺ and NO₃⁻'),
    ('precipitation of iron(II) hydroxide from iron(II) sulfate and sodium hydroxide', 'FeSO4(aq) + 2NaOH(aq) -> Fe(OH)2(s) + Na2SO4(aq)', 'Fe2+(aq) + 2OH-(aq) -> Fe(OH)2(s)', 'Na⁺ and SO₄²⁻'),
]
for _d, _e, _i, _s in IONIC_EQS:
    assert balanced(_e), _e


def IE(s):
    """Ionic equation ascii -> unicode: 'Cu2+(aq)' -> Cu²⁺(aq), 'CO3^2-(aq)' -> CO₃²⁻(aq)."""
    out = []
    for tok in s.split(' '):
        if tok in ('+', '->'):
            out.append('→' if tok == '->' else '+')
            continue
        m = re.match(r'^(\d*)([A-Za-z0-9()]+?)(\^?)(\d?[+-])?(\((?:s|l|g|aq)\))?$', tok)
        if not m:
            out.append(tok)
            continue
        co, body, caret, ch, st = m.groups()
        if ch and not caret:
            # charge digits glued to formula, e.g. Cu2+  -> body 'Cu', ch '2+'
            pass
        txt = (co or '') + F(body) + ((ch or '').translate(str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻'))) + (st or '')
        out.append(txt)
    return ' '.join(out)


t4c = T('Ionic equations and spectator ions', 'ionic equations', 'spectator ions')
t4c.fixed('C1', (1, 2), [
    ('What is a spectator ion?', 'an ion present in the reaction mixture that does not take part in the reaction', 'Spectator ions are unchanged; they are left out of the ionic equation.',
     ['an ion that forms a precipitate', 'an ion that is oxidised', 'an ion that is formed from water']),
    ('Which ionic equation represents the neutralisation of any acid by any alkali?', 'H⁺(aq) + OH⁻(aq) → H₂O(l)', 'The H⁺ from the acid reacts with OH⁻ from the alkali.',
     ['Na⁺(aq) + Cl⁻(aq) → NaCl(s)', 'H₂(g) + O₂(g) → H₂O(l)', 'H⁺(aq) + Cl⁻(aq) → HCl(aq)']),
    ('Which substances are shown as separate ions in an ionic equation?', 'ionic compounds that are dissolved in water (aqueous)', 'Solids, liquids, gases and molecular substances are written as formulae.',
     ['all solids', 'all gases', 'water']),
    ('In the reaction AgNO₃(aq) + NaCl(aq) → AgCl(s) + NaNO₃(aq), which ions are spectator ions?', 'Na⁺ and NO₃⁻', 'Ag⁺ and Cl⁻ form the precipitate; Na⁺ and NO₃⁻ stay in solution.', ['Ag⁺ and Cl⁻', 'Ag⁺ and NO₃⁻', 'Na⁺ and Cl⁻']),
    ('State what must be equal on both sides of a balanced ionic equation, in addition to the numbers of atoms.', 'the total charge', '[1]'),
])
t4c.fixed('C2', (2, 3, 4), [
    ('Explain why the ionic equation for the reaction of nitric acid with sodium hydroxide is the same as that for hydrochloric acid with potassium hydroxide.', 'In both, the only change is H⁺ + OH⁻ → H₂O; the metal ions and the acid anions are spectator ions that remain in solution unchanged.', '1 mark: H⁺ + OH⁻ → H₂O; 1 mark: other ions are spectators [2]'),
    ('Explain why silver chloride is written as AgCl(s), not as separate ions, in an ionic equation.', 'It is an insoluble solid (precipitate); its ions are held in a lattice and are not free in solution.', '[2]'),
    ('Explain how an ionic equation can be checked to make sure it is balanced.', 'The numbers of each type of atom and the total charge must both be the same on each side.', '[2]'),
    ('A student writes the ionic equation for zinc reacting with copper(II) sulfate as Zn + CuSO₄ → ZnSO₄ + Cu. Explain why this is not an ionic equation and give the correct one.', 'It includes the sulfate spectator ion within formulae; the ionic equation is Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s).', '1 mark: spectator not removed; 1 mark: correct ionic equation [2]'),
])


@t4c.add('C3', (1, 2, 3, 4))
def t4c_write(r, D):
    d, full, ion, spec = r.choice(IONIC_EQS)
    if D == 1:
        pool = [IE(x[2]) for x in IONIC_EQS if x[2] != ion]
        return M(r, f'Which is the ionic equation for the {d}?', IE(ion), pool, f'Full: {E(full)}; spectators {spec} removed → {IE(ion)}.')
    stem = f'The full equation for the {d} is {E(full)}. Write the ionic equation for this reaction, including state symbols, and identify the spectator ions.'
    key = f'{IE(ion)}: 1 mark species; 1 mark balanced with states; 1 mark spectators {spec} [3]'
    if D >= 4:
        stem += ' Show that your equation is balanced for charge.'
        key = key.replace(' [3]', '; 1 mark: charge equal on both sides [4]')
    return Q(stem, f'{IE(ion)}; spectator ions: {spec}', key, 'short')


@t4c.add('C1', (1, 2, 3))
def t4c_spect(r, D):
    d, full, ion, spec = r.choice(IONIC_EQS)
    pool = list({x[3] for x in IONIC_EQS if x[3] != spec}) + ['there are no spectator ions']
    return M(r, f'Which ions are spectator ions in the reaction {E(full)}?', spec, pool, f'Ionic equation: {IE(ion)}; the ions unchanged in solution are {spec}.')


@t4c.add('C3', (2, 3, 4, 5))
def t4c_ppt(r, D):
    pairs = [('Ba', 'SO4'), ('Pb', 'SO4'), ('Ag', 'Cl'), ('Pb', 'Cl'), ('Ca', 'CO3'), ('Zn', 'CO3'), ('Cu', 'CO3'), ('Pb', 'I'), ('Ag', 'Br'), ('Ag', 'I'), ('Ba', 'CO3'), ('Mg', 'CO3')]
    c, a = r.choice(pairs)
    (cs, cn), (as_, an), eq, ion, side = ppt_reagents(c, a, alt=r.choice([0, 1]))
    ionu = IE(ion.replace('^', '').replace('->', '->')).replace('(s)', '')
    prod = salt_f(c, a)
    p = person(r)
    stem = f'{p} mixes aqueous {cn} with aqueous {an}. A precipitate of {salt_n(c, a)} forms. Write the full balanced equation and the ionic equation, each with state symbols.'
    full = E(eq)
    io_parts = ion.split(' -> ')[0].split(' + ')
    ionic_ = ' + '.join(IE(x) + '(aq)' for x in io_parts) + ' → ' + F(prod) + '(s)'
    key = f'full: {full} [1]; state symbols [1]; ionic: {ionic_} [1]'
    if D >= 4:
        stem += ' Name the spectator ions.'
        sp1 = [x for x in atoms(side[0])]
        key += f'; spectators: the ions of {side[1]} [1]'
    return Q(stem, f'{full}; {ionic_}', key, 'short')


@t4c.add('C2', (2, 3, 4), 'explain')
def t4c_why(r, D):
    d, full, ion, spec = r.choice(IONIC_EQS)
    return Q(f'For the {d}, {E(full)}, explain why {spec} {"are" if " and " in spec else "is"} not included in the ionic equation, and write the ionic equation.',
             f'{spec} {"are" if " and " in spec else "is"} present in the same form, dissolved in solution, before and after the reaction (spectator ion{"s" if " and " in spec else ""}). Ionic equation: {IE(ion)}.',
             '1 mark: unchanged / remain in solution; 1 mark: ionic equation [2]' if D <= 3 else '1 mark: spectator meaning; 1 mark: ions that react identified; 1 mark: ionic equation with states [3]')


def _t4c_c4(r, D):
    d, full, ion, spec = r.choice(IONIC_EQS)
    p = person(r)
    intro = r.choice([f'{p} investigates the {d}. The full equation is {E(nostate(full))}.', f'In {lab(r)}, a student carries out the {d}: {E(nostate(full))}.'])
    parts = [
        lambda r: ('Add state symbols to the full equation.', E(full), '[1]'),
        lambda r: ('List all the ions present in the reactant solutions.', 'all ions from the aqueous reactants, e.g. ' + spec + ' and the reacting ions', '[1]'),
        lambda r: ('Identify the spectator ions.', spec, '[1]'),
        lambda r: ('Write the ionic equation with state symbols.', IE(ion), '1 mark species; 1 mark balanced with states [2]'),
        lambda r: ('Show that the ionic equation is balanced for charge.', 'total charge on the left equals total charge on the right', '[1]'),
        lambda r: ('Describe what would be observed during the reaction.', {True: 'a precipitate forms', False: 'see observations: e.g. fizzing / colour change / temperature rise'}['precipitation' in d], '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t4c.add('C4', (2, 3, 4, 5), 'multi_step')(_t4c_c4)
t4c.add('C3', (4, 5), 'multi_step')(_t4c_c4)

CHAPTERS[4] = [t4a, t4b, t4c]


# ===================================================================== Ch5 Chemical calculations
AR.setdefault('B', 11)
MRLIST = [('water', 'H2O'), ('carbon dioxide', 'CO2'), ('sodium chloride', 'NaCl'), ('calcium carbonate', 'CaCO3'), ('sulfuric acid', 'H2SO4'), ('sodium hydroxide', 'NaOH'),
          ('magnesium oxide', 'MgO'), ('ammonia', 'NH3'), ('methane', 'CH4'), ('glucose', 'C6H12O6'), ('copper(II) sulfate', 'CuSO4'), ('ethanol', 'C2H5OH'),
          ('calcium hydroxide', 'Ca(OH)2'), ('aluminium oxide', 'Al2O3'), ('ammonium nitrate', 'NH4NO3'), ('iron(III) oxide', 'Fe2O3'), ('potassium nitrate', 'KNO3'),
          ('sodium carbonate', 'Na2CO3'), ('magnesium chloride', 'MgCl2'), ('nitric acid', 'HNO3'), ('ammonium sulfate', '(NH4)2SO4'), ('zinc oxide', 'ZnO'), ('oxygen', 'O2'),
          ('chlorine', 'Cl2'), ('nitrogen', 'N2'), ('hydrogen', 'H2'), ('sulfur dioxide', 'SO2'), ('propane', 'C3H8'), ('hydrated copper(II) sulfate', 'CuSO4.5H2O'),
          ('lead(II) nitrate', 'Pb(NO3)2'), ('silver nitrate', 'AgNO3'), ('potassium hydroxide', 'KOH'), ('copper(II) oxide', 'CuO'), ('magnesium sulfate', 'MgSO4'),
          ('calcium chloride', 'CaCl2'), ('sodium sulfate', 'Na2SO4'), ('hydrogen chloride', 'HCl'), ('aluminium sulfate', 'Al2(SO4)3'), ('sulfur trioxide', 'SO3'), ('butane', 'C4H10')]
MOLEC = {'H2O', 'CO2', 'NH3', 'CH4', 'C6H12O6', 'C2H5OH', 'O2', 'Cl2', 'N2', 'H2', 'SO2', 'C3H8', 'HCl', 'SO3', 'C4H10', 'H2SO4', 'HNO3'}
EL_MOLES = [('magnesium', 'Mg'), ('carbon', 'C'), ('iron', 'Fe'), ('copper', 'Cu'), ('sodium', 'Na'), ('calcium', 'Ca'), ('aluminium', 'Al'), ('zinc', 'Zn'), ('sulfur', 'S'), ('silver', 'Ag'), ('lead', 'Pb')]
NS = [0.1, 0.2, 0.25, 0.5, 0.4, 0.05, 1.5, 2.0, 0.15, 0.3, 0.025, 0.8, 1.2, 0.6, 0.02, 3.0]


def mr_work(f):
    return ' + '.join(f'{(str(k) + " × ") if k > 1 else ""}{mr(AR[e])}' for e, k in atoms(f).items()) + f' = {mr(Mr(f))}'


def ar_data(*fs):
    els = sorted({e for f in fs for e in atoms(f)})
    return '(Ar: ' + ', '.join(f'{e} = {mr(AR[e])}' for e in els) + ')'


t5a = T('Relative formula mass and the mole; Avogadro constant', 'relative formula mass', 'the mole', 'avogadro constant')
t5a.fixed('C1', (1, 2), [
    ('What is the Avogadro constant?', '6.02 × 10²³ particles per mole', 'One mole of any substance contains 6.02 × 10²³ particles.', ['6.02 × 10⁻²³ particles per mole', '24 dm³ per mole', '12 g per mole']),
    ('Which quantity has the unit mol?', 'amount of substance', 'The mole is the unit of amount of substance.', ['mass', 'concentration', 'relative formula mass']),
    ('Which contains the greatest number of atoms?', '1 mol of methane, CH₄', 'CH₄: 5 atoms per molecule → 5 mol atoms.', ['1 mol of helium, He', '1 mol of oxygen, O₂', '1 mol of carbon dioxide, CO₂']),
    ('What is the mass of one mole of oxygen molecules, O₂? (Ar: O = 16)', '32 g', 'Mr(O₂) = 2 × 16 = 32, so 1 mol = 32 g.', ['16 g', '8 g', '64 g']),
    ('Define relative formula mass, Mr.', 'The sum of the relative atomic masses of all the atoms shown in the formula.', '[1]'),
    ('State the equation linking number of moles, mass and molar mass.', 'moles = mass (g) ÷ molar mass (g/mol)', '[1]'),
])
t5a.fixed('C2', (2, 3, 4), [
    ('Explain why 1 mol of hydrogen gas, H₂, has a mass of 2 g but 1 mol of hydrogen atoms has a mass of 1 g.', 'Each H₂ molecule contains two H atoms, so Mr(H₂) = 2; 1 mol of molecules contains 2 mol of atoms.', '1 mark: H₂ diatomic Mr = 2; 1 mark: 2 mol atoms per mol molecules [2]'),
    ('Explain why 10 g of magnesium contains more atoms than 10 g of copper.', 'Magnesium atoms are lighter (Ar 24 vs 64), so 10 g contains more moles (0.417 vs 0.156 mol) and therefore more atoms.', '1 mark: Ar comparison; 1 mark: more moles → more atoms [2]'),
    ('A student calculates the number of moles in 32 g of oxygen gas as 2 mol. Explain the error.', 'Oxygen gas is O₂ with Mr 32, so 32 g is 1 mol of O₂ molecules; the student used Ar (16) instead of Mr.', '[2]'),
    ('Explain what is meant by "one mole" of a substance.', 'The amount of substance containing 6.02 × 10²³ particles (atoms, molecules or ions) – the Avogadro constant; its mass in grams equals the Ar or Mr.', '[2]'),
    ('Explain why relative formula mass has no units.', 'It is a ratio: the mass of a formula unit compared with 1/12 of the mass of a carbon-12 atom.', '[1]'),
])


@t5a.add('C1', (1, 2, 3))
def t5a_mr(r, D):
    n, f = r.choice(MRLIST)
    v = Mr(f)
    at = atoms(f)
    wrong = [sum(AR[e] for e in at), v + 16, v - 1, v + AR[list(at)[0]], v * 2, v - 16 if v > 30 else v + 2]
    return NM(r, f'What is the relative formula mass of {n}, {F(f)}? {ar_data(f)}', v, wrong, '', mr_work(f), f=mr)


@t5a.add('C3', (1, 2, 3, 4, 5))
def t5a_moles(r, D):
    n, f = r.choice(MRLIST)
    M_ = Mr(f)
    nn = r.choice(NS)
    m = nn * M_
    mode = r.choice(['n', 'm', 'N']) if D <= 3 else r.choice(['N', 'atoms', 'chain'])
    p = person(r)
    if mode == 'n':
        if D == 1:
            return NM(r, f'How many moles are in {g3(m)} g of {n}, {F(f)}? {ar_data(f)}', nn, [nn * 2, nn / 2, m * M_, nn * 10, M_ / m], ' mol', f'n = m/Mr = {g3(m)} ÷ {mr(M_)} = {g3(nn)} mol')
        return Q(f'{p} weighs out {g3(m)} g of {n}, {F(f)}. Calculate the number of moles of {n}. {ar_data(f)}', f'{g3(nn)} mol', f'Mr = {mr(M_)} [1]; n = {g3(m)} ÷ {mr(M_)} = {g3(nn)} mol [1]', 'numerical')
    if mode == 'm':
        return Q(f'Calculate the mass of {g3(nn)} mol of {n}, {F(f)}. {ar_data(f)}', f'{g3(m)} g', f'Mr = {mr(M_)} [1]; m = {g3(nn)} × {mr(M_)} = {g3(m)} g [1]', 'numerical')
    if mode == 'N':
        N = nn * NA
        return Q(f'Calculate the number of {"molecules" if f in MOLEC else "formula units"} in {g3(m)} g of {n}, {F(f)}. (Avogadro constant = 6.02 × 10²³ /mol) {ar_data(f)}', sci(N),
                 f'n = {g3(m)} ÷ {mr(M_)} = {g3(nn)} mol [1]; N = {g3(nn)} × 6.02 × 10²³ = {sci(N)} [1]', 'numerical')
    if mode == 'atoms':
        nf, ff = r.choice([x for x in MRLIST if x[1] in MOLEC])
        M2 = Mr(ff)
        n2 = r.choice(NS)
        el = r.choice(list(atoms(ff)))
        k = atoms(ff)[el]
        N = n2 * k * NA
        return Q(f'Calculate the number of {el} atoms in {g3(n2 * M2)} g of {nf}, {F(ff)}. (Avogadro constant = 6.02 × 10²³ /mol) {ar_data(ff)}', sci(N),
                 f'Mr = {mr(M2)}; n(molecules) = {g3(n2 * M2)} ÷ {mr(M2)} = {g3(n2)} mol [1]; n({el}) = {k} × {g3(n2)} = {g3(n2 * k)} mol [1]; N = {g3(n2 * k)} × 6.02 × 10²³ = {sci(N)} [1]', 'numerical')
    (n1, f1), (n2_, f2) = r.sample(MRLIST, 2)
    m1 = r.choice([5.0, 10.0, 20.0, 50.0, 100.0])
    a1, a2 = m1 / Mr(f1), m1 / Mr(f2)
    more = n1 if a1 > a2 else n2_
    if abs(a1 - a2) / max(a1, a2) < 0.05:
        return None
    return Q(f'{p} has {sf(m1)} g of {n1}, {F(f1)}, and {sf(m1)} g of {n2_}, {F(f2)}. Calculate the number of moles of each and deduce which sample contains more {"molecules" if f1 in MOLEC and f2 in MOLEC else "particles (formula units)"}. {ar_data(f1, f2)}',
             f'{F(f1)}: {g3(a1)} mol; {F(f2)}: {g3(a2)} mol; {more} contains more.',
             f'Mr {mr(Mr(f1))} and {mr(Mr(f2))} [1]; moles {g3(a1)} and {g3(a2)} [1]; conclusion: {more} (more moles → more particles) [1]', 'numerical')


@t5a.add('C2', (2, 3, 4), 'explain')
def t5a_compare(r, D):
    (e1, s1), (e2, s2) = r.sample(EL_MOLES, 2)
    m = r.choice([6.0, 12.0, 24.0, 10.0, 48.0])
    a1, a2 = m / AR[s1], m / AR[s2]
    more = e1 if a1 > a2 else e2
    return Q(f'{person(r)} says that {sf(m)} g of {e1} and {sf(m)} g of {e2} must contain the same number of atoms because they have the same mass. Explain why this is incorrect. (Ar: {s1} = {mr(AR[s1])}, {s2} = {mr(AR[s2])})',
             f'The atoms have different masses, so equal masses contain different numbers of moles: {e1} {g3(a1)} mol, {e2} {g3(a2)} mol; {more} has more atoms.',
             '1 mark: atoms of different elements have different masses; 1 mark: moles calculated / compared; ' + ('1 mark: correct conclusion [3]' if D >= 3 else 'total [2]'))


def _t5a_c4(r, D):
    n, f = r.choice([x for x in MRLIST if len(atoms(x[1])) >= 2])
    M_ = Mr(f)
    nn = r.choice(NS)
    m = nn * M_
    el = r.choice(list(atoms(f)))
    k = atoms(f)[el]
    intro = r.choice([f'A sample of {n}, {F(f)}, has a mass of {g3(m)} g.', f'{person(r)} weighs {g3(m)} g of {n}, {F(f)}, on a balance in {lab(r)}.'])
    intro += f' {ar_data(f)} (Avogadro constant = 6.02 × 10²³ /mol)'
    parts = [
        lambda r: (f'Calculate the relative formula mass of {F(f)}.', mr(M_), mr_work(f) + ' [1]'),
        lambda r: ('Calculate the number of moles in the sample.', f'{g3(nn)} mol', f'{g3(m)} ÷ {mr(M_)} [1]'),
        lambda r: (f'Calculate the number of moles of {el} atoms in the sample.', f'{g3(nn * k)} mol', f'{k} × {g3(nn)} [1]'),
        lambda r: (f'Calculate the number of {"molecules" if f in MOLEC else "formula units"} in the sample.', sci(nn * NA), f'{g3(nn)} × 6.02 × 10²³ [1]'),
        lambda r: (f'Calculate the mass of {el} in the sample.', f'{g3(nn * k * AR[el])} g', f'{g3(nn * k)} × {mr(AR[el])} [1]'),
        lambda r: (f'Calculate the percentage by mass of {el} in {F(f)}.', f'{g3(k * AR[el] / M_ * 100)}%', f'{k} × {mr(AR[el])} ÷ {mr(M_)} × 100 [2]'),
        lambda r: (f'Calculate the mass of {F(f)} that would contain twice as many particles as this sample.', f'{g3(2 * m)} g', f'2 × {g3(m)} [1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t5a.add('C4', (2, 3, 4, 5), 'multi_step')(_t5a_c4)


# ---------------------------------------------------------- 5.2 reacting masses, limiting reactant, yield
RXN = [(w, e) for w, e in EQS if all(s in ('s', 'g', 'l') for _, _, s in parse_eq(e)[0])]
RXN2 = [(w, e) for w, e in RXN if len(parse_eq(e)[0]) == 2]


def _pick_pair(r, e):
    L, R = parse_eq(e)
    a = r.choice(L)
    b = r.choice([x for x in R if x[2] in ('s', 'g', 'l')] or R)
    return a, b


t5b = T('Reacting masses, limiting reactants and percentage yield', 'reacting masses', 'limiting reactants', 'percentage yield')
t5b.fixed('C1', (1, 2), [
    ('What is meant by the limiting reactant?', 'the reactant that is completely used up and so limits the amount of product', 'Limiting reactant runs out first; the other is in excess.',
     ['the reactant present in the greatest mass', 'the reactant left over at the end', 'the catalyst used in the reaction']),
    ('A reaction has a theoretical yield of 20 g and an actual yield of 15 g. What is the percentage yield?', '75%', '15/20 × 100 = 75%.', ['133%', '25%', '5%']),
    ('Why is the actual yield of a reaction usually less than the theoretical yield?', 'Some product is lost during separation or the reaction does not go to completion.', 'Losses on filtering/transfer, side reactions, incomplete or reversible reactions.',
     ['Mass is destroyed in the reaction.', 'The limiting reactant is in excess.', 'The catalyst is used up.']),
    ('In the reaction 2Mg + O₂ → 2MgO, what is the mole ratio of magnesium to magnesium oxide?', '1 : 1', '2 mol Mg → 2 mol MgO.', ['2 : 1', '1 : 2', '2 : 3']),
    ('State the formula used to calculate percentage yield.', 'percentage yield = (actual yield ÷ theoretical yield) × 100', '[1]'),
])
t5b.fixed('C2', (2, 3, 4), [
    ('Explain why adding more of the reactant that is in excess does not increase the mass of product.', 'The amount of product depends on the limiting reactant; once it has all reacted, extra excess reactant has nothing to react with.', '[2]'),
    ('Explain how you would use a balanced equation to find the mass of product from a known mass of reactant.', 'Convert mass of reactant to moles (÷ Mr); use the mole ratio from the equation to find moles of product; multiply by Mr of product.', '1 mark: moles of reactant; 1 mark: mole ratio; 1 mark: × Mr of product [3]'),
    ('A student obtains a percentage yield of 108% for a dried precipitate. Suggest a reason for this.', 'The product was not completely dry (still contained water) or was contaminated with another substance.', '[1]'),
    ('Explain why a reversible reaction cannot have a 100% yield.', 'The products re-form the reactants, so at equilibrium not all reactants have been converted to products.', '[2]'),
])


@t5b.add('C3', (1, 2, 3, 4))
def t5b_mass(r, D):
    w, e = r.choice(RXN)
    (na, fa, sa), (nb, fb, sb) = _pick_pair(r, e)
    ma = r.choice([1.2, 2.4, 4.0, 4.8, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 25.0, 50.0, 100.0, 2.0, 3.2])
    moles_a = ma / Mr(fa)
    moles_b = moles_a * nb / na
    mb = moles_b * Mr(fb)
    p = person(r)
    data = ar_data(fa, fb)
    stem = r.choice([f'{p} reacts {g3(ma)} g of {F(fa)} completely. {E(nostate(e))}. Calculate the mass of {F(fb)} formed. {data}',
                     f'Use the equation {E(nostate(e))} to calculate the maximum mass of {F(fb)} that can be made from {g3(ma)} g of {F(fa)}. {data}',
                     f'In a factory in {city(r)}, {g3(ma)} g of {F(fa)} react in the reaction {E(nostate(e))}. Calculate the mass of {F(fb)} produced. {data}'])
    key = f'n({F(fa)}) = {g3(ma)} ÷ {mr(Mr(fa))} = {g3(moles_a)} mol [1]; ratio {na}:{nb} → n({F(fb)}) = {g3(moles_b)} mol [1]; mass = {g3(moles_b)} × {mr(Mr(fb))} = {g3(mb)} g [1]'
    if D == 1:
        return NM(r, stem, mb, [moles_a * Mr(fb), mb * 2, mb / 2, ma, ma * Mr(fb) / Mr(fa) * (2 if nb == na else 1)], ' g', key)
    return Q(stem, f'{g3(mb)} g', key, 'numerical')


@t5b.add('C3', (3, 4, 5))
def t5b_limit(r, D):
    w, e = r.choice(RXN2)
    L, R = parse_eq(e)
    (n1, f1, _), (n2, f2, _) = L
    nb, fb, _ = r.choice(R)
    k1 = r.choice([0.1, 0.2, 0.25, 0.5, 0.4, 0.3])
    k2 = k1 * r.choice([0.5, 0.6, 0.75, 1.5, 2.0, 1.25])
    m1, m2 = k1 * n1 * Mr(f1), k2 * n2 * Mr(f2)
    m1, m2 = r3(m1), r3(m2)
    a1, a2 = m1 / Mr(f1), m2 / Mr(f2)
    lim = (f1, a1, n1) if a1 / n1 < a2 / n2 else (f2, a2, n2)
    exc = f2 if lim[0] == f1 else f1
    if abs(a1 / n1 - a2 / n2) / max(a1 / n1, a2 / n2) < 0.1:
        return None
    nprod = lim[1] / lim[2] * nb
    mprod = nprod * Mr(fb)
    stem = f'{g3(m1)} g of {F(f1)} is mixed with {g3(m2)} g of {F(f2)}. {E(nostate(e))}. Deduce which reactant is limiting and calculate the mass of {F(fb)} formed. {ar_data(f1, f2, fb)}'
    key = (f'n({F(f1)}) = {g3(a1)} mol, n({F(f2)}) = {g3(a2)} mol [1]; compare with ratio {n1}:{n2} → {F(lim[0])} limiting, {F(exc)} in excess [1]; '
           f'n({F(fb)}) = {g3(nprod)} mol [1]; mass = {g3(nprod)} × {mr(Mr(fb))} = {g3(mprod)} g [1]')
    ans = f'{F(lim[0])} is limiting; {g3(mprod)} g of {F(fb)}'
    if D >= 5:
        y = r.choice([60, 65, 72, 80, 85, 90])
        act = r3(mprod * y / 100)
        stem += f' The actual mass obtained was {g3(act)} g. Calculate the percentage yield.'
        ans += f'; yield {g3(act / r3(mprod) * 100)}%'
        key += f'; % yield = {g3(act)} ÷ {g3(mprod)} × 100 = {g3(act / r3(mprod) * 100)}% [1]'
    return Q(stem, ans, key, 'numerical')


@t5b.add('C3', (2, 3, 4))
def t5b_yield(r, D):
    w, e = r.choice(RXN)
    (na, fa, sa), (nb, fb, sb) = _pick_pair(r, e)
    ma = r.choice([2.4, 4.8, 5.0, 10.0, 12.0, 20.0, 25.0, 40.0, 50.0])
    th = ma / Mr(fa) * nb / na * Mr(fb)
    y = r.choice([55, 62, 68, 74, 78, 82, 88, 93])
    act = r3(th * y / 100)
    p = person(r)
    if D == 2:
        return Q(f'The theoretical yield of {F(fb)} in a reaction is {g3(th)} g. {p} obtains {g3(act)} g. Calculate the percentage yield.', f'{g3(act / r3(th) * 100)}%',
                 f'{g3(act)} ÷ {g3(th)} × 100 [1] = {g3(act / r3(th) * 100)}% [1]', 'numerical')
    stem = f'{p} uses {g3(ma)} g of {F(fa)} in the reaction {E(nostate(e))} and obtains {g3(act)} g of {F(fb)}. Calculate the theoretical yield and the percentage yield. {ar_data(fa, fb)}'
    key = f'n({F(fa)}) = {g3(ma / Mr(fa))} mol [1]; theoretical mass {F(fb)} = {g3(th)} g [1]; % yield = {g3(act)} ÷ {g3(th)} × 100 = {g3(act / r3(th) * 100)}% [1]'
    if D >= 4:
        stem += ' Suggest one reason why the yield is less than 100%.'
        key += '; reason, e.g. losses on transfer/filtration, incomplete reaction [1]'
    return Q(stem, f'{g3(th)} g; {g3(act / r3(th) * 100)}%', key, 'numerical')


@t5b.add('C2', (2, 3, 4), 'explain')
def t5b_spot(r, D):
    w, e = r.choice([x for x in RXN if any(n > 1 for n in coeffs(x[1]))])
    L, R = parse_eq(e)
    (na, fa, _), (nb, fb, _) = _pick_pair(r, e)
    if na == nb:
        return None
    ma = r.choice([4.8, 6.0, 12.0, 24.0, 10.0])
    right = ma / Mr(fa) * nb / na * Mr(fb)
    wrong = ma / Mr(fa) * Mr(fb)
    return Q(f'{person(r)} calculates the mass of {F(fb)} made from {g3(ma)} g of {F(fa)} in the reaction {E(nostate(e))} and gets {g3(wrong)} g. Identify the error and give the correct answer. {ar_data(fa, fb)}',
             f'The mole ratio {na}:{nb} from the equation was ignored. Correct: n = {g3(ma / Mr(fa))} mol {F(fa)} → {g3(ma / Mr(fa) * nb / na)} mol {F(fb)} → {g3(right)} g.',
             '1 mark: mole ratio not used; 1 mark: correct answer ' + g3(right) + ' g [2]')


def _t5b_c4(r, D):
    w, e = r.choice(RXN)
    (na, fa, sa), (nb, fb, sb) = _pick_pair(r, e)
    ma = r.choice([2.4, 4.8, 6.0, 10.0, 12.0, 20.0, 40.0])
    moles = ma / Mr(fa)
    th = moles * nb / na * Mr(fb)
    y = r.choice([60, 70, 75, 80, 85, 90])
    act = r3(th * y / 100)
    p = person(r)
    intro = r.choice([f'{p} carries out the reaction {w} using {g3(ma)} g of {F(fa)}.', f'A manufacturer in {city(r)} makes {F(fb)} by the reaction {w}, starting from {g3(ma)} g of {F(fa)}.'])
    intro += f' {E(nostate(e))} {ar_data(fa, fb)}'
    parts = [
        lambda r: (f'Calculate the number of moles of {F(fa)} used.', f'{g3(moles)} mol', f'{g3(ma)} ÷ {mr(Mr(fa))} [1]'),
        lambda r: (f'Deduce the number of moles of {F(fb)} that can form.', f'{g3(moles * nb / na)} mol', f'ratio {na}:{nb} [1]'),
        lambda r: (f'Calculate the theoretical (maximum) mass of {F(fb)}.', f'{g3(th)} g', f'{g3(moles * nb / na)} × {mr(Mr(fb))} [1]'),
        lambda r: (f'The actual mass obtained was {g3(act)} g. Calculate the percentage yield.', f'{g3(act / r3(th) * 100)}%', f'{g3(act)} ÷ {g3(th)} × 100 [1]'),
        lambda r: ('Suggest two reasons why the percentage yield is less than 100%.', 'product lost on transfer/filtration; reaction incomplete; side reactions; impure reactant', '1 mark each [2]'),
        lambda r: (f'Calculate the mass of {F(fa)} needed to make {g3(2 * th)} g of {F(fb)} at 100% yield.', f'{g3(2 * ma)} g', 'double the quantities [1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t5b.add('C4', (2, 3, 4, 5), 'multi_step')(_t5b_c4)
t5b.add('C3', (4, 5), 'multi_step')(_t5b_c4)


# ---------------------------------------------------------- 5.3 gas volume and concentration
GASREAC = [  # equation, solid reactant, gas product, context
    ('CaCO3(s) + 2HCl(aq) -> CaCl2(aq) + H2O(l) + CO2(g)', 'CaCO3', 'CO2', 'calcium carbonate reacts with excess hydrochloric acid'),
    ('Mg(s) + 2HCl(aq) -> MgCl2(aq) + H2(g)', 'Mg', 'H2', 'magnesium reacts with excess hydrochloric acid'),
    ('Zn(s) + H2SO4(aq) -> ZnSO4(aq) + H2(g)', 'Zn', 'H2', 'zinc reacts with excess dilute sulfuric acid'),
    ('2H2O2(aq) -> 2H2O(l) + O2(g)', 'H2O2', 'O2', 'hydrogen peroxide decomposes with a manganese(IV) oxide catalyst'),
    ('Na2CO3(s) + 2HCl(aq) -> 2NaCl(aq) + H2O(l) + CO2(g)', 'Na2CO3', 'CO2', 'sodium carbonate reacts with excess hydrochloric acid'),
    ('CaCO3(s) -> CaO(s) + CO2(g)', 'CaCO3', 'CO2', 'calcium carbonate is heated strongly'),
    ('CuCO3(s) -> CuO(s) + CO2(g)', 'CuCO3', 'CO2', 'copper(II) carbonate is heated'),
    ('2Al(s) + 6HCl(aq) -> 2AlCl3(aq) + 3H2(g)', 'Al', 'H2', 'aluminium reacts with excess hydrochloric acid'),
    ('Ca(s) + 2H2O(l) -> Ca(OH)2(aq) + H2(g)', 'Ca', 'H2', 'calcium reacts with excess water'),
    ('2Na(s) + 2H2O(l) -> 2NaOH(aq) + H2(g)', 'Na', 'H2', 'sodium reacts with excess water'),
    ('MgCO3(s) + 2HCl(aq) -> MgCl2(aq) + H2O(l) + CO2(g)', 'MgCO3', 'CO2', 'magnesium carbonate reacts with excess hydrochloric acid'),
]
for _e, *_ in GASREAC:
    assert balanced(_e), _e
GASVOL = [  # equation of gases for volume ratios
    ('CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)', 'methane'), ('C3H8(g) + 5O2(g) -> 3CO2(g) + 4H2O(l)', 'propane'), ('2H2(g) + O2(g) -> 2H2O(l)', 'hydrogen'),
    ('N2(g) + 3H2(g) -> 2NH3(g)', 'nitrogen'), ('2CO(g) + O2(g) -> 2CO2(g)', 'carbon monoxide'), ('2C2H6(g) + 7O2(g) -> 4CO2(g) + 6H2O(l)', 'ethane'),
    ('C2H4(g) + 3O2(g) -> 2CO2(g) + 2H2O(l)', 'ethene'), ('H2(g) + Cl2(g) -> 2HCl(g)', 'hydrogen'), ('2SO2(g) + O2(g) -> 2SO3(g)', 'sulfur dioxide')]
SOLUTES = [('sodium hydroxide', 'NaOH'), ('sodium chloride', 'NaCl'), ('potassium hydroxide', 'KOH'), ('copper(II) sulfate', 'CuSO4'), ('sodium carbonate', 'Na2CO3'),
           ('hydrochloric acid', 'HCl'), ('sulfuric acid', 'H2SO4'), ('nitric acid', 'HNO3'), ('potassium nitrate', 'KNO3'), ('magnesium sulfate', 'MgSO4'), ('silver nitrate', 'AgNO3'),
           ('glucose', 'C6H12O6'), ('ammonium chloride', 'NH4Cl'), ('calcium chloride', 'CaCl2')]
CONCS = [0.05, 0.1, 0.2, 0.25, 0.4, 0.5, 0.8, 1.0, 1.5, 2.0]
VOLS = [10.0, 20.0, 25.0, 40.0, 50.0, 100.0, 125.0, 150.0, 200.0, 250.0, 500.0]

t5c = T('Molar gas volume and concentration of solutions in g/dm³ and mol/dm³', 'molar gas volume', 'concentration of solutions')
t5c.fixed('C1', (1, 2), [
    ('What is the volume of one mole of any gas at room temperature and pressure?', '24 dm³', 'Molar gas volume at r.t.p. = 24 dm³ (24 000 cm³).', ['22.4 cm³', '24 cm³', '1 dm³']),
    ('How many cm³ are there in 1 dm³?', '1000', '1 dm³ = 1000 cm³.', ['100', '10', '24 000']),
    ('What volume is occupied by 0.5 mol of carbon dioxide at r.t.p.?', '12 dm³', '0.5 × 24 = 12 dm³.', ['48 dm³', '22 dm³', '0.5 dm³']),
    ('Which unit is used for concentration measured in moles?', 'mol/dm³', 'Concentration = moles ÷ volume in dm³.', ['g/cm³', 'mol/g', 'dm³/mol']),
    ('State the equation linking concentration, amount of solute in moles and volume of solution.', 'concentration (mol/dm³) = moles ÷ volume (dm³)', '[1]'),
])
t5c.fixed('C2', (2, 3, 4), [
    ('Explain why 1 mol of hydrogen and 1 mol of carbon dioxide occupy the same volume at r.t.p.', 'In a gas the particles are very far apart, so the volume depends on the number of particles, not their size or mass; equal moles → equal volumes.', '[2]'),
    ('Explain how to convert a concentration in mol/dm³ to g/dm³.', 'Multiply the concentration in mol/dm³ by the molar mass (Mr) of the solute.', '[1]'),
    ('A student calculates the moles in 25 cm³ of 0.1 mol/dm³ acid as 2.5 mol. Explain the error.', 'The volume must be in dm³: 25 cm³ = 0.025 dm³, so moles = 0.025 × 0.1 = 0.0025 mol.', '1 mark: volume not converted to dm³; 1 mark: 0.0025 mol [2]'),
    ('Explain why the molar gas volume of 24 dm³ applies only at room temperature and pressure.', 'Gas volume depends on temperature and pressure; at a higher temperature or lower pressure the same number of moles occupies a larger volume.', '[2]'),
])


@t5c.add('C3', (1, 2, 3, 4))
def t5c_gas(r, D):
    n, f = r.choice([x for x in MRLIST if x[1] in ('CO2', 'O2', 'N2', 'H2', 'Cl2', 'SO2', 'NH3', 'CH4', 'C3H8', 'HCl', 'C4H10')])
    nn = r.choice(NS)
    mode = r.choice(['v', 'n', 'm']) if D >= 2 else 'v'
    V = nn * VOL
    if mode == 'v':
        unit = r.choice(['dm³', 'cm³'])
        val = V if unit == 'dm³' else V * 1000
        if D == 1:
            return NM(r, f'What is the volume of {g3(nn)} mol of {n} at r.t.p.?', val, [val / 2, val * 2, nn * 22.4 * (1 if unit == 'dm³' else 1000), val / 24, val * 1000 if unit == 'dm³' else val / 1000], ' ' + unit,
                      f'V = {g3(nn)} × 24 = {g3(V)} dm³' + (f' = {g3(V * 1000)} cm³' if unit == 'cm³' else ''))
        return Q(f'Calculate the volume, in {unit}, of {g3(nn)} mol of {n} at r.t.p.', f'{g3(val)} {unit}', f'{g3(nn)} × 24' + (' × 1000' if unit == 'cm³' else '') + f' = {g3(val)} {unit} [1]', 'numerical')
    if mode == 'n':
        Vc = V * 1000
        return Q(f'{person(r)} collects {g3(Vc)} cm³ of {n} at r.t.p. Calculate the number of moles of gas collected.', f'{g3(nn)} mol', f'{g3(Vc)} ÷ 24 000 = {g3(nn)} mol [2]' if D >= 3 else f'{g3(Vc)} ÷ 24 000 = {g3(nn)} mol [1]', 'numerical')
    m = nn * Mr(f)
    return Q(f'Calculate the volume at r.t.p. occupied by {g3(m)} g of {n}, {F(f)}. {ar_data(f)}', f'{g3(V)} dm³',
             f'n = {g3(m)} ÷ {mr(Mr(f))} = {g3(nn)} mol [1]; V = {g3(nn)} × 24 = {g3(V)} dm³ [1]', 'numerical')


@t5c.add('C3', (2, 3, 4, 5))
def t5c_rxn(r, D):
    e, sol, gas, ctx = r.choice(GASREAC)
    L, R = parse_eq(e)
    ns = [n for n, f, _ in L if f == sol][0]
    ng = [n for n, f, _ in R if f == gas][0]
    if sol == 'H2O2':
        return None
    m = r.choice([0.12, 0.24, 0.48, 0.5, 1.0, 1.2, 2.0, 2.4, 2.5, 5.0, 0.6, 0.27, 0.54, 0.46, 0.92])
    n_s = m / Mr(sol)
    n_g = n_s * ng / ns
    V = n_g * 24000
    p = person(r)
    stem = f'{p} finds that when {g3(m)} g of {F(sol)} is used, {ctx}. {E(nostate(e))}. Calculate the volume of {F(gas)} produced at r.t.p., in cm³. {ar_data(sol)}'
    stem = stem.replace(f'finds that when {g3(m)} g of {F(sol)} is used, {ctx}', f'uses {g3(m)} g of {F(sol)}: {ctx}')
    key = f'n({F(sol)}) = {g3(m)} ÷ {mr(Mr(sol))} = {g3(n_s)} mol [1]; n({F(gas)}) = {g3(n_g)} mol (ratio {ns}:{ng}) [1]; V = {g3(n_g)} × 24 000 = {g3(V)} cm³ [1]'
    if D >= 5:
        stem += f' Calculate the mass of {F(gas)} produced.'
        key += f'; mass = {g3(n_g)} × {mr(Mr(gas))} = {g3(n_g * Mr(gas))} g [1]'
        return Q(stem, f'{g3(V)} cm³; {g3(n_g * Mr(gas))} g', key, 'numerical')
    return Q(stem, f'{g3(V)} cm³', key, 'numerical')


@t5c.add('C3', (1, 2, 3, 4))
def t5c_conc(r, D):
    n, f = r.choice(SOLUTES)
    c = r.choice(CONCS)
    V = r.choice(VOLS)
    mode = r.choice(['n', 'c', 'g', 'mass']) if D >= 2 else 'n'
    nn = c * V / 1000
    if mode == 'n':
        if D == 1:
            return NM(r, f'How many moles of {n} are in {sf(V)} cm³ of a {sf(c)} mol/dm³ solution?', nn, [c * V, nn * 10, c / V, nn * 2, V / c / 1000], ' mol', f'n = c × V = {sf(c)} × {sf(V)}/1000 = {g3(nn)} mol')
        return Q(f'Calculate the number of moles of {n} in {sf(V)} cm³ of {sf(c)} mol/dm³ solution.', f'{g3(nn)} mol', f'V = {sf(V / 1000)} dm³ [1]; n = {sf(c)} × {sf(V / 1000)} = {g3(nn)} mol [1]', 'numerical')
    if mode == 'c':
        return Q(f'{g3(nn)} mol of {n} is dissolved in water and made up to {sf(V)} cm³. Calculate the concentration in mol/dm³.', f'{g3(c)} mol/dm³', f'c = {g3(nn)} ÷ {sf(V / 1000)} = {g3(c)} mol/dm³ [2]', 'numerical')
    if mode == 'g':
        return Q(f'Convert a concentration of {sf(c)} mol/dm³ of {n}, {F(f)}, into g/dm³. {ar_data(f)}', f'{g3(c * Mr(f))} g/dm³', f'Mr = {mr(Mr(f))} [1]; {sf(c)} × {mr(Mr(f))} = {g3(c * Mr(f))} g/dm³ [1]', 'numerical')
    m = nn * Mr(f)
    stem = f'{person(r)} needs to make {sf(V)} cm³ of {sf(c)} mol/dm³ {n}, {F(f)}. Calculate the mass of solute needed. {ar_data(f)}'
    key = f'n = {sf(c)} × {sf(V / 1000)} = {g3(nn)} mol [1]; Mr = {mr(Mr(f))}; mass = {g3(nn)} × {mr(Mr(f))} = {g3(m)} g [1]'
    if D >= 4:
        stem += ' Describe how the solution should be prepared.'
        key += '; dissolve in some distilled water, transfer to a volumetric flask with washings, make up to the mark and mix [2]'
    return Q(stem, f'{g3(m)} g', key, 'numerical')


@t5c.add('C3', (2, 3, 4))
def t5c_ratio(r, D):
    e, nm = r.choice(GASVOL)
    L, R = parse_eq(e)
    gas = [(n, f) for n, f, s in L + R if s == 'g']
    (n1, f1), (n2, f2) = r.sample(gas, 2)
    V1 = r.choice([10, 20, 30, 40, 50, 60, 100, 150])
    V2 = V1 * n2 / n1
    return Q(f'Use the equation {E(nostate(e))} to calculate the volume of {F(f2)} that reacts with or is produced from {V1} cm³ of {F(f1)}. All volumes are measured at the same temperature and pressure.',
             f'{sf(V2)} cm³', f'equal volumes of gases contain equal numbers of moles [1]; ratio {n1}:{n2} → {V1} × {n2}/{n1} = {sf(V2)} cm³ [1]', 'numerical')


@t5c.add('C2', (2, 3, 4), 'explain')
def t5c_err(r, D):
    n, f = r.choice(SOLUTES)
    c = r.choice(CONCS)
    V = r.choice([10.0, 20.0, 25.0, 50.0, 250.0])
    nn = c * V / 1000
    errs = [(f'calculates the moles of {n} in {sf(V)} cm³ of {sf(c)} mol/dm³ solution as {g3(c * V)} mol', f'The volume was not converted to dm³; n = {sf(c)} × {sf(V)}/1000 = {g3(nn)} mol.'),
            (f'says that {g3(nn * Mr(f))} g of {F(f)} dissolved to make {sf(V)} cm³ of solution gives a concentration of {g3(nn * Mr(f) / V * 1000)} mol/dm³', f'That value is the concentration in g/dm³; dividing by Mr ({mr(Mr(f))}) gives {g3(c)} mol/dm³.'),
            (f'says that 2 mol of oxygen gas occupies 24 dm³ at r.t.p. because oxygen is O₂', 'Each mole of molecules occupies 24 dm³, so 2 mol occupies 48 dm³.')]
    s, fix = r.choice(errs)
    return Q(f'{person(r)} {s}. Explain the error and give the correct answer.' + (f' {ar_data(f)}' if 'Mr' in fix else ''), fix, '1 mark: error identified; 1 mark: correct value [2]')


def _t5c_c4(r, D):
    e, sol, gas, ctx = r.choice([g for g in GASREAC if 'HCl' in g[0] or 'H2SO4' in g[0]])
    L, R = parse_eq(e)
    acid = 'HCl' if 'HCl' in e else 'H2SO4'
    na_ = [n for n, f, _ in L if f == acid][0]
    ns = [n for n, f, _ in L if f == sol][0]
    ng = [n for n, f, _ in R if f == gas][0]
    c = r.choice([0.5, 1.0, 2.0, 1.5])
    V = r.choice([20.0, 25.0, 40.0, 50.0])
    nacid = c * V / 1000
    m = r3(nacid / na_ * ns * Mr(sol) * r.choice([1.5, 2, 3]))
    p = person(r)
    intro = f'{p} adds {g3(m)} g of {F(sol)} to {sf(V)} cm³ of {sf(c)} mol/dm³ {"hydrochloric acid" if acid == "HCl" else "sulfuric acid"}. {E(nostate(e))} {ar_data(sol)}'
    n_s = m / Mr(sol)
    lim_acid = nacid / na_ < n_s / ns
    n_g = (nacid / na_ if lim_acid else n_s / ns) * ng
    parts = [
        lambda r: ('Calculate the number of moles of acid used.', f'{g3(nacid)} mol', f'{sf(c)} × {sf(V / 1000)} [1]'),
        lambda r: (f'Calculate the number of moles of {F(sol)} added.', f'{g3(n_s)} mol', f'{g3(m)} ÷ {mr(Mr(sol))} [1]'),
        lambda r: ('Deduce which reactant is in excess.', F(sol) if lim_acid else 'the acid', f'compare using ratio {ns}:{na_} [1]'),
        lambda r: (f'Calculate the maximum volume of {F(gas)} produced at r.t.p., in cm³.', f'{g3(n_g * 24000)} cm³', f'n({F(gas)}) = {g3(n_g)} mol [1]; × 24 000 [1] total [2]'),
        lambda r: ('Calculate the concentration of the acid in g/dm³.', f'{g3(c * Mr(acid))} g/dm³', f'{sf(c)} × {mr(Mr(acid))} [1]'),
        lambda r: (f'Describe how the volume of {F(gas)} could be measured.', 'collect in a gas syringe (or over water in an inverted measuring cylinder)', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t5c.add('C4', (2, 3, 4, 5), 'multi_step')(_t5c_c4)


# ---------------------------------------------------------- 5.4 empirical/molecular formulae, % composition, purity
EMPF = ['C2H4', 'C2H6', 'C4H10', 'C6H12', 'C6H6', 'C3H6', 'C6H12O6', 'C2H4O2', 'H2O2', 'N2O4', 'P4O10', 'C4H8', 'C8H18', 'C5H10', 'B2H6', 'C2H2', 'C3H8', 'CH4', 'C2H6O', 'C4H8O2']
IONIC_EMP = ['MgO', 'CuO', 'Cu2O', 'Fe2O3', 'Al2O3', 'Na2O', 'CaO', 'ZnO', 'PbO2', 'FeS', 'Al2S3', 'MgCl2', 'CaBr2', 'SO3', 'SO2', 'NO2', 'Fe3O4']
AR.setdefault('Br', 80)


def empirical(f):
    at = atoms(f)
    g = 0
    for v in at.values():
        g = math.gcd(g, v)
    return ''.join(e + (str(v // g) if v // g > 1 else '') for e, v in at.items()), g


def pct(f):
    M_ = Mr(f)
    return [(e, k * AR[e] / M_ * 100) for e, k in atoms(f).items()]


def emp_from_pct(ps):
    ms = [(e, p / AR[e]) for e, p in ps]
    lo = min(v for _, v in ms)
    rat = [(e, v / lo) for e, v in ms]
    for mult in (1, 2, 3, 4):
        if all(abs(x * mult - round(x * mult)) < 0.08 for _, x in rat):
            return ''.join(e + (str(round(x * mult)) if round(x * mult) > 1 else '') for e, x in rat), ms, rat, mult
    return None


t5d = T('Empirical and molecular formulae; percentage composition and percentage purity', 'empirical and molecular formulae', 'percentage composition', 'percentage purity')
t5d.fixed('C1', (1, 2), [
    ('What is an empirical formula?', 'the simplest whole-number ratio of atoms of each element in a compound', 'Empirical formula = simplest ratio.', ['the actual number of atoms in one molecule', 'the formula showing all bonds', 'the formula of the ions in a compound']),
    ('What is the empirical formula of ethane, C₂H₆?', 'CH₃', 'Divide 2:6 by 2 → 1:3.', ['C₂H₆', 'CH₂', 'C₂H₃']),
    ('A compound has the empirical formula CH₂ and Mr 56. What is its molecular formula?', 'C₄H₈', 'Mr(CH₂) = 14; 56/14 = 4 → C₄H₈.', ['C₂H₄', 'C₃H₆', 'C₅H₁₀']),
    ('Which compound has the same empirical and molecular formula?', 'water, H₂O', 'H₂O cannot be simplified.', ['hydrogen peroxide, H₂O₂', 'ethene, C₂H₄', 'glucose, C₆H₁₂O₆']),
    ('State the formula for calculating percentage purity.', 'percentage purity = (mass of pure substance ÷ mass of impure sample) × 100', '[1]'),
])
t5d.fixed('C2', (2, 3, 4), [
    ('Explain why the empirical formula of an ionic compound is the same as the formula normally written for it.', 'An ionic compound is a giant lattice, not discrete molecules; its formula already shows the simplest ratio of ions.', '[2]'),
    ('Explain why the empirical formula alone is not enough to identify a molecular compound.', 'Different compounds can share the same empirical formula (e.g. C₂H₄ and C₃H₆ are both CH₂); the Mr is needed to find the molecular formula.', '[2]'),
    ('Explain why a lid is lifted from time to time when magnesium is heated in a crucible to find the formula of magnesium oxide.', 'To let oxygen in so that all the magnesium reacts, while keeping the lid on most of the time stops magnesium oxide smoke escaping.', '1 mark: let oxygen in; 1 mark: prevent loss of product [2]'),
    ('Explain why it is important for medicines to have a high percentage purity.', 'Impurities could be harmful or reduce the effectiveness/dose of the active substance.', '[2]'),
])


@t5d.add('C3', (2, 3, 4, 5))
def t5d_emp(r, D):
    f = r.choice(EMPF + IONIC_EMP)
    ps = pct(f)
    ps_r = [(e, round(p, 1)) for e, p in ps]
    res = emp_from_pct(ps_r)
    ef, g = empirical(f)
    if not res or atoms(res[0]) != atoms(ef):
        return None
    _, ms, rat, mult = res
    use_mass = r.random() < 0.4
    if use_mass:
        tot = r.choice([2.0, 3.0, 4.6, 5.0, 10.0, 1.5])
        masses = [(e, round(p * tot / 100, 3)) for e, p in ps]
        res2 = emp_from_pct(masses)
        if not res2 or atoms(res2[0]) != atoms(ef):
            return None
        _, ms, rat, mult = res2
        data = ', '.join(f'{fmt_s(m_)} g of {e}' for e, m_ in masses)
        stem = f'Analysis of {sf(tot)} g of a compound shows that it contains {data}. Calculate the empirical formula of the compound. {ar_data(f)}'
    else:
        data = ', '.join(f'{e} {fmt_s(p)}%' for e, p in ps_r)
        stem = f'A compound has the following composition by mass: {data}. Calculate its empirical formula. {ar_data(f)}'
    key = 'moles: ' + ', '.join(f'{e} {g3(v)}' for e, v in ms) + ' [1]; divide by smallest: ' + ', '.join(f'{e} {g3(x)}' for e, x in rat) + (f' (× {mult})' if mult > 1 else '') + f' [1]; empirical formula {F(ef)} [1]'
    ans = F(ef)
    if D >= 4 and g > 1 and f in EMPF:
        stem += f' The relative molecular mass of the compound is {mr(Mr(f))}. Deduce its molecular formula.'
        key += f'; Mr(empirical) = {mr(Mr(ef))}; {mr(Mr(f))} ÷ {mr(Mr(ef))} = {g} → {F(f)} [1]'
        ans += f'; molecular formula {F(f)}'
    return Q(stem, ans, key, 'numerical')


@t5d.add('C3', (1, 2, 3, 4))
def t5d_pct(r, D):
    n, f = r.choice(MRLIST)
    el = r.choice(list(atoms(f)))
    k = atoms(f)[el]
    v = k * AR[el] / Mr(f) * 100
    if D == 1:
        return NM(r, f'What is the percentage by mass of {el} in {n}, {F(f)}? {ar_data(f)}', v, [AR[el] / Mr(f) * 100, v / 2 if k == 1 else AR[el] / Mr(f) * 100 * (k + 1), 100 - v, v * 1.2, k * AR[el]], '%',
                  f'{k} × {mr(AR[el])} ÷ {mr(Mr(f))} × 100 = {g3(v)}%')
    if 'H2O' in f and '.' in f and r.random() < 0.6:
        w = atoms('5H2O' if '5H2O' in f else 'H2O')
        x = int(f.split('.')[1].split('H2O')[0] or 1)
        vw = x * 18 / Mr(f) * 100
        return Q(f'Calculate the percentage by mass of water in {n}, {F(f)}. {ar_data(f)}', f'{g3(vw)}%', f'Mr = {mr(Mr(f))} [1]; {x} × 18 ÷ {mr(Mr(f))} × 100 = {g3(vw)}% [1]', 'numerical')
    stem = f'Calculate the percentage by mass of {el} in {n}, {F(f)}. {ar_data(f)}'
    key = f'Mr = {mr(Mr(f))} [1]; {k} × {mr(AR[el])} ÷ {mr(Mr(f))} × 100 = {g3(v)}% [1]'
    if D >= 3:
        mass = r.choice([10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0])
        stem += f' Hence calculate the mass of {el} in {sf(mass)} g of {F(f)}.'
        key += f'; mass = {g3(v)}/100 × {sf(mass)} = {g3(v * mass / 100)} g [1]'
        return Q(stem, f'{g3(v)}%; {g3(v * mass / 100)} g', key, 'numerical')
    return Q(stem, f'{g3(v)}%', key, 'numerical')


PURITY = [('limestone', 'CaCO3', 'CaCO3(s) -> CaO(s) + CO2(g)', 'CO2', 'heated strongly until constant mass; the carbon dioxide given off is measured'),
          ('a sample of impure magnesium', 'Mg', 'Mg(s) + 2HCl(aq) -> MgCl2(aq) + H2(g)', 'H2', 'added to excess hydrochloric acid; the hydrogen given off is measured'),
          ('impure zinc', 'Zn', 'Zn(s) + H2SO4(aq) -> ZnSO4(aq) + H2(g)', 'H2', 'added to excess dilute sulfuric acid; the hydrogen produced is measured'),
          ('impure sodium carbonate', 'Na2CO3', 'Na2CO3(s) + 2HCl(aq) -> 2NaCl(aq) + H2O(l) + CO2(g)', 'CO2', 'added to excess hydrochloric acid; the carbon dioxide produced is measured'),
          ('impure copper(II) carbonate', 'CuCO3', 'CuCO3(s) -> CuO(s) + CO2(g)', 'CO2', 'heated until no more gas is given off')]


@t5d.add('C3', (3, 4, 5))
def t5d_purity(r, D):
    nm, f, e, gas, how = r.choice(PURITY)
    m = r.choice([1.0, 2.0, 2.5, 5.0, 10.0, 0.5, 1.2, 4.0])
    pur = r.choice([75, 80, 85, 88, 90, 92, 95, 96])
    npure = m * pur / 100 / Mr(f)
    V = npure * 24000
    V = float(sf(V, 3).replace(',', ''))
    p = person(r)
    stem = f'{p} has {sf(m)} g of {nm}, containing {F(f)}. The sample is {how}: {sf(V, 3)} cm³ of {F(gas)} at r.t.p. is collected. {E(nostate(e))}. Calculate the percentage purity of the sample. (Assume the impurities do not produce gas.) {ar_data(f)}'
    ng = V / 24000
    mp = ng * Mr(f)
    key = f'n({F(gas)}) = {sf(V, 3)} ÷ 24 000 = {g3(ng)} mol [1]; n({F(f)}) = {g3(ng)} mol [1]; mass = {g3(ng)} × {mr(Mr(f))} = {g3(mp)} g [1]; purity = {g3(mp)} ÷ {sf(m)} × 100 = {g3(mp / m * 100)}% [1]'
    return Q(stem, f'{g3(mp / m * 100)}%', key, 'numerical')


@t5d.add('C2', (2, 3, 4), 'explain')
def t5d_mol(r, D):
    f = r.choice([x for x in EMPF if empirical(x)[1] > 1])
    ef, g = empirical(f)
    return Q(f'Compound Z has the empirical formula {F(ef)} and a relative molecular mass of {mr(Mr(f))}. Explain how to deduce its molecular formula and state the molecular formula. {ar_data(f)}',
             f'Mr of {F(ef)} = {mr(Mr(ef))}; {mr(Mr(f))} ÷ {mr(Mr(ef))} = {g}; multiply the empirical formula by {g}: {F(f)}.',
             f'1 mark: Mr of empirical formula {mr(Mr(ef))}; 1 mark: ratio {g}; 1 mark: {F(f)} [3]' if D >= 3 else f'1 mark: method (divide Mr by empirical Mr); 1 mark: {F(f)} [2]')


def _t5d_c4(r, D):
    met = r.choice([('magnesium', 'Mg', 'MgO'), ('copper', 'Cu', 'CuO'), ('calcium', 'Ca', 'CaO'), ('zinc', 'Zn', 'ZnO')])
    nm, s, ox = met
    m1 = r.choice([0.24, 0.36, 0.48, 0.6, 0.72, 1.2])
    if s != 'Mg':
        m1 = round(m1 * AR[s] / 24, 2)
    mo = m1 / AR[s] * Mr(ox)
    crucible = r.choice([18.42, 20.15, 22.67, 19.88, 21.04, 23.51])
    p = person(r)
    intro = (f'{p} heats {nm} in a crucible to find the formula of its oxide. Results: mass of crucible + lid = {crucible:.2f} g; mass of crucible + lid + {nm} = {crucible + m1:.2f} g; '
             f'mass of crucible + lid + oxide after heating to constant mass = {crucible + mo:.2f} g. {ar_data(ox)}')
    mO = round(crucible + mo, 2) - round(crucible + m1, 2)
    nM, nO = round(m1, 2) / AR[s], mO / 16
    parts = [
        lambda r: (f'Calculate the mass of {nm} used and the mass of oxygen that combined with it.', f'{m1:.2f} g; {mO:.2f} g', '1 mark each [2]'),
        lambda r: ('Calculate the empirical formula of the oxide.', F(ox), f'n({s}) = {g3(nM)}, n(O) = {g3(nO)} [1]; ratio ≈ 1:1 → {F(ox)} [1] total [2]'),
        lambda r: ('Explain why the crucible is heated to constant mass.', 'to make sure all the metal has reacted', '[1]'),
        lambda r: (f'Calculate the percentage by mass of {s} in the oxide.', f'{g3(AR[s] / Mr(ox) * 100)}%', f'{mr(AR[s])} ÷ {mr(Mr(ox))} × 100 [1]'),
        lambda r: ('Suggest why the student\'s ratio might be slightly lower in oxygen than expected.', 'some metal did not react / some oxide smoke escaped when the lid was lifted', '[1]'),
        lambda r: ('Explain why the lid is lifted occasionally during heating.', 'to let in air (oxygen) for the reaction while minimising loss of product', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


t5d.add('C4', (2, 3, 4, 5), 'case')(_t5d_c4)


# ---------------------------------------------------------- 5.5 titration calculations
TITR = [  # alkali name, formula, acid name, formula, alkali:acid ratio (a, b) as in a ALK + b ACID, equation
    ('sodium hydroxide', 'NaOH', 'hydrochloric acid', 'HCl', 1, 1, 'NaOH(aq) + HCl(aq) -> NaCl(aq) + H2O(l)'),
    ('potassium hydroxide', 'KOH', 'nitric acid', 'HNO3', 1, 1, 'KOH(aq) + HNO3(aq) -> KNO3(aq) + H2O(l)'),
    ('sodium hydroxide', 'NaOH', 'sulfuric acid', 'H2SO4', 2, 1, '2NaOH(aq) + H2SO4(aq) -> Na2SO4(aq) + 2H2O(l)'),
    ('potassium hydroxide', 'KOH', 'sulfuric acid', 'H2SO4', 2, 1, '2KOH(aq) + H2SO4(aq) -> K2SO4(aq) + 2H2O(l)'),
    ('sodium carbonate', 'Na2CO3', 'hydrochloric acid', 'HCl', 1, 2, 'Na2CO3(aq) + 2HCl(aq) -> 2NaCl(aq) + H2O(l) + CO2(g)'),
    ('aqueous ammonia', 'NH3', 'hydrochloric acid', 'HCl', 1, 1, 'NH3(aq) + HCl(aq) -> NH4Cl(aq)'),
    ('sodium hydroxide', 'NaOH', 'nitric acid', 'HNO3', 1, 1, 'NaOH(aq) + HNO3(aq) -> NaNO3(aq) + H2O(l)'),
    ('sodium carbonate', 'Na2CO3', 'sulfuric acid', 'H2SO4', 1, 1, 'Na2CO3(aq) + H2SO4(aq) -> Na2SO4(aq) + H2O(l) + CO2(g)'),
]
for _t in TITR:
    assert balanced(_t[6]), _t


def titres(r, true):
    rough = round(true + r.choice([0.6, 0.8, 1.0, 1.2, 0.5]), 1)
    tr = [round(true + r.choice([-0.05, 0.0, 0.05, 0.0]), 2) for _ in range(3)]
    odd = r.random() < 0.5
    if odd:
        i = r.randrange(3)
        tr[i] = round(true + r.choice([0.3, 0.4, -0.35, 0.45]), 2)
    conc = [x for x in tr if abs(x - true) <= 0.051]
    if len(conc) < 2:
        return None
    return rough, tr, conc


t5e = T('Titration calculations', 'titration calculations')
t5e.fixed('C1', (1, 2), [
    ('What is meant by concordant titres?', 'titres that agree within 0.10 cm³ of each other', 'Concordant results are within 0.10 cm³; only these are averaged.', ['titres that are exactly the same as the rough titre', 'the largest and smallest titres', 'titres within 1.0 cm³ of each other']),
    ('Which apparatus is used to measure 25.0 cm³ of alkali accurately into a conical flask?', 'volumetric pipette', 'A pipette delivers a fixed volume accurately.', ['measuring cylinder', 'beaker', 'burette funnel']),
    ('Why is the rough titre not used when calculating the mean titre?', 'It is only an approximate value done quickly to find the end-point.', 'The rough titre overshoots; only accurate concordant titres are averaged.', ['It is always the most accurate value.', 'It uses a different indicator.', 'It is measured with a pipette.']),
    ('What is the colour of methyl orange at the end-point when acid is added to alkali?', 'orange', 'Methyl orange: yellow in alkali, red in acid; orange at the end-point.', ['colourless', 'pink', 'blue']),
    ('State why the burette is rinsed with the solution it will contain before filling.', 'to remove water/impurities that would dilute the solution', '[1]'),
])
t5e.fixed('C2', (2, 3, 4), [
    ('Explain why the conical flask is swirled during a titration.', 'To mix the solutions so the acid and alkali react completely and the colour change at the end-point is seen accurately.', '[2]'),
    ('Explain why a white tile is placed under the conical flask.', 'It makes the colour change of the indicator easier to see, so the end-point is judged accurately.', '[1]'),
    ('Explain why the solution is added drop by drop near the end-point.', 'So that the end-point is not overshot; one drop can change the indicator colour.', '[2]'),
    ('A student does not rinse the burette with acid but leaves it wet with water. Explain the effect on the titre.', 'The acid is diluted, so more acid is needed to neutralise the alkali – the titre is too large and the calculated alkali concentration too high.', '[2]'),
])


@t5e.add('C3', (2, 3, 4, 5))
def t5e_calc(r, D):
    an, af, cn, cf, a, b, e = r.choice(TITR)
    Valk = r.choice([20.0, 25.0, 10.0])
    calk = r.choice([0.1, 0.08, 0.12, 0.15, 0.2, 0.05, 0.25])
    cacid = r.choice([0.1, 0.08, 0.12, 0.15, 0.2, 0.05, 0.25, 0.4])
    nalk = calk * Valk / 1000
    nacid = nalk * b / a
    true = round(nacid / cacid * 1000, 2)
    if not (10 <= true <= 45):
        return None
    true = round(true * 20) / 20
    T_ = titres(r, true)
    if not T_:
        return None
    rough, tr, conc = T_
    mean = sum(conc) / len(conc)
    p = person(r)
    ind = r.choice(['methyl orange', 'thymolphthalein'])
    unk = r.choice(['alkali', 'acid']) if D >= 3 else 'alkali'
    rows = f'rough {rough:.2f}; ' + '; '.join(f'titre {i + 1}: {x:.2f}' for i, x in enumerate(tr))
    if unk == 'alkali':
        intro = f'{p} titrates {sf(Valk, 3)} cm³ of {an} solution of unknown concentration with {sf(cacid)} mol/dm³ {cn}, using {ind} indicator. Titres (cm³): {rows}. {E(nostate(e))}'
        ncal = cacid * mean / 1000
        nal = ncal * a / b
        c_ = nal / (Valk / 1000)
        steps = [f'mean of concordant titres = ({" + ".join(f"{x:.2f}" for x in conc)}) ÷ {len(conc)} = {mean:.2f} cm³ [1]', f'n({F(cf)}) = {sf(cacid)} × {mean:.2f}/1000 = {g3(ncal)} mol [1]',
                 f'n({F(af)}) = {g3(nal)} mol (ratio {a}:{b}) [1]', f'c = {g3(nal)} ÷ {sf(Valk / 1000)} = {g3(c_)} mol/dm³ [1]']
        ans = f'mean titre {mean:.2f} cm³; concentration {g3(c_)} mol/dm³'
        q = 'Calculate the concentration of the ' + an + ' in mol/dm³.'
    else:
        intro = f'{p} titrates {sf(Valk, 3)} cm³ of {sf(calk)} mol/dm³ {an} with {cn} of unknown concentration, using {ind} indicator. Titres (cm³): {rows}. {E(nostate(e))}'
        nal = calk * Valk / 1000
        ncal = nal * b / a
        c_ = ncal / (mean / 1000)
        steps = [f'mean of concordant titres = {mean:.2f} cm³ [1]', f'n({F(af)}) = {sf(calk)} × {sf(Valk / 1000)} = {g3(nal)} mol [1]', f'n({F(cf)}) = {g3(ncal)} mol (ratio {a}:{b}) [1]',
                 f'c = {g3(ncal)} ÷ {mean / 1000:.5f} = {g3(c_)} mol/dm³ [1]']
        ans = f'mean titre {mean:.2f} cm³; concentration {g3(c_)} mol/dm³'
        q = 'Calculate the concentration of the ' + cn + ' in mol/dm³.'
    stem = f'{intro} Identify the concordant titres and calculate the mean titre. {q}'
    if D >= 5:
        stem += ' Convert your answer into g/dm³.'
        f_ = af if unk == 'alkali' else cf
        ans += f'; {g3(c_ * Mr(f_))} g/dm³'
        steps.append(f'× Mr {mr(Mr(f_))} = {g3(c_ * Mr(f_))} g/dm³ [1]')
    return Q(stem, ans, '; '.join(steps), 'case' if D >= 4 else 'numerical')


@t5e.add('C3', (1, 2, 3))
def t5e_mean(r, D):
    true = round(r.uniform(15, 35) * 20) / 20
    T_ = titres(r, true)
    if not T_:
        return None
    rough, tr, conc = T_
    mean = sum(conc) / len(conc)
    rows = f'rough {rough:.2f}, ' + ', '.join(f'{x:.2f}' for x in tr)
    if D == 1:
        return NM(r, f'A student\'s titres are (cm³): {rows}. What is the mean of the concordant titres?', mean, [sum(tr) / 3, (sum(tr) + rough) / 4, max(tr), rough], ' cm³',
                  f'Concordant: {", ".join(f"{x:.2f}" for x in conc)} → mean {mean:.2f} cm³', f=lambda x: f'{x:.2f}')
    return Q(f'Titration results (cm³): {rows}. Identify the concordant titres and calculate the mean titre, giving your answer to 2 decimal places.' + (' Explain why the rough titre is excluded.' if D >= 3 else ''),
             f'concordant: {", ".join(f"{x:.2f}" for x in conc)}; mean {mean:.2f} cm³' + ('; the rough titre is only approximate (end-point overshot).' if D >= 3 else ''),
             f'concordant identified [1]; mean {mean:.2f} cm³ [1]' + ('; reason [1]' if D >= 3 else ''), 'numerical')


@t5e.add('C3', (2, 3, 4))
def t5e_vol(r, D):
    an, af, cn, cf, a, b, e = r.choice(TITR)
    Valk = r.choice([20.0, 25.0])
    calk, cacid = r.choice([0.1, 0.2, 0.15, 0.05]), r.choice([0.1, 0.2, 0.25, 0.08])
    nacid = calk * Valk / 1000 * b / a
    V = nacid / cacid * 1000
    return Q(f'Calculate the volume of {sf(cacid)} mol/dm³ {cn} needed to neutralise {sf(Valk, 3)} cm³ of {sf(calk)} mol/dm³ {an}. {E(nostate(e))}',
             f'{g3(V)} cm³', f'n({F(af)}) = {g3(calk * Valk / 1000)} mol [1]; n({F(cf)}) = {g3(nacid)} mol [1]; V = {g3(nacid)} ÷ {sf(cacid)} × 1000 = {g3(V)} cm³ [1]', 'numerical')


@t5e.add('C2', (2, 3, 4), 'explain')
def t5e_err(r, D):
    errs = [('reads the burette from the top of the meniscus instead of the bottom', 'Every reading is wrong by a constant amount; read at eye level from the bottom of the meniscus.'),
            ('leaves an air bubble in the burette jet which disappears during the titration', 'The volume delivered appears larger than it really is, so the titre is too high; remove the bubble before the first reading.'),
            ('uses a measuring cylinder instead of a pipette for the alkali', 'A measuring cylinder is much less accurate, so the volume of alkali (and the calculated concentration) is less reliable.'),
            ('adds a lot of indicator', 'Indicators are weak acids/bases and can affect the titre; only a few drops should be used.'),
            ('averages all four results including the rough titre', 'The rough titre overshoots the end-point; only concordant titres (within 0.10 cm³) should be averaged.'),
            ('rinses the conical flask with the alkali before adding the pipetted volume', 'Extra alkali stays in the flask, so the titre is too large; rinse the flask with distilled water only.')]
    s, fix = r.choice(errs)
    return Q(f'During a titration, {person(r)} {s}. Explain the effect on the results and how the procedure should be improved.', fix, '1 mark: effect; 1 mark: improvement [2]')


def _t5e_c4(r, D):
    an, af, cn, cf, a, b, e = r.choice(TITR)
    Valk = 25.0
    calk = r.choice([0.1, 0.08, 0.12, 0.2])
    cacid = r.choice([0.1, 0.15, 0.2, 0.05])
    nacid = calk * Valk / 1000 * b / a
    true = round(nacid / cacid * 1000 * 20) / 20
    if not (10 <= true <= 45):
        return None
    T_ = titres(r, true)
    if not T_:
        return None
    rough, tr, conc = T_
    mean = sum(conc) / len(conc)
    c_ = cacid * mean / 1000 * a / b / (Valk / 1000)
    p = person(r)
    intro = f'{p} carries out a titration to find the concentration of a solution of {an}. 25.0 cm³ of the {an} is titrated with {sf(cacid)} mol/dm³ {cn}. Titres (cm³): rough {rough:.2f}, ' + ', '.join(f'{x:.2f}' for x in tr) + f'. {E(nostate(e))}'
    parts = [
        lambda r: (f'Name the apparatus used to measure the 25.0 cm³ of {an} and the apparatus used to add the acid.', 'volumetric pipette; burette', '1 mark each [2]'),
        lambda r: ('Suggest a suitable indicator and give the colour change at the end-point.', 'methyl orange: yellow to orange (or thymolphthalein: blue to colourless)', '1 mark indicator; 1 mark colours [2]'),
        lambda r: ('Calculate the mean of the concordant titres.', f'{mean:.2f} cm³', 'concordant only [1]'),
        lambda r: (f'Calculate the concentration of the {an} in mol/dm³.', f'{g3(c_)} mol/dm³', f'n(acid) = {g3(cacid * mean / 1000)} mol; ratio {a}:{b}; ÷ 0.025 dm³ [3]'),
        lambda r: ('Explain why the titration is repeated until concordant results are obtained.', 'to check reliability / identify and discard anomalous results', '[1]'),
        lambda r: ('Describe how the end-point is found accurately.', 'add acid dropwise near the end-point, swirling, until one drop changes the indicator colour permanently', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


t5e.add('C4', (2, 3, 4, 5), 'case')(_t5e_c4)

CHAPTERS[5] = [t5a, t5b, t5c, t5d, t5e]


# ===================================================================== Ch6 Electrochemistry
MOLTEN = [  # name, formula, metal, metal sym, charge, non-metal product, product formula, anion sym, anion charge, anode observation, cathode observation
    ('lead(II) bromide', 'PbBr2', 'lead', 'Pb', 2, 'bromine', 'Br2', 'Br', 1, 'red-brown vapour', 'grey/silvery liquid lead collects below the cathode'),
    ('sodium chloride', 'NaCl', 'sodium', 'Na', 1, 'chlorine', 'Cl2', 'Cl', 1, 'bubbles of pale green gas', 'silvery liquid sodium forms'),
    ('potassium iodide', 'KI', 'potassium', 'K', 1, 'iodine', 'I2', 'I', 1, 'purple vapour', 'silvery liquid potassium forms'),
    ('zinc chloride', 'ZnCl2', 'zinc', 'Zn', 2, 'chlorine', 'Cl2', 'Cl', 1, 'bubbles of pale green gas', 'grey liquid zinc forms'),
    ('lithium bromide', 'LiBr', 'lithium', 'Li', 1, 'bromine', 'Br2', 'Br', 1, 'red-brown vapour', 'silvery liquid lithium forms'),
    ('calcium chloride', 'CaCl2', 'calcium', 'Ca', 2, 'chlorine', 'Cl2', 'Cl', 1, 'bubbles of pale green gas', 'grey calcium metal forms'),
    ('aluminium oxide (dissolved in molten cryolite)', 'Al2O3', 'aluminium', 'Al', 3, 'oxygen', 'O2', 'O', 2, 'bubbles of gas (oxygen)', 'molten aluminium collects'),
    ('lead(II) iodide', 'PbI2', 'lead', 'Pb', 2, 'iodine', 'I2', 'I', 1, 'purple vapour', 'grey liquid lead forms'),
    ('magnesium chloride', 'MgCl2', 'magnesium', 'Mg', 2, 'chlorine', 'Cl2', 'Cl', 1, 'bubbles of pale green gas', 'silvery liquid magnesium forms'),
    ('zinc bromide', 'ZnBr2', 'zinc', 'Zn', 2, 'bromine', 'Br2', 'Br', 1, 'red-brown vapour', 'grey liquid zinc forms'),
    ('potassium bromide', 'KBr', 'potassium', 'K', 1, 'bromine', 'Br2', 'Br', 1, 'red-brown vapour', 'silvery liquid potassium forms'),
    ('sodium iodide', 'NaI', 'sodium', 'Na', 1, 'iodine', 'I2', 'I', 1, 'purple vapour', 'silvery liquid sodium forms'),
]


def cath_eq(sym, q):
    return f'{ionf(sym, q)} + {str(q) if q > 1 else ""}e⁻ → {sym}'


def anode_eq(sym, q):
    if sym == 'O':
        return '2O²⁻ → O₂ + 4e⁻'
    return f'2{ionf(sym, 1, True)} → {F(sym + "2")} + 2e⁻'


t6a = T('Electrolysis of molten binary ionic compounds', 'electrolysis of molten binary ionic compounds', 'molten')
t6a.fixed('C1', (1, 2), [
    ('What is electrolysis?', 'the decomposition of an ionic compound, when molten or in aqueous solution, by the passage of an electric current', 'Definition of electrolysis.',
     ['the movement of electrons through a metal wire', 'the dissolving of an ionic compound in water', 'the reaction of a metal with an acid']),
    ('What is the name of the negative electrode?', 'cathode', 'Cathode = negative; cations are attracted to it.', ['anode', 'electrolyte', 'anion']),
    ('Why must lead(II) bromide be molten before it can be electrolysed?', 'The ions must be free to move.', 'In the solid the ions are fixed in the lattice.', ['The electrons must be free to move.', 'It must react with oxygen.', 'The bromine must be a gas.']),
    ('Which product forms at the anode when molten sodium chloride is electrolysed?', 'chlorine', 'Cl⁻ ions are attracted to the anode and lose electrons.', ['sodium', 'hydrogen', 'oxygen']),
    ('Which material is commonly used for inert electrodes?', 'graphite (carbon)', 'Graphite conducts and is unreactive.', ['iron', 'copper', 'zinc']),
    ('State the name given to the liquid or solution that conducts electricity and is decomposed during electrolysis.', 'electrolyte', '[1]'),
])
t6a.fixed('C2', (2, 3, 4), [
    ('Explain why solid lead(II) bromide does not conduct electricity but molten lead(II) bromide does.', 'In the solid the ions are held in fixed positions in the lattice; when molten the ions can move to the electrodes and carry the charge.', '1 mark: solid ions fixed; 1 mark: molten ions mobile [2]'),
    ('Describe how charge is carried in the external circuit and in the electrolyte during electrolysis.', 'Electrons flow through the external wires; ions move through the electrolyte (cations to the cathode, anions to the anode).', '1 mark: electrons in wires; 1 mark: ions in electrolyte [2]'),
    ('Explain why a metal is always formed at the cathode when a molten binary ionic compound is electrolysed.', 'The metal ions are positive, so they are attracted to the negative cathode, where they gain electrons and become metal atoms.', '[2]'),
    ('Explain why electrolysis of molten lead(II) bromide should be done in a fume cupboard.', 'Bromine vapour is produced at the anode and it is toxic.', '[1]'),
    ('Explain the meaning of the term binary compound in "molten binary ionic compound".', 'A compound made of only two elements, such as a metal and a non-metal (e.g. NaCl).', '[1]'),
])


@t6a.add('C1', (1, 2, 3))
def t6a_prod(r, D):
    m = r.choice(MOLTEN)
    nm, f, met, ms, q, nmet, nf, an, aq, obs_a, obs_c = m
    if D <= 2:
        el = r.choice(['cathode', 'anode'])
        corr = met if el == 'cathode' else nmet
        return M(r, f'Molten {nm} is electrolysed using inert electrodes. Which product forms at the {el}?', corr, list({x[2] for x in MOLTEN} | {x[5] for x in MOLTEN} | {'hydrogen'}),
                 f'{cap(met)} at the cathode ({cath_eq(ms, q)}); {nmet} at the anode ({anode_eq(an, aq)}).')
    pool = [f'{x}; {y}' for x, y in [(nmet, met), ('hydrogen', nmet), (met, 'oxygen' if nmet != 'oxygen' else 'chlorine'), ('hydrogen', 'oxygen')]]
    return M(r, f'Which row shows the products at the cathode and anode when molten {nm} is electrolysed?', f'{met}; {nmet}', pool,
             f'Cathode: {met}; anode: {nmet}.')


@t6a.add('C3', (2, 3, 4, 5))
def t6a_half(r, D):
    m = r.choice(MOLTEN)
    nm, f, met, ms, q, nmet, nf, an, aq, obs_a, obs_c = m
    stem = f'Molten {nm}, {F(f)}, is electrolysed using graphite electrodes. Name the products at each electrode and write the ionic half-equation for the reaction at each electrode.'
    key = f'cathode: {met} [1]; {cath_eq(ms, q)} [1]; anode: {nmet} [1]; {anode_eq(an, aq)} [1]'
    ans = f'cathode: {met}, {cath_eq(ms, q)}; anode: {nmet}, {anode_eq(an, aq)}'
    if D >= 4:
        stem += ' State which electrode reaction is oxidation and explain why.'
        key += '; anode is oxidation: anions lose electrons [1]'
        ans += '; the anode reaction is oxidation (electron loss).'
    if D == 2:
        stem = f'Write the ionic half-equation for the formation of {met} at the cathode during the electrolysis of molten {nm}.'
        return Q(stem, cath_eq(ms, q), f'{cath_eq(ms, q)}: species [1]; electrons balanced [1]', 'short')
    return Q(stem, ans, key, 'short')


@t6a.add('C2', (2, 3, 4), 'explain')
def t6a_explain(r, D):
    m = r.choice(MOLTEN)
    nm, f, met, ms, q, nmet, nf, an, aq, obs_a, obs_c = m
    return Q(f'Explain how {met} and {nmet} are formed at the electrodes when molten {nm} is electrolysed. Refer to the movement of ions and electrons.',
             f'{ionf(ms, q)} ions move to the cathode (negative) and gain electrons to form {met}; {ionf(an, aq, True) if an != "O" else "O²⁻"} ions move to the anode (positive) and lose electrons to form {nmet}. Electrons flow through the external circuit from anode to cathode.',
             '1 mark: cations to cathode gain electrons; 1 mark: anions to anode lose electrons; ' + ('1 mark: electrons flow through external circuit [3]' if D >= 3 else 'total [2]'))


def _t6a_c4(r, D):
    m = r.choice(MOLTEN)
    nm, f, met, ms, q, nmet, nf, an, aq, obs_a, obs_c = m
    p = person(r)
    intro = r.choice([f'{p} electrolyses molten {nm}, {F(f)}, using graphite electrodes.', f'In an industrial process in {city(r)}, molten {nm}, {F(f)}, is electrolysed using inert electrodes.'])
    parts = [
        lambda r: ('Explain why the compound must be molten.', 'so that the ions are free to move to the electrodes', '[1]'),
        lambda r: ('Describe what is observed at each electrode.', f'cathode: {obs_c}; anode: {obs_a}', '1 mark each [2]'),
        lambda r: ('Write the half-equation for the reaction at the cathode.', cath_eq(ms, q), '[1]'),
        lambda r: ('Write the half-equation for the reaction at the anode.', anode_eq(an, aq), '[1]'),
        lambda r: ('Identify which electrode reaction is reduction, giving a reason.', 'cathode: metal ions gain electrons', '[2]'),
        lambda r: ('Explain why graphite is used for the electrodes.', 'it conducts electricity and is inert (unreactive) with high melting point', '[1]'),
        lambda r: ('Describe the movement of electrons in the external circuit.', 'from the anode through the wires to the cathode (via the power supply)', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t6a.add('C4', (2, 3, 4, 5), 'multi_step')(_t6a_c4)
t6a.add('C3', (4, 5), 'multi_step')(_t6a_c4)


# ---------------------------------------------------------- 6.2 aqueous electrolysis
AQ = [  # name, formula, ions, cathode, anode, cathode eq, anode eq, note
    ('concentrated aqueous sodium chloride', 'NaCl', 'Na⁺, Cl⁻, H⁺, OH⁻', 'hydrogen', 'chlorine', '2H⁺ + 2e⁻ → H₂', '2Cl⁻ → Cl₂ + 2e⁻', 'sodium hydroxide solution remains'),
    ('concentrated hydrochloric acid', 'HCl', 'H⁺, Cl⁻, OH⁻', 'hydrogen', 'chlorine', '2H⁺ + 2e⁻ → H₂', '2Cl⁻ → Cl₂ + 2e⁻', ''),
    ('dilute sulfuric acid', 'H2SO4', 'H⁺, SO₄²⁻, OH⁻', 'hydrogen', 'oxygen', '2H⁺ + 2e⁻ → H₂', '4OH⁻ → O₂ + 2H₂O + 4e⁻', 'twice the volume of hydrogen as oxygen'),
    ('aqueous copper(II) sulfate', 'CuSO4', 'Cu²⁺, SO₄²⁻, H⁺, OH⁻', 'copper', 'oxygen', 'Cu²⁺ + 2e⁻ → Cu', '4OH⁻ → O₂ + 2H₂O + 4e⁻', 'the blue colour fades and the solution becomes acidic'),
    ('concentrated aqueous copper(II) chloride', 'CuCl2', 'Cu²⁺, Cl⁻, H⁺, OH⁻', 'copper', 'chlorine', 'Cu²⁺ + 2e⁻ → Cu', '2Cl⁻ → Cl₂ + 2e⁻', ''),
    ('concentrated aqueous potassium bromide', 'KBr', 'K⁺, Br⁻, H⁺, OH⁻', 'hydrogen', 'bromine', '2H⁺ + 2e⁻ → H₂', '2Br⁻ → Br₂ + 2e⁻', 'potassium hydroxide solution remains'),
    ('concentrated aqueous potassium iodide', 'KI', 'K⁺, I⁻, H⁺, OH⁻', 'hydrogen', 'iodine', '2H⁺ + 2e⁻ → H₂', '2I⁻ → I₂ + 2e⁻', ''),
    ('aqueous sodium hydroxide', 'NaOH', 'Na⁺, OH⁻, H⁺', 'hydrogen', 'oxygen', '2H⁺ + 2e⁻ → H₂', '4OH⁻ → O₂ + 2H₂O + 4e⁻', ''),
    ('aqueous sodium sulfate', 'Na2SO4', 'Na⁺, SO₄²⁻, H⁺, OH⁻', 'hydrogen', 'oxygen', '2H⁺ + 2e⁻ → H₂', '4OH⁻ → O₂ + 2H₂O + 4e⁻', ''),
    ('aqueous potassium nitrate', 'KNO3', 'K⁺, NO₃⁻, H⁺, OH⁻', 'hydrogen', 'oxygen', '2H⁺ + 2e⁻ → H₂', '4OH⁻ → O₂ + 2H₂O + 4e⁻', ''),
    ('aqueous silver nitrate', 'AgNO3', 'Ag⁺, NO₃⁻, H⁺, OH⁻', 'silver', 'oxygen', 'Ag⁺ + e⁻ → Ag', '4OH⁻ → O₂ + 2H₂O + 4e⁻', ''),
    ('concentrated aqueous copper(II) bromide', 'CuBr2', 'Cu²⁺, Br⁻, H⁺, OH⁻', 'copper', 'bromine', 'Cu²⁺ + 2e⁻ → Cu', '2Br⁻ → Br₂ + 2e⁻', ''),
    ('aqueous magnesium sulfate', 'MgSO4', 'Mg²⁺, SO₄²⁻, H⁺, OH⁻', 'hydrogen', 'oxygen', '2H⁺ + 2e⁻ → H₂', '4OH⁻ → O₂ + 2H₂O + 4e⁻', ''),
]
TESTS = {'hydrogen': 'a lighted splint gives a squeaky pop', 'oxygen': 'a glowing splint relights', 'chlorine': 'damp blue litmus paper turns red then is bleached white',
         'bromine': 'the solution near the anode turns orange/brown', 'iodine': 'the solution near the anode turns brown', 'copper': 'a pink-brown solid coats the cathode', 'silver': 'a silvery/grey solid coats the cathode'}
CATH_RULE = {'hydrogen': 'the metal is more reactive than hydrogen, so H⁺ ions are discharged instead', 'copper': 'copper is less reactive than hydrogen, so Cu²⁺ ions are discharged', 'silver': 'silver is less reactive than hydrogen, so Ag⁺ ions are discharged'}
AN_RULE = {'chlorine': 'halide ions in a concentrated solution are discharged', 'bromine': 'halide ions in a concentrated solution are discharged', 'iodine': 'halide ions in a concentrated solution are discharged',
           'oxygen': 'there are no halide ions, so OH⁻ ions are discharged to give oxygen'}

t6b = T('Electrolysis of aqueous solutions: predicting products at the electrodes', 'electrolysis of aqueous solutions', 'predicting products at the electrodes')
t6b.fixed('C1', (1, 2), [
    ('Which ions are present in all aqueous solutions, in addition to the ions of the dissolved compound?', 'H⁺ and OH⁻', 'Water ionises slightly: H₂O ⇌ H⁺ + OH⁻.', ['Na⁺ and Cl⁻', 'O²⁻ and H⁺', 'H₃O⁺ and Cl⁻']),
    ('What forms at the cathode when concentrated aqueous sodium chloride is electrolysed?', 'hydrogen', 'Na is more reactive than H, so H⁺ is discharged.', ['sodium', 'chlorine', 'oxygen']),
    ('What forms at the anode when dilute sulfuric acid is electrolysed with inert electrodes?', 'oxygen', 'No halide; OH⁻ discharged → O₂.', ['hydrogen', 'sulfur', 'sulfur dioxide']),
    ('Which test identifies the gas produced at the anode when concentrated hydrochloric acid is electrolysed?', 'It bleaches damp litmus paper.', 'Chlorine bleaches damp litmus.', ['It relights a glowing splint.', 'It gives a squeaky pop with a lighted splint.', 'It turns limewater milky.']),
    ('Which metal can be deposited at the cathode from its aqueous solution?', 'copper', 'Only metals less reactive than hydrogen are deposited.', ['sodium', 'magnesium', 'potassium']),
    ('State the product at the cathode when aqueous copper(II) sulfate is electrolysed with graphite electrodes.', 'copper', '[1]'),
])
t6b.fixed('C2', (2, 3, 4), [
    ('Explain why hydrogen, not sodium, is produced at the cathode when concentrated aqueous sodium chloride is electrolysed.', 'Sodium is more reactive than hydrogen, so H⁺ ions (from water) gain electrons more readily than Na⁺ ions; hydrogen gas forms.', '1 mark: Na more reactive than H; 1 mark: H⁺ discharged [2]'),
    ('Explain why the blue colour of copper(II) sulfate solution fades during electrolysis with inert electrodes.', 'Cu²⁺ ions, which cause the blue colour, are removed from solution as copper is deposited on the cathode.', '[2]'),
    ('Explain why the solution becomes alkaline during the electrolysis of concentrated aqueous sodium chloride.', 'H⁺ and Cl⁻ ions are removed; Na⁺ and OH⁻ ions remain, forming sodium hydroxide.', '[2]'),
    ('Explain why the volume of hydrogen collected is twice the volume of oxygen when dilute sulfuric acid is electrolysed.', 'For every 4 electrons, 2 H₂ are formed at the cathode (4H⁺ + 4e⁻ → 2H₂) but only 1 O₂ at the anode (4OH⁻ → O₂ + 2H₂O + 4e⁻).', '[2]'),
    ('Explain why oxygen, not chlorine, may be the main product at the anode when very dilute aqueous sodium chloride is electrolysed.', 'In a dilute solution the concentration of Cl⁻ ions is low, so OH⁻ ions are discharged instead, giving oxygen.', '[2]'),
])


@t6b.add('C1', (1, 2, 3))
def t6b_prod(r, D):
    x = r.choice(AQ)
    nm, f, ions, cat, ano, ce, ae, note = x
    if D <= 2:
        el = r.choice(['cathode', 'anode'])
        corr = cat if el == 'cathode' else ano
        pool = ['hydrogen', 'oxygen', 'chlorine', 'copper', 'sodium', 'bromine', 'sulfur', 'potassium', 'silver', 'iodine']
        return M(r, f'{cap(nm)} is electrolysed using inert electrodes. What is formed at the {el}?', corr, pool, f'Cathode: {cat} ({CATH_RULE[cat]}); anode: {ano} ({AN_RULE[ano]}).')
    pool = [f'{a}; {b}' for a, b in [(ano, cat), ('hydrogen', 'oxygen'), ('hydrogen', 'chlorine'), ('copper', 'oxygen'), (f.split('2')[0] if False else 'sodium', ano)]]
    return M(r, f'Which row shows the products at the cathode and the anode when {nm} is electrolysed with inert electrodes?', f'{cat}; {ano}', pool, f'Cathode {cat}; anode {ano}.')


@t6b.add('C3', (2, 3, 4, 5))
def t6b_predict(r, D):
    x = r.choice(AQ)
    nm, f, ions, cat, ano, ce, ae, note = x
    p = person(r)
    stem = f'{p} electrolyses {nm} using graphite electrodes. List the ions present in the solution and predict the product at each electrode, explaining your predictions.'
    ans = f'Ions: {ions}. Cathode: {cat} – {CATH_RULE[cat]}. Anode: {ano} – {AN_RULE[ano]}.'
    key = f'ions {ions} [1]; cathode {cat} with reason [1]; anode {ano} with reason [1]'
    if D >= 4:
        stem += ' Write the half-equation at each electrode and describe a test for each product.'
        ans += f' {ce}; {ae}. Tests: {cat} – {TESTS[cat]}; {ano} – {TESTS[ano]}.'
        key += f'; {ce} [1]; {ae} [1]; tests [1]'
    return Q(stem, ans, key, 'short' if D <= 3 else 'case')


@t6b.add('C2', (2, 3, 4), 'explain')
def t6b_why(r, D):
    x = r.choice(AQ)
    nm, f, ions, cat, ano, ce, ae, note = x
    which = r.choice(['cathode', 'anode'])
    if which == 'cathode':
        return Q(f'Explain why {cat} is produced at the cathode when {nm} is electrolysed.', f'Positive ions present are {", ".join(i for i in ions.split(", ") if "⁺" in i)}; {CATH_RULE[cat]}.',
                 '1 mark: identifies cations present; 1 mark: reactivity reasoning [2]')
    return Q(f'Explain why {ano} is produced at the anode when {nm} is electrolysed.', f'Negative ions present are {", ".join(i for i in ions.split(", ") if "⁻" in i)}; {AN_RULE[ano]}.',
             '1 mark: identifies anions present; 1 mark: rule applied [2]')


@t6b.add('C3', (1, 2, 3))
def t6b_test(r, D):
    x = r.choice(AQ)
    nm, f, ions, cat, ano, ce, ae, note = x
    prod = r.choice([cat, ano])
    el = 'cathode' if prod == cat else 'anode'
    return M(r, f'{cap(nm)} is electrolysed with inert electrodes. Which observation identifies the product at the {el}?', cap(TESTS[prod]) + '.', [cap(v) + '.' for k, v in TESTS.items() if k != prod] + ['Limewater turns milky.'],
             f'{cap(el)} product: {prod} – {TESTS[prod]}.')


def _t6b_c4(r, D):
    x = r.choice(AQ)
    nm, f, ions, cat, ano, ce, ae, note = x
    p = person(r)
    intro = r.choice([f'{p} sets up a cell to electrolyse {nm} using inert graphite electrodes.', f'A technician in {city(r)} electrolyses {nm} with carbon electrodes and collects the products.'])
    parts = [
        lambda r: ('List all the ions present in the solution.', ions, '[1]'),
        lambda r: ('Name the product at the cathode and explain why it forms.', f'{cat}: {CATH_RULE[cat]}', '1 mark product; 1 mark reason [2]'),
        lambda r: ('Name the product at the anode and explain why it forms.', f'{ano}: {AN_RULE[ano]}', '1 mark product; 1 mark reason [2]'),
        lambda r: ('Write the half-equation for the reaction at the cathode.', ce, '[1]'),
        lambda r: ('Write the half-equation for the reaction at the anode.', ae, '[1]'),
        lambda r: ('Describe a test to identify the product at the anode.', TESTS[ano], '[1]'),
        lambda r: ('Describe one change in the electrolyte during the experiment.', note or 'the concentration of the dissolved compound changes as ions are discharged', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t6b.add('C4', (2, 3, 4, 5), 'multi_step')(_t6b_c4)
t6b.add('C3', (4, 5), 'multi_step')(_t6b_c4)


# ---------------------------------------------------------- 6.3 half-equations, electroplating, purification
PLATE = [('steel spoon', 'silver', 'Ag', 1, 'silver nitrate'), ('iron key', 'copper', 'Cu', 2, 'copper(II) sulfate'), ('steel bicycle bell', 'nickel', 'Ni', 2, 'nickel(II) sulfate'),
         ('brass medal', 'silver', 'Ag', 1, 'silver nitrate'), ('steel can', 'tin', 'Sn', 2, 'tin(II) sulfate'), ('steel bolt', 'zinc', 'Zn', 2, 'zinc sulfate'),
         ('copper bracelet', 'silver', 'Ag', 1, 'silver nitrate'), ('steel tap', 'nickel', 'Ni', 2, 'nickel(II) sulfate'), ('iron door handle', 'copper', 'Cu', 2, 'copper(II) sulfate')]
AR.setdefault('Ni', 59)
AR.setdefault('Sn', 119)

t6c = T('Ionic half-equations at electrodes; electroplating and purification of copper', 'ionic half-equations at electrodes', 'electroplating', 'purification of copper')
t6c.fixed('C1', (1, 2), [
    ('In electroplating, where is the object to be plated placed?', 'as the cathode', 'Metal ions gain electrons and deposit on the cathode.', ['as the anode', 'in the electrolyte without connection', 'between the electrodes']),
    ('Which electrolyte is used to electroplate an object with silver?', 'aqueous silver nitrate', 'The electrolyte must contain ions of the plating metal.', ['aqueous sodium chloride', 'dilute sulfuric acid', 'aqueous copper(II) sulfate']),
    ('In the purification of copper, what is the anode made of?', 'impure copper', 'Impure copper anode dissolves; pure copper deposits on the cathode.', ['pure copper', 'graphite', 'platinum']),
    ('Which half-equation shows what happens at the anode during the purification of copper?', 'Cu → Cu²⁺ + 2e⁻', 'The copper anode is oxidised and dissolves.', ['Cu²⁺ + 2e⁻ → Cu', '4OH⁻ → O₂ + 2H₂O + 4e⁻', '2H⁺ + 2e⁻ → H₂']),
    ('Give two reasons why metals are electroplated.', 'to improve appearance; to resist corrosion', '1 mark each [2]'),
])
t6c.fixed('C2', (2, 3, 4), [
    ('Explain why the concentration of copper(II) ions in the electrolyte stays constant during the purification of copper.', 'Copper atoms at the anode lose electrons and go into solution as Cu²⁺ at the same rate as Cu²⁺ ions gain electrons and are deposited at the cathode.', '[2]'),
    ('Explain what happens to the impurities in the impure copper anode during purification.', 'Insoluble impurities (e.g. silver, gold) fall to the bottom as anode sludge; more reactive metals dissolve as ions and stay in solution.', '[2]'),
    ('Explain why the electrolyte in electroplating must contain ions of the plating metal.', 'These ions are discharged (gain electrons) at the cathode to form the metal coating; the anode of the same metal replaces them.', '[2]'),
    ('Explain why a copper anode gets smaller when copper(II) sulfate solution is electrolysed using copper electrodes.', 'Copper atoms at the anode are oxidised to Cu²⁺ ions (Cu → Cu²⁺ + 2e⁻), which pass into solution.', '[2]'),
])


@t6c.add('C1', (1, 2, 3))
def t6c_half(r, D):
    sym, q, nm = r.choice([('Cu', 2, 'copper'), ('Ag', 1, 'silver'), ('Zn', 2, 'zinc'), ('Pb', 2, 'lead'), ('Al', 3, 'aluminium'), ('Na', 1, 'sodium'), ('Ni', 2, 'nickel'), ('Mg', 2, 'magnesium'), ('Fe', 3, 'iron')])
    corr = cath_eq(sym, q)
    pool = [f'{ionf(sym, q)} → {sym} + {q if q > 1 else ""}e⁻', f'{ionf(sym, q)} + {q + 1}e⁻ → {sym}', f'{sym} + {q if q > 1 else ""}e⁻ → {ionf(sym, q)}', f'{ionf(sym, q)} + e⁻ → {sym}' if q > 1 else f'{ionf(sym, q)} + 2e⁻ → {sym}']
    return M(r, f'Which is the correct half-equation for the formation of {nm} at the cathode from {ionf(sym, q)} ions?', corr, pool, f'Reduction at cathode: {corr} (charges balance).')


@t6c.add('C3', (2, 3, 4, 5))
def t6c_plate(r, D):
    obj, met, sym, q, el = r.choice(PLATE)
    p = person(r)
    stem = f'{p} wants to electroplate a {obj} with {met}. Describe the set-up: name the anode, the cathode and the electrolyte, and write the half-equations at each electrode.'
    ans = f'anode: {met}; cathode: the {obj}; electrolyte: aqueous {el}. Cathode: {cath_eq(sym, q)}; anode: {sym} → {ionf(sym, q)} + {str(q) if q > 1 else ""}e⁻'
    key = f'anode {met} [1]; cathode {obj} [1]; electrolyte {el} [1]; {cath_eq(sym, q)} [1]; anode half-equation [1]'
    if D <= 2:
        stem = f'A {obj} is to be electroplated with {met}. Name the anode, the cathode and a suitable electrolyte.'
        return Q(stem, f'anode: {met}; cathode: {obj}; electrolyte: aqueous {el}', f'1 mark each [3]', 'short')
    if D >= 5:
        dm = r.choice([0.27, 0.54, 1.08, 0.32, 0.64, 1.28, 0.59])
        stem += f' After plating, the mass of the anode has decreased by {dm} g. State the increase in mass of the {obj} and calculate the moles of {met} transferred.'
        ans += f'; increase {dm} g; {g3(dm / AR[sym])} mol'
        key += f'; same mass gained {dm} g [1]; n = {dm} ÷ {mr(AR[sym])} = {g3(dm / AR[sym])} mol [1]'
    return Q(stem, ans, key, 'short')


@t6c.add('C3', (3, 4, 5))
def t6c_purify(r, D):
    loss = r.choice([2.50, 3.20, 4.00, 5.60, 6.40, 8.00, 10.0, 12.5])
    pur = r.choice([90, 92, 94, 95, 96, 98, 97.5])
    gain = round(loss * pur / 100, 2)
    p = person(r)
    stem = f'{p} purifies copper by electrolysis. During the experiment the impure copper anode loses {loss:.2f} g and the pure copper cathode gains {gain:.2f} g. Calculate the percentage of copper in the impure anode and explain why the two masses are different.'
    ans = f'{g3(gain / loss * 100)}%; the anode also contained impurities, which fell as sludge or dissolved without being deposited.'
    key = f'% = {gain:.2f} ÷ {loss:.2f} × 100 [1] = {g3(gain / loss * 100)}% [1]; impurities lost from anode do not deposit on cathode [1]'
    if D >= 4:
        stem += ' Write the half-equations at the anode and the cathode.'
        key += '; Cu → Cu²⁺ + 2e⁻ [1]; Cu²⁺ + 2e⁻ → Cu [1]'
        ans += ' Anode: Cu → Cu²⁺ + 2e⁻; cathode: Cu²⁺ + 2e⁻ → Cu.'
    return Q(stem, ans, key, 'case')


@t6c.add('C2', (2, 3, 4), 'explain')
def t6c_err(r, D):
    obj, met, sym, q, el = r.choice(PLATE)
    errs = [(f'connected the {obj} to the positive terminal', f'The {obj} must be the cathode (negative) so that {ionf(sym, q)} ions gain electrons and deposit on it; as the anode it would be oxidised instead.'),
            (f'used aqueous sodium chloride as the electrolyte', f'The electrolyte must contain {ionf(sym, q)} ions (e.g. {el}); with NaCl, hydrogen would form at the cathode instead of {met}.'),
            ('did not clean the surface of the object before plating', 'Grease or oxide on the surface stops the plating metal sticking evenly; the object should be cleaned first.')]
    s, fix = r.choice(errs)
    return Q(f'{person(r)} tried to electroplate a {obj} with {met} but {s}. Explain why this would not work well and how to correct it.', fix, '1 mark: problem explained; 1 mark: correction [2]')


def _t6c_c4(r, D):
    p = person(r)
    intro = r.choice([f'Copper used for electrical wiring must be very pure. {p} visits a refinery in {city(r)} where impure copper is purified by electrolysis.', f'{p} sets up a cell to purify a bar of impure copper by electrolysis.'])
    loss = r.choice([4.0, 5.0, 8.0, 10.0])
    gain = round(loss * r.choice([0.9, 0.92, 0.95, 0.96]), 2)
    parts = [
        lambda r: ('Name the anode, cathode and electrolyte used.', 'anode: impure copper; cathode: pure copper; electrolyte: aqueous copper(II) sulfate', '1 mark each [3]'),
        lambda r: ('Write the half-equation at the anode.', 'Cu → Cu²⁺ + 2e⁻', '[1]'),
        lambda r: ('Write the half-equation at the cathode.', 'Cu²⁺ + 2e⁻ → Cu', '[1]'),
        lambda r: ('Explain why the colour of the electrolyte does not change.', 'Cu²⁺ ions are added at the anode at the same rate they are removed at the cathode', '[2]'),
        lambda r: ('Describe what happens to the impurities.', 'unreactive metals fall as anode sludge; reactive metals dissolve and stay in solution', '[2]'),
        lambda r: (f'The anode loses {loss:.2f} g and the cathode gains {gain:.2f} g. Calculate the percentage purity of the copper anode.', f'{g3(gain / loss * 100)}%', f'{gain:.2f} ÷ {loss:.2f} × 100 [1]'),
        lambda r: ('Suggest why very pure copper is needed for wiring.', 'impurities reduce electrical conductivity', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t6c.add('C4', (2, 3, 4, 5), 'multi_step')(_t6c_c4)


# ---------------------------------------------------------- 6.4 fuel cells
FC_ADV = ['the only chemical product is water, so no carbon dioxide or other pollutants are released at the point of use', 'fuel cells are more efficient at converting chemical energy to electrical energy',
          'there are fewer moving parts, so less maintenance and quieter running', 'hydrogen can be made from water using renewable electricity']
FC_DIS = ['hydrogen is a gas that is difficult and expensive to store and transport (high pressure tanks)', 'hydrogen is flammable/explosive', 'there are few hydrogen filling stations',
          'most hydrogen is currently made from fossil fuels (e.g. methane), which releases CO₂', 'fuel cells are expensive (they contain costly catalysts such as platinum)']

t6d = T('Hydrogen–oxygen fuel cells: advantages and disadvantages compared with petrol engines', 'fuel cells', 'hydrogen–oxygen fuel cells', 'petrol engines')
t6d.fixed('C1', (1, 2), [
    ('What is the only chemical product of a hydrogen–oxygen fuel cell?', 'water', '2H₂ + O₂ → 2H₂O.', ['carbon dioxide', 'hydrogen peroxide', 'carbon monoxide']),
    ('What does a fuel cell produce directly from chemical energy?', 'electrical energy', 'A fuel cell uses hydrogen and oxygen to produce electricity.', ['heat only', 'light energy', 'nuclear energy']),
    ('Which is an advantage of a hydrogen fuel cell car compared with a petrol car?', 'It produces no carbon dioxide when running.', 'Water is the only product.', ['Hydrogen is easy to store.', 'There are many hydrogen filling stations.', 'Fuel cells are cheap to make.']),
    ('Which is a disadvantage of hydrogen fuel cells?', 'Hydrogen is difficult to store safely.', 'Hydrogen gas needs high-pressure tanks and is flammable.', ['They produce carbon monoxide.', 'They produce nitrogen oxides.', 'They need petrol to start.']),
    ('Write the overall equation for the reaction in a hydrogen–oxygen fuel cell.', '2H₂ + O₂ → 2H₂O', '[1]'),
])
t6d.fixed('C2', (2, 3, 4), [
    ('Explain why hydrogen fuel cell cars are described as "zero emission" but may still contribute to climate change.', 'At the point of use only water is produced; but if the hydrogen is made from fossil fuels (e.g. methane) or the electricity for electrolysis comes from fossil fuels, CO₂ is released during production.', '1 mark: only water in use; 1 mark: CO₂ from hydrogen production [2]'),
    ('Compare the products of combustion in a petrol engine with the products of a hydrogen–oxygen fuel cell.', 'Petrol engine: carbon dioxide, water, and pollutants such as carbon monoxide, nitrogen oxides and particulates; fuel cell: water only.', '[2]'),
    ('Explain why storing hydrogen is a problem for fuel cell vehicles.', 'Hydrogen is a gas with a low density, so it must be stored at very high pressure in heavy, strong tanks; it is also highly flammable.', '[2]'),
    ('Explain why a fuel cell is described as converting chemical energy directly into electrical energy.', 'The redox reaction between hydrogen and oxygen transfers electrons through an external circuit, rather than burning the fuel to produce heat and then motion.', '[2]'),
])


@t6d.add('C1', (1, 2, 3))
def t6d_adv(r, D):
    if r.random() < 0.5:
        c = r.choice(FC_ADV)
        return M(r, 'Which statement is an advantage of hydrogen–oxygen fuel cells compared with petrol engines?', cap(c) + '.', [cap(x) + '.' for x in FC_DIS], 'Advantage: ' + c + '.')
    c = r.choice(FC_DIS)
    return M(r, 'Which statement is a disadvantage of hydrogen–oxygen fuel cells compared with petrol engines?', cap(c) + '.', [cap(x) + '.' for x in FC_ADV], 'Disadvantage: ' + c + '.')


@t6d.add('C3', (2, 3, 4, 5))
def t6d_data(r, D):
    p = person(r)
    rng_f, rng_p = r.choice([480, 500, 550, 600, 650]), r.choice([600, 650, 700, 750, 800])
    t_f, t_p = r.choice([4, 5, 6]), r.choice([3, 4, 5])
    co2_p = r.choice([120, 140, 160, 180])
    cost_f, cost_p = r.choice([55000, 60000, 65000, 70000]), r.choice([25000, 30000, 35000])
    st_f, st_p = r.choice([3, 5, 8, 12]), r.choice([800, 1200, 1500, 2000])
    stem = (f'{p} compares a hydrogen fuel cell car with a petrol car in {city(r)}. Data: range on a full tank – fuel cell {rng_f} km, petrol {rng_p} km; refuelling time – fuel cell {t_f} min, petrol {t_p} min; '
            f'CO₂ emitted while driving – fuel cell 0 g/km, petrol {co2_p} g/km; purchase price – fuel cell ${cost_f:,}, petrol ${cost_p:,}; filling stations in the city – hydrogen {st_f}, petrol {st_p}. '
            'Use the data and your own knowledge to evaluate which car is the better choice.')
    ans = (f'Fuel cell: no CO₂ or other pollutants when driving (only water), but costs ${cost_f - cost_p:,} more, {f"has {rng_p - rng_f} km less range" if rng_p > rng_f else f"although it has {rng_f - rng_p} km more range"} and there are only {st_f} hydrogen filling stations; hydrogen may be made from fossil fuels. '
           'Petrol: cheaper, convenient, but emits CO₂ (climate change) plus CO, NOx and particulates. A justified conclusion either way.')
    key = '1 mark: environmental advantage of fuel cell from data; 1 mark: practical disadvantage from data (cost/range/stations); 1 mark: knowledge – water only product / hydrogen storage or production; 1 mark: petrol pollutants; 1 mark: justified conclusion [5]'
    if D <= 3:
        key = '1 mark: one advantage from the data; 1 mark: one disadvantage from the data; 1 mark: conclusion with reason [3]'
        stem = stem.replace('Use the data and your own knowledge to evaluate which car is the better choice.', 'Give one advantage and one disadvantage of the fuel cell car shown by the data, and state which car you would choose.')
    return Q(stem, ans, key, 'case')


@t6d.add('C2', (2, 3, 4), 'explain')
def t6d_explain(r, D):
    a, d = r.choice(FC_ADV), r.choice(FC_DIS)
    ctx = r.choice([f'A bus company in {city(r)} is considering replacing diesel buses with hydrogen fuel cell buses.', f'{person(r)} is writing a report on hydrogen fuel cell cars.',
                    f'The government of a country is deciding whether to build hydrogen filling stations in {city(r)}.'])
    return Q(f'{ctx} Explain one advantage and one disadvantage of hydrogen fuel cells compared with petrol or diesel engines.', f'Advantage: {a}. Disadvantage: {d}.',
             '1 mark: advantage explained; 1 mark: disadvantage explained [2]' if D <= 3 else '1 mark: advantage; 1 mark: explanation; 1 mark: disadvantage with explanation [3]')


def _t6d_c4(r, D):
    p = person(r)
    intro = r.choice([f'A city council in {city(r)} is replacing petrol vans with hydrogen fuel cell vans.', f'{p} researches hydrogen–oxygen fuel cells for a school project.'])
    parts = [
        lambda r: ('Write the overall equation for the reaction in the fuel cell.', '2H₂ + O₂ → 2H₂O', '[1]'),
        lambda r: ('State the energy change that takes place in a fuel cell.', 'chemical energy → electrical energy', '[1]'),
        lambda r: ('Give two advantages of fuel cell vans compared with petrol vans.', f'{FC_ADV[0]}; {FC_ADV[r.choice([1, 2])]}', '1 mark each [2]'),
        lambda r: ('Give two disadvantages of fuel cell vans.', f'{FC_DIS[0]}; {FC_DIS[r.choice([2, 3, 4])]}', '1 mark each [2]'),
        lambda r: ('Name two pollutants produced by petrol engines that are not produced by fuel cells.', 'carbon dioxide; carbon monoxide (also oxides of nitrogen, particulates)', '1 mark each [2]'),
        lambda r: ('Suggest why fuel cell vans are only truly low-carbon if the hydrogen is made using renewable electricity.', 'otherwise CO₂ is released when the hydrogen is produced (from methane or fossil-fuel electricity)', '[2]'),
        lambda r: ('Evaluate whether the council has made a good decision.', 'balanced judgement: cleaner air and lower CO₂ vs cost, storage, refuelling infrastructure, source of hydrogen', '1 mark each side; 1 mark conclusion [3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='long')


t6d.add('C4', (2, 3, 4, 5), 'long')(_t6d_c4)

CHAPTERS[6] = [t6a, t6b, t6c, t6d]


# ===================================================================== Ch7 Chemical energetics
EXO = ['magnesium ribbon is added to dilute hydrochloric acid', 'sodium hydroxide solution is added to dilute hydrochloric acid', 'methane burns in a Bunsen burner',
       'calcium oxide is added to water', 'zinc powder is added to copper(II) sulfate solution', 'iron powder in a hand warmer reacts with oxygen', 'sodium reacts with water',
       'potassium hydroxide solution is added to dilute nitric acid', 'ethanol burns in a spirit burner', 'anhydrous copper(II) sulfate is added to water']
ENDO = ['ammonium nitrate dissolves in water', 'citric acid is mixed with sodium hydrogencarbonate solution', 'calcium carbonate is heated strongly and decomposes',
        'potassium chloride dissolves in water', 'ethanoic acid reacts with sodium hydrogencarbonate', 'ammonium chloride dissolves in water', 'hydrated copper(II) sulfate is heated and turns white',
        'water is electrolysed into hydrogen and oxygen', 'photosynthesis takes place in a leaf']

t7a = T('Exothermic and endothermic reactions and temperature change', 'exothermic and endothermic reactions', 'temperature change')
t7a.fixed('C1', (1, 2), [
    ('What is an exothermic reaction?', 'a reaction that transfers thermal energy to the surroundings', 'Exothermic: energy released; surroundings get hotter.', ['a reaction that takes in thermal energy from the surroundings', 'a reaction that needs a catalyst', 'a reaction that only happens when heated']),
    ('Which observation shows that a reaction in a test tube is endothermic?', 'The test tube feels cold.', 'Energy is taken in from the surroundings.', ['The mixture fizzes.', 'A precipitate forms.', 'The test tube feels hot.']),
    ('Which process is endothermic?', 'thermal decomposition of calcium carbonate', 'Decomposition needs continuous heating.', ['combustion of methane', 'neutralisation', 'respiration']),
    ('Which type of reaction is used in self-heating cans of food?', 'exothermic', 'Heat is released to warm the food.', ['endothermic', 'reversible', 'thermal decomposition']),
    ('State the sign of the enthalpy change, ΔH, for an endothermic reaction.', 'positive (+)', '[1]'),
    ('State what is meant by an endothermic reaction.', 'A reaction that takes in thermal energy from the surroundings, so the temperature of the surroundings decreases.', '[1]'),
])
t7a.fixed('C2', (2, 3, 4), [
    ('Explain why the temperature of the mixture falls when ammonium nitrate dissolves in water.', 'The process is endothermic: thermal energy is taken in from the water (surroundings), so the temperature falls.', '[2]'),
    ('Explain why a polystyrene cup with a lid is used when measuring temperature changes of reactions in solution.', 'Polystyrene is an insulator and the lid reduces heat loss/gain to the surroundings, so the measured temperature change is more accurate.', '1 mark: insulation; 1 mark: reduces energy transfer → more accurate [2]'),
    ('Explain why the temperature change measured in a simple experiment is usually smaller than the true value for an exothermic reaction.', 'Some heat is lost to the surroundings (air, container, thermometer) instead of raising the temperature of the solution.', '[2]'),
    ('A student says, "Endothermic reactions make things cold, so they release cold." Explain the error.', 'Endothermic reactions take in thermal energy from the surroundings; the surroundings lose energy and their temperature falls. "Cold" is not released.', '[2]'),
    ('Explain why cold packs used for sports injuries contain substances that dissolve endothermically.', 'When the substance dissolves it takes in thermal energy from the surroundings (the injury), cooling it.', '[2]'),
])


@t7a.add('C1', (1, 2, 3))
def t7a_class(r, D):
    if r.random() < 0.5:
        x, kind = r.choice(EXO), 'exothermic'
    else:
        x, kind = r.choice(ENDO), 'endothermic'
    if D <= 2:
        return M(r, f'When {x}, which statement is correct?', f'The reaction is {kind} and the temperature of the surroundings {"rises" if kind == "exothermic" else "falls"}.',
                 [f'The reaction is {"endothermic" if kind == "exothermic" else "exothermic"} and the temperature of the surroundings {"rises" if kind == "exothermic" else "falls"}.',
                  f'The reaction is {kind} and the temperature of the surroundings {"falls" if kind == "exothermic" else "rises"}.',
                  f'The reaction is {"endothermic" if kind == "exothermic" else "exothermic"} and the temperature of the surroundings {"falls" if kind == "exothermic" else "rises"}.'],
                 f'{cap(kind)}: energy {"released to" if kind == "exothermic" else "taken in from"} the surroundings.')
    return M(r, f'When {x}, what is the sign of ΔH and what happens to the temperature of the surroundings?', f'ΔH {"negative" if kind == "exothermic" else "positive"}; temperature {"rises" if kind == "exothermic" else "falls"}',
             ['ΔH negative; temperature rises', 'ΔH negative; temperature falls', 'ΔH positive; temperature rises', 'ΔH positive; temperature falls'], f'{cap(kind)} reaction.')


@t7a.add('C3', (1, 2, 3, 4))
def t7a_table(r, D):
    k = 3 if D <= 2 else 4
    rx = r.sample([(x, 'exo') for x in EXO] + [(x, 'endo') for x in ENDO], k)
    rows = []
    out = []
    for i, (x, kind) in enumerate(rx):
        t1 = r.choice(range(17, 25))
        dt = r.choice(range(3, 30)) * (1 if kind == 'exo' else -1)
        if kind == 'endo':
            dt = max(dt, -12)
        rows.append(f'experiment {i + 1}: {x}; start {t1} °C, end {t1 + dt} °C')
        out.append((i + 1, kind, dt))
    big = max(out, key=lambda o: abs(o[2]))
    if D == 1:
        o = r.choice(out)
        return M(r, f'{rows[o[0] - 1].capitalize()}. What is the temperature change and what type of reaction is it?', f'{"+" if o[2] > 0 else "−"}{abs(o[2])} °C; {"exothermic" if o[1] == "exo" else "endothermic"}',
                 [f'{"+" if o[2] > 0 else "−"}{abs(o[2])} °C; {"endothermic" if o[1] == "exo" else "exothermic"}', f'{"−" if o[2] > 0 else "+"}{abs(o[2])} °C; {"exothermic" if o[1] == "exo" else "endothermic"}',
                  f'{"−" if o[2] > 0 else "+"}{abs(o[2])} °C; {"endothermic" if o[1] == "exo" else "exothermic"}'], 'ΔT = end − start; rise → exothermic, fall → endothermic.')
    stem = 'Results: ' + '; '.join(rows) + '. Calculate the temperature change in each experiment, classify each reaction as exothermic or endothermic, and identify the experiment with the largest energy change.'
    ans = '; '.join(f'{i}: {"+" if dt > 0 else "−"}{abs(dt)} °C, {"exothermic" if kind == "exo" else "endothermic"}' for i, kind, dt in out) + f'; largest change: experiment {big[0]}'
    return Q(stem, ans, f'{ans}. 1 mark per experiment (change and classification) [{k}]; largest [1]', 'case')


@t7a.add('C3', (3, 4, 5))
def t7a_thermo(r, D):
    alk, acid = r.choice([('sodium hydroxide', 'hydrochloric acid'), ('potassium hydroxide', 'nitric acid'), ('sodium hydroxide', 'nitric acid'), ('potassium hydroxide', 'hydrochloric acid')])
    Valk = 25.0
    calk = r.choice([1.0, 2.0, 0.5, 1.5])
    cacid = r.choice([1.0, 2.0, 1.5, 0.5])
    Veq = Valk * calk / cacid
    if not (10 <= Veq <= 50) or Veq % 5:
        return None
    t0 = r.choice(range(18, 24))
    rise = r.choice(range(6, 14))
    vols = list(range(0, int(Veq) + 20, 5))
    temps = []
    for v in vols:
        if v <= Veq:
            temps.append(round(t0 + rise * v / Veq, 1))
        else:
            temps.append(round(t0 + rise - (v - Veq) * rise / (Veq + 25) * 0.6, 1))
    rows = ', '.join(f'{v} cm³: {t:.1f} °C' for v, t in zip(vols, temps))
    p = person(r)
    stem = f'{p} adds {acid} in 5 cm³ portions to {sf(Valk, 3)} cm³ of {sf(calk)} mol/dm³ {alk} in a polystyrene cup and records the temperature: {rows}. Describe and explain the shape of the results. State the volume of acid needed to neutralise the alkali and use it to calculate the concentration of the acid.'
    ans = f'Temperature rises (exothermic neutralisation) until {sf(Veq)} cm³, then falls as excess cold acid is added and heat is lost. Neutralisation at {sf(Veq)} cm³; acid concentration = {g3(cacid)} mol/dm³.'
    key = f'1 mark: rise – exothermic neutralisation; 1 mark: fall after end-point – no more reaction, cooler acid added; 1 mark: {sf(Veq)} cm³; 1 mark: n(alkali) = {g3(calk * Valk / 1000)} mol; c = {g3(calk * Valk / 1000)} ÷ {sf(Veq / 1000)} = {g3(cacid)} mol/dm³ [4]'
    return Q(stem, ans, key, 'case')


@t7a.add('C2', (2, 3, 4), 'explain')
def t7a_explain(r, D):
    if r.random() < 0.5:
        x, kind = r.choice(EXO), 'exothermic'
    else:
        x, kind = r.choice(ENDO), 'endothermic'
    return Q(f'When {x}, the temperature of the mixture {"rises" if kind == "exothermic" else "falls"}. Explain this observation in terms of energy transfer and state the sign of ΔH.',
             f'The reaction is {kind}: thermal energy is {"transferred to" if kind == "exothermic" else "taken in from"} the surroundings, so their temperature {"rises" if kind == "exothermic" else "falls"}. ΔH is {"negative" if kind == "exothermic" else "positive"}.',
             '1 mark: classification; 1 mark: direction of energy transfer; ' + ('1 mark: sign of ΔH [3]' if D >= 3 else 'total [2]'))


def _t7a_c4(r, D):
    x1 = r.choice(EXO)
    x2 = r.choice(ENDO)
    t1 = r.choice(range(18, 24))
    d1, d2 = r.choice(range(5, 25)), r.choice(range(3, 10))
    p = person(r)
    intro = f'{p} investigates two reactions in polystyrene cups. Reaction A: {x1}; the temperature changes from {t1} °C to {t1 + d1} °C. Reaction B: {x2}; the temperature changes from {t1} °C to {t1 - d2} °C.'
    parts = [
        lambda r: ('Calculate the temperature change for each reaction.', f'A: +{d1} °C; B: −{d2} °C', '1 mark each [2]'),
        lambda r: ('Classify each reaction as exothermic or endothermic, giving a reason.', 'A exothermic (temperature rises); B endothermic (temperature falls)', '1 mark each [2]'),
        lambda r: ('State the sign of ΔH for each reaction.', 'A negative; B positive', '[1]'),
        lambda r: ('Explain why a polystyrene cup is used rather than a glass beaker.', 'polystyrene is a better insulator, reducing heat transfer with the surroundings', '[1]'),
        lambda r: ('Suggest two ways to make the results more accurate.', 'use a lid; stir; use a more precise thermometer / data logger; repeat and average', '1 mark each [2]'),
        lambda r: ('Suggest a practical use for reaction A and for reaction B.', 'A: hand warmer / self-heating can; B: cold pack', '1 mark each [2]'),
        lambda r: ('Explain why the final temperature of reaction A eventually returns to room temperature.', 'once the reaction stops, heat is lost to the surroundings', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


t7a.add('C4', (2, 3, 4, 5), 'case')(_t7a_c4)


# ---------------------------------------------------------- 7.2 reaction pathway diagrams
PATH_RX = ['the combustion of methane', 'the reaction of hydrogen with chlorine', 'the decomposition of hydrogen peroxide', 'the thermal decomposition of calcium carbonate',
           'the formation of ammonia from nitrogen and hydrogen', 'the reaction of zinc with copper(II) sulfate', 'the decomposition of hydrogen iodide', 'the reaction of nitrogen with oxygen',
           'reaction X', 'reaction Y', 'the hydration of ethene', 'the oxidation of sulfur dioxide']

t7b = T('Reaction pathway diagrams, enthalpy change and activation energy', 'reaction pathway diagrams', 'enthalpy change', 'activation energy')
t7b.fixed('C1', (1, 2), [
    ('What is activation energy, Ea?', 'the minimum energy that colliding particles must have to react', 'Ea: minimum energy needed for a successful collision.', ['the energy released by a reaction', 'the total energy of the products', 'the energy of the catalyst']),
    ('On a reaction pathway diagram for an exothermic reaction, where are the products?', 'below the reactants', 'Energy is released, so products have less energy.', ['above the reactants', 'at the same level as the reactants', 'at the top of the curve']),
    ('What is the effect of a catalyst on a reaction pathway diagram?', 'It lowers the peak (activation energy) but does not change ΔH.', 'Alternative pathway with lower Ea.', ['It lowers the energy of the products.', 'It increases ΔH.', 'It raises the energy of the reactants.']),
    ('What does ΔH represent on a reaction pathway diagram?', 'the difference in energy between products and reactants', 'ΔH = energy of products − energy of reactants.', ['the height of the peak above the reactants', 'the energy of the products only', 'the height of the peak above the products']),
    ('State the meaning of the symbol ΔH.', 'enthalpy change (energy transferred) of a reaction', '[1]'),
])
t7b.fixed('C2', (2, 3, 4), [
    ('Explain why a reaction with a negative ΔH can still need heating to start it.', 'The particles still need enough energy to overcome the activation energy before bonds break; once started, the energy released keeps the reaction going.', '[2]'),
    ('Describe how a reaction pathway diagram for an endothermic reaction differs from one for an exothermic reaction.', 'Endothermic: products are higher in energy than reactants (ΔH positive); exothermic: products lower (ΔH negative). Both show a hump for activation energy.', '[2]'),
    ('Explain how a catalyst increases the rate of a reaction, using a reaction pathway diagram.', 'It provides an alternative pathway with a lower activation energy (lower peak), so a greater proportion of collisions have enough energy to react.', '[2]'),
    ('A student says that a catalyst makes a reaction more exothermic. Explain the error.', 'A catalyst lowers the activation energy only; the energies of the reactants and products, and so ΔH, are unchanged.', '[2]'),
])


def _levels(r, D):
    R_ = r.choice(range(50, 400, 10))
    dH = r.choice([-1, 1]) * r.choice(range(20, 300, 5))
    P_ = R_ + dH
    if P_ < 0:
        P_ = R_ - dH
        dH = -dH
    Ea = r.choice(range(40, 300, 5)) + max(0, dH)
    return R_, P_, R_ + Ea, dH, Ea


@t7b.add('C3', (1, 2, 3, 4))
def t7b_calc(r, D):
    R_, P_, Tp, dH, Ea = _levels(r, D)
    rx = r.choice(PATH_RX)
    stem = f'On a reaction pathway diagram for {rx}, the reactants are at {R_} kJ/mol, the products at {P_} kJ/mol and the top of the energy hump at {Tp} kJ/mol.'
    if D == 1:
        what = r.choice(['ΔH', 'Ea'])
        v = dH if what == 'ΔH' else Ea
        wrong = [-dH, Tp - P_, Ea + dH, P_, Tp] if what == 'ΔH' else [Tp - P_, Tp, dH, Ea + abs(dH)]
        return NM(r, stem + f' What is the value of {"the enthalpy change, ΔH" if what == "ΔH" else "the activation energy, Ea"}?', v, wrong, ' kJ/mol',
                  f'ΔH = {P_} − {R_} = {dH:+d} kJ/mol; Ea = {Tp} − {R_} = {Ea} kJ/mol', f=lambda x: neg(f'{x:+.0f}') if what == 'ΔH' else str(int(x)))
    stem += ' Calculate the enthalpy change, ΔH, and the activation energy, Ea, and state whether the reaction is exothermic or endothermic.'
    ans = neg(f'ΔH = {dH:+d} kJ/mol; Ea = {Ea} kJ/mol; {"exothermic" if dH < 0 else "endothermic"}')
    key = neg(f'ΔH = {P_} − {R_} = {dH:+d} kJ/mol [1]; Ea = {Tp} − {R_} = {Ea} kJ/mol [1]; {"exothermic" if dH < 0 else "endothermic"} [1]')
    if D >= 4:
        cat = r.choice(range(20, Ea - 10, 5))
        stem += f' A catalyst lowers the top of the hump to {Tp - cat} kJ/mol. Calculate the new activation energy and state the effect on ΔH.'
        ans += f'; catalysed Ea = {Ea - cat} kJ/mol; ΔH unchanged'
        key += f'; new Ea = {Tp - cat} − {R_} = {Ea - cat} kJ/mol [1]; ΔH unchanged [1]'
    return Q(stem, ans, key, 'numerical')


@t7b.add('C2', (2, 3, 4), 'explain')
def t7b_describe(r, D):
    R_, P_, Tp, dH, Ea = _levels(r, D)
    rx = r.choice(PATH_RX)
    kind = 'exothermic' if dH < 0 else 'endothermic'
    return Q(neg(f'{cap(rx)} has ΔH = {dH:+d} kJ/mol and an activation energy of {Ea} kJ/mol. Describe the reaction pathway diagram for this reaction, labelling ΔH and Ea, and explain what the diagram shows about the energy change.'),
             f'Products drawn {"below" if dH < 0 else "above"} reactants; a hump between them; Ea arrow from reactants up to the peak ({Ea} kJ/mol); ΔH arrow from reactants to products ({abs(dH)} kJ/mol {"down" if dH < 0 else "up"}). The reaction is {kind}: energy is {"released to" if dH < 0 else "taken in from"} the surroundings.',
             '1 mark: products correctly placed; 1 mark: Ea shown from reactants to peak; 1 mark: ΔH shown between reactants and products; ' + ('1 mark: exo/endo explanation [4]' if D >= 4 else 'total [3]'))


@t7b.add('C1', (1, 2, 3))
def t7b_which(r, D):
    R_, P_, Tp, dH, Ea = _levels(r, D)
    corr = 'exothermic' if dH < 0 else 'endothermic'
    return M(r, f'In a reaction pathway diagram the reactants are at {R_} kJ/mol and the products at {P_} kJ/mol. Which statement is correct?',
             f'The reaction is {corr} and ΔH is {"negative" if dH < 0 else "positive"}.', ['The reaction is exothermic and ΔH is positive.', 'The reaction is endothermic and ΔH is negative.',
                                                                                        f'The reaction is {"endothermic" if dH < 0 else "exothermic"} and ΔH is {"positive" if dH < 0 else "negative"}.', 'The reaction has no activation energy.'],
             neg(f'ΔH = {P_} − {R_} = {dH:+d} kJ/mol.'))


def _t7b_c4(r, D):
    R_, P_, Tp, dH, Ea = _levels(r, D)
    rx = r.choice(PATH_RX)
    cat = r.choice(range(20, max(25, Ea - 10), 5))
    p = person(r)
    intro = f'{p} studies {rx}. The reactants have an energy of {R_} kJ/mol, the products {P_} kJ/mol and the transition state (top of the hump) {Tp} kJ/mol.'
    parts = [
        lambda r: ('Calculate ΔH for the reaction.', neg(f'{dH:+d} kJ/mol'), f'{P_} − {R_} [1]'),
        lambda r: ('Calculate the activation energy.', f'{Ea} kJ/mol', f'{Tp} − {R_} [1]'),
        lambda r: ('State and explain whether the reaction is exothermic or endothermic.', 'exothermic: products lower than reactants, energy released' if dH < 0 else 'endothermic: products higher than reactants, energy absorbed', '[2]'),
        lambda r: (f'A catalyst reduces the activation energy by {cat} kJ/mol. Describe the change to the diagram.', f'peak lower by {cat} kJ/mol (at {Tp - cat} kJ/mol); reactant and product levels unchanged', '[2]'),
        lambda r: ('Explain why the catalyst increases the rate of reaction.', 'lower Ea, so a greater proportion of colliding particles have energy ≥ Ea; more successful collisions per second', '[2]'),
        lambda r: ('Calculate the activation energy of the reverse reaction.', f'{Tp - P_} kJ/mol', f'{Tp} − {P_} [1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t7b.add('C4', (2, 3, 4, 5), 'multi_step')(_t7b_c4)


# ---------------------------------------------------------- 7.3 bond energies
BE_SETS = [{'H–H': 436, 'Cl–Cl': 242, 'H–Cl': 431, 'Br–Br': 193, 'H–Br': 366, 'I–I': 151, 'H–I': 299, 'F–F': 158, 'H–F': 568, 'O=O': 498, 'O–H': 464, 'C–H': 413, 'C=O': 805, 'C–C': 347,
            'C=C': 612, 'N≡N': 945, 'N–H': 391, 'C–Cl': 346, 'C–Br': 290, 'C–O': 358},
           {'H–H': 436, 'Cl–Cl': 243, 'H–Cl': 432, 'Br–Br': 193, 'H–Br': 366, 'I–I': 151, 'H–I': 298, 'F–F': 158, 'H–F': 562, 'O=O': 496, 'O–H': 463, 'C–H': 412, 'C=O': 743, 'C–C': 348,
            'C=C': 612, 'N≡N': 944, 'N–H': 388, 'C–Cl': 338, 'C–Br': 276, 'C–O': 360},
           {'H–H': 435, 'Cl–Cl': 242, 'H–Cl': 431, 'Br–Br': 192, 'H–Br': 366, 'I–I': 151, 'H–I': 299, 'F–F': 158, 'H–F': 565, 'O=O': 497, 'O–H': 460, 'C–H': 410, 'C=O': 805, 'C–C': 346,
            'C=C': 614, 'N≡N': 941, 'N–H': 390, 'C–Cl': 339, 'C–Br': 285, 'C–O': 358}]
BE_RX = [  # equation, bonds broken, bonds made
    ('H2 + Cl2 -> 2HCl', {'H–H': 1, 'Cl–Cl': 1}, {'H–Cl': 2}), ('H2 + Br2 -> 2HBr', {'H–H': 1, 'Br–Br': 1}, {'H–Br': 2}), ('H2 + I2 -> 2HI', {'H–H': 1, 'I–I': 1}, {'H–I': 2}),
    ('H2 + F2 -> 2HF', {'H–H': 1, 'F–F': 1}, {'H–F': 2}), ('2H2 + O2 -> 2H2O', {'H–H': 2, 'O=O': 1}, {'O–H': 4}),
    ('CH4 + 2O2 -> CO2 + 2H2O', {'C–H': 4, 'O=O': 2}, {'C=O': 2, 'O–H': 4}), ('N2 + 3H2 -> 2NH3', {'N≡N': 1, 'H–H': 3}, {'N–H': 6}),
    ('C2H4 + H2 -> C2H6', {'C=C': 1, 'C–H': 4, 'H–H': 1}, {'C–C': 1, 'C–H': 6}), ('C2H4 + Br2 -> C2H4Br2', {'C=C': 1, 'C–H': 4, 'Br–Br': 1}, {'C–C': 1, 'C–H': 4, 'C–Br': 2}),
    ('CH4 + Cl2 -> CH3Cl + HCl', {'C–H': 4, 'Cl–Cl': 1}, {'C–H': 3, 'C–Cl': 1, 'H–Cl': 1}), ('2C2H6 + 7O2 -> 4CO2 + 6H2O', {'C–C': 2, 'C–H': 12, 'O=O': 7}, {'C=O': 8, 'O–H': 12}),
    ('C2H4 + 3O2 -> 2CO2 + 2H2O', {'C=C': 1, 'C–H': 4, 'O=O': 3}, {'C=O': 4, 'O–H': 4}), ('C3H8 + 5O2 -> 3CO2 + 4H2O', {'C–C': 2, 'C–H': 8, 'O=O': 5}, {'C=O': 6, 'O–H': 8}),
    ('C2H4 + H2O -> C2H5OH', {'C=C': 1, 'C–H': 4, 'O–H': 2}, {'C–C': 1, 'C–H': 5, 'C–O': 1, 'O–H': 1}),
    ('2CH3OH + 3O2 -> 2CO2 + 4H2O', {'C–H': 6, 'C–O': 2, 'O–H': 2, 'O=O': 3}, {'C=O': 4, 'O–H': 8}), ('2HI -> H2 + I2', {'H–I': 2}, {'H–H': 1, 'I–I': 1}),
    ('2NH3 -> N2 + 3H2', {'N–H': 6}, {'N≡N': 1, 'H–H': 3}), ('2HCl -> H2 + Cl2', {'H–Cl': 2}, {'H–H': 1, 'Cl–Cl': 1}), ('2H2O -> 2H2 + O2', {'O–H': 4}, {'H–H': 2, 'O=O': 1}),
    ('C2H6 + Cl2 -> C2H5Cl + HCl', {'C–H': 6, 'C–C': 1, 'Cl–Cl': 1}, {'C–H': 5, 'C–C': 1, 'C–Cl': 1, 'H–Cl': 1}),
]
for _e, _b, _m in BE_RX:
    _L, _R = parse_eq(_e)
    _bond_atoms = lambda d: sum(n for n in d.values())
    assert balanced(_e), _e


def be_sum(d, BE):
    return sum(BE[k] * n for k, n in d.items())


def be_work(d, BE):
    return ' + '.join(f'{n} × {BE[k]}' if n > 1 else f'{BE[k]}' for k, n in d.items())


t7c = T('Bond breaking, bond making and calculating enthalpy change from bond energies', 'bond energies', 'bond breaking, bond making')
t7c.fixed('C1', (1, 2), [
    ('Which statement about bond breaking and bond making is correct?', 'Bond breaking is endothermic and bond making is exothermic.', 'Energy is needed to break bonds and released when bonds form.',
     ['Bond breaking is exothermic and bond making is endothermic.', 'Both are exothermic.', 'Both are endothermic.']),
    ('A reaction is exothermic. What does this show about the bonds?', 'More energy is released making new bonds than is taken in breaking bonds.', 'ΔH = energy in − energy out < 0.', ['More energy is taken in breaking bonds than is released making bonds.', 'No bonds are broken.', 'The bonds in the products are weaker.']),
    ('What is the unit of bond energy?', 'kJ/mol', 'Bond energy: energy to break one mole of bonds.', ['kJ', 'J/g', 'mol/kJ']),
    ('State the equation used to calculate ΔH from bond energies.', 'ΔH = total energy of bonds broken − total energy of bonds made', '[1]'),
    ('State what is meant by bond energy.', 'the energy needed to break one mole of a particular covalent bond (in the gas state)', '[1]'),
])
t7c.fixed('C2', (2, 3, 4), [
    ('Explain, in terms of bonds, why the combustion of methane is exothermic.', 'The energy released when the C=O and O–H bonds in CO₂ and H₂O are made is greater than the energy needed to break the C–H and O=O bonds.', '[2]'),
    ('Explain why bond breaking is endothermic.', 'Energy must be supplied to overcome the attraction between the shared electrons and the nuclei that holds the atoms together.', '[2]'),
    ('Explain why ΔH values calculated from bond energies often differ from values measured by experiment.', 'Bond energies are average values from many compounds; the actual bond strength depends on the molecule, and measurements may involve substances not in the gas state.', '[2]'),
    ('A student calculates ΔH as (bonds made − bonds broken). Explain why this gives the wrong sign.', 'ΔH = energy taken in (bonds broken) − energy given out (bonds made); reversing the subtraction reverses the sign.', '[2]'),
])


@t7c.add('C3', (2, 3, 4, 5))
def t7c_calc(r, D):
    e, br, mk = r.choice(BE_RX)
    BE = r.choice(BE_SETS)
    needed = sorted(set(br) | set(mk))
    data = ', '.join(f'{k} {BE[k]}' for k in needed)
    inn, out = be_sum(br, BE), be_sum(mk, BE)
    dH = inn - out
    p = person(r)
    stem = r.choice([f'Use the bond energies (kJ/mol) {data} to calculate the enthalpy change for the reaction {E(e)}.',
                     f'{p} uses these bond energies, in kJ/mol: {data}. Calculate ΔH for the reaction {E(e)}.',
                     f'The reaction {E(e)} takes place in the gas phase. Bond energies in kJ/mol: {data}. Calculate the energy change of the reaction.'])
    key = f'bonds broken: {be_work(br, BE)} = {inn} kJ [1]; bonds made: {be_work(mk, BE)} = {out} kJ [1]; ΔH = {inn} − {out} = {neg(f"{dH:+d}")} kJ/mol [1]'
    ans = neg(f'{dH:+d} kJ/mol')
    if D >= 4:
        stem += ' State whether the reaction is exothermic or endothermic and explain your answer in terms of bond breaking and bond making.'
        ans += f' ({"exothermic" if dH < 0 else "endothermic"})'
        key += f'; {"exothermic: more energy released making bonds than taken in breaking" if dH < 0 else "endothermic: more energy taken in breaking bonds than released making"} [1]'
    if D == 2:
        return NM(r, stem, dH, [-dH, inn + out, inn, -out, dH + 100], ' kJ/mol', key, f=lambda x: neg(f'{x:+.0f}'))
    return Q(stem, ans, key, 'numerical')


@t7c.add('C3', (3, 4, 5))
def t7c_unknown(r, D):
    e, br, mk = r.choice(BE_RX)
    BE = r.choice(BE_SETS)
    allk = sorted(set(br) | set(mk))
    hide = r.choice([k for k in allk if (br.get(k, 0) != mk.get(k, 0))])
    dH = be_sum(br, BE) - be_sum(mk, BE)
    data = ', '.join(f'{k} {BE[k]}' for k in allk if k != hide)
    nb, nm_ = br.get(hide, 0), mk.get(hide, 0)
    net = nb - nm_
    rest = be_sum({k: v for k, v in br.items() if k != hide}, BE) - be_sum({k: v for k, v in mk.items() if k != hide}, BE)
    stem = neg(f'For the reaction {E(e)}, ΔH = {dH:+d} kJ/mol. Using the bond energies (kJ/mol) {data}, calculate the bond energy of the {hide} bond.')
    return Q(stem, f'{BE[hide]} kJ/mol', neg(f'ΔH = broken − made [1]; {dH:+d} = {rest:+d} + ({net:+d} × x) [1]; x = {BE[hide]} kJ/mol [1]'), 'numerical')


@t7c.add('C2', (2, 3, 4), 'explain')
def t7c_list(r, D):
    e, br, mk = r.choice(BE_RX)
    return Q(f'For the reaction {E(e)}, list the bonds broken and the bonds made, and explain how these determine whether the reaction is exothermic or endothermic.',
             f'Broken: {", ".join(f"{n} × {k}" for k, n in br.items())}. Made: {", ".join(f"{n} × {k}" for k, n in mk.items())}. If more energy is released making bonds than is taken in breaking them, the reaction is exothermic; otherwise endothermic.',
             '1 mark: bonds broken; 1 mark: bonds made; 1 mark: comparison rule [3]')


def _t7c_c4(r, D):
    e, br, mk = r.choice(BE_RX)
    BE = r.choice(BE_SETS)
    needed = sorted(set(br) | set(mk))
    inn, out = be_sum(br, BE), be_sum(mk, BE)
    dH = inn - out
    p = person(r)
    intro = r.choice([f'{p} uses bond energies to study the reaction {E(e)}.', f'Engineers in {city(r)} assess the energy change of the reaction {E(e)}.'])
    intro += ' Bond energies (kJ/mol): ' + ', '.join(f'{k} {BE[k]}' for k in needed) + '.'
    parts = [
        lambda r: ('Calculate the energy needed to break the bonds in the reactants.', f'{inn} kJ', be_work(br, BE) + ' [1]'),
        lambda r: ('Calculate the energy released when the bonds in the products are made.', f'{out} kJ', be_work(mk, BE) + ' [1]'),
        lambda r: ('Calculate ΔH for the reaction.', neg(f'{dH:+d} kJ/mol'), f'{inn} − {out} [1]'),
        lambda r: ('State whether the reaction is exothermic or endothermic and explain why.', ('exothermic: more energy released forming bonds than needed to break bonds' if dH < 0 else 'endothermic: more energy needed to break bonds than released making them'), '[2]'),
        lambda r: ('Describe the reaction pathway diagram for this reaction.', f'products {"below" if dH < 0 else "above"} reactants by {abs(dH)} kJ/mol with an activation energy hump', '[2]'),
        lambda r: ('Suggest why the experimental value of ΔH may differ from your answer.', 'bond energies are averages; not all substances in gas state; heat losses in experiments', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t7c.add('C4', (2, 3, 4, 5), 'multi_step')(_t7c_c4)
t7c.add('C3', (4, 5), 'multi_step')(_t7c_c4)

CHAPTERS[7] = [t7a, t7b, t7c]


# ===================================================================== Ch8 Chemical reactions (rates)
PHYS = ['ice melting', 'sugar dissolving in water', 'water boiling', 'iodine subliming when warmed', 'steam condensing on a window', 'wax melting', 'copper(II) sulfate crystals being ground into a powder',
        'ethanol evaporating', 'water freezing', 'a copper wire being bent', 'salt being separated from sea water by evaporation', 'sand being filtered from water', 'ink being separated by chromatography']
CHEM = ['magnesium burning in air', 'iron rusting', 'bread being baked', 'an egg being fried', 'magnesium reacting with acid', 'copper(II) carbonate turning black when heated', 'milk going sour',
        'glucose being fermented to ethanol', 'wood burning', 'an acid being neutralised by an alkali', 'silver tarnishing', 'water being electrolysed', 'a match burning']
CHEM_SIGNS = ['a new substance is formed', 'a gas is given off (not by boiling)', 'a permanent colour change', 'an energy change (heat or light) that is not just a change of state', 'the change is usually difficult to reverse']

t8a = T('Physical and chemical changes', 'physical and chemical changes')
t8a.fixed('C1', (1, 2), [
    ('Which is a chemical change?', 'magnesium burning in air', 'A new substance (magnesium oxide) forms.', ['ice melting', 'salt dissolving in water', 'water boiling']),
    ('Which is a physical change?', 'water freezing', 'No new substance; only the state changes.', ['iron rusting', 'wood burning', 'milk going sour']),
    ('Which statement describes a physical change?', 'No new substance is formed and the change is easily reversed.', 'Physical: same substance, easily reversible.', ['A new substance is formed.', 'A precipitate forms from two solutions.', 'A gas is produced by a reaction.']),
    ('Which observation is a sign of a chemical change?', 'Bubbles of gas form when two solutions are mixed.', 'Gas evolution from a reaction indicates a new substance.', ['A solid melts.', 'A liquid evaporates.', 'Sugar disappears when stirred into water.']),
    ('State one difference between a physical change and a chemical change.', 'In a chemical change a new substance is formed; in a physical change no new substance forms.', '[1]'),
])
t8a.fixed('C2', (2, 3, 4), [
    ('Explain why dissolving salt in water is a physical change.', 'No new substance is formed; the salt can be recovered unchanged by evaporating the water.', '[2]'),
    ('Explain why heating hydrated copper(II) sulfate is a chemical change even though it can be reversed by adding water.', 'A new substance (anhydrous copper(II) sulfate, white) and water are formed; chemical bonds to the water of crystallisation are broken, and there is an energy change.', '[2]'),
    ('A student says that boiling water is a chemical change because a gas is formed. Explain why this is incorrect.', 'The gas is steam, which is still water (H₂O); only the state changes, so it is a physical change.', '[2]'),
    ('Explain why the total mass stays the same in both physical and chemical changes in a closed container.', 'Atoms are not created or destroyed; they are only rearranged (chemical) or move apart/closer (physical).', '[2]'),
])


@t8a.add('C1', (1, 2, 3))
def t8a_which(r, D):
    want = r.choice(['physical', 'chemical'])
    c = r.choice(PHYS if want == 'physical' else CHEM)
    pool = r.sample(CHEM if want == 'physical' else PHYS, 5)
    return M(r, f'Which of these is a {want} change?', c, pool, f'{cap(c)}: ' + ('no new substance forms.' if want == 'physical' else 'a new substance forms.'))


@t8a.add('C3', (1, 2, 3, 4))
def t8a_sort(r, D):
    k = 4 if D <= 2 else 6
    items = [(x, 'physical') for x in r.sample(PHYS, k // 2)] + [(x, 'chemical') for x in r.sample(CHEM, k - k // 2)]
    r.shuffle(items)
    stem = 'Classify each change as physical or chemical: ' + '; '.join(x for x, _ in items) + '.'
    ans = '; '.join(f'{x}: {c}' for x, c in items)
    if D >= 4:
        stem += ' For one of the chemical changes, give one observation that shows a new substance has formed.'
        ans += '. Observation, e.g. ' + r.choice(CHEM_SIGNS) + '.'
        return Q(stem, ans, f'{ans}. 1 mark per two correct [3]; observation [1]', 'short')
    return Q(stem, ans, f'{ans}. 1 mark per two correct [{k // 2}]', 'short')


@t8a.add('C2', (2, 3, 4), 'explain')
def t8a_why(r, D):
    if r.random() < 0.5:
        c, kind = r.choice(PHYS), 'physical'
        why = 'no new substance is formed; the change can be reversed easily (e.g. by cooling, heating or evaporating)'
    else:
        c, kind = r.choice(CHEM), 'chemical'
        why = 'a new substance is formed; ' + r.choice(CHEM_SIGNS[1:])
    return Q(f'{person(r)} observes {c}. State whether this is a physical or a chemical change and explain your answer.', f'{cap(kind)}: {why}.',
             '1 mark: classification; 1 mark: reason [2]' if D <= 3 else '1 mark: classification; 1 mark: new substance or not; 1 mark: supporting evidence (reversibility/observation) [3]')


@t8a.add('C4', (2, 3, 4, 5), 'multi_step')
def t8a_c4(r, D):
    p = person(r)
    sub = r.choice([('copper(II) carbonate', 'green', 'black', 'carbon dioxide', 'CuCO3', 'CuO'), ('zinc carbonate', 'white', 'yellow when hot, white when cool', 'carbon dioxide', 'ZnCO3', 'ZnO')])
    nm, c1, c2, gas, f1, f2 = sub
    m = r.choice([2.47, 3.70, 4.94, 6.18, 1.24])
    m2 = m * Mr(f2) / Mr(f1)
    intro = f'{p} heats {sf(m, 3)} g of {c1} {nm}, {F(f1)}, in a test tube. The solid turns {c2} and a gas is given off that turns limewater milky. A separate sample of wax is heated: it melts and then solidifies again on cooling.'
    parts = [
        lambda r: ('State whether each change is physical or chemical.', f'heating {nm}: chemical; melting wax: physical', '1 mark each [2]'),
        lambda r: (f'Give two pieces of evidence that heating {nm} is a chemical change.', 'colour change; gas produced (CO₂); not reversed on cooling', '1 mark each [2]'),
        lambda r: ('Write the symbol equation for the decomposition.', E(f'{f1}(s) -> {f2}(s) + CO2(g)'), '[2]'),
        lambda r: (f'Calculate the mass of solid left after complete decomposition. {ar_data(f1)}', f'{g3(m2)} g', f'n = {sf(m, 3)} ÷ {mr(Mr(f1))}; × {mr(Mr(f2))} [2]'),
        lambda r: ('Explain why melting the wax is a physical change.', 'no new substance; the wax solidifies again unchanged', '[1]'),
        lambda r: ('Explain why the mass of the test tube and contents decreases.', 'carbon dioxide gas escapes', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')



# ---------------------------------------------------------- 8.2 factors affecting rate
RATE_RX = [('magnesium', 'hydrochloric acid', 'hydrogen', 'Mg', ['ribbon', 'turnings', 'powder']), ('calcium carbonate (marble)', 'hydrochloric acid', 'carbon dioxide', 'CaCO3', ['large lumps', 'small chips', 'powder']),
           ('zinc', 'sulfuric acid', 'hydrogen', 'Zn', ['large granules', 'small granules', 'powder']), ('calcium carbonate', 'nitric acid', 'carbon dioxide', 'CaCO3', ['large lumps', 'small chips', 'powder']),
           ('iron', 'hydrochloric acid', 'hydrogen', 'Fe', ['nails', 'filings', 'powder'])]
FORMS = ['large lumps', 'small chips', 'powder']
FACTOR_TXT = {'concentration': 'increasing the concentration increases the rate', 'temperature': 'increasing the temperature increases the rate',
              'surface area': 'increasing the surface area (smaller pieces / powder) increases the rate', 'catalyst': 'adding a catalyst increases the rate', 'pressure': 'increasing the pressure of a gaseous reaction increases the rate'}

t8b = T('Factors affecting rate of reaction: concentration, pressure, surface area, temperature and catalysts', 'factors affecting rate of reaction', 'concentration pressure surface area temperature catalysts')
t8b.fixed('C1', (1, 2), [
    ('Which change increases the rate of reaction between marble chips and hydrochloric acid?', 'using powdered marble instead of chips', 'Larger surface area → faster reaction.', ['using larger marble chips', 'cooling the acid', 'using more dilute acid']),
    ('What is a catalyst?', 'a substance that increases the rate of a reaction and is unchanged chemically at the end', 'Catalysts speed up reactions without being used up.', ['a substance that slows a reaction down', 'a reactant that is used up', 'a product of the reaction']),
    ('Which catalyst is used to speed up the decomposition of hydrogen peroxide?', 'manganese(IV) oxide', 'MnO₂ catalyses 2H₂O₂ → 2H₂O + O₂.', ['iron', 'vanadium(V) oxide', 'sodium chloride']),
    ('For a reaction between gases, which change increases the rate?', 'increasing the pressure', 'Particles closer together → more frequent collisions.', ['decreasing the pressure', 'increasing the volume of the container', 'removing the catalyst']),
    ('Which explains why flour dust in a factory can explode?', 'It has a very large surface area.', 'Fine powders react extremely rapidly with oxygen.', ['It has a low melting point.', 'It is a catalyst.', 'It is very dense.']),
    ('State two ways of increasing the rate of reaction between zinc and dilute sulfuric acid.', 'any two: increase acid concentration; increase temperature; use zinc powder; add a catalyst (copper(II) sulfate)', '1 mark each [2]'),
])
t8b.fixed('C2', (2, 3, 4), [
    ('Explain why food is stored in a refrigerator.', 'Lower temperature slows the reactions (including those of microorganisms) that cause food to decay.', '[2]'),
    ('Explain why a catalyst is useful in industry even though it is not used up.', 'It speeds up the reaction so that products are made faster and at lower temperature, saving energy and cost; it can be reused.', '[2]'),
    ('Explain why the total volume of gas produced is the same when the same mass of magnesium reacts with excess acid at two different temperatures.', 'The amount of product depends on the amount of limiting reactant (magnesium), which is the same; temperature only changes how fast the gas is made.', '[2]'),
    ('Describe a fair test to investigate the effect of acid concentration on the rate of reaction with magnesium.', 'Change only the concentration; keep the volume of acid, mass/length of magnesium, temperature and surface area the same; measure the volume of gas over time or the time for the reaction to finish.', '1 mark: one independent variable; 1 mark: two controls; 1 mark: measurement [3]'),
])


def _rate_chain(r, k, FORMS=FORMS):
    """k experiments, each faster than the previous by changing one factor upwards (unambiguous order)."""
    e = {'conc': r.choice([0.25, 0.5, 1.0]), 'temp': r.choice([15, 20, 25]), 'form': r.choice(FORMS[:2])}
    chain = [dict(e)]
    for _ in range(k - 1):
        opts = []
        if e['conc'] < 2.0:
            opts.append('conc')
        if e['temp'] < 60:
            opts.append('temp')
        if FORMS.index(e['form']) < 2:
            opts.append('form')
        f = r.choice(opts)
        e = dict(e)
        if f == 'conc':
            e['conc'] = r.choice([c for c in (0.5, 1.0, 1.5, 2.0) if c > e['conc']])
        elif f == 'temp':
            e['temp'] = e['temp'] + r.choice([10, 15, 20])
        else:
            e['form'] = FORMS[FORMS.index(e['form']) + 1]
        chain.append(e)
    return chain


@t8b.add('C3', (1, 2, 3, 4))
def t8b_rank(r, D):
    k = 3 if D <= 2 else 4
    rx = r.choice(RATE_RX)
    chain = _rate_chain(r, k, rx[4])
    idx = list(range(k))
    r.shuffle(idx)
    exps = [chain[i] for i in idx]
    rows = '; '.join(f'experiment {j + 1}: {e["form"]}, {sf(e["conc"])} mol/dm³ acid, {e["temp"]} °C' for j, e in enumerate(exps))
    order = sorted(range(k), key=lambda j: -idx[j])
    solid = rx[0].split(' (')[0]
    if D <= 2:
        frame = r.choice([f'{who(r)} reacts {solid} with {rx[1]} in {k} experiments.', f'In {lab(r)}, the rate of reaction of {solid} with {rx[1]} is compared.',
                          f'{person(r)} varies the conditions for the reaction of {solid} with {rx[1]}, keeping the mass of solid and volume of acid the same.'])
        return M(r, f'{frame} {rows}. Which experiment has the fastest initial rate?',
                 f'experiment {order[0] + 1}', [f'experiment {j + 1}' for j in range(k)] + ['all the same'],
                 f'Experiment {order[0] + 1} has conditions at least as favourable in every factor (concentration, temperature, surface area) and better in at least one.')
    stem = f'{who(r)} reacts {solid} with {rx[1]}, using the same mass of solid and volume of acid each time. {rows}. Put the experiments in order of initial rate, fastest first, and explain your order.'
    ans = ' > '.join(f'{j + 1}' for j in order)
    return Q(stem, f'Order: {ans}. Higher concentration, higher temperature and smaller pieces (larger surface area) each increase the rate.',
             f'order {ans} [2]; explanation referring to each factor varied [2]', 'case')


@t8b.add('C1', (1, 2, 3))
def t8b_effect(r, D):
    f = r.choice(['concentration', 'temperature', 'surface area', 'catalyst', 'pressure'])
    rx = r.choice(RATE_RX)
    change = {'concentration': f'the {rx[1]} is replaced by a more dilute solution', 'temperature': f'the {rx[1]} is cooled in ice', 'surface area': f'the {rx[0].split(" (")[0]} is used as a powder instead of {rx[4][0]}',
              'catalyst': 'a suitable catalyst is added', 'pressure': 'the pressure of the gases is increased'}[f]
    up = f in ('surface area', 'catalyst', 'pressure')
    ctx = f'In the reaction between {rx[0]} {rx[4][0]} and {rx[1]}, {change}.' if f != 'pressure' else 'In the reaction between nitrogen and hydrogen gases, the pressure is increased.'
    return M(r, f'{ctx} What happens to the rate of reaction?', 'It increases.' if up else 'It decreases.', ['It increases.', 'It decreases.', 'It stays the same.', 'The reaction stops completely.'], FACTOR_TXT[f] + '.')


@t8b.add('C2', (2, 3, 4), 'explain')
def t8b_predict(r, D):
    rx = r.choice(RATE_RX)
    f = r.choice(['concentration', 'temperature', 'surface area', 'catalyst'])
    p = person(r)
    c = {'concentration': f'doubles the concentration of the {rx[1]}', 'temperature': f'warms the {rx[1]} from 20 °C to 40 °C', 'surface area': f'uses powdered {rx[0].split(" (")[0]} instead of {rx[4][0]}',
         'catalyst': 'adds a few drops of copper(II) sulfate solution as a catalyst'}[f]
    if f == 'catalyst' and rx[2] != 'hydrogen':
        return None
    return Q(f'{p} {c} in the reaction between {rx[0]} {rx[4][1]} and {rx[1]}, keeping all other variables the same. Predict the effect on the rate and on the total volume of {rx[2]} produced if the solid is the limiting reactant.',
             f'The rate increases; the total volume of {rx[2]} stays the same because the amount of limiting reactant is unchanged.', '1 mark: rate increases; 1 mark: same total volume with reason [2]' if D <= 3 else '1 mark: rate increases; 1 mark: reason (factor); 1 mark: same final volume, same amount of limiting reactant [3]')


def _t8b_c4(r, D):
    rx = r.choice(RATE_RX)
    p = person(r)
    solid = rx[0].split(' (')[0]
    intro = r.choice([f'{p} plans an investigation into how the rate of reaction between {solid} and {rx[1]} can be changed.', f'A company in {city(r)} wants to make {rx[2]} faster from {solid} and {rx[1]}.'])
    parts = [
        lambda r: ('State three changes that would increase the rate of reaction.', 'increase acid concentration; increase temperature; use smaller pieces / powder (or add a catalyst)', '1 mark each [3]'),
        lambda r: (f'Describe how the rate could be measured.', f'measure the volume of {rx[2]} produced at regular time intervals with a gas syringe (or mass loss on a balance)', '1 mark apparatus; 1 mark timed readings [2]'),
        lambda r: ('Name the independent variable and two control variables for an investigation into the effect of temperature.', f'independent: temperature; control: concentration and volume of acid, mass and size of {solid}', '1 mark independent; 1 mark controls [2]'),
        lambda r: ('Explain why the experiment should be repeated.', 'to identify anomalous results and calculate a reliable mean', '[1]'),
        lambda r: ('Suggest one safety precaution.', 'wear eye protection (acid); no naked flames near hydrogen' if rx[2] == 'hydrogen' else 'wear eye protection; avoid acid on skin', '[1]'),
        lambda r: ('Explain why increasing the temperature by 10 °C can roughly double the rate.', 'particles move faster, collide more often and a much larger proportion have energy ≥ Ea', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t8b.add('C4', (2, 3, 4, 5), 'multi_step')(_t8b_c4)


# ---------------------------------------------------------- 8.3 collision theory
CT = {'concentration': 'there are more reacting particles per unit volume, so collisions are more frequent (more collisions per second)',
      'pressure': 'the gas particles are closer together, so collisions are more frequent',
      'surface area': 'more particles of the solid are exposed to the other reactant, so collisions are more frequent',
      'temperature': 'particles have more kinetic energy and move faster, so they collide more frequently and a greater proportion of collisions have energy greater than or equal to the activation energy',
      'catalyst': 'it provides an alternative pathway with a lower activation energy, so a greater proportion of collisions are successful'}
CT_ERR = [('"A catalyst gives the particles more energy."', 'A catalyst lowers the activation energy; it does not give particles more energy.'),
          ('"Increasing the concentration makes the particles move faster."', 'Concentration increases the number of particles per unit volume, so collisions are more frequent; particle speed depends on temperature.'),
          ('"Increasing the temperature increases the activation energy."', 'Activation energy is unchanged by temperature; more particles have energy ≥ Ea.'),
          ('"Powder reacts faster because its particles are smaller atoms."', 'The atoms are the same; the powder has a larger surface area so more particles are exposed for collisions.'),
          ('"Every collision between particles leads to a reaction."', 'Only collisions with energy ≥ activation energy (and correct orientation) are successful.'),
          ('"Higher temperature makes the reaction faster because there are more particles."', 'The number of particles is the same; they move faster, collide more often and with more energy.'),
          ('"A catalyst is used up in the reaction."', 'A catalyst is chemically unchanged at the end of the reaction.')]

t8c = T('Collision theory and activation energy: explaining changes in rate', 'collision theory', 'explaining changes in rate')
t8c.fixed('C1', (1, 2), [
    ('According to collision theory, what must happen for particles to react?', 'They must collide with at least the activation energy.', 'Successful collisions need energy ≥ Ea.', ['They must be in the same state.', 'They must be heated.', 'They must collide with a catalyst.']),
    ('Why does increasing the concentration of an acid increase the rate of reaction?', 'There are more particles per unit volume, so there are more frequent collisions.', 'Collision frequency increases.', ['The particles move faster.', 'The activation energy decreases.', 'The particles have more energy.']),
    ('Why does increasing temperature increase the rate of reaction?', 'Particles move faster and more collisions have energy ≥ activation energy.', 'More frequent and more energetic collisions.', ['The activation energy is lowered.', 'There are more particles.', 'The surface area increases.']),
    ('What is meant by collision frequency?', 'the number of collisions per unit time', 'Frequency = collisions per second.', ['the energy of each collision', 'the total number of particles', 'the activation energy']),
    ('State the effect of a catalyst on the activation energy of a reaction.', 'It lowers it.', '[1]'),
])
t8c.fixed('C2', (2, 3, 4), [
    ('Explain, using collision theory, why powdered calcium carbonate reacts faster with acid than lumps of the same mass.', 'The powder has a larger surface area, so more particles are exposed to the acid; collisions are more frequent.', '[2]'),
    ('Explain why a small increase in temperature can cause a large increase in rate.', 'A higher temperature increases the energy of the particles, so a much greater proportion of collisions have energy ≥ Ea, as well as increasing collision frequency.', '[2]'),
    ('Explain why the rate of reaction decreases as a reaction proceeds.', 'The reactants are used up, so their concentration decreases and collisions become less frequent.', '[2]'),
    ('Explain why increasing the pressure has no effect on the rate of a reaction between a solid and a liquid.', 'Pressure only affects gases; it changes how close together gas particles are, but has no significant effect on liquids and solids.', '[2]'),
])


@t8c.add('C2', (2, 3, 4), 'explain')
def t8c_explain(r, D):
    f = r.choice(list(CT))
    rx = r.choice(RATE_RX)
    if f == 'pressure':
        ctx = 'In the Haber process, nitrogen and hydrogen react at high pressure.'
        q = 'Explain, using collision theory, why increasing the pressure increases the rate.'
    else:
        solid = rx[0].split(' (')[0]
        ch = {'concentration': f'the concentration of the {rx[1]} is increased', 'surface area': f'the {solid} is used as a powder instead of large pieces',
              'temperature': f'the {rx[1]} is heated to a higher temperature', 'catalyst': 'a catalyst is added'}[f]
        if f == 'surface area':
            ch = f'the {solid} is used as a powder instead of {rx[4][0]}'
        ctx = f'In the reaction between {solid} and {rx[1]}, {ch}.'
        q = 'Explain, using collision theory, why the rate increases.'
    key = {'temperature': '1 mark: particles faster / more kinetic energy; 1 mark: more frequent collisions; 1 mark: greater proportion with energy ≥ Ea [3]',
           'catalyst': '1 mark: alternative pathway; 1 mark: lower activation energy; 1 mark: greater proportion of collisions successful [3]'}.get(f, '1 mark: more particles per unit volume / closer / exposed; 1 mark: more frequent collisions (per second) [2]')
    return Q(f'{ctx} {q}', cap(CT[f]) + '.', key)


@t8c.add('C2', (2, 3))
def t8c_err(r, D):
    s, fix = r.choice(CT_ERR)
    return Q(f'{person(r)} writes: {s} Explain why this statement is incorrect and give a correct statement.', fix, '1 mark: error identified; 1 mark: correct statement [2]')


@t8c.add('C1', (1, 2, 3))
def t8c_mcq(r, D):
    f = r.choice(list(CT))
    wrong = [cap(v) + '.' for k, v in CT.items() if k != f] + ['The particles become larger.', 'The activation energy increases.']
    ch = {'concentration': 'a more concentrated acid is used', 'pressure': 'the pressure of a gaseous reaction mixture is increased', 'surface area': 'a solid reactant is crushed into a powder',
          'temperature': 'the temperature is increased', 'catalyst': 'a catalyst is added'}[f]
    return M(r, f'Which statement explains why the rate increases when {ch}?', cap(CT[f]) + '.', wrong, cap(CT[f]) + '.')


@t8c.add('C3', (2, 3, 4, 5))
def t8c_data(r, D):
    T1 = r.choice([20, 25, 30])
    t1 = r.choice([120, 150, 180, 200, 240])
    rows = []
    temps = [T1 + 10 * i for i in range(4)]
    times = [round(t1 / 2 ** i * r.choice([0.95, 1.0, 1.05])) for i in range(4)]
    rows = ', '.join(f'{T} °C: {t} s' for T, t in zip(temps, times))
    p = person(r)
    stem = f'{p} measures the time taken for a fixed amount of magnesium ribbon to react completely with excess hydrochloric acid at different temperatures: {rows}. Describe the effect of temperature on the time and on the rate, calculate the rate (1/time) at {temps[0]} °C and {temps[-1]} °C, and explain the trend using collision theory.'
    ans = f'As temperature increases the time decreases and the rate increases (roughly doubling every 10 °C). Rate at {temps[0]} °C = {sci(1 / times[0])} /s; at {temps[-1]} °C = {sci(1 / times[-1])} /s. Particles move faster, collide more often, and more collisions have energy ≥ Ea.'
    key = '1 mark: time decreases / rate increases; 1 mark: rates calculated; 1 mark: more frequent collisions; 1 mark: more collisions with energy ≥ Ea [4]'
    if D <= 2:
        stem = f'{p} measures the time for magnesium to react with acid at different temperatures: {rows}. Describe the trend and explain it using collision theory.'
        key = '1 mark: faster at higher temperature; 1 mark: more frequent and more energetic collisions [2]'
        ans = 'As temperature increases the time decreases, so the rate increases (roughly doubling every 10 °C): particles move faster, collide more often, and more collisions have energy ≥ Ea.'
    return Q(stem, ans, key, 'case')


def _t8c_c4(r, D):
    p = person(r)
    intro = r.choice([f'{p} compares the rate of decomposition of hydrogen peroxide, 2H₂O₂ → 2H₂O + O₂, with and without manganese(IV) oxide, and at two different temperatures.', f'A cleaning-products company in {city(r)} studies how fast hydrogen peroxide decomposes to oxygen and water.'])
    parts = [
        lambda r: ('Explain what is meant by activation energy.', 'minimum energy colliding particles need to react', '[1]'),
        lambda r: ('Explain how manganese(IV) oxide increases the rate.', 'catalyst: alternative pathway with lower Ea; greater proportion of collisions successful', '[2]'),
        lambda r: ('Explain why the reaction is faster at a higher temperature.', 'particles faster: more frequent collisions; greater proportion with energy ≥ Ea', '[3]'),
        lambda r: ('Describe how you could show that the manganese(IV) oxide is not used up.', 'filter, wash and dry the catalyst after the reaction and weigh it – same mass; it can catalyse again', '[2]'),
        lambda r: ('Explain why the rate decreases as the reaction proceeds.', 'concentration of H₂O₂ falls, so fewer collisions per second', '[2]'),
        lambda r: ('Suggest why the company stores hydrogen peroxide in a cool, dark place.', 'lower temperature (and no light energy) slows the decomposition', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t8c.add('C4', (2, 3, 4, 5), 'multi_step')(_t8c_c4)


# ---------------------------------------------------------- 8.4 measuring rates and graphs
GAS_RX = [('Mg', 'magnesium ribbon', 'hydrochloric acid', 'H2', 'Mg(s) + 2HCl(aq) -> MgCl2(aq) + H2(g)'),
          ('CaCO3', 'marble chips', 'hydrochloric acid', 'CO2', 'CaCO3(s) + 2HCl(aq) -> CaCl2(aq) + H2O(l) + CO2(g)'),
          ('Zn', 'zinc powder', 'sulfuric acid', 'H2', 'Zn(s) + H2SO4(aq) -> ZnSO4(aq) + H2(g)')]


def gas_curve(r, Vf, n=8, dt=None):
    dt = dt or r.choice([10, 15, 20, 30])
    k = r.choice([3.5, 4.0, 4.5, 5.0]) / ((n - 2) * dt)
    ts = [i * dt for i in range(n)]
    vs = [round(Vf * (1 - math.exp(-k * t))) for t in ts]
    vs[-1] = vs[-2] = round(Vf)
    for i in range(1, n):
        vs[i] = max(vs[i], vs[i - 1])
    return ts, vs, k


t8d = T('Practical methods for measuring rate and interpreting rate-of-reaction graphs', 'practical methods for measuring rate', 'rate-of-reaction graphs')
t8d.fixed('C1', (1, 2), [
    ('Which apparatus is used to measure the volume of gas produced in a reaction?', 'gas syringe', 'A gas syringe collects and measures gas volume.', ['burette', 'pipette', 'thermometer']),
    ('On a graph of volume of gas against time, what does a steeper gradient show?', 'a faster rate of reaction', 'Gradient = rate.', ['a slower rate', 'more gas in total', 'the reaction has stopped']),
    ('On a graph of volume of gas against time, what does it mean when the line becomes horizontal?', 'The reaction has stopped.', 'No more gas is produced: a reactant is used up.', ['The reaction is fastest.', 'The catalyst is used up.', 'The temperature has increased.']),
    ('In the reaction between sodium thiosulfate and hydrochloric acid, what is measured to follow the rate?', 'the time for a cross under the flask to disappear', 'A sulfur precipitate makes the mixture opaque.', ['the volume of hydrogen produced', 'the change in pH', 'the mass of gas lost']),
    ('Why is cotton wool placed in the neck of the flask when following rate by loss in mass?', 'to let carbon dioxide escape but stop acid spray escaping', 'Only gas mass is lost.', ['to stop the gas escaping', 'to act as a catalyst', 'to keep the flask warm']),
    ('State the formula for the average rate of reaction.', 'average rate = amount of product formed (or reactant used) ÷ time taken', '[1]'),
])
t8d.fixed('C2', (2, 3, 4), [
    ('Explain why the gradient of a volume–time graph is steepest at the start of a reaction.', 'The concentration of reactants is highest at the start, so collisions are most frequent and the rate is greatest.', '[2]'),
    ('Explain why measuring the loss in mass is not a good method for a reaction that produces hydrogen.', 'Hydrogen has a very low mass (Mr = 2), so the change in mass is too small to measure accurately.', '[2]'),
    ('Describe how the graph would differ if the same reaction were repeated with half the mass of the limiting reactant at the same temperature.', 'The initial gradient would be similar or slightly less, and the final volume would be half as much.', '[2]'),
    ('Explain why "1/time" can be used as a measure of the rate in the disappearing-cross experiment.', 'The same amount of sulfur is formed each time; a shorter time means a faster rate, so rate is proportional to 1/time.', '[2]'),
])


@t8d.add('C3', (2, 3, 4, 5))
def t8d_syringe(r, D):
    s, sname, acid, gas, e = r.choice(GAS_RX)
    m = r.choice([0.024, 0.048, 0.06, 0.072, 0.096, 0.12]) if s == 'Mg' else (r.choice([0.1, 0.2, 0.25, 0.3, 0.4]) if s == 'CaCO3' else r.choice([0.065, 0.13, 0.195, 0.26]))
    Vf = m / Mr(s) * 24000
    ts, vs, k = gas_curve(r, Vf)
    rows = ', '.join(f'{t} s: {v} cm³' for t, v in zip(ts, vs))
    i = r.choice([2, 3, 4])
    p = person(r)
    intro = f'{p} adds {sf(m, 3)} g of {sname} to excess {acid} and collects the {F(gas)} in a gas syringe. Results: {rows}. {E(nostate(e))}'
    parts = [
        lambda r: (f'Calculate the average rate of reaction during the first {ts[i]} s.', f'{g3(vs[i] / ts[i])} cm³/s', f'{vs[i]} ÷ {ts[i]} [1]'),
        lambda r: ('Describe how the rate changes during the reaction and explain why.', 'fastest at the start, decreases, then zero when reaction stops; reactant concentration decreases / limiting reactant used up', '1 mark description; 1 mark explanation [2]'),
        lambda r: (f'Show by calculation that the final volume is consistent with {sf(m, 3)} g of {F(s)}. {ar_data(s)}', f'{g3(Vf)} cm³', f'n = {sf(m, 3)} ÷ {mr(Mr(s))} = {g3(m / Mr(s))} mol; × 24 000 = {g3(Vf)} cm³ [2]'),
        lambda r: (f'Describe how the results would differ if the experiment were repeated at a higher temperature with the same mass of {sname}.', 'steeper initial gradient (faster); same final volume, reached sooner', '1 mark each [2]'),
        lambda r: ('State one variable that must be controlled.', 'volume/concentration of acid, temperature, size of solid pieces', '[1]'),
        lambda r: (f'Calculate the rate between {ts[1]} s and {ts[2]} s.', f'{g3((vs[2] - vs[1]) / (ts[2] - ts[1]))} cm³/s', f'({vs[2]} − {vs[1]}) ÷ ({ts[2]} − {ts[1]}) [1]'),
    ]
    if D <= 2:
        return compose(r, intro, [parts[0], parts[1], parts[4]], k=(2,), type_='case')
    return compose(r, intro, parts, k=(2, 3) if D == 3 else (3, 4), type_='case')


@t8d.add('C3', (1, 2, 3))
def t8d_avg(r, D):
    s, sname, acid, gas, e = r.choice(GAS_RX)
    V = r.choice(range(20, 120, 4))
    t = r.choice([20, 30, 40, 50, 60, 80, 100, 120])
    if D == 1:
        return NM(r, f'In a reaction of {sname} with {acid}, {V} cm³ of gas is collected in the first {t} s. What is the average rate of reaction?', V / t, [t / V, V * t, V / t * 60, V / (2 * t)], ' cm³/s', f'{V} ÷ {t} = {g3(V / t)} cm³/s')
    return Q(f'{V} cm³ of {F(gas)} is produced in the first {t} s when {sname} reacts with {acid}. Calculate the average rate in cm³/s and in cm³/min.', f'{g3(V / t)} cm³/s; {g3(V / t * 60)} cm³/min',
             f'{V} ÷ {t} = {g3(V / t)} cm³/s [1]; × 60 = {g3(V / t * 60)} cm³/min [1]', 'numerical')


@t8d.add('C3', (2, 3, 4))
def t8d_thio(r, D):
    concs = [0.04, 0.08, 0.12, 0.16, 0.20]
    k = r.choice([4.0, 4.8, 5.6, 6.4])
    times = [round(k / c) for c in concs]
    rows = ', '.join(f'{sf(c)} mol/dm³: {t} s' for c, t in zip(concs, times))
    p = person(r)
    stem = f'{p} times how long it takes for a cross under a flask to disappear when hydrochloric acid is added to sodium thiosulfate solution of different concentrations: {rows}. Calculate 1000/time for the most and least concentrated solutions, describe the relationship between concentration and rate, and explain why the cross disappears.'
    ans = f'1000/t = {g3(1000 / times[-1])} and {g3(1000 / times[0])} /s; rate is (directly) proportional to concentration – doubling the concentration halves the time. A precipitate of sulfur forms and hides the cross.'
    return Q(stem, ans, '1 mark: both values of 1000/t; 1 mark: rate increases with concentration; 1 mark: proportional/doubling halves time; 1 mark: sulfur precipitate [4]', 'case')


@t8d.add('C2', (2, 3, 4), 'explain')
def t8d_method(r, D):
    s, sname, acid, gas, e = r.choice(GAS_RX)
    meth = r.choice(['gas syringe', 'loss in mass', 'upturned measuring cylinder'])
    if meth == 'loss in mass' and gas == 'H2':
        return None
    desc = {'gas syringe': f'connect the flask to a gas syringe; record the volume of {F(gas)} every 10–30 s with a stop-watch', 'loss in mass': 'put the flask with cotton wool in the neck on a balance; record the mass every 30 s as CO₂ escapes',
            'upturned measuring cylinder': 'collect the gas over water in an upturned measuring cylinder; record the volume at regular intervals'}[meth]
    return Q(f'Describe how the rate of reaction between {sname} and {acid} could be followed using a {meth} method, and state what is plotted on the graph.', f'{cap(desc)}; plot {"mass" if meth == "loss in mass" else "volume of gas"} against time.',
             '1 mark: apparatus; 1 mark: readings at regular time intervals; 1 mark: graph axes [3]')


def _t8d_c4(r, D):
    s, sname, acid, gas, e = r.choice(GAS_RX[:2])
    m = 0.12 if s == 'Mg' else 0.5
    Vf = m / Mr(s) * 24000
    ts, vs, k = gas_curve(r, Vf, n=8, dt=20)
    rows = ', '.join(f'{t} s: {v} cm³' for t, v in zip(ts, vs))
    p = person(r)
    intro = f'{p} reacts {sf(m)} g of {sname} with 50 cm³ of 1.0 mol/dm³ {acid} (excess) at 25 °C. Volume of {F(gas)}: {rows}. {ar_data(s)}'
    parts = [
        lambda r: ('Describe how the volume of gas changes with time.', 'increases quickly at first, then more slowly, then stays constant', '[2]'),
        lambda r: ('Calculate the average rate over the first 40 s.', f'{g3(vs[2] / 40)} cm³/s', f'{vs[2]} ÷ 40 [1]'),
        lambda r: ('Calculate the theoretical final volume of gas at r.t.p.', f'{g3(Vf)} cm³', f'{sf(m)} ÷ {mr(Mr(s))} × 24 000 [2]'),
        lambda r: ('Suggest why the reaction stops.', f'all the {sname} has reacted (limiting reactant)', '[1]'),
        lambda r: ('Describe the curve you would expect if 25 cm³ of 2.0 mol/dm³ acid were used instead, with the same solid.', 'steeper at the start (more concentrated); same final volume (same amount of limiting solid)', '1 mark each [2]'),
        lambda r: ('Describe the curve if half the mass of solid were used with the original acid.', f'slightly less steep at first; final volume halved (≈ {g3(Vf / 2)} cm³)', '[2]'),
        lambda r: ('Evaluate whether a gas syringe or mass-loss method is better for this reaction.', 'gas syringe: hydrogen too light for mass loss' if gas == 'H2' else 'either; mass loss works for CO₂ (Mr 44) but the gas syringe is more sensitive for small volumes', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


t8d.add('C4', (2, 3, 4, 5), 'case')(_t8d_c4)

CHAPTERS[8] = [t8a, t8b, t8c, t8d]


# ===================================================================== Ch9 Reversible reactions and equilibrium
t9a = T('Reversible reactions: hydrated and anhydrous copper(II) sulfate and cobalt(II) chloride', 'reversible reactions', 'hydrated and anhydrous copper(ii) sulfate', 'cobalt(ii) chloride')
t9a.fixed('C1', (1, 2), [
    ('What colour change is seen when water is added to anhydrous copper(II) sulfate?', 'white to blue', 'CuSO₄ + 5H₂O → CuSO₄·5H₂O (blue).', ['blue to white', 'pink to blue', 'blue to pink']),
    ('What colour change is seen when hydrated cobalt(II) chloride is heated?', 'pink to blue', 'Water of crystallisation is removed: CoCl₂·6H₂O (pink) → CoCl₂ (blue).', ['blue to pink', 'white to blue', 'blue to white']),
    ('What does the symbol ⇌ show in an equation?', 'The reaction is reversible.', '⇌ means the reaction can go in both directions.', ['The reaction is fast.', 'The reaction is exothermic.', 'A catalyst is used.']),
    ('Which substance is used to test for the presence of water?', 'anhydrous copper(II) sulfate', 'Turns from white to blue with water.', ['limewater', 'universal indicator', 'aqueous bromine']),
    ('What is meant by water of crystallisation?', 'water molecules chemically bonded within the crystal structure of a salt', 'Hydrated salts contain water of crystallisation.', ['water used to dissolve a salt', 'water produced in neutralisation', 'water in the air around crystals']),
    ('State what is meant by a reversible reaction.', 'a reaction in which the products can react to re-form the reactants', '[1]'),
])
t9a.fixed('C2', (2, 3, 4), [
    ('Explain why the test with anhydrous copper(II) sulfate shows that a liquid contains water but not that it is pure water.', 'Any liquid containing water turns it blue; purity must be shown by a sharp boiling point of 100 °C (or melting point of 0 °C).', '1 mark: detects water only; 1 mark: boiling point test for purity [2]'),
    ('Explain why heating blue copper(II) sulfate crystals is described as a reversible reaction.', 'Heating removes the water to give white anhydrous copper(II) sulfate; adding water to the white powder re-forms the blue hydrated salt.', '[2]'),
    ('Explain why the dehydration of hydrated copper(II) sulfate is endothermic and its rehydration is exothermic.', 'Energy is needed to break the bonds to the water of crystallisation; the same amount is released when the water re-bonds (the mixture gets hot).', '[2]'),
    ('Explain how cobalt(II) chloride paper can be used to show the humidity of the air.', 'It is blue when dry and turns pink as it absorbs water vapour; the colour indicates how much water is present.', '[2]'),
])


@t9a.add('C1', (1, 2, 3))
def t9a_colour(r, D):
    salt = r.choice(['copper', 'cobalt'])
    act = r.choice(['heated', 'water added'])
    if salt == 'copper':
        corr = 'blue to white' if act == 'heated' else 'white to blue'
        start = 'hydrated copper(II) sulfate crystals are heated' if act == 'heated' else 'water is added to anhydrous copper(II) sulfate'
        key = 'CuSO₄·5H₂O (blue) ⇌ CuSO₄ (white) + 5H₂O'
    else:
        corr = 'pink to blue' if act == 'heated' else 'blue to pink'
        start = 'hydrated cobalt(II) chloride is heated' if act == 'heated' else 'water is added to anhydrous cobalt(II) chloride'
        key = 'CoCl₂·6H₂O (pink) ⇌ CoCl₂ (blue) + 6H₂O'
    ctx = r.choice([f'What colour change is seen when {start}?', f'{person(r)} observes the solid when {start}. Which colour change is seen?'])
    return M(r, ctx, corr, ['blue to white', 'white to blue', 'pink to blue', 'blue to pink', 'green to blue'], key)


@t9a.add('C3', (2, 3, 4, 5))
def t9a_water(r, D):
    hyd = r.choice([('CuSO4', 5, 'copper(II) sulfate'), ('CoCl2', 6, 'cobalt(II) chloride'), ('MgSO4', 7, 'magnesium sulfate'), ('ZnSO4', 7, 'zinc sulfate'), ('BaCl2', 2, 'barium chloride')])
    f, x, nm = hyd
    n = r.choice([0.01, 0.02, 0.015, 0.025, 0.008, 0.012])
    mh = n * (Mr(f) + 18 * x)
    ma = n * Mr(f)
    p = person(r)
    crucible = r.choice([15.62, 17.08, 18.95, 20.33])
    stem = f'{p} heats a sample of hydrated {nm}, {F(f)}·xH₂O, to constant mass. Mass of crucible = {crucible:.2f} g; crucible + hydrated salt = {crucible + mh:.2f} g; crucible + anhydrous salt = {crucible + ma:.2f} g. Calculate the value of x. {ar_data(f + "H2O")}'
    mw = round(crucible + mh, 2) - round(crucible + ma, 2)
    ma_ = round(crucible + ma, 2) - crucible
    key = f'mass of water = {mw:.2f} g, anhydrous = {ma_:.2f} g [1]; n(water) = {mw:.2f} ÷ 18 = {g3(mw / 18)}, n(salt) = {ma_:.2f} ÷ {mr(Mr(f))} = {g3(ma_ / Mr(f))} [1]; x = {g3(mw / 18 / (ma_ / Mr(f)))} ≈ {x} [1]'
    if abs(mw / 18 / (ma_ / Mr(f)) - x) > 0.3:
        return None
    if D >= 4:
        stem += ' Explain why the sample is heated to constant mass and describe a test to show the water given off is water.'
        key += '; to ensure all water removed [1]; anhydrous copper(II) sulfate turns white to blue [1]'
    return Q(stem, f'x = {x}', key, 'numerical')


@t9a.add('C2', (2, 3, 4), 'explain')
def t9a_explain(r, D):
    ctx = r.choice([('a drop of a colourless liquid from a puddle in ' + city(r) + ' turns white anhydrous copper(II) sulfate blue', 'The liquid contains water; it may not be pure – test the boiling point (100 °C) to check purity.'),
                    ('blue cobalt(II) chloride paper turns pink when left in a bathroom', 'The air contains water vapour, which rehydrates the cobalt(II) chloride: CoCl₂ + 6H₂O → CoCl₂·6H₂O.'),
                    ('white anhydrous copper(II) sulfate gets hot when water is added', 'Rehydration is exothermic: energy is released as water bonds to the copper(II) sulfate (the reverse of the endothermic dehydration).'),
                    ('a bag of silica gel containing blue cobalt(II) chloride indicator turns pink in a shoe box', 'The silica gel has absorbed water; the indicator is hydrated (pink). Heating it would drive off the water and turn it blue again.')])
    s, a = ctx
    return Q(f'Explain the observation: {s}.', a, '1 mark: identifies water / hydration; 1 mark: equation or energy change or reversibility [2]' if D <= 3 else '1 mark: water; 1 mark: reversible hydration; 1 mark: energy or test detail [3]')


def _t9a_c4(r, D):
    p = person(r)
    n = r.choice([0.01, 0.02])
    m = n * Mr('CuSO4.5H2O')
    intro = f'{p} heats {g3(m)} g of blue hydrated copper(II) sulfate crystals, CuSO₄·5H₂O, in an evaporating basin until a white powder remains. Water is then added drop by drop to the cooled powder. {ar_data("CuSO4H2O")}'
    parts = [
        lambda r: ('Write the equation for the reversible reaction, including the ⇌ symbol.', 'CuSO₄·5H₂O ⇌ CuSO₄ + 5H₂O', '[2]'),
        lambda r: ('Describe what is observed when the water is added.', 'white powder turns blue; the mixture gets warm', '1 mark each [2]'),
        lambda r: ('State whether the forward reaction (heating) is endothermic or exothermic, giving a reason.', 'endothermic: heat must be supplied to remove the water', '[1]'),
        lambda r: ('Calculate the mass of white anhydrous copper(II) sulfate formed.', f'{g3(n * Mr("CuSO4"))} g', f'n = {g3(m)} ÷ 250 = {g3(n)} mol; × 160 [2]'),
        lambda r: ('Calculate the mass of water lost.', f'{g3(n * 90)} g', f'{g3(m)} − {g3(n * 160)} [1]'),
        lambda r: ('Suggest how cobalt(II) chloride could be used for the same purpose.', 'blue anhydrous cobalt(II) chloride turns pink with water', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t9a.add('C4', (2, 3, 4, 5), 'multi_step')(_t9a_c4)


# ---------------------------------------------------------- 9.2 dynamic equilibrium
EQM = [('N2(g) + 3H2(g) <=> 2NH3(g)', -92, 'the Haber process'), ('2SO2(g) + O2(g) <=> 2SO3(g)', -196, 'the Contact process'), ('H2(g) + I2(g) <=> 2HI(g)', -10, 'the formation of hydrogen iodide'),
       ('N2O4(g) <=> 2NO2(g)', 58, 'the dissociation of dinitrogen tetroxide (colourless) into nitrogen dioxide (brown)'), ('CO(g) + 2H2(g) <=> CH3OH(g)', -91, 'the manufacture of methanol'),
       ('CH4(g) + H2O(g) <=> CO(g) + 3H2(g)', 206, 'steam reforming of methane'), ('C2H4(g) + H2O(g) <=> C2H5OH(g)', -45, 'the hydration of ethene'),
       ('CO(g) + H2O(g) <=> CO2(g) + H2(g)', -41, 'the water–gas shift reaction'), ('N2(g) + O2(g) <=> 2NO(g)', 181, 'the formation of nitrogen monoxide in car engines'),
       ('2NO(g) + O2(g) <=> 2NO2(g)', -114, 'the oxidation of nitrogen monoxide'), ('PCl5(g) <=> PCl3(g) + Cl2(g)', 93, 'the decomposition of phosphorus pentachloride')]
AR.setdefault('P', 31)
for _e, _h, _d in EQM:
    assert balanced(_e), _e


def gas_moles(e):
    L, R = parse_eq(e)
    return sum(n for n, f, s in L if s == 'g'), sum(n for n, f, s in R if s == 'g')


CHANGES = ['increase temperature', 'decrease temperature', 'increase pressure', 'decrease pressure', 'add a catalyst', 'increase the concentration of a reactant', 'remove the product']


def shift(e, dH, ch):
    gl, gr = gas_moles(e)
    if ch == 'increase temperature':
        return ('left' if dH < 0 else 'right'), f'the forward reaction is {"exothermic" if dH < 0 else "endothermic"}, so the equilibrium shifts in the endothermic direction to oppose the increase in temperature'
    if ch == 'decrease temperature':
        return ('right' if dH < 0 else 'left'), f'the forward reaction is {"exothermic" if dH < 0 else "endothermic"}, so the equilibrium shifts in the exothermic direction'
    if ch in ('increase pressure', 'decrease pressure'):
        if gl == gr:
            return 'none', f'there are equal numbers of moles of gas on each side ({gl} and {gr}), so pressure has no effect on the position of equilibrium'
        fewer = 'right' if gr < gl else 'left'
        more = 'left' if fewer == 'right' else 'right'
        if ch == 'increase pressure':
            return fewer, f'there are {gl} mol of gas on the left and {gr} on the right; the equilibrium shifts towards fewer gas molecules'
        return more, f'there are {gl} mol of gas on the left and {gr} on the right; the equilibrium shifts towards more gas molecules'
    if ch == 'add a catalyst':
        return 'none', 'a catalyst speeds up the forward and reverse reactions equally; equilibrium is reached faster but its position is unchanged'
    return 'right', 'the equilibrium shifts to the right to oppose the change (use up the added reactant / replace the removed product)'


def yield_word(d):
    return {'right': 'increases', 'left': 'decreases', 'none': 'does not change'}[d]


t9b = T('Dynamic equilibrium and predicting the effect of temperature, pressure and concentration', 'dynamic equilibrium', 'effect of temperature, pressure and concentration')
t9b.fixed('C1', (1, 2), [
    ('Which statement about a reaction at dynamic equilibrium is correct?', 'The rates of the forward and reverse reactions are equal.', 'Dynamic equilibrium: both reactions continue at equal rates; concentrations stay constant.',
     ['The forward and reverse reactions have stopped.', 'The concentrations of reactants and products are always equal.', 'Only the forward reaction takes place.']),
    ('What is needed for a reversible reaction to reach equilibrium?', 'a closed system', 'No substances can enter or leave.', ['an open container', 'a catalyst', 'a high temperature']),
    ('What is the effect of a catalyst on the position of equilibrium?', 'There is no effect.', 'It increases both rates equally.', ['It shifts to the right.', 'It shifts to the left.', 'It increases the yield.']),
    ('At equilibrium, what can be said about the concentrations of reactants and products?', 'They remain constant.', 'Constant but not necessarily equal.', ['They are equal.', 'They keep increasing.', 'They are both zero.']),
    ('State the meaning of a closed system.', 'a system from which no substances can escape or be added', '[1]'),
])
t9b.fixed('C2', (2, 3, 4), [
    ('Explain why an equilibrium is described as dynamic.', 'Both the forward and reverse reactions are still happening, at the same rate, so the concentrations do not change even though particles are constantly reacting.', '[2]'),
    ('Explain why equilibrium cannot be reached in an open beaker if one of the products is a gas.', 'The gas escapes, so the reverse reaction cannot take place; the system is not closed.', '[2]'),
    ('Explain why a catalyst is used in industry even though it does not change the yield at equilibrium.', 'It increases the rate so equilibrium is reached faster, allowing a lower temperature to be used and saving time and energy.', '[2]'),
    ('A student says that at equilibrium there are equal amounts of reactants and products. Explain the error.', 'At equilibrium the rates of the forward and reverse reactions are equal; the amounts are constant but usually not equal.', '[2]'),
])


@t9b.add('C1', (1, 2, 3))
def t9b_mcq(r, D):
    e, dH, d = r.choice(EQM)
    ch = r.choice(CHANGES[:5])
    dirn, why = shift(e, dH, ch)
    words = {'right': 'The position of equilibrium shifts to the right.', 'left': 'The position of equilibrium shifts to the left.', 'none': 'The position of equilibrium does not change.'}
    return M(r, neg(f'For {d}, {E(nostate(e))}, ΔH = {dH:+d} kJ/mol, what is the effect of the following change: {ch}?'), words[dirn],
             list(words.values()) + ['The reaction stops.'], cap(why) + '.')


@t9b.add('C2', (2, 3, 4), 'explain')
def t9b_explain(r, D):
    e, dH, d = r.choice(EQM)
    ch = r.choice(CHANGES)
    dirn, why = shift(e, dH, ch)
    L, R = parse_eq(e)
    prod = ' and '.join(F(f) for _, f, _ in R)
    if ch == 'increase the concentration of a reactant':
        rf = r.choice(L)[1]
        ch = f'the concentration of {F(rf)} is increased'
    elif ch == 'remove the product':
        ch = f'{F(R[0][1])} is removed as it forms'
    return Q(neg(f'Consider {d}: {E(e)}, ΔH = {dH:+d} kJ/mol. Predict and explain the effect on the position of equilibrium and on the yield of {prod} when {ch}.'),
             f'Equilibrium {"shifts to the " + dirn if dirn != "none" else "position does not change"}; yield of {prod} {yield_word(dirn)}. Reason: {why}.',
             '1 mark: direction; 1 mark: effect on yield; 1 mark: reason [3]' if D >= 3 else '1 mark: direction/yield; 1 mark: reason [2]')


@t9b.add('C3', (2, 3, 4, 5))
def t9b_multi(r, D):
    e, dH, d = r.choice(EQM)
    chs = r.sample(CHANGES[:5], 3 if D <= 3 else 4)
    res = [(c, *shift(e, dH, c)) for c in chs]
    gl, gr = gas_moles(e)
    stem = neg(f'{cap(d)} is represented by {E(e)}, ΔH = {dH:+d} kJ/mol. For each change, predict the effect on the equilibrium yield of products: ' + '; '.join(c for c in chs) + '.')
    ans = '; '.join(f'{c}: yield {yield_word(dn)}' for c, dn, w in res)
    key = '; '.join(f'{c} → {yield_word(dn)} ({w})' for c, dn, w in res) + f'. 1 mark each [{len(chs)}]'
    if D >= 5:
        stem += ' Suggest the conditions of temperature and pressure that would give the highest yield, and comment on why these may not be used in industry.'
        bestT = 'low' if dH < 0 else 'high'
        bestP = 'high' if gr < gl else ('low' if gr > gl else 'any (no effect)')
        ans += f'. Highest yield: {bestT} temperature, {bestP} pressure; a compromise is used because low temperature gives a slow rate and high pressure is expensive/dangerous.'
        key += f'; {bestT} T and {bestP} P [1]; compromise reason [1]'
    return Q(stem, ans, key, 'short')


@t9b.add('C3', (3, 4, 5))
def t9b_colour(r, D):
    sc = r.choice([('N2O4(g) <=> 2NO2(g)', 58, 'colourless', 'brown', 'N₂O₄', 'NO₂'),
                   ('2NO2(g) <=> N2O4(g)', -58, 'brown', 'colourless', 'NO₂', 'N₂O₄')])
    e, dH, c1, c2, a, b = sc
    ch = r.choice(['the sealed syringe is placed in hot water', 'the sealed syringe is placed in iced water', 'the plunger of the sealed syringe is pushed in quickly and held'])
    if 'hot' in ch:
        dirn = 'right' if dH > 0 else 'left'
        why = 'the endothermic direction is favoured at higher temperature'
    elif 'iced' in ch:
        dirn = 'left' if dH > 0 else 'right'
        why = 'the exothermic direction is favoured at lower temperature'
    else:
        gl, gr = gas_moles(e)
        dirn = 'right' if gr < gl else 'left'
        why = 'higher pressure favours the side with fewer gas molecules'
    more = c2 if dirn == 'right' else c1
    colour = 'darker brown' if more == 'brown' else 'paler'
    return Q(neg(f'A sealed syringe contains an equilibrium mixture: {E(e)}, ΔH = {dH:+d} kJ/mol. {a} is {c1} and {b} is {c2}. Predict and explain the colour change when {ch}.'),
             f'The mixture becomes {colour}: equilibrium shifts to the {dirn} because {why}.', '1 mark: colour change; 1 mark: direction; 1 mark: reason [3]', 'short')


def _t9b_c4(r, D):
    e, dH, d = r.choice(EQM)
    gl, gr = gas_moles(e)
    p = person(r)
    intro = neg(f'{p} studies {d}: {E(e)}, ΔH = {dH:+d} kJ/mol. The reaction is carried out in a closed system.')
    parts = [
        lambda r: ('Explain what is meant by dynamic equilibrium.', 'forward and reverse rates equal; concentrations constant; both reactions continue', '[2]'),
        lambda r: ('Predict and explain the effect of increasing the temperature on the yield.', f'yield {yield_word(shift(e, dH, "increase temperature")[0])}: {shift(e, dH, "increase temperature")[1]}', '1 mark effect; 1 mark reason [2]'),
        lambda r: ('Predict and explain the effect of increasing the pressure on the yield.', f'yield {yield_word(shift(e, dH, "increase pressure")[0])}: {shift(e, dH, "increase pressure")[1]}', '1 mark effect; 1 mark reason [2]'),
        lambda r: ('Explain the effect of a catalyst on the rate and on the yield.', 'rate increases (equilibrium reached sooner); yield unchanged', '[2]'),
        lambda r: ('Explain why increasing the temperature increases the rate even if it lowers the yield.', 'particles faster: more frequent, more energetic collisions', '[1]'),
        lambda r: ('Suggest why the system must be closed.', 'so that no reactants or products escape, allowing equilibrium to be established', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t9b.add('C4', (2, 3, 4, 5), 'multi_step')(_t9b_c4)
t9b.add('C3', (4, 5), 'multi_step')(_t9b_c4)


# ---------------------------------------------------------- 9.3 Haber and Contact
HABER_P = [10, 25, 50, 100, 200, 400]
HABER_T = {200: [50.7, 63.6, 74.0, 81.5, 89.0, 94.6], 300: [14.7, 27.4, 39.5, 52.5, 66.7, 79.7], 400: [3.9, 8.7, 15.3, 25.2, 38.7, 55.4], 500: [1.2, 2.9, 5.6, 10.6, 18.3, 31.9]}

t9c = T('Industrial conditions: Haber process and Contact process', 'haber process', 'contact process', 'industrial conditions')
t9c.fixed('C1', (1, 2), [
    ('What are the typical conditions used in the Haber process?', '450 °C, 200 atm, iron catalyst', 'Compromise conditions for rate, yield and cost.', ['450 °C, 2 atm, vanadium(V) oxide catalyst', '25 °C, 1 atm, no catalyst', '1000 °C, 1000 atm, platinum catalyst']),
    ('Which catalyst is used in the Contact process?', 'vanadium(V) oxide', 'V₂O₅ catalyses 2SO₂ + O₂ ⇌ 2SO₃.', ['iron', 'nickel', 'manganese(IV) oxide']),
    ('What is the source of the hydrogen used in the Haber process?', 'methane (natural gas)', 'Hydrogen is obtained from methane by reaction with steam.', ['the air', 'sea water by distillation', 'sulfur']),
    ('What is the source of nitrogen for the Haber process?', 'the air', 'Fractional distillation of liquid air.', ['natural gas', 'water', 'ammonium salts']),
    ('Which pressure is used in the Contact process?', '1–2 atm', 'Yield is already high; high pressure not worth the cost.', ['200 atm', '1000 atm', '50 atm']),
    ('State the source of sulfur dioxide for the Contact process.', 'burning sulfur (or roasting sulfide ores)', '[1]'),
    ('Write the equation for the reaction in the Haber process.', 'N₂ + 3H₂ ⇌ 2NH₃', '[1]'),
])
t9c.fixed('C2', (2, 3, 4), [
    ('Explain why a temperature of about 450 °C is used in the Haber process even though a lower temperature gives a higher yield.', 'The forward reaction is exothermic, so a lower temperature would increase yield, but the rate would be too slow; 450 °C is a compromise between rate and yield.', '1 mark: lower T higher yield (exothermic); 1 mark: rate too slow; 1 mark: compromise [3]'),
    ('Explain why a pressure of 200 atm is used in the Haber process rather than 1000 atm.', 'Higher pressure increases yield (fewer gas molecules on the right) and rate, but very high pressures are expensive to produce and dangerous; 200 atm is a compromise.', '[2]'),
    ('Explain why the Contact process uses a low pressure of about 2 atm.', 'The equilibrium yield of SO₃ is already very high (about 99%) at low pressure, so the extra cost of high pressure is not justified.', '[2]'),
    ('Explain why unreacted nitrogen and hydrogen are recycled in the Haber process.', 'Only about 15% conversion is achieved per pass; recycling the unreacted gases means they are eventually converted, saving raw materials and money.', '[2]'),
    ('Explain how ammonia is separated from the unreacted gases in the Haber process.', 'The mixture is cooled; ammonia condenses to a liquid (higher boiling point) while nitrogen and hydrogen remain as gases.', '[2]'),
])


@t9c.add('C3', (2, 3, 4, 5))
def t9c_table(r, D):
    Ts = sorted(r.sample(list(HABER_T), 3))
    ps = sorted(r.sample(range(6), 4))
    rows = '; '.join(f'{T} °C: ' + ', '.join(f'{HABER_P[i]} atm {HABER_T[T][i]}%' for i in ps) for T in Ts)
    T0 = r.choice(Ts)
    i0 = r.choice(ps)
    stem = f'The table shows the percentage of ammonia at equilibrium under different conditions. {rows}. State the percentage yield at {T0} °C and {HABER_P[i0]} atm, and describe the effects of temperature and pressure on the yield.'
    ans = f'{HABER_T[T0][i0]}%. Yield increases as pressure increases and decreases as temperature increases.'
    key = f'{HABER_T[T0][i0]}% [1]; higher pressure → higher yield [1]; higher temperature → lower yield [1]'
    if D >= 4:
        stem += ' Explain these trends using N₂ + 3H₂ ⇌ 2NH₃, ΔH = −92 kJ/mol, and explain why 450 °C and 200 atm are chosen in industry.'
        ans += ' Pressure: 4 mol gas → 2 mol, so high pressure favours NH₃. Temperature: forward reaction exothermic, so low temperature favours NH₃. 450 °C gives an acceptable rate; 200 atm limits cost and danger.'
        key += '; fewer gas molecules on the right [1]; exothermic forward reaction [1]; compromise rate/cost/safety [1]'
    return Q(stem, ans, key, 'case')


@t9c.add('C1', (1, 2, 3))
def t9c_cond(r, D):
    proc = r.choice(['Haber', 'Contact'])
    what = r.choice(['temperature', 'pressure', 'catalyst', 'equation'])
    data = {'Haber': {'temperature': '450 °C', 'pressure': '200 atm', 'catalyst': 'iron', 'equation': 'N₂ + 3H₂ ⇌ 2NH₃'},
            'Contact': {'temperature': '450 °C', 'pressure': '2 atm', 'catalyst': 'vanadium(V) oxide', 'equation': '2SO₂ + O₂ ⇌ 2SO₃'}}
    pool = {'temperature': ['450 °C', '25 °C', '1000 °C', '100 °C'], 'pressure': ['200 atm', '2 atm', '1000 atm', '50 atm'], 'catalyst': ['iron', 'vanadium(V) oxide', 'nickel', 'platinum'],
            'equation': ['N₂ + 3H₂ ⇌ 2NH₃', '2SO₂ + O₂ ⇌ 2SO₃', 'N₂ + H₂ ⇌ NH₃', 'S + O₂ → SO₂']}[what]
    return M(r, f'Which {what} is used in the {proc} process?' if what != 'equation' else f'Which equation represents the main reversible reaction in the {proc} process?', data[proc][what], pool,
             f'{proc} process: {data[proc]["temperature"]}, {data[proc]["pressure"]}, {data[proc]["catalyst"]} catalyst; {data[proc]["equation"]}.')


@t9c.add('C2', (2, 3, 4), 'explain')
def t9c_why(r, D):
    proc = r.choice(['Haber', 'Contact'])
    fac = r.choice(['temperature', 'pressure', 'catalyst'])
    a = {('Haber', 'temperature'): 'Forward reaction is exothermic, so low temperature gives a higher yield but a slow rate; 450 °C is a compromise between rate and yield.',
         ('Haber', 'pressure'): '4 mol of gas form 2 mol, so high pressure increases yield and rate; 200 atm balances yield against the cost and danger of higher pressures.',
         ('Haber', 'catalyst'): 'Iron increases the rate so equilibrium is reached quickly at a moderate temperature; it does not change the yield.',
         ('Contact', 'temperature'): 'Forward reaction is exothermic, so low temperature favours SO₃ but is slow; 450 °C is a compromise.',
         ('Contact', 'pressure'): '3 mol of gas form 2 mol, so higher pressure would favour SO₃, but the yield is already about 99% at 2 atm, so high pressure is not worth the cost.',
         ('Contact', 'catalyst'): 'Vanadium(V) oxide increases the rate of formation of SO₃ without affecting the equilibrium position.'}[(proc, fac)]
    return Q(f'Explain the choice of {fac} used in the {proc} process.', a, '1 mark: effect on yield/rate; 1 mark: justification (compromise/cost) [2]' if D <= 3 else '1 mark: effect on yield with reason; 1 mark: effect on rate; 1 mark: compromise/cost [3]')


def _t9c_c4(r, D):
    proc = r.choice(['Haber', 'Contact'])
    p = person(r)
    if proc == 'Haber':
        intro = f'A fertiliser company near {city(r)} makes ammonia by the Haber process: N₂(g) + 3H₂(g) ⇌ 2NH₃(g), ΔH = −92 kJ/mol.'
        parts = [
            lambda r: ('State the sources of the nitrogen and hydrogen.', 'nitrogen from the air; hydrogen from methane (natural gas)', '1 mark each [2]'),
            lambda r: ('State the conditions used.', '450 °C, 200 atm, iron catalyst', '1 mark each [3]'),
            lambda r: ('Explain why a higher pressure gives a higher yield.', '4 mol gas → 2 mol; equilibrium shifts to fewer gas molecules', '[2]'),
            lambda r: ('Explain why 450 °C is described as a compromise temperature.', 'lower T gives higher yield (exothermic) but too slow; 450 °C gives acceptable rate and yield', '[2]'),
            lambda r: ('Describe how ammonia is removed and what happens to unreacted gases.', 'cooled so ammonia liquefies; unreacted N₂ and H₂ recycled', '[2]'),
            lambda r: ('Calculate the maximum mass of ammonia from 56 tonnes of nitrogen.', '68 tonnes', '56/28 = 2 Mmol N₂ → 4 Mmol NH₃ × 17 = 68 t [2]'),
        ]
    else:
        intro = f'Sulfuric acid is made in {city(r)} by the Contact process. The key step is 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH = −196 kJ/mol.'
        parts = [
            lambda r: ('State the sources of the sulfur dioxide and oxygen.', 'burning sulfur (or roasting sulfide ores); air', '1 mark each [2]'),
            lambda r: ('State the conditions used.', '450 °C, 1–2 atm, vanadium(V) oxide catalyst', '1 mark each [3]'),
            lambda r: ('Explain why a low pressure is used even though higher pressure favours SO₃.', 'yield already high (~99%) at low pressure; high pressure costly', '[2]'),
            lambda r: ('Explain the effect of increasing the temperature on the yield of SO₃.', 'decreases: forward reaction exothermic so equilibrium shifts left', '[2]'),
            lambda r: ('State the role of the vanadium(V) oxide.', 'catalyst: increases rate, unchanged at end', '[1]'),
            lambda r: ('Calculate the maximum mass of SO₃ from 128 tonnes of SO₂.', '160 tonnes', '128/64 = 2 Mmol → 2 Mmol × 80 = 160 t [2]'),
        ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t9c.add('C4', (2, 3, 4, 5), 'multi_step')(_t9c_c4)

CHAPTERS[9] = [t9a, t9b, t9c]


# ===================================================================== Ch10 Redox
REDOX_O = [  # equation, oxidised, reduced, oxidising agent, reducing agent (oxygen transfer)
    ('CuO(s) + H2(g) -> Cu(s) + H2O(l)', 'hydrogen', 'copper(II) oxide', 'copper(II) oxide', 'hydrogen'),
    ('Fe2O3(s) + 3CO(g) -> 2Fe(l) + 3CO2(g)', 'carbon monoxide', 'iron(III) oxide', 'iron(III) oxide', 'carbon monoxide'),
    ('2PbO(s) + C(s) -> 2Pb(s) + CO2(g)', 'carbon', 'lead(II) oxide', 'lead(II) oxide', 'carbon'),
    ('ZnO(s) + C(s) -> Zn(s) + CO(g)', 'carbon', 'zinc oxide', 'zinc oxide', 'carbon'),
    ('CuO(s) + Mg(s) -> Cu(s) + MgO(s)', 'magnesium', 'copper(II) oxide', 'copper(II) oxide', 'magnesium'),
    ('Fe2O3(s) + 2Al(s) -> Al2O3(s) + 2Fe(l)', 'aluminium', 'iron(III) oxide', 'iron(III) oxide', 'aluminium'),
    ('2CuO(s) + C(s) -> 2Cu(s) + CO2(g)', 'carbon', 'copper(II) oxide', 'copper(II) oxide', 'carbon'),
    ('PbO(s) + H2(g) -> Pb(s) + H2O(l)', 'hydrogen', 'lead(II) oxide', 'lead(II) oxide', 'hydrogen'),
    ('Fe2O3(s) + 3C(s) -> 2Fe(s) + 3CO(g)', 'carbon', 'iron(III) oxide', 'iron(III) oxide', 'carbon'),
    ('2Mg(s) + CO2(g) -> 2MgO(s) + C(s)', 'magnesium', 'carbon dioxide', 'carbon dioxide', 'magnesium'),
]
REDOX_E = [  # ionic equation (display), oxidised species, reduced species, ox half, red half
    ('Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)', 'Zn', 'Cu²⁺', 'Zn → Zn²⁺ + 2e⁻', 'Cu²⁺ + 2e⁻ → Cu'),
    ('Mg(s) + Cu²⁺(aq) → Mg²⁺(aq) + Cu(s)', 'Mg', 'Cu²⁺', 'Mg → Mg²⁺ + 2e⁻', 'Cu²⁺ + 2e⁻ → Cu'),
    ('Fe(s) + Cu²⁺(aq) → Fe²⁺(aq) + Cu(s)', 'Fe', 'Cu²⁺', 'Fe → Fe²⁺ + 2e⁻', 'Cu²⁺ + 2e⁻ → Cu'),
    ('Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)', 'Cu', 'Ag⁺', 'Cu → Cu²⁺ + 2e⁻', 'Ag⁺ + e⁻ → Ag'),
    ('Mg(s) + 2Ag⁺(aq) → Mg²⁺(aq) + 2Ag(s)', 'Mg', 'Ag⁺', 'Mg → Mg²⁺ + 2e⁻', 'Ag⁺ + e⁻ → Ag'),
    ('Cl₂(aq) + 2Br⁻(aq) → 2Cl⁻(aq) + Br₂(aq)', 'Br⁻', 'Cl₂', '2Br⁻ → Br₂ + 2e⁻', 'Cl₂ + 2e⁻ → 2Cl⁻'),
    ('Cl₂(aq) + 2I⁻(aq) → 2Cl⁻(aq) + I₂(aq)', 'I⁻', 'Cl₂', '2I⁻ → I₂ + 2e⁻', 'Cl₂ + 2e⁻ → 2Cl⁻'),
    ('Br₂(aq) + 2I⁻(aq) → 2Br⁻(aq) + I₂(aq)', 'I⁻', 'Br₂', '2I⁻ → I₂ + 2e⁻', 'Br₂ + 2e⁻ → 2Br⁻'),
    ('Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g)', 'Zn', 'H⁺', 'Zn → Zn²⁺ + 2e⁻', '2H⁺ + 2e⁻ → H₂'),
    ('Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g)', 'Mg', 'H⁺', 'Mg → Mg²⁺ + 2e⁻', '2H⁺ + 2e⁻ → H₂'),
    ('2Na(s) + Cl₂(g) → 2NaCl(s)', 'Na', 'Cl₂', 'Na → Na⁺ + e⁻', 'Cl₂ + 2e⁻ → 2Cl⁻'),
    ('Zn(s) + Pb²⁺(aq) → Zn²⁺(aq) + Pb(s)', 'Zn', 'Pb²⁺', 'Zn → Zn²⁺ + 2e⁻', 'Pb²⁺ + 2e⁻ → Pb'),
    ('2Fe²⁺(aq) + Cl₂(aq) → 2Fe³⁺(aq) + 2Cl⁻(aq)', 'Fe²⁺', 'Cl₂', 'Fe²⁺ → Fe³⁺ + e⁻', 'Cl₂ + 2e⁻ → 2Cl⁻'),
    ('2Al(s) + 3Cu²⁺(aq) → 2Al³⁺(aq) + 3Cu(s)', 'Al', 'Cu²⁺', 'Al → Al³⁺ + 3e⁻', 'Cu²⁺ + 2e⁻ → Cu'),
]

t10a = T('Oxidation and reduction as gain or loss of oxygen and loss or gain of electrons', 'oxidation and reduction', 'gain or loss of oxygen', 'loss or gain of electrons')
t10a.fixed('C1', (1, 2), [
    ('What is oxidation in terms of electrons?', 'loss of electrons', 'OIL RIG: oxidation is loss, reduction is gain.', ['gain of electrons', 'gain of protons', 'loss of neutrons']),
    ('What is reduction in terms of oxygen?', 'loss of oxygen', 'A substance that loses oxygen is reduced.', ['gain of oxygen', 'gain of hydrogen ions', 'loss of electrons']),
    ('What is a redox reaction?', 'a reaction in which oxidation and reduction take place at the same time', 'Electrons lost by one species are gained by another.', ['a reaction that only involves oxygen', 'a neutralisation reaction', 'a reaction in which a precipitate forms']),
    ('In the reaction Zn + Cu²⁺ → Zn²⁺ + Cu, which species is reduced?', 'Cu²⁺', 'Cu²⁺ gains two electrons.', ['Zn', 'Zn²⁺', 'Cu']),
    ('State the meaning of OIL RIG.', 'Oxidation Is Loss (of electrons), Reduction Is Gain (of electrons)', '[1]'),
])
t10a.fixed('C2', (2, 3, 4), [
    ('Explain why the reaction of magnesium with oxygen is described as oxidation in two different ways.', 'Magnesium gains oxygen to form MgO; also each Mg atom loses two electrons to form Mg²⁺.', '1 mark: gains oxygen; 1 mark: loses electrons [2]'),
    ('Explain why oxidation and reduction must always happen together.', 'Electrons lost by one substance must be gained by another (or oxygen removed from one is added to another).', '[2]'),
    ('Explain why the reaction of chlorine with potassium bromide is a redox reaction even though no oxygen is involved.', 'Bromide ions lose electrons (oxidised) to form bromine; chlorine gains electrons (reduced) to form chloride ions.', '[2]'),
    ('A student says, "In Fe₂O₃ + 3CO → 2Fe + 3CO₂, iron is oxidised because it changes." Explain the error.', 'Iron(III) oxide loses oxygen, so it is reduced; carbon monoxide gains oxygen and is oxidised.', '[2]'),
])


@t10a.add('C1', (1, 2, 3))
def t10a_oxy(r, D):
    e, ox, red, oa, ra = r.choice(REDOX_O)
    which = r.choice(['oxidised', 'reduced'])
    corr = ox if which == 'oxidised' else red
    L, R = parse_eq(e)
    names = [ox, red] + ['the metal formed', 'oxygen']
    return M(r, f'In the reaction {E(e)}, which substance is {which}?', corr, names, f'{cap(ox)} gains oxygen (oxidised); {red} loses oxygen (reduced).')


@t10a.add('C3', (2, 3, 4, 5))
def t10a_elec(r, D):
    e, ox, red, h1, h2 = r.choice(REDOX_E)
    stem = f'For the reaction {e}, identify the species oxidised and the species reduced, explaining your answer in terms of electrons.'
    ans = f'{ox} is oxidised (loses electrons: {h1}); {red} is reduced (gains electrons: {h2}).'
    key = f'1 mark: {ox} oxidised; 1 mark: {red} reduced; 1 mark: electron loss/gain explanation [3]'
    if D >= 4:
        stem += ' Write the two half-equations.'
        key = key.replace(' [3]', f'; 1 mark: {h1}; 1 mark: {h2} [5]')
    if D == 2:
        return M(r, f'In the reaction {e}, which statement is correct?', f'{ox} loses electrons and is oxidised.', [f'{ox} gains electrons and is reduced.', f'{red} loses electrons and is oxidised.', f'{ox} gains electrons and is oxidised.', f'{red} gains electrons and is oxidised.'],
                 f'{h1} (oxidation); {h2} (reduction).')
    return Q(stem, ans, key, 'short')


@t10a.add('C2', (2, 3, 4), 'explain')
def t10a_explain(r, D):
    e, ox, red, oa, ra = r.choice(REDOX_O)
    return Q(f'Explain why the reaction {E(e)} is a redox reaction.', f'{cap(red)} loses oxygen, so it is reduced; {ox} gains oxygen, so it is oxidised. Both happen at once.',
             '1 mark: reduced species with reason; 1 mark: oxidised species with reason [2]' if D <= 3 else '1 mark: reduced; 1 mark: oxidised; 1 mark: simultaneous / oxygen transferred from one to the other [3]')


@t10a.add('C2', (2, 3))
def t10a_spot(r, D):
    e, ox, red, h1, h2 = r.choice(REDOX_E)
    p = person(r)
    return Q(f'{p} writes that in the reaction {e}, "{red} is oxidised because it gains electrons." Identify the error and correct it.', f'Gaining electrons is reduction: {red} is reduced ({h2}); {ox} is oxidised ({h1}).',
             '1 mark: gain of electrons = reduction; 1 mark: correct identification [2]')


def _t10a_c4(r, D):
    e, ox, red, oa, ra = r.choice(REDOX_O)
    e2, ox2, red2, h1, h2 = r.choice(REDOX_E)
    p = person(r)
    intro = f'{p} studies two reactions. Reaction 1: {E(e)}. Reaction 2: {e2}.'
    parts = [
        lambda r: ('Define oxidation and reduction in terms of oxygen.', 'oxidation: gain of oxygen; reduction: loss of oxygen', '[2]'),
        lambda r: ('Identify the substance oxidised and the substance reduced in reaction 1.', f'oxidised: {ox}; reduced: {red}', '1 mark each [2]'),
        lambda r: ('Define oxidation and reduction in terms of electrons.', 'oxidation: loss of electrons; reduction: gain of electrons', '[2]'),
        lambda r: ('Write the two half-equations for reaction 2.', f'{h1}; {h2}', '1 mark each [2]'),
        lambda r: ('Identify the oxidising agent in reaction 2.', red2, '[1]'),
        lambda r: ('Explain why reaction 2 is a redox reaction even though no oxygen is involved.', f'electrons are transferred from {ox2} to {red2}', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t10a.add('C4', (2, 3, 4, 5), 'multi_step')(_t10a_c4)


# ---------------------------------------------------------- 10.2 oxidation numbers
KNOWN_ON = {'O': -2, 'H': 1, 'K': 1, 'Na': 1, 'Li': 1, 'F': -1, 'Mg': 2, 'Ca': 2, 'Ba': 2, 'Al': 3}
OXN = [('H2SO4', 0, 'S'), ('SO2', 0, 'S'), ('H2S', 0, 'S'), ('SO3', 0, 'S'), ('SO4', -2, 'S'), ('SO3', -2, 'S'), ('NH3', 0, 'N'), ('NO2', 0, 'N'), ('HNO3', 0, 'N'), ('NO3', -1, 'N'),
       ('NH4', 1, 'N'), ('N2O', 0, 'N'), ('NO', 0, 'N'), ('N2O4', 0, 'N'), ('KMnO4', 0, 'Mn'), ('MnO2', 0, 'Mn'), ('MnO4', -1, 'Mn'), ('K2Cr2O7', 0, 'Cr'), ('Cr2O7', -2, 'Cr'),
       ('Cr2O3', 0, 'Cr'), ('CrO4', -2, 'Cr'), ('Fe2O3', 0, 'Fe'), ('FeO', 0, 'Fe'), ('NaClO', 0, 'Cl'), ('ClO3', -1, 'Cl'), ('NaClO3', 0, 'Cl'), ('HCl', 0, 'Cl'), ('CO2', 0, 'C'),
       ('CO', 0, 'C'), ('CH4', 0, 'C'), ('CO3', -2, 'C'), ('Cu2O', 0, 'Cu'), ('CuO', 0, 'Cu'), ('P4O10', 0, 'P'), ('PO4', -3, 'P'), ('KIO3', 0, 'I'), ('Cl2O7', 0, 'Cl'), ('SO2Cl2', 0, 'S')]


def oxnum(f, q, el):
    at = atoms(f)
    known = dict(KNOWN_ON)
    if el != 'Cl' and 'Cl' in at:
        known['Cl'] = -1
    s = sum(known[e] * n for e, n in at.items() if e != el)
    v = (q - s) / at[el]
    return int(v) if v == int(v) else v


def sp(f, q):
    if q == 0:
        return F(f)
    return F(f) + (('' if abs(q) == 1 else str(abs(q))) + ('+' if q > 0 else '-')).translate(str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻'))


ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}
NAMED = [('FeCl2', 'iron(II) chloride'), ('FeCl3', 'iron(III) chloride'), ('Cu2O', 'copper(I) oxide'), ('CuO', 'copper(II) oxide'), ('PbO', 'lead(II) oxide'), ('PbO2', 'lead(IV) oxide'),
         ('MnO2', 'manganese(IV) oxide'), ('Cr2O3', 'chromium(III) oxide'), ('SnCl2', 'tin(II) chloride'), ('SnCl4', 'tin(IV) chloride'), ('FeSO4', 'iron(II) sulfate'), ('Fe2(SO4)3', 'iron(III) sulfate'),
         ('Cu(NO3)2', 'copper(II) nitrate'), ('CuCl', 'copper(I) chloride'), ('Fe(OH)2', 'iron(II) hydroxide'), ('Fe(OH)3', 'iron(III) hydroxide'), ('SO2', 'sulfur(IV) oxide'), ('SO3', 'sulfur(VI) oxide'),
         ('NO2', 'nitrogen(IV) oxide'), ('CoCl2', 'cobalt(II) chloride'), ('KMnO4', 'potassium manganate(VII)'), ('K2Cr2O7', 'potassium dichromate(VI)'), ('PbCl2', 'lead(II) chloride'),
         ('MnSO4', 'manganese(II) sulfate'), ('CrCl3', 'chromium(III) chloride'), ('Fe2O3', 'iron(III) oxide'), ('FeO', 'iron(II) oxide'), ('CuSO4', 'copper(II) sulfate')]

t10b = T('Oxidation numbers and Roman numerals in names of compounds', 'oxidation numbers', 'roman numerals in names of compounds')
t10b.fixed('C1', (1, 2), [
    ('What is the oxidation number of any uncombined element?', '0', 'Elements (e.g. O₂, Fe) have oxidation number 0.', ['+1', '−1', 'equal to its group number']),
    ('What is the usual oxidation number of oxygen in its compounds?', '−2', 'Oxygen is usually −2 (except peroxides).', ['+2', '−1', '0']),
    ('What does the Roman numeral in iron(III) chloride show?', 'the oxidation number of iron is +3', 'Roman numeral = oxidation number of the metal.', ['there are three chlorine atoms', 'there are three iron atoms', 'iron is in Group III']),
    ('In terms of oxidation number, what happens to a species that is oxidised?', 'Its oxidation number increases.', 'Oxidation: increase in oxidation number.', ['Its oxidation number decreases.', 'Its oxidation number stays the same.', 'It becomes zero.']),
    ('State the sum of the oxidation numbers in a neutral compound.', 'zero', '[1]'),
])
t10b.fixed('C2', (2, 3, 4), [
    ('Explain why the sum of the oxidation numbers in the sulfate ion, SO₄²⁻, is −2.', 'The sum of oxidation numbers in an ion equals the charge on the ion: S (+6) + 4 × O (−2) = −2.', '[2]'),
    ('Explain why Roman numerals are needed in the names of iron compounds but not in the names of sodium compounds.', 'Iron (a transition element) has variable oxidation numbers (+2 and +3), so the numeral shows which ion is present; sodium is always +1.', '[2]'),
    ('Explain, using oxidation numbers, why 2Fe²⁺ + Cl₂ → 2Fe³⁺ + 2Cl⁻ is a redox reaction.', 'Fe increases from +2 to +3 (oxidised); Cl decreases from 0 to −1 (reduced).', '[2]'),
    ('Explain how the name potassium manganate(VII) shows the oxidation number of manganese in KMnO₄.', 'The (VII) shows Mn is +7: +1 (K) + 7 + 4 × (−2) = 0.', '[2]'),
])


@t10b.add('C1', (1, 2, 3))
def t10b_on(r, D):
    f, q, el = r.choice(OXN)
    v = oxnum(f, q, el)
    if not isinstance(v, int):
        return None
    wrong = [-v, v + 2, v - 2, v + 1, abs(v) + 1, 0 if v else 2]
    return NM(r, f'What is the oxidation number of {el} in {sp(f, q)}?', v, wrong, '', f'Sum = {q}; using O = −2, H = +1 etc.: {el} = {v:+d}', f=lambda x: neg(f'{int(x):+d}') if x else '0')


@t10b.add('C3', (2, 3, 4))
def t10b_calc(r, D):
    k = 2 if D <= 2 else 3
    picks = r.sample(OXN, k)
    vals = [(f, q, el, oxnum(f, q, el)) for f, q, el in picks]
    if any(not isinstance(v, int) for *_, v in vals):
        return None
    stem = 'Deduce the oxidation number of the stated element in each species: ' + '; '.join(f'{el} in {sp(f, q)}' for f, q, el, v in vals) + '.'
    ans = '; '.join(f'{el} in {sp(f, q)}: {neg(f"{v:+d}") if v else "0"}' for f, q, el, v in vals)
    return Q(stem, ans, ans + f'. 1 mark each [{k}]', 'short')


@t10b.add('C1', (1, 2, 3))
def t10b_name(r, D):
    f, nm = r.choice(NAMED)
    if r.random() < 0.5:
        others = [x[1] for x in NAMED if x[0] != f]
        num = re.search(r'\((\w+)\)', nm).group(1)
        alt = [nm.replace(f'({num})', f'({x})') for x in ROMAN.values() if x != num][:4]
        return M(r, f'What is the name of the compound {F(f)}?', nm, alt + r.sample(others, 2), f'Oxidation number of the metal/element in {F(f)} gives the numeral: {nm}.')
    others = [F(x[0]) for x in NAMED if x[1] != nm and x[1].split('(')[0] == nm.split('(')[0]] + [F(x[0]) for x in r.sample(NAMED, 3) if x[1] != nm]
    return M(r, f'What is the formula of {nm}?', F(f), others, f'{nm}: {F(f)}.')


@t10b.add('C3', (3, 4, 5))
def t10b_redox(r, D):
    rx = r.choice([('2Fe2+(aq) + Cl2(aq) -> 2Fe3+(aq) + 2Cl-(aq)', [('Fe', '+2', '+3'), ('Cl', '0', '−1')], 'Fe²⁺', 'Cl₂'),
                   ('SO2 + 2H2S -> 3S + 2H2O', [('S in SO₂', '+4', '0'), ('S in H₂S', '−2', '0')], 'H₂S', 'SO₂'),
                   ('CuO + H2 -> Cu + H2O', [('Cu', '+2', '0'), ('H', '0', '+1')], 'H₂', 'CuO'),
                   ('2KI + Cl2 -> 2KCl + I2', [('I', '−1', '0'), ('Cl', '0', '−1')], 'KI (I⁻)', 'Cl₂'),
                   ('Fe2O3 + 3CO -> 2Fe + 3CO2', [('Fe', '+3', '0'), ('C', '+2', '+4')], 'CO', 'Fe₂O₃'),
                   ('MnO2 + 4HCl -> MnCl2 + Cl2 + 2H2O', [('Mn', '+4', '+2'), ('Cl', '−1', '0')], 'HCl', 'MnO₂'),
                   ('2SO2 + O2 -> 2SO3', [('S', '+4', '+6'), ('O', '0', '−2')], 'SO₂', 'O₂'),
                   ('Zn + Cu2+ -> Zn2+ + Cu', [('Zn', '0', '+2'), ('Cu', '+2', '0')], 'Zn', 'Cu²⁺')])
    e, chs, red_ag, ox_ag = rx
    disp = IE(e) if '+(' in e or '-(' in e or '2+' in e else E(e)
    stem = f'Use oxidation numbers to show that {disp} is a redox reaction. Identify the oxidising agent and the reducing agent.'
    ans = '; '.join(f'{a}: {b} → {c}' for a, b, c in chs) + f'. Oxidising agent: {ox_ag}; reducing agent: {red_ag}.'
    key = '; '.join(f'{a} {b} → {c}' for a, b, c in chs) + ' [2]; increase = oxidation, decrease = reduction [1]; agents [1]'
    return Q(stem, ans, key, 'short')


@t10b.add('C2', (2, 3, 4), 'explain')
def t10b_explain(r, D):
    f, nm = r.choice(NAMED)
    num = re.search(r'\((\w+)\)', nm).group(1)
    val = [k for k, v in ROMAN.items() if v == num][0]
    return Q(f'Explain how the name {nm} relates to the formula {F(f)}.', f'The numeral ({num}) is the oxidation number (+{val}) of the {nm.split("(")[0].split(" ")[-1]} in the compound; the other ions/atoms balance this so the total is zero.',
             '1 mark: numeral = oxidation number; 1 mark: charge balance shown [2]')


def _t10b_c4(r, D):
    f, nm = r.choice(NAMED[:16])
    p = person(r)
    sp1 = r.sample(OXN, 2)
    intro = f'{p} is given a bottle labelled {nm} and also studies the species {sp(sp1[0][0], sp1[0][1])} and {sp(sp1[1][0], sp1[1][1])}.'
    num = re.search(r'\((\w+)\)', nm).group(1)
    parts = [
        lambda r: ('Write the formula of the compound in the bottle.', F(f), '[1]'),
        lambda r: ('State what the Roman numeral in the name tells you.', f'the oxidation number of the metal/element is +{[k for k, v in ROMAN.items() if v == num][0]}', '[1]'),
        lambda r: (f'Deduce the oxidation number of {sp1[0][2]} in {sp(sp1[0][0], sp1[0][1])}.', str(oxnum(*sp1[0])), '[1]'),
        lambda r: (f'Deduce the oxidation number of {sp1[1][2]} in {sp(sp1[1][0], sp1[1][1])}.', str(oxnum(*sp1[1])), '[1]'),
        lambda r: ('Define oxidation in terms of oxidation number.', 'an increase in oxidation number', '[1]'),
        lambda r: ('State the rules you used to deduce oxidation numbers.', 'elements 0; O −2; H +1; sum = 0 for compounds or = charge for ions', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t10b.add('C4', (2, 3, 4, 5), 'multi_step')(_t10b_c4)


# ---------------------------------------------------------- 10.3 oxidising/reducing agents, tests
REDUCERS = [('iron(II) sulfate solution', 'Fe²⁺ is oxidised to Fe³⁺'), ('sulfur dioxide solution', 'SO₂ is oxidised to sulfate'), ('sodium sulfite solution', 'SO₃²⁻ is oxidised to SO₄²⁻'),
            ('potassium iodide solution', 'I⁻ is oxidised to I₂'), ('ethanol (warm)', 'ethanol is oxidised'), ('aqueous tin(II) chloride', 'Sn²⁺ is oxidised to Sn⁴⁺')]
OXIDISERS = [('chlorine water', 'Cl₂ is reduced to Cl⁻'), ('bromine water', 'Br₂ is reduced to Br⁻'), ('iron(III) chloride solution', 'Fe³⁺ is reduced to Fe²⁺'),
             ('acidified potassium dichromate(VI)', 'Cr₂O₇²⁻ is reduced to Cr³⁺'), ('acidified potassium manganate(VII)', 'MnO₄⁻ is reduced to Mn²⁺'), ('sodium chlorate(I) (bleach) solution', 'ClO⁻ is reduced to Cl⁻')]

t10c = T('Oxidising and reducing agents; tests with acidified potassium manganate(VII) and potassium iodide', 'oxidising and reducing agents', 'potassium manganate(vii)', 'potassium iodide')
t10c.fixed('C1', (1, 2), [
    ('What is an oxidising agent?', 'a substance that oxidises another substance and is itself reduced', 'It accepts electrons.', ['a substance that is oxidised', 'a substance that gives away electrons', 'a substance that contains oxygen']),
    ('What colour change is seen when acidified potassium manganate(VII) reacts with a reducing agent?', 'purple to colourless', 'MnO₄⁻ (purple) is reduced to Mn²⁺ (colourless).', ['colourless to purple', 'orange to green', 'colourless to brown']),
    ('What colour change is seen when aqueous potassium iodide reacts with an oxidising agent?', 'colourless to brown', 'I⁻ is oxidised to I₂ (brown in solution).', ['brown to colourless', 'purple to colourless', 'colourless to blue']),
    ('In the reaction CuO + H₂ → Cu + H₂O, what is the reducing agent?', 'hydrogen', 'H₂ removes oxygen from CuO and is itself oxidised.', ['copper(II) oxide', 'copper', 'water']),
    ('State the reagent used to test for a reducing agent.', 'acidified potassium manganate(VII)', '[1]'),
])
t10c.fixed('C2', (2, 3, 4), [
    ('Explain why potassium iodide is used to test for an oxidising agent.', 'An oxidising agent removes electrons from iodide ions, forming iodine; the colourless solution turns brown.', '[2]'),
    ('Explain why acidified potassium manganate(VII) turns colourless when sulfur dioxide is bubbled through it.', 'Sulfur dioxide is a reducing agent: it gives electrons to the manganate(VII) ions, reducing them from purple MnO₄⁻ to colourless Mn²⁺.', '[2]'),
    ('Explain why an oxidising agent is itself reduced.', 'It gains the electrons that it removes from the substance it oxidises.', '[2]'),
    ('Explain why a substance cannot be both an oxidising agent and the substance oxidised in the same reaction step.', 'The oxidising agent gains electrons (is reduced) while the substance oxidised loses electrons; one species cannot both gain and lose the same electrons.', '[2]'),
])


@t10c.add('C3', (1, 2, 3, 4))
def t10c_deduce(r, D):
    if r.random() < 0.5:
        s, why = r.choice(REDUCERS)
        obs = 'acidified potassium manganate(VII) changes from purple to colourless; aqueous potassium iodide shows no change'
        corr = 'reducing agent'
    else:
        s, why = r.choice(OXIDISERS)
        if 'manganate' in s:
            return None
        obs = 'aqueous potassium iodide changes from colourless to brown; acidified potassium manganate(VII) stays purple'
        corr = 'oxidising agent'
    lab_ = r.choice('ABCDEJKLMQRXYZ')
    if D <= 2:
        return M(r, f'Solution {lab_} is tested: {obs}. What does this show about {lab_}?', f'It is a {corr}.', ['It is a reducing agent.', 'It is an oxidising agent.', 'It is an acid.', 'It is an alkali.'],
                 f'{cap(obs)} → {corr}.')
    stem = f'{who(r)} tests solution {lab_} ({s}) with two reagents: {obs}. Deduce whether {lab_} is an oxidising or a reducing agent and explain the colour change in terms of electron transfer.'
    ans = f'{cap(corr)}. ' + (f'{why}: {lab_} gives electrons to MnO₄⁻ ions, which are reduced to colourless Mn²⁺.' if corr == 'reducing agent' else f'{why}: {lab_} takes electrons from I⁻ ions, which are oxidised to brown I₂.')
    key = '1 mark: correct deduction; 1 mark: identifies the colour change; 1 mark: electron transfer explanation [3]'
    if D >= 4:
        stem += ' Write the half-equation for the change in the test reagent.' if corr == 'oxidising agent' else ' State the change in oxidation number of manganese.'
        ans += ' 2I⁻ → I₂ + 2e⁻' if corr == 'oxidising agent' else ' Mn: +7 → +2.'
        key = key.replace(' [3]', '; 1 mark: half-equation / oxidation number change [4]')
    return Q(stem, ans, key, 'short')


@t10c.add('C1', (1, 2, 3))
def t10c_agent(r, D):
    if r.random() < 0.5:
        e, ox, red, oa, ra = r.choice(REDOX_O)
        want = r.choice(['oxidising agent', 'reducing agent'])
        corr = oa if want == 'oxidising agent' else ra
        return M(r, f'In the reaction {E(e)}, what is the {want}?', corr, [ox, red, 'oxygen', 'the metal formed'], f'Oxidising agent: {oa} (reduced); reducing agent: {ra} (oxidised).')
    e, ox, red, h1, h2 = r.choice(REDOX_E)
    want = r.choice(['oxidising agent', 'reducing agent'])
    corr = red if want == 'oxidising agent' else ox
    return M(r, f'In the reaction {e}, what is the {want}?', corr, [ox, red, 'the electrons', 'water'], f'{ox} loses electrons (reducing agent); {red} gains electrons (oxidising agent).')


@t10c.add('C2', (2, 3, 4), 'explain')
def t10c_explain(r, D):
    e, ox, red, h1, h2 = r.choice(REDOX_E)
    return Q(f'In the reaction {e}, explain which species is the oxidising agent and which is the reducing agent.', f'{red} is the oxidising agent: it gains electrons ({h2}) and is reduced. {ox} is the reducing agent: it loses electrons ({h1}) and is oxidised.',
             '1 mark: oxidising agent with reason; 1 mark: reducing agent with reason [2]' if D <= 3 else '1 mark: oxidising agent; 1 mark: reducing agent; 1 mark: half-equations or electron explanation [3]')


def _t10c_c4(r, D):
    red_, why1 = r.choice(REDUCERS[:3])
    oxi, why2 = r.choice([o for o in OXIDISERS if 'manganate' not in o[0]])
    p = person(r)
    intro = f'{p} has two unlabelled solutions, P and Q. One is {red_} and the other is {oxi}. Acidified potassium manganate(VII) and aqueous potassium iodide are available.'
    parts = [
        lambda r: ('Describe how the two reagents can be used to identify which solution is the reducing agent.', 'add acidified KMnO₄: the reducing agent turns it from purple to colourless', '1 mark reagent; 1 mark colour change [2]'),
        lambda r: ('Describe the result expected when aqueous potassium iodide is added to the oxidising agent.', 'colourless to brown (iodine formed)', '[1]'),
        lambda r: ('Explain the colour change with potassium iodide in terms of electrons.', 'the oxidising agent removes electrons from iodide ions: 2I⁻ → I₂ + 2e⁻', '[2]'),
        lambda r: ('State what happens to the oxidation number of manganese when manganate(VII) reacts with the reducing agent.', 'decreases from +7 to +2 (reduced)', '[1]'),
        lambda r: (f'Explain why {red_} is described as a reducing agent.', f'{why1}: it loses electrons and reduces the other substance', '[2]'),
        lambda r: ('Suggest why the potassium manganate(VII) must be acidified.', 'H⁺ ions are needed for the reduction of MnO₄⁻ to Mn²⁺', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


t10c.add('C4', (2, 3, 4, 5), 'case')(_t10c_c4)
t10c.add('C3', (4, 5), 'case')(_t10c_c4)

CHAPTERS[10] = [t10a, t10b, t10c]


# ===================================================================== Ch11 Acids and bases
PH = [('dilute hydrochloric acid', 1), ('stomach acid', 2), ('lemon juice', 2), ('vinegar', 3), ('cola drink', 3), ('orange juice', 4), ('black coffee', 5), ('rain water', 6), ('milk', 6),
      ('pure water', 7), ('sodium chloride solution', 7), ('sea water', 8), ('baking soda solution', 9), ('toothpaste', 9), ('milk of magnesia', 10), ('soap solution', 10), ('aqueous ammonia', 11),
      ('bleach', 12), ('limewater', 12), ('oven cleaner', 13), ('dilute sodium hydroxide', 14), ('tomato juice', 4), ('sodium hydrogencarbonate solution', 8)]


def ui(ph):
    if ph <= 3:
        return 'red'
    if ph <= 5:
        return 'orange'
    if ph < 7:
        return 'yellow'
    if ph < 7.5:
        return 'green'
    if ph <= 10:
        return 'blue'
    return 'purple (violet)'


def ph_class(ph):
    if ph <= 3:
        return 'strongly acidic'
    if ph < 7:
        return 'weakly acidic'
    if ph < 7.5:
        return 'neutral'
    if ph <= 10:
        return 'weakly alkaline'
    return 'strongly alkaline'


IND = {'litmus': ('red', 'blue'), 'methyl orange': ('red', 'yellow'), 'thymolphthalein': ('colourless', 'blue')}

t11a = T('Properties of acids and alkalis: indicators, pH scale and universal indicator', 'properties of acids and alkalis', 'indicators, ph scale and universal indicator')
t11a.fixed('C1', (1, 2), [
    ('What colour is thymolphthalein in an alkaline solution?', 'blue', 'Thymolphthalein: colourless in acid, blue in alkali.', ['colourless', 'red', 'yellow']),
    ('What colour is methyl orange in an acidic solution?', 'red', 'Methyl orange: red in acid, yellow in alkali.', ['yellow', 'blue', 'colourless']),
    ('Which pH value is neutral?', '7', 'pH 7 is neutral at 25 °C.', ['0', '1', '14']),
    ('What is an alkali?', 'a soluble base', 'Alkalis dissolve in water and produce OH⁻ ions.', ['any substance with pH below 7', 'an insoluble metal oxide', 'a substance that produces H⁺ ions']),
    ('Which colour does universal indicator turn in a solution of pH 1?', 'red', 'Strong acids give red with universal indicator.', ['green', 'blue', 'purple']),
    ('State the colour of litmus in acidic and in alkaline solutions.', 'acid: red; alkali: blue', '[2]'),
])
t11a.fixed('C2', (2, 3, 4), [
    ('Explain why universal indicator is more useful than litmus for comparing two acids.', 'Universal indicator shows a range of colours corresponding to pH values, so it shows how acidic each solution is; litmus only shows acid or alkali.', '[2]'),
    ('Explain why a pH meter can give more precise results than universal indicator paper.', 'It gives a numerical reading (often to 0.01) rather than relying on judging a colour against a chart.', '[2]'),
    ('Describe how to measure the pH of a solution using universal indicator paper.', 'Use a clean glass rod to put a drop of the solution on the paper; compare the colour with the pH colour chart.', '[2]'),
    ('Explain the difference between a base and an alkali.', 'A base is any substance that neutralises an acid (e.g. a metal oxide or hydroxide); an alkali is a base that dissolves in water.', '[2]'),
])


@t11a.add('C1', (1, 2, 3))
def t11a_colour(r, D):
    nm, ph = r.choice(PH)
    if r.random() < 0.5:
        return M(r, f'A sample of {nm} has a pH of {ph:g}. What colour does universal indicator turn?', ui(ph), ['red', 'orange', 'yellow', 'green', 'blue', 'purple (violet)'], f'pH {ph:g} → {ui(ph)} ({ph_class(ph)}).')
    ind = r.choice(list(IND))
    acid = ph < 7
    if ph == 7 or ph == 7.4:
        return None
    col = IND[ind][0] if acid else IND[ind][1]
    return M(r, f'What colour is {ind} in {nm} (pH {ph:g})?', col, ['red', 'blue', 'yellow', 'colourless', 'purple', 'green'], f'{cap(ind)}: {IND[ind][0]} in acid, {IND[ind][1]} in alkali.')


@t11a.add('C3', (1, 2, 3, 4))
def t11a_table(r, D):
    k = 3 if D <= 2 else 4
    sols = r.sample(PH, k)
    if len({p for _, p in sols}) < k:
        return None
    labs = 'ABCD'
    rows = '; '.join(f'{labs[i]}: {nm} turns universal indicator {ui(ph)}' for i, (nm, ph) in enumerate(sols))
    if D == 1:
        most = min(sols, key=lambda x: x[1])
        if [ui(p) for _, p in sols].count(ui(most[1])) > 1:
            return None
        return M(r, f'Universal indicator is added to {k} solutions. {rows}. Which solution is the most acidic?', labs[sols.index(most)], list(labs[:k]) + ['none of them'], f'Red/orange = lowest pH → {labs[sols.index(most)]}.')
    stem = f'Universal indicator is added to {k} solutions. {rows}. Suggest a pH for each and classify each as strongly acidic, weakly acidic, neutral, weakly alkaline or strongly alkaline. State which solution would turn thymolphthalein blue.'
    blue = [labs[i] for i, (nm, ph) in enumerate(sols) if ph > 9.5]
    ans = '; '.join(f'{labs[i]}: pH ≈ {ph:g}, {ph_class(ph)}' for i, (nm, ph) in enumerate(sols)) + f'. Thymolphthalein blue: {", ".join(blue) if blue else "none (no strongly alkaline solution)"}'
    return Q(stem, ans, ans + f'. 1 mark per solution [{k}]; thymolphthalein [1]', 'short')


@t11a.add('C2', (2, 3, 4), 'explain')
def t11a_explain(r, D):
    (n1, p1), (n2, p2) = r.sample(PH, 2)
    if p1 == p2:
        return None
    return Q(f'{person(r)} tests {n1} and {n2} with universal indicator: they turn {ui(p1)} and {ui(p2)} respectively. Suggest the pH of each and explain what the colours show about the solutions.',
             f'{n1}: pH ≈ {p1:g} ({ph_class(p1)}); {n2}: pH ≈ {p2:g} ({ph_class(p2)}). ' + ('The lower pH solution has a higher concentration of H⁺ ions.' if min(p1, p2) < 7 else 'The higher pH solution has a higher concentration of OH⁻ ions.'),
             '1 mark: both pH values; 1 mark: classification; ' + ('1 mark: link to H⁺/OH⁻ concentration [3]' if D >= 3 else 'total [2]'))


def _t11a_c4(r, D):
    sols = r.sample(PH, 4)
    p = person(r)
    intro = f'{p} tests four household and laboratory solutions from a kitchen in {city(r)}: ' + ', '.join(nm for nm, _ in sols) + '.'
    parts = [
        lambda r: ('Predict the colour of universal indicator in each solution.', '; '.join(f'{nm}: {ui(ph)}' for nm, ph in sols), '1 mark per two correct [2]'),
        lambda r: ('Identify any solutions that are alkaline and state the ion responsible.', ', '.join(nm for nm, ph in sols if ph > 7.4) + ' – OH⁻ ions' if any(ph > 7.4 for _, ph in sols) else 'none are alkaline; alkalis contain OH⁻ ions', '[2]'),
        lambda r: ('State the colour of methyl orange in the most acidic solution.', 'red' if min(ph for _, ph in sols) < 7 else 'yellow', '[1]'),
        lambda r: ('Describe how a more precise pH value could be obtained.', 'use a calibrated pH meter / probe', '[1]'),
        lambda r: ('Explain the difference between an alkali and a base.', 'alkali is a soluble base', '[1]'),
        lambda r: ('Suggest which solution could be used to treat a bee sting (acidic) and why.', next((nm for nm, ph in sols if 7.5 < ph <= 10), 'a weak alkali such as baking soda') + ': a weak alkali neutralises the acid without damaging skin', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t11a.add('C4', (2, 3, 4, 5), 'multi_step')(_t11a_c4)


# ---------------------------------------------------------- 11.2 proton donors / acceptors, strong and weak
PT = [('HCl(g) + NH₃(g) → NH₄Cl(s)', 'HCl', 'NH₃'), ('HCl(g) + H₂O(l) → H₃O⁺(aq) + Cl⁻(aq)', 'HCl', 'H₂O'), ('NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + OH⁻(aq)', 'H₂O', 'NH₃'),
      ('H⁺(aq) + OH⁻(aq) → H₂O(l)', 'H⁺', 'OH⁻'), ('CH₃COOH(aq) + H₂O(l) ⇌ CH₃COO⁻(aq) + H₃O⁺(aq)', 'CH₃COOH', 'H₂O'), ('2H⁺(aq) + CO₃²⁻(aq) → H₂O(l) + CO₂(g)', 'H⁺', 'CO₃²⁻'),
      ('HNO₃(aq) + NH₃(aq) → NH₄⁺(aq) + NO₃⁻(aq)', 'HNO₃', 'NH₃'), ('CuO(s) + 2H⁺(aq) → Cu²⁺(aq) + H₂O(l)', 'H⁺', 'CuO (the O²⁻ ion)'), ('H₂SO₄(aq) + 2OH⁻(aq) → SO₄²⁻(aq) + 2H₂O(l)', 'H₂SO₄', 'OH⁻'),
      ('HBr(g) + H₂O(l) → H₃O⁺(aq) + Br⁻(aq)', 'HBr', 'H₂O')]
STRONG = [('hydrochloric acid', 'HCl', 'HCl → H⁺ + Cl⁻'), ('nitric acid', 'HNO₃', 'HNO₃ → H⁺ + NO₃⁻'), ('sulfuric acid', 'H₂SO₄', 'H₂SO₄ → 2H⁺ + SO₄²⁻')]
WEAK = [('ethanoic acid', 'CH₃COOH'), ('citric acid', 'citric acid'), ('carbonic acid', 'H₂CO₃'), ('methanoic acid', 'HCOOH')]
WEAK_PH = {0.1: 2.9, 0.01: 3.4, 1.0: 2.4, 0.5: 2.5}
STRONG_PH = {0.1: 1.0, 0.01: 2.0, 1.0: 0.0, 0.5: 0.3}

t11b = T('Acids as proton donors and bases as proton acceptors; strong and weak acids', 'proton donors', 'proton acceptors', 'strong and weak acids')
t11b.fixed('C1', (1, 2), [
    ('What is an acid, according to the proton definition?', 'a proton (H⁺) donor', 'Acids donate H⁺ ions.', ['a proton acceptor', 'an electron donor', 'a hydroxide ion donor']),
    ('What is a base, according to the proton definition?', 'a proton (H⁺) acceptor', 'Bases accept H⁺ ions.', ['a proton donor', 'an electron acceptor', 'a substance with pH below 7']),
    ('Which acid is a weak acid?', 'ethanoic acid', 'Ethanoic acid only partially dissociates.', ['hydrochloric acid', 'nitric acid', 'sulfuric acid']),
    ('What is meant by a strong acid?', 'an acid that is completely dissociated into ions in aqueous solution', 'Strong = fully ionised.', ['a concentrated acid', 'an acid with a pH of 7', 'an acid that does not ionise']),
    ('Which ion is present in all aqueous solutions of acids?', 'H⁺', 'Acids produce H⁺(aq).', ['OH⁻', 'Cl⁻', 'Na⁺']),
    ('State the ion present in excess in all alkaline solutions.', 'OH⁻ (hydroxide)', '[1]'),
])
t11b.fixed('C2', (2, 3, 4), [
    ('Explain the difference between a strong acid and a concentrated acid.', 'Strength refers to the degree of dissociation (strong = fully ionised); concentration refers to how much acid is dissolved per dm³. A weak acid can be concentrated.', '[2]'),
    ('Explain why 0.1 mol/dm³ ethanoic acid has a higher pH than 0.1 mol/dm³ hydrochloric acid.', 'Ethanoic acid is weak and only partially dissociates, so the concentration of H⁺ ions is lower, giving a higher pH.', '[2]'),
    ('Explain why magnesium reacts more slowly with ethanoic acid than with hydrochloric acid of the same concentration.', 'Ethanoic acid is only partially ionised, so the concentration of H⁺ ions is lower and collisions between H⁺ and Mg are less frequent.', '[2]'),
    ('Explain why ammonia is described as a base when it reacts with hydrogen chloride.', 'Ammonia accepts a proton (H⁺) from HCl to form the ammonium ion, NH₄⁺.', '[2]'),
    ('Write equations to show the difference in dissociation of hydrochloric acid and ethanoic acid.', 'HCl → H⁺ + Cl⁻ (complete); CH₃COOH ⇌ CH₃COO⁻ + H⁺ (partial, reversible).', '[2]'),
])


@t11b.add('C1', (1, 2, 3))
def t11b_pt(r, D):
    e, don, acc = r.choice(PT)
    want = r.choice(['proton donor (acid)', 'proton acceptor (base)'])
    corr = don if 'donor' in want else acc
    pool = [don, acc] + [x for x in re.findall(r'[A-Z][A-Za-z₀-₉⁺⁻²³]*', e) if x not in (don, acc)][:3] + ['the electrons']
    return M(r, f'In the reaction {e}, which species acts as the {want}?', corr, pool, f'{don} donates H⁺; {acc} accepts H⁺.')


@t11b.add('C3', (2, 3, 4, 5))
def t11b_compare(r, D):
    s = r.choice(STRONG[:2])  # monoprotic only: pH values and H2 volume comparison assume HA
    w = WEAK[0]
    c = r.choice([0.1, 0.01, 1.0, 0.5])
    p = person(r)
    t_s = r.choice([20, 25, 30, 40])
    t_w = t_s * r.choice([4, 5, 6, 8])
    intro = (f'{p} compares {sf(c)} mol/dm³ {s[0]} with {sf(c)} mol/dm³ {w[0]}. Results: pH – {s[0]} {STRONG_PH[c]:.1f}, {w[0]} {WEAK_PH[c]:.1f}; time for a 2 cm piece of magnesium ribbon to react – '
             f'{s[0]} {t_s} s, {w[0]} {t_w} s; electrical conductivity – {s[0]} high, {w[0]} low.')
    dph = WEAK_PH[c] - STRONG_PH[c]
    parts = [
        lambda r: ('Explain the difference in pH.', f'{s[0]} is a strong acid, fully dissociated; {w[0]} is weak, partially dissociated, so lower [H⁺]', '1 mark: strong fully dissociated; 1 mark: weak partially so lower [H⁺] [2]'),
        lambda r: ('Explain why magnesium reacts faster with the strong acid.', 'higher concentration of H⁺ ions, so more frequent collisions', '[2]'),
        lambda r: ('Explain the difference in conductivity.', 'more ions in the strong acid solution to carry charge', '[1]'),
        lambda r: (f'Write an equation for the dissociation of {w[0]}.', 'CH₃COOH ⇌ CH₃COO⁻ + H⁺' if 'ethanoic' in w[0] else 'HCOOH ⇌ HCOO⁻ + H⁺', '[1]'),
        lambda r: (f'Calculate how many times greater the H⁺ concentration is in the {s[0]}, using the pH values.', f'about {sf(10 ** dph, 2)} times', f'pH difference {dph:.1f}; each unit = factor 10 → 10^{dph:.1f} ≈ {sf(10 ** dph, 2)} [2]'),
        lambda r: ('Predict whether the same total volume of hydrogen would be produced if excess magnesium were used with equal volumes of each acid. Explain.', 'yes: same number of moles of acid; the weak acid continues to dissociate as H⁺ is used up', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@t11b.add('C3', (1, 2, 3))
def t11b_factor(r, D):
    p1 = r.choice(range(1, 7))
    d = r.choice([1, 2, 3]) if p1 + 3 <= 7 else r.choice([1, 2])
    p2 = p1 + d
    f = 10 ** d
    if D == 1:
        return NM(r, f'Solution X has a pH of {p1} and solution Y has a pH of {p2}. How many times greater is the hydrogen ion concentration in X than in Y?', f, [d, 2 * d, f / 10 if d > 1 else 2, f * 10, d * 10 if d > 1 else 5], '',
                  f'Each pH unit is a factor of 10: 10^{d} = {f}.', f=lambda x: f'{int(x):,}' if x >= 1 else str(x))
    return Q(f'The pH of an acid solution increases from {p1} to {p2} when it is diluted. Describe how the hydrogen ion concentration changes, giving the factor.', f'It decreases by a factor of {f:,} (10 for each pH unit).',
             f'1 mark: decreases; 1 mark: factor 10^{d} = {f:,} [2]', 'short')


@t11b.add('C2', (2, 3, 4), 'explain')
def t11b_explain(r, D):
    e, don, acc = r.choice(PT)
    return Q(f'Explain, in terms of proton transfer, which species is the acid and which is the base in the reaction {e}.', f'{don} is the acid because it donates a proton (H⁺); {acc} is the base because it accepts the proton.',
             '1 mark: acid identified as proton donor; 1 mark: base identified as proton acceptor [2]')


def _t11b_c4(r, D):
    s = r.choice(STRONG)
    w = WEAK[0]
    p = person(r)
    intro = r.choice([f'A cleaning company in {city(r)} must choose between {s[0]} and ethanoic acid (vinegar) for removing limescale (calcium carbonate).', f'{p} investigates the differences between {s[0]} and ethanoic acid of the same concentration.'])
    parts = [
        lambda r: ('Define a strong acid and a weak acid.', 'strong: completely dissociated in water; weak: partially dissociated', '[2]'),
        lambda r: (f'Write equations to show the dissociation of {s[0]} and of ethanoic acid.', f'{s[2]} (complete); CH₃COOH ⇌ CH₃COO⁻ + H⁺ (partial)', '1 mark each [2]'),
        lambda r: ('Predict which acid has the lower pH at the same concentration and explain why.', f'{s[0]}: higher [H⁺] because fully dissociated', '[2]'),
        lambda r: ('Write the ionic equation for the reaction of an acid with calcium carbonate.', 'CaCO₃(s) + 2H⁺(aq) → Ca²⁺(aq) + H₂O(l) + CO₂(g)', '[2]'),
        lambda r: ('Identify the proton donor and the proton acceptor in that reaction.', 'H⁺ (from the acid) donor; carbonate ion acceptor', '[1]'),
        lambda r: ('Evaluate which acid is better for the cleaning company.', 'strong acid works faster but is more corrosive/hazardous; ethanoic acid is safer for surfaces and users but slower – justified choice', '1 mark each side; 1 mark conclusion [3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='long')


t11b.add('C4', (2, 3, 4, 5), 'long')(_t11b_c4)


# ---------------------------------------------------------- 11.3 reactions of acids
ACID_RX = []
for _c, _a, _bases in EXCESS:
    for _b, _k in _bases:
        ACID_RX.append((_c, _a, _b, _k))


def prods_of(kind):
    return {'oxide': 'salt + water', 'carbonate': 'salt + water + carbon dioxide', 'metal': 'salt + hydrogen', 'hydroxide': 'salt + water'}[kind]


def obs_of(kind):
    return {'oxide': 'the solid dissolves, forming a solution (coloured if a copper/iron salt)', 'carbonate': 'fizzing (effervescence) as carbon dioxide is given off; the solid dissolves',
            'metal': 'fizzing as hydrogen is given off; the metal gets smaller', 'hydroxide': 'the solid dissolves'}[kind]


t11c = T('Typical reactions of acids with metals, bases and carbonates; neutralisation', 'typical reactions of acids', 'metals, bases and carbonates', 'neutralisation')
t11c.fixed('C1', (1, 2), [
    ('What are the products when a metal reacts with a dilute acid?', 'a salt and hydrogen', 'Metal + acid → salt + hydrogen.', ['a salt and water', 'a salt, water and carbon dioxide', 'an oxide and hydrogen']),
    ('Which gas is produced when a carbonate reacts with an acid?', 'carbon dioxide', 'Carbonate + acid → salt + water + CO₂.', ['hydrogen', 'oxygen', 'chlorine']),
    ('Which salt is formed when zinc oxide reacts with sulfuric acid?', 'zinc sulfate', 'Sulfuric acid gives sulfates.', ['zinc chloride', 'zinc sulfide', 'zinc nitrate']),
    ('What is formed in every neutralisation reaction between an acid and an alkali?', 'water', 'H⁺ + OH⁻ → H₂O.', ['hydrogen', 'carbon dioxide', 'oxygen']),
    ('What is formed when an alkali is warmed with an ammonium salt?', 'ammonia gas', 'NH₄⁺ + OH⁻ → NH₃ + H₂O.', ['hydrogen gas', 'nitrogen gas', 'carbon dioxide']),
    ('State the general word equation for the reaction of an acid with a base.', 'acid + base → salt + water', '[1]'),
])
t11c.fixed('C2', (2, 3, 4), [
    ('Explain how the name of the salt formed in an acid reaction depends on the acid used.', 'The acid provides the anion: hydrochloric acid → chlorides, sulfuric acid → sulfates, nitric acid → nitrates; the metal or base provides the cation.', '[2]'),
    ('Explain why copper does not react with dilute hydrochloric acid but magnesium does.', 'Copper is below hydrogen in the reactivity series, so it cannot displace hydrogen from the acid; magnesium is above hydrogen.', '[2]'),
    ('Describe a test to show that a gas given off when an acid reacts with a solid is carbon dioxide.', 'Bubble the gas through limewater; it turns milky (cloudy white).', '[2]'),
    ('Explain why farmers add calcium hydroxide (slaked lime) to acidic soil.', 'It is a base that neutralises the excess acid in the soil, raising the pH so crops grow better.', '[2]'),
])


@t11c.add('C1', (1, 2, 3))
def t11c_salt(r, D):
    c, a, b, kind = r.choice(ACID_RX)
    sname = salt_n(c, a)
    acid = ACID[a][0]
    pool = [salt_n(c, x) for x in ('Cl', 'SO4', 'NO3') if x != a] + [f'{CAT[c][0]} {"sulfide" if a == "SO4" else "oxide"}', salt_n(c, 'CO3') if kind != 'carbonate' else f'{CAT[c][0]} hydroxide']
    if D <= 2:
        return M(r, f'{cap(base_name(c, kind))} reacts with {acid}. Which salt is formed?', sname, pool, f'{E(excess_eq(c, a, b, kind))}')
    return M(r, f'{cap(base_name(c, kind))} reacts with {acid}. What are the products?', f'{sname} + {prods_of(kind).split(" + ", 1)[1]}',
             [f'{sname} + {x}' for x in ('water', 'water + carbon dioxide', 'hydrogen', 'hydrogen + water') if x != prods_of(kind).split(" + ", 1)[1]], f'{prods_of(kind)}: {E(excess_eq(c, a, b, kind))}.')


@t11c.add('C3', (2, 3, 4, 5))
def t11c_eq(r, D):
    c, a, b, kind = r.choice(ACID_RX)
    eq = excess_eq(c, a, b, kind)
    acid = ACID[a][0]
    p = person(r)
    stem = f'{p} adds {base_name(c, kind)} to {acid}. Describe what is observed, name the products and write the balanced symbol equation.'
    ans = f'{cap(obs_of(kind))}. Products: {salt_n(c, a)} and {prods_of(kind).split(" + ", 1)[1].replace(" + ", " and ")}. {E(eq)}'
    key = f'observation [1]; products named [1]; {E(eq)}: formulae [1], balanced [1]'
    if D >= 4:
        stem += ' Write the ionic equation for the reaction.'
        H = '2H⁺(aq)'
        ion = {'oxide': f'{F(b)}(s) + {H} → {ionf(CAT[c][1], 2)}(aq) + H₂O(l)', 'carbonate': f'{F(b)}(s) + {H} → {ionf(CAT[c][1], 2)}(aq) + H₂O(l) + CO₂(g)',
               'metal': f'{F(b)}(s) + {H} → {ionf(CAT[c][1], 2)}(aq) + H₂(g)', 'hydroxide': f'{F(b)}(s) + {H} → {ionf(CAT[c][1], 2)}(aq) + 2H₂O(l)'}[kind]
        ans += f'; ionic: {ion}'
        key += f'; ionic equation {ion} [1]'
    if D == 2:
        return Q(f'Name the products formed when {base_name(c, kind)} reacts with {acid}, and describe one observation.', f'{salt_n(c, a)} and {prods_of(kind).split(" + ", 1)[1].replace(" + ", " and ")}; {obs_of(kind)}',
                 'products [1]; observation [1]', 'short')
    return Q(stem, ans, key, 'short')


@t11c.add('C3', (3, 4, 5))
def t11c_neut(r, D):
    alk, an, _, _ = r.choice(ALK)
    a = r.choice(list(ACID))
    eq, ratio = neut_eq(alk, a)
    c = r.choice([0.1, 0.2, 0.5, 1.0])
    V = r.choice([20.0, 25.0, 50.0])
    n_alk = c * V / 1000
    n_acid = n_alk / ratio
    ca = r.choice([0.1, 0.2, 0.25, 0.5])
    Va = n_acid / ca * 1000
    if not (10 <= Va <= 50):
        return None
    stem = f'{sf(V, 3)} cm³ of {sf(c)} mol/dm³ {an} is exactly neutralised by {ACID[a][0]} of concentration {sf(ca)} mol/dm³. {E(eq)}. Calculate the volume of acid needed and name the salt formed.'
    salt = {'NaOH': 'sodium', 'KOH': 'potassium', 'NH3': 'ammonium'}[alk] + ' ' + AN[a][0]
    return Q(stem, f'{g3(Va)} cm³; {salt}', f'n(alkali) = {g3(n_alk)} mol [1]; n(acid) = {g3(n_acid)} mol (ratio {ratio}:1) [1]; V = {g3(Va)} cm³ [1]; salt {salt} [1]', 'numerical')


@t11c.add('C2', (2, 3, 4), 'explain')
def t11c_explain(r, D):
    c, a, b, kind = r.choice(ACID_RX)
    acid = ACID[a][0]
    return Q(f'Explain how you could tell, from observations alone, whether a white solid added to {acid} is a metal carbonate or a metal oxide.',
             'A carbonate fizzes (effervescence) because CO₂ is produced, which turns limewater milky; an oxide dissolves without fizzing (only salt + water).',
             '1 mark: carbonate fizzes / CO₂; 1 mark: oxide no gas; ' + ('1 mark: limewater test [3]' if D >= 3 else 'total [2]'))


def _t11c_c4(r, D):
    c, a, b, kind = r.choice(ACID_RX)
    acid = ACID[a][0]
    eq = excess_eq(c, a, b, kind)
    p = person(r)
    intro = r.choice([f'{p} adds an excess of {base_name(c, kind)} to warm {acid} to make crystals of {salt_n(c, a)}.', f'In {lab(r)}, {salt_n(c, a)} is made by reacting {base_name(c, kind)} with {acid}.'])
    parts = [
        lambda r: ('Describe what is observed during the reaction.', obs_of(kind), '[1]'),
        lambda r: ('Write the balanced symbol equation, with state symbols.', E(eq.replace(' + ', ' + ')), '1 mark formulae; 1 mark balancing [2]'),
        lambda r: ('Explain why an excess of the solid is used.', 'to make sure all the acid reacts; excess removed by filtration', '[2]'),
        lambda r: ('Describe how pure, dry crystals are obtained.', 'filter; heat filtrate to crystallisation point; cool; filter and dry crystals', '[3]'),
        lambda r: ('Describe a test for the gas produced.' if kind in ('carbonate', 'metal') else 'Explain why no gas is produced.',
                   'limewater turns milky (CO₂)' if kind == 'carbonate' else ('lighted splint – squeaky pop (H₂)' if kind == 'metal' else 'a base reacts with acid to give only salt and water'), '[1]'),
        lambda r: ('Identify the ion responsible for the acidic properties of the acid.', 'H⁺(aq)', '[1]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t11c.add('C4', (2, 3, 4, 5), 'multi_step')(_t11c_c4)


# ---------------------------------------------------------- 11.4 oxides
OXIDES = [('Na2O', 'sodium oxide', 'basic'), ('MgO', 'magnesium oxide', 'basic'), ('CaO', 'calcium oxide', 'basic'), ('CuO', 'copper(II) oxide', 'basic'), ('K2O', 'potassium oxide', 'basic'),
          ('Fe2O3', 'iron(III) oxide', 'basic'), ('Li2O', 'lithium oxide', 'basic'), ('Al2O3', 'aluminium oxide', 'amphoteric'), ('ZnO', 'zinc oxide', 'amphoteric'),
          ('CO2', 'carbon dioxide', 'acidic'), ('SO2', 'sulfur dioxide', 'acidic'), ('SO3', 'sulfur trioxide', 'acidic'), ('P4O10', 'phosphorus(V) oxide', 'acidic'), ('NO2', 'nitrogen dioxide', 'acidic'),
          ('SiO2', 'silicon(IV) oxide', 'acidic'), ('CO', 'carbon monoxide', 'neutral'), ('NO', 'nitrogen monoxide', 'neutral'), ('N2O', 'dinitrogen oxide', 'neutral')]
OX_DEF = {'basic': 'reacts with acids (but not alkalis) to form a salt and water; oxides of metals are usually basic', 'acidic': 'reacts with alkalis (but not acids) to form a salt and water; oxides of non-metals are usually acidic',
          'amphoteric': 'reacts with both acids and alkalis to form a salt and water', 'neutral': 'reacts with neither acids nor alkalis'}
OX_EQ = {'MgO': 'MgO(s) + 2HCl(aq) -> MgCl2(aq) + H2O(l)', 'CaO': 'CaO(s) + 2HCl(aq) -> CaCl2(aq) + H2O(l)', 'CuO': 'CuO(s) + H2SO4(aq) -> CuSO4(aq) + H2O(l)', 'Na2O': 'Na2O(s) + 2HCl(aq) -> 2NaCl(aq) + H2O(l)',
         'CO2': 'CO2(g) + 2NaOH(aq) -> Na2CO3(aq) + H2O(l)', 'SO2': 'SO2(g) + 2NaOH(aq) -> Na2SO3(aq) + H2O(l)', 'SO3': 'SO3(g) + 2NaOH(aq) -> Na2SO4(aq) + H2O(l)',
         'ZnO': 'ZnO(s) + 2HCl(aq) -> ZnCl2(aq) + H2O(l)', 'Al2O3': 'Al2O3(s) + 6HCl(aq) -> 2AlCl3(aq) + 3H2O(l)', 'Fe2O3': 'Fe2O3(s) + 6HCl(aq) -> 2FeCl3(aq) + 3H2O(l)', 'K2O': 'K2O(s) + 2HNO3(aq) -> 2KNO3(aq) + H2O(l)'}
for _e in OX_EQ.values():
    assert balanced(_e), _e

t11d = T('Acidic, basic and amphoteric oxides', 'acidic, basic and amphoteric oxides', 'amphoteric')
t11d.fixed('C1', (1, 2), [
    ('Which oxide is amphoteric?', 'zinc oxide', 'ZnO reacts with both acids and alkalis.', ['magnesium oxide', 'sulfur dioxide', 'sodium oxide']),
    ('Which type of oxide is formed by most non-metals?', 'acidic', 'Non-metal oxides react with alkalis.', ['basic', 'amphoteric', 'neutral']),
    ('Which oxide reacts with dilute hydrochloric acid but not with aqueous sodium hydroxide?', 'calcium oxide', 'Basic oxide.', ['carbon dioxide', 'aluminium oxide', 'sulfur trioxide']),
    ('Which oxide is neutral?', 'carbon monoxide', 'CO reacts with neither acids nor alkalis.', ['carbon dioxide', 'zinc oxide', 'copper(II) oxide']),
    ('What is an amphoteric oxide?', 'an oxide that reacts with both acids and bases to form a salt and water', 'Al₂O₃ and ZnO.', ['an oxide that reacts with neither acids nor bases', 'an oxide of a non-metal', 'an oxide that dissolves in water']),
    ('Name the two amphoteric oxides you should know.', 'aluminium oxide and zinc oxide', '[2]'),
])
t11d.fixed('C2', (2, 3, 4), [
    ('Explain why sulfur dioxide is classified as an acidic oxide.', 'It reacts with alkalis (e.g. sodium hydroxide) to form a salt and water, and dissolves in water to give an acidic solution.', '[2]'),
    ('Describe how you could show that aluminium oxide is amphoteric.', 'Add some to dilute hydrochloric acid and some to warm aqueous sodium hydroxide; it dissolves (reacts) in both.', '[2]'),
    ('Explain why oxides of elements on the left of the Periodic Table are basic while those on the right are acidic.', 'Metals (on the left) form basic oxides; non-metals (on the right) form acidic oxides; metallic character decreases across a period.', '[2]'),
    ('Explain why calcium oxide is used to remove sulfur dioxide from power-station waste gases.', 'Calcium oxide is basic and neutralises the acidic sulfur dioxide, forming calcium sulfite (and so reducing acid rain).', '[2]'),
])


@t11d.add('C1', (1, 2, 3))
def t11d_class(r, D):
    f, nm, kind = r.choice(OXIDES)
    return M(r, r.choice([f'How is {nm}, {F(f)}, classified?', f'Which type of oxide is {nm}, {F(f)}?']), kind, ['acidic', 'basic', 'amphoteric', 'neutral'], f'{cap(nm)} is {kind}: {OX_DEF[kind]}.')


@t11d.add('C3', (2, 3, 4, 5))
def t11d_tests(r, D):
    picks = r.sample(OXIDES, 4 if D >= 3 else 3)
    if len({k for _, _, k in picks}) < 3:
        return None
    labs = 'PQRS'
    def res(kind):
        a = 'reacts' if kind in ('basic', 'amphoteric') else 'no reaction'
        b = 'reacts' if kind in ('acidic', 'amphoteric') else 'no reaction'
        return a, b
    rows = '; '.join(f'oxide {labs[i]}: with dilute HCl – {res(k)[0]}, with aqueous NaOH – {res(k)[1]}' for i, (f, nm, k) in enumerate(picks))
    stem = f'Four oxides are tested with acid and alkali. {rows}. Classify each oxide as acidic, basic, amphoteric or neutral.'.replace('Four', str(len(picks)).replace('3', 'Three').replace('4', 'Four'))
    ans = '; '.join(f'{labs[i]}: {k}' for i, (f, nm, k) in enumerate(picks))
    key = ans + f'. 1 mark each [{len(picks)}]'
    if D >= 4:
        stem += ' Suggest the identity of each oxide.'
        ans += '. Possible identities: ' + ', '.join(f'{labs[i]} {nm}' for i, (f, nm, k) in enumerate(picks))
        key += '; suitable identities [1]'
    return Q(stem, ans, key, 'case')


@t11d.add('C3', (2, 3, 4))
def t11d_eq(r, D):
    f = r.choice(list(OX_EQ))
    nm, kind = [(n, k) for ff, n, k in OXIDES if ff == f][0]
    e = OX_EQ[f]
    L, R = parse_eq(e)
    other = [x for x in L if x[1] != f][0][1]
    oname = {'HCl': 'hydrochloric acid', 'H2SO4': 'sulfuric acid', 'HNO3': 'nitric acid', 'NaOH': 'sodium hydroxide solution'}[other]
    stem = f'Write the balanced symbol equation, with state symbols, for the reaction of {nm} with {oname}, and state what this reaction shows about the type of oxide.'
    return Q(stem, f'{E(e)}; {nm} is {kind}' + (' (it reacts with an acid)' if kind in ('basic', 'amphoteric') and other != 'NaOH' else ' (it reacts with an alkali)'),
             f'{E(e)}: formulae [1]; balanced [1]; states [1]; type of oxide [1]', 'short')


@t11d.add('C2', (2, 3, 4), 'explain')
def t11d_explain(r, D):
    f, nm, kind = r.choice(OXIDES)
    el = nm.split(' ')[0].replace('(II)', '').replace('(III)', '').replace('(IV)', '').replace('(V)', '')
    metal = kind in ('basic', 'amphoteric')
    return Q(f'Predict how {nm}, {F(f)}, reacts with dilute hydrochloric acid and with aqueous sodium hydroxide, and explain your prediction.',
             f'It is {kind}: {OX_DEF[kind]}.' + (f' {cap(el)} is a metal, and metal oxides are basic or amphoteric.' if metal else (f' {cap(el)} is a non-metal, and non-metal oxides are usually acidic.' if kind != 'neutral' else f' {cap(el)} is a non-metal, but a few non-metal oxides such as CO, NO and N₂O are neutral.')),
             '1 mark: classification; 1 mark: reactions with acid and alkali; ' + ('1 mark: link to metal/non-metal [3]' if D >= 3 else 'total [2]'))


def _t11d_c4(r, D):
    pick = r.sample([o for o in OXIDES if o[2] != 'neutral'], 3)
    p = person(r)
    intro = f'{p} investigates the oxides {", ".join(f"{nm} ({F(f)})" for f, nm, k in pick)}.'
    eqf = next((f for f, nm, k in pick if f in OX_EQ), None)
    parts = [
        lambda r: ('Classify each oxide as acidic, basic or amphoteric.', '; '.join(f'{nm}: {k}' for f, nm, k in pick), '1 mark each [3]'),
        lambda r: ('Explain how the type of oxide is linked to the position of the element in the Periodic Table.', 'metals on left → basic; non-metals on right → acidic; some (Al, Zn) amphoteric', '[2]'),
        lambda r: ('Describe an experiment to show that an oxide is amphoteric.', 'add to dilute acid and to aqueous NaOH separately; it reacts/dissolves in both', '[2]'),
        lambda r: ('Predict the pH of a solution formed when an acidic oxide dissolves in water.', 'below 7', '[1]'),
        lambda r: ('Name the products when a basic oxide reacts with an acid.', 'a salt and water', '[1]'),
    ]
    if eqf:
        parts.append(lambda r: (f'Write a balanced equation for one reaction of {F(eqf)}.', E(OX_EQ[eqf]), '[2]'))
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t11d.add('C4', (2, 3, 4, 5), 'multi_step')(_t11d_c4)

CHAPTERS[11] = [t11a, t11b, t11c, t11d]


# ---------------------------------------------------------------- marks follow the marking key
def _key_marks(k):
    """Total marks implied by a marking key: per-part totals for (a)/(b) keys, otherwise the
    sum of the [n] mark points (or the stated total where the key gives one)."""
    if re.search(r'\([a-h]\) ', k) and re.match(r'^\(a\)', k.strip()):
        segs = [s for s in re.split(r'\([a-h]\) ', k) if s.strip()]
        vals = [_key_marks(s) for s in segs]
        return sum(v or 1 for v in vals) if segs else None
    nums = [int(x) for x in re.findall(r'\[(\d+)\]', k)]
    if not nums:
        return None
    if 'total [' in k:
        return nums[-1]
    return sum(nums)


def _marks_from_key(fn):
    def w(r, D):
        q = fn(r, D)
        if q and not q.get('options') and not re.match(r'^\(a\)', q.get('key', '').strip()):
            m = _key_marks(q.get('key', ''))
            if m and 1 <= m <= 12:
                q['marks'] = m
        return q
    w.__name__ = getattr(fn, '__name__', 'fn')
    return w


for _ts in CHAPTERS.values():
    for _t in _ts:
        for _tp in _t.templates:
            _tp.fn = _marks_from_key(_tp.fn)
