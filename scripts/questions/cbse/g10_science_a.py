"""CBSE class 10 science families, chapters 1-4 (Chemical Reactions and Equations; Acids, Bases and
Salts; Metals and Non-metals; Carbon and its Compounds). Equations are checked for atom balance
at import time."""
from __future__ import annotations

import re
from math import gcd

from qbank import name, num, inr
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g10-science-ch'
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
MASS = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'Na': 23, 'Mg': 24, 'Al': 27, 'S': 32, 'Cl': 35.5, 'K': 39, 'Ca': 40, 'Fe': 56, 'Cu': 63.5, 'Zn': 65, 'Pb': 207, 'Ag': 108, 'Ba': 137, 'I': 127, 'Mn': 55}


def sub(s: str) -> str:
    """ASCII formula -> subscripted (digits after a letter or ')' only)."""
    return re.sub(r'(?<=[A-Za-z)])(\d+)', lambda m: m.group(1).translate(SUB), s)


def atoms(f: str) -> dict:
    """Count atoms in an ASCII formula such as Ca(OH)2 or CuSO4.5H2O."""
    tot: dict = {}
    for part in f.split('.'):
        k = 1
        m = re.match(r'^(\d+)(.*)$', part)
        if m:
            k, part = int(m.group(1)), m.group(2)
        stack = [{}]
        for tok in re.findall(r'[A-Z][a-z]?\d*|\(|\)\d*', part):
            if tok == '(':
                stack.append({})
            elif tok.startswith(')'):
                n = int(tok[1:] or 1)
                top = stack.pop()
                for e, c in top.items():
                    stack[-1][e] = stack[-1].get(e, 0) + c * n
            else:
                e = re.match(r'[A-Z][a-z]?', tok).group(0)
                n = int(tok[len(e):] or 1)
                stack[-1][e] = stack[-1].get(e, 0) + n
        for e, c in stack[0].items():
            tot[e] = tot.get(e, 0) + c * k
    return tot


def molar(f: str) -> float:
    return sum(MASS[e] * n for e, n in atoms(f).items())


def side(spec):
    tot: dict = {}
    for c, f in spec:
        for e, n in atoms(f).items():
            tot[e] = tot.get(e, 0) + c * n
    return tot


def eqn(spec_l, spec_r, arrow='→', show=True):
    def s(spec):
        return ' + '.join((f'{c}' if (c != 1 and show) else '') + sub(f) for c, f in spec)
    return f'{s(spec_l)} {arrow} {s(spec_r)}'


# ======================= ch01 Chemical Reactions and Equations
# (reactants, products, type, note); coefficients are checked below
RXN = [
    ([(3, 'Fe'), (4, 'H2O')], [(1, 'Fe3O4'), (4, 'H2')], 'displacement', 'iron with steam'),
    ([(2, 'H2'), (1, 'O2')], [(2, 'H2O')], 'combination', 'burning of hydrogen'),
    ([(2, 'Mg'), (1, 'O2')], [(2, 'MgO')], 'combination', 'burning of magnesium ribbon'),
    ([(2, 'Na'), (2, 'H2O')], [(2, 'NaOH'), (1, 'H2')], 'displacement', 'sodium with water'),
    ([(1, 'CaCO3')], [(1, 'CaO'), (1, 'CO2')], 'decomposition', 'heating limestone'),
    ([(2, 'Pb(NO3)2')], [(2, 'PbO'), (4, 'NO2'), (1, 'O2')], 'decomposition', 'heating lead nitrate'),
    ([(2, 'FeSO4')], [(1, 'Fe2O3'), (1, 'SO2'), (1, 'SO3')], 'decomposition', 'heating ferrous sulphate crystals'),
    ([(2, 'AgCl')], [(2, 'Ag'), (1, 'Cl2')], 'decomposition', 'silver chloride in sunlight'),
    ([(2, 'H2O')], [(2, 'H2'), (1, 'O2')], 'decomposition', 'electrolysis of water'),
    ([(1, 'BaCl2'), (1, 'Na2SO4')], [(1, 'BaSO4'), (2, 'NaCl')], 'double displacement', 'barium chloride with sodium sulphate'),
    ([(1, 'Pb(NO3)2'), (2, 'KI')], [(1, 'PbI2'), (2, 'KNO3')], 'double displacement', 'lead nitrate with potassium iodide'),
    ([(1, 'Fe'), (1, 'CuSO4')], [(1, 'FeSO4'), (1, 'Cu')], 'displacement', 'iron nail in copper sulphate solution'),
    ([(1, 'Zn'), (1, 'H2SO4')], [(1, 'ZnSO4'), (1, 'H2')], 'displacement', 'zinc with dilute sulphuric acid'),
    ([(1, 'CH4'), (2, 'O2')], [(1, 'CO2'), (2, 'H2O')], 'combustion', 'burning of methane'),
    ([(4, 'Al'), (3, 'O2')], [(2, 'Al2O3')], 'combination', 'aluminium with oxygen'),
    ([(1, 'Fe2O3'), (2, 'Al')], [(1, 'Al2O3'), (2, 'Fe')], 'displacement', 'thermit reaction'),
    ([(1, 'N2'), (3, 'H2')], [(2, 'NH3')], 'combination', 'formation of ammonia'),
    ([(1, 'CuO'), (1, 'H2')], [(1, 'Cu'), (1, 'H2O')], 'redox', 'hydrogen over heated copper oxide'),
    ([(1, 'Na2CO3'), (2, 'HCl')], [(2, 'NaCl'), (1, 'H2O'), (1, 'CO2')], 'double displacement', 'washing soda with hydrochloric acid'),
    ([(1, 'C3H8'), (5, 'O2')], [(3, 'CO2'), (4, 'H2O')], 'combustion', 'burning of propane (LPG)'),
    ([(1, 'Ca(OH)2'), (1, 'CO2')], [(1, 'CaCO3'), (1, 'H2O')], 'other', 'carbon dioxide through lime water'),
    ([(2, 'Al'), (6, 'HCl')], [(2, 'AlCl3'), (3, 'H2')], 'displacement', 'aluminium with hydrochloric acid'),
    ([(1, 'MnO2'), (4, 'HCl')], [(1, 'MnCl2'), (2, 'H2O'), (1, 'Cl2')], 'redox', 'manganese dioxide with hydrochloric acid'),
    ([(1, 'ZnCO3')], [(1, 'ZnO'), (1, 'CO2')], 'decomposition', 'calcination of zinc carbonate'),
    ([(2, 'Cu'), (1, 'O2')], [(2, 'CuO')], 'combination', 'heating copper powder in air'),
    ([(2, 'KClO3')], [(2, 'KCl'), (3, 'O2')], 'decomposition', 'heating potassium chlorate'),
    ([(2, 'Fe'), (3, 'Cl2')], [(2, 'FeCl3')], 'combination', 'iron with chlorine'),
    ([(1, 'C2H5OH'), (3, 'O2')], [(2, 'CO2'), (3, 'H2O')], 'combustion', 'burning of ethanol'),
    ([(2, 'NaOH'), (1, 'H2SO4')], [(1, 'Na2SO4'), (2, 'H2O')], 'double displacement', 'neutralisation of sulphuric acid'),
    ([(1, 'CaO'), (1, 'H2O')], [(1, 'Ca(OH)2')], 'combination', 'slaking of quicklime'),
    ([(2, 'ZnS'), (3, 'O2')], [(2, 'ZnO'), (2, 'SO2')], 'roasting', 'roasting of zinc blende'),
    ([(1, 'ZnO'), (1, 'C')], [(1, 'Zn'), (1, 'CO')], 'redox', 'reduction of zinc oxide with carbon'),
    ([(2, 'HgO')], [(2, 'Hg'), (1, 'O2')], 'decomposition', 'heating mercuric oxide'),
    ([(3, 'MnO2'), (4, 'Al')], [(3, 'Mn'), (2, 'Al2O3')], 'displacement', 'reduction of manganese dioxide by aluminium'),
    ([(2, 'Cu2S'), (3, 'O2')], [(2, 'Cu2O'), (2, 'SO2')], 'roasting', 'roasting of copper glance'),
    ([(1, 'NaOH'), (1, 'HCl')], [(1, 'NaCl'), (1, 'H2O')], 'double displacement', 'neutralisation'),
    ([(2, 'AgBr')], [(2, 'Ag'), (1, 'Br2')], 'decomposition', 'silver bromide in sunlight'),
]
MASS['Br'] = 80
MASS['Hg'] = 201
for _l, _r, *_ in RXN:
    assert side(_l) == side(_r), (_l, _r)
RXN_BAL = [x for x in RXN if any(c != 1 for c, _ in x[0] + x[1])]

c1s1_defs = [
    ('a chemical reaction', 'a process in which one or more substances change to form new substances with different properties'),
    ('a chemical equation', 'a symbolic representation of a chemical reaction using formulae of reactants and products'),
    ('reactants', 'the substances that take part in a chemical reaction'),
    ('products', 'the new substances formed in a chemical reaction'),
    ('a precipitate', 'an insoluble solid formed in a solution during a chemical reaction'),
    ('an exothermic reaction', 'a reaction in which heat is released along with the products'),
    ('an endothermic reaction', 'a reaction in which heat is absorbed'),
]
c1s1_obs = {
    'a change in colour': ['an iron nail turning brown in copper sulphate solution', 'brown copper powder turning black on heating in air', 'blue copper sulphate solution turning colourless when zinc is added'],
    'evolution of a gas': ['zinc granules added to dilute sulphuric acid', 'washing soda added to dilute hydrochloric acid', 'electrolysis of water', 'marble chips added to dilute hydrochloric acid'],
    'formation of a precipitate': ['lead nitrate solution mixed with potassium iodide solution', 'barium chloride solution mixed with sodium sulphate solution', 'silver nitrate solution mixed with sodium chloride solution'],
    'a change in temperature': ['quicklime added to water', 'mixing dilute hydrochloric acid with sodium hydroxide solution', 'dissolving ammonium chloride in water (solution gets cold)'],
}
c1s1_mc = [
    ('Magnesium ribbon is cleaned with sandpaper before burning in order to:', 'remove the layer of magnesium oxide on its surface', 'make it shiny', 'increase its mass', 'cool it'),
    ('When magnesium ribbon burns in air, it gives:', 'a dazzling white flame and a white powder', 'a blue flame and black powder', 'no flame', 'a yellow flame and green powder'),
    ('Which observation shows that a chemical reaction has taken place when lead nitrate and potassium iodide solutions are mixed?', 'a yellow precipitate forms', 'the solution boils', 'a gas is evolved', 'the solution turns blue'),
    ('When quicklime is added to water, the beaker becomes hot. This shows that the reaction is:', 'exothermic', 'endothermic', 'a decomposition', 'a physical change'),
    ('Respiration is considered an exothermic reaction because:', 'energy is released when glucose combines with oxygen', 'it needs sunlight', 'heat is absorbed', 'it produces oxygen'),
    ('The colour of the precipitate formed when barium chloride reacts with sodium sulphate is:', 'white', 'yellow', 'blue', 'black'),
    ('When zinc granules react with dilute sulphuric acid, the gas evolved:', 'burns with a pop sound', 'turns lime water milky', 'relights a glowing splinter', 'smells of rotten eggs'),
]
c1s1_why = [
    ('Why should a magnesium ribbon be cleaned before burning it in air?', 'Magnesium reacts with oxygen to form a layer of magnesium oxide on the surface, which slows burning; cleaning removes it.', '1 mark: oxide layer. 1 mark: hinders burning.'),
    ('How will you show that the gas formed when zinc reacts with dilute sulphuric acid is hydrogen?', 'Bring a burning splinter near the mouth of the test tube; the gas burns with a pop sound.', '1 mark test. 1 mark observation.'),
    ('Why is respiration called an exothermic reaction?', 'Glucose combines with oxygen in cells to form carbon dioxide and water, releasing energy.', '1 mark reaction. 1 mark energy released.'),
    ('What change do you observe when ferrous sulphate crystals are heated, and what does it show?', 'The green colour changes to reddish brown (Fe₂O₃) and a smell of burning sulphur is noticed; a decomposition reaction has occurred.', '1 mark observation. 1 mark conclusion.'),
    ('Name two observations that show a chemical reaction has taken place when an iron nail is kept in copper sulphate solution.', 'The blue colour of the solution fades (becomes light green) and a reddish-brown coating of copper forms on the nail.', '1 mark each.'),
]
c1s1_ar = [
    ('A precipitate of lead iodide forms when lead nitrate solution is mixed with potassium iodide solution.', 'Lead iodide is insoluble in water.', 'a', 'R explains A.'),
    ('Dissolving quicklime in water is an exothermic process.', 'Heat is released when calcium oxide reacts with water.', 'a', 'R explains A.'),
    ('Burning of magnesium is a chemical change.', 'A new substance, magnesium oxide, is formed.', 'a', 'R explains A.'),
    ('Evaporation of water is a chemical reaction.', 'Water vapour has the same composition as water.', 'd', 'A is false (it is a physical change); R is true.'),
]


def c1s1_class(r):
    l, rr, t, note = r.choice(RXN)
    exo = t in ('combination', 'combustion') or note in ('neutralisation', 'neutralisation of sulphuric acid', 'slaking of quicklime', 'thermit reaction', 'sodium with water')
    endo = t == 'decomposition'
    if note == 'heating potassium chlorate':
        raise ValueError
    if not (exo or endo):
        raise ValueError
    a = 'exothermic' if exo else 'endothermic'
    return {'stem': f'Is the reaction {eqn(l, rr)} ({note}) exothermic or endothermic? Give a reason.',
            'answer': f'{cap(a)}; ' + ('heat is released as the products form.' if exo else 'energy (heat, light or electricity) must be supplied to break the reactant.'),
            'key': f'{cap(a)} (1 mark); reason (1 mark).'}


c1s2_defs = [
    ('a balanced chemical equation', 'an equation in which the number of atoms of each element is the same on both sides'),
    ('a skeletal chemical equation', 'an unbalanced equation showing only the formulae of reactants and products'),
    ('the law of conservation of mass', 'the law that mass can neither be created nor destroyed in a chemical reaction'),
    ('a state symbol', 'a symbol such as (s), (l), (g) or (aq) written with a formula to show the physical state'),
    ('the hit-and-trial method', 'balancing an equation by trying the smallest whole-number coefficients until atoms on both sides are equal'),
]
c1s2_mc = [
    ('Chemical equations are balanced to satisfy the law of:', 'conservation of mass', 'constant proportions', 'multiple proportions', 'conservation of energy'),
    ('The symbol (aq) in an equation means the substance is:', 'dissolved in water', 'a gas', 'a liquid', 'a solid'),
    ('In the equation 2H₂ + O₂ → 2H₂O, the number of oxygen atoms on each side is:', '2', '1', '4', '3'),
    ('Which of these equations is balanced?', '2Mg + O₂ → 2MgO', 'Mg + O₂ → MgO', 'H₂ + O₂ → H₂O', 'Na + H₂O → NaOH + H₂'),
    ('Conditions such as temperature, pressure or catalyst are written:', 'above or below the arrow', 'in the reactants', 'after the products', 'they are never written'),
    ('While balancing, we must not change the:', 'formulae (subscripts) of the substances', 'coefficients', 'number of molecules', 'state symbols'),
]
c1s2_why = [
    ('Why should a chemical equation be balanced?', 'Atoms are neither created nor destroyed in a reaction, so the number of atoms of each element must be equal on both sides (law of conservation of mass).', '1 mark atoms conserved. 1 mark law.'),
    ('Why can we not balance H₂ + O₂ → H₂O by writing H₂ + O₂ → H₂O₂?', 'Changing the subscript changes the substance (H₂O₂ is hydrogen peroxide, not water); only coefficients may be changed.', '1 mark different substance. 1 mark coefficients only.'),
    ('How does writing state symbols make an equation more informative?', 'It tells us whether each substance is a solid, liquid, gas or aqueous solution, e.g. 3Fe(s) + 4H₂O(g) → Fe₃O₄(s) + 4H₂(g) shows steam is used.', '1 mark meaning. 1 mark example.'),
]
c1s2_ar = [
    ('A balanced equation has equal numbers of atoms of each element on both sides.', 'Mass is conserved in a chemical reaction.', 'a', 'R explains A.'),
    ('In the equation Fe + H₂O → Fe₃O₄ + H₂, iron must be given a coefficient of 3.', 'There are 3 iron atoms in Fe₃O₄.', 'a', 'R explains A.'),
    ('We can balance an equation by changing the subscripts of formulae.', 'Subscripts tell the number of atoms in a molecule.', 'd', 'A is false (subscripts must not be changed); R is true.'),
]


def c1s2_bal(r):
    l, rr, t, note = r.choice(RXN_BAL)
    return {'stem': f'Balance the following equation ({note}): {eqn([(1, f) for _, f in l], [(1, f) for _, f in rr], show=False)}',
            'answer': eqn(l, rr), 'key': f'Balanced: {eqn(l, rr)}. Atoms of each element are equal on both sides.'}


