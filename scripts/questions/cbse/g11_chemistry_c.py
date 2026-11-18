"""CBSE class 11 chemistry families, units 7-9 (Redox, Organic basic principles, Hydrocarbons)."""
from __future__ import annotations

import math
from fractions import Fraction

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap

P = 'cbse-g11-chemistry'

# ---------------- ch07 st1 classical and electron-transfer views ----------------

REDOX_RX = [  # reaction, oxidised, reduced, oxidising agent, reducing agent
    ('Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)', 'Zn', 'Cu²⁺', 'Cu²⁺', 'Zn'),
    ('2Mg(s) + O₂(g) → 2MgO(s)', 'Mg', 'O₂', 'O₂', 'Mg'),
    ('CuO(s) + H₂(g) → Cu(s) + H₂O(l)', 'H₂', 'CuO', 'CuO', 'H₂'),
    ('Fe₂O₃(s) + 3CO(g) → 2Fe(s) + 3CO₂(g)', 'CO', 'Fe₂O₃', 'Fe₂O₃', 'CO'),
    ('2Na(s) + Cl₂(g) → 2NaCl(s)', 'Na', 'Cl₂', 'Cl₂', 'Na'),
    ('H₂S(g) + Cl₂(g) → 2HCl(g) + S(s)', 'H₂S', 'Cl₂', 'Cl₂', 'H₂S'),
    ('2FeCl₃(aq) + H₂S(g) → 2FeCl₂(aq) + 2HCl(aq) + S(s)', 'H₂S', 'FeCl₃', 'FeCl₃', 'H₂S'),
    ('Cl₂(g) + 2KI(aq) → 2KCl(aq) + I₂(s)', 'KI (I⁻)', 'Cl₂', 'Cl₂', 'KI (I⁻)'),
    ('2H₂S(g) + SO₂(g) → 3S(s) + 2H₂O(l)', 'H₂S', 'SO₂', 'SO₂', 'H₂S'),
    ('MnO₂(s) + 4HCl(aq) → MnCl₂(aq) + Cl₂(g) + 2H₂O(l)', 'HCl', 'MnO₂', 'MnO₂', 'HCl'),
    ('2Al(s) + Fe₂O₃(s) → Al₂O₃(s) + 2Fe(s)', 'Al', 'Fe₂O₃', 'Fe₂O₃', 'Al'),
    ('Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)', 'Cu', 'Ag⁺', 'Ag⁺', 'Cu')]


def ox_agent(r):
    rx, o, red, oa, ra = r.choice(REDOX_RX)
    return mcq(f'In the reaction {rx}, which species is the oxidising agent?', oa, [ra] + r.sample([x[3] for x in REDOX_RX if x[3] not in (oa, ra)] + [x[4] for x in REDOX_RX if x[4] not in (oa, ra)], 2),
                   f'{oa} gains electrons (is reduced), so it oxidises {ra}.', r)


def ox_agent_all(r):
    rx, o, red, oa, ra = r.choice(REDOX_RX)
    return {'stem': f'In the reaction {rx}, identify the species oxidised, the species reduced, the oxidising agent and the reducing agent.',
            'answer': f'Oxidised: {o}; reduced: {red}; oxidising agent: {oa}; reducing agent: {ra}',
            'key': f'½ mark each: {o} loses electrons/gains oxygen or loses hydrogen (oxidised, reducing agent); {red} is reduced and is the oxidising agent.'}


CH7S1 = {
    'topic': 'oxidation and reduction',
    'terms': [('oxidation', 'the loss of electrons by a species (classically, addition of oxygen or removal of hydrogen)'),
              ('reduction', 'the gain of electrons by a species (classically, removal of oxygen or addition of hydrogen)'),
              ('an oxidising agent', 'a reagent that accepts electrons and is itself reduced'),
              ('a reducing agent', 'a reagent that donates electrons and is itself oxidised'),
              ('a redox reaction', 'a reaction in which oxidation and reduction take place simultaneously'),
              ('a half reaction', 'the part of a redox reaction that shows only the oxidation or only the reduction with electrons')],
    'groups': [('an oxidation according to the classical concept', ['2Mg + O₂ → 2MgO', 'H₂S + Cl₂ → 2HCl + S (for H₂S)', 'CH₄ + 2O₂ → CO₂ + 2H₂O (for CH₄)', '2Na + H₂ → 2NaH (for Na)']),
               ('a reduction according to the classical concept', ['CuO + H₂ → Cu + H₂O (for CuO)', 'CH₂=CH₂ + H₂ → CH₃CH₃ (for ethene)', '2HgO → 2Hg + O₂ (for HgO)', 'Fe₂O₃ + 3CO → 2Fe + 3CO₂ (for Fe₂O₃)'])],
    'classify': False,
    'tf': (['Oxidation and reduction always occur together.', 'An oxidising agent is itself reduced in a reaction.',
            'In Zn + Cu²⁺ → Zn²⁺ + Cu, zinc is the reducing agent.', 'Loss of electrons is oxidation.', 'Removal of hydrogen from a substance is oxidation in the classical sense.'],
           [('A reducing agent gains electrons.', 'A reducing agent loses electrons and is itself oxidised.'),
            ('In 2Na + Cl₂ → 2NaCl, chlorine is oxidised.', 'Chlorine gains electrons and is reduced; sodium is oxidised.'),
            ('Addition of hydrogen to a substance is oxidation.', 'Addition of hydrogen is reduction.'),
            ('An oxidising agent loses electrons.', 'An oxidising agent gains (accepts) electrons.')]),
    'ar': [('When a zinc rod is dipped in copper sulphate solution, the blue colour fades.', 'Zinc reduces Cu²⁺ ions to copper metal and itself goes into solution as Zn²⁺.', 'a', 'Removal of blue Cu²⁺ from solution fades the colour.'),
           ('Copper metal displaces silver from silver nitrate solution.', 'Copper is a stronger reducing agent than silver.', 'a', 'Cu gives electrons to Ag⁺, so Ag is deposited.')],
    'fams': [F('C2', 'D2', 'mcq', ox_agent), F('C3', 'D2', 'explain', ox_agent_all)],
    'qa': [('C4', 'D4', 'explain', 'When a copper rod is placed in zinc sulphate solution, no reaction occurs; but a zinc rod in copper sulphate gets coated with copper. Explain the difference.',
            'Zinc has a greater tendency to lose electrons than copper (Zn is a stronger reducing agent), so Zn reduces Cu²⁺; Cu cannot reduce Zn²⁺.',
            '1 mark: relative tendency to lose electrons; 1 mark: direction of electron transfer.'),
           ('C4', 'D3', 'explain', 'H₂O₂ acts as an oxidising agent towards Fe²⁺ but as a reducing agent towards acidified KMnO₄. How is this possible?',
            'Oxygen in H₂O₂ is in the −1 state, between −2 and 0; it can be reduced to −2 (H₂O) by Fe²⁺ or oxidised to 0 (O₂) by the stronger oxidant MnO₄⁻.',
            '1 mark: intermediate oxidation state −1; 1 mark: direction depends on the partner.')],
}

# ---------------- ch07 st2 oxidation number ----------------

ONS = [  # display, target element, count of target, [(element, count, ON)], charge
    ('KMnO₄', 'Mn', 1, [('K', 1, 1), ('O', 4, -2)], 0), ('K₂Cr₂O₇', 'Cr', 2, [('K', 2, 1), ('O', 7, -2)], 0),
    ('H₂SO₄', 'S', 1, [('H', 2, 1), ('O', 4, -2)], 0), ('SO₃²⁻', 'S', 1, [('O', 3, -2)], -2), ('S₂O₃²⁻', 'S', 2, [('O', 3, -2)], -2),
    ('S₄O₆²⁻', 'S', 4, [('O', 6, -2)], -2), ('NH₃', 'N', 1, [('H', 3, 1)], 0), ('HNO₃', 'N', 1, [('H', 1, 1), ('O', 3, -2)], 0),
    ('NO₂', 'N', 1, [('O', 2, -2)], 0), ('N₂O', 'N', 2, [('O', 1, -2)], 0), ('N₂H₄', 'N', 2, [('H', 4, 1)], 0),
    ('HNO₂', 'N', 1, [('H', 1, 1), ('O', 2, -2)], 0), ('NH₄⁺', 'N', 1, [('H', 4, 1)], 1), ('NH₂OH', 'N', 1, [('H', 3, 1), ('O', 1, -2)], 0),
    ('H₂O₂', 'O', 2, [('H', 2, 1)], 0), ('OF₂', 'O', 1, [('F', 2, -1)], 0), ('Fe₃O₄', 'Fe', 3, [('O', 4, -2)], 0),
    ('H₃PO₄', 'P', 1, [('H', 3, 1), ('O', 4, -2)], 0), ('H₃PO₃', 'P', 1, [('H', 3, 1), ('O', 3, -2)], 0), ('H₃PO₂', 'P', 1, [('H', 3, 1), ('O', 2, -2)], 0),
    ('ClO₄⁻', 'Cl', 1, [('O', 4, -2)], -1), ('ClO₃⁻', 'Cl', 1, [('O', 3, -2)], -1), ('ClO⁻', 'Cl', 1, [('O', 1, -2)], -1),
    ('MnO₂', 'Mn', 1, [('O', 2, -2)], 0), ('MnO₄²⁻', 'Mn', 1, [('O', 4, -2)], -2), ('CH₄', 'C', 1, [('H', 4, 1)], 0),
    ('HCHO', 'C', 1, [('H', 2, 1), ('O', 1, -2)], 0), ('C₃O₂', 'C', 3, [('O', 2, -2)], 0), ('NaH', 'H', 1, [('Na', 1, 1)], 0),
    ('CaH₂', 'H', 2, [('Ca', 1, 2)], 0), ('KO₂', 'O', 2, [('K', 1, 1)], 0), ('Na₂O₂', 'O', 2, [('Na', 2, 1)], 0),
    ('OsO₄', 'Os', 1, [('O', 4, -2)], 0), ('V₂O₅', 'V', 2, [('O', 5, -2)], 0), ('CrO₄²⁻', 'Cr', 1, [('O', 4, -2)], -2),
    ('[Fe(CN)₆]⁴⁻', 'Fe', 1, [('CN', 6, -1)], -4), ('[Fe(CN)₆]³⁻', 'Fe', 1, [('CN', 6, -1)], -3), ('CO', 'C', 1, [('O', 1, -2)], 0),
    ('C₁₂H₂₂O₁₁', 'C', 12, [('H', 22, 1), ('O', 11, -2)], 0), ('Pb₃O₄', 'Pb', 3, [('O', 4, -2)], 0)]


def onstr(x):
    f = Fraction(x).limit_denominator(12)
    s = f'{f.numerator}/{f.denominator}' if f.denominator != 1 else str(f.numerator)
    if f > 0:
        s = '+' + s
    return s.replace('-', '−')


def ox_num(r):
    sp, el, n, others, q = r.choice(ONS)
    x = Fraction(q - sum(c * o for _, c, o in others), n)
    ans = onstr(x)
    wrong = [onstr(v) for v in dict.fromkeys([x + 1, x - 1, -x if x else Fraction(2), x + 2, Fraction(q - sum(c * o for _, c, o in others))]) if onstr(v) != ans][:3]
    eqn = ' + '.join(f'{c}({onstr(o)})' if c > 1 else f'({onstr(o)})' for _, c, o in others)
    return mcq(f'What is the oxidation number of {el} in {sp}?', ans, wrong,
               f'{n if n > 1 else ""}x + {eqn} = {q} ⇒ x = {ans}.' + (' (An average value; the atoms are not all equivalent.)' if Fraction(x).denominator != 1 else ''), r)


def ox_num_short(r):
    a, b = r.sample(ONS, 2)
    res = []
    for sp, el, n, others, q in (a, b):
        x = Fraction(q - sum(c * o for _, c, o in others), n)
        res.append((sp, el, onstr(x)))
    return {'stem': f'Calculate the oxidation number of {res[0][1]} in {res[0][0]} and of {res[1][1]} in {res[1][0]}.',
            'answer': f'{res[0][1]} in {res[0][0]}: {res[0][2]}; {res[1][1]} in {res[1][0]}: {res[1][2]}',
            'key': f'Sum of oxidation numbers equals the charge on the species; 1 mark each: {res[0][2]} and {res[1][2]}.'}


