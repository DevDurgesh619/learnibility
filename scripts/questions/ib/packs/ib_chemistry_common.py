"""Shared helpers for the IB DP Chemistry packs (ib-g11-chemistry, ib-g12-chemistry).

IB Chemistry data booklet (first assessment 2025) values are used throughout:
  NA = 6.02 × 10²³ mol⁻¹, R = 8.31 J K⁻¹ mol⁻¹, Vm = 22.7 dm³ mol⁻¹ (STP: 273 K, 100 kPa),
  c(water) = 4.18 J g⁻¹ K⁻¹, F = 96 500 C mol⁻¹, Kw = 1.00 × 10⁻¹⁴ (298 K), h = 6.63 × 10⁻³⁴ J s,
  c = 3.00 × 10⁸ m s⁻¹, relative atomic masses to 2 d.p., average bond enthalpies, standard
  enthalpies of formation / combustion, standard entropies, standard electrode potentials, pKa/pKb.

Formulae are written in ASCII (CuSO4.5H2O, SO4^2-) and pretty-printed with subscripts / superscripts.

Mock = HL Paper 1 (1A 40 MCQ, 40 marks + 1B data-based / experimental, 35 marks) + Paper 2
(structured and extended response, 90 marks): 52 items, 165 marks in every mock.
"""
from __future__ import annotations

import dataclasses
import math
import re

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from engine import Slot

CONFIG = {'minutesPerMark': 1.2, 'mcqMinutes': 1.5}

MOCK = [
    dict(section='Paper 1A – multiple-choice questions', count=40, c=['C1', 'C3', 'C3', 'C1', 'C3'], d=[2, 3, 2, 3, 4], type='mcq', marks=1),
    dict(section='Paper 1B – data-based and experimental questions', count=3, c=['C3', 'C4'], d=[3, 4], type='case', marks=9, style='p1b'),
    dict(section='Paper 1B – data-based and experimental questions (short)', count=1, c=['C3'], d=[3], type='case', marks=8, style='p1b'),
    dict(section='Paper 2 – structured short-response questions', count=6, c=['C3', 'C4'], d=[3, 4, 4], type='multi_step', marks=10, style='p2'),
    dict(section='Paper 2 – extended-response questions', count=2, c=['C4'], d=[4, 5], type='long', marks=15, style='p2x'),
]

# ---------------------------------------------------------------------------------------------
# Data booklet constants
# ---------------------------------------------------------------------------------------------
NA = 6.02e23
RGAS = 8.31
VM = 22.7
CW = 4.18
FARADAY = 96500
KW = 1.00e-14
H_PLANCK = 6.63e-34
C_LIGHT = 3.00e8

AR = {'H': 1.01, 'He': 4.00, 'Li': 6.94, 'Be': 9.01, 'B': 10.81, 'C': 12.01, 'N': 14.01, 'O': 16.00, 'F': 19.00,
      'Ne': 20.18, 'Na': 22.99, 'Mg': 24.31, 'Al': 26.98, 'Si': 28.09, 'P': 30.97, 'S': 32.07, 'Cl': 35.45,
      'Ar': 39.95, 'K': 39.10, 'Ca': 40.08, 'Sc': 44.96, 'Ti': 47.87, 'V': 50.94, 'Cr': 52.00, 'Mn': 54.94,
      'Fe': 55.85, 'Co': 58.93, 'Ni': 58.69, 'Cu': 63.55, 'Zn': 65.38, 'Ga': 69.72, 'Ge': 72.63, 'As': 74.92,
      'Se': 78.97, 'Br': 79.90, 'Kr': 83.80, 'Rb': 85.47, 'Sr': 87.62, 'Ag': 107.87, 'Sn': 118.71, 'I': 126.90,
      'Cs': 132.91, 'Ba': 137.33, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59, 'Pb': 207.20}

ELEMENTS = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
            'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
            'Rb', 'Sr']