def c1s2_coef(r):
    l, rr, t, note = r.choice(RXN_BAL)
    allf = l + rr
    i = r.choice([k for k, (c, _) in enumerate(allf) if c != 1])
    c, f = allf[i]
    sk = eqn([(1, x) for _, x in l], [(1, x) for _, x in rr], show=False)
    wrong = [str(x) for x in dict.fromkeys((c + 1, c - 1, c * 2, c + 2, 1, 3)) if x != c and x > 0][:3]
    return {'stem': f'When the equation {sk} is balanced with the smallest whole numbers, what is the coefficient of {sub(f)}?',
            'answer': str(c), 'key': f'{eqn(l, rr)}.', 'distractors': wrong}


def c1s2_count(r):
    l, rr, t, note = r.choice(RXN_BAL)
    tot = side(l)
    e = r.choice(sorted(tot))
    n = tot[e]
    return {'stem': f'In the balanced equation {eqn(l, rr)}, how many atoms of {e} are there on each side?',
            'answer': str(n), 'key': f'Counting on the reactant side: {n}; the product side has the same.',
            'distractors': [str(x) for x in dict.fromkeys((n + 1, n * 2, n - 1, n + 2, n + 3)) if x != n and x > 0][:3]}


DECOMP = [('CaCO3', 'CaO', 'CO2', 'calcium carbonate', 'calcium oxide', 'carbon dioxide'),
          ('ZnCO3', 'ZnO', 'CO2', 'zinc carbonate', 'zinc oxide', 'carbon dioxide'),
          ('MgCO3', 'MgO', 'CO2', 'magnesium carbonate', 'magnesium oxide', 'carbon dioxide')]


def c1s2_mass(r):
    f, p, g, n1, n2, n3 = r.choice(DECOMP)
    m = r.choice([10, 20, 25, 50, 100, 200])
    k = molar(p) / molar(f)
    mp = m * k
    mg = m - mp
    return {'stem': f'On heating, {m} g of {n1} gives {sig(mp, 4)} g of {n2} and {n3} gas only. Using the law of conservation of mass, find the mass of {n3} produced.',
            'answer': f'{sig(mg, 4)} g', 'key': f'Mass of reactants = mass of products: {m} = {sig(mp, 4)} + x, so x = {sig(mg, 4)} g.',
            'distractors': [f'{sig(m + mp, 4)} g', f'{sig(mp, 4)} g', f'{sig(mg * 2, 4)} g']}


c1s3_defs = [
    ('a combination reaction', 'a reaction in which two or more substances combine to form a single product'),
    ('a decomposition reaction', 'a reaction in which a single reactant breaks down to give simpler products'),
    ('a displacement reaction', 'a reaction in which a more reactive element displaces a less reactive element from its compound'),
    ('a double displacement reaction', 'a reaction in which there is an exchange of ions between the reactants'),
    ('a precipitation reaction', 'a reaction that produces an insoluble substance (precipitate)'),
    ('thermal decomposition', 'decomposition of a substance by heating'),
    ('photolytic decomposition', 'decomposition of a substance by light'),
    ('electrolytic decomposition', 'decomposition of a substance by passing electricity'),
]
RTYPE = {}
for _l, _r, _t, _n in RXN:
    tt = {'combustion': None, 'redox': None, 'roasting': None, 'other': None}.get(_t, _t)
    if tt:
        RTYPE.setdefault(f'a {tt} reaction', []).append(eqn(_l, _r))
c1s3_mc = [
    ('The reaction 2AgCl → 2Ag + Cl₂ in sunlight is used in:', 'black and white photography', 'making soaps', 'refining copper', 'making cement'),
    ('Which energy is used in the electrolysis of water?', 'electrical energy', 'light energy', 'heat energy', 'sound energy'),
    ('The reaction between an acid and a base is an example of:', 'a double displacement reaction', 'a combination reaction', 'a decomposition reaction', 'a displacement reaction'),
    ('In the electrolysis of water, the volume of gas collected at the cathode is:', 'double that at the anode (hydrogen)', 'half that at the anode', 'equal to that at the anode', 'zero'),
    ('Calcium oxide reacts vigorously with water to produce slaked lime. This is:', 'a combination reaction that is exothermic', 'a decomposition reaction', 'an endothermic reaction', 'a displacement reaction'),
    ('Decomposition of vegetable matter into compost is an example of:', 'an exothermic reaction', 'an endothermic reaction', 'a displacement reaction', 'a double displacement reaction'),
]
c1s3_why = [
    ('Why are decomposition reactions called the opposite of combination reactions?', 'In combination, two or more reactants form one product; in decomposition, one reactant breaks into two or more products.', '1 mark each.'),
    ('Why does the colour of copper sulphate solution change when an iron nail is dipped in it?', 'Iron is more reactive than copper and displaces it, forming light-green ferrous sulphate; copper is deposited.', '1 mark displacement. 1 mark FeSO₄ colour.'),
    ('Why is silver chloride kept in dark-coloured bottles?', 'In sunlight it decomposes into silver and chlorine (photolytic decomposition).', '1 mark light. 1 mark decomposition.'),
    ('In the electrolysis of water, why is the volume of one gas double that of the other?', 'Water (H₂O) has two hydrogen atoms for each oxygen atom, so 2 volumes of hydrogen and 1 volume of oxygen form.', '1 mark ratio. 1 mark reason.'),
]
c1s3_ar = [
    ('The reaction Fe + CuSO₄ → FeSO₄ + Cu is a displacement reaction.', 'Iron is more reactive than copper.', 'a', 'R explains A.'),
    ('Heating calcium carbonate is a decomposition reaction.', 'It needs heat energy to break down into calcium oxide and carbon dioxide.', 'a', 'R explains A.'),
    ('The reaction between BaCl₂ and Na₂SO₄ is a double displacement reaction.', 'A white precipitate of BaSO₄ is formed.', 'b', 'Both true; the exchange of ions (not the precipitate) makes it double displacement.'),
    ('All decomposition reactions are exothermic.', 'Decomposition needs energy to break the reactant.', 'd', 'A is false (most decomposition reactions are endothermic); R is true.'),
]


def c1s3_type(r):
    l, rr, t, note = r.choice([x for x in RXN if x[2] in ('combination', 'decomposition', 'displacement', 'double displacement')])
    wrong = [x for x in ('combination', 'decomposition', 'displacement', 'double displacement') if x != t]
    return {'stem': f'Identify the type of reaction: {eqn(l, rr)}', 'answer': f'{t}', 'key': f'{cap(note)}: {t} reaction.', 'distractors': wrong}


def c1s3_typeX(r):
    l, rr, t, note = r.choice([x for x in RXN if x[2] in ('combination', 'decomposition', 'displacement', 'double displacement')])
    why = {'combination': 'two or more reactants form a single product', 'decomposition': 'a single reactant breaks into simpler products',
           'displacement': 'a more reactive element displaces a less reactive one from its compound', 'double displacement': 'the reactants exchange ions'}[t]
    return {'stem': f'Name the type of the reaction {eqn(l, rr)} ({note}) and justify your answer.', 'answer': f'{cap(t)} reaction, because {why}.', 'key': '1 mark type. 1 mark reason.'}


c1s4_defs = [
    ('oxidation', 'the gain of oxygen or loss of hydrogen by a substance during a reaction'),
    ('reduction', 'the loss of oxygen or gain of hydrogen by a substance during a reaction'),
    ('a redox reaction', 'a reaction in which one substance is oxidised while another is reduced'),
    ('an oxidising agent', 'a substance that gives oxygen or removes hydrogen, and is itself reduced'),
    ('a reducing agent', 'a substance that removes oxygen or gives hydrogen, and is itself oxidised'),
    ('corrosion', 'the slow eating away of a metal by the action of air, moisture or chemicals on its surface'),
    ('rancidity', 'the oxidation of fats and oils in food that changes their smell and taste'),
]
REDOX = [
    ('CuO + H₂ → Cu + H₂O', 'H₂', 'CuO'), ('ZnO + C → Zn + CO', 'C', 'ZnO'), ('MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂', 'HCl', 'MnO₂'),
    ('Fe₂O₃ + 2Al → Al₂O₃ + 2Fe', 'Al', 'Fe₂O₃'), ('Fe₂O₃ + 3CO → 2Fe + 3CO₂', 'CO', 'Fe₂O₃'), ('PbO + C → Pb + CO', 'C', 'PbO'),
    ('H₂S + Cl₂ → S + 2HCl', 'H₂S', 'Cl₂'), ('3MnO₂ + 4Al → 3Mn + 2Al₂O₃', 'Al', 'MnO₂'), ('2Cu + O₂ → 2CuO', 'Cu', 'O₂'),
    ('CuO + C → Cu + CO', 'C', 'CuO'), ('2Mg + CO₂ → 2MgO + C', 'Mg', 'CO₂'), ('ZnO + CO → Zn + CO₂', 'CO', 'ZnO'),
]
c1s4_mc = [
    ('The brown coating on iron objects left in moist air is:', 'rust (hydrated iron(III) oxide)', 'iron sulphate', 'iron chloride', 'iron carbonate'),
    ('The black coating on silver articles is:', 'silver sulphide', 'silver oxide', 'silver chloride', 'silver nitrate'),
    ('Copper acquires a green coating in moist air due to:', 'basic copper carbonate', 'copper sulphate', 'copper oxide', 'copper chloride'),
    ('Chips packets are flushed with nitrogen to:', 'prevent oxidation (rancidity) of the oil', 'make them heavier', 'keep them cool', 'kill bacteria'),
    ('Antioxidants are added to foods containing fats to:', 'slow down rancidity', 'increase colour', 'speed up cooking', 'add sweetness'),
    ('In 2Cu + O₂ → 2CuO, copper is:', 'oxidised', 'reduced', 'neither oxidised nor reduced', 'decomposed'),
]
c1s4_why = [
    ('Why are food items such as chips packed in packets flushed with nitrogen?', 'Nitrogen is unreactive and keeps oxygen out, so the oils and fats do not get oxidised and become rancid.', '1 mark unreactive. 1 mark prevents oxidation.'),
    ('Why does an iron bridge need to be painted regularly?', 'Paint keeps air and moisture away from iron and so prevents rusting (corrosion).', '1 mark barrier. 1 mark prevents rust.'),
    ('Why is keeping food in an air-tight container or a refrigerator useful?', 'It reduces contact with oxygen and slows oxidation, delaying rancidity.', '1 mark less oxygen. 1 mark slower rancidity.'),
    ('Why is corrosion a serious problem?', 'Every year huge sums are spent replacing damaged iron in bridges, ships, cars and railings; it weakens structures.', '1 mark cost. 1 mark weakening.'),
]
c1s4_ar = [
    ('In CuO + H₂ → Cu + H₂O, copper oxide is reduced.', 'Copper oxide loses oxygen.', 'a', 'R explains A.'),
    ('Rusting of iron needs both air and water.', 'Iron nails kept in dry air or in boiled water under oil do not rust.', 'a', 'R explains A.'),
    ('Silver articles turn black after some time.', 'Silver reacts with sulphur compounds in the air to form silver sulphide.', 'a', 'R explains A.'),
    ('Oxidation is the gain of hydrogen.', 'Reduction is the gain of hydrogen.', 'd', 'A is false; R is true.'),
]


def c1s4_redox(r):
    e, ox, red = r.choice(REDOX)
    return {'stem': f'In the reaction {e}, identify the substance oxidised and the substance reduced.', 'answer': f'Oxidised: {ox}. Reduced: {red}.',
            'key': f'{ox} gains oxygen or loses hydrogen (oxidised, the reducing agent); {red} loses oxygen or gains hydrogen (reduced, the oxidising agent).'}


def c1s4_agent(r):
    e, ox, red = r.choice(REDOX)
    q = r.choice(['oxidising agent', 'reducing agent'])
    a = red if q == 'oxidising agent' else ox
    others = [x for x in {ox, red} if x != a]
    pool = [x for x in re.findall(r'[A-Z][A-Za-z₀-₉]*', e) if x not in (a,)]
    wrong = list(dict.fromkeys(others + pool))[:3]
    if len(wrong) < 3:
        raise ValueError
    return {'stem': f'In the reaction {e}, which substance is the {q}?', 'answer': a, 'key': f'{red} is reduced, so it is the oxidising agent; {ox} is oxidised, so it is the reducing agent.', 'distractors': wrong}


c1_hots = [
    ('A shiny brown metal X on heating in air turns black. When hydrogen is passed over the hot black substance, it turns brown again. Identify X and the black substance and write both equations, naming the type of each.', 'X is copper; the black substance is copper(II) oxide. 2Cu + O₂ → 2CuO (combination, oxidation); CuO + H₂ → Cu + H₂O (redox: CuO reduced, H₂ oxidised).', '1 mark identification. 1 mark each equation.'),
    ('A student kept iron nails in three test tubes: (A) in tap water, (B) in boiled water with a layer of oil, (C) with anhydrous calcium chloride. In which do the nails rust? What does this show?', 'Only in A. B has no air (boiled water, oil layer) and C has no moisture; rusting needs both air and water.', '1 mark A. 1 mark reasons. 1 mark conclusion.'),
    ('Why does a solution of lead nitrate and potassium iodide give a yellow precipitate while sodium chloride and potassium nitrate solutions on mixing give no change?', 'Lead nitrate and KI exchange ions to form insoluble PbI₂; NaCl and KNO₃ would give NaNO₃ and KCl, which are both soluble, so no precipitate forms.', '1 mark exchange. 1 mark insoluble PbI₂. 1 mark soluble products.'),
    ('Calcium oxide reacts with water to form slaked lime, which is used for white-washing walls. After two to three days the walls become shiny. Explain with equations.', 'CaO + H₂O → Ca(OH)₂ (combination, exothermic). Ca(OH)₂ reacts slowly with CO₂ in air: Ca(OH)₂ + CO₂ → CaCO₃ + H₂O; a thin shiny layer of calcium carbonate forms.', '1 mark first equation. 1 mark second. 1 mark shine due to CaCO₃.'),
]


def c1_case(r):
    m = r.choice([5, 10, 20, 25, 50])
    mo = m * molar('CaO') / molar('CaCO3')
    return {'stem': (f'Read: In a lime kiln in Katni, {m} kg of limestone (CaCO₃) is heated strongly. It gives quicklime and a gas that turns lime water milky. The quicklime is added to water in a drum; the drum becomes very hot.\n'
                     '(i) Write the balanced equation for heating limestone and name the type of reaction. (ii) Find the mass of quicklime formed (Ca = 40, C = 12, O = 16). (iii) Write the equation for adding quicklime to water. (iv) Is the second reaction exothermic or endothermic?'),
            'answer': f'(i) CaCO₃ → CaO + CO₂; thermal decomposition. (ii) {sig(mo, 3)} kg. (iii) CaO + H₂O → Ca(OH)₂. (iv) Exothermic.',
            'key': f'(ii) 100 g of CaCO₃ gives 56 g CaO, so {m} kg gives {m} × 56/100 = {sig(mo, 3)} kg. 1 mark each part.'}


c1_long = [
    ('What is a balanced chemical equation? Why should equations be balanced? Balance the following and name the type of each: (a) Fe + H₂O → Fe₃O₄ + H₂ (b) Pb(NO₃)₂ → PbO + NO₂ + O₂ (c) BaCl₂ + Na₂SO₄ → BaSO₄ + NaCl.',
     'Equal number of atoms of each element on both sides; to obey the law of conservation of mass. (a) 3Fe + 4H₂O → Fe₃O₄ + 4H₂ (displacement). (b) 2Pb(NO₃)₂ → 2PbO + 4NO₂ + O₂ (thermal decomposition). (c) BaCl₂ + Na₂SO₄ → BaSO₄ + 2NaCl (double displacement, precipitation).',
     '1 mark definition; 1 mark reason; 1 mark each equation.'),
    ('Explain with one example and equation each: combination, decomposition, displacement and double displacement reactions. Which of them is used to obtain metals from their oxides?',
     'Combination: CaO + H₂O → Ca(OH)₂. Decomposition: CaCO₃ → CaO + CO₂. Displacement: Fe + CuSO₄ → FeSO₄ + Cu. Double displacement: Na₂SO₄ + BaCl₂ → BaSO₄ + 2NaCl. Displacement (e.g. thermit Fe₂O₃ + 2Al → 2Fe + Al₂O₃) / reduction is used to obtain metals.',
     '1 mark each type; 1 mark last part.'),
    ('Define oxidation and reduction in terms of oxygen and hydrogen. Identify the substances oxidised and reduced in (a) ZnO + C → Zn + CO (b) MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂. Explain corrosion and rancidity with one way to prevent each.',
     'Oxidation: gain of oxygen/loss of hydrogen; reduction: loss of oxygen/gain of hydrogen. (a) C oxidised, ZnO reduced. (b) HCl oxidised, MnO₂ reduced. Corrosion: metal attacked by air and moisture (rusting) – prevent by painting/galvanising. Rancidity: oxidation of fats – prevent by antioxidants/nitrogen flushing/air-tight packing.',
     '1 mark definitions; 2 marks identification; 2 marks corrosion and rancidity.'),
    ('What happens when (a) silver chloride is kept in sunlight, (b) electricity is passed through acidified water, (c) ferrous sulphate crystals are heated? Write equations and state the type of energy used in each.',
     '(a) 2AgCl → 2Ag + Cl₂, turns grey; light. (b) 2H₂O → 2H₂ + O₂, hydrogen at cathode is double the volume of oxygen at anode; electrical. (c) 2FeSO₄ → Fe₂O₃ + SO₂ + SO₃, green to reddish brown with burning sulphur smell; heat.',
     '1½ marks each (rounded); ½ mark energy types.'),
]

