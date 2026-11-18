"""CBSE class 11 chemistry families, units 4-6 (Chemical bonding, Thermodynamics, Equilibrium)."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap

P = 'cbse-g11-chemistry'
SUPD = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')

# ---------------- ch04 st1 Kossel-Lewis, ionic/covalent, formal charge ----------------

VAL = {'H': 1, 'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Cl': 7, 'S': 6, 'P': 5, 'Be': 2, 'Br': 7, 'Si': 4, 'Xe': 8, 'I': 7, 'Al': 3}
VSP = [  # display, composition, charge
    ('CO₃²⁻', {'C': 1, 'O': 3}, -2), ('NO₃⁻', {'N': 1, 'O': 3}, -1), ('SO₄²⁻', {'S': 1, 'O': 4}, -2), ('NH₄⁺', {'N': 1, 'H': 4}, 1),
    ('CN⁻', {'C': 1, 'N': 1}, -1), ('H₂O', {'H': 2, 'O': 1}, 0), ('CO₂', {'C': 1, 'O': 2}, 0), ('PCl₅', {'P': 1, 'Cl': 5}, 0),
    ('O₃', {'O': 3}, 0), ('HNO₃', {'H': 1, 'N': 1, 'O': 3}, 0), ('NO₂⁻', {'N': 1, 'O': 2}, -1), ('PO₄³⁻', {'P': 1, 'O': 4}, -3),
    ('SF₆', {'S': 1, 'F': 6}, 0), ('BF₃', {'B': 1, 'F': 3}, 0), ('H₃O⁺', {'H': 3, 'O': 1}, 1), ('CH₃⁺', {'C': 1, 'H': 3}, 1),
    ('C₂H₄', {'C': 2, 'H': 4}, 0), ('HCN', {'H': 1, 'C': 1, 'N': 1}, 0), ('ClO₄⁻', {'Cl': 1, 'O': 4}, -1), ('XeF₄', {'Xe': 1, 'F': 4}, 0)]


def val_electrons(r):
    f, comp, q = r.choice(VSP)
    n = sum(VAL[e] * k for e, k in comp.items()) - q
    parts = ' + '.join(f'{k} × {VAL[e]} ({e})' if k > 1 else f'{VAL[e]} ({e})' for e, k in comp.items())
    extra = f' + {-q} (charge)' if q < 0 else (f' − {q} (charge)' if q > 0 else '')
    return {'stem': f'How many valence electrons must be shown in the Lewis structure of {f}?', 'answer': str(n),
            'key': f'{parts}{extra} = {n}.', 'distractors': [str(n + 2 * (q or 1)), str(n - q if q else n + 1), str(n + 8)]}


FC = [('O₃', 'the central O atom', '+1', 'V = 6, lone-pair electrons = 2, bonding electrons = 6: 6 − 2 − ½(6) = +1'),
      ('O₃', 'the O atom joined by a single bond', '−1', '6 − 6 − ½(2) = −1'),
      ('O₃', 'the O atom joined by a double bond', '0', '6 − 4 − ½(4) = 0'),
      ('CO (:C≡O:)', 'the C atom', '−1', '4 − 2 − ½(6) = −1'), ('CO (:C≡O:)', 'the O atom', '+1', '6 − 2 − ½(6) = +1'),
      ('NH₄⁺', 'the N atom', '+1', '5 − 0 − ½(8) = +1'), ('NO₃⁻', 'the N atom', '+1', '5 − 0 − ½(8) = +1'),
      ('NO₃⁻', 'a singly bonded O atom', '−1', '6 − 6 − ½(2) = −1'), ('H₃O⁺', 'the O atom', '+1', '6 − 2 − ½(6) = +1'),
      ('CO₂ (O=C=O)', 'the C atom', '0', '4 − 0 − ½(8) = 0'), ('CN⁻ ([:C≡N:]⁻)', 'the C atom', '−1', '4 − 2 − ½(6) = −1'),
      ('BF₄⁻', 'the B atom', '−1', '3 − 0 − ½(8) = −1')]


def formal_charge(r):
    sp, atom, fc, why = r.choice(FC)
    wrong = [x for x in ['+1', '−1', '0', '+2', '−2'] if x != fc]
    return mcq(f'Calculate the formal charge on {atom} in {sp}.', fc, r.sample(wrong, 3),
               f'Formal charge = V − L − ½B: {why}.', r)


LATTICE_ORDER = [('increasing order of lattice enthalpy', ['KCl', 'NaCl', 'LiCl'], 'Smaller cation, closer ions and stronger attraction: K⁺ > Na⁺ > Li⁺ in size.', '<'),
                 ('increasing order of lattice enthalpy', ['NaCl', 'MgO', 'Al₂O₃'], 'Higher ionic charges give much larger lattice enthalpies.', '<'),
                 ('increasing order of covalent character', ['NaCl', 'MgCl₂', 'AlCl₃'], "By Fajans' rules, higher charge and smaller cation polarise the anion more.", '<')]

CH4S1 = {
    'topic': 'ionic and covalent bonding',
    'terms': [('the octet rule', 'the tendency of atoms to gain, lose or share electrons so as to have eight electrons in their valence shell'),
              ('a covalent bond', 'a bond formed by the mutual sharing of a pair of electrons between two atoms'),
              ('an ionic bond', 'the electrostatic attraction between oppositely charged ions formed by transfer of electrons'),
              ('a coordinate bond', 'a covalent bond in which both shared electrons are provided by one atom'),
              ('formal charge', 'the difference between the valence electrons of a free atom and the electrons assigned to it in a Lewis structure'),
              ('lattice enthalpy', 'the energy required to completely separate one mole of a solid ionic compound into gaseous ions'),
              ('a lone pair', 'a pair of valence electrons not involved in bonding')],
    'groups': [('a molecule with an incomplete octet on the central atom', ['BeCl₂', 'BCl₃', 'LiCl', 'BF₃', 'AlCl₃']),
               ('a molecule with an expanded octet', ['PCl₅', 'SF₆', 'H₂SO₄', 'IF₇', 'XeF₄']),
               ('an odd-electron molecule', ['NO', 'NO₂', 'ClO₂'])],
    'groups2': [('an ionic compound', ['NaCl', 'MgO', 'CaF₂', 'KBr', 'Na₂O']), ('a covalent compound', ['CH₄', 'NH₃', 'CCl₄', 'H₂O', 'SO₂'])],
    'tf': (['Formation of an ionic bond is favoured by low ionisation enthalpy of the metal and highly negative electron gain enthalpy of the non-metal.',
            'The octet rule cannot explain the shapes of molecules.', 'Noble gases like xenon form compounds such as XeF₂ and XeF₄.',
            'In NH₄⁺ one N–H bond is a coordinate bond, but all four bonds become identical.', 'The lowest-energy Lewis structure usually has the smallest formal charges on the atoms.'],
           [('The octet rule explains the stability of all molecules.', 'Many molecules (BF₃, PCl₅, NO) do not obey the octet rule.'),
            ('In BF₃ boron has eight electrons around it.', 'Boron in BF₃ has only six electrons (incomplete octet).'),
            ('Formal charges represent real charges on the atoms in a molecule.', 'Formal charges are a bookkeeping device; they do not show the real charge distribution.'),
            ('Lattice enthalpy decreases with increase in the charges on the ions.', 'Lattice enthalpy increases with higher ionic charges and smaller ionic size.')]),
    'orders': LATTICE_ORDER,
    'ar': [('BF₃ does not obey the octet rule.', 'Boron has only three valence electrons to share.', 'a', 'Sharing three electrons gives B only six electrons in BF₃.'),
           ('Ionic compounds have high melting points.', 'A large amount of energy is needed to break the strong electrostatic forces in the lattice.', 'a', 'Strong attraction between ions in the lattice causes high melting points.')],
    'fams': [F('C2', 'D2', 'short', val_electrons), F('C3', 'D3', 'mcq', formal_charge)],
    'qa': [('C4', 'D4', 'explain', 'Write two resonance-free Lewis structures for CO₂: O=C=O and O≡C–O. Use formal charges to decide which is preferred.',
            'O=C=O: all formal charges 0. O≡C–O: +1 on the triply bonded O, −1 on the singly bonded O. The structure with zero formal charges (O=C=O) is preferred.',
            '1 mark: formal charges on both; 1 mark: lowest formal charges preferred.'),
           ('C4', 'D3', 'explain', 'Although NaCl is formed from Na⁺ and Cl⁻ ions, the formation of Na⁺(g) and Cl⁻(g) from atoms is endothermic overall. Why then does NaCl form so readily?',
            'The large lattice enthalpy released when gaseous ions come together to form the crystal more than compensates for the energy needed to form the ions.',
            '1 mark: ion formation net endothermic (IE > |EGE|); 1 mark: lattice enthalpy makes the overall process exothermic.')],
}

# ---------------- ch04 st2 bond parameters, resonance, polarity ----------------

def dipole(r):
    q = r.choice([0.2, 0.3, 0.4, 0.5, 0.6]) * 1.602e-19
    d = r.choice([92, 100, 115, 127, 141, 160]) * 1e-12
    mu = q * d / 3.336e-30
    return {'stem': f'In a diatomic molecule the partial charges are ±{q / 1.602e-19:.1f}e and the bond length is {d * 1e12:.0f} pm. Calculate the dipole moment in debye. (e = 1.602 × 10⁻¹⁹ C, 1 D = 3.336 × 10⁻³⁰ C m)',
            'answer': f'{mu:.2f} D', 'key': f'μ = q × d = {q:.3e} C × {d:.3e} m = {q * d:.3e} C m (1) = {mu:.2f} D (1).'.replace('e-', ' × 10^-'),
            'distractors': [f'{mu * 2:.2f} D', f'{mu / 3.336:.2f} D', f'{mu * 10:.2f} D']}


BO_RES = [('O₃', '1.5', 'two equivalent resonance structures with one single and one double bond'),
          ('CO₃²⁻', '1.33', 'three resonance structures share one double bond among three C–O bonds'),
          ('NO₃⁻', '1.33', 'three resonance structures share one double bond among three N–O bonds'),
          ('benzene (C–C)', '1.5', 'two Kekulé structures give each C–C bond half double-bond character'),
          ('NO₂⁻', '1.5', 'two resonance structures share one double bond between two N–O bonds'),
          ('SO₄²⁻ (S–O, with two S=O in each structure)', '1.5', 'six resonance structures share two double bonds among four S–O bonds'),
          ('HCOO⁻ (C–O)', '1.5', 'two resonance structures share one double bond between two C–O bonds')]


def res_bond_order(r):
    sp, bo, why = r.choice(BO_RES)
    wrong = [x for x in ['1', '1.33', '1.5', '2', '1.25', '0.5'] if x != bo]
    return mcq(f'What is the average bond order of the bonds in {sp}?', bo, r.sample(wrong[:4], 3), f'{bo}: {why}.', r)


CH4S2 = {
    'topic': 'bond parameters, resonance and polarity',
    'terms': [('bond length', 'the equilibrium distance between the nuclei of two bonded atoms in a molecule'),
              ('bond enthalpy', 'the amount of energy required to break one mole of bonds of a particular type between two atoms in the gaseous state'),
              ('bond order', 'the number of bonds between two atoms in a molecule'),
              ('resonance', 'the representation of a molecule by two or more Lewis structures, none of which alone describes it fully'),
              ('the resonance hybrid', 'the actual structure of a molecule, intermediate between its canonical forms'),
              ('dipole moment', 'the product of the magnitude of the charge and the distance between the centres of positive and negative charge'),
              ('bond angle', 'the angle between the orbitals containing bonding electron pairs around the central atom')],
    'groups': [('a polar molecule', ['H₂O', 'NH₃', 'CHCl₃', 'SO₂', 'NF₃', 'HCl']), ('a non-polar molecule', ['CO₂', 'BF₃', 'CCl₄', 'CH₄', 'BeF₂', 'PCl₅'])],
    'orders': [('increasing order of C–C bond length', ['C≡C (ethyne)', 'C=C (ethene)', 'C–C in benzene', 'C–C (ethane)'], 'Higher bond order gives a shorter bond: 3 > 2 > 1.5 > 1.', '<'),
               ('increasing order of bond enthalpy', ['C–C', 'C=C', 'C≡C'], 'Bond enthalpy increases with bond order.', '<'),
               ('increasing order of dipole moment', ['CCl₄', 'NF₃', 'NH₃', 'H₂O'], 'CCl₄ is zero (symmetric); in NF₃ the lone-pair moment opposes the bond moments; NH₃ (1.47 D) is lower than H₂O (1.85 D).', '<'),
               ('increasing order of bond length', ['H–F', 'H–Cl', 'H–Br', 'H–I'], 'Halogen atom size increases from F to I.', '<')],
    'tf': (['CO₂ has zero dipole moment because it is linear.', 'Bond length decreases as bond order increases.',
            'The dipole moment of NH₃ is greater than that of NF₃.', 'Resonance stabilises a molecule.',
            'The canonical forms of a molecule have no real existence.'],
           [('The canonical structures of a molecule exist in equilibrium with each other.', 'Canonical forms have no real existence; the molecule is a single resonance hybrid.'),
            ('BF₃ is polar because each B–F bond is polar.', 'BF₃ is non-polar because the three bond dipoles in its trigonal planar shape cancel.'),
            ('The dipole moment of NF₃ is greater than that of NH₃.', 'In NF₃ the lone-pair dipole opposes the N–F bond dipoles, so its moment (0.24 D) is less than NH₃ (1.47 D).'),
            ('A triple bond is longer than a double bond between the same two atoms.', 'A triple bond is shorter than a double bond.'),
            ('The unit of dipole moment is the newton.', 'Dipole moment is measured in debye (1 D = 3.336 × 10⁻³⁰ C m).')]),
    'ar': [('All the C–O bonds in CO₃²⁻ are of equal length.', 'CO₃²⁻ is a resonance hybrid of three equivalent canonical structures.', 'a', 'Delocalisation makes each C–O bond of order 1.33.'),
           ('H₂O has a net dipole moment.', 'H₂O is a bent molecule, so its bond dipoles do not cancel.', 'a', 'Bent shape leaves a resultant dipole of 1.85 D.'),
           ('CCl₄ is non-polar.', 'The C–Cl bond is non-polar.', 'c', 'A is true because of the symmetric tetrahedral shape; but C–Cl bonds are polar, so R is false.')],
    'fams': [F('C3', 'D3', 'numerical', dipole), F('C3', 'D2', 'mcq', res_bond_order)],
    'qa': [('C4', 'D4', 'explain', 'Both BeF₂ and H₂O are triatomic molecules with polar bonds. Why does BeF₂ have zero dipole moment while H₂O has 1.85 D?',
            'BeF₂ is linear, so the two equal Be–F bond dipoles cancel. H₂O is bent (104.5°) due to two lone pairs, so the O–H bond dipoles add to a resultant.',
            '1 mark: BeF₂ linear, cancellation; 1 mark: H₂O bent, resultant.'),
           ('C4', 'D3', 'explain', 'Use resonance to explain why both O–O bonds in ozone have the same length (128 pm), intermediate between O–O (148 pm) and O=O (121 pm).',
            'O₃ is a resonance hybrid of two structures with the double bond in either position; each O–O bond has bond order 1.5, so both lengths are equal and intermediate.',
            '1 mark: two canonical forms; 1 mark: bond order 1.5 ⇒ equal, intermediate length.')],
}

# ---------------- ch04 st3 VSEPR ----------------

VSEPR = [  # species, bp, lp, shape, hybridisation, angle note
    ('BeCl₂', 2, 0, 'linear', 'sp', '180°'), ('BF₃', 3, 0, 'trigonal planar', 'sp²', '120°'), ('CH₄', 4, 0, 'tetrahedral', 'sp³', '109.5°'),
    ('NH₃', 3, 1, 'trigonal pyramidal', 'sp³', '107°'), ('H₂O', 2, 2, 'bent (V-shaped)', 'sp³', '104.5°'), ('PCl₅', 5, 0, 'trigonal bipyramidal', 'sp³d', '120° and 90°'),
    ('SF₄', 4, 1, 'see-saw', 'sp³d', 'distorted'), ('ClF₃', 3, 2, 'T-shaped', 'sp³d', 'about 87.5°'), ('XeF₂', 2, 3, 'linear', 'sp³d', '180°'),
    ('SF₆', 6, 0, 'octahedral', 'sp³d²', '90°'), ('BrF₅', 5, 1, 'square pyramidal', 'sp³d²', 'about 84.5°'), ('XeF₄', 4, 2, 'square planar', 'sp³d²', '90°'),
    ('SO₂', 2, 1, 'bent (V-shaped)', 'sp²', 'about 119°'), ('NH₄⁺', 4, 0, 'tetrahedral', 'sp³', '109.5°'), ('H₃O⁺', 3, 1, 'trigonal pyramidal', 'sp³', 'about 107°'),
    ('PCl₃', 3, 1, 'trigonal pyramidal', 'sp³', 'about 100°'), ('I₃⁻', 2, 3, 'linear', 'sp³d', '180°'), ('BCl₃', 3, 0, 'trigonal planar', 'sp²', '120°'),
    ('SiCl₄', 4, 0, 'tetrahedral', 'sp³', '109.5°'), ('H₂S', 2, 2, 'bent (V-shaped)', 'sp³', 'about 92°'), ('SO₃', 3, 0, 'trigonal planar', 'sp²', '120°'),
    ('NF₃', 3, 1, 'trigonal pyramidal', 'sp³', 'about 102°'), ('CO₂', 2, 0, 'linear', 'sp', '180°'), ('PF₅', 5, 0, 'trigonal bipyramidal', 'sp³d', '120° and 90°')]
SHAPES = sorted({x[3] for x in VSEPR})


def vsepr_shape(r):
    sp, bp, lp, sh, hy, ang = r.choice(VSEPR)
    wrong = r.sample([s for s in SHAPES if s != sh], 3)
    return mcq(f'According to VSEPR theory, what is the shape of {sp}?', sh, wrong, f'{sp}: {bp} bond pairs + {lp} lone pair(s) around the central atom ⇒ {sh} ({ang}).', r)


def vsepr_pairs(r):
    sp, bp, lp, sh, hy, ang = r.choice(VSEPR)
    return {'stem': f'How many bond pairs and lone pairs are there around the central atom of {sp}? Predict its shape.',
            'answer': f'{bp} bond pairs, {lp} lone pair{"s" if lp != 1 else ""}; {sh}',
            'key': f'Count the valence electrons of the central atom used in σ bonds and left over: {bp} bp + {lp} lp ⇒ electron geometry of {bp + lp} pairs; shape {sh} (1 + 1).',
            'distractors': [f'{bp} bond pairs, {lp + 1} lone pairs; {r.choice([s for s in SHAPES if s != sh])}', f'{bp + lp} bond pairs, 0 lone pairs; {r.choice([s for s in SHAPES if s != sh])}', f'{bp} bond pairs, {max(lp - 1, 0) if lp else 2} lone pairs; {r.choice([s for s in SHAPES if s != sh])}']}


def same_shape(r):
    a = r.choice(VSEPR)
    same = [x for x in VSEPR if x[3] == a[3] and x[0] != a[0]]
    if not same:
        raise ValueError
    b = r.choice(same)
    others = r.sample([x for x in VSEPR if x[3] != a[3]], 3)
    return mcq(f'Which of the following has the same shape as {a[0]}?', b[0], [x[0] for x in others],
               f'{a[0]} and {b[0]} are both {a[3]}; ' + '; '.join(f'{x[0]} is {x[3]}' for x in others) + '.', r)


CH4S3 = {
    'topic': 'VSEPR theory',
    'terms': [('VSEPR theory', 'the theory that the shape of a molecule depends on the number of valence-shell electron pairs around the central atom, which repel one another'),
              ('a bond pair', 'a pair of electrons shared between two atoms'),
              ('a lone pair', 'a pair of electrons on an atom that is not shared'),
              ('electron-pair geometry', 'the arrangement in space of all electron pairs (bond and lone) around the central atom')],
    'orders': [('decreasing order of repulsion between electron pairs', ['lone pair–lone pair', 'lone pair–bond pair', 'bond pair–bond pair'],
                'Lone pairs are held by only one nucleus and spread out more, so they repel more strongly.', '>'),
               ('decreasing order of bond angle', ['CH₄', 'NH₃', 'H₂O'], 'All have four electron pairs; each lone pair compresses the H–X–H angle: 109.5° > 107° > 104.5°.', '>'),
               ('decreasing order of bond angle', ['BeCl₂', 'BF₃', 'CH₄', 'NH₃', 'H₂O'], '180° > 120° > 109.5° > 107° > 104.5°.', '>')],
    'tf': (['Lone pair–lone pair repulsion is greater than bond pair–bond pair repulsion.', 'XeF₄ is square planar with two lone pairs on Xe.',
            'In SF₄ the lone pair occupies an equatorial position.', 'The bond angle in H₂O is smaller than in NH₃.', 'ClF₃ is T-shaped.'],
           [('NH₃ is trigonal planar.', 'NH₃ is trigonal pyramidal because of one lone pair on nitrogen.'),
            ('XeF₂ is bent like H₂O.', 'XeF₂ is linear: three lone pairs occupy the equatorial positions of a trigonal bipyramid.'),
            ('The H–O–H bond angle in water is 109.5°.', 'It is 104.5° because two lone pairs compress the angle.'),
            ('SF₆ is a square pyramidal molecule.', 'SF₆ is octahedral; BrF₅ is square pyramidal.'),
            ('Bond pair–bond pair repulsion is the strongest of all repulsions.', 'Lone pair–lone pair repulsion is the strongest.')]),
    'ar': [('The bond angle in NH₃ is less than 109.5°.', 'Lone pair–bond pair repulsion is greater than bond pair–bond pair repulsion.', 'a', 'The lone pair pushes the N–H bonds closer, giving 107°.'),
           ('XeF₄ is square planar.', 'In an octahedral electron geometry, two lone pairs sit opposite each other to minimise repulsion.', 'a', 'Six pairs (4 bp + 2 lp) with lone pairs trans leave a square plane of F atoms.')],
    'fams': [F('C2', 'D2', 'mcq', vsepr_shape), F('C3', 'D3', 'explain', vsepr_pairs), F('C3', 'D3', 'mcq', same_shape)],
    'qa': [('C4', 'D4', 'explain', 'Both BF₃ and NH₃ are AB₃ molecules, but BF₃ is planar and NH₃ is pyramidal. Explain using VSEPR theory.',
            'B in BF₃ has 3 bond pairs and no lone pair ⇒ trigonal planar. N in NH₃ has 3 bond pairs and 1 lone pair ⇒ tetrahedral electron geometry with pyramidal shape.',
            '1 mark each for correct electron-pair count and shape.'),
           ('C4', 'D5', 'long', 'Using VSEPR theory, predict the shapes of (a) SF₄, (b) ClF₃, (c) XeF₂, (d) BrF₅ and (e) XeF₄. For each, state the number of bond pairs and lone pairs on the central atom.',
            '(a) 4 bp, 1 lp – see-saw. (b) 3 bp, 2 lp – T-shaped. (c) 2 bp, 3 lp – linear. (d) 5 bp, 1 lp – square pyramidal. (e) 4 bp, 2 lp – square planar.',
            '1 mark each (pairs and shape).')],
}

# ---------------- ch04 st4 hybridisation ----------------

SIGMAPI = [('ethene (CH₂=CH₂)', 5, 1), ('ethyne (HC≡CH)', 3, 2), ('HCN', 2, 2), ('CO₂', 2, 2), ('N₂', 1, 2), ('benzene (C₆H₆)', 12, 3),
           ('buta-1,3-diene (CH₂=CH–CH=CH₂)', 9, 2), ('propene (CH₃–CH=CH₂)', 8, 1), ('propadiene (CH₂=C=CH₂)', 6, 2),
           ('acrylonitrile (CH₂=CH–C≡N)', 6, 3), ('propyne (CH₃–C≡CH)', 6, 2), ('methanal (HCHO)', 3, 1), ('ethanoic acid (CH₃COOH)', 7, 1),
           ('ethane (C₂H₆)', 7, 0), ('but-1-en-3-yne (CH₂=CH–C≡CH)', 7, 3)]


def sigma_pi(r):
    m, s, p = r.choice(SIGMAPI)
    return {'stem': f'How many σ and π bonds are present in {m}?', 'answer': f'{s} σ and {p} π',
            'key': f'Every single bond is one σ; a double bond is 1σ + 1π; a triple bond is 1σ + 2π ⇒ {s} σ, {p} π.',
            'distractors': [f'{s + p} σ and {p} π', f'{s} σ and {p + 1} π', f'{s - 1} σ and {p} π' if s > 1 else f'{s + 1} σ and {p} π']}


HYB_C = [('each carbon in ethene', 'sp²'), ('each carbon in ethyne', 'sp'), ('each carbon in ethane', 'sp³'), ('the carbon in CO₂', 'sp'),
         ('the central carbon in propadiene (CH₂=C=CH₂)', 'sp'), ('the carbon in HCHO', 'sp²'), ('each carbon in benzene', 'sp²'),
         ('the carbon in CH₄', 'sp³'), ('the nitrile carbon in CH₃C≡N', 'sp'), ('the carbonyl carbon in CH₃COOH', 'sp²'),
         ('the B atom in BF₃', 'sp²'), ('the Be atom in BeCl₂', 'sp'), ('the P atom in PCl₅', 'sp³d'), ('the S atom in SF₆', 'sp³d²'),
         ('the N atom in NH₃', 'sp³'), ('the O atom in H₂O', 'sp³'), ('the Xe atom in XeF₄', 'sp³d²'), ('the N atom in NH₄⁺', 'sp³')]
HYBS = ['sp', 'sp²', 'sp³', 'sp³d', 'sp³d²']


def hybrid(r):
    a, hy = r.choice(HYB_C)
    return mcq(f'What is the hybridisation of {a}?', hy, r.sample([x for x in HYBS if x != hy], 3),
               f'Count σ bonds + lone pairs on the atom: {hy}.', r)


def hyb_carbons(r):
    cands = [('CH₂=CH–CH₃', ['sp²', 'sp²', 'sp³']), ('HC≡C–CH₃', ['sp', 'sp', 'sp³']), ('CH₂=C=CH₂', ['sp²', 'sp', 'sp²']),
             ('CH₃–CH₂–OH', ['sp³', 'sp³']), ('HC≡C–CH=CH₂', ['sp', 'sp', 'sp²', 'sp²']), ('CH₃–CHO', ['sp³', 'sp²']),
             ('CH₂=CH–CN', ['sp²', 'sp²', 'sp']), ('CH₃–COOH', ['sp³', 'sp²']), ('CH₃–C≡N', ['sp³', 'sp']), ('CH₂=CH–CH=CH₂', ['sp²'] * 4)]
    m, hs = r.choice(cands)
    ans = ', '.join(f'C{i + 1}: {h}' for i, h in enumerate(hs))
    return {'stem': f'Number the carbon atoms from left to right in {m} and state the hybridisation of each.', 'answer': ans,
            'key': f'Four σ (single bonds only) ⇒ sp³; one double bond ⇒ sp²; one triple or two double bonds ⇒ sp: {ans}. (½ mark each)'}


CH4S4 = {
    'topic': 'hybridisation',
    'terms': [('hybridisation', 'the intermixing of atomic orbitals of slightly different energies to form an equal number of new orbitals of equivalent energy and shape'),
              ('a sigma (σ) bond', 'a bond formed by end-to-end (head-on) overlap of orbitals along the internuclear axis'),
              ('a pi (π) bond', 'a bond formed by sidewise overlap of p orbitals with axes parallel to each other'),
              ('valence bond theory', 'the theory that a covalent bond forms by overlap of half-filled atomic orbitals of the bonding atoms')],
    'features': {'intro': 'A central atom has the following hybridisation features:', 'q': 'Identify the type of hybridisation', 'what': 'hybridisation',
                 'items': [('sp', ['two hybrid orbitals at 180°', '50% s character', 'found in BeCl₂ and ethyne', 'linear arrangement']),
                           ('sp²', ['three hybrid orbitals at 120°', '33.3% s character', 'found in BF₃ and ethene', 'trigonal planar arrangement']),
                           ('sp³', ['four hybrid orbitals at 109.5°', '25% s character', 'found in CH₄ and C₂H₆', 'tetrahedral arrangement']),
                           ('sp³d', ['five hybrid orbitals', 'three equatorial and two axial positions', 'found in PCl₅', 'trigonal bipyramidal arrangement']),
                           ('sp³d²', ['six hybrid orbitals at 90°', 'found in SF₆', 'octahedral arrangement', 'uses two d orbitals'])]},
    'tf': (['A σ bond is stronger than a π bond.', 'Hybrid orbitals form only σ bonds.', 'The axial bonds in PCl₅ are longer than the equatorial bonds.',
            'Free rotation is possible about a C–C single bond but not about a C=C double bond.', 'sp hybrid orbitals have 50% s character.'],
           [('A π bond can be formed without a σ bond between two atoms.', 'A π bond is always formed in addition to a σ bond.'),
            ('Hybrid orbitals form π bonds.', 'Hybrid orbitals form σ bonds; π bonds come from unhybridised p orbitals.'),
            ('In PCl₅ all five P–Cl bonds are of equal length.', 'Axial P–Cl bonds (240 pm) are longer than equatorial ones (202 pm).'),
            ('sp³ orbitals have more s character than sp² orbitals.', 'sp³ has 25% and sp² has 33.3% s character.'),
            ('The overlap of a 1s and a 2p orbital always gives a π bond.', 's–p head-on overlap gives a σ bond.')]),
    'orders': [('increasing order of s character of the hybrid orbitals', ['sp³', 'sp²', 'sp'], 's character is 25%, 33.3% and 50%.', '<'),
               ('increasing order of electronegativity of carbon', ['sp³ carbon', 'sp² carbon', 'sp carbon'], 'More s character holds electrons closer to the nucleus.', '<')],
    'ar': [('PCl₅ is very reactive.', 'The two axial P–Cl bonds are longer and weaker than the equatorial bonds.', 'a', 'Weaker axial bonds break easily, making PCl₅ reactive.'),
           ('Ethyne is a linear molecule.', 'Each carbon in ethyne is sp hybridised.', 'a', 'sp hybrid orbitals point at 180°.')],
    'fams': [F('C3', 'D2', 'short', sigma_pi), F('C2', 'D2', 'mcq', hybrid), F('C3', 'D4', 'explain', hyb_carbons)],
    'qa': [('C4', 'D5', 'long', 'Describe the hybridisation in the formation of ethene. Show how the σ and π bonds are formed, and explain why ethene is planar and does not show free rotation about the C=C bond.',
            'Each C is sp² (2s + 2pₓ + 2p_y); two sp² orbitals overlap with H 1s, one with the other C (σ C–C). The unhybridised 2p_z orbitals overlap sideways to form the π bond. All σ bonds lie in one plane (120°); rotation would break the sideways π overlap.',
            '1 mark sp² hybridisation; 1 mark σ framework; 1 mark π bond from p_z; 1 mark planarity; 1 mark no free rotation.')],
}

# ---------------- ch04 st5 MO theory and hydrogen bonding ----------------

MO_SPECIES = [('H₂⁺', 1, False), ('H₂', 2, False), ('H₂⁻', 3, False), ('He₂⁺', 3, False), ('He₂', 4, False), ('Li₂', 6, False), ('Be₂', 8, False),
              ('B₂', 10, False), ('C₂', 12, False), ('N₂⁺', 13, False), ('N₂', 14, False), ('N₂⁻', 15, False), ('O₂⁺', 15, True), ('O₂', 16, True),
              ('O₂⁻', 17, True), ('O₂²⁻', 18, True), ('F₂', 18, True), ('Ne₂', 20, True)]
MO_LOW = [('σ1s', 2, 1), ('σ*1s', 2, -1), ('σ2s', 2, 1), ('σ*2s', 2, -1), ('π2p', 4, 1), ('σ2p', 2, 1), ('π*2p', 4, -1), ('σ*2p', 2, -1)]
MO_HIGH = [('σ1s', 2, 1), ('σ*1s', 2, -1), ('σ2s', 2, 1), ('σ*2s', 2, -1), ('σ2p', 2, 1), ('π2p', 4, 1), ('π*2p', 4, -1), ('σ*2p', 2, -1)]


def mo(nel, high):
    left, nb, na, unp, cfg = nel, 0, 0, 0, []
    for o, cap, s in (MO_HIGH if high else MO_LOW):
        if left <= 0:
            break
        k = min(cap, left)
        left -= k
        if s > 0:
            nb += k
        else:
            na += k
        cfg.append(f'({o}){str(k).translate(SUPD)}')
        if cap == 4:
            unp += k if k <= 2 else 4 - k
        else:
            unp += k % 2
    return nb, na, unp, ' '.join(cfg)


def mo_bo(r):
    sp, n, hi = r.choice(MO_SPECIES)
    nb, na, u, cfg = mo(n, hi)
    bo = (nb - na) / 2
    mag = 'paramagnetic' if u else 'diamagnetic'
    return {'stem': f'Using molecular orbital theory, calculate the bond order of {sp} and predict whether it is paramagnetic or diamagnetic.',
            'answer': f'Bond order {num(bo)}; {mag}',
            'key': f'{n} electrons: {cfg} (1); bond order = (N_b − N_a)/2 = ({nb} − {na})/2 = {num(bo)} (½); {u} unpaired electron(s) ⇒ {mag} (½).',
            'distractors': [f'Bond order {num(bo)}; {"diamagnetic" if u else "paramagnetic"}', f'Bond order {num(bo + 0.5)}; {mag}', f'Bond order {num(abs(bo - 1))}; {mag}']}


def mo_compare(r):
    fam = r.choice([['O₂²⁻', 'O₂⁻', 'O₂', 'O₂⁺'], ['N₂⁻', 'N₂⁺', 'N₂'], ['H₂⁻', 'H₂⁺', 'H₂'], ['Li₂', 'B₂', 'C₂', 'N₂']])
    data = {x[0]: x for x in MO_SPECIES}
    bos = []
    for sp in fam:
        _, n, hi = data[sp]
        nb, na, _, _ = mo(n, hi)
        bos.append((nb - na) / 2)
    if len(set(bos)) != len(bos):
        sub = []
        seen = set()
        for sp, b in zip(fam, bos):
            if b not in seen:
                sub.append((sp, b))
                seen.add(b)
    else:
        sub = list(zip(fam, bos))
    if len(sub) < 3:
        raise ValueError
    sub.sort(key=lambda x: x[1])
    good = ' < '.join(s for s, _ in sub)
    sh = sub[:]
    while sh == sub:
        r.shuffle(sh)
    return {'stem': f'Arrange {", ".join(s for s, _ in sh)} in increasing order of bond order and hence of stability. Show the bond orders.',
            'answer': good, 'key': 'Bond orders: ' + ', '.join(f'{s} {num(b)}' for s, b in sub) + f' ⇒ {good}. Higher bond order means greater stability and shorter bond.'}


CH4S5 = {
    'topic': 'molecular orbital theory and hydrogen bonding',
    'terms': [('a bonding molecular orbital', 'a molecular orbital formed by additive overlap of atomic orbitals, with electron density increased between the nuclei'),
              ('an antibonding molecular orbital', 'a molecular orbital formed by subtractive overlap, with a node between the nuclei and higher energy'),
              ('bond order', 'half the difference between the numbers of electrons in bonding and antibonding molecular orbitals'),
              ('a hydrogen bond', 'the attractive force that binds a hydrogen atom of one molecule (or group) to a highly electronegative atom of another'),
              ('LCAO', 'the linear combination of atomic orbitals used to form molecular orbitals'),
              ('a paramagnetic substance', 'a substance that is attracted by a magnetic field because it has unpaired electrons')],
    'groups': [('a compound showing intramolecular hydrogen bonding', ['o-nitrophenol', 'salicylaldehyde (o-hydroxybenzaldehyde)', 'o-hydroxybenzoic acid']),
               ('a compound showing intermolecular hydrogen bonding', ['p-nitrophenol', 'water', 'hydrogen fluoride', 'ethanol', 'ammonia']),
               ('a substance with no hydrogen bonding', ['methane', 'carbon tetrachloride', 'diethyl ether (pure)', 'benzene'])],
    'tf': (['O₂ is paramagnetic.', 'He₂ does not exist because its bond order is zero.', 'A bond order of zero means the molecule is not stable.',
            'Intermolecular hydrogen bonding raises the boiling point.', 'N₂ has a bond order of 3.'],
           [('O₂ is diamagnetic because all its electrons are paired.', 'O₂ has two unpaired electrons in π*2p orbitals and is paramagnetic.'),
            ('Antibonding molecular orbitals are lower in energy than bonding orbitals.', 'Antibonding orbitals are higher in energy than the combining atomic orbitals.'),
            ('o-Nitrophenol has a higher boiling point than p-nitrophenol.', 'o-Nitrophenol has intramolecular H-bonding and is more volatile; p-nitrophenol has intermolecular H-bonding and a higher boiling point.'),
            ('Bond order of O₂⁺ is less than that of O₂.', 'O₂⁺ has bond order 2.5, greater than O₂ (2).'),
            ('Hydrogen bonds are stronger than covalent bonds.', 'Hydrogen bonds are much weaker than covalent bonds.')]),
    'ar': [('O₂ is paramagnetic.', 'O₂ has two unpaired electrons in its antibonding π*2p orbitals.', 'a', 'Unpaired electrons make O₂ paramagnetic.'),
           ('Ice floats on water.', 'In ice each water molecule is hydrogen bonded to four others in an open cage-like structure.', 'a', 'The open structure makes ice less dense than water.'),
           ('HF is a liquid at 0 °C while HCl is a gas.', 'HF molecules are associated through strong intermolecular hydrogen bonds.', 'a', 'H-bonding raises the boiling point of HF (293 K).')],
    'fams': [F('C3', 'D3', 'explain', mo_bo), F('C4', 'D4', 'explain', mo_compare)],
    'qa': [('C4', 'D5', 'long', '(a) Write the molecular orbital configuration of N₂ and O₂. (b) Calculate their bond orders. (c) Explain why O₂ is paramagnetic but N₂ is diamagnetic. (d) Predict which of N₂ and N₂⁺ has the longer bond.',
            '(a) N₂: σ1s² σ*1s² σ2s² σ*2s² π2p⁴ σ2p²; O₂: … σ2p² π2p⁴ π*2p². (b) N₂ 3, O₂ 2. (c) O₂ has two unpaired π* electrons; N₂ has none. (d) N₂⁺ (bond order 2.5) has the longer bond.',
            '(a) 2 marks (b) 1 mark (c) 1 mark (d) 1 mark.'),
           ('C4', 'D3', 'explain', 'Ethanol (46 g mol⁻¹) boils at 351 K but dimethyl ether (46 g mol⁻¹) boils at 248 K. Explain.',
            'Ethanol molecules are associated by intermolecular hydrogen bonds (O–H…O), which need extra energy to break; dimethyl ether has no O–H and cannot H-bond with itself.',
            '1 mark: H-bonding in ethanol; 1 mark: none in ether.')],
}

# ---------------- ch05 st1 system, state functions, first law, work ----------------

R = 8.314


def work_irrev(r):
    p = r.choice([1, 1.5, 2, 2.5, 3, 5])
    V1 = r.choice([1, 2, 5, 10])
    V2 = V1 + r.choice([2, 3, 5, 8, 10, 15])
    w = -p * (V2 - V1)
    return {'stem': f'A gas expands isothermally against a constant external pressure of {p} bar from {V1} L to {V2} L. Calculate the work done in joules. (1 L bar = 100 J)',
            'answer': f'{num(w * 100)} J', 'key': f'w = −p_ext ΔV = −{p} × ({V2} − {V1}) = {num(w)} L bar = {num(w * 100)} J (work done by the system, so negative).',
            'distractors': [f'{num(-w * 100)} J', f'{num(w)} J', f'{num(w * 101.3)} J']}


def work_rev(r):
    n = r.choice([0.5, 1, 2, 3])
    T = r.choice([298, 300, 310, 350, 400])
    V1 = r.choice([1, 2, 5])
    V2 = V1 * r.choice([2, 5, 10])
    w = -2.303 * n * R * T * math.log10(V2 / V1)
    return {'stem': f'{n} mol of an ideal gas expands isothermally and reversibly at {T} K from {V1} L to {V2} L. Calculate w, q and ΔU. (R = 8.314 J K⁻¹ mol⁻¹)',
            'answer': f'w = {sf(w / 1000, 3)} kJ; q = {sf(-w / 1000, 3)} kJ; ΔU = 0',
            'key': f'w = −2.303 nRT log(V₂/V₁) = −2.303 × {n} × 8.314 × {T} × log {V2 // V1 if V2 % V1 == 0 else V2 / V1} = {sf(w, 4)} J (2); isothermal ideal gas ⇒ ΔU = 0, q = −w (1).',
            'distractors': [f'w = {sf(-w / 1000, 3)} kJ; q = {sf(w / 1000, 3)} kJ; ΔU = 0', f'w = {sf(w / 1000, 3)} kJ; q = 0; ΔU = {sf(w / 1000, 3)} kJ', f'w = {sf(w / 2303, 3)} kJ; q = {sf(-w / 2303, 3)} kJ; ΔU = 0']}


def first_law(r):
    q = r.choice([-1, 1]) * r.randint(2, 20) * 50
    w = r.choice([-1, 1]) * r.randint(1, 15) * 50
    dU = q + w
    who = name(r)
    qs = f'absorbs {abs(q)} J of heat' if q > 0 else f'releases {abs(q)} J of heat'
    ws = f'{abs(w)} J of work is done on it' if w > 0 else f'it does {abs(w)} J of work on the surroundings'
    return {'stem': f'In {who}\'s experiment a system {qs} and {ws}. Calculate the change in internal energy of the system.',
            'answer': f'ΔU = {num(dU)} J', 'key': f'ΔU = q + w with q = {num(q)} J and w = {num(w)} J (signs: heat absorbed and work done on the system are positive) ⇒ ΔU = {num(dU)} J.',
            'distractors': [f'ΔU = {num(q - w)} J', f'ΔU = {num(-dU)} J', f'ΔU = {num(abs(q) + abs(w))} J' if abs(q) + abs(w) != dU else f'ΔU = {num(dU + 100)} J']}


CH5S1 = {
    'topic': 'the first law of thermodynamics',
    'terms': [('a system', 'the part of the universe in which observations are made'),
              ('the surroundings', 'everything in the universe other than the system'),
              ('an isolated system', 'a system that exchanges neither energy nor matter with the surroundings'),
              ('a closed system', 'a system that exchanges energy but not matter with the surroundings'),
              ('an open system', 'a system that exchanges both energy and matter with the surroundings'),
              ('a state function', 'a property whose value depends only on the state of the system and not on how that state was reached'),
              ('an adiabatic process', 'a process in which no heat is transferred between the system and the surroundings'),
              ('internal energy', 'the total energy of a system, the sum of its chemical, electrical, mechanical and other energies')],
    'groups': [('a state function', ['internal energy', 'enthalpy', 'entropy', 'Gibbs energy', 'pressure', 'temperature']), ('a path function', ['heat', 'work'])],
    'groups2': [('an example of an open system', ['hot tea in an open cup', 'water boiling in an open beaker', 'a living plant']),
                ('an example of a closed system', ['a gas in a sealed steel cylinder', 'reactants in a stoppered metal flask', 'a sealed bottle of soda']),
                ('an example of an isolated system', ['hot coffee in an ideal thermos flask', 'reactants in a sealed, perfectly insulated vessel', 'the universe as a whole'])],
    'tf': (['For an isolated system ΔU = 0.', 'For an ideal gas undergoing isothermal expansion ΔU = 0.', 'Work done by the system is taken as negative (IUPAC convention).',
            'In an adiabatic process q = 0, so ΔU = w.', 'Free expansion of an ideal gas into vacuum involves no work.'],
           [('Heat is a state function.', 'Heat is a path function; its value depends on how the change is carried out.'),
            ('Work done on the system is taken as negative.', 'Work done on the system is positive in the IUPAC convention.'),
            ('In an isolated system energy can be exchanged with the surroundings.', 'An isolated system exchanges neither energy nor matter.'),
            ('Reversible expansion gives less work than irreversible expansion between the same states.', 'Reversible expansion gives the maximum work.')]),
    'ar': [('For free expansion of an ideal gas into vacuum, w = 0.', 'The external pressure in free expansion is zero.', 'a', 'w = −p_ext ΔV = 0 when p_ext = 0.'),
           ('Internal energy is a state function.', 'The change in internal energy depends only on the initial and final states.', 'a', 'A state-function change is path independent.')],
    'fams': [F('C2', 'D2', 'numerical', work_irrev), F('C3', 'D4', 'multi_step', work_rev, kinds=('long5',)), F('C2', 'D2', 'numerical', first_law)],
    'qa': [('C4', 'D3', 'explain', 'An ideal gas is expanded from the same initial to the same final state (a) reversibly and (b) against a constant low external pressure. Which gives more work, and is ΔU different for the two paths?',
            'Reversible expansion gives the maximum work (|w| larger). ΔU is the same for both because internal energy is a state function.',
            '1 mark: reversible gives more work; 1 mark: ΔU same (state function).')],
}

# ---------------- ch05 st2 enthalpy, heat capacity, calorimetry ----------------

DNG = [('N₂(g) + 3H₂(g) → 2NH₃(g)', -2, -87.4), ('CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)', -2, -885.4), ('C(graphite) + O₂(g) → CO₂(g)', 0, -393.5),
       ('2H₂(g) + O₂(g) → 2H₂O(l)', -3, -564.2), ('CaCO₃(s) → CaO(s) + CO₂(g)', 1, 175.5), ('PCl₅(g) → PCl₃(g) + Cl₂(g)', 1, 85.4),
       ('C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l)', -1, -1364.5), ('H₂(g) + Cl₂(g) → 2HCl(g)', 0, -184.6), ('2SO₂(g) + O₂(g) → 2SO₃(g)', -1, -195.3),
       ('N₂O₄(g) → 2NO₂(g)', 1, 54.7), ('C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(l)', -3, -2212.6), ('NH₄Cl(s) → NH₃(g) + HCl(g)', 2, 171.0)]


def dH_dU(r):
    eq, dn, base = r.choice(DNG)
    T = 298
    dU = round(base * r.uniform(0.97, 1.03), 1)
    dH = dU + dn * R * T / 1000
    return {'stem': f'For the reaction {eq}, ΔU = {num(dU)} kJ mol⁻¹ at 298 K. Calculate ΔH. (R = 8.314 J K⁻¹ mol⁻¹)',
            'answer': f'ΔH = {dH:.2f} kJ mol⁻¹', 'key': f'Δn_g = (gaseous products) − (gaseous reactants) = {dn} (1); ΔH = ΔU + Δn_gRT = {num(dU)} + ({dn})(8.314 × 10⁻³)(298) = {dH:.2f} kJ mol⁻¹ (1).',
            'distractors': [f'ΔH = {dU - dn * R * T / 1000:.2f} kJ mol⁻¹' if dn else f'ΔH = {dU + R * T / 1000:.2f} kJ mol⁻¹', f'ΔH = {dU + dn * R * T:.2f} kJ mol⁻¹' if dn else f'ΔH = {dU - R * T / 1000:.2f} kJ mol⁻¹', f'ΔH = {dU + dn * 0.0821 * 298:.2f} kJ mol⁻¹' if dn else f'ΔH = {dU * 2:.2f} kJ mol⁻¹']}


SPH = [('water', 4.18), ('aluminium', 0.90), ('iron', 0.45), ('copper', 0.385), ('ethanol', 2.44)]


def heat_q(r):
    sub, cp = r.choice(SPH)
    m = r.choice([50, 100, 150, 200, 250, 500])
    T1 = r.choice([20, 25, 27, 30])
    T2 = T1 + r.choice([10, 15, 20, 25, 35, 50])
    q = m * cp * (T2 - T1)
    return {'stem': f'How much heat is needed to raise the temperature of {m} g of {sub} from {T1} °C to {T2} °C? (Specific heat = {cp} J g⁻¹ K⁻¹)',
            'answer': f'{sf(q / 1000, 3)} kJ', 'key': f'q = m c ΔT = {m} × {cp} × {T2 - T1} = {num(q, 1)} J = {sf(q / 1000, 3)} kJ.',
            'distractors': [f'{sf(m * cp * T2 / 1000, 3)} kJ', f'{sf(q / 100, 3)} kJ', f'{sf(m * cp * (T2 - T1 + 273) / 1000, 3)} kJ']}


FUELS = [('graphite', 12, 'C(graphite)'), ('glucose', 180, 'C₆H₁₂O₆'), ('benzoic acid', 122, 'C₆H₅COOH'), ('naphthalene', 128, 'C₁₀H₈'), ('sucrose', 342, 'C₁₂H₂₂O₁₁')]


def bomb(r):
    f, Mm, fm = r.choice(FUELS)
    m = r.choice([0.5, 1.0, 1.2, 1.5, 2.0])
    Cc = r.choice([10, 15, 20, 25])
    dT = round(r.uniform(0.5, 4.5), 2)
    qv = Cc * dT
    dU = -qv / m * Mm
    return {'stem': f'{m} g of {f} ({fm}, molar mass {Mm} g mol⁻¹) is burnt in a bomb calorimeter of heat capacity {Cc} kJ K⁻¹. The temperature rises by {dT} K. Calculate ΔU of combustion per mole.',
            'answer': f'{sf(dU, 3)} kJ mol⁻¹', 'key': f'Heat released at constant volume = C ΔT = {Cc} × {dT} = {num(qv, 2)} kJ (1); per mole = {num(qv, 2)} × {Mm}/{m} = {sf(-dU, 4)} kJ; reaction is exothermic so ΔU = {sf(dU, 3)} kJ mol⁻¹ (1).',
            'distractors': [f'{sf(-dU, 3)} kJ mol⁻¹', f'{sf(-qv, 3)} kJ mol⁻¹', f'{sf(dU / Mm, 3)} kJ mol⁻¹']}


CH5S2 = {
    'topic': 'enthalpy and calorimetry',
    'terms': [('enthalpy', 'a state function defined as H = U + pV'),
              ('heat capacity', 'the amount of heat required to raise the temperature of a substance by one degree'),
              ('molar heat capacity', 'the heat capacity of one mole of a substance'),
              ('specific heat capacity', 'the quantity of heat required to raise the temperature of one gram of a substance by one degree'),
              ('a bomb calorimeter', 'a steel vessel immersed in water in which combustion is carried out at constant volume to measure ΔU'),
              ('an extensive property', 'a property whose value depends on the quantity or size of matter present'),
              ('an intensive property', 'a property whose value does not depend on the quantity or size of matter present')],
    'groups': [('an extensive property', ['mass', 'volume', 'internal energy', 'enthalpy', 'heat capacity']),
               ('an intensive property', ['temperature', 'pressure', 'density', 'molar heat capacity', 'viscosity', 'surface tension'])],
    'tf': (['ΔH = q at constant pressure.', 'ΔU = q at constant volume.', 'For reactions involving only solids and liquids, ΔH ≈ ΔU.',
            'Cp − Cv = R for one mole of an ideal gas.', 'A bomb calorimeter measures heat change at constant volume.'],
           [('A bomb calorimeter measures ΔH directly.', 'A bomb calorimeter works at constant volume and measures ΔU.'),
            ('Cv is greater than Cp for an ideal gas.', 'Cp is greater than Cv; Cp − Cv = R.'),
            ('ΔH and ΔU are always equal for gaseous reactions.', 'They differ by Δn_gRT; they are equal only when Δn_g = 0.'),
            ('Heat capacity is an intensive property.', 'Heat capacity is extensive; molar or specific heat capacity is intensive.')]),
    'ar': [('For the reaction H₂(g) + Cl₂(g) → 2HCl(g), ΔH = ΔU.', 'Δn_g for this reaction is zero.', 'a', 'ΔH = ΔU + Δn_gRT with Δn_g = 2 − 2 = 0.'),
           ('Cp is greater than Cv for a gas.', 'At constant pressure part of the heat supplied is used to do work of expansion.', 'a', 'Extra heat for pV work makes Cp larger.')],
    'fams': [F('C3', 'D3', 'numerical', dH_dU), F('C2', 'D2', 'numerical', heat_q), F('C3', 'D4', 'numerical', bomb, marks=3)],
    'qa': [('C4', 'D4', 'explain', 'Why is the enthalpy of combustion obtained from a bomb calorimeter corrected before it is quoted as ΔcH? When is no correction needed?',
            'A bomb calorimeter gives ΔU (constant volume); ΔH = ΔU + Δn_gRT, so a correction is needed when the number of moles of gas changes. No correction is needed if Δn_g = 0.',
            '1 mark: calorimeter gives ΔU; 1 mark: conversion using Δn_gRT / no correction when Δn_g = 0.')],
}

# ---------------- ch05 st3 Hess's law and enthalpies of reactions ----------------

DFH = {'CO₂(g)': -393.5, 'H₂O(l)': -285.8, 'H₂O(g)': -241.8, 'CH₄(g)': -74.8, 'C₂H₄(g)': 52.3, 'C₂H₂(g)': 226.7, 'C₂H₆(g)': -84.7,
       'C₃H₈(g)': -103.8, 'C₂H₅OH(l)': -277.7, 'NH₃(g)': -46.1, 'NO(g)': 90.3, 'NO₂(g)': 33.2, 'N₂O₄(g)': 9.2, 'HCl(g)': -92.3,
       'CO(g)': -110.5, 'SO₂(g)': -296.8, 'SO₃(g)': -395.7, 'CaO(s)': -635.1, 'CaCO₃(s)': -1206.9, 'Fe₂O₃(s)': -824.2, 'Al₂O₃(s)': -1675.7,
       'C₆H₁₂O₆(s)': -1273.3}
HESS = [([('CH₄(g)', 1), ('O₂(g)', 2)], [('CO₂(g)', 1), ('H₂O(l)', 2)]), ([('C₂H₄(g)', 1), ('H₂(g)', 1)], [('C₂H₆(g)', 1)]),
        ([('C₂H₄(g)', 1), ('O₂(g)', 3)], [('CO₂(g)', 2), ('H₂O(l)', 2)]), ([('C₂H₂(g)', 1), ('H₂(g)', 2)], [('C₂H₆(g)', 1)]),
        ([('C₃H₈(g)', 1), ('O₂(g)', 5)], [('CO₂(g)', 3), ('H₂O(l)', 4)]), ([('C₂H₅OH(l)', 1), ('O₂(g)', 3)], [('CO₂(g)', 2), ('H₂O(l)', 3)]),
        ([('NH₃(g)', 4), ('O₂(g)', 5)], [('NO(g)', 4), ('H₂O(g)', 6)]), ([('NO₂(g)', 2)], [('N₂O₄(g)', 1)]),
        ([('SO₂(g)', 2), ('O₂(g)', 1)], [('SO₃(g)', 2)]), ([('CaCO₃(s)', 1)], [('CaO(s)', 1), ('CO₂(g)', 1)]),
        ([('Fe₂O₃(s)', 1), ('CO(g)', 3)], [('Fe(s)', 2), ('CO₂(g)', 3)]), ([('Al(s)', 2), ('Fe₂O₃(s)', 1)], [('Al₂O₃(s)', 1), ('Fe(s)', 2)]),
        ([('C₆H₁₂O₆(s)', 1), ('O₂(g)', 6)], [('CO₂(g)', 6), ('H₂O(l)', 6)]), ([('C₂H₆(g)', 2), ('O₂(g)', 7)], [('CO₂(g)', 4), ('H₂O(l)', 6)])]


def eqstr(rs, ps):
    f = lambda side: ' + '.join(f'{c if c != 1 else ""}{s}' for s, c in side)
    return f'{f(rs)} → {f(ps)}'


def hess_f(r):
    rs, ps = r.choice(HESS)
    dH = sum(c * DFH.get(s, 0) for s, c in ps) - sum(c * DFH.get(s, 0) for s, c in rs)
    data = sorted({s for s, _ in rs + ps if s in DFH})
    return {'stem': f'Calculate ΔᵣH° for {eqstr(rs, ps)} using the standard enthalpies of formation (kJ mol⁻¹): ' + ', '.join(f'{s} {DFH[s]}' for s in data) + '.',
            'answer': f'{dH:.1f} kJ mol⁻¹', 'key': f'ΔᵣH° = ΣΔfH°(products) − ΣΔfH°(reactants); elements in standard state have ΔfH° = 0 ⇒ {dH:.1f} kJ mol⁻¹ (2).',
            'distractors': [f'{-dH:.1f} kJ mol⁻¹', f'{sum(DFH.get(s, 0) for s, c in ps) - sum(DFH.get(s, 0) for s, c in rs):.1f} kJ mol⁻¹' if any(c != 1 for _, c in rs + ps) else f'{dH * 2:.1f} kJ mol⁻¹', f'{dH + 100:.1f} kJ mol⁻¹']}


BE = {'H–H': 436, 'Cl–Cl': 242, 'Br–Br': 192, 'F–F': 155, 'I–I': 151, 'H–Cl': 431, 'H–Br': 366, 'H–F': 565, 'H–I': 299, 'C–H': 414,
      'C–C': 347, 'C=C': 611, 'N≡N': 946, 'N–H': 389, 'C–Cl': 330, 'O=O': 498, 'O–H': 464}
BRX = [('H₂(g) + Cl₂(g) → 2HCl(g)', {'H–H': 1, 'Cl–Cl': 1}, {'H–Cl': 2}), ('H₂(g) + Br₂(g) → 2HBr(g)', {'H–H': 1, 'Br–Br': 1}, {'H–Br': 2}),
       ('H₂(g) + F₂(g) → 2HF(g)', {'H–H': 1, 'F–F': 1}, {'H–F': 2}), ('H₂(g) + I₂(g) → 2HI(g)', {'H–H': 1, 'I–I': 1}, {'H–I': 2}),
       ('CH₂=CH₂(g) + H₂(g) → CH₃–CH₃(g)', {'C=C': 1, 'H–H': 1}, {'C–C': 1, 'C–H': 2}), ('N₂(g) + 3H₂(g) → 2NH₃(g)', {'N≡N': 1, 'H–H': 3}, {'N–H': 6}),
       ('CH₄(g) + Cl₂(g) → CH₃Cl(g) + HCl(g)', {'C–H': 1, 'Cl–Cl': 1}, {'C–Cl': 1, 'H–Cl': 1}),
       ('CH₂=CH₂(g) + Cl₂(g) → CH₂Cl–CH₂Cl(g)', {'C=C': 1, 'Cl–Cl': 1}, {'C–C': 1, 'C–Cl': 2}),
       ('2H₂(g) + O₂(g) → 2H₂O(g)', {'H–H': 2, 'O=O': 1}, {'O–H': 4})]


def bond_enthalpy(r):
    eq, br, mk = r.choice(BRX)
    b = sum(BE[k] * n for k, n in br.items())
    m = sum(BE[k] * n for k, n in mk.items())
    dH = b - m
    data = sorted(set(br) | set(mk))
    return {'stem': f'Estimate ΔᵣH for {eq} from the bond enthalpies (kJ mol⁻¹): ' + ', '.join(f'{k} {BE[k]}' for k in data) + '.',
            'answer': f'{num(dH)} kJ mol⁻¹', 'key': f'ΔᵣH = Σ(bonds broken) − Σ(bonds formed) = {b} − {m} = {num(dH)} kJ mol⁻¹ (bonds broken: ' + ', '.join(f'{n} {k}' for k, n in br.items()) + '; formed: ' + ', '.join(f'{n} {k}' for k, n in mk.items()) + ').',
            'distractors': [f'{num(-dH)} kJ mol⁻¹', f'{num(b + m)} kJ mol⁻¹', f'{num(sum(BE[k] for k in br) - sum(BE[k] for k in mk))} kJ mol⁻¹' if sum(BE[k] for k in br) - sum(BE[k] for k in mk) != dH else f'{num(dH / 2)} kJ mol⁻¹']}


def hess_combine(r):
    a = r.choice([-393.5, -395.4, -393.0])
    b = r.choice([-283.0, -282.9, -283.5])
    return {'stem': f'Given: C(graphite) + O₂(g) → CO₂(g), ΔH = {a} kJ mol⁻¹; CO(g) + ½O₂(g) → CO₂(g), ΔH = {b} kJ mol⁻¹. Use Hess\'s law to find ΔH for C(graphite) + ½O₂(g) → CO(g).',
            'answer': f'{a - b:.1f} kJ mol⁻¹', 'key': f'Target = (1st) − (2nd): ΔH = {a} − ({b}) = {a - b:.1f} kJ mol⁻¹ (2).',
            'distractors': [f'{a + b:.1f} kJ mol⁻¹', f'{b - a:.1f} kJ mol⁻¹', f'{a:.1f} kJ mol⁻¹']}


def hess_combine2(r):
    c_ = r.choice([-393.5, -394.0])
    h_ = r.choice([-285.8, -286.0])
    comb = r.choice([(-890.3, 'CH₄', 1, 2, -74.8), (-1411.0, 'C₂H₄', 2, 2, 52.3), (-1560.0, 'C₂H₆', 2, 3, -84.7), (-2220.0, 'C₃H₈', 3, 4, -103.8)])
    dc, f, nc, nh, _ = comb
    dfh = nc * c_ + nh * h_ - dc
    return {'stem': f'The enthalpy of combustion of {f}(g) is {dc} kJ mol⁻¹, of graphite is {c_} kJ mol⁻¹ and of H₂(g) is {h_} kJ mol⁻¹ (water as liquid). Calculate the standard enthalpy of formation of {f}.',
            'answer': f'{dfh:.1f} kJ mol⁻¹', 'key': f'ΔfH = {nc} × ΔcH(C) + {nh} × ΔcH(H₂) − ΔcH({f}) = {nc}({c_}) + {nh}({h_}) − ({dc}) = {dfh:.1f} kJ mol⁻¹ (3).',
            'distractors': [f'{-dfh:.1f} kJ mol⁻¹', f'{c_ + h_ - dc:.1f} kJ mol⁻¹', f'{dc - nc * c_ - nh * h_ + 50:.1f} kJ mol⁻¹']}


CH5S3 = {
    'topic': 'thermochemistry',
    'terms': [("Hess's law of constant heat summation", 'the law that the total enthalpy change of a reaction is the same whether it occurs in one step or several steps'),
              ('standard enthalpy of formation', 'the enthalpy change for the formation of one mole of a compound from its elements in their most stable states'),
              ('enthalpy of combustion', 'the enthalpy change when one mole of a substance burns completely in oxygen'),
              ('enthalpy of atomisation', 'the enthalpy change on breaking one mole of bonds completely to obtain atoms in the gas phase'),
              ('enthalpy of solution', 'the enthalpy change when one mole of a substance dissolves in a specified amount of solvent'),
              ('enthalpy of neutralisation', 'the enthalpy change when one equivalent of an acid is neutralised by a base in dilute solution'),
              ('a thermochemical equation', 'a balanced equation that shows the physical states of all species together with the value of ΔᵣH')],
    'tf': (['The standard enthalpy of formation of an element in its most stable state is zero.', 'Enthalpy of combustion is always negative.',
            'If a reaction is reversed, the sign of ΔH is reversed.', 'If the coefficients of a thermochemical equation are doubled, ΔH is doubled.',
            'Bond enthalpy values are average values for a given type of bond.'],
           [('The standard enthalpy of formation of diamond is zero.', 'Graphite is the standard state of carbon; ΔfH°(diamond) = +1.9 kJ mol⁻¹.'),
            ('Hess\'s law shows that ΔH depends on the path followed.', 'Hess\'s law shows ΔH is independent of path because enthalpy is a state function.'),
            ('The enthalpy of combustion of a fuel is positive.', 'Combustion releases heat, so the enthalpy of combustion is negative.'),
            ('Reversing a reaction leaves ΔH unchanged.', 'Reversing a reaction changes the sign of ΔH.')]),
    'ar': [('ΔfH° of O₂(g) is zero.', 'O₂(g) is the most stable form of oxygen at 1 bar and 298 K.', 'a', 'By definition ΔfH° is zero for an element in its reference state.'),
           ('Enthalpy of neutralisation of strong acids by strong bases is nearly constant (−57.1 kJ mol⁻¹).', 'The net reaction in each case is H⁺(aq) + OH⁻(aq) → H₂O(l).', 'a', 'Strong electrolytes are fully ionised, so the same net reaction occurs.')],
    'fams': [F('C3', 'D3', 'numerical', hess_f), F('C3', 'D3', 'numerical', bond_enthalpy), F('C3', 'D2', 'numerical', hess_combine),
             F('C4', 'D4', 'multi_step', hess_combine2, kinds=('long5',))],
    'qa': [('C4', 'D4', 'explain', 'The enthalpy of neutralisation of acetic acid with NaOH is −55.8 kJ mol⁻¹, less negative than for HCl (−57.1). Explain.',
            'Acetic acid is a weak acid; part of the heat released is used to ionise it completely (enthalpy of ionisation), so less heat is evolved.',
            '1 mark: weak acid not fully ionised; 1 mark: energy used for ionisation.'),
           ('C4', 'D3', 'case', 'A student mixes 50 mL of 1.0 M HCl with 50 mL of 1.0 M NaOH in a polystyrene cup. The temperature rises from 25.0 °C to 31.8 °C. Take the specific heat of the solution as 4.18 J g⁻¹ K⁻¹ and its density as 1.0 g mL⁻¹.\n(i) Calculate the heat released. (1 mark)\n(ii) How many moles of water are formed? (1 mark)\n(iii) Calculate the enthalpy of neutralisation and say why a polystyrene cup is used. (2 marks)',
            '(i) q = 100 × 4.18 × 6.8 = 2842 J (ii) 0.050 mol (iii) ΔH = −2.842/0.050 = −56.8 kJ mol⁻¹; polystyrene is a good insulator, so little heat is lost.',
            '(i) 1 (ii) 1 (iii) 1 for −56.8 kJ mol⁻¹, 1 for insulation.', ('case',))],
}

# ---------------- ch05 st4 entropy and Gibbs energy ----------------

def gibbs(r):
    dH = r.choice([-1, 1]) * r.randint(10, 180)
    dS = r.choice([-1, 1]) * r.randint(20, 300)
    T = r.choice([298, 300, 350, 400, 500, 1000])
    dG = dH - T * dS / 1000
    sp = 'spontaneous' if dG < 0 else 'non-spontaneous'
    return {'stem': f'For a reaction ΔH = {dH} kJ mol⁻¹ and ΔS = {dS} J K⁻¹ mol⁻¹. Calculate ΔG at {T} K and say whether the reaction is spontaneous at this temperature.',
            'answer': f'ΔG = {dG:.1f} kJ mol⁻¹; {sp}', 'key': f'ΔG = ΔH − TΔS = {dH} − {T} × ({dS}/1000) = {dG:.1f} kJ mol⁻¹ (1); ΔG {"<" if dG < 0 else ">"} 0 ⇒ {sp} (1).',
            'distractors': [f'ΔG = {dH - T * dS:.1f} kJ mol⁻¹; {"spontaneous" if dH - T * dS < 0 else "non-spontaneous"}', f'ΔG = {dH + T * dS / 1000:.1f} kJ mol⁻¹; {"spontaneous" if dH + T * dS / 1000 < 0 else "non-spontaneous"}', f'ΔG = {dG:.1f} kJ mol⁻¹; {"non-spontaneous" if dG < 0 else "spontaneous"}']}


def crossover(r):
    sgn = r.choice([1, -1])
    dH = sgn * r.randint(20, 180)
    dS = sgn * r.randint(40, 250)
    T = dH * 1000 / dS
    when = 'above' if sgn > 0 else 'below'
    return {'stem': f'For a reaction ΔH = {dH} kJ mol⁻¹ and ΔS = {dS} J K⁻¹ mol⁻¹ (both roughly independent of temperature). Find the temperature at which ΔG = 0 and state the range of temperature in which the reaction is spontaneous.',
            'answer': f'T = {T:.0f} K; spontaneous {when} {T:.0f} K',
            'key': f'At equilibrium ΔG = 0 ⇒ T = ΔH/ΔS = {dH * 1000}/{dS} = {T:.0f} K (1). ' + ('ΔH and ΔS both positive: TΔS outweighs ΔH at higher T, so spontaneous above this temperature (1).' if sgn > 0 else 'ΔH and ΔS both negative: ΔH dominates at lower T, so spontaneous below this temperature (1).'),
            'distractors': [f'T = {T:.0f} K; spontaneous {"below" if sgn > 0 else "above"} {T:.0f} K', f'T = {T / 1000:.3f} K; spontaneous {when} it', f'T = {T + 273:.0f} K; spontaneous {when} it']}


def dG_K(r):
    K = r.choice([10, 100, 2.5e3, 1e5, 1e-2, 1e-4, 4.0, 50])
    T = 298
    dG = -2.303 * R * T * math.log10(K) / 1000
    return {'stem': f'The equilibrium constant of a reaction at 298 K is {sf(K, 2) if K < 1e4 and K > 1e-3 else sci(K, 2)}. Calculate ΔG° for the reaction. (R = 8.314 J K⁻¹ mol⁻¹)',
            'answer': f'{dG:.2f} kJ mol⁻¹', 'key': f'ΔG° = −2.303 RT log K = −2.303 × 8.314 × 298 × log({sf(K, 2) if K < 1e4 and K > 1e-3 else sci(K, 2)}) = {dG:.2f} kJ mol⁻¹.',
            'distractors': [f'{-dG:.2f} kJ mol⁻¹', f'{dG / 2.303:.2f} kJ mol⁻¹', f'{dG * 1000:.0f} kJ mol⁻¹']}


CH5S4 = {
    'topic': 'spontaneity, entropy and Gibbs energy',
    'terms': [('entropy', 'a measure of the degree of randomness or disorder in a system'),
              ('Gibbs energy', 'the state function G = H − TS whose decrease at constant T and p gives useful work'),
              ('a spontaneous process', 'a process that has the potential to proceed without the assistance of an external agency'),
              ('the second law of thermodynamics', 'the law that the total entropy of the system and surroundings increases in a spontaneous process'),
              ('the third law of thermodynamics', 'the law that the entropy of a perfectly crystalline substance approaches zero as the temperature approaches absolute zero')],
    'groups': [('a process with an increase in entropy', ['melting of ice', 'evaporation of water', 'CaCO₃(s) → CaO(s) + CO₂(g)', 'sublimation of iodine', 'N₂O₄(g) → 2NO₂(g)', 'dissolving NaCl in water']),
               ('a process with a decrease in entropy', ['freezing of water', 'condensation of steam', 'N₂(g) + 3H₂(g) → 2NH₃(g)', '2SO₂(g) + O₂(g) → 2SO₃(g)', 'crystallisation of sugar from solution', 'H₂(g) + ½O₂(g) → H₂O(l)'])],
    'features': {'intro': 'For a reaction:', 'q': 'Under what conditions is the reaction spontaneous', 'what': 'condition',
                 'case': False, 'long': False,
                 'items': [('spontaneous at all temperatures', ['ΔH is negative and ΔS is positive', 'both terms in ΔG = ΔH − TΔS are negative']),
                           ('spontaneous only at high temperature', ['ΔH is positive and ΔS is positive', 'TΔS outweighs ΔH when T > ΔH/ΔS']),
                           ('spontaneous only at low temperature', ['ΔH is negative and ΔS is negative', 'ΔH outweighs TΔS when T < ΔH/ΔS']),
                           ('non-spontaneous at all temperatures', ['ΔH is positive and ΔS is negative', 'ΔG is always positive', 'the reverse reaction is spontaneous at all temperatures'])]},
    'tf': (['A reaction with ΔG < 0 is spontaneous at constant temperature and pressure.', 'At equilibrium ΔG = 0.', 'The entropy of a gas is greater than that of the same substance as a liquid.',
            'ΔG° = −RT ln K.', 'A negative ΔH alone does not guarantee spontaneity.'],
           [('All exothermic reactions are spontaneous.', 'An exothermic reaction with large negative ΔS can be non-spontaneous at high temperature.'),
            ('Entropy decreases when a solid melts.', 'Melting increases entropy because particles become more disordered.'),
            ('A spontaneous reaction must be fast.', 'Spontaneity says nothing about rate; e.g. diamond → graphite is spontaneous but extremely slow.'),
            ('If K > 1, ΔG° is positive.', 'If K > 1, ΔG° = −RT ln K is negative.')]),
    'ar': [('Melting of ice at 298 K is spontaneous although it is endothermic.', 'At 298 K the TΔS term is larger than ΔH, so ΔG is negative.', 'a', 'ΔG = ΔH − TΔS < 0 above 273 K.'),
           ('Entropy of the universe increases in a spontaneous process.', 'ΔS(total) = ΔS(system) + ΔS(surroundings) > 0 for a spontaneous change.', 'a', 'This is the second law.')],
    'fams': [F('C3', 'D3', 'numerical', gibbs), F('C4', 'D4', 'explain', crossover), F('C3', 'D4', 'numerical', dG_K)],
}

# ---------------- ch06 equilibrium ----------------

EQ = [  # display, reactants [(sp, n, phase)], products, dH sign (+1 endo, -1 exo, 0 none), name
    ('N₂(g) + 3H₂(g) ⇌ 2NH₃(g)', [('N₂', 1, 'g'), ('H₂', 3, 'g')], [('NH₃', 2, 'g')], -1),
    ('2SO₂(g) + O₂(g) ⇌ 2SO₃(g)', [('SO₂', 2, 'g'), ('O₂', 1, 'g')], [('SO₃', 2, 'g')], -1),
    ('PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)', [('PCl₅', 1, 'g')], [('PCl₃', 1, 'g'), ('Cl₂', 1, 'g')], 1),
    ('N₂O₄(g) ⇌ 2NO₂(g)', [('N₂O₄', 1, 'g')], [('NO₂', 2, 'g')], 1),
    ('H₂(g) + I₂(g) ⇌ 2HI(g)', [('H₂', 1, 'g'), ('I₂', 1, 'g')], [('HI', 2, 'g')], 0),
    ('N₂(g) + O₂(g) ⇌ 2NO(g)', [('N₂', 1, 'g'), ('O₂', 1, 'g')], [('NO', 2, 'g')], 1),
    ('CaCO₃(s) ⇌ CaO(s) + CO₂(g)', [('CaCO₃', 1, 's')], [('CaO', 1, 's'), ('CO₂', 1, 'g')], 1),
    ('CO(g) + 2H₂(g) ⇌ CH₃OH(g)', [('CO', 1, 'g'), ('H₂', 2, 'g')], [('CH₃OH', 1, 'g')], -1),
    ('CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g)', [('CO', 1, 'g'), ('H₂O', 1, 'g')], [('CO₂', 1, 'g'), ('H₂', 1, 'g')], -1),
    ('C(s) + H₂O(g) ⇌ CO(g) + H₂(g)', [('C', 1, 's'), ('H₂O', 1, 'g')], [('CO', 1, 'g'), ('H₂', 1, 'g')], 1),
    ('2NO(g) + O₂(g) ⇌ 2NO₂(g)', [('NO', 2, 'g'), ('O₂', 1, 'g')], [('NO₂', 2, 'g')], -1),
    ('4NH₃(g) + 5O₂(g) ⇌ 4NO(g) + 6H₂O(g)', [('NH₃', 4, 'g'), ('O₂', 5, 'g')], [('NO', 4, 'g'), ('H₂O', 6, 'g')], -1),
]


def conc(side, solids=False):
    out = []
    for sp, n, ph in side:
        if ph == 's' and not solids:
            continue
        out.append(f'[{sp}]{str(n).translate(SUPD) if n > 1 else ""}')
    return ''.join(out) or '1'


def kc_expr(r):
    eq, rs, ps, _ = r.choice(EQ)
    good = f'Kc = {conc(ps)}/{conc(rs)}'
    inv = f'Kc = {conc(rs)}/{conc(ps)}'
    nocoef = f'Kc = {"".join(f"[{s}]" for s, n, ph in ps if ph != "s")}/{"".join(f"[{s}]" for s, n, ph in rs if ph != "s") or "1"}'
    withs = f'Kc = {conc(ps, True)}/{conc(rs, True)}'
    wrong = [w for w in dict.fromkeys([inv, nocoef, withs, f'Kc = {conc(ps)} × {conc(rs)}']) if w != good][:3]
    return mcq(f'Which is the correct expression for Kc of {eq}?', good, wrong,
               f'Products over reactants, each concentration raised to its stoichiometric coefficient; pure solids are omitted: {good}.', r)


def kc_calc(r):
    eq, rs, ps, _ = r.choice([e for e in EQ if all(ph == 'g' for _, _, ph in e[1] + e[2]) and len(e[1] + e[2]) <= 4])
    vals = {}
    for sp, n, ph in rs + ps:
        vals[sp] = r.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.4, 0.5, 0.8, 1.2, 1.5, 2.0])
    num_ = 1
    for sp, n, ph in ps:
        num_ *= vals[sp] ** n
    den = 1
    for sp, n, ph in rs:
        den *= vals[sp] ** n
    K = num_ / den
    return {'stem': f'At equilibrium for {eq}, the concentrations are ' + ', '.join(f'[{s}] = {vals[s]} M' for s in vals) + '. Calculate Kc.',
            'answer': f'Kc = {sf(K, 3)}', 'key': f'Kc = {conc(ps)}/{conc(rs)} = {sf(num_, 3)}/{sf(den, 3)} = {sf(K, 3)}.',
            'distractors': [f'Kc = {sf(1 / K, 3)}', f'Kc = {sf(sum(vals[s] * n for s, n, _ in ps) / sum(vals[s] * n for s, n, _ in rs), 3)}', f'Kc = {sf(K * 2, 3)}']}


def k_manip(r):
    eq, rs, ps, _ = r.choice(EQ)
    K = r.choice([2.0, 4.0, 0.25, 50, 1.6e-3, 6.4e2, 0.04, 9.0])
    op = r.choice(['rev', 'double', 'half'])
    if op == 'rev':
        v, how = 1 / K, 'the reverse reaction'
        rule = "K' = 1/K"
    elif op == 'double':
        v, how = K * K, 'the reaction with all coefficients doubled'
        rule = "K' = K²"
    else:
        v, how = math.sqrt(K), 'the reaction with all coefficients halved'
        rule = "K' = K^½"
    return {'stem': f'Kc for {eq} is {sf(K, 2)} at a certain temperature. What is the equilibrium constant for {how} at the same temperature?',
            'answer': sf(v, 3), 'key': f'{rule} = {sf(v, 3)}.', 'distractors': [x for x in dict.fromkeys([sf(1 / K, 3), sf(K * K, 3), sf(math.sqrt(K), 3), sf(2 * K, 3), sf(-K, 3)]) if x != sf(v, 3)][:3]}


RL = 0.0831


def kp_kc(r):
    eq, rs, ps, _ = r.choice([e for e in EQ if sum(n for _, n, ph in e[2] if ph == 'g') != sum(n for _, n, ph in e[1] if ph == 'g')])
    dn = sum(n for _, n, ph in ps if ph == 'g') - sum(n for _, n, ph in rs if ph == 'g')
    T = r.choice([400, 500, 600, 700, 800])
    Kc = r.choice([0.5, 1.2, 2.5, 4.0, 10, 0.04, 6.0])
    Kp = Kc * (RL * T) ** dn
    return {'stem': f'For {eq}, Kc = {Kc} at {T} K. Calculate Kp. (R = 0.0831 bar L mol⁻¹ K⁻¹)',
            'answer': f'Kp = {sf(Kp, 3)}', 'key': f'Δn_g = {dn} (1); Kp = Kc(RT)^Δn = {Kc} × ({RL} × {T})^{dn} = {sf(Kp, 3)} (1).',
            'distractors': [f'Kp = {sf(Kc * (RL * T) ** (-dn), 3)}', f'Kp = {sf(Kc * (8.314 * T) ** dn, 3)}', f'Kp = {sf(Kc, 3)}']}


def q_vs_k(r):
    eq, rs, ps, _ = r.choice([e for e in EQ if all(ph == 'g' for _, _, ph in e[1] + e[2]) and len(e[1] + e[2]) <= 3])
    vals = {s: r.choice([0.1, 0.2, 0.3, 0.5, 1.0, 1.5]) for s, _, _ in rs + ps}
    Q = 1
    for s, n, _ in ps:
        Q *= vals[s] ** n
    for s, n, _ in rs:
        Q /= vals[s] ** n
    K = Q * r.choice([0.2, 0.5, 2, 5, 10])
    d = 'forward (towards products)' if Q < K else 'backward (towards reactants)'
    return {'stem': f'For {eq}, Kc = {sf(K, 3)}. A mixture has ' + ', '.join(f'[{s}] = {v} M' for s, v in vals.items()) + '. Calculate the reaction quotient and predict the direction of net reaction.',
            'answer': f'Qc = {sf(Q, 3)}; net reaction {d}', 'key': f'Qc = {conc(ps)}/{conc(rs)} = {sf(Q, 3)} (1); Qc {"<" if Q < K else ">"} Kc ⇒ net reaction goes {d} (1).',
            'distractors': [f'Qc = {sf(Q, 3)}; net reaction {"backward (towards reactants)" if Q < K else "forward (towards products)"}', f'Qc = {sf(1 / Q, 3)}; net reaction {d}', f'Qc = {sf(Q, 3)}; the mixture is at equilibrium']}


CHANGES = ['increasing the pressure (by reducing volume)', 'decreasing the pressure', 'raising the temperature', 'lowering the temperature',
           'adding a catalyst', 'adding more of a reactant', 'removing a product as it forms', 'adding an inert gas at constant volume']


def lechatelier(r):
    eq, rs, ps, dh = r.choice(EQ)
    dn = sum(n for _, n, ph in ps if ph == 'g') - sum(n for _, n, ph in rs if ph == 'g')
    ch = r.choice(CHANGES)
    if 'temperature' in ch and dh == 0:
        ch = r.choice(CHANGES[:2] + CHANGES[4:])
    if 'pressure' in ch:
        up = 'increasing' in ch
        if dn == 0:
            ans, why = 'no effect on the position of equilibrium', 'the number of moles of gas is the same on both sides (Δn_g = 0)'
        else:
            fwd = (dn < 0) == up
            ans = 'shifts forward (towards products)' if fwd else 'shifts backward (towards reactants)'
            why = f'Δn_g = {dn}; the system moves towards the side with {"fewer" if up else "more"} moles of gas'
    elif 'temperature' in ch:
        up = 'raising' in ch
        fwd = (dh > 0) == up
        ans = 'shifts forward (towards products)' if fwd else 'shifts backward (towards reactants)'
        why = f'the forward reaction is {"endothermic" if dh > 0 else "exothermic"}; {"heating favours the endothermic direction" if up else "cooling favours the exothermic direction"} (K changes)'
    elif 'catalyst' in ch:
        ans, why = 'no effect on the position of equilibrium', 'a catalyst speeds up forward and backward reactions equally; equilibrium is only reached sooner'
    elif 'inert' in ch:
        ans, why = 'no effect on the position of equilibrium', 'partial pressures and concentrations of the reacting gases do not change at constant volume'
    else:
        ans, why = 'shifts forward (towards products)', 'the system tries to use up the added reactant / replace the removed product (Q < K)'
    opts = ['shifts forward (towards products)', 'shifts backward (towards reactants)', 'no effect on the position of equilibrium', 'the value of Kc becomes zero']
    return mcq(f'For the equilibrium {eq}{" (forward reaction " + ("endothermic" if dh > 0 else "exothermic") + ")" if dh else ""}, what is the effect of {ch}?',
               ans, [o for o in opts if o != ans][:3], f'{cap(ans)}: {why} (Le Chatelier\'s principle).', r)


def ice_hi(r):
    a = r.choice([0.5, 1.0, 1.5, 2.0])
    K = r.choice([4, 9, 16, 25, 36, 49, 64])
    s = math.sqrt(K)
    x = a * s / (2 + s)
    V = r.choice([1, 2])
    return {'stem': f'{a} mol each of H₂ and I₂ are heated in a {V} L sealed vessel. At equilibrium, H₂(g) + I₂(g) ⇌ 2HI(g), Kc = {K}. Calculate the equilibrium concentrations of H₂, I₂ and HI.',
            'answer': f'[H₂] = [I₂] = {sf((a - x) / V, 3)} M; [HI] = {sf(2 * x / V, 3)} M',
            'key': f'Let x mol react: (2x)²/(a − x)² = {K} ⇒ 2x/({a} − x) = {num(s)} (1) ⇒ x = {sf(x, 3)} mol (1); divide by volume: [H₂] = [I₂] = {sf((a - x) / V, 3)} M, [HI] = {sf(2 * x / V, 3)} M (1).'}


def pcl5_alpha(r):
    c0 = r.choice([0.1, 0.2, 0.5, 1.0])
    K = r.choice([0.01, 0.02, 0.05, 0.1, 0.2])
    # K = c0 a²/(1-a) => c0 a² + K a - K = 0
    al = (-K + math.sqrt(K * K + 4 * c0 * K)) / (2 * c0)
    return {'stem': f'PCl₅ is heated in a closed vessel at an initial concentration of {c0} M: PCl₅(g) ⇌ PCl₃(g) + Cl₂(g), Kc = {K}. Calculate the degree of dissociation of PCl₅ and the equilibrium concentration of Cl₂.',
            'answer': f'α = {al:.3f}; [Cl₂] = {sf(c0 * al, 3)} M', 'key': f'Kc = c₀α²/(1 − α) ⇒ {c0}α² + {K}α − {K} = 0 (1); α = {al:.3f} (1); [Cl₂] = c₀α = {sf(c0 * al, 3)} M (1).'}


EQ_TERMS = [('dynamic equilibrium', 'a state in which the forward and backward reactions occur at equal rates, so concentrations remain constant'),
            ('the law of mass action', 'the law that the rate of a reaction is proportional to the product of the active masses of the reactants'),
            ('the equilibrium constant', 'the ratio of the product of equilibrium concentrations of products to that of reactants, each raised to its stoichiometric coefficient'),
            ('the reaction quotient', 'the ratio of concentrations of products to reactants at any stage of a reaction, written like the equilibrium constant'),
            ('a homogeneous equilibrium', 'an equilibrium in which all reactants and products are in the same phase'),
            ('a heterogeneous equilibrium', 'an equilibrium in which the reactants and products are in more than one phase')]

CH6S1 = {
    'topic': 'dynamic equilibrium',
    'terms': EQ_TERMS,
    'groups': [('a homogeneous equilibrium', ['N₂(g) + 3H₂(g) ⇌ 2NH₃(g)', 'H₂(g) + I₂(g) ⇌ 2HI(g)', 'CH₃COOH(l) + C₂H₅OH(l) ⇌ CH₃COOC₂H₅(l) + H₂O(l)', '2SO₂(g) + O₂(g) ⇌ 2SO₃(g)']),
               ('a heterogeneous equilibrium', ['CaCO₃(s) ⇌ CaO(s) + CO₂(g)', 'H₂O(l) ⇌ H₂O(g)', 'Ni(s) + 4CO(g) ⇌ Ni(CO)₄(g)', 'Ag₂O(s) + 2HNO₃(aq) ⇌ 2AgNO₃(aq) + H₂O(l)'])],
    'tf': (['At equilibrium the rates of forward and backward reactions are equal.', 'Equilibrium can be reached from either direction.',
            'Equilibrium is possible only in a closed system.', 'At equilibrium the concentrations of reactants and products remain constant.',
            'The vapour pressure of a liquid in a closed container at constant temperature is an equilibrium property.'],
           [('At equilibrium all reactions stop.', 'Equilibrium is dynamic; forward and backward reactions continue at equal rates.'),
            ('At equilibrium the concentrations of reactants and products are always equal.', 'They are constant, not necessarily equal.'),
            ('A catalyst changes the value of the equilibrium constant.', 'A catalyst does not change K; it only helps reach equilibrium faster.'),
            ('Pure solids are included in the expression for Kc.', 'Concentrations of pure solids and liquids are constant and are omitted.')]),
    'ar': [('In CaCO₃(s) ⇌ CaO(s) + CO₂(g), Kp = p(CO₂).', 'The concentrations (activities) of pure solids are taken as constant and omitted.', 'a', 'Only gaseous CO₂ appears in the expression.'),
           ('Equilibrium is dynamic in nature.', 'Using radioactive isotopes such as D₂ in the ammonia equilibrium shows exchange continues at equilibrium.', 'a', 'Deuterium appears in NH₃ even at equilibrium, showing reactions continue.')],
    'fams': [F('C2', 'D2', 'mcq', kc_expr), F('C3', 'D2', 'numerical', kc_calc)],
    'qa': [('C4', 'D3', 'explain', 'Water in a sealed bottle at room temperature does not appear to evaporate after some time, but in an open dish it dries up. Explain in terms of equilibrium.',
            'In the sealed bottle the rate of evaporation becomes equal to the rate of condensation (dynamic equilibrium, constant vapour pressure). In the open dish vapour escapes, so equilibrium is never reached and evaporation continues.',
            '1 mark: dynamic equilibrium in a closed system; 1 mark: open system cannot reach equilibrium.'),
           ('C4', 'D4', 'explain', 'Sugar dissolves in water until the solution is saturated, after which extra sugar stays undissolved. How could you show that the saturated solution is in dynamic equilibrium?',
            'Add a little radioactively labelled sugar to the saturated solution: radioactivity soon appears both in the solution and in the solid, showing dissolution and crystallisation continue at equal rates.',
            '1 mark: labelled (radioactive) sugar; 1 mark: exchange observed between solid and solution.')],
}

CH6S2 = {
    'topic': "equilibrium constants and Le Chatelier's principle",
    'terms': [("Le Chatelier's principle", 'the principle that a change in any factor that determines equilibrium conditions causes the system to shift so as to reduce the effect of the change'),
              ('Kp', 'the equilibrium constant expressed in terms of partial pressures of gases'),
              ('Δn_g', 'the number of moles of gaseous products minus the number of moles of gaseous reactants')],
    'tf': (['Kp = Kc when Δn_g = 0.', 'The value of K changes with temperature.', 'A large K indicates that products predominate at equilibrium.',
            'If Qc < Kc the reaction proceeds in the forward direction.', 'Adding an inert gas at constant volume does not disturb equilibrium.'],
           [('Increasing pressure favours the side with more moles of gas.', 'Increasing pressure favours the side with fewer moles of gas.'),
            ('For an exothermic reaction K increases with temperature.', 'For an exothermic reaction K decreases as temperature rises.'),
            ('If Qc > Kc the reaction moves in the forward direction.', 'If Qc > Kc the reaction moves backwards, towards reactants.'),
            ('Changing concentration changes the value of K.', 'Changing concentration shifts the position of equilibrium but does not change K.')]),
    'ar': [('In the Haber process a high pressure is used.', 'The forward reaction N₂ + 3H₂ ⇌ 2NH₃ involves a decrease in the number of moles of gas.', 'a', 'High pressure shifts equilibrium towards fewer gas moles, i.e. NH₃.'),
           ('A catalyst does not change the equilibrium composition.', 'A catalyst lowers the activation energy of both forward and backward reactions equally.', 'a', 'Both rates rise equally, so K is unchanged.'),
           ('For H₂(g) + I₂(g) ⇌ 2HI(g), Kp = Kc.', 'Δn_g = 0 for this reaction.', 'a', 'Kp = Kc(RT)^0 = Kc.')],
    'fams': [F('C3', 'D3', 'numerical', kp_kc), F('C3', 'D3', 'numerical', q_vs_k, marks=2), F('C3', 'D2', 'mcq', lechatelier), F('C2', 'D2', 'short', k_manip),
             F('C4', 'D4', 'multi_step', ice_hi, kinds=('long5',)), F('C4', 'D5', 'multi_step', pcl5_alpha, kinds=('long5',))],
    'qa': [('C4', 'D4', 'explain', 'In the manufacture of ammonia (N₂ + 3H₂ ⇌ 2NH₃, ΔH = −92.4 kJ mol⁻¹) a low temperature favours a high yield, yet about 700 K is used. Explain this choice.',
            'At low temperature the equilibrium yield is high but the rate is too slow; about 700 K with an iron catalyst and ~200 atm gives an acceptable yield at a fast rate (optimum conditions).',
            '1 mark: low T favours yield but slow; 1 mark: compromise temperature with catalyst for rate.'),
           ('C4', 'D3', 'case', 'Read and answer: [Co(H₂O)₆]²⁺(aq) (pink) + 4Cl⁻(aq) ⇌ [CoCl₄]²⁻(aq) (blue) + 6H₂O(l). A pink solution turns blue when warmed and pink again in ice.\n(i) Is the forward reaction endothermic or exothermic? (1 mark)\n(ii) Predict the colour change on adding concentrated HCl. (1 mark)\n(iii) What happens on adding water, and why? (2 marks)',
            '(i) Endothermic (heating favours blue). (ii) Turns blue (more Cl⁻ shifts forward). (iii) Turns pink: adding water (a product) shifts equilibrium backward and dilutes Cl⁻.',
            '(i) 1 (ii) 1 (iii) 1 for pink + 1 for reason.', ('case',))],
}

# ---------------- ch06 st3 acids, bases, pH ----------------

def ph_strong(r):
    kind = r.choice(['HCl', 'HNO₃', 'NaOH', 'KOH', 'Ba(OH)₂'])
    c = r.choice([1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-4, 4e-3, 2.5e-3])
    if kind in ('HCl', 'HNO₃'):
        pH = -math.log10(c)
        k = f'[H₃O⁺] = {sci(c, 2)} M ⇒ pH = −log({sci(c, 2)}) = {pH:.2f}.'
    else:
        oh = c * (2 if kind == 'Ba(OH)₂' else 1)
        pOH = -math.log10(oh)
        pH = 14 - pOH
        k = f'[OH⁻] = {sci(oh, 2)} M ⇒ pOH = {pOH:.2f}; pH = 14 − {pOH:.2f} = {pH:.2f} (298 K).'
    return {'stem': f'Calculate the pH of a {sci(c, 2)} M aqueous solution of {kind} at 298 K.', 'answer': f'{pH:.2f}', 'key': k,
            'distractors': [f'{14 - pH:.2f}', f'{pH + 0.30:.2f}', f'{pH - 1:.2f}']}


def h_from_ph(r):
    pH = round(r.uniform(1.5, 12.5), 2)
    hh = 10 ** -pH
    oh = 1e-14 / hh
    src = r.choice(['a sample of rain water', 'a soft drink', 'a soap solution', 'a sample of lake water', 'gastric juice', 'an antacid suspension'])
    return {'stem': f'The pH of {src} is {pH}. Calculate [H₃O⁺] and [OH⁻] in it at 298 K.',
            'answer': f'[H₃O⁺] = {sci(hh)} M; [OH⁻] = {sci(oh)} M', 'key': f'[H₃O⁺] = 10^−pH = 10^−{pH} = {sci(hh)} M (1); [OH⁻] = Kw/[H₃O⁺] = 1.0 × 10⁻¹⁴/{sci(hh)} = {sci(oh)} M (1).',
            'distractors': [f'[H₃O⁺] = {sci(oh)} M; [OH⁻] = {sci(hh)} M', f'[H₃O⁺] = {sci(hh * 10)} M; [OH⁻] = {sci(oh / 10)} M', f'[H₃O⁺] = {sci(pH / 14)} M; [OH⁻] = {sci(1 - pH / 14)} M']}


CONJ = [('HCl', 'Cl⁻'), ('H₂O', 'OH⁻'), ('H₃O⁺', 'H₂O'), ('NH₄⁺', 'NH₃'), ('HSO₄⁻', 'SO₄²⁻'), ('H₂CO₃', 'HCO₃⁻'), ('HCO₃⁻', 'CO₃²⁻'),
        ('CH₃COOH', 'CH₃COO⁻'), ('HF', 'F⁻'), ('H₂PO₄⁻', 'HPO₄²⁻'), ('NH₃', 'NH₂⁻'), ('HNO₃', 'NO₃⁻'), ('H₂S', 'HS⁻')]


def conjugate(r):
    a, b = r.choice(CONJ)
    if r.random() < 0.5:
        wrong = list(dict.fromkeys([x for x, y in CONJ if x != a and y != b]))
        return mcq(f'What is the conjugate base of {a}?', b, r.sample([y for x, y in CONJ if y != b and x != a], 3),
                   f'Removing H⁺ from {a} gives its conjugate base {b}.', r)
    return mcq(f'What is the conjugate acid of {b}?', a, r.sample([x for x, y in CONJ if x != a and y != b], 3),
               f'Adding H⁺ to {b} gives its conjugate acid {a}.', r)


CH6S3 = {
    'topic': 'acids, bases and pH',
    'terms': [('an Arrhenius acid', 'a substance that dissociates in water to give hydrogen ions H⁺(aq)'),
              ('a Brønsted–Lowry acid', 'a substance that is able to donate a proton, H⁺'),
              ('a Lewis acid', 'a species that accepts an electron pair'),
              ('a Lewis base', 'a species that donates an electron pair'),
              ('the ionic product of water', 'the product [H₃O⁺][OH⁻] in water, 1.0 × 10⁻¹⁴ at 298 K'),
              ('pH', 'the negative logarithm to base 10 of the hydrogen ion concentration (activity)'),
              ('an amphoteric species', 'a species that can act both as an acid and as a base')],
    'groups': [('a Lewis acid', ['BF₃', 'AlCl₃', 'Co³⁺', 'Mg²⁺', 'H⁺']), ('a Lewis base', ['NH₃', 'OH⁻', 'F⁻', 'H₂O', 'C₂H₅OC₂H₅'])],
    'tf': (['Kw = 1.0 × 10⁻¹⁴ at 298 K.', 'pH + pOH = 14 at 298 K.', 'Pure water is neutral at all temperatures.',
            'Kw increases with temperature.', 'A stronger acid has a weaker conjugate base.'],
           [('The pH of pure water is always 7.', 'pH of pure water is 7 only at 298 K; Kw changes with temperature.'),
            ('A solution with pH 3 has 10 times fewer H⁺ ions than one with pH 4.', 'pH 3 has 10 times more H⁺ than pH 4.'),
            ('BF₃ is a Lewis base.', 'BF₃ is electron deficient and accepts an electron pair: a Lewis acid.'),
            ('A strong acid has a strong conjugate base.', 'A strong acid has a very weak conjugate base.')]),
    'ar': [('Water is amphoteric.', 'Water can donate a proton to NH₃ and accept a proton from HCl.', 'a', 'It acts as an acid with NH₃ and a base with HCl.'),
           ('BF₃ acts as a Lewis acid.', 'Boron in BF₃ has an incomplete octet.', 'a', 'Electron-deficient boron accepts a lone pair.'),
           ('The pH of 10⁻⁸ M HCl is 8.', 'HCl is a strong acid.', 'd', 'A is false: the H⁺ from water (10⁻⁷ M) dominates, so pH is about 6.98. R is true.')],
    'orders': [('increasing order of pH', ['gastric juice', 'lemon juice', 'black coffee', 'pure water at 298 K', 'blood', 'milk of magnesia'],
                'Typical pH: gastric juice ~1.2, lemon ~2.2, black coffee ~5.0, water 7.0, blood ~7.4, milk of magnesia ~10.', '<'),
               ('increasing order of acid strength', ['H₂O', 'CH₃COOH', 'HF', 'HCl'], 'HCl is strong; Ka(HF) ≈ 3.5 × 10⁻⁴ > Ka(CH₃COOH) ≈ 1.8 × 10⁻⁵; water is a very weak acid.', '<')],
    'fams': [F('C2', 'D2', 'numerical', ph_strong), F('C3', 'D3', 'numerical', h_from_ph), F('C2', 'D2', 'mcq', conjugate)],
    'qa': [('C4', 'D4', 'explain', 'The pH of a 10⁻⁸ M HCl solution is not 8. Explain and estimate its pH.',
            'An acid solution cannot be basic. [H⁺] from water (≈10⁻⁷ M) must be included: [H⁺] ≈ 1.1 × 10⁻⁷ M, pH ≈ 6.96.',
            '1 mark: contribution of water; 1 mark: pH slightly below 7.')],
}

# ---------------- ch06 st4 weak acids, buffers, hydrolysis ----------------

WEAK = [('acetic acid', 1.8e-5), ('formic acid', 1.8e-4), ('benzoic acid', 6.5e-5), ('hydrofluoric acid', 3.5e-4), ('hypochlorous acid', 3.0e-8), ('nitrous acid', 4.5e-4)]


def weak_ph(r):
    a, Ka = r.choice(WEAK)
    c = r.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
    h = math.sqrt(Ka * c)
    if h / c > 0.05:
        raise ValueError
    return {'stem': f'Calculate the degree of ionisation and pH of a {c} M solution of {a}. (Ka = {sci(Ka, 2)})',
            'answer': f'α = {sci(h / c)}; pH = {-math.log10(h):.2f}', 'key': f'α = √(Ka/c) = √({sci(Ka, 2)}/{c}) = {sci(h / c)} (1); [H⁺] = cα = {sci(h)} M; pH = {-math.log10(h):.2f} (1).',
            'distractors': [f'α = {sci(h / c)}; pH = {-math.log10(c):.2f}', f'α = {sci(Ka / c)}; pH = {-math.log10(Ka * c):.2f}', f'α = {sci(h)}; pH = {-math.log10(h) / 2:.2f}']}


def weak_base(r):
    c = r.choice([0.01, 0.05, 0.1, 0.2])
    Kb = 1.8e-5
    oh = math.sqrt(Kb * c)
    pH = 14 + math.log10(oh)
    return {'stem': f'Calculate the pH of a {c} M aqueous ammonia solution. (Kb = 1.8 × 10⁻⁵)', 'answer': f'pH = {pH:.2f}',
            'key': f'[OH⁻] = √(Kb c) = {sci(oh)} M (1); pOH = {-math.log10(oh):.2f}; pH = 14 − pOH = {pH:.2f} (1).',
            'distractors': [f'pH = {14 - pH:.2f}', f'pH = {14 + math.log10(c):.2f}', f'pH = {pH - 1:.2f}']}


def buffer(r):
    a, Ka = r.choice(WEAK[:4])
    ca = r.choice([0.1, 0.2, 0.25, 0.5])
    cs = r.choice([0.05, 0.1, 0.2, 0.4, 0.5])
    pKa = -math.log10(Ka)
    pH = pKa + math.log10(cs / ca)
    salt = {'acetic acid': 'sodium acetate', 'formic acid': 'sodium formate', 'benzoic acid': 'sodium benzoate', 'hydrofluoric acid': 'sodium fluoride'}[a]
    return {'stem': f'A buffer is prepared with {ca} M {a} and {cs} M {salt}. Calculate its pH. (Ka = {sci(Ka, 2)})',
            'answer': f'pH = {pH:.2f}', 'key': f'pKa = {pKa:.2f} (1); Henderson equation: pH = pKa + log([salt]/[acid]) = {pKa:.2f} + log({cs}/{ca}) = {pH:.2f} (1).',
            'distractors': [f'pH = {pKa - math.log10(cs / ca):.2f}' if cs != ca else f'pH = {pKa + 1:.2f}', f'pH = {pKa:.2f}' if cs != ca else f'pH = {pKa - 1:.2f}', f'pH = {14 - pH:.2f}']}


def hydrolysis_ph(r):
    a, Ka = r.choice(WEAK[:3])
    c = r.choice([0.01, 0.05, 0.1, 0.2])
    salt = {'acetic acid': 'sodium acetate', 'formic acid': 'sodium formate', 'benzoic acid': 'sodium benzoate'}[a]
    pKa = -math.log10(Ka)
    pH = 7 + 0.5 * (pKa + math.log10(c))
    return {'stem': f'Calculate the pH of a {c} M solution of {salt}. (Ka of {a} = {sci(Ka, 2)})', 'answer': f'pH = {pH:.2f}',
            'key': f'Salt of a weak acid and strong base hydrolyses to give OH⁻: pH = 7 + ½(pKa + log c) = 7 + ½({pKa:.2f} + {math.log10(c):.2f}) = {pH:.2f}.',
            'distractors': [f'pH = {14 - pH:.2f}', f'pH = 7.00', f'pH = {7 + pKa + math.log10(c):.2f}']}


CH6S4 = {
    'topic': 'weak electrolytes, buffers and salt hydrolysis',
    'terms': [('a buffer solution', 'a solution that resists change in pH on dilution or on addition of small amounts of acid or alkali'),
              ('the degree of ionisation', 'the fraction of the total amount of a weak electrolyte that is present as ions at equilibrium'),
              ('salt hydrolysis', 'the reaction of the cation or anion of a salt with water that changes the pH of the solution'),
              ('the acid ionisation constant', 'the equilibrium constant Ka for the ionisation of a weak acid in water'),
              ("Ostwald's dilution law", 'the relation α = √(Ka/c), showing that the degree of ionisation of a weak electrolyte increases on dilution')],
    'groups': [('a salt whose aqueous solution is acidic', ['NH₄Cl', '(NH₄)₂SO₄', 'FeCl₃', 'AlCl₃', 'CuSO₄']),
               ('a salt whose aqueous solution is basic', ['CH₃COONa', 'Na₂CO₃', 'NaCN', 'K₂CO₃', 'NaHCO₃']),
               ('a salt whose aqueous solution is neutral', ['NaCl', 'KNO₃', 'Na₂SO₄', 'KCl', 'NaNO₃'])],
    'groups2': [('an acidic buffer', ['CH₃COOH + CH₃COONa', 'HCOOH + HCOONa', 'H₂CO₃ + NaHCO₃']), ('a basic buffer', ['NH₄OH + NH₄Cl', 'NH₃ + (NH₄)₂SO₄'])],
    'tf': (['The degree of ionisation of a weak acid increases on dilution.', 'An aqueous solution of NH₄Cl is acidic.',
            'A mixture of acetic acid and sodium acetate acts as a buffer.', 'pKa + pKb = 14 for a conjugate acid–base pair at 298 K.',
            'Blood is buffered at a pH of about 7.4.'],
           [('A solution of CH₃COONa is acidic.', 'Acetate ions hydrolyse to give OH⁻, so the solution is basic.'),
            ('A mixture of HCl and NaCl is a buffer.', 'HCl is a strong acid; a buffer needs a weak acid and its salt (or weak base and its salt).'),
            ('Degree of ionisation of a weak acid decreases on dilution.', 'By Ostwald\'s law, α increases on dilution.'),
            ('A higher pKa means a stronger acid.', 'A higher pKa means a weaker acid.')]),
    'ar': [('An aqueous solution of sodium carbonate is basic.', 'CO₃²⁻ ions react with water to form HCO₃⁻ and OH⁻.', 'a', 'Hydrolysis of carbonate releases OH⁻.'),
           ('A buffer resists change in pH on adding a little acid.', 'The conjugate base in the buffer removes the added H⁺.', 'a', 'e.g. CH₃COO⁻ + H⁺ → CH₃COOH.')],
    'fams': [F('C3', 'D3', 'numerical', weak_ph), F('C3', 'D2', 'numerical', weak_base), F('C3', 'D3', 'numerical', buffer),
             F('C4', 'D4', 'numerical', hydrolysis_ph, marks=3)],
    'qa': [('C4', 'D4', 'explain', 'Explain, with equations, how a buffer of acetic acid and sodium acetate keeps its pH almost constant when a few drops of HCl or NaOH are added.',
            'Added H⁺ is removed by acetate: CH₃COO⁻ + H⁺ → CH₃COOH. Added OH⁻ is removed by acetic acid: CH₃COOH + OH⁻ → CH₃COO⁻ + H₂O. The ratio [salt]/[acid] changes little, so pH hardly changes.',
            '1 mark each equation; the ratio argument is needed for full marks.'),
           ('C4', 'D5', 'long', '(a) Derive the Henderson–Hasselbalch equation for an acidic buffer. (b) Calculate the pH of a buffer that is 0.10 M in CH₃COOH and 0.20 M in CH₃COONa (pKa = 4.74). (c) What is the pH after diluting this buffer ten times? Explain.',
            '(a) Ka = [H⁺][A⁻]/[HA] ⇒ pH = pKa + log([A⁻]/[HA]). (b) 4.74 + log 2 = 5.04. (c) Still 5.04: dilution does not change the ratio [A⁻]/[HA].',
            '(a) 2 marks (b) 2 marks (c) 1 mark.')],
}

# ---------------- ch06 st5 solubility equilibria ----------------

KSP = [('AgCl', 1.8e-10, 'AB'), ('BaSO₄', 1.1e-10, 'AB'), ('AgBr', 5.0e-13, 'AB'), ('CaF₂', 5.3e-9, 'AB2'), ('PbI₂', 7.1e-9, 'AB2'),
       ('Mg(OH)₂', 1.8e-11, 'AB2'), ('Ag₂CrO₄', 1.1e-12, 'A2B'), ('CaCO₃', 2.8e-9, 'AB'), ('PbCl₂', 1.6e-5, 'AB2'), ('Ag₂CO₃', 8.1e-12, 'A2B')]


def ksp_s(r):
    salt, K, t = r.choice(KSP)
    if t == 'AB':
        s = math.sqrt(K)
        rel = 'Ksp = s × s = s²'
    else:
        s = (K / 4) ** (1 / 3)
        rel = 'Ksp = s(2s)² = 4s³' if t == 'AB2' else 'Ksp = (2s)²s = 4s³'
    return {'stem': f'The solubility product of {salt} is {sci(K, 2)} at 298 K. Calculate its molar solubility in water.',
            'answer': f'{sci(s)} mol L⁻¹', 'key': f'{rel} (1) ⇒ s = {sci(s)} mol L⁻¹ (1).',
            'distractors': [sci(math.sqrt(K)) + ' mol L⁻¹' if t != 'AB' else sci((K / 4) ** (1 / 3)) + ' mol L⁻¹', sci(K / 2) + ' mol L⁻¹', sci(s * 2) + ' mol L⁻¹']}


def ksp_from_s(r):
    salt, K, t = r.choice(KSP)
    s = math.sqrt(K) if t == 'AB' else (K / 4) ** (1 / 3)
    s = float(f'{s:.2e}')
    K2 = s * s if t == 'AB' else 4 * s ** 3
    return {'stem': f'The molar solubility of {salt} in water at 298 K is {sci(s, 2)} mol L⁻¹. Calculate its solubility product.',
            'answer': f'Ksp = {sci(K2)}', 'key': f'{"Ksp = s²" if t == "AB" else "Ksp = 4s³"} = {sci(K2)}.',
            'distractors': [f'Ksp = {sci(s * s if t != "AB" else 4 * s ** 3)}', f'Ksp = {sci(2 * s * s)}', f'Ksp = {sci(s)}']}


def precip(r):
    salt, K, t = r.choice([x for x in KSP if x[2] == 'AB'])
    ions = {'AgCl': ('Ag⁺', 'Cl⁻', 'AgNO₃', 'NaCl'), 'BaSO₄': ('Ba²⁺', 'SO₄²⁻', 'BaCl₂', 'Na₂SO₄'), 'AgBr': ('Ag⁺', 'Br⁻', 'AgNO₃', 'KBr'), 'CaCO₃': ('Ca²⁺', 'CO₃²⁻', 'CaCl₂', 'Na₂CO₃')}[salt]
    c1 = r.choice([1e-3, 1e-4, 2e-5, 1e-5, 1e-6, 5e-7])
    c2 = r.choice([1e-3, 1e-4, 2e-5, 1e-5, 1e-6, 5e-7])
    Q = (c1 / 2) * (c2 / 2)
    if abs(math.log10(Q / K)) < 0.3:
        raise ValueError
    res = 'a precipitate forms' if Q > K else 'no precipitate forms'
    return {'stem': f'Equal volumes of {sci(c1, 1)} M {ions[2]} and {sci(c2, 1)} M {ions[3]} are mixed. Will {salt} precipitate? (Ksp of {salt} = {sci(K, 2)})',
            'answer': f'Qsp = {sci(Q, 2)}; {res}', 'key': f'After mixing each concentration halves: [{ions[0]}] = {sci(c1 / 2, 1)}, [{ions[1]}] = {sci(c2 / 2, 1)} M (1); Qsp = {sci(Q, 2)} {">" if Q > K else "<"} Ksp ⇒ {res} (1).',
            'distractors': [f'Qsp = {sci(Q, 2)}; {"no precipitate forms" if Q > K else "a precipitate forms"}', f'Qsp = {sci(c1 * c2, 2)}; {res}', f'Qsp = {sci(c1 * c2, 2)}; {"no precipitate forms" if c1 * c2 > K else "a precipitate forms"}']}


def common_ion(r):
    salt, K, t = r.choice([x for x in KSP if x[2] in ('AB', 'AB2')])
    c = r.choice([0.01, 0.05, 0.1, 0.2])
    if t == 'AB':
        s = K / c
        s0 = math.sqrt(K)
        add = {'AgCl': 'NaCl', 'BaSO₄': 'Na₂SO₄', 'AgBr': 'KBr', 'CaCO₃': 'Na₂CO₃'}[salt]
        rel = f'Ksp = s(s + {c}) ≈ s × {c}'
    else:
        s = K / (c * c)
        s0 = (K / 4) ** (1 / 3)
        add = {'CaF₂': 'NaF', 'PbI₂': 'KI', 'Mg(OH)₂': 'NaOH', 'PbCl₂': 'NaCl'}[salt]
        rel = f'Ksp = s(2s + {c})² ≈ s × {c}²'
    if s > c / 20:
        raise ValueError
    return {'stem': f'Calculate the molar solubility of {salt} (Ksp = {sci(K, 2)}) in a {c} M solution of {add}, and compare it with its solubility in pure water.',
            'answer': f'{sci(s)} mol L⁻¹ (in water {sci(s0)} mol L⁻¹); solubility is lowered by the common ion',
            'key': f'{rel} ⇒ s = {sci(s)} mol L⁻¹ (2); in pure water s = {sci(s0)} mol L⁻¹, so the common ion suppresses solubility (1).'}


CH6S5 = {
    'topic': 'solubility equilibria',
    'terms': [('the solubility product', 'the product of the molar concentrations of the ions of a sparingly soluble salt in its saturated solution, each raised to the power of its number in the formula'),
              ('the common ion effect', 'the suppression of the ionisation or solubility of an electrolyte by adding a strong electrolyte that has an ion in common with it'),
              ('the ionic product (Qsp)', 'the product of ionic concentrations, raised to suitable powers, in a solution that may not be saturated'),
              ('molar solubility', 'the number of moles of a solute dissolved in one litre of its saturated solution')],
    'tf': (['A precipitate forms when Qsp exceeds Ksp.', 'Adding NaCl lowers the solubility of AgCl.', 'Ksp of a salt depends on temperature.',
            'For a salt of type AB₂, Ksp = 4s³.', 'Pure NaCl can be obtained by passing HCl gas into a saturated NaCl solution.'],
           [('Adding a common ion increases the solubility of a sparingly soluble salt.', 'A common ion decreases the solubility (Le Chatelier).'),
            ('A precipitate forms whenever Qsp is less than Ksp.', 'A precipitate forms only when Qsp > Ksp.'),
            ('For AgCl, Ksp = 2s.', 'For AgCl, Ksp = s².'),
            ('The salt with the smaller Ksp is always less soluble, whatever its formula type.', 'Ksp values can be compared directly only for salts of the same formula type.')]),
    'ar': [('The solubility of AgCl is less in 0.1 M NaCl than in water.', 'Cl⁻ is a common ion that shifts AgCl(s) ⇌ Ag⁺ + Cl⁻ to the left.', 'a', 'Common ion effect lowers solubility.'),
           ('A precipitate of BaSO₄ forms when Qsp > Ksp.', 'When the ionic product exceeds Ksp the solution is supersaturated.', 'a', 'Excess ions combine to form solid until Q = Ksp.')],
    'fams': [F('C2', 'D2', 'numerical', ksp_s), F('C2', 'D2', 'numerical', ksp_from_s), F('C3', 'D3', 'numerical', precip, marks=2),
             F('C4', 'D4', 'multi_step', common_ion, kinds=('long5',))],
    'qa': [('C4', 'D3', 'explain', 'In the purification of common salt, HCl gas is passed through a saturated solution of impure NaCl. Pure NaCl crystallises out. Explain.',
            'HCl adds Cl⁻ (a common ion); the ionic product [Na⁺][Cl⁻] exceeds the solubility product, so pure NaCl precipitates while soluble impurities stay in solution.',
            '1 mark: common ion Cl⁻; 1 mark: ionic product exceeds Ksp ⇒ precipitation.')],
}

SPECS = {'ch04-st1': CH4S1, 'ch04-st2': CH4S2, 'ch04-st3': CH4S3, 'ch04-st4': CH4S4, 'ch04-st5': CH4S5,
         'ch05-st1': CH5S1, 'ch05-st2': CH5S2, 'ch05-st3': CH5S3, 'ch05-st4': CH5S4,
         'ch06-st1': CH6S1, 'ch06-st2': CH6S2, 'ch06-st3': CH6S3, 'ch06-st4': CH6S4, 'ch06-st5': CH6S5}

FAMILIES = build_all(P, SPECS)
