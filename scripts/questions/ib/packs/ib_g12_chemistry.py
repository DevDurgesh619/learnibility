"""IB DP Chemistry SL/HL (first assessment 2025), DP year 2 – ib-g12-chemistry.

Structure 3 (the periodic table, functional groups, spectroscopy) and Reactivity 2.2–2.3 (kinetics,
equilibrium), Reactivity 3 (proton transfer, electron transfer, radicals, nucleophilic and electrophilic
mechanisms) and the Internal Assessment.

Numerical items are parametric and compute their answers with IB data-booklet values
(see ib_chemistry_common). Answers are quoted to 3 significant figures unless the data justify
fewer (pH to 2 d.p.). Mock = HL Paper 1A (40 MCQ) + 1B (data-based, 35 marks) + Paper 2 (90 marks).
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from ib_chemistry_common import (AR, BE, CONFIG, CW, EN, ENAME, EO, ACIDS, BASES, INDICATORS, FARADAY, KW, HF, IE1,  # noqa: F401
                                  MOCK, NA, RGAS, S0, VM, Z, atoms, chem, dp, ion, make_templates, mr, nmcq, num,
                                  p1b, pct_error, pick, q, repeat_readings, sf, sgn)
from ib_g11_chemistry import config, config_ion, cfg_short, cfg_s, unpaired, TM_COMP  # noqa: F401

R = Registry()
templates = make_templates(R)


def init(subject_id):
    pass


def _lst(xs):
    xs = list(xs)
    return ', '.join(xs[:-1]) + ' and ' + xs[-1]


def rsf(x, n=3):
    """x rounded to n significant figures, as a float."""
    return float(f'{x:.{n}g}')


def ionx(f):
    """Single-charge species from the ACIDS/BASES tables: 'NO2-' -> 'NO₂⁻', 'NH4+' -> 'NH₄⁺'."""
    if '^' not in f and f[-1] in '+-' and (len(f) < 2 or f[-2] not in '23'):
        return chem(f[:-1]) + sup(f[-1])
    return ion(f)


def cap(s):
    return s[0].upper() + s[1:]


# =============================================================================================
# ch01 S3.1 The periodic table: classification of elements
# =============================================================================================
BLOCK_OF = {'s': 's-block', 'p': 'p-block', 'd': 'd-block', 'f': 'f-block'}
POS_ELS = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
           'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr']


def _pos_fix(el):
    """(period, group 1-18, block letter) from the ground-state configuration."""
    if el == 'He':
        return 1, 18, 's'
    occ = dict(config(Z[el]))
    p = max(int(sl[0]) for sl in occ)
    ns, np_, nd = occ.get(f'{p}s', 0), occ.get(f'{p}p', 0), occ.get(f'{p - 1}d', 0) if p >= 4 else 0
    if np_:
        return p, 12 + np_, 'p'
    if 21 <= Z[el] <= 30 or 39 <= Z[el] <= 48:
        return p, nd + ns, 'd'
    return p, ns, 's'


R.facts('ch01-st1', F(
    terms=[('period', 'a horizontal row of the periodic table; the period number equals the number of the outer (highest occupied) main energy level'),
           ('group', 'a vertical column of the periodic table containing elements with the same outer-shell electron configuration'),
           ('s-block', 'the region of the periodic table (groups 1 and 2, plus He) in which the highest-energy electron occupies an s sublevel'),
           ('p-block', 'the region of the periodic table (groups 13–18) in which the highest-energy electron occupies a p sublevel'),
           ('d-block', 'the region of the periodic table (groups 3–12) in which the highest-energy electron occupies a d sublevel'),
           ('valence electrons', 'the electrons in the outer main energy level of an atom (plus, for d-block elements, the (n−1)d electrons) that are involved in bonding'),
           ('metalloid', 'an element with properties intermediate between those of metals and non-metals, such as boron, silicon, germanium, arsenic and tellurium')],
    facts=[('Which block of the periodic table contains the transition elements?', 'd-block', ['s-block', 'p-block', 'f-block'], 'Transition elements fill the 3d, 4d or 5d sublevel.'),
           ('What do elements in the same group have in common?', 'the same number of valence electrons', ['the same number of occupied energy levels', 'the same atomic radius', 'the same number of neutrons'], 'Same outer-shell configuration → similar chemistry.'),
           ('Which element is a metalloid?', 'silicon', ['sulfur', 'aluminium', 'phosphorus'], 'Si lies on the metal/non-metal boundary.'),
           ('The lanthanoids and actinoids form which block?', 'f-block', ['d-block', 'p-block', 's-block'], 'They fill 4f and 5f sublevels.'),
           ('Which group contains the halogens?', '17', ['1', '16', '18'], 'Halogens: F, Cl, Br, I, At – ns² np⁵.'),
           ('What does the period number of a main-group element indicate?', 'the number of occupied main energy levels', ['the number of valence electrons', 'the charge of its most common ion', 'the number of unpaired electrons'], 'Period n → outer electrons in level n.')],
    why=[('Explain why elements in the same group have similar chemical properties.', 'They have the same number of electrons in their outer shell (same outer configuration), and chemical reactions involve the outer electrons, so they react in similar ways.'),
         ('Explain why the periodic table can be divided into s, p, d and f blocks.', 'The position of an element depends on the sublevel that its highest-energy electron enters; the width of each block (2, 6, 10, 14 columns) equals the number of electrons the sublevel can hold.'),
         ('Explain why helium is placed in group 18 even though its configuration is 1s².', 'Helium has a full outer shell like the other noble gases and is similarly unreactive, so it is placed with them rather than with the reactive group 2 metals.'),
         ('Explain how the electron configuration of an element allows its period and group to be deduced.', 'The highest occupied main level gives the period; the number of outer (valence) electrons gives the group (for p-block add 10 to the s + p electrons; for d-block add the (n−1)d and ns electrons).'),
         ('Explain why the elements in period 2 are the first to show the full s and p sublevel pattern.', 'Level n = 2 contains a 2s and three 2p orbitals, holding up to 8 electrons, so period 2 contains 8 elements from Li (2s¹) to Ne (2s² 2p⁶).')],
    contrast=[('a period', 'a group', 'A period is a horizontal row (same number of occupied main levels, properties change across it); a group is a vertical column (same outer configuration, similar properties).'),
              ('the s-block', 'the p-block', 'In the s-block the outermost electron enters an s sublevel (groups 1, 2); in the p-block it enters a p sublevel (groups 13–18).'),
              ('metals', 'non-metals', 'Metals (left) tend to lose electrons, form basic oxides and conduct; non-metals (right) tend to gain or share electrons, form acidic oxides and are mostly insulators.')],
    misc=[('Elements in the same period have similar chemical properties.', 'Elements in the same GROUP have similar properties; across a period the properties change gradually from metallic to non-metallic.'),
          ('The group number always equals the number of electrons in the outer shell.', 'This holds for groups 1 and 2; for groups 13–18 the outer-shell electrons equal the group number minus 10, and d-block group numbers include (n−1)d electrons.'),
          ('Hydrogen is an alkali metal because it is in group 1.', 'Hydrogen has one valence electron (1s¹) but is a non-metal that forms H₂ molecules; it is often placed separately because its properties do not match group 1.')],
    apply=[('Deduce the period, group and block of the element with configuration [Ar] 3d¹⁰ 4s² 4p³.', 'period 4, group 15, p-block (arsenic)', 2),
           ('An element X forms a 2+ ion with configuration [Ar]. Deduce the position of X in the periodic table.', 'X has [Ar] 4s²: calcium – period 4, group 2, s-block', 2),
           ('State the outer-shell configuration shared by all elements in group 16.', 'ns² np⁴', 1)],
    evaluate=[('The periodic table is the most important organising principle in chemistry.', ['predicts properties and reactivity from position', 'summarises electron configurations and periodic trends', 'predicted undiscovered elements (Mendeleev, gallium and germanium)'], ['position does not fully predict properties (e.g. hydrogen, anomalous first members of groups)', 'other principles (conservation of energy, equilibrium) are equally fundamental', 'f-block placement and group 3 membership are still debated'], 'It is a central organising tool, but it summarises underlying quantum principles rather than replacing them.')],
    extended=[('Element Q has 33 electrons. (a) Write its full electron configuration. (b) Deduce its period, group and block. (c) Predict, with a reason, whether its oxide is acidic or basic. (d) Identify one other element with similar chemical properties.', '(a) 1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s² 4p³. (b) period 4, group 15, p-block (arsenic). (c) acidic – non-metal/metalloid oxide. (d) phosphorus (or N, Sb) – same ns² np³ outer configuration.', 6, 'multi_step')],
))


@R.add('ch01-st1', 'C3', (1, 4), 'mcq')
def c3_position_mcq(rng, slot):
    el = pick(rng, [e for e in POS_ELS if e not in ('H', 'He')])
    p, g, b = _pos_fix(el)
    cfg = cfg_short(config(Z[el]))
    right = f'period {p}, group {g}'
    wr = {f'period {p - 1}, group {g}', f'period {p}, group {g - 10 if g > 12 else g + 10 if g <= 2 else g - 1}', f'period {p + 1}, group {g}', f'period {p}, group {g + 1 if g < 18 else g - 2}'}
    wr = [w for w in wr if w != right and 'group 0' not in w and 'group -' not in w and 'period 0' not in w]
    rng.shuffle(wr)
    stem = pick(rng, [f'An element has the ground-state configuration {cfg}. Where is it in the periodic table?',
                      f'Where in the periodic table is the element whose atoms have the configuration {cfg}?'])
    return mcq(rng, stem, right, wr[:3], f'Highest occupied level n = {p} → period {p}; outer configuration → group {g} ({b}-block): {ENAME[el]}.')


@R.add('ch01-st1', 'C3', (1, 4), 'short')
def c3_position_short(rng, slot):
    el = pick(rng, [e for e in POS_ELS if e not in ('H', 'He')])
    p, g, b = _pos_fix(el)
    if rng.random() < 0.5:
        stem = f'An atom of an element contains {Z[el]} electrons. Deduce the period, group and block of the element.'
    else:
        stem = f'Write the condensed electron configuration of {ENAME[el]} (Z = {Z[el]}) and use it to state its period, group and block.'
    return dict(stem=stem, answer=f'{cfg_short(config(Z[el]))}: period {p}, group {g}, {b}-block', markingKey=f'Configuration {cfg_short(config(Z[el]))} (1); period {p} and group {g} (1); {b}-block (1).', type='short', marks=3)


@R.add('ch01-st1', 'C3', (1, 3), 'mcq')
def c3_block_mcq(rng, slot):
    el = pick(rng, POS_ELS)
    p, g, b = _pos_fix(el)
    right = f'{b}-block'
    stem = f'In which block of the periodic table is {ENAME[el]} (Z = {Z[el]}) found?'
    return mcq(rng, stem, right, [x for x in ['s-block', 'p-block', 'd-block', 'f-block'] if x != right], f'{ENAME[el]}: {cfg_short(config(Z[el]))}; highest-energy electron in a {b} sublevel.')


@R.add('ch01-st1', 'C3', (2, 4), 'mcq')
def c3_same_group(rng, slot):
    groups = {1: ['Li', 'Na', 'K', 'Rb'], 2: ['Be', 'Mg', 'Ca', 'Sr'], 13: ['B', 'Al', 'Ga'], 14: ['C', 'Si', 'Ge'], 15: ['N', 'P', 'As'], 16: ['O', 'S', 'Se'], 17: ['F', 'Cl', 'Br'], 18: ['Ne', 'Ar', 'Kr']}
    g = pick(rng, list(groups))
    a, b = rng.sample(groups[g], 2)
    others = [e for gg, es in groups.items() if gg != g for e in es]
    wr = rng.sample(others, 3)
    stem = f'Which element has chemical properties most similar to those of the element with atomic number {Z[a]}?'
    return mcq(rng, stem, ENAME[b], [ENAME[w] for w in wr], f'Z = {Z[a]} is {ENAME[a]} (group {g}); {ENAME[b]} is in the same group with the same outer configuration.')


@R.add('ch01-st1', 'C2', (1, 4), 'mcq')
def c2_outer_cfg(rng, slot):
    g, cfg = pick(rng, [(1, 'ns¹'), (2, 'ns²'), (13, 'ns² np¹'), (14, 'ns² np²'), (15, 'ns² np³'), (16, 'ns² np⁴'), (17, 'ns² np⁵'), (18, 'ns² np⁶')])
    pool = ['ns¹', 'ns²', 'ns² np¹', 'ns² np²', 'ns² np³', 'ns² np⁴', 'ns² np⁵', 'ns² np⁶']
    wr = [x for x in pool if x != cfg]
    rng.shuffle(wr)
    return mcq(rng, f'Which outer-shell configuration is shared by the elements of group {g}?', cfg, wr[:3], f'Group {g} → {cfg}.')


R.mcqs('ch01-st1', 'C2', (1, 4), [
    ('Why is the d-block ten elements wide?', 'A d sublevel has five orbitals holding a maximum of ten electrons.', ['There are ten transition metals in every period.', 'Each d orbital holds ten electrons.', 'The 3d sublevel fills after the 4p sublevel.'], 'Block width = sublevel capacity.'),
    ('Why are the elements of period 3 placed in the same period?', 'Their outer electrons are all in the third main energy level.', ['They all have three valence electrons.', 'They all form 3+ ions.', 'They all have similar properties.'], 'Same number of occupied levels.'),
    ('Which statement about elements in the same group is correct?', 'They have the same number of valence electrons but different numbers of occupied shells.', ['They have the same number of shells.', 'They have identical first ionisation energies.', 'They all have the same atomic radius.'], 'Same outer configuration, different n.'),
    ('Why does potassium appear in period 4 rather than period 3?', 'Its outermost electron enters the 4s sublevel, which fills before 3d.', ['It has four valence electrons.', 'It has four neutrons more than sodium.', 'Its 3p sublevel is incomplete.'], '[Ar] 4s¹.'),
])


# ---- ch01-st2 periodic trends ----
ATR = {'Li': 130, 'Be': 99, 'B': 84, 'C': 75, 'N': 71, 'O': 64, 'F': 60, 'Na': 160, 'Mg': 140, 'Al': 124, 'Si': 114,
       'P': 109, 'S': 104, 'Cl': 100, 'K': 200, 'Ca': 174, 'Br': 117, 'Rb': 215, 'Sr': 190, 'I': 136, 'Cs': 238, 'Ba': 206}
IONR = {'Li+': 76, 'Na+': 102, 'K+': 138, 'Rb+': 152, 'Cs+': 167, 'Be2+': 45, 'Mg2+': 72, 'Ca2+': 100, 'Sr2+': 118, 'Ba2+': 135,
        'Al3+': 54, 'F-': 133, 'Cl-': 181, 'Br-': 196, 'I-': 220, 'O2-': 140, 'S2-': 184, 'N3-': 146}
EA1 = {'H': -73, 'Li': -60, 'Na': -53, 'K': -48, 'C': -122, 'Si': -134, 'O': -141, 'S': -200, 'F': -328, 'Cl': -349, 'Br': -325, 'I': -295, 'P': -72, 'Al': -42}
ISO = [['N3-', 'O2-', 'F-', 'Na+', 'Mg2+', 'Al3+'], ['S2-', 'Cl-', 'K+', 'Ca2+']]
IZ = {'N3-': 7, 'O2-': 8, 'F-': 9, 'Na+': 11, 'Mg2+': 12, 'Al3+': 13, 'S2-': 16, 'Cl-': 17, 'K+': 19, 'Ca2+': 20}

R.facts('ch01-st2', F(
    terms=[('atomic radius', 'half the distance between the nuclei of two bonded atoms of the same element'),
           ('effective nuclear charge', 'the net positive charge experienced by an outer electron: the nuclear charge minus the shielding by inner electrons'),
           ('first electron affinity', 'the enthalpy change when one mole of electrons is added to one mole of gaseous atoms to form one mole of gaseous 1− ions'),
           ('electronegativity', 'the relative ability of an atom to attract a shared pair of electrons in a covalent bond'),
           ('first ionisation energy', 'the minimum energy required to remove one mole of electrons from one mole of gaseous atoms in their ground state'),
           ('isoelectronic', 'having the same number of electrons (and electron configuration), e.g. O²⁻, F⁻, Na⁺ and Mg²⁺'),
           ('shielding', 'the reduction in attraction between the nucleus and outer electrons caused by repulsion from inner electrons')],
    facts=[('Which element has the highest electronegativity?', 'fluorine', ['chlorine', 'oxygen', 'caesium'], 'F = 4.0 on the Pauling scale.'),
           ('How does atomic radius change across period 3 from Na to Cl?', 'it decreases', ['it increases', 'it stays constant', 'it increases then decreases'], 'Nuclear charge rises; shielding roughly constant.'),
           ('Which ion has the largest radius?', 'S²⁻', ['Cl⁻', 'K⁺', 'Ca²⁺'], 'Isoelectronic: fewest protons → largest.'),
           ('Which element has the most exothermic first electron affinity?', 'chlorine', ['fluorine', 'iodine', 'oxygen'], 'Cl −349 kJ mol⁻¹; F is smaller and suffers more electron repulsion.'),
           ('How does electronegativity change down group 17?', 'it decreases', ['it increases', 'it stays the same', 'it first increases then decreases'], 'Bonding pair further from the nucleus, more shielding.'),
           ('Compared with its atom, a positive ion is', 'smaller', ['larger', 'the same size', 'larger only for group 1'], 'Loss of the outer shell / greater attraction per electron.')],
    why=[('Explain why atomic radius decreases across a period.', 'Nuclear charge increases by one each element while electrons are added to the same main level, so shielding barely increases; the greater effective nuclear charge pulls the outer electrons closer.'),
         ('Explain why a sodium ion is smaller than a sodium atom.', 'Na⁺ has lost its 3s electron, so it has one fewer occupied main level, and the 11 protons now attract only 10 electrons more strongly.'),
         ('Explain why the second electron affinity of oxygen is endothermic.', 'Adding an electron to O⁻ means bringing a negative electron towards a negative ion; energy must be supplied to overcome the repulsion.'),
         ('Explain why first ionisation energy decreases down a group.', 'The outer electron is in a higher main level, further from the nucleus and more shielded by inner electrons, so it is less strongly attracted and easier to remove (despite the higher nuclear charge).'),
         ('Explain why the ionic radius decreases in the isoelectronic series N³⁻, O²⁻, F⁻, Na⁺, Mg²⁺.', 'All have the configuration 1s² 2s² 2p⁶, but nuclear charge increases from 7 to 12, so the same number of electrons is pulled closer.'),
         ('Explain why fluorine has a less exothermic electron affinity than chlorine.', 'Fluorine is very small, so the added electron enters a compact 2p sublevel where repulsion from the existing electrons is greater.')],
    contrast=[('electronegativity', 'electron affinity', 'Electronegativity is a relative (unitless) measure of attraction for a bonding pair in a molecule; electron affinity is a measured enthalpy change (kJ mol⁻¹) for adding an electron to an isolated gaseous atom.'),
              ('a cation', 'an anion of the same element', 'Cations are smaller than their atoms (fewer electrons, often fewer shells); anions are larger (extra electron–electron repulsion, same nuclear charge).'),
              ('nuclear charge', 'effective nuclear charge', 'Nuclear charge is the total number of protons; effective nuclear charge is what an outer electron actually feels after shielding by inner electrons.')],
    misc=[('Atoms get bigger across a period because more electrons are added.', 'Across a period the extra electrons go into the same shell while the nuclear charge increases, so the atoms get smaller.'),
          ('Electronegativity is measured in kJ mol⁻¹.', 'Electronegativity is a relative scale without units (Pauling scale); electron affinity and ionisation energy have units of kJ mol⁻¹.'),
          ('Negative ions are smaller than their atoms because they have extra electrons pulling inwards.', 'Electrons do not pull inwards; the extra electron increases repulsion while the nuclear charge is unchanged, so the anion is larger.')],
    apply=[('Arrange Na⁺, Mg²⁺ and Al³⁺ in order of increasing ionic radius and explain the order.', 'Al³⁺ < Mg²⁺ < Na⁺: isoelectronic (10 electrons) with increasing nuclear charge 11 → 13 pulling electrons closer.', 3),
           ('Predict, with a reason, whether rubidium or strontium has the larger atomic radius.', 'Rubidium: same period, but Sr has one more proton with similar shielding, so its electrons are held closer.', 2),
           ('Use electronegativity values to predict which atom carries the partial positive charge in the C–Cl bond.', 'Carbon (2.6) is less electronegative than chlorine (3.2), so C is δ+.', 1)],
    evaluate=[('Effective nuclear charge alone explains all periodic trends.', ['explains decrease in radius and increase in IE and electronegativity across a period', 'combined with distance it explains group trends'], ['distance and shielding must be considered down a group', 'sublevel effects (2p vs 2s, paired electrons) cause anomalies in IE', 'electron–electron repulsion explains electron affinity anomalies (F vs Cl)'], 'It is the key idea across a period but must be combined with distance, shielding and sublevel structure.')],
    extended=[('The first ionisation energies (kJ mol⁻¹) of period 3 are Na 496, Mg 738, Al 578, Si 787, P 1012, S 1000, Cl 1251, Ar 1521. (a) Describe the general trend and explain it. (b) Explain the decrease from Mg to Al. (c) Explain the decrease from P to S. (d) Predict, with a reason, the value for K relative to Na.', '(a) increases: increasing nuclear charge, same shell, similar shielding. (b) Al 3p electron is higher in energy and shielded by 3s². (c) S has a paired 3p electron; repulsion makes it easier to remove. (d) lower (419): 4s electron further away and more shielded.', 8, 'multi_step')],
))


@R.add('ch01-st2', 'C3', (1, 4), 'mcq')
def c3_radius_rank(rng, slot):
    pool = rng.sample(list(ATR), 4)
    kind = rng.choice(['largest', 'smallest'])
    best = (max if kind == 'largest' else min)(pool, key=lambda e: ATR[e])
    if sorted(ATR[e] for e in pool).count(ATR[best]) > 1:
        return None
    stem = f'Which of {_lst(ENAME[e] for e in sorted(pool, key=lambda e: Z[e]))} has the {kind} atomic radius?'
    return mcq(rng, stem, ENAME[best], [ENAME[e] for e in pool if e != best], 'Atomic radii / pm (data booklet): ' + ', '.join(f'{e} {ATR[e]}' for e in pool) + '. Radius decreases across a period and increases down a group.')


@R.add('ch01-st2', 'C3', (1, 4), 'mcq')
def c3_iso_rank(rng, slot):
    ser = pick(rng, ISO)
    pool = rng.sample(ser, min(4, len(ser)))
    kind = rng.choice(['largest', 'smallest'])
    best = (max if kind == 'largest' else min)(pool, key=lambda s: IONR[s])
    stem = f'The ions {_lst(ion(s) for s in pool)} are isoelectronic. Which has the {kind} radius?'
    return mcq(rng, stem, ion(best), [ion(s) for s in pool if s != best], 'Same number of electrons; ' + ', '.join(f'{ion(s)} has {IZ[s]} protons' for s in pool) + '. More protons → smaller ion.')


@R.add('ch01-st2', 'C3', (1, 4), 'mcq')
def c3_en_rank(rng, slot):
    els = [e for e in EN if e not in ('H',)]
    for _ in range(20):
        pool = rng.sample(els, 4)
        kind = rng.choice(['highest', 'lowest'])
        vals = [EN[e] for e in pool]
        t = max(vals) if kind == 'highest' else min(vals)
        if vals.count(t) == 1:
            break
    else:
        return None
    best = pool[vals.index(t)]
    stem = f'Which of the elements {_lst(ENAME[e] for e in sorted(pool, key=lambda e: Z[e]))} has the {kind} electronegativity?'
    return mcq(rng, stem, ENAME[best], [ENAME[e] for e in pool if e != best], 'Pauling values: ' + ', '.join(f'{e} {EN[e]}' for e in pool) + '. Electronegativity increases across a period and decreases down a group.')


@R.add('ch01-st2', 'C3', (2, 4), 'mcq')
def c3_ea_rank(rng, slot):
    pool = rng.sample(list(EA1), 4)
    best = min(pool, key=lambda e: EA1[e])
    if [EA1[e] for e in pool].count(EA1[best]) > 1:
        return None
    stem = f'Which of {_lst(ENAME[e] for e in sorted(pool, key=lambda e: Z[e]))} has the most exothermic first electron affinity?'
    return mcq(rng, stem, ENAME[best], [ENAME[e] for e in pool if e != best], 'First electron affinities / kJ mol⁻¹: ' + ', '.join(f'{e} {EA1[e]}' for e in pool) + '.')


@R.add('ch01-st2', 'C3', (1, 5), 'short')
def c3_atom_vs_ion(rng, slot):
    pairs = [('Na', 'Na+'), ('Mg', 'Mg2+'), ('Al', 'Al3+'), ('K', 'K+'), ('Ca', 'Ca2+'), ('Cl', 'Cl-'), ('F', 'F-'), ('O', 'O2-'), ('S', 'S2-'), ('Br', 'Br-'), ('Li', 'Li+'), ('I', 'I-')]
    a, i_ = pick(rng, pairs)
    bigger = a if ATR[a] > IONR[i_] else i_
    neg = '-' in i_
    stem = pick(rng, [f'The atomic radius of {ENAME[a]} is {ATR[a]} pm and the ionic radius of {ion(i_)} is {IONR[i_]} pm. Explain the difference.',
                      f'Predict, with a reason, whether the {ENAME[a]} atom or the {ion(i_)} ion is larger.'])
    why = ('the anion has extra electron(s), increasing electron–electron repulsion while the nuclear charge is unchanged, so the electron cloud expands' if neg else
           'the cation has lost its outer shell, and the same nuclear charge now attracts fewer electrons more strongly')
    return dict(stem=stem, answer=f'{ion(bigger) if bigger == i_ else ENAME[a] + " atom"} is larger: {why}.', markingKey=f'Correct comparison (1); {why} (1–2).', type='explain' if stem.startswith('The') else 'short', marks=3 if stem.startswith('The') else 2)


@R.add('ch01-st2', 'C3', (2, 4), 'numerical')
def c3_ie_from_wavelength(rng, slot):
    el = pick(rng, ['Na', 'K', 'Li', 'Mg', 'Ca', 'Al', 'H', 'Rb'])
    E = IE1[el] * 1000 / NA
    lam = 6.63e-34 * 3.00e8 / E
    stem = pick(rng, [f'The first ionisation energy of {ENAME[el]} is {IE1[el]} kJ mol⁻¹. Calculate the maximum wavelength of electromagnetic radiation, in nm, that could ionise a single gaseous {ENAME[el]} atom.',
                      f'Calculate the longest wavelength of light (in nm) able to remove the outer electron from a gaseous atom of {ENAME[el]}, given that its first ionisation energy is {IE1[el]} kJ mol⁻¹.'])
    return num(stem, q(lam * 1e9, 'nm'), f'E per atom = {IE1[el]} × 10³ / 6.02 × 10²³ = {sf(E)} J (M1); λ = hc/E = (6.63 × 10⁻³⁴ × 3.00 × 10⁸)/{sf(E)} = {sf(lam)} m (M1) = {q(lam * 1e9, "nm")} (A1).', 3)


R.mcqs('ch01-st2', 'C2', (1, 4), [
    ('Why does the first ionisation energy of potassium lie below that of sodium?', 'The 4s electron of potassium is further from the nucleus and more shielded.', ['Potassium has fewer protons.', 'Potassium has a smaller atomic radius.', 'The 4s orbital is lower in energy than 3s.'], 'Distance and shielding outweigh higher nuclear charge.'),
    ('Why is the Mg²⁺ ion smaller than the Na⁺ ion?', 'Mg²⁺ has one more proton attracting the same number of electrons.', ['Mg²⁺ has fewer electron shells.', 'Mg²⁺ has more electrons.', 'Mg is in a lower period.'], 'Isoelectronic, Z 12 vs 11.'),
    ('Which statement explains why electronegativity increases across period 2?', 'Nuclear charge increases while the bonding electrons stay in the same shell.', ['Atomic radius increases.', 'More shells are added.', 'Shielding increases strongly.'], 'Higher effective nuclear charge.'),
    ('Why is the first electron affinity of most elements exothermic?', 'The added electron is attracted by the nucleus of the neutral atom.', ['Energy is needed to overcome repulsion.', 'Electrons are always removed exothermically.', 'The ion formed is always a noble gas.'], 'Attraction > repulsion for X(g) + e⁻.'),
    ('Why are the atomic radii of noble gases usually not compared with other elements in the period?', 'They do not normally form bonds, so a covalent (bonded) radius cannot be measured in the same way.', ['They have no electrons in their outer shell.', 'Their radii are infinitely large.', 'They are all radioactive.'], 'Atomic radius is defined from bonded atoms.'),
])


# ---- ch01-st3 period 3 oxides ----
OXIDES = [('Na2O', 'sodium oxide', 'basic', 'ionic', 'Na2O(s) + H2O(l) → 2NaOH(aq)', 14, 'Na2O(s) + 2HCl(aq) → 2NaCl(aq) + H2O(l)'),
          ('MgO', 'magnesium oxide', 'basic', 'ionic', 'MgO(s) + H2O(l) → Mg(OH)2(s/aq)', 10, 'MgO(s) + 2HCl(aq) → MgCl2(aq) + H2O(l)'),
          ('Al2O3', 'aluminium oxide', 'amphoteric', 'ionic with some covalent character', 'insoluble in water', 7, 'Al2O3(s) + 6HCl(aq) → 2AlCl3(aq) + 3H2O(l); Al2O3(s) + 2NaOH(aq) + 3H2O(l) → 2NaAl(OH)4(aq)'),
          ('SiO2', 'silicon dioxide', 'acidic', 'giant covalent', 'insoluble in water', 7, 'SiO2(s) + 2NaOH(aq) → Na2SiO3(aq) + H2O(l)'),
          ('P4O10', 'phosphorus(V) oxide', 'acidic', 'simple molecular covalent', 'P4O10(s) + 6H2O(l) → 4H3PO4(aq)', 2, 'P4O10(s) + 12NaOH(aq) → 4Na3PO4(aq) + 6H2O(l)'),
          ('SO3', 'sulfur trioxide', 'acidic', 'simple molecular covalent', 'SO3(g) + H2O(l) → H2SO4(aq)', 1, 'SO3(g) + 2NaOH(aq) → Na2SO4(aq) + H2O(l)'),
          ('SO2', 'sulfur dioxide', 'acidic', 'simple molecular covalent', 'SO2(g) + H2O(l) → H2SO3(aq)', 3, 'SO2(g) + 2NaOH(aq) → Na2SO3(aq) + H2O(l)'),
          ('Cl2O7', 'dichlorine heptoxide', 'acidic', 'simple molecular covalent', 'Cl2O7(l) + H2O(l) → 2HClO4(aq)', 1, 'Cl2O7(l) + 2NaOH(aq) → 2NaClO4(aq) + H2O(l)')]
OXX = {o[0]: o for o in OXIDES}


def eqp(e):
    """Pretty-print an equation written with ASCII formulae."""
    out = []
    for tok in e.split(' '):
        if any(ch.isdigit() for ch in tok) and any(ch.isalpha() for ch in tok):
            m = tok
            lead = ''
            while m and m[0].isdigit():
                lead += m[0]
                m = m[1:]
            out.append(lead + chem(m) if m else tok)
        else:
            out.append(tok)
    return ' '.join(out)


R.facts('ch01-st3', F(
    terms=[('basic oxide', 'a metal oxide that reacts with acids to form a salt and water; soluble ones form alkaline solutions'),
           ('acidic oxide', 'a non-metal oxide that reacts with bases and dissolves in water to form an acidic solution'),
           ('amphoteric', 'able to react both as an acid and as a base, e.g. aluminium oxide'),
           ('acid deposition', 'the process by which acidic substances (from SO₂ and NOx) leave the atmosphere as wet (rain, snow) or dry deposits'),
           ('ocean acidification', 'the decrease in the pH of the oceans caused by the dissolving of atmospheric carbon dioxide to form carbonic acid')],
    facts=[('Which period 3 oxide is amphoteric?', 'Al₂O₃', ['MgO', 'SiO₂', 'P₄O₁₀'], 'Al₂O₃ reacts with both HCl and NaOH.'),
           ('Which oxide dissolves in water to form the solution with the highest pH?', 'Na₂O', ['MgO', 'SO₃', 'Al₂O₃'], 'Na₂O → NaOH(aq), pH ≈ 14.'),
           ('What is formed when sulfur trioxide reacts with water?', 'sulfuric acid', ['sulfurous acid', 'hydrogen sulfide', 'sulfur dioxide'], 'SO₃ + H₂O → H₂SO₄.'),
           ('How does the acid-base character of the oxides change across period 3?', 'from basic through amphoteric to acidic', ['from acidic to basic', 'all are acidic', 'from amphoteric to basic'], 'Ionic metal oxides → covalent non-metal oxides.'),
           ('Which gas is the main cause of natural acidity in rain water (pH ≈ 5.6)?', 'carbon dioxide', ['sulfur dioxide', 'nitrogen', 'ozone'], 'CO₂ + H₂O ⇌ H₂CO₃.'),
           ('Which oxide is insoluble in water but reacts with hot concentrated sodium hydroxide?', 'SiO₂', ['Na₂O', 'SO₂', 'P₄O₁₀'], 'Giant covalent acidic oxide.')],
    why=[('Explain why the oxides of the metals on the left of period 3 are basic.', 'They are ionic and contain the oxide ion, O²⁻, which accepts protons (O²⁻ + H₂O → 2OH⁻; O²⁻ + 2H⁺ → H₂O).'),
         ('Explain why aluminium oxide is described as amphoteric.', 'It reacts with acids (e.g. HCl, forming Al³⁺ salts) and with strong bases (NaOH, forming aluminate ions, Al(OH)₄⁻), so it behaves as both a base and an acid.'),
         ('Explain why sulfur dioxide released from burning coal causes acid rain.', 'SO₂ dissolves in rain water to form sulfurous acid (SO₂ + H₂O → H₂SO₃) and can be oxidised to SO₃/sulfuric acid, lowering the pH of the rain below 5.6.'),
         ('Explain how nitrogen oxides are formed in car engines.', 'At the very high temperature of combustion, nitrogen and oxygen from the air combine: N₂ + O₂ → 2NO; NO is then oxidised to NO₂ in the air.'),
         ('Explain why increasing atmospheric carbon dioxide lowers the pH of the oceans.', 'More CO₂ dissolves: CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻, increasing [H⁺]; this reduces carbonate available to shell-forming organisms.')],
    contrast=[('a basic oxide', 'an acidic oxide', 'A basic oxide (usually ionic, metal) reacts with acids and forms OH⁻ in water; an acidic oxide (usually covalent, non-metal) reacts with bases and forms H⁺/H₃O⁺ in water.'),
              ('sodium oxide', 'phosphorus(V) oxide', 'Na₂O is ionic and basic, forming NaOH(aq) (pH 14); P₄O₁₀ is molecular covalent and acidic, forming H₃PO₄(aq) (pH ~2).'),
              ('wet acid deposition', 'dry acid deposition', 'Wet deposition is acid dissolved in rain, snow or fog; dry deposition is acidic gases or particles settling directly onto surfaces.')],
    misc=[('All oxides dissolve in water to give acidic or alkaline solutions.', 'Some oxides (Al₂O₃, SiO₂) are insoluble and give neutral water; their acid/base character is shown by their reactions with acids and bases.'),
          ('Aluminium oxide is acidic because aluminium is in group 13.', 'Al₂O₃ is amphoteric: it reacts with both acids and bases.'),
          ('Acid rain is caused mainly by carbon dioxide.', 'CO₂ only makes rain weakly acidic (pH 5.6); acid rain (pH < 5.6) is caused by SO₂ and NOx forming H₂SO₄ and HNO₃.')],
    apply=[('Write an equation for the reaction of magnesium oxide with nitric acid.', 'MgO(s) + 2HNO₃(aq) → Mg(NO₃)₂(aq) + H₂O(l)', 2),
           ('Write equations to show that nitrogen dioxide forms two acids with water.', '2NO₂(g) + H₂O(l) → HNO₃(aq) + HNO₂(aq)', 2),
           ('Write an equation for the neutralisation of acidic lake water with calcium oxide (lime), using H⁺ to represent the acid.', 'CaO(s) + 2H⁺(aq) → Ca²⁺(aq) + H₂O(l)', 2),
           ('Write equations for the reactions of aluminium oxide with hydrochloric acid and with aqueous sodium hydroxide.', 'Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; Al₂O₃ + 2NaOH + 3H₂O → 2NaAl(OH)₄', 4)],
    evaluate=[('Reducing sulfur emissions has solved the problem of acid deposition.', ['flue-gas desulfurisation and low-sulfur fuels have cut SO₂ emissions sharply in Europe and North America', 'rain pH in many regions has recovered'], ['NOx from vehicles and agriculture remain significant', 'emissions are rising in some industrialising regions', 'damaged soils and lakes recover slowly'], 'Major progress has been made, but NOx emissions and global variation mean the problem is reduced, not solved.')],
    extended=[('The oxides of period 3 elements range from Na₂O to SO₃. (a) Describe the change in bonding and structure across the period. (b) Write equations for the reactions of Na₂O and SO₃ with water and state the approximate pH of each solution. (c) Explain why Al₂O₃ is described as amphoteric, with equations.', '(a) giant ionic (Na₂O, MgO, Al₂O₃) → giant covalent (SiO₂) → simple molecular (P₄O₁₀, SO₃). (b) Na₂O + H₂O → 2NaOH, pH 13–14; SO₃ + H₂O → H₂SO₄, pH 0–1. (c) Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; Al₂O₃ + 2NaOH + 3H₂O → 2NaAl(OH)₄.', 8, 'multi_step')],
))


@R.add('ch01-st3', 'C3', (1, 4), 'mcq')
def c3_oxide_nature(rng, slot):
    o = pick(rng, OXIDES)
    right = o[2]
    stem = pick(rng, [f'Which term best describes the acid-base character of {o[1]}, {chem(o[0])}?', f'How would {chem(o[0])} be classified?'])
    return mcq(rng, stem, right, [x for x in ['basic', 'amphoteric', 'acidic', 'neutral'] if x != right], f'{chem(o[0])}: {o[3]}; {right}.')


@R.add('ch01-st3', 'C3', (1, 4), 'mcq')
def c3_oxide_ph(rng, slot):
    pool = rng.sample(OXIDES, 4)
    kind = rng.choice(['highest', 'lowest'])
    best = (max if kind == 'highest' else min)(pool, key=lambda o: o[5])
    if [o[5] for o in pool].count(best[5]) > 1:
        return None
    stem = f'Equal amounts of {_lst(chem(o[0]) for o in pool)} are each added to separate beakers of water. Which beaker has the {kind} pH?'
    return mcq(rng, stem, chem(best[0]), [chem(o[0]) for o in pool if o != best], 'Approximate pH: ' + ', '.join(f'{chem(o[0])} {o[5]}' for o in pool) + ' (insoluble oxides leave water at about 7).')


@R.add('ch01-st3', 'C3', (1, 4), 'short')
def c3_oxide_eq(rng, slot):
    o = pick(rng, OXIDES)
    if o[0] == 'Al2O3':
        k = rng.randrange(2)
        stem = f'Write a balanced equation for the reaction of aluminium oxide with {"hydrochloric acid" if k == 0 else "aqueous sodium hydroxide"}.'
        ans = eqp(o[6].split('; ')[k])
    elif 'insoluble' in o[4] or rng.random() < 0.4:
        stem = f'Write a balanced equation for the reaction of {o[1]} with {"aqueous sodium hydroxide" if o[2] != "basic" else "hydrochloric acid"}.'
        ans = eqp(o[6])
    else:
        stem = f'Write a balanced equation, with state symbols, for the reaction of {o[1]} with water and state whether the solution formed is acidic or alkaline.'
        ans = eqp(o[4]) + f'; {"alkaline" if o[2] == "basic" else "acidic"}'
    return dict(stem=stem, answer=ans, markingKey=f'Correct formulae (1); balanced (1). {ans}', type='short', marks=2)


@R.add('ch01-st3', 'C3', (2, 5), 'numerical')
def c3_oxide_neutralise(rng, slot):
    f, coef_acid, acid = pick(rng, [('MgO', 2, 'HCl'), ('CaO', 2, 'HCl'), ('Na2O', 2, 'HCl'), ('MgO', 1, 'H2SO4'), ('CaO', 1, 'H2SO4'), ('Al2O3', 6, 'HCl'), ('ZnO', 2, 'HCl')])
    c = rng.choice([0.100, 0.200, 0.250, 0.500, 1.00, 2.00])
    m = round(rng.uniform(0.2, 3.0), 2)
    n_ox = m / mr(f)
    V = n_ox * coef_acid / c * 1000
    nm = {'MgO': 'magnesium oxide', 'CaO': 'calcium oxide', 'Na2O': 'sodium oxide', 'Al2O3': 'aluminium oxide', 'ZnO': 'zinc oxide'}[f]
    an = {'HCl': 'hydrochloric acid', 'H2SO4': 'sulfuric acid'}[acid]
    stem = pick(rng, [f'Calculate the volume, in cm³, of {sf(c)} mol dm⁻³ {an} needed to react exactly with {m:.2f} g of {nm}.',
                      f'A {m:.2f} g sample of the basic oxide {chem(f)} is neutralised by {sf(c)} mol dm⁻³ {an}. Determine the minimum volume of acid required.'])
    if f == 'Al2O3' and rng.random() < 0.5:
        stem = f'Aluminium oxide is amphoteric. Calculate the volume of {sf(c)} mol dm⁻³ hydrochloric acid that reacts with {m:.2f} g of Al₂O₃: Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O.'
    return num(stem, q(V, 'cm³'), f'n({chem(f)}) = {m:.2f}/{mr(f):.2f} = {sf(n_ox)} mol (M1); n(acid) = {coef_acid} × n = {sf(n_ox * coef_acid)} mol (M1); V = n/c = {q(V, "cm³")} (A1).', 3)


@R.add('ch01-st3', 'C3', (2, 4), 'numerical')
def c3_rain_ph(rng, slot):
    ph1 = round(rng.uniform(5.6, 6.0), 1)
    ph2 = round(rng.uniform(3.8, 4.8), 1)
    f = 10 ** (ph1 - ph2)
    city = pick(rng, CITIES)
    stem = pick(rng, [f'Unpolluted rain has a pH of about {ph1}. Rain collected near a coal-fired power station outside {city} had a pH of {ph2}. Calculate how many times greater [H⁺] is in the polluted rain.',
                      f'The pH of rain in {city} fell from {ph1} to {ph2} over several decades. By what factor did the hydrogen ion concentration increase?'])
    return num(stem, sf(f, 2), f'[H⁺] = 10⁻ᵖᴴ; ratio = 10^({ph1} − {ph2}) (M1) = {sf(f, 2)} (A1).', 2)


R.mcqs('ch01-st3', 'C2', (1, 4), [
    ('Why does sodium oxide form an alkaline solution in water?', 'Its oxide ions accept protons from water, forming hydroxide ions.', ['It releases H⁺ ions.', 'It is a covalent molecule.', 'Sodium ions react with water to form H₂.'], 'O²⁻ + H₂O → 2OH⁻.'),
    ('Why is silicon dioxide classed as an acidic oxide although it does not dissolve in water?', 'It reacts with bases such as hot concentrated sodium hydroxide to form a salt.', ['It forms carbonic acid.', 'It reacts with hydrochloric acid.', 'It contains H⁺ ions.'], 'SiO₂ + 2NaOH → Na₂SiO₃ + H₂O.'),
    ('Which change in bonding occurs across the period 3 oxides?', 'ionic to covalent', ['covalent to ionic', 'metallic to ionic', 'no change'], 'Electronegativity difference with O decreases.'),
    ('How does calcium carbonate neutralise acid rain in lakes?', 'CaCO₃ reacts with H⁺ ions to form Ca²⁺, water and carbon dioxide.', ['It absorbs SO₂ from the air above the lake.', 'It forms a protective layer on the water.', 'It oxidises sulfurous acid.'], 'CaCO₃ + 2H⁺ → Ca²⁺ + H₂O + CO₂.'),
])


@p1b(R, 'ch01-st3')
def p1b_oxide_titration(rng, slot):
    f, nm, ctx = pick(rng, [('MgO', 'magnesium oxide', 'a powdered antacid'), ('CaO', 'calcium oxide', 'a sample of quicklime'), ('ZnO', 'zinc oxide', 'a zinc oxide cream base'),
                            ('MgO', 'magnesium oxide', 'a batch of refractory powder'), ('CaO', 'calcium oxide', 'a lime fertiliser')])
    m = round(rng.uniform(0.30, 0.60), 3)
    purity = rng.uniform(0.86, 0.97)
    va, ca = pick(rng, [(50.00, 0.500), (40.00, 0.600), (50.00, 0.400), (25.00, 1.000)])
    nacid = va / 1000 * ca
    n_ox = m * purity / mr(f)
    left = nacid - 2 * n_ox
    if left <= 0:
        return None
    vflask, aliq = pick(rng, [(250.0, 25.00), (100.0, 10.00), (250.0, 50.00), (100.0, 20.00)])
    fac = vflask / aliq
    cb = pick(rng, [0.100, 0.150, 0.200])
    titre = round(left / fac / cb * 1000, 2)
    if not 8 < titre < 48:
        return None
    n_left = cb * titre / 1000 * fac
    n_ox_calc = (nacid - n_left) / 2
    pur = n_ox_calc * mr(f) / m * 100
    who = name(rng)
    intro = (f'{who} analysed {ctx} containing {nm}. A {m:.3f} g sample was dissolved in {va:.2f} cm³ of {ca:.3f} mol dm⁻³ hydrochloric acid (an excess). The solution was made up to {vflask:.1f} cm³, and {aliq:.2f} cm³ portions were titrated with {cb:.3f} mol dm⁻³ sodium hydroxide. '
             f'The mean titre was {titre:.2f} cm³.')
    parts = [('Calculate the amount, in mol, of HCl remaining in the {:.1f} cm³ solution.'.format(vflask), f'{sf(n_left)} mol', f'n(NaOH) = {cb:.3f} × {titre / 1000:.5f} = {sf(cb * titre / 1000)} mol (M1); × {fac:g} = {sf(n_left)} mol (A1).', 2),
             (f'Determine the amount of {chem(f)} in the sample and its percentage purity.', f'{sf(n_ox_calc)} mol; {pur:.1f} %', f'n(HCl) reacted = {sf(nacid)} − {sf(n_left)} = {sf(nacid - n_left)} mol (M1); n({chem(f)}) = half = {sf(n_ox_calc)} mol (M1); purity = {sf(n_ox_calc * mr(f))}/{m:.3f} × 100 = {pur:.1f} % (A1).', 3)]
    pool = [('Explain why a back titration is used rather than titrating the oxide directly with acid.', f'{cap(nm)} is a sparingly soluble solid, so it reacts slowly and its end point would be hard to detect directly.', 'Insoluble / slow-reacting solid (1); end point unclear in direct titration (1).', 2),
            ('State one assumption made in this calculation.', 'The impurities do not react with hydrochloric acid.', 'Impurities unreactive with acid (1).', 1),
            (f'Write an equation for the reaction of {nm} with hydrochloric acid.', eqp(f'{f}(s) + 2HCl(aq) → {f[:-1]}Cl2(aq) + H2O(l)'), 'Balanced equation (1).', 1),
            (f'State, with a reason, whether {nm} is a basic or an amphoteric oxide.', 'amphoteric – it reacts with both acids and bases' if f == 'ZnO' else 'basic – it reacts with acids to form a salt and water but not with bases', 'classification with reason (1).', 1),
            ('Suggest a suitable indicator for the titration and state the colour change.', 'phenolphthalein: colourless to pink (strong acid–strong base)', 'indicator and colour change (1).', 1),
            ('Calculate the percentage uncertainty in the titre if each burette reading is ±0.05 cm³.', f'{0.10 / titre * 100:.2f} %', f'0.10/{titre:.2f} × 100 (1).', 1)]
    rng.shuffle(pool)
    return dict(intro=intro, parts=parts + pool[:2], extras=pool[2:])


# ---- ch01-st4 oxidation states and transition elements ----
COMPLEX = [('[Fe(H2O)6]^2+', 'Fe', 2, 6, 'H₂O', 'pale green'), ('[Fe(H2O)6]^3+', 'Fe', 3, 6, 'H₂O', 'yellow-brown'),
           ('[Cu(H2O)6]^2+', 'Cu', 2, 6, 'H₂O', 'blue'), ('[Cu(NH3)4(H2O)2]^2+', 'Cu', 2, 6, 'NH₃ and H₂O', 'deep blue'),
           ('[CuCl4]^2-', 'Cu', 2, 4, 'Cl⁻', 'yellow-green'), ('[Co(H2O)6]^2+', 'Co', 2, 6, 'H₂O', 'pink'),
           ('[CoCl4]^2-', 'Co', 2, 4, 'Cl⁻', 'blue'), ('[Fe(CN)6]^3-', 'Fe', 3, 6, 'CN⁻', 'red-orange'),
           ('[Fe(CN)6]^4-', 'Fe', 2, 6, 'CN⁻', 'yellow'), ('[Ag(NH3)2]^+', 'Ag', 1, 2, 'NH₃', 'colourless'),
           ('[Cr(H2O)6]^3+', 'Cr', 3, 6, 'H₂O', 'violet/green'), ('[Ni(H2O)6]^2+', 'Ni', 2, 6, 'H₂O', 'green'),
           ('[Zn(H2O)6]^2+', 'Zn', 2, 6, 'H₂O', 'colourless'), ('[Ni(NH3)6]^2+', 'Ni', 2, 6, 'NH₃', 'blue-violet'),
           ('[Fe(SCN)(H2O)5]^2+', 'Fe', 3, 6, 'SCN⁻ and H₂O', 'blood red'), ('[Mn(H2O)6]^2+', 'Mn', 2, 6, 'H₂O', 'very pale pink')]
LIG_CH = {'H2O': 0, 'NH3': 0, 'Cl': -1, 'CN': -1, 'SCN': -1}


def cx(f):
    return chem(f)


OX_SPECIES = [('MnO4^-', 'Mn', 7), ('MnO4^2-', 'Mn', 6), ('Cr2O7^2-', 'Cr', 6), ('CrO4^2-', 'Cr', 6), ('VO2^+', 'V', 5), ('VO^2+', 'V', 4),
              ('Fe2O3', 'Fe', 3), ('Fe3O4', 'Fe', None), ('SO4^2-', 'S', 6), ('SO3^2-', 'S', 4), ('S2O3^2-', 'S', 2), ('NO3^-', 'N', 5),
              ('NO2^-', 'N', 3), ('NH4^+', 'N', -3), ('ClO3^-', 'Cl', 5), ('ClO^-', 'Cl', 1), ('H2O2', 'O', -1), ('PO4^3-', 'P', 5),
              ('Cu2O', 'Cu', 1), ('TiO2', 'Ti', 4), ('K2FeO4', 'Fe', 6), ('N2O4', 'N', 4), ('IO3^-', 'I', 5), ('MnO2', 'Mn', 4)]


def oxs(v):
    return f'+{v}' if v > 0 else ('0' if v == 0 else f'−{-v}')


R.facts('ch01-st4', F(
    terms=[('transition element', 'an element that has an incomplete d sublevel in its atom or in one of its common ions'),
           ('ligand', 'a molecule or negative ion with a lone pair of electrons that forms a coordination bond to a central metal ion'),
           ('coordination number', 'the number of coordination bonds from ligands to the central metal ion in a complex'),
           ('complex ion', 'a central metal ion surrounded by ligands bonded to it by coordination bonds'),
           ('oxidation state', 'the charge an atom would have if all its bonds were ionic; shown with a sign before the number, e.g. +3'),
           ('paramagnetic', 'attracted into a magnetic field because the substance contains unpaired electrons'),
           ('diamagnetic', 'weakly repelled by a magnetic field because all the electrons are paired')],
    facts=[('Which element is NOT a transition element according to the IUPAC definition?', 'zinc', ['iron', 'copper', 'chromium'], 'Zn and Zn²⁺ have a full 3d¹⁰ sublevel.'),
           ('What is the coordination number of the metal in [Cu(H₂O)₆]²⁺?', '6', ['2', '4', '8'], 'Six water ligands.'),
           ('Why are many transition metal complexes coloured?', 'Light is absorbed as electrons move between split d orbitals.', ['Light is emitted as electrons fall to the ground state.', 'The ligands are coloured.', 'The d orbitals are full.'], 'd–d transitions; complementary colour seen.'),
           ('Which ion is colourless in aqueous solution?', 'Zn²⁺', ['Cu²⁺', 'Fe³⁺', 'Ni²⁺'], 'd¹⁰ – no d–d transition possible.'),
           ('Which property is characteristic of transition elements?', 'variable oxidation states', ['low melting points', 'only one stable ion', 'colourless compounds'], 'Similar energies of 3d and 4s electrons.'),
           ('What is the oxidation state of manganese in KMnO₄?', '+7', ['+2', '+4', '+6'], 'K +1, O −2 ×4 → Mn +7.')],
    why=[('Explain why transition elements show variable oxidation states.', 'The 3d and 4s electrons have similar energies, so different numbers of them can be lost (or used in bonding) without a very large jump in ionisation energy.'),
         ('Explain why transition metal complexes are often coloured.', 'Ligands split the d orbitals into two sets of slightly different energy; an electron absorbs visible light of energy matching the gap and is promoted; the colour seen is the complementary colour of the light absorbed.'),
         ('Explain why scandium is not usually regarded as forming coloured compounds although it is a d-block element.', 'Its only common ion, Sc³⁺, has no d electrons (3d⁰), so no d–d transitions are possible and its compounds are colourless.'),
         ('Explain why transition metals and their compounds are often good catalysts.', 'They can change oxidation state easily and provide surfaces/d orbitals that adsorb reactants, weakening bonds and offering an alternative pathway of lower activation energy.'),
         ('Explain why the Fe³⁺ ion is more stable than might be expected.', 'Fe³⁺ has the configuration [Ar] 3d⁵ – a half-filled d sublevel with one electron in each orbital, which minimises electron–electron repulsion.'),
         ('Explain how a ligand forms a bond to a transition metal ion.', 'The ligand donates a lone pair of electrons into an empty orbital of the metal ion, forming a coordination (dative covalent) bond.')],
    contrast=[('a paramagnetic substance', 'a diamagnetic substance', 'Paramagnetic substances have unpaired electrons and are attracted into a magnetic field; diamagnetic substances have all electrons paired and are weakly repelled.'),
              ('oxidation state', 'ionic charge', 'An oxidation state is a formal value assigned to an atom in any species (even covalent ones); an ionic charge is the actual charge on an ion.'),
              ('a ligand', 'a central metal ion', 'A ligand is a lone-pair donor (Lewis base); the central metal ion accepts the lone pairs (Lewis acid) into its empty orbitals.')],
    misc=[('Zinc is a transition element because it is in the d-block.', 'Zinc has a full 3d¹⁰ sublevel in both the atom and its only ion Zn²⁺, so it does not meet the definition of a transition element.'),
          ('Copper sulfate solution is blue because it emits blue light.', 'It absorbs light in the red-orange region (d–d transition) and transmits the complementary blue light.'),
          ('When iron forms Fe²⁺, the electrons are removed from the 3d sublevel first.', 'The 4s electrons are lost first: Fe [Ar] 3d⁶ 4s² → Fe²⁺ [Ar] 3d⁶.')],
    apply=[('Deduce the oxidation state of chromium in the dichromate(VI) ion, Cr₂O₇²⁻.', '2x + 7(−2) = −2 → x = +6', 1),
           ('State the number of unpaired electrons in Fe³⁺ and predict whether its compounds are paramagnetic.', '5 unpaired (3d⁵); paramagnetic', 2),
           ('Name a ligand that can form two coordination bonds to a metal ion.', 'ethane-1,2-diamine (or ethanedioate) – a bidentate ligand', 1)],
    evaluate=[('Transition metals are essential to modern industrial chemistry.', ['catalysts: Fe (Haber), V₂O₅ (Contact), Ni (hydrogenation), Pt/Pd/Rh (catalytic converters)', 'structural metals and alloys (steel, titanium)', 'pigments and electronics'], ['many are scarce, expensive or toxic (Cr(VI), Ni, Co)', 'mining causes environmental damage', 'enzymes and organocatalysts can replace some uses'], 'They are central to many key processes, but sustainability and toxicity concerns are driving the search for alternatives and recycling.')],
    extended=[('Iron(III) chloride solution is yellow-brown and is paramagnetic. (a) Write the electron configuration of Fe³⁺. (b) Explain why the solution is coloured. (c) Explain why it is paramagnetic. (d) Suggest why a solution of Zn²⁺ ions is colourless and diamagnetic.', '(a) [Ar] 3d⁵. (b) water ligands split the 3d orbitals; visible light of energy matching the splitting is absorbed; complementary colour transmitted. (c) five unpaired 3d electrons. (d) Zn²⁺ is 3d¹⁰: no d–d transitions possible and all electrons paired.', 7, 'multi_step')],
))


@R.add('ch01-st4', 'C3', (1, 4), 'mcq')
def c3_complex_ox(rng, slot):
    f, m, ox, cn, lig, col = pick(rng, COMPLEX)
    wr = [oxs(x) for x in sorted({ox - 1, ox + 1, ox + 2, ox + 3, 0} - {ox}) if x >= 0]
    rng.shuffle(wr)
    stem = pick(rng, [f'What is the oxidation state of {ENAME[m]} in the complex ion {cx(f)}?', f'Deduce the oxidation state of the central metal ion in {cx(f)}.'])
    return mcq(rng, stem, oxs(ox), wr[:3], f'Ligand charges ({lig}) and overall charge of the complex give {m} = {oxs(ox)}.')


@R.add('ch01-st4', 'C3', (1, 4), 'mcq')
def c3_coord_no(rng, slot):
    f, m, ox, cn, lig, col = pick(rng, COMPLEX)
    wr = [str(x) for x in [2, 4, 6, 8, 3] if x != cn]
    rng.shuffle(wr)
    stem = f'What is the coordination number of {m} in {cx(f)}?'
    return mcq(rng, stem, str(cn), wr[:3], f'{cn} coordination bonds from the ligands ({lig}).')


@R.add('ch01-st4', 'C3', (1, 4), 'mcq')
def c3_species_ox(rng, slot):
    f, el, ox = pick(rng, [s for s in OX_SPECIES if s[2] is not None])
    wr = [oxs(x) for x in sorted({ox - 2, ox + 2, ox - 1, -ox if ox else 2, ox + 1} - {ox})]
    rng.shuffle(wr)
    stem = f'What is the oxidation state of {ENAME[el]} in {chem(f)}?'
    return mcq(rng, stem, oxs(ox), wr[:3], f'O = −2 (−1 in peroxides), H = +1, K = +1; the sum equals the overall charge of {chem(f)}, so {el} = {oxs(ox)}.')


TMI = [('Ti', 2), ('Ti', 3), ('V', 2), ('V', 3), ('Cr', 2), ('Cr', 3), ('Mn', 2), ('Mn', 3), ('Fe', 2), ('Fe', 3), ('Co', 2), ('Co', 3), ('Ni', 2), ('Cu', 1), ('Cu', 2), ('Zn', 2), ('Sc', 3)]


@R.add('ch01-st4', 'C3', (1, 4), 'mcq')
def c3_unpaired(rng, slot):
    el, ch = pick(rng, TMI)
    c = config_ion(Z[el], ch)
    u = unpaired(c)
    wr = [str(x) for x in sorted({0, 1, 2, 3, 4, 5} - {u})]
    rng.shuffle(wr)
    sym = f'{el}{sup(ch) if ch > 1 else ""}⁺'
    stem = pick(rng, [f'How many unpaired electrons are there in a gaseous {sym} ion?', f'A gaseous {sym} ion has how many unpaired electrons in its ground state?'])
    return mcq(rng, stem, str(u), wr[:3], f'{sym}: {cfg_short(c)} → {u} unpaired electron{"s" if u != 1 else ""} (Hund’s rule).')


@R.add('ch01-st4', 'C3', (1, 5), 'short')
def c3_tm_ion_props(rng, slot):
    el, ch = pick(rng, TMI)
    c = config_ion(Z[el], ch)
    u = unpaired(c)
    nd = dict(c).get('3d', 0)
    col = 'coloured' if 0 < nd < 10 else 'colourless'
    mag = 'paramagnetic' if u else 'diamagnetic'
    sym = f'{el}{sup(ch) if ch > 1 else ""}⁺'
    stem = f'For the {sym} ion: (a) write its electron configuration; (b) state the number of unpaired electrons; (c) predict whether its aqueous complexes are coloured and whether they are paramagnetic.'
    return dict(stem=stem, answer=f'(a) {cfg_short(c)}; (b) {u}; (c) {col}, {mag}', markingKey=f'(a) {cfg_short(c)} – 4s removed first (1). (b) {u} (1). (c) {col} because {"partially filled 3d allows d–d transitions" if col == "coloured" else "3d⁰ or 3d¹⁰ allows no d–d transitions"} (1); {mag} (1).', type='short', marks=4)


@R.add('ch01-st4', 'C3', (2, 4), 'numerical')
def c3_absorb_wavelength(rng, slot):
    lam = rng.choice([450, 480, 500, 530, 560, 580, 600, 620, 650, 690])
    E = 6.63e-34 * 3.00e8 / (lam * 1e-9) * NA / 1000
    comp = {450: 'yellow-orange', 480: 'orange', 500: 'red', 530: 'red-violet', 560: 'violet', 580: 'blue-violet', 600: 'blue', 620: 'blue-green', 650: 'green-blue', 690: 'green'}[lam]
    stem = f'A solution of a transition metal complex absorbs light most strongly at {lam} nm. Calculate the energy difference between the split d orbitals in kJ mol⁻¹.'
    return num(stem, q(E, 'kJ mol⁻¹'), f'E = hc/λ = 6.63 × 10⁻³⁴ × 3.00 × 10⁸ / {lam} × 10⁻⁹ = {sf(E * 1000 / NA)} J per ion (M1); × 6.02 × 10²³ / 1000 = {q(E, "kJ mol⁻¹")} (A1). The solution appears approximately {comp} (complementary colour).', 2)


R.mcqs('ch01-st4', 'C2', (1, 4), [
    ('Why is Zn²⁺(aq) colourless?', 'Its 3d sublevel is full, so no d–d electron transitions can occur.', ['It has no d electrons at all.', 'It absorbs all visible light.', 'Water is not a ligand for zinc.'], '3d¹⁰.'),
    ('Why does changing the ligand often change the colour of a complex?', 'Different ligands split the d orbitals by different amounts, changing the wavelength absorbed.', ['Ligands emit light of different colours.', 'The oxidation state of the metal always changes.', 'The number of d electrons doubles.'], 'Splitting depends on the ligand.'),
    ('Why does iron form both Fe²⁺ and Fe³⁺ ions?', 'The 4s and 3d electrons are close in energy, so either two or three can be lost.', ['Iron has two different isotopes.', 'Fe³⁺ has a full 3d sublevel.', 'Iron is in group 2 and group 3.'], 'Similar energies of 3d and 4s.'),
    ('Which property makes transition metals effective heterogeneous catalysts?', 'They can adsorb reactant molecules onto their surface using d orbitals.', ['They have very low densities.', 'They have full d sublevels.', 'They always increase ΔH of the reaction.'], 'Adsorption weakens reactant bonds.'),
])

R.f['ch01-st1'].evaluate.append(('Mendeleev deserves more credit for the periodic table than any later chemist.', ['left gaps and predicted properties of undiscovered elements (eka-silicon = germanium)', 'reordered elements (Te/I) by properties rather than strictly by mass'], ['Moseley showed atomic number, not mass, is the ordering principle', 'quantum theory later explained why the pattern exists', 'others (Meyer, Newlands) produced similar arrangements'], 'Mendeleev’s predictive table was a decisive step, but the modern table rests on later work on atomic number and electron structure.'))
R.f['ch01-st2'].evaluate.append(('Electronegativity is a less useful idea than ionisation energy because it cannot be measured directly.', ['IE is a measured, well-defined quantity', 'electronegativity values depend on the scale used (Pauling, Mulliken)'], ['electronegativity predicts bond polarity and bond type, which IE does not', 'it underpins the bonding triangle and explains reactivity patterns'], 'Both are useful: IE is more rigorous, but electronegativity is the more practical tool for predicting bonding.'))
R.f['ch01-st3'].evaluate.append(('Ocean acidification is a more serious long-term threat than acid rain.', ['affects all oceans globally and is directly linked to rising CO₂', 'harms shell- and coral-forming organisms and marine food chains', 'very slow to reverse'], ['acid rain has caused severe local damage to forests, lakes and buildings', 'acid rain is still a problem in some industrial regions'], 'Acid rain is a more local and more controllable problem; ocean acidification is global and harder to reverse, so in the long term it is the more serious one.'))
R.f['ch01-st4'].evaluate.append(('The colours of transition metal compounds are simply a property of the metal.', ['the number of d electrons (oxidation state) of the metal is essential', 'd⁰ and d¹⁰ ions are colourless whatever the ligand'], ['the ligand changes the d-orbital splitting and so the colour ([Cu(H₂O)₆]²⁺ blue, [CuCl₄]²⁻ yellow-green)', 'coordination number and geometry also change the colour'], 'Colour depends on the metal, its oxidation state, the ligands and the geometry together.'))


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step')
def c4_trend_data(rng, slot):
    grp = pick(rng, [['Li', 'Na', 'K', 'Rb', 'Cs'], ['Be', 'Mg', 'Ca', 'Sr', 'Ba'], ['F', 'Cl', 'Br', 'I'], ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl']])
    hide = pick(rng, grp[1:-1])
    rows = '\n'.join(f'{e} | {ATR[e] if e != hide else "?"}' for e in grp)
    down = grp[0] in ('Li', 'Be', 'F')
    lo, hi = ATR[grp[grp.index(hide) - 1]], ATR[grp[grp.index(hide) + 1]]
    stem = (f'The atomic radii (pm) of some elements are shown.\n\nelement | atomic radius / pm\n{rows}\n\n'
            f'(a) Estimate the atomic radius of {ENAME[hide]}. (b) Explain the trend shown in the table. (c) Predict, with a reason, how the first ionisation energies of these elements vary. '
            f'(d) Suggest why ionic radii, rather than atomic radii, are used to explain the lattice enthalpies of their compounds.')
    trend = 'increases down the group: more occupied shells, outer electrons further from the nucleus, more shielding' if down else 'decreases across the period: nuclear charge increases while electrons enter the same shell with similar shielding'
    return dict(stem=stem, answer=f'(a) between {min(lo, hi)} and {max(lo, hi)} pm (actual {ATR[hide]} pm); (b) radius {trend}; (c) IE {"decreases down the group" if down else "generally increases across the period"}.',
                markingKey=f'(a) value between {min(lo, hi)} and {max(lo, hi)} pm (A1). (b) {trend} (R1 R1). (c) IE {"decreases" if down else "increases (with small dips at Al and S)"} – outer electron {"less" if down else "more"} strongly attracted (R1). (d) in ionic compounds the ions, not atoms, are present; ionic radius sets the distance between charges (R1).', type='multi_step', marks=6)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def c4_complex_unknown(rng, slot):
    f, m, ox, cn, lig, col = pick(rng, [c for c in COMPLEX if c[5] != 'colourless'])
    c = config_ion(Z[m], ox)
    u = unpaired(c)
    stem = (f'A student prepares the complex ion {cx(f)}, which is {col} in solution. (a) Deduce the oxidation state of {m} and write its electron configuration. (b) State the coordination number and the type of bond between the ligand and the metal. '
            f'(c) Explain the origin of the colour. (d) Predict, with a reason, whether the complex is paramagnetic.')
    return dict(stem=stem, answer=f'(a) {oxs(ox)}; {cfg_short(c)}. (b) {cn}; coordination (dative covalent) bonds. (c) d–d transitions in split 3d orbitals; complementary colour seen. (d) {"paramagnetic" if u else "diamagnetic"} ({u} unpaired)',
                markingKey=f'(a) {oxs(ox)} (A1); {cfg_short(c)} (A1). (b) {cn} (A1); ligand donates a lone pair (A1). (c) ligands split d orbitals; visible light absorbed promotes an electron; transmitted complementary colour (R1 R1). (d) {u} unpaired electrons → {"paramagnetic" if u else "diamagnetic"} (R1).', type='multi_step', marks=7)


# =============================================================================================
# ch02 S3.2 Functional groups: classification of organic compounds
# =============================================================================================
# name, condensed formula, molecular formula, class, degree (1/2/3 or None)
ORG = [
    ('methane', 'CH4', 'CH4', 'alkane', None), ('ethane', 'CH3CH3', 'C2H6', 'alkane', None), ('propane', 'CH3CH2CH3', 'C3H8', 'alkane', None),
    ('butane', 'CH3CH2CH2CH3', 'C4H10', 'alkane', None), ('2-methylpropane', 'CH3CH(CH3)CH3', 'C4H10', 'alkane', None),
    ('pentane', 'CH3CH2CH2CH2CH3', 'C5H12', 'alkane', None), ('2-methylbutane', 'CH3CH(CH3)CH2CH3', 'C5H12', 'alkane', None),
    ('2,2-dimethylpropane', 'C(CH3)4', 'C5H12', 'alkane', None), ('hexane', 'CH3(CH2)4CH3', 'C6H14', 'alkane', None),
    ('ethene', 'CH2=CH2', 'C2H4', 'alkene', None), ('propene', 'CH2=CHCH3', 'C3H6', 'alkene', None), ('but-1-ene', 'CH2=CHCH2CH3', 'C4H8', 'alkene', None),
    ('but-2-ene', 'CH3CH=CHCH3', 'C4H8', 'alkene', None), ('2-methylpropene', 'CH2=C(CH3)2', 'C4H8', 'alkene', None),
    ('ethyne', 'HC≡CH', 'C2H2', 'alkyne', None), ('propyne', 'HC≡CCH3', 'C3H4', 'alkyne', None),
    ('chloromethane', 'CH3Cl', 'CH3Cl', 'halogenoalkane', 1), ('bromoethane', 'CH3CH2Br', 'C2H5Br', 'halogenoalkane', 1),
    ('1-bromopropane', 'CH3CH2CH2Br', 'C3H7Br', 'halogenoalkane', 1), ('2-bromopropane', 'CH3CHBrCH3', 'C3H7Br', 'halogenoalkane', 2),
    ('1-chlorobutane', 'CH3CH2CH2CH2Cl', 'C4H9Cl', 'halogenoalkane', 1), ('2-chlorobutane', 'CH3CHClCH2CH3', 'C4H9Cl', 'halogenoalkane', 2),
    ('2-bromo-2-methylpropane', '(CH3)3CBr', 'C4H9Br', 'halogenoalkane', 3), ('1-iodobutane', 'CH3CH2CH2CH2I', 'C4H9I', 'halogenoalkane', 1),
    ('2-chloro-2-methylbutane', 'CH3CCl(CH3)CH2CH3', 'C5H11Cl', 'halogenoalkane', 3),
    ('methanol', 'CH3OH', 'CH4O', 'alcohol', 1), ('ethanol', 'CH3CH2OH', 'C2H6O', 'alcohol', 1), ('propan-1-ol', 'CH3CH2CH2OH', 'C3H8O', 'alcohol', 1),
    ('propan-2-ol', 'CH3CH(OH)CH3', 'C3H8O', 'alcohol', 2), ('butan-1-ol', 'CH3CH2CH2CH2OH', 'C4H10O', 'alcohol', 1),
    ('butan-2-ol', 'CH3CH(OH)CH2CH3', 'C4H10O', 'alcohol', 2), ('2-methylpropan-2-ol', '(CH3)3COH', 'C4H10O', 'alcohol', 3),
    ('2-methylpropan-1-ol', '(CH3)2CHCH2OH', 'C4H10O', 'alcohol', 1), ('pentan-3-ol', 'CH3CH2CH(OH)CH2CH3', 'C5H12O', 'alcohol', 2),
    ('methanal', 'HCHO', 'CH2O', 'aldehyde', None), ('ethanal', 'CH3CHO', 'C2H4O', 'aldehyde', None), ('propanal', 'CH3CH2CHO', 'C3H6O', 'aldehyde', None),
    ('butanal', 'CH3CH2CH2CHO', 'C4H8O', 'aldehyde', None),
    ('propanone', 'CH3COCH3', 'C3H6O', 'ketone', None), ('butanone', 'CH3COCH2CH3', 'C4H8O', 'ketone', None),
    ('pentan-2-one', 'CH3COCH2CH2CH3', 'C5H10O', 'ketone', None), ('pentan-3-one', 'CH3CH2COCH2CH3', 'C5H10O', 'ketone', None),
    ('methanoic acid', 'HCOOH', 'CH2O2', 'carboxylic acid', None), ('ethanoic acid', 'CH3COOH', 'C2H4O2', 'carboxylic acid', None),
    ('propanoic acid', 'CH3CH2COOH', 'C3H6O2', 'carboxylic acid', None), ('butanoic acid', 'CH3CH2CH2COOH', 'C4H8O2', 'carboxylic acid', None),
    ('methyl ethanoate', 'CH3COOCH3', 'C3H6O2', 'ester', None), ('ethyl ethanoate', 'CH3COOCH2CH3', 'C4H8O2', 'ester', None),
    ('ethyl methanoate', 'HCOOCH2CH3', 'C3H6O2', 'ester', None), ('methyl propanoate', 'CH3CH2COOCH3', 'C4H8O2', 'ester', None),
    ('propyl ethanoate', 'CH3COOCH2CH2CH3', 'C5H10O2', 'ester', None),
    ('methylamine', 'CH3NH2', 'CH5N', 'amine', None), ('ethylamine', 'CH3CH2NH2', 'C2H7N', 'amine', None), ('propan-1-amine', 'CH3CH2CH2NH2', 'C3H9N', 'amine', None),
    ('ethanamide', 'CH3CONH2', 'C2H5NO', 'amide', None), ('propanamide', 'CH3CH2CONH2', 'C3H7NO', 'amide', None),
    ('methoxymethane', 'CH3OCH3', 'C2H6O', 'ether', None), ('methoxyethane', 'CH3OCH2CH3', 'C3H8O', 'ether', None),
    ('ethanenitrile', 'CH3CN', 'C2H3N', 'nitrile', None), ('propanenitrile', 'CH3CH2CN', 'C3H5N', 'nitrile', None),
    ('benzene', 'C6H6', 'C6H6', 'arene', None), ('methylbenzene', 'C6H5CH3', 'C7H8', 'arene', None),
]
ORGN = {o[0]: o for o in ORG}
FG = {'alkane': ('none (C–C and C–H only)', 'alkyl'), 'alkene': ('C=C', 'alkenyl'), 'alkyne': ('C≡C', 'alkynyl'), 'halogenoalkane': ('C–X (X = halogen)', 'halogeno'),
      'alcohol': ('–OH', 'hydroxyl'), 'aldehyde': ('–CHO', 'carbonyl (aldehyde)'), 'ketone': ('C=O between two carbons', 'carbonyl (ketone)'),
      'carboxylic acid': ('–COOH', 'carboxyl'), 'ester': ('–COO–', 'ester'), 'amine': ('–NH₂', 'amino'), 'amide': ('–CONH₂', 'amido'),
      'ether': ('C–O–C', 'ether'), 'nitrile': ('–C≡N', 'nitrile'), 'arene': ('benzene ring', 'phenyl')}
SUFFIX = {'alkane': '-ane', 'alkene': '-ene', 'alkyne': '-yne', 'alcohol': '-ol', 'aldehyde': '-al', 'ketone': '-one', 'carboxylic acid': '-oic acid',
          'amine': '-amine', 'amide': '-amide', 'nitrile': '-nitrile', 'ester': '-oate', 'halogenoalkane': 'prefix chloro-/bromo-/iodo-', 'ether': 'alkoxy- prefix'}
GENF = {'alkane': 'CₙH₂ₙ₊₂', 'alkene': 'CₙH₂ₙ', 'alkyne': 'CₙH₂ₙ₋₂', 'alcohol': 'CₙH₂ₙ₊₁OH', 'aldehyde': 'CₙH₂ₙO', 'ketone': 'CₙH₂ₙO',
        'carboxylic acid': 'CₙH₂ₙO₂', 'ester': 'CₙH₂ₙO₂', 'halogenoalkane': 'CₙH₂ₙ₊₁X', 'amine': 'CₙH₂ₙ₊₁NH₂'}
CLASSES = sorted(FG)


def oc(o):
    return chem(o[1])


R.facts('ch02-st1', F(
    terms=[('homologous series', 'a family of compounds with the same functional group and general formula, in which successive members differ by CH₂ and show a gradual trend in physical properties'),
           ('functional group', 'the atom or group of atoms in a molecule that is responsible for its characteristic chemical reactions'),
           ('saturated', 'containing only single carbon–carbon bonds'),
           ('unsaturated', 'containing at least one carbon–carbon double or triple bond'),
           ('aromatic', 'containing a benzene ring (delocalised π system of six electrons)'),
           ('primary alcohol', 'an alcohol in which the carbon bonded to the –OH group is attached to only one other carbon atom'),
           ('tertiary halogenoalkane', 'a halogenoalkane in which the carbon bonded to the halogen is attached to three other carbon atoms')],
    facts=[('Which functional group is present in all carboxylic acids?', '–COOH', ['–OH only', '–CHO', '–COO–'], 'Carboxyl group.'),
           ('Successive members of a homologous series differ by', 'CH₂', ['CH₃', 'CH', 'C₂H₄'], 'One methylene unit.'),
           ('Which compound is unsaturated?', 'propene', ['propane', 'propan-1-ol', 'propanoic acid'], 'Contains C=C.'),
           ('Which class of compound contains the –CONH₂ group?', 'amides', ['amines', 'esters', 'nitriles'], 'Amido group.'),
           ('Which term describes 2-methylpropan-2-ol?', 'a tertiary alcohol', ['a primary alcohol', 'a secondary alcohol', 'an aldehyde'], 'C–OH carbon bonded to three C atoms.'),
           ('How does the boiling point change along a homologous series?', 'it increases as chain length increases', ['it decreases', 'it is constant', 'it alternates'], 'Stronger London forces with more electrons.')],
    why=[('Explain why members of a homologous series have similar chemical properties.', 'They have the same functional group, which is the reactive part of the molecule, so they undergo the same types of reaction.'),
         ('Explain why the boiling points of the alkanes increase with chain length.', 'Each extra CH₂ adds electrons and surface area, so London (dispersion) forces between molecules become stronger and more energy is needed to separate them.'),
         ('Explain why ethanol has a much higher boiling point than propane although their molar masses are similar.', 'Ethanol molecules form hydrogen bonds through their –OH groups; propane molecules are held only by weak London forces.'),
         ('Explain why branched alkanes have lower boiling points than their straight-chain isomers.', 'Branching makes molecules more compact with smaller surface contact, so London forces between molecules are weaker.'),
         ('Explain why the lower members of the alcohols are soluble in water but the higher members are not.', 'The –OH group forms hydrogen bonds with water, but as the non-polar hydrocarbon chain lengthens, it disrupts water’s hydrogen bonding and solubility falls.')],
    contrast=[('an aldehyde', 'a ketone', 'In an aldehyde the carbonyl group is at the end of the chain (–CHO, bonded to at least one H); in a ketone it is between two carbon atoms.'),
              ('a carboxylic acid', 'an ester', 'A carboxylic acid contains –COOH (with an O–H); an ester contains –COO– linking two carbon groups and has no O–H.'),
              ('an amine', 'an amide', 'An amine has N bonded to carbon and hydrogen (–NH₂); an amide has the nitrogen bonded to a carbonyl carbon (–CONH₂).'),
              ('a saturated compound', 'an unsaturated compound', 'A saturated compound has only single C–C bonds; an unsaturated one has at least one C=C or C≡C bond.')],
    misc=[('Propanone and propanal are in the same homologous series because they have the same molecular formula.', 'They are functional group isomers: propanal is an aldehyde and propanone a ketone, so they belong to different series.'),
          ('Benzene is unsaturated so it behaves like an alkene.', 'Benzene’s π electrons are delocalised, making it much more stable; it usually undergoes substitution, not addition.'),
          ('All compounds containing an –OH group are alcohols.', 'Carboxylic acids (–COOH) and phenols also contain O–H but are not alcohols; an alcohol has –OH on an sp³ carbon.')],
    apply=[('Deduce the molecular formula of the alcohol with five carbon atoms and state its general formula.', 'C₅H₁₁OH (C₅H₁₂O); CₙH₂ₙ₊₁OH', 2),
           ('Classify butan-2-ol, 2-methylpropan-2-ol and butan-1-ol as primary, secondary or tertiary.', 'butan-2-ol secondary; 2-methylpropan-2-ol tertiary; butan-1-ol primary', 3),
           ('Identify the functional groups present in 2-hydroxypropanoic acid (lactic acid), CH₃CH(OH)COOH.', 'hydroxyl (secondary alcohol) and carboxyl', 2)],
    evaluate=[('Classifying organic compounds by functional group is more useful than classifying them by carbon skeleton.', ['functional group determines reactivity, so reactions can be predicted', 'IUPAC naming is organised around functional groups'], ['carbon skeleton determines physical properties, isomerism and shape', 'polyfunctional molecules belong to several classes'], 'Functional groups predict chemistry best, but a full description needs both classifications.'),
              ('Homologous series show that organic chemistry is fundamentally predictable.', ['gradual trends in physical properties', 'the same reactions apply to every member'], ['first members often behave anomalously (methanoic acid, methanal)', 'branching and isomerism change properties', 'multiple functional groups interact'], 'Homologous series make organic chemistry largely predictable, though the first members, branching and multiple functional groups are important exceptions.')],
    extended=[('Compound X, C₃H₆O, does not react with sodium but forms a yellow-orange precipitate with 2,4-DNPH. (a) Draw two possible structures of X. (b) Name each and identify its class. (c) Suggest a chemical test to distinguish them. (d) Explain which has the higher boiling point.', '(a)/(b) propanal CH₃CH₂CHO (aldehyde) and propanone CH₃COCH₃ (ketone). (c) warm with acidified K₂Cr₂O₇ – propanal turns it orange → green, propanone no change (or Tollens’/Fehling’s). (d) similar (propanone 56 °C, propanal 48 °C) – both dipole–dipole; propanone’s more exposed C=O dipole gives slightly stronger attractions.', 6, 'multi_step')],
))


@R.add('ch02-st1', 'C3', (1, 4), 'mcq')
def c3_class_of(rng, slot):
    o = pick(rng, [x for x in ORG if x[3] not in ('arene',)])
    right = o[3]
    wr = [c for c in CLASSES if c != right and c != 'arene']
    rng.shuffle(wr)
    if right == 'aldehyde':
        wr = ['ketone'] + [w for w in wr if w != 'ketone']
    if right == 'ester':
        wr = ['carboxylic acid'] + [w for w in wr if w != 'carboxylic acid']
    stem = pick(rng, [f'To which class of organic compound does {oc(o)} belong?', f'The compound with the condensed structural formula {oc(o)} is'])
    return mcq(rng, stem, right if stem.startswith('To') else ('an ' if right[0] in 'aeiou' else 'a ') + right, [w if stem.startswith('To') else ('an ' if w[0] in 'aeiou' else 'a ') + w for w in wr[:3]], f'{oc(o)} ({o[0]}) contains {FG[right][0]}: {right}.')


@R.add('ch02-st1', 'C3', (1, 4), 'mcq')
def c3_degree(rng, slot):
    o = pick(rng, [x for x in ORG if x[4]])
    kind = {1: 'primary', 2: 'secondary', 3: 'tertiary'}[o[4]]
    cls = 'alcohol' if o[3] == 'alcohol' else 'halogenoalkane'
    wr = [x for x in ['primary', 'secondary', 'tertiary'] if x != kind] + ['not classifiable in this way']
    stem = f'Is {o[0]}, {oc(o)}, a primary, secondary or tertiary {cls}?'
    return mcq(rng, stem, kind, wr, f'The carbon bearing the {"–OH" if cls == "alcohol" else "halogen"} is bonded to {o[4]} other carbon atom{"s" if o[4] > 1 else ""} (methanol/chloromethane count as primary).')


@R.add('ch02-st1', 'C3', (1, 4), 'mcq')
def c3_next_member(rng, slot):
    cls = pick(rng, ['alkane', 'alkene', 'alcohol', 'aldehyde', 'carboxylic acid', 'alkyne'])
    n = rng.randint(2, 7)
    f = {'alkane': (n, 2 * n + 2, ''), 'alkene': (n, 2 * n, ''), 'alkyne': (n, 2 * n - 2, ''), 'alcohol': (n, 2 * n + 2, 'O'),
         'aldehyde': (n, 2 * n, 'O'), 'carboxylic acid': (n, 2 * n, 'O2')}
    def fs(k):
        c, h, o_ = f[cls] if k == n else {'alkane': (k, 2 * k + 2, ''), 'alkene': (k, 2 * k, ''), 'alkyne': (k, 2 * k - 2, ''), 'alcohol': (k, 2 * k + 2, 'O'), 'aldehyde': (k, 2 * k, 'O'), 'carboxylic acid': (k, 2 * k, 'O2')}[cls]
        return chem(f'C{c if c > 1 else ""}H{h}{o_}')
    right = fs(n + 1)
    c, h, o_ = f[cls]
    wr = [chem(f'C{n + 1}H{h + 1}{o_}'), chem(f'C{n + 1}H{h}{o_}'), chem(f'C{n + 2}H{h + 4}{o_}'), chem(f'C{n + 1}H{h + 3}{o_}')]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'A member of the {cls} homologous series has the molecular formula {fs(n)}. What is the molecular formula of the next member of the series?'
    return mcq(rng, stem, right, wr[:3], f'Successive members differ by CH₂: {fs(n)} + CH₂ = {right} (general formula {GENF[cls]}).')


@R.add('ch02-st1', 'C3', (1, 5), 'short')
def c3_fg_identify(rng, slot):
    o = pick(rng, ORG)
    stem = pick(rng, [f'Identify the functional group in {o[0]}, {oc(o)}, and state the homologous series to which it belongs.',
                      f'State the name of the functional group present in {oc(o)} and the class of compound.'])
    return dict(stem=stem, answer=f'{FG[o[3]][1]} group ({FG[o[3]][0]}); {o[3]}', markingKey=f'{FG[o[3]][1]} / {FG[o[3]][0]} (1); {o[3]} (1).', type='short', marks=2)


@R.add('ch02-st1', 'C3', (2, 4), 'numerical')
def c3_series_mr(rng, slot):
    cls = pick(rng, ['alkane', 'alcohol', 'carboxylic acid', 'aldehyde', 'alkene'])
    n = rng.randint(3, 9)
    f = {'alkane': f'C{n}H{2 * n + 2}', 'alcohol': f'C{n}H{2 * n + 1}OH', 'carboxylic acid': f'C{n - 1}H{2 * n - 1}COOH', 'aldehyde': f'C{n}H{2 * n}O', 'alkene': f'C{n}H{2 * n}'}[cls]
    M = mr(f)
    stem = f'A member of the {cls}s has a molar mass of {M:.2f} g mol⁻¹. Using the general formula {GENF[cls]}, determine the number of carbon atoms and write its molecular formula.'
    return num(stem, f'{n} C atoms; {chem(f)}', f'Mr of general formula in terms of n set equal to {M:.2f} (M1); n = {n} (A1); {chem(f)} (A1).', 3)


R.mcqs('ch02-st1', 'C2', (1, 4), [
    ('Why does butan-1-ol have a higher boiling point than pentane?', 'Butan-1-ol molecules form hydrogen bonds.', ['Butan-1-ol has a larger molar mass.', 'Pentane is branched.', 'Butan-1-ol has stronger covalent bonds.'], 'Hydrogen bonding via –OH.'),
    ('Why do ethanol and propan-1-ol react similarly with sodium?', 'They contain the same functional group.', ['They have the same molar mass.', 'They are isomers.', 'They have the same boiling point.'], 'Same –OH group.'),
    ('Which explains why the boiling points of straight-chain alkanes rise steadily?', 'London forces increase with the number of electrons.', ['Hydrogen bonding increases.', 'C–C bonds get stronger.', 'The molecules become more polar.'], 'More electrons → larger temporary dipoles.'),
    ('Why is methylbenzene classed as aromatic?', 'It contains a benzene ring with delocalised π electrons.', ['It has a pleasant smell.', 'It contains a methyl group.', 'It is unsaturated like an alkene.'], 'Aromatic = benzene ring.'),
])


# ---- ch02-st2 nomenclature and formulae ----
R.facts('ch02-st2', F(
    terms=[('molecular formula', 'a formula showing the actual number of atoms of each element in one molecule'),
           ('structural formula', 'a representation showing how the atoms in a molecule are bonded to one another'),
           ('skeletal formula', 'a simplified formula in which carbon atoms are at the ends and junctions of lines and hydrogen atoms bonded to carbon are not shown'),
           ('condensed structural formula', 'a formula showing the groups attached to each carbon in order along the chain, e.g. CH₃CH₂OH'),
           ('stereochemical formula', 'a 3D representation using wedges (towards the viewer) and dashes (away) to show the spatial arrangement of bonds'),
           ('parent chain', 'the longest continuous chain of carbon atoms containing the principal functional group, which gives the stem of the IUPAC name')],
    facts=[('What is the stem name for a chain of four carbon atoms?', 'but-', ['prop-', 'pent-', 'meth-'], 'meth, eth, prop, but, pent, hex.'),
           ('Which suffix indicates an aldehyde?', '-al', ['-ol', '-one', '-oic acid'], 'ethanal, propanal.'),
           ('What is the IUPAC name of CH₃COCH₃?', 'propanone', ['propanal', 'propan-2-ol', 'methyl ethanoate'], 'Ketone with three carbons.'),
           ('What is the IUPAC name of CH₃CH₂COOH?', 'propanoic acid', ['ethanoic acid', 'propanal', 'propyl methanoate'], 'Carboxylic acid, three carbons including C of COOH.'),
           ('In a skeletal formula, which atoms are usually not drawn?', 'hydrogen atoms bonded to carbon', ['carbon atoms in functional groups', 'oxygen atoms', 'all hydrogen atoms including O–H'], 'C–H hydrogens implied.'),
           ('Which name is correct for CH₃CH(CH₃)CH₂CH₃?', '2-methylbutane', ['3-methylbutane', 'pentane', '2-ethylpropane'], 'Longest chain 4, lowest locant.')],
    why=[('Explain why the name "3-methylbutane" is incorrect.', 'The chain must be numbered from the end giving the substituent the lowest locant, so the compound is 2-methylbutane.'),
         ('Explain why "1-methylpropane" is not a valid IUPAC name.', 'A methyl group on carbon 1 extends the longest chain to four carbons, so the compound is butane.'),
         ('Explain why a skeletal formula is useful for large organic molecules.', 'It shows the carbon skeleton and functional groups clearly without the clutter of every C and H, making structure and isomerism easier to see.'),
         ('Explain why the name of an ester has two parts.', 'An ester is formed from an alcohol and a carboxylic acid; the alkyl group from the alcohol is named first and the carboxylate (-oate) from the acid second, e.g. ethyl ethanoate.'),
         ('Explain why a molecular formula alone cannot identify an organic compound.', 'Many compounds (isomers) share the same molecular formula; a structural formula is needed to show how the atoms are connected.')],
    contrast=[('a molecular formula', 'an empirical formula', 'A molecular formula gives the actual number of each atom in a molecule; an empirical formula gives only the simplest whole-number ratio.'),
              ('a structural formula', 'a skeletal formula', 'A structural formula shows all atoms and bonds (or groups); a skeletal formula shows only the carbon skeleton as lines plus functional groups, omitting C and C–H atoms.'),
              ('propan-1-ol', 'propan-2-ol', 'Both C₃H₇OH: in propan-1-ol the –OH is on the end carbon (primary); in propan-2-ol it is on the middle carbon (secondary).')],
    misc=[('CH₃CH₂CH₂CH₃ should be named 1-methylpropane.', 'The longest chain has four carbons, so it is butane.'),
          ('Ethyl methanoate and methyl ethanoate are the same compound.', 'They are isomers: ethyl methanoate is HCOOCH₂CH₃, methyl ethanoate is CH₃COOCH₃.'),
          ('In a skeletal formula, the hydrogen of an –OH group is also omitted.', 'Only hydrogens bonded to carbon are omitted; the H of –OH (and N–H) is always shown.')],
    apply=[('Name the compound CH₃CH₂CH(CH₃)CH₂OH.', '2-methylbutan-1-ol', 2),
           ('Draw the skeletal formula of pentan-2-one and state its molecular formula.', 'zig-zag of five carbons with C=O at carbon 2; C₅H₁₀O', 2),
           ('Give the IUPAC name of the ester formed from propanoic acid and methanol.', 'methyl propanoate', 1),
           ('Name (CH₃)₂CHCH₂CH₂Br.', '1-bromo-3-methylbutane', 2)],
    evaluate=[('Systematic IUPAC names should completely replace common names in chemistry.', ['each name corresponds to one structure – unambiguous worldwide', 'names can be deduced from structures and vice versa'], ['names of large molecules become very long and impractical', 'common names (acetone, aspirin) are entrenched in industry and medicine', 'trade names are needed for products'], 'IUPAC names are essential for precision, but common names will remain alongside them for convenience.')],
    extended=[('A compound has the condensed formula CH₃CH(CH₃)CH(OH)CH₃. (a) Give its IUPAC name. (b) Draw its skeletal formula. (c) Write its molecular and empirical formulae. (d) State whether it is a primary, secondary or tertiary alcohol, with a reason.', '(a) 3-methylbutan-2-ol. (b) zig-zag of four carbons with a methyl branch on C3 and OH on C2. (c) C₅H₁₂O for both. (d) secondary – the C bearing OH is bonded to two other carbons.', 6, 'multi_step')],
))


@R.add('ch02-st2', 'C3', (1, 4), 'mcq')
def c3_name_from_formula(rng, slot):
    o = pick(rng, [x for x in ORG if x[3] not in ('arene',)])
    same = [x[0] for x in ORG if x[2] == o[2] and x[0] != o[0]]
    near = [x[0] for x in ORG if x[3] == o[3] and x[0] != o[0]]
    wr = list(dict.fromkeys(same + rng.sample(near, min(3, len(near)))))
    if len(wr) < 3:
        wr += rng.sample([x[0] for x in ORG if x[0] != o[0] and x[0] not in wr], 3 - len(wr))
    stem = pick(rng, [f'What is the IUPAC name of {oc(o)}?', f'Which is the correct systematic name for the compound {oc(o)}?'])
    return mcq(rng, stem, o[0], wr[:3], f'{oc(o)}: {o[3]} → {o[0]}.')


@R.add('ch02-st2', 'C3', (1, 4), 'mcq')
def c3_formula_from_name(rng, slot):
    o = pick(rng, [x for x in ORG if x[3] not in ('arene',)])
    others = [x for x in ORG if x[0] != o[0] and x[1] != o[1]]
    same = [x for x in others if x[2] == o[2]]
    wr = [oc(x) for x in same] + [oc(x) for x in rng.sample(others, 4)]
    wr = [w for w in dict.fromkeys(wr) if w != oc(o)]
    stem = f'Which is the condensed structural formula of {o[0]}?'
    return mcq(rng, stem, oc(o), wr[:3], f'{o[0]} = {oc(o)} ({chem(o[2])}).')


@R.add('ch02-st2', 'C3', (1, 4), 'mcq')
def c3_molecular_formula(rng, slot):
    o = pick(rng, ORG)
    a = atoms(o[2])
    right = chem(o[2])
    wr = []
    for dh in (2, -2, 1):
        b = dict(a)
        b['H'] = b['H'] + dh
        wr.append(chem(''.join(f'{e}{b[e] if b[e] > 1 else ""}' for e in b)))
    stem = f'What is the molecular formula of {o[0]}?'
    return mcq(rng, stem, right, [w for w in wr if w != right][:3], f'{oc(o)} → {right}.')


def ihd(f):
    a = atoms(f)
    c, h, n = a.get('C', 0), a.get('H', 0), a.get('N', 0)
    x = sum(a.get(e, 0) for e in ('F', 'Cl', 'Br', 'I'))
    return (2 * c + 2 + n - h - x) // 2


@R.add('ch02-st2', 'C3', (2, 4), 'mcq')
def c3_empirical(rng, slot):
    o = pick(rng, [x for x in ORG if 'N' not in x[2]])
    a = atoms(o[2])
    g = 0
    for v in a.values():
        g = math.gcd(g, v)
    emp = ''.join(f'{e}{a[e] // g if a[e] // g > 1 else ""}' for e in a)
    if g == 1:
        return None
    wr = [chem(o[2]), chem(''.join(f'{e}{a[e] // g * 2 if a[e] // g * 2 > 1 else ""}' for e in a)) if g != 2 else chem(''.join(f'{e}{a[e] + 1}' for e in a)), chem(''.join(f'{e}{max(1, a[e] - 1) if a[e] > 1 else ""}' for e in a))]
    wr = [w for w in dict.fromkeys(wr) if w != chem(emp)]
    if len(wr) < 3:
        wr.append(chem('CH'))
    stem = f'What is the empirical formula of {o[0]}, {chem(o[2])}?'
    return mcq(rng, stem, chem(emp), wr[:3], f'Divide by {g}: {chem(emp)}.')


@R.add('ch02-st2', 'C3', (1, 5), 'short')
def c3_name_short(rng, slot):
    o = pick(rng, [x for x in ORG if x[3] not in ('arene',)])
    if rng.random() < 0.5:
        stem = f'State the IUPAC name of {oc(o)} and identify its homologous series.'
        ans = f'{o[0]}; {o[3]}'
    else:
        stem = f'Draw the full structural formula of {o[0]} and write its molecular formula.'
        ans = f'structure of {oc(o)}; {chem(o[2])}'
    return dict(stem=stem, answer=ans, markingKey=f'{ans} (1 each).', type='short', marks=2)


R.mcqs('ch02-st2', 'C2', (1, 4), [
    ('Why is CH₃CH₂CH(CH₃)CH₃ named 2-methylbutane rather than 3-methylbutane?', 'The chain is numbered to give the substituent the lowest possible number.', ['The methyl group is always on carbon 2.', 'Butane has only two possible positions.', 'The longest chain has five carbons.'], 'Lowest locants rule.'),
    ('Which feature of a skeletal formula represents a carbon atom?', 'each end and each junction of the lines', ['each letter C', 'only the ends of lines', 'only junctions of three or more lines'], 'Vertices = C atoms.'),
    ('In "ethyl propanoate", which part of the name comes from the alcohol?', 'ethyl', ['propanoate', 'propan', 'oate'], 'Alkyl from alcohol, -oate from acid.'),
    ('Why does propan-2-ol need a number in its name while ethanol does not?', 'In propanol the –OH can be on more than one distinct carbon, giving isomers.', ['Ethanol has no isomers at all.', 'Numbers are only used for secondary alcohols.', 'Propan-2-ol has two –OH groups.'], 'Locant distinguishes position isomers.'),
])

R.f['ch02-st2'].evaluate.append(('Skeletal formulae are the best way to represent organic molecules.', ['quick to draw and read for large molecules', 'make the carbon skeleton and functional groups obvious', 'standard in research and pharmacology'], ['hide hydrogen atoms, so counting H and spotting environments for NMR is harder', 'do not show 3D shape unless wedges/dashes are added', 'beginners find implied atoms confusing'], 'Skeletal formulae are the most efficient for large molecules, but full or 3D formulae are better when every atom or the spatial arrangement matters.'))


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def c4_formula_puzzle(rng, slot):
    mf_ = pick(rng, ['C3H8O', 'C4H8O', 'C3H6O2', 'C4H10O', 'C4H8O2', 'C2H6O', 'C5H10O'])
    iso = [o for o in ORG if o[2] == mf_]
    if len(iso) < 2:
        return None
    a, b = rng.sample(iso, 2)
    stem = (f'Two compounds, P and Q, both have the molecular formula {chem(mf_)}. P is {"an" if a[3][0] in "aeiou" else "a"} {a[3]} and Q is {"an" if b[3][0] in "aeiou" else "a"} {b[3]}. '
            f'(a) Draw a structural formula and give the IUPAC name for a possible structure of P and of Q. (b) Determine the empirical formula of P. (c) State the type of isomerism shown. (d) Suggest one physical property that would differ between P and Q and explain why.')
    a_ = atoms(mf_)
    g = 0
    for v in a_.values():
        g = math.gcd(g, v)
    emp = chem(''.join(f'{e}{a_[e] // g if a_[e] // g > 1 else ""}' for e in a_))
    return dict(stem=stem, answer=f'(a) P {a[0]} ({oc(a)}), Q {b[0]} ({oc(b)}); (b) {emp}; (c) structural isomerism ({"functional group" if a[3] != b[3] else "position/chain"}); (d) e.g. boiling point – different intermolecular forces.',
                markingKey=f'(a) correct structures and names, e.g. {a[0]} and {b[0]} (A1 A1 A1 A1). (b) {emp} (A1). (c) structural ({"functional group" if a[3] != b[3] else "chain/position"}) isomers (A1). (d) boiling point or solubility differs because of different intermolecular forces (e.g. hydrogen bonding in one) (R1).', type='multi_step', marks=7)


# ---- ch02-st3 isomers ----
STRUCT_ISO = [('C4H10', 2, 'butane and 2-methylpropane'), ('C5H12', 3, 'pentane, 2-methylbutane and 2,2-dimethylpropane'),
              ('C6H14', 5, 'hexane, 2-methylpentane, 3-methylpentane, 2,2-dimethylbutane and 2,3-dimethylbutane'),
              ('C3H7Cl', 2, '1-chloropropane and 2-chloropropane'), ('C4H9Br', 4, '1-bromobutane, 2-bromobutane, 1-bromo-2-methylpropane and 2-bromo-2-methylpropane'),
              ('C3H8O', 3, 'propan-1-ol, propan-2-ol and methoxyethane'), ('C2H4Cl2', 2, '1,1-dichloroethane and 1,2-dichloroethane'),
              ('C3H6Cl2', 4, '1,1-, 1,2-, 1,3- and 2,2-dichloropropane'), ('C3H6O2', 3, 'propanoic acid, methyl ethanoate and ethyl methanoate (acids and esters only)'),
              ('C4H10O', 4, 'butan-1-ol, butan-2-ol, 2-methylpropan-1-ol and 2-methylpropan-2-ol (alcohols only)')]
CHIRAL = [('butan-2-ol', 'CH3CH(OH)CH2CH3', True), ('propan-2-ol', 'CH3CH(OH)CH3', False), ('2-bromobutane', 'CH3CHBrCH2CH3', True),
          ('1-chlorobutane', 'CH3CH2CH2CH2Cl', False), ('2-hydroxypropanoic acid', 'CH3CH(OH)COOH', True), ('2-aminopropanoic acid', 'CH3CH(NH2)COOH', True),
          ('aminoethanoic acid', 'H2NCH2COOH', False), ('3-methylhexane', 'CH3CH2CH(CH3)CH2CH2CH3', True), ('3-methylpentane', 'CH3CH2CH(CH3)CH2CH3', False),
          ('2-methylbutan-1-ol', 'HOCH2CH(CH3)CH2CH3', True), ('pentan-3-ol', 'CH3CH2CH(OH)CH2CH3', False), ('pentan-2-ol', 'CH3CH(OH)CH2CH2CH3', True),
          ('2-bromo-2-methylpropane', '(CH3)3CBr', False), ('butanone', 'CH3COCH2CH3', False), ('1,2-dibromopropane', 'CH2BrCHBrCH3', True),
          ('2-chloropropane', 'CH3CHClCH3', False), ('2-chloropentane', 'CH3CHClCH2CH2CH3', True), ('3-chloropentane', 'CH3CH2CHClCH2CH3', False),
          ('2-bromobutanoic acid', 'CH3CH2CHBrCOOH', True), ('1-bromo-2-methylpropane', '(CH3)2CHCH2Br', False)]
CISTRANS = [('but-2-ene', 'CH3CH=CHCH3', True), ('but-1-ene', 'CH2=CHCH2CH3', False), ('pent-2-ene', 'CH3CH=CHCH2CH3', True),
            ('2-methylbut-2-ene', '(CH3)2C=CHCH3', False), ('1,2-dichloroethene', 'CHCl=CHCl', True), ('1,1-dichloroethene', 'CH2=CCl2', False),
            ('hex-3-ene', 'CH3CH2CH=CHCH2CH3', True), ('propene', 'CH2=CHCH3', False), ('2-methylpropene', 'CH2=C(CH3)2', False),
            ('1-bromopropene', 'CHBr=CHCH3', True), ('but-2-enoic acid', 'CH3CH=CHCOOH', True), ('3-methylpent-2-ene', 'CH3CH=C(CH3)CH2CH3', True),
            ('2,3-dimethylbut-2-ene', '(CH3)2C=C(CH3)2', False), ('1,2-dibromoethene', 'CHBr=CHBr', True), ('pent-1-ene', 'CH2=CHCH2CH2CH3', False)]

R.facts('ch02-st3', F(
    terms=[('structural isomers', 'compounds with the same molecular formula but different structural formulae (different connectivity of atoms)'),
           ('stereoisomers', 'compounds with the same structural formula but a different arrangement of atoms in space'),
           ('chiral carbon', 'a carbon atom bonded to four different atoms or groups (a stereocentre)'),
           ('enantiomers', 'a pair of stereoisomers that are non-superimposable mirror images of each other'),
           ('racemic mixture', 'an equimolar mixture of two enantiomers, which does not rotate plane-polarised light'),
           ('cis-trans isomers', 'stereoisomers that differ in the positions of groups relative to a double bond or ring, which restricts rotation'),
           ('optical activity', 'the ability of a substance to rotate the plane of plane-polarised light')],
    facts=[('Which compound shows cis-trans isomerism?', 'but-2-ene', ['but-1-ene', 'propene', '2-methylpropene'], 'Each C of C=C has two different groups.'),
           ('Which compound has a chiral carbon atom?', 'butan-2-ol', ['propan-2-ol', 'butan-1-ol', '2-methylpropan-2-ol'], 'C2 bonded to H, OH, CH₃ and C₂H₅.'),
           ('How do two enantiomers differ in their physical properties?', 'They rotate plane-polarised light in opposite directions.', ['They have different boiling points.', 'They have different densities.', 'They have different molar masses.'], 'Identical except for optical rotation and interactions with other chiral species.'),
           ('Why does but-2-ene have cis and trans forms?', 'Rotation about the C=C double bond is restricted.', ['It contains a chiral carbon.', 'It has a branched chain.', 'It has two functional groups.'], 'π bond prevents rotation.'),
           ('How many structural isomers have the formula C₄H₁₀?', '2', ['1', '3', '4'], 'butane, 2-methylpropane.'),
           ('What is the effect of a racemic mixture on plane-polarised light?', 'no net rotation', ['rotation to the right', 'rotation to the left', 'the light is absorbed'], 'Equal and opposite rotations cancel.')],
    why=[('Explain why but-2-ene exists as cis and trans isomers but but-1-ene does not.', 'Rotation about C=C is restricted by the π bond; in but-2-ene each double-bond carbon carries two different groups (H and CH₃), but in but-1-ene one carbon carries two identical H atoms.'),
         ('Explain why 2-bromobutane is optically active but 1-bromobutane is not.', 'In 2-bromobutane carbon 2 is bonded to four different groups (H, Br, CH₃, C₂H₅), so the molecule is chiral and exists as non-superimposable mirror images; 1-bromobutane has no such carbon.'),
         ('Explain why cis and trans isomers can have different boiling points.', 'Their shapes differ: in the cis isomer the bond dipoles may not cancel, giving a net dipole and dipole–dipole forces, while the symmetric trans isomer may be non-polar.'),
         ('Explain how a polarimeter can distinguish between enantiomers.', 'Plane-polarised light is passed through each solution; one enantiomer rotates the plane clockwise and the other anticlockwise by the same angle under the same conditions.'),
         ('Explain why enantiomers of a drug can have different effects in the body.', 'Receptors and enzymes are chiral; only one enantiomer may fit the binding site, so the two can differ in activity or toxicity (e.g. thalidomide).')],
    contrast=[('structural isomers', 'stereoisomers', 'Structural isomers differ in the bonding sequence of atoms; stereoisomers have the same bonding sequence but different spatial arrangements.'),
              ('cis-trans isomerism', 'optical isomerism', 'Cis-trans isomerism arises from restricted rotation (C=C or ring); optical isomerism arises from a chiral centre with four different groups.'),
              ('a cis isomer', 'a trans isomer', 'In a cis isomer the two similar groups are on the same side of the double bond; in a trans isomer they are on opposite sides.')],
    misc=[('Every molecule with a C=C double bond shows cis-trans isomerism.', 'Each carbon of the C=C must carry two different groups; but-1-ene and 2-methylpropene do not.'),
          ('Enantiomers have different chemical properties in all reactions.', 'Enantiomers react identically with non-chiral reagents; they differ only with other chiral species and in their effect on plane-polarised light.'),
          ('A carbon bonded to two identical CH₂ groups can be a chiral centre.', 'A chiral centre needs four DIFFERENT groups; the whole groups attached, not only the first atom, must differ.')],
    apply=[('Draw and name the structural isomers of C₄H₉Cl.', '1-chlorobutane, 2-chlorobutane, 1-chloro-2-methylpropane, 2-chloro-2-methylpropane', 4),
           ('Identify the chiral carbon in 2-hydroxypropanoic acid and draw its two enantiomers using wedge and dash bonds.', 'C2 (bonded to H, OH, CH₃, COOH); two tetrahedral mirror-image 3D structures', 3),
           ('State the number of structural isomers of C₅H₁₂ and name them.', '3: pentane, 2-methylbutane, 2,2-dimethylpropane', 2)],
    evaluate=[('Chirality is the most important type of isomerism in medicine.', ['enantiomers can have very different biological activities (thalidomide, ibuprofen)', 'drug regulators require single-enantiomer testing'], ['structural isomers have completely different properties too', 'cis-trans isomerism matters in fats and in drugs such as cisplatin'], 'Chirality is critical for drug action, but all forms of isomerism matter to medicinal chemists.'),
              ('Molecular formulae are of little use in organic chemistry because of isomerism.', ['many isomers share a formula (C₆H₁₄ has 5)', 'a formula gives no structural information'], ['molecular formula fixes Mr and composition, the starting point for structure determination', 'combined with IHD and spectroscopy it narrows possible structures'], 'Molecular formulae are an essential first step, though never sufficient on their own.')],
    extended=[('Compound Y, C₄H₈, decolourises bromine water. (a) Draw and name all the structural isomers of Y that are alkenes. (b) Identify which one shows stereoisomerism and draw its two forms. (c) Explain why this isomerism occurs. (d) Y reacts with HBr to give a product with a chiral carbon. Suggest the identity of Y and of the product.', '(a) but-1-ene, but-2-ene, 2-methylpropene. (b) but-2-ene: cis (Z) and trans (E). (c) restricted rotation about C=C and two different groups on each C. (d) but-1-ene or but-2-ene → 2-bromobutane (chiral C2).', 8, 'multi_step')],
))


@R.add('ch02-st3', 'C3', (1, 4), 'mcq')
def c3_n_isomers(rng, slot):
    f, n, names = pick(rng, STRUCT_ISO)
    wr = [str(x) for x in sorted({n - 1, n + 1, n + 2, n * 2} - {n, 0})]
    rng.shuffle(wr)
    note = ' (consider only alcohols)' if f == 'C4H10O' else ' (consider only carboxylic acids and esters)' if f == 'C3H6O2' else ''
    stem = f'How many structural isomers have the molecular formula {chem(f)}{note}?'
    return mcq(rng, stem, str(n), wr[:3], f'{n}: {names}.')


@R.add('ch02-st3', 'C3', (1, 4), 'mcq')
def c3_chiral_pick(rng, slot):
    kind = rng.choice([True, False])
    right = pick(rng, [c for c in CHIRAL if c[2] == kind])
    wr = rng.sample([c for c in CHIRAL if c[2] != kind], 3)
    pool = sorted([right] + wr)
    stem = f'Which of {_lst(c[0] for c in pool)} {"has" if kind else "does not have"} a chiral carbon atom?'
    return mcq(rng, stem, right[0], [w[0] for w in wr], f'{right[0]} ({chem(right[1])}) {"has a carbon bonded to four different groups" if kind else "has no carbon bonded to four different groups"}; ' + ('the others do not.' if kind else 'each of the others does.'))


@R.add('ch02-st3', 'C3', (1, 4), 'mcq')
def c3_cistrans_pick(rng, slot):
    kind = rng.choice([True, False])
    right = pick(rng, [c for c in CISTRANS if c[2] == kind])
    wr = rng.sample([c for c in CISTRANS if c[2] != kind], 3)
    pool = sorted([right] + wr)
    stem = f'Which of {_lst(c[0] for c in pool)} {"shows" if kind else "cannot show"} cis-trans isomerism?'
    return mcq(rng, stem, right[0], [w[0] for w in wr], f'{right[0]} ({chem(right[1])}): ' + ('each C=C carbon has two different groups.' if kind else 'one C=C carbon carries two identical groups.'))


@R.add('ch02-st3', 'C3', (1, 5), 'short')
def c3_stereo_short(rng, slot):
    if rng.random() < 0.5:
        n, f, ch = pick(rng, CHIRAL)
        stem = f'Determine whether {n}, {chem(f)}, can exist as enantiomers. Explain your answer.'
        ans = ('Yes – it contains a carbon bonded to four different groups (a chiral centre), so it has non-superimposable mirror images.' if ch else
               'No – no carbon atom is bonded to four different groups, so its mirror image is superimposable.')
    else:
        n, f, ch = pick(rng, CISTRANS)
        stem = f'Deduce whether {n}, {chem(f)}, shows cis-trans isomerism. Explain your answer.'
        ans = ('Yes – rotation about C=C is restricted and each carbon of the double bond carries two different groups.' if ch else
               'No – one carbon of the C=C carries two identical groups, so the two arrangements are the same.')
    return dict(stem=stem, answer=ans, markingKey=f'{ans.split(" – ")[0]} (1); reason: {ans.split(" – ")[1]} (1).', type='short', marks=2)


@R.add('ch02-st3', 'C3', (2, 4), 'numerical')
def c3_rotation(rng, slot):
    a = round(rng.uniform(5, 40), 1)
    frac_ = rng.choice([0.25, 0.3, 0.4, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95])
    obs = a * (2 * frac_ - 1)
    nm = pick(rng, [c[0] for c in CHIRAL if c[2]])
    stem = (f'A pure sample of one enantiomer of {nm} rotates plane-polarised light by +{a}° under certain conditions. A mixture of the two enantiomers under the same conditions rotates the light by {sgn(obs, 3)}°. '
            f'Calculate the percentage of the (+) enantiomer in the mixture.')
    if abs(obs) < 0.05:
        return None
    return num(stem, f'{frac_ * 100:.0f} %', f'observed/maximum = (x − (1 − x)) = {sgn(obs, 3)}/{a} (M1); 2x − 1 = {sf(obs / a)} → x = {frac_ * 100:.0f} % (A1).', 2)


R.mcqs('ch02-st3', 'C2', (1, 4), [
    ('Why do enantiomers have identical boiling points?', 'Their intermolecular forces are identical because they have the same structure and polarity.', ['They are the same molecule.', 'They have different molar masses.', 'They are racemic.'], 'Mirror images – same physical properties.'),
    ('What structural feature is needed for a molecule to be chiral?', 'a carbon atom bonded to four different groups', ['a C=C double bond', 'a ring of six atoms', 'an –OH group'], 'Stereocentre.'),
    ('Why are cis- and trans-but-2-ene not interconverted at room temperature?', 'Breaking the π bond to allow rotation requires a large amount of energy.', ['The σ bond cannot rotate.', 'They are structural isomers.', 'The molecules are chiral.'], 'Restricted rotation.'),
    ('Which statement about structural isomers is correct?', 'They can have different functional groups and different chemical properties.', ['They always have the same boiling point.', 'They are always mirror images.', 'They have different molecular formulae.'], 'e.g. ethanol and methoxymethane.'),
])


# ---- ch02-st4 spectroscopy ----
IR = [('O–H (alcohols)', '3200–3600', 'broad'), ('O–H (carboxylic acids)', '2500–3000', 'very broad'), ('C=O', '1700–1750', 'strong, sharp'),
      ('C–H', '2850–3090', 'medium'), ('C=C', '1620–1680', 'medium'), ('N–H', '3300–3500', 'medium'), ('C–O', '1050–1410', 'strong'),
      ('C≡C', '2100–2260', 'weak')]
IR_CLASS = {'alcohol': ['O–H (alcohols)', 'C–O'], 'carboxylic acid': ['O–H (carboxylic acids)', 'C=O'], 'aldehyde': ['C=O'], 'ketone': ['C=O'],
            'ester': ['C=O', 'C–O'], 'alkene': ['C=C'], 'amine': ['N–H'], 'alkane': [], 'halogenoalkane': [], 'amide': ['N–H', 'C=O'], 'ether': ['C–O'], 'alkyne': ['C≡C']}
IRD = {b: r for b, r, _ in IR}
# name: (number of environments, ratio, splitting HL)
NMR = {'ethanol': (3, '3:2:1', 'CH₃ triplet, CH₂ quartet, OH singlet'), 'methanol': (2, '3:1', 'two singlets'),
       'propan-1-ol': (4, '3:2:2:1', None), 'propan-2-ol': (3, '6:1:1', 'CH₃ doublet, CH multiplet (septet), OH singlet'),
       'ethanal': (2, '3:1', 'CH₃ doublet, CHO quartet'), 'propanone': (1, '6 (single peak)', 'one singlet'), 'propanal': (3, '3:2:1', None),
       'butanone': (3, '3:3:2', 'CH₃CO singlet, CH₂ quartet, CH₃ triplet'), 'ethanoic acid': (2, '3:1', 'two singlets'),
       'propanoic acid': (3, '3:2:1', 'CH₃ triplet, CH₂ quartet, COOH singlet'), 'methyl ethanoate': (2, '3:3', 'two singlets'),
       'ethyl ethanoate': (3, '3:2:3', 'CH₃CO singlet, OCH₂ quartet, CH₃ triplet'), 'ethyl methanoate': (3, '1:2:3', 'HCOO singlet, CH₂ quartet, CH₃ triplet'),
       'methyl propanoate': (3, '3:2:3', 'OCH₃ singlet, CH₂ quartet, CH₃ triplet'), 'bromoethane': (2, '3:2', 'CH₃ triplet, CH₂ quartet'),
       '1-bromopropane': (3, '3:2:2', None), '2-bromopropane': (2, '6:1', 'CH₃ doublet, CH septet'), '2-methylpropan-2-ol': (2, '9:1', 'two singlets'),
       '2-bromo-2-methylpropane': (1, '9 (single peak)', 'one singlet'), 'benzene': (1, '6 (single peak)', 'one singlet'), 'ethane': (1, '6 (single peak)', 'one singlet'),
       'propane': (2, '6:2 (3:1)', 'CH₃ triplet, CH₂ septet'), 'butane': (2, '6:4 (3:2)', None), '2-methylpropane': (2, '9:1', 'CH₃ doublet, CH multiplet'),
       'methoxymethane': (1, '6 (single peak)', 'one singlet'), 'ethylamine': (3, '3:2:2', None), 'pentan-3-one': (2, '6:4 (3:2)', 'CH₃ triplet, CH₂ quartet'),
       'pentan-2-one': (4, '3:2:2:3', None), 'ethene': (1, '4 (single peak)', 'one singlet'), 'methyl propanoate ': (3, '3:2:3', None)}
FRAG = [(15, 'CH₃⁺'), (29, 'C₂H₅⁺ or CHO⁺'), (31, 'CH₂OH⁺'), (43, 'C₃H₇⁺ or CH₃CO⁺'), (45, 'COOH⁺'), (77, 'C₆H₅⁺'), (17, 'OH⁺')]

R.facts('ch02-st4', F(
    terms=[('molecular ion', 'the ion formed when a molecule loses one electron in a mass spectrometer, M⁺; its m/z value gives the relative molecular mass'),
           ('fragmentation', 'the breaking of a molecular ion into smaller positive ions and neutral species in a mass spectrometer'),
           ('wavenumber', 'the reciprocal of wavelength (cm⁻¹), used to locate absorptions in an infrared spectrum'),
           ('chemical shift', 'the position of an NMR signal relative to the TMS reference (δ, in ppm), which depends on the chemical environment of the nucleus'),
           ('index of hydrogen deficiency', 'the number of rings plus π bonds in a molecule, deduced from its molecular formula'),
           ('tetramethylsilane (TMS)', 'the reference compound, Si(CH₃)₄, assigned δ = 0 ppm in ¹H NMR spectroscopy'),
           ('integration trace', 'the stepped line on an NMR spectrum whose heights are proportional to the number of hydrogen atoms in each environment')],
    facts=[('What does an infrared spectrum mainly identify?', 'the bonds and functional groups present', ['the relative molecular mass', 'the number of hydrogen environments', 'the carbon skeleton length'], 'Bond vibrations absorb at characteristic wavenumbers.'),
           ('Which absorption range (cm⁻¹) indicates a C=O bond?', '1700–1750', ['3200–3600', '2500–3000', '1620–1680'], 'Data booklet.'),
           ('Why is TMS used as the NMR reference?', 'It gives one strong signal from 12 equivalent hydrogens, upfield of most organic signals.', ['It absorbs infrared radiation strongly.', 'It contains many different hydrogen environments.', 'It reacts with the sample.'], 'Single peak at δ 0, inert, volatile.'),
           ('What does the number of peaks in a low-resolution ¹H NMR spectrum show?', 'the number of different hydrogen environments', ['the total number of hydrogen atoms', 'the number of carbon atoms', 'the relative molecular mass'], 'Each environment gives one signal.'),
           ('In mass spectrometry, the peak with the highest m/z (ignoring isotope peaks) is usually', 'the molecular ion', ['the base peak', 'the CH₃⁺ fragment', 'the solvent'], 'M⁺ gives Mr.'),
           ('Which bond causes a very broad absorption at 2500–3000 cm⁻¹?', 'O–H in carboxylic acids', ['C=O', 'O–H in alcohols', 'N–H'], 'Strongly hydrogen-bonded acid O–H.')],
    why=[('Explain why only some molecules absorb infrared radiation.', 'A bond vibration absorbs IR only if it changes the dipole moment of the molecule; symmetrical vibrations of non-polar bonds (e.g. in N₂, O₂) do not absorb.'),
         ('Explain why the ¹H NMR spectrum of propanone shows only one peak.', 'All six hydrogens are in identical environments (two equivalent CH₃ groups attached to C=O), so they all absorb at the same chemical shift.'),
         ('Explain how the m/z value of the molecular ion helps to identify a compound.', 'The molecular ion is the molecule minus one electron, so its m/z equals the relative molecular mass, which restricts the possible molecular formulae.'),
         ('Explain the n + 1 rule in high-resolution ¹H NMR.', 'A signal is split into n + 1 lines by the n hydrogens on adjacent carbon atoms, because their spins can align with or against the field in different combinations.'),
         ('Explain why a combination of spectroscopic techniques is usually needed to identify an unknown compound.', 'Each technique gives different information – MS gives Mr and fragments, IR the functional groups, NMR the hydrogen environments and connectivity – so together they fix one structure.')],
    contrast=[('the molecular ion peak', 'the base peak', 'The molecular ion peak (highest m/z, M⁺) gives Mr; the base peak is the most abundant (tallest) peak, often a stable fragment.'),
              ('low-resolution ¹H NMR', 'high-resolution ¹H NMR', 'Low resolution shows one peak per environment with areas in the ratio of H atoms; high resolution also shows splitting (n + 1 rule) revealing neighbouring hydrogens.'),
              ('IR absorption of an alcohol O–H', 'IR absorption of a carboxylic acid O–H', 'An alcohol O–H gives a broad band at 3200–3600 cm⁻¹; an acid O–H gives a very broad band at lower wavenumber, 2500–3000 cm⁻¹, often overlapping C–H.')],
    misc=[('The tallest peak in a mass spectrum is always the molecular ion.', 'The tallest peak is the base peak, often a stable fragment; the molecular ion is the peak at the highest m/z (excluding isotope peaks).'),
          ('The number of peaks in a ¹H NMR spectrum equals the number of hydrogen atoms.', 'Peaks correspond to different hydrogen environments; the integration ratio gives the relative number of H atoms in each.'),
          ('An IR absorption at 1700–1750 cm⁻¹ proves the compound is a ketone.', 'C=O occurs in aldehydes, ketones, acids, esters and amides; other evidence is needed to identify which.')],
    apply=[('Calculate the index of hydrogen deficiency of C₆H₆ and interpret it.', 'IHD = (2 × 6 + 2 − 6)/2 = 4: one ring + three C=C (benzene)', 2),
           ('A compound with Mr = 46 shows a broad IR absorption at 3200–3600 cm⁻¹ and three ¹H NMR signals in the ratio 3:2:1. Identify it.', 'ethanol, CH₃CH₂OH', 2),
           ('State the m/z values of two fragments expected in the mass spectrum of ethanol and identify the ions.', '31 (CH₂OH⁺), 29 (C₂H₅⁺); also 45 (M − H) or 15 (CH₃⁺)', 2)],
    evaluate=[('Spectroscopic techniques have made traditional chemical tests obsolete.', ['spectroscopy is fast, needs tiny samples and gives detailed structures', 'it is non-destructive (IR, NMR)'], ['instruments are expensive and need trained operators', 'simple tests (bromine water, Tollens’) are cheap, quick and portable', 'tests remain valuable for teaching and field work'], 'Spectroscopy dominates structure determination, but chemical tests keep a role where speed, cost and portability matter.'),
              ('¹H NMR is the single most informative technique for determining organic structures.', ['gives number of environments, ratio of H atoms and (high resolution) neighbouring H', 'chemical shift indicates the type of environment'], ['does not give Mr directly (MS does)', 'does not detect atoms without H (e.g. C=O carbon) without ¹³C NMR', 'IR identifies functional groups more quickly'], 'NMR is often the most informative, but full identification normally needs MS and IR as well.')],
    extended=[('An unknown compound contains C 54.5 %, H 9.1 %, O 36.4 % by mass. Its mass spectrum has M⁺ at m/z = 88; its IR spectrum shows a strong absorption at 1740 cm⁻¹ and no broad band above 2500 cm⁻¹; its ¹H NMR spectrum has three peaks with integration ratio 3:2:3 (singlet, quartet, triplet). (a) Determine the empirical and molecular formulae. (b) Deduce the functional group. (c) Deduce the structure.', '(a) C₂H₄O; C₄H₈O₂. (b) C=O with no O–H: ester. (c) CH₃COOCH₂CH₃, ethyl ethanoate (CH₃CO singlet, OCH₂ quartet, CH₃ triplet).', 8, 'multi_step')],
))


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3_ihd(rng, slot):
    o = pick(rng, ORG + [('cyclohexane', 'C6H12', 'C6H12', 'cycloalkane', None), ('cyclohexene', 'C6H10', 'C6H10', 'cycloalkene', None),
                         ('phenol', 'C6H5OH', 'C6H6O', 'phenol', None), ('benzoic acid', 'C6H5COOH', 'C7H6O2', 'acid', None)])
    v = ihd(o[2])
    wr = [str(x) for x in sorted({v - 1, v + 1, v + 2, 2 * v + 1} - {v}) if x >= 0]
    rng.shuffle(wr)
    stem = pick(rng, [f'What is the index of hydrogen deficiency (IHD) of a compound with molecular formula {chem(o[2])}?', f'Calculate the IHD for {chem(o[2])}.'])
    return mcq(rng, stem, str(v), wr[:3], f'IHD = (2C + 2 + N − H − X)/2 for {chem(o[2])} = {v} (rings + π bonds).')


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3_ir_assign(rng, slot):
    o = pick(rng, [x for x in ORG if IR_CLASS.get(x[3])])
    bands = IR_CLASS[o[3]]
    b = pick(rng, bands)
    others = [x for x in IRD if x not in bands and x != 'C–H']
    rng.shuffle(others)
    stem = f'Which absorption, in cm⁻¹, would be present in the infrared spectrum of {o[0]} but absent from that of {pick(rng, ["hexane", "pentane", "butane"])}?'
    right = f'{IRD[b]} ({b})'
    return mcq(rng, stem, right, [f'{IRD[x]} ({x})' for x in others[:3]], f'{o[0]} is {"an" if o[3][0] in "aeiou" else "a"} {o[3]}: {", ".join(f"{x} {IRD[x]}" for x in bands)}; the alkane shows only C–H (2850–3090).')


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3_nmr_env(rng, slot):
    nm = pick(rng, [k for k in NMR if k.strip() == k])
    n, ratio, _ = NMR[nm]
    f = ORGN[nm][1] if nm in ORGN else nm
    kind = rng.random() < 0.5
    if kind:
        wr = [str(x) for x in sorted({n - 1, n + 1, n + 2, atoms(ORGN[nm][2] if nm in ORGN else 'C2H4')['H']} - {n}) if x > 0]
        rng.shuffle(wr)
        stem = f'How many signals appear in the low-resolution ¹H NMR spectrum of {nm}, {chem(f)}?'
        return mcq(rng, stem, str(n), wr[:3], f'{nm}: {n} hydrogen environment{"s" if n > 1 else ""} in the ratio {ratio}.')
    others = list(dict.fromkeys(v[1] for k, v in NMR.items() if v[1] != ratio))
    rng.shuffle(others)
    stem = f'What is the ratio of the peak areas in the ¹H NMR spectrum of {nm}?'
    return mcq(rng, stem, ratio, others[:3], f'{chem(f)}: {n} environment(s), {ratio}.')


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3_frag(rng, slot):
    m, ion_ = pick(rng, FRAG)
    o = pick(rng, [x for x in ORG if mr(x[2]) > m + 10])
    wr = [x[1] for x in FRAG if x[0] != m]
    rng.shuffle(wr)
    stem = f'The mass spectrum of {o[0]} shows a peak at m/z = {m}. Which ion is most likely responsible?'
    return mcq(rng, stem, ion_, wr[:3], f'm/z {m} corresponds to {ion_} (data booklet fragments).')


@R.add('ch02-st4', 'C3', (2, 5), 'short')
def c3_identify(rng, slot):
    nm = pick(rng, [k for k in NMR if k in ORGN and IR_CLASS.get(ORGN[k][3]) is not None])
    o = ORGN[nm]
    n, ratio, split = NMR[nm]
    M = mr(o[2])
    bands = IR_CLASS[o[3]]
    irtxt = ', '.join(f'{IRD[b]} cm⁻¹' for b in bands) if bands else 'only 2850–3090 cm⁻¹'
    stem = (f'An unknown compound has the molecular formula {chem(o[2])} (molecular ion at m/z = {round(M)}). Its IR spectrum shows absorptions at {irtxt}. '
            f'Its ¹H NMR spectrum has {n} signal{"s" if n > 1 else ""} with areas in the ratio {ratio}. Deduce the structure and name of the compound.')
    if slot.d >= 4 and split:
        stem += f' The high-resolution spectrum shows: {split}.'
    dup = [k for k in NMR if k in ORGN and ORGN[k][2] == o[2] and NMR[k][1] == ratio and IR_CLASS.get(ORGN[k][3]) == bands and k != nm]
    if dup:
        return None
    return dict(stem=stem, answer=f'{nm}, {oc(o)}', markingKey=f'IR: {", ".join(bands) or "no functional-group bands"} → {o[3]} (1); {n} environments in ratio {ratio} (1); structure {oc(o)} – {nm} (1).', type='short', marks=3)


@R.add('ch02-st4', 'C3', (2, 4), 'mcq')
def c3_splitting(rng, slot):
    nbr = rng.randint(0, 6)
    names = ['singlet', 'doublet', 'triplet', 'quartet', 'quintet', 'sextet', 'septet']
    ctx = pick(rng, ['in a high-resolution ¹H NMR spectrum', 'in the high-resolution spectrum of an unknown compound'])
    stem = f'A group of hydrogen atoms {ctx} has {nbr} hydrogen atom{"s" if nbr != 1 else ""} on the adjacent carbon atoms. Into how many lines is its signal split?'
    right = f'{nbr + 1} ({names[nbr]})'
    wr = [f'{x + 1} ({names[x]})' for x in {max(0, nbr - 1), min(6, nbr + 1), nbr if nbr < 6 else 5} if x != nbr]
    wr += [f'{nbr} ({names[nbr - 1]})' if nbr > 0 else '2 (doublet)', f'{min(7, nbr + 2)} ({names[min(6, nbr + 1)]})']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    return mcq(rng, stem, right, wr[:3], f'n + 1 rule: {nbr} + 1 = {nbr + 1} lines.')


R.mcqs('ch02-st4', 'C2', (1, 4), [
    ('Why does CO₂ absorb infrared radiation although it is a non-polar molecule?', 'Its asymmetric stretching and bending vibrations change the dipole moment.', ['Its C=O bonds are non-polar.', 'Its symmetric stretch changes the dipole.', 'It has a permanent dipole.'], 'IR activity needs a change in dipole.'),
    ('Why does a carboxylic acid give an absorption at a lower wavenumber than an alcohol O–H?', 'Strong hydrogen bonding between acid molecules weakens the O–H bond.', ['The acid O–H bond is stronger.', 'Acids contain no O–H bond.', 'The C=O bond absorbs there.'], 'Very broad 2500–3000 band.'),
    ('Why does the molecular ion of chloromethane give two peaks, at m/z 50 and 52?', 'Chlorine has two isotopes, ³⁵Cl and ³⁷Cl.', ['Chloromethane fragments into two ions.', 'Two electrons are removed.', 'Carbon has two isotopes in equal amounts.'], '3:1 isotope ratio.'),
    ('Why do the hydrogens of a CH₃ group next to a CH₂ group appear as a triplet?', 'The two neighbouring hydrogens split the signal into n + 1 = 3 lines.', ['There are three hydrogens in CH₃.', 'The CH₃ has three neighbours.', 'The CH₃ is next to oxygen.'], 'n + 1 rule.'),
])


@p1b(R, 'ch02-st4')
def p1b_spectra(rng, slot):
    nm = pick(rng, ['ethanol', 'propan-2-ol', 'ethyl ethanoate', 'propanoic acid', 'butanone', 'propanone', 'ethanal', 'methyl propanoate', '2-methylpropan-2-ol', 'bromoethane'])
    o = ORGN[nm]
    a = atoms(o[2])
    M = mr(o[2])
    pct = {e: AR[e] * k / M * 100 for e, k in a.items()}
    n, ratio, split = NMR[nm]
    bands = IR_CLASS[o[3]]
    comp = ', '.join(f'{e} {pct[e]:.1f} %' for e in a)
    irtxt = ', '.join(f'{IRD[b]} cm⁻¹ ({"broad" if "O–H" in b else "strong"})' for b in bands) if bands else 'only absorptions near 2900 cm⁻¹'
    intro = (f'An unknown compound X has the percentage composition by mass: {comp}. The following spectroscopic data were obtained.\n\n'
             f'Mass spectrum: molecular ion peak at m/z = {round(M)}.\nInfrared spectrum: {irtxt}.\n¹H NMR: {n} signal{"s" if n > 1 else ""}, integration ratio {ratio}.')
    g = 0
    for v in a.values():
        g = math.gcd(g, v)
    emp = chem(''.join(f'{e}{a[e] // g if a[e] // g > 1 else ""}' for e in a))
    return dict(intro=intro, parts=[
        ('Determine the empirical formula of X.', emp, f'Divide each % by Ar, then by the smallest (M1); {emp} (A1).', 2),
        ('Use the mass spectrum to deduce the molecular formula of X.', chem(o[2]), f'Mr = {round(M)} → {chem(o[2])} (A1).', 1),
        ('Calculate the index of hydrogen deficiency of X and state what it indicates.', f'{ihd(o[2])}', f'IHD = {ihd(o[2])} (A1); {"one π bond or ring" if ihd(o[2]) == 1 else "no rings or π bonds" if ihd(o[2]) == 0 else "rings/π bonds"} (A1).', 2),
        ('Identify the bond(s) responsible for the infrared absorptions.', ', '.join(bands) or 'C–H only', f'{", ".join(bands) or "C–H"} (1).', 1),
        ('Deduce the structure of X, explaining how the ¹H NMR data support it.', f'{nm}, {oc(o)}', f'{n} environments in ratio {ratio} match {oc(o)} (R1); structure (A1).', 2)],
        extras=[('Suggest the identity of a fragment ion in the mass spectrum of X at m/z = 15.', 'CH₃⁺', 'CH₃⁺ (1).', 1)])


# =============================================================================================
# ch03 R2.2 How fast? The rate of chemical change
# =============================================================================================
RATE_RX = [  # equation, reactant A, B (or None), order A, order B, context
    ('2NO(g) + O2(g) → 2NO2(g)', 'NO', 'O2', 2, 1, 'the oxidation of nitrogen monoxide'),
    ('2NO(g) + 2H2(g) → N2(g) + 2H2O(g)', 'NO', 'H2', 2, 1, 'the reduction of nitrogen monoxide by hydrogen'),
    ('(CH3)3CBr + OH- → (CH3)3COH + Br-', '(CH3)3CBr', 'OH^-', 1, 0, 'the hydrolysis of 2-bromo-2-methylpropane'),
    ('CH3CH2Br + OH- → CH3CH2OH + Br-', 'CH3CH2Br', 'OH^-', 1, 1, 'the hydrolysis of bromoethane'),
    ('CH3COCH3 + I2 → CH3COCH2I + HI (acid catalysed)', 'CH3COCH3', 'I2', 1, 0, 'the iodination of propanone'),
    ('S2O8^2- + 2I- → 2SO4^2- + I2', 'S2O8^2-', 'I^-', 1, 1, 'the oxidation of iodide ions by peroxodisulfate'),
    ('H2O2 + 2I- + 2H+ → I2 + 2H2O', 'H2O2', 'I^-', 1, 1, 'the oxidation of iodide ions by hydrogen peroxide'),
    ('NO2(g) + CO(g) → NO(g) + CO2(g)', 'NO2', 'CO', 2, 0, 'the reaction of nitrogen dioxide with carbon monoxide below 500 K'),
    ('H2(g) + I2(g) → 2HI(g)', 'H2', 'I2', 1, 1, 'the formation of hydrogen iodide'),
    ('BrO3- + 5Br- + 6H+ → 3Br2 + 3H2O (excess H+)', 'BrO3^-', 'Br^-', 1, 1, 'the reaction of bromate(V) and bromide ions in excess acid'),
]
ONE_RX = [('2N2O5(g) → 4NO2(g) + O2(g)', 'N2O5', 1, 'the decomposition of dinitrogen pentoxide'), ('2HI(g) → H2(g) + I2(g)', 'HI', 2, 'the decomposition of hydrogen iodide'),
          ('2H2O2(aq) → 2H2O(l) + O2(g)', 'H2O2', 1, 'the decomposition of hydrogen peroxide'), ('C12H22O11 + H2O → 2C6H12O6 (in excess water)', 'C12H22O11', 1, 'the acid hydrolysis of sucrose'),
          ('2NO2(g) → 2NO(g) + O2(g)', 'NO2', 2, 'the thermal decomposition of nitrogen dioxide')]


def kunit(order):
    return {0: 'mol dm⁻³ s⁻¹', 1: 's⁻¹', 2: 'dm³ mol⁻¹ s⁻¹', 3: 'dm⁶ mol⁻² s⁻¹'}[order]


def rexp(a, b, m, n):
    t = []
    for s, o in ((a, m), (b, n)):
        if s is None or o == 0:
            continue
        t.append(f'[{chem(s)}]' + (sup(o) if o > 1 else ''))
    return 'rate = k' + ''.join(t)


R.facts('ch03-st1', F(
    terms=[('rate of reaction', 'the change in concentration (or amount) of a reactant or product per unit time'),
           ('initial rate', 'the rate of reaction at time zero, found from the gradient of the tangent to the concentration–time curve at t = 0'),
           ('mean rate', 'the overall change in concentration (or amount) divided by the total time taken'),
           ('tangent', 'a straight line touching a curve at one point; its gradient gives the instantaneous rate at that time'),
           ('colorimetry', 'a technique that measures the absorbance of light by a coloured solution, which is proportional to its concentration'),
           ('clock reaction', 'a reaction in which a sudden colour change after a measured time indicates that a fixed amount of product has formed')],
    facts=[('What are the units of rate of reaction for a change in concentration?', 'mol dm⁻³ s⁻¹', ['mol dm⁻³', 'dm³ mol⁻¹ s⁻¹', 's⁻¹'], 'Concentration per unit time.'),
           ('Why does the gradient of a concentration–time graph for a reactant decrease with time?', 'The concentration of reactant decreases, so collisions become less frequent.', ['The activation energy increases.', 'The temperature falls.', 'The catalyst is used up.'], 'Rate depends on concentration.'),
           ('Which method is suitable for following CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)?', 'measuring the loss in mass over time', ['colorimetry', 'measuring the change in pH of the solid', 'measuring the volume of liquid formed'], 'CO₂ escapes.'),
           ('Which reaction could be followed using colorimetry?', 'the reaction of propanone with iodine', ['the reaction of magnesium with hydrochloric acid', 'the neutralisation of NaOH by HCl', 'the decomposition of calcium carbonate'], 'Iodine is coloured.'),
           ('How is the initial rate found from a graph of product concentration against time?', 'from the gradient of the tangent at t = 0', ['from the final concentration', 'from the area under the curve', 'from the time taken to finish'], 'Instantaneous rate at t = 0.'),
           ('How does the rate of a reaction change as it proceeds (at constant temperature)?', 'it decreases', ['it increases', 'it stays constant', 'it first decreases then increases'], 'Reactants used up.')],
    why=[('Explain why the rate of a reaction is greatest at the start.', 'The concentration of reactants is highest at the start, so the frequency of successful collisions is greatest; as reactants are used up the rate falls.'),
         ('Explain why a gas syringe is preferable to collecting gas over water for carbon dioxide.', 'Carbon dioxide is fairly soluble in water, so some would dissolve and the measured volume would be too low; a gas syringe avoids this.'),
         ('Explain why the cotton wool plug is used when following a reaction by mass loss.', 'It allows the gas to escape but prevents acid spray/droplets from leaving the flask, which would add to the mass loss.'),
         ('Explain why a clock reaction measures an approximate initial rate.', 'The time is measured for a small, fixed amount of product to form while reactant concentrations have hardly changed, so 1/t is proportional to the initial rate.'),
         ('Explain why measuring the conductivity of a solution can be used to follow some reactions.', 'If the number or type of ions changes during the reaction, the electrical conductivity changes in proportion to the extent of reaction.')],
    contrast=[('initial rate', 'mean rate', 'Initial rate is the instantaneous rate at t = 0 (gradient of the tangent); mean rate is the total change divided by the total time.'),
              ('a continuous method', 'a discontinuous (sampling) method', 'In a continuous method a property (mass, volume, absorbance) is monitored throughout one run; in a sampling method portions are removed, quenched and analysed at intervals (e.g. by titration).')],
    misc=[('A reaction that gives more product has a faster rate.', 'The amount of product depends on the amount of limiting reactant; rate is how fast the change happens.'),
          ('The rate of reaction is constant until the reaction stops.', 'For most reactions the rate falls continuously as the reactant concentrations decrease.'),
          ('The units of rate are always mol s⁻¹.', 'Rate in terms of concentration has units mol dm⁻³ s⁻¹; other units (cm³ s⁻¹, g s⁻¹) apply if volume or mass is measured.')],
    apply=[('In a reaction, 48.0 cm³ of gas was collected in the first 30 s and 72.0 cm³ in the first 60 s. Calculate the mean rate in each 30 s interval and comment.', '1.60 cm³ s⁻¹ then 0.800 cm³ s⁻¹: the rate halves as reactants are used up', 3),
           ('Suggest a suitable method to follow the reaction Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g).', 'Collect H₂ in a gas syringe and record volume at regular time intervals (or mass loss is too small for H₂).', 2)],
    evaluate=[('Measuring the volume of gas produced is the best way to follow the rate of any reaction.', ['continuous, simple and gives many data points', 'precise gas syringes are available'], ['only works when a gas is produced', 'soluble gases (CO₂, NH₃) give low readings', 'colorimetry or conductivity may be more precise and do not disturb the system'], 'It is convenient for gas-producing reactions, but the best method depends on which property changes measurably.'),
              ('Initial rates are more useful than mean rates.', ['initial rate relates directly to known starting concentrations, so it is used to find orders', 'not affected by product build-up or reverse reaction'], ['drawing a tangent introduces uncertainty', 'mean rates are easier to measure and adequate for comparisons'], 'Initial rates are essential for kinetic analysis, though mean rates are fine for simple comparisons.')],
    extended=[('A student follows the reaction of marble chips with excess hydrochloric acid by measuring mass loss. (a) Sketch the expected mass–time graph and explain its shape. (b) Explain how the initial rate can be found. (c) State and explain two changes that would increase the rate. (d) Suggest why the final mass loss is the same when powdered marble is used.', '(a) mass falls steeply at first then levels off: rate decreases as acid concentration and surface area fall; stops when CaCO₃ used up. (b) tangent at t = 0, gradient. (c) higher acid concentration/temperature/smaller chips – more frequent and/or more energetic collisions. (d) same amount of CaCO₃ → same mass of CO₂.', 7, 'multi_step')],
))


@R.add('ch03-st1', 'C3', (1, 4), 'numerical')
def c3_mean_rate(rng, slot):
    kind = pick(rng, ['gas', 'mass', 'conc'])
    t = rng.choice([20, 30, 40, 60, 90, 120])
    if kind == 'gas':
        v = round(rng.uniform(15, 90), 1)
        stem = pick(rng, [f'{v} cm³ of hydrogen was collected in a gas syringe in the first {t} s of the reaction between magnesium and hydrochloric acid. Calculate the mean rate of gas production.',
                          f'In the decomposition of hydrogen peroxide, {v} cm³ of oxygen formed in {t} s. Determine the mean rate in cm³ s⁻¹.'])
        r = v / t
        return num(stem, q(r, 'cm³ s⁻¹'), f'rate = {v}/{t} (M1) = {q(r, "cm³ s⁻¹")} (A1).', 2)
    if kind == 'mass':
        m = round(rng.uniform(0.20, 2.50), 2)
        stem = f'Marble chips react with hydrochloric acid in an open flask. The mass decreased by {m:.2f} g in {t} s. Calculate the mean rate of production of carbon dioxide in mol s⁻¹.'
        r = m / 44.01 / t
        return num(stem, q(r, 'mol s⁻¹'), f'n(CO₂) = {m:.2f}/44.01 = {sf(m / 44.01)} mol (M1); rate = /{t} = {q(r, "mol s⁻¹")} (A1).', 2)
    c0 = rng.choice([0.100, 0.200, 0.250, 0.500, 1.00])
    c1 = c0 * rng.uniform(0.3, 0.8)
    stem = f'The concentration of a reactant fell from {sf(c0)} mol dm⁻³ to {sf(c1)} mol dm⁻³ in {t} s. Calculate the mean rate of reaction.'
    r = (c0 - rsf(c1)) / t
    return num(stem, q(r, 'mol dm⁻³ s⁻¹'), f'rate = ({sf(c0)} − {sf(c1)})/{t} (M1) = {q(r, "mol dm⁻³ s⁻¹")} (A1).', 2)


@R.add('ch03-st1', 'C3', (2, 4), 'mcq')
def c3_tangent(rng, slot):
    y1 = round(rng.uniform(0.05, 0.40), 2)
    t2 = rng.choice([20, 40, 50, 80, 100])
    y2 = round(y1 + rng.uniform(0.10, 0.60), 2)
    g = (y2 - y1) / t2
    stem = f'A tangent drawn to a concentration–time curve for a product at t = 0 passes through (0 s, {y1:.2f} mol dm⁻³) and ({t2} s, {y2:.2f} mol dm⁻³). What is the initial rate of reaction?'
    return nmcq(rng, stem, g, [y2 / t2, (y2 - y1) * t2, t2 / (y2 - y1)], 'mol dm⁻³ s⁻¹', f'gradient = ({y2:.2f} − {y1:.2f})/{t2} = {sf(g)} mol dm⁻³ s⁻¹.', extra=True)


@R.add('ch03-st1', 'C3', (1, 4), 'mcq')
def c3_method(rng, slot):
    rxs = [('Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)', 'volume of hydrogen collected in a gas syringe'),
           ('CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)', 'loss in mass of the reaction flask'),
           ('CH₃COCH₃(aq) + I₂(aq) → CH₃COCH₂I(aq) + HI(aq)', 'absorbance of the solution in a colorimeter'),
           ('Na₂S₂O₃(aq) + 2HCl(aq) → 2NaCl(aq) + S(s) + SO₂(g) + H₂O(l)', 'time for a cross under the flask to disappear'),
           ('(CH₃)₃CBr + H₂O → (CH₃)₃COH + H⁺ + Br⁻', 'electrical conductivity of the solution'),
           ('2H₂O₂(aq) → 2H₂O(l) + O₂(g)', 'volume of oxygen collected in a gas syringe'),
           ('2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O', 'absorbance (fading purple colour) in a colorimeter')]
    eq, right = pick(rng, rxs)
    wr = list(dict.fromkeys(r for e, r in rxs if r != right and not (('gas syringe' in r) and ('gas syringe' in right))))
    rng.shuffle(wr)
    stem = f'Which measurement is most suitable for following the rate of {eq}?'
    return mcq(rng, stem, right, wr[:3], f'The property that changes measurably here: {right}.')


R.mcqs('ch03-st1', 'C2', (1, 4), [
    ('Why does the volume of gas collected per minute decrease as the reaction proceeds?', 'The concentration of the reactants decreases.', ['The activation energy rises.', 'The products act as catalysts.', 'The gas syringe becomes full.'], 'Lower concentration → fewer collisions.'),
    ('In a clock reaction, why is the rate taken as proportional to 1/time?', 'The same fixed amount of product forms in each run before the colour change.', ['The reaction always takes one second.', 'Time is inversely proportional to temperature.', 'The colour change is reversible.'], 'rate ∝ (fixed amount)/t.'),
    ('Which change would NOT alter the gradient of a mass-loss graph for marble with excess acid?', 'using a larger volume of acid at the same concentration', ['using powdered marble', 'heating the acid', 'using more concentrated acid'], 'Concentration unchanged.'),
    ('Why is a sample quenched before titration in a sampling method?', 'To stop the reaction so the concentration at that time can be measured.', ['To speed up the reaction.', 'To remove the catalyst.', 'To increase the concentration.'], 'Freeze the composition.'),
])


@p1b(R, 'ch03-st1')
def p1b_gas_rate(rng, slot):
    vmax = round(rng.uniform(60, 95), 0)
    k = rng.uniform(0.02, 0.05)
    ts = [0, 30, 60, 90, 120, 150, 180]
    vs = [round(vmax * (1 - math.exp(-k * t)), 1) for t in ts]
    tab = '\n'.join(f'{t} | {v}' for t, v in zip(ts, vs))
    m1 = (vs[1] - vs[0]) / 30
    m2 = (vs[4] - vs[3]) / 30
    intro = (f'Magnesium ribbon was added to excess hydrochloric acid and the hydrogen produced was collected in a gas syringe (uncertainty ±0.5 cm³). Room conditions: 298 K, 100 kPa.\n\ntime / s | volume of H₂ / cm³\n{tab}')
    n = vs[-1] / 1000 / (RGAS * 298 / 100000) / 1000 * 1000
    nH2 = 100000 * vs[-1] * 1e-6 / (RGAS * 298)
    return dict(intro=intro, parts=[
        ('Calculate the mean rate of hydrogen production in the first 30 s and between 90 s and 120 s.', f'{sf(m1)} and {sf(m2)} cm³ s⁻¹', f'{vs[1]}/30 = {sf(m1)} cm³ s⁻¹ (A1); ({vs[4]} − {vs[3]})/30 = {sf(m2)} cm³ s⁻¹ (A1).', 2),
        ('Explain the difference between the two rates.', 'The acid concentration and the magnesium surface area decrease as the reaction proceeds, so collisions become less frequent.', 'Reactants used up / lower concentration (1); fewer collisions per unit time (1).', 2),
        ('Calculate the amount of hydrogen collected after 180 s, using pV = nRT.', q(nH2, 'mol'), f'n = pV/RT = 1.00 × 10⁵ × {vs[-1]} × 10⁻⁶ / (8.31 × 298) (M1) = {q(nH2, "mol")} (A1).', 2),
        ('Calculate the percentage uncertainty in the volume reading at 30 s.', f'{0.5 / vs[1] * 100:.1f} %', f'0.5/{vs[1]} × 100 = {0.5 / vs[1] * 100:.1f} % (A1).', 1),
        ('State how the initial rate could be determined more accurately from these data.', 'Plot volume against time and draw a tangent to the curve at t = 0; calculate its gradient.', 'Tangent at t = 0 on a plotted curve (1).', 1)],
        extras=[('Suggest one source of systematic error in this experiment.', 'Gas escapes before the bung is fitted, or the syringe plunger sticks, giving readings that are too low.', 'Gas loss at start / friction in syringe (1).', 1)])


# ---- ch03-st2 collision theory, Ea, Maxwell–Boltzmann, catalysts ----
R.facts('ch03-st2', F(
    terms=[('activation energy', 'the minimum energy that colliding particles must have for a reaction to occur'),
           ('catalyst', 'a substance that increases the rate of a reaction by providing an alternative pathway of lower activation energy, and is unchanged chemically at the end'),
           ('Maxwell–Boltzmann distribution', 'the distribution of kinetic energies of particles in a gas (or solution) at a given temperature'),
           ('collision theory', 'the theory that particles must collide with sufficient energy (≥ Ea) and with the correct orientation for a reaction to occur'),
           ('heterogeneous catalyst', 'a catalyst in a different phase from the reactants, e.g. solid iron in the Haber process'),
           ('homogeneous catalyst', 'a catalyst in the same phase as the reactants, e.g. H⁺(aq) in esterification'),
           ('transition state', 'the highest-energy arrangement of atoms along the reaction pathway, at the peak of the energy profile')],
    facts=[('What is the main reason why the rate increases with temperature?', 'A larger proportion of collisions have energy ≥ Ea.', ['Collisions occur less often.', 'The activation energy decreases.', 'ΔH becomes more negative.'], 'Energy factor outweighs frequency factor.'),
           ('What happens to the Maxwell–Boltzmann curve when temperature increases?', 'The peak moves to higher energy and becomes lower; the area stays the same.', ['The peak moves to lower energy.', 'The area under the curve increases.', 'The curve does not change.'], 'Same number of particles.'),
           ('How does a catalyst increase the rate of a reaction?', 'It provides a pathway with a lower activation energy.', ['It increases the kinetic energy of particles.', 'It shifts the equilibrium to the right.', 'It makes ΔH more negative.'], 'More particles have E ≥ Ea(cat).'),
           ('Why does increasing the surface area of a solid reactant increase the rate?', 'More particles are exposed, so collisions are more frequent.', ['The activation energy decreases.', 'The particles move faster.', 'The enthalpy change increases.'], 'Collision frequency.'),
           ('What does the area under a Maxwell–Boltzmann curve represent?', 'the total number of particles', ['the activation energy', 'the average kinetic energy', 'the rate constant'], 'Area = total particles.'),
           ('Which statement about a catalysed reaction is correct?', 'ΔH is unchanged.', ['Ea is increased.', 'More product forms at equilibrium.', 'The catalyst is used up.'], 'Only the pathway changes.')],
    why=[('Explain, using collision theory, why increasing the concentration of a solution increases the rate of reaction.', 'There are more particles per unit volume, so collisions occur more frequently and the number of successful collisions (E ≥ Ea, correct orientation) per second increases.'),
         ('Explain, with reference to the Maxwell–Boltzmann distribution, why a small temperature rise causes a large increase in rate.', 'At higher temperature the distribution shifts to higher energies; the area beyond Ea increases greatly, so a much larger fraction of collisions are successful, while collision frequency rises only slightly.'),
         ('Explain why not all collisions between reactant particles lead to a reaction.', 'Particles must collide with energy at least equal to the activation energy and with the correct orientation (geometry) so that bonds can break and form.'),
         ('Explain how a catalyst affects the Maxwell–Boltzmann distribution and the rate.', 'The distribution is unchanged, but the lower activation energy line moves left, so a larger area (more particles) has E ≥ Ea(cat) and the rate increases.'),
         ('Explain why powdered zinc reacts faster with acid than a lump of zinc of the same mass.', 'The powder has a much larger surface area, so more zinc atoms are exposed to collisions with H⁺ ions per unit time.')],
    contrast=[('a homogeneous catalyst', 'a heterogeneous catalyst', 'A homogeneous catalyst is in the same phase as the reactants (often forming an intermediate); a heterogeneous catalyst is in a different phase and works by adsorption on its surface.'),
              ('the effect of temperature on rate', 'the effect of a catalyst on rate', 'Raising temperature increases particle energies so more exceed the same Ea; a catalyst leaves the energies unchanged but lowers Ea.'),
              ('a transition state', 'an intermediate', 'A transition state is an unstable arrangement at an energy maximum that cannot be isolated; an intermediate is a species formed in one step and used in a later step, at an energy minimum between peaks.')],
    misc=[('Increasing the temperature increases the rate mainly because particles collide more often.', 'Collision frequency rises only slightly; the main effect is that a much greater fraction of collisions have E ≥ Ea.'),
          ('A catalyst gives the particles more energy so they can react.', 'A catalyst does not change particle energies; it provides an alternative pathway with lower Ea.'),
          ('Increasing temperature lowers the activation energy.', 'Ea is (approximately) constant; more particles have energy greater than or equal to it at higher temperature.')],
    apply=[('A reaction has Ea = 75 kJ mol⁻¹ and ΔH = −40 kJ mol⁻¹. Calculate the activation energy of the reverse reaction.', 'Ea(reverse) = 75 − (−40) = 115 kJ mol⁻¹', 2),
           ('Sketch a Maxwell–Boltzmann distribution at two temperatures, T₁ < T₂, and use it to explain the effect of temperature on rate.', 'T₂ curve flatter with peak at higher energy, same area; area beyond Ea larger at T₂ → more successful collisions', 3)],
    evaluate=[('Catalysts are the single most important factor in making industrial processes sustainable.', ['allow lower temperatures and pressures, saving energy', 'improve selectivity, reducing waste', 'enable greener routes (enzymes, zeolites)'], ['many catalysts use scarce or toxic metals (Pt, Pd, Rh)', 'feedstock choice, energy source and recycling are equally important', 'catalysts can be poisoned and need replacing'], 'Catalysts are vital for sustainability, but they work together with renewable feedstocks, energy efficiency and recycling.'),
              ('Collision theory fully explains how temperature affects reaction rates.', ['explains energy distribution and fraction of successful collisions', 'combined with the Maxwell–Boltzmann distribution it is quantitatively useful'], ['orientation (steric) factors are hard to predict', 'it treats particles as hard spheres and ignores the transition state', 'enzyme-catalysed rates fall at high temperature (denaturation)'], 'It explains most temperature effects well, but transition-state theory and special cases give a fuller picture.')],
    extended=[('Hydrogen peroxide decomposes slowly at room temperature but rapidly when manganese(IV) oxide is added. (a) Write an equation for the decomposition. (b) Draw an energy profile for the catalysed and uncatalysed reactions (ΔH = −98 kJ mol⁻¹). (c) Explain the effect of the catalyst using a Maxwell–Boltzmann distribution. (d) Describe how you would show that MnO₂ is not used up.', '(a) 2H₂O₂ → 2H₂O + O₂. (b) exothermic profile, catalysed peak lower, same ΔH. (c) lower Ea line; larger area beyond it; more successful collisions. (d) filter, wash, dry and weigh the MnO₂ before and after; same mass; reuse to show it still catalyses.', 8, 'multi_step')],
))


@R.add('ch03-st2', 'C3', (1, 4), 'mcq')
def c3_ea_reverse(rng, slot):
    ea = rng.randint(40, 180)
    dh = rng.choice([-1, 1]) * rng.randint(20, min(150, ea - 5))
    rev = ea - dh
    stem = pick(rng, [f'For a reaction, Ea(forward) = {ea} kJ mol⁻¹ and ΔH = {sgn(dh, 4)} kJ mol⁻¹. What is the activation energy of the reverse reaction?',
                      f'An energy profile shows a forward activation energy of {ea} kJ mol⁻¹ and an enthalpy change of {sgn(dh, 4)} kJ mol⁻¹. Determine Ea for the reverse reaction.'])
    wr = [f'{x} kJ mol⁻¹' for x in dict.fromkeys([ea + dh, abs(dh), ea]) if x != rev and x > 0]
    while len(wr) < 3:
        wr.append(f'{rev + 10 * len(wr)} kJ mol⁻¹')
    return mcq(rng, stem, f'{rev} kJ mol⁻¹', wr[:3], f'Ea(reverse) = Ea(forward) − ΔH = {ea} − ({sgn(dh, 4)}) = {rev} kJ mol⁻¹.')


@R.add('ch03-st2', 'C3', (2, 5), 'numerical')
def c3_fraction_factor(rng, slot):
    ea = rng.choice([40, 50, 60, 75, 80, 90, 100, 120])
    t1 = rng.choice([288, 293, 298, 303, 310])
    t2 = t1 + rng.choice([10, 15, 20, 25, 30])
    f1 = math.exp(-ea * 1000 / (RGAS * t1))
    f2 = math.exp(-ea * 1000 / (RGAS * t2))
    stem = pick(rng, [f'The fraction of collisions with energy ≥ Ea is approximately e^(−Ea/RT). For Ea = {ea} kJ mol⁻¹, calculate by what factor this fraction increases when the temperature rises from {t1} K to {t2} K.',
                      f'Using f = e^(−Ea/RT), determine the ratio f({t2} K)/f({t1} K) for a reaction with activation energy {ea} kJ mol⁻¹, and comment on the effect of temperature on rate.'])
    return num(stem, sf(f2 / f1), f'ratio = exp[(Ea/R)(1/{t1} − 1/{t2})] = exp[{ea * 1000}/8.31 × ({sf(1 / t1 - 1 / t2)})] (M1) = {sf(f2 / f1)} (A1); a small rise in T greatly increases the fraction of successful collisions (R1).', 3)


@R.add('ch03-st2', 'C3', (1, 4), 'mcq')
def c3_factor_effect(rng, slot):
    changes = [('the temperature is increased', 'more frequent collisions and a greater proportion with E ≥ Ea'),
               ('a catalyst is added', 'an alternative pathway with lower Ea, so a greater proportion of collisions are successful'),
               ('the concentration of the acid is increased', 'more particles per unit volume, so more frequent collisions'),
               ('the solid is powdered', 'larger surface area, so more frequent collisions'),
               ('the pressure of the gaseous reactants is increased', 'more particles per unit volume, so more frequent collisions')]
    sys_ = pick(rng, ['zinc reacts with sulfuric acid', 'calcium carbonate reacts with hydrochloric acid', 'hydrogen peroxide decomposes', 'ammonia is formed from nitrogen and hydrogen', 'ethene reacts with hydrogen over nickel'])
    ch, right = pick(rng, changes)
    if 'powdered' in ch and sys_ in ('hydrogen peroxide decomposes', 'ammonia is formed from nitrogen and hydrogen'):
        return None
    wr = [w for c_, w in changes if w != right] + ['the activation energy of the uncatalysed reaction decreases', 'the enthalpy change becomes more negative']
    rng.shuffle(wr)
    stem = f'When {sys_}, the rate increases if {ch}. What is the best explanation?'
    return mcq(rng, stem, right, [w for w in wr if w != right][:3], f'{ch} → {right}.')


R.mcqs('ch03-st2', 'C2', (1, 4), [
    ('Why does a catalyst not change the enthalpy change of a reaction?', 'The energies of reactants and products are unchanged; only the pathway differs.', ['It increases the energy of the products.', 'It is used up in the reaction.', 'It lowers the energy of the reactants.'], 'ΔH is a state function.'),
    ('Why does the peak of the Maxwell–Boltzmann curve get lower at higher temperature?', 'The particle energies spread over a wider range while the total number of particles is fixed.', ['Particles are lost on heating.', 'The activation energy rises.', 'Fewer particles have the average energy because they react.'], 'Area constant.'),
    ('Why is the orientation of a collision important in some reactions?', 'Only collisions in which the reacting groups meet allow the correct bonds to break and form.', ['Orientation changes the activation energy of the reaction.', 'Particles must collide head-on to transfer heat.', 'Orientation only matters for single atoms.'], 'Steric factor.'),
    ('How does an enzyme act as a catalyst?', 'Its active site binds the substrate, providing a pathway of lower activation energy.', ['It raises the temperature of the cell.', 'It shifts equilibria to the right.', 'It changes ΔH of the reaction.'], 'Biological catalyst.'),
])


# ---- ch03-st3 rate equations (HL) ----
R.facts('ch03-st3', F(
    terms=[('rate equation', 'an experimentally determined expression rate = k[A]^m[B]^n relating the rate to the concentrations of reactants'),
           ('order of reaction', 'the power to which the concentration of a reactant is raised in the rate equation'),
           ('overall order', 'the sum of the individual orders of all reactants in the rate equation'),
           ('rate constant', 'the constant of proportionality k in the rate equation; it depends on temperature but not on concentration'),
           ('half-life', 'the time taken for the concentration of a reactant to fall to half its initial value'),
           ('zero order', 'describes a reactant whose concentration has no effect on the rate')],
    facts=[('For a first-order reaction, what is the effect of doubling the concentration of the reactant?', 'the rate doubles', ['the rate is unchanged', 'the rate quadruples', 'the rate halves'], 'rate ∝ [A].'),
           ('What are the units of k for a second-order reaction?', 'dm³ mol⁻¹ s⁻¹', ['s⁻¹', 'mol dm⁻³ s⁻¹', 'dm⁶ mol⁻² s⁻¹'], 'k = rate/[A]².'),
           ('What shape is a graph of rate against concentration for a zero-order reactant?', 'a horizontal straight line', ['a straight line through the origin', 'an upward curve', 'a downward curve'], 'rate independent of [A].'),
           ('Which reaction property has a constant half-life?', 'a first-order reaction', ['a zero-order reaction', 'a second-order reaction', 'any reaction at constant temperature'], 't½ = ln 2/k.'),
           ('What shape is a concentration–time graph for a zero-order reactant?', 'a straight line with negative gradient', ['an exponential decay', 'a horizontal line', 'an upward curve'], 'constant rate.'),
           ('Which factor changes the value of the rate constant?', 'temperature', ['concentration', 'pressure', 'volume of solution'], 'k = Ae^(−Ea/RT).')],
    why=[('Explain why orders of reaction must be determined experimentally.', 'Orders depend on the mechanism (the rate-determining step), which cannot be deduced from the stoichiometric equation.'),
         ('Explain how a graph of rate against concentration can be used to determine the order with respect to a reactant.', 'Horizontal line: zero order; straight line through the origin: first order; upward curve (rate ∝ [A]²): second order.'),
         ('Explain why the half-life of a first-order reaction is independent of the initial concentration.', 'For first order, t½ = ln 2/k, which depends only on k; the same fraction of reactant reacts in each equal time interval.'),
         ('Explain why the iodination of propanone is zero order with respect to iodine.', 'Iodine is not involved in the rate-determining step (enol formation, catalysed by H⁺); it reacts in a fast later step.')],
    contrast=[('a first-order reaction', 'a second-order reaction', 'For first order, rate ∝ [A] and t½ is constant; for second order, rate ∝ [A]² and t½ increases as the concentration falls.'),
              ('the rate constant', 'the rate of reaction', 'The rate changes as concentrations change during a reaction; the rate constant k is fixed at a given temperature.')],
    misc=[('The orders in the rate equation are the coefficients in the balanced equation.', 'Orders are found by experiment and relate to the rate-determining step; e.g. 2N₂O₅ → 4NO₂ + O₂ is first order.'),
          ('A zero-order reactant is not needed for the reaction.', 'It is consumed in the reaction, but in a step after the rate-determining step, so its concentration does not affect the rate.'),
          ('The rate constant increases as the reaction proceeds.', 'k is constant at constant temperature; the rate falls because concentrations fall.')],
    apply=[('For rate = k[A]²[B], state the overall order and the units of k.', 'third order; dm⁶ mol⁻² s⁻¹', 2),
           ('A first-order reaction has k = 0.0231 s⁻¹. Calculate its half-life.', 't½ = 0.693/0.0231 = 30.0 s', 2)],
    evaluate=[('The initial-rates method is the best way to determine orders of reaction.', ['each experiment isolates one reactant', 'avoids complications from products and reverse reactions'], ['requires several experiments and tangent drawing (uncertainty)', 'continuous monitoring with half-life analysis can give the order from one run', 'isolation (large excess) methods may be simpler'], 'Initial rates are reliable and widely used, but half-life and graphical methods can be more efficient.')],
    extended=[('The reaction 2NO(g) + Br₂(g) → 2NOBr(g) is second order in NO and first order in Br₂. (a) Write the rate equation. (b) State the effect on the rate of doubling [NO] and halving [Br₂]. (c) Deduce the units of k. (d) Explain whether a single-step mechanism is likely.', '(a) rate = k[NO]²[Br₂]. (b) ×4 × ½ = ×2. (c) dm⁶ mol⁻² s⁻¹. (d) a termolecular collision is unlikely; probably two steps, e.g. NO + Br₂ ⇌ NOBr₂ (fast), NOBr₂ + NO → 2NOBr (slow).', 7, 'multi_step')],
))


def _rate_table(rng, rx):
    eq, a, b, m, n, ctx = rx
    k = rng.uniform(0.5, 9.5) * 10 ** rng.choice([-3, -2, -1, 0, 1])
    a0 = rng.choice([0.010, 0.020, 0.050, 0.100, 0.200])
    b0 = rng.choice([0.010, 0.020, 0.050, 0.100, 0.200])
    fa = rng.choice([2, 3])
    fb = rng.choice([2, 3])
    exps = [(a0, b0), (a0 * fa, b0), (a0, b0 * fb), (a0 * fa, b0 * fb)]
    rows = []
    for x, y in exps:
        r = k * x ** m * y ** n
        rows.append((x, y, rsf(r)))
    return k, rows


@R.add('ch03-st3', 'C3', (2, 5), 'numerical')
def c3_orders_table(rng, slot):
    rx = pick(rng, RATE_RX)
    eq, a, b, m, n, ctx = rx
    k, rows = _rate_table(rng, rx)
    tab = '\n'.join(f'{i + 1} | {sf(x)} | {sf(y)} | {sf(r)}' for i, (x, y, r) in enumerate(rows[:3]))
    x1, y1, r1 = rows[0]
    kk = r1 / (x1 ** m * y1 ** n)
    stem = (f'The initial rate of {ctx}, {eqp(eq)}, was measured at constant temperature.\n\nexperiment | [{chem(a)}] / mol dm⁻³ | [{chem(b)}] / mol dm⁻³ | initial rate / mol dm⁻³ s⁻¹\n{tab}\n\n'
            f'Deduce the order with respect to each reactant, write the rate equation and calculate the rate constant, with units.')
    return num(stem, f'{m} in {chem(a)}, {n} in {chem(b)}; {rexp(a, b, m, n)}; k = {q(kk, kunit(m + n))}',
               f'Exp 1→2: [{chem(a)}] ×{rows[1][0] / x1:.0f}, rate ×{rows[1][2] / r1:.3g} → order {m} (M1 A1); exp 1→3: [{chem(b)}] ×{rows[2][1] / y1:.0f}, rate ×{rows[2][2] / r1:.3g} → order {n} (A1); {rexp(a, b, m, n)} (A1); k = {sf(r1)}/({sf(x1)}{"²" if m == 2 else ""}{"" if n == 0 else " × " + sf(y1)}) = {q(kk, kunit(m + n))} (A1).', 5, 'multi_step')


@R.add('ch03-st3', 'C3', (1, 4), 'mcq')
def c3_rate_change(rng, slot):
    rx = pick(rng, RATE_RX)
    eq, a, b, m, n, ctx = rx
    fa = rng.choice([0.5, 2, 3, 4])
    fb = rng.choice([0.5, 1, 2, 3])
    f = fa ** m * fb ** n
    def fx(x):
        return f'{x:g}' if x >= 1 else ('½' if x == 0.5 else '¼' if x == 0.25 else '⅛' if x == 0.125 else f'{x:g}')
    def ch_(s, v):
        return 'doubled' if v == 2 else 'tripled' if v == 3 else 'quadrupled' if v == 4 else 'halved' if v == 0.5 else 'unchanged'
    stem = f'For {ctx}, {rexp(a, b, m, n)}. By what factor does the rate change if [{chem(a)}] is {ch_(a, fa)} and [{chem(b)}] is {ch_(b, fb)}?'
    cands = [fa * fb, fa ** 2 * fb ** 2, fa * fb ** 2, fa ** 2 * fb, fa ** m, fb ** n, fa ** (m + 1) * fb ** n]
    wr = [f'× {fx(x)}' for x in dict.fromkeys(cands) if abs(x - f) > 1e-9]
    if len(wr) < 3:
        return None
    return mcq(rng, stem, f'× {fx(f)}', wr[:3], f'factor = ({fx(fa)}){sup(m) if m != 1 else ""} × ({fx(fb)}){sup(n) if n != 1 else ""} = {fx(f)}.')


@R.add('ch03-st3', 'C3', (1, 4), 'mcq')
def c3_k_units(rng, slot):
    rx = pick(rng, RATE_RX)
    eq, a, b, m, n, ctx = rx
    o = m + n
    right = kunit(o)
    stem = f'The rate equation for {ctx} is {rexp(a, b, m, n)}. What are the units of k?'
    return mcq(rng, stem, right, [kunit(x) for x in range(4) if x != o], f'overall order {o} → k = rate/(conc){sup(o) if o > 1 else ""} → {right}.')


@R.add('ch03-st3', 'C3', (2, 4), 'numerical')
def c3_half_life(rng, slot):
    eq, sp, order, ctx = pick(rng, [r for r in ONE_RX if r[2] == 1])
    if rng.random() < 0.5:
        k = rng.uniform(1, 9) * 10 ** rng.choice([-4, -3, -2])
        stem = f'The decomposition in {ctx} is first order with k = {sf(k)} s⁻¹. Calculate its half-life.'
        return num(stem, q(math.log(2) / k, 's'), f't½ = ln 2/k = 0.693/{sf(k)} (M1) = {q(math.log(2) / k, "s")} (A1).', 2)
    th = rng.choice([20, 30, 45, 60, 90, 120, 300])
    nhl = rng.choice([2, 3, 4])
    c0 = rng.choice([0.400, 0.800, 1.20, 1.60])
    stem = f'In {ctx} (first order), the half-life is {th} s. Starting from [{chem(sp)}] = {sf(c0)} mol dm⁻³, calculate the concentration after {th * nhl} s and the rate constant.'
    return num(stem, f'{sf(c0 / 2 ** nhl)} mol dm⁻³; k = {q(math.log(2) / th, "s⁻¹")}', f'{nhl} half-lives (M1): {sf(c0)}/{2 ** nhl} = {sf(c0 / 2 ** nhl)} mol dm⁻³ (A1); k = 0.693/{th} = {q(math.log(2) / th, "s⁻¹")} (A1).', 3)


R.mcqs('ch03-st3', 'C2', (1, 4), [
    ('Why does the rate constant have different units for reactions of different overall order?', 'k = rate/(concentration terms), and the number of concentration terms depends on the overall order.', ['Units of k are always s⁻¹.', 'k depends on the concentration.', 'Different temperatures are used.'], 'Dimensional analysis.'),
    ('A reaction has rate = k[X]². Which graph is a straight line through the origin?', 'rate against [X]²', ['rate against [X]', '[X] against time', 'rate against 1/[X]'], 'rate ∝ [X]².'),
    ('Why can a reactant be zero order?', 'It takes part only after the rate-determining step.', ['It is a catalyst.', 'It is present in very small amount.', 'It is a product.'], 'Not in RDS.'),
    ('What happens to the half-life of a first-order reaction if the initial concentration is doubled?', 'It stays the same.', ['It doubles.', 'It halves.', 'It quadruples.'], 't½ = ln 2/k.'),
])


@p1b(R, 'ch03-st3')
def p1b_initial_rates(rng, slot):
    rx = pick(rng, RATE_RX)
    eq, a, b, m, n, ctx = rx
    k, rows = _rate_table(rng, rx)
    tab = '\n'.join(f'{i + 1} | {sf(x)} | {sf(y)} | {sf(r)}' for i, (x, y, r) in enumerate(rows))
    x1, y1, r1 = rows[0]
    kk = r1 / (x1 ** m * y1 ** n)
    intro = f'The initial rate of {ctx}, {eqp(eq)}, was measured.\n\nexperiment | [{chem(a)}] / mol dm⁻³ | [{chem(b)}] / mol dm⁻³ | initial rate / mol dm⁻³ s⁻¹\n{tab}'
    xn, yn = rows[0][0] * 1.5, rows[0][1] * 2.5
    rn = kk * xn ** m * yn ** n
    return dict(intro=intro, parts=[
        (f'Deduce the order of reaction with respect to {chem(a)} and to {chem(b)}.', f'{m} and {n}', f'Exps 1 and 2 → {m} (A1); exps 1 and 3 → {n} (A1).', 2),
        ('Write the rate equation and calculate the rate constant, including units.', f'{rexp(a, b, m, n)}; {q(kk, kunit(m + n))}', f'{rexp(a, b, m, n)} (A1); k = {q(kk, kunit(m + n))} (A1, units A1).', 3),
        (f'Calculate the initial rate when [{chem(a)}] = {sf(xn)} and [{chem(b)}] = {sf(yn)} mol dm⁻³.', q(rn, 'mol dm⁻³ s⁻¹'), f'rate = k × {sf(xn)}{sup(m) if m > 1 else ""}{"" if n == 0 else " × " + sf(yn) + (sup(n) if n > 1 else "")} = {q(rn, "mol dm⁻³ s⁻¹")} (A1).', 1),
        ('Use experiment 4 to check your rate equation.', f'predicted {sf(kk * rows[3][0] ** m * rows[3][1] ** n)}, matches {sf(rows[3][2])}', f'Predicted rate equals measured rate (1).', 1)],
        extras=[('State why the temperature must be kept constant in all experiments.', 'k depends on temperature, so a change would alter the rate independently of concentration.', 'k varies with T (1).', 1)])


# ---- ch03-st4 mechanisms and Arrhenius (HL) ----
MECH = [('2NO₂ + F₂ → 2NO₂F', 'Step 1 (slow): NO₂ + F₂ → NO₂F + F; Step 2 (fast): NO₂ + F → NO₂F', 'rate = k[NO₂][F₂]', 'F atom'),
        ('NO₂ + CO → NO + CO₂', 'Step 1 (slow): NO₂ + NO₂ → NO₃ + NO; Step 2 (fast): NO₃ + CO → NO₂ + CO₂', 'rate = k[NO₂]²', 'NO₃'),
        ('(CH₃)₃CBr + OH⁻ → (CH₃)₃COH + Br⁻', 'Step 1 (slow): (CH₃)₃CBr → (CH₃)₃C⁺ + Br⁻; Step 2 (fast): (CH₃)₃C⁺ + OH⁻ → (CH₃)₃COH', 'rate = k[(CH₃)₃CBr]', '(CH₃)₃C⁺ carbocation'),
        ('2H₂O₂ → 2H₂O + O₂ (I⁻ catalysed)', 'Step 1 (slow): H₂O₂ + I⁻ → H₂O + IO⁻; Step 2 (fast): H₂O₂ + IO⁻ → H₂O + O₂ + I⁻', 'rate = k[H₂O₂][I⁻]', 'IO⁻'),
        ('2NO + O₂ → 2NO₂', 'Step 1 (fast equilibrium): 2NO ⇌ N₂O₂; Step 2 (slow): N₂O₂ + O₂ → 2NO₂', 'rate = k[NO]²[O₂]', 'N₂O₂'),
        ('O₃ + O → 2O₂ (Cl catalysed)', 'Step 1 (slow): Cl + O₃ → ClO + O₂; Step 2 (fast): ClO + O → Cl + O₂', 'rate = k[Cl][O₃]', 'ClO'),
        ('H₂ + 2ICl → I₂ + 2HCl', 'Step 1 (slow): H₂ + ICl → HI + HCl; Step 2 (fast): HI + ICl → I₂ + HCl', 'rate = k[H₂][ICl]', 'HI')]

R.facts('ch03-st4', F(
    terms=[('reaction mechanism', 'the sequence of elementary steps by which an overall reaction occurs'),
           ('rate-determining step', 'the slowest step in a reaction mechanism, which determines the overall rate'),
           ('molecularity', 'the number of particles (molecules, atoms or ions) that take part in an elementary step'),
           ('intermediate', 'a species formed in one step of a mechanism and consumed in a later step'),
           ('Arrhenius equation', 'k = Ae^(−Ea/RT), relating the rate constant to the activation energy and absolute temperature'),
           ('frequency factor (A)', 'the pre-exponential factor in the Arrhenius equation, related to collision frequency and the fraction with correct orientation')],
    facts=[('What is the gradient of a graph of ln k against 1/T?', '−Ea/R', ['Ea/R', '−R/Ea', 'ln A'], 'ln k = ln A − Ea/RT.'),
           ('Which species in a mechanism is a catalyst?', 'a species used in an early step and regenerated in a later step', ['a species formed then used up', 'the product of the slow step', 'a reactant in the overall equation'], 'Catalyst regenerated.'),
           ('A step involving two particles colliding is described as', 'bimolecular', ['unimolecular', 'termolecular', 'zero order'], 'Molecularity 2.'),
           ('Why are termolecular steps rare?', 'A simultaneous collision of three particles with the right energy and orientation is very unlikely.', ['Three particles cannot react.', 'They are always fast.', 'They have zero activation energy.'], 'Low probability.'),
           ('What is the y-intercept of a graph of ln k against 1/T?', 'ln A', ['A', 'Ea', '−Ea/R'], 'At 1/T = 0.'),
           ('Which statement about an intermediate is correct?', 'It is formed in one step and used up in a later step.', ['It appears in the overall equation.', 'It is the same as the transition state.', 'It is regenerated at the end.'], 'Not in overall equation.')],
    why=[('Explain why the rate equation depends only on the species in the rate-determining step (and steps before it).', 'The overall rate cannot be faster than the slowest step; species involved only after the slow step do not affect how fast it proceeds.'),
         ('Explain how a graph of ln k against 1/T is used to determine the activation energy.', 'ln k = ln A − (Ea/R)(1/T), so a plot of ln k against 1/T is a straight line with gradient −Ea/R; Ea = −gradient × R.'),
         ('Explain why a proposed mechanism can be shown to be wrong but never proved correct by kinetic data.', 'A mechanism must agree with the rate equation and the overall equation; several different mechanisms can fit the same data, so agreement supports but does not prove it.'),
         ('Explain why reactions with large activation energies are more sensitive to temperature changes.', 'In k = Ae^(−Ea/RT), the exponential term changes more for a given change in T when Ea is large, so k rises more steeply.')],
    contrast=[('molecularity', 'order of reaction', 'Molecularity is the number of particles in one elementary step (theoretical); order is the experimentally determined power of a concentration in the rate equation.'),
              ('an intermediate', 'a catalyst in a mechanism', 'An intermediate is formed then consumed; a catalyst is consumed in an early step and regenerated later.')],
    misc=[('The slow step is always the first step of a mechanism.', 'The rate-determining step can be any step; if a fast pre-equilibrium comes first, reactants in it also appear in the rate equation.'),
          ('A larger activation energy means the rate constant is less affected by temperature.', 'Larger Ea makes k more sensitive to temperature (steeper ln k vs 1/T line).')],
    apply=[('For the mechanism Step 1 (slow) A + B → C; Step 2 (fast) C + B → D, deduce the overall equation and the rate equation.', 'A + 2B → D; rate = k[A][B]', 2),
           ('An Arrhenius plot has a gradient of −6500 K. Calculate the activation energy.', 'Ea = 6500 × 8.31 = 54.0 kJ mol⁻¹', 2)],
    evaluate=[('Kinetic data are the best evidence for a reaction mechanism.', ['rate equations directly test which species are in the RDS', 'orders rule out many mechanisms'], ['several mechanisms may fit the same rate equation', 'isotopic labelling, stereochemistry and detection of intermediates give independent evidence'], 'Kinetics is a key test, but mechanisms are best supported by several independent lines of evidence.'),
              ('The Arrhenius equation shows that temperature is the most important factor affecting rate.', ['k depends exponentially on T', 'small T changes cause large rate changes'], ['catalysts reduce Ea and can have larger effects', 'concentration and surface area also matter', 'many biological and industrial systems cannot tolerate high T'], 'Temperature has a powerful exponential effect, but catalysts and conditions are often more practical levers.')],
    extended=[('The reaction 2NO(g) + 2H₂(g) → N₂(g) + 2H₂O(g) has rate = k[NO]²[H₂]. (a) State the overall order. (b) Propose a two-step mechanism consistent with the rate equation and identify the intermediate. (c) The rate constant doubles when the temperature rises from 1100 K to 1150 K. Calculate Ea. (d) Explain why the reaction is very slow at room temperature.', '(a) 3. (b) 2NO + H₂ → N₂ + H₂O₂ (slow); H₂O₂ + H₂ → 2H₂O (fast); intermediate H₂O₂ (or N₂O pathway). (c) ln 2 = (Ea/8.31)(1/1100 − 1/1150) → Ea ≈ 146 kJ mol⁻¹. (d) high Ea: very small fraction of collisions have E ≥ Ea at 298 K.', 8, 'multi_step')],
))


@R.add('ch03-st4', 'C3', (2, 5), 'numerical')
def c3_arrhenius_ea(rng, slot):
    ea = rng.uniform(35, 140)
    t1 = rng.choice([288, 293, 298, 303, 310, 320])
    t2 = t1 + rng.choice([10, 15, 20, 30, 40])
    ratio = math.exp(ea * 1000 / RGAS * (1 / t1 - 1 / t2))
    ratio = rsf(ratio)
    ea_c = RGAS * math.log(ratio) / (1 / t1 - 1 / t2) / 1000
    k1 = rng.uniform(1, 9) * 10 ** rng.choice([-5, -4, -3])
    k2 = k1 * ratio
    stem = pick(rng, [f'The rate constant of a reaction is {sf(k1)} s⁻¹ at {t1} K and {sf(k2)} s⁻¹ at {t2} K. Calculate the activation energy.',
                      f'When the temperature is raised from {t1} K to {t2} K, the rate constant increases from {sf(k1)} to {sf(k2)} s⁻¹. Use the Arrhenius equation to determine Ea in kJ mol⁻¹.'])
    ea_c = RGAS * math.log(rsf(k2) / rsf(k1)) / (1 / t1 - 1 / t2) / 1000
    return num(stem, q(ea_c, 'kJ mol⁻¹'), f'ln(k₂/k₁) = (Ea/R)(1/T₁ − 1/T₂) (M1); ln({sf(rsf(k2) / rsf(k1))}) = Ea/8.31 × {sf(1 / t1 - 1 / t2)} (M1); Ea = {q(ea_c, "kJ mol⁻¹")} (A1).', 3)


@R.add('ch03-st4', 'C3', (2, 5), 'numerical')
def c3_arrhenius_k2(rng, slot):
    ea = rng.choice([45, 52, 60, 68, 75, 84, 90, 105])
    t1 = rng.choice([290, 298, 300, 310])
    t2 = t1 + rng.choice([10, 20, 25, 35, 50])
    k1 = rng.uniform(1, 9) * 10 ** rng.choice([-4, -3, -2])
    k2 = k1 * math.exp(ea * 1000 / RGAS * (1 / t1 - 1 / t2))
    stem = f'A reaction has Ea = {ea} kJ mol⁻¹ and k = {sf(k1)} dm³ mol⁻¹ s⁻¹ at {t1} K. Calculate k at {t2} K.'
    return num(stem, q(k2, 'dm³ mol⁻¹ s⁻¹'), f'ln(k₂/k₁) = ({ea * 1000}/8.31)(1/{t1} − 1/{t2}) = {sf(math.log(k2 / k1))} (M1); k₂ = {sf(k1)} × e^{sf(math.log(k2 / k1))} (M1) = {q(k2, "dm³ mol⁻¹ s⁻¹")} (A1).', 3)


@R.add('ch03-st4', 'C3', (1, 4), 'mcq')
def c3_gradient_ea(rng, slot):
    g = rng.randint(25, 160) * 100
    ea = g * RGAS / 1000
    stem = pick(rng, [f'A graph of ln k against 1/T is a straight line of gradient −{g} K. What is the activation energy?', f'An Arrhenius plot (ln k vs 1/T) has a gradient of −{g:,} K. Determine Ea.'.replace(',', ' ')])
    return nmcq(rng, stem, ea, [g / RGAS / 1000, g * RGAS, g / 1000], 'kJ mol⁻¹', f'Ea = −gradient × R = {g} × 8.31 = {sf(ea * 1000)} J mol⁻¹ = {sf(ea)} kJ mol⁻¹.', extra=True)


@R.add('ch03-st4', 'C3', (1, 4), 'mcq')
def c3_mech_rate(rng, slot):
    ov, steps, rate, inter = pick(rng, MECH)
    others = list(dict.fromkeys(m[2] for m in MECH if m[2] != rate))
    rng.shuffle(others)
    if rng.random() < 0.6:
        stem = f'The proposed mechanism for {ov} is: {steps}. Which rate equation is consistent with this mechanism?'
        return mcq(rng, stem, rate, others[:3], f'The slow step (and any fast equilibrium before it) determines the rate: {rate}.')
    oth = list(dict.fromkeys(m[3] for m in MECH if m[3] != inter))
    rng.shuffle(oth)
    stem = f'In the mechanism {steps}, which species is an intermediate?'
    return mcq(rng, stem, inter, oth[:3], f'{inter} is formed in one step and used up in the next.')


R.mcqs('ch03-st4', 'C2', (1, 4), [
    ('Why can the rate equation not be deduced from the overall balanced equation?', 'The rate depends on the mechanism, in particular the rate-determining step.', ['The balanced equation is never correct.', 'Orders are always 1.', 'The equation does not show the catalyst.'], 'Kinetics ≠ stoichiometry.'),
    ('How does a catalyst change an Arrhenius plot?', 'The line is less steep because Ea is lower.', ['The line is steeper.', 'The gradient becomes positive.', 'The line does not change.'], 'Gradient = −Ea/R.'),
    ('A mechanism has a fast equilibrium before a slow step. Which species appear in the rate equation?', 'those in the slow step, with any intermediate replaced by the reactants that formed it', ['only those in the slow step', 'only those in the fast step', 'all species in the overall equation'], 'Pre-equilibrium.'),
    ('Why does the rate constant increase with temperature?', 'The exponential term e^(−Ea/RT) increases as T increases.', ['A decreases as T increases.', 'Ea increases with T.', 'The concentrations increase.'], 'Arrhenius.'),
])


@p1b(R, 'ch03-st4')
def p1b_arrhenius(rng, slot):
    ea = rng.uniform(45, 95)
    A = 10 ** rng.uniform(9, 12)
    Ts = [293, 303, 313, 323, 333]
    rows = []
    for T in Ts:
        k = A * math.exp(-ea * 1000 / (RGAS * T))
        rows.append((T, rsf(k)))
    pts = [(1 / T, math.log(k)) for T, k in rows]
    g = (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0])
    ea_c = -g * RGAS / 1000
    tab = '\n'.join(f'{T} | {sf(k)} | {1 / T * 1000:.3f} | {math.log(k):.2f}' for T, k in rows)
    intro = f'The rate constant of a reaction was measured at several temperatures.\n\nT / K | k / s⁻¹ | (1/T) / 10⁻³ K⁻¹ | ln k\n{tab}'
    lnA = pts[0][1] - g * pts[0][0]
    return dict(intro=intro, parts=[
        ('State the quantities that should be plotted to obtain a straight line, and explain why.', 'ln k (y) against 1/T (x), because ln k = ln A − (Ea/R)(1/T).', 'ln k vs 1/T (1); linear form of Arrhenius equation (1).', 2),
        ('Determine the gradient of the line using the first and last points.', f'{sf(g)} K', f'({pts[-1][1]:.2f} − {pts[0][1]:.2f})/({pts[-1][0] * 1000:.3f} − {pts[0][0] * 1000:.3f}) × 10³ (M1) = {sf(g)} K (A1).', 2),
        ('Calculate the activation energy.', q(ea_c, 'kJ mol⁻¹'), f'Ea = −gradient × R = {sf(-g)} × 8.31 = {q(ea_c, "kJ mol⁻¹")} (A1).', 1),
        ('Determine the frequency factor, A.', q(math.exp(lnA), 's⁻¹'), f'ln A = ln k − gradient/T = {lnA:.2f} (M1); A = {q(math.exp(lnA), "s⁻¹")} (A1).', 2),
        ('Suggest why using a line of best fit through all points is better than using two points.', 'It uses all the data, reducing the effect of random error in any single measurement.', 'Averages random errors / identifies outliers (1).', 1)],
        extras=[])


# =============================================================================================
# ch04 R2.3 How far? The extent of chemical change
# =============================================================================================
# equation text, reactants {sp: coef}, products {sp: coef}, ΔH / kJ, all-gas?, context
EQM = [
    ('N2(g) + 3H2(g) ⇌ 2NH3(g)', {'N2': 1, 'H2': 3}, {'NH3': 2}, -92, True, 'the Haber process'),
    ('2SO2(g) + O2(g) ⇌ 2SO3(g)', {'SO2': 2, 'O2': 1}, {'SO3': 2}, -196, True, 'the Contact process'),
    ('H2(g) + I2(g) ⇌ 2HI(g)', {'H2': 1, 'I2': 1}, {'HI': 2}, 52, True, 'the formation of hydrogen iodide'),
    ('N2O4(g) ⇌ 2NO2(g)', {'N2O4': 1}, {'NO2': 2}, 57, True, 'the dissociation of dinitrogen tetroxide'),
    ('CO(g) + 2H2(g) ⇌ CH3OH(g)', {'CO': 1, 'H2': 2}, {'CH3OH': 1}, -91, True, 'methanol synthesis'),
    ('CO(g) + H2O(g) ⇌ CO2(g) + H2(g)', {'CO': 1, 'H2O': 1}, {'CO2': 1, 'H2': 1}, -41, True, 'the water–gas shift reaction'),
    ('CH4(g) + H2O(g) ⇌ CO(g) + 3H2(g)', {'CH4': 1, 'H2O': 1}, {'CO': 1, 'H2': 3}, 206, True, 'steam reforming of methane'),
    ('PCl5(g) ⇌ PCl3(g) + Cl2(g)', {'PCl5': 1}, {'PCl3': 1, 'Cl2': 1}, 88, True, 'the dissociation of phosphorus pentachloride'),
    ('N2(g) + O2(g) ⇌ 2NO(g)', {'N2': 1, 'O2': 1}, {'NO': 2}, 181, True, 'the formation of nitrogen monoxide in car engines'),
    ('2NO(g) + O2(g) ⇌ 2NO2(g)', {'NO': 2, 'O2': 1}, {'NO2': 2}, -114, True, 'the oxidation of nitrogen monoxide'),
    ('CH3COOH(l) + C2H5OH(l) ⇌ CH3COOC2H5(l) + H2O(l)', {'CH3COOH': 1, 'C2H5OH': 1}, {'CH3COOC2H5': 1, 'H2O': 1}, -2, False, 'esterification of ethanoic acid'),
    ('2HI(g) ⇌ H2(g) + I2(g)', {'HI': 2}, {'H2': 1, 'I2': 1}, -52, True, 'the decomposition of hydrogen iodide'),
    ('C2H4(g) + H2O(g) ⇌ C2H5OH(g)', {'C2H4': 1, 'H2O': 1}, {'C2H5OH': 1}, -45, True, 'the hydration of ethene'),
    ('2NO2(g) ⇌ N2O4(g)', {'NO2': 2}, {'N2O4': 1}, -57, True, 'the dimerisation of nitrogen dioxide'),
]
GAS_EQM = [e for e in EQM if e[4]]


def kc_expr(e):
    def side(d):
        return ''.join(f'[{chem(s)}]' + (sup(c) if c > 1 else '') for s, c in d.items())
    return f'Kc = {side(e[2])} / {side(e[1])}'


def kc_val(e, conc):
    num_ = 1.0
    den = 1.0
    for s, c in e[2].items():
        num_ *= conc[s] ** c
    for s, c in e[1].items():
        den *= conc[s] ** c
    return num_ / den


def dn_gas(e):
    return sum(e[2].values()) - sum(e[1].values())


R.facts('ch04-st1', F(
    terms=[('dynamic equilibrium', 'the state of a reversible reaction in a closed system in which the forward and reverse rates are equal and concentrations remain constant'),
           ('equilibrium constant (Kc)', 'the value of the equilibrium expression (product concentrations raised to their coefficients divided by reactant concentrations raised to theirs) at a given temperature'),
           ('closed system', 'a system in which matter cannot enter or leave, although energy can be exchanged'),
           ('position of equilibrium', 'the relative amounts of reactants and products present at equilibrium'),
           ('homogeneous equilibrium', 'an equilibrium in which all reactants and products are in the same phase'),
           ('reversible reaction', 'a reaction that can proceed in both the forward and reverse directions')],
    facts=[('Which statement about a system at dynamic equilibrium is correct?', 'The rates of the forward and reverse reactions are equal.', ['The reactions have stopped.', 'The concentrations of reactants and products are equal.', 'Only the forward reaction occurs.'], 'Equal rates; constant concentrations.'),
           ('What does a very large value of Kc (e.g. 10¹⁰) indicate?', 'The equilibrium lies far to the right; the reaction goes almost to completion.', ['The reaction is very fast.', 'The equilibrium lies to the left.', 'The reaction is endothermic.'], 'Products dominate.'),
           ('Which factor changes the value of Kc?', 'temperature', ['pressure', 'concentration of a reactant', 'adding a catalyst'], 'K depends only on T.'),
           ('How is Kc for the reverse reaction related to Kc for the forward reaction?', 'It is the reciprocal, 1/Kc.', ['It is the same.', 'It is −Kc.', 'It is Kc².'], 'Expression inverted.'),
           ('Which condition is necessary to establish an equilibrium?', 'a closed system', ['a catalyst', 'high pressure', 'equal amounts of reactants'], 'No matter escapes.'),
           ('If the coefficients of an equation are doubled, the new equilibrium constant is', 'Kc²', ['2Kc', 'Kc/2', '√Kc'], 'Each power doubles.')],
    why=[('Explain why the concentrations at equilibrium remain constant even though reactions are still occurring.', 'The forward and reverse reactions proceed at the same rate, so each species is formed as fast as it is used up.'),
         ('Explain why a catalyst does not change the value of Kc.', 'It lowers the activation energy of the forward and reverse reactions equally, speeding both by the same factor, so equilibrium is reached faster but its position is unchanged.'),
         ('Explain what the magnitude of Kc tells you about an equilibrium mixture.', 'Kc ≫ 1: mostly products (lies to the right); Kc ≪ 1: mostly reactants (lies to the left); Kc ≈ 1: significant amounts of both.'),
         ('Explain why an equilibrium cannot be established in an open beaker for CaCO₃(s) ⇌ CaO(s) + CO₂(g).', 'CO₂ escapes, so the reverse reaction cannot occur at the same rate; the decomposition continues until completion.')],
    contrast=[('a static equilibrium', 'a dynamic equilibrium', 'In a static equilibrium nothing is changing; in a dynamic equilibrium forward and reverse reactions continue at equal rates.'),
              ('the position of equilibrium', 'the equilibrium constant', 'The position (composition) can change with concentration or pressure; Kc is fixed at a given temperature.')],
    misc=[('At equilibrium the concentrations of reactants and products are equal.', 'At equilibrium the concentrations are constant, not equal; their ratio is given by Kc.'),
          ('Adding a catalyst increases the yield at equilibrium.', 'A catalyst only increases the rate at which equilibrium is reached; the equilibrium yield is unchanged.'),
          ('At equilibrium both the forward and backward reactions stop.', 'Both reactions continue at equal rates (dynamic equilibrium).')],
    apply=[('Write the equilibrium expression for 4NH₃(g) + 5O₂(g) ⇌ 4NO(g) + 6H₂O(g).', 'Kc = [NO]⁴[H₂O]⁶ / [NH₃]⁴[O₂]⁵', 1),
           ('Kc for H₂(g) + I₂(g) ⇌ 2HI(g) is 54 at 700 K. State Kc for HI(g) ⇌ ½H₂(g) + ½I₂(g) at 700 K.', '1/√54 = 0.136', 2)],
    evaluate=[('The equilibrium constant is more useful than the rate constant in industry.', ['K shows the maximum possible yield under given conditions', 'guides choice of temperature and pressure'], ['a large K is useless if the rate is too slow (k matters)', 'compromise conditions balance rate and yield', 'catalyst choice depends on kinetics'], 'Both are essential: K sets the limit, k determines how quickly it is approached.'),
              ('The concept of dynamic equilibrium applies only to chemical reactions in closed laboratory vessels.', ['equilibrium requires a closed system', 'textbook examples are closed vessels'], ['phase equilibria (liquid–vapour) and solubility equilibria are dynamic', 'biological and environmental systems (O₂–haemoglobin, CO₂–ocean) behave similarly', 'steady states in open systems resemble equilibria'], 'The idea extends far beyond laboratory vessels, though true equilibrium strictly needs a closed system.')],
    extended=[('At 400 °C, an equilibrium mixture for N₂(g) + 3H₂(g) ⇌ 2NH₃(g) contains [N₂] = 0.40, [H₂] = 1.20 and [NH₃] = 0.20 mol dm⁻³. (a) Write the Kc expression. (b) Calculate Kc. (c) State and explain what the value indicates. (d) Deduce Kc for 2NH₃ ⇌ N₂ + 3H₂ at the same temperature.', '(a) Kc = [NH₃]²/[N₂][H₂]³. (b) 0.04/(0.40 × 1.728) = 0.0579. (c) < 1: reactants predominate at 400 °C. (d) 1/0.0579 = 17.3.', 6, 'multi_step')],
))


@R.add('ch04-st1', 'C3', (1, 4), 'mcq')
def c3_kc_expr(rng, slot):
    e = pick(rng, EQM)
    right = kc_expr(e)
    rev = (e[0], e[2], e[1]) + e[3:]
    def side(d, flat=False):
        return ''.join(f'[{chem(s)}]' + ('' if flat or c == 1 else sup(c)) for s, c in d.items())
    wr = [kc_expr(rev), f'Kc = {side(e[2], True)} / {side(e[1], True)}',
          'Kc = ' + ' + '.join(f'{c if c > 1 else ""}[{chem(s)}]' for s, c in e[2].items()) + ' / ' + ' + '.join(f'{c if c > 1 else ""}[{chem(s)}]' for s, c in e[1].items())]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'What is the equilibrium expression for {eqp(e[0])}?'
    return mcq(rng, stem, right, wr[:3], 'Products over reactants, each raised to its coefficient.')


@R.add('ch04-st1', 'C3', (2, 5), 'numerical')
def c3_kc_calc(rng, slot):
    e = pick(rng, EQM)
    conc = {s: round(rng.uniform(0.05, 1.5), 2) for s in list(e[1]) + list(e[2])}
    K = kc_val(e, conc)
    vals = ', '.join(f'[{chem(s)}] = {conc[s]:.2f}' for s in conc)
    stem = pick(rng, [f'For {e[5]}, {eqp(e[0])}, an equilibrium mixture contains (mol dm⁻³): {vals}. Calculate Kc at this temperature.',
                      f'Calculate the equilibrium constant for {eqp(e[0])} given the equilibrium concentrations {vals} (all in mol dm⁻³).'])
    return num(stem, sf(K), f'{kc_expr(e)} (M1); substitution (M1); Kc = {sf(K)} (A1).', 3)


@R.add('ch04-st1', 'C3', (1, 4), 'mcq')
def c3_kc_manip(rng, slot):
    e = pick(rng, GAS_EQM)
    K = rsf(10 ** rng.uniform(-3, 4))
    kind = pick(rng, ['reverse', 'double', 'half'])
    if kind == 'reverse':
        v, txt = 1 / K, 'the reverse reaction'
    elif kind == 'double':
        v, txt = K ** 2, 'the equation with all coefficients doubled'
    else:
        v, txt = K ** 0.5, 'the equation with all coefficients halved'
    stem = f'At a certain temperature Kc = {sf(K)} for {eqp(e[0])}. What is the value of Kc for {txt} at the same temperature?'
    cands = [1 / K, K ** 2, K ** 0.5, 2 * K, K / 2, -K, 1 / K ** 2]
    wr = [sf(x) for x in cands if x > 0 and sf(x) != sf(v)]
    wr = list(dict.fromkeys(wr))
    rng.shuffle(wr)
    return mcq(rng, stem, sf(v), wr[:3], {'reverse': 'Reverse → 1/Kc', 'double': 'Coefficients ×2 → Kc²', 'half': 'Coefficients ×½ → √Kc'}[kind] + f' = {sf(v)}.')


@R.add('ch04-st1', 'C3', (1, 4), 'mcq')
def c3_k_meaning(rng, slot):
    e = pick(rng, EQM)
    exp_ = rng.choice([-12, -8, -5, -3, 3, 5, 8, 12, 0])
    K = rng.uniform(1.2, 9.5) * 10 ** exp_ if exp_ else rng.uniform(0.5, 2.0)
    if exp_ > 0:
        right = 'The equilibrium mixture contains mostly products.'
    elif exp_ < 0:
        right = 'The equilibrium mixture contains mostly reactants.'
    else:
        right = 'Significant amounts of both reactants and products are present.'
    wr = [x for x in ['The equilibrium mixture contains mostly products.', 'The equilibrium mixture contains mostly reactants.', 'Significant amounts of both reactants and products are present.', 'The reaction is very fast.', 'The reaction has stopped.'] if x != right]
    rng.shuffle(wr)
    stem = f'For {eqp(e[0])}, Kc = {sf(K)} at a given temperature. Which statement is correct?'
    return mcq(rng, stem, right, wr[:3], f'Kc {"≫ 1" if exp_ > 0 else "≪ 1" if exp_ < 0 else "≈ 1"}; K says nothing about rate.')


R.mcqs('ch04-st1', 'C2', (1, 4), [
    ('Why does an equilibrium mixture appear unchanging?', 'The forward and reverse reactions occur at equal rates.', ['All reactions have stopped.', 'The reactants have been used up.', 'The concentrations are equal.'], 'Dynamic.'),
    ('Which change could make a reversible reaction in a sealed flask reach equilibrium faster without changing the equilibrium composition?', 'adding a catalyst', ['adding more reactant', 'raising the temperature', 'removing product'], 'Catalyst speeds both directions.'),
    ('What is the relationship between Kc for a reaction and Kc for its reverse?', 'They are reciprocals.', ['They are equal.', 'They add up to 1.', 'They have opposite signs.'], '1/Kc.'),
    ('Why are concentrations of pure solids omitted from equilibrium expressions?', 'Their concentration is effectively constant.', ['They do not take part in the reaction.', 'They are always products.', 'They react too slowly.'], 'Included in K.'),
])


# ---- ch04-st2 Le Chatelier ----
def lc_answer(e, change):
    dH, dn = e[3], dn_gas(e)
    if change == 'increase T':
        return ('right' if dH > 0 else 'left'), ('increases' if dH > 0 else 'decreases')
    if change == 'decrease T':
        return ('left' if dH > 0 else 'right'), ('decreases' if dH > 0 else 'increases')
    if change == 'increase p':
        return ('left' if dn > 0 else 'right' if dn < 0 else 'no shift'), 'no change'
    if change == 'decrease p':
        return ('right' if dn > 0 else 'left' if dn < 0 else 'no shift'), 'no change'
    if change == 'add reactant':
        return 'right', 'no change'
    if change == 'remove product':
        return 'right', 'no change'
    if change == 'add product':
        return 'left', 'no change'
    return 'no shift', 'no change'


CHANGE_TXT = {'increase T': 'the temperature is increased', 'decrease T': 'the temperature is decreased', 'increase p': 'the pressure is increased by reducing the volume',
              'decrease p': 'the pressure is decreased by increasing the volume', 'add reactant': 'more {r} is added', 'remove product': '{p} is removed as it forms',
              'add product': 'more {p} is added', 'catalyst': 'a catalyst is added'}


def _ctext(e, ch):
    r = chem(list(e[1])[0])
    p = chem(list(e[2])[0])
    return CHANGE_TXT[ch].format(r=r, p=p)


R.facts('ch04-st2', F(
    terms=[('Le Chatelier’s principle', 'if a system at equilibrium is subjected to a change, the position of equilibrium shifts to partially counteract (minimise) the change'),
           ('yield', 'the amount of product obtained, often expressed as a percentage of the theoretical maximum'),
           ('compromise conditions', 'industrial conditions chosen to balance equilibrium yield, rate, cost and safety'),
           ('exothermic reaction', 'a reaction that releases heat to the surroundings (ΔH negative)')],
    facts=[('What is the effect of increasing the pressure on N₂(g) + 3H₂(g) ⇌ 2NH₃(g)?', 'The position shifts right, towards fewer gas moles.', ['The position shifts left.', 'Kc increases.', 'There is no effect.'], '4 → 2 mol gas.'),
           ('What happens to Kc for an exothermic reaction when the temperature increases?', 'Kc decreases.', ['Kc increases.', 'Kc is unchanged.', 'Kc becomes negative.'], 'Equilibrium shifts in the endothermic direction.'),
           ('Which change has no effect on the position of H₂(g) + I₂(g) ⇌ 2HI(g)?', 'increasing the pressure', ['increasing the temperature', 'adding hydrogen', 'removing HI'], 'Equal gas moles (2 = 2).'),
           ('Why is an iron catalyst used in the Haber process?', 'To increase the rate at which equilibrium is reached.', ['To increase the equilibrium yield.', 'To increase Kc.', 'To make the reaction exothermic.'], 'Catalysts affect rate only.'),
           ('How does the equilibrium respond when a product is removed?', 'It shifts to the right to replace the product.', ['It shifts to the left.', 'Kc increases.', 'It stops.'], 'Counteracts the change.'),
           ('What colour change is seen when N₂O₄ ⇌ 2NO₂ (ΔH +57 kJ) is heated?', 'the mixture becomes darker brown', ['the mixture becomes colourless', 'no change', 'the mixture turns blue'], 'Shifts right: more brown NO₂.')],
    why=[('Explain why a moderate temperature (about 450 °C) is used in the Haber process although a lower temperature gives a higher yield.', 'The forward reaction is exothermic, so low T increases yield, but the rate would be too slow; 450 °C is a compromise between acceptable yield and rate (with an iron catalyst).'),
         ('Explain the effect of increasing pressure on the yield of SO₃ in 2SO₂(g) + O₂(g) ⇌ 2SO₃(g).', 'Higher pressure favours the side with fewer gas molecules (3 → 2), so the position shifts right and the yield of SO₃ increases; in practice the yield is already high at about 1–2 atm.'),
         ('Explain why changing the concentration of a reactant does not change Kc.', 'The system responds by changing the other concentrations until the ratio in the equilibrium expression again equals Kc, which depends only on temperature.'),
         ('Explain why Le Chatelier’s principle predicts but does not explain shifts in equilibrium.', 'It describes the direction of the shift; the explanation lies in changes in the relative rates of the forward and reverse reactions (or Q versus K).')],
    contrast=[('the effect of temperature on equilibrium', 'the effect of pressure on equilibrium', 'Temperature changes both the position and the value of K; pressure changes only the position (for reactions with different numbers of gas moles), not K.'),
              ('the effect of a catalyst', 'the effect of increasing concentration', 'A catalyst speeds both reactions equally and does not shift equilibrium; increasing a reactant’s concentration shifts the position to the right.')],
    misc=[('Increasing the pressure always increases the yield of product.', 'Pressure favours the side with fewer gas moles; if products have more gas moles the yield falls, and if both sides are equal there is no effect.'),
          ('Adding more reactant increases the value of Kc.', 'Kc is unchanged; the position shifts right until the ratio returns to Kc.'),
          ('Increasing the temperature always shifts the equilibrium to the right.', 'Increasing temperature favours the endothermic direction, which may be either forward or reverse.')],
    apply=[('Predict the effect of decreasing the temperature on the yield of methanol in CO(g) + 2H₂(g) ⇌ CH₃OH(g), ΔH = −91 kJ mol⁻¹.', 'Yield increases: exothermic forward reaction favoured at lower T (Kc increases).', 2),
           ('State and explain the effect of adding a small amount of NaOH(aq) to 2CrO₄²⁻(aq) + 2H⁺(aq) ⇌ Cr₂O₇²⁻(aq) + H₂O(l).', 'OH⁻ removes H⁺; equilibrium shifts left; colour changes from orange to yellow.', 2)],
    evaluate=[('Le Chatelier’s principle is sufficient to choose the conditions for an industrial process.', ['predicts the direction of shifts with T, p and concentration', 'explains high pressure for Haber'], ['ignores rate, cost, safety and energy use', 'does not give quantitative yields (K needed)', 'compromise conditions are always required'], 'It is a useful qualitative guide, but rates, economics and K values decide the actual conditions.'),
              ('Removing the product continuously is the best way to increase the yield of an equilibrium reaction.', ['shifts the equilibrium right without changing K', 'used for NH₃ (liquefied) and esters (distilled off)'], ['not always physically possible', 'requires energy for separation', 'changing T, p or excess reagent can be cheaper'], 'Removing product is highly effective where separation is easy, but the best method depends on the system.')],
    extended=[('In the Contact process, 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH = −196 kJ mol⁻¹, conditions of about 450 °C, 2 atm and a V₂O₅ catalyst are used. (a) Predict the effect of increasing temperature on the yield and on Kc. (b) Explain why a higher pressure is not used. (c) Explain the role of V₂O₅. (d) Suggest why excess air is used.', '(a) yield and Kc decrease (exothermic). (b) conversion already ~99 % at low pressure; high pressure costly. (c) increases rate, equilibrium reached faster, no effect on yield. (d) increases [O₂], shifting the position right and using all the more valuable SO₂.', 8, 'multi_step')],
))


@R.add('ch04-st2', 'C3', (1, 4), 'mcq')
def c3_lc_shift(rng, slot):
    e = pick(rng, EQM)
    ch = pick(rng, ['increase T', 'decrease T', 'increase p', 'decrease p', 'add reactant', 'remove product', 'add product', 'catalyst'])
    if ch in ('increase p', 'decrease p') and not e[4]:
        return None
    pos, K = lc_answer(e, ch)
    txt = {'right': 'shifts to the right', 'left': 'shifts to the left', 'no shift': 'does not change'}
    right = f'The position {txt[pos]} and Kc {"is unchanged" if K == "no change" else K}.'
    opts = [f'The position {txt[p_]} and Kc {"is unchanged" if k_ == "no change" else k_}.' for p_ in ('right', 'left', 'no shift') for k_ in ('increases', 'decreases', 'no change')]
    wr = [o for o in opts if o != right]
    rng.shuffle(wr)
    stem = f'For {eqp(e[0])}, ΔH = {sgn(e[3], 4)} kJ mol⁻¹. What happens if {_ctext(e, ch)} at equilibrium?'
    why = {'increase T': 'Endothermic direction favoured', 'decrease T': 'Exothermic direction favoured', 'increase p': f'Fewer gas moles favoured (Δn = {dn_gas(e)})', 'decrease p': f'More gas moles favoured (Δn = {dn_gas(e)})',
           'add reactant': 'Shift to use up the added reactant', 'remove product': 'Shift to replace product', 'add product': 'Shift to use up added product', 'catalyst': 'Catalyst speeds both reactions equally'}[ch]
    return mcq(rng, stem, right, wr[:3], f'{why}; only temperature changes Kc.')


@R.add('ch04-st2', 'C3', (1, 5), 'short')
def c3_lc_explain(rng, slot):
    e = pick(rng, EQM)
    ch = pick(rng, ['increase T', 'decrease T', 'increase p', 'decrease p', 'add reactant', 'remove product'])
    if ch in ('increase p', 'decrease p') and not e[4]:
        return None
    pos, K = lc_answer(e, ch)
    stem = f'For {e[5]}, {eqp(e[0])}, ΔH = {sgn(e[3], 4)} kJ mol⁻¹, predict and explain the effect on the equilibrium yield of {chem(list(e[2])[0])} when {_ctext(e, ch)}.'
    eff = {'right': 'increases', 'left': 'decreases', 'no shift': 'is unchanged'}[pos]
    why = {'increase T': f'the {"endothermic forward" if e[3] > 0 else "endothermic reverse"} reaction is favoured', 'decrease T': f'the {"exothermic forward" if e[3] < 0 else "exothermic reverse"} reaction is favoured',
           'increase p': f'the side with fewer gas moles is favoured ({sum(e[1].values())} : {sum(e[2].values())})', 'decrease p': f'the side with more gas moles is favoured ({sum(e[1].values())} : {sum(e[2].values())})',
           'add reactant': 'the system uses up some of the added reactant', 'remove product': 'the system replaces the removed product'}[ch]
    return dict(stem=stem, answer=f'Yield {eff}: {why}.' + (f' Kc {K}.' if ch.endswith('T') else ''), markingKey=f'yield {eff} (1); {why} (1)' + (f'; Kc {K} (1).' if ch.endswith('T') else '.'), type='explain', marks=3 if ch.endswith('T') else 2)


@R.add('ch04-st2', 'C3', (2, 4), 'mcq')
def c3_conditions_pick(rng, slot):
    e = pick(rng, [x for x in GAS_EQM if dn_gas(x) != 0])
    hiT = e[3] > 0
    hip = dn_gas(e) < 0
    right = f'{"high" if hiT else "low"} temperature and {"high" if hip else "low"} pressure'
    wr = [f'{a} temperature and {b} pressure' for a in ('high', 'low') for b in ('high', 'low')]
    wr = [w for w in wr if w != right]
    stem = f'Which conditions give the highest equilibrium yield of {chem(list(e[2])[0])} in {eqp(e[0])}, ΔH = {sgn(e[3], 4)} kJ mol⁻¹?'
    return mcq(rng, stem, right, wr, f'{"Endothermic" if hiT else "Exothermic"} forward reaction → {"high" if hiT else "low"} T; gas moles {sum(e[1].values())} → {sum(e[2].values())} → {"high" if hip else "low"} p.')


R.mcqs('ch04-st2', 'C2', (1, 4), [
    ('Why does increasing the temperature of an exothermic equilibrium reduce the yield of product?', 'The endothermic (reverse) reaction is favoured to absorb the added heat.', ['The catalyst stops working.', 'The products decompose irreversibly.', 'Kc increases.'], 'Le Chatelier and K(T).'),
    ('Why does a change in pressure have no effect on H₂(g) + Cl₂(g) ⇌ 2HCl(g)?', 'There are equal numbers of gas moles on both sides.', ['The reaction is exothermic.', 'HCl is very soluble.', 'Chlorine is a gas.'], '2 = 2.'),
    ('In terms of rates, why does adding reactant shift an equilibrium to the right?', 'The forward rate increases temporarily until the rates are equal again.', ['The reverse rate increases.', 'Kc increases.', 'The activation energy decreases.'], 'Rates rebalance.'),
    ('Why is ammonia removed by condensing it in the Haber process?', 'Removing product shifts the equilibrium to the right, increasing conversion.', ['Ammonia poisons the catalyst.', 'It increases Kc.', 'It raises the pressure.'], 'Product removal.'),
])


# ---- ch04-st3 Q and ICE (HL) ----
R.facts('ch04-st3', F(
    terms=[('reaction quotient (Q)', 'the value of the equilibrium expression calculated using concentrations at any moment, not necessarily at equilibrium'),
           ('ICE table', 'a table of Initial, Change and Equilibrium amounts or concentrations used to calculate equilibrium compositions'),
           ('extent of reaction', 'how far a reaction has proceeded towards products, measured by the change in amount of a species'),
           ('approximation for small K', 'assuming that the change x is negligible compared with initial concentrations when K is very small')],
    facts=[('If Q < K, in which direction will the reaction proceed?', 'forward, to form more products', ['backward, to form more reactants', 'no net change', 'it cannot be predicted'], 'Q increases towards K.'),
           ('If Q > K, what happens?', 'The reverse reaction is favoured until Q = K.', ['The forward reaction is favoured.', 'The system is at equilibrium.', 'K increases.'], 'Too many products.'),
           ('At equilibrium, how are Q and K related?', 'Q = K', ['Q > K', 'Q < K', 'Q = 0'], 'Definition.'),
           ('In an ICE table, what does the "C" row show?', 'the change in concentration, related by the stoichiometric ratio', ['the concentration of the catalyst', 'the constant K', 'the concentration at completion'], 'Change ∝ coefficients.')],
    why=[('Explain how comparing Q with K predicts the direction of a reaction.', 'If Q < K the ratio of products to reactants is too low, so the forward reaction proceeds; if Q > K the reverse reaction proceeds; if Q = K the system is at equilibrium.'),
         ('Explain why the changes in an ICE table must follow the mole ratio of the equation.', 'The amounts of each species that react or form are fixed by stoichiometry: for aA + bB → cC the changes are −ax, −bx and +cx.'),
         ('Explain when it is reasonable to assume that x is negligible in an equilibrium calculation.', 'When K is very small (e.g. < 10⁻³) relative to the initial concentrations, so very little reacts and [A]₀ − x ≈ [A]₀; the result should be checked (x < 5 % of [A]₀).')],
    contrast=[('Q', 'K', 'Q uses the concentrations at any instant; K uses equilibrium concentrations only and is constant at a given temperature.'),
              ('initial concentrations', 'equilibrium concentrations', 'Initial concentrations are those before reaction; equilibrium concentrations are initial values adjusted by the changes (x) that occur as equilibrium is reached.')],
    misc=[('If Q is less than K, the reaction is at equilibrium.', 'Q < K means the system is not at equilibrium; the forward reaction proceeds until Q = K.'),
          ('In an ICE table the changes are always equal for every species.', 'The changes are in the ratio of the stoichiometric coefficients.')],
    apply=[('For N₂O₄ ⇌ 2NO₂ (Kc = 4.6 × 10⁻³), a mixture has [N₂O₄] = 0.10 and [NO₂] = 0.050 mol dm⁻³. Determine Q and the direction of reaction.', 'Q = 0.050²/0.10 = 0.025 > Kc → reverse reaction (more N₂O₄ forms)', 3)],
    evaluate=[('ICE-table calculations accurately predict real equilibrium mixtures.', ['based on the equilibrium law, which holds well for dilute solutions and ideal gases'], ['concentrations should be activities: deviations at high concentration', 'K values are temperature-specific and often approximate', 'approximations (small x) introduce error'], 'They give good estimates under ideal conditions but are approximations for concentrated or non-ideal systems.'),
              ('The reaction quotient is a more useful idea than Le Chatelier’s principle.', ['Q vs K gives a quantitative, unambiguous prediction', 'explains why concentration changes do not alter K'], ['Le Chatelier is quicker for qualitative predictions', 'Q does not directly treat temperature changes (K changes)'], 'Q gives the rigorous basis; Le Chatelier remains a convenient qualitative shortcut.')],
    extended=[('2.00 mol of H₂ and 2.00 mol of I₂ are heated in a 1.00 dm³ flask until equilibrium: H₂(g) + I₂(g) ⇌ 2HI(g), Kc = 49.0. (a) Construct an ICE table. (b) Calculate the equilibrium concentration of each species. (c) Calculate the percentage of H₂ converted. (d) Predict the effect of adding 1.00 mol of HI at equilibrium, using Q.', '(a) I: 2, 2, 0; C: −x, −x, +2x; E: 2 − x, 2 − x, 2x. (b) √49 = 7 = 2x/(2 − x) → x = 1.56: [H₂] = [I₂] = 0.444, [HI] = 3.11 mol dm⁻³. (c) 77.8 %. (d) Q rises above K → reverse reaction until Q = K.', 8, 'multi_step')],
))


@R.add('ch04-st3', 'C3', (1, 4), 'mcq')
def c3_q_direction(rng, slot):
    e = pick(rng, EQM)
    conc = {s: round(rng.uniform(0.05, 1.5), 2) for s in list(e[1]) + list(e[2])}
    Q = kc_val(e, conc)
    K = Q * rng.choice([0.1, 0.2, 0.5, 2, 5, 10, 50])
    vals = ', '.join(f'[{chem(s)}] = {conc[s]:.2f}' for s in conc)
    right = 'towards products (forward)' if Q < K else 'towards reactants (reverse)'
    wr = ['towards reactants (reverse)' if Q < K else 'towards products (forward)', 'no net reaction – the system is at equilibrium', 'it cannot be predicted without knowing ΔH']
    stem = f'For {eqp(e[0])}, Kc = {sf(K)}. A mixture contains {vals} mol dm⁻³. In which direction does the reaction proceed?'
    return mcq(rng, stem, right, wr, f'Q = {sf(Q)} {"<" if Q < K else ">"} Kc → {right}.')


@R.add('ch04-st3', 'C3', (2, 5), 'numerical')
def c3_ice_kc(rng, slot):
    e = pick(rng, EQM)
    r = list(e[1])
    init = {s: round(rng.uniform(0.5, 2.0), 2) for s in r}
    lim = min(init[s] / e[1][s] for s in r)
    x = round(lim * rng.uniform(0.2, 0.7), 3)
    eq_ = {s: init[s] - e[1][s] * x for s in r}
    eq_.update({s: e[2][s] * x for s in e[2]})
    known = list(e[2])[0]
    K = kc_val(e, eq_)
    V = rng.choice([1.00, 2.00, 0.500])
    ini_txt = ' and '.join(f'{sf(init[s] * V)} mol of {chem(s)}' for s in r)
    stem = (f'{ini_txt} were placed in a sealed {sf(V)} dm³ container. At equilibrium ({eqp(e[0])}) the mixture contained {sf(eq_[known] * V)} mol of {chem(known)}. '
            f'Calculate the equilibrium concentrations of all species and the value of Kc.')
    eqs = ', '.join(f'[{chem(s)}] = {sf(eq_[s])}' for s in eq_)
    return num(stem, f'{eqs}; Kc = {sf(K)}', f'Initial concentrations = n/{sf(V)} (M1); change from stoichiometry: x = {sf(x)} mol dm⁻³ (M1); equilibrium: {eqs} (A1); Kc = {sf(K)} (A1).', 4, 'multi_step')


@R.add('ch04-st3', 'C3', (2, 5), 'numerical')
def c3_ice_hi(rng, slot):
    K = rng.choice([25.0, 36.0, 46.0, 49.0, 54.0, 64.0, 81.0])
    a = rng.choice([0.100, 0.200, 0.400, 0.500, 1.00, 1.50])
    rt = math.sqrt(K)
    x = a * rt / (2 + rt)
    stem = pick(rng, [f'Equal initial concentrations of H₂ and I₂, each {sf(a)} mol dm⁻³, are heated: H₂(g) + I₂(g) ⇌ 2HI(g), Kc = {sf(K)}. Calculate the equilibrium concentration of HI.',
                      f'For H₂(g) + I₂(g) ⇌ 2HI(g), Kc = {sf(K)} at a high temperature. Starting with [H₂] = [I₂] = {sf(a)} mol dm⁻³ and no HI, determine [HI] at equilibrium.'])
    return num(stem, q(2 * x, 'mol dm⁻³'), f'Kc = (2x)²/({sf(a)} − x)² (M1); √{sf(K)} = 2x/({sf(a)} − x) (M1); x = {sf(x)}, [HI] = 2x = {q(2 * x, "mol dm⁻³")} (A1).', 3)


@R.add('ch04-st3', 'C3', (3, 5), 'numerical')
def c3_ice_small_k(rng, slot):
    K = rng.uniform(1.0, 9.0) * 10 ** rng.choice([-8, -7, -6, -5])
    a = rng.choice([0.100, 0.200, 0.500, 1.00])
    x = math.sqrt(K * a)
    stem = f'For A(g) ⇌ B(g) + C(g), Kc = {sf(K)} at 500 K. Starting with [A] = {sf(a)} mol dm⁻³, calculate [B] at equilibrium, stating the approximation used.'
    return num(stem, q(x, 'mol dm⁻³'), f'Kc = x²/({sf(a)} − x) ≈ x²/{sf(a)} because K is very small (M1); x = √({sf(K)} × {sf(a)}) (M1) = {q(x, "mol dm⁻³")} (A1).', 3)


R.mcqs('ch04-st3', 'C2', (1, 4), [
    ('A system has Q = K. What can be concluded?', 'The system is at equilibrium.', ['The reaction has gone to completion.', 'Only reactants are present.', 'The temperature must change.'], 'Q = K.'),
    ('Why does adding a reactant make Q less than K?', 'The denominator of the expression increases.', ['The numerator increases.', 'K increases.', 'The temperature falls.'], 'Q smaller.'),
    ('In an ICE table for N₂ + 3H₂ ⇌ 2NH₃, if N₂ changes by −x, what is the change for NH₃?', '+2x', ['+x', '−2x', '+3x'], 'Mole ratio 1 : 2.'),
    ('Why can equilibrium concentrations never be negative in an ICE calculation?', 'A species cannot react beyond the amount present, so x is limited by the reactant amounts.', ['K is always positive.', 'Concentrations are squared.', 'The volume is constant.'], 'Physical constraint.'),
])


# ---- ch04-st4 ΔG and K (HL) ----
R.facts('ch04-st4', F(
    terms=[('standard Gibbs energy change (ΔG⦵)', 'the Gibbs energy change for a reaction with all species in their standard states; related to K by ΔG⦵ = −RT ln K'),
           ('spontaneous reaction', 'a reaction that is thermodynamically favourable (ΔG < 0) under the stated conditions'),
           ('thermodynamic control', 'the extent of reaction determined by the relative stability (ΔG) of reactants and products rather than by rates')],
    facts=[('If ΔG⦵ is negative, what can be said about K?', 'K > 1', ['K < 1', 'K = 1', 'K = 0'], 'ΔG⦵ = −RT ln K.'),
           ('What is the value of ΔG⦵ when K = 1?', '0', ['1', '−RT', 'RT'], 'ln 1 = 0.'),
           ('Which equation links ΔG⦵ and the equilibrium constant?', 'ΔG⦵ = −RT ln K', ['ΔG⦵ = RT ln K', 'ΔG⦵ = −nFE⦵', 'ΔG⦵ = ΔH⦵ − TΔS⦵ only'], 'Data booklet.'),
           ('A reaction has a large positive ΔG⦵. What does this imply about its equilibrium mixture?', 'It contains mostly reactants.', ['It contains mostly products.', 'It reacts very slowly.', 'It is exothermic.'], 'K ≪ 1.')],
    why=[('Explain why a reaction with a negative ΔG⦵ may not occur at a noticeable rate.', 'ΔG⦵ shows that products are favoured at equilibrium, but says nothing about the activation energy; a high Ea makes the reaction very slow (kinetic stability).'),
         ('Explain why K changes with temperature in terms of ΔG⦵.', 'ΔG⦵ = ΔH⦵ − TΔS⦵ changes with T, and K = e^(−ΔG⦵/RT) depends on both ΔG⦵ and T, so K changes.'),
         ('Explain the significance of the sign of ΔG⦵ for the position of equilibrium.', 'ΔG⦵ < 0 gives K > 1 (products favoured); ΔG⦵ > 0 gives K < 1 (reactants favoured); ΔG⦵ = 0 gives K = 1.')],
    contrast=[('ΔG', 'ΔG⦵', 'ΔG applies to the actual conditions (and is zero at equilibrium); ΔG⦵ refers to standard states and fixes the value of K.'),
              ('thermodynamic stability', 'kinetic stability', 'Thermodynamic stability depends on ΔG (relative energies of reactants and products); kinetic stability depends on Ea (how fast change occurs).')],
    misc=[('If ΔG⦵ is negative, the reaction goes to completion.', 'A negative ΔG⦵ means K > 1, so products predominate, but some reactants remain unless K is extremely large.'),
          ('ΔG⦵ = 0 means the reaction does not occur.', 'ΔG⦵ = 0 means K = 1; both reactants and products are present in comparable amounts at equilibrium.')],
    apply=[('Calculate K at 298 K for a reaction with ΔG⦵ = −10.0 kJ mol⁻¹.', 'ln K = 10 000/(8.31 × 298) = 4.04; K = 56.6', 2)],
    evaluate=[('ΔG⦵ is the most important quantity for deciding whether an industrial reaction is worth carrying out.', ['determines the maximum yield (K)', 'shows whether the process is thermodynamically feasible'], ['rates (Ea, catalysts) decide practicality', 'costs, safety and environmental factors matter', 'conditions can be changed to overcome unfavourable K (removing product)'], 'ΔG⦵ establishes feasibility, but kinetics and economics decide whether a process is viable.'),
              ('A negative ΔG⦵ guarantees that a reaction will be observed.', ['negative ΔG⦵ means products are favoured at equilibrium'], ['high activation energy may make it imperceptibly slow (diamond → graphite)', 'non-standard conditions change ΔG'], 'ΔG⦵ shows feasibility only; whether reaction is observed depends on kinetics and conditions.')],
    extended=[('For N₂(g) + 3H₂(g) ⇌ 2NH₃(g), ΔH⦵ = −92.2 kJ mol⁻¹ and ΔS⦵ = −199 J K⁻¹ mol⁻¹. (a) Calculate ΔG⦵ at 298 K and at 700 K. (b) Calculate K at each temperature. (c) Explain why the Haber process is run at about 700 K despite the value of K.', '(a) −32.9 kJ mol⁻¹; +47.1 kJ mol⁻¹. (b) 5.8 × 10⁵; 3.0 × 10⁻⁴. (c) rate at 298 K is far too slow; higher T with catalyst and high pressure and NH₃ removal gives an acceptable rate and yield.', 8, 'multi_step')],
))


@R.add('ch04-st4', 'C3', (2, 5), 'numerical')
def c3_k_from_dg(rng, slot):
    dg = rng.choice([-1, 1]) * rng.uniform(2, 60)
    dg = round(dg, 1)
    T = rng.choice([298, 350, 400, 500, 700, 1000])
    K = math.exp(-dg * 1000 / (RGAS * T))
    e = pick(rng, EQM)
    stem = pick(rng, [f'For {eqp(e[0])}, ΔG⦵ = {sgn(dg, 3)} kJ mol⁻¹ at {T} K. Calculate the equilibrium constant at this temperature.',
                      f'A reaction has a standard Gibbs energy change of {sgn(dg, 3)} kJ mol⁻¹ at {T} K. Determine K and state whether reactants or products predominate at equilibrium.'])
    return num(stem, sf(K), f'ln K = −ΔG⦵/RT = −({sgn(dg * 1000, 3)})/(8.31 × {T}) = {sf(-dg * 1000 / (RGAS * T))} (M1, J conversion); K = {sf(K)} (A1); {"products" if K > 1 else "reactants"} predominate (R1).', 3)


@R.add('ch04-st4', 'C3', (2, 5), 'numerical')
def c3_dg_from_k(rng, slot):
    K = rng.uniform(1.0, 9.9) * 10 ** rng.choice([-10, -6, -3, -1, 1, 2, 4, 8])
    T = rng.choice([298, 373, 450, 600, 800])
    dg = -RGAS * T * math.log(K) / 1000
    stem = f'The equilibrium constant for a reaction is {sf(K)} at {T} K. Calculate ΔG⦵ in kJ mol⁻¹.'
    return num(stem, sgn(dg, 3, 'kJ mol⁻¹'), f'ΔG⦵ = −RT ln K = −8.31 × {T} × ln({sf(K)}) (M1) = {sgn(dg * 1000, 3)} J mol⁻¹ = {sgn(dg, 3, "kJ mol⁻¹")} (A1).', 2)


@R.add('ch04-st4', 'C3', (1, 4), 'mcq')
def c3_dg_sign(rng, slot):
    K = rng.uniform(1.1, 9.9) * 10 ** rng.choice([-9, -5, -2, -1, 1, 2, 5, 9])
    T = rng.choice([298, 400, 500, 750])
    right = 'negative' if K > 1 else 'positive'
    stem = f'At {T} K the equilibrium constant of a reaction is {sf(K)}. What is the sign of ΔG⦵ and which species predominate at equilibrium?'
    opts = {('negative', 'products'), ('positive', 'reactants'), ('negative', 'reactants'), ('positive', 'products')}
    r = (right, 'products' if K > 1 else 'reactants')
    return mcq(rng, stem, f'ΔG⦵ is {r[0]}; {r[1]} predominate', [f'ΔG⦵ is {a}; {b} predominate' for a, b in opts if (a, b) != r], f'K {">" if K > 1 else "<"} 1 → ln K {">" if K > 1 else "<"} 0 → ΔG⦵ {r[0]}.')


@R.add('ch04-st4', 'C3', (2, 5), 'numerical')
def c3_k_from_dh_ds(rng, slot):
    dh = rng.choice([-1, 1]) * rng.randint(20, 200)
    ds = rng.choice([-1, 1]) * rng.randint(20, 250)
    T = rng.choice([298, 400, 500, 600, 800, 1000])
    dg = dh - T * ds / 1000
    if abs(dg) > 80:
        return None
    K = math.exp(-dg * 1000 / (RGAS * T))
    stem = f'For a reaction, ΔH⦵ = {sgn(dh, 4)} kJ mol⁻¹ and ΔS⦵ = {sgn(ds, 4)} J K⁻¹ mol⁻¹. Calculate ΔG⦵ and K at {T} K.'
    return num(stem, f'ΔG⦵ = {sgn(dg, 3, "kJ mol⁻¹")}; K = {sf(K)}', f'ΔG⦵ = ΔH⦵ − TΔS⦵ = {sgn(dh, 4)} − {T} × ({sgn(ds / 1000, 3)}) = {sgn(dg, 3)} kJ mol⁻¹ (M1 A1); K = e^(−ΔG⦵/RT) = {sf(K)} (A1).', 3)


R.mcqs('ch04-st4', 'C2', (1, 4), [
    ('Why is ΔG zero for a system at equilibrium?', 'There is no further tendency for net change in either direction.', ['No reactions are occurring.', 'ΔH and ΔS are both zero.', 'K is zero.'], 'Equilibrium = minimum G.'),
    ('Why must ΔG⦵ be converted to J mol⁻¹ before using ΔG⦵ = −RT ln K?', 'R is in J K⁻¹ mol⁻¹.', ['K has units of kJ.', 'T is in kJ.', 'ln K must be negative.'], 'Consistent units.'),
    ('A reaction has ΔG⦵ = +5 kJ mol⁻¹ at 298 K. Which statement is correct?', 'K is slightly less than 1; noticeable amounts of products form.', ['No products form.', 'The reaction goes to completion.', 'K is very large.'], 'K ≈ 0.13.'),
    ('Why does a large negative ΔG⦵ not guarantee a fast reaction?', 'ΔG⦵ is unrelated to the activation energy.', ['Fast reactions have positive ΔG⦵.', 'ΔG⦵ depends on catalyst.', 'K decreases with rate.'], 'Thermodynamics vs kinetics.'),
])


ESTERS = [('ethanoic acid', 'ethanol', 'ethyl ethanoate', 'CH₃COOH(l) + C₂H₅OH(l) ⇌ CH₃COOC₂H₅(l) + H₂O(l)'),
          ('propanoic acid', 'methanol', 'methyl propanoate', 'C₂H₅COOH(l) + CH₃OH(l) ⇌ C₂H₅COOCH₃(l) + H₂O(l)'),
          ('methanoic acid', 'propan-1-ol', 'propyl methanoate', 'HCOOH(l) + C₃H₇OH(l) ⇌ HCOOC₃H₇(l) + H₂O(l)'),
          ('ethanoic acid', 'butan-1-ol', 'butyl ethanoate', 'CH₃COOH(l) + C₄H₉OH(l) ⇌ CH₃COOC₄H₉(l) + H₂O(l)')]


def p1b_ester_eq(rng, slot):
    acid, alc, est, eqn = pick(rng, ESTERS)
    a0 = round(rng.uniform(0.150, 0.250), 3)
    b0 = round(rng.uniform(0.150, 0.250), 3)
    K = rng.uniform(3.0, 5.0)
    # solve K = x^2/((a-x)(b-x))
    A = 1 - K
    B = K * (a0 + b0)
    C = -K * a0 * b0
    x = (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A) if A != 0 else -C / B
    if not (0 < x < min(a0, b0)):
        x = (-B - math.sqrt(B * B - 4 * A * C)) / (2 * A)
    left = a0 - x
    cb = pick(rng, [0.500, 0.400, 0.250])
    vt = round(left / cb * 1000 / 10, 2)  # titre for a 1/10 aliquot
    if not 10 < vt < 50:
        return None
    n_left = cb * vt / 1000 * 10
    xc = a0 - n_left
    Kc = xc ** 2 / ((a0 - xc) * (b0 - xc))
    days = pick(rng, ['a week', 'ten days', 'two weeks'])
    intro = (f'A student mixed {a0:.3f} mol of {acid}, {b0:.3f} mol of {alc} and a few drops of concentrated sulfuric acid in a sealed tube and left it for {days} at 298 K. '
             f'The mixture was quickly made up to 250.0 cm³ with ice-cold water (to stop further reaction), and 25.00 cm³ portions were immediately titrated with {cb:.3f} mol dm⁻³ NaOH. After allowing for the sulfuric acid, the mean titre due to {acid} was {vt:.2f} cm³.\n'
             f'{eqn}')
    parts = [
        (f'Calculate the amount of {acid} remaining at equilibrium.', f'{sf(n_left)} mol', f'n(NaOH) = {cb} × {vt / 1000:.5f} × 10 (M1) = {sf(n_left)} mol (A1).', 2),
        (f'Determine the equilibrium amounts of {alc}, {est} and water.', f'{alc} {sf(b0 - xc)} mol; ester and water {sf(xc)} mol each', f'x = {a0:.3f} − {sf(n_left)} = {sf(xc)} mol (M1); {alc} {sf(b0 - xc)} mol, ester = water = {sf(xc)} mol (A1).', 2),
        ('Calculate Kc for the reaction.', sf(Kc), f'Volume cancels; Kc = ({sf(xc)})²/({sf(n_left)} × {sf(b0 - xc)}) (M1) = {sf(Kc)} (A1).', 2)]
    tail = [('Explain why the volume of the mixture does not need to be known to calculate Kc.', 'There are equal numbers of moles on each side, so the volume terms cancel in the expression.', 'Equal powers on top and bottom; V cancels (1).', 1),
            ('State the role of the sulfuric acid.', 'catalyst – speeds up attainment of equilibrium', 'Catalyst (1).', 1),
            ('Explain why ice-cold water was used.', 'Cooling and dilution slow the reaction so the equilibrium composition is not changed before titration.', 'rate reduced / composition frozen (1).', 1),
            (f'Predict the effect on the yield of {est} of adding more {alc}.', f'The yield increases: equilibrium shifts right to use up the added {alc}.', 'shift right (1).', 1)]
    rng.shuffle(tail)
    return dict(intro=intro, parts=parts + tail[:2], extras=tail[2:])


p1b(R, 'ch04-st3')(p1b_ester_eq)


@p1b(R, 'ch04-st2')
def p1b_n2o4_temp(rng, slot):
    sysm = pick(rng, ['N2O4', 'HI'])
    who = name(rng)
    if sysm == 'N2O4':
        dH, Kref, Tref = 57.2, 4.6e-3, 298
        Ts = sorted(rng.sample([273, 298, 323, 348, 373, 398], 4))
        eq = 'N₂O₄(g) ⇌ 2NO₂(g)'
        intro0 = f'{who} studied the dissociation of colourless dinitrogen tetroxide into brown nitrogen dioxide: {eq}. Values of Kc were measured at several temperatures.'
        unit = ' / mol dm⁻³'
    else:
        dH, Kref, Tref = -9.4, 54.3, 698
        Ts = sorted(rng.sample([500, 600, 650, 698, 750, 800], 4))
        eq = 'H₂(g) + I₂(g) ⇌ 2HI(g)'
        intro0 = f'{who} studied the equilibrium between hydrogen, violet iodine vapour and colourless hydrogen iodide: {eq}. Values of Kc were measured at several temperatures.'
        unit = ''
    Ks = [Kref * math.exp(-dH * 1000 / RGAS * (1 / T - 1 / Tref)) for T in Ts]
    Tq = Ts[rng.randrange(4)]
    Kq = Ks[Ts.index(Tq)]
    tab = '\n'.join(f'{T} | {sf(K)}' for T, K in zip(Ts, Ks))
    intro = intro0 + f'\n\nT / K | Kc{unit}\n{tab}'
    if sysm == 'N2O4':
        c2 = rsf(rng.uniform(0.020, 0.200), 2)
        x = math.sqrt(Kq * c2)
        parts = [('Write the expression for Kc.', 'Kc = [NO₂]²/[N₂O₄]', 'correct expression (1).', 1),
                 ('Deduce, with a reason, the sign of ΔH for the forward reaction.', 'positive (endothermic): Kc increases with temperature, so the forward reaction is favoured by heating.', 'positive (1); Kc rises with T (1).', 2),
                 (f'At {Tq} K the equilibrium concentration of N₂O₄ is {sf(c2, 2)} mol dm⁻³. Calculate the equilibrium concentration of NO₂.', q(x, 'mol dm⁻³', 2),
                  f'[NO₂] = √(Kc × [N₂O₄]) = √({sf(Kq)} × {sf(c2, 2)}) (M1) = {q(x, "mol dm⁻³", 2)} (A1).', 2)]
        pool = [('Predict and explain the colour change when the volume of the container is halved at constant temperature.', 'Initially darker (concentration doubles), then becomes paler as equilibrium shifts left towards fewer gas molecules; Kc unchanged.', 'shift left – fewer moles of gas (1); immediate darkening then partial fading (1).', 2),
                ('Explain why Kc has units of mol dm⁻³ for this reaction.', 'There is one more concentration term in the numerator than the denominator: (mol dm⁻³)²/(mol dm⁻³).', 'unit analysis (1).', 1),
                ('Predict the colour change when the equilibrium mixture is placed in ice water.', 'It becomes paler: the exothermic reverse reaction is favoured, forming colourless N₂O₄.', 'paler (1); shift left (1).', 2)]
    else:
        c2 = rsf(rng.uniform(0.0010, 0.0050), 2)
        x = math.sqrt(Kq) * c2
        parts = [('Write the expression for Kc.', 'Kc = [HI]²/([H₂][I₂])', 'correct expression (1).', 1),
                 ('Deduce, with a reason, the sign of ΔH for the forward reaction.', 'negative (exothermic): Kc decreases as temperature increases, so the reverse reaction is favoured by heating.', 'negative (1); Kc falls with T (1).', 2),
                 (f'At {Tq} K the equilibrium concentrations of H₂ and I₂ are both {sf(c2, 2)} mol dm⁻³. Calculate the equilibrium concentration of HI.', q(x, 'mol dm⁻³', 2),
                  f'[HI] = √(Kc × [H₂][I₂]) = √({sf(Kq)}) × {sf(c2, 2)} (M1) = {q(x, "mol dm⁻³", 2)} (A1).', 2)]
        pool = [('Predict the effect of doubling the total pressure on the position of equilibrium.', 'No effect: there are equal numbers of gas molecules on each side.', 'no shift (1); 2 mol gas on each side (1).', 2),
                ('Explain why Kc has no units for this reaction.', 'The concentration terms cancel: (mol dm⁻³)²/(mol dm⁻³)².', 'unit analysis (1).', 1),
                ('Predict what is observed when the mixture is heated at constant volume.', 'The violet colour deepens: the endothermic reverse reaction is favoured, forming more I₂.', 'darker violet (1); shift left (1).', 2)]
    pool.append(('State the effect of a catalyst on the value of Kc.', 'No effect – a catalyst speeds up forward and reverse reactions equally.', 'no change (1).', 1))
    pool.append((f'Calculate ΔG⦵ at {Tq} K from the value of Kc.', sgn(-RGAS * Tq * math.log(Kq) / 1000, 3, 'kJ mol⁻¹'), f'ΔG⦵ = −RT ln K = −8.31 × {Tq} × ln({sf(Kq)}) (M1) = {sgn(-RGAS * Tq * math.log(Kq) / 1000, 3, "kJ mol⁻¹")} (A1).', 2))
    rng.shuffle(pool)
    return dict(intro=intro, parts=parts + pool[:2], extras=pool[2:])


# =============================================================================================
# ch05 R3.1 Proton transfer reactions: acids and bases
# =============================================================================================
PAIRS = [('HCl', 'Cl^-'), ('HNO3', 'NO3^-'), ('H2SO4', 'HSO4^-'), ('HSO4^-', 'SO4^2-'), ('H3O^+', 'H2O'), ('H2O', 'OH^-'), ('NH4^+', 'NH3'),
         ('CH3COOH', 'CH3COO^-'), ('H2CO3', 'HCO3^-'), ('HCO3^-', 'CO3^2-'), ('H2PO4^-', 'HPO4^2-'), ('HPO4^2-', 'PO4^3-'), ('HF', 'F^-'),
         ('HCN', 'CN^-'), ('CH3NH3^+', 'CH3NH2'), ('H2S', 'HS^-'), ('HCOOH', 'HCOO^-'), ('NH3', 'NH2^-')]
CONJ_B = {a: b for a, b in PAIRS}
CONJ_A = {b: a for a, b in PAIRS}
AMPHI = ['H2O', 'HCO3^-', 'HSO4^-', 'H2PO4^-', 'HPO4^2-', 'HS^-', 'NH3']
STRONG_A = [('hydrochloric acid', 'HCl', 1), ('nitric acid', 'HNO3', 1), ('hydrobromic acid', 'HBr', 1)]
STRONG_B = [('sodium hydroxide', 'NaOH', 1), ('potassium hydroxide', 'KOH', 1), ('barium hydroxide', 'Ba(OH)2', 2), ('lithium hydroxide', 'LiOH', 1)]
KW_T = [(0, 0.114e-14), (10, 0.293e-14), (25, 1.00e-14), (40, 2.92e-14), (50, 5.48e-14), (60, 9.61e-14)]


def bl_reaction(rng):
    for _ in range(30):
        ha, a_ = pick(rng, PAIRS)
        b, bh = pick(rng, [(v, k) for k, v in PAIRS])
        if b in (ha, a_) or bh in (ha, a_):
            continue
        return ha, b, a_, bh
    return None


def ph(x):
    return f'{-math.log10(x):.2f}'


R.facts('ch05-st1', F(
    terms=[('Brønsted–Lowry acid', 'a proton (H⁺) donor'),
           ('Brønsted–Lowry base', 'a proton (H⁺) acceptor'),
           ('conjugate acid–base pair', 'two species that differ by one proton, e.g. NH₄⁺/NH₃'),
           ('amphiprotic', 'able to act as both a Brønsted–Lowry acid and a Brønsted–Lowry base, e.g. H₂O or HCO₃⁻'),
           ('amphoteric', 'able to react as both an acid and a base (a broader term than amphiprotic, e.g. Al₂O₃)'),
           ('oxonium ion', 'the H₃O⁺ ion, formed when a proton bonds to a water molecule')],
    facts=[('What is the conjugate base of H₂SO₄?', 'HSO₄⁻', ['SO₄²⁻', 'H₃SO₄⁺', 'H₂O'], 'Remove one H⁺.'),
           ('What is the conjugate acid of NH₃?', 'NH₄⁺', ['NH₂⁻', 'H₃O⁺', 'N₂H₄'], 'Add one H⁺.'),
           ('Which species is amphiprotic?', 'HCO₃⁻', ['CO₃²⁻', 'Cl⁻', 'NH₄⁺'], 'Can donate or accept H⁺.'),
           ('In NH₃ + H₂O ⇌ NH₄⁺ + OH⁻, which species acts as a Brønsted–Lowry acid?', 'H₂O', ['NH₃', 'NH₄⁺ only', 'OH⁻'], 'Water donates H⁺ to NH₃.'),
           ('Which feature must a Brønsted–Lowry base have?', 'a lone pair of electrons to accept a proton', ['a hydrogen atom', 'a positive charge', 'an OH group'], 'Lone pair bonds to H⁺.'),
           ('A typical acid reacts with a metal carbonate to give', 'a salt, water and carbon dioxide', ['a salt and hydrogen', 'a salt only', 'a base and water'], 'e.g. CaCO₃ + 2HCl.')],
    why=[('Explain why water is described as amphiprotic.', 'Water can donate a proton (to bases such as NH₃, forming OH⁻) and accept a proton (from acids such as HCl, forming H₃O⁺).'),
         ('Explain why H₃O⁺ is used to represent H⁺ in aqueous solution.', 'A bare proton cannot exist alone in water; it bonds to a lone pair on a water molecule, forming the oxonium ion.'),
         ('Explain why every Brønsted–Lowry acid–base reaction involves two conjugate pairs.', 'When an acid donates a proton it becomes its conjugate base, and the base that accepts it becomes its conjugate acid, so two pairs are always present.'),
         ('Explain why the Brønsted–Lowry theory is more general than the Arrhenius theory of acids and bases.', 'It does not require water or OH⁻: any proton transfer counts, so bases such as NH₃ and reactions in other solvents or in the gas phase are included.')],
    contrast=[('a Brønsted–Lowry acid', 'a Brønsted–Lowry base', 'An acid donates a proton; a base accepts a proton using a lone pair.'),
              ('amphiprotic', 'amphoteric', 'Amphiprotic species donate or accept protons (Brønsted–Lowry); amphoteric substances react with both acids and bases by any mechanism.'),
              ('an acid', 'its conjugate base', 'The conjugate base has one fewer H⁺ (and a charge one unit more negative) than the acid.')],
    misc=[('The conjugate base of HCl is OH⁻.', 'The conjugate base is formed by removing one proton: Cl⁻.'),
          ('A base must contain hydroxide ions.', 'A Brønsted–Lowry base is any proton acceptor, e.g. NH₃, CO₃²⁻ or CH₃NH₂.'),
          ('NH₄⁺ is a base because it contains nitrogen.', 'NH₄⁺ has no lone pair and can donate a proton: it is an acid (conjugate acid of NH₃).')],
    apply=[('Identify the two conjugate acid–base pairs in HCO₃⁻ + OH⁻ ⇌ CO₃²⁻ + H₂O.', 'HCO₃⁻/CO₃²⁻ and H₂O/OH⁻', 2),
           ('Write equations to show HSO₄⁻ acting as an acid with water and as a base with H₃O⁺.', 'HSO₄⁻ + H₂O ⇌ SO₄²⁻ + H₃O⁺; HSO₄⁻ + H₃O⁺ ⇌ H₂SO₄ + H₂O', 2)],
    evaluate=[('The Brønsted–Lowry model is the most useful definition of acids and bases.', ['explains reactions without water and the role of NH₃', 'introduces conjugate pairs and relative strengths'], ['does not cover acids without protons (BF₃, AlCl₃) – Lewis theory does', 'Arrhenius model is simpler for many aqueous reactions'], 'It is the most useful for proton-transfer chemistry, but Lewis theory is needed for a complete picture.'),
              ('Water is the most important amphiprotic substance in chemistry.', ['solvent for most acid–base reactions; autoionisation sets the pH scale', 'acts as acid or base depending on partner'], ['many other amphiprotic species are biologically vital (HCO₃⁻ buffer, H₂PO₄⁻, amino acids)', 'non-aqueous solvents also show proton transfer'], 'Water is uniquely important as the solvent, but other amphiprotic species are equally important in specific systems.')],
    extended=[('Hydrogencarbonate ions are important in blood. (a) Write equations to show that HCO₃⁻ is amphiprotic. (b) Identify the conjugate pairs in each equation. (c) Explain how HCO₃⁻ helps to keep blood pH roughly constant when acid enters the blood. (d) State the conjugate base of H₂CO₃ and of HCO₃⁻.', '(a) HCO₃⁻ + H₂O ⇌ CO₃²⁻ + H₃O⁺; HCO₃⁻ + H₃O⁺ ⇌ H₂CO₃ + H₂O. (b) HCO₃⁻/CO₃²⁻ & H₃O⁺/H₂O; H₃O⁺/H₂O & H₂CO₃/HCO₃⁻. (c) HCO₃⁻ accepts H⁺ to form H₂CO₃ (→ CO₂ + H₂O, exhaled), removing added acid. (d) HCO₃⁻; CO₃²⁻.', 7, 'multi_step')],
))


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def c3_conj(rng, slot):
    if rng.random() < 0.5:
        a, b = pick(rng, PAIRS)
        others = [chem(x) for x in set(CONJ_B) | set(CONJ_A) if x not in (a, b)]
        rng.shuffle(others)
        stem = f'What is the conjugate base of {chem(a)}?'
        return mcq(rng, stem, chem(b), others[:3], f'Remove one H⁺ from {chem(a)}: {chem(b)}.')
    a, b = pick(rng, PAIRS)
    others = [chem(x) for x in set(CONJ_B) | set(CONJ_A) if x not in (a, b)]
    rng.shuffle(others)
    stem = f'What is the conjugate acid of {chem(b)}?'
    return mcq(rng, stem, chem(a), others[:3], f'Add one H⁺ to {chem(b)}: {chem(a)}.')


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def c3_bl_roles(rng, slot):
    r = bl_reaction(rng)
    if r is None:
        return None
    ha, b, a_, bh = r
    eq = f'{chem(ha)} + {chem(b)} ⇌ {chem(a_)} + {chem(bh)}'
    kind = rng.choice(['acid', 'base', 'pairs'])
    if kind == 'pairs':
        right = f'{chem(ha)}/{chem(a_)} and {chem(bh)}/{chem(b)}'
        wr = [f'{chem(ha)}/{chem(b)} and {chem(a_)}/{chem(bh)}', f'{chem(ha)}/{chem(bh)} and {chem(b)}/{chem(a_)}', f'{chem(b)}/{chem(a_)} and {chem(ha)}/{chem(bh)}']
        stem = f'Which are the two conjugate acid–base pairs (acid/base) in {eq}?'
        return mcq(rng, stem, right, wr, f'{chem(ha)} donates H⁺ → {chem(a_)}; {chem(b)} accepts H⁺ → {chem(bh)}.')
    right = chem(ha) if kind == 'acid' else chem(b)
    wr = [chem(x) for x in (ha, b, a_, bh) if chem(x) != right]
    stem = f'Which species acts as a Brønsted–Lowry {kind} in the forward reaction {eq}?'
    return mcq(rng, stem, right, wr, f'{chem(ha)} donates a proton to {chem(b)}.')


@R.add('ch05-st1', 'C3', (1, 5), 'short')
def c3_bl_short(rng, slot):
    r = bl_reaction(rng)
    if r is None:
        return None
    ha, b, a_, bh = r
    eq = f'{chem(ha)} + {chem(b)} ⇌ {chem(a_)} + {chem(bh)}'
    stem = pick(rng, [f'Identify the Brønsted–Lowry acid and base on each side of the equilibrium {eq}.', f'For {eq}, state the two conjugate acid–base pairs.'])
    return dict(stem=stem, answer=f'acids: {chem(ha)} and {chem(bh)}; bases: {chem(b)} and {chem(a_)}; pairs {chem(ha)}/{chem(a_)}, {chem(bh)}/{chem(b)}',
                markingKey=f'{chem(ha)}/{chem(a_)} (1); {chem(bh)}/{chem(b)} (1).', type='short', marks=2)


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def c3_amphi(rng, slot):
    right = pick(rng, AMPHI)
    nonam = ['Cl^-', 'NO3^-', 'NH4^+', 'CO3^2-', 'SO4^2-', 'PO4^3-', 'H3O^+', 'CH3COO^-', 'F^-']
    wr = rng.sample(nonam, 3)
    stem = f'Which of {_lst(chem(x) for x in sorted([right] + wr))} is amphiprotic?'
    return mcq(rng, stem, chem(right), [chem(w) for w in wr], f'{chem(right)} can both donate a proton (→ {chem(CONJ_B.get(right, "?"))}) and accept one (→ {chem(CONJ_A.get(right, "?"))}).')


R.mcqs('ch05-st1', 'C2', (1, 4), [
    ('Why can CH₃NH₂ act as a Brønsted–Lowry base?', 'The nitrogen atom has a lone pair that can accept a proton.', ['It contains hydrogen atoms.', 'It releases OH⁻ ions directly.', 'It is a gas.'], 'Lone pair on N.'),
    ('Why does the conjugate base of a strong acid have negligible basic strength?', 'The acid fully donates its proton, so the conjugate base has almost no tendency to accept one back.', ['It has no lone pairs.', 'It is always neutral.', 'It is a strong base.'], 'Inverse strength relationship.'),
    ('In HNO₃ + H₂SO₄ ⇌ H₂NO₃⁺ + HSO₄⁻, how does nitric acid behave?', 'as a base', ['as an acid', 'as an oxidising agent only', 'as a catalyst'], 'Accepts H⁺ from H₂SO₄.'),
    ('Which pair is NOT a conjugate acid–base pair?', 'H₃O⁺ and OH⁻', ['NH₄⁺ and NH₃', 'H₂O and OH⁻', 'HCO₃⁻ and CO₃²⁻'], 'Differ by two protons.'),
])


# ---- ch05-st2 pH and Kw ----
R.facts('ch05-st2', F(
    terms=[('pH', 'the negative logarithm to base 10 of the hydrogen ion concentration: pH = −log₁₀[H⁺]'),
           ('ionic product of water (Kw)', 'Kw = [H⁺][OH⁻] = 1.00 × 10⁻¹⁴ at 298 K'),
           ('pOH', 'the negative logarithm of the hydroxide ion concentration; pH + pOH = 14.00 at 298 K'),
           ('neutral solution', 'a solution in which [H⁺] = [OH⁻]; pH 7.00 only at 298 K'),
           ('autoionisation of water', 'the reaction H₂O(l) ⇌ H⁺(aq) + OH⁻(aq) (or 2H₂O ⇌ H₃O⁺ + OH⁻)')],
    facts=[('By what factor does [H⁺] change when the pH falls by 2 units?', 'increases 100 times', ['increases 2 times', 'decreases 100 times', 'increases 20 times'], 'Log scale.'),
           ('What is [OH⁻] in a solution of pH 3.00 at 298 K?', '1.0 × 10⁻¹¹ mol dm⁻³', ['1.0 × 10⁻³ mol dm⁻³', '3.0 mol dm⁻³', '1.0 × 10⁻⁷ mol dm⁻³'], 'Kw/[H⁺].'),
           ('The autoionisation of water is endothermic. What happens to the pH of pure water as it is heated?', 'it decreases but the water stays neutral', ['it increases', 'it stays at 7.00', 'it decreases and the water becomes acidic'], 'Kw increases.'),
           ('What is the pH of 0.0100 mol dm⁻³ HCl?', '2.00', ['1.00', '0.0100', '12.00'], 'pH = −log 0.0100.'),
           ('Which is true for all aqueous solutions at 298 K?', '[H⁺][OH⁻] = 1.00 × 10⁻¹⁴', ['[H⁺] = [OH⁻]', 'pH > 7', '[H⁺] + [OH⁻] = 14'], 'Kw.'),
           ('What happens to the pH of an acid when it is diluted tenfold?', 'it increases by 1 (strong acid)', ['it decreases by 1', 'it increases by 10', 'it does not change'], '[H⁺] ÷ 10.')],
    why=[('Explain why pure water at 50 °C has a pH below 7 but is still neutral.', 'Autoionisation is endothermic, so Kw is larger at 50 °C and [H⁺] > 10⁻⁷ mol dm⁻³; but [H⁺] = [OH⁻], so the water is neutral.'),
         ('Explain why a logarithmic scale is used for hydrogen ion concentration.', '[H⁺] varies over many orders of magnitude (from ~1 to 10⁻¹⁴ mol dm⁻³); a log scale compresses this into convenient numbers (0–14).'),
         ('Explain why a tenfold dilution of a strong acid raises the pH by one unit.', 'The strong acid is fully dissociated, so [H⁺] falls by a factor of 10, and −log of a value ten times smaller is one unit greater.')],
    contrast=[('pH', 'pOH', 'pH = −log[H⁺]; pOH = −log[OH⁻]; at 298 K they add up to 14.00.'),
              ('an acidic solution', 'a neutral solution', 'In an acidic solution [H⁺] > [OH⁻]; in a neutral solution they are equal (pH 7.00 only at 298 K).')],
    misc=[('A solution of pH 2 is twice as acidic as a solution of pH 4.', 'pH is logarithmic: pH 2 has [H⁺] 100 times greater than pH 4.'),
          ('Pure water always has pH 7.', 'Only at 298 K; Kw changes with temperature, so neutral pH changes too.'),
          ('Diluting an alkali lowers its pH below 7.', 'Dilution brings the pH of an alkali closer to 7 but never below it.')],
    apply=[('Calculate the pH of 0.0250 mol dm⁻³ NaOH at 298 K.', '[OH⁻] = 0.0250; pOH = 1.60; pH = 12.40', 2),
           ('Calculate [H⁺] in a solution of pH 4.70.', '10⁻⁴·⁷⁰ = 2.0 × 10⁻⁵ mol dm⁻³', 1)],
    evaluate=[('The pH scale is an adequate measure of acidity for all purposes.', ['simple, widely understood, easily measured with meters and indicators', 'compresses a huge range'], ['pH is temperature dependent (neutral point varies)', 'does not distinguish strong/weak acids or show acid amount (buffering capacity)', 'breaks down for very concentrated acids (negative pH)'], 'pH is ideal for everyday aqueous measurements but must be supplemented by concentration, pKa and buffer capacity.'),
              ('Measuring pH with a meter is always better than using universal indicator.', ['meters are precise (±0.01) and objective', 'can log data continuously'], ['meters must be calibrated with buffers and are temperature sensitive', 'indicators are cheap, quick, and adequate for rough values'], 'A calibrated meter is far more precise, but indicator is acceptable when a rough value is enough.')],
    extended=[('25.0 cm³ of 0.100 mol dm⁻³ HCl is mixed with 15.0 cm³ of 0.100 mol dm⁻³ NaOH at 298 K. (a) Calculate the amount of excess acid. (b) Calculate the pH of the mixture. (c) Calculate the volume of NaOH needed to reach pH 7. (d) Explain why the pH changes rapidly near the end point.', '(a) 1.00 × 10⁻³ mol. (b) [H⁺] = 1.00 × 10⁻³/0.0400 = 0.0250 → pH 1.60. (c) 25.0 cm³. (d) near equivalence a tiny amount of excess reagent changes [H⁺] by orders of magnitude because the pH scale is logarithmic.', 7, 'multi_step')],
))


@R.add('ch05-st2', 'C3', (1, 4), 'numerical')
def c3_ph_strong(rng, slot):
    if rng.random() < 0.5:
        nm, f, n = pick(rng, STRONG_A)
        c = rsf(rng.uniform(1, 9.9) * 10 ** rng.choice([-4, -3, -2, -1]))
        stem = pick(rng, [f'Calculate the pH of {sf(c)} mol dm⁻³ {nm}.', f'What is the pH of a {sf(c)} mol dm⁻³ solution of {chem(f)}?'])
        return num(stem, ph(c), f'Strong acid: [H⁺] = {sf(c)} mol dm⁻³ (M1); pH = −log({sf(c)}) = {ph(c)} (A1).', 2)
    nm, f, n = pick(rng, STRONG_B)
    c = rsf(rng.uniform(1, 9.9) * 10 ** rng.choice([-4, -3, -2, -1]))
    oh = c * n
    phv = 14 + math.log10(oh)
    stem = pick(rng, [f'Calculate the pH of {sf(c)} mol dm⁻³ {nm} at 298 K.', f'Determine the pH of a {sf(c)} mol dm⁻³ solution of {chem(f)} at 298 K.'])
    return num(stem, f'{phv:.2f}', f'[OH⁻] = {n if n > 1 else ""}{" × " if n > 1 else ""}{sf(c)} = {sf(oh)} (M1); [H⁺] = Kw/[OH⁻] or pOH = {-math.log10(oh):.2f} (M1); pH = {phv:.2f} (A1).', 3)


@R.add('ch05-st2', 'C3', (1, 4), 'mcq')
def c3_ph_ratio(rng, slot):
    p1 = round(rng.uniform(1.0, 6.0), 1)
    d = rng.choice([1, 2, 3, 0.3, 0.5, 1.5])
    p2 = round(p1 + d, 1)
    f = 10 ** (p2 - p1)
    stem = f'Solution X has pH {p1} and solution Y has pH {p2}. How many times greater is [H⁺] in X than in Y?'
    return nmcq(rng, stem, f, [p2 / p1, p2 - p1, (p2 - p1) * 10, 2 * f], '', f'ratio = 10^({p2} − {p1}) = {sf(f, 2)}.', n=2, extra=True)


@R.add('ch05-st2', 'C3', (2, 4), 'numerical')
def c3_kw_temp(rng, slot):
    T, kw = pick(rng, [x for x in KW_T if x[0] != 25])
    h = math.sqrt(kw)
    stem = pick(rng, [f'At {T} °C, Kw = {sf(kw)}. Calculate the pH of pure water at this temperature and state whether it is acidic, neutral or alkaline.',
                      f'The ionic product of water at {T} °C is {sf(kw)}. Determine [H⁺] and pH for pure water at {T} °C.'])
    return num(stem, f'[H⁺] = {q(h, "mol dm⁻³")}; pH = {ph(h)}; neutral', f'[H⁺] = [OH⁻] = √{sf(kw)} = {sf(h)} mol dm⁻³ (M1); pH = {ph(h)} (A1); neutral because [H⁺] = [OH⁻] (R1).', 3)


@R.add('ch05-st2', 'C3', (2, 5), 'numerical')
def c3_mix_ph(rng, slot):
    nmA, fA, _ = pick(rng, STRONG_A)
    nmB, fB, nB = pick(rng, STRONG_B)
    ca = rng.choice([0.100, 0.200, 0.0500, 0.150])
    cb = rng.choice([0.100, 0.200, 0.0500, 0.150])
    va = rng.choice([20.0, 25.0, 30.0, 40.0, 50.0])
    vb = rng.choice([10.0, 15.0, 20.0, 25.0, 35.0, 45.0])
    nh = ca * va / 1000
    noh = cb * nB * vb / 1000
    vt = (va + vb) / 1000
    if abs(nh - noh) / max(nh, noh) < 0.05:
        return None
    if nh > noh:
        h = (nh - noh) / vt
        phv = -math.log10(h)
        ex = f'excess H⁺ = {sf(nh - noh)} mol; [H⁺] = {sf(h)}'
    else:
        oh = (noh - nh) / vt
        phv = 14 + math.log10(oh)
        ex = f'excess OH⁻ = {sf(noh - nh)} mol; [OH⁻] = {sf(oh)}'
    stem = f'{va} cm³ of {sf(ca)} mol dm⁻³ {nmA} is mixed with {vb} cm³ of {sf(cb)} mol dm⁻³ {nmB} at 298 K. Calculate the pH of the resulting solution.'
    return num(stem, f'{phv:.2f}', f'n(H⁺) = {sf(nh)}, n(OH⁻) = {sf(noh)} (M1); {ex} mol dm⁻³ in {va + vb:g} cm³ (M1); pH = {phv:.2f} (A1).', 3)


@R.add('ch05-st2', 'C3', (1, 4), 'mcq')
def c3_dilute_ph(rng, slot):
    p1 = round(rng.uniform(0.5, 3.5), 2)
    f = rng.choice([10, 100, 1000, 2, 5, 50])
    p2 = p1 + math.log10(f)
    nm = pick(rng, STRONG_A)[0]
    stem = f'A solution of {nm} has pH {p1:.2f}. It is diluted {f}-fold with water. What is the new pH?'
    wr = [p1 - math.log10(f), p1 * f, p1 + f]
    wr = [f'{w:.2f}' for w in wr if w > 0 and abs(w - p2) > 0.01]
    while len(wr) < 3:
        wr.append(f'{p2 + 1:.2f}')
    return mcq(rng, stem, f'{p2:.2f}', list(dict.fromkeys(wr))[:3], f'[H⁺] ÷ {f} → pH + log {f} = {p2:.2f}.')


R.mcqs('ch05-st2', 'C2', (1, 4), [
    ('Why does the pH of pure water decrease as temperature increases?', 'Autoionisation is endothermic, so Kw and [H⁺] increase.', ['Water becomes acidic.', 'OH⁻ ions evaporate.', 'Kw decreases.'], 'Le Chatelier.'),
    ('What is the pH of a neutral solution at 298 K?', '7.00', ['0', '14.00', '1.00'], '[H⁺] = 10⁻⁷.'),
    ('Why can the pH of a concentrated strong acid be negative?', 'If [H⁺] > 1 mol dm⁻³, −log[H⁺] is negative.', ['The pH scale stops at 0.', 'Kw becomes negative.', 'The acid becomes a base.'], 'e.g. 2 mol dm⁻³ HCl.'),
    ('How is the pH of a solution of a strong base calculated at 298 K?', 'pH = 14.00 − pOH', ['pH = pOH', 'pH = −log[OH⁻]', 'pH = 14 × [OH⁻]'], 'pH + pOH = 14.'),
])


# ---- ch05-st3 strong and weak; titration curves ----
R.facts('ch05-st3', F(
    terms=[('strong acid', 'an acid that dissociates (ionises) completely in aqueous solution'),
           ('weak acid', 'an acid that only partially dissociates in aqueous solution, establishing an equilibrium'),
           ('equivalence point', 'the point in a titration at which stoichiometrically equivalent amounts of acid and base have reacted'),
           ('neutralisation', 'the reaction between an acid and a base to form a salt and water (H⁺ + OH⁻ → H₂O)'),
           ('end point', 'the point in a titration at which the indicator changes colour'),
           ('pH curve', 'a graph of pH against the volume of titrant added during an acid–base titration')],
    facts=[('Which acid is weak?', 'ethanoic acid', ['hydrochloric acid', 'nitric acid', 'sulfuric acid'], 'Partially dissociated.'),
           ('At 298 K, what is the pH at the equivalence point of a strong acid–strong base titration?', '7', ['below 7', 'above 7', '1'], 'Neutral salt.'),
           ('Which observation distinguishes 0.1 mol dm⁻³ HCl from 0.1 mol dm⁻³ CH₃COOH?', 'HCl has a higher electrical conductivity.', ['HCl reacts with NaOH, but CH₃COOH does not.', 'CH₃COOH has a lower pH.', 'Both have pH 1.'], 'More ions.'),
           ('What is the pH at the equivalence point of a weak acid–strong base titration?', 'above 7', ['exactly 7', 'below 7', 'equal to the pKa'], 'Conjugate base hydrolyses.'),
           ('Why is the enthalpy of neutralisation of ethanoic acid less exothermic than that of HCl?', 'Energy is used to complete the dissociation of the weak acid.', ['Ethanoic acid is more concentrated.', 'Fewer moles of water form.', 'Ethanoic acid is a liquid.'], 'Endothermic ionisation.'),
           ('Equal volumes and concentrations of HCl and CH₃COOH need what volumes of NaOH for neutralisation?', 'the same volume', ['more for HCl', 'more for CH₃COOH', 'none for CH₃COOH'], 'Same amount of acid.')],
    why=[('Explain why 1.0 mol dm⁻³ ethanoic acid reacts more slowly with magnesium than 1.0 mol dm⁻³ hydrochloric acid.', 'Ethanoic acid is only partially dissociated, so its [H⁺] is much lower and collisions between H⁺ and Mg are less frequent.'),
         ('Explain why the same amount of hydrogen is eventually produced from equal amounts of HCl and CH₃COOH with excess magnesium.', 'As H⁺ is used, the weak acid equilibrium shifts to the right, releasing more H⁺ until all the acid has reacted; the total amount of acid is the same.'),
         ('Explain the shape of the pH curve when a strong base is added to a strong acid.', 'pH rises slowly at first (excess acid), then very steeply around the equivalence point (pH 7) where a drop of base changes [H⁺] by many orders of magnitude, then levels off at high pH (excess base).'),
         ('Explain why a concentrated weak acid can have a lower pH than a dilute strong acid.', 'pH depends on [H⁺]; a large concentration of a partially dissociated acid can give more H⁺ than a very dilute fully dissociated acid.')],
    contrast=[('a strong acid', 'a concentrated acid', 'Strength refers to the extent of dissociation; concentration refers to the amount of acid per unit volume.'),
              ('the equivalence point', 'the end point', 'The equivalence point is where stoichiometric amounts have reacted; the end point is where the indicator changes colour – ideally the same.'),
              ('a strong base', 'a weak base', 'A strong base (e.g. NaOH) is fully dissociated/ionised; a weak base (e.g. NH₃) only partially reacts with water to form OH⁻.')],
    misc=[('A weak acid needs less alkali to neutralise it than a strong acid.', 'Equal amounts of any monoprotic acid need the same amount of alkali; strength affects pH, not stoichiometry.'),
          ('Strong acids are always concentrated.', 'Strength is the degree of dissociation; a strong acid can be very dilute.'),
          ('The pH at the equivalence point is always 7.', 'Only for strong acid–strong base at 298 K; weak acid–strong base > 7, strong acid–weak base < 7.')],
    apply=[('Sketch the pH curve for adding 0.10 mol dm⁻³ NaOH to 25.0 cm³ of 0.10 mol dm⁻³ CH₃COOH and label the equivalence point.', 'starts ≈ pH 2.9, buffer region, steep rise ≈ pH 7–11 at 25.0 cm³, equivalence ≈ pH 8.7, levels ≈ 12.5', 3),
           ('State three experimental differences between 0.10 mol dm⁻³ HNO₃ and 0.10 mol dm⁻³ HCOOH.', 'HNO₃ lower pH, higher conductivity, faster reaction with Mg/CaCO₃ (and more exothermic neutralisation)', 3)],
    evaluate=[('Conductivity measurements are the best way to distinguish strong and weak acids.', ['direct measure of ion concentration', 'quick, quantitative'], ['concentration must be identical', 'pH meters give equivalent information', 'rates of reaction or ΔH of neutralisation also distinguish them'], 'Conductivity is a good method, but only valid for equal concentrations; pH is equally effective.'),
              ('Titration is the most reliable way to find the concentration of an acid.', ['precise (±0.1 cm³ burette) and cheap', 'works for strong and weak acids'], ['end point detection depends on indicator choice', 'pH-metric or conductometric titrations avoid subjective colour changes'], 'Titration is reliable when an appropriate indicator or pH probe is used.')],
    extended=[('A student titrates 25.0 cm³ of 0.100 mol dm⁻³ NH₃(aq) with 0.100 mol dm⁻³ HCl. (a) Write the ionic equation. (b) Calculate the volume of HCl at the equivalence point. (c) Sketch the pH curve and estimate the pH at equivalence, explaining it. (d) Suggest a suitable indicator.', '(a) NH₃ + H⁺ → NH₄⁺. (b) 25.0 cm³. (c) starts ~11.1, buffer region, steep fall ~7 → 3, equivalence ~5.3 because NH₄⁺ is acidic. (d) methyl red (or methyl orange).', 7, 'multi_step')],
))


@R.add('ch05-st3', 'C3', (1, 4), 'mcq')
def c3_equiv_ph(rng, slot):
    combos = [('strong acid', 'strong base', '7', ['hydrochloric acid', 'nitric acid'], ['sodium hydroxide', 'potassium hydroxide']),
              ('weak acid', 'strong base', 'above 7', [a[0] for a in ACIDS[:6]], ['sodium hydroxide', 'potassium hydroxide']),
              ('strong acid', 'weak base', 'below 7', ['hydrochloric acid', 'nitric acid'], ['ammonia', 'methylamine', 'ethylamine'])]
    ta, tb, right, As, Bs = pick(rng, combos)
    a, b = pick(rng, As), pick(rng, Bs)
    stem = f'{cap(a)} is titrated with {b}. What is the pH at the equivalence point at 298 K?'
    return mcq(rng, stem, right, [x for x in ['7', 'above 7', 'below 7', 'exactly 14'] if x != right], f'{ta} + {tb}: salt is {"neutral" if right == "7" else "basic (conjugate base hydrolyses)" if right == "above 7" else "acidic (conjugate acid hydrolyses)"}.')


@R.add('ch05-st3', 'C3', (1, 4), 'numerical')
def c3_equiv_vol(rng, slot):
    acid = pick(rng, [('hydrochloric acid', 1), ('ethanoic acid', 1), ('sulfuric acid', 2), ('nitric acid', 1), ('ethanedioic acid', 2), ('methanoic acid', 1)])
    base = pick(rng, [('sodium hydroxide', 1), ('potassium hydroxide', 1), ('barium hydroxide', 2)])
    ca = rng.choice([0.0500, 0.100, 0.125, 0.200, 0.0800])
    va = rng.choice([10.0, 20.0, 25.0])
    cb = rng.choice([0.100, 0.150, 0.200, 0.0950])
    v = ca * acid[1] * va / (cb * base[1])
    stem = f'Calculate the volume of {sf(cb)} mol dm⁻³ {base[0]} needed to reach the equivalence point with {va} cm³ of {sf(ca)} mol dm⁻³ {acid[0]}.'
    return num(stem, q(v, 'cm³'), f'n(H⁺) = {sf(ca)} × {va / 1000} × {acid[1]} = {sf(ca * va / 1000 * acid[1])} mol (M1); n(base) = n(H⁺)/{base[1]} (M1); V = {q(v, "cm³")} (A1).', 3)


@R.add('ch05-st3', 'C3', (1, 4), 'mcq')
def c3_strong_weak_obs(rng, slot):
    a = pick(rng, ['hydrochloric acid', 'nitric acid'])
    w = pick(rng, [x[0] for x in ACIDS[:6]])
    c = rng.choice(['0.100', '0.500', '1.00', '0.0500'])
    tests = [('pH', f'{a} has the lower pH'), ('electrical conductivity', f'{a} has the higher conductivity'), ('rate of reaction with magnesium ribbon', f'{a} produces bubbles faster'),
             ('temperature rise on neutralisation with excess NaOH', f'{a} gives a slightly larger temperature rise'), ('volume of NaOH needed for neutralisation', 'they need the same volume')]
    t, right = pick(rng, tests)
    wr = [r for _, r in tests if r != right]
    if t != 'volume of NaOH needed for neutralisation':
        wr = [f'{w} has the lower pH' if 'pH' in t else f'{w} gives the faster/larger change'] + [x for x in wr if 'same volume' in x] + [f'there is no difference in {t}']
    wr = list(dict.fromkeys(wr))
    stem = f'Solutions of {a} and {w}, both {c} mol dm⁻³, are compared by measuring {t}. What result is expected?'
    return mcq(rng, stem, right, [x for x in wr if x != right][:3], f'{a} is fully dissociated (higher [H⁺]); both contain the same amount of acid.')


R.mcqs('ch05-st3', 'C2', (1, 4), [
    ('Why does a weak acid give a higher pH than a strong acid of the same concentration?', 'It is only partially dissociated, so [H⁺] is lower.', ['It contains fewer molecules.', 'It needs less alkali.', 'It is more concentrated.'], 'Degree of dissociation.'),
    ('Why is there a gradual rise (buffer region) on the pH curve of a weak acid with a strong base?', 'A mixture of the weak acid and its conjugate base resists pH change.', ['The base is weak.', 'The indicator reacts.', 'The acid is fully neutralised.'], 'HA/A⁻ buffer.'),
    ('Why does ammonia solution conduct electricity poorly?', 'Only a small fraction of NH₃ molecules react with water to form ions.', ['It contains no ions.', 'NH₃ is a strong base.', 'It is a covalent gas.'], 'Weak base.'),
    ('What does the vertical section of a pH curve represent?', 'the region around the equivalence point where pH changes rapidly', ['the buffer region', 'the start of the titration', 'where the acid is in excess'], 'Steep jump.'),
])


@p1b(R, 'ch05-st3')
def p1b_ph_curve(rng, slot):
    nm, f, cb_, pka = pick(rng, ACIDS[:6])
    ca = rng.choice([0.100, 0.0800, 0.120])
    va = 25.00
    cb = 0.100
    veq = ca * va / cb
    ka = 10 ** -pka
    def phat(v):
        na = ca * va / 1000
        nb = cb * v / 1000
        vt = (va + v) / 1000
        if v == 0:
            return -math.log10(math.sqrt(ka * ca))
        if nb < na:
            return pka + math.log10(nb / (na - nb))
        if abs(nb - na) < 1e-12:
            cA = na / vt
            return 14 + math.log10(math.sqrt(KW / ka * cA))
        return 14 + math.log10((nb - na) / vt)
    vols = [0, round(veq / 4, 1), round(veq / 2, 1), round(3 * veq / 4, 1), round(veq - 1, 1), round(veq, 2), round(veq + 1, 1), round(veq + 10, 1)]
    tab = '\n'.join(f'{v:.2f} | {phat(v):.2f}' for v in vols)
    intro = (f'25.00 cm³ of {sf(ca)} mol dm⁻³ {nm} was titrated with {sf(cb)} mol dm⁻³ sodium hydroxide, and the pH was recorded with a calibrated pH meter (±0.01).\n\nvolume NaOH / cm³ | pH\n{tab}')
    return dict(intro=intro, parts=[
        ('State the volume of NaOH at the equivalence point and explain how it is identified from the data.', f'{veq:.2f} cm³ – the centre of the steepest rise in pH', f'{veq:.2f} cm³ (A1); midpoint of vertical section (R1).', 2),
        (f'Use the data to determine the pKa of {nm}, explaining your method.', f'pKa = pH at half-equivalence = {phat(round(veq / 2, 1)):.2f}', f'At half-equivalence [HA] = [A⁻] so pH = pKa (R1); {phat(round(veq / 2, 1)):.2f} (A1).', 2),
        ('Explain why the pH at the equivalence point is above 7.', f'The salt formed contains the conjugate base {ionx(cb_)}, which accepts protons from water forming OH⁻.', f'{ionx(cb_)} hydrolyses: A⁻ + H₂O ⇌ HA + OH⁻ (1).', 1),
        ('Suggest, with a reason, a suitable indicator for this titration.', 'phenolphthalein (pKa 9.6), which changes colour within the steep rise above pH 7', 'phenolphthalein (1); colour change range within vertical section (1).', 2),
        ('State one reason why a pH meter must be calibrated before use.', 'To ensure readings are accurate, using buffer solutions of known pH.', 'Calibration with standard buffers removes systematic error (1).', 1)],
        extras=[])


# =============================================================================================
# ch06 R3.1 Proton transfer: equilibria and buffers (HL)
# =============================================================================================
WEAK = [a for a in ACIDS]


def weak_ph(c, pka):
    ka = 10 ** -pka
    return -math.log10(math.sqrt(ka * c)), math.sqrt(ka * c)


R.facts('ch06-st1', F(
    terms=[('acid dissociation constant (Ka)', 'the equilibrium constant for HA(aq) ⇌ H⁺(aq) + A⁻(aq): Ka = [H⁺][A⁻]/[HA]'),
           ('pKa', 'the negative logarithm of Ka: pKa = −log₁₀Ka; a smaller pKa means a stronger acid'),
           ('base dissociation constant (Kb)', 'the equilibrium constant for B(aq) + H₂O(l) ⇌ BH⁺(aq) + OH⁻(aq): Kb = [BH⁺][OH⁻]/[B]'),
           ('percentage dissociation', 'the percentage of the weak acid molecules that have dissociated at equilibrium: [H⁺]/[HA]₀ × 100'),
           ('pKb', 'the negative logarithm of Kb; for a conjugate pair pKa + pKb = 14.00 at 298 K')],
    facts=[('Which acid is the strongest?', 'chloroethanoic acid (pKa 2.87)', ['ethanoic acid (pKa 4.76)', 'propanoic acid (pKa 4.87)', 'phenol (pKa 9.99)'], 'Smallest pKa.'),
           ('For a conjugate acid–base pair at 298 K, Ka × Kb equals', 'Kw', ['1', 'pKa', '14'], 'Ka × Kb = 1.00 × 10⁻¹⁴.'),
           ('What approximation is usually made when calculating the pH of a weak acid?', '[HA] at equilibrium ≈ initial concentration', ['[H⁺] = initial concentration', 'Ka = 1', '[A⁻] = 0'], 'Small dissociation.'),
           ('Which base is the strongest?', 'dimethylamine (pKb 3.27)', ['ammonia (pKb 4.75)', 'phenylamine (pKb 9.13)', 'water'], 'Smallest pKb.'),
           ('How does the percentage dissociation of a weak acid change on dilution?', 'it increases', ['it decreases', 'it stays the same', 'it becomes zero'], 'Le Chatelier – more particles side favoured.'),
           ('If pKa = 4.76, what is Ka?', '1.74 × 10⁻⁵', ['4.76', '5.76 × 10⁻⁴', '1.74 × 10⁵'], 'Ka = 10⁻ᵖᴷᵃ.')],
    why=[('Explain why a smaller pKa indicates a stronger acid.', 'pKa = −log Ka, so a smaller pKa means a larger Ka: the equilibrium lies further to the right and more H⁺ ions are produced.'),
         ('Explain why chloroethanoic acid is a stronger acid than ethanoic acid.', 'The electronegative Cl atom withdraws electron density, stabilising the carboxylate anion (spreading its charge) and weakening the O–H bond, so dissociation is more favourable.'),
         ('Explain why the pH of a weak acid cannot be calculated simply from its concentration.', 'Only a small fraction dissociates, so [H⁺] is much less than the acid concentration; Ka is needed to find [H⁺].'),
         ('Explain the relationship between the strength of an acid and the strength of its conjugate base.', 'Ka × Kb = Kw, so the stronger the acid (larger Ka), the weaker its conjugate base (smaller Kb).')],
    contrast=[('Ka', 'pKa', 'Ka is the dissociation constant (larger = stronger acid); pKa = −log Ka (smaller = stronger acid) and is more convenient for comparison.'),
              ('Ka', 'Kb', 'Ka measures the extent of proton donation by an acid to water; Kb measures proton acceptance from water by a base.')],
    misc=[('A larger pKa means a stronger acid.', 'A larger pKa means a smaller Ka, so a weaker acid.'),
          ('Diluting a weak acid decreases its percentage dissociation.', 'Dilution shifts HA ⇌ H⁺ + A⁻ to the right, increasing the percentage dissociation (although [H⁺] falls).')],
    apply=[('Calculate the pH of 0.100 mol dm⁻³ ethanoic acid (pKa 4.76).', '[H⁺] = √(1.74 × 10⁻⁵ × 0.100) = 1.32 × 10⁻³; pH = 2.88', 3),
           ('The pKa of NH₄⁺ is 9.25. Calculate the pKb of NH₃.', '14.00 − 9.25 = 4.75', 1)],
    evaluate=[('The approximation [HA]eq ≈ [HA]₀ is always acceptable for weak acids.', ['valid when Ka is small and c is not too low (dissociation < 5 %)', 'greatly simplifies calculations'], ['fails for relatively strong weak acids (pKa < 3) or very dilute solutions', 'the quadratic method is needed then'], 'It is acceptable in most IB contexts but must be checked (x < 5 % of c).'),
              ('pKa values are the best way to compare the strength of acids.', ['logarithmic scale is convenient', 'independent of concentration', 'tabulated in the data booklet'], ['depend on temperature and solvent', 'say nothing about the amount of acid present', 'for polyprotic acids several values are needed'], 'pKa is the best single measure of intrinsic strength, but conditions and polyprotic behaviour must be considered.')],
    extended=[('Methanoic acid (pKa 3.75) is found in ant stings. (a) Write the Ka expression. (b) Calculate the pH of 0.0500 mol dm⁻³ methanoic acid. (c) Calculate its percentage dissociation. (d) Compare its strength with ethanoic acid (pKa 4.76) and suggest a reason.', '(a) Ka = [H⁺][HCOO⁻]/[HCOOH]. (b) Ka = 1.78 × 10⁻⁴; [H⁺] = 2.98 × 10⁻³; pH = 2.53. (c) 5.96 %. (d) methanoic is stronger; the CH₃ group in ethanoic acid is electron-donating, destabilising the anion.', 8, 'multi_step')],
))


@R.add('ch06-st1', 'C3', (2, 5), 'numerical')
def c3_weak_ph(rng, slot):
    nm, f, cb_, pka = pick(rng, WEAK)
    c = rng.choice([0.0100, 0.0500, 0.100, 0.200, 0.250, 0.500, 1.00])
    phv, h = weak_ph(c, pka)
    if h / c > 0.05:
        return None
    stem = pick(rng, [f'Calculate the pH of {sf(c)} mol dm⁻³ {nm} (pKa = {pka:.2f}).', f'Determine the pH of a {sf(c)} mol dm⁻³ solution of {chem(f)}, given pKa = {pka:.2f}.'])
    return num(stem, f'{phv:.2f}', f'Ka = 10⁻{pka:.2f} = {sf(10 ** -pka)} (M1); [H⁺] = √(Ka × c) = {sf(h)} mol dm⁻³ (M1); pH = {phv:.2f} (A1).', 3)


@R.add('ch06-st1', 'C3', (2, 5), 'numerical')
def c3_ka_from_ph(rng, slot):
    nm, f, cb_, pka = pick(rng, WEAK)
    c = rng.choice([0.0500, 0.100, 0.200, 0.500])
    phv, h = weak_ph(c, pka)
    phr = round(phv, 2)
    hh = 10 ** -phr
    ka = hh ** 2 / c
    stem = f'A {sf(c)} mol dm⁻³ solution of {nm} has a pH of {phr:.2f}. Calculate Ka and pKa for the acid, and its percentage dissociation.'
    return num(stem, f'Ka = {sf(ka)}; pKa = {-math.log10(ka):.2f}; {hh / c * 100:.2f} %', f'[H⁺] = 10⁻{phr:.2f} = {sf(hh)} (M1); Ka = [H⁺]²/c = {sf(ka)} (A1); pKa = {-math.log10(ka):.2f} (A1); % = {sf(hh)}/{sf(c)} × 100 = {hh / c * 100:.2f} % (A1).', 4, 'multi_step')


@R.add('ch06-st1', 'C3', (2, 5), 'numerical')
def c3_weak_base_ph(rng, slot):
    nm, f, ca_, pkb = pick(rng, BASES)
    c = rng.choice([0.0500, 0.100, 0.200, 0.500])
    kb = 10 ** -pkb
    oh = math.sqrt(kb * c)
    if oh / c > 0.06:
        return None
    phv = 14 + math.log10(oh)
    stem = f'Calculate the pH of {sf(c)} mol dm⁻³ {nm} at 298 K (pKb = {pkb:.2f}).'
    return num(stem, f'{phv:.2f}', f'Kb = {sf(kb)} (M1); [OH⁻] = √(Kb × c) = {sf(oh)} (M1); pOH = {-math.log10(oh):.2f}; pH = {phv:.2f} (A1).', 3)


@R.add('ch06-st1', 'C3', (1, 4), 'mcq')
def c3_strength_rank(rng, slot):
    pool = rng.sample(WEAK, 4)
    kind = rng.choice(['strongest', 'weakest'])
    best = (min if kind == 'strongest' else max)(pool, key=lambda a: a[3])
    stem = f'The pKa values of four acids are: ' + '; '.join(f'{a[0]} {a[3]:.2f}' for a in sorted(pool, key=lambda a: a[0])) + f'. Which is the {kind} acid?'
    return mcq(rng, stem, best[0], [a[0] for a in pool if a != best], f'{"Smallest" if kind == "strongest" else "Largest"} pKa → {kind}: {best[0]}.')


@R.add('ch06-st1', 'C3', (1, 4), 'mcq')
def c3_pka_pkb(rng, slot):
    if rng.random() < 0.5:
        nm, f, cb_, pka = pick(rng, WEAK)
        v = 14 - pka
        stem = f'The pKa of {nm} is {pka:.2f}. What is the pKb of its conjugate base, {ionx(cb_)}, at 298 K?'
        return mcq(rng, stem, f'{v:.2f}', [f'{pka:.2f}', f'{14 + pka:.2f}', f'{pka - 7:.2f}' if pka > 7 else f'{7 - pka + 7:.2f}'], f'pKa + pKb = 14.00 → {v:.2f}.')
    nm, f, ca_, pkb = pick(rng, BASES)
    v = 14 - pkb
    stem = f'The pKb of {nm} is {pkb:.2f}. What is the pKa of its conjugate acid, {ionx(ca_)}, at 298 K?'
    return mcq(rng, stem, f'{v:.2f}', [f'{pkb:.2f}', f'{14 + pkb:.2f}', f'{abs(7 - pkb):.2f}'], f'pKa + pKb = 14.00 → {v:.2f}.')


R.mcqs('ch06-st1', 'C2', (1, 4), [
    ('Why does Ka for a weak acid not change when the acid is diluted?', 'Ka depends only on temperature.', ['The acid becomes strong.', 'The dissociation stops.', 'Ka depends on concentration.'], 'Equilibrium constant.'),
    ('Why is phenylamine a much weaker base than ammonia?', 'The nitrogen lone pair is delocalised into the benzene ring, so it is less available to accept a proton.', ['It has no lone pair.', 'It is a larger molecule.', 'It is insoluble in water.'], 'pKb 9.13 vs 4.75.'),
    ('Which statement explains why the conjugate base of a weak acid is a weak base?', 'Ka × Kb = Kw, so a moderate Ka gives a moderate Kb.', ['It has no charge.', 'It is always a strong base.', 'It contains no hydrogen.'], 'e.g. CH₃COO⁻ pKb 9.24.'),
    ('Why must the approximation [HA]eq ≈ [HA]₀ be checked?', 'It is valid only if the acid dissociates by less than about 5 %.', ['It is always invalid.', 'Ka depends on it.', 'It changes the pKa.'], '5 % rule.'),
])


# ---- ch06-st2 buffers ----
R.facts('ch06-st2', F(
    terms=[('buffer solution', 'a solution that resists changes in pH when small amounts of acid or base are added'),
           ('acidic buffer', 'a buffer made from a weak acid and its conjugate base (salt), e.g. CH₃COOH/CH₃COONa'),
           ('basic buffer', 'a buffer made from a weak base and its conjugate acid (salt), e.g. NH₃/NH₄Cl'),
           ('buffer capacity', 'the amount of acid or base that a buffer can neutralise before its pH changes significantly'),
           ('Henderson–Hasselbalch relationship', 'the equation pH = pKa + log₁₀([A⁻]/[HA]), used to calculate the pH of an acidic buffer')],
    facts=[('Which mixture forms a buffer solution?', 'ethanoic acid and sodium ethanoate', ['hydrochloric acid and sodium chloride', 'sodium hydroxide and sodium chloride', 'nitric acid and sodium nitrate'], 'Weak acid + conjugate base.'),
           ('What is the pH of a buffer containing equal concentrations of HA and A⁻?', 'equal to the pKa', ['7', '14 − pKa', '2 × pKa'], 'log 1 = 0.'),
           ('Which mixture makes a basic buffer?', 'ammonia and ammonium chloride', ['ammonia and sodium hydroxide', 'ammonium chloride and HCl', 'sodium hydroxide and water'], 'Weak base + conjugate acid.'),
           ('Which is the most important buffer in blood plasma?', 'carbonic acid / hydrogencarbonate', ['ethanoic acid / ethanoate', 'ammonia / ammonium', 'hydrochloric acid / chloride'], 'H₂CO₃/HCO₃⁻.'),
           ('What happens to the pH of a buffer when it is diluted with water?', 'it stays almost the same', ['it increases sharply', 'it decreases sharply', 'it becomes 7'], 'Ratio unchanged.'),
           ('Mixing 2 mol of CH₃COOH with 1 mol of NaOH gives', 'a buffer with [CH₃COOH] = [CH₃COO⁻]', ['a neutral solution', 'excess NaOH', 'only sodium ethanoate'], 'Half neutralised.')],
    why=[('Explain how an ethanoic acid / sodium ethanoate buffer resists a decrease in pH when a small amount of acid is added.', 'The added H⁺ reacts with the large reservoir of ethanoate ions: CH₃COO⁻ + H⁺ → CH₃COOH, so [H⁺] barely changes.'),
         ('Explain how an ammonia/ammonium chloride buffer responds to the addition of a small amount of NaOH.', 'The added OH⁻ reacts with NH₄⁺: NH₄⁺ + OH⁻ → NH₃ + H₂O, removing most of the OH⁻ so the pH changes very little.'),
         ('Explain why a mixture of hydrochloric acid and sodium chloride is not a buffer.', 'Cl⁻ is the conjugate base of a strong acid and has negligible tendency to accept protons, so it cannot remove added H⁺, and HCl cannot remove OH⁻ reversibly.'),
         ('Explain why a buffer works best when pH ≈ pKa.', 'When [HA] ≈ [A⁻], both components are present in large amounts, so the buffer can neutralise added acid or base equally well.')],
    contrast=[('an acidic buffer', 'a basic buffer', 'An acidic buffer (weak acid + its salt) holds the pH below 7; a basic buffer (weak base + its salt) holds it above 7.'),
              ('buffer pH', 'buffer capacity', 'Buffer pH depends on pKa and the ratio [A⁻]/[HA]; buffer capacity depends on the actual concentrations of the components.')],
    misc=[('A buffer keeps the pH completely constant.', 'A buffer minimises pH change for small additions; large additions exceed its capacity.'),
          ('Any acid mixed with its salt forms a buffer.', 'Only a WEAK acid with its conjugate base forms a buffer; strong acid/salt mixtures do not.')],
    apply=[('Calculate the pH of a buffer containing 0.200 mol dm⁻³ CH₃COOH and 0.100 mol dm⁻³ CH₃COONa (pKa 4.76).', 'pH = 4.76 + log(0.100/0.200) = 4.46', 2),
           ('Suggest a buffer system suitable for maintaining pH 9.25.', 'NH₃/NH₄Cl with equal concentrations (pKa of NH₄⁺ = 9.25)', 2)],
    evaluate=[('Buffers are essential to life.', ['blood pH must stay 7.35–7.45 (carbonate buffer)', 'enzymes work in narrow pH ranges; cells use phosphate and protein buffers'], ['organisms also control pH by breathing (CO₂) and excretion (kidneys)', 'buffers have limited capacity – other regulation is needed'], 'Buffers are essential, working together with respiratory and renal control.'),
              ('The Henderson–Hasselbalch equation gives the exact pH of a buffer.', ['derived directly from Ka', 'accurate for typical buffers'], ['assumes initial concentrations equal equilibrium concentrations', 'fails for very dilute buffers or extreme ratios', 'uses concentrations not activities'], 'It is an excellent approximation within its assumptions, not an exact result.')],
    extended=[('A buffer is made by adding 50.0 cm³ of 0.100 mol dm⁻³ NaOH to 100.0 cm³ of 0.100 mol dm⁻³ ethanoic acid (pKa 4.76). (a) Calculate the amounts of CH₃COOH and CH₃COO⁻ present. (b) Calculate the pH. (c) Calculate the pH after adding 1.00 × 10⁻³ mol of HCl. (d) Explain why the pH change is small.', '(a) 5.00 × 10⁻³ mol each. (b) 4.76. (c) 6.00 × 10⁻³ HA, 4.00 × 10⁻³ A⁻ → pH = 4.76 + log(4/6) = 4.58. (d) added H⁺ converted to CH₃COOH by ethanoate.', 8, 'multi_step')],
))


@R.add('ch06-st2', 'C3', (2, 5), 'numerical')
def c3_buffer_ph(rng, slot):
    nm, f, cb_, pka = pick(rng, [a for a in WEAK if a[3] < 8])
    ca = rng.choice([0.0500, 0.100, 0.150, 0.200, 0.250, 0.500])
    cs = rng.choice([0.0500, 0.100, 0.150, 0.200, 0.250, 0.500])
    phv = pka + math.log10(cs / ca)
    salt = 'sodium ' + nm.replace(' acid', '').replace('ic', 'ate').replace('oate', 'oate')
    salt = {'ethanoic acid': 'sodium ethanoate', 'methanoic acid': 'sodium methanoate', 'propanoic acid': 'sodium propanoate', 'benzoic acid': 'sodium benzoate', 'chloroethanoic acid': 'sodium chloroethanoate', 'butanoic acid': 'sodium butanoate', 'nitrous acid': 'sodium nitrite', 'hypochlorous acid': 'sodium hypochlorite'}.get(nm, salt)
    stem = pick(rng, [f'Calculate the pH of a buffer solution containing {sf(ca)} mol dm⁻³ {nm} (pKa {pka:.2f}) and {sf(cs)} mol dm⁻³ {salt}.',
                      f'A buffer is prepared with [{chem(f)}] = {sf(ca)} mol dm⁻³ and [{ionx(cb_)}] = {sf(cs)} mol dm⁻³. Given pKa = {pka:.2f}, determine its pH.'])
    return num(stem, f'{phv:.2f}', f'pH = pKa + log([A⁻]/[HA]) (M1) = {pka:.2f} + log({sf(cs)}/{sf(ca)}) = {phv:.2f} (A1).', 2)


@R.add('ch06-st2', 'C3', (3, 5), 'numerical')
def c3_buffer_partial(rng, slot):
    nm, f, cb_, pka = pick(rng, [a for a in WEAK if a[3] < 6])
    va = rng.choice([50.0, 100.0, 25.0])
    ca = rng.choice([0.100, 0.200])
    vb = rng.choice([10.0, 15.0, 20.0, 25.0, 30.0, 40.0])
    cb = 0.100
    na = ca * va / 1000
    nb = cb * vb / 1000
    if nb >= na * 0.95:
        return None
    phv = pka + math.log10(nb / (na - nb))
    stem = f'{vb} cm³ of {sf(cb)} mol dm⁻³ NaOH is added to {va} cm³ of {sf(ca)} mol dm⁻³ {nm} (pKa {pka:.2f}). Calculate the pH of the resulting buffer.'
    return num(stem, f'{phv:.2f}', f'n(HA)₀ = {sf(na)}, n(OH⁻) = {sf(nb)} mol (M1); after reaction n(A⁻) = {sf(nb)}, n(HA) = {sf(na - nb)} (M1); pH = {pka:.2f} + log({sf(nb)}/{sf(na - nb)}) = {phv:.2f} (A1).', 3)


@R.add('ch06-st2', 'C3', (1, 4), 'mcq')
def c3_buffer_pick(rng, slot):
    good = [('CH₃COOH and CH₃COONa', 'acidic'), ('NH₃ and NH₄Cl', 'basic'), ('HCOOH and HCOOK', 'acidic'), ('H₂CO₃ and NaHCO₃', 'acidic'), ('NaH₂PO₄ and Na₂HPO₄', 'acidic (pH ≈ 7.2)'),
            ('excess CH₃COOH with a little NaOH', 'acidic'), ('excess NH₃ with a little HCl', 'basic'), ('C₆H₅COOH and C₆H₅COONa', 'acidic'), ('CH₃NH₂ and CH₃NH₃Cl', 'basic')]
    bad = ['HCl and NaCl', 'NaOH and NaCl', 'HNO₃ and KNO₃', 'excess NaOH with a little CH₃COOH', 'excess HCl with a little NH₃', 'NaCl and water', 'H₂SO₄ and Na₂SO₄', 'KOH and KCl']
    g = pick(rng, good)
    wr = rng.sample(bad, 3)
    stem = pick(rng, ['Which mixture of aqueous solutions acts as a buffer?', 'Which combination would produce a buffer solution?']) + ' (' + '; '.join(sorted([g[0]] + wr)) + ')'
    return mcq(rng, stem, g[0], wr, f'{g[0]}: weak acid/base and its conjugate present together ({g[1]} buffer).')


@R.add('ch06-st2', 'C3', (2, 4), 'mcq')
def c3_buffer_ratio(rng, slot):
    nm, f, cb_, pka = pick(rng, [a for a in WEAK if a[3] < 8])
    target = round(pka + rng.choice([-1, -0.5, -0.3, 0.3, 0.5, 1]), 2)
    r = 10 ** (target - pka)
    stem = f'What ratio [{ionx(cb_)}]/[{chem(f)}] gives a buffer of pH {target:.2f}, given pKa({nm}) = {pka:.2f}?'
    return nmcq(rng, stem, r, [1 / r, target - pka, 10 * r], '', f'log ratio = pH − pKa = {target - pka:.2f}; ratio = {sf(r)}.', extra=True)


R.mcqs('ch06-st2', 'C2', (1, 4), [
    ('Why does a buffer need large concentrations of both the weak acid and its conjugate base?', 'So that both added H⁺ and added OH⁻ can be removed without greatly changing the ratio.', ['To make the pH equal to 7.', 'To increase Ka.', 'So that the acid becomes strong.'], 'Capacity.'),
    ('What happens to the ratio [A⁻]/[HA] when a little acid is added to an acidic buffer?', 'It decreases slightly.', ['It increases greatly.', 'It does not change at all.', 'It becomes zero.'], 'A⁻ → HA.'),
    ('Why does hyperventilation raise blood pH?', 'Losing CO₂ shifts H₂CO₃ ⇌ CO₂ + H₂O, removing H⁺ via HCO₃⁻ + H⁺ → H₂CO₃.', ['It adds OH⁻ to blood.', 'It increases [H₂CO₃].', 'It removes HCO₃⁻.'], 'Carbonate buffer equilibrium.'),
    ('Why is the pH of a buffer almost unchanged on dilution?', 'Both concentrations fall by the same factor, so their ratio is unchanged.', ['Water is a buffer.', 'Ka increases.', 'The acid dissociates fully.'], 'Ratio constant.'),
])


# ---- ch06-st3 pH curves, indicators and salt pH ----
SALTS = [('sodium chloride', 'NaCl', 'neutral', 'ions of a strong acid and a strong base do not hydrolyse'),
         ('ammonium chloride', 'NH4Cl', 'acidic', 'NH₄⁺ donates a proton: NH₄⁺ ⇌ NH₃ + H⁺'),
         ('sodium ethanoate', 'CH3COONa', 'basic', 'CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻'),
         ('sodium carbonate', 'Na2CO3', 'basic', 'CO₃²⁻ + H₂O ⇌ HCO₃⁻ + OH⁻'),
         ('potassium nitrate', 'KNO3', 'neutral', 'neither ion hydrolyses'),
         ('iron(III) chloride', 'FeCl3', 'acidic', '[Fe(H₂O)₆]³⁺ ⇌ [Fe(H₂O)₅(OH)]²⁺ + H⁺ (high charge density)'),
         ('aluminium chloride', 'AlCl3', 'acidic', '[Al(H₂O)₆]³⁺ releases H⁺ (high charge density cation)'),
         ('sodium methanoate', 'HCOONa', 'basic', 'HCOO⁻ accepts a proton from water'),
         ('ammonium nitrate', 'NH4NO3', 'acidic', 'NH₄⁺ is a weak acid; NO₃⁻ does not hydrolyse'),
         ('potassium ethanoate', 'CH3COOK', 'basic', 'ethanoate is a weak base'),
         ('sodium sulfate', 'Na2SO4', 'neutral', 'ions of a strong acid and a strong base'),
         ('sodium hydrogencarbonate', 'NaHCO3', 'basic (weakly)', 'HCO₃⁻ is a slightly stronger base than acid')]

R.facts('ch06-st3', F(
    terms=[('acid–base indicator', 'a weak acid (HIn) whose undissociated form and conjugate base (In⁻) have different colours'),
           ('end point', 'the point at which the indicator changes colour, ideally coinciding with the equivalence point'),
           ('salt hydrolysis', 'the reaction of an ion of a salt with water, producing H⁺ or OH⁻ and changing the pH'),
           ('half-equivalence point', 'the point in a weak acid titration at which half the acid has been neutralised, where pH = pKa'),
           ('colour change range', 'the pH range over which an indicator changes colour, approximately pKa(HIn) ± 1')],
    facts=[('Which indicator is suitable for titrating ethanoic acid with sodium hydroxide?', 'phenolphthalein', ['methyl orange', 'bromophenol blue', 'methyl red'], 'Equivalence pH > 7.'),
           ('Which indicator is suitable for titrating ammonia with hydrochloric acid?', 'methyl orange', ['phenolphthalein', 'phenol red', 'thymol blue'], 'Equivalence pH < 7.'),
           ('A solution of ammonium chloride is', 'acidic', ['neutral', 'basic', 'strongly basic'], 'NH₄⁺ is a weak acid.'),
           ('Why is no indicator suitable for a weak acid–weak base titration?', 'There is no sharp vertical section in the pH curve.', ['The equivalence point is at pH 7.', 'The reactants are coloured.', 'The reaction is too slow.'], 'Gradual pH change.'),
           ('At the half-equivalence point of a weak acid titration, pH equals', 'pKa', ['7', 'pKb', '14 − pKa'], '[HA] = [A⁻].'),
           ('Which salt forms a basic solution?', 'sodium ethanoate', ['sodium chloride', 'ammonium nitrate', 'potassium nitrate'], 'Conjugate base of a weak acid.')],
    why=[('Explain how an indicator changes colour.', 'HIn ⇌ H⁺ + In⁻; in acid the equilibrium lies left (colour of HIn), in alkali OH⁻ removes H⁺ and it shifts right (colour of In⁻).'),
         ('Explain why an indicator must have a pKa close to the pH at the equivalence point.', 'Its colour change range (≈ pKa ± 1) must lie within the steep part of the pH curve so that it changes colour with a single drop at equivalence.'),
         ('Explain why a solution of sodium ethanoate is alkaline.', 'Ethanoate ions are the conjugate base of a weak acid and accept protons from water: CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻, so [OH⁻] > [H⁺].'),
         ('Explain why iron(III) chloride solution is acidic.', 'The small, highly charged Fe³⁺ ion polarises its water ligands, releasing H⁺: [Fe(H₂O)₆]³⁺ ⇌ [Fe(H₂O)₅OH]²⁺ + H⁺.')],
    contrast=[('the pH curve for a strong acid–strong base titration', 'the pH curve for a weak acid–strong base titration', 'Strong/strong: low start (~1), sharp jump ~3–11 around pH 7; weak/strong: higher start, buffer region, shorter jump ~7–11 with equivalence above 7.'),
              ('the equivalence point', 'the half-equivalence point', 'At equivalence all the acid has been neutralised; at half-equivalence half has, so pH = pKa.')],
    misc=[('All salts dissolve to give neutral solutions.', 'Salts of a weak acid and strong base are basic; salts of a strong acid and weak base are acidic.'),
          ('Any indicator can be used for any titration because they all change colour at pH 7.', 'Each indicator changes colour over its own pH range, which must fall within the vertical section of the curve.')],
    apply=[('Calculate the pH of 0.100 mol dm⁻³ sodium ethanoate (pKa of ethanoic acid 4.76).', 'Kb = 10⁻⁹·²⁴ = 5.75 × 10⁻¹⁰; [OH⁻] = 7.58 × 10⁻⁶; pH = 8.88', 3),
           ('Choose an indicator for HCl titrated with NaOH and explain your choice.', 'Phenolphthalein or methyl orange (or bromothymol blue): the vertical section spans about pH 3–11, covering their ranges', 2)],
    evaluate=[('Indicators are less reliable than pH meters for finding equivalence points.', ['meters give a full curve and objective readings', 'work for coloured solutions and weak/weak titrations'], ['indicators are quick, cheap and accurate when chosen well', 'meters need calibration and careful handling'], 'With the right indicator, accuracy is similar; meters are better for difficult cases.'),
              ('The pH of salt solutions can always be predicted from the parent acid and base.', ['strong/strong neutral, weak acid salt basic, weak base salt acidic'], ['salts of weak acid + weak base depend on relative Ka and Kb', 'highly charged metal ions (Fe³⁺, Al³⁺) give acidic solutions', 'amphiprotic anions (HCO₃⁻, H₂PO₄⁻) need Ka and Kb comparison'], 'The parent acid/base rule works for simple cases but needs Ka/Kb data in general.')],
    extended=[('20.0 cm³ of 0.100 mol dm⁻³ NaOH is titrated into 20.0 cm³ of 0.100 mol dm⁻³ propanoic acid (pKa 4.87). (a) Calculate the initial pH. (b) State the pH at the half-equivalence point. (c) Calculate the pH at the equivalence point. (d) Select a suitable indicator.', '(a) [H⁺] = √(1.35 × 10⁻⁵ × 0.100) → pH 2.94. (b) 4.87. (c) [A⁻] = 0.0500; Kb = 7.41 × 10⁻¹⁰; [OH⁻] = 6.09 × 10⁻⁶; pH 8.78. (d) phenolphthalein.', 8, 'multi_step')],
))


@R.add('ch06-st3', 'C3', (1, 4), 'mcq')
def c3_salt_ph(rng, slot):
    nm, f, kind, why = pick(rng, SALTS)
    base_kind = kind.split(' ')[0]
    stem = pick(rng, [f'Is an aqueous solution of {nm}, {chem(f)}, acidic, neutral or basic?', f'Predict the pH of a 0.1 mol dm⁻³ solution of {chem(f)} relative to 7.'])
    if stem.startswith('Predict'):
        right = {'acidic': 'below 7', 'neutral': 'equal to 7', 'basic': 'above 7'}[base_kind]
        return mcq(rng, stem, right, [x for x in ['below 7', 'equal to 7', 'above 7', 'equal to 14'] if x != right], f'{why}.')
    return mcq(rng, stem, base_kind, [x for x in ['acidic', 'neutral', 'basic', 'amphoteric'] if x != base_kind], f'{why}.')


@R.add('ch06-st3', 'C3', (1, 4), 'mcq')
def c3_indicator_pick(rng, slot):
    kind = pick(rng, ['wa_sb', 'sa_wb', 'sa_sb'])
    if kind == 'wa_sb':
        a = pick(rng, [x[0] for x in WEAK[:6]])
        stem = f'Which indicator is most suitable for the titration of {a} with sodium hydroxide?'
        right = pick(rng, [i for i in INDICATORS if i[1] > 7.5])
        wr = [i for i in INDICATORS if i[1] < 5.5]
    elif kind == 'sa_wb':
        b = pick(rng, [x[0] for x in BASES[:4]])
        stem = f'Which indicator is most suitable for the titration of {b} with hydrochloric acid?'
        right = pick(rng, [i for i in INDICATORS if i[1] < 5.5])
        wr = [i for i in INDICATORS if i[1] > 7.5]
    else:
        return None
    others = [i for i in INDICATORS if i != right and i in wr]
    rng.shuffle(others)
    if len(others) < 3:
        others += [i for i in INDICATORS if i != right and i not in others and abs(i[1] - right[1]) > 2]
    fmt_ = lambda i: f'{i[0]} (pKa {i[1]})'
    return mcq(rng, stem, fmt_(right), [fmt_(i) for i in others[:3]], f'Equivalence pH {"> 7" if kind == "wa_sb" else "< 7"}; {right[0]} changes colour over {right[2]}.')


@R.add('ch06-st3', 'C3', (2, 5), 'numerical')
def c3_salt_ph_calc(rng, slot):
    if rng.random() < 0.6:
        nm, f, cb_, pka = pick(rng, [a for a in WEAK if a[3] < 6])
        c = rng.choice([0.0500, 0.100, 0.200, 0.500])
        kb = KW / 10 ** -pka
        oh = math.sqrt(kb * c)
        phv = 14 + math.log10(oh)
        stem = f'Calculate the pH of a {sf(c)} mol dm⁻³ solution of the sodium salt of {nm} (pKa {pka:.2f}) at 298 K.'
        return num(stem, f'{phv:.2f}', f'pKb = 14.00 − {pka:.2f} = {14 - pka:.2f}; Kb = {sf(kb)} (M1); [OH⁻] = √(Kb × c) = {sf(oh)} (M1); pH = {phv:.2f} (A1).', 3)
    nm, f, ca_, pkb = pick(rng, BASES[:4])
    c = rng.choice([0.0500, 0.100, 0.200, 0.500])
    ka = KW / 10 ** -pkb
    h = math.sqrt(ka * c)
    stem = f'Calculate the pH of a {sf(c)} mol dm⁻³ solution of {nm.replace("amine", "ammonium").replace("ammonia", "ammonium")} chloride, which contains {ionx(ca_)}, the conjugate acid of {nm} (pKb {pkb:.2f}).'
    return num(stem, ph(h), f'pKa = 14.00 − {pkb:.2f} = {14 - pkb:.2f}; Ka = {sf(ka)} (M1); [H⁺] = √(Ka × c) = {sf(h)} (M1); pH = {ph(h)} (A1).', 3)


@R.add('ch06-st3', 'C3', (1, 4), 'mcq')
def c3_ind_colour(rng, slot):
    nm, pk, rngtxt, ca, cb = pick(rng, INDICATORS)
    p = round(rng.choice([pk - 2.5, pk - 2, pk + 2, pk + 2.5]), 1)
    if p < 0 or p > 14:
        return None
    right = ca if p < pk else cb
    opts = list(dict.fromkeys([ca, cb, 'green', 'orange', 'purple', 'colourless', 'pink']))
    wr = [o for o in opts if o != right]
    rng.shuffle(wr)
    stem = f'{cap(nm)} (pKa {pk}) is {ca} in its acid form (HIn) and {cb} in its base form (In⁻). What colour is it in a solution of pH {p}?'
    return mcq(rng, stem, right, wr[:3], f'pH {p} is {"below" if p < pk else "above"} the range {rngtxt}: {"HIn" if p < pk else "In⁻"} dominates → {right}.')


R.mcqs('ch06-st3', 'C2', (1, 4), [
    ('Why does the equivalence point of a weak acid–strong base titration lie above pH 7?', 'The conjugate base of the weak acid reacts with water to produce OH⁻.', ['Excess NaOH is always present.', 'Weak acids are basic.', 'Water dissociates more.'], 'A⁻ hydrolysis.'),
    ('Why is the vertical section of a pH curve shorter for a weak acid with a strong base?', 'The starting pH is higher and the buffer region raises the pH before equivalence.', ['Less base is needed.', 'The acid is more concentrated.', 'The reaction is slower.'], 'Starts ~pH 3 not 1.'),
    ('Why does an indicator change colour over a range of about two pH units?', 'The eye detects one colour when one form is about ten times the other.', ['Indicators are strong acids.', 'Two protons are lost.', 'The temperature changes.'], 'pKa ± 1.'),
    ('Why is aluminium chloride solution acidic?', 'The hydrated Al³⁺ ion releases H⁺ from its water ligands.', ['Chloride ions are acidic.', 'Aluminium reacts with water to give H₂.', 'It contains HCl.'], 'Hydrated cation hydrolysis.'),
])


# ---- ch06-st4 Lewis acids and bases ----
LEWIS = [('BF₃ + NH₃ → F₃B–NH₃', 'BF₃', 'NH₃'), ('AlCl₃ + Cl⁻ → AlCl₄⁻', 'AlCl₃', 'Cl⁻'), ('Cu²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺', 'Cu²⁺', 'NH₃'),
         ('H⁺ + H₂O → H₃O⁺', 'H⁺', 'H₂O'), ('Fe³⁺ + 6H₂O → [Fe(H₂O)₆]³⁺', 'Fe³⁺', 'H₂O'), ('Ag⁺ + 2NH₃ → [Ag(NH₃)₂]⁺', 'Ag⁺', 'NH₃'),
         ('CO₂ + OH⁻ → HCO₃⁻', 'CO₂', 'OH⁻'), ('BCl₃ + (CH₃)₃N → Cl₃B–N(CH₃)₃', 'BCl₃', '(CH₃)₃N'), ('Co²⁺ + 4Cl⁻ → [CoCl₄]²⁻', 'Co²⁺', 'Cl⁻'),
         ('FeBr₃ + Br₂ → FeBr₄⁻ + Br⁺', 'FeBr₃', 'Br₂'), ('H⁺ + NH₃ → NH₄⁺', 'H⁺', 'NH₃'), ('SO₃ + H₂O → H₂SO₄', 'SO₃', 'H₂O'),
         ('Ni²⁺ + 6NH₃ → [Ni(NH₃)₆]²⁺', 'Ni²⁺', 'NH₃'), ('CH₃⁺ + Cl⁻ → CH₃Cl', 'CH₃⁺', 'Cl⁻'), ('Zn²⁺ + 4OH⁻ → [Zn(OH)₄]²⁻', 'Zn²⁺', 'OH⁻')]

R.facts('ch06-st4', F(
    terms=[('Lewis acid', 'an electron-pair acceptor'),
           ('Lewis base', 'an electron-pair donor'),
           ('coordination bond', 'a covalent bond in which both electrons are provided by one atom (the Lewis base)'),
           ('nucleophile', 'an electron-rich species that donates a pair of electrons to an electron-deficient centre; a Lewis base'),
           ('electrophile', 'an electron-deficient species that accepts a pair of electrons; a Lewis acid'),
           ('adduct', 'the product formed when a Lewis acid and a Lewis base combine through a coordination bond')],
    facts=[('In BF₃ + NH₃ → F₃B–NH₃, what is the role of BF₃?', 'Lewis acid', ['Lewis base', 'Brønsted–Lowry acid', 'Brønsted–Lowry base'], 'Accepts N lone pair.'),
           ('Which species can act as a Lewis base?', 'NH₃', ['BF₃', 'AlCl₃', 'H⁺'], 'Lone pair on N.'),
           ('Why is every Brønsted–Lowry base also a Lewis base?', 'Accepting a proton requires donating a lone pair to it.', ['It contains OH⁻.', 'It is always charged.', 'It has an incomplete octet.'], 'Lone pair needed.'),
           ('What type of bond forms between a ligand and a metal ion in a complex?', 'a coordination (dative covalent) bond', ['an ionic bond', 'a hydrogen bond', 'a metallic bond'], 'Ligand donates pair.'),
           ('Which species is a Lewis acid but not a Brønsted–Lowry acid?', 'AlCl₃', ['HCl', 'NH₄⁺', 'H₂O'], 'No proton to donate.'),
           ('In complex ions, transition metal ions act as', 'Lewis acids', ['Lewis bases', 'Brønsted–Lowry bases', 'reducing agents only'], 'Accept lone pairs.')],
    why=[('Explain why BF₃ acts as a Lewis acid.', 'Boron has only six electrons in its valence shell (incomplete octet) and an empty p orbital, so it can accept a lone pair, e.g. from NH₃.'),
         ('Explain why the Lewis theory is broader than the Brønsted–Lowry theory.', 'It defines acids and bases by electron-pair transfer rather than proton transfer, so it includes reactions with no protons, such as BF₃ + NH₃ and complex ion formation.'),
         ('Explain the relationship between nucleophiles and Lewis bases.', 'Nucleophiles donate an electron pair to an electron-deficient carbon or other centre, which is exactly the definition of a Lewis base.'),
         ('Explain why water can act as a Lewis base towards metal ions.', 'The oxygen atom of water has two lone pairs; one can be donated to an empty orbital of a metal ion, forming a coordination bond (aqua complex).')],
    contrast=[('a Lewis acid', 'a Brønsted–Lowry acid', 'A Lewis acid accepts an electron pair; a Brønsted–Lowry acid donates a proton (H⁺ itself is the Lewis acid in that case).'),
              ('a Lewis base', 'a nucleophile', 'Both donate an electron pair; "nucleophile" is used in organic mechanisms for attack on electron-deficient carbon, while "Lewis base" is the general term.')],
    misc=[('A Lewis acid must contain hydrogen.', 'A Lewis acid is any electron-pair acceptor (BF₃, AlCl₃, metal ions) – no hydrogen is needed.'),
          ('NH₄⁺ is a Lewis base because it contains nitrogen.', 'In NH₄⁺ all the nitrogen’s electrons are used in bonds; it has no lone pair and cannot act as a Lewis base.')],
    apply=[('Identify the Lewis acid and Lewis base in Cu²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺ and describe the bond formed.', 'Cu²⁺ Lewis acid, NH₃ Lewis base; coordination bonds from N lone pairs to Cu²⁺', 2),
           ('Explain, with an equation, why AlCl₃ is used as a catalyst in the chlorination of benzene.', 'AlCl₃ (Lewis acid) accepts a lone pair from Cl₂: AlCl₃ + Cl₂ → AlCl₄⁻ + Cl⁺, generating the electrophile', 3)],
    evaluate=[('The Lewis definition makes the Brønsted–Lowry definition unnecessary.', ['Lewis includes all Brønsted–Lowry reactions and many more', 'unifies acid–base, complex formation and organic mechanisms'], ['Brønsted–Lowry is simpler and quantitative (pH, Ka) for aqueous chemistry', 'Lewis strength has no single scale'], 'Lewis theory is more general, but Brønsted–Lowry remains the practical framework for aqueous equilibria.'),
              ('Classifying a species as a Lewis acid or base is always clear-cut.', ['electron-pair donors/acceptors are usually easy to identify'], ['some species (H₂O, Al(OH)₃, SO₂) act as either depending on the partner', 'reactions such as FeBr₃ + Br₂ involve partial transfer'], 'Classification depends on the reaction, not just on the species.')],
    extended=[('Ammonia reacts with boron trifluoride and with hydrogen chloride. (a) Write equations for both reactions. (b) Classify each reactant using both Lewis and Brønsted–Lowry theories. (c) Draw the Lewis structure of the product F₃B–NH₃ and state the shapes around B and N. (d) Explain why BF₃ cannot act as a Brønsted–Lowry acid.', '(a) NH₃ + BF₃ → F₃B–NH₃; NH₃ + HCl → NH₄Cl. (b) NH₃ Lewis base in both and B–L base with HCl; BF₃ Lewis acid only; HCl B–L acid (H⁺ is Lewis acid). (c) coordination bond N→B; tetrahedral at both B and N. (d) it has no proton to donate.', 7, 'multi_step')],
))


@R.add('ch06-st4', 'C3', (1, 4), 'mcq')
def c3_lewis_role(rng, slot):
    eq, acid, base = pick(rng, LEWIS)
    kind = rng.choice(['acid', 'base'])
    right = acid if kind == 'acid' else base
    other = base if kind == 'acid' else acid
    prods = eq.split('→')[1].strip().split(' + ')
    wr = [other] + prods
    wr += ['H₂O' if 'H₂O' not in (acid, base) else 'OH⁻']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'Which species acts as a Lewis {kind} in the reaction {eq}?'
    return mcq(rng, stem, right, wr[:3], f'{base} donates an electron pair to {acid} ({"acceptor" if kind == "acid" else "donor"} = {right}).')


@R.add('ch06-st4', 'C3', (1, 4), 'mcq')
def c3_lewis_pick(rng, slot):
    acids_ = ['BF₃', 'AlCl₃', 'BCl₃', 'Fe³⁺', 'Cu²⁺', 'H⁺', 'Ag⁺', 'FeBr₃', 'Co²⁺', 'Zn²⁺']
    bases_ = ['NH₃', 'H₂O', 'Cl⁻', 'OH⁻', 'CN⁻', 'CH₃NH₂', 'F⁻', '(CH₃)₃N']
    kind = rng.choice(['acid', 'base'])
    right = pick(rng, acids_ if kind == 'acid' else bases_)
    wr = rng.sample(bases_ if kind == 'acid' else acids_, 3)
    stem = f'Which of {_lst(sorted([right] + wr))} can act only as a Lewis {kind}?'
    return mcq(rng, stem, right, wr, f'{right} {"has an empty orbital to accept a pair" if kind == "acid" else "has a lone pair to donate"}; the others are {"electron-pair donors" if kind == "acid" else "electron-pair acceptors"}.')


@R.add('ch06-st4', 'C3', (1, 5), 'short')
def c3_lewis_short(rng, slot):
    eq, acid, base = pick(rng, LEWIS)
    stem = pick(rng, [f'For the reaction {eq}, identify the Lewis acid and the Lewis base, and state the type of bond formed.', f'Classify the reactants in {eq} using Lewis theory and explain your answer.'])
    return dict(stem=stem, answer=f'Lewis acid {acid}; Lewis base {base}; coordination bond', markingKey=f'{acid} accepts an electron pair – Lewis acid (1); {base} donates a lone pair – Lewis base (1); coordination (dative) bond formed (1).', type='short', marks=3)


R.mcqs('ch06-st4', 'C2', (1, 4), [
    ('Why is H⁺ described as a Lewis acid?', 'It has an empty 1s orbital and accepts a lone pair.', ['It donates a proton.', 'It has a lone pair.', 'It is positively charged only.'], 'Electron-pair acceptor.'),
    ('Why can transition metal ions form complexes with several ligands?', 'They have empty orbitals that can accept lone pairs from ligands.', ['They have many lone pairs.', 'They are Lewis bases.', 'They form ionic bonds with ligands.'], 'Lewis acids.'),
    ('Why is a nucleophile considered a Lewis base?', 'It donates an electron pair to form a new bond.', ['It accepts electrons.', 'It is always negative.', 'It contains a proton.'], 'Electron-pair donor.'),
    ('Which statement explains why the Lewis theory is more general?', 'It includes reactions that do not involve proton transfer.', ['It only applies to aqueous solutions.', 'It only applies to metals.', 'It requires H⁺ ions.'], 'e.g. BF₃ + NH₃.'),
])


@p1b(R, 'ch06-st2')
def p1b_buffer_pka(rng, slot):
    nm, f, cb_, pka = pick(rng, [a for a in WEAK if a[3] < 6])
    ratios = [0.25, 0.5, 1.0, 2.0, 4.0]
    rows = [(r, round(pka + math.log10(r) + rng.uniform(-0.03, 0.03), 2)) for r in ratios]
    tab = '\n'.join(f'{r:.2f} | {math.log10(r):.2f} | {p:.2f}' for r, p in rows)
    intro = (f'A student made a series of buffers from 0.100 mol dm⁻³ {nm} and 0.100 mol dm⁻³ of its sodium salt in different volume ratios and measured the pH of each with a calibrated pH meter (±0.01).\n\n'
             f'[A⁻]/[HA] | log([A⁻]/[HA]) | pH\n{tab}')
    mid = [p for r, p in rows if r == 1.0][0]
    g = (rows[-1][1] - rows[0][1]) / (math.log10(rows[-1][0]) - math.log10(rows[0][0]))
    return dict(intro=intro, parts=[
        ('State the relationship that predicts a straight-line graph of pH against log([A⁻]/[HA]), and the expected gradient.', 'pH = pKa + log([A⁻]/[HA]); gradient = 1', 'Henderson–Hasselbalch (1); gradient 1 (1).', 2),
        ('Determine the gradient from the first and last data points and comment on it.', f'{g:.2f} – close to the theoretical value of 1', f'({rows[-1][1]:.2f} − {rows[0][1]:.2f})/({math.log10(4):.2f} − ({math.log10(0.25):.2f})) = {g:.2f} (A1); ≈ 1, supports model (R1).', 2),
        (f'Deduce the pKa of {nm} from the data.', f'{mid:.2f} (y-intercept, where the ratio is 1)', f'pKa = pH when log ratio = 0: {mid:.2f} (A1).', 1),
        (f'The data-booklet pKa is {pka:.2f}. Calculate the percentage error in the student’s value.', f'{abs(mid - pka) / pka * 100:.1f} %', f'|{mid:.2f} − {pka:.2f}|/{pka:.2f} × 100 = {abs(mid - pka) / pka * 100:.1f} % (A1).', 1),
        ('Explain why diluting each buffer tenfold would have little effect on the results.', 'The ratio [A⁻]/[HA] is unchanged by dilution, so the pH remains almost the same.', 'Ratio constant (1); pH depends on ratio (1).', 2)],
        extras=[('Suggest why the pH meter was rinsed with distilled water between readings.', 'To avoid carrying over solution that would change the next buffer’s composition.', 'Prevents cross-contamination (1).', 1)])


# =============================================================================================
# ch07 R3.2 Electron transfer reactions
# =============================================================================================
HALF = [  # reduction half-equation, oxidised species, reduced species, electrons
    ('MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ → Mn²⁺(aq) + 4H₂O(l)', 'MnO₄⁻', 'Mn²⁺', 5),
    ('Cr₂O₇²⁻(aq) + 14H⁺(aq) + 6e⁻ → 2Cr³⁺(aq) + 7H₂O(l)', 'Cr₂O₇²⁻', 'Cr³⁺', 6),
    ('H₂O₂(aq) + 2H⁺(aq) + 2e⁻ → 2H₂O(l)', 'H₂O₂', 'H₂O', 2),
    ('O₂(g) + 4H⁺(aq) + 4e⁻ → 2H₂O(l)', 'O₂', 'H₂O', 4),
    ('NO₃⁻(aq) + 4H⁺(aq) + 3e⁻ → NO(g) + 2H₂O(l)', 'NO₃⁻', 'NO', 3),
    ('SO₄²⁻(aq) + 4H⁺(aq) + 2e⁻ → SO₂(g) + 2H₂O(l)', 'SO₄²⁻', 'SO₂', 2),
    ('VO₂⁺(aq) + 2H⁺(aq) + e⁻ → VO²⁺(aq) + H₂O(l)', 'VO₂⁺', 'VO²⁺', 1),
    ('IO₃⁻(aq) + 6H⁺(aq) + 5e⁻ → ½I₂(aq) + 3H₂O(l)', 'IO₃⁻', 'I₂', 5),
    ('MnO₂(s) + 4H⁺(aq) + 2e⁻ → Mn²⁺(aq) + 2H₂O(l)', 'MnO₂', 'Mn²⁺', 2),
    ('Fe³⁺(aq) + e⁻ → Fe²⁺(aq)', 'Fe³⁺', 'Fe²⁺', 1),
    ('I₂(aq) + 2e⁻ → 2I⁻(aq)', 'I₂', 'I⁻', 2),
    ('S₄O₆²⁻(aq) + 2e⁻ → 2S₂O₃²⁻(aq)', 'S₄O₆²⁻', 'S₂O₃²⁻', 2),
    ('Cl₂(g) + 2e⁻ → 2Cl⁻(aq)', 'Cl₂', 'Cl⁻', 2),
    ('2CO₂(g) + 2e⁻ → C₂O₄²⁻(aq)', 'CO₂', 'C₂O₄²⁻', 2),
]
REDOX_RX = [  # equation, oxidising agent, reducing agent, species oxidised, species reduced
    ('Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)', 'Cu²⁺', 'Zn'), ('Cl₂(aq) + 2Br⁻(aq) → 2Cl⁻(aq) + Br₂(aq)', 'Cl₂', 'Br⁻'),
    ('2Fe³⁺(aq) + 2I⁻(aq) → 2Fe²⁺(aq) + I₂(aq)', 'Fe³⁺', 'I⁻'), ('MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 'MnO₄⁻', 'Fe²⁺'),
    ('Cr₂O₇²⁻ + 6I⁻ + 14H⁺ → 2Cr³⁺ + 3I₂ + 7H₂O', 'Cr₂O₇²⁻', 'I⁻'), ('Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g)', 'H⁺', 'Mg'),
    ('2Al(s) + Fe₂O₃(s) → Al₂O₃(s) + 2Fe(l)', 'Fe₂O₃', 'Al'), ('CuO(s) + H₂(g) → Cu(s) + H₂O(g)', 'CuO', 'H₂'),
    ('I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻', 'I₂', 'S₂O₃²⁻'), ('2MnO₄⁻ + 5H₂O₂ + 6H⁺ → 2Mn²⁺ + 5O₂ + 8H₂O', 'MnO₄⁻', 'H₂O₂'),
    ('Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)', 'Ag⁺', 'Cu'), ('Fe₂O₃(s) + 3CO(g) → 2Fe(s) + 3CO₂(g)', 'Fe₂O₃', 'CO'),
    ('2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O', 'MnO₄⁻', 'C₂O₄²⁻'), ('Br₂(aq) + 2I⁻(aq) → 2Br⁻(aq) + I₂(aq)', 'Br₂', 'I⁻')]

R.facts('ch07-st1', F(
    terms=[('oxidation', 'loss of electrons, or an increase in oxidation state'),
           ('reduction', 'gain of electrons, or a decrease in oxidation state'),
           ('oxidising agent', 'a species that oxidises another species and is itself reduced (an electron acceptor)'),
           ('reducing agent', 'a species that reduces another species and is itself oxidised (an electron donor)'),
           ('half-equation', 'an equation showing either the oxidation or the reduction part of a redox reaction, including electrons'),
           ('disproportionation', 'a redox reaction in which the same element is simultaneously oxidised and reduced')],
    facts=[('In Zn + Cu²⁺ → Zn²⁺ + Cu, which species is the oxidising agent?', 'Cu²⁺', ['Zn', 'Zn²⁺', 'Cu'], 'Cu²⁺ gains electrons.'),
           ('What is the oxidation state of sulfur in H₂SO₄?', '+6', ['+4', '+2', '−2'], '2(+1) + x + 4(−2) = 0.'),
           ('What is the oxidation state of oxygen in H₂O₂?', '−1', ['−2', '0', '+1'], 'Peroxide.'),
           ('Which change is a reduction?', 'Cr₂O₇²⁻ → Cr³⁺', ['Fe²⁺ → Fe³⁺', 'I⁻ → I₂', 'Mg → Mg²⁺'], 'Cr +6 → +3.'),
           ('What is the oxidation state of any element in its uncombined state?', '0', ['+1', '−1', 'equal to its group number'], 'Elements = 0.'),
           ('Which reaction is a disproportionation?', 'Cl₂ + 2NaOH → NaCl + NaClO + H₂O', ['Zn + 2HCl → ZnCl₂ + H₂', 'CuO + H₂ → Cu + H₂O', 'NaOH + HCl → NaCl + H₂O'], 'Cl 0 → −1 and +1.')],
    why=[('Explain why oxidation and reduction always occur together.', 'Electrons lost by one species must be gained by another; electrons cannot exist free in solution, so an oxidation is always accompanied by a reduction.'),
         ('Explain how to balance a half-equation in acidic solution.', 'Balance the element changing oxidation state, add H₂O to balance O, add H⁺ to balance H, then add electrons to balance charge.'),
         ('Explain why oxidation states are useful even for covalent compounds.', 'They allow electron transfer to be tracked in any reaction by treating bonds as ionic, so redox can be identified and equations balanced.'),
         ('Explain why the number of electrons must be equal when combining two half-equations.', 'The electrons released in oxidation must all be accepted in reduction; multiplying half-equations to equalise electrons ensures no free electrons appear in the overall equation.')],
    contrast=[('oxidation', 'reduction', 'Oxidation is electron loss (oxidation state increases); reduction is electron gain (oxidation state decreases).'),
              ('an oxidising agent', 'a reducing agent', 'An oxidising agent accepts electrons and is reduced; a reducing agent donates electrons and is oxidised.')],
    misc=[('The oxidising agent is the species that is oxidised.', 'The oxidising agent is itself reduced; it causes another species to be oxidised.'),
          ('Oxygen always has an oxidation state of −2.', 'Oxygen is −1 in peroxides (H₂O₂), +2 in OF₂ and 0 in O₂.'),
          ('In a half-equation, electrons are always written on the right.', 'Electrons appear on the left in a reduction and on the right in an oxidation.')],
    apply=[('Write a balanced half-equation for the oxidation of Fe²⁺ to Fe³⁺ and combine it with MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O.', 'Fe²⁺ → Fe³⁺ + e⁻; MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 3),
           ('Deduce the oxidation states of nitrogen in NH₃, N₂, NO and NO₃⁻.', '−3, 0, +2, +5', 2)],
    evaluate=[('Defining redox in terms of oxidation states is better than in terms of oxygen or hydrogen transfer.', ['applies to all redox reactions, including those without O or H', 'allows equations to be balanced systematically'], ['oxidation states are formal and not real charges', 'oxygen/hydrogen definitions are intuitive for combustion and organic redox'], 'Oxidation states give the most general definition, while older definitions are useful special cases.'),
              ('Half-equations represent what actually happens in a redox reaction.', ['in electrochemical cells the half-reactions really occur at separate electrodes', 'they show the electron transfer clearly'], ['in solution the electron transfer may be direct and via intermediates', 'species like "H⁺" and free electrons are simplifications'], 'They are a powerful bookkeeping model and are real in cells, but simplify the mechanism in solution.')],
    extended=[('Acidified potassium dichromate(VI) oxidises ethanol to ethanal. (a) Write the half-equation for the reduction of Cr₂O₇²⁻ to Cr³⁺. (b) Write the half-equation for the oxidation of C₂H₅OH to CH₃CHO. (c) Combine them into an overall equation. (d) State the colour change and the change in oxidation state of chromium.', '(a) Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O. (b) C₂H₅OH → CH₃CHO + 2H⁺ + 2e⁻. (c) Cr₂O₇²⁻ + 3C₂H₅OH + 8H⁺ → 2Cr³⁺ + 3CH₃CHO + 7H₂O. (d) orange to green; +6 → +3.', 8, 'multi_step')],
))


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3_redox_agent(rng, slot):
    eq, ox, red = pick(rng, REDOX_RX)
    kind = pick(rng, ['oxidising agent', 'reducing agent', 'species oxidised', 'species reduced'])
    right = ox if kind in ('oxidising agent', 'species reduced') else red
    other = red if right == ox else ox
    prods = [p.strip().split('(')[0].lstrip('0123456789') for p in eq.split('→')[1].split(' + ')]
    wr = [other] + [p for p in prods if p not in ('H₂O', right)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        wr.append('H⁺' if 'H⁺' not in (right,) else 'H₂O')
    stem = f'In the reaction {eq}, which is the {kind}?'
    return mcq(rng, stem, right, wr[:3], f'{ox} gains electrons (is reduced, the oxidising agent); {red} loses electrons (is oxidised, the reducing agent).')


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3_half_e(rng, slot):
    eqn, o, r, n = pick(rng, HALF)
    stem = pick(rng, [f'How many electrons are needed to balance the half-equation for the reduction of {o} to {r} in acidic solution?', f'In the balanced reduction half-equation {o} → {r} (acidic solution), how many electrons appear?'])
    wr = [str(x) for x in sorted({n - 1, n + 1, n + 2, 2 * n, 8} - {n}) if x > 0]
    rng.shuffle(wr)
    return mcq(rng, stem, str(n), wr[:3], f'{eqn}.')


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3_ox_change(rng, slot):
    pairs = [('MnO4^-', 'Mn^2+', 'Mn', 7, 2), ('Cr2O7^2-', 'Cr^3+', 'Cr', 6, 3), ('NO3^-', 'NO2', 'N', 5, 4), ('NO3^-', 'NO', 'N', 5, 2), ('SO4^2-', 'SO2', 'S', 6, 4),
             ('Fe^2+', 'Fe^3+', 'Fe', 2, 3), ('I^-', 'I2', 'I', -1, 0), ('H2O2', 'O2', 'O', -1, 0), ('H2O2', 'H2O', 'O', -1, -2), ('S2O3^2-', 'S4O6^2-', 'S', 2, 2.5),
             ('Cl2', 'ClO^-', 'Cl', 0, 1), ('NH3', 'NO', 'N', -3, 2), ('ClO3^-', 'Cl^-', 'Cl', 5, -1), ('VO2^+', 'VO^2+', 'V', 5, 4)]
    a, b, el, x1, x2 = pick(rng, pairs)
    if x2 == 2.5:
        return None
    kind = 'oxidation' if x2 > x1 else 'reduction'
    right = f'{oxs(x1)} to {oxs(x2)}, {kind}'
    wr = [f'{oxs(x2)} to {oxs(x1)}, {"reduction" if kind == "oxidation" else "oxidation"}', f'{oxs(x1)} to {oxs(x2)}, {"reduction" if kind == "oxidation" else "oxidation"}', f'{oxs(x1)} to {oxs(x1 + (1 if x2 > x1 else -1) * (abs(x2 - x1) + 1))}, {kind}']
    stem = f'When {chem(a)} is converted to {chem(b)}, how does the oxidation state of {ENAME.get(el, el)} change?'
    return mcq(rng, stem, right, [w for w in dict.fromkeys(wr) if w != right][:3], f'{el}: {oxs(x1)} in {chem(a)}, {oxs(x2)} in {chem(b)} → {kind}.')


@R.add('ch07-st1', 'C3', (1, 5), 'short')
def c3_ox_state_short(rng, slot):
    f, el, ox = pick(rng, [s for s in OX_SPECIES if s[2] is not None])
    stem = pick(rng, [f'Deduce the oxidation state of {ENAME[el]} in {chem(f)}, showing your working.', f'State the oxidation state of {el} in {chem(f)} and name the species using Roman numerals where appropriate.'])
    return dict(stem=stem, answer=oxs(ox), markingKey=f'Sum of oxidation states = overall charge with O −2 (−1 in peroxides), H +1, K +1 (M1); {el} = {oxs(ox)} (A1).', type='short', marks=2)


R.mcqs('ch07-st1', 'C2', (1, 4), [
    ('Why is the reaction 2Na + Cl₂ → 2NaCl a redox reaction?', 'Sodium loses electrons and chlorine gains them.', ['A salt is formed.', 'It is exothermic.', 'Oxygen is transferred.'], 'Electron transfer.'),
    ('Why is H⁺ added to the left side of the half-equation for MnO₄⁻ → Mn²⁺?', 'To combine with oxide oxygen to form water and balance H.', ['To act as a catalyst.', 'To balance the electrons.', 'Because MnO₄⁻ is a base.'], 'Acidic conditions.'),
    ('Which statement about a reducing agent is correct?', 'It donates electrons and its oxidation state increases.', ['It accepts electrons.', 'Its oxidation state decreases.', 'It is always a non-metal.'], 'Reducing agent is oxidised.'),
    ('Why is NaOH + HCl → NaCl + H₂O not a redox reaction?', 'No element changes its oxidation state.', ['No electrons exist in it.', 'It is exothermic.', 'Water is formed.'], 'All oxidation states unchanged.'),
])


# ---- ch07-st2 reactivity, halogens, redox titrations ----
METALS_RS = ['K', 'Na', 'Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'Cu', 'Ag', 'Au']
ION_OF = {'K': 'K⁺', 'Na': 'Na⁺', 'Ca': 'Ca²⁺', 'Mg': 'Mg²⁺', 'Al': 'Al³⁺', 'Zn': 'Zn²⁺', 'Fe': 'Fe²⁺', 'Ni': 'Ni²⁺', 'Sn': 'Sn²⁺', 'Pb': 'Pb²⁺', 'Cu': 'Cu²⁺', 'Ag': 'Ag⁺', 'Au': 'Au³⁺'}
SALT_OF = {'Zn': 'zinc sulfate', 'Fe': 'iron(II) sulfate', 'Ni': 'nickel(II) sulfate', 'Sn': 'tin(II) chloride', 'Pb': 'lead(II) nitrate', 'Cu': 'copper(II) sulfate', 'Ag': 'silver nitrate', 'Mg': 'magnesium sulfate', 'Al': 'aluminium sulfate'}
HALOGENS = ['F', 'Cl', 'Br', 'I']
HAL_COL = {'Cl': 'pale green', 'Br': 'orange/yellow-brown', 'I': 'brown (purple in hexane)'}
TITR = [  # oxidant, reductant, mole ratio ox:red, equation, oxidant name, reductant name
    ('MnO₄⁻', 'Fe²⁺', (1, 5), 'MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 'potassium manganate(VII)', 'iron(II) sulfate'),
    ('Cr₂O₇²⁻', 'Fe²⁺', (1, 6), 'Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O', 'potassium dichromate(VI)', 'iron(II) ammonium sulfate'),
    ('MnO₄⁻', 'C₂O₄²⁻', (2, 5), '2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O', 'potassium manganate(VII)', 'sodium ethanedioate'),
    ('MnO₄⁻', 'H₂O₂', (2, 5), '2MnO₄⁻ + 5H₂O₂ + 6H⁺ → 2Mn²⁺ + 5O₂ + 8H₂O', 'potassium manganate(VII)', 'hydrogen peroxide'),
    ('I₂', 'S₂O₃²⁻', (1, 2), 'I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻', 'iodine', 'sodium thiosulfate'),
]

R.facts('ch07-st2', F(
    terms=[('activity series', 'a list of metals in order of their reactivity (ease of losing electrons to form positive ions)'),
           ('displacement reaction', 'a reaction in which a more reactive element displaces a less reactive one from a compound'),
           ('redox titration', 'a titration in which an oxidising agent reacts with a reducing agent, often with a self-indicating reagent such as MnO₄⁻'),
           ('self-indicating', 'describes a titrant whose own colour change shows the end point, e.g. purple MnO₄⁻ becoming colourless Mn²⁺'),
           ('iodometric titration', 'an analysis in which an oxidant liberates I₂ from excess I⁻, and the I₂ is titrated with thiosulfate using starch')],
    facts=[('Which metal will displace copper from copper(II) sulfate solution?', 'zinc', ['silver', 'gold', 'platinum'], 'Zn above Cu.'),
           ('Which halogen is the strongest oxidising agent?', 'fluorine', ['chlorine', 'bromine', 'iodine'], 'Most electronegative, most readily reduced.'),
           ('What colour change is seen at the end point when MnO₄⁻ is added to Fe²⁺(aq)?', 'colourless to permanent pale pink', ['purple to colourless', 'orange to green', 'blue to colourless'], 'First excess MnO₄⁻.'),
           ('What is used as the indicator in iodine–thiosulfate titrations?', 'starch', ['phenolphthalein', 'methyl orange', 'no indicator is needed'], 'Blue-black with I₂.'),
           ('What is observed when chlorine water is added to potassium bromide solution?', 'the solution turns orange/yellow-brown', ['no change', 'a white precipitate forms', 'the solution turns purple'], 'Br₂ formed.'),
           ('Which metal reacts with cold water to produce hydrogen?', 'sodium', ['copper', 'iron', 'silver'], 'Very reactive.')],
    why=[('Explain why reactivity of the halogens decreases down group 17.', 'Atoms get larger, so the incoming electron is further from the nucleus and more shielded; the attraction for an extra electron decreases, making them weaker oxidising agents.'),
         ('Explain why magnesium displaces copper from copper(II) sulfate solution.', 'Magnesium is more reactive: it loses electrons more readily, reducing Cu²⁺ to Cu while being oxidised to Mg²⁺.'),
         ('Explain why potassium manganate(VII) titrations are carried out in excess dilute sulfuric acid.', 'H⁺ is needed for MnO₄⁻ to be reduced to Mn²⁺; H₂SO₄ is used because HCl would be oxidised to Cl₂ and HNO₃ is itself an oxidant.'),
         ('Explain why starch is added only near the end point in an iodine–thiosulfate titration.', 'If added when much iodine is present, a stable starch–iodine complex forms that releases iodine slowly, making the end point inaccurate.')],
    contrast=[('a more reactive metal', 'a less reactive metal', 'A more reactive metal loses electrons more readily (stronger reducing agent) and displaces less reactive metals from their salts.'),
              ('an acid–base titration', 'a redox titration', 'An acid–base titration involves proton transfer and usually needs an added indicator; a redox titration involves electron transfer and may be self-indicating.')],
    misc=[('Iodine displaces chlorine from sodium chloride solution.', 'Iodine is a weaker oxidising agent than chlorine and cannot oxidise Cl⁻; no reaction occurs.'),
          ('In a manganate(VII) titration the end point is when the solution becomes colourless.', 'MnO₄⁻ is decolourised while Fe²⁺ remains; the end point is the first permanent pale pink colour.')],
    apply=[('Write an ionic equation for the reaction of zinc with silver nitrate solution and identify the reducing agent.', 'Zn + 2Ag⁺ → Zn²⁺ + 2Ag; zinc', 2),
           ('Predict whether bromine reacts with potassium iodide solution. Write an ionic equation if it does.', 'Yes: Br₂ + 2I⁻ → 2Br⁻ + I₂', 2)],
    evaluate=[('Redox titrations are more useful than acid–base titrations in analysis.', ['determine iron in tablets, ores, vitamin C, dissolved oxygen, chlorine in bleach', 'often self-indicating'], ['many analytes are acids or bases', 'reagents such as MnO₄⁻ must be standardised and are unstable', 'side reactions can interfere'], 'Both are essential; the choice depends on whether the analyte is a redox or acid–base species.'),
              ('The activity series can be explained entirely by ionisation energies.', ['metals with lower IE generally lose electrons more easily'], ['in water, hydration enthalpy and atomisation also matter (Li is very reactive in water despite higher IE than Cs)', 'standard electrode potentials give a better measure'], 'IE is part of the explanation, but E⦵ values account for all the energy terms in solution.')],
    extended=[('An iron tablet of mass 0.950 g was dissolved in dilute sulfuric acid and titrated with 0.0200 mol dm⁻³ KMnO₄; 23.50 cm³ was needed. (a) Write the ionic equation. (b) Calculate the amount of Fe²⁺. (c) Calculate the percentage by mass of iron in the tablet. (d) Explain why the titration is self-indicating.', '(a) MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O. (b) 4.70 × 10⁻⁴ × 5 = 2.35 × 10⁻³ mol. (c) 0.131 g; 13.8 %. (d) purple MnO₄⁻ is decolourised until Fe²⁺ is used up; the first excess gives a permanent pink.', 8, 'multi_step')],
))


@R.add('ch07-st2', 'C3', (1, 4), 'mcq')
def c3_displace(rng, slot):
    a, b = rng.sample(METALS_RS[3:12], 2)
    if b not in SALT_OF:
        return None
    reacts = METALS_RS.index(a) < METALS_RS.index(b)
    right = f'Yes: {a} + {ION_OF[b]} → {ION_OF[a]} + {b} (balanced appropriately)' if reacts else 'No reaction occurs.'
    stem = f'A piece of {ENAME[a]} is placed in {SALT_OF[b]} solution. Does a displacement reaction occur?'
    wr = ['No reaction occurs.' if reacts else f'Yes: {a} + {ION_OF[b]} → {ION_OF[a]} + {b} (balanced appropriately)', f'Yes: {b} + {ION_OF[a]} → {ION_OF[b]} + {a} (balanced appropriately)', f'Yes: hydrogen gas is produced from the {SALT_OF[b]}']
    return mcq(rng, stem, right, wr, f'{ENAME[a]} is {"more" if reacts else "less"} reactive than {ENAME[b]}.')


@R.add('ch07-st2', 'C3', (1, 4), 'mcq')
def c3_halogen_disp(rng, slot):
    x, y = rng.sample(['Cl', 'Br', 'I'], 2)
    reacts = HALOGENS.index(x) < HALOGENS.index(y)
    salt = pick(rng, ['potassium', 'sodium'])
    hal = {'Cl': 'chloride', 'Br': 'bromide', 'I': 'iodide'}
    elem = {'Cl': 'chlorine water', 'Br': 'bromine water', 'I': 'iodine solution'}
    stem = f'{cap(elem[x])} is added to aqueous {salt} {hal[y]}. What is observed?'
    right = f'the solution turns {HAL_COL[y]}' if reacts else 'no reaction; the colour of the added halogen remains'
    wr = [f'the solution turns {HAL_COL[z]}' for z in ('Cl', 'Br', 'I') if z not in (y,) and f'the solution turns {HAL_COL[z]}' != right] + ['no reaction; the colour of the added halogen remains', 'a white precipitate forms']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    return mcq(rng, stem, right, wr[:3], f'{ENAME[x]} is {"a stronger" if reacts else "a weaker"} oxidising agent than {ENAME[y]}' + (f': {x}₂ + 2{y}⁻ → 2{x}⁻ + {y}₂.' if reacts else '.'))


@R.add('ch07-st2', 'C3', (2, 5), 'numerical')
def c3_redox_titr(rng, slot):
    ox, red, (a, b), eq, oxn, redn = pick(rng, TITR)
    c_ox = rng.choice([0.0100, 0.0200, 0.0250, 0.0500, 0.100])
    v_ox = round(rng.uniform(15.0, 28.0), 2)
    v_red = rng.choice([10.0, 20.0, 25.0])
    n_ox = c_ox * v_ox / 1000
    n_red = n_ox * b / a
    c_red = n_red / (v_red / 1000)
    stem = pick(rng, [f'{v_red} cm³ of a {redn} solution required {v_ox:.2f} cm³ of {sf(c_ox)} mol dm⁻³ {oxn} for complete reaction: {eq}. Calculate the concentration of {red} in the solution.',
                      f'In a redox titration ({eq}), {v_ox:.2f} cm³ of {sf(c_ox)} mol dm⁻³ {ox} reacted with {v_red} cm³ of {red}(aq). Determine [{red}].'])
    return num(stem, q(c_red, 'mol dm⁻³'), f'n({ox}) = {sf(c_ox)} × {v_ox / 1000:.5f} = {sf(n_ox)} mol (M1); n({red}) = {b}/{a} × n = {sf(n_red)} mol (M1); c = {sf(n_red)}/{v_red / 1000} = {q(c_red, "mol dm⁻³")} (A1).', 3)


R.mcqs('ch07-st2', 'C2', (1, 4), [
    ('Why does chlorine oxidise iodide ions but iodine does not oxidise chloride ions?', 'Chlorine has a greater tendency to gain electrons than iodine.', ['Iodine is a solid.', 'Chloride ions are more reactive.', 'Chlorine has a larger atomic radius.'], 'Oxidising power Cl₂ > I₂.'),
    ('Why does sodium react more vigorously with water than magnesium?', 'Sodium loses its single outer electron more easily.', ['Sodium is denser.', 'Magnesium is a non-metal.', 'Magnesium has fewer electrons.'], 'Lower IE, more reactive.'),
    ('Why is hydrochloric acid not used to acidify manganate(VII) titrations?', 'MnO₄⁻ would oxidise Cl⁻ to Cl₂, using up extra titrant.', ['HCl is a weak acid.', 'HCl reacts with Fe²⁺.', 'It makes the end point pink.'], 'Side reaction.'),
    ('Why is the colour of the end point in a dichromate titration hard to see?', 'The change is from green Cr³⁺ to a slight orange tint, so a redox indicator is needed.', ['Dichromate is colourless.', 'Cr³⁺ is purple.', 'The solution is opaque.'], 'Use diphenylamine sulfonate.'),
])


@p1b(R, 'ch07-st2')
def p1b_iron_tablet(rng, slot):
    src = pick(rng, ['Several iron tablets', 'A sample of iron(II) sulfate lawn treatment', 'A sample of impure iron(II) sulfate crystals', 'Some crushed iron supplement capsules'])
    ox = pick(rng, ['Mn', 'Cr'])
    m = round(rng.uniform(1.50, 4.00), 3)
    pct = rng.uniform(10, 20)
    nfe = m * pct / 100 / AR['Fe']
    vflask, aliq = pick(rng, [(250.0, 25.00), (100.0, 10.00), (250.0, 20.00), (200.0, 25.00)])
    fac = vflask / aliq
    c = pick(rng, [0.0100, 0.00800, 0.0120])
    ratio = 5 if ox == 'Mn' else 6
    v = round(nfe / fac / ratio / c * 1000, 2)
    if not 8 < v < 48:
        return None
    n_ox = c * v / 1000
    nfe_c = n_ox * ratio * fac
    pct_c = nfe_c * AR['Fe'] / m * 100
    if ox == 'Mn':
        reag, eqn = 'potassium manganate(VII)', 'MnO₄⁻(aq) + 5Fe²⁺(aq) + 8H⁺(aq) → Mn²⁺(aq) + 5Fe³⁺(aq) + 4H₂O(l)'
        spc = 'MnO₄⁻'
        endp = ('State and explain the colour change at the end point.', 'colourless (pale yellow) to permanent pale pink – the first excess of purple MnO₄⁻ is not decolourised', 'colourless → pink (1); excess MnO₄⁻ once Fe²⁺ used up (1).', 2)
    else:
        reag, eqn = 'potassium dichromate(VI)', 'Cr₂O₇²⁻(aq) + 6Fe²⁺(aq) + 14H⁺(aq) → 2Cr³⁺(aq) + 6Fe³⁺(aq) + 7H₂O(l)'
        spc = 'Cr₂O₇²⁻'
        endp = ('Explain why a redox indicator (e.g. sodium diphenylamine sulfonate) is needed in this titration.', 'The colour change of dichromate (orange) to Cr³⁺ (green) is gradual and masked, so no sharp end point is seen without an indicator.', 'orange → green not sharp (1); indicator gives a distinct change (1).', 2)
    intro = (f'{src} with a total mass of {m:.3f} g {"were" if src.startswith(("Several", "Some")) else "was"} dissolved in dilute sulfuric acid and made up to {vflask:.1f} cm³. {aliq:.2f} cm³ portions were titrated with {c:.5f} mol dm⁻³ {reag}. The mean titre was {v:.2f} cm³ (burette ±0.05 cm³ per reading).\n'
             + eqn)
    parts = [(f'Calculate the amount of {spc} in the mean titre.', f'{sf(n_ox)} mol', f'{c} × {v / 1000:.5f} = {sf(n_ox)} mol (A1).', 1),
             ('Calculate the total amount of Fe²⁺ in the sample.', f'{sf(nfe_c)} mol', f'× {ratio} (M1); × {fac:g} for the full {vflask:.1f} cm³ (M1) = {sf(nfe_c)} mol (A1).', 3),
             ('Calculate the percentage by mass of iron in the sample.', f'{pct_c:.1f} %', f'{sf(nfe_c)} × 55.85 = {sf(nfe_c * AR["Fe"])} g (M1); /{m:.3f} × 100 = {pct_c:.1f} % (A1).', 2)]
    pool = [endp,
            ('Suggest why the sample must be analysed soon after dissolving.', 'Fe²⁺ is slowly oxidised to Fe³⁺ by air, which would give a low result.', 'Air oxidation of Fe²⁺ (1).', 1),
            ('State the change in oxidation state of iron in the reaction.', '+2 to +3 (oxidised)', '+2 → +3 (1).', 1),
            ('Explain why dilute sulfuric acid, not hydrochloric acid, is used to acidify the solution.' if ox == 'Mn' else 'State the role of the H⁺ ions in the reaction.',
             'HCl would be oxidised to Cl₂ by manganate(VII), giving a titre that is too high.' if ox == 'Mn' else 'H⁺ is a reactant: it combines with oxide from dichromate to form water.', 'reason (1).', 1),
            ('Calculate the percentage uncertainty in the mean titre.', f'{0.10 / v * 100:.2f} %', f'0.10/{v:.2f} × 100 (1).', 1)]
    rng.shuffle(pool)
    return dict(intro=intro, parts=parts + pool[:1], extras=pool[1:])


# ---- ch07-st3 primary, secondary and electrolytic cells ----
MOLTEN = [('sodium chloride', 'NaCl', 'sodium', 'chlorine', 'Na⁺ + e⁻ → Na', '2Cl⁻ → Cl₂ + 2e⁻'),
          ('lead(II) bromide', 'PbBr2', 'lead', 'bromine', 'Pb²⁺ + 2e⁻ → Pb', '2Br⁻ → Br₂ + 2e⁻'),
          ('magnesium chloride', 'MgCl2', 'magnesium', 'chlorine', 'Mg²⁺ + 2e⁻ → Mg', '2Cl⁻ → Cl₂ + 2e⁻'),
          ('potassium iodide', 'KI', 'potassium', 'iodine', 'K⁺ + e⁻ → K', '2I⁻ → I₂ + 2e⁻'),
          ('aluminium oxide (in cryolite)', 'Al2O3', 'aluminium', 'oxygen', 'Al³⁺ + 3e⁻ → Al', '2O²⁻ → O₂ + 4e⁻'),
          ('lithium chloride', 'LiCl', 'lithium', 'chlorine', 'Li⁺ + e⁻ → Li', '2Cl⁻ → Cl₂ + 2e⁻'),
          ('zinc chloride', 'ZnCl2', 'zinc', 'chlorine', 'Zn²⁺ + 2e⁻ → Zn', '2Cl⁻ → Cl₂ + 2e⁻'),
          ('calcium bromide', 'CaBr2', 'calcium', 'bromine', 'Ca²⁺ + 2e⁻ → Ca', '2Br⁻ → Br₂ + 2e⁻')]
AQ = [('concentrated sodium chloride solution', 'hydrogen', 'chlorine'), ('dilute sulfuric acid', 'hydrogen', 'oxygen'),
      ('copper(II) sulfate solution (inert electrodes)', 'copper', 'oxygen'), ('potassium iodide solution', 'hydrogen', 'iodine'),
      ('silver nitrate solution (inert electrodes)', 'silver', 'oxygen'), ('copper(II) chloride solution', 'copper', 'chlorine'),
      ('sodium hydroxide solution', 'hydrogen', 'oxygen'), ('very dilute sodium chloride solution', 'hydrogen', 'oxygen')]
CELLS = [('zinc–carbon (dry) cell', 'primary', 'zinc', 'manganese(IV) oxide'), ('alkaline cell', 'primary', 'zinc', 'manganese(IV) oxide'),
         ('lead–acid battery', 'secondary', 'lead', 'lead(IV) oxide'), ('lithium-ion battery', 'secondary', 'lithium in graphite', 'lithium metal oxide (e.g. LiCoO₂)'),
         ('nickel–metal hydride battery', 'secondary', 'metal hydride', 'nickel oxide hydroxide'), ('hydrogen–oxygen fuel cell', 'fuel cell', 'hydrogen', 'oxygen')]

R.facts('ch07-st3', F(
    terms=[('voltaic (galvanic) cell', 'an electrochemical cell that converts chemical energy from a spontaneous redox reaction into electrical energy'),
           ('electrolytic cell', 'a cell in which electrical energy drives a non-spontaneous redox reaction'),
           ('anode', 'the electrode at which oxidation occurs'),
           ('cathode', 'the electrode at which reduction occurs'),
           ('salt bridge', 'a connection containing an electrolyte that allows ions to move between half-cells to complete the circuit and maintain charge balance'),
           ('primary cell', 'a cell that cannot be recharged because its reaction is not reversible'),
           ('secondary cell', 'a rechargeable cell in which the reaction can be reversed by applying an external current')],
    facts=[('At which electrode does oxidation take place in all electrochemical cells?', 'the anode', ['the cathode', 'the salt bridge', 'both electrodes'], 'An Ox, Red Cat.'),
           ('In a voltaic cell, electrons flow through the external circuit from', 'anode to cathode', ['cathode to anode', 'salt bridge to anode', 'cathode to salt bridge'], 'Anode is negative.'),
           ('What is formed at the cathode during electrolysis of molten sodium chloride?', 'sodium', ['chlorine', 'hydrogen', 'oxygen'], 'Na⁺ reduced.'),
           ('Which is a secondary (rechargeable) cell?', 'lithium-ion battery', ['zinc–carbon cell', 'alkaline cell', 'silver oxide button cell'], 'Reversible.'),
           ('In an electrolytic cell, the anode is', 'positive', ['negative', 'neutral', 'always made of the metal deposited'], 'Connected to + terminal.'),
           ('Why must ionic compounds be molten or dissolved to be electrolysed?', 'The ions must be free to move.', ['The electrons must be free to move.', 'To lower the voltage.', 'To prevent oxidation.'], 'Mobile ions carry charge.')],
    why=[('Explain the function of the salt bridge in a voltaic cell.', 'It allows ions to migrate between the half-cells, completing the circuit and balancing the charge that builds up as oxidation and reduction occur.'),
         ('Explain why hydrogen, not sodium, is formed at the cathode when aqueous sodium chloride is electrolysed.', 'Water (or H⁺) is much more easily reduced than Na⁺ (E⦵ Na⁺/Na = −2.71 V), so H₂ is produced: 2H₂O + 2e⁻ → H₂ + 2OH⁻.'),
         ('Explain why lead–acid batteries can be recharged.', 'The discharge products (PbSO₄) remain on the electrodes, and an external current reverses the redox reactions to regenerate Pb and PbO₂.'),
         ('Explain why concentrated sodium chloride solution gives chlorine at the anode but very dilute solution gives oxygen.', 'At high [Cl⁻] chloride ions are preferentially oxidised (concentration effect); in dilute solution water is oxidised to O₂ because its E⦵ is lower.'),
         ('Explain why fuel cells are more efficient than burning fuel to generate electricity.', 'Chemical energy is converted directly to electrical energy without the heat-engine stage, which loses a large proportion as heat.')],
    contrast=[('a voltaic cell', 'an electrolytic cell', 'A voltaic cell uses a spontaneous reaction to produce electricity (anode −, cathode +); an electrolytic cell uses electricity to drive a non-spontaneous reaction (anode +, cathode −).'),
              ('a primary cell', 'a secondary cell', 'A primary cell is used once and discarded; a secondary cell can be recharged because its reactions are reversible.'),
              ('a fuel cell', 'a rechargeable battery', 'A fuel cell needs a continuous supply of fuel and oxidant; a battery stores its reactants internally and is recharged electrically.')],
    misc=[('In all cells the anode is positive.', 'The anode is the site of oxidation: negative in a voltaic cell, positive in an electrolytic cell.'),
          ('Electrons flow through the salt bridge.', 'Electrons flow through the external wire; ions flow through the salt bridge.')],
    apply=[('Write the half-equations at each electrode for the electrolysis of molten lead(II) bromide.', 'cathode: Pb²⁺ + 2e⁻ → Pb; anode: 2Br⁻ → Br₂ + 2e⁻', 2),
           ('State the products at each electrode when dilute sulfuric acid is electrolysed using platinum electrodes and their volume ratio.', 'H₂ at cathode, O₂ at anode, 2 : 1', 2)],
    evaluate=[('Lithium-ion batteries are the best option for storing renewable energy.', ['high energy density and efficiency', 'falling costs; widely manufactured'], ['lithium and cobalt mining have environmental and ethical costs', 'limited cycle life and fire risk', 'other options (pumped hydro, flow batteries, hydrogen) suit large-scale storage'], 'Excellent for vehicles and short-term storage, but a mix of technologies is needed for grid-scale renewable storage.'),
              ('Hydrogen fuel cells will replace batteries in all vehicles.', ['fast refuelling and long range', 'only water emitted'], ['hydrogen production is mostly from fossil fuels', 'storage and distribution are difficult', 'batteries are cheaper and more efficient for cars'], 'Fuel cells may suit heavy transport, but batteries are likely to dominate passenger vehicles.')],
    extended=[('A hydrogen–oxygen fuel cell uses an alkaline electrolyte. (a) Write the half-equations at the anode and cathode. (b) Write the overall equation. (c) State the direction of electron flow. (d) Discuss one advantage and one disadvantage of fuel cells compared with lithium-ion batteries.', '(a) anode: H₂ + 2OH⁻ → 2H₂O + 2e⁻; cathode: O₂ + 2H₂O + 4e⁻ → 4OH⁻. (b) 2H₂ + O₂ → 2H₂O. (c) anode → cathode through the external circuit. (d) e.g. fast refuelling/only water / hydrogen storage and production.', 7, 'multi_step')],
))


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3_molten_products(rng, slot):
    nm, f, cat, an, hc, ha = pick(rng, MOLTEN)
    kind = rng.choice(['cathode', 'anode'])
    right = cat if kind == 'cathode' else an
    pool = list(dict.fromkeys([cat, an, 'hydrogen', 'oxygen', 'chlorine', 'sodium']))
    wr = [x for x in pool if x != right]
    rng.shuffle(wr)
    stem = f'Molten {nm} is electrolysed with inert electrodes. What is formed at the {kind}?'
    return mcq(rng, stem, right, wr[:3], f'Cathode: {hc}; anode: {ha}.')


@R.add('ch07-st3', 'C3', (2, 4), 'mcq')
def c3_aq_products(rng, slot):
    sol, cat, an = pick(rng, AQ)
    right = f'{cat} at the cathode and {an} at the anode'
    wr = [f'{an} at the cathode and {cat} at the anode', f'sodium at the cathode and {an} at the anode' if 'sodium' in sol else f'hydrogen at the cathode and oxygen at the anode',
          f'{cat} at the cathode and hydrogen at the anode', 'hydrogen at the cathode and chlorine at the anode']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'What are the products when {sol} is electrolysed?'
    return mcq(rng, stem, right, wr[:3], f'{sol}: {cat} (cathode, most easily reduced) and {an} (anode, most easily oxidised at that concentration).')


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3_cell_type(rng, slot):
    nm, kind, neg, pos = pick(rng, CELLS)
    stem = pick(rng, [f'How is the {nm} classified?', f'Which description fits the {nm}?'])
    right = {'primary': 'a primary cell – not rechargeable', 'secondary': 'a secondary cell – rechargeable', 'fuel cell': 'a fuel cell – reactants supplied continuously'}[kind]
    wr = [v for k, v in {'primary': 'a primary cell – not rechargeable', 'secondary': 'a secondary cell – rechargeable', 'fuel cell': 'a fuel cell – reactants supplied continuously'}.items() if k != kind] + ['an electrolytic cell – needs an external power supply to operate']
    return mcq(rng, stem, right, wr, f'{nm}: negative electrode {neg}, positive electrode {pos}.')


@R.add('ch07-st3', 'C3', (2, 5), 'numerical')
def c3_faraday(rng, slot):
    metal, n, sol = pick(rng, [('Cu', 2, 'copper(II) sulfate'), ('Ag', 1, 'silver nitrate'), ('Zn', 2, 'zinc sulfate'), ('Ni', 2, 'nickel(II) sulfate'), ('Al', 3, 'molten aluminium oxide'), ('Cr', 3, 'chromium(III) sulfate')])
    I = rng.choice([0.200, 0.500, 1.00, 1.50, 2.00, 2.50])
    t = rng.choice([10, 15, 20, 30, 45, 60]) * 60
    Q = I * t
    m = Q / FARADAY / n * AR[metal]
    stem = pick(rng, [f'A current of {sf(I)} A is passed through {sol} for {t // 60} minutes. Calculate the mass of {ENAME[metal]} deposited at the cathode.',
                      f'During electroplating with {sol}, a steady current of {sf(I)} A flows for {t // 60} min. Determine the mass of {metal} plated.'])
    return num(stem, q(m, 'g'), f'Q = It = {sf(I)} × {t} = {sf(Q)} C (M1); n(e⁻) = Q/F = {sf(Q / FARADAY)} mol; n({metal}) = n(e⁻)/{n} (M1); m = {q(m, "g")} (A1).', 3)


R.mcqs('ch07-st3', 'C2', (1, 4), [
    ('Why does a voltaic cell stop working if the salt bridge is removed?', 'The circuit is broken and charge builds up in each half-cell.', ['The electrodes dissolve.', 'Electrons cannot flow through the wire.', 'The reaction becomes non-spontaneous.'], 'Ion flow needed.'),
    ('Why is aluminium extracted by electrolysis rather than by reduction with carbon?', 'Aluminium is more reactive than carbon, so carbon cannot reduce Al₂O₃.', ['Aluminium oxide is a gas.', 'Carbon is too expensive.', 'Electrolysis is exothermic.'], 'Reactivity.'),
    ('Why is the electrolyte in the lead–acid battery dilute sulfuric acid?', 'It provides H⁺ and SO₄²⁻ ions that take part in both electrode reactions.', ['It is a non-conductor.', 'It prevents recharging.', 'It contains lead ions.'], 'PbSO₄ formation.'),
    ('What happens at the anode during copper electroplating with a copper anode?', 'Copper atoms are oxidised to Cu²⁺ ions.', ['Copper is deposited.', 'Oxygen is formed.', 'Hydrogen is formed.'], 'Cu → Cu²⁺ + 2e⁻.'),
])


# ---- ch07-st4 standard electrode potentials (HL) ----
EOX = [e for e in EO]


def _e_name(e):
    return f'{ion(e[0]) if e[0][-1] in "+-" else chem(e[0])}/{ion(e[1]) if e[1][-1] in "+-" else chem(e[1])}'


R.facts('ch07-st4', F(
    terms=[('standard electrode potential (E⦵)', 'the potential of a half-cell measured against the standard hydrogen electrode under standard conditions (298 K, 100 kPa, 1 mol dm⁻³)'),
           ('standard hydrogen electrode', 'the reference half-cell, H₂(g, 100 kPa) | H⁺(aq, 1 mol dm⁻³) on platinum, assigned E⦵ = 0.00 V'),
           ('cell potential (E⦵cell)', 'the potential difference between two half-cells under standard conditions: E⦵cell = E⦵(cathode) − E⦵(anode)'),
           ('standard conditions (electrochemistry)', '298 K, 100 kPa for gases and 1 mol dm⁻³ for ions in solution'),
           ('cell diagram', 'a shorthand representation of a voltaic cell, e.g. Zn(s)|Zn²⁺(aq)||Cu²⁺(aq)|Cu(s), with the anode on the left')],
    facts=[('What is the relationship between ΔG⦵ and E⦵cell?', 'ΔG⦵ = −nFE⦵cell', ['ΔG⦵ = nFE⦵cell', 'ΔG⦵ = −RT ln E⦵', 'ΔG⦵ = E⦵/nF'], 'Data booklet.'),
           ('A positive E⦵cell indicates that the reaction is', 'spontaneous under standard conditions', ['non-spontaneous', 'at equilibrium', 'endothermic'], 'ΔG⦵ < 0.'),
           ('Which species is the strongest oxidising agent?', 'F₂ (E⦵ = +2.87 V)', ['Cl₂ (+1.36 V)', 'Cu²⁺ (+0.34 V)', 'Li⁺ (−3.04 V)'], 'Most positive E⦵.'),
           ('Which species is the strongest reducing agent?', 'Li (E⦵ Li⁺/Li = −3.04 V)', ['Zn (−0.76 V)', 'Cu (+0.34 V)', 'Ag (+0.80 V)'], 'Most negative E⦵.'),
           ('What is E⦵ of the standard hydrogen electrode?', '0.00 V', ['+1.00 V', '−1.00 V', '+0.34 V'], 'By definition.'),
           ('In a cell diagram, what does the double vertical line represent?', 'the salt bridge', ['a phase boundary', 'the electrodes', 'the external circuit'], '||.')],
    why=[('Explain why E⦵ values are measured relative to the standard hydrogen electrode.', 'The potential of a single half-cell cannot be measured alone; it must be compared with a reference half-cell whose potential is defined as zero.'),
         ('Explain why a more positive E⦵ indicates a stronger oxidising agent.', 'A more positive E⦵ means the oxidised form has a greater tendency to gain electrons and be reduced, so it oxidises other species more readily.'),
         ('Explain why a reaction with a positive E⦵cell may not be observed in practice.', 'E⦵cell shows the reaction is thermodynamically feasible but says nothing about rate; a high activation energy (or non-standard conditions) may prevent it.'),
         ('Explain why platinum is used in the standard hydrogen electrode.', 'Platinum is inert and conducts electricity, providing a surface on which H₂/H⁺ equilibrium is established without the electrode itself reacting.')],
    contrast=[('E⦵cell', 'ΔG⦵', 'E⦵cell is an electrical measure (V) of the driving force – positive when spontaneous; ΔG⦵ is the energy measure (kJ mol⁻¹) – negative when spontaneous; ΔG⦵ = −nFE⦵.'),
              ('the anode of a voltaic cell', 'the cathode of a voltaic cell', 'The anode is the half-cell with the more negative E⦵ where oxidation occurs (negative terminal); the cathode has the more positive E⦵ where reduction occurs.')],
    misc=[('Doubling a half-equation doubles its E⦵ value.', 'E⦵ is an intensive property and does not change when the half-equation is multiplied.'),
          ('A larger E⦵cell means the reaction is faster.', 'E⦵cell relates to thermodynamic feasibility (ΔG⦵), not to rate.')],
    apply=[('Calculate E⦵cell for Zn(s)|Zn²⁺(aq)||Ag⁺(aq)|Ag(s).', '+0.80 − (−0.76) = +1.56 V', 2),
           ('Calculate ΔG⦵ for Zn + Cu²⁺ → Zn²⁺ + Cu (E⦵cell = +1.10 V).', 'ΔG⦵ = −2 × 96 500 × 1.10 = −212 kJ mol⁻¹', 2)],
    evaluate=[('Standard electrode potentials reliably predict which redox reactions will occur.', ['positive E⦵cell → thermodynamically feasible', 'useful for predicting products and cell voltages'], ['only valid under standard conditions', 'say nothing about rate (kinetic barriers)', 'concentration and complexation change E'], 'They predict feasibility well under standard conditions, but kinetics and conditions determine what is actually observed.'),
              ('The hydrogen electrode is a practical reference for everyday measurements.', ['defines the scale; highly reproducible'], ['needs H₂ gas at 100 kPa and platinised Pt – inconvenient', 'secondary references (silver/silver chloride, calomel) are used instead'], 'It defines the scale, but practical measurements use more convenient secondary reference electrodes.')],
    extended=[('A cell is made from a Mg²⁺/Mg half-cell and a Cu²⁺/Cu half-cell. (a) Write the cell diagram. (b) Calculate E⦵cell. (c) Write the overall equation and calculate ΔG⦵. (d) State and explain what happens to the mass of each electrode.', '(a) Mg(s)|Mg²⁺(aq)||Cu²⁺(aq)|Cu(s). (b) +0.34 − (−2.37) = +2.71 V. (c) Mg + Cu²⁺ → Mg²⁺ + Cu; ΔG⦵ = −2 × 96 500 × 2.71 = −523 kJ mol⁻¹. (d) Mg electrode loses mass (oxidised to Mg²⁺); Cu electrode gains mass (Cu deposited).', 8, 'multi_step')],
))


def ev(x):
    """Electrode potential to 2 d.p. with sign, as in the data booklet."""
    return ('+' if x > 0 else '') + f'{x:.2f}'.replace('-', '−')


def _cell(rng):
    a, b = rng.sample(EOX, 2)
    if a[3] == b[3]:
        return None
    cat, an = (a, b) if a[3] > b[3] else (b, a)
    return cat, an, round(cat[3] - an[3], 2)


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3_ecell(rng, slot):
    r = _cell(rng)
    if r is None:
        return None
    cat, an, E = r
    stem = pick(rng, [f'What is E⦵cell for a cell made from the {_e_name(cat)} (E⦵ = {ev(cat[3])} V) and {_e_name(an)} (E⦵ = {ev(an[3])} V) half-cells?',
                      f'Using E⦵({_e_name(cat)}) = {ev(cat[3])} V and E⦵({_e_name(an)}) = {ev(an[3])} V, calculate the standard cell potential.'])
    wr = [round(cat[3] + an[3], 2), round(an[3] - cat[3], 2), round(cat[3] - 2 * an[3], 2), round(abs(cat[3]) + abs(an[3]) + 0.1, 2)]
    wr = [f'{ev(w)} V' for w in dict.fromkeys(wr) if abs(w - E) > 0.005]
    return mcq(rng, stem, f'{ev(E)} V', wr[:3], f'E⦵cell = E⦵(cathode) − E⦵(anode) = {ev(cat[3])} − ({ev(an[3])}) = {ev(E)} V.')


@R.add('ch07-st4', 'C3', (2, 5), 'numerical')
def c3_dg_cell(rng, slot):
    r = _cell(rng)
    if r is None:
        return None
    cat, an, E = r
    n = cat[2] * an[2] // math.gcd(cat[2], an[2])
    dg = -n * FARADAY * E / 1000
    stem = f'A voltaic cell is made from {_e_name(cat)} (E⦵ = {ev(cat[3])} V) and {_e_name(an)} (E⦵ = {ev(an[3])} V). Determine E⦵cell, the number of electrons transferred in the balanced overall equation, and ΔG⦵.'
    return num(stem, f'E⦵cell = {ev(E)} V; n = {n}; ΔG⦵ = {sgn(dg, 3, "kJ mol⁻¹")}', f'E⦵cell = {ev(E)} V (A1); electrons balanced: n = {n} (A1); ΔG⦵ = −nFE = −{n} × 96 500 × {E:.2f} = {sgn(dg, 3, "kJ mol⁻¹")} (A1).', 3)


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3_strongest_ox(rng, slot):
    pool = rng.sample(EOX, 4)
    kind = rng.choice(['oxidising', 'reducing'])
    if kind == 'oxidising':
        best = max(pool, key=lambda e: e[3])
        lab = lambda e: ion(e[0]) if e[0][-1] in '+-' else chem(e[0])
    else:
        best = min(pool, key=lambda e: e[3])
        lab = lambda e: ion(e[1]) if e[1][-1] in '+-' else chem(e[1])
    if [e[3] for e in pool].count(best[3]) > 1:
        return None
    stem = f'Using the E⦵ values {"; ".join(f"{_e_name(e)} {ev(e[3])} V" for e in pool)}, which species is the strongest {kind} agent?'
    return mcq(rng, stem, lab(best), [lab(e) for e in pool if e != best], f'{"Most positive" if kind == "oxidising" else "Most negative"} E⦵ → {lab(best)}.')


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3_spont(rng, slot):
    ox_, red_ = rng.sample(EOX, 2)
    if ox_[3] == red_[3]:
        return None
    o = ion(ox_[0]) if ox_[0][-1] in '+-' else chem(ox_[0])
    rd = ion(red_[1]) if red_[1][-1] in '+-' else chem(red_[1])
    E = round(ox_[3] - red_[3], 2)
    yes = E > 0
    stem = f'Will {o} oxidise {rd} under standard conditions? E⦵({_e_name(ox_)}) = {ev(ox_[3])} V; E⦵({_e_name(red_)}) = {ev(red_[3])} V.'
    right = f'Yes, E⦵cell = {ev(E)} V' if yes else f'No, E⦵cell = {ev(E)} V'
    wr = [f'{"No" if yes else "Yes"}, E⦵cell = {ev(E)} V', f'{"Yes" if yes else "No"}, E⦵cell = {ev(-E)} V', f'{"No" if yes else "Yes"}, E⦵cell = {ev(-E)} V']
    return mcq(rng, stem, right, wr, f'E⦵cell = E⦵(reduction of {o}) − E⦵({_e_name(red_)}) = {ev(E)} V; {"positive → spontaneous" if yes else "negative → not spontaneous"}.')


R.mcqs('ch07-st4', 'C2', (1, 4), [
    ('Why do E⦵ values not change when a half-equation is multiplied by 2?', 'E⦵ is a potential per electron, an intensive property.', ['Electrons are not counted.', 'ΔG also does not change.', 'Only gases are affected.'], 'Intensive.'),
    ('Why does a negative E⦵cell mean the reaction is not spontaneous?', 'ΔG⦵ = −nFE⦵ would be positive.', ['The cell has no electrons.', 'E⦵ is always positive.', 'The anode is positive.'], 'ΔG⦵ > 0.'),
    ('In a cell, the half-cell with the more negative E⦵ acts as', 'the anode (oxidation)', ['the cathode (reduction)', 'the salt bridge', 'the reference'], 'Loses electrons.'),
    ('Why is E⦵ for Na⁺/Na very negative?', 'Sodium very readily loses an electron, so Na⁺ is very hard to reduce.', ['Na⁺ is a strong oxidising agent.', 'Sodium is a non-metal.', 'Na⁺ has a full shell, so it gains electrons easily.'], 'Strong reducing agent.'),
])


# ---- ch07-st5 oxidation of alcohols, reduction of carbonyls ----
ALC = [o for o in ORG if o[3] == 'alcohol']
OXPROD = {'methanol': ('methanal', 'methanoic acid'), 'ethanol': ('ethanal', 'ethanoic acid'), 'propan-1-ol': ('propanal', 'propanoic acid'),
          'butan-1-ol': ('butanal', 'butanoic acid'), '2-methylpropan-1-ol': ('2-methylpropanal', '2-methylpropanoic acid'),
          'propan-2-ol': ('propanone', None), 'butan-2-ol': ('butanone', None), 'pentan-3-ol': ('pentan-3-one', None), '2-methylpropan-2-ol': (None, None)}
REDPROD = {'ethanal': 'ethanol', 'propanal': 'propan-1-ol', 'butanal': 'butan-1-ol', 'methanal': 'methanol', 'propanone': 'propan-2-ol', 'butanone': 'butan-2-ol',
           'pentan-2-one': 'pentan-2-ol', 'pentan-3-one': 'pentan-3-ol', 'ethanoic acid': 'ethanol', 'propanoic acid': 'propan-1-ol'}

R.facts('ch07-st5', F(
    terms=[('acidified potassium dichromate(VI)', 'an oxidising agent (K₂Cr₂O₇/H₂SO₄) used to oxidise alcohols; it turns from orange to green as Cr₂O₇²⁻ is reduced to Cr³⁺'),
           ('reflux', 'continuous boiling with a vertical condenser so that vapour condenses and returns to the flask, allowing complete reaction without loss of volatile substances'),
           ('distillation', 'heating a mixture and condensing the vapour in a separate vessel, used to remove a volatile product such as an aldehyde as soon as it forms'),
           ('sodium borohydride', 'NaBH₄, a reducing agent (source of hydride ions) that reduces aldehydes to primary alcohols and ketones to secondary alcohols'),
           ('lithium aluminium hydride', 'LiAlH₄, a powerful reducing agent in dry ether that also reduces carboxylic acids to primary alcohols')],
    facts=[('What is the product of heating propan-2-ol with acidified potassium dichromate(VI)?', 'propanone', ['propanal', 'propanoic acid', 'no reaction'], 'Secondary → ketone.'),
           ('Which alcohol is not oxidised by acidified dichromate(VI)?', '2-methylpropan-2-ol', ['propan-1-ol', 'butan-2-ol', 'ethanol'], 'Tertiary.'),
           ('What colour change occurs when ethanol is oxidised by acidified potassium dichromate(VI)?', 'orange to green', ['green to orange', 'purple to colourless', 'colourless to brown'], 'Cr(VI) → Cr(III).'),
           ('Which conditions convert ethanol into ethanoic acid?', 'excess acidified dichromate, heated under reflux', ['limited oxidant, distilled immediately', 'NaBH₄ in water', 'concentrated H₂SO₄ at 170 °C'], 'Full oxidation.'),
           ('Which reagent reduces ethanoic acid to ethanol?', 'LiAlH₄ in dry ether', ['NaBH₄ in water', 'acidified K₂Cr₂O₇', 'H₂ with no catalyst'], 'NaBH₄ too weak for acids.'),
           ('The reduction of butanone gives', 'butan-2-ol', ['butan-1-ol', 'butanal', 'butanoic acid'], 'Ketone → secondary alcohol.')],
    why=[('Explain why distillation is used to obtain an aldehyde from a primary alcohol.', 'The aldehyde has a lower boiling point than the alcohol (no hydrogen bonding), so it distils off as soon as it forms, preventing further oxidation to the carboxylic acid.'),
         ('Explain why tertiary alcohols resist oxidation by acidified dichromate(VI).', 'The carbon bearing the –OH has no hydrogen atom, so it cannot form C=O without breaking a C–C bond.'),
         ('Explain why reflux is used to oxidise a primary alcohol to a carboxylic acid.', 'Refluxing keeps the volatile aldehyde intermediate in contact with excess oxidant so that it is fully oxidised to the acid.'),
         ('Explain why NaBH₄ can reduce aldehydes and ketones but not carboxylic acids.', 'NaBH₄ is a mild hydride donor; the carboxyl carbon is less electrophilic (delocalisation) and the acid reacts with hydride to form a carboxylate, so the stronger LiAlH₄ is needed.')],
    contrast=[('oxidising a primary alcohol by distillation', 'oxidising it under reflux', 'Distillation removes the aldehyde as it forms; reflux keeps it in the flask so it is oxidised further to the carboxylic acid.'),
              ('NaBH₄', 'LiAlH₄', 'NaBH₄ is milder and can be used in water or alcohol (reduces aldehydes and ketones); LiAlH₄ is much stronger, needs dry ether and also reduces carboxylic acids.')],
    misc=[('All alcohols are oxidised to carboxylic acids by acidified dichromate.', 'Only primary alcohols (via aldehydes) give acids; secondary give ketones; tertiary are not oxidised.'),
          ('Reducing propanone gives propan-1-ol.', 'Reduction of a ketone gives a secondary alcohol: propan-2-ol.')],
    apply=[('Write an equation for the oxidation of propan-1-ol to propanoic acid using [O] for the oxidising agent.', 'CH₃CH₂CH₂OH + 2[O] → CH₃CH₂COOH + H₂O', 2),
           ('Write an equation for the reduction of butanal by NaBH₄ using [H].', 'CH₃CH₂CH₂CHO + 2[H] → CH₃CH₂CH₂CH₂OH', 2)],
    evaluate=[('Acidified dichromate(VI) is a suitable oxidising agent for industrial alcohol oxidation.', ['reliable, easy colour change, good yields in the laboratory'], ['Cr(VI) is toxic and carcinogenic; waste disposal is costly', 'catalytic oxidation with air (e.g. Cu or Ag catalysts) is cheaper and greener'], 'It is a good laboratory reagent, but greener catalytic methods are preferred industrially.'),
              ('Chemical tests are sufficient to distinguish primary, secondary and tertiary alcohols.', ['dichromate distinguishes tertiary (no change) from primary/secondary', 'the products can be tested further (Tollens’ for aldehydes)'], ['several steps are needed; colour judgements are subjective', 'IR and NMR give faster, more definitive results'], 'Chemical tests can distinguish them, but spectroscopy is quicker and more reliable.')],
    extended=[('Three isomeric alcohols, A, B and C, have the formula C₄H₁₀O. A is oxidised to a ketone; B is not oxidised; C gives an acid on refluxing. (a) Identify A, B and C. (b) Name the products of oxidation of A and C. (c) Describe the colour change with acidified dichromate. (d) Explain how distillation could be used to obtain an aldehyde from C.', '(a) A butan-2-ol, B 2-methylpropan-2-ol, C butan-1-ol (or 2-methylpropan-1-ol). (b) butanone; butanoic acid. (c) orange → green for A and C; stays orange for B. (d) heat with limited oxidant and distil the lower-boiling aldehyde as it forms.', 8, 'multi_step')],
))


@R.add('ch07-st5', 'C3', (1, 4), 'mcq')
def c3_ox_product(rng, slot):
    nm = pick(rng, list(OXPROD))
    ald, acid = OXPROD[nm]
    cond = rng.choice(['distil', 'reflux'])
    if ald is None:
        right = 'no reaction (tertiary alcohol)'
    elif acid is None:
        right = ald
    else:
        right = ald if cond == 'distil' else acid
    pool = [x for v in OXPROD.values() for x in v if x] + ['no reaction (tertiary alcohol)']
    wr = [x for x in [ald, acid, 'no reaction (tertiary alcohol)'] + rng.sample(pool, 4) if x and x != right]
    wr = list(dict.fromkeys(wr))
    ctext = 'heated with acidified potassium dichromate(VI) and the product distilled off immediately' if cond == 'distil' else 'heated under reflux with excess acidified potassium dichromate(VI)'
    stem = f'{cap(nm)} is {ctext}. What is the organic product?'
    deg = ORGN[nm][4] if nm in ORGN else 1
    return mcq(rng, stem, right, wr[:3], f'{nm} is a {"primary" if deg == 1 else "secondary" if deg == 2 else "tertiary"} alcohol → {right}.')


@R.add('ch07-st5', 'C3', (1, 4), 'mcq')
def c3_red_product(rng, slot):
    nm = pick(rng, list(REDPROD))
    reag = 'LiAlH₄ in dry ether' if 'acid' in nm else rng.choice(['NaBH₄', 'LiAlH₄ in dry ether'])
    right = REDPROD[nm]
    pool = list(dict.fromkeys(REDPROD.values()))
    wr = [x for x in pool if x != right]
    rng.shuffle(wr)
    stem = f'What is the organic product when {nm} is reduced with {reag}?'
    return mcq(rng, stem, right, wr[:3], f'{"Aldehydes/acids → primary" if "al" in nm.split()[-1] or "acid" in nm else "Ketones → secondary"} alcohols: {right}.')


@R.add('ch07-st5', 'C3', (1, 5), 'short')
def c3_ox_eq(rng, slot):
    nm = pick(rng, [k for k, v in OXPROD.items() if v[0] and k in ORGN])
    ald, acid = OXPROD[nm]
    o = ORGN[nm]
    prod = acid or ald
    po = ORGN.get(prod)
    if po is None:
        return None
    n_o = 2 if acid else 1
    stem = f'Write a balanced equation, using [O] to represent the oxidising agent, for the {"complete " if acid else ""}oxidation of {nm} and name the type of product formed.'
    ans = f'{oc(o)} + {"2" if n_o == 2 else ""}[O] → {oc(po)} + H₂O; {po[3]}'
    return dict(stem=stem, answer=ans, markingKey=f'Correct product {oc(po)} (1); balanced with {n_o}[O] and H₂O (1); {po[3]} (1).', type='short', marks=3)


@R.add('ch07-st5', 'C3', (2, 4), 'mcq')
def c3_alc_identify(rng, slot):
    deg = rng.choice([1, 2, 3])
    obs = {1: 'turns the orange dichromate green, and the distilled product gives a silver mirror with Tollens’ reagent',
           2: 'turns the orange dichromate green, but the product does not react with Tollens’ reagent',
           3: 'leaves the dichromate orange'}[deg]
    right = pick(rng, [o[0] for o in ALC if o[4] == deg])
    wr = rng.sample([o[0] for o in ALC if o[4] != deg], 3)
    stem = f'An alcohol, warmed with acidified potassium dichromate(VI), {obs}. Which alcohol could it be?'
    return mcq(rng, stem, right, wr, f'{"Primary → aldehyde (positive Tollens’)" if deg == 1 else "Secondary → ketone" if deg == 2 else "Tertiary – not oxidised"}: {right}.')


R.mcqs('ch07-st5', 'C2', (1, 4), [
    ('Why does the aldehyde distil off before the alcohol during partial oxidation?', 'Aldehydes cannot form hydrogen bonds between their molecules, so they have lower boiling points.', ['Aldehydes have higher molar masses.', 'Aldehydes are ionic.', 'The alcohol decomposes.'], 'Weaker IMF.'),
    ('In the oxidation of an alcohol, what happens to the dichromate ion?', 'It is reduced from Cr(VI) to Cr(III).', ['It is oxidised to Cr(VII).', 'It acts as a catalyst.', 'It is unchanged.'], 'Orange → green.'),
    ('Why is NaBH₄ described as a source of nucleophilic hydride?', 'It delivers H⁻ ions that attack the electron-deficient carbonyl carbon.', ['It releases H⁺ ions.', 'It produces H₂ gas only.', 'It is a strong acid.'], 'Nucleophilic addition.'),
    ('Why is the oxidation of alcohols also classed as a redox reaction?', 'The carbon bearing the –OH increases in oxidation state while Cr decreases.', ['Water is produced.', 'Oxygen gas is formed.', 'The alcohol gains hydrogen.'], 'Electron transfer.'),
])


# =============================================================================================
# ch08 R3.3 Electron sharing reactions (radicals)
# =============================================================================================
BONDS_H = [('Cl–Cl', 242), ('Br–Br', 193), ('F–F', 159), ('I–I', 151), ('C–H', 414), ('C–Cl', 324), ('C–Br', 285), ('C–F', 492), ('O=O', 498), ('H–H', 436), ('C–C', 346), ('C–I', 228), ('O–O', 144), ('H–Cl', 431)]
RADICALS = [('Cl•', True), ('CH₃•', True), ('NO', True), ('NO₂', True), ('•OH', True), ('Br•', True), ('C₂H₅•', True), ('ClO•', True), ('H•', True),
            ('Cl⁻', False), ('CH₃⁺', False), ('H₂O', False), ('NO₂⁺', False), ('CH₄', False), ('OH⁻', False), ('Br⁻', False), ('NH₃', False), ('N₂', False)]
MONO = [('methane', 1, 'chloromethane'), ('ethane', 1, 'chloroethane'), ('propane', 2, '1-chloropropane and 2-chloropropane'),
        ('butane', 2, '1-chlorobutane and 2-chlorobutane'), ('2-methylpropane', 2, '1-chloro-2-methylpropane and 2-chloro-2-methylpropane'),
        ('pentane', 3, '1-, 2- and 3-chloropentane'), ('2,2-dimethylpropane', 1, '1-chloro-2,2-dimethylpropane'), ('cyclohexane', 1, 'chlorocyclohexane'),
        ('2-methylbutane', 4, '1-chloro-2-methylbutane, 2-chloro-2-methylbutane, 2-chloro-3-methylbutane and 1-chloro-3-methylbutane'), ('hexane', 3, '1-, 2- and 3-chlorohexane')]
ALK_R = [('methane', 'CH4', 'CH₃•', 'CH3Cl', 'C2H6'), ('ethane', 'C2H6', 'C₂H₅•', 'C2H5Cl', 'C4H10'), ('propane', 'C3H8', 'C₃H₇•', 'C3H7Cl', 'C6H14')]
HALS = [('chlorine', 'Cl'), ('bromine', 'Br')]

R.facts('ch08-st1', F(
    terms=[('radical', 'a species with one or more unpaired electrons'),
           ('homolytic fission', 'the breaking of a covalent bond in which each atom takes one electron of the shared pair, forming two radicals'),
           ('heterolytic fission', 'the breaking of a covalent bond in which one atom takes both electrons of the shared pair, forming a cation and an anion'),
           ('fish-hook arrow', 'a half-headed curly arrow showing the movement of a single electron'),
           ('photodissociation', 'the breaking of a bond by absorption of a photon of sufficient energy (UV light)')],
    facts=[('What is needed to bring about homolytic fission of Cl₂ at room temperature?', 'ultraviolet light', ['a catalyst', 'an acid', 'infrared radiation'], 'UV photons break Cl–Cl (242 kJ mol⁻¹).'),
           ('Which species is a radical?', 'CH₃•', ['CH₃⁺', 'CH₃⁻', 'CH₄'], 'Unpaired electron.'),
           ('Homolytic fission of a C–Br bond produces', 'two radicals', ['a cation and an anion', 'two cations', 'two anions'], 'One electron each.'),
           ('Why are radicals very reactive?', 'They have an unpaired electron that readily forms a bond.', ['They are always charged.', 'They have full outer shells.', 'They are very large.'], 'Seek to pair electrons.'),
           ('Which bond is broken most easily by UV light?', 'I–I (151 kJ mol⁻¹)', ['C–F (492 kJ mol⁻¹)', 'C–H (414 kJ mol⁻¹)', 'H–H (436 kJ mol⁻¹)'], 'Weakest bond.'),
           ('Which arrow represents the movement of one electron?', 'a half-headed (fish-hook) arrow', ['a double-headed arrow', 'a straight arrow', 'an equilibrium arrow'], 'Radical mechanisms.')],
    why=[('Explain why homolytic fission usually needs UV light or high temperature.', 'Breaking a covalent bond requires energy equal to the bond enthalpy; UV photons (or high-temperature collisions) supply enough energy per molecule to break the bond evenly.'),
         ('Explain why the nitrogen monoxide molecule, NO, is a radical.', 'NO has an odd number of valence electrons (5 + 6 = 11), so one electron is necessarily unpaired.'),
         ('Explain why the C–F bond in CFCs is not broken in the stratosphere while the C–Cl bond is.', 'The C–F bond (492 kJ mol⁻¹) is much stronger than C–Cl (324 kJ mol⁻¹); the UV photons available have enough energy to break C–Cl but not C–F.'),
         ('Explain why visible light does not split chlorine molecules but UV light does.', 'Each photon’s energy is E = hc/λ; visible photons have too little energy to provide the 242 kJ mol⁻¹ needed per molecule, while shorter-wavelength UV photons have enough.')],
    contrast=[('homolytic fission', 'heterolytic fission', 'In homolytic fission each atom takes one electron, giving two radicals; in heterolytic fission one atom takes both electrons, giving ions.'),
              ('a radical', 'an ion', 'A radical has an unpaired electron and may be neutral; an ion has a charge from unequal numbers of protons and electrons, usually with all electrons paired.')],
    misc=[('All radicals carry a charge.', 'Most radicals (Cl•, CH₃•) are neutral; the defining feature is an unpaired electron.'),
          ('Homolytic fission produces a positive and a negative ion.', 'That describes heterolytic fission; homolytic fission produces two radicals.')],
    apply=[('Calculate the maximum wavelength of light that can break the Cl–Cl bond (242 kJ mol⁻¹).', 'E per bond = 242 000/6.02 × 10²³ = 4.02 × 10⁻¹⁹ J; λ = hc/E = 4.95 × 10⁻⁷ m (495 nm)', 3),
           ('Show, using fish-hook arrows, the homolytic fission of Br₂.', 'Two fish-hook arrows from the bond, one to each Br; Br₂ → 2Br•', 2)],
    evaluate=[('Radical reactions are too unselective to be useful in synthesis.', ['radical halogenation gives mixtures of isomers and polysubstitution', 'chain reactions are hard to control'], ['radical polymerisation makes poly(ethene) and many plastics', 'selective radical reactions exist (bromination prefers 3° C–H)', 'radical chemistry is vital in the atmosphere and biology'], 'They are less selective than ionic reactions but are industrially and biologically essential.'),
              ('Bond enthalpies are sufficient to predict which bond breaks in photodissociation.', ['weaker bonds need lower-energy photons', 'explains why C–Cl breaks before C–F'], ['the molecule must absorb at that wavelength', 'average bond enthalpies differ from specific bonds', 'quantum yield and competing processes matter'], 'Bond enthalpies give a good first prediction, but absorption spectra decide what actually happens.')],
    extended=[('Hydrogen peroxide decomposes in sunlight. (a) Draw the Lewis structure of H₂O₂. (b) Use the O–O bond enthalpy (144 kJ mol⁻¹) to calculate the maximum wavelength of light that breaks this bond. (c) Show the homolytic fission with fish-hook arrows. (d) Explain why the products are highly reactive.', '(a) H–O–O–H with two lone pairs on each O. (b) E = 144 000/6.02 × 10²³ = 2.39 × 10⁻¹⁹ J; λ = 8.31 × 10⁻⁷ m (831 nm). (c) H₂O₂ → 2•OH. (d) •OH radicals have an unpaired electron and react rapidly to pair it.', 7, 'multi_step')],
))


@R.add('ch08-st1', 'C3', (2, 5), 'numerical')
def c3_bond_lambda(rng, slot):
    b, e = pick(rng, BONDS_H)
    E = e * 1000 / NA
    lam = 6.63e-34 * 3.00e8 / E
    stem = pick(rng, [f'The bond enthalpy of {b} is {e} kJ mol⁻¹. Calculate the maximum wavelength of radiation, in nm, that can cause homolytic fission of this bond.',
                      f'Determine the longest wavelength (nm) of light able to break one {b} bond (bond enthalpy {e} kJ mol⁻¹) and state the region of the spectrum.'])
    region = 'ultraviolet' if lam < 400e-9 else 'visible' if lam < 700e-9 else 'infrared'
    return num(stem, q(lam * 1e9, 'nm'), f'E per bond = {e} × 10³/6.02 × 10²³ = {sf(E)} J (M1); λ = hc/E = {sf(lam)} m (M1) = {q(lam * 1e9, "nm")} ({region}) (A1).', 3)


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def c3_is_radical(rng, slot):
    kind = rng.choice([True, False])
    right = pick(rng, [r for r in RADICALS if r[1] == kind])
    wr = rng.sample([r for r in RADICALS if r[1] != kind], 3)
    stem = f'Which of {_lst(sorted(x[0] for x in [right] + wr))} {"is a radical" if kind else "is NOT a radical"}?'
    return mcq(rng, stem, right[0], [w[0] for w in wr], f'{right[0]} {"has an unpaired electron" if kind else "has all electrons paired"}.')


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def c3_weakest_bond(rng, slot):
    pool = rng.sample(BONDS_H, 4)
    kind = rng.choice(['longest', 'shortest'])
    best = (min if kind == 'longest' else max)(pool, key=lambda x: x[1])
    if [p[1] for p in pool].count(best[1]) > 1:
        return None
    stem = f'Using bond enthalpies, which bond, {_lst(p[0] for p in sorted(pool))}, can be broken homolytically by the radiation of {kind} wavelength?'
    return mcq(rng, stem, best[0], [p[0] for p in pool if p != best], 'Bond enthalpies / kJ mol⁻¹: ' + ', '.join(f'{p[0]} {p[1]}' for p in pool) + f'. {"Weakest bond needs lowest-energy (longest-λ) photons" if kind == "longest" else "Strongest bond needs highest-energy (shortest-λ) photons"}.')


@R.add('ch08-st1', 'C3', (1, 5), 'short')
def c3_fission_products(rng, slot):
    b, c, d = pick(rng, [('C–Cl in CH₃Cl', 'CH₃• + Cl•', 'CH₃⁺ + Cl⁻'), ('Br–Br', 'Br• + Br•', 'Br⁺ + Br⁻'), ('H–Cl', 'H• + Cl•', 'H⁺ + Cl⁻'),
                         ('C–Br in C₂H₅Br', 'C₂H₅• + Br•', 'C₂H₅⁺ + Br⁻'), ('O–O in H₂O₂', '•OH + •OH', 'OH⁺ + OH⁻ (unlikely)'), ('C–I in CH₃I', 'CH₃• + I•', 'CH₃⁺ + I⁻')])
    stem = f'State the products of (a) homolytic and (b) heterolytic fission of the {b} bond, and identify which fission gives radicals.'
    return dict(stem=stem, answer=f'(a) {c}; (b) {d}; homolytic gives radicals', markingKey=f'(a) {c} (1); (b) {d} (more electronegative atom takes the pair) (1); homolytic → radicals (1).', type='short', marks=3)


R.mcqs('ch08-st1', 'C2', (1, 4), [
    ('Why is the hydroxyl radical, •OH, different from the hydroxide ion, OH⁻?', '•OH has an unpaired electron and no charge; OH⁻ has an extra electron, all paired.', ['They are identical.', '•OH is positively charged.', 'OH⁻ is a radical.'], '9 vs 10 electrons.'),
    ('Why is a fish-hook arrow used in radical mechanisms?', 'It shows the movement of a single electron.', ['It shows a pair of electrons moving.', 'It shows heat being released.', 'It shows ions forming.'], 'Half-arrow.'),
    ('Why do non-polar bonds tend to undergo homolytic fission?', 'Neither atom has a strong tendency to take both electrons.', ['They are very weak.', 'They are ionic.', 'They contain lone pairs.'], 'Equal sharing.'),
    ('Why does chlorine react with methane in the dark only very slowly?', 'Without UV light, too few Cl–Cl bonds break to start the chain.', ['Methane is a radical.', 'The reaction is endothermic.', 'Chlorine is a liquid.'], 'Initiation needs UV.'),
])


# ---- ch08-st2 radical substitution ----
def rad_steps(alk, hal):
    nm, f, R_, prod, dimer = alk
    hn, X = hal
    Rf = R_.replace('•', '')
    steps = [('initiation', f'{X}₂ → 2{X}•'),
             ('propagation', f'{chem(f)} + {X}• → {R_} + H{X}'),
             ('propagation', f'{R_} + {X}₂ → {chem(prod.replace("Cl", X))} + {X}•'),
             ('termination', f'{X}• + {X}• → {X}₂'),
             ('termination', f'{R_} + {X}• → {chem(prod.replace("Cl", X))}'),
             ('termination', f'{R_} + {R_} → {chem(dimer)}')]
    return steps


R.facts('ch08-st2', F(
    terms=[('radical substitution', 'a reaction in which a hydrogen atom in an alkane is replaced by a halogen atom via a radical chain mechanism'),
           ('initiation', 'the step in a radical mechanism in which radicals are first formed, e.g. by UV light splitting X₂'),
           ('propagation', 'steps in which a radical reacts with a molecule to form a product and another radical, so the chain continues'),
           ('termination', 'steps in which two radicals combine to form a molecule, removing radicals and ending the chain'),
           ('chain reaction', 'a reaction in which the product of one step (a radical) starts the next step, so many cycles occur from one initiation')],
    facts=[('Which step is a termination step in the chlorination of methane?', 'CH₃• + Cl• → CH₃Cl', ['Cl₂ → 2Cl•', 'CH₄ + Cl• → CH₃• + HCl', 'CH₃• + Cl₂ → CH₃Cl + Cl•'], 'Two radicals combine.'),
           ('Why is a small amount of ethane formed when methane reacts with chlorine?', 'Two methyl radicals combine in a termination step.', ['Methane is impure.', 'Ethane is a propagation product.', 'Cl₂ reacts with CH₄ to give C₂H₆.'], 'CH₃• + CH₃• → C₂H₆.'),
           ('Which conditions are needed for the reaction of ethane with bromine?', 'UV light', ['concentrated H₂SO₄', 'a nickel catalyst', 'aqueous NaOH'], 'Radical initiation.'),
           ('What is the inorganic product in the propagation steps of methane chlorination?', 'hydrogen chloride', ['hydrogen', 'water', 'chloromethane'], 'CH₄ + Cl• → CH₃• + HCl.'),
           ('Why does radical substitution give a mixture of products?', 'Further substitution occurs and radicals can attack any C–H bond.', ['The reaction is reversible.', 'The catalyst is unselective.', 'The halogen is impure.'], 'Poly-substitution and isomers.'),
           ('How many radicals are consumed in a termination step?', 'two', ['one', 'none', 'three'], 'Radicals pair up.')],
    why=[('Explain why the propagation steps allow a small amount of UV light to convert a large amount of reactants.', 'Each propagation cycle uses one radical and produces another, so a single initiation can lead to thousands of cycles before termination occurs.'),
         ('Explain how dichloromethane can form when methane reacts with chlorine.', 'Chloromethane can itself react with Cl• (CH₃Cl + Cl• → CH₂Cl• + HCl), and CH₂Cl• reacts with Cl₂ to form CH₂Cl₂; excess methane reduces this.'),
         ('Explain why alkanes are generally unreactive but react with halogens in UV light.', 'C–C and C–H bonds are strong and non-polar, so most reagents do not attack them; halogen radicals formed by UV are reactive enough to abstract H atoms.'),
         ('Explain why using excess alkane favours the monosubstituted product.', 'Halogen radicals are then much more likely to collide with alkane molecules than with the halogenoalkane product, reducing further substitution.')],
    contrast=[('a propagation step', 'a termination step', 'A propagation step has one radical on each side (the chain continues); a termination step combines two radicals into a molecule (the chain stops).'),
              ('radical substitution', 'electrophilic addition', 'Radical substitution (alkanes + X₂, UV) replaces H with X via radicals; electrophilic addition (alkenes + X₂/HX) adds across C=C via ionic intermediates.')],
    misc=[('Termination steps are the main source of the product in radical substitution.', 'Most product forms in the propagation steps; termination steps are rare because radical concentrations are low.'),
          ('In the initiation step, chlorine splits into Cl⁺ and Cl⁻.', 'UV light causes homolytic fission into two Cl• radicals.')],
    apply=[('Write the initiation, two propagation steps and one termination step for the reaction of ethane with bromine in UV light.', 'Br₂ → 2Br•; C₂H₆ + Br• → C₂H₅• + HBr; C₂H₅• + Br₂ → C₂H₅Br + Br•; C₂H₅• + Br• → C₂H₅Br', 4),
           ('State the number of different monochlorinated products formed from propane and name them.', '2: 1-chloropropane and 2-chloropropane', 2)],
    evaluate=[('Radical substitution is a good method to make a single pure halogenoalkane.', ['simple reagents and conditions (X₂, UV)', 'useful for symmetrical alkanes (methane, cyclohexane)'], ['mixtures of isomers and polysubstituted products', 'separation needed, lowering yield and atom economy', 'alcohols + HX give a specific product'], 'It is poor for selective synthesis except with symmetrical alkanes; other routes are preferred.'),
              ('The mechanism of radical substitution is fully supported by evidence.', ['traces of termination products (ethane) are detected', 'reaction needs UV light and is inhibited by radical scavengers', 'one photon causes many reactions (chain)'], ['individual radicals are hard to observe directly', 'other mechanisms might also fit some observations'], 'The radical chain mechanism is well supported by multiple, independent lines of evidence.')],
    extended=[('Methane reacts with chlorine in sunlight. (a) Write equations for initiation, two propagation steps and two termination steps. (b) Explain why the reaction is described as a chain reaction. (c) Explain why a mixture of chloromethanes forms and how the yield of CH₃Cl can be increased. (d) Calculate the atom economy for CH₄ + Cl₂ → CH₃Cl + HCl.', '(a) Cl₂ → 2Cl•; CH₄ + Cl• → CH₃• + HCl; CH₃• + Cl₂ → CH₃Cl + Cl•; 2Cl• → Cl₂; CH₃• + CH₃• → C₂H₆. (b) radicals regenerated in propagation. (c) further substitution; use excess CH₄. (d) 50.48/(16.05 + 70.90) × 100 = 58.1 %.', 8, 'multi_step')],
))


@R.add('ch08-st2', 'C3', (1, 4), 'mcq')
def c3_step_type(rng, slot):
    alk = pick(rng, ALK_R)
    hal = pick(rng, HALS)
    steps = rad_steps(alk, hal)
    kind, eq = pick(rng, steps)
    stem = f'In the reaction of {alk[0]} with {hal[0]} in UV light, which type of step is {eq}?'
    return mcq(rng, stem, kind, [x for x in ['initiation', 'propagation', 'termination', 'heterolytic fission'] if x != kind], {'initiation': 'Radicals formed from a molecule.', 'propagation': 'One radical in, one radical out.', 'termination': 'Two radicals combine.'}[kind])


@R.add('ch08-st2', 'C3', (1, 4), 'mcq')
def c3_n_mono(rng, slot):
    nm, n, names = pick(rng, MONO)
    wr = [str(x) for x in sorted({n - 1, n + 1, n + 2, n * 2} - {n, 0})]
    rng.shuffle(wr)
    stem = pick(rng, [f'How many structurally different monochloro products can form when {nm} reacts with chlorine in UV light?', f'{cap(nm)} is chlorinated in UV light. How many different monosubstituted isomers are possible?'])
    return mcq(rng, stem, str(n), wr[:3], f'{n}: {names} (one per distinct hydrogen environment).')


@R.add('ch08-st2', 'C3', (1, 5), 'short')
def c3_write_steps(rng, slot):
    alk = pick(rng, ALK_R)
    hal = pick(rng, HALS)
    steps = rad_steps(alk, hal)
    want = pick(rng, ['initiation and the two propagation steps', 'the two propagation steps and two termination steps', 'one propagation step and the termination step that forms ' + chem(alk[4])])
    stem = f'For the reaction of {alk[0]} with {hal[0]} in ultraviolet light, write equations for {want}.'
    if want.startswith('initiation'):
        ans = '; '.join(e for k, e in steps[:3])
    elif want.startswith('the two'):
        ans = '; '.join(e for k, e in steps[1:5])
    else:
        ans = steps[1][1] + '; ' + steps[5][1]
    return dict(stem=stem, answer=ans, markingKey=f'{ans} (1 mark per correct equation; radicals shown with •).', type='short', marks=3 if want.startswith('init') else 4 if want.startswith('the two') else 2)


@R.add('ch08-st2', 'C3', (2, 4), 'mcq')
def c3_term_product(rng, slot):
    alk = pick(rng, ALK_R)
    hal = pick(rng, HALS)
    right = chem(alk[4])
    wr = [chem(a[4]) for a in ALK_R if a != alk] + [chem(alk[1]), chem(alk[3].replace('Cl', hal[1]))]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'Which hydrocarbon is formed in small amounts by a termination step when {alk[0]} reacts with {hal[0]} in UV light?'
    return mcq(rng, stem, right, wr[:3], f'{alk[2]} + {alk[2]} → {right}.')


R.mcqs('ch08-st2', 'C2', (1, 4), [
    ('Why is the reaction of methane with chlorine described as substitution?', 'A hydrogen atom is replaced by a chlorine atom.', ['Chlorine adds across a double bond.', 'Water is eliminated.', 'Two molecules join to form one.'], 'Replacement.'),
    ('Why are termination steps rare compared with propagation steps?', 'The concentration of radicals is very low, so radical–radical collisions are unlikely.', ['Termination needs UV light.', 'Termination is endothermic.', 'Radicals cannot combine.'], 'Low [radical].'),
    ('Why does the reaction of methane with chlorine stop soon after the UV light is switched off?', 'No new radicals are formed and existing ones are removed by termination.', ['Methane is used up immediately.', 'The products are unstable.', 'Chlorine evaporates.'], 'Chain ends.'),
    ('What is the role of UV light in the chlorination of alkanes?', 'It breaks Cl–Cl bonds homolytically to start the chain.', ['It acts as a catalyst for heterolysis.', 'It heats the alkane.', 'It ionises the alkane.'], 'Initiation.'),
])


# ---- ch08-st3 ozone depletion ----
CFCS = [('CCl3F', 'trichlorofluoromethane (CFC-11)'), ('CCl2F2', 'dichlorodifluoromethane (CFC-12)'), ('CClF3', 'chlorotrifluoromethane (CFC-13)'), ('C2Cl3F3', 'CFC-113'), ('CHClF2', 'chlorodifluoromethane (HCFC-22)')]

R.facts('ch08-st3', F(
    terms=[('ozone layer', 'the region of the stratosphere (15–35 km) with a relatively high concentration of ozone, O₃, which absorbs harmful UV radiation'),
           ('chlorofluorocarbon (CFC)', 'a compound of carbon, chlorine and fluorine, once used in refrigerants and aerosols, which releases Cl• radicals in the stratosphere'),
           ('catalytic cycle', 'a sequence of reactions in which a radical is consumed in one step and regenerated in a later step, so it destroys many ozone molecules'),
           ('Montreal Protocol', 'the 1987 international agreement to phase out the production of ozone-depleting substances such as CFCs'),
           ('stratosphere', 'the layer of the atmosphere from about 10 to 50 km above the Earth’s surface, containing the ozone layer')],
    facts=[('Which radical is mainly responsible for ozone depletion by CFCs?', 'Cl•', ['F•', 'CH₃•', 'H•'], 'C–Cl bond breaks.'),
           ('Why are CFCs stable in the lower atmosphere?', 'They are unreactive and insoluble, and the UV reaching low altitudes cannot break their bonds.', ['They react quickly with water.', 'They are radicals.', 'They are very soluble.'], 'Reach the stratosphere intact.'),
           ('Which equation represents the natural formation of ozone?', 'O₂ + O• → O₃', ['O₂ + O₂ → O₃ + O', 'O₃ + O• → 2O₂', 'Cl• + O₃ → ClO• + O₂'], 'After O₂ photolysis.'),
           ('Which gases also catalyse ozone depletion?', 'nitrogen oxides (NO and NO₂)', ['carbon dioxide', 'methane', 'argon'], 'NO• catalytic cycle.'),
           ('Why does ozone absorb UV radiation of longer wavelength than O₂?', 'The bonds in O₃ are weaker than the O=O double bond.', ['O₃ is a smaller molecule.', 'O₃ has a double bond stronger than O₂.', 'O₃ is ionic.'], 'Bond order 1.5.'),
           ('Which compounds were introduced as less harmful replacements for CFCs?', 'HFCs (hydrofluorocarbons)', ['HCs only', 'Halons', 'CCl₄'], 'No chlorine.')],
    why=[('Explain why a single chlorine radical can destroy thousands of ozone molecules.', 'Cl• reacts with O₃ to form ClO• and O₂, and ClO• reacts with O• to regenerate Cl•; Cl• is a catalyst that is not used up until a termination reaction removes it.'),
         ('Explain why the ozone layer is important for life on Earth.', 'Ozone absorbs harmful high-energy UV-B and UV-C radiation, which damages DNA, causing skin cancer, cataracts and harm to crops and plankton.'),
         ('Explain why HFCs do not deplete ozone even though they reach the stratosphere.', 'They contain no chlorine or bromine; C–F and C–H bonds are too strong to release radicals that catalyse ozone breakdown.'),
         ('Explain why the ozone hole forms mainly over Antarctica in spring.', 'Polar stratospheric clouds form in the extreme winter cold, and reactions on their surfaces convert reservoir compounds into Cl₂; when sunlight returns in spring, Cl₂ photolyses into Cl• that rapidly destroys ozone.')],
    contrast=[('ozone in the stratosphere', 'ozone in the troposphere', 'Stratospheric ozone is beneficial, absorbing UV; tropospheric (ground-level) ozone is a harmful pollutant formed in photochemical smog.'),
              ('natural ozone depletion', 'catalysed ozone depletion', 'Naturally, O₃ is broken down by UV and O• and re-formed in a steady state; catalysed depletion by Cl• or NO• accelerates breakdown and lowers the steady-state concentration.')],
    misc=[('CFCs damage ozone because they react directly with O₃ molecules.', 'The CFC must first be split by UV in the stratosphere to release Cl• radicals; it is the Cl• that catalyses O₃ destruction.'),
          ('The ozone hole is caused mainly by carbon dioxide.', 'The ozone hole is caused by chlorine and bromine compounds (CFCs, halons); CO₂ is linked with global warming, not ozone depletion.')],
    apply=[('Write equations to show how Cl• radicals are formed from CCl₂F₂ and how they catalyse the decomposition of ozone.', 'CCl₂F₂ → CClF₂• + Cl• (UV); Cl• + O₃ → ClO• + O₂; ClO• + O• → Cl• + O₂; overall O₃ + O• → 2O₂', 4),
           ('Show how NO acts as a catalyst for ozone depletion.', 'NO• + O₃ → NO₂• + O₂; NO₂• + O• → NO• + O₂', 2)],
    evaluate=[('The Montreal Protocol is the most successful environmental treaty ever.', ['nearly universal ratification; CFC production almost eliminated', 'ozone layer projected to recover by about 2060', 'also reduced greenhouse forcing'], ['CFCs persist for decades; recovery is slow', 'replacement HFCs are powerful greenhouse gases (needed Kigali amendment)', 'illegal emissions have been detected'], 'It is a remarkable success, though recovery is slow and replacements created new problems.'),
              ('Replacing CFCs with HFCs solved the problems caused by CFCs.', ['HFCs do not deplete ozone', 'similar useful properties (non-toxic, non-flammable)'], ['HFCs are potent greenhouse gases', 'they are being phased down under the Kigali amendment', 'alternatives (hydrocarbons, CO₂, HFOs) have other drawbacks'], 'HFCs solved ozone depletion but contributed to climate change, so further replacement is under way.')],
    extended=[('In the stratosphere, O₂ and O₃ absorb UV radiation. (a) Write equations for the photodissociation of O₂ and O₃ and for the formation of O₃. (b) The O=O bond enthalpy is 498 kJ mol⁻¹; calculate the maximum wavelength that can break it. (c) Explain how chlorine radicals disturb this steady state, with equations. (d) Explain why the effect persists for decades.', '(a) O₂ → 2O•; O₃ → O₂ + O•; O₂ + O• → O₃. (b) E = 8.27 × 10⁻¹⁹ J; λ = 2.40 × 10⁻⁷ m = 240 nm. (c) Cl• + O₃ → ClO• + O₂; ClO• + O• → Cl• + O₂ – catalytic, faster breakdown. (d) CFCs have long lifetimes and each Cl• destroys many O₃ molecules before termination.', 8, 'multi_step')],
))


@R.add('ch08-st3', 'C3', (1, 4), 'mcq')
def c3_cfc_radical(rng, slot):
    f, nm = pick(rng, CFCS)
    a = atoms(f)
    if a.get('C', 0) == 1:
        rest = dict(a)
        rest['Cl'] -= 1
        frag = 'C' + ''.join(f'{e}{rest[e] if rest[e] > 1 else ""}' for e in ('H', 'Cl', 'F') if rest.get(e))
        right = f'{chem(f)} → {chem(frag)}• + Cl•'
        rest2 = dict(a)
        rest2['F'] -= 1
        frag2 = 'C' + ''.join(f'{e}{rest2[e] if rest2[e] > 1 else ""}' for e in ('H', 'Cl', 'F') if rest2.get(e))
        wr = [f'{chem(f)} → {chem(frag2)}• + F•', f'{chem(f)} → {chem(frag)}⁺ + Cl⁻', f'{chem(f)} + O₃ → {chem(frag)}O + ClO₂']
    else:
        right = 'C₂Cl₂F₃• + Cl•'
        wr = ['C₂Cl₃F₂• + F•', 'C₂Cl₂F₃⁺ + Cl⁻', 'C₂Cl₃F₃⁺ + e⁻']
    stem = f'Which equation shows the first step in the breakdown of {nm} in the stratosphere?'
    return mcq(rng, stem, right, wr, 'UV light breaks the weakest bond, C–Cl (324 kJ mol⁻¹), homolytically; C–F (492 kJ mol⁻¹) is not broken.')


@R.add('ch08-st3', 'C3', (1, 4), 'mcq')
def c3_cycle_role(rng, slot):
    cyc = pick(rng, [('Cl• + O₃ → ClO• + O₂; ClO• + O• → Cl• + O₂', 'Cl•', 'ClO•'), ('NO• + O₃ → NO₂• + O₂; NO₂• + O• → NO• + O₂', 'NO•', 'NO₂•'),
                     ('Br• + O₃ → BrO• + O₂; BrO• + O• → Br• + O₂', 'Br•', 'BrO•'), ('•OH + O₃ → HO₂• + O₂; HO₂• + O₃ → •OH + 2O₂', '•OH', 'HO₂•')])
    steps, cat, inter = cyc
    kind = rng.choice(['catalyst', 'intermediate', 'overall'])
    if kind == 'overall':
        right = '2O₃ → 3O₂' if 'HO₂• + O₃' in steps else 'O₃ + O• → 2O₂'
        wr = ['O₂ + O• → O₃', '2O₃ → 3O₂' if right != '2O₃ → 3O₂' else 'O₃ + O• → 2O₂', f'{cat} + O₃ → {inter} + O₂']
        stem = f'What is the overall equation for the cycle {steps}?'
        return mcq(rng, stem, right, wr, 'Add the steps and cancel species on both sides.')
    right = cat if kind == 'catalyst' else inter
    wr = [x for x in [cat, inter, 'O₃', 'O₂', 'O•'] if x != right]
    stem = f'In the cycle {steps}, which species acts as the {kind}?'
    return mcq(rng, stem, right, wr[:3], f'{cat} is used and regenerated (catalyst); {inter} is formed then used (intermediate).')


@R.add('ch08-st3', 'C3', (2, 4), 'numerical')
def c3_ozone_lambda(rng, slot):
    sp, e = pick(rng, [('O₂ (O=O)', 498), ('O₃ (O–O in ozone)', 362), ('CCl₂F₂ (C–Cl)', 324), ('CCl₂F₂ (C–F)', 492), ('ClO• (Cl–O)', 269)])
    E = e * 1000 / NA
    lam = 6.63e-34 * 3.00e8 / E
    stem = f'The bond enthalpy for the bond broken in {sp} is {e} kJ mol⁻¹. Calculate the maximum wavelength of radiation, in nm, that can break this bond.'
    return num(stem, q(lam * 1e9, 'nm'), f'E = {e} × 10³/6.02 × 10²³ = {sf(E)} J (M1); λ = hc/E (M1) = {q(lam * 1e9, "nm")} (A1).', 3)


R.mcqs('ch08-st3', 'C2', (1, 4), [
    ('Why does a chlorine radical act as a catalyst in ozone depletion?', 'It is regenerated at the end of each cycle.', ['It lowers the energy of ozone.', 'It is a product of the overall reaction.', 'It increases the rate of ozone formation.'], 'Not consumed.'),
    ('Why does UV light break C–Cl but not C–F bonds in CFCs?', 'The C–Cl bond is weaker, so lower-energy photons are sufficient.', ['C–F bonds absorb visible light.', 'Fluorine is less electronegative.', 'C–Cl is ionic.'], 'Bond enthalpy.'),
    ('Why is it a problem that CFCs are very stable in the troposphere?', 'They survive long enough to diffuse up to the stratosphere.', ['They react with ozone at ground level.', 'They cause acid rain.', 'They are greenhouse gases only.'], 'Long lifetime.'),
    ('Which statement explains why ozone formation and depletion are in a steady state without pollutants?', 'The rates of ozone formation and breakdown by UV are equal.', ['No reactions occur.', 'Ozone is not affected by UV.', 'Oxygen does not absorb UV.'], 'Chapman cycle.'),
])


@p1b(R, 'ch08-st3')
def p1b_ozone_data(rng, slot):
    yrs = [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020]
    base = rng.randint(300, 320)
    minv = rng.randint(95, 120)
    vals = []
    for y in yrs:
        if y <= 2000:
            v = base - (base - minv) * (y - 1980) / 20
        else:
            v = minv + (y - 2000) * rng.uniform(0.8, 1.6)
        vals.append(round(v))
    tab = '\n'.join(f'{y} | {v}' for y, v in zip(yrs, vals))
    r1 = (vals[4] - vals[0]) / 20
    r2 = (vals[-1] - vals[4]) / 20
    intro = f'The minimum ozone column over Antarctica each October (Dobson units, DU) is shown.\n\nyear | minimum ozone / DU\n{tab}'
    return dict(intro=intro, parts=[
        ('Calculate the mean rate of change of minimum ozone between 1980 and 2000.', f'{r1:.1f} DU per year', f'({vals[4]} − {vals[0]})/20 (M1) = {r1:.1f} DU yr⁻¹ (A1).', 2),
        ('Calculate the mean rate of change between 2000 and 2020 and comment on the trend.', f'+{r2:.1f} DU per year – slow recovery', f'({vals[-1]} − {vals[4]})/20 = {r2:.1f} DU yr⁻¹ (A1); slow recovery after the Montreal Protocol (R1).', 2),
        ('Explain why the recovery is much slower than the decline.', 'CFCs already in the atmosphere have lifetimes of 50–100 years and each Cl• destroys many O₃ molecules before termination.', 'Long atmospheric lifetimes of CFCs (1); catalytic Cl• (1).', 2),
        ('Write two equations showing how Cl• catalyses ozone destruction.', 'Cl• + O₃ → ClO• + O₂; ClO• + O• → Cl• + O₂', 'Each equation (1 + 1).', 2)],
        extras=[('Suggest one reason why year-to-year values fluctuate.', 'Variations in stratospheric temperature and polar vortex strength change the extent of ozone loss.', 'Meteorological variation (1).', 1)])


# =============================================================================================
# ch09 R3.4 Electron-pair sharing: nucleophilic substitution
# =============================================================================================
NUCS = ['OH⁻', 'H₂O', 'NH₃', 'CN⁻', 'Cl⁻', 'Br⁻', 'I⁻', 'CH₃O⁻', 'CH₃NH₂', 'H⁻ (from NaBH₄)']
ELECS = ['H⁺', 'NO₂⁺', 'Br⁺', 'CH₃⁺', '(CH₃)₃C⁺', 'BF₃', 'AlCl₃', 'the δ+ carbon of C=O', 'the δ+ carbon of C–Br', 'Cl⁺']
HET = [('C–Cl in chloromethane', 'CH₃⁺ and Cl⁻'), ('H–Br', 'H⁺ and Br⁻'), ('C–Br in 2-bromo-2-methylpropane', '(CH₃)₃C⁺ and Br⁻'), ('C–I in iodoethane', 'C₂H₅⁺ and I⁻'),
       ('H–Cl', 'H⁺ and Cl⁻'), ('O–H in water', 'H⁺ and OH⁻'), ('Br–Br polarised by FeBr₃', 'Br⁺ and Br⁻ (as FeBr₄⁻)'), ('C–Cl in 2-chloro-2-methylbutane', 'C₅H₁₁⁺ and Cl⁻')]
HALO = [o for o in ORG if o[3] == 'halogenoalkane']
SUBST_OH = {'chloromethane': 'methanol', 'bromoethane': 'ethanol', '1-bromopropane': 'propan-1-ol', '2-bromopropane': 'propan-2-ol', '1-chlorobutane': 'butan-1-ol',
            '2-chlorobutane': 'butan-2-ol', '2-bromo-2-methylpropane': '2-methylpropan-2-ol', '1-iodobutane': 'butan-1-ol', '2-chloro-2-methylbutane': '2-methylbutan-2-ol'}
SUBST_NH3 = {'chloromethane': 'methylamine', 'bromoethane': 'ethylamine', '1-bromopropane': 'propan-1-amine', '1-chlorobutane': 'butan-1-amine', '1-iodobutane': 'butan-1-amine', '2-bromopropane': 'propan-2-amine'}
SUBST_CN = {'chloromethane': 'ethanenitrile', 'bromoethane': 'propanenitrile', '1-bromopropane': 'butanenitrile', '1-chlorobutane': 'pentanenitrile', '1-iodobutane': 'pentanenitrile'}

R.facts('ch09-st1', F(
    terms=[('nucleophile', 'an electron-rich species with a lone pair that it donates to an electron-deficient atom to form a new covalent bond'),
           ('electrophile', 'an electron-deficient species that accepts a pair of electrons to form a new covalent bond'),
           ('heterolytic fission', 'the breaking of a covalent bond in which both electrons go to one atom, forming a cation and an anion'),
           ('curly arrow', 'a full-headed arrow showing the movement of a pair of electrons, from a lone pair or bond to an atom or bond'),
           ('carbocation', 'an ion with a positively charged carbon atom that has only three bonds (six outer electrons)'),
           ('leaving group', 'the atom or group (e.g. a halide ion) that departs with the bonding pair when a bond breaks heterolytically')],
    facts=[('Which species is a nucleophile?', 'CN⁻', ['NO₂⁺', 'H⁺', 'BF₃'], 'Lone pair donor.'),
           ('Which species is an electrophile?', 'NO₂⁺', ['NH₃', 'OH⁻', 'H₂O'], 'Electron-pair acceptor.'),
           ('Where does a curly arrow start?', 'at a lone pair or a covalent bond', ['at a positive charge', 'at an atom nucleus', 'at an empty orbital'], 'Arrows show electron pairs moving.'),
           ('In heterolytic fission of C–Br, which atom takes the bonding pair?', 'bromine', ['carbon', 'both equally', 'neither'], 'More electronegative atom.'),
           ('Which is the best description of a carbocation?', 'a positively charged carbon species with three bonds', ['a carbon radical', 'a negatively charged carbon', 'a carbon with five bonds'], 'Electrophile.'),
           ('Why is the carbon atom in a C–Cl bond attacked by nucleophiles?', 'Chlorine is more electronegative, making carbon δ+.', ['Carbon has a lone pair.', 'The bond is non-polar.', 'Chlorine is δ+.'], 'Polar bond.')],
    why=[('Explain why water can act as a nucleophile.', 'The oxygen atom has two lone pairs and a partial negative charge, so it can donate a lone pair to an electron-deficient carbon.'),
         ('Explain why polar bonds tend to break heterolytically.', 'The more electronegative atom already has a greater share of the bonding pair, so it tends to take both electrons when the bond breaks, forming ions.'),
         ('Explain why a negatively charged nucleophile such as OH⁻ is usually stronger than its neutral conjugate acid, H₂O.', 'The negative charge means the lone pairs are higher in energy and more strongly attracted to a δ+ centre, so OH⁻ donates them more readily.'),
         ('Explain the meaning of a curly arrow drawn from the C–Br bond to the Br atom.', 'Both electrons of the C–Br bond move onto bromine, breaking the bond heterolytically and forming Br⁻.')],
    contrast=[('a nucleophile', 'an electrophile', 'A nucleophile is an electron-pair donor attracted to δ+ centres; an electrophile is an electron-pair acceptor attracted to electron-rich regions.'),
              ('a full-headed curly arrow', 'a fish-hook arrow', 'A full-headed arrow shows the movement of an electron pair (ionic mechanisms); a fish-hook arrow shows a single electron (radical mechanisms).')],
    misc=[('All negative ions are electrophiles.', 'Negative ions with lone pairs are nucleophiles; electrophiles are electron-deficient (often positive).'),
          ('Curly arrows show the movement of atoms.', 'Curly arrows show the movement of electron pairs, not atoms.')],
    apply=[('Classify each species as a nucleophile or electrophile: NH₃, H⁺, Br⁻, CH₃⁺, H₂O, NO₂⁺.', 'nucleophiles: NH₃, Br⁻, H₂O; electrophiles: H⁺, CH₃⁺, NO₂⁺', 3),
           ('Draw curly arrows to show the heterolytic fission of the C–Br bond in 2-bromo-2-methylpropane.', 'Arrow from C–Br bond to Br; (CH₃)₃C⁺ + Br⁻', 2)],
    evaluate=[('Curly-arrow mechanisms are a realistic description of reactions.', ['predict products, stereochemistry and rate equations', 'consistent with kinetic and isotopic evidence'], ['they are simplified models of continuous electron density changes', 'transition states and solvent effects are not shown'], 'Curly arrows are a powerful predictive model, though a simplified one.'),
              ('The nucleophile/electrophile classification is more useful than the Lewis acid/base classification in organic chemistry.', ['focuses on attack on carbon, explaining mechanisms', 'directly linked to curly-arrow mechanisms'], ['it is essentially the same idea as Lewis theory', 'Lewis theory is more general across inorganic chemistry'], 'They describe the same electron-pair donation; nucleophile/electrophile is simply the organic chemist’s language for it.')],
    extended=[('Bromoethane reacts with aqueous hydroxide ions. (a) Identify the nucleophile and the electrophilic centre. (b) Explain why the carbon is electrophilic. (c) Draw the mechanism with curly arrows. (d) Name the organic product and state the type of reaction.', '(a) OH⁻; the carbon bonded to Br. (b) Br is more electronegative → C δ+. (c) arrow from OH⁻ lone pair to C; arrow from C–Br bond to Br; transition state; products. (d) ethanol; nucleophilic substitution.', 7, 'multi_step')],
))


@R.add('ch09-st1', 'C3', (1, 4), 'mcq')
def c3_nuc_pick(rng, slot):
    kind = rng.choice(['nucleophile', 'electrophile'])
    right = pick(rng, NUCS if kind == 'nucleophile' else ELECS)
    wr = rng.sample(ELECS if kind == 'nucleophile' else NUCS, 3)
    stem = f'Which of {_lst(sorted([right] + wr))} can act as {"a nucleophile" if kind == "nucleophile" else "an electrophile"}?'
    return mcq(rng, stem, right, wr, f'{right} {"has a lone pair to donate" if kind == "nucleophile" else "is electron-deficient and accepts a pair"}.')


@R.add('ch09-st1', 'C3', (1, 4), 'mcq')
def c3_het_products(rng, slot):
    b, prods = pick(rng, HET)
    wr = [p for _, p in HET if p != prods]
    rng.shuffle(wr)
    first = prods.split(' and ')
    wr = [f'{first[0].replace("⁺", "•")} and {first[1].replace("⁻", "•")}' if '⁺' in first[0] else 'two radicals', f'{first[0].replace("⁺", "⁻")} and {first[1].replace("⁻", "⁺")}'] + wr
    wr = [w for w in dict.fromkeys(wr) if w != prods]
    stem = f'What are the products of heterolytic fission of the {b} bond?'
    return mcq(rng, stem, prods, wr[:3], 'The more electronegative atom takes both bonding electrons.')


@R.add('ch09-st1', 'C3', (1, 5), 'short')
def c3_arrows(rng, slot):
    h = pick(rng, HALO)
    nuc = pick(rng, ['OH⁻', 'CN⁻', 'NH₃', 'H₂O'])
    stem = f'Describe, in words, the curly arrows needed to show the first step of the reaction between {nuc} and {h[0]} ({oc(h)}).'
    X = 'Br' if 'Br' in h[1] else 'Cl' if 'Cl' in h[1] else 'I'
    return dict(stem=stem, answer=f'An arrow from a lone pair on {nuc} to the δ+ carbon bonded to {X}; an arrow from the C–{X} bond to the {X} atom.', markingKey=f'Arrow from lone pair (not charge) of {nuc} to C (1); arrow from C–{X} bond to {X} (1).', type='short', marks=2)


R.mcqs('ch09-st1', 'C2', (1, 4), [
    ('Why is NH₃ a nucleophile but NH₄⁺ is not?', 'NH₃ has a lone pair; in NH₄⁺ all electron pairs are bonding.', ['NH₄⁺ is negatively charged.', 'NH₃ is a cation.', 'NH₄⁺ has two lone pairs.'], 'Lone pair needed.'),
    ('Why does a C–I bond break more easily than a C–F bond?', 'The C–I bond is longer and weaker.', ['Iodine is more electronegative.', 'C–I is more polar.', 'C–F has a lone pair.'], 'Bond enthalpy 228 vs 492.'),
    ('Why are carbocations electrophiles?', 'The positive carbon has an incomplete octet and accepts an electron pair.', ['They have lone pairs.', 'They are radicals.', 'They are negatively charged.'], 'Six electrons.'),
    ('Which statement about heterolytic fission is correct?', 'It produces oppositely charged ions.', ['It produces two radicals.', 'It requires UV light.', 'Both atoms take one electron.'], 'Unequal split.'),
])


# ---- ch09-st2 SN1 and SN2 (HL) ----
R.facts('ch09-st2', F(
    terms=[('SN2 mechanism', 'a one-step bimolecular nucleophilic substitution in which the nucleophile attacks as the leaving group departs, via a single transition state'),
           ('SN1 mechanism', 'a two-step unimolecular nucleophilic substitution in which the leaving group departs first to form a carbocation, which is then attacked by the nucleophile'),
           ('transition state', 'the highest-energy, partially bonded arrangement of atoms in a reaction step'),
           ('inversion of configuration', 'the reversal of the 3D arrangement around a chiral carbon (like an umbrella turning inside out) that occurs in SN2'),
           ('racemisation', 'formation of a 50:50 mixture of enantiomers, as when a planar carbocation is attacked equally from both sides in SN1')],
    facts=[('Which mechanism is typical for a tertiary halogenoalkane?', 'SN1', ['SN2', 'radical substitution', 'electrophilic addition'], 'Stable 3° carbocation, steric hindrance.'),
           ('What is the rate equation for an SN2 reaction of RX with OH⁻?', 'rate = k[RX][OH⁻]', ['rate = k[RX]', 'rate = k[OH⁻]', 'rate = k[RX]²'], 'Both in the single step.'),
           ('Why does a tertiary halogenoalkane react by SN1?', 'The tertiary carbocation is stabilised by three electron-releasing alkyl groups.', ['Tertiary carbons have no hydrogen.', 'Tertiary halogenoalkanes are less polar.', 'It reacts via radicals.'], 'Inductive effect.'),
           ('What happens to the stereochemistry when an optically active 2-bromobutane reacts by SN2?', 'inversion of configuration', ['racemisation', 'retention', 'no change'], 'Backside attack.'),
           ('Which halogenoalkane reacts fastest by SN2?', 'bromomethane', ['2-bromo-2-methylpropane', '2-bromopropane', '2-bromobutane'], 'Least steric hindrance.'),
           ('How many steps are there in an SN1 mechanism?', 'two', ['one', 'three', 'four'], 'Ionisation then attack.')],
    why=[('Explain why primary halogenoalkanes react by SN2 rather than SN1.', 'Primary carbocations are very unstable (only one electron-releasing alkyl group), and the carbon is not crowded, so the nucleophile can attack from the back in a single step.'),
         ('Explain why the SN1 rate equation does not include the nucleophile.', 'The rate-determining first step is the ionisation of the halogenoalkane to a carbocation; the nucleophile only reacts in the fast second step.'),
         ('Explain why an SN1 reaction of an optically active halogenoalkane gives a racemic mixture.', 'The intermediate carbocation is planar (sp²), so the nucleophile attacks equally from either face, giving equal amounts of both enantiomers.'),
         ('Explain why tertiary halogenoalkanes do not react by SN2.', 'Three bulky alkyl groups block the backside approach of the nucleophile to the carbon (steric hindrance).')],
    contrast=[('SN1', 'SN2', 'SN1: two steps via a carbocation, rate = k[RX], favoured by tertiary substrates, racemisation; SN2: one concerted step, rate = k[RX][Nu], favoured by primary substrates, inversion.'),
              ('a transition state', 'a carbocation intermediate', 'A transition state is an energy maximum with partial bonds; a carbocation is an intermediate in an energy minimum between two transition states.')],
    misc=[('Secondary halogenoalkanes only react by SN1.', 'Secondary halogenoalkanes can react by either mechanism, depending on the nucleophile and solvent.'),
          ('In SN1 the nucleophile and the halogenoalkane collide in the rate-determining step.', 'In SN1 the slow step involves only the halogenoalkane ionising; the nucleophile reacts in the fast second step.')],
    apply=[('State the mechanism and rate equation for the hydrolysis of 2-bromo-2-methylpropane by aqueous NaOH.', 'SN1; rate = k[(CH₃)₃CBr]', 2),
           ('Draw the SN2 mechanism for bromoethane with OH⁻, including the transition state.', 'Arrow from OH⁻ to C; arrow C–Br → Br; transition state [HO···CH₂(CH₃)···Br]⁻ with partial bonds; products ethanol + Br⁻', 4)],
    evaluate=[('The SN1/SN2 classification fully explains nucleophilic substitution.', ['explains the effect of substrate structure, kinetics and stereochemistry', 'predicts rate equations'], ['many secondary substrates react by mixed mechanisms', 'solvent effects and ion pairs complicate the picture', 'elimination competes'], 'The two limiting mechanisms are very useful but real reactions often lie between them.'),
              ('Stereochemical evidence is the strongest evidence for the SN2 mechanism.', ['inversion of configuration is observed for chiral substrates', 'cannot be explained by a carbocation'], ['kinetic evidence (second order) is equally important', 'achiral substrates show no stereochemical change'], 'Stereochemical inversion is compelling, but together with kinetic data it provides the strongest case.')],
    extended=[('(R)-2-bromobutane is hydrolysed under two different conditions. (a) Draw the SN2 mechanism and state the stereochemistry of the product. (b) Draw the SN1 mechanism and explain the stereochemistry of the product. (c) Write rate equations for both. (d) Suggest how the conditions could favour SN1.', '(a) backside attack, inversion → (S)-butan-2-ol. (b) planar secondary carbocation, attack from both faces → racemic butan-2-ol. (c) SN2 rate = k[RBr][OH⁻]; SN1 rate = k[RBr]. (d) polar protic solvent (water), weak nucleophile, low [OH⁻].', 9, 'multi_step')],
))


@R.add('ch09-st2', 'C3', (1, 4), 'mcq')
def c3_sn_mech(rng, slot):
    h = pick(rng, HALO)
    deg = h[4]
    right = {1: 'SN2', 2: 'SN1 or SN2 (depending on conditions)', 3: 'SN1'}[deg]
    wr = [x for x in ['SN2', 'SN1', 'SN1 or SN2 (depending on conditions)', 'radical substitution'] if x != right]
    stem = f'By which mechanism does {h[0]}, {oc(h)}, mainly react with aqueous hydroxide ions?'
    return mcq(rng, stem, right, wr, f'{h[0]} is {"primary" if deg == 1 else "secondary" if deg == 2 else "tertiary"} → {right}.')


@R.add('ch09-st2', 'C3', (1, 4), 'mcq')
def c3_sn_rate(rng, slot):
    h = pick(rng, [x for x in HALO if x[4] in (1, 3)])
    nuc = pick(rng, [('OH⁻', 'aqueous sodium hydroxide'), ('CN⁻', 'potassium cyanide in ethanol'), ('NH₃', 'excess ammonia in ethanol')])
    rx = f'[{chem(h[2])}]'
    right = f'rate = k{rx}[{nuc[0]}]' if h[4] == 1 else f'rate = k{rx}'
    wr = [f'rate = k{rx}', f'rate = k{rx}[{nuc[0]}]', f'rate = k[{nuc[0]}]', f'rate = k{rx}²[{nuc[0]}]']
    wr = [w for w in wr if w != right]
    stem = f'What is the rate equation for the reaction of {h[0]} with {nuc[1]}?'
    return mcq(rng, stem, right, wr[:3], f'{"Primary → SN2: both reactants in the one step" if h[4] == 1 else "Tertiary → SN1: only RX in the slow step"}.')


@R.add('ch09-st2', 'C3', (1, 4), 'mcq')
def c3_sn_product(rng, slot):
    h = pick(rng, HALO)
    kind = pick(rng, ['OH', 'NH3', 'CN'])
    table = {'OH': SUBST_OH, 'NH3': SUBST_NH3, 'CN': SUBST_CN}[kind]
    if h[0] not in table:
        return None
    right = table[h[0]]
    pool = list(dict.fromkeys(list(SUBST_OH.values()) + list(SUBST_NH3.values()) + list(SUBST_CN.values())))
    wr = [x for x in pool if x != right]
    rng.shuffle(wr)
    reag = {'OH': 'warm aqueous sodium hydroxide', 'NH3': 'excess ammonia in ethanol, heated in a sealed tube', 'CN': 'potassium cyanide in ethanol under reflux'}[kind]
    stem = f'What is the organic product when {h[0]} reacts with {reag}?'
    return mcq(rng, stem, right, wr[:3], f'The nucleophile replaces the halogen: {right}' + (' (the carbon chain is extended by one).' if kind == 'CN' else '.'))


@R.add('ch09-st2', 'C3', (2, 5), 'short')
def c3_stereo_outcome(rng, slot):
    sub = pick(rng, ['(R)-2-bromobutane', '(S)-2-bromobutane', '(R)-2-chlorobutane', '(S)-2-iodobutane', '(R)-3-bromo-3-methylhexane', '(S)-3-chloro-3-methylhexane'])
    tert = 'methylhexane' in sub
    mech = 'SN1' if tert else rng.choice(['SN1', 'SN2'])
    prod = sub.replace('bromo', 'ol').replace('chloro', 'ol').replace('iodo', 'ol')
    if tert:
        prod_name = '3-methylhexan-3-ol'
    else:
        prod_name = 'butan-2-ol'
    flip = '(S)' if '(R)' in sub else '(R)'
    ans = f'{flip}-{prod_name} (inversion of configuration)' if mech == 'SN2' else f'racemic {prod_name} (equal amounts of (R) and (S))'
    stem = f'{cap(sub)} reacts with hydroxide ions by an {mech} mechanism. Predict the stereochemistry of the product and explain your answer.'
    why = 'backside attack by OH⁻ inverts the arrangement of groups (Walden inversion)' if mech == 'SN2' else 'the planar carbocation intermediate is attacked equally from both faces'
    return dict(stem=stem, answer=f'{ans}: {why}.', markingKey=f'{ans} (1); {why} (1–2).', type='short', marks=3)


R.mcqs('ch09-st2', 'C2', (1, 4), [
    ('Why is the rate of an SN1 reaction independent of the nucleophile concentration?', 'The nucleophile reacts only in the fast step after the rate-determining ionisation.', ['The nucleophile is a catalyst.', 'There is no nucleophile in SN1.', 'The nucleophile is always in excess.'], 'Slow step involves RX only.'),
    ('Why are tertiary carbocations more stable than primary carbocations?', 'Three alkyl groups donate electron density to the positive carbon.', ['They have more hydrogen atoms.', 'They are radicals.', 'They are smaller.'], 'Positive inductive effect.'),
    ('In an SN2 transition state, how many groups are partially or fully bonded to the central carbon?', 'five', ['four', 'three', 'six'], 'Nu···C···X plus three substituents.'),
    ('Why does steric hindrance slow SN2 reactions?', 'Bulky groups block the nucleophile’s approach to the back of the carbon.', ['It makes the C–X bond stronger.', 'It destabilises carbocations.', 'It changes the leaving group.'], 'Backside attack blocked.'),
])


@p1b(R, 'ch09-st2')
def p1b_sn_kinetics(rng, slot):
    sub = pick(rng, [('2-bromo-2-methylpropane', 1, 0, 'SN1'), ('1-bromobutane', 1, 1, 'SN2')])
    nm, m, n, mech = sub
    k = rng.uniform(1, 9) * 10 ** rng.choice([-4, -3])
    a0 = rng.choice([0.010, 0.020])
    b0 = rng.choice([0.010, 0.020])
    rows = [(a0, b0), (2 * a0, b0), (a0, 2 * b0)]
    tab = '\n'.join(f'{i + 1} | {sf(x)} | {sf(y)} | {sf(k * x ** m * y ** n)}' for i, (x, y) in enumerate(rows))
    intro = f'The initial rate of hydrolysis of {nm} (RBr) by hydroxide ions was measured at 298 K.\n\nexperiment | [RBr] / mol dm⁻³ | [OH⁻] / mol dm⁻³ | initial rate / mol dm⁻³ s⁻¹\n{tab}'
    o = m + n
    return dict(intro=intro, parts=[
        ('Deduce the orders with respect to RBr and OH⁻.', f'{m} and {n}', f'exp 1→2: rate ×2 → first order in RBr (A1); exp 1→3: rate ×{2 ** n} → order {n} in OH⁻ (A1).', 2),
        ('Write the rate equation and calculate k with units.', f'rate = k[RBr]{"[OH⁻]" if n else ""}; k = {q(k, kunit(o))}', f'rate equation (A1); k = {sf(k)} (A1) {kunit(o)} (A1).', 3),
        ('Deduce the mechanism and explain how the data support it.', f'{mech}: ' + ('only RBr in the rate-determining step (carbocation formation)' if mech == 'SN1' else 'both RBr and OH⁻ in one concerted step'), f'{mech} (1); link to orders (1).', 2),
        ('Explain why the temperature of the reaction mixtures was controlled.', 'The rate constant depends strongly on temperature.', 'k varies with T (1).', 1)],
        extras=[('Suggest a method for following the rate of this reaction.', 'Measure conductivity (ions change) or quench samples and titrate remaining OH⁻ with acid.', 'Valid method (1).', 1)])


# ---- ch09-st3 factors affecting nucleophilic substitution ----
CX = [('C–F', 492), ('C–Cl', 324), ('C–Br', 285), ('C–I', 228)]

R.facts('ch09-st3', F(
    terms=[('leaving group ability', 'the ease with which a group departs with the bonding pair; better leaving groups form weaker bonds to carbon and stable anions (I⁻ > Br⁻ > Cl⁻ > F⁻)'),
           ('protic solvent', 'a solvent with O–H or N–H bonds (e.g. water, ethanol) that can hydrogen-bond to ions; favours SN1'),
           ('aprotic solvent', 'a polar solvent without O–H or N–H bonds (e.g. propanone) that does not solvate nucleophiles strongly; favours SN2'),
           ('nucleophilicity', 'the relative ability of a species to donate a lone pair to carbon in a substitution reaction'),
           ('steric hindrance', 'the slowing of a reaction because bulky groups block the approach of the attacking species')],
    facts=[('Which halogenoalkane is hydrolysed fastest by aqueous OH⁻?', '1-iodobutane', ['1-chlorobutane', '1-bromobutane', '1-fluorobutane'], 'C–I weakest bond.'),
           ('Which nucleophile reacts faster with bromoethane?', 'OH⁻', ['H₂O', 'both equally', 'neither reacts'], 'Charged nucleophile stronger.'),
           ('Which solvent type favours SN1 reactions?', 'polar protic (e.g. water)', ['non-polar (e.g. hexane)', 'aprotic (e.g. propanone)', 'no solvent'], 'Stabilises carbocation and anion.'),
           ('Why is the C–F bond rarely broken in nucleophilic substitution?', 'It is the strongest carbon–halogen bond.', ['F is the least electronegative halogen.', 'It is non-polar.', 'Fluoroalkanes are radicals.'], '492 kJ mol⁻¹.'),
           ('Which factor mainly determines the relative rates of hydrolysis of chloro-, bromo- and iodoalkanes?', 'the carbon–halogen bond enthalpy', ['the bond polarity', 'the molar mass', 'the solubility in water'], 'Bond strength outweighs polarity.'),
           ('With aqueous silver nitrate in ethanol, which halogenoalkane gives a precipitate most quickly?', '2-iodo-2-methylpropane', ['1-chlorobutane', '1-bromobutane', 'chlorobenzene'], 'Tertiary + weakest C–X.')],
    why=[('Explain why iodoalkanes are hydrolysed faster than chloroalkanes even though the C–Cl bond is more polar.', 'The C–I bond is much weaker (228 vs 324 kJ mol⁻¹), so it breaks more easily; bond strength matters more than polarity in determining the rate.'),
         ('Explain why polar protic solvents favour the SN1 mechanism.', 'They stabilise the carbocation and the leaving anion by solvation (ion–dipole/hydrogen bonding), lowering the energy of the ionisation step.'),
         ('Explain why aprotic solvents favour SN2 reactions.', 'They do not hydrogen-bond to the nucleophile, so the anion is less solvated and more reactive towards the carbon.'),
         ('Explain why hydroxide ions are better nucleophiles than water molecules.', 'OH⁻ carries a full negative charge, so its lone pairs are more available and it is more strongly attracted to the δ+ carbon.')],
    contrast=[('the effect of the leaving group', 'the effect of the nucleophile', 'The leaving group affects both SN1 and SN2 rates (weaker C–X bond → faster); the nucleophile’s strength affects SN2 rates but not SN1 rates.'),
              ('a protic solvent', 'an aprotic solvent', 'A protic solvent has O–H or N–H bonds and solvates anions strongly (favours SN1); an aprotic solvent lacks them and leaves nucleophiles more reactive (favours SN2).')],
    misc=[('Chloroalkanes are hydrolysed fastest because the C–Cl bond is the most polar of the C–Cl, C–Br and C–I bonds.', 'Rate depends mainly on bond strength; C–I is weakest, so iodoalkanes react fastest.'),
          ('A stronger nucleophile always increases the rate of substitution.', 'A stronger nucleophile increases the SN2 rate but has no effect on SN1, whose rate-determining step does not involve the nucleophile.')],
    apply=[('Predict the order of hydrolysis rates for 1-chlorobutane, 1-bromobutane and 1-iodobutane with aqueous silver nitrate and describe the observations.', 'iodo > bromo > chloro; yellow AgI fastest, cream AgBr, white AgCl slowest', 3),
           ('Suggest a solvent and nucleophile that would favour SN2 for converting 1-bromopropane into propan-1-ol.', 'OH⁻ (aqueous NaOH or in a polar aprotic solvent) – strong nucleophile, primary substrate', 2)],
    evaluate=[('Bond enthalpy is the single most important factor in the rate of nucleophilic substitution.', ['explains I > Br > Cl > F trend clearly', 'affects both SN1 and SN2'], ['substrate structure (1°/2°/3°) changes the mechanism and rate hugely', 'nucleophile and solvent effects can be large', 'polarity plays some role'], 'Bond enthalpy dominates the halogen trend, but structure, nucleophile and solvent are equally important overall.'),
              ('The silver nitrate test is a reliable way to identify the halogen in a halogenoalkane.', ['precipitate colours differ (AgCl white, AgBr cream, AgI yellow)', 'rate of formation shows relative C–X reactivity'], ['colours are hard to distinguish', 'confirmation with ammonia solubility is needed', 'mass spectrometry (isotope patterns) is more definitive'], 'It is a useful qualitative test but needs confirmation.')],
    extended=[('A student compares the rates of hydrolysis of 1-chlorobutane, 1-bromobutane and 1-iodobutane using aqueous silver nitrate in ethanol at 50 °C. (a) Write an equation for the hydrolysis of 1-bromobutane by water. (b) Explain why silver nitrate is used. (c) Predict and explain the order of reactivity. (d) Identify two variables that must be controlled.', '(a) C₄H₉Br + H₂O → C₄H₉OH + H⁺ + Br⁻. (b) Ag⁺ + X⁻ → AgX(s); time for precipitate measures rate. (c) iodo > bromo > chloro – C–X bond enthalpies 228 < 285 < 324 kJ mol⁻¹. (d) temperature, volumes/concentrations, same chain length/structure.', 8, 'multi_step')],
))


@R.add('ch09-st3', 'C3', (1, 4), 'mcq')
def c3_rate_rank(rng, slot):
    chain = pick(rng, [('1-', 'butane'), ('2-', '-2-methylpropane'), ('1-', 'propane'), ('', 'ethane')])
    names = {'C–Cl': 'chloro', 'C–Br': 'bromo', 'C–I': 'iodo', 'C–F': 'fluoro'}
    pool = rng.sample(CX, 3)
    kind = rng.choice(['fastest', 'slowest'])
    best = (min if kind == 'fastest' else max)(pool, key=lambda x: x[1])
    def nmf(b):
        if chain[1].startswith('-'):
            return f'2-{names[b[0]]}{chain[1]}'
        return f'{chain[0]}{names[b[0]]}{chain[1]}'
    others = [nmf(b) for b in pool if b != best] + [f'they all react at the same rate']
    stem = f'Which of {_lst(nmf(b) for b in pool)} is hydrolysed {kind} by aqueous hydroxide ions under the same conditions?'
    return mcq(rng, stem, nmf(best), others[:3], 'Bond enthalpies / kJ mol⁻¹: ' + ', '.join(f'{b[0]} {b[1]}' for b in pool) + '. Weaker bond → faster substitution.')


@R.add('ch09-st3', 'C3', (1, 4), 'mcq')
def c3_factor_change(rng, slot):
    h = pick(rng, HALO)
    deg = h[4]
    changes = [('replacing OH⁻ by H₂O as the nucleophile', 'decreases' if deg == 1 else 'has little effect on'),
               ('doubling the concentration of OH⁻', 'doubles' if deg == 1 else 'has no effect on'),
               ('replacing the halogen by iodine', 'increases'),
               ('using a polar aprotic solvent instead of water', 'increases' if deg == 1 else 'decreases'),
               ('raising the temperature by 10 °C', 'increases')]
    ch, eff = pick(rng, changes)
    right = f'{eff} the rate'
    wr = [x for x in ['increases the rate', 'decreases the rate', 'has no effect on the rate', 'doubles the rate', 'has little effect on the rate'] if x != right and not (right == 'has no effect on the rate' and x == 'has little effect on the rate') and not (right == 'has little effect on the rate' and x == 'has no effect on the rate')]
    rng.shuffle(wr)
    stem = f'For the substitution reaction of {h[0]} ({"primary, SN2" if deg == 1 else "secondary" if deg == 2 else "tertiary, SN1"}) with hydroxide ions, what is the effect of {ch}?'
    if deg == 2 and ch in [c for c, _ in changes[:2]] + [changes[3][0]]:
        return None
    return mcq(rng, stem, right, wr[:3], f'{ch}: {"SN2 rate depends on [Nu] and nucleophile strength" if deg == 1 else "SN1 rate depends only on [RX] and carbocation formation"}.')


@R.add('ch09-st3', 'C3', (1, 4), 'mcq')
def c3_agno3(rng, slot):
    COL = {'Cl': 'white', 'Br': 'cream', 'I': 'yellow'}
    hx = {X: [o for o in HALO if X in o[1]] for X in COL}
    T = pick(rng, [40, 50, 60])
    kind = rng.choice(['obs', 'which', 'which', 'order'])
    if kind == 'obs':
        X = pick(rng, [x for x in COL if hx[x]])
        h = pick(rng, hx[X])
        stem = f'A few drops of {h[0]} ({oc(h)}) are added to ethanolic silver nitrate in a water bath at {T} °C. What is seen after several minutes?'
        right = f'a {COL[X]} precipitate of Ag{X}'
        wr = [f'a {c} precipitate of Ag{x}' for x, c in COL.items() if x != X] + [pick(rng, ['no change', 'a brown precipitate of Ag₂O', 'a silver mirror'])]
        return mcq(rng, stem, right, wr, f'Water hydrolyses the C–{X} bond; Ag⁺ + {X}⁻ → Ag{X}(s), {COL[X]}.')
    if kind == 'which':
        X = pick(rng, [x for x in COL if hx[x]])
        h = pick(rng, hx[X])
        others = [o for x in COL if x != X for o in hx[x]]
        if len(others) < 3:
            return None
        wr = [o[0] for o in rng.sample(others, 3)]
        stem = f'Which compound from {_lst(sorted([h[0]] + wr))} gives a {COL[X]} precipitate when warmed to {T} °C with silver nitrate in aqueous ethanol?'
        return mcq(rng, stem, h[0], wr, f'{COL[X]} precipitate = Ag{X}, so the compound contains C–{X}.')
    trio = []
    for X in ('Cl', 'Br', 'I'):
        cand = [o for o in hx[X] if o[4] == 1] if hx[X] and any(o[4] == 1 for o in hx[X]) else hx[X]
        if not cand:
            return None
        trio.append(pick(rng, cand)[0])
    right = ' > '.join([trio[2], trio[1], trio[0]])
    wr = [' > '.join(trio), ' > '.join([trio[1], trio[2], trio[0]]), ' > '.join([trio[0], trio[2], trio[1]])]
    shown = trio[:]
    rng.shuffle(shown)
    stem = f'{_lst(shown)} are each warmed with ethanolic silver nitrate at {T} °C. What is the order in which precipitates appear, fastest first?'
    return mcq(rng, stem, right, wr, 'C–I (228) < C–Br (285) < C–Cl (324 kJ mol⁻¹): the weakest bond is hydrolysed fastest.')


R.mcqs('ch09-st3', 'C2', (1, 4), [
    ('Why does the rate of SN1 depend on the stability of the carbocation?', 'Carbocation formation is the rate-determining step; a more stable carbocation forms faster.', ['The carbocation is the nucleophile.', 'Stability affects only SN2.', 'The leaving group is a carbocation.'], 'Rate-determining step.'),
    ('Why does a protic solvent slow SN2 reactions with anionic nucleophiles?', 'It hydrogen-bonds to the nucleophile, making it less available.', ['It stabilises the transition state.', 'It removes the halogen.', 'It reacts with the halogenoalkane.'], 'Solvation shell.'),
    ('Why is fluoroethane almost inert to hydrolysis?', 'The C–F bond is very strong.', ['Fluorine is a good leaving group.', 'C–F is non-polar.', 'Fluoroethane is insoluble.'], '492 kJ mol⁻¹.'),
    ('Why does 2-bromo-2-methylpropane hydrolyse faster in water than 1-bromobutane?', 'It forms a stable tertiary carbocation, so the SN1 pathway is fast in water.', ['It has a stronger C–Br bond.', 'It is a primary halogenoalkane.', 'Water is a stronger nucleophile for it.'], 'SN1 in protic solvent.'),
])


# =============================================================================================
# ch10 R3.4 Electron-pair sharing: electrophilic addition and substitution (HL)
# =============================================================================================
# alkene: (name, molecular formula, symmetrical?, {reagent: (major, minor or None)}, carbocation for major, degree)
ALK = [
    ('ethene', 'C2H4', True, {'HBr': ('bromoethane', None), 'HCl': ('chloroethane', None), 'HI': ('iodoethane', None),
                               'Br₂': ('1,2-dibromoethane', None), 'H₂O': ('ethanol', None), 'H₂': ('ethane', None)}, 'CH₃CH₂⁺', 'primary'),
    ('propene', 'C3H6', False, {'HBr': ('2-bromopropane', '1-bromopropane'), 'HCl': ('2-chloropropane', '1-chloropropane'), 'HI': ('2-iodopropane', '1-iodopropane'),
                                 'Br₂': ('1,2-dibromopropane', None), 'H₂O': ('propan-2-ol', 'propan-1-ol'), 'H₂': ('propane', None)}, 'CH₃CH⁺CH₃', 'secondary'),
    ('but-1-ene', 'C4H8', False, {'HBr': ('2-bromobutane', '1-bromobutane'), 'HCl': ('2-chlorobutane', '1-chlorobutane'), 'HI': ('2-iodobutane', '1-iodobutane'),
                                   'Br₂': ('1,2-dibromobutane', None), 'H₂O': ('butan-2-ol', 'butan-1-ol'), 'H₂': ('butane', None)}, 'CH₃CH₂CH⁺CH₃', 'secondary'),
    ('but-2-ene', 'C4H8', True, {'HBr': ('2-bromobutane', None), 'HCl': ('2-chlorobutane', None), 'HI': ('2-iodobutane', None),
                                  'Br₂': ('2,3-dibromobutane', None), 'H₂O': ('butan-2-ol', None), 'H₂': ('butane', None)}, 'CH₃CH⁺CH₂CH₃', 'secondary'),
    ('2-methylpropene', 'C4H8', False, {'HBr': ('2-bromo-2-methylpropane', '1-bromo-2-methylpropane'), 'HCl': ('2-chloro-2-methylpropane', '1-chloro-2-methylpropane'),
                                         'HI': ('2-iodo-2-methylpropane', '1-iodo-2-methylpropane'), 'Br₂': ('1,2-dibromo-2-methylpropane', None),
                                         'H₂O': ('2-methylpropan-2-ol', '2-methylpropan-1-ol'), 'H₂': ('2-methylpropane', None)}, '(CH₃)₃C⁺', 'tertiary'),
    ('pent-1-ene', 'C5H10', False, {'HBr': ('2-bromopentane', '1-bromopentane'), 'HCl': ('2-chloropentane', '1-chloropentane'), 'HI': ('2-iodopentane', '1-iodopentane'),
                                     'Br₂': ('1,2-dibromopentane', None), 'H₂O': ('pentan-2-ol', 'pentan-1-ol'), 'H₂': ('pentane', None)}, 'CH₃CH₂CH₂CH⁺CH₃', 'secondary'),
    ('2-methylbut-2-ene', 'C5H10', False, {'HBr': ('2-bromo-2-methylbutane', '2-bromo-3-methylbutane'), 'HCl': ('2-chloro-2-methylbutane', '2-chloro-3-methylbutane'),
                                            'HI': ('2-iodo-2-methylbutane', '2-iodo-3-methylbutane'), 'Br₂': ('2,3-dibromo-2-methylbutane', None),
                                            'H₂O': ('2-methylbutan-2-ol', '3-methylbutan-2-ol'), 'H₂': ('2-methylbutane', None)}, '(CH₃)₂C⁺CH₂CH₃', 'tertiary'),
    ('cyclohexene', 'C6H10', True, {'HBr': ('bromocyclohexane', None), 'HCl': ('chlorocyclohexane', None), 'HI': ('iodocyclohexane', None),
                                     'Br₂': ('1,2-dibromocyclohexane', None), 'H₂O': ('cyclohexanol', None), 'H₂': ('cyclohexane', None)}, 'C₆H₁₁⁺ (secondary)', 'secondary'),
]
ALK_D = {a[0]: a for a in ALK}
REAG_COND = {'HBr': 'hydrogen bromide gas or concentrated solution at room temperature', 'HCl': 'hydrogen chloride at room temperature',
             'HI': 'hydrogen iodide at room temperature', 'Br₂': 'bromine (or bromine water) at room temperature',
             'H₂O': 'steam with a phosphoric(V) acid catalyst at about 300 °C and 6 MPa', 'H₂': 'hydrogen with a nickel catalyst at about 150 °C'}
ADD_FORM = {'HBr': 'Br', 'HCl': 'Cl', 'HI': 'I', 'Br₂': 'Br2', 'H₂O': 'H2O', 'H₂': 'H2'}


def _add_mr(alk, reag):
    base = atoms(alk[1])
    add = atoms({'HBr': 'HBr', 'HCl': 'HCl', 'HI': 'HI', 'Br₂': 'Br2', 'H₂O': 'H2O', 'H₂': 'H2'}[reag])
    return sum(AR[e] * n for e, n in base.items()) + sum(AR[e] * n for e, n in add.items())


R.facts('ch10-st1', F(
    terms=[('electrophilic addition', 'a reaction in which an electrophile attacks the electron-rich C=C double bond and two species add across it, forming a saturated product'),
           ("Markovnikov's rule", 'when HX adds to an unsymmetrical alkene, the hydrogen atom adds to the carbon that already has more hydrogen atoms, so X bonds to the more substituted carbon'),
           ('carbocation intermediate', 'the positively charged species formed when the electrophile bonds to one carbon of the C=C bond, leaving the other carbon with only three bonds'),
           ('positive inductive effect', 'the donation of electron density through σ bonds by alkyl groups, which stabilises an adjacent positive charge'),
           ('induced dipole (in Br₂)', 'the temporary polarisation of the Br–Br bond, Brᵟ⁺–Brᵟ⁻, caused by repulsion from the electron-rich π bond of an approaching alkene'),
           ('unsymmetrical alkene', 'an alkene in which the two carbon atoms of the C=C bond carry different groups, so addition of HX can give two different products')],
    facts=[('Which species is the electrophile when HBr adds to ethene?', 'the δ+ hydrogen atom of HBr', ['Br⁻', 'the π electrons of ethene', 'the δ− bromine atom'], 'H attacks the π bond first.'),
           ('What is observed when bromine water is shaken with an alkene?', 'The orange-brown colour disappears.', ['A white precipitate forms.', 'The solution turns purple.', 'No change.'], 'Br₂ is used up by addition.'),
           ('Which carbocation is the most stable?', 'tertiary', ['primary', 'secondary', 'methyl'], 'Three alkyl groups donate electron density.'),
           ('What is the major product of HBr adding to propene?', '2-bromopropane', ['1-bromopropane', '1,2-dibromopropane', 'propan-2-ol'], 'Via the secondary carbocation.'),
           ('Which part of an alkene is attacked by electrophiles?', 'the π bond of C=C', ['the C–H σ bonds', 'the carbon nuclei', 'the C–C σ bond only'], 'Electron-rich region above and below the plane.'),
           ('How many steps are there in the electrophilic addition of HBr to an alkene?', 'two', ['one', 'three', 'four'], 'Carbocation formation, then Br⁻ attack.')],
    why=[('Explain why alkenes undergo addition rather than substitution reactions.', 'The π bond is weaker than the σ bond and its electrons are exposed above and below the plane, so electrophiles attack it; breaking only the π bond and forming two new σ bonds is energetically favourable.'),
         ('Explain why a non-polar bromine molecule can act as an electrophile.', 'As Br₂ approaches the electron-rich π bond, electron repulsion induces a dipole, Brᵟ⁺–Brᵟ⁻; the δ+ bromine accepts the π electron pair and the Br–Br bond breaks heterolytically.'),
         ('Explain, in terms of carbocation stability, why propene forms more 2-bromopropane than 1-bromopropane with HBr.', 'Addition of H⁺ to the terminal carbon gives a secondary carbocation, which is stabilised by two alkyl groups (positive inductive effect); it forms faster than the primary carbocation, so its product, 2-bromopropane, is major.'),
         ('Explain why but-2-ene gives only one product with HBr.', 'The alkene is symmetrical: H⁺ adding to either carbon of C=C gives the same secondary carbocation, so only 2-bromobutane forms.'),
         ('Explain why the decolourisation of bromine water distinguishes hexene from hexane.', 'Hexene adds bromine across its C=C bond at room temperature, removing the orange colour; hexane, being saturated, reacts only by radical substitution in UV light, so the colour remains in the dark.')],
    contrast=[('the major product', 'the minor product of HBr addition to propene', 'The major product (2-bromopropane) forms via the more stable secondary carbocation; the minor product (1-bromopropane) forms via the less stable primary carbocation.'),
              ('electrophilic addition to alkenes', 'nucleophilic substitution of halogenoalkanes', 'In addition the electron-rich C=C is attacked by an electrophile and nothing leaves; in substitution a nucleophile attacks a δ+ carbon and a halide leaving group is replaced.'),
              ('a primary carbocation', 'a tertiary carbocation', 'A primary carbocation has one alkyl group on the positive carbon and is least stable; a tertiary carbocation has three alkyl groups donating electron density and is most stable.')],
    misc=[("Markovnikov's rule says the bromine adds to the carbon with more hydrogen atoms.", 'The hydrogen adds to the carbon with more hydrogens; bromine ends up on the more substituted carbon.'),
          ('The second step of HBr addition is attack by Br⁺.', 'The second step is attack by the nucleophile Br⁻ on the carbocation.'),
          ('Bromine reacts with alkenes because Br₂ is a polar molecule.', 'Br₂ is non-polar; a dipole is induced by the π electrons of the alkene.')],
    apply=[('Draw the mechanism for the reaction of propene with hydrogen bromide to form the major product.', 'Arrow from C=C to H of HBr; arrow from H–Br bond to Br; secondary carbocation CH₃CH⁺CH₃ and Br⁻; arrow from Br⁻ lone pair to C⁺; product 2-bromopropane.', 4),
           ('Predict the major product when 2-methylpropene reacts with steam in the presence of an acid catalyst and explain your answer.', '2-methylpropan-2-ol; H⁺ adds to CH₂ to give the tertiary carbocation (CH₃)₃C⁺, which is most stable and is then attacked by water.', 3)],
    evaluate=[("Markovnikov's rule is a reliable way of predicting the products of addition reactions.", ['correctly predicts the major product of HX and H₂O addition to unsymmetrical alkenes', 'explained by carbocation stability'], ['it gives only the major product – mixtures still form', 'it does not apply to symmetrical alkenes, Br₂ or H₂ addition, or to reactions that do not go via carbocations'], "The rule is reliable for ionic HX/H₂O additions, and is best understood as a consequence of carbocation stability rather than as a law."),
              ('Bromine water is a definitive test for an alkene.', ['rapid decolourisation at room temperature in the dark', 'simple and cheap'], ['other unsaturated compounds (alkynes) also decolourise it', 'phenols and some other compounds react with bromine water', 'it does not identify which alkene is present'], 'It is a good test for C=C unsaturation, but confirmation needs further evidence such as IR or ¹H NMR.')],
    extended=[('Propene reacts with hydrogen bromide. (a) State the type of reaction. (b) Draw the mechanism leading to the major product. (c) Explain why this product is major. (d) Suggest how the ratio of products could be measured.', '(a) electrophilic addition. (b) curly arrows from π bond to H, from H–Br to Br; CH₃CH⁺CH₃; Br⁻ attacks C⁺ → 2-bromopropane. (c) secondary carbocation more stable than primary (two alkyl groups, positive inductive effect) → forms faster. (d) gas chromatography or ¹H NMR peak ratios of the mixture.', 8, 'multi_step')],
))


@R.add('ch10-st1', 'C3', (1, 4), 'mcq')
def c3_add_major(rng, slot):
    a = pick(rng, ALK)
    reag = pick(rng, list(a[3]))
    maj, mnr = a[3][reag]
    wr = [w for w in [mnr] + [a[3][r][0] for r in a[3] if r != reag] if w and w != maj]
    wr = list(dict.fromkeys(wr))
    if len(wr) < 3:
        return None
    rng.shuffle(wr)
    if mnr:
        wr = [mnr] + [w for w in wr if w != mnr]
    stem = f'What is the major organic product when {a[0]} reacts with {REAG_COND[reag].split(" at ")[0].split(" with ")[0] if reag != "H₂O" else "steam"} ({reag}) under suitable conditions?'
    why = f'{maj} forms via the {a[5]} carbocation {a[4]}' if reag in ('HBr', 'HCl', 'HI', 'H₂O') and mnr else f'{reag} adds across the C=C bond to give {maj}'
    return mcq(rng, stem, maj, wr[:3], why + '.')


@R.add('ch10-st1', 'C3', (1, 4), 'mcq')
def c3_carbocation(rng, slot):
    a = pick(rng, [x for x in ALK if not x[2]])
    reag = pick(rng, ['HBr', 'HCl', 'HI', 'H₂O'])
    deg = a[5]
    opts = ['primary', 'secondary', 'tertiary', 'methyl']
    wr = [o for o in opts if o != deg]
    stem = f'In the reaction of {a[0]} with {reag}, which type of carbocation intermediate leads to the major product, {a[3][reag][0]}?'
    return mcq(rng, stem, deg, wr, f'{a[4]} is {deg}; the more substituted carbocation is more stable.')


@R.add('ch10-st1', 'C3', (1, 4), 'mcq')
def c3x_one_product(rng, slot):
    sym = [x[0] for x in ALK if x[2]] + ['2,3-dimethylbut-2-ene', 'hex-3-ene']
    uns = [x[0] for x in ALK if not x[2]] + ['hex-1-ene', '2-methylbut-1-ene']
    if rng.random() < 0.5:
        right = pick(rng, sym)
        wr = rng.sample(uns, 3)
        stem = f'Which alkene from {_lst(sorted([right] + wr))} gives only one structural isomer on reaction with HBr?'
        key = f'{right} is symmetrical about C=C.'
    else:
        right = pick(rng, uns)
        wr = rng.sample(sym, 3)
        stem = f'Which alkene from {_lst(sorted([right] + wr))} gives a mixture of two structural isomers on reaction with HCl?'
        key = f'{right} is unsymmetrical, so Markovnikov and anti-Markovnikov products form.'
    return mcq(rng, stem, right, wr, key)


@R.add('ch10-st1', 'C3', (1, 5), 'short')
def c3_markov_explain(rng, slot):
    a = pick(rng, [x for x in ALK if not x[2]])
    reag = pick(rng, ['HBr', 'HCl', 'HI', 'H₂O'])
    maj, mnr = a[3][reag]
    stem = f'{cap(a[0])} reacts with {reag}. Name the major and minor organic products and explain which is major.'
    ans = f'major: {maj}; minor: {mnr}. The major product forms via the more stable {a[5]} carbocation ({a[4]}), stabilised by the positive inductive effect of its alkyl groups.'
    return dict(stem=stem, answer=ans, markingKey=f'{maj} major (1); {mnr} minor (1); {a[5]} carbocation more stable / more alkyl groups donating (1).', type='short', marks=3)


@R.add('ch10-st1', 'C3', (1, 5), 'numerical')
def c3_add_mass(rng, slot):
    a = pick(rng, ALK)
    reag = pick(rng, ['HBr', 'Br₂', 'H₂O', 'HCl'])
    m = rsf(rng.uniform(1.0, 12.0), 3)
    Ma = mr(a[1])
    Mp = _add_mr(a, reag)
    n = m / Ma
    mp = n * Mp
    prod = a[3][reag][0]
    rd = {'HBr': 'hydrogen bromide', 'HCl': 'hydrogen chloride', 'Br₂': 'bromine', 'H₂O': 'steam (with an acid catalyst)'}[reag]
    if slot.d <= 2:
        stem = f'Calculate the maximum mass of {prod} that can form when {q(m, "g")} of {a[0]} reacts completely with excess {rd}.'
        return num(stem, q(mp, 'g'), f'n({a[0]}) = {sf(m)}/{Ma:.2f} = {sf(n)} mol (M1); 1 : 1 → m = {sf(n)} × {Mp:.2f} = {q(mp, "g")} (A1).', 2)
    y = rng.randint(55, 92)
    act = mp * y / 100
    stem = f'{q(m, "g")} of {a[0]} reacted with excess {rd} and {q(act, "g")} of {prod} was isolated. Calculate the percentage yield.'
    return num(stem, f'{y:.0f} %' if abs(act / mp * 100 - y) < 0.5 else f'{act / mp * 100:.1f} %',
               f'n = {sf(m)}/{Ma:.2f} = {sf(n)} mol (M1); theoretical mass = {q(mp, "g")} (M1); yield = {sf(act)}/{sf(mp)} × 100 = {act / mp * 100:.0f} % (A1).', 3)


DIENES = [('cyclohexene', 'C6H10', 1), ('hexa-1,5-diene', 'C6H10', 2), ('buta-1,3-diene', 'C4H6', 2), ('limonene', 'C10H16', 2),
          ('myrcene', 'C10H16', 3), ('oct-1-ene', 'C8H16', 1), ('cycloocta-1,5-diene', 'C8H12', 2), ('hexa-1,3,5-triene', 'C6H8', 3)]


@R.add('ch10-st1', 'C3', (2, 5), 'numerical')
def c3_cc_count(rng, slot):
    nm, f_, k = pick(rng, DIENES)
    M = mr(f_)
    nh = rsf(rng.uniform(0.0020, 0.0060), 3)
    m = nh * M
    rg = pick(rng, ['Br₂', 'H₂'])
    if rg == 'Br₂':
        c = pick(rng, [0.100, 0.200, 0.250])
        V = nh * k / c * 1000
        stem = f'A sample of {q(m, "g")} of an unsaturated hydrocarbon {chem(f_)} decolourised exactly {q(V, "cm³")} of {q(c, "mol dm⁻³")} bromine solution. Deduce the number of C=C double bonds in one molecule.'
        key = f'n(hydrocarbon) = {sf(m)}/{M:.2f} = {sf(nh)} mol (M1); n(Br₂) = {sf(V)} × 10⁻³ × {sf(c)} = {sf(nh * k)} mol (M1); ratio = {k} (A1).'
    else:
        V = nh * k * VM * 1000
        stem = f'{q(m, "g")} of a hydrocarbon {chem(f_)} reacted completely with {q(V, "cm³")} of hydrogen at STP in the presence of a nickel catalyst. Deduce the number of C=C double bonds in one molecule (molar volume = 22.7 dm³ mol⁻¹).'
        key = f'n(hydrocarbon) = {sf(nh)} mol (M1); n(H₂) = {sf(V)}/22700 = {sf(nh * k)} mol (M1); ratio = {k} (A1).'
    return num(stem, str(k), key, 3)


R.mcqs('ch10-st1', 'C2', (1, 4), [
    ('Why does the C=C bond of an alkene attract electrophiles?', 'It is a region of high electron density due to the π bond.', ['It is positively charged.', 'It has a lone pair.', 'It is polar.'], 'Exposed π electrons.'),
    ('Why does HBr react with alkenes faster than HCl does?', 'The H–Br bond is weaker than the H–Cl bond, so it breaks more easily.', ['HBr is more polar.', 'Bromine is more electronegative.', 'HCl is a gas.'], 'Bond enthalpy 366 vs 431 kJ mol⁻¹.'),
    ('Why is a tertiary carbocation more stable than a secondary one?', 'More alkyl groups push electron density towards the positive carbon.', ['It has more hydrogen atoms.', 'It is a radical.', 'It is planar.'], 'Positive inductive effect.'),
    ('Why is the product of adding Br₂ to ethene saturated?', 'The π bond is broken and every carbon forms four single bonds.', ['A C=C bond is formed.', 'Bromine is removed.', 'HBr is eliminated.'], 'Addition removes unsaturation.'),
])


@p1b(R, 'ch10-st1')
def p1b_hbr_ratio(rng, slot):
    a = pick(rng, [x for x in ALK if not x[2]])
    reag = pick(rng, ['HBr', 'HCl'])
    maj, mnr = a[3][reag]
    pmaj = rng.randint(80, 97)
    m = rsf(rng.uniform(2.0, 8.0), 3)
    Ma = mr(a[1])
    Mp = _add_mr(a, reag)
    y = rng.randint(60, 90)
    tot = m / Ma * Mp * y / 100
    intro = (f'A student bubbled excess {reag} through a solution containing {q(m, "g")} of {a[0]} at room temperature. '
             f'{q(tot, "g")} of a liquid product mixture was obtained. Gas chromatography showed two peaks:\n\n'
             f'compound | peak area / %\n{maj} | {pmaj}\n{mnr} | {100 - pmaj}')
    return dict(intro=intro, parts=[
        ('Calculate the percentage yield of the product mixture.', f'{y} %', f'n(alkene) = {sf(m)}/{Ma:.2f} = {sf(m / Ma)} mol (M1); theoretical = {sf(m / Ma * Mp)} g (M1); yield = {y} % (A1).', 3),
        ('Explain the ratio of products in terms of the mechanism.', f'{maj} is major because it forms via the more stable {a[5]} carbocation; {mnr} forms via a less stable carbocation.', 'carbocation intermediate (1); more alkyl groups / positive inductive effect → more stable (1).', 2),
        (f'Calculate the mass of {maj} in the mixture.', q(tot * pmaj / 100, 'g'), f'{sf(tot)} × {pmaj}/100 = {q(tot * pmaj / 100, "g")} (A1), assuming peak area ∝ mass.', 1),
        ('State why the two products have identical molecular formulas.', 'They are structural (positional) isomers.', 'structural isomers (1).', 1)],
        extras=[('Suggest why the reaction is carried out in the dark.', f'To prevent radical substitution side reactions initiated by UV light.', 'radical reactions avoided (1).', 1)])


# ---- ch10-st2 electrophilic substitution of benzene ----
ARSUB = [
    ('nitration', 'concentrated nitric acid and concentrated sulfuric acid at below 55 °C', 'NO₂⁺', 'nitrobenzene', 'C6H5NO2', 'H₂O (with H₂SO₄ regenerated)',
     'HNO₃ + 2H₂SO₄ → NO₂⁺ + H₃O⁺ + 2HSO₄⁻'),
    ('bromination', 'bromine with an iron(III) bromide (or AlBr₃) halogen carrier', 'Br⁺', 'bromobenzene', 'C6H5Br', 'HBr', 'Br₂ + FeBr₃ → Br⁺ + FeBr₄⁻'),
    ('chlorination', 'chlorine with an aluminium chloride (or FeCl₃) halogen carrier', 'Cl⁺', 'chlorobenzene', 'C6H5Cl', 'HCl', 'Cl₂ + AlCl₃ → Cl⁺ + AlCl₄⁻'),
]

R.facts('ch10-st2', F(
    terms=[('electrophilic substitution', 'a reaction in which an electrophile replaces a hydrogen atom on an aromatic ring, so the delocalised π system is retained'),
           ('nitronium ion', 'the electrophile NO₂⁺, formed when concentrated sulfuric acid protonates nitric acid, which then loses water'),
           ('halogen carrier', 'a Lewis acid such as FeBr₃ or AlCl₃ that accepts a lone pair from a halogen molecule, polarising it to generate the X⁺ electrophile'),
           ('delocalised π system (benzene)', 'six p electrons spread over all six carbon atoms in a continuous ring above and below the plane of the molecule'),
           ('stabilisation (delocalisation) energy', 'the difference between the enthalpy change expected for a hypothetical Kekulé structure and the actual value, showing the extra stability of the delocalised ring'),
           ('arenium ion (Wheland intermediate)', 'the positively charged intermediate formed when an electrophile bonds to one ring carbon, temporarily breaking the delocalised system')],
    facts=[('What is the electrophile in the nitration of benzene?', 'NO₂⁺', ['NO₃⁻', 'HNO₃', 'NO₂'], 'Nitronium ion.'),
           ('What is the role of concentrated sulfuric acid in nitration?', 'It protonates nitric acid to generate NO₂⁺.', ['It is a dehydrating agent only.', 'It is the electrophile.', 'It is a reducing agent.'], 'Acts as the stronger acid.'),
           ('What are the C–C bond lengths in benzene?', 'all equal, between C–C and C=C', ['alternately long and short', 'all equal to C=C', 'all equal to C–C'], '140 pm.'),
           ('Why is iron(III) bromide used in the bromination of benzene?', 'It is a halogen carrier that generates the Br⁺ electrophile.', ['It decolourises bromine.', 'It reduces benzene.', 'It removes HBr.'], 'Lewis acid catalyst.'),
           ('What is the H–C–C bond angle in benzene?', '120°', ['109.5°', '90°', '180°'], 'Trigonal planar, sp².'),
           ('Which inorganic product forms in the bromination of benzene?', 'HBr', ['H₂', 'Br⁻ only', 'FeBr₂'], 'H⁺ lost from ring combines with Br⁻.')],
    why=[('Explain why benzene undergoes substitution rather than addition reactions.', 'Addition would permanently destroy the delocalised π system and its stabilisation energy; substitution restores the delocalised ring, so it is energetically favoured.'),
         ('Explain why benzene does not decolourise bromine water at room temperature, whereas cyclohexene does.', 'The delocalised electron density in benzene is spread over six atoms and is less concentrated than in a localised C=C bond, so it cannot polarise Br₂ enough without a halogen carrier.'),
         ('Explain the evidence from enthalpies of hydrogenation that benzene is more stable than a Kekulé structure.', 'Three C=C bonds would release about 3 × −120 = −360 kJ mol⁻¹, but benzene releases only about −208 kJ mol⁻¹, so it is about 150 kJ mol⁻¹ more stable than expected.'),
         ('Explain why the nitration of benzene is carried out below about 55 °C.', 'At higher temperatures further substitution occurs, giving dinitrobenzene and other by-products.'),
         ('Explain how the H⁺ released in bromination regenerates the catalyst.', 'H⁺ from the arenium ion reacts with FeBr₄⁻ to form HBr and FeBr₃, so the halogen carrier is regenerated.')],
    contrast=[('the reaction of bromine with cyclohexene', 'the reaction of bromine with benzene', 'Cyclohexene undergoes rapid electrophilic addition at room temperature without a catalyst; benzene needs a halogen carrier and undergoes electrophilic substitution, keeping its ring.'),
              ('the Kekulé structure of benzene', 'the delocalised model of benzene', 'The Kekulé structure has alternating single and double bonds of different lengths; the delocalised model has six equal bonds (140 pm) with π electrons spread round the ring.')],
    misc=[('Benzene has three double bonds and so reacts like an alkene.', 'Benzene has a delocalised π system; it does not behave as three isolated C=C bonds and prefers substitution.'),
          ('In nitration, nitric acid acts as the acid and sulfuric acid as the base.', 'Sulfuric acid is the stronger acid and protonates nitric acid, which acts as a base.')],
    apply=[('Write equations to show the formation of the electrophile in the nitration of benzene and the overall reaction.', 'HNO₃ + 2H₂SO₄ → NO₂⁺ + H₃O⁺ + 2HSO₄⁻; C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O', 3),
           ('Draw the mechanism for the bromination of benzene in the presence of FeBr₃.', 'Arrow from delocalised ring to Br⁺; arenium ion with horseshoe ring and + charge, H and Br on sp³ carbon; arrow from C–H bond into ring; bromobenzene + H⁺ (→ HBr, FeBr₃ regenerated).', 4)],
    evaluate=[("Kekulé's structure of benzene is an adequate model.", ['explains the formula C₆H₆ and the hexagonal ring', 'useful for counting electrons in mechanisms'], ['predicts unequal bond lengths – all are 140 pm', 'predicts addition with bromine water', 'predicts a hydrogenation enthalpy of −360, not −208 kJ mol⁻¹', 'predicts two isomers of 1,2-dibromobenzene'], 'It is inadequate: structural and thermochemical evidence supports the delocalised model.'),
              ('Using enthalpies of hydrogenation gives an accurate value for the stabilisation energy of benzene.', ['experimental data are reliable', 'simple comparison with cyclohexene'], ['assumes each C=C in a Kekulé structure behaves like cyclohexene', 'ignores strain and conjugation effects (cyclohexa-1,3-diene is −232 not −240)', 'values depend on phase/conditions'], 'It gives a reasonable estimate (about 150 kJ mol⁻¹) but not an exact value, as it depends on the reference compound.')],
    extended=[('Benzene reacts with a mixture of concentrated nitric and sulfuric acids. (a) Write an equation for the formation of the electrophile. (b) Draw the mechanism. (c) Explain why benzene undergoes substitution rather than addition. (d) Calculate the mass of nitrobenzene that could be obtained from 7.81 g of benzene at a 75 % yield.', '(a) HNO₃ + 2H₂SO₄ → NO₂⁺ + H₃O⁺ + 2HSO₄⁻. (b) arrow ring → NO₂⁺; arenium ion; C–H bond electrons return to ring; H⁺ lost. (c) substitution keeps the delocalised ring (stabilisation ≈150 kJ mol⁻¹). (d) n = 7.81/78.12 = 0.100 mol; 0.100 × 123.12 × 0.75 = 9.23 g.', 9, 'multi_step')],
))


@R.add('ch10-st2', 'C3', (1, 4), 'mcq')
def c3_arsub_pick(rng, slot):
    r = pick(rng, ARSUB)
    ask = rng.choice(['electrophile', 'product', 'by-product'])
    if ask == 'electrophile':
        right = r[2]
        wr = [x[2] for x in ARSUB if x != r] + {'nitration': ['NO₃⁻', 'HNO₃'], 'bromination': ['Br⁻', 'FeBr₄⁻'], 'chlorination': ['Cl⁻', 'AlCl₄⁻']}[r[0]]
        stem = f'Benzene is treated with {r[1]}. What is the electrophile?'
    elif ask == 'product':
        right = r[3]
        wr = {'nitration': ['1,3-dinitrobenzene (major)', 'phenylamine', 'cyclohexyl nitrate'], 'bromination': ['1,2-dibromocyclohexane', 'bromocyclohexane', '1,2,3,4,5,6-hexabromocyclohexane'],
              'chlorination': ['1,2-dichlorocyclohexane', 'chlorocyclohexane', 'chloromethylbenzene']}[r[0]]
        stem = f'What is the main organic product when benzene reacts with {r[1]}?'
    else:
        right = r[5].split(' (')[0]
        wr = [x for x in ['H₂O', 'HBr', 'HCl', 'H₂', 'NO₂', 'Br₂'] if x != right]
        rng.shuffle(wr)
        stem = f'In the {r[0]} of benzene using {r[1]}, which inorganic product forms (apart from regenerated catalyst)?'
    rng.shuffle(wr)
    return mcq(rng, stem, right, wr[:3], f'{r[6]}; electrophile {r[2]} substitutes one H to give {r[3]}.')


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def c3_stab_energy(rng, slot):
    h1 = rng.randint(-122, -118)
    hb = rng.randint(-212, -205)
    exp = 3 * h1
    st = hb - exp
    stem = (f'The enthalpy change of hydrogenation of cyclohexene is {sgn(h1, 3, "kJ mol⁻¹")} and that of benzene is {sgn(hb, 3, "kJ mol⁻¹")}. '
            'Calculate the stabilisation energy of benzene relative to a hypothetical cyclohexa-1,3,5-triene.')
    if slot.type == 'mcq' or slot.d <= 2:
        return nmcq(rng, stem, abs(st), [abs(hb - h1), abs(exp), abs(hb), abs(2 * h1 - hb)], 'kJ mol⁻¹', f'3 × ({h1}) = {exp}; {exp} − ({hb}) = {exp - hb} → {abs(st)} kJ mol⁻¹ more stable.', n=3)
    return num(stem, f'{abs(st)} kJ mol⁻¹', f'expected = 3 × ({sgn(h1, 3)}) = {sgn(exp, 3)} kJ mol⁻¹ (M1); stabilisation = {sgn(hb, 3)} − ({sgn(exp, 3)}) = {abs(st)} kJ mol⁻¹ (A1) (benzene is more stable).', 2)


@R.add('ch10-st2', 'C3', (2, 5), 'numerical')
def c3_arsub_mass(rng, slot):
    r = pick(rng, ARSUB)
    m = rsf(rng.uniform(2.0, 15.0), 3)
    Mb = mr('C6H6')
    Mp = mr(r[4])
    n = m / Mb
    if slot.d <= 3:
        y = rng.randint(55, 90)
        mp = n * Mp * y / 100
        stem = f'{q(m, "g")} of benzene undergoes {r[0]} with {r[1]}. Calculate the mass of {r[3]} obtained if the yield is {y} %.'
        return num(stem, q(mp, 'g'), f'n(C₆H₆) = {sf(m)}/{Mb:.2f} = {sf(n)} mol (M1); theoretical = {sf(n)} × {Mp:.2f} = {sf(n * Mp)} g (M1); × {y}/100 = {q(mp, "g")} (A1).', 3)
    act = n * Mp * rng.uniform(0.5, 0.9)
    pc = act / (n * Mp) * 100
    stem = f'In the {r[0]} of {q(m, "g")} of benzene, {q(act, "g")} of {r[3]} was isolated. Calculate the percentage yield and suggest one reason why it is below 100 %.'
    return num(stem, f'{pc:.1f} %; e.g. further substitution or loss during purification', f'theoretical = {sf(n)} × {Mp:.2f} = {sf(n * Mp)} g (M1); yield = {pc:.1f} % (A1); further substitution / incomplete reaction / loss on separation (1).', 3, 'multi_step')


@R.add('ch10-st2', 'C3', (1, 4), 'mcq')
def c3x_bond_length(rng, slot):
    cc = rng.choice([153, 154])
    cd = rng.choice([134, 135])
    ar = 140
    stem = (f'The C–C single bond length is {cc} pm and the C=C double bond length is {cd} pm. Which statement about the carbon–carbon bonds in benzene is consistent with the delocalised model?')
    right = f'All six are equal, at about {ar} pm.'
    wr = [f'Three are {cc} pm and three are {cd} pm.', f'All six are {cd} pm.', f'All six are {cc} pm.']
    return mcq(rng, stem, right, wr, 'Intermediate bond order of 1.5.')


R.mcqs('ch10-st2', 'C2', (1, 4), [
    ('Why does benzene need a catalyst to react with bromine whereas cyclohexene does not?', 'The delocalised electrons are less available, so a stronger electrophile (Br⁺) is required.', ['Benzene is saturated.', 'Benzene has no π electrons.', 'Bromine is a nucleophile.'], 'Lower local electron density.'),
    ('Why is the arenium intermediate higher in energy than benzene?', 'The delocalised ring is partly broken in the intermediate.', ['It has more bonds.', 'It is a radical.', 'It is neutral.'], 'Loss of aromatic stabilisation.'),
    ('Which evidence best supports the delocalised structure of benzene?', 'Its enthalpy of hydrogenation is less exothermic than 3 × that of cyclohexene.', ['Its formula is C₆H₆.', 'It burns with a smoky flame.', 'It is a liquid.'], 'About 150 kJ mol⁻¹ extra stability.'),
    ('Why does the arenium ion lose H⁺ rather than add a nucleophile?', 'Losing H⁺ restores the stable delocalised ring.', ['H⁺ is a nucleophile.', 'Addition is too fast.', 'Nucleophiles are absent.'], 'Re-aromatisation.'),
])


@p1b(R, 'ch10-st2')
def p1b_hydrogenation(rng, slot):
    h1 = rng.randint(-122, -118)
    rows = [('cyclohexene', h1)]
    if rng.random() < 0.7:
        rows.append(('cyclohexa-1,3-diene', rng.randint(-234, -230)))
    if rng.random() < 0.5:
        rows.append(('cyclohexa-1,4-diene', rng.randint(-242, -238)))
    hb = rng.randint(-210, -206)
    rows.append(('benzene', hb))
    order = rows[:]
    rng.shuffle(order)
    who = name(rng)
    intro = (f'{who} collected the enthalpy changes of hydrogenation of some cyclic hydrocarbons, each forming cyclohexane, from a database.\n\n'
             'compound | ΔH / kJ mol⁻¹\n' + '\n'.join(f'{a} | {sgn(b, 3)}' for a, b in order))
    parts = [('Predict the enthalpy of hydrogenation of a hypothetical Kekulé structure, cyclohexa-1,3,5-triene.', sgn(3 * h1, 3, 'kJ mol⁻¹'), f'3 × ({sgn(h1, 3)}) (A1).', 1),
             ('Calculate the stabilisation energy of benzene.', f'{hb - 3 * h1} kJ mol⁻¹', f'{sgn(hb, 3)} − ({sgn(3 * h1, 3)}) = {hb - 3 * h1} kJ mol⁻¹ (A1); benzene more stable (1).', 2)]
    pool = [('Write an equation for the hydrogenation of benzene.', 'C₆H₆ + 3H₂ → C₆H₁₂', 'correct formulas and balancing (1).', 1),
            ('State the catalyst and one condition used for hydrogenation.', 'nickel, about 150 °C (or Pt/Pd at room temperature)', 'catalyst (1); condition (1).', 2),
            ('State one piece of structural evidence for delocalisation in benzene.', 'All C–C bonds are the same length (140 pm) by X-ray diffraction.', 'equal bond lengths (1).', 1),
            ('Explain why benzene reacts with bromine by substitution rather than addition.', 'Substitution keeps the delocalised ring and its stabilisation energy; addition would destroy it.', 'delocalisation retained (1); energetically favoured (1).', 2),
            ('Calculate the volume of hydrogen at STP needed to hydrogenate 0.0500 mol of benzene (molar volume 22.7 dm³ mol⁻¹).', '3.41 dm³', '0.150 mol H₂ (M1) × 22.7 = 3.41 dm³ (A1).', 2)]
    names = [a for a, _ in rows]
    if 'cyclohexa-1,3-diene' in names:
        hd = dict(rows)['cyclohexa-1,3-diene']
        pool.append(('Compare the value for cyclohexa-1,3-diene with 2 × the value for cyclohexene and suggest a reason for the difference.', f'{sgn(hd, 3)} vs {sgn(2 * h1, 3)}: slightly less exothermic because the conjugated double bonds have a small amount of delocalisation.', 'comparison (1); conjugation/partial delocalisation (1).', 2))
    if 'cyclohexa-1,4-diene' in names:
        h4 = dict(rows)['cyclohexa-1,4-diene']
        pool.append(('Explain why the value for cyclohexa-1,4-diene is close to 2 × the value for cyclohexene.', f'{sgn(h4, 3)} ≈ {sgn(2 * h1, 3)}: its two C=C bonds are isolated (not conjugated), so each behaves like the bond in cyclohexene.', 'isolated double bonds (1); no delocalisation (1).', 2))
    rng.shuffle(pool)
    return dict(intro=intro, parts=parts + pool[:2], extras=pool[2:])


# ---- ch10-st3 reaction pathways ----
# conversion: (from class, to class, reagents/conditions, reaction type)
CONV = [
    ('alkane', 'halogenoalkane', 'Cl₂ or Br₂ with UV light', 'free-radical substitution'),
    ('alkene', 'halogenoalkane', 'HBr (or HCl) at room temperature', 'electrophilic addition'),
    ('alkene', 'dihalogenoalkane', 'Br₂ at room temperature', 'electrophilic addition'),
    ('alkene', 'alcohol', 'steam with H₃PO₄ catalyst, about 300 °C and 6 MPa', 'electrophilic addition (hydration)'),
    ('alkene', 'alkane', 'H₂ with a Ni catalyst, about 150 °C', 'addition (hydrogenation, reduction)'),
    ('halogenoalkane', 'alcohol', 'warm aqueous NaOH', 'nucleophilic substitution'),
    ('halogenoalkane', 'amine', 'excess ammonia in ethanol, heated under pressure', 'nucleophilic substitution'),
    ('primary alcohol', 'aldehyde', 'acidified K₂Cr₂O₇, distil the product as it forms', 'oxidation'),
    ('primary alcohol', 'carboxylic acid', 'excess acidified K₂Cr₂O₇, heat under reflux', 'oxidation'),
    ('secondary alcohol', 'ketone', 'acidified K₂Cr₂O₇, heat under reflux', 'oxidation'),
    ('aldehyde', 'primary alcohol', 'NaBH₄ in water or ethanol', 'reduction'),
    ('ketone', 'secondary alcohol', 'NaBH₄ in water or ethanol', 'reduction'),
    ('carboxylic acid', 'primary alcohol', 'LiAlH₄ in dry ether, then dilute acid', 'reduction'),
    ('carboxylic acid', 'ester', 'an alcohol with a concentrated H₂SO₄ catalyst, heat', 'condensation (esterification)'),
    ('benzene', 'nitrobenzene', 'concentrated HNO₃ and H₂SO₄ below 55 °C', 'electrophilic substitution'),
    ('benzene', 'bromobenzene', 'Br₂ with FeBr₃', 'electrophilic substitution'),
    ('nitrobenzene', 'phenylamine', 'tin and concentrated HCl under reflux, then NaOH', 'reduction'),
]
# routes: list of (compound, (reagents, type) to reach next)
ROUTES = [
    ['ethane', 'chloroethane', 'ethanol', 'ethanoic acid'],
    ['ethene', 'bromoethane', 'ethanol', 'ethanal'],
    ['ethene', 'ethanol', 'ethanoic acid', 'ethyl ethanoate'],
    ['propene', '2-bromopropane', 'propan-2-ol', 'propanone'],
    ['propene', 'propan-2-ol', 'propanone', 'propan-2-ol'],
    ['propane', '1-bromopropane', 'propan-1-ol', 'propanal'],
    ['propane', '1-chloropropane', 'propan-1-ol', 'propanoic acid'],
    ['but-2-ene', '2-bromobutane', 'butan-2-ol', 'butanone'],
    ['but-1-ene', 'butane', '1-chlorobutane', 'butan-1-ol'],
    ['ethanoic acid', 'ethanol', 'ethanal'],
    ['benzene', 'nitrobenzene', 'phenylamine'],
    ['bromoethane', 'ethanol', 'ethanoic acid', 'ethyl ethanoate'],
    ['propanoic acid', 'propan-1-ol', 'propanal'],
    ['ethene', 'ethane', 'chloroethane', 'ethylamine'],
]
CLS = {'ethane': 'alkane', 'propane': 'alkane', 'butane': 'alkane', 'ethene': 'alkene', 'propene': 'alkene', 'but-1-ene': 'alkene', 'but-2-ene': 'alkene',
       'chloroethane': 'halogenoalkane', 'bromoethane': 'halogenoalkane', '2-bromopropane': 'halogenoalkane', '1-bromopropane': 'halogenoalkane',
       '1-chloropropane': 'halogenoalkane', '2-bromobutane': 'halogenoalkane', '1-chlorobutane': 'halogenoalkane',
       'ethanol': 'primary alcohol', 'propan-1-ol': 'primary alcohol', 'butan-1-ol': 'primary alcohol', 'propan-2-ol': 'secondary alcohol', 'butan-2-ol': 'secondary alcohol',
       'ethanal': 'aldehyde', 'propanal': 'aldehyde', 'propanone': 'ketone', 'butanone': 'ketone',
       'ethanoic acid': 'carboxylic acid', 'propanoic acid': 'carboxylic acid', 'ethyl ethanoate': 'ester', 'ethylamine': 'amine',
       'benzene': 'benzene', 'nitrobenzene': 'nitrobenzene', 'phenylamine': 'phenylamine'}


def _conv(a, b):
    ca, cb = CLS[a], CLS[b]
    if ca == 'alkene' and cb == 'alcohol' or ca == 'alkene' and cb.endswith('alcohol'):
        cb = 'alcohol'
    if ca == 'halogenoalkane' and cb.endswith('alcohol'):
        cb = 'alcohol'
    for r in CONV:
        if r[0] == ca and r[1] == cb:
            rg = r[2]
            if a == 'ethanol' and b == 'ethyl ethanoate':
                rg = 'ethanoic acid with a concentrated H₂SO₄ catalyst, heat'
            if ca == 'carboxylic acid' and cb == 'ester':
                rg = 'ethanol with a concentrated H₂SO₄ catalyst, heat'
            return rg, r[3]
    raise KeyError((a, b))


for _r in ROUTES:
    for _a, _b in zip(_r, _r[1:]):
        _conv(_a, _b)


R.facts('ch10-st3', F(
    terms=[('retrosynthesis', 'planning a synthesis by working backwards from the target molecule to simpler, available starting materials'),
           ('reaction pathway', 'a sequence of reactions, each with stated reagents and conditions, that converts a starting material into a target compound'),
           ('heating under reflux', 'heating a reaction mixture with a vertical condenser so that volatile substances condense and return to the flask, allowing complete reaction'),
           ('overall yield', 'the product of the fractional yields of each step in a multi-step synthesis, expressed as a percentage'),
           ('reducing agent (organic)', 'a reagent such as NaBH₄ or LiAlH₄ that supplies hydride (H⁻) to reduce carbonyl compounds or carboxylic acids to alcohols'),
           ('functional group interconversion', 'the conversion of one functional group into another by a single reaction step')],
    facts=[('Which reagent reduces a carboxylic acid to a primary alcohol?', 'LiAlH₄', ['NaBH₄', 'acidified K₂Cr₂O₇', 'H₂SO₄'], 'NaBH₄ is too weak for acids.'),
           ('Which conditions convert ethanol into ethanal rather than ethanoic acid?', 'acidified K₂Cr₂O₇ with distillation', ['acidified K₂Cr₂O₇ under reflux', 'NaBH₄', 'concentrated H₂SO₄ at 170 °C'], 'Remove aldehyde before further oxidation.'),
           ('Which conversion requires UV light?', 'alkane → halogenoalkane', ['alkene → alcohol', 'halogenoalkane → alcohol', 'alcohol → ketone'], 'Radical substitution.'),
           ('What type of reaction converts a halogenoalkane into an alcohol?', 'nucleophilic substitution', ['electrophilic addition', 'oxidation', 'free-radical substitution'], 'OH⁻ replaces X.'),
           ('Which reagent converts nitrobenzene into phenylamine?', 'tin and concentrated HCl', ['NaBH₄', 'HNO₃', 'Br₂/FeBr₃'], 'Reduction, then NaOH.'),
           ('Which reaction type converts propanone into propan-2-ol?', 'reduction', ['oxidation', 'hydration', 'substitution'], 'Hydride adds to C=O.')],
    why=[('Explain why the overall yield of a multi-step synthesis is often low.', 'The yield of each step is below 100 %, and the overall yield is the product of all the step yields, so losses multiply with each additional step.'),
         ('Explain why a two-step route from an alkane to an alcohol via a halogenoalkane gives an impure product.', 'Radical substitution of the alkane gives a mixture of mono- and polysubstituted, and positional isomers of, halogenoalkanes, so the alcohol made from them is also a mixture.'),
         ('Explain why ketones cannot be oxidised by acidified dichromate(VI).', 'Oxidation would require breaking a strong C–C bond because the carbonyl carbon has no hydrogen attached.'),
         ('Explain why chemists prefer short synthetic routes.', 'Fewer steps give a higher overall yield, use less reagent and energy, produce less waste and save time, improving atom economy and green credentials.')],
    contrast=[('NaBH₄', 'LiAlH₄', 'NaBH₄ is a mild reducing agent that reduces aldehydes and ketones in water or ethanol; LiAlH₄ is stronger, also reduces carboxylic acids, and must be used in dry ether.'),
              ('distillation', 'heating under reflux', 'Distillation removes a volatile product as it forms (e.g. an aldehyde); reflux keeps all substances in the flask so reaction goes to completion (e.g. carboxylic acid).')],
    misc=[('NaBH₄ reduces ethanoic acid to ethanol.', 'NaBH₄ cannot reduce carboxylic acids; LiAlH₄ is needed.'),
          ('Oxidising a secondary alcohol under reflux gives a carboxylic acid.', 'A secondary alcohol is oxidised to a ketone, which is not oxidised further.'),
          ('The overall yield of a three-step synthesis is the average of the step yields.', 'The overall yield is the product of the step yields.')],
    apply=[('Outline a two-step synthesis of propanone from propene, giving reagents and conditions for each step.', 'Step 1: steam, H₃PO₄ catalyst, 300 °C, 6 MPa → propan-2-ol (major); Step 2: acidified K₂Cr₂O₇, reflux → propanone.', 4),
           ('Outline a two-step synthesis of phenylamine from benzene.', 'Step 1: conc. HNO₃/H₂SO₄ below 55 °C → nitrobenzene; Step 2: Sn/conc. HCl, reflux, then NaOH → phenylamine.', 4)],
    evaluate=[('Retrosynthesis is the most effective way to plan an organic synthesis.', ['works backwards from the target, revealing simple starting materials', 'allows comparison of several routes'], ['the reverse reactions may not be practical', 'yields, cost, safety and selectivity must still be checked'], 'Retrosynthesis is a powerful planning tool, but each proposed step must be evaluated practically.'),
              ('Making ethanol from ethene is better than making it from bromoethane.', ['one step, near 100 % atom economy', 'continuous industrial process'], ['high temperature and pressure needed', 'ethene from crude oil (non-renewable)', 'low conversion per pass'], 'Hydration of ethene is preferred industrially for its atom economy, though fermentation offers a renewable alternative.')],
    extended=[('Ethyl ethanoate can be made from ethene in three steps. (a) Outline the route with reagents and conditions. (b) State the type of each reaction. (c) If the step yields are 90 %, 80 % and 65 %, calculate the overall yield. (d) Suggest one way the synthesis could be made greener.', '(a) ethene + steam/H₃PO₄ → ethanol; some ethanol + excess K₂Cr₂O₇/H⁺, reflux → ethanoic acid; ethanol + ethanoic acid, conc. H₂SO₄, heat → ethyl ethanoate. (b) electrophilic addition; oxidation; condensation (esterification). (c) 0.90 × 0.80 × 0.65 = 46.8 %. (d) bio-ethanol from fermentation / recycle unreacted materials / use less hazardous oxidants.', 9, 'multi_step')],
))


@R.add('ch10-st3', 'C3', (1, 4), 'mcq')
def c3_conv_reagent(rng, slot):
    r = pick(rng, CONV)
    # reagents that would ALSO achieve the conversion are never offered as distractors
    also = {('alkene', 'halogenoalkane'): {'Br₂ at room temperature', 'Cl₂ or Br₂ with UV light'},
            ('aldehyde', 'primary alcohol'): {'LiAlH₄ in dry ether, then dilute acid'},
            ('ketone', 'secondary alcohol'): {'LiAlH₄ in dry ether, then dilute acid'},
            ('secondary alcohol', 'ketone'): {'acidified K₂Cr₂O₇, distil the product as it forms', 'excess acidified K₂Cr₂O₇, heat under reflux'},
            ('alkane', 'halogenoalkane'): set()}.get((r[0], r[1]), set())
    same = [x[2] for x in CONV if x[0] == r[0] and x[2] != r[2] and x[2] not in also]
    rest = [x[2] for x in CONV if x[2] != r[2] and x[2] not in also and x[2] not in same]
    rng.shuffle(rest)
    wr = list(dict.fromkeys(same + rest))
    art = lambda w: ('an ' if w[0] in 'aeiou' else 'a ') + w
    stem = (f'Which reagents and conditions convert {art(r[0])} into {art(r[1])}?' if r[0] not in ('benzene', 'nitrobenzene')
            else f'Which reagents and conditions convert {r[0]} into {r[1]}?')
    return mcq(rng, stem, r[2], wr[:3], f'{r[3]}.')


@R.add('ch10-st3', 'C3', (1, 4), 'mcq')
def c3_route_type(rng, slot):
    rt = pick(rng, ROUTES)
    i = rng.randrange(len(rt) - 1)
    a, b = rt[i], rt[i + 1]
    rg, ty = _conv(a, b)
    types = ['free-radical substitution', 'electrophilic addition', 'nucleophilic substitution', 'oxidation', 'reduction', 'electrophilic substitution', 'condensation (esterification)']
    base = ty.split(' (')[0] if not ty.startswith('condensation') else ty
    if ty.startswith('addition (hydro'):
        base = 'reduction'
    wr = [t for t in types if t != base and not ty.startswith(t)]
    rng.shuffle(wr)
    stem = f'In the synthesis route {" → ".join(rt)}, what type of reaction converts {a} into {b}?'
    return mcq(rng, stem, base, wr[:3], f'{a} → {b}: {rg}.')


@R.add('ch10-st3', 'C3', (1, 5), 'short')
def c3_route_outline(rng, slot):
    rt = pick(rng, ROUTES)
    k = 2 if slot.d <= 3 or len(rt) == 3 else 3
    i = rng.randrange(len(rt) - k)
    seg = rt[i:i + k + 1]
    steps = [_conv(x, y) for x, y in zip(seg, seg[1:])]
    stem = f'Outline a {k}-step synthesis of {seg[-1]} from {seg[0]}. Give the intermediate(s), the reagents and conditions, and the type of each reaction.'
    ans = '; '.join(f'step {j + 1}: {seg[j]} → {seg[j + 1]} using {rg} ({ty})' for j, (rg, ty) in enumerate(steps))
    return dict(stem=stem, answer=ans, markingKey=' '.join(f'Step {j + 1}: intermediate/product {seg[j + 1]} (1); {rg} (1).' for j, (rg, ty) in enumerate(steps)) + ' Reaction types (1).',
                type='short' if k == 2 else 'multi_step', marks=2 * k + 1)


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def c3_overall_yield(rng, slot):
    k = 2 if slot.d <= 2 else rng.choice([3, 4]) if slot.d <= 3 else rng.choice([2, 3])
    ys = [rng.randint(55, 95) for _ in range(k)]
    tot = 1.0
    for y in ys:
        tot *= y / 100
    ylist = ', '.join(f'{y} %' for y in ys)
    if slot.d <= 3:
        stem = f'A {k}-step synthesis has step yields of {ylist}. Calculate the overall percentage yield.'
        if slot.type == 'mcq':
            return nmcq(rng, stem, tot * 100, [sum(ys) / k, min(ys), 100 - sum(100 - y for y in ys)], '%', 'Multiply the fractional yields.')
        return num(stem, f'{sf(tot * 100)} %', f'{" × ".join(f"{y / 100:.2f}" for y in ys)} (M1) = {sf(tot * 100)} % (A1).', 2)
    rt = pick(rng, [r for r in ROUTES if len(r) >= k + 1])
    seg = rt[:k + 1]
    if seg[0] not in _MF or seg[-1] not in _MF:
        return None
    m0 = rsf(rng.uniform(5.0, 20.0), 3)
    M0, M1 = mr(_MF[seg[0]]), mr(_MF[seg[-1]])
    mf = m0 / M0 * M1 * tot
    stem = f'{q(m0, "g")} of {seg[0]} is converted into {seg[-1]} by the route {" → ".join(seg)}, with step yields of {ylist} (1 : 1 stoichiometry at each step). Calculate the mass of {seg[-1]} obtained.'
    return num(stem, q(mf, 'g'), f'n = {sf(m0)}/{M0:.2f} = {sf(m0 / M0)} mol (M1); overall yield = {sf(tot * 100)} % (M1); m = {sf(m0 / M0)} × {sf(tot)} × {M1:.2f} = {q(mf, "g")} (A1).', 3)


_MF = {'ethane': 'C2H6', 'propane': 'C3H8', 'ethene': 'C2H4', 'propene': 'C3H6', 'but-1-ene': 'C4H8', 'but-2-ene': 'C4H8', 'bromoethane': 'C2H5Br',
       'ethanoic acid': 'C2H4O2', 'ethanal': 'C2H4O', 'ethyl ethanoate': 'C4H8O2', 'propanone': 'C3H6O', 'propan-2-ol': 'C3H8O', 'propanal': 'C3H6O',
       'propanoic acid': 'C3H6O2', 'butanone': 'C4H8O', 'butan-1-ol': 'C4H10O', 'benzene': 'C6H6', 'phenylamine': 'C6H7N', 'ethylamine': 'C2H7N', 'ethanol': 'C2H6O'}


@R.add('ch10-st3', 'C3', (2, 4), 'mcq')
def c3x_route_order(rng, slot):
    rt = pick(rng, [r for r in ROUTES if len(r) >= 3])
    seg = rt[:3]
    (r1, t1), (r2, t2) = _conv(seg[0], seg[1]), _conv(seg[1], seg[2])
    right = f'1: {r1}; 2: {r2}'
    wr = [f'1: {r2}; 2: {r1}']
    others = [x[2] for x in CONV if x[2] not in (r1, r2)]
    rng.shuffle(others)
    wr += [f'1: {r1}; 2: {others[0]}', f'1: {others[1]}; 2: {r2}']
    stem = f'{cap(seg[0])} is converted into {seg[2]} via {seg[1]}. Which reagents are used, in order?'
    return mcq(rng, stem, right, wr, f'{seg[0]} → {seg[1]} ({t1}); {seg[1]} → {seg[2]} ({t2}).')


R.mcqs('ch10-st3', 'C2', (1, 4), [
    ('Why is NaBH₄ chosen rather than LiAlH₄ to reduce propanone in the laboratory?', 'NaBH₄ is safer and can be used in water or ethanol.', ['NaBH₄ is a stronger reducing agent.', 'LiAlH₄ cannot reduce ketones.', 'NaBH₄ is an oxidising agent.'], 'LiAlH₄ reacts violently with water.'),
    ('Why is an aldehyde distilled off as it forms during the oxidation of a primary alcohol?', 'To prevent its further oxidation to a carboxylic acid.', ['Aldehydes are solids.', 'To speed up the reaction.', 'To remove water.'], 'Aldehyde has the lowest b.p.'),
    ('Why is making ethylamine from bromoethane and ammonia done with excess ammonia?', 'To reduce further substitution forming secondary and tertiary amines.', ['Ammonia is a catalyst.', 'To lower the temperature.', 'Bromoethane is a gas.'], 'Product amine is also a nucleophile.'),
    ('Why does the radical chlorination step reduce the purity of a synthesis?', 'It gives a mixture of substitution products.', ['It needs a catalyst.', 'It is endothermic.', 'It is too slow.'], 'Multiple substitution.'),
])

R.mcqs('ch10-st1', 'C1', (1, 3), [
    ('Which reagent and condition convert ethene to ethanol industrially?', 'steam with H₃PO₄ catalyst', ['aqueous NaOH', 'acidified K₂Cr₂O₇', 'H₂ with Ni'], 'Hydration.'),
    ('Which catalyst is used for the hydrogenation of alkenes?', 'nickel', ['iron', 'vanadium(V) oxide', 'platinum(IV) oxide only'], 'About 150 °C.'),
])
R.mcqs('ch10-st2', 'C1', (1, 3), [
    ('What is the shape of the benzene molecule?', 'planar hexagonal', ['chair-shaped', 'tetrahedral', 'linear'], 'All sp² carbons.'),
    ('What is the hybridisation of carbon in benzene?', 'sp²', ['sp³', 'sp', 'sp³d'], 'Three σ bonds, one p orbital.'),
])
R.mcqs('ch10-st3', 'C1', (1, 3), [
    ('Which type of reaction converts an alcohol and a carboxylic acid into an ester?', 'condensation', ['addition', 'reduction', 'hydrolysis'], 'Water eliminated.'),
    ('Which reagent oxidises butan-2-ol to butanone?', 'acidified potassium dichromate(VI)', ['NaBH₄', 'LiAlH₄', 'aqueous NaOH'], 'Orange → green.'),
])


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step')
def c4_kekule_eval(rng, slot):
    h1 = rng.randint(-122, -118)
    hd = rng.randint(-234, -230)
    hb = rng.randint(-210, -206)
    st = hb - 3 * h1
    st2 = hb - (hd + h1)
    stem = (f'ΔH(hydrogenation) values: cyclohexene {sgn(h1, 3, "kJ mol⁻¹")}, cyclohexa-1,3-diene {sgn(hd, 3, "kJ mol⁻¹")}, benzene {sgn(hb, 3, "kJ mol⁻¹")}. '
            '(a) Calculate the stabilisation energy of benzene using cyclohexene as the reference. (b) Estimate it again by treating benzene as cyclohexa-1,3-diene plus one further isolated C=C bond. '
            '(c) Evaluate which estimate is more reliable and what both show about the Kekulé model.')
    ans = (f'(a) 3 × ({h1}) = {3 * h1}; {hb} − ({3 * h1}) = {st} → {abs(st)} kJ mol⁻¹. (b) ({hd}) + ({h1}) = {hd + h1}; {hb} − ({hd + h1}) = {st2} → {abs(st2)} kJ mol⁻¹. '
           '(c) The second estimate allows for the small conjugation energy of adjacent C=C bonds, so it is closer to a true “localised triene”; both show that benzene is substantially more stable than any Kekulé structure, so the delocalised model is supported.')
    return num(stem, ans, f'(a) {abs(st)} (2). (b) {abs(st2)} (2). (c) judgement on the reference compound (1); conclusion: Kekulé model inadequate / delocalisation (1).', 6, 'multi_step', gap='G7')


# =============================================================================================
# ch11 Internal Assessment: scientific investigation
# =============================================================================================
# (topic, research question, IV (with range), DV (how measured), [(controlled variable, how controlled)], technique)
INV = [
    ('the rate of reaction of magnesium with hydrochloric acid',
     'How does the concentration of hydrochloric acid (0.20, 0.40, 0.60, 0.80 and 1.00 mol dm⁻³) affect the initial rate of reaction with magnesium ribbon at 25 °C, measured by the volume of hydrogen collected in a gas syringe in the first 30 s?',
     'concentration of hydrochloric acid', 'volume of hydrogen collected in the first 30 s',
     [('mass (length) of magnesium ribbon', 'cut 3.0 cm lengths from the same roll'), ('temperature', 'use a water bath at 25.0 °C'),
      ('volume of acid', 'measure 50.0 cm³ with a burette'), ('surface condition of magnesium', 'clean each strip with emery paper')], 'gas collection'),
    ('the reaction between sodium thiosulfate and hydrochloric acid',
     'How does temperature (20, 30, 40, 50 and 60 °C) affect the rate of reaction between 0.10 mol dm⁻³ sodium thiosulfate and 1.0 mol dm⁻³ hydrochloric acid, measured by the time for a cross to be obscured?',
     'temperature of the reaction mixture', 'time for the cross to disappear (rate ∝ 1/t)',
     [('concentration of thiosulfate', 'use the same stock solution'), ('volume of reactants', 'use the same pipetted volumes'),
      ('depth of solution / observer', 'same flask and same observer'), ('concentration of acid', 'same stock solution')], 'visual timing'),
    ('the enthalpy of combustion of alcohols',
     'How does the number of carbon atoms in a primary alcohol (methanol to pentan-1-ol) affect its enthalpy of combustion, determined by spirit-burner calorimetry heating 100.0 g of water?',
     'number of carbon atoms in the alcohol chain', 'temperature rise of the water (used to calculate ΔHc)',
     [('mass of water', 'measure 100.0 cm³ with a measuring cylinder'), ('distance between flame and calorimeter', 'fix the clamp height at 3.0 cm'),
      ('wick length', 'trim each wick to the same length'), ('draughts', 'use a draught shield')], 'calorimetry'),
    ('the decomposition of hydrogen peroxide',
     'How does the mass of manganese(IV) oxide catalyst (0.10–0.50 g) affect the initial rate of decomposition of 25.0 cm³ of 1.0 mol dm⁻³ hydrogen peroxide at 25 °C, measured by the rate of mass loss on a balance?',
     'mass of manganese(IV) oxide', 'rate of mass loss of the flask (oxygen released)',
     [('particle size of MnO₂', 'use powder from the same batch'), ('volume and concentration of H₂O₂', 'use the same stock and a pipette'),
      ('temperature', 'thermostatic water bath'), ('swirling', 'use a magnetic stirrer at constant speed')], 'mass loss'),
    ('the vitamin C content of fruit juice',
     'How does the storage temperature (5, 15, 25, 35 °C) of fresh orange juice for 48 hours affect its ascorbic acid concentration, determined by titration with 0.0010 mol dm⁻³ DCPIP?',
     'storage temperature of the juice', 'volume of DCPIP needed (ascorbic acid concentration)',
     [('storage time', 'store all samples for exactly 48 h'), ('juice source', 'use juice from one batch of oranges'),
      ('volume of juice titrated', 'use a 10.00 cm³ pipette'), ('exposure to light', 'store in sealed, dark containers')], 'titration'),
    ('the solubility of potassium nitrate',
     'How does temperature (30–70 °C) affect the solubility of potassium nitrate in water, measured by the temperature at which crystals first appear on cooling solutions of known concentration?',
     'mass of KNO₃ per 100 g of water (solution concentration)', 'temperature at which crystals first appear',
     [('mass of water', 'weigh 10.00 g of water'), ('rate of cooling', 'cool in air at room temperature with stirring'),
      ('purity of KNO₃', 'use the same analytical-grade batch')], 'crystallisation'),
    ('the colour of copper(II) solutions',
     'How does the concentration of copper(II) sulfate (0.010–0.100 mol dm⁻³) affect the absorbance at 635 nm measured with a colorimeter?',
     'concentration of copper(II) sulfate', 'absorbance at 635 nm',
     [('wavelength/filter', 'use the same 635 nm setting'), ('path length', 'use identical 1.00 cm cuvettes'),
      ('temperature', 'allow solutions to reach room temperature'), ('calibration', 'zero with distilled water before each reading')], 'colorimetry'),
    ('the voltage of a Daniell cell',
     'How does the concentration of copper(II) ions (0.0010–1.0 mol dm⁻³) affect the cell potential of a Zn|Zn²⁺||Cu²⁺|Cu cell at 25 °C, measured with a high-resistance voltmeter?',
     'concentration of copper(II) ions', 'cell potential',
     [('[Zn²⁺]', 'keep at 1.0 mol dm⁻³'), ('temperature', 'water bath at 25 °C'), ('condition of the salt bridge', 'use fresh KNO₃-soaked filter paper for each run'),
      ('electrode surface area', 'clean electrodes of the same size')], 'electrochemistry'),
    ('the pH of ethanoic acid solutions',
     'How does the concentration of ethanoic acid (0.0010–0.10 mol dm⁻³) affect its pH and calculated degree of dissociation at 25 °C, measured with a calibrated pH probe?',
     'concentration of ethanoic acid', 'pH of the solution',
     [('temperature', 'water bath at 25.0 °C'), ('probe calibration', 'calibrate with pH 4 and 7 buffers before use'),
      ('purity of water used for dilution', 'use deionised water')], 'pH measurement'),
    ('the rate of hydrolysis of halogenoalkanes',
     'How does the identity of the halogen (Cl, Br, I) in 1-halobutanes affect the time taken for a precipitate to form with ethanolic silver nitrate at 50 °C?',
     'identity of the halogen in the 1-halobutane', 'time for a precipitate to appear',
     [('temperature', 'water bath at 50 °C'), ('volume of halogenoalkane', 'add 5 drops from the same pipette'),
      ('concentration and volume of AgNO₃', 'same stock, 1.0 cm³'), ('carbon chain', 'use only 1-halobutanes')], 'precipitation timing'),
]

R.facts('ch11-st1', F(
    terms=[('research question', 'a focused, answerable question that states the independent variable (with its range), the dependent variable and how it will be measured, and the system studied'),
           ('independent variable', 'the variable that the investigator deliberately changes in a controlled way'),
           ('dependent variable', 'the variable that is measured in response to changes in the independent variable'),
           ('controlled variable', 'a variable that is kept constant because it could otherwise affect the dependent variable'),
           ('background information (IA)', 'relevant chemistry theory and context that explains why the research question is worth investigating and supports a hypothesis'),
           ('hypothesis', 'a testable prediction of the relationship between the independent and dependent variables, justified with scientific reasoning')],
    facts=[('Which feature makes a research question focused?', 'It names the IV with its range and how the DV is measured.', ['It is as broad as possible.', 'It contains a hypothesis.', 'It avoids numbers.'], 'Specific and measurable.'),
           ('What is a controlled variable?', 'a variable kept constant during the investigation', ['the variable measured', 'the variable changed', 'a variable that cannot be measured'], 'Fair test.'),
           ('How many values of a continuous independent variable are usually recommended for a reliable trend?', 'at least five', ['one', 'two', 'three at most'], 'Enough points for a graph.'),
           ('Which IA criterion assesses the research question and methodology?', 'Research design', ['Data analysis', 'Conclusion', 'Evaluation'], 'IB 2025 criteria.'),
           ('What are the four IA assessment criteria (2025)?', 'research design, data analysis, conclusion, evaluation', ['personal engagement, exploration, analysis, evaluation', 'planning, data collection, processing, evaluation', 'design, communication, analysis, reflection'], 'Each worth 6 marks.'),
           ('What is the maximum mark for the IA in the 2025 chemistry course?', '24', ['20', '30', '36'], '4 criteria × 6.')],
    why=[('Explain why the range of the independent variable should be stated in the research question.', 'It shows the investigation is planned and focused, defines the scope of the conclusion and ensures enough data points to establish a trend.'),
         ('Explain why controlled variables must be identified and controlled.', 'If they change, they could alter the dependent variable, so any change could not be attributed to the independent variable alone; the conclusion would be invalid.'),
         ('Explain why a preliminary trial is useful when designing an investigation.', 'It tests the method and apparatus, shows whether the chosen range and measurement times are suitable, and reveals problems to fix before data are collected.'),
         ('Explain why safety, ethical and environmental considerations are included in the research design.', 'They show the method is appropriate and responsible: hazards are assessed and minimised, waste is disposed of correctly and no unethical procedures are used.')],
    contrast=[('the independent variable', 'the dependent variable', 'The independent variable is deliberately changed by the investigator; the dependent variable is measured to see how it responds.'),
              ('a controlled variable', 'an uncontrolled (confounding) variable', 'A controlled variable is kept constant by design; an uncontrolled variable changes during the experiment and may affect the results.')],
    misc=[('The dependent variable is the one kept constant.', 'Controlled variables are kept constant; the dependent variable is measured.'),
          ('A broad research question is better because it allows more conclusions.', 'A focused question allows a valid, specific conclusion within the time available.')],
    apply=[('Rewrite the question "Does temperature affect reaction rate?" as a focused IA research question.', 'e.g. How does temperature (20–60 °C, five values) affect the rate of reaction of 0.10 mol dm⁻³ sodium thiosulfate with 1.0 mol dm⁻³ HCl, measured by the time for a cross to disappear?', 3),
           ('For an investigation of the effect of concentration of HCl on the rate of reaction with CaCO₃ chips, identify the IV, the DV and two controlled variables.', 'IV: [HCl]; DV: rate of mass loss or volume of CO₂ per unit time; controls: mass and size of chips, temperature, volume of acid.', 3)],
    evaluate=[('A simple, safe investigation can score as highly as a complex one in the IA.', ['criteria reward a focused question, sound method and thorough analysis, not complexity', 'simple methods often yield more precise data'], ['very simple investigations may lack depth for analysis', 'limited scope can restrict evaluation'], 'Yes – the IA rewards quality of design and analysis, so a well-executed simple investigation can score full marks.'),
              ('Database or simulation-based investigations are as valid as hands-on experiments for the IA.', ['allowed by the 2025 guide', 'large data sets enable sophisticated analysis'], ['less control over how data were collected', 'uncertainties may be unknown'], 'They are valid if the research question is focused and the data quality is evaluated critically.')],
    extended=[('A student proposes: "Investigating how temperature affects the rate of the reaction of magnesium with acid." (a) Rewrite this as a focused research question. (b) Identify the IV, DV and three controlled variables, stating how each is controlled. (c) Suggest a hypothesis with scientific justification. (d) State one safety consideration.', '(a) e.g. How does temperature (20–60 °C) affect the initial rate of reaction of 3.0 cm Mg ribbon with 50.0 cm³ of 1.0 mol dm⁻³ HCl, measured by H₂ volume in 30 s? (b) IV temperature; DV volume of H₂ in 30 s; controls: Mg length/mass (same roll), acid concentration and volume, surface cleanliness. (c) rate increases with temperature because more particles have E ≥ Ea (Maxwell–Boltzmann). (d) HCl is an irritant / H₂ flammable – goggles, no flames.', 9, 'multi_step')],
))


@R.add('ch11-st1', 'C3', (1, 4), 'mcq')
def c3_inv_variable(rng, slot):
    inv = pick(rng, INV)
    ask = rng.choice(['independent', 'dependent', 'controlled'])
    ctrl = [c for c, _ in inv[4]]
    if ask == 'independent':
        right, wr = inv[2], [inv[3]] + rng.sample(ctrl, 2)
    elif ask == 'dependent':
        right, wr = inv[3], [inv[2]] + rng.sample(ctrl, 2)
    else:
        right = pick(rng, ctrl)
        wr = [inv[2], inv[3], pick(rng, ['the colour of the laboratory', 'the name of the student', 'the time of day the experiment ends'])]
    stem = f'Research question: "{inv[1]}" Which is a{"n" if ask == "independent" else ""} {ask} variable?'
    return mcq(rng, stem, right, wr, f'IV = {inv[2]}; DV = {inv[3]}.')


@R.add('ch11-st1', 'C3', (1, 4), 'short')
def c3_inv_control(rng, slot):
    inv = pick(rng, INV)
    cv, how = pick(rng, inv[4])
    stem = f'In an investigation of {inv[0]} (research question: "{inv[1]}"), explain why {cv} must be controlled and state how this could be done.'
    return dict(stem=stem, answer=f'{cap(cv)} could also affect {inv[3]}, so changes in the DV could not be attributed to {inv[2]} alone; {how}.',
                markingKey=f'Could affect the DV / fair test (1); method: {how} (1).', type='short', marks=2)


@R.add('ch11-st1', 'C3', (1, 4), 'mcq')
def c3_inv_focused(rng, slot):
    inv = pick(rng, INV)
    right = inv[1]
    wr = [f'What affects {inv[0]}?', f'Does the {inv[2]} matter?', f'How does {inv[3]} change {inv[2]}?']
    stem = f'Which is the most focused research question for an investigation of {inv[0]}?'
    return mcq(rng, stem, right, wr, 'States IV with range, DV with method, and the system.')


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def c2_inv_hyp(rng, slot):
    HYP = {'gas collection': ('the rate increases with concentration', 'more particles per unit volume, so more frequent successful collisions'),
           'visual timing': ('the rate increases with temperature', 'a larger fraction of particles has energy ≥ Ea and collisions are more frequent'),
           'calorimetry': ('ΔHc becomes more exothermic by a roughly constant amount per CH₂', 'each extra CH₂ adds the same bonds broken and formed in combustion'),
           'mass loss': ('the rate increases with catalyst mass', 'a larger surface area provides more active sites for the lower-Ea pathway'),
           'titration': ('the ascorbic acid concentration falls more at higher temperature', 'oxidation of ascorbic acid is faster at higher temperature'),
           'crystallisation': ('crystals appear at higher temperatures for more concentrated solutions', 'the solubility of KNO₃ increases with temperature because dissolving is endothermic'),
           'colorimetry': ('absorbance is directly proportional to concentration', 'more absorbing ions in the light path (Beer–Lambert law)'),
           'electrochemistry': ('the cell potential increases with [Cu²⁺]', 'a higher [Cu²⁺] shifts Cu²⁺ + 2e⁻ ⇌ Cu right, making the copper electrode potential more positive'),
           'pH measurement': ('pH increases as concentration decreases, while the degree of dissociation rises', 'dilution shifts the weak-acid equilibrium towards ions'),
           'precipitation timing': ('the precipitate forms fastest for the iodo compound', 'the C–I bond is weakest, so it breaks most easily')}
    inv = pick(rng, INV)
    h, why = HYP[inv[5]]
    stem = f'Formulate a hypothesis, with scientific justification, for the research question: "{inv[1]}"'
    return dict(stem=stem, answer=f'Hypothesis: {h}, because {why}.', markingKey=f'Testable prediction relating IV and DV (1); scientific reasoning: {why} (1–2).', type='explain', marks=3)


R.mcqs('ch11-st1', 'C2', (1, 4), [
    ('Why should an IA investigation include repeated trials?', 'To assess and reduce the effect of random errors on the mean.', ['To remove systematic errors.', 'To increase the range of the IV.', 'To avoid controlling variables.'], 'Repeats average out random scatter.'),
    ('Why is a pilot (preliminary) experiment carried out?', 'To check that the method and IV range give measurable results.', ['To collect the final data.', 'To calculate percentage error.', 'To write the conclusion.'], 'Refines the method.'),
    ('Why is "How does catalyst affect rate?" a weak research question?', 'It does not specify the catalyst, range, reaction or how the rate is measured.', ['It is too detailed.', 'It contains units.', 'It names the dependent variable.'], 'Not focused.'),
    ('Why should the IV be continuous where possible?', 'It allows a graph and quantitative relationship to be determined.', ['It removes uncertainty.', 'It avoids repeats.', 'It reduces the number of controlled variables.'], 'Enables trend analysis.'),
])
R.mcqs('ch11-st1', 'C3', (1, 4), [
    ('In an investigation of how temperature affects the rate of the iodine clock reaction, which is the dependent variable?', 'the time for the blue-black colour to appear', ['the temperature', 'the volume of starch', 'the concentration of iodide'], 'Measured response.'),
    ('A student varies the concentration of acid and measures the time for a magnesium strip to dissolve. Which variable must be controlled?', 'the mass of magnesium', ['the time taken', 'the acid concentration', 'the volume of hydrogen produced'], 'Affects the DV.'),
])


# ---- ch11-st2 methodology, data and uncertainties ----
GLASS = [('burette', 50.00, 0.05, 'cm³', 2), ('25 cm³ pipette', 25.00, 0.03, 'cm³', 2), ('250 cm³ volumetric flask', 250.0, 0.2, 'cm³', 1),
         ('100 cm³ measuring cylinder', 100.0, 0.5, 'cm³', 1), ('10 cm³ pipette', 10.00, 0.02, 'cm³', 2), ('50 cm³ measuring cylinder', 50.0, 0.5, 'cm³', 1)]

R.facts('ch11-st2', F(
    terms=[('random error', 'an unpredictable variation in a measurement that makes readings scatter either side of the true value; reduced by repeating and averaging'),
           ('systematic error', 'an error that shifts all readings in the same direction by a similar amount, e.g. from a miscalibrated instrument; not reduced by repeats'),
           ('absolute uncertainty', 'the range, ± value, within which the true value of a measurement is expected to lie, with the same units as the measurement'),
           ('percentage uncertainty', 'the absolute uncertainty divided by the measured value, multiplied by 100'),
           ('precision', 'how close repeated measurements are to one another (small random uncertainty)'),
           ('accuracy', 'how close a measurement or result is to the true or accepted value')],
    facts=[('What is the uncertainty of a reading from an analogue instrument, such as a burette scale?', 'half the smallest division', ['the smallest division', 'twice the smallest division', 'zero'], '±0.05 cm³ on a burette.'),
           ('What is the uncertainty of a digital balance reading 12.345 g?', '±0.001 g', ['±0.005 g', '±0.01 g', '±0.0005 g'], 'Last digit.'),
           ('How are absolute uncertainties combined when two quantities are subtracted?', 'they are added', ['they are subtracted', 'they are multiplied', 'the larger is used'], 'e.g. titre = final − initial.'),
           ('How are uncertainties combined when quantities are multiplied or divided?', 'percentage uncertainties are added', ['absolute uncertainties are added', 'percentage uncertainties are multiplied', 'they are averaged'], 'Relative uncertainties add.'),
           ('What happens to the percentage uncertainty when a quantity is squared?', 'it is doubled', ['it is halved', 'it is unchanged', 'it is squared'], 'Power rule.'),
           ('Which change reduces the percentage uncertainty in a temperature rise?', 'producing a larger temperature change', ['using a smaller mass of water', 'reading the thermometer less often', 'using a larger beaker without a lid'], 'Same absolute uncertainty over a larger value.')],
    why=[('Explain why the uncertainty of a titre is ±0.10 cm³ when each burette reading is ±0.05 cm³.', 'The titre is the difference between two readings, and absolute uncertainties are added when quantities are subtracted: 0.05 + 0.05 = 0.10 cm³.'),
         ('Explain why repeating trials does not reduce a systematic error.', 'A systematic error shifts every reading in the same direction, so the mean is shifted by the same amount; only changing the method or calibrating removes it.'),
         ('Explain why a pipette is preferred to a measuring cylinder for measuring 25 cm³ of solution in a titration.', 'The pipette has a much smaller uncertainty (±0.03 vs ±0.5 cm³), so the percentage uncertainty of the volume, and hence of the calculated concentration, is lower.'),
         ('Explain why the processed result should not be quoted to more significant figures than the raw data justify.', 'The precision of a calculated result is limited by the least precise measurement; extra figures imply a precision that was not achieved.')],
    contrast=[('random error', 'systematic error', 'Random errors scatter readings either side of the true value and are reduced by repeats; systematic errors shift all readings in one direction and require a change of method.'),
              ('accuracy', 'precision', 'Accuracy is closeness to the true value; precision is closeness of repeated readings to each other.')],
    misc=[('Using more significant figures makes a result more accurate.', 'Reporting more figures does not improve accuracy; it should reflect the precision of the measurements.'),
          ('Uncertainties are always added as absolute values.', 'Absolute uncertainties are added for sums and differences; percentage uncertainties are added for products and quotients.')],
    apply=[('A temperature rises from 21.4 ± 0.1 °C to 29.8 ± 0.1 °C. Calculate ΔT with its absolute and percentage uncertainty.', '8.4 ± 0.2 °C (2.4 %)', 2),
           ('Calculate the percentage uncertainty in a concentration found from n = 0.00250 ± 0.5 % mol and V = 25.00 ± 0.03 cm³.', '0.5 % + 0.12 % = 0.6 %', 2)],
    evaluate=[('Repeating each measurement five times guarantees an accurate result.', ['reduces random error in the mean', 'reveals anomalous results'], ['does not remove systematic errors', 'precise results can still be inaccurate'], 'Repeats improve precision and reliability, but accuracy also needs the absence of systematic error.'),
              ('Digital instruments always give more reliable data than analogue ones.', ['remove reading (parallax) errors', 'often higher resolution'], ['can be miscalibrated (systematic error)', 'displayed resolution may exceed true accuracy', 'response time may lag'], 'Digital instruments reduce reading error, but calibration and real accuracy still need to be checked.')],
    extended=[('In a titration, 25.00 ± 0.03 cm³ of NaOH was neutralised by a mean titre of 22.45 ± 0.10 cm³ of 0.1000 ± 0.0002 mol dm⁻³ HCl. (a) Calculate the concentration of the NaOH. (b) Calculate its percentage and absolute uncertainty. (c) Identify the largest source of uncertainty and suggest how to reduce it.', '(a) 0.1000 × 22.45/25.00 = 0.0898 mol dm⁻³. (b) 0.2 % + 0.45 % + 0.12 % = 0.77 % ≈ 0.8 %; ±0.0007 mol dm⁻³. (c) the titre (0.45 %): use a more dilute acid to give a larger titre or a burette with finer graduations.', 8, 'multi_step')],
))

repeat_readings(R, 'ch11-st2', 'the titre', 'cm³', 18.0, 28.0, 2,
                ['titrated a vinegar sample against standardised sodium hydroxide.', 'titrated diluted bleach with sodium thiosulfate.', 'titrated an antacid solution with hydrochloric acid.'])
repeat_readings(R, 'ch11-st2', 'the temperature rise', '°C', 6.0, 18.0, 1,
                ['measured the temperature change on neutralising an acid with an alkali in a polystyrene cup.', 'measured the temperature rise of water heated by a spirit burner.'])


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def c3_titre_unc(rng, slot):
    i0 = round(rng.uniform(0.0, 5.0), 2)
    i0 = round(round(i0 * 20) / 20, 2)
    t = round(round(rng.uniform(15.0, 30.0) * 20) / 20, 2)
    f_ = round(i0 + t, 2)
    pct = 0.10 / t * 100
    stem = f'Burette readings (±0.05 cm³): initial {i0:.2f} cm³, final {f_:.2f} cm³. Calculate the titre with its absolute and percentage uncertainty.'
    if slot.type == 'mcq':
        return mcq(rng, stem, f'{t:.2f} ± 0.10 cm³ ({pct:.2f} %)', [f'{t:.2f} ± 0.05 cm³ ({pct / 2:.2f} %)', f'{t:.2f} ± 0.10 cm³ ({pct / 2:.2f} %)', f'{t:.2f} ± 0.00 cm³ (0.00 %)'],
                   'Two readings: absolute uncertainties add.')
    return num(stem, f'{t:.2f} ± 0.10 cm³ ({pct:.2f} %)', f'titre = {f_:.2f} − {i0:.2f} = {t:.2f} cm³ (A1); ±(0.05 + 0.05) = ±0.10 cm³ (A1); 0.10/{t:.2f} × 100 = {pct:.2f} % (A1).', 3)


@R.add('ch11-st2', 'C3', (2, 5), 'numerical')
def c3_q_unc(rng, slot):
    m = round(rng.uniform(40.0, 150.0), 1)
    t1 = round(rng.uniform(18.0, 24.0), 1)
    dT = round(rng.uniform(4.0, 25.0), 1)
    t2 = round(t1 + dT, 1)
    dT = round(t2 - t1, 1)
    qv = m * CW * dT
    pm = 0.1 / m * 100
    pt = 0.2 / dT * 100
    tot = pm + pt
    stem = (f'A student heated {m:.1f} ± 0.1 g of water from {t1:.1f} ± 0.1 °C to {t2:.1f} ± 0.1 °C. Calculate the heat absorbed, q = mcΔT (c = 4.18 J g⁻¹ K⁻¹), '
            'and its absolute uncertainty (ignore the uncertainty in c).')
    au = qv * tot / 100
    return num(stem, f'{q(qv, "J")} ± {sf(au, 2)} J',
               f'ΔT = {dT:.1f} ± 0.2 °C (M1); q = {m:.1f} × 4.18 × {dT:.1f} = {sf(qv)} J (A1); % unc = {pm:.2f} + {pt:.2f} = {tot:.2f} % (M1); ±{sf(au, 2)} J (A1).', 4, 'multi_step')


@R.add('ch11-st2', 'C3', (2, 5), 'numerical')
def c3_conc_unc(rng, slot):
    g = pick(rng, GLASS[:3])
    m = round(rng.uniform(1.0, 5.0), 3)
    sub = pick(rng, [('sodium carbonate', 'Na2CO3'), ('potassium hydrogenphthalate', 'C8H5KO4'), ('oxalic acid dihydrate', 'C2H6O6'), ('sodium chloride', 'NaCl')])
    M = mr(sub[1])
    V = 250.0
    c = m / M / (V / 1000)
    pm = 0.001 / m * 100
    pv = 0.2 / V * 100
    tot = pm + pv
    stem = (f'{m:.3f} ± 0.001 g of {sub[0]} (M = {M:.2f} g mol⁻¹) is dissolved and made up to 250.0 ± 0.2 cm³ in a volumetric flask. '
            'Calculate the concentration and its percentage uncertainty.')
    return num(stem, f'{q(c, "mol dm⁻³", 3)} ± {tot:.2f} %', f'c = ({m:.3f}/{M:.2f})/0.2500 = {sf(c)} mol dm⁻³ (A1); % unc = {pm:.3f} + {pv:.2f} = {tot:.2f} % (M1 A1).', 3)


@R.add('ch11-st2', 'C3', (1, 4), 'mcq')
def c3x_instrument_unc(rng, slot):
    g = pick(rng, GLASS)
    val = g[1] * rng.choice([0.4, 0.5, 0.8, 1.0]) if g[0] in ('burette',) or 'cylinder' in g[0] else g[1]
    val = round(val, g[4])
    p = g[2] / val * 100
    stem = f'A volume of {val:.{g[4]}f} cm³ is measured with a {g[0]} (uncertainty ±{g[2]} cm³). What is the percentage uncertainty?'
    wr = [p * 2, p / 2, p * 10]
    return nmcq(rng, stem, p, wr, '%', f'{g[2]}/{val:.{g[4]}f} × 100.', n=2)


@R.add('ch11-st2', 'C3', (1, 4), 'mcq')
def c3x_error_type(rng, slot):
    SYS = ['The balance read 0.02 g with nothing on it.', 'Heat was lost to the surroundings in every calorimetry run.', 'The pH meter was calibrated with an out-of-date buffer.',
           'The thermometer reads 0.5 °C too high at all temperatures.', 'The student always read the burette at eye level above the meniscus.', 'The gas syringe stuck slightly, so volumes were always low.']
    RAN = ['The stopwatch was started a fraction of a second early or late in different trials.', 'The end-point colour was judged slightly differently each time.',
           'Small fluctuations in room draughts affected the flame each run.', 'The last digit of the balance fluctuated between readings.', 'The cross was judged to disappear at slightly different times.']
    kind = rng.choice(['systematic', 'random'])
    right = pick(rng, SYS if kind == 'systematic' else RAN)
    wr = rng.sample(RAN if kind == 'systematic' else SYS, 3)
    stem = f'Which source of error is {kind}?'
    return mcq(rng, stem, right, wr, 'Systematic: same direction every time; random: scatter either side.' if kind == 'systematic' else 'Random: unpredictable scatter between trials.')


R.mcqs('ch11-st2', 'C2', (1, 4), [
    ('Why is the mean of repeated titres calculated only from concordant results?', 'Concordant titres (within ±0.10 cm³) exclude rough or anomalous values.', ['To make the uncertainty zero.', 'Because the rough titre is always most accurate.', 'To remove systematic error.'], 'Reliability.'),
    ('Why does a larger titre give a smaller percentage uncertainty?', 'The absolute uncertainty stays ±0.10 cm³ while the measured value increases.', ['The burette is more precise.', 'The uncertainty becomes zero.', 'Systematic errors cancel.'], 'Ratio falls.'),
    ('Why are the uncertainties of a mass by difference added?', 'Each of the two weighings has its own uncertainty.', ['Masses are multiplied.', 'Only the larger mass counts.', 'Balances are digital.'], 'Subtraction rule.'),
    ('Why is a polystyrene cup with a lid used in calorimetry?', 'To reduce heat exchange with the surroundings (a systematic error).', ['To increase random error.', 'To speed up the reaction.', 'To measure volume.'], 'Insulation.'),
])


@p1b(R, 'ch11-st2')
def p1b_titration_ia(rng, slot):
    sub = pick(rng, [('ethanoic acid in vinegar', 'CH₃COOH', 1, 'sodium hydroxide', 'phenolphthalein'), ('sodium hydroxide in drain cleaner', 'NaOH', 1, 'hydrochloric acid', 'methyl orange')])
    cb = pick(rng, [0.1000, 0.1050, 0.0980])
    va = 25.00
    tit = rng.uniform(19.0, 27.0)
    ts = [round(round((tit + rng.uniform(-0.12, 0.12)) * 20) / 20, 2) for _ in range(3)]
    rough = round(round((tit + rng.uniform(0.4, 0.9)) * 20) / 20, 2)
    conc = [x for x in ts if max(ts) - min(ts) <= 0.20]
    if len(conc) < 3:
        return None
    mean = sum(ts) / 3
    c = cb * mean / va
    pct = 0.0002 / cb * 100 + 0.10 / mean * 100 + 0.03 / va * 100
    intro = (f'A student determined the concentration of {sub[0]} (diluted) by titrating 25.00 ± 0.03 cm³ portions with {cb:.4f} ± 0.0002 mol dm⁻³ {sub[3]} using {sub[4]}.\n\n'
             f'trial | rough | 1 | 2 | 3\ntitre / cm³ (±0.10) | {rough:.2f} | ' + ' | '.join(f'{x:.2f}' for x in ts))
    return dict(intro=intro, parts=[
        ('Calculate the mean titre, explaining which trials you used.', f'{mean:.2f} cm³ from trials 1–3 (rough excluded)', f'mean of concordant trials = {mean:.2f} cm³ (A1); rough titre excluded (1).', 2),
        ('Calculate the concentration of the diluted sample.', q(c, 'mol dm⁻³'), f'n = {cb:.4f} × {mean:.2f}/1000 = {sf(cb * mean / 1000)} mol (M1); c = n/0.02500 = {q(c, "mol dm⁻³")} (A1).', 2),
        ('Calculate the percentage uncertainty in the concentration.', f'{pct:.2f} %', f'{0.0002 / cb * 100:.2f} + {0.10 / mean * 100:.2f} + {0.03 / va * 100:.2f} (M1) = {pct:.2f} % (A1).', 2),
        ('Identify the largest contributor to the uncertainty and suggest an improvement.', 'the titre; use a larger titre (more concentrated sample or smaller-volume burette with finer scale)', 'titre identified (1); valid improvement (1).', 2)],
        extras=[('State why the burette was rinsed with the titrant before filling.', 'To prevent dilution of the titrant by residual water.', 'avoid dilution (1).', 1)])


# ---- ch11-st3 analysis, conclusion and evaluation ----
IA_WEAK = [('heat loss to the surroundings in calorimetry', 'the temperature rise and so |ΔH| are too small', 'insulate the cup, use a lid and extrapolate a cooling curve back to the time of mixing'),
        ('incomplete combustion of the alcohol (soot on the calorimeter)', 'less energy is released, so |ΔHc| is too small', 'ensure a good air supply and use a draught shield'),
        ('gas escaping before the bung is replaced', 'measured gas volumes are too low', 'use a divided flask or a tube containing the solid that is tipped after sealing'),
        ('judging the colour change of the end point subjectively', 'random scatter in titres or times', 'use a colorimeter or pH probe to detect the end point'),
        ('temperature not controlled in rate experiments', 'rates vary between trials unpredictably', 'carry out all trials in a thermostatic water bath'),
        ('evaporation of volatile alcohol from the spirit burner before weighing', 'the mass burned is overestimated, so |ΔHc| is too small', 'put the cap on the burner immediately and reweigh quickly'),
        ('only three values of the independent variable', 'the trend cannot be established reliably', 'use at least five values across a wider range')]

R.facts('ch11-st3', F(
    terms=[('line of best fit', 'a straight line or smooth curve drawn through data so that points are evenly scattered on either side, showing the trend'),
           ('anomalous result', 'a data point that does not fit the pattern of the others, often caused by a mistake, and is investigated or excluded from analysis'),
           ('percentage error', 'the difference between the experimental and literature values divided by the literature value, multiplied by 100'),
           ('gradient uncertainty', 'half the difference between the steepest and shallowest lines that pass through the error bars of the data'),
           ('error bars', 'lines drawn on data points to show the absolute uncertainty in a plotted quantity'),
           ('extrapolation', 'extending a graph beyond the measured data range to estimate a value')],
    facts=[('When is a difference from the literature value explained by random errors alone?', 'when the percentage error is less than the percentage uncertainty', ['when the percentage error is greater than the percentage uncertainty', 'whenever repeats are taken', 'never'], 'Otherwise systematic errors are present.'),
           ('What does a straight line through the origin on a graph of y against x show?', 'y is directly proportional to x', ['y is inversely proportional to x', 'y is independent of x', 'y increases exponentially'], 'y = kx.'),
           ('Which IA criterion is concerned with weaknesses and improvements?', 'Evaluation', ['Research design', 'Data analysis', 'Conclusion'], 'Limitations and realistic improvements.'),
           ('Which IA criterion requires a conclusion justified by the data and compared with accepted science?', 'Conclusion', ['Research design', 'Evaluation', 'Data analysis'], 'Answer the RQ.'),
           ('How is an anomalous result usually treated?', 'It is identified, explained if possible and excluded from the mean or line of best fit.', ['It is always included.', 'It is deleted without comment.', 'It is replaced by an estimate.'], 'Transparency.'),
           ('What does a large y-intercept on a graph expected to pass through the origin suggest?', 'a systematic error', ['a random error', 'perfect accuracy', 'high precision'], 'Shift of all values.')],
    why=[('Explain why the gradient of a graph is often a better result than a single calculated value.', 'The gradient uses all data points, so random errors in individual readings are averaged, and a systematic offset affects the intercept rather than the gradient.'),
         ('Explain why improvements in the evaluation should be specific and realistic.', 'Vague suggestions such as "be more careful" do not address the identified weakness; a specific change, linked to a source of error, shows understanding of how it would improve the data.'),
         ('Explain why a conclusion should refer to the uncertainty of the result.', 'The uncertainty shows how confident the conclusion is and whether the difference from the literature value can be explained by random error.'),
         ('Explain why a strong correlation does not prove a causal relationship.', 'Another uncontrolled variable may be responsible for both changes; a scientific mechanism and controlled variables are needed to support causation.')],
    contrast=[('percentage error', 'percentage uncertainty', 'Percentage error compares the result with an accepted value (accuracy); percentage uncertainty is the estimated range of the result from measurement limitations (precision).'),
              ('a limitation of the method', 'a realistic improvement', 'A limitation is a weakness that affected the data; an improvement is a specific change that would reduce that weakness.')],
    misc=[('A percentage error of 5 % means the uncertainty is 5 %.', 'Percentage error measures accuracy against the literature value; uncertainty is calculated from the measurements.'),
          ('All points must lie on the line of best fit.', 'Points should scatter evenly either side; error bars that cross the line indicate a good fit.')],
    apply=[('A student obtained ΔHc(ethanol) = −1050 ± 5 % kJ mol⁻¹; the literature value is −1367 kJ mol⁻¹. Comment on the result.', 'Percentage error = 23 %, larger than 5 % uncertainty, so systematic errors (heat loss, incomplete combustion) dominate.', 3),
           ('The steepest and shallowest lines through error bars have gradients of −4950 K and −4550 K. State the gradient with its uncertainty.', '−4750 ± 200 K', 2)],
    evaluate=[('A result with a small percentage uncertainty is necessarily accurate.', ['small random error suggests careful measurement', 'precise data allow trends to be seen'], ['systematic errors may still shift the result', 'precision is not accuracy'], 'No – a precise result can be inaccurate; comparing with the literature value tests accuracy.'),
              ('Excluding anomalous results improves the validity of a conclusion.', ['removes values caused by mistakes', 'gives a more representative mean or line'], ['may hide a real effect', 'must be justified, not just inconvenient'], 'Only when the anomaly is justified; otherwise it should be investigated and repeated.')],
    extended=[('In an investigation of ΔHc of alcohols, the student obtained −590, −1050, −1500 and −1990 kJ mol⁻¹ for methanol to butan-1-ol (literature: −726, −1367, −2021, −2676). (a) Describe the trend. (b) Calculate the percentage error for butan-1-ol. (c) Identify two systematic errors and their effect. (d) Suggest improvements and evaluate whether the conclusion is valid.', '(a) ΔHc becomes more negative by about 450–490 kJ mol⁻¹ per CH₂. (b) |−1990 − (−2676)|/2676 × 100 = 25.6 %. (c) heat loss to surroundings and incomplete combustion → values too small. (d) draught shield, lid, insulated calorimeter or bomb calorimeter; trend is valid (linear increase) but absolute values are inaccurate.', 9, 'multi_step')],
))

pct_error(R, 'ch11-st3', 'the enthalpy of neutralisation', 'kJ mol⁻¹', -57.1, 0.75, 0.95,
          ['mixed equal volumes of 1.00 mol dm⁻³ HCl and NaOH in a polystyrene cup.', 'measured the temperature rise on neutralising nitric acid with potassium hydroxide.'],
          ['heat lost to the surroundings, making ΔT too small – use a lid and extrapolate the cooling curve', 'heat absorbed by the cup and thermometer – include their heat capacity or use a vacuum flask'], signed=True)
pct_error(R, 'ch11-st3', 'the molar volume of a gas at room conditions', 'dm³ mol⁻¹', 24.5, 0.85, 0.97,
          ['reacted magnesium with excess acid and collected hydrogen in a gas syringe.', 'collected carbon dioxide over water from the reaction of calcium carbonate with acid.'],
          ['gas lost before the bung was inserted – use a tipping tube to start the reaction after sealing', 'some CO₂ dissolved in the water – collect in a gas syringe instead'])


@R.add('ch11-st3', 'C3', (1, 5), 'numerical')
def c3_grad_unc(rng, slot):
    g = rsf(rng.uniform(-9000, -3000), 3)
    d = abs(g) * rng.uniform(0.03, 0.08)
    gmax, gmin = rsf(g - d, 3), rsf(g + d, 3)
    best = (gmax + gmin) / 2
    u = abs(gmax - gmin) / 2
    stem = (f'A graph of ln k against 1/T was drawn with error bars. The steepest and shallowest lines through the error bars have gradients of {sgn(gmax, 3, "K")} and {sgn(gmin, 3, "K")}. '
            'State the gradient with its absolute uncertainty' + (' and calculate Ea with its uncertainty (R = 8.31 J K⁻¹ mol⁻¹).' if slot.d >= 3 else '.'))
    if slot.d >= 3:
        ea = -best * RGAS / 1000
        ue = u * RGAS / 1000
        return num(stem, f'{sgn(best, 3, "K")} ± {sf(u, 2)} K; Ea = {sf(ea)} ± {sf(ue, 2)} kJ mol⁻¹',
                   f'mean gradient = {sf(best)} K (A1); ± half difference = {sf(u, 2)} K (A1); Ea = −gradient × R = {sf(ea)} kJ mol⁻¹ (A1) ± {sf(ue, 2)} (A1).', 4, 'multi_step')
    return num(stem, f'{sgn(best, 3, "K")} ± {sf(u, 2)} K', f'mean of the two gradients = {sf(best)} K (A1); uncertainty = |{sf(gmax)} − ({sf(gmin)})|/2 = {sf(u, 2)} K (A1).', 2)


@R.add('ch11-st3', 'C3', (2, 5), 'numerical')
def c3_err_vs_unc(rng, slot):
    case = pick(rng, [('ΔH of neutralisation', -57.1, 'kJ mol⁻¹', True), ('ΔHc of ethanol', -1367, 'kJ mol⁻¹', True), ('Ka of ethanoic acid', 1.74e-5, 'mol dm⁻³', False),
                      ('molar volume of hydrogen at room conditions', 24.5, 'dm³ mol⁻¹', False), ('Ea of the iodine clock reaction', 53.0, 'kJ mol⁻¹', False)])
    nm, lit, u, sg = case
    unc = rng.choice([2.0, 3.0, 4.0, 5.0, 6.0, 8.0])
    err = rng.uniform(0.5, 12.0)
    v = lit * (1 - err / 100) if rng.random() < 0.7 else lit * (1 + err / 100)
    v = rsf(v, 3)
    e = abs(v - lit) / abs(lit) * 100
    vs = sgn(v, 3, u) if sg else q(v, u)
    ls = sgn(lit, 3, u) if sg else q(lit, u)
    within = e <= unc
    stem = f'A student determined the {nm} as {vs} ± {unc:.0f} %. The literature value is {ls}. Calculate the percentage error and deduce whether random errors alone can account for the difference.'
    concl = 'yes – the percentage error is within the percentage uncertainty, so random errors can account for it' if within else 'no – the percentage error exceeds the percentage uncertainty, so systematic errors must also be present'
    return num(stem, f'{e:.1f} %; {concl}', f'|{sf(v)} − ({sf(lit)})|/|{sf(lit)}| × 100 = {e:.1f} % (M1 A1); compare with {unc:.0f} %: {concl} (R1).', 3)


@R.add('ch11-st3', 'C3', (1, 4), 'short')
def c3_weakness(rng, slot):
    w, eff, imp = pick(rng, IA_WEAK)
    stem = f'In the evaluation of an investigation, a student identifies "{w}" as a weakness. State its effect on the results and suggest a realistic improvement.'
    return dict(stem=stem, answer=f'Effect: {eff}. Improvement: {imp}.', markingKey=f'Effect on the data (1); specific improvement: {imp} (1).', type='short', marks=2)


@R.add('ch11-st3', 'C3', (1, 4), 'mcq')
def c3x_weak_fix(rng, slot):
    i = rng.randrange(len(IA_WEAK))
    w, eff, imp = IA_WEAK[i]
    wr = [x[2] for j, x in enumerate(IA_WEAK) if j != i]
    rng.shuffle(wr)
    stem = f'Which improvement best addresses the weakness "{w}"?'
    return mcq(rng, stem, imp, wr[:2] + ['repeat the experiment more carefully'], eff + '.')


@R.add('ch11-st3', 'C3', (1, 4), 'mcq')
def c3x_anomaly(rng, slot):
    base = rng.uniform(20.0, 40.0)
    vals = [round(base + rng.uniform(-0.3, 0.3), 1) for _ in range(4)]
    k = rng.randrange(5)
    bad = round(base + rng.choice([-1, 1]) * rng.uniform(2.5, 4.0), 1)
    vals.insert(k, bad)
    good = [v for j, v in enumerate(vals) if j != k]
    mg = sum(good) / 4
    mall = sum(vals) / 5
    stem = f'Five repeat times for a cross to disappear were {", ".join(f"{v:.1f}" for v in vals)} s. What is the most appropriate mean?'
    right = f'{mg:.1f} s (excluding {bad:.1f} s)'
    wr = [f'{mall:.1f} s (all five values)', f'{(max(vals) + min(vals)) / 2:.1f} s (mid-range)', f'{sorted(vals)[2]:.1f} s (median)']
    if len({right.split()[0]} | {w.split()[0] for w in wr}) < 4:
        return None
    return mcq(rng, stem, right, wr, f'{bad:.1f} s is anomalous and excluded.')


R.mcqs('ch11-st3', 'C2', (1, 4), [
    ('Why is the y-intercept of a calibration graph of absorbance against concentration expected to be zero?', 'A solution with no absorbing species should have zero absorbance relative to the blank.', ['Absorbance is always zero.', 'The cuvette absorbs all light.', 'Concentration is never zero.'], 'Blank sets zero.'),
    ('Why do error bars that all overlap the line of best fit support the relationship?', 'The deviations can be explained by the measurement uncertainty.', ['They show systematic error.', 'They prove causation.', 'They show the gradient is zero.'], 'Consistent with random error.'),
    ('Why might a calorimetry result be consistently less exothermic than the literature value?', 'Heat is lost to the surroundings in every trial.', ['Random errors in reading the thermometer.', 'Too many repeats.', 'The balance is too precise.'], 'Systematic error.'),
    ('Why should a conclusion compare the result with the literature value?', 'To assess the accuracy of the result.', ['To calculate the uncertainty.', 'To identify the IV.', 'To avoid evaluation.'], 'Percentage error.'),
])


@p1b(R, 'ch11-st3')
def p1b_beer_lambert(rng, slot):
    eps = rng.uniform(9.0, 13.0)
    cs = [0.020, 0.040, 0.060, 0.080, 0.100]
    off = rng.choice([0.000, 0.000, 0.020, 0.030])
    ab = [round(eps * c + off + rng.uniform(-0.008, 0.008), 3) for c in cs]
    au = round(rng.uniform(0.30, 0.95), 3)
    # best-fit through data (least squares)
    mx = sum(cs) / 5
    my = sum(ab) / 5
    sl = sum((x - mx) * (y - my) for x, y in zip(cs, ab)) / sum((x - mx) ** 2 for x in cs)
    ic = my - sl * mx
    cu = (au - ic) / sl
    intro = ('A student measured the absorbance of copper(II) sulfate solutions at 635 nm with a colorimeter, then measured an unknown solution.\n\n'
             'concentration / mol dm⁻³ | ' + ' | '.join(f'{c:.3f}' for c in cs) + '\nabsorbance | ' + ' | '.join(f'{a:.3f}' for a in ab) +
             f'\n\nAbsorbance of the unknown = {au:.3f}')
    sysmsg = (f'The intercept ({sf(ic, 2)}) is not zero, suggesting a systematic error such as not zeroing with a blank or a dirty cuvette.' if abs(ic) > 0.012
              else f'The intercept ({sf(ic, 1) if abs(ic) >= 0.001 else "≈ 0"}) is close to zero, so no significant systematic error is indicated.')
    return dict(intro=intro, parts=[
        ('Determine the gradient of the line of best fit, with units.', f'{sf(sl)} mol⁻¹ dm³', f'gradient from best-fit line ≈ {sf(sl)} (A1); unit mol⁻¹ dm³ (A1).', 2),
        ('Determine the concentration of the unknown solution.', q(cu, 'mol dm⁻³'), f'c = (A − intercept)/gradient = ({au:.3f} − ({sf(ic, 2)}))/{sf(sl)} = {q(cu, "mol dm⁻³")} (M1 A1).', 2),
        ('Comment on the y-intercept of the line.', sysmsg, 'value of intercept (1); interpretation (1).', 2),
        ('Suggest why the unknown should lie within the range of the standards.', 'Extrapolation assumes linearity continues; Beer–Lambert may fail at high concentration.', 'interpolation more reliable (1).', 1),
        ('State one variable that must be kept constant for all solutions.', 'wavelength/filter, path length (same cuvette) or temperature', 'one valid variable (1).', 1)],
        extras=[('State why the colorimeter is zeroed with distilled water.', 'To remove absorbance from the solvent and cuvette.', 'blank (1).', 1)])


R.mcqs('ch11-st2', 'C1', (1, 3), [
    ('What is the uncertainty of a 50 cm³ burette reading?', '±0.05 cm³', ['±0.1 cm³', '±0.5 cm³', '±0.01 cm³'], 'Half of 0.1 cm³ division.'),
    ('Which piece of glassware has the smallest uncertainty for measuring 25 cm³?', 'a 25 cm³ volumetric pipette', ['a 50 cm³ measuring cylinder', 'a 100 cm³ beaker', 'a conical flask'], '±0.03 cm³.'),
])
R.mcqs('ch11-st3', 'C1', (1, 3), [
    ('What does a percentage error measure?', 'the accuracy of a result compared with an accepted value', ['the precision of repeats', 'the range of the IV', 'the instrument resolution'], 'Accuracy.'),
    ('What are error bars used to show?', 'the uncertainty in plotted values', ['the line of best fit', 'anomalous points only', 'the gradient'], 'Visual uncertainty.'),
])


# ---- extra C4 for ch04-st4 (ΔG⦵ and K across temperatures) ----
DG_RX = [('N₂(g) + 3H₂(g) ⇌ 2NH₃(g)', -92.2, -199, 'the Haber process'), ('2SO₂(g) + O₂(g) ⇌ 2SO₃(g)', -196, -188, 'the Contact process'),
         ('CH₄(g) + H₂O(g) ⇌ CO(g) + 3H₂(g)', 206, 215, 'steam reforming of methane'),
         ('CaCO₃(s) ⇌ CaO(s) + CO₂(g)', 178, 161, 'the decomposition of limestone'), ('CO(g) + 2H₂(g) ⇌ CH₃OH(g)', -90.7, -219, 'methanol synthesis')]


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step')
def c4_dg_two_temps(rng, slot):
    eq, dh, ds, nm = pick(rng, DG_RX)
    T1 = 298
    T2 = pick(rng, [500, 600, 700, 800, 1000, 1200])
    g1 = dh - T1 * ds / 1000
    g2 = dh - T2 * ds / 1000
    K1 = math.exp(-g1 * 1000 / (RGAS * T1))
    K2 = math.exp(-g2 * 1000 / (RGAS * T2))
    Tx = dh / (ds / 1000)
    stem = (f'For {nm}, {eq}, ΔH⦵ = {sgn(dh, 3, "kJ mol⁻¹")} and ΔS⦵ = {sgn(ds, 3, "J K⁻¹ mol⁻¹")}. '
            f'(a) Calculate ΔG⦵ and K at {T1} K and at {T2} K. (b) Determine the temperature at which K = 1. '
            '(c) Evaluate, using your answers and kinetic considerations, the choice of operating temperature for this process.')
    exo = dh < 0
    judge = ('K falls as T rises (exothermic), so a compromise temperature is used: high enough for an acceptable rate with a catalyst, low enough for a reasonable yield.'
             if exo else 'K rises with T (endothermic, ΔS > 0), so high temperatures favour both yield and rate; the limit is energy cost and materials.')
    ans = (f'(a) {T1} K: ΔG⦵ = {sgn(g1, 3, "kJ mol⁻¹")}, K = {sf(K1)}; {T2} K: ΔG⦵ = {sgn(g2, 3, "kJ mol⁻¹")}, K = {sf(K2)}. '
           f'(b) T = ΔH⦵/ΔS⦵ = {sf(Tx)} K. (c) {judge}')
    key = (f'(a) ΔG⦵ = ΔH⦵ − TΔS⦵ with ΔS in kJ (M1); values (A1 A1); K = e^(−ΔG⦵/RT) (M1) values (A1). (b) {sf(Tx)} K (A1). '
           f'(c) links trend in K to sign of ΔH⦵ (1); rate/catalyst/cost argument and judgement (1).')
    return num(stem, ans, key, 8, 'multi_step', gap='G7')