# ======================= ch02 Acids, Bases and Salts
ACIDS = [('hydrochloric acid', 'HCl', 1, 'chloride', 'Cl', 1, True), ('sulphuric acid', 'H2SO4', 2, 'sulphate', 'SO4', 2, True),
         ('nitric acid', 'HNO3', 1, 'nitrate', 'NO3', 1, True), ('acetic acid', 'CH3COOH', 1, 'acetate', 'CH3COO', 1, False),
         ('carbonic acid', 'H2CO3', 2, 'carbonate', 'CO3', 2, False)]
BASES = [('sodium hydroxide', 'NaOH', 'sodium', 'Na', 1, True), ('potassium hydroxide', 'KOH', 'potassium', 'K', 1, True),
         ('calcium hydroxide', 'Ca(OH)2', 'calcium', 'Ca', 2, True), ('magnesium hydroxide', 'Mg(OH)2', 'magnesium', 'Mg', 2, False),
         ('ammonium hydroxide', 'NH4OH', 'ammonium', 'NH4', 1, False)]
POLY = {'SO4', 'NO3', 'CO3', 'CH3COO', 'NH4', 'OH'}


def ionic(cat, cv, an, av):
    g = gcd(cv, av)
    nc, na = av // g, cv // g

    def part(sym, n):
        if n == 1:
            return sym
        return (f'({sym})' if sym in POLY else sym) + str(n)
    if an == 'CH3COO':
        return 'CH3COO' + cat if na == 1 else f'(CH3COO){na}{cat}'
    return part(cat, nc) + part(an, na)


def neut(acid, base):
    an_name, af, ah, sname, an, av, sa = acid
    bn, bf, cname, cat, cv, sb = base
    salt = ionic(cat, cv, an, av)
    if salt is None:
        return None
    # coefficients: a acid + b base -> c salt + w H2O
    g = gcd(cv, av)
    nc, na = av // g, cv // g
    a_c = na * 1  # acid molecules supply na anions
    b_c = nc
    w = a_c * ah
    spec_l, spec_r = [(a_c, af), (b_c, bf)], [(1, salt), (w, 'H2O')]
    if side(spec_l) != side(spec_r):
        return None
    return salt, f'{cname} {sname}', eqn(spec_l, spec_r), sa, sb


NEUT = []
for _a in ACIDS[:4]:
    for _b in BASES:
        _x = neut(_a, _b)
        if _x:
            NEUT.append((_a, _b) + _x)

c2s1_defs = [
    ('an acid', 'a substance that is sour in taste, turns blue litmus red and gives H⁺ ions in water'),
    ('a base', 'a substance that is bitter, soapy to touch, turns red litmus blue and gives OH⁻ ions in water'),
    ('an indicator', 'a substance that changes colour or smell to show whether a solution is acidic or basic'),
    ('an olfactory indicator', 'a substance whose smell changes in acidic or basic medium, such as onion or clove oil'),
    ('neutralisation', 'the reaction between an acid and a base to give a salt and water'),
    ('an alkali', 'a base that is soluble in water'),
]
c2s1_ind = {
    'phenolphthalein': ('colourless', 'pink'), 'methyl orange': ('red', 'yellow'), 'blue litmus': ('red', 'blue (no change)'),
    'red litmus': ('red (no change)', 'blue'), 'turmeric': ('yellow (no change)', 'reddish brown'), 'red cabbage juice': ('red', 'green'),
}
c2s1_mc = [
    ('Which gas is evolved when zinc reacts with dilute hydrochloric acid?', 'hydrogen', 'oxygen', 'chlorine', 'carbon dioxide'),
    ('Which gas is evolved when sodium carbonate reacts with dilute hydrochloric acid?', 'carbon dioxide', 'hydrogen', 'chlorine', 'oxygen'),
    ('Zinc reacts with sodium hydroxide solution on heating to give:', 'sodium zincate and hydrogen', 'zinc hydroxide and sodium', 'zinc oxide and water', 'no reaction'),
    ('Copper oxide reacts with dilute hydrochloric acid to give a:', 'blue-green solution of copper(II) chloride', 'white precipitate', 'colourless gas', 'red solution'),
    ('Metal oxides are generally:', 'basic in nature', 'acidic in nature', 'neutral', 'amphoteric always'),
    ('Non-metallic oxides such as CO₂ are:', 'acidic in nature', 'basic in nature', 'neutral always', 'salts'),
    ('Which of these is an olfactory indicator?', 'clove oil', 'litmus', 'phenolphthalein', 'methyl orange'),
]
c2s1_why = [
    ('Why should curd and sour substances not be kept in brass and copper vessels?', 'They contain acids, which react with copper and brass to form poisonous compounds and spoil the food.', '1 mark acid reacts. 1 mark poisonous.'),
    ('How will you test the gas formed when a metal reacts with an acid?', 'Bring a burning candle near the gas; it burns with a pop sound, showing it is hydrogen.', '1 mark test. 1 mark result.'),
    ('Why does lime water turn milky when the gas from marble chips and hydrochloric acid is passed through it?', 'The gas is CO₂, which reacts with calcium hydroxide to form insoluble white calcium carbonate: Ca(OH)₂ + CO₂ → CaCO₃ + H₂O.', '1 mark CO₂. 1 mark CaCO₃.'),
    ('Why is the reaction between an acid and a base called neutralisation?', 'The acid and base cancel each other\'s effect, forming salt and water, and the resulting solution is neutral if both are strong.', '1 mark cancel effect. 1 mark salt and water.'),
]
c2s1_ar = [
    ('Metal oxides react with acids to give salt and water.', 'Metal oxides are basic in nature.', 'a', 'R explains A.'),
    ('Hydrogen gas is evolved when zinc reacts with dilute HCl.', 'Zinc is more reactive than hydrogen.', 'a', 'R explains A.'),
    ('Carbon dioxide reacts with calcium hydroxide to give a salt and water.', 'Carbon dioxide is a non-metallic oxide, which is acidic.', 'a', 'R explains A.'),
    ('Phenolphthalein turns pink in an acid.', 'Phenolphthalein is a synthetic indicator.', 'd', 'A is false (it is colourless in acid, pink in base); R is true.'),
]


def c2s1_ind_q(r):
    ind = r.choice(list(c2s1_ind))
    med = r.choice(['acidic', 'basic'])
    col = c2s1_ind[ind][0 if med == 'acidic' else 1]
    pool = sorted({c for v in c2s1_ind.values() for c in v if c.split(' (')[0] != col.split(' (')[0]})
    wrong = [w for w in pool if w.split(' (')[0] not in (col.split(' (')[0],)]
    return {'stem': f'What colour does {ind} show in a {med} solution?', 'answer': col, 'key': f'{cap(ind)}: {c2s1_ind[ind][0]} in acid, {c2s1_ind[ind][1]} in base.',
            'distractors': random_pick(r, wrong, 3)}


def random_pick(r, xs, k):
    xs = list(dict.fromkeys(xs))
    return r.sample(xs, k)


def c2s1_neut(r):
    a, b, salt, sname, e, sa, sb = r.choice(NEUT)
    return {'stem': f'Write the balanced equation for the reaction of {a[0]} with {b[0]} and name the salt formed.',
            'answer': f'{e}; salt: {sname}', 'key': f'Acid + base → salt + water: {e}. 1 mark equation, 1 mark name.'}


def c2s1_salt(r):
    a, b, salt, sname, e, sa, sb = r.choice(NEUT)
    others = list({x[3] for x in NEUT if x[3] != sname})
    return {'stem': f'Which salt is formed when {a[0]} reacts with {b[0]}?', 'answer': sname, 'key': f'{e}.', 'distractors': r.sample(others, 3)}


CARB = [('sodium carbonate', 'Na2CO3', 'Na', 1), ('calcium carbonate', 'CaCO3', 'Ca', 2), ('sodium hydrogencarbonate', 'NaHCO3', 'Na', 1), ('magnesium carbonate', 'MgCO3', 'Mg', 2)]
CARB_EQ = {
    ('Na2CO3', 'HCl'): ([(1, 'Na2CO3'), (2, 'HCl')], [(2, 'NaCl'), (1, 'H2O'), (1, 'CO2')]),
    ('CaCO3', 'HCl'): ([(1, 'CaCO3'), (2, 'HCl')], [(1, 'CaCl2'), (1, 'H2O'), (1, 'CO2')]),
    ('NaHCO3', 'HCl'): ([(1, 'NaHCO3'), (1, 'HCl')], [(1, 'NaCl'), (1, 'H2O'), (1, 'CO2')]),
    ('MgCO3', 'HCl'): ([(1, 'MgCO3'), (2, 'HCl')], [(1, 'MgCl2'), (1, 'H2O'), (1, 'CO2')]),
    ('Na2CO3', 'H2SO4'): ([(1, 'Na2CO3'), (1, 'H2SO4')], [(1, 'Na2SO4'), (1, 'H2O'), (1, 'CO2')]),
    ('NaHCO3', 'H2SO4'): ([(2, 'NaHCO3'), (1, 'H2SO4')], [(1, 'Na2SO4'), (2, 'H2O'), (2, 'CO2')]),
    ('CaCO3', 'HNO3'): ([(1, 'CaCO3'), (2, 'HNO3')], [(1, 'Ca(NO3)2'), (1, 'H2O'), (1, 'CO2')]),
    ('Na2CO3', 'HNO3'): ([(1, 'Na2CO3'), (2, 'HNO3')], [(2, 'NaNO3'), (1, 'H2O'), (1, 'CO2')]),
}
for _l, _r in CARB_EQ.values():
    assert side(_l) == side(_r)
MET_ACID = {
    ('Zn', 'HCl'): ([(1, 'Zn'), (2, 'HCl')], [(1, 'ZnCl2'), (1, 'H2')]), ('Mg', 'HCl'): ([(1, 'Mg'), (2, 'HCl')], [(1, 'MgCl2'), (1, 'H2')]),
    ('Fe', 'HCl'): ([(1, 'Fe'), (2, 'HCl')], [(1, 'FeCl2'), (1, 'H2')]), ('Al', 'HCl'): ([(2, 'Al'), (6, 'HCl')], [(2, 'AlCl3'), (3, 'H2')]),
    ('Zn', 'H2SO4'): ([(1, 'Zn'), (1, 'H2SO4')], [(1, 'ZnSO4'), (1, 'H2')]), ('Mg', 'H2SO4'): ([(1, 'Mg'), (1, 'H2SO4')], [(1, 'MgSO4'), (1, 'H2')]),
    ('Fe', 'H2SO4'): ([(1, 'Fe'), (1, 'H2SO4')], [(1, 'FeSO4'), (1, 'H2')]), ('Al', 'H2SO4'): ([(2, 'Al'), (3, 'H2SO4')], [(1, 'Al2(SO4)3'), (3, 'H2')]),
}
for _l, _r in MET_ACID.values():
    assert side(_l) == side(_r)
MNAME = {'Zn': 'zinc', 'Mg': 'magnesium', 'Fe': 'iron', 'Al': 'aluminium', 'Cu': 'copper', 'Ag': 'silver', 'Pb': 'lead', 'Na': 'sodium', 'K': 'potassium', 'Ca': 'calcium', 'Au': 'gold', 'Hg': 'mercury'}
ANAME = {'HCl': 'dilute hydrochloric acid', 'H2SO4': 'dilute sulphuric acid', 'HNO3': 'dilute nitric acid'}


def c2s1_carb(r):
    (c, a), (l, rr) = r.choice(list(CARB_EQ.items()))
    cn = [x[0] for x in CARB if x[1] == c][0]
    return {'stem': f'Write the balanced equation for the reaction of {cn} with {ANAME[a]}. How will you test the gas evolved?',
            'answer': f'{eqn(l, rr)}; pass the gas through lime water, which turns milky (CO₂).', 'key': '1 mark equation. 1 mark test.'}


def c2s1_metal(r):
    (m, a), (l, rr) = r.choice(list(MET_ACID.items()))
    return {'stem': f'Write the balanced equation for the reaction of {MNAME[m]} with {ANAME[a]} and name the gas evolved.',
            'answer': f'{eqn(l, rr)}; hydrogen gas.', 'key': '1 mark equation. 1 mark gas (burns with a pop).'}


def c2s1_vol(r):
    v1 = r.choice([8, 10, 12, 15, 20, 25])
    v2 = r.choice([5, 6, 8, 9, 10, 12, 16])
    k = r.choice([2, 3, 1.5, 0.5])
    v3 = v1 * k
    ans = v2 * k
    return {'stem': f'{num(v1)} mL of a sodium hydroxide solution is exactly neutralised by {num(v2)} mL of a given hydrochloric acid solution. How much of the same acid is needed to neutralise {num(v3)} mL of the same NaOH solution?',
            'answer': f'{num(ans)} mL', 'key': f'Acid needed is proportional to the base: {num(v2)} × {num(v3)}/{num(v1)} = {num(ans)} mL.',
            'distractors': [f'{num(v1 * v3 / v2, 2)} mL', f'{num(v3)} mL', f'{num(ans + v2)} mL']}


c2s2_defs = [
    ('hydronium ion', 'the H₃O⁺ ion formed when an H⁺ ion combines with a water molecule'),
    ('dilution', 'the process of decreasing the concentration of ions per unit volume by adding water to an acid or a base'),
    ('an electrolyte', 'a substance whose solution conducts electricity because it contains ions'),
    ('an alkali', 'a water-soluble base that gives OH⁻ ions in water, such as NaOH and KOH'),
]
c2s2_mc = [
    ('Acids show acidic behaviour only in the presence of:', 'water', 'oxygen', 'air', 'sunlight'),
    ('A solution of glucose or alcohol does not conduct electricity because:', 'it does not give ions in water', 'it is a strong acid', 'it is a base', 'it is coloured'),
    ('Dry HCl gas does not change the colour of dry blue litmus paper because:', 'H⁺ ions are not formed without water', 'it is a base', 'it is neutral', 'litmus is not an indicator'),
    ('While diluting a concentrated acid, one should:', 'add the acid slowly to water with constant stirring', 'add water to the acid', 'heat the acid', 'add the acid quickly to water'),
    ('All bases that dissolve in water are called:', 'alkalis', 'salts', 'acids', 'indicators'),
    ('Which ion is common to all acids in aqueous solution?', 'H⁺ (H₃O⁺)', 'OH⁻', 'Cl⁻', 'Na⁺'),
]
c2s2_why = [
    ('Why does an aqueous solution of an acid conduct electricity?', 'Acids give H⁺ (H₃O⁺) ions and anions in water; these ions carry the current.', '1 mark ions. 1 mark carry current.'),
    ('Why should water never be added to a concentrated acid?', 'Mixing is highly exothermic; adding water to acid may make the mixture splash out and cause burns, and the glass may break.', '1 mark exothermic. 1 mark splashing.'),
    ('Why do HCl and HNO₃ show acidic character in water while alcohol and glucose do not?', 'HCl and HNO₃ produce H⁺ ions in water; alcohol and glucose contain hydrogen but do not ionise to give H⁺.', '1 mark each.'),
    ('How is the concentration of H₃O⁺ ions affected when a solution of an acid is diluted?', 'It decreases, because the same number of ions is spread through a larger volume.', '1 mark decreases. 1 mark reason.'),
]
c2s2_ar = [
    ('Dry HCl gas does not turn dry blue litmus red.', 'Acids produce H⁺ ions only in the presence of water.', 'a', 'R explains A.'),
    ('Glucose solution does not conduct electricity.', 'Glucose contains hydrogen.', 'b', 'Both are true, but R does not explain A (glucose does not ionise).'),
    ('An acid should be added to water, not water to an acid.', 'Dilution of a concentrated acid is highly exothermic.', 'a', 'R explains A.'),
    ('All bases are alkalis.', 'Alkalis are bases that dissolve in water.', 'd', 'A is false (only soluble bases are alkalis); R is true.'),
]
c2s2_cats = {
    'an electrolyte (conducts in solution)': ['dilute hydrochloric acid', 'sodium hydroxide solution', 'common salt solution', 'dilute sulphuric acid', 'vinegar'],
    'a non-electrolyte (does not conduct)': ['glucose solution', 'alcohol in water', 'distilled water', 'sugar solution'],
}

c2s3_defs = [
    ('the pH scale', 'a scale from 0 to 14 used to measure the hydrogen ion concentration of a solution'),
    ('a strong acid', 'an acid that gives a large number of H⁺ ions in water, such as HCl'),
    ('a weak acid', 'an acid that gives fewer H⁺ ions in water, such as acetic acid'),
    ('a universal indicator', 'a mixture of indicators that shows different colours at different pH values'),
    ('a strong base', 'a base that gives a large number of OH⁻ ions in water, such as NaOH'),
]
PH = [('gastric juice', 1.2), ('lemon juice', 2.2), ('vinegar', 3), ('tomato juice', 4.2), ('coffee', 5), ('pure water', 7),
      ('human blood', 7.4), ('baking soda solution', 8.5), ('milk of magnesia', 10), ('sodium hydroxide solution', 14), ('acid rain', 5), ('milk', 6.6),
      ('soap solution', 10), ('saliva before a meal', 7.4), ('household ammonia', 11.5)]