ENAME = {'H': 'hydrogen', 'He': 'helium', 'Li': 'lithium', 'Be': 'beryllium', 'B': 'boron', 'C': 'carbon',
         'N': 'nitrogen', 'O': 'oxygen', 'F': 'fluorine', 'Ne': 'neon', 'Na': 'sodium', 'Mg': 'magnesium',
         'Al': 'aluminium', 'Si': 'silicon', 'P': 'phosphorus', 'S': 'sulfur', 'Cl': 'chlorine', 'Ar': 'argon',
         'K': 'potassium', 'Ca': 'calcium', 'Sc': 'scandium', 'Ti': 'titanium', 'V': 'vanadium', 'Cr': 'chromium',
         'Mn': 'manganese', 'Fe': 'iron', 'Co': 'cobalt', 'Ni': 'nickel', 'Cu': 'copper', 'Zn': 'zinc',
         'Ga': 'gallium', 'Ge': 'germanium', 'As': 'arsenic', 'Se': 'selenium', 'Br': 'bromine', 'Kr': 'krypton',
         'Rb': 'rubidium', 'Sr': 'strontium', 'Ag': 'silver', 'Sn': 'tin', 'I': 'iodine', 'Cs': 'caesium',
         'Ba': 'barium', 'Pb': 'lead', 'Au': 'gold', 'Pt': 'platinum', 'Hg': 'mercury'}
