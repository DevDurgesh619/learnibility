"""CBSE Class 12 Chemistry, units 4-6: d- and f-block elements, coordination compounds, haloalkanes and haloarenes.

Families are built from fact tables with the shared kit in g11_chemistry_kit.py; numerical answers are computed here.
"""
from __future__ import annotations

import math

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap

P = 'cbse-g12-chemistry'
SUPD = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def sup(n: int) -> str:
    return str(n).translate(SUPD)


def bm(n: int) -> float:
    return math.sqrt(n * (n + 2))


ROMAN = {0: '0', 1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}

# ---------------------------------------------------------------- unit 4: d- and f-block

D3 = [('Sc', 21, 'scandium', 1, 2), ('Ti', 22, 'titanium', 2, 2), ('V', 23, 'vanadium', 3, 2), ('Cr', 24, 'chromium', 5, 1),
      ('Mn', 25, 'manganese', 5, 2), ('Fe', 26, 'iron', 6, 2), ('Co', 27, 'cobalt', 7, 2), ('Ni', 28, 'nickel', 8, 2),
      ('Cu', 29, 'copper', 10, 1), ('Zn', 30, 'zinc', 10, 2)]


def d_config(r):
    s, Z, nm, d, s4 = r.choice(D3)
    good = f'[Ar] 3d{sup(d)} 4s{sup(s4)}'
    cands = []
    if d + s4 <= 10:
        cands.append(f'[Ar] 3d{sup(d + s4)}')
    if s4 == 1:
        cands.append(f'[Ar] 3d{sup(d - 1)} 4s²')
    elif d < 10:
        cands.append(f'[Ar] 3d{sup(d + 1)} 4s¹')
    cands.append(f'[Ar] 3d{sup(d - 1)} 4s² 4p¹' if d > 1 else '[Ar] 4s² 4p¹')
    for k in (Z - 1, Z + 1, Z + 2, Z - 2):
        for x in D3:
            if x[1] == k:
                cands.append(f'[Ar] 3d{sup(x[3])} 4s{sup(x[4])}')
    wrong = [c for c in dict.fromkeys(cands) if c != good]
    note = ' (exceptional: a half-filled/completely filled 3d subshell is extra stable)' if s4 == 1 else ''
    return mcq(f'What is the ground-state electronic configuration of {nm} (Z = {Z})?', good, wrong[:3],
               f'{cap(nm)}: {good}{note}.', r)


ION_MAG = [('Sc³⁺', 0), ('Ti³⁺', 1), ('Ti⁴⁺', 0), ('V³⁺', 2), ('V²⁺', 3), ('Cr³⁺', 3), ('Cr²⁺', 4), ('Mn²⁺', 5), ('Mn³⁺', 4),
           ('Fe²⁺', 4), ('Fe³⁺', 5), ('Co²⁺', 3), ('Co³⁺', 4), ('Ni²⁺', 2), ('Cu²⁺', 1), ('Cu⁺', 0), ('Zn²⁺', 0)]
ION_D = {'Sc³⁺': 0, 'Ti³⁺': 1, 'Ti⁴⁺': 0, 'V³⁺': 2, 'V²⁺': 3, 'Cr³⁺': 3, 'Cr²⁺': 4, 'Mn²⁺': 5, 'Mn³⁺': 4, 'Fe²⁺': 6, 'Fe³⁺': 5,
         'Co²⁺': 7, 'Co³⁺': 6, 'Ni²⁺': 8, 'Cu²⁺': 9, 'Cu⁺': 10, 'Zn²⁺': 10}