c2s3_cats = {
    'a strong acid': ['hydrochloric acid', 'sulphuric acid', 'nitric acid'],
    'a weak acid': ['acetic acid', 'citric acid', 'carbonic acid', 'tartaric acid'],
    'a strong base': ['sodium hydroxide', 'potassium hydroxide'],
    'a weak base': ['ammonium hydroxide', 'magnesium hydroxide'],
}
NAT = {
    'lactic acid': 'sour milk (curd)', 'citric acid': 'lemon and orange', 'tartaric acid': 'tamarind', 'acetic acid': 'vinegar',
    'oxalic acid': 'tomato', 'methanoic acid': 'ant sting and nettle sting',
}
c2s3_mc = [
    ('Tooth decay starts when the pH of the mouth falls below:', '5.5', '7', '8.5', '9'),
    ('Our body works within a pH range of about:', '7.0 to 7.8', '1 to 3', '10 to 12', '4 to 5'),
    ('Which is used to relieve indigestion due to excess stomach acid?', 'milk of magnesia (antacid)', 'vinegar', 'lemon juice', 'common salt'),
    ('A bee sting can be treated by rubbing:', 'baking soda (a mild base)', 'vinegar', 'lemon juice', 'sugar'),
    ('Nettle leaves inject which acid?', 'methanoic acid', 'acetic acid', 'citric acid', 'oxalic acid'),
    ('If the pH of soil is too acidic, farmers add:', 'quicklime, slaked lime or chalk', 'vinegar', 'acid', 'common salt'),
    ('The pH of rain water is less than 5.6. It is called:', 'acid rain', 'basic rain', 'neutral rain', 'pure rain'),
    ('A solution turns universal indicator dark green-blue. Its pH is about:', '10', '1', '4', '7'),
]
c2s3_why = [
    ('Why does using toothpaste help prevent tooth decay?', 'Toothpastes are basic and neutralise the acid produced by bacteria from food particles, so the pH stays above 5.5 and enamel is not corroded.', '1 mark basic. 1 mark neutralise acid.'),
    ('Why does the flow of acid rain into rivers make the survival of aquatic life difficult?', 'It lowers the pH of river water; aquatic animals survive only in a narrow pH range.', '1 mark lower pH. 1 mark narrow range.'),
    ('Why do we take an antacid such as milk of magnesia during indigestion?', 'Excess HCl in the stomach causes pain; the mild base neutralises the excess acid.', '1 mark excess acid. 1 mark neutralises.'),
    ('Why is HCl a stronger acid than acetic acid of the same concentration?', 'HCl ionises almost completely in water and gives more H⁺ ions; acetic acid ionises only partly.', '1 mark more H⁺. 1 mark partial ionisation.'),
]
c2s3_ar = [
    ('Tooth decay starts when the pH of the mouth falls below 5.5.', 'Tooth enamel, made of calcium hydroxyapatite, is corroded by acid.', 'a', 'R explains A.'),
    ('HCl is a strong acid.', 'HCl ionises completely in water to give H⁺ ions.', 'a', 'R explains A.'),
    ('A solution of pH 2 is more acidic than one of pH 5.', 'Lower pH means higher H⁺ ion concentration.', 'a', 'R explains A.'),
    ('The pH of pure water is 14.', 'Pure water is neutral.', 'd', 'A is false (it is 7); R is true.'),
]


def c2s3_nature(r):
    n, p = r.choice(PH)
    k = 'acidic' if p < 7 else ('basic' if p > 7 else 'neutral')
    return {'stem': f'The pH of {n} is about {num(p)}. Is it acidic, basic or neutral?', 'answer': k, 'key': f'pH < 7 acidic, 7 neutral, > 7 basic: {num(p)} is {k}.',
            'distractors': [x for x in ('acidic', 'basic', 'neutral', 'amphoteric') if x != k]}


def c2s3_order(r):
    xs = r.sample(PH, 4)
    if len({p for _, p in xs}) < 4:
        raise ValueError
    names = 'ABCD'
    lab = list(zip(names, xs))
    inc = sorted(lab, key=lambda t: t[1][1])
    return {'stem': 'Solutions ' + ', '.join(f'{a} ({n})' for a, (n, p) in lab) + ' have pH values ' + ', '.join(f'{a}: {num(p)}' for a, (n, p) in lab) +
            '. Arrange them in increasing order of hydrogen ion concentration.',
            'answer': ' < '.join(a for a, _ in sorted(lab, key=lambda t: -t[1][1])),
            'key': 'Higher pH means lower H⁺ concentration. Increasing [H⁺]: ' + ' < '.join(f'{a} (pH {num(p)})' for a, (n, p) in sorted(lab, key=lambda t: -t[1][1])) + '.'}


def c2s3_nat(r):
    a = r.choice(list(NAT))
    src = NAT[a]
    wrong = r.sample([x for x in NAT if x != a], 3)
    return {'stem': f'Which acid is naturally present in {src}?', 'answer': a, 'key': f'{cap(src)} contains {a}.', 'distractors': wrong}


c2s4_defs = [
    ('a salt', 'an ionic compound formed by the neutralisation of an acid with a base'),
    ('a family of salts', 'salts having the same positive or the same negative radical'),
    ('water of crystallisation', 'the fixed number of water molecules present in one formula unit of a salt crystal'),
    ('the chlor-alkali process', 'the electrolysis of brine to give sodium hydroxide, chlorine and hydrogen'),
    ('plaster of Paris', 'calcium sulphate hemihydrate (CaSO₄·½H₂O), which sets to a hard mass with water'),
    ('washing soda', 'sodium carbonate decahydrate (Na₂CO₃·10H₂O)'),
    ('baking soda', 'sodium hydrogencarbonate (NaHCO₃)'),
    ('bleaching powder', 'calcium oxychloride (CaOCl₂), made by the action of chlorine on dry slaked lime'),
]
c2s4_use = {
    'baking soda': ['making bread and cake spongy (in baking powder)', 'as an antacid', 'in soda-acid fire extinguishers'],
    'washing soda': ['removing permanent hardness of water', 'manufacture of borax', 'as a cleaning agent for domestic purposes'],
    'bleaching powder': ['bleaching cotton and linen in textile mills', 'disinfecting drinking water', 'as an oxidising agent in industries'],
    'plaster of Paris': ['supporting fractured bones', 'making toys and decorative materials', 'making surfaces smooth'],
    'sodium hydroxide': ['degreasing metals', 'making artificial fibres'],
}
c2s4_cats = {
    'a neutral salt (pH 7)': ['sodium chloride', 'potassium nitrate', 'sodium sulphate', 'potassium chloride'],
    'an acidic salt (pH < 7)': ['ammonium chloride', 'ammonium sulphate', 'copper sulphate'],
    'a basic salt (pH > 7)': ['sodium carbonate', 'sodium hydrogencarbonate', 'sodium acetate', 'potassium carbonate'],
}
HYD = [('copper sulphate pentahydrate', 'CuSO4', 5, 'CuSO₄·5H₂O'), ('washing soda', 'Na2CO3', 10, 'Na₂CO₃·10H₂O'), ('gypsum', 'CaSO4', 2, 'CaSO₄·2H₂O'),
       ('green vitriol (ferrous sulphate)', 'FeSO4', 7, 'FeSO₄·7H₂O'), ('Epsom salt (magnesium sulphate)', 'MgSO4', 7, 'MgSO₄·7H₂O')]
c2s4_mc = [
    ('The chemical formula of plaster of Paris is:', 'CaSO₄·½H₂O', 'CaSO₄·2H₂O', 'CaCO₃', 'CaOCl₂'),
    ('In the chlor-alkali process, chlorine gas is given off at the:', 'anode', 'cathode', 'both electrodes', 'neither'),
    ('Baking powder is a mixture of baking soda and:', 'a mild edible acid such as tartaric acid', 'washing soda', 'common salt', 'bleaching powder'),
    ('Blue copper sulphate crystals turn white on heating because:', 'they lose water of crystallisation', 'copper is removed', 'they melt', 'they gain oxygen'),
    ('Plaster of Paris should be stored in a moisture-proof container because:', 'it sets into hard gypsum with water', 'it catches fire', 'it turns blue', 'it evaporates'),
    ('Rock salt is brown in colour due to:', 'impurities', 'water of crystallisation', 'chlorine', 'iron oxide always'),
    ('Which salt is used to make the sodium hydroxide, chlorine and hydrogen in industry?', 'sodium chloride (brine)', 'sodium carbonate', 'calcium sulphate', 'ammonium chloride'),
]
c2s4_why = [
    ('Why does a cake become soft and spongy when baking powder is added?', 'On heating (or with water), NaHCO₃ reacts with the acid in baking powder to give CO₂, which makes the dough rise.', '1 mark CO₂. 1 mark dough rises.'),
    ('Why is the salt sodium carbonate basic, while ammonium chloride is acidic?', 'Sodium carbonate is made from a strong base (NaOH) and a weak acid (H₂CO₃); ammonium chloride from a weak base (NH₄OH) and a strong acid (HCl).', '1 mark each.'),
    ('How is plaster of Paris prepared, and what happens when it is mixed with water?', 'By heating gypsum at 373 K: CaSO₄·2H₂O → CaSO₄·½H₂O + 1½H₂O. With water it sets to a hard mass of gypsum.', '1 mark preparation. 1 mark setting.'),
    ('Why is bleaching powder used to disinfect drinking water?', 'It releases chlorine, which kills germs in the water.', '2 marks.'),
]
c2s4_ar = [
    ('Sodium chloride solution is neutral.', 'It is formed from a strong acid and a strong base.', 'a', 'R explains A.'),
    ('Copper sulphate crystals turn white on heating.', 'They lose their water of crystallisation.', 'a', 'R explains A.'),
    ('Plaster of Paris is used for setting fractured bones.', 'It sets into a hard solid when mixed with water.', 'a', 'R explains A.'),
    ('Washing soda is used to remove permanent hardness of water.', 'Washing soda is an acidic salt.', 'c', 'A is true; R is false – washing soda is basic.'),
]


def c2s4_nature(r):
    a, b, salt, sname, e, sa, sb = r.choice(NEUT)
    if sa and sb:
        k, why = 'neutral (pH 7)', 'a strong acid and a strong base'
    elif sa and not sb:
        k, why = 'acidic (pH < 7)', 'a strong acid and a weak base'
    elif sb and not sa:
        k, why = 'basic (pH > 7)', 'a weak acid and a strong base'
    else:
        raise ValueError
    return {'stem': f'Will a solution of {sname}, formed from {a[0]} and {b[0]}, be acidic, basic or neutral? Give a reason.', 'answer': f'{cap(k)}; it is formed from {why}.',
            'key': '1 mark nature. 1 mark reason.'}


def c2s4_hyd(r):
    n, f, k, disp = r.choice(HYD)
    M = molar(f) + k * 18
    p = k * 18 / M * 100
    return {'stem': f'Calculate the percentage of water of crystallisation in {n}, {disp}. (H = 1, O = 16, S = 32, Na = 23, C = 12, Ca = 40, Fe = 56, Mg = 24, Cu = 63.5)',
            'answer': f'{sig(p, 3)}%', 'key': f'Molar mass = {num(molar(f), 1)} + {k} × 18 = {num(M, 1)} g/mol; % water = {k * 18}/{num(M, 1)} × 100 = {sig(p, 3)}%.',
            'distractors': [f'{sig(k * 18 / molar(f) * 100, 3)}%', f'{sig(100 - p, 3)}%', f'{sig(18 / M * 100, 3)}%']}


c2_hots = [
    ('A compound X of sodium is used as an antacid and in fire extinguishers. On heating it gives a gas Y that turns lime water milky. Identify X and Y and write the equation for heating X. What is the pH nature of X?', 'X is baking soda NaHCO₃; Y is CO₂. 2NaHCO₃ → Na₂CO₃ + H₂O + CO₂. It is a mild base (pH about 8–9).', '1 mark identification. 1 mark equation. 1 mark nature.'),
    ('Fresh milk has a pH of 6. A milkman adds a very small amount of baking soda to it. Why does he shift the pH towards slightly alkaline, and why does this milk take longer to set as curd?', 'Slightly alkaline milk does not get sour quickly, so it keeps longer. The lactic acid formed during curdling is first neutralised by the base, so curd forms more slowly.', '1 mark keeps longer. 2 marks slower curdling.'),
    ('You have two solutions A (pH 6) and B (pH 8). Which has more H⁺ ions? Which is acidic and which basic? What happens to the pH of A if it is diluted a hundred times with water?', 'A has more H⁺ ions; A is acidic and B basic. On dilution the pH of A increases towards 7, but it does not become basic.', '1 mark each part.'),
    ('Equal lengths of magnesium ribbon are added to test tubes A (HCl) and B (CH₃COOH) of the same concentration. In which tube will the fizzing be more vigorous and why?', 'A: HCl is a strong acid and gives more H⁺ ions, so hydrogen is evolved faster than with weak acetic acid.', '1 mark A. 2 marks reason.'),
]


def c2_case(r):
    n, p = r.choice([x for x in PH if x[1] != 7])
    n2, p2 = r.choice([x for x in PH if (x[1] - 7) * (p - 7) < 0])
    return {'stem': (f'Read: In a school lab, Ananya tests the pH of some liquids with universal indicator paper: {n} gives pH {num(p)} and {n2} gives pH {num(p2)}.\n'
                     f'(i) Which of the two is acidic? (ii) Which has the higher OH⁻ ion concentration? (iii) What colour would phenolphthalein show in the basic liquid? (iv) Why does tooth decay start when the pH in the mouth falls below 5.5?'),
            'answer': f'(i) {n if p < 7 else n2}. (ii) {n2 if p < 7 else n} (higher pH). (iii) Pink. (iv) The acid produced corrodes tooth enamel (calcium hydroxyapatite).',
            'key': '1 mark each part.'}


c2_long = [
    ('What is the chlor-alkali process? Write the equation and name the products formed at the anode and cathode. Give two uses of each product.',
     'Electrolysis of brine: 2NaCl(aq) + 2H₂O(l) → 2NaOH(aq) + Cl₂(g) + H₂(g). Chlorine at the anode, hydrogen at the cathode, NaOH near the cathode. Uses: NaOH – soaps, degreasing metals; Cl₂ – water treatment, PVC, bleaching powder; H₂ – fuels, margarine (hydrogenation), ammonia.',
     '1 mark process; 1 mark equation; 1 mark products; 2 marks uses.'),
    ('Write the chemical name, formula, method of preparation and two uses each of (a) bleaching powder (b) baking soda (c) washing soda.',
     '(a) Calcium oxychloride CaOCl₂; Ca(OH)₂ + Cl₂ → CaOCl₂ + H₂O; bleaching cotton, disinfecting water. (b) Sodium hydrogencarbonate NaHCO₃; NaCl + H₂O + CO₂ + NH₃ → NH₄Cl + NaHCO₃; antacid, baking powder. (c) Sodium carbonate decahydrate Na₂CO₃·10H₂O; recrystallisation of sodium carbonate (from heating baking soda); removing hardness of water, glass industry.',
     '1⅔ marks each (rounded).'),
    ('What is pH? Draw the pH scale showing the variation of H⁺ and OH⁻ concentration. Explain the importance of pH in (a) digestion (b) tooth decay (c) soil (d) bee stings.',
     'pH measures H⁺ concentration on a 0–14 scale: below 7 acidic, 7 neutral, above 7 basic; H⁺ decreases and OH⁻ increases from 0 to 14. (a) Stomach HCl aids digestion; excess is neutralised by antacids. (b) Below pH 5.5 enamel corrodes; basic toothpaste helps. (c) Plants need a specific pH; acidic soil is treated with lime. (d) Methanoic acid in a sting is neutralised with baking soda.',
     '1 mark pH; 1 mark scale; 3 marks applications.'),
    ('Explain the reactions of acids with (a) metals (b) metal carbonates (c) metal oxides (d) bases, with one balanced equation each. How would you show that all acids contain hydrogen?',
     '(a) Zn + H₂SO₄ → ZnSO₄ + H₂. (b) Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂. (c) CuO + 2HCl → CuCl₂ + H₂O. (d) NaOH + HCl → NaCl + H₂O. Solutions of different acids (HCl, H₂SO₄) conduct electricity and react with zinc to give hydrogen; this shows they all give H⁺ ions.',
     '1 mark each reaction; 1 mark last part.'),
]

# ======================= ch03 Metals and Non-metals
SERIES = ['K', 'Na', 'Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Pb', 'H', 'Cu', 'Hg', 'Ag', 'Au']
SALT = {'Mg': ('MgSO4', 'magnesium sulphate', 'colourless'), 'Zn': ('ZnSO4', 'zinc sulphate', 'colourless'), 'Fe': ('FeSO4', 'iron(II) sulphate', 'pale green'),
        'Cu': ('CuSO4', 'copper sulphate', 'blue'), 'Ag': ('AgNO3', 'silver nitrate', 'colourless')}
NITR = {'Mg': 'Mg(NO3)2', 'Zn': 'Zn(NO3)2', 'Fe': 'Fe(NO3)2', 'Cu': 'Cu(NO3)2', 'Pb': 'Pb(NO3)2'}
SULF = {'Mg': 'MgSO4', 'Zn': 'ZnSO4', 'Fe': 'FeSO4', 'Cu': 'CuSO4'}