RX_TYPE = [('a combination reaction', ['C(s) + O₂(g) → CO₂(g)', '3Mg(s) + N₂(g) → Mg₃N₂(s)', 'CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)', 'H₂(g) + Cl₂(g) → 2HCl(g)']),
           ('a decomposition reaction', ['2H₂O(l) → 2H₂(g) + O₂(g)', '2NaH(s) → 2Na(s) + H₂(g)', '2KClO₃(s) → 2KCl(s) + 3O₂(g)', '2HgO(s) → 2Hg(l) + O₂(g)']),
           ('a metal displacement reaction', ['CuSO₄(aq) + Zn(s) → Cu(s) + ZnSO₄(aq)', 'V₂O₅(s) + 5Ca(s) → 2V(s) + 5CaO(s)', 'TiCl₄(l) + 2Mg(s) → Ti(s) + 2MgCl₂(s)', 'Cr₂O₃(s) + 2Al(s) → Al₂O₃(s) + 2Cr(s)']),
           ('a non-metal displacement reaction', ['2Na(s) + 2H₂O(l) → 2NaOH(aq) + H₂(g)', 'Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g)', 'Cl₂(g) + 2KBr(aq) → 2KCl(aq) + Br₂(l)', '2F₂(g) + 2H₂O(l) → 4HF(aq) + O₂(g)']),
           ('a disproportionation reaction', ['2H₂O₂(aq) → 2H₂O(l) + O₂(g)', 'P₄(s) + 3OH⁻(aq) + 3H₂O(l) → PH₃(g) + 3H₂PO₂⁻(aq)', 'Cl₂(g) + 2OH⁻(aq) → ClO⁻(aq) + Cl⁻(aq) + H₂O(l)', 'S₈(s) + 12OH⁻(aq) → 4S²⁻(aq) + 2S₂O₃²⁻(aq) + 6H₂O(l)'])]

CH7S2 = {
    'topic': 'oxidation number and types of redox reactions',
    'terms': [('oxidation number', 'the charge an atom would have in a compound if the electron pairs were counted with the more electronegative atom'),
              ('a disproportionation reaction', 'a redox reaction in which an element in one oxidation state is simultaneously oxidised and reduced'),
              ('a displacement reaction', 'a reaction in which an ion or atom in a compound is replaced by an ion or atom of another element'),
              ('a comproportionation reaction', 'a reaction in which an element in two different oxidation states forms a product with an intermediate oxidation state')],
    'groups': RX_TYPE,
    'classify': False,
    'tf': (['The oxidation number of an element in its free state is zero.', 'Fluorine always has an oxidation number of −1 in its compounds.',
            'In peroxides oxygen has an oxidation number of −1.', 'The sum of oxidation numbers in a polyatomic ion equals its charge.',
            'Hydrogen has an oxidation number of −1 in metal hydrides such as NaH.', 'An increase in oxidation number is oxidation.'],
           [('Oxygen always has an oxidation number of −2.', 'Oxygen is −1 in peroxides, −½ in superoxides and +2 in OF₂.'),
            ('The oxidation number of hydrogen is +1 in all its compounds.', 'In metal hydrides (NaH, CaH₂) hydrogen is −1.'),
            ('A decrease in oxidation number is oxidation.', 'A decrease in oxidation number is reduction.'),
            ('Fractional oxidation numbers are impossible.', 'Average oxidation numbers can be fractional, e.g. Fe in Fe₃O₄ is +8/3.'),
            ('In a disproportionation reaction two different elements are oxidised.', 'One element is both oxidised and reduced.')]),
    'ar': [('Fluorine does not show disproportionation.', 'Fluorine is the most electronegative element and cannot show a positive oxidation state.', 'a', 'Without positive states F cannot be oxidised and reduced at once.'),
           ('2H₂O₂ → 2H₂O + O₂ is a disproportionation reaction.', 'Oxygen changes from −1 to −2 and to 0.', 'a', 'The same element is reduced and oxidised.'),
           ('The oxidation number of S in S₄O₆²⁻ is +2.5.', 'All four sulphur atoms in S₄O₆²⁻ are in the same state.', 'c', '+2.5 is an average; the two bridging S atoms are 0 and the two terminal ones +5, so R is false.')],
    'fams': [F('C2', 'D2', 'mcq', ox_num), F('C3', 'D3', 'explain', ox_num_short)],
    'qa': [('C4', 'D4', 'explain', 'The average oxidation number of S in Na₂S₄O₆ is +2.5, but sulphur cannot really have a fractional oxidation state. Explain using its structure.',
            'In S₄O₆²⁻ the two central S atoms are bonded only to S (oxidation number 0) and the two terminal S atoms to three O each (+5). Average = (0 + 0 + 5 + 5)/4 = +2.5.',
            '1 mark: structure with two kinds of S; 1 mark: 0 and +5 give the average.'),
           ('C4', 'D5', 'long', '(a) Assign oxidation numbers to each element in the reaction P₄ + 3OH⁻ + 3H₂O → PH₃ + 3H₂PO₂⁻. (b) Identify the type of redox reaction. (c) Explain why ClO₄⁻ does not undergo disproportionation while ClO⁻ does.',
            '(a) P: 0 → −3 (PH₃) and +1 (H₂PO₂⁻); O −2; H +1. (b) Disproportionation. (c) In ClO₄⁻ chlorine is in its highest state (+7) and cannot be oxidised further; in ClO⁻ Cl (+1) can be oxidised and reduced.',
            '(a) 2 marks (b) 1 mark (c) 2 marks.')],
}

# ---------------- ch07 st3 balancing redox ----------------

