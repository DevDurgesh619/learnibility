"""CBSE class 12 chemistry families, units 1-3 (Solutions, Electrochemistry, Chemical Kinetics)."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap
import g11_chemistry_a as x1
import g11_chemistry_c as x7

P = 'cbse-g12-chemistry'
R = 8.314
FAR = 96500

# ---------------- ch01 st1 types of solutions and concentration ----------------

def ppm(r):
    sp = r.choice(['dissolved oxygen in a lake', 'fluoride in drinking water', 'chloroform in a water sample', 'lead in a soil extract', 'nitrate in well water'])
    m = r.choice([0.002, 0.005, 0.01, 0.015, 0.02, 0.05])
    M = r.choice([100, 250, 500, 1000])
    v = m / (M * 1000) * 1e6 if False else m / (M * 1000) * 1e6
    return {'stem': f'A {M} kg sample of water is found to contain {num(m * 1000, 3)} g of a substance ({sp}). Express its concentration in parts per million (ppm) by mass.',
            'answer': f'{sf(m * 1000 / (M * 1000) * 1e6, 3)} ppm', 'key': f'ppm = mass of component / total mass × 10⁶ = {num(m * 1000, 3)} g / {M * 1000} g × 10⁶ = {sf(m * 1000 / (M * 1000) * 1e6, 3)} ppm.',
            'distractors': [f'{sf(m * 1000 / M, 3)} ppm', f'{sf(m * 1000 / (M * 1000) * 1e3, 3)} ppm', f'{sf(m * 1000 / (M * 1000) * 1e9, 3)} ppm']}


SOL_TYPES = [('a gaseous solution', ['a mixture of oxygen and nitrogen gases', 'chloroform mixed with nitrogen gas', 'camphor in nitrogen gas']),
             ('a liquid solution', ['oxygen dissolved in water', 'ethanol dissolved in water', 'glucose dissolved in water']),
             ('a solid solution', ['a solution of hydrogen in palladium', 'amalgam of mercury with sodium', 'copper dissolved in gold'])]

CH1S1 = {
    'topic': 'solutions and their concentration',
    'terms': [('a solution', 'a homogeneous mixture of two or more components'),
              ('a binary solution', 'a solution containing two components'),
              ('molality', 'the number of moles of solute per kilogram of solvent'),
              ('molarity', 'the number of moles of solute dissolved in one litre of solution'),
              ('parts per million', 'the number of parts of a component per million parts of all the components of the solution'),
              ('mole fraction', 'the ratio of the number of moles of one component to the total number of moles of all components')],
    'groups': SOL_TYPES,
    'tf': (['Molality, mole fraction and mass percentage do not depend on temperature.', 'Molarity decreases with increase in temperature.',
            'The solvent is usually the component present in the larger amount.', 'Concentration in ppm is used for very dilute solutions such as pollutants in water.',
            'Brass is a solid solution of zinc in copper.'],
           [('Molality depends on temperature.', 'Molality depends only on masses, so it is independent of temperature.'),
            ('In a gaseous solution the solvent is a liquid.', 'In a gaseous solution the solvent is a gas.'),
            ('Mole fraction of a component can be greater than one.', 'Mole fraction is always less than one; all mole fractions add up to 1.'),
            ('Mass percentage changes with temperature.', 'Mass percentage depends only on masses and does not change with temperature.')]),
    'ar': [('Molality is preferred to molarity in colligative property measurements over a range of temperature.', 'Molality is based on mass of solvent, which does not change with temperature.', 'a', 'Mass is temperature independent; volume is not.'),
           ('Amalgam of mercury with sodium is a solid solution.', 'In this solution the solute is a liquid and the solvent is a solid.', 'a', 'Liquid (Hg) in solid (Na) gives a solid solution.')],
    'fams': [F('C2', 'D2', 'numerical', x1.molarity), F('C2', 'D2', 'numerical', x1.molality), F('C3', 'D3', 'numerical', x1.mole_fraction),
             F('C2', 'D1', 'numerical', x1.mass_percent), F('C3', 'D2', 'numerical', ppm), F('C4', 'D4', 'multi_step', x1.molarity_density, kinds=('long5',)),
             F('C4', 'D4', 'numerical', x1.molarity_to_molality, marks=3)],
    'qa': [('C4', 'D3', 'explain', 'Concentrated nitric acid used in the laboratory is 68% HNO₃ by mass. What other information is needed to express this as molarity, and why?',
            'The density of the solution; molarity needs the volume of solution, which is obtained from mass and density (V = m/d).',
            '1 mark: density; 1 mark: molarity needs volume of solution.')],
}

# ---------------- ch01 st2 Henry's law ----------------

KH = [('N₂', 76.48), ('O₂', 34.86), ('CO₂', 1.67), ('H₂', 69.16), ('He', 144.97), ('Ar', 40.3), ('CH₄', 0.413)]


def henry_x(r):
    g, k = r.choice(KH)
    p = r.choice([0.5, 0.8, 1, 2, 2.5, 5, 10])
    x = p / (k * 1000)
    n = x * 55.5
    return {'stem': f'The Henry\'s law constant of {g} in water at 298 K is {k} kbar. Calculate the mole fraction of {g} in water when its partial pressure is {p} bar, and the number of millimoles dissolved in 1 L (55.5 mol) of water.',
            'answer': f'x = {sci(x)}; {sf(n * 1000, 3)} mmol', 'key': f'p = K_H x ⇒ x = {p} bar / ({k} × 10³ bar) = {sci(x)} (1); n ≈ x × 55.5 = {sci(n)} mol = {sf(n * 1000, 3)} mmol (1).',
            'distractors': [f'x = {sci(p / k)}; {sf(p / k * 55.5 * 1000, 3)} mmol', f'x = {sci(x * 2)}; {sf(n * 2000, 3)} mmol', f'x = {sci(k / p / 1e6)}; {sf(n * 100, 3)} mmol']}


def henry_compare(r):
    (g1, k1), (g2, k2) = r.sample(KH, 2)
    more = g1 if k1 < k2 else g2
    return mcq(f'At 298 K the Henry\'s law constants of {g1} and {g2} in water are {k1} kbar and {k2} kbar. Which gas is more soluble in water at the same partial pressure?',
               more, [g2 if more == g1 else g1, 'both are equally soluble', 'cannot be predicted from K_H'],
               f'x = p/K_H, so the gas with the smaller K_H ({more}) has the higher solubility.', r)


CH1S2 = {
    'topic': "solubility and Henry's law",
    'terms': [("Henry's law", 'the law that at constant temperature the solubility of a gas in a liquid is directly proportional to the partial pressure of the gas'),
              ('solubility', 'the maximum amount of a substance that can be dissolved in a specified amount of solvent at a given temperature'),
              ('a saturated solution', 'a solution in which no more solute can be dissolved at the same temperature and pressure'),
              ('the bends', 'a painful condition in deep-sea divers caused by nitrogen bubbles forming in the blood on rapid ascent'),
              ('anoxia', 'a condition of low oxygen in blood and tissues, seen in climbers at high altitudes')],
    'features': {'intro': 'Read the situation:', 'q': 'Which application or effect of gas solubility is illustrated', 'what': 'effect', 'long': False,
                 'items': [('sealing soft drinks under high CO₂ pressure', ['soda bottles are sealed under high pressure', 'fizz appears when the bottle is opened', 'the solubility of CO₂ increases with pressure']),
                           ('the bends in scuba divers', ['divers breathe air under high pressure deep under water', 'on rapid ascent nitrogen comes out of the blood as bubbles', 'tanks are diluted with helium to avoid it']),
                           ('anoxia at high altitude', ['climbers feel weak and unable to think clearly', 'the partial pressure of oxygen is low at high altitude', 'less oxygen dissolves in the blood']),
                           ('aquatic life in cold water', ['fish survive better in cold water', 'more oxygen dissolves at lower temperature', 'gas dissolution is exothermic'])]},
    'tf': (['The solubility of a gas in a liquid decreases with increase in temperature.', 'A higher value of K_H means a lower solubility of the gas.',
            'Scuba divers use air diluted with helium to reduce the bends.', 'Dissolution of a gas in a liquid is generally exothermic.',
            'Pressure has no significant effect on the solubility of solids in liquids.'],
           [('The solubility of gases in water increases with temperature.', 'Gas solubility decreases with rise in temperature because dissolution is exothermic.'),
            ('A higher K_H value means higher solubility of the gas.', 'x = p/K_H, so higher K_H means lower solubility.'),
            ('Pressure greatly increases the solubility of solids in liquids.', 'Solids and liquids are nearly incompressible, so pressure has little effect.'),
            ('Aquatic species are more comfortable in warm water.', 'Cold water holds more dissolved oxygen, so aquatic life is more comfortable in cold water.')]),
    'ar': [('Soft drink bottles are sealed under high pressure.', 'The solubility of CO₂ in water increases with its partial pressure.', 'a', "Henry's law."),
           ('The value of K_H increases with temperature.', 'The solubility of gases in liquids decreases with increase in temperature.', 'a', 'Lower solubility at higher T means a larger K_H.')],
    'fams': [F('C3', 'D3', 'numerical', henry_x, marks=2), F('C3', 'D2', 'mcq', henry_compare)],
    'qa': [('C4', 'D4', 'explain', 'Why do climbers at high altitudes, such as on the way to Ladakh, often feel weak and unable to think clearly?',
            'At high altitude the partial pressure of oxygen is low; by Henry\'s law less oxygen dissolves in the blood (anoxia).', '1 mark: low partial pressure of O₂; 1 mark: Henry\'s law ⇒ low dissolved O₂.')],
}

# ---------------- ch01 st3 Raoult's law ----------------

PAIRS = [('benzene', 'toluene', 12.8, 3.85), ('n-hexane', 'n-heptane', 20.2, 6.1), ('chlorobenzene', 'bromobenzene', 1.6, 0.6),
         ('ethyl bromide', 'ethyl chloride', 63.0, 160.0), ('benzene', 'toluene', 75, 22)]


def raoult(r):
    a, b, pa, pb = r.choice(PAIRS)
    xa = r.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8])
    pt = xa * pa + (1 - xa) * pb
    ya = xa * pa / pt
    unit = 'kPa'
    return {'stem': f'The vapour pressures of pure {a} and {b} at a certain temperature are {pa} {unit} and {pb} {unit}. Assuming ideal behaviour, calculate the total vapour pressure of a solution with mole fraction of {a} = {xa}, and the mole fraction of {a} in the vapour.',
            'answer': f'p(total) = {sf(pt, 3)} {unit}; y({a}) = {ya:.3f}',
            'key': f'p = x_A p°_A + x_B p°_B = {xa} × {pa} + {num(1 - xa, 2)} × {pb} = {sf(pt, 3)} {unit} (2); y_A = x_A p°_A / p = {sf(xa * pa, 3)}/{sf(pt, 3)} = {ya:.3f} (1).',
            'distractors': [f'p(total) = {sf(pa + pb, 3)} {unit}; y({a}) = {xa}', f'p(total) = {sf(pt, 3)} {unit}; y({a}) = {xa}', f'p(total) = {sf((pa + pb) / 2, 3)} {unit}; y({a}) = {1 - ya:.3f}']}


def rlvp_molar_mass(r):
    solv, Ms, p0 = r.choice([('water', 18, 3.17), ('benzene', 78, 12.8), ('water', 18, 23.8), ('carbon disulphide', 76, 53.3)])
    w2 = r.choice([2, 5, 10, 18, 20])
    w1 = r.choice([90, 100, 150, 200])
    M2 = r.choice([60, 92, 128, 180, 342])
    x2 = (w2 / M2) / (w2 / M2 + w1 / Ms)
    p = round(p0 * (1 - x2), 3)
    return {'stem': f'The vapour pressure of pure {solv} is {p0} kPa. When {w2} g of a non-volatile solute is dissolved in {w1} g of {solv}, the vapour pressure becomes {p:.3f} kPa. Calculate the molar mass of the solute (use the dilute-solution approximation).',
            'answer': f'≈ {sf((w2 * Ms * p0) / (w1 * (p0 - p)), 3)} g mol⁻¹',
            'key': f'(p° − p)/p° ≈ n₂/n₁ = (w₂ M₁)/(M₂ w₁) (1) ⇒ M₂ = w₂ M₁ p° / (w₁ Δp) = {w2} × {Ms} × {p0}/({w1} × {p0 - p:.3f}) = {sf((w2 * Ms * p0) / (w1 * (p0 - p)), 3)} g mol⁻¹ (2).'}


DEV = [('a solution showing positive deviation from Raoult\'s law', ['ethanol + acetone', 'carbon disulphide + acetone', 'ethanol + water', 'benzene + methanol']),
       ('a solution showing negative deviation from Raoult\'s law', ['chloroform + acetone', 'nitric acid + water', 'phenol + aniline', 'hydrochloric acid + water']),
       ('a nearly ideal solution', ['n-hexane + n-heptane', 'benzene + toluene', 'bromoethane + chloroethane', 'chlorobenzene + bromobenzene'])]

CH1S3 = {
    'topic': "vapour pressure and Raoult's law",
    'terms': [("Raoult's law", 'the law that for a solution of volatile liquids the partial vapour pressure of each component is directly proportional to its mole fraction'),
              ('an ideal solution', 'a solution that obeys Raoult\'s law over the entire range of concentration, with ΔmixH = 0 and ΔmixV = 0'),
              ('an azeotrope', 'a binary mixture having the same composition in liquid and vapour phase and boiling at a constant temperature'),
              ('a minimum boiling azeotrope', 'an azeotrope formed by solutions showing large positive deviation from Raoult\'s law'),
              ('a maximum boiling azeotrope', 'an azeotrope formed by solutions showing large negative deviation from Raoult\'s law'),
              ('relative lowering of vapour pressure', 'the ratio (p° − p)/p°, equal to the mole fraction of the solute for a dilute solution')],
    'groups': DEV,
    'features': {'intro': 'A binary liquid mixture shows:', 'q': 'What type of solution is it', 'what': 'solution',
                 'items': [('a solution with positive deviation', ['A–B interactions weaker than A–A and B–B', 'ΔmixH positive (heat absorbed on mixing)', 'ΔmixV positive (volume increases)', 'forms minimum boiling azeotrope at a certain composition']),
                           ('a solution with negative deviation', ['A–B interactions stronger than A–A and B–B', 'ΔmixH negative (heat evolved on mixing)', 'ΔmixV negative (volume decreases)', 'forms maximum boiling azeotrope at a certain composition']),
                           ('an ideal solution', ['A–B interactions nearly equal to A–A and B–B', 'ΔmixH = 0', 'ΔmixV = 0', 'obeys Raoult\'s law over the entire range'])]},
    'tf': (['An ideal solution has ΔmixH = 0 and ΔmixV = 0.', '95% ethanol by volume is a minimum boiling azeotrope.', 'Nitric acid and water (68% HNO₃) form a maximum boiling azeotrope.',
            'In an ideal solution the vapour is richer in the more volatile component.', 'Chloroform and acetone form hydrogen bonds on mixing.'],
           [('A mixture of chloroform and acetone shows positive deviation.', 'It shows negative deviation because new hydrogen bonds form between them.'),
            ('Azeotropes can be separated by fractional distillation.', 'Azeotropes boil at constant composition, so they cannot be separated by fractional distillation.'),
            ('In positive deviation the vapour pressure is lower than predicted by Raoult\'s law.', 'In positive deviation the vapour pressure is higher than predicted.'),
            ('Ethanol and water show negative deviation from Raoult\'s law.', 'Ethanol–water shows positive deviation (H-bonds in ethanol are broken).')]),
    'ar': [('A solution of chloroform and acetone shows negative deviation from Raoult\'s law.', 'Chloroform forms a hydrogen bond with acetone, so A–B attractions are stronger.', 'a', 'Stronger A–B attraction lowers the escaping tendency.'),
           ('Ethanol cannot be obtained 100% pure by fractional distillation of its aqueous solution.', 'Ethanol and water form a minimum boiling azeotrope at about 95% ethanol.', 'a', 'At azeotropic composition liquid and vapour have the same composition.')],
    'fams': [F('C3', 'D3', 'numerical', raoult, marks=3), F('C4', 'D4', 'multi_step', rlvp_molar_mass, kinds=('long5',))],
    'qa': [('C4', 'D4', 'explain', 'When 50 mL of ethanol is mixed with 50 mL of water the volume of the solution is slightly less than 100 mL, yet the mixture shows positive deviation in vapour pressure. Discuss what each observation tells you.',
            'Volume contraction shows strong ethanol–water H-bonding and close packing; positive deviation in vapour pressure arises because ethanol–ethanol H-bonds are broken and the escaping tendency increases. Real solutions are more complex than the simple model.',
            '1 mark: interpretation of volume; 1 mark: interpretation of vapour pressure.')],
}

# ---------------- ch01 st4 colligative properties ----------------

SOLV = [('water', 0.52, 1.86), ('benzene', 2.53, 5.12)]
SOLUTES = [('glucose', 180, 1), ('urea', 60, 1), ('sucrose', 342, 1), ('NaCl', 58.5, 2), ('KCl', 74.5, 2), ('CaCl₂', 111, 3), ('K₂SO₄', 174, 3), ('MgSO₄', 120, 2)]


def dTb(r):
    s, M2, i = r.choice(SOLUTES)
    w2 = r.choice([1, 2, 5, 10, 18, 20, 30])
    w1 = r.choice([100, 200, 250, 500])
    m = w2 / M2 / (w1 / 1000)
    dt = i * 0.52 * m
    if dt < 0.05:
        raise ValueError('elevation too small to show')
    return {'stem': f'{w2} g of {s} is dissolved in {w1} g of water. Calculate the boiling point of the solution. (K_b of water = 0.52 K kg mol⁻¹' + (f'; assume complete dissociation, i = {i})' if i > 1 else ')'),
            'answer': f'ΔT_b = {sf(dt, 3)} K; T_b = {373.15 + dt:.2f} K', 'key': f'm = {w2}/{M2} ÷ {w1 / 1000:g} = {sf(m, 3)} mol kg⁻¹ (1); ΔT_b = iK_b m = {i} × 0.52 × {sf(m, 3)} = {dt:.3f} K (1); T_b = 373.15 + {dt:.3f} = {373.15 + dt:.2f} K.',
            'distractors': [f'ΔT_b = {sf(dt, 3)} K; T_b = {373.15 - dt:.2f} K', f'ΔT_b = {sf(dt / i, 3)} K; T_b = {373.15 + dt / i:.2f} K' if i > 1 else f'ΔT_b = {sf(dt * 2, 3)} K; T_b = {373.15 + dt * 2:.2f} K',
                            f'ΔT_b = {sf(1.86 * i * m, 3)} K; T_b = {373.15 + 1.86 * i * m:.2f} K']}


def dTf(r):
    solv, Kb, Kf = r.choice(SOLV)
    s, M2, i = r.choice(SOLUTES if solv == 'water' else [('naphthalene', 128, 1), ('benzoic acid (assume no association)', 122, 1), ('anthracene', 178, 1)])
    w2 = r.choice([1, 2, 3, 5, 10])
    w1 = r.choice([50, 100, 200, 250])
    m = w2 / M2 / (w1 / 1000)
    dt = i * Kf * m
    T0 = 273.15 if solv == 'water' else 278.6
    return {'stem': f'Calculate the freezing point of a solution containing {w2} g of {s} in {w1} g of {solv}. (K_f = {Kf} K kg mol⁻¹; freezing point of pure {solv} = {T0} K' + (f'; i = {i})' if i > 1 else ')'),
            'answer': f'{T0 - dt:.2f} K', 'key': f'm = {sf(m, 3)} mol kg⁻¹ (1); ΔT_f = iK_f m = {dt:.3f} K (1); T_f = {T0} − {dt:.3f} = {T0 - dt:.2f} K.',
            'distractors': [f'{T0 + dt:.2f} K', f'{T0 - dt / i:.2f} K' if i > 1 else f'{T0 - dt * 2:.2f} K', f'{T0 - Kb * i * m:.2f} K']}


def molar_mass_dTf(r):
    solv, Kb, Kf = r.choice(SOLV)
    M2 = r.choice([60, 92, 128, 180, 256, 342])
    w2 = r.choice([1, 2, 2.5, 5])
    w1 = r.choice([50, 75, 100, 200])
    dt = Kf * w2 / M2 / (w1 / 1000)
    dt = round(dt, 3)
    Mc = Kf * w2 * 1000 / (dt * w1)
    return {'stem': f'{w2} g of a non-electrolyte dissolved in {w1} g of {solv} lowered its freezing point by {dt} K. Calculate the molar mass of the solute. (K_f of {solv} = {Kf} K kg mol⁻¹)',
            'answer': f'{sf(Mc, 3)} g mol⁻¹', 'key': f'M₂ = K_f × w₂ × 1000 / (ΔT_f × w₁) = {Kf} × {w2} × 1000/({dt} × {w1}) = {sf(Mc, 3)} g mol⁻¹.',
            'distractors': [f'{sf(Mc / 1000, 3)} g mol⁻¹', f'{sf(Kb * w2 * 1000 / (dt * w1), 3)} g mol⁻¹', f'{sf(Mc * 2, 3)} g mol⁻¹']}


def osmotic(r):
    s, M2, i = r.choice(SOLUTES + [('a protein', 60000, 1), ('a polymer', 185000, 1)])
    w2 = r.choice([0.5, 1, 1.26, 2, 5]) if M2 < 1000 else r.choice([0.5, 1.0, 1.26, 2.0])
    V = r.choice([100, 250, 500, 1000])
    T = r.choice([300, 310, 298, 310])
    C = w2 / M2 / (V / 1000)
    pi = i * C * 0.083 * T
    return {'stem': f'Calculate the osmotic pressure of a solution containing {w2} g of {s} (molar mass {M2} g mol⁻¹) in {V} mL of solution at {T} K. (R = 0.083 L bar mol⁻¹ K⁻¹' + (f'; i = {i})' if i > 1 else ')'),
            'answer': f'{sf(pi, 3)} bar', 'key': f'C = {w2}/{M2} ÷ {V / 1000:g} = {sf(C, 3)} mol L⁻¹ (1); π = iCRT = {i} × {sf(C, 3)} × 0.083 × {T} = {sf(pi, 3)} bar (1).',
            'distractors': [f'{sf(pi / 0.083 * 8.314, 3)} bar', f'{sf(pi * 1000 / V if V != 1000 else pi * 10, 3)} bar', f'{sf(pi / i if i > 1 else pi * 2, 3)} bar']}


def vant_hoff(r):
    kind = r.choice(['diss', 'assoc'])
    if kind == 'diss':
        salt, n = r.choice([('KCl', 2), ('NaCl', 2), ('MgCl₂', 3), ('K₂SO₄', 3), ('Ca(NO₃)₂', 3)])
        al = r.choice([0.6, 0.7, 0.8, 0.85, 0.9])
        i = 1 + al * (n - 1)
        return {'stem': f'{salt} is {int(al * 100)}% dissociated in an aqueous solution. Calculate the van\'t Hoff factor.',
                'answer': f'i = {i:.2f}', 'key': f'i = 1 + α(n − 1) with n = {n} ions: 1 + {al}({n - 1}) = {i:.2f}.',
                'distractors': [f'i = {n:.2f}', f'i = {1 - al * (n - 1) if 1 - al * (n - 1) > 0 else al:.2f}', f'i = {1 + al:.2f}' if n == 3 else f'i = {al * n:.2f}']}
    al = r.choice([0.6, 0.7, 0.8, 0.9, 0.95])
    i = 1 - al / 2
    return {'stem': f'Acetic acid dimerises in benzene: 2CH₃COOH ⇌ (CH₃COOH)₂. If the degree of association is {al}, what is the van\'t Hoff factor?',
            'answer': f'i = {i:.3f}', 'key': f'i = 1 − α + α/2 = 1 − α/2 = 1 − {al}/2 = {i:.3f}.',
            'distractors': [f'i = {1 + al / 2:.3f}', f'i = {1 - al:.3f}', f'i = {2 - al:.3f}']}


def abnormal(r):
    s, M2, n = r.choice([('NaCl', 58.5, 2), ('KCl', 74.5, 2), ('MgCl₂', 95, 3), ('K₂SO₄', 174, 3)])
    w2 = r.choice([1, 2, 5])
    w1 = r.choice([100, 200, 250])
    al = r.choice([0.7, 0.8, 0.9])
    i = 1 + al * (n - 1)
    m = w2 / M2 / (w1 / 1000)
    dt = round(i * 1.86 * m, 3)
    i_obs = dt / (1.86 * m)
    a_obs = (i_obs - 1) / (n - 1)
    return {'stem': f'A solution of {w2} g of {s} in {w1} g of water freezes at {273.15 - dt:.3f} K. Calculate the van\'t Hoff factor and the degree of dissociation of {s}. (K_f = 1.86 K kg mol⁻¹; freezing point of water 273.15 K)',
            'answer': f'i = {i_obs:.2f}; α = {a_obs:.2f}',
            'key': f'Calculated ΔT_f (no dissociation) = 1.86 × {sf(m, 3)} = {1.86 * m:.4f} K (1); observed ΔT_f = {dt} K, so i = {i_obs:.2f} (1); α = (i − 1)/(n − 1) = {a_obs:.2f} (1).'}


CH1S4 = {
    'topic': 'colligative properties',
    'terms': [('a colligative property', 'a property of a dilute solution that depends only on the number of solute particles and not on their nature'),
              ('osmosis', 'the flow of solvent molecules through a semipermeable membrane from pure solvent (or dilute solution) to the more concentrated solution'),
              ('osmotic pressure', 'the excess pressure that must be applied on the solution side to just stop osmosis'),
              ('reverse osmosis', 'the flow of solvent from the solution to pure solvent when a pressure larger than the osmotic pressure is applied to the solution'),
              ('isotonic solutions', 'solutions having the same osmotic pressure at a given temperature'),
              ("the van't Hoff factor", 'the ratio of the normal molar mass to the abnormal (observed) molar mass of a solute'),
              ('the ebullioscopic constant', 'the elevation of boiling point for a one molal solution, K_b'),
              ('the cryoscopic constant', 'the depression of freezing point for a one molal solution, K_f')],
    'groups': [('a colligative property', ['relative lowering of vapour pressure', 'elevation of boiling point', 'depression of freezing point', 'osmotic pressure']),
               ('a property that is not colligative', ['viscosity', 'refractive index', 'surface tension', 'colour of the solution'])],
    'orders': [('increasing order of depression in freezing point for 0.1 m aqueous solutions (complete dissociation)', ['glucose', 'NaCl', 'CaCl₂', 'Al₂(SO₄)₃'],
                'ΔT_f ∝ i: glucose 1, NaCl 2, CaCl₂ 3, Al₂(SO₄)₃ 5.', '<'),
               ('increasing order of boiling point of 0.1 m aqueous solutions (complete dissociation)', ['urea', 'KCl', 'K₂SO₄', 'K₄[Fe(CN)₆]'], 'ΔT_b ∝ i: 1, 2, 3, 5.', '<')],
    'tf': (['Osmotic pressure is used to find molar masses of proteins and polymers.', '0.9% NaCl solution (normal saline) is isotonic with blood plasma.',
            'Desalination of sea water can be done by reverse osmosis.', 'For association of solute particles, i is less than 1.', 'K_f of water is 1.86 K kg mol⁻¹.'],
           [('Colligative properties depend on the nature of the solute.', 'They depend only on the number of solute particles.'),
            ('Red blood cells placed in a hypertonic NaCl solution swell and burst.', 'In a hypertonic solution water leaves the cells and they shrink; they swell in a hypotonic solution.'),
            ('For dissociation of a solute, i is less than 1.', 'For dissociation i > 1; for association i < 1.'),
            ('Freezing point of a solution is higher than that of the pure solvent.', 'Adding a non-volatile solute lowers the freezing point.')]),
    'ar': [('Osmotic pressure is preferred for finding molar masses of proteins.', 'Osmotic pressure is measured at room temperature and is large even for very dilute solutions.', 'a', 'Biomolecules are unstable at high temperature and are only slightly soluble.'),
           ('The molar mass of acetic acid in benzene is found to be about 120 g mol⁻¹.', 'Acetic acid dimerises in benzene due to hydrogen bonding.', 'a', 'Association halves the number of particles, doubling the apparent molar mass.'),
           ('Ethylene glycol is added to water in car radiators in cold places like Leh.', 'Ethylene glycol lowers the freezing point of water.', 'a', 'Antifreeze depresses the freezing point.')],
    'fams': [F('C3', 'D2', 'numerical', dTb), F('C3', 'D3', 'numerical', dTf), F('C3', 'D3', 'numerical', molar_mass_dTf, marks=3),
             F('C3', 'D3', 'numerical', osmotic), F('C2', 'D2', 'numerical', vant_hoff), F('C4', 'D5', 'multi_step', abnormal, kinds=('long5',))],
    'qa': [('C4', 'D4', 'explain', 'Why does a raw mango placed in concentrated salt solution shrivel, while a dried raisin placed in water swells?',
            'The salt solution is hypertonic, so water moves out of the mango cells by osmosis; water enters the raisin cells (hypertonic inside) from pure water.', '1 mark each with osmosis direction.'),
           ('C4', 'D3', 'case', 'Read and answer. People living in hilly regions of Himachal Pradesh add ethylene glycol to car radiators in winter. In coastal cities, reverse osmosis plants supply drinking water.\n(i) Which colligative property is used in the first case? (1 mark)\n(ii) Why is reverse osmosis called "reverse"? (1 mark)\n(iii) Calculate the mass of ethylene glycol (62 g mol⁻¹) needed per kg of water to lower its freezing point by 6 K. (K_f = 1.86 K kg mol⁻¹) (2 marks)',
            '(i) Depression of freezing point. (ii) Pressure greater than the osmotic pressure forces solvent from solution to solvent side, opposite to osmosis. (iii) m = 6/1.86 = 3.23 mol kg⁻¹; mass = 3.23 × 62 = 200 g.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',))],
}

# ---------------- ch02 electrochemistry ----------------

E0 = x7.E0
E0_NM = x7.E0_NM


def cell_notation(r):
    a, b = r.sample(E0, 2)
    an, ca = (a, b) if a[1] < b[1] else (b, a)
    note = f'{an[2]}(s) | {an[3]}(aq) || {ca[3]}(aq) | {ca[2]}(s)'
    return {'stem': f'Write the cell notation for a galvanic cell made from the {a[0]} and {b[0]} couples (E° = {a[1]:+.2f} V and {b[1]:+.2f} V), and write the half reactions at the anode and cathode.'.replace('-', '−'),
            'answer': note, 'key': f'Anode (lower E°, oxidation) on the left: {an[2]} → {an[3]} + ne⁻; cathode (reduction): {ca[3]} + ne⁻ → {ca[2]} (1); notation {note} (1).',
            'distractors': [f'{ca[2]}(s) | {ca[3]}(aq) || {an[3]}(aq) | {an[2]}(s)', f'{an[3]}(aq) | {an[2]}(s) || {ca[2]}(s) | {ca[3]}(aq)', f'{an[2]}(s) | {ca[3]}(aq) || {an[3]}(aq) | {ca[2]}(s)']}


NERNST = [('Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)', 1.10, 2, 'Zn²⁺', 'Cu²⁺', 1, 1), ('Mg(s) + 2Ag⁺(aq) → Mg²⁺(aq) + 2Ag(s)', 3.17, 2, 'Mg²⁺', 'Ag⁺', 1, 2),
          ('Ni(s) + 2Ag⁺(aq) → Ni²⁺(aq) + 2Ag(s)', 1.05, 2, 'Ni²⁺', 'Ag⁺', 1, 2), ('Fe(s) + Cu²⁺(aq) → Fe²⁺(aq) + Cu(s)', 0.78, 2, 'Fe²⁺', 'Cu²⁺', 1, 1),
          ('Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)', 0.46, 2, 'Cu²⁺', 'Ag⁺', 1, 2), ('Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g, 1 bar)', 0.76, 2, 'Zn²⁺', 'H⁺', 1, 2),
          ('Mg(s) + Cu²⁺(aq) → Mg²⁺(aq) + Cu(s)', 2.70, 2, 'Mg²⁺', 'Cu²⁺', 1, 1), ('2Al(s) + 3Ni²⁺(aq) → 2Al³⁺(aq) + 3Ni(s)', 1.41, 6, 'Al³⁺', 'Ni²⁺', 2, 3)]


def nernst(r):
    eq, E0c, n, p, q, cp, cq = r.choice(NERNST)
    a = r.choice([0.001, 0.01, 0.1, 0.5, 1.0, 0.05])
    b = r.choice([0.001, 0.01, 0.1, 0.5, 1.0, 0.2])
    Q = a ** cp / b ** cq
    E = E0c - 0.059 / n * math.log10(Q)
    return {'stem': f'Calculate the emf of the cell in which the reaction {eq} occurs, when [{p}] = {a} M and [{q}] = {b} M at 298 K. (E°cell = {E0c} V)',
            'answer': f'{E:.3f} V', 'key': f'E = E° − (0.059/{n}) log ([{p}]{"²" if cp == 2 else ""}/[{q}]{"²" if cq == 2 else ("³" if cq == 3 else "")}) (1) = {E0c} − (0.059/{n}) log({sf(Q, 3)}) (1) = {E:.3f} V (1).',
            'distractors': [f'{E0c + 0.059 / n * math.log10(Q):.3f} V', f'{E0c - 0.059 * math.log10(Q):.3f} V', f'{E0c:.3f} V']}


def dG_E(r):
    eq, E0c, n, *_ = r.choice(NERNST)
    dG = -n * FAR * E0c / 1000
    return {'stem': f'Calculate the standard Gibbs energy change for the cell reaction {eq}, given E°cell = {E0c} V. (F = 96500 C mol⁻¹)',
            'answer': f'{sf(dG, 3)} kJ mol⁻¹', 'key': f'ΔᵣG° = −nFE°cell = −{n} × 96500 × {E0c} = {sf(dG * 1000, 4)} J mol⁻¹ = {sf(dG, 3)} kJ mol⁻¹ (n = {n}).',
            'distractors': [f'{sf(-dG, 3)} kJ mol⁻¹', f'{sf(dG / n, 3)} kJ mol⁻¹' if n > 1 else f'{sf(dG * 2, 3)} kJ mol⁻¹', f'{sf(dG * 1000, 3)} kJ mol⁻¹']}


def K_from_E(r):
    eq, E0c, n, *_ = r.choice([x for x in NERNST if x[1] < 1.2])
    lk = n * E0c / 0.059
    return {'stem': f'Calculate the equilibrium constant at 298 K for the reaction {eq}, E°cell = {E0c} V.',
            'answer': f'log K = {lk:.2f}; K ≈ {sci(10 ** lk, 2)}',
            'key': f'log K = nE°/0.059 = {n} × {E0c}/0.059 = {lk:.2f} (1); K = antilog = {sci(10 ** lk, 2)} (1).',
            'distractors': [f'log K = {E0c / 0.059:.2f}; K ≈ {sci(10 ** (E0c / 0.059), 2)}', f'log K = {-lk:.2f}; K ≈ {sci(10 ** -lk, 2)}', f'log K = {lk * 2.303:.2f}; K ≈ {sci(10 ** (lk * 2.303), 2)}']}


def ph_hydrogen(r):
    pH = r.choice([1, 2, 3, 4, 5, 6, 10, 12])
    E = -0.059 * pH
    return {'stem': f'Calculate the electrode potential of a hydrogen electrode in contact with a solution of pH {pH} at 298 K (p(H₂) = 1 bar).',
            'answer': f'{E:.3f} V', 'key': f'H⁺ + e⁻ → ½H₂; E = 0 − 0.059 log (1/[H⁺]) = −0.059 × pH = {E:.3f} V.',
            'distractors': [f'{-E:.3f} V', f'{E / 2:.3f} V', f'{-0.0591 * (14 - pH):.3f} V']}


CH2S1 = {
    'topic': 'galvanic cells and electrode potentials',
    'terms': x7.CH7S4['terms'] + [('the standard electrode potential', 'the electrode potential when all species in the half-cell are at unit concentration (1 M), 1 bar and 298 K'),
                                   ('the cell potential (emf)', 'the difference between the electrode potentials of the cathode and the anode when no current is drawn')],
    'tf': x7.CH7S4['tf'],
    'orders': x7.CH7S4['orders'],
    'ar': x7.CH7S4['ar'] + [('A salt bridge is used in a Daniell cell.', 'It allows the flow of ions between the two solutions and maintains electrical neutrality.', 'a', 'Without it charge builds up and current stops.')],
    'fams': [F('C3', 'D3', 'numerical', x7.ecell), F('C3', 'D3', 'mcq', x7.strongest), F('C4', 'D3', 'explain', x7.displace), F('C2', 'D2', 'short', cell_notation)],
    'qa': x7.CH7S4['qa'] + [('C4', 'D3', 'explain', 'Why is the standard hydrogen electrode not convenient for routine use, and what is used instead?',
                              'It is difficult to maintain 1 bar H₂ and unit H⁺ activity, and platinum gets poisoned; secondary reference electrodes such as the calomel electrode are used.', '1 mark each.')],
}

CH2S2 = {
    'topic': 'the Nernst equation and Gibbs energy of cells',
    'terms': [('the Nernst equation', 'the equation relating the electrode or cell potential to the concentrations of the species involved'),
              ('a concentration cell', 'a cell in which both electrodes are of the same material but dip into solutions of different concentration'),
              ('Gibbs energy of a cell reaction', 'the maximum electrical work obtainable, ΔᵣG = −nFE(cell)'),
              ('the Faraday constant', 'the charge on one mole of electrons, about 96487 C mol⁻¹ (96500 C mol⁻¹)')],
    'tf': (['At equilibrium the emf of a cell is zero.', 'ΔᵣG° = −nFE°cell.', 'A positive E°cell means the cell reaction is spontaneous.',
            'E°cell is an intensive property.', 'log K = nE°cell/0.059 at 298 K.'],
           [('E°cell depends on the number of electrons written in the balanced equation.', 'E°cell is intensive and does not change when the equation is multiplied; ΔG° does.'),
            ('At equilibrium E°cell = 0.', 'At equilibrium Ecell = 0; E°cell is a constant for the reaction.'),
            ('A negative ΔG means E is negative.', 'ΔG = −nFE, so a negative ΔG corresponds to a positive E.'),
            ('Increasing [Cu²⁺] lowers the emf of the Daniell cell.', 'Raising [Cu²⁺] (a reactant) increases the emf.')]),
    'ar': [('The emf of a Daniell cell increases when [Cu²⁺] is increased.', 'In the Nernst equation, increasing a reactant concentration decreases log Q.', 'a', 'E = E° − (0.059/2) log([Zn²⁺]/[Cu²⁺]).'),
           ('E°cell is an intensive property.', 'ΔᵣG° of a cell reaction is an extensive property.', 'b', 'Both true; R is a different fact, not why E° is intensive.')],
    'fams': [F('C3', 'D4', 'multi_step', nernst, kinds=('long5',)), F('C3', 'D2', 'numerical', dG_E), F('C3', 'D3', 'numerical', K_from_E), F('C3', 'D3', 'numerical', ph_hydrogen)],
    'qa': [('C4', 'D4', 'explain', 'The emf of the cell Zn | Zn²⁺(0.1 M) || Cu²⁺(1 M) | Cu is slightly more than 1.10 V. Explain using the Nernst equation, and say what happens to the emf as the cell is used.',
            'E = 1.10 − (0.059/2) log(0.1/1) = 1.13 V; as the cell works [Zn²⁺] rises and [Cu²⁺] falls, Q increases and E decreases until it becomes zero at equilibrium.', '1 mark calculation; 1 mark change with use.'),
           ('C4', 'D5', 'long', '(a) Derive the relation between E°cell and the equilibrium constant. (b) Calculate K for Cu(s) + 2Ag⁺ → Cu²⁺ + 2Ag(s), E° = 0.46 V. (c) Calculate ΔᵣG° and comment on the extent of the reaction.',
            '(a) ΔG° = −nFE° and ΔG° = −2.303RT log K ⇒ log K = nFE°/2.303RT = nE°/0.059 at 298 K. (b) log K = 2 × 0.46/0.059 = 15.6; K = 3.9 × 10¹⁵ (≈ 3.92 × 10¹⁵). (c) ΔG° = −2 × 96500 × 0.46 = −88.8 kJ mol⁻¹; very large K ⇒ reaction goes almost to completion.',
            '(a) 2 marks (b) 1.5 marks (c) 1.5 marks.')],
}

KAPPA_E = [('KCl', 149.9), ('NaCl', 126.4), ('HCl', 425.9), ('NaOH', 248.1), ('CH₃COONa', 91.0), ('KNO₃', 145.0)]
LAM0 = {'H⁺': 349.6, 'Na⁺': 50.1, 'K⁺': 73.5, 'Ca²⁺': 119.0, 'Mg²⁺': 106.0, 'Cl⁻': 76.3, 'Br⁻': 78.1, 'SO₄²⁻': 160.0, 'CH₃COO⁻': 40.9, 'OH⁻': 199.1, 'NO₃⁻': 71.5}


def cell_const(r):
    Rr = r.choice([55, 100, 150, 245, 520, 1500])
    c, k = r.choice([(0.1, 0.0129), (0.01, 0.00141), (0.02, 0.00277), (0.05, 0.00667), (0.001, 0.000147)])
    G = k * Rr
    Rm = k * 1000 / c
    return {'stem': f'The resistance of a conductivity cell containing {c} M KCl solution is {Rr} Ω. If the conductivity of this solution is {k} S cm⁻¹, calculate the cell constant and the molar conductivity.',
            'answer': f'G* = {sf(G, 3)} cm⁻¹; Λm = {sf(Rm, 3)} S cm² mol⁻¹',
            'key': f'G* = κ × R = {k} × {Rr} = {sf(G, 3)} cm⁻¹ (1); Λm = κ × 1000/c = {k} × 1000/{c} = {sf(Rm, 3)} S cm² mol⁻¹ (1).',
            'distractors': [f'G* = {sf(k / Rr, 3)} cm⁻¹; Λm = {sf(Rm, 3)} S cm² mol⁻¹', f'G* = {sf(G, 3)} cm⁻¹; Λm = {sf(k / c, 3)} S cm² mol⁻¹', f'G* = {sf(Rr / k, 3)} cm⁻¹; Λm = {sf(Rm * 10, 3)} S cm² mol⁻¹']}


WEAK_LAM = [('CH₃COOH', [('CH₃COONa', 91.0), ('HCl', 425.9), ('NaCl', 126.4)], 390.5, 1.8e-5),
            ('NH₄OH', [('NH₄Cl', 129.8), ('NaOH', 248.1), ('NaCl', 126.4)], 251.5, 1.8e-5),
            ('HCOOH', [('HCOONa', 104.6), ('HCl', 425.9), ('NaCl', 126.4)], 404.1, 1.8e-4)]


def kohlrausch(r):
    w, data, L0, Ka = r.choice(WEAK_LAM)
    s = ' + '.join(f'Λ°({d[0]})' if i < 2 else f'− Λ°({d[0]})' for i, d in enumerate(data)).replace('+ −', '−')
    val = data[0][1] + data[1][1] - data[2][1]
    return {'stem': f'Λ°m of {", ".join(f"{d[0]} = {d[1]}" for d in data)} S cm² mol⁻¹. Use Kohlrausch\'s law to calculate Λ°m for {w}.',
            'answer': f'{val:.1f} S cm² mol⁻¹', 'key': f'Λ°({w}) = {s} = {data[0][1]} + {data[1][1]} − {data[2][1]} = {val:.1f} S cm² mol⁻¹.',
            'distractors': [f'{data[0][1] + data[1][1] + data[2][1]:.1f} S cm² mol⁻¹', f'{data[0][1] - data[1][1] + data[2][1]:.1f} S cm² mol⁻¹', f'{data[1][1] - data[0][1]:.1f} S cm² mol⁻¹']}


def degree_diss(r):
    w, data, L0, Ka = r.choice(WEAK_LAM)
    c = r.choice([0.001, 0.0025, 0.005, 0.01, 0.02])
    al = math.sqrt(Ka / c)
    if al > 0.5:
        raise ValueError
    Lm = al * L0
    Lm = round(Lm, 2)
    al2 = Lm / L0
    K = c * al2 ** 2 / (1 - al2)
    return {'stem': f'The molar conductivity of {c} M {w} is {Lm} S cm² mol⁻¹. If Λ°m for {w} is {L0} S cm² mol⁻¹, calculate its degree of dissociation and dissociation constant.',
            'answer': f'α = {al2:.4f}; K = {sci(K)} mol L⁻¹', 'key': f'α = Λm/Λ°m = {Lm}/{L0} = {al2:.4f} (1); K = cα²/(1 − α) = {c} × {al2:.4f}²/(1 − {al2:.4f}) = {sci(K)} mol L⁻¹ (2).',
            'distractors': [f'α = {L0 / Lm:.2f}; K = {sci(c * al2)} mol L⁻¹', f'α = {al2:.4f}; K = {sci(c * al2)} mol L⁻¹', f'α = {al2 ** 2:.5f}; K = {sci(K / 10)} mol L⁻¹']}


CH2S3 = {
    'topic': 'conductance of electrolytic solutions',
    'terms': [('conductivity', 'the conductance of a solution of 1 cm length and 1 cm² cross-section, the reciprocal of resistivity'),
              ('molar conductivity', 'the conductivity of a solution divided by its molar concentration (Λm = κ/c)'),
              ('the cell constant', 'the ratio of the distance between the electrodes to their area of cross-section (l/A)'),
              ("Kohlrausch's law of independent migration of ions", 'the law that the limiting molar conductivity of an electrolyte is the sum of the limiting contributions of its cation and anion'),
              ('limiting molar conductivity', 'the molar conductivity of an electrolyte when its concentration approaches zero')],
    'groups': [('a strong electrolyte', ['KCl', 'NaCl', 'HCl', 'NaOH', 'K₂SO₄']), ('a weak electrolyte', ['CH₃COOH', 'NH₄OH', 'HCOOH', 'HCN', 'H₂CO₃'])],
    'orders': [('increasing order of limiting molar ionic conductivity', ['CH₃COO⁻', 'Na⁺', 'K⁺', 'Cl⁻', 'OH⁻', 'H⁺'],
                'Λ° (S cm² mol⁻¹): CH₃COO⁻ 40.9, Na⁺ 50.1, K⁺ 73.5, Cl⁻ 76.3, OH⁻ 199.1, H⁺ 349.6 (H⁺ and OH⁻ move by proton hopping).', '<'),
               ('increasing order of molar conductivity at infinite dilution', ['Li⁺', 'Na⁺', 'K⁺'], 'Smaller Li⁺ is most hydrated, so its hydrated ion is largest and moves slowest.', '<')],
    'tf': (['Conductivity decreases with dilution, but molar conductivity increases.', 'For strong electrolytes Λm varies linearly with √c.',
            'Λ°m of weak electrolytes cannot be obtained by extrapolation to zero concentration.', 'The SI unit of conductivity is S m⁻¹.',
            'H⁺ ions have unusually high ionic conductivity in water.'],
           [('Molar conductivity decreases on dilution.', 'Molar conductivity increases on dilution; conductivity (κ) decreases.'),
            ('Λ°m of acetic acid is found by extrapolating the Λm vs √c graph to zero.', 'The curve for a weak electrolyte rises steeply near zero, so Kohlrausch\'s law is used instead.'),
            ('The unit of molar conductivity is S cm⁻¹.', 'It is S cm² mol⁻¹ (or S m² mol⁻¹).'),
            ('Conductivity of an electrolytic solution decreases with temperature.', 'It increases with temperature because ions move faster.')]),
    'ar': [('Molar conductivity of a weak electrolyte increases steeply on dilution.', 'The degree of dissociation of a weak electrolyte increases greatly on dilution.', 'a', 'More ions are produced per mole.'),
           ('Conductivity of a solution decreases on dilution.', 'The number of ions per unit volume decreases on dilution.', 'a', 'Fewer carriers per cm³.')],
    'fams': [F('C3', 'D3', 'numerical', cell_const), F('C3', 'D2', 'numerical', kohlrausch), F('C4', 'D4', 'multi_step', degree_diss, kinds=('long5',))],
    'qa': [('C4', 'D4', 'explain', 'Λm of KCl changes only a little on dilution while that of acetic acid increases sharply. Explain, and say how Λ°m of acetic acid is obtained.',
            'KCl is fully ionised; dilution only reduces interionic attraction. Acetic acid is weak; dilution increases its degree of dissociation greatly. Λ°m(CH₃COOH) is obtained from Kohlrausch\'s law using Λ° of HCl, CH₃COONa and NaCl.',
            '1 mark: strong vs weak; 1 mark: Kohlrausch\'s law.')],
}

# ---------------- ch02 st4 electrolysis ----------------

ELEC = [('Cu', 63.5, 2, 'CuSO₄'), ('Ag', 108, 1, 'AgNO₃'), ('Zn', 65.4, 2, 'ZnSO₄'), ('Ni', 58.7, 2, 'NiSO₄'), ('Al', 27, 3, 'molten Al₂O₃'), ('Cr', 52, 3, 'a Cr³⁺ salt')]


def faraday(r):
    m, M, n, s = r.choice(ELEC)
    I = r.choice([0.5, 1, 1.5, 2, 2.5, 5, 10])
    t = r.choice([10, 15, 20, 30, 45, 60, 120])
    Q = I * t * 60
    mass = Q * M / (n * FAR)
    return {'stem': f'A current of {I} A is passed through a solution of {s} for {t} minutes. Calculate the mass of {m} deposited at the cathode. (Molar mass of {m} = {M} g mol⁻¹, F = 96500 C mol⁻¹)',
            'answer': f'{sf(mass, 3)} g', 'key': f'Q = It = {I} × {t * 60} = {num(Q)} C (1); {m}{ {1: '⁺', 2: '²⁺', 3: '³⁺'}[n]} + {n}e⁻ → {m}; mass = QM/(nF) = {num(Q)} × {M}/({n} × 96500) = {sf(mass, 3)} g (1).',
            'distractors': [f'{sf(mass * n, 3)} g' if n > 1 else f'{sf(mass * 2, 3)} g', f'{sf(I * t * M / (n * FAR), 3)} g', f'{sf(mass / 2, 3)} g']}


def charge_needed(r):
    sp, e, what = r.choice([('Al³⁺ to Al', 3, '1 mol of Al³⁺'), ('Cu²⁺ to Cu', 2, '1 mol of Cu²⁺'), ('MnO₄⁻ to Mn²⁺', 5, '1 mol of MnO₄⁻'),
                            ('Cr₂O₇²⁻ to Cr³⁺', 6, '1 mol of Cr₂O₇²⁻'), ('H₂O to O₂', 2, '1 mol of H₂O'), ('FeO to Fe₂O₃', 1, '1 mol of FeO'), ('Ca²⁺ to Ca from molten CaCl₂', 2, '1 mol of Ca²⁺')])
    return {'stem': f'How much electricity in coulombs is required for the reduction (or oxidation) of {what} ({sp})?', 'answer': f'{e}F = {num(e * FAR)} C',
            'key': f'{e} mol of electrons are transferred per mole ⇒ Q = {e} × 96500 = {num(e * FAR)} C.',
            'distractors': [f'{num((e + 1) * FAR)} C', f'{num(FAR)} C' if e != 1 else f'{num(2 * FAR)} C', f'{num(e * FAR / 2)} C']}


CH2S4 = {
    'topic': 'electrolysis',
    'terms': [("Faraday's first law of electrolysis", 'the law that the mass of a substance deposited at an electrode is proportional to the quantity of electricity passed'),
              ("Faraday's second law of electrolysis", 'the law that the amounts of different substances liberated by the same quantity of electricity are proportional to their chemical equivalent weights'),
              ('electrolysis', 'the decomposition of an electrolyte by passing electricity through its solution or melt'),
              ('an electrolytic cell', 'a cell in which electrical energy is used to bring about a non-spontaneous chemical change'),
              ('one faraday', 'the charge carried by one mole of electrons, 96487 C (≈ 96500 C)')],
    'features': {'intro': 'In an electrolysis experiment:', 'q': 'Which electrolysis is being carried out', 'what': 'process', 'long': False,
                 'items': [('electrolysis of molten NaCl', ['sodium metal is formed at the cathode', 'chlorine gas is formed at the anode', 'no water is present']),
                           ('electrolysis of aqueous NaCl (brine)', ['hydrogen gas is formed at the cathode', 'chlorine gas is formed at the anode', 'NaOH remains in solution']),
                           ('electrolysis of aqueous CuSO₄ with copper electrodes', ['copper is deposited at the cathode', 'copper dissolves from the anode', 'the colour of the solution stays the same']),
                           ('electrolysis of dilute H₂SO₄ with platinum electrodes', ['hydrogen gas is formed at the cathode', 'oxygen gas is formed at the anode', 'effectively water is decomposed'])]},
    'tf': (['In electrolysis of aqueous NaCl, H₂ is formed at the cathode.', 'One faraday deposits one mole of silver from AgNO₃ solution.',
            'Electrolysis involves a non-spontaneous redox reaction.', 'In an electrolytic cell the cathode is the negative electrode.', 'Aluminium is obtained by electrolysis of molten alumina mixed with cryolite.'],
           [('In electrolysis of aqueous NaCl, sodium metal is deposited at the cathode.', 'Water (E° −0.83 V) is reduced in preference to Na⁺ (−2.71 V), so H₂ is evolved.'),
            ('One faraday deposits one mole of copper from CuSO₄ solution.', 'Cu²⁺ needs two electrons, so 1 F deposits 0.5 mol of Cu.'),
            ('In an electrolytic cell oxidation occurs at the cathode.', 'Oxidation occurs at the anode in all cells.'),
            ('The mass deposited is independent of the current.', 'Mass deposited ∝ It (Faraday\'s first law).')]),
    'ar': [('In the electrolysis of aqueous NaCl, Cl₂ is liberated at the anode, not O₂.', 'Oxidation of water to O₂ has a kinetic overpotential, so Cl⁻ is oxidised preferentially.', 'a', 'Overpotential for O₂ makes Cl₂ evolution favoured.'),
           ('The same quantity of electricity deposits different masses of Cu and Ag.', 'Masses deposited are proportional to M/n (equivalent mass) of the metals.', 'a', 'Faraday\'s second law.')],
    'fams': [F('C3', 'D3', 'numerical', faraday, marks=3), F('C2', 'D2', 'short', charge_needed)],
    'qa': [('C4', 'D4', 'explain', 'Two electrolytic cells containing AgNO₃ and CuSO₄ solutions are connected in series. If 1.08 g of silver is deposited, what mass of copper is deposited? (Ag = 108, Cu = 63.5)',
            'Moles of e⁻ = 1.08/108 = 0.01; Cu²⁺ needs 2 e⁻, so 0.005 mol Cu = 0.318 g.', '1 mark: same charge in series; 1 mark: 0.318 g.'),
           ('C4', 'D5', 'long', '(a) State Faraday\'s two laws of electrolysis. (b) A current of 1.5 A is passed for 10 min through molten CaCl₂. Calculate the mass of Ca at the cathode and the volume of Cl₂ at the anode at STP (22.7 L mol⁻¹). (Ca = 40)',
            '(a) m ∝ Q; for the same Q, masses ∝ equivalent weights. (b) Q = 900 C = 0.00933 F; Ca: 0.00466 mol = 0.187 g; Cl₂: 0.00466 mol × 22.7 = 0.106 L.',
            '(a) 2 marks (b) 3 marks.')],
}

CH2S5 = {
    'topic': 'batteries, fuel cells and corrosion',
    'terms': [('a primary battery', 'a battery in which the reaction occurs only once and which cannot be recharged'),
              ('a secondary battery', 'a battery that can be recharged by passing current through it in the opposite direction'),
              ('a fuel cell', 'a galvanic cell that converts the energy of combustion of fuels such as hydrogen directly into electrical energy'),
              ('corrosion', 'the slow destruction of a metal by its surroundings through an electrochemical process'),
              ('rusting', 'the corrosion of iron forming hydrated ferric oxide, Fe₂O₃·xH₂O'),
              ('sacrificial protection', 'protection of a metal by covering or connecting it with a more reactive metal that corrodes in its place')],
    'groups': [('a primary battery', ['dry (Leclanché) cell', 'mercury cell', 'alkaline manganese cell']), ('a secondary battery', ['lead storage battery', 'nickel–cadmium cell', 'lithium-ion battery']),
               ('a fuel cell', ['H₂–O₂ fuel cell', 'methane–oxygen fuel cell', 'methanol–oxygen fuel cell'])],
    'features': {'intro': 'A cell has these features:', 'q': 'Identify the cell', 'what': 'cell',
                 'items': [('the dry (Leclanché) cell', ['zinc container as anode', 'carbon (graphite) rod surrounded by MnO₂ as cathode', 'paste of NH₄Cl and ZnCl₂ as electrolyte', 'potential about 1.5 V']),
                           ('the mercury cell', ['zinc–mercury amalgam anode', 'paste of HgO and carbon as cathode', 'paste of KOH and ZnO as electrolyte', 'constant potential about 1.35 V over its life']),
                           ('the lead storage battery', ['lead anode and a grid of lead packed with PbO₂ as cathode', '38% sulphuric acid as electrolyte', 'used in automobiles and inverters', 'can be recharged']),
                           ('the H₂–O₂ fuel cell', ['H₂ and O₂ bubbled through porous carbon electrodes into concentrated NaOH', 'used in the Apollo space programme', 'product water can be used for drinking', 'efficiency about 70%'])]},
    'tf': (['The mercury cell gives a constant voltage throughout its life.', 'The H₂–O₂ fuel cell was used in the Apollo space programme.', 'Galvanising protects iron by coating it with zinc.',
            'During discharge of a lead storage battery, the density of sulphuric acid decreases.', 'Rusting needs both oxygen and water.'],
           [('A lead storage battery is a primary cell.', 'It is a secondary cell; it can be recharged.'),
            ('The dry cell can be recharged many times.', 'The dry cell is a primary cell and cannot be recharged.'),
            ('Rusting of iron is faster in dry air.', 'Moisture (and electrolytes such as salt) are needed; rusting is faster in moist, salty air.'),
            ('Zinc coating on iron prevents rusting only as long as the coating is unbroken.', 'Zinc protects iron even when scratched, as it is more reactive and corrodes sacrificially.')]),
    'ar': [('Iron rusts faster in coastal areas like Mumbai.', 'Salt in moist air increases the conductivity of the water film on iron.', 'a', 'Electrolyte speeds the electrochemical corrosion.'),
           ('Fuel cells are pollution free.', 'In the H₂–O₂ fuel cell the only product is water.', 'a', 'No harmful products are formed.')],
    'qa': [('C4', 'D4', 'explain', 'Write the anode and cathode reactions during rusting of iron and explain why it is called an electrochemical process.',
            'Anode: 2Fe → 2Fe²⁺ + 4e⁻; cathode: O₂ + 4H⁺ + 4e⁻ → 2H₂O; Fe²⁺ is further oxidised to Fe₂O₃·xH₂O. A small galvanic cell forms on the metal surface with water as electrolyte.',
            '1 mark reactions; 1 mark electrochemical cell explanation.')],
}

# ---------------- ch03 kinetics ----------------

RATE_RX = [('2N₂O₅(g) → 4NO₂(g) + O₂(g)', [('N₂O₅', 2)], [('NO₂', 4), ('O₂', 1)]), ('N₂(g) + 3H₂(g) → 2NH₃(g)', [('N₂', 1), ('H₂', 3)], [('NH₃', 2)]),
           ('2HI(g) → H₂(g) + I₂(g)', [('HI', 2)], [('H₂', 1), ('I₂', 1)]), ('5Br⁻ + BrO₃⁻ + 6H⁺ → 3Br₂ + 3H₂O', [('Br⁻', 5), ('BrO₃⁻', 1), ('H⁺', 6)], [('Br₂', 3)]),
           ('2NO(g) + O₂(g) → 2NO₂(g)', [('NO', 2), ('O₂', 1)], [('NO₂', 2)]), ('2H₂O₂(aq) → 2H₂O(l) + O₂(g)', [('H₂O₂', 2)], [('O₂', 1)]),
           ('4NH₃(g) + 5O₂(g) → 4NO(g) + 6H₂O(g)', [('NH₃', 4), ('O₂', 5)], [('NO', 4), ('H₂O', 6)])]


def rate_rel(r):
    eq, rs, ps = r.choice(RATE_RX)
    a = r.choice(rs)
    b = r.choice(ps)
    v = r.choice([1.2e-3, 2.5e-4, 6.0e-2, 3.6e-3, 4.0e-5, 8.0e-4])
    vb = v * b[1] / a[1]
    return {'stem': f'For the reaction {eq}, the rate of disappearance of {a[0]} is {sci(v, 2)} mol L⁻¹ s⁻¹. Calculate the rate of formation of {b[0]} and the rate of reaction.',
            'answer': f'd[{b[0]}]/dt = {sci(vb)} mol L⁻¹ s⁻¹; rate = {sci(v / a[1])} mol L⁻¹ s⁻¹',
            'key': f'Rate = −(1/{a[1]}) d[{a[0]}]/dt = (1/{b[1]}) d[{b[0]}]/dt (1); d[{b[0]}]/dt = {b[1]}/{a[1]} × {sci(v, 2)} = {sci(vb)}; rate of reaction = {sci(v / a[1])} mol L⁻¹ s⁻¹ (1).',
            'distractors': [f'd[{b[0]}]/dt = {sci(v * a[1] / b[1])} mol L⁻¹ s⁻¹; rate = {sci(v / a[1])} mol L⁻¹ s⁻¹', f'd[{b[0]}]/dt = {sci(v)} mol L⁻¹ s⁻¹; rate = {sci(v)} mol L⁻¹ s⁻¹', f'd[{b[0]}]/dt = {sci(vb)} mol L⁻¹ s⁻¹; rate = {sci(v * a[1])} mol L⁻¹ s⁻¹']}


def avg_rate(r):
    c1 = r.choice([0.80, 1.00, 0.50, 0.25, 1.20])
    c2 = round(c1 * r.choice([0.4, 0.5, 0.6, 0.75, 0.8]), 3)
    t = r.choice([10, 20, 30, 40, 50, 60])
    rt = (c1 - c2) / t
    sp = r.choice(['A', 'N₂O₅', 'H₂O₂', 'the ester'])
    return {'stem': f'The concentration of {sp} falls from {c1} mol L⁻¹ to {c2} mol L⁻¹ in {t} s. Calculate the average rate of the reaction in mol L⁻¹ s⁻¹ and in mol L⁻¹ min⁻¹ (for the reaction {sp} → products).',
            'answer': f'{sci(rt)} mol L⁻¹ s⁻¹; {sci(rt * 60)} mol L⁻¹ min⁻¹', 'key': f'r_av = −Δ[R]/Δt = ({c1} − {c2})/{t} = {sci(rt)} mol L⁻¹ s⁻¹ (1); × 60 = {sci(rt * 60)} mol L⁻¹ min⁻¹ (1).',
            'distractors': [f'{sci(rt * 2)} mol L⁻¹ s⁻¹; {sci(rt * 120)} mol L⁻¹ min⁻¹', f'{sci(c2 / t)} mol L⁻¹ s⁻¹; {sci(c2 / t * 60)} mol L⁻¹ min⁻¹', f'{sci(rt)} mol L⁻¹ s⁻¹; {sci(rt / 60)} mol L⁻¹ min⁻¹']}


CH3S1 = {
    'topic': 'rate of a chemical reaction',
    'terms': [('the rate of a reaction', 'the change in concentration of a reactant or product per unit time'),
              ('the average rate', 'the change in concentration divided by the time interval over which it occurs'),
              ('the instantaneous rate', 'the rate at a particular moment, given by the slope of the tangent to the concentration–time curve'),
              ('a catalyst', 'a substance that alters the rate of a reaction without itself undergoing any permanent chemical change')],
    'groups': [('a very fast reaction', ['precipitation of AgCl on mixing AgNO₃ and NaCl', 'neutralisation of HCl by NaOH', 'explosion of a mixture of H₂ and Cl₂ in sunlight']),
               ('a very slow reaction', ['rusting of iron', 'weathering of rocks', 'conversion of diamond into graphite']),
               ('a reaction of moderate rate', ['inversion of cane sugar', 'hydrolysis of starch', 'decomposition of H₂O₂ without catalyst'])],
    'tf': (['The rate of a reaction is always positive.', 'Rate of reaction generally decreases with time.', 'A catalyst does not change the equilibrium constant.',
            'Rate increases with increase in concentration of reactants (in general).', 'The unit of rate is mol L⁻¹ s⁻¹.'],
           [('The rate of a reaction is constant throughout the reaction.', 'Rate usually falls as reactants are used up.'),
            ('Rate of disappearance of N₂O₅ in 2N₂O₅ → 4NO₂ + O₂ equals the rate of formation of NO₂.', 'd[NO₂]/dt = 2 × (−d[N₂O₅]/dt).'),
            ('A catalyst increases the yield of the products at equilibrium.', 'A catalyst only helps reach equilibrium faster; it does not change the yield.'),
            ('Instantaneous rate equals average rate over any interval.', 'They are equal only when the time interval approaches zero.')]),
    'ar': [('Rate of a reaction decreases with time.', 'The concentration of reactants decreases as the reaction proceeds.', 'a', 'Rate depends on concentration.'),
           ('Food spoils faster in summer.', 'The rate of reactions increases with temperature.', 'a', 'Higher temperature speeds the decay reactions.')],
    'fams': [F('C3', 'D3', 'numerical', rate_rel, marks=2), F('C2', 'D2', 'numerical', avg_rate)],
    'qa': [('C4', 'D4', 'explain', 'Milk kept in a refrigerator stays fresh longer than milk kept on a kitchen shelf in Chennai. Explain in terms of factors affecting the rate.',
            'Rates of the microbial/chemical spoiling reactions fall at low temperature; fewer molecules have the activation energy (rate roughly halves for every 10 K drop).', '1 mark: temperature effect; 1 mark: activation energy explanation.')],
}


def order_units(r):
    n = r.choice([0, 1, 2, 3, 0.5, 1.5])
    u = {0: 'mol L⁻¹ s⁻¹', 1: 's⁻¹', 2: 'mol⁻¹ L s⁻¹', 3: 'mol⁻² L² s⁻¹', 0.5: 'mol^½ L^−½ s⁻¹', 1.5: 'mol^−½ L^½ s⁻¹'}[n]
    opts = ['mol L⁻¹ s⁻¹', 's⁻¹', 'mol⁻¹ L s⁻¹', 'mol⁻² L² s⁻¹', 'mol^½ L^−½ s⁻¹', 'mol^−½ L^½ s⁻¹']
    return mcq(f'What are the units of the rate constant of a reaction of order {num(n)} (concentration in mol L⁻¹, time in s)?', u, r.sample([o for o in opts if o != u], 3),
               f'Units of k = (mol L⁻¹)^(1 − n) s⁻¹ with n = {num(n)} ⇒ {u}.', r)


def order_from_law(r):
    a = r.choice([0.5, 1, 2])
    b = r.choice([0, 0.5, 1, 1.5, 2])
    o = a + b
    law = f'Rate = k[A]{"" if a == 1 else ("^½" if a == 0.5 else "²")}' + ('' if b == 0 else f'[B]{"" if b == 1 else ("^½" if b == 0.5 else ("^3/2" if b == 1.5 else "²"))}')
    return {'stem': f'For a reaction A + B → products, the rate law is {law}. What is the overall order? What happens to the rate if [A] is doubled keeping [B] constant?',
            'answer': f'Order {num(o)}; rate becomes {sf(2 ** a, 3)} times', 'key': f'Order = sum of exponents = {num(a)} + {num(b)} = {num(o)} (1); rate ∝ [A]^{num(a)}, so doubling [A] multiplies rate by 2^{num(a)} = {sf(2 ** a, 3)} (1).',
            'distractors': [f'Order {num(o)}; rate becomes 2 times' if a != 1 else f'Order {num(o)}; rate becomes 4 times', f'Order {num(o + 1)}; rate becomes {sf(2 ** a, 3)} times', f'Order 2; rate becomes {sf(2 ** (a + b), 3)} times']}


SUP = {0: '⁰', 1: '', 2: '²'}
KU = {0: 'mol L⁻¹ s⁻¹', 1: 's⁻¹', 2: 'mol⁻¹ L s⁻¹', 3: 'mol⁻² L² s⁻¹', 4: 'mol⁻³ L³ s⁻¹'}


def initial_rates(r):
    a = r.choice([0, 1, 2])
    b = r.choice([0, 1, 2])
    k = r.choice([2.0e-3, 5.0e-2, 1.5e-1, 4.0e-4])
    A1, B1 = r.choice([0.1, 0.2]), r.choice([0.1, 0.2])
    fa, fb = r.choice([2, 3]), r.choice([2, 3])
    rows = [(A1, B1), (A1 * fa, B1), (A1, B1 * fb)]
    rates = [k * x ** a * y ** b for x, y in rows]
    tab = '; '.join(f'Exp {i + 1}: [A] = {num(x, 2)} M, [B] = {num(y, 2)} M, initial rate = {sci(rt)} M s⁻¹' for i, ((x, y), rt) in enumerate(zip(rows, rates)))
    return {'stem': f'For A + B → products the following data were obtained. {tab}. Find the order with respect to A and B, write the rate law and calculate k.',
            'answer': f'Order in A = {a}, in B = {b}; rate = k[A]{"" if a == 1 else ("⁰" if a == 0 else "²")}[B]{"" if b == 1 else ("⁰" if b == 0 else "²")}; k = {sci(k)} {KU[a + b]}',
            'key': f'Exp 2/1: rate × {num(rates[1] / rates[0], 3)} when [A] × {fa} ⇒ order in A = {a} (1); Exp 3/1: rate × {num(rates[2] / rates[0], 3)} when [B] × {fb} ⇒ order in B = {b} (1); k = rate/([A]{SUP[a]}[B]{SUP[b]}) = {sci(k)} {KU[a + b]} (1).'}


CH3S2 = {
    'topic': 'rate law, order and molecularity',
    'terms': [('the rate law', 'the expression in which the reaction rate is given in terms of the molar concentrations of reactants, each raised to some power found experimentally'),
              ('the order of a reaction', 'the sum of the powers of the concentration terms in the rate law expression'),
              ('molecularity', 'the number of reacting species taking part in an elementary reaction that must collide simultaneously'),
              ('the rate constant', 'the rate of reaction when the concentration of each reactant is unity'),
              ('an elementary reaction', 'a reaction that takes place in one step'),
              ('the rate determining step', 'the slowest step of a complex reaction, which controls the overall rate'),
              ('a pseudo first order reaction', 'a reaction that is of higher order but behaves as first order because one reactant is present in large excess')],
    'features': {'intro': 'A quantity in kinetics has these characteristics:', 'q': 'Which quantity is it', 'what': 'quantity', 'case': False,
                 'items': [('order of reaction', ['it is found experimentally', 'it can be zero or fractional', 'it applies to elementary as well as complex reactions', 'it is the sum of powers in the rate law']),
                           ('molecularity', ['it is a theoretical concept', 'it is always a whole number and cannot be zero', 'it applies only to elementary reactions', 'it is the number of species colliding in an elementary step'])]},
    'tf': (['Order of a reaction can be fractional.', 'Molecularity cannot be zero.', 'Hydrolysis of ethyl acetate in excess water is pseudo first order.',
            'The rate law cannot be predicted just by looking at the balanced equation.', 'The units of k for a zero order reaction are mol L⁻¹ s⁻¹.'],
           [('Molecularity can be fractional.', 'Molecularity is always a whole number (1, 2 or 3).'),
            ('The order of a reaction is always equal to the sum of the stoichiometric coefficients.', 'Order is found experimentally and may differ from the coefficients.'),
            ('The units of k for a first order reaction are mol L⁻¹ s⁻¹.', 'For first order k has units s⁻¹.'),
            ('Inversion of cane sugar is a true first order reaction.', 'It is pseudo first order; water is present in large excess.')]),
    'ar': [('Hydrolysis of ethyl acetate in aqueous acid is a pseudo first order reaction.', 'Water is present in large excess and its concentration remains nearly constant.', 'a', 'Rate = k[ester][H₂O] ≈ k′[ester].'),
           ('Molecularity has no meaning for a complex reaction.', 'A complex reaction takes place in several steps, each with its own molecularity.', 'a', 'Molecularity applies to elementary steps; the overall order is set by the slow step.')],
    'fams': [F('C2', 'D2', 'mcq', order_units), F('C3', 'D2', 'explain', order_from_law), F('C4', 'D4', 'multi_step', initial_rates, kinds=('long5',))],
    'qa': [('C4', 'D3', 'explain', 'The decomposition of NH₃ on a hot platinum surface is zero order at high pressure. Explain.',
            'At high pressure the metal surface is completely covered (saturated) with NH₃ molecules; further increase in pressure cannot increase the amount on the surface, so rate is independent of concentration.', '1 mark: surface saturation; 1 mark: rate independent of [NH₃].')],
}


def first_order_t(r):
    k = r.choice([1.15e-3, 2.3e-3, 6.93e-3, 5.0e-4, 1.0e-2, 4.6e-2])
    p = r.choice([50, 60, 75, 80, 90, 99, 99.9])
    t = 2.303 / k * math.log10(100 / (100 - p))
    return {'stem': f'A first order reaction has rate constant {sci(k, 3)} s⁻¹. How long will it take for {p}% of the reactant to react?',
            'answer': f'{sf(t, 3)} s', 'key': f't = (2.303/k) log([R]₀/[R]) = (2.303/{sci(k, 3)}) log(100/{num(100 - p, 1)}) (1) = {sf(t, 3)} s (1).',
            'distractors': [f'{sf(t * 2.303, 3)} s', f'{sf(0.693 / k, 3)} s' if p != 50 else f'{sf(t * 2, 3)} s', f'{sf(t / 2.303, 3)} s']}


def half_life(r):
    k = r.choice([0.0231, 0.0693, 1.386e-3, 2.31e-4, 3.465e-2, 5.5e-14])
    unit = r.choice(['s⁻¹', 'min⁻¹', 'h⁻¹'])
    t = 0.693 / k
    return {'stem': f'The rate constant of a first order reaction is {sci(k, 3)} {unit}. Calculate its half-life.', 'answer': f'{sf(t, 3)} {unit[:-2]}',
            'key': f't½ = 0.693/k = 0.693/{sci(k, 3)} = {sf(t, 3)} {unit[:-2]}; half-life of a first order reaction does not depend on initial concentration.',
            'distractors': [f'{sf(k / 0.693, 3)} {unit[:-2]}', f'{sf(t * 2, 3)} {unit[:-2]}', f'{sf(2.303 / k, 3)} {unit[:-2]}']}


def fraction_left(r):
    n = r.randint(2, 6)
    t12 = r.choice([5, 10, 15, 20, 30, 69.3])
    t = n * t12
    frac = 0.5 ** n
    m0 = r.choice([1, 2, 5, 10, 16, 32, 64])
    sp = r.choice(['a radioactive isotope', 'N₂O₅ in CCl₄', 'H₂O₂ decomposing on a catalyst', 'a first order reactant'])
    return {'stem': f'The half-life of {sp} (first order) is {num(t12)} min. If the initial amount is {m0} g, what mass remains after {num(t)} min?',
            'answer': f'{sf(m0 * frac, 3)} g', 'key': f'{num(t)}/{num(t12)} = {n} half-lives; remaining = {m0} × (½)^{n} = {sf(m0 * frac, 3)} g.',
            'distractors': [f'{sf(m0 / (2 * n), 3)} g', f'{sf(m0 * (1 - frac), 3)} g', f'{sf(m0 * 0.5 ** (n - 1), 3)} g']}


def zero_order(r):
    k = r.choice([0.002, 0.005, 0.01, 0.025])
    R0 = r.choice([0.1, 0.2, 0.5, 1.0])
    t12 = R0 / (2 * k)
    return {'stem': f'A zero order reaction has k = {k} mol L⁻¹ s⁻¹ and an initial concentration of {R0} mol L⁻¹. Calculate its half-life and the time for complete reaction.',
            'answer': f't½ = {sf(t12, 3)} s; complete in {sf(2 * t12, 3)} s', 'key': f'[R] = [R]₀ − kt; t½ = [R]₀/2k = {R0}/(2 × {k}) = {sf(t12, 3)} s (1); complete when [R] = 0: t = [R]₀/k = {sf(2 * t12, 3)} s (1).',
            'distractors': [f't½ = {sf(0.693 / k, 3)} s; complete in {sf(1.386 / k, 3)} s', f't½ = {sf(t12 * 2, 3)} s; complete in {sf(t12 * 4, 3)} s', f't½ = {sf(t12, 3)} s; complete in infinite time']}


def k_from_data(r):
    k = r.choice([0.005, 0.01, 0.02, 0.05, 0.1])
    R0 = r.choice([0.8, 1.0, 0.5, 0.4])
    t = r.choice([10, 20, 30, 50, 60])
    Rt = R0 * math.exp(-k * t)
    Rt = round(Rt, 3)
    kc = 2.303 / t * math.log10(R0 / Rt)
    return {'stem': f'For a first order reaction the concentration of reactant falls from {R0} M to {Rt} M in {t} min. Calculate the rate constant and the half-life.',
            'answer': f'k = {sci(kc)} min⁻¹; t½ = {sf(0.693 / kc, 3)} min', 'key': f'k = (2.303/t) log([R]₀/[R]) = (2.303/{t}) log({R0}/{Rt}) = {sci(kc)} min⁻¹ (2); t½ = 0.693/k = {sf(0.693 / kc, 3)} min (1).'}


CH3S3 = {
    'topic': 'integrated rate equations',
    'terms': [('half-life', 'the time in which the concentration of a reactant is reduced to one half of its initial concentration'),
              ('a zero order reaction', 'a reaction whose rate is independent of the concentration of the reactants'),
              ('a first order reaction', 'a reaction whose rate is proportional to the first power of the concentration of the reactant'),
              ('the integrated rate equation', 'an equation relating concentration directly to time, obtained by integrating the differential rate law')],
    'features': {'intro': 'A reaction shows the following behaviour:', 'q': 'What is the order of the reaction', 'what': 'order',
                 'items': [('zero order', ['a plot of [R] against t is a straight line with slope −k', 'half-life is directly proportional to initial concentration', 'units of k are mol L⁻¹ s⁻¹', 'shown by the decomposition of NH₃ on hot platinum at high pressure']),
                           ('first order', ['a plot of ln[R] against t is a straight line with slope −k', 'half-life is independent of initial concentration', 'units of k are s⁻¹', 'shown by radioactive decay and the decomposition of N₂O₅']),
                           ('second order', ['a plot of 1/[R] against t is a straight line', 'half-life is inversely proportional to initial concentration', 'units of k are mol⁻¹ L s⁻¹', 'rate is proportional to the square of a single reactant concentration'])]},
    'tf': (['For a first order reaction t½ = 0.693/k.', 'The time for 99.9% completion of a first order reaction is about 10 times its half-life.',
            'For a zero order reaction, t½ is proportional to [R]₀.', 'Radioactive decay follows first order kinetics.', 'A plot of log[R] against t for a first order reaction is linear with slope −k/2.303.'],
           [('The half-life of a first order reaction depends on the initial concentration.', 'For first order t½ = 0.693/k, independent of [R]₀.'),
            ('A zero order reaction never goes to completion.', 'For zero order [R] = [R]₀ − kt, which becomes zero at t = [R]₀/k.'),
            ('For a first order reaction a plot of [R] against t is a straight line.', 'ln[R] (or log[R]) against t is linear; [R] against t is linear for zero order.'),
            ('The time for 75% completion of a first order reaction is three half-lives.', 'It is two half-lives (100 → 50 → 25).')]),
    'ar': [('The half-life of a first order reaction is independent of the initial concentration.', 't½ = 0.693/k contains no concentration term.', 'a', 'Direct from the integrated rate law.'),
           ('Time taken for 75% completion of a first order reaction is twice its half-life.', 'After each half-life the concentration is halved.', 'a', '100 → 50 → 25 needs two half-lives.')],
    'fams': [F('C3', 'D3', 'numerical', first_order_t), F('C2', 'D2', 'numerical', half_life), F('C3', 'D2', 'numerical', fraction_left),
             F('C3', 'D3', 'numerical', zero_order), F('C4', 'D4', 'multi_step', k_from_data, kinds=('long5',))],
    'qa': [('C4', 'D5', 'long', '(a) Derive the integrated rate equation for a first order reaction. (b) Show that the time required for 99.9% completion is about ten times its half-life. (c) A first order reaction is 20% complete in 10 min. Calculate k.',
            '(a) −d[R]/dt = k[R] ⇒ ln([R]₀/[R]) = kt ⇒ k = (2.303/t) log([R]₀/[R]). (b) t₉₉.₉ = (2.303/k) log 1000 = 6.909/k; t½ = 0.693/k; ratio ≈ 10. (c) k = (2.303/10) log(100/80) = 0.0223 min⁻¹.',
            '(a) 2 marks (b) 1.5 marks (c) 1.5 marks.')],
}


def arrhenius_ea(r):
    T1 = r.choice([298, 300, 310, 320])
    dT = r.choice([10, 20, 25, 50])
    T2 = T1 + dT
    f = r.choice([2, 3, 4, 10])
    Ea = 2.303 * R * math.log10(f) * T1 * T2 / (T2 - T1)
    return {'stem': f'The rate constant of a reaction becomes {f} times when the temperature is raised from {T1} K to {T2} K. Calculate the activation energy. (R = 8.314 J K⁻¹ mol⁻¹)',
            'answer': f'{sf(Ea / 1000, 3)} kJ mol⁻¹', 'key': f'log(k₂/k₁) = (Ea/2.303R)[(T₂ − T₁)/(T₁T₂)] (1); log {f} = Ea/(2.303 × 8.314) × {dT}/({T1} × {T2}) (1) ⇒ Ea = {sf(Ea, 4)} J mol⁻¹ = {sf(Ea / 1000, 3)} kJ mol⁻¹ (1).',
            'distractors': [f'{sf(Ea / 2303, 3)} kJ mol⁻¹', f'{sf(Ea / 1000 * 2, 3)} kJ mol⁻¹', f'{sf(R * math.log(f) * T1 * T2 / (T2 - T1) / 10, 3)} kJ mol⁻¹']}


def arrhenius_k2(r):
    Ea = r.choice([50, 60, 75, 100, 120]) * 1000
    T1 = r.choice([300, 298])
    T2 = T1 + r.choice([10, 20, 30, 50])
    k1 = r.choice([1.5e-3, 2.0e-4, 3.0e-2, 5.0e-5])
    lr = Ea / (2.303 * R) * (T2 - T1) / (T1 * T2)
    k2 = k1 * 10 ** lr
    return {'stem': f'A reaction has activation energy {Ea // 1000} kJ mol⁻¹ and rate constant {sci(k1, 2)} s⁻¹ at {T1} K. Calculate the rate constant at {T2} K.',
            'answer': f'{sci(k2)} s⁻¹', 'key': f'log(k₂/k₁) = Ea(T₂ − T₁)/(2.303 R T₁T₂) = {lr:.3f} (1); k₂/k₁ = {sf(10 ** lr, 3)} (1); k₂ = {sci(k2)} s⁻¹ (1).',
            'distractors': [f'{sci(k1 * lr)} s⁻¹', f'{sci(k1 * math.exp(lr))} s⁻¹', f'{sci(k1 / 10 ** lr)} s⁻¹']}


def fraction_ea(r):
    Ea = r.choice([20, 40, 50, 75, 100]) * 1000
    T = r.choice([300, 400, 500, 600])
    f = math.exp(-Ea / (R * T))
    return {'stem': f'What fraction of molecules have energy equal to or greater than the activation energy of {Ea // 1000} kJ mol⁻¹ at {T} K? (fraction = e^(−Ea/RT))',
            'answer': sci(f), 'key': f'x = e^(−Ea/RT) = e^(−{Ea}/(8.314 × {T})) = e^(−{Ea / (R * T):.2f}) = {sci(f)}.',
            'distractors': [sci(math.exp(-Ea / (R * T * 2.303))), sci(f * 10), sci(1 - f) if f > 0.01 else sci(f / 10)]}


CH3S4 = {
    'topic': 'temperature dependence of rate',
    'terms': [('activation energy', 'the minimum extra energy that reactant molecules must absorb to form the activated complex'),
              ('the activated complex', 'the unstable intermediate of highest energy formed during the conversion of reactants into products'),
              ('the Arrhenius equation', 'the equation k = A e^(−Ea/RT) relating the rate constant to temperature'),
              ('the frequency factor', 'the pre-exponential factor A in the Arrhenius equation, related to collision frequency'),
              ('effective collisions', 'collisions in which molecules collide with sufficient kinetic energy and proper orientation to form products'),
              ('the collision frequency', 'the number of collisions per second per unit volume of the reaction mixture')],
    'tf': (['For many reactions the rate nearly doubles for a 10 K rise in temperature.', 'A catalyst lowers the activation energy.', 'A plot of ln k against 1/T is a straight line with slope −Ea/R.',
            'Only collisions with proper orientation and sufficient energy lead to reaction.', 'A catalyst does not change ΔG of a reaction.'],
           [('A catalyst increases the activation energy of a reaction.', 'A catalyst provides an alternative path of lower activation energy.'),
            ('A plot of ln k against T is a straight line.', 'ln k against 1/T is linear (slope −Ea/R).'),
            ('All collisions between reactant molecules lead to products.', 'Only effective collisions (enough energy and proper orientation) give products.'),
            ('A catalyst changes the enthalpy of reaction.', 'ΔH and ΔG are unchanged; only the path and Ea change.')]),
    'ar': [('The rate of reaction increases with temperature.', 'At higher temperature a larger fraction of molecules has energy ≥ Ea.', 'a', 'Maxwell–Boltzmann distribution shifts to higher energies.'),
           ('A catalyst does not alter the equilibrium constant.', 'A catalyst lowers the activation energy of forward and backward reactions equally.', 'a', 'Both rates rise equally.')],
    'fams': [F('C3', 'D4', 'multi_step', arrhenius_ea, kinds=('long5',)), F('C4', 'D4', 'numerical', arrhenius_k2, marks=3), F('C3', 'D3', 'numerical', fraction_ea)],
    'qa': [('C4', 'D3', 'case', 'Read and answer. A student measured the rate constant of the decomposition of N₂O₅ at different temperatures and plotted log k against 1/T. The graph was a straight line with slope −5400 K.\n(i) Which equation predicts this straight line? (1 mark)\n(ii) Calculate Ea. (R = 8.314 J K⁻¹ mol⁻¹) (2 marks)\n(iii) How would the line change if a catalyst were added? (1 mark)',
            '(i) Arrhenius equation, log k = log A − Ea/(2.303RT). (ii) Ea = 2.303 × 8.314 × 5400 = 103.4 kJ mol⁻¹. (iii) Slope becomes less steep (smaller Ea).',
            '(i) 1 (ii) 2 (iii) 1.', ('case',)),
           ('C4', 'D4', 'explain', 'Draw (describe) an energy profile for an exothermic reaction with and without a catalyst. Label Ea and ΔH and state what the catalyst changes.',
            'Reactants above products (ΔH negative); a hump for the activated complex; catalysed path has a lower hump (smaller Ea) but the same reactant and product levels, so ΔH is unchanged.', '1 mark labelled profile; 1 mark catalyst effect.')],
}

SPECS = {'ch01-st1': CH1S1, 'ch01-st2': CH1S2, 'ch01-st3': CH1S3, 'ch01-st4': CH1S4,
         'ch02-st1': CH2S1, 'ch02-st2': CH2S2, 'ch02-st3': CH2S3, 'ch02-st4': CH2S4, 'ch02-st5': CH2S5,
         'ch03-st1': CH3S1, 'ch03-st2': CH3S2, 'ch03-st3': CH3S3, 'ch03-st4': CH3S4}

FAMILIES = build_all(P, SPECS)