def disp_pair(x, y):
    """metal x placed in a solution of y's salt. Returns (reacts, equation or None)."""
    rx = SERIES.index(x) < SERIES.index(y)
    sf, sn, col = SALT[y]
    if not rx:
        return False, None, sn
    if y == 'Ag':
        l, rr = [(1, x), (2, 'AgNO3')], [(1, NITR[x]), (2, 'Ag')]
    else:
        l, rr = [(1, x), (1, sf)], [(1, SULF[x]), (1, y)]
    assert side(l) == side(rr)
    return True, eqn(l, rr), sn


def c3s2_disp(r):
    x = r.choice(['Mg', 'Zn', 'Fe', 'Cu'])
    y = r.choice([k for k in SALT if k != x])
    ok, e, sn = disp_pair(x, y)
    if ok:
        ans = f'Yes. {e}. {MNAME[x].capitalize()} is more reactive than {MNAME[y]}.'
    else:
        ans = f'No reaction; {MNAME[x]} is less reactive than {MNAME[y]}.'
    return {'stem': f'A strip of {MNAME[x]} is placed in {sn} solution. Will any reaction occur? If yes, write the equation.', 'answer': ans, 'key': '1 mark yes/no with reason (reactivity series). 1 mark equation.'}


EXTRA_ABOVE = ['sodium chloride solution', 'potassium nitrate solution', 'calcium chloride solution', 'aluminium sulphate solution']
KEY_SERIES = 'Reactivity series: K > Na > Ca > Mg > Al > Zn > Fe > Pb > H > Cu > Hg > Ag > Au. A metal displaces only less reactive metals from their salt solutions.'


def c3s2_dispq(r):
    x = r.choice(['Mg', 'Zn', 'Fe', 'Cu'])
    ys = [k for k in SALT if k != x]
    good = [SALT[y][1] + ' solution' for y in ys if SERIES.index(x) < SERIES.index(y)]
    bad = [SALT[y][1] + ' solution' for y in ys if SERIES.index(x) > SERIES.index(y)]
    bad += [e for e in EXTRA_ABOVE if not (x == 'Mg' and False) and SERIES.index(x) > SERIES.index({'sodium': 'Na', 'potassium': 'K', 'calcium': 'Ca', 'aluminium': 'Al'}[e.split()[0]])]
    if len(good) >= 3 and r.random() < 0.5:
        return {'stem': f'{MNAME[x].capitalize()} metal will NOT displace the metal from which of these solutions?', 'answer': r.choice(bad), 'key': KEY_SERIES, 'distractors': r.sample(good, 3)}
    return {'stem': f'{MNAME[x].capitalize()} metal will displace the metal from which of these solutions?', 'answer': r.choice(good), 'key': KEY_SERIES, 'distractors': r.sample(bad, 3)}


def c3s2_order(r):
    ms = r.sample(['K', 'Na', 'Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Pb', 'Cu', 'Hg', 'Ag', 'Au'], 4)
    o = sorted(ms, key=SERIES.index)
    return {'stem': 'Arrange these metals in decreasing order of reactivity: ' + ', '.join(MNAME[m] for m in ms) + '.', 'answer': ' > '.join(MNAME[m] for m in o),
            'key': 'Reactivity series: K > Na > Ca > Mg > Al > Zn > Fe > Pb > [H] > Cu > Hg > Ag > Au.'}


def c3s2_acid(r):
    m = r.choice(['K', 'Na', 'Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Cu', 'Hg', 'Ag', 'Au'])
    ok = SERIES.index(m) < SERIES.index('H')
    a = 'Yes, hydrogen gas is evolved' if ok else 'No, it does not displace hydrogen'
    return {'stem': f'Does {MNAME[m]} give hydrogen gas with dilute hydrochloric acid? Give a reason.',
            'answer': f'{a}; {MNAME[m]} is {"above" if ok else "below"} hydrogen in the reactivity series.', 'key': '1 mark answer. 1 mark reason.'}


METAL_FACTS = {
    'reacts violently with cold water and is stored under kerosene': ['sodium', 'potassium'],
    'reacts with cold water less violently, and floats as bubbles of hydrogen stick to it': ['calcium'],
    'does not react with cold water but reacts with hot water': ['magnesium'],
    'reacts only with steam to form a metal oxide and hydrogen': ['iron', 'zinc', 'aluminium'],
    'does not react with water at all': ['copper', 'silver', 'gold', 'lead'],
}
c3s1_defs = [
    ('malleability', 'the property of metals by which they can be beaten into thin sheets'),
    ('ductility', 'the property of metals by which they can be drawn into thin wires'),
    ('sonorous', 'producing a ringing sound when struck'),
    ('lustre', 'the shiny appearance of a metal surface'),
    ('a metalloid', 'an element that shows properties of both metals and non-metals'),
]
c3s1_exc = {
    'a metal that is liquid at room temperature': ['mercury'],
    'a non-metal that is liquid at room temperature': ['bromine'],
    'a non-metal that is a good conductor of electricity': ['graphite'],
    'a non-metal that is lustrous': ['iodine'],
    'a metal that can be cut with a knife': ['sodium', 'potassium', 'lithium'],
    'a metal with a melting point so low that it melts in the palm': ['gallium', 'caesium'],
    'the hardest natural substance (a form of carbon)': ['diamond'],
}
c3s1_cats = {
    'a metal': ['copper', 'aluminium', 'zinc', 'mercury', 'sodium', 'iron', 'gold'],
    'a non-metal': ['sulphur', 'carbon', 'oxygen', 'iodine', 'bromine', 'phosphorus', 'nitrogen'],
}
c3s1_mc = [
    ('The best conductors of heat are:', 'silver and copper', 'lead and mercury', 'iron and zinc', 'sodium and potassium'),
    ('The poorest conductors of heat among metals are:', 'lead and mercury', 'silver and copper', 'gold and silver', 'aluminium and copper'),
    ('Which metal is the most ductile?', 'gold', 'iron', 'zinc', 'lead'),
    ('Most non-metals are:', 'poor conductors of heat and electricity', 'malleable', 'sonorous', 'lustrous'),
    ('Which of these is used to make school bells?', 'metals, because they are sonorous', 'non-metals', 'plastic', 'wood'),
    ('Electric wires have a coating of PVC or rubber because:', 'it is a poor conductor and prevents shocks', 'it conducts electricity', 'it is shiny', 'it is sonorous'),
]
c3s1_why = [
    ('Why are cooking vessels made of aluminium or copper while their handles are made of plastic?', 'Metals conduct heat well, so food cooks quickly; plastic is a poor conductor, so the handle stays cool to hold.', '1 mark each.'),
    ('Why is sodium kept immersed in kerosene oil?', 'It reacts so vigorously with oxygen and moisture in air that it catches fire; kerosene keeps air away.', '1 mark reactivity. 1 mark keeps air away.'),
    ('Why are metals used to make thin foils and wires?', 'They are malleable and ductile.', '1 mark each.'),
    ('Give two examples of exceptions to general properties of metals or non-metals.', 'Mercury is a liquid metal; graphite is a non-metal that conducts electricity (also iodine is lustrous, Na/K are soft).', '1 mark each.'),
]
c3s1_ar = [
    ('Gold and silver are used to make jewellery.', 'They are lustrous and do not corrode easily.', 'a', 'R explains A.'),
    ('Graphite is used to make electrodes.', 'Graphite is a good conductor of electricity.', 'a', 'R explains A.'),
    ('Mercury is a metal.', 'All metals are solids at room temperature.', 'c', 'A is true; R is false (mercury itself is a liquid).'),
    ('Sodium can be cut with a knife.', 'Sodium is a soft metal.', 'a', 'R explains A.'),
]

c3s2_defs = [
    ('the reactivity series', 'a list of metals arranged in order of decreasing reactivity'),
    ('an amphoteric oxide', 'a metal oxide that reacts with both acids and bases to give salt and water, such as Al₂O₃ and ZnO'),
    ('aqua regia', 'a freshly prepared mixture of concentrated hydrochloric acid and concentrated nitric acid in the ratio 3:1 that dissolves gold and platinum'),
    ('a basic oxide', 'a metal oxide that reacts with an acid to give salt and water'),
]
c3s2_mc = [
    ('Which metal does not react with oxygen even at high temperature?', 'gold', 'magnesium', 'zinc', 'iron'),
    ('Hydrogen gas is not evolved when a metal reacts with nitric acid because:', 'HNO₃ is a strong oxidising agent and oxidises H₂ to water', 'nitric acid is weak', 'metals do not react with HNO₃', 'it gives oxygen instead'),
    ('Which metals react with very dilute HNO₃ to give hydrogen?', 'magnesium and manganese', 'copper and silver', 'gold and platinum', 'iron and lead'),
    ('Aluminium oxide is:', 'amphoteric', 'acidic', 'basic only', 'neutral'),
    ('Calcium floats when added to water because:', 'bubbles of hydrogen stick to its surface', 'it is lighter than water', 'it does not react', 'it forms oxygen'),
    ('Iron reacts with steam to form:', 'Fe₃O₄ and hydrogen', 'FeO and oxygen', 'Fe(OH)₃', 'no reaction'),
]
c3s2_why = [
    ('Why does copper not give hydrogen with dilute HCl, while zinc does?', 'Zinc is above hydrogen in the reactivity series and displaces it from the acid; copper is below hydrogen.', '1 mark zinc above H. 1 mark copper below.'),
    ('Why is aluminium oxide called amphoteric? Give equations.', 'It reacts with acids and with bases: Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O.', '1 mark each.'),
    ('Why does the blue colour of copper sulphate fade when zinc is added?', 'Zinc displaces copper, forming colourless zinc sulphate, and red-brown copper is deposited.', '1 mark displacement. 1 mark colourless ZnSO₄.'),
    ('Why is a layer of aluminium oxide useful to aluminium?', 'The thin, tough oxide layer protects the metal from further oxidation (corrosion).', '2 marks.'),
]
c3s2_ar = [
    ('Zinc displaces copper from copper sulphate solution.', 'Zinc is more reactive than copper.', 'a', 'R explains A.'),
    ('Copper does not react with dilute HCl.', 'Copper is below hydrogen in the reactivity series.', 'a', 'R explains A.'),
    ('Silver displaces copper from copper sulphate solution.', 'Silver is more reactive than copper.', 'e', ''),
    ('Potassium is stored in kerosene.', 'Potassium reacts vigorously with air and water.', 'a', 'R explains A.'),
]
c3s2_ar[2] = ('Copper displaces silver from silver nitrate solution.', 'Copper is more reactive than silver.', 'a', 'R explains A.')

# ionic compounds
ION_M = {'Na': (11, '2, 8, 1', 1), 'K': (19, '2, 8, 8, 1', 1), 'Mg': (12, '2, 8, 2', 2), 'Ca': (20, '2, 8, 8, 2', 2), 'Al': (13, '2, 8, 3', 3)}
ION_N = {'Cl': (17, '2, 8, 7', 1, 'chloride', 'chlorine'), 'O': (8, '2, 6', 2, 'oxide', 'oxygen'), 'S': (16, '2, 8, 6', 2, 'sulphide', 'sulphur'), 'F': (9, '2, 7', 1, 'fluoride', 'fluorine')}
MNAME.update({'K': 'potassium', 'Na': 'sodium', 'Ca': 'calcium'})


def ion_cmp(m, n):
    zm, cm, vm = ION_M[m]
    zn, cn, vn, an, en = ION_N[n]
    g = gcd(vm, vn)
    a, b = vn // g, vm // g
    f = sub(m + (str(a) if a > 1 else '') + n + (str(b) if b > 1 else ''))
    e = a * vm
    return f, e, f'{MNAME[m]} {an}', zm, cm, vm, zn, cn, vn, en


def c3s3_form(r):
    m, n = r.choice(list(ION_M)), r.choice(list(ION_N))
    f, e, nm, zm, cm, vm, zn, cn, vn, en = ion_cmp(m, n)
    sup = {1: '', 2: '2', 3: '3'}
    return {'stem': f'Show the formation of {nm} from {MNAME[m]} (Z = {zm}) and {en} (Z = {zn}) by transfer of electrons. Write the formula and the number of electrons transferred per formula unit.',
            'answer': f'{MNAME[m].capitalize()} ({cm}) loses {vm} electron{"s" if vm > 1 else ""} to form {m}{sup[vm]}+; {en} ({cn}) gains {vn} to form {n}{sup[vn]}−. Formula {f}; {e} electron{"s" if e > 1 else ""} transferred.',
            'key': '1 mark configurations and ions. 1 mark formula and electrons.'}


def c3s3_formula(r):
    m, n = r.choice(list(ION_M)), r.choice(list(ION_N))
    f, e, nm, *_ = ion_cmp(m, n)
    alt = {sub(x) for x in (m + n, m + n + '2', m + '2' + n, m + '2' + n + '3', m + '3' + n + '2', m + n + '3')} - {f}
    return {'stem': f'What is the formula of {nm}?', 'answer': f, 'key': f'Valency of {m} = {ION_M[m][2]}, of {n} = {ION_N[n][2]}: {f}.', 'distractors': r.sample(sorted(alt), 3)}


c3s3_defs = [
    ('an ionic compound', 'a compound formed by the transfer of electrons from a metal to a non-metal'),
    ('a cation', 'a positively charged ion formed when an atom loses electrons'),
    ('an anion', 'a negatively charged ion formed when an atom gains electrons'),
    ('an electrovalent bond', 'the bond formed by the electrostatic attraction between oppositely charged ions'),
]
c3s3_mc = [
    ('Ionic compounds conduct electricity:', 'in the molten state and in aqueous solution', 'in the solid state only', 'never', 'only as gases'),
    ('Ionic compounds have high melting points because:', 'strong forces of attraction exist between the ions', 'they are liquids', 'they are covalent', 'they have weak bonds'),
    ('Ionic compounds are generally soluble in:', 'water', 'kerosene', 'petrol', 'all organic solvents'),
    ('The electronic configuration of the Mg²⁺ ion is:', '2, 8', '2, 8, 2', '2, 8, 8', '2, 6'),
    ('In forming NaCl, sodium:', 'loses one electron', 'gains one electron', 'shares one electron', 'loses two electrons'),
]
c3s3_why = [
    ('Why do ionic compounds not conduct electricity in the solid state?', 'The ions are held in fixed positions in the crystal and cannot move.', '1 mark fixed ions. 1 mark no movement.'),
    ('Why are ionic compounds hard and brittle?', 'Strong attraction between the ions makes them hard; when force is applied, layers of like ions come together and repel, so they break.', '1 mark each.'),
    ('Why are ionic compounds insoluble in kerosene and petrol?', 'These solvents are non-polar and cannot separate the strongly attracted ions.', '2 marks.'),
]
c3s3_ar = [
    ('Molten sodium chloride conducts electricity.', 'Ions are free to move in the molten state.', 'a', 'R explains A.'),
    ('MgCl₂ is an ionic compound.', 'Magnesium transfers two electrons to two chlorine atoms.', 'a', 'R explains A.'),
    ('Ionic compounds have low melting points.', 'Ions in ionic compounds are held by strong electrostatic forces.', 'd', 'A is false; R is true.'),
]

c3s4_defs = [
    ('a mineral', 'a naturally occurring element or compound found in the earth\'s crust'),
    ('an ore', 'a mineral from which a metal can be extracted profitably'),
    ('gangue', 'the impurities such as soil and sand present in an ore'),
    ('roasting', 'heating a sulphide ore strongly in excess of air to convert it into an oxide'),
    ('calcination', 'heating a carbonate ore strongly in limited air to convert it into an oxide'),
    ('electrolytic refining', 'purification of an impure metal by electrolysis, using the impure metal as anode and a thin strip of pure metal as cathode'),
    ('anode mud', 'the insoluble impurities that settle below the anode during electrolytic refining'),
    ('metallurgy', 'the process of extracting metals from their ores and refining them'),
]
c3s4_cats = {
    'extracted by electrolysis of the molten chloride or oxide': ['sodium', 'potassium', 'calcium', 'magnesium', 'aluminium'],
    'extracted by reduction of the oxide using carbon': ['zinc', 'iron', 'lead'],
    'extracted by heating the sulphide ore in air alone': ['mercury', 'copper'],
    'found free (native) in nature': ['gold', 'silver', 'platinum'],
}
c3s4_ore = {
    'a sulphide ore': ['zinc blende (ZnS)', 'cinnabar (HgS)', 'copper glance (Cu₂S)', 'galena (PbS)'],
    'a carbonate ore': ['calamine (ZnCO₃)', 'limestone (CaCO₃)', 'siderite (FeCO₃)'],
    'an oxide ore': ['haematite (Fe₂O₃)', 'bauxite (Al₂O₃·2H₂O)', 'pyrolusite (MnO₂)'],
}
c3s4_mc = [
    ('Highly reactive metals such as sodium are obtained by:', 'electrolytic reduction of their molten chlorides', 'heating with carbon', 'heating alone', 'roasting'),
    ('In electrolytic refining of copper, the electrolyte is:', 'acidified copper sulphate solution', 'water', 'molten copper', 'sodium chloride solution'),
    ('In electrolytic refining, the pure metal is deposited at the:', 'cathode', 'anode', 'bottom as anode mud', 'surface of the electrolyte'),
    ('The thermit reaction is used to:', 'join railway tracks and cracked machine parts', 'refine copper', 'make steel', 'extract sodium'),
    ('Metals at the bottom of the reactivity series are often found:', 'in the free state', 'as chlorides only', 'never in nature', 'as gases'),
    ('Carbon cannot reduce oxides of sodium and aluminium because:', 'these metals have more affinity for oxygen than carbon', 'carbon is a metal', 'their oxides are gases', 'they are not oxides'),
]
c3s4_why = [
    ('Why is a sulphide ore first converted into an oxide before reduction?', 'It is easier to obtain a metal from its oxide than from its sulphide or carbonate.', '2 marks.'),
    ('Why are sodium and aluminium extracted by electrolysis and not by heating with carbon?', 'They are highly reactive and have a greater affinity for oxygen than carbon, so carbon cannot reduce their oxides.', '1 mark reactive. 1 mark carbon cannot reduce.'),
    ('Explain why mercury can be extracted from cinnabar simply by heating.', 'Mercury is low in the reactivity series; heating HgS in air gives HgO (2HgS + 3O₂ → 2HgO + 2SO₂), which decomposes on further heating (2HgO → 2Hg + O₂).', '1 mark low reactivity. 1 mark equations.'),
]
c3s4_ar = [
    ('Gold is found in the free state in nature.', 'Gold is very unreactive.', 'a', 'R explains A.'),
    ('Aluminium is extracted by electrolysis of molten alumina.', 'Aluminium is highly reactive and cannot be reduced by carbon.', 'a', 'R explains A.'),
    ('Zinc blende is calcined to get zinc oxide.', 'Zinc blende is a sulphide ore.', 'd', 'A is false (sulphide ores are roasted, not calcined); R is true.'),
    ('In electrolytic refining, the impure metal is made the anode.', 'Metal from the anode dissolves and pure metal deposits at the cathode.', 'a', 'R explains A.'),
]

