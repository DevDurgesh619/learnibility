"""CBSE Class 12 Chemistry, units 7-10: alcohols, phenols and ethers; aldehydes, ketones and carboxylic acids; amines; biomolecules.

Families are built from fact tables with the shared kit in g11_chemistry_kit.py; numerical answers are computed here.
"""
from __future__ import annotations

import math

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap

P = 'cbse-g12-chemistry'


def table_mcq(rows, stem_fmt, why_fmt=None, pool=None):
    """rows: (a, b, answer, why). Builds an MCQ generator with wrong answers from other rows (or `pool`)."""
    def g(r):
        a, b, ans, why = r.choice(rows)
        src = pool if pool else [x[2] for x in rows]
        wrong = [x for x in dict.fromkeys(src) if x != ans]
        if len(wrong) < 3:
            raise ValueError('pool too small')
        return mcq(stem_fmt.format(a=a, b=b), ans, r.sample(wrong, 3), (why_fmt or '{ans}: {why}.').format(a=a, b=b, ans=cap(ans), why=why), r)
    return g


def table_explain(rows, stem_fmt, marks_note='Product (1); reaction name or reason (1).'):
    def g(r):
        a, b, ans, why = r.choice(rows)
        others = [f'{cap(x[2])}; {x[3]}' for x in rows if x[2] != ans]
        return {'stem': stem_fmt.format(a=a, b=b), 'answer': f'{cap(ans)}; {why}', 'key': f'{cap(ans)} (1); {why} (1).',
                'distractors': r.sample(others, 3)}
    return g


def name_mcq(rows, what='compound'):
    """rows: (formula, correct name, [wrong names])."""
    def g(r):
        f, good, wrong = r.choice(rows)
        return mcq(f'What is the IUPAC name of {f}?', good, r.sample(wrong, 3), f'{f} = {good}.', r)

    def h(r):
        f, good, wrong = r.choice(rows)
        others = [x[0] for x in rows if x[0] != f]
        return mcq(f'Which structure corresponds to {good}?', f, r.sample(others, 3), f'{good} = {f}.', r)
    return g, h


# ---------------------------------------------------------------- unit 7: alcohols, phenols and ethers

ALC_NAMES = [('CH₃CH(OH)CH₃', 'propan-2-ol', ['propan-1-ol', '2-propanol-1', 'propanol-2-ene']),
             ('(CH₃)₃COH', '2-methylpropan-2-ol', ['2-methylpropan-1-ol', '1,1-dimethylethanol', 'butan-2-ol']),
             ('CH₃CH₂CH(OH)CH₃', 'butan-2-ol', ['butan-3-ol', 'butan-1-ol', '2-methylpropan-1-ol']),
             ('HOCH₂CH₂OH', 'ethane-1,2-diol', ['ethane-1,1-diol', 'ethanediol-1,2-ene', 'propane-1,2-diol']),
             ('CH₂=CHCH₂OH', 'prop-2-en-1-ol', ['prop-1-en-3-ol', 'propen-1-ol-2', 'prop-2-en-2-ol']),
             ('C₆H₅CH₂OH', 'phenylmethanol', ['phenol', '2-methylphenol', 'phenylethanol']),
             ('(CH₃)₂CHCH₂OH', '2-methylpropan-1-ol', ['2-methylpropan-2-ol', '1-methylpropan-1-ol', 'butan-2-ol']),
             ('CH₃CH(OH)CH₂CH(CH₃)₂', '4-methylpentan-2-ol', ['2-methylpentan-4-ol', '4-methylpentan-1-ol', '4,4-dimethylbutan-2-ol']),
             ('HOCH₂CH(OH)CH₂OH', 'propane-1,2,3-triol', ['propane-1,1,3-triol', 'propan-1,2,3-ol', 'butane-1,2,3-triol']),
             ('o-CH₃C₆H₄OH', '2-methylphenol', ['3-methylphenol', '4-methylphenol', 'phenylmethanol']),
             ('m-C₆H₄(OH)₂', 'benzene-1,3-diol', ['benzene-1,2-diol', 'benzene-1,4-diol', 'cyclohexane-1,3-diol']),
             ('p-C₆H₄(OH)₂', 'benzene-1,4-diol', ['benzene-1,3-diol', 'benzene-1,2-diol', '4-hydroxyphenol-1'])]
alc_name, alc_struct = name_mcq(ALC_NAMES)

ALC_PREP = [('propene', 'H₂O in the presence of dilute H₂SO₄', 'propan-2-ol', "acid-catalysed hydration follows Markovnikov's rule"),
            ('propene', 'B₂H₆, then H₂O₂/NaOH', 'propan-1-ol', 'hydroboration–oxidation gives the anti-Markovnikov alcohol'),
            ('ethanal', 'H₂ over Pd (or NaBH₄)', 'ethanol', 'reduction of an aldehyde gives a primary alcohol'),
            ('propanone', 'NaBH₄', 'propan-2-ol', 'reduction of a ketone gives a secondary alcohol'),
            ('methanal', 'CH₃MgBr, then H₂O', 'ethanol', 'methanal with a Grignard reagent gives a primary alcohol'),
            ('ethanal', 'CH₃MgBr, then H₂O', 'propan-2-ol', 'other aldehydes give secondary alcohols with Grignard reagents'),
            ('propanone', 'CH₃MgBr, then H₂O', '2-methylpropan-2-ol', 'ketones give tertiary alcohols with Grignard reagents'),
            ('ethanoic acid', 'LiAlH₄, then H₂O', 'ethanol', 'LiAlH₄ reduces carboxylic acids to primary alcohols'),
            ('chlorobenzene', 'NaOH at 623 K and 300 atm, then dilute HCl', 'phenol', 'Dow process'),
            ('benzenesulphonic acid', 'fusion with NaOH, then acid', 'phenol', 'phenol from sulphonic acid'),
            ('benzenediazonium chloride', 'warm water', 'phenol', 'hydrolysis of the diazonium salt'),
            ('cumene', 'O₂ (air), then dilute acid', 'phenol (with propanone)', 'cumene hydroperoxide rearranges in acid')]
alc_prep = table_mcq(ALC_PREP, 'What is the main product when {a} is treated with {b}?')
alc_prep_x = table_explain(ALC_PREP, 'Write the product formed when {a} is treated with {b}, and name the process or principle.')

PHENOL_RX = [('phenol', 'bromine water', '2,4,6-tribromophenol (white precipitate)', 'the –OH group strongly activates the ring'),
             ('phenol', 'Br₂ in CS₂ at low temperature', 'a mixture of o- and p-bromophenol', 'in a non-polar solvent at low temperature monobromination occurs'),
             ('phenol', 'dilute HNO₃ at 298 K', 'a mixture of o- and p-nitrophenol', 'the –OH group is o/p-directing'),
             ('phenol', 'concentrated HNO₃', '2,4,6-trinitrophenol (picric acid)', 'trinitration of the strongly activated ring'),
             ('sodium phenoxide', 'CO₂ at 400 K and 4–7 atm, then H⁺', 'salicylic acid (2-hydroxybenzoic acid)', 'Kolbe reaction'),
             ('phenol', 'CHCl₃ and aqueous NaOH, then H⁺', 'salicylaldehyde (2-hydroxybenzaldehyde)', 'Reimer–Tiemann reaction'),
             ('phenol', 'zinc dust (heat)', 'benzene', 'reduction of phenol by zinc dust'),
             ('phenol', 'Na₂Cr₂O₇ with H₂SO₄', 'benzoquinone', 'oxidation of phenol'),
             ('ethanol', 'conc. H₂SO₄ at 443 K', 'ethene', 'acid-catalysed dehydration'),
             ('ethanol', 'PCC', 'ethanal', 'mild oxidation of a 1° alcohol stops at the aldehyde'),
             ('propan-2-ol', 'Cu at 573 K', 'propanone', 'dehydrogenation of a 2° alcohol'),
             ('2-methylpropan-2-ol', 'Cu at 573 K', '2-methylpropene', 'a 3° alcohol undergoes dehydration'),
             ('ethanol', 'ethanoic acid with a few drops of conc. H₂SO₄', 'ethyl ethanoate', 'esterification'),
             ('ethanol', 'sodium metal', 'sodium ethoxide and H₂', 'alcohols are weakly acidic')]
phenol_rx = table_mcq(PHENOL_RX, 'What is the main product when {a} reacts with {b}?')
phenol_rx_x = table_explain(PHENOL_RX, 'Write the main product when {a} reacts with {b}, and name the reaction or give the reason.')

PKA = [('phenol', 10.0), ('o-nitrophenol', 7.2), ('m-nitrophenol', 8.3), ('p-nitrophenol', 7.1), ('o-cresol', 10.2), ('m-cresol', 10.1),
       ('2,4,6-trinitrophenol', 0.5), ('ethanol', 15.9), ('2,4-dinitrophenol', 4.0)]


def acid_pick(r):
    sub = r.sample(PKA, 4)
    mode = r.choice(['most', 'least'])
    best = min(sub, key=lambda x: x[1]) if mode == 'most' else max(sub, key=lambda x: x[1])
    wrong = [x[0] for x in sub if x is not best]
    tab = ', '.join(f'{x[0]} {x[1]}' for x in sub)
    return mcq(f'Given the pKa values {tab}, which compound is the {mode} acidic?', best[0], wrong,
               f'Lower pKa means stronger acid: {best[0]} (pKa {best[1]}) is the {mode} acidic.', r)


def ka_from_pka(r):
    s, p = r.choice([x for x in PKA if x[1] > 1])
    c = r.choice([0.1, 0.01, 0.05])
    Ka = 10 ** -p
    if math.sqrt(Ka / c) > 0.1:
        raise ValueError('approximation not valid')
    pH = 0.5 * (p - math.log10(c))
    return {'stem': f'The pKa of {s} is {p}. Calculate its Ka and the pH of a {c} M aqueous solution (assume weak acid, α ≪ 1).',
            'answer': f'Ka = {sci(Ka, 2)}; pH = {pH:.2f}',
            'key': f'Ka = 10^(−pKa) = {sci(Ka, 2)} (1); pH = ½(pKa − log c) = ½({p} − log {c}) = {pH:.2f} (2).',
            'distractors': [f'Ka = {sci(Ka, 2)}; pH = {p - math.log10(c):.2f}', f'Ka = {sci(10 ** p if p < 10 else Ka * 10, 2)}; pH = {pH:.2f}', f'Ka = {sci(Ka, 2)}; pH = {0.5 * p:.2f}']}


GLUC = 180.0
ETH = 46.0


def ferment(r):
    m = r.choice([0.9, 1.8, 3.6, 4.5, 9.0, 18.0, 45.0])
    eff = r.choice([100, 90, 80, 75])
    n = m * 1000 / GLUC
    me = n * 2 * ETH * eff / 100 / 1000
    vco2 = n * 2 * 22.7 * eff / 100
    who = name(r)
    return {'stem': f'At a sugar mill near Kolhapur, {who} ferments {m} kg of glucose with yeast (zymase): C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂. If the yield is {eff}%, calculate the mass of ethanol formed and the volume of CO₂ at STP (22.7 L mol⁻¹).',
            'answer': f'{sf(me, 3)} kg ethanol; {sf(vco2, 3)} L CO₂',
            'key': f'n(glucose) = {m * 1000:g}/180 = {sf(n, 3)} mol (1); ethanol = 2 × {sf(n, 3)} × 46 × {eff}% = {sf(me, 3)} kg (1); CO₂ = 2 × {sf(n, 3)} × 22.7 × {eff}% = {sf(vco2, 3)} L (1).',
            'distractors': [f'{sf(me / 2, 3)} kg ethanol; {sf(vco2 / 2, 3)} L CO₂', f'{sf(n * 2 * ETH / 1000, 3)} kg ethanol; {sf(n * 2 * 22.4, 3)} L CO₂' if eff != 100 else f'{sf(me * 0.9, 3)} kg ethanol; {sf(vco2 * 0.9, 3)} L CO₂', f'{sf(m * 46 / 180, 3)} kg ethanol; {sf(n * 22.7, 3)} L CO₂']}


ETHER_NAMES = [('CH₃OCH₂CH₃', 'methoxyethane', ['ethoxymethane', 'propan-2-ol', 'methyl ethanol']),
               ('C₆H₅OCH₃', 'methoxybenzene', ['phenylmethanol', 'methylphenol', 'benzyl methyl ether-1']),
               ('C₂H₅OC₂H₅', 'ethoxyethane', ['diethoxy', 'butan-2-ol', 'ethoxyethanol']),
               ('(CH₃)₂CHOCH₃', '2-methoxypropane', ['1-methoxypropane', '2-methoxy-2-methylethane', 'propoxymethane']),
               ('C₆H₅OCH₂CH₃', 'ethoxybenzene', ['phenoxyethanol', '2-ethylphenol', 'methoxytoluene']),
               ('CH₃OCH₂CH₂OCH₃', '1,2-dimethoxyethane', ['1,1-dimethoxyethane', 'dimethoxypropane', 'ethane-1,2-diol dimethyl-1']),
               ('(CH₃)₃COCH₃', '2-methoxy-2-methylpropane', ['1-methoxybutane', '2-methoxybutane', 'tert-butoxymethane-2'])]
ether_name, ether_struct = name_mcq(ETHER_NAMES)

WILLIAMSON = [('2-methoxy-2-methylpropane', '(CH₃)₃CONa + CH₃Br', '(CH₃)₃CBr + CH₃ONa', 'a 3° halide with a strong base gives elimination (2-methylpropene)'),
              ('methoxyethane', 'CH₃CH₂ONa + CH₃Br (or CH₃ONa + CH₃CH₂Br)', 'CH₃CH₂OH + CH₃OH with conc. H₂SO₄ at 413 K', 'both halides are primary/methyl, so SN2 works either way'),
              ('anisole (methoxybenzene)', 'C₆H₅ONa + CH₃Br', 'C₆H₅Br + CH₃ONa', 'aryl halides do not undergo SN2'),
              ('ethoxybenzene', 'C₆H₅ONa + CH₃CH₂Br', 'C₆H₅Br + CH₃CH₂ONa', 'aryl halides do not undergo SN2'),
              ('2-ethoxy-2-methylpropane', '(CH₃)₃CONa + CH₃CH₂Br', '(CH₃)₃CBr + CH₃CH₂ONa', 'tertiary halides give alkenes with alkoxides'),
              ('1-ethoxypropane', 'CH₃CH₂CH₂ONa + CH₃CH₂Br', 'CH₃CH₂CH₂OH + CH₃CH₂OH (H⁺, 413 K)', 'acid dehydration of two different alcohols gives a mixture')]


def williamson(r):
    e, good, bad, why = r.choice(WILLIAMSON)
    others = [x[2] for x in WILLIAMSON if x[0] != e] + ['CH₃OH + CH₃CH₂OH with conc. H₂SO₄ at 443 K']
    return mcq(f'Which pair of reactants is best for preparing {e} by Williamson synthesis?', good, [bad] + r.sample([o for o in others if o != bad], 2),
               f'{good}: the alkyl halide should be primary (or methyl) for SN2; {why}.', r)


