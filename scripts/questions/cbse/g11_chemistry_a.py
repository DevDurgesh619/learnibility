"""CBSE class 11 chemistry families, units 1-3 (Basic concepts, Structure of atom, Periodicity)."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, near, cap

P = 'cbse-g11-chemistry'

NA = 6.022e23
AM = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'Na': 23, 'Mg': 24, 'Al': 27, 'S': 32, 'Cl': 35.5, 'K': 39, 'Ca': 40,
      'Fe': 56, 'Cu': 63.5, 'Zn': 65, 'P': 31, 'Ag': 108, 'Br': 80}

# (display formula, composition, name)
CMPD = [
    ('H₂O', {'H': 2, 'O': 1}, 'water'), ('CO₂', {'C': 1, 'O': 2}, 'carbon dioxide'),
    ('NH₃', {'N': 1, 'H': 3}, 'ammonia'), ('CH₄', {'C': 1, 'H': 4}, 'methane'),
    ('C₆H₁₂O₆', {'C': 6, 'H': 12, 'O': 6}, 'glucose'), ('NaCl', {'Na': 1, 'Cl': 1}, 'sodium chloride'),
    ('H₂SO₄', {'H': 2, 'S': 1, 'O': 4}, 'sulphuric acid'), ('CaCO₃', {'Ca': 1, 'C': 1, 'O': 3}, 'calcium carbonate'),
    ('NaOH', {'Na': 1, 'O': 1, 'H': 1}, 'sodium hydroxide'), ('HCl', {'H': 1, 'Cl': 1}, 'hydrogen chloride'),
    ('C₂H₅OH', {'C': 2, 'H': 6, 'O': 1}, 'ethanol'), ('CO(NH₂)₂', {'C': 1, 'O': 1, 'N': 2, 'H': 4}, 'urea'),
    ('Na₂CO₃', {'Na': 2, 'C': 1, 'O': 3}, 'sodium carbonate'), ('MgO', {'Mg': 1, 'O': 1}, 'magnesium oxide'),
    ('CH₃COOH', {'C': 2, 'H': 4, 'O': 2}, 'acetic acid'), ('HNO₃', {'H': 1, 'N': 1, 'O': 3}, 'nitric acid'),
    ('KCl', {'K': 1, 'Cl': 1}, 'potassium chloride'), ('C₁₂H₂₂O₁₁', {'C': 12, 'H': 22, 'O': 11}, 'sucrose'),
    ('Al₂O₃', {'Al': 2, 'O': 3}, 'aluminium oxide'), ('SO₂', {'S': 1, 'O': 2}, 'sulphur dioxide'),
    ('C₃H₈', {'C': 3, 'H': 8}, 'propane'), ('KOH', {'K': 1, 'O': 1, 'H': 1}, 'potassium hydroxide'),
]


def M(comp):
    return sum(AM[e] * n for e, n in comp.items())


def mstr(x):
    return num(x, 1)


# ---------------- ch01 st1 matter, properties, SI units, measurement ----------------

def sigfig_count(r):
    kind = r.choice(['lead0', 'trail0', 'mid0', 'sci', 'plain'])
    if kind == 'lead0':
        digits = str(r.randint(11, 999))
        s = '0.' + '0' * r.randint(1, 3) + digits
        n = len(digits)
    elif kind == 'trail0':
        base = str(r.randint(11, 99))
        z = r.randint(1, 2)
        s = base[0] + '.' + base[1:] + '0' * z
        n = len(base) + z
    elif kind == 'mid0':
        if r.random() < .5:
            s, n = f'{r.randint(1, 9)}0{r.randint(1, 9)}.{r.randint(1, 9)}', 4
        else:
            s, n = f'{r.randint(1, 9)}00{r.randint(1, 9)}', 4
    elif kind == 'sci':
        m = f'{r.randint(1, 9)}.{r.randint(10, 99)}' + ('0' if r.random() < .5 else '')
        e = r.choice(['²', '³', '⁴', '⁵', '⁻²', '⁻³', '⁻⁴'])
        s = f'{m} × 10{e}'
        n = len(m.replace('.', ''))
    else:
        s, n = f'{r.randint(1, 9)}{r.randint(1, 9)}.{r.randint(1, 9)}{r.randint(1, 9)}', 4
    return {'stem': f'How many significant figures are present in {s}?', 'answer': str(n),
            'key': f'{s} has {n} significant figures (leading zeros are not significant; zeros between non-zero digits and trailing zeros after a decimal point are; the power of ten is not counted).',
            'distractors': [str(x) for x in [n - 1, n + 1, n + 2, n - 2] if x > 0][:3]}


def sigfig_round(r):
    n = r.choice([2, 3, 4])
    x = r.uniform(10 ** (n - 2), 10 ** (n - 1) - 0.01)
    xs = f'{x:.4f}'
    x = float(xs)
    ans = sf(x, n)
    return {'stem': f'Round off {xs} to {n} significant figures.', 'answer': ans,
            'key': f'Keep {n} digits from the left and round on the next digit: {xs} → {ans}.',
            'distractors': [sf(x, n + 1), sf(x, n - 1), f'{x:.{n}f}', f'{math.floor(x * 10 ** (n - 1 - math.floor(math.log10(x)))) / 10 ** (n - 1 - math.floor(math.log10(x))):.{max(n - 1 - math.floor(math.log10(x)), 0)}f}']}


def sigfig_calc(r):
    dec = r.choice([1, 2])
    a = round(r.uniform(1, 9.9), dec)
    b = round(r.uniform(1, 9.9), 3)
    As, Bs = f'{a:.{dec}f}', f'{b:.3f}'
    n = min(dec + 1, 4)
    prod = float(As) * float(Bs)
    ans = sf(prod, n)
    return {'stem': f'A student multiplies {As} by {Bs} on a calculator. Report the product to the correct number of significant figures.',
            'answer': ans, 'key': f'{As} × {Bs} = {prod:.5f}; a product keeps the least number of significant figures in the data ({n}), so {ans}.',
            'distractors': [f'{prod:.5f}'.rstrip('0'), sf(prod, n + 1), sf(prod, n + 2)]}


TEMP = [('°C to K', lambda c: c + 273.15, '°C', 'K'), ('°C to °F', lambda c: 9 / 5 * c + 32, '°C', '°F')]


def unit_temp(r):
    c = r.choice([-40, -10, 0, 10, 25, 37, 50, 80, 100, 120, 150, 200, 300])
    c = c + r.choice([0, 5])
    which = r.choice(TEMP)
    v = which[1](c)
    who = name(r)
    if which[3] == 'K':
        return {'stem': f'{who} records the temperature of a water bath in the laboratory as {c} °C. Express it on the kelvin scale.',
                'answer': f'{num(v, 2)} K', 'key': f'K = °C + 273.15 = {c} + 273.15 = {num(v, 2)} K.',
                'distractors': [f'{num(c - 273.15, 2)} K', f'{num(c + 273, 0)}.0 K' if c + 273 != v else f'{c + 300} K', f'{num(9 / 5 * c + 32, 1)} K']}
    return {'stem': f'Convert {c} °C into the Fahrenheit scale.', 'answer': f'{num(v, 1)} °F',
            'key': f'°F = (9/5)(°C) + 32 = (9/5)({c}) + 32 = {num(v, 1)} °F.',
            'distractors': [f'{num(5 / 9 * c + 32, 1)} °F', f'{num(9 / 5 * (c + 32), 1)} °F', f'{num(c + 273.15, 2)} °F']}


def unit_conv(r):
    k = r.choice(['L', 'density', 'mm', 'mL'])
    if k == 'L':
        v = r.choice([0.5, 1.5, 2, 2.5, 3.5, 4, 5, 7.5, 12, 25])
        return {'stem': f'A beaker holds {num(v)} L of solution. Express this volume in m³ and in cm³.',
                'answer': f'{sci(v / 1000, 2)} m³; {num(v * 1000)} cm³',
                'key': f'1 L = 1000 cm³ = 10⁻³ m³, so {num(v)} L = {num(v * 1000)} cm³ = {sci(v / 1000, 2)} m³.'}
    if k == 'density':
        d = r.choice([0.79, 0.88, 1.06, 1.2, 1.84, 2.7, 7.86, 11.3, 13.6])
        return {'stem': f'The density of a liquid is {d} g cm⁻³. Express it in the SI unit.',
                'answer': f'{num(d * 1000)} kg m⁻³',
                'key': f'1 g cm⁻³ = 10⁻³ kg / 10⁻⁶ m³ = 1000 kg m⁻³; {d} × 1000 = {num(d * 1000)} kg m⁻³.',
                'distractors': [f'{num(d / 1000, 5)} kg m⁻³', f'{num(d * 100)} kg m⁻³', f'{num(d * 1e6)} kg m⁻³']}
    if k == 'mm':
        v = r.choice([250, 500, 750, 1200, 3500, 45])
        return {'stem': f'Express {v} nm in metres using scientific notation.', 'answer': f'{sci(v * 1e-9, 2)} m',
                'key': f'1 nm = 10⁻⁹ m, so {v} nm = {sci(v * 1e-9, 2)} m.',
                'distractors': [f'{sci(v * 1e-6, 2)} m', f'{sci(v * 1e-12, 2)} m', f'{sci(v * 1e-10, 2)} m']}
    v = r.choice([5, 20, 25, 50, 75, 125, 250, 500])
    return {'stem': f'A pipette delivers {v} mL. What is this volume in dm³?', 'answer': f'{num(v / 1000, 3)} dm³',
            'key': f'1 dm³ = 1 L = 1000 mL; {v} mL = {num(v / 1000, 3)} dm³.',
            'distractors': [f'{num(v / 100, 3)} dm³', f'{num(v * 1000)} dm³', f'{num(v / 10, 3)} dm³']}


def precision_case(r):
    true = round(r.uniform(2.0, 5.0), 2)
    who = name(r)
    a = [round(true + r.uniform(-0.01, 0.01), 2) for _ in range(3)]
    off = round(r.uniform(0.3, 0.6), 2)
    b = [round(true + off + r.uniform(-0.01, 0.01), 2) for _ in range(3)]
    spread = round(r.uniform(0.2, 0.4), 2)
    c = [round(true - spread, 2), round(true + spread * 0.2, 2), round(true + spread, 2)]
    return {'stem': (f'The true mass of a sample is {true:.2f} g. Three students weighed it three times each.\n'
                     f'{who}: {", ".join(f"{x:.2f}" for x in a)} g\nStudent B: {", ".join(f"{x:.2f}" for x in b)} g\n'
                     f'Student C: {", ".join(f"{x:.2f}" for x in c)} g\n'
                     f'(i) Whose readings are both precise and accurate? (1 mark)\n(ii) Whose readings are precise but not accurate? (1 mark)\n'
                     f'(iii) Distinguish between precision and accuracy. (2 marks)'),
            'answer': f'(i) {who} (ii) Student B (iii) Precision is closeness of repeated readings to each other; accuracy is closeness to the true value.',
            'key': f'(i) {who}: readings close to each other and to {true:.2f} g (1). (ii) B: close together but about {off} g high (1). (iii) precision – agreement among measurements; accuracy – agreement with the true value (1 + 1).'}


CH1S1 = {
    'topic': 'matter and its properties',
    'terms': [('a homogeneous mixture', 'a mixture whose composition is uniform throughout'),
              ('a heterogeneous mixture', 'a mixture whose composition is not uniform throughout'),
              ('a compound', 'a substance formed when atoms of two or more elements combine in a fixed ratio'),
              ('an element', 'a substance that consists of only one kind of atom'),
              ('an intensive property', 'a property that does not depend on the quantity of matter present'),
              ('an extensive property', 'a property whose value depends on the quantity of matter present'),
              ('precision', 'the closeness of various measurements of the same quantity to each other'),
              ('accuracy', 'the agreement of a measured value with the true value'),
              ('the mole', 'the SI base unit of amount of substance'),
              ('the kelvin', 'the SI base unit of thermodynamic temperature')],
    'groups': [('a homogeneous mixture', ['air', 'sugar solution in water', 'brass', 'sea water (filtered)', 'petrol']),
               ('a heterogeneous mixture', ['a mixture of salt and sugar crystals', 'grains with pulses', 'muddy water', 'oil in water', 'sand and iron filings']),
               ('a compound', ['water', 'carbon dioxide', 'sodium chloride', 'glucose', 'ammonia']),
               ('an element', ['copper', 'oxygen gas', 'sulphur', 'graphite', 'mercury'])],
    'tf': (['The SI unit of amount of substance is the mole.',
            'Matter can exist in three physical states: solid, liquid and gas.',
            'The components of a mixture can be separated by physical methods.',
            'A compound cannot be separated into its elements by physical methods.',
            'In a homogeneous mixture the composition is uniform throughout.',
            'Colour, odour, melting point and density are physical properties.',
            'The SI unit of temperature is the kelvin.'],
           [('The SI unit of mass is the gram.', 'The SI unit of mass is the kilogram.'),
            ('In a compound the constituents are present in a variable ratio.', 'In a compound the constituents are present in a fixed ratio by mass.'),
            ('Burning of a candle involves only physical change.', 'Burning of a candle involves a chemical change (combustion) as well as melting.'),
            ('Liquids have a definite shape but no definite volume.', 'Liquids have a definite volume but no definite shape.'),
            ('The SI unit of length is the centimetre.', 'The SI unit of length is the metre.'),
            ('The properties of a compound are the same as those of its constituent elements.', 'The properties of a compound are different from those of its constituent elements.')]),
    'ar': [('Water is a compound and not a mixture.', 'The ratio of hydrogen to oxygen by mass in water is always 1 : 8.', 'a',
            'A fixed composition is what makes water a compound, so R explains A.'),
           ('A temperature on the kelvin scale can never be negative.', 'Absolute zero, 0 K, is the lowest possible temperature.', 'a',
            'Since nothing can be colder than 0 K, kelvin temperatures are zero or positive; R explains A.'),
           ('Air is a homogeneous mixture.', 'The composition of air is fixed at all places and heights.', 'c',
            'A is true, but the composition of air varies (e.g. with altitude and pollution), so R is false.')],
    'fams': [F('C2', 'D2', 'short', sigfig_count), F('C2', 'D2', 'numerical', sigfig_round),
             F('C3', 'D3', 'numerical', sigfig_calc), F('C2', 'D1', 'numerical', unit_temp),
             F('C3', 'D2', 'numerical', unit_conv), F('C4', 'D3', 'case', precision_case, kinds=('case',))],
    'qa': [('C4', 'D3', 'explain', 'A student says that milk is a pure substance because it looks the same throughout. Is the student right? Explain.',
            'No. Milk is a mixture (colloid) of fat, proteins, lactose and water; looking uniform does not make it a pure substance.',
            '1 mark: milk is a mixture; 1 mark: variable composition / components separable (e.g. cream separates on centrifuging).'),
           ('C4', 'D4', 'explain', 'Why is it necessary to express measured quantities using SI units in scientific work? Give two reasons.',
            'SI units are a single internationally agreed system, so results from different laboratories can be compared and converted without error; the units are related by powers of ten.',
            '1 mark each for two valid reasons (international agreement/comparability; decimal relations; defined base units).')],
}

# ---------------- ch01 st2 laws of chemical combination, atomic and molecular masses ----------------

ISOTOPES = [('chlorine', [(34.969, 75.77), (36.966, 24.23)], 35.45), ('boron', [(10.013, 19.9), (11.009, 80.1)], 10.81),
            ('copper', [(62.930, 69.17), (64.928, 30.83)], 63.55), ('lithium', [(6.015, 7.59), (7.016, 92.41)], 6.94),
            ('bromine', [(78.918, 50.69), (80.916, 49.31)], 79.90), ('gallium', [(68.926, 60.11), (70.925, 39.89)], 69.72)]


def avg_atomic_mass(r):
    el, iso, _ = r.choice(ISOTOPES)
    if r.random() < 0.5:
        a = round(iso[0][1] + r.uniform(-1.5, 1.5), 1)
        iso = [(iso[0][0], a), (iso[1][0], round(100 - a, 1))]
    m = sum(x * p / 100 for x, p in iso)
    parts = ' and '.join(f'{x} u ({p}%)' for x, p in iso)
    return {'stem': f'Naturally occurring {el} consists of two isotopes with masses {parts}. Calculate the average atomic mass of {el}.',
            'answer': f'{m:.2f} u', 'key': f'Average = Σ(fractional abundance × mass) = ' + ' + '.join(f'{p / 100:.4f} × {x}' for x, p in iso) + f' = {m:.2f} u.',
            'distractors': [f'{(iso[0][0] + iso[1][0]) / 2:.2f} u', f'{m + 0.5:.2f} u', f'{m - 0.4:.2f} u']}


def molecular_mass(r):
    f, comp, nm = r.choice(CMPD)
    m = M(comp)
    terms = ' + '.join(f'{n}({AM[e]})' if n > 1 else f'{AM[e]}' for e, n in comp.items())
    return {'stem': f'Calculate the molecular (formula) mass of {nm}, {f}. (Atomic masses: ' + ', '.join(f'{e} = {AM[e]}' for e in comp) + ' u)',
            'answer': f'{mstr(m)} u', 'key': f'{terms} = {mstr(m)} u.',
            'distractors': [f'{mstr(m + 16)} u', f'{mstr(m - AM[list(comp)[0]])} u', f'{mstr(m * 2)} u']}


MULT = [('carbon', 'oxygen', 12, [16, 32], ['CO', 'CO₂']), ('nitrogen', 'oxygen', 28, [16, 32, 48, 64, 80], ['N₂O', 'NO', 'N₂O₃', 'NO₂', 'N₂O₅']),
        ('hydrogen', 'oxygen', 2, [16, 32], ['H₂O', 'H₂O₂']), ('sulphur', 'oxygen', 32, [32, 48], ['SO₂', 'SO₃']),
        ('iron', 'oxygen', 112, [32, 48], ['FeO', 'Fe₂O₃'])]


def multiple_prop(r):
    a, b, fixed, masses, fs = r.choice(MULT)
    i, j = sorted(r.sample(range(len(masses)), 2))
    scale = r.choice([1, 2, 3, 5])
    m1, m2 = masses[i] * scale, masses[j] * scale
    g = math.gcd(masses[i], masses[j])
    ra, rb = masses[i] // g, masses[j] // g
    return {'stem': f'Two oxides of {a} contain {m1} g and {m2} g of {b} respectively combined with {fixed * scale} g of {a}. Show that these data illustrate the law of multiple proportions.',
            'answer': f'Masses of {b} combining with a fixed mass of {a} are in the ratio {ra} : {rb}, a simple whole-number ratio.',
            'key': f'Fixed mass of {a} = {fixed * scale} g; {m1} : {m2} = {ra} : {rb} (simple whole numbers), as in {fs[i]} and {fs[j]} – 2 marks.',
            'distractors': [f'{rb} : {ra}', f'{ra + 1} : {rb}', f'1 : 1']}


GAYLUSSAC = [('H₂(g) + Cl₂(g) → 2HCl(g)', 'hydrogen', 'hydrogen chloride', 1, 2, 'formed'), ('2H₂(g) + O₂(g) → 2H₂O(g)', 'oxygen', 'water vapour', 1, 2, 'formed'),
             ('N₂(g) + 3H₂(g) → 2NH₃(g)', 'nitrogen', 'ammonia', 1, 2, 'formed'), ('N₂(g) + 3H₂(g) → 2NH₃(g)', 'ammonia', 'hydrogen', 2, 3, 'required'),
             ('2CO(g) + O₂(g) → 2CO₂(g)', 'carbon monoxide', 'oxygen', 2, 1, 'required'), ('CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)', 'methane', 'oxygen', 1, 2, 'required'),
             ('H₂(g) + Cl₂(g) → 2HCl(g)', 'hydrogen chloride', 'chlorine', 2, 1, 'required')]


def gay_lussac(r):
    eq, a, b, ca, cb, verb = r.choice(GAYLUSSAC)
    v = r.choice([10, 20, 25, 40, 50, 60, 75, 100, 150, 200])
    ans = v * cb / ca
    q = f'what volume of {b} is formed from {v} mL of {a}' if verb == 'formed' else f'what volume of {b} is required to produce (or react with) {v} mL of {a}'
    if verb == 'required' and a in ('methane', 'carbon monoxide'):
        q = f'what volume of {b} is required to burn {v} mL of {a} completely'
    if verb == 'required' and a in ('ammonia', 'hydrogen chloride'):
        q = f'what volume of {b} is required to produce {v} mL of {a}'
    return {'stem': f'For the reaction {eq}, {q}? All volumes are measured at the same temperature and pressure.',
            'answer': f'{num(ans)} mL', 'key': f'By Gay-Lussac\'s law volumes react in the ratio of coefficients: {ca} : {cb}, so {v} × {cb}/{ca} = {num(ans)} mL.',
            'distractors': [f'{num(v * ca / cb)} mL', f'{num(v)} mL', f'{num(ans * 2)} mL']}


def conservation(r):
    who = name(r)
    m1 = round(r.uniform(5, 20), 1)
    m2 = round(r.uniform(5, 20), 1)
    p1 = round(r.uniform(2, m1 + m2 - 2), 1)
    p2 = round(m1 + m2 - p1, 1)
    return {'stem': f'In an experiment {who} reacts {m1} g of reactant A completely with {m2} g of reactant B in a closed flask to form {p1} g of product C and product D only. What mass of D is formed, and which law does the calculation use?',
            'answer': f'{p2} g; law of conservation of mass',
            'key': f'Mass of reactants = mass of products: {m1} + {m2} = {p1} + m(D), so m(D) = {p2} g (1 mark); law of conservation of mass (1 mark).',
            'distractors': [f'{round(m1 + m2 + p1, 1)} g', f'{round(m1 - p1 if m1 > p1 else p1 - m1, 1)} g', f'{round(p2 + 1, 1)} g']}


CH1S2 = {
    'topic': 'the laws of chemical combination',
    'terms': [('the law of conservation of mass', 'the law stating that matter can neither be created nor destroyed in a chemical reaction'),
              ('the law of definite proportions', 'the law stating that a given compound always contains exactly the same proportion of elements by weight'),
              ('the law of multiple proportions', 'the law stating that when two elements form more than one compound, the masses of one element that combine with a fixed mass of the other are in a small whole-number ratio'),
              ("Gay-Lussac's law of gaseous volumes", 'the law stating that gases combine or are produced in a chemical reaction in a simple ratio by volume at the same temperature and pressure'),
              ("Avogadro's law", 'the law stating that equal volumes of all gases at the same temperature and pressure contain equal numbers of molecules'),
              ('the atomic mass unit (u)', 'a mass exactly equal to one-twelfth of the mass of one carbon-12 atom'),
              ('average atomic mass', 'the mass of an element calculated from the masses of its isotopes weighted by their natural abundances')],
    'classify': False,
    'groups': [('a scientist associated with the law of conservation of mass', ['Antoine Lavoisier']),
               ('a scientist associated with the law of definite proportions', ['Joseph Proust']),
               ('a scientist associated with the law of multiple proportions', ['John Dalton']),
               ('a scientist associated with the law of gaseous volumes', ['Joseph Louis Gay-Lussac']),
               ('a scientist associated with equal volumes containing equal numbers of molecules', ['Lorenzo Avogadro'])],
    'tf': (["Dalton's atomic theory could explain the laws of chemical combination by mass.",
            "According to Dalton's theory, compounds are formed when atoms of different elements combine in a fixed ratio.",
            'Proust worked with natural and synthetic samples of cupric carbonate and found the same composition.',
            'One atomic mass unit is one-twelfth of the mass of a carbon-12 atom.',
            "Dalton's atomic theory could not explain the law of gaseous volumes."],
           [("Dalton's atomic theory explained the law of gaseous volumes.", "Dalton's atomic theory could not explain the law of gaseous volumes."),
            ('The law of multiple proportions was given by Lavoisier.', 'The law of multiple proportions was given by Dalton.'),
            ('Atomic mass unit is defined with respect to the hydrogen-1 atom.', 'The atomic mass unit is defined as one-twelfth of the mass of a carbon-12 atom.'),
            ('Gay-Lussac\'s law relates masses of reacting substances.', "Gay-Lussac's law relates volumes of reacting gases at the same temperature and pressure."),
            ('According to Avogadro, equal masses of gases contain equal numbers of molecules.', 'Equal volumes of gases at the same temperature and pressure contain equal numbers of molecules.')]),
    'ar': [('Hydrogen and oxygen form H₂O and H₂O₂; the masses of oxygen combining with 2 g of hydrogen are in the ratio 1 : 2.', 'When two elements form more than one compound, the masses of one element combining with a fixed mass of the other are in a simple whole-number ratio.', 'a',
            'This is the law of multiple proportions, which explains A.'),
           ('The average atomic mass of chlorine is 35.5 u.', 'Chlorine exists as two isotopes, ³⁵Cl and ³⁷Cl, in about 3 : 1 ratio.', 'a',
            'The weighted average of 35 and 37 in 3 : 1 ratio is about 35.5 u, so R explains A.')],
    'fams': [F('C3', 'D2', 'numerical', avg_atomic_mass), F('C2', 'D2', 'numerical', molecular_mass),
             F('C3', 'D3', 'explain', multiple_prop, marks=2), F('C3', 'D2', 'numerical', gay_lussac),
             F('C2', 'D2', 'numerical', conservation)],
    'qa': [('C4', 'D3', 'explain', '2 volumes of hydrogen react with 1 volume of oxygen to give 2 volumes of water vapour. Why could Dalton\'s atomic theory not explain this, and how did Avogadro resolve it?',
            'Dalton assumed atoms of gases (H, O) combine; 1 volume of oxygen giving 2 volumes of steam would need half-atoms. Avogadro proposed that gases exist as molecules (H₂, O₂) that can split, so 2H₂ + O₂ → 2H₂O.',
            '1 mark: the problem of splitting indivisible atoms; 1 mark: Avogadro\'s distinction between atoms and polyatomic molecules.'),
           ('C4', 'D4', 'explain', 'A sample of carbon dioxide made by burning charcoal and another made by heating limestone both contain 27.3% carbon by mass. Which law is illustrated, and why is this observation evidence that CO₂ is a compound?',
            'The law of definite proportions: a compound has the same composition by mass whatever its source, which is a defining feature of a compound (a mixture can vary).',
            '1 mark: law of definite proportions; 1 mark: fixed composition independent of source/method.'),
           ('C4', 'D5', 'long', 'State the postulates of Dalton\'s atomic theory. Explain, using one example each, how the theory accounts for the law of conservation of mass and the law of multiple proportions. Give one limitation of the theory.',
            'Postulates: matter is made of indivisible atoms; atoms of an element are identical in mass and properties; compounds form when atoms combine in fixed ratios; atoms are neither created nor destroyed in reactions. Conservation of mass: atoms are only rearranged (e.g. C + O₂ → CO₂). Multiple proportions: whole atoms combine, so CO and CO₂ have O in 1 : 2 ratio for fixed C. Limitation: cannot explain the law of gaseous volumes / atoms are divisible.',
            '2 marks postulates; 1 mark conservation example; 1 mark multiple proportions example; 1 mark limitation.')],
}

# ---------------- ch01 st3 mole concept, % composition, empirical formula ----------------

def moles_from_mass(r):
    f, comp, nm = r.choice(CMPD)
    m = M(comp)
    n = r.choice([0.1, 0.2, 0.25, 0.5, 1.5, 2, 2.5, 3, 0.05, 0.4])
    mass = n * m
    return {'stem': f'How many moles of {nm} ({f}) are present in {mstr(mass)} g of it? (Molar mass = {mstr(m)} g mol⁻¹)',
            'answer': f'{num(n, 3)} mol', 'key': f'n = mass / molar mass = {mstr(mass)} / {mstr(m)} = {num(n, 3)} mol.',
            'distractors': [f'{num(n * 2, 3)} mol', f'{num(n / 2, 3)} mol', f'{num(mass * m / 100, 2)} mol']}


def molecules(r):
    f, comp, nm = r.choice(CMPD)
    m = M(comp)
    mass = r.choice([1, 2, 5, 9, 10, 18, 22, 44, 50, 100]) * (1 if r.random() < 0.5 else m / 10)
    mass = round(mass, 1)
    n = mass / m
    N = n * NA
    atoms = N * sum(comp.values())
    return {'stem': f'Calculate the number of molecules and the total number of atoms in {mstr(mass)} g of {nm} ({f}). (Molar mass = {mstr(m)} g mol⁻¹, Nₐ = 6.022 × 10²³ mol⁻¹)',
            'answer': f'{sci(N)} molecules; {sci(atoms)} atoms',
            'key': f'n = {mstr(mass)}/{mstr(m)} = {sf(n)} mol (½); molecules = n × Nₐ = {sci(N)} (1); each molecule has {sum(comp.values())} atoms, so atoms = {sci(atoms)} (½).',
            'distractors': [f'{sci(N)} molecules; {sci(N)} atoms', f'{sci(n * NA * 2)} molecules; {sci(atoms * 2)} atoms', f'{sci(mass * NA)} molecules; {sci(mass * NA * sum(comp.values()))} atoms']}


def mass_of_atoms(r):
    e = r.choice(['C', 'Na', 'Mg', 'Fe', 'Ca', 'Al', 'Cu', 'Zn', 'S'])
    k = r.choice([1, 2, 3, 5, 0.5, 1.5, 2.5])
    N = k * NA
    mass = k * AM[e]
    return {'stem': f'What is the mass of {sci(N)} atoms of {e}? (Atomic mass of {e} = {AM[e]} u)', 'answer': f'{mstr(mass)} g',
            'key': f'{sci(N)} / 6.022 × 10²³ = {num(k)} mol; mass = {num(k)} × {AM[e]} = {mstr(mass)} g.',
            'distractors': [f'{mstr(AM[e])} g', f'{mstr(mass * 2)} g', f'{mstr(AM[e] / k)} g']}


def percent_comp(r):
    f, comp, nm = r.choice([c for c in CMPD if len(c[1]) >= 2])
    m = M(comp)
    e = r.choice(list(comp))
    p = AM[e] * comp[e] / m * 100
    return {'stem': f'Calculate the mass percentage of {e} in {nm} ({f}). (Atomic masses: ' + ', '.join(f'{x} = {AM[x]}' for x in comp) + ' u)',
            'answer': f'{p:.2f}%', 'key': f'Molar mass = {mstr(m)} g mol⁻¹; % {e} = {comp[e]} × {AM[e]} / {mstr(m)} × 100 = {p:.2f}%.',
            'distractors': [f'{AM[e] / m * 100:.2f}%' if comp[e] > 1 else f'{100 - p:.2f}%', f'{p / 2:.2f}%', f'{min(p * 1.5, 99):.2f}%']}


EF = [('C₂H₄', {'C': 1, 'H': 2}, 'CH₂', 28), ('C₆H₆', {'C': 1, 'H': 1}, 'CH', 78), ('C₆H₁₂O₆', {'C': 1, 'H': 2, 'O': 1}, 'CH₂O', 180),
      ('C₂H₄O₂', {'C': 1, 'H': 2, 'O': 1}, 'CH₂O', 60), ('H₂O₂', {'H': 1, 'O': 1}, 'HO', 34), ('C₂H₆', {'C': 1, 'H': 3}, 'CH₃', 30),
      ('N₂O₄', {'N': 1, 'O': 2}, 'NO₂', 92), ('C₄H₁₀', {'C': 2, 'H': 5}, 'C₂H₅', 58), ('C₃H₆', {'C': 1, 'H': 2}, 'CH₂', 42),
      ('C₂H₂', {'C': 1, 'H': 1}, 'CH', 26), ('C₈H₁₈', {'C': 4, 'H': 9}, 'C₄H₉', 114), ('P₄O₁₀', {'P': 2, 'O': 5}, 'P₂O₅', 284)]


def emp_formula(r):
    mf, ec, ef, Mm = r.choice(EF)
    em = M(ec)
    pct = {e: AM[e] * n / em * 100 for e, n in ec.items()}
    ps = ', '.join(f'{e} {pct[e]:.2f}%' for e in ec)
    k = round(Mm / em)
    others = [x[2] for x in EF if x[2] != ef]
    return {'stem': f'A compound contains {ps} by mass. Its molar mass is {Mm} g mol⁻¹. Find its empirical and molecular formulae.',
            'answer': f'Empirical formula {ef}; molecular formula {mf}',
            'key': f'Divide each % by atomic mass and by the smallest value: ' + ', '.join(f'{e} {pct[e]:.2f}/{AM[e]} = {pct[e] / AM[e]:.3f}' for e in ec) +
                   f' → ratio gives {ef} (empirical mass {mstr(em)}) (2 marks); n = {Mm}/{mstr(em)} = {k}, molecular formula {mf} (1 mark).',
            'distractors': [f'Empirical formula {ef}; molecular formula {ef}', f'Empirical formula {others[0]}; molecular formula {mf}', f'Empirical formula {mf}; molecular formula {ef}']}


def mol_from_emp(r):
    mf, ec, ef, Mm = r.choice(EF)
    em = M(ec)
    wrong = list({x[0] for x in EF if x[2] != ef})
    r.shuffle(wrong)
    return {'stem': f'The empirical formula of a compound is {ef} and its molar mass is {Mm} g mol⁻¹. What is its molecular formula?',
            'answer': mf, 'key': f'Empirical formula mass = {mstr(em)}; n = {Mm}/{mstr(em)} = {round(Mm / em)}; molecular formula = ({ef})ₙ = {mf}.',
            'distractors': wrong[:3]}


CH1S3 = {
    'topic': 'the mole concept',
    'terms': [('one mole', 'the amount of substance that contains as many particles as there are atoms in exactly 12 g of carbon-12'),
              ('the Avogadro constant', 'the number of elementary entities in one mole, 6.022 × 10²³ mol⁻¹'),
              ('molar mass', 'the mass of one mole of a substance expressed in grams'),
              ('the empirical formula', 'the formula that gives the simplest whole-number ratio of atoms of the elements in a compound'),
              ('the molecular formula', 'the formula that gives the exact number of each type of atom in a molecule'),
              ('formula mass', 'the sum of atomic masses of the atoms in the formula unit of an ionic compound')],
    'tf': (['One mole of any substance contains 6.022 × 10²³ elementary entities.',
            'The molar mass of a substance in g mol⁻¹ is numerically equal to its molecular mass in u.',
            'The molecular formula is a whole-number multiple of the empirical formula.',
            'Glucose and acetic acid have the same empirical formula, CH₂O.',
            'For ionic compounds such as NaCl we use formula mass instead of molecular mass.'],
           [('One mole of oxygen gas contains 6.022 × 10²³ atoms.', 'One mole of O₂ contains 6.022 × 10²³ molecules, i.e. 2 × 6.022 × 10²³ atoms.'),
            ('The empirical formula of benzene is C₆H₆.', 'The empirical formula of benzene is CH; C₆H₆ is its molecular formula.'),
            ('1 g of hydrogen gas and 1 g of oxygen gas contain the same number of molecules.', 'They contain different numbers of molecules because their molar masses (2 and 32 g mol⁻¹) differ.'),
            ('The molar mass of water is 18 u.', 'The molar mass of water is 18 g mol⁻¹; 18 u is the mass of one molecule.'),
            ('The empirical and molecular formulae of a compound can never be the same.', 'They can be the same, e.g. H₂O, CO₂ and CH₄.')]),
    'orders': [('increasing order of number of molecules in 10 g of each gas', ['CO₂ (44)', 'O₂ (32)', 'N₂ (28)', 'CH₄ (16)', 'H₂ (2)'],
                'For equal mass, n = m/M, so the gas with the smaller molar mass has more molecules.', '<'),
               ('increasing order of mass', ['1 mol of H₂', '1 mol of H₂O', '1 mol of O₂', '1 mol of CO₂', '1 mol of H₂SO₄'],
                'The mass of one mole equals the molar mass: 2 < 18 < 32 < 44 < 98 g.', '<')],
    'ar': [('The empirical formula of glucose is CH₂O.', 'The molecular formula of glucose is C₆H₁₂O₆, whose atoms are in the ratio 1 : 2 : 1.', 'a',
            'Dividing C₆H₁₂O₆ by 6 gives the simplest ratio CH₂O, so R explains A.'),
           ('18 g of water and 2 g of hydrogen gas contain the same number of molecules.', 'Both quantities are one mole of the substance.', 'a',
            'n = 18/18 = 1 mol and 2/2 = 1 mol, and one mole always has Nₐ molecules.'),
           ('One mole of NaCl contains 6.022 × 10²³ molecules.', 'NaCl is an ionic compound.', 'd',
            'A is false: NaCl has no molecules; one mole contains 6.022 × 10²³ formula units (Na⁺Cl⁻ pairs). R is true.')],
    'fams': [F('C2', 'D2', 'numerical', moles_from_mass), F('C3', 'D3', 'numerical', molecules, marks=2),
             F('C2', 'D2', 'numerical', mass_of_atoms), F('C2', 'D2', 'numerical', percent_comp),
             F('C3', 'D4', 'multi_step', emp_formula, kinds=('long5',)), F('C3', 'D3', 'short', mol_from_emp)],
    'qa': [('C4', 'D4', 'explain', 'Which contains more atoms: 1 g of Mg or 1 g of Ca? Justify without calculating the exact numbers. (Mg = 24, Ca = 40)',
            '1 g of Mg, because it has the smaller molar mass and so more moles (1/24 > 1/40) and therefore more atoms.',
            '1 mark: Mg; 1 mark: n = m/M is larger for smaller molar mass.'),
           ('C4', 'D3', 'explain', 'A hydrocarbon gives 3.38 g of CO₂ and 0.690 g of H₂O on complete combustion. How would you find its empirical formula? Outline the steps.',
            'Moles of C = moles of CO₂ = 3.38/44 = 0.0768; moles of H = 2 × 0.690/18 = 0.0767; ratio C : H = 1 : 1, so the empirical formula is CH.',
            '1 mark: C from CO₂ and H from H₂O (×2); 1 mark: ratio and empirical formula CH.')],
}

# ---------------- ch01 st4 stoichiometry and limiting reagent ----------------

RXN = [  # (equation, [(name, formula, coeff, M)] reactants, products)
    ('CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)', [('methane', 'CH₄', 1, 16), ('oxygen', 'O₂', 2, 32)], [('carbon dioxide', 'CO₂', 1, 44), ('water', 'H₂O', 2, 18)]),
    ('2H₂(g) + O₂(g) → 2H₂O(l)', [('hydrogen', 'H₂', 2, 2), ('oxygen', 'O₂', 1, 32)], [('water', 'H₂O', 2, 18)]),
    ('N₂(g) + 3H₂(g) → 2NH₃(g)', [('nitrogen', 'N₂', 1, 28), ('hydrogen', 'H₂', 3, 2)], [('ammonia', 'NH₃', 2, 17)]),
    ('CaCO₃(s) → CaO(s) + CO₂(g)', [('calcium carbonate', 'CaCO₃', 1, 100)], [('calcium oxide', 'CaO', 1, 56), ('carbon dioxide', 'CO₂', 1, 44)]),
    ('2Mg(s) + O₂(g) → 2MgO(s)', [('magnesium', 'Mg', 2, 24), ('oxygen', 'O₂', 1, 32)], [('magnesium oxide', 'MgO', 2, 40)]),
    ('Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g)', [('zinc', 'Zn', 1, 65), ('hydrogen chloride', 'HCl', 2, 36.5)], [('zinc chloride', 'ZnCl₂', 1, 136), ('hydrogen', 'H₂', 1, 2)]),
    ('C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(l)', [('propane', 'C₃H₈', 1, 44), ('oxygen', 'O₂', 5, 32)], [('carbon dioxide', 'CO₂', 3, 44), ('water', 'H₂O', 4, 18)]),
    ('C(s) + O₂(g) → CO₂(g)', [('carbon', 'C', 1, 12), ('oxygen', 'O₂', 1, 32)], [('carbon dioxide', 'CO₂', 1, 44)]),
    ('2KClO₃(s) → 2KCl(s) + 3O₂(g)', [('potassium chlorate', 'KClO₃', 2, 122.5)], [('potassium chloride', 'KCl', 2, 74.5), ('oxygen', 'O₂', 3, 32)]),
    ('Fe₂O₃(s) + 3CO(g) → 2Fe(s) + 3CO₂(g)', [('iron(III) oxide', 'Fe₂O₃', 1, 160), ('carbon monoxide', 'CO', 3, 28)], [('iron', 'Fe', 2, 56), ('carbon dioxide', 'CO₂', 3, 44)]),
]


def stoich_mass(r):
    eq, rs, ps = r.choice(RXN)
    a = r.choice(rs)
    b = r.choice(ps)
    n_a = r.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5]) * a[2]
    ma = n_a * a[3]
    mb = n_a * b[2] / a[2] * b[3]
    who = name(r)
    return {'stem': f'{who} uses the reaction {eq}. What mass of {b[0]} is formed from {mstr(ma)} g of {a[0]} reacting completely? (Molar masses: {a[1]} = {mstr(a[3])}, {b[1]} = {mstr(b[3])} g mol⁻¹)',
            'answer': f'{mstr(mb)} g', 'key': f'n({a[1]}) = {mstr(ma)}/{mstr(a[3])} = {num(n_a, 3)} mol (1); mole ratio {a[1]} : {b[1]} = {a[2]} : {b[2]}, so n({b[1]}) = {num(n_a * b[2] / a[2], 3)} mol; mass = {mstr(mb)} g (1).',
            'distractors': [f'{mstr(n_a * b[3])} g', f'{mstr(ma * b[3] / a[3])} g', f'{mstr(mb * 2)} g']}


def limiting(r):
    eq, rs, ps = r.choice([x for x in RXN if len(x[1]) == 2])
    a, b = rs
    p = ps[0]
    na = r.choice([1, 2, 3, 4, 5, 6]) * a[2] / 2
    nb = r.choice([1, 2, 3, 4, 5, 6]) * b[2] / 2
    if abs(na / a[2] - nb / b[2]) < 1e-9:
        nb += b[2] / 2
    lim = a if na / a[2] < nb / b[2] else b
    nl = na if lim is a else nb
    np_ = nl / lim[2] * p[2]
    mass_p = np_ * p[3]
    exc = b if lim is a else a
    nexc_left = (nb if lim is a else na) - nl / lim[2] * exc[2]
    return {'stem': f'For the reaction {eq}, {num(na * a[3], 2)} g of {a[0]} is mixed with {num(nb * b[3], 2)} g of {b[0]}. Identify the limiting reagent and calculate the mass of {p[0]} formed. (Molar masses: {a[1]} {mstr(a[3])}, {b[1]} {mstr(b[3])}, {p[1]} {mstr(p[3])} g mol⁻¹)',
            'answer': f'{cap(lim[0])} is the limiting reagent; {mstr(mass_p)} g of {p[0]}',
            'key': f'n({a[1]}) = {num(na, 3)} mol, n({b[1]}) = {num(nb, 3)} mol (1). Dividing by coefficients: {num(na / a[2], 3)} vs {num(nb / b[2], 3)}, so {lim[1]} is limiting (1). '
                   f'n({p[1]}) = {num(np_, 3)} mol → {mstr(mass_p)} g (1). {num(nexc_left, 3)} mol of {exc[1]} remains unreacted.',
            'distractors': [f'{cap(exc[0])} is the limiting reagent; {mstr((nb if lim is a else na) / exc[2] * p[2] * p[3])} g of {p[0]}',
                            f'{cap(lim[0])} is the limiting reagent; {mstr(nl * p[3])} g of {p[0]}',
                            f'{cap(exc[0])} is the limiting reagent; {mstr(mass_p)} g of {p[0]}']}


def gas_volume(r):
    eq, rs, ps = r.choice([x for x in RXN if any(s[1] in ('CO₂', 'O₂', 'H₂', 'NH₃') for s in x[2])])
    g = [s for s in ps if s[1] in ('CO₂', 'O₂', 'H₂', 'NH₃')][0]
    a = rs[0]
    na = r.choice([0.5, 1, 2, 3, 4]) * a[2]
    v = na * g[2] / a[2] * 22.7
    return {'stem': f'Using {eq}, calculate the volume of {g[0]} at STP produced from {mstr(na * a[3])} g of {a[0]}. (Molar mass of {a[1]} = {mstr(a[3])} g mol⁻¹; molar volume at STP = 22.7 L mol⁻¹)',
            'answer': f'{sf(v, 3)} L', 'key': f'n({a[1]}) = {num(na, 3)} mol; n({g[1]}) = {num(na * g[2] / a[2], 3)} mol; V = {num(na * g[2] / a[2], 3)} × 22.7 = {sf(v, 3)} L.',
            'distractors': [sf(v * 2, 3) + ' L', sf(na * 22.7, 3) + ' L' if g[2] != a[2] else sf(v / 2, 3) + ' L', sf(v * 1.5, 3) + ' L']}


def stoich_case(r):
    who = name(r)
    m_caco3 = r.choice([10, 20, 25, 40, 50])
    purity = r.choice([80, 85, 90, 95])
    pure = m_caco3 * purity / 100
    n = pure / 100
    return {'stem': (f'{who} heats {m_caco3} g of a limestone sample that is {purity}% CaCO₃ by mass (the impurities do not decompose). CaCO₃(s) → CaO(s) + CO₂(g). (Ca = 40, C = 12, O = 16)\n'
                     f'(i) What mass of pure CaCO₃ is present? (1 mark)\n(ii) How many moles of CO₂ are released? (1 mark)\n(iii) What mass of CaO is formed, and what is the total loss in mass of the sample? (2 marks)'),
            'answer': f'(i) {num(pure, 2)} g (ii) {num(n, 4)} mol (iii) CaO {num(n * 56, 3)} g; loss in mass {num(n * 44, 3)} g',
            'key': f'(i) {purity}% of {m_caco3} g = {num(pure, 2)} g (1). (ii) {num(pure, 2)}/100 = {num(n, 4)} mol CO₂ (1). (iii) CaO = {num(n, 4)} × 56 = {num(n * 56, 3)} g (1); loss = mass of CO₂ = {num(n * 44, 3)} g (1).'}


CH1S4 = {
    'topic': 'stoichiometry',
    'terms': [('stoichiometry', 'the calculation of the masses (and sometimes volumes) of reactants and products involved in a chemical reaction'),
              ('the limiting reagent', 'the reactant that is completely consumed first and so limits the amount of product formed'),
              ('the excess reagent', 'the reactant that is left over after the reaction is complete'),
              ('stoichiometric coefficients', 'the numbers placed before formulae in a balanced equation that give the mole ratio of reacting species'),
              ('a balanced chemical equation', 'an equation in which the number of atoms of each element is the same on both sides')],
    'tf': (['The coefficients in a balanced equation give the ratio of moles of reactants and products.',
            'The amount of product formed is decided by the limiting reagent.',
            'A balanced chemical equation obeys the law of conservation of mass.',
            'For gases at the same temperature and pressure the coefficients also give the ratio of volumes.'],
           [('The reactant present in the smaller mass is always the limiting reagent.', 'The limiting reagent is found by comparing moles divided by coefficients, not masses.'),
            ('Coefficients in a balanced equation give the ratio of masses of the reactants.', 'Coefficients give the mole ratio, not the mass ratio.'),
            ('In 2H₂ + O₂ → 2H₂O, 2 g of hydrogen reacts with 32 g of oxygen.', '2 g of hydrogen (1 mol) reacts with 16 g of oxygen (0.5 mol).'),
            ('The excess reagent is used up completely in a reaction.', 'The limiting reagent is used up completely; some excess reagent is left over.')]),
    'ar': [('In the reaction N₂ + 3H₂ → 2NH₃, if 28 g of N₂ and 2 g of H₂ are mixed, H₂ is the limiting reagent.', 'H₂ is needed in three times the number of moles of N₂, but only 1 mol of H₂ is present for 1 mol of N₂.', 'a',
            '1 mol of N₂ needs 3 mol of H₂; only 1 mol of H₂ is available, so H₂ runs out first.'),
           ('A balanced equation has the same number of molecules on both sides.', 'A balanced equation has the same number of atoms of each element on both sides.', 'd',
            'A is false (e.g. 2H₂ + O₂ → 2H₂O has 3 molecules on the left, 2 on the right); R is true.')],
    'fams': [F('C3', 'D2', 'numerical', stoich_mass), F('C3', 'D4', 'multi_step', limiting, kinds=('long5',)),
             F('C3', 'D3', 'numerical', gas_volume, marks=2), F('C4', 'D3', 'case', stoich_case, kinds=('case',))],
    'qa': [('C4', 'D4', 'explain', 'In an industry 2.00 × 10³ g of N₂ is mixed with 1.00 × 10³ g of H₂ to make ammonia. Without full calculation, explain which reactant is limiting and why the yield is quoted in terms of it.',
            'n(N₂) = 2000/28 ≈ 71.4 mol needs 214 mol of H₂; available H₂ = 1000/2 = 500 mol, so N₂ is limiting; the product amount is fixed by the reactant that runs out.',
            '1 mark: N₂ limiting with mole comparison; 1 mark: product depends on the limiting reagent.'),
           ('C4', 'D5', 'long', 'Dioxygen is prepared by heating potassium chlorate: 2KClO₃ → 2KCl + 3O₂. (a) Calculate the mass of KClO₃ needed to give 4.8 g of O₂. (b) What volume does this oxygen occupy at STP (22.7 L mol⁻¹)? (c) If only 3.6 g of O₂ is collected, what is the percentage yield? (K = 39, Cl = 35.5, O = 16)',
            '(a) n(O₂) = 0.15 mol; n(KClO₃) = 0.10 mol; mass = 12.25 g. (b) 0.15 × 22.7 = 3.41 L. (c) 3.6/4.8 × 100 = 75%.',
            '(a) 2 marks (moles of O₂ and ratio 2 : 3, mass 12.25 g); (b) 1.5 marks; (c) 1.5 marks.')],
}

# ---------------- ch01 st5 concentration terms ----------------

SOLUTES = [('NaOH', 40), ('NaCl', 58.5), ('glucose (C₆H₁₂O₆)', 180), ('urea (NH₂CONH₂)', 60), ('KCl', 74.5),
           ('Na₂CO₃', 106), ('H₂SO₄', 98), ('sucrose (C₁₂H₂₂O₁₁)', 342), ('KOH', 56), ('oxalic acid dihydrate (H₂C₂O₄·2H₂O)', 126)]


def molarity(r):
    s, m = r.choice(SOLUTES)
    n = r.choice([0.05, 0.1, 0.2, 0.25, 0.5, 0.75, 1.0])
    V = r.choice([100, 200, 250, 500, 1000])
    mass = n * m * V / 1000
    who = name(r)
    return {'stem': f'{who} dissolves {num(mass, 3)} g of {s} in water and makes the solution up to {V} mL in a volumetric flask. Calculate the molarity. (Molar mass = {num(m)} g mol⁻¹)',
            'answer': f'{num(n, 3)} M', 'key': f'n = {num(mass, 3)}/{num(m)} = {num(n * V / 1000, 4)} mol; M = n/V(L) = {num(n * V / 1000, 4)}/{V / 1000:g} = {num(n, 3)} mol L⁻¹.',
            'distractors': [f'{num(n * V / 1000, 4)} M', f'{num(n * 10, 3)} M', f'{num(n / 2, 3)} M']}


def molality(r):
    s, m = r.choice(SOLUTES)
    mass = r.choice([2, 3, 4.5, 5, 6, 9, 10, 18, 20])
    w = r.choice([100, 200, 250, 500])
    b = mass / m / (w / 1000)
    return {'stem': f'Calculate the molality of a solution containing {mass} g of {s} in {w} g of water. (Molar mass = {num(m)} g mol⁻¹)',
            'answer': f'{sf(b, 3)} mol kg⁻¹', 'key': f'n = {mass}/{num(m)} = {sf(mass / m, 3)} mol; m = n / mass of solvent (kg) = {sf(mass / m, 3)}/{w / 1000:g} = {sf(b, 3)} mol kg⁻¹.',
            'distractors': [f'{sf(mass / m, 3)} mol kg⁻¹', f'{sf(b * 10, 3)} mol kg⁻¹', f'{sf(mass / m / ((w + mass) / 1000), 3)} mol kg⁻¹' if abs(mass / m / ((w + mass) / 1000) - b) / b > 0.02 else f'{sf(b / 2, 3)} mol kg⁻¹']}


def mole_fraction(r):
    s, m = r.choice(SOLUTES[:4] + [('ethanol (C₂H₅OH)', 46), ('methanol (CH₃OH)', 32)])
    ns = r.choice([0.1, 0.2, 0.25, 0.5, 1])
    nw = r.choice([2, 4, 5, 10])
    xs = ns / (ns + nw)
    return {'stem': f'A solution is made by mixing {num(ns * m, 3)} g of {s} with {nw * 18} g of water. Calculate the mole fraction of the solute. (Molar mass of solute = {num(m)} g mol⁻¹, water = 18 g mol⁻¹)',
            'answer': f'{xs:.3f}', 'key': f'n(solute) = {num(ns, 3)} mol, n(water) = {nw} mol; x = {num(ns, 3)}/({num(ns, 3)} + {nw}) = {xs:.3f}.',
            'distractors': [f'{ns / nw:.3f}', f'{1 - xs:.3f}', f'{ns * m / (ns * m + nw * 18):.3f}']}


def mass_percent(r):
    a = r.choice([5, 10, 12, 15, 20, 25, 30])
    b = r.choice([45, 70, 80, 95, 100, 150, 200])
    p = a / (a + b) * 100
    s = r.choice(['sodium chloride', 'sugar', 'potassium nitrate', 'copper sulphate'])
    return {'stem': f'{a} g of {s} is dissolved in {b} g of water. What is the mass percentage of {s} in the solution?',
            'answer': f'{p:.2f}%', 'key': f'Mass % = mass of solute / mass of solution × 100 = {a}/({a} + {b}) × 100 = {p:.2f}%.',
            'distractors': [f'{a / b * 100:.2f}%', f'{100 - p:.2f}%', f'{a / (a + b):.2f}%']}


def dilution(r):
    M1 = r.choice([0.5, 1, 2, 5, 6, 10, 12])
    M2 = r.choice([x for x in [0.1, 0.2, 0.25, 0.5, 1] if x < M1])
    V2 = r.choice([100, 250, 500, 1000])
    V1 = M2 * V2 / M1
    acid = r.choice(['HCl', 'H₂SO₄', 'HNO₃', 'NaOH'])
    return {'stem': f'What volume of {M1} M {acid} must be diluted with water to prepare {V2} mL of {M2} M {acid}?', 'answer': f'{num(V1, 2)} mL',
            'key': f'M₁V₁ = M₂V₂ → V₁ = {M2} × {V2}/{M1} = {num(V1, 2)} mL; dilute to {V2} mL.',
            'distractors': [f'{num(M1 * V2 / M2, 2)} mL', f'{num(V2 - V1, 2)} mL', f'{num(V1 * 2, 2)} mL']}


def molarity_density(r):
    acid, m, pct, d = r.choice([('H₂SO₄', 98, 98, 1.84), ('HNO₃', 63, 69, 1.41), ('HCl', 36.5, 36, 1.18), ('NH₃', 17, 28, 0.90), ('H₂SO₄', 98, 50, 1.40)])
    Mo = pct * d * 10 / m
    return {'stem': f'A commercial sample of {acid} is {pct}% by mass and has a density of {d} g mL⁻¹. Calculate its molarity. (Molar mass = {m} g mol⁻¹)',
            'answer': f'{sf(Mo, 3)} M', 'key': f'Take 100 g solution: {pct} g {acid} = {sf(pct / m, 3)} mol (1); volume = 100/{d} = {sf(100 / d, 3)} mL (1); M = {sf(pct / m, 3)} × 1000/{sf(100 / d, 3)} = {sf(Mo, 3)} mol L⁻¹ (1).',
            'distractors': [f'{sf(pct / m * 10, 3)} M', f'{sf(Mo / d, 3)} M', f'{sf(Mo * 1.15, 3)} M']}


CH1S5 = {
    'topic': 'concentration terms',
    'terms': [('molarity', 'the number of moles of solute in one litre of solution'),
              ('molality', 'the number of moles of solute per kilogram of solvent'),
              ('mole fraction', 'the ratio of the number of moles of a component to the total number of moles of all components'),
              ('mass per cent', 'the mass of solute in grams per 100 g of solution'),
              ('a standard solution', 'a solution whose concentration is accurately known')],
    'tf': (['Molality does not change with temperature.', 'The sum of the mole fractions of all components of a solution is 1.',
            'Molarity decreases slightly when a solution is heated because its volume increases.',
            'Molarity is expressed in mol L⁻¹.'],
           [('Molality depends on temperature because volume changes with temperature.', 'Molality depends on masses only, so it is independent of temperature.'),
            ('Molarity is the number of moles of solute per kilogram of solvent.', 'Molarity is the number of moles of solute per litre of solution.'),
            ('A 1 M solution and a 1 m aqueous solution of NaCl have exactly the same composition.', 'They differ: 1 M has 1 mol in 1 L of solution, 1 m has 1 mol in 1 kg of solvent.'),
            ('Mole fraction has the unit mol kg⁻¹.', 'Mole fraction is a ratio and has no unit.')]),
    'ar': [('Molality is preferred over molarity for work at different temperatures.', 'Molality is defined using mass of solvent, which does not change with temperature.', 'a',
            'Mass is independent of temperature, so molality stays constant; R explains A.'),
           ('The molarity of a solution changes with temperature.', 'The volume of a solution changes with temperature.', 'a',
            'Molarity is moles per litre of solution, so a change in volume changes molarity.')],
    'fams': [F('C2', 'D2', 'numerical', molarity), F('C2', 'D2', 'numerical', molality), F('C3', 'D3', 'numerical', mole_fraction),
             F('C2', 'D1', 'numerical', mass_percent), F('C3', 'D2', 'numerical', dilution),
             F('C4', 'D4', 'multi_step', molarity_density, kinds=('long5',))],
    'qa': [('C4', 'D3', 'explain', 'A student prepares 0.1 M NaOH at 15 °C and uses it in a titration at 35 °C. Would its molarity at 35 °C be the same? Which concentration term would avoid this problem?',
            'No; the solution expands on warming, so the molarity falls slightly. Molality (or mole fraction/mass per cent) is independent of temperature.',
            '1 mark: molarity decreases with temperature (volume increases); 1 mark: molality is temperature independent.')],
}

# ---------------- ch02 st1 subatomic particles, Thomson and Rutherford ----------------

ELEM = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr']
ENAME = ['hydrogen', 'helium', 'lithium', 'beryllium', 'boron', 'carbon', 'nitrogen', 'oxygen', 'fluorine', 'neon', 'sodium',
         'magnesium', 'aluminium', 'silicon', 'phosphorus', 'sulphur', 'chlorine', 'argon', 'potassium', 'calcium', 'scandium',
         'titanium', 'vanadium', 'chromium', 'manganese', 'iron', 'cobalt', 'nickel', 'copper', 'zinc', 'gallium', 'germanium',
         'arsenic', 'selenium', 'bromine', 'krypton']
SPECIES = [('C', 6, 12, 0), ('C', 6, 14, 0), ('O', 8, 16, -2), ('Na', 11, 23, 1), ('Mg', 12, 24, 2), ('Al', 13, 27, 3),
           ('Cl', 17, 35, -1), ('Cl', 17, 37, 0), ('K', 19, 39, 1), ('Ca', 20, 40, 2), ('Fe', 26, 56, 3), ('Fe', 26, 56, 2),
           ('Br', 35, 80, -1), ('N', 7, 14, -3), ('S', 16, 32, -2), ('F', 9, 19, -1), ('P', 15, 31, 0), ('Zn', 30, 65, 2),
           ('U', 92, 238, 0), ('Cu', 29, 63, 2), ('H', 1, 2, 0), ('H', 1, 3, 0), ('Ar', 18, 40, 0), ('Li', 3, 7, 1)]
SUPD = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
SUBD = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def ion(sym, A, q, Z=None):
    ch = '' if q == 0 else (('' if abs(q) == 1 else str(abs(q))) + ('+' if q > 0 else '−'))
    return f'{str(A).translate(SUPD)}{sym}{ch.translate(SUPD).replace("+", "⁺").replace("−", "⁻")}'


def pne(r):
    sym, Z, A, q = r.choice(SPECIES)
    e = Z - q
    s = ion(sym, A, q)
    return {'stem': f'Give the number of protons, neutrons and electrons in {s} (atomic number of {sym} = {Z}).',
            'answer': f'p = {Z}, n = {A - Z}, e = {e}', 'key': f'Protons = Z = {Z}; neutrons = A − Z = {A} − {Z} = {A - Z}; electrons = Z − charge = {e}.',
            'distractors': [f'p = {Z}, n = {A - Z}, e = {Z}' if q else f'p = {Z}, n = {A}, e = {Z}', f'p = {A - Z}, n = {Z}, e = {e}', f'p = {A}, n = {Z}, e = {e}']}


def isotope_kind(r):
    pairs = [('¹²C and ¹⁴C', 'isotopes', 'same Z (6), different A'), ('³⁵Cl and ³⁷Cl', 'isotopes', 'same Z (17), different A'),
             ('¹H and ³H', 'isotopes', 'same Z (1), different A'), ('⁴⁰Ar and ⁴⁰Ca', 'isobars', 'same A (40), different Z'),
             ('¹⁴C and ¹⁴N', 'isobars', 'same A (14), different Z'), ('⁴⁰K and ⁴⁰Ca', 'isobars', 'same A (40), different Z'),
             ('¹⁴C and ¹⁶O', 'isotones', 'both have 8 neutrons'), ('Na⁺ and Ne', 'isoelectronic species', 'both have 10 electrons'),
             ('O²⁻ and F⁻', 'isoelectronic species', 'both have 10 electrons'), ('K⁺ and Cl⁻', 'isoelectronic species', 'both have 18 electrons'),
             ('²³⁵U and ²³⁸U', 'isotopes', 'same Z (92), different A'), ('³H and ³He', 'isobars', 'same A (3), different Z')]
    p, k, why = r.choice(pairs)
    wrong = [x for x in ['isotopes', 'isobars', 'isotones', 'isoelectronic species', 'allotropes'] if x != k]
    return mcq(f'The pair {p} are best described as …', k, r.sample(wrong, 3), f'{cap(k)}: {why}.', r)


CH2S1 = {
    'topic': 'subatomic particles and early atomic models',
    'terms': [('cathode rays', 'streams of negatively charged particles that travel from the cathode to the anode in a discharge tube'),
              ('canal rays', 'positively charged particles produced in a discharge tube that move towards the cathode'),
              ('the atomic number', 'the number of protons in the nucleus of an atom'),
              ('the mass number', 'the total number of protons and neutrons in the nucleus'),
              ('isotopes', 'atoms of the same element with the same atomic number but different mass numbers'),
              ('isobars', 'atoms of different elements with the same mass number but different atomic numbers'),
              ('nucleons', 'the protons and neutrons present in the nucleus')],
    'classify': False,
    'groups': [('a discovery or result of J.J. Thomson', ['the charge-to-mass ratio of the electron', 'the plum pudding model of the atom']),
               ('a discovery or result of Rutherford', ['the nuclear model of the atom', 'the α-particle scattering experiment with gold foil']),
               ('a discovery of James Chadwick', ['the neutron, by bombarding beryllium with α-particles']),
               ('a result of R.A. Millikan', ['the charge on the electron from the oil drop experiment'])],
    'tf': (['Most α-particles passed through the gold foil undeflected.',
            'Thomson\'s model could explain the overall neutrality of the atom.',
            'The neutron was discovered by Chadwick in 1932.',
            'Rutherford\'s model could not explain the stability of the atom.',
            'Very few α-particles were deflected by nearly 180°.'],
           [('Most α-particles were deflected through large angles by the gold foil.', 'Most α-particles passed through undeflected; only a few were deflected through large angles.'),
            ('Rutherford\'s model explains the stability of an atom.', 'According to electromagnetic theory a revolving electron should radiate energy and spiral into the nucleus, so the model cannot explain stability.'),
            ('Canal rays have the same e/m value for all gases.', 'The e/m of canal-ray particles depends on the gas in the tube.'),
            ('The mass of a proton is about equal to the mass of an electron.', 'A proton is about 1840 times heavier than an electron.'),
            ('In Thomson\'s model the positive charge is concentrated in a small nucleus.', 'In Thomson\'s model the positive charge is spread uniformly over a sphere with electrons embedded in it.')]),
    'features': {'intro': 'An observation from an experiment is:', 'q': 'Which atomic model or conclusion does it support',
                 'items': [('Rutherford\'s nuclear model', ['most of the space in the atom is empty', 'the positive charge and most of the mass are concentrated in a tiny nucleus', 'a few α-particles bounce back from a thin gold foil']),
                           ('Thomson\'s plum pudding model', ['the positive charge is spread uniformly through the atom', 'electrons are embedded like seeds in a watermelon', 'mass is assumed to be distributed uniformly']),
                           ('Bohr\'s model', ['electrons revolve in fixed circular orbits of definite energy', 'energy is emitted only when an electron jumps from a higher to a lower orbit', 'the angular momentum of the electron is quantised'])]},
    'ar': [('Cathode rays are deflected towards the positive plate in an electric field.', 'Cathode rays consist of negatively charged particles.', 'a', 'Negative particles are attracted by a positive plate.'),
           ('Rutherford\'s model failed to explain the stability of the atom.', 'An accelerating charged particle should emit electromagnetic radiation and lose energy.', 'a',
            'An electron revolving round the nucleus would lose energy and spiral into it, so R explains A.')],
    'fams': [F('C2', 'D2', 'short', pne), F('C2', 'D2', 'mcq', isotope_kind), ],
    'qa': [('C3', 'D3', 'explain', 'In a discharge tube the charge-to-mass ratio of cathode-ray particles is the same whatever gas fills the tube or whatever metal the cathode is made of. What does this show? How do canal rays differ in this respect?',
            'Electrons are a basic constituent of all atoms (e/mₑ = 1.758820 × 10¹¹ C kg⁻¹). The e/m of canal-ray particles depends on the gas, since they are positive ions of that gas.',
            '1 mark: same e/m ⇒ electrons present in all atoms; 1 mark: canal-ray e/m depends on the gas (lightest from H₂ = proton).'),
           ('C4', 'D4', 'explain', 'If the gold foil in Rutherford\'s experiment were replaced by a much thicker foil of a lighter metal such as aluminium, how would you expect the results to change? Reason it out.',
            'Fewer large-angle deflections per atom, since the aluminium nucleus has a much smaller positive charge (Z = 13 vs 79); a thicker foil would also stop more α-particles and cause multiple scattering.',
            '1 mark: smaller nuclear charge gives weaker repulsion and fewer back-scattered particles; 1 mark: thickness effect / multiple scattering.')],
}

# ---------------- ch02 st2 EM radiation, Planck, photoelectric effect ----------------

h = 6.626e-34
c = 3.0e8


def nu_lambda(r):
    lam = r.choice([400, 450, 500, 550, 589, 600, 650, 700, 250, 300])
    nu = c / (lam * 1e-9)
    wn = 1 / (lam * 1e-9)
    src = 'a sodium lamp' if lam == 589 else r.choice(['a spectral lamp', 'an LED', 'a laser'])
    return {'stem': f'Light of wavelength {lam} nm is emitted by {src}. Calculate its frequency and wavenumber. (c = 3.0 × 10⁸ m s⁻¹)',
            'answer': f'ν = {sci(nu)} s⁻¹; ν̄ = {sci(wn)} m⁻¹',
            'key': f'ν = c/λ = 3.0 × 10⁸ / {lam} × 10⁻⁹ = {sci(nu)} Hz (1); ν̄ = 1/λ = {sci(wn)} m⁻¹ (1).',
            'distractors': [f'ν = {sci(nu / 10)} s⁻¹; ν̄ = {sci(wn)} m⁻¹', f'ν = {sci(nu)} s⁻¹; ν̄ = {sci(wn / 100)} m⁻¹', f'ν = {sci(lam * 1e-9 / c)} s⁻¹; ν̄ = {sci(wn)} m⁻¹']}


def photon_energy(r):
    lam = r.choice([200, 250, 300, 400, 450, 500, 600, 700])
    E = h * c / (lam * 1e-9)
    n = r.choice([None, 1])
    if n:
        Emol = E * NA / 1000
        return {'stem': f'Calculate the energy of one mole of photons of radiation of wavelength {lam} nm. (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, Nₐ = 6.022 × 10²³ mol⁻¹)',
                'answer': f'{sf(Emol, 3)} kJ mol⁻¹', 'key': f'E per photon = hc/λ = {sci(E)} J (1); × Nₐ = {sci(E * NA)} J mol⁻¹ = {sf(Emol, 3)} kJ mol⁻¹ (1).',
                'distractors': [f'{sf(Emol / 10, 3)} kJ mol⁻¹', f'{sf(Emol * 10, 3)} kJ mol⁻¹', f'{sci(E)} kJ mol⁻¹']}
    return {'stem': f'What is the energy of a photon of light of wavelength {lam} nm? (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹)',
            'answer': f'{sci(E)} J', 'key': f'E = hc/λ = (6.626 × 10⁻³⁴ × 3.0 × 10⁸)/({lam} × 10⁻⁹) = {sci(E)} J.',
            'distractors': [sci(E * 10) + ' J', sci(E / 10) + ' J', sci(E * 1e-9) + ' J']}


METALS_W = [('sodium', 2.3), ('potassium', 2.25), ('lithium', 2.42), ('magnesium', 3.7), ('copper', 4.8), ('silver', 4.3), ('caesium', 1.9), ('zinc', 4.3)]


def photoelectric(r):
    met, W = r.choice(METALS_W)
    lam = r.choice([150, 180, 200, 220, 250, 300, 350, 400, 450])
    E_eV = h * c / (lam * 1e-9) / 1.602e-19
    if E_eV <= W + 0.2:
        raise ValueError
    ke = E_eV - W
    return {'stem': f'The work function of {met} is {W} eV. Light of wavelength {lam} nm falls on its surface. Calculate the kinetic energy of the ejected electrons in eV. (hc = 1240 eV nm, approximately)',
            'answer': f'{ke:.2f} eV', 'key': f'Photon energy = 1240/{lam} = {1240 / lam:.2f} eV (1); KE = hν − W₀ = {1240 / lam:.2f} − {W} = {1240 / lam - W:.2f} eV (1).',
            'distractors': [f'{1240 / lam:.2f} eV', f'{1240 / lam + W:.2f} eV', f'{W:.2f} eV']}


def threshold(r):
    met, W = r.choice(METALS_W)
    lam0 = 1240 / W
    nu0 = W * 1.602e-19 / h
    return {'stem': f'The work function of {met} is {W} eV. Calculate its threshold frequency and threshold wavelength. (h = 6.626 × 10⁻³⁴ J s, 1 eV = 1.602 × 10⁻¹⁹ J)',
            'answer': f'ν₀ = {sci(nu0)} s⁻¹; λ₀ = {lam0:.0f} nm',
            'key': f'W₀ = hν₀ ⇒ ν₀ = {W} × 1.602 × 10⁻¹⁹ / 6.626 × 10⁻³⁴ = {sci(nu0)} s⁻¹ (1); λ₀ = c/ν₀ = {lam0:.0f} nm (1).'}


CH2S2 = {
    'topic': 'electromagnetic radiation and quantum theory',
    'terms': [('a quantum', 'the smallest quantity of energy that can be emitted or absorbed in the form of electromagnetic radiation'),
              ('the photoelectric effect', 'the ejection of electrons from a metal surface when light of suitable frequency falls on it'),
              ('the threshold frequency', 'the minimum frequency of light needed to eject electrons from a given metal surface'),
              ('the work function', 'the minimum energy needed to remove an electron from the surface of a metal'),
              ('wavenumber', 'the number of wavelengths per unit length, the reciprocal of wavelength'),
              ('black body radiation', 'radiation emitted by an ideal body that absorbs and emits all frequencies'),
              ('frequency', 'the number of waves that pass a given point in one second')],
    'orders': [('increasing order of wavelength', ['X-rays', 'ultraviolet', 'visible light', 'infrared', 'microwaves', 'radio waves'],
                'Wavelength increases (and frequency decreases) from X-rays to radio waves in the electromagnetic spectrum.', '<'),
               ('increasing order of photon energy', ['red light', 'yellow light', 'green light', 'blue light', 'violet light'],
                'E = hc/λ; wavelength decreases from red (~700 nm) to violet (~400 nm), so photon energy increases.', '<')],
    'tf': (['The kinetic energy of photoelectrons increases with the frequency of incident light.',
            'The number of photoelectrons ejected is proportional to the intensity of light.',
            'Electrons are ejected without any time lag when light of suitable frequency strikes the metal.',
            'All electromagnetic radiations travel with the same speed in vacuum.',
            'Planck\'s constant has the unit J s.'],
           [('Increasing the intensity of light increases the kinetic energy of photoelectrons.', 'Intensity increases the number of photoelectrons; their kinetic energy depends on frequency.'),
            ('Red light of very high intensity can eject electrons from any metal.', 'No electrons are ejected below the threshold frequency, however intense the light.'),
            ('The energy of a photon is inversely proportional to its frequency.', 'E = hν, so the energy of a photon is directly proportional to frequency.'),
            ('Radio waves have a higher frequency than X-rays.', 'X-rays have a much higher frequency than radio waves.')]),
    'ar': [('Photoelectrons are not emitted below the threshold frequency, whatever the intensity of light.', 'The energy of one photon (hν) must at least equal the work function to eject one electron.', 'a',
            'Each electron is ejected by one photon, so the photon energy, not intensity, decides emission.'),
           ('The wave theory of light could not explain the photoelectric effect.', 'According to the wave theory, energy of light depends on its intensity.', 'a',
            'The wave theory predicts emission at any frequency for bright enough light, which is not observed.')],
    'fams': [F('C2', 'D2', 'numerical', nu_lambda), F('C2', 'D2', 'numerical', photon_energy), F('C3', 'D3', 'numerical', photoelectric),
             F('C3', 'D4', 'numerical', threshold)],
    'qa': [('C4', 'D4', 'explain', 'A metal does not emit electrons when red light falls on it, but does with blue light of much lower intensity. Explain using Planck\'s quantum theory.',
            'Blue photons have higher frequency and energy (E = hν) than the work function; red photons have energy below it. Emission depends on photon energy, not intensity.',
            '1 mark: E = hν compared with W₀; 1 mark: intensity changes only number of photons.'),
           ('C4', 'D3', 'case', 'In an experiment on the photoelectric effect, the following data were obtained for a metal: light of 300 nm gives electrons with KE 1.84 eV; light of 400 nm gives electrons with KE 0.81 eV.\n(i) Calculate the work function of the metal (hc = 1240 eV nm). (1 mark)\n(ii) Find the threshold wavelength. (1 mark)\n(iii) Would light of 600 nm eject electrons? Explain. (2 marks)',
            '(i) W₀ = 1240/300 − 1.84 = 2.29 eV (ii) λ₀ = 1240/2.29 ≈ 541 nm (iii) No; 600 nm photon has 2.07 eV < 2.29 eV.',
            '(i) 1 mark (either data point gives ≈ 2.29 eV). (ii) 1 mark. (iii) 1 mark: E = 2.07 eV; 1 mark: less than W₀ so no emission.', ('case',))],
}

# ---------------- ch02 st3 Bohr model and line spectra ----------------

SERIES = {1: 'Lyman', 2: 'Balmer', 3: 'Paschen', 4: 'Brackett', 5: 'Pfund'}
RH = 109677  # cm⁻¹


def bohr_energy(r):
    n = r.randint(1, 6)
    Z, sp = r.choice([(1, 'the hydrogen atom'), (1, 'the hydrogen atom'), (2, 'He⁺'), (3, 'Li²⁺')])
    E = -2.18e-18 * Z * Z / n / n
    return {'stem': f'Calculate the energy of the electron in the n = {n} orbit of {sp} using Bohr\'s theory. (Eₙ = −2.18 × 10⁻¹⁸ (Z²/n²) J)',
            'answer': f'{sci(E)} J', 'key': f'Eₙ = −2.18 × 10⁻¹⁸ × {Z}²/{n}² = {sci(E)} J.',
            'distractors': [sci(-2.18e-18 * Z / n) + ' J', sci(-2.18e-18 * Z * Z / n) + ' J', sci(2.18e-18 * Z * Z / n / n * 2) + ' J']}


def bohr_radius(r):
    n = r.randint(1, 5)
    Z, sp = r.choice([(1, 'hydrogen atom'), (2, 'He⁺ ion'), (3, 'Li²⁺ ion')])
    rad = 52.9 * n * n / Z
    return {'stem': f'Calculate the radius of the n = {n} Bohr orbit of the {sp}. (r₁ for hydrogen = 52.9 pm)',
            'answer': f'{num(rad, 1)} pm', 'key': f'rₙ = 52.9 × n²/Z = 52.9 × {n * n}/{Z} = {num(rad, 1)} pm.',
            'distractors': [f'{num(52.9 * n / Z, 1)} pm', f'{num(52.9 * n * n * Z, 1)} pm', f'{num(52.9 * n * n / Z / Z, 1) if Z > 1 else num(52.9 * (n + 1) ** 2, 1)} pm']}


def transition(r):
    n1 = r.choice([1, 2, 2, 3])
    n2 = r.randint(n1 + 1, n1 + 4)
    wn = RH * (1 / n1 ** 2 - 1 / n2 ** 2)
    lam = 1e7 / wn
    reg = 'ultraviolet' if n1 == 1 else ('visible' if n1 == 2 else 'infrared')
    return {'stem': f'An electron in a hydrogen atom falls from n = {n2} to n = {n1}. Calculate the wavelength of the radiation emitted and name the spectral series. (R_H = 109 677 cm⁻¹)',
            'answer': f'{lam:.1f} nm; {SERIES[n1]} series ({reg})',
            'key': f'ν̄ = R_H(1/{n1}² − 1/{n2}²) = {wn:.0f} cm⁻¹ (1); λ = 1/ν̄ = {lam:.1f} nm (1); final level n = {n1} ⇒ {SERIES[n1]} series (1).',
            'distractors': [f'{lam:.1f} nm; {SERIES[n1 % 5 + 1]} series', f'{1e7 / (RH * (1 / n1 - 1 / n2)):.1f} nm; {SERIES[n1]} series', f'{lam * 2:.1f} nm; {SERIES[n1]} series']}


def series_name(r):
    n1 = r.randint(1, 5)
    n2 = r.randint(n1 + 1, n1 + 3)
    wrong = [SERIES[k] for k in SERIES if k != n1]
    return mcq(f'To which series does the line produced by the transition n = {n2} → n = {n1} in the hydrogen spectrum belong?',
               SERIES[n1], r.sample(wrong, 3), f'Lines ending at n = {n1} form the {SERIES[n1]} series.', r)


def n_lines(r):
    n = r.randint(3, 8)
    k = n * (n - 1) // 2
    return {'stem': f'Electrons in a sample of hydrogen atoms are excited to the n = {n} level. What is the maximum number of spectral lines that can be emitted as they return to the ground state?',
            'answer': str(k), 'key': f'Number of lines = n(n − 1)/2 = {n} × {n - 1}/2 = {k}.',
            'distractors': [str(n - 1), str(n * (n + 1) // 2), str(n * n)]}


def ionisation_h(r):
    n = r.randint(1, 4)
    E = 2.18e-18 / n / n
    return {'stem': f'How much energy is needed to ionise a hydrogen atom whose electron is in the n = {n} orbit? (E₁ = −2.18 × 10⁻¹⁸ J)',
            'answer': f'{sci(E)} J', 'key': f'Ionisation energy = 0 − Eₙ = 2.18 × 10⁻¹⁸/{n * n} = {sci(E)} J.',
            'distractors': [sci(2.18e-18 / n) + ' J', sci(2.18e-18 * n * n) + ' J', sci(-E) + ' J']}


CH2S3 = {
    'topic': "Bohr's model of the hydrogen atom",
    'terms': [('a stationary state', 'an orbit of fixed energy in which an electron revolves without radiating energy, according to Bohr'),
              ('an emission spectrum', 'the spectrum of radiation emitted by a substance that has absorbed energy'),
              ('an absorption spectrum', 'the spectrum obtained when white light passes through a sample and certain wavelengths are absorbed, leaving dark lines'),
              ('a line spectrum', 'a spectrum consisting of discrete bright lines with dark spaces between them'),
              ('the ground state', 'the lowest energy state of an atom')],
    'tf': (['The Balmer series lines of hydrogen lie in the visible region.', 'The Lyman series lies in the ultraviolet region.',
            'Bohr\'s theory applies only to single-electron species such as H, He⁺ and Li²⁺.',
            'The energy of an electron in a Bohr orbit becomes less negative as n increases.',
            'The angular momentum of an electron in a Bohr orbit is an integral multiple of h/2π.'],
           [('The Lyman series of hydrogen lies in the visible region.', 'The Lyman series lies in the ultraviolet region; the Balmer series is visible.'),
            ('Bohr\'s theory explains the spectra of multi-electron atoms well.', 'It fails for multi-electron atoms and cannot explain fine structure or the Zeeman and Stark effects.'),
            ('The energy gap between successive Bohr orbits increases with n.', 'The energy gap between successive orbits decreases as n increases.'),
            ('The radius of the n-th Bohr orbit is proportional to n.', 'The radius of the n-th orbit is proportional to n².')]),
    'ar': [('The spectrum of hydrogen consists of discrete lines.', 'The electron in a hydrogen atom can have only certain definite energies.', 'a',
            'Transitions between fixed energy levels give fixed frequencies, hence lines.'),
           ('Bohr\'s model violates Heisenberg\'s uncertainty principle.', 'Bohr\'s model gives the electron a definite path (orbit) with definite position and momentum.', 'a',
            'Exact orbits need exact position and momentum together, which the uncertainty principle forbids.')],
    'fams': [F('C2', 'D2', 'numerical', bohr_energy), F('C2', 'D2', 'numerical', bohr_radius), F('C3', 'D4', 'multi_step', transition, kinds=('long5',)),
             F('C2', 'D1', 'mcq', series_name), F('C3', 'D3', 'short', n_lines), F('C3', 'D2', 'numerical', ionisation_h)],
    'qa': [('C4', 'D4', 'explain', 'Why does the hydrogen atom, which has only one electron, show so many lines in its spectrum?',
            'A sample has a very large number of atoms; different atoms are excited to different levels and fall back by different transitions, each giving a line of a definite frequency.',
            '1 mark: many atoms in different excited states; 1 mark: each transition between two levels gives one line.'),
           ('C4', 'D3', 'explain', 'Give two limitations of Bohr\'s model of the atom.',
            'It cannot explain the spectra of multi-electron atoms; it cannot explain splitting of lines in magnetic (Zeeman) or electric (Stark) fields; it ignores the dual nature of the electron and the uncertainty principle.',
            '1 mark each for any two limitations.')],
}

# ---------------- ch02 st4 quantum numbers and orbitals ----------------

LL = 'spdf'


def orbital_name(r):
    n = r.randint(1, 5)
    l = r.randint(0, min(n - 1, 3))
    nm = f'{n}{LL[l]}'
    wrong = list({f'{n}{LL[(l + 1) % 4]}', f'{n + 1}{LL[l]}', f'{max(n - 1, 1)}{LL[l]}' if n > 1 else f'{n + 2}{LL[l]}', f'{l}{LL[min(n - 1, 3)]}'} - {nm})
    return mcq(f'Which orbital is described by the quantum numbers n = {n}, l = {l}?', nm, wrong[:3], f'l = {l} corresponds to a {LL[l]} orbital; n = {n} gives {nm}.', r)


def nodes(r):
    n = r.randint(2, 5)
    l = r.randint(0, min(n - 1, 3))
    rad = n - l - 1
    return {'stem': f'How many radial nodes and angular nodes does a {n}{LL[l]} orbital have?', 'answer': f'{rad} radial, {l} angular',
            'key': f'Radial nodes = n − l − 1 = {n} − {l} − 1 = {rad}; angular nodes = l = {l}; total {n - 1}.',
            'distractors': [f'{l} radial, {rad} angular', f'{n - 1} radial, {l} angular', f'{rad + 1} radial, {l} angular']}


def orbitals_in_shell(r):
    n = r.randint(2, 6)
    q = r.choice(['orbitals', 'electrons'])
    v = n * n if q == 'orbitals' else 2 * n * n
    return {'stem': f'What is the maximum number of {q} in the shell with n = {n}?', 'answer': str(v),
            'key': f'Number of orbitals = n² = {n * n}; electrons = 2n² = {2 * n * n}.',
            'distractors': [str(x) for x in {n * n, 2 * n * n, 2 * n, n * (n + 1), 2 * n + 1} - {v}][:3]}


def valid_qn(r):
    n = r.randint(1, 4)
    good_l = r.randint(0, n - 1)
    good_m = r.randint(-good_l, good_l)
    s = r.choice(['+½', '−½'])
    good = f'n = {n}, l = {good_l}, mₗ = {good_m:+d}, mₛ = {s}'.replace('+0', '0').replace('-', '−')
    bad = [f'n = {n}, l = {n}, mₗ = 0, mₛ = +½', f'n = {n + 1}, l = 1, mₗ = −2, mₛ = −½', f'n = {n}, l = 0, mₗ = 0, mₛ = 0'] if True else []
    bad[0] = bad[0]
    return mcq('Which of the following sets of quantum numbers is allowed for an electron?', good, bad,
               f'{good} is allowed: l ranges 0…n − 1, mₗ from −l to +l, mₛ = ±½. The others break one rule (l = n, |mₗ| > l, or mₛ = 0).', r)


def debroglie(r):
    who = r.choice(['an electron', 'a proton', 'a cricket ball'])
    if who == 'a cricket ball':
        m = r.choice([0.15, 0.16, 0.10])
        v = r.choice([20, 30, 40, 25])
        ms = f'{m} kg'
    elif who == 'an electron':
        m = 9.1e-31
        v = r.choice([1e5, 2e5, 5e5, 1e6, 2.2e6, 3e6])
        ms = '9.1 × 10⁻³¹ kg'
    else:
        m = 1.67e-27
        v = r.choice([1e3, 5e3, 1e4, 2e4, 1e5])
        ms = '1.67 × 10⁻²⁷ kg'
    lam = h / (m * v)
    return {'stem': f'Calculate the de Broglie wavelength of {who} of mass {ms} moving with a velocity of {sci(v, 2) if v >= 1000 else v} m s⁻¹. (h = 6.626 × 10⁻³⁴ J s)',
            'answer': f'{sci(lam)} m', 'key': f'λ = h/mv = 6.626 × 10⁻³⁴ / ({ms} × {sci(v, 2) if v >= 1000 else v}) = {sci(lam)} m.' +
            (' Such a tiny wavelength cannot be detected, so wave nature is unimportant for macroscopic objects.' if who == 'a cricket ball' else ''),
            'distractors': [sci(lam * 10) + ' m', sci(lam / 10) + ' m', sci(lam * 1000) + ' m']}


def uncertainty(r):
    dx = r.choice([1e-10, 1e-11, 1e-9, 5e-11, 2e-10])
    m = 9.1e-31
    dv = h / (4 * math.pi * m * dx)
    return {'stem': f'The position of an electron is measured within an uncertainty of {sci(dx, 1)} m. Calculate the minimum uncertainty in its velocity. (h = 6.626 × 10⁻³⁴ J s, mₑ = 9.1 × 10⁻³¹ kg)',
            'answer': f'{sci(dv)} m s⁻¹', 'key': f'Δx · mΔv ≥ h/4π ⇒ Δv = h/(4π m Δx) = {sci(dv)} m s⁻¹.',
            'distractors': [sci(dv * 4 * math.pi) + ' m s⁻¹', sci(dv / 10) + ' m s⁻¹', sci(dv * 2) + ' m s⁻¹']}


CH2S4 = {
    'topic': 'quantum numbers and atomic orbitals',
    'terms': [('the principal quantum number', 'the quantum number that determines the size and, largely, the energy of an orbital'),
              ('the azimuthal quantum number', 'the quantum number that determines the shape of an orbital (subshell)'),
              ('the magnetic quantum number', 'the quantum number that gives the spatial orientation of an orbital'),
              ('the spin quantum number', 'the quantum number that describes the orientation of the electron\'s spin, +½ or −½'),
              ('a node', 'a region where the probability density of finding the electron is zero'),
              ('an atomic orbital', 'the wave function ψ for an electron in an atom'),
              ('degenerate orbitals', 'orbitals having the same energy')],
    'orders': [('increasing order of energy of orbitals in a multi-electron atom', ['3s', '3p', '4s', '3d', '4p', '5s', '4d'],
                'By the (n + l) rule: lower n + l has lower energy; for equal n + l, lower n is lower in energy.', '<'),
               ('increasing order of number of radial nodes', ['2p', '3p', '4p', '5p'], 'Radial nodes = n − l − 1, so for p orbitals it is 0, 1, 2, 3.', '<')],
    'tf': (['A d subshell has five orbitals.', 'The 2p orbitals are degenerate in a hydrogen atom.',
            'For n = 3 the possible values of l are 0, 1 and 2.', 'ψ² gives the probability density of finding the electron.',
            'Orbitals with l = 0 are spherically symmetrical.'],
           [('The 3d orbital has two radial nodes.', 'A 3d orbital has n − l − 1 = 0 radial nodes and two angular nodes.'),
            ('For l = 2, mₗ can have values from 0 to 2 only.', 'For l = 2, mₗ = −2, −1, 0, +1, +2.'),
            ('A p orbital is spherical in shape.', 'A p orbital is dumb-bell shaped; s orbitals are spherical.'),
            ('In a multi-electron atom 4s is higher in energy than 3d.', 'In a multi-electron atom (e.g. K, Ca) 4s fills before 3d because it has a lower (n + l) value.'),
            ('Heisenberg\'s principle says we can know the exact position and momentum of an electron.', 'It is impossible to know both exactly at the same time.')]),
    'ar': [('The 2s orbital has one radial node.', 'The number of radial nodes is n − l − 1.', 'a', 'For 2s, n − l − 1 = 2 − 0 − 1 = 1.'),
           ('Wave nature of a moving cricket ball cannot be detected.', 'The de Broglie wavelength of a macroscopic body is extremely small.', 'a', 'λ = h/mv is tiny for large m.')],
    'fams': [F('C2', 'D2', 'mcq', orbital_name), F('C3', 'D2', 'short', nodes), F('C2', 'D2', 'short', orbitals_in_shell),
             F('C3', 'D3', 'mcq', valid_qn), F('C3', 'D3', 'numerical', debroglie), F('C3', 'D4', 'numerical', uncertainty)],
    'qa': [('C4', 'D4', 'explain', 'Why are electrons in a hydrogen atom with the same n but different l of equal energy, while in a multi-electron atom they are not?',
            'In hydrogen the energy depends only on n. In multi-electron atoms, inner electrons shield the nucleus; s electrons penetrate closer to the nucleus than p, p more than d, so they feel a larger effective nuclear charge and have lower energy.',
            '1 mark: energy depends only on n for H; 1 mark: shielding/penetration in multi-electron atoms.'),
           ('C4', 'D5', 'long', '(a) Write the four quantum numbers for each electron in the 2p subshell of nitrogen, following Hund\'s rule. (b) How many orbitals are there for n = 4, and how many of them are d orbitals? (c) Explain why l = 3 is not possible for n = 3.',
            '(a) n = 2, l = 1, mₗ = −1, 0, +1 each with mₛ = +½. (b) 16 orbitals; 5 are 4d. (c) l can only take values 0 to n − 1 = 2.',
            '(a) 2 marks; (b) 2 marks; (c) 1 mark.')],
}

# ---------------- ch02 st5 electronic configuration ----------------

AUF = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p']
CAP = {'s': 2, 'p': 6, 'd': 10}


def config(Z):
    if Z == 24:
        return '1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s¹'
    if Z == 29:
        return '1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s¹'
    out, left = [], Z
    for o in AUF:
        if left <= 0:
            break
        k = min(CAP[o[1]], left)
        out.append(f'{o}{str(k).translate(SUPD)}')
        left -= k
    return ' '.join(out)


def config_list(Z):
    d = {}
    for part in config(Z).split():
        orb = part[:2]
        k = int(part[2:].translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')))
        d[orb] = k
    return d


def unpaired(Z):
    tot = 0
    for orb, k in config_list(Z).items():
        cap = CAP[orb[1]]
        no = cap // 2
        tot += k if k <= no else cap - k
    return tot


def ec_write(r):
    Z = r.randint(5, 30)
    s = config(Z)
    wrong = []
    if Z in (24, 29):
        wrong.append(s.replace('3d⁵ 4s¹', '3d⁴ 4s²').replace('3d¹⁰ 4s¹', '3d⁹ 4s²'))
    alt = config(Z + 1)
    wrong += [alt, config(Z - 1)]
    if '4s' in s and '3d' in s:
        wrong.append(s.replace(' 4s²', '').replace('3d', '4s² 3d') if False else config(Z - 2))
    wrong = [w for w in dict.fromkeys(wrong) if w != s][:3]
    while len(wrong) < 3:
        wrong.append(config(Z + len(wrong) + 1))
    return mcq(f'Which is the ground-state electronic configuration of {ENAME[Z - 1]} (Z = {Z})?', s, wrong,
               f'Filling by Aufbau order 1s 2s 2p 3s 3p 4s 3d: {s}.' + (' Half-filled/fully filled 3d gives extra stability (exception).' if Z in (24, 29) else ''), r)


def ec_unpaired(r):
    Z = r.randint(5, 30)
    u = unpaired(Z)
    return {'stem': f'Write the electronic configuration of {ENAME[Z - 1]} (Z = {Z}) and state the number of unpaired electrons in its ground state.',
            'answer': f'{config(Z)}; {u} unpaired electron{"s" if u != 1 else ""}',
            'key': f'Configuration {config(Z)} (1); by Hund\'s rule electrons occupy degenerate orbitals singly first, giving {u} unpaired (1).',
            'distractors': [f'{config(Z)}; {u + 1} unpaired electrons', f'{config(Z)}; {abs(u - 1)} unpaired electrons', f'{config(Z)}; {u + 2} unpaired electrons']}


IONS = [(26, 2, 'Fe²⁺', '[Ar] 3d⁶', 4), (26, 3, 'Fe³⁺', '[Ar] 3d⁵', 5), (29, 1, 'Cu⁺', '[Ar] 3d¹⁰', 0), (29, 2, 'Cu²⁺', '[Ar] 3d⁹', 1),
        (25, 2, 'Mn²⁺', '[Ar] 3d⁵', 5), (24, 3, 'Cr³⁺', '[Ar] 3d³', 3), (30, 2, 'Zn²⁺', '[Ar] 3d¹⁰', 0), (27, 2, 'Co²⁺', '[Ar] 3d⁷', 3),
        (28, 2, 'Ni²⁺', '[Ar] 3d⁸', 2), (22, 4, 'Ti⁴⁺', '[Ar]', 0), (21, 3, 'Sc³⁺', '[Ar]', 0), (23, 3, 'V³⁺', '[Ar] 3d²', 2)]


def ion_config(r):
    Z, q, s, cfg, u = r.choice(IONS)
    return {'stem': f'Write the electronic configuration of {s} (Z of {ELEM[Z - 1]} = {Z}) and give the number of unpaired electrons. Explain which electrons are removed first.',
            'answer': f'{cfg}; {u} unpaired', 'key': f'Electrons are removed first from 4s (outermost, higher n), then 3d: {s} = {cfg} (1); unpaired = {u} (1).',
            'distractors': [f'{cfg.replace("[Ar]", "[Ar] 4s²")}; {u} unpaired' if q >= 2 else f'[Ar] 3d⁹ 4s¹; 1 unpaired', f'{cfg}; {u + 1} unpaired', f'[Ar] 3d{str(Z - 18 - q - 2).translate(SUPD)} 4s²; {u} unpaired' if Z - 18 - q - 2 > 0 else f'{cfg}; 2 unpaired']}


CH2S5 = {
    'topic': 'filling of orbitals in atoms',
    'terms': [('the Aufbau principle', 'the principle that in the ground state orbitals are filled in order of increasing energy'),
              ("Pauli's exclusion principle", 'the principle that no two electrons in an atom can have the same set of four quantum numbers'),
              ("Hund's rule of maximum multiplicity", 'the rule that pairing of electrons in degenerate orbitals does not take place until each orbital is singly occupied'),
              ('the (n + l) rule', 'the rule that an orbital with a lower value of n + l has lower energy and is filled first'),
              ('valence electrons', 'the electrons in the outermost shell of an atom'),
              ('core electrons', 'the electrons in the inner completely filled shells')],
    'tf': (['Chromium has the configuration [Ar] 3d⁵ 4s¹.', 'Copper has the configuration [Ar] 3d¹⁰ 4s¹.',
            'An orbital can hold a maximum of two electrons with opposite spins.', 'Half-filled and completely filled subshells have extra stability.',
            'Nitrogen has three unpaired electrons in its ground state.'],
           [('Chromium has the configuration [Ar] 3d⁴ 4s².', 'Chromium is [Ar] 3d⁵ 4s¹ because a half-filled d subshell is more stable.'),
            ('An orbital can hold three electrons if they have different spins.', 'By Pauli\'s principle an orbital holds at most two electrons, with opposite spins.'),
            ('In forming Fe²⁺, two 3d electrons are removed from iron.', 'The two 4s electrons are removed: Fe²⁺ is [Ar] 3d⁶.'),
            ('Oxygen has four unpaired electrons.', 'Oxygen (2p⁴) has two unpaired electrons.'),
            ('According to Hund\'s rule electrons pair up before they fill degenerate orbitals singly.', 'Electrons enter degenerate orbitals singly with parallel spins before pairing.')]),
    'ar': [('The electronic configuration of Cu is [Ar] 3d¹⁰ 4s¹ and not [Ar] 3d⁹ 4s².', 'Completely filled subshells have extra stability due to symmetry and larger exchange energy.', 'a',
            'The fully filled 3d¹⁰ arrangement is more stable, so R explains A.'),
           ('The 4s orbital is filled before 3d.', 'The (n + l) value of 4s is lower than that of 3d.', 'a', '4s: n + l = 4; 3d: n + l = 5.')],
    'fams': [F('C2', 'D2', 'mcq', ec_write), F('C3', 'D3', 'explain', ec_unpaired), F('C4', 'D3', 'explain', ion_config)],
    'qa': [('C4', 'D4', 'explain', 'Which is more stable, Fe²⁺ or Fe³⁺? Justify using electronic configurations.',
            'Fe³⁺ ([Ar] 3d⁵) is more stable than Fe²⁺ ([Ar] 3d⁶) because a half-filled d subshell has extra stability (symmetry and exchange energy).',
            '1 mark: both configurations; 1 mark: half-filled 3d⁵ more stable.'),
           ('C4', 'D3', 'explain', 'An element has the configuration 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s¹. Identify it and explain why its configuration is not 3d⁴ 4s².',
            'Chromium (Z = 24). The half-filled 3d⁵ 4s¹ arrangement is more stable due to symmetrical distribution and greater exchange energy.',
            '1 mark: chromium; 1 mark: stability of half-filled subshells.')],
}

# ---------------- ch03 st1 classification and periodic law ----------------

DIGIT = ['nil', 'un', 'bi', 'tri', 'quad', 'pent', 'hex', 'sept', 'oct', 'enn']
DSYM = ['n', 'u', 'b', 't', 'q', 'p', 'h', 's', 'o', 'e']
IUPAC_REAL = {101: 'mendelevium', 102: 'nobelium', 103: 'lawrencium', 104: 'rutherfordium', 105: 'dubnium', 106: 'seaborgium',
              107: 'bohrium', 108: 'hassium', 109: 'meitnerium', 110: 'darmstadtium', 111: 'roentgenium', 112: 'copernicium',
              113: 'nihonium', 114: 'flerovium', 115: 'moscovium', 116: 'livermorium', 117: 'tennessine', 118: 'oganesson'}


def sysname(Z):
    ds = [int(x) for x in str(Z)]
    n = ''.join(DIGIT[d] for d in ds) + 'ium'
    n = n.replace('ii', 'i').replace('nnn', 'nn')
    s = ''.join(DSYM[d] for d in ds)
    return n, s.capitalize()


def iupac_z(r):
    Z = r.randint(101, 120)
    n, s = sysname(Z)
    wrong_z = r.sample([z for z in range(101, 121) if z != Z], 3)
    return mcq(f'What is the IUPAC systematic (temporary) name and symbol of the element with atomic number {Z}?',
               f'{n} ({s})', [f'{sysname(z)[0]} ({sysname(z)[1]})' for z in wrong_z],
               f'Digits {" ".join(str(Z))} → {" + ".join(DIGIT[int(d)] for d in str(Z))} + ium = {n}, symbol {s}.' + (f' Its official name is {IUPAC_REAL[Z]}.' if Z in IUPAC_REAL else ''), r)


def iupac_from_name(r):
    Z = r.randint(101, 120)
    n, s = sysname(Z)
    return {'stem': f'An element has the IUPAC temporary name “{n}”. What is its atomic number and symbol?', 'answer': f'Z = {Z}; {s}',
            'key': f'Each root stands for a digit: {n} → {Z}; symbol {s}.',
            'distractors': [f'Z = {Z + 1}; {sysname(Z + 1)[1]}', f'Z = {Z - 10}; {s}', f'Z = {int(str(Z)[::-1]) if str(Z)[::-1][0] != "0" else Z + 2}; {s}']}


TRIADS = [('Li, Na, K', 7, 39, 23), ('Ca, Sr, Ba', 40, 137, 88), ('Cl, Br, I', 35.5, 127, 80), ('S, Se, Te', 32, 128, 79)]


def triad(r):
    t, a, c, b = r.choice(TRIADS)
    mid = (a + c) / 2
    return {'stem': f'In Döbereiner\'s triad {t}, the atomic masses of the first and third elements are {a} and {c}. Predict the atomic mass of the middle element and compare it with the actual value, {b}.',
            'answer': f'{num(mid, 2)}; close to the actual value {b}',
            'key': f'Law of triads: middle mass ≈ average of the other two = ({a} + {c})/2 = {num(mid, 2)}, close to {b}.',
            'distractors': [num(a + c, 1), num(c - a, 1), num(mid + 10, 1)]}


CH3S1 = {
    'topic': 'the classification of elements',
    'terms': [('the modern periodic law', 'the law that the physical and chemical properties of elements are periodic functions of their atomic numbers'),
              ("Mendeleev's periodic law", 'the law that the properties of elements are periodic functions of their atomic weights'),
              ("Döbereiner's law of triads", 'the observation that in groups of three similar elements the atomic weight of the middle element is about the mean of the other two'),
              ("Newlands' law of octaves", 'the observation that every eighth element, arranged by atomic weight, had properties similar to the first'),
              ('a period', 'a horizontal row of the periodic table'),
              ('a group', 'a vertical column of the periodic table')],
    'classify': False,
    'groups': [('a contribution of Mendeleev', ['leaving gaps for undiscovered elements', 'predicting the properties of eka-aluminium and eka-silicon', 'placing some elements out of atomic-weight order to group them by properties']),
               ('a contribution of Moseley', ['showing that the frequency of X-rays emitted is related to atomic number', 'establishing atomic number as the more fundamental property']),
               ('a contribution of Newlands', ['the law of octaves']), ('a contribution of Döbereiner', ['the law of triads']),
               ('a contribution of Lothar Meyer', ['plotting atomic volume against atomic weight'])],
    'tf': (['The modern periodic table has 18 groups and 7 periods.', 'Eka-aluminium predicted by Mendeleev was later discovered as gallium.',
            'Eka-silicon predicted by Mendeleev was later discovered as germanium.', 'Moseley showed that atomic number is a more fundamental property than atomic mass.',
            'The position of isotopes was a problem in Mendeleev\'s periodic table.'],
           [('Mendeleev arranged elements in order of increasing atomic number.', 'Mendeleev arranged elements in order of increasing atomic weight.'),
            ('The modern periodic table has 8 groups and 9 periods.', 'The long form has 18 groups and 7 periods.'),
            ("Newlands' law of octaves worked well for all elements up to uranium.", 'It worked well only up to calcium.'),
            ('Eka-silicon was later discovered as gallium.', 'Eka-silicon is germanium; eka-aluminium is gallium.')]),
    'ar': [('Mendeleev left gaps in his periodic table.', 'He believed that some elements were still undiscovered and predicted their properties.', 'a',
            'The gaps were deliberate places for elements such as gallium and germanium.'),
           ('In Mendeleev\'s table iodine (126.9) was placed after tellurium (127.6).', 'Mendeleev gave more importance to similarity in properties than to the order of atomic weights.', 'a',
            'Iodine resembles F, Cl, Br, so he placed it with them despite the lower atomic weight.')],
    'fams': [F('C2', 'D2', 'mcq', iupac_z), F('C3', 'D3', 'short', iupac_from_name), F('C3', 'D2', 'explain', triad)],
    'qa': [('C4', 'D3', 'explain', 'Why is the modern periodic law based on atomic number and not on atomic mass? Give one anomaly of Mendeleev\'s table it removes.',
            'Properties depend on electronic configuration, which is set by atomic number. It removes anomalies like Ar (39.9) before K (39.1) and Co before Ni, and the position of isotopes.',
            '1 mark: properties depend on Z/electronic configuration; 1 mark: one anomaly resolved.'),
           ('C4', 'D4', 'explain', 'Mendeleev predicted that eka-aluminium would have atomic weight about 68 and form an oxide E₂O₃. Explain how he could make such a prediction.',
            'From the gap below aluminium: properties of an element were taken as the average of its neighbours in the group and period; aluminium forms Al₂O₃, so its group member would form E₂O₃.',
            '1 mark: interpolation from neighbours; 1 mark: group valency gives the formula of the oxide.')],
}

# ---------------- ch03 st2 blocks and position ----------------

def block_of(Z):
    if Z in (1, 2):
        return 's'
    cfg = config(Z) if Z <= 36 else None
    last = cfg.split()[-1][:2] if cfg else None
    if Z in (24, 29):
        return 'd'
    return last[1]


def group_of(Z):
    if Z <= 2:
        return 1 if Z == 1 else 18
    if Z <= 10:
        v = Z - 2
        return v if v <= 2 else v + 10
    if Z <= 18:
        v = Z - 10
        return v if v <= 2 else v + 10
    v = Z - 18
    return v if v <= 12 else v - 12 + 12


def period_of(Z):
    return 1 if Z <= 2 else 2 if Z <= 10 else 3 if Z <= 18 else 4


def position(r):
    Z = r.choice([z for z in range(3, 37) if z != 2])
    g, p, b = group_of(Z), period_of(Z), block_of(Z)
    return {'stem': f'An element has the electronic configuration {config(Z)}. State its period, group and block in the modern periodic table.',
            'answer': f'Period {p}, group {g}, {b}-block',
            'key': f'Highest n = {p} ⇒ period {p}; last electron enters {b} subshell ⇒ {b}-block; group {g} from the number of valence (ns + np, or ns + (n−1)d) electrons.',
            'distractors': [f'Period {p}, group {g % 18 + 1}, {b}-block', f'Period {p + 1 if p < 4 else p - 1}, group {g}, {b}-block', f'Period {p}, group {g}, {"p" if b != "p" else "s"}-block']}


BLOCK_FACT = [('s-block', ['alkali and alkaline earth metals', 'outer configuration ns¹ or ns²', 'mostly reactive metals with low ionisation enthalpies', 'form mostly ionic compounds (except Li and Be)']),
              ('p-block', ['outer configuration ns² np¹⁻⁶', 'include metals, non-metals and metalloids', 'contain the halogens and noble gases', 'non-metallic character increases across a period']),
              ('d-block', ['outer configuration (n−1)d¹⁻¹⁰ ns⁰⁻²', 'mostly form coloured ions', 'show variable oxidation states', 'used widely as catalysts']),
              ('f-block', ['outer configuration (n−2)f¹⁻¹⁴ (n−1)d⁰⁻¹ ns²', 'lanthanoids and actinoids', 'actinoids are radioactive', 'placed separately at the bottom of the table'])]

CH3S2 = {
    'topic': 'the s, p, d and f blocks',
    'terms': [('representative elements', 'the s- and p-block elements together'),
              ('transition elements', 'the d-block elements, placed between the s- and p-blocks'),
              ('inner transition elements', 'the f-block elements, the lanthanoids and actinoids'),
              ('metalloids', 'elements such as silicon, germanium and arsenic that show properties of both metals and non-metals'),
              ('noble gases', 'the group 18 elements with completely filled valence shells')],
    'groups': [('an s-block element', ['sodium', 'calcium', 'potassium', 'magnesium', 'lithium', 'barium']),
               ('a p-block element', ['aluminium', 'sulphur', 'chlorine', 'nitrogen', 'silicon', 'neon']),
               ('a d-block element', ['iron', 'copper', 'chromium', 'zinc', 'manganese', 'nickel']),
               ('an f-block element', ['cerium', 'uranium', 'thorium', 'europium', 'neodymium', 'plutonium'])],
    'features': {'intro': 'An element has these characteristics:', 'q': 'To which block of the periodic table does it belong', 'items': BLOCK_FACT},
    'tf': (['Helium is placed in group 18 although its configuration is 1s².', 'The number of elements in the fourth period is 18.',
            'Elements in the same group have the same number of valence electrons (for main groups).', 'The 4f series follows lanthanum.'],
           [('Helium is placed in the s-block group 2 in the periodic table.', 'Helium is placed in group 18 with the noble gases because its valence shell is completely filled.'),
            ('The third period contains 18 elements.', 'The third period contains 8 elements (3s and 3p).'),
            ('d-block elements have the general configuration ns² np⁶.', 'd-block elements have (n−1)d¹⁻¹⁰ ns⁰⁻².'),
            ('All p-block elements are non-metals.', 'The p-block has metals (Al, Sn, Pb), metalloids and non-metals.')]),
    'ar': [('The number of elements in a period equals the number of electrons that can fill the orbitals being filled.', 'In period 4, the 4s, 3d and 4p orbitals are filled, holding 18 electrons.', 'a',
            'Period 4 has 18 elements because 2 + 10 + 6 = 18.'),
           ('Zinc is placed in the d-block.', 'The last electron in zinc enters the 3d subshell.', 'a', 'Zn is [Ar] 3d¹⁰ 4s²; the differentiating electron is in 3d.')],
    'fams': [F('C3', 'D3', 'explain', position)],
    'qa': [('C4', 'D4', 'explain', 'Hydrogen is placed in group 1 but it also resembles the halogens. Give one reason for each placement.',
            'Group 1: one electron in its valence shell (1s¹), forms H⁺. Halogens: needs one electron to complete its shell, forms H⁻ and diatomic molecules.',
            '1 mark each.')],
}

# ---------------- ch03 st3 periodic trends ----------------

CH3S3 = {
    'topic': 'periodic trends',
    'terms': [('ionisation enthalpy', 'the energy required to remove an electron from an isolated gaseous atom in its ground state'),
              ('electron gain enthalpy', 'the enthalpy change when an electron is added to a neutral gaseous atom to form an anion'),
              ('electronegativity', 'a qualitative measure of the ability of an atom in a chemical compound to attract shared electrons to itself'),
              ('isoelectronic species', 'atoms and ions that have the same number of electrons'),
              ('the shielding effect', 'the reduction in the nuclear attraction felt by valence electrons due to inner electrons'),
              ('the covalent radius', 'half the distance between the nuclei of two identical atoms joined by a single covalent bond'),
              ('effective nuclear charge', 'the net positive charge experienced by a valence electron after shielding by inner electrons')],
    'orders': [('increasing order of atomic radius', ['F', 'O', 'N', 'C', 'B', 'Be', 'Li'], 'Across a period atomic radius decreases as nuclear charge increases; so it increases from F to Li.', '<'),
               ('increasing order of atomic radius', ['Li', 'Na', 'K', 'Rb', 'Cs'], 'Down a group a new shell is added at each step, so radius increases.', '<'),
               ('increasing order of first ionisation enthalpy', ['Li', 'B', 'Be', 'C', 'O', 'N', 'F', 'Ne'],
                'IE rises across period 2, but B < Be (2p electron is easier to remove than 2s) and O < N (N has a stable half-filled 2p³).', '<'),
               ('increasing order of ionic radius', ['Al³⁺', 'Mg²⁺', 'Na⁺', 'F⁻', 'O²⁻', 'N³⁻'],
                'These are isoelectronic (10 electrons); the greater the nuclear charge, the smaller the ion.', '<'),
               ('order of increasing negative electron gain enthalpy (from least to most negative)', ['I', 'Br', 'F', 'Cl'],
                'Cl has the most negative value; F is less negative than Cl because of strong electron repulsion in its small 2p subshell.', '<'),
               ('increasing order of electronegativity', ['Cs', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'F'],
                'Electronegativity increases across a period and decreases down a group; F is the most electronegative element.', '<'),
               ('increasing order of first ionisation enthalpy', ['Cs', 'Rb', 'K', 'Na', 'Li'], 'Down group 1 atomic size increases, so the valence electron is removed more easily.', '<')],
    'tf': (['The ionisation enthalpy of nitrogen is higher than that of oxygen.', 'Fluorine is the most electronegative element.',
            'Chlorine has the most negative electron gain enthalpy among the halogens.', 'A cation is smaller than its parent atom.',
            'The second ionisation enthalpy of an element is always higher than its first.', 'Noble gases have large positive electron gain enthalpies.'],
           [('Fluorine has the most negative electron gain enthalpy of all elements.', 'Chlorine has the most negative electron gain enthalpy; fluorine\'s small size causes inter-electronic repulsion.'),
            ('An anion is smaller than its parent atom.', 'An anion is larger because the added electron increases repulsion and the effective nuclear charge per electron falls.'),
            ('Ionisation enthalpy increases down a group.', 'Ionisation enthalpy generally decreases down a group as atomic size increases.'),
            ('Atomic radius increases from left to right across a period.', 'Atomic radius decreases across a period because effective nuclear charge increases.'),
            ('The first ionisation enthalpy of boron is higher than that of beryllium.', 'B is lower than Be, because the 2p electron of B is shielded by 2s electrons and is easier to remove.'),
            ('Electronegativity has the unit kJ mol⁻¹.', 'Electronegativity is a dimensionless relative number (e.g. Pauling scale).')]),
    'ar': [('The first ionisation enthalpy of nitrogen is greater than that of oxygen.', 'Nitrogen has a half-filled, extra-stable 2p³ configuration.', 'a',
            'Removing an electron from the stable half-filled 2p³ needs more energy; oxygen loses a paired 2p electron easily.'),
           ('Na⁺ is smaller than F⁻.', 'Na⁺ and F⁻ are isoelectronic but Na⁺ has a higher nuclear charge.', 'a', 'More protons pull the same 10 electrons more strongly.'),
           ('Noble gases have large positive electron gain enthalpies.', 'The added electron would have to enter the next higher shell.', 'a', 'Their valence shells are full, so an extra electron is very unstable.')],
    'qa': [('C4', 'D4', 'explain', 'The first ionisation enthalpies (kJ mol⁻¹) of Na, Mg and Al are 496, 737 and 577. Explain why Mg is higher than both Na and Al.',
            'Mg has a higher nuclear charge than Na and a stable filled 3s² subshell; in Al the electron removed is a 3p electron, which is higher in energy and shielded by 3s, so it is removed more easily.',
            '1 mark: Mg vs Na (nuclear charge); 1 mark: Mg vs Al (3s² vs 3p¹, penetration/shielding).'),
           ('C4', 'D5', 'long', 'Elements A, B, C and D have first ionisation enthalpies 520, 2080, 900 and 1681 kJ mol⁻¹ and electron gain enthalpies −60, +116, positive and −328 kJ mol⁻¹. Identify (a) the most reactive metal, (b) the most reactive non-metal, (c) a noble gas, (d) a metal that forms a stable binary halide of formula MX₂. Justify each.',
            '(a) A (lowest IE, 520 – Li). (b) D (high IE and very negative EGE – F). (c) B (very high IE, positive EGE – Ne). (d) C (IE 900 with positive EGE – Be forms BeX₂).',
            'Identification with reason: (a) 1, (b) 1.5, (c) 1, (d) 1.5 marks.'),
           ('C4', 'D3', 'case', 'Read the data for the second-period elements and answer.\nFirst ionisation enthalpy (kJ mol⁻¹): Li 520, Be 899, B 801, C 1086, N 1402, O 1314, F 1681, Ne 2081.\n(i) What is the general trend across the period? (1 mark)\n(ii) Explain why Be > B. (1 mark)\n(iii) Explain why N > O. (2 marks)',
            '(i) It increases (with exceptions). (ii) B loses a 2p electron, shielded by 2s and higher in energy. (iii) N has a stable half-filled 2p³; in O the removed electron is paired and repelled.',
            '(i) increasing nuclear charge – 1. (ii) 1. (iii) half-filled stability 1 + electron-pair repulsion in O 1.', ('case',))],
}

# ---------------- ch03 st4 valence, oxidation states, reactivity ----------------

GROUP_VAL = {'Na': (1, 1), 'K': (1, 1), 'Li': (1, 1), 'Mg': (2, 2), 'Ca': (2, 2), 'Ba': (2, 2), 'Al': (13, 3),
             'B': (13, 3), 'C': (14, 4), 'Si': (14, 4), 'N': (15, 3), 'P': (15, 3), 'O': (16, 2), 'S': (16, 2), 'F': (17, 1), 'Cl': (17, 1), 'Br': (17, 1)}
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def binary_formula(r):
    metal = r.choice(['Na', 'K', 'Li', 'Mg', 'Ca', 'Ba', 'Al'])
    nonm = r.choice(['O', 'S', 'F', 'Cl', 'Br', 'N'])
    a, b = GROUP_VAL[metal][1], GROUP_VAL[nonm][1]
    g = math.gcd(a, b)
    x, y = b // g, a // g
    f = f'{metal}{str(x).translate(SUB) if x > 1 else ""}{nonm}{str(y).translate(SUB) if y > 1 else ""}'
    wrong = set()
    for (p, q) in [(1, 1), (y, x), (2, 1), (1, 2), (2, 3), (3, 2)]:
        w = f'{metal}{str(p).translate(SUB) if p > 1 else ""}{nonm}{str(q).translate(SUB) if q > 1 else ""}'
        if w != f:
            wrong.add(w)
    return mcq(f'Using the positions of the elements in the periodic table, predict the formula of the compound formed between {metal} (group {GROUP_VAL[metal][0]}) and {nonm} (group {GROUP_VAL[nonm][0]}).',
               f, sorted(wrong)[:3], f'Valence of {metal} = {a}, of {nonm} = {b}; crossing the valencies gives {f}.', r)


CH3S4 = {
    'topic': 'periodicity of valence and chemical reactivity',
    'groups': [('an acidic oxide', ['Cl₂O₇', 'SO₃', 'P₄O₁₀', 'CO₂', 'N₂O₅']), ('a basic oxide', ['Na₂O', 'CaO', 'MgO', 'K₂O', 'BaO']),
               ('an amphoteric oxide', ['Al₂O₃', 'ZnO', 'BeO', 'SnO₂', 'PbO']), ('a neutral oxide', ['CO', 'NO', 'N₂O'])],
    'tf': (['Oxides of elements on the left of a period are basic and on the right are acidic.', 'Al₂O₃ reacts with both acids and bases.',
            'Lithium shows a diagonal relationship with magnesium.', 'Fluorine shows only the −1 oxidation state in its compounds.',
            'The most reactive metals are on the extreme left of the periodic table.'],
           [('Na₂O is an acidic oxide.', 'Na₂O is a strongly basic oxide (forms NaOH with water).'),
            ('Reactivity of alkali metals decreases down the group.', 'Reactivity of alkali metals increases down the group as ionisation enthalpy falls.'),
            ('Fluorine can show a +7 oxidation state like chlorine.', 'Fluorine, being the most electronegative element, shows only −1.'),
            ('Elements of group 2 commonly show valence 3.', 'Group 2 elements show valence 2.')]),
    'ar': [('Lithium and magnesium show similar properties.', 'Li and Mg have similar sizes and charge-to-radius ratios (diagonal relationship).', 'a',
            'Similar polarising power gives similar chemistry, so R explains A.'),
           ('Cl₂O₇ is an acidic oxide.', 'Non-metal oxides generally react with water to form acids.', 'a', 'Cl₂O₇ + H₂O → 2HClO₄.')],
    'orders': [('increasing order of acidic character of oxides', ['Na₂O', 'MgO', 'Al₂O₃', 'SiO₂', 'P₄O₁₀', 'SO₃', 'Cl₂O₇'],
                'Across period 3 metallic character falls, so oxides change from basic through amphoteric to acidic.', '<')],
    'fams': [F('C3', 'D2', 'mcq', binary_formula)],
    'qa': [('C4', 'D4', 'explain', 'Predict, with reason, whether the oxide formed by an element with Z = 20 is acidic or basic, and write its formula.',
            'Z = 20 is calcium (group 2, a reactive metal); it forms the basic oxide CaO (CaO + H₂O → Ca(OH)₂).',
            '1 mark: Ca, basic; 1 mark: CaO with reason (metal oxide/forms hydroxide).'),
           ('C4', 'D3', 'explain', 'Why do the elements of the second period (Li to F) differ from the rest of their groups in many properties?',
            'Small size, high electronegativity and ionisation enthalpy, and absence of d orbitals; so they cannot expand their valence shell beyond 4 and form pπ–pπ multiple bonds.',
            '1 mark: small size/high EN; 1 mark: no d orbitals / maximum covalency 4.')],
}

# ---------------- extra C3/C4 generators ----------------

def definite_check(r):
    f, comp, nm = r.choice([('CO₂', {'C': 1, 'O': 2}, 'carbon dioxide'), ('H₂O', {'H': 2, 'O': 1}, 'water'), ('MgO', {'Mg': 1, 'O': 1}, 'magnesium oxide'),
                            ('CuO', {'Cu': 1, 'O': 1}, 'copper(II) oxide'), ('NaCl', {'Na': 1, 'Cl': 1}, 'sodium chloride')])
    AMx = dict(AM, Cu=63.5)
    e1, e2 = list(comp)
    frac1 = AMx[e1] * comp[e1] / (AMx[e1] * comp[e1] + AMx[e2] * comp[e2])
    m1 = round(r.uniform(2, 6), 2)
    m2 = round(r.uniform(6, 12), 2)
    a1, a2 = round(m1 * frac1, 3), round(m2 * frac1, 3)
    who, who2 = name(r), name(r)
    return {'stem': f'{who} decomposed {m1} g of {nm} from one source and obtained {a1} g of {e1}. {who2} decomposed {m2} g of {nm} made in a different way and obtained {a2} g of {e1}. Show that the results agree with the law of definite proportions.',
            'answer': f'% {e1} = {a1 / m1 * 100:.1f}% in both samples, so the composition is fixed.',
            'key': f'Sample 1: {a1}/{m1} × 100 = {a1 / m1 * 100:.1f}% (1); sample 2: {a2}/{m2} × 100 = {a2 / m2 * 100:.1f}% (1); same composition irrespective of source ⇒ law of definite proportions.'}


def more_atoms(r):
    (f1, c1, n1), (f2, c2, n2) = r.sample(CMPD, 2)
    m1 = r.choice([1, 2, 5, 10, 18, 20])
    m2 = r.choice([1, 2, 5, 10, 18, 20])
    a1 = m1 / M(c1) * sum(c1.values())
    a2 = m2 / M(c2) * sum(c2.values())
    if abs(a1 - a2) / max(a1, a2) < 0.05:
        raise ValueError
    big = f'{m1} g of {f1}' if a1 > a2 else f'{m2} g of {f2}'
    return {'stem': f'Which contains more atoms in total: {m1} g of {n1} ({f1}) or {m2} g of {n2} ({f2})? Show your reasoning. (Molar masses: {f1} = {mstr(M(c1))}, {f2} = {mstr(M(c2))} g mol⁻¹)',
            'answer': f'{big}', 'key': f'Moles of atoms: {f1}: {m1}/{mstr(M(c1))} × {sum(c1.values())} = {a1:.3f} mol; {f2}: {m2}/{mstr(M(c2))} × {sum(c2.values())} = {a2:.3f} mol (1 each); so {big} has more atoms.',
            'distractors': [f'{m2} g of {f2}' if a1 > a2 else f'{m1} g of {f1}', 'Both contain the same number of atoms', 'Cannot be decided without the volumes']}


def percent_yield(r):
    eq, rs, ps = r.choice(RXN)
    a, b = rs[0], ps[0]
    na = r.choice([0.2, 0.5, 1, 2, 2.5]) * a[2]
    theo = na * b[2] / a[2] * b[3]
    y = r.choice([60, 65, 70, 75, 80, 85, 90])
    actual = round(theo * y / 100, 2)
    who = name(r)
    return {'stem': f'{who} carries out the reaction {eq} using {mstr(na * a[3])} g of {a[0]} (other reactants in excess) and collects {num(actual, 2)} g of {b[0]}. Calculate the theoretical yield and the percentage yield. (Molar masses: {a[1]} {mstr(a[3])}, {b[1]} {mstr(b[3])} g mol⁻¹) Suggest one reason why the yield is less than 100%.',
            'answer': f'Theoretical yield {num(theo, 2)} g; percentage yield {y}%',
            'key': f'n({a[1]}) = {num(na, 3)} mol → n({b[1]}) = {num(na * b[2] / a[2], 3)} mol → {num(theo, 2)} g (1); % yield = {num(actual, 2)}/{num(theo, 2)} × 100 = {y}% (1); reason: incomplete reaction, side reactions or loss during handling (1).'}


def mix_solutions(r):
    M1, V1 = r.choice([0.1, 0.2, 0.5, 1.0, 1.5]), r.choice([50, 100, 150, 200, 250])
    M2, V2 = r.choice([0.1, 0.25, 0.4, 2.0, 0.8]), r.choice([100, 200, 300, 400])
    if M1 == M2:
        raise ValueError
    Mf = (M1 * V1 + M2 * V2) / (V1 + V2)
    s = r.choice(['NaCl', 'glucose', 'KCl', 'urea'])
    return {'stem': f'{V1} mL of {M1} M {s} solution is mixed with {V2} mL of {M2} M {s} solution. Calculate the molarity of the final solution (assume volumes are additive).',
            'answer': f'{sf(Mf, 3)} M', 'key': f'Total moles = ({M1} × {V1} + {M2} × {V2})/1000 = {num((M1 * V1 + M2 * V2) / 1000, 4)} mol; total volume = {V1 + V2} mL; M = {sf(Mf, 3)} mol L⁻¹.',
            'distractors': [f'{sf((M1 + M2) / 2, 3)} M' if abs((M1 + M2) / 2 - Mf) > 0.005 else f'{sf(M1 + M2, 3)} M', f'{sf(M1 + M2, 3)} M', f'{sf(Mf * 2, 3)} M']}


def molarity_to_molality(r):
    s, m = r.choice(SOLUTES[:6])
    Mo = r.choice([0.5, 1.0, 1.5, 2.0])
    d = r.choice([1.02, 1.04, 1.05, 1.08, 1.10])
    mass_sol = 1000 * d
    mass_solute = Mo * m
    mass_solv = mass_sol - mass_solute
    b = Mo / (mass_solv / 1000)
    return {'stem': f'The density of a {Mo} M solution of {s} is {d} g mL⁻¹. Calculate its molality. (Molar mass = {num(m)} g mol⁻¹)',
            'answer': f'{sf(b, 3)} mol kg⁻¹',
            'key': f'1 L solution = {num(mass_sol)} g; solute = {Mo} × {num(m)} = {num(mass_solute, 2)} g (1); solvent = {num(mass_solv, 2)} g (1); m = {Mo}/{num(mass_solv / 1000, 4)} = {sf(b, 3)} mol kg⁻¹ (1).',
            'distractors': [f'{sf(Mo / d, 3)} mol kg⁻¹', f'{sf(Mo, 3)} mol kg⁻¹', f'{sf(Mo / (mass_sol / 1000), 3)} mol kg⁻¹']}


ID_SPECIES = [('Mg', 12, 24, 2), ('Na', 11, 23, 1), ('O', 8, 16, -2), ('F', 9, 19, -1), ('Al', 13, 27, 3), ('S', 16, 32, -2),
              ('Cl', 17, 35, -1), ('K', 19, 39, 1), ('Ca', 20, 40, 2), ('Ne', 10, 20, 0), ('Ar', 18, 40, 0), ('N', 7, 14, -3)]


def identify_species(r):
    sym, Z, A, q = r.choice(ID_SPECIES)
    e = Z - q
    sp = ion(sym, A, q)
    wrong = [ion(sym, A, 0) if q else ion(sym, A, 1), ion(ELEM[e - 1], e + (A - Z), 0), ion(sym, A + 1, q)]
    return mcq(f'A species has {Z} protons, {A - Z} neutrons and {e} electrons. Which species is it?', sp, wrong,
               f'Z = {Z} ⇒ {sym}; A = {Z} + {A - Z} = {A}; charge = {Z} − {e} = {q:+d} ⇒ {sp}.', r)


def photon_count(r):
    P = r.choice([10, 25, 40, 60, 100])
    lam = r.choice([400, 450, 500, 550, 600, 650])
    t = r.choice([1, 2, 5, 10])
    E = h * c / (lam * 1e-9)
    N = P * t / E
    return {'stem': f'A {P} W lamp emits monochromatic light of wavelength {lam} nm. How many photons does it emit in {t} s? (Assume all the power is emitted as light; h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹)',
            'answer': f'{sci(N)} photons', 'key': f'Energy per photon = hc/λ = {sci(E)} J (1); energy emitted = {P} × {t} = {P * t} J (1); N = {P * t}/{sci(E)} = {sci(N)} (1).',
            'distractors': [sci(N / t) + ' photons', sci(N * 10) + ' photons', sci(P / E / 10) + ' photons']}


def find_n2(r):
    n1 = r.choice([1, 2, 2, 3])
    n2 = r.randint(n1 + 1, n1 + 4)
    wn = RH * (1 / n1 ** 2 - 1 / n2 ** 2)
    lam = 1e7 / wn
    return {'stem': f'A line in the {SERIES[n1]} series of hydrogen has wavelength {lam:.1f} nm. Find the value of n for the higher energy level involved. (R_H = 109 677 cm⁻¹)',
            'answer': f'n = {n2}', 'key': f'ν̄ = 1/λ = {wn:.0f} cm⁻¹ (1); {SERIES[n1]} series ⇒ n₁ = {n1}; 1/n₂² = 1/{n1 * n1} − ν̄/R_H = {1 / n2 ** 2:.4f} (1); n₂ = {n2} (1).',
            'distractors': [f'n = {n2 + 1}', f'n = {n2 - 1 if n2 - 1 > n1 else n2 + 2}', f'n = {n1}']}


def orbital_from_nodes(r):
    n = r.randint(2, 5)
    l = r.randint(0, min(n - 1, 3))
    rad = n - l - 1
    nm = f'{n}{LL[l]}'
    wrong = list(dict.fromkeys([f'{n + 1}{LL[l]}', f'{n}{LL[(l + 1) % 4]}' if (l + 1) % 4 < n else f'{n + 2}{LL[(l + 1) % 4]}', f'{rad + l + 2}{LL[max(l - 1, 0)]}', f'{n - 1 if n > l + 1 else n + 3}{LL[l]}']))
    wrong = [w for w in wrong if w != nm][:3]
    return mcq(f'An orbital has {rad} radial node{"s" if rad != 1 else ""} and {l} angular node{"s" if l != 1 else ""}. Identify the orbital.', nm, wrong,
               f'Angular nodes = l = {l} ⇒ {LL[l]}; radial nodes = n − l − 1 = {rad} ⇒ n = {n}; so {nm}.', r)


def most_unpaired(r):
    Zs = r.sample([z for z in range(5, 31)], 4)
    us = [unpaired(z) for z in Zs]
    if us.count(max(us)) != 1:
        raise ValueError
    best = Zs[us.index(max(us))]
    return mcq('Which of the following atoms has the largest number of unpaired electrons in its ground state? ' + ', '.join(f'{ENAME[z - 1]} (Z = {z})' for z in Zs),
               f'{ENAME[best - 1]} (Z = {best})', [f'{ENAME[z - 1]} (Z = {z})' for z in Zs if z != best],
               '; '.join(f'{ELEM[z - 1]}: {unpaired(z)}' for z in Zs) + f' ⇒ {ENAME[best - 1]}.', r)


SUPERHEAVY = {113: (13, 'p', 7), 114: (14, 'p', 7), 115: (15, 'p', 7), 116: (16, 'p', 7), 117: (17, 'p', 7), 118: (18, 'p', 7), 119: (1, 's', 8), 120: (2, 's', 8)}


def predict_superheavy(r):
    Z = r.choice(list(SUPERHEAVY))
    g, b, p = SUPERHEAVY[Z]
    nm, sy = sysname(Z)
    fam = {1: 'alkali metals', 2: 'alkaline earth metals', 17: 'halogens', 18: 'noble gases'}.get(g, f'group {g} elements')
    return {'stem': f'Element {Z} ({nm}, {sy}) has not been characterised fully. Predict its period, group and block, and name the family it would belong to.',
            'answer': f'Period {p}, group {g}, {b}-block; {fam}',
            'key': f'Period 7 ends at Z = 118 (7p⁶). ' + (f'Z = {Z} lies in 7p: 7s² 5f¹⁴ 6d¹⁰ 7p{str(Z - 112).translate(SUPD)} ⇒ group {g} (1 + 1).' if b == 'p' else f'Z = {Z} begins period 8 with 8s{"¹" if g == 1 else "²"} ⇒ group {g} (1 + 1).'),
            'distractors': [f'Period {p}, group {g}, d-block; transition metals', f'Period {p - 1}, group {g}, {b}-block; {fam}', f'Period {p}, group {(g % 18) + 1}, {b}-block; group {(g % 18) + 1} elements']}


def position5(r):
    Z = r.randint(37, 54)
    if Z <= 38:
        g, b = Z - 36, 's'
    elif Z <= 48:
        g, b = Z - 36, 'd'
    else:
        g, b = Z - 36, 'p'
    return {'stem': f'Without writing the full electronic configuration, predict the period, group and block of the element with atomic number {Z}. Show how you decide.',
            'answer': f'Period 5, group {g}, {b}-block',
            'key': f'Period 4 ends at Kr (Z = 36), so Z = {Z} is in period 5 (1); it is the {Z - 36}th element of the period: 5s fills for 37–38, 4d for 39–48, 5p for 49–54 ⇒ group {g}, {b}-block (1).',
            'distractors': [f'Period 4, group {g}, {b}-block', f'Period 5, group {g - 10 if g > 12 else g + 10}, {b}-block', f'Period 5, group {g}, {"p" if b != "p" else "d"}-block']}


CH1S1['orders'] = [('increasing order of length', ['1 pm', '1 nm', '1 μm', '1 mm', '1 cm', '1 dm', '1 m'],
                    'pico = 10⁻¹², nano = 10⁻⁹, micro = 10⁻⁶, milli = 10⁻³, centi = 10⁻², deci = 10⁻¹.', '<')]
CH1S2['fams'].append(F('C4', 'D3', 'explain', definite_check, marks=2))
CH1S3['fams'].append(F('C4', 'D3', 'explain', more_atoms, marks=2))
CH1S4['fams'].append(F('C4', 'D4', 'multi_step', percent_yield, kinds=('long5',)))
CH1S5['fams'] += [F('C4', 'D3', 'numerical', mix_solutions), F('C4', 'D4', 'numerical', molarity_to_molality, marks=3)]
CH2S1['fams'].append(F('C4', 'D3', 'mcq', identify_species))
CH2S1['orders'] = [('increasing order of charge-to-mass ratio (magnitude)', ['neutron', 'α-particle', 'proton', 'electron'],
                    'Neutron has no charge; α (2+, 4 u) has half the e/m of a proton (1+, 1 u); the electron is ~1840 times lighter than a proton.', '<')]
CH2S2['fams'].append(F('C4', 'D4', 'multi_step', photon_count, kinds=('long5',)))
CH2S3['fams'].append(F('C4', 'D4', 'numerical', find_n2, marks=3))
CH2S4['fams'].append(F('C4', 'D3', 'mcq', orbital_from_nodes))
CH2S5['fams'].append(F('C4', 'D3', 'mcq', most_unpaired))
CH3S1['fams'].append(F('C4', 'D3', 'explain', predict_superheavy, marks=2))
CH3S2['fams'].append(F('C4', 'D3', 'explain', position5, marks=2))
CH3S4['terms'] = [('valence', 'the combining capacity of an element, usually the number of valence electrons or eight minus that number'),
                  ('the diagonal relationship', 'the similarity in properties between certain second-period elements and the third-period elements diagonally below them'),
                  ('an amphoteric oxide', 'an oxide that reacts with both acids and bases'),
                  ('oxidation state', 'the charge an atom in a compound appears to have when the bonding electrons are counted with the more electronegative atom'),
                  ('an anomalous property', 'a property of the first member of a group that differs from the rest of the group')]

SPECS = {
    'ch01-st1': CH1S1, 'ch01-st2': CH1S2, 'ch01-st3': CH1S3, 'ch01-st4': CH1S4, 'ch01-st5': CH1S5,
    'ch02-st1': CH2S1, 'ch02-st2': CH2S2, 'ch02-st3': CH2S3, 'ch02-st4': CH2S4, 'ch02-st5': CH2S5,
    'ch03-st1': CH3S1, 'ch03-st2': CH3S2, 'ch03-st3': CH3S3, 'ch03-st4': CH3S4,
}

FAMILIES = build_all(P, SPECS)