c3s5_defs = [
    ('rusting', 'the corrosion of iron in the presence of air and moisture, forming hydrated iron(III) oxide'),
    ('galvanisation', 'coating iron or steel with a thin layer of zinc to prevent rusting'),
    ('an alloy', 'a homogeneous mixture of two or more metals, or a metal and a non-metal'),
    ('an amalgam', 'an alloy in which one of the metals is mercury'),
    ('anodising', 'forming a thick oxide layer on aluminium by electrolysis to protect it'),
]
c3s5_alloy = {
    'copper and zinc': ['brass'], 'copper and tin': ['bronze'], 'lead and tin': ['solder'],
    'iron, nickel and chromium': ['stainless steel'], 'iron and carbon': ['steel'],
}
c3s5_prev = {
    'galvanising (zinc coating)': ['iron buckets and roofing sheets', 'iron pipes for water'],
    'painting': ['iron bridges and railings', 'iron grills of windows'],
    'oiling or greasing': ['bicycle chains', 'machine parts'],
    'electroplating with chromium': ['bicycle handlebars', 'taps in bathrooms'],
    'alloying': ['stainless steel utensils'],
}
c3s5_mc = [
    ('Galvanised iron does not rust even if the zinc coating is broken because:', 'zinc is more reactive and corrodes in preference to iron', 'zinc is less reactive', 'iron becomes inactive', 'zinc absorbs water'),
    ('Pure gold is 24 carat. 22-carat gold contains:', '22 parts gold and 2 parts silver or copper', '22% gold', 'only gold', '2 parts gold'),
    ('Solder is used to weld electrical wires because it has:', 'a low melting point', 'a high melting point', 'high resistance', 'high reactivity'),
    ('The electrical conductivity of an alloy compared with that of the pure metal is usually:', 'lower', 'higher', 'the same', 'zero'),
    ('Rust is chemically:', 'hydrated iron(III) oxide', 'iron sulphate', 'iron carbonate', 'iron(II) chloride'),
]
c3s5_why = [
    ('Why is pure gold not used for making jewellery?', 'Pure (24-carat) gold is very soft; alloying with silver or copper makes it hard.', '2 marks.'),
    ('Why is the iron pillar near the Qutub Minar in Delhi famous?', 'It was made about 1600 years ago and has not rusted, showing the skill of ancient Indian iron workers.', '1 mark age. 1 mark rust-free.'),
    ('Why are iron sheets galvanised for roofing?', 'The zinc coating keeps air and moisture away and protects iron even if scratched, since zinc is more reactive.', '1 mark barrier. 1 mark sacrificial.'),
]
c3s5_ar = [
    ('Stainless steel does not rust easily.', 'It is an alloy of iron with nickel and chromium.', 'a', 'R explains A.'),
    ('22-carat gold is harder than 24-carat gold.', '22-carat gold is alloyed with copper or silver.', 'a', 'R explains A.'),
    ('Iron rusts in dry air.', 'Rusting needs both air and moisture.', 'd', 'A is false; R is true.'),
]


def c3s5_carat(r):
    c = r.choice([14, 18, 20, 22])
    m = r.choice([5, 8, 10, 12, 20, 25])
    g = m * c / 24
    nm = name(r)
    return {'stem': f'{nm} buys a {m} g {c}-carat gold chain in Jaipur. What percentage of the chain is gold, and what mass of pure gold does it contain? (pure gold = 24 carat)',
            'answer': f'{sig(c / 24 * 100, 3)}%; {sig(g, 3)} g', 'key': f'% gold = {c}/24 × 100 = {sig(c / 24 * 100, 3)}%; mass = {m} × {c}/24 = {sig(g, 3)} g.',
            'distractors': [f'{c}%; {sig(m * c / 100, 3)} g', f'{sig(c / 24 * 100, 3)}%; {sig(m * 24 / c, 3)} g', f'{sig((24 - c) / 24 * 100, 3)}%; {sig(m - g, 3)} g']}


c3_hots = [
    ('An element X forms an oxide X₂O₃ that reacts with both HCl and NaOH. X is found as a protective oxide layer that prevents its corrosion. Identify X, write both reactions of the oxide, and say how X is extracted.', 'X is aluminium. Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O. Extracted by electrolysis of molten alumina.', '1 mark X. 1 mark reactions. 1 mark extraction.'),
    ('Metals A, B, C and D were added to solutions. A displaced B from its salt; C did not react with B\'s salt; D displaced A from its salt. Arrange them in decreasing order of reactivity.', 'D > A > B > C (C is below B).', '1 mark each comparison; 1 mark order.'),
    ('A copper vessel turned green after a few days. A student cleaned it with lemon juice. Explain the green coating and the cleaning, with equations where possible.', 'Copper reacts with moist CO₂ in air to form green basic copper carbonate [CuCO₃·Cu(OH)₂]. Lemon juice (citric acid) reacts with this basic coating and dissolves it, so the shine returns.', '1 mark coating. 1 mark acid. 1 mark basic nature.'),
    ('Why is the reactivity of a metal related to how easily it is extracted? Give one example each of a metal extracted by electrolysis, by carbon reduction and by heating alone.', 'More reactive metals hold oxygen more strongly, so they need more energy (electrolysis); less reactive ones are reduced easily. Electrolysis: Na/Al; carbon: Zn/Fe; heating alone: Hg/Cu.', '1 mark relation. 2 marks examples.'),
]


def c3_case(r):
    x = r.choice(['Zn', 'Fe'])
    ok, e, sn = disp_pair(x, 'Cu')
    third = 'Fe' if x == 'Zn' else 'Zn'
    third_ans = (f'{SALT[third][1]} reacts (zinc displaces iron)' if x == 'Zn' else f'{SALT[third][1]}: no reaction (iron is less reactive than zinc)')
    return {'stem': (f'Read: Rohan put {MNAME[x]} strips in four test tubes containing copper sulphate, silver nitrate, {SALT[third][1]} and magnesium sulphate solutions.\n'
                     '(i) In which tube does a reddish-brown deposit form? Write the equation. (ii) What colour does the solution in that tube become? (iii) In which tube(s) does no reaction occur, and why? (iv) Arrange magnesium, zinc, iron, copper and silver in decreasing order of reactivity.'),
            'answer': f'(i) Copper sulphate: {e}. (ii) {cap(SALT[x][2])}. (iii) Magnesium sulphate' + (f' and {SALT[third][1]}' if x == 'Fe' else '') + f': {MNAME[x]} is less reactive than ' + ('magnesium.' if x == 'Zn' else 'magnesium and zinc.') + ' (iv) Mg > Zn > Fe > Cu > Ag.',
            'key': '1 mark each part.'}


def c3_case2(r):
    c = r.choice([18, 20, 22])
    m = r.choice([10, 20, 40])
    return {'stem': (f'Read: A jeweller in Thrissur makes ornaments of {c}-carat gold. Pure gold is too soft. Brass and bronze vessels are also sold in the market, and the iron gate of the shop is galvanised.\n'
                     f'(i) What percentage of a {c}-carat ornament is gold? (ii) How much pure gold is there in a {m} g ornament? (iii) Name the metals in brass and bronze. (iv) Why does a galvanised gate not rust even when scratched?'),
            'answer': f'(i) {sig(c / 24 * 100, 3)}%. (ii) {sig(m * c / 24, 3)} g. (iii) Brass: copper and zinc; bronze: copper and tin. (iv) Zinc is more reactive and corrodes first, protecting iron.',
            'key': '1 mark each part.'}


c3_long = [
    ('Describe the steps involved in the extraction of a metal of medium reactivity, such as zinc, from its sulphide and carbonate ores. Write equations. How is the metal refined?',
     'Concentration of ore (removal of gangue). Roasting: 2ZnS + 3O₂ → 2ZnO + 2SO₂. Calcination: ZnCO₃ → ZnO + CO₂. Reduction with carbon: ZnO + C → Zn + CO. Electrolytic refining: impure metal anode, pure metal cathode, solution of its salt as electrolyte; pure metal deposits on the cathode, impurities form anode mud.',
     '1 mark concentration; 2 marks roasting/calcination; 1 mark reduction; 1 mark refining.'),
    ('Show the formation of NaCl and MgCl₂ by transfer of electrons. Write any four properties of ionic compounds with reasons.',
     'Na (2,8,1) → Na⁺ + e⁻; Cl (2,8,7) + e⁻ → Cl⁻; Na⁺Cl⁻. Mg (2,8,2) → Mg²⁺ + 2e⁻; 2Cl + 2e⁻ → 2Cl⁻; MgCl₂. Properties: hard solids (strong attraction), high melting and boiling points, soluble in water but not in kerosene, conduct electricity in molten state or solution (free ions).',
     '2 marks formation; 3 marks properties.'),
    ('What is corrosion? Describe an experiment to show that both air and water are needed for rusting. Give three methods to prevent rusting.',
     'Corrosion is the eating away of metals by air, moisture and chemicals. Three test tubes with iron nails: (A) tap water – rusts; (B) boiled water with oil layer – no rust (no air); (C) dry air with anhydrous CaCl₂ – no rust (no moisture). Prevention: painting, oiling/greasing, galvanising, chrome plating, anodising, making alloys.',
     '1 mark definition; 2 marks experiment; 2 marks methods.'),
    ('How do metals react with (a) oxygen (b) water (c) dilute acids (d) solutions of other metal salts? Give one equation each.',
     '(a) 2Mg + O₂ → 2MgO (basic oxide). (b) 2Na + 2H₂O → 2NaOH + H₂ (Fe, Zn, Al react only with steam). (c) Zn + 2HCl → ZnCl₂ + H₂ (metals below H do not react). (d) Fe + CuSO₄ → FeSO₄ + Cu (more reactive displaces less reactive).',
     '1 mark each; 1 mark overall reactivity link.'),
]

# ======================= ch04 Carbon and its Compounds
PFX = ['meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct', 'non', 'dec']


def hc(n, kind):
    if kind == 'alkane':
        return f'C{n}H{2 * n + 2}', PFX[n - 1] + 'ane'
    if kind == 'alkene':
        return f'C{n}H{2 * n}', PFX[n - 1] + 'ene'
    return f'C{n}H{2 * n - 2}', PFX[n - 1] + 'yne'


def fmt_c(f):
    return sub(re.sub(r'C1H', 'CH', f))


c4s3_defs = [
    ('a homologous series', 'a series of compounds with the same functional group and similar chemical properties, in which successive members differ by a –CH₂– unit'),
    ('a functional group', 'an atom or group of atoms that decides the characteristic properties of an organic compound'),
    ('a hydrocarbon', 'a compound made of carbon and hydrogen only'),
    ('a heteroatom', 'an atom other than carbon and hydrogen, such as oxygen, nitrogen or a halogen, that replaces hydrogen in a hydrocarbon'),
    ('an alkane', 'a saturated hydrocarbon with only single bonds, general formula CₙH₂ₙ₊₂'),
    ('an alkene', 'an unsaturated hydrocarbon with a carbon–carbon double bond, general formula CₙH₂ₙ'),
    ('an alkyne', 'an unsaturated hydrocarbon with a carbon–carbon triple bond, general formula CₙH₂ₙ₋₂'),
]
FG = [('alcohol', '–OH', 'ol', 'propanol'), ('aldehyde', '–CHO', 'al', 'propanal'), ('ketone', '>C=O', 'one', 'propanone'),
      ('carboxylic acid', '–COOH', 'oic acid', 'propanoic acid'), ('haloalkane (chloro)', '–Cl', 'chloro- (prefix)', 'chloropropane'), ('haloalkane (bromo)', '–Br', 'bromo- (prefix)', 'bromopropane')]


def iupac(cls, n):
    p = PFX[n - 1]
    if cls == 'alcohol':
        f = 'CH3OH' if n == 1 else 'CH3' + 'CH2' * (n - 1) + 'OH'
        return f, p + 'anol'
    if cls == 'aldehyde':
        f = 'HCHO' if n == 1 else 'CH3' + 'CH2' * (n - 2) + 'CHO'
        return f, p + 'anal'
    if cls == 'ketone':
        f = 'CH3CO' + ('CH2' * (n - 3)) + 'CH3'
        return f, p + 'anone'
    if cls == 'acid':
        f = 'HCOOH' if n == 1 else 'CH3' + 'CH2' * (n - 2) + 'COOH'
        return f, p + 'anoic acid'
    if cls == 'chloro':
        f = 'CH3Cl' if n == 1 else 'CH3' + 'CH2' * (n - 2) + 'CH2Cl'
        return f, 'chloro' + p + 'ane'
    if cls == 'bromo':
        f = 'CH3Br' if n == 1 else 'CH3' + 'CH2' * (n - 2) + 'CH2Br'
        return f, 'bromo' + p + 'ane'


IUP = [(c, n) for c in ('alcohol', 'aldehyde', 'acid', 'chloro', 'bromo') for n in range(1, 5)] + [('ketone', 3), ('ketone', 4)]
for _c, _n in IUP:
    _f, _ = iupac(_c, _n)
    assert atoms(_f).get('C') == _n, (_c, _n, _f)


def c4s3_name(r):
    c, n = r.choice(IUP)
    f, nm = iupac(c, n)
    others = list({iupac(c2, n2)[1] for c2, n2 in IUP if iupac(c2, n2)[1] != nm and (n2 == n or c2 == c)})
    return {'stem': f'Write the IUPAC name of {sub(f)}.', 'answer': nm, 'key': f'{n} carbon atom{"s" if n > 1 else ""} (prefix {PFX[n - 1]}-) with the {c if c not in ("chloro", "bromo") else "halo"} group: {nm}.',
            'distractors': r.sample(sorted(others), 3)}


def c4s3_formula(r):
    c, n = r.choice(IUP)
    f, nm = iupac(c, n)
    return {'stem': f'Draw the structure (write the condensed formula) of {nm} and name its functional group.', 'answer': f'{sub(f)}; ' + {
        'alcohol': 'alcohol (–OH)', 'aldehyde': 'aldehyde (–CHO)', 'ketone': 'ketone (>C=O)', 'acid': 'carboxylic acid (–COOH)', 'chloro': 'halo group (–Cl)', 'bromo': 'halo group (–Br)'}[c],
        'key': '1 mark structure. 1 mark functional group.'}


def c4s3_hc(r):
    kind = r.choice(['alkane', 'alkene', 'alkyne'])
    n = r.randint(2, 8)
    f, nm = hc(n, kind)
    q = r.random() < 0.5
    if q:
        wrong = list({hc(n, k)[1] for k in ('alkane', 'alkene', 'alkyne') if k != kind and not (n == 1 and k != 'alkane')} | {hc(n + 1, kind)[1], hc(max(1 if kind == 'alkane' else 2, n - 1), kind)[1]} - {nm})
        return {'stem': f'Name the hydrocarbon {fmt_c(f)}.', 'answer': nm, 'key': f'{fmt_c(f)} fits Cₙ{"H₂ₙ₊₂" if kind == "alkane" else "H₂ₙ" if kind == "alkene" else "H₂ₙ₋₂"} with n = {n}: {nm} ({kind}).', 'distractors': r.sample(wrong, min(3, len(wrong)))}
    wrong = list({fmt_c(hc(n, k)[0]) for k in ('alkane', 'alkene', 'alkyne') if k != kind} | {fmt_c(hc(n + 1, kind)[0])} - {fmt_c(f)})
    return {'stem': f'What is the molecular formula of {nm}?', 'answer': fmt_c(f), 'key': f'{cap(kind)}, n = {n}: {fmt_c(f)}.', 'distractors': r.sample(wrong, 3)}