ETHER_RX = [('methoxyethane', 'excess HI (heat)', 'iodomethane and ethanol', 'I⁻ attacks the less hindered methyl group (SN2)'),
            ('anisole', 'HI (heat)', 'phenol and iodomethane', 'the aryl–O bond has partial double bond character and is not cleaved'),
            ('2-methoxy-2-methylpropane', 'HI', '2-iodo-2-methylpropane and methanol', 'a stable 3° carbocation forms (SN1)'),
            ('anisole', 'Br₂ in ethanoic acid', '4-bromoanisole (major)', 'the –OCH₃ group is o/p-directing and activating'),
            ('anisole', 'CH₃COCl with anhydrous AlCl₃', '4-methoxyacetophenone (major)', 'Friedel–Crafts acylation at the para position'),
            ('anisole', 'conc. HNO₃ + conc. H₂SO₄', '4-nitroanisole (major) and 2-nitroanisole', 'nitration at o/p positions'),
            ('ethoxyethane', 'excess hot conc. HI', 'iodoethane (2 mol)', 'both C–O bonds are cleaved')]
ether_rx = table_mcq(ETHER_RX, 'What are the main products when {a} reacts with {b}?')

CH7S1 = {
    'topic': 'nomenclature and preparation of alcohols and phenols',
    'terms': [('a primary alcohol', 'an alcohol in which the –OH group is attached to a carbon bonded to one other carbon'),
              ('a tertiary alcohol', 'an alcohol in which the –OH group is attached to a carbon bonded to three other carbons'),
              ('hydroboration–oxidation', 'the addition of diborane to an alkene followed by oxidation with alkaline H₂O₂ to give an anti-Markovnikov alcohol'),
              ('the cumene process', 'the industrial preparation of phenol from cumene via cumene hydroperoxide, with propanone as by-product'),
              ('a Grignard reagent', 'an alkylmagnesium halide that adds to carbonyl compounds to give alcohols after hydrolysis'),
              ('an allylic alcohol', 'an alcohol in which –OH is on an sp³ carbon next to a C=C double bond')],
    'groups': [('a primary alcohol', ['ethanol', 'propan-1-ol', '2-methylpropan-1-ol', 'phenylmethanol']), ('a secondary alcohol', ['propan-2-ol', 'butan-2-ol', 'cyclohexanol']),
               ('a tertiary alcohol', ['2-methylpropan-2-ol', '2-methylbutan-2-ol', '1-methylcyclohexanol']), ('a phenol', ['2-methylphenol', 'benzene-1,3-diol', '4-nitrophenol'])],
    'tf': (['Methanal gives a primary alcohol with a Grignard reagent.', 'Ketones give tertiary alcohols with Grignard reagents.', 'Hydroboration–oxidation of propene gives propan-1-ol.',
            'Phenol is made commercially from cumene.', 'In alcohols the C–O–H bond angle is slightly less than tetrahedral.'],
           [('Hydration of propene in acid gives propan-1-ol.', 'It follows Markovnikov\'s rule and gives propan-2-ol.'),
            ('Reduction of propanone gives propan-1-ol.', 'Reduction of a ketone gives a secondary alcohol, propan-2-ol.'),
            ('In phenol the C–O bond is longer than in methanol.', 'The C–O bond in phenol is shorter, due to partial double bond character and the sp² carbon.'),
            ('Ethanal gives a tertiary alcohol with CH₃MgBr.', 'Ethanal gives a secondary alcohol, propan-2-ol.')]),
    'ar': [('The C–O bond length in phenol is less than that in methanol.', 'In phenol the lone pair on oxygen is in conjugation with the ring, giving partial double bond character.', 'a', 'Also the carbon is sp².'),
           ('Propene gives propan-1-ol on hydroboration–oxidation.', 'Boron adds to the less substituted carbon of the double bond.', 'a', 'Anti-Markovnikov orientation.'),
           ('Methanal and CH₃MgBr give a tertiary alcohol.', 'Methanal has no alkyl groups on the carbonyl carbon.', 'd', 'It gives ethanol, a primary alcohol; the reason is true.')],
    'fams': [F('C2', 'D2', 'mcq', alc_name), F('C2', 'D1', 'mcq', alc_struct), F('C3', 'D3', 'mcq', alc_prep), F('C4', 'D4', 'explain', alc_prep_x)],
    'qa': [('C4', 'D4', 'explain', 'Show how propan-2-ol and 2-methylpropan-2-ol can be prepared using Grignard reagents.',
            'Propan-2-ol: CH₃CHO + CH₃MgBr → (CH₃)₂CHOMgBr → (H₂O) (CH₃)₂CHOH. 2-Methylpropan-2-ol: CH₃COCH₃ + CH₃MgBr → (CH₃)₃COMgBr → (H₂O) (CH₃)₃COH.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'Anil prepares phenol by the cumene process in a project report.\n(i) Write the starting material and the intermediate. (1 mark)\n(ii) What is the by-product and why is it useful? (1 mark)\n(iii) Give two other laboratory methods to make phenol. (2 marks)',
            '(i) Cumene (isopropylbenzene); cumene hydroperoxide. (ii) Propanone (acetone), a valuable solvent. (iii) From chlorobenzene (NaOH, 623 K, 300 atm) or from benzenesulphonic acid (NaOH fusion) or from benzenediazonium chloride (warm water).',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH7S2 = {
    'topic': 'properties of alcohols and phenols; acidity',
    'terms': [('Lucas test', 'a test with conc. HCl and anhydrous ZnCl₂ in which 3° alcohols give immediate turbidity, 2° in about five minutes and 1° only on heating'),
              ('the Kolbe reaction', 'the reaction of sodium phenoxide with CO₂ under pressure to give salicylic acid'),
              ('the Reimer–Tiemann reaction', 'the reaction of phenol with chloroform and NaOH that introduces a –CHO group at the ortho position'),
              ('esterification', 'the reaction of an alcohol or phenol with a carboxylic acid, acid chloride or anhydride to form an ester'),
              ('the phenoxide ion', 'the anion C₆H₅O⁻, stabilised by delocalisation of the negative charge into the ring')],
    'tf': (['Phenol is more acidic than ethanol.', 'o-Nitrophenol is steam volatile due to intramolecular hydrogen bonding.', 'Boiling points of alcohols decrease with branching.',
            'Electron-withdrawing groups increase the acidity of phenol.', 'Tertiary alcohols react fastest with the Lucas reagent.'],
           [('Ethanol is more acidic than phenol.', 'Phenol is more acidic; the phenoxide ion is resonance-stabilised.'),
            ('p-Nitrophenol is steam volatile because of intramolecular hydrogen bonding.', 'o-Nitrophenol is steam volatile; p-nitrophenol forms intermolecular hydrogen bonds.'),
            ('Electron-donating groups such as –CH₃ increase the acidity of phenol.', 'They decrease acidity; cresols are weaker acids than phenol.'),
            ('Primary alcohols give immediate turbidity with Lucas reagent.', 'Tertiary alcohols give immediate turbidity; primary alcohols react only on heating.')]),
    'orders': [('order of acid strength', ['ethanol', 'p-cresol', 'phenol', 'p-nitrophenol', '2,4,6-trinitrophenol'], 'Electron-withdrawing –NO₂ stabilises the phenoxide; –CH₃ destabilises it; alkoxide has no resonance.', '<'),
               ('order of boiling point', ['butane', 'methoxyethane', 'propanal', 'propan-1-ol'], 'Intermolecular hydrogen bonding in alcohols gives the highest boiling point.', '<'),
               ('order of reactivity with Lucas reagent', ['2-methylpropan-2-ol', 'butan-2-ol', 'butan-1-ol'], 'Stability of the carbocation: 3° > 2° > 1°.', '>'),
               ('order of acidity of alcohols', ['methanol', 'ethanol', 'propan-2-ol', '2-methylpropan-2-ol'], 'Alkyl groups (+I) destabilise the alkoxide ion.', '>')],
    'ar': [('Phenol is more acidic than ethanol.', 'The phenoxide ion is stabilised by resonance, but the ethoxide ion is not.', 'a', 'Delocalisation of the negative charge.'),
           ('o-Nitrophenol has a lower boiling point than p-nitrophenol.', 'o-Nitrophenol has intramolecular hydrogen bonding.', 'a', 'p-Isomer has intermolecular H-bonding and higher b.p.'),
           ('Alcohols have higher boiling points than ethers of comparable mass.', 'Alcohols form intermolecular hydrogen bonds.', 'a', 'Extra energy is needed to break the H-bonds.'),
           ('Phenol reacts with bromine water to give a white precipitate.', 'The –OH group deactivates the benzene ring.', 'c', 'The –OH group strongly activates the ring, giving 2,4,6-tribromophenol.')],
    'fams': [F('C3', 'D3', 'mcq', phenol_rx), F('C3', 'D2', 'explain', phenol_rx_x), F('C3', 'D3', 'mcq', acid_pick), F('C4', 'D4', 'multi_step', ka_from_pka)],
    'qa': [('C4', 'D4', 'explain', 'Explain why the presence of a nitro group at the ortho or para position increases the acidity of phenol.',
            'The –NO₂ group withdraws electrons by –R and –I effects; at o/p positions the negative charge of the phenoxide ion is delocalised onto the nitro group, which stabilises the ion and makes the release of H⁺ easier.',
            '1 mark effect; 1 mark stabilisation of phenoxide.'),
           ('C4', 'D5', 'long', 'How are the following conversions carried out? Write equations. (i) Phenol to salicylic acid, (ii) phenol to salicylaldehyde, (iii) phenol to picric acid, (iv) propan-2-ol to propanone, (v) ethanol to ethene.',
            '(i) Kolbe: C₆H₅ONa + CO₂ (400 K, 4–7 atm) then H⁺. (ii) Reimer–Tiemann: CHCl₃ + aq. NaOH, then H⁺. (iii) Conc. HNO₃ (better: sulphonation then nitration). (iv) Cu at 573 K (or acidified K₂Cr₂O₇). (v) Conc. H₂SO₄ at 443 K.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'Tanvi is given three unlabelled alcohols of formula C₄H₁₀O: butan-1-ol, butan-2-ol and 2-methylpropan-2-ol. She adds Lucas reagent to each.\n(i) What is Lucas reagent? (1 mark)\n(ii) Predict the observation for each. (2 marks)\n(iii) Explain the order of reactivity. (1 mark)',
            '(i) Conc. HCl with anhydrous ZnCl₂. (ii) 2-Methylpropan-2-ol: turbidity at once; butan-2-ol: turbidity in about 5 minutes; butan-1-ol: no turbidity at room temperature. (iii) Reaction goes via carbocations; stability 3° > 2° > 1°.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH7S3 = {
    'topic': 'commercially important alcohols',
    'terms': [('wood spirit', 'methanol, which was formerly obtained by destructive distillation of wood'),
              ('denatured alcohol', 'ethanol made unfit for drinking by adding copper sulphate and pyridine'),
              ('fermentation', 'the slow breakdown of sugars into ethanol and CO₂ by enzymes from yeast'),
              ('invertase', 'the yeast enzyme that hydrolyses sucrose into glucose and fructose'),
              ('zymase', 'the yeast enzyme that converts glucose and fructose into ethanol and carbon dioxide')],
    'tf': (['Methanol is made industrially from CO and H₂ over a ZnO–Cr₂O₃ catalyst.', 'Drinking even small amounts of methanol can cause blindness.', 'Ethanol is obtained commercially by fermentation of molasses.',
            'Air is kept out during fermentation.', 'Commercial ethanol is denatured by adding copper sulphate and pyridine.'],
           [('Fermentation is carried out in the presence of plenty of air.', 'Air is excluded; with oxygen ethanol is oxidised to ethanoic acid.'),
            ('Methanol is safe to drink in small amounts.', 'Methanol is highly poisonous and can cause blindness and death.'),
            ('Zymase converts sucrose directly into ethanol.', 'Invertase first hydrolyses sucrose; zymase then converts glucose and fructose into ethanol.'),
            ('Denatured alcohol is made by adding sugar to ethanol.', 'Copper sulphate (colour) and pyridine (smell) are added.')]),
    'orders': [('sequence in the manufacture of ethanol from molasses', ['sucrose (molasses)', 'glucose + fructose (invertase)', 'ethanol + CO₂ (zymase)'], 'Invertase hydrolyses sucrose; zymase ferments the hexoses.', '→')],
    'ar': [('Fermentation for ethanol is carried out in the absence of air.', 'In the presence of air ethanol is oxidised to ethanoic acid.', 'a', 'Sour taste of spoiled wine.'),
           ('Commercial alcohol is coloured blue and has a foul smell.', 'Copper sulphate and pyridine are added to it.', 'a', 'Denatured alcohol cannot be drunk.')],
    'features': {'intro': 'An important alcohol has these features:', 'q': 'Identify the alcohol', 'what': 'alcohol', 'long': False,
                 'items': [('methanol', ['called wood spirit', 'made from CO and H₂ at 573–673 K over ZnO–Cr₂O₃', 'used as a solvent and to make methanal', 'highly poisonous, can cause blindness']),
                           ('ethanol', ['made by fermentation of molasses', 'enzymes invertase and zymase are used', 'denatured with CuSO₄ and pyridine', 'used in beverages, as solvent and as fuel']),
                           ('glycerol (propane-1,2,3-triol)', ['by-product of soap manufacture', 'has three –OH groups', 'very viscous with a high boiling point', 'used in cosmetics and to make nitroglycerine'])]},
    'fams': [F('C3', 'D3', 'numerical', ferment), F('C4', 'D4', 'multi_step', ferment)],
    'qa': [('C3', 'D2', 'explain', 'Write the equations for the preparation of methanol from synthesis gas and of ethanol from sucrose.',
            'CO + 2H₂ → CH₃OH (ZnO–Cr₂O₃, 200–300 atm, 573–673 K). C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ + C₆H₁₂O₆ (invertase); C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂ (zymase).',
            '1 mark each.'),
           ('C1', 'D2', 'short', 'What is denatured alcohol?', 'Ethanol made unfit for drinking by adding copper sulphate and pyridine.', '1 mark.')],
}

CH7S4 = {
    'topic': 'ethers',
    'terms': [('Williamson synthesis', 'the preparation of ethers by the reaction of an alkyl halide with a sodium alkoxide or phenoxide'),
              ('a symmetrical ether', 'an ether in which both alkyl or aryl groups attached to oxygen are the same'),
              ('an unsymmetrical ether', 'an ether in which the two groups attached to oxygen are different'),
              ('anisole', 'methoxybenzene, C₆H₅OCH₃'),
              ('cleavage of ethers', 'the breaking of the C–O bond of ethers by hot concentrated HI or HBr')],
    'tf': (['Williamson synthesis works best with primary alkyl halides.', 'Ethers have lower boiling points than isomeric alcohols.', 'The C–O–C bond angle in ethers is a little more than tetrahedral.',
            'Anisole gives phenol and iodomethane with HI.', 'The methoxy group activates the benzene ring.'],
           [('Tertiary alkyl halides give good yields of ethers in Williamson synthesis.', 'With alkoxides tertiary halides undergo elimination to alkenes.'),
            ('Anisole gives iodobenzene and methanol with HI.', 'It gives phenol and iodomethane; the aryl–O bond is not broken.'),
            ('Ethers are more soluble in water than alcohols of similar mass.', 'They are similar in solubility to alcohols for small members but cannot donate H-bonds; boiling points are much lower.'),
            ('The methoxy group is meta-directing.', 'It is o/p-directing and activating.')]),
    'ar': [('Ethers have lower boiling points than isomeric alcohols.', 'Ethers cannot form intermolecular hydrogen bonds.', 'a', 'No O–H group.'),
           ('Anisole reacts with HI to give phenol and iodomethane.', 'The aryl carbon–oxygen bond has partial double bond character.', 'a', 'So only the methyl–O bond is broken.'),
           ('(CH₃)₃C–O–CH₃ gives (CH₃)₃CI and CH₃OH with HI.', 'The reaction proceeds by SN1 via the stable tertiary carbocation.', 'a', 'Stable 3° carbocation forms.'),
           ('2-Methoxy-2-methylpropane can be made from (CH₃)₃CBr and CH₃ONa.', 'Tertiary halides undergo elimination with strong bases.', 'd', 'Elimination gives 2-methylpropene; the reason is true.')],
    'fams': [F('C2', 'D2', 'mcq', ether_name), F('C2', 'D1', 'mcq', ether_struct), F('C3', 'D3', 'mcq', williamson), F('C3', 'D3', 'mcq', ether_rx)],
    'qa': [('C4', 'D4', 'explain', 'Of the two ways of making 2-methoxy-2-methylpropane by Williamson synthesis, which is correct? Explain with equations.',
            '(CH₃)₃CONa + CH₃Br → (CH₃)₃COCH₃ + NaBr. The alternative (CH₃)₃CBr + CH₃ONa gives mainly 2-methylpropene because the 3° halide undergoes elimination with the strong base.',
            '1 mark correct pair; 1 mark reason with equation.'),
           ('C4', 'D5', 'long', 'Write equations for (i) Williamson synthesis of ethoxyethane, (ii) reaction of methoxyethane with HI, (iii) bromination of anisole, (iv) Friedel–Crafts methylation of anisole, (v) nitration of anisole.',
            '(i) C₂H₅ONa + C₂H₅Br → C₂H₅OC₂H₅ + NaBr. (ii) CH₃OC₂H₅ + HI → CH₃I + C₂H₅OH. (iii) Br₂ in CH₃COOH → 4-bromoanisole (major) + 2-bromoanisole. (iv) CH₃Cl/AlCl₃ → 2- and 4-methoxytoluene. (v) Conc. HNO₃/H₂SO₄ → 4-nitroanisole (major) + 2-nitroanisole.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'Rakesh heats methoxyethane and, separately, anisole with hydrogen iodide.\n(i) Write the products in each case. (2 marks)\n(ii) Why does anisole not give iodobenzene? (1 mark)\n(iii) Which product forms from tert-butyl methyl ether, and by which mechanism? (1 mark)',
            '(i) Methoxyethane: CH₃I + C₂H₅OH; anisole: C₆H₅OH + CH₃I. (ii) The C(aryl)–O bond has partial double bond character and the sp² carbon resists SN attack. (iii) (CH₃)₃CI + CH₃OH by SN1.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',))],
}

# ---------------------------------------------------------------- unit 8: aldehydes, ketones and carboxylic acids

CO_NAMES = [('CH₃CH₂COCH₃', 'butan-2-one', ['butan-3-one', 'butanal', '2-methylpropanal']),
            ('C₆H₅COCH₃', '1-phenylethanone', ['2-phenylethanal', 'phenylmethanal', '1-phenylpropanone']),
            ('CH₃CH=CHCHO', 'but-2-enal', ['but-3-enal', 'but-2-en-1-one', 'butanal']),
            ('(CH₃)₂CHCHO', '2-methylpropanal', ['2-methylpropan-1-one', 'butanal', '1-methylpropanal']),
            ('CH₃COCH₂COCH₃', 'pentane-2,4-dione', ['pentane-1,3-dione', 'pentan-2,4-one', 'hexane-2,4-dione']),
            ('C₆H₅COC₆H₅', 'diphenylmethanone', ['diphenylmethanal', '1,1-diphenylethanone', 'benzophenol']),
            ('OHC–CHO', 'ethanedial', ['ethanal', 'ethane-1,2-dione', 'oxalic acid']),
            ('CH₃CH(CH₃)CH₂COCH₃', '4-methylpentan-2-one', ['2-methylpentan-4-one', '4-methylpentanal', '4,4-dimethylbutan-2-one']),
            ('(CH₃)₂C=CHCOCH₃', '4-methylpent-3-en-2-one', ['2-methylpent-2-en-4-one', '4-methylpent-2-en-2-one', '4-methylpent-3-enal']),
            ('CH₃CH(Br)CH₂CHO', '3-bromobutanal', ['2-bromobutanal', '3-bromobutan-1-one', '1-bromobutanal']),
            ('CH₃COOCH₂CH₃', 'ethyl ethanoate', ['ethyl methanoate', 'methyl propanoate', 'propyl ethanoate']),
            ('HOOC–COOH', 'ethanedioic acid', ['ethanoic acid', 'oxalic aldehyde', 'propanedioic acid'])]
co_name, co_struct = name_mcq(CO_NAMES)

CO_PREP = [('benzoyl chloride', 'H₂ over Pd–BaSO₄', 'benzaldehyde', 'Rosenmund reduction'),
           ('ethanenitrile', 'SnCl₂/HCl, then H₃O⁺', 'ethanal', 'Stephen reaction'),
           ('ethyl ethanoate', 'DIBAL-H, then H₂O', 'ethanal', 'DIBAL-H reduces esters to aldehydes'),
           ('toluene', 'CrO₂Cl₂ in CS₂, then H₃O⁺', 'benzaldehyde', 'Etard reaction'),
           ('benzene', 'CO and HCl with anhydrous AlCl₃/CuCl', 'benzaldehyde', 'Gatterman–Koch reaction'),
           ('ethanenitrile', 'C₂H₅MgBr, then H₃O⁺', 'butan-2-one', 'Grignard reagents with nitriles give ketones'),
           ('benzene', 'CH₃COCl with anhydrous AlCl₃', 'acetophenone (1-phenylethanone)', 'Friedel–Crafts acylation'),
           ('ethanoyl chloride', 'dimethylcadmium', 'propanone', 'acyl chlorides with dialkylcadmium give ketones'),
           ('ethyne', 'H₂O with HgSO₄/H₂SO₄', 'ethanal', 'hydration of ethyne'),
           ('propan-2-ol', 'Cu at 573 K', 'propanone', 'dehydrogenation of a secondary alcohol'),
           ('but-2-ene', 'O₃, then Zn/H₂O', 'ethanal', 'ozonolysis'),
           ('ethanol', 'PCC', 'ethanal', 'mild oxidation of a primary alcohol')]
co_prep = table_mcq(CO_PREP, 'What is the product when {a} is treated with {b}?')
co_prep_x = table_explain(CO_PREP, 'Name the product and the reaction when {a} is treated with {b}.')

CO_RX = [('ethanal', 'HCN', 'ethanal cyanohydrin (2-hydroxypropanenitrile)', 'nucleophilic addition of CN⁻'),
         ('propanone', 'NaHSO₃', 'the bisulphite addition compound', 'nucleophilic addition; used to separate carbonyl compounds'),
         ('propanone', 'NH₂OH', 'propanone oxime', 'addition–elimination with hydroxylamine'),
         ('ethanal', 'C₆H₅NHNH₂', 'ethanal phenylhydrazone', 'addition–elimination with phenylhydrazine'),
         ('propanone', 'semicarbazide (H₂NNHCONH₂)', 'propanone semicarbazone', 'addition–elimination'),
         ('propanone', 'Zn–Hg with conc. HCl', 'propane', 'Clemmensen reduction'),
         ('propanone', 'NH₂NH₂, then KOH in ethylene glycol (heat)', 'propane', 'Wolff–Kishner reduction'),
         ('ethanal', 'dilute NaOH', '3-hydroxybutanal (aldol)', 'aldol condensation; ethanal has α-hydrogens'),
         ('methanal', 'concentrated KOH', 'methanol and potassium methanoate', 'Cannizzaro reaction; methanal has no α-hydrogen'),
         ('benzaldehyde', 'concentrated NaOH', 'benzyl alcohol and sodium benzoate', 'Cannizzaro reaction'),
         ('ethanal', "Tollens' reagent", 'ethanoate ion and a silver mirror', 'aldehydes reduce Tollens\' reagent'),
         ('ethanal', "Fehling's solution", 'ethanoate ion and a red-brown precipitate of Cu₂O', 'aliphatic aldehydes reduce Fehling\'s solution'),
         ('propanone', 'NaOI (I₂ + NaOH)', 'iodoform (yellow precipitate) and sodium ethanoate', 'methyl ketones give the iodoform test'),
         ('benzaldehyde', 'conc. HNO₃ + conc. H₂SO₄', '3-nitrobenzaldehyde', 'the –CHO group is meta-directing')]
co_rx = table_mcq(CO_RX, 'What is formed when {a} reacts with {b}?')
co_rx_x = table_explain(CO_RX, 'What is formed when {a} reacts with {b}? Name the reaction or give the reason.')

DISTINGUISH = [('ethanal', 'propanone', "Tollens' test (silver mirror with ethanal only)"),
               ('propanal', 'propanone', "Fehling's test (red precipitate with propanal only)"),
               ('pentan-2-one', 'pentan-3-one', 'iodoform test (yellow precipitate with pentan-2-one only)'),
               ('ethanal', 'methanal', 'iodoform test (positive with ethanal only)'),
               ('benzaldehyde', 'ethanal', "Fehling's test (positive with ethanal only)"),
               ('benzaldehyde', 'acetophenone', "Tollens' test (silver mirror with benzaldehyde only)"),
               ('phenol', 'benzoic acid', 'NaHCO₃ test (effervescence with benzoic acid only)'),
               ('ethanol', 'methanol', 'iodoform test (yellow precipitate with ethanol only)'),
               ('propan-2-ol', 'propan-1-ol', 'iodoform test (positive with propan-2-ol only)')]
TESTS = ["Tollens' test (silver mirror with the aldehyde)", "Fehling's test (red precipitate with the aliphatic aldehyde)", 'iodoform test (yellow precipitate)',
         'NaHCO₃ test (effervescence of CO₂)', 'Lucas test (turbidity)', 'ferric chloride test (violet colour)']


def distinguish(r):
    a, b, t = r.choice(DISTINGUISH)
    base = t.split(' (')[0]
    wrong = [x for x in TESTS if x.split(' (')[0] != base]
    return mcq(f'Which test can distinguish {a} from {b}?', t, r.sample(wrong, 3), f'{cap(t)}.', r)


def distinguish_x(r):
    a, b, t = r.choice(DISTINGUISH)
    return {'stem': f'Give a simple chemical test to distinguish between {a} and {b}.', 'answer': cap(t) + '.',
            'key': f'Name of the test and reagent (1); observation for the correct compound (1): {t}.'}


CA_PKA = [('HCOOH', 3.75), ('CH₃COOH', 4.76), ('ClCH₂COOH', 2.86), ('Cl₂CHCOOH', 1.26), ('Cl₃CCOOH', 0.65), ('CF₃COOH', 0.23),
          ('C₆H₅COOH', 4.19), ('4-nitrobenzoic acid', 3.41), ('CH₃CH₂COOH', 4.88)]


def ca_pick(r):
    sub = r.sample(CA_PKA, 4)
    mode = r.choice(['strongest', 'weakest'])
    best = min(sub, key=lambda x: x[1]) if mode == 'strongest' else max(sub, key=lambda x: x[1])
    return mcq(f'Which of the following is the {mode} acid: {", ".join(x[0] for x in r.sample(sub, 4))}?', best[0], [x[0] for x in sub if x is not best],
               f'{best[0]} (pKa {best[1]}) is the {mode}; electron-withdrawing groups increase acid strength, electron-donating groups decrease it.', r)


def ca_ph(r):
    s, p = r.choice([x for x in CA_PKA if x[1] > 2.5])
    c = r.choice([0.1, 0.05, 0.01, 0.2])
    Ka = 10 ** -p
    al = math.sqrt(Ka / c)
    if al > 0.1:
        raise ValueError('approximation not valid')
    pH = 0.5 * (p - math.log10(c))
    return {'stem': f'The pKa of {s} is {p}. Calculate its dissociation constant Ka, the degree of dissociation and the pH of a {c} M solution (assume α ≪ 1).',
            'answer': f'Ka = {sci(Ka, 2)}; α = {sf(al, 2)}; pH = {pH:.2f}',
            'key': f'Ka = 10^(−{p}) = {sci(Ka, 2)} (1); α = √(Ka/c) = {sf(al, 2)} (1); [H⁺] = cα = {sci(c * al, 2)} M, pH = {pH:.2f} (1).',
            'distractors': [f'Ka = {sci(Ka, 2)}; α = {sf(al * al, 2)}; pH = {pH * 2:.2f}', f'Ka = {sci(Ka, 2)}; α = {sf(al, 2)}; pH = {p:.2f}', f'Ka = {sci(Ka * 10, 2)}; α = {sf(al * math.sqrt(10), 2)}; pH = {pH - 0.5:.2f}']}


CA_RX = [('ethanoic acid', 'Cl₂ with red phosphorus', '2-chloroethanoic acid', 'Hell–Volhard–Zelinsky reaction (α-halogenation)'),
         ('sodium ethanoate', 'soda lime (heat)', 'methane', 'decarboxylation'),
         ('ethanoic acid', 'LiAlH₄, then H₂O', 'ethanol', 'reduction to a primary alcohol'),
         ('ethanoic acid', 'PCl₅', 'ethanoyl chloride', 'replacement of –OH by Cl'),
         ('ethanoic acid', 'ethanol with conc. H₂SO₄', 'ethyl ethanoate', 'esterification'),
         ('ethanoic acid', 'NH₃, then heat', 'ethanamide', 'ammonium salt dehydrates to the amide'),
         ('ethanoic acid', 'P₂O₅ (heat)', 'ethanoic anhydride', 'dehydration'),
         ('benzoic acid', 'conc. HNO₃ + conc. H₂SO₄', '3-nitrobenzoic acid', 'the –COOH group is meta-directing'),
         ('toluene', 'alkaline KMnO₄, then H₃O⁺', 'benzoic acid', 'side-chain oxidation'),
         ('CH₃MgBr', 'dry ice (CO₂), then H₃O⁺', 'ethanoic acid', 'carboxylation of a Grignard reagent'),
         ('ethanenitrile', 'H₃O⁺ (heat)', 'ethanoic acid', 'hydrolysis of a nitrile'),
         ('ethanoic acid', 'NaHCO₃', 'sodium ethanoate, CO₂ and water', 'acids are stronger than carbonic acid')]
ca_rx = table_mcq(CA_RX, 'What is the product when {a} is treated with {b}?')
ca_rx_x = table_explain(CA_RX, 'Write the product when {a} is treated with {b}, and name the reaction.')

CH8S1 = {
    'topic': 'nomenclature, structure and preparation of aldehydes and ketones',
    'terms': [('the carbonyl group', 'the C=O group, in which carbon is sp² hybridised and the bond is polar'),
              ('Rosenmund reduction', 'the hydrogenation of an acyl chloride over palladium on barium sulphate to give an aldehyde'),
              ('Stephen reaction', 'the reduction of a nitrile with SnCl₂ and HCl to an imine, which is hydrolysed to an aldehyde'),
              ('Etard reaction', 'the oxidation of toluene with chromyl chloride to give benzaldehyde'),
              ('Gatterman–Koch reaction', 'the formylation of benzene with CO and HCl in the presence of anhydrous AlCl₃/CuCl'),
              ('Friedel–Crafts acylation', 'the reaction of an arene with an acyl chloride and anhydrous AlCl₃ to give an aryl ketone')],
    'groups': [('a method that gives an aldehyde', ['Rosenmund reduction', 'Stephen reaction', 'Etard reaction', 'Gatterman–Koch reaction']),
               ('a method that gives a ketone', ['Friedel–Crafts acylation', 'nitrile + Grignard reagent', 'acyl chloride + dialkylcadmium', 'dehydrogenation of a 2° alcohol'])],
    'tf': (['The carbonyl carbon is sp² hybridised.', 'In Rosenmund reduction, BaSO₄ poisons the catalyst so that the aldehyde is not reduced further.', 'DIBAL-H reduces nitriles and esters to aldehydes.',
            'The C=O bond is polar, with carbon carrying δ⁺.', 'Ketones are prepared from acyl chlorides and dialkylcadmium.'],
           [('Friedel–Crafts acylation of benzene gives benzaldehyde.', 'With CH₃COCl/AlCl₃ it gives acetophenone; benzaldehyde comes from Gatterman–Koch or Etard reaction.'),
            ('The carbonyl carbon is sp³ hybridised.', 'It is sp² hybridised, with a planar trigonal arrangement.'),
            ('Grignard reagents give ketones with dialkylcadmium.', 'Ketones are made from acyl chlorides and dialkylcadmium, or from nitriles and Grignard reagents.'),
            ('Oxidation of a secondary alcohol gives an aldehyde.', 'Secondary alcohols give ketones.')]),
    'ar': [('The carbonyl carbon is electrophilic.', 'Oxygen is more electronegative than carbon and pulls the π electrons.', 'a', 'Carbon carries δ⁺.'),
           ('Rosenmund reduction stops at the aldehyde stage.', 'The Pd catalyst is poisoned with BaSO₄.', 'a', 'Poisoned catalyst prevents further reduction to the alcohol.'),
           ('Etard reaction gives benzoic acid from toluene.', 'Chromyl chloride forms a chromium complex that is hydrolysed to benzaldehyde.', 'd', 'Etard reaction stops at benzaldehyde; the reason is true.')],
    'fams': [F('C2', 'D2', 'mcq', co_name), F('C2', 'D1', 'mcq', co_struct), F('C3', 'D3', 'mcq', co_prep), F('C3', 'D2', 'explain', co_prep_x)],
    'qa': [('C4', 'D4', 'explain', 'How will you convert (i) ethanenitrile to butan-2-one and (ii) toluene to benzaldehyde? Write equations.',
            '(i) CH₃CN + C₂H₅MgBr (dry ether) → imine salt, then H₃O⁺ → CH₃COC₂H₅. (ii) Toluene + CrO₂Cl₂ in CS₂ → chromium complex, then H₃O⁺ → C₆H₅CHO (Etard); or side-chain chlorination to benzal chloride and hydrolysis.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'Meera wants to prepare benzaldehyde in the laboratory without forming benzoic acid.\n(i) Name two reactions she could use starting from toluene and benzene. (2 marks)\n(ii) Why is benzoyl chloride reduced using a poisoned catalyst? (1 mark)\n(iii) Name the reagent that converts an ester directly to an aldehyde. (1 mark)',
            '(i) Etard reaction (toluene + CrO₂Cl₂) and Gatterman–Koch reaction (benzene + CO/HCl, AlCl₃/CuCl). (ii) Pd–BaSO₄ is poisoned so that the aldehyde is not reduced further to the alcohol. (iii) DIBAL-H.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',)),
           ('C1', 'D2', 'short', 'Draw the structure of 4-methylpent-3-en-2-one.', '(CH₃)₂C=CH–CO–CH₃.', '1 mark.')],
}

CH8S2 = {
    'topic': 'reactions of aldehydes and ketones',
    'terms': [('the aldol condensation', 'the reaction of two molecules of an aldehyde or ketone with α-hydrogen in dilute alkali to give a β-hydroxy carbonyl compound'),
              ('the Cannizzaro reaction', 'the self oxidation–reduction of an aldehyde without α-hydrogen in concentrated alkali'),
              ('the Clemmensen reduction', 'the reduction of a carbonyl group to CH₂ with zinc amalgam and concentrated HCl'),
              ('the Wolff–Kishner reduction', 'the reduction of a carbonyl group to CH₂ with hydrazine and KOH in ethylene glycol'),
              ("Tollens' reagent", 'ammoniacal silver nitrate solution, which gives a silver mirror with aldehydes'),
              ('the iodoform test', 'the formation of a yellow precipitate of CHI₃ by compounds with a CH₃CO– or CH₃CH(OH)– group on treatment with NaOI')],
    'groups': [('a compound that undergoes aldol condensation', ['ethanal', 'propanal', 'propanone', 'acetophenone']),
               ('a compound that undergoes the Cannizzaro reaction', ['methanal', 'benzaldehyde', '2,2-dimethylpropanal', '4-methoxybenzaldehyde'])],
    'tf': (['Aldehydes are generally more reactive than ketones in nucleophilic addition.', 'Methanal does not give the iodoform test.', 'Benzaldehyde does not reduce Fehling\'s solution.',
            'Aldehydes without α-hydrogen undergo the Cannizzaro reaction.', 'Propanone gives the iodoform test.'],
           [('Ketones are more reactive than aldehydes towards nucleophiles.', 'Aldehydes are more reactive (less steric hindrance and less +I effect).'),
            ('Benzaldehyde undergoes aldol condensation.', 'It has no α-hydrogen; it undergoes the Cannizzaro reaction.'),
            ('Ketones give a silver mirror with Tollens\' reagent.', 'Ketones are not oxidised by mild oxidising agents; only aldehydes give the test.'),
            ('Pentan-3-one gives the iodoform test.', 'It has no CH₃CO– group; pentan-2-one gives the test.')]),
    'orders': [('order of reactivity towards nucleophilic addition', ['methanal', 'ethanal', 'propanone', 'butan-2-one'], 'Alkyl groups increase steric hindrance and reduce the δ⁺ on carbon.', '>'),
               ('order of reactivity towards HCN', ['benzaldehyde', 'acetophenone', 'benzophenone'], 'More aryl/alkyl groups ⇒ more hindrance and less electrophilic carbon.', '>')],
    'ar': [('Aldehydes are more reactive than ketones towards nucleophilic addition.', 'Two alkyl groups in ketones reduce the electrophilicity of the carbonyl carbon and cause steric hindrance.', 'a', 'Electronic and steric reasons.'),
           ('Methanal undergoes the Cannizzaro reaction.', 'Methanal has no α-hydrogen atom.', 'a', 'Without α-H, aldol is not possible.'),
           ('Benzaldehyde gives a positive Fehling\'s test.', 'Benzaldehyde is an aldehyde.', 'd', 'Aromatic aldehydes do not reduce Fehling\'s solution; the reason is true.'),
           ('Propanone gives a yellow precipitate with I₂ and NaOH.', 'Propanone contains a CH₃CO– group.', 'a', 'Methyl ketones give iodoform.')],
    'fams': [F('C3', 'D3', 'mcq', co_rx), F('C3', 'D2', 'explain', co_rx_x), F('C3', 'D3', 'mcq', distinguish), F('C4', 'D4', 'explain', distinguish_x, marks=2)],
    'qa': [('C4', 'D4', 'explain', 'Write the mechanism of nucleophilic addition of HCN to a carbonyl compound. Why is a small amount of base used?',
            'Base forms CN⁻ from HCN; CN⁻ attacks the electrophilic carbonyl carbon forming a tetrahedral alkoxide intermediate, which takes H⁺ from HCN to give the cyanohydrin. Base increases the concentration of the strong nucleophile CN⁻.',
            '1 mark mechanism; 1 mark role of base.'),
           ('C4', 'D5', 'long', 'An organic compound A (C₃H₆O) gives a yellow precipitate with I₂/NaOH, does not reduce Tollens\' reagent, and forms an addition product with NaHSO₃. On Clemmensen reduction it gives propane. Identify A and write all the reactions. Name one compound isomeric with A that gives a silver mirror.',
            'A is propanone, CH₃COCH₃. CH₃COCH₃ + 3NaOI → CHI₃ + CH₃COONa + 2NaOH; CH₃COCH₃ + NaHSO₃ → (CH₃)₂C(OH)SO₃Na; CH₃COCH₃ + 4[H] (Zn–Hg/HCl) → CH₃CH₂CH₃ + H₂O. Propanal (CH₃CH₂CHO) is the isomer that gives a silver mirror.',
            '1 mark identification; 3 marks reactions; 1 mark isomer.'),
           ('C4', 'D3', 'case', 'Sameer has two compounds X (C₇H₆O) and Y (C₂H₄O). Both give a silver mirror. Y gives a red precipitate with Fehling\'s solution and a yellow precipitate with NaOI; X gives neither.\n(i) Identify X and Y. (2 marks)\n(ii) Which of them undergoes the Cannizzaro reaction? Write its products. (2 marks)',
            '(i) X: benzaldehyde (C₆H₅CHO); Y: ethanal (CH₃CHO). (ii) Benzaldehyde (no α-H): with conc. NaOH it gives benzyl alcohol and sodium benzoate.',
            '(i) 2 (ii) 2.', ('case',))],
}

CH8S3 = {
    'topic': 'carboxylic acids',
    'terms': [('the Hell–Volhard–Zelinsky reaction', 'the α-halogenation of a carboxylic acid with chlorine or bromine in the presence of red phosphorus'),
              ('decarboxylation', 'the loss of CO₂ from a carboxylic acid salt on heating with soda lime, giving an alkane with one carbon less'),
              ('Kolbe electrolysis', 'the electrolysis of aqueous sodium or potassium salts of carboxylic acids to give alkanes with twice the alkyl group'),
              ('the carboxylate ion', 'the anion RCOO⁻, stabilised by resonance between two equivalent structures'),
              ('an acyl chloride', 'the derivative RCOCl formed by reacting a carboxylic acid with PCl₅, PCl₃ or SOCl₂')],
    'tf': (['Carboxylic acids are stronger acids than phenols.', 'Electron-withdrawing groups increase the strength of carboxylic acids.', 'Carboxylic acids form dimers through hydrogen bonding in the vapour phase.',
            'Benzoic acid undergoes nitration at the meta position.', 'Carboxylic acids do not give the reactions of the carbonyl group such as oxime formation.'],
           [('Ethanoic acid is a stronger acid than methanoic acid.', 'Methanoic acid (pKa 3.75) is stronger; the –CH₃ group (+I) weakens ethanoic acid.'),
            ('Chloroethanoic acid is weaker than ethanoic acid.', 'The –I effect of Cl stabilises the anion, so chloroethanoic acid is stronger.'),
            ('Benzoic acid undergoes Friedel–Crafts reaction readily.', 'The –COOH group deactivates the ring and the AlCl₃ binds to it; no Friedel–Crafts reaction.'),
            ('Carboxylic acids are reduced by NaBH₄ to alcohols.', 'They are reduced by LiAlH₄ or diborane; NaBH₄ does not reduce the –COOH group.')]),
    'orders': [('order of acid strength', ['CH₃COOH', 'HCOOH', 'ClCH₂COOH', 'Cl₂CHCOOH', 'Cl₃CCOOH'], 'More electron-withdrawing chlorine atoms stabilise the carboxylate ion; –CH₃ destabilises it.', '<'),
               ('order of acid strength', ['ethanol', 'phenol', 'benzoic acid', '4-nitrobenzoic acid'], 'Carboxylate is more stabilised than phenoxide; –NO₂ adds further stabilisation.', '<'),
               ('order of boiling point', ['butane', 'propanal', 'propan-1-ol', 'ethanoic acid'], 'Carboxylic acids form strong intermolecular H-bonded dimers.', '<')],
    'ar': [('Carboxylic acids are more acidic than phenols.', 'The carboxylate ion is stabilised by two equivalent resonance structures.', 'a', 'Negative charge on two electronegative O atoms.'),
           ('Monochloroethanoic acid is stronger than ethanoic acid.', 'Chlorine shows a −I effect.', 'a', 'It stabilises the carboxylate.'),
           ('Carboxylic acids have higher boiling points than alcohols of similar mass.', 'Carboxylic acids form dimers by strong hydrogen bonding.', 'a', 'H-bonds persist even in the vapour.'),
           ('The carbonyl group of carboxylic acids reacts with NH₂OH like aldehydes.', 'Resonance in –COOH reduces the electrophilic character of the carbonyl carbon.', 'd', 'Carboxylic acids do not form oximes; the reason is true.')],
    'fams': [F('C3', 'D3', 'mcq', ca_rx), F('C3', 'D2', 'explain', ca_rx_x), F('C3', 'D3', 'mcq', ca_pick), F('C4', 'D4', 'multi_step', ca_ph)],
    'qa': [('C4', 'D4', 'explain', 'Arrange in increasing order of acid strength and justify: CH₃CH₂CH(Br)COOH, CH₃CH(Br)CH₂COOH, (CH₃)₂CHCOOH, CH₃CH₂CH₂COOH.',
            '(CH₃)₂CHCOOH < CH₃CH₂CH₂COOH < CH₃CH(Br)CH₂COOH < CH₃CH₂CH(Br)COOH. +I of alkyl groups weakens; –I of Br strengthens and is greater when Br is closer to –COOH.',
            '1 mark order; 1 mark reason.'),
           ('C4', 'D5', 'long', 'Write equations for: (i) HVZ reaction of ethanoic acid, (ii) decarboxylation of sodium propanoate, (iii) Kolbe electrolysis of sodium ethanoate, (iv) reduction of ethanoic acid with LiAlH₄, (v) preparation of benzoic acid from toluene.',
            '(i) CH₃COOH + Cl₂ (red P) → ClCH₂COOH + HCl. (ii) CH₃CH₂COONa + NaOH (CaO, heat) → CH₃CH₃ + Na₂CO₃. (iii) 2CH₃COONa + 2H₂O → C₂H₆ + 2CO₂ + 2NaOH + H₂ (electrolysis). (iv) CH₃COOH → (LiAlH₄, then H₃O⁺) CH₃CH₂OH. (v) C₆H₅CH₃ → (KMnO₄/KOH, heat, then H₃O⁺) C₆H₅COOH.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'Divya measures the pKa of three acids: ethanoic acid (4.76), chloroethanoic acid (2.86) and trichloroethanoic acid (0.65).\n(i) Which is the strongest acid? (1 mark)\n(ii) Explain the trend. (2 marks)\n(iii) Predict whether fluoroethanoic acid is stronger or weaker than chloroethanoic acid. (1 mark)',
            '(i) Trichloroethanoic acid. (ii) Chlorine is electron-withdrawing (−I); each Cl disperses the negative charge of the carboxylate, stabilising it and increasing acid strength. (iii) Stronger, because F is more electronegative (−I effect larger).',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH8S4 = {
    'topic': 'uses of aldehydes, ketones and carboxylic acids',
    'terms': [('formalin', 'a 40% aqueous solution of methanal, used to preserve biological specimens'),
              ('vinegar', 'a 6–8% solution of ethanoic acid in water, used as a food condiment'),
              ('sodium benzoate', 'the sodium salt of benzoic acid, used as a food preservative'),
              ('bakelite', 'a thermosetting polymer made from phenol and methanal'),
              ('esters of benzoic acid', 'compounds used in perfumery')],
    'groups': [('a use of methanal', ['preservation of biological specimens (formalin)', 'manufacture of bakelite', 'manufacture of urea–formaldehyde resins']),
               ('a use of propanone', ['solvent for paints and lacquers', 'nail polish remover', 'manufacture of chloroform']),
               ('a use of a carboxylic acid or its salt', ['vinegar (ethanoic acid)', 'food preservative (sodium benzoate)', 'soaps (sodium salts of higher fatty acids)'])],
    'tf': (['Formalin is a 40% solution of methanal in water.', 'Vinegar contains ethanoic acid.', 'Sodium benzoate is used as a food preservative.',
            'Propanone is used as a solvent.', 'Higher fatty acids are used to make soaps.'],
           [('Formalin is a 40% solution of ethanal.', 'Formalin is a 40% aqueous solution of methanal.'),
            ('Vinegar is a 40% solution of ethanoic acid.', 'Vinegar is 6–8% ethanoic acid.'),
            ('Sodium benzoate is used as a dye.', 'It is a food preservative.'),
            ('Bakelite is made from propanone and phenol.', 'Bakelite is made from phenol and methanal.')]),
    'ar': [('Formalin is used to preserve biological specimens.', 'Methanal denatures proteins and kills microorganisms.', 'a', 'Prevents decay.'),
           ('Sodium benzoate is added to sauces and jams.', 'It prevents the growth of microorganisms.', 'a', 'Food preservative.')],
    'features': {'intro': 'A carbonyl compound or acid has these uses:', 'q': 'Identify the compound', 'what': 'compound', 'long': False,
                 'items': [('methanal', ['40% solution called formalin', 'preserves biological specimens', 'used to make bakelite', 'used in urea–formaldehyde glues']),
                           ('ethanal', ['used to make ethanoic acid', 'used to make ethyl ethanoate', 'used to make vinyl ethanoate', 'starting material for drugs']),
                           ('propanone', ['common industrial solvent', 'used as nail polish remover', 'by-product of the cumene process', 'used to dissolve acetylene in cylinders']),
                           ('benzoic acid', ['its sodium salt is a food preservative', 'its esters are used in perfumery', 'made by oxidation of toluene', 'used in medicine as a urinary antiseptic'])]},
    'qa': [('C4', 'D4', 'explain', 'Give two uses each of methanal and ethanoic acid.',
            'Methanal: formalin for preserving specimens; making bakelite and urea–formaldehyde resins. Ethanoic acid: vinegar in food; making cellulose acetate, ethyl ethanoate and other chemicals.',
            '1 mark each compound.'),
           ('C3', 'D2', 'explain', 'Why is sodium benzoate preferred to benzoic acid as a food preservative?',
            'Sodium benzoate is much more soluble in water, so it mixes evenly into food; in the acidic food it forms benzoic acid, which stops microbial growth.',
            '1 mark solubility; 1 mark action.')],
}

# ---------------------------------------------------------------- unit 9: amines

AMINE_NAMES = [('CH₃NH₂', 'methanamine', ['methylamine-1', 'aminomethane-1', 'ethanamine']),
               ('CH₃CH₂NHCH₃', 'N-methylethanamine', ['N-ethylmethanamine', 'propan-1-amine', 'N,N-dimethylmethanamine']),
               ('(CH₃)₃N', 'N,N-dimethylmethanamine', ['trimethanamine', 'N-methylethanamine', 'propan-2-amine']),
               ('C₆H₅NH₂', 'benzenamine (aniline)', ['phenylmethanamine', 'aminocyclohexane', 'N-phenylamine-1']),
               ('C₆H₅NHCH₃', 'N-methylbenzenamine', ['4-methylbenzenamine', 'phenylmethanamine', 'N-phenylmethanol']),
               ('(CH₃)₂CHNH₂', 'propan-2-amine', ['propan-1-amine', '2-methylethanamine', 'N-methylethanamine']),
               ('H₂N(CH₂)₆NH₂', 'hexane-1,6-diamine', ['hexanediamine-1,6-ene', 'hexane-1,5-diamine', 'cyclohexane-1,6-diamine']),
               ('C₆H₅CH₂NH₂', 'phenylmethanamine', ['benzenamine', 'N-methylbenzenamine', '2-methylbenzenamine']),
               ('CH₃CH₂CH₂NH₂', 'propan-1-amine', ['propan-2-amine', 'N-methylethanamine', 'propylamine-1']),
               ('(C₂H₅)₂NH', 'N-ethylethanamine', ['diethanamine', 'butan-2-amine', 'N,N-diethylmethanamine'])]
am_name, am_struct = name_mcq(AMINE_NAMES)

AM_CLASS = [('CH₃NH₂', 'a primary amine'), ('C₆H₅NH₂', 'a primary amine'), ('(CH₃)₂CHNH₂', 'a primary amine'), ('(CH₃)₃CNH₂', 'a primary amine'),
            ('(CH₃)₂NH', 'a secondary amine'), ('C₆H₅NHCH₃', 'a secondary amine'), ('(C₂H₅)₂NH', 'a secondary amine'),
            ('(CH₃)₃N', 'a tertiary amine'), ('C₆H₅N(CH₃)₂', 'a tertiary amine'), ('(C₂H₅)₃N', 'a tertiary amine'),
            ('(CH₃)₄N⁺I⁻', 'a quaternary ammonium salt')]
am_class = table_mcq([(a, '', c, f'{a} has the nitrogen bonded to the number of carbon groups that defines {c}') for a, c in AM_CLASS],
                     'How is {a} classified?', pool=['a primary amine', 'a secondary amine', 'a tertiary amine', 'a quaternary ammonium salt'])

AM_PREP = [('nitrobenzene', 'Fe scrap and HCl', 'aniline', 'reduction of the nitro group'),
           ('nitrobenzene', 'H₂ over Pd', 'aniline', 'catalytic hydrogenation'),
           ('phthalimide', 'ethanolic KOH, then C₂H₅Br, then alkaline hydrolysis', 'ethanamine', 'Gabriel phthalimide synthesis (only 1° aliphatic amines)'),
           ('ethanamide', 'Br₂ and aqueous NaOH', 'methanamine', 'Hoffmann bromamide degradation: the amine has one carbon less'),
           ('propanamide', 'Br₂ and aqueous NaOH', 'ethanamine', 'Hoffmann bromamide degradation'),
           ('benzamide', 'Br₂ and aqueous NaOH', 'aniline', 'Hoffmann bromamide degradation'),
           ('ethanenitrile', 'LiAlH₄ (or H₂/Ni)', 'ethanamine', 'reduction of nitriles gives amines with one carbon more than the alkyl halide used'),
           ('ethanamide', 'LiAlH₄, then H₂O', 'ethanamine', 'reduction of amides keeps the same number of carbons'),
           ('chloroethane', 'excess ethanolic NH₃ in a sealed tube', 'ethanamine (with 2° and 3° amines)', 'ammonolysis of alkyl halides gives a mixture')]
am_prep = table_mcq(AM_PREP, 'What is the main amine formed when {a} is treated with {b}?')


AMIDES = [('ethanamide', 'CH₃CONH₂', 59, 'methanamine', 'CH₃NH₂', 31), ('propanamide', 'CH₃CH₂CONH₂', 73, 'ethanamine', 'C₂H₅NH₂', 45),
          ('butanamide', 'CH₃(CH₂)₂CONH₂', 87, 'propan-1-amine', 'C₃H₇NH₂', 59), ('benzamide', 'C₆H₅CONH₂', 121, 'aniline', 'C₆H₅NH₂', 93)]


def hoffmann(r):
    a, af, Ma, b, bf, Mb = r.choice(AMIDES)
    m = r.choice([5.9, 7.3, 8.7, 12.1, 10.0, 20.0, 2.5])
    y = r.choice([100, 80, 70, 60])
    mb = m / Ma * Mb * y / 100
    return {'stem': f'In the Hoffmann bromamide degradation, {m} g of {a} ({af}) is treated with Br₂ and aqueous NaOH. Identify the amine and calculate its mass if the yield is {y}%. (Molar masses: amide {Ma}, amine {Mb} g mol⁻¹)',
            'answer': f'{b} ({bf}); {sf(mb, 3)} g',
            'key': f'RCONH₂ + Br₂ + 4NaOH → RNH₂ + Na₂CO₃ + 2NaBr + 2H₂O: one carbon is lost, giving {b} (1); n = {m}/{Ma} = {sf(m / Ma, 3)} mol (1); mass = n × {Mb} × {y}% = {sf(mb, 3)} g (1).',
            'distractors': [f'{b} ({bf}); {sf(m / Ma * Mb, 3) if y != 100 else sf(mb * 0.8, 3)} g', f'{b} ({bf}); {sf(m * y / 100, 3)} g', f'{a.replace("amide", "amine")}; {sf(mb * (Mb + 14) / Mb, 3)} g']}


PKB = [('NH₃', 4.75), ('methanamine', 3.38), ('N-methylmethanamine', 3.27), ('N,N-dimethylmethanamine', 4.22), ('ethanamine', 3.29),
       ('N-ethylethanamine', 3.00), ('N,N-diethylethanamine', 3.25), ('aniline', 9.38), ('N-methylaniline', 9.30), ('N,N-dimethylaniline', 8.92),
       ('4-methylaniline', 8.92), ('4-nitroaniline', 13.0), ('phenylmethanamine', 4.70)]


def base_pick(r):
    while True:
        sub = r.sample(PKB, 4)
        vals = [x[1] for x in sub]
        if len(set(vals)) == 4:
            break
    mode = r.choice(['strongest', 'weakest'])
    best = min(sub, key=lambda x: x[1]) if mode == 'strongest' else max(sub, key=lambda x: x[1])
    tab = ', '.join(f'{x[0]} {x[1]}' for x in sub)
    return mcq(f'Given the pKb values {tab}, which is the {mode} base?', best[0], [x[0] for x in sub if x is not best],
               f'Lower pKb means stronger base: {best[0]} (pKb {best[1]}).', r)


def kb_calc(r):
    s, p = r.choice(PKB)
    c = r.choice([0.1, 0.05, 0.01, 0.2])
    Kb = 10 ** -p
    if math.sqrt(Kb / c) > 0.1:
        raise ValueError('approximation not valid')
    pOH = 0.5 * (p - math.log10(c))
    return {'stem': f'The pKb of {s} is {p}. Calculate Kb and the pH of a {c} M aqueous solution at 298 K (assume α ≪ 1).',
            'answer': f'Kb = {sci(Kb, 2)}; pH = {14 - pOH:.2f}',
            'key': f'Kb = 10^(−{p}) = {sci(Kb, 2)} (1); pOH = ½(pKb − log c) = {pOH:.2f} (1); pH = 14 − pOH = {14 - pOH:.2f} (1).',
            'distractors': [f'Kb = {sci(Kb, 2)}; pH = {pOH:.2f}', f'Kb = {sci(Kb, 2)}; pH = {14 - (p - math.log10(c)):.2f}', f'Kb = {sci(10 ** -(14 - p), 2)}; pH = {14 - pOH:.2f}']}


AM_RX = [('aniline', 'bromine water', '2,4,6-tribromoaniline (white precipitate)', 'the –NH₂ group strongly activates the ring'),
         ('aniline', 'ethanoic anhydride (pyridine)', 'acetanilide (N-phenylethanamide)', 'acetylation reduces the activating effect of –NH₂'),
         ('aniline', 'conc. HNO₃ + conc. H₂SO₄', 'p-nitroaniline (51%), m-nitroaniline (47%) and o-nitroaniline (2%)', 'protonation to anilinium ion gives much meta product'),
         ('aniline', 'conc. H₂SO₄, then heat at 453–473 K', 'sulphanilic acid', 'sulphonation; the product exists as a zwitterion'),
         ('ethanamine', 'CHCl₃ and alcoholic KOH (heat)', 'ethyl isocyanide (foul smell)', 'carbylamine reaction, given only by primary amines'),
         ('ethanamine', 'HNO₂ (NaNO₂ + HCl)', 'ethanol with evolution of N₂', 'aliphatic diazonium salts are unstable'),
         ('aniline', 'NaNO₂ + HCl at 273–278 K', 'benzenediazonium chloride', 'diazotisation'),
         ('ethanamine', 'benzenesulphonyl chloride', 'N-ethylbenzenesulphonamide, soluble in alkali', 'Hinsberg test for primary amines'),
         ('N-ethylethanamine', 'benzenesulphonyl chloride', 'N,N-diethylbenzenesulphonamide, insoluble in alkali', 'Hinsberg test for secondary amines'),
         ('ethanamine', 'CH₃COCl', 'N-ethylethanamide', 'acylation of a primary amine')]
am_rx = table_mcq(AM_RX, 'What is formed when {a} reacts with {b}?')
am_rx_x = table_explain(AM_RX, 'What is formed when {a} reacts with {b}? Give the reason or name the reaction.')

DIAZ = [('CuCl/HCl', 'chlorobenzene', 'Sandmeyer reaction'), ('CuBr/HBr', 'bromobenzene', 'Sandmeyer reaction'), ('CuCN/KCN', 'benzonitrile', 'Sandmeyer reaction'),
        ('Cu powder and HCl', 'chlorobenzene', 'Gattermann reaction'), ('KI', 'iodobenzene', 'replacement by iodide'),
        ('HBF₄, then heat', 'fluorobenzene', 'Balz–Schiemann reaction'), ('H₃PO₂ (hypophosphorous acid)', 'benzene', 'replacement by H'),
        ('warm water', 'phenol', 'hydrolysis'), ('phenol in alkaline medium', 'p-hydroxyazobenzene (orange dye)', 'azo coupling at the para position'),
        ('aniline in mildly acidic medium', 'p-aminoazobenzene (yellow dye)', 'azo coupling'),
        ('ethanol', 'benzene', 'reduction by ethanol (ethanal formed)'), ('HBF₄ then NaNO₂/Cu (heat)', 'nitrobenzene', 'replacement by –NO₂')]
diaz = table_mcq([('benzenediazonium chloride', a, b, c) for a, b, c in DIAZ], 'What is formed when {a} is treated with {b}?')
diaz_x = table_explain([('benzenediazonium chloride', a, b, c) for a, b, c in DIAZ], 'Write the product when {a} is treated with {b}, and name the reaction.')

CONVERSIONS = [('benzene', 'fluorobenzene', 'benzene → (HNO₃/H₂SO₄) nitrobenzene → (Sn/HCl) aniline → (NaNO₂/HCl, 273 K) diazonium salt → (HBF₄, heat) fluorobenzene'),
               ('aniline', 'benzonitrile', 'aniline → (NaNO₂/HCl, 273–278 K) benzenediazonium chloride → (CuCN/KCN) benzonitrile'),
               ('aniline', '1,3,5-tribromobenzene', 'aniline → (Br₂ water) 2,4,6-tribromoaniline → (NaNO₂/HCl, 273 K) diazonium salt → (H₃PO₂) 1,3,5-tribromobenzene'),
               ('nitrobenzene', 'benzoic acid', 'nitrobenzene → (Sn/HCl) aniline → (NaNO₂/HCl) diazonium salt → (CuCN/KCN) benzonitrile → (H₃O⁺) benzoic acid'),
               ('aniline', 'p-bromoaniline', 'aniline → (acetic anhydride) acetanilide → (Br₂ in CH₃COOH) p-bromoacetanilide → (H⁺/OH⁻ hydrolysis) p-bromoaniline'),
               ('benzene', 'm-bromophenol', 'benzene → (HNO₃/H₂SO₄) nitrobenzene → (Br₂/FeBr₃) m-bromonitrobenzene → (Sn/HCl) m-bromoaniline → (NaNO₂/HCl) diazonium → (warm H₂O) m-bromophenol'),
               ('aniline', 'iodobenzene', 'aniline → (NaNO₂/HCl, 273–278 K) benzenediazonium chloride → (KI) iodobenzene')]


def convert(r):
    a, b, path = r.choice(CONVERSIONS)
    steps = path.count('→')
    return {'stem': f'How will you convert {a} into {b}? Give the reagents for each step.', 'answer': path,
            'key': f'Each correct step with reagent/conditions earns credit ({steps} step{"s" if steps > 1 else ""}): {path}.'}


CH9S1 = {
    'topic': 'structure, classification, nomenclature and preparation of amines',
    'terms': [('a primary amine', 'an amine in which one hydrogen of ammonia is replaced by an alkyl or aryl group'),
              ('a secondary amine', 'an amine in which two hydrogens of ammonia are replaced by alkyl or aryl groups'),
              ('Gabriel phthalimide synthesis', 'the preparation of primary aliphatic amines from phthalimide, KOH and an alkyl halide followed by hydrolysis'),
              ('Hoffmann bromamide degradation', 'the conversion of an amide to a primary amine with one carbon less using Br₂ and NaOH'),
              ('ammonolysis', 'the cleavage of the C–X bond of an alkyl halide by ammonia to give amines'),
              ('a quaternary ammonium salt', 'a salt R₄N⁺X⁻ in which all four hydrogens of the ammonium ion are replaced by alkyl groups')],
    'tf': (['The nitrogen in amines is sp³ hybridised with a pyramidal shape.', 'Gabriel synthesis cannot be used to prepare aromatic primary amines.', 'Hoffmann bromamide degradation gives an amine with one carbon less than the amide.',
            'Reduction of nitrobenzene with Fe and HCl is preferred industrially.', 'Ammonolysis of alkyl halides gives a mixture of amines.'],
           [('Gabriel phthalimide synthesis is used to prepare aniline.', 'Aryl halides do not undergo nucleophilic substitution with the phthalimide anion; it gives only 1° aliphatic amines.'),
            ('Hoffmann bromamide degradation gives an amine with the same number of carbons as the amide.', 'One carbon is lost (as carbonate).'),
            ('Reduction of nitriles gives amines with one carbon less.', 'Nitrile reduction gives amines with the same carbon chain; the chain is one carbon longer than the alkyl halide used.'),
            ('The C–N–H bond angle in amines is 120°.', 'Nitrogen is sp³; the angle is about 108° (pyramidal).')]),
    'ar': [('Aromatic primary amines cannot be prepared by Gabriel phthalimide synthesis.', 'Aryl halides do not undergo nucleophilic substitution with the phthalimide anion.', 'a', 'The C–X bond of aryl halides is resistant.'),
           ('Iron scrap and HCl are preferred for reducing nitrobenzene to aniline.', 'FeCl₂ formed is hydrolysed, releasing HCl during the reaction.', 'a', 'So only a small amount of acid is needed.'),
           ('Ammonolysis of alkyl halides gives a pure primary amine.', 'The primary amine formed can react further with alkyl halide.', 'd', 'A mixture of 1°, 2°, 3° amines and quaternary salt is obtained; the reason is true.')],
    'fams': [F('C2', 'D2', 'mcq', am_name), F('C2', 'D1', 'mcq', am_class), F('C3', 'D3', 'mcq', am_prep), F('C4', 'D4', 'multi_step', hoffmann), F('C2', 'D2', 'mcq', am_struct)],
    'qa': [('C4', 'D4', 'explain', 'Why cannot aniline be prepared by Gabriel phthalimide synthesis? Suggest a method to prepare it.',
            'Aryl halides do not undergo nucleophilic substitution with the phthalimide anion. Aniline is made by reduction of nitrobenzene with Sn/HCl or Fe/HCl (or H₂/Pd).',
            '1 mark reason; 1 mark method.'),
           ('C4', 'D3', 'case', 'Harish has propanamide in his laboratory and wants ethanamine.\n(i) Name the reaction he should use and give the reagents. (2 marks)\n(ii) How many carbon atoms are lost? (1 mark)\n(iii) Which reagent would convert propanamide into propan-1-amine instead? (1 mark)',
            '(i) Hoffmann bromamide degradation with Br₂ and aqueous NaOH. (ii) One carbon is lost (as Na₂CO₃). (iii) LiAlH₄ followed by H₂O.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',))],
}

CH9S2 = {
    'topic': 'physical properties, basicity and reactions of amines',
    'terms': [('the carbylamine reaction', 'the reaction of a primary amine with chloroform and alcoholic KOH giving a foul-smelling isocyanide'),
              ('the Hinsberg test', 'the test with benzenesulphonyl chloride that distinguishes primary, secondary and tertiary amines'),
              ('acetylation', 'the replacement of a hydrogen of –NH₂ by an acetyl group, e.g. aniline to acetanilide'),
              ('the anilinium ion', 'the ion C₆H₅NH₃⁺ formed when aniline is protonated'),
              ('a zwitterion', 'a dipolar ion with both positive and negative charges, as in sulphanilic acid')],
    'groups': [('a test given only by primary amines', ['carbylamine test', 'nitrous acid giving N₂ (aliphatic)']), ('a test that distinguishes 1°, 2° and 3° amines', ['Hinsberg test with benzenesulphonyl chloride']),
               ('a property of aniline', ['less basic than ammonia', 'forms 2,4,6-tribromoaniline with bromine water', 'no Friedel–Crafts reaction'])],
    'classify': False,
    'tf': (['Aniline is a weaker base than ammonia.', 'Aliphatic amines are stronger bases than ammonia.', 'Primary amines have higher boiling points than tertiary amines of similar mass.',
            'Aniline does not undergo Friedel–Crafts reaction.', 'Only primary amines give the carbylamine test.'],
           [('Aniline is a stronger base than methylamine.', 'The lone pair of aniline is delocalised into the ring; it is much weaker (pKb 9.38 vs 3.38).'),
            ('Tertiary amines have the highest boiling points among isomeric amines.', 'Tertiary amines have no N–H for hydrogen bonding; they boil lowest.'),
            ('Nitration of aniline gives only p-nitroaniline.', 'A large amount of m-nitroaniline also forms because the anilinium ion is meta-directing.'),
            ('Secondary amines give the carbylamine test.', 'Only primary amines give it.')]),
    'orders': [('order of basic strength in aqueous solution', ['(C₂H₅)₂NH', '(C₂H₅)₃N', 'C₂H₅NH₂', 'NH₃'], 'Combination of +I effect, solvation of the ammonium ion and steric effects.', '>'),
               ('order of basic strength in aqueous solution', ['(CH₃)₂NH', 'CH₃NH₂', '(CH₃)₃N', 'NH₃'], 'Methyl amines: 2° > 1° > 3° > NH₃.', '>'),
               ('order of basic strength', ['C₂H₅NH₂', 'NH₃', 'C₆H₅NH₂', 'p-nitroaniline'], 'Aryl ring and –NO₂ withdraw the lone pair; alkyl groups push it.', '>'),
               ('order of boiling point', ['(C₂H₅)₃N', '(C₂H₅)₂NH', 'C₄H₉NH₂', 'butan-1-ol'], 'Fewer N–H bonds ⇒ weaker H-bonding; O–H bonds are more polar than N–H.', '<')],
    'ar': [('Aniline is a weaker base than ethanamine.', 'In aniline the lone pair on nitrogen is delocalised into the benzene ring.', 'a', 'Less available for protonation.'),
           ('Aniline does not undergo Friedel–Crafts reaction.', 'Aniline forms a salt with AlCl₃, which places a positive charge on nitrogen.', 'a', 'The ring is deactivated.'),
           ('Acetylation of aniline is done before nitration.', 'Acetylation reduces the activating effect of –NH₂ and protects it from oxidation.', 'a', 'Controlled monosubstitution at para.'),
           ('Tertiary amines give the Hinsberg test with a soluble product.', 'Tertiary amines have no hydrogen on nitrogen.', 'd', 'They do not react with benzenesulphonyl chloride; the reason is true.')],
    'fams': [F('C3', 'D3', 'mcq', am_rx), F('C3', 'D2', 'explain', am_rx_x), F('C3', 'D3', 'mcq', base_pick), F('C4', 'D4', 'multi_step', kb_calc)],
    'qa': [('C4', 'D4', 'explain', 'Arrange (C₂H₅)₂NH, (C₂H₅)₃N, C₂H₅NH₂ and NH₃ in decreasing order of basic strength in water, and explain why the order is not simply 3° > 2° > 1°.',
            '(C₂H₅)₂NH > (C₂H₅)₃N > C₂H₅NH₂ > NH₃. Besides the +I effect, the solvation (H-bonding) of the ammonium ion and steric hindrance matter: 3° ammonium ions are poorly solvated.',
            '1 mark order; 1 mark explanation.'),
           ('C4', 'D5', 'long', 'Describe the Hinsberg test. How does it distinguish between primary, secondary and tertiary amines? Write the reactions with ethanamine and N-ethylethanamine.',
            'Benzenesulphonyl chloride reacts with 1° amines to give N-alkylbenzenesulphonamide, which has an acidic N–H and dissolves in alkali (C₆H₅SO₂Cl + C₂H₅NH₂ → C₆H₅SO₂NHC₂H₅). 2° amines give N,N-dialkylbenzenesulphonamide, insoluble in alkali (C₆H₅SO₂N(C₂H₅)₂). 3° amines do not react.',
            '1 mark reagent; 3 marks behaviour of 1°, 2°, 3°; 1 mark equations.'),
           ('C4', 'D3', 'case', 'Pooja nitrates aniline directly and gets a mixture with a lot of m-nitroaniline. She then acetylates aniline first.\n(i) Why is much m-nitroaniline formed? (1 mark)\n(ii) What does acetylation achieve? (2 marks)\n(iii) Which product does she get after hydrolysis? (1 mark)',
            '(i) In strongly acidic medium aniline is protonated to the anilinium ion, which is meta-directing. (ii) The acetyl group reduces the activating effect (lone pair also shared with C=O), prevents protonation/oxidation and allows mono-nitration at para. (iii) p-Nitroaniline (major).',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH9S3 = {
    'topic': 'diazonium salts',
    'terms': [('diazotisation', 'the conversion of a primary aromatic amine to a diazonium salt with NaNO₂ and HCl at 273–278 K'),
              ('the Sandmeyer reaction', 'the replacement of the diazonium group by Cl, Br or CN using the corresponding copper(I) salt'),
              ('the Gattermann reaction', 'the replacement of the diazonium group by Cl or Br using copper powder and the halogen acid'),
              ('a coupling reaction', 'the reaction of a diazonium salt with phenol or aniline giving a coloured azo compound'),
              ('the Balz–Schiemann reaction', 'the preparation of fluoroarenes by heating arenediazonium fluoroborates')],
    'tf': (['Arenediazonium salts are more stable than alkyldiazonium salts.', 'Diazotisation is carried out at 273–278 K.', 'Coupling of benzenediazonium chloride with phenol gives an orange dye.',
            'Benzenediazonium chloride gives benzene with hypophosphorous acid.', 'The diazonium group can be replaced by –I using KI alone.'],
           [('Diazotisation is carried out at about 350 K.', 'It is carried out at 273–278 K because diazonium salts decompose at higher temperatures.'),
            ('Fluorobenzene is made by treating benzenediazonium chloride with KF.', 'It is made by heating the fluoroborate (Balz–Schiemann reaction).'),
            ('Alkyldiazonium salts are stable at room temperature.', 'They decompose at once giving N₂ and carbocations; only arenediazonium salts are fairly stable.'),
            ('Azo coupling with phenol occurs at the meta position.', 'Coupling occurs at the para position.')]),
    'ar': [('Arenediazonium salts are more stable than alkyldiazonium salts.', 'In arenediazonium ions the positive charge is delocalised over the benzene ring.', 'a', 'Resonance stabilisation.'),
           ('Diazonium salts are prepared and used at low temperature.', 'They decompose to phenol and N₂ when warmed.', 'a', 'Hence 273–278 K.'),
           ('Aniline is converted to fluorobenzene via the diazonium salt.', 'Fluoride ion cannot be introduced by direct nucleophilic substitution with KF.', 'a', 'The Balz–Schiemann route is used.')],
    'fams': [F('C3', 'D3', 'mcq', diaz), F('C2', 'D2', 'mcq', diaz), F('C3', 'D2', 'explain', diaz_x), F('C4', 'D4', 'explain', convert, marks=3, minutes=4), F('C4', 'D5', 'multi_step', convert)],
    'qa': [('C4', 'D3', 'case', 'Ritika makes benzenediazonium chloride in an ice bath and uses it to prepare an orange dye.\n(i) Write the equation for its preparation. (1 mark)\n(ii) Why is the ice bath needed? (1 mark)\n(iii) Which reagent gives the orange dye, and at which position does coupling occur? (2 marks)',
            '(i) C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O (273–278 K). (ii) The salt decomposes at higher temperature. (iii) Phenol in alkaline medium; para position, giving p-hydroxyazobenzene.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'Explain with equations the importance of diazonium salts in the synthesis of aromatic compounds. Include preparation of chlorobenzene, iodobenzene, fluorobenzene, phenol and benzene.',
            'C₆H₅N₂⁺Cl⁻ + CuCl/HCl → C₆H₅Cl + N₂ (Sandmeyer); + KI → C₆H₅I; + HBF₄ → C₆H₅N₂⁺BF₄⁻ → (heat) C₆H₅F + BF₃ + N₂; + H₂O (warm) → C₆H₅OH + N₂ + HCl; + H₃PO₂ + H₂O → C₆H₆ + N₂ + H₃PO₃ + HCl. These products cannot easily be made by direct substitution.',
            '1 mark each.')],
}

# ---------------------------------------------------------------- unit 10: biomolecules

SUGARS = [('aldohexose (e.g. glucose)', 4), ('ketohexose (e.g. fructose)', 3), ('aldopentose (e.g. ribose)', 3), ('aldotetrose (e.g. erythrose)', 2), ('ketopentose (e.g. ribulose)', 2)]


def stereo_sugar(r):
    s, n = r.choice(SUGARS)
    return {'stem': f'How many chiral carbon atoms are present in the open-chain form of an {s}, and how many stereoisomers are possible?',
            'answer': f'{n} chiral carbons; 2^{n} = {2 ** n} stereoisomers',
            'key': f'Count the CH(OH) carbons with four different groups: {n} (1); stereoisomers = 2ⁿ = {2 ** n} (1).',
            'distractors': [f'{n + 1} chiral carbons; {2 ** (n + 1)} stereoisomers', f'{n} chiral carbons; {2 * n} stereoisomers', f'{n - 1} chiral carbons; {2 ** (n - 1)} stereoisomers']}


def sucrose_hyd(r):
    m = r.choice([17.1, 34.2, 68.4, 85.5, 171, 342, 513])
    n = m / 342
    g = n * 180
    who = name(r)
    return {'stem': f'{who} hydrolyses {m} g of sucrose with dilute acid: C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ (glucose) + C₆H₁₂O₆ (fructose). Calculate the mass of glucose formed. Why is this product mixture called invert sugar? (Molar masses: sucrose 342, glucose 180 g mol⁻¹)',
            'answer': f'{sf(g, 3)} g of glucose; the sign of rotation is inverted from dextro (sucrose) to laevo (mixture)',
            'key': f'n = {m}/342 = {sf(n, 3)} mol (1); glucose = {sf(n, 3)} × 180 = {sf(g, 3)} g (1); the rotation changes from dextro (sucrose) to laevo (mixture), because fructose (−92.4°) outweighs glucose (+52.5°) (1).',
            'distractors': [f'{sf(2 * g, 3)} g of glucose; the sign of rotation is inverted from dextro to laevo', f'{sf(m / 2, 3)} g of glucose; the sign of rotation is inverted from dextro to laevo',
                            f'{sf(g, 3)} g of glucose; the mixture stays dextrorotatory']}


GLU_RX = [('glucose', 'HI (prolonged heating)', 'n-hexane', 'all six carbons are in a straight chain'),
          ('glucose', 'hydroxylamine', 'glucose oxime', 'presence of a carbonyl group'),
          ('glucose', 'HCN', 'glucose cyanohydrin', 'presence of a carbonyl group'),
          ('glucose', 'bromine water', 'gluconic acid', 'the carbonyl group is an aldehyde group'),
          ('glucose', 'nitric acid', 'saccharic acid', 'a primary alcohol group is present along with –CHO'),
          ('glucose', 'acetic anhydride', 'glucose pentaacetate', 'five –OH groups are present'),
          ('sucrose', 'dilute HCl (hydrolysis)', 'equimolar glucose and fructose (invert sugar)', 'glycosidic link between C1 of α-glucose and C2 of β-fructose is broken'),
          ('maltose', 'dilute acid (hydrolysis)', 'two molecules of α-D-glucose', 'C1–C4 glycosidic linkage'),
          ('lactose', 'dilute acid (hydrolysis)', 'β-D-galactose and β-D-glucose', 'C1 of galactose is linked to C4 of glucose')]
glu_rx = table_mcq(GLU_RX, 'What is obtained when {a} reacts with {b}?', why_fmt='{ans}: {why}.')

AA = [('glycine', 'Gly', 75), ('alanine', 'Ala', 89), ('valine', 'Val', 117), ('leucine', 'Leu', 131), ('serine', 'Ser', 105), ('cysteine', 'Cys', 121),
      ('phenylalanine', 'Phe', 165), ('lysine', 'Lys', 146), ('glutamic acid', 'Glu', 147), ('aspartic acid', 'Asp', 133)]


def peptide_mass(r, ks=(2, 3)):
    k = r.choice(ks)
    sel = [r.choice(AA) for _ in range(k)]
    tot = sum(x[2] for x in sel)
    M = tot - 18 * (k - 1)
    seq = '–'.join(x[1] for x in sel)
    tab = ', '.join(f'{x[0]} {x[2]}' for x in dict.fromkeys(sel))
    return {'stem': f'Calculate the number of peptide bonds and the molar mass of the peptide {seq}. (Molar masses in g mol⁻¹: {tab}; water 18)',
            'answer': f'{k - 1} peptide bond{"s" if k > 2 else ""}; {M} g mol⁻¹',
            'key': f'{k} amino acids join by {k - 1} peptide bond{'s' if k > 2 else ''}, losing {k - 1} H₂O (1); M = {tot} − {k - 1} × 18 = {M} g mol⁻¹ (1).',
            'distractors': [f'{k} peptide bonds; {tot - 18 * k} g mol⁻¹', f'{k - 1} peptide bonds; {tot} g mol⁻¹', f'{k - 1} peptide bonds; {tot + 18 * (k - 1)} g mol⁻¹']}


def peptide_count(r):
    k = r.choice([2, 3, 4])
    names = [x[0] for x in r.sample(AA, k)]
    n = math.factorial(k)
    wrong = [str(x) for x in dict.fromkeys([k, k * k, 2 ** k, n * 2, n + 1, k - 1]) if x != n and x > 0][:3]
    return mcq(f'How many different peptides containing each of {", ".join(names[:-1])} and {names[-1]} exactly once are possible?', str(n), wrong,
               f'Order matters (N- and C-terminals are different) ⇒ {k}! = {n} peptides.', r)


VITS = [('vitamin A', 'xerophthalmia (hardening of the cornea) and night blindness', 'fat'), ('vitamin B₁ (thiamine)', 'beriberi (loss of appetite, retarded growth)', 'water'),
        ('vitamin B₂ (riboflavin)', 'cheilosis (fissuring at the corners of the mouth and lips), digestive disorders', 'water'),
        ('vitamin B₆ (pyridoxine)', 'convulsions', 'water'), ('vitamin B₁₂', 'pernicious anaemia', 'water'),
        ('vitamin C (ascorbic acid)', 'scurvy (bleeding gums)', 'water'), ('vitamin D', 'rickets in children and osteomalacia in adults', 'fat'),
        ('vitamin E', 'increased fragility of RBCs and muscular weakness', 'fat'), ('vitamin K', 'increased blood clotting time', 'fat')]


def vit_def(r):
    v, d, s = r.choice(VITS)
    if r.random() < 0.5:
        return mcq(f'Deficiency of which vitamin causes {d}?', v, [x[0] for x in r.sample([x for x in VITS if x[0] != v], 3)], f'{cap(v)} deficiency: {d}.', r)
    return mcq(f'Which disease is caused by deficiency of {v}?', d, [x[1] for x in r.sample([x for x in VITS if x[0] != v], 3)], f'{cap(v)} deficiency: {d}.', r)


def chargaff(r):
    base = r.choice(['adenine', 'guanine', 'thymine', 'cytosine'])
    p = r.choice([15, 18, 20, 22, 24, 26, 28, 30, 32, 35])
    pair = {'adenine': 'thymine', 'thymine': 'adenine', 'guanine': 'cytosine', 'cytosine': 'guanine'}[base]
    rest = (100 - 2 * p) / 2
    others = [b for b in ('adenine', 'thymine', 'guanine', 'cytosine') if b not in (base, pair)]
    return {'stem': f'A sample of double-stranded DNA contains {p}% {base}. Calculate the percentages of the other three bases.',
            'answer': f'{pair} {p}%; {others[0]} {num(rest, 1)}%; {others[1]} {num(rest, 1)}%',
            'key': f'Base pairing (Chargaff\'s rule): {base} = {pair} = {p}% (1); remaining {100 - 2 * p}% is shared equally: {others[0]} = {others[1]} = {num(rest, 1)}% (1).',
            'distractors': [f'{pair} {num(rest, 1)}%; {others[0]} {p}%; {others[1]} {num(rest, 1)}%', f'{pair} {p}%; {others[0]} {num(100 - 2 * p, 1)}%; {others[1]} 0%',
                            f'{pair} {num((100 - p) / 3, 1)}%; {others[0]} {num((100 - p) / 3, 1)}%; {others[1]} {num((100 - p) / 3, 1)}%']}


COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
RNA = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}


def complement(r):
    s = ''.join(r.choice('ATGC') for _ in range(r.choice([8, 9, 10, 12])))
    mode = r.choice(['dna', 'rna'])
    if mode == 'dna':
        good = ''.join(COMP[c] for c in s)
        wrong = [''.join(RNA[c] for c in s), good[::-1], ''.join({'A': 'G', 'G': 'A', 'T': 'C', 'C': 'T'}[c] for c in s)]
        return mcq(f'One strand of a DNA segment has the base sequence 5′-{s}-3′. What is the sequence of the complementary strand (written 3′ → 5′)?', f"3′-{good}-5′",
                   [f"3′-{w}-5′" for w in wrong], f'A pairs with T and G pairs with C: 3′-{good}-5′.', r)
    good = ''.join(RNA[c] for c in s)
    wrong = [''.join(COMP[c] for c in s), good[::-1], s.replace('T', 'U')]
    return mcq(f'The template strand of a DNA segment reads 5′-{s}-3′. What is the sequence of the mRNA transcribed from it (written 3′ → 5′)?', f"3′-{good}-5′",
               [f"3′-{w}-5′" for w in wrong], f'In RNA, uracil replaces thymine: A → U, T → A, G → C, C → G ⇒ 3′-{good}-5′.', r)


CH10S1 = {
    'topic': 'carbohydrates',
    'terms': [('a monosaccharide', 'a carbohydrate that cannot be hydrolysed further to simpler polyhydroxy aldehydes or ketones'),
              ('a reducing sugar', 'a sugar that reduces Fehling\'s solution and Tollens\' reagent because it has a free aldehyde or ketone group'),
              ('anomers', 'two cyclic forms of a sugar that differ only in the configuration at C1 (α and β)'),
              ('a glycosidic linkage', 'the oxide linkage that joins two monosaccharide units through an oxygen atom'),
              ('invert sugar', 'the equimolar mixture of glucose and fructose formed by hydrolysis of sucrose, which is laevorotatory'),
              ('glycogen', 'the storage polysaccharide of animals, structurally similar to amylopectin but more highly branched')],
    'groups': [('a monosaccharide', ['glucose', 'fructose', 'ribose', 'galactose']), ('a disaccharide', ['sucrose', 'maltose', 'lactose']),
               ('a polysaccharide', ['starch', 'cellulose', 'glycogen'])],
    'groups2': [('a reducing sugar', ['glucose', 'fructose', 'maltose', 'lactose']), ('a non-reducing carbohydrate', ['sucrose', 'starch', 'cellulose'])],
    'tf': (['Glucose gives n-hexane on prolonged heating with HI.', 'Sucrose is a non-reducing sugar.', 'Cellulose is a straight-chain polymer of β-D-glucose.',
            'Amylose is water soluble and forms 15–20% of starch.', 'Glucose does not give Schiff\'s test, which supports its cyclic structure.'],
           [('Sucrose is a reducing sugar.', 'In sucrose the reducing groups of both glucose and fructose are used in the glycosidic bond, so it is non-reducing.'),
            ('Cellulose is a polymer of α-D-glucose.', 'Cellulose is made of β-D-glucose units linked C1–C4.'),
            ('Maltose consists of glucose and fructose.', 'Maltose consists of two α-D-glucose units linked C1–C4.'),
            ('Amylopectin is an unbranched chain.', 'Amylopectin is branched, with C1–C6 links at branch points.')]),
    'ar': [('Glucose does not form a hydrogensulphite addition product with NaHSO₃.', 'Glucose exists mainly as a cyclic hemiacetal with no free –CHO group.', 'a', 'Evidence for the ring structure.'),
           ('Sucrose is called a non-reducing sugar.', 'The reducing groups of glucose and fructose are involved in the glycosidic bond.', 'a', 'No free hemiacetal.'),
           ('Glucose pentaacetate does not react with hydroxylamine.', 'Glucose pentaacetate has no free –OH at C1.', 'a', 'Cannot open to the free aldehyde.'),
           ('Hydrolysis of sucrose gives a dextrorotatory product.', 'Fructose has a larger laevorotation than the dextrorotation of glucose.', 'd', 'The product (invert sugar) is laevorotatory; the reason is true.')],
    'features': {'intro': 'A carbohydrate has these features:', 'q': 'Identify the carbohydrate', 'what': 'carbohydrate', 'long': False,
                 'items': [('sucrose', ['disaccharide of α-D-glucose and β-D-fructose', 'C1–C2 glycosidic linkage', 'non-reducing sugar', 'gives invert sugar on hydrolysis']),
                           ('maltose', ['disaccharide of two α-D-glucose units', 'C1–C4 glycosidic linkage', 'reducing sugar', 'formed by the action of diastase on starch']),
                           ('lactose', ['milk sugar', 'β-D-galactose and β-D-glucose', 'C1 of galactose linked to C4 of glucose', 'reducing sugar']),
                           ('starch', ['storage carbohydrate of plants', 'amylose (15–20%) and amylopectin (80–85%)', 'gives blue colour with iodine', 'polymer of α-glucose']),
                           ('cellulose', ['main component of plant cell walls', 'straight chain of β-D-glucose', 'C1–C4 β-glycosidic links', 'cannot be digested by humans'])]},
    'fams': [F('C3', 'D3', 'mcq', glu_rx), F('C3', 'D3', 'numerical', stereo_sugar), F('C4', 'D4', 'multi_step', sucrose_hyd)],
    'qa': [('C4', 'D5', 'long', 'Give the evidence that glucose has (i) a straight chain of six carbons, (ii) a carbonyl group, (iii) an aldehyde group, (iv) five –OH groups, and (v) explain which facts cannot be explained by the open-chain structure.',
            '(i) HI gives n-hexane. (ii) Forms oxime with NH₂OH and cyanohydrin with HCN. (iii) Bromine water oxidises it to gluconic acid. (iv) Acetylation gives a pentaacetate. (v) No Schiff\'s test or NaHSO₃ addition; pentaacetate does not react with NH₂OH; existence of α and β forms — explained by the cyclic hemiacetal (pyranose) structure.',
            '1 mark each.')],
}

CH10S2 = {
    'topic': 'proteins',
    'terms': [('a peptide bond', 'the amide linkage –CO–NH– formed between the –COOH group of one amino acid and the –NH₂ group of another'),
              ('an essential amino acid', 'an amino acid that cannot be synthesised in the body and must be obtained from the diet'),
              ('a zwitterion', 'the dipolar ion formed when the –COOH group of an amino acid loses a proton to its own –NH₂ group'),
              ('denaturation', 'the loss of biological activity of a protein when its secondary and tertiary structures are destroyed by heat or pH change'),
              ('the primary structure of a protein', 'the specific sequence in which amino acids are linked in a polypeptide chain'),
              ('the α-helix', 'a secondary structure in which a polypeptide chain forms a right-handed coil held by hydrogen bonds between –NH and –CO groups')],
    'groups': [('an essential amino acid', ['valine', 'leucine', 'lysine', 'phenylalanine']), ('a non-essential amino acid', ['glycine', 'alanine', 'serine', 'glutamic acid'])],
    'groups2': [('a fibrous protein', ['keratin', 'myosin', 'collagen']), ('a globular protein', ['insulin', 'albumin', 'haemoglobin'])],
    'tf': (['Glycine is the only common α-amino acid that is not optically active.', 'Boiling an egg denatures its proteins.', 'Amino acids exist as zwitterions in aqueous solution.',
            'The primary structure of a protein is not changed on denaturation.', 'Keratin is a fibrous protein.'],
           [('Denaturation breaks the peptide bonds of a protein.', 'Denaturation destroys secondary and tertiary structures; the primary structure (peptide bonds) is intact.'),
            ('Glycine is optically active.', 'Glycine (H₂NCH₂COOH) has two H on the α-carbon and is optically inactive.'),
            ('Insulin is a fibrous protein.', 'Insulin is a globular protein.'),
            ('The α-helix is held by disulphide bonds only.', 'It is held mainly by intramolecular hydrogen bonds between –NH and –C=O groups.')]),
    'orders': [('order of levels of protein structure', ['primary', 'secondary', 'tertiary', 'quaternary'], 'Sequence → local folding (α-helix/β-sheet) → overall folding → association of subunits.', '→')],
    'ar': [('Amino acids have high melting points.', 'Amino acids exist as zwitterions with strong electrostatic attractions.', 'a', 'Salt-like character.'),
           ('Curdling of milk is denaturation.', 'Lactic acid formed by bacteria changes the pH and disturbs the protein structure.', 'a', 'pH change denatures proteins.'),
           ('Glycine is optically active.', 'Glycine has two hydrogen atoms on its α-carbon.', 'd', 'Glycine is optically inactive; the reason is true and explains why.'),
           ('The primary structure of a protein is lost on denaturation.', 'Denaturation disturbs hydrogen bonds and other weak forces.', 'd', 'The primary structure stays; only higher structures are lost. The reason is true.')],
    'features': {'intro': 'A level of protein structure has these features:', 'q': 'Which level of structure is described', 'what': 'level', 'case': False,
                 'items': [('primary structure', ['sequence of amino acids', 'held by peptide bonds', 'any change gives a different protein', 'not affected by denaturation']),
                           ('secondary structure', ['α-helix or β-pleated sheet', 'hydrogen bonds between –CO and –NH groups', 'local shape of the backbone', 'lost on denaturation']),
                           ('tertiary structure', ['overall folding of the chain', 'gives fibrous or globular shapes', 'held by H-bonds, disulphide links, van der Waals and electrostatic forces', 'lost on denaturation']),
                           ('quaternary structure', ['arrangement of two or more polypeptide subunits', 'shown by haemoglobin with four subunits', 'held by non-covalent forces', 'only in proteins with several chains'])]},
    'fams': [F('C3', 'D3', 'numerical', peptide_mass), F('C4', 'D4', 'multi_step', lambda r: peptide_mass(r, (4, 5))), F('C3', 'D3', 'mcq', peptide_count)],
    'qa': [('C4', 'D4', 'explain', 'What happens to the structure of a protein when it is denatured? Give two examples of denaturation from daily life.',
            'Hydrogen bonds and other weak interactions are broken; the globules unfold and helices uncoil, so secondary and tertiary structures are lost and biological activity is lost, though the primary structure remains. Examples: coagulation of egg white on boiling; curdling of milk by lactic acid.',
            '1 mark change; 1 mark two examples.'),
           ('C4', 'D3', 'case', 'Nikita learns that she cannot make some amino acids in her body and must get them from dal, milk and eggs.\n(i) What are such amino acids called? Give two examples. (2 marks)\n(ii) Why do amino acids behave like salts? (1 mark)\n(iii) Write the structure of the dipeptide Gly–Ala. (1 mark)',
            '(i) Essential amino acids, e.g. valine, leucine (lysine, phenylalanine). (ii) They exist as zwitterions (H₃N⁺–CHR–COO⁻). (iii) H₂N–CH₂–CO–NH–CH(CH₃)–COOH.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',))],
}

CH10S3 = {
    'topic': 'enzymes, vitamins and hormones',
    'terms': [('an enzyme', 'a biological catalyst, usually a globular protein, that speeds up a specific reaction'),
              ('a vitamin', 'an organic compound required in small amounts in the diet for normal growth and health'),
              ('a hormone', 'a chemical messenger produced by endocrine glands and carried by blood to target organs'),
              ('a fat-soluble vitamin', 'a vitamin such as A, D, E or K that is stored in the liver and adipose tissue'),
              ('a water-soluble vitamin', 'a vitamin such as those of the B group or C that must be supplied regularly in the diet')],
    'groups': [('a fat-soluble vitamin', ['vitamin A', 'vitamin D', 'vitamin E', 'vitamin K']), ('a water-soluble vitamin', ['vitamin B₁', 'vitamin B₂', 'vitamin B₆', 'vitamin C'])],
    'groups2': [('a hormone that regulates blood glucose', ['insulin', 'glucagon']), ('a steroid hormone', ['estrogen', 'testosterone', 'progesterone', 'cortisol']),
                ('an enzyme', ['maltase', 'invertase', 'pepsin', 'trypsin'])],
    'tf': (['Enzymes are highly specific in their action.', 'Enzymes lower the activation energy of reactions.', 'Vitamin B₁₂ is stored in the liver although it is water soluble.',
            'Insulin and glucagon together keep the blood glucose level in a narrow range.', 'Deficiency of thyroxine causes hypothyroidism.'],
           [('Vitamin C is a fat-soluble vitamin.', 'Vitamin C is water soluble and must be taken regularly.'),
            ('Enzymes raise the activation energy of reactions.', 'They lower the activation energy.'),
            ('Deficiency of vitamin D causes scurvy.', 'Vitamin D deficiency causes rickets/osteomalacia; scurvy is due to vitamin C deficiency.'),
            ('Insulin raises the blood glucose level.', 'Insulin lowers blood glucose; glucagon raises it.')]),
    'ar': [('Vitamin C must be supplied regularly in the diet.', 'Vitamin C is water soluble and is excreted in urine.', 'a', 'It cannot be stored.'),
           ('Enzymes speed up reactions.', 'Enzymes lower the activation energy.', 'a', 'Lower Ea means faster rate.'),
           ('Vitamin A is stored in the body.', 'Vitamin A is water soluble.', 'c', 'Vitamin A is fat soluble and is stored in liver and adipose tissue.')],
    'fams': [F('C2', 'D2', 'mcq', vit_def)],
    'qa': [('C3', 'D3', 'explain', 'Why must vitamin C be supplied regularly in our diet while vitamin A need not be?',
            'Vitamin C is water soluble and is readily excreted in urine, so it cannot be stored. Vitamin A is fat soluble and is stored in liver and adipose tissue.',
            '1 mark each.'),
           ('C4', 'D4', 'explain', 'Explain how enzymes act as catalysts. How are they different from ordinary chemical catalysts?',
            'Enzymes provide a different pathway with lower activation energy; the substrate binds to the active site to form an enzyme–substrate complex that breaks down to products. They are proteins, highly specific, work at mild temperature and pH, and are needed in very small amounts.',
            '1 mark mechanism; 1 mark differences.'),
           ('C4', 'D3', 'case', 'A doctor in Lucknow sees three children: one with bleeding gums, one with bow legs, and one who cannot see well in dim light.\n(i) Identify the vitamin deficient in each. (3 marks)\n(ii) Which of these vitamins are fat soluble? (1 mark)',
            '(i) Bleeding gums: vitamin C (scurvy); bow legs: vitamin D (rickets); poor dim-light vision: vitamin A (night blindness). (ii) Vitamins A and D.',
            '(i) 3 (ii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Classify vitamins with examples. Name the deficiency diseases of vitamins A, B₁, B₁₂, C and D. Why is vitamin B₁₂ an exception?',
            'Fat soluble (A, D, E, K) and water soluble (B group, C). A: xerophthalmia/night blindness; B₁: beriberi; B₁₂: pernicious anaemia; C: scurvy; D: rickets/osteomalacia. Vitamin B₁₂ is water soluble but is stored in the liver.',
            '1 mark classification; 3 marks diseases; 1 mark exception.')],
}

CH10S4 = {
    'topic': 'nucleic acids',
    'terms': [('a nucleoside', 'a unit formed by a nitrogenous base attached to C1′ of a pentose sugar'),
              ('a nucleotide', 'a nucleoside joined to a phosphoric acid group at C5′ of the sugar'),
              ('a phosphodiester linkage', 'the link between the 5′ and 3′ carbons of the sugars of adjacent nucleotides through a phosphate group'),
              ('the double helix', 'the structure of DNA in which two complementary polynucleotide strands are coiled around a common axis'),
              ('replication', 'the process by which a DNA molecule makes an identical copy of itself'),
              ('Chargaff\'s rule', 'the observation that in double-stranded DNA the amount of A equals T and the amount of G equals C')],
    'groups': [('a purine base', ['adenine', 'guanine']), ('a pyrimidine base', ['cytosine', 'thymine', 'uracil']),
               ('a pentose sugar found in nucleic acids', ['ribose', '2-deoxyribose'])],
    'classify': False,
    'tf': (['The sugar in DNA is 2-deoxyribose.', 'In DNA, adenine pairs with thymine and guanine with cytosine.', 'RNA is usually single stranded.',
            'Nucleotides are joined by phosphodiester linkages.', 'DNA is responsible for transmission of heredity.'],
           [('RNA contains thymine.', 'RNA contains uracil in place of thymine.'),
            ('The sugar in RNA is 2-deoxyribose.', 'RNA contains ribose; DNA contains 2-deoxyribose.'),
            ('In DNA, adenine pairs with guanine.', 'Adenine pairs with thymine (two H-bonds); guanine pairs with cytosine (three H-bonds).'),
            ('DNA and RNA both have a double helix structure.', 'DNA is a double helix; RNA is usually a single strand.')]),
    'ar': [('The two strands of DNA are complementary.', 'Hydrogen bonds form only between specific base pairs, A with T and G with C.', 'a', 'Specific pairing.'),
           ('RNA does not contain thymine.', 'Uracil replaces thymine in RNA.', 'a', 'U pairs with A.'),
           ('A nucleoside contains a phosphate group.', 'A nucleotide is a nucleoside with a phosphate.', 'd', 'A nucleoside is only base + sugar; the reason is true.')],
    'features': {'intro': 'A nucleic acid has these features:', 'q': 'Identify the nucleic acid', 'what': 'nucleic acid', 'compare': True,
                 'items': [('DNA', ['sugar is 2-deoxyribose', 'bases A, G, C and T', 'double-stranded helix', 'can replicate and carries hereditary information']),
                           ('RNA', ['sugar is ribose', 'bases A, G, C and U', 'usually single-stranded', 'directs protein synthesis'])]},
    'fams': [F('C3', 'D3', 'numerical', chargaff), F('C3', 'D3', 'mcq', complement)],
    'qa': [('C4', 'D4', 'explain', 'What is the difference between a nucleoside and a nucleotide? Draw a simple scheme of the structure of a dinucleotide.',
            'Nucleoside = base + sugar (base at C1′); nucleotide = nucleoside + phosphate at C5′. Dinucleotide: base–sugar–phosphate–sugar–base, the phosphate joining C5′ of one sugar to C3′ of the next (phosphodiester link).',
            '1 mark difference; 1 mark scheme.'),
           ('C4', 'D3', 'case', 'Kabir reads that a DNA sample from a plant contains 30% adenine.\n(i) What percentages of thymine, guanine and cytosine are present? (2 marks)\n(ii) Which bases pair by three hydrogen bonds? (1 mark)\n(iii) Name the sugar present. (1 mark)',
            '(i) T 30%, G 20%, C 20%. (ii) Guanine and cytosine. (iii) 2-Deoxyribose (β-D-2-deoxyribose).',
            '(i) 2 (ii) 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the structure of DNA. Give three differences between DNA and RNA and state the biological functions of each.',
            'DNA: two antiparallel polynucleotide strands of 2-deoxyribose, phosphate and bases A, G, C, T, coiled in a double helix with A=T and G≡C base pairing by hydrogen bonds. Differences: sugar (deoxyribose vs ribose), bases (T vs U), double vs single strand. Functions: DNA stores and transmits heredity and replicates; RNA (m-, t-, r-RNA) carries out protein synthesis.',
            '2 marks structure; 2 marks differences; 1 mark functions.')],
}

SPECS = {'ch07-st1': CH7S1, 'ch07-st2': CH7S2, 'ch07-st3': CH7S3, 'ch07-st4': CH7S4,
         'ch08-st1': CH8S1, 'ch08-st2': CH8S2, 'ch08-st3': CH8S3, 'ch08-st4': CH8S4,
         'ch09-st1': CH9S1, 'ch09-st2': CH9S2, 'ch09-st3': CH9S3,
         'ch10-st1': CH10S1, 'ch10-st2': CH10S2, 'ch10-st3': CH10S3, 'ch10-st4': CH10S4}
FAMILIES = build_all(P, SPECS)