Z = {e: i + 1 for i, e in enumerate(ELEMENTS)}
Z.update({'Ag': 47, 'Sn': 50, 'I': 53, 'Cs': 55, 'Ba': 56, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Pb': 82})

# Pauling electronegativities (data booklet)
EN = {'H': 2.2, 'Li': 1.0, 'Be': 1.6, 'B': 2.0, 'C': 2.6, 'N': 3.0, 'O': 3.4, 'F': 4.0, 'Na': 0.9, 'Mg': 1.3,
      'Al': 1.6, 'Si': 1.9, 'P': 2.2, 'S': 2.6, 'Cl': 3.2, 'K': 0.8, 'Ca': 1.0, 'Ti': 1.5, 'Cr': 1.7, 'Mn': 1.6,
      'Fe': 1.8, 'Co': 1.9, 'Ni': 1.9, 'Cu': 1.9, 'Zn': 1.7, 'Ge': 2.0, 'As': 2.2, 'Se': 2.6, 'Br': 3.0,
      'Rb': 0.8, 'Sr': 1.0, 'Ag': 1.9, 'Sn': 2.0, 'I': 2.7, 'Cs': 0.8, 'Ba': 0.9, 'Pb': 2.3}

# First ionisation energies / kJ mol⁻¹
IE1 = {'H': 1312, 'He': 2372, 'Li': 520, 'Be': 900, 'B': 801, 'C': 1086, 'N': 1402, 'O': 1314, 'F': 1681,
       'Ne': 2081, 'Na': 496, 'Mg': 738, 'Al': 578, 'Si': 787, 'P': 1012, 'S': 1000, 'Cl': 1251, 'Ar': 1521,
       'K': 419, 'Ca': 590, 'Rb': 403, 'Sr': 549, 'Cs': 376, 'Ba': 503}

# Average bond enthalpies / kJ mol⁻¹ (data booklet)
BE = {'H-H': 436, 'C-C': 346, 'C=C': 614, 'C≡C': 839, 'C-H': 414, 'C-O': 358, 'C=O': 804, 'O-H': 463,
      'O=O': 498, 'O-O': 144, 'N≡N': 945, 'N=N': 470, 'N-N': 158, 'N-H': 391, 'C-N': 286, 'C≡N': 890,
      'H-F': 567, 'H-Cl': 431, 'H-Br': 366, 'H-I': 298, 'F-F': 159, 'Cl-Cl': 242, 'Br-Br': 193, 'I-I': 151,
      'C-F': 492, 'C-Cl': 324, 'C-Br': 285, 'C-I': 228, 'Si-H': 318, 'S-H': 364}

# Standard enthalpies of formation / kJ mol⁻¹ and standard entropies / J K⁻¹ mol⁻¹ (298 K)
HF = {'H2O(l)': -286, 'H2O(g)': -242, 'CO2(g)': -394, 'CO(g)': -111, 'CH4(g)': -74, 'C2H6(g)': -84,
      'C3H8(g)': -105, 'C4H10(g)': -126, 'C2H4(g)': 52, 'C2H2(g)': 228, 'C6H6(l)': 49, 'CH3OH(l)': -239,
      'C2H5OH(l)': -278, 'NH3(g)': -46, 'NO(g)': 90, 'NO2(g)': 33, 'N2O4(g)': 9, 'SO2(g)': -297,
      'SO3(g)': -396, 'HCl(g)': -92, 'HBr(g)': -36, 'HF(g)': -273, 'CaCO3(s)': -1207, 'CaO(s)': -635,
      'MgO(s)': -602, 'Fe2O3(s)': -824, 'Al2O3(s)': -1676, 'H2O2(l)': -188, 'CH3COOH(l)': -484,
      'C6H12O6(s)': -1273, 'NaCl(s)': -411, 'CuO(s)': -157, 'ZnO(s)': -350, 'PCl3(l)': -320,
      'PCl5(s)': -444, 'H2S(g)': -21, 'C3H6(g)': 20, 'N2H4(l)': 51}
S0 = {'H2(g)': 131, 'O2(g)': 205, 'N2(g)': 192, 'Cl2(g)': 223, 'C(s)': 5.7, 'H2O(l)': 70, 'H2O(g)': 189,
      'CO2(g)': 214, 'CO(g)': 198, 'CH4(g)': 186, 'C2H6(g)': 230, 'C2H4(g)': 220, 'C3H8(g)': 270,
      'NH3(g)': 193, 'NO(g)': 211, 'NO2(g)': 240, 'N2O4(g)': 304, 'SO2(g)': 248, 'SO3(g)': 257,
      'HCl(g)': 187, 'CaCO3(s)': 93, 'CaO(s)': 40, 'MgO(s)': 27, 'Mg(s)': 33, 'Fe(s)': 27, 'Fe2O3(s)': 87,
      'Al(s)': 28, 'Al2O3(s)': 51, 'CH3OH(l)': 127, 'C2H5OH(l)': 161, 'H2O2(l)': 110, 'NaCl(s)': 72,
      'Na(s)': 51, 'Cu(s)': 33, 'CuO(s)': 43, 'Zn(s)': 42, 'ZnO(s)': 44, 'C6H12O6(s)': 212, 'S(s)': 32,
      'H2S(g)': 206, 'C3H6(g)': 267}

# Standard electrode potentials / V: (oxidised form, reduced form, n, E°, half-equation text)
EO = [
    ('Li+', 'Li', 1, -3.04, 'Li⁺(aq) + e⁻ ⇌ Li(s)'),
    ('K+', 'K', 1, -2.93, 'K⁺(aq) + e⁻ ⇌ K(s)'),
    ('Ca2+', 'Ca', 2, -2.87, 'Ca²⁺(aq) + 2e⁻ ⇌ Ca(s)'),
    ('Na+', 'Na', 1, -2.71, 'Na⁺(aq) + e⁻ ⇌ Na(s)'),
    ('Mg2+', 'Mg', 2, -2.37, 'Mg²⁺(aq) + 2e⁻ ⇌ Mg(s)'),
    ('Al3+', 'Al', 3, -1.66, 'Al³⁺(aq) + 3e⁻ ⇌ Al(s)'),
    ('Mn2+', 'Mn', 2, -1.18, 'Mn²⁺(aq) + 2e⁻ ⇌ Mn(s)'),
    ('Zn2+', 'Zn', 2, -0.76, 'Zn²⁺(aq) + 2e⁻ ⇌ Zn(s)'),
    ('Fe2+', 'Fe', 2, -0.45, 'Fe²⁺(aq) + 2e⁻ ⇌ Fe(s)'),
    ('Ni2+', 'Ni', 2, -0.26, 'Ni²⁺(aq) + 2e⁻ ⇌ Ni(s)'),
    ('Sn2+', 'Sn', 2, -0.14, 'Sn²⁺(aq) + 2e⁻ ⇌ Sn(s)'),
    ('Pb2+', 'Pb', 2, -0.13, 'Pb²⁺(aq) + 2e⁻ ⇌ Pb(s)'),
    ('H+', 'H2', 2, 0.00, '2H⁺(aq) + 2e⁻ ⇌ H₂(g)'),
    ('Cu2+', 'Cu', 2, 0.34, 'Cu²⁺(aq) + 2e⁻ ⇌ Cu(s)'),
    ('I2', 'I-', 2, 0.54, 'I₂(s) + 2e⁻ ⇌ 2I⁻(aq)'),
    ('Fe3+', 'Fe2+', 1, 0.77, 'Fe³⁺(aq) + e⁻ ⇌ Fe²⁺(aq)'),
    ('Ag+', 'Ag', 1, 0.80, 'Ag⁺(aq) + e⁻ ⇌ Ag(s)'),
    ('Br2', 'Br-', 2, 1.07, 'Br₂(l) + 2e⁻ ⇌ 2Br⁻(aq)'),
    ('O2', 'H2O', 4, 1.23, 'O₂(g) + 4H⁺(aq) + 4e⁻ ⇌ 2H₂O(l)'),
    ('Cr2O7^2-', 'Cr3+', 6, 1.36, 'Cr₂O₇²⁻(aq) + 14H⁺(aq) + 6e⁻ ⇌ 2Cr³⁺(aq) + 7H₂O(l)'),
    ('Cl2', 'Cl-', 2, 1.36, 'Cl₂(g) + 2e⁻ ⇌ 2Cl⁻(aq)'),
    ('MnO4-', 'Mn2+', 5, 1.51, 'MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ ⇌ Mn²⁺(aq) + 4H₂O(l)'),
    ('F2', 'F-', 2, 2.87, 'F₂(g) + 2e⁻ ⇌ 2F⁻(aq)'),
]
METAL_EO = {r[1]: r for r in EO if r[1] in ('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'Cu', 'Ag', 'Mn')}

# Weak acids (pKa) and weak bases (pKb), 298 K
ACIDS = [('ethanoic acid', 'CH3COOH', 'CH3COO-', 4.76), ('methanoic acid', 'HCOOH', 'HCOO-', 3.75),
         ('propanoic acid', 'CH3CH2COOH', 'CH3CH2COO-', 4.87), ('benzoic acid', 'C6H5COOH', 'C6H5COO-', 4.20),
         ('chloroethanoic acid', 'CH2ClCOOH', 'CH2ClCOO-', 2.87), ('butanoic acid', 'CH3CH2CH2COOH', 'CH3CH2CH2COO-', 4.83),
         ('hydrocyanic acid', 'HCN', 'CN-', 9.21), ('phenol', 'C6H5OH', 'C6H5O-', 9.99),
         ('hypochlorous acid', 'HOCl', 'OCl-', 7.53), ('nitrous acid', 'HNO2', 'NO2-', 3.35)]
BASES = [('ammonia', 'NH3', 'NH4+', 4.75), ('methylamine', 'CH3NH2', 'CH3NH3+', 3.34),
         ('ethylamine', 'CH3CH2NH2', 'CH3CH2NH3+', 3.35), ('dimethylamine', '(CH3)2NH', '(CH3)2NH2+', 3.27),
         ('phenylamine', 'C6H5NH2', 'C6H5NH3+', 9.13)]
INDICATORS = [('methyl orange', 3.7, '3.1–4.4', 'red', 'yellow'), ('bromophenol blue', 4.2, '3.0–4.6', 'yellow', 'blue'),
              ('methyl red', 5.1, '4.4–6.2', 'red', 'yellow'), ('bromothymol blue', 7.0, '6.0–7.6', 'yellow', 'blue'),
              ('phenol red', 7.9, '6.8–8.4', 'yellow', 'red'), ('phenolphthalein', 9.6, '8.3–10.0', 'colourless', 'pink')]

# ---------------------------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------------------------
SUBS = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def chem(f: str) -> str:
    """'CuSO4.5H2O' -> 'CuSO₄·5H₂O'; 'SO4^2-' -> 'SO₄²⁻'; state symbols kept."""
    charge = ''
    if '^' in f:
        f, charge = f.split('^', 1)
    f = f.replace('.', '·')
    f = re.sub(r'(?<=[A-Za-z\)\]])(\d+)', lambda m: m.group(1).translate(SUBS), f)
    if charge:
        charge = sup(charge)
    return f + charge


def ion(f: str) -> str:
    """'Fe3+' -> 'Fe³⁺', 'Cl-' -> 'Cl⁻'; polyatomic ions ending in a digit use '^': 'SO4^2-', 'NO3^-'."""
    if '^' in f:
        return chem(f)
    m = re.match(r'^(.*?)(\d*)([+-])$', f)
    if not m:
        return chem(f)
    body, n, s_ = m.groups()
    return chem(body) + sup(n + s_)


def sf(x, n=3):
    """x to n significant figures; scientific form with superscript powers outside 10⁻³ … 10⁵."""
    if x == 0:
        return '0'
    mag = math.floor(math.log10(abs(x)))
    xr = round(x, -mag + n - 1)
    if xr == 0:
        return '0'
    mag = math.floor(math.log10(abs(xr)))
    if -3 <= mag < 5:
        dec = max(0, n - 1 - mag)
        s = f'{xr:.{dec}f}'
        return s.replace('-', '−')
    m_ = xr / 10 ** mag
    return f'{m_:.{n - 1}f} × 10{sup(mag)}'.replace('-', '−', 1) if m_ < 0 else f'{m_:.{n - 1}f} × 10{sup(mag)}'


def q(x, unit='', n=3):
    return f'{sf(x, n)} {unit}'.strip()


def sgn(x, n=3, unit=''):
    """Signed value, e.g. +52.4 kJ mol⁻¹ / −890 kJ mol⁻¹."""
    s = sf(x, n)
    if n >= 4 and float(x).is_integer() and abs(x) < 1e5:
        s = str(int(x)).replace('-', '−')  # sums of integer data-booklet values: keep as integers
    if x > 0:
        s = '+' + s
    return f'{s} {unit}'.strip()


def dp(x, d=2):
    return f'{x:.{d}f}'.replace('-', '−')


def pick(rng, seq):
    return seq[rng.randrange(len(seq))]


def num(stem, ans, key, marks=2, type='numerical', gap=None):
    d = dict(stem=stem, answer=ans, markingKey=key, marks=marks, type=type)
    if gap:
        d['gap'] = gap
    return d


def nmcq(rng, stem, v, wrongs, unit, key, n=3, extra=True, signed=False):
    """Numeric MCQ: wrongs are common-error values (listed first), then generic fall-backs."""
    f = (lambda x: sgn(x, n, unit)) if signed else (lambda x: q(x, unit, n))
    c = f(v)
    ws = []
    pool = list(wrongs) + ([v * 2, v / 2, v * 10, v / 10, v * 4, v / 4, v * 1.5, -v] if extra else [])
    for w in pool:
        if w is None or w == 0:
            continue
        s = f(w)
        if s != c and s not in ws:
            ws.append(s)
    if len(ws) < 3:
        return None
    return mcq(rng, stem, c, ws[:3], key)


# ---------------------------------------------------------------------------------------------
# Formula parsing
# ---------------------------------------------------------------------------------------------
def atoms(f: str) -> dict:
    """Count atoms in an ASCII formula: 'Ca(OH)2', 'CuSO4.5H2O', 'CH3COOH'."""
    f = f.split('^')[0]
    f = re.sub(r'\([a-z]+\)$', '', f)  # state symbol
    total: dict = {}
    for part in f.split('.'):
        m = re.match(r'^(\d+)(.*)$', part)
        mult = 1
        if m:
            mult, part = int(m.group(1)), m.group(2)
        for k, v in _parse(part).items():
            total[k] = total.get(k, 0) + v * mult
    return total


def _parse(s: str) -> dict:
    stack = [{}]
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in '([':
            stack.append({})
            i += 1
        elif ch in ')]':
            i += 1
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            k = int(s[i:j]) if j > i else 1
            top = stack.pop()
            for e, v in top.items():
                stack[-1][e] = stack[-1].get(e, 0) + v * k
            i = j
        elif ch.isupper():
            j = i + 1
            if j < len(s) and s[j].islower():
                j += 1
            e = s[i:j]
            k0 = j
            while j < len(s) and s[j].isdigit():
                j += 1
            k = int(s[k0:j]) if j > k0 else 1
            stack[-1][e] = stack[-1].get(e, 0) + k
            i = j
        else:
            i += 1
    return stack[0]


def mr(f: str) -> float:
    return sum(AR[e] * k for e, k in atoms(f).items())


def mr_s(f: str) -> str:
    return f'{mr(f):.2f}'


# ---------------------------------------------------------------------------------------------
# Paper 1B (data-based / experimental) wrapper
# ---------------------------------------------------------------------------------------------
GENERIC_EXTRAS = [
    ('State why the measurements should be repeated at least three times.',
     'To identify anomalous results and to reduce the effect of random errors by calculating a mean.',
     'Identifies anomalies / reduces random error by averaging (1).', 1),
    ('Explain why repeating the experiment would not reduce a systematic error in the result.',
     'A systematic error shifts every reading in the same direction by a similar amount, so the mean of repeats is shifted too; it must be removed by improving the method or calibrating the apparatus.',
     'Systematic error has the same direction/size in every trial (1); averaging does not cancel it – the method or calibration must change (1).', 2),
    ('Outline one way in which the precision of the measured data could be improved.',
     'Use apparatus with a smaller uncertainty (higher resolution), or increase the size of the measured quantity so the percentage uncertainty falls, and repeat trials.',
     'Any valid way of reducing random uncertainty: higher-resolution instrument / larger measured quantity / more repeats (1).', 1),
    ('Distinguish between the accuracy and the precision of an experimental result.',
     'Accuracy is how close the result is to the true (literature) value; precision is how close repeated results are to one another (how small the random uncertainty is).',
     'Accuracy – closeness to the true value (1); precision – closeness/agreement of repeated readings (1).', 2),
]


def p1b(R, key, c=('C3', 'C4'), d=(3, 5), name_=None):
    """Decorator: fn(rng, slot) -> dict(intro, parts=[(q, a, key, m)], extras=[(q, a, key, m)]).
    Parts are padded with extras to the section marks (default 8) and lettered (a), (b), …"""
    def deco(fn):
        def wrap(rng, slot):
            s = fn(rng, slot)
            if s is None:
                return None
            parts = list(s['parts'])
            target = slot.marks or 8
            have = sum(p[3] for p in parts)
            if have > target:
                while parts and have > target:
                    have -= parts.pop()[3]
            extras = list(s.get('extras', []))
            gen = list(GENERIC_EXTRAS)
            rng.shuffle(gen)
            for e in extras + gen:
                if have == target:
                    break
                if have + e[3] <= target:
                    parts.append(e)
                    have += e[3]
            if have != target or len(parts) < 2:
                return None
            L = 'abcdefgh'
            stem = s['intro'] + '\n\n' + '\n'.join(f'({L[i]}) {p[0]} [{p[3]}]' for i, p in enumerate(parts))
            ans = ' '.join(f'({L[i]}) {p[1]}' for i, p in enumerate(parts))
            mk = ' '.join(f'({L[i]}) [{p[3]}] {p[2]}' for i, p in enumerate(parts))
            return dict(stem=stem, answer=ans, markingKey=mk, type='case', marks=target, gap='G7')
        R.t.setdefault(key, []).append(T(c, d, wrap, 'case', 'p1b', name_ or fn.__name__))
        return fn
    return deco


# ---------------------------------------------------------------------------------------------
# Generic IA-skills factories
# ---------------------------------------------------------------------------------------------
def repeat_readings(R, key, quantity, unit, lo, hi, n_dp, contexts, c='C3', d=(1, 4)):
    """Mean, absolute (half-range) and percentage uncertainty of repeated readings."""
    def fn(rng, slot):
        true = rng.uniform(lo, hi)
        k = 3 if slot.d <= 2 else rng.choice([4, 5])
        spread = true * rng.uniform(0.01, 0.04)
        vals = [round(true + rng.uniform(-spread, spread), n_dp) for _ in range(k)]
        if len(set(vals)) < 3:
            return None
        mean = sum(vals) / k
        half = (max(vals) - min(vals)) / 2
        pct = 100 * half / mean
        ctx = pick(rng, contexts)
        who = name(rng)
        vs = ', '.join(f'{v:.{n_dp}f}' for v in vals)
        if slot.d <= 2:
            stem = f'{who} {ctx} The repeated readings of {quantity} were {vs} {unit}. Calculate the mean and its absolute uncertainty.'
            ans = f'{mean:.{n_dp}f} ± {half:.{n_dp}f} {unit}'
            k_ = f'Mean = {mean:.{n_dp}f} {unit} (A1); uncertainty = half the range = ({max(vals):.{n_dp}f} − {min(vals):.{n_dp}f})/2 = {half:.{n_dp}f} {unit} (A1).'
            return num(stem, ans, k_, 2)
        stem = f'{who} {ctx} The {k} readings of {quantity} were {vs} {unit}. Determine the mean, its absolute uncertainty and its percentage uncertainty.'
        ans = f'{mean:.{n_dp}f} ± {half:.{n_dp}f} {unit} ({pct:.1f} %)'
        k_ = (f'Mean = {mean:.{n_dp}f} {unit} (A1); absolute uncertainty = half range = {half:.{n_dp}f} {unit} (A1); '
              f'percentage uncertainty = {half:.{n_dp}f}/{mean:.{n_dp}f} × 100 = {pct:.1f} % (A1).')
        return num(stem, ans, k_, 3)
    R.t.setdefault(key, []).append(T(c, d, fn, 'numerical', None, 'repeat_readings_' + key))


def pct_error(R, key, what, unit, lit, lo, hi, contexts, causes, c=('C3', 'C4'), d=(2, 5), signed=False):
    """Percentage error against a literature value plus identification of a systematic error."""
    def fn(rng, slot):
        v = lit * rng.uniform(lo, hi)
        v = float(f'{v:.3g}')
        err = abs(v - lit) / abs(lit) * 100
        ctx = pick(rng, contexts)
        cause = pick(rng, causes)
        who = name(rng)
        vs = sgn(v, 3, unit) if signed else q(v, unit)
        ls = sgn(lit, 3, unit) if signed else q(lit, unit)
        if slot.d <= 3:
            stem = f'{who} {ctx} The experimental value of {what} was {vs}; the literature value is {ls}. Calculate the percentage error.'
            return num(stem, f'{err:.1f} %', f'|{vs} − ({ls})| / |{ls}| × 100 (M1) = {err:.1f} % (A1).', 2)
        stem = (f'{who} {ctx} The experimental value of {what} was {vs}; the literature value is {ls}. '
                f'(a) Calculate the percentage error. (b) Suggest, with a reason, one systematic error that could account for the difference and how it could be reduced.')
        return num(stem, f'(a) {err:.1f} %; (b) {cause}', f'(a) |experimental − literature|/|literature| × 100 = {err:.1f} % (M1 A1). (b) {cause} (R1 for a cause consistent with the direction of the error, R1 for a matching improvement).', 4, 'multi_step', gap='G7')
    R.t.setdefault(key, []).append(T(c, d, fn, 'numerical', None, 'pct_error_' + key))


# ---------------------------------------------------------------------------------------------
# Paper 2 composites (only used to fill mock sections)
# ---------------------------------------------------------------------------------------------
def _part(rng, tpls, c, d, used, slot):
    pool = [t for t in tpls if (c in (t.c if isinstance(t.c, tuple) else (t.c,))) and t.type != 'mcq'
            and t.style is None and t.name not in used and t.d[0] <= d <= t.d[1] + 1]
    rng.shuffle(pool)
    for t in pool[:8]:
        try:
            out = t.fn(rng, Slot(slot.subtopic, slot.chapter, c, d, set='part'))
        except IndexError:
            out = None
        if out and out.get('type') != 'mcq' and not out.get('options'):
            used.add(t.name)
            return out
    return None


def _fix_marks(key, m_):
    return re.sub(r'\(\d+ marks?:', f'({m_} marks:', key)


def clean_name(n):
    n = re.sub(r'^[SR]\d\.\d\s+', '', n)
    n = n.replace(' (HL)', '').replace('(HL)', '')
    return n[0].lower() + n[1:]


_SUBL = re.compile(r'\(([a-f])\)')


def _sub_roman(t):
    """Inner part labels (a), (b)… of a component item become (i), (ii)… inside a composite."""
    return _SUBL.sub(lambda m: '(' + ['i', 'ii', 'iii', 'iv', 'v', 'vi'][ord(m.group(1)) - 97] + ')', t)


def composite(st, tpls, spec, style):
    def fn(rng, slot):
        if slot.set != 'mock':
            return None
        used = set()
        parts = []
        for c, d, m_ in spec:
            p = _part(rng, tpls, c, d, used, slot)
            if p is None:
                return None
            p = dict(p, stem=_sub_roman(p['stem']), answer=_sub_roman(str(p['answer'])), markingKey=_sub_roman(str(p['markingKey'])))
            parts.append((p, m_))
        stems = [p['stem'] for p, _ in parts]
        if len(set(stems)) < len(stems):
            return None
        intro = f'This question is about {clean_name(st["name"])}.'
        L = 'abcdef'
        stem = intro + '\n\n' + '\n\n'.join(f'({L[i]}) {p["stem"]} [{m_}]' for i, (p, m_) in enumerate(parts))
        ans = ' '.join(f'({L[i]}) {p["answer"]}' for i, (p, m_) in enumerate(parts))
        key = ' '.join(f'({L[i]}) [{m_} marks] {_fix_marks(p["markingKey"], m_)}' for i, (p, m_) in enumerate(parts))
        return dict(stem=stem, answer=ans, markingKey=key, type='multi_step' if style == 'p2' else 'long',
                    marks=sum(m_ for _, m_ in parts), gap='G5')
    return fn


P2_SPECS = [
    [('C1', 2, 2), ('C3', 3, 4), ('C2', 3, 4)],
    [('C2', 2, 3), ('C3', 3, 4), ('C2', 3, 3)],
    [('C1', 2, 2), ('C2', 3, 3), ('C3', 4, 5)],
]
P2X_SPECS = [
    [('C2', 3, 3), ('C3', 3, 4), ('C3', 4, 3), ('C4', 4, 5)],
    [('C1', 2, 2), ('C2', 3, 4), ('C3', 4, 4), ('C4', 4, 5)],
]

STYLE = {'eval_marks': 6, 'essay_marks': 12,
         'markband': 'IB-style extended response: 9-12 – accurate chemistry throughout, correct terminology, equations/data used to support each point, balanced evaluation and a justified conclusion; 5-8 – mostly accurate, some support, limited evaluation; 1-4 – fragmentary, largely descriptive.'}


SUPD = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-'}
NUM_RE = re.compile(r'^([+−-]?)(\d+(?:\.\d+)?)(?: × 10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+))?(?:\s+(.*))?$')


def parse_num(ans):
    """'−890 kJ mol⁻¹' -> (value, sig figs, unit, signed) or None for anything that is not a single quantity."""
    m = NUM_RE.match(ans.strip())
    if not m:
        return None
    sign, mant, exp, unit = m.groups()
    unit = unit or ''
    if re.search(r'\d', unit.replace('⁻¹', '').replace('⁻²', '').replace('⁻³', '').replace('³', '').replace('²', '')):
        return None
    if any(ch in unit for ch in ';,()=') or len(unit) > 18:
        return None
    v = float(mant) * (10 ** int(''.join(SUPD[c] for c in exp)) if exp else 1)
    if sign in ('−', '-'):
        v = -v
    digits = mant.replace('.', '').lstrip('0') or '0'
    n = max(2, min(4, len(digits) if '.' in mant or exp else len(mant.rstrip('0')) or 1))
    return v, n, unit, bool(sign)


def mcqize(t):
    """MCQ version of a numerical template: same stem, distractors from typical slips (×10ⁿ, ×2, sign)."""
    def fn(rng, slot):
        pr = None
        for dd in dict.fromkeys([slot.d, 2, 1]):
            out = t.fn(rng, dataclasses.replace(slot, d=dd, type='numerical'))
            if out is None:
                continue
            if out.get('type') == 'mcq':
                return out
            pr = parse_num(str(out['answer']))
            if pr is not None:
                break
        if pr is None:
            return None
        v, n, unit, signed = pr
        if v == 0:
            return None
        f = (lambda x: sgn(x, n, unit)) if signed else (lambda x: q(x, unit, n))
        cands = [v * 10, v / 10, v * 2, v / 2, v * 1000, v / 1000, v * 3, v / 3]
        if signed:
            cands = [-v, -v, -v * 2] + cands
        rng.shuffle(cands)
        if signed:
            cands.insert(0, -v)
        right = f(v)
        ws = []
        for c in cands:
            sx = f(c)
            if sx != right and sx not in ws:
                ws.append(sx)
        if len(ws) < 3:
            return None
        stem = out['stem']
        return mcq(rng, stem, right, ws[:3], out['markingKey'])
    return T(t.c, t.d, fn, 'mcq', None, 'mcq_' + t.name)


_MINUS = re.compile(r'(?<=[\s(=:/\[])-(?=\d)|^-(?=\d)')
_DOTS = re.compile(r'(?<!\.)\.\.(?!\.)')


def _tidy(t):
    """Clean doubled full stops that arise when a fact ending in '.' is joined to a key."""
    def fn(rng, slot):
        out = t.fn(rng, slot)
        if out:
            for k in ('stem', 'answer', 'markingKey'):
                if isinstance(out.get(k), str):
                    out[k] = _MINUS.sub('−', _DOTS.sub('.', out[k]))
            if out.get('options'):
                out['options'] = [_MINUS.sub('−', o) for o in out['options']]
                if isinstance(out.get('answer'), str) and out['answer'] not in out['options']:
                    return None
        return out
    return T(t.c, t.d, fn, t.type, t.style, t.name)


def make_templates(R):
    cache: dict = {}

    def templates(st):
        if st['id'] in cache:
            return cache[st['id']]
        base = R.build(st, STYLE)
        base = base + [mcqize(t) for t in base if t.type == 'numerical' and t.style is None]
        out = list(base)
        if not any(t.style == 'p1b' for t in base):
            chk = st['id'].rsplit('-', 2)[-2]
            for k2, ts in R.t.items():
                if k2.startswith(chk + '-'):
                    out += [t for t in ts if t.style == 'p1b']
        for i, spec in enumerate(P2_SPECS):
            out.append(T(('C3', 'C4'), (3, 5), composite(st, base, spec, 'p2'), 'multi_step', 'p2', f'p2_{i}'))
        for i, spec in enumerate(P2X_SPECS):
            out.append(T('C4', (3, 5), composite(st, base, spec, 'p2x'), 'long', 'p2x', f'p2x_{i}'))
        out = [_tidy(t) for t in out]
        cache[st['id']] = out
        return out
    return templates