def c4s3_next(r):
    kind = r.choice(['alkane', 'alkene', 'alkyne'])
    n = r.randint(1 if kind == 'alkane' else 2, 6)
    f, nm = hc(n, kind)
    f2, nm2 = hc(n + 1, kind)
    m1, m2 = molar(f), molar(f2)
    return {'stem': f'Write the formula and name of the next higher homologue of {nm} ({fmt_c(f)}). By how much do their molecular masses differ?',
            'answer': f'{nm2} ({fmt_c(f2)}); {num(m2 - m1)} u', 'key': f'Add a –CH₂– unit: {fmt_c(f2)}. Masses {num(m1)} u and {num(m2)} u; difference 14 u.'}


c4s3_cats = {
    'an alcohol': ['methanol', 'ethanol', 'propanol', 'butanol'],
    'an aldehyde': ['methanal', 'ethanal', 'propanal', 'butanal'],
    'a ketone': ['propanone', 'butanone'],
    'a carboxylic acid': ['methanoic acid', 'ethanoic acid', 'propanoic acid'],
    'a haloalkane': ['chloromethane', 'bromoethane', 'chloropropane'],
}
c4s3_mc = [
    ('Successive members of a homologous series differ in molecular mass by:', '14 u', '12 u', '16 u', '2 u'),
    ('The general formula of alkynes is:', 'CₙH₂ₙ₋₂', 'CₙH₂ₙ₊₂', 'CₙH₂ₙ', 'CₙHₙ'),
    ('The functional group in ethanal is:', 'aldehyde (–CHO)', 'alcohol (–OH)', 'ketone (>C=O)', 'carboxylic acid (–COOH)'),
    ('Which property shows a gradation in a homologous series?', 'melting and boiling points', 'chemical properties', 'functional group', 'general formula'),
    ('CH₃COCH₃ is named:', 'propanone', 'propanal', 'propanol', 'ethanone'),
]
c4s3_why = [
    ('Why do members of a homologous series show similar chemical properties?', 'Chemical properties are decided by the functional group, which is the same for all members.', '2 marks.'),
    ('Why do physical properties such as boiling point increase along a homologous series?', 'Molecular mass increases by 14 u for each –CH₂– unit added, so the forces between molecules increase.', '1 mark mass increases. 1 mark forces.'),
    ('Can CH₃OH and C₂H₅OH be called homologues? Give two reasons.', 'Yes; both have the –OH functional group and they differ by one –CH₂– unit (14 u).', '1 mark each reason.'),
]
c4s3_ar = [
    ('Methanol and ethanol belong to the same homologous series.', 'They have the same functional group and differ by a –CH₂– unit.', 'a', 'R explains A.'),
    ('Propanone and propanal have the same molecular formula C₃H₆O.', 'They have different functional groups.', 'b', 'Both are true; R does not explain why the formulae are equal.'),
    ('The boiling points of members of a homologous series are equal.', 'They have the same functional group.', 'd', 'A is false (boiling points increase); R is true.'),
]

c4s1_defs = [
    ('a covalent bond', 'a bond formed by the sharing of a pair of electrons between two atoms'),
    ('a single bond', 'a covalent bond formed by sharing one pair of electrons'),
    ('a double bond', 'a covalent bond formed by sharing two pairs of electrons'),
    ('a triple bond', 'a covalent bond formed by sharing three pairs of electrons'),
    ('an electron-dot structure', 'a diagram showing the valence electrons of atoms as dots or crosses, with shared pairs between them'),
]
COV = [('hydrogen', 'H₂', 1, 0, 0, 2), ('chlorine', 'Cl₂', 1, 0, 0, 2), ('oxygen', 'O₂', 0, 1, 0, 4), ('nitrogen', 'N₂', 0, 0, 1, 6),
       ('methane', 'CH₄', 4, 0, 0, 8), ('water', 'H₂O', 2, 0, 0, 4), ('ammonia', 'NH₃', 3, 0, 0, 6), ('carbon dioxide', 'CO₂', 0, 2, 0, 8),
       ('ethane', 'C₂H₆', 7, 0, 0, 14), ('ethene', 'C₂H₄', 4, 1, 0, 12), ('ethyne', 'C₂H₂', 2, 0, 1, 10), ('propane', 'C₃H₈', 10, 0, 0, 20),
       ('hydrogen chloride', 'HCl', 1, 0, 0, 2), ('cyclohexane', 'C₆H₁₂', 18, 0, 0, 36)]
for _n, _f, s1, d2, t3, e in COV:
    assert e == 2 * s1 + 4 * d2 + 6 * t3


def c4s1_bonds(r):
    n, f, s1, d2, t3, e = r.choice(COV)
    tot = s1 + d2 + t3
    parts = [f'{k} {w}' for k, w in ((s1, 'single'), (d2, 'double'), (t3, 'triple')) if k]
    return {'stem': f'How many covalent bonds are present in a molecule of {n} ({f}), and how many electrons are shared in all?',
            'answer': f'{tot} bond{"s" if tot > 1 else ""} ({", ".join(parts)}); {e} shared electrons',
            'key': f'Single = 2 electrons, double = 4, triple = 6: {", ".join(parts)} = {e} electrons.'}


def c4s1_bondq(r):
    n, f, s1, d2, t3, e = r.choice([c for c in COV if sum(1 for k in c[2:5] if k) == 1])
    k = 'triple' if t3 else ('double' if d2 else 'single')
    return {'stem': f'What type of covalent bond(s) does a molecule of {n} ({f}) contain?', 'answer': f'{k} bond' + ('s only' if (s1 + d2 + t3) > 1 else ''),
            'key': f'{cap(n)}: {s1 + d2 + t3} {k} bond{"s" if (s1 + d2 + t3) > 1 else ""}.', 'distractors': [f'{x} bond' + ('s only' if (s1 + d2 + t3) > 1 else '') for x in ('single', 'double', 'triple', 'ionic') if x != k]}


c4s1_mc = [
    ('Carbon forms covalent bonds because:', 'it cannot easily gain or lose four electrons', 'it is a metal', 'it has one valence electron', 'it is very reactive'),
    ('Covalent compounds are generally:', 'poor conductors of electricity with low melting points', 'good conductors', 'ionic', 'high melting solids always'),
    ('The number of valence electrons in a carbon atom is:', '4', '2', '6', '8'),
    ('In the nitrogen molecule, the atoms are joined by:', 'a triple bond', 'a single bond', 'a double bond', 'an ionic bond'),
    ('Diamond and graphite are:', 'allotropes of carbon', 'isomers', 'isotopes', 'compounds of carbon'),
    ('Fullerene C₆₀ is shaped like a:', 'football', 'sheet', 'chain', 'tetrahedron'),
]
c4s1_why = [
    ('Why does carbon neither form C⁴⁺ nor C⁴⁻ ions?', 'Losing four electrons needs a lot of energy, and gaining four is hard because six protons cannot hold ten electrons; so carbon shares electrons.', '1 mark each.'),
    ('Why are covalent compounds poor conductors of electricity?', 'They are made of molecules and do not form ions.', '2 marks.'),
    ('Why is diamond hard but graphite soft and slippery?', 'In diamond each carbon is bonded to four others in a rigid 3-D network; in graphite each carbon is bonded to three others in layers that slide over each other.', '1 mark each.'),
]
c4s1_ar = [
    ('Graphite conducts electricity.', 'Each carbon in graphite is bonded to three others, leaving free electrons.', 'a', 'R explains A.'),
    ('Covalent compounds have low melting points.', 'The forces between their molecules are weak.', 'a', 'R explains A.'),
    ('Carbon forms ionic compounds easily.', 'Carbon has four valence electrons.', 'd', 'A is false (it forms covalent compounds); R is true.'),
]

c4s2_defs = [
    ('catenation', 'the unique ability of carbon to form bonds with other carbon atoms, giving long chains, branches and rings'),
    ('tetravalency', 'the property of carbon of having a valency of four'),
    ('a saturated compound', 'a carbon compound in which carbon atoms are joined only by single bonds'),
    ('an unsaturated compound', 'a carbon compound containing a double or triple bond between carbon atoms'),
    ('structural isomers', 'compounds with the same molecular formula but different structures'),
]
c4s2_cats = {
    'a saturated hydrocarbon': ['methane', 'ethane', 'propane', 'butane', 'cyclohexane'],
    'an unsaturated hydrocarbon': ['ethene', 'ethyne', 'propene', 'butene', 'benzene'],
}
c4s2_mc = [
    ('Butane (C₄H₁₀) has how many structural isomers?', '2', '1', '3', '4'),
    ('The two isomers of butane differ in:', 'the arrangement of carbon atoms (straight chain and branched)', 'the number of carbon atoms', 'molecular formula', 'functional group'),
    ('The main reason for the large number of carbon compounds is:', 'catenation and tetravalency', 'its low melting point', 'its metallic nature', 'its ionic bonding'),
    ('Benzene, C₆H₆, has:', 'a ring with alternate single and double bonds', 'only single bonds', 'triple bonds', 'no carbon–carbon bonds'),
    ('Compounds of carbon are very stable because:', 'carbon is small and forms strong bonds', 'carbon is large', 'carbon is a metal', 'carbon has eight electrons'),
]
c4s2_why = [
    ('Why can carbon form a very large number of compounds?', 'Catenation (bonding with other carbon atoms in chains, branches and rings) and tetravalency (bonding with four other atoms including O, N, S, H, halogens).', '1 mark each.'),
    ('Why are carbon–carbon bonds very strong and stable?', 'Carbon is a small atom, so its nucleus holds the shared electron pairs strongly.', '2 marks.'),
    ('Give two differences between saturated and unsaturated hydrocarbons.', 'Saturated: only single bonds, burn with a clean blue flame. Unsaturated: double or triple bonds, burn with a yellow sooty flame and undergo addition reactions.', '1 mark each.'),
]
c4s2_ar = [
    ('Butane and isobutane are structural isomers.', 'They have the same molecular formula but different structures.', 'a', 'R explains A.'),
    ('Ethene is an unsaturated hydrocarbon.', 'It has a carbon–carbon double bond.', 'a', 'R explains A.'),
    ('Methane has structural isomers.', 'Methane has only one carbon atom.', 'd', 'A is false; R is true.'),
]


def c4s2_type(r):
    kind = r.choice(['alkane', 'alkene', 'alkyne'])
    n = r.randint(2, 8)
    f, nm = hc(n, kind)
    a = 'saturated' if kind == 'alkane' else 'unsaturated'
    bond = {'alkane': 'only single bonds', 'alkene': 'one C=C double bond', 'alkyne': 'one C≡C triple bond'}[kind]
    return {'stem': f'Assuming an open-chain hydrocarbon, is {fmt_c(f)} saturated or unsaturated? Which homologous series does it belong to?', 'answer': f'{cap(a)}; {kind}s ({bond}).',
            'key': f'{fmt_c(f)} fits the general formula of {kind}s: {a}.'}


