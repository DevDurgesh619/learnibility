"""Cambridge International AS Chemistry 9701 (grade 11), CUP coursebook 3rd ed. chapters 1-18.

Paper 1 (MCQ), Paper 2 (AS structured) and Paper 3 (practical) styles. Data tables (isotopes,
ionisation energies, bond energies, enthalpies, equilibria, Period 3, Groups 2 and 17, organic
families) drive parameterised templates; compose() builds structured items with "[n]" part marks.

Marks convention: in a single (non-composed) item every "[n]" in the key is one mark point and the
item's marks are their sum; in a compose() part the key ends with a single "[n]" (the part total).
MCQs are 1 mark (Paper 1).
"""
import math
import re
from ._lib import topic, mcq, sf, sup, person, two_people, city, num_mcq
from ._lib import compose as _compose

_BARE = re.compile(r'^\s*\[(\d+)\]\s*$')


def _keyfix(p):
    def g(r):
        x = p(r)
        if x and _BARE.match(x[2]):
            return (x[0], x[1], x[1].rstrip() + ' ' + x[2].strip())
        if x:
            ms = [int(m) for m in re.findall(r'\[(\d+)\]', x[2])]
            if len(ms) > 1:
                body = re.sub(r'\s*\[\d+\]', '', x[2]).strip().rstrip(';').strip()
                return (x[0], x[1], f'{body} [{sum(ms)}]')
        return x
    return g


def compose(r, intro, parts, *a, need=(), **kw):
    """compose() whose parts with a bare "[n]" key get the model answer as their mark points.

    need: indices of parts that use the data given in the intro; at least one of them is always included.
    """
    ps = [_keyfix(p) if p is not None else (lambda r: None) for p in parts]
    if not need:
        return _compose(r, intro, ps, *a, **kw)
    import random as _random
    texts = []
    for i in need:
        x = parts[i](_random.Random(0)) if parts[i] is not None else None
        if x:
            texts.append(x[0])
    for _ in range(25):
        q = _compose(r, intro, ps, *a, **kw)
        if q and any(t in q['stem'] for t in texts):
            return q
    return None

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# ===================================================================== helpers
_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
_SUPT = str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')


def F(s):
    """ASCII formula -> Unicode: 'Al2(SO4)3' -> Al₂(SO₄)₃, 'SO4^2-' -> SO₄²⁻, 'CuSO4.5H2O' -> CuSO₄·5H₂O."""
    charge = ''
    if '^' in s:
        s, charge = s.split('^', 1)
    out = []
    prev = ''
    for ch in s:
        if ch.isdigit() and (prev.isalpha() or prev == ')' or prev in '₀₁₂₃₄₅₆₇₈₉'):
            ch2 = ch.translate(_SUB)
        elif ch == '.':
            ch2 = '·'
        else:
            ch2 = ch
        out.append(ch2)
        prev = ch2
    return ''.join(out) + charge.translate(_SUPT)


def E(s):
    """Equation -> Unicode, coefficients kept: '2Na + 2H2O -> 2NaOH + H2'. Tokens may carry state symbols '(g)'."""
    toks = []
    for tok in s.split(' '):
        if tok == '->':
            toks.append('→')
        elif tok == '<=>':
            toks.append('⇌')
        elif tok in ('+', '', '½'):
            toks.append(tok)
        else:
            st = ''
            m0 = re.match(r'^(.*?)(\((?:g|l|s|aq)\))$', tok)
            if m0:
                tok, st = m0.group(1), m0.group(2)
            m = re.match(r'^(\d+(?:/\d+)?|½)([A-Z(\[].*)$', tok)
            if m:
                toks.append(m.group(1) + F(m.group(2)) + st)
            else:
                toks.append(F(tok) + st)
    return ' '.join(toks)


# Cambridge 9701 data-booklet style relative atomic masses
AR = {'H': 1.0, 'He': 4.0, 'Li': 6.9, 'Be': 9.0, 'B': 10.8, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'F': 19.0, 'Ne': 20.2, 'Na': 23.0,
      'Mg': 24.3, 'Al': 27.0, 'Si': 28.1, 'P': 31.0, 'S': 32.1, 'Cl': 35.5, 'Ar': 39.9, 'K': 39.1, 'Ca': 40.1, 'Ti': 47.9,
      'Cr': 52.0, 'Mn': 54.9, 'Fe': 55.8, 'Co': 58.9, 'Ni': 58.7, 'Cu': 63.5, 'Zn': 65.4, 'Br': 79.9, 'Sr': 87.6, 'Ag': 107.9,
      'Sn': 118.7, 'I': 126.9, 'Ba': 137.3, 'Pb': 207.2}


def _atoms(s):
    stack = [{}]
    i = 0
    while i < len(s):
        c = s[i]
        if c == '(':
            stack.append({}); i += 1
        elif c == ')':
            i += 1
            m = re.match(r'\d+', s[i:])
            k = int(m.group()) if m else 1
            i += len(m.group()) if m else 0
            top = stack.pop()
            for el, n in top.items():
                stack[-1][el] = stack[-1].get(el, 0) + n * k
        else:
            m = re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
            if not m:
                i += 1
                continue
            el, n = m.group(1), int(m.group(2) or 1)
            stack[-1][el] = stack[-1].get(el, 0) + n
            i += len(m.group())
    return stack[0]


def atoms(s):
    s = s.split('^')[0]
    tot = {}
    for part in s.split('.'):
        m = re.match(r'^(\d*)(.*)$', part)
        k = int(m.group(1) or 1)
        for el, n in _atoms(m.group(2)).items():
            tot[el] = tot.get(el, 0) + n * k
    return tot


def Mr(s):
    return sum(AR[el] * n for el, n in atoms(s).items())


def g3(x):
    """3 s.f. string (exact halves round up, as a mark scheme would)."""
    if x == 0:
        return '0'
    return sf(x * (1 + 1e-12), 3) if x > 0 else '−' + sf(-x * (1 + 1e-12), 3)


def g4(x):
    return sf(x * (1 + 1e-12), 4) if x > 0 else '−' + sf(-x * (1 + 1e-12), 4)


def r3(x):
    return float(g3(x).replace(',', '').replace('−', '-'))


def mr1(x):
    """Mr to 1 d.p."""
    return f'{x:.1f}'


def sgn(x, dp=0):
    """Signed kJ value with Unicode minus: +52 / −286."""
    v = round(x, dp)
    s = f'{abs(v):.{dp}f}' if dp else str(int(abs(v)))
    return ('−' if v < 0 else '+') + s


def cap(s):
    return s[0].upper() + s[1:]


def art(word):
    return ('an ' if word[0].lower() in 'aeiou' else 'a ') + word


def mc(r, stem, correct, pool, key):
    try:
        o, a = mcq(r, correct, [p for p in pool if p != correct])
    except ValueError:
        return None
    return {'stem': stem, 'options': o, 'answer': a, 'key': key, 'marks': 1}


def nmc(r, stem, val, wrong, unit, key, f=g3):
    try:
        o, a = num_mcq(r, val, wrong, fmtf=f, unit=unit)
    except ValueError:
        return None
    return {'stem': stem, 'options': o, 'answer': a, 'key': key, 'marks': 1}


def who(r):
    return f'{person(r)}, a student in {city(r)},'


LABS = ['a school laboratory', 'a college laboratory', 'a quality-control laboratory', 'an AS practical class', 'a university teaching laboratory', 'a research laboratory']


def lab(r):
    return r.choice(LABS)


def P(r, intro):
    """Fill {p}, {p2}, {c}, {lab} in an intro string."""
    a, b = two_people(r)
    return intro.format(p=a, p2=b, c=city(r), lab=lab(r))


def c4reg(t, fn, c3=True):
    """Register a compose-based structured question for C4 (and C3 D3-5)."""
    t.add('C4', (2, 3, 4, 5), 'multi_step')(fn)
    if c3:
        t.add('C3', (3, 4, 5), 'multi_step')(fn)
    return fn


def c2mix(t, intros, extra=()):
    """C2 structured item: scenario intro + 1-3 explain parts drawn from the topic's fixed C2 entries (+ extra)."""
    def fn(r, D):
        ents = [e for e, _ in getattr(t, 'entries', {}).get('C2', [])] + list(extra)
        parts = [(lambda e: (lambda r: (e[0], e[1], e[2])))(e) for e in ents]
        return compose(r, P(r, r.choice(intros)), parts, k=(1, 2, 3), keep_order=False, type_='explain')
    fn.__name__ = 'c2mix'
    t.add('C2', (2, 3, 4), 'explain')(fn)
    return fn


ERR_FRAMES = ['{p} writes in a revision note: "{s}" Identify the error in this statement and give the correct version.',
              'In a test answer, {p} states: "{s}" Explain why this statement is incorrect.',
              'A student in {c} claims that {s2} Is the student correct? Explain your answer.',
              '"{s}" Comment on this statement made by a student, correcting any error.']


def errs(t, rows, D=(2, 3, 4)):
    """Spot-the-error C2 items: rows of (incorrect statement, correction)."""
    def fn(r, D_):
        s, fix = r.choice(rows)
        fr = r.choice(ERR_FRAMES)
        s2 = s[0].lower() + s[1:]
        stem = fr.format(p=person(r), c=city(r), s=s, s2=s2)
        return {'stem': stem, 'answer': 'The statement is incorrect. ' + fix, 'key': 'identifies the error [1]; correct chemistry stated with reason [1]', 'type': 'explain'}
    fn.__name__ = 'errs'
    t.add('C2', D, 'explain')(fn)
    return fn


_MK = re.compile(r'\[(\d+)\]')


def _wrap(fn):
    def w(r, D):
        q = fn(r, D)
        if q is None:
            return None
        if 'marks' not in q:
            if q.get('options'):
                q['marks'] = 1
            else:
                m = [int(x) for x in _MK.findall(q.get('key', ''))]
                if m:
                    q['marks'] = max(1, min(20, sum(m)))
        return q
    w.__name__ = getattr(fn, '__name__', 'tpl')
    return w


def finalize():
    for topics in CHAPTERS.values():
        for t in topics:
            for tp in t.templates:
                if not getattr(tp, '_wrapped', False):
                    tp.fn = _wrap(tp.fn)
                    tp._wrapped = True


def isotope(A, sym, ch=0):
    """Nuclide notation: ³⁷Cl⁻, ²⁷Al³⁺."""
    c = ''
    if ch:
        c = (str(abs(ch)) if abs(ch) > 1 else '') + ('+' if ch > 0 else '-')
    return sup(A) + sym + c.translate(_SUPT)


def ion(sym, ch):
    c = (str(abs(ch)) if abs(ch) > 1 else '') + ('+' if ch > 0 else '-')
    return F(sym) + c.translate(_SUPT)


# ===================================================================== Ch1 Atomic structure; atoms, molecules and stoichiometry
# ---------------------------------------------------------- 1.1 particles in the atom
BEAM = [  # label, charge, relative mass
    ('protons', 1, 1), ('¹H⁺ ions', 1, 1), ('²H⁺ ions', 1, 2), ('³H⁺ ions', 1, 3), ('⁴He²⁺ ions (α-particles)', 2, 4), ('⁴He⁺ ions', 1, 4),
    ('³He²⁺ ions', 2, 3), ('⁶Li⁺ ions', 1, 6), ('⁷Li⁺ ions', 1, 7), ('¹²C⁶⁺ ions', 6, 12), ('¹⁶O²⁺ ions', 2, 16), ('⁶Li³⁺ ions', 3, 6),
]

t1a = topic('Particles in the atom: relative charge and mass; behaviour of protons, neutrons and electrons in an electric field', 'particles in the atom: relative charge and mass', 'electric field')
t1a.fixed('C1', (1, 2), [
    ('What is the relative mass of an electron, compared with a proton of relative mass 1?', '1/1836', 'Electron relative mass ≈ 1/1836 (negligible); proton 1; neutron 1.', ['1', '0', '1/18']),
    ('Which particle has a relative charge of 0 and a relative mass of 1?', 'neutron', 'Neutron: charge 0, mass 1. Proton: +1, 1. Electron: −1, 1/1836.', ['proton', 'electron', 'positron']),
    ('A beam of neutrons passes between two charged plates. What happens to the beam?', 'It is not deflected', 'Neutrons are uncharged, so the electric field exerts no force on them.', ['It is deflected towards the positive plate', 'It is deflected towards the negative plate', 'It is slowed down and stops']),
    ('Towards which plate is a beam of electrons deflected?', 'the positive plate', 'Electrons are negatively charged and are attracted to the positive plate.', ['the negative plate', 'neither plate', 'first one plate then the other']),
    ('Where is almost all of the mass of an atom concentrated?', 'in the nucleus', 'Protons and neutrons (each relative mass 1) are in the tiny nucleus; electrons have negligible mass.', ['in the electron shells', 'evenly through the atom', 'in the outermost shell']),
    ('Which statement about protons and electrons in an electric field is correct?', 'Electrons are deflected much more than protons, in the opposite direction', 'Same size charge but the electron mass is 1/1836 of a proton, so its deflection is far greater; opposite charges deflect opposite ways.',
     ['Protons are deflected more than electrons, in the same direction', 'Both are deflected equally in opposite directions', 'Neither is deflected because atoms are neutral']),
    ('State the relative charge and relative mass of a proton.', 'Relative charge +1; relative mass 1.', '[1]'),
])
t1a.fixed('C2', (2, 3, 4), [
    ('Explain why a beam of electrons is deflected through a much larger angle than a beam of protons in the same electric field.', 'The charges are equal in size, but an electron has about 1/1836 of the mass of a proton, so its charge-to-mass ratio is much larger and it is deflected more.', 'same size charge; much smaller mass / larger charge-to-mass ratio [2]'),
    ('Explain why protons and electrons are deflected in opposite directions between charged plates.', 'They have opposite charges: protons (+) are attracted to the negative plate and electrons (−) to the positive plate.', 'opposite charges; attraction to oppositely charged plate [2]'),
    ('Explain why an atom is electrically neutral even though it contains charged particles.', 'It contains equal numbers of protons (+1) and electrons (−1), so the charges cancel; neutrons are uncharged.', 'equal numbers of p and e; charges cancel [2]'),
    ('Suggest why ²H⁺ ions are deflected less than ¹H⁺ ions in the same electric field.', 'Both have charge +1 but ²H⁺ has twice the mass, so its charge-to-mass ratio is halved and it is deflected less (about half the angle).', 'same charge; greater mass so smaller charge/mass ratio [2]'),
    ('Describe the structure of an atom in terms of the positions of the sub-atomic particles.', 'A very small, dense nucleus containing protons and neutrons is surrounded by electrons in shells (energy levels); most of the atom is empty space.', 'nucleus with p and n; electrons in shells around it [2]'),
])
errs(t1a, [
    ('Neutrons are deflected towards the negative plate because they are neutral.', 'Neutrons have no charge, so they experience no force in an electric field and are not deflected.'),
    ('Electrons are deflected less than protons because they are smaller.', 'Electrons are deflected MORE: same size charge but much smaller mass gives a larger charge-to-mass ratio.'),
    ('Most of the mass of an atom is due to its electrons.', 'Electrons have negligible mass (1/1836); the mass is in the nucleus (protons and neutrons).'),
    ('An α-particle (He²⁺) is deflected more than a proton because it has a larger charge.', 'Deflection depends on charge/mass: He²⁺ has 2/4 = 0.5 compared with 1/1 for a proton, so it is deflected less (about half).'),
])
c2mix(t1a, ['{p} is studying how beams of sub-atomic particles behave between two charged plates.', 'A textbook in {c} describes the sub-atomic particles in an atom.', 'In {lab}, a demonstration shows beams of charged particles passing through an electric field.'])


@t1a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1a_defl(r, D):
    a, b = r.sample(BEAM, 2)
    th = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    ra, rb = a[1] / a[2], b[1] / b[2]
    new = th * rb / ra
    if D == 1:
        return mc(r, f'Which beam is deflected most in an electric field: {a[0]} or {b[0]}?', a[0] if ra > rb else b[0] if rb > ra else 'they are deflected equally', [a[0], b[0], 'they are deflected equally', 'neither beam is deflected'],
                  f'Deflection ∝ charge/mass: {a[0]} {sf(ra)}, {b[0]} {sf(rb)}.')
    stem = f'A beam of {a[0]} is deflected through an angle of {th}° when it passes between two charged plates. Calculate the angle through which a beam of {b[0]}, travelling at the same speed, would be deflected by the same plates.'
    key = f'angle ∝ charge/mass [1]; {a[0]}: {a[1]}/{a[2]}, {b[0]}: {b[1]}/{b[2]} [1]; angle = {th} × ({b[1]}/{b[2]}) ÷ ({a[1]}/{a[2]}) = {g3(new)}° [1]'
    if D >= 4:
        stem += ' State and explain the direction of deflection compared with an electron beam.'
        key += '; both positive so deflected towards the negative plate, opposite to electrons [1]'
    return {'stem': stem, 'answer': f'{g3(new)}°' + ('; towards the negative plate (opposite direction to electrons)' if D >= 4 else ''), 'key': key}


def t1a_c4(r, D):
    a, b = r.sample(BEAM, 2)
    th = r.choice([3, 4, 6, 8])
    intro = P(r, r.choice(['{p} sets up an experiment in which separate beams of protons, neutrons and electrons, all at the same speed, pass between two oppositely charged plates.',
                           'A physics–chemistry project in {c} studies how ions and sub-atomic particles move in an electric field.',
                           'In {lab}, beams of different particles are fired between two charged plates and the angles of deflection are measured.']))
    ra, rb = a[1] / a[2], b[1] / b[2]
    parts = [
        lambda r: ('Copy and complete a table giving the relative mass and relative charge of a proton, a neutron and an electron.', 'proton: 1, +1; neutron: 1, 0; electron: 1/1836, −1', '[2]'),
        lambda r: ('State which beam is not deflected and explain why.', 'Neutrons — they have no charge so the electric field exerts no force on them.', '[2]'),
        lambda r: ('Explain why the electron beam is deflected through a larger angle than the proton beam and in the opposite direction.', 'Equal size, opposite charge; much smaller mass (1/1836) so larger charge-to-mass ratio; attracted to the positive plate.', '[3]'),
        lambda r: (f'A beam of {a[0]} is deflected by {th}°. Calculate the angle of deflection of {b[0]} under the same conditions.', f'{g3(th * rb / ra)}°', f'angle ∝ charge/mass; {th} × {sf(rb)}/{sf(ra)} = {g3(th * rb / ra)}° [2]'),
        lambda r: ('Predict the effect on the deflection of the proton beam of increasing the voltage across the plates.', 'Larger deflection, because the electric field and so the force on each proton is greater.', '[1]'),
        lambda r: ('Suggest why a beam of ²H⁺ ions could be used to distinguish deuterium from ¹H⁺.', '²H⁺ has twice the mass and the same charge, so it is deflected through half the angle.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t1a, t1a_c4)

# ---------------------------------------------------------- 1.2 isotopes, nucleon number, radii
EL = {  # symbol: (name, Z)
    'H': ('hydrogen', 1), 'He': ('helium', 2), 'Li': ('lithium', 3), 'Be': ('beryllium', 4), 'B': ('boron', 5), 'C': ('carbon', 6), 'N': ('nitrogen', 7), 'O': ('oxygen', 8),
    'F': ('fluorine', 9), 'Ne': ('neon', 10), 'Na': ('sodium', 11), 'Mg': ('magnesium', 12), 'Al': ('aluminium', 13), 'Si': ('silicon', 14), 'P': ('phosphorus', 15),
    'S': ('sulfur', 16), 'Cl': ('chlorine', 17), 'Ar': ('argon', 18), 'K': ('potassium', 19), 'Ca': ('calcium', 20), 'Sc': ('scandium', 21), 'Ti': ('titanium', 22),
    'V': ('vanadium', 23), 'Cr': ('chromium', 24), 'Mn': ('manganese', 25), 'Fe': ('iron', 26), 'Co': ('cobalt', 27), 'Ni': ('nickel', 28), 'Cu': ('copper', 29),
    'Zn': ('zinc', 30), 'Ga': ('gallium', 31), 'Ge': ('germanium', 32), 'As': ('arsenic', 33), 'Se': ('selenium', 34), 'Br': ('bromine', 35), 'Kr': ('krypton', 36),
    'Rb': ('rubidium', 37), 'Sr': ('strontium', 38), 'Ag': ('silver', 47), 'I': ('iodine', 53), 'Cs': ('caesium', 55), 'Ba': ('barium', 56), 'U': ('uranium', 92),
}
NUCLIDES = [('H', 1, (1, 0)), ('H', 2, (1, 0)), ('H', 3, (1,)), ('Li', 6, (1, 0)), ('Li', 7, (1, 0)), ('B', 11, (0, 3)), ('C', 12, (0,)), ('C', 13, (0,)), ('C', 14, (0,)),
            ('N', 14, (0, -3)), ('N', 15, (-3,)), ('O', 16, (0, -2)), ('O', 18, (0, -2)), ('F', 19, (-1,)), ('Na', 23, (1, 0)), ('Mg', 24, (2, 0)), ('Mg', 26, (2,)),
            ('Al', 27, (3, 0)), ('S', 32, (-2, 0)), ('S', 34, (-2,)), ('Cl', 35, (-1, 0)), ('Cl', 37, (-1, 0)), ('K', 39, (1,)), ('K', 41, (1,)), ('Ca', 40, (2, 0)),
            ('Ca', 44, (2,)), ('Fe', 56, (2, 3, 0)), ('Fe', 54, (2, 3)), ('Cu', 63, (2, 1)), ('Cu', 65, (2, 1)), ('Zn', 64, (2,)), ('Br', 79, (-1, 0)), ('Br', 81, (-1,)),
            ('Rb', 85, (1,)), ('Sr', 88, (2,)), ('Ag', 107, (1,)), ('Ag', 109, (1,)), ('I', 127, (-1, 0)), ('Ba', 138, (2,)), ('Ti', 48, (4, 2)), ('Mn', 55, (2,)), ('U', 235, (0,)), ('U', 238, (0,))]
ISOEL = [  # isoelectronic series (symbol, charge)
    [('N', -3), ('O', -2), ('F', -1), ('Na', 1), ('Mg', 2), ('Al', 3)],
    [('P', -3), ('S', -2), ('Cl', -1), ('K', 1), ('Ca', 2)],
]
RAD_PAIRS = [  # (bigger, smaller, reason)
    ('Na', 'Mg', 'across a period: Mg has more protons (greater nuclear charge) but similar shielding, so electrons are pulled closer'),
    ('Mg', 'Si', 'across Period 3 nuclear charge increases with similar shielding'), ('Al', 'Cl', 'across Period 3 nuclear charge increases with similar shielding'),
    ('K', 'Na', 'down a group there is an extra shell of electrons, further from the nucleus and with more shielding'),
    ('Ca', 'Mg', 'down Group 2 there is an extra occupied shell'), ('Br', 'Cl', 'down Group 17 there is an extra occupied shell'),
    ('Li', 'F', 'across Period 2 nuclear charge increases with similar shielding'), ('S', 'O', 'down Group 16 there is an extra occupied shell'),
]

t1b = topic('Isotopes, nucleon number and atomic and ionic radii trends', 'isotopes, nucleon number', 'atomic and ionic radii')
t1b.fixed('C1', (1, 2), [
    ('What are isotopes?', 'atoms of the same element with different numbers of neutrons', 'Isotopes: same proton (atomic) number, different neutron number, so different nucleon (mass) number.', ['atoms with the same nucleon number but different proton numbers', 'atoms of different elements with the same number of neutrons', 'ions of the same element with different charges']),
    ('Why do isotopes of the same element have the same chemical properties?', 'They have the same electronic configuration', 'Chemistry depends on electrons; isotopes have the same number of protons and electrons.', ['They have the same mass', 'They have the same number of neutrons', 'They have the same density']),
    ('Which property differs between ³⁵Cl and ³⁷Cl?', 'density of the gas', 'Physical properties depending on mass (density, rate of diffusion) differ; chemical properties do not.', ['number of electrons', 'number of protons', 'reaction with sodium']),
    ('What is meant by the nucleon number of an atom?', 'the total number of protons and neutrons in the nucleus', 'Nucleon (mass) number A = protons + neutrons.', ['the number of protons only', 'the number of neutrons only', 'the number of protons and electrons']),
    ('How does the radius of a positive ion compare with the radius of its atom?', 'The ion is smaller', 'Losing the outer shell and fewer electrons per proton means the remaining electrons are held closer.', ['The ion is larger', 'They are the same', 'It depends on the number of neutrons']),
    ('How does the radius of a negative ion compare with the radius of its atom?', 'The ion is larger', 'Extra electron(s) increase repulsion between electrons with the same nuclear charge, so the ion expands.', ['The ion is smaller', 'They are the same', 'It is always exactly double']),
    ('State the trend in atomic radius across Period 3 from sodium to chlorine.', 'Atomic radius decreases.', '[1]'),
])
t1b.fixed('C2', (2, 3, 4), [
    ('Explain why atomic radius decreases across Period 3.', 'Nuclear charge (number of protons) increases while shielding stays roughly the same (same number of inner shells), so the outer electrons are pulled closer to the nucleus.', 'increasing nuclear charge; similar shielding / same shell [2]'),
    ('Explain why atomic radius increases down a group.', 'Each element has an extra occupied shell, so the outer electrons are further from the nucleus and more shielded, outweighing the increased nuclear charge.', 'extra shell/further away; more shielding [2]'),
    ('Explain why a sodium ion, Na⁺, is much smaller than a sodium atom.', 'Na⁺ has lost its outer (3s) shell, so it has one fewer shell; also the 11 protons now attract only 10 electrons, so they are held closer.', 'one fewer shell; same nuclear charge on fewer electrons [2]'),
    ('Explain why a chloride ion, Cl⁻, is larger than a chlorine atom.', 'Cl⁻ has an extra electron in the same outer shell; increased repulsion between electrons and the same nuclear charge (17 protons for 18 electrons) means the electron cloud expands.', 'extra electron, more repulsion; same nuclear charge [2]'),
    ('Explain why ³⁵Cl and ³⁷Cl react in the same way with sodium.', 'Both have 17 protons and 17 electrons with the same electronic configuration; chemical reactions involve electrons, not neutrons.', 'same electronic configuration; reactions depend on electrons [2]'),
])
errs(t1b, [
    ('Isotopes have the same number of neutrons but different numbers of protons.', 'Isotopes have the same number of protons and different numbers of neutrons.'),
    ('Atomic radius increases across a period because more electrons are added.', 'Radius decreases across a period: nuclear charge increases while electrons enter the same shell with similar shielding.'),
    ('Mg²⁺ is larger than Na⁺ because magnesium has more protons.', 'Mg²⁺ is smaller: the ions are isoelectronic and Mg²⁺ has the greater nuclear charge (12 vs 11 protons) pulling the same 10 electrons closer.'),
    ('The ³⁷Cl isotope has 37 protons.', '³⁷Cl has 17 protons and 20 neutrons; 37 is the nucleon number.'),
])
c2mix(t1b, ['{p} is comparing data on the sizes of atoms and ions in a data book.', 'A student in {c} is revising isotopes and radii for an AS test.'])


@t1b.add('C3', (1, 2, 3, 4), 'numerical')
def t1b_count(r, D):
    sym, A, chs = r.choice(NUCLIDES)
    ch = r.choice(chs)
    Z = EL[sym][1]
    p, n, e = Z, A - Z, Z - ch
    sp = isotope(A, sym, ch)
    if D == 1:
        what = r.choice(['neutrons', 'electrons'])
        val = n if what == 'neutrons' else e
        return nmc(r, f'How many {what} are there in one {sp} {"ion" if ch else "atom"}?', val, [p, A, n if what == 'electrons' else e, val + 1, val - 1, Z + ch], '', f'{sp}: {p} protons, {n} neutrons, {e} electrons.', f=str)
    if D <= 3:
        return {'stem': f'State the number of protons, neutrons and electrons in the {"ion" if ch else "atom"} {sp}.', 'answer': f'{p} protons, {n} neutrons, {e} electrons',
                'key': f'protons = Z = {p} [1]; neutrons = A − Z = {A} − {Z} = {n} [1]' + (f'; electrons = {Z} − ({ch:+d}) = {e} [1]' if ch else f'; electrons = {e} [1]')}
    # D4: identify a species from particle counts
    return {'stem': f'A species X has {p} protons, {n} neutrons and {e} electrons. Use the Periodic Table to identify X and write its full symbol, showing nucleon number, proton number and charge.',
            'answer': f'{EL[sym][0]}: {sp} (proton number {Z})', 'key': f'Z = {p} identifies {EL[sym][0]} [1]; A = {p} + {n} = {A} [1]; charge = {p} − {e} = {ch:+d} [1]; correct symbol {sp} [1]'}


@t1b.add('C2', (2, 3, 4), 'explain')
def t1b_isoel(r, D):
    ser = r.choice(ISOEL)
    k = 2 if D <= 2 else 3
    pick = r.sample(ser, k)
    order = sorted(pick, key=lambda x: EL[x[0]][1])  # smaller Z -> larger radius
    names = ', '.join(ion(s, c) for s, c in pick)
    big = ' > '.join(ion(s, c) for s, c in order)
    ne = EL[pick[0][0]][1] - pick[0][1]
    return {'stem': f'The species {names} all have {ne} electrons. Place them in order of decreasing radius and explain the order.', 'answer': f'{big}. They are isoelectronic, so the species with more protons (greater nuclear charge) attracts the same number of electrons more strongly and is smaller.',
            'key': 'correct order [1]; same number of electrons / isoelectronic [1]; greater nuclear charge pulls electrons closer [1]' if D >= 3 else 'correct order [1]; greater nuclear charge, same electrons [1]'}


@t1b.add('C2', (2, 3), 'explain')
def t1b_rad(r, D):
    big, small, why = r.choice(RAD_PAIRS)
    if r.random() < 0.5:
        return mc(r, f'Which atom has the larger atomic radius, {EL[big][0]} or {EL[small][0]}?', EL[big][0], [EL[small][0], 'they are the same size', 'it cannot be predicted without the nucleon number'], f'{EL[big][0]} is larger: {why}.')
    return {'stem': f'Explain why {EL[big][0]} atoms are larger than {EL[small][0]} atoms.', 'answer': cap(why) + '.', 'key': 'correct comparison of nuclear charge or shells [1]; effect on attraction for outer electrons [1]'}


def t1b_c4(r, D):
    sym = r.choice(['Cl', 'Mg', 'Br', 'Cu', 'Fe'])
    isos = [x for x in NUCLIDES if x[0] == sym]
    a, b = isos[0], isos[1]
    Z = EL[sym][1]
    intro = P(r, r.choice([f'Naturally occurring {EL[sym][0]} contains the isotopes {isotope(a[1], sym)} and {isotope(b[1], sym)}.',
                           f'{{p}} is researching the isotopes of {EL[sym][0]}, {isotope(a[1], sym)} and {isotope(b[1], sym)}, for a project in {{c}}.']))
    ch = [c for c in a[2] if c][0] if any(a[2]) else 0
    parts = [
        lambda r: ('Define the term isotopes.', 'Atoms of the same element with the same number of protons but different numbers of neutrons.', '[1]'),
        lambda r: (f'State the number of protons, neutrons and electrons in an atom of each isotope.', f'{isotope(a[1], sym)}: {Z} p, {a[1] - Z} n, {Z} e; {isotope(b[1], sym)}: {Z} p, {b[1] - Z} n, {Z} e', '[2]'),
        lambda r: ('Explain why the two isotopes have the same chemical properties.', 'Same number of electrons / same electronic configuration; chemical reactions involve electrons.', '[2]'),
        lambda r: ('State one physical property that differs between the isotopes.', 'Density / mass / rate of diffusion (of the element or its compounds).', '[1]'),
        (lambda r: (f'Compare the radius of the {ion(sym, ch)} ion with that of the {EL[sym][0]} atom, and explain.', ('The ion is smaller: it has lost electrons (outer shell), so the same nuclear charge holds fewer electrons more closely.' if ch > 0 else 'The ion is larger: extra electron(s) increase repulsion while the nuclear charge is unchanged.'), '[2]')) if ch else (lambda r: None),
        lambda r: (f'State how the atomic radius of {EL[sym][0]} compares with that of the element directly above it in the Periodic Table, giving a reason.', 'Larger: one more occupied shell, outer electrons further from the nucleus and more shielded.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t1b, t1b_c4)

# ---------------------------------------------------------- 1.3 relative masses and mass spectra
SPECTRA = [  # element, [(isotopic mass, % abundance)]
    ('Cl', [(35, 75.8), (37, 24.2)]), ('Mg', [(24, 79.0), (25, 10.0), (26, 11.0)]), ('Cu', [(63, 69.2), (65, 30.8)]), ('Br', [(79, 50.7), (81, 49.3)]),
    ('B', [(10, 19.9), (11, 80.1)]), ('Li', [(6, 7.5), (7, 92.5)]), ('Si', [(28, 92.2), (29, 4.7), (30, 3.1)]), ('Ne', [(20, 90.5), (21, 0.3), (22, 9.2)]),
    ('Rb', [(85, 72.2), (87, 27.8)]), ('Ga', [(69, 60.1), (71, 39.9)]), ('Ag', [(107, 51.8), (109, 48.2)]), ('K', [(39, 93.3), (41, 6.7)]),
    ('Sr', [(84, 0.6), (86, 9.9), (87, 7.0), (88, 82.5)]), ('Zn', [(64, 49.2), (66, 27.7), (67, 4.0), (68, 18.5), (70, 0.6)]),
]
EL['Ga'] = ('gallium', 31)
MRCPDS = ['H2O', 'CO2', 'NH3', 'CH4', 'C2H5OH', 'H2SO4', 'CaCO3', 'NaOH', 'MgCl2', 'Al2(SO4)3', 'CuSO4.5H2O', 'Ca(OH)2', 'KMnO4', 'K2Cr2O7', 'Na2CO3.10H2O', 'C6H12O6', 'Fe2O3', '(NH4)2SO4', 'Mg(NO3)2', 'CH3COOH', 'Ba(OH)2', 'NaHCO3', 'C3H8', 'Pb(NO3)2']

t1c = topic('Relative atomic, isotopic and molecular mass; calculating Ar from mass spectra', 'relative atomic, isotopic and molecular mass', 'mass spectra')
t1c.fixed('C1', (1, 2), [
    ('Relative atomic mass is defined relative to which standard?', 'one-twelfth of the mass of an atom of carbon-12', 'Ar = weighted mean mass of an atom ÷ (1/12 × mass of one ¹²C atom).', ['the mass of one hydrogen atom', 'one-sixteenth of the mass of an oxygen-16 atom', 'the mass of one proton']),
    ('What is meant by the relative isotopic mass of an isotope?', 'the mass of one atom of the isotope relative to 1/12 of the mass of a carbon-12 atom', 'Relative isotopic mass applies to a single isotope; Ar is the weighted mean of all isotopes.', ['the weighted mean mass of all the isotopes of the element', 'the number of neutrons in the isotope', 'the mass of one mole of the element']),
    ('In a mass spectrum of an element, what does the height of each peak show?', 'the relative abundance of that isotope', 'x-axis: m/e (mass/charge); y-axis: relative abundance.', ['the mass of the isotope', 'the charge on the ion', 'the number of neutrons']),
    ('What is the relative molecular mass of a molecule?', 'the weighted mean mass of the molecule relative to 1/12 of the mass of a ¹²C atom', 'Mr = sum of Ar values of the atoms in the formula.', ['the mass of one mole of molecules in kilograms', 'the number of atoms in the molecule', 'the mass of the heaviest isotope in the molecule']),
    ('Chlorine contains ³⁵Cl and ³⁷Cl in the ratio 3 : 1. How many molecular-ion peaks does Cl₂ give in its mass spectrum?', '3', 'Cl₂⁺ at m/e 70 (³⁵Cl³⁵Cl), 72 (³⁵Cl³⁷Cl) and 74 (³⁷Cl³⁷Cl) in the ratio 9 : 6 : 1.', ['2', '4', '1']),
    ('State the meaning of the term relative formula mass.', 'The sum of the relative atomic masses of the atoms in the formula unit of a (giant) compound, relative to 1/12 of the mass of a ¹²C atom.', '[1]'),
])
t1c.fixed('C2', (2, 3, 4), [
    ('Explain why the relative atomic mass of chlorine, 35.5, is not a whole number.', 'Chlorine is a mixture of isotopes (³⁵Cl and ³⁷Cl); Ar is a weighted mean of their masses based on abundance.', 'mixture of isotopes; weighted mean [2]'),
    ('Explain why the Cl₂ molecular-ion peaks at m/e 70, 72 and 74 have heights in the ratio 9 : 6 : 1.', 'Probabilities with ³⁵Cl : ³⁷Cl = 3 : 1: ³⁵Cl–³⁵Cl = 3/4 × 3/4 = 9/16; ³⁵Cl–³⁷Cl (two ways) = 2 × 3/4 × 1/4 = 6/16; ³⁷Cl–³⁷Cl = 1/16.', 'identifies isotope combinations [1]; probabilities give 9 : 6 : 1 [1]'),
    ('Explain why Br₂ gives three molecular-ion peaks at m/e 158, 160 and 162 in a ratio of about 1 : 2 : 1.', '⁷⁹Br and ⁸¹Br are present in roughly equal amounts; ⁷⁹Br⁷⁹Br, ⁷⁹Br⁸¹Br (two ways) and ⁸¹Br⁸¹Br give 1 : 2 : 1.', 'about 1 : 1 isotopes [1]; mixed molecule can form two ways [1]'),
    ('Explain the difference between relative isotopic mass and relative atomic mass.', 'Relative isotopic mass is for one isotope; relative atomic mass is the weighted mean of the isotopic masses of all naturally occurring isotopes, both relative to 1/12 of ¹²C.', 'isotopic = single isotope [1]; Ar = weighted mean [1]'),
])
errs(t1c, [
    ('The relative atomic mass of chlorine is 36, the average of 35 and 37.', 'Ar is a weighted mean: (35 × 75.8 + 37 × 24.2)/100 = 35.5, because ³⁵Cl is about three times as abundant.'),
    ('Relative atomic mass is measured relative to the mass of a hydrogen atom.', 'The standard is 1/12 of the mass of a carbon-12 atom.'),
    ('Relative molecular mass has the unit g mol⁻¹.', 'Mr is a ratio and has no units; molar mass has units g mol⁻¹.'),
])
c2mix(t1c, ['{p} is analysing mass spectra recorded in {lab}.', 'A student in {c} is revising definitions of relative masses.'])


def _ar(iso):
    tot = sum(a for _, a in iso)
    return sum(m * a for m, a in iso) / tot


@t1c.add('C3', (1, 2, 3, 4), 'numerical')
def t1c_ar(r, D):
    sym, iso = r.choice(SPECTRA)
    if D >= 3 and r.random() < 0.6:
        # fictional sample with peak heights
        base = r.randint(40, 200)
        k = 2 if D == 3 else 3
        ms = sorted(r.sample(range(base, base + 5), k))
        hs = [r.choice([1.0, 2.0, 3.0, 4.0, 5.0, 6.5, 8.0, 12.0, 15.0]) for _ in ms]
        iso = list(zip(ms, hs))
        name = f'a sample of element X from {r.choice(["a meteorite", "a deep-sea mineral", "a volcanic rock", "a lunar soil sample"])}'
        lst = '; '.join(f'm/e {m}: relative height {sf(h, 2)}' for m, h in iso)
        val = _ar(iso)
        return {'stem': f'The mass spectrum of {name} shows the following peaks, each due to a singly charged ion: {lst}. Calculate the relative atomic mass of X to three significant figures.',
                'answer': g3(val), 'key': f'Σ(m × height) = {sf(sum(m * h for m, h in iso), 5)} [1]; ÷ total height {sf(sum(h for _, h in iso), 4)} [1]; Ar = {g3(val)} [1]'}
    val = _ar(iso)
    lst = ', '.join(f'{isotope(m, sym)} {a}%' for m, a in iso)
    if D == 1:
        return nmc(r, f'A sample of {EL[sym][0]} contains {lst}. What is its relative atomic mass?', val, [sum(m for m, _ in iso) / len(iso), iso[-1][0], iso[0][0] + 0.5, val + 0.6], '', f'Weighted mean = {g3(val)}.')
    return {'stem': f'Naturally occurring {EL[sym][0]} has the isotopic composition {lst}. Calculate the relative atomic mass of {EL[sym][0]} to three significant figures.',
            'answer': g3(val), 'key': f'Σ(mass × abundance) = {sf(sum(m * a for m, a in iso), 5)} [1]; ÷ 100, Ar = {g3(val)} [1]'}


@t1c.add('C3', (2, 3, 4, 5), 'numerical')
def t1c_abund(r, D):
    sym, iso = r.choice([x for x in SPECTRA if len(x[1]) == 2])
    m1, m2 = iso[0][0], iso[1][0]
    x = r.choice([12.5, 20, 25, 30, 37.5, 40, 45, 55, 60, 62.5, 70, 75, 80, 90])
    ar = (m1 * x + m2 * (100 - x)) / 100
    stem = f'A sample of {EL[sym][0]} from {r.choice(["a mineral spring", "a laboratory supplier", "an industrial process", "a geological survey"])} in {city(r)} contains only {isotope(m1, sym)} and {isotope(m2, sym)}. Its relative atomic mass is {sf(ar, 4)}. Calculate the percentage abundance of {isotope(m1, sym)}.'
    key = f'let % of {isotope(m1, sym)} = x: {m1}x + {m2}(100 − x) = {sf(ar * 100, 5)} [1]; {m2 - m1}x = {sf(m2 * 100 - ar * 100, 5)} [1]; x = {sf(x, 3)}% [1]'
    return {'stem': stem, 'answer': f'{sf(x, 3)}%', 'key': key}


@t1c.add('C1', (1, 2, 3))
def t1c_mr(r, D):
    f = r.choice(MRCPDS)
    M = Mr(f)
    return nmc(r, f'Use the relative atomic masses in the Periodic Table to find the relative formula mass of {F(f)}.', M, [M - 16, M + 18, M * 2 if M < 200 else M / 2, M - 1], '', f'Mr = {mr1(M)}.', f=mr1)


@t1c.add('C3', (3, 4, 5), 'numerical')
def t1c_dihal(r, D):
    sym, iso = r.choice([('Cl', [(35, 3), (37, 1)]), ('Br', [(79, 1), (81, 1)])])
    (m1, a1), (m2, a2) = iso
    t_ = a1 + a2
    p1, p2 = a1 / t_, a2 / t_
    peaks = [(2 * m1, p1 * p1), (m1 + m2, 2 * p1 * p2), (2 * m2, p2 * p2)]
    mn = min(h for _, h in peaks)
    rat = ' : '.join(sf(h / mn, 2) for _, h in peaks)
    return {'stem': f'{EL[sym][0].capitalize()} consists of {isotope(m1, sym)} and {isotope(m2, sym)} in the ratio {a1} : {a2}. Predict the m/e values of the peaks for the molecular ion {F(sym + "2")}⁺ and their relative heights. Explain your answer.',
            'answer': f'm/e {peaks[0][0]}, {peaks[1][0]}, {peaks[2][0]} in the ratio {rat}', 'key': f'three m/e values {peaks[0][0]}, {peaks[1][0]}, {peaks[2][0]} [1]; probabilities: {sf(p1, 2)}², 2 × {sf(p1, 2)} × {sf(p2, 2)}, {sf(p2, 2)}² [1]; ratio {rat} [1]'}


def t1c_c4(r, D):
    sym, iso = r.choice(SPECTRA[:12])
    val = _ar(iso)
    intro = P(r, r.choice([f'{{p}} records the mass spectrum of a sample of {EL[sym][0]} in {{lab}}. Peaks: ' + ', '.join(f'm/e {m} ({a}%)' for m, a in iso) + '.',
                           f'A forensic laboratory in {{c}} analyses a sample of {EL[sym][0]} using a mass spectrometer. The peaks are at ' + ', '.join(f'm/e {m} (abundance {a}%)' for m, a in iso) + '.']))
    parts = [
        lambda r: ('Define relative atomic mass.', 'The weighted mean mass of an atom of the element relative to 1/12 of the mass of an atom of carbon-12.', '[2]'),
        lambda r: ('Calculate the relative atomic mass of the element to three significant figures.', g3(val), f'Σ(m × %)/100 = {g3(val)} [2]'),
        lambda r: ('State what is plotted on each axis of a mass spectrum.', 'x-axis: mass-to-charge ratio (m/e); y-axis: relative abundance (intensity).', '[1]'),
        lambda r: ('Explain why each peak is due to a different isotope rather than a different element.', 'All peaks come from atoms of the same element (same proton number) that differ only in neutron number and so in mass.', '[1]'),
        lambda r: ('Suggest why a small peak may appear at half of one of the m/e values.', 'A doubly charged ion (2+) of that isotope has m/e equal to half its mass.', '[1]'),
        lambda r: (f'Calculate the relative formula mass of the chloride {F(sym + "Cl" + ("2" if sym in ("Mg", "Cu", "Sr", "Zn") else ""))}, using Ar(Cl) = 35.5 and your answer above.', g3(val + 35.5 * (2 if sym in ('Mg', 'Cu', 'Sr', 'Zn') else 1)), '[1]') if sym != 'Cl' else None,
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 5))


c4reg(t1c, t1c_c4)

# ---------------------------------------------------------- 1.4 mole, Avogadro, empirical and molecular formulae
EMP = [  # molecular formula, name
    ('C2H6', 'ethane'), ('C6H12', 'cyclohexane'), ('C2H4O2', 'ethanoic acid'), ('C6H12O6', 'glucose'), ('C4H10', 'butane'), ('N2O4', 'dinitrogen tetroxide'),
    ('P4O10', 'phosphorus(V) oxide'), ('C4H8O2', 'ethyl ethanoate'), ('C3H6O', 'propanone'), ('C8H18', 'octane'), ('H2O2', 'hydrogen peroxide'), ('B2H6', 'diborane'),
    ('C2H2', 'ethyne'), ('C6H6', 'benzene'), ('C3H6O2', 'propanoic acid'), ('C2H4Cl2', '1,2-dichloroethane'), ('C4H8', 'but-1-ene'), ('N2H4', 'hydrazine'),
    ('C3H8O', 'propan-1-ol'), ('S2Cl2', 'disulfur dichloride'), ('C2H6O2', 'ethane-1,2-diol'), ('C5H10O', 'pentan-2-one'),
]
SALTS = ['Fe2O3', 'Al2O3', 'Na2SO4', 'K2Cr2O7', 'MgSO4', 'CaCO3', 'NaHCO3', 'Cu2O', 'Fe3O4', 'KNO3', 'Ca3(PO4)2', 'Na2S2O3']
HYD = [('CuSO4', 'copper(II) sulfate', 5), ('MgSO4', 'magnesium sulfate', 7), ('ZnSO4', 'zinc sulfate', 7), ('FeSO4', 'iron(II) sulfate', 7), ('Na2CO3', 'sodium carbonate', 10),
       ('BaCl2', 'barium chloride', 2), ('Na2SO4', 'sodium sulfate', 10), ('CaCl2', 'calcium chloride', 6), ('CoCl2', 'cobalt(II) chloride', 6), ('MgCl2', 'magnesium chloride', 6)]
ORDER_EL = ['C', 'H', 'N', 'O', 'S', 'Cl', 'P', 'B']


def empirical(f):
    a = atoms(f)
    g = 0
    for v in a.values():
        g = math.gcd(g, v)
    return {k: v // g for k, v in a.items()}, g


def fstr(d):
    keys = sorted(d, key=lambda k: (ORDER_EL.index(k) if k in ORDER_EL else -1, k))
    return ''.join(k + (str(d[k]) if d[k] > 1 else '') for k in keys)


def pcts(f):
    a = atoms(f)
    M = Mr(f)
    return {k: round(AR[k] * v / M * 100, 1) for k, v in a.items()}


L_AV = 6.02e23

t1d = topic('The mole, Avogadro constant, empirical and molecular formulae', 'the mole, avogadro constant', 'empirical and molecular formulae')
t1d.fixed('C1', (1, 2), [
    ('What is the Avogadro constant?', 'the number of particles in one mole of a substance, 6.02 × 10²³ mol⁻¹', 'L = 6.02 × 10²³ mol⁻¹: the number of atoms in exactly 12 g of carbon-12.', ['the mass of one mole of a substance', 'the volume of one mole of gas at r.t.p.', 'the number of atoms in 1 g of hydrogen']),
    ('What is meant by the empirical formula of a compound?', 'the simplest whole-number ratio of atoms of each element in the compound', 'Molecular formula = actual numbers of atoms in a molecule; empirical = simplest ratio.', ['the actual number of atoms of each element in a molecule', 'the formula showing how atoms are bonded', 'the formula of one mole of the compound']),
    ('Which compound has the same empirical formula as ethanoic acid, C₂H₄O₂?', 'glucose, C₆H₁₂O₆', 'Both reduce to CH₂O.', ['ethanol, C₂H₆O', 'ethane, C₂H₆', 'propanoic acid, C₃H₆O₂']),
    ('A mole of a substance is defined as the amount containing the same number of particles as there are atoms in exactly …', '12 g of carbon-12', 'Definition of the mole based on ¹²C (now fixed by the value of L).', ['1 g of hydrogen', '16 g of oxygen', '22.4 dm³ of a gas']),
    ('Which sample contains the greatest number of atoms?', '1 mol of CH₄', '1 mol CH₄ has 5 mol atoms; 1 mol NH₃ 4 mol; 1 mol H₂O 3 mol; 1 mol O₂ 2 mol.', ['1 mol of NH₃', '1 mol of H₂O', '1 mol of O₂']),
    ('State the formula connecting amount of substance n, mass m and molar mass M.', 'n = m/M', '[1]'),
])
t1d.fixed('C2', (2, 3, 4), [
    ('Explain why the empirical formula and molecular formula of propanone, C₃H₆O, are the same.', 'The numbers of atoms 3 : 6 : 1 have no common factor, so the simplest ratio is the molecular formula itself.', 'no common factor [1]; simplest ratio equals actual numbers [1]'),
    ('Explain why 1 mol of hydrogen gas and 1 mol of helium gas contain different numbers of atoms.', 'Both contain 6.02 × 10²³ particles, but hydrogen exists as H₂ molecules (2 atoms each) whereas helium is monatomic, so H₂ has 1.20 × 10²⁴ atoms.', 'same number of particles [1]; H₂ diatomic so twice the atoms [1]'),
    ('Explain why the empirical formula alone is not enough to identify a molecular compound.', 'Many compounds share an empirical formula (e.g. CH₂O for methanal, ethanoic acid and glucose); Mr is needed to find the molecular formula.', 'several compounds share it [1]; need Mr [1]'),
    ('Explain how you would find the formula of a hydrated salt by heating.', 'Weigh, heat to constant mass to remove all water, reweigh; moles of water and anhydrous salt from masses give the ratio x.', 'heat to constant mass [1]; calculate mole ratio of water : anhydrous salt [1]'),
])
errs(t1d, [
    ('The empirical formula of hexane, C₆H₁₄, is CH₂.', 'Divide by the highest common factor 2: the empirical formula is C₃H₇.'),
    ('One mole of water contains 6.02 × 10²³ atoms.', 'One mole of water contains 6.02 × 10²³ molecules, i.e. 3 × 6.02 × 10²³ = 1.81 × 10²⁴ atoms.'),
    ('To find the empirical formula you divide each percentage by the atomic number.', 'Divide each mass (or %) by the relative atomic mass Ar, then by the smallest value.'),
])
c2mix(t1d, ['{p} is analysing an unknown compound in {lab}.', 'A student in {c} is checking calculations involving the mole.'])


@t1d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1d_emp(r, D):
    f, nm = r.choice(EMP)
    e, g = empirical(f)
    pc = pcts(f)
    lst = ', '.join(f'{k} {pc[k]}%' for k in sorted(pc, key=lambda k: ORDER_EL.index(k) if k in ORDER_EL else 9))
    ef = fstr(e)
    M = Mr(f)
    if D == 1:
        return mc(r, f'What is the empirical formula of {F(f)}?', F(ef), [F(f), F(fstr({k: v * 2 for k, v in e.items()})) if g != 2 else F(fstr({k: v * 3 for k, v in e.items()})), F(fstr({k: 1 for k in e})), F(fstr({k: v + 1 for k, v in e.items()}))], f'Divide by the highest common factor {g}: {F(ef)}.')
    if D == 2:
        return {'stem': f'A compound has the composition by mass {lst}. Calculate its empirical formula.', 'answer': F(ef),
                'key': f'divide % by Ar [1]; divide by smallest and round to whole numbers: {F(ef)} [1]'}
    return {'stem': f'Compound Y, used in {r.choice(["a dye works", "a pharmaceutical plant", "a fuel laboratory", "a university project"])} in {city(r)}, has the composition by mass {lst}. Its relative molecular mass is {mr1(M)}. Calculate the empirical formula and the molecular formula of Y.',
            'answer': f'empirical {F(ef)}; molecular {F(f)}', 'key': f'moles: % ÷ Ar [1]; ratio → {F(ef)} [1]; Mr(empirical) = {mr1(Mr(ef))} [1]; {mr1(M)}/{mr1(Mr(ef))} = {g} so {F(f)} [1]'}


@t1d.add('C3', (2, 3, 4), 'numerical')
def t1d_hyd(r, D):
    f, nm, x = r.choice(HYD)
    Ma = Mr(f)
    n = r.choice([0.0100, 0.0125, 0.0150, 0.0200, 0.0250, 0.0300, 0.0400])
    m_hyd = n * (Ma + 18.0 * x)
    m_an = n * Ma
    return {'stem': f'{who(r)} heats {sf(m_hyd, 3)} g of hydrated {nm}, {F(f)}·xH₂O, to constant mass. The anhydrous residue has a mass of {sf(m_an, 3)} g. Calculate the value of x.',
            'answer': f'x = {x}', 'key': f'mass of water = {sf(m_hyd - m_an, 3)} g; n(H₂O) = {sf((m_hyd - m_an) / 18.0, 3)} mol [1]; n({F(f)}) = {sf(m_an, 3)}/{mr1(Ma)} = {sf(m_an / Ma, 3)} mol [1]; ratio = {x} [1]'}


@t1d.add('C3', (1, 2, 3), 'numerical')
def t1d_moles(r, D):
    f = r.choice(MRCPDS + ['O2', 'N2', 'Cl2', 'CO2', 'SO2'])
    M = Mr(f)
    m = r.choice([0.5, 1.0, 2.0, 2.5, 4.0, 5.0, 8.0, 10.0, 12.5, 20.0, 25.0])
    n = m / M
    na = sum(atoms(f).values())
    if D == 1:
        return nmc(r, f'What amount, in mol, is present in {sf(m, 3)} g of {F(f)}?', n, [m * M, M / m, n * 2, n / 2], ' mol', f'n = m/M = {sf(m, 3)}/{mr1(M)}.')
    if D == 2:
        return {'stem': f'Calculate the number of molecules (or formula units) in {sf(m, 3)} g of {F(f)}. (L = 6.02 × 10²³ mol⁻¹)', 'answer': f'{sf(n * L_AV / 10 ** math.floor(math.log10(n * L_AV)), 3)} × 10{sup(math.floor(math.log10(n * L_AV)))}',
                'key': f'n = {sf(m, 3)}/{mr1(M)} = {g3(n)} mol [1]; × 6.02 × 10²³ [1]'}
    N = n * L_AV * na
    e = math.floor(math.log10(N))
    return {'stem': f'Calculate the total number of atoms in {sf(m, 3)} g of {F(f)}. (L = 6.02 × 10²³ mol⁻¹)', 'answer': f'{sf(N / 10 ** e, 3)} × 10{sup(e)}',
            'key': f'n = {g3(n)} mol [1]; × L gives formula units [1]; × {na} atoms per unit = {sf(N / 10 ** e, 3)} × 10{sup(e)} [1]'}


@t1d.add('C3', (4, 5), 'numerical')
def t1d_comb(r, D):
    hc = r.choice([('C3H8', 'propane'), ('C4H10', 'butane'), ('C2H6', 'ethane'), ('C5H12', 'pentane'), ('C6H14', 'hexane'), ('C2H4', 'ethene'), ('C3H6', 'propene'), ('C8H18', 'octane')])
    a = atoms(hc[0])
    n = r.choice([0.005, 0.01, 0.02, 0.025])
    mco2 = n * a['C'] * 44.0
    mh2o = n * a['H'] / 2 * 18.0
    e, g = empirical(hc[0])
    return {'stem': f'Complete combustion of a sample of hydrocarbon Z produced {sf(mco2, 3)} g of carbon dioxide and {sf(mh2o, 3)} g of water. Calculate the empirical formula of Z.' + (f' The relative molecular mass of Z is {mr1(Mr(hc[0]))}; deduce its molecular formula.' if D == 5 else ''),
            'answer': f'empirical {F(fstr(e))}' + (f'; molecular {F(hc[0])}' if D == 5 else ''),
            'key': f'n(C) = n(CO₂) = {sf(mco2, 3)}/44.0 = {sf(mco2 / 44, 3)} [1]; n(H) = 2 × {sf(mh2o, 3)}/18.0 = {sf(mh2o / 9, 3)} [1]; ratio C : H → {F(fstr(e))} [1]' + (f'; {mr1(Mr(hc[0]))}/{mr1(Mr(fstr(e)))} = {g} → {F(hc[0])} [1]' if D == 5 else '')}


def t1d_c4(r, D):
    f, nm = r.choice(EMP)
    e, g = empirical(f)
    pc = pcts(f)
    M = Mr(f)
    m = r.choice([1.5, 2.0, 3.0, 4.5, 6.0])
    intro = P(r, r.choice([f'{{p}} analyses an unknown liquid in {{lab}}. It has the composition by mass ' + ', '.join(f'{k} {pc[k]}%' for k in pc) + f' and Mr = {mr1(M)}.',
                           f'An environmental chemist in {{c}} isolates a pollutant with composition ' + ', '.join(f'{k} {pc[k]}%' for k in pc) + f'. Mass spectrometry shows Mr = {mr1(M)}.']))
    parts = [
        lambda r: ('Define the term empirical formula.', 'The simplest whole-number ratio of atoms of each element in a compound.', '[1]'),
        lambda r: ('Calculate the empirical formula.', F(fstr(e)), 'divide by Ar, then by smallest, whole-number ratio [2]'),
        lambda r: ('Deduce the molecular formula, showing your working.', F(f), f'Mr(empirical) = {mr1(Mr(fstr(e)))}; {mr1(M)}/{mr1(Mr(fstr(e)))} = {g} [2]'),
        lambda r: (f'Calculate the number of molecules in {m} g of the compound. (L = 6.02 × 10²³ mol⁻¹)', f'{sf(m / M * L_AV / 10 ** math.floor(math.log10(m / M * L_AV)), 3)} × 10{sup(math.floor(math.log10(m / M * L_AV)))}', f'n = {m}/{mr1(M)}; × L [2]'),
        lambda r: ('State the meaning of the term mole.', 'The amount of substance containing 6.02 × 10²³ particles (as many as there are atoms in 12 g of ¹²C).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2, 3))


c4reg(t1d, t1d_c4)

# ---------------------------------------------------------- 1.5 reacting masses, gas volumes, concentrations, titrations
RXN = [  # equation; gas species at r.t.p.
    'CaCO3 -> CaO + CO2', '2Mg + O2 -> 2MgO', 'Fe2O3 + 3CO -> 2Fe + 3CO2', 'CH4 + 2O2 -> CO2 + 2H2O', 'C3H8 + 5O2 -> 3CO2 + 4H2O', '2NaHCO3 -> Na2CO3 + H2O + CO2',
    '2Al + 3Cl2 -> 2AlCl3', 'N2 + 3H2 -> 2NH3', 'Zn + 2HCl -> ZnCl2 + H2', '2KClO3 -> 2KCl + 3O2', 'CaCO3 + 2HCl -> CaCl2 + H2O + CO2', 'Mg + 2HCl -> MgCl2 + H2',
    'C2H5OH + 3O2 -> 2CO2 + 3H2O', '4NH3 + 5O2 -> 4NO + 6H2O', '2Pb(NO3)2 -> 2PbO + 4NO2 + O2', 'TiCl4 + 2Mg -> Ti + 2MgCl2', '2Na + 2H2O -> 2NaOH + H2', 'Ca + 2H2O -> Ca(OH)2 + H2',
    'Fe2O3 + 2Al -> 2Fe + Al2O3', '2C4H10 + 13O2 -> 8CO2 + 10H2O', 'MgCO3 -> MgO + CO2', '2Mg(NO3)2 -> 2MgO + 4NO2 + O2',
]
GAS = {'O2', 'CO2', 'H2', 'NH3', 'N2', 'Cl2', 'NO', 'NO2', 'CH4', 'C3H8', 'CO', 'C4H10', 'SO2'}


def parse(eq):
    l, rt = eq.split(' -> ')
    def side(s):
        out = []
        for tok in s.split(' + '):
            m = re.match(r'^(\d*)(.*)$', tok)
            out.append((int(m.group(1) or 1), m.group(2)))
        return out
    return side(l), side(rt)


ACIDBASE = [  # acid, alkali, acid:alkali mole ratio a:b in equation, equation
    ('HCl', 'NaOH', 1, 1, 'HCl + NaOH -> NaCl + H2O'), ('H2SO4', 'NaOH', 1, 2, 'H2SO4 + 2NaOH -> Na2SO4 + 2H2O'), ('HNO3', 'KOH', 1, 1, 'HNO3 + KOH -> KNO3 + H2O'),
    ('HCl', 'Na2CO3', 2, 1, '2HCl + Na2CO3 -> 2NaCl + H2O + CO2'), ('H2SO4', 'KOH', 1, 2, 'H2SO4 + 2KOH -> K2SO4 + 2H2O'), ('CH3COOH', 'NaOH', 1, 1, 'CH3COOH + NaOH -> CH3COONa + H2O'),
    ('HCl', 'Ba(OH)2', 2, 1, '2HCl + Ba(OH)2 -> BaCl2 + 2H2O'), ('H2SO4', 'Na2CO3', 1, 1, 'H2SO4 + Na2CO3 -> Na2SO4 + H2O + CO2'), ('HNO3', 'Ca(OH)2', 2, 1, '2HNO3 + Ca(OH)2 -> Ca(NO3)2 + 2H2O'),
]
ANAME = {'HCl': 'hydrochloric acid', 'H2SO4': 'sulfuric acid', 'HNO3': 'nitric acid', 'CH3COOH': 'ethanoic acid', 'NaOH': 'sodium hydroxide', 'KOH': 'potassium hydroxide',
         'Na2CO3': 'sodium carbonate', 'Ba(OH)2': 'barium hydroxide', 'Ca(OH)2': 'calcium hydroxide'}

t1e = topic('Reacting masses, gas volumes, solution concentrations and titration calculations', 'reacting masses, gas volumes', 'titration calculations')
t1e.fixed('C1', (1, 2), [
    ('What volume does one mole of any gas occupy at room temperature and pressure?', '24.0 dm³', 'Molar gas volume at r.t.p. = 24.0 dm³ mol⁻¹ (24 000 cm³).', ['22.4 dm³', '1.00 dm³', '240 cm³']),
    ('What is the concentration of a solution containing 0.50 mol of solute in 250 cm³ of solution?', '2.0 mol dm⁻³', 'c = n/V = 0.50/0.250 = 2.0 mol dm⁻³.', ['0.125 mol dm⁻³', '0.50 mol dm⁻³', '125 mol dm⁻³']),
    ('In a titration, which apparatus is used to measure exactly 25.0 cm³ of the solution of unknown concentration?', 'a volumetric pipette', 'Pipette delivers a fixed volume; burette delivers the titrant.', ['a measuring cylinder', 'a beaker', 'a burette']),
    ('Which titres should be used to calculate the mean titre?', 'concordant titres, within 0.10 cm³ of each other', 'Discard the rough titre; average concordant results.', ['all titres including the rough one', 'only the largest titre', 'only the first accurate titre']),
    ('Why is the percentage yield of a reaction usually less than 100%?', 'some product is lost or side reactions occur', 'Losses on transfer/filtration, incomplete or reversible reactions, side reactions.', ['the law of conservation of mass is broken', 'the catalyst is used up', 'the molar mass changes']),
    ('State the formula connecting concentration, amount and volume of solution.', 'c = n/V (V in dm³)', '[1]'),
])
t1e.fixed('C2', (2, 3, 4), [
    ('Explain why the burette is rinsed with the solution it will contain rather than with water.', 'Water left in the burette would dilute the solution and change its concentration, making the titre too large.', 'water dilutes [1]; effect on titre [1]'),
    ('Explain the term limiting reagent.', 'The reactant that is completely used up first; it determines the maximum amount of product, the other reactant being in excess.', 'used up first [1]; determines amount of product [1]'),
    ('Explain why equal volumes of different gases at the same temperature and pressure contain the same number of molecules.', 'Gas molecules are far apart, so the volume depends on the number of molecules rather than their size (Avogadro’s law).', 'molecules far apart/size negligible [1]; volume depends on number [1]'),
    ('Explain why a back titration is used to find the amount of calcium carbonate in an eggshell.', 'CaCO₃ is insoluble and reacts slowly, so a known excess of acid is added and the unreacted acid is titrated with alkali; the acid used = total − excess.', 'insoluble/slow so direct titration impractical [1]; excess acid titrated [1]'),
])
errs(t1e, [
    ('In a titration calculation, the volume 25.0 cm³ is used directly in c = n/V to give the concentration in mol dm⁻³.', 'Convert to dm³ first: 25.0 cm³ = 0.0250 dm³.'),
    ('One mole of water occupies 24.0 dm³ at room temperature and pressure.', 'Water is a liquid at r.t.p.; 24.0 dm³ is the molar volume of gases only.'),
    ('In H₂SO₄ + 2NaOH, the moles of NaOH equal the moles of H₂SO₄.', 'The mole ratio is 1 : 2, so moles of NaOH are twice the moles of H₂SO₄.'),
])
c2mix(t1e, ['{p} carries out titrations in {lab}.', 'A chemical company in {c} uses reacting-mass calculations to plan production.'])


@t1e.add('C3', (1, 2, 3, 4), 'numerical')
def t1e_mass(r, D):
    eq = r.choice(RXN)
    L, R = parse(eq)
    a = r.choice([x for x in L if x[1] not in ('H2O',)])
    b = r.choice([x for x in R if x[1] not in ('H2O',)])
    ma = r.choice([1.2, 2.4, 3.6, 4.8, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0])
    na = ma / Mr(a[1])
    nb = na * b[0] / a[0]
    gas = b[1] in GAS
    if gas and D >= 2 and r.random() < 0.5:
        v = nb * 24.0
        return {'stem': f'For the reaction {E(eq)}, calculate the volume of {F(b[1])} at room temperature and pressure formed from {sf(ma, 3)} g of {F(a[1])} reacting completely.',
                'answer': f'{g3(v)} dm³', 'key': f'n({F(a[1])}) = {sf(ma, 3)}/{mr1(Mr(a[1]))} = {g3(na)} mol [1]; ratio {a[0]} : {b[0]} gives n({F(b[1])}) = {g3(nb)} mol [1]; V = {g3(nb)} × 24.0 = {g3(v)} dm³ [1]'}
    mb = nb * Mr(b[1])
    if D == 1:
        return nmc(r, f'For the reaction {E(eq)}, what mass of {F(b[1])} is formed from {sf(ma, 3)} g of {F(a[1])}?', mb, [ma * Mr(b[1]) / Mr(a[1]), mb * 2, mb / 2, ma], ' g', f'n ratio {a[0]} : {b[0]}; mass = {g3(mb)} g.')
    stem = f'Calculate the mass of {F(b[1])} formed when {sf(ma, 3)} g of {F(a[1])} reacts completely: {E(eq)}.'
    key = f'n({F(a[1])}) = {sf(ma, 3)}/{mr1(Mr(a[1]))} = {g3(na)} mol [1]; n({F(b[1])}) = {g3(nb)} mol [1]; mass = {g3(nb)} × {mr1(Mr(b[1]))} = {g3(mb)} g [1]'
    ans = f'{g3(mb)} g'
    if D >= 4:
        act = mb * r.choice([0.62, 0.7, 0.75, 0.8, 0.85, 0.9])
        stem += f' In practice {g3(act)} g was obtained. Calculate the percentage yield.'
        key += f'; % yield = {g3(act)}/{g3(mb)} × 100 = {g3(act / mb * 100)}% [1]'
        ans += f'; {g3(act / mb * 100)}%'
    return {'stem': stem, 'answer': ans, 'key': key}


@t1e.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1e_titr(r, D):
    acid, alk, ka, kb, eq = r.choice(ACIDBASE)
    cb = r.choice([0.100, 0.0500, 0.120, 0.150, 0.200, 0.0800])
    vb = 25.0
    nb = cb * vb / 1000
    na = nb * ka / kb
    titre = r.choice([18.5, 20.0, 21.6, 22.4, 23.8, 24.5, 26.2, 27.5, 19.6])
    ca = na / (titre / 1000)
    if D == 1:
        return nmc(r, f'What amount of {F(alk)} is present in 25.0 cm³ of a {sf(cb, 3)} mol dm⁻³ solution?', nb, [cb * 25.0, cb / 25.0, nb * 10, nb * 2], ' mol', f'n = cV = {sf(cb, 3)} × 0.0250.')
    stem = f'{who(r)} titrates 25.0 cm³ of {sf(cb, 3)} mol dm⁻³ {ANAME[alk]} with {ANAME[acid]}. The mean titre is {titre} cm³. The equation is {E(eq)}. Calculate the concentration of the acid.'
    key = f'n({F(alk)}) = {sf(cb, 3)} × 25.0/1000 = {g3(nb)} mol [1]; n({F(acid)}) = {g3(nb)} × {ka}/{kb} = {g3(na)} mol [1]; c = {g3(na)}/({titre}/1000) = {g3(ca)} mol dm⁻³ [1]'
    if D >= 4:
        trial = [titre + r.choice([0.5, 0.8, 1.1]), titre + 0.05, titre - 0.05, titre + 0.6]
        stem = (f'{who(r)} titrates 25.0 cm³ portions of {sf(cb, 3)} mol dm⁻³ {ANAME[alk]} with {ANAME[acid]}. Titres: rough {sf(trial[0], 3)} cm³, then {trial[1]:.2f}, {trial[2]:.2f} and {trial[3]:.2f} cm³. '
                f'The equation is {E(eq)}. Select suitable titres, calculate the mean titre and hence the concentration of the acid in mol dm⁻³ and in g dm⁻³.')
        mean = (trial[1] + trial[2]) / 2
        ca = na / (mean / 1000)
        key = f'concordant titres {trial[1]:.2f} and {trial[2]:.2f} (within 0.10 cm³), mean {mean:.2f} cm³ [1]; n({F(alk)}) = {g3(nb)} mol [1]; n(acid) = {g3(na)} mol [1]; c = {g3(ca)} mol dm⁻³ [1]; × Mr {mr1(Mr(acid))} = {g3(ca * Mr(acid))} g dm⁻³ [1]'
        return {'stem': stem, 'answer': f'mean {mean:.2f} cm³; {g3(ca)} mol dm⁻³; {g3(ca * Mr(acid))} g dm⁻³', 'key': key}
    return {'stem': stem, 'answer': f'{g3(ca)} mol dm⁻³', 'key': key}


@t1e.add('C3', (3, 4, 5), 'numerical')
def t1e_limit(r, D):
    eq = r.choice(['Mg + 2HCl -> MgCl2 + H2', 'Zn + 2HCl -> ZnCl2 + H2', 'CaCO3 + 2HCl -> CaCl2 + H2O + CO2', '2Al + 6HCl -> 2AlCl3 + 3H2'])
    L, R = parse(eq)
    (k1, s), (k2, _) = L
    gas = [x for x in R if x[1] in GAS][0]
    m = r.choice([0.50, 0.80, 1.00, 1.20, 2.00, 2.50])
    V = r.choice([25.0, 40.0, 50.0, 100.0])
    c = r.choice([0.500, 1.00, 2.00, 0.250])
    ns, nh = m / Mr(s), c * V / 1000
    need_h = ns * k2 / k1
    lim = s if nh >= need_h else 'HCl'
    ngas = (ns * gas[0] / k1) if lim == s else (nh * gas[0] / k2)
    return {'stem': f'{sf(m, 3)} g of {F(s)} is added to {sf(V, 3)} cm³ of {sf(c, 3)} mol dm⁻³ hydrochloric acid: {E(eq)}. Determine which reactant is in excess and calculate the volume of {F(gas[1])} produced at room temperature and pressure, in cm³.',
            'answer': f'{"HCl" if lim == s else F(s)} is in excess; {g3(ngas * 24000)} cm³', 'key': f'n({F(s)}) = {g3(ns)} mol [1]; n(HCl) = {g3(nh)} mol [1]; HCl needed = {g3(need_h)} mol, so {F(lim)} is limiting [1]; V = {g3(ngas)} × 24 000 = {g3(ngas * 24000)} cm³ [1]'}


@t1e.add('C3', (5,), 'numerical')
def t1e_back(r, D):
    mshell = r.choice([0.500, 0.600, 0.750, 0.800, 1.00])
    pur = r.choice([0.85, 0.88, 0.9, 0.92, 0.95])
    nca = mshell * pur / 100.1
    vac, cac = 50.0, r.choice([0.500, 0.400])
    nac = vac * cac / 1000
    xs = nac - 2 * nca
    cb = 0.100 if xs * 1000 / 0.1 < 50 else 0.200
    # back titration with 25.0 cm3 aliquot of 250 cm3 solution
    titre = xs / 10 / cb * 1000
    if titre < 5 or titre > 45:
        return None
    pc = pur * 100
    return {'stem': f'{who(r)} adds {sf(mshell, 3)} g of powdered eggshell to {vac} cm³ of {sf(cac, 3)} mol dm⁻³ HCl (an excess). After reaction the solution is made up to 250 cm³; a 25.0 cm³ portion needs {titre:.2f} cm³ of {sf(cb, 3)} mol dm⁻³ NaOH for neutralisation. Calculate the percentage by mass of CaCO₃ in the eggshell. (Mr CaCO₃ = 100.1; CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂)',
            'answer': f'{g3(pc)}%', 'key': f'n(NaOH) = n(HCl) in 25.0 cm³ = {g3(xs / 10)} mol [1]; excess HCl in 250 cm³ = {g3(xs)} mol [1]; HCl reacted = {g3(nac)} − {g3(xs)} = {g3(2 * nca)} mol [1]; n(CaCO₃) = {g3(nca)} mol [1]; mass = {g3(nca * 100.1)} g, % = {g3(pc)}% [1]'}


def t1e_c4(r, D):
    acid, alk, ka, kb, eq = r.choice(ACIDBASE[:6])
    ca = r.choice([0.100, 0.0500, 0.150])
    titre = r.choice([20.4, 21.5, 22.8, 23.6, 24.4])
    na = ca * titre / 1000
    nb = na * kb / ka
    cb = nb / 0.025
    intro = P(r, r.choice([f'{{p}} uses a standard solution of {sf(ca, 3)} mol dm⁻³ {ANAME[acid]} to find the concentration of a solution of {ANAME[alk]} in {{lab}}. 25.0 cm³ of the alkali needed a mean titre of {titre} cm³.',
                           f'A water-treatment works in {{c}} checks the concentration of a {ANAME[alk]} solution by titration with {sf(ca, 3)} mol dm⁻³ {ANAME[acid]}. A 25.0 cm³ sample needs {titre} cm³ of acid.']))
    parts = [
        lambda r: ('Write a balanced equation for the reaction.', E(eq), '[1]'),
        lambda r: ('Calculate the amount of acid in the mean titre.', f'{g3(na)} mol', '[1]'),
        lambda r: ('Calculate the concentration of the alkali in mol dm⁻³.', f'{g3(cb)} mol dm⁻³', f'n(alkali) = {g3(nb)} mol; ÷ 0.0250 [2]'),
        lambda r: ('Calculate the concentration of the alkali in g dm⁻³.', f'{g3(cb * Mr(alk))} g dm⁻³', f'× Mr {mr1(Mr(alk))} [1]'),
        lambda r: ('Describe how the titration should be carried out to obtain an accurate mean titre.', 'Rinse apparatus with the solutions; pipette 25.0 cm³ alkali into a conical flask with indicator; add acid from the burette, swirling, dropwise near the end-point; repeat to concordant titres (within 0.10 cm³).', '[3]'),
        lambda r: ('The burette readings are recorded to the nearest 0.05 cm³. Calculate the percentage uncertainty in the titre if each reading has an uncertainty of ±0.05 cm³.', f'{g3(0.10 / titre * 100)}%', f'two readings: 0.10/{titre} × 100 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2, 3, 5))


c4reg(t1e, t1e_c4)

CHAPTERS[1] = [t1a, t1b, t1c, t1d, t1e]


# ===================================================================== Ch2 Electrons in atoms
SUBS = [('1s', 2), ('2s', 2), ('2p', 6), ('3s', 2), ('3p', 6), ('4s', 2), ('3d', 10), ('4p', 6), ('5s', 2)]
WRITE_ORDER = ['1s', '2s', '2p', '3s', '3p', '3d', '4s', '4p', '5s']
ZSYM = {v[1]: k for k, v in EL.items()}


def config(Z, charge=0):
    """dict subshell -> electrons for an atom/ion (Z <= 38)."""
    c = {}
    n = Z
    for s, cap_ in SUBS:
        if n <= 0:
            break
        k = min(n, cap_)
        c[s] = k
        n -= k
    if Z == 24:
        c['4s'], c['3d'] = 1, 5
    if Z == 29:
        c['4s'], c['3d'] = 1, 10
    if charge > 0:
        rem = charge
        for s in ['4p', '4s', '3d', '3p', '3s', '2p', '2s', '1s'] if Z > 20 else ['5s', '4p', '3d', '4s', '3p', '3s', '2p', '2s', '1s']:
            if rem <= 0:
                break
            if c.get(s):
                k = min(rem, c[s])
                c[s] -= k
                rem -= k
        c = {k: v for k, v in c.items() if v}
    elif charge < 0:
        n = -charge
        for s, cap_ in SUBS:
            have = c.get(s, 0)
            if have < cap_ and n > 0:
                k = min(cap_ - have, n)
                c[s] = have + k
                n -= k
    return c


def cstr(c):
    return ''.join(s + sup(c[s]) for s in WRITE_ORDER if c.get(s))


def unpaired(c):
    tot = 0
    for s, e in c.items():
        o = {'s': 1, 'p': 3, 'd': 5}[s[-1]]
        tot += e if e <= o else 2 * o - e
    return tot


CONF_EL = [z for z in range(1, 37)]
CONF_ION = [('Na', 1), ('Mg', 2), ('Al', 3), ('O', -2), ('F', -1), ('Cl', -1), ('S', -2), ('N', -3), ('K', 1), ('Ca', 2), ('Fe', 2), ('Fe', 3), ('Cu', 2), ('Cu', 1),
            ('Zn', 2), ('Cr', 3), ('Mn', 2), ('Co', 2), ('Ni', 2), ('Ti', 2), ('V', 3), ('Sc', 3), ('Br', -1), ('P', -3), ('Li', 1), ('Be', 2), ('H', -1)]

t2a = topic('Shells, subshells and orbitals; shapes of s and p orbitals', 'shells, subshells and orbitals', 'shapes of s and p orbitals')
t2a.fixed('C1', (1, 2), [
    ('What is the shape of an s orbital?', 'spherical', 's orbitals are spherical; p orbitals are dumbbell-shaped along x, y and z axes.', ['dumbbell-shaped', 'a flat disc', 'four-lobed']),
    ('How many orbitals are there in a p subshell?', '3', 'p subshell: px, py, pz — 3 orbitals, up to 6 electrons.', ['1', '5', '6']),
    ('What is the maximum number of electrons in one orbital?', '2', 'Each orbital holds up to two electrons with opposite spins.', ['1', '6', '8']),
    ('Which subshell is filled immediately after 4s?', '3d', 'Order of filling: 1s 2s 2p 3s 3p 4s 3d 4p — 4s is lower in energy than 3d when empty.', ['4p', '3p', '4d']),
    ('What is the maximum number of electrons in the third shell (n = 3)?', '18', '3s (2) + 3p (6) + 3d (10) = 18 = 2n².', ['8', '32', '10']),
    ('What is an orbital?', 'a region of space around the nucleus that can hold up to two electrons', 'Orbital: region with a high probability of finding up to 2 electrons of opposite spin.', ['the circular path followed by an electron', 'a group of subshells with the same energy', 'the nucleus of an atom']),
    ('Which statement about the three 2p orbitals is correct?', 'they have the same energy and are at right angles to each other', '2px, 2py, 2pz: degenerate, mutually perpendicular dumbbells.', ['they have different energies', 'they are all spherical', 'they lie along the same axis']),
    ('State the number of orbitals in a d subshell.', '5', '[1]'),
])
t2a.fixed('C2', (2, 3, 4), [
    ('Explain why the 4s subshell fills before the 3d subshell.', 'The 4s subshell is lower in energy than 3d (in atoms from K to Ca), so electrons occupy it first.', '4s lower energy [1]; electrons fill lowest energy first [1]'),
    ('Describe the difference between a 1s and a 2s orbital.', 'Both are spherical, but the 2s orbital is larger (further from the nucleus) and higher in energy.', 'both spherical [1]; 2s larger/higher energy [1]'),
    ('Describe the shape and orientation of the 2p orbitals.', 'Three dumbbell-shaped orbitals (2px, 2py, 2pz) arranged at right angles along the x, y and z axes, each with two lobes on either side of the nucleus.', 'dumbbell [1]; three at 90° to each other [1]'),
    ('Explain the term subshell.', 'A group of orbitals of equal energy within a shell, labelled s, p, d or f (1, 3, 5 or 7 orbitals).', 'orbitals of same energy within a shell [1]; s/p/d with orbital numbers [1]'),
])
errs(t2a, [
    ('A p orbital can hold up to 6 electrons.', 'A p subshell holds 6 electrons; each p orbital holds a maximum of 2.'),
    ('Electrons in an orbital move in a fixed circular path around the nucleus.', 'An orbital is a region of space where there is a high probability of finding the electron(s); not a fixed orbit.'),
    ('The 3d subshell is always filled before 4s.', '4s fills first because it is lower in energy than 3d for K and Ca; 3d then fills from Sc to Zn.'),
])
c2mix(t2a, ['{p} is drawing diagrams of atomic orbitals for a revision poster.', 'A class in {c} is studying the arrangement of electrons in shells and subshells.'])


@t2a.add('C3', (1, 2, 3, 4), 'numerical')
def t2a_count(r, D):
    if D <= 2:
        n = r.choice([1, 2, 3, 4])
        what = r.choice(['orbitals', 'electrons'])
        val = n * n if what == 'orbitals' else 2 * n * n
        return nmc(r, f'What is the maximum number of {what} in the shell with principal quantum number n = {n}?', val, [n, 2 * n, n * n if what == 'electrons' else 2 * n * n, 8, val + 2], '', f'{what}: {"n²" if what == "orbitals" else "2n²"} = {val}.', f=str)
    Z = r.choice(range(5, 37))
    c = config(Z)
    sub = r.choice(['s', 'p', 'd'] if Z > 20 else ['s', 'p'])
    val = sum(v for k, v in c.items() if k.endswith(sub))
    norb = sum(1 for k, v in c.items() if k.endswith(sub) for _ in range({'s': 1, 'p': 3, 'd': 5}[sub]) if v)
    return {'stem': f'For an atom of {EL[ZSYM[Z]][0]} (proton number {Z}), state (i) the total number of electrons in {sub} orbitals and (ii) the number of {sub} orbitals that contain at least one electron.',
            'answer': f'(i) {val} (ii) {sum(min(v, {"s": 1, "p": 3, "d": 5}[sub]) for k, v in c.items() if k.endswith(sub))}', 'key': f'configuration {cstr(c)} [1]; (i) {val} [1]; (ii) count of occupied {sub} orbitals [1]'}


def t2a_c4(r, D):
    Z = r.choice([7, 8, 15, 16, 17, 19, 20, 24, 26, 29])
    c = config(Z)
    intro = P(r, r.choice([f'{{p}} is studying the electron arrangement of {EL[ZSYM[Z]][0]} (proton number {Z}).', f'A teacher in {{c}} asks students to describe the orbitals occupied in an atom of {EL[ZSYM[Z]][0]}, Z = {Z}.']))
    parts = [
        lambda r: ('Write the full electronic configuration.', cstr(c), '[1]'),
        lambda r: ('Sketch and describe the shape of an s orbital and of a p orbital.', 's: sphere centred on the nucleus; p: dumbbell (two lobes) along an axis.', '[2]'),
        lambda r: ('State the number of occupied orbitals in the atom.', str(sum(min(v, {'s': 1, 'p': 3, 'd': 5}[k[-1]]) for k, v in c.items())), '[1]'),
        lambda r: ('State the number of unpaired electrons, explaining how electrons occupy orbitals of equal energy.', f'{unpaired(c)}; electrons occupy orbitals of equal energy singly (with parallel spins) before pairing, because this minimises repulsion.', '[2]'),
        lambda r: ('Explain why the 4s subshell is filled before 3d.', '4s is lower in energy than 3d.', '[1]'),
        lambda r: ('State the maximum number of electrons that the third shell can hold and how they are distributed among subshells.', '18: 3s 2, 3p 6, 3d 10.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t2a, t2a_c4)

# ---------------------------------------------------------- 2.2 electronic configurations, box notation, free radicals
t2b = topic('Electronic configurations including 1s²2s²2p⁶ notation and the box notation; free radicals', 'electronic configurations including 1s', 'box notation; free radicals')
t2b.fixed('C1', (1, 2), [
    ('What is the electronic configuration of chromium, Cr (Z = 24)?', '1s²2s²2p⁶3s²3p⁶3d⁵4s¹', 'Cr is an exception: a half-filled 3d⁵ subshell with 4s¹ is more stable.', ['1s²2s²2p⁶3s²3p⁶3d⁴4s²', '1s²2s²2p⁶3s²3p⁶3d⁶', '1s²2s²2p⁶3s²3p⁶4s²4p⁴']),
    ('Which electrons are removed first when an iron atom forms the Fe²⁺ ion?', 'the 4s electrons', 'Transition-metal ions lose 4s electrons before 3d: Fe²⁺ is [Ar]3d⁶.', ['the 3d electrons', 'one 4s and one 3d electron', 'the 3p electrons']),
    ('What is a free radical?', 'a species with one or more unpaired electrons', 'Free radicals (e.g. Cl•, CH₃•) have an unpaired electron and are very reactive.', ['a positive ion with a full outer shell', 'a molecule with a lone pair of electrons', 'an atom with a full outer shell']),
    ('In box notation, what do two arrows pointing in opposite directions in one box represent?', 'two electrons with opposite spins in the same orbital', 'Each box = orbital; arrows = electrons; paired electrons have opposite spin.', ['two electrons with the same spin', 'an empty orbital', 'two orbitals of the same energy']),
    ('Which species has the same electronic configuration as argon?', 'K⁺', 'K⁺ has 18 electrons: 1s²2s²2p⁶3s²3p⁶.', ['Na⁺', 'Ca', 'F⁻']),
    ('State the shorthand electronic configuration of copper, Cu (Z = 29).', '[Ar]3d¹⁰4s¹', '[1]'),
])
t2b.fixed('C2', (2, 3, 4), [
    ('Explain why a chlorine atom is a free radical but a chloride ion is not.', 'Cl (3p⁵) has an unpaired electron; Cl⁻ (3p⁶) has all electrons paired.', 'Cl has unpaired electron [1]; Cl⁻ all paired [1]'),
    ('Explain, using box notation, why nitrogen has three unpaired electrons.', 'The three 2p electrons occupy the three 2p orbitals singly with parallel spins (Hund’s rule) because this minimises repulsion.', 'box diagram 2p↑ ↑ ↑ [1]; singly occupied to minimise repulsion [1]'),
    ('Explain why copper has the configuration [Ar]3d¹⁰4s¹ rather than [Ar]3d⁹4s².', 'A completely filled 3d subshell gives a more stable (lower energy) arrangement.', 'full 3d more stable [1]; one 4s electron moves into 3d [1]'),
    ('Explain why the methyl radical, •CH₃, is very reactive.', 'Carbon has an unpaired electron; the radical readily forms a bond by pairing that electron (e.g. with Cl•).', 'unpaired electron [1]; pairs by forming bond [1]'),
])
errs(t2b, [
    ('The Fe²⁺ ion has the configuration [Ar]3d⁴4s².', 'The 4s electrons are lost first: Fe²⁺ is [Ar]3d⁶.'),
    ('The oxygen atom has no unpaired electrons because 2p⁴ is an even number.', 'In 2p⁴ one orbital is paired and two are singly occupied, so O has two unpaired electrons.'),
    ('The configuration of potassium is 1s²2s²2p⁶3s²3p⁶3d¹.', '4s is lower in energy than 3d, so K is 1s²2s²2p⁶3s²3p⁶4s¹.'),
])
c2mix(t2b, ['{p} is writing electronic configurations for a homework task.', 'A student in {c} is drawing box diagrams of atoms and ions.'])


@t2b.add('C1', (1, 2, 3))
def t2b_conf(r, D):
    if r.random() < 0.5:
        Z = r.choice(CONF_EL)
        c = config(Z)
        nm = f'{EL[ZSYM[Z]][0]} (Z = {Z})'
    else:
        s, ch = r.choice(CONF_ION)
        Z = EL[s][1]
        c = config(Z, ch)
        nm = f'the {ion(s, ch)} ion ({EL[s][0]}, Z = {Z})'
    right = cstr(c)
    wrong = set()
    # plausible errors
    if Z > 20:
        c2 = config(Z)
        wrong.add(cstr(c2))
        cc = dict(c)
        if cc.get('3d') and cc.get('3d') >= 1:
            cc['3d'] -= 1; cc['4s'] = cc.get('4s', 0) + 1
            wrong.add(cstr(cc))
    cc = dict(c)
    last = [s for s in WRITE_ORDER if cc.get(s)][-1]
    cc[last] += 1
    wrong.add(cstr(cc))
    if cc[last] > 2:
        cc = dict(c); cc[last] -= 1; wrong.add(cstr(cc))
    cc = dict(c)
    if cc.get('3d') and not cc.get('4s'):
        cc['3d'] -= 2; cc['4s'] = 2; wrong.add(cstr(cc))
    if cc.get('3p') == 6 and not cc.get('4s') and Z <= 20:
        wrong.add(cstr({**cc, '3p': 5, '4s': 1}))
    wrong.add(cstr(config(max(1, Z - 1))))
    wrong.add(cstr(config(min(36, Z + 1))))
    wrong.discard(right)
    return mc(r, f'What is the electronic configuration of {nm}?', right, sorted(wrong), f'{right}. ' + ('Transition-metal ions lose 4s electrons first.' if Z > 20 and 'ion' in nm else ''))


@t2b.add('C3', (1, 2, 3, 4), 'short')
def t2b_unp(r, D):
    if r.random() < 0.6:
        Z = r.choice(CONF_EL[1:])
        c = config(Z)
        nm = f'an atom of {EL[ZSYM[Z]][0]} (Z = {Z})'
    else:
        s, ch = r.choice(CONF_ION)
        Z = EL[s][1]
        c = config(Z, ch)
        nm = f'the {ion(s, ch)} ion'
    u = unpaired(c)
    if D == 1:
        return nmc(r, f'How many unpaired electrons are there in {nm}?', u, [u + 1, u + 2, max(0, u - 1) if u else 3, 0 if u else 1, 4, 5], '', f'{cstr(c)}: {u} unpaired.', f=str)
    rad = 'is' if u else 'is not'
    return {'stem': f'Write the electronic configuration of {nm}. Use box notation for the outer subshells to deduce the number of unpaired electrons and state whether it is a free radical.' if D >= 3 else f'Write the full electronic configuration of {nm} and state the number of unpaired electrons.',
            'answer': f'{cstr(c)}; {u} unpaired electron(s); it {rad} a free radical' if D >= 3 else f'{cstr(c)}; {u} unpaired', 'key': f'configuration {cstr(c)} [1]; {u} unpaired (singly-filled orbitals before pairing) [1]' + (f'; {"radical: has unpaired electron(s)" if u else "not a radical: all paired"} [1]' if D >= 3 else '')}


def t2b_c4(r, D):
    s, ch = r.choice([x for x in CONF_ION if EL[x[0]][1] > 20 and x[1] > 0])
    Z = EL[s][1]
    ca, ci = config(Z), config(Z, ch)
    intro = P(r, r.choice([f'{EL[s][0].capitalize()} (Z = {Z}) forms the ion {ion(s, ch)}, which is found in {{p}}’s sample of a mineral from {{c}}.', f'{{p}} is investigating compounds of {EL[s][0]}, Z = {Z}, which contain {ion(s, ch)} ions.']))
    parts = [
        lambda r: (f'Write the full electronic configuration of a {EL[s][0]} atom.', cstr(ca), '[1]'),
        lambda r: (f'Write the electronic configuration of the {ion(s, ch)} ion.', cstr(ci), '[1]'),
        lambda r: ('Explain which electrons are lost when the ion forms.', 'The 4s electrons are lost first (then 3d), because once 3d is occupied the 4s electrons are higher in energy / further from the nucleus.', '[2]'),
        lambda r: (f'Draw the box notation for the 3d and 4s subshells of {ion(s, ch)} and state the number of unpaired electrons.', f'{unpaired(ci)} unpaired electrons', '[2]'),
        lambda r: ('Define the term free radical and state whether this ion is one.', f'A species with an unpaired electron; ' + ('yes, it has unpaired electrons (though as a stable ion it is not usually described as a reactive radical)' if unpaired(ci) else 'no, all electrons are paired'), '[2]'),
        lambda r: ('Name another species with the same electronic configuration as Ar.', 'e.g. K⁺, Ca²⁺, Cl⁻, S²⁻', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t2b, t2b_c4)

# ---------------------------------------------------------- 2.3 successive ionisation energies
IE = {  # successive IEs, kJ mol-1
    'Li': [520, 7298, 11815], 'Be': [900, 1757, 14849, 21007], 'B': [801, 2427, 3660, 25026, 32827], 'C': [1086, 2353, 4621, 6223, 37831],
    'N': [1402, 2856, 4578, 7475, 9445, 53267], 'O': [1314, 3388, 5301, 7469, 10990, 13327, 71330], 'Na': [496, 4562, 6910, 9543, 13354], 'Mg': [738, 1451, 7733, 10543, 13630],
    'Al': [578, 1817, 2745, 11577, 14842], 'Si': [787, 1577, 3232, 4356, 16091, 19805], 'P': [1012, 1907, 2914, 4964, 6274, 21267], 'S': [1000, 2252, 3357, 4556, 7004, 8496, 27107],
    'Cl': [1251, 2298, 3822, 5159, 6540, 9362, 11018, 33604], 'K': [419, 3052, 4420, 5877], 'Ca': [590, 1145, 4912, 6491, 8153], 'Sr': [550, 1064, 4138, 5500], 'Ba': [503, 965, 3600],
}
GROUP = {'Li': 1, 'Na': 1, 'K': 1, 'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'B': 13, 'Al': 13, 'C': 14, 'Si': 14, 'N': 15, 'P': 15, 'O': 16, 'S': 16, 'Cl': 17}
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth']


def ie_eq(sym, n, states=True):
    a = sym + (('^' + (str(n - 1) if n - 1 > 1 else '') + '+') if n > 1 else '')
    b = sym + '^' + (str(n) if n > 1 else '') + '+'
    g = '(g)' if states else ''
    return f'{F(a)}{g} → {F(b)}{g} + e⁻'


def jump_after(ies):
    best, k = 0, 0
    for i in range(1, len(ies)):
        ratio = ies[i] / ies[i - 1]
        if ratio > best:
            best, k = ratio, i
    return k


t2c = topic('First and successive ionisation energies and factors affecting them', 'first and successive ionisation energies', 'factors affecting them')
t2c.fixed('C1', (1, 2), [
    ('Which equation represents the first ionisation energy of sodium?', 'Na(g) → Na⁺(g) + e⁻', 'First IE: 1 mol of gaseous atoms → 1 mol of gaseous 1+ ions.', ['Na(s) → Na⁺(g) + e⁻', 'Na(g) + e⁻ → Na⁻(g)', 'Na(s) → Na⁺(aq) + e⁻']),
    ('Which factor does NOT affect the first ionisation energy of an atom?', 'the number of neutrons in the nucleus', 'IE depends on nuclear charge, distance of outer electron, shielding and spin-pair repulsion.', ['the nuclear charge', 'the distance of the outer electron from the nucleus', 'shielding by inner electrons']),
    ('Why do successive ionisation energies of an element always increase?', 'each electron is removed from an increasingly positive ion', 'Fewer electrons remain for the same nuclear charge, so attraction for each is greater.', ['the nuclear charge increases after each ionisation', 'electrons are removed from inner shells first', 'the atom gains neutrons']),
    ('An element has successive ionisation energies 578, 1817, 2745, 11 577 kJ mol⁻¹. In which group is it?', '13', 'Large jump after the 3rd electron: three outer electrons, Group 13 (aluminium).', ['3', '2', '14']),
    ('What is the unit of ionisation energy?', 'kJ mol⁻¹', 'Ionisation energies are molar quantities: kJ mol⁻¹.', ['kJ', 'J g⁻¹', 'mol kJ⁻¹']),
    ('Define the first ionisation energy of an element.', 'The energy needed to remove one electron from each atom in one mole of gaseous atoms to form one mole of gaseous 1+ ions.', '[2]'),
])
t2c.fixed('C2', (2, 3, 4), [
    ('Explain why there is a very large increase between the first and second ionisation energies of potassium.', 'The second electron is removed from a shell closer to the nucleus (3p), with much less shielding, so it is held far more strongly.', 'second electron from inner shell [1]; closer/less shielded so more attraction [1]'),
    ('Explain how a graph of successive ionisation energies provides evidence for electron shells.', 'Large jumps occur when electrons start to be removed from a new shell closer to the nucleus; the number of electrons between jumps shows the number in each shell.', 'big jumps between shells [1]; number of electrons in each shell [1]'),
    ('State and explain three factors that affect the size of an ionisation energy.', 'Nuclear charge (more protons, higher IE); distance of the electron from the nucleus (further, lower IE); shielding by inner electrons (more shielding, lower IE). Spin-pair repulsion lowers IE.', 'one mark per factor with direction [3]'),
    ('Explain why the second ionisation energy of an element is always larger than its first.', 'The second electron is removed from a positive ion; the same nuclear charge attracts fewer electrons, so there is less repulsion and greater attraction.', 'removed from positive ion [1]; greater attraction/less repulsion [1]'),
])
errs(t2c, [
    ('The second ionisation energy of magnesium is Mg(g) → Mg²⁺(g) + 2e⁻.', 'Second IE removes one electron from the 1+ ion: Mg⁺(g) → Mg²⁺(g) + e⁻.'),
    ('Ionisation energies increase because the nuclear charge increases each time an electron is removed.', 'The nuclear charge is unchanged; the electron is removed from an increasingly positive ion with less electron–electron repulsion.'),
    ('The first ionisation energy is the energy released when an electron is added to an atom.', 'It is the energy needed to remove one electron from each atom in 1 mol of gaseous atoms (endothermic).'),
])
c2mix(t2c, ['{p} is plotting successive ionisation energies from a data book.', 'A student in {c} compares ionisation energy data for several elements.'])


@t2c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2c_group(r, D):
    sym = r.choice(list(IE))
    ies = IE[sym]
    k = jump_after(ies)
    grp = GROUP[sym]
    lst = ', '.join(f'{v:,}' if v >= 10000 else str(v) for v in ies)
    if D == 1:
        return nmc(r, f'Element X has the successive ionisation energies (kJ mol⁻¹) {lst}. How many electrons are in the outer shell of X?', k, [k + 1, k - 1 if k > 1 else 4, len(ies), 8], '', f'Largest jump after electron {k}.', f=str)
    if D <= 3:
        return {'stem': f'The successive ionisation energies of element X, in kJ mol⁻¹, are {lst}. Deduce the group of X in the Periodic Table, explaining your reasoning.', 'answer': f'Group {grp}',
                'key': f'largest jump between {ORD[k - 1]} and {ORD[k]} IE [1]; so {k} electron(s) in outer shell, Group {grp} [1]'}
    name = EL[sym][0]
    return {'stem': f'Element X is in Period {3 if sym in ("Na", "Mg", "Al", "Si", "P", "S", "Cl") else 2 if sym in ("Li", "Be", "B", "C", "N", "O") else 4 if sym in ("K", "Ca") else 5 if sym == "Sr" else 6}. Its successive ionisation energies (kJ mol⁻¹) are {lst}. Identify X, write an equation for its {ORD[k]} ionisation energy and explain why this value is so much larger than the {ORD[k - 1]}.',
            'answer': f'{name}; {ie_eq(sym, k + 1)}; the {ORD[k]} electron is removed from an inner shell, closer to the nucleus and less shielded.', 'key': f'jump after {k} electrons: Group {grp}, so {name} [1]; equation with state symbols [1]; inner shell/closer [1]; less shielding/greater attraction [1]'}


@t2c.add('C1', (1, 2, 3))
def t2c_eq(r, D):
    sym = r.choice(list(IE))
    n = r.randint(1, min(4, len(IE[sym])))
    right = ie_eq(sym, n)
    a = sym + (('^' + (str(n - 1) if n - 1 > 1 else '') + '+') if n > 1 else '')
    b = sym + '^' + (str(n) if n > 1 else '') + '+'
    wrong = [f'{F(sym)}(g) → {F(b)}(g) + {n}e⁻' if n > 1 else f'{F(sym)}(s) → {F(b)}(g) + e⁻', f'{F(a)}(s) → {F(b)}(s) + e⁻', f'{F(a)}(g) + e⁻ → {F(b)}(g)', f'{F(a)}(aq) → {F(b)}(aq) + e⁻', f'{F(b)}(g) + e⁻ → {F(a)}(g)']
    return mc(r, f'Which equation represents the {ORD[n - 1]} ionisation energy of {EL[sym][0]}?', right, wrong, f'{ORD[n - 1].capitalize()} IE: remove one electron from each gaseous {"atom" if n == 1 else "ion"}: {right}.')


def t2c_c4(r, D):
    sym = r.choice(['Mg', 'Al', 'Si', 'P', 'S', 'Na', 'Ca', 'Cl'])
    ies = IE[sym]
    k = jump_after(ies)
    lst = ', '.join(f'{v:,}' if v >= 10000 else str(v) for v in ies)
    intro = P(r, r.choice([f'The successive ionisation energies of element Q, in kJ mol⁻¹, are {lst}.', f'{{p}} finds the following successive ionisation energies for an unknown element Q in a data book in {{lab}}: {lst} kJ mol⁻¹.']))
    parts = [
        lambda r: ('Define the term first ionisation energy.', 'Energy needed to remove one electron from each atom in one mole of gaseous atoms to form one mole of gaseous 1+ ions.', '[2]'),
        lambda r: ('Deduce the group to which Q belongs, explaining your answer.', f'Group {GROUP[sym]}: biggest jump after the {ORD[k - 1]} electron.', '[2]'),
        lambda r: (f'Write an equation, with state symbols, for the {ORD[min(2, len(ies) - 1)]} ionisation energy of Q (use the symbol Q).', ie_eq('Q', min(3, len(ies))), '[1]'),
        lambda r: ('Explain why successive ionisation energies increase.', 'Each electron is removed from a more positive ion; less repulsion and greater attraction for remaining electrons.', '[2]'),
        lambda r: (f'Explain the large increase between the {ORD[k - 1]} and {ORD[k]} ionisation energies.', 'The electron is removed from a new shell closer to the nucleus with less shielding.', '[2]'),
        lambda r: ('Q is in Period 3. Identify Q and write the electronic configuration of its atom.', f'{EL[sym][0]}: {cstr(config(EL[sym][1]))}', '[2]') if sym not in ('Ca',) else None,
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 4, 5))


c4reg(t2c, t2c_c4)

# ---------------------------------------------------------- 2.4 trends in first IE
IE1 = {'H': 1312, 'He': 2372, 'Li': 520, 'Be': 900, 'B': 801, 'C': 1086, 'N': 1402, 'O': 1314, 'F': 1681, 'Ne': 2081, 'Na': 496, 'Mg': 738, 'Al': 578, 'Si': 787,
       'P': 1012, 'S': 1000, 'Cl': 1251, 'Ar': 1521, 'K': 419, 'Ca': 590, 'Rb': 403, 'Sr': 550, 'Cs': 376, 'Ba': 503, 'Br': 1140, 'I': 1008, 'Kr': 1351}
IE_PAIRS = [  # (a, b) -> reason for which is higher
    ('Be', 'B', 'B’s outer electron is in the 2p subshell, which is higher in energy and slightly shielded by the 2s electrons, so B has the lower first IE'),
    ('Mg', 'Al', 'Al’s outer electron is in the 3p subshell, higher in energy and shielded by the 3s electrons, so Al has the lower first IE'),
    ('N', 'O', 'in O the 2p⁴ electron removed is paired in an orbital; spin-pair repulsion makes it easier to remove, so O has the lower first IE'),
    ('P', 'S', 'in S the 3p⁴ electron removed is paired; spin-pair repulsion makes it easier to remove, so S has the lower first IE'),
    ('Na', 'Mg', 'Mg has a greater nuclear charge and the electron is in the same shell with similar shielding, so Mg has the higher first IE'),
    ('Si', 'P', 'P has a greater nuclear charge, with similar shielding, so P has the higher first IE'),
    ('Cl', 'Ar', 'Ar has a greater nuclear charge, same shell and shielding, so Ar has the higher first IE'),
    ('Li', 'Na', 'Na’s outer electron is in a shell further from the nucleus and more shielded, so Na has the lower first IE despite more protons'),
    ('Na', 'K', 'K’s outer electron is further from the nucleus and more shielded, so K has the lower first IE'),
    ('Mg', 'Ca', 'Ca’s outer electron is in the fourth shell, further away and more shielded, so Ca has the lower first IE'),
    ('Ca', 'Sr', 'Sr’s outer electron is further from the nucleus with more shielding, so Sr has the lower first IE'),
    ('F', 'Cl', 'Cl’s outer electron is in the third shell, further from the nucleus and more shielded, so Cl has the lower first IE'),
    ('Ne', 'Na', 'Na’s outer electron is in a new shell (3s), further from the nucleus and shielded by the full inner shells, so Na has a much lower first IE'),
    ('C', 'N', 'N has a greater nuclear charge; its 2p electrons are unpaired and in the same subshell, so N has the higher first IE'),
    ('O', 'F', 'F has a greater nuclear charge with similar shielding, so F has the higher first IE'),
    ('Cl', 'Br', 'Br’s outer electron is in the fourth shell, further away and more shielded, so Br has the lower first IE'),
]

t2d = topic('Trends in first ionisation energy across a period and down a group', 'trends in first ionisation energy', 'across a period and down a group')
t2d.fixed('C1', (1, 2), [
    ('What is the general trend in first ionisation energy across Period 3 from Na to Ar?', 'it increases', 'Nuclear charge increases with similar shielding; dips at Al and S.', ['it decreases', 'it stays the same', 'it increases then decreases steadily']),
    ('Which element in Period 3 has the lowest first ionisation energy?', 'sodium', 'Na has the lowest nuclear charge with one 3s electron.', ['argon', 'aluminium', 'sulfur']),
    ('Why does the first ionisation energy decrease down Group 1?', 'the outer electron is further from the nucleus and more shielded', 'Extra shells outweigh the increase in nuclear charge.', ['the nuclear charge decreases', 'the outer electron is paired', 'the atoms have fewer neutrons']),
    ('Which pair shows a decrease in first ionisation energy from the first element to the second, because of spin-pair repulsion?', 'phosphorus to sulfur', 'S 3p⁴ has a paired electron; repulsion lowers IE.', ['magnesium to aluminium', 'sodium to magnesium', 'silicon to phosphorus']),
    ('Which element has the highest first ionisation energy?', 'helium', 'He: two electrons in the 1s orbital close to the nucleus, no shielding.', ['neon', 'hydrogen', 'fluorine']),
    ('State the general trend in first ionisation energy down Group 2.', 'It decreases.', '[1]'),
])
t2d.fixed('C2', (2, 3, 4), [
    ('Explain the general increase in first ionisation energy across Period 3.', 'Nuclear charge increases, electrons are added to the same shell so shielding is similar; atomic radius decreases so the outer electron is held more strongly.', 'nuclear charge increases [1]; same shell/similar shielding [1]'),
    ('Explain why the first ionisation energy of aluminium is lower than that of magnesium.', 'Al’s outer electron is in a 3p orbital, higher in energy than 3s and partly shielded by the 3s electrons, so it is easier to remove.', '3p vs 3s [1]; higher energy/extra shielding [1]'),
    ('Explain why the first ionisation energy of sulfur is lower than that of phosphorus.', 'In S the electron is removed from a 3p orbital containing a pair of electrons; spin-pair repulsion makes it easier to remove.', 'paired electron in 3p [1]; repulsion [1]'),
    ('Explain why the first ionisation energy decreases down Group 2 even though nuclear charge increases.', 'The outer electron is in a shell further from the nucleus and is more shielded by inner shells; these effects outweigh the extra nuclear charge.', 'further/more shells [1]; more shielding outweighs nuclear charge [1]'),
])
errs(t2d, [
    ('The first ionisation energy of oxygen is higher than nitrogen because oxygen has more protons.', 'O is lower than N: the electron removed from O is paired in a 2p orbital and spin-pair repulsion makes it easier to remove.'),
    ('First ionisation energy increases down a group because nuclear charge increases.', 'It decreases: increased distance and shielding outweigh the increased nuclear charge.'),
    ('Aluminium has a lower first ionisation energy than magnesium because of spin-pair repulsion.', 'The reason is that Al’s electron is in the higher-energy 3p subshell, shielded by 3s electrons; spin-pair repulsion explains the P → S dip.'),
])
c2mix(t2d, ['{p} plots a graph of first ionisation energy against proton number for elements 1 to 20.', 'A student in {c} is explaining the pattern of first ionisation energies in Periods 2 and 3.'])


@t2d.add('C2', (2, 3, 4), 'explain')
def t2d_pair(r, D):
    a, b, why = r.choice(IE_PAIRS)
    hi = a if IE1[a] > IE1[b] else b
    if D == 2 and r.random() < 0.5:
        return mc(r, f'Which element has the higher first ionisation energy, {EL[a][0]} or {EL[b][0]}?', EL[hi][0], [EL[a][0], EL[b][0], 'they have the same value', 'it depends on the number of neutrons'], f'{EL[hi][0]}: {why}.')
    frame = r.choice([f'The first ionisation energies of {EL[a][0]} and {EL[b][0]} are {IE1[a]} and {IE1[b]} kJ mol⁻¹ respectively. Explain the difference.',
                      f'Predict which of {EL[a][0]} and {EL[b][0]} has the higher first ionisation energy and explain your prediction.',
                      f'{person(r)} says {EL[a][0]} and {EL[b][0]} should have similar first ionisation energies. Use ideas about electronic structure to explain which is higher.'])
    return {'stem': frame, 'answer': f'{EL[hi][0]} is higher: {why}.', 'key': 'correct element higher [1]; explanation in terms of subshell / pairing / nuclear charge / distance and shielding [1]' + ('; refers to electronic configurations [1]' if D >= 4 else '')}


@t2d.add('C3', (1, 2, 3, 4), 'short')
def t2d_seq(r, D):
    per = r.choice([['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'], ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar']])
    i = r.randint(0, 4)
    seg = per[i:i + 4]
    vals = [IE1[s] for s in seg]
    labs = 'WXYZ'
    lst = ', '.join(f'{labs[j]} {vals[j]}' for j in range(4))
    dip = [j for j in range(1, 4) if vals[j] < vals[j - 1]]
    if not dip:
        return None
    j = dip[0]
    grp = GROUP.get(seg[j], {'Ne': 18, 'Ar': 18, 'F': 17}.get(seg[j]))
    if D == 1:
        return mc(r, f'Four consecutive elements W, X, Y, Z in Period {2 if per[0] == "Li" else 3} have first ionisation energies (kJ mol⁻¹) {lst}. Which element is in Group {grp}?', labs[j], list(labs), f'The dip occurs at {labs[j]} ({EL[seg[j]][0]}).')
    return {'stem': f'Four consecutive elements W, X, Y and Z in Period {2 if per[0] == "Li" else 3} have first ionisation energies of {lst} kJ mol⁻¹. Identify the four elements and explain why the first ionisation energy of {labs[j]} is lower than that of {labs[j - 1]}.',
            'answer': ', '.join(f'{labs[k]} = {EL[seg[k]][0]}' for k in range(4)) + f'. {cap([p[2] for p in IE_PAIRS if p[0] == seg[j - 1] and p[1] == seg[j]][0]) if any(p[0] == seg[j - 1] and p[1] == seg[j] for p in IE_PAIRS) else ""}.',
            'key': f'dip identifies Group {grp} [1]; all four identified [1]; explanation ({"subshell p higher energy/shielded" if grp == 13 else "spin-pair repulsion"}) [1]'}


def t2d_c4(r, D):
    per = r.choice([2, 3])
    els = ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'] if per == 2 else ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar']
    intro = P(r, r.choice([f'{{p}} plots the first ionisation energies of the Period {per} elements: ' + ', '.join(f'{s} {IE1[s]}' for s in els) + ' kJ mol⁻¹.',
                           f'The table shows first ionisation energies (kJ mol⁻¹) for Period {per}, studied by a class in {{c}}: ' + ', '.join(f'{s} {IE1[s]}' for s in els) + '.']))
    g2, g13, g15, g16 = els[1], els[2], els[4], els[5]
    nxt = 'Na' if per == 2 else 'K'
    parts = [
        lambda r: ('Describe and explain the general trend across the period.', 'Increases: nuclear charge increases, same shell, similar shielding.', '[2]'),
        lambda r: (f'Explain why {EL[g13][0]} has a lower first IE than {EL[g2][0]}.', f'Outer electron of {g13} in a p subshell: higher energy, shielded by s electrons.', '[2]'),
        lambda r: (f'Explain why {EL[g16][0]} has a lower first IE than {EL[g15][0]}.', 'Spin-pair repulsion: electron removed from a doubly occupied p orbital.', '[2]'),
        lambda r: (f'Predict, with a reason, how the first IE of {EL[nxt][0]} compares with that of {EL[els[-1]][0]}.', f'Much lower: new shell further from nucleus, more shielding.', '[2]'),
        lambda r: (f'Write an equation for the first ionisation energy of {EL[els[3]][0]}.', ie_eq(els[3], 1), '[1]'),
        lambda r: (f'Suggest a value for the first IE of the element below {EL[els[0]][0]} in Group 1.', f'about {IE1["Na" if per == 2 else "K"]} kJ mol⁻¹ (any value lower than {IE1[els[0]]})', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(0, 1, 2, 3))


c4reg(t2d, t2d_c4)

CHAPTERS[2] = [t2a, t2b, t2c, t2d]


# ===================================================================== Ch3 Chemical bonding
EN = {'H': 2.2, 'Li': 1.0, 'Be': 1.6, 'B': 2.0, 'C': 2.6, 'N': 3.0, 'O': 3.4, 'F': 4.0, 'Na': 0.9, 'Mg': 1.3, 'Al': 1.6, 'Si': 1.9, 'P': 2.2, 'S': 2.6, 'Cl': 3.2,
      'K': 0.8, 'Ca': 1.0, 'Br': 3.0, 'I': 2.7, 'Cs': 0.8}
BONDS = [('H', 'Cl'), ('C', 'O'), ('O', 'H'), ('N', 'H'), ('C', 'Cl'), ('C', 'H'), ('H', 'F'), ('C', 'F'), ('Si', 'Cl'), ('C', 'Br'), ('H', 'Br'), ('S', 'O'), ('P', 'Cl'),
         ('N', 'O'), ('B', 'F'), ('C', 'N'), ('H', 'I'), ('Si', 'O'), ('Al', 'Cl'), ('C', 'I'), ('O', 'F'), ('N', 'Cl')]
IONIC = ['NaCl', 'MgO', 'CaF2', 'K2O', 'LiF', 'MgCl2', 'Na2O', 'CaO', 'KBr', 'CsF', 'BaCl2', 'Li2O']
COVAL = ['HCl', 'CH4', 'NH3', 'CO2', 'SiCl4', 'H2O', 'PCl3', 'CCl4', 'SO2', 'BF3', 'H2S', 'N2', 'Cl2', 'C2H6']
DATIVE = [('NH₄⁺', 'the lone pair on N of NH₃ is donated to H⁺'), ('H₃O⁺', 'a lone pair on O of H₂O is donated to H⁺'), ('Al₂Cl₆', 'a lone pair on a Cl atom of each AlCl₃ is donated to the Al atom of the other AlCl₃'),
          ('CO', 'one of the three bonds is formed by a lone pair donated from O to C'), ('NH₃BF₃', 'the lone pair on N of NH₃ is donated to the electron-deficient B of BF₃')]

t3a = topic('Ionic, covalent, dative covalent and metallic bonding; electronegativity and bond polarity', 'ionic, covalent, dative covalent and metallic bonding', 'electronegativity and bond polarity')
t3a.fixed('C1', (1, 2), [
    ('What is meant by electronegativity?', 'the power of an atom to attract the bonding electrons in a covalent bond', 'Electronegativity increases across a period and decreases down a group; F is the most electronegative.', ['the energy needed to remove an electron from an atom', 'the energy released when an atom gains an electron', 'the number of electrons an atom can share']),
    ('Which element is the most electronegative?', 'fluorine', 'Electronegativity increases across a period and up a group: F (4.0) is highest.', ['chlorine', 'oxygen', 'caesium']),
    ('What is metallic bonding?', 'electrostatic attraction between positive metal ions and delocalised electrons', 'Lattice of cations in a sea of delocalised electrons.', ['sharing of electron pairs between metal atoms', 'attraction between positive and negative ions', 'attraction between neighbouring metal atoms’ nuclei']),
    ('What is a dative covalent (co-ordinate) bond?', 'a covalent bond in which both shared electrons come from one atom', 'Example: NH₃ + H⁺ → NH₄⁺; drawn as an arrow from donor to acceptor.', ['a bond formed by transfer of electrons', 'a bond between two metal atoms', 'a double covalent bond']),
    ('Which species contains a dative covalent bond?', 'NH₄⁺', 'N lone pair donated to H⁺ in NH₄⁺.', ['NH₃', 'CH₄', 'H₂O']),
    ('What is ionic bonding?', 'electrostatic attraction between oppositely charged ions', 'Formed by electron transfer from metal to non-metal.', ['sharing of a pair of electrons', 'attraction between delocalised electrons and cations', 'attraction between dipoles']),
    ('State how electronegativity changes down Group 17.', 'It decreases.', '[1]'),
])
t3a.fixed('C2', (2, 3, 4), [
    ('Explain why the H–Cl bond is polar.', 'Cl is more electronegative than H, so the bonding pair is drawn towards Cl, giving Hδ+ and Clδ−.', 'Cl more electronegative [1]; unequal sharing, δ+/δ− [1]'),
    ('Explain why tetrachloromethane, CCl₄, has polar bonds but is a non-polar molecule.', 'Each C–Cl bond is polar, but the molecule is symmetrical (tetrahedral) so the bond dipoles cancel.', 'polar bonds [1]; symmetry so dipoles cancel [1]'),
    ('Explain why aluminium chloride exists as Al₂Cl₆ molecules in the vapour at low temperature.', 'Al in AlCl₃ has only six outer electrons; a lone pair from a Cl on another AlCl₃ forms a dative bond to Al, giving each Al an octet.', 'Al electron-deficient [1]; Cl lone pair forms dative bond [1]'),
    ('Explain why metals conduct electricity in the solid state.', 'Delocalised electrons are free to move through the lattice and carry charge when a potential difference is applied.', 'delocalised electrons [1]; mobile, carry charge [1]'),
    ('Explain why electronegativity increases across Period 3.', 'Nuclear charge increases and atomic radius decreases with similar shielding, so the bonding pair is attracted more strongly.', 'nuclear charge/radius [1]; stronger attraction for bonding pair [1]'),
])
errs(t3a, [
    ('In an O–H bond, hydrogen carries a partial negative charge because it is smaller.', 'O is more electronegative, so O is δ− and H is δ+.'),
    ('A dative covalent bond is weaker than an ordinary covalent bond because only one atom provides electrons.', 'Once formed, a dative bond is identical to any other covalent bond (e.g. the four N–H bonds in NH₄⁺ are the same).'),
    ('Metallic bonding is the attraction between metal atoms sharing electron pairs.', 'Metallic bonding is the attraction between positive metal ions and a sea of delocalised electrons.'),
])
c2mix(t3a, ['{p} is comparing types of chemical bond for an AS assignment.', 'A student in {c} is using Pauling electronegativity values to predict bond polarity.'])


@t3a.add('C1', (1, 2, 3))
def t3a_polar(r, D):
    a, b = r.choice([x for x in BONDS if EN[x[0]] != EN[x[1]]])
    neg_ = a if EN[a] > EN[b] else b
    pos = b if neg_ == a else a
    if r.random() < 0.5:
        return mc(r, f'In the {a}–{b} bond, which atom carries the partial negative charge (δ−)?', neg_, [pos, 'neither atom', 'both atoms equally', 'it depends on the state'], f'{neg_} has the higher electronegativity ({EN[neg_]} vs {EN[pos]}).')
    four = r.sample(BONDS, 4)
    best = max(four, key=lambda x: abs(EN[x[0]] - EN[x[1]]))
    if sum(1 for x in four if abs(EN[x[0]] - EN[x[1]]) == abs(EN[best[0]] - EN[best[1]])) > 1:
        return None
    return mc(r, 'Using Pauling electronegativity values, which bond is the most polar?', f'{best[0]}–{best[1]}', [f'{x[0]}–{x[1]}' for x in four], f'Largest electronegativity difference: {best[0]}–{best[1]} ({abs(EN[best[0]] - EN[best[1]]):.1f}).')


@t3a.add('C3', (1, 2, 3, 4), 'short')
def t3a_type(r, D):
    if D == 1:
        c = r.choice(IONIC)
        return mc(r, 'Which compound has ionic bonding?', F(c), [F(x) for x in r.sample(COVAL, 4)], f'{F(c)}: metal + non-metal, large electronegativity difference.')
    pair = r.sample(BONDS + [('Na', 'Cl'), ('Mg', 'O'), ('K', 'F'), ('Ca', 'O'), ('Li', 'F'), ('Cs', 'F')], 1)[0]
    d = round(abs(EN[pair[0]] - EN[pair[1]]), 1)
    kind = 'ionic' if d >= 1.8 else ('polar covalent' if d >= 0.4 else 'essentially non-polar covalent')
    hi = pair[0] if EN[pair[0]] > EN[pair[1]] else pair[1]
    lo = pair[1] if hi == pair[0] else pair[0]
    metals = {'Li', 'Na', 'K', 'Cs', 'Mg', 'Ca', 'Sr', 'Ba', 'Al'}
    if kind == 'ionic' and not (metals & set(pair)):
        return None
    if kind == 'ionic' and 'Al' in pair:
        return None
    chg = {'ionic': f'; {lo} forms positive ions and {hi} negative ions', 'polar covalent': f'; {lo} is δ+ and {hi} is δ−', 'essentially non-polar covalent': '; no significant partial charges'}[kind]
    return {'stem': f'The Pauling electronegativities of {EL[pair[0]][0]} and {EL[pair[1]][0]} are {EN[pair[0]]} and {EN[pair[1]]}. Predict the type of bonding between them and explain your answer' + (', showing any partial charges.' if D >= 3 else '.'),
            'answer': f'Difference = {d:.1f}: {kind}' + (chg if D >= 3 else ''), 'key': f'difference {d:.1f} [1]; {kind} (large difference → electron transfer; small → sharing) [1]' + ('; partial charges or ions correct [1]' if D >= 3 else '')}


@t3a.add('C2', (2, 3, 4), 'explain')
def t3a_dative(r, D):
    sp, why = r.choice(DATIVE)
    return {'stem': f'{r.choice(["Explain how a dative covalent bond forms in", "Describe the bonding in", "Using a dot-and-cross description, explain the formation of the co-ordinate bond in"])} {sp}.',
            'answer': cap(why) + '; both electrons in the shared pair come from the same atom.', 'key': 'identifies donor atom and lone pair [1]; identifies acceptor with empty orbital [1]' + ('; both electrons from one atom/drawn as arrow [1]' if D >= 4 else '')}


def t3a_c4(r, D):
    intro = P(r, r.choice(['{p} investigates the bonding in sodium chloride, hydrogen chloride, ammonium chloride and magnesium in {lab}.',
                           'A materials company in {c} compares substances with ionic, covalent, dative covalent and metallic bonding.']))
    parts = [
        lambda r: ('Draw a dot-and-cross diagram for sodium chloride, showing outer electrons only.', 'Na⁺ with no outer electrons (or full 2,8 shell shown) and Cl⁻ with 8 outer electrons (one cross), charges shown.', '[2]'),
        lambda r: ('Describe the bonding in magnesium metal.', 'Lattice of Mg²⁺ ions in a sea of delocalised electrons (two per atom); electrostatic attraction.', '[2]'),
        lambda r: ('Explain how the ammonium ion is formed from ammonia and a hydrogen ion.', 'Lone pair on N donated to H⁺, forming a dative covalent bond.', '[2]'),
        lambda r: ('Explain why HCl is a polar molecule while Cl₂ is not.', 'Cl more electronegative than H: unequal sharing; in Cl₂ identical atoms share equally.', '[2]'),
        lambda r: ('Define electronegativity and state the trend across a period.', 'Power of an atom to attract the bonding pair in a covalent bond; increases across a period.', '[2]'),
        lambda r: ('Explain why magnesium has a higher melting point than sodium.', 'Mg²⁺ has a higher charge and is smaller; two delocalised electrons per atom; stronger metallic bonding.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t3a, t3a_c4)

# ---------------------------------------------------------- 3.2 sigma and pi bonds; hybridisation
SIGPI = [  # name, formula, sigma, pi, hybridisation of carbon(s) / central atom note
    ('ethane', 'C2H6', 7, 0, 'sp³'), ('ethene', 'C2H4', 5, 1, 'sp²'), ('ethyne', 'C2H2', 3, 2, 'sp'), ('carbon dioxide', 'CO2', 2, 2, 'sp'), ('hydrogen cyanide', 'HCN', 2, 2, 'sp'),
    ('propene', 'CH2=CHCH3', 8, 1, 'sp² (C=C carbons) and sp³ (CH₃)'), ('methanal', 'HCHO', 3, 1, 'sp²'), ('buta-1,3-diene', 'CH2=CHCH=CH2', 9, 2, 'sp²'),
    ('ethanoic acid', 'CH3COOH', 7, 1, 'sp³ (CH₃) and sp² (COOH)'), ('nitrogen', 'N2', 1, 2, 'sp (N)'), ('propyne', 'CH≡CCH3', 6, 2, 'sp (C≡C) and sp³ (CH₃)'),
    ('ethanal', 'CH3CHO', 6, 1, 'sp³ (CH₃) and sp² (CHO)'), ('propanone', 'CH3COCH3', 9, 1, 'sp³ (CH₃) and sp² (C=O)'), ('but-2-ene', 'CH3CH=CHCH3', 11, 1, 'sp³ and sp²'),
    ('methane', 'CH4', 4, 0, 'sp³'), ('chloroethene', 'CH2=CHCl', 5, 1, 'sp²'), ('propanenitrile', 'CH3CH2CN', 8, 2, 'sp³ and sp (C≡N carbon)'),
]
HYB = {'sp³': ('tetrahedral', '109.5°', 4), 'sp²': ('trigonal planar', '120°', 3), 'sp': ('linear', '180°', 2)}
HYB_C = [('the carbon atom in methane', 'sp³'), ('each carbon atom in ethene', 'sp²'), ('each carbon atom in ethyne', 'sp'), ('the carbon atom in carbon dioxide', 'sp'),
         ('the carbonyl carbon in propanone', 'sp²'), ('the carbon atom of the CH₃ group in ethanal', 'sp³'), ('the carbon atom in hydrogen cyanide', 'sp'),
         ('each carbon in ethane', 'sp³'), ('the carbon of the COOH group in ethanoic acid', 'sp²'), ('the boron atom in BF₃', 'sp²'), ('the carbon atom in methanal', 'sp²')]

t3b = topic('Sigma and pi bonds; hybridisation (sp, sp², sp³)', 'sigma and pi bonds', 'hybridisation (sp, sp')
t3b.fixed('C1', (1, 2), [
    ('How is a σ (sigma) bond formed?', 'by end-on (direct) overlap of orbitals between the two nuclei', 'σ: head-on overlap, electron density on the internuclear axis.', ['by sideways overlap of p orbitals', 'by transfer of electrons', 'by overlap of two empty orbitals']),
    ('How is a π (pi) bond formed?', 'by sideways overlap of adjacent p orbitals', 'π: electron density above and below the internuclear axis.', ['by end-on overlap of s orbitals', 'by overlap of hybrid orbitals along the axis', 'by donation of a lone pair']),
    ('A carbon–carbon double bond consists of', 'one σ bond and one π bond', 'Double bond = σ + π; triple = σ + 2π.', ['two σ bonds', 'two π bonds', 'one σ bond and two π bonds']),
    ('What is the hybridisation of each carbon atom in ethene?', 'sp²', 'Three sp² orbitals form σ bonds (trigonal planar); the unhybridised 2p orbital forms the π bond.', ['sp³', 'sp', 'sp³d']),
    ('What is the bond angle around an sp-hybridised carbon atom?', '180°', 'Two sp orbitals point in opposite directions: linear.', ['109.5°', '120°', '90°']),
    ('Why is a π bond weaker than a σ bond?', 'the sideways overlap of p orbitals is less effective than end-on overlap', 'Less overlap; electron density further from nuclei.', ['π bonds contain fewer electrons', 'π bonds are longer than σ bonds', 'π bonds involve s orbitals']),
    ('State the number of σ bonds and π bonds in a triple bond.', 'One σ and two π.', '[1]'),
])
t3b.fixed('C2', (2, 3, 4), [
    ('Explain why there is no free rotation about a C=C double bond.', 'Rotation would require the sideways overlap of the p orbitals in the π bond to be broken.', 'π bond from sideways p overlap [1]; rotation breaks overlap [1]'),
    ('Describe the hybridisation of carbon in methane and explain the shape of the molecule.', 'One 2s and three 2p orbitals mix to form four equivalent sp³ hybrid orbitals, which repel to a tetrahedral arrangement (109.5°) and overlap end-on with H 1s orbitals to form σ bonds.', 'four sp³ orbitals [1]; tetrahedral 109.5° with σ bonds [1]'),
    ('Explain why ethene is a planar molecule.', 'Each carbon is sp² hybridised with three σ bonds at 120° in a plane; the π bond requires the p orbitals to be parallel, holding all six atoms in one plane.', 'sp² trigonal planar [1]; π overlap keeps atoms in plane [1]'),
    ('Explain why the C=C bond is more reactive than the C–C bond even though it is stronger overall.', 'The π electrons lie above and below the plane, exposed to electrophiles, and the π bond is weaker than the σ bond so it breaks more easily.', 'π electrons exposed/high electron density [1]; π bond weaker [1]'),
])
errs(t3b, [
    ('A double bond consists of two σ bonds.', 'A double bond is one σ bond and one π bond.'),
    ('In ethyne the carbon atoms are sp³ hybridised.', 'Each carbon in ethyne forms two σ bonds and two π bonds, so it is sp hybridised (linear, 180°).'),
    ('A π bond is formed by end-on overlap of p orbitals.', 'A π bond forms by sideways overlap of p orbitals; end-on overlap gives a σ bond.'),
])
c2mix(t3b, ['{p} builds models of hydrocarbons to show σ and π bonds.', 'A student in {c} is revising orbital overlap and hybridisation.'])


@t3b.add('C3', (1, 2, 3, 4), 'short')
def t3b_count(r, D):
    nm, f, s, p, h = r.choice(SIGPI)
    if D == 1:
        return nmc(r, f'How many σ bonds are there in one molecule of {nm}, {F(f)}?', s, [s + p, s - 1, s + 1, s + 2, p], '', f'{nm}: {s} σ, {p} π.', f=str)
    if D == 2:
        return {'stem': f'State the number of σ bonds and π bonds in a molecule of {nm}, {F(f)}.', 'answer': f'{s} σ bonds and {p} π bonds', 'key': f'σ = {s} [1]; π = {p} [1]'}
    return {'stem': f'For a molecule of {nm}, {F(f)}, state the number of σ and π bonds and the hybridisation of the carbon atom(s). Describe how a π bond is formed.',
            'answer': f'{s} σ, {p} π; {h}; π bond: sideways overlap of p orbitals on adjacent atoms', 'key': f'σ = {s} [1]; π = {p} [1]; hybridisation {h} [1]; sideways p overlap [1]'}


@t3b.add('C1', (1, 2, 3))
def t3b_hyb(r, D):
    what, h = r.choice(HYB_C)
    if r.random() < 0.5:
        return mc(r, f'What is the hybridisation of {what}?', h, ['sp', 'sp²', 'sp³', 'sp³d²'], f'{h}: {HYB[h][0]} arrangement of σ bonds ({HYB[h][1]}).')
    return mc(r, f'What is the bond angle around {what}?', HYB[h][1], ['109.5°', '120°', '180°', '90°', '104.5°'], f'{h} → {HYB[h][0]}, {HYB[h][1]}.')


def t3b_c4(r, D):
    nm, f, s, p, h = r.choice([x for x in SIGPI if x[3]])
    intro = P(r, r.choice([f'{{p}} is making a molecular model of {nm}, {F(f)}.', f'A research group in {{c}} is studying the bonding in {nm}, {F(f)}.']))
    parts = [
        lambda r: ('State the number of σ bonds and π bonds in the molecule.', f'{s} σ, {p} π', '[2]'),
        lambda r: ('Describe, with the help of a diagram, how σ and π bonds are formed.', 'σ: end-on overlap of orbitals along the internuclear axis; π: sideways overlap of parallel p orbitals above and below the axis.', '[2]'),
        lambda r: ('State the hybridisation of the carbon atom(s) and the bond angles around them.', f'{h}; ' + ('/'.join(HYB[k][1] for k in HYB if k in h)), '[2]'),
        lambda r: ('Explain why π bonds are weaker than σ bonds.', 'Sideways overlap is less effective; electron density further from the nuclei.', '[1]'),
        lambda r: ('Explain why the molecule is reactive towards electrophiles.', 'The π electrons are an exposed region of high electron density that attracts electrophiles.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t3b, t3b_c4)

# ---------------------------------------------------------- 3.3 VSEPR
SHAPES = {(2, 0): ('linear', '180°'), (3, 0): ('trigonal planar', '120°'), (4, 0): ('tetrahedral', '109.5°'), (3, 1): ('trigonal pyramidal', '107°'),
          (2, 2): ('non-linear (bent)', '104.5°'), (5, 0): ('trigonal bipyramidal', '90° and 120°'), (6, 0): ('octahedral', '90°'), (4, 2): ('square planar', '90°'),
          (2, 1): ('non-linear (bent)', 'about 118°')}
VSEPR = [  # formula, name, central atom, bonding regions, lone pairs
    ('CH4', 'methane', 'C', 4, 0), ('NH3', 'ammonia', 'N', 3, 1), ('H2O', 'water', 'O', 2, 2), ('BF3', 'boron trifluoride', 'B', 3, 0), ('CO2', 'carbon dioxide', 'C', 2, 0),
    ('SF6', 'sulfur hexafluoride', 'S', 6, 0), ('PCl5', 'phosphorus pentachloride', 'P', 5, 0), ('BeCl2', 'beryllium chloride (gas)', 'Be', 2, 0),
    ('NH4^+', 'ammonium ion', 'N', 4, 0), ('H3O^+', 'oxonium ion', 'O', 3, 1), ('SiCl4', 'silicon tetrachloride', 'Si', 4, 0), ('NF3', 'nitrogen trifluoride', 'N', 3, 1),
    ('AlCl3', 'aluminium chloride (monomer)', 'Al', 3, 0), ('BCl3', 'boron trichloride', 'B', 3, 0), ('CCl4', 'tetrachloromethane', 'C', 4, 0), ('NH2^-', 'amide ion', 'N', 2, 2),
    ('BF4^-', 'tetrafluoroborate ion', 'B', 4, 0), ('XeF4', 'xenon tetrafluoride', 'Xe', 4, 2), ('SO2', 'sulfur dioxide', 'S', 2, 1), ('PCl4^+', 'tetrachlorophosphonium ion', 'P', 4, 0),
    ('HCN', 'hydrogen cyanide', 'C', 2, 0), ('NCl3', 'nitrogen trichloride', 'N', 3, 1), ('Cl2O', 'dichlorine oxide', 'O', 2, 2), ('AlCl4^-', 'tetrachloroaluminate ion', 'Al', 4, 0),
]

t3c = topic('VSEPR: shapes of molecules and bond angles', 'vsepr: shapes of molecules and bond angles', 'shapes of molecules')
t3c.fixed('C1', (1, 2), [
    ('What is the shape of an ammonia molecule?', 'trigonal pyramidal', 'NH₃: 3 bonding pairs + 1 lone pair → pyramidal, 107°.', ['trigonal planar', 'tetrahedral', 'T-shaped']),
    ('What is the H–O–H bond angle in water?', '104.5°', '2 bonding pairs + 2 lone pairs; lone pairs repel more, closing the angle from 109.5°.', ['109.5°', '107°', '180°']),
    ('Which molecule is trigonal planar?', 'BF₃', 'BF₃: three bonding pairs, no lone pairs → 120°.', ['NH₃', 'PCl₃', 'CH₄']),
    ('In VSEPR theory, which repulsion is the strongest?', 'lone pair–lone pair', 'lp–lp > lp–bp > bp–bp.', ['bonding pair–bonding pair', 'lone pair–bonding pair', 'all repulsions are equal']),
    ('What is the shape of SF₆?', 'octahedral', 'Six bonding pairs, no lone pairs → octahedral, 90°.', ['hexagonal planar', 'trigonal bipyramidal', 'tetrahedral']),
    ('What are the bond angles in PCl₅?', '90° and 120°', 'Trigonal bipyramidal: axial–equatorial 90°, equatorial–equatorial 120°.', ['109.5° only', '90° only', '120° and 180° only']),
    ('State the basic idea of VSEPR theory.', 'Electron pairs around a central atom repel each other and arrange themselves as far apart as possible.', '[1]'),
])
t3c.fixed('C2', (2, 3, 4), [
    ('Explain why the bond angle in NH₃ (107°) is smaller than in CH₄ (109.5°).', 'NH₃ has a lone pair; lone pair–bond pair repulsion is greater than bond pair–bond pair repulsion, so the N–H bonds are pushed closer.', 'NH₃ lone pair [1]; lp–bp > bp–bp repulsion [1]'),
    ('Explain why CO₂ is linear even though the oxygen atoms carry lone pairs.', 'The shape depends on the electron pairs around the central C atom, which has two double bonds (two regions of electron density) and no lone pairs, so they are 180° apart.', 'two bonding regions around C [1]; no lone pairs on C, 180° [1]'),
    ('Explain why the ammonium ion is tetrahedral while ammonia is pyramidal.', 'In NH₄⁺ the lone pair of NH₃ forms a dative bond to H⁺, giving four bonding pairs and no lone pairs.', 'lone pair used in bond [1]; four bp, 109.5° [1]'),
    ('Explain why BF₃ is a non-polar molecule.', 'B–F bonds are polar but BF₃ is trigonal planar and symmetrical, so the dipoles cancel.', 'polar bonds [1]; symmetrical, dipoles cancel [1]'),
])
errs(t3c, [
    ('Water is linear because there are only two atoms bonded to oxygen.', 'O also has two lone pairs; four electron pairs give a bent shape with angle 104.5°.'),
    ('The bond angle in ammonia is 120° because there are three bonds.', 'N has three bonding pairs and one lone pair (tetrahedral arrangement), so the shape is pyramidal with angle about 107°.'),
    ('In SF₆ the bond angles are 60° because six bonds share 360°.', 'SF₆ is octahedral (three-dimensional) with 90° bond angles.'),
])
c2mix(t3c, ['{p} uses balloons tied together to model the shapes of molecules.', 'A student in {c} is predicting molecular shapes using VSEPR theory.'])


@t3c.add('C3', (1, 2, 3, 4, 5), 'short')
def t3c_shape(r, D):
    f, nm, cen, bp, lp = r.choice(VSEPR)
    shape, ang = SHAPES[(bp, lp)]
    if f in ('SO2', 'XeF4') and D < 4:
        return None
    if D == 1:
        return mc(r, f'What is the shape of {nm}, {F(f)}?', shape, [v[0] for v in SHAPES.values()], f'{bp} bonding region(s) and {lp} lone pair(s) on {cen}: {shape}.')
    if D == 2:
        return mc(r, f'What is the bond angle in {nm}, {F(f)}?', ang, list({v[1] for v in SHAPES.values()}), f'{shape}: {ang}.')
    stem = f'Predict the shape of {"the " if "ion" in nm else ""}{nm}, {F(f)}, and its bond angle. Explain your reasoning in terms of electron pairs around the central {cen} atom.'
    key = f'{bp} bonding pair(s)/regions and {lp} lone pair(s) on {cen} [1]; shape {shape} [1]; angle {ang} [1]'
    if D >= 4:
        key += '; electron pairs repel to be as far apart as possible, lone pairs repel more strongly [1]'
        stem += ' Draw a diagram showing any lone pairs.'
    return {'stem': stem, 'answer': f'{shape}, {ang}', 'key': key}


@t3c.add('C2', (2, 3, 4), 'explain')
def t3c_cmp(r, D):
    a, b = r.sample([x for x in VSEPR if x[0] not in ('SO2', 'XeF4') and x[3] + x[4] == 4], 2)
    sa, sb = SHAPES[(a[3], a[4])], SHAPES[(b[3], b[4])]
    if sa == sb:
        return None
    big = a if a[4] < b[4] else b
    return {'stem': f'Compare the shapes and bond angles of {F(a[0])} and {F(b[0])}. Explain the difference.',
            'answer': f'{F(a[0])}: {sa[0]}, {sa[1]}; {F(b[0])}: {sb[0]}, {sb[1]}. Both have four electron pairs around the central atom, but lone pairs repel more strongly than bonding pairs, so the species with more lone pairs ({F((a if big is b else b)[0])}) has the smaller angle.',
            'key': 'both shapes and angles [1]; four electron pairs in each [1]; lone pairs repel more strongly [1]'}


def t3c_c4(r, D):
    a, b, c = r.sample([x for x in VSEPR if x[0] not in ('XeF4', 'SO2')], 3)
    intro = P(r, r.choice([f'{{p}} is asked to predict the shapes of {F(a[0])}, {F(b[0])} and {F(c[0])}.', f'In an AS lesson in {{c}}, students use VSEPR theory for the species {F(a[0])}, {F(b[0])} and {F(c[0])}.']))
    def part(x):
        return lambda r: (f'Draw a diagram of {F(x[0])} and state its shape and bond angle.', f'{SHAPES[(x[3], x[4])][0]}, {SHAPES[(x[3], x[4])][1]}', '[2]')
    parts = [
        lambda r: ('State the main principle of VSEPR theory.', 'Electron pairs repel and arrange themselves as far apart as possible; lone pairs repel more than bonding pairs.', '[2]'),
        part(a), part(b), part(c),
        lambda r: ('State the order of strength of repulsions between electron pairs.', 'lone pair–lone pair > lone pair–bond pair > bond pair–bond pair', '[1]'),
        lambda r: ('Explain why a molecule with polar bonds may be non-polar overall.', 'If the shape is symmetrical, the bond dipoles cancel.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t3c, t3c_c4)

# ---------------------------------------------------------- 3.4 intermolecular forces
IMF = {  # formula: (name, strongest IMF, electrons, bp in °C)
    'CH4': ('methane', 'id-id', 10, -162), 'C2H6': ('ethane', 'id-id', 18, -89), 'C3H8': ('propane', 'id-id', 26, -42), 'C4H10': ('butane', 'id-id', 34, -1),
    'C5H12': ('pentane', 'id-id', 42, 36), 'HCl': ('hydrogen chloride', 'pd-pd', 18, -85), 'HBr': ('hydrogen bromide', 'pd-pd', 36, -67), 'HI': ('hydrogen iodide', 'pd-pd', 54, -35),
    'HF': ('hydrogen fluoride', 'H', 10, 20), 'H2O': ('water', 'H', 10, 100), 'H2S': ('hydrogen sulfide', 'pd-pd', 18, -60), 'NH3': ('ammonia', 'H', 10, -33),
    'PH3': ('phosphine', 'pd-pd', 18, -88), 'CH3OH': ('methanol', 'H', 18, 65), 'C2H5OH': ('ethanol', 'H', 26, 78), 'CH3CHO': ('ethanal', 'pd-pd', 24, 20),
    'CH3OCH3': ('methoxymethane', 'pd-pd', 26, -24), 'F2': ('fluorine', 'id-id', 18, -188), 'Cl2': ('chlorine', 'id-id', 34, -34), 'Br2': ('bromine', 'id-id', 70, 59),
    'I2': ('iodine', 'id-id', 106, 184), 'He': ('helium', 'id-id', 2, -269), 'Ne': ('neon', 'id-id', 10, -246), 'Ar': ('argon', 'id-id', 18, -186), 'Kr': ('krypton', 'id-id', 36, -153),
    'CH3COCH3': ('propanone', 'pd-pd', 32, 56), 'C(CH3)4': ('2,2-dimethylpropane', 'id-id', 42, 10), 'CH3CH2CH2OH': ('propan-1-ol', 'H', 34, 97), 'SiH4': ('silane', 'id-id', 18, -112),
    'CH3Cl': ('chloromethane', 'pd-pd', 26, -24), 'CCl4': ('tetrachloromethane', 'id-id', 74, 77),
}
IMFN = {'id-id': 'instantaneous dipole–induced dipole (London) forces', 'pd-pd': 'permanent dipole–permanent dipole forces', 'H': 'hydrogen bonding'}
IMF_PAIRS = [('CH4', 'C2H6'), ('C3H8', 'C4H10'), ('HCl', 'HBr'), ('HBr', 'HI'), ('HF', 'HCl'), ('H2O', 'H2S'), ('NH3', 'PH3'), ('CH3OH', 'C2H6'), ('C2H5OH', 'CH3OCH3'),
             ('F2', 'Cl2'), ('Cl2', 'Br2'), ('Br2', 'I2'), ('He', 'Ne'), ('Ar', 'Kr'), ('C5H12', 'C(CH3)4'), ('CH3CHO', 'C3H8'), ('C3H8', 'CH3OCH3'), ('CH3CH2CH2OH', 'CH3COCH3'),
             ('CH4', 'SiH4'), ('CH3Cl', 'C2H6'), ('H2O', 'HF'), ('C2H5OH', 'C3H8'), ('CCl4', 'CH4'), ('NH3', 'CH4')]


def imf_reason(a, b):
    A, B = IMF[a], IMF[b]
    hi, lo = (a, b) if A[3] > B[3] else (b, a)
    H, L = IMF[hi], IMF[lo]
    if hi == 'H2O' and lo == 'HF':
        return hi, 'each H₂O molecule can form two hydrogen bonds (two H atoms and two lone pairs) whereas HF forms on average only one per molecule, so more energy is needed to separate water molecules'
    if H[1] == 'H' and L[1] != 'H':
        return hi, f'{H[0]} molecules form hydrogen bonds (H bonded to N, O or F with a lone pair on a neighbour), which are much stronger than the {IMFN[L[1]]} between {L[0]} molecules'
    if hi == 'C5H12' and lo == 'C(CH3)4':
        return hi, 'both have 42 electrons, but the unbranched pentane molecules have a larger surface area of contact, so the instantaneous dipole–induced dipole forces are stronger'
    if H[1] == 'pd-pd' and L[1] == 'id-id' and abs(H[2] - L[2]) <= 8:
        return hi, f'with a similar number of electrons, {H[0]} is polar and has permanent dipole–permanent dipole forces in addition to London forces, so its intermolecular forces are stronger'
    if H[2] > L[2]:
        return hi, f'{H[0]} has more electrons ({H[2]} vs {L[2]}), so stronger instantaneous dipole–induced dipole forces between molecules; more energy is needed to separate them'
    return hi, f'{H[0]} has the stronger intermolecular forces ({IMFN[H[1]]}), so more energy is needed to separate the molecules'


t3d = topic('Intermolecular forces: instantaneous and permanent dipoles and hydrogen bonding', 'intermolecular forces: instantaneous and permanent dipoles', 'hydrogen bonding')
t3d.fixed('C1', (1, 2), [
    ('Which intermolecular force exists between all molecules?', 'instantaneous dipole–induced dipole forces', 'London (id-id) forces arise from temporary fluctuations in electron density in all molecules.', ['hydrogen bonds', 'permanent dipole–permanent dipole forces', 'ionic bonds']),
    ('Which substance has hydrogen bonding between its molecules?', 'ammonia, NH₃', 'H bonded to N, O or F, with a lone pair on N/O/F of a neighbouring molecule.', ['methane, CH₄', 'hydrogen chloride, HCl', 'phosphine, PH₃']),
    ('Why is ice less dense than liquid water?', 'hydrogen bonding holds the molecules in an open lattice', 'In ice each molecule forms four hydrogen bonds in a tetrahedral open structure; molecules are further apart than in the liquid.', ['ice contains air bubbles', 'water molecules expand when cooled', 'covalent bonds lengthen in ice']),
    ('Why does the boiling point of the noble gases increase down the group?', 'the number of electrons increases, so London forces are stronger', 'More electrons → larger instantaneous dipoles → stronger id-id forces.', ['the atoms become polar', 'hydrogen bonding increases', 'covalent bonds form between atoms']),
    ('Which compound has the highest boiling point?', 'H₂O', 'H₂O forms extensive hydrogen bonding (two per molecule).', ['H₂S', 'H₂Se', 'CH₄']),
    ('State two conditions needed for hydrogen bonding between molecules.', 'H atom bonded to N, O or F; a lone pair on an N, O or F atom of a neighbouring molecule.', '[2]'),
])
t3d.fixed('C2', (2, 3, 4), [
    ('Explain how instantaneous dipole–induced dipole forces arise.', 'Electrons move randomly, so at any instant the electron density is uneven, creating a temporary dipole; this induces a dipole in a neighbouring molecule and the two attract.', 'temporary uneven electron distribution [1]; induces dipole in neighbour, attraction [1]'),
    ('Explain why water has a much higher boiling point than hydrogen sulfide.', 'Water molecules form hydrogen bonds (O is very electronegative and small); H₂S has only weaker permanent dipole and London forces.', 'water hydrogen bonds [1]; stronger than forces in H₂S [1]'),
    ('Explain why propanone (Mr 58) has a higher boiling point than butane (Mr 58).', 'Propanone is polar (C=O dipole) so it has permanent dipole–permanent dipole forces as well as London forces; butane has only London forces.', 'propanone polar, pd-pd [1]; butane only id-id, similar electrons [1]'),
    ('Explain why ethanol is soluble in water but ethane is not.', 'Ethanol’s OH group forms hydrogen bonds with water molecules; ethane is non-polar and cannot.', 'hydrogen bonds with water [1]; ethane non-polar [1]'),
])
errs(t3d, [
    ('When water boils, the O–H bonds break.', 'Boiling overcomes the hydrogen bonds between water molecules; the covalent O–H bonds do not break.'),
    ('HCl molecules form hydrogen bonds because they contain hydrogen and a very electronegative atom.', 'Hydrogen bonding needs H bonded to N, O or F; Cl is too large/diffuse, so HCl has permanent dipole–permanent dipole forces.'),
    ('Non-polar molecules have no intermolecular forces.', 'All molecules have instantaneous dipole–induced dipole (London) forces.'),
])
c2mix(t3d, ['{p} compares the boiling points of several simple molecular substances.', 'A student in {c} is explaining physical properties using intermolecular forces.'])


@t3d.add('C2', (2, 3, 4), 'explain')
def t3d_pair(r, D):
    a, b = r.choice(IMF_PAIRS)
    hi, why = imf_reason(a, b)
    if D == 2 and r.random() < 0.5:
        return mc(r, f'Which has the higher boiling point, {IMF[a][0]} ({F(a)}) or {IMF[b][0]} ({F(b)})?', f'{IMF[hi][0]}', [IMF[a][0], IMF[b][0], 'they have the same boiling point', 'it cannot be predicted'], f'{IMF[hi][0]}: {why}.')
    fr = r.choice([f'The boiling points of {IMF[a][0]}, {F(a)}, and {IMF[b][0]}, {F(b)}, are {IMF[a][3]} °C and {IMF[b][3]} °C. Explain the difference in terms of intermolecular forces.',
                   f'Predict which of {IMF[a][0]} and {IMF[b][0]} has the higher boiling point. Explain your answer.',
                   f'{person(r)} says {IMF[a][0]} and {IMF[b][0]} should have similar boiling points. Explain why this is not correct.'])
    return {'stem': fr.replace('-', '−') if False else fr, 'answer': f'{IMF[hi][0].capitalize()} has the higher boiling point: {why}.', 'key': 'identifies forces in each substance [1]; compares strength with reason (electrons / H bonding / polarity / shape) [1]' + ('; more energy to separate molecules [1]' if D >= 4 else '')}


@t3d.add('C1', (1, 2, 3))
def t3d_kind(r, D):
    f = r.choice(list(IMF))
    k = IMF[f][1]
    return mc(r, f'What is the strongest type of intermolecular force between molecules of {IMF[f][0]}, {F(f)}?', IMFN[k], list(IMFN.values()) + ['covalent bonds', 'ionic attraction'], f'{IMF[f][0]}: {IMFN[k]}.')


@t3d.add('C3', (2, 3, 4), 'short')
def t3d_rank(r, D):
    pool = r.choice([['CH4', 'C2H6', 'C3H8', 'C4H10', 'C5H12'], ['HCl', 'HBr', 'HI', 'HF'], ['He', 'Ne', 'Ar', 'Kr'], ['F2', 'Cl2', 'Br2', 'I2'], ['CH4', 'NH3', 'H2O', 'HF'], ['C3H8', 'CH3OCH3', 'CH3CHO', 'C2H5OH']])
    k = 3 if D <= 3 else 4
    pick = r.sample(pool, min(k, len(pool)))
    order = sorted(pick, key=lambda f: IMF[f][3])
    return {'stem': f'Place the following in order of increasing boiling point and explain the order: ' + ', '.join(f'{IMF[f][0]} ({F(f)})' for f in pick) + '.',
            'answer': ' < '.join(IMF[f][0] for f in order) + '. ' + '; '.join(f'{IMF[f][0]}: {IMFN[IMF[f][1]]}' for f in order) + '.', 'key': 'correct order [1]; identifies type of force in each [1]; links strength to number of electrons / polarity / hydrogen bonding [1]'}


def t3d_c4(r, D):
    intro = P(r, r.choice(['The boiling points of the Group 16 hydrides are H₂O 100 °C, H₂S −60 °C, H₂Se −41 °C and H₂Te −2 °C.', 'The boiling points of the Group 17 hydrides are HF 20 °C, HCl −85 °C, HBr −67 °C and HI −35 °C.',
                           '{p} compares the boiling points of ethanol (78 °C), methoxymethane (−24 °C) and propane (−42 °C), which have similar Mr values.']))
    grp16 = 'H₂O' in intro
    alc = 'ethanol' in intro
    parts = [
        lambda r: ('Explain the trend in boiling point from the second to the fourth compound listed.' if not alc else 'Explain why methoxymethane has a higher boiling point than propane.',
                   'More electrons down the group, so stronger instantaneous dipole–induced dipole forces.' if not alc else 'Methoxymethane is polar (C–O dipoles, bent at O) so has pd-pd forces in addition to London forces.', '[2]'),
        lambda r: ('Explain why the first compound has an anomalously high boiling point.' if not alc else 'Explain why ethanol has the highest boiling point.', 'Hydrogen bonding between molecules (H on O/F; lone pairs; δ+ H attracted to lone pair), much stronger than other intermolecular forces.', '[2]'),
        lambda r: ('Draw a diagram showing a hydrogen bond between two molecules of the compound with the highest boiling point, including partial charges and lone pairs.', 'δ+ H of one molecule aligned with a lone pair on O/F of another, shown as a dashed line, with linear X–H···X arrangement.', '[2]'),
        lambda r: ('State the conditions needed for hydrogen bonding.', 'H bonded to N, O or F; lone pair on N, O or F of another molecule.', '[1]'),
        lambda r: ('Describe how instantaneous dipole–induced dipole forces arise.', 'Uneven electron distribution at an instant creates a temporary dipole that induces a dipole in a neighbour.', '[2]'),
        lambda r: ('Explain why ice floats on water.' if grp16 else 'Explain why ethanol mixes with water in all proportions.' if alc else 'Suggest why HF is a weaker acid than HCl, given the strength of the H–F bond.',
                   'Hydrogen bonds hold molecules in an open tetrahedral lattice; ice is less dense than liquid.' if grp16 else 'Ethanol forms hydrogen bonds with water molecules.' if alc else 'The H–F bond is very strong so it dissociates less in water.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(0, 1, 5))


c4reg(t3d, t3d_c4)

# ---------------------------------------------------------- 3.5 bond energy and bond length
BL = [('H–F', 92, 562), ('H–Cl', 127, 431), ('H–Br', 141, 366), ('H–I', 161, 299), ('C–C', 154, 350), ('C=C', 134, 610), ('C≡C', 120, 840), ('Cl–Cl', 199, 244),
      ('Br–Br', 228, 193), ('I–I', 267, 151), ('C–Cl', 177, 340), ('C–Br', 194, 280), ('C–I', 214, 240), ('C–O', 143, 360), ('C=O', 120, 740), ('N≡N', 110, 944), ('O=O', 121, 496)]
BEMOL = [('CH4', 'methane', {'C–H': 4}), ('NH3', 'ammonia', {'N–H': 3}), ('H2O', 'water', {'O–H': 2}), ('C2H6', 'ethane', {'C–C': 1, 'C–H': 6}), ('CH3Cl', 'chloromethane', {'C–H': 3, 'C–Cl': 1}),
         ('C2H4', 'ethene', {'C=C': 1, 'C–H': 4}), ('CH3OH', 'methanol', {'C–H': 3, 'C–O': 1, 'O–H': 1}), ('HCl', 'hydrogen chloride', {'H–Cl': 1}), ('CCl4', 'tetrachloromethane', {'C–Cl': 4})]
BEV = {'C–H': 410, 'N–H': 390, 'O–H': 460, 'C–C': 350, 'C–Cl': 340, 'C=C': 610, 'C–O': 360, 'H–Cl': 431}

t3e = topic('Bond energy and bond length', 'bond energy and bond length', 'bond energy')
t3e.fixed('C1', (1, 2), [
    ('What is meant by bond energy?', 'the energy needed to break one mole of a particular covalent bond in gaseous molecules', 'Bond breaking is endothermic; average bond energies are means over many compounds.', ['the energy released when one mole of a compound forms from its elements', 'the energy needed to melt one mole of a covalent solid', 'the energy needed to remove an electron from a bond']),
    ('Which hydrogen halide has the weakest H–X bond?', 'HI', 'Bond length increases HF < HCl < HBr < HI, so bond energy decreases.', ['HF', 'HCl', 'HBr']),
    ('What is the bond length?', 'the distance between the nuclei of two bonded atoms', 'Measured in pm (or nm); shorter bonds are usually stronger.', ['the distance between the outer electrons of two atoms', 'the radius of the larger atom', 'the length of a molecule']),
    ('Which bond is the shortest?', 'C≡C', 'More shared electron pairs pull nuclei closer: C≡C (120 pm) < C=C (134 pm) < C–C (154 pm).', ['C–C', 'C=C', 'C–Cl']),
    ('Why are average bond energies used in calculations?', 'the energy of a given bond varies slightly from compound to compound', 'Average values over many compounds; calculated ΔH are approximate.', ['bond energies cannot be measured', 'bonds have the same energy in every compound', 'they include intermolecular forces']),
    ('State the relationship generally found between bond length and bond strength.', 'Shorter bonds are generally stronger (higher bond energy).', '[1]'),
])
t3e.fixed('C2', (2, 3, 4), [
    ('Explain why the H–I bond is weaker than the H–Cl bond.', 'I is a larger atom, so the bonding pair is further from the nuclei and the H–I bond is longer; the attraction is weaker.', 'I larger, bond longer [1]; weaker attraction of nuclei for bonding pair [1]'),
    ('Explain why hydrogen iodide decomposes into its elements on heating with a hot wire but hydrogen chloride does not.', 'The H–I bond is much weaker (299 vs 431 kJ mol⁻¹) so less energy is needed to break it.', 'H–I weaker/longer [1]; less energy needed [1]'),
    ('Explain why a C=C bond is shorter and stronger than a C–C bond.', 'Two shared pairs (σ + π) give greater electron density between the nuclei, pulling them closer and increasing attraction.', 'more shared electrons [1]; nuclei pulled closer/stronger attraction [1]'),
    ('Explain why bond energy values from data books are described as average values.', 'The energy of a bond depends on its environment (the rest of the molecule), so values are means over many compounds.', 'varies with environment [1]; mean of many compounds [1]'),
])
errs(t3e, [
    ('Energy is released when bonds are broken.', 'Breaking bonds requires energy (endothermic); energy is released when bonds form.'),
    ('The H–F bond is the weakest hydrogen halide bond because fluorine is the most reactive halogen.', 'H–F is the strongest (562 kJ mol⁻¹) because it is the shortest bond.'),
    ('A C≡C triple bond is three times as strong as a C–C single bond.', 'C≡C (840 kJ mol⁻¹) is less than 3 × 350, because π bonds are weaker than σ bonds.'),
])
c2mix(t3e, ['{p} studies a data table of bond lengths and bond energies.', 'A student in {c} is explaining the thermal stability of the hydrogen halides.'])


@t3e.add('C2', (2, 3), 'explain')
def t3e_cmp(r, D):
    a, b = r.sample(BL, 2)
    st = a if a[2] > b[2] else b
    if D == 2 and r.random() < 0.5:
        return mc(r, f'Bond lengths: {a[0]} {a[1]} pm, {b[0]} {b[1]} pm. Which bond is likely to be stronger?', st[0], [a[0], b[0], 'they have equal strength', 'bond length gives no information'], f'{st[0]}: bond energy {st[2]} kJ mol⁻¹ vs {(b if st is a else a)[2]}.')
    return {'stem': f'The {a[0]} bond has length {a[1]} pm and the {b[0]} bond has length {b[1]} pm. Predict which bond has the higher bond energy and explain your prediction.',
            'answer': f'{st[0]} ({st[2]} kJ mol⁻¹ compared with {(b if st is a else a)[2]} kJ mol⁻¹).' + (' The shorter bond: the bonding electrons are closer to the nuclei, so the attraction is stronger.' if st[1] < (b if st is a else a)[1] else ' Although longer, it involves more shared electrons or more electronegative atoms, so the attraction is stronger.'),
            'key': 'correct bond [1]; reason in terms of bond length / attraction of nuclei for bonding pair [1]'}


@t3e.add('C3', (1, 2, 3, 4), 'numerical')
def t3e_atom(r, D):
    f, nm, bonds = r.choice(BEMOL)
    n = r.choice([0.25, 0.5, 1.5, 2.0, 0.1, 3.0])
    per = sum(BEV[b] * k for b, k in bonds.items())
    lst = ', '.join(f'{b} {BEV[b]}' for b in bonds)
    if D == 1:
        return nmc(r, f'Using the bond energy {lst} kJ mol⁻¹, what is the energy needed to break all the bonds in one mole of gaseous {nm}, {F(f)}?', per, [per / sum(bonds.values()), per * 2, per - 100, per + 100], ' kJ', f'{" + ".join(f"{k} × {BEV[b]}" for b, k in bonds.items())} = {per} kJ.', f=lambda x: str(int(round(x))))
    return {'stem': f'Using the bond energies (kJ mol⁻¹) {lst}, calculate the energy needed to break all the covalent bonds in {n} mol of gaseous {nm}, {F(f)}.',
            'answer': f'{g3(per * n)} kJ', 'key': f'per mole: {" + ".join(f"{k} × {BEV[b]}" for b, k in bonds.items())} = {per} kJ [1]; × {n} = {g3(per * n)} kJ [1]'}


def t3e_c4(r, D):
    intro = P(r, r.choice(['The table shows bond lengths and bond energies for the hydrogen halides: H–F 92 pm 562 kJ mol⁻¹; H–Cl 127 pm 431 kJ mol⁻¹; H–Br 141 pm 366 kJ mol⁻¹; H–I 161 pm 299 kJ mol⁻¹.',
                           '{p} finds the following data in {lab}: C–C 154 pm, 350 kJ mol⁻¹; C=C 134 pm, 610 kJ mol⁻¹; C≡C 120 pm, 840 kJ mol⁻¹.']))
    hx = 'H–F' in intro
    parts = [
        lambda r: ('Define bond energy.', 'Energy needed to break one mole of the bond in gaseous molecules.', '[1]'),
        lambda r: ('Describe and explain the relationship between bond length and bond energy shown by the data.', 'As bond length increases, bond energy decreases: bonding pair further from nuclei, weaker attraction.' if hx else 'More shared pairs → shorter bond and higher bond energy.', '[2]'),
        lambda r: ('Predict the relative thermal stability of the hydrogen halides and explain.' if hx else 'Explain why the energy of C=C is less than twice that of C–C.', 'HF most stable, HI least: H–X bond energy decreases down the group.' if hx else 'The π bond (sideways overlap) is weaker than the σ bond.', '[2]'),
        lambda r: ('Describe what is seen when a red-hot wire is plunged into a tube of hydrogen iodide.' if hx else 'Explain why alkenes are more reactive than alkanes despite the higher C=C bond energy.',
                   'Purple fumes of iodine: HI decomposes.' if hx else 'Only the weaker π bond must break; π electrons are exposed to electrophiles.', '[1]'),
        lambda r: ('Explain why values in data books are average bond energies.', 'Bond energies vary with molecular environment; averaged over many compounds.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2))


c4reg(t3e, t3e_c4)

CHAPTERS[3] = [t3a, t3b, t3c, t3d, t3e]

# ===================================================================== Ch4 States of matter
R_GAS = 8.31
GASES = [('CO2', 'carbon dioxide'), ('CH4', 'methane'), ('C3H8', 'propane'), ('C4H10', 'butane'), ('NH3', 'ammonia'), ('O2', 'oxygen'), ('N2', 'nitrogen'), ('SO2', 'sulfur dioxide'),
         ('Cl2', 'chlorine'), ('Ar', 'argon'), ('C2H6', 'ethane'), ('H2S', 'hydrogen sulfide'), ('NO2', 'nitrogen dioxide'), ('He', 'helium'), ('Ne', 'neon')]
VOLATILE = [('C6H14', 'hexane'), ('C2H5OH', 'ethanol'), ('CH3COCH3', 'propanone'), ('CH2Cl2', 'dichloromethane'), ('C5H12', 'pentane'), ('CH3OH', 'methanol'), ('C7H16', 'heptane'),
            ('CHCl3', 'trichloromethane'), ('C4H10O', 'ethoxyethane'), ('C3H7OH', 'propan-1-ol'), ('C6H6', 'benzene'), ('CH3CH2Br', 'bromoethane')]

t4a = topic('The gaseous state: ideal gas assumptions and limitations', 'the gaseous state: ideal gas assumptions', 'limitations')
t4a.fixed('C1', (1, 2), [
    ('Which is an assumption of the kinetic theory for an ideal gas?', 'there are no intermolecular forces between the molecules', 'Ideal gas: negligible molecular volume, no intermolecular forces, elastic collisions, random motion.', ['the molecules have a large volume', 'collisions between molecules are inelastic', 'the molecules are stationary']),
    ('Under which conditions does a real gas behave most like an ideal gas?', 'high temperature and low pressure', 'Molecules far apart (low p) and fast moving (high T): forces and molecular volume negligible.', ['low temperature and high pressure', 'low temperature and low pressure', 'high temperature and high pressure']),
    ('Which gas behaves least like an ideal gas at room temperature?', 'ammonia', 'NH₃ has hydrogen bonding (strong intermolecular forces).', ['helium', 'neon', 'hydrogen']),
    ('What is meant by an elastic collision?', 'a collision in which no kinetic energy is lost', 'Total kinetic energy is conserved.', ['a collision in which molecules stick together', 'a collision with the container wall only', 'a collision in which energy is converted to heat']),
    ('Why does a gas exert a pressure on its container?', 'molecules collide with the walls of the container', 'Pressure = force per unit area from molecular collisions.', ['molecules repel the walls electrostatically', 'the gas has weight', 'molecules are attracted to the walls']),
    ('State two assumptions made about the molecules of an ideal gas.', 'Any two: negligible volume of molecules; no intermolecular forces; elastic collisions; random constant motion.', '[2]'),
])
t4a.fixed('C2', (2, 3, 4), [
    ('Explain why real gases deviate from ideal behaviour at high pressure.', 'Molecules are close together, so their own volume is no longer negligible compared with the container volume, and intermolecular forces become significant.', 'molecular volume significant [1]; intermolecular forces significant [1]'),
    ('Explain why real gases deviate from ideal behaviour at low temperature.', 'Molecules move more slowly, so intermolecular attractions have a greater effect and reduce the pressure exerted on the walls.', 'slower molecules [1]; attractions significant [1]'),
    ('Explain why helium behaves more like an ideal gas than hydrogen chloride.', 'He atoms are small with only 2 electrons, so very weak London forces; HCl is polar with permanent dipole forces.', 'He weak forces/small [1]; HCl polar, stronger forces [1]'),
    ('Explain, in terms of molecules, why the pressure of a gas in a sealed container increases when it is heated.', 'Molecules gain kinetic energy and move faster, so they collide with the walls more often and with more force.', 'faster molecules [1]; more frequent/forceful collisions [1]'),
])
errs(t4a, [
    ('Gases behave most ideally at high pressure because the molecules collide more often.', 'Gases are most ideal at low pressure, where molecules are far apart and intermolecular forces/molecular volume are negligible.'),
    ('An ideal gas is one whose molecules attract each other strongly.', 'An ideal gas is assumed to have no intermolecular forces.'),
    ('Ammonia behaves more ideally than nitrogen because it has fewer electrons.', 'Ammonia has hydrogen bonding (strong forces), so it deviates more than nitrogen.'),
])
c2mix(t4a, ['{p} investigates how closely gases follow the ideal gas equation.', 'Engineers in {c} must decide whether a gas in a high-pressure cylinder behaves ideally.'])


@t4a.add('C2', (2, 3, 4), 'explain')
def t4a_cmp(r, D):
    a, b = r.sample([('He', 'helium', 0), ('Ne', 'neon', 1), ('N2', 'nitrogen', 2), ('CH4', 'methane', 3), ('CO2', 'carbon dioxide', 4), ('HCl', 'hydrogen chloride', 5), ('SO2', 'sulfur dioxide', 6), ('NH3', 'ammonia', 7), ('H2O', 'steam', 8)], 2)
    ideal = a if a[2] < b[2] else b
    other = b if ideal is a else a
    cond = r.choice([('a pressure of 100 kPa and 400 K', 'low pressure and high temperature'), ('a pressure of 20 000 kPa and 250 K', 'high pressure and low temperature')])
    return {'stem': f'Samples of {a[1]} and {b[1]} are both kept at {cond[0]}. State which behaves more like an ideal gas and explain. Comment on whether these conditions favour ideal behaviour.',
            'answer': f'{ideal[1].capitalize()}: weaker intermolecular forces (smaller/non-polar or fewer electrons) than {other[1]}. These are {cond[1]} conditions, which {"favour" if "low pressure" in cond[1] else "do not favour"} ideal behaviour.',
            'key': 'correct gas [1]; reason in terms of intermolecular forces/size [1]; comment on conditions [1]'}


@t4a.add('C3', (1, 2, 3), 'short')
def t4a_cond(r, D):
    ps = r.sample([50, 100, 500, 2000, 10000, 20000], 2)
    ts = r.sample([200, 273, 300, 500, 800], 2)
    combos = [(ps[0], ts[0]), (ps[0], ts[1]), (ps[1], ts[0]), (ps[1], ts[1])]
    best = min(combos, key=lambda x: (x[0], -x[1]))
    fmt_ = [f'{p} kPa and {t} K' for p, t in combos]
    return mc(r, f'Under which conditions would a sample of {r.choice(["nitrogen", "methane", "carbon dioxide", "oxygen"])} behave most like an ideal gas?', f'{best[0]} kPa and {best[1]} K', fmt_, 'Lowest pressure and highest temperature: molecules far apart and fast moving.')


def t4a_c4(r, D):
    intro = P(r, r.choice(['{p} compares the behaviour of helium and ammonia stored in cylinders in {lab}.', 'A gas-supply company in {c} stores methane at high pressure in steel cylinders.']))
    parts = [
        lambda r: ('State three assumptions of the kinetic theory for an ideal gas.', 'Negligible molecular volume; no intermolecular forces; elastic collisions; random motion.', '[3]'),
        lambda r: ('Explain why gases deviate from ideal behaviour at high pressure.', 'Molecules close together; molecular volume and intermolecular forces significant.', '[2]'),
        lambda r: ('Explain why ammonia deviates more from ideal behaviour than helium.', 'Ammonia has hydrogen bonding/polar; He atoms have very weak London forces.', '[2]'),
        lambda r: ('State the conditions under which a real gas behaves most ideally.', 'High temperature and low pressure.', '[1]'),
        lambda r: ('Explain why the pressure in a cylinder increases if it is left in the sun.', 'Molecules gain kinetic energy, collide with walls more often and harder.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t4a, t4a_c4)

# ---------------------------------------------------------- 4.2 pV = nRT
t4b = topic('Using pV = nRT to calculate relative molecular mass', 'using pv = nrt', 'relative molecular mass')
t4b.fixed('C1', (1, 2), [
    ('In pV = nRT, what are the SI units of V?', 'm³', 'SI units: p in Pa, V in m³, T in K, R = 8.31 J K⁻¹ mol⁻¹.', ['dm³', 'cm³', 'litres']),
    ('What is 25 °C in kelvin?', '298 K', 'T(K) = T(°C) + 273.', ['25 K', '248 K', '273 K']),
    ('Convert 250 cm³ into m³.', '2.50 × 10⁻⁴ m³', '1 m³ = 10⁶ cm³.', ['2.50 × 10⁻¹ m³', '0.250 m³', '2.50 × 10⁻³ m³']),
    ('Which expression gives the relative molecular mass of a gas from the ideal gas equation?', 'M = mRT/pV', 'n = m/M = pV/RT, so M = mRT/pV.', ['M = pV/mRT', 'M = mpV/RT', 'M = RT/mpV']),
    ('What is the value and unit of the gas constant R?', '8.31 J K⁻¹ mol⁻¹', 'R = 8.31 J K⁻¹ mol⁻¹.', ['8.31 kJ mol⁻¹', '0.0821 J K⁻¹', '6.02 × 10²³ mol⁻¹']),
    ('Convert 101 kPa into pascals.', '101 000 Pa (1.01 × 10⁵ Pa)', '[1]'),
])
t4b.fixed('C2', (2, 3, 4), [
    ('Explain why the volatile-liquid (gas syringe) method gives a value of Mr that may be inaccurate for a liquid like ethanol near its boiling point.', 'Near its boiling point the vapour does not behave ideally (strong intermolecular forces/hydrogen bonding), so pV = nRT does not apply exactly.', 'non-ideal near boiling point [1]; intermolecular forces significant [1]'),
    ('Explain why temperatures must be in kelvin in pV = nRT.', 'Volume and pressure are proportional to absolute temperature; the kelvin scale starts at absolute zero, so using °C gives wrong (even negative) values.', 'proportional to absolute T [1]; °C gives wrong values [1]'),
    ('Suggest one source of error when measuring the Mr of a volatile liquid by injecting it into a heated gas syringe.', 'Some liquid may not vaporise or may evaporate from the needle before weighing; temperature of the syringe may not be uniform.', 'identifies error [1]; effect on Mr [1]'),
])
errs(t4b, [
    ('In pV = nRT, the volume can be used in cm³ if the pressure is in kPa.', 'kPa × dm³ gives J, so kPa with dm³ works; but kPa with cm³ does not — use Pa and m³ for SI consistency.'),
    ('At 100 °C, T = 100 in the ideal gas equation.', 'T must be in kelvin: 100 + 273 = 373 K.'),
])
c2mix(t4b, ['{p} measures the relative molecular mass of a volatile liquid using a gas syringe in an oven.', 'A student in {c} uses the ideal gas equation in a set of calculations.'])


@t4b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4b_mr(r, D):
    f, nm = r.choice(GASES)
    M = Mr(f)
    Tc = r.choice([20, 25, 27, 30, 50, 100])
    T = Tc + 273
    p = r.choice([100, 101, 98.5, 102, 150, 200])
    V = r.choice([100, 150, 200, 250, 300, 500])
    n = p * 1000 * V * 1e-6 / (R_GAS * T)
    m = n * M
    if D == 1:
        return nmc(r, f'What amount of gas, in mol, occupies {V} cm³ at {p} kPa and {T} K? (R = 8.31 J K⁻¹ mol⁻¹)', n, [n * 1000, n / 1000, p * V / (R_GAS * T), n * 10], ' mol', f'n = pV/RT = {p * 1000:.0f} × {V}×10⁻⁶ / (8.31 × {T}).')
    if D == 2:
        what = r.choice(['n', 'V'])
        if what == 'V':
            V = r3(n) * R_GAS * T / (p * 1000) * 1e6
            return {'stem': f'Calculate the volume, in cm³, occupied by {g3(n)} mol of {nm} at {p} kPa and {Tc} °C. (R = 8.31 J K⁻¹ mol⁻¹)', 'answer': f'{g3(V)} cm³',
                    'key': f'T = {T} K, p = {p * 1000:.0f} Pa [1]; V = nRT/p = {g3(V * 1e-6)} m³ = {g3(V)} cm³ [1]'}
    stem = f'A sample of gas G of mass {g3(m)} g occupies {V} cm³ at {p} kPa and {Tc} °C. Calculate the relative molecular mass of G. (R = 8.31 J K⁻¹ mol⁻¹)'
    key = f'convert: p = {p * 1000:.0f} Pa, V = {V} × 10⁻⁶ m³, T = {T} K [1]; n = pV/RT = {g3(n)} mol [1]; Mr = m/n = {g3(M)} [1]'
    ans = f'Mr = {g3(M)}'
    if D >= 4:
        opts = r.sample([x for x in GASES if abs(Mr(x[0]) - M) > 3], 3) + [(f, nm)]
        r.shuffle(opts)
        stem += ' G is one of ' + ', '.join(F(o[0]) for o in opts) + '. Identify G.'
        key += f'; identifies {F(f)} (Mr {mr1(M)}) [1]'
        ans += f'; G is {nm}, {F(f)}'
    return {'stem': stem, 'answer': ans, 'key': key}


@t4b.add('C3', (3, 4, 5), 'numerical')
def t4b_syr(r, D):
    f, nm = r.choice(VOLATILE)
    M = Mr(f)
    Tc = r.choice([90, 95, 100, 105, 110])
    T = Tc + 273
    p = r.choice([100, 101, 102])
    V = r.choice([60.0, 72.5, 80.0, 88.0, 95.0, 105.0])
    m = p * 1000 * V * 1e-6 / (R_GAS * T) * M
    m1 = r.choice([10.524, 12.338, 11.906, 13.452])
    return {'stem': f'{who(r)} injects a small amount of liquid L into a gas syringe kept in an oven at {Tc} °C. The hypodermic syringe weighed {m1:.3f} g before and {m1 - m:.3f} g after injection. The vapour occupies {V} cm³ at {p} kPa. Calculate the Mr of L' + (' and suggest its identity from: ' + ', '.join(F(x[0]) for x in r.sample([v for v in VOLATILE if v[0] != f and abs(Mr(v[0]) - M) > 4], 3) + [(f, nm)]) + '.' if D >= 4 else '.'),
            'answer': f'Mr = {g3(M)}' + (f'; L is {nm}' if D >= 4 else ''), 'key': f'mass = {m:.3f} g [1]; n = pV/RT = {p * 1000:.0f} × {V} × 10⁻⁶/(8.31 × {T}) = {g3(m / M)} mol [1]; Mr = {g3(M)} [1]' + (f'; {nm} (Mr {mr1(M)}) [1]' if D >= 4 else '')}


def t4b_c4(r, D):
    f, nm = r.choice(VOLATILE)
    M = Mr(f)
    T = r.choice([363, 373, 383])
    V = r.choice([70.0, 85.0, 96.0])
    p = 101
    m = p * 1000 * V * 1e-6 / (R_GAS * T) * M
    intro = P(r, r.choice([f'{{p}} vaporises {m:.3f} g of a volatile liquid in a gas syringe at {T} K and {p} kPa. The vapour occupies {V} cm³.', f'In {{lab}} in {{c}}, {m:.3f} g of an unknown liquid evaporates completely in a heated syringe, giving {V} cm³ of vapour at {T} K and {p} kPa.']))
    parts = [
        lambda r: ('State the ideal gas equation and the units of each quantity.', 'pV = nRT: p in Pa, V in m³, n in mol, R in J K⁻¹ mol⁻¹, T in K.', '[2]'),
        lambda r: ('Calculate the amount of vapour in mol.', f'{g3(m / M)} mol', '[2]'),
        lambda r: ('Calculate the relative molecular mass of the liquid.', f'{g3(M)}', '[1]'),
        lambda r: (f'The liquid is {nm}. Suggest why the experimental Mr may differ from the true value.', 'Vapour non-ideal near boiling point (intermolecular forces); loss of liquid by evaporation; temperature not uniform.', '[2]'),
        lambda r: ('State one assumption of the ideal gas model that is least valid at high pressure.', 'Volume of molecules negligible / no intermolecular forces.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2))


c4reg(t4b, t4b_c4)

# ---------------------------------------------------------- 4.3 lattices
LATT = {  # name: (structure, mp desc, conducts solid, conducts molten/aq, soluble in water)
    'sodium chloride': ('giant ionic', 'high (801 °C)', 'no', 'yes', 'yes'), 'magnesium oxide': ('giant ionic', 'very high (2852 °C)', 'no', 'yes (molten)', 'no'),
    'diamond': ('giant covalent (giant molecular)', 'very high (~3550 °C)', 'no', 'n/a', 'no'), 'graphite': ('giant covalent with layers', 'very high (~3650 °C)', 'yes', 'n/a', 'no'),
    'silicon(IV) oxide': ('giant covalent (giant molecular)', 'very high (1710 °C)', 'no', 'no', 'no'), 'copper': ('giant metallic', 'high (1085 °C)', 'yes', 'yes', 'no'),
    'iodine': ('simple molecular', 'low (114 °C)', 'no', 'no', 'slightly'), 'ice': ('simple molecular (hydrogen-bonded)', 'low (0 °C)', 'no', 'very slightly', 'n/a'),
    'buckminsterfullerene (C₆₀)': ('simple molecular', 'sublimes ~600 °C', 'no', 'no', 'no'), 'aluminium': ('giant metallic', 'high (660 °C)', 'yes', 'yes', 'no'),
    'sulfur (S₈)': ('simple molecular', 'low (115 °C)', 'no', 'no', 'no'), 'potassium bromide': ('giant ionic', 'high (734 °C)', 'no', 'yes', 'yes'),
    'graphene': ('giant covalent, single layer', 'very high', 'yes', 'n/a', 'no'),
}
STRUCT_EXPL = {
    'giant ionic': 'strong electrostatic attraction between oppositely charged ions throughout the lattice; ions are fixed in the solid but mobile when molten or dissolved',
    'giant covalent': 'many strong covalent bonds throughout the structure must be broken to melt it',
    'giant metallic': 'strong attraction between cations and delocalised electrons; delocalised electrons carry charge',
    'simple molecular': 'only weak intermolecular forces between molecules need to be overcome; no ions or delocalised electrons',
}


def skey(s):
    for k in STRUCT_EXPL:
        if s.startswith(k):
            return k
    return 'simple molecular'


t4c = topic('Liquid and solid states: giant and simple lattices and relating properties to structure', 'liquid and solid states: giant and simple lattices', 'relating properties to structure')
t4c.fixed('C1', (1, 2), [
    ('Which substance has a giant covalent structure?', 'silicon(IV) oxide', 'SiO₂: each Si bonded to four O in a 3D network.', ['iodine', 'sodium chloride', 'carbon dioxide']),
    ('Why does graphite conduct electricity?', 'each carbon atom has one delocalised electron that can move between the layers', 'Each C forms three σ bonds; the fourth electron is delocalised along the layers.', ['it contains ions', 'it is a metal', 'its layers slide over each other']),
    ('What type of lattice does iodine form in the solid state?', 'simple molecular lattice', 'I₂ molecules held by weak London forces in a regular lattice.', ['giant covalent lattice', 'giant ionic lattice', 'giant metallic lattice']),
    ('Why does solid sodium chloride not conduct electricity?', 'its ions are held in fixed positions in the lattice', 'Ions can move only when molten or in aqueous solution.', ['it has no ions', 'its electrons are delocalised', 'it is covalently bonded']),
    ('Which statement about buckminsterfullerene, C₆₀, is correct?', 'it consists of simple molecules and has a relatively low melting point', 'C₆₀ molecules held by intermolecular forces; soft, sublimes, poor conductor.', ['it is a giant covalent lattice like diamond', 'it is an excellent electrical conductor', 'each carbon forms four single bonds']),
    ('State how the atoms are arranged in graphene.', 'A single layer of carbon atoms, each bonded to three others, in hexagonal rings.', '[1]'),
])
t4c.fixed('C2', (2, 3, 4), [
    ('Explain why diamond is very hard but graphite is soft and slippery.', 'In diamond each C is covalently bonded to four others in a rigid 3D network; in graphite layers are held by weak intermolecular forces and can slide.', 'diamond 3D network of strong bonds [1]; graphite layers with weak forces between [1]'),
    ('Explain why magnesium oxide has a much higher melting point than sodium chloride.', 'Mg²⁺ and O²⁻ have higher charges (and are smaller) than Na⁺ and Cl⁻, so the electrostatic attraction between ions is stronger.', 'higher charges/smaller ions [1]; stronger electrostatic attraction [1]'),
    ('Explain why ice has a lower density than water.', 'Hydrogen bonds hold water molecules in an open tetrahedral lattice in ice; when ice melts the structure collapses and molecules pack more closely.', 'open lattice held by H bonds [1]; collapses on melting [1]'),
    ('Explain why metals are malleable.', 'Layers of cations can slide over each other while the delocalised electrons continue to hold them together.', 'layers slide [1]; metallic bonding maintained [1]'),
    ('Explain why iodine has a low melting point even though the I–I bond is covalent.', 'Melting only overcomes the weak London forces between I₂ molecules; the covalent bonds are not broken.', 'weak intermolecular forces [1]; covalent bonds not broken [1]'),
])
errs(t4c, [
    ('Melting silicon(IV) oxide only requires overcoming weak intermolecular forces.', 'SiO₂ is giant covalent: many strong covalent bonds must be broken, so the melting point is very high.'),
    ('Sodium chloride conducts electricity when solid because it contains ions.', 'The ions are fixed in the lattice in the solid; it conducts only when molten or dissolved.'),
    ('Graphite conducts because its layers can slide over each other.', 'Graphite conducts because of delocalised electrons in each layer; sliding layers explain softness.'),
])
c2mix(t4c, ['{p} tests samples of several solids in {lab}.', 'A materials scientist in {c} is choosing a solid for a high-temperature application.'])


@t4c.add('C3', (1, 2, 3, 4), 'short')
def t4c_deduce(r, D):
    nm = r.choice(list(LATT))
    s, mp, cs, cl, sol = LATT[nm]
    k = skey(s)
    if D == 1:
        return mc(r, f'What type of structure does {nm} have?', s, list({v[0] for v in LATT.values()}), f'{nm}: {s}.')
    stem = f'Solid S has a melting point that is {mp.split(" (")[0]}. It {"conducts" if cs == "yes" else "does not conduct"} electricity when solid' + (f' and {"conducts" if cl.startswith("yes") else "does not conduct"} when molten or dissolved' if cl != 'n/a' else '') + f'. It is {"soluble" if sol == "yes" else "insoluble" if sol == "no" else "only slightly soluble"} in water. Deduce the type of structure in S and explain each property.'
    return {'stem': stem, 'answer': f'{s} (e.g. {nm}): {STRUCT_EXPL[k]}.', 'key': f'structure {s} [1]; melting point explained [1]; conductivity explained [1]' + ('; solubility explained [1]' if D >= 4 else '')}


@t4c.add('C2', (2, 3, 4), 'explain')
def t4c_cmp(r, D):
    a, b = r.sample(list(LATT), 2)
    if skey(LATT[a][0]) == skey(LATT[b][0]):
        return None
    prop = r.choice(['melting point', 'electrical conductivity of the solid'])
    return {'stem': f'Compare the {prop} of {a} and {b}. Explain the difference in terms of structure and bonding.',
            'answer': f'{a}: {LATT[a][0]} — {STRUCT_EXPL[skey(LATT[a][0])]}. {b}: {LATT[b][0]} — {STRUCT_EXPL[skey(LATT[b][0])]}.', 'key': 'structure of each [1]; type of force/particles overcome or mobile charge carriers [1]' + ('; comparison stated [1]' if D >= 4 else '')}


def t4c_c4(r, D):
    a, b, c = r.sample(list(LATT), 3)
    intro = P(r, r.choice([f'{{p}} is given samples of {a}, {b} and {c} to classify in {{lab}}.', f'A museum in {{c}} displays {a}, {b} and {c} to illustrate different structures.']))
    parts = [
        lambda r: (f'State the type of structure of each substance.', f'{a}: {LATT[a][0]}; {b}: {LATT[b][0]}; {c}: {LATT[c][0]}', '[3]'),
        lambda r: (f'Explain the melting point of {a}.', f'{LATT[a][1]}: {STRUCT_EXPL[skey(LATT[a][0])]}.', '[2]'),
        lambda r: (f'Explain whether {b} conducts electricity as a solid.', f'{"Yes" if LATT[b][2] == "yes" else "No"}: {STRUCT_EXPL[skey(LATT[b][0])]}.', '[2]'),
        lambda r: ('Describe the structure of graphite and explain why it is used in electrodes and as a lubricant.', 'Layers of hexagonal C rings, each C bonded to three others; delocalised electrons conduct; weak forces between layers allow sliding.', '[3]'),
        lambda r: ('Explain why ice is less dense than water.', 'Open hydrogen-bonded lattice in ice; collapses on melting.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t4c, t4c_c4)

CHAPTERS[4] = [t4a, t4b, t4c]


# ===================================================================== Ch5 Chemical energetics
C_WATER = 4.18
FORM_EQ = [  # compound, correct formation equation, distractors
    ('methane', 'C(s) + 2H₂(g) → CH₄(g)', ['C(g) + 4H(g) → CH₄(g)', 'CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)', '2C(s) + 4H₂(g) → 2CH₄(g)']),
    ('water', 'H₂(g) + ½O₂(g) → H₂O(l)', ['2H₂(g) + O₂(g) → 2H₂O(l)', 'H₂(g) + ½O₂(g) → H₂O(g)', '2H(g) + O(g) → H₂O(l)']),
    ('ethanol', '2C(s) + 3H₂(g) + ½O₂(g) → C₂H₅OH(l)', ['C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l)', 'C₂H₄(g) + H₂O(g) → C₂H₅OH(l)', '4C(s) + 6H₂(g) + O₂(g) → 2C₂H₅OH(l)']),
    ('ammonia', '½N₂(g) + 1½H₂(g) → NH₃(g)', ['N₂(g) + 3H₂(g) → 2NH₃(g)', 'N(g) + 3H(g) → NH₃(g)', '½N₂(g) + 1½H₂(g) → NH₃(l)']),
    ('sodium chloride', 'Na(s) + ½Cl₂(g) → NaCl(s)', ['Na(g) + Cl(g) → NaCl(s)', '2Na(s) + Cl₂(g) → 2NaCl(s)', 'Na⁺(g) + Cl⁻(g) → NaCl(s)']),
    ('calcium carbonate', 'Ca(s) + C(s) + 1½O₂(g) → CaCO₃(s)', ['CaO(s) + CO₂(g) → CaCO₃(s)', 'Ca(s) + C(s) + 3O(g) → CaCO₃(s)', '2Ca(s) + 2C(s) + 3O₂(g) → 2CaCO₃(s)']),
    ('hydrogen chloride', '½H₂(g) + ½Cl₂(g) → HCl(g)', ['H₂(g) + Cl₂(g) → 2HCl(g)', 'H(g) + Cl(g) → HCl(g)', '½H₂(g) + ½Cl₂(g) → HCl(aq)']),
    ('magnesium oxide', 'Mg(s) + ½O₂(g) → MgO(s)', ['2Mg(s) + O₂(g) → 2MgO(s)', 'Mg(g) + O(g) → MgO(s)', 'Mg²⁺(g) + O²⁻(g) → MgO(s)']),
    ('carbon dioxide', 'C(s) + O₂(g) → CO₂(g)', ['C(g) + 2O(g) → CO₂(g)', 'CO(g) + ½O₂(g) → CO₂(g)', 'C(s) + 2O(g) → CO₂(g)']),
    ('glucose', '6C(s) + 6H₂(g) + 3O₂(g) → C₆H₁₂O₆(s)', ['6CO₂(g) + 6H₂O(l) → C₆H₁₂O₆(s) + 6O₂(g)', '6C(g) + 12H(g) + 6O(g) → C₆H₁₂O₆(s)', 'C₆H₁₂O₆(s) + 6O₂(g) → 6CO₂(g) + 6H₂O(l)']),
]
COMB_EQ = [
    ('methane', 'CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)', ['CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)', 'CH₄(g) + 1½O₂(g) → CO(g) + 2H₂O(l)', 'C(s) + 2H₂(g) → CH₄(g)']),
    ('ethanol', 'C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l)', ['C₂H₅OH(g) + 3O₂(g) → 2CO₂(g) + 3H₂O(g)', '2C₂H₅OH(l) + 6O₂(g) → 4CO₂(g) + 6H₂O(l)', 'C₂H₅OH(l) + 2O₂(g) → 2CO(g) + 3H₂O(l)']),
    ('propane', 'C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(l)', ['C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(g)', 'C₃H₈(g) + 3½O₂(g) → 3CO(g) + 4H₂O(l)', '2C₃H₈(g) + 10O₂(g) → 6CO₂(g) + 8H₂O(l)']),
    ('hydrogen', 'H₂(g) + ½O₂(g) → H₂O(l)', ['2H₂(g) + O₂(g) → 2H₂O(l)', 'H₂(g) + ½O₂(g) → H₂O(g)', 'H₂(g) + O(g) → H₂O(l)']),
    ('methanol', 'CH₃OH(l) + 1½O₂(g) → CO₂(g) + 2H₂O(l)', ['2CH₃OH(l) + 3O₂(g) → 2CO₂(g) + 4H₂O(l)', 'CH₃OH(l) + O₂(g) → CO(g) + 2H₂O(l)', 'CH₃OH(g) + 1½O₂(g) → CO₂(g) + 2H₂O(g)']),
    ('butane', 'C₄H₁₀(g) + 6½O₂(g) → 4CO₂(g) + 5H₂O(l)', ['2C₄H₁₀(g) + 13O₂(g) → 8CO₂(g) + 10H₂O(l)', 'C₄H₁₀(g) + 6½O₂(g) → 4CO₂(g) + 5H₂O(g)', 'C₄H₁₀(g) + 4½O₂(g) → 4CO(g) + 5H₂O(l)']),
    ('carbon (graphite)', 'C(s) + O₂(g) → CO₂(g)', ['C(s) + ½O₂(g) → CO(g)', 'C(g) + O₂(g) → CO₂(g)', 'CO(g) + ½O₂(g) → CO₂(g)']),
]
FUELS = [('methanol', 'CH3OH', -726), ('ethanol', 'C2H5OH', -1367), ('propan-1-ol', 'C3H7OH', -2021), ('butan-1-ol', 'C4H9OH', -2676), ('pentan-1-ol', 'C5H11OH', -3329), ('hexane', 'C6H14', -4163), ('heptane', 'C7H16', -4817)]

t5a = topic('Enthalpy change, standard conditions and definitions of ΔH (reaction, formation, combustion, neutralisation)', 'enthalpy change, standard conditions', 'definitions of δh')
t5a.fixed('C1', (1, 2), [
    ('What are the standard conditions used for standard enthalpy changes?', '298 K and 101 kPa', 'Standard conditions: 298 K, 101 kPa, solutions 1.00 mol dm⁻³, substances in standard states.', ['273 K and 101 kPa', '298 K and 1 kPa', '0 °C and 100 kPa']),
    ('Which statement describes an exothermic reaction?', 'ΔH is negative and energy is transferred to the surroundings', 'Exothermic: products lower in enthalpy than reactants; temperature of surroundings rises.', ['ΔH is positive and the surroundings cool', 'ΔH is negative and the surroundings cool', 'ΔH is zero']),
    ('What is the standard enthalpy change of formation of an element in its standard state?', 'zero', 'By definition ΔHf of an element in its standard state is 0.', ['always positive', 'always negative', 'equal to its enthalpy of atomisation']),
    ('What is the standard enthalpy change of neutralisation?', 'the enthalpy change when one mole of water is formed by the reaction of an acid with an alkali under standard conditions', 'H⁺(aq) + OH⁻(aq) → H₂O(l), about −57 kJ mol⁻¹ for strong acid + strong base.', ['the enthalpy change when one mole of acid reacts completely', 'the enthalpy change when one mole of salt dissolves', 'the energy needed to neutralise one mole of base']),
    ('On a reaction pathway diagram for an endothermic reaction, where are the products?', 'above the reactants', 'Endothermic: ΔH positive, products at higher enthalpy.', ['below the reactants', 'at the same level as the reactants', 'at the top of the activation energy hump']),
    ('Define standard enthalpy change of combustion.', 'The enthalpy change when one mole of a substance is burned completely in excess oxygen under standard conditions (298 K, 101 kPa).', '[2]'),
])
t5a.fixed('C2', (2, 3, 4), [
    ('Explain why the standard enthalpy change of neutralisation for HCl and NaOH is the same as for HNO₃ and KOH.', 'Both are strong acids and strong bases, fully ionised; the reaction in each case is H⁺(aq) + OH⁻(aq) → H₂O(l).', 'fully ionised [1]; same ionic equation [1]'),
    ('Explain why the enthalpy change of neutralisation of ethanoic acid with NaOH is less exothermic than that of HCl with NaOH.', 'Ethanoic acid is weak and only partly ionised; some energy is used to ionise it as it reacts.', 'weak acid partly ionised [1]; energy used for ionisation [1]'),
    ('Explain, in terms of bond breaking and bond making, why a reaction is exothermic.', 'More energy is released in forming the bonds in the products than is absorbed in breaking the bonds in the reactants.', 'bond breaking endothermic, making exothermic [1]; energy released > absorbed [1]'),
    ('Explain why standard conditions must be stated for enthalpy changes.', 'Enthalpy changes depend on temperature, pressure, concentration and physical states, so a reference is needed to compare values.', 'ΔH depends on conditions/states [1]; allows comparison [1]'),
])
errs(t5a, [
    ('The standard enthalpy change of formation of water is the enthalpy change for 2H₂(g) + O₂(g) → 2H₂O(l).', 'ΔHf refers to one mole of product: H₂(g) + ½O₂(g) → H₂O(l).'),
    ('An exothermic reaction has a positive ΔH because heat is given out.', 'Exothermic reactions have a negative ΔH: the system loses enthalpy to the surroundings.'),
    ('Standard conditions are 0 °C and 1 atm.', 'For standard enthalpy changes the conditions are 298 K (25 °C) and 101 kPa.'),
])
c2mix(t5a, ['{p} is writing equations to represent standard enthalpy changes.', 'A student in {c} is comparing exothermic and endothermic processes.'])


@t5a.add('C1', (1, 2, 3))
def t5a_eq(r, D):
    if r.random() < 0.5:
        nm, right, wr = r.choice(FORM_EQ)
        return mc(r, f'Which equation represents the standard enthalpy change of formation of {nm}?', right, wr, f'ΔHf: one mole of compound from its elements in their standard states: {right}.')
    nm, right, wr = r.choice(COMB_EQ)
    return mc(r, f'Which equation represents the standard enthalpy change of combustion of {nm}?', right, wr, f'ΔHc: one mole burned completely in oxygen, products in standard states: {right}.')


@t5a.add('C3', (1, 2, 3), 'short')
def t5a_profile(r, D):
    dh = r.choice([-286, -92, -57, -890, +52, +178, +90, +206, -197, +131])
    ea = r.choice([60, 75, 120, 150, 180, 240])
    if dh > 0 and ea < dh:
        ea = dh + r.choice([40, 80, 120])
    rev = ea - dh
    if D == 1:
        return nmc(r, f'A reaction has ΔH = {sgn(dh)} kJ mol⁻¹ and activation energy {ea} kJ mol⁻¹. What is the activation energy of the reverse reaction?', rev, [ea + dh, ea, abs(dh), ea * 2], ' kJ mol⁻¹', f'Ea(reverse) = Ea − ΔH = {rev} kJ mol⁻¹.', f=lambda x: str(int(x)))
    return {'stem': f'A reaction has ΔH = {sgn(dh)} kJ mol⁻¹ and an activation energy of {ea} kJ mol⁻¹. Sketch a labelled reaction pathway diagram and calculate the activation energy of the reverse reaction.',
            'answer': f'{"exothermic: products below reactants" if dh < 0 else "endothermic: products above reactants"}; Ea(reverse) = {rev} kJ mol⁻¹', 'key': f'products {"below" if dh < 0 else "above"} reactants with ΔH labelled [1]; Ea hump labelled from reactants [1]; Ea(reverse) = {ea} − ({sgn(dh)}) = {rev} kJ mol⁻¹ [1]'}


def t5a_c4(r, D):
    nm, right, _ = r.choice(COMB_EQ)
    intro = P(r, r.choice([f'{{p}} is studying the combustion of {nm} as a fuel for a project in {{c}}.', f'A fuel company in {{c}} reports enthalpy data for {nm}.']))
    parts = [
        lambda r: ('State the meaning of the term standard conditions.', '298 K and 101 kPa (solutions 1 mol dm⁻³).', '[1]'),
        lambda r: (f'Define standard enthalpy change of combustion and write the equation for {nm}.', f'One mole burned completely in excess O₂ under standard conditions; {right}', '[2]'),
        lambda r: ('Explain why combustion is exothermic in terms of bonds.', 'Energy released forming bonds in CO₂/H₂O exceeds energy absorbed breaking bonds in fuel and O₂.', '[2]'),
        lambda r: ('Sketch a reaction pathway diagram for the combustion, labelling ΔH and Ea.', 'Products below reactants; ΔH negative arrow down; Ea from reactants to peak.', '[2]'),
        lambda r: ('Explain why the fuel does not burn until it is ignited.', 'The activation energy must be supplied to break bonds and start the reaction.', '[1]'),
        lambda r: ('Write the equation for the standard enthalpy change of formation of water.', 'H₂(g) + ½O₂(g) → H₂O(l)', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t5a, t5a_c4)

# ---------------------------------------------------------- 5.2 calorimetry
t5b = topic('Calorimetry: calculating enthalpy change from q = mcΔT', 'calorimetry: calculating enthalpy change', 'q = mcδt')
t5b.fixed('C1', (1, 2), [
    ('In q = mcΔT, what does c represent?', 'the specific heat capacity of the liquid being heated', 'c of water/dilute solutions = 4.18 J g⁻¹ K⁻¹.', ['the concentration of the solution', 'the heat capacity of the calorimeter only', 'the speed of light']),
    ('Why is a polystyrene cup used as a calorimeter for reactions in solution?', 'it is a good thermal insulator with a low heat capacity', 'Reduces heat loss to the surroundings.', ['it reacts with the solution', 'it conducts heat quickly', 'it is transparent']),
    ('What is the main source of error in measuring an enthalpy change of combustion using a spirit burner and a copper can?', 'heat loss to the surroundings', 'Much heat escapes to the air; also incomplete combustion; so the value is less exothermic than the data book.', ['the thermometer is too accurate', 'the fuel is too pure', 'the water is too dense']),
    ('What mass is used for m when 25.0 cm³ of acid is mixed with 25.0 cm³ of alkali?', '50.0 g', 'Assume density 1.00 g cm⁻³: total volume 50.0 cm³ → 50.0 g.', ['25.0 g', '1.00 g', 'the mass of acid only']),
    ('Why is the temperature change extrapolated back to the time of mixing on a temperature–time graph?', 'to allow for heat lost while the reaction was taking place', 'Extrapolation estimates the maximum temperature change if no heat were lost.', ['to make the graph look straight', 'to measure the activation energy', 'because thermometers react slowly']),
    ('State two assumptions made when calculating ΔH from a reaction in a polystyrene cup.', 'Solution has density 1.00 g cm⁻³; specific heat capacity of water (4.18 J g⁻¹ K⁻¹); no heat lost; heat capacity of cup negligible.', '[2]'),
])
t5b.fixed('C2', (2, 3, 4), [
    ('Explain why the experimental enthalpy change of combustion of ethanol is much less exothermic than the data-book value.', 'Heat is lost to the surroundings (air, can); incomplete combustion; evaporation of fuel; non-standard conditions.', 'heat loss [1]; one other valid reason [1]'),
    ('Suggest two improvements to a spirit-burner experiment to obtain a more accurate value of ΔHc.', 'Use a draught shield/lid; insulate the can; use a copper calorimeter; keep the flame close; put a cap on the burner when weighing; stir the water.', 'any two improvements [2]'),
    ('Explain why the temperature rise is the same when 50 cm³ of 1.0 mol dm⁻³ HCl is neutralised by 50 cm³ of 1.0 mol dm⁻³ NaOH as when 100 cm³ of each is used.', 'Twice the amount of water forms, releasing twice the energy, but this heats twice the mass of solution, so ΔT is the same.', 'energy doubles [1]; mass doubles, same ΔT [1]'),
])
errs(t5b, [
    ('In q = mcΔT, m is the mass of fuel burned.', 'm is the mass of the water (or solution) being heated.'),
    ('If the temperature rises by 10 °C then ΔT must be converted to 283 K.', 'A temperature change of 10 °C is the same as 10 K; no 273 is added to a difference.'),
    ('The enthalpy change is positive because the temperature of the water went up.', 'A rise in temperature of the surroundings means the reaction is exothermic, so ΔH is negative.'),
])
c2mix(t5b, ['{p} measures enthalpy changes using a polystyrene cup in {lab}.', 'A school in {c} investigates the energy released by different fuels.'])


@t5b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5b_fuel(r, D):
    nm, f, dhc = r.choice(FUELS)
    M = Mr(f)
    eff = r.choice([0.35, 0.4, 0.45, 0.5, 0.55, 0.6])
    mw = r.choice([100, 150, 200, 250])
    mf = r.choice([0.50, 0.60, 0.75, 0.80, 1.00, 1.20])
    q = mf / M * (-dhc) * 1000 * eff
    dT = q / (mw * C_WATER)
    dT = round(dT, 1)
    if dT > 80 or dT < 3:
        return None
    q = mw * C_WATER * dT
    n = mf / M
    dh = -q / 1000 / n
    if D == 1:
        return nmc(r, f'{mw} g of water is heated from 20.0 °C to {20 + dT:.1f} °C. How much energy is transferred to the water? (c = 4.18 J g⁻¹ K⁻¹)', q, [q / 1000, mw * C_WATER * (20 + dT), q * 2, mw * dT], ' J', f'q = {mw} × 4.18 × {dT:.1f} = {g3(q)} J.')
    stem = f'{who(r)} burns {mf:.2f} g of {nm}, {F(f)}, in a spirit burner under a copper can containing {mw} g of water. The temperature of the water rises by {dT:.1f} °C. Calculate the enthalpy change of combustion of {nm} in kJ mol⁻¹. (c = 4.18 J g⁻¹ K⁻¹)'
    key = f'q = {mw} × 4.18 × {dT:.1f} = {g3(q)} J [1]; n = {mf:.2f}/{mr1(M)} = {g3(n)} mol [1]; ΔH = −{g3(q / 1000)}/{g3(n)} = {g3(dh)} kJ mol⁻¹ (negative sign) [1]'
    ans = f'{g3(dh)} kJ mol⁻¹'
    if D >= 4:
        stem += f' The data-book value is {dhc} kJ mol⁻¹. Calculate the percentage of the energy released that was transferred to the water and suggest one reason for the difference.'
        key += f'; {g3(dh / dhc * 100)}% [1]; heat loss / incomplete combustion [1]'
        ans += f'; {g3(dh / dhc * 100)}%; heat lost to the surroundings'
    return {'stem': stem, 'answer': ans, 'key': key}


@t5b.add('C3', (2, 3, 4, 5), 'numerical')
def t5b_neut(r, D):
    acid = r.choice([('hydrochloric acid', 1), ('nitric acid', 1), ('sulfuric acid', 2)])
    alk = r.choice(['sodium hydroxide', 'potassium hydroxide'])
    Va, Vb = r.choice([(25.0, 25.0), (50.0, 50.0), (25.0, 50.0), (30.0, 30.0), (40.0, 40.0)])
    ca = r.choice([1.00, 2.00, 0.500, 1.50])
    cb = r.choice([1.00, 2.00, 0.500, 1.50])
    nH = ca * Va / 1000 * acid[1]
    nOH = cb * Vb / 1000
    nw = min(nH, nOH)
    dT = round(nw * 57.1 * 1000 / ((Va + Vb) * C_WATER), 1)
    if dT < 2:
        return None
    q = (Va + Vb) * C_WATER * dT
    dh = -q / 1000 / nw
    return {'stem': f'{who(r)} mixes {Va} cm³ of {ca:.2f} mol dm⁻³ {acid[0]} with {Vb} cm³ of {cb:.2f} mol dm⁻³ {alk} in a polystyrene cup. The temperature rises by {dT:.1f} °C. Calculate the enthalpy change of neutralisation. Assume the solution has density 1.00 g cm⁻³ and c = 4.18 J g⁻¹ K⁻¹.',
            'answer': f'{g3(dh)} kJ mol⁻¹', 'key': f'q = {Va + Vb:.0f} × 4.18 × {dT:.1f} = {g3(q)} J [1]; n(H⁺) = {g3(nH)}, n(OH⁻) = {g3(nOH)}, so n(H₂O) = {g3(nw)} mol [1]; ΔH = −{g3(q / 1000)}/{g3(nw)} = {g3(dh)} kJ mol⁻¹ [1]'}


@t5b.add('C3', (3, 4, 5), 'numerical')
def t5b_disp(r, D):
    kind = r.choice(['zinc', 'magnesium', 'iron', 'dissolve'])
    V = r.choice([25.0, 50.0, 100.0])
    if kind == 'dissolve':
        salt, dh_true, Mx = r.choice([('ammonium nitrate', 25.7, 80.0), ('potassium chloride', 17.2, 74.6), ('ammonium chloride', 14.8, 53.5), ('potassium nitrate', 34.9, 101.1)])
        m = r.choice([2.00, 3.00, 4.00, 5.00])
        n = m / Mx
        dT = -round(n * dh_true * 1000 / (V * C_WATER), 1)
        if dT > -0.5:
            return None
        q = V * C_WATER * dT
        dh = -q / 1000 / n
        return {'stem': f'{m:.2f} g of {salt} (Mr {Mx}) is dissolved in {V} cm³ of water in a polystyrene cup. The temperature falls by {-dT:.1f} °C. Calculate the enthalpy change of solution of {salt}, assuming c = 4.18 J g⁻¹ K⁻¹ and that the mass heated is that of the water.',
                'answer': f'{sgn(dh, 1)} kJ mol⁻¹', 'key': f'q = {V:.0f} × 4.18 × {-dT:.1f} = {g3(-q)} J absorbed [1]; n = {m:.2f}/{Mx} = {g3(n)} mol [1]; ΔH = +{g3(-q / 1000)}/{g3(n)} = {sgn(dh, 1)} kJ mol⁻¹ (positive, endothermic) [1]'}
    metal, Mm, dh_true = {'zinc': ('zinc', 65.4, -217), 'magnesium': ('magnesium', 24.3, -532), 'iron': ('iron', 55.8, -152)}[kind]
    c = r.choice([0.200, 0.500, 1.00])
    nCu = c * V / 1000
    dT = round(nCu * -dh_true * 1000 / (V * C_WATER), 1)
    q = V * C_WATER * dT
    dh = -q / 1000 / nCu
    return {'stem': f'{who(r)} adds an excess of {metal} powder to {V} cm³ of {c:.3f} mol dm⁻³ copper(II) sulfate solution. The maximum temperature rise, found by extrapolation, is {dT:.1f} °C. Calculate the enthalpy change for the reaction {E(("Zn" if kind == "zinc" else "Mg" if kind == "magnesium" else "Fe") + " + CuSO4 -> " + ("Zn" if kind == "zinc" else "Mg" if kind == "magnesium" else "Fe") + "SO4 + Cu")}. (c = 4.18 J g⁻¹ K⁻¹; density 1.00 g cm⁻³)',
            'answer': f'{g3(dh)} kJ mol⁻¹', 'key': f'q = {V:.0f} × 4.18 × {dT:.1f} = {g3(q)} J [1]; n(CuSO₄) = {g3(nCu)} mol (metal in excess) [1]; ΔH = −{g3(q / 1000)}/{g3(nCu)} = {g3(dh)} kJ mol⁻¹ [1]'}


def t5b_c4(r, D):
    nm, f, dhc = r.choice(FUELS[:5])
    M = Mr(f)
    mw = 200
    mf = r.choice([0.60, 0.80, 0.90])
    dT = round(mf / M * (-dhc) * 1000 * 0.45 / (mw * C_WATER), 1)
    q = mw * C_WATER * dT
    dh = -q / 1000 / (mf / M)
    intro = P(r, r.choice([f'{{p}} burns {mf:.2f} g of {nm} in a spirit burner to heat 200 g of water in a copper can. The temperature rises by {dT:.1f} °C.',
                           f'In {{lab}} in {{c}}, students heat 200 g of water using {mf:.2f} g of {nm}. The water temperature increases by {dT:.1f} °C.']))
    parts = [
        lambda r: ('Calculate the energy transferred to the water.', f'{g3(q)} J', '[1]'),
        lambda r: (f'Calculate the enthalpy change of combustion of {nm}.', f'{g3(dh)} kJ mol⁻¹', f'n = {mf:.2f}/{mr1(M)}; ΔH = −q/n [2]'),
        lambda r: (f'The data-book value is {dhc} kJ mol⁻¹. Suggest two reasons for the difference.', 'Heat loss to surroundings; incomplete combustion; heat absorbed by can; evaporation of fuel.', '[2]'),
        lambda r: ('Suggest two improvements to the experiment.', 'Draught shield/insulation; lid; reduce distance from flame; weigh burner with cap on.', '[2]'),
        lambda r: ('Write the equation for the complete combustion, with state symbols.', [x[1] for x in COMB_EQ if x[0] == nm][0] if any(x[0] == nm for x in COMB_EQ) else E(f'{f}(l) + ' + {'propan-1-ol': '4½O2(g) -> 3CO2(g) + 4H2O(l)', 'butan-1-ol': '6O2(g) -> 4CO2(g) + 5H2O(l)', 'pentan-1-ol': '7½O2(g) -> 5CO2(g) + 6H2O(l)'}.get(nm, '3O2(g) -> 2CO2(g) + 3H2O(l)')), '[2]'),
        lambda r: ('The thermometer reads to ±0.5 °C. Calculate the percentage uncertainty in the temperature rise.', f'{g3(1.0 / dT * 100)}%', 'two readings: ±1.0 °C on ΔT [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(0, 1, 2, 5))


c4reg(t5b, t5b_c4)

# ---------------------------------------------------------- 5.3 Hess's law
HF = {'CO2(g)': -394, 'H2O(l)': -286, 'H2O(g)': -242, 'CH4(g)': -75, 'C2H6(g)': -85, 'C3H8(g)': -105, 'C2H4(g)': +52, 'C2H5OH(l)': -277, 'CH3OH(l)': -239, 'NH3(g)': -46,
      'NO(g)': +90, 'NO2(g)': +33, 'SO2(g)': -297, 'SO3(g)': -396, 'HCl(g)': -92, 'CaCO3(s)': -1207, 'CaO(s)': -635, 'Fe2O3(s)': -824, 'Al2O3(s)': -1676, 'CO(g)': -111,
      'MgO(s)': -602, 'N2O4(g)': +9, 'C6H12O6(s)': -1273, 'H2O2(l)': -188, 'C4H10(g)': -126, 'NaHCO3(s)': -951, 'Na2CO3(s)': -1131, 'NH4Cl(s)': -314, 'C3H6(g)': +20,
      'CH3COOH(l)': -484, 'PCl3(l)': -320, 'PCl5(s)': -444, 'Fe3O4(s)': -1118, 'H2S(g)': -21}
HESS = ['CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)', '2C2H6(g) + 7O2(g) -> 4CO2(g) + 6H2O(l)', 'C2H4(g) + H2(g) -> C2H6(g)', 'C2H4(g) + H2O(g) -> C2H5OH(l)', 'CaCO3(s) -> CaO(s) + CO2(g)',
        'Fe2O3(s) + 3CO(g) -> 2Fe(s) + 3CO2(g)', '4NH3(g) + 5O2(g) -> 4NO(g) + 6H2O(g)', '2SO2(g) + O2(g) -> 2SO3(g)', 'Fe2O3(s) + 2Al(s) -> Al2O3(s) + 2Fe(s)',
        'C2H5OH(l) + 3O2(g) -> 2CO2(g) + 3H2O(l)', 'N2O4(g) -> 2NO2(g)', '2NO(g) + O2(g) -> 2NO2(g)', '2CH3OH(l) + 3O2(g) -> 2CO2(g) + 4H2O(l)', '2NaHCO3(s) -> Na2CO3(s) + H2O(l) + CO2(g)',
        'NH3(g) + HCl(g) -> NH4Cl(s)', 'C3H8(g) -> C3H6(g) + H2(g)', 'C6H12O6(s) + 6O2(g) -> 6CO2(g) + 6H2O(l)', 'CO(g) + 2H2(g) -> CH3OH(l)', '2H2O2(l) -> 2H2O(l) + O2(g)',
        'C4H10(g) -> C2H6(g) + C2H4(g)', 'PCl3(l) + Cl2(g) -> PCl5(s)', '3Fe2O3(s) + CO(g) -> 2Fe3O4(s) + CO2(g)', '2H2S(g) + 3O2(g) -> 2SO2(g) + 2H2O(l)', 'CH3OH(l) + CO(g) -> CH3COOH(l)']
HC = {'C(s)': -394, 'H2(g)': -286, 'CH4(g)': -890, 'C2H6(g)': -1560, 'C3H8(g)': -2220, 'C4H10(g)': -2877, 'C2H4(g)': -1411, 'C2H5OH(l)': -1367, 'CH3OH(l)': -726,
      'C3H6(g)': -2058, 'C3H7OH(l)': -2021, 'C2H2(g)': -1300, 'C6H12(l)': -3920, 'C6H14(l)': -4163}
HC_NAME = {'CH4(g)': 'methane', 'C2H6(g)': 'ethane', 'C3H8(g)': 'propane', 'C4H10(g)': 'butane', 'C2H4(g)': 'ethene', 'C2H5OH(l)': 'ethanol', 'CH3OH(l)': 'methanol',
           'C3H6(g)': 'propene', 'C3H7OH(l)': 'propan-1-ol', 'C2H2(g)': 'ethyne', 'C6H12(l)': 'cyclohexane', 'C6H14(l)': 'hexane'}
HC_RX = [('C2H4(g) + H2(g) -> C2H6(g)', 'hydrogenation of ethene'), ('C3H6(g) + H2(g) -> C3H8(g)', 'hydrogenation of propene'), ('C2H2(g) + 2H2(g) -> C2H6(g)', 'hydrogenation of ethyne'),
         ('C2H4(g) + H2O(l) -> C2H5OH(l)', 'hydration of ethene'), ('C4H10(g) -> C2H6(g) + C2H4(g)', 'cracking of butane'), ('3C2H2(g) -> C6H6(l)', None)]


def sp_tok(eq):
    L, R = eq.split(' -> ')
    def side(s):
        out = []
        for tok in s.split(' + '):
            m = re.match(r'^(\d*)(.*)$', tok)
            out.append((int(m.group(1) or 1), m.group(2)))
        return out
    return side(L), side(R)


def is_el(s):
    return s.split('(')[0] in ('O2', 'H2', 'N2', 'Cl2', 'Fe', 'Al', 'C', 'Mg', 'Na', 'S', 'Ca')


t5c = topic("Hess's law and energy cycles", "hess's law and energy cycles", 'energy cycles')
t5c.fixed('C1', (1, 2), [
    ("What does Hess's law state?", 'the enthalpy change of a reaction is independent of the route taken, provided the initial and final conditions are the same', 'Conservation of energy: ΔH depends only on initial and final states.', ['the enthalpy change depends on the route', 'the enthalpy change is always negative', 'bond energies are the same in all compounds']),
    ('Which formula uses enthalpy changes of formation to find ΔHr?', 'ΔHr = ΣΔHf(products) − ΣΔHf(reactants)', 'Route via elements: reactants → elements → products.', ['ΔHr = ΣΔHf(reactants) − ΣΔHf(products)', 'ΔHr = ΣΔHf(products) + ΣΔHf(reactants)', 'ΔHr = ΣΔHc(products) − ΣΔHc(reactants)']),
    ('Which formula uses enthalpy changes of combustion to find ΔHr?', 'ΔHr = ΣΔHc(reactants) − ΣΔHc(products)', 'Both reactants and products burn to the same CO₂ and H₂O.', ['ΔHr = ΣΔHc(products) − ΣΔHc(reactants)', 'ΔHr = ΣΔHc(products) + ΣΔHc(reactants)', 'ΔHr = ΣΔHf(products) − ΣΔHc(reactants)']),
    ('Why can the enthalpy change of formation of methane not be measured directly?', 'carbon and hydrogen do not react together directly under standard conditions to form only methane', 'So it is found indirectly from enthalpy changes of combustion using Hess’s law.', ['methane is a gas', 'the reaction is endothermic', 'methane has no bonds']),
    ('What is ΔHf of oxygen gas, O₂(g)?', '0 kJ mol⁻¹', 'Element in its standard state.', ['−496 kJ mol⁻¹', '+496 kJ mol⁻¹', '−286 kJ mol⁻¹']),
    ("State Hess's law.", 'The total enthalpy change for a reaction is independent of the route taken, provided the initial and final conditions are the same.', '[1]'),
])
t5c.fixed('C2', (2, 3, 4), [
    ('Explain why Hess’s law is needed to find the enthalpy change for converting anhydrous copper(II) sulfate into hydrated copper(II) sulfate.', 'The reaction cannot be carried out directly in a controlled way and the temperature change cannot be measured; instead ΔH of solution of each solid is measured and combined.', 'direct reaction cannot be measured [1]; two dissolving steps combined [1]'),
    ('Explain why ΔHf values are used with the products minus reactants, but ΔHc values with reactants minus products.', 'In a formation cycle, elements are the common starting point (arrows up to both sides); in a combustion cycle, CO₂ and H₂O are the common end point (arrows down from both sides).', 'formation cycle from elements [1]; combustion cycle to combustion products [1]'),
    ('Explain why the enthalpy change for C(graphite) → C(diamond) is found using combustion data.', 'The conversion cannot be carried out directly under standard conditions; both forms can be burned to CO₂, and the difference gives ΔH.', 'cannot be measured directly [1]; both combust to CO₂ [1]'),
])
errs(t5c, [
    ('ΔHr = ΣΔHf(reactants) − ΣΔHf(products).', 'It is products minus reactants: ΔHr = ΣΔHf(products) − ΣΔHf(reactants).'),
    ('In a Hess cycle, the ΔHf of O₂ must be multiplied by the number of moles of O₂.', 'ΔHf of an element in its standard state is zero, so O₂ contributes nothing.'),
    ('The enthalpy change of a reaction is larger if it is carried out in two steps.', 'Hess’s law: ΔH is the same whatever the route, provided initial and final conditions are the same.'),
])
c2mix(t5c, ['{p} constructs energy cycles using data-book values.', 'A student in {c} uses Hess’s law to find enthalpy changes that cannot be measured directly.'])


def _fmt_sp(s):
    m = re.match(r'^(.*?)(\(\w+\))$', s)
    return F(m.group(1)) + m.group(2) if m else F(s)


def _eqfmt(eq):
    L, R = sp_tok(eq)
    def side(x):
        return ' + '.join((str(k) if k > 1 else '') + _fmt_sp(s) for k, s in x)
    return side(L) + ' → ' + side(R)


@t5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5c_form(r, D):
    eq = r.choice(HESS)
    L, R = sp_tok(eq)
    dh = sum(k * HF[s] for k, s in R if not is_el(s)) - sum(k * HF[s] for k, s in L if not is_el(s))
    data = sorted({s for _, s in L + R if not is_el(s)})
    lst = '; '.join(f'{_fmt_sp(s)} {sgn(HF[s])}' for s in data)
    if D == 1:
        rev = -dh
        return nmc(r, f'Using ΔHf values (kJ mol⁻¹): {lst}, what is ΔH for {_eqfmt(eq)}?', dh, [rev, sum(k * HF[s] for k, s in R if not is_el(s)) + sum(k * HF[s] for k, s in L if not is_el(s)), dh + 100 if dh != -100 else dh - 50, dh * 2 if dh else 10], ' kJ mol⁻¹', f'ΣΔHf(products) − ΣΔHf(reactants) = {sgn(dh)} kJ mol⁻¹.', f=lambda x: sgn(x))
    stem = f'Use the standard enthalpy changes of formation (kJ mol⁻¹) {lst} to calculate the standard enthalpy change for the reaction {_eqfmt(eq)}.'
    key = f'ΣΔHf(products) = {sgn(sum(k * HF[s] for k, s in R if not is_el(s)))} [1]; ΣΔHf(reactants) = {sgn(sum(k * HF[s] for k, s in L if not is_el(s)))} (elements zero) [1]; ΔH = {sgn(dh)} kJ mol⁻¹ [1]'
    if D >= 4:
        stem += ' Draw the energy cycle you used and state whether the reaction is exothermic or endothermic.'
        key += f'; cycle via elements with arrows correct and {"exothermic" if dh < 0 else "endothermic"} [1]'
    return {'stem': stem, 'answer': f'{sgn(dh)} kJ mol⁻¹', 'key': key}


@t5c.add('C3', (2, 3, 4, 5), 'numerical')
def t5c_comb(r, D):
    if r.random() < 0.5:
        sp = r.choice([k for k in HC_NAME if k not in ('C6H12(l)', 'C3H7OH(l)', 'C2H2(g)', 'C6H14(l)')])
        a = atoms(sp.split('(')[0])
        nC, nH, nO = a.get('C', 0), a.get('H', 0), a.get('O', 0)
        dh = nC * HC['C(s)'] + nH / 2 * HC['H2(g)'] - HC[sp]
        o2 = nO / 2
        form = f'{nC if nC > 1 else ""}C(s) + {fmt_half(nH / 2)}H₂(g)' + (f' + {fmt_half(o2)}O₂(g)' if nO else '') + f' → {_fmt_sp(sp)}'
        return {'stem': f'Use the standard enthalpy changes of combustion (kJ mol⁻¹) C(s) −394, H₂(g) −286 and {HC_NAME[sp]} {HC[sp]} to calculate the standard enthalpy change of formation of {HC_NAME[sp]}: {form}.'.replace('-', '−'),
                'answer': f'{sgn(dh)} kJ mol⁻¹', 'key': f'ΔHf = ΣΔHc(reactants) − ΔHc(product) [1]; = {nC}(−394) + {fmt_half(nH / 2)}(−286) − ({HC[sp]}) [1]; = {sgn(dh)} kJ mol⁻¹ [1]'.replace('(-', '(−')}
    eq, nm = r.choice([x for x in HC_RX if x[1]])
    L, R = sp_tok(eq)
    hcv = lambda s: HC.get(s, HC.get(s.replace('(l)', '(g)'), 0)) if not s.startswith('H2O') else 0
    dh = sum(k * hcv(s) for k, s in L) - sum(k * hcv(s) for k, s in R)
    data = sorted({s for _, s in L + R if not s.startswith('H2O')})
    lst = '; '.join(f'{_fmt_sp(s)} {sgn(HC[s])}' for s in data)
    return {'stem': f'Use the standard enthalpy changes of combustion (kJ mol⁻¹) {lst} to calculate the enthalpy change for the {nm}: {_eqfmt(eq)}.',
            'answer': f'{sgn(dh)} kJ mol⁻¹', 'key': f'ΔHr = ΣΔHc(reactants) − ΣΔHc(products) [1]; correct substitution [1]; {sgn(dh)} kJ mol⁻¹ [1]'}


def fmt_half(x):
    if abs(x - round(x)) < 1e-9:
        return '' if round(x) == 1 else str(int(round(x)))
    w = int(x)
    return (str(w) if w else '') + '½'


def t5c_c4(r, D):
    a1 = r.choice([-66.5, -67.0, -66.0])
    a1s = sgn(a1, 1)
    a2 = r.choice([11.5, 11.7, 12.0])
    dh = a1 - a2
    intro = P(r, r.choice([f'{{p}} wants the enthalpy change for CuSO₄(s) + 5H₂O(l) → CuSO₄·5H₂O(s). The enthalpy change of solution of anhydrous CuSO₄ is {a1s} kJ mol⁻¹ and of CuSO₄·5H₂O is +{a2} kJ mol⁻¹.',
                           f'In {{lab}} in {{c}}, students find ΔH(solution) of CuSO₄(s) = {a1s} kJ mol⁻¹ and of CuSO₄·5H₂O(s) = +{a2} kJ mol⁻¹, to find the enthalpy change of hydration of the anhydrous salt.']))
    parts = [
        lambda r: ("State Hess's law.", 'ΔH is independent of the route, provided initial and final conditions are the same.', '[1]'),
        lambda r: ('Draw an energy cycle linking the two solution enthalpies to the hydration reaction.', 'CuSO₄(s) → CuSO₄·5H₂O(s) (ΔH); both → CuSO₄(aq) via ΔH1 and ΔH2.', '[2]'),
        lambda r: ('Calculate the enthalpy change for the hydration of anhydrous copper(II) sulfate.', f'{sgn(dh, 1)} kJ mol⁻¹', f'ΔH = ΔH1 − ΔH2 = {a1s} − (+{a2}) [2]'),
        lambda r: ('Explain why this enthalpy change cannot be measured directly.', 'Water cannot be added in exactly the right amount; hydration is slow/incomplete and the solid’s temperature change cannot be measured.', '[2]'),
        lambda r: ('Describe how the enthalpy change of solution of anhydrous CuSO₄ could be measured.', 'Add a weighed mass of solid to a measured volume of water in a polystyrene cup; record the maximum temperature change; q = mcΔT; ΔH = −q/n.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2))


c4reg(t5c, t5c_c4)

# ---------------------------------------------------------- 5.4 bond energies
BE = {'H–H': 436, 'C–H': 410, 'C–C': 350, 'C=C': 610, 'O=O': 496, 'O–H': 460, 'C=O (in CO₂)': 805, 'C–O': 360, 'N≡N': 944, 'N–H': 390, 'Cl–Cl': 244, 'H–Cl': 431,
      'Br–Br': 193, 'H–Br': 366, 'C–Br': 280, 'C–Cl': 340, 'H–F': 562, 'F–F': 158, 'H–I': 299, 'I–I': 151}
BERX = [  # equation (display), broken, formed
    ('CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)', {'C–H': 4, 'O=O': 2}, {'C=O (in CO₂)': 2, 'O–H': 4}),
    ('C₂H₄(g) + H₂(g) → C₂H₆(g)', {'C=C': 1, 'C–H': 4, 'H–H': 1}, {'C–C': 1, 'C–H': 6}),
    ('H₂(g) + Cl₂(g) → 2HCl(g)', {'H–H': 1, 'Cl–Cl': 1}, {'H–Cl': 2}), ('H₂(g) + Br₂(g) → 2HBr(g)', {'H–H': 1, 'Br–Br': 1}, {'H–Br': 2}),
    ('N₂(g) + 3H₂(g) → 2NH₃(g)', {'N≡N': 1, 'H–H': 3}, {'N–H': 6}), ('C₂H₄(g) + Br₂(g) → CH₂BrCH₂Br(g)', {'C=C': 1, 'C–H': 4, 'Br–Br': 1}, {'C–C': 1, 'C–H': 4, 'C–Br': 2}),
    ('CH₄(g) + Cl₂(g) → CH₃Cl(g) + HCl(g)', {'C–H': 4, 'Cl–Cl': 1}, {'C–H': 3, 'C–Cl': 1, 'H–Cl': 1}),
    ('C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(g)', {'C–C': 2, 'C–H': 8, 'O=O': 5}, {'C=O (in CO₂)': 6, 'O–H': 8}), ('2H₂(g) + O₂(g) → 2H₂O(g)', {'H–H': 2, 'O=O': 1}, {'O–H': 4}),
    ('C₂H₄(g) + H₂O(g) → C₂H₅OH(g)', {'C=C': 1, 'C–H': 4, 'O–H': 2}, {'C–C': 1, 'C–H': 5, 'C–O': 1, 'O–H': 1}),
    ('2CH₃OH(g) + 3O₂(g) → 2CO₂(g) + 4H₂O(g)', {'C–H': 6, 'C–O': 2, 'O–H': 2, 'O=O': 3}, {'C=O (in CO₂)': 4, 'O–H': 8}), ('H₂(g) + F₂(g) → 2HF(g)', {'H–H': 1, 'F–F': 1}, {'H–F': 2}),
    ('H₂(g) + I₂(g) → 2HI(g)', {'H–H': 1, 'I–I': 1}, {'H–I': 2}), ('C₂H₆(g) + Cl₂(g) → C₂H₅Cl(g) + HCl(g)', {'C–H': 6, 'C–C': 1, 'Cl–Cl': 1}, {'C–H': 5, 'C–C': 1, 'C–Cl': 1, 'H–Cl': 1}),
    ('C₂H₄(g) + HBr(g) → C₂H₅Br(g)', {'C=C': 1, 'C–H': 4, 'H–Br': 1}, {'C–C': 1, 'C–H': 5, 'C–Br': 1}),
]


def be_dh(br, fm):
    b = sum(BE[k] * v for k, v in br.items())
    f = sum(BE[k] * v for k, v in fm.items())
    return b, f, b - f


t5d = topic('Using average bond energies to calculate enthalpy change', 'using average bond energies', 'bond energies to calculate enthalpy change')
t5d.fixed('C1', (1, 2), [
    ('Which expression gives ΔH using bond energies?', 'Σ(bond energies of bonds broken) − Σ(bond energies of bonds formed)', 'Breaking is endothermic (+), forming is exothermic (−).', ['Σ(bonds formed) − Σ(bonds broken)', 'Σ(bonds broken) + Σ(bonds formed)', 'ΣΔHf(products) − Σ(bonds broken)']),
    ('Why is ΔH calculated from average bond energies different from the value found by experiment?', 'average bond energies are means over many compounds, and the calculation assumes all species are gases', 'Actual bond energies depend on the molecule; liquids/solids need extra energy terms.', ['bond energies are always measured wrongly', 'Hess’s law does not apply to bonds', 'the reaction is too fast to measure']),
    ('For which type of species are bond-energy calculations valid?', 'gaseous molecules', 'Bond energies are defined for the gaseous state.', ['ionic solids', 'aqueous ions', 'metals']),
    ('Which process is endothermic?', 'breaking the H–H bond in H₂(g)', 'Bond breaking always requires energy.', ['forming an O–H bond', '2H(g) → H₂(g)', 'H(g) + Cl(g) → HCl(g)']),
    ('State why the value of ΔH calculated using bond energies for a reaction producing liquid water differs from the data-book value.', 'Bond energies are for gases; condensing the water releases extra energy, and average values are used.', '[1]'),
])
t5d.fixed('C2', (2, 3, 4), [
    ('Explain why the C=O bond energy used for CO₂ (805 kJ mol⁻¹) differs from the average C=O value (740 kJ mol⁻¹).', 'Bond energy depends on the environment of the bond; the C=O bonds in CO₂ are stronger than the average C=O in aldehydes and ketones.', 'depends on environment [1]; average vs specific [1]'),
    ('Explain why the enthalpy change for H₂ + Cl₂ → 2HCl calculated from bond energies is close to the experimental value.', 'All species are diatomic gases and the bond energies for H–H, Cl–Cl and H–Cl are exact (not averages) for these molecules.', 'gases [1]; bond energies specific to these molecules, not averages [1]'),
])
errs(t5d, [
    ('ΔH = bonds formed − bonds broken.', 'ΔH = Σ(bonds broken) − Σ(bonds formed), since breaking is endothermic and forming is exothermic.'),
    ('In CH₄ + Cl₂ → CH₃Cl + HCl, all four C–H bonds must be included as formed.', 'Only one C–H bond actually breaks; or, counting all bonds, 4 C–H broken and 3 C–H formed — the three unchanged bonds cancel.'),
])
c2mix(t5d, ['{p} calculates enthalpy changes using a table of average bond energies.', 'A student in {c} compares calculated and experimental enthalpy changes.'])


@t5d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5d_calc(r, D):
    eqn, br, fm = r.choice(BERX)
    b, f, dh = be_dh(br, fm)
    keys = sorted(set(br) | set(fm))
    lst = ', '.join(f'{k} {BE[k]}' for k in keys)
    if D == 1:
        return nmc(r, f'Using bond energies (kJ mol⁻¹) {lst}, what is ΔH for {eqn}?', dh, [-dh, b + f, f, b], ' kJ mol⁻¹', f'broken {b} − formed {f} = {sgn(dh)} kJ mol⁻¹.', f=lambda x: sgn(x))
    if D >= 4 and r.random() < 0.5:
        unk = r.choice([k for k in keys if k in fm and k not in br] or keys)
        side = 'formed' if unk in fm else 'broken'
        others = ', '.join(f'{k} {BE[k]}' for k in keys if k != unk)
        return {'stem': f'For the reaction {eqn}, ΔH = {sgn(dh)} kJ mol⁻¹. Use the bond energies (kJ mol⁻¹) {others} to calculate the bond energy of the {unk} bond.',
                'answer': f'{BE[unk]} kJ mol⁻¹', 'key': f'ΔH = Σbroken − Σformed [1]; sets up equation with x for {unk} ({side}) [1]; correct rearrangement [1]; x = {BE[unk]} kJ mol⁻¹ [1]'}
    stem = f'Use the average bond energies (kJ mol⁻¹) {lst} to calculate the enthalpy change for {eqn}.'
    key = f'bonds broken: ' + ' + '.join(f'{v} × {BE[k]}' for k, v in br.items()) + f' = {b} [1]; bonds formed: ' + ' + '.join(f'{v} × {BE[k]}' for k, v in fm.items()) + f' = {f} [1]; ΔH = {b} − {f} = {sgn(dh)} kJ mol⁻¹ [1]'
    if D >= 4:
        stem += ' Suggest why the value differs from the data-book value.'
        key += '; average bond energies used / species not all gaseous in standard state [1]'
    return {'stem': stem, 'answer': f'{sgn(dh)} kJ mol⁻¹', 'key': key}


def t5d_c4(r, D):
    eqn, br, fm = r.choice(BERX)
    b, f, dh = be_dh(br, fm)
    keys = sorted(set(br) | set(fm))
    intro = P(r, r.choice([f'{{p}} uses bond energies (kJ mol⁻¹) ' + ', '.join(f'{k} {BE[k]}' for k in keys) + f' to study the reaction {eqn}.', f'A chemical engineer in {{c}} estimates the enthalpy change of {eqn} from the bond energies ' + ', '.join(f'{k} {BE[k]}' for k in keys) + ' kJ mol⁻¹.']))
    parts = [
        lambda r: ('Define the term bond energy.', 'Energy needed to break one mole of a covalent bond in gaseous molecules (average over many compounds).', '[1]'),
        lambda r: ('Calculate the energy needed to break the bonds in the reactants.', f'{b} kJ', '[1]'),
        lambda r: ('Calculate the enthalpy change of the reaction.', f'{sgn(dh)} kJ mol⁻¹', f'formed {f}; ΔH = {b} − {f} [2]'),
        lambda r: ('Draw an enthalpy profile showing the bond-breaking and bond-forming steps.', 'Reactants → gaseous atoms (up by bonds broken) → products (down by bonds formed); net ΔH labelled.', '[2]'),
        lambda r: ('Explain why the calculated value is only approximate.', 'Average bond energies used; real bond energies depend on the molecule; non-gaseous states.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2))


c4reg(t5d, t5d_c4)

CHAPTERS[5] = [t5a, t5b, t5c, t5d]

# ===================================================================== Ch6 Redox reactions
ONSP = [  # formula (ascii), charge, element, others
    ('KMnO4', 0, 'Mn', {'K': 1, 'O': -2}), ('MnO4', -1, 'Mn', {'O': -2}), ('MnO2', 0, 'Mn', {'O': -2}), ('K2Cr2O7', 0, 'Cr', {'K': 1, 'O': -2}), ('Cr2O7', -2, 'Cr', {'O': -2}),
    ('CrO4', -2, 'Cr', {'O': -2}), ('SO4', -2, 'S', {'O': -2}), ('SO3', -2, 'S', {'O': -2}), ('H2SO4', 0, 'S', {'H': 1, 'O': -2}), ('SO2', 0, 'S', {'O': -2}), ('H2S', 0, 'S', {'H': 1}),
    ('S2O3', -2, 'S', {'O': -2}), ('S4O6', -2, 'S', {'O': -2}), ('NO3', -1, 'N', {'O': -2}), ('NO2', -1, 'N', {'O': -2}), ('NH4', 1, 'N', {'H': 1}), ('NH3', 0, 'N', {'H': 1}),
    ('N2O4', 0, 'N', {'O': -2}), ('NO', 0, 'N', {'O': -2}), ('HNO3', 0, 'N', {'H': 1, 'O': -2}), ('ClO3', -1, 'Cl', {'O': -2}), ('ClO', -1, 'Cl', {'O': -2}), ('NaClO', 0, 'Cl', {'Na': 1, 'O': -2}),
    ('Cl2O7', 0, 'Cl', {'O': -2}), ('HClO4', 0, 'Cl', {'H': 1, 'O': -2}), ('IO3', -1, 'I', {'O': -2}), ('VO2', 1, 'V', {'O': -2}), ('VO', 2, 'V', {'O': -2}), ('Fe3O4', 0, 'Fe', {'O': -2}),
    ('H2O2', 0, 'O', {'H': 1}), ('PCl5', 0, 'P', {'Cl': -1}), ('H3PO4', 0, 'P', {'H': 1, 'O': -2}), ('P4O10', 0, 'P', {'O': -2}), ('C2O4', -2, 'C', {'O': -2}), ('CH4', 0, 'C', {'H': 1}),
    ('CO', 0, 'C', {'O': -2}), ('NaH', 0, 'H', {'Na': 1}), ('OF2', 0, 'O', {'F': -1}), ('Fe(CN)6', -3, 'Fe', {'C': 2, 'N': -3}), ('CaH2', 0, 'H', {'Ca': 2}), ('Na2O2', 0, 'O', {'Na': 1}), ('BrO3', -1, 'Br', {'O': -2}),
    ('CH3OH', 0, 'C', {'H': 1, 'O': -2}), ('HCHO', 0, 'C', {'H': 1, 'O': -2}), ('HCOOH', 0, 'C', {'H': 1, 'O': -2}), ('SiCl4', 0, 'Si', {'Cl': -1}), ('Al2O3', 0, 'Al', {'O': -2}), ('TiCl4', 0, 'Ti', {'Cl': -1}),
]


def on_of(f, ch, el, oth):
    a = atoms(f)
    tot = ch - sum(oth.get(k, 0) * v for k, v in a.items() if k != el)
    return tot / a[el]


def spname(f, ch):
    if not ch:
        return F(f)
    return F(f) + ((str(abs(ch)) if abs(ch) > 1 else '') + ('+' if ch > 0 else '-')).translate(_SUPT)


def on_str(x):
    if abs(x - round(x)) < 1e-9:
        x = int(round(x))
        return ('+' if x > 0 else '−' if x < 0 else '') + str(abs(x))
    from fractions import Fraction
    fr = Fraction(x).limit_denominator(6)
    if fr.denominator == 2:
        return ('+' if x > 0 else '−') + f'{abs(x):.1f}'
    return ('+' if x > 0 else '−') + f'{abs(fr.numerator)}/{fr.denominator}'


t6a = topic('Oxidation numbers of elements in compounds and ions', 'oxidation numbers of elements in compounds and ions', 'oxidation numbers')
t6a.fixed('C1', (1, 2), [
    ('What is the oxidation number of oxygen in hydrogen peroxide, H₂O₂?', '−1', 'Peroxides are an exception: O is −1.', ['−2', '0', '+1']),
    ('What is the oxidation number of hydrogen in sodium hydride, NaH?', '−1', 'In metal hydrides H is −1.', ['+1', '0', '−2']),
    ('What is the sum of the oxidation numbers in the sulfate ion, SO₄²⁻?', '−2', 'Sum of oxidation numbers equals the charge on the ion.', ['0', '+6', '−8']),
    ('What is the oxidation number of any element in its uncombined state?', '0', 'e.g. Cl₂, Fe, O₂, S₈ all have oxidation number 0.', ['+1', 'equal to its group number', 'equal to its valency']),
    ('Which name correctly uses Roman numerals for Fe₂O₃?', 'iron(III) oxide', 'Fe is +3 in Fe₂O₃.', ['iron(II) oxide', 'iron(VI) oxide', 'diiron(III) trioxide(II)']),
    ('State the rule for the sum of oxidation numbers in a neutral compound.', 'They add up to zero.', '[1]'),
])
t6a.fixed('C2', (2, 3, 4), [
    ('Explain why fluorine always has an oxidation number of −1 in its compounds.', 'F is the most electronegative element, so in every bond it attracts the bonding electrons and gains one electron share.', 'most electronegative [1]; always takes −1 [1]'),
    ('Explain why oxygen has an oxidation number of +2 in OF₂.', 'F is more electronegative than O and is −1; the sum is zero so O is +2.', 'F −1 and more electronegative [1]; sum zero gives +2 [1]'),
    ('Explain how the name potassium manganate(VII) shows the oxidation state of manganese.', 'The Roman numeral VII gives the oxidation number of Mn (+7) in the manganate ion MnO₄⁻.', 'Roman numeral = oxidation number [1]; Mn +7 in MnO₄⁻ [1]'),
])
errs(t6a, [
    ('The oxidation number of sulfur in SO₄²⁻ is +8.', 'Sum must equal −2: S + 4(−2) = −2, so S is +6.'),
    ('In Cl₂ the oxidation number of chlorine is −1.', 'In the element Cl₂ the oxidation number is 0.'),
    ('The oxidation number of Cr in Cr₂O₇²⁻ is +12.', '2Cr + 7(−2) = −2 gives 2Cr = +12, so each Cr is +6.'),
])
c2mix(t6a, ['{p} is assigning oxidation numbers to elements in a set of compounds.', 'A student in {c} is naming compounds using Roman numerals.'])


@t6a.add('C1', (1, 2, 3))
def t6a_on(r, D):
    f, ch, el, oth = r.choice(ONSP)
    x = on_of(f, ch, el, oth)
    sp = spname(f, ch)
    right = on_str(x)
    wr = [on_str(x + d) for d in (-2, -1, 1, 2, 4)] + [on_str(-x) if x else '+2']
    return mc(r, f'What is the oxidation number of {el} in {sp}?', right, [w for w in wr if w != right], f'Sum of oxidation numbers = {str(ch).replace("-", "−")}: {el} = {right}.')


@t6a.add('C3', (1, 2, 3, 4), 'short')
def t6a_set(r, D):
    k = 2 if D <= 2 else 3
    pick = r.sample(ONSP, k)
    parts = []
    for f, ch, el, oth in pick:
        parts.append((f'{el} in {spname(f, ch)}', on_str(on_of(f, ch, el, oth))))
    stem = 'Deduce the oxidation number of ' + '; '.join(p[0] for p in parts) + '.'
    if D >= 4:
        stem += ' Name one of these species using a Roman numeral where appropriate.'
    return {'stem': stem, 'answer': '; '.join(f'{p[0]}: {p[1]}' for p in parts), 'key': ' '.join(f'{p[0]} = {p[1]} [1]' for p in parts) + (' name correct [1]' if D >= 4 else '')}


def t6a_c4(r, D):
    pick = r.sample([x for x in ONSP if x[2] in ('Mn', 'Cr', 'S', 'N', 'Cl')], 3)
    intro = P(r, r.choice(['{p} is investigating compounds of transition metals and non-metals used in titrations in {lab}.', 'A water-treatment chemist in {c} uses several oxidising agents and needs their oxidation states.']))
    parts = [lambda r, x=x: (f'Deduce the oxidation number of {x[2]} in {spname(x[0], x[1])}.', on_str(on_of(*x)), '[1]') for x in pick] + [
        lambda r: ('State the rules you used for oxygen and for the sum of oxidation numbers in an ion.', 'O is −2 (except peroxides/OF₂); sum equals the charge on the ion.', '[2]'),
        lambda r: ('Explain, in terms of oxidation number, what happens to manganese when MnO₄⁻ is converted into Mn²⁺.', 'Oxidation number falls from +7 to +2: manganese is reduced (gains 5 electrons).', '[2]'),
        lambda r: ('Name the compound K₂Cr₂O₇ systematically.', 'potassium dichromate(VI)', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t6a, t6a_c4)

# ---------------------------------------------------------- 6.2 redox processes
RXOX = [  # equation, oxidised (species: from->to), reduced, oxidising agent, reducing agent
    ('Zn + Cu^2+ -> Zn^2+ + Cu', 'Zn (0 → +2)', 'Cu²⁺ (+2 → 0)', 'Cu²⁺', 'Zn'), ('Cl2 + 2Br^- -> 2Cl^- + Br2', 'Br⁻ (−1 → 0)', 'Cl₂ (0 → −1)', 'Cl₂', 'Br⁻'),
    ('2Fe^3+ + 2I^- -> 2Fe^2+ + I2', 'I⁻ (−1 → 0)', 'Fe³⁺ (+3 → +2)', 'Fe³⁺', 'I⁻'), ('Fe2O3 + 3CO -> 2Fe + 3CO2', 'C in CO (+2 → +4)', 'Fe in Fe₂O₃ (+3 → 0)', 'Fe₂O₃', 'CO'),
    ('MnO2 + 4HCl -> MnCl2 + Cl2 + 2H2O', 'Cl in HCl (−1 → 0)', 'Mn (+4 → +2)', 'MnO₂', 'HCl'), ('2Mg + O2 -> 2MgO', 'Mg (0 → +2)', 'O (0 → −2)', 'O₂', 'Mg'),
    ('Cu + 4HNO3 -> Cu(NO3)2 + 2NO2 + 2H2O', 'Cu (0 → +2)', 'N (+5 → +4)', 'HNO₃', 'Cu'), ('CuO + H2 -> Cu + H2O', 'H (0 → +1)', 'Cu (+2 → 0)', 'CuO', 'H₂'),
    ('8HI + H2SO4 -> 4I2 + H2S + 4H2O', 'I (−1 → 0)', 'S (+6 → −2)', 'H₂SO₄', 'HI'), ('2Na + Cl2 -> 2NaCl', 'Na (0 → +1)', 'Cl (0 → −1)', 'Cl₂', 'Na'),
    ('Br2 + SO2 + 2H2O -> 2HBr + H2SO4', 'S (+4 → +6)', 'Br (0 → −1)', 'Br₂', 'SO₂'), ('2Al + Fe2O3 -> Al2O3 + 2Fe', 'Al (0 → +3)', 'Fe (+3 → 0)', 'Fe₂O₃', 'Al'),
    ('Mg + 2H^+ -> Mg^2+ + H2', 'Mg (0 → +2)', 'H (+1 → 0)', 'H⁺', 'Mg'), ('2HBr + H2SO4 -> Br2 + SO2 + 2H2O', 'Br (−1 → 0)', 'S (+6 → +4)', 'H₂SO₄', 'HBr'),
    ('4NH3 + 5O2 -> 4NO + 6H2O', 'N (−3 → +2)', 'O (0 → −2)', 'O₂', 'NH₃'), ('2SO2 + O2 -> 2SO3', 'S (+4 → +6)', 'O (0 → −2)', 'O₂', 'SO₂'),
]
DISP = [('Cl2 + 2NaOH -> NaCl + NaClO + H2O', 'chlorine', '0', '−1 (in NaCl)', '+1 (in NaClO)'), ('3Cl2 + 6NaOH -> 5NaCl + NaClO3 + 3H2O', 'chlorine', '0', '−1 (in NaCl)', '+5 (in NaClO₃)'),
        ('2H2O2 -> 2H2O + O2', 'oxygen', '−1', '−2 (in H₂O)', '0 (in O₂)'), ('Cl2 + H2O -> HCl + HClO', 'chlorine', '0', '−1 (in HCl)', '+1 (in HClO)'),
        ('2Cu^+ -> Cu + Cu^2+', 'copper', '+1', '0 (in Cu)', '+2 (in Cu²⁺)'), ('3NO2 + H2O -> 2HNO3 + NO', 'nitrogen', '+4', '+2 (in NO)', '+5 (in HNO₃)')]


def Eq(s):
    out = []
    for tok in s.split(' '):
        if tok == '->':
            out.append('→')
        elif tok in ('+', '...', ';'):
            out.append(tok)
        else:
            m = re.match(r'^(\d*)(.*)$', tok)
            sp = m.group(2)
            if '^' in sp:
                b, c = sp.split('^')
                out.append(m.group(1) + F(b) + c.translate(_SUPT))
            else:
                out.append(m.group(1) + F(sp))
    return ' '.join(out).replace('; ', '').replace('... ', '')


t6b = topic('Redox processes: electron transfer and changes in oxidation number', 'redox processes: electron transfer', 'changes in oxidation number')
t6b.fixed('C1', (1, 2), [
    ('In terms of electrons, what is oxidation?', 'loss of electrons', 'OIL RIG: oxidation is loss, reduction is gain of electrons.', ['gain of electrons', 'gain of protons', 'loss of protons']),
    ('In terms of oxidation number, what is reduction?', 'a decrease in oxidation number', 'Reduction: oxidation number decreases; oxidation: increases.', ['an increase in oxidation number', 'no change in oxidation number', 'gain of oxygen']),
    ('What is an oxidising agent?', 'a species that accepts electrons and is itself reduced', 'Oxidising agent causes oxidation of another species by taking its electrons.', ['a species that loses electrons', 'a species that is itself oxidised', 'a catalyst for redox reactions']),
    ('What is disproportionation?', 'a reaction in which the same element is simultaneously oxidised and reduced', 'e.g. Cl₂ + 2NaOH → NaCl + NaClO + H₂O.', ['a reaction in which two elements swap places', 'decomposition by heat', 'reaction with water']),
    ('Which change is an oxidation?', 'Fe²⁺ → Fe³⁺', 'Fe²⁺ loses one electron; oxidation number +2 → +3.', ['Cl₂ → 2Cl⁻', 'MnO₄⁻ → Mn²⁺', 'Cu²⁺ → Cu']),
    ('State the meaning of the term reducing agent.', 'A species that donates electrons (and is itself oxidised).', '[1]'),
])
t6b.fixed('C2', (2, 3, 4), [
    ('Explain why the reaction Cl₂ + 2NaOH → NaCl + NaClO + H₂O is described as disproportionation.', 'Chlorine (0) is both reduced to −1 in NaCl and oxidised to +1 in NaClO.', 'Cl 0 → −1 reduction [1]; 0 → +1 oxidation [1]'),
    ('Explain why the reaction NaOH + HCl → NaCl + H₂O is not a redox reaction.', 'No element changes oxidation number (Na +1, O −2, H +1, Cl −1 throughout).', 'no change in oxidation numbers [1]; identifies values [1]'),
    ('Explain why oxidation and reduction always occur together.', 'Electrons lost by one species must be gained by another; electrons cannot exist freely in solution.', 'electrons transferred [1]; must be accepted by another species [1]'),
])
errs(t6b, [
    ('In Zn + Cu²⁺ → Zn²⁺ + Cu, zinc is the oxidising agent because it is oxidised.', 'Zinc is oxidised, so it is the reducing agent; Cu²⁺ is the oxidising agent.'),
    ('Reduction is the loss of electrons.', 'Reduction is gain of electrons (OIL RIG).'),
    ('An oxidising agent increases its own oxidation number.', 'An oxidising agent is reduced, so its oxidation number decreases.'),
])
c2mix(t6b, ['{p} is analysing redox reactions met in AS chemistry.', 'A student in {c} identifies oxidising and reducing agents in a set of reactions.'])


@t6b.add('C3', (1, 2, 3, 4), 'short')
def t6b_id(r, D):
    eq, ox, red, oa, ra = r.choice(RXOX)
    e = Eq(eq)
    if D == 1:
        return mc(r, f'In the reaction {e}, which species is the oxidising agent?', oa, [oa, ra, 'H₂O', 'none — it is not a redox reaction', 'both reactants'], f'{oa} is reduced: {red}.')
    stem = f'For the reaction {e}, use oxidation numbers to identify the species oxidised and the species reduced.'
    key = f'oxidised: {ox} [1]; reduced: {red} [1]'
    if D >= 3:
        stem += ' State the oxidising agent and the reducing agent.'
        key += f'; oxidising agent {oa}, reducing agent {ra} [1]'
    return {'stem': stem, 'answer': f'oxidised: {ox}; reduced: {red}' + (f'; oxidising agent {oa}; reducing agent {ra}' if D >= 3 else ''), 'key': key}


@t6b.add('C2', (2, 3, 4), 'explain')
def t6b_disp(r, D):
    eq, el, a, b, c = r.choice(DISP)
    return {'stem': f'Explain, using oxidation numbers, why the reaction {Eq(eq)} is an example of disproportionation.', 'answer': f'The oxidation number of {el} changes from {a} to {b} (reduction) and from {a} to {c} (oxidation): the same element is both oxidised and reduced.',
            'key': f'{el} starts at {a} [1]; changes to {b} and {c} [1]; same element oxidised and reduced [1]' if D >= 3 else 'oxidation numbers correct [1]; same element both oxidised and reduced [1]'}


def t6b_c4(r, D):
    eq, ox, red, oa, ra = r.choice(RXOX)
    intro = P(r, r.choice([f'{{p}} studies the reaction {Eq(eq)} in {{lab}}.', f'An industrial process in {{c}} involves the reaction {Eq(eq)}.']))
    parts = [
        lambda r: ('Define oxidation and reduction in terms of electrons.', 'Oxidation: loss of electrons; reduction: gain of electrons.', '[1]'),
        lambda r: ('Use oxidation numbers to show which element is oxidised and which is reduced.', f'oxidised {ox}; reduced {red}', '[2]'),
        lambda r: ('Identify the oxidising agent and the reducing agent.', f'oxidising agent {oa}; reducing agent {ra}', '[2]'),
        lambda r: ('Explain why this is a redox reaction rather than an acid–base reaction.', 'Oxidation numbers change: electrons are transferred (not protons).', '[1]'),
        lambda r: ('Write the equation for the reaction of chlorine with cold aqueous sodium hydroxide and explain why it is a disproportionation.', 'Cl₂ + 2NaOH → NaCl + NaClO + H₂O; Cl 0 → −1 and 0 → +1.', '[3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t6b, t6b_c4)

# ---------------------------------------------------------- 6.3 balancing redox equations
# reduction half-equations: left dict, right dict (species -> coefficient), electrons on left
HALF = {
    'MnO4': ({'MnO4^-': 1, 'H^+': 8}, {'Mn^2+': 1, 'H2O': 4}, 5, 1.52, 'manganate(VII) ions'),
    'Cr2O7': ({'Cr2O7^2-': 1, 'H^+': 14}, {'Cr^3+': 2, 'H2O': 7}, 6, 1.33, 'dichromate(VI) ions'),
    'H2O2r': ({'H2O2': 1, 'H^+': 2}, {'H2O': 2}, 2, 1.77, 'hydrogen peroxide'),
    'Cl2': ({'Cl2': 1}, {'Cl^-': 2}, 2, 1.36, 'chlorine'), 'Br2': ({'Br2': 1}, {'Br^-': 2}, 2, 1.07, 'bromine'),
    'NO3': ({'NO3^-': 1, 'H^+': 4}, {'NO': 1, 'H2O': 2}, 3, 0.96, 'nitrate ions'), 'Ag': ({'Ag^+': 1}, {'Ag': 1}, 1, 0.80, 'silver ions'),
    'Fe3': ({'Fe^3+': 1}, {'Fe^2+': 1}, 1, 0.77, 'iron(III) ions'), 'O2': ({'O2': 1, 'H^+': 2}, {'H2O2': 1}, 2, 0.68, 'oxygen'),
    'I2': ({'I2': 1}, {'I^-': 2}, 2, 0.54, 'iodine'), 'Cu2': ({'Cu^2+': 1}, {'Cu': 1}, 2, 0.34, 'copper(II) ions'),
    'SO4': ({'SO4^2-': 1, 'H^+': 4}, {'SO2': 1, 'H2O': 2}, 2, 0.17, 'sulfate ions'), 'S4O6': ({'S4O6^2-': 1}, {'S2O3^2-': 2}, 2, 0.09, 'tetrathionate ions'),
    'CO2': ({'CO2': 2}, {'C2O4^2-': 1}, 2, -0.49, 'carbon dioxide'), 'Zn': ({'Zn^2+': 1}, {'Zn': 1}, 2, -0.76, 'zinc ions'),
}
OXID = ['MnO4', 'Cr2O7', 'H2O2r', 'Cl2', 'Br2', 'NO3', 'Ag', 'Fe3', 'I2', 'Cu2']
REDU = {'Fe3': 'iron(II) ions', 'I2': 'iodide ions', 'CO2': 'ethanedioate ions', 'S4O6': 'thiosulfate ions', 'Zn': 'zinc', 'O2': 'hydrogen peroxide', 'SO4': 'sulfur dioxide', 'Br2': 'bromide ions', 'Cu2': 'copper'}


def spf(s):
    if '^' in s:
        b, c = s.split('^')
        return F(b) + c.translate(_SUPT)
    return F(s)


def half_str(k, ox=False):
    L, R, n, _, _ = HALF[k]
    def side(d, extra=''):
        return ' + '.join((str(v) if v > 1 else '') + spf(s) for s, v in d.items()) + extra
    if ox:
        return side(R) + ' → ' + side(L) + f' + {n if n > 1 else ""}e⁻'
    return side(L) + f' + {n if n > 1 else ""}e⁻' + ' → ' + side(R)


def combine(o, rd, force=None):
    Lo, Ro, no, _, _ = HALF[o]
    Lr, Rr, nr, _, _ = HALF[rd]
    l = no * nr // math.gcd(no, nr)
    a, b = force or (l // no, l // nr)
    net = {}
    for s, v in Lo.items():
        net[s] = net.get(s, 0) - a * v
    for s, v in Ro.items():
        net[s] = net.get(s, 0) + a * v
    for s, v in Rr.items():   # reductant: reverse of its reduction
        net[s] = net.get(s, 0) - b * v
    for s, v in Lr.items():
        net[s] = net.get(s, 0) + b * v
    lhs = [(s, -v) for s, v in net.items() if v < 0]
    rhs = [(s, v) for s, v in net.items() if v > 0]
    g = 0
    for _, v in lhs + rhs:
        g = math.gcd(g, v)
    def side(x):
        return ' + '.join((str(v // g) if v // g > 1 else '') + spf(s) for s, v in x)
    return side(lhs) + ' → ' + side(rhs), a // g if g else a, b // g if g else b, l // g if g else l


PAIRS = [('MnO4', 'Fe3'), ('MnO4', 'I2'), ('MnO4', 'CO2'), ('MnO4', 'O2'), ('MnO4', 'SO4'), ('MnO4', 'Br2'), ('Cr2O7', 'Fe3'), ('Cr2O7', 'I2'), ('Cr2O7', 'SO4'), ('Cr2O7', 'CO2'),
         ('H2O2r', 'Fe3'), ('H2O2r', 'I2'), ('Cl2', 'Fe3'), ('Cl2', 'I2'), ('Cl2', 'Br2'), ('Cl2', 'SO4'), ('Cl2', 'O2'), ('Br2', 'Fe3'), ('Br2', 'I2'), ('Br2', 'SO4'), ('NO3', 'Cu2'),
         ('NO3', 'Fe3'), ('Ag', 'Cu2'), ('Ag', 'Zn'), ('Fe3', 'I2'), ('Fe3', 'Cu2'), ('Fe3', 'Zn'), ('Fe3', 'S4O6'), ('Fe3', 'SO4'), ('I2', 'S4O6'), ('I2', 'SO4'), ('Cu2', 'Zn')]
TITR = [  # oxidant species, reductant, ratio ox:red, names
    ('MnO4', 'Fe3', 'KMnO₄', 'iron(II) sulfate', 'Fe²⁺'), ('MnO4', 'CO2', 'KMnO₄', 'sodium ethanedioate', 'C₂O₄²⁻'), ('Cr2O7', 'Fe3', 'K₂Cr₂O₇', 'iron(II) ammonium sulfate', 'Fe²⁺'),
    ('I2', 'S4O6', 'I₂', 'sodium thiosulfate', 'S₂O₃²⁻'), ('MnO4', 'O2', 'KMnO₄', 'hydrogen peroxide', 'H₂O₂')]

t6c = topic('Balancing redox equations using oxidation numbers and half-equations', 'balancing redox equations', 'half-equations')
t6c.fixed('C1', (1, 2), [
    ('How many electrons appear in the half-equation MnO₄⁻ + 8H⁺ + ?e⁻ → Mn²⁺ + 4H₂O?', '5', 'Mn +7 → +2: gains 5 electrons; charge check: −1 + 8 − 5 = +2.', ['3', '7', '8']),
    ('In the half-equation Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O, what is the change in oxidation number of each chromium atom?', '+6 to +3', 'Each Cr gains 3 electrons; two Cr atoms gain 6.', ['+7 to +3', '+6 to +2', '+12 to +6']),
    ('When combining two half-equations, what must be equal?', 'the number of electrons lost and gained', 'Multiply each half-equation so that electrons cancel.', ['the number of H⁺ ions', 'the number of water molecules', 'the masses of reactants']),
    ('Which half-equation shows the oxidation of iodide ions?', '2I⁻ → I₂ + 2e⁻', 'Iodide loses electrons forming iodine.', ['I₂ + 2e⁻ → 2I⁻', 'I⁻ + e⁻ → I²⁻', '2I⁻ + 2e⁻ → I₂']),
    ('What is the mole ratio of MnO₄⁻ to Fe²⁺ in their redox reaction in acid?', '1 : 5', 'MnO₄⁻ gains 5e⁻; each Fe²⁺ loses 1e⁻.', ['1 : 1', '5 : 1', '1 : 2']),
    ('State what is added to balance oxygen atoms in a half-equation in acidic solution.', 'Water molecules (H₂O), then H⁺ ions to balance hydrogen.', '[1]'),
])
t6c.fixed('C2', (2, 3, 4), [
    ('Explain why acid must be added in titrations with potassium manganate(VII).', 'H⁺ ions are needed in the reduction half-equation of MnO₄⁻ to Mn²⁺; without enough acid, brown MnO₂ forms instead.', 'H⁺ is a reactant [1]; otherwise MnO₂ forms [1]'),
    ('Explain why no indicator is needed in a potassium manganate(VII) titration.', 'MnO₄⁻ is purple and Mn²⁺ almost colourless; at the end-point the first excess drop gives a permanent pale pink colour.', 'purple to colourless [1]; first permanent pink at end-point [1]'),
    ('Explain how oxidation numbers can be used to balance the equation for a redox reaction.', 'The total increase in oxidation number of the element oxidised must equal the total decrease of the element reduced; coefficients are chosen to make these equal, then other atoms are balanced.', 'total increase = total decrease [1]; balance remaining atoms/charges [1]'),
])
errs(t6c, [
    ('The half-equation Fe²⁺ → Fe³⁺ shows reduction.', 'Fe²⁺ → Fe³⁺ + e⁻ is oxidation: electrons are lost.'),
    ('In the overall equation, electrons appear on both sides.', 'Electrons must cancel completely in the overall equation.'),
    ('MnO₄⁻ reacts with Fe²⁺ in a 1 : 1 ratio.', 'MnO₄⁻ gains 5 electrons and Fe²⁺ loses 1, so the ratio is 1 : 5.'),
])
c2mix(t6c, ['{p} is constructing overall redox equations from half-equations.', 'A student in {c} carries out redox titrations.'])


@t6c.add('C3', (2, 3, 4, 5), 'short')
def t6c_comb(r, D):
    o, rd = r.choice(PAIRS)
    ov, a, b, ne = combine(o, rd)
    if D == 2:
        wr = [combine(o, rd, f)[0] for f in ((1, 1), (a, b + 1), (a + 1, b), (b, a)) if f != (a, b)] + [ov.split(' → ')[1] + ' → ' + ov.split(' → ')[0]]
        return mc(r, f'Which overall equation is obtained by combining {half_str(o)} and {half_str(rd, ox=True)}?', ov, wr, f'Multiply to transfer {ne} electrons; cancel: {ov}.')
    stem = f'Construct the overall ionic equation for the reaction of {HALF[o][4]} with {REDU[rd]}, using the half-equations {half_str(o)} and {half_str(rd)}.'
    key = f'reverse second half-equation (oxidation of {REDU[rd]}) [1]; multiply so that {ne} electrons are transferred [1]; overall {ov} [1]'
    if D >= 4:
        stem += ' State the change in oxidation number of the element reduced.'
        key += ' oxidation number change of element reduced stated [1]'
    return {'stem': stem, 'answer': ov, 'key': key}


@t6c.add('C3', (2, 3, 4, 5), 'numerical')
def t6c_titr(r, D):
    o, rd, oxn, redn, rsp = r.choice(TITR)
    ov, a, b, ne = combine(o, rd)
    b = b * {'S4O6': 2}.get(rd, 1)   # S₄O₆²⁻ + 2e⁻ → 2S₂O₃²⁻: two thiosulfate per half-equation
    c = r.choice([0.0200, 0.0100, 0.0500, 0.0150])
    titre = r.choice([18.40, 21.20, 22.65, 23.80, 24.35, 19.90])
    nox = c * titre / 1000
    nred = nox * b / a
    conc = nred / 0.025
    stem = f'25.0 cm³ of a solution of {redn} is titrated with {c:.4f} mol dm⁻³ {oxn}' + (' in the presence of dilute sulfuric acid' if o in ('MnO4', 'Cr2O7') else ', using starch indicator near the end-point' if o == 'I2' else '') + f'. The mean titre is {titre:.2f} cm³. The overall equation is {ov}. Calculate the concentration of {rsp} in the solution.'
    key = f'n(oxidant) = {c:.4f} × {titre:.2f}/1000 = {g3(nox)} mol [1]; ratio {a} : {b} so n({rsp}) = {g3(nred)} mol [1]; c = {g3(nred)}/0.0250 = {g3(conc)} mol dm⁻³ [1]'
    ans = f'{g3(conc)} mol dm⁻³'
    if D >= 5 and rd == 'Fe3':
        stem = f'An iron tablet of mass {r.choice([1.20, 1.35, 1.50]):.2f} g is dissolved in dilute sulfuric acid and made up to 250 cm³. ' + stem.replace('25.0 cm³ of a solution of ' + redn, '25.0 cm³ of this solution') + ' Calculate the mass of iron in the tablet.'
        key += f'; n(Fe²⁺) in 250 cm³ = {g3(nred * 10)} mol, mass = {g3(nred * 10 * 55.8)} g [1]'
        ans += f'; {g3(nred * 10 * 55.8)} g of iron'
    return {'stem': stem, 'answer': ans, 'key': key}


@t6c.add('C1', (1, 2, 3))
def t6c_half(r, D):
    k = r.choice(list(HALF))
    right = half_str(k)
    L, R, n, _, _ = HALF[k]
    wrong = [half_str(k).replace(f'{n if n > 1 else ""}e⁻', f'{n + 1}e⁻'), half_str(k, ox=True), half_str(k).replace(f' + {n if n > 1 else ""}e⁻', '') + f' + {n if n > 1 else ""}e⁻', half_str(k).replace(f'{n if n > 1 else ""}e⁻', f'{n + 2}e⁻')]
    return mc(r, f'Which is the correctly balanced half-equation for the reduction of {HALF[k][4]}?', right, wrong, f'Atoms and charges balanced: {right}.')


def t6c_c4(r, D):
    o, rd, oxn, redn, rsp = r.choice(TITR[:3])
    ov, a, b, ne = combine(o, rd)
    c = 0.0200
    titre = r.choice([20.80, 22.40, 24.10])
    nred = c * titre / 1000 * b / a
    intro = P(r, r.choice([f'{{p}} determines the concentration of {redn} by titration with {c:.4f} mol dm⁻³ {oxn}. 25.0 cm³ of the solution requires {titre:.2f} cm³.',
                           f'A pharmaceutical laboratory in {{c}} checks a solution of {redn} by titrating 25.0 cm³ portions with {c:.4f} mol dm⁻³ {oxn}; the mean titre is {titre:.2f} cm³.']))
    parts = [
        lambda r: ('Write the half-equation for the reduction of the oxidising agent.', half_str(o), '[1]'),
        lambda r: (f'Write the half-equation for the oxidation of {rsp}.', half_str(rd, ox=True), '[1]'),
        lambda r: ('Construct the overall ionic equation.', ov, '[2]'),
        lambda r: (f'Calculate the concentration of {rsp}.', f'{g3(nred / 0.025)} mol dm⁻³', f'n(ox) = {g3(c * titre / 1000)}; × {b}/{a}; ÷ 0.0250 [3]'),
        lambda r: ('Describe the colour change at the end-point.', 'Colourless (pale) to first permanent pale pink' if o == 'MnO4' else 'Orange to green (with redox indicator used to see end-point)', '[1]'),
        lambda r: ('Explain why the titration is carried out in excess dilute sulfuric acid rather than hydrochloric acid.', 'H⁺ needed; HCl would be oxidised by the strong oxidant to Cl₂, giving a larger titre.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(3,))


c4reg(t6c, t6c_c4)

CHAPTERS[6] = [t6a, t6b, t6c]


# ===================================================================== Ch7 Equilibria
EQM = [  # display equation, ΔH kJ/mol, gas moles left, right, description
    ('N₂(g) + 3H₂(g) ⇌ 2NH₃(g)', -92, 4, 2, 'the Haber process'), ('2SO₂(g) + O₂(g) ⇌ 2SO₃(g)', -197, 3, 2, 'the Contact process'),
    ('N₂O₄(g) ⇌ 2NO₂(g)', +58, 1, 2, 'a sealed syringe of brown NO₂ and colourless N₂O₄'), ('H₂(g) + I₂(g) ⇌ 2HI(g)', -10, 2, 2, 'a sealed flask of hydrogen, iodine and hydrogen iodide'),
    ('CO(g) + 2H₂(g) ⇌ CH₃OH(g)', -91, 3, 1, 'methanol manufacture'), ('CH₄(g) + H₂O(g) ⇌ CO(g) + 3H₂(g)', +206, 2, 4, 'steam reforming of methane'),
    ('N₂(g) + O₂(g) ⇌ 2NO(g)', +181, 2, 2, 'nitrogen oxide formation in a car engine'), ('CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g)', -41, 2, 2, 'the water–gas shift reaction'),
    ('PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)', +88, 1, 2, 'the dissociation of phosphorus pentachloride'), ('C₂H₄(g) + H₂O(g) ⇌ C₂H₅OH(g)', -46, 2, 1, 'the hydration of ethene'),
    ('2NO(g) + O₂(g) ⇌ 2NO₂(g)', -114, 3, 2, 'nitrogen dioxide formation in the atmosphere'), ('CH₄(g) + 2H₂S(g) ⇌ CS₂(g) + 4H₂(g)', +232, 3, 5, 'a laboratory study'),
]
CHANGES = ['increase the temperature', 'decrease the temperature', 'increase the pressure', 'decrease the pressure', 'add a catalyst']


def lechat(eq, ch):
    _, dh, gl, gr, _ = eq
    if ch == 'add a catalyst':
        return 'no change', 'a catalyst speeds up the forward and reverse reactions equally, so the equilibrium is reached faster but its position is unchanged'
    if 'temperature' in ch:
        up = ch.startswith('increase')
        endo_dir = 'right' if dh > 0 else 'left'
        d = endo_dir if up else ('left' if endo_dir == 'right' else 'right')
        return f'moves to the {d}', f'the forward reaction is {"endothermic" if dh > 0 else "exothermic"}; {"increasing" if up else "decreasing"} temperature favours the {"endothermic" if up else "exothermic"} direction to {"absorb" if up else "release"} heat'
    up = ch.startswith('increase')
    if gl == gr:
        return 'no change', f'there are equal numbers of moles of gas on each side ({gl}), so pressure has no effect on the position'
    fewer = 'right' if gr < gl else 'left'
    d = fewer if up else ('left' if fewer == 'right' else 'right')
    return f'moves to the {d}', f'there are {gl} mol of gas on the left and {gr} on the right; {"increasing" if up else "decreasing"} pressure favours the side with {"fewer" if up else "more"} gas molecules'


t7a = topic("Reversible reactions, dynamic equilibrium and Le Chatelier's principle", 'reversible reactions, dynamic equilibrium', "le chatelier's principle")
t7a.fixed('C1', (1, 2), [
    ('Which statement describes a reaction at dynamic equilibrium?', 'the rates of the forward and reverse reactions are equal', 'Dynamic: both reactions continue at the same rate; concentrations stay constant (closed system).', ['the forward and reverse reactions have stopped', 'the concentrations of reactants and products are equal', 'the reaction has gone to completion']),
    ("What does Le Chatelier's principle state?", 'if a change is made to a system at equilibrium, the position of equilibrium moves to minimise the change', 'The system opposes the imposed change.', ['a catalyst moves the position of equilibrium to the right', 'equilibrium is reached only at high temperature', 'the equilibrium constant changes with concentration']),
    ('What condition is needed for a dynamic equilibrium to be established?', 'a closed system', 'No substances can enter or leave.', ['an open container', 'a catalyst', 'a high temperature']),
    ('Which change alters the value of the equilibrium constant Kc?', 'changing the temperature', 'Only temperature changes K; concentration and pressure changes shift position but not K.', ['adding a catalyst', 'increasing the pressure', 'adding more reactant']),
    ('What is the effect of a catalyst on a reaction at equilibrium?', 'equilibrium is reached faster but the position does not change', 'Catalyst increases forward and reverse rates equally.', ['the yield of product increases', 'the position moves to the left', 'Kc increases']),
    ('State what is meant by a closed system.', 'A system in which no matter can enter or leave (energy may be exchanged).', '[1]'),
])
t7a.fixed('C2', (2, 3, 4), [
    ('Explain why the concentrations of reactants and products remain constant at dynamic equilibrium even though reactions are still occurring.', 'Forward and reverse reactions occur at the same rate, so each substance is formed as fast as it is used up.', 'both reactions continue [1]; equal rates so no net change [1]'),
    ('Explain why adding more reactant moves the position of equilibrium to the right.', 'The system opposes the increase in reactant concentration by using some of it up, so the forward reaction is favoured until equilibrium is re-established.', 'opposes the change [1]; forward reaction uses up reactant [1]'),
    ('Explain the effect of adding hydrochloric acid to the equilibrium Cr₂O₇²⁻(aq) + H₂O(l) ⇌ 2CrO₄²⁻(aq) + 2H⁺(aq).', 'Increased [H⁺] moves the equilibrium to the left to remove H⁺, so the solution becomes orange (more dichromate).', 'moves left [1]; orange colour/opposes increase in H⁺ [1]'),
    ('Explain why the position of equilibrium in H₂(g) + I₂(g) ⇌ 2HI(g) is not affected by pressure.', 'There are 2 moles of gas on each side, so changing pressure does not favour either side.', 'equal moles of gas [1]; neither side favoured [1]'),
])
errs(t7a, [
    ('At equilibrium the concentrations of reactants and products are equal.', 'At equilibrium the concentrations are constant, not necessarily equal; the rates of forward and reverse reactions are equal.'),
    ('Adding a catalyst increases the yield at equilibrium.', 'A catalyst increases the rates of both reactions equally; the position of equilibrium and the yield are unchanged.'),
    ('Increasing the pressure always increases the yield of products.', 'Pressure favours the side with fewer gas molecules; if that is the reactant side, the yield falls, and if moles are equal there is no effect.'),
])
c2mix(t7a, ['{p} studies reversible reactions in sealed containers in {lab}.', 'A chemical engineer in {c} is choosing conditions for a reversible process.'])


@t7a.add('C2', (2, 3, 4), 'explain')
def t7a_shift(r, D):
    eq = r.choice(EQM)
    ch = r.choice(CHANGES)
    eff, why = lechat(eq, ch)
    if D == 2 and r.random() < 0.5:
        return mc(r, f'For the equilibrium {eq[0]}, ΔH = {sgn(eq[1])} kJ mol⁻¹, what happens to the position of equilibrium if you {ch}?', eff, ['moves to the right', 'moves to the left', 'no change', 'the reaction stops'], f'{cap(eff)}: {why}.')
    stem = f'In {eq[4]}, {eq[0]}, ΔH = {sgn(eq[1])} kJ mol⁻¹. Predict and explain the effect on the position of equilibrium if you {ch}.'
    key = f'{eff} [1]; {why} [1]'
    if D >= 4 and ch != 'add a catalyst':
        stem += ' State the effect, if any, on the value of Kc.'
        key += f'; Kc {"changes (" + ("increases" if (eff.endswith("right")) else "decreases") + ")" if "temperature" in ch else "unchanged (only temperature changes K)"} [1]'
    return {'stem': stem, 'answer': f'{cap(eff)}: {why}.', 'key': key}


@t7a.add('C3', (2, 3, 4), 'short')
def t7a_colour(r, D):
    sysm = r.choice([
        ('N₂O₄(g) ⇌ 2NO₂(g), ΔH = +58 kJ mol⁻¹ (N₂O₄ colourless, NO₂ brown)', [('the syringe is placed in hot water', 'darker brown: endothermic forward reaction favoured, more NO₂'),
                                                                               ('the syringe plunger is pushed in (pressure increased) and held', 'after an initial darkening, the colour becomes paler: equilibrium moves left to fewer gas molecules'),
                                                                               ('the syringe is cooled in ice', 'paler: exothermic reverse reaction favoured, more N₂O₄')]),
        ('[Co(H₂O)₆]²⁺(aq) (pink) + 4Cl⁻(aq) ⇌ [CoCl₄]²⁻(aq) (blue) + 6H₂O(l), ΔH positive', [('concentrated hydrochloric acid is added', 'turns blue: increased [Cl⁻] moves equilibrium right'),
                                                                                         ('water is added', 'turns pink: equilibrium moves left'), ('the solution is heated', 'turns blue: endothermic forward reaction favoured'),
                                                                                         ('the solution is cooled in ice', 'turns pink: exothermic reverse direction favoured')]),
        ('Cr₂O₇²⁻(aq) (orange) + H₂O(l) ⇌ 2CrO₄²⁻(aq) (yellow) + 2H⁺(aq)', [('dilute sulfuric acid is added', 'turns orange: increased [H⁺] moves equilibrium left'),
                                                                             ('aqueous sodium hydroxide is added', 'turns yellow: OH⁻ removes H⁺, equilibrium moves right')]),
        ('Fe³⁺(aq) (yellow) + SCN⁻(aq) ⇌ [FeSCN]²⁺(aq) (blood red)', [('more potassium thiocyanate solution is added', 'deeper red: equilibrium moves right'),
                                                                      ('sodium fluoride is added, which removes Fe³⁺ ions', 'paler red/yellow: equilibrium moves left to replace Fe³⁺')]),
    ])
    what, res = r.choice(sysm[1])
    return {'stem': f'{person(r)} sets up the equilibrium {sysm[0]}. Describe and explain the colour change seen when {what}.', 'answer': cap(res) + '.',
            'key': 'colour change [1]; direction of shift [1]' + ('; reason using Le Chatelier’s principle [1]' if D >= 3 else '')}


def t7a_c4(r, D):
    eq = r.choice(EQM)
    intro = P(r, r.choice([f'The equilibrium {eq[0]}, ΔH = {sgn(eq[1])} kJ mol⁻¹, is used in {eq[4]}.', f'{{p}} investigates the equilibrium {eq[0]} (ΔH = {sgn(eq[1])} kJ mol⁻¹) in {{lab}}.']))
    parts = [
        lambda r: ('State two features of a dynamic equilibrium.', 'Rates of forward and reverse reactions equal; concentrations constant; closed system.', '[2]'),
        lambda r: ("State Le Chatelier's principle.", 'If a change is made to a system at equilibrium, the position moves to minimise/oppose the change.', '[1]'),
        lambda r: ('Predict and explain the effect of increasing the temperature on the equilibrium yield.', f'{lechat(eq, "increase the temperature")[0]}: {lechat(eq, "increase the temperature")[1]}', '[2]'),
        lambda r: ('Predict and explain the effect of increasing the pressure on the equilibrium yield.', f'{lechat(eq, "increase the pressure")[0]}: {lechat(eq, "increase the pressure")[1]}', '[2]'),
        lambda r: ('State and explain the effect of a catalyst.', 'No change in position; equilibrium reached faster as both rates increase equally.', '[2]'),
        lambda r: ('State which change, if any, would alter the value of Kc.', 'Only a change in temperature.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t7a, t7a_c4)

# ---------------------------------------------------------- 7.2 Kc and Kp
KEXPR = [  # equation, Kc expression, wrong expressions, units of Kc, Kp expression
    ('N₂(g) + 3H₂(g) ⇌ 2NH₃(g)', '[NH₃]² / [N₂][H₂]³', ['[NH₃] / [N₂][H₂]', '[N₂][H₂]³ / [NH₃]²', '2[NH₃] / [N₂] 3[H₂]'], 'mol⁻² dm⁶', 'p(NH₃)² / p(N₂) p(H₂)³', 'Pa⁻² (or atm⁻²)'),
    ('2SO₂(g) + O₂(g) ⇌ 2SO₃(g)', '[SO₃]² / [SO₂]²[O₂]', ['[SO₃] / [SO₂][O₂]', '[SO₂]²[O₂] / [SO₃]²', '[SO₃]² / [SO₂]² + [O₂]'], 'mol⁻¹ dm³', 'p(SO₃)² / p(SO₂)² p(O₂)', 'Pa⁻¹ (or atm⁻¹)'),
    ('N₂O₄(g) ⇌ 2NO₂(g)', '[NO₂]² / [N₂O₄]', ['[NO₂] / [N₂O₄]', '[N₂O₄] / [NO₂]²', '2[NO₂] / [N₂O₄]'], 'mol dm⁻³', 'p(NO₂)² / p(N₂O₄)', 'Pa (or atm)'),
    ('H₂(g) + I₂(g) ⇌ 2HI(g)', '[HI]² / [H₂][I₂]', ['[HI] / [H₂][I₂]', '[H₂][I₂] / [HI]²', '2[HI] / [H₂][I₂]'], 'no units', 'p(HI)² / p(H₂) p(I₂)', 'no units'),
    ('PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)', '[PCl₃][Cl₂] / [PCl₅]', ['[PCl₅] / [PCl₃][Cl₂]', '[PCl₃] + [Cl₂] / [PCl₅]', '[PCl₃][Cl₂]'], 'mol dm⁻³', 'p(PCl₃) p(Cl₂) / p(PCl₅)', 'Pa (or atm)'),
    ('CH₃COOH(l) + C₂H₅OH(l) ⇌ CH₃COOC₂H₅(l) + H₂O(l)', '[CH₃COOC₂H₅][H₂O] / [CH₃COOH][C₂H₅OH]', ['[CH₃COOH][C₂H₅OH] / [CH₃COOC₂H₅][H₂O]', '[CH₃COOC₂H₅] / [CH₃COOH][C₂H₅OH]', '[CH₃COOC₂H₅][H₂O]'], 'no units', None, None),
    ('CO(g) + 2H₂(g) ⇌ CH₃OH(g)', '[CH₃OH] / [CO][H₂]²', ['[CH₃OH] / [CO][H₂]', '[CO][H₂]² / [CH₃OH]', '[CH₃OH] / [CO] 2[H₂]'], 'mol⁻² dm⁶', 'p(CH₃OH) / p(CO) p(H₂)²', 'Pa⁻² (or atm⁻²)'),
    ('2NO₂(g) ⇌ 2NO(g) + O₂(g)', '[NO]²[O₂] / [NO₂]²', ['[NO][O₂] / [NO₂]', '[NO₂]² / [NO]²[O₂]', '[NO]² + [O₂] / [NO₂]²'], 'mol dm⁻³', 'p(NO)² p(O₂) / p(NO₂)²', 'Pa (or atm)'),
]

t7b = topic('Equilibrium constants Kc and Kp: expressions and calculations', 'equilibrium constants kc and kp', 'expressions and calculations')
t7b.fixed('C1', (1, 2), [
    ('What is the partial pressure of a gas in a mixture?', 'mole fraction of the gas × total pressure', 'p(A) = x(A) × P(total); the sum of partial pressures = total pressure.', ['total pressure ÷ number of gases', 'moles of gas × total pressure', 'the pressure the gas exerts at r.t.p.']),
    ('What does a very large value of Kc indicate?', 'the position of equilibrium lies far to the right', 'Large K: mostly products at equilibrium.', ['the reaction is very fast', 'the position lies far to the left', 'the reaction is endothermic']),
    ('For an exothermic reaction, what happens to Kc when temperature is increased?', 'it decreases', 'Equilibrium shifts left (endothermic direction) so K decreases.', ['it increases', 'it stays the same', 'it becomes zero']),
    ('Which substances are omitted from a Kc expression for a heterogeneous equilibrium?', 'pure solids (and pure liquids)', 'Their concentrations are constant.', ['gases', 'aqueous ions', 'products']),
    ('What are the units of Kc for H₂(g) + I₂(g) ⇌ 2HI(g)?', 'no units', 'mol² dm⁻⁶ / mol² dm⁻⁶: units cancel.', ['mol dm⁻³', 'mol⁻¹ dm³', 'mol² dm⁻⁶']),
    ('Write the expression for the mole fraction of gas A in a mixture.', 'x(A) = moles of A / total moles of gas', '[1]'),
])
t7b.fixed('C2', (2, 3, 4), [
    ('Explain why increasing the pressure on N₂ + 3H₂ ⇌ 2NH₃ increases the yield of NH₃ but does not change Kp.', 'Kp depends only on temperature; when pressure increases the ratio of partial pressures temporarily differs from Kp and the equilibrium shifts right until the ratio again equals Kp.', 'Kp depends only on temperature [1]; position shifts to restore ratio [1]'),
    ('Explain why the volume of the container is not needed to calculate Kc for H₂ + I₂ ⇌ 2HI.', 'The total moles on each side are equal, so the volume terms cancel in the Kc expression.', 'equal powers top and bottom [1]; V cancels [1]'),
    ('Explain why water is included in the Kc expression for esterification but not for reactions in dilute aqueous solution.', 'In esterification water is a product present in small amounts and its concentration changes; in dilute aqueous solution water is in huge excess and its concentration is effectively constant.', 'water concentration changes in esterification [1]; constant in dilute solution [1]'),
])
errs(t7b, [
    ('For N₂ + 3H₂ ⇌ 2NH₃, Kc = [NH₃]/[N₂][H₂].', 'Concentrations are raised to the power of their coefficients: Kc = [NH₃]²/[N₂][H₂]³.'),
    ('Adding more nitrogen to the Haber equilibrium increases Kc.', 'Kc is unchanged; only temperature alters K. The position shifts right.'),
    ('A partial pressure is the number of moles of a gas multiplied by the total pressure.', 'Partial pressure = mole fraction × total pressure.'),
])
c2mix(t7b, ['{p} carries out equilibrium calculations for an AS test.', 'A research chemist in {c} measures equilibrium compositions of gas mixtures.'])


@t7b.add('C1', (1, 2, 3))
def t7b_expr(r, D):
    eq, ex, wr, u, kp, ku = r.choice(KEXPR)
    if r.random() < 0.6 or not kp:
        return mc(r, f'What is the expression for Kc for the equilibrium {eq}?', f'Kc = {ex}', [f'Kc = {w}' for w in wr], f'Products over reactants, each raised to its coefficient: {ex}.')
    return mc(r, f'What are the units of Kp for {eq}, with partial pressures in Pa?', ku.split(' (')[0], ['Pa', 'Pa⁻¹', 'Pa⁻²', 'Pa²', 'no units'], f'Kp = {kp}: units {ku}.')


@t7b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t7b_kc(r, D):
    kind = r.choice(['HI', 'ester', 'PCl5', 'conc'])
    if D == 1:
        eq, ex, wr, u, kp, ku = r.choice(KEXPR)
        return mc(r, f'What are the units of Kc for {eq}?', u, ['mol dm⁻³', 'mol⁻¹ dm³', 'mol⁻² dm⁶', 'mol² dm⁻⁶', 'no units'], f'Kc = {ex}: units {u}.')
    if kind == 'HI':
        a = r.choice([1.00, 2.00, 1.50, 0.800])
        b = r.choice([1.00, 0.600, 1.20, 0.500])
        x = round(min(a, b) * r.choice([0.6, 0.7, 0.75, 0.8, 0.85]), 3)
        H, I, HI = a - x, b - x, 2 * x
        Kc = HI ** 2 / (H * I)
        return {'stem': f'{a:.2f} mol of hydrogen and {b:.2f} mol of iodine are heated in a sealed container until equilibrium is reached: H₂(g) + I₂(g) ⇌ 2HI(g). At equilibrium {HI:.3f} mol of HI is present. Calculate Kc.',
                'answer': f'Kc = {g3(Kc)} (no units)', 'key': f'n(H₂) = {H:.3f}, n(I₂) = {I:.3f} mol [1]; Kc = {HI:.3f}²/({H:.3f} × {I:.3f}) [1]; = {g3(Kc)}, no units (V cancels) [1]'}
    if kind == 'ester':
        a = r.choice([1.00, 2.00, 0.500, 1.50])
        b = r.choice([1.00, 2.00, 0.500, 1.20])
        x = round(min(a, b) * r.choice([0.5, 0.6, 0.67, 0.7, 0.75]), 3)
        Kc = x * x / ((a - x) * (b - x))
        return {'stem': f'{person(r)} mixes {a:.2f} mol of ethanoic acid with {b:.2f} mol of ethanol and a few drops of concentrated sulfuric acid. At equilibrium the mixture contains {x:.3f} mol of ethyl ethanoate. Calculate Kc for CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O.',
                'answer': f'Kc = {g3(Kc)}', 'key': f'equilibrium: acid {a - x:.3f}, ethanol {b - x:.3f}, ester {x:.3f}, water {x:.3f} mol [1]; Kc expression [1]; Kc = {g3(Kc)}, no units [1]'}
    if kind == 'PCl5':
        n0 = r.choice([0.200, 0.300, 0.400, 0.500])
        V = r.choice([1.00, 2.00, 5.00])
        alpha = r.choice([0.25, 0.3, 0.4, 0.5, 0.6])
        x = n0 * alpha
        Kc = (x / V) ** 2 / ((n0 - x) / V)
        return {'stem': f'{n0:.3f} mol of PCl₅ is heated in a sealed {V:.2f} dm³ flask. At equilibrium {alpha * 100:.0f}% has dissociated: PCl₅(g) ⇌ PCl₃(g) + Cl₂(g). Calculate Kc, giving its units.',
                'answer': f'{g3(Kc)} mol dm⁻³', 'key': f'n(PCl₃) = n(Cl₂) = {g3(x)} mol, n(PCl₅) = {g3(n0 - x)} mol [1]; concentrations ÷ {V:.2f} dm³ [1]; Kc = {g3(Kc)} [1]; mol dm⁻³ [1]'}
    cN, cH = r.choice([0.50, 1.00, 1.20, 0.80]), r.choice([1.50, 2.00, 1.80, 3.00])
    cA = r.choice([0.20, 0.30, 0.40, 0.25])
    Kc = cA ** 2 / (cN * cH ** 3)
    return {'stem': f'At equilibrium at a certain temperature, [N₂] = {cN:.2f} mol dm⁻³, [H₂] = {cH:.2f} mol dm⁻³ and [NH₃] = {cA:.2f} mol dm⁻³ for N₂(g) + 3H₂(g) ⇌ 2NH₃(g). Calculate Kc and give its units.',
            'answer': f'{g3(Kc)} mol⁻² dm⁶', 'key': f'Kc = [NH₃]²/[N₂][H₂]³ [1]; = {cA:.2f}²/({cN:.2f} × {cH:.2f}³) = {g3(Kc)} [1]; mol⁻² dm⁶ [1]'}


@t7b.add('C3', (3, 4, 5), 'numerical')
def t7b_kp(r, D):
    if r.random() < 0.5:
        n0 = 1.00
        a = r.choice([0.20, 0.25, 0.30, 0.40, 0.50])
        P_ = r.choice([100, 150, 200, 300])
        nN, nNO2 = 1 - a, 2 * a
        tot = 1 + a
        pN, pNO = nN / tot * P_, nNO2 / tot * P_
        Kp = pNO ** 2 / pN
        return {'stem': f'Dinitrogen tetroxide dissociates: N₂O₄(g) ⇌ 2NO₂(g). At a certain temperature and a total pressure of {P_} kPa, {a * 100:.0f}% of the N₂O₄ has dissociated. Calculate the partial pressures of both gases and Kp, with units.',
                'answer': f'p(N₂O₄) = {g3(pN)} kPa, p(NO₂) = {g3(pNO)} kPa, Kp = {g3(Kp)} kPa', 'key': f'moles from 1 mol: N₂O₄ {nN:.2f}, NO₂ {nNO2:.2f}, total {tot:.2f} [1]; mole fractions [1]; partial pressures {g3(pN)} and {g3(pNO)} kPa [1]; Kp = {g3(pNO)}²/{g3(pN)} = {g3(Kp)} kPa [1]'}
    nS, nO, nT = r.choice([(0.40, 0.20, 1.40), (0.20, 0.10, 1.70), (0.30, 0.15, 1.55), (0.10, 0.05, 1.85)])
    P_ = r.choice([100, 200, 150])
    tot = nS + nO + nT
    pS, pO, pT = nS / tot * P_, nO / tot * P_, nT / tot * P_
    Kp = pT ** 2 / (pS ** 2 * pO)
    return {'stem': f'An equilibrium mixture for 2SO₂(g) + O₂(g) ⇌ 2SO₃(g) contains {nS:.2f} mol SO₂, {nO:.2f} mol O₂ and {nT:.2f} mol SO₃ at a total pressure of {P_} kPa. Calculate Kp and state its units.',
            'answer': f'{g3(Kp)} kPa⁻¹', 'key': f'total moles {tot:.2f}; mole fractions [1]; p(SO₂) {g3(pS)}, p(O₂) {g3(pO)}, p(SO₃) {g3(pT)} kPa [1]; Kp = p(SO₃)²/(p(SO₂)² p(O₂)) = {g3(Kp)} [1]; kPa⁻¹ [1]'}


def t7b_c4(r, D):
    a = r.choice([1.00, 2.00])
    b = r.choice([1.00, 1.50])
    x = round(min(a, b) * 0.667, 3)
    Kc = x * x / ((a - x) * (b - x))
    intro = P(r, r.choice([f'{{p}} mixes {a:.2f} mol of ethanoic acid and {b:.2f} mol of ethanol with a little concentrated H₂SO₄ and leaves the mixture to reach equilibrium at room temperature. {x:.3f} mol of ethyl ethanoate is formed.',
                           f'In {{lab}} in {{c}}, an ester equilibrium is set up from {a:.2f} mol CH₃COOH and {b:.2f} mol C₂H₅OH; at equilibrium {x:.3f} mol of CH₃COOC₂H₅ is present.']))
    parts = [
        lambda r: ('Write an expression for Kc.', '[CH₃COOC₂H₅][H₂O] / [CH₃COOH][C₂H₅OH]', '[1]'),
        lambda r: ('Calculate the amounts of all four substances at equilibrium.', f'acid {a - x:.3f}, ethanol {b - x:.3f}, ester {x:.3f}, water {x:.3f} mol', '[2]'),
        lambda r: ('Calculate Kc and explain why it has no units.', f'{g3(Kc)}; volume and concentration units cancel (equal moles each side)', '[2]'),
        lambda r: ('State the role of the concentrated sulfuric acid and its effect on the equilibrium position.', 'Catalyst: equilibrium reached faster, position unchanged.', '[2]'),
        lambda r: ('Describe how the amount of ethanoic acid at equilibrium could be found.', 'Titrate a sample with standard NaOH (subtracting the H₂SO₄ catalyst contribution), quickly / after diluting in ice-cold water to stop reaction.', '[2]'),
        lambda r: ('Suggest how the yield of ester could be increased.', 'Use excess ethanol or remove the ester/water as it forms (distil).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2))


c4reg(t7b, t7b_c4)

# ---------------------------------------------------------- 7.3 Haber and Contact processes
t7c = topic('Haber and Contact processes: conditions and compromises', 'haber and contact processes', 'conditions and compromises')
t7c.fixed('C1', (1, 2), [
    ('What catalyst is used in the Haber process?', 'iron', 'Finely divided iron (with promoters).', ['vanadium(V) oxide', 'platinum', 'nickel']),
    ('What catalyst is used in the Contact process?', 'vanadium(V) oxide, V₂O₅', 'V₂O₅ catalyses 2SO₂ + O₂ ⇌ 2SO₃.', ['iron', 'aluminium oxide', 'concentrated sulfuric acid']),
    ('What typical pressure is used in the Haber process?', 'about 20 000 kPa (200 atm)', 'Compromise between yield and cost/safety.', ['about 100 kPa', 'about 2 kPa', 'about 1 000 000 kPa']),
    ('What typical temperature is used in the Contact process?', 'about 450 °C', '400–450 °C: compromise between rate and yield.', ['about 25 °C', 'about 1000 °C', 'about 200 °C']),
    ('Why is a pressure of only 1–2 atm used in the Contact process?', 'the equilibrium yield is already very high at low pressure', 'Over 99% conversion; extra pressure would add cost for little gain.', ['high pressure would decompose SO₃', 'the catalyst works only at low pressure', 'SO₂ would liquefy']),
    ('State how ammonia is removed from the equilibrium mixture in the Haber process.', 'By cooling: ammonia liquefies and is removed; unreacted N₂ and H₂ are recycled.', '[1]'),
])
t7c.fixed('C2', (2, 3, 4), [
    ('Explain why a temperature of about 450 °C is used in the Haber process even though a lower temperature gives a higher equilibrium yield.', 'The forward reaction is exothermic so low temperature favours ammonia, but the rate would be too slow; 450 °C is a compromise giving acceptable rate and yield.', 'low T higher yield (exothermic) [1]; rate too slow at low T, compromise [1]'),
    ('Explain why a very high pressure is not used in the Haber process.', 'High pressure increases yield and rate but is expensive (energy to compress gas, strong pipes) and dangerous.', 'yield would increase [1]; cost/safety [1]'),
    ('Explain why the unreacted gases are recycled in the Haber process.', 'Only about 15% conversion per pass; recycling the N₂ and H₂ means almost all is eventually converted, reducing waste and cost.', 'low conversion per pass [1]; overall conversion high, saves cost [1]'),
    ('Explain why SO₃ is absorbed in concentrated sulfuric acid rather than water in the Contact process.', 'SO₃ reacts violently with water, forming a mist of acid; dissolving in concentrated H₂SO₄ gives oleum, H₂S₂O₇, which is diluted carefully.', 'violent reaction/mist with water [1]; forms oleum then diluted [1]'),
])
errs(t7c, [
    ('The iron catalyst in the Haber process increases the percentage of ammonia at equilibrium.', 'A catalyst increases the rate only; the equilibrium yield is unchanged.'),
    ('The Contact process uses 200 atm because there are fewer moles of gas on the right.', 'Only 1–2 atm is needed because conversion is already over 99%.'),
    ('In the Haber process the temperature is raised to 450 °C to increase the yield.', 'Raising temperature decreases the yield (exothermic); 450 °C is used for an acceptable rate.'),
])
c2mix(t7c, ['An ammonia plant in {c} must choose operating conditions.', '{p} researches how sulfuric acid is made industrially.'])

HAB = {(350, 200): 47, (400, 200): 36, (450, 200): 28, (500, 200): 18, (450, 100): 16, (450, 300): 36, (400, 100): 25, (400, 300): 47, (350, 100): 30, (500, 300): 26}


@t7c.add('C3', (2, 3, 4, 5), 'numerical')
def t7c_calc(r, D):
    if r.random() < 0.5:
        t_ = r.choice([5.0, 10.0, 20.0, 50.0, 100.0])
        pc = r.choice([15, 18, 20, 25, 28])
        nN = t_ * 1e6 / 28.0
        mNH3 = nN * 2 * 17.0 * pc / 100 / 1e6
        return {'stem': f'In one pass through the reactor of an ammonia plant in {city(r)}, {pc}% of the nitrogen is converted into ammonia. Calculate the mass of ammonia, in tonnes, made from {t_:g} tonnes of nitrogen in one pass. (N₂ + 3H₂ ⇌ 2NH₃)',
                'answer': f'{g3(mNH3)} tonnes', 'key': f'n(N₂) = {t_:g} × 10⁶/28.0 = {g3(nN)} mol [1]; n(NH₃) at 100% = {g3(2 * nN)} mol [1]; × {pc}% × 17.0 g mol⁻¹ = {g3(mNH3)} tonnes [1]'}
    t_ = r.choice([1.0, 5.0, 10.0, 32.0, 64.0])
    pc = r.choice([96, 98, 99, 99.5])
    m = t_ * 1e6 / 32.1 * 98.1 / 1e6 * pc / 100
    return {'stem': f'A sulfuric acid plant burns {t_:g} tonnes of sulfur. Overall conversion of sulfur into H₂SO₄ is {pc}%. Calculate the mass of sulfuric acid produced. (S → SO₂ → SO₃ → H₂SO₄)',
            'answer': f'{g3(m)} tonnes', 'key': f'1 mol S → 1 mol H₂SO₄ [1]; mass at 100% = {t_:g} × 98.1/32.1 = {g3(m / pc * 100)} t [1]; × {pc}% = {g3(m)} t [1]'}


@t7c.add('C2', (2, 3, 4), 'explain')
def t7c_data(r, D):
    (t1, p1), (t2, p2) = r.sample(list(HAB), 2)
    y1, y2 = HAB[(t1, p1)], HAB[(t2, p2)]
    if t1 == t2 and p1 == p2:
        return None
    if t1 == t2:
        var = f'pressure ({p1} atm vs {p2} atm) at {t1} °C'
        why = 'higher pressure favours the side with fewer moles of gas (2 mol NH₃ vs 4 mol reactants)'
    elif p1 == p2:
        var = f'temperature ({t1} °C vs {t2} °C) at {p1} atm'
        why = 'the forward reaction is exothermic, so lower temperature favours ammonia'
    else:
        return None
    return {'stem': f'Data for the Haber process show {y1}% ammonia at {t1} °C and {p1} atm, and {y2}% at {t2} °C and {p2} atm. Explain how the {var.split(" (")[0]} affects the equilibrium yield, referring to these data.',
            'answer': f'Changing {var} changes yield from {y1}% to {y2}%: {why}.', 'key': 'correct trend from data [1]; explanation using Le Chatelier [1]' + ('; refers to compromise with rate or cost [1]' if D >= 4 else '')}


def t7c_c4(r, D):
    proc = r.choice(['Haber', 'Contact'])
    intro = P(r, r.choice([f'A chemical company in {{c}} operates the {proc} process.', f'{{p}} is preparing a report on the {proc} process for a class in {{c}}.']))
    if proc == 'Haber':
        parts = [
            lambda r: ('Write the equation for the reaction, with state symbols, and give the sign of ΔH.', 'N₂(g) + 3H₂(g) ⇌ 2NH₃(g); ΔH negative (−92 kJ mol⁻¹)', '[2]'),
            lambda r: ('State the typical conditions used.', 'About 450 °C, 20 000 kPa (200 atm), iron catalyst.', '[2]'),
            lambda r: ('Explain why the temperature used is a compromise.', 'Lower T gives higher yield (exothermic) but slower rate; 450 °C balances these.', '[2]'),
            lambda r: ('Explain the choice of pressure.', 'High pressure favours fewer gas moles (product) and increases rate; very high pressure too costly/dangerous.', '[2]'),
            lambda r: ('Write the expression for Kp.', 'Kp = p(NH₃)² / p(N₂) p(H₂)³', '[1]'),
            lambda r: ('Describe how ammonia is separated and what happens to unreacted gases.', 'Cooled to liquefy NH₃; N₂ and H₂ recycled.', '[2]'),
        ]
    else:
        parts = [
            lambda r: ('Write the equation for the equilibrium step, with state symbols.', '2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH = −197 kJ mol⁻¹', '[2]'),
            lambda r: ('State the conditions used for this step.', 'About 450 °C, 100–200 kPa, V₂O₅ catalyst.', '[2]'),
            lambda r: ('Explain why a high pressure is not used.', 'Conversion is already >99% at low pressure; high pressure is costly.', '[2]'),
            lambda r: ('Explain why the temperature is a compromise.', 'Exothermic: low T higher yield but slower rate.', '[2]'),
            lambda r: ('Write the expression for Kp.', 'Kp = p(SO₃)² / p(SO₂)² p(O₂)', '[1]'),
            lambda r: ('Describe how SO₃ is converted into sulfuric acid.', 'Absorbed in concentrated H₂SO₄ to give oleum, H₂S₂O₇, then diluted with water.', '[2]'),
        ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t7c, t7c_c4)

# ---------------------------------------------------------- 7.4 Brønsted–Lowry acids and bases
BLR = [  # equation, acid, base, conjugate acid, conjugate base
    ('HCl + H₂O → H₃O⁺ + Cl⁻', 'HCl', 'H₂O', 'H₃O⁺', 'Cl⁻'), ('NH₃ + H₂O ⇌ NH₄⁺ + OH⁻', 'H₂O', 'NH₃', 'NH₄⁺', 'OH⁻'), ('CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺', 'CH₃COOH', 'H₂O', 'H₃O⁺', 'CH₃COO⁻'),
    ('HNO₃ + H₂SO₄ ⇌ H₂NO₃⁺ + HSO₄⁻', 'H₂SO₄', 'HNO₃', 'H₂NO₃⁺', 'HSO₄⁻'), ('HCO₃⁻ + H₂O ⇌ CO₃²⁻ + H₃O⁺', 'HCO₃⁻', 'H₂O', 'H₃O⁺', 'CO₃²⁻'), ('NH₄⁺ + OH⁻ ⇌ NH₃ + H₂O', 'NH₄⁺', 'OH⁻', 'H₂O', 'NH₃'),
    ('HCl + NH₃ → NH₄⁺ + Cl⁻', 'HCl', 'NH₃', 'NH₄⁺', 'Cl⁻'), ('H₂O + H₂O ⇌ H₃O⁺ + OH⁻', 'H₂O', 'H₂O', 'H₃O⁺', 'OH⁻'), ('HSO₄⁻ + H₂O ⇌ SO₄²⁻ + H₃O⁺', 'HSO₄⁻', 'H₂O', 'H₃O⁺', 'SO₄²⁻'),
    ('CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + OH⁻', 'H₂O', 'CH₃NH₂', 'CH₃NH₃⁺', 'OH⁻'), ('HF + H₂O ⇌ F⁻ + H₃O⁺', 'HF', 'H₂O', 'H₃O⁺', 'F⁻'), ('CO₃²⁻ + H₂O ⇌ HCO₃⁻ + OH⁻', 'H₂O', 'CO₃²⁻', 'HCO₃⁻', 'OH⁻'),
    ('HCOOH + H₂O ⇌ HCOO⁻ + H₃O⁺', 'HCOOH', 'H₂O', 'H₃O⁺', 'HCOO⁻'), ('H₂SO₄ + H₂O → HSO₄⁻ + H₃O⁺', 'H₂SO₄', 'H₂O', 'H₃O⁺', 'HSO₄⁻'),
]
ACIDS = [('hydrochloric acid', 'strong'), ('nitric acid', 'strong'), ('sulfuric acid', 'strong'), ('ethanoic acid', 'weak'), ('methanoic acid', 'weak'), ('carbonic acid', 'weak'),
         ('hydrofluoric acid', 'weak'), ('propanoic acid', 'weak'), ('hydrobromic acid', 'strong'), ('citric acid', 'weak')]

WEQ = {'ethanoic acid': 'CH₃COOH(aq) ⇌ CH₃COO⁻(aq) + H⁺(aq)', 'methanoic acid': 'HCOOH(aq) ⇌ HCOO⁻(aq) + H⁺(aq)', 'carbonic acid': 'H₂CO₃(aq) ⇌ HCO₃⁻(aq) + H⁺(aq)',
       'hydrofluoric acid': 'HF(aq) ⇌ H⁺(aq) + F⁻(aq)', 'propanoic acid': 'CH₃CH₂COOH(aq) ⇌ CH₃CH₂COO⁻(aq) + H⁺(aq)'}

t7d = topic('Brønsted–Lowry acids and bases; strong and weak acids', 'brønsted–lowry acids and bases', 'strong and weak acids')
t7d.fixed('C1', (1, 2), [
    ('What is a Brønsted–Lowry acid?', 'a proton (H⁺) donor', 'Acid donates H⁺; base accepts H⁺.', ['a proton acceptor', 'an electron-pair donor', 'a substance that produces OH⁻ ions']),
    ('What is the conjugate base of H₂SO₄?', 'HSO₄⁻', 'Remove one H⁺: H₂SO₄ → HSO₄⁻.', ['SO₄²⁻', 'H₃SO₄⁺', 'H₂O']),
    ('What is meant by a strong acid?', 'an acid that is fully ionised (dissociated) in aqueous solution', 'e.g. HCl → H⁺ + Cl⁻ completely; weak acids partially ionise.', ['a concentrated acid', 'an acid with a high pH', 'an acid that reacts slowly']),
    ('Which is a weak base?', 'ammonia', 'NH₃ + H₂O ⇌ NH₄⁺ + OH⁻ (partial).', ['sodium hydroxide', 'potassium hydroxide', 'barium hydroxide']),
    ('Which indicator is suitable for titrating ethanoic acid with sodium hydroxide?', 'phenolphthalein', 'Weak acid–strong base: equivalence point pH about 8–9, in phenolphthalein’s range.', ['methyl orange', 'bromophenol blue', 'no indicator works']),
    ('Define a Brønsted–Lowry base.', 'A proton (H⁺) acceptor.', '[1]'),
])
t7d.fixed('C2', (2, 3, 4), [
    ('Explain the difference between a strong acid and a concentrated acid.', 'Strong refers to complete ionisation in water; concentrated refers to a large amount of acid per dm³ of solution. A weak acid can be concentrated.', 'strong = fully ionised [1]; concentrated = amount per volume [1]'),
    ('Describe an experiment to show that ethanoic acid is weaker than hydrochloric acid of the same concentration.', 'Measure pH (ethanoic higher), compare electrical conductivity (lower), or rate of reaction with magnesium (slower bubbling) for equal concentrations.', 'valid method [1]; correct result for weak acid [1]'),
    ('Explain why water can act as both an acid and a base.', 'It can donate a proton (forming OH⁻) or accept a proton (forming H₃O⁺); it is amphoteric (amphiprotic).', 'donates H⁺ [1]; accepts H⁺ [1]'),
    ('Explain why methyl orange is not a suitable indicator for the titration of ethanoic acid with sodium hydroxide.', 'The pH at the equivalence point is above 7 (about 8–9) and the vertical section is above methyl orange’s range (3–5), so it changes colour too early.', 'equivalence above 7 [1]; methyl orange range too low [1]'),
])
errs(t7d, [
    ('A weak acid is a dilute acid.', 'Weak means partially ionised; dilute means low concentration. A weak acid can be concentrated.'),
    ('In NH₃ + H₂O ⇌ NH₄⁺ + OH⁻, ammonia is the acid because it gains a hydrogen.', 'Ammonia accepts a proton, so it is the base; water donates the proton and is the acid.'),
    ('The conjugate base of HCl is H₂Cl⁺.', 'The conjugate base is formed by losing H⁺: Cl⁻.'),
])
c2mix(t7d, ['{p} compares solutions of strong and weak acids in {lab}.', 'A student in {c} is identifying conjugate acid–base pairs.'])


@t7d.add('C3', (1, 2, 3, 4), 'short')
def t7d_pairs(r, D):
    eq, a, b, ca, cb = r.choice(BLR)
    if D == 1:
        return mc(r, f'In the reaction {eq}, which species acts as a Brønsted–Lowry acid (left to right)?', a, list({a, b, ca, cb}) + ['none of them'], f'{a} donates a proton to {b}.')
    stem = f'For the reaction {eq}, identify the Brønsted–Lowry acid and base on the left-hand side and give the two conjugate acid–base pairs.'
    return {'stem': stem, 'answer': f'acid {a}, base {b}; pairs: {a}/{cb} and {ca}/{b}', 'key': f'acid {a} and base {b} [1]; pair {a}/{cb} [1]; pair {ca}/{b} [1]' if D >= 3 else f'acid {a}, base {b} [1]; one conjugate pair correct [1]'}


@t7d.add('C1', (1, 2, 3))
def t7d_sw(r, D):
    a, k = r.choice(ACIDS)
    return mc(r, f'Which statement about {a} is correct?', f'it is a {k} acid, {"fully" if k == "strong" else "only partially"} ionised in water', ['it is a strong acid, fully ionised in water', 'it is a weak acid, only partially ionised in water', 'it is a base', 'it does not ionise in water at all'],
              f'{a}: {k} acid.')


@t7d.add('C2', (2, 3, 4), 'explain')
def t7d_cmp(r, D):
    s, w = r.choice([x for x in ACIDS if x[1] == 'strong']), r.choice([x for x in ACIDS if x[1] == 'weak'])
    c = r.choice(['0.100', '0.0500', '1.00', '0.200'])
    prop = r.choice([('pH', 'lower pH for the strong acid'), ('electrical conductivity', 'higher conductivity for the strong acid'), ('rate of reaction with magnesium ribbon', 'faster effervescence with the strong acid'),
                     ('volume of 0.100 mol dm⁻³ NaOH needed to neutralise 25.0 cm³ (both monoprotic)', 'the same volume for both (if both monoprotic): the weak acid continues to ionise as H⁺ is removed')])
    if 'sulfuric' in s[0] and 'volume' in prop[0]:
        return None
    return {'stem': f'Solutions of {s[0]} and {w[0]}, both {c} mol dm⁻³, are compared. Predict and explain the difference in their {prop[0]}.' + (f' Write an equation for the partial ionisation of {w[0]}.' if D >= 4 else ''),
            'answer': cap(prop[1]) + f'. {s[0].capitalize()} is fully ionised; {w[0]} is only partially ionised, so [H⁺] is lower.' + (f' {WEQ.get(w[0], "HA(aq) ⇌ H⁺(aq) + A⁻(aq)")}' if D >= 4 else ''),
            'key': 'correct prediction [1]; full vs partial ionisation / [H⁺] [1]' + ('; equation for weak acid equilibrium [1]' if D >= 4 else '')}


def t7d_c4(r, D):
    w = r.choice([x for x in ACIDS if x[1] == 'weak' and x[0] not in ('carbonic acid', 'citric acid')])
    form = {'ethanoic acid': 'CH₃COOH ⇌ CH₃COO⁻ + H⁺', 'methanoic acid': 'HCOOH ⇌ HCOO⁻ + H⁺', 'hydrofluoric acid': 'HF ⇌ F⁻ + H⁺', 'propanoic acid': 'CH₃CH₂COOH ⇌ CH₃CH₂COO⁻ + H⁺'}[w[0]]
    intro = P(r, r.choice([f'{{p}} compares 0.100 mol dm⁻³ {w[0]} with 0.100 mol dm⁻³ hydrochloric acid in {{lab}}.', f'A water-quality laboratory in {{c}} studies solutions of {w[0]} and hydrochloric acid of equal concentration.']))
    parts = [
        lambda r: ('Define a Brønsted–Lowry acid.', 'A proton donor.', '[1]'),
        lambda r: (f'Write an equation to show that {w[0]} is a weak acid.', form, '[1]'),
        lambda r: ('Describe two observations that would show which acid is weaker.', 'Higher pH; lower conductivity; slower reaction with Mg/CaCO₃ for the weak acid.', '[2]'),
        lambda r: (f'Identify the conjugate base of {w[0]}.', form.split('⇌ ')[1].split(' +')[0], '[1]'),
        lambda r: ('Explain why both acids need the same volume of NaOH for neutralisation.', 'Same amount of acid (monoprotic); weak acid equilibrium shifts as H⁺ is removed, until all reacts.', '[2]'),
        lambda r: ('Suggest a suitable indicator for titrating the weak acid with NaOH and explain your choice.', 'Phenolphthalein: equivalence point pH > 7 (about 8–9) within its range.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t7d, t7d_c4)

CHAPTERS[7] = [t7a, t7b, t7c, t7d]

# ===================================================================== Ch8 Reaction kinetics
RATE_RX = [('magnesium ribbon', 'dilute hydrochloric acid', 'hydrogen', 'gas syringe'), ('marble chips (calcium carbonate)', 'dilute hydrochloric acid', 'carbon dioxide', 'gas syringe'),
           ('zinc granules', 'dilute sulfuric acid', 'hydrogen', 'gas syringe'), ('hydrogen peroxide solution', 'manganese(IV) oxide catalyst', 'oxygen', 'gas syringe'),
           ('calcium carbonate powder', 'dilute nitric acid', 'carbon dioxide', 'balance (mass loss)')]

t8a = topic('Rate of reaction: calculating rates from experimental data', 'rate of reaction: calculating rates', 'experimental data')
t8a.fixed('C1', (1, 2), [
    ('What is meant by the rate of a reaction?', 'the change in concentration of a reactant or product per unit time', 'Rate = Δ[conc]/Δt, e.g. mol dm⁻³ s⁻¹.', ['the time taken for the reaction to finish', 'the total amount of product formed', 'the energy released per second']),
    ('What are the units of rate when concentration is in mol dm⁻³ and time in seconds?', 'mol dm⁻³ s⁻¹', 'Rate = Δc/Δt.', ['mol dm⁻³', 's mol⁻¹ dm³', 'mol s']),
    ('How is the initial rate found from a graph of volume of gas against time?', 'by drawing a tangent to the curve at t = 0 and finding its gradient', 'Gradient of tangent at time zero.', ['by reading the final volume', 'by dividing the final volume by the total time', 'by finding the area under the curve']),
    ('Why does the rate of reaction decrease as a reaction proceeds?', 'the concentration of reactants decreases', 'Fewer reactant particles per unit volume, so fewer collisions per second.', ['the activation energy increases', 'the temperature always falls', 'the catalyst is used up']),
    ('Which measurement could follow the rate of CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂?', 'loss of mass of the flask over time', 'CO₂ escapes, so mass falls; or collect gas in a syringe.', ['colour change of the solution', 'increase in pH only at the end', 'mass of CaCl₂ formed at the end']),
    ('State one method other than gas collection for following the rate of a reaction.', 'Mass loss on a balance; colorimetry; titration of samples; pH/conductivity change; time for a cross to disappear.', '[1]'),
])
t8a.fixed('C2', (2, 3, 4), [
    ('Explain why the gradient of a volume-of-gas against time graph decreases with time.', 'As reactants are used up their concentration falls, so collisions are less frequent and the rate (gradient) decreases until it reaches zero.', 'reactant concentration falls [1]; fewer collisions per second [1]'),
    ('Explain why 1/time can be used as a measure of rate in a "disappearing cross" experiment.', 'The same amount of precipitate (sulfur) must form to obscure the cross each time, so rate ∝ amount/time ∝ 1/time.', 'fixed amount of product [1]; rate ∝ 1/t [1]'),
    ('Explain why the final volume of gas is the same when the same mass of marble chips and powder react with excess acid.', 'The same amount of CaCO₃ reacts, so the same amount of CO₂ forms; the powder only increases the rate.', 'same amount of limiting reagent [1]; surface area affects rate only [1]'),
])
errs(t8a, [
    ('The rate of reaction is the total volume of gas produced divided by the time when the reaction stops.', 'That gives an average rate over the whole reaction; the rate at any instant is the gradient of the tangent.'),
    ('Rate of reaction has units of mol dm⁻³.', 'Rate is a change in concentration per unit time: mol dm⁻³ s⁻¹.'),
])
c2mix(t8a, ['{p} measures the volume of gas produced every 30 s during a reaction in {lab}.', 'A student in {c} is analysing rate data from an experiment.'])


@t8a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8a_data(r, D):
    solid, liq, gas, meth = r.choice(RATE_RX[:4])
    Vmax = r.choice([60, 75, 80, 90, 96, 100, 120])
    k = r.choice([0.010, 0.012, 0.015, 0.02, 0.025])
    ts = [0, 30, 60, 90, 120, 180, 240]
    vs = [round(Vmax * (1 - math.exp(-k * t)), 0) for t in ts]
    tab = ', '.join(f'{t} s: {int(v)} cm³' for t, v in zip(ts, vs))
    i = r.randint(0, 3)
    t1, t2 = ts[i], ts[i + 1]
    rate = (vs[i + 1] - vs[i]) / (t2 - t1)
    if D == 1:
        return nmc(r, f'In a reaction, {int(vs[2])} cm³ of gas is collected in the first 60 s. What is the average rate over this time?', vs[2] / 60, [vs[2] * 60, 60 / vs[2] if vs[2] else 1, vs[2] / 30, vs[2] / 120], ' cm³ s⁻¹', f'{int(vs[2])}/60 = {g3(vs[2] / 60)} cm³ s⁻¹.')
    stem = f'{who(r)} reacts {solid} with {liq} and collects the {gas} in a {meth}. Volume readings: {tab}. Calculate the average rate of reaction between {t1} s and {t2} s.'
    key = f'volume change = {int(vs[i + 1])} − {int(vs[i])} = {int(vs[i + 1] - vs[i])} cm³ [1]; rate = {int(vs[i + 1] - vs[i])}/{t2 - t1} = {g3(rate)} cm³ s⁻¹ [1]'
    ans = f'{g3(rate)} cm³ s⁻¹'
    if D >= 3:
        n = (vs[i + 1] - vs[i]) / 24000
        stem += ' Convert this rate into mol of gas per second (molar volume 24 000 cm³ at r.t.p.).'
        key += f'; ÷ 24 000 = {g3(n / (t2 - t1))} mol s⁻¹ [1]'
        ans += f'; {g3(n / (t2 - t1))} mol s⁻¹'
    if D >= 4:
        stem += ' Explain why the rate between 0 and 30 s is greater than between 180 and 240 s.'
        key += '; reactant concentration highest at the start → more frequent collisions [1]'
        ans += '; reactant concentration is greater at the start, so more frequent collisions'
    return {'stem': stem, 'answer': ans, 'key': key}


@t8a.add('C3', (2, 3, 4), 'numerical')
def t8a_conc(r, D):
    c0 = r.choice([0.200, 0.500, 1.00, 0.800])
    frac = r.choice([0.6, 0.5, 0.75, 0.4])
    t = r.choice([20, 40, 50, 80, 100, 120])
    c1 = c0 * frac
    rate = (c0 - c1) / t
    sp = r.choice(['bromine (followed by colorimetry)', 'iodine (followed by colorimetry)', 'hydrochloric acid (followed by titration of samples)', 'the ester (followed by titration)'])
    return {'stem': f'The concentration of {sp} falls from {c0:.3f} mol dm⁻³ to {c1:.3f} mol dm⁻³ in {t} s. Calculate the average rate of reaction, giving units.',
            'answer': f'{g3(rate)} mol dm⁻³ s⁻¹', 'key': f'Δc = {g3(c0 - c1)} mol dm⁻³ [1]; ÷ {t} s = {g3(rate)} mol dm⁻³ s⁻¹ [1]'}


def t8a_c4(r, D):
    solid, liq, gas, meth = r.choice(RATE_RX)
    intro = P(r, r.choice([f'{{p}} investigates the rate of reaction between {solid} and {liq} in {{lab}}, measuring the {gas} produced.', f'A class in {{c}} follows the reaction of {solid} with {liq} using a {meth}.']))
    parts = [
        lambda r: ('Draw a labelled diagram of suitable apparatus.', f'Conical flask with bung and delivery tube to {meth}; stopwatch.' if 'syringe' in meth else 'Flask with cotton-wool plug on a top-pan balance; stopwatch.', '[2]'),
        lambda r: ('Sketch the expected graph and explain its shape.', 'Steep at first, gradient decreases, levels off when limiting reactant used up; concentration falls so fewer collisions.', '[3]'),
        lambda r: ('Describe how to find the initial rate from the graph.', 'Draw a tangent at t = 0; gradient = Δy/Δx.', '[2]'),
        lambda r: ('State two variables that must be controlled.', 'Temperature; concentration/volume of acid; mass and particle size of solid.', '[2]'),
        lambda r: ('Sketch on the same axes the curve for the same mass of solid in smaller pieces, and explain.', 'Steeper initially, same final volume; greater surface area, more frequent collisions.', '[2]'),
        lambda r: ('Suggest one source of error and an improvement.', 'Gas escapes before the bung is inserted (or the timer starts late): use a divided flask or tip the solid in after sealing; take readings at fixed time intervals.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t8a, t8a_c4)

# ---------------------------------------------------------- 8.2 collision theory and Boltzmann
FACTORS8 = [('increasing the concentration of the acid', 'more particles per unit volume, so more frequent collisions; the fraction with E ≥ Ea is unchanged'),
            ('increasing the temperature', 'particles have more kinetic energy: a much greater proportion of collisions have E ≥ Ea (main effect), and collisions are also more frequent'),
            ('using powder instead of lumps', 'greater surface area exposed, so more frequent collisions at the surface'),
            ('increasing the pressure of the gaseous reactants', 'more molecules per unit volume, so more frequent collisions'),
            ('adding a catalyst', 'an alternative route with lower activation energy, so a greater proportion of collisions have E ≥ Ea'),
            ('decreasing the temperature', 'fewer particles have energy ≥ Ea and collisions are less frequent, so fewer successful collisions per second')]

t8b = topic('Collision theory and the Boltzmann distribution', 'collision theory', 'boltzmann distribution')
t8b.fixed('C1', (1, 2), [
    ('What is the activation energy of a reaction?', 'the minimum energy that colliding particles need in order to react', 'Ea: minimum energy for a successful collision.', ['the energy released by the reaction', 'the average energy of the particles', 'the energy needed to melt the reactants']),
    ('In the Boltzmann distribution, what does the area under the curve represent?', 'the total number of molecules', 'Area is constant at different temperatures for the same sample.', ['the activation energy', 'the average energy', 'the rate of reaction']),
    ('How does the Boltzmann distribution change when temperature increases?', 'the peak moves to the right and is lower; more molecules have E ≥ Ea', 'Same area; broader curve shifted to higher energy.', ['the peak moves to the left and is higher', 'the curve does not change', 'the area under the curve increases']),
    ('Why does a small rise in temperature cause a large increase in rate?', 'the proportion of molecules with energy greater than Ea increases greatly', 'Main effect: many more successful collisions; frequency increases only slightly.', ['collision frequency doubles for every 10 °C rise', 'the activation energy decreases', 'the reaction becomes exothermic']),
    ('Where does the Boltzmann distribution curve start?', 'at the origin', 'No molecules have zero energy; the curve never meets the energy axis at high energy.', ['at the activation energy', 'at the peak height', 'at a high number of molecules on the y-axis']),
    ('State two conditions needed for a collision to be successful.', 'Particles must collide with energy ≥ Ea and with the correct orientation.', '[2]'),
])
t8b.fixed('C2', (2, 3, 4), [
    ('Use the Boltzmann distribution to explain why increasing the temperature increases the rate of reaction.', 'At higher temperature the curve shifts to higher energy, so a much larger proportion (area) of molecules have E ≥ Ea; more successful collisions per second.', 'curve shift/more molecules above Ea [1]; more successful collisions per unit time [1]'),
    ('Explain why the Boltzmann distribution curve never meets the energy axis at high energies.', 'There is always a very small number of molecules with very high energy; there is no maximum energy.', 'some molecules with very high energy [1]; no upper limit [1]'),
    ('Explain why increasing concentration increases rate but does not change the proportion of successful collisions.', 'More particles per unit volume give more frequent collisions, but the energy distribution (temperature) is unchanged so the fraction with E ≥ Ea is the same.', 'more frequent collisions [1]; same fraction above Ea [1]'),
])
errs(t8b, [
    ('Increasing temperature increases the rate mainly because particles collide more often.', 'The main reason is that many more particles have energy ≥ Ea; frequency increases only slightly.'),
    ('At a higher temperature the area under the Boltzmann curve increases.', 'The area represents the number of molecules, which is unchanged; the curve flattens and shifts right.'),
    ('Every collision between reactant particles leads to a reaction.', 'Only collisions with energy ≥ Ea and the correct orientation are successful.'),
])
c2mix(t8b, ['{p} draws Boltzmann distributions for a gas at two temperatures.', 'A student in {c} explains rates of reaction using collision theory.'])


@t8b.add('C2', (2, 3, 4), 'explain')
def t8b_factor(r, D):
    f, why = r.choice(FACTORS8)
    rx = r.choice(['magnesium with hydrochloric acid', 'calcium carbonate with nitric acid', 'the decomposition of hydrogen peroxide', 'hydrogen with iodine gas', 'zinc with sulfuric acid', 'sodium thiosulfate with hydrochloric acid'])
    if 'powder' in f and 'gas' in rx:
        return None
    if 'pressure' in f and 'gas' not in rx:
        rx = 'hydrogen with iodine gas'
    return {'stem': f'Explain, using collision theory, the effect on the rate of the reaction of {rx} of {f}.' + (' Refer to the Boltzmann distribution where relevant.' if D >= 3 else ''),
            'answer': f'Rate {"decreases" if "decreas" in f else "increases"}: {why}.' + ((' Boltzmann: the distribution shifts to higher energy (peak lower and further right), so the area above Ea ' + ('decreases.' if 'decreas' in f else 'increases.')) if 'temperature' in f else ' Boltzmann: the curve is unchanged but Ea moves to the left, so a larger area lies above Ea.' if 'catalyst' in f else ' Boltzmann: the distribution and the proportion of particles with E ≥ Ea are unchanged.') * (D >= 3), 'key': 'effect on rate [1]; explanation in terms of collision frequency or energy ≥ Ea [1]' + ('; Boltzmann/proportion above Ea correctly referred to (or stated unchanged) [1]' if D >= 3 else '')}


@t8b.add('C3', (1, 2, 3, 4), 'short')
def t8b_read(r, D):
    T1, T2 = r.choice([(300, 310), (298, 318), (310, 330), (350, 370)])
    f1 = r.choice([0.010, 0.020, 0.015, 0.025])
    mult = r.choice([2, 2.5, 3, 4])
    f2 = f1 * mult
    if D == 1:
        return mc(r, f'In a gas sample at {T1} K, {f1 * 100:.1f}% of molecules have energy ≥ Ea. At {T2} K this becomes {f2 * 100:.1f}%. By what factor would the rate be expected to increase, ignoring the small change in collision frequency?', f'{sf(mult, 2)}', [f'{sf(mult * 2, 2)}', f'{sf(T2 / T1, 3)}', f'{sf(mult / 2, 2)}', '1'], f'Rate ∝ fraction with E ≥ Ea: factor {sf(mult, 2)}.')
    return {'stem': f'For a reaction, {f1 * 100:.1f}% of molecules have energy ≥ Ea at {T1} K and {f2 * 100:.1f}% at {T2} K. Calculate the factor by which the number of molecules able to react increases, and use the Boltzmann distribution to explain why a {T2 - T1} K rise has such a large effect.',
            'answer': f'factor {sf(mult, 2)}; the curve shifts to higher energies so the area beyond Ea increases greatly', 'key': f'factor = {f2 * 100:.1f}/{f1 * 100:.1f} = {sf(mult, 2)} [1]; curve flatter and shifted right [1]; much greater area beyond Ea [1]'}


def t8b_c4(r, D):
    T1, T2 = r.choice([(300, 320), (350, 400), (400, 450)])
    intro = P(r, r.choice([f'{{p}} studies a gas-phase reaction at {T1} K and {T2} K.', f'A research group in {{c}} studies how temperature affects a reaction between gases, at {T1} K and {T2} K.']))
    parts = [
        lambda r: ('Sketch the Boltzmann distribution for the gas at both temperatures, labelling the axes.', f'y: number of molecules with energy E; x: energy. {T2} K curve lower peak, shifted right; same area; both start at origin.', '[3]'),
        lambda r: ('Mark the activation energy and shade the region showing molecules that can react at the higher temperature.', 'Ea on x-axis to the right of the peak; area under the curve to the right of Ea shaded.', '[1]'),
        lambda r: ('Explain why the rate increases with temperature.', 'Greater proportion of molecules with E ≥ Ea; more frequent successful collisions.', '[2]'),
        lambda r: ('Define activation energy.', 'Minimum energy needed by colliding particles for a reaction to occur.', '[1]'),
        lambda r: ('Explain why increasing the pressure also increases the rate, but by a different mechanism.', 'More molecules per unit volume → more frequent collisions; energy distribution unchanged.', '[2]'),
        lambda r: ('State why not all collisions with sufficient energy result in reaction.', 'Particles must also collide with the correct orientation.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(0, 1, 2))


c4reg(t8b, t8b_c4)

# ---------------------------------------------------------- 8.3 catalysts
CATS = [('the Haber process', 'iron', 'heterogeneous'), ('the Contact process', 'vanadium(V) oxide', 'heterogeneous'), ('catalytic converters in cars', 'platinum/rhodium/palladium', 'heterogeneous'),
        ('the hydrogenation of alkenes', 'nickel', 'heterogeneous'), ('esterification', 'concentrated sulfuric acid (H⁺ ions)', 'homogeneous'), ('the oxidation of SO₂ in the atmosphere', 'nitrogen dioxide', 'homogeneous'),
        ('the decomposition of hydrogen peroxide', 'manganese(IV) oxide', 'heterogeneous'), ('the hydration of ethene', 'phosphoric acid on silica', 'heterogeneous'), ('the breakdown of starch in saliva', 'amylase (an enzyme)', 'biological (enzyme)'),
        ('cracking of long-chain alkanes', 'aluminium oxide/zeolites', 'heterogeneous')]

t8c = topic('Effect of catalysts: lower activation energy and the Boltzmann distribution', 'effect of catalysts: lower activation energy', 'catalyst')
t8c.fixed('C1', (1, 2), [
    ('How does a catalyst increase the rate of a reaction?', 'it provides an alternative reaction pathway with a lower activation energy', 'More molecules have E ≥ the lower Ea.', ['it increases the energy of the molecules', 'it increases the temperature', 'it makes the reaction more exothermic']),
    ('What is a homogeneous catalyst?', 'a catalyst in the same phase as the reactants', 'e.g. H⁺(aq) in esterification, NO₂(g) in SO₂ oxidation.', ['a catalyst in a different phase from the reactants', 'a catalyst that is used up', 'a biological catalyst only']),
    ('Which statement about a catalyst is correct?', 'it is chemically unchanged at the end of the reaction', 'Catalysts take part but are regenerated.', ['it is used up in the reaction', 'it changes ΔH for the reaction', 'it changes the position of equilibrium']),
    ('On a Boltzmann distribution, how is the effect of a catalyst shown?', 'Ea is marked at a lower energy, so a larger area lies beyond it', 'The curve itself does not change (same temperature).', ['the curve shifts to the right', 'the curve becomes taller', 'Ea is marked at a higher energy']),
    ('What catalyst is used in the Haber process?', 'iron', 'Heterogeneous catalyst.', ['platinum', 'nickel', 'vanadium(V) oxide']),
    ('State the effect of a catalyst on the enthalpy change of a reaction.', 'No effect: ΔH is unchanged.', '[1]'),
])
t8c.fixed('C2', (2, 3, 4), [
    ('Use the Boltzmann distribution to explain how a catalyst increases the rate of reaction.', 'The catalyst lowers Ea; the curve is unchanged, but a greater proportion of molecules now has energy ≥ Ea, so more successful collisions per second.', 'Ea lowered, curve same [1]; more molecules above Ea [1]'),
    ('Explain why catalysts are important in industry.', 'They allow reactions at lower temperatures, saving energy and cost, and can increase selectivity; they are not used up so small amounts work for a long time.', 'lower temperature/energy saving [1]; reused/not used up [1]'),
    ('Explain why a heterogeneous catalyst is often used as a fine powder or a mesh.', 'Reaction occurs on the surface; a large surface area gives more active sites.', 'surface reaction [1]; larger surface area [1]'),
])
errs(t8c, [
    ('A catalyst gives the reactant molecules more energy.', 'A catalyst lowers the activation energy by providing an alternative route; molecular energies are unchanged.'),
    ('On adding a catalyst the Boltzmann curve moves to the right.', 'The curve is unchanged (same temperature); only the Ea line moves to the left.'),
    ('Catalysts make the reaction more exothermic.', 'ΔH is unchanged by a catalyst.'),
])
c2mix(t8c, ['{p} compares catalysed and uncatalysed decomposition of hydrogen peroxide.', 'An industrial chemist in {c} chooses a catalyst for a manufacturing process.'])


@t8c.add('C1', (1, 2, 3))
def t8c_cat(r, D):
    proc, cat, kind = r.choice(CATS)
    if r.random() < 0.5:
        return mc(r, f'Which catalyst is used in {proc}?', cat, [x[1] for x in CATS], f'{proc}: {cat} ({kind}).')
    return mc(r, f'What type of catalysis is {cat} in {proc}?', kind, ['heterogeneous', 'homogeneous', 'biological (enzyme)', 'autocatalysis'], f'{cat}: {kind}.')


@t8c.add('C3', (2, 3, 4, 5), 'short')
def t8c_profile(r, D):
    dh = r.choice([-98, -196, -57, -92, +52, +90])
    ea = r.choice([75, 120, 180, 210])
    if dh > 0:
        ea += dh
    eac = ea - r.choice([30, 45, 60, 90])
    return {'stem': f'A reaction has ΔH = {sgn(dh)} kJ mol⁻¹. Its activation energy is {ea} kJ mol⁻¹ uncatalysed and {eac} kJ mol⁻¹ with a catalyst. Sketch a reaction pathway diagram showing both routes and calculate the activation energy of the catalysed reverse reaction.',
            'answer': f'Ea(reverse, catalysed) = {eac - dh} kJ mol⁻¹', 'key': f'products {"below" if dh < 0 else "above"} reactants, ΔH labelled [1]; two humps, catalysed lower [1]; Ea(rev) = {eac} − ({sgn(dh)}) = {eac - dh} kJ mol⁻¹ [1]'}


def t8c_c4(r, D):
    proc, cat, kind = r.choice(CATS[:8])
    intro = P(r, r.choice([f'{cap(cat)} is used as a catalyst in {proc}.', f'{{p}} is writing a report on the use of {cat} as a catalyst in {proc}.']))
    parts = [
        lambda r: ('Explain what is meant by a catalyst.', 'A substance that increases the rate of reaction without being used up, by providing an alternative route with lower Ea.', '[2]'),
        lambda r: (f'State whether {cat} acts as a homogeneous or heterogeneous catalyst here, and explain.', f'{kind}: ' + ('different phase from the reactants' if kind == 'heterogeneous' else 'same phase as the reactants' if kind == 'homogeneous' else 'biological catalyst'), '[1]'),
        lambda r: ('Draw a Boltzmann distribution to show how a catalyst increases the rate.', 'Single curve; Ea(cat) to the left of Ea; larger area beyond Ea(cat).', '[3]'),
        lambda r: ('Sketch a reaction pathway diagram for catalysed and uncatalysed routes.', 'Two humps; lower for catalysed; same ΔH.', '[2]'),
        lambda r: ('Give two economic or environmental benefits of using the catalyst.', 'Lower temperature/energy use; less fuel burned so less CO₂; faster production; catalyst reused.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t8c, t8c_c4)

CHAPTERS[8] = [t8a, t8b, t8c]


# ===================================================================== Ch9 Periodicity
P3 = ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar']
P3D = {  # atomic radius nm, ion, ionic radius nm, mp K, structure, conductivity
    'Na': (0.186, 'Na⁺', 0.095, 371, 'giant metallic', 'good'), 'Mg': (0.160, 'Mg²⁺', 0.065, 923, 'giant metallic', 'good (better than Na)'),
    'Al': (0.143, 'Al³⁺', 0.050, 933, 'giant metallic', 'very good (best in Period 3)'), 'Si': (0.117, 'Si⁴⁺', 0.041, 1683, 'giant covalent (giant molecular)', 'semiconductor (poor)'),
    'P': (0.110, 'P³⁻', 0.212, 317, 'simple molecular, P₄', 'non-conductor'), 'S': (0.104, 'S²⁻', 0.184, 392, 'simple molecular, S₈', 'non-conductor'),
    'Cl': (0.099, 'Cl⁻', 0.181, 172, 'simple molecular, Cl₂', 'non-conductor'), 'Ar': (None, None, None, 84, 'monatomic (single atoms)', 'non-conductor'),
}
MP_EXPL = {
    'giant metallic': 'metallic bonding; more delocalised electrons per atom and higher ionic charge from Na to Al gives stronger attraction',
    'giant covalent': 'many strong covalent bonds in a giant structure must be broken',
    'simple molecular': 'only weak instantaneous dipole–induced dipole forces between molecules need to be overcome; strength depends on the number of electrons (S₈ > P₄ > Cl₂)',
    'monatomic': 'very weak London forces between single atoms',
}
OXIDES = {  # element: oxide, bonding/structure, behaviour with water, pH, acid-base nature, equation with water
    'Na': ('Na₂O', 'ionic, giant lattice', 'reacts to form NaOH', '13–14', 'basic', 'Na₂O + H₂O → 2NaOH'),
    'Mg': ('MgO', 'ionic, giant lattice', 'reacts slightly to form Mg(OH)₂', 'about 9', 'basic', 'MgO + H₂O → Mg(OH)₂'),
    'Al': ('Al₂O₃', 'ionic with covalent character, giant lattice', 'insoluble, no reaction', '7', 'amphoteric', 'no reaction'),
    'Si': ('SiO₂', 'giant covalent', 'insoluble, no reaction', '7', 'acidic (reacts with hot concentrated NaOH)', 'no reaction'),
    'P': ('P₄O₁₀', 'simple molecular (covalent)', 'reacts to form phosphoric(V) acid', 'about 2', 'acidic', 'P₄O₁₀ + 6H₂O → 4H₃PO₄'),
    'S': ('SO₂ / SO₃', 'simple molecular (covalent)', 'reacts to form H₂SO₃ / H₂SO₄', 'about 1–2', 'acidic', 'SO₃ + H₂O → H₂SO₄'),
}
CHLORIDES = {
    'Na': ('NaCl', 'ionic', 'dissolves without hydrolysis', '7', 'NaCl(s) → Na⁺(aq) + Cl⁻(aq)'),
    'Mg': ('MgCl₂', 'ionic', 'dissolves with very slight hydrolysis', 'about 6.5', 'MgCl₂(s) → Mg²⁺(aq) + 2Cl⁻(aq)'),
    'Al': ('AlCl₃ (Al₂Cl₆)', 'covalent (simple molecular)', 'hydrolyses, giving steamy fumes of HCl', 'about 3', 'AlCl₃ + 3H₂O → Al(OH)₃ + 3HCl'),
    'Si': ('SiCl₄', 'covalent (simple molecular)', 'hydrolyses vigorously, white solid and fumes of HCl', 'about 1–2', 'SiCl₄ + 2H₂O → SiO₂ + 4HCl'),
    'P': ('PCl₅', 'covalent (simple molecular)', 'hydrolyses vigorously, fumes of HCl', 'about 1–2', 'PCl₅ + 4H₂O → H₃PO₄ + 5HCl'),
}
P3RX = {  # element: with oxygen (obs, eq), with chlorine eq
    'Na': ('burns with a bright yellow flame, white solid', '4Na + O₂ → 2Na₂O', '2Na + Cl₂ → 2NaCl'),
    'Mg': ('burns with a brilliant white flame, white solid', '2Mg + O₂ → 2MgO', 'Mg + Cl₂ → MgCl₂'),
    'Al': ('powder burns with a white flame (surface protected by oxide layer)', '4Al + 3O₂ → 2Al₂O₃', '2Al + 3Cl₂ → 2AlCl₃'),
    'Si': ('reacts slowly on strong heating to form a white solid', 'Si + O₂ → SiO₂', 'Si + 2Cl₂ → SiCl₄'),
    'P': ('white phosphorus burns with a bright white flame, dense white smoke', 'P₄ + 5O₂ → P₄O₁₀', '2P + 5Cl₂ → 2PCl₅'),
    'S': ('burns with a blue flame, choking colourless gas', 'S + O₂ → SO₂', '(sulfur forms S₂Cl₂, not required)'),
}
ONMAX = {'Na': '+1', 'Mg': '+2', 'Al': '+3', 'Si': '+4', 'P': '+5', 'S': '+6'}

t9a = topic('Periodicity of physical properties of Period 3 elements: atomic radius, ionic radius, melting point and conductivity', 'periodicity of physical properties of period 3 elements', 'melting point and conductivity')
t9a.fixed('C1', (1, 2), [
    ('Which Period 3 element has the highest melting point?', 'silicon', 'Si: giant covalent lattice, 1683 K.', ['aluminium', 'sulfur', 'magnesium']),
    ('Which Period 3 element is the best electrical conductor?', 'aluminium', 'Three delocalised electrons per atom.', ['sodium', 'silicon', 'chlorine']),
    ('Why does sulfur have a higher melting point than phosphorus?', 'S₈ molecules have more electrons than P₄, so stronger London forces', 'S₈ (128 e⁻) vs P₄ (60 e⁻).', ['sulfur has covalent bonds and phosphorus does not', 'sulfur is a giant structure', 'sulfur has hydrogen bonding']),
    ('Which ion has the largest radius?', 'P³⁻', 'Anions are larger; P³⁻ has the lowest nuclear charge of the isoelectronic anions.', ['Cl⁻', 'Na⁺', 'Al³⁺']),
    ('Why is the Al³⁺ ion much smaller than the Na⁺ ion?', 'Al³⁺ has more protons for the same number of electrons', 'Isoelectronic (10 e⁻): Al 13 p vs Na 11 p.', ['Al³⁺ has more electron shells', 'Al³⁺ has fewer protons', 'Al³⁺ has more neutrons']),
    ('State the trend in atomic radius across Period 3.', 'Atomic radius decreases from Na to Cl.', '[1]'),
])
t9a.fixed('C2', (2, 3, 4), [
    ('Explain why the melting point increases from sodium to aluminium.', 'Metallic bonding becomes stronger: charge on the ions increases (+1 to +3), ions get smaller and more delocalised electrons per atom, so attraction is stronger.', 'increased ionic charge/smaller ions [1]; more delocalised electrons, stronger metallic bonding [1]'),
    ('Explain why there is a large decrease in melting point from silicon to phosphorus.', 'Si is giant covalent (many strong covalent bonds broken); P is simple molecular P₄ (only weak intermolecular forces overcome).', 'Si giant covalent [1]; P weak intermolecular forces [1]'),
    ('Explain why the ionic radius increases sharply from Si⁴⁺ to P³⁻.', 'Cations have lost the outer (third) shell; anions have gained electrons and keep three shells, so P³⁻ has an extra shell.', 'cations lose outer shell [1]; anions have an extra shell [1]'),
    ('Explain why silicon is a semiconductor.', 'Silicon has a giant covalent structure with no delocalised electrons at low temperature, but a few electrons can be freed on heating, so conductivity is low and increases with temperature.', 'giant covalent, electrons localised [1]; small conductivity increasing with T [1]'),
])
errs(t9a, [
    ('Chlorine has a higher melting point than sulfur because chlorine is more reactive.', 'S₈ has more electrons than Cl₂, so stronger London forces; reactivity does not determine melting point.'),
    ('The melting point of silicon is high because of strong intermolecular forces.', 'Silicon is giant covalent: many strong covalent bonds must be broken.'),
    ('Na⁺ is larger than P³⁻ because sodium is a metal.', 'P³⁻ is larger: anions keep the third shell and have more electron repulsion.'),
])
c2mix(t9a, ['{p} plots properties of the Period 3 elements against proton number.', 'A student in {c} compares the structures of Period 3 elements.'])


@t9a.add('C2', (2, 3, 4), 'explain')
def t9a_pair(r, D):
    a, b = sorted(r.sample(P3, 2), key=P3.index)
    prop = r.choice(['melting point', 'electrical conductivity', 'atomic radius'] if 'Ar' not in (a, b) else ['melting point'])
    if prop == 'melting point':
        hi = a if P3D[a][3] > P3D[b][3] else b
        ka = P3D[a][4].split(',')[0].split(' (')[0]
        kb = P3D[b][4].split(',')[0].split(' (')[0]
        def kk(s):
            for k in MP_EXPL:
                if s.startswith(k):
                    return k
            return 'simple molecular'
        ans = f'{EL[hi][0].capitalize()} has the higher melting point ({P3D[a][3]} K vs {P3D[b][3]} K). {EL[a][0].capitalize()}: {P3D[a][4]} — {MP_EXPL[kk(ka)]}. {EL[b][0].capitalize()}: {P3D[b][4]} — {MP_EXPL[kk(kb)]}.'
    elif prop == 'electrical conductivity':
        hi = a if P3.index(a) <= 2 and (P3.index(b) > 2 or P3.index(a) > P3.index(b)) else b
        ans = f'{EL[a][0]}: {P3D[a][5]}; {EL[b][0]}: {P3D[b][5]}. Metals conduct by delocalised electrons (more per atom Na→Al); Si is a semiconductor; P, S, Cl have no mobile charge carriers.'
    else:
        ans = f'{EL[a][0]} ({P3D[a][0]} nm) is larger than {EL[b][0]} ({P3D[b][0]} nm): nuclear charge increases across the period with similar shielding, so electrons are pulled closer.'
    return {'stem': f'Compare the {prop} of {EL[a][0]} and {EL[b][0]}, and explain the difference in terms of structure and bonding.', 'answer': ans,
            'key': 'correct comparison [1]; structure/bonding or nuclear charge explanation for each [1]' + ('; forces/particles involved named precisely [1]' if D >= 4 else '')}


@t9a.add('C3', (1, 2, 3, 4), 'short')
def t9a_data(r, D):
    el = r.choice(P3[:-1])
    if D == 1:
        return mc(r, f'Which Period 3 element has the structure: {P3D[el][4]}, melting point {P3D[el][3]} K and electrical conductivity: {P3D[el][5]}?', EL[el][0], [EL[x][0] for x in P3 if x != el], f'{EL[el][0]}.')
    k = 3 if D <= 2 else 4
    pick = sorted(r.sample(P3, k), key=lambda x: P3D[x][3])
    return {'stem': 'Place these Period 3 elements in order of increasing melting point and explain the position of the highest: ' + ', '.join(EL[x][0] for x in r.sample(pick, len(pick))) + '.',
            'answer': ' < '.join(EL[x][0] for x in pick) + f'. {EL[pick[-1]][0].capitalize()} is highest: {P3D[pick[-1]][4]}.', 'key': 'correct order [1]; structure of highest identified [1]; reason (bond type broken on melting) [1]'}


def t9a_c4(r, D):
    intro = P(r, r.choice(['The melting points (K) of the Period 3 elements are Na 371, Mg 923, Al 933, Si 1683, P 317, S 392, Cl 172, Ar 84.', '{p} plots a graph of the melting points of the Period 3 elements in {lab}.']))
    parts = [
        lambda r: ('Explain the increase in melting point from Na to Al.', 'Stronger metallic bonding: higher charge, smaller ions, more delocalised electrons.', '[2]'),
        lambda r: ('Explain why silicon has the highest melting point.', 'Giant covalent structure: many strong covalent bonds broken.', '[2]'),
        lambda r: ('Explain the low and varied melting points of P, S and Cl.', 'Simple molecules P₄, S₈, Cl₂: weak London forces; more electrons in S₈ so highest.', '[3]'),
        lambda r: ('Describe and explain the trend in electrical conductivity across the period.', 'Increases Na → Al (more delocalised electrons); Si semiconductor; P to Ar non-conductors (no mobile charge carriers).', '[3]'),
        lambda r: ('Explain why the atomic radius decreases across the period.', 'Increasing nuclear charge with similar shielding.', '[2]'),
        lambda r: ('Explain why argon has the lowest melting point.', 'Monatomic with only very weak London forces (18 electrons).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t9a, t9a_c4)

# ---------------------------------------------------------- 9.2 reactions with oxygen, chlorine and water
t9b = topic('Reactions of Period 3 elements with oxygen, chlorine and water', 'reactions of period 3 elements with oxygen, chlorine and water', 'period 3 reactions')
t9b.fixed('C1', (1, 2), [
    ('What is seen when sodium reacts with cold water?', 'it floats, fizzes, melts into a ball and moves around', '2Na + 2H₂O → 2NaOH + H₂; solution alkaline (pH 13–14).', ['it sinks and reacts very slowly', 'no reaction', 'a white solid forms on the surface only']),
    ('Which equation shows the reaction of magnesium with steam?', 'Mg + H₂O → MgO + H₂', 'With steam MgO forms; with cold water Mg(OH)₂ forms very slowly.', ['Mg + 2H₂O → Mg(OH)₂ + H₂', 'Mg + H₂O → MgH₂ + O', '2Mg + 2H₂O → 2MgOH + H₂']),
    ('Which product forms when phosphorus burns in excess chlorine?', 'PCl₅', 'Excess Cl₂: PCl₅ (limited Cl₂: PCl₃).', ['PCl₃ only', 'P₂Cl₃', 'PCl']),
    ('What colour flame is seen when sulfur burns in oxygen?', 'blue', 'S + O₂ → SO₂.', ['yellow', 'brilliant white', 'lilac']),
    ('Which Period 3 element does not react with oxygen?', 'argon', 'Noble gas with a full outer shell.', ['sulfur', 'silicon', 'phosphorus']),
    ('Write the equation for the reaction of sodium with chlorine.', '2Na + Cl₂ → 2NaCl', '[1]'),
])
t9b.fixed('C2', (2, 3, 4), [
    ('Explain why aluminium appears unreactive with water and oxygen despite its position in the reactivity series.', 'It is covered in a thin, tough layer of aluminium oxide that protects the metal beneath.', 'oxide layer [1]; prevents further reaction [1]'),
    ('Explain why magnesium reacts much faster with steam than with cold water.', 'Steam is at a higher temperature, so more molecules have energy ≥ Ea; magnesium oxide forms rather than a hydroxide layer.', 'higher temperature/more energy [1]; more successful collisions [1]'),
    ('Explain why the maximum oxidation number of Period 3 elements in their oxides rises from +1 to +6.', 'It equals the number of outer-shell electrons used in bonding: Na 1, Mg 2, Al 3, Si 4, P 5, S 6.', 'equals number of outer electrons [1]; examples [1]'),
])
errs(t9b, [
    ('Magnesium reacts vigorously with cold water to form magnesium oxide.', 'Mg reacts very slowly with cold water forming Mg(OH)₂; it forms MgO with steam.'),
    ('Sulfur burns in excess oxygen to form SO₃ directly.', 'Sulfur burns to SO₂; SO₃ needs a catalyst (V₂O₅) and further oxidation.'),
])
c2mix(t9b, ['{p} demonstrates the reactions of Period 3 elements in {lab}.', 'A student in {c} writes equations for reactions of Period 3 elements.'])


@t9b.add('C1', (1, 2, 3))
def t9b_eq(r, D):
    el = r.choice(['Na', 'Mg', 'Al', 'Si', 'P', 'S'])
    obs, ox, cl = P3RX[el]
    if r.random() < 0.5 or el == 'S':
        return mc(r, f'Which equation shows the reaction of {EL[el][0]} with oxygen?', ox, [P3RX[x][1] for x in P3RX if x != el] + ['2Na + O₂ → Na₂O₂ + Na'], f'{ox}; {obs}.')
    return mc(r, f'Which equation shows the reaction of {EL[el][0]} with chlorine?', cl, [P3RX[x][2] for x in P3RX if x not in (el, 'S')], f'{cl}.')


@t9b.add('C3', (2, 3, 4, 5), 'numerical')
def t9b_mass(r, D):
    el = r.choice(['Na', 'Mg', 'Al', 'Si', 'P', 'S'])
    which = r.choice(['oxygen', 'chlorine'] if el != 'S' else ['oxygen'])
    eqtxt = P3RX[el][1] if which == 'oxygen' else P3RX[el][2]
    asc = {'4Na + O₂ → 2Na₂O': '4Na + O2 -> 2Na2O', '2Mg + O₂ → 2MgO': '2Mg + O2 -> 2MgO', '4Al + 3O₂ → 2Al₂O₃': '4Al + 3O2 -> 2Al2O3', 'Si + O₂ → SiO₂': 'Si + O2 -> SiO2',
           'P₄ + 5O₂ → P₄O₁₀': 'P4 + 5O2 -> P4O10', 'S + O₂ → SO₂': 'S + O2 -> SO2', '2Na + Cl₂ → 2NaCl': '2Na + Cl2 -> 2NaCl', 'Mg + Cl₂ → MgCl₂': 'Mg + Cl2 -> MgCl2',
           '2Al + 3Cl₂ → 2AlCl₃': '2Al + 3Cl2 -> 2AlCl3', 'Si + 2Cl₂ → SiCl₄': 'Si + 2Cl2 -> SiCl4', '2P + 5Cl₂ → 2PCl₅': '2P + 5Cl2 -> 2PCl5'}[eqtxt]
    L, R = parse(asc)
    (ka, a), (kg, g) = L
    kb, b = R[0]
    m = r.choice([0.50, 1.00, 1.24, 2.00, 2.43, 2.70, 3.10, 4.60, 5.00])
    na = m / Mr(a)
    stem = f'{m:.2f} g of {EL[el][0]} reacts completely with {which}: {eqtxt}. Calculate the mass of {F(b)} formed'
    key = f'n({F(a)}) = {m:.2f}/{mr1(Mr(a))} = {g3(na)} mol [1]; n({F(b)}) = {g3(na * kb / ka)} mol [1]; mass = {g3(na * kb / ka * Mr(b))} g [1]'
    ans = f'{g3(na * kb / ka * Mr(b))} g'
    if D >= 4:
        vg = na * kg / ka * 24.0
        stem += f' and the volume of {which} used at room temperature and pressure'
        key += f'; V = {g3(na * kg / ka)} × 24.0 = {g3(vg)} dm³ [1]'
        ans += f'; {g3(vg)} dm³'
    return {'stem': stem + '.', 'answer': ans, 'key': key}


def t9b_c4(r, D):
    el = r.choice(['Na', 'Mg', 'Al', 'P'])
    intro = P(r, r.choice([f'{{p}} investigates the reactions of {EL[el][0]} with oxygen, chlorine and water in {{lab}}.', f'A teacher in {{c}} demonstrates the reactions of {EL[el][0]}.']))
    water = {'Na': ('Fizzes, melts, moves; 2Na + 2H₂O → 2NaOH + H₂; pH 13–14', '[2]'), 'Mg': ('Very slow with cold water (Mg + 2H₂O → Mg(OH)₂ + H₂); rapid with steam: Mg + H₂O → MgO + H₂', '[2]'),
             'Al': ('Little reaction due to protective oxide layer.', '[1]'), 'P': ('No reaction with water (stored under water).', '[1]')}[el]
    parts = [
        lambda r: ('Describe what is seen and write an equation for the reaction with oxygen.', f'{P3RX[el][0]}; {P3RX[el][1]}', '[2]'),
        lambda r: ('Write an equation for the reaction with chlorine.', P3RX[el][2], '[1]'),
        lambda r: ('Describe the reaction, if any, with water.', water[0], water[1]),
        lambda r: (f'State the oxidation number of {EL[el][0]} in its oxide and relate it to its electronic configuration.', f'{ONMAX[el]}: equal to the number of outer-shell electrons.', '[2]'),
        lambda r: ('Describe the bonding in the chloride formed and predict its behaviour in water.', f'{CHLORIDES[el][1]}; {CHLORIDES[el][2]}, pH {CHLORIDES[el][3]}', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t9b, t9b_c4)

# ---------------------------------------------------------- 9.3 oxides and chlorides
t9c = topic('Period 3 oxides and chlorides: bonding, acid–base behaviour and reaction with water', 'period 3 oxides and chlorides', 'acid–base behaviour')
t9c.fixed('C1', (1, 2), [
    ('Which Period 3 oxide is amphoteric?', 'Al₂O₃', 'Reacts with acids and with alkalis.', ['MgO', 'SiO₂', 'P₄O₁₀']),
    ('What is the pH of the solution formed when sodium oxide is added to water?', '13–14', 'Na₂O + H₂O → 2NaOH.', ['7', '2', '9']),
    ('Which chloride dissolves in water to give a neutral solution?', 'NaCl', 'Ionic, dissolves without hydrolysis.', ['AlCl₃', 'SiCl₄', 'PCl₅']),
    ('What is observed when SiCl₄ is added to water?', 'steamy fumes of HCl and a white solid', 'SiCl₄ + 2H₂O → SiO₂ + 4HCl.', ['it dissolves to give a neutral solution', 'a yellow precipitate forms', 'no visible change']),
    ('Which oxide reacts with hot concentrated sodium hydroxide but not with water?', 'SiO₂', 'SiO₂ + 2NaOH → Na₂SiO₃ + H₂O (acidic oxide).', ['Na₂O', 'MgO', 'SO₃']),
    ('Write an equation for the reaction of phosphorus(V) oxide with water.', 'P₄O₁₀ + 6H₂O → 4H₃PO₄', '[1]'),
])
t9c.fixed('C2', (2, 3, 4), [
    ('Explain why aluminium oxide is described as amphoteric, giving equations.', 'It reacts with acids: Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; and with alkalis: Al₂O₃ + 2NaOH + 3H₂O → 2NaAl(OH)₄.', 'with acid equation [1]; with alkali equation [1]'),
    ('Explain the trend in the acid–base nature of the Period 3 oxides.', 'Bonding changes from ionic (Na, Mg: basic, contain O²⁻) through amphoteric Al₂O₃ to covalent (Si, P, S: acidic); the electronegativity difference falls across the period.', 'ionic basic → covalent acidic [1]; linked to electronegativity/bonding [1]'),
    ('Explain why MgCl₂ gives a slightly acidic solution but NaCl gives a neutral one.', 'Mg²⁺ is small and doubly charged, so it polarises surrounding water molecules and causes slight hydrolysis releasing H⁺; Na⁺ has a low charge density.', 'Mg²⁺ higher charge density [1]; slight hydrolysis releasing H⁺ [1]'),
    ('Explain why SiO₂ does not react with water although it is an acidic oxide.', 'It is a giant covalent structure; very strong Si–O bonds throughout mean it is insoluble.', 'giant covalent [1]; strong bonds, insoluble [1]'),
])
errs(t9c, [
    ('All Period 3 oxides dissolve in water to form solutions with pH below 7.', 'Na₂O and MgO give alkaline solutions; Al₂O₃ and SiO₂ are insoluble (pH 7); only P and S oxides give acidic solutions.'),
    ('AlCl₃ dissolves in water like NaCl to give a neutral solution.', 'AlCl₃ is covalent and hydrolyses, releasing HCl, so the solution has pH about 3.'),
    ('SiO₂ is a basic oxide because silicon is in the middle of the period.', 'SiO₂ is acidic: it reacts with hot concentrated NaOH to form sodium silicate.'),
])
c2mix(t9c, ['{p} adds Period 3 oxides and chlorides to water and measures the pH in {lab}.', 'A student in {c} relates the bonding in oxides and chlorides to their reactions with water.'])


@t9c.add('C3', (1, 2, 3, 4), 'short')
def t9c_ox(r, D):
    el = r.choice(list(OXIDES))
    ox, bond, beh, ph, nat, eq = OXIDES[el]
    if D == 1:
        return mc(r, f'What is the approximate pH of the mixture when {ox} is added to water?', ph, list({v[3] for v in OXIDES.values()}) + ['10'], f'{ox}: {beh}; pH {ph}.')
    stem = f'Describe the bonding in {ox}, state how it behaves when added to water, and give the approximate pH of the resulting mixture. Write an equation where a reaction occurs.'
    key = f'bonding: {bond} [1]; behaviour: {beh} [1]; pH {ph} [1]' + (f'; equation {eq} [1]' if eq != 'no reaction' else '')
    if D >= 4:
        stem += ' Classify the oxide as acidic, basic or amphoteric and write an equation for its reaction with ' + ('sodium hydroxide.' if 'acid' in nat or nat == 'amphoteric' else 'hydrochloric acid.')
        extra = {'Na': 'Na₂O + 2HCl → 2NaCl + H₂O', 'Mg': 'MgO + 2HCl → MgCl₂ + H₂O', 'Al': 'Al₂O₃ + 2NaOH + 3H₂O → 2NaAl(OH)₄', 'Si': 'SiO₂ + 2NaOH → Na₂SiO₃ + H₂O',
                 'P': 'P₄O₁₀ + 12NaOH → 4Na₃PO₄ + 6H₂O', 'S': 'SO₂ + 2NaOH → Na₂SO₃ + H₂O'}[el]
        key += f'; {nat} [1]; {extra} [1]'
        return {'stem': stem, 'answer': f'{bond}; {beh}; pH {ph}; {nat}; {extra}', 'key': key}
    return {'stem': stem, 'answer': f'{bond}; {beh}; pH {ph}' + (f'; {eq}' if eq != 'no reaction' else ''), 'key': key}


@t9c.add('C3', (2, 3, 4), 'short')
def t9c_cl(r, D):
    el = r.choice(list(CHLORIDES))
    cl, bond, beh, ph, eq = CHLORIDES[el]
    return {'stem': f'{person(r)} adds {cl} to water. Describe the bonding in {cl}, what is observed, the approximate pH and write an equation for the change.',
            'answer': f'{bond}; {beh}; pH {ph}; {eq}', 'key': f'{bond} [1]; observation/hydrolysis or simple dissolving [1]; pH {ph} [1]' + (f'; equation [1]' if D >= 3 else '')}


def t9c_c4(r, D):
    intro = P(r, r.choice(['{p} is given samples of the oxides Na₂O, MgO, Al₂O₃, SiO₂, P₄O₁₀ and SO₃ in {lab}.', 'A teacher in {c} asks students to relate the structures of the Period 3 chlorides NaCl, MgCl₂, AlCl₃, SiCl₄ and PCl₅ to their reactions with water.']))
    oxi = 'oxides' in intro
    parts = ([
        lambda r: ('Describe the trend in bonding across the oxides.', 'Ionic (Na₂O, MgO), ionic with covalent character (Al₂O₃), giant covalent (SiO₂), simple covalent (P₄O₁₀, SO₃).', '[2]'),
        lambda r: ('Write equations for the reactions of Na₂O and SO₃ with water and give the pH of each solution.', 'Na₂O + H₂O → 2NaOH, pH 13–14; SO₃ + H₂O → H₂SO₄, pH 1', '[3]'),
        lambda r: ('Write two equations to show the amphoteric nature of Al₂O₃.', 'Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; Al₂O₃ + 2NaOH + 3H₂O → 2NaAl(OH)₄', '[2]'),
        lambda r: ('Explain why SiO₂ does not dissolve in water but is classified as acidic.', 'Giant covalent, insoluble; reacts with hot concentrated NaOH forming Na₂SiO₃.', '[2]'),
        lambda r: ('Explain the change from basic to acidic oxides in terms of electronegativity.', 'Electronegativity difference with O falls across period: ionic oxides give O²⁻ (basic); covalent oxides react to form acids.', '[2]'),
    ] if oxi else [
        lambda r: ('Describe the bonding in NaCl and in SiCl₄.', 'NaCl ionic lattice; SiCl₄ simple covalent molecules.', '[2]'),
        lambda r: ('Describe what is seen and write an equation when SiCl₄ is added to water.', 'Steamy fumes, white solid: SiCl₄ + 2H₂O → SiO₂ + 4HCl', '[2]'),
        lambda r: ('Write an equation for the hydrolysis of PCl₅ and give the pH of the solution.', 'PCl₅ + 4H₂O → H₃PO₄ + 5HCl; pH 1–2', '[2]'),
        lambda r: ('Explain why NaCl gives a neutral solution.', 'Ionic; ions are simply hydrated, no hydrolysis.', '[1]'),
        lambda r: ('Explain why AlCl₃ gives an acidic solution.', 'Covalent/small highly charged Al³⁺ polarises water; hydrolysis releases H⁺/HCl, pH 3.', '[2]'),
    ])
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t9c, t9c_c4)

# ---------------------------------------------------------- 9.4 deducing an unknown element
UNK = {  # element -> clues
    'Na': ['its oxide dissolves in water to give a solution of pH 14', 'it reacts vigorously with cold water releasing hydrogen', 'its chloride is ionic and gives a neutral solution in water', 'it conducts electricity and has a melting point of 371 K'],
    'Mg': ['its oxide is basic and only slightly soluble, giving pH about 9', 'it burns with a brilliant white flame', 'it reacts very slowly with cold water but rapidly with steam', 'its highest oxidation number is +2'],
    'Al': ['its oxide reacts with both hydrochloric acid and sodium hydroxide', 'its chloride sublimes and exists as dimers in the vapour', 'it is the best electrical conductor in Period 3', 'its highest oxidation number is +3'],
    'Si': ['its oxide is a giant covalent solid that reacts with hot concentrated NaOH', 'it has the highest melting point in Period 3', 'it is a semiconductor', 'its chloride, XCl₄, hydrolyses to give a white solid and HCl'],
    'P': ['its oxide reacts with water to give a solution of pH 2 containing a triprotic acid', 'it forms two chlorides, XCl₃ and XCl₅', 'it exists as tetrahedral X₄ molecules', 'its highest oxidation number is +5'],
    'S': ['it burns with a blue flame giving a choking gas', 'its element exists as crown-shaped X₈ molecules', 'it forms two common oxides, XO₂ and XO₃', 'its highest oxidation number is +6'],
}

t9d = topic('Deducing the nature and position of an unknown element from its properties', 'deducing the nature and position of an unknown element', 'unknown element')
t9d.fixed('C1', (1, 2), [
    ('Element X forms an oxide with formula X₂O₃ that reacts with both acids and bases. What is X?', 'aluminium', 'Amphoteric Al₂O₃.', ['magnesium', 'phosphorus', 'silicon']),
    ('Element Y has a chloride YCl₄ that fumes in moist air. In which group is Y?', '14', 'SiCl₄ hydrolyses; Si is in Group 14.', ['4', '2', '17']),
    ('An element in Period 3 has an oxide that gives a pH of 13 in water. Which element is it?', 'sodium', 'Na₂O + H₂O → 2NaOH.', ['sulfur', 'phosphorus', 'aluminium']),
    ('A Period 3 element exists as X₄ molecules and its oxide is acidic. What is X?', 'phosphorus', 'White phosphorus P₄; P₄O₁₀ acidic.', ['sulfur', 'silicon', 'chlorine']),
    ('State one property that would show an unknown Period 3 element is a metal.', 'Conducts electricity as a solid (or forms a basic oxide/ionic chloride).', '[1]'),
])
t9d.fixed('C2', (2, 3, 4), [
    ('Explain how the formula of the highest oxide of a Period 3 element can be used to deduce its group.', 'The oxidation number in the highest oxide equals the number of outer electrons, giving the group (e.g. X₂O₅: +5, Group 15).', 'oxidation number from formula [1]; equals outer electrons/group [1]'),
    ('Explain how the pH of the solution formed when a chloride is added to water helps identify the element.', 'Ionic chlorides of Na/Mg give pH 7 or 6.5; covalent chlorides (Al, Si, P) hydrolyse to give acidic solutions (pH 1–3).', 'ionic neutral [1]; covalent hydrolyse acidic [1]'),
])
c2mix(t9d, ['{p} is given clues about an unknown Period 3 element.', 'In a chemistry competition in {c}, teams identify elements from their properties.'])


@t9d.add('C3', (1, 2, 3, 4, 5), 'short')
def t9d_id(r, D):
    el = r.choice(list(UNK))
    k = 1 if D <= 1 else 2 if D <= 3 else 3
    cl = r.sample(UNK[el], k)
    if D == 1:
        return mc(r, f'A Period 3 element X has these properties: {cl[0]}. Identify X.', EL[el][0], [EL[x][0] for x in UNK if x != el], f'{EL[el][0]}.')
    stem = f'Element X is in Period 3. ' + '; '.join(cap(c) for c in cl) + '. Identify X and explain how each piece of information supports your answer.'
    if D >= 4:
        stem += ' Write the formula of its highest oxide and of its chloride.'
    hox = {'Na': 'Na₂O', 'Mg': 'MgO', 'Al': 'Al₂O₃', 'Si': 'SiO₂', 'P': 'P₄O₁₀', 'S': 'SO₃'}[el]
    hcl = {'Na': 'NaCl', 'Mg': 'MgCl₂', 'Al': 'AlCl₃', 'Si': 'SiCl₄', 'P': 'PCl₅', 'S': 'S₂Cl₂'}[el]
    return {'stem': stem, 'answer': f'X is {EL[el][0]} (Group {GROUP.get(el, 16 if el == "S" else 14)})' + (f'; {hox}; {hcl}' if D >= 4 else ''),
            'key': f'identifies {EL[el][0]} [1]; ' + ' '.join('links clue to property [1]' for _ in cl) + (' formulae correct [1]' if D >= 4 else '')}


def t9d_c4(r, D):
    el = r.choice(list(UNK))
    cl = r.sample(UNK[el], 3)
    intro = P(r, f'{{p}} is given an unknown Period 3 element X. Observations: ' + '; '.join(cl) + '.')
    hox = {'Na': 'Na₂O', 'Mg': 'MgO', 'Al': 'Al₂O₃', 'Si': 'SiO₂', 'P': 'P₄O₁₀', 'S': 'SO₃'}[el]
    parts = [
        lambda r: ('Identify X, explaining your reasoning.', f'{EL[el][0]}', '[2]'),
        lambda r: ('State the structure and bonding of the element.', P3D[el][4], '[1]'),
        lambda r: ('Write the formula of the highest oxide and state its acid–base nature.', f'{hox}; {OXIDES[el][4]}', '[2]'),
        lambda r: ('Predict the pH of the solution formed when the chloride of X is added to water.', CHLORIDES.get(el, ('', '', '', 'about 1–2 (hydrolysis)'))[3], '[1]'),
        lambda r: ('Write the full electronic configuration of X.', cstr(config(EL[el][1])), '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t9d, t9d_c4)

CHAPTERS[9] = [t9a, t9b, t9c, t9d]

# ===================================================================== Ch10 Group 2
G2 = ['Mg', 'Ca', 'Sr', 'Ba']
G2D = {'Be': (9.0, 0.112, 1560), 'Mg': (24.3, 0.160, 923), 'Ca': (40.1, 0.197, 1115), 'Sr': (87.6, 0.215, 1050), 'Ba': (137.3, 0.217, 1000)}
DEC_T = {'Mg': 540, 'Ca': 900, 'Sr': 1290, 'Ba': 1360}  # carbonate decomposition temperature °C (approx)

t10a = topic('Physical properties and trends in reactivity of Group 2 elements', 'physical properties and trends in reactivity of group 2', 'group 2')
t10a.fixed('C1', (1, 2), [
    ('How does the reactivity of Group 2 metals change down the group?', 'it increases', 'Outer electrons lost more easily (lower IE).', ['it decreases', 'it stays the same', 'it increases then decreases']),
    ('Which Group 2 element has the largest atomic radius?', 'barium', 'An extra shell each period down.', ['magnesium', 'calcium', 'beryllium']),
    ('Why does the first ionisation energy decrease down Group 2?', 'outer electrons are further from the nucleus and more shielded', 'Distance and shielding outweigh increased nuclear charge.', ['nuclear charge decreases', 'atoms gain protons', 'the outer electrons are paired']),
    ('What is the outer-shell configuration of all Group 2 atoms?', 'ns²', 'Two s electrons, lost to form M²⁺.', ['ns¹', 'ns²np¹', 'ns²np⁶']),
    ('Which Group 2 element reacts most vigorously with water?', 'barium', 'Reactivity increases down the group.', ['magnesium', 'calcium', 'strontium']),
    ('State the trend in the first ionisation energy down Group 2.', 'It decreases.', '[1]'),
])
t10a.fixed('C2', (2, 3, 4), [
    ('Explain why the reactivity of the Group 2 elements increases down the group.', 'The two outer electrons are further from the nucleus and more shielded, so less energy is needed to remove them (lower sum of first and second IEs).', 'further/more shielded [1]; electrons lost more easily [1]'),
    ('Explain why Group 2 elements always form 2+ ions.', 'They have two outer-shell (s) electrons; removing them gives a noble-gas configuration, but the third IE (from an inner shell) is far too high.', 'two outer electrons [1]; third IE very high [1]'),
    ('Explain why the melting points of the Group 2 metals generally decrease down the group.', 'Metal ions become larger with the same charge, so the attraction between the ions and the delocalised electrons weakens.', 'larger ions, same charge [1]; weaker metallic bonding [1]'),
])
errs(t10a, [
    ('Reactivity decreases down Group 2 because nuclear charge increases.', 'Reactivity increases: extra shells and shielding outweigh increased nuclear charge, so electrons are lost more easily.'),
    ('Group 2 elements form 1+ ions because the first ionisation energy is lowest.', 'They lose both outer electrons to form M²⁺; the energy is recovered from lattice/hydration enthalpies.'),
])
c2mix(t10a, ['{p} compares the reactions of Group 2 metals in {lab}.', 'A student in {c} explains trends in Group 2.'])


@t10a.add('C2', (2, 3, 4), 'explain')
def t10a_pair(r, D):
    a, b = sorted(r.sample(G2, 2), key=G2.index)
    prop = r.choice(['reactivity with water', 'first ionisation energy', 'atomic radius'])
    hi = {'reactivity with water': b, 'first ionisation energy': a, 'atomic radius': b}[prop]
    return {'stem': f'Predict which of {EL[a][0]} and {EL[b][0]} has the greater {prop}, and explain your answer in terms of atomic structure.',
            'answer': f'{EL[hi][0].capitalize()}. {EL[b][0].capitalize()} has more occupied shells, so its outer electrons are further from the nucleus and more shielded; ' + ('they are lost more easily.' if hi == b and prop != 'atomic radius' else 'less energy is needed to remove them.' if prop == 'first ionisation energy' else 'so the atom is larger.'),
            'key': 'correct element [1]; extra shell/shielding explanation [1]' + ('; effect of nuclear charge outweighed [1]' if D >= 4 else '')}


@t10a.add('C3', (1, 2, 3, 4), 'numerical')
def t10a_calc(r, D):
    m = r.choice(['Mg', 'Ca', 'Sr', 'Ba'])
    mass = r.choice([0.120, 0.200, 0.240, 0.400, 0.500, 0.800, 1.00])
    n = mass / AR[m]
    v = n * 24000
    if D == 1:
        return mc(r, f'Which equation shows the reaction of {EL[m][0]} with water?', f'{m} + 2H₂O → {m}(OH)₂ + H₂', [f'{m} + H₂O → {m}O + H₂' if m != 'Mg' else 'Mg + 2H₂O → MgO₂ + 2H₂', f'2{m} + 2H₂O → 2{m}OH + H₂', f'{m} + H₂O → {m}H₂ + O', f'{m} + 2H₂O → {m}(OH)₂ + O₂'], 'M + 2H₂O → M(OH)₂ + H₂ (Mg with steam gives MgO).')
    return {'stem': f'{mass:.3f} g of {EL[m][0]} reacts completely with excess {"water" if m != "Mg" else "dilute hydrochloric acid"}. Write an equation and calculate the volume of hydrogen produced at room temperature and pressure, in cm³.',
            'answer': (f'{m} + 2H₂O → {m}(OH)₂ + H₂' if m != 'Mg' else 'Mg + 2HCl → MgCl₂ + H₂') + f'; {g3(v)} cm³', 'key': f'equation [1]; n({m}) = {mass:.3f}/{AR[m]} = {g3(n)} mol [1]; V = {g3(n)} × 24 000 = {g3(v)} cm³ [1]'}


def t10a_c4(r, D):
    intro = P(r, r.choice(['{p} adds small pieces of magnesium, calcium, strontium and barium to cold water in {lab}.', 'A data table in {c} lists atomic radii and first ionisation energies of the Group 2 elements: Mg 0.160 nm 738; Ca 0.197 nm 590; Sr 0.215 nm 550; Ba 0.217 nm 503 kJ mol⁻¹.']))
    parts = [
        lambda r: ('Describe and explain the trend in atomic radius.', 'Increases: extra shell each period.', '[2]'),
        lambda r: ('Explain why first ionisation energy decreases down the group.', 'Outer electrons further from nucleus, more shielding; outweighs increased nuclear charge.', '[2]'),
        lambda r: ('Write an equation for the reaction of calcium with water and describe what is seen.', 'Ca + 2H₂O → Ca(OH)₂ + H₂; fizzing, calcium sinks, cloudy white suspension forms.', '[2]'),
        lambda r: ('Explain why barium reacts faster with water than calcium.', 'Lower ionisation energies; electrons lost more easily.', '[2]'),
        lambda r: ('Write an equation for the reaction of magnesium with steam.', 'Mg + H₂O → MgO + H₂', '[1]'),
        lambda r: ('Predict a property of radium, the element below barium.', 'Even more reactive with water; lower IE; larger radius.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t10a, t10a_c4)

# ---------------------------------------------------------- 10.2 reactions with water and acids
t10b = topic('Reactions of Group 2 elements and oxides, hydroxides and carbonates with water and dilute acids', 'reactions of group 2 elements and oxides, hydroxides and carbonates', 'water and dilute acids')
t10b.fixed('C1', (1, 2), [
    ('What forms when calcium oxide reacts with water?', 'calcium hydroxide', 'CaO + H₂O → Ca(OH)₂ (slaked lime).', ['calcium carbonate', 'calcium peroxide', 'calcium hydride']),
    ('Why does the reaction of calcium carbonate lumps with dilute sulfuric acid soon stop?', 'insoluble calcium sulfate forms a coating on the carbonate', 'CaSO₄ is sparingly soluble and blocks further reaction.', ['the acid evaporates', 'the reaction is reversible', 'calcium carbonate dissolves completely']),
    ('Which compound is used by farmers to reduce the acidity of soil?', 'calcium hydroxide', 'Slaked lime neutralises acidic soil.', ['calcium chloride', 'magnesium sulfate', 'barium sulfate']),
    ('Which gas is produced when barium carbonate reacts with dilute nitric acid?', 'carbon dioxide', 'BaCO₃ + 2HNO₃ → Ba(NO₃)₂ + H₂O + CO₂.', ['hydrogen', 'oxygen', 'nitrogen dioxide']),
    ('Which ionic equation represents the reaction of a Group 2 oxide with an acid?', 'O²⁻ + 2H⁺ → H₂O', 'Basic oxides neutralise acids.', ['O²⁻ + H⁺ → OH⁻ + H₂', 'M²⁺ + 2H⁺ → MH₂', 'MO + H₂O → MO₂ + H₂']),
    ('Write an equation for the reaction of magnesium oxide with hydrochloric acid.', 'MgO + 2HCl → MgCl₂ + H₂O', '[1]'),
])
t10b.fixed('C2', (2, 3, 4), [
    ('Explain why the pH of the solution formed by adding Group 2 oxides to water increases down the group.', 'The hydroxides become more soluble down the group, so the concentration of OH⁻ ions in solution increases.', 'hydroxide solubility increases [1]; higher [OH⁻] [1]'),
    ('Explain why limewater turns milky with carbon dioxide.', 'CO₂ reacts with aqueous calcium hydroxide to form insoluble calcium carbonate: Ca(OH)₂ + CO₂ → CaCO₃ + H₂O.', 'CaCO₃ insoluble precipitate [1]; equation [1]'),
    ('Explain why barium sulfate can be swallowed for X-ray imaging even though barium ions are toxic.', 'BaSO₄ is very insoluble, so almost no Ba²⁺ ions are absorbed; it is dense and absorbs X-rays.', 'insoluble [1]; absorbs X-rays [1]'),
])
errs(t10b, [
    ('Magnesium oxide dissolves readily in water to give a strongly alkaline solution.', 'MgO is only slightly soluble; the solution has a pH of about 9.'),
    ('Calcium carbonate reacts completely with dilute sulfuric acid in the same way as with hydrochloric acid.', 'Insoluble CaSO₄ coats the carbonate and the reaction stops; with HCl soluble CaCl₂ forms.'),
])
c2mix(t10b, ['{p} tests Group 2 compounds with water and dilute acids in {lab}.', 'A farmer in {c} asks why lime is spread on fields.'])

G2CPD = [('oxide', 'O', 'MO + 2HCl -> MCl2 + H2O', 'MO + H2O -> M(OH)2'), ('hydroxide', '(OH)2', 'M(OH)2 + 2HCl -> MCl2 + 2H2O', None), ('carbonate', 'CO3', 'MCO3 + 2HCl -> MCl2 + H2O + CO2', None)]


@t10b.add('C1', (1, 2, 3))
def t10b_eq(r, D):
    m = r.choice(G2)
    kind, suf, eq, weq = r.choice(G2CPD)
    acid = r.choice(['HCl', 'HNO3'])
    e = eq.replace('M', m)
    if acid == 'HNO3':
        e = e.replace('2HCl', '2HNO3').replace(f'{m}Cl2', f'{m}(NO3)2')
    right = E(e)
    wr = [E(e.replace('2H', 'H', 1)), E(e.replace(' + H2O', ' + H2')) if 'H2O' in e else E(e + ' + H2'), E(e.replace(f'{m}Cl2', f'{m}Cl').replace(f'{m}(NO3)2', f'{m}NO3')), E(e.replace('2HCl', 'HCl').replace('2HNO3', 'HNO3').replace('2H2O', 'H2O'))]
    return mc(r, f'Which is the balanced equation for the reaction of {EL[m][0]} {kind} with dilute {"hydrochloric" if acid == "HCl" else "nitric"} acid?', right, wr, f'{right}.')


@t10b.add('C3', (2, 3, 4, 5), 'numerical')
def t10b_calc(r, D):
    m = r.choice(G2)
    kind = r.choice(['carbonate', 'oxide', 'hydroxide'])
    f = {'carbonate': f'{m}CO3', 'oxide': f'{m}O', 'hydroxide': f'{m}(OH)2'}[kind]
    mass = r.choice([0.500, 0.750, 1.00, 1.25, 1.50, 2.00])
    c = r.choice([0.500, 1.00, 2.00])
    n = mass / Mr(f)
    V = 2 * n / c * 1000
    stem = f'{mass:.3f} g of {EL[m][0]} {kind}, {F(f)}, reacts exactly with {c:.2f} mol dm⁻³ hydrochloric acid. Calculate the volume of acid needed, in cm³.'
    key = f'n({F(f)}) = {mass:.3f}/{mr1(Mr(f))} = {g3(n)} mol [1]; n(HCl) = 2 × {g3(n)} = {g3(2 * n)} mol [1]; V = {g3(V)} cm³ [1]'
    ans = f'{g3(V)} cm³'
    if kind == 'carbonate' and D >= 4:
        stem += ' Calculate also the volume of CO₂ released at r.t.p.'
        key += f'; V(CO₂) = {g3(n * 24000)} cm³ [1]'
        ans += f'; {g3(n * 24000)} cm³ CO₂'
    return {'stem': stem, 'answer': ans, 'key': key}


def t10b_c4(r, D):
    m = r.choice(['Ca', 'Mg', 'Sr'])
    intro = P(r, r.choice([f'{{p}} investigates the reactions of {EL[m][0]} oxide, hydroxide and carbonate in {{lab}}.', f'A lime works in {{c}} heats limestone (CaCO₃) to make quicklime, CaO, which is then slaked with water.']))
    if 'lime works' in intro:
        m = 'Ca'
    parts = [
        lambda r: (f'Write an equation for the reaction of {EL[m][0]} oxide with water and predict the pH of the solution.', f'{m}O + H₂O → {m}(OH)₂; pH about {"9" if m == "Mg" else "11–12" if m == "Ca" else "12–13"}', '[2]'),
        lambda r: (f'Write an equation for the reaction of {EL[m][0]} carbonate with dilute hydrochloric acid.', E(f'{m}CO3 + 2HCl -> {m}Cl2 + H2O + CO2'), '[1]'),
        lambda r: ('Explain why the reaction of calcium carbonate with dilute sulfuric acid stops after a short time.', 'Insoluble CaSO₄ forms a layer on the solid.', '[2]'),
        lambda r: ('Describe one agricultural use of calcium hydroxide and explain the chemistry.', 'Neutralises acidic soils: Ca(OH)₂ + 2H⁺ → Ca²⁺ + 2H₂O.', '[2]'),
        lambda r: ('Describe how limewater is used to test for CO₂.', 'Bubble gas through; limewater turns milky (CaCO₃ precipitate).', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t10b, t10b_c4)

# ---------------------------------------------------------- 10.3 thermal decomposition and solubility
t10c = topic('Thermal decomposition of nitrates and carbonates; solubility of hydroxides and sulfates', 'thermal decomposition of nitrates and carbonates', 'solubility of hydroxides and sulfates')
t10c.fixed('C1', (1, 2), [
    ('How does the thermal stability of the Group 2 carbonates change down the group?', 'it increases', 'Larger cations polarise the carbonate ion less.', ['it decreases', 'it stays the same', 'there is no pattern']),
    ('What are the products when magnesium nitrate is heated?', 'magnesium oxide, nitrogen dioxide and oxygen', '2Mg(NO₃)₂ → 2MgO + 4NO₂ + O₂.', ['magnesium nitrite and oxygen', 'magnesium, nitrogen and oxygen', 'magnesium oxide and nitrogen']),
    ('Which Group 2 hydroxide is the least soluble?', 'magnesium hydroxide', 'Solubility of hydroxides increases down the group.', ['barium hydroxide', 'strontium hydroxide', 'calcium hydroxide']),
    ('Which Group 2 sulfate is the least soluble?', 'barium sulfate', 'Solubility of sulfates decreases down the group.', ['magnesium sulfate', 'calcium sulfate', 'strontium sulfate']),
    ('What colour gas is seen when a Group 2 nitrate is heated?', 'brown', 'Nitrogen dioxide is brown.', ['colourless only', 'yellow-green', 'purple']),
    ('Write the equation for the thermal decomposition of calcium carbonate.', 'CaCO₃ → CaO + CO₂', '[1]'),
])
t10c.fixed('C2', (2, 3, 4), [
    ('Explain why magnesium carbonate decomposes at a lower temperature than barium carbonate.', 'Mg²⁺ is smaller with the same charge, so it has a higher charge density and polarises (distorts) the carbonate ion more, weakening a C–O bond.', 'Mg²⁺ smaller/higher charge density [1]; polarises carbonate ion more [1]'),
    ('Explain how aqueous barium chloride is used to test for sulfate ions.', 'Add dilute HCl then BaCl₂(aq); a white precipitate of BaSO₄ forms because barium sulfate is insoluble.', 'acidify then add BaCl₂ [1]; white BaSO₄ precipitate [1]'),
    ('Explain why magnesium hydroxide is used as an antacid but not barium hydroxide.', 'Mg(OH)₂ is only slightly soluble, a weak alkali, so it neutralises excess acid safely; Ba(OH)₂ is soluble, strongly alkaline and Ba²⁺ is toxic.', 'Mg(OH)₂ sparingly soluble/mild [1]; Ba(OH)₂ soluble/toxic [1]'),
])
errs(t10c, [
    ('Barium carbonate decomposes more easily than magnesium carbonate because barium is more reactive.', 'BaCO₃ is more stable: the large Ba²⁺ ion polarises the carbonate ion less.'),
    ('Group 2 nitrates decompose to give the metal nitrite and oxygen.', 'Group 2 nitrates give the oxide, NO₂ and O₂ (it is Group 1 nitrates, except Li, that give nitrites).'),
    ('The solubility of both hydroxides and sulfates increases down Group 2.', 'Hydroxide solubility increases but sulfate solubility decreases down the group.'),
])
c2mix(t10c, ['{p} heats Group 2 carbonates and nitrates in {lab}.', 'A student in {c} compares the solubilities of Group 2 compounds.'])


@t10c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10c_decomp(r, D):
    m = r.choice(G2)
    kind = r.choice(['carbonate', 'nitrate'])
    if kind == 'carbonate':
        f, eq, ratio_g = f'{m}CO3', f'{m}CO3 -> {m}O + CO2', 1
    else:
        f, eq, ratio_g = f'{m}(NO3)2', f'2{m}(NO3)2 -> 2{m}O + 4NO2 + O2', 2.5
    mass = r.choice([0.840, 1.00, 1.48, 2.00, 2.50, 3.00, 5.00])
    n = mass / Mr(f)
    mo = n * Mr(f'{m}O')
    if D == 1:
        return mc(r, f'Which equation shows the thermal decomposition of {EL[m][0]} {kind}?', E(eq), [E(f'{m}CO3 -> {m} + CO2 + O2' if kind == 'carbonate' else f'{m}(NO3)2 -> {m}(NO2)2 + O2'), E(f'{m}CO3 -> {m}O2 + CO' if kind == 'carbonate' else f'{m}(NO3)2 -> {m}O + 2NO2'), E(f'2{m}CO3 -> 2{m}O + CO2' if kind == 'carbonate' else f'{m}(NO3)2 -> {m} + 2NO2 + O2')], f'{E(eq)}.')
    stem = f'{who(r)} heats {mass:.3f} g of {EL[m][0]} {kind}, {F(f)}, to constant mass: {E(eq)}. Calculate the mass of solid residue and the total volume of gas produced at r.t.p.'
    key = f'n({F(f)}) = {mass:.3f}/{mr1(Mr(f))} = {g3(n)} mol [1]; residue {F(m + "O")}: {g3(n)} × {mr1(Mr(m + "O"))} = {g3(mo)} g [1]; gas = {g3(n * ratio_g)} mol × 24.0 = {g3(n * ratio_g * 24.0)} dm³ [1]'
    ans = f'{g3(mo)} g; {g3(n * ratio_g * 24.0)} dm³'
    if D >= 4:
        stem += ' Explain how the temperature needed for this decomposition would compare with that for the corresponding ' + ('barium' if m != 'Ba' else 'magnesium') + ' compound.'
        key += '; charge density/polarisation of anion argument [1]'
        ans += '; ' + ('higher temperature for barium compound: Ba²⁺ larger, polarises anion less' if m != 'Ba' else 'lower temperature for magnesium compound: Mg²⁺ smaller, polarises anion more')
    return {'stem': stem, 'answer': ans, 'key': key}


@t10c.add('C1', (1, 2, 3))
def t10c_sol(r, D):
    kind = r.choice(['hydroxide', 'sulfate'])
    a, b = r.sample(G2, 2)
    more = (b if G2.index(b) > G2.index(a) else a) if kind == 'hydroxide' else (a if G2.index(a) < G2.index(b) else b)
    return mc(r, f'Which is more soluble in water: {EL[a][0]} {kind} or {EL[b][0]} {kind}?', f'{EL[more][0]} {kind}', [f'{EL[a][0]} {kind}', f'{EL[b][0]} {kind}', 'they are equally soluble', 'both are completely insoluble'], f'{kind}s: solubility {"increases" if kind == "hydroxide" else "decreases"} down Group 2.')


def t10c_c4(r, D):
    m = r.choice(['Mg', 'Ca', 'Sr'])
    intro = P(r, r.choice([f'{{p}} heats samples of Group 2 nitrates and carbonates and records the time for limewater to turn milky or for brown gas to appear.', f'A research student in {{c}} studies the thermal stability of {EL[m][0]} nitrate and carbonate.']))
    parts = [
        lambda r: (f'Write an equation for the thermal decomposition of {EL[m][0]} nitrate.', E(f'2{m}(NO3)2 -> 2{m}O + 4NO2 + O2'), '[2]'),
        lambda r: ('Describe and explain the trend in thermal stability of the carbonates down Group 2.', 'Increases: cations larger, lower charge density, less polarisation of CO₃²⁻.', '[3]'),
        lambda r: ('Describe a fair way to compare the thermal stabilities of the carbonates.', 'Same moles/mass of each, same heating (same burner/flame), time for limewater to turn milky.', '[2]'),
        lambda r: ('State the trends in solubility of the hydroxides and sulfates.', 'Hydroxides more soluble down group; sulfates less soluble.', '[2]'),
        lambda r: ('Describe a test for sulfate ions using a Group 2 compound.', 'Acidify with dilute HCl, add BaCl₂(aq): white precipitate of BaSO₄.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t10c, t10c_c4)

CHAPTERS[10] = [t10a, t10b, t10c]

# ===================================================================== Ch11 Group 17
HAL = {  # name, state/colour, bp °C, X–X kJ, H–X kJ, solution colours
    'F': ('fluorine', 'pale yellow gas', -188, 158, 562, None), 'Cl': ('chlorine', 'pale yellow-green gas', -34, 242, 431, ('pale green', 'pale green')),
    'Br': ('bromine', 'red-brown liquid', 59, 193, 366, ('orange/yellow', 'orange-red')), 'I': ('iodine', 'grey-black solid (purple vapour)', 184, 151, 299, ('brown', 'violet/purple')),
}
HX = ['Cl', 'Br', 'I']
SILVER = {'Cl': ('white', 'dissolves in dilute ammonia'), 'Br': ('cream', 'dissolves in concentrated ammonia only'), 'I': ('yellow', 'insoluble in concentrated ammonia')}
H2SO4 = {'Cl': ('steamy white fumes of HCl', 'NaCl + H₂SO₄ → NaHSO₄ + HCl', 'no further reaction: HCl is not a strong enough reducing agent to reduce H₂SO₄'),
         'Br': ('steamy fumes of HBr, orange/brown fumes of Br₂ and colourless SO₂', '2HBr + H₂SO₄ → Br₂ + SO₂ + 2H₂O', 'HBr reduces H₂SO₄ (S +6 → +4)'),
         'I': ('steamy fumes, purple vapour/black solid (I₂), yellow solid (S) and smell of bad eggs (H₂S)', '8HI + H₂SO₄ → 4I₂ + H₂S + 4H₂O', 'HI is the strongest reducing agent and reduces S from +6 to −2')}

t11a = topic('Physical properties and volatility of the halogens; bond strength of hydrogen halides', 'physical properties and volatility of the halogens', 'bond strength of hydrogen halides')
t11a.fixed('C1', (1, 2), [
    ('What is the appearance of bromine at room temperature?', 'a red-brown liquid', 'Cl₂ pale yellow-green gas; Br₂ red-brown liquid; I₂ grey-black solid.', ['a pale yellow-green gas', 'a grey-black solid', 'a colourless liquid']),
    ('How does the volatility of the halogens change down the group?', 'it decreases', 'Boiling point increases as London forces increase.', ['it increases', 'it stays the same', 'it increases then decreases']),
    ('Which hydrogen halide is the least thermally stable?', 'HI', 'H–I bond weakest (299 kJ mol⁻¹); a hot wire decomposes HI to purple I₂.', ['HF', 'HCl', 'HBr']),
    ('Why is the F–F bond weaker than the Cl–Cl bond?', 'repulsion between lone pairs on the small, close F atoms', 'Short bond brings non-bonding pairs close together.', ['fluorine has fewer protons', 'F₂ is a liquid', 'fluorine is less electronegative']),
    ('What is the colour of iodine vapour?', 'purple', 'Iodine sublimes on warming to a purple vapour.', ['brown', 'green', 'colourless']),
    ('State the trend in the bond strength of the hydrogen halides from HCl to HI.', 'Decreases (HCl > HBr > HI).', '[1]'),
])
t11a.fixed('C2', (2, 3, 4), [
    ('Explain why the boiling points of the halogens increase down the group.', 'Molecules have more electrons, so stronger instantaneous dipole–induced dipole forces; more energy is needed to separate them.', 'more electrons [1]; stronger London forces [1]'),
    ('Explain why the thermal stability of the hydrogen halides decreases from HF to HI.', 'The halogen atom becomes larger so the H–X bond is longer and weaker; less energy is needed to break it.', 'longer bond [1]; weaker, less energy to break [1]'),
    ('Explain why HCl is a gas but HF is a liquid on a cold day (bp 20 °C).', 'HF forms hydrogen bonds between molecules; HCl has only permanent dipole and London forces.', 'HF hydrogen bonding [1]; stronger than forces in HCl [1]'),
])
errs(t11a, [
    ('Iodine is the most volatile halogen because its molecules are largest.', 'Iodine is the least volatile: its large molecules have the strongest London forces.'),
    ('The bond energies of the halogens decrease steadily from F₂ to I₂.', 'F–F (158) is anomalously weak because of lone-pair repulsion; Cl–Cl (242) is the strongest.'),
])
c2mix(t11a, ['{p} compares the physical properties of the halogens in {lab}.', 'A student in {c} explains the thermal stability of the hydrogen halides.'])


@t11a.add('C2', (2, 3, 4), 'explain')
def t11a_pair(r, D):
    a, b = r.sample(['F', 'Cl', 'Br', 'I'], 2)
    prop = r.choice(['boiling point', 'thermal stability of the hydrogen halide'])
    if prop == 'boiling point':
        hi = a if HAL[a][2] > HAL[b][2] else b
        why = f'{HAL[hi][0]} molecules have more electrons, so stronger instantaneous dipole–induced dipole forces'
        data = f'(boiling points {HAL[a][2]} °C and {HAL[b][2]} °C)'
    else:
        hi = a if HAL[a][4] > HAL[b][4] else b
        why = f'H–{hi} is shorter and stronger ({HAL[hi][4]} kJ mol⁻¹ vs {HAL[b if hi == a else a][4]} kJ mol⁻¹)'
        data = ''
    return {'stem': f'Compare the {prop} of {HAL[a][0]} and {HAL[b][0]} {data} and explain the difference.'.replace('  ', ' ').replace(' .', '.'),
            'answer': f'{HAL[hi][0].capitalize()} {"has the higher boiling point" if prop == "boiling point" else "forms the more stable hydrogen halide"}: {why}.', 'key': 'correct comparison [1]; reason (electrons/London forces or bond length/strength) [1]' + ('; more energy needed to separate molecules/break bonds [1]' if D >= 4 else '')}


@t11a.add('C3', (1, 2, 3, 4), 'short')
def t11a_data(r, D):
    x = r.choice(['F', 'Cl', 'Br', 'I'])
    if D == 1:
        return mc(r, f'What is the appearance of {HAL[x][0]} at room temperature?', HAL[x][1], [v[1] for v in HAL.values()] + ['colourless gas'], f'{HAL[x][0]}: {HAL[x][1]}.')
    a = r.choice(HX)
    return {'stem': f'A red-hot wire is plunged into separate tubes of HCl, HBr and HI. Predict and explain what is seen in the tube of {F("H" + a)}. Use the bond energies H–Cl 431, H–Br 366, H–I 299 kJ mol⁻¹.' + (' Write an equation for any decomposition.' if D >= 3 else ''),
            'answer': {'Cl': 'No change: H–Cl bond strong, not broken.', 'Br': 'Slight orange-brown colour: some HBr decomposes to Br₂.', 'I': 'Purple vapour: HI decomposes into H₂ and I₂ because the H–I bond is weakest.'}[a] + ({'Cl': ' No decomposition, so no equation.', 'Br': ' 2HBr → H₂ + Br₂', 'I': ' 2HI → H₂ + I₂'}[a] if D >= 3 else ''),
            'key': 'correct observation [1]; linked to bond energy [1]' + ('; equation 2HX → H₂ + X₂ where relevant [1]' if D >= 3 else '')}


def t11a_c4(r, D):
    intro = P(r, r.choice(['Data for the halogens: F₂ bp −188 °C, F–F 158 kJ mol⁻¹; Cl₂ bp −34 °C, Cl–Cl 242; Br₂ bp 59 °C, Br–Br 193; I₂ bp 184 °C, I–I 151.', '{p} is preparing a poster on the physical properties of the Group 17 elements for a school in {c}.']))
    parts = [
        lambda r: ('Describe the appearance of chlorine, bromine and iodine at room temperature.', 'Cl₂ pale yellow-green gas; Br₂ red-brown liquid; I₂ grey-black solid.', '[2]'),
        lambda r: ('Explain the trend in volatility.', 'Decreases: more electrons, stronger London forces.', '[2]'),
        lambda r: ('Explain why the F–F bond is weaker than expected.', 'Small atoms; repulsion between lone pairs on adjacent F atoms.', '[1]'),
        lambda r: ('Describe and explain the trend in thermal stability of HCl, HBr and HI.', 'Decreases: bond length increases, bond energy decreases.', '[2]'),
        lambda r: ('Predict the state and colour of astatine.', 'Black solid (less volatile than iodine).', '[1]'),
        lambda r: ('Draw a dot-and-cross diagram of HCl and state the type of intermolecular force.', 'Shared pair H–Cl with three lone pairs on Cl; pd-pd (plus London) forces.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(1, 2))


c4reg(t11a, t11a_c4)

# ---------------------------------------------------------- 11.2 oxidising agents; halide reactions
t11b = topic('Halogens as oxidising agents; reactions of halide ions with silver nitrate and concentrated sulfuric acid', 'halogens as oxidising agents', 'reactions of halide ions with silver nitrate and concentrated sulfuric acid')
t11b.fixed('C1', (1, 2), [
    ('Which halogen is the strongest oxidising agent?', 'fluorine', 'Oxidising power decreases down the group.', ['chlorine', 'bromine', 'iodine']),
    ('What colour precipitate forms when aqueous silver nitrate is added to a solution of potassium bromide?', 'cream', 'AgBr is cream; AgCl white; AgI yellow.', ['white', 'yellow', 'brown']),
    ('Which silver halide is insoluble in concentrated aqueous ammonia?', 'silver iodide', 'AgCl dissolves in dilute NH₃; AgBr in conc NH₃; AgI in neither.', ['silver chloride', 'silver bromide', 'silver fluoride']),
    ('Which halide ion is the strongest reducing agent?', 'I⁻', 'Reducing power of halides increases down the group.', ['F⁻', 'Cl⁻', 'Br⁻']),
    ('Which gas with a smell of bad eggs is produced when concentrated sulfuric acid is added to solid sodium iodide?', 'hydrogen sulfide', 'I⁻ reduces S from +6 to −2.', ['sulfur dioxide', 'hydrogen chloride', 'chlorine']),
    ('Why is dilute nitric acid added before aqueous silver nitrate in the test for halide ions?', 'to remove carbonate (and other) ions that would also give a precipitate', 'Acidify with HNO₃ (not HCl, which adds Cl⁻).', ['to make the precipitate dissolve', 'to oxidise the halide', 'to provide nitrate ions for the precipitate']),
    ('Write the ionic equation for the reaction of chlorine with bromide ions.', 'Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂', '[1]'),
])
t11b.fixed('C2', (2, 3, 4), [
    ('Explain why chlorine displaces bromine from aqueous potassium bromide but iodine does not.', 'Chlorine is a stronger oxidising agent than bromine (its atom more readily gains an electron, smaller with less shielding); iodine is weaker than bromine.', 'oxidising power Cl₂ > Br₂ > I₂ [1]; reason in terms of electron gain [1]'),
    ('Explain why bromide ions can reduce concentrated sulfuric acid but chloride ions cannot.', 'Br⁻ is larger, so its outer electron is further from the nucleus and more easily lost; Br⁻ is a stronger reducing agent than Cl⁻.', 'Br⁻ larger, loses electron more easily [1]; stronger reducing agent [1]'),
    ('Explain why a few cm³ of cyclohexane is added in halogen displacement experiments.', 'Halogens are more soluble in the non-polar solvent and show distinctive colours (Br₂ orange-red, I₂ violet), making identification easier.', 'halogen dissolves in organic layer [1]; distinctive colours [1]'),
])
errs(t11b, [
    ('Iodine displaces chlorine from aqueous sodium chloride.', 'Iodine is a weaker oxidising agent than chlorine, so there is no reaction.'),
    ('Silver chloride is yellow and insoluble in ammonia.', 'AgCl is white and dissolves in dilute ammonia; AgI is yellow and insoluble.'),
    ('Concentrated sulfuric acid oxidises chloride ions to chlorine.', 'Cl⁻ is not a strong enough reducing agent; only HCl fumes form.'),
])
c2mix(t11b, ['{p} tests unknown halide solutions in {lab}.', 'A water-analysis laboratory in {c} identifies halide ions in samples.'])


@t11b.add('C3', (1, 2, 3, 4), 'short')
def t11b_disp(r, D):
    x, y = r.sample(['Cl', 'Br', 'I'], 2)
    salt = r.choice(['potassium', 'sodium'])
    reacts = ['Cl', 'Br', 'I'].index(x) < ['Cl', 'Br', 'I'].index(y)
    if D == 1:
        return mc(r, f'Aqueous {HAL[x][0]} is added to aqueous {salt} {HAL[y][0][:-3] + "ide" if y != "I" else "iodide"}. What happens?', 'a displacement reaction occurs' if reacts else 'no reaction occurs',
                  ['a displacement reaction occurs', 'no reaction occurs', 'a white precipitate forms', 'hydrogen gas is evolved'], f'{HAL[x][0]} is {"stronger" if reacts else "weaker"} oxidising agent than {HAL[y][0]}.')
    yion = {'Cl': 'chloride', 'Br': 'bromide', 'I': 'iodide'}[y]
    stem = f'{person(r)} adds aqueous {HAL[x][0]} to aqueous {salt} {yion}, then shakes the mixture with cyclohexane. Describe what is seen and write an ionic equation for any reaction.'
    if reacts:
        ans = f'Aqueous layer turns {HAL[y][5][0]}; cyclohexane layer {HAL[y][5][1]}. {F(x + "2")} + 2{F(y)}⁻ → 2{F(x)}⁻ + {F(y + "2")}'
    else:
        ans = f'No reaction: {HAL[x][0]} is a weaker oxidising agent than {HAL[y][0]}; colour of the {HAL[x][0]} solution only.'
    if D >= 4:
        stem += ' Explain your answer in terms of the relative oxidising power of the halogens.'
        ans += f' Oxidising power decreases down the group (Cl₂ > Br₂ > I₂): the halogen atom is larger and attracts an extra electron less strongly, so {HAL[x][0]} ' + ('can' if reacts else 'cannot') + f' oxidise {yion} ions.'
    return {'stem': stem, 'answer': ans, 'key': 'reaction or no reaction correctly predicted [1]; colours [1]' + ('; ionic equation [1]' if reacts else '; reason [1]') + ('; explanation of oxidising power [1]' if D >= 4 else '')}


@t11b.add('C3', (2, 3, 4, 5), 'short')
def t11b_test(r, D):
    x = r.choice(HX)
    nm = {'Cl': 'chloride', 'Br': 'bromide', 'I': 'iodide'}[x]
    if r.random() < 0.5:
        col, nh3 = SILVER[x]
        return {'stem': f'A solution contains an unknown halide ion. On adding dilute nitric acid and then aqueous silver nitrate, a {col} precipitate forms that {nh3.replace("dissolves", "dissolves").replace("insoluble", "is insoluble")}. Identify the halide ion and write an ionic equation for the precipitation.' + (' Explain why dilute nitric acid is added first.' if D >= 3 else ''),
                'answer': f'{nm} ion, {F(x)}⁻; Ag⁺(aq) + {F(x)}⁻(aq) → Ag{F(x)}(s)' + ('; HNO₃ removes carbonate (and hydroxide) ions, which would also give a precipitate with Ag⁺' if D >= 3 else ''), 'key': f'{nm} identified [1]; ionic equation with state symbols [1]' + ('; role of HNO₃ explained [1]' if D >= 3 else '')}
    obs, eq, why = H2SO4[x]
    return {'stem': f'Concentrated sulfuric acid is added to solid sodium {nm}. Describe what is seen and write an equation for any redox reaction. Explain the difference from the reaction with sodium chloride.' if x != 'Cl' else 'Concentrated sulfuric acid is added to solid sodium chloride. Describe what is seen, write an equation and explain why no further redox reaction occurs.',
            'answer': f'{cap(obs)}; {eq}; {why}', 'key': 'observations [1]; equation [1]; explanation in terms of reducing power of halide [1]'}


@t11b.add('C3', (2, 3, 4, 5), 'short')
def t11b_unknown(r, D):
    x = r.choice(HX)
    nm = {'Cl': 'chloride', 'Br': 'bromide', 'I': 'iodide'}[x]
    cat = r.choice(['sodium', 'potassium', 'magnesium', 'calcium', 'lithium'])
    tests = [('acidified aqueous silver nitrate', f'{SILVER[x][0]} precipitate'),
             ('dilute then concentrated aqueous ammonia added to the precipitate', SILVER[x][1].replace('dissolves', 'precipitate dissolves').replace('insoluble', 'precipitate is insoluble')),
             ('chlorine water, then shaking with cyclohexane', 'no change' if x == 'Cl' else f'organic layer turns {HAL[x][5][1]}'),
             ('concentrated sulfuric acid added to the solid', H2SO4[x][0])]
    k = 2 if D <= 3 else 3
    pick = r.sample(tests, k)
    lab_ = person(r)
    return {'stem': f'{lab_} tests a solution of an unknown {cat} halide, Q. Results: ' + '; '.join(f'{t}: {o}' for t, o in pick) + '. Identify the anion in Q and explain how each result supports your answer.',
            'answer': f'{nm} ({F(x)}⁻): ' + '; '.join(f'{o} is characteristic of {nm}' for t, o in pick), 'key': f'{nm} identified [1]; ' + ' '.join('result interpreted [1]' for _ in pick)}


def t11b_c4(r, D):
    x = r.choice(HX)
    nm = {'Cl': 'chloride', 'Br': 'bromide', 'I': 'iodide'}[x]
    intro = P(r, r.choice([f'{{p}} is given a white solid that is a sodium halide. The tests below are carried out in {{lab}}.', f'A forensic laboratory in {{c}} analyses an unknown sodium halide, which is sodium {nm}.']))
    parts = [
        lambda r: ('Describe the silver nitrate test and the results for each halide.', 'Acidify with HNO₃, add AgNO₃(aq): Cl⁻ white, Br⁻ cream, I⁻ yellow; confirm with NH₃(aq).', '[3]'),
        lambda r: (f'State the observations with concentrated sulfuric acid for sodium {nm}.', H2SO4[x][0], '[2]'),
        lambda r: ('Write an equation for the redox reaction with concentrated sulfuric acid, if any.', H2SO4[x][1] if x != 'Cl' else 'none (NaCl + H₂SO₄ → NaHSO₄ + HCl only, not redox)', '[1]'),
        lambda r: ('Explain the trend in reducing power of the halide ions.', 'Increases Cl⁻ < Br⁻ < I⁻: larger ions, outer electrons further from nucleus and more shielded, more easily lost.', '[2]'),
        lambda r: ('Write an ionic equation for the reaction of chlorine water with this halide, if any.', (f'Cl₂ + 2{F(x)}⁻ → 2Cl⁻ + {F(x + "2")}' if x != 'Cl' else 'no reaction'), '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t11b, t11b_c4)

# ---------------------------------------------------------- 11.3 disproportionation; water treatment
t11c = topic('Disproportionation of chlorine with cold and hot sodium hydroxide; chlorine in water treatment', 'disproportionation of chlorine', 'chlorine in water treatment')
t11c.fixed('C1', (1, 2), [
    ('What forms when chlorine reacts with cold dilute aqueous sodium hydroxide?', 'sodium chloride, sodium chlorate(I) and water', 'Cl₂ + 2NaOH → NaCl + NaClO + H₂O.', ['sodium chloride and sodium chlorate(V)', 'sodium chloride and hydrogen', 'sodium chlorate(VII) only']),
    ('What forms when chlorine reacts with hot concentrated aqueous sodium hydroxide?', 'sodium chloride, sodium chlorate(V) and water', '3Cl₂ + 6NaOH → 5NaCl + NaClO₃ + 3H₂O.', ['sodium chloride and sodium chlorate(I)', 'sodium chlorate(VII) and water', 'sodium hypochlorite and hydrogen']),
    ('What is the oxidation number of chlorine in NaClO₃?', '+5', 'Na +1, O −2 ×3: Cl = +5.', ['+3', '+1', '+7']),
    ('Which species in chlorinated water kills bacteria?', 'chloric(I) acid, HClO', 'Cl₂ + H₂O ⇌ HCl + HClO; HClO (and ClO⁻) kill microorganisms.', ['hydrochloric acid', 'chloride ions', 'hydrogen gas']),
    ('Which name is used for NaClO, the active ingredient of household bleach?', 'sodium chlorate(I)', 'Also called sodium hypochlorite.', ['sodium chlorate(V)', 'sodium chloride', 'sodium perchlorate']),
    ('Write the equation for the reaction of chlorine with water.', 'Cl₂ + H₂O ⇌ HCl + HClO', '[1]'),
])
t11c.fixed('C2', (2, 3, 4), [
    ('Explain why the reaction of chlorine with cold NaOH is a disproportionation reaction.', 'Chlorine (0) is both reduced to −1 in NaCl and oxidised to +1 in NaClO.', '0 → −1 [1]; 0 → +1 [1]'),
    ('Discuss the benefits and risks of adding chlorine to drinking water.', 'Benefit: kills bacteria, preventing diseases such as cholera; risks: chlorine is toxic in high concentrations and can react with organic matter to form harmful chlorinated compounds.', 'benefit [1]; risk [1]'),
    ('Explain why the products of chlorine with NaOH depend on temperature.', 'At higher temperature chlorate(I) itself disproportionates into chloride and chlorate(V), so hot NaOH gives NaClO₃.', 'ClO⁻ disproportionates when hot [1]; forms ClO₃⁻ and Cl⁻ [1]'),
])
errs(t11c, [
    ('In cold NaOH, chlorine is only reduced.', 'Chlorine is both reduced (to Cl⁻, −1) and oxidised (to ClO⁻, +1): disproportionation.'),
    ('Hot NaOH and chlorine produce sodium chlorate(I).', 'Hot concentrated NaOH gives sodium chlorate(V), NaClO₃, and sodium chloride.'),
])
c2mix(t11c, ['A water-treatment works in {c} uses chlorine to disinfect drinking water.', '{p} investigates the reactions of chlorine with sodium hydroxide in {lab}.'])


@t11c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11c_calc(r, D):
    if D == 1:
        sp = r.choice([('NaClO', '+1'), ('NaClO3', '+5'), ('NaCl', '−1'), ('Cl2', '0'), ('HClO', '+1'), ('NaClO4', '+7')])
        return mc(r, f'What is the oxidation number of chlorine in {F(sp[0])}?', sp[1], ['+1', '+3', '+5', '+7', '−1', '0'], f'Cl in {F(sp[0])}: {sp[1]}.')
    kind = r.choice(['cold', 'hot', 'water'])
    if kind == 'water':
        V = r.choice([1.0, 5.0, 10.0, 50.0])  # million dm3
        ppm = r.choice([0.5, 1.0, 2.0, 0.8])
        kg = V * 1e6 * ppm / 1e6
        return {'stem': f'A water-treatment plant in {city(r)} treats {V:g} million dm³ of water per day and adds chlorine to a concentration of {ppm} mg dm⁻³. Calculate the mass of chlorine used per day in kg and the volume of chlorine gas this represents at r.t.p.',
                'answer': f'{g3(kg)} kg; {g3(kg * 1000 / 71.0 * 24.0)} dm³', 'key': f'mass = {V:g} × 10⁶ × {ppm} mg = {g3(kg)} kg [1]; n = {g3(kg * 1000)}/71.0 = {g3(kg * 1000 / 71.0)} mol [1]; V = × 24.0 = {g3(kg * 1000 / 71.0 * 24.0)} dm³ [1]'}
    vol = r.choice([0.480, 0.720, 1.20, 2.40])
    n = vol / 24.0
    if kind == 'cold':
        m = n * Mr('NaClO')
        naoh = 2 * n
        return {'stem': f'{vol:.3f} dm³ of chlorine (measured at r.t.p.) is bubbled into excess cold dilute sodium hydroxide. Write the equation and calculate the mass of sodium chlorate(I) formed and the amount of NaOH used.',
                'answer': f'Cl₂ + 2NaOH → NaCl + NaClO + H₂O; {g3(m)} g NaClO; {g3(naoh)} mol NaOH', 'key': f'equation [1]; n(Cl₂) = {g3(n)} mol [1]; n(NaClO) = {g3(n)} mol, mass = {g3(m)} g [1]; NaOH = {g3(naoh)} mol [1]'}
    m = n / 3 * Mr('NaClO3')
    return {'stem': f'{vol:.3f} dm³ of chlorine (r.t.p.) reacts with hot concentrated sodium hydroxide. Write the equation, and calculate the mass of sodium chlorate(V) formed. State the oxidation number changes of chlorine.',
            'answer': f'3Cl₂ + 6NaOH → 5NaCl + NaClO₃ + 3H₂O; {g3(m)} g; 0 → −1 and 0 → +5', 'key': f'equation [1]; n(Cl₂) = {g3(n)} mol, n(NaClO₃) = {g3(n / 3)} mol [1]; mass = {g3(m)} g [1]; oxidation numbers 0 → −1 and +5 [1]'}


@t11c.add('C3', (2, 3, 4), 'short')
def t11c_on(r, D):
    eq = r.choice([('Cl2 + 2NaOH -> NaCl + NaClO + H2O', 'yes', '0 → −1 and +1', 'Cl₂ is both oxidised (to NaClO) and reduced (to NaCl)'),
                   ('3Cl2 + 6NaOH -> 5NaCl + NaClO3 + 3H2O', 'yes', '0 → −1 and +5', 'Cl₂ is both oxidised (to NaClO₃) and reduced (to NaCl)'),
                   ('Cl2 + H2O -> HCl + HClO', 'yes', '0 → −1 and +1', 'Cl₂ is both oxidised (to HClO) and reduced (to HCl)'),
                   ('Cl2 + 2KBr -> 2KCl + Br2', 'no', 'Cl 0 → −1 only; Br −1 → 0', 'Br⁻ is oxidised; Cl₂ is reduced'),
                   ('3NaClO -> 2NaCl + NaClO3', 'yes', '+1 → −1 and +5', 'ClO⁻ is both oxidised (to ClO₃⁻) and reduced (to Cl⁻)'),
                   ('NaClO + 2HCl -> NaCl + Cl2 + H2O', 'no (comproportionation)', '+1 and −1 → 0', 'Cl⁻ (from HCl) is oxidised; ClO⁻ is reduced'),
                   ('4KClO3 -> 3KClO4 + KCl', 'yes', '+5 → +7 and −1', 'ClO₃⁻ is both oxidised (to ClO₄⁻) and reduced (to Cl⁻)'),
                   ('H2 + Cl2 -> 2HCl', 'no', 'Cl 0 → −1; H 0 → +1', 'H₂ is oxidised; Cl₂ is reduced')])
    return {'stem': f'Use oxidation numbers to decide whether the reaction {E(eq[0])} is a disproportionation. Explain your answer.' + (' Identify the species oxidised and the species reduced.' if D >= 4 else ''),
            'answer': f'{cap(eq[1])}: chlorine oxidation numbers {eq[2]}.' + (f' {eq[3]}.' if D >= 4 else ''),
            'key': 'oxidation numbers of chlorine in all species [1]; conclusion with reason (same element both oxidised and reduced or not) [1]' + ('; identifies oxidising/reducing roles [1]' if D >= 4 else '')}


def t11c_c4(r, D):
    intro = P(r, r.choice(['A town in {c} disinfects its water supply with chlorine.', '{p} makes bleach in {lab} by passing chlorine into cold sodium hydroxide, and compares it with the product from hot sodium hydroxide.']))
    parts = [
        lambda r: ('Write an equation for the reaction of chlorine with water and identify the species that kills bacteria.', 'Cl₂ + H₂O ⇌ HCl + HClO; HClO (chloric(I) acid)', '[2]'),
        lambda r: ('Write the equation for the reaction of chlorine with cold dilute NaOH.', 'Cl₂ + 2NaOH → NaCl + NaClO + H₂O', '[1]'),
        lambda r: ('Write the equation for the reaction with hot concentrated NaOH and give the oxidation numbers of chlorine in each product.', '3Cl₂ + 6NaOH → 5NaCl + NaClO₃ + 3H₂O; −1 and +5', '[3]'),
        lambda r: ('Define disproportionation using one of these reactions.', 'Same element simultaneously oxidised and reduced, e.g. Cl 0 → −1 and +1.', '[2]'),
        lambda r: ('Give one benefit and one risk of chlorinating drinking water.', 'Kills pathogens/prevents disease; toxic chlorinated organic by-products / toxicity of Cl₂.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t11c, t11c_c4)

CHAPTERS[11] = [t11a, t11b, t11c]

# ===================================================================== Ch12 Nitrogen and sulfur
FERT12 = [('ammonium nitrate', 'NH4NO3'), ('ammonium sulfate', '(NH4)2SO4'), ('ammonium chloride', 'NH4Cl'), ('ammonium phosphate', '(NH4)3PO4'), ('urea', 'CO(NH2)2')]

t12a = topic('Lack of reactivity of nitrogen; ammonia and the ammonium ion: shape and basicity', 'lack of reactivity of nitrogen', 'ammonia and the ammonium ion')
t12a.fixed('C1', (1, 2), [
    ('Why is nitrogen gas very unreactive?', 'the N≡N triple bond is very strong and the molecule is non-polar', 'N≡N bond energy 944 kJ mol⁻¹.', ['nitrogen has no lone pairs', 'nitrogen is a noble gas', 'nitrogen molecules are ionic']),
    ('What is the shape of the ammonium ion?', 'tetrahedral', 'Four bonding pairs, no lone pairs: 109.5°.', ['trigonal pyramidal', 'square planar', 'trigonal planar']),
    ('Why is ammonia a Brønsted–Lowry base?', 'its lone pair on nitrogen can accept a proton', 'NH₃ + H⁺ → NH₄⁺.', ['it donates a proton', 'it contains hydroxide ions', 'it has no lone pairs']),
    ('Which gas is produced when ammonium chloride is warmed with aqueous sodium hydroxide?', 'ammonia', 'NH₄⁺ + OH⁻ → NH₃ + H₂O; turns damp red litmus blue.', ['nitrogen', 'hydrogen', 'chlorine']),
    ('Which test identifies ammonia gas?', 'damp red litmus paper turns blue', 'NH₃ is the only common alkaline gas.', ['limewater turns milky', 'a glowing splint relights', 'damp blue litmus turns red']),
    ('Write the equation for the reaction of ammonia with water.', 'NH₃ + H₂O ⇌ NH₄⁺ + OH⁻', '[1]'),
])
t12a.fixed('C2', (2, 3, 4), [
    ('Explain why nitrogen is used to fill food packaging.', 'It is very unreactive (strong triple bond, non-polar) so it does not oxidise food or support microbial growth.', 'unreactive [1]; reason (triple bond/non-polar) [1]'),
    ('Explain why ammonia is described as a weak base.', 'It only partially reacts with water to form NH₄⁺ and OH⁻; the equilibrium lies to the left.', 'partial reaction [1]; equilibrium to left [1]'),
    ('Explain why farmers should not add calcium hydroxide to soil at the same time as ammonium fertilisers.', 'Calcium hydroxide (a base) reacts with ammonium ions to release ammonia gas, so nitrogen is lost.', 'base reacts with NH₄⁺ [1]; NH₃ lost [1]'),
    ('Explain why the bond angle in NH₄⁺ (109.5°) is larger than in NH₃ (107°).', 'In NH₄⁺ the lone pair has become a bonding pair (dative bond to H⁺), so all four pairs repel equally.', 'lone pair used in bonding [1]; four bonding pairs repel equally [1]'),
])
errs(t12a, [
    ('Nitrogen is unreactive because it is a noble gas.', 'Nitrogen is in Group 15; it is unreactive because of the strong N≡N triple bond.'),
    ('Ammonia acts as a base by donating OH⁻ ions.', 'Ammonia accepts a proton using its lone pair; OH⁻ forms from water.'),
])
c2mix(t12a, ['{p} prepares ammonia in {lab} by heating an ammonium salt with an alkali.', 'A fertiliser company in {c} sells ammonium salts.'])


@t12a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12a_calc(r, D):
    nm, f = r.choice(FERT12)
    M = Mr(f)
    pc = atoms(f)['N'] * 14.0 / M * 100
    if D == 1:
        return nmc(r, f'What is the percentage by mass of nitrogen in {nm}, {F(f)}?', pc, [pc / 2, 14.0 / M * 100, pc * 1.5, 100 - pc], '%', f'{atoms(f)["N"]} × 14.0/{mr1(M)} × 100.')
    if D <= 3:
        return {'stem': f'Calculate the percentage by mass of nitrogen in the fertiliser {nm}, {F(f)}.', 'answer': f'{g3(pc)}%', 'key': f'Mr = {mr1(M)} [1]; {atoms(f)["N"]} × 14.0/{mr1(M)} × 100 = {g3(pc)}% [1]'}
    if 'NH4' not in f:
        return None
    k = 1 if '(' not in f else int(re.search(r'\(NH4\)(\d)', f).group(1))
    mass = r.choice([1.00, 1.20, 1.50, 2.00])
    pur = r.choice([0.82, 0.85, 0.88, 0.9, 0.92, 0.95])
    n_salt = mass * pur / M
    nNH3 = n_salt * k
    vol = 50.0
    cOH = 1.00 if nNH3 < 0.035 else 2.00
    nOH = cOH * vol / 1000
    left = nOH - nNH3
    titre = round(left / 0.500 * 1000, 2)
    if left <= 0 or titre > 50 or titre < 5:
        return None
    left = titre * 0.500 / 1000
    nNH3 = nOH - left
    n_salt = nNH3 / k
    pc = n_salt * M / mass * 100
    return {'stem': f'{mass:.2f} g of an impure fertiliser containing {nm}, {F(f)}, is boiled with {vol:.0f} cm³ of {cOH:.2f} mol dm⁻³ NaOH (an excess) until all the ammonia is driven off. The remaining NaOH needs {titre:.2f} cm³ of 0.500 mol dm⁻³ HCl. Calculate the percentage by mass of {nm} in the fertiliser.',
            'answer': f'{g3(pc)}%', 'key': f'n(NaOH) initially = {g3(nOH)} mol [1]; n(NaOH) left = n(HCl) = {g3(left)} mol [1]; n(NH₄⁺) = n(NaOH) reacted = {g3(nNH3)} mol [1]; n(salt) = {g3(nNH3)}/{k} = {g3(n_salt)} mol, mass = {g3(n_salt * M)} g [1]; % = {g3(pc)}% [1]'}


@t12a.add('C3', (2, 3, 4), 'numerical')
def t12a_gas(r, D):
    nm, f = r.choice(FERT12[:4])
    k = 1 if '(' not in f else int(re.search(r'\(NH4\)(\d)', f).group(1))
    m = r.choice([0.535, 1.07, 1.32, 2.00, 2.64, 0.800])
    n = m / Mr(f)
    v = n * k * 24000
    alk = r.choice(['sodium hydroxide', 'calcium hydroxide'])
    return {'stem': f'{m:.3f} g of {nm}, {F(f)}, is warmed with excess {alk}. Write an ionic equation and calculate the volume of ammonia released at r.t.p., in cm³.',
            'answer': f'NH₄⁺ + OH⁻ → NH₃ + H₂O; {g3(v)} cm³', 'key': f'ionic equation [1]; n(salt) = {m:.3f}/{mr1(Mr(f))} = {g3(n)} mol, n(NH₃) = {g3(n * k)} mol [1]; V = {g3(v)} cm³ [1]'}


def t12a_c4(r, D):
    nm, f = r.choice(FERT12[:4])
    intro = P(r, r.choice([f'{{p}} heats {nm} with calcium hydroxide in {{lab}} to make ammonia.', f'A farmer in {{c}} uses {nm} as a fertiliser.']))
    k = 1 if f in ('NH4NO3', 'NH4Cl') else 2 if f == '(NH4)2SO4' else 3
    anion = {'NH4NO3': 'NO3', 'NH4Cl': 'Cl', '(NH4)2SO4': 'SO4', '(NH4)3PO4': 'PO4'}[f]
    parts = [
        lambda r: ('Explain why nitrogen gas is unreactive.', 'Strong N≡N triple bond (944 kJ mol⁻¹); non-polar.', '[2]'),
        lambda r: ('Write the ionic equation for the reaction of ammonium ions with hydroxide ions.', 'NH₄⁺ + OH⁻ → NH₃ + H₂O', '[1]'),
        lambda r: ('Describe the shapes of NH₃ and NH₄⁺ and explain the difference in bond angle.', 'NH₃ pyramidal 107° (one lone pair); NH₄⁺ tetrahedral 109.5° (no lone pair).', '[3]'),
        lambda r: ('Explain why ammonia is a Brønsted–Lowry base.', 'Lone pair on N accepts a proton.', '[1]'),
        lambda r: (f'Calculate the percentage by mass of nitrogen in {nm}.', f'{g3(atoms(f)["N"] * 14.0 / Mr(f) * 100)}%', '[2]'),
        lambda r: ('Describe a test for the ammonia produced.', 'Damp red litmus paper turns blue.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t12a, t12a_c4)

# ---------------------------------------------------------- 12.2 nitrogen oxides; photochemical smog
t12b = topic('Nitrogen oxides in the atmosphere and catalytic removal; formation of photochemical smog', 'nitrogen oxides in the atmosphere', 'photochemical smog')
t12b.fixed('C1', (1, 2), [
    ('How is nitrogen monoxide formed in a car engine?', 'nitrogen and oxygen from air react at the high temperature of the engine', 'N₂ + O₂ → 2NO (needs high T to break N≡N).', ['by combustion of nitrogen in the fuel only', 'by decomposition of nitric acid', 'from the catalytic converter']),
    ('Which reaction occurs in a catalytic converter?', '2CO + 2NO → 2CO₂ + N₂', 'Pt/Rh catalyst: CO oxidised, NO reduced.', ['N₂ + O₂ → 2NO', 'CO₂ + C → 2CO', '2NO₂ → N₂O₄']),
    ('Which substance is a component of photochemical smog?', 'peroxyacetyl nitrate (PAN)', 'Formed from NO₂, unburnt hydrocarbons and sunlight.', ['carbon dioxide', 'nitrogen', 'argon']),
    ('What conditions are needed for photochemical smog to form?', 'sunlight acting on nitrogen oxides and unburnt hydrocarbons', 'Common in sunny, traffic-heavy cities.', ['cold, dark conditions with no traffic', 'heavy rain and wind', 'high levels of argon']),
    ('What happens to NO when it is released into the air?', 'it is oxidised to NO₂', '2NO + O₂ → 2NO₂ (brown gas).', ['it is reduced to N₂O', 'it reacts with argon', 'it forms ammonia']),
    ('Write an equation for the formation of nitrogen monoxide in a car engine.', 'N₂ + O₂ → 2NO', '[1]'),
])
t12b.fixed('C2', (2, 3, 4), [
    ('Explain why oxides of nitrogen form in car engines but not when the air is at room temperature.', 'The N≡N bond is very strong (high Ea); only at the very high temperatures in the engine do enough collisions have sufficient energy.', 'strong triple bond/high Ea [1]; high temperature in engine [1]'),
    ('Explain how a catalytic converter reduces pollution from nitrogen oxides.', 'NO is reduced to N₂ by reaction with CO (oxidised to CO₂) on the surface of a Pt/Rh catalyst: 2CO + 2NO → 2CO₂ + N₂.', 'NO reduced to N₂, CO oxidised [1]; equation/catalyst [1]'),
    ('Explain why photochemical smog is most serious in sunny cities with heavy traffic.', 'Traffic releases NOx and unburnt hydrocarbons; sunlight breaks down NO₂ starting reactions that form ozone and PAN.', 'NOx and hydrocarbons from traffic [1]; sunlight needed [1]'),
])
errs(t12b, [
    ('Nitrogen oxides in exhaust gases come from nitrogen compounds in the petrol.', 'They come mainly from nitrogen and oxygen in the air reacting at the high engine temperature.'),
    ('A catalytic converter removes nitrogen oxides by oxidising them to nitrogen.', 'NO is reduced to N₂ (oxidation number +2 → 0); CO is oxidised.'),
])
c2mix(t12b, ['A city council in {c} is concerned about air quality from road traffic.', '{p} is researching how catalytic converters work.'])


@t12b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12b_calc(r, D):
    if D == 1:
        sp = r.choice([('NO', '+2'), ('NO₂', '+4'), ('N₂O', '+1'), ('N₂', '0'), ('N₂O₄', '+4'), ('HNO₃', '+5')])
        return mc(r, f'What is the oxidation number of nitrogen in {sp[0]}?', sp[1], ['+1', '+2', '+4', '+5', '0', '−3'], f'N in {sp[0]}: {sp[1]}.')
    mass = r.choice([1.0, 2.0, 3.0, 4.5, 6.0])
    nNO = mass / 30.0
    vN2 = nNO / 2 * 24.0
    mco = nNO * 28.0
    return {'stem': f'A car exhaust contains {mass:.1f} g of nitrogen monoxide per kilometre. In the catalytic converter it reacts: 2CO + 2NO → 2CO₂ + N₂. Calculate the mass of carbon monoxide needed to remove all of the NO and the volume of nitrogen formed at r.t.p. per kilometre. State which species is oxidised.',
            'answer': f'{g3(mco)} g CO; {g3(vN2)} dm³ N₂; CO is oxidised (C +2 → +4)', 'key': f'n(NO) = {mass:.1f}/30.0 = {g3(nNO)} mol [1]; CO 1 : 1 so {g3(mco)} g [1]; n(N₂) = {g3(nNO / 2)} mol, V = {g3(vN2)} dm³ [1]; CO oxidised, NO reduced [1]'}


@t12b.add('C3', (2, 3, 4), 'short')
def t12b_data(r, D):
    peaks = r.choice([(8, 'NO'), (10, 'NO₂'), (14, 'ozone and PAN')])
    city_ = city(r)
    return {'stem': f'Air monitoring in {city_} on a sunny day shows NO peaking at about 08:00, NO₂ peaking at about 10:00 and ozone peaking at about 14:00. Explain the order of these peaks.' + (' Include equations in your answer.' if D >= 4 else ''),
            'answer': 'NO is emitted by morning rush-hour traffic; it is oxidised to NO₂ over the next hours (2NO + O₂ → 2NO₂); NO₂ is photolysed in strong afternoon sunlight (NO₂ → NO + O, O + O₂ → O₃) and reacts with hydrocarbons, so ozone/PAN peak in early afternoon.',
            'key': 'NO from traffic [1]; oxidation to NO₂ [1]; sunlight needed for ozone/PAN formation [1]' + ('; equation(s) [1]' if D >= 4 else '')}


def t12b_c4(r, D):
    intro = P(r, r.choice(['On a sunny afternoon in {c}, the air contains high levels of nitrogen oxides, ozone and PAN.', '{p} is writing a report on how nitrogen oxides from vehicles affect air quality.']))
    parts = [
        lambda r: ('Explain how nitrogen monoxide forms in a petrol engine.', 'High temperature: N₂ + O₂ → 2NO.', '[2]'),
        lambda r: ('Write an equation for the oxidation of NO in air.', '2NO + O₂ → 2NO₂', '[1]'),
        lambda r: ('Describe how photochemical smog forms.', 'NO₂ and unburnt hydrocarbons react in sunlight to form ozone and PAN (peroxyacetyl nitrate).', '[2]'),
        lambda r: ('Write an equation for the removal of NO in a catalytic converter and identify the oxidising agent.', '2CO + 2NO → 2CO₂ + N₂; NO is the oxidising agent.', '[2]'),
        lambda r: ('State one health effect of photochemical smog.', 'Respiratory irritation, eye irritation, asthma.', '[1]'),
        lambda r: ('Explain the role of NO₂ in the formation of acid rain.', 'It catalyses oxidation of SO₂ to SO₃; it also forms nitric acid.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t12b, t12b_c4)

# ---------------------------------------------------------- 12.3 SO2, acid rain, NO2 catalyst
t12c = topic('Sulfur dioxide, acid rain and the role of NO2 as a catalyst in the oxidation of SO2', 'sulfur dioxide, acid rain', 'no2 as a catalyst in the oxidation of so2')
t12c.fixed('C1', (1, 2), [
    ('What is the main source of sulfur dioxide in the atmosphere from human activity?', 'burning fossil fuels containing sulfur compounds', 'e.g. coal-fired power stations.', ['car catalytic converters', 'photosynthesis', 'the Haber process']),
    ('Which equation shows NO₂ acting as a catalyst in the oxidation of SO₂?', 'SO₂ + NO₂ → SO₃ + NO, then NO + ½O₂ → NO₂', 'NO₂ is regenerated: homogeneous catalyst.', ['SO₂ + NO → SO₃ + N', '2SO₂ + O₂ → 2SO₃ only', 'NO₂ + H₂O → HNO₃']),
    ('Which acid is formed when SO₃ dissolves in rainwater?', 'sulfuric acid', 'SO₃ + H₂O → H₂SO₄.', ['sulfurous acid only', 'hydrochloric acid', 'nitric acid']),
    ('Which is an effect of acid rain?', 'damage to limestone buildings', 'CaCO₃ + H₂SO₄ → CaSO₄ + H₂O + CO₂.', ['depletion of the ozone layer', 'increased plant growth in lakes', 'reduced global temperature']),
    ('What type of catalyst is NO₂ in the atmospheric oxidation of SO₂?', 'homogeneous', 'Gas-phase catalyst with gaseous reactants.', ['heterogeneous', 'biological', 'autocatalyst']),
    ('Write an equation for the reaction of sulfur dioxide with water.', 'SO₂ + H₂O → H₂SO₃', '[1]'),
])
t12c.fixed('C2', (2, 3, 4), [
    ('Explain how NO₂ acts as a catalyst for the oxidation of atmospheric SO₂.', 'NO₂ oxidises SO₂ to SO₃ and is reduced to NO; NO is then oxidised back to NO₂ by oxygen, so NO₂ is regenerated.', 'SO₂ + NO₂ → SO₃ + NO [1]; NO + ½O₂ → NO₂ regenerated [1]'),
    ('Explain two environmental effects of acid rain.', 'Lowers pH of lakes, killing fish (and releasing toxic Al³⁺); damages trees by leaching nutrients; corrodes limestone buildings and metal structures.', 'two effects with explanation [2]'),
    ('Explain how flue-gas desulfurisation reduces SO₂ emissions.', 'Waste gases are passed through a slurry of calcium carbonate or calcium oxide, an alkali/base, which reacts with acidic SO₂ to form calcium sulfite/sulfate.', 'base reacts with acidic SO₂ [1]; product named [1]'),
])
errs(t12c, [
    ('NO₂ is used up when it speeds up the oxidation of SO₂.', 'NO₂ is regenerated (NO + ½O₂ → NO₂), so it acts as a catalyst.'),
    ('Acid rain is caused mainly by carbon dioxide.', 'CO₂ makes rain only slightly acidic (pH ~5.6); acid rain is caused by SO₂ and NOx.'),
])
c2mix(t12c, ['A coal-fired power station near {c} releases sulfur dioxide.', '{p} investigates the effect of acid rain on limestone chips in {lab}.'])


@t12c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12c_calc(r, D):
    if D == 1:
        return mc(r, 'What is the role of NO₂ in the reaction sequence SO₂ + NO₂ → SO₃ + NO; NO + ½O₂ → NO₂?', 'catalyst', ['catalyst', 'reactant used up', 'product', 'inhibitor', 'reducing agent only'], 'NO₂ is regenerated.')
    coal = r.choice([100, 500, 1000, 2500])
    pc = r.choice([0.8, 1.2, 1.5, 2.0, 2.5, 3.0])
    mS = coal * pc / 100
    mSO2 = mS / 32.1 * 64.1
    stem = f'A power station in {city(r)} burns {coal} tonnes of coal containing {pc}% sulfur by mass. Calculate the mass of sulfur dioxide produced.'
    key = f'mass S = {g3(mS)} t [1]; S → SO₂: × 64.1/32.1 [1]; = {g3(mSO2)} t [1]'
    ans = f'{g3(mSO2)} tonnes'
    if D >= 4:
        mcc = mS / 32.1 * 100.1
        stem += ' The SO₂ is removed by reaction with calcium carbonate: 2CaCO₃ + 2SO₂ + O₂ → 2CaSO₄ + 2CO₂. Calculate the mass of CaCO₃ needed.'
        key += f'; 1 : 1, mass CaCO₃ = {g3(mcc)} t [1]'
        ans += f'; {g3(mcc)} tonnes CaCO₃'
    return {'stem': stem, 'answer': ans, 'key': key}


@t12c.add('C3', (2, 3, 4, 5), 'short')
def t12c_acid(r, D):
    src = r.choice(['a coal-fired power station', 'a copper smelter', 'an oil refinery', 'a diesel-powered ship', 'a steelworks'])
    tasks = [('write equations to show how NO₂ catalyses the oxidation of SO₂ to SO₃', 'SO₂ + NO₂ → SO₃ + NO; NO + ½O₂ → NO₂', 'SO₂ + NO₂ → SO₃ + NO [1]; NO + ½O₂ → NO₂ (NO₂ regenerated) [1]'),
             ('write an equation for the formation of sulfuric acid in rainwater', 'SO₃ + H₂O → H₂SO₄', 'SO₃ + H₂O → H₂SO₄ [1]'),
             ('write an equation for the reaction of SO₂ with water', 'SO₂ + H₂O → H₂SO₃', 'SO₂ + H₂O → H₂SO₃ [1]'),
             ('explain why NO₂ is described as a catalyst in this process', 'it is used in the first step and regenerated in the second, so it is not used up overall', 'used then regenerated [1]; not consumed overall [1]'),
             ('describe one effect of acid rain on buildings or lakes, with an equation where possible', 'limestone/marble is eroded: CaCO₃ + H₂SO₄ → CaSO₄ + CO₂ + H₂O; lakes become acidic, harming fish', 'effect described [1]; CaCO₃ + H₂SO₄ → CaSO₄ + CO₂ + H₂O [1]'),
             ('state the oxidation number of sulfur in SO₂, SO₃ and H₂SO₄', '+4, +6, +6', 'SO₂ +4 [1]; SO₃ and H₂SO₄ +6 [1]')]
    k = 2 if D <= 3 else 3
    pick = r.sample(tasks, k)
    stem = f'{person(r)} is studying acid rain caused by emissions from {src} near {city(r)}. ' + cap('; '.join(p[0] for p in pick)) + '.'
    return {'stem': stem, 'answer': '; '.join(p[1] for p in pick), 'key': '; '.join(p[2] for p in pick)}


def t12c_c4(r, D):
    intro = P(r, r.choice(['Rain falling near an industrial city in {c} has a pH of 4.2.', '{p} studies how SO₂ and NO₂ from a power station form acid rain.']))
    parts = [
        lambda r: ('Write equations for the formation of SO₂ from burning sulfur impurities and its oxidation to SO₃ catalysed by NO₂.', 'S + O₂ → SO₂; SO₂ + NO₂ → SO₃ + NO; NO + ½O₂ → NO₂', '[3]'),
        lambda r: ('Explain why NO₂ is described as a catalyst.', 'It is regenerated at the end of the cycle.', '[1]'),
        lambda r: ('Write an equation for the formation of sulfuric acid in rain.', 'SO₃ + H₂O → H₂SO₄', '[1]'),
        lambda r: ('Describe two effects of acid rain.', 'Damage to buildings (limestone), death of fish in lakes, damage to forests, corrosion of metals.', '[2]'),
        lambda r: ('Suggest one way to reduce SO₂ emissions.', 'Remove sulfur from fuels; flue-gas desulfurisation with CaCO₃/CaO.', '[1]'),
        lambda r: ('Explain why rain is slightly acidic even in unpolluted air.', 'Dissolved CO₂ forms carbonic acid (pH about 5.6).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t12c, t12c_c4)

CHAPTERS[12] = [t12a, t12b, t12c]


# ===================================================================== organic data
ORG = {  # name: (structural formula, homologous series / class)
    'methane': ('CH4', 'alkane'), 'ethane': ('CH3CH3', 'alkane'), 'propane': ('CH3CH2CH3', 'alkane'), 'butane': ('CH3CH2CH2CH3', 'alkane'), '2-methylpropane': ('CH3CH(CH3)CH3', 'alkane'),
    'pentane': ('CH3CH2CH2CH2CH3', 'alkane'), '2-methylbutane': ('CH3CH(CH3)CH2CH3', 'alkane'), '2,2-dimethylpropane': ('C(CH3)4', 'alkane'), 'hexane': ('CH3(CH2)4CH3', 'alkane'),
    'ethene': ('CH2=CH2', 'alkene'), 'propene': ('CH2=CHCH3', 'alkene'), 'but-1-ene': ('CH2=CHCH2CH3', 'alkene'), 'but-2-ene': ('CH3CH=CHCH3', 'alkene'), '2-methylpropene': ('CH2=C(CH3)2', 'alkene'),
    'pent-2-ene': ('CH3CH=CHCH2CH3', 'alkene'), '2-methylbut-2-ene': ('(CH3)2C=CHCH3', 'alkene'),
    'chloromethane': ('CH3Cl', 'halogenoalkane'), 'bromoethane': ('CH3CH2Br', 'halogenoalkane'), '1-chloropropane': ('CH3CH2CH2Cl', 'halogenoalkane'), '2-bromopropane': ('CH3CHBrCH3', 'halogenoalkane'),
    '1-bromobutane': ('CH3CH2CH2CH2Br', 'halogenoalkane'), '2-bromobutane': ('CH3CHBrCH2CH3', 'halogenoalkane'), '2-bromo-2-methylpropane': ('(CH3)3CBr', 'halogenoalkane'), '1,2-dibromoethane': ('CH2BrCH2Br', 'halogenoalkane'),
    'methanol': ('CH3OH', 'alcohol'), 'ethanol': ('CH3CH2OH', 'alcohol'), 'propan-1-ol': ('CH3CH2CH2OH', 'alcohol'), 'propan-2-ol': ('CH3CH(OH)CH3', 'alcohol'), 'butan-1-ol': ('CH3CH2CH2CH2OH', 'alcohol'),
    'butan-2-ol': ('CH3CH(OH)CH2CH3', 'alcohol'), '2-methylpropan-2-ol': ('(CH3)3COH', 'alcohol'), '2-methylpropan-1-ol': ('(CH3)2CHCH2OH', 'alcohol'), 'ethane-1,2-diol': ('HOCH2CH2OH', 'alcohol (diol)'),
    'methanal': ('HCHO', 'aldehyde'), 'ethanal': ('CH3CHO', 'aldehyde'), 'propanal': ('CH3CH2CHO', 'aldehyde'), 'butanal': ('CH3CH2CH2CHO', 'aldehyde'), '2-methylpropanal': ('(CH3)2CHCHO', 'aldehyde'),
    'propanone': ('CH3COCH3', 'ketone'), 'butanone': ('CH3COCH2CH3', 'ketone'), 'pentan-2-one': ('CH3COCH2CH2CH3', 'ketone'), 'pentan-3-one': ('CH3CH2COCH2CH3', 'ketone'),
    'methanoic acid': ('HCOOH', 'carboxylic acid'), 'ethanoic acid': ('CH3COOH', 'carboxylic acid'), 'propanoic acid': ('CH3CH2COOH', 'carboxylic acid'), 'butanoic acid': ('CH3CH2CH2COOH', 'carboxylic acid'),
    '2-methylpropanoic acid': ('(CH3)2CHCOOH', 'carboxylic acid'),
    'methyl ethanoate': ('CH3COOCH3', 'ester'), 'ethyl ethanoate': ('CH3COOCH2CH3', 'ester'), 'ethyl methanoate': ('HCOOCH2CH3', 'ester'), 'methyl propanoate': ('CH3CH2COOCH3', 'ester'), 'propyl ethanoate': ('CH3COOCH2CH2CH3', 'ester'),
    'ethanenitrile': ('CH3CN', 'nitrile'), 'propanenitrile': ('CH3CH2CN', 'nitrile'), 'butanenitrile': ('CH3CH2CH2CN', 'nitrile'),
    'methylamine': ('CH3NH2', 'amine'), 'ethylamine': ('CH3CH2NH2', 'amine'), 'propylamine': ('CH3CH2CH2NH2', 'amine'),
    '2-hydroxypropanenitrile': ('CH3CH(OH)CN', 'hydroxynitrile'), '2-hydroxy-2-methylpropanenitrile': ('(CH3)2C(OH)CN', 'hydroxynitrile'),
}
GROUPS = {'alkane': 'none (C–C and C–H only)', 'alkene': 'C=C', 'halogenoalkane': 'C–X (X = Cl, Br, I)', 'alcohol': '–OH (hydroxyl)', 'alcohol (diol)': 'two –OH groups', 'aldehyde': '–CHO',
          'ketone': 'C=O within the chain (>C=O)', 'carboxylic acid': '–COOH', 'ester': '–COO– (ester link)', 'nitrile': '–C≡N', 'amine': '–NH₂', 'hydroxynitrile': '–OH and –C≡N'}
GENF = {'alkane': 'CₙH₂ₙ₊₂', 'alkene': 'CₙH₂ₙ', 'alcohol': 'CₙH₂ₙ₊₁OH', 'aldehyde': 'CₙH₂ₙO', 'ketone': 'CₙH₂ₙO', 'carboxylic acid': 'CₙH₂ₙ₊₁COOH', 'halogenoalkane': 'CₙH₂ₙ₊₁X', 'ester': 'CₙH₂ₙO₂'}


def SF(s):
    """Structural formula display: CH3CH(OH)CH3 -> CH₃CH(OH)CH₃, '=' kept, '≡' kept."""
    return F(s)


def MF(name):
    a = atoms(ORG[name][0].replace('=', '').replace('≡', ''))
    return fstr(a)


t13a = topic('Formulae, functional groups and IUPAC nomenclature', 'formulae, functional groups and iupac nomenclature', 'functional groups')
t13a.fixed('C1', (1, 2), [
    ('What is meant by a homologous series?', 'a family of compounds with the same functional group and general formula, each member differing by CH₂', 'Similar chemical properties; gradual change in physical properties.', ['compounds with the same molecular formula', 'compounds containing only carbon and hydrogen', 'compounds with the same boiling point']),
    ('What is the general formula of the alkenes?', 'CₙH₂ₙ', 'Alkenes (one C=C): CₙH₂ₙ; alkanes CₙH₂ₙ₊₂.', ['CₙH₂ₙ₊₂', 'CₙH₂ₙ₋₂', 'CₙH₂ₙ₊₁OH']),
    ('What is the functional group of a ketone?', 'a C=O group bonded to two carbon atoms', 'Ketone >C=O within the chain; aldehyde –CHO at the end.', ['–CHO', '–COOH', '–OH']),
    ('What is a skeletal formula?', 'a simplified formula showing the carbon skeleton as lines, with functional groups shown', 'Each line end/junction is a C; H atoms on C not shown.', ['a formula showing every atom and bond', 'the simplest ratio of atoms', 'a formula showing only the functional group']),
    ('Which is the structural formula of propan-2-ol?', 'CH₃CH(OH)CH₃', 'OH on carbon 2 of a 3-carbon chain.', ['CH₃CH₂CH₂OH', 'CH₃COCH₃', 'CH₃CH₂CHO']),
    ('Give the molecular formula of butane.', 'C₄H₁₀', '[1]'),
])
t13a.fixed('C2', (2, 3, 4), [
    ('Explain why members of a homologous series have similar chemical properties.', 'They contain the same functional group, which determines how the molecules react.', 'same functional group [1]; functional group determines reactions [1]'),
    ('Explain why the boiling points of the alkanes increase with chain length.', 'Longer molecules have more electrons and larger surface area, so stronger instantaneous dipole–induced dipole forces.', 'more electrons/surface contact [1]; stronger London forces [1]'),
    ('Explain the difference between a displayed formula and a structural formula.', 'A displayed formula shows every atom and every bond; a structural formula shows the arrangement of atoms in each carbon unit without showing all bonds (e.g. CH₃CH₂OH).', 'displayed shows all bonds [1]; structural shows groupings without bonds [1]'),
])
errs(t13a, [
    ('CH₃CH₂CH₂OH is named propan-2-ol.', 'The OH is on carbon 1, so it is propan-1-ol; propan-2-ol is CH₃CH(OH)CH₃.'),
    ('Propanone and propanal have the same functional group.', 'Propanone is a ketone (>C=O in the chain); propanal is an aldehyde (–CHO).'),
    ('The longest chain in CH₃CH(CH₃)CH₃ has three carbons, so it is propane.', 'The longest chain is three carbons, but there is also a methyl branch on C2, so the compound has 4 carbons: 2-methylpropane (C₄H₁₀).'),
])
c2mix(t13a, ['{p} is naming organic compounds found in a fragrance laboratory in {c}.', 'A student in {c} is revising organic formulae and nomenclature.'])


@t13a.add('C1', (1, 2, 3))
def t13a_name(r, D):
    nm = r.choice(list(ORG))
    sfm, cls = ORG[nm]
    same = [k for k, v in ORG.items() if v[1] == cls and k != nm]
    if len(same) < 3:
        same += r.sample([k for k in ORG if k != nm], 3)
    if r.random() < 0.5:
        return mc(r, f'What is the IUPAC name of {SF(sfm)}?', nm, same, f'{SF(sfm)}: {nm} ({cls}).')
    return mc(r, f'To which homologous series does {SF(sfm)} belong?', cls, list(GROUPS), f'{SF(sfm)} ({nm}) contains {GROUPS[cls]}: {cls}.')


@t13a.add('C3', (1, 2, 3, 4), 'short')
def t13a_formulae(r, D):
    nm = r.choice(list(ORG))
    sfm, cls = ORG[nm]
    mf = MF(nm)
    e, g = empirical(mf)
    if D == 1:
        return mc(r, f'What is the molecular formula of {nm}?', F(mf), [F(MF(x)) for x in r.sample([k for k in ORG if MF(k) != mf], 5)], f'{SF(sfm)} = {F(mf)}.')
    stem = f'For {nm}, give (a) the structural formula, (b) the molecular formula and (c) the empirical formula.'
    key = f'(a) {SF(sfm)} [1]; (b) {F(mf)} [1]; (c) {F(fstr(e))} [1]'
    ans = f'(a) {SF(sfm)} (b) {F(mf)} (c) {F(fstr(e))}'
    if D >= 4:
        stem += ' Name the homologous series and identify the functional group.'
        key += f'; {cls}, {GROUPS[cls]} [1]'
        ans += f'; {cls}: {GROUPS[cls]}'
    return {'stem': stem, 'answer': ans, 'key': key}


@t13a.add('C2', (2, 3, 4), 'explain')
def t13a_bp(r, D):
    ser = r.choice([['methane', 'ethane', 'propane', 'butane', 'pentane', 'hexane'], ['methanol', 'ethanol', 'propan-1-ol', 'butan-1-ol'], ['methanoic acid', 'ethanoic acid', 'propanoic acid', 'butanoic acid'], ['ethanal', 'propanal', 'butanal']])
    a, b = sorted(r.sample(ser, 2), key=ser.index)
    return {'stem': f'{a.capitalize()} and {b} are members of the same homologous series. State and explain which has the higher boiling point.',
            'answer': f'{b.capitalize()}: longer chain with more electrons, so stronger instantaneous dipole–induced dipole forces between molecules (other intermolecular forces similar).', 'key': f'{b} [1]; more electrons/larger surface area → stronger London forces [1]' + ('; same functional group so other forces similar [1]' if D >= 4 else '')}


def t13a_c4(r, D):
    pick = r.sample(list(ORG), 3)
    intro = P(r, r.choice([f'{{p}} is given three compounds in {{lab}}: ' + ', '.join(SF(ORG[x][0]) for x in pick) + '.', f'A perfume chemist in {{c}} analyses three compounds: ' + ', '.join(SF(ORG[x][0]) for x in pick) + '.']))
    parts = [lambda r, x=x, i=i: (f'Name compound {"ABC"[i]} ({SF(ORG[x][0])}) and identify its homologous series.', f'{x}; {ORG[x][1]}', '[2]') for i, x in enumerate(pick)] + [
        lambda r: ('Give the molecular formula of each compound.', '; '.join(F(MF(x)) for x in pick), '[2]'),
        lambda r: ('Define the term functional group.', 'An atom or group of atoms responsible for the characteristic reactions of a compound.', '[1]'),
        lambda r: ('Draw the displayed formula of the first compound.', f'All atoms and bonds of {SF(ORG[pick[0]][0])} shown.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t13a, t13a_c4)

# ---------------------------------------------------------- 13.2 reaction types and mechanisms
RTYPES = [('CH₂=CH₂ + Br₂ → CH₂BrCH₂Br', 'addition'), ('CH₄ + Cl₂ → CH₃Cl + HCl', 'substitution'), ('CH₃CH₂Br + NaOH → CH₃CH₂OH + NaBr', 'substitution'),
          ('CH₃CH₂OH → CH₂=CH₂ + H₂O', 'elimination'), ('CH₃CH₂Br + NaOH (ethanol) → CH₂=CH₂ + NaBr + H₂O', 'elimination'), ('CH₃COOCH₂CH₃ + H₂O → CH₃COOH + CH₃CH₂OH', 'hydrolysis'),
          ('CH₃COOH + CH₃OH → CH₃COOCH₃ + H₂O', 'condensation (esterification)'), ('CH₃CH₂OH + [O] → CH₃CHO + H₂O', 'oxidation'), ('CH₃COCH₃ + 2[H] → CH₃CH(OH)CH₃', 'reduction'),
          ('CH₂=CHCH₃ + H₂O → CH₃CH(OH)CH₃', 'addition'), ('CH₃CHO + HCN → CH₃CH(OH)CN', 'addition'), ('CH₃CH₂CN + 2H₂O + H⁺ → CH₃CH₂COOH + NH₄⁺', 'hydrolysis'),
          ('C₂H₆ + Br₂ → C₂H₅Br + HBr', 'substitution'), ('CH₃CH₂CH₂OH + 2[O] → CH₃CH₂COOH + H₂O', 'oxidation'), ('CH₂=CH₂ + H₂ → CH₃CH₃', 'addition (reduction)')]
SPECIES = [('OH⁻', 'nucleophile'), ('CN⁻', 'nucleophile'), ('NH₃', 'nucleophile'), ('H₂O', 'nucleophile'), ('Br⁻', 'nucleophile'), ('H⁺', 'electrophile'), ('NO₂⁺', 'electrophile'),
           ('Br₂ (polarised by the C=C)', 'electrophile'), ('the H atom of HBr', 'electrophile'), ('a carbocation CH₃CH⁺CH₃', 'electrophile'), ('Cl•', 'free radical'), ('•CH₃', 'free radical'), ('Br•', 'free radical')]

t13b = topic('Types of reaction and mechanisms: homolytic and heterolytic fission, free radicals, nucleophiles and electrophiles', 'types of reaction and mechanisms', 'homolytic and heterolytic fission')
t13b.fixed('C1', (1, 2), [
    ('What is homolytic fission?', 'breaking a covalent bond so that each atom takes one electron, forming two free radicals', 'e.g. Cl₂ → 2Cl• in UV light.', ['breaking a bond so that one atom takes both electrons', 'forming a bond using a lone pair', 'breaking an ionic bond']),
    ('What is heterolytic fission?', 'breaking a covalent bond so that one atom takes both bonding electrons, forming ions', 'e.g. C–Br → C⁺ + Br⁻.', ['each atom takes one electron', 'two radicals combine', 'a π bond forms']),
    ('What is a nucleophile?', 'an electron-pair donor that attacks an electron-deficient carbon atom', 'e.g. OH⁻, CN⁻, NH₃, H₂O.', ['an electron-pair acceptor', 'a species with an unpaired electron', 'a positive ion that attacks a C=C bond']),
    ('What is an electrophile?', 'an electron-pair acceptor that attacks a region of high electron density', 'e.g. H⁺, Br⁺ (polarised Br₂), carbocations.', ['an electron-pair donor', 'a species with an unpaired electron', 'a negatively charged ion']),
    ('What does a curly arrow show in a reaction mechanism?', 'the movement of a pair of electrons', 'A half-headed (fish-hook) arrow shows one electron.', ['the movement of an atom', 'the direction of heat flow', 'the movement of a proton']),
    ('Name the type of fission that produces free radicals.', 'Homolytic fission.', '[1]'),
])
t13b.fixed('C2', (2, 3, 4), [
    ('Explain why OH⁻ ions attack the carbon atom of the C–Br bond in bromoethane.', 'Br is more electronegative so C is δ+; OH⁻ is a nucleophile that donates a lone pair to the electron-deficient carbon.', 'C δ+ [1]; OH⁻ donates lone pair (nucleophile) [1]'),
    ('Explain why alkenes react with electrophiles rather than nucleophiles.', 'The C=C π bond is a region of high electron density that attracts electron-pair acceptors (electrophiles) and repels nucleophiles.', 'high electron density in π bond [1]; attracts electrophiles [1]'),
    ('Explain why UV light is needed for the reaction of methane with chlorine.', 'UV provides energy for homolytic fission of the Cl–Cl bond to form chlorine radicals that start the chain reaction.', 'homolytic fission of Cl₂ [1]; radicals initiate chain [1]'),
])
errs(t13b, [
    ('A nucleophile is attracted to regions of high electron density.', 'Nucleophiles are electron-pair donors attracted to electron-deficient (δ+) atoms; electrophiles seek high electron density.'),
    ('In homolytic fission the more electronegative atom takes both electrons.', 'That is heterolytic fission; in homolytic fission each atom takes one electron.'),
])
c2mix(t13b, ['{p} is classifying organic reactions and reagents for an AS assignment.', 'A student in {c} is learning to draw curly-arrow mechanisms.'])


@t13b.add('C1', (1, 2, 3))
def t13b_type(r, D):
    eq, ty = r.choice(RTYPES)
    if r.random() < 0.5:
        return mc(r, f'What type of reaction is {eq}?', ty, list({x[1] for x in RTYPES}), f'{eq}: {ty}.')
    sp, k = r.choice(SPECIES)
    return mc(r, f'How is {sp} best classified in organic mechanisms?', k, ['nucleophile', 'electrophile', 'free radical', 'catalyst'], f'{sp}: {k}.')


@t13b.add('C3', (2, 3, 4), 'short')
def t13b_class(r, D):
    pick = r.sample(SPECIES, 3 if D <= 3 else 4)
    return {'stem': 'Classify each of the following as a nucleophile, an electrophile or a free radical, giving a reason in each case: ' + '; '.join(p[0] for p in pick) + '.',
            'answer': '; '.join(f'{p[0]}: {p[1]}' for p in pick), 'key': ' '.join(f'{p[0]} {p[1]} with reason (lone pair donor / electron-pair acceptor / unpaired electron) [1]' for p in pick)}


@t13b.add('C2', (2, 3, 4), 'explain')
def t13b_fission(r, D):
    b = r.choice([('Cl–Cl in UV light', 'homolytic', 'two Cl• radicals'), ('Br–Br in UV light', 'homolytic', 'two Br• radicals'), ('C–Br in 2-bromo-2-methylpropane in water', 'heterolytic', '(CH₃)₃C⁺ and Br⁻'),
                  ('H–Br as it adds to ethene', 'heterolytic', 'H⁺ (adds to C=C) and Br⁻'), ('C–H in methane attacked by Cl•', 'homolytic', '•CH₃ radical (and HCl)'), ('Br–Br as it approaches the C=C bond in ethene', 'heterolytic', 'Br⁺ (adds) and Br⁻')])
    return {'stem': f'State the type of bond fission that occurs for {b[0]}, name the species formed and explain your answer.', 'answer': f'{cap(b[1])} fission: {b[2]}.',
            'key': f'{b[1]} [1]; species formed [1]' + ('; each atom takes one electron / one atom takes both electrons [1]' if D >= 3 else '')}


def t13b_c4(r, D):
    intro = P(r, r.choice(['{p} compares the mechanisms of three reactions: methane with chlorine in UV light, ethene with bromine, and bromoethane with hot aqueous sodium hydroxide.', 'In {lab}, students study free-radical substitution, electrophilic addition and nucleophilic substitution.']))
    parts = [
        lambda r: ('Define homolytic and heterolytic fission.', 'Homolytic: each atom takes one electron (radicals); heterolytic: one atom takes both (ions).', '[2]'),
        lambda r: ('Name the mechanism of each reaction.', 'free-radical substitution; electrophilic addition; nucleophilic substitution', '[3]'),
        lambda r: ('Identify the attacking species in the reaction of bromoethane with OH⁻ and explain why it attacks carbon.', 'OH⁻ nucleophile; C δ+ because Br more electronegative.', '[2]'),
        lambda r: ('Explain how Br₂ acts as an electrophile even though it is non-polar.', 'High electron density of C=C induces a dipole in Br₂; δ+ Br accepts electrons.', '[2]'),
        lambda r: ('State what is shown by a curly arrow.', 'Movement of a pair of electrons.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t13b, t13b_c4)

# ---------------------------------------------------------- 13.3 shapes of organic molecules
ANG = [('the carbon atoms in ethane', '109.5°', 'tetrahedral', 'sp³'), ('the carbon atoms in ethene', '120°', 'trigonal planar', 'sp²'), ('the carbon atoms in ethyne', '180°', 'linear', 'sp'),
       ('the carbonyl carbon in ethanal', '120°', 'trigonal planar', 'sp²'), ('the CH₃ carbon in ethanal', '109.5°', 'tetrahedral', 'sp³'), ('the C≡N carbon in propanenitrile', '180°', 'linear', 'sp'),
       ('the oxygen atom in ethanol (C–O–H)', 'about 104.5°', 'non-linear (bent)', 'sp³-like, two lone pairs'), ('the nitrogen atom in methylamine', 'about 107°', 'pyramidal', 'sp³-like, one lone pair'),
       ('the carbon of the COOH group in ethanoic acid', '120°', 'trigonal planar', 'sp²'), ('each carbon atom in cyclohexane', '109.5°', 'tetrahedral', 'sp³'), ('carbon 2 of propene', '120°', 'trigonal planar', 'sp²')]

t13c = topic('Shapes of organic molecules: σ and π bonds', 'shapes of organic molecules', 'σ and π bonds')
t13c.fixed('C1', (1, 2), [
    ('What is the H–C–H bond angle in methane?', '109.5°', 'Four bonding pairs around C: tetrahedral.', ['120°', '90°', '107°']),
    ('Why is the ethene molecule planar?', 'the π bond requires the p orbitals on both carbons to be parallel, keeping all atoms in one plane', 'sp² carbons with π overlap.', ['the carbon atoms are sp³ hybridised', 'there are no lone pairs', 'C=C bonds are very long']),
    ('How many σ bonds are there in a propene molecule, CH₂=CHCH₃?', '8', '2 C–C σ + 6 C–H σ = 8; plus 1 π.', ['9', '7', '6']),
    ('Which statement explains why a C=C double bond is shorter than a C–C single bond?', 'there is greater electron density between the nuclei', 'σ + π: four shared electrons.', ['the π bond is weaker', 'carbon atoms are smaller in alkenes', 'there are lone pairs on carbon']),
    ('What shape is the arrangement of bonds around a carbon atom with four single bonds?', 'tetrahedral', 'sp³: 109.5°.', ['trigonal planar', 'linear', 'square planar']),
    ('State the bond angle around each carbon atom in ethene.', '120°', '[1]'),
])
t13c.fixed('C2', (2, 3, 4), [
    ('Explain why cis- and trans- isomers of but-2-ene cannot interconvert at room temperature.', 'Rotation about the C=C bond would require breaking the π bond (sideways p-orbital overlap), which needs a lot of energy.', 'π bond restricts rotation [1]; breaking it needs much energy [1]'),
    ('Explain why the carbon chain of butane is described as zig-zag rather than straight.', 'Each carbon is tetrahedral (109.5°), so successive C–C bonds are angled.', 'tetrahedral carbons [1]; 109.5° gives zig-zag [1]'),
])
errs(t13c, [
    ('In propene all the carbon atoms are trigonal planar.', 'Only the two C=C carbons are trigonal planar (sp², 120°); the CH₃ carbon is tetrahedral (109.5°).'),
    ('A π bond is formed by head-on overlap of p orbitals along the C–C axis.', 'A π bond forms by sideways overlap of p orbitals above and below the axis.'),
])
c2mix(t13c, ['{p} builds molecular models of simple organic molecules.', 'A student in {c} predicts bond angles in organic molecules.'])


@t13c.add('C1', (1, 2, 3))
def t13c_ang(r, D):
    what, ang, shape, hyb = r.choice(ANG)
    if r.random() < 0.5:
        return mc(r, f'What is the bond angle around {what}?', ang, ['109.5°', '120°', '180°', 'about 104.5°', 'about 107°', '90°'], f'{what}: {shape}, {ang}.')
    return mc(r, f'What is the arrangement of bonds around {what}?', shape, ['tetrahedral', 'trigonal planar', 'linear', 'non-linear (bent)', 'pyramidal', 'octahedral'], f'{shape} ({ang}).')


@t13c.add('C3', (2, 3, 4, 5), 'short')
def t13c_mol(r, D):
    nm, f, s, p, h = r.choice(SIGPI)
    if 'C' not in f:
        return None
    stem = f'For a molecule of {nm}, {F(f)}, state the number of σ and π bonds and the bond angles around each type of carbon atom. Explain whether all the atoms lie in one plane.'
    angs = ', '.join(f'{k} carbon {HYB[k][1]}' for k in ('sp³', 'sp²', 'sp') if re.search(re.escape(k) + r'(?![²³])', h))
    pi_ = D >= 4 and p > 0
    if pi_:
        stem += ' Describe how a π bond is formed.'
    planar = nm in ('ethene', 'ethyne', 'carbon dioxide', 'hydrogen cyanide', 'methanal', 'buta-1,3-diene', 'nitrogen', 'chloroethene')
    return {'stem': stem, 'answer': f'{s} σ, {p} π; {h}: {angs}; ' + ('all atoms coplanar' if planar else 'not all atoms in one plane (sp³ carbon(s) present)') + ('; π bond: sideways overlap of p orbitals, electron density above and below the bond axis' if pi_ else ''),
            'key': f'σ = {s} and π = {p} [1]; angles {angs} [1]; planarity explained [1]' + ('; π bond formed by sideways overlap of p orbitals [1]' if pi_ else '')}


def t13c_c4(r, D):
    nm, f, s, p, h = r.choice([x for x in SIGPI if x[3] and 'C' in x[1]])
    intro = P(r, r.choice([f'{{p}} studies the bonding in {nm}, {F(f)}.', f'A computational chemist in {{c}} models the shape of {nm}, {F(f)}.']))
    parts = [
        lambda r: ('State the number of σ and π bonds.', f'{s} σ and {p} π', '[2]'),
        lambda r: ('Describe how the π bond is formed.', 'Sideways overlap of p orbitals on adjacent atoms, electron density above and below the bond axis.', '[2]'),
        lambda r: ('State the hybridisation and bond angles around each carbon atom.', f'{h}: ' + ', '.join(f'{k} {HYB[k][1]}' for k in ('sp³', 'sp²', 'sp') if re.search(re.escape(k) + r'(?![²³])', h)), '[2]'),
        lambda r: ('Explain why there is restricted rotation about the double bond.', 'Rotation would break the π overlap.', '[1]'),
        lambda r: ('Explain why the double bond is a site of electrophilic attack.', 'High electron density of π electrons exposed.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t13c, t13c_c4)

# ---------------------------------------------------------- 13.4 isomerism
STEREO = [  # name, structural formula, cis/trans?, chiral?
    ('but-2-ene', 'CH₃CH=CHCH₃', True, False), ('but-1-ene', 'CH₂=CHCH₂CH₃', False, False), ('pent-2-ene', 'CH₃CH=CHCH₂CH₃', True, False), ('2-methylbut-2-ene', '(CH₃)₂C=CHCH₃', False, False),
    ('1,2-dichloroethene', 'CHCl=CHCl', True, False), ('1,1-dichloroethene', 'CH₂=CCl₂', False, False), ('butan-2-ol', 'CH₃CH(OH)CH₂CH₃', False, True), ('2-bromobutane', 'CH₃CHBrCH₂CH₃', False, True),
    ('2-hydroxypropanoic acid', 'CH₃CH(OH)COOH', False, True), ('propan-2-ol', 'CH₃CH(OH)CH₃', False, False), ('2-aminopropanoic acid', 'CH₃CH(NH₂)COOH', False, True),
    ('2-methylbutan-1-ol', 'CH₃CH₂CH(CH₃)CH₂OH', False, True), ('1-chlorobutane', 'CH₃CH₂CH₂CH₂Cl', False, False), ('2-hydroxypropanenitrile', 'CH₃CH(OH)CN', False, True),
    ('2-hydroxy-2-methylpropanenitrile', '(CH₃)₂C(OH)CN', False, False), ('butanone', 'CH₃COCH₂CH₃', False, False), ('3-methylhexane', 'CH₃CH₂CH(CH₃)CH₂CH₂CH₃', False, True),
    ('but-2-enoic acid', 'CH₃CH=CHCOOH', True, False), ('1-bromo-2-chloroethene', 'CHBr=CHCl', True, False), ('3-chlorobut-1-ene', 'CH₂=CHCHClCH₃', False, True),
    ('pent-3-en-2-ol', 'CH₃CH=CHCH(OH)CH₃', True, True), ('2-chloropropane', 'CH₃CHClCH₃', False, False),
]
NISO = [('C₄H₁₀', 'alkanes', 2, 'butane, 2-methylpropane'), ('C₅H₁₂', 'alkanes', 3, 'pentane, 2-methylbutane, 2,2-dimethylpropane'),
        ('C₆H₁₄', 'alkanes', 5, 'hexane, 2-methylpentane, 3-methylpentane, 2,2-dimethylbutane, 2,3-dimethylbutane'), ('C₃H₇Cl', 'halogenoalkanes', 2, '1-chloropropane, 2-chloropropane'),
        ('C₄H₉Br', 'halogenoalkanes', 4, '1-bromobutane, 2-bromobutane, 1-bromo-2-methylpropane, 2-bromo-2-methylpropane'), ('C₄H₁₀O', 'alcohols', 4, 'butan-1-ol, butan-2-ol, 2-methylpropan-1-ol, 2-methylpropan-2-ol'),
        ('C₄H₈', 'alkenes (structural only)', 3, 'but-1-ene, but-2-ene, 2-methylpropene'), ('C₅H₁₀O', 'aldehydes and ketones', 7, 'pentanal, 2-methylbutanal, 3-methylbutanal, 2,2-dimethylpropanal, pentan-2-one, pentan-3-one, 3-methylbutan-2-one'),
        ('C₄H₈O₂', 'esters', 4, 'methyl propanoate, ethyl ethanoate, propyl methanoate, 1-methylethyl methanoate'), ('C₄H₈O₂', 'carboxylic acids', 2, 'butanoic acid, 2-methylpropanoic acid'),
        ('C₃H₈O', 'alcohols and ethers', 3, 'propan-1-ol, propan-2-ol, methoxyethane'), ('C₄H₈O', 'aldehydes and ketones', 3, 'butanal, 2-methylpropanal, butanone')]
FGI = [('propanal', 'propanone', 'C₃H₆O', 'aldehyde vs ketone'), ('ethanoic acid', 'methyl methanoate', 'C₂H₄O₂', 'carboxylic acid vs ester'), ('propanoic acid', 'methyl ethanoate', 'C₃H₆O₂', 'carboxylic acid vs ester'),
       ('ethanol', 'methoxymethane', 'C₂H₆O', 'alcohol vs ether'), ('butanoic acid', 'ethyl ethanoate', 'C₄H₈O₂', 'carboxylic acid vs ester'), ('butanal', 'butanone', 'C₄H₈O', 'aldehyde vs ketone'),
       ('propene', 'cyclopropane', 'C₃H₆', 'alkene vs cycloalkane')]

NISO_ST = {('C₄H₉Br', 'halogenoalkanes'): '2-bromobutane is chiral (optical isomers)', ('C₄H₁₀O', 'alcohols'): 'butan-2-ol is chiral (optical isomers)',
           ('C₄H₈', 'alkenes (structural only)'): 'but-2-ene shows cis/trans isomerism', ('C₅H₁₀O', 'aldehydes and ketones'): '2-methylbutanal is chiral (optical isomers)'}
FGI_TEST = {('propanal', 'propanone'): "Warm with Tollens' reagent: propanal gives a silver mirror; propanone does not.",
            ('ethanoic acid', 'methyl methanoate'): 'Add sodium carbonate solution: ethanoic acid effervesces (CO₂); the ester does not.',
            ('propanoic acid', 'methyl ethanoate'): 'Add sodium carbonate solution: propanoic acid effervesces (CO₂); the ester does not.',
            ('ethanol', 'methoxymethane'): 'Warm with acidified K₂Cr₂O₇: ethanol turns it from orange to green; methoxymethane does not (or Na: H₂ with ethanol only).',
            ('butanoic acid', 'ethyl ethanoate'): 'Add sodium carbonate solution: butanoic acid effervesces (CO₂); the ester does not.',
            ('butanal', 'butanone'): "Warm with Fehling's solution: butanal gives a brick-red precipitate; butanone stays blue.",
            ('propene', 'cyclopropane'): 'Shake with bromine water: propene decolourises it (orange to colourless); cyclopropane does not react at room temperature in the dark.'}

t13d = topic('Structural and stereoisomerism: geometrical (cis/trans) and optical isomerism, chiral centres', 'structural and stereoisomerism', 'chiral centres')
t13d.fixed('C1', (1, 2), [
    ('What are structural isomers?', 'compounds with the same molecular formula but different structural formulae', 'Chain, positional or functional-group isomers.', ['compounds with the same structural formula but different arrangements in space', 'compounds with different molecular formulae', 'mirror images only']),
    ('What is a chiral centre?', 'a carbon atom bonded to four different atoms or groups', 'Gives non-superimposable mirror images (enantiomers).', ['a carbon atom with a double bond', 'a carbon atom bonded to four identical groups', 'any carbon in a ring']),
    ('Which compound shows cis/trans (geometrical) isomerism?', 'but-2-ene', 'Each C of C=C has two different groups.', ['but-1-ene', 'propene', '2-methylpropene']),
    ('How do optical isomers differ in their effect on light?', 'they rotate plane-polarised light in opposite directions', 'Enantiomers: equal and opposite rotation.', ['one absorbs UV, the other does not', 'they have different colours', 'they reflect light differently']),
    ('Which compound has a chiral centre?', 'butan-2-ol', 'C2 bonded to H, OH, CH₃, C₂H₅.', ['propan-2-ol', 'butan-1-ol', 'propanone']),
    ('State the conditions needed for cis/trans isomerism.', 'A C=C bond (restricted rotation) with two different groups on each carbon of the double bond.', '[2]'),
])
t13d.fixed('C2', (2, 3, 4), [
    ('Explain why but-1-ene does not show cis/trans isomerism but but-2-ene does.', 'In but-1-ene one carbon of the C=C carries two H atoms (identical groups); in but-2-ene each C=C carbon has H and CH₃.', 'but-1-ene has two identical groups on one C [1]; but-2-ene different groups on each C [1]'),
    ('Explain why a mixture of equal amounts of two enantiomers has no effect on plane-polarised light.', 'It is a racemic mixture: the equal and opposite rotations cancel out.', 'racemic, equal amounts [1]; rotations cancel [1]'),
    ('Explain why drug molecules with a chiral centre are often produced as a single enantiomer.', 'Only one enantiomer may fit the biological receptor/enzyme; the other may be inactive or harmful, and separating them is costly.', 'one enantiomer active [1]; other may be harmful/wasted [1]'),
])
errs(t13d, [
    ('Propan-2-ol is chiral because carbon 2 has an OH group.', 'Carbon 2 carries two identical CH₃ groups, so it is not a chiral centre.'),
    ('cis/trans isomers have different structural formulae.', 'They have the same structural formula; the arrangement in space differs (stereoisomers).'),
    ('2-methylpropene has cis and trans isomers.', 'One carbon of the C=C carries two CH₃ groups, so no geometrical isomers.'),
])
c2mix(t13d, ['{p} builds models of isomers of organic compounds.', 'A pharmaceutical chemist in {c} studies isomers of a drug molecule.'])


@t13d.add('C1', (1, 2, 3))
def t13d_stereo(r, D):
    nm, f, ct, ch = r.choice(STEREO)
    if ct and ch:
        corr = 'both cis/trans and optical isomerism'
    elif ct:
        corr = 'cis/trans (geometrical) isomerism only'
    elif ch:
        corr = 'optical isomerism only'
    else:
        corr = 'neither cis/trans nor optical isomerism'
    return mc(r, f'Which type(s) of stereoisomerism does {nm}, {f}, show?', corr, ['both cis/trans and optical isomerism', 'cis/trans (geometrical) isomerism only', 'optical isomerism only', 'neither cis/trans nor optical isomerism'],
              f'{nm}: ' + ('C=C with two different groups on each carbon; ' if ct else '') + ('chiral centre (four different groups); ' if ch else '') + corr + '.')


@t13d.add('C3', (2, 3, 4, 5), 'short')
def t13d_count(r, D):
    if r.random() < 0.5:
        mf, cls, n, lst = r.choice(NISO)
        stem = f'Deduce the number of structural isomers of {mf} that are {cls}, and name them.'
        key = f'{n} isomers [1]; names correct [{min(3, n - 1) if D >= 4 else 1}]'
        if D >= 4:
            stem += ' Identify any of them that show stereoisomerism.'
            st = NISO_ST.get((mf, cls), 'none of them shows stereoisomerism')
            key += f'; {st} [1]'
            return {'stem': stem, 'answer': f'{n}: {lst}; {st}', 'key': key}
        return {'stem': stem, 'answer': f'{n}: {lst}', 'key': key}
    a, b, mf, kind = r.choice(FGI)
    return {'stem': f'{cap(a)} and {b} both have the molecular formula {mf}. State the type of isomerism shown and describe one chemical test that would distinguish them.',
            'answer': f'Functional group isomerism ({kind}). {FGI_TEST[(a, b)]}', 'key': 'functional group isomerism [1]; suitable test [1]; result for each [1]'}


@t13d.add('C2', (2, 3, 4), 'explain')
def t13d_explain(r, D):
    nm, f, ct, ch = r.choice(STEREO)
    if ch:
        why = 'it has a chiral carbon bonded to four different groups, so it exists as two non-superimposable mirror images'
    elif ct:
        why = 'it has a C=C bond (restricted rotation) with two different groups on each carbon, so cis and trans forms exist'
    else:
        why = 'it has no chiral centre and no C=C with two different groups on each carbon'
    return {'stem': f'Explain whether {nm}, {f}, shows stereoisomerism. ' + ('Draw the isomers, if any.' if D >= 3 else ''),
            'answer': f'{"Yes" if ct or ch else "No"}: {why}.', 'key': 'correct conclusion [1]; structural reason [1]' + ('; 3D/cis-trans drawings correct [1]' if D >= 3 and (ct or ch) else '; reason fully stated [1]' if D >= 3 else '')}


def t13d_c4(r, D):
    nm, f, ct, ch = r.choice([x for x in STEREO if x[2] or x[3]])
    intro = P(r, r.choice([f'{{p}} investigates the isomers of {nm}, {f}.', f'A flavour company in {{c}} uses {nm}, {f}, and needs to know about its isomers.']))
    parts = [
        lambda r: ('Define the term stereoisomers.', 'Compounds with the same structural formula but different arrangements of atoms in space.', '[1]'),
        lambda r: (f'Explain which type(s) of stereoisomerism {nm} shows.', ('cis/trans: C=C with two different groups on each C. ' if ct else '') + ('Optical: chiral carbon with four different groups.' if ch else ''), '[2]'),
        lambda r: ('Describe how the 3D structures of the stereoisomers differ.', ('cis: the two matching groups are on the same side of the C=C; trans: on opposite sides. ' if ct else '') + ('Two tetrahedral arrangements about the chiral carbon that are non-superimposable mirror images.' if ch else ''), '[2]'),
        lambda r: ('Name or draw one structural isomer of the compound.', 'Any compound with the same molecular formula and different structure.', '[1]'),
        (lambda r: ('Explain how optical isomers can be distinguished.', 'They rotate plane-polarised light in opposite directions.', '[1]')) if ch else None,
        (lambda r: ('Explain why cis and trans isomers do not interconvert at room temperature.', 'The π bond prevents rotation about the C=C bond.', '[1]')) if ct else None,
    ]
    parts = [p for p in parts if p is not None]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t13d, t13d_c4)

CHAPTERS[13] = [t13a, t13b, t13c, t13d]

# ===================================================================== Ch14 Hydrocarbons
ALKANES = [(n, nm) for n, nm in [(1, 'methane'), (2, 'ethane'), (3, 'propane'), (4, 'butane'), (5, 'pentane'), (6, 'hexane'), (7, 'heptane'), (8, 'octane'), (10, 'decane'), (12, 'dodecane')]]
ALKENE_N = {2: 'ethene', 3: 'propene', 4: 'butene', 5: 'pentene', 6: 'hexene'}
ALK_N = dict(ALKANES)


def frac(x):
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f'{int(x)}½' if int(x) else '½'


def comb_eq(n, kind='complete'):
    h = 2 * n + 2
    f = F(f'C{n}H{h}') if n > 1 else 'CH₄'
    if kind == 'complete':
        o = (2 * n + h / 2) / 2
        return f'{f} + {frac(o)}O₂ → {n if n > 1 else ""}CO₂ + {int(h / 2)}H₂O'
    o = (n + h / 2) / 2
    return f'{f} + {frac(o)}O₂ → {n if n > 1 else ""}CO + {int(h / 2)}H₂O'


t14a = topic('Alkanes: combustion, free-radical substitution mechanism and cracking', 'alkanes: combustion, free-radical substitution', 'cracking')
t14a.fixed('C1', (1, 2), [
    ('What are the conditions for the reaction of methane with chlorine?', 'ultraviolet light', 'UV causes homolytic fission of Cl₂.', ['a nickel catalyst at 150 °C', 'aqueous sodium hydroxide', 'concentrated sulfuric acid']),
    ('Which step is a termination step in the chlorination of methane?', '•CH₃ + Cl• → CH₃Cl', 'Two radicals combine; radicals are removed.', ['Cl₂ → 2Cl•', 'CH₄ + Cl• → •CH₃ + HCl', '•CH₃ + Cl₂ → CH₃Cl + Cl•']),
    ('Why are alkanes generally unreactive?', 'C–C and C–H bonds are strong and non-polar', 'Little polarity to attract nucleophiles or electrophiles.', ['they have π bonds', 'they are ionic', 'they contain lone pairs']),
    ('What is the purpose of cracking?', 'to convert long-chain alkanes into shorter, more useful alkanes and alkenes', 'Meets demand for petrol and alkenes for polymers.', ['to separate crude oil into fractions', 'to remove sulfur from fuels', 'to make longer alkanes']),
    ('Which pollutant is produced by incomplete combustion of alkanes?', 'carbon monoxide', 'Limited O₂ gives CO (toxic) and C (soot).', ['sulfur dioxide', 'nitrogen', 'ozone']),
    ('Write the equation for the initiation step in the reaction of methane with bromine.', 'Br₂ → 2Br• (in UV light)', '[1]'),
])
t14a.fixed('C2', (2, 3, 4), [
    ('Explain why the reaction of ethane with excess chlorine gives a mixture of products.', 'Further substitution occurs: Cl• can remove H from chloroethane etc., giving di-, tri- and polychloro compounds; termination also gives butane.', 'further substitution [1]; mixture of products/termination by-products [1]'),
    ('Explain why carbon monoxide is toxic.', 'It binds strongly to haemoglobin, reducing the blood’s ability to carry oxygen.', 'binds haemoglobin [1]; less O₂ transported [1]'),
    ('Explain why the propagation steps are described as a chain reaction.', 'Each propagation step uses one radical and produces another, so the sequence repeats many times from one initiation.', 'radical regenerated [1]; repeats many times [1]'),
    ('State the conditions for catalytic cracking and explain why it is used.', 'Heat (about 500 °C) with a zeolite/Al₂O₃ catalyst; converts low-demand heavy fractions into high-demand petrol and alkenes for polymers.', 'conditions [1]; reason (supply and demand/alkenes) [1]'),
])
errs(t14a, [
    ('In the propagation step, Cl• + CH₄ → CH₃Cl + H•.', 'The correct step is Cl• + CH₄ → •CH₃ + HCl; H• is not formed.'),
    ('Cracking an alkane always gives two alkanes.', 'Cracking gives a shorter alkane and at least one alkene (to balance hydrogen).'),
])
c2mix(t14a, ['{p} investigates the reaction of hexane with bromine in sunlight.', 'An oil refinery in {c} cracks heavy fractions of crude oil.'])


@t14a.add('C3', (1, 2, 3, 4), 'short')
def t14a_comb(r, D):
    n, nm = r.choice(ALKANES[:8])
    kind = r.choice(['complete', 'incomplete'])
    right = comb_eq(n, kind)
    if D <= 2:
        o_wrong = [right.replace(frac((2 * n + n + 1) / 2) + 'O₂' if kind == 'complete' else frac((n + n + 1) / 2) + 'O₂', frac((2 * n + n + 1) / 2 + d) + 'O₂' if kind == 'complete' else frac((n + n + 1) / 2 + d) + 'O₂') for d in (1, -0.5, 0.5, 2)]
        return mc(r, f'Which is the balanced equation for the {kind} combustion of {nm} to {"CO₂" if kind == "complete" else "CO"} and water?', right, o_wrong, right)
    mass = r.choice([1.0, 2.0, 5.0, 10.0, 50.0])
    M = Mr(f'C{n}H{2 * n + 2}')
    vco2 = mass / M * n * 24.0
    return {'stem': f'Write the equation for the complete combustion of {nm}. Calculate the volume of carbon dioxide (r.t.p.) formed when {mass:g} g of {nm} burns completely.' + (' Give one environmental problem of the CO₂ released.' if D >= 4 else ''),
            'answer': f'{comb_eq(n)}; {g3(vco2)} dm³' + ('; enhanced greenhouse effect/climate change' if D >= 4 else ''), 'key': f'balanced equation [1]; n(alkane) = {mass:g}/{mr1(M)} = {g3(mass / M)} mol [1]; V(CO₂) = × {n} × 24.0 = {g3(vco2)} dm³ [1]' + ('; global warming [1]' if D >= 4 else '')}


@t14a.add('C3', (2, 3, 4, 5), 'short')
def t14a_crack(r, D):
    n = r.choice([8, 10, 12, 14, 16])
    m = r.choice([k for k in (4, 5, 6, 7, 8, 10) if k < n - 1])
    rest = n - m
    k = r.choice([1, 2] if rest % 2 == 0 and rest >= 4 else [1])
    alk = f'C{n}H{2 * n + 2}'
    prod = f'C{m}H{2 * m + 2}'
    e_each = rest // k
    alkene = f'C{e_each}H{2 * e_each}'
    co = f'{k if k > 1 else ""}{alkene}'
    eq = f'{F(alk)} → {F(prod)} + {k if k > 1 else ""}{F(alkene)}'
    if rest % k:
        return None
    stem = f'A sample of {ALK_N.get(n, F(alk))}, {F(alk)}, is cracked to give {ALK_N.get(m, F(prod))}, {F(prod)}, and {"one molecule" if k == 1 else f"{k} molecules"} of a single alkene. Write the equation and identify the alkene.'
    key = f'equation balanced [1]; alkene {F(alkene)} ({ALKENE_N.get(e_each, "an alkene")}) [1]'
    if D >= 4:
        stem += ' Describe a test to show that one product is unsaturated and give the conditions for catalytic cracking.'
        key += '; bromine water decolourised (orange → colourless) [1]; ~500 °C, zeolite/Al₂O₃ catalyst [1]'
    return {'stem': stem, 'answer': f'{eq}; alkene {F(alkene)}', 'key': key}


@t14a.add('C2', (2, 3, 4), 'explain')
def t14a_mech(r, D):
    alk, hal = r.choice([('methane', 'chlorine'), ('methane', 'bromine'), ('ethane', 'chlorine'), ('ethane', 'bromine')])
    X = 'Cl' if hal == 'chlorine' else 'Br'
    R = 'CH₃' if alk == 'methane' else 'C₂H₅'
    RH = 'CH₄' if alk == 'methane' else 'C₂H₆'
    steps = f'Initiation: {X}₂ → 2{X}• (UV). Propagation: {RH} + {X}• → •{R} + H{X}; •{R} + {X}₂ → {R}{X} + {X}•. Termination: {X}• + {X}• → {X}₂; •{R} + {X}• → {R}{X}; •{R} + •{R} → {"C₂H₆" if R == "CH₃" else "C₄H₁₀"}.'
    return {'stem': f'Describe the mechanism of the reaction between {alk} and {hal} in ultraviolet light. Name each stage and write equations.' if D >= 3 else f'Name the mechanism for the reaction between {alk} and {hal} in UV light and write the equation for the initiation step.',
            'answer': ('Free-radical substitution. ' + steps) if D >= 3 else f'Free-radical substitution; {X}₂ → 2{X}•', 'key': ('name [1]; initiation with UV [1]; two propagation steps [1]; one termination step [1]' if D >= 3 else 'free-radical substitution [1]; initiation equation [1]')}


def t14a_c4(r, D):
    alk = r.choice(['propane', 'butane', 'methane', 'ethane'])
    n = {'methane': 1, 'ethane': 2, 'propane': 3, 'butane': 4}[alk]
    intro = P(r, r.choice([f'{alk.capitalize()} is used as a fuel in {{c}} and is also a raw material for halogenoalkanes.', f'{{p}} investigates the reactions of {alk} in {{lab}}.']))
    parts = [
        lambda r: (f'Write equations for the complete and incomplete combustion of {alk}.', f'{comb_eq(n)}; {comb_eq(n, "incomplete")}', '[2]'),
        lambda r: ('Explain why incomplete combustion is dangerous.', 'CO is toxic: binds haemoglobin, reduces oxygen transport.', '[1]'),
        lambda r: (f'Describe the free-radical substitution of {alk} with chlorine, including one equation for each stage.', 'Initiation Cl₂ → 2Cl•; propagation RH + Cl• → R• + HCl, R• + Cl₂ → RCl + Cl•; termination two radicals combine.', '[4]'),
        lambda r: ('Explain why a mixture of products is formed.', 'Further substitution; different H atoms substituted; termination products.', '[2]'),
        lambda r: ('Give the conditions for catalytic cracking and state why it is important.', '~500 °C, zeolite catalyst; makes petrol and alkenes in high demand.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t14a, t14a_c4)

# ---------------------------------------------------------- 14.2 alkenes: electrophilic addition
ALKENES = {  # name: (formula, H2, Br2, HBr major (cation), HBr minor, steam major, diol, hot KMnO4)
    'ethene': ('CH₂=CH₂', 'ethane', '1,2-dibromoethane', ('bromoethane', 'primary'), None, 'ethanol', 'ethane-1,2-diol', 'carbon dioxide (and water)'),
    'propene': ('CH₂=CHCH₃', 'propane', '1,2-dibromopropane', ('2-bromopropane', 'secondary'), '1-bromopropane', 'propan-2-ol', 'propane-1,2-diol', 'ethanoic acid and carbon dioxide'),
    'but-1-ene': ('CH₂=CHCH₂CH₃', 'butane', '1,2-dibromobutane', ('2-bromobutane', 'secondary'), '1-bromobutane', 'butan-2-ol', 'butane-1,2-diol', 'propanoic acid and carbon dioxide'),
    'but-2-ene': ('CH₃CH=CHCH₃', 'butane', '2,3-dibromobutane', ('2-bromobutane', 'secondary'), None, 'butan-2-ol', 'butane-2,3-diol', 'ethanoic acid only (two molecules)'),
    '2-methylpropene': ('CH₂=C(CH₃)₂', '2-methylpropane', '1,2-dibromo-2-methylpropane', ('2-bromo-2-methylpropane', 'tertiary'), '1-bromo-2-methylpropane', '2-methylpropan-2-ol', '2-methylpropane-1,2-diol', 'propanone and carbon dioxide'),
    'pent-2-ene': ('CH₃CH=CHCH₂CH₃', 'pentane', '2,3-dibromopentane', ('2-bromopentane and 3-bromopentane (similar amounts)', 'secondary'), None, 'pentan-2-ol and pentan-3-ol', 'pentane-2,3-diol', 'ethanoic acid and propanoic acid'),
    '2-methylbut-2-ene': ('(CH₃)₂C=CHCH₃', '2-methylbutane', '2,3-dibromo-2-methylbutane', ('2-bromo-2-methylbutane', 'tertiary'), '2-bromo-3-methylbutane', '2-methylbutan-2-ol', '2-methylbutane-2,3-diol', 'propanone and ethanoic acid'),
    'cyclohexene': ('C₆H₁₀ (cyclic)', 'cyclohexane', '1,2-dibromocyclohexane', ('bromocyclohexane', 'secondary'), None, 'cyclohexanol', 'cyclohexane-1,2-diol', 'hexanedioic acid'),
}
ADD_COND = {'hydrogen': 'H₂ with a nickel catalyst, about 150 °C', 'bromine': 'bromine (in an organic solvent or bromine water) at room temperature', 'hydrogen bromide': 'HBr(g) at room temperature',
            'steam': 'steam with a phosphoric(V) acid catalyst, about 300 °C and 6 MPa'}

t14b = topic("Alkenes: electrophilic addition mechanism and Markovnikov's rule", 'alkenes: electrophilic addition mechanism', "markovnikov's rule")
t14b.fixed('C1', (1, 2), [
    ('What is the test for an alkene?', 'bromine water turns from orange to colourless', 'Electrophilic addition of Br₂ across C=C.', ['limewater turns milky', 'acidified dichromate turns green', 'a silver mirror forms']),
    ('Which carbocation is the most stable?', 'tertiary', 'More alkyl groups donate electron density and stabilise the positive charge.', ['primary', 'secondary', 'methyl']),
    ('What is the major product when HBr adds to propene?', '2-bromopropane', 'Via the more stable secondary carbocation (Markovnikov).', ['1-bromopropane', '1,2-dibromopropane', 'propan-2-ol']),
    ('What conditions are used to hydrogenate an alkene?', 'hydrogen with a nickel catalyst at about 150 °C', 'Addition of H₂ across C=C.', ['UV light', 'aqueous sodium hydroxide', 'cold dilute KMnO₄']),
    ('In the mechanism for the addition of HBr to ethene, what is the first species to bond to the alkene?', 'the H atom (δ+) of HBr', 'π electrons attack Hδ+; Br⁻ then attacks the carbocation.', ['Br⁻', 'Br•', 'OH⁻']),
    ("State Markovnikov's rule.", 'When HX adds to an unsymmetrical alkene, H adds to the carbon that already has more H atoms (via the more stable carbocation).', '[1]'),
])
t14b.fixed('C2', (2, 3, 4), [
    ('Explain why 2-bromopropane is the major product when HBr reacts with propene.', 'The intermediate secondary carbocation CH₃CH⁺CH₃ is more stable than the primary carbocation because two alkyl groups donate electron density (positive inductive effect).', 'secondary carbocation more stable [1]; alkyl groups electron-donating [1]'),
    ('Explain how a non-polar bromine molecule can act as an electrophile.', 'As Br₂ approaches the electron-rich C=C, the π electrons repel the electrons in Br–Br, inducing a dipole; Brδ+ accepts electrons from the π bond.', 'induced dipole [1]; δ+ Br attacked by π electrons [1]'),
    ('Explain why ethene and bromine water give 2-bromoethanol as well as 1,2-dibromoethane.', 'The carbocation intermediate can be attacked by water (present in large excess) as a nucleophile as well as by Br⁻.', 'carbocation intermediate [1]; water competes as nucleophile [1]'),
])
errs(t14b, [
    ('HBr adds to propene to give mainly 1-bromopropane.', 'The major product is 2-bromopropane via the more stable secondary carbocation.'),
    ('In electrophilic addition, Br⁻ attacks the C=C bond first.', 'The electrophile (H⁺ or Brδ+) is attacked by the π electrons first; Br⁻ then attacks the carbocation.'),
    ('A primary carbocation is more stable than a tertiary carbocation.', 'Tertiary carbocations are most stable: three alkyl groups donate electron density.'),
])
c2mix(t14b, ['{p} investigates the reactions of alkenes in {lab}.', 'A petrochemical plant in {c} converts alkenes into other products.'])


@t14b.add('C1', (1, 2, 3))
def t14b_prod(r, D):
    nm = r.choice(list(ALKENES))
    a = ALKENES[nm]
    reag = r.choice(['hydrogen', 'bromine', 'hydrogen bromide', 'steam'])
    corr = {'hydrogen': a[1], 'bromine': a[2], 'hydrogen bromide': a[3][0], 'steam': a[5]}[reag]
    pool = [a[1], a[2], a[3][0], a[5], a[6]] + ([a[4]] if a[4] else []) + [r.choice([x[2] for x in ALKENES.values()])]
    return mc(r, f'What is the {"major " if reag in ("hydrogen bromide", "steam") else ""}organic product when {nm} reacts with {ADD_COND[reag]}?', corr, pool, f'{nm} + {reag} → {corr}.')


@t14b.add('C3', (2, 3, 4, 5), 'short')
def t14b_mark(r, D):
    nm = r.choice([k for k, v in ALKENES.items() if v[4]])
    a = ALKENES[nm]
    stem = f'Hydrogen bromide reacts with {nm}, {a[0]}. Name the major and minor products and explain, in terms of the intermediates, why one product is formed in greater amount.'
    key = f'major {a[3][0]} [1]; minor {a[4]} [1]; via more stable {a[3][1]} carbocation (more alkyl groups, positive inductive effect) [1]'
    if D >= 4:
        stem += ' Describe the mechanism, including curly arrows and partial charges.'
        key += '; π electrons attack Hδ+, Br–H bond breaks heterolytically [1]; Br⁻ lone pair attacks carbocation [1]'
    return {'stem': stem, 'answer': f'major {a[3][0]}; minor {a[4]}; the {a[3][1]} carbocation intermediate is more stable', 'key': key}


@t14b.add('C2', (2, 3, 4), 'explain')
def t14b_mech(r, D):
    nm = r.choice(['ethene', 'propene', 'but-2-ene', 'cyclohexene'])
    reag = r.choice(['bromine', 'hydrogen bromide'])
    a = ALKENES[nm]
    prod = a[2] if reag == 'bromine' else a[3][0]
    return {'stem': f'Describe the mechanism for the reaction of {nm} with {reag}. Name the mechanism and the product.',
            'answer': f'Electrophilic addition. The π electrons of C=C attack the δ+ {"Br of the polarised Br₂ (induced dipole)" if reag == "bromine" else "H of H–Br"}; the bond breaks heterolytically giving Br⁻ and a carbocation; Br⁻ attacks the carbocation. Product: {prod}.',
            'key': 'name: electrophilic addition [1]; curly arrow from π bond to δ+ atom and heterolytic fission [1]; carbocation and attack by Br⁻ [1]' + ('; product named [1]' if D >= 4 else '')}


def t14b_c4(r, D):
    nm = r.choice(['propene', 'but-1-ene', '2-methylpropene'])
    a = ALKENES[nm]
    intro = P(r, r.choice([f'{{p}} investigates the reactions of {nm}, {a[0]}, in {{lab}}.', f'A chemical company in {{c}} uses {nm} as a feedstock.']))
    parts = [
        lambda r: ('Describe a test to show that the compound is unsaturated.', 'Shake with bromine water: orange to colourless.', '[2]'),
        lambda r: ('Name the products with H₂/Ni and with Br₂.', f'{a[1]}; {a[2]}', '[2]'),
        lambda r: ('Name the major product with HBr and explain why it is the major product.', f'{a[3][0]}: more stable {a[3][1]} carbocation intermediate.', '[2]'),
        lambda r: ('Outline the mechanism for the reaction with HBr.', 'Electrophilic addition: π electrons attack Hδ+, heterolytic fission, carbocation, Br⁻ attacks.', '[3]'),
        lambda r: ('Give the conditions and major product for the reaction with steam.', f'{ADD_COND["steam"]}; {a[5]}', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t14b, t14b_c4)

# ---------------------------------------------------------- 14.3 KMnO4 oxidation
t14c = topic('Oxidation of alkenes with cold dilute and hot concentrated acidified manganate(VII)', 'oxidation of alkenes with cold dilute', 'acidified manganate(vii)')
t14c.fixed('C1', (1, 2), [
    ('What is formed when ethene reacts with cold, dilute, acidified KMnO₄?', 'ethane-1,2-diol', 'Two OH groups added across C=C; purple → colourless.', ['ethanoic acid', 'carbon dioxide', 'ethanol']),
    ('What colour change is seen when an alkene reacts with acidified potassium manganate(VII)?', 'purple to colourless', 'MnO₄⁻ (purple) reduced to Mn²⁺ (almost colourless).', ['orange to green', 'colourless to purple', 'blue to brick red']),
    ('What happens to the C=C bond when an alkene is heated with hot concentrated acidified KMnO₄?', 'it breaks completely', 'Oxidative cleavage gives ketones, carboxylic acids or CO₂.', ['it is converted into a C–C single bond with two OH groups', 'it is unchanged', 'it becomes a triple bond']),
    ('Which product forms from a =CH₂ group on oxidation with hot concentrated KMnO₄?', 'carbon dioxide', '=CH₂ → CO₂ + H₂O; =CHR → RCOOH; =CR₂ → R₂C=O.', ['methanal', 'methanoic acid only', 'methanol']),
    ('Which product forms from a =CR₂ group (two alkyl groups on the carbon) with hot concentrated KMnO₄?', 'a ketone', 'No H on that carbon, so it stops at the ketone.', ['a carboxylic acid', 'an aldehyde', 'carbon dioxide']),
    ('State the reagents and conditions to make a diol from an alkene.', 'Cold, dilute, acidified potassium manganate(VII).', '[1]'),
])
t14c.fixed('C2', (2, 3, 4), [
    ('Explain how hot concentrated KMnO₄ can be used to locate the position of a C=C bond in an alkene.', 'The C=C is split and each carbon becomes C=O; identifying the products (CO₂, acids, ketones) shows which groups were attached on each side of the double bond.', 'C=C cleaved [1]; products identify fragments either side [1]'),
    ('Explain why but-2-ene gives only one organic product with hot concentrated acidified KMnO₄.', 'It is symmetrical: each =CHCH₃ end gives ethanoic acid.', 'symmetrical [1]; both halves give ethanoic acid [1]'),
])
errs(t14c, [
    ('Hot concentrated KMnO₄ converts propene into propane-1,2-diol.', 'The diol forms with cold dilute KMnO₄; hot concentrated KMnO₄ cleaves the C=C to give ethanoic acid and CO₂.'),
    ('2-methylpropene gives two carboxylic acids with hot concentrated KMnO₄.', 'The (CH₃)₂C= end gives propanone (a ketone) and the =CH₂ end gives CO₂.'),
])
c2mix(t14c, ['{p} uses acidified potassium manganate(VII) to identify unknown alkenes.', 'A research student in {c} determines the position of double bonds in a natural product.'])


@t14c.add('C3', (1, 2, 3, 4, 5), 'short')
def t14c_prod(r, D):
    nm = r.choice(list(ALKENES))
    a = ALKENES[nm]
    if D == 1:
        return mc(r, f'What are the organic products when {nm} is heated with concentrated acidified KMnO₄?', a[7], [v[7] for v in ALKENES.values()], f'{nm}: {a[7]}.')
    if D == 2:
        return {'stem': f'Name the organic product formed when {nm}, {a[0]}, is shaken with cold, dilute, acidified potassium manganate(VII). State the colour change.', 'answer': f'{a[6]}; purple to colourless',
                'key': f'{a[6]} [1]; purple → colourless [1]'}
    stem = f'{nm.capitalize()}, {a[0]}, is heated with hot, concentrated, acidified potassium manganate(VII). Name the products and explain how they form.'
    key = f'products {a[7]} [1]; C=C cleaved [1]; =CH₂ → CO₂, =CHR → RCOOH, =CR₂ → ketone applied [1]'
    if D >= 4:
        stem = f'An alkene X, C₅H₁₀ or C₄H₈, gives {a[7]} when heated with hot concentrated acidified KMnO₄. Deduce the structure and name of X, explaining your reasoning.' if nm not in ('cyclohexene', 'ethene', 'propene') else stem
        key += '; structure of X deduced from fragments [1]'
    return {'stem': stem, 'answer': f'{nm} ({a[0]}) → {a[7]}', 'key': key}


def t14c_c4(r, D):
    nm = r.choice(['propene', 'but-1-ene', 'but-2-ene', '2-methylpropene', 'pent-2-ene', '2-methylbut-2-ene'])
    a = ALKENES[nm]
    intro = P(r, r.choice([f'{{p}} is given an alkene, {nm} ({a[0]}), and reacts it separately with cold dilute and hot concentrated acidified KMnO₄.', f'A laboratory in {{c}} studies the oxidation of {nm}, {a[0]}.']))
    parts = [
        lambda r: ('Name the product with cold, dilute, acidified KMnO₄ and state the colour change.', f'{a[6]}; purple to colourless', '[2]'),
        lambda r: ('Name the products with hot, concentrated, acidified KMnO₄.', a[7], '[2]'),
        lambda r: ('Explain why the C=C carbons give different types of product.', '=CH₂ gives CO₂; =CHR gives carboxylic acid; =CR₂ gives ketone.', '[2]'),
        lambda r: ('Describe a test to show which product is a carboxylic acid.', 'Add Na₂CO₃/NaHCO₃: effervescence, CO₂ turns limewater milky.', '[2]'),
        lambda r: ('State the role of manganate(VII) in these reactions.', 'Oxidising agent (it is reduced to Mn²⁺).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t14c, t14c_c4)

# ---------------------------------------------------------- 14.4 addition polymerisation
POLY = [('ethene', 'CH₂=CH₂', 'poly(ethene)', '–CH₂–CH₂–', 28.0, 'plastic bags, bottles'), ('propene', 'CH₂=CHCH₃', 'poly(propene)', '–CH₂–CH(CH₃)–', 42.0, 'ropes, crates'),
        ('chloroethene', 'CH₂=CHCl', 'poly(chloroethene), PVC', '–CH₂–CHCl–', 62.5, 'window frames, pipes'), ('tetrafluoroethene', 'CF₂=CF₂', 'poly(tetrafluoroethene), PTFE', '–CF₂–CF₂–', 100.0, 'non-stick coatings'),
        ('phenylethene', 'CH₂=CHC₆H₅', 'poly(phenylethene), polystyrene', '–CH₂–CH(C₆H₅)–', 104.0, 'packaging, insulation'), ('but-2-ene', 'CH₃CH=CHCH₃', 'poly(but-2-ene)', '–CH(CH₃)–CH(CH₃)–', 56.0, '—'),
        ('propenenitrile', 'CH₂=CHCN', 'poly(propenenitrile)', '–CH₂–CH(CN)–', 53.0, 'acrylic fibres'), ('methyl 2-methylpropenoate', 'CH₂=C(CH₃)COOCH₃', 'poly(methyl 2-methylpropenoate), Perspex', '–CH₂–C(CH₃)(COOCH₃)–', 100.0, 'Perspex sheets')]

t14d = topic('Addition polymerisation and environmental issues of polyalkenes', 'addition polymerisation', 'environmental issues of polyalkenes')
t14d.fixed('C1', (1, 2), [
    ('What is addition polymerisation?', 'the joining of many alkene monomers to form a long chain with no other product', 'C=C bonds open; polymer is the only product.', ['the joining of monomers with loss of water', 'the breaking of a polymer into monomers', 'the reaction of alkanes with oxygen']),
    ('Why are poly(alkenes) non-biodegradable?', 'they are saturated with strong non-polar C–C and C–H bonds that microorganisms cannot break', 'Chemically inert; persist in landfill and the environment.', ['they contain double bonds', 'they are ionic', 'they dissolve in water']),
    ('Which toxic gas is released when PVC is burned?', 'hydrogen chloride', 'PVC contains chlorine.', ['carbon dioxide only', 'nitrogen', 'oxygen']),
    ('What is the repeat unit of poly(propene)?', '–CH₂–CH(CH₃)–', 'Two carbons of the C=C in the main chain; CH₃ as a side group.', ['–CH₂–CH₂–CH₂–', '–CH=CH(CH₃)–', '–CH(CH₃)–CH(CH₃)–']),
    ('Which monomer forms PTFE?', 'tetrafluoroethene', 'CF₂=CF₂ → –(CF₂–CF₂)ₙ–.', ['chloroethene', 'fluoroethane', 'propene']),
    ('State one environmental problem caused by the disposal of poly(alkenes).', 'Non-biodegradable, so they persist in landfill/oceans; burning releases toxic gases (and CO₂).', '[1]'),
])
t14d.fixed('C2', (2, 3, 4), [
    ('Discuss the advantages and disadvantages of disposing of waste poly(alkenes) by combustion.', 'Advantage: energy can be recovered and landfill space saved. Disadvantages: CO₂ (greenhouse gas), CO and toxic gases such as HCl from PVC must be removed.', 'advantage [1]; disadvantage [1]'),
    ('Explain why poly(ethene) is unreactive although ethene is very reactive.', 'In the polymer the C=C bonds have been converted to single C–C bonds; it is effectively a long alkane.', 'no C=C in polymer [1]; saturated/alkane-like [1]'),
])
errs(t14d, [
    ('Poly(ethene) contains many C=C double bonds, which is why it is called a polyalkene.', 'The C=C bonds open during polymerisation; the polymer has only single bonds.'),
    ('The repeat unit of poly(chloroethene) is –CH₂–CH₂–Cl–.', 'The repeat unit is –CH₂–CHCl–: Cl is a side group on one chain carbon.'),
])
c2mix(t14d, ['A recycling company in {c} sorts waste plastics.', '{p} studies the structures of polymers made from alkenes.'])


@t14d.add('C1', (1, 2, 3))
def t14d_unit(r, D):
    mon, f, pol, ru, M, use = r.choice(POLY)
    if r.random() < 0.5:
        return mc(r, f'What is the repeat unit of the polymer formed from {mon}, {f}?', ru, [x[3] for x in POLY], f'{pol}: {ru}.')
    return mc(r, f'Which monomer is used to make a polymer with repeat unit {ru}?', mon, [x[0] for x in POLY], f'{ru} comes from {mon}.')


@t14d.add('C3', (2, 3, 4, 5), 'numerical')
def t14d_calc(r, D):
    mon, f, pol, ru, M, use = r.choice(POLY)
    n = r.choice([500, 1000, 2000, 5000, 10000, 25000])
    Mp = n * M
    if r.random() < 0.5:
        return {'stem': f'A sample of {pol} has an average relative molecular mass of {sf(Mp, 3)}. Calculate the average number of monomer units in each chain, given Mr({mon}) = {M}.',
                'answer': f'{sf(n, 3)}', 'key': f'Mr of repeat unit = Mr of monomer = {M} [1]; n = {sf(Mp, 3)}/{M} = {sf(n, 3)} [1]'}
    mass = r.choice([1.0, 5.0, 10.0, 50.0])
    return {'stem': f'{mass:g} kg of {mon} is polymerised to {pol}. Explain why the mass of polymer formed (assuming complete conversion) is also {mass:g} kg, and draw the repeat unit.' + (' Explain one environmental problem associated with its disposal.' if D >= 4 else ''),
            'answer': f'{mass:g} kg; addition polymerisation has no by-product (atom economy 100%); repeat unit {ru}', 'key': 'no other product / 100% atom economy [1]; repeat unit drawn [1]' + ('; non-biodegradable / toxic combustion products [1]' if D >= 4 else '')}


def t14d_c4(r, D):
    mon, f, pol, ru, M, use = r.choice(POLY[:5])
    intro = P(r, r.choice([f'{pol} is made from {mon}, {f}, and is used for {use}.', f'{{p}} is writing a report for a council in {{c}} about {pol} waste.']))
    parts = [
        lambda r: ('Draw the repeat unit of the polymer.', ru, '[1]'),
        lambda r: ('Name the type of polymerisation and explain the term.', 'Addition polymerisation: monomers with C=C join to form a single product.', '[2]'),
        lambda r: ('Explain why the polymer is chemically unreactive.', 'Saturated: strong non-polar C–C and C–H bonds.', '[1]'),
        lambda r: ('Discuss two methods of disposing of the waste polymer and their environmental impact.', 'Landfill: non-biodegradable, persists; combustion: energy recovery but CO₂ and toxic gases (HCl from PVC); recycling saves resources.', '[3]'),
        lambda r: (f'Calculate the number of monomer units in a chain of Mr {sf(M * 4000, 3)}.', '4000', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t14d, t14d_c4)

CHAPTERS[14] = [t14a, t14b, t14c, t14d]

# ===================================================================== Ch15 Halogen compounds
HALO = {  # name: (formula, class, NaOH(aq) product, KCN product (name, formula), NH3 product, elimination product, preferred mechanism)
    'chloroethane': ('CH₃CH₂Cl', 'primary', 'ethanol', ('propanenitrile', 'CH₃CH₂CN'), 'ethylamine', 'ethene', 'SN2'),
    'bromoethane': ('CH₃CH₂Br', 'primary', 'ethanol', ('propanenitrile', 'CH₃CH₂CN'), 'ethylamine', 'ethene', 'SN2'),
    'iodoethane': ('CH₃CH₂I', 'primary', 'ethanol', ('propanenitrile', 'CH₃CH₂CN'), 'ethylamine', 'ethene', 'SN2'),
    '1-bromopropane': ('CH₃CH₂CH₂Br', 'primary', 'propan-1-ol', ('butanenitrile', 'CH₃CH₂CH₂CN'), 'propylamine', 'propene', 'SN2'),
    '1-chloropropane': ('CH₃CH₂CH₂Cl', 'primary', 'propan-1-ol', ('butanenitrile', 'CH₃CH₂CH₂CN'), 'propylamine', 'propene', 'SN2'),
    '2-bromopropane': ('CH₃CHBrCH₃', 'secondary', 'propan-2-ol', ('2-methylpropanenitrile', 'CH₃CH(CN)CH₃'), 'propan-2-amine', 'propene', 'SN1 and SN2'),
    '1-bromobutane': ('CH₃CH₂CH₂CH₂Br', 'primary', 'butan-1-ol', ('pentanenitrile', 'CH₃CH₂CH₂CH₂CN'), 'butylamine (butan-1-amine)', 'but-1-ene', 'SN2'),
    '2-bromobutane': ('CH₃CHBrCH₂CH₃', 'secondary', 'butan-2-ol', ('2-methylbutanenitrile', 'CH₃CH(CN)CH₂CH₃'), 'butan-2-amine', 'but-1-ene and but-2-ene (cis and trans)', 'SN1 and SN2'),
    '2-bromo-2-methylpropane': ('(CH₃)₃CBr', 'tertiary', '2-methylpropan-2-ol', ('2,2-dimethylpropanenitrile', '(CH₃)₃CCN'), '2-methylpropan-2-amine', '2-methylpropene', 'SN1'),
    '2-chloro-2-methylpropane': ('(CH₃)₃CCl', 'tertiary', '2-methylpropan-2-ol', ('2,2-dimethylpropanenitrile', '(CH₃)₃CCN'), '2-methylpropan-2-amine', '2-methylpropene', 'SN1'),
    '1-iodobutane': ('CH₃CH₂CH₂CH₂I', 'primary', 'butan-1-ol', ('pentanenitrile', 'CH₃CH₂CH₂CH₂CN'), 'butylamine (butan-1-amine)', 'but-1-ene', 'SN2'),
    'iodomethane': ('CH₃I', 'methyl (treated as primary)', 'methanol', ('ethanenitrile', 'CH₃CN'), 'methylamine', 'none (only one carbon)', 'SN2'),
    '2-chlorobutane': ('CH₃CHClCH₂CH₃', 'secondary', 'butan-2-ol', ('2-methylbutanenitrile', 'CH₃CH(CN)CH₂CH₃'), 'butan-2-amine', 'but-1-ene and but-2-ene (cis and trans)', 'SN1 and SN2'),
}
HCOND = {'NaOH(aq)': 'aqueous sodium hydroxide, heated under reflux', 'KCN': 'potassium cyanide in ethanol, heated under reflux', 'NH3': 'excess concentrated ammonia in ethanol, heated in a sealed tube',
         'NaOH(eth)': 'sodium hydroxide dissolved in ethanol, heated'}
CX = {'Cl': 340, 'Br': 280, 'I': 240}

t15a = topic('Making halogenoalkanes and classifying them as primary, secondary and tertiary', 'making halogenoalkanes', 'classifying them as primary, secondary and tertiary')
t15a.fixed('C1', (1, 2), [
    ('How is a tertiary halogenoalkane defined?', 'the carbon bonded to the halogen is attached to three other carbon atoms', 'Primary: 1 C; secondary: 2 C; tertiary: 3 C attached to the C–X carbon.', ['it contains three halogen atoms', 'the halogen is on carbon 3', 'it has three carbon atoms']),
    ('Which reagent converts ethanol into chloroethane?', 'phosphorus(V) chloride, PCl₅', 'Also PCl₃ (heat), SOCl₂, or HCl/ZnCl₂.', ['aqueous sodium chloride', 'chlorine in UV light', 'hydrochloric acid at room temperature with no catalyst']),
    ('How is bromoethane made from ethanol in the laboratory?', 'by heating with sodium bromide and concentrated sulfuric acid', 'NaBr + H₂SO₄ → HBr in situ; C₂H₅OH + HBr → C₂H₅Br + H₂O.', ['by reacting with bromine water', 'by adding aqueous potassium bromide', 'by heating with bromine in UV light']),
    ('Which is a secondary halogenoalkane?', '2-bromopropane', 'C–Br carbon bonded to two other carbons.', ['1-bromopropane', '2-bromo-2-methylpropane', 'bromomethane']),
    ('What is formed when HBr adds to ethene?', 'bromoethane', 'Electrophilic addition.', ['1,2-dibromoethane', 'ethanol', 'bromoethene']),
    ('State two ways of making a halogenoalkane.', 'Any two: free-radical substitution of an alkane; addition of HX (or X₂) to an alkene; substitution of an alcohol with HX/PCl₅/PCl₃/SOCl₂.', '[2]'),
])
t15a.fixed('C2', (2, 3, 4), [
    ('Explain why free-radical substitution is not a good method for making a pure halogenoalkane.', 'A mixture of products forms (further substitution, different positions, termination products), which must be separated, giving a low yield.', 'mixture of products [1]; low yield/separation needed [1]'),
    ('Explain why the reaction of an alcohol with PCl₅ can be used as a test for an –OH group.', 'Steamy fumes of HCl are given off: ROH + PCl₅ → RCl + POCl₃ + HCl.', 'steamy fumes HCl [1]; equation [1]'),
])
errs(t15a, [
    ('2-bromo-2-methylpropane is a secondary halogenoalkane because Br is on carbon 2.', 'The C–Br carbon is attached to three other carbons, so it is tertiary.'),
    ('Bromoethane can be made by adding aqueous sodium bromide to ethanol.', 'HBr (from NaBr + conc H₂SO₄) is needed and the mixture is heated; Br⁻ alone does not replace OH.'),
])
c2mix(t15a, ['{p} prepares halogenoalkanes in {lab}.', 'A chemical supplier in {c} makes halogenoalkanes for synthesis.'])


@t15a.add('C1', (1, 2, 3))
def t15a_class(r, D):
    nm = r.choice([k for k in HALO if 'methyl (' not in HALO[k][1]])
    f, cls = HALO[nm][0], HALO[nm][1]
    return mc(r, f'Classify {nm}, {f}.', f'{cls} halogenoalkane', ['primary halogenoalkane', 'secondary halogenoalkane', 'tertiary halogenoalkane', 'quaternary halogenoalkane'], f'{nm}: {cls}.')


@t15a.add('C3', (2, 3, 4, 5), 'short')
def t15a_make(r, D):
    route = r.choice([('ethanol', 'bromoethane', 'NaBr and concentrated H₂SO₄, heat', 'C₂H₅OH + HBr → C₂H₅Br + H₂O'), ('propan-1-ol', '1-chloropropane', 'PCl₅ at room temperature', 'CH₃CH₂CH₂OH + PCl₅ → CH₃CH₂CH₂Cl + POCl₃ + HCl'),
                      ('propene', '2-bromopropane', 'HBr(g) at room temperature', 'CH₂=CHCH₃ + HBr → CH₃CHBrCH₃'), ('ethane', 'bromoethane', 'Br₂ in UV light', 'C₂H₆ + Br₂ → C₂H₅Br + HBr'),
                      ('2-methylpropan-2-ol', '2-chloro-2-methylpropane', 'concentrated HCl, shaken at room temperature', '(CH₃)₃COH + HCl → (CH₃)₃CCl + H₂O'), ('ethene', 'bromoethane', 'HBr(g) at room temperature', 'CH₂=CH₂ + HBr → CH₃CH₂Br'),
                      ('butan-1-ol', '1-chlorobutane', 'SOCl₂', 'CH₃CH₂CH₂CH₂OH + SOCl₂ → CH₃CH₂CH₂CH₂Cl + SO₂ + HCl'), ('propan-2-ol', '2-bromopropane', 'NaBr and concentrated H₂SO₄, heat', 'CH₃CH(OH)CH₃ + HBr → CH₃CHBrCH₃ + H₂O')])
    s, p, cond, eq = route
    cls = HALO.get(p, (None, {'1-chlorobutane': 'primary'}.get(p, 'primary')))[1]
    stem = f'State the reagents and conditions to convert {s} into {p}, and write an equation.'
    key = f'reagents/conditions: {cond} [1]; equation {eq} [1]'
    if D >= 4:
        stem += ' Classify the product as primary, secondary or tertiary, explaining your answer.'
        key += f'; {cls} with reason [1]'
    return {'stem': stem, 'answer': f'{cond}; {eq}' + (f'; {cls}' if D >= 4 else ''), 'key': key}


def t15a_c4(r, D):
    nm = r.choice(['2-bromopropane', 'bromoethane', '2-bromo-2-methylpropane', '1-bromobutane'])
    f, cls = HALO[nm][0], HALO[nm][1]
    src = {'2-bromopropane': ('propene', 'propan-2-ol'), 'bromoethane': ('ethene', 'ethanol'), '2-bromo-2-methylpropane': ('2-methylpropene', '2-methylpropan-2-ol'), '1-bromobutane': ('but-1-ene (minor product only)', 'butan-1-ol')}[nm]
    intro = P(r, r.choice([f'{{p}} needs a sample of {nm}, {f}, for a synthesis in {{lab}}.', f'A pharmaceutical company in {{c}} uses {nm}, {f}, as an intermediate.']))
    parts = [
        lambda r: ('Classify the halogenoalkane and explain your answer.', f'{cls}: the C–Br carbon is bonded to {"one" if cls == "primary" else "two" if cls == "secondary" else "three"} other carbon atom(s).', '[2]'),
        lambda r: (f'Describe how it could be made from {src[1]}.', 'Heat with NaBr and concentrated H₂SO₄ (HBr formed in situ).', '[2]'),
        lambda r: (f'Explain whether {src[0]} would be a good starting material.', 'Addition of HBr: ' + ('gives this as the major product (Markovnikov).' if nm in ('2-bromopropane', '2-bromo-2-methylpropane') else 'only product.' if nm == 'bromoethane' else '1-bromobutane is only a minor product, so not suitable.'), '[2]'),
        lambda r: ('Explain why making it from an alkane and bromine in UV light is less suitable.', 'Mixture of products from further substitution/different positions; low yield.', '[2]'),
        (lambda r: ('Write the structural formula of an isomer that is a primary halogenoalkane.' if cls != 'primary' else 'Write the structural formula of an isomer that is a secondary halogenoalkane.', {'2-bromopropane': '1-bromopropane, CH₃CH₂CH₂Br', 'bromoethane': '', '2-bromo-2-methylpropane': '1-bromo-2-methylpropane, (CH₃)₂CHCH₂Br, or 1-bromobutane', '1-bromobutane': '2-bromobutane, CH₃CHBrCH₂CH₃'}[nm], '[1]')) if nm != 'bromoethane' else None,
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t15a, t15a_c4)

# ---------------------------------------------------------- 15.2 nucleophilic substitution and elimination
t15b = topic('Nucleophilic substitution reactions with NaOH, KCN, NH3 and elimination with ethanolic NaOH', 'nucleophilic substitution reactions with naoh, kcn, nh3', 'elimination with ethanolic naoh')
t15b.fixed('C1', (1, 2), [
    ('What is formed when bromoethane is heated under reflux with aqueous sodium hydroxide?', 'ethanol', 'OH⁻ substitutes for Br⁻ (nucleophilic substitution).', ['ethene', 'ethylamine', 'propanenitrile']),
    ('What is formed when bromoethane is heated with sodium hydroxide dissolved in ethanol?', 'ethene', 'Elimination of HBr.', ['ethanol', 'ethanal', 'ethoxyethane only']),
    ('Why is the reaction of a halogenoalkane with KCN useful in synthesis?', 'it increases the length of the carbon chain by one', 'Nitrile can be hydrolysed to a carboxylic acid.', ['it removes the halogen as a gas', 'it produces an alkene', 'it shortens the carbon chain']),
    ('What conditions are needed to make an amine from a halogenoalkane?', 'excess ammonia in ethanol, heated in a sealed tube', 'Excess NH₃ reduces further substitution.', ['dilute ammonia at room temperature', 'ammonium chloride and acid', 'nitrogen gas with a catalyst']),
    ('In the reaction of 1-bromopropane with KCN, which species is the nucleophile?', 'CN⁻', 'Cyanide lone pair attacks δ+ carbon.', ['K⁺', 'Br⁻', 'ethanol']),
    ('Name the organic product of the reaction of 1-bromopropane with KCN in ethanol.', 'Butanenitrile, CH₃CH₂CH₂CN.', '[1]'),
])
t15b.fixed('C2', (2, 3, 4), [
    ('Explain why excess ammonia is used when making ethylamine from bromoethane.', 'Ethylamine is itself a nucleophile and can react further with bromoethane to form secondary and tertiary amines; excess NH₃ makes reaction with ammonia more likely.', 'amine product is also a nucleophile [1]; excess NH₃ minimises further substitution [1]'),
    ('Explain why the solvent determines whether substitution or elimination occurs with NaOH.', 'In water OH⁻ acts mainly as a nucleophile (substitution, alcohol); in ethanol OH⁻ acts mainly as a base, removing H⁺ (elimination, alkene).', 'aqueous: nucleophile, substitution [1]; ethanolic: base, elimination [1]'),
    ('Explain why 2-bromobutane gives three different alkenes on elimination.', 'H can be removed from C1 (giving but-1-ene) or C3 (giving but-2-ene), and but-2-ene exists as cis and trans isomers.', 'H removed from either adjacent carbon [1]; but-2-ene has cis/trans [1]'),
])
errs(t15b, [
    ('Heating bromoethane with KCN gives ethanenitrile.', 'The CN group adds a carbon: the product is propanenitrile, CH₃CH₂CN.'),
    ('Ethanolic NaOH converts halogenoalkanes into alcohols.', 'In ethanol, OH⁻ acts as a base and the product is an alkene (elimination); aqueous NaOH gives alcohols.'),
])
c2mix(t15b, ['{p} carries out reactions of halogenoalkanes with nucleophiles in {lab}.', 'An organic chemist in {c} uses halogenoalkanes to build larger molecules.'])


@t15b.add('C1', (1, 2, 3))
def t15b_prod(r, D):
    nm = r.choice(list(HALO))
    h = HALO[nm]
    reag = r.choice(['NaOH(aq)', 'KCN', 'NH3', 'NaOH(eth)'] if 'none' not in h[5] else ['NaOH(aq)', 'KCN', 'NH3'])
    corr = {'NaOH(aq)': h[2], 'KCN': h[3][0], 'NH3': h[4], 'NaOH(eth)': h[5]}[reag]
    return mc(r, f'What is the organic product when {nm}, {h[0]}, reacts with {HCOND[reag]}?', corr, [h[2], h[3][0], h[4], h[5], r.choice([x[2] for x in HALO.values()])], f'{HCOND[reag]}: {corr}.')


@t15b.add('C3', (2, 3, 4, 5), 'short')
def t15b_rx(r, D):
    nm = r.choice(list(HALO))
    h = HALO[nm]
    reag = r.choice(['NaOH(aq)', 'KCN', 'NH3', 'NaOH(eth)'] if 'none' not in h[5] else ['NaOH(aq)', 'KCN', 'NH3'])
    prod = {'NaOH(aq)': h[2], 'KCN': f'{h[3][0]} ({h[3][1]})', 'NH3': h[4], 'NaOH(eth)': h[5]}[reag]
    ty = 'elimination' if reag == 'NaOH(eth)' else 'nucleophilic substitution'
    stem = f'{nm.capitalize()}, {h[0]}, is treated with {HCOND[reag]}. Name the organic product and the type of reaction.'
    key = f'product {prod} [1]; {ty} [1]'
    if D >= 4:
        stem += ' State the role of the inorganic reagent and explain why the carbon attached to the halogen is attacked.' if ty != 'elimination' else ' Explain the role of the hydroxide ion in this reaction.'
        key += '; nucleophile donates lone pair to δ+ carbon (C–X polar) [1]' if ty != 'elimination' else '; OH⁻ acts as a base, removing H⁺ from the carbon adjacent to C–X [1]'
    if D >= 5 and reag == 'KCN':
        stem += ' Suggest how the product could be converted into a carboxylic acid.'
        key += '; heat under reflux with dilute HCl (hydrolysis) [1]'
    return {'stem': stem, 'answer': f'{prod}; {ty}', 'key': key}


@t15b.add('C3', (3, 4, 5), 'numerical')
def t15b_yield(r, D):
    nm = r.choice(['1-bromobutane', '2-bromopropane', 'bromoethane', '1-bromopropane', '2-bromobutane'])
    h = HALO[nm]
    Mh = Mr(h[0].translate(str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')).replace('(', '').replace(')', '').replace('CH3', 'CH3'))
    prod = h[2]
    pf = ORG[prod][0]
    Mp = Mr(pf.replace('=', ''))
    m = r.choice([5.00, 6.85, 8.22, 10.0, 12.3])
    y = r.choice([0.55, 0.6, 0.65, 0.72, 0.8])
    mp = m / Mh * Mp * y
    mp = round(mp, 2)
    y = mp / (m / Mh * Mp)
    return {'stem': f'{who(r)} heats {m:.2f} g of {nm} under reflux with aqueous sodium hydroxide and obtains {mp:.2f} g of {prod}. Calculate the percentage yield.',
            'answer': f'{g3(y * 100)}%', 'key': f'Mr {nm} = {mr1(Mh)}, n = {g3(m / Mh)} mol [1]; theoretical mass {prod} = {g3(m / Mh * Mp)} g (Mr {mr1(Mp)}) [1]; % yield = {g3(y * 100)}% [1]'}


def t15b_c4(r, D):
    nm = r.choice(['1-bromopropane', '2-bromobutane', 'bromoethane', '2-bromopropane'])
    h = HALO[nm]
    intro = P(r, r.choice([f'{{p}} reacts {nm}, {h[0]}, separately with four reagents in {{lab}}.', f'A synthetic chemist in {{c}} uses {nm} as a starting material.']))
    parts = [
        lambda r: ('Name the product with hot aqueous NaOH and the type of reaction.', f'{h[2]}; nucleophilic substitution', '[2]'),
        lambda r: ('Name the product with KCN in ethanol and explain its importance in synthesis.', f'{h[3][0]}; increases carbon chain length by one', '[2]'),
        lambda r: ('State the conditions to make an amine and name the amine formed.', f'{HCOND["NH3"]}; {h[4]}', '[2]'),
        lambda r: ('Name the product(s) with hot ethanolic NaOH and state the role of OH⁻.', f'{h[5]}; base', '[2]'),
        lambda r: ('Explain why the C–Br carbon is attacked by nucleophiles.', 'Br more electronegative so C is δ+.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t15b, t15b_c4)

# ---------------------------------------------------------- 15.3 SN1 / SN2 and reactivity
t15c = topic('SN1 and SN2 mechanisms and relative reactivity linked to C–X bond strength', 'sn1 and sn2 mechanisms', 'c–x bond strength')
t15c.fixed('C1', (1, 2), [
    ('Which type of halogenoalkane reacts mainly by the SN1 mechanism?', 'tertiary', 'Stable tertiary carbocation forms; steric hindrance prevents backside attack.', ['primary', 'methyl', 'none — all react by SN2']),
    ('What does the "2" in SN2 mean?', 'two species are involved in the rate-determining step', 'Bimolecular: halogenoalkane and nucleophile.', ['two products form', 'there are two steps', 'two halogen atoms are replaced']),
    ('Which halogenoalkane is hydrolysed fastest by water?', '1-iodobutane', 'C–I is the weakest bond (240 kJ mol⁻¹), broken most easily.', ['1-chlorobutane', '1-bromobutane', '1-fluorobutane']),
    ('In the hydrolysis of halogenoalkanes by aqueous silver nitrate in ethanol, which precipitate appears first?', 'yellow silver iodide', 'C–I breaks fastest, releasing I⁻ first.', ['white silver chloride', 'cream silver bromide', 'all appear together']),
    ('What intermediate is formed in an SN1 reaction?', 'a carbocation', 'Rate-determining step: C–X breaks heterolytically.', ['a free radical', 'a carbanion', 'a transition state only']),
    ('State the factor that mainly determines the rate of hydrolysis of 1-chlorobutane, 1-bromobutane and 1-iodobutane.', 'The strength of the C–X bond (C–I weakest, fastest).', '[1]'),
])
t15c.fixed('C2', (2, 3, 4), [
    ('Explain why the rate of hydrolysis of halogenoalkanes depends on bond strength rather than bond polarity.', 'Although C–Cl is the most polar, the C–I bond is much weaker (240 vs 340 kJ mol⁻¹), and breaking the C–X bond is needed in the slow step, so iodoalkanes react fastest.', 'C–I weakest bond [1]; bond breaking controls rate despite lower polarity [1]'),
    ('Explain why tertiary halogenoalkanes react by SN1 rather than SN2.', 'Three bulky alkyl groups hinder backside attack by the nucleophile, and they stabilise the tertiary carbocation by electron donation.', 'steric hindrance [1]; stable tertiary carbocation [1]'),
    ('Describe the SN2 mechanism for the reaction of OH⁻ with bromoethane.', 'OH⁻ lone pair attacks the δ+ carbon from the side opposite Br; a five-coordinate transition state forms as C–Br breaks; Br⁻ leaves, giving ethanol.', 'attack on δ+ C opposite Br [1]; transition state and Br⁻ leaves [1]'),
])
errs(t15c, [
    ('Chloroalkanes hydrolyse fastest because the C–Cl bond is the most polar.', 'Iodoalkanes are fastest: the C–I bond is weakest, which outweighs its lower polarity.'),
    ('SN1 reactions involve a single step.', 'SN1 has two steps: slow formation of a carbocation, then fast attack by the nucleophile; "1" means one species in the rate-determining step.'),
])
c2mix(t15c, ['{p} compares the rates of hydrolysis of halogenoalkanes using silver nitrate in {lab}.', 'A student in {c} compares SN1 and SN2 mechanisms.'])


@t15c.add('C2', (2, 3, 4), 'explain')
def t15c_rate(r, D):
    chain = r.choice(['butane', 'propane', 'ethane'])
    pre = {'butane': '1-{}butane', 'propane': '1-{}propane', 'ethane': '{}ethane'}[chain]
    a, b = r.sample(['Cl', 'Br', 'I'], 2)
    na = pre.format({'Cl': 'chloro', 'Br': 'bromo', 'I': 'iodo'}[a])
    nb = pre.format({'Cl': 'chloro', 'Br': 'bromo', 'I': 'iodo'}[b])
    fast = a if CX[a] < CX[b] else b
    nf = na if fast == a else nb
    col = {'Cl': 'white', 'Br': 'cream', 'I': 'yellow'}
    return {'stem': f'{person(r)} adds aqueous silver nitrate in ethanol to separate tubes of {na} and {nb} at 50 °C. Predict which tube forms a precipitate first, state its colour and explain.',
            'answer': f'{nf}: {col[fast]} precipitate of Ag{fast} first, because the C–{fast} bond ({CX[fast]} kJ mol⁻¹) is weaker than C–{b if fast == a else a} ({CX[b if fast == a else a]} kJ mol⁻¹) so it is hydrolysed faster, releasing {fast}⁻ ions.',
            'key': 'correct tube [1]; colour [1]' + ('; weaker C–X bond, hydrolysis faster [1]' if D >= 3 else '')}


@t15c.add('C3', (2, 3, 4, 5), 'short')
def t15c_mech(r, D):
    nm = r.choice(list(HALO))
    h = HALO[nm]
    mech = h[6]
    stem = f'State and explain which mechanism (SN1 or SN2) is most likely for the hydrolysis of {nm}, {h[0]}, by aqueous hydroxide ions.'
    key = f'{mech} [1]; reason: {h[1]} — ' + ('little steric hindrance, carbocation unstable [1]' if mech == 'SN2' else 'stable tertiary carbocation/steric hindrance [1]' if mech == 'SN1' else 'intermediate: both possible [1]')
    if D >= 4:
        stem += ' Describe the mechanism using curly arrows in words.'
        key += ('; OH⁻ attacks δ+ C opposite X, transition state, X⁻ leaves [1]' if 'SN2' in mech else '; C–X breaks heterolytically to carbocation (slow), OH⁻ attacks carbocation (fast) [1]')
    return {'stem': stem, 'answer': f'{mech}', 'key': key}


def t15c_c4(r, D):
    a, b = r.choice([('1-bromobutane', '2-bromo-2-methylpropane'), ('bromoethane', '2-chloro-2-methylpropane'), ('1-iodobutane', '1-bromobutane')])
    intro = P(r, r.choice([f'{{p}} compares the hydrolysis of {a} and {b} in {{lab}}.', f'A kinetics study in {{c}} compares {a} and {b}.']))
    parts = [
        lambda r: (f'State the mechanism by which each compound is hydrolysed.', f'{a}: {HALO[a][6]}; {b}: {HALO[b][6]}', '[2]'),
        lambda r: ('Describe the SN2 mechanism with OH⁻.', 'OH⁻ attacks δ+ C opposite X; transition state; X⁻ leaves.', '[3]'),
        lambda r: ('Describe the SN1 mechanism.', 'Slow heterolytic fission to carbocation; fast attack by OH⁻.', '[2]'),
        lambda r: ('Explain the effect of the halogen on the rate of hydrolysis.', 'C–I < C–Br < C–Cl bond strength; weaker bond hydrolysed faster.', '[2]'),
        lambda r: ('Describe how the rates could be compared experimentally.', 'Add AgNO₃ in ethanol at the same temperature; time for precipitate to appear.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t15c, t15c_c4)

CHAPTERS[15] = [t15a, t15b, t15c]

# ===================================================================== Ch16 Alcohols, esters and carboxylic acids
# name: (structural formula ASCII, class, carbonyl from oxidation, acid from reflux oxidation, alkenes on dehydration, iodoform +)
ALC16 = {
    'methanol': ('CH3OH', 'primary', 'methanal', 'methanoic acid', [], False),
    'ethanol': ('CH3CH2OH', 'primary', 'ethanal', 'ethanoic acid', ['ethene'], True),
    'propan-1-ol': ('CH3CH2CH2OH', 'primary', 'propanal', 'propanoic acid', ['propene'], False),
    'propan-2-ol': ('CH3CH(OH)CH3', 'secondary', 'propanone', None, ['propene'], True),
    'butan-1-ol': ('CH3CH2CH2CH2OH', 'primary', 'butanal', 'butanoic acid', ['but-1-ene'], False),
    'butan-2-ol': ('CH3CH(OH)CH2CH3', 'secondary', 'butanone', None, ['but-1-ene', 'cis-but-2-ene', 'trans-but-2-ene'], True),
    '2-methylpropan-1-ol': ('(CH3)2CHCH2OH', 'primary', '2-methylpropanal', '2-methylpropanoic acid', ['2-methylpropene'], False),
    '2-methylpropan-2-ol': ('(CH3)3COH', 'tertiary', None, None, ['2-methylpropene'], False),
    'pentan-2-ol': ('CH3CH(OH)CH2CH2CH3', 'secondary', 'pentan-2-one', None, ['pent-1-ene', 'cis-pent-2-ene', 'trans-pent-2-ene'], True),
    'pentan-3-ol': ('CH3CH2CH(OH)CH2CH3', 'secondary', 'pentan-3-one', None, ['cis-pent-2-ene', 'trans-pent-2-ene'], False),
    '2-methylbutan-2-ol': ('(CH3)2C(OH)CH2CH3', 'tertiary', None, None, ['2-methylbut-1-ene', '2-methylbut-2-ene'], False),
}
FORM16 = {k: v[0] for k, v in ORG.items()}
FORM16.update({k: v[0] for k, v in ALC16.items()})
FORM16.update({'pentanal': 'CH3CH2CH2CH2CHO', 'pentan-1-ol': 'CH3CH2CH2CH2CH2OH', '1-bromopropane': 'CH3CH2CH2Br', '2-hydroxypropanoic acid': 'CH3CH(OH)COOH',
               '2-hydroxybutanenitrile': 'CH3CH2CH(OH)CN', '2-hydroxybutanoic acid': 'CH3CH2CH(OH)COOH', '2-hydroxy-2-methylpropanoic acid': '(CH3)2C(OH)COOH',
               'methyl propanoate': 'CH3CH2COOCH3', 'propylamine': 'CH3CH2CH2NH2', 'butanoic acid': 'CH3CH2CH2COOH', 'pent-1-ene': 'CH2=CHCH2CH2CH3',
               '2-methylbut-1-ene': 'CH2=C(CH3)CH2CH3', 'ethane-1,2-diol': 'HOCH2CH2OH'})


def SF16(name):
    return F(FORM16[name])


def MF16(name):
    return F(fstr(atoms(FORM16[name].replace('=', '').replace('≡', ''))))


def M16(name):
    return Mr(FORM16[name].replace('=', '').replace('≡', ''))


DHC16 = {'methanol': -726, 'ethanol': -1367, 'propan-1-ol': -2021, 'butan-1-ol': -2676, 'pentan-1-ol': -3329}
NC16 = {'methanol': 1, 'ethanol': 2, 'propan-1-ol': 3, 'butan-1-ol': 4, 'pentan-1-ol': 5, 'propan-2-ol': 3, 'butan-2-ol': 4, '2-methylpropan-2-ol': 4, 'pentan-2-ol': 5}
ALKOX = {'methanol': 'sodium methoxide, CH₃O⁻Na⁺', 'ethanol': 'sodium ethoxide, CH₃CH₂O⁻Na⁺', 'propan-1-ol': 'sodium propoxide, CH₃CH₂CH₂O⁻Na⁺', 'butan-1-ol': 'sodium butoxide, CH₃CH₂CH₂CH₂O⁻Na⁺'}


def alc_comb(name):
    n = NC16[name]
    return f'{MF16(name)} + {frac(1.5 * n)}O₂ → {n if n > 1 else ""}CO₂ + {n + 1}H₂O'


t16a = topic('Alcohols: preparation, combustion and reaction with sodium; classification as primary, secondary and tertiary', 'alcohols: preparation, combustion and reaction with sodium')
t16a.fixed('C1', (1, 2), [
    ('Which conditions are used in the industrial hydration of ethene to make ethanol?', 'steam with a phosphoric acid catalyst, about 300 °C and 6 MPa', 'CH₂=CH₂ + H₂O ⇌ CH₃CH₂OH.', ['aqueous NaOH at room temperature', 'hydrogen with a nickel catalyst at 150 °C', 'bromine water in the dark']),
    ('What are the products when ethanol reacts with sodium?', 'sodium ethoxide and hydrogen', '2CH₃CH₂OH + 2Na → 2CH₃CH₂O⁻Na⁺ + H₂.', ['sodium hydroxide and ethene', 'sodium ethanoate and water', 'ethane and sodium oxide']),
    ('Which alcohol is tertiary?', '2-methylpropan-2-ol', 'The C–OH carbon is bonded to three other carbon atoms.', ['butan-2-ol', '2-methylpropan-1-ol', 'butan-1-ol']),
    ('How is an alcohol made from a halogenoalkane?', 'by heating under reflux with aqueous sodium hydroxide', 'Nucleophilic substitution: RX + OH⁻ → ROH + X⁻.', ['by heating with ethanolic sodium hydroxide', 'by adding acidified dichromate(VI)', 'by shaking with bromine water']),
    ('What is observed when a small piece of sodium is added to ethanol?', 'the sodium fizzes slowly as hydrogen is given off and gradually disappears', 'Slower than with water because the O–H bond in ethanol is less polar.', ['a white precipitate forms immediately', 'the solution turns from orange to green', 'a silver mirror forms']),
    ('Why does propan-1-ol have a higher boiling point than butane, which has a similar Mr?', 'there is hydrogen bonding between propan-1-ol molecules', 'Hydrogen bonds between –OH groups are stronger than the instantaneous dipole forces in butane.', ['propan-1-ol has stronger covalent bonds', 'butane molecules are polar', 'propan-1-ol has more electrons']),
    ('Define a secondary alcohol.', 'An alcohol in which the carbon bonded to –OH is attached to two other carbon atoms.', '[1]'),
    ('Write the equation for the complete combustion of ethanol.', 'C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O', '[1]'),
])
t16a.fixed('C2', (2, 3, 4), [
    ('Explain why sodium reacts less vigorously with ethanol than with water.', 'The ethyl group pushes electrons towards O, so the O–H bond in ethanol is less polar and H⁺ is less readily released than from water.', 'ethyl group electron-donating / O–H less polar [1]; H⁺ released less readily, slower reaction [1]'),
    ('Explain why the lower alcohols are soluble in water but the solubility falls as the chain gets longer.', 'The –OH group forms hydrogen bonds with water; longer hydrocarbon chains cannot hydrogen bond and disrupt water\'s hydrogen bonding, so solubility falls.', 'OH hydrogen bonds with water [1]; longer non-polar chain reduces solubility [1]'),
    ('Explain why ethanol is considered a useful fuel.', 'It burns completely to CO₂ and H₂O releasing a lot of energy per mole, and it can be made from renewable plant material (fermentation), although land is used to grow the crops.', 'exothermic combustion/clean products [1]; renewable source [1]'),
])
errs(t16a, [
    ('Butan-2-ol is a primary alcohol because the –OH group is on the second carbon.', 'The C–OH carbon is attached to two other carbon atoms, so butan-2-ol is a secondary alcohol.'),
    ('When sodium reacts with ethanol, the products are sodium hydroxide and ethane.', 'The products are sodium ethoxide and hydrogen: 2C₂H₅OH + 2Na → 2C₂H₅ONa + H₂.'),
    ('2-methylpropan-2-ol is a secondary alcohol because the –OH is on carbon 2.', 'The C–OH carbon is attached to three other carbons, so it is tertiary.'),
])
c2mix(t16a, ['{p} investigates the properties of alcohols in {lab}.', 'A fuel company in {c} is testing alcohols as fuels.'])


@t16a.add('C1', (1, 2, 3))
def t16a_class(r, D):
    nm = r.choice(list(ALC16))
    f, cls = ALC16[nm][0], ALC16[nm][1]
    if nm == 'methanol':
        return None
    return mc(r, f'Classify {nm}, {SF16(nm)}.', f'{cls} alcohol', ['primary alcohol', 'secondary alcohol', 'tertiary alcohol', 'quaternary alcohol'], f'{nm}: {cls} (count the carbons bonded to the C–OH carbon).')


@t16a.add('C1', (1, 2, 3))
def t16a_comb(r, D):
    nm = r.choice(list(DHC16))
    n = NC16[nm]
    corr = frac(1.5 * n)
    wrong = [frac(1.5 * n + 0.5), frac(1.5 * n - 0.5) if n > 1 else '2', frac(2 * n), frac(n + 0.5), str(n + 1)]
    return mc(r, f'In the balanced equation for the complete combustion of one mole of {nm}, how many moles of oxygen are needed?', corr, wrong, f'{alc_comb(nm)}.')


@t16a.add('C3', (2, 3, 4, 5), 'numerical')
def t16a_na(r, D):
    nm = r.choice(list(ALKOX))
    M = M16(nm)
    m = r.choice([0.92, 1.15, 1.38, 2.30, 1.60, 2.04, 0.64, 3.00, 1.85])
    n = m / M
    V = n / 2 * 24000
    stem = f'{who(r)} adds excess sodium to {m:.2f} g of {nm}. Calculate the volume of hydrogen, in cm³, produced at room temperature and pressure (molar gas volume 24.0 dm³ mol⁻¹).'
    key = f'2ROH + 2Na → 2RONa + H₂ [1]; n({nm}) = {m:.2f}/{mr1(M)} = {g3(n)} mol [1]; n(H₂) = {g3(n / 2)} mol, V = {g3(V)} cm³ [1]'
    ans = f'{g3(V)} cm³'
    if D >= 4:
        stem += ' Name the organic product.'
        key += f'; {ALKOX[nm].split(",")[0]} [1]'
        ans += f'; {ALKOX[nm]}'
    return {'stem': stem, 'answer': ans, 'key': key}


@t16a.add('C3', (2, 3, 4, 5), 'numerical')
def t16a_cal(r, D):
    nm = r.choice(list(DHC16))
    M = M16(nm)
    eff = r.choice([0.45, 0.5, 0.55, 0.6, 0.65, 0.7])
    mw = r.choice([100, 150, 200, 250])
    dT = r.choice([14.5, 18.0, 21.5, 25.0, 28.5, 32.0])
    q = mw * 4.18 * dT
    ma = round(q / 1000 / (eff * -DHC16[nm]) * M, 2)
    if ma <= 0.05:
        return None
    n = ma / M
    dH = -q / 1000 / n
    stem = (f'{who(r)} burns {nm} in a spirit burner under a copper can containing {mw} g of water. The mass of the burner decreases by {ma:.2f} g and the temperature of the water rises by {dT} °C. '
            f'Calculate the enthalpy change of combustion of {nm} (c = 4.18 J g⁻¹ K⁻¹).')
    key = f'q = {mw} × 4.18 × {dT} = {g3(q)} J [1]; n = {ma:.2f}/{mr1(M)} = {g3(n)} mol [1]; ΔH = −{g3(q / 1000)}/{g3(n)} = {g3(dH)} kJ mol⁻¹ (negative sign) [1]'
    ans = f'{g3(dH)} kJ mol⁻¹'
    if D >= 4:
        stem += f' The data-book value is {sgn(DHC16[nm])} kJ mol⁻¹. Suggest two reasons for the difference.'
        key += '; heat lost to the surroundings / can [1]; incomplete combustion or evaporation of alcohol [1]'
        ans += '; heat loss to surroundings; incomplete combustion'
    return {'stem': stem, 'answer': ans, 'key': key}


@t16a.add('C3', (2, 3, 4, 5), 'short')
def t16a_prep(r, D):
    route = r.choice([
        ('ethene', 'ethanol', 'steam, H₃PO₄ catalyst, 300 °C, 6 MPa', 'CH₂=CH₂ + H₂O → CH₃CH₂OH', 'electrophilic addition (hydration)'),
        ('propene', 'propan-2-ol', 'steam, H₃PO₄ catalyst, 300 °C, 6 MPa', 'CH₂=CHCH₃ + H₂O → CH₃CH(OH)CH₃', 'electrophilic addition (hydration)'),
        ('bromoethane', 'ethanol', 'NaOH(aq), heat under reflux', 'CH₃CH₂Br + NaOH → CH₃CH₂OH + NaBr', 'nucleophilic substitution'),
        ('1-bromopropane', 'propan-1-ol', 'NaOH(aq), heat under reflux', 'CH₃CH₂CH₂Br + NaOH → CH₃CH₂CH₂OH + NaBr', 'nucleophilic substitution'),
        ('2-bromo-2-methylpropane', '2-methylpropan-2-ol', 'NaOH(aq), warm', '(CH₃)₃CBr + NaOH → (CH₃)₃COH + NaBr', 'nucleophilic substitution'),
        ('propanone', 'propan-2-ol', 'NaBH₄ in aqueous/alcoholic solution', 'CH₃COCH₃ + 2[H] → CH₃CH(OH)CH₃', 'reduction'),
        ('ethanal', 'ethanol', 'NaBH₄ in aqueous/alcoholic solution', 'CH₃CHO + 2[H] → CH₃CH₂OH', 'reduction'),
        ('ethene', 'ethane-1,2-diol', 'cold, dilute, acidified KMnO₄', 'CH₂=CH₂ + [O] + H₂O → HOCH₂CH₂OH', 'oxidation'),
    ])
    s, p, cond, eq, typ = route
    cls = ALC16.get(p, (None, 'primary (diol)'))[1]
    stem = f'Give the reagents and conditions for making {p} from {s}, and write an equation for the reaction.'
    key = f'{cond} [1]; {eq} [1]'
    ans = f'{cond}; {eq}'
    if D >= 3:
        stem += ' State the type of reaction.'
        key += f'; {typ} [1]'
        ans += f'; {typ}'
    if D >= 5 and p != 'ethane-1,2-diol':
        stem += ' Classify the alcohol formed.'
        key += f'; {cls} [1]'
        ans += f'; {cls}'
    return {'stem': stem, 'answer': ans, 'key': key}


def t16a_c4(r, D):
    nm = r.choice(['ethanol', 'propan-1-ol', 'butan-1-ol', 'methanol'])
    M = M16(nm)
    intro = P(r, r.choice([f'{{p}} studies {nm}, {SF16(nm)}, in {{lab}}.', f'A biofuel producer in {{c}} makes {nm}, {SF16(nm)}, for blending with petrol.']))
    m = r.choice([1.20, 1.50, 2.40, 0.80])
    parts = [
        lambda r: ('Classify the alcohol and explain your answer.', f'{ALC16[nm][1]}: the C–OH carbon is bonded to {"no other" if nm == "methanol" else "one other"} carbon atom' + (' (methanol is treated as primary).' if nm == 'methanol' else '.'), '[2]'),
        lambda r: ('Write an equation for its complete combustion.', alc_comb(nm), '[1]'),
        lambda r: (f'Calculate the volume of hydrogen at r.t.p. formed when {m:.2f} g reacts with excess sodium.', f'n = {m:.2f}/{mr1(M)} = {g3(m / M)} mol; n(H₂) = {g3(m / M / 2)} mol; V = {g3(m / M / 2 * 24.0)} dm³', '[3]'),
        lambda r: ('Name the organic product with sodium.', ALKOX[nm], '[1]'),
        lambda r: ('Explain why it is miscible with water.', 'The –OH group forms hydrogen bonds with water molecules.', '[1]'),
        lambda r: ('Suggest one environmental advantage of using it as a fuel.' if nm != 'methanol' else 'State one hazard of methanol as a fuel.', 'It can be made from renewable biomass, so it is closer to carbon neutral.' if nm != 'methanol' else 'It is toxic and its flame is almost invisible.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t16a, t16a_c4)

# ---------------------------------------------------------- 16.2 oxidation and dehydration
t16b = topic('Oxidation of alcohols with acidified dichromate(VI) and dehydration to alkenes', 'oxidation of alcohols with acidified dichromate(vi)', 'dehydration to alkenes')
t16b.fixed('C1', (1, 2), [
    ('What colour change is seen when propan-2-ol is warmed with acidified potassium dichromate(VI)?', 'orange to green', 'Cr₂O₇²⁻ (orange) is reduced to Cr³⁺ (green).', ['green to orange', 'purple to colourless', 'blue to brick red']),
    ('Which alcohol is not oxidised by acidified potassium dichromate(VI)?', '2-methylpropan-2-ol', 'Tertiary: no H on the C–OH carbon.', ['butan-2-ol', 'butan-1-ol', '2-methylpropan-1-ol']),
    ('How is an aldehyde, rather than a carboxylic acid, obtained from a primary alcohol?', 'by distilling the aldehyde off as soon as it forms', 'The aldehyde has a lower boiling point (no hydrogen bonding) and is removed before further oxidation.', ['by heating under reflux for a long time', 'by using excess dichromate(VI)', 'by adding sodium hydroxide']),
    ('Which catalyst can be used to dehydrate ethanol to ethene?', 'heated aluminium oxide', 'Alternatively concentrated H₂SO₄ or H₃PO₄ with heat.', ['nickel', 'iron', 'platinum at room temperature']),
    ('What type of reaction converts an alcohol into an alkene?', 'elimination (dehydration)', 'H₂O is removed from adjacent carbon atoms.', ['addition', 'substitution', 'reduction']),
    ('What is formed when propan-1-ol is heated under reflux with excess acidified potassium dichromate(VI)?', 'propanoic acid', 'Full oxidation of a primary alcohol under reflux.', ['propanal', 'propanone', 'propene']),
    ('State the product of oxidising a secondary alcohol.', 'A ketone.', '[1]'),
])
t16b.fixed('C2', (2, 3, 4), [
    ('Explain why tertiary alcohols resist oxidation by acidified dichromate(VI).', 'The carbon bearing –OH has no hydrogen atom, so it cannot form C=O without breaking a C–C bond.', 'no H on the C–OH carbon [1]; C=O cannot form without breaking C–C [1]'),
    ('Explain why heating under reflux leads to a carboxylic acid from a primary alcohol.', 'Reflux returns the volatile aldehyde to the flask, so it stays in contact with excess oxidising agent and is oxidised further to the acid.', 'vapours condense and return [1]; aldehyde further oxidised by excess oxidant [1]'),
    ('Explain why dehydration of butan-2-ol gives more than one alkene.', 'Water can be lost with an H from C1 or C3, giving but-1-ene or but-2-ene; but-2-ene has cis and trans isomers, giving three alkenes.', 'H removed from either neighbouring carbon [1]; cis/trans but-2-ene [1]'),
])
errs(t16b, [
    ('Propan-2-ol is oxidised by acidified dichromate(VI) to propanoic acid.', 'Propan-2-ol is secondary, so it is oxidised only to the ketone propanone.'),
    ('During oxidation of an alcohol, acidified dichromate(VI) turns from green to orange.', 'The colour change is orange (Cr₂O₇²⁻) to green (Cr³⁺) because dichromate is reduced.'),
    ('To make ethanal, ethanol is heated under reflux with excess acidified dichromate(VI).', 'Reflux gives ethanoic acid; ethanal is made by distilling it off as it forms, using excess alcohol.'),
])
c2mix(t16b, ['{p} oxidises a series of alcohols in {lab}.', 'A perfume chemist in {c} uses oxidation and dehydration of alcohols.'])


def ox_eq(nm, full):
    f = SF16(nm)
    _, cls, carb, acid, _, _ = ALC16[nm]
    if cls == 'tertiary':
        return 'no reaction'
    if full and acid:
        return f'{f} + 2[O] → {SF16(acid)} + H₂O'
    return f'{f} + [O] → {SF16(carb)} + H₂O'


def dehyd_eq(nm):
    a = ALC16[nm][4][0]
    return f'{SF16(nm)} → {SF16(a.replace("cis-", "").replace("trans-", ""))} + H₂O'


@t16b.add('C1', (1, 2, 3))
def t16b_prod(r, D):
    nm = r.choice([k for k in ALC16 if k != 'methanol'])
    _, cls, carb, acid, alk, _ = ALC16[nm]
    mode = r.choice(['distil', 'reflux'])
    corr = 'no organic product (no reaction)' if cls == 'tertiary' else (acid if mode == 'reflux' and acid else carb)
    pool = [x for x in [carb, acid, 'no organic product (no reaction)', alk[0].replace('cis-', '').replace('trans-', '')] if x] + [ALC16[k][2] for k in ALC16 if ALC16[k][2]]
    cond = 'warmed with acidified K₂Cr₂O₇ and the product distilled off immediately' if mode == 'distil' else 'heated under reflux with excess acidified K₂Cr₂O₇'
    return mc(r, f'{cap(nm)} is {cond}. What is the organic product?', corr, pool, f'{nm} is {cls}: {ox_eq(nm, mode == "reflux")}.')


@t16b.add('C1', (1, 2, 3))
def t16b_alk(r, D):
    nm = r.choice([k for k in ALC16 if ALC16[k][4]])
    alk = ALC16[nm][4]
    n = len(alk)
    return mc(r, f'How many different alkenes (including stereoisomers) can form when {nm} is dehydrated?', str(n), ['1', '2', '3', '4', '5'], f'{nm} → {", ".join(alk)}.')


@t16b.add('C3', (2, 3, 4, 5), 'short')
def t16b_ox(r, D):
    nm = r.choice([k for k in ALC16 if k != 'methanol'])
    _, cls, carb, acid, alk, _ = ALC16[nm]
    stem = f'{who(r)} warms {nm}, {SF16(nm)}, with acidified potassium dichromate(VI). Describe what is observed and give the organic product(s) formed, with equations.'
    if cls == 'tertiary':
        key = 'tertiary alcohol [1]; no reaction: solution stays orange [1]'
        ans = 'Tertiary alcohol, not oxidised; the solution stays orange.'
    elif cls == 'secondary':
        key = f'orange → green [1]; {carb} [1]; {ox_eq(nm, False)} [1]'
        ans = f'Orange to green; {carb}; {ox_eq(nm, False)}'
    else:
        key = f'orange → green [1]; {carb} on distillation, {ox_eq(nm, False)} [1]; {acid} under reflux, {ox_eq(nm, True)} [1]'
        ans = f'Orange to green; distil: {carb}; reflux: {acid}'
    if D >= 4:
        stem += ' Identify the inorganic species responsible for the colour change.'
        key += '; Cr₂O₇²⁻ reduced to Cr³⁺ [1]' if cls != 'tertiary' else '; Cr₂O₇²⁻ remains (not reduced) [1]'
        ans += '; Cr₂O₇²⁻ → Cr³⁺' if cls != 'tertiary' else '; Cr₂O₇²⁻ unchanged'
    return {'stem': stem, 'answer': ans, 'key': key}


@t16b.add('C3', (2, 3, 4, 5), 'short')
def t16b_dehyd(r, D):
    nm = r.choice([k for k in ALC16 if ALC16[k][4]])
    alk = ALC16[nm][4]
    stem = f'{cap(nm)}, {SF16(nm)}, is passed over heated aluminium oxide. Name all the alkenes that could form and write an equation for the formation of one of them.'
    key = f'{", ".join(alk)} [{min(len(alk), 3)}]; {dehyd_eq(nm)} [1]'
    ans = f'{", ".join(alk)}; {dehyd_eq(nm)}'
    if D >= 4:
        stem += ' State the type of reaction.'
        key += '; elimination/dehydration [1]'
        ans += '; elimination (dehydration)'
    return {'stem': stem, 'answer': ans, 'key': key}


@t16b.add('C3', (3, 4, 5), 'numerical')
def t16b_yield(r, D):
    nm = r.choice(['ethanol', 'propan-1-ol', 'propan-2-ol', 'butan-2-ol', 'butan-1-ol'])
    _, cls, carb, acid, _, _ = ALC16[nm]
    prod = acid if (acid and r.random() < 0.5) else carb
    Ma, Mp = M16(nm), M16(prod)
    m = r.choice([4.60, 6.00, 7.40, 5.20, 9.25])
    y = r.choice([0.42, 0.55, 0.61, 0.68, 0.74])
    mp = m / Ma * Mp * y
    mp = round(mp, 2)
    y = mp / (m / Ma * Mp)
    return {'stem': f'{who(r)} oxidises {m:.2f} g of {nm} with acidified potassium dichromate(VI) and collects {mp:.2f} g of {prod}. Calculate the percentage yield.',
            'answer': f'{g3(y * 100)}%', 'key': f'n({nm}) = {m:.2f}/{mr1(Ma)} = {g3(m / Ma)} mol [1]; theoretical mass = {g3(m / Ma)} × {mr1(Mp)} = {g3(m / Ma * Mp)} g [1]; yield = {g3(y * 100)}% [1]'}


def t16b_c4(r, D):
    a, b = r.sample(['propan-1-ol', 'propan-2-ol', '2-methylpropan-2-ol', 'butan-1-ol', 'butan-2-ol'], 2)
    intro = P(r, r.choice([f'{{p}} is given two unlabelled alcohols, {a} and {b}, in {{lab}}.', f'A quality-control chemist in {{c}} must tell apart samples of {a} and {b}.']))
    parts = [
        lambda r: ('Classify each alcohol.', f'{a}: {ALC16[a][1]}; {b}: {ALC16[b][1]}', '[2]'),
        lambda r: (f'Describe the result of warming each with acidified potassium dichromate(VI).', '; '.join(f'{x}: ' + ('stays orange' if ALC16[x][1] == 'tertiary' else 'orange → green') for x in (a, b)), '[2]'),
        lambda r: (f'Give the organic product of oxidising {a} by distillation and write an equation.', ox_eq(a, False) if ALC16[a][1] != 'tertiary' else 'no reaction (tertiary)', '[2]'),
        lambda r: (f'Name the alkene(s) formed when {b} is dehydrated.', ', '.join(ALC16[b][4]), '[2]'),
        lambda r: ('Describe how the oxidation products of the two alcohols could be distinguished.', 'Aldehydes give a red-brown precipitate with warm Fehling\'s solution (or a silver mirror with Tollens\'); ketones do not; a tertiary alcohol gives no product.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t16b, t16b_c4)

# ---------------------------------------------------------- 16.3 carboxylic acids and esters
ACID_E = [('methanoic acid', 'HCOOH', 'methanoate', 'HCOO'), ('ethanoic acid', 'CH3COOH', 'ethanoate', 'CH3COO'), ('propanoic acid', 'CH3CH2COOH', 'propanoate', 'CH3CH2COO'), ('butanoic acid', 'CH3CH2CH2COOH', 'butanoate', 'CH3CH2CH2COO')]
ALC_E = [('methanol', 'CH3OH', 'methyl', 'CH3'), ('ethanol', 'CH3CH2OH', 'ethyl', 'CH2CH3'), ('propan-1-ol', 'CH3CH2CH2OH', 'propyl', 'CH2CH2CH3'), ('butan-1-ol', 'CH3CH2CH2CH2OH', 'butyl', 'CH2CH2CH2CH3')]


def ester(r):
    ac = r.choice(ACID_E)
    al = r.choice(ALC_E)
    return ac, al, f'{al[2]} {ac[2]}', ac[3] + al[3]


def est_eq(ac, al, ef):
    return f'{F(ac[1])} + {F(al[1])} ⇌ {F(ef)} + H₂O'


t16c = topic('Carboxylic acids and esterification; acid hydrolysis of esters', 'carboxylic acids and esterification', 'acid hydrolysis of esters')
t16c.fixed('C1', (1, 2), [
    ('What is the catalyst in the esterification of ethanoic acid with ethanol?', 'concentrated sulfuric acid', 'A few drops of conc H₂SO₄; the mixture is heated.', ['aqueous sodium hydroxide', 'nickel', 'aluminium oxide']),
    ('What is observed when ethanoic acid is added to sodium carbonate solution?', 'effervescence of carbon dioxide', '2CH₃COOH + Na₂CO₃ → 2CH₃COONa + CO₂ + H₂O.', ['a white precipitate', 'a silver mirror', 'an orange to green colour change']),
    ('Which compound is formed when butanenitrile is heated under reflux with dilute hydrochloric acid?', 'butanoic acid', 'CH₃CH₂CH₂CN + 2H₂O + HCl → CH₃CH₂CH₂COOH + NH₄Cl.', ['butan-1-ol', 'butanal', 'propanoic acid']),
    ('What are the products of the acid hydrolysis of methyl ethanoate?', 'ethanoic acid and methanol', 'CH₃COOCH₃ + H₂O ⇌ CH₃COOH + CH₃OH.', ['methanoic acid and ethanol', 'sodium ethanoate and methanol', 'ethanal and methanal']),
    ('Why is the acid hydrolysis of an ester incomplete?', 'the reaction is reversible and reaches equilibrium', 'Alkaline hydrolysis goes to completion because the carboxylate ion is formed.', ['the ester is insoluble', 'the acid catalyst is used up', 'the products are gases']),
    ('What gas is produced when magnesium reacts with propanoic acid?', 'hydrogen', 'Mg + 2CH₃CH₂COOH → (CH₃CH₂COO)₂Mg + H₂.', ['carbon dioxide', 'oxygen', 'methane']),
    ('Give the name of the salt formed when ethanoic acid reacts with sodium hydroxide.', 'Sodium ethanoate, CH₃COONa.', '[1]'),
])
t16c.fixed('C2', (2, 3, 4), [
    ('Explain why esters have lower boiling points than carboxylic acids of similar Mr.', 'Ester molecules have no O–H group, so they cannot hydrogen bond to each other; carboxylic acids form hydrogen bonds (dimers).', 'no H bonding between ester molecules [1]; acids hydrogen bond [1]'),
    ('Explain why alkaline hydrolysis of an ester goes to completion but acid hydrolysis does not.', 'In alkali the carboxylic acid is converted to a carboxylate ion, which cannot react with the alcohol, so the reverse reaction is removed; acid hydrolysis is a reversible equilibrium.', 'carboxylate ion formed / does not react with alcohol [1]; acid hydrolysis reversible [1]'),
    ('Explain why esterification is carried out with heating under reflux and concentrated sulfuric acid.', 'Reaction is slow: heat increases rate, reflux prevents loss of volatile reactants and products, and H₂SO₄ catalyses the reaction (and absorbs water, shifting the equilibrium right).', 'reflux keeps volatiles / heat increases rate [1]; catalyst (and dehydrating agent) [1]'),
])
errs(t16c, [
    ('Ethanoic acid and methanol react to form ethyl methanoate.', 'The alkyl part comes from the alcohol and the -oate part from the acid: the product is methyl ethanoate, CH₃COOCH₃.'),
    ('Esters are made by heating a carboxylic acid with an alcohol and aqueous sodium hydroxide.', 'A concentrated sulfuric acid catalyst is used; NaOH would hydrolyse the ester.'),
    ('Acid hydrolysis of ethyl ethanoate gives sodium ethanoate and ethanol.', 'Acid hydrolysis gives ethanoic acid and ethanol; sodium ethanoate forms in alkaline hydrolysis with NaOH.'),
])
c2mix(t16c, ['{p} makes esters for a fragrance project in {lab}.', 'A food flavouring company in {c} manufactures esters.'])


@t16c.add('C1', (1, 2, 3))
def t16c_name(r, D):
    ac, al, en, ef = ester(r)
    wrong = [f'{ac[2].replace("anoate", "yl")} {al[2].replace("yl", "anoate")}', f'{al[2]} {r.choice([a[2] for a in ACID_E if a != ac])}', f'{r.choice([a[2] for a in ALC_E if a != al])} {ac[2]}', f'{al[2]} {ac[0].split()[0]}']
    return mc(r, f'What is the name of the ester formed from {ac[0]} and {al[0]}?', en, wrong, f'{est_eq(ac, al, ef)}; alcohol → alkyl, acid → -oate.')


@t16c.add('C1', (1, 2, 3))
def t16c_hyd(r, D):
    ac, al, en, ef = ester(r)
    corr = f'{ac[0]} and {al[0]}'
    wrong = [f'{r.choice([a[0] for a in ACID_E if a != ac])} and {r.choice([a[0] for a in ALC_E if a != al])}', f'sodium {ac[2]} and {al[0]}', f'{ac[0]} only', f'{al[0]} and water']
    return mc(r, f'Which compounds are formed when {en}, {F(ef)}, is heated under reflux with dilute sulfuric acid?', corr, wrong, f'{F(ef)} + H₂O ⇌ {F(ac[1])} + {F(al[1])}.')


@t16c.add('C3', (2, 3, 4, 5), 'numerical')
def t16c_yield(r, D):
    ac, al, en, ef = ester(r)
    Ma, Me = Mr(ac[1]), Mr(ef)
    m = r.choice([3.00, 4.50, 6.00, 7.40, 8.80, 12.0])
    y = r.choice([0.45, 0.52, 0.6, 0.66, 0.7])
    me = m / Ma * Me * y
    me = round(me, 2)
    y = me / (m / Ma * Me)
    stem = f'{who(r)} heats {m:.2f} g of {ac[0]} with excess {al[0]} and a little concentrated sulfuric acid, and obtains {me:.2f} g of {en}. Calculate the percentage yield.'
    key = f'n(acid) = {m:.2f}/{mr1(Ma)} = {g3(m / Ma)} mol [1]; theoretical = {g3(m / Ma)} × {mr1(Me)} = {g3(m / Ma * Me)} g [1]; yield = {g3(y * 100)}% [1]'
    ans = f'{g3(y * 100)}%'
    if D >= 4:
        stem += ' Write the equation and suggest why the yield is less than 100%.'
        key += f'; {est_eq(ac, al, ef)} [1]; equilibrium/reversible reaction (or losses on purification) [1]'
        ans += f'; {est_eq(ac, al, ef)}; reversible reaction reaches equilibrium'
    return {'stem': stem, 'answer': ans, 'key': key}


@t16c.add('C3', (2, 3, 4, 5), 'numerical')
def t16c_titr(r, D):
    nm, f = r.choice([(a[0], a[1]) for a in ACID_E] + [('2-methylpropanoic acid', '(CH3)2CHCOOH')])
    M = Mr(f)
    c = r.choice([0.100, 0.120, 0.150, 0.200])
    v = r.choice([18.40, 21.60, 24.25, 26.80, 30.10])
    n = c * v / 1000
    m = round(n * M, 3)
    Mexp = m / n
    stem = (f'{who(r)} dissolves {m:.3f} g of an unknown saturated monocarboxylic acid, CₙH₂ₙ₊₁COOH, in water and titrates the whole solution with {c:.3f} mol dm⁻³ NaOH; {v:.2f} cm³ is required. '
            'Calculate the Mr of the acid and identify it.')
    key = f'n(NaOH) = n(acid) = {c:.3f} × {v:.2f}/1000 = {g3(n)} mol [1]; Mr = {m:.3f}/{g3(n)} = {g3(Mexp)} [1]; 14n + 46 = {g3(Mexp)} so n = {round((Mexp - 46) / 14)}: {"butanoic acid or 2-methylpropanoic acid" if "butanoic" in nm or "2-methyl" in nm else nm} [1]'
    ans = f'Mr ≈ {g3(Mexp)}; ' + ('butanoic acid (or 2-methylpropanoic acid)' if 'butanoic' in nm or '2-methyl' in nm else nm)
    return {'stem': stem, 'answer': ans, 'key': key}


@t16c.add('C3', (2, 3, 4, 5), 'short')
def t16c_rx(r, D):
    nm, f = r.choice([(a[0], a[1]) for a in ACID_E[1:]])
    rxs = [('sodium carbonate solution', 'effervescence (CO₂)', f'2{F(f)} + Na₂CO₃ → 2{F(f[:-1])}Na + CO₂ + H₂O'),
           ('magnesium ribbon', 'effervescence (H₂), magnesium dissolves', f'2{F(f)} + Mg → ({F(f[:-1])})₂Mg + H₂'),
           ('aqueous sodium hydroxide', 'no visible change (neutralisation, warms)', f'{F(f)} + NaOH → {F(f[:-1])}Na + H₂O')]
    k = 2 if D <= 3 else 3
    pick = r.sample(rxs, k)
    stem = f'{who(r)} adds {nm}, {F(f)}, separately to ' + ' and '.join(p[0] for p in pick) + '. For each, state what is observed and write an equation.'
    key = '; '.join(f'{p[0]}: {p[1]} [1]; {p[2]} [1]' for p in pick)
    ans = '; '.join(f'{p[0]}: {p[1]}, {p[2]}' for p in pick)
    return {'stem': stem, 'answer': ans, 'key': key}


def t16c_c4(r, D):
    ac, al, en, ef = ester(r)
    Me = Mr(ef)
    intro = P(r, r.choice([f'{{p}} makes the ester {en} in {{lab}}.', f'A flavour company in {{c}} produces {en} for fruit flavourings.']))
    parts = [
        lambda r: ('Name the carboxylic acid and alcohol needed and give the conditions.', f'{ac[0]} and {al[0]}; concentrated H₂SO₄ catalyst, heat under reflux', '[2]'),
        lambda r: ('Write an equation for the reaction.', est_eq(ac, al, ef), '[1]'),
        lambda r: ('Give the structural and molecular formulae of the ester.', f'{F(ef)}; {F(fstr(atoms(ef)))}', '[2]'),
        lambda r: (f'Calculate the Mr of {en}.', mr1(Me), '[1]'),
        lambda r: ('Describe the acid hydrolysis of the ester, including conditions and products.', f'Heat under reflux with dilute H₂SO₄/HCl; {ac[0]} and {al[0]}; reversible', '[2]'),
        lambda r: ('Give the products if the ester is instead heated with aqueous NaOH.', f'sodium {ac[2]} and {al[0]}', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t16c, t16c_c4)

# ---------------------------------------------------------- 16.4 iodoform
# name: (positive?, carboxylate formed, why)
IODO = {
    'ethanol': (True, 'methanoate, HCOO⁻', 'contains CH₃CH(OH)–'), 'methanol': (False, None, 'no CH₃CH(OH)– group'), 'propan-1-ol': (False, None, 'no CH₃CH(OH)– group'),
    'propan-2-ol': (True, 'ethanoate, CH₃COO⁻', 'contains CH₃CH(OH)–'), 'butan-1-ol': (False, None, 'no CH₃CH(OH)– group'), 'butan-2-ol': (True, 'propanoate, CH₃CH₂COO⁻', 'contains CH₃CH(OH)–'),
    '2-methylpropan-2-ol': (False, None, 'tertiary; no CH₃CH(OH)– group'), 'pentan-2-ol': (True, 'butanoate, CH₃CH₂CH₂COO⁻', 'contains CH₃CH(OH)–'), 'pentan-3-ol': (False, None, 'no CH₃CH(OH)– group'),
    'ethanal': (True, 'methanoate, HCOO⁻', 'contains CH₃CO–'), 'propanal': (False, None, 'no CH₃CO– group'), 'propanone': (True, 'ethanoate, CH₃COO⁻', 'contains CH₃CO–'),
    'butanone': (True, 'propanoate, CH₃CH₂COO⁻', 'contains CH₃CO–'), 'pentan-2-one': (True, 'butanoate, CH₃CH₂CH₂COO⁻', 'contains CH₃CO–'), 'pentan-3-one': (False, None, 'no CH₃CO– group'),
    'butanal': (False, None, 'no CH₃CO– group'), 'ethanoic acid': (False, None, 'the CH₃CO– is part of a carboxylic acid, which does not react'),
}
FORM16.update({'pentan-3-one': 'CH3CH2COCH2CH3', 'pentan-2-one': 'CH3COCH2CH2CH3'})
M_CHI3 = 12.0 + 1.0 + 3 * 126.9

t16d = topic('The tri-iodomethane (iodoform) reaction', 'the tri-iodomethane (iodoform) reaction', 'iodoform')
t16d.fixed('C1', (1, 2), [
    ('Which reagent is used for the tri-iodomethane (iodoform) test?', 'alkaline aqueous iodine (I₂ and NaOH(aq)), warmed', 'A pale yellow precipitate of CHI₃ indicates CH₃CO– or CH₃CH(OH)–.', ['acidified potassium dichromate(VI)', 'Tollens\' reagent', 'aqueous silver nitrate']),
    ('What is seen in a positive tri-iodomethane test?', 'a pale yellow precipitate with an antiseptic smell', 'The precipitate is CHI₃.', ['a silver mirror', 'a brick-red precipitate', 'an orange colour turning green']),
    ('Which compound gives a positive tri-iodomethane test?', 'propan-2-ol', 'Contains CH₃CH(OH)–, oxidised to CH₃CO– by the alkaline iodine.', ['propan-1-ol', 'methanol', 'pentan-3-one']),
    ('Which is the only aldehyde that gives a positive tri-iodomethane test?', 'ethanal', 'Ethanal is the only aldehyde with a CH₃CO– group.', ['methanal', 'propanal', 'butanal']),
    ('What is the formula of tri-iodomethane?', 'CHI₃', 'Iodoform.', ['CH₃I', 'CH₂I₂', 'CI₄']),
    ('Name the two structural groups that give a positive tri-iodomethane test.', 'CH₃CO– (methyl carbonyl) and CH₃CH(OH)– (secondary alcohol next to a methyl group, or ethanol).', '[2]'),
])
t16d.fixed('C2', (2, 3, 4), [
    ('Explain why ethanol gives a positive tri-iodomethane test even though it has no C=O group.', 'Alkaline iodine first oxidises ethanol, CH₃CH₂OH (which contains CH₃CH(OH)–), to ethanal, CH₃CHO, which contains CH₃CO– and then reacts.', 'oxidised by alkaline iodine [1]; to ethanal containing CH₃CO– [1]'),
    ('Explain how the tri-iodomethane test can distinguish butanone from pentan-3-one.', 'Butanone, CH₃COCH₂CH₃, contains CH₃CO– and gives a pale yellow precipitate; pentan-3-one, CH₃CH₂COCH₂CH₃, does not, so no precipitate forms.', 'butanone has CH₃CO–, yellow ppt [1]; pentan-3-one no CH₃CO–, no ppt [1]'),
])
errs(t16d, [
    ('Propan-1-ol gives a positive tri-iodomethane test because it is an alcohol.', 'Only alcohols with a CH₃CH(OH)– group react; propan-1-ol, CH₃CH₂CH₂OH, does not, so no precipitate forms.'),
    ('In the tri-iodomethane reaction, propanone forms CHI₃ and a carboxylate with three carbon atoms.', 'The CH₃ becomes CHI₃, so the carboxylate has one fewer carbon atom: ethanoate, CH₃COO⁻.'),
])
c2mix(t16d, ['{p} uses alkaline aqueous iodine to test organic liquids in {lab}.', 'A forensic laboratory in {c} uses the tri-iodomethane test.'], extra=[
    ('Give the structure of the organic ion formed, as well as CHI₃, when propanone reacts with alkaline iodine.', 'Ethanoate, CH₃COO⁻.', 'ethanoate CH₃COO⁻ [1]'),
])


@t16d.add('C1', (1, 2, 3))
def t16d_which(r, D):
    pos = [k for k, v in IODO.items() if v[0]]
    neg = [k for k, v in IODO.items() if not v[0]]
    if r.random() < 0.5:
        c = r.choice(pos)
        return mc(r, 'Which compound gives a pale yellow precipitate when warmed with alkaline aqueous iodine?', f'{c}, {SF16(c)}', [f'{k}, {SF16(k)}' for k in neg], f'{c} {IODO[c][2]}.')
    c = r.choice(neg)
    return mc(r, 'Which compound does NOT give a positive tri-iodomethane (iodoform) test?', f'{c}, {SF16(c)}', [f'{k}, {SF16(k)}' for k in pos], f'{c}: {IODO[c][2]}.')


@t16d.add('C1', (1, 2, 3))
def t16d_ion(r, D):
    c = r.choice([k for k, v in IODO.items() if v[0]])
    corr = IODO[c][1]
    pool = list({v[1] for v in IODO.values() if v[1]}) + ['ethanoate, CH₃COO⁻', 'pentanoate, CH₃CH₂CH₂CH₂COO⁻']
    return mc(r, f'{cap(c)} is warmed with alkaline aqueous iodine. Apart from CHI₃, which organic ion is formed?', corr, pool, f'The CH₃ of CH₃CO– becomes CHI₃; the carboxylate has one fewer carbon: {corr}.')


@t16d.add('C3', (2, 3, 4, 5), 'short')
def t16d_pred(r, D):
    c = r.choice(list(IODO))
    pos, ion_, why = IODO[c]
    stem = f'{who(r)} warms {c}, {SF16(c)}, with alkaline aqueous iodine. Predict what is observed and explain your answer.'
    if pos:
        key = f'pale yellow precipitate [1]; {why} [1]'
        ans = f'Pale yellow precipitate of CHI₃; {why}.'
        if D >= 4:
            stem += ' Name the organic products.'
            key += f'; CHI₃ and {ion_} [1]'
            ans += f' Products: CHI₃ and {ion_}.'
    else:
        key = f'no precipitate (no change) [1]; {why} [1]'
        ans = f'No yellow precipitate; {why}.'
        if D >= 4:
            stem += ' Suggest an isomer of it that would give a positive result.'
            alt = {'propan-1-ol': 'propan-2-ol', 'butan-1-ol': 'butan-2-ol', '2-methylpropan-2-ol': 'butan-2-ol', 'pentan-3-ol': 'pentan-2-ol', 'propanal': 'propanone', 'pentan-3-one': 'pentan-2-one', 'butanal': 'butanone', 'methanol': None, 'ethanoic acid': None}.get(c)
            if not alt:
                return None
            key += f'; {alt} [1]'
            ans += f' Isomer: {alt}.'
    return {'stem': stem, 'answer': ans, 'key': key}


@t16d.add('C3', (3, 4, 5), 'numerical')
def t16d_mass(r, D):
    c = r.choice(['propanone', 'butanone', 'ethanal', 'pentan-2-one'])
    M = M16(c)
    m = r.choice([0.580, 0.720, 0.440, 0.860, 1.16, 1.45])
    y = r.choice([0.6, 0.7, 0.75, 0.8, 0.85])
    mt = m / M * M_CHI3
    return {'stem': f'{who(r)} reacts {m:.3g} g of {c} with excess alkaline aqueous iodine. Each molecule gives one molecule of CHI₃. Calculate the mass of CHI₃ expected if the yield is {int(y * 100)}% (Ar: I = 126.9).',
            'answer': f'{g3(mt * y)} g', 'key': f'n({c}) = {m:.3g}/{mr1(M)} = {g3(m / M)} mol [1]; Mr CHI₃ = {mr1(M_CHI3)}, theoretical mass = {g3(mt)} g [1]; × {y} = {g3(mt * y)} g [1]'}


def t16d_c4(r, D):
    setx = r.choice([('C₃H₈O', ['propan-1-ol', 'propan-2-ol']), ('C₄H₈O', ['butanal', 'butanone']), ('C₅H₁₀O', ['pentan-2-one', 'pentan-3-one']), ('C₄H₁₀O', ['butan-1-ol', 'butan-2-ol', '2-methylpropan-2-ol'])])
    mf, cands = setx
    x = r.choice(cands)
    intro = P(r, f'{{p}} has an unknown compound X, {mf}, which is one of: {", ".join(cands)}. X gives {"a pale yellow precipitate" if IODO[x][0] else "no precipitate"} when warmed with alkaline aqueous iodine.')
    parts = [
        lambda r: ('Identify X and explain your answer.', f'{x}: {IODO[x][2]}', '[2]'),
        lambda r: ('Give the formula and colour of the precipitate formed in a positive test.', 'CHI₃, pale yellow', '[1]'),
        lambda r: ('Name the reagents used and state the conditions.', 'iodine and aqueous sodium hydroxide; warm', '[1]'),
        lambda r: (f'Give the structural formula of each candidate.', '; '.join(f'{k}: {SF16(k)}' for k in cands), f'[{len(cands)}]'),
        lambda r: ('Suggest one further test that would confirm the identity of X.', 'Aldehyde vs ketone: Fehling\'s/Tollens\'; alcohols: acidified dichromate (tertiary stays orange) or oxidation product tested with Fehling\'s.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t16d, t16d_c4)

CHAPTERS[16] = [t16a, t16b, t16c, t16d]

# ===================================================================== Ch17 Carbonyl compounds
# name: (kind, alcohol, HCN product name, HCN product formula, chiral product?)
CARB = {
    'ethanal': ('aldehyde', 'ethanol', '2-hydroxypropanenitrile', 'CH3CH(OH)CN', True),
    'propanal': ('aldehyde', 'propan-1-ol', '2-hydroxybutanenitrile', 'CH3CH2CH(OH)CN', True),
    'butanal': ('aldehyde', 'butan-1-ol', '2-hydroxypentanenitrile', 'CH3CH2CH2CH(OH)CN', True),
    '2-methylpropanal': ('aldehyde', '2-methylpropan-1-ol', '2-hydroxy-3-methylbutanenitrile', '(CH3)2CHCH(OH)CN', True),
    'pentanal': ('aldehyde', 'pentan-1-ol', '2-hydroxyhexanenitrile', 'CH3CH2CH2CH2CH(OH)CN', True),
    'propanone': ('ketone', 'propan-2-ol', '2-hydroxy-2-methylpropanenitrile', '(CH3)2C(OH)CN', False),
    'butanone': ('ketone', 'butan-2-ol', '2-hydroxy-2-methylbutanenitrile', 'CH3CH2C(CH3)(OH)CN', True),
    'pentan-2-one': ('ketone', 'pentan-2-ol', '2-hydroxy-2-methylpentanenitrile', 'CH3CH2CH2C(CH3)(OH)CN', True),
    'pentan-3-one': ('ketone', 'pentan-3-ol', '2-ethyl-2-hydroxybutanenitrile', '(CH3CH2)2C(OH)CN', False),
}
for _k, _v in CARB.items():
    FORM16[_v[2]] = _v[3]


def red_eq(c):
    return f'{SF16(c)} + 2[H] → {SF16(CARB[c][1])}'


t17a = topic('Aldehydes and ketones: preparation by oxidation and reduction with NaBH4', 'aldehydes and ketones: preparation by oxidation', 'reduction with nabh4')
t17a.fixed('C1', (1, 2), [
    ('Which reagent reduces propanone to propan-2-ol?', 'sodium tetrahydridoborate(III), NaBH₄', 'CH₃COCH₃ + 2[H] → CH₃CH(OH)CH₃.', ['acidified potassium dichromate(VI)', 'Fehling\'s solution', 'concentrated sulfuric acid']),
    ('Which alcohol is oxidised to make butanone?', 'butan-2-ol', 'Secondary alcohol → ketone.', ['butan-1-ol', '2-methylpropan-2-ol', 'butanoic acid']),
    ('What is formed when ethanal is reduced by NaBH₄?', 'ethanol', 'Aldehydes are reduced to primary alcohols.', ['ethanoic acid', 'ethane', 'ethene']),
    ('Which species from NaBH₄ acts as the nucleophile in the reduction of carbonyl compounds?', 'the hydride ion, H⁻', 'H⁻ attacks the δ+ carbonyl carbon.', ['H⁺', 'Na⁺', 'BH₃']),
    ('Which statement about aldehydes and ketones is correct?', 'both contain the C=O group', 'Aldehydes have C=O at the end of the chain (–CHO); ketones have C=O within the chain.', ['both contain an –OH group', 'ketones are oxidised by Tollens\' reagent', 'aldehydes have C=O within the carbon chain']),
    ('What type of alcohol is formed when a ketone is reduced?', 'A secondary alcohol.', '[1]'),
])
t17a.fixed('C2', (2, 3, 4), [
    ('Explain why aldehydes and ketones have lower boiling points than the alcohols from which they are made.', 'Carbonyls have permanent dipole–dipole forces but no O–H, so they cannot hydrogen bond with each other; alcohols do hydrogen bond.', 'no hydrogen bonding in carbonyls [1]; alcohols hydrogen bond, stronger forces [1]'),
    ('Explain why an aldehyde is distilled off as it forms during the oxidation of a primary alcohol.', 'The aldehyde is volatile (lower bp than alcohol) and is removed before it can be oxidised further to the carboxylic acid.', 'lower boiling point, removed [1]; prevents further oxidation to acid [1]'),
    ('Explain why NaBH₄ reduces C=O but not C=C bonds.', 'H⁻ is a nucleophile and attacks the δ+ carbon of the polar C=O bond; the non-polar C=C is electron-rich and does not attract nucleophiles.', 'C=O polar, δ+ C attacked by H⁻ [1]; C=C non-polar/electron rich [1]'),
])
errs(t17a, [
    ('Reduction of butanone with NaBH₄ gives butan-1-ol.', 'Ketones are reduced to secondary alcohols: butanone gives butan-2-ol.'),
    ('Propanal is made by heating propan-2-ol under reflux with acidified dichromate(VI).', 'Propan-2-ol gives propanone; propanal is made from propan-1-ol by distilling the aldehyde off as it forms.'),
])
c2mix(t17a, ['{p} prepares carbonyl compounds in {lab}.', 'A fragrance manufacturer in {c} makes aldehydes and ketones.'])


@t17a.add('C1', (1, 2, 3))
def t17a_red(r, D):
    c = r.choice(list(CARB))
    corr = CARB[c][1]
    pool = [CARB[k][1] for k in CARB] + [ALC16.get(corr, ('', '', None, None))[3] or 'propanoic acid']
    return mc(r, f'What is the organic product when {c}, {SF16(c)}, is reduced with NaBH₄?', corr, pool, f'{red_eq(c)}.')


@t17a.add('C1', (1, 2, 3))
def t17a_from(r, D):
    c = r.choice(list(CARB))
    a = CARB[c][1]
    pool = [CARB[k][1] for k in CARB if k != c] + ['2-methylpropan-2-ol']
    how = 'distilling the product off as it forms' if CARB[c][0] == 'aldehyde' else 'heating under reflux'
    return mc(r, f'{cap(c)} is made by oxidising an alcohol with acidified potassium dichromate(VI) and {how}. Which alcohol is used?', a, pool, f'{a} ({ALC16.get(a, ("", "primary"))[1]}) → {c}.')


@t17a.add('C3', (2, 3, 4, 5), 'short')
def t17a_route(r, D):
    c = r.choice(list(CARB))
    kind, a = CARB[c][0], CARB[c][1]
    how = 'warm with acidified K₂Cr₂O₇ (excess alcohol) and distil off the aldehyde as it forms' if kind == 'aldehyde' else 'heat under reflux with acidified K₂Cr₂O₇'
    stem = f'{who(r)} wants to make {c}, {SF16(c)}, from an alcohol and then reduce a sample back to the alcohol. Name the alcohol and give the reagents and conditions for each step, with equations using [O] and [H].'
    key = f'{a} [1]; {how} [1]; {SF16(a)} + [O] → {SF16(c)} + H₂O [1]; NaBH₄ (aqueous/alcoholic) [1]; {red_eq(c)} [1]'
    ans = f'{a}; {how}; {SF16(a)} + [O] → {SF16(c)} + H₂O; NaBH₄; {red_eq(c)}'
    if D >= 5:
        stem += ' State the type of reaction in the reduction step.'
        key += '; nucleophilic addition (reduction) [1]'
        ans += '; reduction (nucleophilic addition of H⁻)'
    return {'stem': stem, 'answer': ans, 'key': key}


@t17a.add('C3', (3, 4, 5), 'numerical')
def t17a_yield(r, D):
    c = r.choice(list(CARB))
    a = CARB[c][1]
    Ma, Mc = M16(a), M16(c)
    m = r.choice([5.00, 6.50, 8.00, 10.0, 3.70])
    y = r.choice([0.35, 0.4, 0.48, 0.55, 0.62])
    mc_ = m / Ma * Mc * y
    mc_ = round(mc_, 2)
    y = mc_ / (m / Ma * Mc)
    stem = f'{who(r)} oxidises {m:.2f} g of {a} and obtains {mc_:.2f} g of {c}. Calculate the percentage yield.'
    key = f'n({a}) = {m:.2f}/{mr1(Ma)} = {g3(m / Ma)} mol [1]; max mass {c} = {g3(m / Ma * Mc)} g (Mr {mr1(Mc)}) [1]; yield = {g3(y * 100)}% [1]'
    ans = f'{g3(y * 100)}%'
    if D >= 5 and CARB[c][0] == 'aldehyde':
        stem += ' Suggest one reason why the yield is low.'
        key += '; some aldehyde oxidised further to the carboxylic acid (or lost on distillation) [1]'
        ans += '; further oxidation to the acid'
    return {'stem': stem, 'answer': ans, 'key': key}


def t17a_c4(r, D):
    c = r.choice(list(CARB))
    kind, a = CARB[c][0], CARB[c][1]
    intro = P(r, r.choice([f'{{p}} investigates {c}, {SF16(c)}, in {{lab}}.', f'An industrial chemist in {{c}} produces {c} by oxidation of an alcohol.']))
    parts = [
        lambda r: ('State whether the compound is an aldehyde or a ketone and explain.', f'{kind}: C=O ' + ('at the end of the chain (–CHO)' if kind == 'aldehyde' else 'within the chain, bonded to two carbons'), '[2]'),
        lambda r: ('Name the alcohol it is made from and describe the conditions.', f'{a}; ' + ('acidified K₂Cr₂O₇, distil off as it forms' if kind == 'aldehyde' else 'acidified K₂Cr₂O₇, heat under reflux'), '[2]'),
        lambda r: ('Write an equation for its reduction with NaBH₄ using [H].', red_eq(c), '[1]'),
        lambda r: ('Name the type of alcohol formed on reduction.', 'primary' if kind == 'aldehyde' else 'secondary', '[1]'),
        lambda r: ('Suggest why its boiling point is lower than that of the alcohol.', 'No O–H, so no hydrogen bonding between molecules; only dipole–dipole forces.', '[2]'),
        lambda r: ('Give its molecular formula and Mr.', f'{MF16(c)}; {mr1(M16(c))}', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t17a, t17a_c4)

# ---------------------------------------------------------- 17.2 HCN nucleophilic addition
t17b = topic('Nucleophilic addition of HCN to carbonyl compounds: mechanism', 'nucleophilic addition of hcn to carbonyl compounds', 'mechanism')
t17b.fixed('C1', (1, 2), [
    ('What type of mechanism occurs when HCN reacts with ethanal?', 'nucleophilic addition', 'CN⁻ attacks the δ+ carbonyl carbon.', ['electrophilic addition', 'nucleophilic substitution', 'free-radical substitution']),
    ('Which species attacks the carbonyl carbon in the reaction with HCN?', 'CN⁻', 'The cyanide ion uses its lone pair on carbon.', ['H⁺', 'HCN molecule as an electrophile', 'K⁺']),
    ('How is HCN usually provided in the laboratory?', 'KCN with dilute sulfuric acid, generating HCN in situ', 'HCN is very toxic; the reaction is done in a fume cupboard.', ['bubbling HCN gas from a cylinder', 'KCN in ethanol only', 'NaCN with sodium hydroxide']),
    ('Why is the product of HCN addition to ethanal a racemic mixture?', 'the planar C=O is attacked equally from either side', 'Equal amounts of the two optical isomers form, so there is no net optical activity.', ['the product has no chiral centre', 'only one face of the molecule can be attacked', 'the cyanide ion is chiral']),
    ('Why does the reaction with HCN increase the length of the carbon chain?', 'the CN group adds a new carbon atom', 'Useful in synthesis; nitrile can be hydrolysed to –COOH.', ['the C=O carbon is removed', 'HCN is a source of hydrogen only', 'two molecules join together']),
    ('Name the product of the reaction of HCN with propanone.', '2-Hydroxy-2-methylpropanenitrile, (CH₃)₂C(OH)CN.', '[1]'),
])
t17b.fixed('C2', (2, 3, 4), [
    ('Describe the role of the intermediate in the mechanism of HCN addition to a carbonyl compound.', 'CN⁻ attack produces a negatively charged alkoxide intermediate (O⁻), which accepts H⁺ from HCN (or water) to form the hydroxynitrile, regenerating CN⁻.', 'O⁻ intermediate [1]; protonated by HCN, regenerating CN⁻ [1]'),
    ('Explain why the carbonyl carbon is attacked by nucleophiles.', 'Oxygen is more electronegative than carbon, so the C=O bond is polar and the carbon is δ+, attracting the lone pair of a nucleophile.', 'O more electronegative / bond polar [1]; δ+ carbon attracts nucleophile [1]'),
    ('Explain why the reaction of HCN with propanone does not give optical isomers.', 'The product, (CH₃)₂C(OH)CN, has two identical CH₃ groups on the new carbon, so it has no chiral centre.', 'two identical CH₃ groups [1]; no chiral centre so no optical isomers [1]'),
])
errs(t17b, [
    ('In the reaction of HCN with ethanal, H⁺ attacks the carbonyl oxygen first.', 'The first step is attack of the nucleophile CN⁻ on the δ+ carbonyl carbon; H⁺ is added to the O⁻ intermediate afterwards.'),
    ('The product of HCN and ethanal is optically active because it has a chiral centre.', 'The product has a chiral centre, but a racemic mixture forms (equal attack from either side of the planar C=O), so it is not optically active.'),
])
c2mix(t17b, ['{p} studies the reaction of carbonyl compounds with HCN in {lab}.', 'A pharmaceutical chemist in {c} uses HCN addition to lengthen carbon chains.'])


@t17b.add('C1', (1, 2, 3))
def t17b_prod(r, D):
    c = r.choice(list(CARB))
    corr = f'{CARB[c][2]}, {SF16(CARB[c][2])}'
    pool = [f'{CARB[k][2]}, {SF16(CARB[k][2])}' for k in CARB if k != c]
    return mc(r, f'What is the product when {c}, {SF16(c)}, reacts with HCN (from KCN and dilute acid)?', corr, pool, f'Nucleophilic addition across C=O: {SF16(c)} + HCN → {SF16(CARB[c][2])}.')


@t17b.add('C1', (1, 2, 3))
def t17b_chiral(r, D):
    c = r.choice(list(CARB))
    ch = CARB[c][4]
    corr = 'a racemic mixture of two optical isomers' if ch else 'a single product with no chiral centre'
    return mc(r, f'Which describes the product of the reaction of HCN with {c}?', corr, ['a racemic mixture of two optical isomers', 'a single product with no chiral centre', 'a single optical isomer only', 'a pair of cis/trans isomers'],
              f'Product {SF16(CARB[c][2])}: ' + ('new carbon has four different groups; planar C=O attacked equally from both sides → racemic.' if ch else 'two identical groups on the new carbon, not chiral.'))


@t17b.add('C3', (2, 3, 4, 5), 'explain')
def t17b_mech(r, D):
    c = r.choice(list(CARB))
    p = CARB[c][2]
    stem = f'Describe, with the aid of curly-arrow descriptions, the mechanism of the reaction between {c}, {SF16(c)}, and HCN. Name the product.'
    key = 'curly arrow from C of CN⁻ lone pair to δ+ carbonyl C [1]; C=O π electrons move to O, forming O⁻ intermediate [1]; O⁻ takes H⁺ from HCN (arrow from O⁻ to H), regenerating CN⁻ [1]; ' + f'{p}, {SF16(p)} [1]'
    ans = f'CN⁻ attacks δ+ C; C=O π bond breaks to give O⁻; O⁻ protonated by HCN; product {p}, {SF16(p)}.'
    if D >= 4:
        stem += ' State whether the product is optically active and explain.'
        key += '; ' + ('racemic mixture: planar C=O attacked equally from both sides, so not optically active [2]' if CARB[c][4] else 'no chiral centre (two identical groups), so not optically active [2]')
        ans += ' Not optically active: ' + ('racemic mixture.' if CARB[c][4] else 'no chiral centre.')
    return {'stem': stem, 'answer': ans, 'key': key}


@t17b.add('C3', (2, 3, 4, 5), 'numerical')
def t17b_calc(r, D):
    c = r.choice(list(CARB))
    p = CARB[c][2]
    Mc, Mp = M16(c), M16(p)
    m = r.choice([2.20, 2.90, 3.60, 4.30, 5.80])
    y = r.choice([0.5, 0.6, 0.65, 0.72, 0.8])
    stem = f'{who(r)} reacts {m:.2f} g of {c} with excess HCN. Calculate the Mr of the product, {p}, and the mass formed if the yield is {int(y * 100)}%.'
    key = f'product {MF16(p)}, Mr = {mr1(Mp)} [1]; n({c}) = {m:.2f}/{mr1(Mc)} = {g3(m / Mc)} mol [1]; mass = {g3(m / Mc)} × {mr1(Mp)} × {y} = {g3(m / Mc * Mp * y)} g [1]'
    return {'stem': stem, 'answer': f'Mr = {mr1(Mp)}; {g3(m / Mc * Mp * y)} g', 'key': key}


def t17b_c4(r, D):
    c = r.choice(list(CARB))
    p = CARB[c][2]
    ch = CARB[c][4]
    intro = P(r, r.choice([f'{{p}} reacts {c}, {SF16(c)}, with KCN and dilute sulfuric acid in a fume cupboard in {{lab}}.', f'A chemist in {{c}} uses {c} and HCN to make {p}.']))
    parts = [
        lambda r: ('Name the mechanism and the attacking species.', 'nucleophilic addition; CN⁻', '[2]'),
        lambda r: ('Describe the mechanism, including the intermediate.', 'CN⁻ attacks δ+ C=O carbon; π electrons to O giving O⁻ intermediate; O⁻ takes H⁺ from HCN, regenerating CN⁻', '[3]'),
        lambda r: ('Give the structural formula of the product.', SF16(p), '[1]'),
        lambda r: ('Explain whether the product sample rotates plane-polarised light.', ('No: racemic mixture, as planar C=O attacked equally from both sides.' if ch else 'No: the product has no chiral centre.'), '[2]'),
        lambda r: ('Explain why the KCN/acid mixture is used rather than HCN gas.', 'HCN is a highly toxic gas; generating it in situ reduces the hazard (and provides CN⁻ ions).', '[1]'),
        lambda r: ('Suggest how the product could be converted into a hydroxy carboxylic acid.', 'Heat under reflux with dilute HCl (acid hydrolysis of the nitrile).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t17b, t17b_c4)

# ---------------------------------------------------------- 17.3 tests
TESTS17 = {
    'DNPH': ('2,4-DNPH (Brady\'s reagent)', 'orange/yellow precipitate', 'orange/yellow precipitate', 'no precipitate'),
    'Fehling': ('Fehling\'s solution, warmed', 'blue solution gives a brick-red precipitate (Cu₂O)', 'stays blue', 'stays blue'),
    'Tollens': ('Tollens\' reagent, warmed', 'silver mirror forms', 'no silver mirror', 'no silver mirror'),
}
NONCARB = ['ethanol', 'propan-1-ol', 'propan-2-ol', 'ethanoic acid', 'ethyl ethanoate']


def test_obs(test, c):
    nm, ald, ket, other = TESTS17[test]
    if c in CARB:
        return ald if CARB[c][0] == 'aldehyde' else ket
    return other


t17c = topic('Testing for carbonyl compounds: 2,4-DNPH, Fehling\'s and Tollens\' reagents', 'testing for carbonyl compounds: 2,4-dnph, fehling\'s and tollens\' reagents', 'carbonyl tests')
t17c.fixed('C1', (1, 2), [
    ('Which reagent gives an orange precipitate with both aldehydes and ketones?', '2,4-dinitrophenylhydrazine (2,4-DNPH)', 'Condensation (addition–elimination) gives a 2,4-dinitrophenylhydrazone.', ['Fehling\'s solution', 'Tollens\' reagent', 'acidified dichromate(VI)']),
    ('What is observed when ethanal is warmed with Tollens\' reagent?', 'a silver mirror forms', 'Ag⁺ is reduced to Ag; the aldehyde is oxidised.', ['a brick-red precipitate', 'orange to green', 'no change']),
    ('What is the brick-red precipitate formed in a positive Fehling\'s test?', 'copper(I) oxide, Cu₂O', 'Cu²⁺ (blue) is reduced to Cu(I).', ['copper(II) oxide', 'copper metal', 'copper(II) hydroxide']),
    ('Why do ketones not react with Fehling\'s solution?', 'ketones are not easily oxidised', 'There is no H on the carbonyl carbon.', ['ketones have no C=O group', 'ketones are insoluble in water', 'ketones are reducing agents']),
    ('How can the 2,4-DNPH derivative be used to identify a particular carbonyl compound?', 'by recrystallising it and comparing its melting point with data tables', 'Each derivative has a characteristic melting point.', ['by measuring its colour', 'by testing it with Tollens\' reagent', 'by measuring its boiling point']),
    ('What is the role of the aldehyde in the Tollens\' test?', 'reducing agent', 'The aldehyde reduces Ag⁺ to Ag and is oxidised to a carboxylic acid (carboxylate).', ['oxidising agent', 'catalyst', 'dehydrating agent']),
    ('State the colour of the precipitate formed with 2,4-DNPH.', 'Orange (or yellow-orange).', '[1]'),
])
t17c.fixed('C2', (2, 3, 4), [
    ('Explain why aldehydes give a positive result with Tollens\' reagent but ketones do not.', 'Aldehydes have an H on the carbonyl carbon and are easily oxidised to carboxylic acids, reducing Ag⁺ to Ag; ketones cannot be oxidised without breaking C–C bonds.', 'aldehydes oxidised (to acid/carboxylate) [1]; Ag⁺ reduced to Ag; ketones not oxidised [1]'),
    ('Explain why the 2,4-DNPH test alone cannot distinguish an aldehyde from a ketone.', 'Both contain C=O and both form an orange precipitate; a second test (Fehling\'s or Tollens\') is needed.', 'both have C=O, both positive [1]; Fehling\'s/Tollens\' needed [1]'),
])
errs(t17c, [
    ('Propanone gives a silver mirror with Tollens\' reagent because it contains C=O.', 'Propanone is a ketone, which is not oxidised, so no silver mirror forms; only aldehydes react.'),
    ('In Fehling\'s test, the aldehyde is reduced and a brick-red precipitate of copper forms.', 'The aldehyde is oxidised; Cu²⁺ is reduced to copper(I) oxide, Cu₂O.'),
])
c2mix(t17c, ['{p} identifies unknown organic liquids in {lab}.', 'A forensic chemist in {c} tests samples for carbonyl compounds.'])


@t17c.add('C1', (1, 2, 3))
def t17c_obs(r, D):
    c = r.choice(list(CARB) + NONCARB)
    test = r.choice(list(TESTS17))
    corr = test_obs(test, c)
    pool = ['orange/yellow precipitate', 'no precipitate', 'blue solution gives a brick-red precipitate (Cu₂O)', 'stays blue', 'silver mirror forms', 'no silver mirror', 'white precipitate forms']
    return mc(r, f'What is observed when {c} is tested with {TESTS17[test][0]}?', corr, pool, f'{c}: ' + (CARB[c][0] if c in CARB else 'not a carbonyl compound') + f' → {corr}.')


@t17c.add('C3', (2, 3, 4, 5), 'short')
def t17c_pair(r, D):
    a = r.choice([k for k in CARB if CARB[k][0] == 'aldehyde'])
    b = r.choice([k for k in CARB if CARB[k][0] == 'ketone'] + NONCARB[:3])
    if r.random() < 0.5:
        a, b = b, a
    if b in CARB and a in CARB:
        test = r.choice(['Fehling', 'Tollens'])
    elif (a in CARB) != (b in CARB):
        test = 'DNPH' if (a in CARB and CARB[a][0] == 'ketone') or (b in CARB and CARB[b][0] == 'ketone') else r.choice(['Fehling', 'Tollens', 'DNPH'])
    else:
        return None
    stem = f'Describe a chemical test to distinguish between {a} and {b}. Give the observation for each compound.'
    key = f'{TESTS17[test][0]} [1]; {a}: {test_obs(test, a)} [1]; {b}: {test_obs(test, b)} [1]'
    ans = f'{TESTS17[test][0]}: {a} – {test_obs(test, a)}; {b} – {test_obs(test, b)}'
    if D >= 4:
        stem += ' Explain the result for the compound that reacts.'
        x = a if test_obs(test, a) in ('orange/yellow precipitate', 'blue solution gives a brick-red precipitate (Cu₂O)', 'silver mirror forms') else b
        why = 'C=O reacts in condensation (addition–elimination)' if test == 'DNPH' else 'the aldehyde is oxidised (to carboxylic acid), reducing ' + ('Cu²⁺ to Cu₂O' if test == 'Fehling' else 'Ag⁺ to Ag')
        key += f'; {x}: {why} [1]'
        ans += f'; {x}: {why}'
    return {'stem': stem, 'answer': ans, 'key': key}


UNK17 = [('C₃H₆O', ['propanal', 'propanone']), ('C₄H₈O', ['butanal', 'butanone']), ('C₅H₁₀O', ['pentanal', 'pentan-2-one', 'pentan-3-one'])]


@t17c.add('C3', (2, 3, 4, 5), 'short')
def t17c_unk(r, D):
    mf, cands = r.choice(UNK17)
    x = r.choice(cands)
    iod = IODO.get(x, (False,))[0]
    res = [f'2,4-DNPH: {test_obs("DNPH", x)}', f'Fehling\'s solution: {test_obs("Fehling", x)}']
    if len(cands) == 3 or D >= 4:
        res.append('alkaline aqueous iodine: ' + ('pale yellow precipitate' if iod else 'no precipitate'))
    stem = f'{who(r)} tests an unknown compound Y, {mf}, which is one of {", ".join(cands)}. Results: ' + '; '.join(res) + '. Identify Y, explaining how each result supports your answer.'
    key = f'DNPH positive: carbonyl [1]; Fehling\'s {"positive: aldehyde" if CARB[x][0] == "aldehyde" else "negative: ketone"} [1]'
    if len(res) == 3:
        key += f'; iodoform {"positive: CH₃CO– present" if iod else "negative: no CH₃CO–"} [1]'
    key += f'; Y = {x}, {SF16(x)} [1]'
    return {'stem': stem, 'answer': f'Y is {x}, {SF16(x)}.', 'key': key}


def t17c_c4(r, D):
    mf, cands = r.choice(UNK17)
    intro = P(r, f'{{p}} has three bottles, labelled A, B and C. Two contain the isomers {" and ".join(cands[:2])} ({mf}), and the third contains ethanol.')
    parts = [
        lambda r: ('Describe a test that shows which bottles contain a carbonyl compound.', '2,4-DNPH: orange precipitate with both carbonyls; none with ethanol', '[2]'),
        lambda r: ('Describe how to distinguish the two carbonyl isomers.', f'Fehling\'s (warm): {cands[0]}: {test_obs("Fehling", cands[0])}; {cands[1]}: {test_obs("Fehling", cands[1])} (or Tollens\')', '[2]'),
        lambda r: ('Name the inorganic product formed in a positive Fehling\'s test and state what happens to the organic compound.', 'Cu₂O; the aldehyde is oxidised to a carboxylic acid (carboxylate)', '[2]'),
        lambda r: ('Explain how the 2,4-DNPH products could confirm the identity of each isomer.', 'Recrystallise the precipitates and compare melting points with known values.', '[2]'),
        lambda r: ('Suggest a test that would give a positive result with ethanol but not with ' + cands[0] + '.', ('Acidified K₂Cr₂O₇ also oxidises the aldehyde, so use alkaline iodine: ethanol gives a yellow precipitate, ' + cands[0] + ' does not.') if not IODO.get(cands[0], (False,))[0] else 'Sodium: effervescence (H₂) with ethanol only.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t17c, t17c_c4)

CHAPTERS[17] = [t17a, t17b, t17c]

# ===================================================================== Ch18 Analytical techniques
IR18 = [('C–O', (1040, 1300), 'alcohols, esters, carboxylic acids'), ('C=C', (1500, 1680), 'alkenes'), ('C=O', (1640, 1750), 'aldehydes, ketones, carboxylic acids, esters'),
        ('C≡N', (2200, 2250), 'nitriles'), ('C–H', (2850, 2950), 'alkanes, alkenes'), ('N–H', (3300, 3500), 'amines'), ('O–H (alcohol)', (3200, 3600), 'alcohols (broad)'),
        ('O–H (carboxylic acid)', (2500, 3000), 'carboxylic acids (very broad)')]
IR_TABLE = 'Data: C–O 1040–1300; C=C 1500–1680; C=O 1640–1750; C≡N 2200–2250; C–H 2850–2950; N–H 3300–3500; O–H (alcohol) 3200–3600 (broad); O–H (acid) 2500–3000 (very broad), all in cm⁻¹.'
# characteristic absorptions above 1500 cm⁻¹ (besides C–H) by class
IRSIG = {'alcohol': 'broad 3200–3600 (O–H)', 'aldehyde': 'sharp ~1720 (C=O) only', 'ketone': 'sharp ~1715 (C=O) only', 'carboxylic acid': '~1710 (C=O) and very broad 2500–3000 (O–H)',
         'ester': '~1740 (C=O) and 1040–1300 (C–O), no O–H', 'alkene': '~1650 (C=C)', 'nitrile': '~2230 (C≡N)', 'alkane': 'only C–H (2850–2950)', 'amine': '3300–3500 (N–H)'}
IRCPD = {'alcohol': ['ethanol', 'propan-1-ol', 'butan-2-ol'], 'aldehyde': ['propanal', 'ethanal', 'butanal'], 'ketone': ['propanone', 'butanone'], 'carboxylic acid': ['ethanoic acid', 'propanoic acid'],
         'ester': ['ethyl ethanoate', 'methyl ethanoate'], 'alkene': ['propene', 'but-1-ene'], 'nitrile': ['propanenitrile', 'butanenitrile'], 'alkane': ['hexane', 'pentane'], 'amine': ['ethylamine', 'propylamine']}

t18a = topic('Infrared spectroscopy: identifying functional groups from absorption ranges', 'infrared spectroscopy', 'identifying functional groups from absorption ranges')
t18a.fixed('C1', (1, 2), [
    ('What happens to a molecule when it absorbs infrared radiation?', 'its bonds vibrate more (stretch and bend)', 'Each bond absorbs at a characteristic frequency (wavenumber).', ['electrons are removed', 'the molecule fragments into ions', 'nuclei change spin']),
    ('Which feature of an IR spectrum distinguishes a carboxylic acid from an alcohol?', 'a C=O absorption near 1700 cm⁻¹ with a very broad O–H at 2500–3000 cm⁻¹', 'Alcohol O–H is at 3200–3600 cm⁻¹ and there is no C=O.', ['a C–H absorption at 2900 cm⁻¹', 'an absorption below 1000 cm⁻¹', 'a C≡N absorption']),
    ('What is the fingerprint region of an IR spectrum used for?', 'identifying a compound by comparison with spectra of known compounds', 'Below about 1500 cm⁻¹ the pattern is unique to each compound.', ['measuring the Mr', 'finding the number of carbon atoms', 'detecting isotopes']),
    ('How can IR spectroscopy show that ethanol has been fully oxidised to ethanoic acid?', 'a C=O absorption appears and the broad alcohol O–H at 3200–3600 cm⁻¹ is replaced by a very broad O–H at 2500–3000 cm⁻¹', 'Use the data table.', ['the C–H absorption disappears', 'a C≡N absorption appears', 'an N–H absorption appears']),
    ('Which greenhouse gas property is explained by IR absorption?', 'CO₂ and H₂O absorb infrared radiation emitted by the Earth', 'Bond vibrations absorb IR, warming the atmosphere.', ['CO₂ absorbs ultraviolet radiation', 'CO₂ reflects visible light', 'CO₂ emits X-rays']),
    ('State the units of wavenumber in IR spectroscopy.', 'cm⁻¹', '[1]'),
])
t18a.fixed('C2', (2, 3, 4), [
    ('Explain how infrared spectroscopy is used in breathalysers.', 'Ethanol absorbs IR (C–H/O–H vibration) at characteristic wavenumbers; the amount of absorption is proportional to the ethanol concentration in the breath.', 'ethanol bonds absorb at characteristic wavenumber [1]; absorbance measures concentration [1]'),
    ('Explain why an IR spectrum alone may not distinguish propanal from propanone.', 'Both have a C=O absorption near 1720 cm⁻¹ and C–H absorptions; the difference is only in the fingerprint region, which must be matched with known spectra.', 'both have C=O and C–H [1]; fingerprint region/comparison needed [1]'),
])
errs(t18a, [
    ('An absorption at 1720 cm⁻¹ shows that a compound must be an aldehyde.', 'An absorption at 1640–1750 cm⁻¹ shows C=O, which is present in aldehydes, ketones, carboxylic acids and esters.'),
    ('A broad absorption at 3200–3600 cm⁻¹ shows a carboxylic acid.', 'That range shows an alcohol O–H; carboxylic acid O–H is very broad at 2500–3000 cm⁻¹, with C=O near 1700 cm⁻¹.'),
])
c2mix(t18a, ['{p} uses an IR spectrometer to monitor reactions in {lab}.', 'An environmental laboratory in {c} uses IR spectroscopy.'])


@t18a.add('C1', (1, 2, 3))
def t18a_bond(r, D):
    choices = {'C–O': (1060, 1280), 'C=C': (1520, 1630), 'C=O': (1690, 1750), 'C≡N': (2210, 2250), 'O–H (carboxylic acid)': (2500, 2800), 'O–H (alcohol)': (3200, 3290)}
    b = r.choice(list(choices))
    lo, hi = choices[b]
    v = r.randrange(lo, hi + 1, 10)
    pool = [x[0] for x in IR18 if x[0] != b]
    if b.startswith('O–H'):
        pool = [p for p in pool if not p.startswith('O–H')]
    return mc(r, f'{IR_TABLE} A compound has a strong absorption at {v} cm⁻¹. Which bond is responsible?', b, pool, f'{v} cm⁻¹ lies in the {b} range.')


@t18a.add('C1', (1, 2, 3))
def t18a_cpd(r, D):
    groups = ['alcohol', 'carboxylic acid', 'alkene', 'nitrile', 'alkane', r.choice(['aldehyde', 'ketone', 'ester'])]
    cls = r.choice(groups)
    c = r.choice(IRCPD[cls])
    pool = [r.choice(IRCPD[g]) for g in groups if g != cls]
    return mc(r, f'{IR_TABLE} An IR spectrum shows (apart from C–H): {IRSIG[cls]}. Which compound could give this spectrum?', c, pool, f'{c} is {art(cls)}: {IRSIG[cls]}.')


@t18a.add('C3', (2, 3, 4, 5), 'short')
def t18a_mon(r, D):
    alc = r.choice(['ethanol', 'propan-1-ol', 'butan-1-ol', 'propan-2-ol', 'butan-2-ol'])
    _, cls, carb, acid, _, _ = ALC16[alc]
    opts = [('alcohol', alc, 'broad absorption at 3200–3600 cm⁻¹ and no absorption at 1640–1750 cm⁻¹', 'O–H (alcohol) present, no C=O: unreacted alcohol')] if D <= 3 else []
    opts.append((ORG.get(carb, ('', 'aldehyde'))[1], carb, 'strong absorption at about 1720 cm⁻¹ and no broad absorption above 2500 cm⁻¹ other than C–H at 2900', 'C=O present, no O–H: ' + ('aldehyde' if cls == 'primary' else 'ketone')))
    if acid:
        opts.append(('carboxylic acid', acid, 'strong absorption at about 1710 cm⁻¹ and a very broad absorption from 2500 to 3000 cm⁻¹', 'C=O and acid O–H: carboxylic acid'))
    _, prod, desc, why = r.choice(opts)
    stem = f'{IR_TABLE} {who(r)} oxidises {alc} with acidified potassium dichromate(VI). The IR spectrum of the product shows a {desc}. Identify the product and explain your reasoning.'
    key = f'assigns absorption(s) to bonds [1]; {why} [1]; product = {prod} [1]'
    ans = f'{prod}: {why}'
    if D >= 4:
        stem += ' State the conditions that would give this product.'
        cond = 'no reaction / starting material unchanged (insufficient heating)' if prod == alc else ('distil off as formed' if prod == carb and cls == 'primary' else 'heat under reflux with excess oxidant')
        key += f'; {cond} [1]'
        ans += f'; {cond}'
    return {'stem': stem, 'answer': ans, 'key': key}


@t18a.add('C3', (2, 3, 4, 5), 'short')
def t18a_assign(r, D):
    cls = r.choice(['alcohol', 'carboxylic acid', 'ester', 'nitrile', 'alkene', 'ketone', 'amine'])
    c = r.choice(IRCPD[cls])
    bonds = {'alcohol': ['O–H (alcohol) 3200–3600', 'C–O 1040–1300', 'C–H 2850–2950'], 'carboxylic acid': ['O–H (acid) 2500–3000', 'C=O 1640–1750', 'C–O 1040–1300'],
             'ester': ['C=O 1640–1750', 'C–O 1040–1300', 'C–H 2850–2950'], 'nitrile': ['C≡N 2200–2250', 'C–H 2850–2950'], 'alkene': ['C=C 1500–1680', 'C–H 2850–2950'],
             'ketone': ['C=O 1640–1750', 'C–H 2850–2950'], 'amine': ['N–H 3300–3500', 'C–H 2850–2950']}[cls]
    k = 2 if D <= 3 else len(bonds)
    stem = f'{IR_TABLE} Predict {"two" if k == 2 else "the main"} absorption ranges you would expect in the IR spectrum of {c}, {SF16(c)}, and name the bond responsible for each.'
    key = '; '.join(f'{b} cm⁻¹ [1]' for b in bonds[:k])
    return {'stem': stem, 'answer': '; '.join(b + ' cm⁻¹' for b in bonds[:k]), 'key': key}


def t18a_c4(r, D):
    a, b = r.sample(['alcohol', 'carboxylic acid', 'ester', 'ketone', 'aldehyde'], 2)
    if {a, b} == {'ketone', 'aldehyde'}:
        b = 'alcohol'
    ca, cb = r.choice(IRCPD[a]), r.choice(IRCPD[b])
    intro = P(r, f'{{p}} records IR spectra of two liquids, P ({ca}) and Q ({cb}), in {{lab}}. {IR_TABLE}')
    parts = [
        lambda r: ('State what causes absorption of IR radiation by molecules.', 'Bonds vibrate (stretch/bend) at characteristic frequencies when they absorb IR.', '[1]'),
        lambda r: ('Predict the key absorption(s) for P.', IRSIG[a], '[2]'),
        lambda r: ('Predict the key absorption(s) for Q.', IRSIG[b], '[2]'),
        lambda r: ('Explain which feature would let you tell P and Q apart most easily.', f'P: {IRSIG[a]}; Q: {IRSIG[b]}; the presence/absence of the distinguishing band', '[2]'),
        lambda r: ('Explain the use of the fingerprint region.', 'Below 1500 cm⁻¹; compare with a database of known spectra to confirm identity.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


c4reg(t18a, t18a_c4)

# ---------------------------------------------------------- 18.2 mass spectrometry
MS18 = {  # name: (M, [(m/z, ion, radical lost)])
    'propanone': (58, [(43, 'CH₃CO⁺', 'CH₃•'), (15, 'CH₃⁺', 'CH₃CO•')]),
    'propanal': (58, [(29, 'C₂H₅⁺ (or CHO⁺)', 'CHO• (or C₂H₅•)'), (57, 'C₂H₅CO⁺', 'H•')]),
    'ethanol': (46, [(31, 'CH₂OH⁺', 'CH₃•'), (29, 'C₂H₅⁺', 'OH•'), (45, 'C₂H₅O⁺', 'H•')]),
    'propan-1-ol': (60, [(31, 'CH₂OH⁺', 'C₂H₅•'), (29, 'C₂H₅⁺', 'CH₂OH•')]),
    'propan-2-ol': (60, [(45, 'CH₃CHOH⁺', 'CH₃•'), (43, 'C₃H₇⁺', 'OH•'), (15, 'CH₃⁺', 'CH₃CHOH•')]),
    'butane': (58, [(43, 'C₃H₇⁺', 'CH₃•'), (29, 'C₂H₅⁺', 'C₂H₅•'), (15, 'CH₃⁺', 'C₃H₇•')]),
    'butanone': (72, [(43, 'CH₃CO⁺', 'C₂H₅•'), (57, 'C₂H₅CO⁺', 'CH₃•'), (29, 'C₂H₅⁺', 'CH₃CO•')]),
    'pentan-3-one': (86, [(57, 'C₂H₅CO⁺', 'C₂H₅•'), (29, 'C₂H₅⁺', 'C₂H₅CO•')]),
    'pentan-2-one': (86, [(43, 'CH₃CO⁺', 'C₃H₇•'), (71, 'C₃H₇CO⁺', 'CH₃•')]),
    'ethanoic acid': (60, [(45, 'COOH⁺', 'CH₃•'), (43, 'CH₃CO⁺', 'OH•'), (15, 'CH₃⁺', 'COOH•')]),
    'methyl ethanoate': (74, [(43, 'CH₃CO⁺', 'CH₃O•'), (59, 'COOCH₃⁺', 'CH₃•'), (15, 'CH₃⁺', 'COOCH₃•')]),
    'ethyl ethanoate': (88, [(43, 'CH₃CO⁺', 'C₂H₅O•'), (29, 'C₂H₅⁺', 'CH₃COO•')]),
    'propanoic acid': (74, [(45, 'COOH⁺', 'C₂H₅•'), (29, 'C₂H₅⁺', 'COOH•'), (57, 'C₂H₅CO⁺', 'OH•')]),
    'ethanal': (44, [(29, 'CHO⁺', 'CH₃•'), (15, 'CH₃⁺', 'CHO•'), (43, 'CH₃CO⁺', 'H•')]),
}
HALMS = [  # name, formula, peaks (m/z), ratio
    ('chloromethane', 'CH₃Cl', (50, 52), '3 : 1'), ('chloroethane', 'C₂H₅Cl', (64, 66), '3 : 1'), ('2-chloropropane', 'C₃H₇Cl', (78, 80), '3 : 1'),
    ('bromomethane', 'CH₃Br', (94, 96), '1 : 1'), ('bromoethane', 'C₂H₅Br', (108, 110), '1 : 1'), ('1-bromopropane', 'C₃H₇Br', (122, 124), '1 : 1'),
    ('dichloromethane', 'CH₂Cl₂', (84, 86, 88), '9 : 6 : 1'), ('1,2-dibromoethane', 'C₂H₄Br₂', (186, 188, 190), '1 : 2 : 1'), ('1,1-dichloroethane', 'C₂H₄Cl₂', (98, 100, 102), '9 : 6 : 1'),
]
MSFORM = {'butane': 'CH3CH2CH2CH3', 'ethanal': 'CH3CHO'}

t18b = topic('Mass spectrometry: molecular ion, M+1 peak and fragmentation patterns', 'mass spectrometry: molecular ion, m+1 peak', 'fragmentation patterns')
t18b.fixed('C1', (1, 2), [
    ('What causes the M+1 peak in the mass spectrum of an organic compound?', 'molecules containing one ¹³C atom', 'About 1.1% of carbon atoms are ¹³C.', ['molecules that have gained a hydrogen atom', 'ions with a 2+ charge', 'fragments that have lost one hydrogen']),
    ('In a mass spectrum, which peak gives the Mr of the compound?', 'the molecular ion peak, M⁺, with the highest m/z (ignoring M+1)', 'The molecular ion is the whole molecule minus one electron.', ['the tallest peak (base peak)', 'the peak at m/z 15', 'the smallest peak']),
    ('Which ion causes a peak at m/z 43 in the mass spectrum of propanone?', 'CH₃CO⁺', 'Loss of CH₃• from the molecular ion (58 − 15 = 43).', ['C₂H₅⁺', 'CH₃⁺', 'COOH⁺']),
    ('A compound shows molecular ion peaks at m/z 78 and 80 in the ratio 3 : 1. What does this suggest?', 'the molecule contains one chlorine atom', '³⁵Cl : ³⁷Cl ≈ 3 : 1.', ['the molecule contains one bromine atom', 'the molecule contains two chlorine atoms', 'the molecule contains ¹³C']),
    ('Why do bromine compounds show M and M+2 peaks of about equal height?', '⁷⁹Br and ⁸¹Br are present in roughly equal amounts', 'Natural abundance ratio about 1 : 1.', ['bromine has only one isotope', 'bromine atoms are very heavy', 'Br₂ molecules form']),
    ('State the formula used to find the number of carbon atoms from the M and M+1 peaks.', 'n = (100 × height of M+1)/(1.1 × height of M).', '[1]'),
])
t18b.fixed('C2', (2, 3, 4), [
    ('Explain why only positive ions are detected in a mass spectrometer, and why radicals formed on fragmentation are not.', 'Ions are deflected/accelerated by electric (and magnetic) fields and reach the detector; uncharged radicals are not affected and are not detected.', 'only charged particles accelerated/deflected [1]; radicals uncharged, not detected [1]'),
    ('Explain how fragmentation patterns help distinguish propan-1-ol from propan-2-ol.', 'Both have M⁺ = 60, but propan-1-ol gives a peak at m/z 31 (CH₂OH⁺) while propan-2-ol gives m/z 45 (CH₃CHOH⁺).', 'same M⁺ [1]; different characteristic fragments 31 vs 45 [1]'),
])
errs(t18b, [
    ('The tallest peak in a mass spectrum is always the molecular ion.', 'The tallest peak is the base peak, often a stable fragment; M⁺ is the peak with the highest m/z (apart from M+1/M+2).'),
    ('A compound with M⁺ peaks at m/z 108 and 110 of equal height contains two chlorine atoms.', 'Equal M and M+2 peaks show one bromine atom (⁷⁹Br : ⁸¹Br ≈ 1 : 1); one Cl gives 3 : 1.'),
])
c2mix(t18b, ['{p} interprets mass spectra in {lab}.', 'A drug-testing laboratory in {c} uses mass spectrometry to identify compounds.'])


@t18b.add('C3', (2, 3, 4, 5), 'numerical')
def t18b_m1(r, D):
    n = r.randint(2, 8)
    hM = r.choice([40.0, 55.0, 62.5, 72.0, 80.0, 90.0, 35.0, 48.0])
    h1 = round(1.1 * n * hM / 100, 2)
    nexp = 100 * h1 / (1.1 * hM)
    stem = f'In the mass spectrum of an organic compound, the M peak has a relative height of {hM} and the M+1 peak a relative height of {h1}. Calculate the number of carbon atoms in one molecule.'
    key = f'n = (100 × {h1})/(1.1 × {hM}) [1]; = {nexp:.2f} so {n} carbon atoms [1]'
    ans = f'{n}'
    if D >= 4:
        mzM = r.choice({2: [46, 60], 3: [58, 60, 74], 4: [72, 74, 88], 5: [86, 88], 6: [100, 86], 7: [100, 114], 8: [114, 128]}[n])
        stem += f' The molecular ion has m/z = {mzM}. Suggest a molecular formula containing only C, H and O.'
        rem = mzM - 12 * n
        sol = None
        for o in range(0, 4):
            h = rem - 16 * o
            if 0 < h <= 2 * n + 2 and h % 2 == 0:
                sol = (h, o)
                break
        if not sol:
            return None
        h, o = sol
        mf = F(f'C{n}H{h}' + (f'O{o}' if o > 1 else 'O' if o == 1 else ''))
        key += f'; remaining mass {rem} → {mf} [1]'
        ans += f'; {mf}'
    return {'stem': stem, 'answer': ans, 'key': key}


@t18b.add('C1', (1, 2, 3))
def t18b_frag(r, D):
    c = r.choice(list(MS18))
    M, fr = MS18[c]
    mz, ion_, rad = r.choice(fr)
    pool = ['CH₃⁺', 'C₂H₅⁺', 'CH₂OH⁺', 'CH₃CO⁺', 'COOH⁺', 'C₂H₅CO⁺', 'C₃H₇⁺', 'CHO⁺', 'C₃H₇CO⁺', 'COOCH₃⁺']
    pool = [p for p in pool if p not in ion_ and not (mz in (29,) and p in ('CHO⁺', 'C₂H₅⁺')) and not (mz == 43 and p in ('C₃H₇⁺', 'CH₃CO⁺')) and not (mz == 45 and p in ('COOH⁺', 'CH₃CHOH⁺'))]
    return mc(r, f'The mass spectrum of {c} (Mr = {M}) has a peak at m/z = {mz}. Which ion is responsible?', ion_, pool, f'M⁺ ({M}) → {ion_} (m/z {mz}) + {rad}.')


@t18b.add('C1', (1, 2, 3))
def t18b_hal(r, D):
    nm, f, peaks, ratio = r.choice(HALMS)
    corr = ' and '.join(str(p) for p in peaks) + f' in the ratio {ratio}'
    alt_ratio = {'3 : 1': ['1 : 1', '1 : 3'], '1 : 1': ['3 : 1', '1 : 2'], '9 : 6 : 1': ['1 : 2 : 1', '3 : 1 : 0'], '1 : 2 : 1': ['9 : 6 : 1', '1 : 1 : 1']}[ratio]
    pool = [' and '.join(str(p) for p in peaks) + f' in the ratio {x}' for x in alt_ratio] + [' and '.join(str(p - 2) for p in peaks) + f' in the ratio {ratio}', ' and '.join(str(p + 1) for p in peaks) + f' in the ratio {ratio}']
    return mc(r, f'Which molecular ion peaks are seen in the mass spectrum of {nm}, {f}? (Use ¹²C, ¹H, ³⁵Cl/³⁷Cl ≈ 3 : 1, ⁷⁹Br/⁸¹Br ≈ 1 : 1.)', corr, pool, f'{nm}: {corr}.')


@t18b.add('C3', (2, 3, 4, 5), 'short')
def t18b_interp(r, D):
    c = r.choice(list(MS18))
    M, fr = MS18[c]
    k = 1 if D <= 2 else min(2, len(fr))
    pick = r.sample(fr, k)
    stem = f'The mass spectrum of {c}, {SF16(c) if c in FORM16 else F(MSFORM[c])}, shows peaks at m/z = {M} and ' + ' and '.join(str(p[0]) for p in pick) + '. Identify the species responsible for each peak and write an equation for the formation of one of the fragment ions.'
    key = f'{M}: molecular ion M⁺ [1]; ' + '; '.join(f'{p[0]}: {p[1]} [1]' for p in pick) + f'; M⁺ → {pick[0][1]} + {pick[0][2]} [1]'
    ans = f'{M}: M⁺; ' + '; '.join(f'{p[0]}: {p[1]} (loss of {p[2]})' for p in pick)
    return {'stem': stem, 'answer': ans, 'key': key}


@t18b.add('C3', (2, 3, 4, 5), 'short')
def t18b_dist(r, D):
    pair = r.choice([('propan-1-ol', 'propan-2-ol'), ('propanal', 'propanone'), ('butanone', 'butane'), ('pentan-2-one', 'pentan-3-one'), ('ethanoic acid', 'propan-1-ol'), ('methyl ethanoate', 'propanoic acid')])
    a, b = pair
    Ma, fa = MS18[a]
    Mb, fb = MS18[b]
    ua = [x for x in fa if x[0] not in [y[0] for y in fb]]
    ub = [x for x in fb if x[0] not in [y[0] for y in fa]]
    if not ua or not ub:
        return None
    stem = f'Explain how mass spectrometry could distinguish {a} from {b}.'
    if Ma == Mb:
        key = f'same M⁺ at m/z {Ma} [1]; {a}: {ua[0][0]} ({ua[0][1]}) [1]; {b}: {ub[0][0]} ({ub[0][1]}) [1]'
    else:
        key = f'M⁺: {a} {Ma}, {b} {Mb} [1]; {a} fragment {ua[0][0]} ({ua[0][1]}) [1]; {b} fragment {ub[0][0]} ({ub[0][1]}) [1]'
    ans = f'{a}: M⁺ {Ma}, fragment {ua[0][0]} {ua[0][1]}; {b}: M⁺ {Mb}, fragment {ub[0][0]} {ub[0][1]}'
    return {'stem': stem, 'answer': ans, 'key': key}


def t18b_c4(r, D):
    c = r.choice(list(MS18))
    M, fr = MS18[c]
    n = NCARB18.get(c)
    if not n:
        return None
    hM = r.choice([50.0, 64.0, 80.0, 36.0])
    h1 = round(1.1 * n * hM / 100, 2)
    sf_ = SF16(c) if c in FORM16 else F(MSFORM[c])
    peaks = sorted({p[0] for p in fr})
    intro = P(r, f'{{p}} analyses an unknown compound Z in {{lab}}. Its mass spectrum has peaks at m/z = {", ".join(map(str, peaks))}, {M} and {M + 1}; the {M} and {M + 1} peaks have relative heights {hM} and {h1}. Z is {c}, {sf_}.')
    parts = [
        lambda r: ('Calculate the number of carbon atoms in Z from the M and M+1 peaks.', f'n = 100 × {h1}/(1.1 × {hM}) = {n}', '[2]'),
        lambda r: (f'Identify the species responsible for the peak at m/z {M}.', f'molecular ion, {c} minus one electron (M⁺)', '[1]'),
        lambda r: ('Identify the ions responsible for two of the fragment peaks.', '; '.join(f'{p[0]}: {p[1]}' for p in fr[:2]), '[2]'),
        lambda r: (f'Write an equation for the formation of the ion at m/z {fr[0][0]}.', f'M⁺ → {fr[0][1]} + {fr[0][2]}', '[1]'),
        lambda r: ('Explain why the radical formed is not detected.', 'It is uncharged, so it is not accelerated or deflected.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(0, 1, 2, 3))


NCARB18 = {'propanone': 3, 'propanal': 3, 'ethanol': 2, 'propan-1-ol': 3, 'propan-2-ol': 3, 'butane': 4, 'butanone': 4, 'pentan-3-one': 5, 'pentan-2-one': 5, 'ethanoic acid': 2,
           'methyl ethanoate': 3, 'ethyl ethanoate': 4, 'propanoic acid': 3, 'ethanal': 2}
c4reg(t18b, t18b_c4)

# ---------------------------------------------------------- 18.3 synthesis
SYN_EDGES = [
    ('ethene', 'ethanol', 'steam, H₃PO₄ catalyst, 300 °C, 6 MPa'), ('ethene', 'bromoethane', 'HBr(g), room temperature'), ('ethene', 'ethane', 'H₂, Ni catalyst, 150 °C'),
    ('ethene', '1,2-dibromoethane', 'Br₂, room temperature'), ('ethene', 'ethane-1,2-diol', 'cold dilute acidified KMnO₄'), ('ethane', 'bromoethane', 'Br₂, UV light'),
    ('bromoethane', 'ethanol', 'NaOH(aq), heat under reflux'), ('bromoethane', 'ethene', 'NaOH in ethanol, heat'), ('bromoethane', 'propanenitrile', 'KCN in ethanol, heat under reflux'),
    ('bromoethane', 'ethylamine', 'excess NH₃ in ethanol, heat in a sealed tube'), ('ethanol', 'ethanal', 'acidified K₂Cr₂O₇, warm, distil off product'),
    ('ethanol', 'ethanoic acid', 'excess acidified K₂Cr₂O₇, heat under reflux'), ('ethanol', 'ethene', 'heated Al₂O₃ (or conc. H₂SO₄, heat)'), ('ethanol', 'bromoethane', 'NaBr and conc. H₂SO₄, heat'),
    ('ethanal', 'ethanoic acid', 'acidified K₂Cr₂O₇, heat under reflux'), ('ethanal', 'ethanol', 'NaBH₄'), ('ethanal', '2-hydroxypropanenitrile', 'HCN (KCN + dilute H₂SO₄)'),
    ('2-hydroxypropanenitrile', '2-hydroxypropanoic acid', 'dilute HCl, heat under reflux'), ('propanenitrile', 'propanoic acid', 'dilute HCl, heat under reflux'),
    ('ethanoic acid', 'ethyl ethanoate', 'ethanol, conc. H₂SO₄ catalyst, heat under reflux'), ('ethanoic acid', 'methyl ethanoate', 'methanol, conc. H₂SO₄ catalyst, heat under reflux'),
    ('propene', 'propan-2-ol', 'steam, H₃PO₄ catalyst, 300 °C, 6 MPa'), ('propene', '2-bromopropane', 'HBr(g), room temperature'), ('propene', 'propane', 'H₂, Ni catalyst, 150 °C'),
    ('2-bromopropane', 'propan-2-ol', 'NaOH(aq), heat under reflux'), ('2-bromopropane', 'propene', 'NaOH in ethanol, heat'), ('propan-2-ol', 'propanone', 'acidified K₂Cr₂O₇, heat under reflux'),
    ('propan-2-ol', 'propene', 'heated Al₂O₃ (or conc. H₂SO₄, heat)'), ('propanone', 'propan-2-ol', 'NaBH₄'), ('propanone', '2-hydroxy-2-methylpropanenitrile', 'HCN (KCN + dilute H₂SO₄)'),
    ('2-hydroxy-2-methylpropanenitrile', '2-hydroxy-2-methylpropanoic acid', 'dilute HCl, heat under reflux'),
    ('propan-1-ol', 'propanal', 'acidified K₂Cr₂O₇, warm, distil off product'), ('propan-1-ol', 'propanoic acid', 'excess acidified K₂Cr₂O₇, heat under reflux'),
    ('propan-1-ol', 'propene', 'heated Al₂O₃ (or conc. H₂SO₄, heat)'), ('propan-1-ol', '1-bromopropane', 'NaBr and conc. H₂SO₄, heat'),
    ('1-bromopropane', 'propan-1-ol', 'NaOH(aq), heat under reflux'), ('1-bromopropane', 'butanenitrile', 'KCN in ethanol, heat under reflux'), ('1-bromopropane', 'propene', 'NaOH in ethanol, heat'),
    ('1-bromopropane', 'propylamine', 'excess NH₃ in ethanol, heat in a sealed tube'), ('butanenitrile', 'butanoic acid', 'dilute HCl, heat under reflux'),
    ('propanal', 'propanoic acid', 'acidified K₂Cr₂O₇, heat under reflux'), ('propanal', 'propan-1-ol', 'NaBH₄'), ('propanal', '2-hydroxybutanenitrile', 'HCN (KCN + dilute H₂SO₄)'),
    ('2-hydroxybutanenitrile', '2-hydroxybutanoic acid', 'dilute HCl, heat under reflux'), ('propanoic acid', 'methyl propanoate', 'methanol, conc. H₂SO₄ catalyst, heat under reflux'),
]
SYN_START = ['ethene', 'ethane', 'ethanol', 'bromoethane', 'propene', 'propan-1-ol', '1-bromopropane', 'propan-2-ol', '2-bromopropane']


def syn_paths(start):
    """BFS: shortest route from start to every reachable compound. Returns {target: [edge, ...]}."""
    from collections import deque
    best = {start: []}
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for e in SYN_EDGES:
            if e[0] == u and e[1] not in best:
                best[e[1]] = best[u] + [e]
                dq.append(e[1])
    return best


def syn_pick(r, steps):
    opts = []
    for s in SYN_START:
        for tgt, path in syn_paths(s).items():
            if len(path) == steps:
                opts.append((s, tgt, path))
    return r.choice(opts) if opts else None


def route_str(path):
    return '; '.join(f'step {i + 1}: {e[0]} → {e[1]} ({e[2]})' for i, e in enumerate(path))


t18c = topic('Designing multi-step synthetic routes using AS functional group reactions', 'designing multi-step synthetic routes', 'synthetic routes')
t18c.fixed('C1', (1, 2), [
    ('Which two-step route converts bromoethane into propanoic acid?', 'KCN in ethanol, then heat under reflux with dilute HCl', 'CH₃CH₂Br → CH₃CH₂CN → CH₃CH₂COOH (chain lengthened by one carbon).', ['NaOH(aq), then acidified K₂Cr₂O₇', 'NH₃, then dilute HCl', 'ethanolic NaOH, then steam']),
    ('Which reaction increases the length of a carbon chain by one carbon atom?', 'substitution of a halogenoalkane with cyanide ions', 'Also HCN addition to carbonyl compounds.', ['dehydration of an alcohol', 'oxidation of an alcohol', 'hydrolysis of an ester']),
    ('Which reagent converts propan-2-ol into propene?', 'heated aluminium oxide', 'Dehydration (elimination).', ['NaBH₄', 'acidified K₂Cr₂O₇', 'HBr']),
    ('What is the first step in converting ethene into ethanoic acid?', 'hydration with steam and a phosphoric acid catalyst', 'Ethanol is then oxidised under reflux with acidified dichromate(VI).', ['reaction with HCN', 'reduction with NaBH₄', 'reaction with ammonia']),
    ('Which compound must be made first to convert propene into propanone?', 'propan-2-ol', 'Hydration (Markovnikov) then oxidation of the secondary alcohol.', ['propan-1-ol', 'propanal', '1-bromopropane']),
    ('State one reason why chemists prefer routes with fewer steps.', 'Each step loses product, so fewer steps give a higher overall yield (and less waste/cost).', '[1]'),
])
t18c.fixed('C2', (2, 3, 4), [
    ('Explain why the overall yield of a multi-step synthesis is often low.', 'The overall yield is the product of the yields of each step; e.g. three steps of 70% give only 0.7³ ≈ 34%.', 'yields multiply [1]; example/each step loses product [1]'),
    ('Explain why the conversion of propene to propan-1-ol is not straightforward.', 'Hydration of propene gives mainly propan-2-ol (Markovnikov: more stable secondary carbocation), so propan-1-ol is only a minor product.', 'Markovnikov / secondary carbocation more stable [1]; propan-2-ol is major product [1]'),
])
errs(t18c, [
    ('Propanoic acid can be made from bromoethane by heating with aqueous NaOH and then oxidising.', 'NaOH(aq) gives ethanol, which oxidises to ethanoic acid (two carbons); to add a carbon use KCN then acid hydrolysis.'),
    ('Propanone is made from propene by adding HBr and then oxidising the bromoalkane.', 'Halogenoalkanes are not oxidised by dichromate; convert propene to propan-2-ol (steam/H₃PO₄ or via 2-bromopropane and NaOH(aq)) and then oxidise.'),
])
c2mix(t18c, ['{p} plans a synthesis for a project in {lab}.', 'A pharmaceutical company in {c} designs routes to small organic molecules.'])


@t18c.add('C1', (1, 2, 3))
def t18c_step(r, D):
    e = r.choice(SYN_EDGES)
    pool = list({x[2] for x in SYN_EDGES if x[2] != e[2]})
    return mc(r, f'Which reagents and conditions convert {e[0]} into {e[1]}?', e[2], pool, f'{e[0]} → {e[1]}: {e[2]}.')


@t18c.add('C1', (1, 2, 3))
def t18c_inter(r, D):
    x = syn_pick(r, 2)
    if not x:
        return None
    s, tgt, path = x
    mid = path[0][1]
    pool = list({e[1] for e in SYN_EDGES if e[1] not in (mid, tgt, s)})
    return mc(r, f'A two-step synthesis converts {s} into {tgt}. Which compound is the intermediate?', mid, pool, route_str(path) + '.')


@t18c.add('C3', (2, 3, 4, 5), 'short')
def t18c_route(r, D):
    x = syn_pick(r, 2 if D <= 3 else 3)
    if not x:
        return None
    s, tgt, path = x
    stem = f'Suggest a {len(path)}-step synthesis of {tgt}, {SF16(tgt)}, starting from {s}, {SF16(s)}. For each step give the reagents and conditions and name the intermediate(s).'
    key = '; '.join(f'step {i + 1} reagents/conditions: {e[2]} [1]' for i, e in enumerate(path)) + '; intermediate(s): ' + ', '.join(e[1] for e in path[:-1]) + f' [{len(path) - 1}]'
    return {'stem': stem, 'answer': route_str(path) + ' (any valid alternative route accepted)', 'key': key}


@t18c.add('C3', (3, 4, 5), 'numerical')
def t18c_yield(r, D):
    x = syn_pick(r, 3 if D >= 4 else 2)
    if not x:
        return None
    s, tgt, path = x
    ys = [r.choice([55, 62, 70, 75, 80, 85, 90]) for _ in path]
    tot = 1
    for y in ys:
        tot *= y / 100
    M1, M2 = M16(s), M16(tgt)
    m = r.choice([10.0, 15.0, 20.0, 25.0])
    mt = m / M1 * M2 * tot
    stem = (f'{who(r)} converts {s} into {tgt} by the route: {route_str(path)}. The yields of the steps are ' + ', '.join(f'{y}%' for y in ys) +
            f'. Calculate the overall percentage yield and the mass of {tgt} obtained from {m:.1f} g of {s}.')
    key = f'overall yield = {" × ".join(str(y / 100) for y in ys)} = {g3(tot * 100)}% [1]; n({s}) = {m:.1f}/{mr1(M1)} = {g3(m / M1)} mol [1]; mass = {g3(m / M1)} × {mr1(M2)} × {g3(tot)} = {g3(mt)} g [1]'
    return {'stem': stem, 'answer': f'{g3(tot * 100)}%; {g3(mt)} g', 'key': key}


def t18c_c4(r, D):
    x = syn_pick(r, 3) if D >= 4 else syn_pick(r, 2)
    if not x:
        return None
    s, tgt, path = x
    intro = P(r, f'{{p}} needs to make {tgt}, {SF16(tgt)}, from {s}, {SF16(s)}, in {{lab}}.')
    parts = [
        lambda r: ('Suggest a route, giving the intermediate(s).', ' → '.join([s] + [e[1] for e in path]), f'[{len(path) - 1}]'),
        lambda r: ('Give the reagents and conditions for each step.', '; '.join(e[2] for e in path), f'[{len(path)}]'),
        lambda r: ('State the type of reaction for the first step.', SYN_TYPE(path[0]), '[1]'),
        lambda r: ('Describe a chemical or spectroscopic test to show the final step is complete.', SYN_TEST(path[-1][1]), '[1]'),
        lambda r: ('Explain why the overall yield is lower than the yield of any single step.', 'Yields multiply; product is lost at every step.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step', need=(0,))


def SYN_TYPE(e):
    c = e[2]
    if 'steam' in c or 'HBr' in c or 'Br₂, room' in c:
        return 'electrophilic addition'
    if 'H₂, Ni' in c:
        return 'addition (hydrogenation/reduction)'
    if 'UV' in c:
        return 'free-radical substitution'
    if 'NaOH(aq)' in c or 'KCN' in c or 'NH₃' in c or 'NaBr' in c:
        return 'nucleophilic substitution'
    if 'NaOH in ethanol' in c or 'Al₂O₃' in c:
        return 'elimination'
    if 'K₂Cr₂O₇' in c or 'KMnO₄' in c:
        return 'oxidation'
    if 'NaBH₄' in c:
        return 'reduction (nucleophilic addition)'
    if 'HCN' in c:
        return 'nucleophilic addition'
    if 'HCl' in c:
        return 'hydrolysis'
    return 'condensation (esterification)'


def SYN_TEST(t):
    if t.endswith('acid'):
        return 'IR: very broad O–H 2500–3000 cm⁻¹ and C=O ~1710 cm⁻¹ (or effervescence with Na₂CO₃).'
    if t.endswith('nitrile'):
        return 'IR: C≡N absorption at 2200–2250 cm⁻¹.'
    if t.endswith('ol') and 'diol' not in t:
        return 'IR: broad O–H at 3200–3600 cm⁻¹ and no C=O.'
    if t.endswith('al'):
        return 'Tollens\' reagent gives a silver mirror (or IR C=O at ~1720 cm⁻¹).'
    if t.endswith('one'):
        return '2,4-DNPH gives an orange precipitate; Fehling\'s stays blue.'
    if t.endswith('ene'):
        return 'Bromine water is decolourised.'
    if t.endswith('oate'):
        return 'IR: C=O ~1740 cm⁻¹ and C–O, no O–H; fruity smell.'
    if t.startswith('bromo') or 'bromo' in t:
        return 'Warm with NaOH(aq), acidify with HNO₃, add AgNO₃: cream precipitate.'
    if t.endswith('amine'):
        return 'IR: N–H absorption at 3300–3500 cm⁻¹.'
    return 'Compare the IR spectrum with that of a pure sample (fingerprint region).'


c4reg(t18c, t18c_c4)

CHAPTERS[18] = [t18a, t18b, t18c]


finalize()
