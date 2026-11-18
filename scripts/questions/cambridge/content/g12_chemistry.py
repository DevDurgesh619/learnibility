"""Cambridge International A Level Chemistry 9701, syllabus topics 23-37 (A Level), CUP coursebook 3rd ed. ch 19-30, grade 12.

Paper 4 (A Level structured) and Paper 5 (planning, analysis and evaluation) styles, with Paper 1-style
MCQs for recall. Knowledge-pack builders (key terms, MCQs, explain items, misconceptions, long answers)
are shared from g9_biology.py; formula rendering, Ar values and number formatting from g11_chemistry.py;
the marking-key enrichment from g11_biology.py.

Data tables drive parameterised templates: Born-Haber cycles, hydration and solution enthalpies,
Faraday's laws, E° cells and feasibility, the Nernst equation, pH / Ka / Kw, buffers, titration curves
and indicators, Ksp and the common ion effect, partition coefficients, initial-rates data, half-lives,
the Arrhenius equation, entropy and Gibbs free energy, ΔG = −nFE°, d-electron configurations and
complex ions, Kstab, MnO4⁻ / Cr2O7²⁻ / thiosulfate titrations, hydrogenation enthalpies of benzene,
pKa of chloroacids, amino-acid electrophoresis, polymer repeat units, Rf and GLC peak areas,
13C and 1H NMR, the M+1 peak, and multi-step synthetic routes.
"""
import math
import re
from ._lib import compose, sf, sci, sup, person, two_people, city  # noqa: F401
from .g9_biology import cap, low, fx, Q, MQ, NQ, T, facts, mcqs, explain, shorts, longs, myths  # noqa: F401
from .g11_chemistry import F, Mr, g3, sgn, AR  # noqa: F401
from .g11_biology import _wrap as _bio_wrap
from .g9_biology import NQ as _NQ0


def _qfix(s):
    """Turn a converted 'What is ...' final sentence into a question."""
    mm = re.match(r'^(.*?)(\s*\[[^\[\]]*\])?$', s, re.S)
    body, tail = mm.group(1).rstrip(), mm.group(2) or ''
    if body.endswith('.'):
        last = re.split(r'(?<=[.?!])\s+(?=[A-Z])', body)[-1]
        if re.match(r'(What|How|At what|Which)\b', last):
            body = body[:-1] + '?'
    return body + tail


def NQ(r, stem, *a, **k):  # noqa: F811
    return _NQ0(r, _qfix(stem), *a, **k)

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

FARADAY = 96500
L_AV = 6.02e23
RGAS = 8.31


def case(r, intro, parts, k=(2, 3, 4), typ='case'):
    return compose(r, intro, parts, k=k, type_=typ)


def P_(text, ans, key):
    return lambda r: (text, ans, key)


def m(x):
    """Unicode minus for a formatted number string."""
    return str(x).replace('-', '−')


def kj(x, dp=0):
    """kJ mol⁻¹ value with sign."""
    return sgn(x, dp) + ' kJ mol⁻¹'


def who(r):
    return person(r)


def lab(r):
    return r.choice(['a school laboratory', 'a college laboratory', 'a quality-control laboratory', 'a research laboratory', 'a university teaching laboratory'])


# ===================================================================== 1 Lattice energy
METAL = {  # atomisation, IE1, IE2 (kJ mol⁻¹)
    'Li': (159, 520, 7298), 'Na': (107, 496, 4562), 'K': (89, 419, 3051), 'Rb': (81, 403, 2633),
    'Mg': (148, 736, 1450), 'Ca': (178, 590, 1145), 'Sr': (164, 550, 1064), 'Ba': (180, 503, 965)}
NONMET = {  # atomisation (per mole of atoms), EA1, EA2
    'F': (79, -328, None), 'Cl': (121, -349, None), 'Br': (112, -325, None), 'I': (107, -295, None), 'O': (249, -141, 798)}
SALTS = {  # formula: (metal, nonmetal, charge of cation, n anions, ΔHf)
    'NaF': ('Na', 'F', 1, 1, -574), 'NaCl': ('Na', 'Cl', 1, 1, -411), 'NaBr': ('Na', 'Br', 1, 1, -361), 'NaI': ('Na', 'I', 1, 1, -288),
    'KF': ('K', 'F', 1, 1, -567), 'KCl': ('K', 'Cl', 1, 1, -437), 'KBr': ('K', 'Br', 1, 1, -394), 'KI': ('K', 'I', 1, 1, -328),
    'LiF': ('Li', 'F', 1, 1, -616), 'LiCl': ('Li', 'Cl', 1, 1, -409), 'RbCl': ('Rb', 'Cl', 1, 1, -435),
    'MgO': ('Mg', 'O', 2, 1, -602), 'CaO': ('Ca', 'O', 2, 1, -635), 'SrO': ('Sr', 'O', 2, 1, -592), 'BaO': ('Ba', 'O', 2, 1, -548),
    'MgCl2': ('Mg', 'Cl', 2, 2, -641), 'CaCl2': ('Ca', 'Cl', 2, 2, -796), 'BaCl2': ('Ba', 'Cl', 2, 2, -859), 'MgF2': ('Mg', 'F', 2, 2, -1124),
    'CaF2': ('Ca', 'F', 2, 2, -1228), 'MgBr2': ('Mg', 'Br', 2, 2, -524), 'SrCl2': ('Sr', 'Cl', 2, 2, -829)}
NAME_M = {'Li': 'lithium', 'Na': 'sodium', 'K': 'potassium', 'Rb': 'rubidium', 'Mg': 'magnesium', 'Ca': 'calcium', 'Sr': 'strontium', 'Ba': 'barium'}
NAME_X = {'F': ('fluorine', 'fluoride'), 'Cl': ('chlorine', 'chloride'), 'Br': ('bromine', 'bromide'), 'I': ('iodine', 'iodide'), 'O': ('oxygen', 'oxide')}


def salt_name(f):
    mt, x, _, _, _ = SALTS[f]
    return f'{NAME_M[mt]} {NAME_X[x][1]}'


def bh_terms(f):
    """Return list of (label, value) and lattice energy."""
    mt, x, z, n, hf = SALTS[f]
    at_m, ie1, ie2 = METAL[mt]
    at_x, ea1, ea2 = NONMET[x]
    terms = [('enthalpy change of atomisation of ' + NAME_M[mt], at_m), ('first ionisation energy of ' + NAME_M[mt], ie1)]
    if z == 2:
        terms.append(('second ionisation energy of ' + NAME_M[mt], ie2))
    terms.append((f'enthalpy change of atomisation of {NAME_X[x][0]}' + (f' (× {n})' if n > 1 else ''), at_x * n))
    terms.append((f'first electron affinity of {NAME_X[x][0]}' + (f' (× {n})' if n > 1 else ''), ea1 * n))
    if x == 'O':
        terms.append(('second electron affinity of oxygen', ea2))
    le = hf - sum(v for _, v in terms)
    return terms, le, hf


t = T('Lattice energy, enthalpy of atomisation and electron affinity: definitions', 'lattice energy, enthalpy of atomisation')
facts(t, [('lattice energy', 'the enthalpy change when 1 mole of an ionic compound is formed from its gaseous ions under standard conditions'),
          ('enthalpy change of atomisation', 'the enthalpy change when 1 mole of gaseous atoms is formed from the element in its standard state under standard conditions'),
          ('first electron affinity', 'the enthalpy change when 1 mole of electrons is added to 1 mole of gaseous atoms to form 1 mole of gaseous 1− ions'),
          ('second electron affinity', 'the enthalpy change when 1 mole of electrons is added to 1 mole of gaseous 1− ions to form 1 mole of gaseous 2− ions'),
          ('first ionisation energy', 'the energy needed to remove 1 mole of electrons from 1 mole of gaseous atoms to form 1 mole of gaseous 1+ ions'),
          ('enthalpy change of hydration', 'the enthalpy change when 1 mole of gaseous ions dissolves in water to form an infinitely dilute solution'),
          ('enthalpy change of solution', 'the enthalpy change when 1 mole of an ionic solid dissolves in water to form an infinitely dilute solution')])
mcqs(t, [('Which equation represents the lattice energy of sodium chloride?', 'Na⁺(g) + Cl⁻(g) → NaCl(s)', 'Formation of 1 mol of solid from gaseous ions.', ['NaCl(s) → Na⁺(g) + Cl⁻(g)', 'Na(s) + ½Cl₂(g) → NaCl(s)', 'Na⁺(aq) + Cl⁻(aq) → NaCl(s)']),
         ('Which equation represents the enthalpy change of atomisation of chlorine?', '½Cl₂(g) → Cl(g)', 'Per mole of gaseous atoms formed.', ['Cl₂(g) → 2Cl(g)', 'Cl(g) → Cl⁻(g)', 'Cl₂(l) → Cl₂(g)']),
         ('Why is the second electron affinity of oxygen endothermic?', 'An electron is added to a negative ion, so energy is needed to overcome repulsion', 'O⁻(g) + e⁻ → O²⁻(g) is +798 kJ mol⁻¹.', ['Oxygen has a full outer shell', 'The electron is added to an inner shell', 'Oxygen atoms are very large']),
         ('Which equation represents the first electron affinity of bromine?', 'Br(g) + e⁻ → Br⁻(g)', 'Gaseous atoms to gaseous 1− ions.', ['½Br₂(l) + e⁻ → Br⁻(g)', 'Br₂(g) + 2e⁻ → 2Br⁻(g)', 'Br⁻(g) → Br(g) + e⁻']),
         ('Which enthalpy change is always exothermic?', 'Lattice energy', 'Ions attract each other; forming the lattice releases energy.', ['Enthalpy change of atomisation', 'First ionisation energy', 'Second electron affinity'])])
shorts(t, [('Write an equation, with state symbols, for the enthalpy change of atomisation of magnesium.', 'Mg(s) → Mg(g)', 'correct species [1]; state symbols [1] [2]'),
           ('Write an equation, with state symbols, for the lattice energy of calcium chloride.', 'Ca²⁺(g) + 2Cl⁻(g) → CaCl₂(s)', 'correct species and charges [1]; state symbols [1] [2]')])
explain(t, [('Explain why first electron affinities of the halogens are exothermic.', 'The added electron is attracted by the nucleus (effective nuclear charge) of the atom; energy is released as it enters the outer shell.', 'attraction between nucleus and incoming electron [1]; energy released [1] [2]'),
            ('Explain why the enthalpy change of atomisation of bromine is not simply half the Br–Br bond energy.', 'Bromine is a liquid in its standard state, so energy is also needed to vaporise it (overcome intermolecular forces) before the bonds are broken.', 'bromine is liquid [1]; vaporisation energy also required [1] [2]'),
            ('Explain why the second ionisation energy of magnesium is greater than the first.', 'The second electron is removed from a positive ion; there is greater attraction between the nucleus and the remaining electrons (less shielding/repulsion), so more energy is needed.', 'removed from positive ion [1]; stronger attraction [1] [2]'),
            ('Explain why lattice energy cannot be measured directly.', 'Gaseous ions cannot be made and combined directly under controlled conditions; it is calculated indirectly using a Born–Haber cycle (Hess\'s law).', 'cannot form lattice from gaseous ions experimentally [1]; Born–Haber cycle / Hess\'s law [1] [2]')])
myths(t, [('Lattice energy is the energy needed to break an ionic lattice into its ions.', 'In the 9701 syllabus, lattice energy is the (exothermic) enthalpy change when 1 mole of solid forms from its gaseous ions.'),
          ('The enthalpy change of atomisation of chlorine refers to Cl₂(g) → 2Cl(g).', 'It refers to forming 1 mole of gaseous atoms: ½Cl₂(g) → Cl(g).'),
          ('All electron affinities are exothermic.', 'First electron affinities are usually exothermic but second electron affinities (e.g. O⁻ → O²⁻) are endothermic because of repulsion.')])
mcqs(t, [('For which change is the enthalpy change equal to the first electron affinity of fluorine?', 'F(g) + e⁻ → F⁻(g)', 'Gaseous atom to gaseous ion.', ['½F₂(g) + e⁻ → F⁻(g)', 'F₂(g) + 2e⁻ → 2F⁻(g)', 'F(g) → F⁺(g) + e⁻']),
         ('Which process has the most endothermic enthalpy change?', 'Mg⁺(g) → Mg²⁺(g) + e⁻', 'Second IE of Mg is 1450 kJ mol⁻¹.', ['Na(g) → Na⁺(g) + e⁻', 'Cl(g) + e⁻ → Cl⁻(g)', '½Cl₂(g) → Cl(g)'])], D=(2, 3), C='C2')

EQ_KINDS = [('the lattice energy of {s}', lambda f: f'{_ions(f)} → {F(f)}(s)'),
            ('the standard enthalpy change of formation of {s}', lambda f: f'{_elems(f)} → {F(f)}(s)'),
            ('the first ionisation energy of {m}', lambda f: f'{SALTS[f][0]}(g) → {SALTS[f][0]}⁺(g) + e⁻'),
            ('the enthalpy change of atomisation of {m}', lambda f: f'{SALTS[f][0]}(s) → {SALTS[f][0]}(g)'),
            ('the first electron affinity of {x}', lambda f: f'{SALTS[f][1]}(g) + e⁻ → {SALTS[f][1]}⁻(g)')]
STD_STATE = {'F': 'F₂(g)', 'Cl': 'Cl₂(g)', 'Br': 'Br₂(l)', 'I': 'I₂(s)', 'O': 'O₂(g)'}


def _ions(f):
    mt, x, z, n, _ = SALTS[f]
    ch = '⁺' if z == 1 else '²⁺'
    an = '²⁻' if x == 'O' else '⁻'
    return f'{mt}{ch}(g) + {(str(n) if n > 1 else "")}{x}{an}(g)'


def _elems(f):
    mt, x, z, n, _ = SALTS[f]
    s_ = STD_STATE[x]
    coef = {1: '½', 2: ''}[n] if x != 'O' else '½'
    return f'{mt}(s) + {coef}{s_}'


@t.add('C3', (1, 2, 3, 4), 'short')
def which_eq(r, D):
    f = r.choice(list(SALTS))
    i = r.randrange(len(EQ_KINDS))
    name, fn = EQ_KINDS[i]
    mt, x = SALTS[f][0], SALTS[f][1]
    nm = name.format(s=salt_name(f), m=NAME_M[mt], x=NAME_X[x][0])
    if D <= 2:
        others = [EQ_KINDS[j][0].format(s=salt_name(f), m=NAME_M[mt], x=NAME_X[x][0]) for j in range(len(EQ_KINDS)) if j != i]
        return MQ(r, f'Which enthalpy change is represented by the equation {fn(f)}?', cap(nm), [cap(o) for o in others], f'{fn(f)} represents {nm}.')
    return Q(f'Write an equation, with state symbols, to represent {nm}.' + (' Explain whether the enthalpy change is exothermic or endothermic.' if D >= 4 else ''),
             fn(f) + ('' if D < 4 else ('; exothermic (attraction / bond formation releases energy)' if i in (0, 1, 4) else '; endothermic (energy needed to break bonds / remove electrons)')),
             'correct species and amounts [1]; state symbols [1]' + (' [2]' if D < 4 else '; sign with reason [1] [3]'), 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def defs_case(r, D):
    f = r.choice(['NaCl', 'KBr', 'MgO', 'CaCl2', 'LiF', 'BaO'])
    st = f'{who(r)} is preparing a Born–Haber cycle for {salt_name(f)}, {F(f)}.'
    mt, x = SALTS[f][0], SALTS[f][1]
    parts = [P_(f'Define the term lattice energy and write an equation for the lattice energy of {F(f)}.', f'Enthalpy change when 1 mol of ionic solid forms from its gaseous ions; {_ions(f)} → {F(f)}(s).', 'definition [2]; equation with state symbols [1] [3]'),
             P_(f'Write equations for the enthalpy changes of atomisation of {NAME_M[mt]} and of {NAME_X[x][0]}.', f'{mt}(s) → {mt}(g); {"½" + STD_STATE[x]} → {x}(g)', 'each equation [1] [2]'),
             P_(f'Explain why the first ionisation energy of {NAME_M[mt]} is endothermic.', 'Energy is needed to overcome the attraction between the nucleus and the outer electron.', '[1]'),
             P_('State Hess\'s law and explain why it allows lattice energy to be calculated.', 'The total enthalpy change for a reaction is independent of the route taken; so the enthalpy of formation equals the sum of the steps in the cycle, and the one unknown (lattice energy) can be found.', 'statement [1]; application to cycle [1] [2]')]
    if x == 'O':
        parts.append(P_('Explain why the second electron affinity of oxygen is endothermic.', 'The incoming electron is repelled by the negative O⁻ ion, so energy must be supplied.', '[2]'))
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Define lattice energy, enthalpy change of atomisation and first electron affinity, and explain the factors that make each exothermic or endothermic.', 'Definitions with gaseous species and 1 mol; lattice energy exothermic (electrostatic attraction between oppositely charged ions); atomisation endothermic (bonds/metallic bonding broken, vaporisation); first EA exothermic (nuclear attraction for added electron), second EA endothermic (repulsion by negative ion); IE endothermic.',
           'three definitions [3]; sign of lattice energy explained [1]; atomisation [1]; EA1 and EA2 [2] [7]')])
t1a = t

# ---------------------------------------------------------------------
t = T('Constructing Born–Haber cycles and calculating lattice energy', 'constructing born–haber cycles')
facts(t, [('Born–Haber cycle', 'an enthalpy cycle that relates the enthalpy change of formation of an ionic compound to its lattice energy and the energy changes in forming gaseous ions'),
          ("Hess's law", 'the total enthalpy change for a reaction is independent of the route by which it takes place, provided the initial and final conditions are the same'),
          ('standard enthalpy change of formation', 'the enthalpy change when 1 mole of a compound is formed from its elements in their standard states under standard conditions')])
mcqs(t, [('In a Born–Haber cycle for NaCl, which step follows the formation of Na(g)?', 'Na(g) → Na⁺(g) + e⁻', 'Atomise, ionise, then add electron to Cl.', ['Na⁺(g) + Cl⁻(g) → NaCl(s)', 'Na(s) → Na(g)', '½Cl₂(g) → Cl(g)']),
         ('Lattice energy is calculated from a Born–Haber cycle using which relationship?', 'ΔHf = sum of all other steps + lattice energy', 'Hess\'s law: both routes from elements to solid give the same total.', ['Lattice energy = ΔHf + sum of other steps', 'Lattice energy = −ΔHf', 'Lattice energy = IE + EA']),
         ('How many times is the atomisation enthalpy of chlorine included in a Born–Haber cycle for MgCl₂?', 'Twice', 'Two Cl atoms are needed per formula unit.', ['Once', 'Three times', 'Not at all']),
         ('Which value is needed in a Born–Haber cycle for CaO but not for CaCl₂?', 'The second electron affinity of oxygen', 'O²⁻ requires two electron affinities.', ['The second ionisation energy of calcium', 'The enthalpy change of atomisation of calcium', 'The first electron affinity'])])
shorts(t, [('State the steps, in order, that are needed to form K⁺(g) and Cl⁻(g) from K(s) and Cl₂(g).', 'Atomise potassium; ionise potassium (first IE); atomise chlorine (½Cl₂ → Cl); first electron affinity of chlorine.', 'atomisation steps [1]; IE and EA [1] [2]')])
explain(t, [('Explain why the lattice energy calculated from a Born–Haber cycle may differ from a value calculated from a purely ionic model.', 'Real compounds may have some covalent character (polarisation of the anion by the cation), which increases the strength of bonding compared with a purely ionic model, so the experimental value is more exothermic.', 'covalent character / polarisation [1]; experimental more exothermic [1] [2]'),
            ('Explain why the formation of MgO is exothermic even though forming Mg²⁺ and O²⁻ ions from the elements is strongly endothermic.', 'The lattice energy of MgO is very exothermic because the ions are small and doubly charged, releasing more than enough energy to compensate for the endothermic ionisation and second electron affinity steps.', 'endothermic steps identified [1]; very exothermic lattice energy [1]; reason: small, 2+/2− ions [1] [3]'),
            ('Use a Born–Haber argument to explain why MgCl (containing Mg⁺) is not formed.', 'Although forming Mg⁺ needs less ionisation energy, the lattice energy of MgCl would be much less exothermic than that of MgCl₂ (smaller charge), so ΔHf of MgCl₂ is far more negative; MgCl₂ is more stable.', 'less ionisation for Mg⁺ [1]; much smaller lattice energy for MgCl [1]; MgCl₂ more exothermic ΔHf [1] [3]')])
myths(t, [('In a Born–Haber cycle, the lattice energy equals the enthalpy change of formation.', 'ΔHf equals the sum of atomisation, ionisation, electron affinity and lattice energy terms; lattice energy is found by rearranging this.'),
          ('For MgCl₂, the first electron affinity of chlorine is used once.', 'Two chloride ions form, so 2 × first electron affinity (and 2 × atomisation of chlorine) are used.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def born_haber(r, D):
    f = r.choice(list(SALTS) if D >= 3 else [k for k in SALTS if SALTS[k][2] == 1 and SALTS[k][3] == 1])
    terms, le, hf = bh_terms(f)
    target = r.choice(['LE', 'LE', 'HF', 'EA']) if D >= 4 else 'LE'
    data = '; '.join(f'{lab_} {sgn(v)}' for lab_, v in terms)
    if target == 'LE':
        st = f'Use the following data (kJ mol⁻¹) to calculate the lattice energy of {salt_name(f)}, {F(f)}: enthalpy change of formation of {F(f)} {sgn(hf)}; {data}.'
        key = f'LE = ΔHf − (sum of other terms) [1]; sum = {sgn(sum(v for _, v in terms))} [1]; LE = {sgn(hf)} − ({sgn(sum(v for _, v in terms))}) = {kj(le)} [1] [3]'
        ans = kj(le)
        val = le
    elif target == 'HF':
        st = f'The lattice energy of {F(f)} is {sgn(le)} kJ mol⁻¹. Use this and the following data (kJ mol⁻¹) to calculate the standard enthalpy change of formation of {F(f)}: {data}.'
        key = f'ΔHf = sum of terms + lattice energy [1]; = {sgn(sum(v for _, v in terms))} + ({sgn(le)}) [1] = {kj(hf)} [1] [3]'
        ans = kj(hf)
        val = hf
    else:
        mt, x, z, n, _ = SALTS[f]
        ea_lab = [i for i, (lab_, _) in enumerate(terms) if 'first electron affinity' in lab_][0]
        ea = terms[ea_lab][1]
        rest = [(lab_, v) for i, (lab_, v) in enumerate(terms) if i != ea_lab]
        data2 = '; '.join(f'{lab_} {sgn(v)}' for lab_, v in rest)
        st = f'Use the data (kJ mol⁻¹) to calculate the first electron affinity of {NAME_X[x][0]}: lattice energy of {F(f)} {sgn(le)}; enthalpy change of formation {sgn(hf)}; {data2}.'
        key = f'ΔHf = Σ terms + LE [1]; {n} × EA = {sgn(hf)} − ({sgn(sum(v for _, v in rest))}) − ({sgn(le)}) = {sgn(ea)} [1]; EA = {kj(ea / n)} [1] [3]'
        ans = kj(ea / n)
        val = ea / n
    if D <= 2:
        o = NQ(r, st.replace('Use the following data', 'Using the data').replace('to calculate', 'what is'), val, [-val, val + 2 * (terms[1][1]), hf + sum(v for _, v in terms), val / 2], ' kJ mol⁻¹', key, f=lambda v: sgn(v))
        return o
    if D >= 5:
        st += ' Draw the Born–Haber cycle, labelling each step, and explain why the lattice energy is exothermic.'
        key = key.replace(' [3]', '') + '; cycle drawn with all species and state symbols [2]; attraction between ions releases energy [1] [6]'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def bh_case(r, D):
    f = r.choice(['MgO', 'CaO', 'MgCl2', 'CaCl2', 'SrO', 'CaF2', 'BaCl2'])
    terms, le, hf = bh_terms(f)
    data = '; '.join(f'{lab_} {sgn(v)}' for lab_, v in terms)
    st = f'The following data (kJ mol⁻¹) refer to {salt_name(f)}: enthalpy change of formation {sgn(hf)}; {data}.'
    endo = sum(v for _, v in terms if v > 0)
    mt = SALTS[f][0]
    parts = [P_(f'Calculate the lattice energy of {F(f)}.', kj(le), f'sum of terms = {sgn(sum(v for _, v in terms))} [1]; LE = {sgn(hf)} − ({sgn(sum(v for _, v in terms))}) = {kj(le)} [1] [2]'),
             P_('Calculate the total energy needed for all the endothermic steps.', f'{sgn(endo)} kJ mol⁻¹', f'sum of positive terms = {sgn(endo)} [1]'),
             P_(f'Explain why the second ionisation energy of {NAME_M[mt]} is larger than the first.', 'The electron is removed from a positive ion with a greater effective attraction (less repulsion), so more energy is needed.', '[2]'),
             P_(f'Suggest, with a reason, how the lattice energy of {F(f)} would compare with that of a compound of a Group 1 metal with the same anion.', f'{F(f)} is much more exothermic because the {mt}²⁺ ion has a higher charge (and similar or smaller radius), giving stronger electrostatic attraction.', 'more exothermic [1]; higher charge / charge density [1] [2]'),
             P_('Explain why the overall formation of this compound is exothermic despite the large endothermic steps.', 'The lattice energy is very large and exothermic and outweighs the endothermic atomisation and ionisation steps.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how a Born–Haber cycle is constructed for magnesium chloride and explain how it is used to calculate the lattice energy.', 'Elements Mg(s) + Cl₂(g) at zero; ΔHf down to MgCl₂(s); upward steps: atomise Mg, IE1 and IE2 of Mg, atomise 2 Cl (2 × ½Cl₂), 2 × EA1 of Cl; lattice energy from Mg²⁺(g) + 2Cl⁻(g) to MgCl₂(s); Hess\'s law: ΔHf = Σ steps + LE; rearrange; sign conventions.',
           'species at each level [2]; correct multiples for Cl [1]; IE1 and IE2 [1]; lattice energy step [1]; Hess\'s law and rearrangement [2] [7]')])
t1b = t

# ---------------------------------------------------------------------
t = T('Effect of ionic charge and radius on lattice energy', 'effect of ionic charge and radius on lattice energy')
facts(t, [('ionic radius', 'the radius of an ion in an ionic crystal; cations are smaller and anions larger than their parent atoms'),
          ('charge density', 'the ratio of the charge of an ion to its size (volume); small, highly charged ions have high charge density'),
          ('polarisation', 'the distortion of the electron cloud of an anion by a neighbouring cation with high charge density')])
mcqs(t, [('Which compound has the most exothermic lattice energy?', 'MgO', 'Smallest ions with 2+ and 2− charges.', ['NaCl', 'KBr', 'CaO']),
         ('Why is the lattice energy of NaF more exothermic than that of NaCl?', 'F⁻ is smaller than Cl⁻, so the ions are closer and attract more strongly', 'Same charges; smaller radius.', ['F⁻ has a larger charge than Cl⁻', 'F has a higher electron affinity', 'NaF has more covalent character']),
         ('Lattice energy becomes less exothermic down Group 1 for the chlorides because', 'the cation radius increases so the attraction between ions decreases', 'Larger ions, greater separation.', ['the cation charge increases', 'the anion radius increases', 'the ionisation energy increases']),
         ('Which pair of factors leads to a very exothermic lattice energy?', 'High ionic charges and small ionic radii', 'Lattice energy ∝ charge product ÷ (sum of radii).', ['Low charges and small radii', 'High charges and large radii', 'Low charges and large radii'])])
shorts(t, [('State the two factors that affect the magnitude of lattice energy.', 'The charges on the ions and the sizes (radii) of the ions.', '[2]')])
explain(t, [('Explain why the lattice energy of MgO is much more exothermic than that of NaCl.', 'Mg²⁺ and O²⁻ have double charges (charge product 4 vs 1) and are smaller than Na⁺ and Cl⁻, so the ions are closer together and attract more strongly.', 'higher charges [1]; smaller ions [1]; stronger electrostatic attraction [1] [3]'),
            ('Explain why the lattice energies of the Group 2 oxides become less exothermic down the group.', 'The cation radius increases down the group (charge stays 2+), so the distance between ion centres increases and the electrostatic attraction decreases.', 'cation size increases [1]; same charge [1]; weaker attraction [1] [3]'),
            ('Explain why experimental lattice energies of silver halides are more exothermic than values calculated assuming purely ionic bonding.', 'Ag⁺ polarises the large halide ions, giving some covalent character, which adds to the bonding strength.', 'polarisation of anion [1]; covalent character increases bonding [1] [2]')])
myths(t, [('The larger the ions, the more exothermic the lattice energy.', 'Larger ions are further apart, so attraction is weaker and lattice energy is less exothermic.'),
          ('Charge has little effect on lattice energy compared with size.', 'Doubling both charges roughly quadruples the attraction; charge usually has the larger effect.')])

RADII = {'Li⁺': 76, 'Na⁺': 102, 'K⁺': 138, 'Rb⁺': 152, 'Mg²⁺': 72, 'Ca²⁺': 100, 'Sr²⁺': 118, 'Ba²⁺': 135, 'F⁻': 133, 'Cl⁻': 181, 'Br⁻': 196, 'I⁻': 220, 'O²⁻': 140}
CMP = [('LiF', 'Li⁺', 'F⁻'), ('NaF', 'Na⁺', 'F⁻'), ('KF', 'K⁺', 'F⁻'), ('NaCl', 'Na⁺', 'Cl⁻'), ('KCl', 'K⁺', 'Cl⁻'), ('NaBr', 'Na⁺', 'Br⁻'), ('KI', 'K⁺', 'I⁻'), ('RbCl', 'Rb⁺', 'Cl⁻'),
       ('MgO', 'Mg²⁺', 'O²⁻'), ('CaO', 'Ca²⁺', 'O²⁻'), ('SrO', 'Sr²⁺', 'O²⁻'), ('BaO', 'Ba²⁺', 'O²⁻'), ('NaI', 'Na⁺', 'I⁻'), ('LiCl', 'Li⁺', 'Cl⁻')]


def _q(i):
    return 2 if '²' in i else 1


def le_est(c, a):
    return _q(c) * _q(a) / (RADII[c] + RADII[a])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def le_compare(r, D):
    for _ in range(20):
        (f1, c1, a1), (f2, c2, a2) = r.sample(CMP, 2)
        e1, e2 = le_est(c1, a1), le_est(c2, a2)
        if abs(e1 - e2) / max(e1, e2) > 0.04:
            break
    else:
        return None
    big = f1 if e1 > e2 else f2
    if D <= 2:
        return MQ(r, f'Which of these compounds has the more exothermic lattice energy: {F(f1)} or {F(f2)}?', F(big), [F(f1 if big == f2 else f2), 'They have the same lattice energy', 'It cannot be predicted without a Born–Haber cycle'],
                  f'{F(big)}: ' + ('higher ionic charges' if _q(c1) * _q(a1) != _q(c2) * _q(a2) else 'smaller ions, closer together') + '.')
    rad = ', '.join(f'{i} {RADII[i]} pm' for i in dict.fromkeys([c1, a1, c2, a2]))
    why = ('the product of the ionic charges is larger' if _q(c1) * _q(a1) != _q(c2) * _q(a2) else 'the sum of the ionic radii is smaller, so the ions are closer')
    return Q(f'Ionic radii: {rad}. Predict which of {F(f1)} and {F(f2)} has the more exothermic lattice energy. Explain your answer.', f'{F(big)}: {why}, so the electrostatic attraction between the ions is stronger.',
             f'{F(big)} [1]; reference to charge and/or radius using the data [1]; stronger attraction [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def le_trend(r, D):
    grp = r.choice([['LiF', 'LiCl', 'NaCl', 'KCl', 'RbCl'], ['MgO', 'CaO', 'SrO', 'BaO'], ['NaF', 'NaCl', 'NaBr', 'NaI']])
    vals = {f: bh_terms(f)[1] for f in grp if f in SALTS}
    st = f'{who(r)} calculated the lattice energies (kJ mol⁻¹) of a series of compounds: ' + ', '.join(f'{F(f)} {sgn(v)}' for f, v in vals.items()) + '.'
    parts = [P_('Describe and explain the trend in lattice energy shown by the data.', 'Lattice energy becomes less exothermic along the series because the ionic radius of the varying ion increases, so the ions are further apart and the electrostatic attraction is weaker.', 'trend described with data [1]; increasing radius [1]; weaker attraction [1] [3]'),
             P_('Explain why the lattice energy of MgO (about −3800 kJ mol⁻¹) is about five times that of NaF (about −920 kJ mol⁻¹).', 'The charge product is 4 times larger (2+ × 2− vs 1+ × 1−) and Mg²⁺ and O²⁻ are about the same size as or smaller than Na⁺ and F⁻.', 'charge product ×4 [1]; similar / smaller radii [1] [2]'),
             P_('Suggest why the experimental lattice energy of a compound can differ from a theoretical value calculated from an ionic model.', 'Polarisation of the anion by the cation introduces covalent character, making the experimental value more exothermic.', '[2]'),
             P_('Predict, with a reason, how the melting points of these compounds would vary.', 'Melting point generally decreases along the series as lattice energy becomes less exothermic, because less energy is needed to separate the ions.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how the charge and size of ions affect lattice energy, using examples from Groups 1 and 2.', 'Lattice energy depends on electrostatic attraction ∝ charge product / distance between ion centres; higher charge → more exothermic (MgO vs NaF); smaller ions → more exothermic (LiF vs KF; MgO vs BaO); down a group cation radius increases so less exothermic; anion size also (NaF to NaI); polarisation and covalent character.',
           'electrostatic attraction principle [1]; charge effect with example [2]; radius effect with example [2]; trend down group [1]; polarisation [1] [7]')])
t1c = t

# ---------------------------------------------------------------------
HYD = {'Li⁺': -519, 'Na⁺': -406, 'K⁺': -322, 'Rb⁺': -301, 'Mg²⁺': -1926, 'Ca²⁺': -1579, 'Sr²⁺': -1446, 'Ba²⁺': -1309, 'F⁻': -506, 'Cl⁻': -364, 'Br⁻': -335, 'I⁻': -293, 'OH⁻': -460}
LEX = {'LiF': (-1049, 'Li⁺', 'F⁻', 1), 'LiCl': (-853, 'Li⁺', 'Cl⁻', 1), 'NaF': (-923, 'Na⁺', 'F⁻', 1), 'NaCl': (-787, 'Na⁺', 'Cl⁻', 1), 'NaBr': (-751, 'Na⁺', 'Br⁻', 1),
       'NaI': (-705, 'Na⁺', 'I⁻', 1), 'KF': (-821, 'K⁺', 'F⁻', 1), 'KCl': (-711, 'K⁺', 'Cl⁻', 1), 'KBr': (-679, 'K⁺', 'Br⁻', 1), 'KI': (-651, 'K⁺', 'I⁻', 1),
       'MgCl2': (-2526, 'Mg²⁺', 'Cl⁻', 2), 'CaCl2': (-2258, 'Ca²⁺', 'Cl⁻', 2), 'SrCl2': (-2156, 'Sr²⁺', 'Cl⁻', 2), 'BaCl2': (-2056, 'Ba²⁺', 'Cl⁻', 2), 'MgBr2': (-2440, 'Mg²⁺', 'Br⁻', 2)}

t = T('Enthalpies of solution and hydration; solubility and thermal stability trends of Group 2 compounds', 'enthalpies of solution and hydration')
facts(t, [('enthalpy change of hydration', 'the enthalpy change when 1 mole of gaseous ions dissolves in sufficient water to form an infinitely dilute solution'),
          ('enthalpy change of solution', 'the enthalpy change when 1 mole of an ionic solid dissolves in sufficient water to form an infinitely dilute solution'),
          ('thermal decomposition', 'the breakdown of a compound into simpler substances by heating, e.g. CaCO₃ → CaO + CO₂'),
          ('polarising power', 'the ability of a cation to distort the electron cloud of a neighbouring anion; greatest for small, highly charged cations')])
mcqs(t, [('Which ion has the most exothermic enthalpy change of hydration?', 'Mg²⁺', 'Small and doubly charged: strongest attraction for water molecules.', ['Ba²⁺', 'Na⁺', 'K⁺']),
         ('How does the thermal stability of the Group 2 carbonates change down the group?', 'It increases', 'Larger cations polarise the carbonate ion less.', ['It decreases', 'It stays the same', 'It increases then decreases']),
         ('How does the solubility of the Group 2 sulfates change down the group?', 'It decreases', 'Hydration enthalpy of the cation falls faster than lattice energy.', ['It increases', 'It stays the same', 'It increases then decreases']),
         ('How does the solubility of the Group 2 hydroxides change down the group?', 'It increases', 'Mg(OH)₂ sparingly soluble; Ba(OH)₂ quite soluble.', ['It decreases', 'It stays the same', 'It decreases then increases']),
         ('Which expression gives the enthalpy change of solution of NaCl?', 'ΔHsol = ΔHhyd(Na⁺) + ΔHhyd(Cl⁻) − ΔHlatt(NaCl)', 'Lattice broken (−LE) then ions hydrated.', ['ΔHsol = ΔHlatt + ΔHhyd(Na⁺) + ΔHhyd(Cl⁻)', 'ΔHsol = ΔHlatt − ΔHhyd(Na⁺) − ΔHhyd(Cl⁻)', 'ΔHsol = −ΔHlatt − ΔHhyd(Na⁺) − ΔHhyd(Cl⁻)'])])
shorts(t, [('Write an equation, with state symbols, for the enthalpy change of hydration of the calcium ion.', 'Ca²⁺(g) + aq → Ca²⁺(aq)', 'species [1]; state symbols [1] [2]'),
           ('Write an equation for the thermal decomposition of magnesium nitrate.', '2Mg(NO₃)₂ → 2MgO + 4NO₂ + O₂', 'correct products [1]; balanced [1] [2]')])
explain(t, [('Explain why hydration enthalpies become less exothermic down Group 2.', 'Ionic radius increases down the group (same 2+ charge), so the charge density decreases and the attraction between the ion and the lone pairs (δ−) on water molecules becomes weaker.', 'radius increases [1]; lower charge density [1]; weaker ion–dipole attraction [1] [3]'),
            ('Explain why the thermal stability of Group 2 carbonates increases down the group.', 'Cations get larger down the group, so their charge density and polarising power decrease; they distort the electron cloud of the carbonate ion less, so the C–O bonds are weakened less and more heat is needed to decompose the carbonate.', 'cation radius increases [1]; less polarisation of carbonate ion [1]; C–O bond weakened less [1] [3]'),
            ('Explain why the solubility of the Group 2 sulfates decreases down the group.', 'Both lattice energy and hydration enthalpy become less exothermic, but the hydration enthalpy of the cation decreases more (the large sulfate ion dominates the lattice distance), so ΔHsol becomes more endothermic and solubility falls.', 'both decrease [1]; hydration enthalpy falls more [1]; ΔHsol more endothermic [1] [3]'),
            ('Explain why water molecules are arranged differently around cations and anions in solution.', 'Around cations the δ− oxygen atoms point towards the ion; around anions the δ+ hydrogen atoms point towards the ion (ion–dipole attraction).', 'O towards cation [1]; H towards anion [1] [2]')])
myths(t, [('A compound with an endothermic enthalpy change of solution cannot dissolve in water.', 'Many compounds with endothermic ΔHsol (e.g. NaCl, NH₄NO₃) dissolve because the entropy increase makes ΔG negative.'),
          ('Barium carbonate decomposes more easily than magnesium carbonate because barium is more reactive.', 'BaCO₃ is more thermally stable: the large Ba²⁺ ion polarises the carbonate ion less.'),
          ('Hydration enthalpies are endothermic because bonds to water must be broken.', 'Hydration is exothermic: ion–dipole attractions form between the gaseous ion and water molecules.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def solution_h(r, D):
    f = r.choice(list(LEX))
    le, c, a, n = LEX[f]
    hc, ha = HYD[c], HYD[a]
    hs = -le + hc + n * ha
    mode = r.choice(['sol', 'sol', 'hyd']) if D >= 3 else 'sol'
    if mode == 'sol':
        st = f'The lattice energy of {F(f)} is {sgn(le)} kJ mol⁻¹. The enthalpy changes of hydration are: {c} {sgn(hc)} kJ mol⁻¹; {a} {sgn(ha)} kJ mol⁻¹. Calculate the enthalpy change of solution of {F(f)}.'
        key = f'ΔHsol = −ΔHlatt + ΣΔHhyd [1]; = +{-le} + ({sgn(hc)}) + {n if n > 1 else ""}{"× " if n > 1 else ""}({sgn(ha)}) [1] = {kj(hs)} [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate', 'What is'), hs, [le + hc + n * ha, -hs, -le + hc + ha if n > 1 else -le - hc - ha, hs + 100], ' kJ mol⁻¹', key, f=lambda v: sgn(v))
        if D >= 4:
            st += ' Suggest, with a reason, whether the compound is likely to be soluble in water.'
            key = key.replace(' [3]', '') + '; comment linking sign/size of ΔHsol (and entropy) to solubility [1] [4]'
            return Q(st, f'{kj(hs)}; ' + ('exothermic, so likely to be soluble' if hs < 0 else 'only slightly endothermic, so it can still dissolve because entropy increases' if hs < 40 else 'quite endothermic, so solubility may be limited'), key, 'numerical')
        return Q(st, kj(hs), key, 'numerical')
    st = f'For {F(f)}, the lattice energy is {sgn(le)} kJ mol⁻¹ and the enthalpy change of solution is {sgn(hs)} kJ mol⁻¹. The enthalpy change of hydration of {a} is {sgn(ha)} kJ mol⁻¹. Calculate the enthalpy change of hydration of {c}.'
    key = f'ΔHsol = −ΔHlatt + ΔHhyd(cation) + {n} × ΔHhyd(anion) [1]; ΔHhyd({c}) = {sgn(hs)} − {-le} − {n} × ({sgn(ha)}) [1] = {kj(hc)} [1] [3]'
    return Q(st, kj(hc), key, 'numerical')


G2 = [('magnesium carbonate', 'MgCO₃ → MgO + CO₂', 'the smallest Group 2 cation, Mg²⁺, has the highest charge density and polarises the carbonate ion most'),
      ('barium carbonate', 'BaCO₃ → BaO + CO₂', 'the large Ba²⁺ ion has a low charge density and polarises the carbonate ion least'),
      ('calcium nitrate', '2Ca(NO₃)₂ → 2CaO + 4NO₂ + O₂', 'Ca²⁺ is intermediate in size, so its nitrate decomposes at an intermediate temperature'),
      ('strontium carbonate', 'SrCO₃ → SrO + CO₂', 'Sr²⁺ is larger than Ca²⁺ so polarises the carbonate ion less; a higher temperature is needed')]


@t.add('C3', (1, 2, 3, 4), 'short')
def g2_trend(r, D):
    pair = r.sample(['Mg', 'Ca', 'Sr', 'Ba'], 2)
    order = ['Mg', 'Ca', 'Sr', 'Ba']
    lo, hi = sorted(pair, key=order.index)
    kind = r.choice(['carbonate', 'nitrate', 'sulfate', 'hydroxide'])
    nm = {'Mg': 'magnesium', 'Ca': 'calcium', 'Sr': 'strontium', 'Ba': 'barium'}
    if kind in ('carbonate', 'nitrate'):
        q = f'Which decomposes at the lower temperature: {nm[lo]} {kind} or {nm[hi]} {kind}?'
        ans = f'{cap(nm[lo])} {kind}'
        why = f'{lo}²⁺ is smaller with a higher charge density, so it polarises the {kind} ion more, weakening its bonds.'
    elif kind == 'sulfate':
        q = f'Which is more soluble in water: {nm[lo]} sulfate or {nm[hi]} sulfate?'
        ans = f'{cap(nm[lo])} sulfate'
        why = 'Sulfate solubility decreases down the group because the hydration enthalpy of the cation becomes much less exothermic.'
    else:
        q = f'Which is more soluble in water: {nm[lo]} hydroxide or {nm[hi]} hydroxide?'
        ans = f'{cap(nm[hi])} hydroxide'
        why = 'Hydroxide solubility increases down the group (lattice energy falls faster than hydration enthalpy for the small OH⁻ ion).'
    if D <= 2:
        other = f'{cap(nm[hi])} {kind}' if ans.startswith(cap(nm[lo])) else f'{cap(nm[lo])} {kind}'
        return MQ(r, q, ans, [other, 'Both are the same', 'It depends only on the mass of the sample'], why)
    return Q(q + ' Explain your answer.', f'{ans}. {why}', 'correct choice [1]; explanation in terms of ionic radius / charge density [1]; polarisation or hydration/lattice argument [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def g2_case(r, D):
    carb = r.choice(['MgCO3', 'CaCO3', 'SrCO3', 'BaCO3'])
    mass = round(r.uniform(1.5, 5.0), 2)
    mr_ = Mr(carb)
    mo = carb.replace('CO3', 'O')
    loss = mass * 44.0 / mr_
    st = f'{who(r)} heated {fx(mass, 2)} g of {F(carb)} strongly to constant mass in {lab(r)}.'
    parts = [P_('Write an equation for the reaction.', f'{F(carb)} → {F(mo)} + CO₂', '[1]'),
             P_('Calculate the expected loss in mass.', f'{g3(loss)} g', f'moles = {fx(mass, 2)} ÷ {fx(mr_, 1)} = {g3(mass / mr_)} [1]; × 44.0 = {g3(loss)} g [1] [2]'),
             P_('Explain the trend in thermal stability of the Group 2 carbonates.', 'Stability increases down the group: cation radius increases so charge density and polarising power decrease; the carbonate ion is distorted less, so C–O bonds are weakened less.', 'trend [1]; cation size / charge density [1]; polarisation of carbonate [1] [3]'),
             P_('Explain why heating to constant mass is necessary.', 'To ensure that decomposition is complete, so all CO₂ has been lost.', '[1]'),
             P_('Suggest why a Bunsen burner may not decompose barium carbonate completely.', 'BaCO₃ is very thermally stable and needs a temperature higher than a Bunsen flame can provide.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how enthalpy changes of hydration and lattice energy determine the enthalpy change of solution, and use these ideas to explain the solubility trends of Group 2 sulfates and hydroxides.', 'ΔHsol = −LE + ΣΔHhyd; hydration: ion–dipole attraction, more exothermic for small/high charge ions; lattice energy; sulfates: large anion so lattice energy changes little down group while hydration enthalpy of cation falls a lot → ΔHsol more endothermic → less soluble; hydroxides: small anion so lattice energy falls faster → more soluble; entropy also involved.',
           'cycle / equation [2]; factors affecting hydration [1]; sulfate trend explained [2]; hydroxide trend explained [1]; entropy / ΔG mention [1] [7]')])
t1d = t

CHAPTERS[1] = [t1a, t1b, t1c, t1d]


# ===================================================================== 2 Electrochemistry
ELYS = [  # electrolyte, product, electrode, electrons per mole of product, molar mass, gas?
    ('aqueous copper(II) sulfate', 'copper', 'cathode', 2, 63.5, False, 'Cu²⁺ + 2e⁻ → Cu'),
    ('aqueous silver nitrate', 'silver', 'cathode', 1, 107.9, False, 'Ag⁺ + e⁻ → Ag'),
    ('molten sodium chloride', 'sodium', 'cathode', 1, 23.0, False, 'Na⁺ + e⁻ → Na'),
    ('molten aluminium oxide (in cryolite)', 'aluminium', 'cathode', 3, 27.0, False, 'Al³⁺ + 3e⁻ → Al'),
    ('dilute sulfuric acid', 'hydrogen', 'cathode', 2, 2.0, True, '2H⁺ + 2e⁻ → H₂'),
    ('dilute sulfuric acid', 'oxygen', 'anode', 4, 32.0, True, '2H₂O → O₂ + 4H⁺ + 4e⁻'),
    ('concentrated aqueous sodium chloride', 'chlorine', 'anode', 2, 71.0, True, '2Cl⁻ → Cl₂ + 2e⁻'),
    ('aqueous nickel(II) sulfate', 'nickel', 'cathode', 2, 58.7, False, 'Ni²⁺ + 2e⁻ → Ni'),
    ('aqueous zinc sulfate', 'zinc', 'cathode', 2, 65.4, False, 'Zn²⁺ + 2e⁻ → Zn')]

t = T('Electrolysis: Faraday\'s laws, F = Le and calculating mass and volume of products', 'electrolysis: faraday\'s laws')
facts(t, [('Faraday constant', 'the charge carried by one mole of electrons, about 96 500 C mol⁻¹ (F = Le)'),
          ('electrolysis', 'the decomposition of a compound, molten or in aqueous solution, by passing an electric current through it'),
          ('coulomb', 'the unit of electric charge; the charge passing when a current of 1 A flows for 1 s (Q = It)'),
          ('Avogadro constant', 'the number of particles in one mole, 6.02 × 10²³ mol⁻¹'),
          ('electroplating', 'the coating of an object with a thin layer of metal by making it the cathode in an electrolysis cell')])
mcqs(t, [('Which expression links the Faraday constant, the Avogadro constant and the charge on an electron?', 'F = Le', 'Charge of one mole of electrons.', ['L = Fe', 'e = FL', 'F = L ÷ e']),
         ('How many faradays are needed to deposit 1 mol of copper from Cu²⁺ ions?', '2', 'Cu²⁺ + 2e⁻ → Cu.', ['1', '0.5', '4']),
         ('A current of 2.0 A flows for 10 minutes. What charge passes?', '1200 C', 'Q = It = 2.0 × 600.', ['20 C', '120 C', '12 000 C']),
         ('Which product is formed at the anode in the electrolysis of dilute sulfuric acid?', 'Oxygen', '4OH⁻ / 2H₂O lose electrons.', ['Hydrogen', 'Sulfur dioxide', 'Sulfur']),
         ('What volume of hydrogen at r.t.p. is produced by 1 faraday of charge?', '12.0 dm³', '2 F per mole of H₂ (24.0 dm³), so 1 F gives 0.5 mol.', ['24.0 dm³', '6.0 dm³', '48.0 dm³'])])
shorts(t, [('State the relationship between charge, current and time.', 'Q = It (charge in coulombs = current in amperes × time in seconds).', '[1]'),
           ('Describe how the Avogadro constant could be determined by electrolysis of copper(II) sulfate with copper electrodes.', 'Pass a measured current for a measured time; weigh the cathode before and after; moles Cu = mass ÷ 63.5; moles electrons = 2 × moles Cu; L = (Q ÷ e) ÷ moles electrons.', 'measure I and t [1]; mass change of cathode [1]; calculation route [1] [3]')])
explain(t, [('Explain why twice as much charge is needed to deposit one mole of copper as one mole of silver.', 'Copper is deposited from Cu²⁺, which needs 2 electrons per atom; silver from Ag⁺, which needs 1 electron per atom; so 2 F vs 1 F per mole.', 'Cu²⁺ needs 2e⁻ [1]; Ag⁺ needs 1e⁻ [1] [2]'),
            ('Explain why the mass of the anode decreases when copper(II) sulfate solution is electrolysed using copper electrodes.', 'Copper atoms of the anode are oxidised to Cu²⁺ ions (Cu → Cu²⁺ + 2e⁻), which go into solution.', 'anode oxidised [1]; half-equation [1] [2]'),
            ('Explain why the volume of oxygen produced in the electrolysis of dilute sulfuric acid is half the volume of hydrogen.', 'Four electrons are released per O₂ formed but only two are needed per H₂; the same charge passes at each electrode so moles of O₂ = half moles of H₂.', 'electrons per molecule [1]; same charge at each electrode [1] [2]')])
myths(t, [('The mass of product formed in electrolysis depends only on the current.', 'It depends on the total charge (current × time) and on the number of electrons needed per ion (charge on the ion).'),
          ('One faraday deposits one mole of any metal.', 'One faraday deposits one mole of a metal only if its ion has a 1+ charge; for M²⁺ it deposits 0.5 mol.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def faraday_calc(r, D):
    ely, prod, el, n, M, gas, half = r.choice(ELYS)
    I = r.choice([0.25, 0.40, 0.50, 0.80, 1.20, 1.50, 2.00, 2.50, 3.00])
    tmin = r.choice([10, 15, 20, 25, 30, 40, 45, 60, 90])
    Qc = I * tmin * 60
    mol_e = Qc / FARADAY
    mol_p = mol_e / n
    mass = mol_p * M
    vol = mol_p * 24.0
    mode = r.choice(['mass', 'mass', 'time', 'current']) if D >= 4 else 'mass'
    if mode == 'mass':
        what = (f'volume of {prod} at room temperature and pressure (24.0 dm³ mol⁻¹)' if gas else f'mass of {prod} deposited')
        ans = f'{g3(vol * 1000)} cm³' if gas else f'{g3(mass)} g'
        st = f'A current of {fx(I, 2)} A is passed through {ely} for {tmin} minutes. Calculate the {what} at the {el}. [F = 96 500 C mol⁻¹]'
        key = f'Q = {fx(I, 2)} × {tmin * 60} = {fx(Qc, 0)} C [1]; mol e⁻ = {fx(Qc, 0)} ÷ 96 500 = {g3(mol_e)} [1]; {half}: mol {prod} = {g3(mol_e)} ÷ {n} = {g3(mol_p)} [1]; ' + (f'× 24 000 = {g3(vol * 1000)} cm³ [1] [4]' if gas else f'× {M} = {g3(mass)} g [1] [4]')
        if D <= 2:
            v = vol * 1000 if gas else mass
            return NQ(r, st.replace('Calculate the', 'What is the'), v, [v * n, v / n * (n - 1) if n > 1 else v * 2, v * 60, v * 2.5], ' cm³' if gas else ' g', key)
        return Q(st, ans, key, 'numerical')
    if mode == 'time':
        tgt = round(mass if not gas else vol * 1000, 2 if not gas else 0)
        if tgt <= 0:
            return None
        tt = tgt / (M if not gas else 24000) * n * FARADAY / I
        st = f'Calculate the time, in minutes, needed to produce {fx(tgt, 2 if not gas else 0)} {"cm³ (at r.t.p.)" if gas else "g"} of {prod} by electrolysis of {ely} using a current of {fx(I, 2)} A. [F = 96 500 C mol⁻¹]'
        return Q(st, f'{g3(tt / 60)} min', f'mol {prod} = {g3(tgt / (M if not gas else 24000))} [1]; mol e⁻ = × {n} [1]; Q = mol e⁻ × 96 500 = {g3(tt * I)} C [1]; t = Q ÷ I = {g3(tt)} s = {g3(tt / 60)} min [1] [4]', 'numerical')
    tgt = round(mass, 3) if not gas else round(vol * 1000)
    st = f'In the electrolysis of {ely}, {fx(tgt, 3) if not gas else tgt} {"g" if not gas else "cm³ (at r.t.p.)"} of {prod} was produced in {tmin} minutes. Calculate the current used. [F = 96 500 C mol⁻¹]'
    Ic = (tgt / (M if not gas else 24000)) * n * FARADAY / (tmin * 60)
    return Q(st, f'{g3(Ic)} A', f'mol {prod} = {g3(tgt / (M if not gas else 24000))} [1]; mol e⁻ × {n} [1]; Q = {g3(Ic * tmin * 60)} C [1]; I = Q ÷ t = {g3(Ic)} A [1] [4]', 'numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def avogadro(r, D):
    I = r.choice([0.20, 0.30, 0.40, 0.50])
    tmin = r.choice([20, 30, 40, 50, 60])
    Lt = r.uniform(5.9e23, 6.2e23)
    e = 1.60e-19
    Qc = I * tmin * 60
    mass = Qc / e / Lt / 2 * 63.5
    mass = round(mass, 3)
    L = Qc / e / (mass / 63.5 * 2)
    st = (f'{who(r)} electrolysed copper(II) sulfate solution using copper electrodes and a constant current of {fx(I, 2)} A for {tmin} minutes. The cathode gained {fx(mass, 3)} g. '
          f'The charge on an electron is 1.60 × 10⁻¹⁹ C.')
    parts = [P_('Calculate the number of electrons that passed through the circuit.', sci(Qc / e, 3), f'Q = {fx(I, 2)} × {tmin * 60} = {fx(Qc, 0)} C [1]; ÷ 1.60 × 10⁻¹⁹ = {sci(Qc / e, 3)} [1] [2]'),
             P_('Calculate a value for the Avogadro constant from these results.', f'{sci(L, 3)} mol⁻¹', f'mol Cu = {fx(mass, 3)} ÷ 63.5 = {g3(mass / 63.5)} [1]; mol e⁻ = 2 × that = {g3(2 * mass / 63.5)} [1]; L = {sci(Qc / e, 3)} ÷ {g3(2 * mass / 63.5)} = {sci(L, 3)} [1] [3]'),
             P_('Write the half-equation for the reaction at the cathode.', 'Cu²⁺(aq) + 2e⁻ → Cu(s)', '[1]'),
             P_('Suggest why the cathode should be washed with propanone and dried before reweighing.', 'To remove the solution so the mass measured is copper only; propanone evaporates quickly at low temperature without oxidising the copper.', '[2]')]
    return case(r, st, parts, k=(2, 3), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def plating_case(r, D):
    met, ion, n, M = r.choice([('silver', 'Ag⁺', 1, 107.9), ('nickel', 'Ni²⁺', 2, 58.7), ('copper', 'Cu²⁺', 2, 63.5), ('chromium', 'Cr³⁺', 3, 52.0)])
    area = r.choice([50, 80, 120, 200])
    thick = r.choice([5, 10, 20, 25])  # μm
    dens = {'silver': 10.5, 'nickel': 8.9, 'copper': 8.96, 'chromium': 7.19}[met]
    vol = area * thick * 1e-4
    mass = vol * dens
    I = r.choice([0.5, 1.0, 1.5, 2.0])
    tt = mass / M * n * FARADAY / I
    st = f'A workshop in {city(r)} electroplates a metal object of surface area {area} cm² with a layer of {met} {thick} μm thick, using a solution containing {ion} ions and a current of {fx(I, 1)} A. The density of {met} is {dens} g cm⁻³.'
    parts = [P_(f'Calculate the mass of {met} needed.', f'{g3(mass)} g', f'volume = {area} × {thick} × 10⁻⁴ = {g3(vol)} cm³ [1]; mass = × {dens} = {g3(mass)} g [1] [2]'),
             P_('Calculate the time needed, in minutes.', f'{g3(tt / 60)} min', f'mol = {g3(mass / M)} [1]; mol e⁻ = × {n} = {g3(mass / M * n)} [1]; t = mol e⁻ × 96 500 ÷ {fx(I, 1)} = {g3(tt)} s = {g3(tt / 60)} min [1] [3]'),
             P_('State which electrode the object must be and write the half-equation for the reaction there.', f'Cathode: {ion} + {n if n > 1 else ""}e⁻ → {met.capitalize()[:2] if met in ("silver", "nickel", "chromium", "copper") and False else {"silver": "Ag", "nickel": "Ni", "copper": "Cu", "chromium": "Cr"}[met]}', 'cathode [1]; half-equation [1] [2]'),
             P_('Suggest why the actual time needed is longer than calculated.', 'Some current is used in side reactions such as hydrogen production at the cathode (current efficiency less than 100%).', '[1]'),
             P_(f'Explain why the anode is often made of {met}.', f'The {met} anode is oxidised to {ion} ions, replacing those removed from solution, so the concentration stays constant.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how you would determine a value for the Avogadro constant by electrolysis, and explain the calculation.', 'Copper electrodes in CuSO₄(aq); clean, dry, weigh cathode; series circuit with ammeter and variable resistor; constant current for measured time; remove, wash with water then propanone, dry, reweigh; Q = It; mol Cu = Δm ÷ 63.5; mol e⁻ = 2 × mol Cu; number of electrons = Q ÷ e; L = number of electrons ÷ mol e⁻; sources of error.',
           'apparatus [1]; measurements [2]; Q = It [1]; mol e⁻ from mass [1]; L calculation [1]; error / improvement [1] [7]')])
t2a = t

# ---------------------------------------------------------------------
HC = {  # key: (oxidised form, reduced form, electrons, E°, text half-equation)
    'Mg': ('Mg²⁺', 'Mg', 2, -2.38, 'Mg²⁺(aq) + 2e⁻ ⇌ Mg(s)'), 'Al': ('Al³⁺', 'Al', 3, -1.66, 'Al³⁺(aq) + 3e⁻ ⇌ Al(s)'), 'Zn': ('Zn²⁺', 'Zn', 2, -0.76, 'Zn²⁺(aq) + 2e⁻ ⇌ Zn(s)'),
    'Cr': ('Cr³⁺', 'Cr', 3, -0.74, 'Cr³⁺(aq) + 3e⁻ ⇌ Cr(s)'), 'Fe': ('Fe²⁺', 'Fe', 2, -0.44, 'Fe²⁺(aq) + 2e⁻ ⇌ Fe(s)'), 'Ni': ('Ni²⁺', 'Ni', 2, -0.25, 'Ni²⁺(aq) + 2e⁻ ⇌ Ni(s)'),
    'Sn': ('Sn²⁺', 'Sn', 2, -0.14, 'Sn²⁺(aq) + 2e⁻ ⇌ Sn(s)'), 'Pb': ('Pb²⁺', 'Pb', 2, -0.13, 'Pb²⁺(aq) + 2e⁻ ⇌ Pb(s)'), 'H': ('2H⁺', 'H₂', 2, 0.00, '2H⁺(aq) + 2e⁻ ⇌ H₂(g)'),
    'Cu': ('Cu²⁺', 'Cu', 2, 0.34, 'Cu²⁺(aq) + 2e⁻ ⇌ Cu(s)'), 'I': ('I₂', '2I⁻', 2, 0.54, 'I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)'), 'Fe3': ('Fe³⁺', 'Fe²⁺', 1, 0.77, 'Fe³⁺(aq) + e⁻ ⇌ Fe²⁺(aq)'),
    'Ag': ('Ag⁺', 'Ag', 1, 0.80, 'Ag⁺(aq) + e⁻ ⇌ Ag(s)'), 'Br': ('Br₂', '2Br⁻', 2, 1.07, 'Br₂(aq) + 2e⁻ ⇌ 2Br⁻(aq)'), 'Cl': ('Cl₂', '2Cl⁻', 2, 1.36, 'Cl₂(aq) + 2e⁻ ⇌ 2Cl⁻(aq)')}
METALS_HC = ['Mg', 'Al', 'Zn', 'Cr', 'Fe', 'Ni', 'Sn', 'Pb', 'Cu', 'Ag']


def _mul(sp, k):
    """Multiply a species string with an optional leading coefficient by k."""
    if k == 1:
        return sp
    c = 1
    s = sp
    if sp[0].isdigit():
        c = int(sp[0])
        s = sp[1:]
    return f'{c * k}{s}'


def overall(ox_key, red_key):
    """Species reduced from half-cell red_key (more positive) and oxidised from ox_key. Returns equation string."""
    o1, r1, n1, _, _ = HC[red_key]   # gets reduced: o1 + n1 e → r1
    o2, r2, n2, _, _ = HC[ox_key]    # gets oxidised: r2 → o2 + n2 e
    l = n1 * n2 // math.gcd(n1, n2)
    a, b = l // n1, l // n2
    return f'{_mul(o1, a)} + {_mul(r2, b)} → {_mul(r1, a)} + {_mul(o2, b)}'


t = T('Standard electrode potentials and the standard hydrogen electrode; standard cell potentials', 'standard electrode potentials')
facts(t, [('standard electrode potential', 'the potential difference between a half-cell and the standard hydrogen electrode under standard conditions (298 K, 101 kPa, 1.00 mol dm⁻³ ions)'),
          ('standard hydrogen electrode', 'a platinum electrode coated in platinum black, in contact with H₂ gas at 101 kPa and 1.00 mol dm⁻³ H⁺ ions at 298 K, assigned E° = 0.00 V'),
          ('standard cell potential', 'the potential difference between two half-cells under standard conditions, E°cell = E°(positive electrode) − E°(negative electrode)'),
          ('salt bridge', 'a strip of filter paper soaked in saturated KNO₃(aq) that completes the circuit by allowing ions to move between half-cells without mixing the solutions'),
          ('half-cell', 'an element in contact with a solution of its ions, or two ions of the same element in solution with an inert platinum electrode')])
mcqs(t, [('Why is platinum used as the electrode in the standard hydrogen electrode?', 'It is inert and conducts electricity', 'It provides a surface for H₂/H⁺ equilibrium without reacting.', ['It is a good reducing agent', 'It reacts with hydrogen', 'It has an E° of 0.00 V']),
         ('Why is potassium nitrate used in a salt bridge rather than potassium chloride?', 'Chloride ions could react with some ions in the half-cells, e.g. forming AgCl precipitate', 'Nitrates are all soluble and unreactive.', ['KNO₃ conducts electrons', 'KCl is insoluble', 'KNO₃ has a higher E°']),
         ('What are the standard conditions for measuring electrode potentials?', '298 K, 101 kPa and 1.00 mol dm⁻³ concentrations', 'Standard conditions.', ['273 K, 101 kPa and 1.00 mol dm⁻³', '298 K, 100 kPa and 0.10 mol dm⁻³', '373 K, 101 kPa and 1.00 mol dm⁻³']),
         ('Which half-cell needs a platinum electrode?', 'Fe³⁺(aq)/Fe²⁺(aq)', 'No solid metal in the equilibrium.', ['Cu²⁺(aq)/Cu(s)', 'Zn²⁺(aq)/Zn(s)', 'Ag⁺(aq)/Ag(s)']),
         ('A high-resistance voltmeter is used to measure cell potentials because', 'it draws very little current so the potential difference is not reduced', 'Measures maximum p.d. (e.m.f.).', ['it increases the current', 'it reacts with the electrodes', 'it reverses the cell reaction'])])
shorts(t, [('Draw or describe a cell that could be used to measure the standard electrode potential of the Cu²⁺/Cu half-cell.', 'Cu electrode in 1.00 mol dm⁻³ Cu²⁺(aq) connected by a salt bridge (KNO₃) and a high-resistance voltmeter to a standard hydrogen electrode (Pt, H₂ at 101 kPa, 1.00 mol dm⁻³ H⁺, 298 K).', 'Cu/Cu²⁺ half-cell [1]; SHE details [1]; salt bridge and voltmeter [1] [3]')])
explain(t, [('Explain why a salt bridge is needed in an electrochemical cell.', 'It completes the circuit by allowing ions to flow between the half-cells, maintaining electrical neutrality, without allowing the solutions to mix.', 'completes circuit / ion movement [1]; solutions do not mix [1] [2]'),
            ('Explain what the sign of a standard electrode potential shows about a half-cell.', 'A more positive E° means the oxidised form is more easily reduced (better oxidising agent) relative to H⁺/H₂; a more negative E° means the reduced form is more easily oxidised (better reducing agent).', 'positive: oxidised form easily reduced [1]; negative: reduced form easily oxidised [1] [2]'),
            ('Explain why the standard hydrogen electrode is rarely used in practice and what is used instead.', 'H₂ gas is flammable and difficult to keep at 101 kPa; platinum black is easily poisoned; a secondary standard (e.g. a calomel or Ag/AgCl reference electrode) of known E° is used.', 'practical difficulties [1]; secondary reference electrode [1] [2]')])
myths(t, [('Electrons flow through the salt bridge.', 'Electrons flow through the external wire; ions move through the salt bridge.'),
          ('E°cell = E°(negative electrode) − E°(positive electrode).', 'E°cell = E°(positive, more positive half-cell) − E°(negative half-cell), which gives a positive value.'),
          ('Doubling the half-equation doubles the electrode potential.', 'E° is an intensive property; multiplying a half-equation does not change E°.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ecell(r, D):
    a, b = r.sample(list(HC), 2)
    if HC[a][3] == HC[b][3]:
        return None
    pos, neg = (a, b) if HC[a][3] > HC[b][3] else (b, a)
    E = HC[pos][3] - HC[neg][3]
    st = f'A cell is made from the half-cells {HC[a][4]} (E° = {m(f"{HC[a][3]:+.2f}")} V) and {HC[b][4]} (E° = {m(f"{HC[b][3]:+.2f}")} V).'
    eq = overall(neg, pos)
    if D == 1:
        return NQ(r, st + ' What is the standard cell potential?', E, [HC[a][3] + HC[b][3], abs(HC[a][3]) + abs(HC[b][3]) if E != abs(HC[a][3]) + abs(HC[b][3]) else E + 0.5, E / 2, -E], ' V',
                  f'E°cell = {m(f"{HC[pos][3]:+.2f}")} − ({m(f"{HC[neg][3]:+.2f}")}) = {fx(E, 2)} V.', f=lambda v: m(f'{v:.2f}'))
    parts = [P_('Calculate the standard cell potential.', f'+{E:.2f} V', f'E°cell = E°(positive) − E°(negative) [1] = {m(f"{HC[pos][3]:+.2f}")} − ({m(f"{HC[neg][3]:+.2f}")}) = +{E:.2f} V [1] [2]'),
             P_('Identify the positive electrode and state the direction of electron flow in the external circuit.', f'The {HC[pos][0]}/{HC[pos][1]} half-cell is positive; electrons flow from the {HC[neg][0]}/{HC[neg][1]} half-cell to the {HC[pos][0]}/{HC[pos][1]} half-cell.', 'positive electrode [1]; direction [1] [2]'),
             P_('Write the overall equation for the cell reaction.', eq, 'correct species [1]; balanced electrons [1] [2]'),
             P_('State the conditions under which this cell potential would be measured.', '298 K; 1.00 mol dm⁻³ solutions; 101 kPa for any gas; high-resistance voltmeter; salt bridge.', 'any two conditions [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def she_case(r, D):
    mt = r.choice(['Zn', 'Cu', 'Ni', 'Fe', 'Pb', 'Ag', 'Mg'])
    E = HC[mt][3]
    st = f'{who(r)} measured the standard electrode potential of the {HC[mt][0]}/{HC[mt][1]} half-cell using a standard hydrogen electrode. The voltmeter read {abs(E):.2f} V and the {"metal" if E < 0 else "hydrogen electrode"} was the negative terminal.'
    parts = [P_('State the standard electrode potential of the half-cell, with its sign.', f'{m(f"{E:+.2f}")} V', '[1]'),
             P_('Describe the standard hydrogen electrode.', 'Platinum electrode coated with platinum black, dipping into 1.00 mol dm⁻³ H⁺(aq) (e.g. HCl), with H₂ gas bubbled over it at 101 kPa, at 298 K.', 'Pt electrode [1]; 1.00 mol dm⁻³ H⁺ [1]; H₂ at 101 kPa, 298 K [1] [3]'),
             P_('Explain why the concentration of the metal ion solution must be 1.00 mol dm⁻³.', 'The electrode potential depends on concentration (position of the equilibrium); standard values allow comparison.', '[2]'),
             P_('Explain the function of the salt bridge and why it contains KNO₃.', 'Allows ions to move to complete the circuit without mixing the solutions; KNO₃ ions do not react with or precipitate the ions in the half-cells.', 'function [1]; reason for KNO₃ [1] [2]'),
             P_('Write the half-equation for the reaction that happens in the metal half-cell when the cell delivers a current.', (f'{HC[mt][1]} → {HC[mt][0]} + {HC[mt][2] if HC[mt][2] > 1 else ""}e⁻' if E < 0 else f'{HC[mt][0]} + {HC[mt][2] if HC[mt][2] > 1 else ""}e⁻ → {HC[mt][1]}'), '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the standard hydrogen electrode and explain how it is used to measure the standard electrode potential of a metal/metal-ion half-cell.', 'SHE: Pt (platinum black), 1.00 mol dm⁻³ H⁺, H₂ at 101 kPa, 298 K, E° = 0.00 V; connect to metal in 1.00 mol dm⁻³ of its ions; salt bridge of KNO₃(aq); high-resistance voltmeter; reading = E° with sign from polarity; standard conditions; secondary standards.',
           'SHE details [2]; metal half-cell [1]; salt bridge [1]; voltmeter [1]; sign convention [1]; standard conditions [1] [7]')])
t2b = t

# ---------------------------------------------------------------------
t = T('Using E° values to predict the feasibility of reactions and the direction of electron flow', 'using e° values to predict the feasibility')
facts(t, [('feasible reaction', 'a reaction that is energetically possible under standard conditions, shown by a positive E°cell'),
          ('oxidising agent', 'a species that accepts electrons and is itself reduced; stronger oxidising agents have more positive E°'),
          ('reducing agent', 'a species that donates electrons and is itself oxidised; stronger reducing agents are in half-cells with more negative E°')])
mcqs(t, [('Which is the strongest oxidising agent?', 'Cl₂', 'Most positive E° (+1.36 V) among these.', ['Br₂', 'I₂', 'Fe³⁺']),
         ('Which is the strongest reducing agent?', 'Mg', 'Most negative E° (−2.38 V).', ['Zn', 'Fe', 'Cu']),
         ('A reaction has a positive E°cell but no reaction is seen. What is the most likely reason?', 'The activation energy is high so the reaction is very slow', 'E° says nothing about rate.', ['The reaction is not feasible', 'The E° values are wrong', 'The reaction is endothermic']),
         ('Using E° values, which reaction is feasible?', 'Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂', 'E°cell = 1.36 − 1.07 = +0.29 V.', ['I₂ + 2Br⁻ → 2I⁻ + Br₂', 'Cu²⁺ + 2Ag → Cu + 2Ag⁺', 'Zn²⁺ + Cu → Zn + Cu²⁺'])])
shorts(t, [('State two reasons why a reaction predicted to be feasible by E° values may not be observed.', 'High activation energy (slow rate); non-standard conditions (concentrations, temperature) change E values.', '[2]')])
explain(t, [('Explain how E° values are used to decide whether a reaction is feasible.', 'Identify the species reduced and oxidised; E°cell = E°(reduction half) − E°(oxidation half); if E°cell is positive the reaction is feasible.', 'identify half-equations [1]; E°cell calculation [1]; positive → feasible [1] [3]'),
            ('Explain why acidified potassium manganate(VII) can oxidise chloride ions but acidified potassium dichromate(VI) barely can.', 'E°(MnO₄⁻/Mn²⁺) = +1.52 V is more positive than E°(Cl₂/Cl⁻) = +1.36 V, so E°cell is +0.16 V; for dichromate +1.33 V is slightly less than +1.36 V, so E°cell is −0.03 V (not feasible under standard conditions).', 'MnO₄⁻ comparison [1]; Cr₂O₇²⁻ comparison [1]; sign of E°cell [1] [3]'),
            ('Explain why iron(II) salts are slowly oxidised in air.', 'E°(O₂/H₂O) = +1.23 V is more positive than E°(Fe³⁺/Fe²⁺) = +0.77 V, so oxygen can oxidise Fe²⁺ to Fe³⁺ (E°cell = +0.46 V).', 'compare E° values [1]; positive E°cell [1] [2]')])
myths(t, [('If E°cell is positive, the reaction will happen quickly.', 'A positive E°cell shows the reaction is feasible; it gives no information about rate.'),
          ('The half-cell with the more negative E° is reduced.', 'The half-cell with the more positive E° undergoes reduction; the more negative one undergoes oxidation.')])

REDOX_PAIRS = ['Mg', 'Zn', 'Fe', 'Ni', 'Pb', 'Cu', 'Ag', 'I', 'Fe3', 'Br', 'Cl', 'Sn', 'Al']


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def feasible(r, D):
    a, b = r.sample(REDOX_PAIRS, 2)
    # proposed: oxidised form of a reacts with reduced form of b
    o_a, r_a, n_a, E_a, h_a = HC[a]
    o_b, r_b, n_b, E_b, h_b = HC[b]
    if (a in ('Fe', 'Fe3') and b in ('Fe', 'Fe3')) or E_a == E_b:
        return None
    E = E_a - E_b
    eq = overall(b, a)
    ok = E > 0
    st = f'Use the E° values {h_a} E° = {m(f"{E_a:+.2f}")} V and {h_b} E° = {m(f"{E_b:+.2f}")} V to predict whether {o_a.lstrip("2")} will react with {r_b.lstrip("2")} under standard conditions.'
    if D <= 2:
        return MQ(r, st.replace(' to predict whether', '. Will').replace(' under standard conditions.', ' under standard conditions?'), 'Yes; E°cell is positive' if ok else 'No; E°cell is negative',
                  ['Yes; E°cell is negative', 'No; E°cell is positive', 'It depends only on the masses used'] if ok else ['Yes; E°cell is positive', 'Yes; E°cell is negative', 'It depends only on the masses used'],
                  f'E°cell = {m(f"{E_a:+.2f}")} − ({m(f"{E_b:+.2f}")}) = {m(f"{E:+.2f}")} V.')
    ans = (f'Yes: E°cell = {m(f"{E_a:+.2f}")} − ({m(f"{E_b:+.2f}")}) = {m(f"{E:+.2f}")} V, positive. Equation: {eq}.' if ok else
           f'No: E°cell = {m(f"{E_a:+.2f}")} − ({m(f"{E_b:+.2f}")}) = {m(f"{E:+.2f}")} V, negative; the reverse reaction is feasible instead.')
    key = 'E°cell calculated [1]; correct conclusion [1]' + ('; balanced equation [1] [3]' if ok else '; reverse reaction identified [1] [3]')
    return Q(st + (' If a reaction occurs, write the equation.' if D >= 3 else ''), ans, key, 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def feas_case(r, D):
    st = (f'A student in {city(r)} is given these data: MnO₄⁻ + 8H⁺ + 5e⁻ ⇌ Mn²⁺ + 4H₂O, E° = +1.52 V; Cl₂ + 2e⁻ ⇌ 2Cl⁻, E° = +1.36 V; Fe³⁺ + e⁻ ⇌ Fe²⁺, E° = +0.77 V; I₂ + 2e⁻ ⇌ 2I⁻, E° = +0.54 V; Cr₂O₇²⁻ + 14H⁺ + 6e⁻ ⇌ 2Cr³⁺ + 7H₂O, E° = +1.33 V.')
    parts = [P_('Explain why acidified MnO₄⁻ is not used to titrate Fe²⁺ in a solution containing hydrochloric acid.', 'MnO₄⁻ can also oxidise Cl⁻ to Cl₂ (E°cell = +0.16 V), so more MnO₄⁻ would be used and the titre would be too high.', 'MnO₄⁻ oxidises Cl⁻ [1]; E°cell positive [1]; titre too high [1] [3]'),
             P_('Show that Fe³⁺ ions can oxidise iodide ions and write the equation.', 'E°cell = 0.77 − 0.54 = +0.23 V (positive); 2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂', 'E°cell [1]; equation [1] [2]'),
             P_('Identify the strongest oxidising agent and the strongest reducing agent in the list.', 'Strongest oxidising agent: MnO₄⁻ (in acid); strongest reducing agent: I⁻.', '[2]'),
             P_('Write the overall equation for the oxidation of Fe²⁺ by acidified dichromate(VI) and calculate E°cell.', 'Cr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → 2Cr³⁺ + 7H₂O + 6Fe³⁺; E°cell = 1.33 − 0.77 = +0.56 V', 'equation [1]; balanced [1]; E°cell [1] [3]'),
             P_('Explain why the E° value of a half-cell containing H⁺ depends on pH.', 'H⁺ appears in the half-equation; changing [H⁺] shifts the equilibrium and so changes the electrode potential (less positive at higher pH).', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how standard electrode potentials can be used to predict whether reactions are feasible, and discuss the limitations of such predictions.', 'More positive E°: better oxidising agent; reduction happens at more positive half-cell; E°cell = E°red − E°ox; positive → feasible; example (Cl₂ + 2Br⁻); direction of electron flow from negative to positive; limitations: rate/activation energy, non-standard concentrations, temperature, E° for aqueous solutions only, small E°cell may be reversed by concentration changes.',
           'oxidising / reducing strength [1]; calculation method [2]; worked example [1]; limitations (two) [2]; concentration effect [1] [7]')])
t2c = t

# ---------------------------------------------------------------------
t = T('The Nernst equation and effect of concentration on electrode potential', 'the nernst equation')
facts(t, [('Nernst equation', 'E = E° + (0.059/z) log([oxidised form]/[reduced form]) at 298 K, which gives the electrode potential at non-standard concentrations'),
          ('concentration cell', 'a cell made of two identical half-cells with different ion concentrations; it has a small e.m.f. that depends on the concentration ratio')])
mcqs(t, [('How does the electrode potential of the Cu²⁺/Cu half-cell change when [Cu²⁺] is decreased?', 'It becomes less positive', 'Equilibrium Cu²⁺ + 2e⁻ ⇌ Cu shifts left.', ['It becomes more positive', 'It does not change', 'It becomes exactly zero']),
         ('In the Nernst equation E = E° + (0.059/z) log([ox]/[red]), what does z represent?', 'The number of electrons transferred in the half-equation', 'e.g. z = 2 for Zn²⁺/Zn.', ['The charge on the electrode', 'The concentration of the ion', 'The temperature']),
         ('The concentration of Ag⁺ in an Ag⁺/Ag half-cell is reduced from 1.0 to 0.010 mol dm⁻³. By how much does E change?', 'It decreases by 0.118 V', '0.059 × log(0.010) = −0.118 V.', ['It decreases by 0.059 V', 'It increases by 0.118 V', 'It decreases by 0.236 V'])])
shorts(t, [('State the Nernst equation for a metal/metal-ion half-cell Mⁿ⁺/M at 298 K.', 'E = E° + (0.059/n) log[Mⁿ⁺]', '[1]')])
explain(t, [('Explain, in terms of equilibrium, why increasing the concentration of Zn²⁺ makes the Zn²⁺/Zn electrode potential less negative.', 'Zn²⁺ + 2e⁻ ⇌ Zn shifts to the right, removing electrons from the electrode, so the electrode becomes less negative (E increases).', 'equilibrium shifts right [1]; fewer electrons on electrode / E more positive [1] [2]'),
            ('Explain why a cell made from two Cu²⁺/Cu half-cells with different concentrations produces a voltage.', 'The half-cell with the higher [Cu²⁺] has the more positive electrode potential (Nernst), so there is a potential difference; electrons flow until the concentrations become equal.', 'different E values from concentration [1]; potential difference / electron flow [1] [2]')])
myths(t, [('Changing the concentration of ions has no effect on electrode potential.', 'Electrode potentials depend on concentration as given by the Nernst equation; E° values apply only at 1.00 mol dm⁻³.'),
          ('In the Nernst equation, z is the charge on the ion squared.', 'z is the number of electrons transferred in the half-equation.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def nernst(r, D):
    mt = r.choice(['Zn', 'Cu', 'Ag', 'Ni', 'Fe', 'Pb', 'Fe3'])
    ox, red, z, E0, h = HC[mt]
    if mt == 'Fe3':
        a = r.choice([0.1, 0.2, 0.5, 2.0, 5.0, 10.0])
        b = r.choice([1.0, 0.5, 0.1, 0.05])
        E = E0 + 0.059 * math.log10(a / b)
        st = f'Calculate the electrode potential of an Fe³⁺/Fe²⁺ half-cell (E° = +0.77 V) at 298 K in which [Fe³⁺] = {fx(a, 2)} mol dm⁻³ and [Fe²⁺] = {fx(b, 2)} mol dm⁻³.'
        key = f'E = 0.77 + 0.059 log({fx(a, 2)}/{fx(b, 2)}) [1]; log term = {fx(math.log10(a / b), 3)} [1]; E = {m(f"{E:+.2f}")} V [1] [3]'
        ans = f'{m(f"{E:+.2f}")} V'
    else:
        c = r.choice([0.001, 0.005, 0.01, 0.05, 0.10, 0.20, 0.50, 2.0])
        E = E0 + 0.059 / z * math.log10(c)
        st = f'Calculate the electrode potential at 298 K of a {ox}/{red} half-cell (E° = {m(f"{E0:+.2f}")} V) in which [{ox}] = {fx(c, 3)} mol dm⁻³. Use E = E° + (0.059/z) log[{ox}].'
        key = f'z = {z} [1]; E = {m(f"{E0:+.2f}")} + (0.059/{z}) × log {fx(c, 3)} = {m(f"{E0:+.2f}")} + ({m(fx(0.059 / z * math.log10(c), 4))}) [1] = {m(f"{E:+.3f}")} V [1] [3]'
        ans = f'{m(f"{E:+.3f}")} V'
    if D == 1:
        return NQ(r, st.replace('Calculate the', 'What is the'), E, [E0, 2 * E0 - E, E + 0.059, E - 0.059 * 2], ' V', key, f=lambda v: m(f'{v:+.2f}'))
    if D >= 4 and mt != 'Fe3':
        other = r.choice([k for k in ('Cu', 'Ag', 'Zn', 'Ni') if k != mt])
        Eo = HC[other][3]
        Ecell = abs(Eo - E)
        st += f' This half-cell is connected to a standard {HC[other][0]}/{HC[other][1]} half-cell (E° = {m(f"{Eo:+.2f}")} V). Calculate the cell potential and identify the positive electrode.'
        posn = f'{HC[other][0]}/{HC[other][1]}' if Eo > E else f'{ox}/{red}'
        return Q(st, f'{ans}; E cell = {fx(Ecell, 3)} V; positive electrode: {posn}', key.replace(' [3]', '') + f'; Ecell = {fx(Ecell, 3)} V [1]; positive electrode {posn} [1] [5]', 'numerical')
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def conc_cell(r, D):
    c1 = r.choice([1.0, 0.5])
    c2 = r.choice([0.01, 0.001, 0.05, 0.005])
    Ecell = 0.059 / 2 * math.log10(c1 / c2)
    st = f'{who(r)} set up a cell consisting of two Cu²⁺/Cu half-cells, one with [Cu²⁺] = {fx(c1, 2)} mol dm⁻³ and the other with [Cu²⁺] = {fx(c2, 3)} mol dm⁻³, joined by a salt bridge. E°(Cu²⁺/Cu) = +0.34 V.'
    E1 = 0.34 + 0.0295 * math.log10(c1)
    E2 = 0.34 + 0.0295 * math.log10(c2)
    parts = [P_('Calculate the electrode potential of each half-cell.', f'{m(f"{E1:+.3f}")} V and {m(f"{E2:+.3f}")} V', f'Nernst with z = 2 [1]; both values correct [1] [2]'),
             P_('Calculate the cell e.m.f. and identify the positive electrode.', f'{fx(Ecell, 3)} V; the half-cell with {fx(c1, 2)} mol dm⁻³ Cu²⁺ is positive', f'difference = {fx(Ecell, 3)} V [1]; more concentrated half-cell positive [1] [2]'),
             P_('Describe what happens to the concentrations in each half-cell as the cell delivers a current.', 'In the concentrated half-cell Cu²⁺ is reduced to Cu so [Cu²⁺] falls; in the dilute half-cell Cu is oxidised so [Cu²⁺] rises; the e.m.f. falls to zero when they are equal.', 'concentrated falls [1]; dilute rises [1]; e.m.f. falls [1] [3]'),
             P_('Suggest how this type of cell could be used to measure an unknown Cu²⁺ concentration.', 'Measure the e.m.f. against a half-cell of known concentration and use the Nernst equation to calculate the unknown concentration.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how and why electrode potentials change with concentration, using the Nernst equation and examples.', 'E = E° + (0.059/z) log([ox]/[red]); increasing [oxidised form] shifts equilibrium right, E more positive; e.g. Cu²⁺/Cu at 0.010 mol dm⁻³: E = 0.34 − 0.059 = +0.28 V; Fe³⁺/Fe²⁺ ratio; H⁺ in half-equations makes E pH-dependent; consequences for feasibility when E°cell is small; concentration cells.',
           'equation [1]; equilibrium explanation [2]; worked example [2]; pH / feasibility consequence [2] [7]')])
t2d = t

CHAPTERS[2] = [t2a, t2b, t2c, t2d]


# ===================================================================== 3 Further aspects of equilibria
WEAK = [('ethanoic acid', 'CH₃COOH', 1.74e-5), ('methanoic acid', 'HCOOH', 1.78e-4), ('propanoic acid', 'CH₃CH₂COOH', 1.35e-5), ('benzoic acid', 'C₆H₅COOH', 6.31e-5),
        ('chloroethanoic acid', 'CH₂ClCOOH', 1.38e-3), ('hydrofluoric acid', 'HF', 5.6e-4), ('nitrous acid', 'HNO₂', 4.5e-4), ('lactic acid', 'CH₃CH(OH)COOH', 1.38e-4)]


def pka(K):
    return -math.log10(K)


t = T('pH, Kw, Ka and pKa: calculations for strong and weak acids and strong bases', 'ph, kw, ka and pka')
facts(t, [('pH', 'the negative logarithm to base 10 of the hydrogen ion concentration: pH = −log[H⁺]'),
          ('Kw', 'the ionic product of water, [H⁺][OH⁻] = 1.00 × 10⁻¹⁴ mol² dm⁻⁶ at 298 K'),
          ('Ka', 'the acid dissociation constant: Ka = [H⁺][A⁻]/[HA] for a weak acid HA'),
          ('pKa', 'the negative logarithm of Ka; a smaller pKa means a stronger acid'),
          ('strong acid', 'an acid that dissociates completely in aqueous solution'),
          ('weak acid', 'an acid that dissociates only partially in aqueous solution'),
          ('conjugate base', 'the species formed when an acid loses a proton, e.g. CH₃COO⁻ from CH₃COOH')])
mcqs(t, [('What is the pH of 0.010 mol dm⁻³ hydrochloric acid?', '2.0', 'Strong acid: [H⁺] = 0.010; pH = 2.0.', ['1.0', '0.010', '12.0']),
         ('What are the units of Kw?', 'mol² dm⁻⁶', '[H⁺][OH⁻].', ['mol dm⁻³', 'mol⁻² dm⁶', 'no units']),
         ('Which assumption is made when calculating the pH of a weak acid from Ka and its concentration?', 'The concentration of undissociated acid at equilibrium equals its initial concentration', 'Dissociation is very small; also [H⁺] = [A⁻].', ['The acid is fully dissociated', '[H⁺] from water is large', 'Ka changes with concentration']),
         ('Which acid is the strongest?', 'pKa = 2.9', 'Smallest pKa = largest Ka.', ['pKa = 4.8', 'pKa = 4.2', 'pKa = 9.2']),
         ('What is the pH of pure water at 298 K?', '7.00', '[H⁺] = 1.0 × 10⁻⁷.', ['0', '14.00', '1.00'])])
shorts(t, [('Write the expression for Ka for ethanoic acid.', 'Ka = [H⁺][CH₃COO⁻] ÷ [CH₃COOH]', '[1]'),
           ('State two assumptions made in calculating the pH of a weak acid.', '[H⁺] = [A⁻] (dissociation of water negligible); [HA] at equilibrium ≈ initial concentration (dissociation small).', '[2]')])
explain(t, [('Explain why pure water is neutral at all temperatures even though its pH changes.', 'In pure water [H⁺] = [OH⁻] always, so it is neutral; Kw increases with temperature (dissociation is endothermic), so [H⁺] increases and pH decreases below 7.', '[H⁺] = [OH⁻] [1]; Kw increases with T, so pH falls [1] [2]'),
            ('Explain why 0.10 mol dm⁻³ ethanoic acid has a higher pH than 0.10 mol dm⁻³ hydrochloric acid.', 'Ethanoic acid is weak and only partially dissociates, so [H⁺] is much lower than 0.10 mol dm⁻³; HCl dissociates fully.', 'partial vs full dissociation [1]; lower [H⁺] [1] [2]'),
            ('Explain why diluting a strong acid by a factor of 10 increases the pH by 1, but diluting a weak acid by 10 increases the pH by only about 0.5.', 'For a strong acid [H⁺] falls by 10 times. For a weak acid [H⁺] = √(Ka × c), so [H⁺] falls by √10 (and dilution increases the fraction dissociated).', 'strong: [H⁺] ÷ 10 [1]; weak: √(Ka c) relation [1] [2]')])
myths(t, [('A strong acid is the same as a concentrated acid.', 'Strength refers to the extent of dissociation; concentration refers to the amount of acid per dm³.'),
          ('The pH of 0.10 mol dm⁻³ NaOH is 1.', 'For a strong base pOH = 1, so pH = 14 − 1 = 13 at 298 K.'),
          ('A weak acid with a larger pKa is stronger.', 'A larger pKa means a smaller Ka, so the acid is weaker.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ph_calc(r, D):
    kind = r.choice(['strong', 'base', 'weak', 'weak', 'ka_from_ph']) if D >= 2 else r.choice(['strong', 'base'])
    if kind == 'strong':
        acid, n = r.choice([('hydrochloric acid', 1), ('nitric acid', 1), ('sulfuric acid (assume full dissociation)', 2)])
        c = r.choice([0.20, 0.050, 0.025, 0.0040, 0.0015, 0.12, 0.35])
        ph = -math.log10(c * n)
        st = f'Calculate the pH of {fx(c, 4)} mol dm⁻³ {acid}.'
        key = f'[H⁺] = {fx(c * n, 4)} mol dm⁻³ [1]; pH = −log {fx(c * n, 4)} = {fx(ph, 2)} [1] [2]'
        val = ph
    elif kind == 'base':
        base, n = r.choice([('sodium hydroxide', 1), ('potassium hydroxide', 1), ('barium hydroxide', 2)])
        c = r.choice([0.20, 0.050, 0.025, 0.0040, 0.10, 0.015])
        oh = c * n
        ph = 14 + math.log10(oh)
        st = f'Calculate the pH of {fx(c, 4)} mol dm⁻³ {base} at 298 K. (Kw = 1.00 × 10⁻¹⁴ mol² dm⁻⁶)'
        key = f'[OH⁻] = {fx(oh, 4)} [1]; [H⁺] = Kw ÷ [OH⁻] = {sci(1e-14 / oh, 3)} [1]; pH = {fx(ph, 2)} [1] [3]'
        val = ph
    elif kind == 'weak':
        nm, fm, Ka = r.choice(WEAK)
        c = r.choice([0.010, 0.050, 0.10, 0.20, 0.25, 0.50])
        h = math.sqrt(Ka * c)
        ph = -math.log10(h)
        st = f'Calculate the pH of {fx(c, 3)} mol dm⁻³ {nm}, {fm}. Ka = {sci(Ka, 3)} mol dm⁻³.'
        key = f'Ka = [H⁺]² ÷ [HA] [1]; [H⁺] = √({sci(Ka, 3)} × {fx(c, 3)}) = {sci(h, 3)} [1]; pH = {fx(ph, 2)} [1] [3]'
        val = ph
    else:
        nm, fm, Ka = r.choice(WEAK)
        c = r.choice([0.010, 0.050, 0.10, 0.20])
        ph = round(-math.log10(math.sqrt(Ka * c)), 2)
        h = 10 ** -ph
        Kc = h * h / c
        st = f'A {fx(c, 3)} mol dm⁻³ solution of {nm} has a pH of {fx(ph, 2)}. Calculate Ka and pKa for {nm}.'
        key = f'[H⁺] = 10^−{fx(ph, 2)} = {sci(h, 3)} [1]; Ka = [H⁺]² ÷ c = {sci(Kc, 3)} mol dm⁻³ [1]; pKa = {fx(pka(Kc), 2)} [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate Ka and pKa for', 'What is Ka for'), Kc, [h, h / c, Kc * 10, math.sqrt(Kc)], ' mol dm⁻³', key, f=lambda v: sci(v, 2))
        return Q(st, f'Ka = {sci(Kc, 3)} mol dm⁻³; pKa = {fx(pka(Kc), 2)}', key, 'numerical')
    if D <= 2:
        return NQ(r, st.replace('Calculate the pH', 'What is the pH'), val, [14 - val, val + 1, val - 1 if val > 1.5 else val + 2, -val], '', key, f=lambda v: fx(v, 2) if v >= 0 else m(fx(v, 2)))
    return Q(st, fx(val, 2), key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def acid_case(r, D):
    nm, fm, Ka = r.choice(WEAK)
    c = r.choice([0.10, 0.050, 0.20])
    h = math.sqrt(Ka * c)
    alpha = h / c * 100
    st = f'{who(r)} compares solutions of {fx(c, 2)} mol dm⁻³ hydrochloric acid and {fx(c, 2)} mol dm⁻³ {nm} (Ka = {sci(Ka, 3)} mol dm⁻³) at 298 K.'
    parts = [P_('Calculate the pH of each solution.', f'HCl: {fx(-math.log10(c), 2)}; {nm}: {fx(-math.log10(h), 2)}', f'HCl pH = {fx(-math.log10(c), 2)} [1]; [H⁺] = √(Ka c) = {sci(h, 3)} [1]; pH = {fx(-math.log10(h), 2)} [1] [3]'),
             P_(f'Calculate the percentage of {nm} molecules that are dissociated.', f'{fx(alpha, 2)}%', f'{sci(h, 3)} ÷ {fx(c, 2)} × 100 = {fx(alpha, 2)}% [1]'),
             P_('Explain why the two acids need the same volume of NaOH for neutralisation even though their pH values differ.', 'Both contain the same number of moles of acid (monoprotic, same concentration); as OH⁻ removes H⁺, the weak acid equilibrium shifts to release more H⁺ until all the acid reacts.', 'same moles of acid [1]; equilibrium shifts to replace H⁺ [1] [2]'),
             P_('Calculate pKa for the weak acid.', fx(pka(Ka), 2), f'pKa = −log {sci(Ka, 3)} = {fx(pka(Ka), 2)} [1]'),
             P_('Suggest a simple test, other than pH, to distinguish between the two solutions.', 'Add magnesium ribbon (or calcium carbonate): the strong acid gives faster effervescence; or measure electrical conductivity (higher for HCl).', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain the terms pH, Kw and Ka and show how they are used to calculate the pH of strong acids, strong bases and weak acids.', 'pH = −log[H⁺]; Kw = [H⁺][OH⁻] = 1.00 × 10⁻¹⁴ at 298 K; strong acid [H⁺] = c; strong base [H⁺] = Kw/[OH⁻]; weak acid Ka = [H⁺][A⁻]/[HA], assumptions, [H⁺] = √(Ka c); pKa; worked examples; temperature dependence of Kw.',
           'definitions [2]; strong acid example [1]; strong base example [1]; weak acid method with assumptions [2]; pKa / temperature [1] [7]')])
t3a = t

# ---------------------------------------------------------------------
t = T('Buffer solutions: how they work and calculating their pH; buffers in blood', 'buffer solutions')
facts(t, [('buffer solution', 'a solution that resists changes in pH when small amounts of acid or alkali are added'),
          ('acidic buffer', 'a buffer made from a weak acid and a salt of its conjugate base, e.g. ethanoic acid and sodium ethanoate'),
          ('basic buffer', 'a buffer made from a weak base and a salt of its conjugate acid, e.g. ammonia and ammonium chloride'),
          ('Henderson–Hasselbalch equation', 'pH = pKa + log([A⁻]/[HA]) for an acidic buffer')])
mcqs(t, [('Which mixture forms a buffer solution?', 'Ethanoic acid and sodium ethanoate', 'Weak acid + its conjugate base.', ['Hydrochloric acid and sodium chloride', 'Sodium hydroxide and sodium chloride', 'Nitric acid and potassium nitrate']),
         ('What is the pH of a buffer containing equal concentrations of a weak acid (pKa 4.76) and its sodium salt?', '4.76', 'pH = pKa when [A⁻] = [HA].', ['7.00', '9.24', '2.38']),
         ('Which equilibrium is the main buffer in human blood?', 'H₂CO₃ ⇌ H⁺ + HCO₃⁻', 'Carbonic acid / hydrogencarbonate.', ['NH₄⁺ ⇌ NH₃ + H⁺', 'HCl ⇌ H⁺ + Cl⁻', 'H₂O ⇌ H⁺ + OH⁻']),
         ('Which mixture produces a buffer when mixed?', '50 cm³ of 0.20 mol dm⁻³ CH₃COOH and 25 cm³ of 0.20 mol dm⁻³ NaOH', 'Half-neutralised weak acid: equal HA and A⁻.', ['25 cm³ of 0.20 mol dm⁻³ HCl and 25 cm³ of 0.20 mol dm⁻³ NaOH', '25 cm³ of 0.20 mol dm⁻³ CH₃COOH and 50 cm³ of 0.20 mol dm⁻³ NaOH', '50 cm³ of 0.20 mol dm⁻³ HCl and 25 cm³ of 0.20 mol dm⁻³ NaOH'])])
shorts(t, [('Write equations to show how an ethanoic acid / sodium ethanoate buffer removes added H⁺ and added OH⁻.', 'H⁺ + CH₃COO⁻ → CH₃COOH; OH⁻ + CH₃COOH → CH₃COO⁻ + H₂O', '[2]')])
explain(t, [('Explain how a mixture of ethanoic acid and sodium ethanoate acts as a buffer.', 'Large reservoirs of CH₃COOH and CH₃COO⁻; added H⁺ combines with CH₃COO⁻ to form CH₃COOH; added OH⁻ reacts with CH₃COOH to form CH₃COO⁻ and water; the ratio [A⁻]/[HA] changes very little so pH stays nearly constant.', 'large amounts of HA and A⁻ [1]; H⁺ removed by A⁻ [1]; OH⁻ removed by HA [1]; ratio nearly constant [1] [4]'),
            ('Explain how the carbonic acid–hydrogencarbonate buffer controls the pH of blood.', 'H₂CO₃ ⇌ H⁺ + HCO₃⁻; extra H⁺ (e.g. lactic acid) combines with HCO₃⁻ to form H₂CO₃, which forms CO₂ removed in the lungs; extra OH⁻ reacts with H₂CO₃; pH stays at about 7.4.', 'equilibrium [1]; response to H⁺ [1]; response to OH⁻ [1] [3]'),
            ('Explain why a buffer cannot resist large additions of acid.', 'Once most of the conjugate base has reacted, there is not enough A⁻ to remove further H⁺, so the pH falls sharply (buffer capacity exceeded).', '[2]')])
myths(t, [('A buffer keeps the pH completely constant.', 'A buffer minimises changes in pH for small additions of acid or alkali; the pH changes slightly.'),
          ('A buffer always has a pH of 7.', 'The pH of a buffer depends on the pKa of the weak acid and the ratio [A⁻]/[HA]; it can be acidic or basic.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def buffer_ph(r, D):
    nm, fm, Ka = r.choice(WEAK)
    pk = pka(Ka)
    mode = r.choice(['conc', 'mix', 'mass', 'ratio']) if D >= 3 else 'conc'
    if mode == 'conc':
        ca = r.choice([0.10, 0.20, 0.50, 0.25])
        cb = r.choice([0.05, 0.10, 0.20, 0.40, 0.15])
        ph = pk + math.log10(cb / ca)
        st = f'Calculate the pH of a buffer containing {fx(ca, 2)} mol dm⁻³ {nm} and {fx(cb, 2)} mol dm⁻³ of its sodium salt. Ka = {sci(Ka, 3)} mol dm⁻³.'
        key = f'[H⁺] = Ka × [HA]/[A⁻] = {sci(Ka, 3)} × {fx(ca, 2)}/{fx(cb, 2)} = {sci(Ka * ca / cb, 3)} [1]; pH = {fx(ph, 2)} [1] [2]'
    elif mode == 'mix':
        va, ca = r.choice([50, 100]), r.choice([0.10, 0.20])
        vb, cb = r.choice([10, 20, 25, 30, 40]), r.choice([0.10, 0.20])
        na, nb = va * ca / 1000, vb * cb / 1000
        if nb >= na:
            return None
        ph = pk + math.log10(nb / (na - nb))
        st = f'{vb} cm³ of {fx(cb, 2)} mol dm⁻³ NaOH is added to {va} cm³ of {fx(ca, 2)} mol dm⁻³ {nm} (Ka = {sci(Ka, 3)} mol dm⁻³). Calculate the pH of the resulting buffer.'
        key = f'mol HA = {g3(na)}; mol OH⁻ = {g3(nb)} [1]; HA left = {g3(na - nb)}, A⁻ formed = {g3(nb)} [1]; [H⁺] = Ka × {g3(na - nb)}/{g3(nb)} = {sci(Ka * (na - nb) / nb, 3)} [1]; pH = {fx(ph, 2)} [1] [4]'
    elif mode == 'mass':
        if nm != 'ethanoic acid':
            nm, fm, Ka = WEAK[0]
            pk = pka(Ka)
        V = r.choice([250, 500, 1000])
        ca = r.choice([0.10, 0.20])
        ms = r.choice([1.64, 2.05, 3.28, 4.10, 0.82])
        nb = ms / 82.0
        cb = nb / (V / 1000)
        ph = pk + math.log10(cb / ca)
        st = f'{ms:.2f} g of sodium ethanoate (Mr = 82.0) is dissolved in {V} cm³ of {fx(ca, 2)} mol dm⁻³ ethanoic acid (Ka = 1.74 × 10⁻⁵ mol dm⁻³). Assuming no volume change, calculate the pH of the buffer.'
        key = f'mol CH₃COONa = {g3(nb)} [1]; [CH₃COO⁻] = {g3(cb)} mol dm⁻³ [1]; [H⁺] = 1.74 × 10⁻⁵ × {fx(ca, 2)}/{g3(cb)} = {sci(Ka * ca / cb, 3)} [1]; pH = {fx(ph, 2)} [1] [4]'
    else:
        target = round(pk + r.choice([-0.5, -0.3, 0.2, 0.4, 0.6]), 2)
        ratio = 10 ** (target - pk)
        st = f'A buffer of pH {fx(target, 2)} is required using {nm} (pKa = {fx(pk, 2)}) and its sodium salt. Calculate the ratio [salt] : [acid] needed.'
        key = f'pH = pKa + log([A⁻]/[HA]) [1]; log ratio = {fx(target - pk, 2)} [1]; ratio = {fx(ratio, 2)} : 1 [1] [3]'
        return Q(st, f'{fx(ratio, 2)} : 1', key, 'numerical')
    if D <= 2:
        return NQ(r, st.replace('Calculate the pH', 'What is the pH'), ph, [pk, pk - (ph - pk), 14 - ph, ph + 1], '', key, f=lambda v: fx(v, 2))
    return Q(st, fx(ph, 2), key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def buffer_case(r, D):
    nm, fm, Ka = WEAK[0]
    ca, cb = r.choice([(0.10, 0.10), (0.20, 0.10), (0.10, 0.15), (0.15, 0.20)])
    V = 1.0
    add = r.choice([0.005, 0.010, 0.002])
    ph0 = pka(Ka) + math.log10(cb / ca)
    ph1 = pka(Ka) + math.log10((cb - add) / (ca + add))
    st = f'{who(r)} prepared 1.00 dm³ of a buffer containing {fx(ca, 2)} mol of ethanoic acid and {fx(cb, 2)} mol of sodium ethanoate (Ka = 1.74 × 10⁻⁵ mol dm⁻³). Then {fx(add, 3)} mol of HCl was added.'
    parts = [P_('Calculate the pH of the buffer before the acid was added.', fx(ph0, 2), f'[H⁺] = 1.74 × 10⁻⁵ × {fx(ca, 2)}/{fx(cb, 2)} [1]; pH = {fx(ph0, 2)} [1] [2]'),
             P_('Calculate the pH after adding the acid.', fx(ph1, 2), f'CH₃COO⁻ = {fx(cb - add, 3)} mol; CH₃COOH = {fx(ca + add, 3)} mol [1]; pH = {fx(ph1, 2)} [1] [2]'),
             P_('Calculate the pH if the same amount of HCl were added to 1.00 dm³ of pure water.', fx(-math.log10(add), 2), f'[H⁺] = {fx(add, 3)} [1]; pH = {fx(-math.log10(add), 2)} [1] [2]'),
             P_('Write an equation to show how the buffer removed the added H⁺ ions.', 'CH₃COO⁻ + H⁺ → CH₃COOH', '[1]'),
             P_('Explain why the pH of blood must be kept close to 7.4.', 'Enzymes and other proteins (e.g. haemoglobin) have ionisable R groups; a change in pH changes their charges and shape, affecting their function.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain what a buffer solution is, how an acidic buffer works, and how its pH can be calculated, with reference to the buffer in blood.', 'Definition; weak acid + conjugate base reservoirs; equations for added H⁺ and OH⁻; ratio nearly constant; pH = pKa + log([A⁻]/[HA]) or [H⁺] = Ka[HA]/[A⁻]; example calculation; blood: H₂CO₃/HCO₃⁻, CO₂ removal by lungs, pH 7.35–7.45; limits of buffer capacity.',
           'definition [1]; mechanism with equations [2]; calculation method [2]; blood buffer [2] [7]')])
t3b = t

# ---------------------------------------------------------------------
INDIC = [('methyl orange', 3.1, 4.4, 'red', 'yellow'), ('bromophenol blue', 3.0, 4.6, 'yellow', 'blue'), ('methyl red', 4.2, 6.3, 'red', 'yellow'),
         ('bromothymol blue', 6.0, 7.6, 'yellow', 'blue'), ('phenolphthalein', 8.3, 10.0, 'colourless', 'pink'), ('thymol blue (base range)', 8.0, 9.6, 'yellow', 'blue')]
TITR = [('strong acid', 'strong base', 'HCl', 'NaOH', (3.5, 10.5), 'any indicator with a range in the vertical section (e.g. methyl orange or phenolphthalein)', 7.0),
        ('weak acid', 'strong base', 'CH₃COOH', 'NaOH', (7.5, 10.5), 'phenolphthalein', 8.7),
        ('strong acid', 'weak base', 'HCl', 'NH₃', (3.5, 6.5), 'methyl orange (or methyl red)', 5.3),
        ('weak acid', 'weak base', 'CH₃COOH', 'NH₃', None, 'no suitable indicator (no sharp vertical section); use a pH meter', 7.0)]

t = T('pH titration curves and choice of indicator', 'ph titration curves and choice of indicator')
facts(t, [('equivalence point', 'the point in a titration at which the amounts of acid and base are exactly stoichiometrically equivalent'),
          ('end point', 'the point in a titration at which the indicator changes colour'),
          ('indicator', 'a weak acid (HIn) whose undissociated and dissociated forms have different colours; it changes colour over a range of about 2 pH units around its pKa'),
          ('half-equivalence point', 'the point in the titration of a weak acid at which half the acid has been neutralised, where pH = pKa')])
mcqs(t, [('Which indicator is most suitable for titrating ethanoic acid with sodium hydroxide?', 'Phenolphthalein', 'Vertical section about pH 7–11.', ['Methyl orange', 'Methyl red', 'Bromophenol blue']),
         ('Which indicator is most suitable for titrating ammonia solution with hydrochloric acid?', 'Methyl orange', 'Vertical section about pH 3–7.', ['Phenolphthalein', 'Thymol blue', 'No indicator works']),
         ('What is the approximate pH at the equivalence point when ethanoic acid is titrated with sodium hydroxide?', 'About 9', 'Ethanoate ions are weakly basic.', ['Exactly 7', 'About 4', 'About 13']),
         ('Why is no indicator suitable for a weak acid–weak base titration?', 'There is no steep vertical section in the titration curve', 'pH changes gradually at equivalence.', ['Weak acids do not react with weak bases', 'The equivalence point is at pH 14', 'Indicators are destroyed by weak bases'])])
shorts(t, [('State the relationship between pH and pKa at the half-equivalence point of a weak acid–strong base titration.', 'pH = pKa (because [HA] = [A⁻]).', '[1]')])
explain(t, [('Explain why an indicator changes colour over a range of pH values.', 'HIn ⇌ H⁺ + In⁻; the two forms have different colours; the colour seen depends on the ratio [In⁻]/[HIn], which changes from about 1:10 to 10:1 over about two pH units around pKa(HIn).', 'equilibrium HIn ⇌ H⁺ + In⁻ [1]; ratio determines colour [1]; ~2 pH units around pKa [1] [3]'),
            ('Explain the shape of the titration curve when NaOH is added to ethanoic acid.', 'Starts at about pH 3 (weak acid); rises slowly through a buffer region where pH ≈ pKa at half-neutralisation; steep rise around equivalence (pH 7–11) at the stoichiometric volume; levels off at about pH 12–13 in excess alkali.', 'start pH [1]; buffer region / half-equivalence [1]; vertical section 7–11 [1]; final pH [1] [4]'),
            ('Explain how a titration curve can be used to determine the pKa of a weak acid.', 'Find the equivalence volume from the vertical section; at half this volume half the acid is neutralised, [HA] = [A⁻], so pH = pKa; read the pH from the curve.', 'equivalence volume [1]; half-equivalence [HA] = [A⁻] [1]; read pH = pKa [1] [3]')])
myths(t, [('The pH at the equivalence point is always 7.', 'It is 7 only for strong acid–strong base titrations; it is above 7 for weak acid–strong base and below 7 for strong acid–weak base.'),
          ('Any indicator will work for any titration.', 'The indicator must change colour completely within the vertical section of the titration curve.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def indicator(r, D):
    a_t, b_t, acid, base, rng, best, eqph = r.choice(TITR)
    ind = r.choice(INDIC)
    nm, lo, hi, c1, c2 = ind
    suit = rng is not None and lo >= rng[0] and hi <= rng[1]
    if D <= 2:
        return MQ(r, f'A {a_t} ({acid}) is titrated with a {b_t} ({base}). Which indicator would be most suitable?', cap(best.split(' (')[0]) if rng else 'No indicator is suitable; use a pH meter',
                  [cap(x) for x in ['methyl orange', 'phenolphthalein', 'bromothymol blue', 'thymol blue'] if x != best.split(' (')[0]][:3] if rng else ['Methyl orange', 'Phenolphthalein', 'Bromothymol blue'],
                  f'Vertical section {"pH " + str(rng[0]) + "–" + str(rng[1]) if rng else "absent"}; {best}.')
    st = f'{who(r)} titrates {acid}(aq) with {base}(aq). The vertical section of the titration curve is ' + (f'from about pH {rng[0]} to pH {rng[1]}' if rng else 'absent; the pH changes gradually') + f'. {cap(nm)} changes colour from {c1} to {c2} between pH {lo} and {hi}. Explain whether {nm} is a suitable indicator.'
    ans = (f'Yes: its range ({lo}–{hi}) lies entirely within the vertical section, so it changes colour sharply at the equivalence point.' if suit else
           f'No: ' + (f'its range ({lo}–{hi}) does not lie within the vertical section ({rng[0]}–{rng[1]}), so it would change colour gradually or before/after the equivalence point.' if rng else 'there is no vertical section, so no indicator gives a sharp end point.'))
    return Q(st, ans, 'correct decision [1]; comparison of range with vertical section [1] [2]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def titr_curve(r, D):
    nm, fm, Ka = r.choice(WEAK)
    ca = r.choice([0.080, 0.10, 0.12, 0.15])
    va = 25.0
    cb = r.choice([0.10, 0.12, 0.15, 0.20])
    veq = va * ca / cb
    st = f'{fx(va, 1)} cm³ of {fx(ca, 3)} mol dm⁻³ {nm} (Ka = {sci(Ka, 3)} mol dm⁻³) is titrated with {fx(cb, 2)} mol dm⁻³ NaOH.'
    h0 = math.sqrt(Ka * ca)
    parts = [P_('Calculate the volume of NaOH needed to reach the equivalence point.', f'{fx(veq, 2)} cm³', f'mol acid = {g3(va * ca / 1000)} [1]; V = {g3(va * ca / 1000)} ÷ {fx(cb, 2)} × 1000 = {fx(veq, 2)} cm³ [1] [2]'),
             P_('Calculate the initial pH of the acid.', fx(-math.log10(h0), 2), f'[H⁺] = √(Ka × {fx(ca, 3)}) = {sci(h0, 3)} [1]; pH = {fx(-math.log10(h0), 2)} [1] [2]'),
             P_('State the pH after half of the equivalence volume has been added, and explain why.', f'{fx(pka(Ka), 2)}: [HA] = [A⁻] so pH = pKa', f'pH = pKa = {fx(pka(Ka), 2)} [1]; [HA] = [A⁻] [1] [2]'),
             P_('Suggest a suitable indicator and explain your choice.', 'Phenolphthalein: the equivalence point is above pH 7 (vertical section about 7–11) and phenolphthalein changes colour between pH 8.3 and 10.', 'phenolphthalein [1]; reason [1] [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def curve_case(r, D):
    a_t, b_t, acid, base, rng, best, eqph = r.choice(TITR[:3])
    st = f'{who(r)} used a pH meter to follow the titration of 25.0 cm³ of 0.100 mol dm⁻³ {acid} with 0.100 mol dm⁻³ {base}, and plotted a titration curve.'
    parts = [P_('Sketch or describe the shape of the curve, giving the approximate initial pH, the pH range of the vertical section and the equivalence volume.',
                f'Initial pH about {"1" if a_t == "strong acid" else "2.9"}; vertical section about pH {rng[0]}–{rng[1]} at 25.0 cm³; final pH about {"13" if b_t == "strong base" else "11"}.', 'initial pH [1]; vertical section [1]; equivalence at 25.0 cm³ [1]; final pH [1] [4]'),
             P_('State the pH at the equivalence point and explain why it has this value.', f'About {eqph}: ' + ('the salt (NaCl) does not hydrolyse.' if eqph == 7.0 else ('the ethanoate ion is a weak base, so the solution is slightly alkaline.' if eqph > 7 else 'the ammonium ion is a weak acid, so the solution is slightly acidic.')), 'value [1]; explanation [1] [2]'),
             P_('Choose a suitable indicator and justify your choice.', f'{cap(best)}: its colour-change range lies within the vertical section.', 'indicator [1]; justification [1] [2]'),
             P_('Explain why using a pH meter is better than an indicator for determining the pKa of a weak acid.', 'A pH meter gives the pH at every point, so the half-equivalence pH (= pKa) can be read from the curve; an indicator only shows the end point.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe and explain the shapes of pH titration curves for strong acid–strong base, weak acid–strong base and strong acid–weak base titrations, and explain how an indicator is chosen.', 'Strong/strong: pH 1 to 13, vertical 3–11, equivalence 7. Weak/strong: start ~3, buffer region, pH = pKa at half-equivalence, vertical 7–11, equivalence ~9 (A⁻ basic). Strong/weak: vertical 3–7, equivalence ~5 (NH₄⁺ acidic). Weak/weak: no vertical. Indicator: HIn ⇌ H⁺ + In⁻, range ≈ pKa ± 1, must lie within vertical section; examples.',
           'three curves [3]; equivalence pH explanations [1]; indicator theory [1]; choice rule with examples [2] [7]')])
t3c = t

# ---------------------------------------------------------------------
KSP = [('silver chloride', 'AgCl', 1, 1, 1.8e-10, 143.4, 'Ag⁺', 'Cl⁻'), ('barium sulfate', 'BaSO4', 1, 1, 1.1e-10, 233.4, 'Ba²⁺', 'SO₄²⁻'),
       ('calcium fluoride', 'CaF2', 1, 2, 3.9e-11, 78.1, 'Ca²⁺', 'F⁻'), ('lead(II) iodide', 'PbI2', 1, 2, 7.1e-9, 461.0, 'Pb²⁺', 'I⁻'),
       ('silver chromate', 'Ag2CrO4', 2, 1, 1.1e-12, 331.8, 'Ag⁺', 'CrO₄²⁻'), ('magnesium hydroxide', 'Mg(OH)2', 1, 2, 5.6e-12, 58.3, 'Mg²⁺', 'OH⁻'),
       ('calcium carbonate', 'CaCO3', 1, 1, 3.4e-9, 100.1, 'Ca²⁺', 'CO₃²⁻'), ('silver bromide', 'AgBr', 1, 1, 5.0e-13, 187.8, 'Ag⁺', 'Br⁻'),
       ('lead(II) chloride', 'PbCl2', 1, 2, 1.7e-5, 278.2, 'Pb²⁺', 'Cl⁻'), ('copper(II) hydroxide', 'Cu(OH)2', 1, 2, 2.2e-20, 97.5, 'Cu²⁺', 'OH⁻')]


def ksp_expr(x, y, cat, an):
    return f'[{cat}]{"²" if x == 2 else ""}[{an}]{"²" if y == 2 else ""}'


def ksp_units(x, y):
    n = x + y
    return f'mol{sup(n)} dm{sup(-3 * n)}'


t = T('Solubility product Ksp and the common ion effect', 'solubility product ksp')
facts(t, [('solubility product', 'Ksp: the product of the concentrations of the ions in a saturated solution of a sparingly soluble salt, each raised to the power of its coefficient in the equilibrium'),
          ('common ion effect', 'the reduction in the solubility of a sparingly soluble salt when a solution containing one of its ions is added'),
          ('ionic product', 'the product of ion concentrations (raised to their powers) in any solution; a precipitate forms if it exceeds Ksp'),
          ('saturated solution', 'a solution containing the maximum amount of solute that can dissolve at that temperature, in equilibrium with undissolved solid')])
mcqs(t, [('What is the Ksp expression for calcium fluoride, CaF₂?', '[Ca²⁺][F⁻]²', 'CaF₂(s) ⇌ Ca²⁺ + 2F⁻.', ['[Ca²⁺][F⁻]', '[Ca²⁺][2F⁻]', '[Ca²⁺]²[F⁻]']),
         ('What are the units of Ksp for silver chloride?', 'mol² dm⁻⁶', 'Two ion concentrations multiplied.', ['mol dm⁻³', 'mol³ dm⁻⁹', 'no units']),
         ('Adding sodium chloride to a saturated solution of silver chloride causes', 'some silver chloride to precipitate', 'Common ion effect: equilibrium shifts left.', ['more silver chloride to dissolve', 'no change', 'silver metal to form']),
         ('A precipitate forms when two solutions are mixed if', 'the ionic product exceeds Ksp', 'The solution would be supersaturated.', ['the ionic product is less than Ksp', 'Ksp is greater than 1', 'the solutions have the same concentration'])])
shorts(t, [('Write the expression for the solubility product of lead(II) iodide and give its units.', 'Ksp = [Pb²⁺][I⁻]²; mol³ dm⁻⁹', 'expression [1]; units [1] [2]')])
explain(t, [('Explain the common ion effect using silver chloride and sodium chloride as an example.', 'AgCl(s) ⇌ Ag⁺(aq) + Cl⁻(aq); adding NaCl increases [Cl⁻]; to keep [Ag⁺][Cl⁻] = Ksp the equilibrium shifts left, AgCl precipitates and its solubility decreases.', 'equilibrium [1]; increased [Cl⁻] [1]; shift left / lower solubility [1] [3]'),
            ('Explain why Ksp values are only used for sparingly soluble salts.', 'For very soluble salts the ion concentrations are high and ions interact, so the simple expression is not valid; Ksp applies to saturated solutions of salts with low solubility.', '[2]'),
            ('Explain how Ksp is used to predict whether a precipitate forms when two solutions are mixed.', 'Calculate the concentrations of the ions after mixing (allowing for dilution); calculate the ionic product; if it exceeds Ksp, a precipitate forms.', 'concentrations after mixing [1]; ionic product [1]; compare with Ksp [1] [3]')])
myths(t, [('A salt with a smaller Ksp is always less soluble than one with a larger Ksp.', 'This is only true for salts of the same formula type (e.g. both AB); Ksp values of AB and AB₂ salts cannot be compared directly.'),
          ('Adding a common ion increases the Ksp of a salt.', 'Ksp is constant at a given temperature; the common ion decreases the solubility, not Ksp.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ksp_calc(r, D):
    nm, f, x, y, K, M, cat, an = r.choice(KSP)
    s = (K / (x ** x * y ** y)) ** (1 / (x + y))
    mode = r.choice(['sol', 'ksp', 'common', 'ppt']) if D >= 3 else r.choice(['sol', 'ksp'])
    expr = ksp_expr(x, y, cat, an)
    if mode == 'sol':
        st = f'The solubility product of {nm}, {F(f)}, is {sci(K, 2)} {ksp_units(x, y)} at 298 K. Calculate its solubility in mol dm⁻³.'
        pw = f'{x ** x * y ** y}s{sup(x + y)}' if x + y > 2 else 's²'
        key = f'Ksp = {expr} = {pw} [1]; s = {sci(s, 3)} mol dm⁻³ [1] [2]'
        if D <= 2:
            return NQ(r, st.replace('Calculate its solubility', 'What is its solubility'), s, [math.sqrt(K), K, s * 2, s / 2] if x + y > 2 else [K, s * 2, K ** (1 / 3), s * 10], ' mol dm⁻³', key, f=lambda v: sci(v, 2))
        if D >= 4:
            st += ' Hence calculate its solubility in g dm⁻³.'
            return Q(st, f'{sci(s, 3)} mol dm⁻³; {sci(s * M, 3)} g dm⁻³', key.replace(' [2]', '') + f'; × Mr {M} = {sci(s * M, 3)} g dm⁻³ [1] [3]', 'numerical')
        return Q(st, f'{sci(s, 3)} mol dm⁻³', key, 'numerical')
    if mode == 'ksp':
        sg = float(f'{s * M:.3g}')
        s2 = sg / M
        K2 = (x * s2) ** x * (y * s2) ** y
        st = f'The solubility of {nm}, {F(f)}, is {sci(sg, 3)} g dm⁻³ at 298 K. Calculate the solubility product, giving its units.'
        key = f's = {sci(sg, 3)} ÷ {M} = {sci(s2, 3)} mol dm⁻³ [1]; [{cat}] = {sci(x * s2, 3)}, [{an}] = {sci(y * s2, 3)} [1]; Ksp = {expr} = {sci(K2, 3)} {ksp_units(x, y)} [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the solubility product, giving its units', 'What is the solubility product'), K2, [s2 ** 2 if x + y > 2 else s2, K2 * 2, K2 / 4, s2], f' {ksp_units(x, y)}', key, f=lambda v: sci(v, 2))
        return Q(st, f'{sci(K2, 3)} {ksp_units(x, y)}', key, 'numerical')
    if mode == 'common':
        if x != 1:
            return None
        c = r.choice([0.010, 0.050, 0.10, 0.20])
        src = {'Cl⁻': 'sodium chloride', 'SO₄²⁻': 'sodium sulfate', 'F⁻': 'sodium fluoride', 'I⁻': 'potassium iodide', 'OH⁻': 'sodium hydroxide', 'CO₃²⁻': 'sodium carbonate', 'Br⁻': 'potassium bromide'}[an]
        sc = K / (y * c) ** y
        st = f'Ksp of {nm} is {sci(K, 2)} {ksp_units(x, y)}. Calculate the solubility of {nm} in {fx(c, 3)} mol dm⁻³ {src} and compare it with its solubility in pure water.'
        key = f'[{an}] ≈ {fx(y * c, 3)} (from {src}) [1]; [{cat}] = Ksp ÷ {fx(y * c, 3)}{"²" if y == 2 else ""} = {sci(sc, 3)} mol dm⁻³ [1]; in water s = {sci(s, 3)}, so much lower (common ion effect) [1] [3]'
        return Q(st, f'{sci(sc, 3)} mol dm⁻³ (compared with {sci(s, 3)} mol dm⁻³ in water); lower due to the common ion effect', key, 'numerical')
    v1, v2 = r.choice([(50, 50), (100, 100), (25, 75)])
    c1 = r.choice([1e-3, 2e-3, 5e-4, 1e-2, 1e-4])
    c2 = r.choice([1e-3, 2e-3, 5e-4, 1e-2, 1e-4])
    a1 = c1 * v1 / (v1 + v2)
    a2 = c2 * v2 / (v1 + v2)
    ip = a1 ** x * a2 ** y
    st = (f'{v1} cm³ of {sci(c1, 1)} mol dm⁻³ of a solution containing {cat} ions is mixed with {v2} cm³ of {sci(c2, 1)} mol dm⁻³ of a solution containing {an} ions. '
          f'Ksp of {nm} = {sci(K, 2)} {ksp_units(x, y)}. Predict whether a precipitate of {nm} forms.')
    yes = ip > K
    key = f'concentrations after mixing: [{cat}] = {sci(a1, 3)}, [{an}] = {sci(a2, 3)} [1]; ionic product = {sci(ip, 3)} [1]; {">" if yes else "<"} Ksp so {"precipitate forms" if yes else "no precipitate"} [1] [3]'
    return Q(st, f'Ionic product {sci(ip, 3)} is {"greater" if yes else "less"} than Ksp, so {"a precipitate forms" if yes else "no precipitate forms"}.', key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def ksp_case(r, D):
    nm, f, x, y, K, M, cat, an = r.choice([k for k in KSP if k[2] == 1])
    s = (K / (y ** y)) ** (1 / (1 + y))
    st = f'{who(r)} is investigating {nm}, {F(f)}, which has Ksp = {sci(K, 2)} {ksp_units(x, y)} at 298 K, in {lab(r)}.'
    parts = [P_(f'Write an equation for the equilibrium in a saturated solution of {nm} and the expression for Ksp.', f'{F(f)}(s) ⇌ {cat}(aq) + {"2" if y == 2 else ""}{an}(aq); Ksp = {ksp_expr(x, y, cat, an)}', 'equation [1]; expression [1] [2]'),
             P_('Calculate the solubility in mol dm⁻³ and in g dm⁻³.', f'{sci(s, 3)} mol dm⁻³; {sci(s * M, 3)} g dm⁻³', f's from Ksp = {"4s³" if y == 2 else "s²"} [1]; s = {sci(s, 3)} [1]; × {M} = {sci(s * M, 3)} g dm⁻³ [1] [3]'),
             P_(f'Explain the effect on the solubility of {nm} of adding a solution containing {an} ions.', f'Solubility decreases: increased [{an}] shifts the equilibrium to the left (common ion effect), so the solid precipitates until the ionic product equals Ksp again.', 'decreases [1]; equilibrium shift / Ksp constant [1] [2]'),
             P_('Explain why the Ksp of a salt depends on temperature but not on the presence of other ions.', 'Ksp is an equilibrium constant, which changes only with temperature; other ions change the position of equilibrium (concentrations) but not the constant.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain the meaning of solubility product and the common ion effect, and show how Ksp values are used in calculations.', 'Ksp expression from equilibrium of sparingly soluble salt; units; calculating solubility from Ksp (s² or 4s³); Ksp from solubility; predicting precipitation by comparing ionic product with Ksp after mixing; common ion effect: shift of equilibrium, reduced solubility, calculation; Ksp constant at fixed temperature.',
           'definition and expression [2]; solubility calculation [2]; precipitation prediction [1]; common ion effect with example [2] [7]')])
t3d = t

# ---------------------------------------------------------------------
t = T('Partition coefficients between two immiscible solvents', 'partition coefficients')
facts(t, [('partition coefficient', 'Kpc: the ratio of the concentrations of a solute in two immiscible solvents at equilibrium, at a given temperature'),
          ('immiscible', 'describes two liquids that do not mix but form separate layers, such as water and hexane'),
          ('solvent extraction', 'the separation of a solute from one solvent by shaking with a second, immiscible solvent in which it is more soluble')])
mcqs(t, [('Ammonia is shaken with water and trichloromethane. Kpc (CHCl₃/water) is 0.04. What does this show?', 'Ammonia is much more soluble in water', 'It forms hydrogen bonds with water.', ['Ammonia is more soluble in trichloromethane', 'Ammonia is equally soluble in both', 'Ammonia does not dissolve in either']),
         ('Which gives the greater extraction of a solute from water?', 'Two extractions with 25 cm³ of organic solvent', 'Several small extractions remove more than one large one.', ['One extraction with 50 cm³ of organic solvent', 'One extraction with 25 cm³ of organic solvent', 'Both methods remove the same amount']),
         ('Kpc depends on', 'the temperature and the solute and solvents used', 'It is an equilibrium constant.', ['the volume of the solvents', 'the mass of solute added', 'the shape of the separating funnel'])])
shorts(t, [('Write an expression for the partition coefficient of iodine between hexane and water.', 'Kpc = [I₂ in hexane] ÷ [I₂ in water]', '[1]')])
explain(t, [('Explain why iodine has a large partition coefficient between hexane and water.', 'Iodine is non-polar; it interacts well with non-polar hexane by instantaneous dipole–induced dipole forces but cannot form strong interactions with polar water molecules (which hydrogen-bond to each other).', 'iodine non-polar [1]; similar intermolecular forces with hexane [1] [2]'),
            ('Explain why several small extractions are more efficient than one large one.', 'Each extraction removes a fraction of the remaining solute; repeating with fresh solvent removes a fraction of what is left each time, so the total removed is greater for the same total volume.', '[2]')])
myths(t, [('The partition coefficient depends on how much solvent is used.', 'Kpc is an equilibrium constant at a given temperature; the amount extracted depends on volumes, but Kpc does not.'),
          ('A partition coefficient greater than 1 means the solute is more soluble in water.', 'It depends on how Kpc is defined; for Kpc = [org]/[aq], a value above 1 means the solute is more soluble in the organic solvent.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def partition(r, D):
    sol = r.choice([('butanedioic acid', 'ethoxyethane', 'water'), ('iodine', 'hexane', 'water'), ('caffeine', 'dichloromethane', 'water'), ('an organic acid X', 'octan-1-ol', 'water')])
    solute, org, aq = sol
    K = r.choice([0.25, 0.5, 2.0, 4.0, 8.5, 15.0, 40.0, 85.0])
    tot = r.choice([0.50, 1.00, 2.00, 5.00])  # g
    Vaq = r.choice([50, 100])
    Vorg = r.choice([10, 20, 25, 50])
    x = tot * K * Vorg / (K * Vorg + Vaq)
    mode = r.choice(['K', 'extract', 'double']) if D >= 3 else 'K'
    if mode == 'K':
        co = x / Vorg
        ca = (tot - x) / Vaq
        st = f'{fx(tot, 2)} g of {solute} was shaken with {Vaq} cm³ of {aq} and {Vorg} cm³ of {org} until equilibrium. The {org} layer then contained {g3(x)} g of {solute}. Calculate the partition coefficient, Kpc = [{solute}]({org}) ÷ [{solute}]({aq}).'
        key = f'mass in {aq} = {g3(tot - x)} g [1]; concentrations {g3(x)}/{Vorg} and {g3(tot - x)}/{Vaq} [1]; Kpc = {g3(co / ca)} [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the partition coefficient', 'What is the partition coefficient'), co / ca, [x / (tot - x), ca / co, (tot - x) / x, co / ca * 2], '', key)
        return Q(st, g3(co / ca), key, 'numerical')
    if mode == 'extract':
        st = f'Kpc for {solute} between {org} and {aq} is {fx(K, 2)}. {fx(tot, 2)} g of {solute} is dissolved in {Vaq} cm³ of {aq} and shaken with {Vorg} cm³ of {org}. Calculate the mass extracted into the {org}.'
        key = f'let x g extracted: (x/{Vorg}) ÷ (({fx(tot, 2)} − x)/{Vaq}) = {fx(K, 2)} [1]; rearranged [1]; x = {g3(x)} g [1] [3]'
        return Q(st, f'{g3(x)} g', key, 'numerical')
    half = Vorg / 2
    x1 = tot * K * half / (K * half + Vaq)
    rem = tot - x1
    x2 = rem * K * half / (K * half + Vaq)
    st = (f'Kpc for {solute} between {org} and {aq} is {fx(K, 2)}. {fx(tot, 2)} g of {solute} is dissolved in {Vaq} cm³ of {aq}. Compare the total mass extracted using (i) one portion of {Vorg} cm³ of {org} and (ii) two successive portions of {fx(half, 1)} cm³.')
    key = f'(i) x = {g3(x)} g [1]; (ii) first {g3(x1)} g [1]; second {g3(x2)} g [1]; total {g3(x1 + x2)} g, more than one portion [1] [4]'
    return Q(st, f'(i) {g3(x)} g; (ii) {g3(x1 + x2)} g — two smaller portions extract more.', key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def partition_case(r, D):
    st = f'{who(r)} wants to extract an organic product from an aqueous reaction mixture using a separating funnel and an immiscible organic solvent.'
    parts = [P_('Describe how the extraction would be carried out.', 'Pour mixture and solvent into separating funnel; stopper, invert and shake, releasing pressure through the tap; allow layers to separate; run off the lower layer; repeat with fresh solvent; combine organic layers, dry with anhydrous salt, evaporate the solvent.', 'shake and vent [1]; separate layers [1]; repeat [1]; dry and remove solvent [1] [4]'),
             P_('Explain why the organic solvent must be immiscible with water.', 'So that two layers form and can be separated; the product distributes between them according to Kpc.', '[2]'),
             P_('Explain how the polarity of a solute affects its partition coefficient between octan-1-ol and water.', 'Non-polar solutes are more soluble in octan-1-ol (larger Kpc); polar or ionic solutes that hydrogen-bond with water are more soluble in water (smaller Kpc).', '[2]'),
             P_('Suggest why the extraction is repeated several times with small volumes of solvent.', 'More solute is extracted in total for the same total volume of solvent.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain what is meant by a partition coefficient and how it is used in solvent extraction, including a calculation to show why several small extractions are more effective.', 'Kpc = [X]org/[X]aq at equilibrium at a given temperature; depends on relative solubility (polarity, intermolecular forces); extraction method; calculation: x/Vorg ÷ (m − x)/Vaq = Kpc; one vs two portions worked example; uses (drug design – lipophilicity, purification).',
           'definition [1]; factors affecting Kpc [1]; method [2]; calculation [2]; application [1] [7]')])
t3e = t

CHAPTERS[3] = [t3a, t3b, t3c, t3d, t3e]


# ===================================================================== 4 Reaction kinetics
def k_units(n):
    return {0: 'mol dm⁻³ s⁻¹', 1: 's⁻¹', 2: 'dm³ mol⁻¹ s⁻¹', 3: 'dm⁶ mol⁻² s⁻¹', 4: 'dm⁹ mol⁻³ s⁻¹'}[n]


def nice(v):
    """3 s.f.; ordinary notation for 0.01-9999, standard form otherwise."""
    return g3(v) if 0.01 <= abs(v) < 10000 else sci(v, 3)


def rate_eq(sp, od):
    terms = ''.join(f'[{s}]' + ('²' if n == 2 else '') for s, n in zip(sp, od) if n)
    return 'rate = k' + terms


ORD_WORD = {0: 'zero order', 1: 'first order', 2: 'second order'}
RATE_RX = [
    ('2NO(g) + O₂(g) → 2NO₂(g)', ['NO', 'O₂'], [2, 1]),
    ('H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l)', ['H₂O₂', 'I⁻', 'H⁺'], [1, 1, 0]),
    ('CH₃COCH₃(aq) + I₂(aq) → CH₃COCH₂I(aq) + HI(aq), catalysed by H⁺(aq)', ['CH₃COCH₃', 'I₂', 'H⁺'], [1, 0, 1]),
    ('(CH₃)₃CBr + OH⁻ → (CH₃)₃COH + Br⁻', ['(CH₃)₃CBr', 'OH⁻'], [1, 0]),
    ('CH₃CH₂Br + OH⁻ → CH₃CH₂OH + Br⁻', ['CH₃CH₂Br', 'OH⁻'], [1, 1]),
    ('S₂O₈²⁻(aq) + 2I⁻(aq) → 2SO₄²⁻(aq) + I₂(aq)', ['S₂O₈²⁻', 'I⁻'], [1, 1]),
    ('2H₂(g) + 2NO(g) → N₂(g) + 2H₂O(g)', ['NO', 'H₂'], [2, 1]),
    ('BrO₃⁻(aq) + 5Br⁻(aq) + 6H⁺(aq) → 3Br₂(aq) + 3H₂O(l)', ['BrO₃⁻', 'Br⁻', 'H⁺'], [1, 1, 2]),
    ('2NO₂(g) + F₂(g) → 2NO₂F(g)', ['NO₂', 'F₂'], [1, 1]),
    ('NO₂(g) + CO(g) → NO(g) + CO₂(g)', ['NO₂', 'CO'], [2, 0]),
    ('P + Q → R', ['P', 'Q'], None), ('X + 2Y → Z', ['X', 'Y'], None), ('D + E → F + G', ['D', 'E'], None)]


def rates_table(r, D):
    eqn, sp, od = r.choice(RATE_RX)
    if od is None:
        od = r.choice([[1, 1], [2, 0], [1, 2], [0, 1], [2, 1], [1, 0], [0, 2]])
    k = r.choice([1.5, 2.4, 3.2, 4.0, 6.5, 8.0, 1.2, 2.8, 5.5]) * 10 ** r.randint(-4, 0)
    base = [r.choice([0.010, 0.020, 0.025, 0.050, 0.10, 0.20]) for _ in sp]
    exps = [list(base)]
    facs = []
    for i in range(len(sp)):
        f = r.choice([2, 3, 4] if od[i] < 2 else [2, 3])
        row = list(base)
        row[i] = base[i] * f
        facs.append(f)
        exps.append(row)
    if D >= 4 and len(sp) == 2:
        # replace experiment 3 by one where both concentrations change
        f0, f1 = r.choice([(2, 2), (3, 2), (2, 3)])
        exps[2] = [base[0] * f0, base[1] * f1]
    rates = [float(f'{k * math.prod(c ** n for c, n in zip(row, od)):.3g}') for row in exps]
    kd = rates[0] / math.prod(c ** n for c, n in zip(base, od))
    return eqn, sp, od, exps, rates, kd


def table_text(sp, exps, rates):
    rows = '; '.join(f'experiment {i + 1}: ' + ', '.join(f'[{s}] = {fx(c, 4)}' for s, c in zip(sp, row)) + f', initial rate = {nice(rt)} mol dm⁻³ s⁻¹' for i, (row, rt) in enumerate(zip(exps, rates)))
    return rows


t = T('Rate equations, orders of reaction and rate constants', 'rate equations, orders of reaction')
facts(t, [('rate of reaction', 'the change in concentration of a reactant or product per unit time'),
          ('order of reaction', 'the power to which the concentration of a reactant is raised in the rate equation'),
          ('rate constant', 'k: the constant of proportionality in the rate equation; it changes only with temperature (or catalyst)'),
          ('rate equation', 'an expression, found by experiment, of the form rate = k[A]ᵐ[B]ⁿ'),
          ('overall order', 'the sum of the orders with respect to each reactant in the rate equation'),
          ('initial rate', 'the rate of reaction at time zero, found from the gradient of the tangent to a concentration–time graph at t = 0')])
mcqs(t, [('For rate = k[A]²[B], what is the overall order of reaction?', '3', '2 + 1 = 3.', ['2', '1', '4']),
         ('What are the units of k for a second-order reaction?', 'dm³ mol⁻¹ s⁻¹', 'k = rate ÷ conc² = mol dm⁻³ s⁻¹ ÷ mol² dm⁻⁶.', ['mol dm⁻³ s⁻¹', 's⁻¹', 'dm⁶ mol⁻² s⁻¹']),
         ('Which factor changes the value of the rate constant k for a reaction?', 'Temperature', 'k depends on temperature (and on a catalyst), not concentration.', ['Concentration of reactants', 'Volume of solution', 'Mass of reactants']),
         ('For rate = k[X], what happens to the rate when [X] is tripled?', 'The rate triples', 'First order: rate ∝ [X].', ['The rate is unchanged', 'The rate increases nine times', 'The rate doubles'])])
mcqs(t, [('For rate = k[A][B]², [A] is doubled and [B] is halved. What is the effect on the rate?', 'The rate halves', '2 × (½)² = ½.', ['The rate doubles', 'The rate is unchanged', 'The rate quarters']),
         ('Why can orders of reaction not be deduced from a balanced equation?', 'Orders depend on the mechanism (the rate-determining step), so must be found by experiment', 'The stoichiometric equation shows the overall change, not the steps.', ['Balanced equations are often wrong', 'Orders depend only on temperature', 'The coefficients always equal the orders'])], D=(2, 3), C='C2')
shorts(t, [('State the units of the rate constant for a reaction with rate = k[A]²[B].', 'dm⁶ mol⁻² s⁻¹', '[1]'),
           ('Define the term order of reaction with respect to a reactant.', 'The power to which the concentration of that reactant is raised in the experimentally determined rate equation.', '[1]')])
explain(t, [('Explain why a reactant can appear in the balanced equation but not in the rate equation.', 'It is zero order: it is not involved in the rate-determining step (it reacts in a fast step after the slow step), so changing its concentration does not affect the rate.', 'zero order [1]; not in rate-determining step [1] [2]'),
            ('Explain how the initial rate of a reaction is found from a concentration–time graph.', 'Draw a tangent to the curve at time zero and calculate its gradient (change in concentration ÷ change in time).', 'tangent at t = 0 [1]; gradient [1] [2]'),
            ('Explain why the units of k depend on the overall order of reaction.', 'k = rate ÷ (concentration terms); the rate always has units mol dm⁻³ s⁻¹, so the units of k depend on how many concentration terms are multiplied in the rate equation.', '[2]')])
myths(t, [('The order of reaction with respect to each reactant equals its coefficient in the balanced equation.', 'Orders can only be found by experiment; for example 2H₂ + 2NO → N₂ + 2H₂O has rate = k[NO]²[H₂].'),
          ('The rate constant increases when the concentration of a reactant is increased.', 'k is independent of concentration; it changes only with temperature (or a catalyst).'),
          ('A zero-order reactant is not used up in the reaction.', 'It is used up, but its concentration does not affect the rate because it is not in the rate-determining step.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def initial_rates(r, D):
    eqn, sp, od, exps, rates, kd = rates_table(r, D)
    tab = table_text(sp, exps, rates)
    n = sum(od)
    st = f'The initial rate of the reaction {eqn} was measured at constant temperature. Results: {tab}.'
    if D <= 2:
        i = r.randrange(len(sp))
        return MQ(r, st + f' What is the order of reaction with respect to {sp[i]}?', ORD_WORD[od[i]], [w for kk, w in ORD_WORD.items() if kk != od[i]] + ['third order'],
                  f'Compare experiments 1 and {i + 2}: [{sp[i]}] × {fx(exps[i + 1][i] / exps[0][i], 2)} gives rate × {fx(rates[i + 1] / rates[0], 3)}, so {ORD_WORD[od[i]]}.')
    ords = '; '.join(f'{ORD_WORD[o]} in {s}' for s, o in zip(sp, od))
    ask = 'Deduce the order with respect to each reactant and write the rate equation.'
    key = f'orders: {ords} [{len(sp)}]; {rate_eq(sp, od)} [1]'
    ans = f'{ords}; {rate_eq(sp, od)}'
    tot = len(sp) + 1
    if D >= 4:
        ask += ' Calculate the rate constant, k, and give its units.'
        key += f'; k = {nice(rates[0])} ÷ ({" × ".join(fx(c, 4) + ("²" if o == 2 else "") for c, o in zip(exps[0], od) if o) or "1"}) = {nice(kd)} {k_units(n)} [1]; units [1]'
        ans += f'; k = {nice(kd)} {k_units(n)}'
        tot += 2
    if D >= 5:
        newc = [r.choice([0.015, 0.030, 0.040, 0.060, 0.080]) for _ in sp]
        nr = kd * math.prod(c ** o for c, o in zip(newc, od))
        ask += ' Calculate the initial rate when ' + ' and '.join(f'[{s}] = {fx(c, 3)} mol dm⁻³' for s, c in zip(sp, newc)) + '.'
        key += f'; rate = {nice(kd)} × ... = {nice(nr)} mol dm⁻³ s⁻¹ [1]'
        ans += f'; new rate = {nice(nr)} mol dm⁻³ s⁻¹'
        tot += 1
    return Q(st + ' ' + ask, ans, key + f' [{tot}]', 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def k_units_q(r, D):
    sp = r.choice([['A', 'B'], ['NO', 'O₂'], ['H₂O₂', 'I⁻'], ['C₄H₉Br', 'OH⁻'], ['X', 'Y'], ['S₂O₈²⁻', 'I⁻']])
    od = r.choice([[1, 0], [1, 1], [2, 0], [2, 1], [1, 2], [0, 0], [0, 1]])
    n = sum(od)
    eq = rate_eq(sp, od)
    if D <= 2:
        return MQ(r, f'For a reaction with {eq}, what are the units of k?', k_units(n), [k_units(x) for x in range(5) if x != n][:3] if n < 4 else [k_units(x) for x in (0, 1, 2)], f'Overall order {n}; k = rate ÷ concentration terms.')
    f = r.choice([2, 3, 0.5])
    nz = [j for j in range(2) if od[j]]
    if not nz:
        return None
    i = r.choice(nz)
    fac = f ** od[i]
    st = f'A reaction has {eq}. State the overall order, deduce the units of k, and state the factor by which the rate changes when [{sp[i]}] is multiplied by {fx(f, 1)} at constant temperature.'
    return Q(st, f'overall order {n}; units {k_units(n)}; rate × {fx(fac, 3)}', f'order {n} [1]; units {k_units(n)} [1]; factor {fx(fac, 3)} [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def rates_case(r, D):
    eqn, sp, od, exps, rates, kd = rates_table(r, 3)
    n = sum(od)
    method = r.choice(['colorimetry, measuring the absorbance of the solution at regular intervals', 'a clock-reaction method, timing how long a fixed amount of product takes to form',
                       'measuring the volume of gas produced at regular intervals', 'withdrawing samples, quenching them and titrating'])
    st = f'{who(r)} investigated the reaction {eqn} in {lab(r)} using {method}. Results: {table_text(sp, exps, rates)}.'
    ords = '; '.join(f'{ORD_WORD[o]} in {s}' for s, o in zip(sp, od))
    zero = [s for s, o in zip(sp, od) if o == 0]
    parts = [P_('Deduce the order of reaction with respect to each reactant, explaining your reasoning.', ords, f'each order with comparison of experiments [{len(sp)}]'),
             P_('Write the rate equation and calculate the rate constant, k, with its units.', f'{rate_eq(sp, od)}; k = {nice(kd)} {k_units(n)}', f'rate equation [1]; value of k [1]; units {k_units(n)} [1] [3]'),
             P_('Explain why it is the initial rate that is measured in each experiment.', 'At the start the concentrations are known exactly (equal to the values mixed) and the products have not yet affected the rate.', '[1]'),
             P_('State and explain the effect on k of carrying out the experiments at a higher temperature.', 'k increases, because a greater proportion of collisions have energy ≥ Ea, so the rate increases at the same concentrations.', 'k increases [1]; reason [1] [2]')]
    if zero:
        parts.append(P_(f'Explain why {zero[0]} does not appear in the rate equation even though it is a reactant.', f'{zero[0]} is not involved in the rate-determining step; it reacts in a fast step after the slow step.', '[2]'))
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how the initial-rates method is used to determine the rate equation for a reaction, and explain how the rate constant and its units are obtained.', 'Several experiments, changing the concentration of one reactant at a time with others constant and temperature constant; measure initial rate (tangent at t = 0 or clock method); compare ratios to deduce orders (0, 1, 2); write rate = k[A]ᵐ[B]ⁿ; substitute values to calculate k; units from overall order; k depends on temperature.',
           'controlled variables [1]; initial rate measurement [1]; deducing orders from ratios [2]; rate equation [1]; k and units [2] [7]')])
t4a = t

# ---------------------------------------------------------------------
HL_RX = [('the decomposition of dinitrogen pentoxide, 2N₂O₅(g) → 4NO₂(g) + O₂(g)', 'N₂O₅', (2.0e-4, 8.0e-4)),
         ('the decomposition of hydrogen peroxide catalysed by manganese(IV) oxide', 'H₂O₂', (5.0e-4, 3.0e-3)),
         ('the isomerisation of cyclopropane to propene', 'cyclopropane', (5.0e-5, 6.0e-4)),
         ('the acid-catalysed hydrolysis of sucrose', 'sucrose', (1.0e-4, 6.0e-4)),
         ('the hydrolysis of 2-bromo-2-methylpropane', '(CH₃)₃CBr', (2.0e-3, 1.0e-2)),
         ('the decomposition of benzenediazonium chloride in warm water', 'C₆H₅N₂⁺', (1.0e-3, 5.0e-3)),
         ('the hydrolysis of methyl ethanoate in excess dilute acid', 'CH₃COOCH₃', (1.0e-4, 8.0e-4))]

t = T('Determining order from concentration–time and rate–concentration graphs; half-life', 'determining order from concentration–time')
facts(t, [('half-life', 't½: the time taken for the concentration of a reactant to fall to half of its initial value'),
          ('first-order reaction', 'a reaction whose rate is directly proportional to the concentration of one reactant; it has a constant half-life'),
          ('zero-order reaction', 'a reaction whose rate does not depend on the concentration of the reactant; its concentration–time graph is a straight line'),
          ('second-order reaction', 'a reaction whose rate is proportional to the square of the concentration of a reactant; its half-life increases as the reaction proceeds'),
          ('tangent', 'a straight line touching a curve at one point, whose gradient gives the rate at that time')])
mcqs(t, [('What is the shape of a rate–concentration graph for a first-order reactant?', 'A straight line through the origin', 'Rate ∝ [A].', ['A horizontal straight line', 'An upward curve', 'A downward curve']),
         ('What is the shape of a rate–concentration graph for a zero-order reactant?', 'A horizontal straight line', 'Rate is independent of [A].', ['A straight line through the origin', 'An upward curve', 'A straight line with negative gradient']),
         ('What is the shape of a concentration–time graph for a zero-order reactant?', 'A straight line with negative gradient', 'Constant rate.', ['A curve with constant half-life', 'A horizontal straight line', 'A curve with increasing gradient']),
         ('Which equation links the half-life and rate constant of a first-order reaction?', 'k = 0.693 ÷ t½', 'k = ln 2 / t½.', ['k = t½ ÷ 0.693', 'k = 0.693 × t½', 'k = 2 ÷ t½'])])
mcqs(t, [('A concentration–time graph shows successive half-lives of 40 s, 80 s and 160 s. What is the order with respect to the reactant?', 'Second order', 'Half-life doubles as concentration halves: second order.', ['First order', 'Zero order', 'Third order']),
         ('A concentration–time graph shows successive half-lives of 25 s, 25 s and 25 s. What is the order with respect to the reactant?', 'First order', 'Constant half-life: first order.', ['Zero order', 'Second order', 'Third order']),
         ('A rate–concentration graph is an upward curve, and rate ÷ [A]² is constant. What is the order with respect to A?', 'Second order', 'Rate ∝ [A]².', ['First order', 'Zero order', 'Half order'])], D=(2, 3), C='C2')
shorts(t, [('State how the half-life of a first-order reaction depends on the initial concentration.', 'It is independent of initial concentration (constant).', '[1]'),
           ('Sketch-describe the rate–concentration graph for a second-order reactant.', 'An upward curve (parabola) through the origin: rate ∝ [A]².', '[1]')])
explain(t, [('Explain how a concentration–time graph can be used to show that a reaction is first order.', 'Measure two or more successive half-lives from the graph; if they are constant, the reaction is first order.', 'successive half-lives [1]; constant [1] [2]'),
            ('Explain how a rate–concentration graph is drawn from a concentration–time graph.', 'Draw tangents to the concentration–time curve at several times; the gradient of each tangent gives the rate at that concentration; plot rate against concentration.', 'tangents [1]; gradients = rate [1]; plot rate v. concentration [1] [3]'),
            ('Explain why the half-life of a zero-order reaction decreases as the reaction proceeds.', 'The rate is constant, so the time to remove half of a smaller amount of reactant is shorter.', '[2]')])
myths(t, [('A first-order reaction takes twice as long to go to 25% as to 50% of the starting concentration because the rate is constant.', 'It does take two half-lives, but because the half-life is constant, not because the rate is constant; the rate falls as the concentration falls.'),
          ('All reactions have a constant half-life.', 'Only first-order reactions have a constant half-life; for zero order it decreases and for second order it increases.'),
          ('The initial rate is the average rate over the whole experiment.', 'The initial rate is the gradient of the tangent at time zero.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def half_life(r, D):
    desc, sp, (lo, hi) = r.choice(HL_RX)
    th = float(f'{0.693 / (lo * (hi / lo) ** r.random()):.2g}')
    k = 0.693 / th
    mode = r.choice(['k', 't', 'frac', 'time']) if D >= 3 else r.choice(['k', 't'])
    if mode == 'k':
        st = f'The half-life of {desc} at a certain temperature is {sf(th, 2)} s. The reaction is first order with respect to {sp}. Calculate the rate constant, k.'
        key = f'k = 0.693 ÷ t½ [1] = 0.693 ÷ {sf(th, 2)} = {sci(k, 3)} s⁻¹ [1] [2]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the rate constant, k.', 'What is the rate constant, k?'), k, [th / 0.693, 0.693 * th, 1 / th, 2 / th], ' s⁻¹', key, f=lambda v: sci(v, 3))
        ans = f'{sci(k, 3)} s⁻¹'
    elif mode == 't':
        kk = float(f'{k:.3g}')
        st = f'{cap(desc)} is first order with respect to {sp}, with k = {sci(kk, 3)} s⁻¹. Calculate the half-life.'
        key = f't½ = 0.693 ÷ k [1] = {sf(0.693 / kk, 3)} s [1] [2]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the half-life.', 'What is the half-life?'), 0.693 / kk, [kk / 0.693, 1 / kk, 0.5 / kk, 2 * 0.693 / kk], ' s', key)
        ans = f'{sf(0.693 / kk, 3)} s'
    elif mode == 'frac':
        c0 = r.choice([0.80, 0.64, 0.40, 0.25, 0.120, 0.050])
        nh = r.choice([2, 3, 4, 5])
        st = f'In {desc}, the initial concentration of {sp} is {fx(c0, 3)} mol dm⁻³ and the half-life is {sf(th, 2)} s. Calculate the concentration of {sp} after {sf(nh * th, 3)} s.'
        key = f'{sf(nh * th, 3)} s = {nh} half-lives [1]; [{sp}] = {fx(c0, 3)} ÷ 2{sup(nh)} = {g3(c0 / 2 ** nh)} mol dm⁻³ [1] [2]'
        ans = f'{g3(c0 / 2 ** nh)} mol dm⁻³'
    else:
        pc = r.choice([(25, 2), (12.5, 3), (6.25, 4), (3.125, 5)])
        st = f'{cap(desc)} is first order with respect to {sp}, with half-life {sf(th, 2)} s. Calculate the time taken for the concentration of {sp} to fall to {fx(pc[0], 3)}% of its initial value.'
        key = f'{fx(pc[0], 3)}% = {pc[1]} half-lives [1]; time = {pc[1]} × {sf(th, 2)} = {sf(pc[1] * th, 3)} s [1] [2]'
        ans = f'{sf(pc[1] * th, 3)} s'
    if D >= 5:
        c0 = r.choice([0.050, 0.10, 0.20, 0.40])
        st += f' Hence calculate the initial rate of reaction when [{sp}] = {fx(c0, 2)} mol dm⁻³.'
        key = key.rsplit(' [', 1)[0] + f'; k = {sci(k, 3)} s⁻¹; rate = k[{sp}] = {sci(k * c0, 3)} mol dm⁻³ s⁻¹ [2] [4]'
        ans += f'; initial rate = {sci(k * c0, 3)} mol dm⁻³ s⁻¹'
    return Q(st, ans, key, 'numerical')


@t.add('C3', (2, 3, 4, 5), 'short')
def conc_time(r, D):
    o = r.choice([0, 1, 2])
    c0 = r.choice([0.80, 0.64, 1.00, 0.48])
    dt = r.choice([10, 20, 30, 50, 60, 100])
    if o == 0:
        k = c0 / r.choice([6, 8, 10]) / dt
        cs = [c0 - k * dt * i for i in range(5)]
    elif o == 1:
        h = r.choice([1, 2])  # half-lives per interval /2
        k = 0.693 / (dt * h)
        cs = [c0 * math.exp(-k * dt * i) for i in range(7)]
    else:
        k = 1 / (c0 * dt * 2)
        cs = [1 / (1 / c0 + k * dt * i) for i in range(7)]
    sp = r.choice(['A', 'X', 'the ester', 'the halogenoalkane', 'N₂O₅', 'H₂O₂'])
    data = ', '.join(f't = {dt * i} s: {g3(c)}' for i, c in enumerate(cs))
    st = f'The concentration of {sp} (mol dm⁻³) was measured during a reaction at constant temperature: {data}.'
    why = {0: 'concentration falls by the same amount in each time interval (constant rate, straight-line graph)', 1: f'the half-life is constant ({sf(0.693 / k, 3)} s)', 2: 'successive half-lives double (half-life increases as concentration falls)'}[o]
    if D <= 2:
        return MQ(r, st + f' What is the order of reaction with respect to {sp}?', ORD_WORD[o], [w for kk, w in ORD_WORD.items() if kk != o] + ['third order'], f'{cap(ORD_WORD[o])}: {why}.')
    ask = f' Deduce the order of reaction with respect to {sp}. Explain your answer.'
    key = f'{ORD_WORD[o]} [1]; {why} [1]'
    ans = f'{cap(ORD_WORD[o])}: {why}.'
    tot = 2
    if D >= 4 and o in (0, 1):
        ask += ' Calculate the rate constant, including units.'
        if o == 0:
            key += f'; k = gradient = {g3(k * dt)} ÷ {dt} = {sci(k, 3)} mol dm⁻³ s⁻¹ [2]'
            ans += f' k = {sci(k, 3)} mol dm⁻³ s⁻¹.'
        else:
            key += f'; k = 0.693 ÷ {sf(0.693 / k, 3)} = {sci(k, 3)} s⁻¹ [2]'
            ans += f' k = {sci(k, 3)} s⁻¹.'
        tot += 2
    return Q(st + ask, ans, key + f' [{tot}]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def hl_case(r, D):
    desc, sp, (lo, hi) = r.choice(HL_RX)
    th = float(f'{0.693 / (lo * (hi / lo) ** r.random()):.2g}')
    k = 0.693 / th
    c0 = r.choice([0.20, 0.40, 0.80])
    st = f'{who(r)} followed {desc} at 300 K. A graph of [{sp}] against time was a curve; the concentration fell from {fx(c0, 2)} to {fx(c0 / 2, 2)} mol dm⁻³ in {sf(th, 2)} s and from {fx(c0 / 2, 2)} to {fx(c0 / 4, 3)} mol dm⁻³ in a further {sf(th, 2)} s.'
    parts = [P_(f'Deduce the order of reaction with respect to {sp}. Explain your answer.', 'First order: the half-life is constant.', 'first order [1]; constant half-life [1] [2]'),
             P_('Calculate the rate constant, k, and give its units.', f'{sci(k, 3)} s⁻¹', f'k = 0.693 ÷ {sf(th, 2)} [1] = {sci(k, 3)} [1]; s⁻¹ [1] [3]'),
             P_(f'Calculate the initial rate of reaction when [{sp}] = {fx(c0, 2)} mol dm⁻³.', f'{sci(k * c0, 3)} mol dm⁻³ s⁻¹', f'rate = k[{sp}] = {sci(k, 3)} × {fx(c0, 2)} = {sci(k * c0, 3)} [1]'),
             P_('Describe how the initial rate could be found directly from the concentration–time graph.', 'Draw a tangent to the curve at t = 0 and calculate its gradient.', '[2]'),
             P_('Sketch-describe the rate–concentration graph you would expect for this reaction.', 'A straight line through the origin, gradient = k.', 'straight line through origin [1]; gradient k [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how graphs of concentration against time and of rate against concentration are used to determine the order of reaction with respect to a reactant.', 'Concentration–time: zero order straight line, first order curve with constant half-life, second order curve with increasing half-life; tangents give rates; rate–concentration: zero order horizontal, first order straight line through origin, second order upward curve; k from half-life (k = 0.693/t½) or gradient.',
           'concentration–time shapes [2]; half-life test [1]; tangents [1]; rate–concentration shapes [2]; k from graph [1] [7]')])
t4b = t

# ---------------------------------------------------------------------
MECH = [  # overall, rate eq, steps [(eq, speed)], intermediate
    ('2NO₂(g) + F₂(g) → 2NO₂F(g)', 'rate = k[NO₂][F₂]', [('NO₂ + F₂ → NO₂F + F', 'slow'), ('NO₂ + F → NO₂F', 'fast')], 'F'),
    ('NO₂(g) + CO(g) → NO(g) + CO₂(g)', 'rate = k[NO₂]²', [('2NO₂ → NO₃ + NO', 'slow'), ('NO₃ + CO → NO₂ + CO₂', 'fast')], 'NO₃'),
    ('(CH₃)₃CBr + OH⁻ → (CH₃)₃COH + Br⁻', 'rate = k[(CH₃)₃CBr]', [('(CH₃)₃CBr → (CH₃)₃C⁺ + Br⁻', 'slow'), ('(CH₃)₃C⁺ + OH⁻ → (CH₃)₃COH', 'fast')], '(CH₃)₃C⁺'),
    ('H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O', 'rate = k[H₂O₂][I⁻]', [('H₂O₂ + I⁻ → IO⁻ + H₂O', 'slow'), ('IO⁻ + 2H⁺ + I⁻ → I₂ + H₂O', 'fast')], 'IO⁻'),
    ('2H₂(g) + 2NO(g) → N₂(g) + 2H₂O(g)', 'rate = k[NO]²[H₂]', [('2NO + H₂ → N₂ + H₂O₂', 'slow'), ('H₂O₂ + H₂ → 2H₂O', 'fast')], 'H₂O₂'),
    ('2N₂O₅(g) → 4NO₂(g) + O₂(g)', 'rate = k[N₂O₅]', [('N₂O₅ → NO₂ + NO₃', 'slow'), ('NO₂ + NO₃ → NO + NO₂ + O₂', 'fast'), ('NO + NO₃ → 2NO₂', 'fast')], 'NO₃'),
    ('CH₃COCH₃ + I₂ → CH₃COCH₂I + HI (H⁺ catalyst)', 'rate = k[CH₃COCH₃][H⁺]', [('CH₃COCH₃ + H⁺ → CH₃C(OH⁺)CH₃', 'fast'), ('CH₃C(OH⁺)CH₃ → CH₃C(OH)=CH₂ + H⁺', 'slow'), ('CH₃C(OH)=CH₂ + I₂ → CH₃COCH₂I + HI', 'fast')], 'CH₃C(OH)=CH₂'),
    ('2NO(g) + Br₂(g) → 2NOBr(g)', 'rate = k[NO][Br₂]', [('NO + Br₂ → NOBr₂', 'slow'), ('NOBr₂ + NO → 2NOBr', 'fast')], 'NOBr₂'),
    ('2ICl(g) + H₂(g) → I₂(g) + 2HCl(g)', 'rate = k[ICl][H₂]', [('ICl + H₂ → HI + HCl', 'slow'), ('HI + ICl → I₂ + HCl', 'fast')], 'HI'),
    ('O₃(g) + NO(g) → O₂(g) + NO₂(g)', 'rate = k[O₃][NO]', [('O₃ + NO → O₂ + NO₂', 'slow (single step)')], None)]

t = T('Rate-determining step and deducing mechanisms from rate equations', 'rate-determining step')
facts(t, [('rate-determining step', 'the slowest step in a reaction mechanism, which limits the overall rate of reaction'),
          ('intermediate', 'a species formed in one step of a mechanism and used up in a later step; it does not appear in the overall equation'),
          ('reaction mechanism', 'the sequence of elementary steps by which a reaction takes place'),
          ('elementary step', 'a single step in a mechanism involving the collision or breakdown of one, two or (rarely) three particles'),
          ('molecularity', 'the number of particles that take part in an elementary step')])
mcqs(t, [('Which species appear in the rate equation?', 'Those involved in the rate-determining step (or in steps before it)', 'The slow step controls the rate.', ['All species in the balanced equation', 'Only the products', 'Only the catalyst']),
         ('In an SN1 mechanism, the rate-determining step is', 'the heterolytic breaking of the C–halogen bond to form a carbocation', 'Rate = k[RX].', ['the attack of the nucleophile on the carbocation', 'the formation of a transition state containing OH and Br', 'the loss of H⁺']),
         ('The rate equation for the hydrolysis of bromoethane is rate = k[CH₃CH₂Br][OH⁻]. This is consistent with', 'a one-step SN2 mechanism', 'Both species in the single (rate-determining) step.', ['an SN1 mechanism', 'a free-radical mechanism', 'an electrophilic addition mechanism'])])
mcqs(t, [('For 2A + B → C, rate = k[A]². Which could be the rate-determining step?', '2A → A₂', 'Two A particles in the slow step; B reacts later.', ['A + B → AB', 'A₂ + B → C', 'B → B*']),
         ('A catalyst appears in the rate equation but not in the overall equation. Why?', 'It takes part in the rate-determining step but is regenerated later', 'Catalysts are used and reformed.', ['It is a product of the reaction', 'It is an intermediate', 'It changes the equilibrium constant']),
         ('Which statement about an intermediate is correct?', 'It is formed in one step and used up in a later step', 'Does not appear in overall equation.', ['It is the same as a transition state', 'It appears in the overall equation', 'It is a catalyst'])], D=(2, 3), C='C2')
shorts(t, [('State what is meant by the rate-determining step.', 'The slowest step in the mechanism, which controls the overall rate.', '[1]'),
           ('Define the term intermediate in a reaction mechanism.', 'A species formed in one step and used up in a later step of the mechanism.', '[1]')])
explain(t, [('Explain why the rate equation for the hydrolysis of 2-bromo-2-methylpropane does not include [OH⁻].', 'The rate-determining step is the slow ionisation of (CH₃)₃CBr to a carbocation; OH⁻ reacts in a fast later step, so it is zero order (SN1).', 'slow step is ionisation [1]; OH⁻ in fast step [1] [2]'),
            ('Explain why the overall order of reaction is related to the number of particles in the rate-determining step.', 'The rate depends on the frequency of the slow step; the species (and numbers of each) that collide in this step appear in the rate equation with powers equal to their numbers.', '[2]'),
            ('Explain the difference between an intermediate and a transition state.', 'An intermediate is a real species with a finite lifetime, formed and used up (energy minimum between steps); a transition state is the highest-energy arrangement during a step and cannot be isolated (energy maximum).', 'intermediate described [1]; transition state described [1] [2]')])
myths(t, [('The rate-determining step is always the first step of a mechanism.', 'It is the slowest step, which may come after a fast step; species in earlier fast steps can also appear in the rate equation.'),
          ('An intermediate is the same as a transition state.', 'An intermediate can be isolated (energy minimum); a transition state is an energy maximum.'),
          ('If a species appears in the overall equation, it must appear in the rate equation.', 'Only species in (or before) the rate-determining step appear; others are zero order.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def mech_q(r, D):
    ov, req, steps, inter = r.choice(MECH)
    if len(steps) < 2:
        return None
    stx = '; '.join(f'step {i + 1}: {s}' for i, (s, _) in enumerate(steps))
    slow = [i for i, (_, sp) in enumerate(steps) if sp.startswith('slow')][0]
    st = f'The reaction {ov} has the rate equation {req}. A proposed mechanism is: {stx}.'
    if D <= 2:
        return MQ(r, st + ' Which step is the rate-determining step?', f'Step {slow + 1}', [f'Step {i + 1}' for i in range(len(steps)) if i != slow] + ['All steps are equally fast', 'None of the steps'], f'Step {slow + 1} contains the species (in the ratio) shown in the rate equation.')
    ask = ' Identify the rate-determining step and the intermediate, explaining your answers.'
    key = f'step {slow + 1} is rate-determining [1]; its species match the rate equation [1]; intermediate {inter} [1]; formed then used up / not in overall equation [1]'
    ans = f'Step {slow + 1} (matches the rate equation); intermediate {inter}, formed in one step and used in another.'
    tot = 4
    if D >= 4:
        ask += ' Show that the steps add up to the overall equation.'
        key += '; steps summed with intermediates cancelling [1]'
        ans += ' Adding the steps and cancelling intermediates gives the overall equation.'
        tot += 1
    return Q(st + ask, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'short')
def mech_choose(r, D):
    ov, req, steps, inter = r.choice([m_ for m_ in MECH if len(m_[2]) == 2])
    slow = [s for s, sp in steps if sp == 'slow'][0]
    other = [s for s, sp in steps if sp != 'slow'][0]
    st = f'For the reaction {ov}, the rate equation found by experiment is {req}.'
    if D <= 3:
        return MQ(r, st + ' Which equation could represent the rate-determining step?', slow, [other, re.sub(r'\((g|aq|l|s)\)', '', ov.split(' (H⁺')[0]), 'a step involving only the products'], f'The slow step must contain exactly the species in the rate equation: {slow}.')
    return Q(st + ' Suggest a two-step mechanism for this reaction that is consistent with the rate equation. State which step is slow.', f'{slow} (slow); {other} (fast)',
             'slow step containing the species in the rate equation [1]; second step uses the intermediate [1]; steps sum to the overall equation [1]; slow step identified [1] [4]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def mech_case(r, D):
    hal = r.choice([('2-bromo-2-methylpropane', '(CH₃)₃CBr', 'tertiary', 'SN1', 'rate = k[(CH₃)₃CBr]'), ('bromoethane', 'CH₃CH₂Br', 'primary', 'SN2', 'rate = k[CH₃CH₂Br][OH⁻]'),
                    ('2-chloro-2-methylbutane', 'CH₃CH₂C(CH₃)₂Cl', 'tertiary', 'SN1', 'rate = k[CH₃CH₂C(CH₃)₂Cl]'), ('1-bromobutane', 'CH₃CH₂CH₂CH₂Br', 'primary', 'SN2', 'rate = k[CH₃CH₂CH₂CH₂Br][OH⁻]')])
    nm, fm, cls, mech, req = hal
    f = r.choice([2, 3])
    st = f'{who(r)} studied the hydrolysis of {nm}, {fm}, by aqueous hydroxide ions. Doubling [{fm}] doubled the rate; multiplying [OH⁻] by {f} ' + ('had no effect on the rate.' if mech == 'SN1' else f'multiplied the rate by {f}.')
    parts = [P_('Deduce the rate equation.', req, '[2]'),
             P_('Name the mechanism and explain how the rate equation supports it.', f'{mech}: ' + ('only the halogenoalkane is in the slow step (ionisation to a carbocation)' if mech == 'SN1' else 'both the halogenoalkane and OH⁻ collide in a single step'), 'mechanism named [1]; link to species in slow step [1] [2]'),
             P_('Describe the mechanism, including the rate-determining step.', ('Slow: C–Br bond breaks heterolytically to give a tertiary carbocation and Br⁻; fast: OH⁻ attacks the carbocation.' if mech == 'SN1' else 'One step: OH⁻ lone pair attacks δ+ carbon from the side opposite the halogen; transition state with partial bonds; C–Br bond breaks, Br⁻ leaves.'), 'step 1 [1]; step 2 / transition state [1]; curly arrows / dipole described [1] [3]'),
             P_(f'Explain why {cls} halogenoalkanes tend to react by this mechanism.', ('Tertiary carbocations are stabilised by the positive inductive effect of three alkyl groups, and the alkyl groups hinder backside attack.' if cls == 'tertiary' else 'Primary carbocations are unstable, and there is little steric hindrance to attack by the nucleophile.'), '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how the rate equation for a reaction gives information about its mechanism, using the hydrolysis of halogenoalkanes and one other reaction as examples.', 'Rate equation shows the species in the rate-determining step; orders give numbers of each; zero-order species react after the slow step; SN1 (tertiary): rate = k[RX], slow ionisation then fast attack; SN2 (primary): rate = k[RX][OH⁻], single step; another example such as NO₂ + CO, rate = k[NO₂]², slow step 2NO₂ → NO₃ + NO; intermediates and summing steps.',
           'principle [2]; SN1 [1]; SN2 [1]; second example with steps [2]; intermediate / steps sum [1] [7]')])
t4c = t

# ---------------------------------------------------------------------
CATS = [('the Haber process, N₂ + 3H₂ ⇌ 2NH₃', 'iron', 'heterogeneous'), ('the Contact process, 2SO₂ + O₂ ⇌ 2SO₃', 'vanadium(V) oxide', 'heterogeneous'),
        ('catalytic converters, 2CO + 2NO → 2CO₂ + N₂', 'platinum / rhodium', 'heterogeneous'), ('hydrogenation of alkenes', 'nickel', 'heterogeneous'),
        ('the reaction between S₂O₈²⁻ and I⁻ ions', 'Fe²⁺ / Fe³⁺ ions', 'homogeneous'), ('atmospheric oxidation of SO₂', 'nitrogen dioxide', 'homogeneous'),
        ('esterification of ethanoic acid with ethanol', 'H⁺ ions (concentrated sulfuric acid)', 'homogeneous'), ('the reaction of MnO₄⁻ with ethanedioate ions', 'Mn²⁺ ions (autocatalysis)', 'homogeneous'),
        ('decomposition of hydrogen peroxide', 'manganese(IV) oxide', 'heterogeneous'), ('cracking of long-chain alkanes', 'zeolite (aluminosilicate)', 'heterogeneous')]

t = T('Homogeneous and heterogeneous catalysis; effect of temperature on k and Arrhenius equation', 'homogeneous and heterogeneous catalysis')
facts(t, [('homogeneous catalyst', 'a catalyst in the same phase as the reactants'),
          ('heterogeneous catalyst', 'a catalyst in a different phase from the reactants, usually a solid with gaseous or liquid reactants'),
          ('adsorption', 'the formation of weak bonds between reactant molecules and active sites on the surface of a solid catalyst'),
          ('activation energy', 'Ea: the minimum energy that colliding particles must have for a reaction to occur'),
          ('Arrhenius equation', 'k = Ae^(−Ea/RT), linking the rate constant to activation energy and temperature'),
          ('autocatalysis', 'catalysis of a reaction by one of its own products')])
mcqs(t, [('Which is a homogeneous catalyst?', 'Fe²⁺ ions in the reaction between S₂O₈²⁻ and I⁻ ions', 'All in aqueous solution.', ['Iron in the Haber process', 'V₂O₅ in the Contact process', 'Nickel in hydrogenation']),
         ('In heterogeneous catalysis, which is the correct order of steps?', 'Adsorption, reaction, desorption', 'Reactants adsorb, bonds weaken and react, products desorb.', ['Desorption, reaction, adsorption', 'Reaction, adsorption, desorption', 'Adsorption, desorption, reaction']),
         ('According to the Arrhenius equation, a plot of ln k against 1/T gives a straight line with gradient', '−Ea/R', 'ln k = ln A − Ea/RT.', ['Ea/R', '−R/Ea', 'ln A']),
         ('Why does a small temperature increase cause a large increase in rate?', 'The fraction of molecules with energy ≥ Ea increases greatly', 'Boltzmann distribution shifts.', ['Collision frequency doubles', 'Ea decreases', 'The rate constant becomes smaller'])])
mcqs(t, [('Why does Fe²⁺ catalyse the reaction between S₂O₈²⁻ and I⁻?', 'Each step involves oppositely charged ions, so Ea is lower than for two negative ions colliding', 'S₂O₈²⁻ + 2Fe²⁺ then 2Fe³⁺ + 2I⁻.', ['Fe²⁺ adsorbs I⁻ on its surface', 'Fe²⁺ increases the temperature', 'Fe²⁺ shifts the equilibrium']),
         ('A catalyst increases the rate constant k because it', 'provides a route with lower activation energy', 'Ea appears in the exponent of the Arrhenius equation.', ['increases the temperature', 'increases the concentrations', 'increases the enthalpy change']),
         ('Why is the catalyst in a catalytic converter spread thinly on a ceramic honeycomb?', 'To give a large surface area with a small mass of expensive metal', 'More active sites per gram of Pt/Rh.', ['To stop the catalyst being adsorbed', 'To make the reaction homogeneous', 'To increase the activation energy'])], D=(2, 3), C='C2')
shorts(t, [('Write the two equations to show how Fe²⁺ ions catalyse the reaction between S₂O₈²⁻ and I⁻ ions.', 'S₂O₈²⁻ + 2Fe²⁺ → 2SO₄²⁻ + 2Fe³⁺; 2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂', 'each equation [1] [2]'),
           ('Write two equations to show how NO₂ catalyses the oxidation of SO₂ in the atmosphere.', 'SO₂ + NO₂ → SO₃ + NO; NO + ½O₂ → NO₂', 'each equation [1] [2]')])
explain(t, [('Explain how iron acts as a heterogeneous catalyst in the Haber process.', 'N₂ and H₂ are adsorbed onto active sites on the iron surface; bonds within the molecules are weakened and the reactants are held close together in a favourable orientation; NH₃ forms and desorbs, freeing the sites.', 'adsorption [1]; bonds weakened / orientation [1]; desorption [1] [3]'),
            ('Explain why the reaction between S₂O₈²⁻ and I⁻ ions is slow without a catalyst.', 'Both ions are negatively charged, so they repel; collisions with enough energy are rare (high Ea).', '[2]'),
            ('Explain, in terms of the Arrhenius equation, why increasing temperature increases the rate constant.', 'k = Ae^(−Ea/RT); as T increases, −Ea/RT becomes less negative so e^(−Ea/RT), the fraction of collisions with E ≥ Ea, increases.', 'exponent less negative [1]; larger fraction with E ≥ Ea [1] [2]'),
            ('Explain why catalysts can be poisoned.', 'Impurities (e.g. sulfur, lead) adsorb strongly onto the active sites and do not desorb, blocking them so reactants cannot be adsorbed.', '[2]')])
myths(t, [('A catalyst increases the rate by increasing the energy of the particles.', 'A catalyst provides an alternative route with a lower activation energy; the energy distribution of the particles is unchanged.'),
          ('In heterogeneous catalysis, the strongest-adsorbing catalyst is always best.', 'If adsorption is too strong the products do not desorb; a good catalyst adsorbs strongly enough to weaken bonds but weakly enough to release the products.'),
          ('Increasing the temperature lowers the activation energy.', 'Ea is unchanged; a higher temperature increases the proportion of particles with energy ≥ Ea.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def arrhenius(r, D):
    Ea = r.choice([45, 52, 60, 68, 75, 84, 92, 105, 120]) * 1000
    T1 = r.choice([288, 293, 298, 303, 310, 320])
    T2 = T1 + r.choice([10, 15, 20, 25, 30, 40])
    k1 = float(f'{r.choice([1.2, 2.5, 3.6, 4.8, 6.2, 8.5]) * 10 ** r.randint(-5, -1):.2g}')
    k2 = k1 * math.exp(-Ea / RGAS * (1 / T2 - 1 / T1))
    k2r = float(f'{k2:.3g}')
    ctx = r.choice(['the hydrolysis of methyl ethanoate in excess acid', 'the isomerisation of cyclopropane', 'the hydrolysis of 2-bromo-2-methylpropane', 'the acid-catalysed hydrolysis of sucrose', 'the decomposition of N₂O₅', 'the decomposition of benzenediazonium ions in water'])
    mode = r.choice(['Ea', 'k2', 'graph']) if D >= 4 else 'Ea' if D >= 3 else r.choice(['Ea', 'k2'])
    if mode == 'Ea':
        Eac = RGAS * math.log(k2r / k1) / (1 / T1 - 1 / T2)
        st = f'For {ctx}, k = {sci(k1, 2)} s⁻¹ at {T1} K and {nice(k2r)} s⁻¹ at {T2} K. Use the Arrhenius equation, ln k = ln A − Ea/RT, to calculate the activation energy in kJ mol⁻¹. (R = 8.31 J K⁻¹ mol⁻¹)'
        key = f'ln(k₂/k₁) = (Ea/R)(1/T₁ − 1/T₂) [1]; ln({g3(k2r / k1)}) = {g3(math.log(k2r / k1))} and 1/T₁ − 1/T₂ = {sci(1 / T1 - 1 / T2, 3)} [1]; Ea = {g3(Eac / 1000)} kJ mol⁻¹ [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Use the Arrhenius equation, ln k = ln A − Ea/RT, to calculate', 'Using ln k = ln A − Ea/RT, what is').replace('in kJ mol⁻¹.', 'in kJ mol⁻¹?'), Eac / 1000, [Eac / 1000 / 2.303, Eac / 1000 * 2, RGAS * (k2r / k1) / (1 / T1 - 1 / T2) / 1000, Eac / 1000 / 8.31], ' kJ mol⁻¹', key)
        return Q(st, f'{g3(Eac / 1000)} kJ mol⁻¹', key, 'numerical')
    if mode == 'k2':
        st = f'For {ctx}, Ea = {Ea // 1000} kJ mol⁻¹ and k = {sci(k1, 2)} s⁻¹ at {T1} K. Calculate k at {T2} K. (R = 8.31 J K⁻¹ mol⁻¹)'
        key = f'ln(k₂/k₁) = (Ea/R)(1/T₁ − 1/T₂) = {g3(Ea / RGAS * (1 / T1 - 1 / T2))} [1]; k₂/k₁ = {g3(k2 / k1)} [1]; k₂ = {sci(k2, 3)} s⁻¹ [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate k', 'What is k').replace(f'{T2} K.', f'{T2} K?'), k2, [k1 * T2 / T1, k1 * 2, k2 * 10, k1 * math.exp(Ea / RGAS * (1 / T1 - 1 / T2))], ' s⁻¹', key, f=lambda v: sci(v, 3))
        return Q(st, f'{sci(k2, 3)} s⁻¹', key, 'numerical')
    Ts = sorted(r.sample([290, 300, 310, 320, 330, 340, 350], 4))
    lnA = r.choice([20.0, 24.5, 28.0, 30.5])
    pts = [(1 / T, lnA - Ea / (RGAS * T)) for T in Ts]
    grad = (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0])
    data = '; '.join(f'T = {T} K, ln k = {fx(lnk, 2)}' for T, (_, lnk) in zip(Ts, pts))
    st = f'Values of the rate constant for {ctx} were measured at different temperatures: {data}. Calculate 1/T for each, plot (or use) a graph of ln k against 1/T, and determine the activation energy. (R = 8.31 J K⁻¹ mol⁻¹)'
    key = f'1/T values correct [1]; gradient = −Ea/R [1]; gradient ≈ {g3(grad)} K [1]; Ea = {g3(-grad * RGAS / 1000)} kJ mol⁻¹ [1] [4]'
    return Q(st, f'gradient ≈ {g3(grad)} K; Ea ≈ {g3(-grad * RGAS / 1000)} kJ mol⁻¹ (allow ±3%)', key, 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def cat_type(r, D):
    proc, cat, typ = r.choice(CATS)
    if D <= 2:
        return MQ(r, f'In {proc}, the catalyst is {cat}. What type of catalysis is this?', cap(typ), ['Heterogeneous' if typ == 'homogeneous' else 'Homogeneous', 'Autocatalysis by the products only', 'Enzyme catalysis'] if 'auto' not in cat else ['Heterogeneous', 'Enzyme catalysis', 'Surface adsorption only'],
                  f'{cap(typ)}: catalyst {"in the same phase as" if typ == "homogeneous" else "in a different phase from"} the reactants.')
    how = ('the catalyst takes part in the reaction (often by changing oxidation state) in steps with lower Ea and is regenerated' if typ == 'homogeneous'
           else 'reactants are adsorbed onto active sites, bonds weaken, reaction occurs, and products desorb')
    return Q(f'In {proc}, the catalyst is {cat}. State whether this is homogeneous or heterogeneous catalysis. Explain your answer and outline how it increases the rate.', f'{cap(typ)}; {how}.',
             'type [1]; phase reasoning [1]; mode of action [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def cat_case(r, D):
    T1 = r.choice([298, 303, 308])
    Ea = r.choice([50, 56, 62, 75])
    fac = math.exp(-Ea * 1000 / RGAS * (1 / (T1 + 10) - 1 / T1))
    st = f'{who(r)} is studying the reaction between peroxodisulfate ions and iodide ions, S₂O₈²⁻(aq) + 2I⁻(aq) → 2SO₄²⁻(aq) + I₂(aq), which has Ea = {Ea} kJ mol⁻¹ without a catalyst.'
    parts = [P_('Explain why the uncatalysed reaction is slow at room temperature.', 'Two negative ions repel each other, so the activation energy is high and few collisions are successful.', '[2]'),
             P_('Write two equations to show how Fe³⁺ ions catalyse this reaction.', '2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂; S₂O₈²⁻ + 2Fe²⁺ → 2SO₄²⁻ + 2Fe³⁺', 'each equation [1] [2]'),
             P_('State the type of catalysis and explain why Fe²⁺ ions would be equally effective.', 'Homogeneous; the cycle can start with either ion, since Fe²⁺ is oxidised to Fe³⁺ by S₂O₈²⁻ and Fe³⁺ is reduced back.', 'homogeneous [1]; either ion starts the cycle [1] [2]'),
             P_(f'Use the Arrhenius equation to calculate the factor by which k increases when the temperature is raised from {T1} K to {T1 + 10} K. (R = 8.31 J K⁻¹ mol⁻¹)', f'× {g3(fac)}', f'ln(k₂/k₁) = (Ea/R)(1/T₁ − 1/T₂) = {g3(math.log(fac))} [1]; factor {g3(fac)} [1] [2]'),
             P_('Describe, with reference to the Boltzmann distribution, why a catalyst increases the rate.', 'It provides a route with lower Ea, so a larger proportion of molecules in the distribution have energy ≥ Ea.', 'lower Ea [1]; larger area beyond Ea [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Compare homogeneous and heterogeneous catalysis, giving one example of each, and explain how temperature and catalysts affect the rate constant using the Arrhenius equation.', 'Homogeneous: same phase, intermediate formation, e.g. Fe²⁺/Fe³⁺ in S₂O₈²⁻/I⁻ with equations, or NO₂ in SO₂ oxidation; heterogeneous: different phase, adsorption–reaction–desorption, e.g. Fe in Haber process, catalytic converters; poisoning; k = Ae^(−Ea/RT): higher T increases fraction with E ≥ Ea; catalyst lowers Ea, increasing k; ln k vs 1/T gradient −Ea/R.',
           'homogeneous with example and equations [2]; heterogeneous mechanism [2]; Arrhenius temperature effect [2]; catalyst effect on Ea and k [1] [7]')])
t4d = t

CHAPTERS[4] = [t4a, t4b, t4c, t4d]


# ===================================================================== 5 Entropy and Gibbs free energy
S0 = {'H₂(g)': 130.6, 'O₂(g)': 205.0, 'N₂(g)': 191.6, 'H₂O(l)': 69.9, 'H₂O(g)': 188.7, 'CO₂(g)': 213.6, 'CaCO₃(s)': 92.9, 'CaO(s)': 39.7,
      'NH₃(g)': 192.3, 'CH₄(g)': 186.2, 'C(s)': 5.7, 'Mg(s)': 32.7, 'MgO(s)': 26.9, 'CO(g)': 197.6, 'SO₂(g)': 248.1, 'SO₃(g)': 256.7,
      'NO(g)': 210.7, 'NO₂(g)': 240.0, 'N₂O₄(g)': 304.2, 'HCl(g)': 186.8, 'C₂H₄(g)': 219.3, 'C₂H₆(g)': 229.2, 'CH₃OH(l)': 126.8,
      'Fe(s)': 27.3, 'Fe₂O₃(s)': 87.4, 'NH₄Cl(s)': 94.6, 'H₂O₂(l)': 109.6, 'MgCO₃(s)': 65.7, 'ZnO(s)': 43.6, 'Zn(s)': 41.6}
# (equation, reactants[(n, sp)], products[(n, sp)], ΔH kJ mol⁻¹)
GRX = [('CaCO₃(s) → CaO(s) + CO₂(g)', [(1, 'CaCO₃(s)')], [(1, 'CaO(s)'), (1, 'CO₂(g)')], 178),
       ('MgCO₃(s) → MgO(s) + CO₂(g)', [(1, 'MgCO₃(s)')], [(1, 'MgO(s)'), (1, 'CO₂(g)')], 117),
       ('N₂(g) + 3H₂(g) → 2NH₃(g)', [(1, 'N₂(g)'), (3, 'H₂(g)')], [(2, 'NH₃(g)')], -92),
       ('2SO₂(g) + O₂(g) → 2SO₃(g)', [(2, 'SO₂(g)'), (1, 'O₂(g)')], [(2, 'SO₃(g)')], -196),
       ('2H₂(g) + O₂(g) → 2H₂O(l)', [(2, 'H₂(g)'), (1, 'O₂(g)')], [(2, 'H₂O(l)')], -572),
       ('2NO₂(g) → N₂O₄(g)', [(2, 'NO₂(g)')], [(1, 'N₂O₄(g)')], -57),
       ('NH₄Cl(s) → NH₃(g) + HCl(g)', [(1, 'NH₄Cl(s)')], [(1, 'NH₃(g)'), (1, 'HCl(g)')], 176),
       ('CH₄(g) + H₂O(g) → CO(g) + 3H₂(g)', [(1, 'CH₄(g)'), (1, 'H₂O(g)')], [(1, 'CO(g)'), (3, 'H₂(g)')], 206),
       ('C(s) + H₂O(g) → CO(g) + H₂(g)', [(1, 'C(s)'), (1, 'H₂O(g)')], [(1, 'CO(g)'), (1, 'H₂(g)')], 131),
       ('2Mg(s) + O₂(g) → 2MgO(s)', [(2, 'Mg(s)'), (1, 'O₂(g)')], [(2, 'MgO(s)')], -1204),
       ('C₂H₄(g) + H₂(g) → C₂H₆(g)', [(1, 'C₂H₄(g)'), (1, 'H₂(g)')], [(1, 'C₂H₆(g)')], -137),
       ('H₂O(l) → H₂O(g)', [(1, 'H₂O(l)')], [(1, 'H₂O(g)')], 44),
       ('2Fe₂O₃(s) + 3C(s) → 4Fe(s) + 3CO₂(g)', [(2, 'Fe₂O₃(s)'), (3, 'C(s)')], [(4, 'Fe(s)'), (3, 'CO₂(g)')], 467),
       ('N₂(g) + O₂(g) → 2NO(g)', [(1, 'N₂(g)'), (1, 'O₂(g)')], [(2, 'NO(g)')], 181),
       ('2H₂O₂(l) → 2H₂O(l) + O₂(g)', [(2, 'H₂O₂(l)')], [(2, 'H₂O(l)'), (1, 'O₂(g)')], -196),
       ('ZnO(s) + C(s) → Zn(s) + CO(g)', [(1, 'ZnO(s)'), (1, 'C(s)')], [(1, 'Zn(s)'), (1, 'CO(g)')], 238),
       ('Fe₂O₃(s) + 3CO(g) → 2Fe(s) + 3CO₂(g)', [(1, 'Fe₂O₃(s)'), (3, 'CO(g)')], [(2, 'Fe(s)'), (3, 'CO₂(g)')], -25)]


def dS(rx):
    _, re_, pr, _ = rx
    return sum(n * S0[s] for n, s in pr) - sum(n * S0[s] for n, s in re_)


def s_work(rx):
    _, re_, pr, _ = rx
    a = ' + '.join(f'{n} × {S0[s]:.1f}' if n > 1 else f'{S0[s]:.1f}' for n, s in pr)
    b = ' + '.join(f'{n} × {S0[s]:.1f}' if n > 1 else f'{S0[s]:.1f}' for n, s in re_)
    return f'ΔS = ΣS(products) − ΣS(reactants) = ({a}) − ({b})'


def s_data(rx):
    _, re_, pr, _ = rx
    sp = list(dict.fromkeys([s for _, s in re_ + pr]))
    return ', '.join(f'{s} {S0[s]:.1f}' for s in sp)


SIGN_PROC = [('H₂O(l) → H₂O(g)', '+', 'liquid to gas: particles far more disordered'), ('N₂(g) + 3H₂(g) → 2NH₃(g)', '−', 'fewer moles of gas (4 → 2)'),
             ('CaCO₃(s) → CaO(s) + CO₂(g)', '+', 'a gas is formed from a solid'), ('NaCl(s) + aq → Na⁺(aq) + Cl⁻(aq)', '+', 'ions in solution are more disordered than in a lattice'),
             ('Ag⁺(aq) + Cl⁻(aq) → AgCl(s)', '−', 'aqueous ions form an ordered solid'), ('H₂O(l) → H₂O(s)', '−', 'liquid to ordered solid'),
             ('2H₂O₂(l) → 2H₂O(l) + O₂(g)', '+', 'a gas is produced'), ('Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)', '+', 'a gas is produced'),
             ('2Mg(s) + O₂(g) → 2MgO(s)', '−', 'a gas is used up, forming a solid'), ('N₂O₄(g) → 2NO₂(g)', '+', 'more moles of gas (1 → 2)'),
             ('Br₂(l) → Br₂(g)', '+', 'liquid to gas'), ('I₂(g) → I₂(s)', '−', 'gas to solid'), ('CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)', '−', 'three moles of gas become one'),
             ('NH₄NO₃(s) + aq → NH₄⁺(aq) + NO₃⁻(aq)', '+', 'solid lattice breaks into dispersed ions'), ('2SO₂(g) + O₂(g) → 2SO₃(g)', '−', 'fewer moles of gas (3 → 2)'),
             ('NH₄Cl(s) → NH₃(g) + HCl(g)', '+', 'two moles of gas form from a solid'), ('heating 1 mol of copper from 300 K to 500 K', '+', 'particles vibrate more; more ways to distribute energy'),
             ('C₂H₄(g) + H₂(g) → C₂H₆(g)', '−', 'two moles of gas become one')]

t = T('Entropy, S: disorder, predicting the sign of ΔS and calculating entropy change', 'entropy, s: disorder')
facts(t, [('entropy', 'S: a measure of the dispersal of energy and of the number of possible arrangements of particles and their energy (disorder) in a system'),
          ('standard molar entropy', 'S°: the entropy of 1 mole of a substance in its standard state at 298 K and 1 bar, in J K⁻¹ mol⁻¹'),
          ('entropy change', 'ΔS: the difference between the total entropy of the products and of the reactants, ΣS(products) − ΣS(reactants)'),
          ('spontaneous change', 'a change that, once started, takes place without a continuous supply of energy from outside the system'),
          ('third law of thermodynamics', 'the entropy of a perfect crystal at absolute zero is zero, so all substances have positive standard entropies at 298 K')])
mcqs(t, [('Which substance has the highest standard molar entropy at 298 K?', 'CO₂(g)', 'Gases have much higher entropy than liquids or solids.', ['H₂O(l)', 'C(s)', 'CaCO₃(s)']),
         ('What are the units of standard molar entropy?', 'J K⁻¹ mol⁻¹', 'Entropy values are given in joules, not kilojoules.', ['kJ mol⁻¹', 'J mol⁻¹', 'kJ K mol⁻¹']),
         ('Which change has a negative entropy change?', 'Steam condensing to water', 'Gas to liquid: fewer arrangements.', ['Ice melting', 'Sugar dissolving', 'A solid decomposing to give a gas']),
         ('Why is the entropy of a gas greater than that of its liquid?', 'Gas particles are more widely spread and have many more possible arrangements and energy states', 'Greater dispersal of particles and energy.', ['Gas particles are larger', 'Gas particles have stronger intermolecular forces', 'Gases have a higher density'])])
mcqs(t, [('For which reaction is ΔS most positive?', 'NH₄Cl(s) → NH₃(g) + HCl(g)', 'Two moles of gas from a solid.', ['N₂(g) + 3H₂(g) → 2NH₃(g)', 'H₂(g) + Cl₂(g) → 2HCl(g)', 'H₂O(g) → H₂O(l)']),
         ('For H₂(g) + Cl₂(g) → 2HCl(g), why is ΔS small?', 'The number of moles of gas does not change', '2 mol gas → 2 mol gas.', ['All the substances are elements', 'The reaction is exothermic', 'HCl is a polar molecule'])], D=(2, 3), C='C2')
shorts(t, [('State the meaning of the term entropy.', 'A measure of the dispersal of energy / number of ways particles and their energy can be arranged in a system (disorder).', '[1]'),
           ('Give the equation used to calculate the entropy change of a reaction from standard entropies.', 'ΔS° = ΣS°(products) − ΣS°(reactants)', '[1]')])
explain(t, [('Explain why the entropy of a substance increases sharply at its boiling point.', 'At the boiling point the liquid becomes a gas; the particles become much more spread out with many more possible arrangements and energy distributions, so entropy jumps.', 'change of state to gas [1]; many more arrangements [1] [2]'),
            ('Explain why dissolving an ionic solid in water usually has a positive entropy change.', 'The ordered lattice breaks up and the ions disperse throughout the solution, increasing the number of possible arrangements (though water molecules become ordered around ions).', '[2]'),
            ('Explain why the standard entropy of diamond is lower than that of graphite.', 'Diamond is a rigid three-dimensional lattice with strong bonds in all directions, so its atoms have fewer ways of vibrating/arranging energy than graphite, whose layers can slide and vibrate more freely.', '[2]')])
myths(t, [('Standard entropies are given in kJ K⁻¹ mol⁻¹, so ΔS can be used directly with ΔH in kJ.', 'S° values are in J K⁻¹ mol⁻¹; ΔS must be divided by 1000 before combining with ΔH in kJ mol⁻¹.'),
          ('Elements in their standard states have zero entropy, as they have zero enthalpy of formation.', 'Elements have positive standard entropies; only a perfect crystal at 0 K has zero entropy.'),
          ('An exothermic reaction must always have a positive entropy change.', 'ΔH and ΔS are independent; e.g. N₂ + 3H₂ → 2NH₃ is exothermic with negative ΔS.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ds_sign(r, D):
    proc, sg, why = r.choice(SIGN_PROC)
    if D <= 2:
        sg_w = 'positive' if sg == '+' else 'negative'
        return MQ(r, f'What is the sign of the entropy change, ΔS, for {proc}?', f'{cap(sg_w)}, because {why}', [f'{"Negative" if sg == "+" else "Positive"}, because {why}', f'{cap(sg_w)}, because the reaction is exothermic', 'Zero, because mass is conserved'], f'ΔS is {sg_w}: {why}.')
    proc2, sg2, why2 = r.choice([p for p in SIGN_PROC if p[0] != proc])
    return Q(f'Predict the sign of ΔS for each change and explain your predictions: (i) {proc}; (ii) {proc2}.', f'(i) {"positive" if sg == "+" else "negative"}: {why}; (ii) {"positive" if sg2 == "+" else "negative"}: {why2}.',
             'each sign [1]; each reason referring to states / moles of gas / disorder [1] [4]', 'short')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ds_calc(r, D):
    rx = r.choice(GRX)
    v = dS(rx)
    st = f'Use the standard entropies (J K⁻¹ mol⁻¹): {s_data(rx)} to calculate ΔS° for the reaction {rx[0]}.'
    key = f'{s_work(rx)} [1]; = {sgn(v, 1)} J K⁻¹ mol⁻¹ [1] [2]'
    if D <= 2:
        tot_p = sum(S0[s] for _, s in rx[2]) - sum(S0[s] for _, s in rx[1])
        return NQ(r, f'Standard entropies (J K⁻¹ mol⁻¹): {s_data(rx)}. What is ΔS° for the reaction {rx[0]}?', v, [-v, tot_p, v / 1000, sum(n * S0[s] for n, s in rx[2]) + sum(n * S0[s] for n, s in rx[1])], ' J K⁻¹ mol⁻¹', key, f=lambda x: sgn(x, 1))
    ans = f'{sgn(v, 1)} J K⁻¹ mol⁻¹'
    if D >= 4:
        st += ' Explain whether the sign of your answer is as expected.'
        key = key.replace(' [2]', '') + '; sign related to change in moles/states of gas [1] [3]'
        ans += '; ' + ('positive as expected: more gas / more disorder in the products' if v > 0 else 'negative as expected: fewer moles of gas / more ordered products')
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def ds_case(r, D):
    rx = r.choice([g for g in GRX if abs(dS(g)) > 50])
    v = dS(rx)
    st = f'{who(r)} is studying the reaction {rx[0]} (ΔH° = {sgn(rx[3])} kJ mol⁻¹). Standard entropies (J K⁻¹ mol⁻¹): {s_data(rx)}.'
    parts = [P_('Predict, without calculation, the sign of ΔS° for this reaction. Explain your prediction.', ('Positive' if v > 0 else 'Negative') + ': ' + ('more moles of gas / more disordered products' if v > 0 else 'fewer moles of gas / more ordered products') + '.', 'sign [1]; reason [1] [2]'),
             P_('Calculate ΔS° for the reaction.', f'{sgn(v, 1)} J K⁻¹ mol⁻¹', f'{s_work(rx)} [1]; {sgn(v, 1)} J K⁻¹ mol⁻¹ [1] [2]'),
             P_('Explain why all the standard entropy values are positive.', 'All substances above 0 K have some disorder (particles vibrate / have energy to distribute); only a perfect crystal at 0 K has S = 0.', '[1]'),
             P_('Explain why the standard entropy of a gas is much larger than that of a solid.', 'Gas particles move randomly and are widely spaced, with many more possible arrangements of particles and energy.', '[2]'),
             P_('Calculate ΔG° at 298 K and state whether the reaction is feasible at this temperature.', f'ΔG° = {sgn(rx[3])} − 298 × ({sgn(v / 1000, 4)}) = {kj(rx[3] - 298 * v / 1000, 1)}; ' + ('feasible' if rx[3] - 298 * v / 1000 < 0 else 'not feasible'), 'ΔS in kJ [1]; ΔG value [1]; conclusion [1] [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain what is meant by entropy and describe how the entropy of a system changes with temperature, change of state and changes in the number of moles of gas. Include how ΔS is calculated from standard entropies.', 'Entropy = dispersal of energy / number of arrangements; increases with temperature (more energy states); large jumps at melting and especially boiling; gases ≫ liquids > solids; reactions producing more moles of gas have positive ΔS; dissolving usually positive; ΔS = ΣS(products) − ΣS(reactants) with units J K⁻¹ mol⁻¹; worked example.',
           'definition [1]; temperature [1]; changes of state [2]; moles of gas [1]; calculation with units [2] [7]')])
t5a = t

# ---------------------------------------------------------------------
t = T('Gibbs free energy: ΔG = ΔH – TΔS and feasibility of reactions', 'gibbs free energy')
facts(t, [('Gibbs free energy change', 'ΔG: the energy change that determines feasibility, given by ΔG = ΔH − TΔS'),
          ('feasible reaction', 'a reaction for which ΔG is negative (or zero), so it can take place without continuous input of energy'),
          ('standard Gibbs free energy change', 'ΔG°: the Gibbs free energy change for a reaction under standard conditions'),
          ('kinetic stability', 'the situation in which a reaction is feasible (ΔG negative) but does not occur at a measurable rate because the activation energy is high'),
          ('absolute temperature', 'temperature measured in kelvin, used for T in ΔG = ΔH − TΔS')])
mcqs(t, [('A reaction is feasible when', 'ΔG is negative', 'ΔG ≤ 0 for a feasible change.', ['ΔH is positive', 'ΔS is negative', 'ΔG is positive']),
         ('In ΔG = ΔH − TΔS, what units must ΔS have if ΔH is in kJ mol⁻¹?', 'kJ K⁻¹ mol⁻¹', 'Divide J K⁻¹ mol⁻¹ by 1000.', ['J K⁻¹ mol⁻¹', 'kJ mol⁻¹', 'J mol⁻¹']),
         ('A reaction has ΔH negative and ΔS positive. When is it feasible?', 'At all temperatures', 'Both terms make ΔG negative.', ['Only at high temperatures', 'Only at low temperatures', 'At no temperature'])])
mcqs(t, [('ΔG for the combustion of methane is very negative, but methane does not burn at room temperature without a spark. Why?', 'The activation energy is high, so the rate is negligible', 'ΔG says nothing about rate.', ['ΔS is negative', 'The reaction is endothermic', 'ΔG is positive at room temperature']),
         ('A reaction has ΔH = +50 kJ mol⁻¹ and ΔS = −100 J K⁻¹ mol⁻¹. Which is correct?', 'It is not feasible at any temperature', 'Both terms make ΔG positive.', ['It is feasible above 500 K', 'It is feasible below 500 K', 'It is feasible at all temperatures'])], D=(2, 3), C='C2')
shorts(t, [('State the equation linking ΔG, ΔH, T and ΔS.', 'ΔG = ΔH − TΔS', '[1]'),
           ('State the condition for a reaction to be feasible in terms of ΔG.', 'ΔG ≤ 0 (negative)', '[1]')])
explain(t, [('Explain why a reaction with a negative ΔG may not take place at room temperature.', 'ΔG shows only that the reaction is thermodynamically feasible; if the activation energy is high the rate is extremely slow (kinetically stable).', 'ΔG relates to feasibility only [1]; high Ea / slow rate [1] [2]'),
            ('Explain why ΔS must be divided by 1000 when calculating ΔG.', 'Standard entropies are given in J K⁻¹ mol⁻¹ but ΔH is in kJ mol⁻¹; units must be consistent.', '[1]'),
            ('Explain how an endothermic reaction can be feasible.', 'If ΔS is positive and large enough, at a high enough temperature TΔS exceeds ΔH, so ΔG = ΔH − TΔS is negative.', 'positive ΔS [1]; TΔS > ΔH at high T [1] [2]')])
myths(t, [('All exothermic reactions are feasible.', 'An exothermic reaction with a negative ΔS becomes non-feasible at high temperature when TΔS outweighs ΔH.'),
          ('If ΔG is negative, the reaction will happen quickly.', 'ΔG indicates feasibility only; a high activation energy can make the rate negligible.'),
          ('T in ΔG = ΔH − TΔS can be in °C.', 'T must be the absolute temperature in kelvin.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def dg_calc(r, D):
    rx = r.choice(GRX)
    v = dS(rx)
    T_ = r.choice([298, 298, 400, 500, 700, 1000, 1200])
    g = rx[3] - T_ * v / 1000
    st = f'For the reaction {rx[0]}, ΔH° = {sgn(rx[3])} kJ mol⁻¹ and ΔS° = {sgn(v, 1)} J K⁻¹ mol⁻¹. Calculate ΔG at {T_} K and state whether the reaction is feasible at this temperature.'
    key = f'ΔG = ΔH − TΔS [1]; = {sgn(rx[3])} − {T_} × ({sgn(v / 1000, 4)}) [1]; = {kj(g, 1)} [1]; {"feasible (ΔG < 0)" if g < 0 else "not feasible (ΔG > 0)"} [1] [4]'
    if D <= 2:
        return NQ(r, f'For the reaction {rx[0]}, ΔH° = {sgn(rx[3])} kJ mol⁻¹ and ΔS° = {sgn(v, 1)} J K⁻¹ mol⁻¹. What is ΔG at {T_} K?', g, [rx[3] - (T_ - 273) * v / 1000, rx[3] + T_ * v / 1000, rx[3] - v / 1000, -g], ' kJ mol⁻¹', key, f=lambda x: sgn(x, 1))
    ans = f'{kj(g, 1)}; {"feasible" if g < 0 else "not feasible"}'
    if D >= 4:
        st = f'Use the standard entropies (J K⁻¹ mol⁻¹): {s_data(rx)}, and ΔH° = {sgn(rx[3])} kJ mol⁻¹, to calculate ΔG for {rx[0]} at {T_} K. State whether the reaction is feasible at this temperature.'
        key = f'{s_work(rx)} = {sgn(v, 1)} J K⁻¹ mol⁻¹ [1]; ' + key.replace(' [4]', ' [5]')
    return Q(st, ans, key, 'numerical')


@t.add('C3', (2, 3, 4), 'short')
def dg_signs(r, D):
    combos = [('negative', 'positive', 'feasible at all temperatures'), ('positive', 'negative', 'never feasible'),
              ('negative', 'negative', 'feasible only at low temperatures (below T = ΔH/ΔS)'), ('positive', 'positive', 'feasible only at high temperatures (above T = ΔH/ΔS)')]
    h, s_, res = r.choice(combos)
    ex = r.choice([g for g in GRX if (g[3] < 0) == (h == 'negative') and (dS(g) < 0) == (s_ == 'negative')] or [None])
    exs = f' An example is {ex[0]}.' if ex and D >= 3 else ''
    if D <= 2:
        return MQ(r, f'A reaction has ΔH {h} and ΔS {s_}. Under what conditions is it feasible?', cap(res), [cap(c[2]) for c in combos if c[2] != res], f'ΔG = ΔH − TΔS: {res}.')
    return Q(f'A reaction has ΔH {h} and ΔS {s_}. Use ΔG = ΔH − TΔS to explain how the feasibility of the reaction depends on temperature.' + exs,
             f'{cap(res)}: ' + {'feasible at all temperatures': 'both ΔH and −TΔS are negative, so ΔG is always negative',
                                 'never feasible': 'both ΔH and −TΔS are positive, so ΔG is always positive',
                                 'feasible only at low temperatures (below T = ΔH/ΔS)': 'ΔH is negative but −TΔS is positive and grows with T; at high T it outweighs ΔH',
                                 'feasible only at high temperatures (above T = ΔH/ΔS)': 'ΔH is positive but −TΔS is negative and grows with T; at high T it outweighs ΔH'}[res] + '.',
             'sign of −TΔS term [1]; comparison with ΔH as T changes [1]; conclusion [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def dg_case(r, D):
    rx = r.choice([g for g in GRX if g[3] > 0 and dS(g) > 0])
    v = dS(rx)
    Tm = rx[3] * 1000 / v
    use = {'CaCO₃(s) → CaO(s) + CO₂(g)': 'the manufacture of quicklime in a lime kiln', 'MgCO₃(s) → MgO(s) + CO₂(g)': 'producing magnesium oxide for refractory bricks',
           'NH₄Cl(s) → NH₃(g) + HCl(g)': 'the decomposition of ammonium chloride on heating', 'CH₄(g) + H₂O(g) → CO(g) + 3H₂(g)': 'steam reforming to make hydrogen',
           'C(s) + H₂O(g) → CO(g) + H₂(g)': 'making water gas from coke', 'H₂O(l) → H₂O(g)': 'the boiling of water', '2Fe₂O₃(s) + 3C(s) → 4Fe(s) + 3CO₂(g)': 'extracting iron using carbon',
           'N₂(g) + O₂(g) → 2NO(g)': 'formation of nitrogen monoxide in a car engine', 'ZnO(s) + C(s) → Zn(s) + CO(g)': 'extracting zinc by heating its oxide with carbon'}[rx[0]]
    st = f'{who(r)} is evaluating {use}: {rx[0]}, ΔH° = {sgn(rx[3])} kJ mol⁻¹. Standard entropies (J K⁻¹ mol⁻¹): {s_data(rx)}.'
    g298 = rx[3] - 298 * v / 1000
    parts = [P_('Calculate ΔS° for the reaction.', f'{sgn(v, 1)} J K⁻¹ mol⁻¹', f'{s_work(rx)} [1]; {sgn(v, 1)} [1] [2]'),
             P_('Calculate ΔG° at 298 K and comment on the feasibility of the reaction at room temperature.', f'{kj(g298, 1)}; not feasible at 298 K', f'ΔG = {sgn(rx[3])} − 298 × {sgn(v / 1000, 4)} [1]; {kj(g298, 1)} [1]; not feasible [1] [3]'),
             P_('Calculate the minimum temperature at which the reaction becomes feasible.', f'{sf(Tm, 3)} K', f'ΔG = 0 so T = ΔH ÷ ΔS [1]; = {sgn(rx[3])} ÷ ({sgn(v / 1000, 4)}) = {sf(Tm, 3)} K [1] [2]'),
             P_('Suggest two reasons why the actual temperature used may differ from your calculated value.', 'ΔH and ΔS vary with temperature (values are for 298 K); a higher temperature is needed for a reasonable rate; conditions are not standard (e.g. product gases removed).', 'any two [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how the Gibbs equation, ΔG = ΔH − TΔS, is used to decide whether a reaction is feasible, and discuss why a feasible reaction may not occur in practice.', 'ΔG ≤ 0 for feasible; units (ΔS ÷ 1000); four sign combinations with temperature dependence; worked example such as CaCO₃ decomposition; T at ΔG = 0 is T = ΔH/ΔS; kinetic stability: high Ea; standard vs non-standard conditions.',
           'equation and condition [1]; units [1]; sign combinations [2]; example calculation [2]; kinetic factors [1] [7]')])
t5b = t

# ---------------------------------------------------------------------
CELLS_G = [('Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)', 2, 1.10), ('Fe(s) + Cu²⁺(aq) → Fe²⁺(aq) + Cu(s)', 2, 0.78), ('Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s)', 2, 0.46),
           ('2Fe³⁺(aq) + 2I⁻(aq) → 2Fe²⁺(aq) + I₂(aq)', 2, 0.23), ('Cl₂(aq) + 2Br⁻(aq) → 2Cl⁻(aq) + Br₂(aq)', 2, 0.27), ('Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g)', 2, 2.38),
           ('MnO₄⁻(aq) + 8H⁺(aq) + 5Fe²⁺(aq) → Mn²⁺(aq) + 5Fe³⁺(aq) + 4H₂O(l)', 5, 0.75), ('Cr₂O₇²⁻(aq) + 14H⁺(aq) + 6Fe²⁺(aq) → 2Cr³⁺(aq) + 6Fe³⁺(aq) + 7H₂O(l)', 6, 0.56),
           ('2H₂(g) + O₂(g) → 2H₂O(l)', 4, 1.23), ('Zn(s) + 2Ag⁺(aq) → Zn²⁺(aq) + 2Ag(s)', 2, 1.56), ('Cu(s) + 2Fe³⁺(aq) → Cu²⁺(aq) + 2Fe²⁺(aq)', 2, 0.43),
           ('Br₂(aq) + 2I⁻(aq) → 2Br⁻(aq) + I₂(aq)', 2, 0.55), ('Ni(s) + Cu²⁺(aq) → Ni²⁺(aq) + Cu(s)', 2, 0.59), ('Mg(s) + Zn²⁺(aq) → Mg²⁺(aq) + Zn(s)', 2, 1.61)]

t = T('Effect of temperature on feasibility; linking ΔG to E°cell', 'effect of temperature on feasibility')
facts(t, [('ΔG° = −nFE°cell', 'the relationship between the standard Gibbs free energy change of a redox reaction and its standard cell potential, where n is the number of electrons transferred'),
          ('Faraday constant', 'F: the charge on 1 mole of electrons, 96 500 C mol⁻¹'),
          ('threshold temperature', 'the temperature at which ΔG = 0, given by T = ΔH ÷ ΔS, above or below which a reaction becomes feasible'),
          ('standard cell potential', 'E°cell: the e.m.f. of a cell under standard conditions, E°(reduction electrode) − E°(oxidation electrode)'),
          ('thermodynamic feasibility', 'whether a reaction can occur in terms of energy, shown by ΔG ≤ 0 or E°cell > 0')])
mcqs(t, [('What is the sign of ΔG° for a reaction with a positive E°cell?', 'Negative', 'ΔG° = −nFE°.', ['Positive', 'Zero', 'It depends on ΔH']),
         ('In ΔG° = −nFE°cell, what does n represent?', 'The number of moles of electrons transferred in the balanced equation', 'From the half-equations.', ['The number of moles of reactant', 'The charge on the metal ion', 'The number of electrodes']),
         ('At what temperature does a reaction with ΔH = +100 kJ mol⁻¹ and ΔS = +200 J K⁻¹ mol⁻¹ become feasible?', 'Above 500 K', 'T = 100 ÷ 0.200 = 500 K.', ['Above 0.5 K', 'Below 500 K', 'Above 20 000 K'])])
mcqs(t, [('Why does the feasibility of an exothermic reaction with negative ΔS decrease as temperature increases?', 'The −TΔS term becomes more positive', 'It eventually outweighs ΔH.', ['ΔH becomes more negative', 'The activation energy increases', 'ΔS becomes positive']),
         ('The unit of ΔG° from ΔG° = −nFE°cell, with F in C mol⁻¹ and E in V, is', 'J mol⁻¹', 'C × V = J.', ['kJ mol⁻¹', 'V mol⁻¹', 'C mol⁻¹'])], D=(2, 3), C='C2')
shorts(t, [('State the relationship between ΔG° and E°cell, defining each symbol.', 'ΔG° = −nFE°cell; n = moles of electrons transferred, F = Faraday constant (96 500 C mol⁻¹), E°cell = standard cell potential.', 'equation [1]; symbols [1] [2]')])
explain(t, [('Explain why a reaction with positive E°cell might still not be observed.', 'Positive E°cell (negative ΔG) shows thermodynamic feasibility, but the activation energy may be high so the rate is negligible; non-standard concentrations may also change E.', 'kinetic barrier [1]; non-standard conditions [1] [2]'),
            ('Explain why the decomposition of calcium carbonate is feasible only at high temperatures.', 'ΔH is positive and ΔS is positive; ΔG becomes negative only when TΔS exceeds ΔH, i.e. above T = ΔH/ΔS (about 1100 K).', '[2]'),
            ('Explain why ΔH and ΔS are assumed constant when the threshold temperature is calculated.', 'Standard values are measured at 298 K; they change a little with temperature, so the calculated T = ΔH/ΔS is an approximation.', '[2]')])
myths(t, [('E°cell and ΔG° have the same sign.', 'They have opposite signs: ΔG° = −nFE°cell, so a positive E°cell gives a negative ΔG°.'),
          ('In ΔG = −nFE, n is the number of moles of the metal used.', 'n is the number of moles of electrons transferred in the balanced equation.'),
          ('Raising the temperature always makes a reaction more feasible.', 'Only if ΔS is positive; if ΔS is negative, higher T makes ΔG less negative.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def dg_ecell(r, D):
    eq, n, E = r.choice(CELLS_G)
    g = -n * FARADAY * E / 1000
    mode = r.choice(['G', 'E']) if D >= 3 else 'G'
    if mode == 'G':
        st = f'For the cell reaction {eq}, E°cell = {m(f"{E:+.2f}")} V. Calculate ΔG° for the reaction in kJ mol⁻¹. (F = 96 500 C mol⁻¹)'
        key = f'n = {n} [1]; ΔG° = −nFE° = −{n} × 96 500 × {fx(E, 2)} [1]; = {kj(g, 1)} [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate ΔG°', 'What is ΔG°').replace('in kJ mol⁻¹.', 'in kJ mol⁻¹?'), g, [-g, g / n, 2 * g, -g / n], ' kJ mol⁻¹', key, f=lambda x: sgn(x, 1))
        ans = kj(g, 1)
        if D >= 4:
            st += ' Explain what your answer shows about the reaction.'
            key = key.replace(' [3]', '') + '; ΔG negative so feasible under standard conditions [1] [4]'
            ans += '; negative, so the reaction is feasible under standard conditions'
        return Q(st, ans, key, 'numerical')
    gg = round(g)
    st = f'For the reaction {eq}, ΔG° = {sgn(gg)} kJ mol⁻¹. Calculate E°cell. (F = 96 500 C mol⁻¹)'
    Ec = -gg * 1000 / (n * FARADAY)
    key = f'n = {n} [1]; E° = −ΔG° ÷ nF = {abs(gg) * 1000} ÷ ({n} × 96 500) [1]; = {m(f"{Ec:+.2f}")} V [1] [3]'
    return Q(st, f'{m(f"{Ec:+.2f}")} V', key, 'numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def t_thresh(r, D):
    rx = r.choice([g for g in GRX if (g[3] > 0) == (dS(g) > 0) and abs(dS(g)) > 10])
    v = dS(rx)
    Tm = rx[3] * 1000 / v
    up = v > 0
    st = f'For {rx[0]}, ΔH° = {sgn(rx[3])} kJ mol⁻¹ and ΔS° = {sgn(v, 1)} J K⁻¹ mol⁻¹. Calculate the temperature at which ΔG° = 0 and state whether the reaction is feasible above or below this temperature.'
    key = f'0 = ΔH − TΔS so T = ΔH ÷ ΔS [1]; T = {sgn(rx[3])} ÷ ({sgn(v / 1000, 4)}) = {sf(Tm, 3)} K [1]; feasible {"above" if up else "below"} this temperature [1] [3]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the temperature at which ΔG° = 0 and state whether the reaction is feasible above or below this temperature.', 'At what temperature is ΔG° = 0?'), Tm, [Tm / 1000, Tm - 273, rx[3] / v, Tm * 2], ' K', key)
    ans = f'{sf(Tm, 3)} K; feasible {"above" if up else "below"} this temperature'
    if D >= 5:
        Tq = r.choice([298, 500, 800, 1200, 1500])
        gq = rx[3] - Tq * v / 1000
        st += f' Calculate ΔG° at {Tq} K and confirm your answer.'
        key = key.replace(' [3]', '') + f'; ΔG°({Tq} K) = {kj(gq, 1)} [1] [4]'
        ans += f'; at {Tq} K ΔG° = {kj(gq, 1)} ({"feasible" if gq < 0 else "not feasible"})'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def ecell_case(r, D):
    eq, n, E = r.choice([c for c in CELLS_G if c[2] < 1.7])
    g = -n * FARADAY * E / 1000
    st = f'{who(r)} in {city(r)} builds an electrochemical cell based on the reaction {eq}, which has E°cell = {m(f"{E:+.2f}")} V.'
    parts = [P_('Calculate ΔG° for the cell reaction.', kj(g, 1), f'n = {n} [1]; −{n} × 96 500 × {fx(E, 2)} ÷ 1000 [1]; {kj(g, 1)} [1] [3]'),
             P_('Explain what the signs of E°cell and ΔG° show about the reaction.', 'E°cell positive and ΔG° negative: the reaction is thermodynamically feasible under standard conditions.', '[2]'),
             P_('Suggest why the reaction might not be observed when the reagents are mixed, even though ΔG° is negative.', 'The activation energy may be high so the rate is very slow; or concentrations are not standard.', '[1]'),
             P_('Describe and explain how E for the cell would change if the concentration of a reactant ion were increased.', 'E becomes more positive: the equilibrium at that electrode shifts to the right (Le Chatelier / Nernst), so the reaction becomes more feasible and ΔG more negative.', 'E more positive [1]; reason [1] [2]'),
             P_('State the relationship between ΔG and the cell e.m.f. under non-standard conditions.', 'ΔG = −nFE, using the measured cell e.m.f. E.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Discuss how temperature affects the feasibility of reactions, using ΔG = ΔH − TΔS, and explain how ΔG° is related to E°cell for redox reactions.', 'Four sign combinations; −TΔS grows with T; threshold temperature T = ΔH/ΔS with example (CaCO₃ ~1100 K); assumptions (ΔH, ΔS constant); ΔG° = −nFE°cell, n electrons, units J → kJ; positive E° gives negative ΔG; kinetic limitations and non-standard conditions.',
           'temperature effect with signs [2]; threshold calculation [1]; assumptions [1]; ΔG° = −nFE° with example [2]; limitations [1] [7]')])
t5c = t

CHAPTERS[5] = [t5a, t5b, t5c]


# ===================================================================== 6 Transition elements
TM = {'Sc': ('scandium', 1, 2), 'Ti': ('titanium', 2, 2), 'V': ('vanadium', 3, 2), 'Cr': ('chromium', 5, 1), 'Mn': ('manganese', 5, 2), 'Fe': ('iron', 6, 2),
      'Co': ('cobalt', 7, 2), 'Ni': ('nickel', 8, 2), 'Cu': ('copper', 10, 1), 'Zn': ('zinc', 10, 2)}
SUPN = {0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', 10: '¹⁰'}


def tm_config(el, q=0):
    _, d, s_ = TM[el]
    if q == 0:
        return f'1s² 2s² 2p⁶ 3s² 3p⁶ 3d{SUPN[d]} 4s{SUPN[s_]}'
    dn = d + s_ - q
    return '1s² 2s² 2p⁶ 3s² 3p⁶' + (f' 3d{SUPN[dn]}' if dn > 0 else '')


def d_count(el, q):
    _, d, s_ = TM[el]
    return d + s_ - q if q else d


def unpaired(n):
    return n if n <= 5 else 10 - n


def ion(el, q):
    return el + ({1: '⁺', 2: '²⁺', 3: '³⁺', 4: '⁴⁺'}[q])


OXS = [('MnO₄⁻', 'Mn', 7), ('MnO₄²⁻', 'Mn', 6), ('MnO₂', 'Mn', 4), ('Cr₂O₇²⁻', 'Cr', 6), ('CrO₄²⁻', 'Cr', 6), ('[Cr(H₂O)₆]³⁺', 'Cr', 3), ('VO₂⁺', 'V', 5),
       ('VO²⁺', 'V', 4), ('[V(H₂O)₆]³⁺', 'V', 3), ('[Fe(CN)₆]³⁻', 'Fe', 3), ('[Fe(CN)₆]⁴⁻', 'Fe', 2), ('[CuCl₄]²⁻', 'Cu', 2), ('Cu₂O', 'Cu', 1),
       ('[Co(NH₃)₆]³⁺', 'Co', 3), ('[CoCl₄]²⁻', 'Co', 2), ('[Ni(NH₃)₆]²⁺', 'Ni', 2), ('TiO₂', 'Ti', 4), ('[Ti(H₂O)₆]³⁺', 'Ti', 3),
       ('[Fe(C₂O₄)₃]³⁻', 'Fe', 3), ('[Ni(CN)₄]²⁻', 'Ni', 2), ('[Mn(H₂O)₆]²⁺', 'Mn', 2), ('FeO₄²⁻', 'Fe', 6), ('[Co(H₂O)₆]²⁺', 'Co', 2), ('K₂[CuCl₄]', 'Cu', 2), ('K₄[Fe(CN)₆]', 'Fe', 2)]

t = T('General properties of transition elements: electronic configuration, variable oxidation states and catalytic activity', 'general properties of transition elements')
facts(t, [('transition element', 'a d-block element that forms one or more stable ions with an incomplete d subshell'),
          ('variable oxidation states', 'the ability of a transition element to form ions or compounds in several oxidation states, because 3d and 4s electrons have similar energies'),
          ('ligand', 'a molecule or ion with one or more lone pairs of electrons that forms a dative covalent bond to a central metal ion'),
          ('complex ion', 'a central metal atom or ion surrounded by ligands bonded by dative covalent (coordinate) bonds'),
          ('d-block element', 'an element whose highest-energy electron is in a d subshell'),
          ('paramagnetism', 'attraction into a magnetic field shown by species with unpaired electrons, such as many transition metal ions')])
mcqs(t, [('What is the electronic configuration of Fe³⁺?', '1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵', '4s electrons lost first, then one 3d electron.', ['1s² 2s² 2p⁶ 3s² 3p⁶ 3d³ 4s²', '1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁶', '1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁴ 4s¹']),
         ('Which element of the first row of the d block is not a transition element?', 'Zinc', 'Zn²⁺ has a full 3d¹⁰ subshell.', ['Iron', 'Copper', 'Titanium']),
         ('What is the electronic configuration of a chromium atom?', '1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s¹', 'Half-filled 3d subshell is more stable.', ['1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁴ 4s²', '1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁶', '1s² 2s² 2p⁶ 3s² 3p⁶ 3d³ 4s² 4p¹']),
         ('Which electrons are lost first when a transition metal forms an ion?', '4s electrons', '4s is filled first but lost first.', ['3d electrons', '3p electrons', '4p electrons'])])
mcqs(t, [('Why is scandium not classed as a transition element?', 'Its only ion, Sc³⁺, has no d electrons', 'Sc³⁺ is 3d⁰.', ['It has no 4s electrons', 'It does not form ions', 'Its d subshell is full']),
         ('Why do transition elements show variable oxidation states?', 'The 3d and 4s electrons have similar energies, so different numbers can be lost or shared', 'Successive ionisation energies rise gradually.', ['They have very high first ionisation energies', 'They have full d subshells', 'They form only covalent compounds']),
         ('Which property of transition elements explains their catalytic activity?', 'They can change oxidation state and adsorb reactants using d orbitals', 'Electron transfer and surface bonding.', ['They have high melting points', 'They are good conductors', 'They are dense'])], D=(2, 3), C='C2')
shorts(t, [('State two properties of transition elements that are not shown by s-block metals.', 'Any two: variable oxidation states; form complex ions; form coloured compounds; act as catalysts.', '[2]'),
           ('Write the electronic configuration of the copper atom and of the Cu²⁺ ion.', 'Cu: 1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s¹; Cu²⁺: 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁹', 'each [1] [2]')])
explain(t, [('Explain why transition elements and their compounds often act as catalysts.', 'They can change oxidation state readily, accepting and donating electrons in intermediate steps; and they can adsorb reactants onto their surfaces using d orbitals, weakening bonds.', 'variable oxidation states [1]; adsorption / d orbitals [1] [2]'),
            ('Explain why zinc is a d-block element but not a transition element.', 'Its outermost electrons are in the 3d/4s region (d block), but its only ion Zn²⁺ has a complete 3d¹⁰ subshell, so it does not form an ion with an incomplete d subshell.', '[2]'),
            ('Explain why the maximum oxidation state of manganese is +7.', 'Mn has 7 electrons in its 3d and 4s orbitals (3d⁵ 4s²), all of similar energy, so up to 7 can be used in bonding (e.g. in MnO₄⁻).', '[2]')])
myths(t, [('Transition metal atoms lose their 3d electrons before their 4s electrons.', 'The 4s electrons are lost first when the ions form.'),
          ('All d-block elements are transition elements.', 'Scandium and zinc are d-block elements but form only ions with empty (Sc³⁺) or full (Zn²⁺) d subshells.'),
          ('Transition elements have only one stable oxidation state, like Group 2 metals.', 'Transition elements show variable oxidation states because 3d and 4s electrons are close in energy.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def ox_config(r, D):
    sp, el, q = r.choice(OXS)
    nm = TM[el][0]
    dn = d_count(el, q)
    if D <= 2:
        opts = [q + 1, q - 1, q + 2, q - 2, 8 - q]
        return MQ(r, f'What is the oxidation state of {nm} in {sp}?', f'+{q}', [f'+{o}' for o in opts if 0 < o <= 8 and o != q], f'Sum of oxidation states equals the overall charge: {nm} is +{q}.')
    st = f'State the oxidation state of {nm} in {sp} and give the electronic configuration of {nm} in this oxidation state.'
    ans = f'+{q}; {tm_config(el, q)}'
    key = f'+{q} [1]; {tm_config(el, q)} [1]'
    tot = 2
    if D >= 4:
        st += ' State the number of unpaired electrons and explain whether you would expect compounds of this ion to be coloured.'
        col = dn not in (0, 10)
        ans += f'; {unpaired(dn)} unpaired electron(s); ' + ('coloured: partly filled d subshell allows d–d transitions' if col else f'colourless: 3d{SUPN[dn]} so no d–d transitions are possible')
        key += f'; {unpaired(dn)} unpaired [1]; colour with reason (d{dn}) [1]'
        tot += 2
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (1, 2, 3, 4), 'short')
def config_q(r, D):
    el = r.choice(['Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu'])
    q = r.choice([2, 3] if el not in ('Cu',) else [1, 2])
    nm = TM[el][0]
    if D <= 2:
        dn = d_count(el, q)
        wrong = [tm_config(el, 0), '1s² 2s² 2p⁶ 3s² 3p⁶' + (f' 3d{SUPN[max(dn - 2, 0)]} 4s²' if dn >= 2 else ' 4s²'), '1s² 2s² 2p⁶ 3s² 3p⁶' + f' 3d{SUPN[min(dn + 1, 10)]}', '1s² 2s² 2p⁶ 3s² 3p⁶' + f' 3d{SUPN[max(dn - 1, 1)]} 4s¹']
        return MQ(r, f'What is the electronic configuration of the {ion(el, q)} ion?', tm_config(el, q), wrong, f'{nm.capitalize()} atom {tm_config(el)}; lose 4s electrons first: {tm_config(el, q)}.')
    st = f'Write the full electronic configurations of a {nm} atom and of the {ion(el, q)} ion.'
    ans = f'{nm.capitalize()}: {tm_config(el)}; {ion(el, q)}: {tm_config(el, q)}'
    key = 'atom [1]; ion (4s electrons removed first) [1]'
    tot = 2
    if D >= 4:
        st += f' Use your answer to explain why {nm} is classed as a transition element.'
        ans += f'; {ion(el, q)} has an incomplete 3d subshell, so {nm} forms a stable ion with a partly filled d subshell'
        key += '; incomplete d subshell in the ion [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def tm_case(r, D):
    el = r.choice(['Mn', 'Fe', 'Cr', 'V', 'Co', 'Cu'])
    nm = TM[el][0]
    sps = [s for s in OXS if s[1] == el]
    sp, _, q = r.choice(sps)
    cat = {'Mn': 'MnO₂ catalyses the decomposition of hydrogen peroxide', 'Fe': 'iron catalyses the Haber process', 'Cr': 'chromium(III) oxide is used as a catalyst in some dehydrogenation reactions',
           'V': 'vanadium(V) oxide catalyses the Contact process', 'Co': 'cobalt compounds catalyse the oxidation of tartrate ions by hydrogen peroxide', 'Cu': 'copper catalyses the oxidation of methanol to methanal'}[el]
    st = f'{who(r)} is writing a report on {nm}, a first-row transition element. One of its compounds contains {sp}. In industry, {cat}.'
    dn = d_count(el, q)
    parts = [P_(f'Write the electronic configuration of a {nm} atom.', tm_config(el), '[1]'),
             P_(f'Deduce the oxidation state of {nm} in {sp} and give the electronic configuration of {nm} in this state.', f'+{q}; {tm_config(el, q)}', 'oxidation state [1]; configuration [1] [2]'),
             P_(f'Explain why {nm} can exist in several oxidation states.', 'The 3d and 4s electrons are similar in energy, so different numbers of them can be lost or used in bonding without a large jump in ionisation energy.', '[2]'),
             P_('Explain how the transition element acts as a catalyst in the industrial example.', 'It provides an alternative route with lower activation energy, by adsorbing reactants on its surface (using d orbitals) and/or changing oxidation state in intermediate steps.', 'lower Ea route [1]; adsorption or variable oxidation state [1] [2]'),
             P_(f'Predict, with a reason, whether compounds containing {sp} would be paramagnetic.', ('Yes: ' if unpaired(dn) else 'No: ') + f'{nm} in the +{q} state has {unpaired(dn)} unpaired electron(s).', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe and explain the characteristic properties of the transition elements Ti to Cu, referring to electronic configurations, variable oxidation states and catalytic activity.', 'Definition (incomplete d subshell in an ion); configurations including Cr 3d⁵4s¹ and Cu 3d¹⁰4s¹; 4s lost before 3d; variable oxidation states because 3d/4s similar in energy, max state rises to Mn (+7) then falls; examples MnO₄⁻, Cr₂O₇²⁻, VO₂⁺; catalysis: variable oxidation states (Fe²⁺/Fe³⁺) and adsorption (Fe, V₂O₅); complexes and colour; Sc and Zn not transition elements.',
           'definition [1]; configurations with exceptions [2]; variable oxidation states explained [2]; catalysis with examples [2] [7]')])
t6a = t

# ---------------------------------------------------------------------
CPX = [('[Cu(H₂O)₆]²⁺', 'Cu', 2, 'water', 'monodentate', 6, 'octahedral', '90°', None),
       ('[CuCl₄]²⁻', 'Cu', 2, 'chloride ions', 'monodentate', 4, 'tetrahedral', '109.5°', None),
       ('[Cu(NH₃)₄(H₂O)₂]²⁺', 'Cu', 2, 'ammonia and water', 'monodentate', 6, 'octahedral', '90°', None),
       ('[CoCl₄]²⁻', 'Co', 2, 'chloride ions', 'monodentate', 4, 'tetrahedral', '109.5°', None),
       ('[Co(H₂O)₆]²⁺', 'Co', 2, 'water', 'monodentate', 6, 'octahedral', '90°', None),
       ('[Fe(H₂O)₆]²⁺', 'Fe', 2, 'water', 'monodentate', 6, 'octahedral', '90°', None),
       ('[Ag(NH₃)₂]⁺', 'Ag', 1, 'ammonia', 'monodentate', 2, 'linear', '180°', None),
       ('[Pt(NH₃)₂Cl₂]', 'Pt', 2, 'ammonia and chloride ions', 'monodentate', 4, 'square planar', '90°', 'geometrical (cis/trans) isomerism; the cis isomer is the anticancer drug cisplatin'),
       ('[Ni(CN)₄]²⁻', 'Ni', 2, 'cyanide ions', 'monodentate', 4, 'square planar', '90°', None),
       ('[Co(NH₃)₆]³⁺', 'Co', 3, 'ammonia', 'monodentate', 6, 'octahedral', '90°', None),
       ('[Ni(en)₃]²⁺', 'Ni', 2, 'ethane-1,2-diamine (en)', 'bidentate', 6, 'octahedral', '90°', 'optical isomerism (non-superimposable mirror images)'),
       ('[Co(en)₃]³⁺', 'Co', 3, 'ethane-1,2-diamine (en)', 'bidentate', 6, 'octahedral', '90°', 'optical isomerism (non-superimposable mirror images)'),
       ('[Cr(C₂O₄)₃]³⁻', 'Cr', 3, 'ethanedioate ions', 'bidentate', 6, 'octahedral', '90°', 'optical isomerism (non-superimposable mirror images)'),
       ('[Co(NH₃)₄Cl₂]⁺', 'Co', 3, 'ammonia and chloride ions', 'monodentate', 6, 'octahedral', '90°', 'geometrical (cis/trans) isomerism'),
       ('[Ni(H₂O)₆]²⁺', 'Ni', 2, 'water', 'monodentate', 6, 'octahedral', '90°', None),
       ('[Fe(EDTA)]⁻', 'Fe', 3, 'EDTA⁴⁻', 'hexadentate', 6, 'octahedral', '90°', 'optical isomerism'),
       ('[Co(en)₂Cl₂]⁺', 'Co', 3, 'ethane-1,2-diamine and chloride ions', 'bidentate and monodentate', 6, 'octahedral', '90°', 'geometrical (cis/trans) isomerism; the cis isomer also shows optical isomerism'),
       ('[Cr(H₂O)₆]³⁺', 'Cr', 3, 'water', 'monodentate', 6, 'octahedral', '90°', None),
       ('[Fe(CN)₆]³⁻', 'Fe', 3, 'cyanide ions', 'monodentate', 6, 'octahedral', '90°', None),
       ('[Ni(en)₂(H₂O)₂]²⁺', 'Ni', 2, 'ethane-1,2-diamine and water', 'bidentate and monodentate', 6, 'octahedral', '90°', 'geometrical (cis/trans) isomerism; the cis isomer also shows optical isomerism')]
MNAME = {'Cu': 'copper', 'Co': 'cobalt', 'Fe': 'iron', 'Ag': 'silver', 'Pt': 'platinum', 'Ni': 'nickel', 'Cr': 'chromium'}

t = T('Complex ions: ligands, coordination number, geometry and stereoisomerism in complexes', 'complex ions: ligands')
facts(t, [('coordination number', 'the number of dative (coordinate) bonds from ligands to the central metal ion'),
          ('monodentate ligand', 'a ligand that forms one dative bond to a metal ion, e.g. H₂O, NH₃, Cl⁻, CN⁻'),
          ('bidentate ligand', 'a ligand that forms two dative bonds to a metal ion, e.g. ethane-1,2-diamine or ethanedioate'),
          ('polydentate ligand', 'a ligand that forms several dative bonds to one metal ion, e.g. hexadentate EDTA⁴⁻'),
          ('dative covalent bond', 'a covalent bond in which both electrons of the shared pair come from the same atom (the ligand)'),
          ('geometrical isomerism', 'in complexes, isomerism arising from different spatial arrangements of ligands, such as cis and trans forms'),
          ('optical isomerism', 'isomerism in which two forms are non-superimposable mirror images, e.g. in [Ni(en)₃]²⁺')])
mcqs(t, [('What is the coordination number of the metal ion in [Cu(NH₃)₄(H₂O)₂]²⁺?', '6', 'Four NH₃ plus two H₂O.', ['4', '2', '8']),
         ('What is the shape of [CuCl₄]²⁻?', 'Tetrahedral', 'Large Cl⁻ ligands: four-coordinate tetrahedral.', ['Octahedral', 'Square planar', 'Linear']),
         ('Which is a bidentate ligand?', 'Ethane-1,2-diamine, H₂NCH₂CH₂NH₂', 'Two N lone pairs.', ['Ammonia', 'Cyanide ion', 'Water']),
         ('What is the shape of [Ag(NH₃)₂]⁺?', 'Linear', 'Two ligands at 180°.', ['Tetrahedral', 'Bent', 'Square planar'])])
mcqs(t, [('Why does [CuCl₄]²⁻ have a lower coordination number than [Cu(H₂O)₆]²⁺?', 'Chloride ions are larger than water molecules, so fewer fit around the metal ion', 'Ligand size.', ['Chloride ions are uncharged', 'Water is bidentate', 'Cu is in a different oxidation state']),
         ('Which complex shows optical isomerism?', '[Ni(en)₃]²⁺', 'Three bidentate ligands: non-superimposable mirror images.', ['[Cu(H₂O)₆]²⁺', '[CuCl₄]²⁻', 'trans-[Co(NH₃)₄Cl₂]⁺']),
         ('Why is trans-[Pt(NH₃)₂Cl₂] not an effective anticancer drug, unlike cisplatin?', 'Its shape does not allow both Pt–Cl positions to bind adjacent guanine bases in DNA', 'Cis arrangement required to cross-link DNA.', ['It is not a complex', 'It has a different oxidation state of Pt', 'It is octahedral'])], D=(2, 3), C='C2')
shorts(t, [('Define the term ligand.', 'A species with a lone pair of electrons that forms a dative covalent bond to a central metal ion.', '[1]'),
           ('Describe the two isomers of [Pt(NH₃)₂Cl₂] and name the type of isomerism.', 'Square planar: cis (Cl next to each other, 90°) and trans (Cl opposite, 180°); geometrical (cis/trans) isomerism.', 'both arrangements [1]; geometrical isomerism [1] [2]')])
explain(t, [('Explain how ligands bond to a central metal ion.', 'Each ligand donates a lone pair of electrons into an empty orbital of the metal ion, forming a dative covalent (coordinate) bond.', 'lone pair donated [1]; dative bond to empty orbital [1] [2]'),
            ('Explain why [Ni(en)₃]²⁺ shows optical isomerism but [Ni(H₂O)₆]²⁺ does not.', 'With three bidentate en ligands the octahedral complex has no plane of symmetry, so it exists as two non-superimposable mirror images; the hexaaqua ion has planes of symmetry.', 'no plane of symmetry / chiral [1]; mirror images non-superimposable [1] [2]'),
            ('Explain how cisplatin acts as an anticancer drug.', 'It loses its chloride ligands inside cells (ligand exchange with water); Pt then bonds to two adjacent nitrogen atoms of guanine bases on DNA, distorting DNA and preventing replication of cancer cells.', 'ligand exchange [1]; binds to DNA bases [1]; prevents replication [1] [3]')])
myths(t, [('The coordination number of a complex equals the number of ligands.', 'It equals the number of dative bonds; with bidentate ligands (e.g. [Ni(en)₃]²⁺) it is twice the number of ligands.'),
          ('All four-coordinate complexes are tetrahedral.', 'Some are square planar, e.g. cisplatin [Pt(NH₃)₂Cl₂] and [Ni(CN)₄]²⁻.'),
          ('Cis and trans isomers of complexes are optical isomers.', 'Cis/trans isomers are geometrical isomers; optical isomers are non-superimposable mirror images.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def cpx_q(r, D):
    f, el, q, lig, dent, cn, shp, ang, iso = r.choice(CPX)
    nm = MNAME[el]
    if D <= 2:
        a = r.randrange(3)
        if a == 0:
            return MQ(r, f'What is the coordination number of {nm} in {f}?', str(cn), [str(x) for x in (2, 4, 6, 8, 3) if x != cn], f'{cn} dative bonds from {lig} ({dent}).')
        if a == 1:
            return MQ(r, f'What is the shape of the complex ion {f}?', cap(shp), [cap(x) for x in ('octahedral', 'tetrahedral', 'square planar', 'linear', 'trigonal planar') if x != shp], f'Coordination number {cn}: {shp}.')
        return MQ(r, f'What is the oxidation state of {nm} in {f}?', f'+{q}', [f'+{x}' for x in (1, 2, 3, 4, 6) if x != q], f'Overall charge minus ligand charges gives +{q}.')
    st = f'For the complex {f}, state the oxidation state of {nm}, the coordination number, the shape and a bond angle.'
    ans = f'+{q}; coordination number {cn}; {shp}; {ang}'
    key = f'+{q} [1]; {cn} [1]; {shp} [1]; {ang} [1]'
    tot = 4
    if D >= 4:
        st += ' Identify the type of ligand present and state, with a reason, whether the complex shows stereoisomerism.'
        ans += f'; ligand: {lig} ({dent}); ' + (iso if iso else 'no stereoisomers, because all positions are equivalent / the ligands are identical and monodentate')
        key += '; ligand type [1]; stereoisomerism decision with reason [1]'
        tot += 2
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'short')
def iso_q(r, D):
    f, el, q, lig, dent, cn, shp, ang, iso = r.choice([c for c in CPX if c[8]])
    if D <= 2:
        kind = 'optical' if iso.startswith('optical') else 'geometrical'
        return MQ(r, f'Which type of stereoisomerism is shown by {f}?', 'Optical isomerism' if kind == 'optical' else 'Geometrical (cis/trans) isomerism', ['Structural isomerism', 'Geometrical (cis/trans) isomerism' if kind == 'optical' else 'Optical isomerism', 'No stereoisomerism', 'Chain isomerism'], iso + '.')
    return Q(f'The complex {f} shows stereoisomerism. Identify the type(s) of stereoisomerism and describe the arrangement of the ligands in the isomers.', cap(iso) + '. ' +
             ('The ligands span adjacent positions of the octahedron, so the two forms are mirror images that cannot be superimposed.' if iso.startswith('optical') else
              'In the cis isomer two identical ligands are adjacent (90°); in the trans isomer they are opposite each other (180°).'),
             'type(s) of isomerism [1]; description of arrangement [1]; reference to shape [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def cpx_case(r, D):
    el = r.choice(['Cu', 'Co'])
    if el == 'Cu':
        st = f'{who(r)} adds concentrated hydrochloric acid dropwise to aqueous copper(II) sulfate, which contains [Cu(H₂O)₆]²⁺. The solution turns yellow-green. In a second tube, excess aqueous ammonia is added to [Cu(H₂O)₆]²⁺ and a deep blue solution forms.'
        a, b, c = '[Cu(H₂O)₆]²⁺', '[CuCl₄]²⁻', '[Cu(NH₃)₄(H₂O)₂]²⁺'
        eq1 = '[Cu(H₂O)₆]²⁺ + 4Cl⁻ ⇌ [CuCl₄]²⁻ + 6H₂O'
    else:
        st = f'{who(r)} adds concentrated hydrochloric acid to pink aqueous cobalt(II) chloride, containing [Co(H₂O)₆]²⁺, and the solution turns blue. Adding water reverses the change.'
        a, b, c = '[Co(H₂O)₆]²⁺', '[CoCl₄]²⁻', None
        eq1 = '[Co(H₂O)₆]²⁺ + 4Cl⁻ ⇌ [CoCl₄]²⁻ + 6H₂O'
    parts = [P_('Write an equation for the reaction with concentrated hydrochloric acid.', eq1, '[1]'),
             P_(f'State the shape and coordination number of {a} and of {b}.', f'{a}: octahedral, 6; {b}: tetrahedral, 4', 'each complex [1] [2]'),
             P_('Explain why the coordination number changes.', 'Chloride ions are larger than water molecules, so only four fit around the metal ion.', '[1]'),
             P_('Explain why adding water reverses the change.', 'The equilibrium shifts to the left as [H₂O] increases (and [Cl⁻] decreases), re-forming the hexaaqua ion.', '[2]')]
    if c:
        parts.append(P_(f'Name the type of reaction that forms {c} and describe its structure.', f'Ligand exchange (substitution); {c} is octahedral with four NH₃ in a plane and two H₂O ligands opposite each other.', 'ligand exchange [1]; structure [1] [2]'))
    else:
        parts.append(P_('Suggest how this reaction could be used as a test for water.', 'Blue anhydrous cobalt(II) chloride paper turns pink when water is present, as the aqua complex forms.', '[2]'))
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the bonding, shapes and types of isomerism found in transition metal complexes, using named examples.', 'Ligands donate lone pairs (dative bonds); mono-, bi- and polydentate ligands (H₂O, en, EDTA⁴⁻); coordination numbers 2, 4, 6; shapes linear [Ag(NH₃)₂]⁺, tetrahedral [CuCl₄]²⁻, square planar cisplatin, octahedral [Cu(H₂O)₆]²⁺; cis/trans in [Pt(NH₃)₂Cl₂] and [Co(NH₃)₄Cl₂]⁺; optical in [Ni(en)₃]²⁺; cisplatin action.',
           'dative bonding [1]; ligand types [1]; shapes with examples [2]; geometrical isomerism [1]; optical isomerism [1]; application [1] [7]')])
t6b = t

# ---------------------------------------------------------------------
HPL, CL = 6.63e-34, 3.00e8
COLOURS = [(400, 450, 'violet', 'yellow'), (450, 495, 'blue', 'orange'), (495, 570, 'green', 'red-purple (magenta)'), (570, 590, 'yellow', 'violet'), (590, 620, 'orange', 'blue'), (620, 750, 'red', 'blue-green (cyan)')]
ABS = [('[Ti(H₂O)₆]³⁺', 500, 'purple'), ('[Cu(H₂O)₆]²⁺', 790, 'pale blue'), ('[Cu(NH₃)₄(H₂O)₂]²⁺', 600, 'deep blue'), ('[Co(H₂O)₆]²⁺', 515, 'pink'),
       ('[CoCl₄]²⁻', 690, 'blue'), ('[Cr(H₂O)₆]³⁺', 575, 'violet'), ('[Co(NH₃)₆]³⁺', 475, 'yellow-orange'), ('[Ni(NH₃)₆]²⁺', 570, 'blue-violet')]


def colour_of(lam):
    for lo, hi, a, s_ in COLOURS:
        if lo <= lam < hi:
            return a, s_
    return None, None


t = T('Splitting of d orbitals and the origin of colour in complexes', 'splitting of d orbitals')
facts(t, [('d-orbital splitting', 'the separation of the five d orbitals of a metal ion into groups of different energy when ligands approach'),
          ('ΔE', 'the energy gap between the split d orbitals, related to the frequency of light absorbed by ΔE = hf = hc/λ'),
          ('d–d transition', 'the promotion of an electron from a lower-energy d orbital to a higher-energy d orbital by absorbing visible light'),
          ('complementary colour', 'the colour seen when light of a particular colour is absorbed from white light; e.g. absorbing orange gives blue'),
          ('spectrochemical effect', 'the observation that different ligands split the d orbitals by different amounts (e.g. NH₃ more than H₂O)')])
mcqs(t, [('In an octahedral complex, how are the d orbitals split?', 'Two orbitals at higher energy and three at lower energy', 'dz² and dx²−y² point at ligands.', ['Three higher and two lower', 'Four higher and one lower', 'They remain degenerate']),
         ('Why is [Zn(H₂O)₆]²⁺ colourless?', 'Zn²⁺ has a full 3d subshell, so no d–d transitions are possible', '3d¹⁰.', ['Zn²⁺ has no d orbitals', 'Water does not split d orbitals', 'Zn²⁺ is too small']),
         ('A complex absorbs light in the orange region. What colour does it appear?', 'Blue', 'Complementary colour.', ['Orange', 'Red', 'Yellow']),
         ('Which equation links the d-orbital energy gap to the wavelength of light absorbed?', 'ΔE = hc/λ', 'E = hf and c = fλ.', ['ΔE = hλ/c', 'ΔE = λ/hc', 'ΔE = hcλ'])])
mcqs(t, [('Replacing H₂O ligands by NH₃ in a copper(II) complex increases ΔE. What happens to the wavelength of light absorbed?', 'It decreases', 'Larger ΔE: higher-energy, shorter-wavelength light.', ['It increases', 'It is unchanged', 'No light is absorbed']),
         ('Why are [Cu(H₂O)₆]²⁺ and [CuCl₄]²⁻ different colours?', 'Different ligands and geometries give different ΔE, so different wavelengths are absorbed', 'ΔE depends on ligand and shape.', ['Cu has different oxidation states', 'Chloride ions are coloured', 'One is a solid and one is a solution']),
         ('Why is Sc³⁺ colourless in solution?', 'It has no d electrons (3d⁰), so no d–d transitions can occur', 'No electrons to promote.', ['It has a full 3d subshell', 'Its d orbitals are not split', 'It forms only tetrahedral complexes'])], D=(2, 3), C='C2')
shorts(t, [('Name the two d orbitals at higher energy in an octahedral complex.', 'dx²−y² and dz²', '[1]'),
           ('State two factors that affect the size of ΔE in a complex.', 'Any two: identity of the ligand; coordination number / geometry; oxidation state of the metal; identity of the metal.', '[2]')])
explain(t, [('Explain why transition metal complexes are often coloured.', 'Ligands split the d orbitals into two energy levels; an electron in a lower d orbital absorbs visible light of energy ΔE and is promoted; the light transmitted/reflected is the complementary colour.', 'd orbitals split [1]; absorption of visible light / electron promoted [1]; complementary colour seen [1] [3]'),
            ('Explain why the splitting in a tetrahedral complex is smaller than in an octahedral complex.', 'In a tetrahedral complex fewer ligands are present and none point directly at the d orbitals, so the repulsion difference between orbitals is smaller.', '[2]'),
            ('Explain why changing the ligands around a metal ion can change its colour.', 'Different ligands split the d orbitals by different amounts (ΔE), so a different frequency/wavelength of light is absorbed and the complementary colour changes.', '[2]')])
myths(t, [('A blue complex absorbs blue light.', 'It appears blue because it absorbs the complementary colour (orange/red) and transmits blue.'),
          ('All transition metal compounds are coloured.', 'Ions with d⁰ (Sc³⁺, Ti⁴⁺) or d¹⁰ (Cu⁺, Zn²⁺) configurations cannot undergo d–d transitions and are colourless.'),
          ('In an octahedral complex, three d orbitals rise in energy and two fall.', 'The two orbitals pointing at the ligands (dz², dx²−y²) are raised; the other three are lower.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def de_calc(r, D):
    if r.random() < 0.5:
        f, lam, seen = r.choice(ABS)
        who_ = f'The complex {f}'
    else:
        lam = r.randrange(420, 740, 5)
        f, seen = None, colour_of(lam)[1]
        who_ = r.choice(['A complex of nickel(II)', 'A complex of cobalt(III)', 'An aqueous chromium(III) complex', 'A vanadium(III) complex', 'A copper(II) complex'])
    E1 = HPL * CL / (lam * 1e-9)
    Em = E1 * L_AV / 1000
    ab, comp = colour_of(lam) if lam < 750 else ('red/near-infrared', 'blue')
    st = f'{who_} absorbs light most strongly at a wavelength of {lam} nm. Calculate the energy gap, ΔE, between the split d orbitals for one ion, in J. (h = 6.63 × 10⁻³⁴ J s, c = 3.00 × 10⁸ m s⁻¹)'
    key = f'ΔE = hc/λ [1]; λ = {lam} × 10⁻⁹ m [1]; ΔE = {sci(E1, 3)} J [1] [3]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the energy gap', 'What is the energy gap').replace('in J.', 'in J?'), E1, [E1 * 1e9 / 1e9 * 1e3, HPL * lam * 1e-9 / CL, HPL / (lam * 1e-9), E1 * L_AV], ' J', key, f=lambda v: sci(v, 3))
    ans = f'{sci(E1, 3)} J'
    if D >= 4:
        st += f' Calculate ΔE in kJ mol⁻¹ (L = 6.02 × 10²³ mol⁻¹) and predict the colour of the complex.'
        key = key.replace(' [3]', '') + f'; × L ÷ 1000 = {g3(Em)} kJ mol⁻¹ [1]; absorbs {ab}, appears {comp} [1] [5]'
        ans += f'; {g3(Em)} kJ mol⁻¹; absorbs {ab} light so appears {comp}' + (f' (observed: {seen})' if f else '')
    return Q(st, ans, key, 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def col_pred(r, D):
    lo, hi, ab, comp = r.choice(COLOURS)
    lam = r.randrange(lo, hi, 5)
    if D <= 2:
        return MQ(r, f'A solution of a transition metal complex absorbs light mainly at {lam} nm ({ab}). What colour does the solution appear?', cap(comp), [cap(c[3]) for c in COLOURS if c[3] != comp][:3] + [cap(ab)], f'Absorbs {ab}; transmits the complementary colour, {comp}.')
    st = f'A solution of a complex absorbs light mainly at {lam} nm ({ab}). Predict its colour and explain why it is coloured.'
    ans = f'{cap(comp)}: ligands split the d orbitals; {ab} light of energy ΔE is absorbed as an electron is promoted; the complementary colour is transmitted.'
    key = f'{comp} [1]; d-orbital splitting [1]; absorption / electron promoted [1] [3]'
    if D >= 4:
        st += ' Predict how the wavelength absorbed would change if the ligands were replaced by ligands that cause a larger splitting.'
        ans += ' Larger ΔE means higher-energy light is absorbed, so a shorter wavelength.'
        key = key.replace(' [3]', '') + '; shorter wavelength with reason [1] [4]'
    return Q(st, ans, key, 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def colour_case(r, D):
    k_ = r.choice([0.40, 0.52, 0.65, 0.80, 1.10])  # absorbance per 0.0100 mol dm⁻³... scaled
    slope = k_ / 0.0100
    cu = r.choice([0.0042, 0.0055, 0.0068, 0.0074, 0.0081])
    A = round(slope * cu, 2)
    cfound = A / slope
    st = (f'{who(r)} uses colorimetry to find the concentration of copper(II) ions in a sample of waste water from a factory in {city(r)}. Excess aqueous ammonia is added to form the deep blue complex [Cu(NH₃)₄(H₂O)₂]²⁺. '
          f'Standards give a straight calibration line with absorbance {fx(k_, 2)} at 0.0100 mol dm⁻³ (passing through the origin). The sample gives an absorbance of {fx(A, 2)}.')
    parts = [P_('Explain why excess ammonia is added before measuring the absorbance.', 'To convert all Cu²⁺ into the intensely coloured ammine complex, which absorbs more strongly than [Cu(H₂O)₆]²⁺, improving sensitivity.', '[2]'),
             P_('Calculate the concentration of copper(II) ions in the sample.', f'{g3(cfound)} mol dm⁻³', f'conc = {fx(A, 2)} ÷ {fx(k_, 2)} × 0.0100 [1]; = {g3(cfound)} mol dm⁻³ [1] [2]'),
             P_('Suggest the colour of filter that should be used and explain your choice.', 'An orange/red filter: the blue complex absorbs orange/red light most strongly, giving the greatest change in absorbance with concentration.', 'complementary colour filter [1]; reason [1] [2]'),
             P_('Explain, in terms of d orbitals, why the ammine complex has a different colour from the aqua complex.', 'NH₃ splits the d orbitals more than H₂O (larger ΔE), so a shorter wavelength of light is absorbed and the transmitted colour changes from pale blue to deep blue.', 'different ΔE [1]; different wavelength absorbed [1] [2]'),
             P_('Explain why a solution of Zn²⁺ ions treated in the same way would give no absorbance in the visible region.', 'Zn²⁺ is 3d¹⁰; there is no space in the upper d orbitals for an electron to be promoted, so no d–d transitions.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain why transition metal complexes are coloured and why the colour depends on the ligands and the geometry of the complex.', 'Five degenerate d orbitals split when ligands approach; octahedral: two higher (dz², dx²−y²), three lower; tetrahedral: reverse, smaller split; d–d transition absorbs visible light of energy ΔE = hc/λ; complementary colour transmitted; different ligands (NH₃ > H₂O > Cl⁻) give different ΔE; examples [Cu(H₂O)₆]²⁺ pale blue, [Cu(NH₃)₄(H₂O)₂]²⁺ deep blue, [CuCl₄]²⁻ yellow; d⁰ and d¹⁰ colourless.',
           'splitting in octahedral [2]; tetrahedral [1]; absorption and complementary colour [2]; ligand effect with examples [1]; d⁰/d¹⁰ [1] [7]')])
t6c = t

# ---------------------------------------------------------------------
KST = [('[Cu(NH₃)₄(H₂O)₂]²⁺', '[Cu(H₂O)₆]²⁺', 'NH₃', 4, 13.1, '[Cu(H₂O)₆]²⁺ + 4NH₃ ⇌ [Cu(NH₃)₄(H₂O)₂]²⁺ + 4H₂O'),
       ('[CuCl₄]²⁻', '[Cu(H₂O)₆]²⁺', 'Cl⁻', 4, 5.6, '[Cu(H₂O)₆]²⁺ + 4Cl⁻ ⇌ [CuCl₄]²⁻ + 6H₂O'),
       ('[Cu(EDTA)]²⁻', '[Cu(H₂O)₆]²⁺', 'EDTA⁴⁻', 1, 18.8, '[Cu(H₂O)₆]²⁺ + EDTA⁴⁻ ⇌ [Cu(EDTA)]²⁻ + 6H₂O'),
       ('[Ni(NH₃)₆]²⁺', '[Ni(H₂O)₆]²⁺', 'NH₃', 6, 8.6, '[Ni(H₂O)₆]²⁺ + 6NH₃ ⇌ [Ni(NH₃)₆]²⁺ + 6H₂O'),
       ('[Ni(en)₃]²⁺', '[Ni(H₂O)₆]²⁺', 'en', 3, 18.3, '[Ni(H₂O)₆]²⁺ + 3en ⇌ [Ni(en)₃]²⁺ + 6H₂O'),
       ('[Ag(NH₃)₂]⁺', 'Ag⁺', 'NH₃', 2, 7.2, 'Ag⁺ + 2NH₃ ⇌ [Ag(NH₃)₂]⁺'),
       ('[Ag(S₂O₃)₂]³⁻', 'Ag⁺', 'S₂O₃²⁻', 2, 13.5, 'Ag⁺ + 2S₂O₃²⁻ ⇌ [Ag(S₂O₃)₂]³⁻'),
       ('[Ag(CN)₂]⁻', 'Ag⁺', 'CN⁻', 2, 21.1, 'Ag⁺ + 2CN⁻ ⇌ [Ag(CN)₂]⁻'),
       ('[Co(NH₃)₆]²⁺', '[Co(H₂O)₆]²⁺', 'NH₃', 6, 5.1, '[Co(H₂O)₆]²⁺ + 6NH₃ ⇌ [Co(NH₃)₆]²⁺ + 6H₂O')]


def kst_units(n):
    return f'dm{sup(3 * n)} mol{sup(-n)}' if n > 1 else 'dm³ mol⁻¹'


def kst_expr(cx, aq, lig, n):
    return f'[{cx}] ÷ ([{aq}][{lig}]' + (sup(n) if n > 1 else '') + ')'


t = T('Ligand exchange and stability constants Kstab', 'ligand exchange and stability constants kstab')
facts(t, [('ligand exchange', 'a reaction in which one or more ligands in a complex are replaced by other ligands'),
          ('stability constant', 'Kstab: the equilibrium constant for the formation of a complex ion in a solvent from its constituent ions or molecules'),
          ('chelate effect', 'the greater stability of complexes formed by polydentate ligands, due to the increase in the number of particles (entropy) when they replace monodentate ligands'),
          ('log Kstab', 'the logarithm of the stability constant, used to compare stabilities of complexes because Kstab values are very large'),
          ('chelate', 'a complex in which a polydentate ligand forms a ring with the central metal ion')])
mcqs(t, [('What is the Kstab expression for Ag⁺ + 2NH₃ ⇌ [Ag(NH₃)₂]⁺?', '[[Ag(NH₃)₂]⁺] ÷ ([Ag⁺][NH₃]²)', 'Water concentration is omitted.', ['[Ag⁺][NH₃]² ÷ [[Ag(NH₃)₂]⁺]', '[[Ag(NH₃)₂]⁺] ÷ ([Ag⁺][NH₃])', '[[Ag(NH₃)₂]⁺] ÷ [Ag⁺]']),
         ('Why is [H₂O] not included in Kstab expressions for aqueous complexes?', 'Water is in large excess, so its concentration is effectively constant', 'Absorbed into the constant.', ['Water is not a ligand', 'Water is a product', 'Water is a gas']),
         ('Which complex is the most stable? log Kstab: [Cu(NH₃)₄(H₂O)₂]²⁺ 13.1; [CuCl₄]²⁻ 5.6; [Cu(EDTA)]²⁻ 18.8', '[Cu(EDTA)]²⁻', 'Largest log Kstab.', ['[CuCl₄]²⁻', '[Cu(NH₃)₄(H₂O)₂]²⁺', '[Cu(H₂O)₆]²⁺'])])
mcqs(t, [('Why does EDTA⁴⁻ readily replace six water ligands around Cu²⁺?', 'The number of particles increases from 2 to 7, so entropy increases (chelate effect)', 'ΔS positive, ΔG negative.', ['EDTA⁴⁻ is a stronger acid', 'Cu–O bonds are weaker than Cu–N bonds', 'Water is a bidentate ligand']),
         ('Carbon monoxide is toxic because', 'it forms a more stable complex with the Fe²⁺ in haemoglobin than O₂ does', 'Higher Kstab for CO; ligand exchange.', ['it oxidises Fe²⁺ to Fe³⁺', 'it denatures haemoglobin', 'it is a bidentate ligand'])], D=(2, 3), C='C2')
shorts(t, [('Write the expression for Kstab of [Cu(NH₃)₄(H₂O)₂]²⁺ and give its units.', f'Kstab = [[Cu(NH₃)₄(H₂O)₂]²⁺] ÷ ([[Cu(H₂O)₆]²⁺][NH₃]⁴); {kst_units(4)}', 'expression [1]; units [1] [2]')])
explain(t, [('Explain how log Kstab values are used to predict whether a ligand exchange reaction occurs.', 'A ligand will replace another if the new complex has a larger Kstab (more stable); the equilibrium lies towards the complex with the larger stability constant.', '[2]'),
            ('Explain the chelate effect using the reaction of [Ni(H₂O)₆]²⁺ with ethane-1,2-diamine.', '[Ni(H₂O)₆]²⁺ + 3en → [Ni(en)₃]²⁺ + 6H₂O; 4 particles become 7, so ΔS is positive; ΔH is small (similar Ni–N bonds), so ΔG is negative and the chelate is much more stable.', 'equation / particle count [1]; ΔS positive [1]; ΔG negative [1] [3]'),
            ('Explain why the Kstab of the haemoglobin–CO complex is important in carbon monoxide poisoning.', 'CO binds to Fe²⁺ in haemoglobin far more strongly than O₂ (larger Kstab); ligand exchange of O₂ by CO is effectively irreversible, so oxygen transport is reduced.', '[2]')])
myths(t, [('A larger Kstab means the complex forms faster.', 'Kstab measures the position of equilibrium (stability), not the rate of formation.'),
          ('Ligand exchange always changes the coordination number.', 'It may or may not; NH₃ replacing H₂O keeps 6, but Cl⁻ replacing H₂O gives a 4-coordinate complex.'),
          ('The chelate effect is mainly due to stronger metal–ligand bonds.', 'It is mainly an entropy effect: more particles are released when a polydentate ligand replaces monodentate ones.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def kstab_calc(r, D):
    cx, aq, lig, n, lk, eq = r.choice(KST)
    K = 10 ** lk
    Lc = r.choice([0.10, 0.20, 0.50, 1.0]) if n > 1 else r.choice([0.010, 0.020, 0.050])
    cc = r.choice([0.020, 0.050, 0.10])
    Mc = float(f'{cc / (K * Lc ** n):.3g}')
    Kc = cc / (Mc * Lc ** n)
    mode = r.choice(['K', 'M']) if D >= 3 else 'K'
    expr = kst_expr(cx, aq, lig, n)
    if mode == 'K':
        st = f'For the equilibrium {eq}, the equilibrium concentrations are [{cx}] = {fx(cc, 3)}, [{aq}] = {sci(Mc, 3)} and [{lig}] = {fx(Lc, 3)} mol dm⁻³. Calculate Kstab and give its units.'
        key = f'Kstab = {expr} [1]; = {fx(cc, 3)} ÷ ({sci(Mc, 3)} × {fx(Lc, 3)}{sup(n) if n > 1 else ""}) = {sci(Kc, 3)} [1]; units {kst_units(n)} [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate Kstab and give its units.', 'What is the value of Kstab?'), Kc, [1 / Kc, cc / (Mc * Lc), Kc * Lc, Mc * Lc ** n / cc], '', key, f=lambda v: sci(v, 3))
        ans = f'{sci(Kc, 3)} {kst_units(n)}'
        if D >= 4:
            st += ' Calculate log Kstab.'
            ans += f'; log Kstab = {fx(math.log10(Kc), 2)}'
            key = key.replace(' [3]', '') + f'; log Kstab = {fx(math.log10(Kc), 2)} [1] [4]'
        return Q(st, ans, key, 'numerical')
    st = f'For {eq}, log Kstab = {lk}. In a solution at equilibrium, [{lig}] = {fx(Lc, 3)} mol dm⁻³ and [{cx}] = {fx(cc, 3)} mol dm⁻³. Calculate the concentration of {aq} remaining.'
    Mr_ = cc / (K * Lc ** n)
    key = f'Kstab = 10^{lk} = {sci(K, 3)} [1]; [{aq}] = [{cx}] ÷ (Kstab × [{lig}]{sup(n) if n > 1 else ""}) [1]; = {sci(Mr_, 3)} mol dm⁻³ [1] [3]'
    ans = f'{sci(Mr_, 3)} mol dm⁻³'
    if D >= 5:
        st += ' Comment on what this shows about the stability of the complex.'
        ans += '; very small, so almost all the metal ion is complexed: the complex is very stable'
        key = key.replace(' [3]', '') + '; comment [1] [4]'
    return Q(st, ans, key, 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def kstab_pred(r, D):
    grp = r.choice([[k for k in KST if k[1] == '[Cu(H₂O)₆]²⁺'], [k for k in KST if k[1] == 'Ag⁺'], [k for k in KST if k[1] == '[Ni(H₂O)₆]²⁺'] + [k for k in KST if k[1] == '[Ni(H₂O)₆]²⁺']])
    a, b = r.sample(grp, 2)
    if a[4] == b[4]:
        return None
    lo, hi = (a, b) if a[4] < b[4] else (b, a)
    data = f'log Kstab: {lo[0]} {lo[4]}; {hi[0]} {hi[4]}'
    if D <= 2:
        return MQ(r, f'{data}. {lo[2]} is added to a solution of {hi[0]}. What happens?', f'No significant change; {hi[0]} is more stable', [f'{lo[0]} forms completely', 'The metal ion precipitates', 'Both complexes are destroyed'], f'{hi[0]} has the larger Kstab, so exchange does not occur to a significant extent.')
    return Q(f'{data}. Predict what happens when {hi[2]} is added to a solution containing {lo[0]}. Explain your answer and write an equation.',
             f'Ligand exchange: {hi[0]} forms because it has the larger Kstab (more stable complex); {lo[0]} + {hi[3] if hi[3] > 1 else ""}{hi[2]} → {hi[0]} + {lo[3] if lo[3] > 1 else ""}{lo[2]} (with water as needed).',
             f'{hi[0]} forms [1]; larger Kstab / more stable [1]; equation [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def kstab_case(r, D):
    st = f'{who(r)} investigates ligand exchange in copper(II) complexes. log Kstab: [Cu(NH₃)₄(H₂O)₂]²⁺ 13.1; [CuCl₄]²⁻ 5.6; [Cu(EDTA)]²⁻ 18.8.'
    parts = [P_('Write an expression for Kstab of [CuCl₄]²⁻ and give its units.', f'[[CuCl₄]²⁻] ÷ ([[Cu(H₂O)₆]²⁺][Cl⁻]⁴); {kst_units(4)}', 'expression [1]; units [1] [2]'),
             P_('Predict what is observed when excess aqueous ammonia is added to a yellow-green solution of [CuCl₄]²⁻. Explain using the data.', 'The solution turns deep blue as [Cu(NH₃)₄(H₂O)₂]²⁺ forms, because it has a much larger Kstab than [CuCl₄]²⁻.', 'deep blue [1]; Kstab comparison [1] [2]'),
             P_('Write an equation for the reaction of [Cu(NH₃)₄(H₂O)₂]²⁺ with EDTA⁴⁻ and explain why it occurs.', '[Cu(NH₃)₄(H₂O)₂]²⁺ + EDTA⁴⁻ → [Cu(EDTA)]²⁻ + 4NH₃ + 2H₂O; [Cu(EDTA)]²⁻ is more stable (larger Kstab); particles increase from 2 to 7 so ΔS is positive (chelate effect).', 'equation [1]; Kstab [1]; entropy / chelate effect [1] [3]'),
             P_('Suggest why EDTA is used in the treatment of heavy-metal poisoning.', 'It forms very stable, soluble chelates with metal ions (large Kstab), which can be excreted.', '[1]'),
             P_('Explain why the Kstab values are quoted as logarithms.', 'The values cover a very large range (10⁵ to 10¹⁹), so logarithms are easier to compare.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain what is meant by ligand exchange and stability constant, and use examples to show how Kstab values and the chelate effect determine which complexes form.', 'Ligand exchange definition with equations (Cu²⁺ with NH₃ and Cl⁻; Co²⁺ with Cl⁻); Kstab expression and units; water omitted; larger Kstab means more stable, equilibrium favours it; log Kstab comparison; chelate effect: EDTA⁴⁻ / en, increase in particles, positive ΔS; haemoglobin and CO.',
           'definition and example [2]; Kstab expression [1]; using values to predict [2]; chelate effect [1]; CO/haemoglobin or EDTA application [1] [7]')])
t6d = t

# ---------------------------------------------------------------------
t = T('Redox chemistry of transition elements: MnO4⁻ and Cr2O7²⁻ titrations', 'redox chemistry of transition elements')
facts(t, [('self-indicating titration', 'a titration in which a reagent acts as its own indicator, e.g. MnO₄⁻, whose end point is the first permanent pale pink colour'),
          ('acidified potassium manganate(VII)', 'a strong oxidising agent, MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O, used in redox titrations'),
          ('acidified potassium dichromate(VI)', 'an oxidising agent, Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O, orange changing to green'),
          ('iodometric titration', 'a titration in which iodine released by an oxidising agent is titrated with sodium thiosulfate using starch indicator'),
          ('mole ratio', 'the ratio of the amounts of reactants in a balanced equation, used to convert moles of titrant to moles of analyte')])
mcqs(t, [('What is the mole ratio MnO₄⁻ : Fe²⁺ in an acidified redox titration?', '1 : 5', 'MnO₄⁻ gains 5e⁻; each Fe²⁺ loses 1e⁻.', ['1 : 1', '1 : 6', '2 : 5']),
         ('What is the mole ratio Cr₂O₇²⁻ : Fe²⁺?', '1 : 6', 'Cr₂O₇²⁻ gains 6e⁻.', ['1 : 5', '1 : 3', '2 : 3']),
         ('What is the colour change at the end point of a manganate(VII) titration of Fe²⁺?', 'Colourless to pale pink', 'First excess MnO₄⁻ remains pink.', ['Pink to colourless', 'Orange to green', 'Blue-black to colourless']),
         ('Why is dilute sulfuric acid, not hydrochloric acid, used to acidify manganate(VII) titrations?', 'MnO₄⁻ would oxidise Cl⁻ to chlorine', 'This would use extra MnO₄⁻.', ['HCl is too weak an acid', 'Sulfuric acid is a catalyst', 'HCl reacts with Fe²⁺'])])
mcqs(t, [('What is the mole ratio MnO₄⁻ : C₂O₄²⁻ in the titration of ethanedioate ions?', '2 : 5', '2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O.', ['1 : 5', '5 : 2', '1 : 2']),
         ('In the titration of ethanedioate with MnO₄⁻, the reaction speeds up after the first few drops because', 'Mn²⁺ formed acts as a catalyst (autocatalysis)', 'Product catalyses the reaction.', ['the solution cools', 'MnO₄⁻ concentration increases', 'CO₂ is a catalyst']),
         ('In the iodometric analysis of copper(II), how many moles of thiosulfate react per mole of Cu²⁺?', '1', '2Cu²⁺ → I₂ → 2S₂O₃²⁻.', ['2', '0.5', '4'])], D=(2, 3), C='C2')
shorts(t, [('Write the ionic equation for the reaction of MnO₄⁻ with Fe²⁺ in acidic solution.', 'MnO₄⁻ + 8H⁺ + 5Fe²⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 'species [1]; balanced [1] [2]'),
           ('Write the ionic equation for the reaction of Cr₂O₇²⁻ with Fe²⁺ in acidic solution.', 'Cr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O', 'species [1]; balanced [1] [2]')])
explain(t, [('Explain why no indicator is needed in a manganate(VII) titration.', 'MnO₄⁻ is intensely purple and Mn²⁺ is almost colourless; the first drop in excess gives a permanent pale pink colour, which marks the end point.', '[2]'),
            ('Explain why the ethanedioate solution is warmed to about 60 °C before titration with MnO₄⁻.', 'The reaction is slow at room temperature (high activation energy) until Mn²⁺ forms; warming increases the rate so the end point is sharp.', '[2]'),
            ('Explain how a redox titration with thiosulfate is used to find the percentage of copper in brass.', 'Dissolve brass in nitric acid; neutralise, add excess KI: 2Cu²⁺ + 4I⁻ → 2CuI + I₂; titrate I₂ with thiosulfate (I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻) using starch near the end point; n(Cu) = n(S₂O₃²⁻).', 'iodine liberated [1]; titration with starch [1]; 1:1 ratio [1] [3]')])
myths(t, [('In a manganate(VII) titration, the end point is when the pink colour disappears.', 'MnO₄⁻ is in the burette; the end point is the first permanent pale pink colour.'),
          ('MnO₄⁻ reacts with Fe²⁺ in a 1 : 1 ratio.', 'MnO₄⁻ gains 5 electrons and Fe²⁺ loses 1, so the ratio is 1 : 5.'),
          ('Starch should be added at the start of an iodine–thiosulfate titration.', 'Starch is added near the end point (pale yellow) so that the iodine–starch complex does not form irreversibly at high iodine concentration.')])

TITS = {
    'fe_mn': ('MnO₄⁻', 'potassium manganate(VII)', 'Fe²⁺', 1, 5, 'MnO₄⁻ + 8H⁺ + 5Fe²⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 'colourless to pale pink'),
    'fe_cr': ('Cr₂O₇²⁻', 'potassium dichromate(VI)', 'Fe²⁺', 1, 6, 'Cr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O', 'green to violet-blue (with a redox indicator)'),
    'ox_mn': ('MnO₄⁻', 'potassium manganate(VII)', 'C₂O₄²⁻', 2, 5, '2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O', 'colourless to pale pink'),
    'h2o2_mn': ('MnO₄⁻', 'potassium manganate(VII)', 'H₂O₂', 2, 5, '2MnO₄⁻ + 5H₂O₂ + 6H⁺ → 2Mn²⁺ + 5O₂ + 8H₂O', 'colourless to pale pink'),
    'cu_thio': ('S₂O₃²⁻', 'sodium thiosulfate', 'Cu²⁺', 1, 1, '2Cu²⁺ + 4I⁻ → 2CuI + I₂, then I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻', 'blue-black to colourless (starch, added near the end point)')}


def titre_setup(r, kind):
    tf, tname, an, a, b, eq, ep = TITS[kind]
    c = r.choice([0.0200, 0.0100, 0.0150, 0.0500] if kind != 'cu_thio' else [0.100, 0.0800, 0.120])
    if kind in ('fe_cr',):
        c = r.choice([0.0167, 0.0200, 0.0100])
    V = round(r.uniform(14.0, 38.0) * 20) / 20
    n_t = c * V / 1000
    n_a = n_t * b / a
    return tf, tname, an, a, b, eq, ep, c, V, n_t, n_a


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def redox_titr(r, D):
    kind = r.choice(['fe_mn', 'fe_cr', 'ox_mn', 'h2o2_mn', 'cu_thio'])
    tf, tname, an, a, b, eq, ep, c, V, n_t, n_a = titre_setup(r, kind)
    base = f'{V:.2f} cm³ of {fx(c, 4)} mol dm⁻³ {tname} reacted with 25.0 cm³ of a solution containing {an} ions' if kind != 'cu_thio' else f'Excess KI was added to 25.0 cm³ of a copper(II) solution; the iodine released needed {V:.2f} cm³ of {fx(c, 4)} mol dm⁻³ sodium thiosulfate'
    base = base.replace('containing H₂O₂ ions', 'of hydrogen peroxide').replace('containing C₂O₄²⁻ ions', 'of ethanedioate ions')
    key1 = f'n({tf}) = {fx(c, 4)} × {V:.2f} ÷ 1000 = {sci(n_t, 3)} mol [1]; n({an}) = × {b}/{a} = {sci(n_a, 3)} mol [1]'
    if D <= 2:
        return NQ(r, f'{base}. Equation: {eq}. How many moles of {an} were in the 25.0 cm³ sample?', n_a, [n_t, n_t * a / b, n_a * 10, n_t * b], ' mol', key1 + ' [2]', f=lambda v: sci(v, 3))
    conc = n_a / 0.025
    st = f'{base}. Equation: {eq}. Calculate the concentration of {an} in the sample.'
    key = key1 + f'; concentration = {sci(n_a, 3)} ÷ 0.0250 = {g3(conc)} mol dm⁻³ [1]'
    ans = f'{g3(conc)} mol dm⁻³'
    tot = 3
    if D >= 4:
        if kind in ('fe_mn', 'fe_cr'):
            st += ' The 25.0 cm³ sample was taken from 250 cm³ of solution made by dissolving iron tablets in dilute sulfuric acid. Calculate the total mass of iron in the tablets.'
            mass = n_a * 10 * 55.8
            key += f'; × 10 = {sci(n_a * 10, 3)} mol; × 55.8 = {g3(mass)} g [1]'
            ans += f'; mass of iron = {g3(mass)} g'
        elif kind == 'h2o2_mn':
            st += ' The sample had been made by diluting 10.0 cm³ of a hair bleach to 250 cm³. Calculate the concentration of H₂O₂ in the bleach in g dm⁻³.'
            cb = conc * 25
            key += f'; × 25 = {g3(cb)} mol dm⁻³; × 34.0 = {g3(cb * 34.0)} g dm⁻³ [1]'
            ans += f'; bleach {g3(cb)} mol dm⁻³ = {g3(cb * 34.0)} g dm⁻³'
        elif kind == 'ox_mn':
            st += ' The sample came from 250 cm³ of a solution made from impure ethanedioic acid crystals, H₂C₂O₄·2H₂O (Mr 126.0). Calculate the mass of pure crystals present.'
            key += f'; × 10 × 126.0 = {g3(n_a * 10 * 126.0)} g [1]'
            ans += f'; {g3(n_a * 10 * 126.0)} g'
        else:
            st += ' The 25.0 cm³ sample came from 250 cm³ of solution made by dissolving a brass sample in nitric acid. Calculate the mass of copper in the brass.'
            key += f'; × 10 × 63.5 = {g3(n_a * 10 * 63.5)} g [1]'
            ans += f'; {g3(n_a * 10 * 63.5)} g'
        tot += 1
    if D >= 5:
        st += ' State the colour change at the end point.'
        key += f'; {ep} [1]'
        ans += f'; end point {ep}'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'numerical')


@t.add('C3', (3, 4, 5), 'numerical')
def hydrate_x(r, D):
    x = r.choice([6, 7, 7, 5, 4])
    Mr_ = 151.9 + 18.0 * x
    mass = round(r.uniform(5.5, 8.0), 2)
    n_tot = mass / Mr_
    n_al = n_tot / 10
    c = 0.0200
    V = n_al / 5 / c * 1000
    Vr = round(V * 20) / 20
    if not 12 <= Vr <= 45:
        return None
    n_t = c * Vr / 1000
    n_fe = n_t * 5 * 10
    Mc = mass / n_fe
    xc = (Mc - 151.9) / 18.0
    st = (f'{fx(mass, 2)} g of hydrated iron(II) sulfate, FeSO₄·xH₂O, was dissolved in dilute sulfuric acid and made up to 250 cm³. 25.0 cm³ portions needed a mean titre of {Vr:.2f} cm³ of 0.0200 mol dm⁻³ KMnO₄. '
          f'Calculate the value of x. (Mr of FeSO₄ = 151.9)')
    key = f'n(MnO₄⁻) = {sci(n_t, 3)} [1]; n(Fe²⁺) in 25.0 cm³ = {sci(n_t * 5, 3)} [1]; in 250 cm³ = {sci(n_fe, 3)} [1]; Mr = {g3(Mc)} [1]; x = ({g3(Mc)} − 151.9) ÷ 18.0 = {fx(xc, 2)} ≈ {round(xc)} [1] [5]'
    return Q(st, f'x = {round(xc)} (calculated {fx(xc, 2)})', key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def titr_case(r, D):
    kind = r.choice(['fe_mn', 'fe_cr'])
    tf, tname, an, a, b, eq, ep, c, V, n_t, n_a = titre_setup(r, kind)
    mt = round(r.uniform(1.2, 2.6), 2)
    fe = n_a * 10 * 55.8
    pc = fe / mt * 100
    if pc > 60:
        return None
    st = (f'{who(r)} in {lab(r)} analyses an iron supplement. {mt:.2f} g of crushed tablets were dissolved in dilute sulfuric acid and made up to 250 cm³. 25.0 cm³ portions were titrated with {fx(c, 4)} mol dm⁻³ {tname}; the mean titre was {V:.2f} cm³.')
    parts = [P_('Write the ionic equation for the titration reaction.', eq, '[1]'),
             P_('Calculate the percentage by mass of iron in the tablets.', f'{g3(pc)}%', f'n({tf}) = {sci(n_t, 3)} [1]; n(Fe²⁺) = {sci(n_a, 3)} in 25.0 cm³ [1]; × 10 × 55.8 = {g3(fe)} g [1]; % = {g3(pc)} [1] [4]'),
             P_('Explain why dilute sulfuric acid is used rather than hydrochloric acid.', 'The oxidising agent would oxidise Cl⁻ ions to chlorine, using extra titrant and giving a high titre.', '[2]'),
             P_('State how the end point is detected.', ep.capitalize() + '.', '[1]'),
             P_('Suggest why the results might underestimate the iron content if the solution was left in air for a long time before titration.', 'Some Fe²⁺ is oxidised by air to Fe³⁺, which does not react with the titrant, so the titre is lower.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how redox titrations with acidified potassium manganate(VII) and potassium dichromate(VI) are used to determine the amount of iron(II) in a sample, including equations, end points and a specimen calculation.', 'Half-equations MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O, Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O, Fe²⁺ → Fe³⁺ + e⁻; overall equations and ratios 1:5 and 1:6; sulfuric acid not HCl; MnO₄⁻ self-indicating (pale pink), dichromate needs redox indicator; procedure; calculation from titre to moles to mass/percentage; sources of error (air oxidation).',
           'half-equations and ratios [2]; acid choice [1]; end points [1]; procedure [1]; calculation [2] [7]')])
t6e = t

CHAPTERS[6] = [t6a, t6b, t6c, t6d, t6e]


# ===================================================================== 7 Benzene and its compounds
t = T('Bonding in benzene: delocalised π system and stability compared with the Kekulé model', 'bonding in benzene')
facts(t, [('delocalised electrons', 'electrons that are shared between more than two atoms, as in the ring of six p electrons in benzene'),
          ('Kekulé structure', 'a model of benzene as a ring of six carbon atoms with alternating C–C single and C=C double bonds'),
          ('π bond', 'a bond formed by sideways overlap of p orbitals above and below the plane of the bonded atoms'),
          ('delocalisation energy', 'the extra stability of benzene compared with the hypothetical Kekulé structure, shown by its less exothermic enthalpy change of hydrogenation'),
          ('arene', 'a hydrocarbon containing one or more benzene rings'),
          ('sp² hybridisation', 'mixing of one s and two p orbitals to give three orbitals in a plane at 120°, as for each carbon in benzene')])
mcqs(t, [('What are the C–C–C bond angles in benzene?', '120°', 'Planar hexagon, sp² carbons.', ['109.5°', '90°', '180°']),
         ('How many electrons are in the delocalised π system of benzene?', '6', 'One p electron from each carbon.', ['3', '12', '2']),
         ('What is the length of the carbon–carbon bonds in benzene compared with C–C (0.154 nm) and C=C (0.134 nm)?', 'All 0.139 nm, between the two', 'All bonds equal and intermediate.', ['Alternating 0.154 and 0.134 nm', 'All 0.154 nm', 'All 0.134 nm']),
         ('What type of hybridisation do the carbon atoms in benzene show?', 'sp²', 'Three σ bonds in a plane plus one p orbital.', ['sp³', 'sp', 'None'])])
mcqs(t, [('Why does benzene not decolourise bromine water, unlike cyclohexene?', 'Addition would destroy the stable delocalised π system', 'Benzene prefers substitution.', ['Benzene has no π electrons', 'Bromine is not an electrophile', 'Benzene is saturated']),
         ('The enthalpy change of hydrogenation of benzene is less exothermic than three times that of cyclohexene. This shows that', 'benzene is more stable than the Kekulé structure suggests', 'Delocalisation energy.', ['benzene has three C=C bonds', 'benzene is less stable than cyclohexene', 'hydrogenation of benzene is endothermic'])], D=(2, 3), C='C2')
shorts(t, [('Describe how the delocalised π system in benzene is formed.', 'Each carbon has one p orbital (perpendicular to the ring) containing one electron; the six p orbitals overlap sideways to form a ring of π electron density above and below the plane.', 'p orbitals overlap sideways [1]; rings above and below plane [1] [2]')])
explain(t, [('Explain three pieces of evidence that the Kekulé structure of benzene is incorrect.', 'All C–C bond lengths are equal (0.139 nm); enthalpy change of hydrogenation is about 152 kJ mol⁻¹ less exothermic than predicted; benzene does not readily undergo addition (does not decolourise bromine water).', 'bond lengths [1]; hydrogenation enthalpy [1]; lack of addition [1] [3]'),
            ('Explain why benzene undergoes substitution rather than addition reactions.', 'Substitution keeps the delocalised π system and its stabilisation; addition would destroy it, which is energetically unfavourable.', '[2]'),
            ('Explain why benzene is planar.', 'Each carbon is sp² hybridised with three σ bonds at 120° in a plane; the p orbitals overlap best when the ring is flat.', '[2]')])
myths(t, [('Benzene has three C=C double bonds that are very reactive.', 'The six π electrons are delocalised over all six carbons; benzene is much less reactive towards addition than alkenes.'),
          ('Benzene has alternating single and double bonds of different lengths.', 'All six C–C bonds are the same length, 0.139 nm.'),
          ('Delocalisation makes benzene less stable than cyclohexa-1,3,5-triene.', 'Delocalisation makes benzene more stable, by about 152 kJ mol⁻¹.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def hydrog(r, D):
    h1 = r.choice([-118, -119, -120, -121])
    hb = r.choice([-205, -207, -208, -210])
    pred = 3 * h1
    stab = hb - pred
    base = f'The enthalpy change of hydrogenation of cyclohexene is {m(h1)} kJ mol⁻¹ and that of benzene is {m(hb)} kJ mol⁻¹.'
    st = base + ' Calculate the predicted value for the Kekulé structure (cyclohexa-1,3,5-triene) and hence the stabilisation (delocalisation) energy of benzene.'
    key = f'predicted = 3 × ({m(h1)}) = {m(pred)} kJ mol⁻¹ [1]; stabilisation = {m(pred)} − ({m(hb)}) = {abs(stab)} kJ mol⁻¹ [1] [2]'
    if D <= 2:
        return NQ(r, base + ' What is the delocalisation (stabilisation) energy of benzene?', abs(stab), [abs(pred), abs(hb), abs(h1) * 2 - abs(hb) if abs(h1) * 2 != abs(hb) else 99, abs(stab) / 3], ' kJ mol⁻¹', key, f=lambda v: str(int(round(v))))
    ans = f'predicted {m(pred)} kJ mol⁻¹; stabilisation energy {abs(stab)} kJ mol⁻¹'
    if D >= 3:
        st += ' Write an equation for the hydrogenation of benzene and state the conditions.'
        key = key.replace(' [2]', '') + '; C₆H₆ + 3H₂ → C₆H₁₂ [1]; nickel catalyst, heat (about 150 °C), high pressure [1] [4]'
        ans += '; C₆H₆ + 3H₂ → C₆H₁₂ (Ni catalyst, heat, pressure)'
    if D >= 5:
        st += ' Explain what your answer shows about the structure of benzene.'
        key = key.replace(' [4]', '') + '; benzene is more stable than Kekulé; delocalised π system [1] [5]'
        ans += '; benzene is more stable than the Kekulé structure because its π electrons are delocalised'
    return Q(st, ans, key, 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def kekule_ev(r, D):
    ev = [('bond lengths', 'X-ray diffraction shows all six C–C bonds are 0.139 nm, between C–C (0.154 nm) and C=C (0.134 nm)', 'Kekulé predicts alternating long and short bonds'),
          ('enthalpy of hydrogenation', 'hydrogenation of benzene releases about 152 kJ mol⁻¹ less energy than three times that of cyclohexene', 'Kekulé predicts about −360 kJ mol⁻¹'),
          ('reaction with bromine', 'benzene does not decolourise bromine water at room temperature', 'Kekulé predicts rapid electrophilic addition like an alkene'),
          ('number of isomers', 'only one 1,2-disubstituted benzene (e.g. 1,2-dibromobenzene) exists', 'Kekulé predicts two isomers (Br atoms across a single or a double bond)')]
    a = r.choice(ev)
    if D <= 2:
        return MQ(r, f'Which observation about {a[0]} is evidence against the Kekulé structure of benzene?', cap(a[1]), ['Benzene burns with a smoky flame', 'Benzene is a liquid at room temperature', 'Benzene has the formula C₆H₆'], f'{cap(a[1])}; {a[2]}.')
    b = r.choice([e for e in ev if e != a])
    return Q(f'Describe and explain two pieces of evidence, one involving {a[0]} and one involving {b[0]}, that show benzene does not have the Kekulé structure.', f'{cap(a[1])} ({a[2]}); {b[1]} ({b[2]}). Both show the π electrons are delocalised.',
             'first evidence [1]; contrast with Kekulé prediction [1]; second evidence [1]; contrast [1] [4]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def benz_case(r, D):
    h1 = r.choice([-119, -120])
    hb = r.choice([-208, -207])
    st = f'{who(r)} compares cyclohexene and benzene. The enthalpy changes of hydrogenation are {m(h1)} kJ mol⁻¹ (cyclohexene) and {m(hb)} kJ mol⁻¹ (benzene).'
    parts = [P_('Use the data to calculate the delocalisation energy of benzene.', f'{abs(hb - 3 * h1)} kJ mol⁻¹', f'3 × ({m(h1)}) = {m(3 * h1)} [1]; difference {abs(hb - 3 * h1)} kJ mol⁻¹ [1] [2]'),
             P_('Describe the bonding in benzene, including the type of orbital overlap.', 'Planar ring of sp² carbons with C–C and C–H σ bonds at 120°; one p orbital on each carbon overlaps sideways with both neighbours, giving a delocalised ring of six π electrons above and below the plane.', 'σ framework [1]; p orbital overlap [1]; delocalised ring of 6 electrons [1] [3]'),
             P_('Compare the reactions of cyclohexene and benzene with bromine at room temperature.', 'Cyclohexene decolourises bromine rapidly by electrophilic addition; benzene does not react without a halogen carrier, and then undergoes substitution.', 'cyclohexene addition [1]; benzene no reaction / substitution with catalyst [1] [2]'),
             P_('Explain why the π electrons in benzene are less available to electrophiles than those in cyclohexene.', 'In benzene the π electrons are spread over six carbons (lower electron density) whereas in cyclohexene they are localised between two carbons (high electron density), so an electrophile is less strongly attracted/polarised.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the structure and bonding of benzene and evaluate the evidence that it is not adequately described by the Kekulé model.', 'σ framework of sp² carbons, planar, 120°; overlapping p orbitals form delocalised π ring of six electrons; Kekulé: alternating single/double; evidence: equal bond lengths 0.139 nm, hydrogenation 152 kJ mol⁻¹ less exothermic, resistance to addition (bromine water), one 1,2-disubstituted isomer; consequence: substitution reactions preserve delocalisation.',
           'bonding description [2]; Kekulé model [1]; evidence (three pieces) [3]; consequence for reactivity [1] [7]')])
t7a = t

# ---------------------------------------------------------------------
ESUB = [('nitration', 'concentrated nitric acid and concentrated sulfuric acid, below 55 °C', 'NO₂⁺', 'HNO₃ + 2H₂SO₄ → NO₂⁺ + 2HSO₄⁻ + H₃O⁺', 'nitrobenzene', 'C₆H₅NO₂', 123.0, 'H⁺'),
        ('bromination', 'bromine with an iron(III) bromide (or iron) catalyst, room temperature, dry', 'Br⁺', 'Br₂ + FeBr₃ → Br⁺ + FeBr₄⁻', 'bromobenzene', 'C₆H₅Br', 156.9, 'HBr'),
        ('chlorination', 'chlorine with an aluminium chloride (or iron(III) chloride) catalyst, room temperature, dry', 'Cl⁺', 'Cl₂ + AlCl₃ → Cl⁺ + AlCl₄⁻', 'chlorobenzene', 'C₆H₅Cl', 112.5, 'HCl'),
        ('Friedel–Crafts alkylation', 'chloromethane with an anhydrous aluminium chloride catalyst, heat under reflux', 'CH₃⁺', 'CH₃Cl + AlCl₃ → CH₃⁺ + AlCl₄⁻', 'methylbenzene', 'C₆H₅CH₃', 92.0, 'HCl'),
        ('Friedel–Crafts alkylation', 'chloroethane with an anhydrous aluminium chloride catalyst, heat under reflux', 'CH₃CH₂⁺', 'CH₃CH₂Cl + AlCl₃ → CH₃CH₂⁺ + AlCl₄⁻', 'ethylbenzene', 'C₆H₅CH₂CH₃', 106.0, 'HCl'),
        ('Friedel–Crafts acylation', 'ethanoyl chloride with an anhydrous aluminium chloride catalyst, heat under reflux', 'CH₃CO⁺', 'CH₃COCl + AlCl₃ → CH₃CO⁺ + AlCl₄⁻', 'phenylethanone', 'C₆H₅COCH₃', 120.0, 'HCl')]

t = T('Electrophilic substitution reactions of arenes: nitration, halogenation and Friedel–Crafts', 'electrophilic substitution reactions of arenes')
facts(t, [('electrophile', 'a species that accepts a pair of electrons to form a new covalent bond'),
          ('electrophilic substitution', 'a reaction in which an electrophile replaces a hydrogen atom on an arene ring'),
          ('halogen carrier', 'a Lewis acid catalyst such as FeBr₃ or AlCl₃ that polarises a halogen molecule to generate the electrophile'),
          ('nitronium ion', 'NO₂⁺, the electrophile in nitration, formed from concentrated nitric and sulfuric acids'),
          ('Friedel–Crafts reaction', 'the alkylation or acylation of an arene using a halogenoalkane or acyl chloride with an AlCl₃ catalyst'),
          ('arenium intermediate', 'the positively charged intermediate formed when an electrophile bonds to a benzene ring, in which delocalisation is partly lost')])
mcqs(t, [('What is the electrophile in the nitration of benzene?', 'NO₂⁺', 'Nitronium ion.', ['NO₂⁻', 'NO₃⁻', 'HNO₃']),
         ('What is the role of AlCl₃ in Friedel–Crafts acylation?', 'It generates the electrophile CH₃CO⁺ by accepting Cl⁻', 'Lewis acid / halogen carrier.', ['It is a nucleophile', 'It is a reducing agent', 'It removes water']),
         ('Which reagents convert benzene into nitrobenzene?', 'Concentrated HNO₃ and concentrated H₂SO₄ at below 55 °C', 'Nitrating mixture.', ['Dilute HNO₃ at room temperature', 'NaNO₂ and HCl below 10 °C', 'HNO₃ with an AlCl₃ catalyst']),
         ('Which product forms when benzene reacts with ethanoyl chloride and AlCl₃?', 'Phenylethanone', 'Acylation adds CH₃CO.', ['Ethylbenzene', 'Phenyl ethanoate', 'Benzoic acid'])])
mcqs(t, [('In the mechanism of nitration, what happens immediately after NO₂⁺ bonds to the ring?', 'An H⁺ is lost from the same carbon, restoring the delocalised system', 'Intermediate loses H⁺.', ['A nucleophile adds to the ring', 'NO₂⁺ leaves again', 'A second NO₂⁺ adds']),
         ('Why is the catalyst regenerated in the bromination of benzene?', 'H⁺ from the ring reacts with FeBr₄⁻ to form HBr and FeBr₃', 'H⁺ + FeBr₄⁻ → FeBr₃ + HBr.', ['FeBr₃ does not react at all', 'Bromine oxidises the iron', 'The product decomposes'])], D=(2, 3), C='C2')
shorts(t, [('Write an equation to show the formation of the electrophile in the nitration of benzene.', 'HNO₃ + 2H₂SO₄ → NO₂⁺ + 2HSO₄⁻ + H₃O⁺', '[1]'),
           ('State the reagents and conditions for the conversion of methylbenzene into benzoic acid.', 'Hot alkaline potassium manganate(VII), heat under reflux, then acidify (dilute H₂SO₄).', 'reagent [1]; conditions [1] [2]')])
explain(t, [('Describe the mechanism of the bromination of benzene.', 'FeBr₃ polarises Br₂ forming Br⁺ (FeBr₄⁻); π electrons of the ring attack Br⁺ forming a positive intermediate with partly broken delocalisation; C–H bond breaks, electrons return to the ring, H⁺ lost; H⁺ + FeBr₄⁻ → HBr + FeBr₃.', 'electrophile formation [1]; curly arrow from ring to Br⁺ [1]; intermediate [1]; loss of H⁺ and catalyst regenerated [1] [4]'),
            ('Explain why the temperature is kept below 55 °C in the nitration of benzene.', 'Above this, further substitution occurs to give dinitro (and trinitro) products.', '[1]'),
            ('Explain why the side chain of methylbenzene reacts with chlorine in UV light but the ring reacts with chlorine in the presence of AlCl₃.', 'UV light produces Cl radicals that substitute H on the CH₃ group (free-radical substitution); AlCl₃ generates the electrophile Cl⁺, which substitutes on the electron-rich ring (electrophilic substitution).', 'UV: free-radical on side chain [1]; AlCl₃: electrophilic on ring [1] [2]')])
myths(t, [('Benzene reacts with bromine by electrophilic addition, like ethene.', 'Benzene undergoes electrophilic substitution, which keeps the delocalised ring.'),
          ('The halogen carrier is used up in the bromination of benzene.', 'FeBr₃ is regenerated when H⁺ reacts with FeBr₄⁻, so it is a catalyst.'),
          ('Friedel–Crafts reactions can be carried out in aqueous solution.', 'AlCl₃ reacts with water, so anhydrous conditions are needed.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def esub_q(r, D):
    nm, cond, el, gen, prod, pf, M, by = r.choice(ESUB)
    if D <= 2:
        a = r.randrange(2)
        if a == 0:
            return MQ(r, f'Benzene is converted into {prod} by {nm}. What is the electrophile?', el, [e[2] for e in ESUB if e[2] != el][:3], f'{gen}.')
        return MQ(r, f'Which reagents and conditions convert benzene into {prod}?', cap(cond), [cap(e[1]) for e in ESUB if e[4] != prod][:3], f'{cap(nm)}: {cond}.')
    st = f'Benzene is converted into {prod}, {pf}. Give the reagents and conditions, name the type of reaction, and write an equation for the formation of the electrophile.'
    ans = f'{cap(cond)}; electrophilic substitution ({nm}); {gen}'
    key = 'reagents [1]; conditions [1]; electrophilic substitution [1]; equation for electrophile [1]'
    tot = 4
    if D >= 4:
        st += ' Describe the mechanism, using curly arrows in words.'
        ans += f'; mechanism: curly arrow from the π ring to {el}; positively charged intermediate (delocalisation partly lost); C–H bond breaks, electrons return to ring, H⁺ lost ({"forms " + by if by != "H⁺" else "regenerates the acid"})'
        key += '; arrow from ring to electrophile [1]; intermediate with + charge [1]; loss of H⁺ restoring ring [1]'
        tot += 3
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def esub_yield(r, D):
    nm, cond, el, gen, prod, pf, M, by = r.choice(ESUB)
    mb = r.choice([5.00, 7.80, 10.0, 15.6, 20.0, 3.90])
    yp = r.choice([55, 62, 68, 72, 80, 85])
    th = mb / 78.0 * M
    act = th * yp / 100
    st = f'{mb:.2f} g of benzene (Mr 78.0) was converted into {prod} (Mr {M:.1f}) by {nm}. The mass of purified {prod} obtained was {g3(act)} g. Calculate the percentage yield.'
    key = f'n(benzene) = {mb:.2f} ÷ 78.0 = {sci(mb / 78.0, 3)} mol [1]; theoretical mass = {g3(th)} g [1]; yield = {g3(act)} ÷ {g3(th)} × 100 = {yp}% [1] [3]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the percentage yield.', 'What is the percentage yield?'), yp, [act / mb * 100, yp * 78 / M, 100 - yp, mb / act * 100], '%', key, f=lambda v: str(int(round(v))))
    ans = f'{yp}%'
    if D >= 4:
        st += ' Suggest two reasons why the yield is less than 100%.'
        key = key.replace(' [3]', '') + '; any two: further substitution / side products; loss on purification / transfer; incomplete reaction [2] [5]'
        ans += '; e.g. some disubstitution (side products), losses during separation and purification'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def esub_case(r, D):
    nm, cond, el, gen, prod, pf, M, by = r.choice(ESUB)
    st = f'{who(r)} plans to make {prod}, {pf}, from benzene in {lab(r)} by {nm}.'
    parts = [P_('State the reagents and conditions needed.', cap(cond), 'reagents [1]; conditions [1] [2]'),
             P_('Write an equation to show how the electrophile is formed.', gen, '[1]'),
             P_('Describe the mechanism of the reaction.', f'π electrons of the ring attack {el}; arenium (positive) intermediate forms with delocalisation partly lost; C–H bond breaks and electrons return to the ring, restoring delocalisation; H⁺ lost.', 'attack by ring [1]; intermediate [1]; H⁺ lost / ring restored [1] [3]'),
             P_('Explain why benzene needs a catalyst for this reaction whereas an alkene does not.', 'Benzene\'s π electrons are delocalised (lower electron density) so it cannot polarise the reagent; a strong electrophile must be generated by the catalyst.', '[2]'),
             P_('Explain why the reaction gives a substitution product rather than an addition product.', 'Loss of H⁺ restores the stable delocalised π system; addition would destroy it.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe, with mechanisms and conditions, the electrophilic substitution reactions of benzene with nitric acid, bromine and an acyl chloride.', 'Nitration: conc HNO₃/H₂SO₄ < 55 °C, NO₂⁺ formation equation; bromination: Br₂ with FeBr₃, Br⁺ formation; acylation: CH₃COCl + AlCl₃ reflux, CH₃CO⁺; general mechanism: attack by π electrons, positive intermediate, loss of H⁺ to restore delocalisation; catalyst regeneration; products nitrobenzene, bromobenzene, phenylethanone.',
           'nitration [2]; halogenation [1]; Friedel–Crafts [1]; mechanism [2]; catalyst regeneration [1] [7]')])
t7b = t

# ---------------------------------------------------------------------
t = T('Phenol: acidity and reactions with bases, sodium and bromine water', 'phenol: acidity')
facts(t, [('phenol', 'C₆H₅OH, a compound in which an –OH group is bonded directly to a benzene ring'),
          ('phenoxide ion', 'C₆H₅O⁻, the anion formed when phenol loses H⁺; its negative charge is delocalised into the ring'),
          ('2,4,6-tribromophenol', 'the white precipitate formed when phenol reacts with bromine water at room temperature'),
          ('weak acid', 'an acid that only partly dissociates in water, such as phenol (Ka about 1.3 × 10⁻¹⁰ mol dm⁻³)'),
          ('activating group', 'a substituent such as –OH that increases the electron density of the ring and makes electrophilic substitution easier')])
mcqs(t, [('What is the order of acidity, weakest first?', 'Ethanol < water < phenol', 'Phenoxide is stabilised by delocalisation; ethoxide destabilised by alkyl group.', ['Phenol < water < ethanol', 'Water < ethanol < phenol', 'Ethanol < phenol < water']),
         ('What is formed when phenol reacts with aqueous sodium hydroxide?', 'Sodium phenoxide and water', 'Acid–base neutralisation.', ['Sodium phenoxide and hydrogen', 'Sodium benzoate and water', 'No reaction occurs']),
         ('What is observed when bromine water is added to aqueous phenol?', 'The orange solution is decolourised and a white precipitate forms', '2,4,6-tribromophenol.', ['No change', 'A yellow precipitate forms', 'Effervescence occurs']),
         ('Phenol does not react with sodium carbonate solution because', 'phenol is too weak an acid to release CO₂ from carbonate', 'Carboxylic acids do; phenol does not.', ['phenol is insoluble in water', 'phenol is a base', 'sodium carbonate is an acid'])])
mcqs(t, [('Why does phenol react with bromine water without a catalyst, unlike benzene?', 'A lone pair on O is delocalised into the ring, increasing its electron density', 'Activated ring polarises Br₂.', ['Phenol has fewer π electrons', 'Phenol is an alkene', 'Bromine water contains a catalyst']),
         ('Why is phenol more acidic than ethanol?', 'The negative charge of the phenoxide ion is delocalised over the ring', 'Stabilised conjugate base.', ['Phenol has more hydrogen atoms', 'The ethoxide ion is stabilised by its alkyl group', 'Phenol is more soluble in water'])], D=(2, 3), C='C2')
shorts(t, [('Write an equation for the reaction of phenol with sodium.', '2C₆H₅OH + 2Na → 2C₆H₅ONa + H₂', 'products [1]; balanced [1] [2]'),
           ('Write an equation for the reaction of phenol with bromine water.', 'C₆H₅OH + 3Br₂ → C₆H₂Br₃OH + 3HBr', 'tribromophenol [1]; balanced [1] [2]')])
explain(t, [('Explain why phenol is a stronger acid than ethanol.', 'In the phenoxide ion, a lone pair on oxygen overlaps with the π system so the negative charge is delocalised over the ring, stabilising the ion; in ethoxide the alkyl group pushes electron density onto O⁻, destabilising it. So phenol dissociates more.', 'phenoxide charge delocalised [1]; ethoxide destabilised by alkyl group [1]; more dissociation [1] [3]'),
            ('Explain why phenol reacts more readily than benzene with electrophiles.', 'A lone pair from the oxygen is partially delocalised into the ring, increasing the π electron density so the ring polarises electrophiles more easily; substitution occurs at the 2-, 4- and 6- positions.', 'lone pair delocalised into ring [1]; higher electron density [1]; 2,4,6 positions [1] [3]'),
            ('Explain how phenol can be distinguished from ethanol using a chemical test.', 'Add bromine water: phenol decolourises it and gives a white precipitate; ethanol gives no change. (Or: phenol gives a violet colour with neutral FeCl₃.)', 'test [1]; results for both [1] [2]')])
myths(t, [('Phenol is an alcohol, so it is less acidic than water.', 'Phenol is more acidic than water because the phenoxide ion is stabilised by delocalisation.'),
          ('Phenol reacts with sodium carbonate to give carbon dioxide.', 'Phenol is too weak an acid; only carboxylic acids react with carbonates to give CO₂.'),
          ('Phenol needs a halogen carrier to react with bromine.', 'The –OH group activates the ring, so phenol reacts with bromine water at room temperature.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def phenol_calc(r, D):
    mode = r.choice(['tbp', 'h2', 'ph']) if D >= 3 else r.choice(['tbp', 'h2'])
    if mode == 'tbp':
        mp = r.choice([0.470, 0.940, 1.41, 1.88, 2.35])
        yp = r.choice([80, 85, 90, 95])
        mt = mp / 94.0 * 330.7 * yp / 100
        st = f'{mp:.2f} g of phenol (Mr 94.0) was treated with excess bromine water. Calculate the theoretical mass of 2,4,6-tribromophenol (Mr 330.7) that could be formed.'
        th = mp / 94.0 * 330.7
        key = f'n(phenol) = {mp:.2f} ÷ 94.0 = {sci(mp / 94, 3)} mol [1]; 1 : 1 ratio [1]; mass = {g3(th)} g [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the theoretical mass', 'What is the theoretical mass').replace('could be formed.', 'could be formed?'), th, [th / 3, mp * 330.7 / 94.0 / 1000 * 1000 * 3, mp / 330.7 * 94.0, th * 2], ' g', key)
        ans = f'{g3(th)} g'
        if D >= 4:
            st += f' The actual mass obtained was {g3(mt)} g. Calculate the percentage yield and write the equation for the reaction.'
            key = key.replace(' [3]', '') + f'; yield = {yp}% [1]; C₆H₅OH + 3Br₂ → C₆H₂Br₃OH + 3HBr [1] [5]'
            ans += f'; {yp}%; C₆H₅OH + 3Br₂ → C₆H₂Br₃OH + 3HBr'
        return Q(st, ans, key, 'numerical')
    if mode == 'h2':
        mp = r.choice([0.470, 0.940, 1.88, 2.82, 3.76])
        v = mp / 94.0 / 2 * 24.0 * 1000
        st = f'Excess sodium was added to {mp:.2f} g of molten phenol (Mr 94.0). Calculate the volume of hydrogen produced, in cm³, at room temperature and pressure. (molar volume 24.0 dm³)'
        key = f'2C₆H₅OH + 2Na → 2C₆H₅ONa + H₂ [1]; n(H₂) = {sci(mp / 94, 3)} ÷ 2 = {sci(mp / 188, 3)} mol [1]; V = {g3(v)} cm³ [1] [3]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the volume of hydrogen produced', 'What volume of hydrogen is produced').replace('pressure.', 'pressure?'), v, [v * 2, v / 2, v / 1000, mp / 94 * 22.4 * 1000], ' cm³', key)
        return Q(st, f'{g3(v)} cm³', key, 'numerical')
    c = r.choice([0.010, 0.050, 0.10, 0.20])
    Ka = 1.3e-10
    h = math.sqrt(Ka * c)
    st = f'Ka for phenol is 1.3 × 10⁻¹⁰ mol dm⁻³. Calculate the pH of a {fx(c, 3)} mol dm⁻³ aqueous solution of phenol.'
    key = f'[H⁺] = √(Ka × c) = √(1.3 × 10⁻¹⁰ × {fx(c, 3)}) [1]; = {sci(h, 3)} mol dm⁻³ [1]; pH = {fx(-math.log10(h), 2)} [1] [3]'
    ans = f'pH = {fx(-math.log10(h), 2)}'
    if D >= 5:
        st += ' State one assumption you have made.'
        key = key.replace(' [3]', '') + '; [H⁺] = [C₆H₅O⁻] / dissociation negligible so [C₆H₅OH] ≈ initial / ignore H⁺ from water [1] [4]'
        ans += '; assume the dissociation of phenol is small, so [C₆H₅OH] at equilibrium ≈ initial concentration'
    return Q(st, ans, key, 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def phenol_rxn(r, D):
    rx = [('aqueous sodium hydroxide', 'C₆H₅OH + NaOH → C₆H₅ONa + H₂O', 'phenol dissolves to give a colourless solution', 'sodium phenoxide'),
          ('sodium metal', '2C₆H₅OH + 2Na → 2C₆H₅ONa + H₂', 'effervescence; sodium dissolves', 'sodium phenoxide and hydrogen'),
          ('bromine water', 'C₆H₅OH + 3Br₂ → C₆H₂Br₃OH + 3HBr', 'orange bromine water decolourised; white precipitate', '2,4,6-tribromophenol'),
          ('dilute nitric acid at room temperature', 'C₆H₅OH + HNO₃ → HOC₆H₄NO₂ + H₂O', 'a mixture of yellow 2- and 4-nitrophenol forms', '2-nitrophenol and 4-nitrophenol'),
          ('aqueous sodium carbonate', 'no reaction', 'no effervescence', 'no reaction (phenol is too weak an acid)')]
    a = r.choice(rx)
    if D <= 2:
        return MQ(r, f'What is formed when phenol reacts with {a[0]}?', cap(a[3]), [cap(x[3]) for x in rx if x != a][:3], f'{a[1]}; {a[2]}.')
    return Q(f'Describe what is observed when phenol is added to {a[0]}. Name the organic product and write an equation.', f'{cap(a[2])}; {a[3]}; {a[1]}',
             'observation [1]; product [1]; equation [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def phenol_case(r, D):
    st = f'{who(r)} is given three colourless liquids labelled A, B and C. They are ethanol, phenol (dissolved in water) and ethanoic acid, but the labels have been lost. pKa values: ethanol about 16, phenol 9.9, ethanoic acid 4.8.'
    parts = [P_('Place the three compounds in order of increasing acidity and explain the position of phenol.', 'Ethanol < phenol < ethanoic acid; phenoxide ion is stabilised by delocalisation of the negative charge into the ring, but less than the carboxylate ion, where the charge is delocalised over two electronegative O atoms.', 'order [1]; phenoxide delocalisation [1]; comparison with carboxylate [1] [3]'),
             P_('Describe a test using sodium carbonate solution that identifies one of the compounds.', 'Ethanoic acid gives effervescence (CO₂, turns limewater milky); phenol and ethanol do not react.', 'reagent and result [1]; others no reaction [1] [2]'),
             P_('Describe a test that distinguishes phenol from ethanol, giving the equation.', 'Bromine water: phenol decolourises it with a white precipitate (C₆H₅OH + 3Br₂ → C₆H₂Br₃OH + 3HBr); ethanol no change.', 'test and observations [1]; equation [1] [2]'),
             P_('Explain why phenol reacts with sodium hydroxide but ethanol does not.', 'Phenol is acidic enough (pKa 9.9) to be deprotonated by OH⁻; ethanol is a weaker acid than water, so the equilibrium lies to the left.', '[2]'),
             P_('Explain why phenol undergoes substitution with bromine more readily than benzene.', 'Lone pair on O delocalised into the ring increases electron density, polarising Br₂ without a catalyst.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Compare the acidity of phenol with that of water, ethanol and ethanoic acid, and describe the reactions of phenol with sodium, sodium hydroxide and bromine water.', 'Order ethanol < water < phenol < ethanoic acid; phenoxide stabilised by delocalisation; alkoxide destabilised by +I alkyl; carboxylate charge over two O; Na gives H₂ and sodium phenoxide; NaOH gives sodium phenoxide (no reaction with carbonate); bromine water gives white 2,4,6-tribromophenol – activated ring; equations.',
           'acidity order [1]; explanation [2]; sodium [1]; NaOH and carbonate [1]; bromine water with explanation [2] [7]')])
t7c = t

# ---------------------------------------------------------------------
SUBST = {'OH': ('–OH', '2,4', True, 'phenol'), 'NH2': ('–NH₂', '2,4', True, 'phenylamine'), 'CH3': ('–CH₃', '2,4', True, 'methylbenzene'),
         'Cl': ('–Cl', '2,4', False, 'chlorobenzene'), 'NO2': ('–NO₂', '3', False, 'nitrobenzene'), 'COOH': ('–COOH', '3', False, 'benzoic acid'),
         'CHO': ('–CHO', '3', False, 'benzaldehyde'), 'COCH3': ('–COCH₃', '3', False, 'phenylethanone')}
PROD = {('CH3', 'nitration'): ('2-nitromethylbenzene and 4-nitromethylbenzene', 'concentrated HNO₃ and H₂SO₄, about 30 °C'),
        ('NO2', 'nitration'): ('1,3-dinitrobenzene', 'concentrated HNO₃ and H₂SO₄, heat above 55 °C'),
        ('NO2', 'bromination'): ('1-bromo-3-nitrobenzene', 'Br₂ with FeBr₃ catalyst, heat'),
        ('CH3', 'bromination'): ('2-bromomethylbenzene and 4-bromomethylbenzene', 'Br₂ with FeBr₃ catalyst, room temperature, no UV light'),
        ('Cl', 'nitration'): ('1-chloro-2-nitrobenzene and 1-chloro-4-nitrobenzene', 'concentrated HNO₃ and H₂SO₄'),
        ('COOH', 'nitration'): ('3-nitrobenzoic acid', 'concentrated HNO₃ and H₂SO₄, heat'),
        ('COCH3', 'bromination'): ('1-(3-bromophenyl)ethanone', 'Br₂ with FeBr₃ catalyst'),
        ('OH', 'bromination'): ('2,4,6-tribromophenol', 'bromine water, room temperature, no catalyst'),
        ('OH', 'nitration'): ('2-nitrophenol and 4-nitrophenol', 'dilute HNO₃, room temperature'),
        ('CHO', 'nitration'): ('3-nitrobenzaldehyde', 'concentrated HNO₃ and H₂SO₄'),
        ('Cl', 'bromination'): ('1-bromo-2-chlorobenzene and 1-bromo-4-chlorobenzene', 'Br₂ with FeBr₃ catalyst'),
        ('NH2', 'bromination'): ('2,4,6-tribromophenylamine', 'bromine water, room temperature, no catalyst')}

t = T('Directing effects of substituents on the benzene ring', 'directing effects of substituents')
facts(t, [('2,4-directing group', 'a substituent that directs incoming electrophiles to the 2- and 4- positions, e.g. –OH, –NH₂, –CH₃, –Cl'),
          ('3-directing group', 'a substituent that directs incoming electrophiles to the 3- position, e.g. –NO₂, –COOH, –CHO, –COR'),
          ('activating group', 'a substituent that donates electron density to the ring, making electrophilic substitution faster than for benzene'),
          ('deactivating group', 'a substituent that withdraws electron density from the ring, making electrophilic substitution slower than for benzene'),
          ('disubstituted arene', 'a benzene ring carrying two substituents, numbered to give the lowest locants')])
mcqs(t, [('Which group directs an incoming electrophile to the 3- position?', '–NO₂', 'Electron-withdrawing groups are 3-directing.', ['–OH', '–CH₃', '–NH₂']),
         ('Which group activates the benzene ring towards electrophilic substitution?', '–OH', 'Lone pair donated into the ring.', ['–NO₂', '–COOH', '–CHO']),
         ('What is the main product of nitrating nitrobenzene?', '1,3-dinitrobenzene', '–NO₂ is 3-directing.', ['1,2-dinitrobenzene', '1,4-dinitrobenzene', '1,3,5-trinitrobenzene']),
         ('What are the main products of the bromination of methylbenzene with FeBr₃?', '2-bromo- and 4-bromomethylbenzene', '–CH₃ is 2,4-directing.', ['3-bromomethylbenzene only', '(bromomethyl)benzene', '2,4,6-tribromomethylbenzene'])])
mcqs(t, [('To make 1-bromo-3-nitrobenzene from benzene, the order of reactions should be', 'nitration first, then bromination', '–NO₂ directs Br to the 3- position.', ['bromination first, then nitration', 'both at the same time', 'either order gives the same product']),
         ('Why is chlorobenzene 2,4-directing but deactivating?', 'Cl donates a lone pair into the ring (2,4-directing) but withdraws electrons inductively more strongly (deactivating)', 'Two opposing effects.', ['Cl is a strong electron donor', 'Cl has no lone pairs', 'Cl is a 3-directing group'])], D=(2, 3), C='C2')
shorts(t, [('Name two groups that are 2,4-directing and two that are 3-directing.', '2,4: any two of –OH, –NH₂, –CH₃ (alkyl), –Cl (halogen); 3: any two of –NO₂, –COOH, –CHO, –COR, –CN.', 'two 2,4 [1]; two 3 [1] [2]')])
explain(t, [('Explain why methylbenzene undergoes nitration faster than benzene.', 'The methyl group donates electron density into the ring (positive inductive effect), increasing the π electron density so the ring attracts the electrophile NO₂⁺ more strongly and the intermediate is stabilised.', 'electron-donating CH₃ [1]; higher ring electron density / intermediate stabilised [1] [2]'),
            ('Explain why the order of steps matters when making a disubstituted benzene.', 'The first substituent controls where the second goes: a 2,4-directing group gives 2- and 4- products, a 3-directing group gives 3- products, so the steps must be ordered to give the required isomer.', '[2]'),
            ('Explain why nitrobenzene reacts with electrophiles more slowly than benzene.', 'The –NO₂ group withdraws electron density from the ring, lowering its π electron density, so electrophiles are attracted less; harsher conditions are needed.', '[2]')])
myths(t, [('All substituents direct incoming groups to the 4- position.', '–NO₂, –COOH, –CHO and –COR are 3-directing; only electron-donating groups (and halogens) are 2,4-directing.'),
          ('2,4-directing groups always activate the ring.', 'Halogens are 2,4-directing but deactivating.'),
          ('The order of substitution steps does not affect the product.', 'The first group directs the second, so changing the order changes the isomer formed.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def direct_q(r, D):
    (g, rx), (prod, cond) = r.choice(list(PROD.items()))
    sym, pos, act, name = SUBST[g]
    if D <= 2:
        opts = ['the 2- and 4- positions', 'the 3- position', 'the 2-, 4- and 6- positions', 'the 3- and 5- positions']
        right = 'the 2-, 4- and 6- positions' if prod.startswith('2,4,6') else ('the 2- and 4- positions' if pos == '2,4' else 'the 3- position')
        return MQ(r, f'In the {rx} of {name} ({cond}), at which position(s) on the ring does substitution mainly occur?', right, [o for o in opts if o != right], f'{sym} is {pos}-directing: {prod}.')
    st = f'Predict the main organic product(s) of the {rx} of {name} ({cond}). Explain your answer in terms of the directing effect of the substituent.'
    ans = f'{cap(prod)}; {sym} is {pos}-directing' + (' and activating (electron-donating)' if act else ' and deactivating (electron-withdrawing)' if pos == '3' else ' but deactivating')
    key = 'product(s) [1]; directing effect of the substituent [1]'
    tot = 2
    if D >= 4:
        st += f' State whether {name} reacts faster or slower than benzene, with a reason.'
        ans += f'; {name} reacts {"faster" if act else "slower"} than benzene because the substituent {"donates electron density to" if act else "withdraws electron density from"} the ring'
        key += '; rate comparison with reason [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def direct_case(r, D):
    tgt = r.choice([('1-bromo-3-nitrobenzene', 'nitration (conc HNO₃/H₂SO₄, < 55 °C) then bromination (Br₂, FeBr₃)', '–NO₂ is 3-directing, so it must be introduced first'),
                    ('1-bromo-4-nitrobenzene', 'bromination (Br₂, FeBr₃) then nitration (conc HNO₃/H₂SO₄); separate the 4-isomer from the 2-isomer', '–Br is 2,4-directing, so it must be introduced first'),
                    ('3-nitrobenzoic acid', 'Friedel–Crafts methylation, oxidation with hot alkaline KMnO₄ then acid, then nitration', '–COOH is 3-directing, so oxidise before nitrating'),
                    ('4-nitrobenzoic acid', 'Friedel–Crafts methylation, nitration (separate 4-isomer), then oxidation of –CH₃ with hot alkaline KMnO₄ then acid', '–CH₃ is 2,4-directing, so nitrate before oxidising')])
    st = f'{who(r)} wants to make {tgt[0]} starting from benzene in two or three steps.'
    parts = [P_('Suggest the order of steps, with reagents and conditions.', tgt[1], 'correct order [1]; reagents and conditions for each step [2] [3]'),
             P_('Explain why the steps must be carried out in this order.', tgt[2] + '.', '[2]'),
             P_('Explain, in terms of electron density, why –NO₂ is a deactivating group.', 'Electron-withdrawing –NO₂ reduces the π electron density of the ring, so electrophiles are attracted less strongly and the reaction is slower.', '[2]'),
             P_('Suggest how the required isomer could be separated from any other isomers formed.', 'Fractional crystallisation / recrystallisation (or chromatography), since isomers have different solubilities and melting points; check purity by melting point.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain the directing and activating effects of substituents on the benzene ring and show how they are used to plan the synthesis of disubstituted arenes.', 'Electron-donating –OH, –NH₂, –CH₃ activate and direct 2,4; halogens 2,4 but deactivate; electron-withdrawing –NO₂, –COOH, –CHO deactivate and direct 3; reason: electron density in ring and stability of intermediates; examples: phenol + bromine water; nitration of methylbenzene vs nitrobenzene; planning order of steps for 1-bromo-3-nitrobenzene vs 1-bromo-4-nitrobenzene.',
           '2,4-directing groups [1]; 3-directing groups [1]; activation/deactivation explained [2]; examples [1]; synthesis planning [2] [7]')])
t7d = t

CHAPTERS[7] = [t7a, t7b, t7c, t7d]


# ===================================================================== 8 Carboxylic acids and derivatives
PKA = [('ethanoic acid', 'CH₃COOH', 4.76), ('chloroethanoic acid', 'CH₂ClCOOH', 2.86), ('dichloroethanoic acid', 'CHCl₂COOH', 1.29), ('trichloroethanoic acid', 'CCl₃COOH', 0.65),
       ('methanoic acid', 'HCOOH', 3.75), ('propanoic acid', 'CH₃CH₂COOH', 4.87), ('benzoic acid', 'C₆H₅COOH', 4.20), ('2-chloropropanoic acid', 'CH₃CHClCOOH', 2.83),
       ('3-chloropropanoic acid', 'CH₂ClCH₂COOH', 3.98), ('fluoroethanoic acid', 'CH₂FCOOH', 2.59), ('bromoethanoic acid', 'CH₂BrCOOH', 2.90)]

t = T('Acidity of carboxylic acids and chlorine-substituted acids', 'acidity of carboxylic acids')
facts(t, [('carboxylate ion', 'RCOO⁻, the anion formed when a carboxylic acid loses H⁺; its charge is delocalised over two oxygen atoms'),
          ('inductive effect', 'the donation or withdrawal of electron density along σ bonds by an atom or group, e.g. electron withdrawal by chlorine'),
          ('pKa', '−log₁₀ Ka; the smaller the pKa, the stronger the acid'),
          ('electron-withdrawing group', 'a group, such as –Cl, that pulls electron density away from the –COO⁻ group and stabilises the anion'),
          ('electron-donating group', 'a group, such as an alkyl group, that pushes electron density towards the –COO⁻ group and destabilises the anion')])
mcqs(t, [('Which acid is the strongest?', 'Trichloroethanoic acid', 'Three electron-withdrawing Cl atoms; pKa 0.65.', ['Ethanoic acid', 'Chloroethanoic acid', 'Propanoic acid']),
         ('Why is ethanoic acid a stronger acid than ethanol?', 'The ethanoate ion is stabilised by delocalisation of the negative charge over two oxygen atoms', 'Carboxylate resonance.', ['Ethanoic acid has more hydrogen atoms', 'Ethanol is a base', 'Ethanoic acid forms hydrogen bonds']),
         ('Which is a weaker acid than ethanoic acid?', 'Propanoic acid', 'Ethyl group more electron-donating than methyl.', ['Methanoic acid', 'Chloroethanoic acid', 'Benzoic acid']),
         ('Which reagent is oxidised by acidified potassium manganate(VII) to carbon dioxide?', 'Ethanedioic acid', 'HOOC–COOH → 2CO₂.', ['Ethanoic acid', 'Propanoic acid', 'Benzoic acid'])])
mcqs(t, [('2-chloropropanoic acid (pKa 2.83) is stronger than 3-chloropropanoic acid (pKa 3.98) because', 'the Cl atom is closer to the –COOH group, so its electron-withdrawing effect on the anion is greater', 'Inductive effects weaken with distance.', ['2-chloropropanoic acid has more Cl atoms', 'Cl is electron-donating', '3-chloropropanoic acid is a diol']),
         ('Why can methanoic acid be oxidised but ethanoic acid cannot (under mild conditions)?', 'Methanoic acid contains an aldehyde H–C=O group', 'HCOOH → CO₂ + H₂O with Tollens\' or Fehling\'s.', ['Methanoic acid is a weaker acid', 'Ethanoic acid has no C=O group', 'Methanoic acid is a gas'])], D=(2, 3), C='C2')
shorts(t, [('State and explain the order of acidity of ethanol, phenol and ethanoic acid.', 'Ethanol < phenol < ethanoic acid: ethoxide destabilised by alkyl group; phenoxide charge partly delocalised into ring; ethanoate charge delocalised over two O atoms.', 'order [1]; explanation [1] [2]'),
           ('Write an equation for the oxidation of methanoic acid by acidified potassium manganate(VII), using [O].', 'HCOOH + [O] → CO₂ + H₂O', '[1]')])
explain(t, [('Explain why chloroethanoic acid is a stronger acid than ethanoic acid.', 'Chlorine is electronegative and withdraws electron density from the –COO⁻ group (negative inductive effect), spreading the negative charge and stabilising the anion, so the acid dissociates more.', 'electron withdrawal by Cl [1]; anion stabilised [1]; more dissociation [1] [3]'),
            ('Explain the trend in acid strength from ethanoic acid to trichloroethanoic acid.', 'Each extra Cl atom withdraws more electron density, increasingly stabilising the carboxylate ion; pKa falls from 4.76 to 0.65, so acid strength increases.', 'more Cl, more withdrawal [1]; anion more stable [1]; data quoted [1] [3]'),
            ('Explain why propanoic acid is slightly weaker than ethanoic acid.', 'The ethyl group is slightly more electron-donating than methyl, increasing the negative charge density on the carboxylate ion and destabilising it.', '[2]')])
myths(t, [('Chlorine atoms make chloroethanoic acid weaker because they donate electrons.', 'Chlorine withdraws electron density, stabilising the anion and making the acid stronger.'),
          ('The position of the chlorine atom in a chloropropanoic acid has no effect on acid strength.', 'The closer the Cl is to the –COOH group, the stronger its inductive effect and the stronger the acid.'),
          ('A lower pKa means a weaker acid.', 'A lower pKa means a larger Ka, so a stronger acid.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def acid_ph(r, D):
    nm, f, pk = r.choice([p for p in PKA if p[2] >= 2.5])
    c = r.choice([0.050, 0.10, 0.20, 0.50, 1.00])
    Ka = 10 ** -pk
    h = math.sqrt(Ka * c)
    st = f'The pKa of {nm}, {f}, is {pk}. Calculate the pH of a {fx(c, 3)} mol dm⁻³ solution of the acid.'
    key = f'Ka = 10⁻{pk} = {sci(Ka, 3)} [1]; [H⁺] = √(Ka × c) = {sci(h, 3)} [1]; pH = {fx(-math.log10(h), 2)} [1] [3]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the pH', 'What is the pH').replace('of the acid.', 'of the acid?'), -math.log10(h), [-math.log10(c), -math.log10(Ka * c), pk, -math.log10(h) * 2], '', key, f=lambda v: fx(v, 2))
    ans = f'pH = {fx(-math.log10(h), 2)}'
    if D >= 4:
        nm2, f2, pk2 = r.choice([p for p in PKA if p[0] != nm and p[2] >= 2.5])
        h2 = math.sqrt(10 ** -pk2 * c)
        st += f' Calculate the pH of a solution of {nm2} (pKa {pk2}) of the same concentration and explain the difference in terms of structure.'
        ans += f'; {nm2}: pH = {fx(-math.log10(h2), 2)}; ' + ('the second acid is stronger' if pk2 < pk else 'the second acid is weaker') + ' because of the inductive effects of its substituents on the stability of the carboxylate ion'
        key = key.replace(' [3]', '') + f'; second pH = {fx(-math.log10(h2), 2)} [1]; explanation using inductive effect / anion stability [1] [5]'
    return Q(st, ans, key, 'numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def acid_rank(r, D):
    ch = r.sample(PKA, 3)
    srt = sorted(ch, key=lambda x: -x[2])
    order = ' < '.join(x[0] for x in srt)
    if D <= 2:
        a = min(ch, key=lambda x: x[2])
        return MQ(r, 'Which is the strongest acid: ' + ', '.join(x[0] for x in ch) + '?', cap(a[0]), [cap(x[0]) for x in ch if x != a] + ['They are all equally strong'], f'{cap(a[0])} has the lowest pKa ({a[2]}).')
    st = 'pKa values: ' + '; '.join(f'{x[0]} {x[2]}' for x in ch) + '. Arrange the acids in order of increasing strength and explain the position of the strongest acid.'
    s_ = srt[-1]
    why = ('electron-withdrawing halogen atoms stabilise the carboxylate ion' if any(h in s_[1] for h in ('Cl', 'F', 'Br')) else
           'it has no electron-donating alkyl group, so its anion is more stable' if s_[0] == 'methanoic acid' else 'its substituent destabilises the anion least / stabilises it most')
    return Q(st, f'{order}; strongest: {s_[0]}, because {why}.', 'order [1]; explanation for strongest [1]; reference to stability of anion [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def acid_case(r, D):
    c = r.choice([0.10, 0.20])
    st = f'{who(r)} measures the pH of {fx(c, 2)} mol dm⁻³ solutions of ethanoic acid (pKa 4.76) and chloroethanoic acid (pKa 2.86) in {lab(r)}.'
    p1 = -math.log10(math.sqrt(10 ** -4.76 * c))
    p2 = -math.log10(math.sqrt(10 ** -2.86 * c))
    parts = [P_('Calculate the expected pH of each solution.', f'ethanoic {fx(p1, 2)}; chloroethanoic {fx(p2, 2)}', f'[H⁺] = √(Ka c) [1]; ethanoic pH {fx(p1, 2)} [1]; chloroethanoic pH {fx(p2, 2)} [1] [3]'),
             P_('Explain why chloroethanoic acid is the stronger acid.', 'Cl withdraws electron density (negative inductive effect), delocalising the negative charge and stabilising the chloroethanoate ion.', '[2]'),
             P_('Suggest why the measured pH of the chloroethanoic acid solution is slightly higher than calculated.', 'The approximation [HA] ≈ initial concentration is less valid for a stronger weak acid, as a significant fraction dissociates.', '[1]'),
             P_('Predict, with a reason, the pKa of dichloroethanoic acid relative to the two acids.', 'Lower than 2.86 (about 1.3): two Cl atoms withdraw more electron density.', '[2]'),
             P_('Describe a chemical test, other than pH, to show that both are carboxylic acids.', 'Add sodium carbonate: effervescence of CO₂ (turns limewater milky).', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain the relative acidities of ethanol, phenol, ethanoic acid and the chlorine-substituted ethanoic acids.', 'Acid strength depends on stability of conjugate base; ethoxide destabilised (+I alkyl), phenoxide partly delocalised into ring, carboxylate delocalised over two O; Cl substituents withdraw electrons (−I), stabilising anion; more Cl → stronger (pKa 4.76, 2.86, 1.29, 0.65); position effect (2- vs 3-chloropropanoic); data use.',
           'anion stability principle [1]; alcohol/phenol/acid comparison [2]; inductive effect of Cl [2]; number/position effect with data [2] [7]')])
t8a = t

# ---------------------------------------------------------------------
ACYL = {'ethanoyl': ('CH3CO', 'ethanoic acid', 'ethanoate', 'ethanamide', 'CH₃CO'), 'propanoyl': ('CH3CH2CO', 'propanoic acid', 'propanoate', 'propanamide', 'CH₃CH₂CO'),
        'butanoyl': ('CH3CH2CH2CO', 'butanoic acid', 'butanoate', 'butanamide', 'CH₃CH₂CH₂CO'), 'benzoyl': ('C6H5CO', 'benzoic acid', 'benzoate', 'benzamide', 'C₆H₅CO')}
NUC = {'water': ('H2O', 'OH', None, 'acid'), 'methanol': ('CH3OH', 'OCH3', 'methyl', 'ester'), 'ethanol': ('CH3CH2OH', 'OCH2CH3', 'ethyl', 'ester'),
       'propan-1-ol': ('CH3CH2CH2OH', 'OCH2CH2CH3', 'propyl', 'ester'), 'phenol': ('C6H5OH', 'OC6H5', 'phenyl', 'ester'), 'ammonia': ('NH3', 'NH2', None, 'amide'),
       'methylamine': ('CH3NH2', 'NHCH3', 'methyl', 'subamide'), 'ethylamine': ('CH3CH2NH2', 'NHCH2CH3', 'ethyl', 'subamide'), 'phenylamine': ('C6H5NH2', 'NHC6H5', 'phenyl', 'subamide')}


def acyl_prod(acyl, nuc):
    a = ACYL[acyl]
    n_ = NUC[nuc]
    f = a[0] + n_[1]
    name = {'acid': a[1], 'ester': f'{n_[2]} {a[2]}', 'amide': a[3], 'subamide': f'N-{n_[2]}{a[3]}'}[n_[3]]
    return name, f


def acyl_eq(acyl, nuc):
    a = ACYL[acyl]
    n_ = NUC[nuc]
    nm, f = acyl_prod(acyl, nuc)
    if n_[3] in ('amide', 'subamide'):
        return f'{F(a[0] + "Cl")} + 2{F(n_[0])} → {F(f)} + {F(n_[0].replace("H2", "H3", 1) if n_[0] != "NH3" else "NH4")}⁺Cl⁻'.replace('NH₄⁺Cl⁻', 'NH₄Cl')
    return f'{F(a[0] + "Cl")} + {F(n_[0])} → {F(f)} + HCl'


t = T('Acyl chlorides: preparation and reactions with water, alcohols, phenols and amines', 'acyl chlorides: preparation')
facts(t, [('acyl chloride', 'a compound containing the –COCl functional group, e.g. ethanoyl chloride CH₃COCl'),
          ('nucleophilic addition–elimination', 'the mechanism by which acyl chlorides react with nucleophiles: addition to C=O followed by elimination of HCl'),
          ('ester', 'a compound containing the –COO– group, formed from an acyl chloride and an alcohol or phenol'),
          ('N-substituted amide', 'an amide in which a hydrogen on nitrogen is replaced by an alkyl or aryl group, e.g. N-methylethanamide'),
          ('thionyl chloride', 'SOCl₂, a reagent that converts carboxylic acids into acyl chlorides, giving SO₂ and HCl as gaseous by-products')])
mcqs(t, [('Which reagent converts ethanoic acid into ethanoyl chloride?', 'SOCl₂', 'Also PCl₅ or PCl₃ with heat.', ['HCl(aq)', 'Cl₂ in UV light', 'NaCl']),
         ('What is formed when ethanoyl chloride reacts with water?', 'Ethanoic acid and hydrogen chloride', 'Vigorous hydrolysis; steamy fumes.', ['Ethanol and HCl', 'Ethanal and HCl', 'Ethanamide and HCl']),
         ('What is formed when ethanoyl chloride reacts with phenol?', 'Phenyl ethanoate', 'Esters of phenol are made from acyl chlorides.', ['Ethyl benzoate', 'Phenylethanone', 'Benzoic acid']),
         ('What is observed when ethanoyl chloride is added to water?', 'A vigorous reaction with steamy (misty) fumes of HCl', 'Rapid hydrolysis.', ['A white precipitate', 'No reaction at room temperature', 'A brown gas'])])
mcqs(t, [('Why are esters of phenol made using acyl chlorides rather than carboxylic acids?', 'Phenol is a poor nucleophile and reacts very slowly with carboxylic acids', 'Acyl chlorides are much more reactive.', ['Phenol is a strong acid', 'Carboxylic acids are too reactive', 'Phenol reacts with H₂SO₄']),
         ('What is the order of ease of hydrolysis, easiest first?', 'Acyl chloride > alkyl chloride > aryl chloride', 'Acyl C very δ+; aryl C–Cl strengthened by delocalisation.', ['Aryl chloride > alkyl chloride > acyl chloride', 'Alkyl chloride > acyl chloride > aryl chloride', 'All hydrolyse at the same rate'])], D=(2, 3), C='C2')
shorts(t, [('Write an equation for the preparation of propanoyl chloride from propanoic acid using SOCl₂.', 'CH₃CH₂COOH + SOCl₂ → CH₃CH₂COCl + SO₂ + HCl', 'products [1]; balanced [1] [2]'),
           ('Write an equation for the preparation of ethanoyl chloride using PCl₅.', 'CH₃COOH + PCl₅ → CH₃COCl + POCl₃ + HCl', '[2]')])
explain(t, [('Explain why acyl chlorides are hydrolysed much more readily than chloroalkanes.', 'The carbonyl carbon is bonded to two electronegative atoms (O and Cl), so it is strongly δ+ and attacked readily by water; it is also planar, allowing easy approach by the nucleophile.', 'two electronegative atoms / large δ+ [1]; easy nucleophilic attack [1] [2]'),
            ('Explain why chlorobenzene is very difficult to hydrolyse.', 'A lone pair on Cl overlaps with the π system of the ring, giving the C–Cl bond partial double-bond character, so it is stronger; the π electrons also repel nucleophiles.', 'delocalisation of Cl lone pair [1]; stronger C–Cl bond / repulsion of nucleophile [1] [2]'),
            ('Explain why SOCl₂ is a convenient reagent for making acyl chlorides.', 'The by-products SO₂ and HCl are gases, which escape, leaving the acyl chloride easy to purify.', '[1]')])
myths(t, [('Acyl chlorides react with alcohols only when heated with a concentrated sulfuric acid catalyst.', 'Acyl chlorides react rapidly with alcohols at room temperature with no catalyst.'),
          ('Chlorobenzene is hydrolysed by water as easily as ethanoyl chloride.', 'Chlorobenzene is very hard to hydrolyse because its C–Cl bond is strengthened by delocalisation.'),
          ('The reaction of ethanoyl chloride with ammonia gives ethylamine.', 'It gives the amide, ethanamide (and ammonium chloride).')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def acyl_q(r, D):
    acyl = r.choice(list(ACYL))
    nuc = r.choice(list(NUC))
    nm, f = acyl_prod(acyl, nuc)
    if D <= 2:
        wr = [acyl_prod(acyl, n)[0] for n in NUC if n != nuc]
        wr = [w for w in wr if w != nm]
        r.shuffle(wr)
        return MQ(r, f'What is the organic product when {acyl} chloride reacts with {nuc}?', nm, wr[:3], f'{acyl_eq(acyl, nuc)}.')
    st = f'Name and give the structural formula of the organic product formed when {acyl} chloride reacts with {nuc}. Write an equation for the reaction.'
    ans = f'{nm}, {F(f)}; {acyl_eq(acyl, nuc)}'
    key = 'name [1]; structural formula [1]; equation [1]'
    tot = 3
    if D >= 4:
        st += ' State the conditions and the type of reaction.'
        ans += '; room temperature; nucleophilic addition–elimination' + (' (concentrated NH₃ / amine in excess)' if NUC[nuc][3] in ('amide', 'subamide') else '')
        key += '; conditions [1]; addition–elimination [1]'
        tot += 2
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def acyl_yield(r, D):
    acyl = r.choice(list(ACYL))
    nuc = r.choice(['ethanol', 'methanol', 'phenol', 'phenylamine', 'methylamine', 'propan-1-ol'])
    nm, f = acyl_prod(acyl, nuc)
    Ma = Mr(ACYL[acyl][0] + 'Cl')
    Mp = Mr(f)
    ma = r.choice([2.00, 3.50, 5.00, 7.85, 10.0])
    yp = r.choice([58, 64, 70, 76, 82, 88])
    th = ma / Ma * Mp
    act = th * yp / 100
    st = f'{ma:.2f} g of {acyl} chloride (Mr {Ma:.1f}) was reacted with excess {nuc}, giving {g3(act)} g of {nm} (Mr {Mp:.1f}). Calculate the percentage yield.'
    key = f'n(acyl chloride) = {sci(ma / Ma, 3)} mol [1]; theoretical mass = {g3(th)} g [1]; yield = {yp}% [1] [3]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the percentage yield.', 'What is the percentage yield?'), yp, [act / ma * 100, yp * Ma / Mp, 100 - yp, ma / act * 100], '%', key, f=lambda v: str(int(round(v))))
    ans = f'{yp}%'
    if D >= 4:
        st += ' Explain why an acyl chloride is used rather than the carboxylic acid.'
        ans += '; acyl chlorides react rapidly and irreversibly at room temperature' + (' (phenol reacts too slowly with carboxylic acids)' if nuc == 'phenol' else '; carboxylic acid reactions are slow and reversible')
        key = key.replace(' [3]', '') + '; reason [1] [4]'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def acyl_case(r, D):
    acyl = r.choice(list(ACYL))
    a = ACYL[acyl]
    st = f'{who(r)} converts {a[1]} into {acyl} chloride and then uses it to make three derivatives.'
    pe, pfe = acyl_prod(acyl, 'ethanol')
    pa, pfa = acyl_prod(acyl, 'ammonia')
    pp, pfp = acyl_prod(acyl, 'phenol')
    parts = [P_(f'Give a reagent for converting {a[1]} into {acyl} chloride and write the equation.', f'SOCl₂: {F(a[0] + "OH")} + SOCl₂ → {F(a[0] + "Cl")} + SO₂ + HCl (or PCl₅ / PCl₃ with heat)', 'reagent [1]; equation [1] [2]'),
             P_(f'Name the products formed with ethanol, with concentrated ammonia and with phenol.', f'{pe} ({F(pfe)}); {pa} ({F(pfa)}); {pp} ({F(pfp)})', 'each product [1] [3]'),
             P_('Describe what is seen when the acyl chloride is added to water and write an equation.', f'Vigorous reaction, steamy white fumes of HCl; {acyl_eq(acyl, "water")}', 'observation [1]; equation [1] [2]'),
             P_('Explain why acyl chlorides are more reactive towards nucleophiles than carboxylic acids.', 'Cl is more electron-withdrawing and a better leaving group; the carbonyl carbon is more δ+, and Cl⁻ is lost easily in the elimination step.', '[2]'),
             P_('Explain why the reaction with phenol is used to make the phenyl ester.', 'Phenol reacts only very slowly with carboxylic acids, because its lone pair is delocalised into the ring (poor nucleophile).', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the preparation of acyl chlorides and their reactions with water, alcohols, phenols and amines, and explain their high reactivity compared with other chlorine compounds.', 'Preparation with SOCl₂, PCl₅ or PCl₃ (equations); reactions at room temperature: water → acid + HCl; alcohol → ester; phenol → phenyl ester; NH₃ → amide; primary amine → N-substituted amide; equations; reactivity: C bonded to O and Cl, very δ+, planar, Cl⁻ good leaving group; comparison acyl > alkyl > aryl chloride for hydrolysis.',
           'preparation [2]; four reactions with products [3]; reactivity explanation [1]; comparison with alkyl/aryl chlorides [1] [7]')])
t8b = t

# ---------------------------------------------------------------------
t = T('Addition–elimination mechanism of acyl chlorides', 'addition–elimination mechanism')
facts(t, [('nucleophile', 'a species with a lone pair of electrons that it donates to an electron-deficient atom to form a new bond'),
          ('tetrahedral intermediate', 'the species formed when a nucleophile adds to the carbonyl carbon of an acyl chloride, with four groups around that carbon'),
          ('leaving group', 'an atom or group, such as Cl⁻, that departs with the bonding pair of electrons during the elimination step'),
          ('curly arrow', 'a symbol showing the movement of a pair of electrons from a lone pair or bond to an atom or new bond'),
          ('carbonyl carbon', 'the δ+ carbon atom of a C=O group, attacked by nucleophiles')])
mcqs(t, [('In the reaction of ethanoyl chloride with water, which atom does the nucleophile attack?', 'The carbonyl carbon', 'It is δ+.', ['The oxygen of C=O', 'The chlorine', 'The methyl carbon']),
         ('What is eliminated in the second stage of the reaction of an acyl chloride with an alcohol?', 'HCl (Cl⁻ then H⁺)', 'C=O reforms, Cl⁻ leaves, H⁺ lost.', ['H₂O', 'Cl₂', 'The alcohol']),
         ('What is the first step of the addition–elimination mechanism?', 'The lone pair of the nucleophile attacks the δ+ carbonyl carbon, and the C=O π electrons move onto oxygen', 'Addition.', ['Cl⁻ leaves to form a carbocation', 'H⁺ adds to the carbonyl oxygen', 'A free radical forms'])])
mcqs(t, [('Why is the carbonyl carbon in an acyl chloride strongly δ+?', 'It is bonded to two electronegative atoms, O and Cl', 'Both withdraw electron density.', ['It has a lone pair', 'It is part of a benzene ring', 'It is bonded to hydrogen']),
         ('Why is the reaction of ethanoyl chloride with ethylamine called addition–elimination?', 'The amine adds to C=O to form an intermediate, then HCl is eliminated as C=O reforms', 'Two stages.', ['Ethylamine is added and then removed', 'An alkene forms and is then hydrogenated', 'The reaction is reversible'])], D=(2, 3), C='C2')
shorts(t, [('Explain what is meant by the term nucleophile.', 'A species that donates a lone pair of electrons to an electron-deficient atom, forming a new covalent bond.', '[1]')])
explain(t, [('Describe, in words, the curly arrows in the reaction of ethanoyl chloride with methanol.', 'Arrow from O lone pair of methanol to δ+ carbonyl C; arrow from C=O π bond to O, forming O⁻ in the tetrahedral intermediate; arrow from O⁻ back to reform C=O; arrow from C–Cl bond to Cl, which leaves as Cl⁻; H⁺ lost from the oxygen (taken by Cl⁻ to give HCl).', 'nucleophile attack [1]; C=O to O [1]; C=O reforms and Cl⁻ leaves [1]; H⁺ lost [1] [4]'),
            ('Explain why an acyl chloride reacts with a nucleophile by addition–elimination rather than by SN2.', 'The planar carbonyl carbon allows nucleophilic addition to the C=O bond, forming a tetrahedral intermediate; then the C=O reforms with loss of the good leaving group Cl⁻.', '[2]')])
myths(t, [('In the addition–elimination mechanism, Cl⁻ leaves first to form a carbocation.', 'The nucleophile adds first to the carbonyl carbon; Cl⁻ leaves when the C=O bond reforms.'),
          ('The oxygen of the carbonyl group is attacked by the nucleophile.', 'The δ+ carbonyl carbon is attacked; the electrons of the C=O π bond move onto the oxygen.')])

NUC_MECH = {'water': ('O', 'H₂O'), 'methanol': ('O', 'CH₃OH'), 'ethanol': ('O', 'CH₃CH₂OH'), 'ammonia': ('N', 'NH₃'), 'methylamine': ('N', 'CH₃NH₂'), 'ethylamine': ('N', 'CH₃CH₂NH₂')}


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def mech_ae(r, D):
    acyl = r.choice(list(ACYL))
    nuc = r.choice(list(NUC_MECH))
    at, nf = NUC_MECH[nuc]
    nm, f = acyl_prod(acyl, nuc)
    ac = F(ACYL[acyl][0] + 'Cl')
    if D <= 2:
        return MQ(r, f'In the reaction of {ac} with {nf}, which atom of {nf} forms the new bond to carbon?', f'The {"oxygen" if at == "O" else "nitrogen"} atom (using its lone pair)', ['A hydrogen atom', 'The chlorine atom', 'A carbon atom of the nucleophile'], f'The lone pair on {at} attacks the δ+ carbonyl carbon.')
    st = f'Describe the mechanism of the reaction between {ac} and {nf}, naming the mechanism and showing the movement of electron pairs in words. Name the organic product.'
    ans = (f'Nucleophilic addition–elimination. Lone pair on {at} of {nf} attacks the δ+ carbonyl carbon; C=O π electrons move to O giving a tetrahedral intermediate (O⁻, {at}⁺); '
           f'C=O reforms, Cl⁻ leaves; H⁺ lost from {at} (forms HCl{" / NH₄Cl with excess" if at == "N" else ""}). Product: {nm}.')
    key = 'name of mechanism [1]; nucleophile attacks δ+ C [1]; C=O electrons to O / intermediate [1]; C=O reforms and Cl⁻ leaves [1]; H⁺ lost [1]; product [1] [6]'
    if D <= 3:
        st = st.replace(', naming the mechanism and showing the movement of electron pairs in words', ' in words')
        key = 'nucleophile attacks δ+ C [1]; intermediate [1]; Cl⁻ eliminated / H⁺ lost [1]; product [1] [4]'
    return Q(st, ans, key, 'short')


@t.add('C3', (2, 3, 4), 'short')
def mech_err(r, D):
    errs = [('the curly arrow starts from the chlorine atom and goes to the carbonyl carbon', 'the arrow should start from the lone pair on the nucleophile and go to the δ+ carbonyl carbon'),
            ('the nucleophile attacks the carbonyl oxygen', 'the nucleophile attacks the δ+ carbonyl carbon; the C=O π electrons move onto the oxygen'),
            ('Cl⁻ leaves first, giving an acylium carbocation, which is then attacked', 'addition to C=O occurs first, giving a tetrahedral intermediate; Cl⁻ leaves as C=O reforms'),
            ('the product of ethanoyl chloride and ethanol is ethanoic acid', 'the product is the ester ethyl ethanoate (and HCl)'),
            ('the intermediate has a positive charge on the carbonyl oxygen', 'the carbonyl oxygen carries the negative charge in the intermediate; the nucleophile atom carries the positive charge')]
    e = r.choice(errs)
    p = who(r)
    return Q(f'{p} drew the mechanism for the reaction of an acyl chloride with a nucleophile. In it, {e[0]}. Identify the error and describe the correct step.', cap(e[1]) + '.', 'error identified [1]; correct step [1] [2]', 'explain')


@t.add('C4', (2, 3, 4, 5), 'case')
def ae_case(r, D):
    acyl = r.choice(list(ACYL))
    nuc = r.choice(['ethanol', 'methylamine', 'ammonia', 'methanol'])
    at, nf = NUC_MECH[nuc]
    nm, f = acyl_prod(acyl, nuc)
    ac = F(ACYL[acyl][0] + 'Cl')
    st = f'{who(r)} studies the reaction of {acyl} chloride, {ac}, with {nuc}, {nf}, at room temperature.'
    parts = [P_('Explain why the carbonyl carbon is susceptible to nucleophilic attack.', 'It is bonded to two electronegative atoms (O and Cl), so it carries a large δ+ charge; it is planar and accessible.', '[2]'),
             P_('Describe the mechanism, showing curly arrows in words, and draw-describe the intermediate.', f'Lone pair on {at} attacks C; C=O π electrons move to O; tetrahedral intermediate with O⁻ and {at}⁺; C=O reforms, Cl⁻ leaves; H⁺ lost from {at}.', 'attack [1]; intermediate [1]; elimination of Cl⁻ [1]; loss of H⁺ [1] [4]'),
             P_('Name the organic product and give its structural formula.', f'{nm}, {F(f)}', '[2]'),
             P_(f'Suggest why {"two moles of the amine/ammonia are needed" if at == "N" else "the reaction is carried out in dry conditions"}.', ('The HCl formed reacts with a second mole of the base to form a salt.' if at == 'N' else 'Water would hydrolyse the acyl chloride to the carboxylic acid, lowering the yield of ester.'), '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe and explain the nucleophilic addition–elimination mechanism for the reactions of acyl chlorides with water, alcohols and amines.', 'δ+ carbonyl carbon bonded to O and Cl; nucleophile lone pair (O of water/alcohol, N of amine) attacks; C=O π electrons to O; tetrahedral intermediate; C=O reforms, Cl⁻ leaves; H⁺ lost; products acid/ester/amide + HCl (amine salt); why addition–elimination not substitution; comparison of nucleophiles.',
           'δ+ carbon explained [1]; addition step [2]; elimination step [2]; products for three nucleophiles [2] [7]')])
t8c = t

CHAPTERS[8] = [t8a, t8b, t8c]


# ===================================================================== 9 Organic nitrogen compounds
AMINES = [('ammonia', 'NH₃', 9.25), ('methylamine', 'CH₃NH₂', 10.64), ('ethylamine', 'CH₃CH₂NH₂', 10.73), ('phenylamine', 'C₆H₅NH₂', 4.60),
          ('propylamine', 'CH₃CH₂CH₂NH₂', 10.57), ('diethylamine', '(CH₃CH₂)₂NH', 10.98)]

t = T('Amines: preparation, basicity and relative basic strength of ammonia, ethylamine and phenylamine', 'amines: preparation, basicity')
facts(t, [('amine', 'an organic compound derived from ammonia by replacing one or more hydrogen atoms with alkyl or aryl groups'),
          ('primary amine', 'an amine with one alkyl or aryl group on the nitrogen atom, RNH₂'),
          ('Brønsted base', 'a proton (H⁺) acceptor; amines act as bases using the lone pair on nitrogen'),
          ('alkylammonium salt', 'the ionic compound formed when an amine reacts with an acid, e.g. ethylammonium chloride CH₃CH₂NH₃⁺Cl⁻'),
          ('positive inductive effect', 'the donation of electron density by alkyl groups, which increases the availability of the nitrogen lone pair'),
          ('phenylamine', 'C₆H₅NH₂, an aromatic amine made by reducing nitrobenzene with tin and concentrated hydrochloric acid')])
mcqs(t, [('Which is the order of base strength, weakest first?', 'Phenylamine < ammonia < ethylamine', 'Lone-pair availability.', ['Ethylamine < ammonia < phenylamine', 'Ammonia < phenylamine < ethylamine', 'Phenylamine < ethylamine < ammonia']),
         ('Which reagents convert nitrobenzene into phenylamine?', 'Tin and concentrated HCl, heat, then NaOH', 'Reduction, then liberate the free amine.', ['NaBH₄ in water', 'Conc HNO₃ and H₂SO₄', 'NaNO₂ and HCl below 10 °C']),
         ('Which reagent and conditions convert bromoethane into ethylamine?', 'Excess ammonia in ethanol, heated in a sealed tube', 'Nucleophilic substitution.', ['Aqueous NaOH, reflux', 'KCN in ethanol', 'LiAlH₄ in dry ether']),
         ('Which reagent reduces ethanenitrile to ethylamine?', 'LiAlH₄ in dry ether (or H₂ with Ni)', 'C≡N → CH₂NH₂.', ['Sn and conc HCl', 'K₂Cr₂O₇ and H₂SO₄', 'NaOH(aq)'])])
mcqs(t, [('Why is phenylamine a weaker base than ammonia?', 'The nitrogen lone pair is delocalised into the benzene ring, so it is less available to accept H⁺', 'Overlap with π system.', ['Phenylamine is less soluble', 'The ring donates electrons to nitrogen', 'Phenylamine has no lone pair']),
         ('Why does the reaction of bromoethane with ammonia give a mixture of products?', 'The ethylamine formed is itself a nucleophile and reacts with more bromoethane', 'Further substitution gives secondary and tertiary amines.', ['Ammonia is a weak base', 'Bromoethane decomposes', 'Ethylamine is an electrophile'])], D=(2, 3), C='C2')
shorts(t, [('Write an equation for the reaction of ethylamine with hydrochloric acid.', 'CH₃CH₂NH₂ + HCl → CH₃CH₂NH₃⁺Cl⁻', '[1]'),
           ('Write an equation for the reduction of nitrobenzene to phenylamine, using [H].', 'C₆H₅NO₂ + 6[H] → C₆H₅NH₂ + 2H₂O', 'products [1]; balanced [1] [2]')])
explain(t, [('Explain why ethylamine is a stronger base than ammonia.', 'The ethyl group donates electron density to the nitrogen (positive inductive effect), making the lone pair more available to accept a proton.', 'alkyl group electron-donating [1]; lone pair more available [1] [2]'),
            ('Explain why phenylamine is a weaker base than ammonia.', 'The lone pair on nitrogen overlaps with the delocalised π system of the ring, spreading the electron density and making the lone pair less available to accept H⁺.', 'lone pair delocalised into ring [1]; less available [1] [2]'),
            ('Explain why excess ammonia is used to make a primary amine from a halogenoalkane.', 'To make it more likely that the halogenoalkane reacts with ammonia rather than with the amine product, reducing the formation of secondary and tertiary amines and quaternary salts.', '[2]')])
myths(t, [('Phenylamine is a stronger base than ethylamine because the benzene ring donates electrons to the nitrogen.', 'The nitrogen lone pair is delocalised into the ring, making phenylamine a much weaker base.'),
          ('Amines are acids because they contain N–H bonds.', 'Amines are bases: the nitrogen lone pair accepts H⁺.'),
          ('Halogenoalkanes react with ammonia to give only the primary amine.', 'A mixture forms because the amine product can react further with the halogenoalkane.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def amine_ph(r, D):
    nm, f, pkah = r.choice(AMINES)
    c = r.choice([0.010, 0.050, 0.10, 0.20, 0.50])
    Kb = 10 ** (pkah - 14)
    oh = math.sqrt(Kb * c)
    ph = 14 + math.log10(oh)
    st = f'The pKa of the conjugate acid of {nm} is {pkah}. Calculate the pH of a {fx(c, 3)} mol dm⁻³ aqueous solution of {nm}. (Kw = 1.00 × 10⁻¹⁴ mol² dm⁻⁶)'
    key = f'Kb = Kw ÷ Ka = {sci(Kb, 3)} [1]; [OH⁻] = √(Kb × c) = {sci(oh, 3)} [1]; pOH = {fx(-math.log10(oh), 2)} [1]; pH = {fx(ph, 2)} [1] [4]'
    if D <= 2:
        grp = r.sample(AMINES, 4)
        best = max(grp, key=lambda a: a[2]) if r.random() < 0.5 else min(grp, key=lambda a: a[2])
        word = 'strongest' if best[2] == max(a[2] for a in grp) else 'weakest'
        return MQ(r, 'pKa values of the conjugate acids: ' + '; '.join(f'{a[0]} {a[2]}' for a in grp) + f'. Which is the {word} base?', cap(best[0]), [cap(a[0]) for a in grp if a != best],
                  f'The {"larger" if word == "strongest" else "smaller"} the pKa of the conjugate acid, the {"stronger" if word == "strongest" else "weaker"} the base: {best[0]} ({best[2]}).')
    if D <= 3:
        key = f'[OH⁻] = √(Kb × c) with Kb = {sci(Kb, 3)} [1]; [OH⁻] = {sci(oh, 3)} [1]; pH = {fx(ph, 2)} [1] [3]'
    ans = f'pH = {fx(ph, 2)}'
    return Q(st, ans, key, 'numerical')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def amine_prep(r, D):
    route = r.choice([('nitrobenzene', 123.0, 'phenylamine', 93.0, 'tin and concentrated hydrochloric acid, heat under reflux, then excess NaOH(aq)', 'C₆H₅NO₂ + 6[H] → C₆H₅NH₂ + 2H₂O'),
                      ('ethanenitrile', 41.0, 'ethylamine', 45.0, 'LiAlH₄ in dry ether (or H₂ with a Ni catalyst)', 'CH₃CN + 4[H] → CH₃CH₂NH₂'),
                      ('propanamide', 73.0, 'propylamine', 59.0, 'LiAlH₄ in dry ether', 'CH₃CH₂CONH₂ + 4[H] → CH₃CH₂CH₂NH₂ + H₂O'),
                      ('bromoethane', 108.9, 'ethylamine', 45.0, 'excess ethanolic ammonia, heated in a sealed tube', 'CH₃CH₂Br + 2NH₃ → CH₃CH₂NH₂ + NH₄Br')])
    s_, Ms, p, Mp, cond, eq = route
    ms = r.choice([2.46, 5.00, 6.15, 10.0, 12.3])
    yp = r.choice([45, 55, 63, 70, 78])
    th = ms / Ms * Mp
    act = th * yp / 100
    if D <= 2:
        return MQ(r, f'Which reagents and conditions convert {s_} into {p}?', cap(cond), [cap(x[4]) for x in [('', 0, '', 0, 'aqueous NaOH, heat under reflux'), ('', 0, '', 0, 'acidified K₂Cr₂O₇, distil'), ('', 0, '', 0, 'NaNO₂ and HCl below 10 °C'), ('', 0, '', 0, 'concentrated H₂SO₄ and HNO₃ at 50 °C')]][:3], f'{eq}.')
    st = f'{ms:.2f} g of {s_} (Mr {Ms:.1f}) was converted into {p} (Mr {Mp:.1f}) using {cond}. {g3(act)} g of {p} was obtained. Calculate the percentage yield.'
    key = f'n = {ms:.2f} ÷ {Ms:.1f} = {sci(ms / Ms, 3)} mol [1]; theoretical mass {g3(th)} g [1]; yield {yp}% [1] [3]'
    ans = f'{yp}%'
    if D >= 4:
        st += ' Write an equation for the reaction.'
        key = key.replace(' [3]', '') + f'; {eq} [1] [4]'
        ans += f'; {eq}'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def amine_case(r, D):
    st = f'{who(r)} compares the basicity of ammonia, ethylamine and phenylamine. pKa values of the conjugate acids: NH₄⁺ 9.25, CH₃CH₂NH₃⁺ 10.73, C₆H₅NH₃⁺ 4.60.'
    parts = [P_('Write an equation to show ethylamine acting as a base in water.', 'CH₃CH₂NH₂ + H₂O ⇌ CH₃CH₂NH₃⁺ + OH⁻', '[1]'),
             P_('Use the data to place the three bases in order of increasing strength and explain the order.', 'Phenylamine < ammonia < ethylamine; ethyl group donates electron density (lone pair more available); in phenylamine lone pair delocalised into ring (less available).', 'order [1]; ethylamine [1]; phenylamine [1] [3]'),
             P_('Calculate the pH of 0.100 mol dm⁻³ ethylamine.', f'pH = {fx(14 + math.log10(math.sqrt(10 ** (10.73 - 14) * 0.1)), 2)}', f'Kb = 10⁻³·²⁷ [1]; [OH⁻] = {sci(math.sqrt(10 ** (10.73 - 14) * 0.1), 3)} [1]; pH [1] [3]'),
             P_('Describe how phenylamine is made from benzene in two steps.', 'Nitration (conc HNO₃/H₂SO₄, < 55 °C) to nitrobenzene; reduction with Sn/conc HCl under reflux, then NaOH.', 'step 1 [1]; step 2 [1] [2]'),
             P_('Explain why the product mixture is made alkaline with NaOH after reduction.', 'In acid the amine is present as the phenylammonium salt; NaOH releases the free amine.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how primary amines are prepared, and explain the relative basic strengths of ammonia, ethylamine and phenylamine.', 'Halogenoalkane + excess ethanolic NH₃ in sealed tube (mixture of products); reduction of nitriles (LiAlH₄ or H₂/Ni) and amides (LiAlH₄); phenylamine from nitrobenzene with Sn/HCl then NaOH; basicity from lone pair on N; alkyl +I effect increases; delocalisation into ring decreases; order phenylamine < ammonia < ethylamine; salts with acids.',
           'preparations [3]; lone pair basis [1]; ethylamine [1]; phenylamine [1]; order / salt formation [1] [7]')])
t9a = t

# ---------------------------------------------------------------------
DIAZ = [('phenylamine', 'C₆H₅NH₂', 'benzenediazonium chloride', 'C₆H₅N₂⁺Cl⁻'), ('4-methylphenylamine', 'CH₃C₆H₄NH₂', '4-methylbenzenediazonium chloride', 'CH₃C₆H₄N₂⁺Cl⁻'),
        ('4-nitrophenylamine', 'O₂NC₆H₄NH₂', '4-nitrobenzenediazonium chloride', 'O₂NC₆H₄N₂⁺Cl⁻'), ('4-chlorophenylamine', 'ClC₆H₄NH₂', '4-chlorobenzenediazonium chloride', 'ClC₆H₄N₂⁺Cl⁻')]
COUP = [('phenol', 'alkaline solution (NaOH)', 'C₆H₄OH', 'a yellow-orange azo dye'), ('naphthalen-2-ol', 'alkaline solution (NaOH)', 'C₁₀H₆OH', 'an orange-red azo dye'),
        ('N,N-dimethylphenylamine', 'weakly acidic solution', 'C₆H₄N(CH₃)₂', 'a yellow azo dye')]
DYE_F = {('phenylamine', 'phenol'): 'C12H10N2O', ('phenylamine', 'naphthalen-2-ol'): 'C16H12N2O', ('phenylamine', 'N,N-dimethylphenylamine'): 'C14H15N3',
         ('4-methylphenylamine', 'phenol'): 'C13H12N2O', ('4-methylphenylamine', 'naphthalen-2-ol'): 'C17H14N2O', ('4-methylphenylamine', 'N,N-dimethylphenylamine'): 'C15H17N3',
         ('4-nitrophenylamine', 'phenol'): 'C12H9N3O3', ('4-nitrophenylamine', 'naphthalen-2-ol'): 'C16H11N3O3', ('4-nitrophenylamine', 'N,N-dimethylphenylamine'): 'C14H14N4O2',
         ('4-chlorophenylamine', 'phenol'): 'C12H9N2OCl', ('4-chlorophenylamine', 'naphthalen-2-ol'): 'C16H11N2OCl', ('4-chlorophenylamine', 'N,N-dimethylphenylamine'): 'C14H14N3Cl'}

t = T('Phenylamine and azo dyes: diazotisation and coupling', 'phenylamine and azo dyes')
facts(t, [('diazotisation', 'the reaction of a primary aromatic amine with nitrous acid (NaNO₂ + HCl) below 10 °C to form a diazonium salt'),
          ('diazonium ion', 'Ar–N₂⁺, the cation formed by diazotisation, which acts as an electrophile in coupling reactions'),
          ('coupling reaction', 'the electrophilic substitution of a diazonium ion onto an activated arene such as phenol, forming an azo compound'),
          ('azo group', 'the –N=N– linkage that joins two aromatic rings in an azo dye'),
          ('nitrous acid', 'HNO₂, generated in situ from sodium nitrite and hydrochloric acid because it is unstable'),
          ('chromophore', 'the part of a dye molecule, such as an extended delocalised system containing –N=N–, responsible for absorbing visible light')])
mcqs(t, [('Which reagents and conditions convert phenylamine into benzenediazonium chloride?', 'NaNO₂ and dilute HCl, below 10 °C', 'Nitrous acid generated in situ.', ['Conc HNO₃ and H₂SO₄ at 55 °C', 'Sn and conc HCl, reflux', 'NaOH(aq), heat']),
         ('What is formed when a solution of benzenediazonium chloride is warmed above 10 °C?', 'Phenol and nitrogen gas', 'C₆H₅N₂⁺ + H₂O → C₆H₅OH + N₂ + H⁺.', ['Phenylamine', 'Benzene and NH₃', 'An azo dye']),
         ('At which position of phenol does coupling with a diazonium ion mainly occur?', 'The 4-position', 'Para to –OH.', ['The 3-position', 'The oxygen atom', 'The 1-position']),
         ('Why is the coupling of benzenediazonium ions with phenol carried out in alkaline solution?', 'To form the phenoxide ion, which is more strongly activated towards electrophilic attack', 'Phenoxide is more electron-rich.', ['To keep the diazonium ion stable', 'To neutralise the azo dye', 'To make the dye insoluble'])])
mcqs(t, [('Why must diazotisation be carried out below 10 °C?', 'The diazonium salt decomposes at higher temperatures, giving nitrogen and phenol', 'Unstable.', ['The reaction is too exothermic to start', 'Nitrous acid is a gas above 10 °C', 'Phenylamine freezes']),
         ('Why are azo compounds coloured?', 'The –N=N– group extends the delocalised π system across both rings, so visible light is absorbed', 'Extended conjugation.', ['They contain transition metal ions', 'They are ionic', 'The N=N bond is very weak'])], D=(2, 3), C='C2')
shorts(t, [('Write an equation for the formation of benzenediazonium chloride from phenylamine.', 'C₆H₅NH₂ + HNO₂ + HCl → C₆H₅N₂⁺Cl⁻ + 2H₂O', 'species [1]; balanced [1] [2]'),
           ('Write an equation for the coupling of benzenediazonium ions with phenol.', 'C₆H₅N₂⁺ + C₆H₅OH → C₆H₅N=NC₆H₄OH + H⁺', 'product [1]; balanced [1] [2]')])
explain(t, [('Explain why benzenediazonium ions act as electrophiles in coupling reactions.', 'The terminal nitrogen of –N₂⁺ is electron-deficient (positive charge) and accepts a pair of electrons from the activated ring of phenol, forming an –N=N– link by electrophilic substitution.', 'N₂⁺ electron-deficient [1]; attacked by electron-rich ring [1] [2]'),
            ('Explain why aryl diazonium salts are more stable than alkyl diazonium salts.', 'The positive charge of the –N₂⁺ group is partly delocalised into the benzene ring, stabilising it; alkyl diazonium ions decompose immediately even at low temperature.', '[2]'),
            ('Explain why azo dyes made from different amines and coupling agents have different colours.', 'Changes in the substituents and extent of the delocalised system change the energy gap and so the wavelength of visible light absorbed.', '[2]')])
myths(t, [('Diazotisation of phenylamine should be carried out at about 50 °C to speed up the reaction.', 'It must be below 10 °C, otherwise the diazonium salt decomposes to phenol and nitrogen.'),
          ('In azo coupling, the diazonium ion acts as a nucleophile.', 'The diazonium ion is an electrophile; the activated ring of the coupling agent is the nucleophile.'),
          ('Nitrous acid is bought as a stable reagent.', 'HNO₂ is unstable; it is made in situ from NaNO₂ and dilute HCl.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def azo_q(r, D):
    am, af, dz, dzf = r.choice(DIAZ)
    cp, ccond, frag, col = r.choice(COUP)
    ar = dzf.replace('N₂⁺Cl⁻', '')
    prod = f'{ar}–N=N–{frag}'
    if D <= 2:
        return MQ(r, f'{cap(am)} is diazotised and then coupled with {cp}. What is the structure of the product?', prod, [f'{ar}–NH–{frag}', f'{ar}–N₂⁺', f'{ar}–O–{frag}'], f'Coupling forms an –N=N– azo link: {prod}.')
    st = f'Describe how {am} could be converted into an azo dye by coupling with {cp}. Give the reagents and conditions for each stage and the structure of the dye.'
    ans = f'Stage 1: NaNO₂ and dilute HCl below 10 °C forms {dz}, {dzf}. Stage 2: add to {cp} in {ccond} (cold): {prod}, {col}.'
    key = 'NaNO₂ + HCl [1]; below 10 °C [1]; diazonium salt [1]; coupling conditions [1]; azo product structure [1]'
    tot = 5
    if D >= 4:
        mm = Mr(DYE_F[(am, cp)])
        st += ' Calculate the Mr of the dye.'
        ans += f' Mr = {fx(mm, 1)}.'
        key += f'; Mr {fx(mm, 1)} [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def azo_yield(r, D):
    am, af, dz, dzf = r.choice(DIAZ)
    cp, ccond, frag, col = r.choice(COUP)
    Ma = Mr({'phenylamine': 'C6H7N', '4-methylphenylamine': 'C7H9N', '4-nitrophenylamine': 'C6H6N2O2', '4-chlorophenylamine': 'C6H6NCl'}[am])
    Md = Mr(DYE_F[(am, cp)])
    ma = r.choice([0.93, 1.86, 2.79, 4.65])
    yp = r.choice([40, 52, 61, 68, 75])
    th = ma / Ma * Md
    act = th * yp / 100
    st = f'{ma:.2f} g of {am} (Mr {Ma:.1f}) was diazotised and coupled with excess {cp}, giving {g3(act)} g of azo dye (Mr {Md:.1f}). Calculate the percentage yield.'
    key = f'n(amine) = {sci(ma / Ma, 3)} mol [1]; theoretical mass = {g3(th)} g [1]; yield = {yp}% [1] [3]'
    ans = f'{yp}%'
    if D >= 4:
        st += ' Suggest why the yield is low if the diazonium solution is allowed to warm up before coupling.'
        ans += '; above 10 °C the diazonium ion decomposes to phenol and N₂, so less is available for coupling'
        key = key.replace(' [3]', '') + '; decomposition to phenol + N₂ [1] [4]'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def azo_case(r, D):
    am, af, dz, dzf = r.choice(DIAZ)
    cp, ccond, frag, col = r.choice(COUP[:2])
    ar = dzf.replace('N₂⁺Cl⁻', '')
    st = f'A dye company in {city(r)} makes an azo dye from benzene in four steps, via nitrobenzene, then {am if am == "phenylamine" else "phenylamine derivative " + am}, then {dz}, which is coupled with {cp}.'
    parts = [P_('Give the reagents and conditions for converting benzene into nitrobenzene and then into phenylamine.', 'Conc HNO₃ + conc H₂SO₄ below 55 °C; then Sn + conc HCl, reflux, then NaOH(aq).', 'nitration [1]; reduction [1] [2]'),
             P_('Write an equation for the diazotisation and explain why the temperature must be kept low.', f'{af} + HNO₂ + HCl → {dzf} + 2H₂O; below 10 °C as the diazonium salt decomposes above this.', 'equation [1]; reason [1] [2]'),
             P_('Give the structure of the dye and the conditions for coupling.', f'{ar}–N=N–{frag} (coupling at the 4-position / 1-position for naphthol); {ccond}, cold', 'structure [1]; conditions [1] [2]'),
             P_('Explain why the dye is coloured.', 'The –N=N– group links two aromatic rings into an extended delocalised system that absorbs light in the visible region.', '[2]'),
             P_('State what is formed if the diazonium solution is warmed with water.', 'A phenol (and N₂ gas, H⁺).', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the formation of azo dyes from phenylamine, including reagents, conditions, equations and the reasons for the conditions used.', 'Phenylamine from nitrobenzene (Sn/HCl); diazotisation: NaNO₂ + HCl → HNO₂ in situ, below 10 °C, C₆H₅N₂⁺Cl⁻; decomposition above 10 °C to phenol + N₂; coupling with phenol in NaOH(aq) (phenoxide more activated) at 4-position; electrophilic substitution; –N=N– extended delocalisation gives colour; uses as dyes and indicators.',
           'diazotisation reagents and temperature [2]; equation [1]; coupling conditions and product [2]; mechanism type [1]; origin of colour [1] [7]')])
t9b = t

# ---------------------------------------------------------------------
AMIDES = [('ethanamide', 'CH₃CONH₂', 'ethanoic acid', 'CH₃COOH', 'ammonia', 'NH₃', 'ethylamine', 'CH₃CH₂NH₂', 'ethanoate', 59.0),
          ('propanamide', 'CH₃CH₂CONH₂', 'propanoic acid', 'CH₃CH₂COOH', 'ammonia', 'NH₃', 'propylamine', 'CH₃CH₂CH₂NH₂', 'propanoate', 73.0),
          ('N-methylethanamide', 'CH₃CONHCH₃', 'ethanoic acid', 'CH₃COOH', 'methylamine', 'CH₃NH₂', 'N-methylethylamine', 'CH₃CH₂NHCH₃', 'ethanoate', 73.0),
          ('N-ethylpropanamide', 'CH₃CH₂CONHCH₂CH₃', 'propanoic acid', 'CH₃CH₂COOH', 'ethylamine', 'CH₃CH₂NH₂', 'N-ethylpropylamine', 'CH₃CH₂CH₂NHCH₂CH₃', 'propanoate', 101.0),
          ('benzamide', 'C₆H₅CONH₂', 'benzoic acid', 'C₆H₅COOH', 'ammonia', 'NH₃', 'phenylmethylamine', 'C₆H₅CH₂NH₂', 'benzoate', 121.0),
          ('N-phenylethanamide', 'CH₃CONHC₆H₅', 'ethanoic acid', 'CH₃COOH', 'phenylamine', 'C₆H₅NH₂', 'N-ethylphenylamine', 'CH₃CH₂NHC₆H₅', 'ethanoate', 135.0)]

t = T('Amides: formation, hydrolysis and reduction', 'amides: formation, hydrolysis')
facts(t, [('amide', 'a compound containing the –CONH– group (–CONH₂ for primary amides), e.g. ethanamide CH₃CONH₂'),
          ('amide hydrolysis', 'the breaking of the C–N bond of an amide by water, catalysed by heating with aqueous acid or alkali'),
          ('reduction of an amide', 'the conversion of an amide into an amine with LiAlH₄ in dry ether, e.g. CH₃CONH₂ → CH₃CH₂NH₂'),
          ('peptide (amide) link', 'the –CONH– linkage that joins amino acids in proteins and monomers in polyamides'),
          ('lithium tetrahydridoaluminate', 'LiAlH₄, a powerful reducing agent used in dry ether to reduce amides and nitriles to amines')])
mcqs(t, [('What are the products of heating ethanamide with dilute hydrochloric acid?', 'Ethanoic acid and ammonium chloride', 'Acid hydrolysis.', ['Ethylamine and water', 'Sodium ethanoate and ammonia', 'Ethanol and ammonia']),
         ('What are the products of heating ethanamide with aqueous sodium hydroxide?', 'Sodium ethanoate and ammonia', 'Alkaline hydrolysis releases NH₃ gas.', ['Ethanoic acid and ammonium chloride', 'Ethylamine and water', 'Ethanal and ammonia']),
         ('What is formed when ethanamide is reduced by LiAlH₄?', 'Ethylamine', 'C=O reduced to CH₂.', ['Ethanol', 'Methylamine', 'Ethanenitrile']),
         ('Which reagent forms N-methylethanamide from ethanoyl chloride?', 'Methylamine', 'Acyl chloride + primary amine.', ['Ammonia', 'Methanol', 'Ethylamine'])])
mcqs(t, [('Why are amides much weaker bases than amines?', 'The nitrogen lone pair is delocalised over the C=O group, so it is not available to accept H⁺', 'Amide resonance.', ['Amides have no lone pairs', 'Amides are ionic', 'Amides are insoluble in water']),
         ('Why does alkaline hydrolysis of an amide give off a gas that turns red litmus blue?', 'Ammonia (or a volatile amine) is released', 'NH₃ is alkaline.', ['Carbon dioxide is released', 'Hydrogen is released', 'Chlorine is released'])], D=(2, 3), C='C2')
shorts(t, [('Write an equation for the hydrolysis of ethanamide by aqueous sodium hydroxide.', 'CH₃CONH₂ + NaOH → CH₃COONa + NH₃', '[2]'),
           ('Write an equation for the reduction of propanamide using [H].', 'CH₃CH₂CONH₂ + 4[H] → CH₃CH₂CH₂NH₂ + H₂O', '[2]')])
explain(t, [('Explain why amides are only very weak bases.', 'The lone pair on nitrogen is delocalised into the C=O π bond (partial double-bond character of C–N), and the carbonyl group withdraws electron density, so the lone pair is not available to bond to H⁺.', 'delocalisation of lone pair [1]; not available for H⁺ [1] [2]'),
            ('Explain why amides need prolonged heating with acid or alkali to hydrolyse, whereas acyl chlorides react with cold water.', 'The C–N bond in amides is strengthened by delocalisation and NH₂⁻ is a poor leaving group, so hydrolysis is slow; acyl chlorides have a very δ+ carbon and a good leaving group (Cl⁻).', '[2]')])
myths(t, [('Amides are basic like amines because they contain an NH₂ group.', 'Amides are almost neutral because the nitrogen lone pair is delocalised into the C=O group.'),
          ('Acid hydrolysis of ethanamide gives ammonia gas.', 'In acid, ammonium ions form (NH₄⁺); ammonia is released only in alkaline hydrolysis.'),
          ('Reduction of an amide with LiAlH₄ gives a carboxylic acid.', 'Reduction converts the C=O into CH₂, giving an amine.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def amide_q(r, D):
    nm, f, acid, af, base, bf, red, rf, anion, M = r.choice(AMIDES)
    kind = r.choice(['acid', 'alkali', 'reduce'])
    acidsalt = {'NH₃': 'NH₄⁺', 'CH₃NH₂': 'CH₃NH₃⁺', 'CH₃CH₂NH₂': 'CH₃CH₂NH₃⁺', 'C₆H₅NH₂': 'C₆H₅NH₃⁺'}[bf]
    res = {'acid': (f'{acid} ({af}) and {acidsalt} ions', 'hot dilute hydrochloric acid (heated under reflux)'),
           'alkali': (f'sodium {anion} ({af.replace("COOH", "COO⁻Na⁺")}) and {base} ({bf})', 'hot aqueous sodium hydroxide (heated under reflux)'),
           'reduce': (f'{red} ({rf})', 'LiAlH₄ in dry ether')}
    prod, cond = res[kind]
    if D <= 2:
        return MQ(r, f'What is formed when {nm}, {f}, is treated with {cond}?', cap(prod), [cap(res[k][0]) for k in res if k != kind] + [f'{cap(acid)} and hydrogen'], f'{cap(prod)}.')
    st = f'State the products of the reaction of {nm}, {f}, with {cond}, and name the type of reaction.'
    ans = f'{cap(prod)}; ' + ('hydrolysis' if kind != 'reduce' else 'reduction')
    key = 'products [2]; type of reaction [1]'
    tot = 3
    if D >= 4:
        o = r.choice([k for k in res if k != kind])
        st += f' Compare these products with those formed with {res[o][1]}.'
        ans += f'; with {res[o][1]}: {res[o][0]}'
        key += '; products of second reaction [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def amide_calc(r, D):
    nm, f, acid, af, base, bf, red, rf, anion, M = r.choice(AMIDES[:2] + AMIDES[4:5])
    m_ = r.choice([1.18, 2.36, 2.95, 3.54, 1.46, 2.92])
    n_ = m_ / M
    c = r.choice([0.100, 0.200, 0.500])
    V = n_ / c * 1000
    st = f'{m_:.2f} g of {nm} (Mr {M:.1f}) was heated under reflux with excess NaOH(aq). All the ammonia released was absorbed in excess acid. Calculate the volume of {fx(c, 3)} mol dm⁻³ HCl that reacts with this ammonia.'
    key = f'n(amide) = {m_:.2f} ÷ {M:.1f} = {sci(n_, 3)} mol [1]; n(NH₃) = n(HCl) = {sci(n_, 3)} [1]; V = {g3(V)} cm³ [1] [3]'
    ans = f'{g3(V)} cm³'
    if D >= 4:
        st += ' Write the equation for the hydrolysis.'
        key = key.replace(' [3]', '') + f'; {f} + NaOH → {af.replace("COOH", "COONa")} + NH₃ [1] [4]'
        ans += f'; {f} + NaOH → {af.replace("COOH", "COONa")} + NH₃'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def amide_case(r, D):
    nm, f, acid, af, base, bf, red, rf, anion, M = r.choice(AMIDES)
    acyl = {'CH₃COOH': 'ethanoyl chloride', 'CH₃CH₂COOH': 'propanoyl chloride', 'C₆H₅COOH': 'benzoyl chloride'}[af]
    st = f'{who(r)} prepares {nm}, {f}, from {acyl} and {base}, and then investigates its reactions.'
    parts = [P_('Write an equation for the formation of the amide.', f'{acyl.split()[0]} chloride + 2{bf} → {f} + {bf.replace("H₂", "H₃", 1) if bf != "NH₃" else "NH₄"}⁺Cl⁻'.replace('NH₄⁺Cl⁻', 'NH₄Cl').replace(acyl.split()[0] + ' chloride', af.replace('OH', 'Cl')), 'products [1]; balanced [1] [2]'),
             P_('Give the products of hydrolysis of the amide with hot dilute acid and with hot aqueous alkali.', f'acid: {acid} + {base} as its salt; alkali: the {anion} salt + {base}', 'acid [1]; alkali [1] [2]'),
             P_('Give the reagent for reducing the amide and name the product.', f'LiAlH₄ in dry ether; {red} ({rf})', '[2]'),
             P_('Explain why the amide does not react with dilute HCl at room temperature as an amine would.', 'The N lone pair is delocalised into the C=O group, so the amide is not basic.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the formation of amides and their reactions with acids, alkalis and reducing agents, and explain why amides are much weaker bases than amines.', 'Formation from acyl chlorides with NH₃ or primary amines (equations); acid hydrolysis → carboxylic acid + ammonium/alkylammonium salt; alkaline hydrolysis → carboxylate + NH₃/amine; reduction by LiAlH₄ to amines; amide C–N partial double bond, lone pair delocalised onto C=O, so not basic; peptide links in proteins.',
           'formation [2]; acid hydrolysis [1]; alkaline hydrolysis [1]; reduction [1]; basicity explanation [2] [7]')])
t9c = t

# ---------------------------------------------------------------------
AA = [('glycine', 'Gly', 'H', 5.97, 75.0), ('alanine', 'Ala', 'CH₃', 6.00, 89.0), ('serine', 'Ser', 'CH₂OH', 5.68, 105.0), ('valine', 'Val', 'CH(CH₃)₂', 5.96, 117.0),
      ('leucine', 'Leu', 'CH₂CH(CH₃)₂', 5.98, 131.0), ('phenylalanine', 'Phe', 'CH₂C₆H₅', 5.48, 165.0), ('cysteine', 'Cys', 'CH₂SH', 5.07, 121.1),
      ('aspartic acid', 'Asp', 'CH₂COOH', 2.77, 133.0), ('glutamic acid', 'Glu', 'CH₂CH₂COOH', 3.22, 147.0), ('lysine', 'Lys', '(CH₂)₄NH₂', 9.74, 146.0),
      ('arginine', 'Arg', '(CH₂)₃NHC(NH)NH₂', 10.76, 174.0), ('histidine', 'His', 'CH₂C₃H₃N₂', 7.59, 155.0)]
NEUTRAL = AA[:7]


def aac(R):
    return 'CH₂' if R == 'H' else f'CH({R})'


def and_list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]

t = T('Amino acids: zwitterions, isoelectric point and peptide bonds; electrophoresis', 'amino acids: zwitterions')
facts(t, [('zwitterion', 'an ion with both a positive and a negative charge but no overall charge, e.g. ⁺H₃NCH₂COO⁻'),
          ('isoelectric point', 'the pH at which an amino acid exists mainly as its zwitterion and has no overall charge'),
          ('electrophoresis', 'the separation of charged species, such as amino acids or peptides, by their movement in an electric field on a gel or paper at a fixed pH'),
          ('peptide bond', 'the –CONH– amide link formed by a condensation reaction between the –COOH of one amino acid and the –NH₂ of another'),
          ('dipeptide', 'a molecule formed when two amino acids join by one peptide bond, with loss of water'),
          ('α-amino acid', 'a compound with an –NH₂ group and a –COOH group on the same carbon atom, H₂NCH(R)COOH')])
mcqs(t, [('What is the main form of glycine at pH 1?', '⁺H₃NCH₂COOH', 'Low pH: both groups protonated.', ['H₂NCH₂COO⁻', '⁺H₃NCH₂COO⁻', 'H₂NCH₂COOH']),
         ('What is the main form of glycine at pH 12?', 'H₂NCH₂COO⁻', 'High pH: both groups deprotonated.', ['⁺H₃NCH₂COOH', '⁺H₃NCH₂COO⁻', 'H₂NCH₂COOH']),
         ('Why do amino acids have high melting points?', 'They exist as zwitterions with strong ionic attractions between them', 'Ionic lattice.', ['They have strong covalent bonds between molecules', 'They are polymers', 'They are metals']),
         ('How many different dipeptides can be formed from one molecule each of glycine and alanine?', '2', 'Gly–Ala and Ala–Gly.', ['1', '3', '4'])])
mcqs(t, [('In electrophoresis at pH 7, aspartic acid (isoelectric point 2.8) moves towards', 'the anode (positive electrode)', 'pH > pI: negatively charged.', ['the cathode (negative electrode)', 'neither electrode', 'both electrodes']),
         ('In electrophoresis at pH 6.0, why does alanine (isoelectric point 6.0) not move?', 'It is a zwitterion with no overall charge at this pH', 'pH = pI.', ['It is too large', 'It is positively charged', 'It is insoluble'])], D=(2, 3), C='C2')
shorts(t, [('Give the structure of the zwitterion of alanine.', '⁺H₃N–CH(CH₃)–COO⁻', '[1]'),
           ('Write an equation for the formation of the dipeptide Gly–Ala.', 'H₂NCH₂COOH + H₂NCH(CH₃)COOH → H₂NCH₂CONHCH(CH₃)COOH + H₂O', 'peptide link [1]; water [1] [2]')])
explain(t, [('Explain how electrophoresis separates a mixture of amino acids.', 'The mixture is placed on a gel in a buffer at a chosen pH with a potential difference applied; each amino acid has a charge depending on pH relative to its isoelectric point; positive ions move to the cathode, negative to the anode; speed depends on charge and size (Mr); spots are located with ninhydrin and compared with standards.', 'buffer and voltage [1]; charge depends on pH vs pI [1]; direction [1]; speed depends on charge/size [1] [4]'),
            ('Explain why amino acids are soluble in water but insoluble in non-polar solvents.', 'Zwitterions are ionic and form strong ion–dipole attractions with water; non-polar solvents cannot overcome the ionic attractions.', '[2]'),
            ('Explain why the hydrolysis of a protein gives a mixture of amino acids.', 'Heating with 6 mol dm⁻³ HCl breaks the peptide (amide) bonds, releasing the individual amino acids that made up the chain.', '[2]')])
myths(t, [('At its isoelectric point, an amino acid has no charged groups.', 'At the isoelectric point it is a zwitterion: it has both + and − groups but no overall charge.'),
          ('In electrophoresis, all amino acids move towards the anode.', 'Direction depends on the buffer pH relative to the isoelectric point; amino acids with pI above the buffer pH are positive and move to the cathode.'),
          ('A dipeptide from glycine and alanine can only be Gly–Ala.', 'Two different dipeptides are possible, Gly–Ala and Ala–Gly, because the ends are different.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def electro_q(r, D):
    ph = r.choice([2.0, 4.0, 5.5, 6.5, 7.0, 8.0, 9.0, 11.0])
    trio = r.sample(AA, 3)
    if any(abs(a[3] - ph) < 0.15 for a in trio):
        return None
    if D >= 3 and len({a[3] > ph for a in trio}) < 2:
        return None

    def go(a):
        return 'towards the cathode (−)' if a[3] > ph else 'towards the anode (+)'
    if D <= 2:
        a = trio[0]
        return MQ(r, f'A mixture containing {a[0]} (isoelectric point {a[3]}) is analysed by electrophoresis in a buffer at pH {fx(ph, 1)}. In which direction does {a[0]} move?', cap(go(a)), [cap('towards the anode (+)' if a[3] > ph else 'towards the cathode (−)'), 'It does not move', 'It moves in both directions'], f'pH {"<" if a[3] > ph else ">"} pI, so it is {"positively" if a[3] > ph else "negatively"} charged.')
    st = f'A mixture of {", ".join(a[0] for a in trio[:2])} and {trio[2][0]} (isoelectric points {", ".join(str(a[3]) for a in trio)}) is analysed by electrophoresis in a buffer at pH {fx(ph, 1)}. Predict and explain the direction of movement of each amino acid.'
    ans = '; '.join(f'{a[0]}: {"positive" if a[3] > ph else "negative"}, moves {go(a)}' for a in trio) + '. Charge depends on whether the buffer pH is below (positive) or above (negative) the isoelectric point.'
    key = 'each direction [1] ×3; explanation in terms of pH vs isoelectric point [1]'
    tot = 4
    if D >= 4:
        st += ' Suggest a factor, other than charge, that affects how far each amino acid travels.'
        ans += ' Size/Mr also matters: smaller ions with the same charge move faster.'
        key += '; size / Mr [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def peptide_q(r, D):
    a, b = r.sample(NEUTRAL, 2)
    mode = r.choice(['mr', 'count', 'struct']) if D >= 3 else r.choice(['mr', 'count'])
    if mode == 'mr':
        k = r.choice([2, 3]) if D >= 3 else 2
        grp = [a, b] if k == 2 else [a, b, r.choice([x for x in NEUTRAL if x not in (a, b)])]
        tot_ = sum(x[4] for x in grp) - 18.0 * (k - 1)
        st = f'Calculate the Mr of the {"dipeptide" if k == 2 else "tripeptide"} {"–".join(x[1] for x in grp)}. Mr values: ' + ', '.join(f'{x[0]} {fx(x[4], 1)}' for x in grp) + ', water 18.0.'
        key = f'sum of amino acids = {fx(sum(x[4] for x in grp), 1)} [1]; minus {k - 1} × 18.0 = {fx(tot_, 1)} [1] [2]'
        if D <= 2:
            return NQ(r, st.replace('Calculate the Mr', 'What is the Mr').replace(', water 18.0.', ', water 18.0?'), tot_, [tot_ + 18, tot_ + 36, tot_ - 18, sum(x[4] for x in grp) / k], '', key, f=lambda v: fx(v, 1))
        return Q(st, fx(tot_, 1), key, 'numerical')
    if mode == 'count':
        n_ = r.choice([2, 3])
        grp = r.sample(NEUTRAL, n_)
        cnt = math.factorial(n_)
        st = f'How many different {"dipeptides" if n_ == 2 else "tripeptides"} can be made using one molecule each of ' + and_list(x[0] for x in grp) + ', with each amino acid used once?'
        key = f'{n_}! sequences = {cnt} [1]'
        if D <= 2:
            return MQ(r, st, str(cnt), [str(x) for x in (1, 3, 4, 9, 27) if x != cnt][:3], f'{n_}! = {cnt} sequences.')
        return Q(st + ' List their sequences.', f'{cnt}: ' + ', '.join('–'.join(x[1] for x in p) for p in __import__('itertools').permutations(grp)), key.replace(' [1]', '') + ' [1]; all sequences listed [1] [2]', 'numerical')
    st = f'Write the structural formula of the dipeptide formed when the –COOH group of {a[0]} (R = {a[2]}) reacts with the –NH₂ group of {b[0]} (R = {b[2]}). Circle-describe the peptide bond and name the type of reaction.'
    return Q(st, f'H₂N–{aac(a[2])}–CO–NH–{aac(b[2])}–COOH; peptide bond –CO–NH–; condensation (water eliminated)', 'correct order of residues [1]; peptide link [1]; condensation [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def aa_case(r, D):
    a, b, c = r.sample(AA, 3)
    ph = r.choice([5.0, 6.0, 7.0, 8.0])
    while any(abs(x[3] - ph) < 0.3 for x in (a, b, c)):
        ph += 0.5
    st = f'{who(r)} hydrolyses a tripeptide and separates the products by electrophoresis at pH {fx(ph, 1)}. The amino acids are {a[0]} (pI {a[3]}), {b[0]} (pI {b[3]}) and {c[0]} (pI {c[3]}).'
    parts = [P_('State the reagents and conditions for hydrolysing the tripeptide.', 'Heat under reflux with 6 mol dm⁻³ HCl(aq) for several hours (or enzyme).', '[2]'),
             P_('Predict the direction of movement of each amino acid.', '; '.join(f'{x[0]}: {"to cathode" if x[3] > ph else "to anode"}' for x in (a, b, c)), 'all three correct [2]; two correct [1] [2]'),
             (P_(f'Write the structures of {a[0]} at pH 1 and at pH 13.', f'pH 1: ⁺H₃N–{aac(a[2])}–COOH; pH 13: H₂N–{aac(a[2])}–COO⁻', 'each structure [1] [2]') if a in NEUTRAL else
              P_(f'Explain why the isoelectric point of {a[0]} is very different from that of glycine (5.97).', f'Its side chain ({a[2]}) contains an extra {"acidic –COOH" if a[3] < 5 else "basic nitrogen"} group, which {"loses H⁺" if a[3] < 5 else "gains H⁺"}, so a {"lower" if a[3] < 5 else "higher"} pH is needed for no overall charge.', '[2]')),
             P_('Explain how the spots are located and identified after electrophoresis.', 'Spray with ninhydrin (purple spots) or use UV; compare distances with known standards run under the same conditions.', '[2]'),
             P_('State how many different tripeptides could contain these three amino acids, each once.', '6 (3! sequences)', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the acid–base properties of amino acids, the formation and hydrolysis of peptide bonds, and how electrophoresis is used to separate and identify amino acids.', 'H₂NCH(R)COOH; zwitterion ⁺H₃NCH(R)COO⁻ in solid and at pI; cation at low pH, anion at high pH; high melting point, solubility; condensation to form peptide bond, dipeptide equation, water lost; hydrolysis with 6 M HCl reflux; electrophoresis: buffer pH, charge relative to pI, direction to anode/cathode, rate depends on charge and size, ninhydrin, comparison with standards.',
           'zwitterion and pI [2]; forms at low/high pH [1]; peptide formation/hydrolysis [2]; electrophoresis principles [2] [7]')])
t9d = t

CHAPTERS[9] = [t9a, t9b, t9c, t9d]


# ===================================================================== 10 Polymerisation
CPOLY = [('ethane-1,2-diol', 'HOCH₂CH₂OH', 62.0, 'benzene-1,4-dicarboxylic acid', 'HOOC–C₆H₄–COOH', 166.0, 'polyester', 'PET (Terylene)', 'H₂O', 18.0, '–OCH₂CH₂O–CO–C₆H₄–CO–', 'ester'),
         ('hexane-1,6-diamine', 'H₂N(CH₂)₆NH₂', 116.0, 'hexanedioic acid', 'HOOC(CH₂)₄COOH', 146.0, 'polyamide', 'nylon-6,6', 'H₂O', 18.0, '–NH(CH₂)₆NH–CO(CH₂)₄CO–', 'amide'),
         ('hexane-1,6-diamine', 'H₂N(CH₂)₆NH₂', 116.0, 'hexanedioyl dichloride', 'ClOC(CH₂)₄COCl', 183.0, 'polyamide', 'nylon-6,6', 'HCl', 36.5, '–NH(CH₂)₆NH–CO(CH₂)₄CO–', 'amide'),
         ('benzene-1,4-diamine', 'H₂N–C₆H₄–NH₂', 108.0, 'benzene-1,4-dicarbonyl dichloride', 'ClOC–C₆H₄–COCl', 203.0, 'polyamide', 'Kevlar', 'HCl', 36.5, '–NH–C₆H₄–NH–CO–C₆H₄–CO–', 'amide'),
         ('hexane-1,6-diamine', 'H₂N(CH₂)₆NH₂', 116.0, 'decanedioyl dichloride', 'ClOC(CH₂)₈COCl', 239.0, 'polyamide', 'nylon-6,10', 'HCl', 36.5, '–NH(CH₂)₆NH–CO(CH₂)₈CO–', 'amide'),
         ('butane-1,4-diol', 'HO(CH₂)₄OH', 90.0, 'butanedioic acid', 'HOOC(CH₂)₂COOH', 118.0, 'polyester', 'poly(butylene succinate)', 'H₂O', 18.0, '–O(CH₂)₄O–CO(CH₂)₂CO–', 'ester'),
         ('propane-1,3-diol', 'HO(CH₂)₃OH', 76.0, 'benzene-1,4-dicarboxylic acid', 'HOOC–C₆H₄–COOH', 166.0, 'polyester', 'poly(propylene terephthalate)', 'H₂O', 18.0, '–O(CH₂)₃O–CO–C₆H₄–CO–', 'ester'),
         ('ethane-1,2-diol', 'HOCH₂CH₂OH', 62.0, 'hexanedioic acid', 'HOOC(CH₂)₄COOH', 146.0, 'polyester', 'poly(ethylene adipate)', 'H₂O', 18.0, '–OCH₂CH₂O–CO(CH₂)₄CO–', 'ester')]
SPOLY = [('2-hydroxypropanoic acid (lactic acid)', 'CH₃CH(OH)COOH', 90.0, 'polyester', 'poly(lactic acid), PLA', '–OCH(CH₃)CO–', 'ester'),
         ('hydroxyethanoic acid', 'HOCH₂COOH', 76.0, 'polyester', 'poly(glycolic acid)', '–OCH₂CO–', 'ester'),
         ('6-aminohexanoic acid', 'H₂N(CH₂)₅COOH', 131.0, 'polyamide', 'nylon-6', '–NH(CH₂)₅CO–', 'amide'),
         ('glycine', 'H₂NCH₂COOH', 75.0, 'polyamide (polypeptide)', 'poly(glycine)', '–NHCH₂CO–', 'amide'),
         ('3-hydroxybutanoic acid', 'CH₃CH(OH)CH₂COOH', 104.0, 'polyester', 'poly(3-hydroxybutanoate), PHB', '–OCH(CH₃)CH₂CO–', 'ester')]

t = T('Condensation polymers: polyesters and polyamides including proteins', 'condensation polymers')
facts(t, [('condensation polymerisation', 'polymerisation in which monomers join with the elimination of a small molecule such as water or hydrogen chloride'),
          ('polyester', 'a condensation polymer whose monomers are linked by ester (–COO–) groups, e.g. PET'),
          ('polyamide', 'a condensation polymer whose monomers are linked by amide (–CONH–) groups, e.g. nylon-6,6, Kevlar and proteins'),
          ('repeat unit', 'the smallest section of a polymer chain that, repeated, gives the whole polymer'),
          ('dioyl dichloride', 'a compound with two –COCl groups, used instead of a dicarboxylic acid to make polyesters and polyamides faster, with HCl eliminated'),
          ('protein', 'a natural polyamide made of α-amino acid residues joined by peptide bonds')])
mcqs(t, [('What small molecule is eliminated when hexane-1,6-diamine reacts with hexanedioic acid?', 'Water', 'Amide link and H₂O.', ['Hydrogen chloride', 'Ammonia', 'Carbon dioxide']),
         ('Which pair of monomers forms a polyester?', 'A diol and a dicarboxylic acid', 'Ester links form between –OH and –COOH.', ['A diamine and a dicarboxylic acid', 'Two alkenes', 'A diol and a diamine']),
         ('Which linkage is present in proteins?', '–CONH– (peptide/amide)', 'Proteins are polyamides.', ['–COO– (ester)', '–O– (ether)', '–C=C–']),
         ('Which polymer is a polyamide?', 'Kevlar', 'From benzene-1,4-diamine and benzene-1,4-dicarbonyl dichloride.', ['PET', 'Poly(ethene)', 'PLA'])])
mcqs(t, [('Why is Kevlar much stronger than nylon-6,6?', 'Its rigid, planar chains align and form many hydrogen bonds between chains', 'Benzene rings keep chains straight.', ['It has covalent cross-links', 'It is an addition polymer', 'Its chains are branched']),
         ('Why can a single monomer such as 6-aminohexanoic acid form a condensation polymer?', 'It has two different functional groups that can react with each other', '–NH₂ and –COOH on the same molecule.', ['It contains a C=C bond', 'It is very small', 'It forms a zwitterion'])], D=(2, 3), C='C2')
shorts(t, [('Name the two monomers used to make nylon-6,6.', 'Hexane-1,6-diamine and hexanedioic acid (or hexanedioyl dichloride).', 'each [1] [2]'),
           ('Give the repeat unit of PET.', '–OCH₂CH₂O–CO–C₆H₄–CO–', '[2]')])
explain(t, [('Explain why nylon-6,6 fibres are strong.', 'Long chains align closely and there are hydrogen bonds between the N–H of one chain and the C=O of a neighbouring chain, as well as van der Waals forces.', 'hydrogen bonds between chains [1]; N–H and C=O [1] [2]'),
            ('Explain the difference between addition and condensation polymerisation.', 'Addition: monomers with C=C join with no other product; the polymer has the same empirical formula as the monomer. Condensation: monomers with two functional groups join with loss of a small molecule (H₂O or HCl).', 'addition described [1]; condensation described [1] [2]'),
            ('Explain why a dioyl dichloride is sometimes used instead of a dicarboxylic acid to make a polyamide.', 'Acyl chlorides react much faster at room temperature and the reaction is not reversible, so a high molar mass polymer forms quickly (HCl eliminated).', '[2]')])
myths(t, [('Proteins are addition polymers of amino acids.', 'Proteins are condensation polymers: water is eliminated as each peptide bond forms.'),
          ('The repeat unit of a polyester formed from a diol and a dicarboxylic acid contains one monomer.', 'For an AA–BB polymer the repeat unit contains one residue of each monomer.'),
          ('Nylon-6,6 is held together only by van der Waals forces between chains.', 'There are also hydrogen bonds between N–H and C=O groups on neighbouring chains.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def cpoly_q(r, D):
    if r.random() < 0.6:
        a, af, Ma, b, bf, Mb, typ, nm, sm, Msm, ru, link = r.choice(CPOLY)
        Mru = Ma + Mb - 2 * Msm
        mono = f'{a} ({af}) and {b} ({bf})'
        rk = f'Mr(repeat) = {fx(Ma, 1)} + {fx(Mb, 1)} − 2 × {fx(Msm, 1)} = {fx(Mru, 1)}'
    else:
        a, af, Ma, typ, nm, ru, link = r.choice(SPOLY)
        sm, Msm = 'H₂O', 18.0
        Mru = Ma - 18.0
        mono = f'{a} ({af})'
        rk = f'Mr(repeat) = {fx(Ma, 1)} − 18.0 = {fx(Mru, 1)}'
    if D <= 2:
        return MQ(r, f'The condensation polymer {nm} is made from {mono}. What type of polymer is it, and which small molecule is eliminated?', f'{cap(typ)}; {sm}', [f'{cap(typ)}; {"HCl" if sm == "H₂O" else "H₂O"}', f'{"Polyamide" if "ester" in typ else "Polyester"}; {sm}', f'Addition polymer; no small molecule'], f'{cap(link)} links form with loss of {sm}.')
    st = f'{cap(nm)} is a condensation polymer made from {mono}. Give the structure of the repeat unit, state the type of polymer and name the small molecule eliminated.'
    ans = f'{ru}; {typ}; {sm}'
    key = f'repeat unit with {link} link [2]; type [1]; small molecule [1]'
    tot = 4
    if D >= 4:
        Mp = r.choice([18000, 25000, 32000, 40000, 55000])
        n_ = Mp / Mru
        st += f' A sample has an average Mr of {Mp:,}. Calculate the average number of repeat units per chain.'.replace(',', ' ')
        ans += f'; Mr(repeat) = {fx(Mru, 1)}; n ≈ {round(n_)}'
        key += f'; {rk} [1]; n = {Mp} ÷ {fx(Mru, 1)} ≈ {round(n_)} [1]'
        tot += 2
    return Q(st, ans, key + f' [{tot}]', 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def cpoly_case(r, D):
    a, af, Ma, b, bf, Mb, typ, nm, sm, Msm, ru, link = r.choice(CPOLY)
    Mru = Ma + Mb - 2 * Msm
    st = f'A textile manufacturer in {city(r)} produces {nm} from {a} and {b}.'
    parts = [P_('Write the structural formulae of the two monomers and the repeat unit of the polymer.', f'{af}; {bf}; repeat unit {ru}', 'monomers [1]; repeat unit [2] [3]'),
             P_('Name the type of linkage and the small molecule eliminated.', f'{link} linkage; {sm}', '[2]'),
             P_('Calculate the Mr of the repeat unit.', fx(Mru, 1), f'{fx(Ma, 1)} + {fx(Mb, 1)} − 2 × {fx(Msm, 1)} [1] = {fx(Mru, 1)} [1] [2]'),
             P_('Describe the intermolecular forces between the polymer chains.', ('Hydrogen bonds between N–H and C=O groups on adjacent chains, plus van der Waals forces.' if link == 'amide' else 'Permanent dipole–dipole forces between polar ester groups and van der Waals forces (no N–H for hydrogen bonding).'), '[2]'),
             P_('Explain why this polymer can be hydrolysed but poly(ethene) cannot.', f'The {link} links are polar and can be attacked by water/H⁺/OH⁻; poly(ethene) has only non-polar C–C and C–H bonds.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the formation, structure and properties of polyesters and polyamides, including proteins, with examples.', 'Condensation: elimination of H₂O or HCl; polyesters from diol + dicarboxylic acid / dioyl dichloride (PET) or hydroxy acid (PLA); polyamides from diamine + dicarboxylic acid / dioyl dichloride (nylon-6,6, Kevlar) or amino acids (proteins); repeat units; intermolecular forces: hydrogen bonding in polyamides, Kevlar rigidity; hydrolysis of ester/amide links.',
           'condensation principle [1]; polyester example with repeat unit [2]; polyamide example with repeat unit [2]; proteins [1]; properties [1] [7]')])
t10a = t

# ---------------------------------------------------------------------
APOLY = [('ethene', 'CH₂=CH₂', '–CH₂–CH₂–', 'poly(ethene)', 28.0), ('propene', 'CH₂=CHCH₃', '–CH₂–CH(CH₃)–', 'poly(propene)', 42.0),
         ('chloroethene', 'CH₂=CHCl', '–CH₂–CHCl–', 'poly(chloroethene), PVC', 62.5), ('phenylethene', 'CH₂=CHC₆H₅', '–CH₂–CH(C₆H₅)–', 'poly(phenylethene)', 104.0),
         ('tetrafluoroethene', 'CF₂=CF₂', '–CF₂–CF₂–', 'poly(tetrafluoroethene), PTFE', 100.0), ('propenenitrile', 'CH₂=CHCN', '–CH₂–CH(CN)–', 'poly(propenenitrile)', 53.0),
         ('methyl 2-methylpropenoate', 'CH₂=C(CH₃)COOCH₃', '–CH₂–C(CH₃)(COOCH₃)–', 'poly(methyl 2-methylpropenoate)', 100.0),
         ('but-2-ene', 'CH₃CH=CHCH₃', '–CH(CH₃)–CH(CH₃)–', 'poly(but-2-ene)', 56.0), ('1,1-dichloroethene', 'CH₂=CCl₂', '–CH₂–CCl₂–', 'poly(1,1-dichloroethene)', 97.0),
         ('propenamide', 'CH₂=CHCONH₂', '–CH₂–CH(CONH₂)–', 'poly(propenamide)', 71.0), ('ethenyl ethanoate', 'CH₂=CHOCOCH₃', '–CH₂–CH(OCOCH₃)–', 'poly(ethenyl ethanoate)', 86.0)]

t = T('Predicting monomers and repeat units for addition and condensation polymers', 'predicting monomers and repeat units')
facts(t, [('addition polymerisation', 'the joining of many monomers containing C=C bonds to form a single long chain with no other product'),
          ('monomer', 'a small molecule that can join with many others to form a polymer'),
          ('repeat unit', 'the smallest group of atoms that repeats along a polymer chain'),
          ('degree of polymerisation', 'the number of repeat units in a polymer chain, found by dividing the polymer Mr by the repeat-unit Mr'),
          ('backbone', 'the main chain of atoms in a polymer; all carbon in addition polymers, containing O or N in polyesters and polyamides')])
mcqs(t, [('What is the repeat unit of poly(propene)?', '–CH₂–CH(CH₃)–', 'Two backbone carbons; CH₃ side group.', ['–CH₂–CH₂–CH₂–', '–CH(CH₃)–CH(CH₃)–', '–CH₂=CH(CH₃)–']),
         ('Which monomer gives the repeat unit –CH₂–CHCl–?', 'Chloroethene', 'Remove brackets, restore C=C.', ['Chloroethane', '1,2-dichloroethene', 'Chloropropene']),
         ('A polymer chain contains –CO–NH– links in the backbone. What type of polymer is it?', 'A condensation polyamide', 'Amide links.', ['An addition polymer', 'A polyester', 'A polyalkene']),
         ('A polymer has repeat unit –O–CH₂CH₂–O–CO–C₆H₄–CO–. What are its monomers?', 'Ethane-1,2-diol and benzene-1,4-dicarboxylic acid', 'Split at the ester links and add H / OH.', ['Ethene and benzene', 'Ethanol and benzoic acid', 'Ethane-1,2-diamine and benzene-1,4-dicarboxylic acid'])])
mcqs(t, [('How can you tell from the repeat unit whether a polymer was made by addition?', 'The backbone contains only carbon atoms and no ester or amide links', 'Addition polymers form from C=C.', ['It contains oxygen atoms', 'It contains benzene rings', 'Its Mr is very large']),
         ('Why does the repeat unit of a condensation polymer have a smaller Mr than the sum of its monomers?', 'A small molecule such as H₂O or HCl is lost when each link forms', 'Condensation.', ['Some monomers do not react', 'Atoms are lost as gases on heating', 'The monomers are ionised'])], D=(2, 3), C='C2')
shorts(t, [('Give the structure of the repeat unit of poly(tetrafluoroethene).', '–CF₂–CF₂–', '[1]'),
           ('Identify the monomer of an addition polymer with repeat unit –CH₂–CH(CN)–.', 'Propenenitrile, CH₂=CHCN', '[1]')])
explain(t, [('Explain how to deduce the monomer from the repeat unit of an addition polymer.', 'Take the two backbone carbon atoms, remove the extension bonds and put a C=C double bond between them, keeping the side groups.', '[2]'),
            ('Explain how to deduce the monomers of a condensation polymer from a section of the chain.', 'Identify the ester or amide links; break each link at the C–O or C–N bond; add –OH to the C=O end and –H to the O or N end (or –Cl to the C=O end for a dioyl dichloride).', 'identify links [1]; break and add H/OH [1] [2]')])
myths(t, [('The repeat unit of poly(ethene) is –CH₂=CH₂–.', 'The C=C bond becomes a single bond in the polymer; the repeat unit is –CH₂–CH₂–.'),
          ('Addition polymers form with loss of water.', 'Addition polymerisation produces only the polymer; no small molecule is eliminated.'),
          ('Any molecule with two functional groups forms an addition polymer.', 'Molecules with two reactive groups (e.g. –OH and –COOH) form condensation polymers; addition polymers need C=C.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def apoly_q(r, D):
    nm, mf, ru, pn, M = r.choice(APOLY)
    way = r.choice(['m2r', 'r2m'])
    if D <= 2:
        if way == 'm2r':
            return MQ(r, f'What is the repeat unit of the addition polymer formed from {nm}, {mf}?', ru, [x[2] for x in r.sample([a for a in APOLY if a[0] != nm], 3)], f'Open the C=C: {ru}.')
        return MQ(r, f'An addition polymer has the repeat unit {ru}. What is its monomer?', f'{nm}, {mf}', [f'{x[0]}, {x[1]}' for x in r.sample([a for a in APOLY if a[0] != nm], 3)], f'Restore the C=C: {mf}.')
    if way == 'm2r':
        st = f'Give the structure of the repeat unit of the polymer formed from {nm}, {mf}, and name the polymer.'
        ans = f'{ru}; {pn}'
    else:
        st = f'An addition polymer has the repeat unit {ru}. Give the name and structural formula of the monomer.'
        ans = f'{nm}, {mf}'
    key = 'correct structure [1]; name [1]'
    tot = 2
    if D >= 4:
        Mp = r.choice([84000, 120000, 250000, 500000]) if M < 60 else r.choice([150000, 200000, 300000])
        nn = str(int(float(f'{Mp / M:.3g}')))
        st += f' A sample of the polymer has an average Mr of {Mp:,}. Calculate the average number of monomer units per chain.'.replace(',', ' ')
        ans += f'; n = {Mp} ÷ {M:.1f} ≈ {nn}'
        key += f'; Mr(monomer) = {M:.1f} [1]; n ≈ {nn} [1]'
        tot += 2
    return Q(st, ans, key + f' [{tot}]', 'numerical')


@t.add('C3', (2, 3, 4, 5), 'short')
def section_q(r, D):
    if r.random() < 0.6:
        a, af, Ma, b, bf, Mb, typ, nm, sm, Msm, ru, link = r.choice(CPOLY)
        sec = ru.strip('–') + '–' + ru.strip('–')
        mono = f'{a}, {af}, and {b}, {bf}'
    else:
        a, af, Ma, typ, nm, ru, link = r.choice(SPOLY)
        sec = (ru.strip('–') + '–') * 2 + ru.strip('–')
        mono = f'{a}, {af}'
        sm = 'H₂O'
    if D <= 2:
        return MQ(r, f'A section of a polymer chain is –{sec}–. What type of polymer is it?', f'{cap(typ.split(" (")[0])} (condensation)', [f'{"Polyamide" if "ester" in typ else "Polyester"} (condensation)', 'Addition polymer', 'Poly(alkene)'], f'Contains {link} links.')
    st = f'A section of a polymer chain is –{sec}–. Identify the type of linkage and deduce the structure(s) of the monomer(s).'
    ans = f'{link} linkage ({typ}); monomer(s): {mono}'
    key = 'linkage identified [1]; monomer structure(s) [2]'
    tot = 3
    if D >= 4:
        st += ' State the type of polymerisation and suggest one property linked to the linkage.'
        ans += f'; condensation polymerisation; {"hydrogen bonding between chains / can be hydrolysed" if link == "amide" else "can be hydrolysed by acid or alkali (biodegradable)"}'
        key += '; condensation [1]; property [1]'
        tot += 2
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def poly_id_case(r, D):
    ap = r.choice(APOLY)
    cp = r.choice(CPOLY)
    st = f'{who(r)} is given samples of two polymers, X and Y. X has the repeat unit {ap[2]}. Y has the repeat unit {cp[10]}.'
    parts = [P_('State, with a reason, which polymer was made by addition polymerisation.', 'X: its backbone contains only carbon atoms (formed from C=C monomers), with no ester or amide links.', '[2]'),
             P_('Give the structural formula of the monomer of X.', ap[1], '[1]'),
             P_('Identify the linkage in Y and give the structures of its monomers.', f'{cp[11]} linkage; {cp[1]} and {cp[4]}', 'linkage [1]; monomers [2] [3]'),
             P_('Calculate the Mr of the repeat unit of Y.', fx(cp[2] + cp[5] - 2 * cp[9], 1), f'{fx(cp[2], 1)} + {fx(cp[5], 1)} − 2 × {fx(cp[9], 1)} = {fx(cp[2] + cp[5] - 2 * cp[9], 1)} [2]'),
             P_('Suggest, with a reason, which polymer is more likely to biodegrade.', f'Y: the polar {cp[11]} links can be hydrolysed (by enzymes, acid or alkali); X has non-polar C–C and C–H bonds only.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how the repeat unit of a polymer is deduced from its monomer(s), and how the monomers are deduced from a section of polymer chain, for both addition and condensation polymers.', 'Addition: open C=C, two-carbon repeat unit with side groups, reverse by restoring C=C; examples poly(propene), PVC; condensation: identify functional groups (diol/diacid, diamine/diacid or dioyl dichloride, hydroxy acids, amino acids), form ester/amide links with loss of H₂O/HCl, repeat unit contains one of each AA/BB monomer; reverse by breaking links and adding H/OH; degree of polymerisation from Mr.',
           'addition forward and reverse [2]; condensation forward [2]; condensation reverse [2]; Mr / degree of polymerisation [1] [7]')])
t10b = t

# ---------------------------------------------------------------------
DEG = [('poly(ethene)', 'non-biodegradable', 'only non-polar C–C and C–H bonds; no groups that can be hydrolysed or attacked by enzymes'),
       ('poly(propene)', 'non-biodegradable', 'saturated hydrocarbon chain with strong non-polar C–C and C–H bonds'),
       ('PVC', 'non-biodegradable', 'strong C–C and C–Cl bonds; no hydrolysable links'),
       ('PLA (poly(lactic acid))', 'biodegradable', 'ester links are hydrolysed by water and enzymes in compost'),
       ('PHB (poly(3-hydroxybutanoate))', 'biodegradable', 'ester links are hydrolysed by bacterial enzymes'),
       ('nylon-6,6', 'slowly hydrolysable', 'amide links can be hydrolysed by acid or alkali, but only slowly in the environment'),
       ('PET', 'slowly hydrolysable', 'ester links can be hydrolysed by acid or alkali, but slowly in the environment'),
       ('a poly(ethene) containing C=O groups', 'photodegradable', 'C=O groups absorb UV radiation, breaking nearby bonds in the chain')]

t = T('Degradable polymers: biodegradability and photodegradability', 'degradable polymers')
facts(t, [('biodegradable polymer', 'a polymer that can be broken down by microorganisms in the environment into small molecules such as CO₂ and water'),
          ('photodegradable polymer', 'a polymer that breaks down when it absorbs ultraviolet light, usually because it contains C=O groups'),
          ('hydrolysis of a polymer', 'the breaking of ester or amide links in a condensation polymer by reaction with water, catalysed by acid, alkali or enzymes'),
          ('non-biodegradable', 'describes a polymer, such as poly(ethene), that is not broken down by microorganisms because it has no reactive polar groups'),
          ('bioplastic', 'a plastic made from renewable biological sources, such as PLA from corn starch')])
mcqs(t, [('Why is poly(ethene) non-biodegradable?', 'It has only non-polar C–C and C–H bonds that are not attacked by enzymes or water', 'No hydrolysable links.', ['It contains ester links', 'It absorbs UV light', 'It is a condensation polymer']),
         ('What makes a polymer photodegradable?', 'C=O groups that absorb UV light and cause nearby bonds to break', 'Carbonyl groups absorb UV.', ['C–H bonds', 'Hydrogen bonds between chains', 'A high Mr']),
         ('Which polymer is biodegradable?', 'Poly(lactic acid)', 'Polyester; hydrolysed in compost.', ['Poly(ethene)', 'PVC', 'Poly(propene)'])])
mcqs(t, [('Why do photodegradable plastics often break down slowly in landfill?', 'Buried plastic receives little or no UV light', 'Needs light.', ['There is too much oxygen', 'Landfill is too hot', 'Microorganisms block the UV']),
         ('A disadvantage of burning PVC waste is that', 'toxic HCl and possibly dioxins are produced', 'Contains chlorine.', ['it produces no energy', 'it forms poly(ethene)', 'it is biodegradable'])], D=(2, 3), C='C2')
shorts(t, [('State one advantage and one disadvantage of using biodegradable polymers.', 'Advantage: break down in the environment, reducing persistent waste / often from renewable sources. Disadvantage: may need specific composting conditions; can be weaker / more expensive; may contaminate recycling.', 'advantage [1]; disadvantage [1] [2]')])
explain(t, [('Explain why polyesters and polyamides can be hydrolysed but poly(alkenes) cannot.', 'Ester and amide links are polar, with δ+ carbonyl carbons that are attacked by water, H⁺, OH⁻ or enzymes; poly(alkenes) have only strong non-polar C–C and C–H bonds.', 'polar links attacked [1]; poly(alkenes) non-polar [1] [2]'),
            ('Explain why PLA is described as both renewable and biodegradable.', 'Its monomer, lactic acid, is made by fermenting plant sugars (renewable); its ester links are hydrolysed and the products broken down by microorganisms (biodegradable).', '[2]')])
myths(t, [('All polymers break down eventually in landfill within a few years.', 'Poly(alkenes) persist for hundreds of years because they have no hydrolysable links and receive little light or oxygen.'),
          ('Photodegradable polymers break down equally well when buried.', 'They need UV light, so they degrade slowly when buried in landfill.'),
          ('Biodegradable polymers are addition polymers like poly(ethene).', 'Most biodegradable polymers are condensation polymers (polyesters, polyamides) with hydrolysable links.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def deg_q(r, D):
    p, cls, why = r.choice(DEG)
    if D <= 2:
        return MQ(r, f'How would {p} best be described?', cap(cls), [cap(c) for c in ('biodegradable', 'non-biodegradable', 'photodegradable', 'slowly hydrolysable') if c != cls], f'{cap(cls)}: {why}.')
    return Q(f'Explain whether {p} is likely to break down in the environment, referring to its structure.', f'{cap(cls)}: {why}.', 'classification [1]; structural reason [1] [2]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def deg_data(r, D):
    p = r.choice(['PLA', 'PHB', 'a starch-based polymer', 'a poly(butylene succinate) film'])
    m0 = round(r.uniform(2.0, 5.0), 2)
    k = r.uniform(0.04, 0.15)
    wk = [0, 2, 4, 6, 8]
    ms = [round(m0 * math.exp(-k * w), 2) for w in wk]
    data = ', '.join(f'week {w}: {mm:.2f} g' for w, mm in zip(wk, ms))
    loss = (ms[0] - ms[-1]) / ms[0] * 100
    rate = (ms[0] - ms[-1]) / 8
    st = f'Strips of {p} were buried in compost at 40 °C and weighed every two weeks: {data}. Calculate the percentage loss in mass over 8 weeks and the mean rate of mass loss in g per week.'
    key = f'loss = {ms[0] - ms[-1]:.2f} g [1]; % = {g3(loss)}% [1]; rate = {ms[0] - ms[-1]:.2f} ÷ 8 = {g3(rate)} g per week [1] [3]'
    ans = f'{g3(loss)}%; {g3(rate)} g per week'
    if D >= 4:
        st += ' Suggest why the rate of mass loss decreases over time, and state one variable that should be controlled.'
        ans += '; less polymer surface remains / fewer accessible ester links as the strip shrinks; control temperature, moisture, strip size or compost type'
        key = key.replace(' [3]', '') + '; reason [1]; controlled variable [1] [5]'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def deg_case(r, D):
    st = f'A city council in {city(r)} is choosing between bags made of poly(ethene), photodegradable poly(ethene) containing C=O groups, and PLA.'
    parts = [P_('Explain why ordinary poly(ethene) bags persist in the environment.', 'Only strong, non-polar C–C and C–H bonds; not attacked by water, enzymes or UV to any significant extent.', '[2]'),
             P_('Explain how the photodegradable bag breaks down and why this may not work in landfill.', 'C=O groups absorb UV, causing bond fission in the chain; buried bags receive no UV light.', 'mechanism [1]; landfill limitation [1] [2]'),
             P_('Explain how PLA biodegrades, naming the type of reaction involved.', 'Hydrolysis of the ester links (by water/enzymes) to lactic acid, which microorganisms convert to CO₂ and H₂O.', 'hydrolysis of ester links [1]; products broken down [1] [2]'),
             P_('Evaluate the three options, giving one further environmental factor to consider.', 'PLA is renewable and compostable but needs industrial composting; photodegradable bags can fragment into microplastics; poly(ethene) is cheap and recyclable but persists; consider energy/feedstock source, recycling infrastructure, litter, microplastics, cost.', 'balanced comparison [2]; further factor [1] [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Discuss the problems of disposing of polymers and evaluate the use of biodegradable and photodegradable polymers.', 'Poly(alkenes) are non-biodegradable (non-polar, strong bonds) – landfill persistence, litter, microplastics; burning releases CO₂ and toxic HCl (PVC); recycling issues; biodegradable condensation polymers (PLA, PHB) hydrolysed at ester links, renewable feedstocks but need composting; photodegradable polymers with C=O absorb UV, need light, fragment; evaluation and conclusion.',
           'disposal problems [2]; biodegradable chemistry [2]; photodegradable chemistry [1]; evaluation and conclusion [2] [7]')])
t10c = t

CHAPTERS[10] = [t10a, t10b, t10c]


# ===================================================================== 11 Analytical chemistry
# name, formula, M (m/z of M⁺ with ¹²C, ¹H, ¹⁶O, ³⁵Cl, ⁷⁹Br), nC, class, ¹³C [(δ, assignment)], ¹H [(δ, nH, splitting, group)], halogen
CMPD = [
    ('ethanol', 'CH₃CH₂OH', 46, 2, 'alcohol', [(18, 'CH₃'), (58, 'CH₂–O')], [(1.2, 3, 'triplet', 'CH₃'), (3.7, 2, 'quartet', 'CH₂–O'), (2.6, 1, 'singlet', 'O–H')], None),
    ('propan-1-ol', 'CH₃CH₂CH₂OH', 60, 3, 'alcohol', [(10, 'CH₃'), (26, 'CH₂'), (64, 'CH₂–O')], [(0.9, 3, 'triplet', 'CH₃'), (1.6, 2, 'sextet', 'CH₂'), (3.6, 2, 'triplet', 'CH₂–O'), (2.3, 1, 'singlet', 'O–H')], None),
    ('propan-2-ol', '(CH₃)₂CHOH', 60, 3, 'alcohol', [(25, 'CH₃ (×2)'), (64, 'CH–O')], [(1.2, 6, 'doublet', '(CH₃)₂'), (4.0, 1, 'septet', 'CH–O'), (2.2, 1, 'singlet', 'O–H')], None),
    ('ethanoic acid', 'CH₃COOH', 60, 2, 'acid', [(21, 'CH₃'), (178, 'COOH')], [(2.1, 3, 'singlet', 'CH₃'), (11.5, 1, 'singlet', 'COOH')], None),
    ('propanoic acid', 'CH₃CH₂COOH', 74, 3, 'acid', [(9, 'CH₃'), (28, 'CH₂'), (181, 'COOH')], [(1.1, 3, 'triplet', 'CH₃'), (2.4, 2, 'quartet', 'CH₂'), (11.7, 1, 'singlet', 'COOH')], None),
    ('ethanal', 'CH₃CHO', 44, 2, 'aldehyde', [(31, 'CH₃'), (200, 'CHO')], [(2.2, 3, 'doublet', 'CH₃'), (9.8, 1, 'quartet', 'CHO')], None),
    ('propanone', 'CH₃COCH₃', 58, 3, 'ketone', [(30, 'CH₃ (×2)'), (206, 'C=O')], [(2.2, 6, 'singlet', 'CH₃ (×2)')], None),
    ('butanone', 'CH₃COCH₂CH₃', 72, 4, 'ketone', [(8, 'CH₃ of ethyl'), (29, 'CH₃CO'), (37, 'CH₂'), (209, 'C=O')], [(1.1, 3, 'triplet', 'CH₃ of ethyl'), (2.1, 3, 'singlet', 'CH₃CO'), (2.5, 2, 'quartet', 'CH₂')], None),
    ('ethyl ethanoate', 'CH₃COOCH₂CH₃', 88, 4, 'ester', [(14, 'CH₃ of ethyl'), (21, 'CH₃CO'), (60, 'O–CH₂'), (171, 'COO')], [(1.3, 3, 'triplet', 'CH₃ of ethyl'), (2.0, 3, 'singlet', 'CH₃CO'), (4.1, 2, 'quartet', 'O–CH₂')], None),
    ('methyl propanoate', 'CH₃CH₂COOCH₃', 88, 4, 'ester', [(9, 'CH₃'), (27, 'CH₂'), (51, 'O–CH₃'), (175, 'COO')], [(1.1, 3, 'triplet', 'CH₃'), (2.3, 2, 'quartet', 'CH₂CO'), (3.7, 3, 'singlet', 'O–CH₃')], None),
    ('methyl ethanoate', 'CH₃COOCH₃', 74, 3, 'ester', [(21, 'CH₃CO'), (52, 'O–CH₃'), (171, 'COO')], [(2.0, 3, 'singlet', 'CH₃CO'), (3.7, 3, 'singlet', 'O–CH₃')], None),
    ('ethyl methanoate', 'HCOOCH₂CH₃', 74, 3, 'ester', [(14, 'CH₃'), (60, 'O–CH₂'), (161, 'HCOO')], [(1.3, 3, 'triplet', 'CH₃'), (4.2, 2, 'quartet', 'O–CH₂'), (8.1, 1, 'singlet', 'HCOO')], None),
    ('1-bromopropane', 'CH₃CH₂CH₂Br', 122, 3, 'halogenoalkane', [(13, 'CH₃'), (26, 'CH₂'), (36, 'CH₂Br')], [(1.0, 3, 'triplet', 'CH₃'), (1.9, 2, 'sextet', 'CH₂'), (3.4, 2, 'triplet', 'CH₂Br')], 'Br'),
    ('2-bromopropane', '(CH₃)₂CHBr', 122, 3, 'halogenoalkane', [(28, 'CH₃ (×2)'), (45, 'CHBr')], [(1.7, 6, 'doublet', '(CH₃)₂'), (4.2, 1, 'septet', 'CHBr')], 'Br'),
    ('chloroethane', 'CH₃CH₂Cl', 64, 2, 'halogenoalkane', [(19, 'CH₃'), (40, 'CH₂Cl')], [(1.5, 3, 'triplet', 'CH₃'), (3.6, 2, 'quartet', 'CH₂Cl')], 'Cl'),
    ('2-chloropropane', '(CH₃)₂CHCl', 78, 3, 'halogenoalkane', [(27, 'CH₃ (×2)'), (54, 'CHCl')], [(1.5, 6, 'doublet', '(CH₃)₂'), (4.1, 1, 'septet', 'CHCl')], 'Cl'),
    ('2-methylpropan-2-ol', '(CH₃)₃COH', 74, 4, 'alcohol', [(31, 'CH₃ (×3)'), (69, 'C–O')], [(1.3, 9, 'singlet', '(CH₃)₃'), (2.0, 1, 'singlet', 'O–H')], None),
    ('ethylamine', 'CH₃CH₂NH₂', 45, 2, 'amine', [(19, 'CH₃'), (37, 'CH₂–N')], [(1.1, 3, 'triplet', 'CH₃'), (2.7, 2, 'quartet', 'CH₂–N'), (1.3, 2, 'singlet', 'N–H₂')], None),
    ('phenylethanone', 'C₆H₅COCH₃', 120, 8, 'ketone', [(27, 'CH₃'), (128, 'aryl C'), (129, 'aryl C'), (133, 'aryl C'), (137, 'aryl C'), (198, 'C=O')], [(2.6, 3, 'singlet', 'CH₃CO'), (7.5, 5, 'multiplet', 'aryl H')], None),
    ('methylbenzene', 'C₆H₅CH₃', 92, 7, 'arene', [(21, 'CH₃'), (125, 'aryl C'), (128, 'aryl C'), (129, 'aryl C'), (138, 'aryl C')], [(2.3, 3, 'singlet', 'CH₃'), (7.2, 5, 'multiplet', 'aryl H')], None),
    ('pentan-3-one', 'CH₃CH₂COCH₂CH₃', 86, 5, 'ketone', [(8, 'CH₃ (×2)'), (35, 'CH₂ (×2)'), (211, 'C=O')], [(1.0, 6, 'triplet', 'CH₃ (×2)'), (2.4, 4, 'quartet', 'CH₂ (×2)')], None),
    ('ethyl propanoate', 'CH₃CH₂COOCH₂CH₃', 102, 5, 'ester', [(9, 'CH₃CH₂CO'), (14, 'OCH₂CH₃'), (28, 'CH₂CO'), (60, 'O–CH₂'), (174, 'COO')], [(1.1, 3, 'triplet', 'CH₃CH₂CO'), (1.3, 3, 'triplet', 'OCH₂CH₃'), (2.3, 2, 'quartet', 'CH₂CO'), (4.1, 2, 'quartet', 'O–CH₂')], None),
    ('2-methylpropanoic acid', '(CH₃)₂CHCOOH', 88, 4, 'acid', [(19, 'CH₃ (×2)'), (34, 'CH'), (184, 'COOH')], [(1.2, 6, 'doublet', '(CH₃)₂'), (2.6, 1, 'septet', 'CH'), (11.9, 1, 'singlet', 'COOH')], None),
    ('benzene', 'C₆H₆', 78, 6, 'arene', [(128, 'aryl C')], [(7.3, 6, 'singlet', 'aryl H')], None)]
IR = {'alcohol': 'broad O–H absorption at 3200–3600 cm⁻¹; C–O at 1040–1300 cm⁻¹', 'acid': 'very broad O–H absorption at 2500–3000 cm⁻¹; C=O at 1680–1730 cm⁻¹',
      'aldehyde': 'C=O absorption at 1720–1740 cm⁻¹; no O–H', 'ketone': 'C=O absorption at 1680–1720 cm⁻¹; no O–H', 'ester': 'C=O absorption at 1735–1750 cm⁻¹; C–O at 1050–1300 cm⁻¹; no O–H',
      'halogenoalkane': 'C–H absorptions only above 1500 cm⁻¹; C–halogen absorption below 800 cm⁻¹', 'amine': 'N–H absorption at 3300–3500 cm⁻¹', 'arene': 'aromatic C=C absorptions at 1450–1650 cm⁻¹; C–H above 3000 cm⁻¹'}
OH_CLASS = ('alcohol', 'acid', 'amine')


def h_peaks(c):
    return len(c[6])


def h_ratio(c):
    return ' : '.join(str(h[1]) for h in c[6])


def h_desc(c):
    return '; '.join(f'δ {format(h[0], '.1f')}, {h[1]}H, {h[2]} ({h[3]})' for h in c[6])


t = T('Thin-layer and gas–liquid chromatography: Rf and retention times', 'thin-layer and gas–liquid chromatography')
facts(t, [('Rf value', 'the distance moved by a spot divided by the distance moved by the solvent front, measured from the baseline'),
          ('retention time', 'in gas–liquid chromatography, the time between injection of the sample and the emergence of a component from the column'),
          ('stationary phase', 'the phase that does not move in chromatography, e.g. silica on a TLC plate or a non-volatile liquid on a solid support in GLC'),
          ('mobile phase', 'the phase that moves through the stationary phase, e.g. the solvent in TLC or the inert carrier gas in GLC'),
          ('locating agent', 'a reagent, such as ninhydrin for amino acids, or UV light, used to make colourless spots visible'),
          ('partition', 'the distribution of a solute between two phases, the basis of separation in gas–liquid chromatography')])
mcqs(t, [('What is the mobile phase in gas–liquid chromatography?', 'An inert carrier gas such as nitrogen or helium', 'The gas carries the vaporised sample.', ['A non-volatile liquid', 'Silica gel', 'An organic solvent']),
         ('What is the stationary phase in thin-layer chromatography?', 'A thin layer of silica or alumina on a plate', 'Solid adsorbent.', ['The solvent', 'An inert gas', 'Filter paper soaked in water']),
         ('In GLC, what does the area under each peak indicate?', 'The relative amount of that component', 'Peak area ∝ amount.', ['The boiling point of the component', 'The Mr of the component', 'The retention time']),
         ('Why is a pencil used to draw the baseline on a TLC plate?', 'Graphite does not dissolve in the solvent or move up the plate', 'Ink would separate.', ['It is easier to see in UV light', 'It reacts with the spots', 'It makes the solvent move faster'])])
mcqs(t, [('In TLC on silica, a more polar compound usually has', 'a smaller Rf value', 'It is adsorbed more strongly on polar silica.', ['a larger Rf value', 'the same Rf value as a non-polar compound', 'an Rf value greater than 1']),
         ('In GLC, why does a compound with a higher boiling point usually have a longer retention time?', 'It spends more time dissolved in the liquid stationary phase', 'Less volatile; partition favours the liquid.', ['It moves faster with the carrier gas', 'It is adsorbed onto the column walls', 'It is more polar than the carrier gas'])], D=(2, 3), C='C2')
shorts(t, [('State the formula used to calculate an Rf value.', 'Rf = distance moved by spot ÷ distance moved by solvent front', '[1]'),
           ('State two factors that affect the retention time of a compound in GLC.', 'Any two: boiling point/volatility; solubility in (interaction with) the stationary phase; column temperature; carrier gas flow rate; column length.', '[2]')])
explain(t, [('Explain how separation occurs in thin-layer chromatography.', 'Components are partitioned between the polar stationary phase (adsorbed on silica) and the moving solvent; components more strongly adsorbed move more slowly, so they travel different distances.', 'adsorption to stationary phase [1]; solubility in mobile phase [1]; different distances [1] [3]'),
            ('Explain how separation occurs in gas–liquid chromatography.', 'The vaporised sample is carried by an inert gas through a column containing a non-volatile liquid on a solid support; components partition between gas and liquid; those more soluble in the liquid or less volatile take longer to emerge.', 'partition between gas and liquid [1]; solubility/volatility [1]; different retention times [1] [3]'),
            ('Explain why a locating agent may be needed in TLC.', 'Many compounds (e.g. amino acids) are colourless; spraying with a reagent such as ninhydrin or viewing under UV makes the spots visible.', '[2]')])
myths(t, [('An Rf value can be greater than 1 if the spot moves fast.', 'The spot cannot move further than the solvent front, so Rf is always between 0 and 1.'),
          ('In GLC the stationary phase is a gas.', 'The stationary phase is a non-volatile liquid; the mobile phase is the carrier gas.'),
          ('The tallest peak in a gas chromatogram is always the main component.', 'The amount is shown by the peak area, not just its height.')])

RF_SETS = [('amino acids on a silica plate with a butan-1-ol/ethanoic acid/water solvent', [('lysine', 0.14), ('aspartic acid', 0.24), ('alanine', 0.38), ('tyrosine', 0.45), ('valine', 0.60), ('leucine', 0.73)]),
           ('analgesics on a silica plate with ethyl ethanoate', [('caffeine', 0.19), ('paracetamol', 0.36), ('aspirin', 0.55), ('ibuprofen', 0.78)]),
           ('plant pigments on a silica plate with a hexane/propanone solvent', [('chlorophyll b', 0.42), ('chlorophyll a', 0.56), ('xanthophyll', 0.71), ('carotene', 0.95)]),
           ('food dyes on a silica plate with an aqueous ethanol solvent', [('dye E', 0.15), ('dye B', 0.31), ('dye D', 0.50), ('dye A', 0.66), ('dye C', 0.84)])]
GLC_SETS = [('a mixture of alcohols', ['methanol', 'ethanol', 'propan-1-ol', 'butan-1-ol']), ('a mixture of esters', ['methyl ethanoate', 'ethyl ethanoate', 'propyl ethanoate', 'butyl ethanoate']),
            ('a sample of petrol', ['pentane', 'hexane', 'heptane', 'octane']), ('a solvent mixture', ['propanone', 'ethanol', 'methylbenzene', 'water'])]


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def rf_q(r, D):
    desc, refs = r.choice(RF_SETS)
    front = r.choice([6.0, 7.0, 7.5, 8.0, 8.5, 9.0])
    picks = r.sample(refs, 2 if D >= 4 else 1)
    dist = [round(rf * front, 1) for _, rf in picks]
    rfs = [d / front for d in dist]
    ref_txt = ', '.join(f'{n} {fx(v, 2)}' for n, v in refs)
    if D <= 2:
        return NQ(r, f'In a thin-layer chromatogram of {desc}, the solvent front moved {fx(front, 1)} cm and a spot moved {fx(dist[0], 1)} cm from the baseline. What is the Rf value of the spot?', rfs[0], [front / dist[0], 1 - rfs[0], dist[0] / (front + 1), rfs[0] / 2], '', f'Rf = {fx(dist[0], 1)} ÷ {fx(front, 1)} = {fx(rfs[0], 2)}', f=lambda v: fx(v, 2))
    st = (f'An unknown mixture was analysed by thin-layer chromatography of {desc}. The solvent front moved {fx(front, 1)} cm. ' + cap(' and '.join(f'a spot moved {fx(d, 1)} cm' for d in dist)) +
          f'. Reference Rf values in this system: {ref_txt}. Calculate the Rf value of {"each spot" if len(dist) > 1 else "the spot"} and identify the component{"s" if len(dist) > 1 else ""}.')
    ans = '; '.join(f'Rf = {fx(v, 2)}: {n}' for v, (n, _) in zip(rfs, picks))
    key = '; '.join(f'Rf = {fx(d, 1)} ÷ {fx(front, 1)} = {fx(v, 2)} [1]; {n} [1]' for d, v, (n, _) in zip(dist, rfs, picks))
    tot = 2 * len(dist)
    if D >= 5:
        st += ' Suggest how the identification could be confirmed.'
        ans += '; run pure reference samples alongside the mixture on the same plate (co-spotting), or use a different solvent'
        key += '; co-spot with standards / second solvent [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'numerical')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def glc_q(r, D):
    desc, comps = r.choice(GLC_SETS)
    k = 3 if D <= 3 else 4
    names = comps[:k]
    areas = [r.choice([2.4, 3.1, 4.5, 5.6, 6.2, 7.8, 8.4, 9.0, 12.5]) for _ in names]
    tot = sum(areas)
    pcs = [a / tot * 100 for a in areas]
    i = r.randrange(k)
    ar = ', '.join(f'{n} {fx(a, 1)} cm²' for n, a in zip(names, areas))
    if D <= 2:
        return NQ(r, f'A gas chromatogram of {desc} shows peaks with areas: {ar}. What is the percentage of {names[i]} in the mixture?', pcs[i], [areas[i], 100 / k, pcs[i] * 2, 100 - pcs[i]], '%', f'{fx(areas[i], 1)} ÷ {fx(tot, 1)} × 100 = {g3(pcs[i])}%', f=lambda v: g3(v))
    st = f'A gas chromatogram of {desc} shows peaks with areas: {ar}. Calculate the percentage composition of the mixture, assuming that the detector responds equally to each component.'
    ans = '; '.join(f'{n} {g3(p)}%' for n, p in zip(names, pcs))
    key = f'total area {fx(tot, 1)} [1]; each % = area ÷ total × 100 [1]; values correct [1]'
    t_ = 3
    if D >= 4:
        st += ' Predict, with a reason, which component has the shortest retention time.'
        ans += f'; {names[0]} (lowest boiling point / most volatile, least soluble in the stationary phase)' if desc != 'a solvent mixture' else '; propanone (most volatile / lowest boiling point)'
        key += '; shortest retention time with reason [1]'
        t_ += 1
    return Q(st, ans, key + f' [{t_}]', 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def chrom_case(r, D):
    desc, refs = r.choice(RF_SETS[:2])
    front = 8.0
    a, b = r.sample(refs, 2)
    st = f'{who(r)} in {lab(r)} tests a sample suspected to contain {a[0]} and {b[0]} using TLC ({desc}). The solvent front moved {fx(front, 1)} cm; spots moved {fx(a[1] * front, 1)} cm and {fx(b[1] * front, 1)} cm.'
    parts = [P_('Calculate the Rf values of the two spots.', f'{fx(a[1], 2)} and {fx(b[1], 2)}', 'each [1] [2]'),
             P_('Explain why the two components travel different distances.', 'They have different affinities: the more polar component is adsorbed more strongly onto the polar silica and moves more slowly; the other is more soluble in the solvent.', '[2]'),
             P_('Describe how the spots could be made visible if the components are colourless.', 'Use UV light on a plate with a fluorescent indicator, or spray with a locating agent such as ninhydrin (for amino acids) / iodine vapour.', '[1]'),
             P_('Explain why gas–liquid chromatography would not be suitable for analysing these compounds directly.', 'They have low volatility (strong intermolecular forces / ionic zwitterions or many polar groups) and may decompose before they vaporise; GLC needs volatile, thermally stable samples.', '[2]'),
             P_('Predict how the Rf values would change if a more polar solvent were used, and explain why.', 'They would generally increase: the components would be more soluble in the polar mobile phase and compete better with adsorption on the silica.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Compare thin-layer chromatography and gas–liquid chromatography, explaining how each separates components and how the results are interpreted.', 'TLC: silica/alumina stationary phase, solvent mobile phase, separation by adsorption/solubility; Rf = spot ÷ front, compare with standards, locating agents; GLC: liquid on solid support stationary phase, inert carrier gas mobile, separation by partition (volatility, solubility in stationary phase); retention times for identification; peak areas for relative amounts; limitations.',
           'TLC phases and principle [2]; Rf use [1]; GLC phases and principle [2]; retention time and peak area [1]; limitation [1] [7]')])
t11a = t

# ---------------------------------------------------------------------
C13R = [(5, 40, 'C–C (alkyl)'), (10, 70, 'C–Cl or C–Br'), (20, 50, 'C next to C=O'), (25, 60, 'C–N'), (50, 90, 'C–O'), (110, 160, 'aryl / alkene C'), (160, 185, 'C=O of acid or ester'), (190, 220, 'C=O of aldehyde or ketone')]

t = T('Carbon-13 NMR spectroscopy: number and environment of carbon atoms', 'carbon-13 nmr spectroscopy')
facts(t, [('chemical shift', 'δ: the position of an NMR absorption relative to the reference compound TMS, in ppm'),
          ('carbon environment', 'a set of carbon atoms in equivalent positions in a molecule, which give one peak in a ¹³C NMR spectrum'),
          ('TMS', 'tetramethylsilane, Si(CH₃)₄, the reference compound set at δ = 0; inert, volatile and gives a single strong peak'),
          ('deshielding', 'the reduction in electron density around a nucleus by nearby electronegative atoms, which increases its chemical shift'),
          ('¹³C NMR spectrum', 'a spectrum showing one line for each different carbon environment in a molecule')])
mcqs(t, [('How many peaks are in the ¹³C NMR spectrum of propan-2-ol?', '2', 'Two CH₃ carbons are equivalent.', ['3', '1', '4']),
         ('In which range does the carbon of a ketone C=O group absorb?', '190–220 ppm', 'Strongly deshielded.', ['5–40 ppm', '50–90 ppm', '110–160 ppm']),
         ('Why is TMS used as a reference in NMR?', 'It gives a single peak, is inert and volatile', 'All 12 H and 4 C are equivalent.', ['It absorbs at a very high δ', 'It reacts with the sample', 'It is a strong acid']),
         ('How many peaks are in the ¹³C NMR spectrum of benzene?', '1', 'All six carbons are equivalent.', ['6', '3', '2'])])
mcqs(t, [('Which isomer of C₃H₈O gives only two peaks in its ¹³C NMR spectrum?', 'Propan-2-ol', 'Symmetrical.', ['Propan-1-ol', 'Methoxyethane', 'All of them give three peaks']),
         ('Why does the carbon bonded to oxygen in ethanol have a larger chemical shift than the CH₃ carbon?', 'Oxygen is electronegative and withdraws electron density, deshielding that carbon', 'Deshielding raises δ.', ['It has more hydrogens', 'It is further from TMS', 'It is shielded by oxygen'])], D=(2, 3), C='C2')
shorts(t, [('State what each peak in a ¹³C NMR spectrum represents.', 'A different carbon environment.', '[1]')])
explain(t, [('Explain why the ¹³C NMR spectrum of propanone has only two peaks.', 'The two CH₃ carbons are equivalent (molecule is symmetrical), giving one peak; the C=O carbon gives the second.', '[2]'),
            ('Explain how ¹³C NMR can distinguish between butanone and butanal.', 'Butanone C=O near 209 ppm with 4 peaks; butanal C=O around 200 ppm and its CH environments differ; both have 4 peaks, but chemical shifts of the carbons next to C=O differ (e.g. CH₃CO at 29 in butanone).', '[2]'),
            ('Explain why the carbon atoms in a molecule have different chemical shifts.', 'Each carbon is in a different electronic environment; nearby electronegative atoms withdraw electron density (deshield), increasing δ.', '[2]')])
myths(t, [('The number of peaks in a ¹³C NMR spectrum equals the number of carbon atoms.', 'It equals the number of different carbon environments; equivalent carbons give one peak.'),
          ('¹³C NMR peaks are split by neighbouring hydrogens in A Level spectra.', 'Standard ¹³C spectra are decoupled and each environment appears as a single line.'),
          ('Carbon atoms next to oxygen have lower chemical shifts than alkyl carbons.', 'Oxygen deshields the carbon, giving a higher chemical shift (50–90 ppm).')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def c13_q(r, D):
    c = r.choice(CMPD)
    nm, f, M, nC, cls, c13, h1, hal = c
    npk = len(c13)
    if D <= 2:
        return MQ(r, f'How many peaks would be seen in the ¹³C NMR spectrum of {nm}, {f}?', str(npk), [str(x) for x in range(1, 9) if x != npk and abs(x - npk) <= 3][:3], f'{npk} carbon environments.')
    st = f'Predict the number of peaks in the ¹³C NMR spectrum of {nm}, {f}, and suggest the approximate chemical shift of each, identifying the carbon responsible.'
    ans = f'{npk} peaks: ' + '; '.join(f'δ ≈ {d} ({lbl})' for d, lbl in c13)
    key = f'{npk} peaks [1]; shifts in correct ranges [2]; assignments [1] [4]'
    if D >= 5:
        st += ' Explain why there are fewer peaks than carbon atoms, if this is the case.'
        ans += ('; some carbons are equivalent by symmetry, so they share a peak' if npk < nC else '; every carbon is in a different environment')
        key = key.replace(' [4]', '; symmetry / equivalence [1] [5]')
    return Q(st, ans, key, 'short')


@t.add('C3', (2, 3, 4, 5), 'short')
def c13_id(r, D):
    grp = r.choice([['propan-1-ol', 'propan-2-ol', 'ethyl methanoate'], ['ethyl ethanoate', 'methyl propanoate', 'butanone', '2-methylpropanoic acid'], ['1-bromopropane', '2-bromopropane'],
                    ['propanone', 'propanoic acid', 'methyl ethanoate'], ['pentan-3-one', 'ethyl propanoate', 'butanone']])
    cs = [c for c in CMPD if c[0] in grp]
    tgt = r.choice(cs)
    sh = ', '.join(str(d) for d, _ in tgt[5])
    if D <= 2:
        return MQ(r, f'A compound has ¹³C NMR peaks at δ {sh}. Which compound is it?', tgt[0], [c[0] for c in cs if c != tgt] + [x for x in ['ethanol', 'benzene', 'methylbenzene'] if x not in grp][:4 - len(cs)], f'{tgt[0]}: ' + '; '.join(f'{d} {lbl}' for d, lbl in tgt[5]) + '.')
    return Q(f'A compound is one of: {", ".join(grp)}. Its ¹³C NMR spectrum has peaks at δ {sh}. Identify the compound and explain your reasoning.', f'{tgt[0]}: ' + '; '.join(f'{d} = {lbl}' for d, lbl in tgt[5]) + '.',
             'identity [1]; number of environments used [1]; at least two shifts assigned [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def c13_case(r, D):
    a, b = r.choice([('propan-1-ol', 'propan-2-ol'), ('1-bromopropane', '2-bromopropane'), ('ethyl ethanoate', 'methyl propanoate'), ('butanone', '2-methylpropanoic acid'), ('propanone', 'propanoic acid')])
    ca = [c for c in CMPD if c[0] == a][0]
    cb = [c for c in CMPD if c[0] == b][0]
    st = f'{who(r)} has two unlabelled bottles containing {a} ({ca[1]}) and {b} ({cb[1]}) and runs a ¹³C NMR spectrum of each.'
    parts = [P_(f'Predict the number of peaks for each compound.', f'{a}: {len(ca[5])}; {b}: {len(cb[5])}', 'each [1] [2]'),
             P_(f'Predict the approximate chemical shift of the carbon with the highest δ value in each compound and explain why it is high.', f'{a}: δ ≈ {max(ca[5])[0]} ({max(ca[5])[1]}); {b}: δ ≈ {max(cb[5])[0]} ({max(cb[5])[1]}); deshielded by electronegative atom(s) bonded to it.', 'values [1]; explanation [1] [2]'),
             P_('Explain why TMS is added to the samples.', 'It is the reference (δ = 0): inert, volatile, single peak from equivalent atoms.', '[1]'),
             P_('Explain whether the two compounds could be distinguished using only the number of peaks.', ('Yes: different numbers of environments.' if len(ca[5]) != len(cb[5]) else 'No: both have the same number of peaks, so the chemical shifts must be used.'), '[1]'),
             P_('State the solvent used in NMR and explain why.', 'CDCl₃ (deuterated solvent): it contains no ¹H that would give a large solvent signal (for ¹H NMR) and is a suitable non-protic solvent.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how ¹³C NMR spectroscopy is used to determine the structure of an organic compound, using examples of isomers.', 'Each peak = one carbon environment; number of peaks shows symmetry; chemical shift ranges from data booklet (alkyl 5–40, C–O 50–90, aryl 110–160, acid/ester C=O 160–185, aldehyde/ketone C=O 190–220); TMS reference; examples propan-1-ol (3) vs propan-2-ol (2), 1- vs 2-bromopropane; combined with other data.',
           'environments and peaks [2]; chemical shift ranges [2]; TMS [1]; isomer examples [2] [7]')])
t11b = t

# ---------------------------------------------------------------------
t = T('Proton (¹H) NMR: chemical shift, integration, splitting (n+1 rule) and D2O exchange', 'proton (¹h) nmr')
facts(t, [('n + 1 rule', 'a ¹H NMR peak is split into n + 1 lines by n equivalent protons on adjacent carbon atoms'),
          ('integration', 'the relative area under each ¹H NMR peak, proportional to the number of protons in that environment'),
          ('D₂O exchange', 'shaking a sample with D₂O replaces O–H and N–H protons with deuterium, so their peaks disappear from the ¹H NMR spectrum'),
          ('spin–spin splitting', 'the splitting of an NMR peak into a multiplet caused by the magnetic fields of protons on neighbouring carbon atoms'),
          ('deuterated solvent', 'a solvent such as CDCl₃ in which ¹H is replaced by ²H, so that it gives no peak in a ¹H NMR spectrum'),
          ('proton environment', 'a set of equivalent hydrogen atoms that give a single peak (possibly split) in a ¹H NMR spectrum')])
mcqs(t, [('Into how many lines is the CH₂ peak of ethanol (CH₃CH₂OH) split?', '4 (quartet)', 'Adjacent CH₃: 3 + 1.', ['3 (triplet)', '2 (doublet)', '1 (singlet)']),
         ('Which peak disappears when D₂O is added to a sample of propan-1-ol?', 'The O–H peak', 'O–H exchanges with D.', ['The CH₃ peak', 'The CH₂–O peak', 'All peaks']),
         ('What is the ratio of the peak areas in the ¹H NMR spectrum of ethyl ethanoate?', '3 : 3 : 2', 'CH₃ (ethyl), CH₃CO, OCH₂.', ['3 : 2 : 1', '1 : 1 : 1', '6 : 2']),
         ('Why does the O–H proton of an alcohol usually appear as a singlet?', 'It exchanges rapidly with other O–H protons, so it does not couple with neighbouring CH protons', 'Rapid exchange removes splitting.', ['It has no neighbours', 'It is shielded by oxygen', 'It is too small to detect'])])
mcqs(t, [('A peak at δ 1.2 is a doublet with integration 6, and a peak at δ 4.0 is a septet with integration 1. Which group is present?', '(CH₃)₂CH–', 'Six equivalent H next to one H, and one H next to six H.', ['CH₃CH₂–', '(CH₃)₃C–', 'CH₃CO–']),
         ('Why does a CH₃ group next to a C=O give a singlet near δ 2.1 in butanone?', 'The adjacent carbon (C=O) has no hydrogens', 'n = 0, so n + 1 = 1.', ['It is next to an oxygen atom', 'The three H are not equivalent', 'It exchanges with D₂O'])], D=(2, 3), C='C2')
shorts(t, [('State what information is given by the integration of a ¹H NMR spectrum.', 'The relative number of hydrogen atoms in each environment.', '[1]'),
           ('Explain why CDCl₃ rather than CHCl₃ is used as the solvent for ¹H NMR.', 'CDCl₃ contains no ¹H, so it gives no peak that would interfere with the sample spectrum.', '[1]')])
explain(t, [('Explain the splitting pattern of the ¹H NMR spectrum of chloroethane.', 'CH₃ (δ 1.5) is split into a triplet by the 2 H on the adjacent CH₂; CH₂Cl (δ 3.6) is split into a quartet by the 3 H on the adjacent CH₃ (n + 1 rule).', 'triplet for CH₃ with reason [1]; quartet for CH₂ with reason [1] [2]'),
            ('Explain how D₂O can be used to identify an O–H or N–H peak.', 'Shake with D₂O: O–H/N–H protons exchange with deuterium (O–D), which does not absorb in the ¹H range, so that peak disappears from the spectrum.', 'exchange [1]; peak disappears [1] [2]'),
            ('Explain why the CH₂ protons of ethyl ethanoate have a larger chemical shift than the CH₃CO protons.', 'The CH₂ is bonded to the electronegative ester oxygen, which strongly deshields it (δ ≈ 4.1); the CH₃ is next to C=O and less deshielded (δ ≈ 2.0).', '[2]')])
myths(t, [('A CH₂ group next to a CH₃ group appears as a triplet.', 'It is split by the 3 H on CH₃ into a quartet (n + 1 = 4); the CH₃ appears as a triplet.'),
          ('The number of lines in a multiplet equals the number of H atoms in that group.', 'The splitting depends on the number of H on adjacent carbons (n + 1), not on the group itself.'),
          ('Adding D₂O removes all peaks from hydrogen atoms bonded to carbon.', 'Only O–H and N–H protons exchange; C–H peaks remain.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def h1_q(r, D):
    c = r.choice(CMPD)
    nm, f, M, nC, cls, c13, h1, hal = c
    if D <= 2:
        a = r.randrange(2)
        if a == 0:
            n_ = h_peaks(c)
            return MQ(r, f'How many peaks would be seen in the low-resolution ¹H NMR spectrum of {nm}, {f}?', str(n_), [str(x) for x in range(1, 7) if x != n_][:3], f'{n_} proton environments: {h_ratio(c)}.')
        sp = [h for h in h1 if h[2] not in ('multiplet',)]
        h = r.choice(sp)
        return MQ(r, f'In the high-resolution ¹H NMR spectrum of {nm}, {f}, what is the splitting pattern of the {h[3]} protons?', h[2], [x for x in ('singlet', 'doublet', 'triplet', 'quartet', 'sextet', 'septet') if x != h[2]][:3], f'{h[3]}: {h[2]} (n + 1 rule).')
    st = f'Predict the high-resolution ¹H NMR spectrum of {nm}, {f}: give the number of peaks, their approximate chemical shifts, relative integrations and splitting patterns.'
    ans = f'{h_peaks(c)} peaks: {h_desc(c)}'
    key = f'{h_peaks(c)} peaks [1]; integration ratio {h_ratio(c)} [1]; splitting patterns [2]; shifts in correct ranges [1]'
    tot = 5
    if D >= 4 and cls in OH_CLASS:
        st += ' State and explain what happens to the spectrum when D₂O is added.'
        ans += '; with D₂O the O–H/N–H peak disappears because H exchanges with D'
        key += '; D₂O: O–H/N–H peak disappears [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'short')
def h1_id(r, D):
    pool = [c for c in CMPD if c[0] != 'benzene']
    c = r.choice(pool)
    data = h_desc(c)
    peaks = '; '.join(f'δ {format(h[0], '.1f')} ({h[1]}H, {h[2]})' for h in c[6])
    if D <= 2:
        others = r.sample([x for x in pool if x[0] != c[0]], 3)
        return MQ(r, f'A compound gives these ¹H NMR peaks: {peaks}. Which compound is it?', c[0], [o[0] for o in others], f'{c[0]}: {data}.')
    st = f'A compound with molecular formula {formula_of(c)} gives the ¹H NMR spectrum: {peaks}. Identify the compound, assigning each peak.'
    if c[4] in ('alcohol', 'amine'):
        xh = [h for h in c[6] if h[3] in ('O–H', 'N–H₂')][0]
        st += f' The peak at δ {format(xh[0], '.1f')} disappears on shaking with D₂O.'
    return Q(st, f'{c[0]}, {c[1]}: {data}', 'identity [1]; assignment of each peak with splitting explained [2]; integration used [1] [4]', 'short')


MOLF = {'ethanol': 'C₂H₆O', 'propan-1-ol': 'C₃H₈O', 'propan-2-ol': 'C₃H₈O', 'ethanoic acid': 'C₂H₄O₂', 'propanoic acid': 'C₃H₆O₂', 'ethanal': 'C₂H₄O', 'propanone': 'C₃H₆O',
        'butanone': 'C₄H₈O', 'ethyl ethanoate': 'C₄H₈O₂', 'methyl propanoate': 'C₄H₈O₂', 'methyl ethanoate': 'C₃H₆O₂', 'ethyl methanoate': 'C₃H₆O₂', '1-bromopropane': 'C₃H₇Br',
        '2-bromopropane': 'C₃H₇Br', 'chloroethane': 'C₂H₅Cl', '2-chloropropane': 'C₃H₇Cl', '2-methylpropan-2-ol': 'C₄H₁₀O', 'ethylamine': 'C₂H₇N', 'phenylethanone': 'C₈H₈O',
        'methylbenzene': 'C₇H₈', 'pentan-3-one': 'C₅H₁₀O', 'ethyl propanoate': 'C₅H₁₀O₂', '2-methylpropanoic acid': 'C₄H₈O₂', 'benzene': 'C₆H₆'}


def formula_of(c):
    return MOLF[c[0]]


@t.add('C4', (2, 3, 4, 5), 'case')
def h1_case(r, D):
    a, b = r.choice([('ethyl ethanoate', 'methyl propanoate'), ('propan-1-ol', 'propan-2-ol'), ('methyl ethanoate', 'ethyl methanoate'), ('1-bromopropane', '2-bromopropane'), ('ethyl methanoate', 'propanoic acid')])
    ca = [c for c in CMPD if c[0] == a][0]
    cb = [c for c in CMPD if c[0] == b][0]
    st = f'{who(r)} has to decide whether a sample is {a} or {b}, which are isomers ({formula_of(ca)}), using high-resolution ¹H NMR.'
    parts = [P_(f'Predict the ¹H NMR spectrum of {a}.', h_desc(ca), 'peaks and integration [1]; splitting [1]; shifts [1] [3]'),
             P_(f'Predict the ¹H NMR spectrum of {b}.', h_desc(cb), 'peaks and integration [1]; splitting [1]; shifts [1] [3]'),
             P_('Identify one feature that would distinguish the two spectra most clearly.', f'e.g. {a}: {ca[6][-1][2]} at δ {format(ca[6][-1][0], '.1f')} ({ca[6][-1][3]}); {b}: {cb[6][-1][2]} at δ {format(cb[6][-1][0], '.1f')} ({cb[6][-1][3]}).', '[2]'),
             P_('Explain why a deuterated solvent and TMS are used.', 'CDCl₃ has no ¹H so gives no interfering peak; TMS is the reference at δ 0 (single peak, inert, volatile).', '[2]')]
    if ca[4] in OH_CLASS or cb[4] in OH_CLASS:
        parts.append(P_('Explain how D₂O could confirm the presence of an O–H group.', 'Shake with D₂O: the O–H proton exchanges for D and its peak disappears.', '[1]'))
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how chemical shift, integration and spin–spin splitting in a high-resolution ¹H NMR spectrum are used to determine the structure of an organic compound, including the use of D₂O.', 'Chemical shift: environment; deshielding by O, Cl, C=O, aryl (ranges); integration ratio = relative number of H; n + 1 rule with example (ethyl group triplet/quartet; isopropyl doublet/septet); singlets for CH₃ next to C=O or O; O–H/N–H singlets, broad, variable; D₂O exchange removes O–H/N–H peak; TMS and CDCl₃; worked example such as ethyl ethanoate.',
           'chemical shift [1]; integration [1]; n + 1 rule with example [2]; D₂O [1]; TMS/solvent [1]; worked example [1] [7]')])
t11c = t

CHAPTERS[11] = [t11a, t11b, t11c]


# ===================================================================== 12 Organic synthesis
CHIR = [('thalidomide', 1, 'one enantiomer is a sedative; the other caused birth defects (and the forms interconvert in the body)'),
        ('ibuprofen', 1, 'only the (S)-enantiomer is an effective painkiller; the (R)-form is slowly converted in the body'),
        ('2-hydroxypropanoic acid (lactic acid)', 1, None), ('alanine, CH₃CH(NH₂)COOH', 1, None), ('glycine, H₂NCH₂COOH', 0, None),
        ('butan-2-ol', 1, None), ('propan-2-ol', 0, None), ('2-chlorobutane', 1, None), ('1-chlorobutane', 0, None),
        ('2-hydroxypropanenitrile', 1, None), ('3-methylhexane', 1, None), ('2-methylbutanoic acid', 1, None),
        ('ephedrine, C₆H₅CH(OH)CH(CH₃)NHCH₃', 2, None), ('propanone', 0, None), ('L-DOPA', 1, 'only the L-enantiomer is used to treat Parkinson\'s disease; the D-form has side effects'),
        ('naproxen', 1, 'the (S)-enantiomer is the anti-inflammatory drug; the (R)-enantiomer is toxic to the liver'),
        ('menthol', 3, None), ('penicillamine', 1, 'the D-form treats arthritis; the L-form is toxic'), ('2-aminobutanoic acid', 1, None), ('pentan-3-ol', 0, None)]

t = T('Chirality in drug synthesis: separating optical isomers and using natural chiral molecules', 'chirality in drug synthesis')
facts(t, [('chiral centre', 'a carbon atom bonded to four different atoms or groups, giving rise to optical isomers'),
          ('enantiomers', 'a pair of optical isomers that are non-superimposable mirror images of each other'),
          ('racemic mixture', 'an equimolar mixture of two enantiomers, which does not rotate plane-polarised light'),
          ('chiral pool', 'naturally occurring chiral molecules, such as amino acids and sugars, used as single-enantiomer starting materials'),
          ('resolution', 'the separation of a racemic mixture into its two enantiomers'),
          ('chiral catalyst', 'a catalyst, often an enzyme or a metal complex with a chiral ligand, that produces mainly one enantiomer')])
mcqs(t, [('Which molecule contains a chiral centre?', 'Butan-2-ol', 'C2 has H, OH, CH₃ and C₂H₅.', ['Propan-2-ol', '1-chlorobutane', 'Propanone']),
         ('Why is a racemic mixture optically inactive?', 'Equal amounts of the two enantiomers rotate plane-polarised light equally in opposite directions', 'Rotations cancel.', ['It contains no chiral centres', 'It absorbs polarised light', 'The enantiomers react together']),
         ('Which is an advantage of making a drug as a single enantiomer?', 'A smaller dose is needed and side effects from the other isomer are avoided', 'Only one isomer is active.', ['The drug becomes optically inactive', 'The drug is always cheaper to make', 'It increases the number of chiral centres']),
         ('Which method produces a single enantiomer directly?', 'Using an enzyme as a stereoselective catalyst', 'Enzymes are chiral catalysts.', ['Free-radical substitution', 'Nucleophilic addition of HCN to ethanal', 'Fractional distillation'])])
mcqs(t, [('Nucleophilic addition of HCN to ethanal gives a racemic product because', 'the planar C=O can be attacked equally from either side', 'Equal chance of each enantiomer.', ['the product has no chiral centre', 'HCN is a chiral reagent', 'ethanal is chiral']),
         ('Why can enzymes distinguish between enantiomers?', 'Their active sites are chiral, so only one enantiomer fits and binds correctly', 'Shape complementarity.', ['Enzymes are optically inactive', 'Enzymes destroy one enantiomer by heat', 'Enantiomers have different Mr'])], D=(2, 3), C='C2')
shorts(t, [('State two methods used by the pharmaceutical industry to obtain a single enantiomer of a drug.', 'Any two: use a chiral (enzyme / metal–ligand) catalyst; start from a natural chiral molecule (chiral pool); separate (resolve) the racemic mixture, e.g. by chiral chromatography or forming diastereomeric salts.', '[2]')])
explain(t, [('Explain why many synthetic reactions produce a racemic mixture.', 'If an intermediate (e.g. a planar carbocation or C=O) is attacked equally from either side, both enantiomers form in equal amounts.', '[2]'),
            ('Explain why it is important for a drug to be produced as a single optical isomer.', 'Receptors in the body are chiral, so the two enantiomers may have different effects: one may be inactive or harmful (e.g. thalidomide); a single isomer allows a smaller dose and fewer side effects, and is required by regulators.', 'chiral receptors [1]; different activity / harm [1]; dose / side effects [1] [3]'),
            ('Explain why resolving a racemic mixture is wasteful.', 'At least half of the product is the unwanted enantiomer, which must be discarded or converted, lowering the yield and increasing cost and waste.', '[2]')])
myths(t, [('Enantiomers have different chemical properties in all reactions.', 'Enantiomers have identical chemical properties except in reactions with other chiral molecules (e.g. enzymes, receptors).'),
          ('A racemic mixture contains no chiral molecules.', 'It contains equal amounts of two chiral enantiomers whose rotations cancel.'),
          ('All drugs with a chiral centre are harmless as racemic mixtures.', 'The other enantiomer may be inactive or harmful, as in thalidomide.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def chiral_q(r, D):
    nm, n, note = r.choice(CHIR)
    if D <= 2:
        return MQ(r, f'How many chiral centres are present in {nm}?', str(n), [str(x) for x in range(0, 5) if x != n][:3], f'{nm}: {n} chiral centre(s).')
    st = f'State the number of chiral centres in {nm} and the maximum number of stereoisomers that could exist because of them.'
    ans = f'{n} chiral centre(s); maximum 2{sup(n)} = {2 ** n} stereoisomer(s)' if n else '0 chiral centres; no optical isomers'
    key = f'{n} [1]; 2ⁿ = {2 ** n if n else 1} [1]'
    tot = 2
    if D >= 4 and note:
        st += ' Explain why the drug is preferably supplied as a single enantiomer.'
        ans += f'; {note}, so a single enantiomer gives the desired effect with a smaller dose and fewer side effects'
        key += '; reason referring to different biological activity [1]'
        tot += 1
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def chiral_calc(r, D):
    drug = r.choice(['ibuprofen', 'naproxen', 'a β-blocker', 'an anti-asthma drug', 'a herbicide'])
    m_ = r.choice([50.0, 100.0, 200.0, 250.0, 500.0])  # kg racemic
    rec = r.choice([70, 80, 85, 90])
    good = m_ / 2 * rec / 100
    st = f'A company in {city(r)} makes {m_:.0f} kg of {drug} as a racemic mixture. Only one enantiomer is active. Resolution recovers {rec}% of the active enantiomer. Calculate the mass of active enantiomer obtained and the percentage of the original product that is wasted.'
    key = f'active enantiomer present = {fx(m_ / 2, 1)} kg [1]; recovered = {g3(good)} kg [1]; wasted = {g3(100 - good / m_ * 100)}% [1] [3]'
    ans = f'{g3(good)} kg; {g3(100 - good / m_ * 100)}% wasted'
    if D >= 4:
        st += ' Suggest two ways in which the process could be made more efficient.'
        ans += '; use a chiral catalyst / enzyme or a chiral-pool starting material to make only the active enantiomer; racemise and recycle the unwanted enantiomer'
        key = key.replace(' [3]', '') + '; two suggestions [2] [5]'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def chiral_case(r, D):
    nm, n, note = r.choice([c for c in CHIR if c[2]])
    st = f'A pharmaceutical company in {city(r)} manufactures {nm}, which has {n} chiral centre{"s" if n > 1 else ""}: {note}.'
    parts = [P_('Explain what is meant by a chiral centre and describe how the two enantiomers differ.', 'A carbon atom attached to four different groups; enantiomers are non-superimposable mirror images that rotate plane-polarised light in opposite directions.', 'definition [1]; mirror images / optical activity [1] [2]'),
             P_('Explain why the two enantiomers have different effects in the body.', 'Receptors and enzymes are chiral; only one enantiomer fits the binding site correctly (like a hand in a glove).', '[2]'),
             P_('Describe two ways the company could obtain the single active enantiomer.', 'Use a chiral catalyst or enzyme (stereoselective synthesis); start from a natural chiral molecule (chiral pool); or resolve the racemate (chiral chromatography / diastereomeric salts).', 'any two [2]'),
             P_('Give two advantages of producing the single enantiomer rather than the racemate.', 'Smaller dose; fewer side effects; less waste; better regulatory approval / patent protection.', '[2]'),
             P_('Suggest a disadvantage of making the single enantiomer.', 'Extra steps or expensive chiral catalysts/separations increase cost; lower overall yield.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Discuss the importance of chirality in drug design and evaluate the methods used to produce single-enantiomer drugs.', 'Chiral centre and enantiomers; chiral receptors give different activities; thalidomide example; synthetic routes often give racemates (planar intermediates); methods: resolution (wasteful, ≤50%), chiral catalysts/enzymes (stereoselective), chiral pool starting materials (amino acids, sugars); advantages: smaller dose, fewer side effects; disadvantages: cost, extra steps; evaluation.',
           'chirality and receptors [2]; example [1]; racemate formation [1]; methods compared [2]; evaluation [1] [7]')])
t12a = t

# ---------------------------------------------------------------------
STEP = {('alkene', 'bromoalkane'): 'HBr(g) at room temperature', ('alkene', 'alcohol'): 'steam with H₃PO₄ catalyst, about 300 °C and 6 MPa',
        ('bromoalkane', 'alcohol'): 'NaOH(aq), heat under reflux', ('bromoalkane', 'nitrile'): 'KCN in ethanol, heat under reflux',
        ('bromoalkane', 'amine'): 'excess NH₃ in ethanol, heat in a sealed tube', ('nitrile', 'acid'): 'dilute HCl(aq), heat under reflux',
        ('nitrile', 'amine'): 'LiAlH₄ in dry ether (or H₂ with Ni catalyst)', ('alcohol1', 'aldehyde'): 'K₂Cr₂O₇ with dilute H₂SO₄, warm and distil off the product',
        ('alcohol1', 'acid'): 'K₂Cr₂O₇ with dilute H₂SO₄, heat under reflux', ('alcohol2', 'ketone'): 'K₂Cr₂O₇ with dilute H₂SO₄, heat under reflux',
        ('carbonyl', 'hydroxynitrile'): 'HCN with a KCN catalyst (or NaCN/H⁺), room temperature', ('hydroxynitrile', 'hydroxyacid'): 'dilute HCl(aq), heat under reflux',
        ('acid', 'acylchloride'): 'SOCl₂ (or PCl₅), room temperature / warm', ('acylchloride', 'ester'): 'an alcohol (or phenol), room temperature',
        ('acylchloride', 'amide'): 'NH₃ or a primary amine, room temperature', ('acid', 'ester'): 'an alcohol with concentrated H₂SO₄ catalyst, heat under reflux',
        ('amide', 'amine'): 'LiAlH₄ in dry ether', ('carbonyl', 'alcohol'): 'NaBH₄ in water or ethanol', ('alcohol', 'alkene'): 'heat with Al₂O₃ or concentrated H₃PO₄',
        ('benzene', 'nitro'): 'concentrated HNO₃ and H₂SO₄, below 55 °C', ('nitro', 'arylamine'): 'Sn and concentrated HCl, heat under reflux, then NaOH(aq)',
        ('arylamine', 'diazonium'): 'NaNO₂ and dilute HCl, below 10 °C', ('diazonium', 'phenol'): 'warm with water above 10 °C',
        ('methylarene', 'benzoic'): 'hot alkaline KMnO₄, heat under reflux, then acidify', ('benzene', 'ketone_ar'): 'CH₃COCl with anhydrous AlCl₃, heat under reflux',
        ('benzene', 'alkylarene'): 'CH₃Cl with anhydrous AlCl₃, heat under reflux', ('arylamine', 'amide'): 'CH₃COCl, room temperature',
        ('alcohol', 'bromoalkane'): 'NaBr with concentrated H₂SO₄, heat (or PBr₃)', ('alkylarene', 'benzoic'): 'hot alkaline KMnO₄, heat under reflux, then acidify'}
ROUTES = [
    [('ethene', 'alkene'), ('bromoethane', 'bromoalkane'), ('propanenitrile', 'nitrile'), ('propanoic acid', 'acid')],
    [('ethene', 'alkene'), ('bromoethane', 'bromoalkane'), ('propanenitrile', 'nitrile'), ('propylamine', 'amine')],
    [('propan-1-ol', 'alcohol1'), ('propanal', 'aldehyde'), ('2-hydroxybutanenitrile', 'hydroxynitrile'), ('2-hydroxybutanoic acid', 'hydroxyacid')],
    [('ethanol', 'alcohol1'), ('ethanal', 'aldehyde'), ('2-hydroxypropanenitrile', 'hydroxynitrile'), ('2-hydroxypropanoic acid', 'hydroxyacid')],
    [('propan-2-ol', 'alcohol2'), ('propanone', 'ketone'), ('2-hydroxy-2-methylpropanenitrile', 'hydroxynitrile'), ('2-hydroxy-2-methylpropanoic acid', 'hydroxyacid')],
    [('benzene', 'benzene'), ('nitrobenzene', 'nitro'), ('phenylamine', 'arylamine'), ('N-phenylethanamide', 'amide')],
    [('benzene', 'benzene'), ('nitrobenzene', 'nitro'), ('phenylamine', 'arylamine'), ('benzenediazonium chloride', 'diazonium'), ('phenol', 'phenol')],
    [('methylbenzene', 'methylarene'), ('benzoic acid', 'benzoic'), ('benzoyl chloride', 'acylchloride'), ('methyl benzoate', 'ester')],
    [('ethanol', 'alcohol1'), ('ethanoic acid', 'acid'), ('ethanoyl chloride', 'acylchloride'), ('phenyl ethanoate', 'ester')],
    [('bromoethane', 'bromoalkane'), ('ethanol', 'alcohol1'), ('ethanoic acid', 'acid'), ('ethyl ethanoate', 'ester')],
    [('propene', 'alkene'), ('2-bromopropane', 'bromoalkane'), ('propan-2-ol', 'alcohol2'), ('propanone', 'ketone')],
    [('1-bromobutane', 'bromoalkane'), ('butan-1-ol', 'alcohol1'), ('butanoic acid', 'acid'), ('butanoyl chloride', 'acylchloride'), ('butanamide', 'amide')],
    [('ethanoic acid', 'acid'), ('ethanoyl chloride', 'acylchloride'), ('ethanamide', 'amide'), ('ethylamine', 'amine')],
    [('chloroethane', 'bromoalkane'), ('propanenitrile', 'nitrile'), ('propylamine', 'amine')],
    [('but-1-ene', 'alkene'), ('2-bromobutane', 'bromoalkane'), ('butan-2-ol', 'alcohol2'), ('butanone', 'ketone'), ('2-hydroxy-2-methylbutanenitrile', 'hydroxynitrile')],
    [('benzene', 'benzene'), ('phenylethanone', 'ketone_ar'), ('1-phenylethanol', 'alcohol')],
    [('benzene', 'benzene'), ('methylbenzene', 'alkylarene'), ('benzoic acid', 'benzoic')],
    [('propan-1-ol', 'alcohol'), ('propene', 'alkene'), ('2-bromopropane', 'bromoalkane'), ('2-methylpropanenitrile', 'nitrile')]]


def step_key(a, b):
    ka, kb = a[1], b[1]
    if (ka, kb) in STEP:
        return STEP[(ka, kb)]
    alias = {'alcohol1': 'alcohol', 'alcohol2': 'alcohol', 'aldehyde': 'carbonyl', 'ketone': 'carbonyl', 'ketone_ar': 'carbonyl'}
    k2 = (alias.get(ka, ka), alias.get(kb, kb))
    if k2 in STEP:
        return STEP[k2]
    if ka == 'bromoalkane' and kb == 'alcohol2':
        return STEP[('bromoalkane', 'alcohol')]
    if ka == 'bromoalkane' and kb == 'alcohol1':
        return STEP[('bromoalkane', 'alcohol')]
    if ka == 'alcohol' and kb == 'alkene':
        return STEP[('alcohol', 'alkene')]
    if ka == 'benzoic' and kb == 'acylchloride':
        return STEP[('acid', 'acylchloride')]
    if ka == 'alcohol1' and kb == 'acid':
        return STEP[('alcohol1', 'acid')]
    raise KeyError((ka, kb))


EXTRA_R = {('acylchloride', 'ester'): {'methyl benzoate': 'methanol, room temperature', 'phenyl ethanoate': 'phenol, room temperature'},
           ('acid', 'ester'): {'ethyl ethanoate': 'ethanol with concentrated H₂SO₄ catalyst, heat under reflux'},
           ('arylamine', 'amide'): {'N-phenylethanamide': 'ethanoyl chloride, room temperature'}}


def reagent(a, b):
    ex = EXTRA_R.get((a[1], b[1]), {})
    if b[0] in ex:
        return ex[b[0]]
    if a[1] == 'acylchloride' and b[1] == 'amide':
        return 'concentrated NH₃, room temperature' if b[0].endswith('amide') and not b[0].startswith('N-') else STEP[('acylchloride', 'amide')]
    return step_key(a, b)


t = T('Multi-step synthetic routes: identifying functional groups and reagents to convert one compound to another', 'multi-step synthetic routes')
facts(t, [('synthetic route', 'a sequence of reactions, each with stated reagents and conditions, used to convert a starting material into a target molecule'),
          ('functional group interconversion', 'the conversion of one functional group into another, e.g. a primary alcohol into a carboxylic acid'),
          ('overall yield', 'the product of the percentage yields of the individual steps of a synthesis, expressed as a percentage'),
          ('chain extension', 'increasing the carbon chain length by one, e.g. using CN⁻ with a halogenoalkane or HCN with a carbonyl compound'),
          ('retrosynthesis', 'planning a synthesis by working backwards from the target molecule to available starting materials'),
          ('atom economy', 'the percentage of the mass of reactants that ends up in the desired product')])
mcqs(t, [('Which reagent increases the carbon chain length of a halogenoalkane by one?', 'KCN in ethanol', 'Forms a nitrile.', ['NaOH(aq)', 'NH₃ in ethanol', 'K₂Cr₂O₇/H⁺']),
         ('Which reagent and condition convert a primary alcohol into an aldehyde?', 'K₂Cr₂O₇ with dilute H₂SO₄, distilling off the product as it forms', 'Prevents further oxidation.', ['K₂Cr₂O₇ with dilute H₂SO₄ under reflux', 'NaBH₄', 'Concentrated H₂SO₄ at 170 °C']),
         ('Which reagent converts a nitrile into a carboxylic acid?', 'Dilute HCl(aq), heat under reflux', 'Acid hydrolysis.', ['LiAlH₄', 'NaBH₄', 'KCN']),
         ('A three-step synthesis has yields of 80%, 70% and 50%. What is the overall yield?', '28%', '0.80 × 0.70 × 0.50 = 0.28.', ['67%', '50%', '200%'])])
mcqs(t, [('Why is HCN addition to an aldehyde followed by acid hydrolysis useful in synthesis?', 'It adds one carbon and gives a 2-hydroxycarboxylic acid', 'Chain extension plus two functional groups.', ['It removes a carbon atom', 'It forms an alkene', 'It gives a single enantiomer']),
         ('Which reagent reduces a ketone to a secondary alcohol without affecting a C=C bond?', 'NaBH₄', 'Selective for C=O.', ['H₂ with Ni', 'K₂Cr₂O₇/H⁺', 'HBr'])], D=(2, 3), C='C2')
shorts(t, [('State the reagents and conditions to convert bromoethane into propanoic acid in two steps.', 'KCN in ethanol, heat under reflux (gives propanenitrile); then dilute HCl(aq), heat under reflux.', 'step 1 [1]; step 2 [1] [2]')])
explain(t, [('Explain why the overall yield of a multi-step synthesis is often low.', 'Each step has a yield below 100% (incomplete reaction, side reactions, losses on purification); the overall yield is the product of all step yields, so it falls rapidly with more steps.', '[2]'),
            ('Explain how to decide the functional groups present in a target molecule when planning a synthesis.', 'Identify functional groups in target and starting material, compare carbon skeletons (chain length change?), and choose known reactions that interconvert these groups in a sensible order.', '[2]')])
myths(t, [('Heating a primary alcohol under reflux with acidified dichromate gives an aldehyde.', 'Under reflux the aldehyde is oxidised further to a carboxylic acid; distillation is needed to obtain the aldehyde.'),
          ('NaBH₄ reduces carboxylic acids to primary alcohols.', 'NaBH₄ reduces aldehydes and ketones; it does not reduce carboxylic acids.'),
          ('The overall yield of a synthesis is the average of the yields of the steps.', 'It is the product of the step yields.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def route_q(r, D):
    rt = r.choice(ROUTES)
    i = r.randrange(len(rt) - 1)
    a, b = rt[i], rt[i + 1]
    rg = reagent(a, b)
    if D <= 2:
        pool = list(dict.fromkeys(STEP.values()))
        wrong = [w for w in pool if w != rg]
        r.shuffle(wrong)
        return MQ(r, f'Which reagents and conditions convert {a[0]} into {b[0]}?', cap(rg), [cap(w) for w in wrong[:3]], f'{a[0]} → {b[0]}: {rg}.')
    st = f'A synthetic route is: ' + ' → '.join(x[0] for x in rt) + '. Give the reagents and conditions for each step.'
    steps = [f'step {j + 1}: {reagent(rt[j], rt[j + 1])}' for j in range(len(rt) - 1)]
    ans = '; '.join(steps)
    key = f'each step correct [1] × {len(steps)}'
    tot = len(steps)
    if D >= 4:
        st += ' Name the type of reaction in each step.'
        ans += ' (reaction types: e.g. addition, substitution, oxidation, hydrolysis, reduction, condensation as appropriate)'
        key += f'; types [{len(steps)}]'
        tot += len(steps)
    return Q(st, ans, key + f' [{tot}]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def route_yield(r, D):
    rt = r.choice([x for x in ROUTES if len(x) >= 3])
    ys = [r.choice([45, 55, 62, 70, 75, 80, 85, 92]) for _ in range(len(rt) - 1)]
    ov = math.prod(y / 100 for y in ys) * 100
    st = f'In the synthesis ' + ' → '.join(x[0] for x in rt) + ', the step yields are ' + ', '.join(f'{y}%' for y in ys) + '. Calculate the overall percentage yield.'
    key = f'overall = {" × ".join(fx(y / 100, 2) for y in ys)} × 100 [1] = {g3(ov)}% [1] [2]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the overall percentage yield.', 'What is the overall percentage yield?'), ov, [sum(ys) / len(ys), min(ys), ov * 2, 100 - ov], '%', key)
    ans = f'{g3(ov)}%'
    if D >= 4:
        st += f' Calculate the mass of {rt[0][0]} needed to make 1.00 mol of {rt[-1][0]}, if its Mr is 100 for this purpose.'.replace(' if its Mr is 100 for this purpose', '')
        st = st.replace(f'Calculate the mass of {rt[0][0]} needed to make 1.00 mol of {rt[-1][0]}.', f'Calculate the amount (in mol) of {rt[0][0]} needed to make 1.00 mol of {rt[-1][0]}.')
        need = 100 / ov
        ans += f'; {g3(need)} mol of {rt[0][0]}'
        key = key.replace(' [2]', '') + f'; n = 1.00 ÷ {g3(ov / 100)} = {g3(need)} mol [1] [3]'
    return Q(st, ans, key, 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def route_case(r, D):
    rt = r.choice([x for x in ROUTES if len(x) >= 4])
    st = f'{who(r)} in {lab(r)} needs to make {rt[-1][0]} starting from {rt[0][0]}.'
    mids = [x[0] for x in rt[1:-1]]
    parts = [P_('Suggest a synthetic route, naming the intermediate(s).', ' → '.join(x[0] for x in rt), 'intermediates [2]'),
             P_('Give the reagents and conditions for each step.', '; '.join(f'{rt[j][0]} → {rt[j + 1][0]}: {reagent(rt[j], rt[j + 1])}' for j in range(len(rt) - 1)), f'each step [1] [{len(rt) - 1}]'),
             P_(f'Describe a chemical test to show that {mids[0]} has formed in the first step.', 'A test specific to its functional group (e.g. 2,4-DNPH orange precipitate for C=O; Tollens\' silver mirror for an aldehyde; effervescence with Na₂CO₃ for an acid; IR absorption for the new group).', '[2]'),
             P_('Suggest two reasons why the overall yield would be low.', 'Each step has losses (incomplete reactions, side reactions, purification losses); yields multiply.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how a multi-step synthesis is planned, using one aliphatic and one aromatic example to illustrate the choice of reagents and conditions.', 'Identify functional groups and carbon skeleton change; chain extension with CN⁻/HCN; oxidation/reduction; hydrolysis; acyl chloride chemistry; aliphatic example e.g. ethene → bromoethane → propanenitrile → propanoic acid with conditions; aromatic example benzene → nitrobenzene → phenylamine → azo dye or amide; overall yield; safety (HCN, KCN).',
           'planning principles [2]; aliphatic route with reagents [2]; aromatic route with reagents [2]; yield/safety [1] [7]')])
t12b = t

# ---------------------------------------------------------------------
t = T('Combining analytical data (IR, MS and NMR) to identify an unknown organic compound', 'combining analytical data')
facts(t, [('molecular ion', 'M⁺: the ion formed by loss of one electron from a molecule; its m/z gives the relative molecular mass'),
          ('M+1 peak', 'a small peak one unit above M⁺ caused by molecules containing one ¹³C atom; its height relative to M⁺ gives the number of carbon atoms'),
          ('M+2 peak', 'a peak two units above M⁺ due to ³⁷Cl or ⁸¹Br; M : M+2 is about 3 : 1 for one Cl and 1 : 1 for one Br'),
          ('fragmentation', 'the breaking of the molecular ion into smaller ions in a mass spectrometer, giving characteristic peaks'),
          ('infrared spectroscopy', 'a technique that identifies bonds (functional groups) by the frequencies of infrared radiation they absorb'),
          ('fingerprint region', 'the part of an IR spectrum below 1500 cm⁻¹, unique to each compound, used to confirm identity by comparison')])
mcqs(t, [('The M+1 peak height is 4.4% of the M⁺ peak. How many carbon atoms are in the molecule?', '4', 'n = 4.4 ÷ 1.1.', ['3', '5', '44']),
         ('A mass spectrum shows M⁺ and M+2 peaks of equal height. Which atom is present?', 'One bromine atom', '⁷⁹Br : ⁸¹Br ≈ 1 : 1.', ['One chlorine atom', 'Two oxygen atoms', 'One nitrogen atom']),
         ('Which IR absorption shows that a compound is a carboxylic acid rather than an alcohol?', 'A very broad O–H at 2500–3000 cm⁻¹ together with C=O at about 1700 cm⁻¹', 'Acid O–H is broader and lower.', ['A sharp peak at 3600 cm⁻¹', 'An absorption at 2200 cm⁻¹', 'Only C–H absorptions near 2900 cm⁻¹']),
         ('A peak at m/z = 43 in the mass spectrum of butanone is due to', 'CH₃CO⁺', 'Common acylium fragment.', ['C₂H₅⁺', 'CH₃⁺', 'COOH⁺'])])
mcqs(t, [('A compound C₃H₆O shows a C=O absorption in its IR spectrum and a single peak in its ¹H NMR spectrum. What is it?', 'Propanone', 'Two equivalent CH₃ groups.', ['Propanal', 'Propan-2-ol', 'Prop-2-en-1-ol']),
         ('Why is the fingerprint region of an IR spectrum useful?', 'It can be compared with a database spectrum to confirm the identity of a compound', 'Unique pattern.', ['It shows the molecular mass', 'It shows the number of carbon atoms', 'It shows the chemical shift'])], D=(2, 3), C='C2')
shorts(t, [('State the formula linking the M+1 peak to the number of carbon atoms.', 'n = 100 × (height of M+1) ÷ (1.1 × height of M⁺)', '[1]')])
explain(t, [('Explain why a molecule containing one chlorine atom gives an M+2 peak one third the height of the M⁺ peak.', 'Chlorine exists as ³⁵Cl and ³⁷Cl in about a 3 : 1 ratio, so molecules with ³⁷Cl have m/z two units higher and are one third as abundant.', '[2]'),
            ('Explain how IR, MS and ¹H NMR data together identify an organic compound.', 'IR identifies functional groups; MS gives Mr (M⁺), number of carbons (M+1), halogens (M+2) and fragments; ¹H NMR gives the number of H environments, their ratio and neighbouring H (splitting); together they fix the structure.', 'IR [1]; MS [1]; NMR [1] [3]')])
myths(t, [('The M+1 peak is caused by a hydrogen atom attached to the molecular ion.', 'It is caused by molecules containing one ¹³C atom (natural abundance about 1.1%).'),
          ('The highest m/z peak in every mass spectrum is the molecular ion.', 'The M+1 (and M+2) peaks lie above M⁺; M⁺ is the main peak at highest m/z apart from these isotope peaks.'),
          ('IR spectroscopy alone can distinguish all isomers.', 'Isomers with the same functional groups have similar IR absorptions (except in the fingerprint region); NMR is usually needed.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def mplus1(r, D):
    c = r.choice(CMPD)
    n_ = c[3]
    hm = r.choice([20.0, 32.0, 45.0, 60.0, 75.0, 88.0])
    h1 = round(1.1 * n_ * hm / 100, 1)
    nc = 100 * h1 / (1.1 * hm)
    st = f'The mass spectrum of an organic compound has a molecular ion peak at m/z = {c[2]} with relative abundance {fx(hm, 1)} and an M+1 peak with relative abundance {fx(h1, 1)}. Calculate the number of carbon atoms in the molecule.'
    key = f'n = 100 × {fx(h1, 1)} ÷ (1.1 × {fx(hm, 1)}) [1] = {fx(nc, 2)} ≈ {n_} [1] [2]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the number of carbon atoms in the molecule.', 'How many carbon atoms are in the molecule?'), n_, [n_ + 1, n_ - 1 if n_ > 1 else n_ + 2, n_ * 2, n_ + 3], '', key, f=lambda v: str(int(round(v))))
    ans = f'{n_} carbon atoms'
    if D >= 4:
        hal = c[7]
        st += ' The compound contains only C, H and possibly O, Cl or Br. ' + (f'There is an M+2 peak {"one third" if hal == "Cl" else "equal in"} height {"of" if hal == "Cl" else "to"} the M⁺ peak.' if hal else 'There is no significant M+2 peak.') + ' Suggest a molecular formula consistent with the data.'
        ans += f'; {formula_of(c)} (Mr {c[2]})' + (f'; M+2 shows one {hal} atom' if hal else '')
        key = key.replace(' [2]', '') + f'; formula consistent with M = {c[2]} and {n_} C [1]' + ('; halogen from M+2 [1] [4]' if hal else ' [3]')
    return Q(st, ans, key, 'numerical')


@t.add('C3', (2, 3, 4, 5), 'short')
def ir_ms_q(r, D):
    c = r.choice([x for x in CMPD if x[4] != 'arene'])
    nm, f, M, nC, cls, c13, h1, hal = c
    if D <= 2:
        return MQ(r, f'An unknown compound has: {IR[cls]}. Which class of compound is it most likely to be?', cap(cls if cls != 'acid' else 'carboxylic acid'),
                  [cap(x if x != 'acid' else 'carboxylic acid') for x in ['alcohol', 'acid', 'ester', 'ketone', 'aldehyde', 'amine', 'halogenoalkane'] if x != cls][:3], f'{IR[cls]} → {cls}.')
    st = f'Compound Z has M⁺ at m/z = {M} and molecular formula {formula_of(c)}. Its IR spectrum shows {IR[cls]}. Its ¹H NMR spectrum shows: ' + '; '.join(f'δ {format(h[0], ".1f")} ({h[1]}H, {h[2]})' for h in h1) + '. Identify Z, explaining how each piece of evidence supports your answer.'
    ans = f'{nm}, {f}: IR shows {cls} group; M⁺ = {M} matches {formula_of(c)}; NMR: {h_desc(c)}.'
    return Q(st, ans, 'functional group from IR [1]; Mr from MS [1]; NMR environments and splitting interpreted [2]; correct structure [1] [5]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def unknown_case(r, D):
    c = r.choice([x for x in CMPD if x[4] not in ('arene',)])
    nm, f, M, nC, cls, c13, h1, hal = c
    hm = r.choice([40.0, 55.0, 70.0])
    hp1 = round(1.1 * nC * hm / 100, 1)
    st = (f'{who(r)} isolates an unknown compound Q from a reaction mixture. Mass spectrum: M⁺ at m/z = {M} (relative abundance {fx(hm, 1)}), M+1 peak {fx(hp1, 1)}' +
          (f', M+2 peak at m/z = {M + 2} {"one third the height of" if hal == "Cl" else "of equal height to"} M⁺' if hal else '') + f'. IR: {IR[cls]}. ¹³C NMR: {len(c13)} peaks at δ ' + ', '.join(str(d) for d, _ in c13) +
          '. ¹H NMR: ' + '; '.join(f'δ {format(h[0], ".1f")} ({h[1]}H, {h[2]})' for h in h1) + '.')
    parts = [P_('Use the M+1 peak to calculate the number of carbon atoms in Q.', str(nC), f'n = 100 × {fx(hp1, 1)} ÷ (1.1 × {fx(hm, 1)}) = {nC} [1]'),
             P_('Deduce the molecular formula of Q.', formula_of(c), '[1]'),
             P_('Identify the functional group present, using the IR data.', cap(cls if cls != 'acid' else 'carboxylic acid'), '[1]'),
             P_('Use the NMR data to deduce the structure of Q, explaining the splitting patterns.', f'{nm}, {f}: {h_desc(c)}', 'number of environments [1]; splitting explained [1]; integration [1]; structure [1] [4]'),
             P_('Suggest a fragment ion that could give a peak in the mass spectrum, with its m/z value.', {'ester': 'CH₃CO⁺ at m/z 43 or the alkoxy fragment', 'ketone': 'an acylium ion such as CH₃CO⁺ (m/z 43)', 'aldehyde': 'CHO⁺ (m/z 29) or CH₃⁺ (m/z 15)', 'alcohol': 'CH₂OH⁺ (m/z 31) or an alkyl ion', 'acid': 'COOH⁺ (m/z 45)', 'halogenoalkane': 'the alkyl cation after loss of the halogen', 'amine': 'CH₂NH₂⁺ (m/z 30)'}[cls], '[1]')]
    if hal:
        parts.append(P_('Explain what the M+2 peak shows.', f'One {hal} atom: {"³⁵Cl : ³⁷Cl ≈ 3 : 1" if hal == "Cl" else "⁷⁹Br : ⁸¹Br ≈ 1 : 1"}.', '[1]'))
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how infrared spectroscopy, mass spectrometry, ¹³C NMR and ¹H NMR are used together to identify an unknown organic compound, illustrating your answer with a named example.', 'MS: M⁺ gives Mr; M+1 gives number of C (n = 100 × M+1/(1.1 × M)); M+2 for Cl/Br; fragments; IR: O–H, C=O, N–H, C–O ranges and fingerprint region; ¹³C NMR: number of carbon environments and shift ranges; ¹H NMR: environments, integration, n + 1 splitting, D₂O exchange; worked example e.g. ethyl ethanoate (M 88, 4 C, C=O 1740, ¹H 3:3:2 with triplet/singlet/quartet).',
           'MS [2]; IR [1]; ¹³C NMR [1]; ¹H NMR [2]; worked example [1] [7]')])
t12c = t

CHAPTERS[12] = [t12a, t12b, t12c]


# ===================================================================== finalise
for _tps in CHAPTERS.values():
    for _t in _tps:
        for _tp in _t.templates:
            _tp.fn = _bio_wrap(_tp.fn)
        # no auto-paired two-part items: their 4-6 marks would land in 1-mark mock slots and unbalance mock totals
        _t.entries = {}