BAL = [  # balanced equation, oxidant, reductant, ox:red mole ratio, e per oxidant, medium, H+ coeff (or OH-)
    ('MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 'MnO₄⁻', 'Fe²⁺', (1, 5), 5, 'acidic'),
    ('Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O', 'Cr₂O₇²⁻', 'Fe²⁺', (1, 6), 6, 'acidic'),
    ('Cr₂O₇²⁻ + 6I⁻ + 14H⁺ → 2Cr³⁺ + 3I₂ + 7H₂O', 'Cr₂O₇²⁻', 'I⁻', (1, 6), 6, 'acidic'),
    ('2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O', 'MnO₄⁻', 'C₂O₄²⁻', (2, 5), 5, 'acidic'),
    ('2MnO₄⁻ + 10I⁻ + 16H⁺ → 2Mn²⁺ + 5I₂ + 8H₂O', 'MnO₄⁻', 'I⁻', (1, 5), 5, 'acidic'),
    ('2MnO₄⁻ + I⁻ + H₂O → 2MnO₂ + IO₃⁻ + 2OH⁻', 'MnO₄⁻', 'I⁻', (2, 1), 3, 'basic'),
    ('2MnO₄⁻ + 5SO₂ + 2H₂O → 2Mn²⁺ + 5SO₄²⁻ + 4H⁺', 'MnO₄⁻', 'SO₂', (2, 5), 5, 'acidic'),
    ('2MnO₄⁻ + 5H₂O₂ + 6H⁺ → 2Mn²⁺ + 5O₂ + 8H₂O', 'MnO₄⁻', 'H₂O₂', (2, 5), 5, 'acidic'),
    ('Cr₂O₇²⁻ + 3SO₃²⁻ + 8H⁺ → 2Cr³⁺ + 3SO₄²⁻ + 4H₂O', 'Cr₂O₇²⁻', 'SO₃²⁻', (1, 3), 6, 'acidic'),
    ('3Cu + 2NO₃⁻ + 8H⁺ → 3Cu²⁺ + 2NO + 4H₂O', 'NO₃⁻', 'Cu', (2, 3), 3, 'acidic'),
    ('Cr₂O₇²⁻ + 3H₂S + 8H⁺ → 2Cr³⁺ + 3S + 7H₂O', 'Cr₂O₇²⁻', 'H₂S', (1, 3), 6, 'acidic'),
    ('2MnO₄⁻ + 3Br⁻ + H₂O → 2MnO₂ + BrO₃⁻ + 2OH⁻', 'MnO₄⁻', 'Br⁻', (2, 1), 3, 'basic')]


def bal_ratio(r):
    eq, ox, red, (a, b), e, med = r.choice(BAL)
    good = f'{a} : {b}'
    wrong = [w for w in dict.fromkeys([f'{b} : {a}', f'1 : 1', f'{a} : {b + 1}', f'{a + 1} : {b}', f'1 : {e}']) if w != good][:3]
    return mcq(f'When {ox} oxidises {red} in {med} medium, in what mole ratio do {ox} and {red} react?', good, wrong,
               f'Balanced equation: {eq}.', r)


def bal_electrons(r):
    eq, ox, red, (a, b), e, med = r.choice(BAL)
    prod = eq.split('→')[1].split('+')[0].strip()
    prod = ''.join(ch for ch in prod if not ch.isdigit() or prod.index(ch) > 0) if prod[0].isdigit() else prod
    return {'stem': f'How many electrons are gained by one {ox} ion (or molecule) when it acts as an oxidising agent in {med} medium in the reaction {eq}?',
            'answer': str(e), 'key': f'Change in oxidation number of the central atom × number of such atoms in {ox} = {e} electrons per {ox}.',
            'distractors': [str(x) for x in dict.fromkeys([e + 1, e - 1 if e > 1 else e + 2, 2 * e, 8]) if x != e][:3]}


def bal_full(r):
    eq, ox, red, (a, b), e, med = r.choice(BAL)
    left, right = eq.split(' → ')
    strip = lambda side: ' + '.join(t for t in (x.strip().lstrip('0123456789') for x in side.split(' + ')) if t not in ('H⁺', 'H₂O', 'OH⁻'))
    skel, skel_r = strip(left), strip(right)
    return {'stem': f'Balance the following redox reaction in {med} medium by the ion–electron (half-reaction) method: {skel} → {skel_r}',
            'answer': eq, 'key': f'Write oxidation and reduction half reactions; balance atoms other than O and H, then O with H₂O, H with H⁺{" (then add OH⁻ to both sides)" if med == "basic" else ""}, charge with electrons; multiply so electrons cancel ({ox} gains {e} e⁻ each). Result: {eq}. (3 marks: 1 each half reaction, 1 final)'}


def titration(r):
    eq, ox, red, (a, b), e, med = r.choice([x for x in BAL if x[2] in ('Fe²⁺', 'C₂O₄²⁻') and x[5] == 'acidic'])
    Mo = r.choice([0.01, 0.02, 0.05, 0.1])
    Vr = r.choice([10, 20, 25])
    Mr = r.choice([0.05, 0.1, 0.2])
    Vo = Mr * Vr / b * a / Mo
    oxn = 'KMnO₄' if 'Mn' in ox else 'K₂Cr₂O₇'
    rn = 'FeSO₄' if red == 'Fe²⁺' else 'oxalic acid'
    return {'stem': f'What volume of {Mo} M {oxn} is needed to oxidise {Vr} mL of {Mr} M {rn} in acidic medium? ({eq})',
            'answer': f'{num(Vo, 2)} mL', 'key': f'Moles of {red} = {Mr} × {Vr}/1000 = {num(Mr * Vr / 1000, 5)} (1); {ox} : {red} = {a} : {b} ⇒ moles of {ox} = {sci(Mr * Vr / 1000 * a / b, 3)} (1); V = {num(Vo, 2)} mL (1).',
            'distractors': [f'{num(Mr * Vr / Mo, 2)} mL', f'{num(Vo * b * b / a / a, 2)} mL', f'{num(Vo * 2, 2)} mL']}


CH7S3 = {
    'topic': 'balancing redox reactions',
    'terms': [('the oxidation number method', 'a method of balancing redox equations by equalising the total increase and decrease in oxidation numbers'),
              ('the half-reaction method', 'a method of balancing redox equations by balancing separate oxidation and reduction half reactions and adding them'),
              ('a redox titration', 'a titration in which the reaction between the titrant and analyte is an oxidation–reduction'),
              ('a self-indicator', 'a titrant such as KMnO₄ whose own colour change shows the end point')],
    'tf': (['KMnO₄ acts as a self-indicator in redox titrations.', 'In acidic medium MnO₄⁻ is reduced to Mn²⁺.', 'In neutral or weakly basic medium MnO₄⁻ is reduced to MnO₂.',
            'In basic medium, OH⁻ ions are used to balance the hydrogen atoms after H⁺ is neutralised.', 'In a balanced redox equation the electrons lost equal the electrons gained.'],
           [('In acidic medium MnO₄⁻ is reduced to MnO₂.', 'In acidic medium MnO₄⁻ is reduced to Mn²⁺ (gain of 5 e⁻).'),
            ('Cr₂O₇²⁻ gains three electrons when reduced to Cr³⁺.', 'Cr₂O₇²⁻ gains six electrons (two Cr atoms, +6 → +3).'),
            ('Diphenylamine is not needed in dichromate titrations because dichromate is a self-indicator.', 'Dichromate is not a self-indicator; an indicator such as diphenylamine is used.'),
            ('Charge need not be balanced in an ionic redox equation.', 'Both atoms and charges must balance.')]),
    'ar': [('KMnO₄ needs no external indicator in titrations.', 'The intense purple of MnO₄⁻ disappears as it is reduced; the first excess gives a permanent pink.', 'a', 'Its own colour marks the end point.'),
           ('In acidic medium one mole of MnO₄⁻ oxidises five moles of Fe²⁺.', 'Mn changes from +7 to +2, gaining five electrons, while each Fe²⁺ loses one.', 'a', 'Electron balance gives the 1 : 5 ratio.')],
    'fams': [F('C3', 'D2', 'mcq', bal_ratio), F('C2', 'D2', 'short', bal_electrons), F('C3', 'D4', 'multi_step', bal_full, kinds=('long5',)),
             F('C4', 'D4', 'multi_step', titration, kinds=('long5',))],
    'qa': [('C4', 'D3', 'explain', 'Why is KMnO₄ titration of Fe²⁺ carried out in dilute H₂SO₄ and not in HCl?',
            'HCl would be oxidised by MnO₄⁻ to Cl₂, consuming extra KMnO₄ and giving a wrong (high) titre; H₂SO₄ is not oxidised.',
            '1 mark: HCl is oxidised to Cl₂; 1 mark: error in titre.')],
}

# ---------------- ch07 st4 electrode processes ----------------

E0 = [('Li⁺/Li', -3.05, 'Li', 'Li⁺'), ('K⁺/K', -2.93, 'K', 'K⁺'), ('Ca²⁺/Ca', -2.87, 'Ca', 'Ca²⁺'), ('Na⁺/Na', -2.71, 'Na', 'Na⁺'), ('Mg²⁺/Mg', -2.36, 'Mg', 'Mg²⁺'),
      ('Al³⁺/Al', -1.66, 'Al', 'Al³⁺'), ('Zn²⁺/Zn', -0.76, 'Zn', 'Zn²⁺'), ('Fe²⁺/Fe', -0.44, 'Fe', 'Fe²⁺'), ('Ni²⁺/Ni', -0.25, 'Ni', 'Ni²⁺'),
      ('Sn²⁺/Sn', -0.14, 'Sn', 'Sn²⁺'), ('Pb²⁺/Pb', -0.13, 'Pb', 'Pb²⁺'), ('Cu²⁺/Cu', 0.34, 'Cu', 'Cu²⁺'), ('Ag⁺/Ag', 0.80, 'Ag', 'Ag⁺'),
      ('Au³⁺/Au', 1.40, 'Au', 'Au³⁺')]
E0_NM = [('I₂/I⁻', 0.54, 'I⁻', 'I₂'), ('Fe³⁺/Fe²⁺', 0.77, 'Fe²⁺', 'Fe³⁺'), ('Br₂/Br⁻', 1.09, 'Br⁻', 'Br₂'), ('Cl₂/Cl⁻', 1.36, 'Cl⁻', 'Cl₂'),
         ('MnO₄⁻/Mn²⁺', 1.51, 'Mn²⁺', 'MnO₄⁻'), ('F₂/F⁻', 2.87, 'F⁻', 'F₂'), ('Cr₂O₇²⁻/Cr³⁺', 1.33, 'Cr³⁺', 'Cr₂O₇²⁻')]


def ecell(r):
    a, b = r.sample(E0, 2)
    an, ca = (a, b) if a[1] < b[1] else (b, a)
    E = ca[1] - an[1]
    return {'stem': f'A galvanic cell is made from the {a[0]} and {b[0]} electrodes. E°({a[0]}) = {a[1]:+.2f} V and E°({b[0]}) = {b[1]:+.2f} V. Which electrode is the anode, and what is the standard emf of the cell?'.replace('+-', '−').replace('-', '−'),
            'answer': f'Anode: {an[0]}; E°cell = {E:.2f} V', 'key': f'The couple with the lower reduction potential ({an[0]}) is oxidised at the anode (1); E°cell = E°cathode − E°anode = {ca[1]:.2f} − ({an[1]:.2f}) = {E:.2f} V (1).'.replace('-', '−'),
            'distractors': [f'Anode: {ca[0]}; E°cell = {E:.2f} V', f'Anode: {an[0]}; E°cell = {abs(ca[1] + an[1]):.2f} V' if abs(ca[1] + an[1]) != E else f'Anode: {an[0]}; E°cell = {E + 0.5:.2f} V', f'Anode: {ca[0]}; E°cell = {-E:.2f} V'.replace('-', '−')]}


def strongest(r):
    pool = E0 + E0_NM
    k = r.sample(pool, 4)
    if r.random() < 0.5:
        best = max(k, key=lambda x: x[1])
        return mcq('Using the standard reduction potentials ' + ', '.join(f'E°({x[0]}) = {x[1]:+.2f} V' for x in k).replace('-', '−') + ', which is the strongest oxidising agent?',
                   best[3], [x[3] for x in k if x is not best], f'The highest reduction potential means the greatest tendency to gain electrons: {best[3]}.', r)
    best = min(k, key=lambda x: x[1])
    return mcq('Using the standard reduction potentials ' + ', '.join(f'E°({x[0]}) = {x[1]:+.2f} V' for x in k).replace('-', '−') + ', which is the strongest reducing agent?',
               best[2], [x[2] for x in k if x is not best], f'The lowest reduction potential means the greatest tendency to lose electrons: {best[2]}.', r)


def displace(r):
    a, b = r.sample(E0, 2)
    who = name(r)
    ok = a[1] < b[1]
    return {'stem': f'{who} dips a strip of {a[2]} into a solution containing {b[3]} ions. Will a reaction occur? Justify using E°({a[0]}) = {a[1]:+.2f} V and E°({b[0]}) = {b[1]:+.2f} V.'.replace('-', '−'),
            'answer': ('Yes; ' + f'{a[2]} reduces {b[3]} and {b[2]} is deposited') if ok else f'No; {a[2]} cannot reduce {b[3]}',
            'key': f'For {a[2]} + {b[3]} the cell emf = {b[1]:.2f} − ({a[1]:.2f}) = {b[1] - a[1]:.2f} V (1); {"positive, so the reaction is spontaneous" if ok else "negative, so no reaction"} (1).'.replace('-', '−'),
            'distractors': [f'No; {a[2]} cannot reduce {b[3]}' if ok else f'Yes; {a[2]} reduces {b[3]} and {b[2]} is deposited', 'Yes; hydrogen gas is evolved', 'It depends only on the concentration of the solution']}


CH7S4 = {
    'topic': 'redox reactions and electrode processes',
    'terms': [('an electrode potential', 'the potential difference that develops between an electrode and its electrolyte'),
              ('the standard hydrogen electrode', 'a platinum electrode coated with platinum black in 1 M H⁺ with H₂ gas at 1 bar, assigned zero potential'),
              ('a salt bridge', 'a U-tube containing an inert electrolyte such as KCl in agar that connects the two half-cells and keeps them electrically neutral'),
              ('the electrochemical series', 'the arrangement of electrodes in order of their standard reduction potentials'),
              ('a galvanic cell', 'a device that converts the chemical energy of a spontaneous redox reaction into electrical energy')],
    'tf': (['In a galvanic cell oxidation takes place at the anode.', 'The standard electrode potential of the SHE is taken as 0.00 V.',
            'A more negative E° means a stronger reducing agent.', 'In the Daniell cell zinc is the anode.', 'The salt bridge completes the inner circuit.'],
           [('In a galvanic cell the cathode is the negative electrode.', 'In a galvanic cell the cathode is positive; the anode (where oxidation occurs) is negative.'),
            ('Copper can displace zinc from zinc sulphate solution.', 'E°(Cu²⁺/Cu) > E°(Zn²⁺/Zn), so copper cannot reduce Zn²⁺.'),
            ('Fluorine is the strongest reducing agent in the electrochemical series.', 'F₂ has the highest E° and is the strongest oxidising agent.'),
            ('Electrons flow from cathode to anode in the external circuit.', 'Electrons flow from anode to cathode in the external circuit.')]),
    'orders': [('increasing order of reducing power', ['Ag', 'Cu', 'Pb', 'Fe', 'Zn', 'Al', 'Mg', 'Na', 'Li'], 'Reducing power rises as E° (M^n+/M) becomes more negative.', '<'),
               ('increasing order of oxidising power', ['I₂', 'Fe³⁺', 'Br₂', 'Cl₂', 'MnO₄⁻ (acidic)', 'F₂'], 'Oxidising power rises with E°: 0.54 < 0.77 < 1.09 < 1.36 < 1.51 < 2.87 V.', '<')],
    'ar': [('Zinc displaces copper from copper sulphate solution.', 'The standard reduction potential of Zn²⁺/Zn is lower than that of Cu²⁺/Cu.', 'a', 'Zn is the better reducing agent, so it reduces Cu²⁺.'),
           ('Lithium is the strongest reducing agent in aqueous solution.', 'Li⁺/Li has the most negative standard reduction potential.', 'a', 'E° = −3.05 V means the greatest tendency to lose electrons.')],
    'fams': [F('C3', 'D3', 'numerical', ecell), F('C3', 'D3', 'mcq', strongest), F('C4', 'D3', 'explain', displace)],
    'qa': [('C4', 'D4', 'explain', 'Can copper sulphate solution be stored in an iron vessel? Explain using E°(Cu²⁺/Cu) = +0.34 V and E°(Fe²⁺/Fe) = −0.44 V.',
            'No. Iron (lower E°) reduces Cu²⁺ to Cu and itself dissolves as Fe²⁺: Fe + Cu²⁺ → Fe²⁺ + Cu, E°cell = +0.78 V, so the vessel would corrode.',
            '1 mark: no, with spontaneous reaction; 1 mark: E°cell positive.')],
}

# ---------------- ch08 st1 tetravalence, representations, classification ----------------

FG = [('an alcohol', ['CH₃CH₂OH', 'CH₃CH(OH)CH₃', 'CH₃OH', '(CH₃)₃COH']), ('an aldehyde', ['CH₃CHO', 'HCHO', 'CH₃CH₂CHO', 'C₆H₅CHO']),
      ('a ketone', ['CH₃COCH₃', 'CH₃COCH₂CH₃', 'C₆H₅COCH₃']), ('a carboxylic acid', ['CH₃COOH', 'HCOOH', 'CH₃CH₂COOH', 'C₆H₅COOH']),
      ('an ester', ['CH₃COOCH₃', 'HCOOC₂H₅', 'CH₃COOC₂H₅']), ('an ether', ['CH₃OCH₃', 'C₂H₅OC₂H₅', 'CH₃OC₂H₅']),
      ('an amine', ['CH₃NH₂', '(CH₃)₂NH', 'C₆H₅NH₂', '(C₂H₅)₃N'])]

CH8S1 = {
    'topic': 'classification of organic compounds',
    'terms': [('tetravalence of carbon', 'the ability of carbon to form four covalent bonds'),
              ('a functional group', 'an atom or group of atoms joined in a specific manner that determines the characteristic chemical properties of a compound'),
              ('a homologous series', 'a series of organic compounds with the same functional group in which successive members differ by a –CH₂– unit'),
              ('a bond-line formula', 'a representation in which carbon and hydrogen atoms are not shown and lines represent C–C bonds drawn in zig-zag'),
              ('a heterocyclic compound', 'a cyclic compound in which one or more ring atoms is not carbon'),
              ('an alicyclic compound', 'a non-aromatic closed-chain compound such as cyclohexane')],
    'groups': FG,
    'groups2': [('an acyclic (open-chain) compound', ['isobutane', 'acetone', 'acetaldehyde', 'propene']), ('an alicyclic compound', ['cyclohexane', 'cyclopropane', 'cyclohexene', 'tetrahydrofuran (as a cyclic ether)']),
                ('a benzenoid aromatic compound', ['benzene', 'toluene', 'naphthalene', 'aniline']), ('a non-benzenoid or heterocyclic aromatic compound', ['pyridine', 'furan', 'thiophene', 'tropolone'])],
    'classify': False,
    'tf': (['Carbon forms four covalent bonds because it has four valence electrons.', 'Successive members of a homologous series differ by CH₂.',
            'In the bond-line formula of propane only two lines are drawn.', 'Pyridine is a heterocyclic aromatic compound.', 'Members of a homologous series show a gradation in physical properties.'],
           [('Members of a homologous series have different functional groups.', 'Members of a homologous series have the same functional group.'),
            ('Cyclohexane is an aromatic compound.', 'Cyclohexane is an alicyclic (non-aromatic) compound.'),
            ('Successive members of a homologous series differ by CH₃.', 'They differ by a –CH₂– unit (14 u).'),
            ('In carbon compounds the shape of a molecule does not depend on hybridisation.', 'Hybridisation of carbon decides the shape (sp³ tetrahedral, sp² planar, sp linear).')]),
    'ar': [('Carbon forms a very large number of compounds.', 'Carbon shows catenation and forms strong C–C bonds as well as multiple bonds.', 'a', 'Catenation and multiple bonding allow countless chains and rings.'),
           ('Furan is a heterocyclic compound.', 'Its ring contains an oxygen atom.', 'a', 'A ring atom other than carbon makes it heterocyclic.')],
    'qa': [('C4', 'D4', 'explain', 'Ethanol and dimethyl ether have the same molecular formula C₂H₆O. To which classes do they belong and how do their structures differ?',
            'Ethanol (CH₃CH₂OH) is an alcohol with an –OH group; dimethyl ether (CH₃OCH₃) is an ether with C–O–C. They are functional isomers.',
            '1 mark: classes; 1 mark: structural difference / functional isomerism.'),
           ('C4', 'D3', 'explain', 'Why is the molecular mass difference between successive members of a homologous series always 14 u?',
            'Successive members differ by one –CH₂– unit, whose mass is 12 + 2 × 1 = 14 u.', '1 mark: CH₂; 1 mark: 14 u.')],
}

# ---------------- ch08 st2 IUPAC nomenclature and isomerism ----------------

NAMES = [('CH₃CH(CH₃)CH₂CH₃', '2-methylbutane', ['3-methylbutane', 'pentane', '2-ethylpropane']),
         ('(CH₃)₂CHCH(CH₃)₂', '2,3-dimethylbutane', ['2,2-dimethylbutane', '1,2-dimethylbutane', 'hexane']),
         ('CH₃CH₂CH(CH₃)CH₂CH₃', '3-methylpentane', ['2-ethylbutane', '3-ethylbutane', '2-methylpentane']),
         ('(CH₃)₃CCH₂CH₃', '2,2-dimethylbutane', ['3,3-dimethylbutane', '2-ethyl-2-methylpropane', '2,3-dimethylbutane']),
         ('CH₃CH=CHCH₃', 'but-2-ene', ['but-1-ene', 'butane', 'but-3-ene']),
         ('CH₂=CHCH₂CH₃', 'but-1-ene', ['but-3-ene', 'but-2-ene', 'butyl-1-ene']),
         ('HC≡CCH₂CH₃', 'but-1-yne', ['but-3-yne', 'but-2-yne', 'butyne-4']),
         ('CH₃CH(OH)CH₃', 'propan-2-ol', ['propan-1-ol', 'isopropanol-2', 'propanone']),
         ('CH₃CH₂CHO', 'propanal', ['propanone', 'propan-1-al', 'propanol']),
         ('CH₃COCH₂CH₃', 'butan-2-one', ['butan-3-one', 'butanal', 'propan-2-one']),
         ('CH₃COOCH₂CH₃', 'ethyl ethanoate', ['ethyl propanoate', 'methyl propanoate', 'butanoic acid']),
         ('CH₃OCH₂CH₃', 'methoxyethane', ['ethoxymethane', 'propan-1-ol', 'methyl ethanol']),
         ('(CH₃)₃COH', '2-methylpropan-2-ol', ['butan-2-ol', '1,1-dimethylethanol', '2-methylpropan-1-ol']),
         ('CH₃CH(CH₃)CH₂OH', '2-methylpropan-1-ol', ['2-methylpropan-3-ol', 'butan-1-ol', '2-methylpropan-2-ol']),
         ('CH₂=CHCH₂OH', 'prop-2-en-1-ol', ['prop-1-en-3-ol', 'propan-1-ol', 'prop-2-ene-1-al']),
         ('HOCH₂CH₂OH', 'ethane-1,2-diol', ['ethane-1,1-diol', 'ethanol', 'ethane-diol-2']),
         ('CH₃CH₂CH₂CN', 'butanenitrile', ['propanenitrile', 'butanamide', '1-cyanopropane-2']),
         ('CH₃CH(CH₃)COOH', '2-methylpropanoic acid', ['3-methylpropanoic acid', 'butanoic acid', '2-methylbutanoic acid']),
         ('CH₃CH=CHCHO', 'but-2-enal', ['but-3-enal', 'butanal', 'but-2-en-1-one']),
         ('CH₂=CHCN', 'prop-2-enenitrile', ['prop-1-enenitrile', 'propanenitrile', 'ethenenitrile']),
         ('CH₃CH(Br)CH₂CH₃', '2-bromobutane', ['3-bromobutane', '1-bromobutane', '2-bromopropane']),
         ('CH₃CH(CH₃)CH(CH₃)CH₂CH₃', '2,3-dimethylpentane', ['3,4-dimethylpentane', '2-methyl-3-methylpentane', '2,3-dimethylbutane']),
         ('CH₃CH₂C(CH₃)₂CH₂CH₃', '3,3-dimethylpentane', ['2,2-diethylpropane', '3,3-dimethylbutane', '3-ethyl-3-methylbutane']),
         ('ClCH₂COOH', '2-chloroethanoic acid', ['1-chloroethanoic acid', 'chloromethanoic acid', '2-chloropropanoic acid']),
         ('CH₃CH₂CH₂NH₂', 'propan-1-amine', ['propan-3-amine', 'propylamide', 'propanamine-1']),
         ('CH₃COCH₂COCH₃', 'pentane-2,4-dione', ['pentane-2,3-dione', 'pentan-2,4-one', 'pentane-1,3-dione'])]


def iupac(r):
    f, n, wrong = r.choice(NAMES)
    if r.random() < 0.6:
        return mcq(f'What is the IUPAC name of {f}?', n, wrong, f'Select the longest chain containing the functional group/multiple bond, number to give lowest locants: {n}.', r)
    others = [x for x in NAMES if x[0] != f]
    w = [x[0] for x in r.sample(others, 3)]
    return mcq(f'Which condensed formula represents {n}?', f, w, f'{n} is {f}.', r)


ISOM = [('butane and 2-methylpropane', 'chain isomerism'), ('pentane and 2,2-dimethylpropane', 'chain isomerism'), ('pentane and 2-methylbutane', 'chain isomerism'),
        ('propan-1-ol and propan-2-ol', 'position isomerism'), ('but-1-ene and but-2-ene', 'position isomerism'), ('1-chlorobutane and 2-chlorobutane', 'position isomerism'),
        ('ethanol and methoxymethane', 'functional group isomerism'), ('propanal and propanone', 'functional group isomerism'), ('propanoic acid and methyl ethanoate', 'functional group isomerism'),
        ('methoxypropane and ethoxyethane', 'metamerism'), ('N-ethylethanamine and N-methylpropan-1-amine', 'metamerism'),
        ('cis-but-2-ene and trans-but-2-ene', 'geometrical isomerism')]
ISO_T = ['chain isomerism', 'position isomerism', 'functional group isomerism', 'metamerism', 'geometrical isomerism']


def isom(r):
    p, t = r.choice(ISOM)
    return mcq(f'What type of isomerism is shown by {p}?', t, r.sample([x for x in ISO_T if x != t], 3), f'{cap(p)}: {t}.', r)


ISO_COUNT = [('C₄H₁₀', 'structural isomers', 2, 'butane, 2-methylpropane'), ('C₅H₁₂', 'structural isomers', 3, 'pentane, 2-methylbutane, 2,2-dimethylpropane'),
             ('C₆H₁₄', 'structural isomers', 5, 'hexane, 2-methylpentane, 3-methylpentane, 2,2-dimethylbutane, 2,3-dimethylbutane'),
             ('C₃H₈O', 'structural isomers', 3, 'propan-1-ol, propan-2-ol, methoxyethane'),
             ('C₄H₁₀O', 'isomeric alcohols', 4, 'butan-1-ol, butan-2-ol, 2-methylpropan-1-ol, 2-methylpropan-2-ol'),
             ('C₄H₁₀O', 'isomeric ethers', 3, 'methoxypropane, 2-methoxypropane, ethoxyethane'),
             ('C₃H₇Cl', 'structural isomers', 2, '1-chloropropane, 2-chloropropane'), ('C₄H₉Br', 'structural isomers', 4, '1-bromobutane, 2-bromobutane, 1-bromo-2-methylpropane, 2-bromo-2-methylpropane')]


def iso_count(r):
    f, what, n, lst = r.choice(ISO_COUNT)
    return {'stem': f'How many {what} are possible for the molecular formula {f}? Name them.', 'answer': f'{n}: {lst}',
            'key': f'{n} isomers (1 mark); naming them: {lst} (1 mark).', 'distractors': [str(n + 1), str(n - 1), str(n + 2)]}


CH8S2 = {
    'topic': 'IUPAC nomenclature and isomerism',
    'terms': [('isomerism', 'the phenomenon of two or more compounds having the same molecular formula but different properties'),
              ('structural isomers', 'compounds with the same molecular formula but different structures'),
              ('stereoisomers', 'compounds with the same constitution and sequence of bonds but different arrangement of atoms in space'),
              ('metamerism', 'isomerism due to different alkyl chains on either side of the functional group'),
              ('the principal functional group', 'the functional group chosen as the suffix when a compound has more than one functional group'),
              ('the parent chain', 'the longest continuous carbon chain that contains the functional group or multiple bond')],
    'tf': (['In IUPAC naming the chain is numbered to give the lowest locants to the principal functional group.', 'Ethanol and dimethyl ether are functional isomers.',
            'Pentane has three chain isomers including itself.', '–COOH has higher priority than –OH in choosing the suffix.', 'The suffix for a ketone is “-one”.'],
           [('The IUPAC name of CH₃CH(CH₃)CH₂CH₃ is 3-methylbutane.', 'It is 2-methylbutane; the chain is numbered to give the lowest locant.'),
            ('The suffix for aldehydes is “-ol”.', 'The suffix for aldehydes is “-al”; “-ol” is for alcohols.'),
            ('Propanal and propanone are position isomers.', 'They are functional group isomers.'),
            ('Butane and 2-methylpropane are position isomers.', 'They are chain isomers.')]),
    'ar': [('Propan-1-ol and propan-2-ol are position isomers.', 'They differ only in the position of the –OH group on the same carbon chain.', 'a', 'Same chain and group, different position.'),
           ('The IUPAC name of CH₃COCH₂CH₃ is butan-2-one.', 'The C=O carbon must get the lowest possible locant.', 'a', 'Numbering from the left gives C=O at C2.')],
    'fams': [F('C2', 'D2', 'mcq', iupac), F('C3', 'D3', 'mcq', isom), F('C3', 'D4', 'explain', iso_count)],
    'qa': [('C4', 'D4', 'explain', 'A student named CH₃CH₂CH(CH₃)CH₂CH₂CH₃ as 4-methylhexane. Identify the error and give the correct name.',
            'The chain was numbered from the wrong end; numbering must give the substituent the lowest locant: 3-methylhexane.',
            '1 mark: lowest-locant rule; 1 mark: 3-methylhexane.'),
           ('C4', 'D5', 'long', 'For the molecular formula C₄H₈O: (a) draw (write) an aldehyde and a ketone and name them; (b) name the type of isomerism between them; (c) write one more aldehyde isomer and state its relation to the first; (d) give one chemical test to distinguish the aldehyde from the ketone.',
            '(a) Butanal CH₃CH₂CH₂CHO; butan-2-one CH₃COCH₂CH₃. (b) Functional group isomerism. (c) 2-methylpropanal (CH₃)₂CHCHO – chain isomer of butanal. (d) Tollens\' reagent gives a silver mirror with the aldehyde, not the ketone.',
            '(a) 2 marks (b) 1 mark (c) 1 mark (d) 1 mark.')],
}

# ---------------- ch08 st3 electronic displacements and intermediates ----------------

ALPHA_H = [('CH₃CH₂⁺ (ethyl carbocation)', 3), ('(CH₃)₂CH⁺ (isopropyl carbocation)', 6), ('(CH₃)₃C⁺ (tert-butyl carbocation)', 9),
           ('CH₃⁺ (methyl carbocation)', 0), ('CH₃CH₂CH₂⁺ (n-propyl carbocation)', 2), ('(CH₃)₂C⁺CH₂CH₃ (tert-pentyl carbocation)', 8),
           ('CH₃CH=CH₂ (propene, α-H to the double bond)', 3), ('(CH₃)₂C=CH₂ (2-methylpropene)', 6), ('CH₃CH=CHCH₃ (but-2-ene)', 6)]


def alpha_h(r):
    s, n = r.choice(ALPHA_H)
    return {'stem': f'How many α-hydrogen atoms (hyperconjugable C–H bonds) are present in {s}?', 'answer': str(n),
            'key': f'Count C–H bonds on carbon atoms directly attached to the positive carbon / sp² carbon: {n}. More α-H means more hyperconjugative stabilisation.',
            'distractors': [str(x) for x in dict.fromkeys([n + 1, n + 3, abs(n - 3), n + 2]) if x != n][:3]}


CH8S3 = {
    'topic': 'electronic displacements in covalent bonds',
    'terms': [('the inductive effect', 'the permanent displacement of σ-electrons along a carbon chain due to an electronegative or electropositive atom'),
              ('the resonance (mesomeric) effect', 'the polarity produced in a molecule by the interaction of two π bonds or of a π bond and a lone pair on an adjacent atom'),
              ('the electromeric effect', 'a temporary, complete transfer of a shared pair of π-electrons to one atom in the presence of an attacking reagent'),
              ('hyperconjugation', 'the delocalisation of σ-electrons of a C–H bond of an alkyl group attached to an unsaturated atom or a carbocation'),
              ('a carbocation', 'a species with a carbon atom bearing a positive charge and six electrons in its valence shell'),
              ('a carbanion', 'a species with a carbon atom bearing a negative charge and an unshared pair of electrons'),
              ('an electrophile', 'a reagent that takes away an electron pair, i.e. an electron-seeking species'),
              ('a nucleophile', 'a reagent that brings an electron pair, i.e. a nucleus-seeking species')],
    'groups': [('an electrophile', ['NO₂⁺', 'CH₃CO⁺', 'BF₃', 'AlCl₃', 'R₃C⁺']), ('a nucleophile', ['OH⁻', 'CN⁻', 'NH₃', 'RO⁻', 'H₂O'])],
    'groups2': [('a group showing +R (electron-releasing resonance) effect', ['–OH', '–OR', '–NH₂', '–NHCOCH₃', '–Cl']),
                ('a group showing −R (electron-withdrawing resonance) effect', ['–NO₂', '–CHO', '–COOH', '–CN', '–COCH₃'])],
    'orders': [('increasing order of stability of carbocations', ['CH₃⁺', 'CH₃CH₂⁺', '(CH₃)₂CH⁺', '(CH₃)₃C⁺'], 'More alkyl groups give more +I and hyperconjugation (0, 3, 6, 9 α-H).', '<'),
               ('increasing order of acid strength', ['CH₃COOH', 'ClCH₂COOH', 'Cl₂CHCOOH', 'Cl₃CCOOH'], 'Each Cl adds −I effect, stabilising the carboxylate ion.', '<'),
               ('increasing order of acid strength', ['ICH₂COOH', 'BrCH₂COOH', 'ClCH₂COOH', 'FCH₂COOH'], 'The −I effect increases with electronegativity: I < Br < Cl < F.', '<'),
               ('increasing order of stability of carbanions', ['(CH₃)₃C⁻', '(CH₃)₂CH⁻', 'CH₃CH₂⁻', 'CH₃⁻'], 'Alkyl groups (+I) intensify the negative charge, so methyl carbanion is most stable.', '<'),
               ('increasing order of stability of free radicals', ['CH₃•', 'CH₃CH₂•', '(CH₃)₂CH•', '(CH₃)₃C•'], 'Hyperconjugation and +I effect stabilise radicals: 3° > 2° > 1° > methyl.', '<')],
    'tf': (['The inductive effect is a permanent effect.', 'The electromeric effect is temporary and operates only in the presence of a reagent.',
            'Tertiary carbocations are more stable than primary ones.', 'In a carbocation the positive carbon is sp² hybridised.', 'Hyperconjugation is also called no-bond resonance.'],
           [('The inductive effect involves π-electrons.', 'The inductive effect involves σ-electrons; resonance involves π-electrons.'),
            ('Primary carbocations are more stable than tertiary ones.', 'Tertiary carbocations are most stable due to +I and hyperconjugation.'),
            ('The electromeric effect is a permanent effect.', 'It is temporary and disappears when the reagent is removed.'),
            ('Carbanions are electron-deficient species.', 'Carbanions carry an extra lone pair; carbocations are electron deficient.'),
            ('The inductive effect increases with distance from the substituent.', 'It decreases rapidly with distance and is negligible beyond three bonds.')]),
    'ar': [('Trichloroacetic acid is a stronger acid than acetic acid.', 'Chlorine atoms withdraw electrons by the −I effect and stabilise the anion.', 'a', 'A stabilised conjugate base means a stronger acid.'),
           ('(CH₃)₃C⁺ is more stable than CH₃CH₂⁺.', 'The tert-butyl cation has nine α-hydrogens for hyperconjugation.', 'a', 'More hyperconjugation spreads the positive charge.')],
    'fams': [F('C3', 'D2', 'short', alpha_h)],
    'qa': [('C4', 'D4', 'explain', 'Explain why the electron-withdrawing –NO₂ group makes p-nitrophenol a stronger acid than phenol.',
            '–NO₂ withdraws electrons by −I and −R effects, delocalising the negative charge of the phenoxide ion onto the nitro group and stabilising it; a more stable conjugate base means a stronger acid.',
            '1 mark: −R/−I effect; 1 mark: stabilisation of phenoxide ion.')],
}

# ---------------- ch08 st4 reaction types and bond fission ----------------

CH8S4 = {
    'topic': 'types of organic reactions',
    'terms': [('homolytic cleavage', 'the breaking of a covalent bond in which each atom takes one of the shared electrons, forming free radicals'),
              ('heterolytic cleavage', 'the breaking of a covalent bond in which one atom takes both shared electrons, forming ions'),
              ('a free radical', 'a neutral species with an unpaired electron'),
              ('a substitution reaction', 'a reaction in which an atom or group in a molecule is replaced by another atom or group'),
              ('an addition reaction', 'a reaction in which two molecules combine to form a single product, usually across a multiple bond'),
              ('an elimination reaction', 'a reaction in which two atoms or groups are removed from a molecule, usually forming a multiple bond'),
              ('a rearrangement reaction', 'a reaction in which atoms or groups of a molecule are rearranged to give a new structure')],
    'groups': [('a substitution reaction', ['CH₄ + Cl₂ → CH₃Cl + HCl (in light)', 'CH₃Br + OH⁻ → CH₃OH + Br⁻', 'C₆H₆ + Br₂ → C₆H₅Br + HBr (FeBr₃)', 'C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O (H₂SO₄)']),
               ('an addition reaction', ['CH₂=CH₂ + Br₂ → CH₂BrCH₂Br', 'CH₂=CH₂ + H₂ → CH₃CH₃ (Ni)', 'HC≡CH + 2H₂ → CH₃CH₃', 'CH₃CHO + HCN → CH₃CH(OH)CN']),
               ('an elimination reaction', ['CH₃CH₂OH → CH₂=CH₂ + H₂O (conc. H₂SO₄, 443 K)', 'CH₃CH₂Br + KOH(alc) → CH₂=CH₂ + KBr + H₂O', 'CH₂BrCH₂Br + Zn → CH₂=CH₂ + ZnBr₂']),
               ('a rearrangement reaction', ['n-butane → isobutane (AlCl₃/HCl)', 'NH₄CNO → NH₂CONH₂ (on heating)'])],
    'features': {'intro': 'A bond in a reaction breaks in this way:', 'q': 'Identify the type of bond fission', 'what': 'fission',
                 'items': [('homolytic fission', ['each atom keeps one electron of the bonding pair', 'free radicals are formed', 'favoured by heat, light or peroxides and non-polar solvents', 'shown with half-headed (fish-hook) arrows']),
                           ('heterolytic fission', ['one atom keeps both electrons of the bonding pair', 'a carbocation and an anion (or carbanion and cation) are formed', 'favoured by polar solvents', 'shown with full-headed curved arrows'])]},
    'tf': (['Homolytic fission produces free radicals.', 'Chlorination of methane in sunlight proceeds through free radicals.', 'Heterolytic fission gives ions.',
            'Addition of HBr to ethene is an addition reaction.', 'Free radicals are very reactive.'],
           [('Heterolytic fission produces free radicals.', 'Heterolytic fission produces ions; homolytic fission produces radicals.'),
            ('Dehydration of ethanol to ethene is a substitution reaction.', 'It is an elimination reaction.'),
            ('Free radicals carry a positive charge.', 'Free radicals are neutral species with an unpaired electron.'),
            ('Addition reactions are typical of alkanes.', 'Alkanes undergo substitution; addition is typical of unsaturated compounds.')]),
    'ar': [('Chlorination of methane requires sunlight or heat.', 'Energy is needed for homolytic fission of the Cl–Cl bond into chlorine free radicals.', 'a', 'Light provides energy to start the free radical chain.')],
    'qa': [('C4', 'D4', 'explain', 'Classify CH₃CH₂Br + KOH(aq) → CH₃CH₂OH + KBr and CH₃CH₂Br + KOH(alc) → CH₂=CH₂ + KBr + H₂O, and explain why the same reagents give different reactions.',
            'The first is substitution (OH⁻ acts as nucleophile in aqueous medium); the second is elimination (alcoholic KOH gives the stronger base alkoxide/OH⁻ that removes β-H).',
            '1 mark: classification; 1 mark: role of solvent/reagent behaviour.'),
           ('C4', 'D3', 'explain', 'Why are carbocations formed more easily in polar solvents?',
            'Heterolytic fission produces ions; polar solvents stabilise the ions by solvation, lowering the energy needed for the fission.',
            '1 mark: heterolysis gives ions; 1 mark: solvation stabilises them.')],
}

# ---------------- ch08 st5 purification and analysis ----------------

ORG = [('C₂H₆O (ethanol)', {'C': 2, 'H': 6, 'O': 1}), ('C₆H₁₂O₆ (glucose)', {'C': 6, 'H': 12, 'O': 6}), ('C₂H₄O₂ (acetic acid)', {'C': 2, 'H': 4, 'O': 2}),
       ('C₆H₆ (benzene)', {'C': 6, 'H': 6}), ('C₃H₆O (acetone)', {'C': 3, 'H': 6, 'O': 1}), ('C₇H₆O₂ (benzoic acid)', {'C': 7, 'H': 6, 'O': 2}),
       ('C₄H₁₀ (butane)', {'C': 4, 'H': 10})]
MA = {'C': 12, 'H': 1, 'O': 16}


def combustion(r):
    f, c = r.choice(ORG)
    Mm = sum(MA[e] * n for e, n in c.items())
    m = r.choice([0.20, 0.25, 0.30, 0.40, 0.50])
    mco2 = m / Mm * c['C'] * 44
    mh2o = m / Mm * c['H'] / 2 * 18
    pc = 12 / 44 * mco2 / m * 100
    ph = 2 / 18 * mh2o / m * 100
    return {'stem': f'On complete combustion, {m:.2f} g of an organic compound gave {mco2:.3f} g of CO₂ and {mh2o:.3f} g of H₂O. Calculate the percentage of carbon and hydrogen in it.',
            'answer': f'C = {pc:.2f}%; H = {ph:.2f}%', 'key': f'% C = (12/44) × ({mco2:.3f}/{m:.2f}) × 100 = {pc:.2f}% (1); % H = (2/18) × ({mh2o:.3f}/{m:.2f}) × 100 = {ph:.2f}% (1).',
            'distractors': [f'C = {mco2 / m * 100:.2f}%; H = {mh2o / m * 100:.2f}%', f'C = {pc:.2f}%; H = {ph / 2:.2f}%', f'C = {ph:.2f}%; H = {pc:.2f}%']}


def dumas(r):
    m = r.choice([0.15, 0.20, 0.25, 0.30, 0.35])
    V = r.choice([20, 25, 30, 35, 40, 45, 50])
    p = 28 * V / (22400 * m) * 100
    return {'stem': f'In Dumas\' method, {m:.2f} g of an organic compound gave {V} mL of nitrogen measured at STP. Calculate the percentage of nitrogen. (1 mol of N₂ occupies 22400 mL at STP)',
            'answer': f'{p:.2f}%', 'key': f'% N = (28 × V)/(22400 × m) × 100 = (28 × {V})/(22400 × {m:.2f}) × 100 = {p:.2f}%.',
            'distractors': [f'{p / 2:.2f}%', f'{14 * V / (22400 * m) * 100 * 4:.2f}%' if abs(14 * V / (22400 * m) * 400 - p) > 0.01 else f'{p * 1.5:.2f}%', f'{min(p * 3, 99):.2f}%']}


def kjeldahl(r):
    m = r.choice([0.25, 0.40, 0.50, 0.75, 1.0])
    M = r.choice([0.05, 0.1, 0.5])
    V = r.choice([10, 15, 20, 25, 30])
    p = 1.4 * M * 2 * V / m
    if p > 60:
        raise ValueError
    return {'stem': f'In Kjeldahl\'s method, the ammonia evolved from {m:.2f} g of an organic compound was exactly neutralised by {V} mL of {M} M H₂SO₄. Calculate the percentage of nitrogen.',
            'answer': f'{p:.2f}%', 'key': f'Moles of H₂SO₄ = {M} × {V}/1000; NH₃ = 2 × that = {2 * M * V / 1000:.4f} mol (1); % N = 14 × {2 * M * V / 1000:.4f}/{m:.2f} × 100 = {p:.2f}% (1).',
            'distractors': [f'{p / 2:.2f}%', f'{p * 2:.2f}%' if p * 2 < 100 else f'{p / 3:.2f}%', f'{p + 5:.2f}%']}


def carius(r):
    X, A, salt, Ms = r.choice([('bromine', 80, 'AgBr', 188), ('chlorine', 35.5, 'AgCl', 143.5), ('iodine', 127, 'AgI', 235), ('sulphur', 32, 'BaSO₄', 233)])
    m = r.choice([0.15, 0.20, 0.25, 0.30])
    pct = r.uniform(15, 70)
    mx = m * pct / 100 / A * Ms
    mx = round(mx, 3)
    p = A / Ms * mx / m * 100
    return {'stem': f'In the Carius method, {m:.2f} g of an organic compound gave {mx:.3f} g of {salt}. Calculate the percentage of {X} in the compound.',
            'answer': f'{p:.2f}%', 'key': f'% {X} = ({A}/{Ms}) × ({mx:.3f}/{m:.2f}) × 100 = {p:.2f}% (molar mass of {salt} = {Ms} g mol⁻¹).',
            'distractors': [f'{mx / m * 100:.2f}%', f'{p / 2:.2f}%', f'{100 - p:.2f}%']}


def rf(r):
    a = round(r.uniform(1.5, 6.5), 1)
    b = round(a + r.uniform(1.0, 6.0), 1)
    who = name(r)
    return {'stem': f'In {who}\'s paper chromatography experiment the solvent front moved {b} cm and a coloured spot moved {a} cm from the base line. Calculate the Rf value of the component.',
            'answer': f'{a / b:.2f}', 'key': f'Rf = distance moved by substance / distance moved by solvent front = {a}/{b} = {a / b:.2f}.',
            'distractors': [f'{b / a:.2f}', f'{(b - a) / b:.2f}', f'{a / (a + b):.2f}']}


CH8S5 = {
    'topic': 'purification and analysis of organic compounds',
    'features': {'intro': 'A mixture or compound has these properties:', 'q': 'Which method of purification is most suitable', 'what': 'method',
                 'items': [('sublimation', ['the compound changes directly from solid to vapour on heating', 'used for camphor, naphthalene or benzoic acid', 'the impurity is non-sublimable']),
                           ('crystallisation', ['the compound is a solid whose solubility in a solvent differs greatly from that of the impurities', 'it is sparingly soluble in the cold solvent but well soluble when hot', 'used to purify sugar or benzoic acid from water']),
                           ('simple distillation', ['two liquids differ widely in boiling points (e.g. chloroform 334 K and aniline 457 K)', 'the liquids do not decompose at their boiling points', 'the vapour of the lower-boiling liquid is condensed first']),
                           ('fractional distillation', ['two liquids have boiling points close to each other', 'a fractionating column is used', 'used to separate crude oil fractions']),
                           ('steam distillation', ['the compound is steam volatile and immiscible with water', 'used to separate aniline from an aniline–water mixture', 'the mixture boils below 373 K because the vapour pressures add']),
                           ('distillation under reduced pressure', ['the liquid decomposes at or below its boiling point', 'used to recover glycerol from spent lye in soap industry', 'the boiling point is lowered by reducing pressure']),
                           ('differential extraction', ['the compound is more soluble in an organic solvent than in water', 'a separating funnel is used', 'the two solvents are immiscible'])]},
    'features2': {'intro': "In Lassaigne's test the sodium fusion extract shows:", 'q': 'Which element is present', 'what': 'element', 'compare': False, 'long': False,
                  'items': [('nitrogen', ['a Prussian blue colour with FeSO₄ and then FeCl₃ in acid', 'formation of sodium cyanide during fusion', 'Fe₄[Fe(CN)₆]₃ formed']),
                            ('sulphur', ['a violet colour with sodium nitroprusside', 'a black precipitate of PbS with lead acetate', 'formation of Na₂S during fusion']),
                            ('nitrogen and sulphur together', ['a blood-red colour with FeCl₃', 'formation of sodium thiocyanate (NaSCN)', 'no Prussian blue because the cyanide is used up as thiocyanate']),
                            ('a halogen', ['a precipitate with AgNO₃ after boiling with HNO₃', 'white precipitate soluble in NH₄OH for chlorine', 'yellowish precipitate sparingly soluble in NH₄OH for bromine'])]},
    'terms': [('the Rf value', 'the ratio of the distance moved by a substance from the base line to the distance moved by the solvent front'),
              ('chromatography', 'a technique for separating components of a mixture using a stationary phase and a mobile phase'),
              ("Lassaigne's test", 'detection of N, S, P and halogens by converting them into ionic sodium compounds by fusing the organic compound with sodium')],
    'tf': (['In the Kjeldahl method nitrogen is converted into ammonium sulphate.', 'Kjeldahl\'s method is not applicable to nitro compounds, azo compounds and pyridine.',
            'In Dumas\' method nitrogen is collected over KOH solution.', 'Copper(II) oxide is used to oxidise carbon and hydrogen in Liebig\'s method.',
            'In Lassaigne\'s test nitric acid is added before AgNO₃ to decompose cyanide and sulphide.'],
           [('Kjeldahl\'s method works for all organic nitrogen compounds.', 'It does not work for nitro, azo compounds and nitrogen in a ring (pyridine).'),
            ('Steam distillation is used for liquids miscible with water.', 'Steam distillation is used for steam-volatile liquids immiscible with water.'),
            ('Glycerol is purified by simple distillation.', 'Glycerol decomposes at its boiling point; it is distilled under reduced pressure.'),
            ('In Liebig\'s method CO₂ is absorbed in anhydrous CaCl₂.', 'CO₂ is absorbed in KOH; water is absorbed in anhydrous CaCl₂.')]),
    'ar': [('Aniline is separated from water by steam distillation.', 'Aniline is steam volatile and immiscible with water.', 'a', 'The mixture boils below 373 K and aniline distils with steam.'),
           ('Sodium fusion extract is boiled with HNO₃ before testing for halogens.', 'Cyanide and sulphide ions, if present, would give a precipitate with AgNO₃.', 'a', 'Boiling with HNO₃ removes CN⁻ and S²⁻ that would interfere.')],
    'fams': [F('C3', 'D3', 'numerical', combustion), F('C3', 'D3', 'numerical', dumas), F('C3', 'D3', 'numerical', kjeldahl),
             F('C3', 'D2', 'numerical', carius), F('C2', 'D1', 'numerical', rf)],
}

# ---------------- ch09 st1 alkanes ----------------

ALK = ['methane', 'ethane', 'propane', 'butane', 'pentane', 'hexane', 'heptane', 'octane']
ALK_F = ['CH₄', 'C₂H₆', 'C₃H₈', 'C₄H₁₀', 'C₅H₁₂', 'C₆H₁₄', 'C₇H₁₆', 'C₈H₁₈']
RX_ = ['methyl', 'ethyl', 'propyl', 'butyl']
ACID = ['ethanoate', 'propanoate', 'butanoate', 'pentanoate']


def wurtz(r):
    n = r.randint(1, 4)
    X = r.choice(['bromide', 'iodide', 'chloride'])
    prod = ALK[2 * n - 1]
    wrong = list(dict.fromkeys([ALK[n - 1], ALK[min(n, 7)], ALK[min(2 * n, 7)], ALK[2 * n - 2] if 2 * n - 2 >= 0 else ALK[3]]))
    wrong = [w for w in wrong if w != prod][:3]
    return mcq(f'What is the main product when {RX_[n - 1]} {X} is heated with sodium in dry ether (Wurtz reaction)?', prod, wrong,
               f'2R–X + 2Na → R–R + 2NaX; two {RX_[n - 1]} groups join to give {prod} ({ALK_F[2 * n - 1]}).', r)


def decarbox(r):
    n = r.randint(2, 5)
    prod = ALK[n - 2]
    wrong = [w for w in dict.fromkeys([ALK[n - 1], ALK[min(n, 7)], ALK[max(n - 3, 0)] if n - 3 >= 0 else ALK[4], ALK[2 * (n - 1) - 1]]) if w != prod][:3]
    salt = f'sodium {ACID[n - 2]}'
    return mcq(f'Which alkane is formed when {salt} is heated with soda lime (decarboxylation)?', prod, wrong,
               f'RCOONa + NaOH → R–H + Na₂CO₃ (CaO); the product has one carbon less than the acid: {prod}.', r)


def kolbe(r):
    n = r.randint(1, 3)
    salt = ['sodium ethanoate', 'sodium propanoate', 'sodium butanoate'][n - 1]
    prod = ALK[2 * n - 1]
    return {'stem': f'Name the alkane obtained at the anode on electrolysis of an aqueous solution of {salt} (Kolbe\'s electrolytic method), and write the overall equation.',
            'answer': prod, 'key': f'2RCOO⁻Na⁺ + 2H₂O → R–R + 2CO₂ + H₂ + 2NaOH, with R = {RX_[n - 1]}; the alkane is {prod} ({ALK_F[2 * n - 1]}) (1 + 1).',
            'distractors': [ALK[n], ALK[n - 1] if n > 1 else ALK[2], ALK[2 * n]]}


def alkane_o2(r):
    n = r.randint(1, 8)
    V = r.choice([10, 20, 50, 100, 200])
    o2 = (3 * n + 1) / 2
    return {'stem': f'What volume of oxygen is needed for complete combustion of {V} mL of {ALK[n - 1]} ({ALK_F[n - 1]}), all volumes at the same temperature and pressure? Write the balanced equation.',
            'answer': f'{num(V * o2)} mL', 'key': f'CₙH₂ₙ₊₂ + (3n + 1)/2 O₂ → nCO₂ + (n + 1)H₂O; for n = {n}: 1 : {num(o2)} by volume (1) ⇒ {num(V * o2)} mL (1).',
            'distractors': [f'{num(V * n)} mL', f'{num(V * (n + 1))} mL', f'{num(V * o2 * 2)} mL']}


CH9S1 = {
    'topic': 'alkanes',
    'terms': [('a conformation', 'a spatial arrangement of atoms in a molecule obtained by rotation about a C–C single bond'),
              ('the staggered conformation', 'the conformation of ethane in which the hydrogens on the two carbons are as far apart as possible'),
              ('the eclipsed conformation', 'the conformation of ethane in which the hydrogens on the two carbons are directly behind each other'),
              ('torsional strain', 'the repulsive interaction between electron clouds of bonds on adjacent atoms in a conformation'),
              ('pyrolysis (cracking)', 'the decomposition of higher alkanes into lower alkanes and alkenes by heating'),
              ('aromatisation', 'the conversion of n-alkanes with six or more carbons into benzene and its homologues over Cr₂O₃/V₂O₅ catalysts at high temperature'),
              ('the Wurtz reaction', 'the reaction of alkyl halides with sodium in dry ether to form higher alkanes')],
    'tf': (['The staggered conformation of ethane is more stable than the eclipsed one.', 'The energy difference between eclipsed and staggered ethane is about 12.5 kJ mol⁻¹.',
            'Alkanes are generally unreactive because C–C and C–H bonds are strong and non-polar.', 'Methane can be prepared by decarboxylation of sodium acetate.',
            'The Wurtz reaction cannot be used to make methane.'],
           [('Conformations of ethane can be separated at room temperature.', 'The rotational barrier is small (12.5 kJ mol⁻¹), so they interconvert rapidly and cannot be isolated.'),
            ('The eclipsed conformation of ethane is the most stable.', 'The staggered form has least torsional strain and is most stable.'),
            ('Decarboxylation gives an alkane with one carbon more than the acid.', 'It gives an alkane with one carbon less than the acid.'),
            ('Alkanes readily undergo addition reactions.', 'Alkanes are saturated; they undergo substitution, not addition.')]),
    'orders': [('increasing order of boiling point', ['2,2-dimethylpropane', '2-methylbutane', 'pentane'], 'Branching reduces surface area and van der Waals forces, lowering the boiling point.', '<'),
               ('increasing order of boiling point', ['methane', 'ethane', 'propane', 'butane', 'pentane', 'hexane'], 'Boiling point rises with molecular mass and surface area.', '<')],
    'ar': [('Neopentane has a lower boiling point than n-pentane.', 'Branching decreases the surface area and van der Waals forces.', 'a', 'Weaker intermolecular forces lower the boiling point.'),
           ('Methane cannot be prepared by the Wurtz reaction.', 'The Wurtz reaction joins two alkyl groups, so the product has at least two carbon atoms.', 'a', 'R–R always has an even number of carbons ≥ 2.')],
    'fams': [F('C2', 'D2', 'mcq', wurtz), F('C2', 'D2', 'mcq', decarbox), F('C3', 'D3', 'explain', kolbe), F('C3', 'D2', 'numerical', alkane_o2)],
    'qa': [('C4', 'D4', 'explain', 'A mixture of methyl bromide and ethyl bromide is heated with sodium in dry ether. Which alkanes are formed? Why is the Wurtz reaction not good for preparing alkanes with an odd number of carbons?',
            'Ethane (CH₃–CH₃), propane (CH₃–C₂H₅) and butane (C₂H₅–C₂H₅). Mixed halides give a mixture of three alkanes that is hard to separate, so odd-carbon alkanes are not obtained pure.',
            '1 mark: three products; 1 mark: mixture/separation problem.'),
           ('C4', 'D5', 'long', 'Draw (describe) the Newman projections of the staggered and eclipsed conformations of ethane. (a) Which is more stable and why? (b) What is the energy difference? (c) Why cannot the two be isolated? (d) What is meant by the dihedral angle in the two forms?',
            'Staggered: rear H atoms at 60° to front ones; eclipsed: rear H atoms directly behind front ones. (a) Staggered, minimum torsional strain. (b) ~12.5 kJ mol⁻¹. (c) The barrier is small, so rotation is rapid at room temperature. (d) Angle between C–H bonds on adjacent carbons: 60° staggered, 0° eclipsed.',
            '1 mark diagrams; 1 mark each (a)-(d).')],
}

# ---------------- ch09 st2 alkenes ----------------

MARK = [('propene', 'HBr', '2-bromopropane', '1-bromopropane', False), ('propene', 'HBr in the presence of benzoyl peroxide', '1-bromopropane', '2-bromopropane', True),
        ('but-1-ene', 'HBr', '2-bromobutane', '1-bromobutane', False), ('2-methylpropene', 'HBr', '2-bromo-2-methylpropane', '1-bromo-2-methylpropane', False),
        ('2-methylpropene', 'HBr in the presence of peroxide', '1-bromo-2-methylpropane', '2-bromo-2-methylpropane', True),
        ('propene', 'H₂O in the presence of dilute H₂SO₄', 'propan-2-ol', 'propan-1-ol', False), ('but-1-ene', 'HCl', '2-chlorobutane', '1-chlorobutane', False),
        ('2-methylbut-2-ene', 'HBr', '2-bromo-2-methylbutane', '2-bromo-3-methylbutane', False)]


def markovnikov(r):
    a, reag, p, anti, perox = r.choice(MARK)
    wrong = [anti, a.replace('ene', 'ane'), p.replace('bromo', 'dibromo').replace('chloro', 'dichloro') if 'ol' not in p else 'propane-1,2-diol']
    return mcq(f'What is the major product of the reaction of {a} with {reag}?', p, wrong,
               (f'Anti-Markovnikov (peroxide/Kharash) addition through the more stable free radical gives {p}.' if perox else
                f'Markovnikov\'s rule: H adds to the carbon with more hydrogens, via the more stable carbocation, giving {p}.'), r)


OZO = [('ethene', ['methanal', 'methanal']), ('propene', ['ethanal', 'methanal']), ('but-1-ene', ['propanal', 'methanal']),
       ('but-2-ene', ['ethanal', 'ethanal']), ('2-methylpropene', ['propanone', 'methanal']), ('2-methylbut-2-ene', ['propanone', 'ethanal']),
       ('pent-2-ene', ['ethanal', 'propanal']), ('2,3-dimethylbut-2-ene', ['propanone', 'propanone']), ('pent-1-ene', ['butanal', 'methanal'])]


def ozono(r):
    a, ps = r.choice(OZO)
    good = ' and '.join(ps) if ps[0] != ps[1] else f'two molecules of {ps[0]}'
    others = [x for x in OZO if x[0] != a]
    wrong = [(' and '.join(x[1]) if x[1][0] != x[1][1] else f'two molecules of {x[1][0]}') for x in r.sample(others, 3)]
    if r.random() < 0.5:
        return mcq(f'What are the products of ozonolysis (O₃ followed by Zn/H₂O) of {a}?', good, wrong, f'The C=C is cleaved and each carbon becomes C=O: {a} → {good}.', r)
    return mcq(f'An alkene on ozonolysis gives {good}. Identify the alkene.', a, [x[0] for x in r.sample(others, 3)],
               f'Joining the two carbonyl carbons by a double bond gives {a}.', r)


GEO = [('but-2-ene', True), ('but-1-ene', False), ('2-methylpropene', False), ('pent-2-ene', True), ('1,2-dichloroethene', True),
       ('1,1-dichloroethene', False), ('propene', False), ('hex-3-ene', True), ('2-methylbut-2-ene', False), ('but-2-enoic acid', True)]


def geo_iso(r):
    yes = [x[0] for x in GEO if x[1]]
    no = [x[0] for x in GEO if not x[1]]
    if r.random() < 0.5:
        good = r.choice(yes)
        return mcq('Which of the following alkenes shows geometrical (cis–trans) isomerism?', good, r.sample(no, 3),
                   f'{cap(good)} has two different groups on each doubly bonded carbon; the others have two identical groups on one carbon.', r)
    good = r.choice(no)
    return mcq('Which of the following does NOT show geometrical (cis–trans) isomerism?', good, r.sample(yes, 3),
               f'{cap(good)} has two identical groups on one of the doubly bonded carbons.', r)


CH9S2 = {
    'topic': 'alkenes',
    'terms': [("Markovnikov's rule", 'the rule that the negative part of an addendum adds to the carbon atom of the double bond that has fewer hydrogen atoms'),
              ('the peroxide (Kharash) effect', 'the anti-Markovnikov addition of HBr to unsymmetrical alkenes in the presence of an organic peroxide'),
              ('ozonolysis', 'the addition of ozone to an alkene followed by cleavage with Zn/H₂O to give aldehydes or ketones'),
              ('geometrical isomerism', 'stereoisomerism due to different spatial arrangement of groups about a double bond'),
              ('dehydrohalogenation', 'the removal of HX from an alkyl halide by heating with alcoholic KOH to form an alkene'),
              ("Baeyer's reagent", 'cold dilute aqueous potassium permanganate, decolourised by alkenes')],
    'tf': (['cis-But-2-ene has a higher dipole moment than trans-but-2-ene.', 'The peroxide effect is observed only with HBr.',
            'Alkenes decolourise bromine water.', 'Ethene is prepared by heating ethanol with concentrated H₂SO₄ at 443 K.',
            'Hydrogenation of alkenes in the presence of finely divided Ni gives alkanes.'],
           [('The peroxide effect is shown by HCl and HI also.', 'Only HBr shows the peroxide effect; H–Cl is too strong and H–I too weak in the radical steps.'),
            ('trans-But-2-ene is more polar than cis-but-2-ene.', 'In the trans isomer dipoles cancel; the cis isomer is more polar.'),
            ('Addition of HBr to propene gives 1-bromopropane as the major product in the absence of peroxide.', 'Markovnikov addition gives 2-bromopropane.'),
            ('Alkenes do not decolourise Baeyer\'s reagent.', 'Alkenes decolourise cold dilute KMnO₄ (forming glycols).')]),
    'ar': [('Propene reacts with HBr to give 2-bromopropane.', 'The secondary carbocation formed is more stable than the primary one.', 'a', 'Markovnikov product via the more stable 2° carbocation.'),
           ('cis-But-2-ene has a lower melting point than trans-but-2-ene.', 'The trans isomer is more symmetrical and packs better in the crystal lattice.', 'a', 'Better packing gives a higher melting point to the trans form.')],
    'fams': [F('C3', 'D3', 'mcq', markovnikov), F('C3', 'D3', 'mcq', ozono), F('C2', 'D2', 'mcq', geo_iso)],
    'qa': [('C4', 'D4', 'explain', 'An alkene C₄H₈ gives only one product, ethanal, on ozonolysis. Identify it and state whether it shows geometrical isomerism.',
            'But-2-ene (CH₃CH=CHCH₃); yes, it exists as cis- and trans-but-2-ene because each doubly bonded carbon carries H and CH₃.',
            '1 mark: but-2-ene; 1 mark: geometrical isomerism with reason.'),
           ('C4', 'D5', 'long', 'Explain, with mechanism, why HBr adds to propene in the presence of benzoyl peroxide to give 1-bromopropane, but in its absence gives 2-bromopropane. Why is the peroxide effect not observed with HCl?',
            'Without peroxide: ionic electrophilic addition; H⁺ adds to C1 to give the more stable 2° carbocation, then Br⁻ ⇒ 2-bromopropane. With peroxide: Br• (from HBr + peroxide radicals) adds to C1 to give the more stable 2° radical, which takes H from HBr ⇒ 1-bromopropane. H–Cl is too strong to be split homolytically by the radicals.',
            '2 marks ionic mechanism; 2 marks radical mechanism; 1 mark HCl explanation.'),
           ('C4', 'D3', 'case', 'An unknown hydrocarbon X (C₄H₈) decolourises bromine water and Baeyer\'s reagent. On ozonolysis it gives propanone and methanal.\n(i) What do the two tests show? (1 mark)\n(ii) Identify X. (1 mark)\n(iii) Write the major product of X with HBr and explain the rule used. (2 marks)',
            '(i) X is unsaturated (contains C=C). (ii) 2-Methylpropene, (CH₃)₂C=CH₂. (iii) 2-Bromo-2-methylpropane; Markovnikov\'s rule via the stable 3° carbocation.',
            '(i) 1 (ii) 1 (iii) 1 product + 1 rule/explanation.', ('case',))],
}

# ---------------- ch09 st3 alkynes ----------------

def carbide(r):
    m = r.choice([6.4, 12.8, 16, 32, 64, 3.2])
    who = name(r)
    n = m / 64
    V = n * 22.7
    return {'stem': f'{who} adds excess water to {m} g of calcium carbide: CaC₂ + 2H₂O → Ca(OH)₂ + C₂H₂. What volume of ethyne is obtained at STP? (Ca = 40, C = 12; molar volume at STP = 22.7 L)',
            'answer': f'{sf(V, 3)} L', 'key': f'n(CaC₂) = {m}/64 = {num(n, 3)} mol = n(C₂H₂) (1); V = {num(n, 3)} × 22.7 = {sf(V, 3)} L (1).',
            'distractors': [f'{sf(V * 2, 3)} L', f'{sf(m / 26 * 22.7, 3)} L', f'{sf(V / 2, 3)} L']}


HYDRATION = [('ethyne', 'ethanal'), ('propyne', 'propanone'), ('but-1-yne', 'butan-2-one'), ('but-2-yne', 'butan-2-one')]


def alkyne_h2o(r):
    a, p = r.choice(HYDRATION)
    wrong = [w for w in ['ethanal', 'propanone', 'propanal', 'butanal', 'butan-2-one', 'ethanol'] if w != p]
    return mcq(f'What is formed when {a} is passed into dilute H₂SO₄ containing HgSO₄ at 333 K?', p, r.sample(wrong, 3),
               f'Water adds by Markovnikov\'s rule to give an enol, which tautomerises to {p}.', r)


CH9S3 = {
    'topic': 'alkynes',
    'terms': [('a terminal alkyne', 'an alkyne in which the triple bond is at the end of the chain, carrying an acidic hydrogen'),
              ('an acetylide', 'a salt formed when the acidic hydrogen of ethyne or a terminal alkyne is replaced by a metal'),
              ('cyclic polymerisation of ethyne', 'the conversion of three molecules of ethyne into benzene in a red-hot iron tube at 873 K')],
    'groups': [('a compound that reacts with sodium metal to liberate H₂', ['ethyne', 'propyne', 'but-1-yne']), ('a compound that does not react with sodium metal', ['ethene', 'ethane', 'but-2-yne', 'propene'])],
    'orders': [('increasing order of acidic character', ['ethane', 'ethene', 'ethyne'], 'Carbon s character increases sp³ < sp² < sp, so the C–H electrons are held more tightly and H⁺ is lost more easily.', '<'),
               ('increasing order of C–H bond length (decreasing s character of carbon)', ['ethyne', 'ethene', 'ethane'], 'More s character gives a shorter C–H bond: sp < sp² < sp³ in length.', '<')],
    'tf': (['Ethyne is acidic because its hydrogens are attached to sp-hybridised carbon.', 'Ethyne can be prepared from calcium carbide and water.',
            'But-2-yne does not react with sodamide to give a salt.', 'Hydration of propyne gives propanone.', 'Ethyne is a linear molecule.'],
           [('All alkynes are acidic.', 'Only terminal alkynes (with ≡C–H) are acidic; but-2-yne is not.'),
            ('Ethyne is less acidic than ethene.', 'Ethyne is more acidic because sp carbon has 50% s character.'),
            ('Hydration of ethyne gives ethanol.', 'Hydration of ethyne gives ethanal via an enol.'),
            ('Three molecules of ethyne polymerise to give cyclohexane.', 'They give benzene in a red-hot iron tube at 873 K.')]),
    'ar': [('Ethyne reacts with sodium to liberate hydrogen.', 'The hydrogen in ethyne is attached to an sp-hybridised carbon with 50% s character.', 'a', 'The highly electronegative sp carbon makes the H acidic.'),
           ('But-2-yne does not form a sodium salt.', 'But-2-yne has no hydrogen on a triply bonded carbon.', 'a', 'Only ≡C–H hydrogens are acidic.')],
    'fams': [F('C3', 'D2', 'numerical', carbide), F('C3', 'D3', 'mcq', alkyne_h2o)],
    'qa': [('C4', 'D4', 'explain', 'How will you distinguish but-1-yne from but-2-yne by a chemical test? Explain.',
            'But-1-yne (terminal) gives a precipitate with ammoniacal AgNO₃ (Tollens\') or ammoniacal Cu₂Cl₂ / liberates H₂ with Na; but-2-yne does not, as it lacks an acidic ≡C–H.',
            '1 mark: test and observation; 1 mark: reason (acidic terminal H).'),
           ('C4', 'D3', 'explain', 'Convert ethyne into benzene and benzene into ethylbenzene, naming the conditions.',
            'Ethyne → benzene: pass through a red-hot iron tube at 873 K. Benzene + C₂H₅Cl (anhyd. AlCl₃) → ethylbenzene + HCl (Friedel–Crafts alkylation).',
            '1 mark each step with conditions.')],
}

# ---------------- ch09 st4 aromatic hydrocarbons ----------------

HUCKEL = [('benzene', 6, 'aromatic'), ('the cyclopentadienyl anion', 6, 'aromatic'), ('the cycloheptatrienyl (tropylium) cation', 6, 'aromatic'),
          ('naphthalene', 10, 'aromatic'), ('the cyclopropenyl cation', 2, 'aromatic'), ('pyridine', 6, 'aromatic'), ('furan', 6, 'aromatic'),
          ('the cyclopentadienyl cation', 4, 'anti-aromatic'), ('cyclobutadiene', 4, 'anti-aromatic'), ('cyclooctatetraene (tub-shaped)', 8, 'non-aromatic')]


def huckel(r):
    s, n, t = r.choice(HUCKEL)
    return {'stem': f'How many π electrons are delocalised in {s}? Is it aromatic according to Hückel\'s rule?',
            'answer': f'{n} π electrons; {t}', 'key': f'{n} π electrons; aromatic needs a planar cyclic conjugated ring with (4n + 2) π electrons (n = 0, 1, 2 …) ⇒ {t}' + (' (it is not planar).' if 'tub' in s else '.'),
            'distractors': [f'{n} π electrons; {"anti-aromatic" if t == "aromatic" else "aromatic"}', f'{n + 2} π electrons; {t}', f'{max(n - 2, 2)} π electrons; aromatic' if n != 4 else '6 π electrons; aromatic']}


ESUB = [('nitration', 'NO₂⁺ (nitronium ion)', 'conc. HNO₃ + conc. H₂SO₄'), ('sulphonation', 'SO₃', 'fuming H₂SO₄ (oleum)'),
        ('chlorination', 'Cl⁺', 'Cl₂ with anhydrous FeCl₃'), ('Friedel–Crafts alkylation', 'R⁺ (carbocation, e.g. CH₃⁺)', 'CH₃Cl with anhydrous AlCl₃'),
        ('Friedel–Crafts acylation', 'RCO⁺ (acylium ion)', 'CH₃COCl with anhydrous AlCl₃')]


def electrophile(r):
    rx, el, reag = r.choice(ESUB)
    return mcq(f'What is the attacking electrophile in the {rx} of benzene using {reag}?', el, [x[1] for x in ESUB if x[1] != el][:3] if len(ESUB) > 3 else [],
               f'{reag} generates {el}, which attacks the benzene ring.', r)


SUBST_PROD = [('toluene', 'nitration', 'o-nitrotoluene and p-nitrotoluene'), ('nitrobenzene', 'nitration', 'm-dinitrobenzene'),
              ('chlorobenzene', 'nitration', '1-chloro-2-nitrobenzene and 1-chloro-4-nitrobenzene'), ('phenol', 'bromination in CS₂ (low temperature)', 'o-bromophenol and p-bromophenol'),
              ('benzoic acid', 'nitration', 'm-nitrobenzoic acid'), ('anisole', 'Friedel–Crafts methylation', '2-methoxytoluene and 4-methoxytoluene'),
              ('benzaldehyde', 'nitration', 'm-nitrobenzaldehyde'), ('toluene', 'chlorination with FeCl₃', 'o-chlorotoluene and p-chlorotoluene')]


def directive(r):
    s, rx, p = r.choice(SUBST_PROD)
    wrong = [x[2] for x in SUBST_PROD if x[2] != p]
    return mcq(f'What are the main product(s) of {rx} of {s}?', p, r.sample(wrong, 3),
               f'The substituent in {s} is {"ortho/para" if "o-" in p or "2-" in p else "meta"} directing: {p}.', r)


CH9S4 = {
    'topic': 'aromatic hydrocarbons',
    'terms': [('aromaticity', 'the special stability of planar cyclic conjugated molecules with (4n + 2) π electrons'),
              ("Hückel's rule", 'the rule that a planar, cyclic, fully conjugated system is aromatic if it has (4n + 2) π electrons'),
              ('electrophilic substitution', 'a reaction in which an electrophile replaces a hydrogen atom on an aromatic ring'),
              ('an activating group', 'a substituent that increases the electron density of the benzene ring and makes it more reactive towards electrophiles'),
              ('a deactivating group', 'a substituent that decreases the electron density of the benzene ring'),
              ('a σ-complex (arenium ion)', 'the carbocation intermediate formed when an electrophile attacks the benzene ring')],
    'groups': [('an ortho/para-directing group', ['–OH', '–NH₂', '–CH₃', '–OCH₃', '–Cl', '–NHCOCH₃']), ('a meta-directing group', ['–NO₂', '–CHO', '–COOH', '–CN', '–SO₃H', '–COCH₃'])],
    'orders': [('increasing order of reactivity towards electrophilic substitution', ['nitrobenzene', 'chlorobenzene', 'benzene', 'toluene', 'phenol'],
                '–NO₂ strongly deactivates, –Cl weakly deactivates, –CH₃ activates (+I, hyperconjugation), –OH strongly activates (+R).', '<')],
    'tf': (['All C–C bonds in benzene are of equal length (139 pm).', 'Benzene prefers substitution over addition to keep its aromatic stability.',
            'Halogens are deactivating but ortho/para directing.', 'Anhydrous AlCl₃ acts as a Lewis acid in Friedel–Crafts reactions.',
            'Benzene burns with a sooty flame.'],
           [('Benzene readily undergoes addition like an alkene.', 'Benzene prefers substitution; addition destroys the aromatic sextet.'),
            ('–NO₂ is an ortho/para-directing group.', '–NO₂ is a meta-directing, deactivating group.'),
            ('Halogens are activating groups.', 'Halogens deactivate the ring by −I effect, though they are o/p directing by +R.'),
            ('Cyclooctatetraene is aromatic.', 'It is tub-shaped (non-planar) with 8 π electrons and is non-aromatic.')]),
    'ar': [('Benzene undergoes electrophilic substitution rather than addition.', 'Substitution retains the stable delocalised π-electron system.', 'a', 'Aromatic stabilisation is kept in the product.'),
           ('Toluene undergoes nitration faster than benzene.', 'The methyl group releases electrons and activates the ring.', 'a', 'Higher electron density speeds up electrophilic attack.'),
           ('Chlorobenzene is ortho/para directing.', 'Chlorine has a strong +I effect.', 'c', 'A is true (o/p by +R effect), but chlorine has a −I effect, so R is false.')],
    'fams': [F('C3', 'D3', 'explain', huckel), F('C2', 'D2', 'mcq', electrophile), F('C3', 'D3', 'mcq', directive)],
    'qa': [('C4', 'D5', 'long', 'Explain the mechanism of nitration of benzene: (a) generation of the electrophile, (b) formation of the σ-complex, (c) loss of proton. Why is the reaction slower with nitrobenzene?',
            '(a) HNO₃ + 2H₂SO₄ → NO₂⁺ + H₃O⁺ + 2HSO₄⁻. (b) NO₂⁺ attacks the π cloud to give a resonance-stabilised arenium ion (sp³ carbon). (c) HSO₄⁻ removes H⁺, restoring aromaticity: C₆H₅NO₂. Nitrobenzene is deactivated by the −I/−R effect of –NO₂.',
            '(a) 1 (b) 2 (c) 1 (d) 1.'),
           ('C4', 'D4', 'explain', 'Although benzene is highly unsaturated, it does not decolourise bromine water or Baeyer\'s reagent. Explain.',
            'The π electrons are delocalised over the ring (resonance, aromatic sextet), giving extra stability; addition would destroy aromaticity, so it does not react like an alkene.',
            '1 mark: delocalisation/aromatic stability; 1 mark: addition would destroy it.')],
}

# ---------------- ch09 st5 carcinogenicity and toxicity ----------------

CH9S5 = {
    'topic': 'carcinogenicity and toxicity of hydrocarbons',
    'terms': [('a carcinogen', 'a substance that can cause cancer'),
              ('a polynuclear aromatic hydrocarbon', 'a hydrocarbon with more than two benzene rings fused together'),
              ('incomplete combustion', 'burning of a fuel in insufficient oxygen, producing soot, CO and polynuclear hydrocarbons')],
    'groups': [('a carcinogenic polynuclear hydrocarbon', ['1,2-benzanthracene', '3-methylcholanthrene', '1,2-benzpyrene', '1,2,5,6-dibenzanthracene', '9,10-dimethyl-1,2-benzanthracene']),
               ('a hydrocarbon not classed as a polynuclear carcinogen', ['methane', 'ethene', 'hexane', 'cyclohexane'])],
    'classify': False,
    'tf': (['Polynuclear hydrocarbons are formed by incomplete combustion of tobacco, coal and petroleum.', 'Benzene is toxic and carcinogenic.',
            'Polynuclear hydrocarbons damage DNA after entering the body.', 'Hydrocarbons with more than two fused benzene rings may be carcinogenic.'],
           [('Polynuclear hydrocarbons are formed by complete combustion of fuels.', 'They are formed by incomplete combustion of organic matter.'),
            ('Only aliphatic hydrocarbons are carcinogenic.', 'Benzene and polynuclear aromatic hydrocarbons are the known carcinogens.'),
            ('Benzpyrene contains only two fused benzene rings.', 'Benzpyrene has five fused rings; carcinogens have more than two fused rings.'),
            ('Smoke from tobacco contains no hydrocarbons.', 'Tobacco smoke contains carcinogenic polynuclear hydrocarbons such as benzpyrene.')]),
    'ar': [('Inhaling cigarette smoke increases the risk of lung cancer.', 'Tobacco smoke contains polynuclear hydrocarbons such as 1,2-benzpyrene that can damage DNA.', 'a', 'Carcinogenic PAHs from incomplete combustion cause cancer.'),
           ('Polynuclear hydrocarbons are formed during incomplete combustion.', 'Benzene has three double bonds.', 'b', 'Both are true, but the structure of benzene does not explain how PAHs are formed.')],
    'qa': [('C3', 'D2', 'explain', 'Name two sources from which carcinogenic polynuclear hydrocarbons enter the environment.',
            'Incomplete combustion of tobacco (cigarette smoke), coal, petroleum products (vehicle exhaust), wood.', '1 mark each for any two sources.'),
           ('C3', 'D3', 'explain', 'How do polynuclear hydrocarbons cause cancer?',
            'After entering the body they undergo biochemical reactions (metabolic activation) and finally damage DNA, causing uncontrolled cell division (cancer).', '1 mark: biochemical changes; 1 mark: DNA damage.'),
           ('C4', 'D3', 'explain', 'Suggest two measures that can reduce exposure of people in a city like Delhi to carcinogenic hydrocarbons.',
            'Ensure complete combustion (better engines, CNG/BS-VI fuel, catalytic converters); avoid smoking and burning of waste; use LPG instead of coal or wood in homes.', '1 mark each for any two valid measures.'),
           ('C4', 'D4', 'explain', 'Why do tandoor or coal-fired kitchens with poor ventilation pose a greater cancer risk than LPG kitchens?',
            'Coal/wood burn incompletely in limited air, producing soot and polynuclear aromatic hydrocarbons; LPG burns more completely, producing mainly CO₂ and H₂O.', '1 mark: incomplete combustion produces PAHs; 1 mark: LPG burns cleanly.'),
           ('C4', 'D3', 'case', 'A survey found that workers in coal-tar processing units and chimney sweeps had higher rates of skin cancer than office workers.\n(i) Name one carcinogen likely to be present in coal tar. (1 mark)\n(ii) What structural feature do such carcinogens share? (1 mark)\n(iii) Suggest two safety measures for these workers. (2 marks)',
            '(i) 1,2-benzpyrene (or 3-methylcholanthrene / 1,2-benzanthracene). (ii) More than two fused benzene rings (polynuclear aromatic). (iii) Protective clothing and gloves; masks and ventilation; washing skin; regular health checks.',
            '(i) 1 (ii) 1 (iii) 1 each for two measures.', ('case',)),
           ('C4', 'D5', 'long', 'Write a short note on the toxicity of hydrocarbons covering: (a) what polynuclear hydrocarbons are, with two examples; (b) how they are formed; (c) how they act on the body; (d) two ways society can reduce exposure.',
            '(a) Hydrocarbons with more than two fused benzene rings, e.g. 1,2-benzpyrene, 3-methylcholanthrene. (b) Incomplete combustion of tobacco, coal, petroleum. (c) Enter the body, undergo biochemical reactions and damage DNA, causing cancer. (d) Cleaner fuels/complete combustion, ban smoking in public, better ventilation, protective gear.',
            '(a) 1.5 (b) 1 (c) 1.5 (d) 1.')],
}

SPECS = {'ch07-st1': CH7S1, 'ch07-st2': CH7S2, 'ch07-st3': CH7S3, 'ch07-st4': CH7S4,
         'ch08-st1': CH8S1, 'ch08-st2': CH8S2, 'ch08-st3': CH8S3, 'ch08-st4': CH8S4, 'ch08-st5': CH8S5,
         'ch09-st1': CH9S1, 'ch09-st2': CH9S2, 'ch09-st3': CH9S3, 'ch09-st4': CH9S4, 'ch09-st5': CH9S5}

FAMILIES = build_all(P, SPECS)