def c4s4_comb(r):
    kind = r.choice(['alkane', 'alkene', 'alcohol'])
    n = r.randint(1 if kind != 'alkene' else 2, 5)
    if kind == 'alcohol':
        f = f'C{n}H{2 * n + 1}OH'
        nm = PFX[n - 1] + 'anol'
    else:
        f, nm = hc(n, kind)
    f = f.replace('C1H', 'CH')
    a = atoms(f)
    c, h, o = a['C'], a['H'], a.get('O', 0)
    o2 = (2 * c + h / 2 - o) / 2
    k = 1
    while abs(o2 * k - round(o2 * k)) > 1e-9:
        k *= 2
    L = [(k, f), (int(round(o2 * k)), 'O2')]
    R = [(c * k, 'CO2'), (h * k // 2, 'H2O')]
    assert side(L) == side(R)
    return {'stem': f'Write the balanced equation for the complete combustion of {nm} ({sub(f)}).',
            'answer': eqn(L, R), 'key': f'{eqn(L, R)} (+ heat and light). 1 mark formulae, 1 mark balancing.'}


c4s4_defs = [
    ('combustion', 'the burning of a carbon compound in oxygen to give carbon dioxide, water, heat and light'),
    ('an addition reaction', 'a reaction in which an unsaturated compound adds atoms across its double or triple bond'),
    ('hydrogenation', 'the addition of hydrogen to an unsaturated compound in the presence of a catalyst such as nickel'),
    ('a substitution reaction', 'a reaction in which an atom or group in a compound is replaced by another atom or group'),
    ('an oxidising agent', 'a substance that can add oxygen to others, such as alkaline potassium permanganate'),
    ('a catalyst', 'a substance that changes the rate of a reaction without itself being used up'),
]
c4s4_cats = {
    'an addition reaction': ['ethene + hydrogen with nickel catalyst → ethane', 'hydrogenation of vegetable oil to make vanaspati ghee'],
    'a substitution reaction': ['methane + chlorine in sunlight → chloromethane + HCl'],
    'an oxidation reaction': ['ethanol + alkaline KMnO₄ on heating → ethanoic acid', 'ethanol + acidified K₂Cr₂O₇ → ethanoic acid'],
    'a combustion reaction': ['burning of LPG in a stove', 'burning of methane: CH₄ + 2O₂ → CO₂ + 2H₂O', 'burning of kerosene in a lamp'],
}
c4s4_mc = [
    ('Unsaturated hydrocarbons burn with:', 'a yellow sooty flame', 'a clean blue flame', 'no flame', 'a green flame'),
    ('Vegetable oils are converted into vanaspati ghee by:', 'hydrogenation using a nickel catalyst', 'oxidation', 'substitution', 'combustion'),
    ('Which reagent converts ethanol to ethanoic acid?', 'alkaline potassium permanganate', 'sodium', 'conc. sulphuric acid at 443 K', 'hydrogen and nickel'),
    ('The reaction of methane with chlorine in sunlight is:', 'a substitution reaction', 'an addition reaction', 'a combustion reaction', 'a neutralisation'),
    ('When the air holes of a gas burner are closed, the flame becomes yellow and sooty because:', 'the fuel burns incompletely in limited oxygen', 'it gets more oxygen', 'the fuel changes', 'it becomes hotter'),
    ('Animal fats are generally:', 'saturated and considered less healthy', 'unsaturated', 'gases', 'alkynes'),
]
c4s4_why = [
    ('Why are vegetable oils considered healthier than animal fats?', 'Vegetable oils are unsaturated, while animal fats are mostly saturated and are linked to heart problems.', '1 mark each.'),
    ('Why does the bottom of a cooking vessel get blackened when the gas burner flame is yellow?', 'The air holes are blocked, so the fuel burns incompletely and unburnt carbon (soot) deposits on the vessel.', '1 mark incomplete combustion. 1 mark soot.'),
    ('How can you distinguish between ethane and ethene chemically?', 'Ethene decolourises bromine water (addition across the double bond); ethane does not. Ethene also burns with a sooty flame.', '1 mark test. 1 mark reason.'),
]
c4s4_ar = [
    ('Ethene undergoes addition reactions.', 'Ethene has a carbon–carbon double bond.', 'a', 'R explains A.'),
    ('Saturated hydrocarbons undergo substitution reactions.', 'They have only single bonds.', 'a', 'R explains A.'),
    ('Hydrogenation of oils is a substitution reaction.', 'Nickel acts as a catalyst.', 'd', 'A is false (it is an addition reaction); R is true.'),
]

c4s5_defs = [
    ('esterification', 'the reaction of a carboxylic acid with an alcohol in the presence of an acid catalyst to form an ester'),
    ('saponification', 'the alkaline hydrolysis of an ester (or fat) with NaOH to give soap and alcohol'),
    ('a micelle', 'a cluster of soap molecules in water with the hydrocarbon tails inside and ionic heads outside'),
    ('glacial acetic acid', 'pure ethanoic acid, which freezes in cold weather'),
    ('denatured alcohol', 'ethanol made unfit for drinking by adding poisonous methanol and a blue dye'),
    ('a detergent', 'an ammonium or sulphonate salt of a long-chain carboxylic acid that cleans well even in hard water'),
    ('scum', 'the insoluble substance formed when soap reacts with calcium and magnesium salts in hard water'),
]
c4s5_cats = {
    'a property of ethanol': ['a liquid that is used in medicines like tincture iodine', 'reacts with sodium to give hydrogen', 'gives ethene with hot concentrated sulphuric acid', 'neutral to litmus'],
    'a property of ethanoic acid': ['turns blue litmus red', 'reacts with sodium carbonate to give carbon dioxide', '5–8% solution in water is vinegar', 'freezes at 290 K'],
}
c4s5_mc = [
    ('Esters have a:', 'sweet (fruity) smell', 'pungent smell', 'rotten egg smell', 'no smell'),
    ('Ethanol reacts with sodium to give:', 'sodium ethoxide and hydrogen', 'sodium acetate and water', 'ethene', 'carbon dioxide'),
    ('Heating ethanol at 443 K with excess conc. H₂SO₄ gives:', 'ethene', 'ethanoic acid', 'ethyl ethanoate', 'methane'),
    ('Soap does not lather well in hard water because:', 'it forms scum with calcium and magnesium ions', 'it dissolves too much', 'it becomes acidic', 'it evaporates'),
    ('In a micelle, the hydrocarbon tails of soap molecules point:', 'towards the centre (the oil drop)', 'outwards into the water', 'towards the surface of the vessel', 'randomly'),
    ('Ethanoic acid reacts with sodium hydrogencarbonate to give:', 'sodium acetate, water and carbon dioxide', 'ethanol', 'hydrogen', 'ethene'),
]
c4s5_why = [
    ('Explain the cleansing action of soap.', 'Soap molecules have an ionic end (hydrophilic) and a long hydrocarbon tail (hydrophobic); the tails attach to oil/dirt, forming micelles with ionic ends outside, which are washed away by water.', '1 mark structure. 1 mark micelle.'),
    ('Why are detergents better than soaps in hard water?', 'Detergents do not form insoluble scum with calcium and magnesium ions, so they lather even in hard water.', '2 marks.'),
    ('Why is ethanol mixed with methanol and a blue dye in industrial alcohol?', 'To make it poisonous and easy to recognise, so that it is not drunk (denatured alcohol).', '2 marks.'),
    ('How would you distinguish between ethanol and ethanoic acid using sodium hydrogencarbonate?', 'Ethanoic acid gives brisk effervescence of CO₂ (turns lime water milky); ethanol gives no reaction.', '1 mark test. 1 mark result.'),
]
c4s5_ar = [
    ('Ethanoic acid is called glacial acetic acid.', 'Pure ethanoic acid freezes at 290 K in cold climates.', 'a', 'R explains A.'),
    ('Soaps are not effective in hard water.', 'Soap forms scum with Ca²⁺ and Mg²⁺ ions.', 'a', 'R explains A.'),
    ('Esters are used in perfumes and flavouring agents.', 'Esters are sweet-smelling substances.', 'a', 'R explains A.'),
    ('Ethanol turns blue litmus red.', 'Ethanol is a carboxylic acid.', 'e', ''),
]
c4s5_ar[3] = ('Ethanol is used as a fuel additive (in petrol).', 'Ethanol burns in oxygen to give carbon dioxide, water and heat.', 'a', 'R explains A.')

c4_hots = [
    ('An organic compound A (C₂H₆O) reacts with sodium to give hydrogen, and on oxidation with alkaline KMnO₄ gives B (C₂H₄O₂), which gives CO₂ with NaHCO₃. A and B react with an acid catalyst to give a sweet-smelling C. Identify A, B and C and write the equation for the last reaction.', 'A: ethanol; B: ethanoic acid; C: ethyl ethanoate (ester). CH₃COOH + C₂H₅OH → CH₃COOC₂H₅ + H₂O (acid catalyst).', '1 mark A and B. 1 mark C. 1 mark equation.'),
    ('A hydrocarbon X (C₃H₆) decolourises bromine water and burns with a sooty flame. On hydrogenation it gives Y. Identify X and Y and give one reason for each property.', 'X: propene (unsaturated, C=C double bond causes addition with bromine and sooty flame). Y: propane (C₃H₈) formed by addition of H₂ in the presence of Ni.', '1 mark X. 1 mark Y. 1 mark reasons.'),
    ('Why does a mixture of ethyne and oxygen, rather than ethyne and air, give a hot enough flame for welding?', 'With pure oxygen, ethyne burns completely and releases more heat quickly; air has only about 21% oxygen, so combustion is incomplete and a sooty, cooler flame forms.', '1 mark complete combustion. 1 mark air has less O₂. 1 mark sooty flame.'),
    ('A student adds soap to water from a borewell in Gurugram and gets little lather but a lot of curdy precipitate. Explain and suggest two remedies.', 'The water is hard (Ca²⁺/Mg²⁺ salts); soap reacts to form insoluble scum. Use a detergent, or soften the water by boiling or adding washing soda.', '1 mark hard water. 1 mark scum. 1 mark remedies.'),
]


def c4_case(r):
    n = r.randint(2, 5)
    f, nm = hc(n, 'alkane')
    f2, nm2 = hc(n, 'alkene')
    return {'stem': (f'Read: A refinery in Mathura separates hydrocarbons. Sample P is {nm} and sample Q is {nm2}. Q decolourises bromine water; P does not.\n'
                     f'(i) Write the molecular formulae of P and Q. (ii) Which is saturated? (iii) Why does Q decolourise bromine water? (iv) What will be formed when Q is treated with hydrogen in the presence of nickel?'),
            'answer': f'(i) P: {fmt_c(f)}; Q: {fmt_c(f2)}. (ii) P ({nm}). (iii) It has a C=C double bond and undergoes an addition reaction. (iv) {nm} ({fmt_c(f)}).',
            'key': '1 mark each part.'}


c4_long = [
    ('What is a homologous series? Write its four characteristics. Write the names and structures of the first three members of the alkane and alcohol series.',
     'A series of compounds with the same functional group and similar properties in which successive members differ by –CH₂–. Same general formula; differ by 14 u; similar chemical properties; gradation in physical properties. Alkanes: methane CH₄, ethane CH₃CH₃, propane CH₃CH₂CH₃. Alcohols: methanol CH₃OH, ethanol CH₃CH₂OH, propanol CH₃CH₂CH₂OH.',
     '1 mark definition; 2 marks characteristics; 2 marks structures.'),
    ('Describe four chemical properties of carbon compounds with equations: combustion, oxidation, addition and substitution.',
     'Combustion: CH₄ + 2O₂ → CO₂ + 2H₂O + heat. Oxidation: CH₃CH₂OH + alkaline KMnO₄ (heat) → CH₃COOH. Addition: CH₂=CH₂ + H₂ (Ni) → CH₃CH₃ (hydrogenation of oils). Substitution: CH₄ + Cl₂ (sunlight) → CH₃Cl + HCl.',
     '1¼ marks each (rounded).'),
    ('Give the properties of ethanol and ethanoic acid with one equation each for (a) ethanol with sodium (b) dehydration of ethanol (c) esterification (d) ethanoic acid with NaOH (e) ethanoic acid with sodium carbonate.',
     '(a) 2CH₃CH₂OH + 2Na → 2CH₃CH₂ONa + H₂. (b) CH₃CH₂OH → (hot conc. H₂SO₄, 443 K) CH₂=CH₂ + H₂O. (c) CH₃COOH + CH₃CH₂OH → (acid) CH₃COOCH₂CH₃ + H₂O. (d) NaOH + CH₃COOH → CH₃COONa + H₂O. (e) 2CH₃COOH + Na₂CO₃ → 2CH₃COONa + H₂O + CO₂.',
     '1 mark each.'),
    ('What are soaps and detergents? Explain the formation of micelles and the cleansing action of soap with a diagram. Why do soaps not work well in hard water?',
     'Soaps: sodium or potassium salts of long-chain carboxylic acids; detergents: ammonium or sulphonate salts of long-chain acids. Soap molecule: ionic hydrophilic head, hydrocarbon hydrophobic tail; in water tails point inward into oil, heads outward, forming a micelle that is rinsed away. Hard water Ca²⁺/Mg²⁺ form insoluble scum with soap.',
     '1 mark definitions; 3 marks micelle and cleansing; 1 mark hard water.'),
]


FAMILIES = {
    S + '01-st1': [TERM(c1s1_defs), DEF(c1s1_defs), CLS(c1s1_obs, 'Which of these shows {} as evidence of a chemical reaction?', C='C2', D='D2', verb='shows'), MC(c1s1_mc, C='C1', D='D2'),
                   SA(c1s1_why), ARF(c1s1_ar), G('C3', 'D3', 'explain', c1s1_class), SORT(c1s1_obs, 'Group these by the main observation, {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)),
                   SA(c1_hots[2:3], C='C4', D='D4', type='multi_step')],
    S + '01-st2': [TERM(c1s2_defs), DEF(c1s2_defs), MC(c1s2_mc, C='C1', D='D2'), SA(c1s2_why), ARF(c1s2_ar), G('C2', 'D2', 'mcq', c1s2_coef), G('C3', 'D2', 'mcq', c1s2_count),
                   G('C3', 'D3', 'explain', c1s2_bal), G('C3', 'D2', 'numerical', c1s2_mass), G('C4', 'D4', 'multi_step', c1s2_bal), G('C4', 'D3', 'case', c1_case, gap='G7'),
                   LONG(c1_long[:1], C='C4', D='D4'), G('C2', 'D2', 'mcq', c1s2_mass)],
    S + '01-st3': [TERM(c1s3_defs), DEF(c1s3_defs), CLS(RTYPE, 'Which of these equations represents {}?', C='C2', D='D2', verb='represents'), MC(c1s3_mc, C='C1', D='D2'), SA(c1s3_why), ARF(c1s3_ar),
                   G('C3', 'D2', 'mcq', c1s3_type), G('C3', 'D3', 'explain', c1s3_typeX), SA(c1_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c1_long[1:2] + c1_long[3:], C='C4', D='D4'),
                   G('C4', 'D4', 'multi_step', c1s3_typeX)],
    S + '01-st4': [TERM(c1s4_defs), DEF(c1s4_defs), MC(c1s4_mc, C='C1', D='D2'), SA(c1s4_why), ARF(c1s4_ar), G('C3', 'D3', 'explain', c1s4_redox), G('C2', 'D2', 'mcq', c1s4_agent),
                   SA(c1_hots[:2], C='C4', D='D4', type='multi_step'), LONG(c1_long[2:3], C='C4', D='D4'), G('C4', 'D3', 'mcq', c1s4_agent)],
    S + '02-st1': [TERM(c2s1_defs), DEF(c2s1_defs), MC(c2s1_mc, C='C1', D='D2'), G('C2', 'D2', 'mcq', c2s1_ind_q), SA(c2s1_why), ARF(c2s1_ar), G('C3', 'D3', 'explain', c2s1_neut),
                   G('C3', 'D2', 'explain', c2s1_carb), G('C3', 'D2', 'explain', c2s1_metal), G('C3', 'D3', 'numerical', c2s1_vol), G('C2', 'D2', 'mcq', c2s1_salt), G('C4', 'D4', 'multi_step', c2s1_vol),
                   LONG(c2_long[3:], C='C4', D='D4')],
    S + '02-st2': [TERM(c2s2_defs), DEF(c2s2_defs), MC(c2s2_mc, C='C1', D='D2'), SA(c2s2_why), ARF(c2s2_ar), CLS(c2s2_cats, 'Which of the following is {}?', C='C2', D='D2'),
                   SORT(c2s2_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3', n=(2, 3)), SA(c2_hots[2:3], C='C4', D='D4', type='multi_step')],
    S + '02-st3': [TERM(c2s3_defs), DEF(c2s3_defs), MC(c2s3_mc, C='C1', D='D2'), CLS(c2s3_cats, 'Which of the following is {}?', C='C2', D='D2'), G('C2', 'D1', 'mcq', c2s3_nature), G('C1', 'D2', 'mcq', c2s3_nat),
                   SA(c2s3_why), ARF(c2s3_ar), G('C3', 'D3', 'explain', c2s3_order), G('C4', 'D3', 'case', c2_case, gap='G7'), SA(c2_hots[3:], C='C4', D='D4', type='multi_step'),
                   LONG(c2_long[2:3], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c2s3_order)],
    S + '02-st4': [TERM(c2s4_defs), DEF(c2s4_defs), CLS(c2s4_use, 'Which of these is a use of {}?', C='C1', D='D2', verb='is a use of'), MC(c2s4_mc, C='C1', D='D2'), CLS(c2s4_cats, 'Which of the following is {}?', C='C2', D='D2'),
                   SA(c2s4_why), ARF(c2s4_ar), G('C3', 'D3', 'explain', c2s4_nature), G('C3', 'D3', 'numerical', c2s4_hyd), SA(c2_hots[:2], C='C4', D='D4', type='multi_step'),
                   LONG(c2_long[:2], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c2s4_hyd), G('C2', 'D3', 'mcq', c2s4_hyd)],
    S + '03-st1': [TERM(c3s1_defs), DEF(c3s1_defs), CLS(c3s1_cats, 'Which of these elements is {}?', C='C1', D='D1'), CLS(c3s1_exc, 'Which of these is {}?', C='C2', D='D2'), MC(c3s1_mc, C='C1', D='D2'),
                   SA(c3s1_why), ARF(c3s1_ar), SORT(c3s1_cats, 'Classify these elements as {A} or {B}: {L}.', C='C3', D='D2'), SA(c3_hots[2:3], C='C4', D='D4', type='multi_step')],
    S + '03-st2': [TERM(c3s2_defs), DEF(c3s2_defs), MC(c3s2_mc, C='C1', D='D2'), CLS(METAL_FACTS, 'Which metal {}?', C='C2', D='D2', verb='—'), SA(c3s2_why), ARF(c3s2_ar),
                   G('C3', 'D3', 'explain', c3s2_disp), G('C3', 'D2', 'mcq', c3s2_dispq), G('C3', 'D2', 'explain', c3s2_order), G('C2', 'D2', 'explain', c3s2_acid),
                   SA(c3_hots[1:2], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'case', c3_case, gap='G7'), LONG(c3_long[3:], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c3s2_disp)],
    S + '03-st3': [TERM(c3s3_defs), DEF(c3s3_defs), MC(c3s3_mc, C='C1', D='D2'), SA(c3s3_why), ARF(c3s3_ar), G('C3', 'D3', 'explain', c3s3_form), G('C2', 'D2', 'mcq', c3s3_formula),
                   G('C4', 'D4', 'multi_step', c3s3_form), LONG(c3_long[1:2], C='C4', D='D4')],
    S + '03-st4': [TERM(c3s4_defs), DEF(c3s4_defs), CLS(c3s4_cats, 'Which of these metals is {}?', C='C2', D='D2'), CLS(c3s4_ore, 'Which of these is {}?', C='C1', D='D2'), MC(c3s4_mc, C='C1', D='D2'),
                   SA(c3s4_why), ARF(c3s4_ar), SORT(c3s4_cats, 'Classify these metals by method of extraction, {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)), SA(c3_hots[3:] + c3_hots[:1], C='C4', D='D4', type='multi_step'),
                   LONG(c3_long[:1], C='C4', D='D4')],
    S + '03-st5': [TERM(c3s5_defs), DEF(c3s5_defs), CLS(c3s5_alloy, 'Which alloy is made of {}?', C='C1', D='D2', verb='is made of'), CLS(c3s5_prev, 'Which of these is usually protected from rusting by {}?', C='C2', D='D2', verb='is protected by'),
                   MC(c3s5_mc, C='C1', D='D2'), SA(c3s5_why), ARF(c3s5_ar), G('C3', 'D2', 'numerical', c3s5_carat), G('C4', 'D3', 'case', c3_case2, gap='G7'), LONG(c3_long[2:3], C='C4', D='D4'),
                   G('C2', 'D2', 'mcq', c3s5_carat)],
    S + '04-st1': [TERM(c4s1_defs), DEF(c4s1_defs), MC(c4s1_mc, C='C1', D='D2'), SA(c4s1_why), ARF(c4s1_ar), G('C3', 'D3', 'explain', c4s1_bonds), G('C2', 'D2', 'mcq', c4s1_bondq),
                   G('C4', 'D4', 'multi_step', c4s1_bonds), SA(c4_hots[2:3], C='C4', D='D4', type='multi_step')],
    S + '04-st2': [TERM(c4s2_defs), DEF(c4s2_defs), CLS(c4s2_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c4s2_mc, C='C1', D='D2'), SA(c4s2_why), ARF(c4s2_ar),
                   G('C3', 'D2', 'explain', c4s2_type), SORT(c4s2_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3'), G('C4', 'D3', 'case', c4_case, gap='G7'),
                   SA(c4_hots[1:2], C='C4', D='D4', type='multi_step')],
    S + '04-st3': [TERM(c4s3_defs), DEF(c4s3_defs), CLS(c4s3_cats, 'Which of these compounds is {}?', C='C1', D='D2'), MC(c4s3_mc, C='C1', D='D2'), SA(c4s3_why), ARF(c4s3_ar),
                   G('C2', 'D2', 'mcq', c4s3_name), G('C2', 'D2', 'mcq', c4s3_hc), G('C3', 'D3', 'explain', c4s3_formula), G('C3', 'D3', 'numerical', c4s3_next), G('C4', 'D4', 'multi_step', c4s3_next),
                   LONG(c4_long[:1], C='C4', D='D4'), SORT(c4s3_cats, 'Classify these compounds as {A} or {B}: {L}.', C='C3', D='D2', n=(1, 3))],
    S + '04-st4': [TERM(c4s4_defs), DEF(c4s4_defs), CLS(c4s4_cats, 'Which of these is {}?', C='C2', D='D2'), MC(c4s4_mc, C='C1', D='D2'), SA(c4s4_why), ARF(c4s4_ar),
                   G('C3', 'D3', 'explain', c4s4_comb), G('C4', 'D4', 'multi_step', c4s4_comb), LONG(c4_long[1:2], C='C4', D='D4')],
    S + '04-st5': [TERM(c4s5_defs), DEF(c4s5_defs), CLS(c4s5_cats, 'Which of these is {}?', C='C2', D='D2'), MC(c4s5_mc, C='C1', D='D2'), SA(c4s5_why), ARF(c4s5_ar),
                   SORT(c4s5_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(2, 2)), SA(c4_hots[:1] + c4_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c4_long[2:], C='C4', D='D4'),
                   CLS(c4s5_cats, 'Which of these is {}?', C='C3', D='D3', neg=True)],
}
