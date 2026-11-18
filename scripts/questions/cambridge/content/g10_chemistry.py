"""Cambridge IGCSE Chemistry 0620 Extended (2026-28), CUP coursebook chapters 12-22 (grade 10).

Chapter order 1-11 here = coursebook 12 (salts) ... 22 (chemical analysis).
Data tables (ions, salts, metals, homologous series, tests) drive parameterised templates;
compose() builds Paper 4 / Paper 6 style structured items.
"""
import math
import re
from ._lib import topic, mcq, compose, sf, person, two_people, city, num_mcq, near

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# ===================================================================== helpers
_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
_SUP = str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')


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
    return ''.join(out) + charge.translate(_SUP)


def E(s):
    """Equation string -> Unicode with coefficients kept normal: '2Na + 2H2O -> 2NaOH + H2'."""
    toks = []
    for tok in s.split(' '):
        if tok == '->':
            toks.append('→')
        elif tok == '<=>':
            toks.append('⇌')
        elif tok in ('+', ''):
            toks.append(tok)
        else:
            m = re.match(r'^(\d+(?:/\d+)?)([A-Z(].*)$', tok)
            if m:
                toks.append(m.group(1) + F(m.group(2)))
            else:
                toks.append(F(tok))
    return ' '.join(toks)


AR = {'H': 1, 'He': 4, 'Li': 7, 'C': 12, 'N': 14, 'O': 16, 'F': 19, 'Ne': 20, 'Na': 23, 'Mg': 24, 'Al': 27, 'Si': 28, 'P': 31, 'S': 32,
      'Cl': 35.5, 'Ar': 40, 'K': 39, 'Ca': 40, 'Cr': 52, 'Mn': 55, 'Fe': 56, 'Co': 59, 'Ni': 59, 'Cu': 64, 'Zn': 65, 'Br': 80,
      'Ag': 108, 'Sn': 119, 'I': 127, 'Ba': 137, 'Pb': 207}


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
            el, n = m.group(1), int(m.group(2) or 1)
            stack[-1][el] = stack[-1].get(el, 0) + n
            i += len(m.group())
    return stack[0]


def atoms(s):
    tot = {}
    for part in s.split('.'):
        m = re.match(r'^(\d*)(.*)$', part)
        k = int(m.group(1) or 1)
        for el, n in _atoms(m.group(2)).items():
            tot[el] = tot.get(el, 0) + n * k
    return tot


def Mr(s):
    return sum(AR[el] * n for el, n in atoms(s).items())


def mr(x):
    """Format an Mr / mass nicely."""
    return sf(x, 4) if abs(x - round(x)) > 1e-9 else str(int(round(x)))


def g3(x):
    # nudge so exact halves (e.g. 1.575) round up, as a mark scheme would
    return sf(x * (1 + 1e-12), 3)


def r3(x):
    return float(g3(x).replace(',', ''))


def cap(s):
    return s[0].upper() + s[1:]


def art(word):
    return ('an ' if word[0] in 'aeiou' else 'a ') + word


def neg(s):
    return re.sub(r'(?<![\w])-(\d)', '−\\1', s)


def opts4(r, correct, pool):
    return mcq(r, correct, [p for p in pool if p != correct])


def mcq_q(r, stem, correct, pool, key):
    o, a = opts4(r, correct, pool)
    return {'stem': stem, 'options': o, 'answer': a, 'key': key}


def nmcq(r, stem, val, wrong, unit, key, f=g3):
    o, a = num_mcq(r, val, wrong, fmtf=f, unit=unit)
    return {'stem': stem, 'options': o, 'answer': a, 'key': key}


def lead(r, D, words=('State', 'Give')):
    return r.choice(words)


SCHOOLS = ['a school laboratory', 'a college laboratory', 'a water-testing laboratory', 'a chemistry club', 'a sixth-form practical class', 'a quality-control laboratory']


def lab(r):
    return r.choice(SCHOOLS)


def who(r):
    return f'{person(r)}, a student in {city(r)},'


VOL = 24.0  # dm³ per mole at r.t.p.


# ===================================================================== ions and salts
CAT = {  # key: (name, symbol(ascii), charge)
    'Na': ('sodium', 'Na', 1), 'K': ('potassium', 'K', 1), 'NH4': ('ammonium', 'NH4', 1), 'Li': ('lithium', 'Li', 1), 'Ag': ('silver', 'Ag', 1),
    'Mg': ('magnesium', 'Mg', 2), 'Ca': ('calcium', 'Ca', 2), 'Ba': ('barium', 'Ba', 2), 'Zn': ('zinc', 'Zn', 2), 'Cu': ('copper(II)', 'Cu', 2),
    'Fe2': ('iron(II)', 'Fe', 2), 'Fe3': ('iron(III)', 'Fe', 3), 'Pb': ('lead(II)', 'Pb', 2), 'Al': ('aluminium', 'Al', 3),
}
AN = {
    'Cl': ('chloride', 'Cl', 1), 'NO3': ('nitrate', 'NO3', 1), 'SO4': ('sulfate', 'SO4', 2), 'CO3': ('carbonate', 'CO3', 2), 'OH': ('hydroxide', 'OH', 1),
    'Br': ('bromide', 'Br', 1), 'I': ('iodide', 'I', 1),
}
POLY = {'NH4', 'NO3', 'SO4', 'CO3', 'OH'}
ACID = {'Cl': ('hydrochloric acid', 'HCl', 1), 'NO3': ('nitric acid', 'HNO3', 1), 'SO4': ('sulfuric acid', 'H2SO4', 2)}


def salt_f(c, a):
    cq, aq = CAT[c][2], AN[a][2]
    l = cq * aq // math.gcd(cq, aq)
    nc, na = l // cq, l // aq
    cs, as_ = CAT[c][1], AN[a][1]
    left = (f'({cs}){nc}' if cs in POLY else f'{cs}{nc}') if nc > 1 else cs
    right = (f'({as_}){na}' if as_ in POLY else f'{as_}{na}') if na > 1 else as_
    return left + right


def salt_n(c, a):
    return f'{CAT[c][0]} {AN[a][0]}'


def soluble(c, a):
    if c in ('Na', 'K', 'NH4', 'Li'):
        return True
    if a == 'NO3':
        return True
    if a in ('Cl', 'Br', 'I'):
        return c not in ('Ag', 'Pb')
    if a == 'SO4':
        return c not in ('Ba', 'Ca', 'Pb')
    return False  # carbonates, hydroxides


RULE = {
    'group1': 'all sodium, potassium and ammonium salts are soluble',
    'NO3': 'all nitrates are soluble',
    'Cl': 'chlorides are soluble except silver chloride and lead(II) chloride',
    'SO4': 'sulfates are soluble except barium, calcium and lead(II) sulfates',
    'CO3': 'carbonates are insoluble except sodium, potassium and ammonium carbonates',
    'OH': 'hydroxides are insoluble except sodium, potassium and ammonium hydroxides (calcium hydroxide is slightly soluble)',
}


def rule_for(c, a):
    if c in ('Na', 'K', 'NH4', 'Li') and a not in ('Cl',):
        return RULE['group1']
    return RULE.get(a, RULE['group1'])


RULE_SALTS = [(c, a) for c in ('Na', 'K', 'NH4', 'Mg', 'Ca', 'Ba', 'Zn', 'Cu', 'Fe2', 'Fe3', 'Pb', 'Ag', 'Al') for a in ('Cl', 'NO3', 'SO4', 'CO3', 'OH')
              if not ((c, a) in {('Ag', 'OH'), ('Al', 'CO3'), ('Fe3', 'CO3'), ('NH4', 'OH'), ('Ca', 'OH'), ('Ag', 'SO4'), ('Ag', 'CO3')})]
SOL = [x for x in RULE_SALTS if soluble(*x)]
INSOL = [x for x in RULE_SALTS if not soluble(*x)]


def method_for(c, a):
    if not soluble(c, a):
        return 'precipitation'
    if c in ('Na', 'K', 'NH4'):
        return 'titration'
    return 'excess'


METHOD_TXT = {
    'precipitation': 'precipitation: mix two aqueous solutions, one containing each ion, then filter, wash and dry the precipitate',
    'titration': 'titration: neutralise the alkali exactly with the acid using an indicator, repeat without indicator, then crystallise',
    'excess': 'excess insoluble solid method: add an excess of the insoluble base, carbonate or metal to warm acid, filter off the excess, heat the filtrate to the point of crystallisation, cool and dry the crystals',
}

# soluble salts made by the excess method: (cation, anion, base options)
EXCESS = []
for _c, _m in (('Mg', 'Mg'), ('Zn', 'Zn'), ('Cu', 'Cu'), ('Fe2', 'Fe')):
    for _a in ('Cl', 'SO4', 'NO3'):
        bases = [(f'{_m}O', 'oxide'), (f'{_m}CO3', 'carbonate')]
        if _m in ('Mg', 'Zn', 'Fe'):
            bases.append((_m, 'metal'))
        if _m in ('Cu', 'Mg', 'Zn'):
            bases.append((f'{_m}(OH)2', 'hydroxide'))
        EXCESS.append((_c, _a, bases))
BASE_NAME = {'oxide': 'oxide', 'carbonate': 'carbonate', 'metal': '', 'hydroxide': 'hydroxide'}


def base_name(c, kind):
    if kind == 'metal':
        return {'Mg': 'magnesium', 'Zn': 'zinc', 'Fe2': 'iron'}[c]
    return f'{CAT[c][0]} {kind}'


def excess_eq(c, a, base, kind):
    """Balanced equation for a divalent metal base + acid."""
    acid = ACID[a][1]
    k = 2 if ACID[a][2] == 1 else 1
    sf_ = salt_f(c, a)
    ac = f'{k}{acid}' if k > 1 else acid
    if kind == 'oxide':
        return f'{base} + {ac} -> {sf_} + H2O'
    if kind == 'carbonate':
        return f'{base} + {ac} -> {sf_} + H2O + CO2'
    if kind == 'hydroxide':
        return f'{base} + {ac} -> {sf_} + 2H2O'
    return f'{base} + {ac} -> {sf_} + H2'


def by_product(kind):
    return {'oxide': 'water', 'carbonate': 'water and carbon dioxide', 'hydroxide': 'water', 'metal': 'hydrogen'}[kind]


ALK = [('NaOH', 'sodium hydroxide', 'Na', 1), ('KOH', 'potassium hydroxide', 'K', 1), ('NH3', 'aqueous ammonia', 'NH4', 1)]


def neut_eq(alk, a):
    """alk formula, anion key -> equation, alkali:acid mole ratio (alkali per acid)."""
    acid = ACID[a][1]
    if alk == 'NH3':
        if a == 'SO4':
            return '2NH3 + H2SO4 -> (NH4)2SO4', 2
        return f'NH3 + {acid} -> NH4{AN[a][1]}', 1
    m = alk[:-2]
    if a == 'SO4':
        return f'2{alk} + H2SO4 -> {m}2SO4 + 2H2O', 2
    return f'{alk} + {acid} -> {m}{AN[a][1]} + H2O', 1


# insoluble salts by precipitation: (cation, anion)
PPT = [('Ba', 'SO4'), ('Pb', 'SO4'), ('Ca', 'SO4'), ('Ag', 'Cl'), ('Pb', 'Cl'), ('Ca', 'CO3'), ('Mg', 'CO3'), ('Zn', 'CO3'), ('Cu', 'CO3'), ('Ba', 'CO3'), ('Pb', 'CO3'), ('Fe2', 'CO3'), ('Pb', 'I'), ('Ag', 'Br'), ('Ag', 'I')]
PPT_COL = {('Ag', 'Cl'): 'white', ('Ag', 'Br'): 'cream', ('Ag', 'I'): 'yellow', ('Pb', 'I'): 'bright yellow', ('Cu', 'CO3'): 'blue-green', ('Fe2', 'CO3'): 'pale green'}


def ppt_col(c, a):
    return PPT_COL.get((c, a), 'white')


def ppt_reagents(c, a, alt=0):
    """Soluble reagents: (cation salt formula, name), (anion salt formula, name), equation, ionic equation."""
    p, q = CAT[c][2], AN[a][2]
    cat_salt = salt_f(c, 'NO3'); cat_name = salt_n(c, 'NO3')
    if alt and c in ('Ba', 'Ca', 'Mg', 'Zn', 'Cu', 'Fe2') and a != 'Cl':
        cat_salt = salt_f(c, 'Cl'); cat_name = salt_n(c, 'Cl')
    spec = 'K' if (alt and a in ('Cl', 'SO4', 'I', 'Br')) else 'Na'
    an_salt = salt_f(spec, a); an_name = salt_n(spec, a)
    l = p * q // math.gcd(p, q)
    na, nb = l // p, l // q
    prod = salt_f(c, a)
    side_an = 'NO3' if cat_salt.endswith(('NO3', 'NO3)2', 'NO3)3')) else 'Cl'
    side = salt_f(spec, side_an)
    nside = na * p
    def co(n, s):
        return f'{n}{s}' if n > 1 else s
    eq = f'{co(na, cat_salt)} + {co(nb, an_salt)} -> {prod} + {co(nside, side)}'
    ion = f'{co(na, CAT[c][1] + "^" + (str(p) if p > 1 else "") + "+")} + {co(nb, AN[a][1] + "^" + (str(q) if q > 1 else "") + "-")} -> {prod}'
    return (cat_salt, cat_name), (an_salt, an_name), eq, ion, (side, salt_n(spec, side_an))


HYDRATES = [  # anhydrous formula, name, x, colour change on heating
    ('CuSO4', 'copper(II) sulfate', 5, 'blue crystals turn to a white powder'),
    ('MgSO4', 'magnesium sulfate', 7, 'colourless crystals turn to a white powder'),
    ('ZnSO4', 'zinc sulfate', 7, 'colourless crystals turn to a white powder'),
    ('FeSO4', 'iron(II) sulfate', 7, 'pale green crystals turn to a white/pale yellow solid'),
    ('Na2CO3', 'sodium carbonate', 10, 'colourless crystals turn to a white powder'),
    ('CoCl2', 'cobalt(II) chloride', 6, 'pink crystals turn blue'),
    ('BaCl2', 'barium chloride', 2, 'colourless crystals turn to a white powder'),
    ('Na2SO4', 'sodium sulfate', 10, 'colourless crystals turn to a white powder'),
    ('CaCl2', 'calcium chloride', 6, 'colourless crystals turn to a white solid'),
]


# ===================================================================== Ch1 (CB12) Preparation of salts
t1a = topic('Solubility rules', 'solubility rules for salts, hydroxides and carbonates', 'solubility rules', 'salts hydroxides carbonates')
t1a.fixed('C1', (1, 2), [
    ('Which statement about the solubility of salts in water is correct?', 'All nitrates are soluble.', 'Solubility rules: all nitrates are soluble; all sodium, potassium and ammonium salts are soluble.',
     ['All carbonates are soluble.', 'All chlorides are insoluble.', 'All sulfates are insoluble.']),
    ('Which hydroxide is soluble in water?', 'potassium hydroxide', 'Hydroxides are insoluble except those of sodium, potassium and ammonium (calcium hydroxide slightly).', ['copper(II) hydroxide', 'iron(III) hydroxide', 'magnesium hydroxide']),
    ('Which pair of chlorides are both insoluble in water?', 'silver chloride and lead(II) chloride', 'Chlorides are soluble except AgCl and PbCl₂.', ['sodium chloride and silver chloride', 'lead(II) chloride and zinc chloride', 'barium chloride and copper(II) chloride']),
    ('Which three sulfates are insoluble in water?', 'barium sulfate, calcium sulfate and lead(II) sulfate', 'Sulfates are soluble except those of barium, calcium and lead.', ['sodium sulfate, copper(II) sulfate and zinc sulfate',
     'magnesium sulfate, iron(II) sulfate and barium sulfate', 'potassium sulfate, calcium sulfate and ammonium sulfate']),
    ('State the general solubility rule for carbonates.', 'Carbonates are insoluble except sodium, potassium and ammonium carbonates.', '1 mark: insoluble; 1 mark: exceptions Na, K, NH₄⁺ [2]'),
    ('State the general solubility rule for salts of sodium, potassium and ammonium.', 'They are all soluble in water.', '[1]'),
])
t1a.fixed('C2', (2, 3), [
    ('A student says, "Calcium carbonate is soluble because all calcium compounds dissolve." Explain why this is wrong.', 'Carbonates are insoluble except those of sodium, potassium and ammonium; calcium carbonate is insoluble (e.g. limestone does not dissolve in water).', '1 mark: carbonate rule; 1 mark: CaCO₃ insoluble [2]'),
    ('Explain why barium sulfate can be prepared by mixing two solutions but zinc sulfate cannot.', 'Barium sulfate is insoluble so it forms as a precipitate that can be filtered off; zinc sulfate is soluble so it stays dissolved with the other product and cannot be separated by filtration.', '1 mark: BaSO₄ insoluble/precipitates; 1 mark: ZnSO₄ soluble, stays in solution [2]'),
    ('Explain why the solubility rules tell you that every nitrate salt can be used as a source of a metal ion in solution.', 'All nitrates are soluble, so a metal nitrate dissolves to give the metal ions in aqueous solution.', '1 mark: all nitrates soluble; 1 mark: provides aqueous cations [2]'),
    ('Explain why sodium carbonate solution is used, rather than calcium carbonate, to provide carbonate ions for a precipitation.', 'Sodium carbonate is soluble, so it provides carbonate ions in solution; calcium carbonate is insoluble and provides no free carbonate ions.', '1 mark each [2]'),
    ('Distinguish between a soluble and an insoluble salt, giving one example of each.', 'A soluble salt dissolves in water to form a solution (e.g. sodium chloride); an insoluble salt does not dissolve appreciably (e.g. silver chloride).', '1 mark each with example [2]'),
])


@t1a.add('C1', (1, 2, 3))
def t1a_which(r, D):
    want = r.choice(['insoluble', 'soluble'])
    if want == 'insoluble':
        c = r.choice(INSOL); ds = r.sample(SOL, 6)
    else:
        c = r.choice(SOL); ds = r.sample(INSOL, 6)
    cn = salt_n(*c)
    pool = [salt_n(*d) for d in ds]
    stem = r.choice([f'Which salt is {want} in water?', f'Which compound is {want} in water?', f'A technician needs a compound that is {want} in water. Which one should be chosen?'])
    return mcq_q(r, stem, cn, pool, f'{cap(cn)} ({F(salt_f(*c))}) is {want}: {rule_for(*c)}.')


@t1a.add('C1', (1, 2, 3))
def t1a_state(r, D):
    cs = r.sample(RULE_SALTS, 3)
    stem = 'State whether each of these compounds is soluble or insoluble in water: ' + ', '.join(f'{salt_n(*c)} ({F(salt_f(*c))})' for c in cs) + '.'
    ans = '; '.join(f'{salt_n(*c)}: {"soluble" if soluble(*c) else "insoluble"}' for c in cs)
    return {'stem': stem, 'answer': ans, 'key': '1 mark for each correct answer [3] (' + '; '.join(rule_for(*c) for c in cs) + ')', 'type': 'short', 'marks': 3 if D >= 2 else 2}


@t1a.add('C2', (2, 3, 4), 'explain')
def t1a_explain(r, D):
    c = r.choice(RULE_SALTS)
    s = soluble(*c)
    p = person(r)
    claim = 'insoluble' if s else 'soluble'
    return {'stem': f'{p} predicts that {salt_n(*c)}, {F(salt_f(*c))}, is {claim} in water. Use the solubility rules to explain whether {p} is correct.',
            'answer': f'{p} is incorrect: {salt_n(*c)} is {"soluble" if s else "insoluble"} because {rule_for(*c)}.',
            'key': f'1 mark: correct conclusion ({"soluble" if s else "insoluble"}); 1 mark: rule quoted ({rule_for(*c)}) [2]'}


def _mix_pair(r):
    """Two soluble salts whose mixing gives (or does not give) a precipitate."""
    c1 = r.choice(['Ba', 'Pb', 'Ca', 'Ag', 'Mg', 'Zn', 'Cu', 'Fe2', 'Fe3', 'Al', 'K', 'NH4'])
    a1 = 'NO3'
    if c1 in ('Ba', 'Ca', 'Mg', 'Zn', 'Cu', 'Fe2', 'Fe3', 'Al', 'K', 'NH4') and r.random() < 0.5:
        a1 = 'Cl' if c1 not in ('Ag', 'Pb') else 'NO3'
    c2 = r.choice(['Na', 'K'])
    a2 = r.choice(['Cl', 'SO4', 'CO3', 'OH', 'NO3'])
    return (c1, a1), (c2, a2)


@t1a.add('C3', (2, 3, 4))
def t1a_predict(r, D):
    for _ in range(30):
        (c1, a1), (c2, a2) = _mix_pair(r)
        if a1 != a2 and (c1, a2) not in {('Ag', 'OH'), ('Al', 'CO3'), ('Fe3', 'CO3'), ('NH4', 'OH'), ('Ca', 'OH'), ('Ag', 'SO4'), ('Ag', 'CO3')}:
            break
    s1, s2 = salt_n(c1, a1), salt_n(c2, a2)
    pp = [(c1, a2), (c2, a1)]
    insol = [x for x in pp if not soluble(*x)]
    if insol:
        x = insol[0]
        ans = f'Yes: {salt_n(*x)}, {F(salt_f(*x))}, precipitates because {rule_for(*x)}.'
    else:
        ans = f'No precipitate: both possible products, {salt_n(*pp[0])} and {salt_n(*pp[1])}, are soluble.'
    if D == 2:
        corr = salt_n(*insol[0]) if insol else 'no precipitate forms'
        pool = [salt_n(*pp[1]), s1, s2, 'no precipitate forms', salt_n(*pp[0]), 'hydrogen gas', 'water']
        return mcq_q(r, f'Aqueous {s1} is mixed with aqueous {s2}. Which substance, if any, forms as a precipitate?', corr, pool, ans)
    stem = f'Aqueous {s1} is added to aqueous {s2}. Predict whether a precipitate forms. If it does, name it and write the ionic equation, with state symbols.'
    key = ans
    if insol:
        x = insol[0]
        p, q = CAT[x[0]][2], AN[x[1]][2]
        l = p * q // math.gcd(p, q)
        na, nb = l // p, l // q
        ion = f'{(str(na) if na > 1 else "")}{F(CAT[x[0]][1] + "^" + (str(p) if p > 1 else "") + "+")}(aq) + {(str(nb) if nb > 1 else "")}{F(AN[x[1]][1] + "^" + (str(q) if q > 1 else "") + "-")}(aq) → {F(salt_f(*x))}(s)'
        ans += f' Ionic equation: {ion}'
        key = f'1 mark: precipitate named ({salt_n(*x)}); 1 mark: ionic equation {ion}; 1 mark: state symbols [3]'
    else:
        key = f'1 mark: no precipitate; 1 mark: both products soluble ({RULE["NO3"] if "NO3" in (a1, a2) else RULE["group1"]}) [2]'
    return {'stem': stem, 'answer': ans, 'key': key}


@t1a.add('C3', (1, 2, 3))
def t1a_table(r, D):
    cs = r.sample(RULE_SALTS, 5)
    k = sum(1 for c in cs if not soluble(*c))
    names = ', '.join(salt_n(*c) for c in cs)
    if D == 1:
        return nmcq(r, f'How many of these compounds are insoluble in water? {names}', k, [x for x in range(0, 6) if x != k], '', 'Insoluble: ' + (', '.join(salt_n(*c) for c in cs if not soluble(*c)) or 'none') + '.', f=lambda x: str(int(x)))
    return {'stem': f'A technician has samples of {names}. Using the solubility rules, sort them into soluble and insoluble compounds.',
            'answer': 'Soluble: ' + (', '.join(salt_n(*c) for c in cs if soluble(*c)) or 'none') + '. Insoluble: ' + (', '.join(salt_n(*c) for c in cs if not soluble(*c)) or 'none') + '.',
            'key': 'All five correct [3]; four correct [2]; three correct [1].', 'marks': 3}


def _sol_c4(r, D):
    tgt = r.choice([x for x in RULE_SALTS if x[1] in ACID or not soluble(*x)])
    m = method_for(*tgt)
    p = person(r)
    tn, tf = salt_n(*tgt), F(salt_f(*tgt))
    intro = r.choice([f'{p} is asked to prepare a pure, dry sample of {tn}, {tf}, in {lab(r)}.', f'A chemical supplier in {city(r)} needs a sample of {tn}, {tf}.',
                      f'{p} reads that {tn}, {tf}, is used in industry and wants to make some in the laboratory.'])
    parts = [
        lambda r: (f'State whether {tn} is soluble or insoluble in water.', 'soluble' if soluble(*tgt) else 'insoluble', f'{rule_for(*tgt)} [1]'),
        lambda r: ('Name the most suitable method of preparation and explain your choice.', METHOD_TXT[m].split(':')[0],
                   f'1 mark: {m}; 1 mark: reason (salt is {"insoluble" if m == "precipitation" else ("soluble and made from an alkali, so an indicator is needed to find the end-point" if m == "titration" else "soluble and the base/carbonate is insoluble, so excess can be filtered off")}) [2]'),
        lambda r: ('Outline the main steps of the method.', METHOD_TXT[m].split(':')[1].strip(), '1 mark per correct step, up to [3]'),
    ]
    if m == 'precipitation':
        (cs_, cn_), (as_, an_), eq, ion, side = ppt_reagents(*tgt)
        parts += [lambda r: ('Name two aqueous reagents you could mix to make this salt.', f'{cn_} and {an_}', '1 mark each soluble reagent [2]'),
                  lambda r: (f'Write the balanced symbol equation for the reaction between aqueous {cn_} and aqueous {an_}.', E(eq), '1 mark formulae; 1 mark balancing [2]'),
                  lambda r: ('Explain why the precipitate is washed with distilled water before drying.', f'To remove the soluble {side[1]} and any unreacted solution from the surface of the solid.', '[2]')]
    elif m == 'titration':
        a = tgt[1] if tgt[1] in ACID else 'Cl'
        alk = {'Na': 'NaOH', 'K': 'KOH', 'NH4': 'NH3'}[tgt[0]]
        if tgt[1] in ACID:
            eq, _ = neut_eq(alk, a)
            parts += [lambda r: ('Name the acid and the alkali you would use.', f'{ACID[a][0]} and {dict((x[0], x[1]) for x in ALK)[alk]}', '1 mark each [2]'),
                      lambda r: ('Write the balanced symbol equation for the neutralisation reaction used.', E(eq), '1 mark formulae; 1 mark balancing [2]'),
                      lambda r: ('Explain why the titration is repeated without the indicator before crystallising.', 'The indicator would contaminate the salt; using the known volumes gives a pure neutral solution.', '[2]')]
    else:
        ex = [e for e in EXCESS if e[0] == tgt[0] and e[1] == tgt[1]]
        if ex:
            base, kind = r.choice(ex[0][2])
            eq = excess_eq(tgt[0], tgt[1], base, kind)
            parts += [lambda r: ('Name an acid and a suitable insoluble reactant.', f'{ACID[tgt[1]][0]} and {base_name(tgt[0], kind)}', '1 mark each [2]'),
                      lambda r: (f'Write the balanced symbol equation for the reaction of {base_name(tgt[0], kind)} with {ACID[tgt[1]][0]}.', E(eq), '1 mark formulae; 1 mark balancing [2]'),
                      lambda r: ('Explain how you would know when the reactant is in excess.', 'Solid remains undissolved at the bottom' + (' and fizzing stops.' if kind in ('carbonate', 'metal') else '.'), '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1a.add('C4', (2, 3, 4, 5), 'multi_step')(_sol_c4)
t1a.add('C3', (3, 4), 'multi_step')(_sol_c4)


# ---------------------------------------------------------- 1.2 excess insoluble base
t1b = topic('Soluble salt from acid and excess insoluble base', 'preparing a soluble salt from an acid and an excess insoluble base or carbonate', 'excess insoluble base or carbonate')
t1b.fixed('C1', (1, 2), [
    ('Why is the insoluble base added in excess when a soluble salt is prepared from an acid?', 'To make sure all the acid reacts', 'Excess base ensures all the acid is used up; the unreacted solid is then removed by filtration.',
     ['To make the salt insoluble', 'To speed up crystallisation', 'To neutralise the salt']),
    ('How is the unreacted excess copper(II) oxide removed from copper(II) sulfate solution?', 'filtration', 'The excess solid oxide is insoluble and stays on the filter paper; the filtrate is the salt solution.', ['crystallisation', 'distillation', 'chromatography']),
    ('Which pair of reagents can be used to make zinc chloride by the excess-solid method?', 'zinc carbonate and hydrochloric acid', 'Excess insoluble ZnCO₃ + HCl → ZnCl₂ + H₂O + CO₂.', ['zinc nitrate and sodium chloride', 'zinc oxide and sulfuric acid', 'zinc carbonate and nitric acid']),
    ('Which observation shows that excess magnesium carbonate has been added to dilute sulfuric acid?', 'Fizzing stops and solid remains in the flask', 'No more CO₂ is produced and undissolved carbonate remains, so all the acid has reacted.',
     ['The solution turns blue', 'A white precipitate forms immediately', 'The mixture becomes colder']),
    ('Why is copper metal not used with dilute sulfuric acid to make copper(II) sulfate?', 'Copper is below hydrogen in the reactivity series and does not react', 'Cu does not displace hydrogen from dilute acids; use CuO or CuCO₃ instead.',
     ['Copper reacts too violently', 'Copper sulfate is insoluble', 'Copper forms a precipitate with the acid']),
    ('State why the filtrate is heated only until crystals start to form, rather than to dryness.', 'Heating to dryness would remove the water of crystallisation / could decompose the salt; crystals form as the saturated solution cools.', '[1]'),
])
t1b.fixed('C2', (2, 3, 4), [
    ('Explain why the acid is often warmed before the insoluble base is added.', 'The reaction is faster at a higher temperature, so the base dissolves/reacts more quickly.', '1 mark: faster rate; 1 mark: particles have more energy / more frequent collisions [2]'),
    ('Explain why the excess-solid method cannot be used to make sodium sulfate.', 'Sodium compounds (oxide, hydroxide, carbonate) are soluble, so any excess would dissolve and could not be filtered off; titration is used instead.', '1 mark: sodium bases soluble; 1 mark: excess cannot be removed by filtration [2]'),
    ('Explain why calcium carbonate and dilute sulfuric acid are not used to prepare calcium sulfate crystals.', 'Calcium sulfate is insoluble; it coats the carbonate and the reaction soon stops, and the salt cannot be crystallised from solution.', '1 mark: CaSO₄ insoluble; 1 mark: layer stops reaction / salt not in solution [2]'),
    ('Explain why crystals are dried between filter papers or in a warm oven rather than by strong heating.', 'Strong heating would remove water of crystallisation (or decompose the salt), changing its appearance and composition.', '1 mark each [2]'),
    ('A student adds copper(II) oxide to dilute sulfuric acid until no more dissolves and then filters. Describe what is seen in the filter paper and in the filtrate.', 'Black solid (excess copper(II) oxide) in the filter paper; blue solution of copper(II) sulfate as the filtrate.', '1 mark each [2]'),
    ('Explain how you could tell that a sample of the crystals is pure.', 'Pure crystals have a sharp melting point (or, for a hydrate, are uniform in shape and colour); impurities widen and lower the melting range.', '[2]'),
])


@t1b.add('C1', (1, 2, 3))
def t1b_pair(r, D):
    c, a, bases = r.choice(EXCESS)
    base, kind = r.choice(bases)
    tgt = salt_n(c, a)
    corr = f'{base_name(c, kind)} and {ACID[a][0]}'
    other_a = [x for x in ACID if x != a]
    pool = [f'{base_name(c, kind)} and {ACID[x][0]}' for x in other_a] + [f'{salt_n(c, "NO3" if a != "NO3" else "Cl")} and {salt_n("Na", a)}', f'sodium {AN[a][0]} and {CAT[c][0]} metal' if kind != 'metal' else f'{CAT[c][0]} oxide and {ACID[other_a[0]][0]}']
    return mcq_q(r, f'Which pair of reagents could be used to make crystals of {tgt} by adding an excess of an insoluble solid to an acid?', corr, pool,
                 f'{E(excess_eq(c, a, base, kind))}. The acid must provide the {AN[a][0]} ion and the solid the {CAT[c][0]} ion.')


@t1b.add('C2', (2, 3, 4), 'explain')
def t1b_error(r, D):
    c, a, bases = r.choice(EXCESS)
    base, kind = r.choice(bases)
    errs = [
        (f'filtered the mixture before the {base_name(c, kind)} was in excess', 'Some acid would remain unreacted in the filtrate, so the crystals would be contaminated with acid / the yield lower. Keep adding solid until some remains undissolved.'),
        (f'heated the filtrate of {salt_n(c, a)} to dryness in an evaporating basin', 'Heating to dryness removes water of crystallisation (and may decompose the salt), giving a powder rather than hydrated crystals. Heat to the point of crystallisation then leave to cool.'),
        ('kept the filter paper and threw away the filtrate', 'The salt is dissolved in the filtrate; the residue is only the excess solid. The filtrate should be kept and crystallised.'),
        (f'used {ACID[[x for x in ACID if x != a][0]][0]} as the acid', f'That acid would give {salt_n(c, [x for x in ACID if x != a][0])}, not {salt_n(c, a)}; the acid must supply the {AN[a][0]} ion.'),
    ]
    e, fix = r.choice(errs)
    return {'stem': f'{person(r)} tried to make crystals of {salt_n(c, a)} from {base_name(c, kind)} and an acid but {e}. Explain what is wrong with this step and how it should be corrected.',
            'answer': fix, 'key': '1 mark: identifies the consequence; 1 mark: correct procedure [2]'}


@t1b.add('C3', (1, 2, 3))
def t1b_eq(r, D):
    c, a, bases = r.choice(EXCESS)
    base, kind = r.choice(bases)
    eq = E(excess_eq(c, a, base, kind))
    if D == 1:
        prods = {'oxide': 'salt + water', 'carbonate': 'salt + water + carbon dioxide', 'metal': 'salt + hydrogen', 'hydroxide': 'salt + water'}
        return mcq_q(r, f'{cap(base_name(c, kind))} reacts with {ACID[a][0]}. What are the products?', prods[kind], ['salt + water', 'salt + water + carbon dioxide', 'salt + hydrogen', 'salt + oxygen', 'salt + hydrogen + water'], eq)
    return {'stem': f'Write the balanced symbol equation for the reaction between {base_name(c, kind)} and {ACID[a][0]} to make {salt_n(c, a)}.' + (' Include state symbols.' if D >= 3 else ''),
            'answer': eq + (' (states: base (s), acid (aq), salt (aq), water (l), gas (g))' if D >= 3 else ''), 'key': f'{eq}: 1 mark correct formulae; 1 mark balancing' + ('; 1 mark state symbols [3]' if D >= 3 else ' [2]')}


HYD_OF = {('Cu', 'SO4'): ('CuSO4.5H2O', 'copper(II) sulfate-5-water'), ('Mg', 'SO4'): ('MgSO4.7H2O', 'magnesium sulfate-7-water'), ('Zn', 'SO4'): ('ZnSO4.7H2O', 'zinc sulfate-7-water'),
          ('Fe2', 'SO4'): ('FeSO4.7H2O', 'iron(II) sulfate-7-water')}


@t1b.add('C3', (2, 3, 4, 5), 'numerical')
def t1b_mass(r, D):
    c, a, bases = r.choice(EXCESS)
    base, kind = r.choice(bases)
    V = r.choice([20.0, 25.0, 40.0, 50.0, 60.0, 75.0, 100.0])
    conc = r.choice([0.5, 1.0, 1.5, 2.0, 0.8, 0.4])
    nacid = V / 1000 * conc
    ratio = 2 if ACID[a][2] == 1 else 1
    nsalt = nacid / ratio
    hyd = HYD_OF.get((c, a)) if D >= 4 else None
    prodf = hyd[0] if hyd else salt_f(c, a)
    prodn = hyd[1] if hyd else salt_n(c, a)
    M = Mr(prodf)
    mass = nsalt * M
    stem = f'{person(r)} adds excess {base_name(c, kind)} to {sf(V)} cm³ of {sf(conc)} mol/dm³ {ACID[a][0]}. {E(excess_eq(c, a, base, kind))}. Calculate the maximum mass of {prodn}, {F(prodf)}, that could be obtained.'
    steps = f'n(acid) = {sf(V)}/1000 × {sf(conc)} = {g3(nacid)} mol [1]; n(salt) = {g3(nacid)}{" ÷ 2" if ratio == 2 else ""} = {g3(nsalt)} mol [1]; Mr = {mr(M)}; mass = {g3(nsalt)} × {mr(M)} = {g3(mass)} g [1]'
    if D >= 5:
        act = r3(mass * r.choice([0.62, 0.7, 0.75, 0.8, 0.84, 0.9]))
        stem = stem.replace('Calculate the maximum mass', 'Calculate (i) the maximum mass') + f' (ii) The student actually obtains {g3(act)} g. Calculate the percentage yield.'
        return {'stem': stem, 'answer': f'(i) {g3(mass)} g (ii) {g3(act / r3(mass) * 100)}%', 'key': steps + f'; % yield = {g3(act)}/{g3(mass)} × 100 = {g3(act / r3(mass) * 100)}% [1]', 'marks': 4}
    return {'stem': stem, 'answer': f'{g3(mass)} g', 'key': steps}


@t1b.add('C3', (3, 4), 'numerical')
def t1b_minbase(r, D):
    c, a, bases = r.choice(EXCESS)
    base, kind = r.choice(bases)
    V = r.choice([25.0, 30.0, 40.0, 50.0, 80.0])
    conc = r.choice([0.5, 1.0, 2.0, 1.2])
    ratio = 2 if ACID[a][2] == 1 else 1
    nb = V / 1000 * conc / ratio
    m = nb * Mr(base)
    return {'stem': f'Calculate the minimum mass of {base_name(c, kind)}, {F(base)}, needed to react completely with {sf(V)} cm³ of {sf(conc)} mol/dm³ {ACID[a][0]}. Suggest why a larger mass is used in practice. ({E(excess_eq(c, a, base, kind))})',
            'answer': f'{g3(m)} g; excess is used so that all the acid reacts and the salt is not contaminated with acid.',
            'key': f'n(acid) = {g3(V / 1000 * conc)} mol [1]; n(solid) = {g3(nb)} mol [1]; mass = {g3(nb)} × {mr(Mr(base))} = {g3(m)} g [1]; reason [1]', 'marks': 4}


def _excess_c4(r, D):
    c, a, bases = r.choice(EXCESS)
    base, kind = r.choice(bases)
    V = r.choice([25.0, 40.0, 50.0, 60.0, 100.0])
    conc = r.choice([0.5, 1.0, 1.5, 2.0])
    ratio = 2 if ACID[a][2] == 1 else 1
    ns = V / 1000 * conc / ratio
    hyd = HYD_OF.get((c, a))
    prodf = hyd[0] if hyd else salt_f(c, a)
    M = Mr(prodf)
    mass = ns * M
    y = r.choice([55, 60, 68, 72, 78, 85])
    p = person(r)
    sname = salt_n(c, a)
    intro = r.choice([f'{p} prepares crystals of {sname} using {sf(V)} cm³ of {sf(conc)} mol/dm³ {ACID[a][0]} and an excess of {base_name(c, kind)}.',
                      f'In {lab(r)}, {sname} is made by adding {base_name(c, kind)} a little at a time to {sf(V)} cm³ of warm {sf(conc)} mol/dm³ {ACID[a][0]} until it is in excess.',
                      f'A teacher in {city(r)} demonstrates the preparation of {sname} from {base_name(c, kind)} and {sf(V)} cm³ of {ACID[a][0]} of concentration {sf(conc)} mol/dm³.'])
    parts = [
        lambda r: ('Write the balanced symbol equation for the reaction.', E(excess_eq(c, a, base, kind)), '1 mark formulae; 1 mark balanced [2]'),
        lambda r: ('Describe how you would know that the solid is in excess.', 'Solid remains undissolved' + (' and effervescence stops' if kind in ('carbonate', 'metal') else '') + '.', '[1]'),
        lambda r: ('Describe how the excess solid is removed and how crystals are then obtained from the solution.', 'Filter; heat the filtrate to evaporate some water until the point of crystallisation (crystals form on a cold glass rod); leave to cool; filter off crystals; dry between filter papers.', '1 mark each for: filter; heat to crystallisation point; cool; dry crystals [4]'),
        lambda r: (f'Calculate the number of moles of {ACID[a][0]} used.', f'{g3(V / 1000 * conc)} mol', f'n = {sf(V)}/1000 × {sf(conc)} [1]'),
        lambda r: (f'Calculate the maximum mass of {F(prodf)} (Mr = {mr(M)}) that can form.', f'{g3(mass)} g', f'n(salt) = {g3(ns)} mol; mass = {g3(ns)} × {mr(M)} = {g3(mass)} g [2]'),
        lambda r: (f'The percentage yield was {y}%. Calculate the mass of crystals obtained and suggest one reason why the yield is less than 100%.', f'{g3(r3(mass) * y / 100)} g; e.g. some salt remains dissolved in the solution after crystallisation / losses on transfer.', f'mass = {y}/100 × {g3(mass)} [1]; reason [1]; total [2]'),
        lambda r: (f'Explain why {base_name(c, kind)} is suitable for this method but sodium {kind if kind != "metal" else "oxide"} would not be.', f'{cap(base_name(c, kind))} is insoluble, so the excess can be filtered off; sodium compounds are soluble and would contaminate the solution.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1b.add('C4', (2, 3, 4, 5), 'multi_step')(_excess_c4)
t1b.add('C3', (3, 4, 5), 'multi_step')(_excess_c4)


# ---------------------------------------------------------- 1.3 titration
t1c = topic('Soluble salt by titration', 'preparing a soluble salt by titration of an acid with an alkali', 'titration of an acid with an alkali')
t1c.fixed('C1', (1, 2), [
    ('Which salt is best prepared by titration of an acid with an alkali?', 'potassium nitrate', 'Potassium compounds are soluble, so the salt is made by exact neutralisation of KOH with HNO₃.', ['copper(II) sulfate', 'barium sulfate', 'magnesium chloride']),
    ('Why is an indicator needed when a soluble salt is made from an acid and an alkali?', 'Both reactants and the product are soluble, so the end-point cannot be seen without one', 'Nothing visible shows when neutralisation is complete; an indicator changes colour at the end-point.',
     ['To speed up the reaction', 'To make the salt crystallise', 'To react with excess acid']),
    ('Which piece of apparatus is used to add the acid a little at a time during a titration?', 'burette', 'A burette delivers variable, accurately measured volumes.', ['pipette', 'measuring cylinder', 'gas syringe']),
    ('Which apparatus measures exactly 25.0 cm³ of alkali into the conical flask?', 'volumetric pipette', 'A pipette delivers a fixed volume accurately.', ['beaker', 'measuring cylinder', 'burette']),
    ('Which indicator is suitable for a titration of sodium hydroxide with hydrochloric acid?', 'methyl orange', 'Methyl orange (or thymolphthalein) changes sharply at the end-point; universal indicator gives a gradual change.', ['universal indicator', 'litmus solution', 'limewater']),
    ('Name the type of reaction that takes place when an acid reacts with an alkali.', 'Neutralisation', '[1]'),
])
t1c.fixed('C2', (2, 3, 4), [
    ('Explain why the titration is repeated with the same volumes but no indicator when making a salt for use.', 'The indicator would contaminate the salt; repeating with the known volumes gives a neutral salt solution with no indicator.', '1 mark each [2]'),
    ('Explain why the excess-solid method cannot be used to prepare ammonium sulfate.', 'Ammonia/ammonium compounds are soluble (aqueous ammonia is an alkali), so there is no insoluble excess to filter off; an exact volume must be found by titration.', '[2]'),
    ('Explain why the conical flask is swirled during a titration.', 'To mix the acid and alkali so that the colour change shows the true end-point.', '[1]'),
    ('Explain why the acid is added drop by drop near the end-point.', 'One drop can change the indicator colour; adding drop by drop prevents overshooting the end-point.', '[2]'),
    ('Ionic equation: H⁺(aq) + OH⁻(aq) → H₂O(l). Explain why this equation applies to every acid–alkali neutralisation.', 'All acids provide H⁺ ions and all alkalis provide OH⁻ ions; the other ions (spectator ions) do not change, so the net reaction is always H⁺ + OH⁻ → H₂O.', '[2]'),
])


@t1c.add('C1', (1, 2, 3))
def t1c_reag(r, D):
    alk, aname, c, _ = r.choice(ALK)
    a = r.choice(list(ACID))
    tgt = salt_n(c, a)
    corr = f'{aname} and {ACID[a][0]}'
    pool = [f'{aname} and {ACID[x][0]}' for x in ACID if x != a] + [f'{ALK[(i + 1) % 3][1]} and {ACID[a][0]}' for i in range(3) if ALK[i][0] == alk] + [f'{CAT[c][0]} carbonate and water']
    return mcq_q(r, f'Which reagents are titrated together to prepare {tgt}?', corr, pool, f'{E(neut_eq(alk, a)[0])}.')


@t1c.add('C3', (2, 3, 4, 5), 'numerical')
def t1c_vol(r, D):
    alk, aname, c, _ = r.choice(ALK[:2])
    a = r.choice(list(ACID))
    eq, ratio = neut_eq(alk, a)
    Va = r.choice([20.0, 25.0, 10.0])
    ca = r.choice([0.100, 0.200, 0.150, 0.250, 0.500, 0.120])
    cacid = r.choice([0.100, 0.200, 0.0500, 0.125, 0.250, 0.400])
    nalk = Va / 1000 * ca
    nacid = nalk / ratio
    Vacid = nacid / cacid * 1000
    if D >= 4:
        # find concentration of acid from titre
        stem = f'In a titration to make {salt_n(c, a)}, {sf(Va)} cm³ of {sf(ca)} mol/dm³ {aname} was exactly neutralised by {sf(Vacid)} cm³ of {ACID[a][0]}. {E(eq)}. Calculate the concentration of the {ACID[a][0]} in mol/dm³.'
        return {'stem': stem, 'answer': f'{g3(cacid)} mol/dm³', 'key': f'n(alkali) = {sf(Va)}/1000 × {sf(ca)} = {g3(nalk)} mol [1]; n(acid) = {g3(nalk)}{" ÷ 2" if ratio == 2 else ""} = {g3(nacid)} mol [1]; c = {g3(nacid)} ÷ ({sf(Vacid)}/1000) = {g3(cacid)} mol/dm³ [1]'}
    stem = f'{sf(Va)} cm³ of {sf(ca)} mol/dm³ {aname} is titrated with {sf(cacid)} mol/dm³ {ACID[a][0]}. {E(eq)}. Calculate the volume of acid needed to neutralise the alkali.'
    return {'stem': stem, 'answer': f'{g3(Vacid)} cm³', 'key': f'n(alkali) = {g3(nalk)} mol [1]; n(acid) = {g3(nacid)} mol [1]; V = n/c = {g3(nacid / cacid)} dm³ = {g3(Vacid)} cm³ [1]'}


@t1c.add('C3', (1, 2, 3), 'numerical')
def t1c_eq(r, D):
    alk, aname, c, _ = r.choice(ALK)
    a = r.choice(list(ACID))
    eq, ratio = neut_eq(alk, a)
    if D == 1:
        correct = F(salt_f(c, a))
        pool = [F(salt_f(c, x)) for x in ACID if x != a] + [F(salt_f(c, 'OH')) if c != 'NH4' else F('NH4OH'), F(f'({CAT[c][1]})2{AN[a][1]}' if c == 'NH4' else f'{CAT[c][1]}2{AN[a][1]}') if AN[a][2] == 1 else F(f'{CAT[c][1]}{AN[a][1]}'), F(f'H{CAT[c][1]}')]
        return mcq_q(r, f'{cap(aname)} is neutralised by {ACID[a][0]}. What is the formula of the salt formed?', correct, pool, E(eq))
    return {'stem': f'Write the balanced symbol equation for the neutralisation of {aname} by {ACID[a][0]}' + (', and the ionic equation.' if D >= 3 and alk != 'NH3' else '.'),
            'answer': E(eq) + ('; H⁺(aq) + OH⁻(aq) → H₂O(l)' if D >= 3 and alk != 'NH3' else ''), 'key': f'{E(eq)} [2]' + ('; ionic equation [1]' if D >= 3 and alk != 'NH3' else '')}


def _titre_table(r):
    base = r.choice([18.40, 21.65, 23.10, 24.35, 19.80, 22.50, 25.15, 20.70, 16.95, 26.30])
    rough = base + r.choice([0.6, 0.8, 1.0, 0.45, 0.7])
    t = [round(base + d, 2) for d in r.sample([0.0, 0.05, 0.10, 0.0, 0.05], 3)]
    # make one non-concordant sometimes
    if r.random() < 0.4:
        t[r.randrange(3)] = round(base + r.choice([0.45, -0.4, 0.6]), 2)
    conc = [x for x in t if sum(abs(x - y) <= 0.1001 for y in t) >= 2]
    avg = sum(conc) / len(conc)
    starts = [r.choice([0.00, 0.50, 1.20, 2.35, 0.80, 1.05, 3.10]) for _ in range(4)]
    vals = [round(rough, 2)] + t
    rows = [(s, round(s + v, 2), v) for s, v in zip(starts, vals)]
    return rows, conc, avg


def _titr_c4(r, D):
    alk, aname, c, _ = r.choice(ALK[:2])
    a = r.choice(list(ACID))
    eq, ratio = neut_eq(alk, a)
    rows, conc, avg = _titre_table(r)
    Va = r.choice([25.0, 20.0])
    cacid = r.choice([0.100, 0.0800, 0.120, 0.150, 0.200])
    nacid = avg / 1000 * cacid
    nalk = nacid * ratio
    calk = nalk / (Va / 1000)
    ind = r.choice([('methyl orange', 'yellow', 'orange/red'), ('thymolphthalein', 'blue', 'colourless')])
    table = '; '.join(f'{"rough" if i == 0 else "titration " + str(i)}: initial {x[0]:.2f}, final {x[1]:.2f}' for i, x in enumerate(rows))
    intro = f'{person(r)} titrates {sf(Va)} cm³ of {aname} with {sf(cacid)} mol/dm³ {ACID[a][0]} using {ind[0]} indicator. Burette readings / cm³ — {table}.'
    parts = [
        lambda r: ('Calculate each titre and identify the concordant results.', '; '.join(f'{x[2]:.2f}' for x in rows) + ' cm³; concordant: ' + ', '.join(f'{x:.2f}' for x in conc),
                   'titre = final − initial for each [1]; concordant = within 0.10 cm³, rough excluded [1]; total [2]'),
        lambda r: ('Calculate the mean titre using the concordant results.', f'{avg:.2f} cm³', f'mean of {", ".join(f"{x:.2f}" for x in conc)} [1]'),
        lambda r: (f'State the colour change at the end-point.', f'{ind[1]} to {ind[2]}', '[1]'),
        lambda r: (f'Calculate the concentration of the {aname}. {E(eq)}', f'{g3(calk)} mol/dm³', f'n(acid) = {avg:.2f}/1000 × {sf(cacid)} = {g3(nacid)} mol [1]; n(alkali) = {g3(nalk)} mol [1]; c = {g3(nalk)} ÷ {sf(Va / 1000)} = {g3(calk)} mol/dm³ [1]; total [3]'),
        lambda r: ('Explain why the rough titration is not used in calculating the mean.', 'It is only to find the approximate end-point; the acid is added quickly so it usually overshoots.', '[1]'),
        lambda r: (f'Describe how you would then obtain pure dry crystals of {salt_n(c, a)}.', 'Repeat the titration with the same volumes but no indicator; heat the solution to the point of crystallisation; cool; filter and dry crystals.', '1 mark each point [3]'),
        lambda r: ('Suggest one source of error that would make the titre too large.', 'e.g. air bubble in the burette jet / overshooting the end-point / reading the meniscus from above.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t1c.add('C4', (2, 3, 4, 5), 'case')(_titr_c4)
t1c.add('C3', (3, 4, 5), 'case')(_titr_c4)


@t1c.add('C2', (2, 3, 4), 'explain')
def t1c_spot(r, D):
    alk, aname, c, _ = r.choice(ALK)
    a = r.choice(list(ACID))
    errs = [('rinsed the burette with distilled water just before filling it with acid', 'The water dilutes the acid, so a larger titre is needed; the burette should be rinsed with the acid itself.'),
            ('used universal indicator', 'Universal indicator changes colour gradually through many colours, so the end-point is not sharp; use methyl orange or thymolphthalein.'),
            ('read the burette at the top of the meniscus', 'Readings should be taken at the bottom of the meniscus at eye level, otherwise every reading is wrong/parallax error.'),
            (f'evaporated the {salt_n(c, a)} solution from the titration with the indicator still in it', 'The salt is contaminated with indicator; repeat with the same volumes without indicator.'),
            ('left the funnel in the top of the burette during the titration', 'Drops of acid can fall from the funnel, changing the reading; remove it before titrating.')]
    e, fix = r.choice(errs)
    return {'stem': f'While preparing {salt_n(c, a)} from {aname} and {ACID[a][0]}, {person(r)} {e}. Explain why this is a problem and state how to correct it.',
            'answer': fix, 'key': '1 mark: effect on result/product; 1 mark: correct technique [2]'}


# ---------------------------------------------------------- 1.4 precipitation
t1d = topic('Insoluble salt by precipitation', 'preparing an insoluble salt by precipitation', 'precipitation')
t1d.fixed('C1', (1, 2), [
    ('Which pair of solutions could be mixed to prepare insoluble barium sulfate?', 'barium nitrate and sodium sulfate', 'Ba²⁺(aq) + SO₄²⁻(aq) → BaSO₄(s); both reactants must be soluble.', ['barium carbonate and sodium sulfate', 'barium nitrate and sodium chloride', 'barium sulfate and water']),
    ('After precipitation, how is the insoluble salt separated from the mixture?', 'filtration', 'The precipitate stays as residue on the filter paper.', ['crystallisation', 'simple distillation', 'chromatography']),
    ('Why is the precipitate washed with distilled water?', 'To remove soluble impurities', 'Washing removes the soluble by-product and unreacted ions from the solid.', ['To dissolve the precipitate', 'To make crystals grow larger', 'To neutralise the precipitate']),
    ('Which ions are spectator ions when aqueous silver nitrate is mixed with aqueous sodium chloride?', 'Na⁺ and NO₃⁻', 'Ag⁺ + Cl⁻ → AgCl(s); sodium and nitrate ions remain in solution unchanged.', ['Ag⁺ and Cl⁻', 'Na⁺ and Cl⁻', 'Ag⁺ and NO₃⁻']),
    ('State what is meant by a precipitate.', 'An insoluble solid formed when two solutions are mixed.', '[1]'),
])
t1d.fixed('C2', (2, 3, 4), [
    ('Explain why the precipitate is dried in a warm oven rather than heated strongly.', 'Strong heating might decompose the salt (e.g. carbonates give oxides); a warm oven removes the water without changing the salt.', '[2]'),
    ('Explain why lead(II) chloride can be made by mixing aqueous lead(II) nitrate with aqueous sodium chloride.', 'Both reactants are soluble (nitrates and sodium salts) so they provide the ions; lead(II) chloride is insoluble so it precipitates.', '1 mark: reactants soluble; 1 mark: product insoluble [2]'),
    ('Explain why barium sulfate cannot be made by adding barium carbonate to dilute sulfuric acid.', 'Insoluble barium sulfate forms a layer on the carbonate, stopping the reaction; also the product would be mixed with unreacted carbonate.', '[2]'),
    ('Explain the meaning of the term "spectator ion", using the formation of silver chloride as an example.', 'Ions present in the solution that do not take part in the reaction, e.g. Na⁺ and NO₃⁻ when AgNO₃(aq) and NaCl(aq) are mixed.', '[2]'),
    ('Explain why the filter paper and precipitate are rinsed with a little distilled water rather than tap water.', 'Tap water contains dissolved ions (e.g. Ca²⁺, Cl⁻) that would contaminate the salt or form further precipitate.', '[2]'),
])


@t1d.add('C1', (1, 2, 3))
def t1d_pair(r, D):
    c, a = r.choice(PPT)
    (cs, cn), (as_, an_), eq, ion, side = ppt_reagents(c, a, r.randrange(2))
    corr = f'{cn} and {an_}'
    wrong = [f'{salt_n(c, a)} and water', f'{cn} and {salt_n("Na", "NO3")}', f'{salt_n(c, "CO3") if a != "CO3" else salt_n(c, "SO4")} and {an_}', f'{salt_n("Na", "NO3")} and {an_}']
    return mcq_q(r, f'Which pair of aqueous solutions would produce a precipitate of {salt_n(c, a)}?', corr, wrong, f'{E(eq)}; ionic: {E(ion)}.')


@t1d.add('C3', (1, 2, 3, 4))
def t1d_eq(r, D):
    c, a = r.choice(PPT)
    (cs, cn), (as_, an_), eq, ion, side = ppt_reagents(c, a, r.randrange(2))
    if D == 1:
        pool = [E(ion), E(f'{CAT[c][1]} + {AN[a][1]} -> {salt_f(c, a)}'), E(f'Na^+ + NO3^- -> NaNO3'), E(f'{salt_f(c, a)} -> {CAT[c][1]}^{CAT[c][2] if CAT[c][2] > 1 else ""}+ + {AN[a][1]}^{AN[a][2] if AN[a][2] > 1 else ""}-')]
        return mcq_q(r, f'Aqueous {cn} is mixed with aqueous {an_}. Which is the ionic equation for the precipitation?', E(ion), pool, f'{E(ion)}; the other ions are spectators.')
    st = ' Include state symbols.' if D >= 3 else ''
    return {'stem': f'Aqueous {cn} is mixed with aqueous {an_}. Write (a) the balanced symbol equation and (b) the ionic equation for the reaction.{st}',
            'answer': f'(a) {E(eq)} (b) {E(ion)}' + (' — precipitate (s), others (aq)' if st else ''), 'key': f'(a) formulae [1], balancing [1]; (b) ionic equation [1]' + ('; state symbols [1]' if st else ''),
            'marks': 4 if st else 3}


@t1d.add('C3', (3, 4, 5), 'numerical')
def t1d_mass(r, D):
    c, a = r.choice([x for x in PPT if x[1] in ('SO4', 'Cl', 'CO3')])
    (cs, cn), (as_, an_), eq, ion, side = ppt_reagents(c, a)
    p, q = CAT[c][2], AN[a][2]
    l = p * q // math.gcd(p, q); na, nb = l // p, l // q
    V1 = r.choice([20.0, 25.0, 50.0, 40.0]); c1 = r.choice([0.100, 0.200, 0.500, 0.250])
    n1 = V1 / 1000 * c1
    npp = n1 / na
    M = Mr(salt_f(c, a))
    if D >= 5:
        V2 = r.choice([10.0, 15.0, 30.0, 60.0]); c2 = r.choice([0.100, 0.200, 0.400])
        n2 = V2 / 1000 * c2
        npp = min(n1 / na, n2 / nb)
        lim = cn if n1 / na <= n2 / nb else an_
        return {'stem': f'{sf(V1)} cm³ of {sf(c1)} mol/dm³ {cn} is mixed with {sf(V2)} cm³ of {sf(c2)} mol/dm³ {an_}. {E(eq)}. Deduce which reagent is limiting and calculate the mass of {salt_n(c, a)} formed.',
                'answer': f'{lim} is limiting; {g3(npp * M)} g', 'key': f'n({F(cs)}) = {g3(n1)} mol, n({F(as_)}) = {g3(n2)} mol [1]; using the mole ratio {na}:{nb}, {lim} is limiting [1]; n(ppt) = {g3(npp)} mol [1]; mass = {g3(npp)} × {mr(M)} = {g3(npp * M)} g [1]', 'marks': 4}
    return {'stem': f'Excess aqueous {an_} is added to {sf(V1)} cm³ of {sf(c1)} mol/dm³ {cn}. {E(eq)}. Calculate the mass of dry {salt_n(c, a)} precipitate that forms.',
            'answer': f'{g3(npp * M)} g', 'key': f'n({F(cs)}) = {sf(V1)}/1000 × {sf(c1)} = {g3(n1)} mol [1]; n(ppt) = {g3(npp)} mol [1]; Mr {F(salt_f(c, a))} = {mr(M)}, mass = {g3(npp * M)} g [1]'}


@t1d.add('C2', (2, 3, 4), 'explain')
def t1d_err(r, D):
    c, a = r.choice(PPT)
    (cs, cn), (as_, an_), eq, ion, side = ppt_reagents(c, a)
    errs = [(f'used solid {salt_n(c, "CO3") if a != "CO3" else salt_n(c, "OH")} instead of aqueous {cn}', 'The cation must be in solution; an insoluble solid provides no free ions (and would contaminate the product). Use a soluble salt such as the nitrate.'),
            ('evaporated the mixture to dryness instead of filtering', f'The solid would be contaminated with the soluble {side[1]}; filter, wash and dry instead.'),
            ('did not wash the precipitate', f'Soluble {side[1]} remains on the solid, so it is impure; wash with distilled water.'),
            ('kept the filtrate and threw away the residue', f'The {salt_n(c, a)} is the insoluble residue on the filter paper; the filtrate contains only {side[1]}.')]
    e, fix = r.choice(errs)
    return {'stem': f'To prepare {salt_n(c, a)}, {person(r)} {e}. Explain the mistake and how to correct it.', 'answer': fix, 'key': '1 mark: why it is wrong; 1 mark: correction [2]'}


def _ppt_c4(r, D):
    c, a = r.choice(PPT)
    (cs, cn), (as_, an_), eq, ion, side = ppt_reagents(c, a, r.randrange(2))
    V1 = r.choice([25.0, 50.0, 40.0]); c1 = r.choice([0.100, 0.200, 0.500])
    p, q = CAT[c][2], AN[a][2]
    l = p * q // math.gcd(p, q); na = l // p
    npp = V1 / 1000 * c1 / na
    M = Mr(salt_f(c, a))
    act = r3(npp * M * r.choice([0.72, 0.8, 0.86, 0.9, 0.93]))
    p_ = person(r)
    intro = r.choice([f'{p_} prepares {salt_n(c, a)} by mixing {sf(V1)} cm³ of {sf(c1)} mol/dm³ {cn} with an excess of aqueous {an_}.',
                      f'In {lab(r)}, an insoluble salt, {salt_n(c, a)}, is made from {sf(V1)} cm³ of {sf(c1)} mol/dm³ {cn} and excess {an_} solution.',
                      f'A paint pigment manufacturer in {city(r)} makes {salt_n(c, a)} by precipitation, starting from {sf(V1)} cm³ of {sf(c1)} mol/dm³ {cn} in a trial batch.'])
    parts = [
        lambda r: ('State the colour of the precipitate.', ppt_col(c, a), '[1]'),
        lambda r: ('Write the ionic equation, with state symbols.', E(ion).replace(F(salt_f(c, a)), F(salt_f(c, a)) + '(s)'), 'ions (aq) [1]; product (s) and balanced [1]; total [2]'),
        lambda r: ('Name the soluble by-product that remains in solution.', side[1], '[1]'),
        lambda r: ('Describe how a pure dry sample of the salt is obtained from the mixture.', 'Filter; wash the residue with distilled water; dry in a warm oven or between filter papers.', '1 mark each [3]'),
        lambda r: (f'Calculate the maximum mass of precipitate (Mr = {mr(M)}).', f'{g3(npp * M)} g', f'n = {sf(V1)}/1000 × {sf(c1)}{f" ÷ {na}" if na > 1 else ""} = {g3(npp)} mol [1]; mass = {g3(npp * M)} g [1]; total [2]'),
        lambda r: (f'The dry mass obtained was {g3(act)} g. Calculate the percentage yield and suggest one reason why it is below 100%.', f'{g3(act / r3(npp * M) * 100)}%; some solid lost on the filter paper or in transfer.', '[2]'),
        lambda r: (f'Explain why {cn} is used rather than {salt_n(c, "CO3") if a != "CO3" else salt_n(c, "OH")} as the source of {CAT[c][0]} ions.', f'{cap(cn)} is soluble so it provides free {CAT[c][0]} ions; the alternative is insoluble.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1d.add('C4', (2, 3, 4, 5), 'multi_step')(_ppt_c4)
t1d.add('C3', (3, 4), 'multi_step')(_ppt_c4)


# ---------------------------------------------------------- 1.5 hydrated salts
t1e = topic('Hydrated and anhydrous salts', 'hydrated and anhydrous salts and water of crystallisation', 'water of crystallisation', 'hydrated anhydrous')
t1e.fixed('C1', (1, 2), [
    ('What is meant by water of crystallisation?', 'Water molecules chemically combined in a fixed ratio within a crystalline salt', 'Water of crystallisation: water molecules present in hydrated crystals in a definite proportion.',
     ['Water used to dissolve a salt', 'Water that evaporates from a salt solution', 'Water produced when an acid reacts with a base']),
    ('What colour change is seen when blue hydrated copper(II) sulfate is heated strongly?', 'blue to white', 'CuSO₄·5H₂O(s) → CuSO₄(s) + 5H₂O(g): water of crystallisation is driven off.', ['white to blue', 'blue to black', 'green to blue']),
    ('Which formula represents a hydrated salt?', 'MgSO₄·7H₂O', 'The ·7H₂O shows seven molecules of water of crystallisation per formula unit.', ['MgSO₄', 'Mg(OH)₂', 'MgO']),
    ('A salt that contains no water of crystallisation is described as', 'anhydrous', 'Anhydrous = without water of crystallisation.', ['hydrated', 'aqueous', 'deliquescent']),
    ('Define the term hydrated substance.', 'A substance that is chemically combined with water.', '[1]'),
    ('Define the term anhydrous substance.', 'A substance containing no water.', '[1]'),
])
t1e.fixed('C2', (2, 3), [
    ('Explain why adding water to white anhydrous copper(II) sulfate can be used as a test for water.', 'Water recombines to form blue hydrated copper(II) sulfate; the colour change from white to blue shows water is present.', '[2]'),
    ('Explain why the dehydration of hydrated copper(II) sulfate is described as a reversible reaction.', 'Heating removes water to give white anhydrous salt; adding water back reforms the blue hydrated salt.', '1 mark each direction [2]'),
    ('Explain why a hydrated salt is heated "to constant mass" when finding the formula of the hydrate.', 'Repeated heating until the mass stops changing ensures all the water of crystallisation has been removed.', '[2]'),
    ('Explain why heating hydrated copper(II) sulfate is endothermic while adding water to the anhydrous salt is exothermic.', 'Energy is needed to remove the water from the crystal structure; the same energy is released when water recombines.', '[2]'),
])


@t1e.add('C1', (1, 2, 3))
def t1e_formula(r, D):
    f, n, x, col = r.choice(HYDRATES)
    hf = F(f'{f}.{x}H2O')
    pool = [F(f'{f}.{y}H2O') for y in (2, 4, 5, 6, 7, 10) if y != x]
    return mcq_q(r, f'Hydrated {n} contains {x} molecules of water of crystallisation per formula unit. What is its formula?', hf, pool, f'{hf}: anhydrous formula · {x}H₂O.')


@t1e.add('C3', (2, 3, 4, 5), 'numerical')
def t1e_x(r, D):
    f, n, x, col = r.choice(HYDRATES)
    Ma = Mr(f)
    na = r.choice([0.0100, 0.0120, 0.0150, 0.0200, 0.0250, 0.0080])
    m_an = round(na * Ma, 2)
    m_hyd = round(m_an + na * x * 18, 2)
    crucible = round(r.uniform(18, 32), 2)
    nw = (m_hyd - m_an) / 18
    nn = m_an / Ma
    xr = nw / nn
    if D >= 4:
        stem = (f'{person(r)} heats a sample of hydrated {n}, {F(f)}·xH₂O, in a crucible to constant mass. Mass of crucible = {crucible:.2f} g; crucible + hydrated salt = {crucible + m_hyd:.2f} g; '
                f'crucible + anhydrous salt = {crucible + m_an:.2f} g. Calculate the value of x.')
        return {'stem': stem, 'answer': f'x = {x}', 'key': f'mass anhydrous = {m_an:.2f} g, mass water = {m_hyd - m_an:.2f} g [1]; n({F(f)}) = {m_an:.2f}/{mr(Ma)} = {nn:.4f} mol [1]; n(H₂O) = {m_hyd - m_an:.2f}/18 = {nw:.4f} mol [1]; ratio {xr:.2f} so x = {x} [1]', 'marks': 4}
    stem = f'When {m_hyd:.2f} g of hydrated {n}, {F(f)}·xH₂O, is heated until all the water is removed, {m_an:.2f} g of anhydrous {F(f)} remains. Calculate x.'
    return {'stem': stem, 'answer': f'x = {x}', 'key': f'n(anhydrous) = {m_an:.2f}/{mr(Ma)} = {nn:.4f} mol; n(water) = {m_hyd - m_an:.2f}/18 = {nw:.4f} mol [1]; x = {xr:.2f} ≈ {x} [1]' + (' [3]' if D == 3 else ''), 'marks': 3 if D >= 3 else 2}


@t1e.add('C3', (1, 2, 3), 'numerical')
def t1e_pct(r, D):
    f, n, x, col = r.choice(HYDRATES)
    M = Mr(f'{f}.{x}H2O')
    pct = 18 * x / M * 100
    if D == 1:
        return nmcq(r, f'What is the relative formula mass of {F(f + "." + str(x) + "H2O")}?', M, [Mr(f), Mr(f) + 18, Mr(f) + 18 * (x - 1), M + 18], '',
                    f'Mr = {mr(Mr(f))} + {x} × 18 = {mr(M)}.', f=mr)
    return {'stem': f'Calculate the percentage by mass of water in hydrated {n}, {F(f + "." + str(x) + "H2O")}.', 'answer': f'{g3(pct)}%',
            'key': f'Mr = {mr(M)} [1]; % water = {18 * x}/{mr(M)} × 100 = {g3(pct)}% [1]'}


@t1e.add('C2', (2, 3, 4), 'explain')
def t1e_obs(r, D):
    f, n, x, col = r.choice(HYDRATES)
    return {'stem': f'Hydrated {n}, {F(f + "." + str(x) + "H2O")}, is heated in a test-tube. Describe what you would observe and write the equation for the change.',
            'answer': f'{cap(col)}; droplets of colourless liquid (water) condense near the top of the tube. {F(f + "." + str(x) + "H2O")}(s) → {F(f)}(s) + {x}H₂O(g)',
            'key': '1 mark: colour/appearance change; 1 mark: condensation of water; 1 mark: equation [3]', 'marks': 3}


def _hyd_c4(r, D):
    f, n, x, col = r.choice(HYDRATES[:5] + HYDRATES[6:])
    Ma = Mr(f)
    na = r.choice([0.0100, 0.0150, 0.0200, 0.0120])
    m_an = round(na * Ma, 2); m_hyd = round(m_an + na * x * 18, 2)
    heats = [round(m_hyd - (m_hyd - m_an) * k, 2) for k in (0.55, 0.85, 1.0, 1.0)]
    intro = (f'{person(r)} investigates hydrated {n}, {F(f)}·xH₂O. A {m_hyd:.2f} g sample is heated in a crucible; its mass is recorded after each heating: '
             + ', '.join(f'{h:.2f} g' for h in heats) + '.')
    parts = [
        lambda r: ('Explain why the sample was heated several times.', 'To make sure all the water of crystallisation was removed — heating to constant mass.', '[2]'),
        lambda r: ('Calculate the mass of water lost.', f'{m_hyd - m_an:.2f} g', '[1]'),
        lambda r: ('Calculate the value of x.', f'{x}', f'n(anhydrous) = {m_an:.2f}/{mr(Ma)} [1]; n(water) = {m_hyd - m_an:.2f}/18 [1]; ratio → x = {x} [1]; total [3]'),
        lambda r: ('Suggest why a lid is placed loosely on the crucible.', 'To prevent loss of solid by spitting while allowing water vapour to escape.', '[1]'),
        lambda r: ('Describe a test to show that the vapour given off is water.', 'Condense it and add to anhydrous copper(II) sulfate: white → blue (or cobalt(II) chloride paper blue → pink); pure water boils at 100 °C.', '[2]'),
        lambda r: ('Suggest how the calculated value of x would be affected if the sample was not heated to constant mass.', 'x would be too small, because less water would appear to have been lost.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t1e.add('C4', (2, 3, 4, 5), 'case')(_hyd_c4)
t1e.add('C3', (3, 4), 'case')(_hyd_c4)

CHAPTERS[1] = [t1a, t1b, t1c, t1d, t1e]


# ===================================================================== Ch2 (CB13) The Periodic Table
ELEM = [(1, 'H', 'hydrogen'), (2, 'He', 'helium'), (3, 'Li', 'lithium'), (4, 'Be', 'beryllium'), (5, 'B', 'boron'), (6, 'C', 'carbon'), (7, 'N', 'nitrogen'),
        (8, 'O', 'oxygen'), (9, 'F', 'fluorine'), (10, 'Ne', 'neon'), (11, 'Na', 'sodium'), (12, 'Mg', 'magnesium'), (13, 'Al', 'aluminium'), (14, 'Si', 'silicon'),
        (15, 'P', 'phosphorus'), (16, 'S', 'sulfur'), (17, 'Cl', 'chlorine'), (18, 'Ar', 'argon'), (19, 'K', 'potassium'), (20, 'Ca', 'calcium')]
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII'}
METALLIC = {'Li', 'Be', 'Na', 'Mg', 'Al', 'K', 'Ca'}
NONMET = {'H', 'He', 'C', 'N', 'O', 'F', 'Ne', 'P', 'S', 'Cl', 'Ar'}


def config(Z):
    shells = []
    caps_ = [2, 8, 8, 2]
    for c in caps_:
        if Z <= 0:
            break
        shells.append(min(c, Z)); Z -= min(c, Z)
    return shells


def cfg(Z):
    return ','.join(map(str, config(Z)))


def group_of(Z):
    c = config(Z)
    if Z == 2:
        return 8
    return 8 if c[-1] == 8 else c[-1]


def period_of(Z):
    return len(config(Z))


def gp(Z):
    return f'Group {ROMAN[group_of(Z)]}, Period {period_of(Z)}'


MAIN_EL = [e for e in ELEM if e[0] > 2]

t2a = topic('Groups, periods and metallic character', 'arrangement of elements in groups and periods', 'metallic to non-metallic character across a period', 'groups and periods')
t2a.fixed('C1', (1, 2), [
    ('How are the elements arranged in the Periodic Table?', 'In order of increasing proton number', 'Modern table: increasing proton (atomic) number; elements with similar properties fall in the same group.', ['In order of increasing nucleon number', 'In order of discovery', 'In alphabetical order of their symbols']),
    ('What do elements in the same group of the Periodic Table have in common?', 'The same number of outer-shell electrons', 'Group number (I–VII) = number of outer electrons; this gives similar chemical properties.', ['The same number of electron shells', 'The same nucleon number', 'The same number of neutrons']),
    ('The period number of an element tells you', 'the number of occupied electron shells', 'Period = number of shells containing electrons.', ['the number of outer electrons', 'the number of neutrons', 'the charge on its ion']),
    ('How does the character of the elements change from left to right across Period 3?', 'From metallic to non-metallic', 'Na, Mg, Al are metals; Si is a metalloid; P, S, Cl, Ar are non-metals.', ['From non-metallic to metallic', 'It stays metallic', 'It alternates between metal and non-metal']),
    ('Which type of oxide is formed by elements on the left of Period 3, such as sodium and magnesium?', 'basic oxides', 'Metal oxides are basic; non-metal oxides (e.g. SO₂, P₄O₁₀) are acidic; Al₂O₃ is amphoteric.', ['acidic oxides', 'neutral oxides only', 'amphoteric oxides only']),
    ('State the relationship between the group number and the charge on the ion formed by a metal in Groups I to III.', 'The charge on the ion equals the group number (e.g. Group II forms 2+ ions).', '[1]'),
])
t2a.fixed('C2', (2, 3, 4), [
    ('Explain why elements in the same group have similar chemical properties.', 'They have the same number of electrons in their outer shell, and reactions involve the outer electrons.', '1 mark: same number of outer electrons; 1 mark: outer electrons determine reactions [2]'),
    ('Explain, in terms of electrons, why sodium forms Na⁺ ions but chlorine forms Cl⁻ ions.', 'Sodium (2,8,1) loses its one outer electron to gain a full outer shell; chlorine (2,8,7) gains one electron to fill its outer shell.', '1 mark each [2]'),
    ('Describe how the oxides of the elements change across Period 3 from sodium to sulfur.', 'Oxides change from basic (Na₂O, MgO) through amphoteric (Al₂O₃) to acidic (SiO₂, P₄O₁₀, SO₂).', '1 mark basic left; 1 mark acidic right; 1 mark amphoteric aluminium [3]'),
    ('Explain why helium is placed in Group VIII even though it has only two outer electrons.', 'Its outer (first) shell is full, so like the other noble gases it is unreactive.', '[2]'),
    ('Explain why the elements in a period do not have similar properties to each other.', 'Each has a different number of outer electrons, so they react differently (metals on the left, non-metals on the right).', '[2]'),
])


@t2a.add('C1', (1, 2, 3))
def t2a_gp(r, D):
    Z, sym, name = r.choice(MAIN_EL)
    g, p_ = group_of(Z), period_of(Z)
    corr = gp(Z)
    pool = [f'Group {ROMAN[a]}, Period {b}' for a in (max(1, g - 1), g, min(8, g + 1), p_) for b in (p_, p_ + 1, max(1, p_ - 1), g if g <= 4 else 2) if (a, b) != (g, p_) and b >= 1]
    stem = r.choice([f'An element has the electronic configuration {cfg(Z)}. Where is it in the Periodic Table?', f'Where in the Periodic Table is the element with {Z} protons?'])
    return mcq_q(r, stem, corr, pool, f'{name} ({sym}) {cfg(Z)}: {len(config(Z))} shells → Period {p_}; {config(Z)[-1]} outer electron(s) → Group {ROMAN[g]}.')


@t2a.add('C1', (1, 2, 3))
def t2a_find(r, D):
    Z, sym, name = r.choice(MAIN_EL)
    others = [e[2] for e in MAIN_EL if e[0] != Z]
    return mcq_q(r, f'Which element is in {gp(Z).replace(",", " and")}?', name, others, f'{name}: {cfg(Z)}.')


@t2a.add('C2', (2, 3, 4), 'explain')
def t2a_pos(r, D):
    Z, sym, name = r.choice([e for e in MAIN_EL if e[1] not in ('B', 'Si')])
    kind = 'metal' if sym in METALLIC else 'non-metal'
    return {'stem': f'Element {sym} has proton number {Z}. Deduce its electronic configuration, its group and period, and explain whether it is a metal or a non-metal.',
            'answer': f'{cfg(Z)}; {gp(Z)}; {kind} — ' + ('it is on the left of the table and loses outer electrons to form positive ions.' if kind == 'metal' else 'it is on the right of the table and tends to gain/share electrons.'),
            'key': f'1 mark configuration {cfg(Z)}; 1 mark group and period; 1 mark metal/non-metal with reason [3]', 'marks': 3}


def ion_charge(Z):
    g = group_of(Z)
    return g if g <= 3 else (g - 8 if g >= 5 else None)


@t2a.add('C3', (2, 3, 4))
def t2a_formula(r, D):
    m = r.choice([e for e in MAIN_EL if group_of(e[0]) in (1, 2, 3)])
    n = r.choice([e for e in MAIN_EL if group_of(e[0]) in (6, 7) or e[1] == 'N'])
    a, b = ion_charge(m[0]), -ion_charge(n[0])
    l = a * b // math.gcd(a, b)
    f = f'{m[1]}{l // a if l // a > 1 else ""}{n[1]}{l // b if l // b > 1 else ""}'
    if D == 2:
        pool = [F(x) for x in (f'{m[1]}{n[1]}', f'{m[1]}{n[1]}2', f'{m[1]}2{n[1]}', f'{m[1]}2{n[1]}3', f'{m[1]}3{n[1]}2', f'{m[1]}{n[1]}3')]
        return mcq_q(r, f'Element X is in Group {ROMAN[group_of(m[0])]} and element Y is in Group {ROMAN[group_of(n[0])]}. X is {m[2]} and Y is {n[2]}. What is the formula of the compound they form?', F(f), pool,
                     f'{m[2]} forms {m[1]}{"+" if a == 1 else str(a) + "+"}, {n[2]} forms {n[1]}{"−" if b == 1 else str(b) + "−"}; balance charges: {F(f)}.')
    return {'stem': f'Use the positions of {m[2]} ({cfg(m[0])}) and {n[2]} ({cfg(n[0])}) in the Periodic Table to deduce the charges on their ions and the formula of the compound formed between them.',
            'answer': f'{m[1]}{"" if a == 1 else a}+ and {n[1]}{"" if b == 1 else b}−; {F(f)}', 'key': f'1 mark each ion charge; 1 mark formula {F(f)} [3]', 'marks': 3}


P3OX = [('sodium', 'Na2O', 'basic', 'solid'), ('magnesium', 'MgO', 'basic', 'solid'), ('aluminium', 'Al2O3', 'amphoteric', 'solid'), ('silicon', 'SiO2', 'acidic', 'solid'),
        ('phosphorus', 'P4O10', 'acidic', 'solid'), ('sulfur', 'SO2', 'acidic', 'gas')]


@t2a.add('C3', (1, 2, 3))
def t2a_oxide(r, D):
    el, f, kind, st = r.choice(P3OX)
    if D == 1:
        return mcq_q(r, f'What type of oxide is {F(f)}, the oxide of {el}?', kind, ['basic', 'acidic', 'amphoteric', 'neutral'], f'Across Period 3 oxides go basic → amphoteric → acidic; {F(f)} is {kind}.')
    return {'stem': f'Predict whether {F(f)}, the oxide of {el}, reacts with dilute hydrochloric acid, with aqueous sodium hydroxide, or with both. Explain your answer.',
            'answer': {'basic': 'Reacts with acid only: it is a basic (metal) oxide.', 'acidic': 'Reacts with alkali only: it is an acidic (non-metal) oxide.', 'amphoteric': 'Reacts with both: it is amphoteric.'}[kind],
            'key': '1 mark: prediction; 1 mark: type of oxide linked to metallic/non-metallic character [2]'}


def _pt_c4(r, D):
    pick = r.sample([e for e in MAIN_EL], 5)
    letters = 'QRTXZ'
    lst = list(zip(letters, pick))
    intro = 'The table gives the electronic configurations of five elements (letters are not symbols): ' + '; '.join(f'{L} {cfg(e[0])}' for L, e in lst) + '.'
    met = [L for L, e in lst if e[1] in METALLIC]
    same = None
    for i in range(5):
        for j in range(i + 1, 5):
            if group_of(lst[i][1][0]) == group_of(lst[j][1][0]):
                same = (lst[i][0], lst[j][0])
    parts = [
        lambda r: ('Which elements are in the same period as ' + lst[0][0] + '?', ', '.join(L for L, e in lst[1:] if period_of(e[0]) == period_of(lst[0][1][0])) or 'none of them', 'same number of shells [1]'),
        lambda r: ('Which elements are metals? Explain how you decided.', (', '.join(met) or 'none') + ': they have 1, 2 or 3 outer electrons (left of the table) and lose them to form positive ions.', '1 mark letters; 1 mark reason [2]'),
        lambda r: (f'State the group and period of {lst[1][0]}.', gp(lst[1][1][0]), '[2]'),
        lambda r: (f'Predict the charge on the ion formed by {lst[2][0]}, if any.', (f'{ion_charge(lst[2][1][0]):+d}' if ion_charge(lst[2][1][0]) else 'no ion — it does not readily form one') + '', 'from number of outer electrons [1]'),
        lambda r: (('Which two elements would have similar chemical properties? Explain.', f'{same[0]} and {same[1]}: same number of outer electrons (same group).', '[2]') if same else
                   ('Explain why none of these elements would have closely similar chemical properties.', 'They all have different numbers of outer electrons, so they are in different groups.', '[2]')),
        lambda r: (f'Name the element {lst[3][0]}.', lst[3][1][2], '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t2a.add('C4', (2, 3, 4, 5), 'multi_step')(_pt_c4)
t2a.add('C3', (3, 4), 'multi_step')(_pt_c4)

# ---------------------------------------------------------- 2.2 Group I
GI = [('lithium', 'Li', 3, 181, 0.53, 7, 'fizzes steadily and floats; it does not melt', 'red'),
      ('sodium', 'Na', 11, 98, 0.97, 23, 'fizzes rapidly, melts into a silvery ball and moves quickly over the surface', 'yellow'),
      ('potassium', 'K', 19, 63, 0.86, 39, 'reacts violently, melts, moves rapidly and the hydrogen burns with a lilac flame', 'lilac'),
      ('rubidium', 'Rb', 37, 39, 1.53, 85, 'reacts explosively', 'red-violet'),
      ('caesium', 'Cs', 55, 29, 1.93, 133, 'reacts very explosively', 'blue-violet')]
AR.update({'Rb': 85, 'Cs': 133})

t2b = topic('Group I alkali metals', 'group i alkali metals', 'physical properties, reactions with water and predicting trends', 'alkali metals')
t2b.fixed('C1', (1, 2), [
    ('How does the melting point of the Group I metals change down the group?', 'It decreases', 'Li 181 °C, Na 98 °C, K 63 °C: metallic bonding weakens as atoms get larger.', ['It increases', 'It stays the same', 'It increases then decreases']),
    ('Which gas is produced when sodium reacts with water?', 'hydrogen', '2Na + 2H₂O → 2NaOH + H₂.', ['oxygen', 'carbon dioxide', 'chlorine']),
    ('Why are Group I metals stored under oil?', 'To prevent them reacting with oxygen and water vapour in the air', 'They are very reactive; oil keeps air and moisture away.', ['To keep them cool', 'To stop them melting', 'To make them conduct electricity']),
    ('What is the pH of the solution formed when potassium reacts with water?', 'above 7', 'Potassium hydroxide forms: an alkaline solution.', ['exactly 7', 'below 7', 'exactly 0']),
    ('Which statement describes the Group I metals?', 'They are soft and can be cut with a knife', 'Alkali metals are soft, low density metals with low melting points.', ['They are hard with high melting points', 'They are all denser than water', 'They are unreactive']),
    ('State the number of electrons in the outer shell of an atom of a Group I element.', 'One', '[1]'),
])
t2b.fixed('C2', (2, 3, 4), [
    ('Explain why the reactivity of the Group I metals increases down the group.', 'The outer electron is further from the nucleus (more shells, more shielding), so it is less strongly attracted and lost more easily.', '1 mark: more shells / further from nucleus; 1 mark: outer electron lost more easily [2]'),
    ('Explain why sodium floats on water while it reacts.', 'Sodium has a lower density (0.97 g/cm³) than water (1.00 g/cm³).', '[1]'),
    ('Explain why all the Group I metals react in a similar way with water.', 'Each has one outer electron, which is lost to form a 1+ ion; each forms a hydroxide and hydrogen.', '[2]'),
    ('Explain why the solution turns universal indicator purple after lithium has reacted with water.', 'Lithium hydroxide is formed, which is a soluble alkali (OH⁻ ions), so the pH is high.', '[2]'),
    ('Explain why sodium melts into a ball when it reacts with water but lithium does not.', 'The reaction is exothermic; sodium has a low melting point (98 °C) and the reaction is fast enough to melt it; lithium reacts more slowly and has a higher melting point (181 °C).', '[2]'),
])


def _gi(r, heavy=False):
    return r.choice(GI if heavy else GI[:3])


@t2b.add('C1', (1, 2, 3))
def t2b_obs(r, D):
    m = _gi(r)
    pool = [x[6] for x in GI[:3]] + ['sinks and slowly forms a white coating', 'there is no visible reaction']
    return mcq_q(r, f'A small piece of {m[0]} is added to a trough of water. Which observation is correct?', m[6], pool,
                 f'Reactivity increases down Group I: {m[0]} {m[6]}. 2{m[1]} + 2H₂O → 2{m[1]}OH + H₂.')


@t2b.add('C3', (1, 2, 3, 4))
def t2b_eq(r, D):
    m = _gi(r, True)
    rx = r.choice(['water', 'chlorine', 'oxygen'])
    eqs = {'water': (f'2{m[1]} + 2H2O -> 2{m[1]}OH + H2', f'{m[0]} hydroxide and hydrogen'), 'chlorine': (f'2{m[1]} + Cl2 -> 2{m[1]}Cl', f'{m[0]} chloride'),
           'oxygen': (f'4{m[1]} + O2 -> 2{m[1]}2O', f'{m[0]} oxide')}
    eq, prod = eqs[rx]
    if D == 1:
        pool = [E(x) for x in (f'{m[1]} + H2O -> {m[1]}OH + H2', f'2{m[1]} + 2H2O -> 2{m[1]}OH + H2', f'{m[1]} + 2H2O -> {m[1]}(OH)2 + H2', f'2{m[1]} + H2O -> {m[1]}2O + H2', f'2{m[1]} + Cl2 -> 2{m[1]}Cl', f'{m[1]} + Cl2 -> {m[1]}Cl2', f'4{m[1]} + O2 -> 2{m[1]}2O', f'{m[1]} + O2 -> {m[1]}O2', f'2{m[1]} + O2 -> 2{m[1]}O')]
        return mcq_q(r, f'Which is the balanced equation for the reaction of {m[0]} with {rx}?', E(eq), pool, f'{E(eq)}: Group I forms 1+ ions.')
    st = ' Include state symbols.' if D >= 3 else ''
    return {'stem': f'{m[0].capitalize()} reacts with {rx}. Name the product(s) and write the balanced symbol equation.{st}', 'answer': f'{prod}; {E(eq)}',
            'key': f'1 mark name(s); 1 mark formulae; 1 mark balanced' + (' ; 1 mark state symbols [4]' if st else ' [3]'), 'marks': 4 if st else 3}


@t2b.add('C3', (2, 3, 4, 5), 'numerical')
def t2b_h2(r, D):
    m = _gi(r)
    mass = r.choice([0.23, 0.46, 0.69, 0.115, 0.35, 0.39, 0.78, 0.21, 0.14, 1.17])
    n = mass / AR[m[1]]
    vol = n / 2 * VOL * 1000
    if D >= 4:
        Vw = r.choice([100, 200, 250, 500])
        c = n / (Vw / 1000)
        return {'stem': f'{sf(mass)} g of {m[0]} reacts completely with water and the solution is made up to {Vw} cm³. Calculate (a) the volume of hydrogen produced at r.t.p. in cm³ and (b) the concentration of the {m[0]} hydroxide solution in mol/dm³.',
                'answer': f'(a) {g3(vol)} cm³ (b) {g3(c)} mol/dm³', 'key': f'n({m[1]}) = {sf(mass)}/{AR[m[1]]} = {g3(n)} mol [1]; n(H₂) = {g3(n / 2)} mol; V = {g3(n / 2)} × 24 000 = {g3(vol)} cm³ [1]; n({m[1]}OH) = {g3(n)} mol; c = {g3(n)} ÷ {Vw / 1000} = {g3(c)} mol/dm³ [2]', 'marks': 4}
    return {'stem': f'{sf(mass)} g of {m[0]} reacts with excess water: 2{m[1]} + 2H₂O → 2{m[1]}OH + H₂. Calculate the volume of hydrogen produced at room temperature and pressure, in cm³. (1 mol of gas occupies 24 dm³ at r.t.p.)',
            'answer': f'{g3(vol)} cm³', 'key': f'n({m[1]}) = {sf(mass)}/{AR[m[1]]} = {g3(n)} mol [1]; n(H₂) = ½ × {g3(n)} = {g3(n / 2)} mol [1]; V = {g3(n / 2)} × 24 000 = {g3(vol)} cm³ [1]'}


@t2b.add('C3', (2, 3, 4))
def t2b_predict(r, D):
    prop = r.choice(['melting point', 'density'])
    i = 3 if r.random() < 0.6 else 4
    known = GI[:i]
    tgt = GI[i]
    val = {'melting point': 3, 'density': 4}[prop]
    unit = '°C' if prop == 'melting point' else 'g/cm³'
    rng = {'melting point': ('between 20 and 60 °C', 'below 63 °C'), 'density': ('greater than 0.86 g/cm³ (about 1.5 g/cm³)', '')}[prop]
    tbl = '; '.join(f'{x[0]} {x[val]} {unit}' for x in known)
    return {'stem': f'The {"melting points" if prop == "melting point" else "densities"} of some Group I metals are: {tbl}. Predict the {prop} of {tgt[0]} and describe how its reaction with water would compare with that of {known[-1][0]}.',
            'answer': f'About {tgt[val]} {unit} (accept a value consistent with the trend: {"lower than " + str(known[-1][3]) + " °C" if prop == "melting point" else "higher than " + str(known[-2][4])}); it reacts more violently/explosively than {known[-1][0]}.',
            'key': f'1 mark: prediction consistent with trend ({prop} {"decreases" if prop == "melting point" else "generally increases"} down the group); 1 mark: more reactive (explosive) [2]'}


def _gi_c4(r, D):
    m = _gi(r, True)
    other = r.choice([x for x in GI if x != m])
    p = person(r)
    mass = r.choice([0.14, 0.23, 0.39, 0.46, 0.78])
    lightish = m[:3] if m in GI[:3] else GI[1]
    n = mass / AR[lightish[1]]
    intro = r.choice([f'{p} watches a teacher add a small piece of {m[0]} to a trough of water containing a few drops of universal indicator.',
                      f'A video from a laboratory in {city(r)} shows {m[0]} and {other[0]} being added to separate troughs of cold water.',
                      f'An encyclopaedia lists the properties of {m[0]} (proton number {m[2]}), a Group I element.'])
    parts = [
        lambda r: (f'Describe what would be seen when {m[0]} is added to water.', m[6] + '; the indicator turns purple/blue.', '1 mark per observation, max [2]'),
        lambda r: ('Write the balanced symbol equation for the reaction with water.', E(f'2{m[1]} + 2H2O -> 2{m[1]}OH + H2'), '[2]'),
        lambda r: (f'Explain, in terms of atomic structure, why {m[0]} is {"more" if GI.index(m) > GI.index(other) else "less"} reactive than {other[0]}.',
                   f'{cap(m[0])} has {"more" if GI.index(m) > GI.index(other) else "fewer"} electron shells; its outer electron is {"further from" if GI.index(m) > GI.index(other) else "closer to"} the nucleus and {"less" if GI.index(m) > GI.index(other) else "more"} strongly attracted, so it is lost {"more" if GI.index(m) > GI.index(other) else "less"} easily.', '[3]'),
        lambda r: (f'Predict how the melting point of {m[0]} compares with that of {other[0]}.', f'{"lower" if GI.index(m) > GI.index(other) else "higher"}: melting point decreases down the group', '[1]'),
        lambda r: (f'A {sf(mass)} g piece of {lightish[0]} is used. Calculate the volume of hydrogen formed at r.t.p.', f'{g3(n / 2 * 24000)} cm³', f'n = {sf(mass)}/{AR[lightish[1]]}; ÷2; × 24 000 cm³ [3]'),
        lambda r: ('Suggest one safety precaution needed for this demonstration.', 'Use a very small piece / safety screen / goggles / tongs, not fingers.', '[1]'),
        lambda r: (f'State the formula of the ion formed by {m[0]} and explain its charge.', f'{m[1]}⁺: it loses its single outer electron.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t2b.add('C4', (2, 3, 4, 5), 'multi_step')(_gi_c4)
t2b.add('C3', (3, 4, 5), 'multi_step')(_gi_c4)

# ---------------------------------------------------------- 2.3 Group VII
HAL = [('fluorine', 'F', 'pale yellow', 'gas', 'colourless'), ('chlorine', 'Cl', 'pale yellow-green', 'gas', 'pale yellow-green'),
       ('bromine', 'Br', 'red-brown', 'liquid', 'orange'), ('iodine', 'I', 'grey-black', 'solid', 'brown'), ('astatine', 'At', 'black', 'solid', 'dark brown')]
HALIDE = {'Cl': 'chloride', 'Br': 'bromide', 'I': 'iodide'}

t2c = topic('Group VII halogens', 'group vii halogens', 'colours, physical states, trends and displacement reactions', 'halogens displacement')
t2c.fixed('C1', (1, 2), [
    ('What is the colour and state of bromine at room temperature?', 'red-brown liquid', 'Cl₂ pale yellow-green gas; Br₂ red-brown liquid; I₂ grey-black solid.', ['pale yellow-green gas', 'grey-black solid', 'colourless liquid']),
    ('How does the reactivity of the halogens change down Group VII?', 'It decreases', 'F > Cl > Br > I: the atom gains an electron less easily as it gets larger.', ['It increases', 'It stays the same', 'It increases then decreases']),
    ('Which halogen is a grey-black solid at room temperature?', 'iodine', 'Iodine is a grey-black solid that gives a purple vapour on warming.', ['chlorine', 'bromine', 'fluorine']),
    ('Halogens exist as', 'diatomic molecules', 'Each halogen is X₂, two atoms joined by a single covalent bond.', ['single atoms', 'giant ionic lattices', 'metallic lattices']),
    ('Which mixture reacts?', 'chlorine water and aqueous potassium iodide', 'Cl₂ is more reactive than I₂, so it displaces iodide: Cl₂ + 2I⁻ → 2Cl⁻ + I₂.', ['iodine solution and aqueous potassium chloride', 'bromine water and aqueous potassium chloride', 'iodine solution and aqueous potassium bromide']),
    ('State how the melting and boiling points of the halogens change down the group.', 'They increase.', '[1]'),
])
t2c.fixed('C2', (2, 3, 4), [
    ('Explain why the reactivity of the halogens decreases down Group VII.', 'Atoms get larger with more shells, so the nucleus attracts an incoming electron less strongly; the atom gains an electron less easily.', '1 mark: more shells/larger atom; 1 mark: electron gained less easily [2]'),
    ('Explain why bromine water does not react with aqueous potassium chloride.', 'Bromine is less reactive than chlorine, so it cannot displace chloride ions.', '[2]'),
    ('Explain why the reaction between chlorine and potassium bromide is a redox reaction.', 'Chlorine gains electrons (reduced) to form Cl⁻; bromide ions lose electrons (oxidised) to form Br₂.', '1 mark each [2]'),
    ('Explain why all halogens have similar chemical properties.', 'Each atom has seven outer electrons and gains one electron to form a 1− ion.', '[2]'),
    ('A student says, "Iodine is more reactive than bromine because it is a solid." Explain why this is wrong.', 'Physical state does not determine reactivity; iodine is less reactive because its larger atoms gain an electron less easily.', '[2]'),
])


@t2c.add('C1', (1, 2, 3))
def t2c_prop(r, D):
    h = r.choice(HAL[:4])
    q = r.choice(['colour', 'state'])
    if q == 'colour':
        return mcq_q(r, f'What colour is {h[0]} at room temperature?', h[2], [x[2] for x in HAL[:4]] + ['colourless'], f'{h[0]}: {h[2]} {h[3]}.')
    return mcq_q(r, f'What is the physical state of {h[0]} at room temperature and pressure?', h[3], ['gas', 'liquid', 'solid', 'aqueous solution'], f'{h[0]}: {h[2]} {h[3]}.')


def disp(x, y, metal='K'):
    """halogen x key, halide y key -> (reacts, eq, ion, obs)"""
    order = ['F', 'Cl', 'Br', 'I', 'At']
    react = order.index(x) < order.index(y)
    X = HAL[order.index(x)]; Y = HAL[order.index(y)]
    if not react:
        return False, None, None, 'no change; the solution stays the colour of the halogen solution'
    eq = f'{x}2 + 2{metal}{y} -> 2{metal}{x} + {y}2'
    ion = f'{x}2 + 2{y}^- -> 2{x}^- + {y}2'
    obs = f'the colourless solution turns {Y[4]} as {Y[0]} is formed'
    return True, eq, ion, obs


@t2c.add('C3', (1, 2, 3, 4))
def t2c_disp(r, D):
    x, y = r.sample(['Cl', 'Br', 'I'], 2)
    metal = r.choice(['K', 'Na'])
    react, eq, ion, obs = disp(x, y, metal)
    X = HAL[['F', 'Cl', 'Br', 'I'].index(x)]
    sal = f'{"potassium" if metal == "K" else "sodium"} {HALIDE[y]}'
    if D == 1:
        corr = obs if react else 'no change; the solution stays the colour of the halogen solution'
        pool = ['the solution turns orange as bromine is formed', 'the solution turns brown as iodine is formed', 'a white precipitate forms', 'no change; the solution stays the colour of the halogen solution', 'the solution turns pale yellow-green as chlorine is formed']
        return mcq_q(r, f'Aqueous {X[0]} is added to aqueous {sal}. What is observed?', corr, pool, (E(ion) if react else f'{X[0]} is less reactive than {HAL[["F", "Cl", "Br", "I"].index(y)][0]}: no displacement.'))
    st = ' and the ionic equation' if D >= 3 else ''
    if react:
        return {'stem': f'Aqueous {X[0]} is added to aqueous {sal}. Predict whether a reaction occurs. If it does, describe the colour change and write the balanced symbol equation{st}.',
                'answer': f'Yes — {obs}. {E(eq)}' + (f'; ionic: {E(ion)}' if st else ''), 'key': f'1 mark: reaction because {X[0]} is more reactive; 1 mark: colour; 1 mark: equation' + ('; 1 mark ionic equation [4]' if st else ' [3]'), 'marks': 4 if st else 3}
    return {'stem': f'Aqueous {X[0]} is added to aqueous {sal}. Predict whether a reaction occurs and explain your answer.',
            'answer': f'No reaction: {X[0]} is less reactive than {HAL[["F", "Cl", "Br", "I"].index(y)][0]}, so it cannot displace the {HALIDE[y]} ion.', 'key': '1 mark: no reaction; 1 mark: reactivity reason [2]'}


@t2c.add('C2', (2, 3, 4), 'explain')
def t2c_redox(r, D):
    x, y = r.choice([('Cl', 'Br'), ('Cl', 'I'), ('Br', 'I')])
    react, eq, ion, obs = disp(x, y)
    X = HAL[['F', 'Cl', 'Br', 'I'].index(x)]; Y = HAL[['F', 'Cl', 'Br', 'I'].index(y)]
    return {'stem': f'{E(ion)}. Identify the oxidising agent and the species that is oxidised in this reaction, explaining your answer in terms of electron transfer.',
            'answer': f'{X[0]} ({F(x + "2")}) is the oxidising agent — it gains electrons and is reduced to {F(x + "^-")}; the {HALIDE[y]} ions ({F(y + "^-")}) are oxidised — they lose electrons to form {F(y + "2")}.',
            'key': '1 mark oxidising agent; 1 mark species oxidised; 1 mark electron transfer explanation [3]', 'marks': 3}


@t2c.add('C3', (2, 3, 4))
def t2c_astatine(r, D):
    q = r.choice(['state and colour', 'reaction with potassium iodide', 'reactivity compared with iodine', 'boiling point'])
    ans = {'state and colour': 'A black solid (darker than iodine, solid because melting/boiling points increase down the group).',
           'reaction with potassium iodide': 'No reaction: astatine is less reactive than iodine so cannot displace iodide ions.',
           'reactivity compared with iodine': 'Less reactive than iodine: reactivity decreases down Group VII.',
           'boiling point': 'Higher than that of iodine (184 °C): boiling point increases down the group.'}[q]
    return {'stem': f'Astatine is below iodine in Group VII. Use the trends in the group to predict its {q}, giving a reason.', 'answer': ans, 'key': '1 mark prediction; 1 mark trend reason [2]'}


def _hal_c4(r, D):
    hs = ['Cl', 'Br', 'I']
    rows = []
    for x in hs:
        for y in hs:
            if x != y:
                rows.append((x, y, disp(x, y)))
    sel = r.sample(rows, 4)
    names = {'Cl': 'chlorine', 'Br': 'bromine', 'I': 'iodine'}
    p = person(r)
    intro = f'{p} adds aqueous halogens to aqueous potassium halides in a spotting tile. The mixtures tested are: ' + '; '.join(f'{names[a]} + potassium {HALIDE[b]}' for a, b, _ in sel) + '.'
    yes = [(a, b, d) for a, b, d in sel if d[0]]
    parts = [
        lambda r: ('State which of these mixtures react.', '; '.join(f'{names[a]} + {HALIDE[b]}' for a, b, d in yes) or 'none', '1 mark per correct mixture, no extras [2]'),
        lambda r: (('Describe the colour change for the first mixture that reacts.', yes[0][2][3], '[1]') if yes else ('Explain why none of the mixtures react.', 'Each halogen is less reactive than the halogen in the halide.', '[1]')),
        lambda r: (('Write the ionic equation for the first mixture that reacts.', E(yes[0][2][2]), '[2]') if yes else None),
        lambda r: ('Use the results to put chlorine, bromine and iodine in order of reactivity, most reactive first.', 'chlorine > bromine > iodine', '[1]'),
        lambda r: ('Explain this order in terms of the electronic structure of the atoms.', 'Down the group atoms have more shells; the nucleus attracts an extra electron less strongly, so the halogen gains electrons less readily.', '[2]'),
        lambda r: ('Suggest why the experiment is done in a fume cupboard.', 'Chlorine and bromine vapours are toxic.', '[1]'),
        lambda r: (('Identify the reducing agent in the first mixture that reacts.', f'{HALIDE[yes[0][1]]} ions ({F(yes[0][1] + "^-")})', '[1]') if yes else None),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t2c.add('C4', (2, 3, 4, 5), 'case')(_hal_c4)
t2c.add('C3', (3, 4), 'case')(_hal_c4)

# ---------------------------------------------------------- 2.4 Transition elements
OXN = [('FeO', 'iron', 2), ('Fe2O3', 'iron', 3), ('FeCl3', 'iron', 3), ('FeSO4', 'iron', 2), ('CuO', 'copper', 2), ('Cu2O', 'copper', 1), ('CuCl', 'copper', 1),
       ('MnO2', 'manganese', 4), ('KMnO4', 'manganese', 7), ('Cr2O3', 'chromium', 3), ('K2Cr2O7', 'chromium', 6), ('CrCl3', 'chromium', 3), ('V2O5', 'vanadium', 5),
       ('NiO', 'nickel', 2), ('CoCl2', 'cobalt', 2), ('Fe(OH)3', 'iron', 3), ('Fe(OH)2', 'iron', 2), ('Cu(NO3)2', 'copper', 2), ('MnSO4', 'manganese', 2), ('VO2', 'vanadium', 4)]
ROM_OX = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}
TCOL = [('Cu²⁺', 'blue'), ('Fe²⁺', 'pale green'), ('Fe³⁺', 'yellow-brown'), ('Cr³⁺', 'green'), ('MnO₄⁻', 'purple'), ('Cr₂O₇²⁻', 'orange'), ('Co²⁺', 'pink')]
CATS = [('iron', 'the Haber process to make ammonia'), ('vanadium(V) oxide', 'the Contact process to make sulfuric acid'), ('manganese(IV) oxide', 'the decomposition of hydrogen peroxide'),
        ('nickel', 'the hydrogenation of vegetable oils'), ('platinum and rhodium', 'catalytic converters in car exhausts')]

t2d = topic('Transition elements', 'transition elements', 'high density, variable oxidation numbers, coloured compounds and catalysts', 'transition metals')
t2d.fixed('C1', (1, 2), [
    ('Which property is typical of transition elements but not of Group I metals?', 'They form coloured compounds', 'Transition elements: high density, high m.p., coloured compounds, variable oxidation numbers, catalysts.', ['They have low densities', 'They react vigorously with cold water', 'They have low melting points']),
    ('Which catalyst is used in the Haber process?', 'iron', 'Iron catalyses N₂ + 3H₂ ⇌ 2NH₃.', ['vanadium(V) oxide', 'nickel', 'platinum']),
    ('Why is the name iron(III) oxide used for Fe₂O₃?', 'Iron has an oxidation number of +3 in this compound', 'Roman numerals give the oxidation number of the transition element.', ['There are three oxygen atoms', 'There are three iron atoms', 'Iron is in Group III']),
    ('What colour is a solution containing Cu²⁺ ions?', 'blue', 'Aqueous copper(II) ions are blue.', ['green', 'colourless', 'purple']),
    ('Compared with sodium, iron has', 'a higher density and a higher melting point', 'Transition elements are dense, hard, high-melting metals.', ['a lower density and a lower melting point', 'a lower density and a higher melting point', 'the same density and melting point']),
    ('State two properties of transition elements that make them useful as structural metals.', 'High density/strength and high melting point (hard, strong).', '[2]'),
])
t2d.fixed('C2', (2, 3, 4), [
    ('Explain why transition elements are useful in industry as catalysts.', 'They (or their compounds) speed up reactions without being used up, so less energy/lower temperatures are needed and costs fall.', '[2]'),
    ('Compare the physical properties of the Group I metals and the transition elements.', 'Group I: soft, low density, low melting points; transition elements: hard, high density, high melting points.', '1 mark each comparison, max [3]'),
    ('Explain what is meant by "variable oxidation number", using iron as an example.', 'An element can form ions with different charges in different compounds, e.g. Fe²⁺ in iron(II) sulfate and Fe³⁺ in iron(III) chloride.', '[2]'),
    ('Explain how you could tell from appearance alone that a compound probably contains a transition element.', 'Transition element compounds are usually coloured (e.g. blue copper(II) sulfate); compounds of Group I and II metals are usually white or colourless.', '[2]'),
])


@t2d.add('C3', (1, 2, 3, 4))
def t2d_ox(r, D):
    f, el, n = r.choice(OXN)
    if D == 1:
        return nmcq(r, f'What is the oxidation number of {el} in {F(f)}?', n, [x for x in (1, 2, 3, 4, 5, 6, 7) if x != n], '', f'Sum of oxidation numbers = 0 (O −2, Cl −1, K +1, SO₄ −2, NO₃ −1, OH −1) → {el} +{n}.', f=lambda x: f'+{int(x)}')
    return {'stem': f'Deduce the oxidation number of {el} in {F(f)} and hence name the compound using a Roman numeral.' if f not in ('KMnO4', 'K2Cr2O7') else f'Deduce the oxidation number of {el} in {F(f)}, showing your working.',
            'answer': f'+{n}' + (f'; {el}({ROM_OX[n]}) compound' if f not in ('KMnO4', 'K2Cr2O7') else ''),
            'key': f'Oxidation numbers in a compound sum to zero; O = −2, Cl = −1, K = +1, SO₄ = −2, NO₃ = −1, OH = −1 [1]; {el} = +{n} [1]'}


@t2d.add('C1', (1, 2, 3))
def t2d_col(r, D):
    ion, col = r.choice(TCOL)
    return mcq_q(r, f'What colour is an aqueous solution containing {ion} ions?', col, [c for _, c in TCOL] + ['colourless'], f'{ion}(aq) is {col}; coloured ions are typical of transition elements.')


@t2d.add('C1', (1, 2, 3))
def t2d_cat(r, D):
    c, use = r.choice(CATS)
    return mcq_q(r, f'Which substance is used as a catalyst in {use}?', c, [x for x, _ in CATS] + ['aluminium oxide', 'sodium'], f'{c} catalyses {use}; transition elements and their compounds are good catalysts.')


TDATA = [('sodium', 0.97, 98, 'white', 'Group I'), ('potassium', 0.86, 63, 'white', 'Group I'), ('calcium', 1.55, 842, 'white', 'Group II'), ('magnesium', 1.74, 650, 'white', 'Group II'),
         ('iron', 7.87, 1538, 'green or brown', 'transition'), ('copper', 8.96, 1085, 'blue or green', 'transition'), ('chromium', 7.19, 1907, 'green or orange', 'transition'),
         ('nickel', 8.91, 1455, 'green', 'transition'), ('manganese', 7.21, 1246, 'pink or purple', 'transition'), ('cobalt', 8.90, 1495, 'pink or blue', 'transition')]


@t2d.add('C3', (2, 3, 4))
def t2d_data(r, D):
    tr = r.sample([x for x in TDATA if x[4] == 'transition'], 1)
    ot = r.sample([x for x in TDATA if x[4] != 'transition'], 2)
    rows = tr + ot
    r.shuffle(rows)
    L = 'JLM'
    tab = '; '.join(f'{L[i]}: density {x[1]} g/cm³, melting point {x[2]} °C, compounds {x[3]}' for i, x in enumerate(rows))
    i = rows.index(tr[0])
    return {'stem': f'Data for three metals are given. {tab}. Deduce which metal is a transition element and give two pieces of evidence from the data.',
            'answer': f'{L[i]} ({tr[0][0]}): high density, high melting point and coloured compounds.', 'key': '1 mark correct letter; 1 mark each for two pieces of evidence [3]', 'marks': 3}


def _tr_c4(r, D):
    f, el, n = r.choice([x for x in OXN if x[0] not in ('KMnO4', 'K2Cr2O7', 'VO2')])
    f2 = r.choice([x for x in OXN if x[1] == el and x[2] != n] or [None])
    c, use = r.choice(CATS)
    intro = r.choice([f'A pigment manufacturer in {city(r)} uses compounds of {el}, such as {F(f)}.', f'{person(r)} is researching {el}, a transition element, and its compound {F(f)}.',
                      f'A museum display shows minerals that contain {el}, including one with the formula {F(f)}.'])
    parts = [
        lambda r: (f'Deduce the oxidation number of {el} in {F(f)}.', f'+{n}', '[1]'),
        lambda r: (f'Name {F(f)} using a Roman numeral.', f'{el}({ROM_OX[n]}) ' + {'O': 'oxide'}.get(f[-1], 'compound'), '[1]') if f.endswith('O') or f.endswith('O3') else None,
        lambda r: ((f'{el.capitalize()} also forms {F(f2[0])}. Explain what this shows about transition elements.', f'They have variable oxidation numbers: here +{f2[2]} compared with +{n}.', '[2]') if f2 else None),
        lambda r: (f'Give two physical properties of {el} that are typical of transition elements.', 'High density; high melting point (also hard, strong, good conductor).', '[2]'),
        lambda r: (f'{cap(c)} is used in {use}. State what is meant by a catalyst.', 'A substance that increases the rate of a reaction and is unchanged at the end.', '[1]'),
        lambda r: (f'Predict, with a reason, whether {F(f)} is likely to be white or coloured.', 'Coloured: compounds of transition elements are usually coloured.', '[1]'),
        lambda r: (f'Compare the reaction of {el} with cold water with that of sodium.', f'{cap(el)} reacts very slowly or not at all with cold water; sodium reacts vigorously, producing hydrogen.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t2d.add('C4', (2, 3, 4, 5), 'multi_step')(_tr_c4)
t2d.add('C3', (3, 4), 'multi_step')(_tr_c4)

# ---------------------------------------------------------- 2.5 noble gases
NOBLE = [('helium', 'He', 2, '2', -269, 'filling balloons and airships', 'it has a very low density and is unreactive (non-flammable)'),
         ('neon', 'Ne', 10, '2,8', -246, 'advertising signs', 'it glows brightly when electricity passes through it'),
         ('argon', 'Ar', 18, '2,8,8', -186, 'filling filament lamps and as a shield gas in welding', 'it is unreactive, so the hot metal does not react with oxygen'),
         ('krypton', 'Kr', 36, '2,8,18,8', -153, 'some lasers and high-performance lamps', 'it is unreactive and glows when electricity passes'),
         ('xenon', 'Xe', 54, '2,8,18,18,8', -108, 'bright car headlamps and camera flashes', 'it gives an intense light when electricity passes')]

t2e = topic('Noble gases', 'noble gases', 'unreactivity explained by electronic configuration and uses', 'group viii')
t2e.fixed('C1', (1, 2), [
    ('Why are the noble gases unreactive?', 'They have full outer electron shells', 'A full outer shell is stable, so noble gas atoms do not lose, gain or share electrons.', ['They have no electrons', 'They are all liquids', 'They have one outer electron']),
    ('Noble gases exist as', 'single atoms (monatomic)', 'Their atoms are stable, so they do not bond to each other.', ['diatomic molecules', 'giant covalent structures', 'ionic lattices']),
    ('Which gas is used to fill weather balloons?', 'helium', 'Helium has a low density and is non-flammable.', ['argon', 'hydrogen chloride', 'neon']),
    ('How does the boiling point of the noble gases change down the group?', 'It increases', 'He −269 °C, Ne −246 °C, Ar −186 °C: boiling point increases down the group.', ['It decreases', 'It stays the same', 'It decreases then increases']),
    ('State the electronic configuration of argon.', '2,8,8', '[1]'),
])
t2e.fixed('C2', (2, 3, 4), [
    ('Explain why argon is used to fill filament lamps instead of air.', 'Argon is unreactive, so the very hot tungsten filament does not react (oxidise) and burn away, as it would in oxygen.', '[2]'),
    ('Explain why helium is safer than hydrogen for filling airships.', 'Both have low density, but helium is unreactive and does not burn, whereas hydrogen is flammable/explosive in air.', '[2]'),
    ('Explain, using electronic configurations, why neon does not form compounds but sodium does.', 'Neon (2,8) has a full outer shell so it is stable; sodium (2,8,1) loses one electron easily to reach a full outer shell.', '[2]'),
    ('Explain why the noble gases are placed in Group VIII (or 0).', 'They all have full outer shells (eight electrons, or two for helium) and similar unreactive properties.', '[2]'),
])


@t2e.add('C1', (1, 2, 3))
def t2e_use(r, D):
    g = r.choice(NOBLE[:3])
    return mcq_q(r, f'Which noble gas is used for {g[5]}?', g[0], [x[0] for x in NOBLE], f'{g[0]}: {g[6]}.')


@t2e.add('C2', (2, 3, 4), 'explain')
def t2e_why(r, D):
    g = r.choice(NOBLE)
    return {'stem': f'{cap(g[0])} is used for {g[5]}. Explain which property makes it suitable.', 'answer': cap(g[6]) + '.', 'key': '1 mark property; 1 mark link to use [2]'}


@t2e.add('C3', (2, 3, 4))
def t2e_pred(r, D):
    k = r.choice([3, 4])
    known = NOBLE[:k]
    tgt = NOBLE[k]
    tbl = '; '.join(f'{x[0]} {x[4]} °C'.replace('-', '−') for x in known)
    return {'stem': f'The boiling points of some noble gases are: {tbl}. Predict the boiling point of {tgt[0]} and state its physical state at room temperature. Explain why it does not react with fluorine easily.',
            'answer': f'About {tgt[4]} °C (any value between {known[-1][4] + 20} and {known[-1][4] + 80} °C)'.replace('-', '−') + '; gas; full outer shell ({tgt[3]}) so it is very unreactive.',
            'key': '1 mark prediction following trend; 1 mark gas; 1 mark full outer shell [3]', 'marks': 3}


def _ng_c4(r, D):
    g = r.choice(NOBLE)
    o = r.choice([x for x in NOBLE if x != g])
    intro = r.choice([f'A lighting company in {city(r)} uses {g[0]} in its products.', f'{person(r)} reads that {g[0]} (proton number {g[2]}) is used for {g[5]}.', f'Air contains small amounts of noble gases including {g[0]} and {o[0]}.'])
    parts = [
        lambda r: (f'Give the electronic configuration of {g[0]}.', g[3], '[1]'),
        lambda r: (f'Explain why {g[0]} is unreactive.', 'Its outer shell is full, so it does not need to lose, gain or share electrons.', '[2]'),
        lambda r: (f'State why {g[0]} is described as monatomic.', 'It exists as single atoms, not molecules.', '[1]'),
        lambda r: (f'Explain why {g[0]} is suitable for {g[5]}.', cap(g[6]) + '.', '[2]'),
        lambda r: (f'Predict whether {g[0]} has a higher or lower boiling point than {o[0]}.', 'higher' if g[4] > o[4] else 'lower', 'boiling point increases down the group [1]'),
        lambda r: ('Suggest how noble gases are obtained from the air.', 'By fractional distillation of liquid air.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


@t2e.add('C3', (1, 2, 3, 4), 'numerical')
def t2e_balloon(r, D):
    g = r.choice(NOBLE[:3])
    V = r.choice([2.4, 4.8, 6.0, 7.2, 12.0, 3.6, 9.6])
    n = V / VOL
    m = n * AR[g[1]]
    if D == 1:
        return nmcq(r, f'A balloon contains {sf(V)} dm³ of {g[0]} at room temperature and pressure. How many moles of {g[0]} atoms does it contain?', n, [V * 24, n * 2, n / 2, V / 22.4 * 2], ' mol', f'n = V/24 = {sf(V)}/24 = {g3(n)} mol.')
    extra = ''
    if D >= 3:
        ma = n * 29
        extra = f' The same volume of air (mean Mr 29) has a mass of {g3(ma)} g. Use this to explain why a {g[0]}-filled balloon ' + ('rises.' if AR[g[1]] < 29 else 'does not rise.')
    return {'stem': f'A balloon is filled with {sf(V)} dm³ of {g[0]} at r.t.p. Calculate the mass of {g[0]} in the balloon (Ar {g[1]} = {AR[g[1]]}).{extra}',
            'answer': f'{g3(m)} g' + ((' — it is ' + ('less' if AR[g[1]] < 29 else 'more') + ' dense than air.') if extra else ''),
            'key': f'n = {sf(V)}/24 = {g3(n)} mol [1]; mass = {g3(n)} × {AR[g[1]]} = {g3(m)} g [1]' + ('; compares mass/density with air [1]' if extra else ''), 'marks': 3 if extra else 2}


t2e.add('C4', (2, 3, 4, 5), 'multi_step')(_ng_c4)
t2e.add('C3', (3, 4), 'multi_step')(_ng_c4)

CHAPTERS[2] = [t2a, t2b, t2c, t2d, t2e]


# ===================================================================== Ch3 (CB14) Metallic elements and alloys
# metal: name, symbol, charge, acid observation, oxide formula, O2 equation, burning observation
MET = {
    'Mg': ('magnesium', 'Mg', 2, 'rapid fizzing; the metal dissolves quickly and the tube gets warm', 'MgO', '2Mg + O2 -> 2MgO', 'burns with a bright white flame forming a white powder'),
    'Zn': ('zinc', 'Zn', 2, 'steady fizzing; the metal slowly dissolves', 'ZnO', '2Zn + O2 -> 2ZnO', 'glows and forms a solid that is yellow when hot and white when cold'),
    'Fe': ('iron', 'Fe', 2, 'slow fizzing; a pale green solution forms', 'Fe2O3', '4Fe + 3O2 -> 2Fe2O3', 'iron wool burns with orange sparks forming a dark solid'),
    'Ca': ('calcium', 'Ca', 2, 'very rapid fizzing; the metal dissolves quickly', 'CaO', '2Ca + O2 -> 2CaO', 'burns with an orange-red flame forming a white solid'),
    'Al': ('aluminium', 'Al', 3, 'slow at first (oxide layer), then steady fizzing', 'Al2O3', '4Al + 3O2 -> 2Al2O3', 'powdered aluminium burns with a bright white flame forming a white solid'),
    'Cu': ('copper', 'Cu', 2, 'no reaction', 'CuO', '2Cu + O2 -> 2CuO', 'does not burn; the surface turns black when heated'),
}


def acid_eq(m, a='Cl'):
    nm, sym, q = MET[m][:3]
    if m == 'Cu':
        return None
    acid = ACID[a][1]
    if q == 2:
        k = 2 if ACID[a][2] == 1 else 1
        return f'{sym} + {str(k) if k > 1 else ""}{acid} -> {salt_f("Fe2" if m == "Fe" else m, a)} + H2'
    # Al
    if a == 'SO4':
        return '2Al + 3H2SO4 -> Al2(SO4)3 + 3H2'
    return f'2Al + 6{acid} -> 2Al{AN[a][1] if a == "Cl" else "(NO3)"}3 + 3H2'


def salt_name_metal(m, a):
    return salt_n('Fe2' if m == 'Fe' else m, a)


t3a = topic('Properties and reactions of metals', 'physical and chemical properties of metals', 'reactions with dilute acids, water and oxygen', 'properties of metals')
t3a.fixed('C1', (1, 2), [
    ('Which property is shown by all metals?', 'They conduct electricity when solid', 'Metals have delocalised electrons, so they conduct as solids.', ['They have low melting points', 'They are brittle', 'They form acidic oxides']),
    ('Which word describes a metal that can be drawn out into wires?', 'ductile', 'Ductile = can be drawn into wires; malleable = can be hammered into shape.', ['malleable', 'brittle', 'volatile']),
    ('What are the products when zinc reacts with dilute hydrochloric acid?', 'zinc chloride and hydrogen', 'Zn + 2HCl → ZnCl₂ + H₂.', ['zinc chloride and water', 'zinc oxide and hydrogen', 'zinc hydroxide and chlorine']),
    ('Which metal does not react with dilute hydrochloric acid?', 'copper', 'Copper is below hydrogen in the reactivity series.', ['magnesium', 'zinc', 'iron']),
    ('Metal oxides are generally', 'basic', 'Metal oxides react with acids to form a salt and water.', ['acidic', 'neutral', 'gases']),
    ('State two physical properties that are typical of metals but not of non-metals.', 'Any two: good conductors of heat and electricity; malleable; ductile; shiny; high density; high melting point.', '[2]'),
])
t3a.fixed('C2', (2, 3, 4), [
    ('Explain why metals are malleable.', 'The layers of positive ions can slide over each other without breaking the metallic bonds, because the delocalised electrons hold the ions together.', '[2]'),
    ('Compare the physical properties of metals and non-metals.', 'Metals: good conductors, malleable/ductile, shiny, usually high m.p.; non-metals: poor conductors (except graphite), brittle when solid, dull, usually low m.p.', '1 mark per comparison, max [3]'),
    ('Explain why magnesium ribbon is cleaned with sandpaper before it is reacted with acid.', 'To remove the layer of magnesium oxide, so the metal itself reacts and the rate is not slowed.', '[2]'),
    ('Describe a test to identify the gas formed when a metal reacts with a dilute acid.', 'Hold a lighted splint at the mouth of the tube: it burns with a squeaky pop (hydrogen).', '[2]'),
    ('Explain why aluminium reacts slowly with dilute acid at first and then more quickly.', 'A thin protective oxide layer must react/dissolve first; once the metal surface is exposed it reacts steadily.', '[2]'),
])


@t3a.add('C1', (1, 2, 3))
def t3a_obs(r, D):
    m = r.choice(list(MET))
    nm = MET[m][0]
    return mcq_q(r, f'A piece of {nm} is added to dilute hydrochloric acid. What is observed?', MET[m][3], [MET[x][3] for x in MET] + ['a white precipitate forms immediately'], f'{nm}: {MET[m][3]}.' + (f' {E(acid_eq(m))}' if acid_eq(m) else ''))


@t3a.add('C3', (1, 2, 3, 4))
def t3a_eq(r, D):
    m = r.choice([x for x in MET if x != 'Cu'])
    rx = r.choice(['acid', 'oxygen'])
    nm = MET[m][0]
    if rx == 'acid':
        a = r.choice(list(ACID))
        eq = acid_eq(m, a)
        if D == 1:
            pool = [F(salt_f('Fe2' if m == 'Fe' else m, x)) for x in ACID] + [F(MET[m][4]), F(salt_f('Fe3', a)) if m == 'Fe' else F(f'{m}{AN[a][1]}' if MET[m][2] > 1 else f'{m}2{AN[a][1]}')]
            corr = F(salt_f('Fe2' if m == 'Fe' else m, a))
            return mcq_q(r, f'{cap(nm)} reacts with dilute {ACID[a][0]}. What is the formula of the salt formed?', corr, pool, E(eq))
        return {'stem': f'Write the word equation and the balanced symbol equation for the reaction of {nm} with dilute {ACID[a][0]}.' + (' Include state symbols.' if D >= 3 else ''),
                'answer': f'{nm} + {ACID[a][0]} → {salt_name_metal(m, a)} + hydrogen; {E(eq)}', 'key': f'word equation [1]; formulae [1]; balancing [1]' + ('; state symbols [1]' if D >= 3 else ''), 'marks': 4 if D >= 3 else 3}
    eq = MET[m][5]
    if D == 1:
        return mcq_q(r, f'What is formed when {nm} burns in oxygen?', f'{nm} oxide, {F(MET[m][4])}', [f'{nm} oxide, {F(x)}' for x in ('MgO', 'Al2O3', 'Fe2O3', 'CaO', 'ZnO', 'CuO') if x != MET[m][4] and x[:2] == MET[m][4][:2]] + [f'{nm} hydroxide', f'{nm} carbonate', 'hydrogen'], E(eq))
    return {'stem': f'Describe what is seen when {nm} is heated in oxygen, and write the balanced equation.', 'answer': f'{cap(MET[m][6])}; {E(eq)}', 'key': '1 mark observation; 1 mark formulae; 1 mark balanced [3]', 'marks': 3}


@t3a.add('C3', (2, 3, 4, 5), 'numerical')
def t3a_h2(r, D):
    m = r.choice(['Mg', 'Zn', 'Fe', 'Al', 'Ca'])
    a = 'Cl' if r.random() < 0.6 else 'SO4'
    nm = MET[m][0]
    mass = r.choice([0.12, 0.24, 0.36, 0.48, 0.60]) if m == 'Mg' else (r.choice([0.27, 0.54, 0.81, 1.08]) if m == 'Al' else r.choice([0.65, 1.30, 1.96, 0.56, 1.12, 0.40, 0.80, 2.60]))
    if m == 'Zn' and mass in (0.56, 1.12, 1.96):
        mass = 1.30
    n = mass / AR[m]
    ratio = 1.5 if m == 'Al' else 1
    nh = n * ratio
    v = nh * VOL * 1000
    eq = E(acid_eq(m, a))
    if D >= 4:
        mo = mass * 2.5
        return {'stem': f'{person(r)} reacts {sf(mass)} g of {nm} with excess dilute {ACID[a][0]}. {eq}. Calculate (a) the volume of hydrogen at r.t.p. in cm³ and (b) the mass of {salt_name_metal(m, a)} that could be obtained.',
                'answer': f'(a) {g3(v)} cm³ (b) {g3(n / (2 if m == "Al" else 1) * Mr(salt_f("Fe2" if m == "Fe" else m, a)))} g',
                'key': f'n({m}) = {sf(mass)}/{AR[m]} = {g3(n)} mol [1]; n(H₂) = {g3(nh)} mol, V = {g3(v)} cm³ [1]; n(salt) = {g3(n / (2 if m == "Al" else 1))} mol × Mr {mr(Mr(salt_f("Fe2" if m == "Fe" else m, a)))} = {g3(n / (2 if m == "Al" else 1) * Mr(salt_f("Fe2" if m == "Fe" else m, a)))} g [2]', 'marks': 4}
    return {'stem': f'Calculate the volume of hydrogen, in cm³ at r.t.p., produced when {sf(mass)} g of {nm} reacts with excess dilute {ACID[a][0]}. {eq}',
            'answer': f'{g3(v)} cm³', 'key': f'n({m}) = {sf(mass)}/{AR[m]} = {g3(n)} mol [1]; n(H₂) = {g3(nh)} mol [1]; V = {g3(nh)} × 24 000 = {g3(v)} cm³ [1]'}


@t3a.add('C3', (2, 3, 4), 'numerical')
def t3a_oxide(r, D):
    m = r.choice(['Mg', 'Ca', 'Zn', 'Cu'])
    nm = MET[m][0]
    mass = r.choice([0.24, 0.48, 0.72, 1.20, 2.40]) if m == 'Mg' else (r.choice([0.40, 0.80, 2.00]) if m == 'Ca' else (r.choice([0.65, 1.30, 3.25]) if m == 'Zn' else r.choice([0.64, 1.28, 3.20])))
    mo = mass / AR[m] * Mr(MET[m][4])
    return {'stem': f'{sf(mass)} g of {nm} is heated in air until it is completely converted to {nm} oxide, {F(MET[m][4])}. {E(MET[m][5])}. Calculate the mass of oxide formed and the increase in mass.',
            'answer': f'{g3(mo)} g; increase {g3(mo - mass)} g', 'key': f'n = {sf(mass)}/{AR[m]} = {g3(mass / AR[m])} mol [1]; n(oxide) the same; mass = {g3(mass / AR[m])} × {mr(Mr(MET[m][4]))} = {g3(mo)} g [1]; increase = {g3(mo - mass)} g (mass of oxygen combined) [1]'}


METAL_PROPS = [('electrical conductivity', 'good', 'poor (except graphite)'), ('thermal conductivity', 'good', 'poor'), ('appearance', 'shiny (lustrous)', 'dull'),
               ('effect of hammering', 'malleable', 'brittle (when solid)'), ('melting point', 'usually high', 'usually low'), ('type of oxide', 'basic', 'acidic')]


@t3a.add('C2', (2, 3, 4), 'explain')
def t3a_classify(r, D):
    pr = r.sample(METAL_PROPS, 3)
    metal = r.random() < 0.5
    desc = '; '.join(f'{p[0]}: {p[1] if metal else p[2]}' for p in pr)
    return {'stem': f'An unknown element E has these properties — {desc}. Deduce whether E is a metal or a non-metal, explaining your reasoning using each property.',
            'answer': ('Metal' if metal else 'Non-metal') + ': ' + '; '.join(f'{p[1] if metal else p[2]} {p[0]} is typical of a {"metal" if metal else "non-metal"}' for p in pr) + '.',
            'key': '1 mark conclusion; 1 mark per property correctly linked, max [3]', 'marks': 3}


def _met_c4(r, D):
    ms = r.sample([x for x in MET], 3)
    tbl = '; '.join(f'{MET[m][0]}: {MET[m][3]}' for m in ms)
    p = person(r)
    intro = f'{p} adds equal-sized pieces of three metals to separate tubes of the same volume and concentration of dilute hydrochloric acid. Observations — {tbl}.'
    order = sorted(ms, key=lambda m: ['Ca', 'Mg', 'Al', 'Zn', 'Fe', 'Cu'].index(m))
    react = [m for m in ms if m != 'Cu']
    mm = r.choice(react)
    parts = [
        lambda r: ('Put the three metals in order of reactivity, most reactive first.', ' > '.join(MET[m][0] for m in order), '[2]'),
        lambda r: (f'Write the balanced symbol equation for the reaction of {MET[mm][0]} with hydrochloric acid.', E(acid_eq(mm)), '[2]'),
        lambda r: ('State two variables that must be kept the same to make this a fair test.', 'Any two: size/mass/surface area of metal; volume, concentration and temperature of acid.', '[2]'),
        lambda r: ('Describe how the gas could be collected and its volume measured.', 'Connect the tube to a gas syringe (or collect over water in an inverted measuring cylinder) and read the volume.', '[2]'),
        lambda r: ('Describe a test for the gas produced.', 'Lighted splint — squeaky pop: hydrogen.', '[2]'),
        lambda r: (('Explain why one of the metals shows no reaction.', 'Copper is below hydrogen in the reactivity series, so it cannot displace hydrogen from the acid.', '[2]') if 'Cu' in ms else
                   ('Suggest a metal that would show no reaction with the acid and explain why.', 'Copper (or silver/gold): it is below hydrogen in the reactivity series.', '[2]')),
        lambda r: (f'Predict what would be seen if {MET[mm][0]} powder were used instead of a piece.', 'Faster fizzing (larger surface area) but the same total volume of gas for the same mass.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t3a.add('C4', (2, 3, 4, 5), 'case')(_met_c4)
t3a.add('C3', (3, 4), 'case')(_met_c4)

# ---------------------------------------------------------- 3.2 alloys
ALLOYS = [('brass', 'copper and zinc', 'harder and more resistant to corrosion than pure copper', 'musical instruments, door handles and electrical plug pins', ('copper', 'zinc'), (70, 30)),
          ('bronze', 'copper and tin', 'harder and stronger than copper; resists corrosion', 'statues, medals and ship propellers', ('copper', 'tin'), (88, 12)),
          ('stainless steel', 'iron, chromium, nickel and carbon', 'hard, strong and resistant to rusting', 'cutlery, sinks, surgical instruments and chemical plant', ('iron', 'chromium'), (74, 18)),
          ('mild steel', 'iron and a small amount of carbon', 'strong and easily shaped', 'car bodies and machinery', ('iron', 'carbon'), (99.75, 0.25)),
          ('duralumin', 'aluminium, copper and magnesium', 'low density but much stronger than pure aluminium', 'aircraft bodies', ('aluminium', 'copper'), (94, 4)),
          ('solder', 'tin and lead (or tin with copper and silver)', 'low melting point', 'joining electrical components', ('tin', 'lead'), (60, 40)),
          ('cupronickel', 'copper and nickel', 'hard, hard-wearing and resistant to corrosion', 'silver-coloured coins', ('copper', 'nickel'), (75, 25))]

t3b = topic('Alloys', 'alloys as mixtures', 'why alloys are harder and stronger than pure metals', 'alloys')
t3b.fixed('C1', (1, 2), [
    ('What is an alloy?', 'A mixture of a metal with other elements', 'Alloys are mixtures (not compounds) of a metal with one or more other elements, usually metals or carbon.', ['A compound of two metals', 'A pure metal that has been heated', 'An ore of a metal']),
    ('Which metals are mixed to make brass?', 'copper and zinc', 'Brass = copper + zinc.', ['copper and tin', 'iron and chromium', 'aluminium and magnesium']),
    ('Why is stainless steel used for cutlery?', 'It is hard and resistant to rusting', 'Chromium and nickel make stainless steel resist corrosion.', ['It is soft and easily bent', 'It has a low density', 'It conducts electricity well']),
    ('Why are alloys usually harder than the pure metals they are made from?', 'Different-sized atoms disrupt the layers so they cannot slide easily', 'Atoms of different size distort the regular lattice and stop layers sliding.', ['Alloys contain stronger ionic bonds', 'Alloys have no delocalised electrons', 'The atoms in alloys are all the same size']),
    ('Which element is added to iron to make steel?', 'carbon', 'Steel is iron with carbon (and sometimes other metals).', ['sulfur', 'sodium', 'oxygen']),
    ('State one reason why alloys are used instead of pure metals.', 'Alloys are harder/stronger, or more resistant to corrosion, than the pure metal.', '[1]'),
])
t3b.fixed('C2', (2, 3, 4), [
    ('Explain why an alloy is classified as a mixture and not a compound.', 'The elements are not chemically combined in a fixed ratio; the composition can vary and the components keep their properties.', '[2]'),
    ('Explain, in terms of particles, why pure copper is soft but brass is much harder.', 'In pure copper all atoms are the same size in regular layers that slide easily; in brass the larger zinc atoms distort the layers, so they cannot slide easily.', '1 mark: pure metal layers slide; 1 mark: different-sized atoms disrupt layers [2]'),
    ('Describe the structure of an alloy as it would be shown in a diagram.', 'A regular arrangement of metal atoms with some atoms of a different size dotted among them, distorting the layers.', '[2]'),
    ('Explain why pure aluminium is not used for aircraft bodies but duralumin is.', 'Pure aluminium is too soft/weak; duralumin keeps the low density but is much stronger.', '[2]'),
    ('Explain why alloys still conduct electricity.', 'They still contain metal atoms with delocalised electrons that can move through the structure.', '[2]'),
])


@t3b.add('C1', (1, 2, 3))
def t3b_comp(r, D):
    al = r.choice(ALLOYS)
    return mcq_q(r, f'Which elements are the main components of {al[0]}?', al[1], [x[1] for x in ALLOYS], f'{al[0]}: {al[1]}; {al[2]}.')


@t3b.add('C1', (1, 2, 3))
def t3b_use(r, D):
    al = r.choice(ALLOYS)
    return mcq_q(r, f'Which alloy is most suitable for {al[3].split(",")[0].split(" and ")[0]}?', al[0], [x[0] for x in ALLOYS], f'{al[0]} is {al[2]}.')


@t3b.add('C3', (1, 2, 3, 4), 'numerical')
def t3b_pct(r, D):
    al = r.choice([a for a in ALLOYS if a[0] != 'mild steel'])
    p1 = al[5][1] + r.choice([-5, -3, 0, 2, 4]) if al[5][1] > 10 else al[5][1]
    mass = r.choice([25, 40, 50, 80, 120, 150, 200, 250, 500])
    m2 = mass * p1 / 100
    if D == 1:
        return nmcq(r, f'A {mass} g sample of {al[0]} contains {p1}% {al[4][1]} by mass. What mass of {al[4][1]} does it contain?', m2, [mass - m2, m2 * 2, m2 / 2, p1], ' g', f'{p1}/100 × {mass} = {g3(m2)} g.')
    if D >= 3:
        m1 = r.choice([3.2, 6.4, 12.8, 19.5, 26.0, 7.8])
        tot = m1 / (p1 / 100)
        return {'stem': f'Analysis of a {al[0]} object shows it contains {sf(m1)} g of {al[4][1]}, which is {p1}% of the alloy by mass. Calculate the mass of the object and the mass of the other metal(s) in it.',
                'answer': f'{g3(tot)} g; {g3(tot - m1)} g', 'key': f'total = {sf(m1)} × 100/{p1} = {g3(tot)} g [1]; other = {g3(tot)} − {sf(m1)} = {g3(tot - m1)} g [1]'}
    return {'stem': f'A {mass} g key is made of {al[0]} containing {p1}% {al[4][1]} by mass. Calculate the mass of {al[4][1]} and of the rest of the alloy.', 'answer': f'{g3(m2)} g {al[4][1]}; {g3(mass - m2)} g other',
            'key': f'{p1}/100 × {mass} = {g3(m2)} g [1]; {mass} − {g3(m2)} = {g3(mass - m2)} g [1]'}


@t3b.add('C2', (2, 3, 4), 'explain')
def t3b_why(r, D):
    al = r.choice(ALLOYS)
    pure = al[4][0]
    return {'stem': f'{al[0].capitalize()} ({al[1]}) is used for {al[3]}. Explain why {al[0]} is chosen instead of pure {pure}.',
            'answer': f'{al[0].capitalize()} is {al[2]}; pure {pure} is ' + ('softer/weaker' if 'hard' in al[2] or 'strong' in al[2] else 'less suitable') + '. The atoms of different size in the alloy stop the layers sliding.',
            'key': '1 mark: property of alloy relevant to use; 1 mark: comparison with pure metal / structural reason [2]'}


ALLOY_DATA = [('pure copper', 45, 'conducts very well'), ('brass', 120, 'conducts well'), ('pure iron', 70, 'rusts'), ('stainless steel', 200, 'does not rust'),
              ('pure aluminium', 25, 'low density'), ('duralumin', 120, 'low density'), ('pure tin', 5, 'low melting point'), ('bronze', 110, 'resists corrosion')]


def _alloy_c4(r, D):
    al = r.choice(ALLOYS)
    p1 = al[5][1]
    mass = r.choice([50, 80, 120, 200, 400])
    d = r.sample(ALLOY_DATA, 3)
    intro = r.choice([f'A manufacturer in {city(r)} makes {al[3].split(",")[0]} from {al[0]}, an alloy of {al[1]}.', f'{person(r)} is investigating why {al[0]} is used for {al[3].split(",")[0]}.',
                      f'An engineer compares {al[0]} with the pure metal {al[4][0]} for making {al[3]}.'])
    parts = [
        lambda r: ('State what is meant by an alloy.', 'A mixture of a metal with other elements.', '[1]'),
        lambda r: (f'Explain, using a description of the particles, why {al[0]} is harder than pure {al[4][0]}.', 'Atoms of different sizes distort the regular layers, so the layers cannot slide over each other easily.', '[2]'),
        lambda r: (f'A {mass} g item contains {p1}% {al[4][1]}. Calculate the mass of {al[4][1]}.', f'{g3(mass * p1 / 100)} g', '[1]'),
        lambda r: (f'Suggest why {al[0]} is suitable for {al[3].split(",")[0]}.', cap(al[2]) + '.', '[2]'),
        lambda r: ('Hardness values (arbitrary units): ' + '; '.join(f'{x[0]} {x[1]}' for x in d) + '. Which material is hardest and what does this suggest about alloys compared with pure metals?',
                   f'{max(d, key=lambda x: x[1])[0]}; alloys are generally harder than the pure metals they contain.', '[2]'),
        lambda r: ('Explain why an alloy has no fixed melting point, unlike a pure metal.', 'It is a mixture whose composition can vary, so it melts over a range of temperatures.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t3b.add('C4', (2, 3, 4, 5), 'multi_step')(_alloy_c4)
t3b.add('C3', (3, 4), 'multi_step')(_alloy_c4)

# ---------------------------------------------------------- 3.3 uses
USES_M = [('aluminium', 'manufacture of aircraft', 'low density and strong (when alloyed)'), ('aluminium', 'food containers and drinks cans', 'resistance to corrosion and non-toxic'),
          ('aluminium', 'overhead power cables', 'low density and good electrical conductivity'), ('copper', 'electrical wiring', 'good electrical conductivity and ductility'),
          ('copper', 'saucepan bases', 'good thermal conductivity'), ('copper', 'water pipes', 'it does not react with water and is easily bent into shape'),
          ('brass', 'musical instruments and door fittings', 'hardness, attractive colour and resistance to corrosion'),
          ('stainless steel', 'cutlery', 'hardness and resistance to rusting'), ('stainless steel', 'chemical plant', 'strength and resistance to corrosion')]

t3c = topic('Uses of metals and alloys', 'uses of metals and alloys related to their properties', 'aluminium, copper, brass and stainless steel', 'uses of metals')
t3c.fixed('C1', (1, 2), [
    ('Why is aluminium used for overhead power cables rather than copper?', 'It has a lower density and is a good conductor', 'Al: low density so pylons can be further apart; it still conducts well (often with a steel core for strength).', ['It conducts better than copper', 'It is magnetic', 'It has a higher density']),
    ('Which property of copper makes it suitable for electrical wiring?', 'It is a good conductor of electricity and is ductile', 'Wires need high conductivity and ductility.', ['It has a low density', 'It is brittle', 'It reacts with water']),
    ('Why is aluminium used for food containers?', 'It resists corrosion', 'A thin oxide layer protects it; it is also non-toxic.', ['It reacts with acids in food', 'It is very dense', 'It is magnetic']),
    ('Which material is used for cutlery because it does not rust?', 'stainless steel', 'Chromium and nickel stop the iron rusting.', ['mild steel', 'pure iron', 'cast iron']),
    ('Give one use of brass.', 'Musical instruments, door handles, electrical plug pins or ornaments.', '[1]'),
])
t3c.fixed('C2', (2, 3, 4), [
    ('Explain why aluminium is used for aircraft even though steel is stronger.', 'Aluminium (alloy) has a much lower density, so the aircraft is lighter and uses less fuel, while still being strong enough; it also resists corrosion.', '[2]'),
    ('Explain why aluminium resists corrosion even though it is a reactive metal.', 'It is covered by a thin, unreactive layer of aluminium oxide that prevents air and water reaching the metal.', '[2]'),
    ('Explain why copper is used for water pipes but iron is not.', 'Copper does not react with water (it is unreactive), whereas iron rusts in water and air.', '[2]'),
    ('Overhead cables have a steel core surrounded by aluminium. Explain the purpose of each metal.', 'Steel provides strength to support the cable; aluminium conducts the electricity and has a low density.', '[2]'),
])


@t3c.add('C1', (1, 2, 3))
def t3c_prop(r, D):
    m, use, prop = r.choice(USES_M)
    return mcq_q(r, f'{cap(m)} is used for {use}. Which property makes it suitable?', prop, [x[2] for x in USES_M], f'{m} — {use}: {prop}.')


@t3c.add('C2', (2, 3, 4), 'explain')
def t3c_explain(r, D):
    m, use, prop = r.choice(USES_M)
    return {'stem': f'Explain why {m} is used for {use}.', 'answer': f'Because of its {prop}.' if not prop.startswith('it') else f'Because {prop}.',
            'key': '1 mark property; 1 mark linked to the use [2]'}


MDATA = [('aluminium', 2.70, 38, 'good', 'resists corrosion', 2.4), ('copper', 8.96, 60, 'very good', 'resists corrosion', 8.5), ('iron', 7.87, 10, 'moderate', 'rusts', 0.5),
         ('stainless steel', 8.00, 1.4, 'poor', 'does not rust', 3.0), ('brass', 8.50, 16, 'good', 'resists corrosion', 6.0), ('zinc', 7.14, 17, 'moderate', 'corrodes slowly', 2.8)]


@t3c.add('C3', (2, 3, 4))
def t3c_choose(r, D):
    rows = r.sample(MDATA, 4)
    need = r.choice([('overhead power cables', lambda x: x[2] / x[1], 'high conductivity for its density'), ('the hull of a lightweight boat', lambda x: (x[4] != 'rusts') / x[1], 'low density and corrosion resistance'),
                     ('kitchen sinks', lambda x: (x[4] == 'does not rust') * 10 + (x[4] != 'rusts'), 'no rusting'), ('electrical wiring', lambda x: x[2], 'highest electrical conductivity')])
    best = max(rows, key=need[1])
    tbl = '; '.join(f'{x[0]}: density {x[1]} g/cm³, conductivity {x[2]} MS/m, corrosion — {x[4]}, cost ${x[5]}/kg' for x in rows)
    return {'stem': f'Use the data to choose the most suitable material for {need[0]} and justify your choice. {tbl}.', 'answer': f'{best[0]}: {need[2]}.',
            'key': f'1 mark choice ({best[0]}); 1 mark justification using data ({need[2]}); 1 mark comparison with another material [3]', 'marks': 3}


def _use_c4(r, D):
    m, use, prop = r.choice(USES_M)
    rows = [MDATA[0]] + r.sample([x for x in MDATA[1:] if x[0] != 'stainless steel'], 2)
    r.shuffle(rows)
    intro = r.choice([f'A company in {city(r)} is choosing a metal for {use}.', f'{person(r)} writes a report on why {m} is used for {use}.', f'Engineers are reviewing the materials used for {use} in a new factory.'])
    parts = [
        lambda r: (f'State the property of {m} that makes it suitable for {use}.', prop, '[1]'),
        lambda r: (f'Explain how this property relates to the structure of {m}.', 'Metallic structure: delocalised electrons give conductivity; layers of ions give malleability/ductility; oxide layer or alloying gives corrosion resistance.', '[2]'),
        lambda r: ('Data: ' + '; '.join(f'{x[0]} density {x[1]} g/cm³, corrosion — {x[4]}' for x in rows) + '. Identify the least dense metal and suggest one use that benefits from its low density.', f'{min(rows, key=lambda x: x[1])[0]}; e.g. aircraft bodies or vehicle parts, to reduce mass (it also resists corrosion).', '[2]'),
        lambda r: ('Suggest one disadvantage of using pure iron for an outdoor structure and how steel overcomes it.', 'Iron rusts and is soft; stainless steel resists rusting and is harder (or mild steel is stronger and can be painted).', '[2]'),
        lambda r: ('Other than physical properties, suggest one factor that affects the choice of metal.', 'Cost, availability, ease of recycling, appearance or toxicity.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t3c.add('C4', (2, 3, 4, 5), 'multi_step')(_use_c4)
t3c.add('C3', (3, 4), 'multi_step')(_use_c4)

CHAPTERS[3] = [t3a, t3b, t3c]


# ===================================================================== Ch4 (CB15) Reactivity of metals
SERIES = ['potassium', 'sodium', 'calcium', 'magnesium', 'aluminium', 'carbon', 'zinc', 'iron', 'hydrogen', 'copper', 'silver', 'gold']
RS = [x for x in SERIES if x not in ('carbon', 'hydrogen')]
SYM = {'potassium': 'K', 'sodium': 'Na', 'calcium': 'Ca', 'magnesium': 'Mg', 'aluminium': 'Al', 'zinc': 'Zn', 'iron': 'Fe', 'copper': 'Cu', 'silver': 'Ag', 'gold': 'Au', 'lead': 'Pb'}
WATER = {  # cold water, steam, dilute HCl
    'potassium': ('reacts very vigorously; the hydrogen ignites with a lilac flame', 'explosive — not attempted', 'explosive — not attempted'),
    'sodium': ('reacts vigorously, fizzing and moving around on the surface', 'explosive — not attempted', 'explosive — not attempted'),
    'calcium': ('fizzes steadily; the water turns cloudy as calcium hydroxide forms', 'reacts violently', 'reacts very vigorously'),
    'magnesium': ('reacts very slowly; a few bubbles over several days', 'burns with a bright white light forming white magnesium oxide and hydrogen', 'reacts vigorously with rapid fizzing'),
    'zinc': ('no reaction', 'reacts when heated, forming zinc oxide and hydrogen', 'reacts steadily with fizzing'),
    'iron': ('no reaction (rusts very slowly)', 'reacts slowly when red hot', 'reacts slowly with a few bubbles'),
    'copper': ('no reaction', 'no reaction', 'no reaction'),
    'silver': ('no reaction', 'no reaction', 'no reaction'),
    'gold': ('no reaction', 'no reaction', 'no reaction'),
}
WEQ = {'potassium': '2K + 2H2O -> 2KOH + H2', 'sodium': '2Na + 2H2O -> 2NaOH + H2', 'calcium': 'Ca + 2H2O -> Ca(OH)2 + H2', 'magnesium': 'Mg + H2O -> MgO + H2', 'zinc': 'Zn + H2O -> ZnO + H2'}
HEQ = {'magnesium': 'Mg + 2HCl -> MgCl2 + H2', 'zinc': 'Zn + 2HCl -> ZnCl2 + H2', 'iron': 'Fe + 2HCl -> FeCl2 + H2', 'calcium': 'Ca + 2HCl -> CaCl2 + H2', 'aluminium': '2Al + 6HCl -> 2AlCl3 + 3H2'}

t4a = topic('The reactivity series', 'the reactivity series', 'reactions of metals with cold water, steam and dilute hydrochloric acid', 'reactivity series')
t4a.fixed('C1', (1, 2), [
    ('Which metal reacts with cold water to form an alkaline solution and hydrogen?', 'calcium', 'K, Na and Ca react with cold water: Ca + 2H₂O → Ca(OH)₂ + H₂.', ['copper', 'zinc', 'iron']),
    ('Which products form when magnesium reacts with steam?', 'magnesium oxide and hydrogen', 'Mg + H₂O(g) → MgO + H₂.', ['magnesium hydroxide and hydrogen', 'magnesium oxide and oxygen', 'magnesium hydroxide and oxygen']),
    ('Which list is in order of decreasing reactivity?', 'sodium, magnesium, zinc, copper', 'Reactivity series: K > Na > Ca > Mg > Al > (C) > Zn > Fe > (H) > Cu > Ag > Au.', ['copper, zinc, magnesium, sodium', 'magnesium, sodium, copper, zinc', 'zinc, sodium, copper, magnesium']),
    ('Which metal does not react with dilute hydrochloric acid?', 'silver', 'Metals below hydrogen (Cu, Ag, Au) do not react with dilute acids.', ['zinc', 'magnesium', 'iron']),
    ('The position of hydrogen in the reactivity series shows that', 'metals above it can displace hydrogen from dilute acids', 'Metals more reactive than hydrogen react with dilute acids to give H₂.', ['metals below it react with water', 'it is a metal', 'all metals react with acids']),
    ('State the order of reactivity of copper, iron and magnesium, most reactive first.', 'magnesium > iron > copper', '[1]'),
])
t4a.fixed('C2', (2, 3, 4), [
    ('Explain why magnesium reacts very slowly with cold water but vigorously with steam.', 'Steam particles have more energy (higher temperature), so more collisions have enough energy to react; also steam gives magnesium oxide on a hot surface.', '[2]'),
    ('Explain why potassium and dilute hydrochloric acid are never reacted in a school laboratory.', 'Potassium is so reactive that the reaction would be explosive.', '[1]'),
    ('Describe how you could use dilute hydrochloric acid to put zinc, iron and magnesium into a reactivity order.', 'Add equal-sized pieces to equal volumes of the same acid at the same temperature; compare the rate of bubbling (or gas volume in a set time); faster = more reactive.', '1 mark fair test; 1 mark rate observation [2]'),
    ('Explain why the reaction of calcium with water makes the water turn cloudy.', 'Calcium hydroxide is formed, which is only slightly soluble, so some appears as a white solid.', '[2]'),
    ('A student says, "Aluminium must be less reactive than iron because aluminium saucepans do not corrode." Explain why the student is wrong.', 'Aluminium is more reactive than iron, but it is protected by a thin, unreactive oxide layer.', '[2]'),
])


@t4a.add('C1', (1, 2, 3))
def t4a_obs(r, D):
    m = r.choice(['potassium', 'sodium', 'calcium', 'magnesium', 'zinc', 'copper'])
    cond = r.choice([0, 1, 2]) if m in ('magnesium', 'zinc', 'copper') else 0
    cname = ['cold water', 'steam', 'dilute hydrochloric acid'][cond]
    corr = WATER[m][cond]
    pool = list({WATER[x][c] for x in WATER for c in range(3)} - {corr, 'explosive — not attempted', 'reacts violently'})
    return mcq_q(r, f'Which observation is expected when {m} is added to {cname}?', corr, pool, f'{m} with {cname}: {corr}.')


@t4a.add('C3', (1, 2, 3, 4))
def t4a_eq(r, D):
    m = r.choice(list(WEQ) + list(HEQ))
    eq = WEQ.get(m) if (m in WEQ and (m not in HEQ or r.random() < 0.5)) else HEQ[m]
    what = 'dilute hydrochloric acid' if 'HCl' in eq else ('steam' if m in ('magnesium', 'zinc') else 'cold water')
    if D == 1:
        prods = eq.split('->')[1].strip()
        return mcq_q(r, f'What are the products when {m} reacts with {what}?', E(prods), [E(x) for x in ('MgO + H2', 'MgCl2 + H2', 'NaOH + H2', 'Ca(OH)2 + H2', 'ZnO + H2', 'FeCl2 + H2', 'KOH + H2', 'CaO + H2', 'MgCl2 + H2O', 'Mg(OH)2 + O2', '2AlCl3 + 3H2', '2KOH + H2', '2NaOH + H2', 'CaCl2 + H2')], E(eq))
    return {'stem': f'Write a balanced symbol equation, with state symbols, for the reaction of {m} with {what}.' if D >= 3 else f'Write a balanced symbol equation for the reaction of {m} with {what}.',
            'answer': E(eq), 'key': f'{E(eq)}: formulae [1]; balancing [1]' + ('; state symbols [1]' if D >= 3 else ''), 'marks': 3 if D >= 3 else 2}


LETTERS4 = 'PQRS'


def _unknown_metals(r, k=4):
    ms = r.sample(['potassium', 'sodium', 'calcium', 'magnesium', 'zinc', 'iron', 'copper', 'silver'], k)
    lab_ = dict(zip(LETTERS4, ms))
    return lab_


def _obs_row(m):
    w, s, h = WATER[m]
    return f'cold water — {w}; dilute acid — {h if "attempted" not in h else "too dangerous to test"}'


@t4a.add('C3', (2, 3, 4, 5))
def t4a_deduce(r, D):
    lab_ = _unknown_metals(r, 3 if D <= 3 else 4)
    rows = '; '.join(f'{L}: {_obs_row(m)}' for L, m in lab_.items())
    order = sorted(lab_, key=lambda L: RS.index(lab_[L]))
    ties = any(_obs_row(lab_[a]) == _obs_row(lab_[b]) for a in lab_ for b in lab_ if a < b)
    if ties:
        return None
    return {'stem': f'A student tests metals {", ".join(lab_)} with cold water and with dilute hydrochloric acid. {rows}. Deduce the order of reactivity of the metals, most reactive first, and suggest the identity of {order[0]}.',
            'answer': ' > '.join(order) + f'; {order[0]} could be {lab_[order[0]]}.', 'key': f'Order {" > ".join(order)} [2]; identity consistent with observations [1]', 'marks': 3}



def _cuso4_pred(m):
    if m in ('potassium', 'sodium', 'calcium'):
        return 'It reacts with the water first: fizzing (hydrogen) and an alkaline hydroxide forms, giving a blue precipitate of copper(II) hydroxide; copper metal is not displaced.'
    if RS.index(m) < RS.index('copper'):
        return 'A brown (pink-brown) solid of copper forms and the blue colour fades: the metal is more reactive than copper, so it displaces it.'
    return 'No reaction: the metal is not more reactive than copper, so it cannot displace it.'

def _rs_c4(r, D):
    lab_ = _unknown_metals(r, 4)
    ms = list(lab_.items())
    rows = '; '.join(f'{L}: {_obs_row(m)}' for L, m in ms)
    if any(_obs_row(a[1]) == _obs_row(b[1]) for a in ms for b in ms if a[0] < b[0]):
        return None
    order = sorted(lab_, key=lambda L: RS.index(lab_[L]))
    rx = [L for L, m in ms if m in HEQ]
    intro = f'{person(r)} investigates four metals, labelled {", ".join(lab_)}. Results — {rows}.'
    parts = [
        lambda r: ('Put the metals in order of reactivity, most reactive first.', ' > '.join(order), '[2]'),
        lambda r: ('Which metal(s) are below hydrogen in the reactivity series? Explain.', ((', '.join(L for L, m in ms if RS.index(m) > RS.index('iron')) + ': they do not react with dilute acid.') if any(RS.index(m) > RS.index('iron') for L, m in ms) else 'None: every metal reacts with dilute acid (or water), so all are above hydrogen.'), '[2]'),
        lambda r: ((f'{rx[0]} is {lab_[rx[0]]}. Write the equation for its reaction with hydrochloric acid.', E(HEQ[lab_[rx[0]]]), '[2]') if rx else None),
        lambda r: (f'Suggest how {order[-1]} could be tested with steam and what result you would expect.', ('Heat the metal strongly in a tube while passing steam over it; no reaction expected.' if lab_[order[-1]] in ('copper', 'silver') else 'Heat in steam; it reacts slowly to form an oxide and hydrogen.'), '[2]'),
        lambda r: (f'Predict what would happen if {order[0]} were added to a solution of copper(II) sulfate. Explain.', _cuso4_pred(lab_[order[0]]), '[2]'),
        lambda r: ('Name the gas produced when metals react with dilute acids and give a test for it.', 'Hydrogen — lighted splint gives a squeaky pop.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t4a.add('C4', (2, 3, 4, 5), 'case')(_rs_c4)
t4a.add('C3', (3, 4), 'case')(_rs_c4)

# ---------------------------------------------------------- 4.2 displacement
DSALT = {'copper': ('copper(II) sulfate', 'CuSO4', 'Cu', 2, 'blue', 'a pink-brown solid forms and the blue colour fades'),
         'iron': ('iron(II) sulfate', 'FeSO4', 'Fe', 2, 'pale green', 'a dark grey solid forms and the pale green colour fades'),
         'zinc': ('zinc sulfate', 'ZnSO4', 'Zn', 2, 'colourless', 'a grey solid forms on the metal'),
         'silver': ('silver nitrate', 'AgNO3', 'Ag', 1, 'colourless', 'shiny grey/silver crystals form on the metal'),
         'magnesium': ('magnesium sulfate', 'MgSO4', 'Mg', 2, 'colourless', 'no displacement expected'),
         'lead': ('lead(II) nitrate', 'Pb(NO3)2', 'Pb', 2, 'colourless', 'a grey solid forms on the metal')}
DMET = ['magnesium', 'zinc', 'iron', 'lead', 'copper', 'silver']
RANK = {'magnesium': 0, 'aluminium': 0.5, 'zinc': 1, 'iron': 2, 'lead': 3, 'copper': 4, 'silver': 5}
SYM['lead'] = 'Pb'


def disp_eq(m, s):
    """metal m added to solution of metal s salt."""
    if RANK[m] >= RANK[s]:
        return None
    name, f, ss, q, col, obs = DSALT[s]
    M = SYM[m]
    if q == 1:  # silver nitrate
        prod = f'{M}(NO3)2'
        return f'{M} + 2AgNO3 -> {prod} + 2Ag', f'{M} + 2Ag^+ -> {M}^2+ + 2Ag'
    anion = 'SO4' if 'SO4' in f else '(NO3)2'
    prod = f'{M}SO4' if anion == 'SO4' else f'{M}(NO3)2'
    return f'{M} + {f} -> {prod} + {ss}', f'{M} + {ss}^2+ -> {M}^2+ + {ss}'


DSPAIRS = [(m, s) for m in DMET for s in ('copper', 'iron', 'zinc', 'silver', 'magnesium', 'lead') if m != s and not (m == 'lead' and 'SO4' in DSALT[s][1])]

t4b = topic('Displacement reactions', 'displacement reactions of metals with aqueous ions and metal oxides', 'displacement reactions', 'metal oxides')
t4b.fixed('C1', (1, 2), [
    ('Which mixture reacts?', 'zinc and copper(II) sulfate solution', 'A more reactive metal displaces a less reactive metal from its compounds: Zn + CuSO₄ → ZnSO₄ + Cu.', ['copper and zinc sulfate solution', 'silver and copper(II) sulfate solution', 'copper and magnesium sulfate solution']),
    ('What is seen when an iron nail is left in copper(II) sulfate solution?', 'A brown coating forms on the nail and the blue colour fades', 'Fe + CuSO₄ → FeSO₄ + Cu: copper deposits; solution becomes pale green.', ['The nail dissolves completely and the solution turns colourless', 'Bubbles of hydrogen form and the solution turns blue', 'Nothing happens']),
    ('Which mixture of powders reacts when heated?', 'aluminium and iron(III) oxide', 'Thermite: 2Al + Fe₂O₃ → Al₂O₃ + 2Fe; aluminium is more reactive than iron.', ['iron and aluminium oxide', 'copper and magnesium oxide', 'copper and zinc oxide']),
    ('In the reaction Mg + CuO → MgO + Cu, which substance is reduced?', 'copper(II) oxide', 'CuO loses oxygen (Cu²⁺ gains electrons) — it is reduced; Mg is oxidised.', ['magnesium', 'magnesium oxide', 'copper']),
    ('State the general rule used to predict whether a displacement reaction will happen.', 'A more reactive metal displaces a less reactive metal from its compounds (solution or oxide).', '[1]'),
])
t4b.fixed('C2', (2, 3, 4), [
    ('Explain why copper does not react with zinc sulfate solution.', 'Copper is less reactive than zinc, so it cannot displace zinc from its compound.', '[2]'),
    ('Explain why the thermite reaction is used to weld railway lines.', 'It is very exothermic; the iron produced is molten and fills the gap between the rails.', '[2]'),
    ('Explain why the displacement of copper by magnesium is a redox reaction.', 'Magnesium atoms lose electrons (oxidised) to form Mg²⁺; copper(II) ions gain electrons (reduced) to form copper atoms.', '1 mark each [2]'),
    ('Explain why the temperature rise is larger when magnesium, rather than iron, is added to copper(II) sulfate solution.', 'Magnesium is further above copper in the reactivity series, so the reaction releases more energy.', '[2]'),
    ('Explain why the sulfate ions are described as spectator ions in Zn + CuSO₄ → ZnSO₄ + Cu.', 'They are present in solution before and after the reaction and are not changed.', '[1]'),
])


@t4b.add('C1', (1, 2, 3))
def t4b_will(r, D):
    m, s = r.choice([x for x in DSPAIRS if RANK[x[0]] < RANK[x[1]]])
    corr = f'{m} and {DSALT[s][0]} solution'
    wrong = [f'{a} and {DSALT[b][0]} solution' for a, b in DSPAIRS if RANK[a] >= RANK[b]]
    return mcq_q(r, 'Which mixture would produce a displacement reaction?', corr, wrong, f'{m} is more reactive than {s}: {E(disp_eq(m, s)[0])}.')


@t4b.add('C3', (1, 2, 3, 4))
def t4b_pred(r, D):
    m, s = r.choice(DSPAIRS)
    sol = DSALT[s]
    res = disp_eq(m, s)
    if D == 1:
        corr = sol[5] if res else 'no visible change'
        return mcq_q(r, f'A piece of {m} is placed in {sol[0]} solution. What is seen?', corr, [x[5] for x in DSALT.values() if x[5] != 'no displacement expected'] + ['no visible change', 'bubbles of hydrogen are given off'],
                     (E(res[0]) if res else f'{m} is less reactive than {s}: no reaction.'))
    if not res:
        return {'stem': f'Predict whether {m} reacts with aqueous {sol[0]}. Explain your answer.', 'answer': f'No reaction: {m} is less reactive than {s}, so it cannot displace it.', 'key': '1 mark prediction; 1 mark reason [2]'}
    st = D >= 3
    return {'stem': f'A piece of {m} is placed in aqueous {sol[0]}. Describe what you would see and write the balanced equation' + (' and the ionic equation.' if st else '.'),
            'answer': f'{cap(sol[5])}. {E(res[0])}' + (f'; ionic: {E(res[1])}' if st else ''), 'key': '1 mark observation; 1 mark equation' + ('; 1 mark ionic equation [3]' if st else ' [2]'), 'marks': 3 if st else 2}


OXD = [('Al', 'Fe2O3', '2Al + Fe2O3 -> Al2O3 + 2Fe', 'aluminium', 'iron(III) oxide', 'Fe', 2), ('Mg', 'CuO', 'Mg + CuO -> MgO + Cu', 'magnesium', 'copper(II) oxide', 'Cu', 1),
       ('Zn', 'CuO', 'Zn + CuO -> ZnO + Cu', 'zinc', 'copper(II) oxide', 'Cu', 1), ('Mg', 'ZnO', 'Mg + ZnO -> MgO + Zn', 'magnesium', 'zinc oxide', 'Zn', 1),
       ('Fe', 'CuO', 'Fe + CuO -> FeO + Cu', 'iron', 'copper(II) oxide', 'Cu', 1), ('Mg', 'PbO', 'Mg + PbO -> MgO + Pb', 'magnesium', 'lead(II) oxide', 'Pb', 1),
       ('Al', 'Cr2O3', '2Al + Cr2O3 -> Al2O3 + 2Cr', 'aluminium', 'chromium(III) oxide', 'Cr', 2)]


@t4b.add('C3', (2, 3, 4, 5), 'numerical')
def t4b_mass(r, D):
    if r.random() < 0.5:
        M, ox, eq, mn, on, prod, k = r.choice(OXD)
        mass = r.choice([2.0, 4.0, 8.0, 16.0, 1.6, 3.2, 5.0, 10.0])
        no = mass / Mr(ox)
        mp = no * k * AR[prod]
        return {'stem': f'{sf(mass)} g of {on} is heated with excess {mn} powder. {E(eq)}. Calculate the mass of {SYM_NAME.get(prod, prod)} produced' + (' and identify the oxidising agent.' if D >= 4 else '.'),
                'answer': f'{g3(mp)} g' + (f'; {on} is the oxidising agent' if D >= 4 else ''), 'key': f'n({F(ox)}) = {sf(mass)}/{mr(Mr(ox))} = {g3(no)} mol [1]; n({prod}) = {g3(no * k)} mol [1]; mass = {g3(mp)} g [1]' + ('; oxidising agent [1]' if D >= 4 else '')}
    m, s = r.choice([x for x in DSPAIRS if RANK[x[0]] < RANK[x[1]] and x[1] in ('copper', 'silver')])
    eq, ion = disp_eq(m, s)
    mass = r.choice([2.07, 4.14, 1.035]) if m == 'lead' else r.choice([0.64, 1.28, 3.20])
    if m == 'zinc':
        mass = r.choice([0.65, 1.30, 1.95])
    elif m == 'iron':
        mass = r.choice([0.56, 1.12, 2.80])
    elif m == 'magnesium':
        mass = r.choice([0.24, 0.48, 1.20])
    nmol = mass / AR[SYM[m]]
    k = 2 if s == 'silver' else 1
    mp = nmol * k * AR[SYM[s]]
    return {'stem': f'{sf(mass)} g of {m} powder is added to excess {DSALT[s][0]} solution. {E(eq)}. Calculate the mass of {s} that is displaced.',
            'answer': f'{g3(mp)} g', 'key': f'n({SYM[m]}) = {sf(mass)}/{AR[SYM[m]]} = {g3(nmol)} mol [1]; n({SYM[s]}) = {g3(nmol * k)} mol [1]; mass = {g3(nmol * k)} × {AR[SYM[s]]} = {g3(mp)} g [1]'}


SYM_NAME = {'Fe': 'iron', 'Cu': 'copper', 'Zn': 'zinc', 'Pb': 'lead', 'Cr': 'chromium'}
TRISE = {'magnesium': (38, 45), 'zinc': (12, 16), 'iron': (6, 9), 'lead': (2, 4), 'copper': (0, 0), 'silver': (0, 0)}


def _disp_c4(r, D):
    ms = r.sample(['magnesium', 'zinc', 'iron', 'copper', 'silver'], 4)
    T0 = r.choice([19.5, 20.0, 21.0, 22.5, 18.0])
    rise = {m: r.randint(*TRISE[m]) for m in ms}
    tbl = '; '.join(f'{m}: start {T0:.1f} °C, highest {T0 + rise[m]:.1f} °C' for m in ms)
    order = sorted(ms, key=lambda m: -rise[m])
    top = order[0]
    eq = disp_eq(top, 'copper')
    intro = f'{person(r)} adds 1.0 g of each metal powder to 25 cm³ of 1.0 mol/dm³ copper(II) sulfate solution in a polystyrene cup and records the temperature. Results — {tbl}.'
    parts = [
        lambda r: ('Calculate the temperature rise for each metal.', '; '.join(f'{m} {rise[m]} °C' for m in ms), '[2]'),
        lambda r: ('Use the results to put the metals in order of reactivity, most reactive first.', ' > '.join(order), '[2]'),
        lambda r: (f'Write the ionic equation for the reaction of {top} with copper(II) ions.', E(eq[1]), '[2]'),
        lambda r: ('Explain why a polystyrene cup is used.', 'It is a good insulator, so less heat is lost to the surroundings.', '[1]'),
        lambda r: ('State two variables that must be controlled.', 'Mass/particle size of metal; volume, concentration and starting temperature of copper(II) sulfate.', '[2]'),
        lambda r: (('Explain why silver gives no temperature rise.', 'Silver is less reactive than copper, so no displacement occurs.', '[2]') if 'silver' in ms else
                   ('Predict the temperature rise if copper powder were used, and explain.', '0 °C: copper cannot displace itself; no reaction.', '[2]')),
        lambda r: (f'State what is seen in the cup containing {top}.', 'Pink-brown solid forms; blue colour fades; the mixture gets hot.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t4b.add('C4', (2, 3, 4, 5), 'case')(_disp_c4)
t4b.add('C3', (3, 4), 'case')(_disp_c4)

# ---------------------------------------------------------- 4.3 explaining reactivity
t4c = topic('Explaining reactivity', 'explaining reactivity as the tendency of a metal to form positive ions', 'apparent unreactivity of aluminium', 'positive ions')
t4c.fixed('C1', (1, 2), [
    ('The reactivity of a metal depends on', 'how easily its atoms lose electrons to form positive ions', 'More reactive metals form positive ions more readily.', ['how easily its atoms gain electrons', 'the size of its nucleus only', 'its density']),
    ('Why does aluminium appear less reactive than its position in the reactivity series suggests?', 'It is coated with a thin, unreactive layer of aluminium oxide', 'The Al₂O₃ layer stops water and acids reaching the metal.', ['It has a very high density', 'It has no outer electrons', 'It forms negative ions']),
    ('Which half-equation shows the oxidation of zinc?', 'Zn → Zn²⁺ + 2e⁻', 'Oxidation is loss of electrons.', ['Zn²⁺ + 2e⁻ → Zn', 'Zn + 2e⁻ → Zn²⁻', 'Zn²⁺ → Zn + 2e⁻']),
    ('In a displacement reaction, the more reactive metal', 'is oxidised', 'It loses electrons to form positive ions.', ['is reduced', 'gains electrons', 'is unchanged']),
    ('Define oxidation in terms of electrons.', 'Oxidation is the loss of electrons.', '[1]'),
    ('Define reduction in terms of electrons.', 'Reduction is the gain of electrons.', '[1]'),
])
t4c.fixed('C2', (2, 3, 4), [
    ('Explain why potassium is more reactive than sodium in terms of electron loss.', 'Potassium’s outer electron is further from the nucleus (more shells, more shielding), so it is lost more easily to form K⁺.', '[2]'),
    ('Explain how the oxide layer on aluminium can be made thicker, and why this is useful.', 'By anodising (electrolysis with aluminium as the anode); the thicker oxide layer gives even better protection against corrosion and can be dyed.', '[2]'),
    ('Explain, in terms of electrons, why magnesium displaces copper from copper(II) sulfate solution.', 'Magnesium has a greater tendency to lose electrons; Mg atoms give electrons to Cu²⁺ ions, forming Mg²⁺ and Cu atoms.', '[2]'),
    ('Explain why aluminium powder reacts quickly with acid while aluminium foil reacts slowly at first.', 'Powder has a larger surface area, and the oxide layer on foil must first be removed before the metal reacts.', '[2]'),
    ('Explain why gold is found uncombined in the Earth’s crust.', 'Gold has very little tendency to form positive ions, so it does not react with oxygen, water or acids.', '[2]'),
])

HALF = [('magnesium', 'Mg', 2), ('zinc', 'Zn', 2), ('iron', 'Fe', 2), ('copper', 'Cu', 2), ('aluminium', 'Al', 3), ('sodium', 'Na', 1), ('calcium', 'Ca', 2), ('silver', 'Ag', 1), ('potassium', 'K', 1)]


@t4c.add('C3', (1, 2, 3))
def t4c_half(r, D):
    nm, s, q = r.choice(HALF)
    ion = F(f'{s}^{q if q > 1 else ""}+')
    ox = f'{s} → {ion} + {q if q > 1 else ""}e⁻'
    red = f'{ion} + {q if q > 1 else ""}e⁻ → {s}'
    want = r.choice(['oxidation', 'reduction'])
    corr = ox if want == 'oxidation' else red
    pool = [ox, red, f'{s} + {q if q > 1 else ""}e⁻ → {ion}', f'{ion} → {s} + {q if q > 1 else ""}e⁻', f'{s} → {s}{"⁻" if q == 1 else str(q).translate(_SUP) + "⁻"} + {q if q > 1 else ""}e⁻']
    if D == 1:
        return mcq_q(r, f'Which half-equation shows the {want} of {"" if want == "oxidation" else nm + " ions to "}{nm if want == "oxidation" else "atoms"}?'.replace('of  ', 'of '), corr, pool, f'{want}: {"loss" if want == "oxidation" else "gain"} of electrons; {corr}.')
    return {'stem': f'Write the half-equation for {nm} atoms forming {nm} ions, and state whether this is oxidation or reduction.', 'answer': f'{ox}; oxidation (loss of electrons).', 'key': '1 mark half-equation; 1 mark oxidation with reason [2]'}


@t4c.add('C2', (2, 3, 4), 'explain')
def t4c_redox(r, D):
    m, s = r.choice([x for x in DSPAIRS if RANK[x[0]] < RANK[x[1]]])
    eq, ion = disp_eq(m, s)
    return {'stem': f'{E(ion)}. Use ideas about electron transfer to explain which species is oxidised and which is reduced, and why this shows {m} is more reactive than {s}.',
            'answer': f'{cap(m)} atoms lose electrons (oxidised) to form ions; {s} ions gain electrons (reduced) to form atoms. {cap(m)} has the greater tendency to form positive ions, so it is more reactive.',
            'key': '1 mark oxidised species; 1 mark reduced species; 1 mark link to tendency to form positive ions [3]', 'marks': 3}


@t4c.add('C3', (2, 3, 4))
def t4c_rank(r, D):
    ms = r.sample([x for x in HALF if x[0] != 'potassium'], 3)
    srt = sorted(ms, key=lambda x: RS.index(x[0]))
    return {'stem': f'Put {", ".join(x[0] for x in ms)} in order of their tendency to form positive ions, greatest first, and write the half-equation for the ion formation of the most reactive one.',
            'answer': ' > '.join(x[0] for x in srt) + f'; {srt[0][1]} → {F(srt[0][1] + "^" + (str(srt[0][2]) if srt[0][2] > 1 else "") + "+")} + {srt[0][2] if srt[0][2] > 1 else ""}e⁻',
            'key': '1 mark order (same as reactivity series); 1 mark half-equation [2]'}


def _al_c4(r, D):
    intro = r.choice([f'{person(r)} notices that aluminium window frames in {city(r)} have lasted for decades without corroding, even though aluminium is high in the reactivity series.',
                      'A drinks company uses aluminium cans, even though aluminium is more reactive than iron.',
                      f'In {lab(r)}, a piece of aluminium foil is placed in dilute hydrochloric acid. For several minutes nothing happens, then the foil starts to fizz steadily.'])
    parts = [
        lambda r: ('Explain why aluminium seems unreactive.', 'It is covered by a thin, tough layer of aluminium oxide that stops oxygen and water reaching the metal.', '[2]'),
        lambda r: ('Explain why the foil in acid reacts only after a delay.', 'The acid must first react with/remove the oxide layer; then the metal is exposed and reacts.', '[2]'),
        lambda r: ('Write the balanced equation for aluminium reacting with hydrochloric acid.', E('2Al + 6HCl -> 2AlCl3 + 3H2'), '[2]'),
        lambda r: ('Write the half-equation for the formation of aluminium ions.', 'Al → Al³⁺ + 3e⁻', '[1]'),
        lambda r: ('State whether aluminium is oxidised or reduced when it forms ions, giving a reason.', 'Oxidised: it loses electrons.', '[1]'),
        lambda r: ('Suggest why aluminium is placed above zinc in the reactivity series even though it often reacts more slowly.', 'Once the oxide layer is removed, aluminium loses electrons more readily than zinc; its position reflects its tendency to form positive ions.', '[2]'),
        lambda r: ('Write the equation for the formation of the oxide layer.', E('4Al + 3O2 -> 2Al2O3'), '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t4c.add('C4', (2, 3, 4, 5), 'multi_step')(_al_c4)
t4c.add('C3', (3, 4), 'multi_step')(_al_c4)


def _rx_c4(r, D):
    m, s = r.choice([x for x in DSPAIRS if RANK[x[0]] < RANK[x[1]]])
    eq, ion = disp_eq(m, s)
    intro = f'{person(r)} places a strip of {m} into aqueous {DSALT[s][0]}. {E(eq)}.'
    q = dict((h[0], h[2]) for h in HALF)
    ss = dict((h[0], h[1]) for h in HALF)
    parts = [
        lambda r: ('Describe what would be seen.', cap(DSALT[s][5]) + '.', '[2]'),
        lambda r: ('Write the ionic equation.', E(ion), '[2]'),
        lambda r: (f'Write the half-equation for the change to the {m} atoms.', f'{SYM[m]} → {F(SYM[m] + "^2+")} + 2e⁻', '[1]'),
        lambda r: (f'Explain, in terms of electrons, which substance is the reducing agent.', f'{cap(m)}: it gives (loses) electrons to the {s} ions.', '[2]'),
        lambda r: (f'Explain why the reaction would not occur if {s} were placed in a solution of {m} ions.', f'{cap(s)} is less reactive; it has less tendency to form positive ions than {m}.', '[2]'),
        lambda r: ('Name the spectator ion.', 'nitrate ion' if 'NO3' in eq else 'sulfate ion', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t4c.add('C4', (2, 3, 4, 5), 'multi_step')(_rx_c4)
t4b.add('C4', (3, 4, 5), 'multi_step')(_rx_c4)

CHAPTERS[4] = [t4a, t4b, t4c]


# ===================================================================== Ch5 (CB16) Extraction and corrosion of metals
ORES = [('zinc', 'zinc blende / zinc oxide', 'ZnO', 'ZnO + C -> Zn + CO', 'carbon', 'Zn', 1), ('lead', 'lead(II) oxide', 'PbO', '2PbO + C -> 2Pb + CO2', 'carbon', 'Pb', 2),
        ('copper', 'copper(II) oxide', 'CuO', '2CuO + C -> 2Cu + CO2', 'carbon', 'Cu', 2), ('iron', 'hematite, Fe₂O₃', 'Fe2O3', 'Fe2O3 + 3CO -> 2Fe + 3CO2', 'carbon (as carbon monoxide)', 'Fe', 2),
        ('tin', 'tin(IV) oxide', 'SnO2', 'SnO2 + C -> Sn + CO2', 'carbon', 'Sn', 1)]
EXTRACT = {'potassium': 'electrolysis of the molten chloride', 'sodium': 'electrolysis of molten sodium chloride', 'calcium': 'electrolysis of the molten chloride',
           'magnesium': 'electrolysis of molten magnesium chloride', 'aluminium': 'electrolysis of aluminium oxide dissolved in molten cryolite',
           'zinc': 'reduction of the oxide with carbon', 'iron': 'reduction of the oxide with carbon (carbon monoxide) in a blast furnace', 'lead': 'reduction of the oxide with carbon',
           'copper': 'reduction with carbon (or electrolysis to purify)', 'silver': 'collecting the native (uncombined) metal', 'gold': 'collecting the native (uncombined) metal'}

t5a = topic('Extraction method and reactivity', 'relating the method of extraction to the reactivity series', 'reduction with carbon', 'extraction')
t5a.fixed('C1', (1, 2), [
    ('Which metal is extracted from its oxide by heating with carbon?', 'zinc', 'Metals below carbon in the reactivity series (Zn, Fe, Pb, Cu) are extracted by reduction with carbon.', ['sodium', 'aluminium', 'magnesium']),
    ('Why must aluminium be extracted by electrolysis rather than by heating with carbon?', 'Aluminium is more reactive than carbon', 'Carbon cannot remove oxygen from oxides of metals above it in the series.', ['Aluminium oxide is a gas', 'Aluminium is less reactive than carbon', 'Carbon reacts with aluminium to form a carbide only']),
    ('Why is gold found as the uncombined element in the Earth’s crust?', 'It is very unreactive', 'Gold does not react with oxygen or water, so it occurs native.', ['It is very reactive', 'It has a low density', 'It is a non-metal']),
    ('In the reaction 2CuO + C → 2Cu + CO₂, what happens to the copper(II) oxide?', 'It is reduced', 'CuO loses oxygen: reduction. Carbon gains oxygen: oxidation.', ['It is oxidised', 'It is neutralised', 'It is decomposed by heat alone']),
    ('What is an ore?', 'A rock containing enough of a metal compound to make extraction worthwhile', 'Ores are naturally occurring rocks from which metals are economically extracted.', ['A pure metal found in the ground', 'An alloy of two metals', 'A mixture of metal and carbon']),
    ('State the method used to extract metals that are more reactive than carbon.', 'Electrolysis of the molten compound.', '[1]'),
])
t5a.fixed('C2', (2, 3, 4), [
    ('Explain why electrolysis is expensive compared with reduction by carbon.', 'It needs large amounts of electricity to melt the ore and decompose it.', '[2]'),
    ('Explain why gold and silver were among the first metals used by humans, whereas aluminium was not extracted until the 19th century.', 'Gold and silver are unreactive and found native; aluminium is very reactive and its compounds can only be decomposed by electrolysis, which needed electricity.', '[3]'),
    ('Explain why carbon is used to extract zinc but not magnesium.', 'Carbon is more reactive than zinc so it removes oxygen from zinc oxide; magnesium is more reactive than carbon.', '[2]'),
    ('Explain why reduction is defined as the loss of oxygen in extraction reactions.', 'The metal oxide gives up its oxygen to the reducing agent (carbon) to leave the metal.', '[1]'),
    ('Explain why recycling metals such as aluminium is important.', 'It saves ores (finite resources) and energy, reduces mining damage and landfill.', '[2]'),
])


@t5a.add('C1', (1, 2, 3))
def t5a_method(r, D):
    m = r.choice(list(EXTRACT))
    corr = EXTRACT[m]
    pool = ['electrolysis of the molten compound', 'reduction of the oxide with carbon', 'found native (uncombined)', 'reduction with hydrogen gas', 'displacement with copper', 'heating the ore with water']
    if corr.startswith('electrolysis'):
        corr2 = 'electrolysis of the molten compound'
    elif corr.startswith('reduction'):
        corr2 = 'reduction of the oxide with carbon'
    else:
        corr2 = 'found native (uncombined)'  # 'collecting the native metal'
    return mcq_q(r, f'Which method is used to obtain {m} from its compounds?', corr2, pool, f'{m}: {corr}. Position relative to carbon in the reactivity series decides the method.')


@t5a.add('C3', (2, 3, 4, 5), 'numerical')
def t5a_mass(r, D):
    m, ore, f, eq, red, sym, k = r.choice([o for o in ORES if o[0] != 'iron'])
    mass = r.choice([8.1, 16.2, 40.5, 4.46, 22.3, 2.0, 8.0, 15.1, 30.2]) if D < 4 else r.choice([100, 250, 500, 1000])
    unit = 'g' if D < 4 else 'kg'
    no = mass / Mr(f)
    mm = no * AR[sym]
    stem = f'{sf(mass)} {unit} of {F(f)} is heated with carbon. {E(eq)}. Calculate the maximum mass of {m} that can be obtained.'
    key = f'n({F(f)}) = {sf(mass)}/{mr(Mr(f))} = {g3(no)} {"mol" if unit == "g" else "kmol"} [1]; n({sym}) = {g3(no)} [1]; mass = {g3(no)} × {AR[sym]} = {g3(mm)} {unit} [1]'
    if D >= 5:
        mc = no / k * 12 if 'CO2' in eq and f != 'SnO2' else no * 12
        stem += ' Also calculate the minimum mass of carbon needed.'
        return {'stem': stem, 'answer': f'{g3(mm)} {unit}; carbon {g3(mc)} {unit}', 'key': key + f'; n(C) from equation ratio; mass C = {g3(mc)} {unit} [1]', 'marks': 4}
    return {'stem': stem, 'answer': f'{g3(mm)} {unit}', 'key': key}


@t5a.add('C2', (2, 3, 4), 'explain')
def t5a_why(r, D):
    a, b = r.sample([x for x in EXTRACT if x in SERIES and x != 'copper'], 2)
    pos = lambda x: 'very low in the series (unreactive)' if x in ('silver', 'gold') else ('above carbon' if SERIES.index(x) < SERIES.index('carbon') else 'below carbon')
    if EXTRACT[a].split()[0] == EXTRACT[b].split()[0]:
        return None
    return {'stem': f'{cap(a)} is obtained by {EXTRACT[a]}, while {b} is obtained by {EXTRACT[b]}. Use the reactivity series to explain the difference.',
            'answer': f'{cap(a)} is {pos(a)} and {b} is {pos(b)} in the reactivity series. Metals above carbon need electrolysis; metals below carbon can be reduced by carbon; very unreactive metals are found native.',
            'key': '1 mark each metal positioned relative to carbon; 1 mark rule linking position to method [3]', 'marks': 3}


@t5a.add('C3', (1, 2, 3))
def t5a_redox(r, D):
    m, ore, f, eq, red, sym, k = r.choice(ORES)
    if D == 1:
        return mcq_q(r, f'In the reaction {E(eq)}, which substance is the reducing agent?', 'carbon monoxide' if 'CO ->' not in eq and 'CO' in eq.split('->')[0] else 'carbon',
                     ['carbon', 'carbon monoxide', F(f), m, 'carbon dioxide'], f'The reducing agent removes oxygen from {F(f)} and is itself oxidised.')
    return {'stem': f'For the reaction {E(eq)}, identify the substance oxidised and the substance reduced, giving a reason in each case.',
            'answer': f'{F(f)} is reduced (loses oxygen); {"carbon monoxide" if "3CO ->" in eq.replace(" ", " ") or "+ 3CO" in eq else "carbon"} is oxidised (gains oxygen).', 'key': '1 mark each with reason [2]'}


def _ext_c4(r, D):
    m, ore, f, eq, red, sym, k = r.choice([o for o in ORES if o[0] != 'iron'])
    mass = r.choice([200, 500, 1000, 2000])
    pur = r.choice([60, 75, 80, 85, 90])
    no = mass * pur / 100 / Mr(f)
    mm = no * AR[sym]
    intro = r.choice([f'A mining company in {city(r)} extracts {m} from an ore containing {F(f)}.', f'{person(r)} reads that {m} is extracted from {ore} by heating it with {red}.',
                      f'In a small smelter, {mass} kg of ore containing {pur}% {F(f)} by mass is heated with coke.'])
    parts = [
        lambda r: (f'Explain why {m} can be extracted using carbon.', f'Carbon is more reactive than {m}, so it can remove oxygen from {F(f)}.', '[2]'),
        lambda r: ('Write the balanced equation for the reduction.', E(eq), '[2]'),
        lambda r: (f'Identify the oxidising agent and explain your choice.', f'{F(f)}: it gives oxygen to carbon (it is reduced).', '[2]'),
        lambda r: (f'{mass} kg of ore contains {pur}% {F(f)}. Calculate the maximum mass of {m} produced.', f'{g3(mm)} kg', f'mass {F(f)} = {g3(mass * pur / 100)} kg [1]; n = {g3(no)} kmol [1]; mass {m} = {g3(mm)} kg [1]; total [3]'),
        lambda r: ('Suggest one environmental problem caused by extracting metals from ores.', 'Mining scars the landscape/habitat loss; CO₂ from burning coke contributes to climate change; waste rock.', '[1]'),
        lambda r: ('Explain why aluminium cannot be extracted in the same way.', 'Aluminium is more reactive than carbon, so carbon cannot reduce aluminium oxide; electrolysis is needed.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t5a.add('C4', (2, 3, 4, 5), 'multi_step')(_ext_c4)
t5a.add('C3', (3, 4), 'multi_step')(_ext_c4)

# ---------------------------------------------------------- 5.2 blast furnace
BF = [('C + O2 -> CO2', 'Coke burns in hot air, releasing heat', 'heat'), ('CO2 + C -> 2CO', 'Carbon dioxide reacts with more coke to form carbon monoxide', 'reducing agent'),
      ('Fe2O3 + 3CO -> 2Fe + 3CO2', 'Carbon monoxide reduces iron(III) oxide to iron', 'reduction'), ('CaCO3 -> CaO + CO2', 'Limestone undergoes thermal decomposition', 'decomposition'),
      ('CaO + SiO2 -> CaSiO3', 'Calcium oxide reacts with silicon(IV) oxide impurities to form slag', 'slag')]
t5b = topic('Blast furnace', 'extraction of iron from hematite in the blast furnace', 'including symbol equations', 'blast furnace')
t5b.fixed('C1', (1, 2), [
    ('What are the three raw materials added at the top of the blast furnace?', 'hematite, coke and limestone', 'Iron ore (hematite), coke (carbon) and limestone; hot air is blown in near the bottom.', ['hematite, coal and sand', 'bauxite, coke and limestone', 'hematite, cryolite and coke']),
    ('Which substance reduces iron(III) oxide in the blast furnace?', 'carbon monoxide', 'Fe₂O₃ + 3CO → 2Fe + 3CO₂.', ['oxygen', 'calcium oxide', 'carbon dioxide']),
    ('What is the purpose of limestone in the blast furnace?', 'To remove acidic impurities such as silicon(IV) oxide as slag', 'CaCO₃ → CaO + CO₂; CaO + SiO₂ → CaSiO₃ (slag).', ['To reduce the iron ore', 'To provide heat', 'To make the iron harder']),
    ('What is the chemical name of slag?', 'calcium silicate', 'CaO + SiO₂ → CaSiO₃.', ['calcium carbonate', 'calcium oxide', 'iron(III) silicate']),
    ('Why is coke burned in hot air at the bottom of the furnace?', 'It provides heat and produces carbon dioxide', 'C + O₂ → CO₂ is very exothermic.', ['It reduces the limestone', 'It removes the slag', 'It cools the furnace']),
    ('State the formula of hematite.', 'Fe₂O₃', '[1]'),
])
t5b.fixed('C2', (2, 3, 4), [
    ('Explain why the molten iron and slag form two separate layers at the bottom of the furnace.', 'Slag is less dense than molten iron, so it floats on top; they do not mix and can be tapped off separately.', '[2]'),
    ('Explain why the reaction CaO + SiO₂ → CaSiO₃ is described as a neutralisation.', 'Calcium oxide is a basic oxide and silicon(IV) oxide is an acidic oxide; they react to form a salt.', '[2]'),
    ('Explain why the waste gases leaving the top of the blast furnace include nitrogen.', 'Hot air is blown in; the nitrogen in it is unreactive and passes through unchanged.', '[1]'),
    ('Explain why carbon monoxide is described as the reducing agent in the blast furnace.', 'It removes oxygen from iron(III) oxide and is itself oxidised to carbon dioxide.', '[2]'),
    ('Explain why the iron from the blast furnace is usually converted into steel.', 'Blast-furnace iron contains about 4% carbon, making it brittle; removing most of the carbon and adding other elements gives stronger, less brittle steel.', '[2]'),
])


@t5b.add('C1', (1, 2, 3))
def t5b_eq(r, D):
    eq, desc, role = r.choice(BF)
    return mcq_q(r, f'Which equation shows the reaction in the blast furnace in which {desc[0].lower() + desc[1:]}?', E(eq), [E(x[0]) for x in BF] + [E('2Fe2O3 + 3C -> 4Fe + 3CO2'), E('Fe2O3 + 3H2 -> 2Fe + 3H2O')], f'{desc}: {E(eq)}.')


@t5b.add('C3', (1, 2, 3, 4))
def t5b_write(r, D):
    eq, desc, role = r.choice(BF)
    if D == 1:
        return mcq_q(r, f'In the blast furnace, {E(eq)}. What type of reaction is this?', {'heat': 'combustion (oxidation)', 'reducing agent': 'redox: carbon dioxide is reduced', 'reduction': 'redox: iron(III) oxide is reduced',
                     'decomposition': 'thermal decomposition', 'slag': 'neutralisation (acid–base)'}[role], ['combustion (oxidation)', 'redox: carbon dioxide is reduced', 'redox: iron(III) oxide is reduced', 'thermal decomposition', 'neutralisation (acid–base)'], desc + '.')
    return {'stem': f'In the blast furnace, {desc[0].lower() + desc[1:]}. Write the balanced symbol equation for this reaction' + (' and state why it is important to the process.' if D >= 3 else '.'),
            'answer': E(eq) + ({'heat': '; it raises the temperature of the furnace.', 'reducing agent': '; it makes the reducing agent CO.', 'reduction': '; it produces the iron.', 'decomposition': '; it makes CaO to remove impurities.', 'slag': '; it removes sandy impurities as slag.'}[role] if D >= 3 else ''),
            'key': 'formulae [1]; balancing [1]' + ('; importance [1]' if D >= 3 else ''), 'marks': 3 if D >= 3 else 2}


@t5b.add('C3', (2, 3, 4, 5), 'numerical')
def t5b_mass(r, D):
    t = r.choice([10, 20, 40, 50, 80, 100, 160, 200, 500])
    pur = r.choice([100, 90, 80, 75, 64, 85]) if D >= 3 else 100
    mfe = t * pur / 100 * 112 / 160
    stem = f'An ore contains {pur}% iron(III) oxide by mass. Calculate the maximum mass of iron, in tonnes, that can be extracted from {t} tonnes of the ore. (Fe₂O₃ + 3CO → 2Fe + 3CO₂)' if pur != 100 else f'Calculate the maximum mass of iron, in tonnes, that can be extracted from {t} tonnes of pure iron(III) oxide. (Fe₂O₃ + 3CO → 2Fe + 3CO₂)'
    key = f'Mr Fe₂O₃ = 160; 160 t gives 2 × 56 = 112 t Fe [1]' + (f'; mass Fe₂O₃ = {g3(t * pur / 100)} t [1]' if pur != 100 else '') + f'; mass Fe = {g3(t * pur / 100)} × 112/160 = {g3(mfe)} t [1]'
    if D >= 5:
        vco = t * pur / 100 * 1e6 / 160 * 3 * 24 / 1000
        stem += ' Calculate also the volume of carbon monoxide, in m³ at r.t.p., needed to reduce the iron(III) oxide (1 m³ = 1000 dm³).'
        return {'stem': stem, 'answer': f'{g3(mfe)} t; {g3(vco)} m³ CO', 'key': key + f'; n(Fe₂O₃) = {g3(t * pur / 100 * 1e6 / 160)} mol, n(CO) = 3×, V = n × 24 dm³ = {g3(vco)} m³ [2]', 'marks': 5}
    return {'stem': stem, 'answer': f'{g3(mfe)} tonnes', 'key': key}


@t5b.add('C3', (2, 3, 4, 5), 'numerical')
def t5b_purity(r, D):
    M = r.choice([20, 25, 40, 50, 60, 80, 120, 150, 250, 400])
    pur = r.choice(range(52, 96))
    mfe = r3(M * pur / 100 * 112 / 160)
    who, where = person(r), city(r)
    pc = mfe * 160 / 112 / M * 100
    ctx = r.choice([f'At a steelworks near {where}, {M} tonnes of hematite ore produced {g3(mfe)} tonnes of iron.',
                    f'{who} is told that {M} tonnes of iron ore from a mine near {where} gave {g3(mfe)} tonnes of iron in a blast furnace.',
                    f'A blast furnace is charged with {M} t of hematite and {g3(mfe)} t of iron is tapped off.'])
    ask = r.choice(['Calculate the percentage by mass of iron(III) oxide in the ore.', 'Determine the percentage purity of the ore, assuming all the iron(III) oxide was reduced.'])
    stem = f'{ctx} Fe₂O₃ + 3CO → 2Fe + 3CO₂. {ask}'
    key = f'mass Fe₂O₃ = {g3(mfe)} × 160/112 = {g3(mfe * 160 / 112)} t [1]; % = {g3(mfe * 160 / 112)}/{M} × 100 = {g3(pc)}% [1]'
    if D >= 4:
        stem += ' Suggest one reason why the actual percentage could be higher than your answer.'
        return {'stem': stem, 'answer': f'{g3(pc)}%; some iron is lost (e.g. in the slag) or not all the oxide is reduced.', 'key': key + '; iron lost in slag/incomplete reduction [1]', 'marks': 3}
    return {'stem': stem, 'answer': f'{g3(pc)}%', 'key': key}


def _bf_c4(r, D):
    t = r.choice([100, 200, 400, 800, 1000])
    pur = r.choice([70, 75, 80, 84, 90])
    mfe = t * pur / 100 * 112 / 160
    intro = r.choice([f'A steelworks in {city(r)} feeds {t} tonnes of hematite ore containing {pur}% iron(III) oxide into its blast furnace each day.', f'{person(r)} is writing a report on the blast furnace used to extract iron from hematite ({pur}% Fe₂O₃).',
                      'A diagram of a blast furnace shows raw materials entering at the top, hot air blown in near the base, and two tap holes at the bottom.'])
    parts = [
        lambda r: ('Name the three solid raw materials.', 'Hematite (iron ore), coke and limestone.', '[1]'),
        lambda r: ('Describe, with equations, how carbon monoxide is formed in the furnace.', f'Coke burns: {E("C + O2 -> CO2")}; CO₂ reacts with more coke: {E("CO2 + C -> 2CO")}.', '1 mark each equation; 1 mark description [3]'),
        lambda r: ('Write the equation for the reduction of iron(III) oxide.', E('Fe2O3 + 3CO -> 2Fe + 3CO2'), '[2]'),
        lambda r: ('Explain, with equations, how sandy impurities are removed.', f'{E("CaCO3 -> CaO + CO2")}; {E("CaO + SiO2 -> CaSiO3")} — slag floats on the iron and is tapped off.', '[3]'),
        lambda r: (f'Calculate the maximum mass of iron produced from {t} tonnes of the ore.', f'{g3(mfe)} tonnes', f'mass Fe₂O₃ = {g3(t * pur / 100)} t [1]; × 112/160 = {g3(mfe)} t [1]; total [2]'),
        lambda r: ('Name two gases that leave the top of the furnace.', 'Nitrogen and carbon dioxide (also some carbon monoxide).', '[2]'),
        lambda r: ('Suggest one use for the slag.', 'Road building or making cement.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t5b.add('C4', (2, 3, 4, 5), 'multi_step')(_bf_c4)
t5b.add('C3', (3, 4, 5), 'multi_step')(_bf_c4)

# ---------------------------------------------------------- 5.3 aluminium
t5c = topic('Extraction of aluminium', 'extraction of aluminium from purified bauxite by electrolysis with cryolite', 'electrolysis with cryolite', 'aluminium extraction')
t5c.fixed('C1', (1, 2), [
    ('What is the main ore of aluminium?', 'bauxite', 'Bauxite is purified to give aluminium oxide (alumina).', ['hematite', 'cryolite', 'limestone']),
    ('Why is aluminium oxide dissolved in molten cryolite?', 'To lower the operating temperature and improve conductivity', 'Al₂O₃ melts above 2000 °C; the solution in cryolite works at about 950 °C, saving energy.', ['To reduce the aluminium ions', 'To provide oxygen for the anode', 'To make the aluminium stronger']),
    ('What forms at the cathode during the electrolysis of aluminium oxide?', 'aluminium', 'Al³⁺ + 3e⁻ → Al at the negative electrode.', ['oxygen', 'carbon dioxide', 'cryolite']),
    ('Why do the carbon anodes need to be replaced regularly?', 'They react with the oxygen produced to form carbon dioxide', 'C + O₂ → CO₂ at high temperature burns the anodes away.', ['They dissolve in the aluminium', 'They are reduced to aluminium', 'They melt']),
    ('What is the half-equation at the cathode?', 'Al³⁺ + 3e⁻ → Al', 'Aluminium ions gain electrons (reduction).', ['2O²⁻ → O₂ + 4e⁻', 'Al → Al³⁺ + 3e⁻', 'O₂ + 4e⁻ → 2O²⁻']),
    ('State the name of the electrolyte used in the extraction of aluminium.', 'Aluminium oxide dissolved in molten cryolite.', '[1]'),
])
t5c.fixed('C2', (2, 3, 4), [
    ('Explain why the aluminium oxide must be molten or dissolved before electrolysis.', 'The ions must be free to move to the electrodes; in the solid they are held in a lattice.', '[2]'),
    ('Explain why the extraction of aluminium uses large amounts of energy.', 'Electricity is needed to keep the electrolyte molten and to decompose Al₂O₃ (strong bonds), and the process runs at about 950 °C.', '[2]'),
    ('Explain why aluminium smelters are often built near hydroelectric power stations.', 'They need huge amounts of electricity; hydroelectric power is cheap and renewable.', '[2]'),
    ('Explain why the reaction at the anode is oxidation.', 'Oxide ions lose electrons to form oxygen molecules: 2O²⁻ → O₂ + 4e⁻.', '[2]'),
    ('Explain why recycling aluminium cans saves more energy than extracting new aluminium.', 'Melting scrap aluminium needs only about 5% of the energy needed for electrolysis of bauxite; it also saves ore.', '[2]'),
])


@t5c.add('C3', (2, 3, 4, 5), 'numerical')
def t5c_mass(r, D):
    t = r.choice([51, 102, 204, 306, 510, 1020, 25.5, 2040])
    mal = t * 54 / 102
    if D >= 4:
        mo2 = t * 48 / 102
        return {'stem': f'{sf(t)} tonnes of aluminium oxide are electrolysed. 2Al₂O₃ → 4Al + 3O₂. Calculate the mass of aluminium produced and the mass of oxygen released at the anodes. Suggest why the actual mass of anode carbon lost is large.',
                'answer': f'{g3(mal)} t aluminium; {g3(mo2)} t oxygen; the oxygen reacts with the hot carbon anodes to form CO₂, burning them away.', 'key': f'Mr Al₂O₃ = 102; 204 t → 108 t Al [1]; Al = {g3(mal)} t [1]; O₂ = {g3(mo2)} t [1]; anodes oxidised to CO₂ [1]', 'marks': 4}
    return {'stem': f'Calculate the maximum mass of aluminium that can be obtained from {sf(t)} tonnes of pure aluminium oxide. (2Al₂O₃ → 4Al + 3O₂)', 'answer': f'{g3(mal)} tonnes',
            'key': f'Mr Al₂O₃ = 102; 2 × 102 = 204 t gives 4 × 27 = 108 t [1]; mass = {sf(t)} × 108/204 = {g3(mal)} t [1]'}


@t5c.add('C3', (2, 3, 4, 5), 'numerical')
def t5c_purity(r, D):
    M = r.choice([10, 20, 40, 50, 75, 100, 200, 300, 500])
    pur = r.choice(range(40, 66))
    mal = r3(M * pur / 100 * 108 / 204)
    where = city(r)
    pc = mal * 204 / 108 / M * 100
    mode = r.choice(['purity', 'al'])
    if mode == 'purity':
        stem = r.choice([f'A plant near {where} electrolyses the alumina obtained from {M} tonnes of bauxite and produces {g3(mal)} tonnes of aluminium.',
                         f'{M} t of bauxite yields enough purified aluminium oxide to make {g3(mal)} t of aluminium by electrolysis.'])
        stem += ' 2Al₂O₃ → 4Al + 3O₂. Calculate the percentage by mass of aluminium oxide in the bauxite.'
        ans = f'{g3(pc)}%'
        key = f'mass Al₂O₃ = {g3(mal)} × 204/108 = {g3(mal * 204 / 108)} t [1]; % = {g3(mal * 204 / 108)}/{M} × 100 = {g3(pc)}% [1]'
    else:
        stem = f'Bauxite mined near {where} contains {pur}% aluminium oxide by mass. Calculate the mass of aluminium that could be made from {M} tonnes of this bauxite. 2Al₂O₃ → 4Al + 3O₂'
        ans = f'{g3(M * pur / 100 * 108 / 204)} t'
        key = f'mass Al₂O₃ = {g3(M * pur / 100)} t [1]; Al = {g3(M * pur / 100)} × 108/204 = {ans} [1]'
    if D >= 4:
        stem += ' State why the electrolysis uses so much electrical energy.'
        return {'stem': stem, 'answer': ans + '; a large current is needed and the electrolyte must be kept molten (about 950 °C).', 'key': key + '; high current / keeping electrolyte molten [1]', 'marks': 3}
    return {'stem': stem, 'answer': ans, 'key': key}


@t5c.add('C3', (1, 2, 3))
def t5c_half(r, D):
    el = r.choice(['cathode', 'anode'])
    eq = 'Al³⁺ + 3e⁻ → Al' if el == 'cathode' else '2O²⁻ → O₂ + 4e⁻'
    if D == 1:
        return mcq_q(r, f'Which half-equation shows the reaction at the {el} in the extraction of aluminium?', eq, ['Al³⁺ + 3e⁻ → Al', '2O²⁻ → O₂ + 4e⁻', 'Al → Al³⁺ + 3e⁻', 'O₂ + 4e⁻ → 2O²⁻', 'C + O₂ → CO₂'], f'{el}: {eq}.')
    return {'stem': f'Write the half-equation for the reaction at the {el} in the extraction of aluminium, and state whether it is oxidation or reduction.',
            'answer': f'{eq}; {"reduction (gain of electrons)" if el == "cathode" else "oxidation (loss of electrons)"}', 'key': '1 mark equation; 1 mark oxidation/reduction with reason [2]'}


@t5c.add('C2', (2, 3, 4), 'explain')
def t5c_err(r, D):
    claims = [('aluminium is produced at the anode', 'Aluminium ions are positive, so they are attracted to the negative cathode, where they gain electrons.'),
              ('cryolite is the ore of aluminium', 'Bauxite is the ore; cryolite is a solvent that lowers the melting point of the electrolyte.'),
              ('aluminium could be extracted more cheaply by heating its oxide with carbon', 'Aluminium is more reactive than carbon, so carbon cannot reduce aluminium oxide.'),
              ('the carbon anodes are used up because they dissolve in the aluminium', 'They burn away because oxygen formed at the anode reacts with the hot carbon to form carbon dioxide.'),
              ('solid aluminium oxide conducts electricity', 'In the solid the ions cannot move; it must be molten or dissolved in cryolite.')]
    c, fix = r.choice(claims)
    return {'stem': f'{person(r)} writes that in the extraction of aluminium "{c}". Explain why this is incorrect.', 'answer': fix, 'key': '1 mark identifying the error; 1 mark correct chemistry [2]'}


def _al_ext_c4(r, D):
    t = r.choice([102, 204, 510, 1020])
    intro = r.choice([f'An aluminium smelter in {city(r)} electrolyses purified bauxite dissolved in molten cryolite at about 950 °C.', f'{person(r)} visits an aluminium plant where {t} tonnes of aluminium oxide are electrolysed each day.',
                      'A diagram shows a steel cell lined with carbon (the cathode) containing a molten electrolyte, with large carbon blocks dipping into it as anodes.'])
    parts = [
        lambda r: ('Explain why cryolite is used.', 'Aluminium oxide dissolves in molten cryolite at a much lower temperature than its melting point, saving energy; it also improves conductivity.', '[2]'),
        lambda r: ('Write the half-equation at the cathode.', 'Al³⁺ + 3e⁻ → Al', '[1]'),
        lambda r: ('Write the half-equation at the anode.', '2O²⁻ → O₂ + 4e⁻', '[1]'),
        lambda r: ('Explain why the anodes must be replaced regularly, with an equation.', f'Oxygen reacts with the hot carbon: {E("C + O2 -> CO2")}, so the anodes burn away.', '[2]'),
        lambda r: (f'Calculate the mass of aluminium produced from {t} tonnes of aluminium oxide.', f'{g3(t * 54 / 102)} tonnes', '[2]'),
        lambda r: ('Give two reasons why recycling aluminium is better than extracting it.', 'Saves energy; conserves bauxite; less mining damage; less CO₂ from anodes and power generation.', '[2]'),
        lambda r: ('Explain why the molten aluminium collects at the bottom of the cell.', 'It is denser than the electrolyte, so it sinks and is siphoned off.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t5c.add('C4', (2, 3, 4, 5), 'multi_step')(_al_ext_c4)
t5c.add('C3', (3, 4), 'multi_step')(_al_ext_c4)

# ---------------------------------------------------------- 5.4 rusting
RUST_TUBES = [('an iron nail in tap water, open to the air', True, 'water and oxygen are both present'), ('an iron nail in boiled water covered with a layer of oil', False, 'boiling removes dissolved oxygen and the oil stops air dissolving'),
              ('an iron nail in dry air with anhydrous calcium chloride', False, 'there is no water'), ('an iron nail in salt water, open to the air', True, 'water and oxygen are present and salt speeds up rusting'),
              ('an iron nail coated in grease, in tap water', False, 'the grease is a barrier that keeps out water and oxygen'), ('an iron nail wrapped in a strip of magnesium, in tap water', False, 'magnesium is more reactive and corrodes instead (sacrificial protection)'),
              ('an iron nail wrapped in a strip of copper, in tap water', True, 'copper is less reactive than iron, so iron still rusts (faster)'), ('a galvanised (zinc-coated) iron nail in tap water', False, 'zinc is a barrier and also corrodes in preference to iron'),
              ('an iron nail painted all over, in tap water', False, 'the paint is a barrier that keeps out water and oxygen'), ('an iron nail in pure nitrogen gas with water', False, 'no oxygen is present')]
PROTECT = [('painting', 'barrier', 'car bodies, bridges and railings'), ('oiling or greasing', 'barrier', 'bicycle chains and machinery'), ('coating with plastic', 'barrier', 'garden fences and dish racks'),
           ('galvanising (coating with zinc)', 'barrier and sacrificial', 'steel roofing sheets and buckets'), ('attaching blocks of magnesium or zinc', 'sacrificial', 'ships’ hulls and underground pipes'),
           ('electroplating with chromium or tin', 'barrier', 'food cans and bicycle handlebars')]

t5d = topic('Rusting and its prevention', 'rusting of iron and steel', 'barrier methods, galvanising and sacrificial protection', 'corrosion')
t5d.fixed('C1', (1, 2), [
    ('Which two substances are needed for iron to rust?', 'oxygen and water', 'Iron + oxygen + water → hydrated iron(III) oxide.', ['carbon dioxide and water', 'nitrogen and oxygen', 'salt and carbon dioxide']),
    ('What is the chemical name for rust?', 'hydrated iron(III) oxide', 'Rust is hydrated iron(III) oxide, Fe₂O₃·xH₂O.', ['iron(II) chloride', 'iron carbonate', 'anhydrous iron(II) oxide']),
    ('What is galvanising?', 'Coating iron with a layer of zinc', 'Zinc gives barrier and sacrificial protection.', ['Coating iron with tin', 'Painting iron with oil-based paint', 'Mixing iron with carbon']),
    ('Why does a block of magnesium attached to a steel ship’s hull stop the hull rusting?', 'Magnesium is more reactive and corrodes instead of the iron', 'Sacrificial protection: Mg loses electrons in preference to Fe.', ['Magnesium is a barrier to water', 'Magnesium reacts with salt to make it harmless', 'Magnesium is less reactive than iron']),
    ('Which method of rust prevention is used for a bicycle chain?', 'oiling', 'Oil is a barrier that does not crack as the chain moves.', ['painting', 'galvanising', 'coating with plastic']),
    ('State the word equation for rusting.', 'iron + water + oxygen → hydrated iron(III) oxide', '[1]'),
])
t5d.fixed('C2', (2, 3, 4), [
    ('Explain why a galvanised bucket does not rust even when the zinc coating is scratched.', 'Zinc is more reactive than iron, so it corrodes (loses electrons) in preference to the iron — sacrificial protection.', '[2]'),
    ('Explain why a tin-plated food can rusts quickly once the tin layer is scratched.', 'Tin is less reactive than iron; once exposed, the iron corrodes in preference to the tin (faster than unprotected iron).', '[2]'),
    ('Explain how barrier methods prevent rusting.', 'They stop oxygen and water from reaching the surface of the iron.', '[2]'),
    ('Explain, in terms of electrons, how sacrificial protection works.', 'The more reactive metal (zinc or magnesium) loses electrons more readily than iron, so it is oxidised instead and the iron does not form ions.', '[2]'),
    ('Explain why cars rust faster in coastal cities and where salt is spread on winter roads.', 'Dissolved salt (ions) increases the rate of rusting.', '[1]'),
])


@t5d.add('C1', (1, 2, 3))
def t5d_tube(r, D):
    tubes = r.sample(RUST_TUBES, 4)
    want = r.choice([True, False])
    hits = [x for x in tubes if x[1] == want]
    if len(hits) != 1:
        return None
    corr = hits[0][0]
    return mcq_q(r, f'In which tube does the iron nail {"rust" if want else "not rust"}?', corr, [x[0] for x in tubes], f'{corr}: {hits[0][2]}.')


@t5d.add('C2', (2, 3, 4), 'explain')
def t5d_explain(r, D):
    t = r.choice(RUST_TUBES)
    return {'stem': f'A student sets up {t[0]}. Predict whether the nail rusts after a week, and explain your prediction.', 'answer': f'{"Rusts" if t[1] else "Does not rust"}: {t[2]}.', 'key': '1 mark prediction; 1 mark reason [2]'}


@t5d.add('C1', (1, 2, 3))
def t5d_method(r, D):
    m, kind, use = r.choice(PROTECT)
    return mcq_q(r, f'Which method of preventing rusting is commonly used for {use}?', m, [x[0] for x in PROTECT], f'{m} ({kind} protection) is used for {use}.')


@t5d.add('C3', (2, 3, 4))
def t5d_sac(r, D):
    cases = [('zinc', True), ('magnesium', True), ('copper', False), ('tin', False), ('aluminium', True), ('silver', False)]
    m, ok = r.choice(cases)
    use = r.choice(['a steel pipeline buried in damp soil', 'an iron pier leg in the sea', 'the steel hull of a ship', 'a steel water tank'])
    return {'stem': f'An engineer proposes attaching blocks of {m} to {use} to stop it rusting. Deduce whether this would work and explain your answer in terms of electron loss.',
            'answer': (f'Yes: {m} is more reactive than iron, so it loses electrons and corrodes instead of the iron (sacrificial protection).' if ok else f'No: {m} is less reactive than iron, so the iron would still lose electrons; it may even rust faster.'),
            'key': '1 mark conclusion; 1 mark reactivity comparison; 1 mark electron loss explanation [3]', 'marks': 3}


@t5d.add('C3', (2, 3, 4), 'numerical')
def t5d_mass(r, D):
    m_fe = r.choice([5.6, 11.2, 2.8, 16.8, 22.4])
    m_r = m_fe / 112 * 160
    o2 = m_fe / 56 * 0.75 * 24
    return {'stem': f'An iron nail of mass {sf(m_fe)} g rusts completely to form iron(III) oxide (ignore the water of hydration). 4Fe + 3O₂ → 2Fe₂O₃. Calculate the mass of iron(III) oxide formed and the volume of oxygen used at r.t.p., in dm³.',
            'answer': f'{g3(m_r)} g; {g3(o2)} dm³', 'key': f'n(Fe) = {sf(m_fe)}/56 = {g3(m_fe / 56)} mol [1]; n(Fe₂O₃) = {g3(m_fe / 112)} mol, mass = {g3(m_r)} g [1]; n(O₂) = ¾ × {g3(m_fe / 56)} = {g3(m_fe / 56 * 0.75)} mol, V = {g3(o2)} dm³ [1]'}


SCRATCH = [('galvanised', False, 'zinc is more reactive than iron, so the zinc loses electrons and corrodes instead (sacrificial protection)'),
           ('painted', True, 'paint is only a barrier; once broken, water and oxygen reach the iron'),
           ('tin-plated', True, 'tin is less reactive than iron, so the iron loses electrons and rusts, even faster than unprotected iron'),
           ('plastic-coated', True, 'the plastic is only a barrier; water and oxygen now reach the iron'),
           ('greased', True, 'grease is only a barrier; where it is wiped off, water and oxygen reach the iron')]
OBJS = ['steel bucket', 'car door panel', 'garden gate', 'food can', 'steel roofing sheet', 'wheelbarrow', 'bicycle frame', 'steel fence post', 'farm water trough', 'lamp post']


@t5d.add('C3', (2, 3, 4))
def t5d_scratch(r, D):
    obj = r.choice(OBJS)
    if D >= 3:
        (a, ra, wa), (b, rb, wb) = r.sample(SCRATCH, 2)
        if ra == rb:
            return None
        stem = f'{person(r)} has two {obj}s, one {a} and one {b}. Both are deeply scratched so that the iron underneath is exposed to rain. Predict which one rusts at the scratch, and explain both observations in terms of reactivity or barriers.'
        return {'stem': stem, 'answer': f'The {a if ra else b} {obj} rusts. {a.capitalize()}: {wa}. {b.capitalize()}: {wb}.',
                'key': '1 mark correct prediction; 1 mark each explanation [3]', 'marks': 3}
    c, rusts, why = r.choice(SCRATCH)
    stem = f'A {c} {obj} in {city(r)} is scratched, exposing the iron underneath. Predict whether the iron at the scratch will rust. Explain your answer.'
    return {'stem': stem, 'answer': f'{"Yes" if rusts else "No"}: {why}.', 'key': '1 mark prediction; 1 mark explanation [2]'}


def _rust_c4(r, D):
    tubes = r.sample(RUST_TUBES, 4)
    tbl = '; '.join(f'tube {i + 1}: {t[0]}' for i, t in enumerate(tubes))
    intro = f'{person(r)} sets up four test-tubes to investigate rusting and leaves them for one week. {tbl}.'
    rusted = [str(i + 1) for i, t in enumerate(tubes) if t[1]]
    parts = [
        lambda r: ('Predict in which tubes the nail rusts.', ', '.join(rusted) or 'none', '[2]'),
        lambda r: ('For one tube where the nail does not rust, explain why.', next((f'Tube {i + 1}: {t[2]}.' for i, t in enumerate(tubes) if not t[1]), 'All nails rust: water and oxygen present.'), '[2]'),
        lambda r: ('State the conditions needed for rusting.', 'Water and oxygen both present.', '[1]'),
        lambda r: ('Write the word equation for rusting.', 'iron + water + oxygen → hydrated iron(III) oxide', '[1]'),
        lambda r: ('Explain why galvanised steel is used for roofing sheets.', 'Zinc coating is a barrier and, if scratched, zinc corrodes in preference to iron (sacrificial).', '[2]'),
        lambda r: ('Suggest why a painted car body rusts quickly once the paint is chipped.', 'The barrier is broken; water and oxygen reach the iron; paint gives no sacrificial protection.', '[2]'),
        lambda r: ('Describe how boiling the water and adding oil changes the conditions.', 'Boiling removes dissolved oxygen; the oil layer stops oxygen from the air redissolving.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t5d.add('C4', (2, 3, 4, 5), 'case')(_rust_c4)
t5d.add('C3', (3, 4), 'case')(_rust_c4)

CHAPTERS[5] = [t5a, t5b, t5c, t5d]


# ===================================================================== Ch6 (CB17) Chemistry of our environment
WTREAT = [('sedimentation and filtration', 'removes solids (sand, soil and other insoluble particles)'), ('treatment with carbon (activated charcoal)', 'removes tastes and odours'),
          ('chlorination', 'kills microbes (bacteria) that cause disease')]
WPOLL = [('nitrates and phosphates from fertilisers', 'cause eutrophication: algae grow, die and decompose, and bacteria use up dissolved oxygen so aquatic life dies'),
         ('metal compounds (e.g. lead or mercury compounds)', 'are toxic to humans and aquatic organisms'), ('sewage', 'contains harmful microbes that cause disease (e.g. cholera)'),
         ('plastics', 'harm aquatic life that eats them or becomes trapped'), ('harmful microbes', 'cause diseases such as cholera and typhoid')]
WSUB = [('dissolved oxygen', 'beneficial — needed by aquatic life'), ('metal compounds', 'beneficial in small amounts (e.g. calcium for teeth) but some, such as lead, are toxic'), ('nitrates from fertilisers', 'harmful — cause eutrophication')]

t6a = topic('Water: tests, treatment and pollutants', 'water: chemical tests for water', 'treatment of the domestic water supply and pollutants in water', 'water treatment')
t6a.fixed('C1', (1, 2), [
    ('Which test shows the presence of water?', 'Anhydrous copper(II) sulfate turns from white to blue', 'Water hydrates CuSO₄ (white → blue) or anhydrous CoCl₂ (blue → pink).', ['Limewater turns milky', 'A glowing splint relights', 'Damp red litmus turns blue']),
    ('Which physical test shows that a sample of water is pure?', 'It boils at exactly 100 °C', 'Pure water: b.p. 100 °C and m.p. 0 °C at standard pressure.', ['It turns anhydrous copper(II) sulfate blue', 'It is colourless', 'It has a pH of 7']),
    ('Why is chlorine added to the domestic water supply?', 'To kill microbes', 'Chlorination disinfects the water.', ['To remove the taste', 'To remove insoluble solids', 'To make the water hard']),
    ('What colour change happens when water is added to anhydrous cobalt(II) chloride?', 'blue to pink', 'Anhydrous CoCl₂ is blue; hydrated is pink.', ['pink to blue', 'white to blue', 'colourless to purple']),
    ('Why is distilled water used in practical chemistry rather than tap water?', 'It contains no dissolved ions that could interfere with results', 'Tap water contains dissolved salts and chlorine that could react or contaminate.', ['It is cheaper', 'It boils at a lower temperature', 'It contains more oxygen']),
    ('State the purpose of using carbon in water treatment.', 'To remove tastes and odours.', '[1]'),
])
t6a.fixed('C2', (2, 3, 4), [
    ('Explain why a positive result with anhydrous copper(II) sulfate does not show that water is pure.', 'It tests for the presence of water only; impure water containing dissolved substances also turns it blue. Purity is shown by b.p. 100 °C/m.p. 0 °C.', '[2]'),
    ('Explain how nitrates from fertilisers can cause fish in a lake to die.', 'Nitrates cause rapid growth of algae (eutrophication); the algae die and are decomposed by bacteria, which use up the dissolved oxygen, so fish suffocate.', '1 mark algal growth; 1 mark decomposition by bacteria; 1 mark oxygen depletion [3]'),
    ('Explain why water from rivers is filtered before it is chlorinated.', 'Filtration removes insoluble solids; otherwise solids could shelter microbes and use up chlorine.', '[2]'),
    ('Some substances in river water are beneficial. Give one example and explain why.', 'Dissolved oxygen for aquatic life, or some metal compounds/minerals such as calcium compounds for healthy teeth and bones.', '[2]'),
    ('Explain why untreated sewage in drinking water is dangerous.', 'It contains harmful microbes that cause diseases such as cholera.', '[2]'),
])


@t6a.add('C1', (1, 2, 3))
def t6a_step(r, D):
    step, why = r.choice(WTREAT)
    return mcq_q(r, f'Which stage of water treatment {why}?', step, [x[0] for x in WTREAT] + ['adding fluoride', 'distillation of all the water'], f'{step}: {why}.')


@t6a.add('C2', (2, 3, 4), 'explain')
def t6a_poll(r, D):
    p, eff = r.choice(WPOLL)
    src = r.choice(['a river near farmland', 'a lake beside a town', 'a coastal bay', 'groundwater near an old factory', 'a reservoir'])
    return {'stem': f'Water samples from {src} in {city(r)} contain {p}. Explain why this is a problem.', 'answer': cap(eff) + '.', 'key': '1 mark identifies harm; 1 mark explains how [2]'}


@t6a.add('C3', (1, 2, 3, 4))
def t6a_test(r, D):
    samp = r.choice([('colourless liquid from a car radiator', 'water and antifreeze'), ('liquid condensed from a candle flame', 'water'), ('clear liquid from a rock pool', 'salt water'),
                     ('liquid produced when hydrated copper(II) sulfate is heated', 'water'), ('colourless liquid labelled "pure water"', 'pure water'), ('liquid formed when hydrogen burns', 'water')])
    if D == 1:
        return mcq_q(r, f'A student wants to know whether a {samp[0]} contains water. Which test should be used?', 'add it to anhydrous copper(II) sulfate', ['add it to anhydrous copper(II) sulfate', 'add limewater', 'test with a glowing splint', 'add aqueous silver nitrate', 'test with damp red litmus paper'], 'White anhydrous CuSO₄ turns blue if water is present.')
    pure = samp[1] in ('water', 'pure water')
    return {'stem': f'Describe a chemical test to show that a {samp[0]} contains water, and a physical test to find out whether it is pure water. Predict the results.',
            'answer': f'Add to anhydrous copper(II) sulfate: turns white → blue (or cobalt(II) chloride blue → pink). Measure the boiling point: pure water boils at exactly 100 °C' + ('; this sample would be expected to do so if uncontaminated.' if pure else '; this sample would boil above 100 °C (and over a range) because it is impure.'),
            'key': '1 mark chemical test; 1 mark result; 1 mark boiling/melting point test; 1 mark expected result [4]', 'marks': 4}


def _water_c4(r, D):
    intro = r.choice([f'A water company in {city(r)} takes water from a river that flows past farmland and a town.', f'{person(r)} visits a water-treatment works that supplies drinking water to a large city.',
                      'A village gets its water from a lake. Algae have covered much of the lake surface this summer and some fish have died.'])
    parts = [
        lambda r: ('Describe the stages in treating the water to make it safe to drink, giving the purpose of each.', 'Sedimentation and filtration — remove solids; carbon — removes tastes/odours; chlorination — kills microbes.', '1 mark each stage with purpose [3]'),
        lambda r: ('Explain how fertiliser run-off can lead to fish deaths.', 'Nitrates/phosphates cause algal bloom; algae die; bacteria decompose them using up dissolved oxygen; fish die.', '[3]'),
        lambda r: ('Describe a chemical test for water.', 'Anhydrous copper(II) sulfate turns white to blue (or anhydrous cobalt(II) chloride blue to pink).', '[2]'),
        lambda r: ('State how you could show the treated water is not pure water.', 'Its boiling point would be slightly above 100 °C (or m.p. below 0 °C); evaporation leaves a residue.', '[1]'),
        lambda r: ('Name two pollutants that might be found in the river and their sources.', 'Nitrates/phosphates from fertilisers; sewage from the town; metal compounds from industry; plastics from litter.', '[2]'),
        lambda r: ('Suggest why chlorine is added at the end of the process.', 'To kill microbes so the water stays safe in the pipes to homes.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t6a.add('C4', (2, 3, 4, 5), 'multi_step')(_water_c4)
t6a.add('C3', (3, 4), 'multi_step')(_water_c4)

# ---------------------------------------------------------- 6.2 fertilisers
FERT = [('ammonium nitrate', 'NH4NO3', 'N'), ('ammonium sulfate', '(NH4)2SO4', 'N'), ('ammonium phosphate', '(NH4)3PO4', 'N and P'), ('potassium nitrate', 'KNO3', 'K and N'),
        ('urea', 'CO(NH2)2', 'N'), ('ammonium chloride', 'NH4Cl', 'N'), ('ammonium hydrogenphosphate', '(NH4)2HPO4', 'N and P'), ('potassium sulfate', 'K2SO4', 'K')]
FMAKE = [('ammonium sulfate', '2NH3 + H2SO4 -> (NH4)2SO4', 'sulfuric acid', 2), ('ammonium nitrate', 'NH3 + HNO3 -> NH4NO3', 'nitric acid', 1), ('ammonium phosphate', '3NH3 + H3PO4 -> (NH4)3PO4', 'phosphoric acid', 3)]

t6b = topic('Fertilisers', 'fertilisers: npk', 'ammonium salts and nitrates for plant growth', 'fertilisers')
t6b.fixed('C1', (1, 2), [
    ('Which three elements are supplied by NPK fertilisers?', 'nitrogen, phosphorus and potassium', 'N, P, K are the main elements needed for plant growth.', ['nitrogen, phosphorus and sodium', 'neon, phosphorus and krypton', 'nitrogen, potassium and calcium']),
    ('Which compound would supply both potassium and nitrogen to a crop?', 'potassium nitrate', 'KNO₃ contains K and N.', ['ammonium sulfate', 'potassium chloride', 'ammonium phosphate']),
    ('Which reaction is used to make the fertiliser ammonium sulfate?', 'ammonia + sulfuric acid', '2NH₃ + H₂SO₄ → (NH₄)₂SO₄.', ['ammonia + nitric acid', 'ammonium chloride + water', 'nitrogen + sulfur']),
    ('Why do plants need nitrogen?', 'To make proteins for growth', 'Nitrogen is needed for proteins (and chlorophyll); phosphorus for roots; potassium for fruit/flowers.', ['To make carbohydrates only', 'To absorb sunlight', 'To make the soil acidic']),
    ('What is formed when an ammonium salt is warmed with an alkali?', 'ammonia gas', 'NH₄⁺ + OH⁻ → NH₃ + H₂O; this is why ammonium fertilisers should not be mixed with lime.', ['nitrogen gas', 'hydrogen gas', 'nitric acid']),
    ('State why farmers add fertilisers to soil.', 'To replace the elements (N, P, K) removed by crops and increase crop yield.', '[1]'),
])
t6b.fixed('C2', (2, 3, 4), [
    ('Explain why farmers should not spread lime (calcium hydroxide) on soil at the same time as ammonium fertilisers.', 'The alkali reacts with ammonium salts to release ammonia gas, so nitrogen is lost from the soil.', '[2]'),
    ('Explain why a farmer might choose ammonium phosphate rather than ammonium nitrate.', 'Ammonium phosphate supplies both nitrogen and phosphorus, whereas ammonium nitrate supplies only nitrogen.', '[2]'),
    ('Explain how overuse of fertilisers can harm rivers.', 'Excess soluble nitrates are washed into rivers, causing eutrophication and loss of oxygen for aquatic life.', '[2]'),
    ('Explain why fertilisers must be soluble in water.', 'Plants absorb the ions in solution through their roots.', '[1]'),
])


@t6b.add('C3', (1, 2, 3, 4), 'numerical')
def t6b_pctN(r, D):
    nm, f, el = r.choice([x for x in FERT if 'N' in x[2].split()])
    M = Mr(f)
    nN = atoms(f).get('N', 0)
    pct = nN * 14 / M * 100
    if D == 1:
        return nmcq(r, f'What is the relative formula mass of {nm}, {F(f)}?', M, [M - 14, M + 16, M * 2, M - 18], '', f'Mr {F(f)} = {mr(M)}.', f=mr)
    if D >= 4:
        a, b = r.sample([x for x in FERT if 'N' in x[2].split()], 2)
        pa = atoms(a[1])['N'] * 14 / Mr(a[1]) * 100; pb = atoms(b[1])['N'] * 14 / Mr(b[1]) * 100
        best = a if pa > pb else b
        return {'stem': f'A farmer must choose between {a[0]}, {F(a[1])}, and {b[0]}, {F(b[1])}, as a source of nitrogen. Calculate the percentage by mass of nitrogen in each and state which supplies more nitrogen per kilogram.',
                'answer': f'{a[0]} {g3(pa)}%; {b[0]} {g3(pb)}%; {best[0]}', 'key': f'Mr {mr(Mr(a[1]))} and {mr(Mr(b[1]))} [1]; % N each [2]; conclusion [1]', 'marks': 4}
    return {'stem': f'Calculate the percentage by mass of nitrogen in {nm}, {F(f)}.', 'answer': f'{g3(pct)}%', 'key': f'Mr = {mr(M)} [1]; % N = {nN} × 14/{mr(M)} × 100 = {g3(pct)}% [1]'}


@t6b.add('C3', (2, 3, 4, 5), 'numerical')
def t6b_make(r, D):
    nm, eq, acid, k = r.choice(FMAKE)
    f = eq.split('-> ')[1]
    mass_nh3 = r.choice([17, 34, 51, 68, 85, 170, 340])
    unit = r.choice(['kg', 'tonnes'])
    n = mass_nh3 / 17
    mp = n / k * Mr(f)
    return {'stem': f'{nm.capitalize()} is made by reacting ammonia with {acid}: {E(eq)}. Calculate the maximum mass of {nm} that can be made from {mass_nh3} {unit} of ammonia.',
            'answer': f'{g3(mp)} {unit}', 'key': f'n(NH₃) = {mass_nh3}/17 = {g3(n)} (k)mol [1]; ratio {k}:1 so n(salt) = {g3(n / k)} [1]; Mr = {mr(Mr(f))}, mass = {g3(mp)} {unit} [1]'}


@t6b.add('C1', (1, 2, 3))
def t6b_el(r, D):
    nm, f, el = r.choice(FERT)
    names = {'N': 'nitrogen', 'P': 'phosphorus', 'K': 'potassium'}
    corr = ' and '.join(names[x] for x in el.split(' and '))
    pool = ['nitrogen', 'phosphorus', 'potassium', 'nitrogen and phosphorus', 'potassium and nitrogen', 'phosphorus and potassium', 'nitrogen, phosphorus and potassium']
    corr = {'nitrogen and phosphorus': 'nitrogen and phosphorus', 'potassium and nitrogen': 'potassium and nitrogen'}.get(corr, corr)
    return mcq_q(r, f'Which of the elements N, P and K needed by plants does {nm}, {F(f)}, supply?', corr, pool, f'{F(f)} contains {corr}.')


def _fert_c4(r, D):
    nm, eq, acid, k = r.choice(FMAKE)
    f = eq.split('-> ')[1]
    M = Mr(f)
    pct = atoms(f)['N'] * 14 / M * 100
    bag = r.choice([25, 40, 50])
    intro = r.choice([f'A fertiliser factory in {city(r)} makes {nm} by reacting ammonia with {acid}.', f'{person(r)} prepares a sample of {nm} in the laboratory by titrating aqueous ammonia with {acid}.',
                      f'A farmer buys {bag} kg bags of {nm} fertiliser for a wheat field.'])
    parts = [
        lambda r: ('Write the balanced equation for the formation of the fertiliser.', E(eq), '[2]'),
        lambda r: (f'Calculate the percentage by mass of nitrogen in {nm}.', f'{g3(pct)}%', f'Mr = {mr(M)} [1]; % = {g3(pct)}% [1]; total [2]'),
        lambda r: (f'Calculate the mass of nitrogen in a {bag} kg bag.', f'{g3(bag * pct / 100)} kg', '[1]'),
        lambda r: ('Explain why this fertiliser should not be mixed with calcium hydroxide.', 'Calcium hydroxide is an alkali; it reacts with ammonium ions to release ammonia gas, losing nitrogen.', '[2]'),
        lambda r: ('State which other element(s) a farmer might need to add, and suggest a compound to supply it.', 'Potassium (e.g. potassium nitrate/sulfate)' + ('' if 'P' in f else ' and phosphorus (e.g. ammonium phosphate)') + '.', '[2]'),
        lambda r: ('Describe a test to show that the fertiliser contains ammonium ions.', 'Warm with aqueous sodium hydroxide: ammonia gas turns damp red litmus blue.', '[2]'),
        lambda r: ('Explain one environmental problem from overuse of this fertiliser.', 'Run-off into rivers causes eutrophication: algal growth, decay, oxygen depletion, death of aquatic life.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t6b.add('C4', (2, 3, 4, 5), 'multi_step')(_fert_c4)
t6b.add('C3', (3, 4), 'multi_step')(_fert_c4)

# ---------------------------------------------------------- 6.3 air
AIR = [('nitrogen', 78), ('oxygen', 21), ('argon', 0.9), ('carbon dioxide', 0.04)]
APOLL = [('carbon monoxide', 'incomplete combustion of carbon-containing fuels', 'toxic: it reduces the ability of the blood to carry oxygen'),
         ('sulfur dioxide', 'combustion of fossil fuels that contain sulfur compounds', 'acid rain, which damages buildings and kills trees and aquatic life'),
         ('oxides of nitrogen', 'reaction of nitrogen and oxygen at the high temperatures in car engines', 'acid rain, photochemical smog and respiratory problems'),
         ('particulates (fine solid particles)', 'incomplete combustion of carbon-containing fuels', 'increased risk of respiratory problems and cancer'),
         ('methane', 'decomposition of vegetation and waste gases from digestion in animals', 'climate change (greenhouse gas)'),
         ('carbon dioxide', 'complete combustion of carbon-containing fuels', 'climate change (greenhouse gas)')]

t6c = topic('Clean air and air pollutants', 'composition of clean, dry air', 'sources and effects of air pollutants', 'air pollutants')
t6c.fixed('C1', (1, 2), [
    ('What is the approximate percentage of oxygen in clean, dry air?', '21%', 'Air: about 78% N₂, 21% O₂, small amounts of noble gases (mainly Ar) and CO₂.', ['78%', '0.04%', '50%']),
    ('Which gas makes up about 78% of clean, dry air?', 'nitrogen', 'Nitrogen is the main component of air.', ['oxygen', 'argon', 'carbon dioxide']),
    ('Which pollutant is produced by the incomplete combustion of petrol?', 'carbon monoxide', 'Limited oxygen gives CO (and soot) instead of CO₂.', ['sulfur dioxide', 'argon', 'ozone only']),
    ('Why is carbon monoxide poisonous?', 'It reduces the ability of the blood to carry oxygen', 'CO combines with haemoglobin.', ['It causes acid rain', 'It is a greenhouse gas only', 'It dissolves in water to form an acid']),
    ('Which gas is formed in car engines from nitrogen and oxygen in the air?', 'nitrogen monoxide', 'High temperature in engines: N₂ + O₂ → 2NO.', ['carbon dioxide', 'sulfur dioxide', 'methane']),
    ('State the main source of sulfur dioxide in the atmosphere.', 'Burning fossil fuels that contain sulfur compounds.', '[1]'),
])
t6c.fixed('C2', (2, 3, 4), [
    ('Explain how oxides of nitrogen are formed in a car engine.', 'At the very high temperature in the engine, nitrogen and oxygen from the air react together.', '[2]'),
    ('Explain how sulfur dioxide causes damage to limestone buildings.', 'SO₂ dissolves in rainwater to form acid rain, which reacts with calcium carbonate in limestone.', '[2]'),
    ('Explain why incomplete combustion is more likely in a poorly ventilated room.', 'There is not enough oxygen, so carbon fuels form carbon monoxide and soot instead of carbon dioxide.', '[2]'),
    ('Explain why particulates are harmful to human health.', 'Fine particles are breathed deep into the lungs, increasing respiratory problems and the risk of cancer.', '[2]'),
])


@t6c.add('C1', (1, 2, 3))
def t6c_src(r, D):
    g, src, eff = r.choice(APOLL)
    if r.random() < 0.5:
        return mcq_q(r, f'What is the main source of {g} in the air?', src, [x[1] for x in APOLL if x[1] != src], f'{g}: {src}.')
    return mcq_q(r, f'What is the main harmful effect of {g}?', eff, list({x[2] for x in APOLL}), f'{g}: {eff}.')


@t6c.add('C2', (2, 3, 4), 'explain')
def t6c_explain(r, D):
    g, src, eff = r.choice(APOLL)
    if g == 'methane':
        place = r.choice(['a large cattle farm', f'a landfill site near {city(r)}', 'flooded rice paddies'])
    else:
        place = r.choice([f'a busy road in {city(r)}', f'a coal-fired power station near {city(r)}', 'a city centre during rush hour', 'an industrial estate'])
    return {'stem': f'Air near {place} is found to contain raised levels of {g}. Describe the likely source of this pollutant and explain one effect it has.',
            'answer': f'Source: {src}. Effect: {eff}.', 'key': '1 mark source; 1 mark effect; 1 mark explanation [3]', 'marks': 3}


@t6c.add('C3', (1, 2, 3, 4), 'numerical')
def t6c_vol(r, D):
    V = r.choice([100, 250, 500, 1000, 2400, 5000, 50])
    g, pc = r.choice(AIR[:3])
    if D == 1:
        return nmcq(r, f'Approximately what volume of {g} is present in {V} dm³ of clean, dry air?', V * pc / 100, [V * x / 100 for x in (78, 21, 0.9, 50) if x != pc], ' dm³', f'{pc}% of {V} dm³.')
    if D >= 3:
        start = r.choice([100, 80, 90, 60, 120])
        fin = start * 0.79
        return {'stem': f'{start} cm³ of air is passed repeatedly over heated copper in a sealed apparatus until the volume stops changing. The final volume (at room temperature) is {sf(fin)} cm³. Calculate the percentage of oxygen in the air and explain why the copper turns black.',
                'answer': f'{g3((start - fin) / start * 100)}%; the copper reacts with oxygen to form black copper(II) oxide.', 'key': f'volume of O₂ = {start} − {sf(fin)} = {sf(start - fin)} cm³ [1]; % = {g3((start - fin) / start * 100)}% [1]; 2Cu + O₂ → 2CuO [1]', 'marks': 3}
    return {'stem': f'Calculate the volume of {g} in a room containing {V} dm³ of clean, dry air.', 'answer': f'{sf(V * pc / 100)} dm³', 'key': f'{pc}/100 × {V} = {sf(V * pc / 100)} dm³ [1]', 'marks': 1}


@t6c.add('C3', (2, 3, 4, 5), 'numerical')
def t6c_so2(r, D):
    t = r.choice([100, 200, 500, 1000, 2000])
    s = r.choice([0.5, 1.0, 1.5, 2.0, 3.0, 2.5])
    mS = t * s / 100
    mSO2 = mS * 64 / 32
    if D >= 4:
        mCaO = mSO2 / 64 * 56
        return {'stem': f'A power station burns {t} tonnes of coal containing {s}% sulfur by mass. Calculate the mass of sulfur dioxide formed (S + O₂ → SO₂) and the mass of calcium oxide needed to remove it in a scrubber (CaO + SO₂ → CaSO₃).',
                'answer': f'{g3(mSO2)} t SO₂; {g3(mCaO)} t CaO', 'key': f'mass S = {g3(mS)} t [1]; SO₂ = {g3(mS)} × 64/32 = {g3(mSO2)} t [1]; CaO = {g3(mSO2)} × 56/64 = {g3(mCaO)} t [2]', 'marks': 4}
    return {'stem': f'Coal containing {s}% sulfur by mass is burned. Calculate the mass of sulfur dioxide produced from {t} tonnes of the coal. (S + O₂ → SO₂)', 'answer': f'{g3(mSO2)} tonnes',
            'key': f'mass S = {s}/100 × {t} = {g3(mS)} t [1]; 32 t S gives 64 t SO₂, so mass SO₂ = {g3(mSO2)} t [1]'}


def _air_c4(r, D):
    gs = r.sample(APOLL, 3)
    intro = r.choice([f'An air-quality station in {city(r)} measures the pollutants ' + ', '.join(g[0] for g in gs) + '.', f'{person(r)} is investigating air pollution near a motorway and a coal-fired power station.',
                      'A report compares the air in a quiet rural village with the air in a busy industrial city.'])
    parts = [
        lambda r: ('State the composition of clean, dry air.', '78% nitrogen, 21% oxygen, about 1% noble gases (mainly argon) and 0.04% carbon dioxide.', '[2]'),
        lambda r: (f'Describe the source of {gs[0][0]}.', cap(gs[0][1]) + '.', '[1]'),
        lambda r: (f'Explain one harmful effect of {gs[1][0]}.', cap(gs[1][2]) + '.', '[2]'),
        lambda r: ('Write an equation for the formation of carbon monoxide from the incomplete combustion of methane.', E('2CH4 + 3O2 -> 2CO + 4H2O'), '[2]'),
        lambda r: ('Write an equation for the formation of nitrogen monoxide in a car engine.', E('N2 + O2 -> 2NO'), '[1]'),
        lambda r: ('Suggest two ways of reducing the concentration of these pollutants in a city.', 'Catalytic converters; low-sulfur fuels / flue-gas desulfurisation; more public transport/electric vehicles; renewable energy.', '[2]'),
        lambda r: (f'Explain how {gs[2][0]} is linked to the source you would expect near a busy road.', cap(gs[2][1]) + '; traffic burns large amounts of fuel.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t6c.add('C4', (2, 3, 4, 5), 'multi_step')(_air_c4)
t6c.add('C3', (3, 4), 'multi_step')(_air_c4)

# ---------------------------------------------------------- 6.4 greenhouse, climate, catalytic converters
STRAT = [('planting trees', 'removes CO₂ by photosynthesis'), ('reducing livestock farming', 'reduces methane emissions'), ('using renewable energy such as wind and solar', 'reduces CO₂ from burning fossil fuels'),
         ('using hydrogen as a fuel', 'produces only water when it burns'), ('flue-gas desulfurisation with calcium oxide', 'removes sulfur dioxide from waste gases'),
         ('using catalytic converters', 'converts CO and NOₓ into CO₂ and N₂'), ('using low-sulfur fuels', 'produces less sulfur dioxide when the fuel burns')]
t6d = topic('Greenhouse gases and climate change', 'greenhouse gases, climate change and reducing pollution', 'catalytic converters and photosynthesis', 'climate change')
t6d.fixed('C1', (1, 2), [
    ('Which two gases are the main greenhouse gases linked to climate change?', 'carbon dioxide and methane', 'CO₂ and CH₄ absorb and re-emit thermal (infrared) energy.', ['oxygen and nitrogen', 'argon and helium', 'sulfur dioxide and hydrogen']),
    ('Which reaction occurs in a catalytic converter?', '2CO + 2NO → 2CO₂ + N₂', 'Pt/Rh catalyst: carbon monoxide and nitrogen monoxide react to form carbon dioxide and nitrogen.', ['2CO₂ → 2CO + O₂', 'N₂ + O₂ → 2NO', 'CH₄ + 2O₂ → CO₂ + 2H₂O']),
    ('What is the word equation for photosynthesis?', 'carbon dioxide + water → glucose + oxygen', 'Photosynthesis needs light and chlorophyll.', ['glucose + oxygen → carbon dioxide + water', 'carbon dioxide + oxygen → glucose + water', 'water + oxygen → glucose + carbon dioxide']),
    ('Which method reduces sulfur dioxide emissions from power stations?', 'flue-gas desulfurisation using calcium oxide', 'CaO (a base) reacts with acidic SO₂.', ['adding catalytic converters to chimneys', 'burning more coal', 'adding nitrogen to the fuel']),
    ('How do greenhouse gases cause the Earth to warm?', 'They absorb and re-emit thermal energy radiated from the Earth’s surface', 'Infrared radiation from the warm surface is absorbed and re-emitted back towards the Earth.', ['They reflect sunlight back into space', 'They destroy the ozone layer', 'They react with oxygen to release heat']),
    ('Give one source of methane in the atmosphere.', 'Decomposition of vegetation or waste gases from digestion in animals (e.g. cattle).', '[1]'),
])
t6d.fixed('C2', (2, 3, 4), [
    ('Explain how increased greenhouse gas emissions lead to climate change.', 'More CO₂/CH₄ absorbs and re-emits more thermal energy towards Earth, raising average temperatures, which changes weather patterns, melts ice and raises sea levels.', '[3]'),
    ('Explain why planting trees can help reduce climate change.', 'Trees remove carbon dioxide from the air by photosynthesis.', '[2]'),
    ('Explain why catalytic converters work only once the engine is warm.', 'The catalyst needs a high temperature to work effectively.', '[1]'),
    ('Explain why using hydrogen as a fuel in cars reduces pollution, but may not stop all CO₂ emissions.', 'Burning hydrogen gives only water; but hydrogen is often made using energy from fossil fuels.', '[2]'),
    ('Explain why photosynthesis and burning fossil fuels have opposite effects on the amount of carbon dioxide in the air.', 'Photosynthesis removes CO₂ to make glucose; combustion releases CO₂.', '[2]'),
])


@t6d.add('C1', (1, 2, 3))
def t6d_strat(r, D):
    s, why = r.choice(STRAT)
    return mcq_q(r, f'Which strategy reduces pollution because it {why}?', s, [x[0] for x in STRAT], f'{s}: {why}.')


@t6d.add('C2', (2, 3, 4), 'explain')
def t6d_strat2(r, D):
    a, b = r.sample(STRAT, 2)
    return {'stem': f'A government in {city(r)} is considering two policies: {a[0]} and {b[0]}. Explain how each would reduce pollution or climate change.',
            'answer': f'{cap(a[0])}: {a[1]}. {cap(b[0])}: {b[1]}.', 'key': '1 mark each policy explained, 1 mark linking to the specific pollutant/gas [3]', 'marks': 3}


@t6d.add('C3', (1, 2, 3, 4))
def t6d_eq(r, D):
    eqs = [('the catalytic converter removes carbon monoxide and nitrogen monoxide together', '2CO + 2NO -> 2CO2 + N2'), ('carbon monoxide is oxidised in a catalytic converter', '2CO + O2 -> 2CO2'),
           ('photosynthesis takes place', '6CO2 + 6H2O -> C6H12O6 + 6O2'), ('methane burns completely', 'CH4 + 2O2 -> CO2 + 2H2O'), ('sulfur dioxide is removed by calcium oxide', 'CaO + SO2 -> CaSO3'),
           ('nitrogen monoxide is converted back to its elements in a catalytic converter', '2NO -> N2 + O2')]
    d, eq = r.choice(eqs)
    if D == 1:
        return mcq_q(r, f'Which balanced equation shows the reaction when {d}?', E(eq), [E(x[1]) for x in eqs] + [E('CO + NO -> CO2 + N2'), E('6CO2 + 6H2O -> C6H12O6 + 3O2')], E(eq))
    return {'stem': f'Write the balanced symbol equation for the reaction when {d}.', 'answer': E(eq), 'key': 'formulae [1]; balanced [1]'}


@t6d.add('C3', (2, 3, 4, 5), 'numerical')
def t6d_photo(r, D):
    mg = r.choice([18, 36, 90, 180, 360, 45, 900])
    n = mg / 180
    if D >= 4:
        vco2 = n * 6 * 24
        return {'stem': f'A plant makes {mg} g of glucose by photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Calculate the volume of carbon dioxide removed from the air at r.t.p., in dm³, and the mass of oxygen released.',
                'answer': f'{g3(vco2)} dm³; {g3(n * 6 * 32)} g', 'key': f'n(glucose) = {mg}/180 = {g3(n)} mol [1]; n(CO₂) = {g3(6 * n)} mol, V = {g3(vco2)} dm³ [1]; n(O₂) = {g3(6 * n)} mol, mass = {g3(n * 192)} g [2]', 'marks': 4}
    return {'stem': f'Calculate the mass of carbon dioxide needed to make {mg} g of glucose by photosynthesis. 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'answer': f'{g3(n * 6 * 44)} g',
            'key': f'n(glucose) = {mg}/180 = {g3(n)} mol [1]; n(CO₂) = {g3(6 * n)} mol [1]; mass = {g3(6 * n)} × 44 = {g3(n * 264)} g [1]'}


@t6d.add('C3', (2, 3, 4), 'numerical')
def t6d_fuel(r, D):
    f = r.choice([('methane', 'CH4', 'CH4 + 2O2 -> CO2 + 2H2O', 1), ('octane', 'C8H18', '2C8H18 + 25O2 -> 16CO2 + 18H2O', 8), ('ethanol', 'C2H5OH', 'C2H5OH + 3O2 -> 2CO2 + 3H2O', 2), ('propane', 'C3H8', 'C3H8 + 5O2 -> 3CO2 + 4H2O', 3)])
    mkg = r.choice([1, 2, 5, 10, 16, 32, 40])
    mco2 = mkg / Mr(f[1]) * f[3] * 44
    return {'stem': f'Calculate the mass of carbon dioxide, in kg, released when {mkg} kg of {f[0]} burns completely. {E(f[2])}', 'answer': f'{g3(mco2)} kg',
            'key': f'Mr {F(f[1])} = {mr(Mr(f[1]))} [1]; 1 mol fuel → {f[3]} mol CO₂ [1]; mass = {mkg} × {f[3]} × 44/{mr(Mr(f[1]))} = {g3(mco2)} kg [1]'}


def _cc_c4(r, D):
    intro = r.choice([f'A car manufacturer in {city(r)} fits catalytic converters containing platinum and rhodium to all its petrol cars.', f'{person(r)} reads a report about rising carbon dioxide and methane levels in the atmosphere.',
                      'A city council plans to cut air pollution and greenhouse gas emissions over the next ten years.'])
    parts = [
        lambda r: ('Name two pollutants removed by a catalytic converter.', 'Carbon monoxide and oxides of nitrogen (also unburned hydrocarbons).', '[2]'),
        lambda r: ('Write the equation for the reaction between carbon monoxide and nitrogen monoxide in a catalytic converter.', E('2CO + 2NO -> 2CO2 + N2'), '[2]'),
        lambda r: ('Explain why catalytic converters do not reduce climate change.', 'They convert CO to CO₂, which is still a greenhouse gas.', '[2]'),
        lambda r: ('Explain how carbon dioxide causes the Earth’s temperature to rise.', 'It absorbs thermal (infrared) energy emitted by the Earth and re-emits it, some back towards the surface.', '[2]'),
        lambda r: ('State two effects of climate change.', 'Rising sea levels; melting ice caps; more extreme weather; changes in rainfall/crop growth; flooding; droughts.', '[2]'),
        lambda r: ('Suggest two strategies to reduce methane emissions.', 'Reduce livestock farming; capture methane from landfill; reduce food waste.', '[2]'),
        lambda r: ('Write the balanced equation for photosynthesis and explain how it affects the atmosphere.', E('6CO2 + 6H2O -> C6H12O6 + 6O2') + '; it removes CO₂ and adds O₂.', '[3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t6d.add('C4', (2, 3, 4, 5), 'multi_step')(_cc_c4)
t6d.add('C3', (3, 4), 'multi_step')(_cc_c4)

CHAPTERS[6] = [t6a, t6b, t6c, t6d]


# ===================================================================== Ch7 (CB18) Introduction to organic chemistry
PFX = {1: 'meth', 2: 'eth', 3: 'prop', 4: 'but', 5: 'pent', 6: 'hex', 7: 'hept', 8: 'oct', 9: 'non', 10: 'dec'}


def chain(n):
    return 'CH3' + 'CH2' * (n - 2) + 'CH3' if n > 1 else 'CH4'


COMP = []  # (name, series, molecular(ascii), structural(ascii), n carbons, functional group)
for _n in range(1, 7):
    COMP.append((f'{PFX[_n]}ane', 'alkane', f'C{_n}H{2 * _n + 2}'.replace('C1H', 'CH'), chain(_n), _n, 'C–C single bonds only'))
for _n, _s in ((2, 'CH2=CH2'), (3, 'CH2=CHCH3'), (4, 'CH2=CHCH2CH3')):
    COMP.append(({2: 'ethene', 3: 'propene', 4: 'but-1-ene'}[_n], 'alkene', f'C{_n}H{2 * _n}', _s, _n, 'C=C double bond'))
for _n, _s in ((1, 'CH3OH'), (2, 'CH3CH2OH'), (3, 'CH3CH2CH2OH'), (4, 'CH3CH2CH2CH2OH')):
    COMP.append(({1: 'methanol', 2: 'ethanol', 3: 'propan-1-ol', 4: 'butan-1-ol'}[_n], 'alcohol', f'C{_n}H{2 * _n + 1}OH'.replace('C1H', 'CH'), _s, _n, '–OH (hydroxyl)'))
for _n, _s in ((1, 'HCOOH'), (2, 'CH3COOH'), (3, 'CH3CH2COOH'), (4, 'CH3CH2CH2COOH')):
    COMP.append(({1: 'methanoic acid', 2: 'ethanoic acid', 3: 'propanoic acid', 4: 'butanoic acid'}[_n], 'carboxylic acid', f'C{_n}H{2 * _n}O2'.replace('C1H', 'CH'), _s, _n, '–COOH (carboxyl)'))
SERIES_INFO = {'alkane': ('CnH2n+2', '-ane', 'C–C single bonds only'), 'alkene': ('CnH2n', '-ene', 'C=C double bond'), 'alcohol': ('CnH2n+1OH', '-ol', '–OH'),
               'carboxylic acid': ('CnH2n+1COOH', '-oic acid', '–COOH'), 'ester': ('—', '-yl -oate', '–COO–')}
COMP4 = [c for c in COMP if c[4] <= 4]


def Fs(s):
    return F(s)


t7a = topic('Organic formulae', 'organic formulae: molecular, general, structural and displayed formulae', 'molecular general structural displayed', 'organic formulae')
t7a.fixed('C1', (1, 2), [
    ('What does a displayed formula show?', 'Every atom and every bond in the molecule', 'Displayed formula: all atoms and all covalent bonds drawn.', ['Only the number of each type of atom', 'The simplest whole-number ratio of atoms', 'Only the functional group']),
    ('What is the general formula of the alkanes?', 'CₙH₂ₙ₊₂', 'Alkanes: CₙH₂ₙ₊₂ (e.g. C₃H₈).', ['CₙH₂ₙ', 'CₙH₂ₙ₊₁OH', 'CₙH₂ₙ₋₂']),
    ('Which is the structural formula of ethanol?', 'CH₃CH₂OH', 'Structural formula shows the arrangement of atoms group by group.', ['C₂H₆O', 'CH₃OH', 'CH₃COOH']),
    ('What is the molecular formula of propane?', 'C₃H₈', 'Propane: 3 carbons, CₙH₂ₙ₊₂ → C₃H₈.', ['C₃H₆', 'C₃H₇OH', 'C₄H₁₀']),
    ('Which term describes the formula CH₂ for ethene, C₂H₄?', 'empirical formula', 'Empirical formula = simplest whole-number ratio of atoms.', ['molecular formula', 'structural formula', 'displayed formula']),
    ('State what is meant by the molecular formula of a compound.', 'The number and type of each atom in one molecule.', '[1]'),
])
t7a.fixed('C2', (2, 3, 4), [
    ('Explain the difference between a molecular formula and a structural formula, using ethanol as the example.', 'Molecular C₂H₆O shows only numbers of atoms; structural CH₃CH₂OH shows how the atoms are grouped/arranged.', '[2]'),
    ('Explain why the general formula of an alkene is CₙH₂ₙ while that of an alkane is CₙH₂ₙ₊₂.', 'The C=C double bond uses two bonding electrons per carbon that would otherwise bond to hydrogen, so an alkene has two fewer H atoms.', '[2]'),
    ('Explain why one carbon atom in a displayed formula always has four bonds drawn.', 'Carbon has four outer electrons and forms four covalent bonds.', '[1]'),
    ('Explain why two different compounds can have the same empirical formula, giving an example.', 'The empirical formula is only the simplest ratio; e.g. ethene C₂H₄ and propene C₃H₆ are both CH₂.', '[2]'),
])


def emp(f):
    a = atoms(f)
    g = 0
    for v in a.values():
        g = math.gcd(g, v)
    order = ['C', 'H', 'O', 'N', 'Cl', 'Br']
    return ''.join(f'{el}{a[el] // g if a[el] // g > 1 else ""}' for el in order if el in a)


def molf(c):
    """Molecular formula in CxHyOz order."""
    a = atoms(c[2])
    return ''.join(f'{el}{a[el] if a[el] > 1 else ""}' for el in ('C', 'H', 'O') if el in a)


@t7a.add('C1', (1, 2, 3))
def t7a_mol(r, D):
    c = r.choice(COMP)
    corr = F(molf(c))
    a = atoms(c[2])
    pool = [F(molf(x)) for x in COMP if molf(x) != molf(c) and abs(x[4] - c[4]) <= 1] + [F(f'C{a["C"]}H{a["H"] + d}' + (f'O{a["O"]}' if 'O' in a else '')) for d in (-2, 2, 1)]
    return mcq_q(r, f'The structural formula of a compound is {F(c[3])}. What is its molecular formula?', corr, pool, f'{c[0]}: count the atoms — {corr}.')


@t7a.add('C3', (1, 2, 3, 4))
def t7a_count(r, D):
    c = r.choice(COMP)
    a = atoms(c[2])
    M = Mr(c[2])
    if D == 1:
        return nmcq(r, f'What is the relative molecular mass of {c[0]}, {F(c[3])}?', M, [M + 2, M - 2, M + 14, M - 14], '', f'Mr = ' + ' + '.join(f'{a[el]} × {AR[el]}' for el in a) + f' = {mr(M)}.', f=mr)
    e = emp(c[2])
    if D >= 3:
        return {'stem': f'For {c[0]}, {F(c[3])}: (a) write the molecular formula, (b) write the empirical formula, (c) calculate the relative molecular mass.',
                'answer': f'(a) {F(molf(c))} (b) {F(e)} (c) {mr(M)}', 'key': '(a) [1] (b) [1] (c) [1]', 'marks': 3}
    return {'stem': f'State the molecular formula of {c[0]} and calculate its relative molecular mass.', 'answer': f'{F(molf(c))}; {mr(M)}', 'key': '1 mark formula; 1 mark Mr [2]'}


@t7a.add('C3', (2, 3, 4, 5), 'numerical')
def t7a_emp(r, D):
    c = r.choice([x for x in COMP if x[1] in ('alkane', 'alkene')] + [('cyclohexane', 'x', 'C6H12', '', 6, ''), ('benzene', 'x', 'C6H6', '', 6, ''), ('glucose', 'x', 'C6H12O6', '', 6, '')])
    a = atoms(c[2])
    M = Mr(c[2])
    pct = {el: a[el] * AR[el] / M * 100 for el in a}
    e = emp(c[2])
    pc = ', '.join(f'{el} {pct[el]:.1f}%' for el in ('C', 'H', 'O') if el in pct)
    if D >= 4:
        return {'stem': f'{"A hydrocarbon" if "O" not in a else "An organic compound"} contains, by mass, {pc}. Its relative molecular mass is {mr(M)}. Calculate its empirical formula and deduce its molecular formula.',
                'answer': f'Empirical {F(e)}; molecular {F(molf(c))}', 'key': f'divide each % by Ar [1]; divide by smallest to get ratio [1]; empirical {F(e)} (Mr {mr(Mr(e))}) [1]; {mr(M)}/{mr(Mr(e))} = {int(round(M / Mr(e)))} so {F(molf(c))} [1]', 'marks': 4}
    return {'stem': f'A compound contains {pc} by mass. Calculate its empirical formula.', 'answer': F(e), 'key': '% ÷ Ar for each element [1]; simplest ratio [1]; formula [1]'}


@t7a.add('C2', (2, 3, 4), 'explain')
def t7a_disp(r, D):
    c = r.choice([x for x in COMP4 if x[4] >= 2])
    a = atoms(c[2])
    nC, nH, nO = a.get('C', 0), a.get('H', 0), a.get('O', 0)
    bonds = {'alkane': f'{nC - 1} C–C and {nH} C–H single bonds', 'alkene': f'one C=C double bond, {nC - 2} C–C single bond(s) and {nH} C–H bonds',
             'alcohol': f'{nC - 1} C–C, {nH - 1} C–H, one C–O and one O–H bond', 'carboxylic acid': f'{nC - 1} C–C, {nH - 1} C–H, one C=O, one C–O and one O–H bond'}[c[1]]
    return {'stem': f'Describe the displayed formula of {c[0]}, {F(c[3])}, stating the number and type of each bond that would be drawn.',
            'answer': f'All atoms shown with every bond: {bonds}; each C has four bonds' + ('; O has two bonds.' if nO else '.'), 'key': '1 mark all bonds shown (each C four bonds); 1 mark correct bond counts [2]'}


def _form_c4(r, D):
    c = r.choice([x for x in COMP4 if x[4] >= 2])
    a = atoms(c[2])
    M = Mr(c[2])
    intro = r.choice([f'A bottle in {lab(r)} is labelled "{c[0]}, {F(c[3])}".', f'{person(r)} is given the structural formula {F(c[3])} for an organic compound.', f'An organic compound X has the structural formula {F(c[3])}.'])
    parts = [
        lambda r: ('Write the molecular formula.', F(molf(c)), '[1]'),
        lambda r: ('Write the empirical formula.', F(emp(c[2])), '[1]'),
        lambda r: ('Name the homologous series and the functional group.', f'{c[1]}; {c[5]}', '[2]'),
        lambda r: ('State the general formula of this homologous series.', F(SERIES_INFO[c[1]][0].replace('n+1', 'N').replace('2n', '2M')).replace('N', 'ₙ₊₁').replace('M', 'ₙ').replace('Cn', 'Cₙ') if False else SERIES_INFO[c[1]][0].replace('CnH2n+2', 'CₙH₂ₙ₊₂').replace('CnH2n+1OH', 'CₙH₂ₙ₊₁OH').replace('CnH2n+1COOH', 'CₙH₂ₙ₊₁COOH').replace('CnH2n', 'CₙH₂ₙ'), '[1]'),
        lambda r: ('Calculate the relative molecular mass.', mr(M), '[1]'),
        lambda r: ('Describe what the displayed formula would show.', 'Every atom and every covalent bond; each carbon with four bonds.', '[1]'),
        lambda r: ('Calculate the percentage by mass of carbon.', f'{g3(a["C"] * 12 / M * 100)}%', '[2]'),
        lambda r: ('Name the next member of the same homologous series and give its formula.', f'{name_of(c[1], c[4] + 1)}, {F(gen_formula(c[1], c[4] + 1))}', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t7a.add('C4', (2, 3, 4, 5), 'multi_step')(_form_c4)
t7a.add('C3', (3, 4), 'multi_step')(_form_c4)

# ---------------------------------------------------------- 7.2 naming
ESTERS = []
for _ac, _an in (('HCOOH', 'methanoic acid'), ('CH3COOH', 'ethanoic acid'), ('CH3CH2COOH', 'propanoic acid')):
    for _al, _aln in (('CH3OH', 'methanol'), ('CH3CH2OH', 'ethanol'), ('CH3CH2CH2OH', 'propan-1-ol')):
        an = {'methanol': 'methyl', 'ethanol': 'ethyl', 'propan-1-ol': 'propyl'}[_aln] + ' ' + _an.replace('oic acid', 'oate')
        R = _ac[:-4] if _ac != 'HCOOH' else 'H'
        Rp = {'CH3OH': 'CH3', 'CH3CH2OH': 'CH2CH3', 'CH3CH2CH2OH': 'CH2CH2CH3'}[_al]
        ESTERS.append((an, f'{R}COO{Rp}', _an, _aln))

t7b = topic('Naming organic compounds', 'naming organic compounds from functional groups and chain length', 'up to four carbons', 'naming')
t7b.fixed('C1', (1, 2), [
    ('What is the name of CH₃CH₂CH₃?', 'propane', '3 carbons = prop-; single bonds only = -ane.', ['propene', 'ethane', 'butane']),
    ('Which prefix shows a chain of four carbon atoms?', 'but-', 'meth- 1, eth- 2, prop- 3, but- 4.', ['prop-', 'pent-', 'eth-']),
    ('What is the functional group of the alcohols?', '–OH', 'Alcohols contain the hydroxyl group –OH; names end in -ol.', ['–COOH', 'C=C', '–COO–']),
    ('Which compound is a carboxylic acid?', 'CH₃COOH', 'Carboxylic acids contain –COOH; CH₃COOH is ethanoic acid.', ['CH₃CH₂OH', 'CH₃COOCH₃', 'CH₂=CH₂']),
    ('What is the name of the ester formed from ethanol and ethanoic acid?', 'ethyl ethanoate', 'Alcohol part → "-yl", acid part → "-oate".', ['ethanoic ethanol', 'ethyl ethanol', 'diethyl ester']),
    ('State the suffix used in the names of alkenes.', '-ene', '[1]'),
])
t7b.fixed('C2', (2, 3, 4), [
    ('Explain how the name "propan-1-ol" describes the structure of the molecule.', 'prop- = 3 carbons; -an- = single C–C bonds; -1-ol = –OH group on the first carbon atom.', '[3]'),
    ('Explain why there is no compound called "methene".', 'An alkene needs a C=C double bond, which requires at least two carbon atoms.', '[2]'),
    ('Explain why ethanoic acid and ethanol have similar names but different properties.', 'Both have two carbons (eth-) but different functional groups (–COOH and –OH), which determine their chemical properties.', '[2]'),
    ('A student names CH₃COOCH₂CH₃ as "ethyl methanoate". Explain the error and give the correct name.', 'The acid part CH₃COO– has two carbons (ethanoate) and the alcohol part –CH₂CH₃ is ethyl: ethyl ethanoate.', '[2]'),
])


@t7b.add('C1', (1, 2, 3))
def t7b_name(r, D):
    c = r.choice(COMP4)
    pool = [x[0] for x in COMP4 if x[0] != c[0] and (x[4] == c[4] or x[1] == c[1])]
    return mcq_q(r, f'What is the name of the compound with the structural formula {F(c[3])}?', c[0], pool, f'{c[4]} carbon(s) → {PFX[c[4]]}-; {c[5]} → {c[1]}: {c[0]}.')


@t7b.add('C3', (1, 2, 3, 4))
def t7b_fromname(r, D):
    c = r.choice(COMP4)
    if D == 1:
        pool = [F(x[3]) for x in COMP4 if x[0] != c[0]]
        return mcq_q(r, f'Which is the structural formula of {c[0]}?', F(c[3]), pool, f'{c[0]}: {F(c[3])}.')
    return {'stem': f'Give the structural formula of {c[0]} and identify its functional group and homologous series.', 'answer': f'{F(c[3])}; {c[5]}; {c[1]}', 'key': '1 mark formula; 1 mark functional group; 1 mark series [3]', 'marks': 3}


@t7b.add('C3', (2, 3, 4, 5))
def t7b_ester(r, D):
    nm, f, acid, alc = r.choice(ESTERS)
    if D == 2:
        return mcq_q(r, f'What is the name of the ester formed from {alc} and {acid}?', nm, [e[0] for e in ESTERS], f'alcohol → "-yl" ({nm.split()[0]}), acid → "-oate" ({nm.split()[1]}).')
    if D >= 4:
        return {'stem': f'An ester has the structural formula {F(f)}. Name the ester and the alcohol and carboxylic acid from which it was made.', 'answer': f'{nm}; {alc} and {acid}',
                'key': '1 mark ester name; 1 mark alcohol; 1 mark acid [3]', 'marks': 3}
    return {'stem': f'Name, and give the structural formula of, the ester made from {alc} and {acid}.', 'answer': f'{nm}; {F(f)}', 'key': '1 mark name; 1 mark formula [2]'}


@t7b.add('C2', (2, 3, 4), 'explain')
def t7b_err(r, D):
    c = r.choice([x for x in COMP4 if x[4] >= 2])
    wrong = r.choice([x for x in COMP4 if x[0] != c[0] and (x[4] == c[4] or x[1] == c[1])])
    return {'stem': f'{person(r)} names {F(c[3])} as "{wrong[0]}". Explain the mistake and give the correct name.',
            'answer': f'Correct name: {c[0]}. ' + (f'The chain has {c[4]} carbon atoms ({PFX[c[4]]}-), not {wrong[4]}.' if wrong[4] != c[4] else f'The functional group is {c[5]}, so it is {art(c[1])}, not {art(wrong[1])}.'),
            'key': '1 mark identifies error (chain length or functional group); 1 mark correct name [2]'}


def _name_c4(r, D):
    cs = r.sample(COMP4, 4)
    L = 'ABCD'
    intro = 'Four organic compounds are: ' + '; '.join(f'{L[i]} {F(c[3])}' for i, c in enumerate(cs)) + '.'
    parts = [
        lambda r: ('Name each compound.', '; '.join(f'{L[i]} {c[0]}' for i, c in enumerate(cs)), '1 mark each, max [4]'),
        lambda r: ('Which compounds are in the same homologous series, if any?', '; '.join(' and '.join(L[i] for i, c in enumerate(cs) if c[1] == ser) + f' ({ser}s)' for ser in dict.fromkeys(c[1] for c in cs) if sum(1 for c in cs if c[1] == ser) > 1) or 'none', '[1]'),
        lambda r: ('Which compound(s) would turn aqueous bromine from orange to colourless?', ', '.join(L[i] for i, c in enumerate(cs) if c[1] == 'alkene') or 'none', 'alkenes only [1]'),
        lambda r: ('Which compound(s) would react with sodium carbonate to give carbon dioxide?', ', '.join(L[i] for i, c in enumerate(cs) if c[1] == 'carboxylic acid') or 'none', 'carboxylic acids [1]'),
        lambda r: ('Give the functional group of compound ' + L[0] + '.', cs[0][5], '[1]'),
        lambda r: ('Give the molecular formula of compound ' + L[1] + '.', F(molf(cs[1])), '[1]'),
        lambda r: ((lambda e: (f'Name the ester that could be made from {e[3]} and {e[2]}, and give its structural formula.', f'{e[0]}; {F(e[1])}', '[2]'))(next(e for e in ESTERS if e[3] in [c[0] for c in cs] and e[2] in [c[0] for c in cs]))
                   if any(e[3] in [c[0] for c in cs] and e[2] in [c[0] for c in cs] for e in ESTERS) else None),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t7b.add('C4', (2, 3, 4, 5), 'multi_step')(_name_c4)
t7b.add('C3', (3, 4), 'multi_step')(_name_c4)

# ---------------------------------------------------------- 7.3 homologous series
BP = {'alkane': [('methane', -162), ('ethane', -89), ('propane', -42), ('butane', -1), ('pentane', 36), ('hexane', 69), ('heptane', 98)],
      'alcohol': [('methanol', 65), ('ethanol', 78), ('propan-1-ol', 97), ('butan-1-ol', 117), ('pentan-1-ol', 138), ('hexan-1-ol', 157)]}
t7c = topic('Homologous series', 'homologous series and their general characteristics', 'homologous series', 'general characteristics')
t7c.fixed('C1', (1, 2), [
    ('Which statement describes members of a homologous series?', 'They have the same general formula and similar chemical properties', 'Homologous series: same functional group and general formula, similar chemical properties, trend in physical properties.', ['They have the same molecular formula', 'They have identical boiling points', 'They have different functional groups']),
    ('By what group of atoms do consecutive members of a homologous series differ?', 'CH₂', 'Each member has one more CH₂ than the previous one.', ['CH₃', 'C₂H₄', 'H₂']),
    ('How does the boiling point change as the chain length increases in the alkanes?', 'It increases', 'Larger molecules have stronger intermolecular forces.', ['It decreases', 'It stays the same', 'It falls then rises']),
    ('What is the molecular formula of the fifth member of the alkanes?', 'C₅H₁₂', 'CₙH₂ₙ₊₂ with n = 5.', ['C₅H₁₀', 'C₄H₁₀', 'C₅H₁₁OH']),
    ('State one general characteristic of a homologous series.', 'Same general formula / same functional group / similar chemical properties / trend in physical properties / differ by CH₂.', '[1]'),
])
t7c.fixed('C2', (2, 3, 4), [
    ('Explain why the members of a homologous series have similar chemical properties.', 'They have the same functional group, which determines how they react.', '[2]'),
    ('Explain why the boiling points of alkanes increase as the number of carbon atoms increases.', 'Larger molecules have stronger intermolecular forces of attraction, so more energy is needed to separate them.', '[2]'),
    ('Explain why methane is a gas but hexane is a liquid at room temperature.', 'Hexane molecules are larger, with stronger intermolecular forces, so its boiling point (69 °C) is above room temperature; methane’s is −162 °C.', '[2]'),
    ('Ethanol and propan-1-ol are in the same homologous series. Explain what this means.', 'They have the same general formula (CₙH₂ₙ₊₁OH), the same –OH functional group and similar chemical properties; they differ by CH₂.', '[2]'),
])


def name_of(series, n):
    p = PFX[n]
    return {'alkane': f'{p}ane', 'alkene': f'{p}ene' if n <= 3 else f'{p}-1-ene', 'alcohol': f'{p}anol' if n <= 2 else f'{p}an-1-ol', 'carboxylic acid': f'{p}anoic acid'}[series]


def gen_formula(series, n):
    if series == 'alkane':
        return f'C{n}H{2 * n + 2}'
    if series == 'alkene':
        return f'C{n}H{2 * n}'
    if series == 'alcohol':
        return f'C{n}H{2 * n + 1}OH'
    return f'C{n - 1}H{2 * n - 1}COOH' if n > 1 else 'HCOOH'


@t7c.add('C3', (1, 2, 3, 4))
def t7c_gen(r, D):
    s = r.choice(['alkane', 'alkene', 'alcohol', 'carboxylic acid'])
    n = r.choice([5, 6, 7, 8, 10, 12, 15, 20]) if D >= 2 else r.choice([5, 6, 7, 8])
    f = gen_formula(s, n).replace('C1H', 'CH')
    if D == 1:
        pool = [F(gen_formula(x, n).replace('C1H', 'CH')) for x in ('alkane', 'alkene', 'alcohol', 'carboxylic acid') if x != s] + [F(gen_formula(s, n + 1).replace('C1H', 'CH'))]
        return mcq_q(r, f'A member of the {s}s contains {n} carbon atoms. What is its formula?', F(f), pool, f'General formula {SERIES_INFO[s][0]} → {F(f)}.')
    M = Mr(f)
    return {'stem': f'Use the general formula of the {s}s to write the formula of the member with {n} carbon atoms and calculate its relative molecular mass.', 'answer': f'{F(f)}; Mr = {mr(M)}',
            'key': f'{SERIES_INFO[s][0]} with n = {n if s != "carboxylic acid" else n - 1} [1]; Mr {mr(M)} [1]'}


@t7c.add('C3', (2, 3, 4))
def t7c_bp(r, D):
    s = r.choice(list(BP))
    data = BP[s]
    k = r.randrange(3, len(data))
    known = data[:k]
    tgt = data[k]
    lo, hi = known[-1][1] + 10, known[-1][1] + 35
    tbl = neg('; '.join(f'{a} {b} °C' for a, b in known))
    return {'stem': f'The boiling points of some {s}s are: {tbl}. Predict the boiling point of {tgt[0]} and explain the trend.',
            'answer': neg(f'About {tgt[1]} °C (accept {lo} to {hi} °C)') + '; boiling point increases as the chain gets longer because intermolecular forces get stronger.', 'key': '1 mark prediction in range; 1 mark trend explained [2]'}


@t7c.add('C2', (2, 3, 4), 'explain')
def t7c_same(r, D):
    a, b = r.sample(COMP4, 2)
    same = a[1] == b[1]
    return {'stem': f'Deduce whether {a[0]}, {F(a[3])}, and {b[0]}, {F(b[3])}, belong to the same homologous series. Explain your answer.',
            'answer': ('Yes: ' if same else 'No: ') + (f'both are {a[1]}s with the same functional group ({a[5]}) and general formula.' if same else f'{a[0]} is {art(a[1])} ({a[5]}) but {b[0]} is {art(b[1])} ({b[5]}).'),
            'key': '1 mark conclusion; 1 mark functional group/general formula reasoning [2]'}


def _hs_c4(r, D):
    s = r.choice(list(BP))
    data = BP[s]
    pts = data[:5]
    tbl = neg('; '.join(f'{a} {b} °C' for a, b in pts))
    intro = f'A student plots the boiling points of the first five {s}s against the number of carbon atoms. Data: {tbl}.'
    nxt = data[5]
    parts = [
        lambda r: (f'State the general formula of the {s}s.', SERIES_INFO[s][0].replace('CnH2n+2', 'CₙH₂ₙ₊₂').replace('CnH2n+1OH', 'CₙH₂ₙ₊₁OH'), '[1]'),
        lambda r: ('Describe the trend shown.', 'Boiling point increases as the number of carbon atoms increases.', '[1]'),
        lambda r: ('Explain the trend.', 'Larger molecules have stronger intermolecular forces, needing more energy to separate.', '[2]'),
        lambda r: (f'Predict the boiling point of {nxt[0]}.', neg(f'About {nxt[1]} °C'), 'value continuing trend ±15 °C [1]'),
        lambda r: ('Which of these compounds are gases at 25 °C?', ', '.join(a for a, b in pts if b < 25) or 'none', '[1]'),
        lambda r: (f'Give two other characteristics of a homologous series.', 'Same functional group; similar chemical properties; differ by CH₂; same general formula.', '[2]'),
        lambda r: (f'Write the molecular formula of {nxt[0]}.', F(gen_formula(s, 6)), '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t7c.add('C4', (2, 3, 4, 5), 'case')(_hs_c4)
t7c.add('C3', (3, 4), 'case')(_hs_c4)

# ---------------------------------------------------------- 7.4 isomers
ISO = {'C4H10': [('butane', 'CH3CH2CH2CH3'), ('methylpropane', 'CH3CH(CH3)CH3')],
       'C5H12': [('pentane', 'CH3CH2CH2CH2CH3'), ('2-methylbutane', 'CH3CH(CH3)CH2CH3'), ('2,2-dimethylpropane', 'C(CH3)4')],
       'C4H8': [('but-1-ene', 'CH2=CHCH2CH3'), ('but-2-ene', 'CH3CH=CHCH3'), ('methylpropene', 'CH2=C(CH3)CH3')],
       'C3H8O': [('propan-1-ol', 'CH3CH2CH2OH'), ('propan-2-ol', 'CH3CH(OH)CH3')],
       'C4H10O': [('butan-1-ol', 'CH3CH2CH2CH2OH'), ('butan-2-ol', 'CH3CH(OH)CH2CH3'), ('2-methylpropan-1-ol', '(CH3)2CHCH2OH')],
       'C2H4O2': [('ethanoic acid', 'CH3COOH'), ('methyl methanoate', 'HCOOCH3')],
       'C3H6O2': [('propanoic acid', 'CH3CH2COOH'), ('methyl ethanoate', 'CH3COOCH3'), ('ethyl methanoate', 'HCOOCH2CH3')]}
ISO_ALL = [(mf, n, s) for mf, lst in ISO.items() for n, s in lst]

t7d = topic('Structural isomers', 'structural isomers: same molecular formula, different structural formula', 'structural isomers', 'isomerism')
t7d.fixed('C1', (1, 2), [
    ('What are structural isomers?', 'Compounds with the same molecular formula but different structural formulae', 'Isomers: same atoms, arranged differently.', ['Compounds with the same structural formula but different molecular formulae', 'Atoms of the same element with different numbers of neutrons', 'Compounds in the same homologous series']),
    ('Which pair are structural isomers?', 'butane and methylpropane', 'Both are C₄H₁₀.', ['butane and propane', 'ethene and ethane', 'methane and methanol']),
    ('How many structural isomers have the molecular formula C₅H₁₂?', '3', 'pentane, 2-methylbutane, 2,2-dimethylpropane.', ['2', '4', '5']),
    ('Which compound is an isomer of propan-1-ol?', 'propan-2-ol', 'Both C₃H₈O; the –OH is on a different carbon.', ['propane', 'propanoic acid', 'ethanol']),
    ('State what is the same and what is different for a pair of structural isomers.', 'Same molecular formula; different structural formula (arrangement of atoms).', '[2]'),
])
t7d.fixed('C2', (2, 3, 4), [
    ('Explain why butane and methylpropane have different boiling points even though they have the same molecular formula.', 'They have different structures; the branched methylpropane has a smaller surface contact between molecules, so weaker intermolecular forces and a lower boiling point.', '[2]'),
    ('Explain why there are no isomers of propane.', 'Three carbon atoms can only be joined in one way in a chain; any other drawing is the same molecule.', '[2]'),
    ('Explain why ethanoic acid and methyl methanoate are isomers but belong to different homologous series.', 'Both are C₂H₄O₂ (same molecular formula) but have different functional groups: –COOH (acid) and –COO– (ester).', '[2]'),
    ('A student draws CH₃CH₂CH₂CH₃ and CH₂(CH₃)CH₂CH₃ and says they are isomers. Explain why the student is wrong.', 'Both are the same straight chain of four carbons (butane); bending the chain does not change the structure.', '[2]'),
])


@t7d.add('C1', (1, 2, 3))
def t7d_pair(r, D):
    mf = r.choice(list(ISO))
    a, b = r.sample(ISO[mf], 2)
    corr = f'{a[0]} and {b[0]}'
    wrong = []
    for _ in range(20):
        x, y = r.sample(ISO_ALL, 2)
        if x[0] != y[0] and x[1] != y[1] and f'{x[1]} and {y[1]}' not in wrong:
            wrong.append(f'{x[1]} and {y[1]}')
    return mcq_q(r, 'Which pair of compounds are structural isomers?', corr, wrong, f'Both have the molecular formula {F(mf)}.')


@t7d.add('C3', (2, 3, 4))
def t7d_draw(r, D):
    mf = r.choice([k for k in ISO if len(ISO[k]) >= 2])
    a = r.choice(ISO[mf])
    others = [x for x in ISO[mf] if x != a]
    if D >= 4:
        return {'stem': f'Give the structural formulae and names of all the structural isomers with the molecular formula {F(mf)} that are listed in the coursebook ({len(ISO[mf])} in total).',
                'answer': '; '.join(f'{n}: {F(s)}' for n, s in ISO[mf]), 'key': f'1 mark per correct isomer, max [{len(ISO[mf])}]', 'marks': len(ISO[mf])}
    return {'stem': f'{a[0].capitalize()} has the structural formula {F(a[1])}. Give the name and structural formula of one structural isomer of {a[0]}.',
            'answer': '; '.join(f'{n}: {F(s)}' for n, s in others) + ' (any one)', 'key': '1 mark correct structural formula; 1 mark name [2]'}


@t7d.add('C2', (2, 3, 4), 'explain')
def t7d_check(r, D):
    x, y = r.sample(ISO_ALL, 2)
    same = x[0] == y[0]
    return {'stem': f'Deduce whether {x[1]}, {F(x[2])}, and {y[1]}, {F(y[2])}, are structural isomers. Explain your answer.',
            'answer': (f'Yes: both have the molecular formula {F(x[0])} but different structures.' if same else f'No: their molecular formulae differ ({F(x[0])} and {F(y[0])}).'),
            'key': '1 mark molecular formulae compared; 1 mark conclusion [2]'}


def _iso_c4(r, D):
    mf = r.choice([k for k in ISO if len(ISO[k]) >= 2])
    lst = ISO[mf]
    a = lst[0]
    intro = r.choice([f'Compounds P and Q both have the molecular formula {F(mf)}. P is {F(lst[0][1])} and Q is {F(lst[1][1])}.', f'{person(r)} builds molecular models of compounds with the formula {F(mf)}.',
                      f'A chemist in {city(r)} separates two liquids, both with molecular formula {F(mf)}, from a mixture.'])
    parts = [
        lambda r: ('Define the term structural isomers.', 'Compounds with the same molecular formula but different structural formulae.', '[2]'),
        lambda r: (f'Name the compound {F(lst[0][1])}.', lst[0][0], '[1]'),
        lambda r: (f'Give the structural formula of {lst[1][0]}.', F(lst[1][1]), '[1]'),
        lambda r: (f'Calculate the relative molecular mass of {F(mf)}.', mr(Mr(mf)), '[1]'),
        lambda r: (f'State the total number of structural isomers with formula {F(mf)} that are listed in the coursebook and name any not already given.', f'{len(lst)}: ' + ', '.join(x[0] for x in lst), '[2]'),
        lambda r: ('Suggest why the isomers can be separated by fractional distillation.', 'Different structures give different boiling points.', '[1]'),
        lambda r: ('State whether the isomers have the same functional group, and what this means for their chemical properties.', ('Not necessarily: here one is a carboxylic acid (–COOH) and the other an ester (–COO–), so their chemical properties are different.' if mf in ('C2H4O2', 'C3H6O2') else 'Yes: they are in the same homologous series with the same functional group, so their chemical properties are similar (physical properties such as boiling point differ).'), '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t7d.add('C4', (2, 3, 4, 5), 'multi_step')(_iso_c4)
t7d.add('C3', (3, 4), 'multi_step')(_iso_c4)

CHAPTERS[7] = [t7a, t7b, t7c, t7d]


# ===================================================================== Ch8 (CB19) Reactions of organic compounds
def frac(x):
    return str(int(x)) if x == int(x) else f'{int(2 * x)}/2'


def comb_eq(series, n):
    """Balanced complete-combustion equation (smallest whole numbers)."""
    if series == 'alkane':
        f, h, o = f'C{n}H{2 * n + 2}', n + 1, (3 * n + 1) / 2
    elif series == 'alkene':
        f, h, o = f'C{n}H{2 * n}', n, 3 * n / 2
    else:  # alcohol
        f, h, o = f'C{n}H{2 * n + 1}OH', n + 1, 3 * n / 2
    f = f.replace('C1H', 'CH')
    k = 1 if o == int(o) else 2
    def co(c, sp):
        c = int(c)
        return (str(c) if c > 1 else '') + sp
    return f'{co(k, f)} + {co(o * k, "O2")} -> {co(n * k, "CO2")} + {co(h * k, "H2O")}', f, k, o * k, n * k, h * k


def alk_name(n):
    return f'{PFX[n]}ane'


t8a = topic('Alkanes: combustion and substitution', 'alkanes: complete combustion and substitution reaction with chlorine in uv light', 'complete combustion', 'substitution')
t8a.fixed('C1', (1, 2), [
    ('What are the products of the complete combustion of an alkane?', 'carbon dioxide and water', 'Excess oxygen: CₙH₂ₙ₊₂ + O₂ → CO₂ + H₂O.', ['carbon monoxide and water', 'carbon and hydrogen', 'carbon dioxide and hydrogen']),
    ('What condition is needed for methane to react with chlorine?', 'ultraviolet light', 'Photochemical substitution needs UV light.', ['a nickel catalyst', 'concentrated sulfuric acid', 'a temperature of 300 °C and 60 atm']),
    ('What type of reaction occurs between ethane and chlorine in UV light?', 'substitution', 'A hydrogen atom is replaced by a chlorine atom.', ['addition', 'polymerisation', 'neutralisation']),
    ('Why are alkanes described as generally unreactive?', 'They contain only strong C–C and C–H single bonds', 'Alkanes are saturated; apart from combustion and substitution they react little.', ['They contain C=C double bonds', 'They are ionic', 'They have no hydrogen atoms']),
    ('What are the products when methane reacts with chlorine in UV light?', 'chloromethane and hydrogen chloride', 'CH₄ + Cl₂ → CH₃Cl + HCl.', ['chloromethane and hydrogen', 'dichloromethane only', 'carbon tetrachloride and hydrogen']),
    ('State what is meant by a saturated hydrocarbon.', 'A hydrocarbon containing only single carbon–carbon bonds.', '[1]'),
])
t8a.fixed('C2', (2, 3, 4), [
    ('Explain why the reaction of methane with chlorine is called a photochemical reaction.', 'It needs ultraviolet light to provide the energy to start the reaction.', '[1]'),
    ('Explain why incomplete combustion of alkanes is dangerous in homes.', 'With too little oxygen, carbon monoxide forms; it is colourless, odourless and toxic.', '[2]'),
    ('Explain why a mixture of products forms when methane reacts with excess chlorine.', 'More than one hydrogen can be substituted in turn: CH₃Cl, CH₂Cl₂, CHCl₃ and CCl₄ can all form.', '[2]'),
    ('Explain why alkanes are used as fuels.', 'Their combustion is very exothermic, releasing a lot of energy, and they burn cleanly in excess oxygen.', '[2]'),
])


@t8a.add('C3', (1, 2, 3, 4))
def t8a_comb(r, D):
    n = r.choice([1, 2, 3, 4, 5, 6, 7, 8]) if D >= 3 else r.choice([1, 2, 3, 4])
    eq, f, k, o, c, h = comb_eq('alkane', n)
    if D == 1:
        return mcq_q(r, f'Which is the balanced equation for the complete combustion of {alk_name(n)}?', E(eq), [E(comb_eq('alkane', n)[0].replace(' -> ', ' -> ').replace(f'{"" if c == 1 else c}CO2', f'{"" if c == 1 else c}CO', 1)),
                     E(f'{f} + O2 -> CO2 + H2O'), E(f'{f} + {n}O2 -> {n}CO2 + {n + 1}H2'), E(f'{f} + {n + 1}O2 -> {n}CO2 + {n + 1}H2O' if n > 1 else 'CH4 + O2 -> CO2 + 2H2')], E(eq))
    return {'stem': f'Write the balanced symbol equation for the complete combustion of {alk_name(n)}, {F(f)}.', 'answer': E(eq), 'key': f'{E(eq)}: correct products [1]; balanced [1]'}


@t8a.add('C3', (2, 3, 4, 5), 'numerical')
def t8a_gasvol(r, D):
    n = r.choice([1, 2, 3, 4])
    eq, f, k, o, c, h = comb_eq('alkane', n)
    V = r.choice([10, 20, 25, 30, 40, 50, 100])
    vo = V * o / k
    vc = V * c / k
    if D >= 4:
        Vo = vo + r.choice([20, 30, 50, 100])
        return {'stem': f'{V} cm³ of {alk_name(n)} is burned completely in {sf(Vo)} cm³ of oxygen. {E(eq)}. All volumes are measured at room temperature and pressure. Calculate the total volume of gas remaining after the reaction (water is a liquid).',
                'answer': f'{sf(Vo - vo + vc)} cm³ ({sf(vc)} cm³ CO₂ + {sf(Vo - vo)} cm³ unreacted O₂)', 'key': f'O₂ used = {sf(vo)} cm³ [1]; O₂ left = {sf(Vo - vo)} cm³ [1]; CO₂ formed = {sf(vc)} cm³ [1]; total {sf(Vo - vo + vc)} cm³ [1]', 'marks': 4}
    return {'stem': f'Calculate the volume of oxygen needed to burn {V} cm³ of {alk_name(n)} completely, and the volume of carbon dioxide formed. {E(eq)} (all volumes at r.t.p.)',
            'answer': f'{sf(vo)} cm³ O₂; {sf(vc)} cm³ CO₂', 'key': f'volume ratio = mole ratio [1]; O₂ = {V} × {frac(o / k)} = {sf(vo)} cm³ [1]; CO₂ = {V} × {frac(c / k)} = {sf(vc)} cm³ [1]'}


@t8a.add('C3', (2, 3, 4))
def t8a_subst(r, D):
    n = r.choice([1, 2])
    f = 'CH4' if n == 1 else 'C2H6'
    pr = 'CH3Cl' if n == 1 else 'C2H5Cl'
    nm = 'chloromethane' if n == 1 else 'chloroethane'
    if D >= 4 and n == 1:
        k = r.choice([2, 3, 4])
        prods = {2: ('CH2Cl2', 'dichloromethane'), 3: ('CHCl3', 'trichloromethane'), 4: ('CCl4', 'tetrachloromethane')}[k]
        return {'stem': f'Methane reacts with excess chlorine in UV light. Write the overall equation for the formation of {prods[1]}, and explain why it is a substitution reaction.',
                'answer': E(f'CH4 + {k}Cl2 -> {prods[0]} + {k}HCl') + f'; {k} hydrogen atoms are replaced by chlorine atoms.', 'key': 'products [1]; balanced [1]; substitution explained [1]', 'marks': 3}
    return {'stem': f'{alk_name(n).capitalize()} reacts with chlorine in the presence of ultraviolet light. Name the organic product, write the equation and state the type of reaction.',
            'answer': f'{nm}; {E(f"{f} + Cl2 -> {pr} + HCl")}; substitution (photochemical)', 'key': '1 mark name; 1 mark equation; 1 mark substitution [3]', 'marks': 3}


@t8a.add('C3', (2, 3, 4, 5), 'numerical')
def t8a_mass(r, D):
    n = r.choice([1, 2, 3, 4, 8])
    eq, f, k, o, c, h = comb_eq('alkane', n)
    m = r.choice([8, 16, 32, 44, 58, 114, 22, 30, 60, 11.4, 5.7])
    M = Mr(f)
    n_ = m / M
    mco2 = n_ * c / k * 44
    mh2o = n_ * h / k * 18
    return {'stem': f'Calculate the mass of carbon dioxide and the mass of water formed when {sf(m)} g of {alk_name(n)} burns completely. {E(eq)}',
            'answer': f'{g3(mco2)} g CO₂; {g3(mh2o)} g H₂O', 'key': f'n({F(f)}) = {sf(m)}/{mr(M)} = {g3(n_)} mol [1]; CO₂: × {frac(c / k)} × 44 = {g3(mco2)} g [1]; H₂O: × {frac(h / k)} × 18 = {g3(mh2o)} g [1]'}


def _alk_c4(r, D):
    n = r.choice([1, 2, 3, 4])
    eq, f, k, o, c, h = comb_eq('alkane', n)
    V = r.choice([20, 50, 100])
    intro = r.choice([f'{alk_name(n).capitalize()}, {F(f)}, is used as a fuel in homes in {city(r)}.', f'{person(r)} investigates the reactions of {alk_name(n)}, a member of the alkane homologous series.',
                      f'A gas cylinder contains {alk_name(n)}, which is burned in a camping stove.'])
    parts = [
        lambda r: ('Write the balanced equation for complete combustion.', E(eq), '[2]'),
        lambda r: ('Name the toxic gas formed if the supply of air is limited, and explain why it is toxic.', 'Carbon monoxide: it reduces the ability of the blood to carry oxygen.', '[2]'),
        lambda r: (f'Calculate the volume of oxygen needed to burn {V} cm³ of {alk_name(n)} completely.', f'{sf(V * o / k)} cm³', '[1]'),
        lambda r: (f'Describe the reaction of {alk_name(n)} with chlorine, including the conditions and the type of reaction.', 'UV light; substitution — an H atom is replaced by Cl, forming a chloroalkane and HCl.', '[3]'),
        lambda r: (f'Explain why {alk_name(n)} does not decolourise aqueous bromine.', 'It is saturated (no C=C bond), so it cannot undergo addition.', '[2]'),
        lambda r: ('Write the equation for the reaction with chlorine to form a monochloro product.', E(f'{f} + Cl2 -> {f.replace("H" + str(2 * n + 2), "H" + str(2 * n + 1)) if n > 1 else "CH3"}Cl + HCl'), '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t8a.add('C4', (2, 3, 4, 5), 'multi_step')(_alk_c4)
t8a.add('C3', (3, 4), 'multi_step')(_alk_c4)

# ---------------------------------------------------------- 8.2 cracking and alkenes
ALKENE_ADD = [('ethene', 'C2H4', 'CH2=CH2'), ('propene', 'C3H6', 'CH2=CHCH3'), ('but-1-ene', 'C4H8', 'CH2=CHCH2CH3')]
ADD_PROD = {'bromine': {'ethene': ('1,2-dibromoethane', 'CH2BrCH2Br'), 'propene': ('1,2-dibromopropane', 'CH2BrCHBrCH3'), 'but-1-ene': ('1,2-dibromobutane', 'CH2BrCHBrCH2CH3')},
            'hydrogen': {'ethene': ('ethane', 'CH3CH3'), 'propene': ('propane', 'CH3CH2CH3'), 'but-1-ene': ('butane', 'CH3CH2CH2CH3')},
            'steam': {'ethene': ('ethanol', 'CH3CH2OH'), 'propene': ('propan-1-ol or propan-2-ol', 'CH3CH2CH2OH / CH3CH(OH)CH3'), 'but-1-ene': ('butan-1-ol or butan-2-ol', 'CH3CH2CH2CH2OH / CH3CH(OH)CH2CH3')}}
ADD_COND = {'bromine': 'room temperature; aqueous bromine (no catalyst)', 'hydrogen': 'nickel catalyst, about 150 °C', 'steam': 'phosphoric acid catalyst, about 300 °C and 6000 kPa (60 atm)'}
ADD_REAG = {'bromine': 'Br2', 'hydrogen': 'H2', 'steam': 'H2O'}


def crack(r):
    n = r.randint(8, 16)
    k = r.choice([1, 1, 2, 3])
    p = r.choice([2, 2, 3])
    m = n - k * p
    if m < 3:
        k, p = 1, 2
        m = n - 2
    lhs = f'C{n}H{2 * n + 2}'
    rhs = f'C{m}H{2 * m + 2} + ' + (f'{k}' if k > 1 else '') + f'C{p}H{2 * p}'
    return n, m, k, p, f'{lhs} -> {rhs}'


t8b = topic('Cracking and addition reactions of alkenes', 'cracking of alkanes and addition reactions of alkenes', 'distinguishing with aqueous bromine', 'cracking alkenes')
t8b.fixed('C1', (1, 2), [
    ('What are the conditions for catalytic cracking?', 'high temperature and a catalyst', 'Large alkane molecules are heated (about 500 °C) over a catalyst such as aluminium oxide or silica.', ['low temperature and UV light', 'high pressure and an enzyme', 'room temperature and a nickel catalyst']),
    ('What is seen when ethene is bubbled through aqueous bromine?', 'The solution turns from orange to colourless', 'Addition across C=C forms colourless 1,2-dibromoethane.', ['The solution turns from colourless to orange', 'A white precipitate forms', 'No change']),
    ('Which type of reaction occurs when an alkene reacts with hydrogen?', 'addition', 'H₂ adds across the C=C bond (Ni catalyst) to form an alkane.', ['substitution', 'cracking', 'combustion only']),
    ('Why is cracking important to oil refineries?', 'It converts large, less useful alkanes into smaller, more useful alkanes and alkenes', 'Demand for petrol and alkenes exceeds supply from distillation.', ['It removes sulfur from crude oil', 'It makes the oil thicker', 'It separates oil into fractions']),
    ('Which product of cracking could be used to make polymers?', 'ethene', 'Alkenes are monomers for addition polymers.', ['octane', 'methane', 'decane']),
    ('State what is meant by an unsaturated hydrocarbon.', 'A hydrocarbon containing at least one carbon–carbon double bond.', '[1]'),
])
t8b.fixed('C2', (2, 3, 4), [
    ('Explain why aqueous bromine can be used to distinguish between an alkane and an alkene.', 'Alkenes are unsaturated and undergo addition with bromine, decolourising it (orange → colourless); alkanes are saturated and do not react, so the solution stays orange.', '[3]'),
    ('Explain why cracking always produces at least one unsaturated product.', 'A long alkane does not have enough hydrogen atoms for all the smaller molecules to be saturated, so at least one alkene (or H₂) forms.', '[2]'),
    ('Explain why alkenes are more reactive than alkanes.', 'The C=C double bond can open up, allowing atoms to add across it.', '[2]'),
    ('Explain why the addition of hydrogen to an alkene is important in the food industry.', 'It converts unsaturated vegetable oils into saturated fats (margarine) with a higher melting point.', '[2]'),
])


@t8b.add('C3', (1, 2, 3, 4))
def t8b_crack(r, D):
    n, m, k, p, eq = crack(r)
    miss = r.choice(['alkene', 'alkane'])
    lhs, rhs = eq.split(' -> ')
    a1, a2 = rhs.split(' + ')
    if D == 1:
        corr = F(a2.lstrip('0123456789')) if miss == 'alkene' else F(a1)
        tgt = a2.lstrip('0123456789') if miss == 'alkene' else a1
        cc = atoms(tgt)['C']
        pool = [F(f'C{cc}H{atoms(tgt)["H"] + d}') for d in (-2, 2, 4, -4) if atoms(tgt)['H'] + d > 0]
        shown = E(eq.replace(a2, f'{a2[:-len(a2.lstrip("0123456789"))]}X') if miss == 'alkene' else eq.replace(a1, 'X'))
        return mcq_q(r, f'A hydrocarbon is cracked: {shown}. What is the formula of X?', corr, pool, f'Balance C and H atoms: {E(eq)}.')
    if D >= 3:
        return {'stem': f'{F(lhs)} is cracked to give {F(a1)} and {"one other product" if k == 1 else str(k) + " molecules of one other product"}. Deduce the formula of the other product, write the equation and describe a test to show the product is unsaturated.',
                'answer': f'{F(a2.lstrip("0123456789"))}; {E(eq)}; add aqueous bromine: turns from orange to colourless.', 'key': '1 mark formula; 1 mark balanced equation; 1 mark test and result [3]', 'marks': 3}
    return {'stem': f'Complete and balance the equation for the cracking of {F(lhs)} into {F(a1)} and {"ethene" if p == 2 else "propene"} only: {F(lhs)} → {F(a1)} + ...', 'answer': E(eq), 'key': f'C: {n} = {m} + {k} × {p}; H: {2 * n + 2} = {2 * m + 2} + {k} × {2 * p} [1]; correct coefficient {k} [1]'}


@t8b.add('C3', (1, 2, 3, 4))
def t8b_add(r, D):
    nm, f, sfm = r.choice(ALKENE_ADD)
    reag = r.choice(list(ADD_PROD))
    pn, pf = ADD_PROD[reag][nm]
    if D == 1:
        return mcq_q(r, f'What is the product when {nm} reacts with {reag}?', pn, [x[0] for rr in ADD_PROD.values() for x in rr.values()], f'Addition across C=C: {pn}.')
    st = f'{E(f + " + " + ADD_REAG[reag] + " -> " + atoms_formula(f, reag))}'
    return {'stem': f'{nm.capitalize()} reacts with {reag}. Name the product, give its structural formula, write the equation using molecular formulae and state the conditions.',
            'answer': f'{pn}; {F(pf)}; {st}; {ADD_COND[reag]}', 'key': '1 mark product name/structure; 1 mark equation; 1 mark conditions [3]', 'marks': 3}


def atoms_formula(f, reag):
    a = atoms(f)
    c, h = a['C'], a['H']
    if reag == 'bromine':
        return f'C{c}H{h}Br2'
    if reag == 'hydrogen':
        return f'C{c}H{h + 2}'
    return f'C{c}H{h + 1}OH'


@t8b.add('C2', (2, 3, 4), 'explain')
def t8b_dist(r, D):
    a = r.choice([x for x in COMP if x[1] == 'alkane' and x[4] >= 2])
    b = r.choice(ALKENE_ADD)
    L = r.sample(['A', 'B'], 2)
    return {'stem': f'Two unlabelled gas jars contain {a[0]} and {b[0]}. Describe a chemical test that would show which jar contains {b[0]}, giving the result for each gas and explaining the difference.',
            'answer': f'Shake each with aqueous bromine. {cap(b[0])}: orange → colourless (addition across C=C). {cap(a[0])}: stays orange (saturated, no addition).', 'key': '1 mark reagent; 1 mark each result; 1 mark explanation [4]', 'marks': 4}


@t8b.add('C3', (2, 3, 4, 5), 'numerical')
def t8b_mass(r, D):
    nm, f, sfm = r.choice(ALKENE_ADD)
    m = r.choice([2.8, 5.6, 14, 28, 1.4, 4.2, 8.4, 2.1])
    M = Mr(f)
    pr = atoms_formula(f, 'bromine')
    mp = m / M * Mr(pr)
    mbr = m / M * 160
    return {'stem': f'Calculate the mass of bromine that reacts exactly with {sf(m)} g of {nm}, and the mass of product formed. {E(f + " + Br2 -> " + pr)}',
            'answer': f'{g3(mbr)} g Br₂; {g3(mp)} g product', 'key': f'n({F(f)}) = {sf(m)}/{mr(M)} = {g3(m / M)} mol [1]; mass Br₂ = {g3(m / M)} × 160 = {g3(mbr)} g [1]; product Mr {mr(Mr(pr))}, mass = {g3(mp)} g [1]'}


def _crack_c4(r, D):
    n, m, k, p, eq = crack(r)
    lhs, rhs = eq.split(' -> ')
    a1, a2 = rhs.split(' + ')
    alk = {2: 'ethene', 3: 'propene'}[p]
    intro = r.choice([f'An oil refinery in {city(r)} cracks {F(lhs)} to make petrol and {alk}.', f'{person(r)} cracks paraffin oil in the laboratory by passing its vapour over heated broken pottery (a catalyst).',
                      f'Long-chain alkanes such as {F(lhs)} are in low demand, so they are cracked: {E(eq)}.'])
    parts = [
        lambda r: ('State the conditions needed for cracking.', 'High temperature (about 500 °C) and a catalyst (e.g. aluminium oxide/silica).', '[2]'),
        lambda r: (f'Write the balanced equation for cracking {F(lhs)} into {F(a1)} and {alk}.', E(eq), '[2]'),
        lambda r: ('Explain why cracking is needed.', 'Demand for smaller alkanes (petrol) and alkenes is greater than the supply from fractional distillation; long chains are less useful.', '[2]'),
        lambda r: (f'Describe a test to show that {alk} is unsaturated.', 'Aqueous bromine turns from orange to colourless.', '[2]'),
        lambda r: (f'Name the product formed when {alk} reacts with steam, and give the conditions.', f'{ADD_PROD["steam"][alk][0]}; {ADD_COND["steam"]}', '[2]'),
        lambda r: (f'Name the product when {alk} reacts with bromine and state the type of reaction.', f'{ADD_PROD["bromine"][alk][0]}; addition', '[2]'),
        lambda r: ('Suggest why hydrogen is also a useful product of some cracking reactions.', 'It can be used as a fuel or to make ammonia/margarine.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t8b.add('C4', (2, 3, 4, 5), 'multi_step')(_crack_c4)
t8b.add('C3', (3, 4, 5), 'multi_step')(_crack_c4)

# ---------------------------------------------------------- 8.3 ethanol
ETH_CMP = [('rate of production', 'slow', 'fast'), ('purity of product', 'impure (about 15% ethanol; must be distilled)', 'pure ethanol'), ('raw material', 'renewable (sugars from crops)', 'non-renewable (ethene from petroleum)'),
           ('process type', 'batch', 'continuous'), ('temperature', '25–35 °C', 'about 300 °C'), ('energy use', 'low', 'high (high temperature and pressure)')]
t8c = topic('Ethanol', 'ethanol: manufacture by fermentation and by catalytic addition of steam to ethene', 'combustion and uses', 'fermentation')
t8c.fixed('C1', (1, 2), [
    ('What are the conditions for making ethanol by fermentation?', 'yeast, 25–35 °C, absence of oxygen', 'Glucose → ethanol + CO₂ using enzymes in yeast, anaerobic, warm.', ['nickel catalyst, 150 °C', 'phosphoric acid catalyst, 300 °C, 60 atm', 'UV light, room temperature']),
    ('What is the catalyst for the addition of steam to ethene?', 'phosphoric acid', 'C₂H₄ + H₂O → C₂H₅OH, H₃PO₄ catalyst, 300 °C, 6000 kPa.', ['yeast', 'iron', 'nickel']),
    ('Which equation represents fermentation?', 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'Glucose → ethanol + carbon dioxide.', ['C₂H₄ + H₂O → C₂H₅OH', 'C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O']),
    ('Give a use of ethanol.', 'As a fuel or as a solvent', 'Ethanol burns cleanly and dissolves many substances.', ['As a fertiliser', 'As a food preservative only', 'As a refrigerant']),
    ('Why is the temperature in fermentation kept below about 40 °C?', 'Higher temperatures denature the enzymes in yeast', 'Enzymes are proteins that lose their shape when too hot.', ['Ethanol freezes above 40 °C', 'Oxygen is needed above 40 °C', 'Glucose decomposes at 40 °C']),
    ('Write the word equation for the complete combustion of ethanol.', 'ethanol + oxygen → carbon dioxide + water', '[1]'),
])
t8c.fixed('C2', (2, 3, 4), [
    ('Explain why fermentation is carried out in the absence of air.', 'With oxygen, yeast respires aerobically to CO₂ and water (and ethanol can be oxidised to ethanoic acid), so no ethanol is produced.', '[2]'),
    ('Explain why fermentation stops when the ethanol concentration reaches about 15%.', 'Ethanol becomes toxic to the yeast and kills it.', '[1]'),
    ('Explain why ethanol made by fermentation can be described as a renewable (biofuel).', 'It is made from sugar from crops that can be regrown each year.', '[2]'),
    ('Explain why ethanol from fermentation must be fractionally distilled.', 'The mixture contains only about 15% ethanol in water and other substances; ethanol (b.p. 78 °C) is separated from water (b.p. 100 °C).', '[2]'),
])


@t8c.add('C2', (2, 3, 4), 'explain')
def t8c_cmp(r, D):
    a, b = r.sample(ETH_CMP, 2)
    cty = city(r)
    return {'stem': f'A company in {cty} must decide whether to make ethanol by fermentation or by the catalytic addition of steam to ethene. Compare the two methods in terms of {a[0]} and {b[0]}.',
            'answer': f'{cap(a[0])}: fermentation {a[1]}, hydration {a[2]}. {cap(b[0])}: fermentation {b[1]}, hydration {b[2]}.', 'key': '1 mark each correct comparison for each factor (both methods) [4]', 'marks': 4 if D >= 3 else 2}


@t8c.add('C3', (2, 3, 4, 5), 'numerical')
def t8c_ferm(r, D):
    mg = r.choice([90, 180, 360, 45, 900, 18, 1800])
    n = mg / 180
    me = n * 2 * 46
    vco2 = n * 2 * 24
    if D >= 4:
        act = r3(me * r.choice([0.6, 0.7, 0.75, 0.8, 0.85]))
        return {'stem': f'{mg} g of glucose is fermented. C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂. Calculate (a) the maximum mass of ethanol, (b) the volume of CO₂ at r.t.p., (c) the percentage yield if {g3(act)} g of ethanol is obtained.',
                'answer': f'(a) {g3(me)} g (b) {g3(vco2)} dm³ (c) {g3(act / r3(me) * 100)}%', 'key': f'n(glucose) = {g3(n)} mol [1]; ethanol = {g3(2 * n)} × 46 = {g3(me)} g [1]; CO₂ = {g3(2 * n)} × 24 = {g3(vco2)} dm³ [1]; yield = {g3(act)}/{g3(me)} × 100 [1]', 'marks': 4}
    return {'stem': f'Calculate the maximum mass of ethanol that can be made by fermenting {mg} g of glucose. C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'answer': f'{g3(me)} g',
            'key': f'n(glucose) = {mg}/180 = {g3(n)} mol [1]; n(ethanol) = {g3(2 * n)} mol [1]; mass = {g3(2 * n)} × 46 = {g3(me)} g [1]'}


@t8c.add('C3', (1, 2, 3, 4))
def t8c_comb(r, D):
    n = r.choice([1, 2, 3, 4])
    eq, f, k, o, c, h = comb_eq('alcohol', n)
    nm = {1: 'methanol', 2: 'ethanol', 3: 'propan-1-ol', 4: 'butan-1-ol'}[n]
    if D == 1:
        return mcq_q(r, f'Which equation shows the complete combustion of {nm}?', E(eq), [E(f'{f} + O2 -> CO2 + H2O'), E(f'{f} -> {n}C + H2O'), E(f'{f} + {n}O2 -> {n}CO + {n + 1}H2O'), E(comb_eq('alkane', n)[0])], E(eq))
    if D >= 3:
        m = r.choice([4.6, 9.2, 23, 46, 3.2, 6.0, 7.4])
        M = Mr(f)
        return {'stem': f'{nm.capitalize()} is used as a fuel. Write the balanced equation for its complete combustion and calculate the mass of carbon dioxide formed when {sf(m)} g burns.',
                'answer': f'{E(eq)}; {g3(m / M * c / k * 44)} g', 'key': f'equation [2]; n = {sf(m)}/{mr(M)} [1]; mass CO₂ = {g3(m / M * c / k * 44)} g [1]', 'marks': 4}
    return {'stem': f'Write the balanced equation for the complete combustion of {nm}.', 'answer': E(eq), 'key': 'products [1]; balanced [1]'}


@t8c.add('C3', (2, 3, 4), 'numerical')
def t8c_hyd(r, D):
    t = r.choice([14, 28, 56, 140, 280, 2.8])
    me = t / 28 * 46
    return {'stem': f'Ethanol is manufactured by the addition of steam to ethene: C₂H₄ + H₂O → C₂H₅OH. Calculate the mass of ethanol formed from {sf(t)} tonnes of ethene, and state the conditions used.',
            'answer': f'{g3(me)} tonnes; phosphoric acid catalyst, about 300 °C, 6000 kPa', 'key': f'28 t ethene → 46 t ethanol [1]; mass = {g3(me)} t [1]; conditions [1]', 'marks': 3}


def _eth_c4(r, D):
    mg = r.choice([180, 360, 900])
    intro = r.choice([f'A biofuel plant in {city(r)} ferments sugar cane juice to make ethanol.', f'{person(r)} sets up a fermentation experiment using glucose solution and yeast in a conical flask fitted with an airlock.',
                      'Ethanol can be made by fermentation or by the catalytic addition of steam to ethene.'])
    parts = [
        lambda r: ('Write the balanced equation for fermentation.', E('C6H12O6 -> 2C2H5OH + 2CO2'), '[2]'),
        lambda r: ('State the conditions for fermentation.', 'Yeast; 25–35 °C; absence of oxygen (anaerobic); aqueous glucose.', '[2]'),
        lambda r: (f'Calculate the mass of ethanol that could be made from {mg} g of glucose.', f'{g3(mg / 180 * 92)} g', '[2]'),
        lambda r: ('Describe how the gas produced could be identified.', 'Bubble it through limewater: it turns milky (carbon dioxide).', '[2]'),
        lambda r: ('Give one advantage and one disadvantage of fermentation compared with the addition of steam to ethene.', 'Advantage: renewable raw material / low temperature. Disadvantage: slow / batch process / impure product needing distillation.', '[2]'),
        lambda r: ('Write the equation for the complete combustion of ethanol.', E('C2H5OH + 3O2 -> 2CO2 + 3H2O'), '[2]'),
        lambda r: ('Explain why the flask is fitted with an airlock.', 'It lets CO₂ escape but stops air (oxygen) and microbes getting in.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t8c.add('C4', (2, 3, 4, 5), 'multi_step')(_eth_c4)
t8c.add('C3', (3, 4), 'multi_step')(_eth_c4)

# ---------------------------------------------------------- 8.4 carboxylic acids
ACIDS_O = [('methanoic acid', 'HCOOH', 'methanoate', 'HCOO'), ('ethanoic acid', 'CH3COOH', 'ethanoate', 'CH3COO'), ('propanoic acid', 'CH3CH2COOH', 'propanoate', 'CH3CH2COO')]


def acid_rx(ac, reag):
    nm, f, sal, an = ac
    if reag == 'magnesium':
        return f'2{f} + Mg -> ({an})2Mg + H2', f'magnesium {sal} and hydrogen', 'fizzing; the magnesium dissolves'
    if reag == 'sodium carbonate':
        return f'2{f} + Na2CO3 -> 2{an}Na + H2O + CO2', f'sodium {sal}, water and carbon dioxide', 'fizzing; gas turns limewater milky'
    if reag == 'sodium hydroxide':
        return f'{f} + NaOH -> {an}Na + H2O', f'sodium {sal} and water', 'no visible change (temperature rises)'
    if reag == 'calcium carbonate':
        return f'2{f} + CaCO3 -> ({an})2Ca + H2O + CO2', f'calcium {sal}, water and carbon dioxide', 'fizzing; the solid dissolves'
    return f'{f} + KOH -> {an}K + H2O', f'potassium {sal} and water', 'no visible change (temperature rises)'


AREAG = ['magnesium', 'sodium carbonate', 'sodium hydroxide', 'calcium carbonate', 'potassium hydroxide']

t8d = topic('Carboxylic acids and esterification', 'carboxylic acids: reactions as weak acids', 'esterification with alcohols', 'carboxylic acids')
t8d.fixed('C1', (1, 2), [
    ('Why is ethanoic acid described as a weak acid?', 'It is only partially dissociated into ions in water', 'CH₃COOH ⇌ CH₃COO⁻ + H⁺ — only a small fraction ionises.', ['It has a low concentration', 'It does not react with metals', 'It is fully dissociated']),
    ('What is the catalyst for esterification?', 'concentrated sulfuric acid', 'Acid + alcohol ⇌ ester + water with a few drops of conc. H₂SO₄, warmed.', ['nickel', 'yeast', 'phosphoric acid at 300 °C']),
    ('Which salt is formed when ethanoic acid reacts with sodium hydroxide?', 'sodium ethanoate', 'CH₃COOH + NaOH → CH₃COONa + H₂O.', ['sodium ethanol', 'sodium methanoate', 'ethyl sodium']),
    ('Which process makes ethanoic acid from ethanol?', 'oxidation with acidified potassium manganate(VII)', 'Ethanol is oxidised (or by bacterial oxidation/fermentation in air) to ethanoic acid.', ['reduction with hydrogen', 'cracking', 'hydration with steam']),
    ('What is the smell of most esters?', 'sweet or fruity', 'Esters are used as flavourings and perfumes.', ['like rotten eggs', 'like vinegar', 'odourless']),
    ('Name the functional group of the carboxylic acids.', '–COOH (carboxyl group)', '[1]'),
])
t8d.fixed('C2', (2, 3, 4), [
    ('Explain why ethanoic acid reacts more slowly with magnesium than hydrochloric acid of the same concentration.', 'Ethanoic acid is a weak acid — only partially dissociated — so the concentration of H⁺ ions is lower.', '[2]'),
    ('Explain why a 0.1 mol/dm³ solution of ethanoic acid has a higher pH than 0.1 mol/dm³ hydrochloric acid.', 'Ethanoic acid is weak and only partly ionised, so [H⁺] is lower; HCl is fully ionised.', '[2]'),
    ('Explain why wine left open to the air turns sour.', 'Bacteria oxidise the ethanol to ethanoic acid (vinegar) using oxygen from the air.', '[2]'),
    ('Explain why esterification is described as a condensation reaction.', 'Two molecules join together and a small molecule (water) is eliminated.', '[2]'),
])


@t8d.add('C3', (1, 2, 3, 4))
def t8d_rx(r, D):
    ac = r.choice(ACIDS_O)
    reag = r.choice(AREAG)
    eq, prods, obs = acid_rx(ac, reag)
    if D == 1:
        pool = [acid_rx(ac, x)[1] for x in AREAG] + [f'{reag.split()[0]} {ac[2]} and oxygen']
        return mcq_q(r, f'What are the products when {ac[0]} reacts with {reag}?', prods, pool, E(eq))
    return {'stem': f'{ac[0].capitalize()} reacts with {reag}. Describe what you would observe, name the products and write the balanced equation.',
            'answer': f'{cap(obs)}; {prods}; {E(eq)}', 'key': '1 mark observation; 1 mark products; 1 mark equation [3]', 'marks': 3}


@t8d.add('C3', (2, 3, 4, 5))
def t8d_ester(r, D):
    nm, f, acid, alc = r.choice(ESTERS)
    if D >= 4:
        acf = {'methanoic acid': 'HCOOH', 'ethanoic acid': 'CH3COOH', 'propanoic acid': 'CH3CH2COOH'}[acid]
        alf = {'methanol': 'CH3OH', 'ethanol': 'CH3CH2OH', 'propan-1-ol': 'CH3CH2CH2OH'}[alc]
        return {'stem': f'{cap(acid)} is warmed with {alc} and a few drops of concentrated sulfuric acid. Name the organic product, give its structural formula, write the equation using structural formulae and state the role of the sulfuric acid.',
                'answer': f'{nm}; {F(f)}; {F(acf)} + {F(alf)} ⇌ {F(f)} + H₂O; catalyst', 'key': '1 mark name; 1 mark formula; 1 mark equation; 1 mark catalyst [4]', 'marks': 4}
    return {'stem': f'Name the ester formed when {acid} reacts with {alc}, and state the conditions needed.', 'answer': f'{nm}; warm with a few drops of concentrated sulfuric acid (catalyst).', 'key': '1 mark name; 1 mark conditions [2]'}


@t8d.add('C3', (2, 3, 4, 5), 'numerical')
def t8d_mass(r, D):
    ac = r.choice(ACIDS_O[1:])
    reag = r.choice(['magnesium', 'sodium carbonate', 'calcium carbonate'])
    eq, prods, obs = acid_rx(ac, reag)
    V = r.choice([25.0, 50.0, 100.0, 40.0]); c = r.choice([0.5, 1.0, 2.0])
    na = V / 1000 * c
    gas = 'hydrogen' if reag == 'magnesium' else 'carbon dioxide'
    vg = na / 2 * 24000
    return {'stem': f'Excess {reag} is added to {sf(V)} cm³ of {sf(c)} mol/dm³ {ac[0]}. {E(eq)}. Calculate the volume of {gas} formed at r.t.p., in cm³.',
            'answer': f'{g3(vg)} cm³', 'key': f'n(acid) = {g3(na)} mol [1]; n(gas) = {g3(na / 2)} mol [1]; V = {g3(vg)} cm³ [1]'}


@t8d.add('C2', (2, 3, 4), 'explain')
def t8d_weak(r, D):
    ac = r.choice(ACIDS_O)
    conc = r.choice(['0.10', '0.50', '1.0'])
    test = r.choice([('pH', 'the ethanoic-type acid has the higher pH (about 3 vs 1)', 'lower [H⁺]'), ('rate of reaction with magnesium ribbon', 'the carboxylic acid fizzes more slowly', 'lower [H⁺]'),
                     ('electrical conductivity', 'the carboxylic acid conducts less well', 'fewer ions in solution')])
    return {'stem': f'{person(r)} compares {conc} mol/dm³ {ac[0]} with {conc} mol/dm³ hydrochloric acid by measuring their {test[0]}. Predict the result and explain it.',
            'answer': f'{cap(test[1]).replace("the ethanoic-type acid", ac[0])}: {ac[0]} is a weak acid, only partially dissociated, so {test[2]}; hydrochloric acid is a strong acid, fully dissociated.',
            'key': '1 mark prediction; 1 mark weak = partially dissociated; 1 mark link to H⁺/ions [3]', 'marks': 3}


def _ac_c4(r, D):
    ac = r.choice(ACIDS_O)
    e = r.choice([x for x in ESTERS if x[2] == ac[0]])
    reag = r.choice(AREAG)
    eq, prods, obs = acid_rx(ac, reag)
    intro = r.choice([f'Vinegar sold in {city(r)} contains ethanoic acid. A student studies {ac[0]}, a member of the same homologous series.', f'{person(r)} investigates the reactions of {ac[0]}, {F(ac[1])}.',
                      f'A food-flavouring company makes the ester {e[0]} from {ac[0]}.'])
    parts = [
        lambda r: (f'State the functional group in {ac[0]}.', '–COOH', '[1]'),
        lambda r: (f'Explain why {ac[0]} is described as a weak acid.', 'It is only partially dissociated into H⁺ ions in aqueous solution.', '[2]'),
        lambda r: (f'Describe what is seen when {reag} is added and write the equation.', f'{cap(obs)}; {E(eq)}', '[3]'),
        lambda r: (f'Name the alcohol needed to make {e[0]} from {ac[0]}, and state the conditions.', f'{e[3]}; warm with concentrated sulfuric acid catalyst.', '[2]'),
        lambda r: (f'Give the structural formula of {e[0]}.', F(e[1]), '[1]'),
        lambda r: ('Suggest a use of esters.', 'Flavourings, perfumes or solvents.', '[1]'),
        lambda r: ('Describe how ethanoic acid can be made from ethanol.', 'Oxidation with acidified aqueous potassium manganate(VII), or by bacterial oxidation in air.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t8d.add('C4', (2, 3, 4, 5), 'multi_step')(_ac_c4)
t8d.add('C3', (3, 4), 'multi_step')(_ac_c4)

CHAPTERS[8] = [t8a, t8b, t8c, t8d]


# ===================================================================== Ch9 (CB20) Petrochemicals and polymers
FRACTIONS = [('refinery gas', 'C1–C4', 'fuel for heating and cooking (bottled gas)'), ('gasoline / petrol', 'C5–C10', 'fuel for cars'), ('naphtha', 'C5–C10', 'feedstock for the chemical industry'),
             ('kerosene / paraffin', 'C10–C16', 'jet fuel'), ('diesel oil / gas oil', 'C15–C20', 'fuel in diesel engines'), ('fuel oil', 'C20–C30', 'fuel for ships and home heating systems'),
             ('lubricating oil', 'C30–C50', 'lubricants, waxes and polishes'), ('bitumen', 'C50+', 'making roads')]

t9a = topic('Petroleum and fractional distillation', 'petroleum and natural gas as fuels', 'fractional distillation of petroleum and uses of fractions', 'fractional distillation')
t9a.fixed('C1', (1, 2), [
    ('What is petroleum?', 'A mixture of hydrocarbons', 'Crude oil is a mixture of many hydrocarbons, mainly alkanes.', ['A single pure hydrocarbon', 'A mixture of alcohols', 'An element']),
    ('What is the main constituent of natural gas?', 'methane', 'Natural gas is mostly CH₄.', ['ethane', 'butane', 'hydrogen']),
    ('How does the boiling point of the fractions change from the top to the bottom of the fractionating column?', 'It increases', 'Larger molecules with higher boiling points condense lower down where it is hotter.', ['It decreases', 'It stays the same', 'It decreases then increases']),
    ('Which fraction is used to surface roads?', 'bitumen', 'Bitumen is the thick residue at the bottom of the column.', ['naphtha', 'kerosene', 'refinery gas']),
    ('Which property increases down the fractionating column?', 'viscosity', 'Down the column: longer chains, higher b.p., higher viscosity, lower volatility.', ['volatility', 'flammability', 'number of molecules per gram']),
    ('State the use of the naphtha fraction.', 'Feedstock (raw material) for making chemicals.', '[1]'),
])
t9a.fixed('C2', (2, 3, 4), [
    ('Explain how petroleum is separated into fractions in a fractionating column.', 'Petroleum is vaporised; vapours rise up the column, which is hotter at the bottom; each fraction condenses at the level where the temperature is below its boiling point and is collected.', '1 mark heated/vaporised; 1 mark temperature gradient; 1 mark condense at different heights by boiling point [3]'),
    ('Explain why refinery gas leaves at the top of the column.', 'Its molecules are the smallest, with the lowest boiling points, so they stay as gases even at the cool top.', '[2]'),
    ('Explain why bitumen is very viscous.', 'Its molecules are very long, with strong intermolecular forces, so they do not flow easily.', '[2]'),
    ('Explain why a fraction is described as a mixture.', 'It contains hydrocarbons with a range of chain lengths and boiling points, not a single compound.', '[2]'),
    ('Explain why petroleum and natural gas are described as non-renewable fuels.', 'They formed over millions of years and are being used much faster than they form.', '[2]'),
])


@t9a.add('C1', (1, 2, 3))
def t9a_use(r, D):
    f, c, use = r.choice(FRACTIONS)
    if r.random() < 0.5:
        return mcq_q(r, f'Which fraction of petroleum is used for {use}?', f, [x[0] for x in FRACTIONS], f'{f} ({c}): {use}.')
    return mcq_q(r, f'What is the main use of the {f} fraction?', use, [x[2] for x in FRACTIONS], f'{f}: {use}.')


@t9a.add('C3', (2, 3, 4))
def t9a_order(r, D):
    fs = r.sample(FRACTIONS, 4)
    srt = sorted(fs, key=lambda x: FRACTIONS.index(x))
    prop = r.choice(['boiling point', 'chain length', 'viscosity', 'volatility'])
    order = srt if prop == 'volatility' else srt[::-1]
    return {'stem': f'Put these fractions in order of decreasing {prop}: ' + ', '.join(x[0] for x in fs) + '. Explain your order.',
            'answer': ' > '.join(x[0] for x in order) + f'; {prop} {"decreases" if prop == "volatility" else "increases"} with chain length (fractions from lower in the column have longer molecules and stronger intermolecular forces).',
            'key': '1 mark order; 1 mark linked to chain length / intermolecular forces [2]'}


@t9a.add('C2', (2, 3, 4), 'explain')
def t9a_compare(r, D):
    a, b = sorted(r.sample(FRACTIONS, 2), key=lambda x: FRACTIONS.index(x))
    return {'stem': f'Compare the {a[0]} and {b[0]} fractions in terms of chain length, boiling point and where they are collected in the column.',
            'answer': f'{cap(a[0])} ({a[1]}) has shorter chains, a lower boiling point and is collected higher up the column than {b[0]} ({b[1]}).', 'key': '1 mark each comparison [3]', 'marks': 3}


@t9a.add('C3', (2, 3, 4, 5), 'numerical')
def t9a_data(r, D):
    tot = r.choice([100, 200, 500, 1000])
    sup = {'refinery gas': r.choice([2, 3, 4]), 'gasoline / petrol': r.choice([8, 10, 12]), 'kerosene / paraffin': r.choice([12, 14]), 'diesel oil / gas oil': r.choice([18, 20, 22]), 'fuel oil and bitumen': None}
    sup['fuel oil and bitumen'] = 100 - sum(v for k, v in sup.items() if v)
    dem = {'refinery gas': 4, 'gasoline / petrol': r.choice([25, 28, 30]), 'kerosene / paraffin': 8, 'diesel oil / gas oil': 23, 'fuel oil and bitumen': None}
    dem['fuel oil and bitumen'] = 100 - sum(v for k, v in dem.items() if v)
    tbl = '; '.join(f'{k}: supply {sup[k]}%, demand {dem[k]}%' for k in sup)
    short = sup['gasoline / petrol']
    extra = (dem['gasoline / petrol'] - short) / 100 * tot
    return {'stem': f'The table shows the percentage supply from fractional distillation and the percentage demand for some fractions. {tbl}. A refinery processes {tot} thousand tonnes of crude oil. Calculate the shortfall of petrol in thousand tonnes and explain how the refinery can meet the demand.',
            'answer': f'{sf(extra)} thousand tonnes; crack excess long-chain fractions (e.g. fuel oil) into smaller alkanes for petrol and alkenes.', 'key': f'shortfall = ({dem["gasoline / petrol"]} − {short})% × {tot} = {sf(extra)} [2]; cracking of surplus heavy fractions [1]', 'marks': 3}


def _frac_c4(r, D):
    fs = r.sample(FRACTIONS, 3)
    intro = r.choice([f'A refinery in {city(r)} separates crude oil by fractional distillation.', f'{person(r)} draws a labelled diagram of a fractionating column showing where three fractions, ' + ', '.join(x[0] for x in fs) + ', are collected.',
                      'Petroleum and natural gas are fossil fuels and important sources of chemicals.'])
    srt = sorted(fs, key=lambda x: FRACTIONS.index(x))
    parts = [
        lambda r: ('Describe how fractional distillation separates petroleum.', 'Petroleum is heated to vaporise it; the column is hot at the bottom and cooler at the top; fractions condense at different heights according to boiling point.', '[3]'),
        lambda r: (f'State which of {", ".join(x[0] for x in fs)} is collected nearest the top and explain why.', f'{srt[0][0]}: shortest chains, lowest boiling point.', '[2]'),
        lambda r: (f'Give a use of {fs[1][0]}.', fs[1][2], '[1]'),
        lambda r: (f'State the approximate number of carbon atoms in molecules of {fs[2][0]}.', fs[2][1], '[1]'),
        lambda r: ('State how volatility changes down the column.', 'It decreases.', '[1]'),
        lambda r: ('Name the main constituent of natural gas and write the equation for its complete combustion.', 'Methane; ' + E('CH4 + 2O2 -> CO2 + 2H2O'), '[2]'),
        lambda r: ('Give one reason why burning fossil fuels causes environmental concern.', 'CO₂ is a greenhouse gas (climate change); SO₂ causes acid rain; CO/particulates from incomplete combustion.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t9a.add('C4', (2, 3, 4, 5), 'multi_step')(_frac_c4)
t9a.add('C3', (3, 4), 'multi_step')(_frac_c4)

# ---------------------------------------------------------- 9.2 addition polymers
MONO = [('ethene', 'CH2=CH2', '–[CH₂–CH₂]ₙ–', 'poly(ethene)', 'plastic bags and cling film', 28), ('propene', 'CH2=CHCH3', '–[CH₂–CH(CH₃)]ₙ–', 'poly(propene)', 'ropes, crates and food containers', 42),
        ('chloroethene', 'CH2=CHCl', '–[CH₂–CHCl]ₙ–', 'poly(chloroethene), PVC', 'water pipes and electrical insulation', 62.5), ('tetrafluoroethene', 'CF2=CF2', '–[CF₂–CF₂]ₙ–', 'poly(tetrafluoroethene), PTFE', 'non-stick coatings for pans', 100),
        ('phenylethene (styrene)', 'CH2=CHC6H5', '–[CH₂–CH(C₆H₅)]ₙ–', 'poly(phenylethene), polystyrene', 'packaging and insulation', 104), ('but-1-ene', 'CH2=CHCH2CH3', '–[CH₂–CH(CH₂CH₃)]ₙ–', 'poly(but-1-ene)', 'hot-water pipes', 56)]

t9b = topic('Addition polymerisation', 'addition polymerisation: poly(ethene)', 'deducing monomers and repeat units', 'addition polymers')
t9b.fixed('C1', (1, 2), [
    ('What is a polymer?', 'A large molecule built up from many small units called monomers', 'Polymers are long-chain molecules made by joining many monomers.', ['A small molecule with one double bond', 'A mixture of alkanes', 'An ionic compound']),
    ('Which type of monomer forms addition polymers?', 'an alkene (contains C=C)', 'The C=C bond opens and monomers join.', ['an alkane', 'an alcohol', 'a carboxylic acid']),
    ('What is the only product of addition polymerisation?', 'the polymer', 'No small molecule is lost, unlike condensation polymerisation.', ['the polymer and water', 'the polymer and hydrogen chloride', 'the polymer and carbon dioxide']),
    ('Which polymer is made from ethene?', 'poly(ethene)', 'n CH₂=CH₂ → –[CH₂–CH₂]ₙ–.', ['nylon', 'PET', 'protein']),
    ('Which monomer is used to make PVC?', 'chloroethene', 'PVC = poly(chloroethene), –[CH₂–CHCl]ₙ–.', ['ethene', 'propene', 'tetrafluoroethene']),
    ('State what happens to the double bond during addition polymerisation.', 'It breaks/opens to form single bonds linking the monomers.', '[1]'),
])
t9b.fixed('C2', (2, 3, 4), [
    ('Explain why addition polymers are described as saturated even though their monomers are unsaturated.', 'The C=C double bonds in the monomers open up to form C–C single bonds in the chain, so the polymer has only single bonds.', '[2]'),
    ('Explain how the repeat unit of an addition polymer is related to its monomer.', 'It has the same atoms as the monomer, but the C=C becomes C–C with bonds extending to neighbouring units.', '[2]'),
    ('Explain why poly(ethene) does not decolourise aqueous bromine but ethene does.', 'Poly(ethene) has no C=C bonds (saturated), so no addition can occur.', '[2]'),
    ('Explain why the empirical formula of poly(ethene) is the same as that of ethene.', 'Polymerisation joins monomers without losing atoms, so the ratio C:H stays 1:2 (CH₂).', '[2]'),
])


@t9b.add('C1', (1, 2, 3))
def t9b_unit(r, D):
    m = r.choice(MONO)
    if r.random() < 0.5:
        return mcq_q(r, f'Which is the repeat unit of the polymer made from {m[0]}, {F(m[1])}?', m[2], [x[2] for x in MONO] + ['–[CH₂=CH₂]ₙ–'], f'Open the C=C: {m[2]}.')
    return mcq_q(r, f'An addition polymer has the repeat unit {m[2]}. What is the monomer?', f'{m[0]}', [x[0] for x in MONO] + ['ethane', 'propane'], f'Put the C=C back: {F(m[1])} ({m[0]}).')


@t9b.add('C3', (2, 3, 4, 5), 'numerical')
def t9b_mr(r, D):
    m = r.choice(MONO)
    n = r.choice([500, 1000, 2000, 2500, 5000, 10000, 20000])
    M = int(round(m[5] * n))
    if D >= 4:
        return {'stem': f'A sample of {m[3]} has an average relative molecular mass of {M:,}. Calculate the average number of monomer units in each chain (Mr of {m[0]} = {sf(m[5])}). Explain why it is described as an "average".',
                'answer': f'{n:,}; chains in a sample have different lengths.', 'key': f'n = {M:,}/{sf(m[5])} = {n:,} [2]; chains of different lengths [1]', 'marks': 3}
    return {'stem': f'A chain of {m[3]} contains {n:,} monomer units. Calculate its relative molecular mass (Mr of {m[0]} = {sf(m[5])}).', 'answer': f'{M:,}', 'key': f'Mr = {n:,} × {sf(m[5])} = {M:,} [2]'}


@t9b.add('C3', (1, 2, 3, 4))
def t9b_eq(r, D):
    m = r.choice(MONO)
    if D <= 2:
        return {'stem': f'Name the polymer formed from {m[0]} and give one use.', 'answer': f'{m[3]}; {m[4]}', 'key': '1 mark name; 1 mark use [2]'}
    return {'stem': f'Write an equation for the formation of {m[3]} from {m[0]}, showing the repeat unit, and explain why this is called addition polymerisation.',
            'answer': f'n {F(m[1])} → {m[2]}; monomers add together through the opened C=C bonds and no other product forms.', 'key': '1 mark n monomer; 1 mark repeat unit with ext. bonds; 1 mark explanation [3]', 'marks': 3}


@t9b.add('C2', (2, 3, 4), 'explain')
def t9b_err(r, D):
    m = r.choice(MONO)
    errs = [(f'draws the repeat unit of {m[3]} with a C=C double bond', 'The double bond opens during polymerisation; the repeat unit has only C–C single bonds with continuation bonds at each end.'),
            (f'says that water is produced when {m[0]} polymerises', 'That is condensation polymerisation; addition polymerisation gives the polymer as the only product.'),
            (f'says that {m[3]} is an alkene because it is made from {m[0]}', 'The polymer is saturated: no C=C bonds remain.')]
    e, fix = r.choice(errs)
    return {'stem': f'{person(r)} {e}. Explain the error.', 'answer': fix, 'key': '1 mark identifies error; 1 mark correct chemistry [2]'}


def _add_c4(r, D):
    m = r.choice(MONO)
    n = r.choice([1000, 2000, 5000])
    intro = r.choice([f'A factory in {city(r)} makes {m[3]} from {m[0]}, {F(m[1])}.', f'{person(r)} investigates the polymer {m[3]}, which is used for {m[4]}.', f'The monomer {m[0]} is made from chemicals obtained from crude oil and is then polymerised.'])
    parts = [
        lambda r: (f'Explain why {m[0]} can form an addition polymer.', 'It has a C=C double bond (unsaturated).', '[1]'),
        lambda r: ('Draw (describe) the repeat unit of the polymer.', m[2], '[2]'),
        lambda r: (f'Calculate the Mr of a chain containing {n} monomer units.', f'{int(round(m[5] * n)):,}', '[1]'),
        lambda r: ('State one property that makes the polymer suitable for its use.', 'e.g. flexible/strong/waterproof/unreactive/electrical insulator.', '[1]'),
        lambda r: (f'Describe a test to show that a sample of {m[0]} has been completely polymerised.', 'Add aqueous bromine: stays orange (no C=C left).', '[2]'),
        lambda r: ('State the difference between addition and condensation polymerisation.', 'Addition: only one product (the polymer); condensation: a small molecule such as water is also formed.', '[2]'),
        lambda r: ('Explain why the polymer is non-biodegradable.', 'Microorganisms cannot break the strong C–C bonds of the chain; it is unreactive.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t9b.add('C4', (2, 3, 4, 5), 'multi_step')(_add_c4)
t9b.add('C3', (3, 4), 'multi_step')(_add_c4)

# ---------------------------------------------------------- 9.3 condensation polymers
COND = [('nylon', 'polyamide', 'a dicarboxylic acid and a diamine', 'amide (–CONH–)', 'water', 'clothing, ropes and fishing nets'),
        ('PET', 'polyester', 'a dicarboxylic acid and a diol', 'ester (–COO–)', 'water', 'plastic bottles and clothing fibres'),
        ('protein', 'natural polyamide', 'amino acids', 'amide (peptide, –CONH–)', 'water', 'enzymes, muscle and hair in living things')]
t9c = topic('Condensation polymers', 'condensation polymers: nylon (polyamide), pet (polyester)', 'proteins from amino acids', 'condensation polymerisation')
t9c.fixed('C1', (1, 2), [
    ('Which linkage is found in nylon?', 'amide linkage', 'Nylon is a polyamide: –CONH– links.', ['ester linkage', 'C=C double bond', 'ionic bond']),
    ('Which small molecule is eliminated when PET is formed?', 'water', 'Diol + dicarboxylic acid → polyester + water.', ['hydrogen', 'carbon dioxide', 'ammonia']),
    ('What are the monomers of proteins?', 'amino acids', 'Amino acids join by amide (peptide) links.', ['sugars', 'fatty acids', 'alkenes']),
    ('What type of polymer is PET?', 'polyester', 'PET links are ester groups.', ['polyamide', 'addition polymer', 'protein']),
    ('Which pair of monomers can form a polyamide?', 'a dicarboxylic acid and a diamine', 'Each –COOH reacts with an –NH₂, eliminating water.', ['a diol and an alkene', 'ethene and propene', 'a diol and a dicarboxylic acid']),
    ('State what is meant by condensation polymerisation.', 'Monomers join to form a polymer with the elimination of a small molecule such as water.', '[1]'),
])
t9c.fixed('C2', (2, 3, 4), [
    ('Explain why each monomer used to make nylon must have two functional groups.', 'A functional group at each end lets the monomer link to two others, so the chain can keep growing.', '[2]'),
    ('Compare the structures of nylon and proteins.', 'Both have amide links; nylon is made from two different monomers (diamine + dicarboxylic acid) repeating, proteins from many different amino acids.', '[2]'),
    ('Explain why PET can be recycled into new PET by converting it back to monomers.', 'The ester links can be broken (hydrolysed/depolymerised) to regenerate the monomers, which are then repolymerised.', '[2]'),
    ('Explain the difference between addition and condensation polymerisation.', 'Addition: alkene monomers join, polymer is the only product. Condensation: monomers with two functional groups join, eliminating water (or HCl).', '[3]'),
])


@t9c.add('C1', (1, 2, 3))
def t9c_link(r, D):
    p = r.choice(COND)
    q = r.choice(['link', 'monomer'])
    if q == 'link':
        return mcq_q(r, f'Which linkage joins the monomer units in {p[0]}?', p[3], [x[3] for x in COND] + ['C–C single bonds from an opened C=C', 'ionic bond'], f'{p[0]} ({p[1]}): {p[3]}.')
    return mcq_q(r, f'Which monomers are used to make {p[0]}?', p[2], [x[2] for x in COND] + ['an alkene', 'a diol and an alkene'], f'{p[0]}: {p[2]}.')


@t9c.add('C2', (2, 3, 4), 'explain')
def t9c_cmp(r, D):
    a, b = r.sample(COND, 2)
    return {'stem': f'Compare {a[0]} and {b[0]} in terms of the type of monomers, the linkage formed and the small molecule eliminated.',
            'answer': f'{a[0]}: {a[2]}, {a[3]}, {a[4]}; {b[0]}: {b[2]}, {b[3]}, {b[4]}.', 'key': '1 mark monomers; 1 mark linkage; 1 mark small molecule [3]', 'marks': 3}


@t9c.add('C3', (2, 3, 4, 5))
def t9c_struct(r, D):
    kind = r.choice(['nylon', 'PET', 'protein'])
    if kind == 'nylon':
        return {'stem': 'A polyamide is made from HOOC–□–COOH and H₂N–■–NH₂ (□ and ■ represent carbon chains). Describe the repeat unit and name the linkage and the other product.',
                'answer': 'Repeat unit –[CO–□–CO–NH–■–NH]–; amide linkage –CONH–; water is eliminated.', 'key': '1 mark repeat unit; 1 mark amide link; 1 mark water [3]', 'marks': 3}
    if kind == 'PET':
        return {'stem': 'A polyester is made from HOOC–□–COOH and HO–■–OH. Describe the repeat unit and name the linkage and the other product. Name a common polyester.',
                'answer': 'Repeat unit –[CO–□–CO–O–■–O]–; ester linkage –COO–; water; PET.', 'key': '1 mark repeat unit; 1 mark ester link; 1 mark water; 1 mark PET [4]', 'marks': 4}
    n = r.choice([3, 4, 5])
    return {'stem': f'Amino acids have the general structure H₂N–CHR–COOH. Describe how {n} amino acid molecules join to form part of a protein, stating the number of water molecules eliminated and the type of linkage formed.',
            'answer': f'The –COOH of one reacts with the –NH₂ of the next; {n - 1} amide (peptide) links form and {n - 1} water molecules are eliminated.', 'key': '1 mark mechanism; 1 mark amide link; 1 mark number of water molecules [3]', 'marks': 3}


@t9c.add('C3', (2, 3, 4), 'numerical')
def t9c_water(r, D):
    n = r.choice([50, 100, 150, 200, 300, 500])
    mono = r.choice([('glycine', 75), ('alanine', 89), ('serine', 105)])
    Mp = n * mono[1] - (n - 1) * 18
    return {'stem': f'A polypeptide is made from {n} molecules of the amino acid {mono[0]} (Mr = {mono[1]}). Calculate the number of water molecules eliminated and the Mr of the polypeptide.',
            'answer': f'{n - 1}; {Mp:,}', 'key': f'{n - 1} links, so {n - 1} H₂O [1]; Mr = {n} × {mono[1]} − {n - 1} × 18 = {Mp:,} [2]', 'marks': 3}


def _cond_c4(r, D):
    p = r.choice(COND)
    intro = r.choice([f'A textile company in {city(r)} produces fibres of {p[0]}.', f'{person(r)} compares the structures of {p[0]} and poly(ethene).', f'{cap(p[0])} is a {p[1]} used for {p[5]}.'])
    parts = [
        lambda r: (f'Name the type of polymerisation used to form {p[0]}.', 'Condensation polymerisation.', '[1]'),
        lambda r: (f'State the monomers used to make {p[0]}.', p[2], '[1]'),
        lambda r: (f'Name the linkage in {p[0]}.', p[3], '[1]'),
        lambda r: ('Name the small molecule eliminated.', p[4], '[1]'),
        lambda r: (f'Explain one difference between the formation of {p[0]} and of poly(ethene).', 'Poly(ethene) forms by addition of alkene monomers with no other product; this polymer forms by condensation, eliminating water.', '[2]'),
        lambda r: ('Describe the repeat unit using block diagrams for the carbon chains.', {'nylon': '–[CO–□–CO–NH–■–NH]–', 'PET': '–[CO–□–CO–O–■–O]–', 'protein': '–[NH–CHR–CO]– (different R groups)'}[p[0]], '[2]'),
        lambda r: ('Suggest one problem caused by disposing of this polymer in landfill.' if p[0] != 'protein' else 'Explain why proteins are broken down in the body but nylon is not.',
                   'It is non-biodegradable, so it persists for many years and takes up space.' if p[0] != 'protein' else 'Enzymes hydrolyse the amide links in proteins; no enzymes break nylon down.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t9c.add('C4', (2, 3, 4, 5), 'multi_step')(_cond_c4)
t9c.add('C3', (3, 4), 'multi_step')(_cond_c4)

# ---------------------------------------------------------- 9.4 plastics
DISPOSAL = [('landfill', 'plastics are non-biodegradable and take up space for hundreds of years'), ('incineration', 'produces carbon dioxide (greenhouse gas) and toxic gases such as hydrogen chloride from PVC'),
            ('dumping in the ocean', 'harms marine animals that swallow or become trapped in plastic; microplastics enter food chains'), ('recycling', 'requires the plastics to be collected and sorted, and some types cannot be recycled')]
t9d = topic('Plastics: properties, disposal and recycling', 'plastics: properties, disposal problems and recycling of pet', 'disposal problems', 'recycling')
t9d.fixed('C1', (1, 2), [
    ('Why do plastics cause disposal problems?', 'Most are non-biodegradable', 'Microorganisms cannot break them down, so they persist.', ['They are biodegradable', 'They dissolve in rain water', 'They react with air']),
    ('Which toxic gas can be produced when PVC is burned?', 'hydrogen chloride', 'PVC contains chlorine; incineration releases HCl.', ['ammonia', 'oxygen', 'nitrogen']),
    ('How can PET be recycled into new PET?', 'It is converted back into monomers, which are repolymerised', 'Depolymerisation (hydrolysis) regenerates the monomers.', ['It is burned to release monomers', 'It is cracked into ethene', 'It is dissolved in water']),
    ('Which property makes plastics useful for food packaging?', 'They are unreactive and waterproof', 'Plastics are inert, light and can be moulded.', ['They are biodegradable', 'They conduct electricity', 'They are very dense']),
    ('Give one property of plastics that makes them useful.', 'Low density / strong / unreactive / waterproof / easily moulded / electrical insulator.', '[1]'),
])
t9d.fixed('C2', (2, 3, 4), [
    ('Explain why burning plastics is not an ideal solution to plastic waste.', 'It releases CO₂ (climate change) and can release toxic gases such as HCl or CO; though energy can be recovered.', '[2]'),
    ('Explain why plastic waste in the oceans is a problem.', 'It persists for years; animals eat it or become entangled; microplastics enter food chains.', '[2]'),
    ('Explain why the same properties that make plastics useful also cause disposal problems.', 'Their unreactivity and strength mean they do not break down/biodegrade in the environment.', '[2]'),
    ('Explain why plastics must be sorted before recycling.', 'Different polymers have different structures and properties, and must be processed separately.', '[2]'),
])


@t9d.add('C1', (1, 2, 3))
def t9d_disp(r, D):
    m, why = r.choice(DISPOSAL)
    return mcq_q(r, f'Which method of dealing with plastic waste has this drawback: it {why}?', m, [x[0] for x in DISPOSAL], f'{m}: {why}.')


@t9d.add('C2', (2, 3, 4), 'explain')
def t9d_eval(r, D):
    a, b = r.sample(DISPOSAL, 2)
    return {'stem': f'A council in {city(r)} is choosing between {a[0]} and {b[0]} for its plastic waste. Give one disadvantage of each.', 'answer': f'{cap(a[0])}: {a[1]}. {cap(b[0])}: {b[1]}.', 'key': '1 mark each disadvantage [2]'}


@t9d.add('C3', (2, 3, 4, 5), 'numerical')
def t9d_data(r, D):
    tot = r.choice([2.4, 3.6, 5.0, 8.0, 12.0])
    rec = r.choice([12, 18, 25, 30, 35])
    inc = r.choice([20, 25, 30, 40])
    land = 100 - rec - inc
    yr = r.choice([5, 10])
    return {'stem': f'A country produces {sf(tot)} million tonnes of plastic waste each year: {rec}% is recycled, {inc}% is incinerated and the rest goes to landfill. Calculate the mass sent to landfill each year and the total over {yr} years, and suggest one way to reduce it.',
            'answer': f'{g3(tot * land / 100)} million tonnes per year; {g3(tot * land / 100 * yr)} million tonnes in {yr} years; increase recycling / use biodegradable plastics / reduce single-use plastics.',
            'key': f'landfill % = {land} [1]; mass = {g3(tot * land / 100)} Mt [1]; × {yr} = {g3(tot * land / 100 * yr)} Mt [1]; suggestion [1]', 'marks': 4}


def _plas_c4(r, D):
    intro = r.choice([f'A drinks company in {city(r)} sells water in PET bottles.', f'{person(r)} carries out a survey of plastic waste on a beach.', 'A city plans to ban single-use plastic bags made of poly(ethene).'])
    parts = [
        lambda r: ('Give two properties of plastics that make them suitable for packaging.', 'Low density; strong; unreactive/does not corrode; waterproof; can be moulded.', '[2]'),
        lambda r: ('Explain why plastic waste persists in the environment.', 'Most plastics are non-biodegradable; microorganisms cannot break them down.', '[2]'),
        lambda r: ('Describe how PET is recycled.', 'Collected and sorted; cleaned; converted back into monomers (depolymerised) which are repolymerised into new PET (or melted and remoulded).', '[2]'),
        lambda r: ('Name the type of polymer PET is and its linkage.', 'Condensation polymer — polyester; ester linkage.', '[2]'),
        lambda r: ('Give two problems of disposing of plastics by incineration.', 'CO₂ released (climate change); toxic gases (HCl, CO); smoke/particulates.', '[2]'),
        lambda r: ('Suggest one advantage of incineration compared with landfill.', 'Energy can be recovered as electricity; reduces land use.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t9d.add('C4', (2, 3, 4, 5), 'multi_step')(_plas_c4)
t9d.add('C3', (3, 4), 'multi_step')(_plas_c4)

CHAPTERS[9] = [t9a, t9b, t9c, t9d]


# ===================================================================== Ch10 (CB21) Experimental design and separation techniques
APP = [('time', 'stop-watch (stopclock)', 'to 0.1 s or 1 s'), ('temperature', 'thermometer', 'to 0.5 °C or 1 °C'), ('mass', 'top-pan balance', 'to 0.01 g'),
       ('an exact volume of 25.0 cm³ of solution', 'volumetric pipette', 'to ±0.05 cm³'), ('a variable volume of acid added in a titration', 'burette', 'to the nearest 0.05 cm³'),
       ('an approximate volume of 50 cm³ of water', 'measuring cylinder', 'to about 1 cm³'), ('the volume of gas given off in a reaction', 'gas syringe', 'to about 1 cm³')]

t10a = topic('Apparatus and measurement', 'choosing apparatus to measure time, temperature, mass and volume', 'accuracy of measurements', 'apparatus')
t10a.fixed('C1', (1, 2), [
    ('Which apparatus measures 25.0 cm³ of solution most accurately?', 'volumetric pipette', 'A pipette delivers a fixed volume accurately (±0.05 cm³).', ['beaker', 'measuring cylinder', 'conical flask']),
    ('Which apparatus is used to measure the volume of gas produced in a reaction?', 'gas syringe', 'A gas syringe (or inverted measuring cylinder/burette over water).', ['pipette', 'thermometer', 'balance']),
    ('To what precision is a burette normally read?', 'to the nearest 0.05 cm³', 'Burette readings are recorded to two decimal places, ending in 0 or 5.', ['to the nearest 1 cm³', 'to the nearest 0.5 cm³', 'to the nearest 10 cm³']),
    ('Which unit is used for volumes measured with a burette?', 'cm³', 'Laboratory volumes are given in cm³ (dm³ for larger volumes).', ['kg', 'mol', 'm²']),
    ('How should the volume in a measuring cylinder be read?', 'at the bottom of the meniscus with the eye level with it', 'Avoids parallax error.', ['at the top of the meniscus from above', 'at the side of the cylinder', 'from below the cylinder']),
    ('Name the apparatus used to measure the mass of a solid.', 'A (top-pan) balance.', '[1]'),
])
t10a.fixed('C2', (2, 3, 4), [
    ('Explain why a burette is used rather than a measuring cylinder to add acid in a titration.', 'A burette measures variable volumes much more precisely (to 0.05 cm³) and allows drop-by-drop addition near the end-point.', '[2]'),
    ('Explain why it is good practice to repeat measurements.', 'To identify anomalous results and calculate a reliable mean.', '[2]'),
    ('Explain why a thermometer reading 0.1 °C intervals is better than one reading 1 °C intervals when measuring a temperature rise of 3 °C.', 'The smaller scale division gives a smaller relative uncertainty, so the temperature change is more accurate.', '[2]'),
    ('Explain why the mass of a reaction flask is recorded as soon as the reactants are mixed in a rate experiment.', 'Gas begins escaping immediately, so a late reading would be too low and the initial mass would be wrong.', '[2]'),
])


@t10a.add('C1', (1, 2, 3))
def t10a_app(r, D):
    q, a, res = r.choice(APP)
    return mcq_q(r, f'Which apparatus is most suitable for measuring {q}?', a, [x[1] for x in APP], f'{a} — reads {res}.')


@t10a.add('C3', (1, 2, 3, 4), 'numerical')
def t10a_burette(r, D):
    i = round(r.choice([0.00, 0.50, 1.20, 2.35, 3.10, 0.85, 1.65, 4.20]), 2)
    t = round(r.choice([18.45, 21.30, 22.65, 24.10, 19.95, 23.85, 25.40, 20.75]), 2)
    f = round(i + t, 2)
    if D == 1:
        return nmcq(r, f'A burette reads {i:.2f} cm³ at the start of a titration and {f:.2f} cm³ at the end-point. What volume was added?', t, [f, i + f, t + 1, t - 0.5, t + 0.5, t - 1, t + 0.05], ' cm³', f'titre = {f:.2f} − {i:.2f} = {t:.2f} cm³.', f=lambda x: f'{x:.2f}')
    if D >= 3:
        t2 = round(t + r.choice([0.05, 0.10, -0.05]), 2)
        t3 = round(t + r.choice([0.6, 0.8, -0.7]), 2)
        conc = sorted([t, t2])
        return {'stem': f'Three titres from a titration are {t:.2f} cm³, {t3:.2f} cm³ and {t2:.2f} cm³. Identify the concordant titres, calculate the mean titre, and explain why the other result is not used.',
                'answer': f'{t:.2f} and {t2:.2f}; mean {(t + t2) / 2:.2f} cm³; {t3:.2f} cm³ differs by more than 0.10 cm³ (anomalous).', 'key': '1 mark concordant pair; 1 mark mean; 1 mark reason [3]', 'marks': 3}
    return {'stem': f'In a titration, the initial burette reading is {i:.2f} cm³ and the final reading is {f:.2f} cm³. Calculate the titre and state the precision to which burette readings are recorded.',
            'answer': f'{t:.2f} cm³; to the nearest 0.05 cm³', 'key': '1 mark subtraction; 1 mark precision [2]'}


@t10a.add('C3', (2, 3, 4), 'numerical')
def t10a_temp(r, D):
    T1 = r.choice([18.5, 19.0, 20.5, 21.0, 22.5, 23.0])
    dT = r.choice([4.5, 6.0, 7.5, 9.0, 12.5, 15.0, 3.5])
    T2 = T1 + dT
    exo = r.random() < 0.7
    if not exo:
        T2 = T1 - dT
    return {'stem': f'In an experiment the starting temperature was {T1:.1f} °C and the {"highest" if exo else "lowest"} temperature reached was {T2:.1f} °C. Calculate the temperature change and state whether the reaction is exothermic or endothermic. Suggest one improvement to the apparatus to reduce heat loss.',
            'answer': f'{"+" if exo else "−"}{dT:.1f} °C; {"exothermic" if exo else "endothermic"}; use an insulated (polystyrene) cup with a lid.', 'key': '1 mark change; 1 mark type; 1 mark improvement [3]', 'marks': 3}


@t10a.add('C2', (2, 3, 4), 'explain')
def t10a_err(r, D):
    errs = [('measured 25 cm³ of alkali for a titration using a beaker', 'A beaker is not accurate; use a 25.0 cm³ volumetric pipette.'),
            ('read the burette from above the meniscus', 'Reading must be at eye level with the bottom of the meniscus to avoid parallax error.'),
            ('used a measuring cylinder to find the volume of hydrogen collected over 10 s intervals', 'It is better to use a gas syringe, which gives a direct and more precise reading as gas is produced.'),
            ('timed a reaction by counting seconds out loud', 'Use a stop-watch for precise timing.'),
            ('weighed a solid on a balance without first setting it to zero with the container', 'The mass of the container would be included; tare the balance or subtract the container mass.')]
    e, fix = r.choice(errs)
    return {'stem': f'In {lab(r)}, {person(r)} {e}. Explain why this is a poor technique and suggest an improvement.', 'answer': fix, 'key': '1 mark reason; 1 mark improvement [2]'}


def _app_c4(r, D):
    rx = r.choice([('magnesium ribbon with dilute hydrochloric acid', 'hydrogen'), ('marble chips (calcium carbonate) with dilute hydrochloric acid', 'carbon dioxide'), ('zinc granules with dilute sulfuric acid', 'hydrogen')])
    times = [0, 20, 40, 60, 80, 100]
    vmax = r.choice([48, 60, 72, 84, 96])
    hl = r.choice([20, 25, 30])
    vols = [round(vmax * (1 - 0.5 ** (t / hl))) for t in times]
    intro = f'{person(r)} investigates the reaction of {rx[0]} by measuring the volume of {rx[1]} produced every 20 s. Results (time / s, volume / cm³): ' + '; '.join(f'{t}, {v}' for t, v in zip(times, vols)) + '.'
    parts = [
        lambda r: ('Name the apparatus used to measure the volume of gas.', 'Gas syringe.', '[1]'),
        lambda r: ('Name the apparatus used to measure time.', 'Stop-watch.', '[1]'),
        lambda r: ('Calculate the mean rate of reaction over the first 40 s.', f'{g3(vols[2] / 40)} cm³/s', f'{vols[2]}/40 [2]'),
        lambda r: ('State and explain how the rate changes during the experiment.', 'Rate decreases: the concentration of acid (and amount of solid) falls, so collisions are less frequent.', '[2]'),
        lambda r: ('Suggest how the volume of acid should be measured, and why.', 'Measuring cylinder is adequate (the acid is in excess) — or a pipette/burette for greater accuracy.', '[1]'),
        lambda r: ('Identify one variable that must be controlled.', 'Temperature, concentration/volume of acid, or mass/surface area of the solid.', '[1]'),
        lambda r: ('Suggest why the results become less reliable if the bung is not inserted quickly.', 'Some gas escapes before it can be collected, so readings are too low.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t10a.add('C4', (2, 3, 4, 5), 'case')(_app_c4)
t10a.add('C3', (3, 4), 'case')(_app_c4)

# ---------------------------------------------------------- 10.2 solutions and choosing separation
MIXES = [('sand from a mixture of sand and water', 'filtration', 'sand is insoluble and stays on the filter paper'), ('salt crystals from salt solution', 'crystallisation (evaporation)', 'water is removed so the dissolved salt is left'),
         ('pure water from sea water', 'simple distillation', 'water boils and is condensed, leaving the dissolved salts'), ('ethanol from a mixture of ethanol and water', 'fractional distillation', 'the liquids have different boiling points (78 °C and 100 °C)'),
         ('the dyes in a black ink', 'paper chromatography', 'the dyes have different solubilities in the solvent and travel different distances'), ('copper(II) sulfate crystals from a mixture with sand', 'dissolve, filter, then crystallise', 'copper(II) sulfate is soluble but sand is not'),
         ('nitrogen and oxygen from liquid air', 'fractional distillation', 'they have different boiling points'), ('chalk (calcium carbonate) from a suspension in water', 'filtration', 'chalk is insoluble'),
         ('the coloured pigments in a leaf extract', 'paper chromatography', 'the pigments travel different distances on the paper'), ('petrol from crude oil', 'fractional distillation', 'the hydrocarbons have different boiling points')]
SOLY = {'potassium nitrate': [(20, 32), (40, 64), (60, 110), (80, 169)], 'ammonium chloride': [(20, 37), (40, 46), (60, 55), (80, 66)], 'potassium chloride': [(20, 34), (40, 40), (60, 46), (80, 51)],
        'copper(II) sulfate': [(20, 32), (40, 45), (60, 62), (80, 84)], 'sodium chloride': [(20, 36), (40, 37), (60, 37), (80, 38)]}

t10b = topic('Solutions and choosing a separation method', 'solvents, solutes, solutions and saturated solutions', 'choosing a separation method', 'saturated solution')
t10b.fixed('C1', (1, 2), [
    ('What is a saturated solution?', 'A solution containing the maximum amount of solute that can dissolve at that temperature', 'No more solute dissolves at that temperature.', ['A solution that contains no solute', 'Any coloured solution', 'A solution that conducts electricity']),
    ('In salt solution, what is the solvent?', 'water', 'Solvent = the liquid that dissolves the solute (salt).', ['salt', 'the solution', 'the residue']),
    ('The substance left on the filter paper after filtration is called the', 'residue', 'Residue stays in the paper; filtrate passes through.', ['filtrate', 'solvent', 'distillate']),
    ('Which method separates a soluble solid from a solution?', 'crystallisation', 'Evaporate some solvent, then cool to form crystals.', ['filtration', 'chromatography', 'fractional distillation']),
    ('Which word describes the substance that dissolves in a solvent?', 'solute', 'Solute + solvent → solution.', ['residue', 'filtrate', 'precipitate']),
    ('State the meaning of the term "solution".', 'A mixture of one or more solutes dissolved in a solvent.', '[1]'),
])
t10b.fixed('C2', (2, 3, 4), [
    ('Explain why crystals form when a hot saturated solution of potassium nitrate is cooled.', 'Solubility decreases as temperature falls, so the solution can hold less solute and the excess crystallises out.', '[2]'),
    ('Explain why simple distillation cannot separate ethanol from water efficiently.', 'Their boiling points are close, so both evaporate; a fractionating column is needed to separate them.', '[2]'),
    ('Explain the difference between dissolving and melting.', 'Dissolving: solute particles spread among solvent particles to form a solution; melting: a solid turns into a liquid on heating — one substance only.', '[2]'),
    ('Explain why salt cannot be removed from sea water by filtration.', 'The salt is dissolved; its particles pass through the filter paper with the water.', '[2]'),
])


@t10b.add('C1', (1, 2, 3))
def t10b_method(r, D):
    tgt, m, why = r.choice(MIXES)
    return mcq_q(r, f'Which method is used to obtain {tgt}?', m, list({x[1] for x in MIXES}) + ['decanting with a magnet'], f'{m}: {why}.')


@t10b.add('C2', (2, 3, 4), 'explain')
def t10b_why(r, D):
    tgt, m, why = r.choice(MIXES)
    return {'stem': f'Suggest a method to obtain {tgt} and explain why it works.', 'answer': f'{cap(m)}: {why}.', 'key': '1 mark method; 1 mark explanation [2]'}


@t10b.add('C3', (2, 3, 4, 5), 'numerical')
def t10b_sol(r, D):
    salt = r.choice([k for k in SOLY if k != 'sodium chloride'])
    data = SOLY[salt]
    (Th, sh), (Tc, sc) = r.sample(data[1:], 1)[0], r.choice(data[:1])
    if Th < Tc:
        (Th, sh), (Tc, sc) = (Tc, sc), (Th, sh)
    w = r.choice([50, 100, 200, 25])
    tbl = '; '.join(f'{T} °C: {s} g' for T, s in data)
    m = (sh - sc) * w / 100
    if D >= 4:
        return {'stem': f'Solubility of {salt} in g per 100 g of water — {tbl}. A saturated solution in {w} g of water at {Th} °C is cooled to {Tc} °C. Calculate the mass of crystals formed, and explain why sodium chloride could not be purified well this way.',
                'answer': f'{sf(m)} g; sodium chloride’s solubility hardly changes with temperature, so few crystals form on cooling.', 'key': f'({sh} − {sc}) g per 100 g [1]; × {w}/100 = {sf(m)} g [2]; NaCl solubility nearly constant [1]', 'marks': 4}
    sep = ' Describe how the crystals are then separated from the solution and dried.' if D == 3 else ''
    return {'stem': f'Solubility of {salt} in g per 100 g of water — {tbl}. Calculate the mass of {salt} that crystallises when a saturated solution in {w} g of water is cooled from {Th} °C to {Tc} °C.{sep}',
            'answer': f'{sf(m)} g' + ('; filter, wash with a little cold distilled water and dry between filter papers (or in a warm oven).' if sep else ''),
            'key': f'difference = {sh} − {sc} = {sh - sc} g per 100 g [1]; × {w}/100 = {sf(m)} g [1]' + ('; filter, wash and dry [1]' if sep else ''), 'marks': 3 if sep else 2}


@t10b.add('C3', (1, 2, 3))
def t10b_terms(r, D):
    sol = r.choice([('sugar', 'water', 'sugar solution'), ('iodine', 'ethanol', 'iodine solution'), ('salt', 'water', 'brine'), ('copper(II) sulfate', 'water', 'blue copper(II) sulfate solution'), ('sulfur', 'methylbenzene', 'sulfur solution')])
    term = r.choice(['solute', 'solvent', 'solution'])
    ans = {'solute': sol[0], 'solvent': sol[1], 'solution': sol[2]}[term]
    return mcq_q(r, f'{cap(sol[0])} dissolves in {sol[1]} to form {sol[2]}. What is the {term}?', ans, [sol[0], sol[1], sol[2], 'the residue', 'the filtrate'], f'solute {sol[0]}; solvent {sol[1]}; solution {sol[2]}.')


def _sep_c4(r, D):
    mix = r.choice([('a mixture of sand, salt and water', ['filter to remove sand (residue)', 'evaporate/crystallise the filtrate to obtain salt', 'or distil the filtrate to collect pure water']),
                    ('rock salt (salt mixed with insoluble rock)', ['crush and dissolve in warm water, stirring', 'filter to remove insoluble rock', 'heat filtrate to crystallisation point and cool; filter and dry crystals']),
                    ('a solution of ethanol, water and a dissolved coloured dye', ['fractional distillation to collect ethanol at 78 °C', 'then water at 100 °C', 'dye left in flask; check purity by chromatography']),
                    ('a mixture of copper(II) oxide powder and copper(II) sulfate crystals', ['add water and stir to dissolve copper(II) sulfate', 'filter: copper(II) oxide is the residue', 'crystallise the filtrate to obtain copper(II) sulfate'])])
    salt = r.choice(['potassium nitrate', 'ammonium chloride'])
    data = SOLY[salt]
    intro = r.choice([f'{person(r)} is given {mix[0]} and asked to obtain pure samples of the components.', f'A technician in {city(r)} must separate {mix[0]}.'])
    parts = [
        lambda r: ('Describe a method to separate the components.', '; '.join(mix[1]) + '.', '1 mark each step [3]'),
        lambda r: ('Define the terms solute and solvent.', 'Solute: substance that dissolves; solvent: liquid in which it dissolves.', '[2]'),
        lambda r: ('Explain why the filtrate is not evaporated to dryness when making crystals.', 'Crystals would be small/impure and lose water of crystallisation; heat to saturation and cool instead.', '[2]'),
        lambda r: (f'The solubility of {salt} is {data[0][1]} g per 100 g water at {data[0][0]} °C and {data[2][1]} g at {data[2][0]} °C. Calculate the mass crystallising when a saturated solution in 100 g of water is cooled from {data[2][0]} °C to {data[0][0]} °C.', f'{data[2][1] - data[0][1]} g', '[1]'),
        lambda r: ('State what is meant by a saturated solution.', 'One in which no more solute can dissolve at that temperature.', '[1]'),
        lambda r: ('Describe how you could show that the water collected is pure.', 'Measure its boiling point: 100 °C exactly (or freezing point 0 °C).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t10b.add('C4', (2, 3, 4, 5), 'case')(_sep_c4)
t10b.add('C3', (3, 4), 'case')(_sep_c4)

# ---------------------------------------------------------- 10.3 techniques
TECH = [('filtration', 'separating an insoluble solid from a liquid', ['filter funnel', 'filter paper', 'conical flask or beaker']),
        ('crystallisation', 'obtaining a soluble solid from its solution', ['evaporating basin', 'Bunsen burner and tripod (or water bath)', 'glass rod to test for the point of crystallisation']),
        ('simple distillation', 'separating a solvent from a solution', ['distillation flask', 'thermometer at the side-arm', 'Liebig condenser with water in at the bottom']),
        ('fractional distillation', 'separating miscible liquids with different boiling points', ['round-bottomed flask', 'fractionating column packed with glass beads', 'thermometer and condenser'])]
LIQS = [('ethanol', 78), ('water', 100), ('methanol', 65), ('propan-1-ol', 97), ('hexane', 69), ('cyclohexane', 81), ('ethanoic acid', 118), ('butan-1-ol', 117)]

t10c = topic('Filtration, crystallisation and distillation', 'filtration, crystallisation, simple distillation and fractional distillation', 'distillation', 'crystallisation filtration')
t10c.fixed('C1', (1, 2), [
    ('In simple distillation, where should the thermometer bulb be placed?', 'next to the side-arm leading to the condenser', 'It measures the temperature of the vapour entering the condenser.', ['in the liquid being heated', 'at the bottom of the condenser', 'in the collecting beaker']),
    ('Why does cold water enter the condenser at the bottom?', 'So that the condenser fills completely and cools efficiently', 'Counter-current flow keeps the jacket full.', ['So that the water boils', 'To make the vapour flow faster', 'To stop the thermometer breaking']),
    ('What is the purpose of the fractionating column?', 'To separate liquids with close boiling points by repeated condensation and evaporation', 'The column has a temperature gradient: the lower-b.p. liquid reaches the top first.', ['To heat the mixture', 'To filter out solids', 'To cool the condenser water']),
    ('How do you know when the point of crystallisation has been reached?', 'Crystals form on a cold glass rod dipped into the solution', 'A drop on a glass rod crystallises as it cools.', ['The solution boils', 'All the water has gone', 'The solution changes colour']),
    ('Which liquid distils first from a mixture of ethanol (b.p. 78 °C) and water (b.p. 100 °C)?', 'ethanol', 'Lower boiling point distils first.', ['water', 'both together at 89 °C', 'neither']),
    ('Name the liquid collected after distillation.', 'The distillate.', '[1]'),
])
t10c.fixed('C2', (2, 3, 4), [
    ('Explain why anti-bumping granules are added to the flask during distillation.', 'They give smooth boiling and prevent large bubbles forming suddenly (bumping).', '[1]'),
    ('Explain how simple distillation obtains pure water from salt solution.', 'Water boils and its vapour passes into the condenser, where it cools and condenses; salt has a very high boiling point so stays in the flask.', '[3]'),
    ('Explain why a water bath is used instead of a Bunsen flame when distilling ethanol.', 'Ethanol is flammable; a water bath heats gently without a naked flame and to below 100 °C.', '[2]'),
    ('Explain why the temperature at the top of the fractionating column stays constant while a fraction is being collected.', 'Only one pure substance is reaching the thermometer, so the temperature equals its boiling point.', '[2]'),
])


@t10c.add('C1', (1, 2, 3))
def t10c_app(r, D):
    t, purpose, app = r.choice(TECH)
    a = r.choice(app)
    return mcq_q(r, f'Which separation technique uses {a}?', t, [x[0] for x in TECH] + ['chromatography'], f'{t} ({purpose}) uses {", ".join(app)}.')


@t10c.add('C3', (2, 3, 4))
def t10c_frac(r, D):
    a, b = r.sample(LIQS, 2)
    lo, hi = sorted([a, b], key=lambda x: x[1])
    if abs(a[1] - b[1]) < 3:
        return None
    return {'stem': f'A mixture of {a[0]} (b.p. {a[1]} °C) and {b[0]} (b.p. {b[1]} °C) is separated by fractional distillation. State which liquid is collected first, the thermometer reading while it distils, and how you would know when the second liquid starts to distil.',
            'answer': f'{lo[0]} first, at {lo[1]} °C; the temperature rises again and stays constant at {hi[1]} °C when {hi[0]} distils.', 'key': '1 mark first liquid; 1 mark temperature; 1 mark sign of second fraction [3]', 'marks': 3}


@t10c.add('C2', (2, 3, 4), 'explain')
def t10c_err(r, D):
    errs = [('placed the thermometer bulb in the boiling liquid during distillation', 'It reads the liquid temperature, not the vapour; place it at the side-arm.'),
            ('connected the condenser so cooling water entered at the top', 'The condenser would not fill fully and cooling would be poor; water should enter at the bottom.'),
            ('heated the solution to dryness to make crystals', 'This gives powder/decomposition and removes water of crystallisation; heat to saturation and cool.'),
            ('sealed the end of the condenser with a bung', 'Pressure would build up and could cause an explosion; the system must be open to the air.'),
            ('used a Bunsen burner to heat ethanol directly', 'Ethanol is flammable; use an electric heater or water bath.')]
    e, fix = r.choice(errs)
    return {'stem': f'During a separation, {person(r)} {e}. Explain what is wrong and how to correct it.', 'answer': fix, 'key': '1 mark problem; 1 mark correction [2]'}


@t10c.add('C3', (2, 3, 4, 5))
def t10c_plan(r, D):
    t, purpose, app = r.choice(TECH)
    ex = {'filtration': 'obtain solid barium sulfate from a reaction mixture', 'crystallisation': 'obtain crystals of copper(II) sulfate from its solution', 'simple distillation': 'obtain pure water from tap water',
          'fractional distillation': 'separate ethanol from a fermented mixture'}[t]
    return {'stem': f'Describe how you would {ex} using {t}. Name the key apparatus.', 'answer': f'{cap(t)} ({purpose}): ' + '; '.join(app) + '.', 'key': '1 mark each correct step/apparatus, max [3]', 'marks': 3}


def _dist_c4(r, D):
    a, b = r.sample([x for x in LIQS], 2)
    lo, hi = sorted([a, b], key=lambda x: x[1])
    if hi[1] - lo[1] < 5:
        return None
    intro = r.choice([f'{person(r)} separates a mixture of {a[0]} and {b[0]} using fractional distillation.', f'A perfume company in {city(r)} purifies {lo[0]} from a mixture with {hi[0]}.',
                      f'A diagram shows a flask containing {a[0]} and {b[0]}, a fractionating column, a thermometer, a condenser and a receiver.'])
    parts = [
        lambda r: ('Explain why fractional distillation, rather than simple distillation, is used.', 'The liquids are miscible with boiling points fairly close together; the column gives better separation.', '[2]'),
        lambda r: (f'State which liquid is collected first and the thermometer reading.', f'{lo[0]} at {lo[1]} °C', '[2]'),
        lambda r: ('Describe what happens inside the fractionating column.', 'Vapours repeatedly condense and re-evaporate on the glass beads; the more volatile liquid rises to the top.', '[2]'),
        lambda r: ('Explain why the water enters the condenser at the bottom.', 'The jacket stays full of cold water so cooling is efficient.', '[1]'),
        lambda r: ('Suggest how the purity of the first fraction could be checked.', f'Measure its boiling point: pure {lo[0]} boils sharply at {lo[1]} °C.', '[1]'),
        lambda r: ('State one safety precaution.', 'Heat with a water bath/electric heater if flammable; do not heat to dryness; use anti-bumping granules; goggles.', '[1]'),
        lambda r: ('Name one industrial process that uses fractional distillation.', 'Separating crude oil into fractions (or liquid air).', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t10c.add('C4', (2, 3, 4, 5), 'case')(_dist_c4)
t10c.add('C3', (3, 4), 'case')(_dist_c4)

# ---------------------------------------------------------- 10.4 chromatography and purity
MPS = [('aspirin', 135), ('paracetamol', 169), ('benzoic acid', 122), ('naphthalene', 80), ('stearic acid', 69), ('salicylic acid', 159), ('caffeine', 236), ('vanillin', 82)]
t10d = topic('Chromatography and purity', 'paper chromatography, locating agents and rf values', 'assessing purity from melting and boiling points', 'chromatography')
t10d.fixed('C1', (1, 2), [
    ('Why is the baseline on a chromatogram drawn in pencil rather than ink?', 'Pencil does not dissolve in the solvent', 'Ink would dissolve and move up the paper, confusing the results.', ['Pencil is easier to see', 'Ink would react with the paper', 'Pencil helps the solvent rise']),
    ('What is a locating agent used for?', 'To make colourless spots visible', 'Spots of colourless substances (e.g. amino acids) are sprayed with a locating agent and appear coloured.', ['To move the spots faster', 'To stop the solvent evaporating', 'To dissolve the sample']),
    ('A pure substance on a chromatogram gives', 'one spot', 'A mixture gives several spots; a pure substance gives a single spot.', ['two spots', 'no spots', 'a spot on the baseline only']),
    ('How does an impurity affect the melting point of a solid?', 'It lowers it and makes it melt over a range of temperatures', 'Pure solids melt sharply at a fixed temperature.', ['It raises it sharply', 'It has no effect', 'It makes it melt at exactly 100 °C']),
    ('Why must the baseline be above the level of the solvent?', 'So that the spots do not dissolve directly into the solvent in the beaker', 'Otherwise the sample washes off into the solvent.', ['So the solvent rises faster', 'To keep the paper dry', 'To prevent evaporation']),
    ('State the formula for calculating an Rf value.', 'Rf = distance travelled by the substance ÷ distance travelled by the solvent front.', '[1]'),
])
t10d.fixed('C2', (2, 3, 4), [
    ('Explain why different substances travel different distances on a chromatogram.', 'They have different solubilities in the solvent and different attraction to the paper; more soluble substances travel further.', '[2]'),
    ('Explain why a lid is placed on the beaker during chromatography.', 'To keep the atmosphere saturated with solvent vapour so the solvent does not evaporate from the paper.', '[1]'),
    ('Explain why an Rf value is always less than 1.', 'The substance cannot travel further than the solvent front.', '[1]'),
    ('Explain why the purity of substances such as drugs and foods is important.', 'Impurities could be harmful/toxic or reduce effectiveness.', '[2]'),
])


@t10d.add('C3', (1, 2, 3, 4), 'numerical')
def t10d_rf(r, D):
    front = r.choice([8.0, 9.0, 10.0, 12.0, 7.5, 11.0])
    rf = r.choice([0.20, 0.25, 0.35, 0.40, 0.45, 0.50, 0.60, 0.65, 0.72, 0.80])
    d = round(front * rf, 1)
    rfv = d / front
    if D == 1:
        return nmcq(r, f'A spot travels {sf(d, 2)} cm and the solvent front travels {sf(front, 2)} cm. What is the Rf value?', rfv, [front / d, rfv * 2 if rfv < 0.5 else rfv / 2, d, 1 - rfv], '', f'Rf = {sf(d, 2)}/{sf(front, 2)} = {sf(rfv, 2)}.', f=lambda x: sf(x, 2))
    if D >= 3:
        refs = r.sample([('A', 0.20), ('B', 0.35), ('C', 0.50), ('D', 0.65), ('E', 0.80), ('F', 0.45)], 3)
        tgt = min(refs, key=lambda x: abs(x[1] - rfv))
        ok = abs(tgt[1] - rfv) < 0.03
        return {'stem': f'In a chromatogram, an unknown dye moves {sf(d, 2)} cm and the solvent front moves {sf(front, 2)} cm. The Rf values of known dyes in the same solvent are: ' + ', '.join(f'{L} {v:.2f}' for L, v in refs) + '. Calculate the Rf of the unknown and deduce which dye it could be.',
                'answer': f'Rf = {sf(rfv, 2)}; ' + (f'it matches dye {tgt[0]}.' if ok else 'it does not match any of the known dyes.'), 'key': '1 mark Rf; 1 mark matching conclusion; 1 mark same solvent/conditions [3]', 'marks': 3}
    return {'stem': f'A spot moved {sf(d, 2)} cm from the baseline and the solvent front moved {sf(front, 2)} cm. Calculate the Rf value.', 'answer': sf(rfv, 2), 'key': f'Rf = {sf(d, 2)}/{sf(front, 2)} [1] = {sf(rfv, 2)} [1]'}


@t10d.add('C3', (2, 3, 4))
def t10d_pure(r, D):
    nm, mp = r.choice(MPS)
    pure = r.random() < 0.5
    obs = f'melts sharply at {mp} °C' if pure else f'melts over the range {mp - r.choice([4, 6, 8])}–{mp - 1} °C'
    return {'stem': f'Pure {nm} melts at {mp} °C. A sample made by {person(r)} {obs}. Deduce whether the sample is pure and explain your answer.',
            'answer': ('Pure: it has a sharp melting point equal to the data value.' if pure else 'Impure: impurities lower the melting point and make it melt over a range.'), 'key': '1 mark conclusion; 1 mark reason [2]'}


@t10d.add('C1', (1, 2, 3))
def t10d_spots(r, D):
    n = r.choice([1, 2, 3, 4])
    stem = f'A food colouring produces {n} spot{"s" if n > 1 else ""} on a chromatogram. What does this show?'
    corr = 'It is a pure substance' if n == 1 else f'It is a mixture of at least {n} substances'
    return mcq_q(r, stem, corr, ['It is a pure substance', 'It is a mixture of at least 2 substances', 'It is a mixture of at least 3 substances', 'It is a mixture of at least 4 substances', 'It contains no dyes'], f'Each spot is a different substance; {n} spot(s).')


def _chrom_c4(r, D):
    front = r.choice([8.0, 10.0, 12.0])
    dyes = r.sample([('red', 0.25), ('yellow', 0.70), ('blue', 0.45), ('green', 0.60), ('orange', 0.35)], 3)
    ink = r.sample(dyes, 2)
    intro = f'{person(r)} uses paper chromatography to test a black ink. Known dyes {", ".join(d[0] for d in dyes)} are spotted next to the ink. The solvent front moves {sf(front, 2)} cm. The ink gives two spots, at {sf(front * ink[0][1], 2)} cm and {sf(front * ink[1][1], 2)} cm; the known dyes travel ' + ', '.join(f'{d[0]} {sf(front * d[1], 2)} cm' for d in dyes) + '.'
    parts = [
        lambda r: ('Calculate the Rf values of the two spots in the ink.', f'{ink[0][1]:.2f} and {ink[1][1]:.2f}', '[2]'),
        lambda r: ('Identify the dyes present in the ink.', f'{ink[0][0]} and {ink[1][0]}', '[2]'),
        lambda r: ('Explain why the baseline is drawn in pencil.', 'Pencil is insoluble in the solvent and will not run.', '[1]'),
        lambda r: ('Explain why the solvent level must be below the baseline.', 'Otherwise the spots dissolve into the solvent in the beaker.', '[1]'),
        lambda r: ('Describe how a colourless amino acid could be seen on a chromatogram.', 'Dry the paper and spray with a locating agent; spots become visible.', '[2]'),
        lambda r: ('Suggest why the Rf values must be compared using the same solvent.', 'Rf values depend on the solvent (and temperature/paper).', '[1]'),
        lambda r: ('Explain how chromatography separates the dyes.', 'Dyes have different solubilities in the solvent/attractions to the paper so travel different distances.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t10d.add('C4', (2, 3, 4, 5), 'case')(_chrom_c4)
t10d.add('C3', (3, 4), 'case')(_chrom_c4)

CHAPTERS[10] = [t10a, t10b, t10c, t10d]


# ===================================================================== Ch11 (CB22) Chemical analysis
CATION_T = [  # ion, name, NaOH(aq), excess NaOH, NH3(aq), excess NH3
    ('Al³⁺', 'aluminium', 'white precipitate', 'soluble in excess, giving a colourless solution', 'white precipitate', 'insoluble in excess'),
    ('NH₄⁺', 'ammonium', 'ammonia produced on warming (damp red litmus turns blue)', '—', '—', '—'),
    ('Ca²⁺', 'calcium', 'white precipitate', 'insoluble in excess', 'no precipitate or very slight white precipitate', '—'),
    ('Cr³⁺', 'chromium(III)', 'green precipitate', 'soluble in excess', 'green precipitate', 'insoluble in excess'),
    ('Cu²⁺', 'copper(II)', 'light blue precipitate', 'insoluble in excess', 'light blue precipitate', 'soluble in excess, giving a dark blue solution'),
    ('Fe²⁺', 'iron(II)', 'green precipitate', 'insoluble in excess', 'green precipitate', 'insoluble in excess'),
    ('Fe³⁺', 'iron(III)', 'red-brown precipitate', 'insoluble in excess', 'red-brown precipitate', 'insoluble in excess'),
    ('Zn²⁺', 'zinc', 'white precipitate', 'soluble in excess, giving a colourless solution', 'white precipitate', 'soluble in excess, giving a colourless solution')]
FLAME = [('Li⁺', 'lithium', 'red'), ('Na⁺', 'sodium', 'yellow'), ('K⁺', 'potassium', 'lilac'), ('Ca²⁺', 'calcium', 'orange-red'), ('Ba²⁺', 'barium', 'light green'), ('Cu²⁺', 'copper(II)', 'blue-green')]
HYDROX = {'Cu²⁺': 'Cu²⁺(aq) + 2OH⁻(aq) → Cu(OH)₂(s)', 'Fe²⁺': 'Fe²⁺(aq) + 2OH⁻(aq) → Fe(OH)₂(s)', 'Fe³⁺': 'Fe³⁺(aq) + 3OH⁻(aq) → Fe(OH)₃(s)', 'Zn²⁺': 'Zn²⁺(aq) + 2OH⁻(aq) → Zn(OH)₂(s)',
          'Al³⁺': 'Al³⁺(aq) + 3OH⁻(aq) → Al(OH)₃(s)', 'Ca²⁺': 'Ca²⁺(aq) + 2OH⁻(aq) → Ca(OH)₂(s)', 'Cr³⁺': 'Cr³⁺(aq) + 3OH⁻(aq) → Cr(OH)₃(s)'}

t11a = topic('Tests for aqueous cations and flame tests', 'identifying aqueous cations with sodium hydroxide and aqueous ammonia', 'flame tests', 'cations')
t11a.fixed('C1', (1, 2), [
    ('Which cation gives a light blue precipitate with aqueous sodium hydroxide?', 'Cu²⁺', 'Cu²⁺ + 2OH⁻ → Cu(OH)₂, light blue, insoluble in excess.', ['Fe²⁺', 'Fe³⁺', 'Zn²⁺']),
    ('Which two cations give white precipitates with aqueous sodium hydroxide that dissolve in excess?', 'Al³⁺ and Zn²⁺', 'Both hydroxides are amphoteric; Ca(OH)₂ does not dissolve in excess.', ['Ca²⁺ and Zn²⁺', 'Al³⁺ and Ca²⁺', 'Fe²⁺ and Fe³⁺']),
    ('How can Al³⁺ and Zn²⁺ be distinguished?', 'Add excess aqueous ammonia: only the zinc hydroxide dissolves', 'Zn(OH)₂ dissolves in excess NH₃(aq); Al(OH)₃ does not.', ['Add sodium hydroxide: only Al³⁺ gives a precipitate', 'Flame test: both give lilac', 'Add acid: only Zn²⁺ fizzes']),
    ('What colour is the flame test for potassium ions?', 'lilac', 'K⁺ lilac; Na⁺ yellow; Li⁺ red; Ca²⁺ orange-red; Ba²⁺ light green; Cu²⁺ blue-green.', ['yellow', 'red', 'blue-green']),
    ('Which test identifies the ammonium ion?', 'Warm with aqueous sodium hydroxide and test the gas with damp red litmus paper', 'NH₄⁺ + OH⁻ → NH₃ + H₂O; ammonia turns damp red litmus blue.', ['Add silver nitrate', 'Add barium nitrate', 'Flame test']),
    ('State the colour of the precipitate formed when aqueous sodium hydroxide is added to a solution of iron(III) ions.', 'Red-brown.', '[1]'),
])
t11a.fixed('C2', (2, 3, 4), [
    ('Explain why a flame test cannot distinguish between solutions of sodium chloride and sodium sulfate.', 'The flame colour is due to the cation; both contain Na⁺ (yellow); an anion test is needed.', '[2]'),
    ('Explain why aqueous sodium hydroxide alone cannot distinguish between Al³⁺ and Zn²⁺ ions.', 'Both give a white precipitate that dissolves in excess NaOH to form a colourless solution.', '[2]'),
    ('Explain why the precipitate formed from a solution of Fe²⁺ ions slowly turns brown at its surface.', 'Iron(II) hydroxide is oxidised by air to iron(III) hydroxide (red-brown).', '[2]'),
    ('Explain why a nichrome or platinum wire is cleaned with concentrated hydrochloric acid before a flame test.', 'To remove traces of other metal ions that would contaminate the flame colour.', '[1]'),
])


@t11a.add('C1', (1, 2, 3))
def t11a_ppt(r, D):
    c = r.choice([x for x in CATION_T if x[0] != 'NH₄⁺'])
    if r.random() < 0.5:
        stem = f'A solution gives a {c[2]} with aqueous sodium hydroxide, {c[3]}. Which cation is present?'
        stem = stem.replace(', —', '')
        cands = [x for x in CATION_T if (x[2], x[3]) == (c[2], c[3])]
        if len(cands) > 1:
            stem = f'A solution gives a {c[2]} with aqueous sodium hydroxide ({c[3]}) and with aqueous ammonia gives {c[4]}' + (f', {c[5]}' if c[5] != '—' else '') + '. Which cation is present?'
        return mcq_q(r, stem, c[0], [x[0] for x in CATION_T] + ['Na⁺', 'K⁺'], f'{c[0]} ({c[1]}): NaOH — {c[2]}, {c[3]}; NH₃ — {c[4]}' + (f', {c[5]}' if c[5] != '—' else '') + '.')
    return mcq_q(r, f'What is observed when aqueous sodium hydroxide is added dropwise, then in excess, to a solution containing {c[1]} ions?', f'{c[2]}, {c[3]}',
                 [f'{x[2]}, {x[3]}' for x in CATION_T if x[0] not in ('NH₄⁺',)] + ['no change'], f'{c[0]}: {c[2]}, {c[3]}.')


@t11a.add('C1', (1, 2, 3))
def t11a_flame(r, D):
    ion, nm, col = r.choice(FLAME)
    if r.random() < 0.5:
        return mcq_q(r, f'A compound gives a {col} flame colour. Which ion is present?', ion, [x[0] for x in FLAME], f'{nm} ({ion}): {col}.')
    return mcq_q(r, f'What is the flame-test colour of {nm} ions?', col, [x[2] for x in FLAME], f'{nm} ({ion}): {col}.')


@t11a.add('C3', (2, 3, 4))
def t11a_eq(r, D):
    ion = r.choice(list(HYDROX))
    c = [x for x in CATION_T if x[0] == ion][0]
    return {'stem': f'Aqueous sodium hydroxide is added to a solution containing {c[1]} ions. Describe what is seen, including when excess is added, and write the ionic equation, with state symbols, for the formation of the precipitate.',
            'answer': f'{cap(c[2])}, {c[3]}; {HYDROX[ion]}', 'key': '1 mark colour of precipitate; 1 mark behaviour in excess; 1 mark ionic equation; 1 mark state symbols [4]', 'marks': 4}


@t11a.add('C3', (2, 3, 4, 5))
def t11a_unknown(r, D):
    cs = r.sample([x for x in CATION_T if x[0] != 'NH₄⁺'], 3)
    L = 'XYZ'
    tbl = '; '.join(f'{L[i]}: NaOH(aq) — {c[2]}, {c[3]}; NH₃(aq) — {c[4]}' + (f', {c[5]}' if c[5] != '—' else '') for i, c in enumerate(cs))
    return {'stem': f'Three solutions X, Y and Z each contain one cation. Results — {tbl}. Identify the cation in each solution.',
            'answer': '; '.join(f'{L[i]} {c[0]} ({c[1]})' for i, c in enumerate(cs)), 'key': '1 mark each correct ion [3]', 'marks': 3}


@t11a.add('C2', (2, 3, 4), 'explain')
def t11a_dist(r, D):
    pairs = [('Al³⁺', 'Zn²⁺', 'add excess aqueous ammonia: the zinc hydroxide precipitate dissolves, the aluminium hydroxide does not'),
             ('Al³⁺', 'Ca²⁺', 'add excess aqueous sodium hydroxide: Al(OH)₃ dissolves, Ca(OH)₂ does not (or flame test: Ca²⁺ orange-red)'),
             ('Fe²⁺', 'Fe³⁺', 'add aqueous sodium hydroxide: Fe²⁺ gives a green precipitate, Fe³⁺ a red-brown precipitate'),
             ('Cu²⁺', 'Cr³⁺', 'add aqueous sodium hydroxide: Cu²⁺ light blue, Cr³⁺ green precipitate (which dissolves in excess)'),
             ('Zn²⁺', 'Ca²⁺', 'add excess aqueous sodium hydroxide: zinc hydroxide dissolves, calcium hydroxide does not; or aqueous ammonia gives a white precipitate only with Zn²⁺'),
             ('Na⁺', 'K⁺', 'flame test: Na⁺ yellow, K⁺ lilac'), ('NH₄⁺', 'Na⁺', 'warm with aqueous NaOH: only NH₄⁺ releases ammonia, turning damp red litmus blue')]
    a, b, t = r.choice(pairs)
    return {'stem': f'Describe a test to distinguish between solutions containing {a} ions and {b} ions. Give the result for each.', 'answer': cap(t) + '.', 'key': '1 mark reagent/test; 1 mark each result [3]', 'marks': 3}


def _cat_c4(r, D):
    c = r.choice([x for x in CATION_T if x[0] in ('Cu²⁺', 'Fe²⁺', 'Fe³⁺', 'Zn²⁺', 'Al³⁺', 'Ca²⁺')])
    fl = [x for x in FLAME if x[0] == c[0]]
    intro = r.choice([f'{person(r)} is given an unlabelled solution of a salt in {lab(r)} and tests it with aqueous sodium hydroxide and aqueous ammonia.', f'A water sample from a mine in {city(r)} is tested for metal ions.',
                      'A solution of an unknown salt is divided into three portions for testing.'])
    parts = [
        lambda r: ('Describe how aqueous sodium hydroxide should be added, and why.', 'A few drops at a time, then in excess, observing after each addition — to see whether any precipitate dissolves in excess.', '[2]'),
        lambda r: (f'The solution gave a {c[2]} with aqueous sodium hydroxide, {c[3]}. Identify the cation, explaining your reasoning.', f'{c[0]} ({c[1]})' + (' — confirm with aqueous ammonia' if c[0] in ('Al³⁺', 'Zn²⁺') else ''), '[2]'),
        lambda r: ('Write the ionic equation for the formation of the precipitate.', HYDROX[c[0]], '[2]'),
        lambda r: (f'Predict what would be seen with aqueous ammonia.', f'{c[4]}' + (f', {c[5]}' if c[5] != '—' else ''), '[2]'),
        lambda r: (('State the expected flame test colour.', fl[0][2], '[1]') if fl else ('Explain why a flame test would not help identify this ion.', 'This ion has no characteristic flame colour in the syllabus; use precipitate tests instead.', '[1]')),
        lambda r: ('Describe how to carry out a flame test.', 'Dip a clean nichrome wire (cleaned with conc. HCl) into the solid, hold in a blue Bunsen flame, observe colour.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t11a.add('C4', (2, 3, 4, 5), 'case')(_cat_c4)
t11a.add('C3', (3, 4), 'case')(_cat_c4)

# ---------------------------------------------------------- 11.2 anions
ANION_T = [('carbonate', 'CO₃²⁻', 'add dilute acid and test the gas with limewater', 'effervescence; carbon dioxide turns limewater milky', 'CO₃²⁻ + 2H⁺ → CO₂ + H₂O'),
           ('chloride', 'Cl⁻', 'acidify with dilute nitric acid, then add aqueous silver nitrate', 'white precipitate', 'Ag⁺(aq) + Cl⁻(aq) → AgCl(s)'),
           ('bromide', 'Br⁻', 'acidify with dilute nitric acid, then add aqueous silver nitrate', 'cream precipitate', 'Ag⁺(aq) + Br⁻(aq) → AgBr(s)'),
           ('iodide', 'I⁻', 'acidify with dilute nitric acid, then add aqueous silver nitrate', 'yellow precipitate', 'Ag⁺(aq) + I⁻(aq) → AgI(s)'),
           ('nitrate', 'NO₃⁻', 'add aqueous sodium hydroxide, then aluminium foil; warm carefully', 'ammonia gas produced, which turns damp red litmus paper blue', ''),
           ('sulfate', 'SO₄²⁻', 'acidify with dilute nitric acid, then add aqueous barium nitrate', 'white precipitate', 'Ba²⁺(aq) + SO₄²⁻(aq) → BaSO₄(s)'),
           ('sulfite', 'SO₃²⁻', 'add dilute hydrochloric acid, warm gently and test the gas with acidified aqueous potassium manganate(VII)', 'sulfur dioxide produced, which turns acidified potassium manganate(VII) from purple to colourless', '')]

t11b = topic('Tests for anions', 'identifying anions: carbonate, chloride, bromide, iodide, nitrate, sulfate and sulfite', 'anions', 'anion tests')
t11b.fixed('C1', (1, 2), [
    ('Which reagent is used to test for sulfate ions after acidifying with dilute nitric acid?', 'aqueous barium nitrate', 'Ba²⁺ + SO₄²⁻ → BaSO₄, white precipitate.', ['aqueous silver nitrate', 'limewater', 'aqueous sodium hydroxide']),
    ('What colour precipitate does an iodide give with acidified aqueous silver nitrate?', 'yellow', 'Cl⁻ white, Br⁻ cream, I⁻ yellow.', ['white', 'cream', 'black']),
    ('Why is the solution acidified with nitric acid before adding silver nitrate?', 'To remove carbonate ions that would also give a precipitate', 'Carbonate would precipitate silver carbonate, giving a false positive.', ['To make the precipitate dissolve', 'To add chloride ions', 'To change the colour of the precipitate']),
    ('Which test shows the presence of nitrate ions?', 'Warm with aqueous sodium hydroxide and aluminium foil; ammonia is produced', 'NO₃⁻ is reduced to NH₃, which turns damp red litmus blue.', ['Add barium nitrate: white precipitate', 'Add silver nitrate: yellow precipitate', 'Add dilute acid: effervescence']),
    ('Which ion is present if a solid fizzes with dilute acid and the gas turns limewater milky?', 'carbonate', 'CO₃²⁻ + 2H⁺ → CO₂ + H₂O.', ['sulfate', 'chloride', 'nitrate']),
    ('State the test and result for a sulfite ion.', 'Add dilute acid and warm; SO₂ given off turns acidified aqueous potassium manganate(VII) from purple to colourless.', '[2]'),
])
t11b.fixed('C2', (2, 3, 4), [
    ('Explain why dilute hydrochloric acid must not be used to acidify a solution before testing for chloride ions with silver nitrate.', 'It adds chloride ions, which would always give a white precipitate (false positive).', '[2]'),
    ('Explain why dilute sulfuric acid must not be used to acidify a solution before the sulfate test.', 'It contains sulfate ions, so a white precipitate would form whether or not the sample contained sulfate.', '[2]'),
    ('Explain why the test for nitrate ions must be carried out only after checking that ammonium ions are absent.', 'Ammonium ions also release ammonia when warmed with NaOH, giving a false positive.', '[2]'),
    ('Explain why the precipitate in the silver nitrate test does not tell you which metal ion is present.', 'The precipitate is a silver halide; the anion is identified, not the cation of the original salt.', '[1]'),
])


@t11b.add('C1', (1, 2, 3))
def t11b_res(r, D):
    a = r.choice(ANION_T)
    if r.random() < 0.5:
        return mcq_q(r, f'A solution is tested: {a[2]}. The result is: {a[3]}. Which ion is present?', f'{a[0]} ({a[1]})', [f'{x[0]} ({x[1]})' for x in ANION_T], f'{a[0]}: {a[2]} → {a[3]}.')
    return mcq_q(r, f'What is the positive result in the test for {a[0]} ions?', a[3], [x[3] for x in ANION_T] + ['brown gas given off'], f'{a[0]}: {a[2]} → {a[3]}.')


@t11b.add('C2', (2, 3, 4), 'explain')
def t11b_desc(r, D):
    a = r.choice(ANION_T)
    return {'stem': f'Describe a test for {a[0]} ions in a solution, giving the reagent(s) and the positive result.' + (' Write the ionic equation.' if a[4] and D >= 3 else ''),
            'answer': f'{cap(a[2])}: {a[3]}.' + (f' {a[4]}' if a[4] and D >= 3 else ''), 'key': '1 mark reagent(s); 1 mark result' + ('; 1 mark ionic equation [3]' if a[4] and D >= 3 else ' [2]'), 'marks': 3 if a[4] and D >= 3 else 2}


@t11b.add('C3', (2, 3, 4, 5))
def t11b_salt(r, D):
    c = r.choice([x for x in CATION_T if x[0] != 'NH₄⁺'] + [('Na⁺', 'sodium', None, None, None, None), ('K⁺', 'potassium', None, None, None, None)])
    a = r.choice(ANION_T)
    fl = dict((x[0], x[2]) for x in FLAME)
    ctest = f'aqueous sodium hydroxide gives a {c[2]}, {c[3]}' if c[2] else f'flame test colour {fl[c[0]]}'
    nm = f'{c[1]} {a[0]}'
    return {'stem': f'A solid salt S is dissolved in water. Test 1: {ctest}. Test 2: {a[2]}: {a[3]}. Identify salt S and explain how each result leads to your answer.',
            'answer': f'{nm}: test 1 shows {c[0]}; test 2 shows {a[1]}.', 'key': '1 mark cation; 1 mark anion; 1 mark name of salt [3]', 'marks': 3}


@t11b.add('C3', (1, 2, 3))
def t11b_halide(r, D):
    a = r.choice(ANION_T[1:4])
    if D == 1:
        return mcq_q(r, f'Acidified aqueous silver nitrate is added to a solution and a {a[3]} forms. Which ion is present?', a[1], ['Cl⁻', 'Br⁻', 'I⁻', 'SO₄²⁻', 'CO₃²⁻'], f'{a[3]} = {a[0]}.')
    return {'stem': f'Acidified aqueous silver nitrate is added to a solution and a {a[3]} forms. Identify the ion and write the ionic equation with state symbols.', 'answer': f'{a[0]} ({a[1]}); {a[4]}', 'key': '1 mark ion; 1 mark equation; 1 mark state symbols [3]', 'marks': 3}


def _an_c4(r, D):
    a1, a2 = r.sample(ANION_T, 2)
    intro = r.choice([f'{person(r)} is given two solids, A and B. A contains {a1[1]} ions and B contains {a2[1]} ions, but the labels have fallen off.', f'A laboratory in {city(r)} needs to confirm the anions present in two fertiliser samples.',
                      'A student must plan tests to identify the anions in two unlabelled salts.'])
    parts = [
        lambda r: (f'Describe a test for {a1[0]} ions and its result.', f'{cap(a1[2])}: {a1[3]}.', '[2]'),
        lambda r: (f'Describe a test for {a2[0]} ions and its result.', f'{cap(a2[2])}: {a2[3]}.', '[2]'),
        lambda r: ((f'Write the ionic equation for the positive {a1[0]} test.', a1[4], '[2]') if a1[4] else None),
        lambda r: ((f'Write the ionic equation for the positive {a2[0]} test.', a2[4], '[2]') if a2[4] else None),
        lambda r: ('Explain why nitric acid, rather than hydrochloric acid, is used to acidify a solution before adding silver nitrate.', 'HCl adds chloride ions that would form a white precipitate.', '[1]'),
        lambda r: ('Explain why the solution is acidified before testing with barium nitrate.', 'To remove carbonate ions, which would also form a white precipitate (barium carbonate).', '[1]'),
        lambda r: ('Name the gas produced in the test for nitrate ions and give a test for it.', 'Ammonia: turns damp red litmus paper blue.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t11b.add('C4', (2, 3, 4, 5), 'case')(_an_c4)
t11b.add('C3', (3, 4), 'case')(_an_c4)

# ---------------------------------------------------------- 11.3 gases
GAS_T = [('ammonia', 'NH₃', 'damp red litmus paper', 'turns blue'), ('carbon dioxide', 'CO₂', 'limewater', 'turns milky'), ('chlorine', 'Cl₂', 'damp litmus paper', 'is bleached'),
         ('hydrogen', 'H₂', 'a lighted splint', 'gives a squeaky pop'), ('oxygen', 'O₂', 'a glowing splint', 'relights'), ('sulfur dioxide', 'SO₂', 'acidified aqueous potassium manganate(VII)', 'turns from purple to colourless')]
GAS_SRC = [('zinc and dilute hydrochloric acid', 'hydrogen'), ('calcium carbonate and dilute hydrochloric acid', 'carbon dioxide'), ('hydrogen peroxide with manganese(IV) oxide', 'oxygen'),
           ('ammonium chloride warmed with sodium hydroxide', 'ammonia'), ('sodium sulfite warmed with dilute hydrochloric acid', 'sulfur dioxide'), ('electrolysis of concentrated sodium chloride solution (at the anode)', 'chlorine'),
           ('magnesium and dilute sulfuric acid', 'hydrogen'), ('heating copper(II) carbonate', 'carbon dioxide')]

t11c = topic('Tests for gases', 'identifying gases: ammonia, carbon dioxide, chlorine, hydrogen, oxygen and sulfur dioxide', 'gas tests', 'identifying gases')
t11c.fixed('C1', (1, 2), [
    ('Which gas relights a glowing splint?', 'oxygen', 'Oxygen supports combustion.', ['hydrogen', 'carbon dioxide', 'nitrogen']),
    ('Which gas bleaches damp litmus paper?', 'chlorine', 'Chlorine bleaches damp litmus (it may turn red first).', ['ammonia', 'oxygen', 'hydrogen']),
    ('What is the test for carbon dioxide?', 'It turns limewater milky', 'CO₂ + Ca(OH)₂ → CaCO₃ (white ppt) + H₂O.', ['It relights a glowing splint', 'It pops with a lighted splint', 'It turns damp red litmus blue']),
    ('Which gas turns damp red litmus paper blue?', 'ammonia', 'Ammonia is an alkaline gas.', ['chlorine', 'sulfur dioxide', 'hydrogen']),
    ('Which gas turns acidified aqueous potassium manganate(VII) from purple to colourless?', 'sulfur dioxide', 'SO₂ is a reducing agent.', ['carbon dioxide', 'oxygen', 'ammonia']),
    ('State the test for hydrogen and the result.', 'A lighted splint gives a squeaky pop.', '[2]'),
])
t11c.fixed('C2', (2, 3, 4), [
    ('Explain why litmus paper must be damp when testing for ammonia.', 'Ammonia must dissolve in water to form an alkaline solution (OH⁻ ions) to change the indicator colour.', '[2]'),
    ('Explain why limewater turns milky with carbon dioxide.', 'CO₂ reacts with calcium hydroxide to form insoluble calcium carbonate, a white precipitate.', '[2]'),
    ('Explain why hydrogen gives a "squeaky pop" with a lighted splint.', 'Hydrogen reacts rapidly (explodes) with oxygen from the air to form water.', '[1]'),
    ('Explain why the test for chlorine must be done in a fume cupboard.', 'Chlorine is toxic.', '[1]'),
])


@t11c.add('C1', (1, 2, 3))
def t11c_test(r, D):
    g = r.choice(GAS_T)
    if r.random() < 0.5:
        return mcq_q(r, f'A gas is tested with {g[2]}, which {g[3]}. Which gas is it?', g[0], [x[0] for x in GAS_T], f'{g[0]}: {g[2]} {g[3]}.')
    return mcq_q(r, f'Which is the test for {g[0]}?', f'{g[2]} {g[3]}', [f'{x[2]} {x[3]}' for x in GAS_T], f'{g[0]} ({g[1]}): {g[2]} {g[3]}.')


@t11c.add('C3', (2, 3, 4))
def t11c_src(r, D):
    src, g = r.choice(GAS_SRC)
    t = [x for x in GAS_T if x[0] == g][0]
    return {'stem': f'A gas is produced from {src}. Name the gas and describe a test to confirm its identity, giving the result.', 'answer': f'{g}; {t[2]} {t[3]}.', 'key': '1 mark gas; 1 mark test; 1 mark result [3]', 'marks': 3}


@t11c.add('C2', (2, 3, 4), 'explain')
def t11c_two(r, D):
    a, b = r.sample(GAS_T, 2)
    return {'stem': f'Two gas jars contain {a[0]} and {b[0]}. Describe one test that would identify each gas, giving the results you would expect.',
            'answer': f'{cap(a[0])}: {a[2]} {a[3]}. {cap(b[0])}: {b[2]} {b[3]}.', 'key': '1 mark each test with result [4]', 'marks': 4 if D >= 3 else 2}


def _gas_c4(r, D):
    srcs = r.sample(GAS_SRC, 3)
    if len({g for _, g in srcs}) < 3:
        return None
    intro = f'{person(r)} carries out three reactions and collects the gases: (1) {srcs[0][0]}; (2) {srcs[1][0]}; (3) {srcs[2][0]}.'
    gt = {x[0]: x for x in GAS_T}
    parts = [
        lambda r: ('Name the gas produced in each reaction.', '; '.join(f'({i + 1}) {g}' for i, (_, g) in enumerate(srcs)), '[3]'),
        lambda r: (f'Describe the test for the gas from reaction (1).', f'{gt[srcs[0][1]][2]} {gt[srcs[0][1]][3]}', '[2]'),
        lambda r: (f'Describe the test for the gas from reaction (2).', f'{gt[srcs[1][1]][2]} {gt[srcs[1][1]][3]}', '[2]'),
        lambda r: ('Suggest which gas should only be tested in a fume cupboard and why.', 'Chlorine, sulfur dioxide or ammonia — they are toxic/irritants.' if any(g in ('chlorine', 'sulfur dioxide', 'ammonia') for _, g in srcs) else 'None of these is highly toxic, but good ventilation is still advised.', '[1]'),
        lambda r: ('Describe how a gas that is less dense than air and insoluble in water could be collected.', 'Over water in an inverted measuring cylinder, or by upward delivery, or in a gas syringe.', '[1]'),
        lambda r: (f'Write an equation for reaction (1).', {'zinc and dilute hydrochloric acid': E('Zn + 2HCl -> ZnCl2 + H2'), 'calcium carbonate and dilute hydrochloric acid': E('CaCO3 + 2HCl -> CaCl2 + H2O + CO2'),
                    'hydrogen peroxide with manganese(IV) oxide': E('2H2O2 -> 2H2O + O2'), 'ammonium chloride warmed with sodium hydroxide': E('NH4Cl + NaOH -> NaCl + NH3 + H2O'),
                    'sodium sulfite warmed with dilute hydrochloric acid': E('Na2SO3 + 2HCl -> 2NaCl + H2O + SO2'), 'electrolysis of concentrated sodium chloride solution (at the anode)': '2Cl⁻ → Cl₂ + 2e⁻',
                    'magnesium and dilute sulfuric acid': E('Mg + H2SO4 -> MgSO4 + H2'), 'heating copper(II) carbonate': E('CuCO3 -> CuO + CO2')}[srcs[0][0]], '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t11c.add('C4', (2, 3, 4, 5), 'case')(_gas_c4)
t11c.add('C3', (3, 4), 'case')(_gas_c4)

# ---------------------------------------------------------- 11.4 titration and indicators
INDIC = [('methyl orange', 'red', 'yellow', 'orange'), ('thymolphthalein', 'colourless', 'blue', 'pale blue / colourless'), ('litmus', 'red', 'blue', 'purple')]
t11d = topic('Acid–base titration and indicators', 'acid–base titration technique', 'choosing suitable indicators', 'titration')
t11d.fixed('C1', (1, 2), [
    ('What colour is methyl orange in an acidic solution?', 'red', 'Methyl orange: red in acid, yellow in alkali, orange at the end-point.', ['yellow', 'blue', 'colourless']),
    ('What colour is thymolphthalein in an alkaline solution?', 'blue', 'Thymolphthalein: colourless in acid, blue in alkali.', ['colourless', 'red', 'yellow']),
    ('Why is universal indicator not used in titrations?', 'It changes colour gradually over a range of pH, so the end-point is not sharp', 'A single sharp colour change is needed.', ['It is too expensive', 'It reacts with the acid', 'It only works in alkalis']),
    ('Which piece of apparatus is rinsed with the alkali before it is used to measure 25.0 cm³ of alkali?', 'the pipette', 'Rinsing with the solution prevents dilution by water left inside.', ['the conical flask', 'the funnel', 'the white tile']),
    ('Why is a white tile placed under the conical flask?', 'To make the colour change easier to see', 'Contrast makes the end-point clearer.', ['To keep the flask cool', 'To catch spills of acid', 'To stop the flask moving']),
    ('Define the term "titre".', 'The volume of solution added from the burette to reach the end-point.', '[1]'),
])
t11d.fixed('C2', (2, 3, 4), [
    ('Explain why the conical flask is rinsed with distilled water but the burette is rinsed with the acid.', 'Water in the flask does not change the number of moles of alkali added by pipette; water in the burette would dilute the acid and change its concentration.', '[2]'),
    ('Explain why titrations are repeated until concordant results are obtained.', 'To make sure results are reliable/repeatable; concordant titres (within 0.10 cm³) are averaged.', '[2]'),
    ('Explain why the burette tap must be filled below the tap (no air bubble) before starting.', 'An air bubble would leave the jet during the titration, making the measured volume larger than the volume delivered.', '[2]'),
    ('Explain why phenolphthalein-type indicators such as thymolphthalein are colourless at the end-point when acid is added to alkali.', 'The alkali has been just neutralised; the indicator changes from blue to colourless as the pH falls below its range.', '[2]'),
])


@t11d.add('C1', (1, 2, 3))
def t11d_col(r, D):
    ind = r.choice(INDIC)
    env = r.choice(['acid', 'alkali'])
    col = ind[1] if env == 'acid' else ind[2]
    return mcq_q(r, f'What colour is {ind[0]} in {"an acidic" if env == "acid" else "an alkaline"} solution?', col, ['red', 'yellow', 'blue', 'colourless', 'purple', 'green'], f'{ind[0]}: {ind[1]} in acid, {ind[2]} in alkali.')


ACIDS_T = [('hydrochloric acid', 'HCl', 1), ('nitric acid', 'HNO3', 1), ('sulfuric acid', 'H2SO4', 2)]
ALKS_T = [('sodium hydroxide', 'NaOH', 1), ('potassium hydroxide', 'KOH', 1), ('sodium carbonate', 'Na2CO3', 2)]


def titr_eq(acid, alk):
    a, b = acid[1], alk[1]
    if b == 'Na2CO3':
        if a == 'H2SO4':
            return 'H2SO4 + Na2CO3 -> Na2SO4 + H2O + CO2', 1, 1
        return f'2{a} + Na2CO3 -> 2Na{a[1:]} + H2O + CO2', 2, 1
    m = b[:-2]
    if a == 'H2SO4':
        return f'H2SO4 + 2{b} -> {m}2SO4 + 2H2O', 1, 2
    return f'{a} + {b} -> {m}{a[1:]} + H2O', 1, 1


@t11d.add('C3', (2, 3, 4, 5), 'numerical')
def t11d_calc(r, D):
    acid = r.choice(ACIDS_T)
    alk = r.choice(ALKS_T)
    eq, na, nb = titr_eq(acid, alk)
    Vb = r.choice([25.0, 20.0, 10.0])
    cb = r.choice([0.100, 0.0500, 0.200, 0.150, 0.0800])
    Va = r.choice([12.50, 18.75, 20.00, 22.40, 24.60, 15.20, 23.85])
    nB = Vb / 1000 * cb
    nA = nB * na / nb
    cA = nA / (Va / 1000)
    if D >= 5:
        mA = cA * Mr(acid[1])
        return {'stem': f'{sf(Vb)} cm³ of {sf(cb)} mol/dm³ {alk[0]} was neutralised by {Va:.2f} cm³ of {acid[0]}. {E(eq)}. Calculate the concentration of the acid in mol/dm³ and in g/dm³.',
                'answer': f'{g3(cA)} mol/dm³; {g3(mA)} g/dm³', 'key': f'n(alkali) = {g3(nB)} mol [1]; n(acid) = {g3(nA)} mol [1]; c = {g3(cA)} mol/dm³ [1]; × Mr {mr(Mr(acid[1]))} = {g3(mA)} g/dm³ [1]', 'marks': 4}
    return {'stem': f'In a titration, {sf(Vb)} cm³ of {sf(cb)} mol/dm³ {alk[0]} required {Va:.2f} cm³ of {acid[0]} for neutralisation. {E(eq)}. Calculate the concentration of the acid.',
            'answer': f'{g3(cA)} mol/dm³', 'key': f'n(alkali) = {sf(Vb)}/1000 × {sf(cb)} = {g3(nB)} mol [1]; n(acid) = {g3(nA)} mol (ratio {na}:{nb}) [1]; c = {g3(nA)} ÷ {Va / 1000:.5f} = {g3(cA)} mol/dm³ [1]'}


@t11d.add('C2', (2, 3, 4), 'explain')
def t11d_err(r, D):
    errs = [('rinsed the pipette with distilled water just before measuring the alkali', 'smaller', 'The alkali is diluted, so fewer moles are added and less acid is needed.'),
            ('left an air bubble in the burette jet that disappeared during the titration', 'larger', 'The reading change includes the bubble volume, so the recorded titre is larger than the acid actually added.'),
            ('added extra distilled water to the conical flask', 'unchanged', 'The number of moles of alkali is unchanged, so the same volume of acid is needed.'),
            ('overshot the end-point by adding acid too quickly', 'larger', 'More acid than needed was added before the colour change was noticed.'),
            ('rinsed the burette with water, not acid, before filling', 'larger', 'The acid is diluted, so a larger volume is needed to neutralise the alkali.')]
    e, eff, why = r.choice(errs)
    return {'stem': f'During a titration, {person(r)} {e}. Predict the effect on the titre and explain.', 'answer': f'Titre {eff}: {why}', 'key': '1 mark effect; 1 mark explanation [2]'}


def _ti_c4(r, D):
    acid = r.choice(ACIDS_T)
    alk = r.choice(ALKS_T[:2])
    eq, na, nb = titr_eq(acid, alk)
    rows, conc, avg = _titre_table(r)
    Vb = 25.0
    ca = r.choice([0.100, 0.120, 0.0800, 0.150])
    nA = avg / 1000 * ca
    nB = nA * nb / na
    cB = nB / 0.025
    ind = r.choice(INDIC[:2])
    table = '; '.join(f'{"rough" if i == 0 else "run " + str(i)}: {x[0]:.2f} → {x[1]:.2f}' for i, x in enumerate(rows))
    intro = f'{person(r)} determines the concentration of {alk[0]} by titrating 25.0 cm³ portions with {sf(ca)} mol/dm³ {acid[0]}, using {ind[0]}. Burette readings (initial → final, cm³): {table}.'
    parts = [
        lambda r: ('Describe how 25.0 cm³ of the alkali is measured into the flask.', 'Use a volumetric pipette (rinsed with the alkali) with a pipette filler; read at the bottom of the meniscus at eye level.', '[2]'),
        lambda r: ('Calculate the titres and the mean of the concordant titres.', '; '.join(f'{x[2]:.2f}' for x in rows) + f'; mean {avg:.2f} cm³', '[2]'),
        lambda r: ('State the colour change at the end-point.', f'{ind[2]} to {ind[1]}' if True else '', '[1]'),
        lambda r: (f'Calculate the concentration of the {alk[0]}. {E(eq)}', f'{g3(cB)} mol/dm³', f'n(acid) = {g3(nA)} mol [1]; n(alkali) = {g3(nB)} mol [1]; c = {g3(nB)}/0.0250 = {g3(cB)} mol/dm³ [1]; total [3]'),
        lambda r: ('Explain why universal indicator is not suitable.', 'It changes colour gradually; no sharp end-point.', '[1]'),
        lambda r: ('Suggest why a white tile is used.', 'To see the colour change clearly.', '[1]'),
        lambda r: ('Explain why the rough titre is not included in the mean.', 'It overshoots/ is only approximate.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t11d.add('C4', (2, 3, 4, 5), 'case')(_ti_c4)
t11d.add('C3', (3, 4, 5), 'case')(_ti_c4)

CHAPTERS[11] = [t11a, t11b, t11c, t11d]


# ---------------------------------------------------------------- marks follow the marking key
import re as _re


def _key_marks(k):
    """Total marks implied by a marking key: per-part totals for (a)/(b) keys, otherwise the
    sum of the [n] mark points (or the stated total / top band where the key gives one)."""
    if _re.search(r'\([a-h]\)', k):
        segs = [s for s in _re.split(r'\([a-h]\)', k) if s.strip()]
        vals = [_key_marks(s) for s in segs]
        return sum(v or 1 for v in vals) if segs else None
    nums = [int(x) for x in _re.findall(r'\[(\d+)\]', k)]
    if not nums:
        return None
    if 'correct [' in k:
        return max(nums)
    if 'total [' in k:
        return nums[-1]
    return sum(nums)


def _marks_from_key(fn):
    def w(r, D):
        q = fn(r, D)
        if q and 'marks' not in q and not q.get('options'):
            m = _key_marks(q.get('key', ''))
            if m and 1 <= m <= 8:
                q['marks'] = m
        return q
    w.__name__ = getattr(fn, '__name__', 'fn')
    return w


for _ts in CHAPTERS.values():
    for _t in _ts:
        for _tp in _t.templates:
            _tp.fn = _marks_from_key(_tp.fn)