ION_Z = {'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30}


def mag_moment(r):
    s, n = r.choice([x for x in ION_MAG if x[1] > 0])
    d = ION_D[s]
    mu = bm(n)
    el = s.rstrip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺')
    return {'stem': f'Calculate the spin-only magnetic moment of {s} ion (Z of {el} = {ION_Z[el]}) in aqueous solution.',
            'answer': f'{mu:.2f} BM', 'key': f'{s} = [Ar] 3d{sup(d)}, with {n} unpaired electron{"s" if n > 1 else ""} (1); μ = √(n(n + 2)) = √({n} × {n + 2}) = {mu:.2f} BM (1).',
            'distractors': [f'{bm(n + 1):.2f} BM', f'{bm(n - 1):.2f} BM' if n > 1 else '2.83 BM', f'{math.sqrt(n):.2f} BM' if n > 1 else '1.00 BM']}


def mag_to_n(r):
    n = r.choice([1, 2, 3, 4, 5])
    mu = bm(n)
    ions = [s for s, k in ION_MAG if k == n]
    return {'stem': f'A divalent or trivalent 3d ion has a spin-only magnetic moment of {mu:.2f} BM. How many unpaired electrons does it have? Name one ion that fits.',
            'answer': f'{n} unpaired electron{"s" if n > 1 else ""}; e.g. {ions[0]}',
            'key': f'μ = √(n(n + 2)) = {mu:.2f} ⇒ n(n + 2) = {n * (n + 2)} ⇒ n = {n} (1); e.g. {", ".join(ions)} (1).',
            'distractors': [f'{n + 1} unpaired electrons', f'{n - 1} unpaired electrons' if n > 1 else '0 unpaired electrons', f'{round(mu)} unpaired electrons' if round(mu) not in (n, n + 1, n - 1) else f'{n + 2} unpaired electrons']}


def colourless(r):
    cl = [s for s, k in ION_MAG if ION_D[s] in (0, 10)]
    co = [s for s, k in ION_MAG if ION_D[s] not in (0, 10)]
    if r.random() < 0.5:
        good = r.choice(cl)
        return mcq('Which of the following ions is colourless in aqueous solution?', good, r.sample(co, 3),
                   f'{good} has a d{sup(ION_D[good])} configuration, so no d–d transition is possible; it is colourless.', r)
    good = r.choice(co)
    return mcq('Which of the following ions is coloured in aqueous solution?', good, r.sample(cl, 3),
               f'{good} is d{sup(ION_D[good])} with partly filled d orbitals, so d–d transitions absorb visible light.', r)


def d_count(r):
    s, n = r.choice(ION_MAG)
    d = ION_D[s]
    el = s.rstrip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺')
    return {'stem': f'How many d electrons are present in {s} (Z of {el} = {ION_Z[el]})? Is it paramagnetic or diamagnetic?',
            'answer': f'd{sup(d)}; {"paramagnetic" if n else "diamagnetic"}',
            'key': f'{s}: [Ar] 3d{sup(d)} (4s electrons are lost first) (1); {n} unpaired ⇒ {"paramagnetic" if n else "diamagnetic"} (1).',
            'distractors': [f'd{sup(d - 1 if d else 1)}; {"diamagnetic" if n else "paramagnetic"}', f'd{sup(d + 1 if d < 10 else d - 2)}; {"paramagnetic" if n else "diamagnetic"}', f'd{sup(d)}; {"diamagnetic" if n else "paramagnetic"}']}


TITR = [('acidified KMnO₄', 'MnO₄⁻', 'Fe²⁺ (as FeSO₄)', 'MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 1, 5),
        ('acidified KMnO₄', 'MnO₄⁻', 'oxalate (as Na₂C₂O₄)', '2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O', 2, 5),
        ('acidified K₂Cr₂O₇', 'Cr₂O₇²⁻', 'Fe²⁺ (as Mohr\'s salt)', 'Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O', 1, 6),
        ('acidified KMnO₄', 'MnO₄⁻', 'iodide (as KI)', '2MnO₄⁻ + 10I⁻ + 16H⁺ → 2Mn²⁺ + 5I₂ + 8H₂O', 2, 10),
        ('acidified K₂Cr₂O₇', 'Cr₂O₇²⁻', 'iodide (as KI)', 'Cr₂O₇²⁻ + 6I⁻ + 14H⁺ → 2Cr³⁺ + 3I₂ + 7H₂O', 1, 6)]


def ox_moles(r):
    ox, oxi, red, eq, a, b = r.choice(TITR)
    n = r.choice([0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1])
    return {'stem': f'How many moles of {oxi} are needed to oxidise {n} mol of {red} in acidic medium? ({eq})',
            'answer': f'{num(n * a / b, 4)} mol', 'key': f'From the equation {a} mol {oxi} ≡ {b} mol reductant (1) ⇒ {n} × {a}/{b} = {num(n * a / b, 4)} mol (1).',
            'distractors': [f'{num(n * b / a, 4)} mol', f'{num(n, 4)} mol', f'{num(n * a / b * 2, 4)} mol']}


def ox_titre(r):
    ox, oxi, red, eq, a, b = r.choice(TITR)
    cr = r.choice([0.05, 0.1, 0.12, 0.15, 0.2])
    vr = r.choice([10, 20, 25])
    co = r.choice([0.01, 0.02, 0.025])
    vo = vr * cr * a / (b * co)
    who = name(r)
    return {'stem': f'{who} titrates {vr} mL of a {cr} M solution of {red} with {co} M {ox}. Using the equation {eq}, calculate the volume of oxidant needed.',
            'answer': f'{sf(vo, 3)} mL',
            'key': f'mol of reductant = {vr} × {cr}/1000 = {sf(vr * cr / 1000, 3)} mol (1); mol {oxi} = {a}/{b} × that = {sf(vr * cr * a / b / 1000, 3)} mol (1); V = n/M = {sf(vo, 3)} mL (1).',
            'distractors': [f'{sf(vr * cr * b / (a * co), 3)} mL', f'{sf(vr * cr / co, 3)} mL', f'{sf(vo / 2, 3)} mL']}


OXS = [('KMnO₄', 'Mn', 7), ('K₂MnO₄', 'Mn', 6), ('MnO₂', 'Mn', 4), ('Mn₂O₇', 'Mn', 7), ('MnSO₄', 'Mn', 2), ('K₂Cr₂O₇', 'Cr', 6),
       ('Na₂CrO₄', 'Cr', 6), ('Cr₂O₃', 'Cr', 3), ('CrO₃', 'Cr', 6), ('FeCr₂O₄', 'Cr', 3), ('CrO₂Cl₂', 'Cr', 6), ('V₂O₅', 'V', 5)]


def ox_state(r):
    c, el, n = r.choice(OXS)
    wrong = [f'+{k}' for k in r.sample([k for k in range(2, 8) if k != n], 3)]
    return mcq(f'What is the oxidation state of {el} in {c}?', f'+{n}', wrong, f'Sum of oxidation numbers = 0 ⇒ {el} = +{n} in {c}.', r)


LN = ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
LN_NAME = ['lanthanum', 'cerium', 'praseodymium', 'neodymium', 'promethium', 'samarium', 'europium', 'gadolinium', 'terbium',
           'dysprosium', 'holmium', 'erbium', 'thulium', 'ytterbium', 'lutetium']


def ln3(r):
    i = r.randrange(15)
    Z = 57 + i
    f = i
    u = f if f <= 7 else 14 - f
    return {'stem': f'Write the electronic configuration of {LN[i]}³⁺ ({LN_NAME[i]}, Z = {Z}) and state the number of unpaired electrons.',
            'answer': f'[Xe] 4f{sup(f)}; {u} unpaired' if f else '[Xe]; 0 unpaired',
            'key': f'Ln³⁺ ions have the configuration [Xe] 4f{sup(f)} (Z − 57 = {f} f electrons) (1); unpaired electrons = {u} (1).',
            'distractors': [(f'[Xe] 4f{sup(f + 1)}; {f + 1 if f + 1 <= 7 else 13 - f} unpaired' if f < 14 else '[Xe] 4f¹³; 1 unpaired'), f'[Xe] 4f{sup(max(f - 1, 0))} 5d¹; {u} unpaired',
                            f'[Xe] 4f{sup(f)} 6s²; {u} unpaired']}


def ln_neutral(r):
    i = r.randrange(15)
    Z = 57 + i
    if LN[i] in ('La',):
        good = '[Xe] 5d¹ 6s²'
    elif LN[i] in ('Ce', 'Gd', 'Lu'):
        good = f'[Xe] 4f{sup(i)} 5d¹ 6s²'
    else:
        good = f'[Xe] 4f{sup(i + 1)} 6s²'
    wrong = {f'[Xe] 4f{sup(i)} 5d¹ 6s²' if i else '[Xe] 4f¹ 6s²', f'[Xe] 4f{sup(i + 1)} 6s²' if i < 14 else '[Xe] 4f¹³ 5d¹ 6s²',
             f'[Xe] 4f{sup(i + 2)} 6s¹' if i < 13 else '[Xe] 4f¹⁴ 6s¹', f'[Xe] 4f{sup(max(i - 1, 0))} 5d² 6s²'}
    wrong.discard(good)
    return mcq(f'What is the electronic configuration of {LN_NAME[i]} (Z = {Z})?', good, sorted(wrong)[:3],
               f'{cap(LN_NAME[i])}: {good}. La, Ce, Gd and Lu keep one 5d electron; the others are [Xe] 4fⁿ 6s².', r)


CH4S1 = {
    'topic': 'position and electronic configuration of transition elements',
    'terms': [('transition elements', 'elements that have incompletely filled d orbitals in the ground state or in any of their common oxidation states'),
              ('the d-block', 'the part of the periodic table (groups 3–12) in which the d orbitals are progressively filled'),
              ('inner transition elements', 'the f-block elements, in which the 4f or 5f orbitals are progressively filled'),
              ('the 3d series', 'the first transition series, from scandium (Z = 21) to zinc (Z = 30)'),
              ('the penultimate shell', 'the shell just inside the outermost shell; in d-block elements the (n − 1)d orbitals belong to it')],
    'groups': [('an element of the 3d series', ['Sc', 'Ti', 'Mn', 'Fe', 'Ni']), ('an element of the 4d series', ['Y', 'Zr', 'Mo', 'Pd', 'Ag']),
               ('an element of the 5d series', ['La', 'Hf', 'W', 'Pt', 'Au']), ('a main-group (s- or p-block) element', ['Ca', 'Ga', 'K', 'Sn'])],
    'classify': False,
    'tf': (['Zinc, cadmium and mercury are not regarded as transition elements.', 'Copper is a transition element because Cu²⁺ has a 3d⁹ configuration.',
            'Chromium has the configuration [Ar] 3d⁵ 4s¹.', 'The d-block occupies the middle of the periodic table, between groups 2 and 13.',
            'Silver (4d¹⁰ 5s¹) is a transition element because Ag²⁺ has an incomplete 4d subshell.'],
           [('Zinc is a transition element because it has electrons in the 3d subshell.', 'Zn has 3d¹⁰ in the atom and in Zn²⁺, so it is not a transition element.'),
            ('Copper has the configuration [Ar] 3d⁹ 4s².', 'Copper is [Ar] 3d¹⁰ 4s¹ because a filled 3d subshell is more stable.'),
            ('In transition elements the last electron enters the outermost (ns) shell.', 'The last electron enters the (n − 1)d subshell.'),
            ('Scandium is not a transition element.', 'Sc has the configuration 3d¹ 4s², an incomplete d subshell, so it is a transition element.')]),
    'orders': [('order of atomic number in the 3d series', ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn'], 'Z increases from 21 (Sc) to 30 (Zn) across the series.', '<'),
               ('order of first ionisation enthalpy', ['Ca', 'Sc', 'Cr', 'Zn'], 'Across the series effective nuclear charge increases; Zn (3d¹⁰ 4s²) has a very stable filled configuration.', '<')],
    'ar': [('Zn, Cd and Hg are not regarded as transition metals.', 'Their atoms and common ions have completely filled d orbitals (d¹⁰).', 'a', 'Full d¹⁰ in the ground state and in M²⁺.'),
           ('Chromium has the configuration 3d⁵ 4s¹ and not 3d⁴ 4s².', 'Half-filled and fully filled subshells have extra stability due to exchange energy.', 'a', 'Exchange energy favours 3d⁵.'),
           ('Copper is a transition element.', 'Copper atom has a completely filled 3d subshell.', 'b', 'Cu is a transition element because Cu²⁺ (3d⁹) has an incomplete d subshell; the reason is true but not the explanation.'),
           ('Scandium is a transition element.', 'Sc³⁺ has an incompletely filled 3d subshell.', 'c', 'Sc³⁺ is [Ar] (3d⁰); Sc is a transition element because the atom is 3d¹ 4s².')],
    'fams': [F('C2', 'D2', 'mcq', d_config), F('C3', 'D3', 'mcq', d_count)],
    'qa': [('C4', 'D4', 'explain', 'Silver has a completely filled d subshell (4d¹⁰) in its ground state. How can you say that it is a transition element?',
            'Silver shows the +2 oxidation state (e.g. AgF₂), in which Ag²⁺ has an incomplete 4d⁹ configuration; so it fits the definition.',
            '1 mark: +2 state; 1 mark: incomplete 4d⁹ fits the definition.'),
           ('C4', 'D4', 'explain', 'Why is the energy of 4s orbitals lower than 3d orbitals when they are being filled, while 4s electrons are lost first when transition metals ionise?',
            'In the neutral atom, 4s fills first (n + l rule). Once 3d is occupied, 3d electrons shield 4s and the 3d orbitals become lower in energy, so the outermost 4s electrons are removed first.',
            '1 mark filling order; 1 mark ionisation order explanation.'),
           ('C4', 'D3', 'case', 'Neha studies the configuration of the first transition series.\n(i) Write the configuration of Cr and Cu. (1 mark)\n(ii) Why are they exceptional? (1 mark)\n(iii) Which element of the series is not a transition element, and why? (2 marks)',
            '(i) Cr: [Ar] 3d⁵ 4s¹; Cu: [Ar] 3d¹⁰ 4s¹. (ii) Half-filled and fully filled d subshells are extra stable (exchange energy, symmetry). (iii) Zinc: 3d¹⁰ both in the atom and in Zn²⁺, so no incomplete d subshell.',
            '(i) 1 (ii) 1 (iii) 1 element + 1 reason.', ('case',))],
}

CH4S2 = {
    'topic': 'general properties of transition elements',
    'terms': [('paramagnetism', 'the attraction of a substance by a magnetic field, caused by unpaired electrons'),
              ('diamagnetism', 'the weak repulsion of a substance by a magnetic field, shown when all electrons are paired'),
              ('an interstitial compound', 'a compound formed when small atoms such as H, C or N are trapped in the crystal lattice of a metal'),
              ('an alloy', 'a blend of metals made by mixing the components, often of transition metals with similar atomic radii'),
              ('a d–d transition', 'the promotion of an electron from a lower to a higher energy d orbital by absorption of visible light'),
              ('the spin-only magnetic moment', 'the magnetic moment μ = √(n(n + 2)) BM calculated from the number of unpaired electrons')],
    'groups': [('a coloured ion in aqueous solution', ['Ti³⁺', 'V³⁺', 'Cr³⁺', 'Mn²⁺', 'Fe³⁺', 'Co²⁺', 'Ni²⁺', 'Cu²⁺']),
               ('a colourless ion in aqueous solution', ['Sc³⁺', 'Ti⁴⁺', 'Cu⁺', 'Zn²⁺'])],
    'groups2': [('a transition metal catalyst', ['V₂O₅ in the contact process', 'finely divided Fe in the Haber process', 'Ni in hydrogenation of oils', 'Ziegler catalyst (TiCl₄ + Al(CH₃)₃)']),
                ('an interstitial compound', ['TiC', 'Mn₄N', 'Fe₃H', 'VH₀.₅₆'])],
    'classify': False,
    'tf': (['Mn shows the largest number of oxidation states in the 3d series (+2 to +7).', 'Transition metals have high enthalpies of atomisation due to many unpaired electrons taking part in metallic bonding.',
            'Interstitial compounds are hard, have high melting points and retain metallic conductivity.', 'Zn²⁺ salts are white because Zn²⁺ has a 3d¹⁰ configuration.',
            'The E°(M²⁺/M) value of copper is positive.', 'Transition metals form complexes because of small ion size, high charge and available d orbitals.'],
           [('All transition metal ions are coloured.', 'd⁰ (Sc³⁺, Ti⁴⁺) and d¹⁰ (Cu⁺, Zn²⁺) ions are colourless.'),
            ('Zinc has the highest enthalpy of atomisation in the 3d series.', 'Zinc has the lowest; it has no unpaired d electrons for metallic bonding.'),
            ('The highest oxidation state of a 3d metal is shown in its hydrides.', 'The highest oxidation states are shown in oxides and fluorides (e.g. Mn₂O₇, CrO₃).'),
            ('Fe³⁺ is less stable than Fe²⁺ because it has fewer electrons.', 'Fe³⁺ (3d⁵, half-filled) is more stable than Fe²⁺ (3d⁶).')]),
    'orders': [('order of spin-only magnetic moment', ['Sc³⁺', 'Cu²⁺', 'Ni²⁺', 'Cr³⁺', 'Fe²⁺', 'Mn²⁺'], 'μ increases with the number of unpaired electrons: 0, 1, 2, 3, 4, 5.', '<'),
               ('order of oxidising power of oxoanions', ['VO₂⁺', 'Cr₂O₇²⁻', 'MnO₄⁻'], 'Oxidising power increases V(V) < Cr(VI) < Mn(VII), following increasing stability of the lower species.', '<')],
    'ar': [('Transition metals and their compounds act as good catalysts.', 'They can show variable oxidation states and form complexes.', 'a', 'Variable valency and surface adsorption help catalysis.'),
           ('Cu⁺ is unstable in aqueous solution.', 'The high hydration enthalpy of Cu²⁺ more than compensates for the second ionisation enthalpy of copper.', 'a', 'So 2Cu⁺ → Cu²⁺ + Cu (disproportionation).'),
           ('Mn²⁺ is more stable than Fe²⁺ towards oxidation to the +3 state.', 'Mn²⁺ has a half-filled 3d⁵ configuration.', 'a', 'Removing an electron from 3d⁵ needs extra energy.'),
           ('Zn²⁺ salts are coloured.', 'Zn²⁺ has a completely filled 3d subshell.', 'd', 'Zn²⁺ (3d¹⁰) salts are white; the reason is true.')],
    'features': {'intro': 'A property of transition elements is explained as follows:', 'q': 'Which property is being described', 'what': 'property', 'long': False, 'case': False,
                 'items': [('colour of their compounds', ['partly filled d orbitals', 'd–d transitions absorb visible light', 'complementary colour is seen', 'ligands split the d orbitals']),
                           ('catalytic activity', ['variable oxidation states', 'large surface area for adsorption', 'formation of unstable intermediates', 'used as finely divided iron in the Haber process']),
                           ('formation of interstitial compounds', ['small atoms like H, C, N are trapped in voids', 'compounds are non-stoichiometric', 'very hard with high melting points', 'formed by elements such as Ti and Mn (TiC, Mn₄N)']),
                           ('paramagnetism', ['presence of unpaired electrons', 'attracted into a magnetic field', 'μ = √(n(n + 2)) BM', 'increases from d¹ to d⁵'])]},
    'fams': [F('C3', 'D3', 'numerical', mag_moment), F('C3', 'D3', 'numerical', mag_to_n), F('C2', 'D2', 'mcq', colourless)],
    'qa': [('C4', 'D4', 'explain', 'The E°(M²⁺/M) value for copper is positive (+0.34 V). What is the reason for this?',
            'Copper has a high enthalpy of atomisation and high ionisation enthalpies, which are not balanced by the hydration enthalpy of Cu²⁺; so the overall change is unfavourable and E° is positive.',
            '1 mark: high ΔaH + IE; 1 mark: not compensated by hydration enthalpy.'),
           ('C4', 'D5', 'long', 'Explain giving reasons: (i) transition metals form a large number of complex compounds; (ii) the lowest oxide of a transition metal is basic and the highest is acidic; (iii) transition metals show variable oxidation states; (iv) Cr²⁺ is reducing while Mn³⁺ is oxidising, though both are d⁴; (v) Sc³⁺ is colourless.',
            '(i) Small, highly charged ions with vacant d orbitals of suitable energy. (ii) In higher oxidation states bonding becomes covalent, e.g. MnO basic, Mn₂O₇ acidic. (iii) (n − 1)d and ns electrons have similar energies, so different numbers can be lost. (iv) Cr²⁺ → Cr³⁺ gives stable d³ (half-filled t₂g); Mn³⁺ → Mn²⁺ gives stable d⁵. (v) 3d⁰: no d–d transition.',
            '1 mark each for (i)–(v).')],
}

CH4S3 = {
    'topic': 'potassium dichromate and potassium permanganate',
    'terms': [('chromite ore', 'the ore FeCr₂O₄ from which potassium dichromate is manufactured'),
              ('pyrolusite', 'the ore MnO₂ from which potassium permanganate is manufactured'),
              ('a self-indicator', 'a titrant whose own colour change marks the end point, as KMnO₄ does'),
              ('the chromate–dichromate equilibrium', 'the pH-dependent interconversion 2CrO₄²⁻ + 2H⁺ ⇌ Cr₂O₇²⁻ + H₂O'),
              ('manganate ion', 'the green ion MnO₄²⁻ in which manganese is in the +6 state')],
    'groups': [('a compound of manganese in the +7 state', ['KMnO₄', 'Mn₂O₇', 'NaMnO₄']), ('a compound of chromium in the +6 state', ['K₂Cr₂O₇', 'Na₂CrO₄', 'CrO₃', 'CrO₂Cl₂']),
               ('a compound of manganese in the +6 state', ['K₂MnO₄', 'Na₂MnO₄', 'BaMnO₄'])],
    'classify': False,
    'tf': (['Potassium dichromate is orange and potassium chromate is yellow.', 'In acidic medium MnO₄⁻ gains 5 electrons to form Mn²⁺.',
            'In neutral or faintly alkaline medium MnO₄⁻ is reduced to MnO₂.', 'Acidified K₂Cr₂O₇ turns green when it oxidises SO₂ or H₂S.',
            'The dichromate ion has two tetrahedra sharing one oxygen atom.', 'Manganate ion (MnO₄²⁻) is green and paramagnetic.'],
           [('KMnO₄ is used as a primary standard in volumetric analysis.', 'KMnO₄ is not a primary standard (it decomposes slowly); K₂Cr₂O₇ is used as a primary standard.'),
            ('In acidic medium Cr₂O₇²⁻ is reduced to Cr²⁺.', 'It is reduced to Cr³⁺, gaining 6 electrons per ion.'),
            ('Adding alkali to a dichromate solution turns it orange.', 'Alkali converts dichromate to yellow chromate.'),
            ('The permanganate ion is paramagnetic.', 'MnO₄⁻ (Mn⁺⁷, d⁰) is diamagnetic; its colour is due to charge transfer.')]),
    'orders': [('sequence in the manufacture of K₂Cr₂O₇', ['FeCr₂O₄ (chromite)', 'Na₂CrO₄', 'Na₂Cr₂O₇', 'K₂Cr₂O₇'], 'Fusion with Na₂CO₃ in air, acidification with H₂SO₄, then double decomposition with KCl.', '→'),
               ('sequence in the manufacture of KMnO₄', ['MnO₂ (pyrolusite)', 'K₂MnO₄', 'KMnO₄'], 'Fusion with KOH and an oxidant gives green manganate; electrolytic oxidation or disproportionation in acid gives permanganate.', '→')],
    'ar': [('KMnO₄ does not need an indicator in redox titrations.', 'The purple MnO₄⁻ is reduced to almost colourless Mn²⁺, so the first excess gives a pink colour.', 'a', 'KMnO₄ acts as a self-indicator.'),
           ('Titrations of KMnO₄ are not carried out in the presence of HCl.', 'HCl is oxidised to chlorine by permanganate.', 'a', 'Part of KMnO₄ would be consumed by HCl, giving wrong results.'),
           ('The colour of KMnO₄ is due to d–d transitions.', 'Mn in KMnO₄ is in the +7 state with no d electrons.', 'd', 'The colour is due to ligand-to-metal charge transfer, not d–d transitions.'),
           ('Dichromate solution turns yellow when alkali is added.', 'Dichromate is converted to chromate in alkaline medium.', 'a', 'Cr₂O₇²⁻ + 2OH⁻ → 2CrO₄²⁻ + H₂O.')],
    'features': {'intro': 'An oxidising agent has these properties:', 'q': 'Identify the compound', 'what': 'compound',
                 'items': [('potassium permanganate (KMnO₄)', ['dark purple crystals', 'made from pyrolusite via green K₂MnO₄', 'in acid gains 5 electrons to give Mn²⁺', 'acts as a self-indicator in titrations']),
                           ('potassium dichromate (K₂Cr₂O₇)', ['orange crystals', 'made from chromite ore via Na₂CrO₄', 'in acid gains 6 electrons to give green Cr³⁺', 'used as a primary standard']),
                           ('potassium manganate (K₂MnO₄)', ['green compound', 'Mn in the +6 state', 'disproportionates in acid to MnO₄⁻ and MnO₂', 'paramagnetic with one unpaired electron']),
                           ('potassium chromate (K₂CrO₄)', ['yellow compound', 'stable in alkaline medium', 'turns orange on acidification', 'contains tetrahedral CrO₄²⁻ ions'])]},
    'fams': [F('C3', 'D3', 'numerical', ox_moles), F('C4', 'D4', 'multi_step', ox_titre), F('C2', 'D2', 'mcq', ox_state)],
    'qa': [('C3', 'D3', 'explain', 'Write the ionic equations for the reaction of acidified KMnO₄ with (i) iron(II) ions and (ii) oxalate ions.',
            '(i) MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O. (ii) 2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O.',
            '1 mark each balanced equation.'),
           ('C3', 'D3', 'explain', 'Write the ionic equations for the reaction of acidified K₂Cr₂O₇ with (i) iodide ions and (ii) H₂S.',
            '(i) Cr₂O₇²⁻ + 6I⁻ + 14H⁺ → 2Cr³⁺ + 3I₂ + 7H₂O. (ii) Cr₂O₇²⁻ + 3H₂S + 8H⁺ → 2Cr³⁺ + 3S + 7H₂O.',
            '1 mark each balanced equation.'),
           ('C4', 'D5', 'long', 'Describe the preparation of potassium dichromate from chromite ore. What is the effect of increasing pH on a solution of potassium dichromate? Write the reaction of acidified K₂Cr₂O₇ with Fe²⁺.',
            '4FeCr₂O₄ + 8Na₂CO₃ + 7O₂ → 8Na₂CrO₄ + 2Fe₂O₃ + 8CO₂; 2Na₂CrO₄ + 2H⁺ → Na₂Cr₂O₇ + 2Na⁺ + H₂O; Na₂Cr₂O₇ + 2KCl → K₂Cr₂O₇ + 2NaCl. Increasing pH converts orange dichromate to yellow chromate. Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O.',
            '3 marks preparation; 1 mark pH effect; 1 mark Fe²⁺ equation.')],
}

CH4S4 = {
    'topic': 'lanthanoids and actinoids',
    'terms': [('lanthanoid contraction', 'the steady decrease in atomic and ionic radii from lanthanum to lutetium, due to poor shielding by 4f electrons'),
              ('the lanthanoids', 'the fourteen elements following lanthanum, in which 4f orbitals are filled'),
              ('the actinoids', 'the fourteen elements following actinium, in which 5f orbitals are filled'),
              ('misch metal', 'an alloy of about 95% lanthanoid metal with iron and traces of S, C, Ca and Al, used in lighter flints'),
              ('actinoid contraction', 'the decrease in size from element to element across the actinoids, greater than the lanthanoid contraction')],
    'groups': [('a lanthanoid', ['cerium', 'neodymium', 'europium', 'gadolinium', 'ytterbium']), ('an actinoid', ['thorium', 'uranium', 'neptunium', 'plutonium', 'americium']),
               ('a d-block element', ['zirconium', 'hafnium', 'tungsten', 'platinum'])],
    'classify': False,
    'tf': (['The common oxidation state of lanthanoids is +3.', 'Ce⁴⁺ is a good oxidising agent in aqueous solution.', 'Actinoids show a greater range of oxidation states than lanthanoids.',
            'All actinoids are radioactive.', 'Due to lanthanoid contraction, Zr and Hf have almost identical radii.', 'Eu²⁺ is a strong reducing agent.'],
           [('Lanthanoid contraction is caused by increased shielding by 4f electrons.', 'It is caused by imperfect (poor) shielding by 4f electrons as nuclear charge increases.'),
            ('Lanthanoids show more oxidation states than actinoids.', 'Actinoids show more oxidation states because 5f, 6d and 7s levels are close in energy.'),
            ('The 4f orbitals penetrate further into the core than 5f orbitals.', '5f orbitals extend further (are less buried) than 4f orbitals.'),
            ('Ionic radii of Ln³⁺ ions increase from La³⁺ to Lu³⁺.', 'They decrease steadily from La³⁺ to Lu³⁺ (lanthanoid contraction).')]),
    'orders': [('order of ionic radii', ['La³⁺', 'Ce³⁺', 'Nd³⁺', 'Gd³⁺', 'Yb³⁺', 'Lu³⁺'], 'Lanthanoid contraction: radii decrease steadily with atomic number.', '>'),
               ('order of basic character of hydroxides', ['La(OH)₃', 'Ce(OH)₃', 'Eu(OH)₃', 'Lu(OH)₃'], 'As the size of Ln³⁺ decreases, covalent character increases and basicity decreases.', '>')],
    'ar': [('Zr and Hf have very similar properties.', 'Lanthanoid contraction makes their atomic radii nearly equal.', 'a', 'Similar size ⇒ similar chemistry.'),
           ('Actinoid contraction is greater than lanthanoid contraction.', '5f electrons shield the nuclear charge more poorly than 4f electrons.', 'a', 'Poorer shielding gives a larger contraction from element to element.'),
           ('Ce⁴⁺ is a strong oxidant.', 'Ce⁴⁺ tends to revert to the common +3 state.', 'a', 'E°(Ce⁴⁺/Ce³⁺) = +1.74 V.'),
           ('La³⁺ and Lu³⁺ are coloured.', 'They have 4f⁰ and 4f¹⁴ configurations respectively.', 'd', 'With f⁰ and f¹⁴ no f–f transitions occur; they are colourless.')],
    'features': {'intro': 'A series of elements shows these features:', 'q': 'Which series is described', 'what': 'series', 'case': False,
                 'items': [('the lanthanoids', ['4f orbitals are filled', 'common oxidation state +3', 'mostly non-radioactive (except promethium)', 'oxidation states +2 and +4 only where f⁰, f⁷ or f¹⁴ results']),
                           ('the actinoids', ['5f orbitals are filled', 'oxidation states up to +7', 'all are radioactive', 'many are man-made, with short half-lives']),
                           ('the 3d transition series', ['3d orbitals are filled', 'oxidation states vary widely, up to +7 for Mn', 'many ions are coloured due to d–d transitions', 'includes iron, cobalt and nickel'])]},
    'fams': [F('C3', 'D3', 'numerical', ln3), F('C2', 'D2', 'mcq', ln_neutral)],
    'qa': [('C4', 'D4', 'explain', 'What is lanthanoid contraction? Give two consequences of it.',
            'The steady decrease in atomic and ionic size from La to Lu due to poor shielding by 4f electrons. Consequences: (i) 4d and 5d elements of the same group (Zr/Hf, Nb/Ta) have nearly equal radii; (ii) basicity of Ln(OH)₃ decreases from La to Lu (also difficulty in separating lanthanoids).',
            '1 mark definition with cause; 1 mark two consequences.'),
           ('C4', 'D3', 'case', 'Aditi compares the chemistry of the lanthanoids and actinoids for a project.\n(i) Which series shows the wider range of oxidation states? (1 mark)\n(ii) Give one reason for your answer. (1 mark)\n(iii) Why is the separation of lanthanoids difficult, and give one use of a lanthanoid alloy. (2 marks)',
            '(i) Actinoids. (ii) 5f, 6d and 7s orbitals are comparable in energy. (iii) Lanthanoid contraction gives very similar sizes and chemistry; misch metal is used in lighter flints and Mg-based alloys for bullets and shells.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Compare the lanthanoids and actinoids with respect to (i) electronic configuration, (ii) oxidation states, (iii) atomic and ionic sizes, (iv) radioactivity and (v) chemical reactivity.',
            '(i) Ln: [Xe] 4f¹⁻¹⁴ 5d⁰⁻¹ 6s²; An: [Rn] 5f¹⁻¹⁴ 6d⁰⁻¹ 7s². (ii) Ln mainly +3; An +3 to +7. (iii) Both contract; actinoid contraction is larger. (iv) Ln non-radioactive except Pm; all An are radioactive. (v) Actinoids are more reactive, especially when finely divided.',
            '1 mark each for (i)–(v).')],
}

# ---------------------------------------------------------------- unit 5: coordination compounds

WERNER = [('CoCl₃·6NH₃', '[Co(NH₃)₆]Cl₃', 4, 3, 'yellow'), ('CoCl₃·5NH₃', '[CoCl(NH₃)₅]Cl₂', 3, 2, 'purple'),
          ('CoCl₃·4NH₃', '[CoCl₂(NH₃)₄]Cl', 2, 1, 'green or violet'), ('CrCl₃·6H₂O (violet)', '[Cr(H₂O)₆]Cl₃', 4, 3, 'violet'),
          ('CrCl₃·6H₂O (light green)', '[CrCl(H₂O)₅]Cl₂·H₂O', 3, 2, 'light green'), ('CrCl₃·6H₂O (dark green)', '[CrCl₂(H₂O)₄]Cl·2H₂O', 2, 1, 'dark green'),
          ('PtCl₄·6NH₃', '[Pt(NH₃)₆]Cl₄', 5, 4, 'white'), ('PtCl₄·4NH₃', '[PtCl₂(NH₃)₄]Cl₂', 3, 2, 'white'), ('PtCl₄·2NH₃', '[PtCl₄(NH₃)₂]', 0, 0, 'white')]


def werner_agcl(r):
    f, cx, ions, agcl, _ = r.choice(WERNER)
    n = r.choice([0.01, 0.02, 0.05, 0.1])
    mol = n * agcl
    who = name(r)
    return {'stem': f'{who} treats {n} mol of {f} with excess AgNO₃ solution. Taking its structure as {cx}, how many moles of AgCl are precipitated, and what mass is this? (Molar mass of AgCl = 143.5 g mol⁻¹)',
            'answer': f'{num(mol, 3)} mol; {sf(mol * 143.5, 3) if mol else "0"} g',
            'key': f'Only Cl⁻ outside the coordination sphere is precipitated: {agcl} per formula unit (1); {n} × {agcl} = {num(mol, 3)} mol; mass = {num(mol, 3)} × 143.5 = {sf(mol * 143.5, 3) if mol else "0"} g (1).',
            'distractors': [f'{num(n * (agcl + 1), 3)} mol; {sf(n * (agcl + 1) * 143.5, 3)} g', f'{num(n * (agcl + 2), 3)} mol; {sf(n * (agcl + 2) * 143.5, 3)} g',
                            f'{num(n * (agcl - 1), 3) if agcl > 1 else num(n * 2, 3)} mol; {sf(n * (agcl - 1 if agcl > 1 else 2) * 143.5, 3)} g']}


def werner_ions(r):
    f, cx, ions, agcl, _ = r.choice(WERNER)
    wrong = [str(k) for k in r.sample([k for k in range(0, 6) if k != ions], 3)]
    return mcq(f'How many ions are produced per formula unit when {cx} dissolves in water?', str(ions), wrong,
               f'{cx}: the complex ion stays intact and {agcl} Cl⁻ ion(s) are released ⇒ {ions} ions in total.' if ions else f'{cx} is a non-electrolyte; it gives no ions.', r)


# (formula, name, metal, oxidation state, coordination number, ligand note)
CX = [('[Co(NH₃)₆]Cl₃', 'hexaamminecobalt(III) chloride', 'Co', 3, 6), ('[CoCl(NH₃)₅]Cl₂', 'pentaamminechloridocobalt(III) chloride', 'Co', 3, 6),
      ('K₃[Fe(CN)₆]', 'potassium hexacyanidoferrate(III)', 'Fe', 3, 6), ('K₄[Fe(CN)₆]', 'potassium hexacyanidoferrate(II)', 'Fe', 2, 6),
      ('[PtCl₂(NH₃)₂]', 'diamminedichloridoplatinum(II)', 'Pt', 2, 4), ('[Ni(CO)₄]', 'tetracarbonylnickel(0)', 'Ni', 0, 4),
      ('K₂[Zn(OH)₄]', 'potassium tetrahydroxidozincate(II)', 'Zn', 2, 4), ('[Cr(H₂O)₆]Cl₃', 'hexaaquachromium(III) chloride', 'Cr', 3, 6),
      ('[Co(en)₃]Cl₃', 'tris(ethane-1,2-diamine)cobalt(III) chloride', 'Co', 3, 6), ('K₃[Al(C₂O₄)₃]', 'potassium trioxalatoaluminate(III)', 'Al', 3, 6),
      ('[Cu(NH₃)₄]SO₄', 'tetraamminecopper(II) sulphate', 'Cu', 2, 4), ('[CoCl₂(en)₂]Cl', 'dichloridobis(ethane-1,2-diamine)cobalt(III) chloride', 'Co', 3, 6),
      ('K₂[PdCl₄]', 'potassium tetrachloridopalladate(II)', 'Pd', 2, 4), ('[Ag(NH₃)₂]Cl', 'diamminesilver(I) chloride', 'Ag', 1, 2),
      ('[CoCl(NH₃)₄(H₂O)]Cl₂', 'tetraammineaquachloridocobalt(III) chloride', 'Co', 3, 6), ('K₂[Ni(CN)₄]', 'potassium tetracyanidonickelate(II)', 'Ni', 2, 4),
      ('[Fe(C₂O₄)₃]³⁻', 'trioxalatoferrate(III) ion', 'Fe', 3, 6), ('[Mn(H₂O)₆]²⁺', 'hexaaquamanganese(II) ion', 'Mn', 2, 6),
      ('[Pt(NH₃)₄][PtCl₄]', 'tetraammineplatinum(II) tetrachloridoplatinate(II)', 'Pt', 2, 4), ('Na₃[Co(NO₂)₆]', 'sodium hexanitrito-N-cobaltate(III)', 'Co', 3, 6)]


def _bad_names(nm, ox):
    out = set()
    rn = ROMAN[ox]
    for k in (ox - 1, ox + 1, ox + 2):
        if 0 <= k <= 7 and k != ox:
            out.add(nm.replace(f'({rn})', f'({ROMAN[k]})', 1))
    if 'ate(' in nm:
        out.add(nm.replace('ate(', '(', 1).replace('ferr(', 'iron(').replace('cobalt(', 'cobalt(').replace('zinc(', 'zinc(').replace('nickel(', 'nickel(').replace('pallad(', 'palladium(').replace('platin(', 'platinum(').replace('alumin(', 'aluminium('))
    else:
        for m in ('cobalt(', 'chromium(', 'copper(', 'platinum(', 'silver(', 'nickel(', 'manganese('):
            if m in nm:
                out.add(nm.replace(m, m[:-1] + 'ate(', 1))
                break
    for a, b in (('chlorido', 'chloro'), ('cyanido', 'cyano'), ('ammine', 'amine'), ('hydroxido', 'hydroxo'), ('aqua', 'hydrato'), ('ethane-1,2-diamine', 'ethylene')):
        if a in nm:
            out.add(nm.replace(a, b))
    out.discard(nm)
    return sorted(out)


def cx_name(r):
    f, nm, m, ox, cn = r.choice(CX)
    bad = _bad_names(nm, ox)
    if len(bad) < 3:
        raise ValueError('few names')
    return mcq(f'What is the IUPAC name of {f}?', nm, r.sample(bad, 3),
               f'{f}: ligands in alphabetical order, then metal with oxidation state {ROMAN[ox]}' + (' and “-ate” for an anionic complex.' if 'ate(' in nm else '.'), r)


def cx_formula(r):
    f, nm, m, ox, cn = r.choice(CX)
    others = [x[0] for x in CX if x[2] == m and x[0] != f] + [x[0] for x in r.sample(CX, 4) if x[0] != f]
    wrong = list(dict.fromkeys(others))[:3]
    return mcq(f'Which formula corresponds to {nm}?', f, wrong, f'{nm} = {f}.', r)


def cx_ox_cn(r):
    f, nm, m, ox, cn = r.choice(CX)
    return {'stem': f'Find the oxidation state and the coordination number of the central metal atom in {f}. Also write its IUPAC name.',
            'answer': f'{m}: oxidation state {"+" if ox else ""}{ox}; coordination number {cn}; {nm}',
            'key': f'Balance ligand and counter-ion charges ⇒ {m} = {"+" if ox else ""}{ox} (1); coordination number = number of donor atoms = {cn} (½); name: {nm} (½).',
            'distractors': [f'{m}: oxidation state +{ox + 1}; coordination number {cn}', f'{m}: oxidation state {"+" if ox else ""}{ox}; coordination number {cn // 2 if cn > 2 else 4}', f'{m}: oxidation state +{cn}; coordination number {cn}' if cn != ox else f'{m}: oxidation state +{ox + 2}; coordination number {cn}']}


ISOM = [('[Co(NH₃)₅(NO₂)]Cl₂ and [Co(NH₃)₅(ONO)]Cl₂', 'linkage isomerism', 'the ambidentate NO₂⁻ binds through N in one and through O in the other'),
        ('[Co(NH₃)₅(SO₄)]Br and [Co(NH₃)₅Br]SO₄', 'ionisation isomerism', 'the counter ion and a ligand exchange places'),
        ('[Co(NH₃)₆][Cr(CN)₆] and [Cr(NH₃)₆][Co(CN)₆]', 'coordination isomerism', 'ligands are interchanged between cationic and anionic complex entities'),
        ('[Cr(H₂O)₆]Cl₃ and [CrCl(H₂O)₅]Cl₂·H₂O', 'solvate (hydrate) isomerism', 'water is inside the coordination sphere in one and outside as water of crystallisation in the other'),
        ('cis- and trans-[PtCl₂(NH₃)₂]', 'geometrical isomerism', 'the same ligands are adjacent (cis) or opposite (trans) in a square planar complex'),
        ('fac- and mer-[Co(NH₃)₃(NO₂)₃]', 'geometrical isomerism', 'three identical ligands occupy one face or a meridian of the octahedron'),
        ('d- and l-[Co(en)₃]³⁺', 'optical isomerism', 'the two forms are non-superimposable mirror images'),
        ('[Co(NH₃)₅(SCN)]²⁺ and [Co(NH₃)₅(NCS)]²⁺', 'linkage isomerism', 'thiocyanate binds through S in one and through N in the other'),
        ('[Pt(NH₃)₄][PtCl₄] and [PtCl(NH₃)₃][PtCl₃(NH₃)]', 'coordination isomerism', 'ligands are distributed differently between cation and anion')]
ISO_TYPES = ['linkage isomerism', 'ionisation isomerism', 'coordination isomerism', 'solvate (hydrate) isomerism', 'geometrical isomerism', 'optical isomerism']


def iso_type(r):
    pair, t, why = r.choice(ISOM)
    return mcq(f'What type of isomerism is shown by {pair}?', t, r.sample([x for x in ISO_TYPES if x != t], 3), f'{cap(t)}: {why}.', r)


GEOM = [('[PtCl₂(NH₃)₂]', 'square planar MA₂B₂', 2, 'cis and trans; no optical isomers'),
        ('[CoCl₂(NH₃)₄]⁺', 'octahedral MA₄B₂', 2, 'cis and trans; no optical isomers'),
        ('[Co(NH₃)₃(NO₂)₃]', 'octahedral MA₃B₃', 2, 'fac and mer; no optical isomers'),
        ('[Co(en)₃]³⁺', 'octahedral M(AA)₃', 2, 'a pair of enantiomers (d and l); no geometrical isomers'),
        ('[CoCl₂(en)₂]⁺', 'octahedral M(AA)₂B₂', 3, 'trans (optically inactive) and a pair of cis enantiomers'),
        ('[Cr(C₂O₄)₃]³⁻', 'octahedral M(AA)₃', 2, 'a pair of enantiomers'),
        ('[NiCl₄]²⁻', 'tetrahedral MA₄', 1, 'no geometrical or optical isomers'),
        ('[PtCl(Br)(NH₃)(py)]', 'square planar MABXL', 3, 'three geometrical isomers'),
        ('[Co(NH₃)₆]³⁺', 'octahedral MA₆', 1, 'no stereoisomers')]


def stereo_count(r):
    cx, t, n, why = r.choice(GEOM)
    wrong = [str(k) for k in r.sample([k for k in range(1, 6) if k != n], 3)]
    return mcq(f'How many stereoisomers are possible for {cx} ({t})?', str(n), wrong, f'{cx}: {why} ⇒ {n}.', r)


# (complex, d count, hybridisation, geometry, unpaired, inner/outer)
VBT = [('[Co(NH₃)₆]³⁺', 6, 'd²sp³', 'octahedral', 0, 'inner orbital (low spin)'), ('[CoF₆]³⁻', 6, 'sp³d²', 'octahedral', 4, 'outer orbital (high spin)'),
       ('[Fe(CN)₆]³⁻', 5, 'd²sp³', 'octahedral', 1, 'inner orbital (low spin)'), ('[Fe(CN)₆]⁴⁻', 6, 'd²sp³', 'octahedral', 0, 'inner orbital (low spin)'),
       ('[FeF₆]³⁻', 5, 'sp³d²', 'octahedral', 5, 'outer orbital (high spin)'), ('[Ni(CN)₄]²⁻', 8, 'dsp²', 'square planar', 0, 'inner orbital'),
       ('[NiCl₄]²⁻', 8, 'sp³', 'tetrahedral', 2, 'outer orbital'), ('[Ni(CO)₄]', 10, 'sp³', 'tetrahedral', 0, 'outer orbital'),
       ('[Mn(CN)₆]³⁻', 4, 'd²sp³', 'octahedral', 2, 'inner orbital (low spin)'), ('[Cr(NH₃)₆]³⁺', 3, 'd²sp³', 'octahedral', 3, 'inner orbital'),
       ('[CoCl₄]²⁻', 7, 'sp³', 'tetrahedral', 3, 'outer orbital'), ('[Fe(H₂O)₆]²⁺', 6, 'sp³d²', 'octahedral', 4, 'outer orbital (high spin)'),
       ('[Zn(NH₃)₄]²⁺', 10, 'sp³', 'tetrahedral', 0, 'outer orbital')]
HYB = ['d²sp³', 'sp³d²', 'dsp²', 'sp³']


def vbt(r):
    cx, d, h, g, u, io = r.choice(VBT)
    mag = 'diamagnetic' if u == 0 else f'paramagnetic, {u} unpaired electron{"s" if u > 1 else ""}'
    return {'stem': f'Using valence bond theory, predict the hybridisation, shape and magnetic behaviour of {cx}.',
            'answer': f'{h}; {g}; {mag}',
            'key': f'Metal ion is d{sup(d)} (½); {h} hybridisation, {g}, {io} (1); {mag}, μ = {bm(u):.2f} BM (½).' if u else f'Metal ion is d{sup(d)} (½); {h} hybridisation, {g}, {io} (1); all electrons paired ⇒ diamagnetic (½).',
            'distractors': [f'{r.choice([x for x in HYB if x != h])}; {g}; {mag}', f'{h}; {g}; {"paramagnetic, 2 unpaired electrons" if u == 0 else "diamagnetic"}',
                            f'{"sp³" if h != "sp³" else "dsp²"}; {"tetrahedral" if g != "tetrahedral" else "square planar"}; {mag}']}


def hyb_mcq(r):
    cx, d, h, g, u, io = r.choice(VBT)
    return mcq(f'What is the hybridisation of the central metal ion in {cx}?', h, [x for x in HYB if x != h], f'{cx}: d{sup(d)}, {h}, {g}, {u} unpaired electron(s).', r)


def cft(r):
    d = r.choice([4, 5, 6, 7])
    strong = r.random() < 0.5
    if strong:
        t = min(d, 6)
        e = d - t
    else:
        t = min(d, 3) + max(0, d - 5)
        e = d - t
    u = (t if t <= 3 else 6 - t) + (e if e <= 2 else 4 - e)
    cfse = -0.4 * t + 0.6 * e
    cond = 'Δo > P (strong field ligand)' if strong else 'Δo < P (weak field ligand)'
    return {'stem': f'Write the configuration of a d{sup(d)} ion in an octahedral crystal field when {cond}. Give the number of unpaired electrons and the CFSE in terms of Δo (ignore pairing energy).',
            'answer': f't₂g{sup(t)} e_g{sup(e)}; {u} unpaired; CFSE = {cfse:+.1f} Δo'.replace('+', '+').replace('-', '−'),
            'key': f'With {cond}, electrons {"pair in t₂g before entering e_g" if strong else "occupy e_g before pairing"} ⇒ t₂g{sup(t)} e_g{sup(e)} (1); unpaired = {u}; CFSE = (−0.4 × {t} + 0.6 × {e}) Δo = {cfse:+.1f} Δo (1).'.replace('-0', '−0').replace('+-', '−'),
            'distractors': _cft_wrong(d, strong, t, e, u)}


def _cft_wrong(d, strong, t, e, u):
    t2 = min(d, 3) + max(0, d - 5) if strong else min(d, 6)
    e2 = d - t2
    u2 = (t2 if t2 <= 3 else 6 - t2) + (e2 if e2 <= 2 else 4 - e2)
    c2 = -0.4 * t2 + 0.6 * e2
    c1 = -0.4 * t + 0.6 * e
    return [f't₂g{sup(t2)} e_g{sup(e2)}; {u2} unpaired; CFSE = {c2:+.1f} Δo'.replace('-', '−'),
            f't₂g{sup(t)} e_g{sup(e)}; {u + 2 if u < 4 else u - 2} unpaired; CFSE = {c1:+.1f} Δo'.replace('-', '−'),
            f't₂g{sup(t)} e_g{sup(e)}; {u} unpaired; CFSE = {-c1 if c1 else -0.4:+.1f} Δo'.replace('-', '−')]


CH5S1 = {
    'topic': "Werner's theory and key terms",
    'terms': [('a ligand', 'an ion or molecule bound to the central atom or ion in a coordination entity'),
              ('the coordination number', 'the number of ligand donor atoms directly bonded to the central metal atom or ion'),
              ('the coordination sphere', 'the central atom with the ligands attached to it, written within square brackets'),
              ('a chelate ligand', 'a di- or polydentate ligand that binds the same metal ion through two or more donor atoms forming a ring'),
              ('an ambidentate ligand', 'a ligand that can bind through two different donor atoms, such as NO₂⁻ or SCN⁻'),
              ('a homoleptic complex', 'a complex in which the metal is bound to only one kind of donor group, e.g. [Co(NH₃)₆]³⁺'),
              ('a heteroleptic complex', 'a complex in which the metal is bound to more than one kind of donor group, e.g. [Co(NH₃)₄Cl₂]⁺'),
              ('denticity', 'the number of donor atoms in a ligand that bind to the metal')],
    'groups': [('a unidentate ligand', ['NH₃', 'H₂O', 'Cl⁻', 'CN⁻', 'CO']), ('a didentate ligand', ['ethane-1,2-diamine (en)', 'oxalate (C₂O₄²⁻)', 'glycinate']),
               ('an ambidentate ligand', ['NO₂⁻', 'SCN⁻', 'CN⁻ (as cyanido/isocyanido)']), ('a hexadentate ligand', ['EDTA⁴⁻'])],
    'tf': (['In Werner\'s theory the primary valence is ionisable and corresponds to the oxidation state.', 'The secondary valence is non-ionisable and equals the coordination number.',
            'A double salt such as Mohr\'s salt dissociates completely into simple ions in water.', 'EDTA⁴⁻ is a hexadentate ligand.', 'Chelate complexes are more stable than similar complexes with unidentate ligands.'],
           [('Complex ions dissociate completely into simple ions in water, like double salts.', 'Complex ions retain their identity; double salts dissociate completely.'),
            ('The secondary valence of a metal is satisfied only by negative ions.', 'Secondary valences can be satisfied by neutral molecules or negative ions.'),
            ('Ethane-1,2-diamine is a unidentate ligand.', 'It is didentate, binding through two nitrogen atoms.'),
            ('In [Co(NH₃)₅Cl]Cl₂ all three chloride ions are precipitated by AgNO₃.', 'Only the two ionisable Cl⁻ outside the sphere are precipitated.')]),
    'ar': [('[Co(NH₃)₆]Cl₃ gives three moles of AgCl with excess AgNO₃.', 'All three chloride ions are outside the coordination sphere.', 'a', 'Ionisable Cl⁻ precipitate as AgCl.'),
           ('Mohr\'s salt gives the test for Fe²⁺ ions.', 'It is a double salt that dissociates completely in water.', 'a', 'Its ions are free in solution.'),
           ('K₄[Fe(CN)₆] gives the test for Fe²⁺ ions.', '[Fe(CN)₆]⁴⁻ is a stable complex ion.', 'd', 'K₄[Fe(CN)₆] does not give Fe²⁺ tests because the complex does not dissociate; the reason is true.')],
    'fams': [F('C3', 'D3', 'numerical', werner_agcl), F('C2', 'D2', 'mcq', werner_ions)],
    'qa': [('C4', 'D4', 'explain', 'On treatment with excess AgNO₃, 1 mol each of CoCl₃·6NH₃, CoCl₃·5NH₃ and CoCl₃·4NH₃ gives 3, 2 and 1 mol of AgCl respectively. Write their structural formulae and state the number of ions each gives in solution.',
            '[Co(NH₃)₆]Cl₃ (4 ions), [CoCl(NH₃)₅]Cl₂ (3 ions), [CoCl₂(NH₃)₄]Cl (2 ions).',
            '1 mark formulae; 1 mark ion count.'),
           ('C4', 'D3', 'case', 'Rohit dissolves three green-violet chromium(III) chloride hydrates, all of formula CrCl₃·6H₂O, in water and adds excess AgNO₃. One mole of each gives 3, 2 and 1 mol of AgCl.\n(i) Write the formulae of the three complexes. (2 marks)\n(ii) What type of isomerism do they show? (1 mark)\n(iii) Which has the highest molar conductivity? (1 mark)',
            '(i) [Cr(H₂O)₆]Cl₃, [CrCl(H₂O)₅]Cl₂·H₂O, [CrCl₂(H₂O)₄]Cl·2H₂O. (ii) Solvate (hydrate) isomerism. (iii) [Cr(H₂O)₆]Cl₃, which gives 4 ions.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'State the postulates of Werner\'s theory of coordination compounds. Explain the difference between a double salt and a complex with examples. Define coordination number and coordination sphere.',
            'Metals show primary (ionisable, oxidation state) and secondary (non-ionisable, coordination number) valences; secondary valences are satisfied by ligands and are directed to fixed positions giving definite geometry. Double salt (e.g. Mohr\'s salt, FeSO₄·(NH₄)₂SO₄·6H₂O) dissociates fully into simple ions; a complex (e.g. K₄[Fe(CN)₆]) keeps the complex ion intact. Coordination number: number of donor atoms bonded to the metal; coordination sphere: metal plus ligands in square brackets.',
            '2 marks postulates; 2 marks double salt vs complex; 1 mark definitions.')],
}

CH5S2 = {
    'topic': 'IUPAC nomenclature of coordination compounds',
    'terms': [('the -ate suffix', 'the ending added to the name of the metal when the complex is an anion'),
              ('a bridging ligand', 'a ligand that links two metal atoms in a polynuclear complex'),
              ('ammine', 'the name of NH₃ as a ligand'), ('aqua', 'the name of H₂O as a ligand'),
              ('bis-, tris-', 'prefixes used for the number of ligands when the ligand name already contains a numerical prefix')],
    'tf': (['In naming, the cation is named before the anion.', 'Ligands are named in alphabetical order, ignoring numerical prefixes.', 'The oxidation state of the metal is written in Roman numerals in brackets.',
            'For anionic complexes, iron is called ferrate.', 'Negative ligands end in -ido, e.g. chlorido, cyanido.'],
           [('Ligands are named after the metal.', 'Ligands are named first, in alphabetical order, then the metal.'),
            ('The name of [Ni(CO)₄] is tetracarbonylnickelate(0).', 'It is a neutral complex: tetracarbonylnickel(0).'),
            ('In formulae, the metal is written after the ligands.', 'In formulae the central atom is written first, then the ligands, all within square brackets.'),
            ('NH₃ as a ligand is called amine.', 'It is called ammine.')]),
    'ar': [('The name of K₄[Fe(CN)₆] ends in “ferrate(II)”.', 'For complex anions the metal name ends in -ate and the Latin name is used for iron.', 'a', 'Anionic complex ⇒ ferrate.'),
           ('[Co(en)₃]Cl₃ is named tris(ethane-1,2-diamine)cobalt(III) chloride.', 'The ligand name ethane-1,2-diamine already contains a numerical prefix.', 'a', 'So tris is used instead of tri.')],
    'fams': [F('C2', 'D2', 'mcq', cx_name), F('C2', 'D2', 'mcq', cx_formula), F('C3', 'D3', 'explain', cx_ox_cn)],
    'qa': [('C1', 'D2', 'short', 'Write the IUPAC name of [Co(NH₃)₆]Cl₃.', 'Hexaamminecobalt(III) chloride.', '1 mark.'),
           ('C1', 'D2', 'short', 'Write the formula of potassium tetracyanidonickelate(II).', 'K₂[Ni(CN)₄].', '1 mark.'),
           ('C4', 'D4', 'explain', 'Write the formulae of (i) tetraamminediaquacobalt(III) chloride and (ii) potassium tetrachloridonickelate(II), and state the coordination number of the metal in each.',
            '(i) [Co(NH₃)₄(H₂O)₂]Cl₃, CN = 6. (ii) K₂[NiCl₄], CN = 4.', '1 mark each.'),
           ('C4', 'D5', 'long', 'Write IUPAC names of (i) [Pt(NH₃)₂Cl(NO₂)], (ii) K₃[Cr(C₂O₄)₃], (iii) [CoCl₂(en)₂]Cl, (iv) [Co(NH₃)₅(CO₃)]Cl and (v) Hg[Co(SCN)₄].',
            '(i) diamminechloridonitrito-N-platinum(II); (ii) potassium trioxalatochromate(III); (iii) dichloridobis(ethane-1,2-diamine)cobalt(III) chloride; (iv) pentaamminecarbonatocobalt(III) chloride; (v) mercury(II) tetrathiocyanato-S-cobaltate(II).',
            '1 mark each.')],
}

CH5S3 = {
    'topic': 'isomerism in coordination compounds',
    'terms': [('linkage isomerism', 'isomerism arising from an ambidentate ligand binding through different donor atoms'),
              ('ionisation isomerism', 'isomerism in which a ligand inside the sphere and a counter ion outside exchange places'),
              ('coordination isomerism', 'isomerism due to interchange of ligands between cationic and anionic complex entities'),
              ('solvate isomerism', 'isomerism in which a solvent molecule is a ligand in one isomer and free solvent of crystallisation in another'),
              ('geometrical isomerism', 'stereoisomerism from different arrangements of ligands around the metal (cis/trans, fac/mer)'),
              ('optical isomerism', 'stereoisomerism in which isomers are non-superimposable mirror images')],
    'groups': [('a structural isomerism', ['linkage', 'ionisation', 'coordination', 'solvate']), ('a stereoisomerism', ['geometrical (cis–trans)', 'facial–meridional', 'optical'])],
    'classify': False,
    'tf': (['Tetrahedral complexes do not show geometrical isomerism.', 'Square planar MA₂B₂ complexes show cis–trans isomerism.', '[Co(en)₃]³⁺ is optically active.',
            'trans-[CoCl₂(en)₂]⁺ is optically inactive.', 'Linkage isomerism needs an ambidentate ligand.'],
           [('Tetrahedral MA₂B₂ complexes show geometrical isomerism.', 'In a tetrahedron all positions are adjacent, so no cis–trans isomers form.'),
            ('cis-[CoCl₂(en)₂]⁺ is optically inactive.', 'The cis isomer has no plane of symmetry and is optically active; the trans isomer is inactive.'),
            ('[Co(NH₃)₅Br]SO₄ and [Co(NH₃)₅(SO₄)]Br are linkage isomers.', 'They are ionisation isomers.'),
            ('Optical isomers differ in their melting points.', 'Enantiomers have identical physical properties except the direction of rotation of plane-polarised light.')]),
    'ar': [('[Co(NH₃)₅(NO₂)]²⁺ and [Co(NH₃)₅(ONO)]²⁺ are linkage isomers.', 'NO₂⁻ is an ambidentate ligand.', 'a', 'It can bind through N or O.'),
           ('[NiCl₄]²⁻ does not show geometrical isomerism.', 'It has a tetrahedral geometry.', 'a', 'Tetrahedral complexes cannot have cis/trans arrangement.'),
           ('trans-[CoCl₂(en)₂]⁺ is optically active.', 'It has a plane of symmetry.', 'd', 'Having a mirror plane, the trans form is optically inactive.')],
    'fams': [F('C3', 'D3', 'mcq', iso_type), F('C3', 'D3', 'mcq', stereo_count)],
    'qa': [('C4', 'D4', 'explain', 'Draw the structures of the geometrical isomers of [Co(NH₃)₃(NO₂)₃] and name them.',
            'Facial (fac): the three NO₂ groups occupy one triangular face of the octahedron. Meridional (mer): the three NO₂ groups lie in a plane containing the metal (a meridian).',
            '1 mark each correctly described isomer.'),
           ('C4', 'D4', 'explain', 'Draw the structures of the optical isomers of [Cr(C₂O₄)₃]³⁻ and explain why they are optically active.',
            'Two non-superimposable mirror-image forms (d and l) with the three oxalate rings arranged like a propeller; no plane or centre of symmetry, so each rotates plane-polarised light.',
            '1 mark structures; 1 mark reason.'),
           ('C4', 'D3', 'case', 'Priya is given two complexes of the same formula: [Co(NH₃)₅(SO₄)]Br (red-violet) and [Co(NH₃)₅Br]SO₄ (red).\n(i) Name the isomerism. (1 mark)\n(ii) How would you distinguish them using BaCl₂ and AgNO₃? (2 marks)\n(iii) Give one more example of the same type. (1 mark)',
            '(i) Ionisation isomerism. (ii) [Co(NH₃)₅Br]SO₄ gives a white BaSO₄ precipitate with BaCl₂; [Co(NH₃)₅(SO₄)]Br gives a pale yellow AgBr precipitate with AgNO₃. (iii) [Co(NH₃)₅Cl]NO₂ and [Co(NH₃)₅(NO₂)]Cl (or similar).',
            '(i) 1 (ii) 2 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain with one example each: (i) linkage, (ii) ionisation, (iii) coordination, (iv) geometrical and (v) optical isomerism in coordination compounds.',
            '(i) [Co(NH₃)₅(NO₂)]²⁺ / [Co(NH₃)₅(ONO)]²⁺. (ii) [Co(NH₃)₅(SO₄)]Br / [Co(NH₃)₅Br]SO₄. (iii) [Co(NH₃)₆][Cr(CN)₆] / [Cr(NH₃)₆][Co(CN)₆]. (iv) cis- and trans-[PtCl₂(NH₃)₂]. (v) d- and l-[Co(en)₃]³⁺.',
            '1 mark each with a correct example.')],
}

CH5S4 = {
    'topic': 'bonding in coordination compounds',
    'terms': [('crystal field splitting', 'the separation of the five degenerate d orbitals into sets of different energy caused by the ligand field'),
              ('the spectrochemical series', 'the arrangement of ligands in order of increasing field strength (Δo)'),
              ('an inner orbital complex', 'a complex in which (n − 1)d orbitals take part in hybridisation, e.g. d²sp³'),
              ('an outer orbital complex', 'a complex in which outer nd orbitals take part in hybridisation, e.g. sp³d²'),
              ('the crystal field stabilisation energy', 'the energy by which the d electrons are stabilised by splitting, e.g. −0.4Δo per t₂g electron'),
              ('a strong field ligand', 'a ligand that produces a large splitting so that Δo > P and electrons pair in t₂g')],
    'tf': (['In an octahedral field the e_g orbitals are higher in energy than the t₂g orbitals.', 'Δt is about 4/9 of Δo for the same metal and ligands.',
            'CN⁻ is a stronger field ligand than F⁻.', '[Ni(CN)₄]²⁻ is square planar and diamagnetic.', 'Tetrahedral complexes are generally high spin.'],
           [('In an octahedral field the t₂g set is raised above the e_g set.', 'The e_g set (pointing at ligands) is raised; t₂g is lowered.'),
            ('Valence bond theory explains the colour of complexes.', 'VBT does not explain colour; crystal field theory does.'),
            ('Tetrahedral complexes are usually low spin.', 'Δt is small (≈ 4/9 Δo), so pairing is rarely favoured; they are high spin.'),
            ('[CoF₆]³⁻ is an inner orbital complex.', 'It is an outer orbital (sp³d²), high-spin complex with 4 unpaired electrons.')]),
    'orders': [('spectrochemical series (increasing field strength)', ['I⁻', 'Br⁻', 'Cl⁻', 'F⁻', 'OH⁻', 'H₂O', 'NH₃', 'en', 'CN⁻', 'CO'], 'Order from the spectrochemical series: halides are weak field, CN⁻ and CO strongest.', '<')],
    'ar': [('[Fe(CN)₆]³⁻ is weakly paramagnetic while [FeF₆]³⁻ is strongly paramagnetic.', 'CN⁻ is a strong field ligand that causes pairing, while F⁻ is weak field.', 'a', '1 versus 5 unpaired electrons.'),
           ('[Ti(H₂O)₆]³⁺ is violet.', 'Ti³⁺ (d¹) absorbs green-yellow light for a t₂g → e_g transition.', 'a', 'The complementary colour (violet) is seen.'),
           ('Anhydrous CuSO₄ is white but CuSO₄·5H₂O is blue.', 'In the absence of ligands the d orbitals are not split.', 'a', 'No splitting ⇒ no d–d transition.'),
           ('[Ni(CO)₄] is tetrahedral.', 'Ni in [Ni(CO)₄] has a 3d⁸ 4s² configuration that remains unchanged.', 'c', 'CO causes pairing to 3d¹⁰; sp³ hybridisation gives a tetrahedral, diamagnetic complex.')],
    'fams': [F('C3', 'D3', 'explain', vbt), F('C3', 'D2', 'mcq', hyb_mcq), F('C4', 'D4', 'explain', cft)],
    'qa': [('C4', 'D4', 'explain', '[Fe(H₂O)₆]³⁺ is strongly paramagnetic whereas [Fe(CN)₆]³⁻ is weakly paramagnetic. Explain.',
            'Fe³⁺ is d⁵. H₂O is weak field: t₂g³ e_g² with 5 unpaired electrons. CN⁻ is strong field: t₂g⁵ with 1 unpaired electron.',
            '1 mark each correct configuration with unpaired electrons.'),
           ('C4', 'D3', 'case', 'Arjun studies two nickel complexes: [NiCl₄]²⁻ (paramagnetic) and [Ni(CN)₄]²⁻ (diamagnetic).\n(i) Give the hybridisation and shape of each. (2 marks)\n(ii) Why are they different? (1 mark)\n(iii) Calculate the spin-only moment of [NiCl₄]²⁻. (1 mark)',
            '(i) [NiCl₄]²⁻: sp³, tetrahedral; [Ni(CN)₄]²⁻: dsp², square planar. (ii) CN⁻ is a strong field ligand that pairs the 3d electrons, freeing a 3d orbital; Cl⁻ is weak field. (iii) 2 unpaired electrons ⇒ μ = √8 = 2.83 BM.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain crystal field splitting in an octahedral complex with a diagram. How does the magnitude of Δo decide whether a d⁴ complex is high spin or low spin? Why are tetrahedral complexes rarely low spin?',
            'Ligands approaching along axes raise e_g (dx²−y², dz²) by 0.6Δo and lower t₂g (dxy, dyz, dxz) by 0.4Δo. For d⁴: if Δo < P, fourth electron enters e_g (t₂g³ e_g¹, high spin); if Δo > P, it pairs in t₂g (t₂g⁴, low spin). In tetrahedral fields Δt ≈ (4/9)Δo is small and usually less than P, so pairing does not occur.',
            '2 marks diagram/splitting; 2 marks d⁴ cases; 1 mark tetrahedral.')],
}

CH5S5 = {
    'topic': 'importance and applications of coordination compounds',
    'terms': [('cisplatin', 'cis-[PtCl₂(NH₃)₂], a complex used to treat cancer'),
              ('chlorophyll', 'the green pigment of plants, a coordination compound of magnesium'),
              ('haemoglobin', 'the red pigment of blood that carries oxygen, a coordination compound of iron'),
              ("Wilkinson's catalyst", '[RhCl(PPh₃)₃], used for hydrogenation of alkenes'),
              ('chelation therapy', 'the removal of excess toxic metal from the body using chelating ligands such as EDTA or D-penicillamine')],
    'groups': [('a biologically important coordination compound', ['chlorophyll (Mg)', 'haemoglobin (Fe)', 'vitamin B₁₂, cyanocobalamin (Co)']),
               ('an industrial or analytical use of complexes', ['estimation of hardness of water with EDTA', 'extraction of gold with cyanide', 'purification of nickel via [Ni(CO)₄]', 'Wilkinson\'s catalyst for hydrogenation'])],
    'tf': (['Hardness of water is estimated by titration with Na₂EDTA.', 'Gold and silver are extracted as cyanide complexes.', 'Nickel is refined by forming volatile [Ni(CO)₄] (Mond process).',
            'Cisplatin is used in the treatment of cancer.', 'Vitamin B₁₂ contains cobalt.'],
           [('Chlorophyll is a coordination compound of iron.', 'Chlorophyll contains magnesium; haemoglobin contains iron.'),
            ('Vitamin B₁₂ contains iron.', 'Vitamin B₁₂ (cyanocobalamin) contains cobalt.'),
            ('Excess copper in the body is removed with dimethylglyoxime.', 'D-penicillamine and desferrioxamine B are used in chelation therapy; DMG is a test reagent for Ni²⁺.'),
            ('Silver halides in photography are fixed by forming [Ag(NH₃)₂]⁺.', 'Fixing uses hypo, forming [Ag(S₂O₃)₂]³⁻.')]),
    'ar': [('EDTA is used to estimate the hardness of water.', 'EDTA forms stable complexes with Ca²⁺ and Mg²⁺.', 'a', 'Selective complexation allows titration.'),
           ('Dimethylglyoxime is used to detect Ni²⁺.', 'Ni²⁺ forms a red precipitate with dimethylglyoxime.', 'a', 'A specific chelate is formed.')],
    'features': {'intro': 'A coordination compound has the following role:', 'q': 'Identify the compound', 'what': 'compound', 'long': False,
                 'items': [('haemoglobin', ['contains iron', 'red pigment of blood', 'carries oxygen', 'metal is held in a porphyrin ring']),
                           ('chlorophyll', ['contains magnesium', 'green pigment of plants', 'needed for photosynthesis', 'metal is held in a porphyrin-type ring']),
                           ('cisplatin', ['contains platinum(II)', 'square planar cis isomer', 'anticancer drug', 'formula [PtCl₂(NH₃)₂]']),
                           ('Na₂EDTA', ['hexadentate in its anionic form', 'used to estimate Ca²⁺ and Mg²⁺', 'removes lead in chelation therapy', 'forms 1 : 1 complexes'])]},
    'qa': [('C4', 'D4', 'explain', 'How is the hardness of water estimated using coordination compounds? Why does EDTA form very stable complexes?',
            'Ca²⁺ and Mg²⁺ are titrated with Na₂EDTA, which forms stable 1 : 1 complexes; the end point is seen with an indicator. EDTA is hexadentate, forming several five-membered chelate rings (chelate effect).',
            '1 mark method; 1 mark chelate effect.'),
           ('C3', 'D2', 'explain', 'Give two uses of coordination compounds in metallurgy.',
            'Extraction of silver and gold as [Ag(CN)₂]⁻ and [Au(CN)₂]⁻ followed by displacement with zinc; purification of nickel by forming [Ni(CO)₄] and decomposing it (Mond process).',
            '1 mark each.')],
}

# ---------------------------------------------------------------- unit 6: haloalkanes and haloarenes

HALO_NAMES = [('(CH₃)₂CHCH₂Cl', '1-chloro-2-methylpropane', ['2-methyl-1-chloropropane', '1-chloro-2-methylbutane', '2-chloro-2-methylpropane']),
              ('CH₃CH₂CH(Br)CH₃', '2-bromobutane', ['3-bromobutane', '1-bromobutane', '2-bromopropane']),
              ('(CH₃)₃CBr', '2-bromo-2-methylpropane', ['1-bromo-2-methylpropane', 'tert-butyl bromide-1', '2-bromobutane']),
              ('CH₂=CHCH₂Br', '3-bromoprop-1-ene', ['1-bromoprop-2-ene', '3-bromopropene-2', '2-bromoprop-1-ene']),
              ('CH₃CH(Cl)CH(CH₃)₂', '2-chloro-3-methylbutane', ['3-chloro-2-methylbutane', '2-chloro-3-methylpentane', '2-chloro-2-methylbutane']),
              ('ClCH₂CH₂Cl', '1,2-dichloroethane', ['1,1-dichloroethane', 'dichloroethene', '1,2-dichloroethene']),
              ('CH₃CHCl₂', '1,1-dichloroethane', ['1,2-dichloroethane', '2,2-dichloroethane', 'ethylidene dichloride-1']),
              ('CH₂=CHCl', 'chloroethene', ['chloroethane', '1-chloroethyne', '2-chloroethene']),
              ('C₆H₅CH₂Cl', '(chloromethyl)benzene', ['chlorobenzene', '1-chloro-2-methylbenzene', 'chlorophenylmethane-2']),
              ('CHCl₃', 'trichloromethane', ['tetrachloromethane', 'dichloromethane', 'trichloroethane']),
              ('CH₃CH₂C(CH₃)₂Br', '2-bromo-2-methylbutane', ['3-bromo-3-methylbutane', '2-bromo-3-methylbutane', '2-bromopentane']),
              ('CH₃CH(CH₃)CH(Br)CH₃', '2-bromo-3-methylbutane', ['3-bromo-2-methylbutane', '2-bromo-2-methylbutane', '2-bromopentane'])]


def halo_name(r):
    f, good, wrong = r.choice(HALO_NAMES)
    return mcq(f'What is the IUPAC name of {f}?', good, wrong, f'{f} = {good} (lowest locants; substituents in alphabetical order).', r)


HCLASS = [('CH₃CH₂Cl', 'a primary (1°) alkyl halide'), ('(CH₃)₂CHCl', 'a secondary (2°) alkyl halide'), ('(CH₃)₃CCl', 'a tertiary (3°) alkyl halide'),
          ('CH₂=CHCH₂Cl', 'an allylic halide'), ('C₆H₅CH₂Cl', 'a benzylic halide'), ('CH₂=CHCl', 'a vinylic halide'), ('C₆H₅Cl', 'an aryl halide'),
          ('CH₃CH₂CH₂Br', 'a primary (1°) alkyl halide'), ('CH₃CH(Br)CH₂CH₃', 'a secondary (2°) alkyl halide'), ('(CH₃)₂C(Br)CH₂CH₃', 'a tertiary (3°) alkyl halide'),
          ('CH₂=CHCH₂Br', 'an allylic halide'), ('C₆H₅CH(Cl)CH₃', 'a benzylic halide'), ('CH₃CH=CHBr', 'a vinylic halide'), ('p-ClC₆H₄CH₃', 'an aryl halide')]


def halo_class(r):
    f, c = r.choice(HCLASS)
    cls = sorted({x[1] for x in HCLASS} - {c})
    return mcq(f'Classify {f}.', c, r.sample(cls, 3), f'{f} is {c}.', r)


PREP = [('ethanol', 'SOCl₂ (in pyridine)', 'chloroethane', 'by-products SO₂ and HCl are gases, so the product is pure'),
        ('bromoethane', 'NaI in dry acetone', 'iodoethane', 'Finkelstein reaction; NaBr precipitates and drives the reaction forward'),
        ('bromomethane', 'AgF', 'fluoromethane', 'Swarts reaction'),
        ('benzenediazonium chloride', 'CuCl/HCl', 'chlorobenzene', 'Sandmeyer reaction'),
        ('benzene', 'Cl₂ in the presence of anhydrous FeCl₃', 'chlorobenzene', 'electrophilic substitution'),
        ('propene', 'HBr', '2-bromopropane', "Markovnikov's addition"),
        ('propene', 'HBr in the presence of a peroxide', '1-bromopropane', 'anti-Markovnikov (peroxide) addition'),
        ('toluene', 'Cl₂ in sunlight (excess toluene)', 'benzyl chloride', 'free-radical side-chain substitution'),
        ('toluene', 'Cl₂ with anhydrous FeCl₃ in the dark', 'a mixture of o- and p-chlorotoluene', 'ring substitution; CH₃ is o/p-directing'),
        ('propan-2-ol', 'conc. HCl with anhydrous ZnCl₂ (Lucas reagent)', '2-chloropropane', 'substitution of –OH by Cl'),
        ('ethanol', 'PCl₅', 'chloroethane', 'replacement of –OH; POCl₃ and HCl are by-products')]


def prep(r):
    s, reag, p, why = r.choice(PREP)
    wrong = [x[2] for x in PREP if x[2] != p]
    wrong = list(dict.fromkeys(r.sample(wrong, len(wrong))))[:3]
    return mcq(f'What is the main organic product when {s} is treated with {reag}?', p, wrong, f'{p}: {why}.', r)


RXN = [('chloroethane', 'alcoholic KCN', 'propanenitrile (CH₃CH₂CN)', 'CN⁻ attacks through carbon (C–C bond is stronger)'),
       ('chloroethane', 'AgCN', 'ethyl isocyanide (CH₃CH₂NC)', 'Ag–C bond is covalent, so the nitrogen attacks'),
       ('bromoethane', 'KNO₂', 'ethyl nitrite (CH₃CH₂ONO)', 'the ionic nitrite attacks through oxygen'),
       ('bromoethane', 'AgNO₂', 'nitroethane (CH₃CH₂NO₂)', 'the covalent AgNO₂ attacks through nitrogen'),
       ('bromoethane', 'aqueous KOH', 'ethanol', 'nucleophilic substitution by OH⁻'),
       ('2-bromobutane', 'alcoholic KOH (heat)', 'but-2-ene (major)', "β-elimination; Zaitsev's rule gives the more substituted alkene"),
       ('bromoethane', 'sodium in dry ether', 'butane', 'Wurtz reaction'),
       ('chlorobenzene', 'sodium and CH₃Cl in dry ether', 'toluene', 'Wurtz–Fittig reaction'),
       ('chlorobenzene', 'NaOH at 623 K and 300 atm, then H⁺', 'phenol', 'Dow process'),
       ('bromoethane', 'Mg in dry ether', 'ethylmagnesium bromide (CH₃CH₂MgBr)', 'formation of a Grignard reagent'),
       ('chlorobenzene', 'conc. HNO₃ + conc. H₂SO₄', '1-chloro-4-nitrobenzene (major) and 1-chloro-2-nitrobenzene', 'Cl is deactivating but o/p-directing'),
       ('bromobenzene', 'sodium in dry ether', 'biphenyl', 'Fittig reaction'),
       ('chloroethane', 'NH₃ (alcoholic, excess)', 'ethanamine', 'nucleophilic substitution (ammonolysis)'),
       ('2-bromopentane', 'alcoholic KOH (heat)', 'pent-2-ene (major)', "Zaitsev's rule")]


def rxn(r):
    s, reag, p, why = r.choice(RXN)
    wrong = list(dict.fromkeys(x[2] for x in r.sample(RXN, len(RXN)) if x[2] != p))[:3]
    return mcq(f'What is the main organic product when {s} reacts with {reag}?', p, wrong, f'{p}: {why}.', r)


def rxn_explain(r):
    s, reag, p, why = r.choice(RXN)
    return {'stem': f'Write the product and name the type of reaction when {s} is treated with {reag}.', 'answer': f'{cap(p)}; {why}',
            'key': f'Product: {p} (1); {why} (1).', 'distractors': [f'{cap(x[2])}; {x[3]}' for x in RXN if x[2] != p][:3]}


CHIRAL = [('2-bromobutane', 1), ('2-chlorobutane', 1), ('butan-2-ol', 1), ('2-chloropentane', 1), ('1-chloro-2-methylbutane', 1),
          ('2-bromo-3-methylbutane', 1), ('3-bromohex-1-ene', 1), ('2-hydroxypropanoic acid (lactic acid)', 1)]
ACHIRAL = ['2-bromopropane', '1-bromobutane', '3-chloropentane', '2-chloro-2-methylbutane', '1-chloropropane', '2-bromo-2-methylpropane',
           'chloroethane', '3-bromopentane', 'propan-2-ol', '1-bromo-2-methylpropane']


def chiral_pick(r):
    if r.random() < 0.6:
        good = r.choice(CHIRAL)[0]
        return mcq('Which of the following compounds is chiral (optically active)?', good, r.sample(ACHIRAL, 3),
                   f'{cap(good)} has a carbon bonded to four different groups.', r)
    good = r.choice(ACHIRAL)
    return mcq('Which of the following compounds is NOT chiral?', good, [x[0] for x in r.sample(CHIRAL, 3)],
               f'{cap(good)} has no carbon bonded to four different groups.', r)


ENANT = [('(+)-butan-2-ol', 13.5), ('(+)-2-bromobutane', 23.1), ('(+)-lactic acid', 3.8), ('(+)-2-chlorobutane', 36.0)]


def ee(r):
    c, a = r.choice(ENANT)
    pur = r.choice([20, 30, 40, 50, 60, 70, 80, 90])
    obs = a * pur / 100
    maj = 50 + pur / 2
    return {'stem': f'Pure {c} has a specific rotation of +{a}°. A sample of it prepared by Sneha shows a specific rotation of +{sf(obs, 3)}°. Calculate the optical purity (enantiomeric excess) and the percentage of each enantiomer.',
            'answer': f'{pur}% ee; {num(maj, 1)}% (+) and {num(100 - maj, 1)}% (−)',
            'key': f'Optical purity = observed/pure × 100 = {sf(obs, 3)}/{a} × 100 = {pur}% (1); (+) = 50 + ee/2 = {num(maj, 1)}%, (−) = {num(100 - maj, 1)}% (the rest is racemic) (2).',
            'distractors': [f'{pur}% ee; {pur}% (+) and {100 - pur}% (−)', f'{100 - pur}% ee; {num(50 + (100 - pur) / 2, 1)}% (+) and {num(50 - (100 - pur) / 2, 1)}% (−)', f'{pur}% ee; 50% (+) and 50% (−)']}


CH6S1 = {
    'topic': 'classification, nomenclature and the C–X bond',
    'terms': [('a haloalkane', 'a compound in which a halogen atom is bonded to an sp³ hybridised carbon of an alkyl group'),
              ('a haloarene', 'a compound in which a halogen atom is bonded directly to an sp² carbon of an aromatic ring'),
              ('an allylic halide', 'a compound in which the halogen is bonded to an sp³ carbon next to a C=C double bond'),
              ('a benzylic halide', 'a compound in which the halogen is bonded to an sp³ carbon attached to an aromatic ring'),
              ('a vinylic halide', 'a compound in which the halogen is bonded to an sp² carbon of a C=C double bond'),
              ('a gem-dihalide', 'a dihalide with both halogen atoms on the same carbon atom')],
    'groups': [('a vic-dihalide', ['1,2-dichloroethane', '1,2-dibromopropane', '2,3-dichlorobutane']), ('a gem-dihalide', ['1,1-dichloroethane', '2,2-dibromopropane', 'dichloromethane']),
               ('a monohalide', ['chloroethane', '2-bromobutane', 'iodomethane'])],
    'tf': (['The C–X bond is polar, with carbon carrying a partial positive charge.', 'C–X bond length increases from C–F to C–I.', 'C–X bond enthalpy decreases from C–F to C–I.',
            'In haloarenes the halogen is bonded to an sp² carbon.', 'CH₂=CHCH₂Cl is an allylic halide.'],
           [('C–X bond enthalpy increases from C–F to C–I.', 'It decreases from C–F to C–I as bond length increases.'),
            ('C₆H₅CH₂Cl is an aryl halide.', 'The halogen is on an sp³ carbon next to the ring: it is a benzylic halide.'),
            ('In CH₂=CHCl the halogen is bonded to an sp³ carbon.', 'It is bonded to an sp² carbon; CH₂=CHCl is a vinylic halide.'),
            ('Ethylidene chloride is 1,2-dichloroethane.', 'Ethylidene chloride is 1,1-dichloroethane; ethylene dichloride is 1,2-dichloroethane.')]),
    'orders': [('order of C–X bond length', ['C–F', 'C–Cl', 'C–Br', 'C–I'], 'Bond length increases as the size of the halogen increases.', '<'),
               ('order of C–X bond enthalpy', ['C–F', 'C–Cl', 'C–Br', 'C–I'], 'Larger halogen ⇒ longer, weaker bond.', '>'),
               ('order of dipole moment', ['CH₃Cl', 'CH₃F', 'CH₃Br', 'CH₃I'], 'CH₃F has a short bond, so its dipole is a little below CH₃Cl; then it falls with electronegativity.', '>')],
    'ar': [('The C–X bond in haloalkanes is polar.', 'Halogens are more electronegative than carbon.', 'a', 'Carbon carries δ⁺, halogen δ⁻.'),
           ('C–Cl bond in chlorobenzene is shorter than in chloroethane.', 'In chlorobenzene the C–Cl bond has partial double bond character due to resonance and carbon is sp².', 'a', 'Both effects shorten the bond.'),
           ('CH₃F has a lower dipole moment than CH₃Cl.', 'Fluorine is less electronegative than chlorine.', 'c', 'F is more electronegative; the smaller C–F bond length lowers the dipole.')],
    'fams': [F('C2', 'D2', 'mcq', halo_name), F('C2', 'D1', 'mcq', halo_class)],
    'qa': [('C1', 'D2', 'short', 'Write the IUPAC name of CH₃CH(Cl)CH₂CH₃.', '2-Chlorobutane.', '1 mark.'),
           ('C4', 'D4', 'explain', 'Write the structures of all isomers of C₄H₉Br and classify each as 1°, 2° or 3°.',
            '1-Bromobutane (1°), 2-bromobutane (2°), 1-bromo-2-methylpropane (1°), 2-bromo-2-methylpropane (3°).',
            '1 mark structures; 1 mark classification.'),
           ('C4', 'D3', 'case', 'Kavya examines the compounds CH₃CH₂Cl, CH₂=CHCl and C₆H₅Cl.\n(i) Classify each. (1 mark)\n(ii) Which has the longest C–Cl bond? Why? (2 marks)\n(iii) Which carbon hybridisation is present in the C–Cl bond of chloroethane? (1 mark)',
            '(i) Chloroethane: 1° alkyl halide; CH₂=CHCl: vinylic; C₆H₅Cl: aryl. (ii) Chloroethane: in vinyl and aryl chlorides resonance gives partial double bond character and the carbon is sp², shortening the bond. (iii) sp³.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH6S2 = {
    'topic': 'preparation and physical properties of haloalkanes',
    'terms': [('the Finkelstein reaction', 'the preparation of alkyl iodides by treating alkyl chlorides or bromides with NaI in dry acetone'),
              ('the Swarts reaction', 'the preparation of alkyl fluorides by heating alkyl chlorides or bromides with metallic fluorides such as AgF or Hg₂F₂'),
              ('the Sandmeyer reaction', 'the replacement of the diazonium group by Cl or Br using CuCl/HCl or CuBr/HBr'),
              ('thionyl chloride', 'SOCl₂, the preferred reagent for converting alcohols to alkyl chlorides because its by-products are gases'),
              ("Lucas reagent", 'concentrated HCl with anhydrous ZnCl₂, used to convert alcohols to chlorides and to distinguish 1°, 2° and 3° alcohols')],
    'groups': [('a method of preparing haloalkanes from alcohols', ['SOCl₂', 'PCl₅', 'PCl₃', 'HCl with anhydrous ZnCl₂']), ('a halogen exchange method', ['Finkelstein reaction', 'Swarts reaction']),
               ('a method of preparing haloarenes', ['Sandmeyer reaction', 'Cl₂ with FeCl₃', 'Gattermann reaction'])],
    'tf': (['Boiling points of alkyl halides increase in the order RF < RCl < RBr < RI.', 'Among isomeric alkyl halides, boiling point decreases with branching.',
            'p-Dichlorobenzene has a higher melting point than o- and m-isomers.', 'Haloalkanes are only slightly soluble in water.', 'Density increases with the number and atomic mass of halogen atoms.'],
           [('Branching increases the boiling point of isomeric haloalkanes.', 'Branching lowers the surface area and van der Waals forces, so the boiling point decreases.'),
            ('Haloalkanes are highly soluble in water.', 'They cannot form strong hydrogen bonds with water, so they are only slightly soluble.'),
            ('Alkyl iodides are prepared by direct iodination of alkanes in good yield.', 'Iodination is reversible; iodides are made by the Finkelstein reaction.'),
            ('In the Swarts reaction alkyl iodides are formed.', 'Alkyl fluorides are formed using AgF, Hg₂F₂, CoF₂ or SbF₃.')]),
    'orders': [('order of boiling point', ['CH₃Cl', 'CH₃Br', 'CH₃I'], 'Larger, more polarisable halogen ⇒ stronger van der Waals forces.', '<'),
               ('order of boiling point of isomers', ['2-bromo-2-methylpropane', '2-bromobutane', '1-bromobutane'], 'More branching ⇒ smaller surface area ⇒ lower boiling point.', '<'),
               ('order of density', ['CH₂Cl₂', 'CHCl₃', 'CCl₄'], 'Density increases with number of chlorine atoms.', '<')],
    'ar': [('SOCl₂ is preferred for preparing alkyl chlorides from alcohols.', 'The by-products SO₂ and HCl escape as gases, leaving a pure product.', 'a', 'No separation needed.'),
           ('p-Dichlorobenzene has a higher melting point than o-dichlorobenzene.', 'The para isomer is more symmetrical and fits better in the crystal lattice.', 'a', 'Better packing.'),
           ('Alkyl halides are soluble in water.', 'Less energy is released when new attractions form between haloalkane and water than is needed to break hydrogen bonds in water.', 'd', 'They are only slightly soluble; the reason is true and explains the low solubility.')],
    'fams': [F('C2', 'D2', 'mcq', prep)],
    'qa': [('C3', 'D2', 'explain', 'Write the equation for the Finkelstein reaction and explain why it goes to completion.',
            'CH₃CH₂Br + NaI → CH₃CH₂I + NaBr (in dry acetone). NaBr is insoluble in acetone and precipitates, which shifts the equilibrium forward (Le Chatelier).',
            '1 mark equation; 1 mark reason.'),
           ('C4', 'D4', 'explain', 'How will you prepare (i) chlorobenzene from aniline and (ii) iodoethane from ethanol? Write equations.',
            '(i) Aniline + NaNO₂/HCl at 273–278 K → benzenediazonium chloride; with CuCl/HCl → chlorobenzene + N₂. (ii) Ethanol + SOCl₂ → chloroethane; then NaI/dry acetone → iodoethane (Finkelstein).',
            '1 mark each conversion.'),
           ('C4', 'D3', 'case', 'Manish compares the boiling points of CH₃Cl (249 K), CH₃Br (276 K), CH₃I (316 K) and of the isomers of C₄H₉Br.\n(i) Why does the boiling point rise from CH₃Cl to CH₃I? (1 mark)\n(ii) Arrange 1-bromobutane, 2-bromobutane and 2-bromo-2-methylpropane by boiling point. (2 marks)\n(iii) Why are haloalkanes heavier than water? (1 mark)',
            '(i) Molecular mass and polarisability increase, so van der Waals forces increase. (ii) 2-Bromo-2-methylpropane < 2-bromobutane < 1-bromobutane; branching lowers surface area. (iii) Halogen atoms have high atomic mass, so bromo and iodo compounds are denser than water.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH6S3 = {
    'topic': 'reactions of haloalkanes and haloarenes',
    'terms': [('an SN2 reaction', 'a one-step bimolecular nucleophilic substitution with backside attack and inversion of configuration'),
              ('an SN1 reaction', 'a two-step unimolecular nucleophilic substitution through a carbocation intermediate'),
              ("Zaitsev's rule", 'the rule that in dehydrohalogenation the preferred alkene has the greater number of alkyl groups on the doubly bonded carbons'),
              ('a Grignard reagent', 'an alkylmagnesium halide RMgX, made from an alkyl halide and Mg in dry ether'),
              ('the Wurtz–Fittig reaction', 'the reaction of an aryl halide and an alkyl halide with sodium in dry ether to give an alkylarene'),
              ('an ambident nucleophile', 'a nucleophile that can attack through two different atoms, such as CN⁻ or NO₂⁻')],
    'tf': (['Tertiary alkyl halides react fastest by the SN1 mechanism.', 'SN2 reactions occur with inversion of configuration.', 'Grignard reagents must be prepared under anhydrous conditions.',
            'Electron-withdrawing groups at ortho and para positions increase the reactivity of haloarenes towards nucleophiles.', 'Haloarenes are less reactive than haloalkanes towards nucleophilic substitution.'],
           [('Primary alkyl halides react fastest by the SN1 mechanism.', 'Tertiary halides form the most stable carbocations and react fastest by SN1; primary halides prefer SN2.'),
            ('The rate of an SN2 reaction depends only on the concentration of the alkyl halide.', 'It depends on both alkyl halide and nucleophile: rate = k[RX][Nu⁻].'),
            ('Chlorobenzene readily gives phenol with aqueous NaOH at room temperature.', 'It needs NaOH at 623 K and 300 atm (Dow process).'),
            ('Haloalkanes give isocyanides with KCN.', 'With KCN they give nitriles; AgCN gives isocyanides.')]),
    'orders': [('order of reactivity towards SN2', ['CH₃Br', 'CH₃CH₂Br', '(CH₃)₂CHBr', '(CH₃)₃CBr'], 'Steric hindrance to backside attack increases from methyl to tertiary.', '>'),
               ('order of reactivity towards SN1', ['(CH₃)₃CBr', '(CH₃)₂CHBr', 'CH₃CH₂Br', 'CH₃Br'], 'Carbocation stability: 3° > 2° > 1° > methyl.', '>'),
               ('order of reactivity of haloalkanes (same alkyl group)', ['R–I', 'R–Br', 'R–Cl', 'R–F'], 'Weaker C–X bond ⇒ better leaving group.', '>')],
    'ar': [('KCN gives alkyl cyanides while AgCN gives isocyanides with haloalkanes.', 'KCN is ionic and attacks through C; AgCN is covalent so N attacks.', 'a', 'Ambident cyanide.'),
           ('Haloarenes are less reactive than haloalkanes towards nucleophilic substitution.', 'The C–X bond in haloarenes has partial double bond character due to resonance.', 'a', 'Resonance, sp² carbon and repulsion of the π cloud all reduce reactivity.'),
           ('(CH₃)₃CBr undergoes SN1 faster than CH₃CH₂Br.', 'The tertiary carbocation is stabilised by hyperconjugation and inductive effect.', 'a', 'More stable carbocation ⇒ faster SN1.'),
           ('Grignard reagents are prepared in aqueous medium.', 'Grignard reagents react with water to give alkanes.', 'd', 'They must be prepared in dry ether.')],
    'features': {'intro': 'A substitution mechanism has these features:', 'q': 'Identify the mechanism', 'what': 'mechanism', 'compare': True,
                 'items': [('SN2', ['one step, no intermediate', 'rate = k[RX][Nu⁻]', 'inversion of configuration', 'fastest for CH₃X and 1° halides']),
                           ('SN1', ['two steps via a carbocation', 'rate = k[RX]', 'racemisation of an optically active substrate', 'fastest for 3° halides, favoured by polar protic solvents']),
                           ('β-elimination (E2)', ['strong base such as alcoholic KOH', 'H and X lost from adjacent carbons', 'alkene formed', "major product follows Zaitsev's rule"])]},
    'fams': [F('C3', 'D3', 'mcq', rxn), F('C3', 'D2', 'explain', rxn_explain)],
    'qa': [('C4', 'D4', 'explain', 'Why is chlorobenzene less reactive than chloroethane towards nucleophilic substitution? Give two reasons.',
            '(i) Resonance gives the C–Cl bond partial double bond character, making it hard to break. (ii) The carbon is sp² hybridised, more electronegative, giving a shorter, stronger bond; also the electron-rich ring repels the nucleophile and the phenyl cation is unstable.',
            '1 mark each reason.'),
           ('C4', 'D5', 'long', 'Explain the SN1 and SN2 mechanisms with suitable examples. How do the structure of the alkyl halide and the stereochemistry of the product differ in the two cases?',
            'SN2: e.g. CH₃Cl + OH⁻; one step, backside attack through a pentacoordinate transition state; rate = k[RX][OH⁻]; inversion; reactivity CH₃ > 1° > 2° > 3°. SN1: e.g. (CH₃)₃CBr + OH⁻; slow ionisation to carbocation, then fast attack; rate = k[RX]; racemisation of chiral substrates; reactivity 3° > 2° > 1°; favoured by polar protic solvents.',
            '2 marks each mechanism; 1 mark comparison.')],
}

CH6S4 = {
    'topic': 'stereochemistry: optical isomerism and chirality',
    'terms': [('a chiral molecule', 'a molecule that is not superimposable on its mirror image'),
              ('enantiomers', 'stereoisomers that are non-superimposable mirror images of each other'),
              ('a racemic mixture', 'an equimolar mixture of two enantiomers, showing zero optical rotation'),
              ('an asymmetric carbon', 'a carbon atom bonded to four different groups'),
              ('a polarimeter', 'the instrument used to measure the rotation of plane-polarised light by an optically active compound'),
              ('retention of configuration', 'preservation of the spatial arrangement of bonds at a stereocentre during a reaction')],
    'groups': [('a dextrorotatory label', ['(+)', 'd-']), ('a laevorotatory label', ['(−)', 'l-']), ('a description of a racemic mixture', ['(±)', 'dl-', 'equimolar mixture of enantiomers'])],
    'classify': False,
    'tf': (['Enantiomers rotate plane-polarised light by equal amounts in opposite directions.', 'A racemic mixture is optically inactive.', 'SN1 reaction of an optically active halide gives mainly a racemic product.',
            'Butan-2-ol is chiral.', 'Enantiomers have identical boiling points.'],
           [('2-Bromopropane is chiral.', 'Its C-2 carries two identical CH₃ groups, so it is achiral.'),
            ('A racemic mixture rotates plane-polarised light to the right.', 'The rotations of the two enantiomers cancel; it is optically inactive.'),
            ('SN2 reactions proceed with retention of configuration.', 'SN2 reactions proceed with inversion (Walden inversion).'),
            ('Enantiomers have different melting points.', 'Enantiomers have identical physical properties except the sign of rotation.')]),
    'ar': [('2-Bromobutane is optically active.', 'It contains a carbon atom bonded to four different groups.', 'a', 'C-2 bears H, Br, CH₃ and C₂H₅.'),
           ('A racemic mixture is optically inactive.', 'It contains equal amounts of the two enantiomers.', 'a', 'Rotations cancel exactly.'),
           ('Hydrolysis of optically active 2-bromobutane by SN1 gives an optically inactive product.', 'The planar carbocation is attacked equally from both faces.', 'a', 'Racemisation.'),
           ('Optical isomers can be separated by fractional distillation.', 'Enantiomers have identical boiling points.', 'd', 'They cannot be separated by distillation; the reason is true.')],
    'fams': [F('C3', 'D3', 'mcq', chiral_pick), F('C4', 'D4', 'multi_step', ee)],
    'qa': [('C3', 'D2', 'explain', 'Identify the chiral molecule in the pair 2-chlorobutane and 1-chlorobutane, and mark the asymmetric carbon.',
            '2-Chlorobutane is chiral; C-2 (bearing H, Cl, CH₃ and C₂H₅) is the asymmetric carbon. 1-Chlorobutane has no such carbon.',
            '1 mark identification; 1 mark asymmetric carbon.'),
           ('C4', 'D4', 'explain', 'Optically active 2-bromobutane gives an optically inactive product on hydrolysis under SN1 conditions, but an inverted product under SN2 conditions. Explain.',
            'SN1: the planar carbocation is attacked from both sides equally ⇒ racemic mixture (inactive). SN2: OH⁻ attacks from the side opposite to Br ⇒ inversion of configuration (product is optically active with opposite configuration).',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'Ishaan places a solution of an organic compound in a polarimeter and finds that it rotates plane-polarised light to the left. The compound is C₄H₉Br.\n(i) Which isomer is it? (1 mark)\n(ii) What label is used for leftward rotation? (1 mark)\n(iii) What would be observed if an equal amount of its mirror image were mixed in, and what is this mixture called? (2 marks)',
            '(i) 2-Bromobutane (the only chiral isomer of C₄H₉Br). (ii) Laevorotatory, (−) or l. (iii) Zero rotation; a racemic mixture.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH6S5 = {
    'topic': 'polyhalogen compounds',
    'terms': [('freons', 'chlorofluorocarbons of methane and ethane, such as CCl₂F₂, used as refrigerants and propellants'),
              ('DDT', 'p,p′-dichlorodiphenyltrichloroethane, the first chlorinated organic insecticide'),
              ('iodoform', 'CHI₃, a yellow solid used earlier as an antiseptic because it liberates iodine'),
              ('phosgene', 'COCl₂, the highly poisonous gas formed when chloroform is oxidised by air in light'),
              ('biomagnification', 'the increase in concentration of a persistent chemical such as DDT at higher levels of a food chain')],
    'groups': [('a use of carbon tetrachloride (earlier or current)', ['manufacture of refrigerants and propellants', 'solvent for oils and fats', 'earlier, fire extinguisher']),
               ('a use of chloroform', ['solvent for fats, alkaloids and iodine', 'manufacture of the refrigerant R-22', 'earlier, as a general anaesthetic']),
               ('a use of dichloromethane', ['paint remover', 'propellant in aerosols', 'process solvent in drug manufacture'])],
    'tf': (['Chloroform is stored in closed dark coloured bottles filled to the brim.', 'DDT is not biodegradable and accumulates in fatty tissues.', 'Freons cause depletion of the ozone layer.',
            'Iodoform acts as an antiseptic because it liberates free iodine.', 'Dichloromethane affects the central nervous system on exposure.'],
           [('Chloroform is oxidised by air in light to carbon dioxide only.', 'It is oxidised to the highly poisonous phosgene (COCl₂).'),
            ('DDT is rapidly broken down in the environment.', 'DDT is very persistent and is stored in fatty tissues, leading to biomagnification.'),
            ('Freons are highly reactive and toxic.', 'Freons are unreactive, non-toxic and non-corrosive; their harm is ozone depletion in the stratosphere.'),
            ('The smell of iodoform is pleasant, so it is still used widely.', 'Its unpleasant smell led to its replacement by other iodine formulations.')]),
    'ar': [('Chloroform is stored in dark bottles filled to the brim.', 'Chloroform is slowly oxidised by air in light to phosgene.', 'a', 'Dark bottles and no air space prevent this.'),
           ('DDT use was banned in many countries.', 'DDT is not biodegradable and accumulates in food chains.', 'a', 'It harms birds and fish.'),
           ('Freons damage the ozone layer.', 'In the stratosphere freons release chlorine radicals that catalyse decomposition of ozone.', 'a', 'Cl• + O₃ → ClO• + O₂ chain.')],
    'features': {'intro': 'A polyhalogen compound has these features:', 'q': 'Identify the compound', 'what': 'compound',
                 'items': [('chloroform (CHCl₃)', ['solvent for fats, alkaloids and iodine', 'earlier used as an anaesthetic', 'oxidised in light to phosgene', 'stored in dark bottles']),
                           ('iodoform (CHI₃)', ['yellow solid', 'formed from ethanol or propanone with I₂ and NaOH', 'antiseptic action due to liberated iodine', 'unpleasant smell']),
                           ('carbon tetrachloride (CCl₄)', ['used to make refrigerants and propellants', 'earlier used in fire extinguishers', 'can damage the liver', 'released into air it depletes ozone']),
                           ('freon-12 (CCl₂F₂)', ['used in refrigeration and air conditioning', 'very stable and non-toxic', 'reaches the stratosphere unchanged', 'releases chlorine radicals that destroy ozone']),
                           ('DDT', ['first chlorinated organic insecticide', 'used against malaria-carrying mosquitoes', 'not biodegradable', 'accumulates in fatty tissues'])]},
    'qa': [('C3', 'D2', 'explain', 'Write the reaction that occurs when chloroform is exposed to air and light. How is this prevented?',
            '2CHCl₃ + O₂ → 2COCl₂ + 2HCl (light). It is stored in closed dark coloured bottles filled completely, so that air is kept out.',
            '1 mark equation; 1 mark precaution.')],
}

SPECS = {'ch04-st1': CH4S1, 'ch04-st2': CH4S2, 'ch04-st3': CH4S3, 'ch04-st4': CH4S4,
         'ch05-st1': CH5S1, 'ch05-st2': CH5S2, 'ch05-st3': CH5S3, 'ch05-st4': CH5S4, 'ch05-st5': CH5S5,
         'ch06-st1': CH6S1, 'ch06-st2': CH6S2, 'ch06-st3': CH6S3, 'ch06-st4': CH6S4, 'ch06-st5': CH6S5}
FAMILIES = build_all(P, SPECS)
