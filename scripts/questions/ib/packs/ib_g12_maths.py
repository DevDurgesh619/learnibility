"""IB DP Mathematics: Analysis & Approaches SL/HL (2019 guide), DP year 2 – ib-g12-maths.

Paper conventions used in the items:
  * Paper 1 (no calculator) – exact answers (surds, π, ln, fractions); tagged style 'p1'.
  * Paper 2 (GDC allowed)   – answers to 3 significant figures (angles in radians unless stated); style 'p2'.
  * Section B / extended    – multi-part structured questions; style 'ext'.
  * HL Paper 3              – extended problem-solving / generalising questions; style 'p3'.
Markschemes use M1 (method), A1 (accuracy, dependent on M), R1 (reasoning), AG (answer given) and
(M1)/(A1) for implied marks, as in IB markschemes. Every numerical answer is computed with sympy/math.
"""
from __future__ import annotations

import math
import re
from fractions import Fraction as Fr

import sympy as sp

from _common import F, Registry, T, fmt, frac, name, two_names, CITIES
from _common import mcq as _mcq

_MINUS = re.compile(r'(?:(?<=^)|(?<=[\s(\[,=/:;]))-(?=[\dA-Za-z(π√∞])')


def fixminus(s_):
    if not isinstance(s_, str):
        return s_
    s_ = _MINUS.sub('−', s_)
    s_ = s_.replace('+ −', '− ').replace('− −', '+ ').replace('−1y', '−y').replace('−1x', '−x')
    s_ = re.sub(r'(?<![\d.\w/^⁰¹²³⁴⁵⁶⁷⁸⁹])1([a-z])(?=[\s²³⁴⁵()+−,;.=]|$)', r'\1', s_)
    return s_


def mcq(rng, stem, correct, wrongs, key, **kw):
    return _mcq(rng, fixminus(stem), fixminus(str(correct)), [fixminus(str(w)) for w in wrongs], fixminus(key), **kw)

CONFIG = {'minutesPerMark': 1.1, 'mcqMinutes': 1.5}

# One mock = the three HL papers in miniature (26 items): Paper 1 (no GDC) Section A short + Section B extended,
# Paper 2 (GDC) Section A short + Section B extended, Paper 3 extended problem-solving. Fixed marks per section.
MOCK = [
    dict(section='Paper 1 Section A – short response, no calculator', count=9, c=['C2', 'C3', 'C3'], d=[2, 3, 3], type='short', marks=6, style='p1'),
    dict(section='Paper 1 Section B – extended response, no calculator', count=3, c=['C4'], d=[4, 4, 5], type='multi_step', marks=15, style='ext'),
    dict(section='Paper 2 Section A – short response, calculator allowed', count=9, c=['C3', 'C2', 'C3'], d=[2, 3, 3], type='short', marks=6, style='p2'),
    dict(section='Paper 2 Section B – extended response, calculator allowed', count=3, c=['C4'], d=[4, 5, 4], type='multi_step', marks=15, style='ext'),
    dict(section='Paper 3 – extended problem-solving (HL)', count=2, c=['C4'], d=[5], type='multi_step', marks=20, style='p3'),
]

R = Registry()
x, y, t, k_ = sp.symbols('x y t k', real=True)
pi = sp.pi
r2, r3 = sp.sqrt(2), sp.sqrt(3)


def init(subject_id):
    pass


def templates(st):
    return R.build(st, {'eval_marks': 6, 'essay_marks': 8,
                        'markband': 'Criterion-referenced: clear mathematical reasoning, correct notation, a justified conclusion.'})


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
_SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
_FN = {'asin': 'arcsin', 'acos': 'arccos', 'atan': 'arctan', 'log': 'ln', 'csc': 'cosec'}


def P(e):
    """Pretty-print a sympy expression in IB-style text: x**2 -> x², exp(2*x) -> e^(2x), log -> ln."""
    s = e if isinstance(e, str) else sp.sstr(e)
    s = re.sub(r'\bexp\(', 'e^(', s)
    for a, b in _FN.items():
        s = re.sub(r'\b%s\(' % a, b + '(', s)
    s = re.sub(r'\bpi\b', 'π', s)
    s = re.sub(r'\bE\b', 'e', s)
    s = s.replace('zoo', '∞').replace('oo', '∞')
    s = re.sub(r'sqrt\(([A-Za-z0-9]+)\)', r'√\1', s)
    s = s.replace('sqrt(', '√(')
    s = re.sub(r'\*\*(\d+)', lambda m_: m_.group(1).translate(_SUP), s)
    s = re.sub(r'\*\*\((-?\d+)\)', lambda m_: m_.group(1).translate(_SUP), s)
    s = re.sub(r'\*\*\(([^()]+)\)', r'^(\1)', s)
    s = s.replace('**', '^')
    s = re.sub(r'\^\(([A-Za-z0-9]+)\)', r'^\1', s)
    s = re.sub(r'(\d)\*(?=[A-Za-z(√π])', r'\1', s)
    s = re.sub(r'\*(?=[a-z]{2,}\(|e\^|√)', ' ', s)
    s = s.replace('*', '')
    s = s.replace('-', '−')
    s = re.sub(r'^−(\d+(?:/\d+)?) \+ ([^−+]+)$', r'\2 − \1', s)
    return s


def nice(e):
    """Exact surd expression as text, combining over a common denominator: (√6 − √2)/4."""
    e = sp.expand(sp.radsimp(sp.expand(e)))
    terms = sp.Add.make_args(e)
    if len(terms) == 1:
        return P(e)
    d = sp.ilcm(*[sp.fraction(sp.together(tm))[1] for tm in terms]) if all(sp.fraction(sp.together(tm))[1].is_Integer for tm in terms) else 1
    if d == 1:
        return P(e)
    num = sp.expand(e * d)
    return f'({P(num)})/{d}'


def ex(e):
    """Exact simplified value as text."""
    return P(sp.nsimplify(sp.simplify(e)) if not isinstance(e, str) else e)


def s3(v):
    """3 significant figures."""
    v = float(v)
    if v == 0:
        return '0'
    mag = math.floor(math.log10(abs(v)))
    dec = max(0, 2 - mag)
    r = round(v, dec)
    if dec == 0:
        return str(int(round(r, 2 - mag)))
    return f'{r:.{dec}f}'.replace('-', '−')


def nz(rng, lo, hi, excl=(0,)):
    return rng.choice([i for i in range(lo, hi + 1) if i not in excl])


def vec(v):
    return '(' + ', '.join(P(c) for c in v) + ')'


def col(v):
    """column vector written inline as (a, b, c)ᵀ in IB style i, j, k components."""
    return '(' + ', '.join(P(c) for c in v) + ')'


def ijk(v):
    parts = []
    for c, e in zip(v, ('i', 'j', 'k')):
        c = sp.nsimplify(c)
        if c == 0:
            continue
        mag = abs(c)
        coef = '' if mag == 1 else P(mag)
        sign = '−' if c < 0 else '+'
        parts.append((sign, f'{coef}{e}'))
    if not parts:
        return '0'
    s = ('−' if parts[0][0] == '−' else '') + parts[0][1]
    for sg, tm in parts[1:]:
        s += f' {sg} {tm}'
    return s


def pick(rng, frames):
    return rng.choice(frames)


def who(rng):
    return name(rng)


def mk(stem, answer, key, marks=None, type=None, gap=None):
    d = dict(stem=fixminus(stem), answer=fixminus(answer), markingKey=fixminus(key))
    if type:
        d['type'] = type
    if marks:
        d['marks'] = marks
    if gap:
        d['gap'] = gap
    return d


def build_parts(rng, intro, plist, kmin=3, gap=None):
    """Multi-part item from (question, answer, key, marks, required) parts; optional parts are dropped at random
    so that extended items vary in structure as well as in numbers."""
    intro = rng.choice(intro) if isinstance(intro, (list, tuple)) else intro
    keep = [p_ for p_ in plist if p_[4] or rng.random() < 0.65]
    i = 0
    while len(keep) < min(kmin, len(plist)):
        cand = [p_ for p_ in plist if p_ not in keep]
        keep.append(cand[i % len(cand)])
        i += 1
    keep.sort(key=plist.index)
    L = 'abcdefgh'
    stem = intro + '\n' + '\n'.join(f'({L[j]}) {p_[0]}' for j, p_ in enumerate(keep))
    ans = ' '.join(f'({L[j]}) {p_[1]}' for j, p_ in enumerate(keep))
    key = ' '.join(f'({L[j]}) {p_[2]}' for j, p_ in enumerate(keep))
    out = dict(stem=fixminus(stem), answer=fixminus(ans), markingKey=fixminus(key) + f' [Total {sum(p_[3] for p_ in keep)} marks]', marks=sum(p_[3] for p_ in keep))
    if gap:
        out['gap'] = gap
    return out


TRIG = {'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan}
STD = [k * pi / 6 for k in range(0, 13)] + [k * pi / 4 for k in (1, 3, 5, 7)]
EXACT_POOL = [sp.Integer(0), sp.Rational(1, 2), r2 / 2, r3 / 2, sp.Integer(1), -sp.Rational(1, 2), -r2 / 2, -r3 / 2,
              sp.Integer(-1), r3, r3 / 3, -r3, -r3 / 3]


def deg(a):
    return int(sp.nsimplify(a * 180 / pi))


def quadrant(a):
    v = float(a) % (2 * math.pi)
    return 1 if v < math.pi / 2 else 2 if v < math.pi else 3 if v < 3 * math.pi / 2 else 4


def exact_wrongs(rng, v, n=3):
    v = sp.nsimplify(v)
    pref = [-v] + [w for w in EXACT_POOL if w != v and w != -v]
    out = []
    for w in pref:
        s_ = P(w)
        if s_ != P(v) and s_ not in out:
            out.append(s_)
    first = out[:1]
    rest = out[1:]
    rng.shuffle(rest)
    return (first + rest)[:n]


def sols_in(expr, lo, hi, var=x):
    """Sorted exact solutions of expr = 0 on [lo, hi]."""
    S = sp.solveset(expr, var, sp.Interval(lo, hi))
    if not isinstance(S, sp.FiniteSet):
        return None
    return sorted(S, key=lambda e: float(e))


def nsols(f, lo, hi, n=1500):
    """Numerical roots of a python function f on [lo, hi] by sign change + bisection."""
    out = []
    step = (hi - lo) / n
    a = lo
    fa = f(a)
    if abs(fa) < 1e-12:
        out.append(a)
    for i in range(1, n + 1):
        b = lo + i * step
        fb = f(b)
        if abs(fb) < 1e-12:
            out.append(b)
        elif fa * fb < 0:
            p, q = a, b
            for _ in range(55):
                mid = (p + q) / 2
                if f(p) * f(mid) <= 0:
                    q = mid
                else:
                    p = mid
            out.append((p + q) / 2)
        a, fa = b, fb
    res = []
    for r in out:
        if not res or abs(r - res[-1]) > 1e-7:
            res.append(r)
    return res


PYTH = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]
QUAD_TXT = {1: '0 < θ < π/2', 2: 'π/2 < θ < π', 3: 'π < θ < 3π/2', 4: '3π/2 < θ < 2π'}
QSIGN = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}  # (cos sign, sin sign)


# =============================================================================================
# ch01 Trigonometric functions and identities
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('unit circle', 'the circle of radius 1 centred at the origin; the point at angle θ (anticlockwise from the positive x-axis) has coordinates (cos θ, sin θ)'),
           ('radian', 'the angle subtended at the centre of a circle by an arc equal in length to the radius; π radians = 180°'),
           ('tan θ (unit circle definition)', 'the ratio sin θ / cos θ, i.e. the gradient of the radius to the point (cos θ, sin θ); undefined when cos θ = 0'),
           ('reference angle', 'the acute angle between the terminal arm of θ and the x-axis, used with the quadrant sign to find exact values')],
    facts=[('Which of the following is the exact value of cos(2π/3)?', '−1/2', ['1/2', '−√3/2', '√3/2'], '2π/3 is in the second quadrant, reference angle π/3, cosine negative: −1/2.'),
           ('In which quadrant are sin θ and tan θ both negative?', 'Fourth quadrant', ['First quadrant', 'Second quadrant', 'Third quadrant'], 'In quadrant 4, x > 0 and y < 0, so sin θ = y < 0 and tan θ = y/x < 0.'),
           ('For which angle θ in [0, 2π] is tan θ undefined?', 'θ = π/2', ['θ = π', 'θ = π/4', 'θ = 0'], 'tan θ = sin θ/cos θ and cos(π/2) = 0.'),
           ('Which of the following is the exact value of sin(7π/4)?', '−√2/2', ['√2/2', '−1/2', '−√3/2'], '7π/4 is in quadrant 4 with reference angle π/4, sine negative.'),
           ('What is 135° in radians?', '3π/4', ['2π/3', '5π/6', '3π/5'], '135 × π/180 = 3π/4.')],
    why=[('Explain why −1 ≤ sin θ ≤ 1 for every real θ.', 'sin θ is the y-coordinate of a point on the unit circle (radius 1), so it can never be further than 1 from 0 on the vertical axis.'),
         ('Explain why tan(π/2) is undefined.', 'At θ = π/2 the point on the unit circle is (0, 1); tan θ = sin θ/cos θ = 1/0 which is undefined (the radius is vertical, its gradient is undefined).'),
         ('Explain, using the unit circle, why cos θ is negative for π/2 < θ < 3π/2.', 'For these angles the point (cos θ, sin θ) lies to the left of the y-axis (quadrants 2 and 3), so its x-coordinate cos θ is negative.'),
         ('Explain why sin(θ + 2π) = sin θ for all θ.', 'Adding 2π is one full turn round the unit circle, returning to the same point, so the y-coordinate is unchanged; sine has period 2π.'),
         ('Explain why sin(π/4) = cos(π/4).', 'At π/4 the radius bisects the first quadrant, so the point lies on y = x and its two coordinates are equal (both √2/2).')],
    misc=[('sin(π/6) = √3/2 because π/6 is a small angle.', 'sin(π/6) = 1/2: in the 30-60-90 triangle the side opposite 30° is half the hypotenuse; √3/2 is cos(π/6) = sin(π/3).'),
          ('tan(3π/4) = 1 because the reference angle is π/4.', 'The reference angle gives the size, but 3π/4 is in quadrant 2 where tan is negative, so tan(3π/4) = −1.'),
          ('cos(−π/3) = −1/2 because the angle is negative.', 'A negative angle is measured clockwise; −π/3 is in quadrant 4 where cosine is positive, so cos(−π/3) = 1/2 (cosine is even).'),
          ('sin(π) = 1 because sin is largest at π.', 'At θ = π the point on the unit circle is (−1, 0), so sin π = 0; the maximum value 1 occurs at π/2.')],
))


def _ang_txt(a, degrees=False):
    return f'{deg(a)}°' if degrees else P(a)


@R.add('ch01-st1', 'C1', (1, 3), 'mcq', style='p1')
def unit_exact_mcq(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    a = rng.choice([s for s in STD if not (fn == 'tan' and sp.cos(s) == 0)])
    v = sp.nsimplify(TRIG[fn](a))
    use_deg = slot.d <= 1 and rng.random() < 0.6
    stem = pick(rng, [f'Find the exact value of {fn}({_ang_txt(a, use_deg)}).',
                      f'Without a calculator, which of the following equals {fn}({_ang_txt(a, use_deg)})?',
                      f'What is the exact value of {fn} {_ang_txt(a, use_deg)}?'])
    return mcq(rng, stem, P(v), exact_wrongs(rng, v),
               f'{_ang_txt(a, use_deg)} lies in quadrant {quadrant(a)}; using the reference angle and the sign of {fn} there gives {P(v)}.')


@R.add('ch01-st1', 'C1', (1, 3), 'short', style='p1')
def unit_exact_short(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    a = rng.choice([s for s in STD if not (fn == 'tan' and sp.cos(s) == 0) and s != 0])
    if slot.d >= 3:
        a = a + rng.choice([-2, 2]) * pi
    v = sp.nsimplify(TRIG[fn](a))
    return mk(f'Write down the exact value of {fn}({P(a)}).', P(v),
              f'A1 for {P(v)}. Reference angle and quadrant sign (angle coterminal with {P(a % (2 * pi))} where relevant).', 1)


@R.add('ch01-st1', 'C1', (1, 2), 'short')
def unit_coords(rng, slot):
    a = rng.choice([s for s in STD if s not in (0, 2 * pi)])
    return mk(f'The point P lies on the unit circle so that OP makes an angle of {P(a)} radians, measured anticlockwise from the positive x-axis. Write down the exact coordinates of P.',
              f'({P(sp.cos(a))}, {P(sp.sin(a))})', f'P = (cos θ, sin θ) = ({P(sp.cos(a))}, {P(sp.sin(a))}). A1 A1.', 2)


@R.add('ch01-st1', 'C2', (1, 4), 'explain', style='p1')
def unit_sign_explain(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    a = rng.choice([s for s in STD if quadrant(s) in (2, 3, 4) and sp.cos(s) != 0 and sp.sin(s) != 0])
    q = quadrant(a)
    v = sp.nsimplify(TRIG[fn](a))
    ref = {2: pi - a, 3: a - pi, 4: 2 * pi - a}[q]
    sign = 'positive' if v > 0 else 'negative'
    frames = [f'Without a calculator, explain why {fn}({P(a)}) = {"" if v > 0 else "−"}{fn}({P(ref)}).',
              f'Using the unit circle, explain why {fn}({P(a)}) is {sign} and hence write down its exact value.',
              f'Explain how the reference angle and the quadrant of {P(a)} give the exact value of {fn}({P(a)}).']
    return mk(rng.choice(frames), P(v),
              f'{P(a)} lies in quadrant {q} (R1); the reference angle is {P(ref)} (A1); in quadrant {q} the {"y" if fn == "sin" else "x" if fn == "cos" else "ratio y/x"}-value makes {fn} {sign} (R1); so {fn}({P(a)}) = {P(v)} (A1).',
              3 if slot.d >= 3 else 2, 'explain')


@R.add('ch01-st1', 'C3', (1, 4), 'short', style='p1')
def unit_expr(rng, slot):
    n = 2 if slot.d <= 2 else 3
    terms, expr = [], 0
    for i in range(n):
        fn = rng.choice(['sin', 'cos', 'tan'])
        a = rng.choice([s for s in STD if s != 0 and not (fn == 'tan' and sp.cos(s) == 0)])
        c = rng.choice([1, 2, 3, -1, -2, 4])
        pw = 2 if (slot.d >= 3 and rng.random() < 0.5) else 1
        expr += c * TRIG[fn](a) ** pw
        coef = '' if c == 1 else '−' if c == -1 else str(c).replace('-', '−')
        terms.append(f'{coef}{fn}{"²" if pw == 2 else ""}({P(a)})')
    s = terms[0]
    for tm in terms[1:]:
        s += (' − ' + tm[1:]) if tm.startswith('−') else (' + ' + tm)
    v = sp.radsimp(sp.simplify(expr))
    return mk(f'Find the exact value of {s}.', P(v),
              f'Each exact trigonometric value correct (A1 each, may be implied); combined and simplified: {P(v)} (A1). No calculator: decimals score A0.', n + 1)


@R.add('ch01-st1', 'C3', (2, 4), 'short', style='p1')
def unit_chord(rng, slot):
    a, b = rng.sample([s for s in STD if s not in (2 * pi,)], 2)
    if a == b:
        return None
    d2 = sp.simplify((sp.cos(a) - sp.cos(b)) ** 2 + (sp.sin(a) - sp.sin(b)) ** 2)
    d = sp.sqrtdenest(sp.radsimp(sp.sqrt(d2)))
    if P(d).count('√') > 2:
        d = sp.sqrt(sp.nsimplify(d2))
        dtxt = f'√({nice(d2)})'
    else:
        dtxt = P(d)
    return mk(f'Points A and B lie on the unit circle at angles {P(a)} and {P(b)} respectively (measured anticlockwise from the positive x-axis). Find the exact distance AB.',
              dtxt, f'A = ({P(sp.cos(a))}, {P(sp.sin(a))}), B = ({P(sp.cos(b))}, {P(sp.sin(b))}) (A1 A1); distance formula (M1); AB² = {nice(d2)}, AB = {dtxt} (A1).', 4)


@R.add('ch01-st1', 'C4', (3, 5), 'multi_step', style='ext')
def unit_triangle(rng, slot):
    a = rng.choice([pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3, 3 * pi / 4, 5 * pi / 6, pi])
    ang = rng.choice([pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3, 3 * pi / 4, 5 * pi / 6])
    b = a + ang
    if b not in STD:
        return None
    area = sp.nsimplify(sp.sin(ang) / 2)
    ab2 = sp.nsimplify(sp.simplify(2 - 2 * sp.cos(ang)))
    return mk(f'The points A and B lie on the unit circle with centre O, where angle AOx = {P(a)} and angle BOx = {P(b)} (both measured anticlockwise from the positive x-axis).\n(a) Write down the exact coordinates of A and B.\n(b) Find the exact size of angle AOB.\n(c) Find the exact area of triangle AOB.\n(d) Show that AB² = 2 − 2cos(AOB) and hence find AB² exactly.',
              f'(a) A({P(sp.cos(a))}, {P(sp.sin(a))}), B({P(sp.cos(b))}, {P(sp.sin(b))}) (b) {P(ang)} (c) {P(area)} (d) AB² = {P(ab2)}',
              f'(a) A1 A1. (b) {P(b)} − {P(a)} = {P(ang)} A1. (c) ½(1)(1)sin({P(ang)}) M1 = {P(area)} A1. (d) cosine rule with OA = OB = 1: AB² = 1 + 1 − 2cos AOB M1 AG; = {P(ab2)} A1.', 8)


@R.add('ch01-st1', 'C4', (2, 4), 'multi_step', style='p1')
def unit_tan_given(rng, slot):
    a, b, c = rng.choice(PYTH)
    q = rng.choice([2, 3, 4])
    cs, ss = QSIGN[q]
    tanv = Fr(ss * a, cs * b)
    sinv, cosv = Fr(ss * a, c), Fr(cs * b, c)
    expr_v = sinv + cosv
    return mk(f'The angle θ satisfies tan θ = {frac(tanv).replace("-", "−")} and {QUAD_TXT[q]}.\n(a) Find the exact value of cos θ.\n(b) Find the exact value of sin θ.\n(c) Hence find the exact value of sin θ + cos θ and state, with a reason, its sign.',
              f'(a) {frac(cosv).replace("-", "−")} (b) {frac(sinv).replace("-", "−")} (c) {frac(expr_v).replace("-", "−")}',
              f'Right-angled triangle with sides {a}, {b}, hypotenuse {c} (M1); sign of cos in quadrant {q} (R1) cos θ = {frac(cosv)} (A1); sin θ = {frac(sinv)} (A1); sum {frac(expr_v)} (A1), sign follows (R1).', 6)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st2', F(
    terms=[('Pythagorean identity', 'the identity cos²θ + sin²θ = 1 for all θ, from x² + y² = 1 on the unit circle'),
           ('double angle identity for sine', 'the identity sin 2θ = 2 sin θ cos θ'),
           ('double angle identities for cosine', 'the identities cos 2θ = cos²θ − sin²θ = 2cos²θ − 1 = 1 − 2sin²θ'),
           ('identity', 'an equation that is true for every value of the variable for which both sides are defined')],
    facts=[('Which of the following is NOT equal to cos 2θ?', '2 sin θ cos θ', ['cos²θ − sin²θ', '1 − 2sin²θ', '2cos²θ − 1'], '2 sin θ cos θ = sin 2θ; the other three are the three forms of cos 2θ.'),
           ('Which expression is identical to 1 − cos²x?', 'sin²x', ['cos²x − 1', 'cos 2x', '2 sin x'], 'From sin²x + cos²x = 1.'),
           ('sin²(3x) + cos²(3x) is equal to', '1', ['3', '9', 'cos 6x'], 'The Pythagorean identity holds for any angle, including 3x.'),
           ('Which is an expression for sin²θ that is useful for integration?', '(1 − cos 2θ)/2', ['(1 + cos 2θ)/2', '1 − 2cos 2θ', '(cos 2θ − 1)/2'], 'cos 2θ = 1 − 2sin²θ rearranges to sin²θ = (1 − cos 2θ)/2.')],
    why=[('Explain how the identity cos²θ + sin²θ = 1 follows from the unit circle.', 'The point (cos θ, sin θ) lies on x² + y² = 1, so substituting x = cos θ, y = sin θ gives cos²θ + sin²θ = 1.'),
         ('Explain why cos 2θ has three equivalent forms.', 'Start from cos 2θ = cos²θ − sin²θ; replacing sin²θ by 1 − cos²θ gives 2cos²θ − 1, replacing cos²θ by 1 − sin²θ gives 1 − 2sin²θ.'),
         ('Explain why knowing sin θ alone is not enough to find cos θ uniquely.', 'cos²θ = 1 − sin²θ gives two square roots ±; the quadrant of θ is needed to choose the sign.'),
         ('Explain which form of cos 2θ you would choose to solve cos 2θ = sin θ, and why.', 'Use cos 2θ = 1 − 2sin²θ so the equation contains only sin θ; it becomes the quadratic 2sin²θ + sin θ − 1 = 0.')],
    misc=[('sin 2x = 2 sin x for all x.', 'Counter-example x = π/2: sin π = 0 but 2 sin(π/2) = 2. The correct identity is sin 2x = 2 sin x cos x.'),
          ('cos 2θ = 2cos θ.', 'Counter-example θ = 0: cos 0 = 1 but 2cos 0 = 2. The identity is cos 2θ = 2cos²θ − 1.'),
          ('If sin θ = 3/5 then cos θ = 4/5.', 'cos θ = ±4/5; it is −4/5 if θ is obtuse (quadrant 2), so the quadrant must be stated.'),
          ('sin²x means sin(x²).', 'sin²x means (sin x)²; sin(x²) is the sine of x squared, a different function.')],
))


@R.add('ch01-st2', 'C1', (1, 3), 'mcq')
def double_ident_mcq(rng, slot):
    k = rng.choice([2, 3, 4, 5, 'θ/2', 'x/2'])
    if isinstance(k, str):
        arg, dbl = k, k.split('/')[0]
    else:
        arg, dbl = f'{k}x', f'{2 * k}x'
    kind = rng.choice(['s', 'c1', 'c2', 'c3'])
    stem_e = {'s': f'2 sin({arg}) cos({arg})', 'c1': f'cos²({arg}) − sin²({arg})', 'c2': f'1 − 2sin²({arg})', 'c3': f'2cos²({arg}) − 1'}[kind]
    correct = f'sin({dbl})' if kind == 's' else f'cos({dbl})'
    other = f'cos({dbl})' if kind == 's' else f'sin({dbl})'
    w = [other, f'{"sin" if kind == "s" else "cos"}({arg})', f'2{"sin" if kind == "s" else "cos"}({arg})', '1']
    return mcq(rng, f'Which of the following is identical to {stem_e}?', correct, w,
               f'Double angle identity with angle {arg}: {stem_e} = {correct}.')


@R.add('ch01-st2', 'C3', (1, 4), 'short', style='p1')
def pyth_quadrant(rng, slot):
    if slot.d <= 2 or rng.random() < 0.5:
        a, b, c = rng.choice(PYTH)
        sv = sp.Rational(a, c)
    else:
        p_, q_ = rng.choice([(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (1, 5), (3, 7)])
        sv = sp.Rational(p_, q_)
    q = rng.choice([1, 2, 3, 4])
    cs, ss = QSIGN[q]
    given = rng.choice(['sin', 'cos'])
    if given == 'sin':
        g = ss * sv
        o = cs * sp.sqrt(1 - sv ** 2)
        so, co = g, o
    else:
        g = cs * sv
        o = ss * sp.sqrt(1 - sv ** 2)
        so, co = o, g
    tn = sp.radsimp(so / co)
    other = 'cos' if given == 'sin' else 'sin'
    return mk(f'Given that {given} θ = {P(g)} and {QUAD_TXT[q]}, find the exact value of (a) {other} θ (b) tan θ.',
              f'(a) {P(sp.radsimp(o))} (b) {P(tn)}',
              f'Use sin²θ + cos²θ = 1: {other}²θ = 1 − ({P(g)})² = {P(1 - sv ** 2)} (M1); choose the sign for quadrant {q} (R1); {other} θ = {P(sp.radsimp(o))} (A1); tan θ = sin θ/cos θ = {P(tn)} (A1).', 4)


@R.add('ch01-st2', 'C3', (2, 5), 'short', style='p1')
def double_values(rng, slot):
    a, b, c = rng.choice(PYTH)
    q = rng.choice([1, 2, 3, 4])
    cs, ss = QSIGN[q]
    sv, cv = sp.Rational(ss * a, c), sp.Rational(cs * b, c)
    s2, c2 = 2 * sv * cv, cv ** 2 - sv ** 2
    want = rng.choice(['s2', 'c2', 't2', 'both'])
    given = rng.choice([('sin θ', sv), ('cos θ', cv)])
    stem_w = {'s2': 'sin 2θ', 'c2': 'cos 2θ', 't2': 'tan 2θ', 'both': 'sin 2θ and cos 2θ'}[want]
    ans = {'s2': P(s2), 'c2': P(c2), 't2': P(s2 / c2), 'both': f'sin 2θ = {P(s2)}, cos 2θ = {P(c2)}'}[want]
    return mk(f'It is given that {given[0]} = {P(given[1])}, where {QUAD_TXT[q]}. Find the exact value of {stem_w}.', ans,
              f'Other ratio by Pythagoras with correct sign: sin θ = {P(sv)}, cos θ = {P(cv)} (M1 A1); double angle identity used (M1); {ans} (A1).', 4 if want != 'both' else 5)


@R.add('ch01-st2', 'C2', (2, 4), 'explain', style='p1')
def double_counter(rng, slot):
    a = rng.choice([pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3])
    claim, true_l, wrong_r = rng.choice([
        ('sin 2x = 2 sin x', sp.sin(2 * a), 2 * sp.sin(a)),
        ('cos 2x = 2 cos x', sp.cos(2 * a), 2 * sp.cos(a)),
        ('cos 2x = cos²x + sin²x', sp.cos(2 * a), sp.Integer(1)),
        ('sin 2x = sin²x', sp.sin(2 * a), sp.sin(a) ** 2)])
    l, r_ = sp.nsimplify(true_l), sp.nsimplify(sp.simplify(wrong_r))
    if sp.simplify(l - r_) == 0:
        return None
    nm = who(rng)
    return mk(f'{nm} claims that {claim} for all x. Use x = {P(a)} to show that the claim is false, and state the correct identity.',
              f'At x = {P(a)}: left side {P(l)}, right side {P(r_)}; not equal.',
              f'Left side evaluated exactly = {P(l)} (A1); right side = {P(r_)} (A1); since they differ the statement is not an identity (R1); correct identity stated (A1).', 4, 'explain', 'G2')


R.static('ch01-st2', 'C2', (2, 4), [
    ('Show that (sin x + cos x)² ≡ 1 + sin 2x.', '(sin x + cos x)² = sin²x + 2 sin x cos x + cos²x = 1 + sin 2x',
     'Expand: sin²x + 2 sin x cos x + cos²x (M1); use sin²x + cos²x = 1 (M1) and 2 sin x cos x = sin 2x (A1) AG.'),
    ('Show that (1 − cos 2x)/sin 2x ≡ tan x.', '(1 − cos 2x)/sin 2x = 2sin²x/(2 sin x cos x) = tan x',
     '1 − cos 2x = 2sin²x (M1 A1); sin 2x = 2 sin x cos x (A1); cancel to sin x/cos x = tan x AG.'),
    ('Show that cos⁴x − sin⁴x ≡ cos 2x.', '(cos²x − sin²x)(cos²x + sin²x) = cos 2x × 1',
     'Difference of two squares (M1); cos²x + sin²x = 1 (A1); cos²x − sin²x = cos 2x (A1) AG.'),
    ('Show that sin 2x/(1 + cos 2x) ≡ tan x.', '2 sin x cos x/(2cos²x) = tan x',
     '1 + cos 2x = 2cos²x (M1 A1); numerator 2 sin x cos x (A1); simplifies to tan x AG.'),
    ('Show that (cos x − sin x)(cos x + sin x) ≡ cos 2x.', 'cos²x − sin²x = cos 2x', 'Expand (M1) cos²x − sin²x (A1) = cos 2x AG.'),
    ('Show that 2 cosec 2x ≡ sec x cosec x.', '2/(2 sin x cos x) = (1/cos x)(1/sin x)',
     'cosec 2x = 1/sin 2x (M1); sin 2x = 2 sin x cos x (A1); 2/(2 sin x cos x) = sec x cosec x AG (A1).'),
    ('Explain why sin²x = (1 − cos 2x)/2 and use it to write sin²(3x) in terms of cos 6x.', 'sin²(3x) = (1 − cos 6x)/2',
     'cos 2x = 1 − 2sin²x rearranged (R1); replace x by 3x (M1); (1 − cos 6x)/2 (A1).'),
    ('Show that sin 4x ≡ 4 sin x cos x cos 2x.', 'sin 4x = 2 sin 2x cos 2x = 4 sin x cos x cos 2x',
     'sin 4x = 2 sin 2x cos 2x (M1 A1); sin 2x = 2 sin x cos x substituted (A1) AG.'),
], type='explain', marks=3)


@R.add('ch01-st2', 'C3', (2, 4), 'short', style='p1')
def cos2_from_sin(rng, slot):
    p_, q_ = rng.choice([(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (1, 5), (3, 5), (4, 5), (1, 6), (5, 6)])
    v = sp.Rational(p_, q_)
    fn = rng.choice(['sin', 'cos'])
    c2 = 1 - 2 * v ** 2 if fn == 'sin' else 2 * v ** 2 - 1
    frames = [f'Given that {fn} θ = {P(v)}, find the exact value of cos 2θ.',
              f'If {fn} α = {P(v)}, find the exact value of cos 2α, showing which identity you use.',
              f'The acute angle β has {fn} β = {P(v)}. Calculate the exact value of cos 2β.']
    return mk(rng.choice(frames), P(c2), f'Choose cos 2θ = {"1 − 2sin²θ" if fn == "sin" else "2cos²θ − 1"} (M1); substitute {P(v)} (A1); {P(c2)} (A1). No need to find the quadrant: only {fn}² appears.', 3)


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step')
def cos4_chain(rng, slot):
    a, b, c = rng.choice(PYTH[:2] + [(4, 3, 5), (12, 5, 13)])
    cv = sp.Rational(b, c)
    c2 = 2 * cv ** 2 - 1
    c4 = 2 * c2 ** 2 - 1
    s2 = 2 * sp.Rational(a, c) * cv
    s4 = 2 * s2 * c2
    return mk(f'The acute angle θ is such that cos θ = {P(cv)}.\n(a) Find the exact value of sin θ.\n(b) Find the exact values of sin 2θ and cos 2θ.\n(c) Hence find the exact value of cos 4θ and of sin 4θ.\n(d) Determine, with a reason, whether 4θ is acute or obtuse given that 0 < 4θ < π.',
              f'(a) {P(sp.Rational(a, c))} (b) sin 2θ = {P(s2)}, cos 2θ = {P(c2)} (c) cos 4θ = {P(c4)}, sin 4θ = {P(s4)} (d) {"acute" if c4 > 0 else "obtuse"}',
              f'(a) Pythagoras, acute so positive: {a}/{c} A1. (b) M1 A1 A1. (c) cos 4θ = 2cos²2θ − 1 M1 = {P(c4)} A1; sin 4θ = 2 sin 2θ cos 2θ = {P(s4)} A1. (d) cos 4θ {"> 0" if c4 > 0 else "< 0"} so 4θ is {"acute" if c4 > 0 else "obtuse"} R1. Total 8 marks. [Valid only when 0 < 4θ < π; check with θ = arccos({P(cv)}) ≈ {s3(math.acos(float(cv)))}.]', 8)


@R.add('ch01-st2', 'C4', (2, 4), 'multi_step', style='p1')
def pyth_expression(rng, slot):
    a, b, c = rng.choice(PYTH)
    q = rng.choice([2, 3, 4])
    cs, ss = QSIGN[q]
    sv, cv = sp.Rational(ss * a, c), sp.Rational(cs * b, c)
    p_, r_ = nz(rng, -4, 4), nz(rng, -4, 4)
    val = p_ * sv * cv + r_ * (cv ** 2 - sv ** 2)
    return mk(f'Let sin θ = {P(sv)}, where {QUAD_TXT[q]}.\n(a) Find cos θ.\n(b) Hence find the exact value of {p_} sin θ cos θ + {r_} cos 2θ.'.replace('+ -', '− ').replace('-', '−'),
              f'(a) {P(cv)} (b) {P(val)}',
              f'(a) cos²θ = 1 − sin²θ (M1), negative/positive by quadrant {q} (R1), {P(cv)} (A1). (b) sin θ cos θ = {P(sv * cv)}, cos 2θ = {P(cv ** 2 - sv ** 2)} (A1 A1); {P(val)} (A1).', 6)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st3', F(
    terms=[('secant (sec x)', 'the reciprocal of cosine: sec x = 1/cos x, defined where cos x ≠ 0'),
           ('cosecant (cosec x)', 'the reciprocal of sine: cosec x = 1/sin x, defined where sin x ≠ 0'),
           ('cotangent (cot x)', 'cot x = cos x / sin x = 1/tan x, defined where sin x ≠ 0'),
           ('arcsin x', 'the inverse of sine restricted to [−π/2, π/2]; domain −1 ≤ x ≤ 1, range −π/2 ≤ arcsin x ≤ π/2'),
           ('arccos x', 'the inverse of cosine restricted to [0, π]; domain −1 ≤ x ≤ 1, range 0 ≤ arccos x ≤ π'),
           ('arctan x', 'the inverse of tangent restricted to (−π/2, π/2); domain all real x, range −π/2 < arctan x < π/2')],
    facts=[('What is the range of y = arccos x?', '0 ≤ y ≤ π', ['−π/2 ≤ y ≤ π/2', '−π/2 < y < π/2', '0 ≤ y ≤ 2π'], 'Cosine is restricted to [0, π] to make it one-to-one.'),
           ('Which identity follows from dividing sin²θ + cos²θ = 1 by cos²θ?', 'tan²θ + 1 = sec²θ', ['1 + cot²θ = cosec²θ', 'tan²θ − 1 = sec²θ', 'sec²θ + 1 = tan²θ'], 'sin²θ/cos²θ + 1 = 1/cos²θ.'),
           ('What is the domain of y = arcsin x?', '−1 ≤ x ≤ 1', ['all real x', '0 ≤ x ≤ π', '−π/2 ≤ x ≤ π/2'], 'arcsin takes a value of sine as its input, and sine values lie in [−1, 1].'),
           ('The graph of y = sec x has vertical asymptotes where', 'cos x = 0', ['sin x = 0', 'tan x = 0', 'cos x = 1'], 'sec x = 1/cos x is undefined when cos x = 0.'),
           ('Which of the following has range y ≤ −1 or y ≥ 1?', 'y = cosec x', ['y = arcsin x', 'y = cot x', 'y = tan x'], '|sin x| ≤ 1 so |1/sin x| ≥ 1.')],
    why=[('Explain why the sine function must have its domain restricted before an inverse function can be defined.', 'Sine is many-to-one (e.g. sin(π/6) = sin(5π/6)), so it has no inverse; restricting to [−π/2, π/2] makes it one-to-one while still covering every value in [−1, 1].'),
         ('Explain why sec x can never take a value between −1 and 1.', '|cos x| ≤ 1, so |sec x| = 1/|cos x| ≥ 1; values strictly between −1 and 1 are impossible.'),
         ('Explain why arccos(cos(5π/3)) is not equal to 5π/3.', 'arccos returns a value in [0, π]; cos(5π/3) = 1/2 and arccos(1/2) = π/3.'),
         ('Explain why 1 + cot²θ = cosec²θ.', 'Divide sin²θ + cos²θ = 1 through by sin²θ (sin θ ≠ 0): 1 + cos²θ/sin²θ = 1/sin²θ.'),
         ('Explain the difference between sin⁻¹x and (sin x)⁻¹.', 'sin⁻¹x = arcsin x is the inverse function (an angle); (sin x)⁻¹ = 1/sin x = cosec x is the reciprocal.')],
    misc=[('arcsin(1/2) = 5π/6, because sin(5π/6) = 1/2.', 'arcsin has range [−π/2, π/2], so arcsin(1/2) = π/6; 5π/6 is another solution of sin x = 1/2 but not the principal value.'),
          ('sec x is the inverse function of cos x.', 'sec x = 1/cos x is the reciprocal; the inverse function is arccos x.'),
          ('arctan(−1) = 3π/4.', 'The range of arctan is (−π/2, π/2), so arctan(−1) = −π/4.'),
          ('cot x = tan(1/x).', 'cot x = 1/tan x = cos x/sin x; it is the reciprocal of tan x, not tan of a reciprocal.')],
))

INV_VALS = [sp.Integer(0), sp.Rational(1, 2), r2 / 2, r3 / 2, sp.Integer(1), -sp.Rational(1, 2), -r2 / 2, -r3 / 2, sp.Integer(-1)]
TAN_VALS = [sp.Integer(0), r3 / 3, sp.Integer(1), r3, -r3 / 3, sp.Integer(-1), -r3]


@R.add('ch01-st3', 'C1', (1, 3), 'mcq', style='p1')
def inv_mcq(rng, slot):
    fn = rng.choice(['arcsin', 'arccos', 'arctan'])
    v = rng.choice(TAN_VALS if fn == 'arctan' else INV_VALS)
    f = {'arcsin': sp.asin, 'arccos': sp.acos, 'arctan': sp.atan}[fn]
    a = f(v)
    pool = [P(z) for z in [pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3, 3 * pi / 4, 5 * pi / 6, -pi / 6, -pi / 4, -pi / 3, -pi / 2, sp.Integer(0), pi, 7 * pi / 6, 5 * pi / 3]]
    alt = [P(pi - a), P(-a), P(a + pi)]
    wr = [w for w in alt + pool if w != P(a)]
    seen = []
    for w in wr:
        if w not in seen:
            seen.append(w)
    return mcq(rng, f'Find the exact value of {fn}({P(v)}).', P(a), seen[:2] + rng.sample(seen[2:], 1),
               f'{fn} returns its principal value; {fn}({P(v)}) = {P(a)}, which lies in the range of {fn}.')


@R.add('ch01-st3', 'C1', (1, 3), 'short', style='p1')
def recip_exact(rng, slot):
    fn = rng.choice(['sec', 'cosec', 'cot'])
    base = {'sec': sp.cos, 'cosec': sp.sin, 'cot': sp.tan}[fn]
    a = rng.choice([s for s in STD if base(s) != 0 and (fn != 'cot' or sp.cos(s) != 0) and s != 0])
    v = sp.radsimp(1 / base(a))
    return mk(f'Write down the exact value of {fn}({P(a)}).', P(v), f'{fn} = 1/{"cos" if fn == "sec" else "sin" if fn == "cosec" else "tan"} (M1); {P(v)} (A1).', 2)


@R.add('ch01-st3', 'C3', (2, 4), 'short', style='p1')
def inv_compose(rng, slot):
    p_, q_ = rng.choice([(1, 3), (2, 3), (3, 5), (4, 5), (5, 13), (12, 13), (1, 4), (2, 7), (8, 17), (3, 4)])
    v = sp.Rational(p_, q_)
    if rng.random() < 0.3:
        v = -v
    inner, outer = rng.choice([('arcsin', 'cos'), ('arccos', 'sin'), ('arcsin', 'tan'), ('arccos', 'tan'), ('arctan', 'sin'), ('arctan', 'cos'), ('arcsin', 'sec'), ('arccos', 'cosec')])
    f = {'arcsin': sp.asin, 'arccos': sp.acos, 'arctan': sp.atan}[inner]
    g = {'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'sec': sp.sec, 'cosec': sp.csc}[outer]
    val = sp.radsimp(sp.simplify(g(f(v))))
    rng_txt = {'arcsin': '[−π/2, π/2]', 'arccos': '[0, π]', 'arctan': '(−π/2, π/2)'}[inner]
    return mk(f'Find the exact value of {outer}({inner}({P(v)})).', P(val),
              f'Let θ = {inner}({P(v)}), so θ ∈ {rng_txt} (R1); right-angled triangle or Pythagorean identity for the other ratio (M1); sign from the range of {inner} (R1); {P(val)} (A1).', 4)


@R.add('ch01-st3', 'C3', (2, 4), 'short', style='p1')
def sec_tan_ident(rng, slot):
    a, b, c = rng.choice(PYTH)
    q = rng.choice([1, 2, 3, 4])
    cs, ss = QSIGN[q]
    tv = sp.Rational(ss * a, cs * b)
    secv = sp.Rational(cs * c, b)
    cosecv = sp.Rational(ss * c, a)
    want = rng.choice(['sec', 'cosec', 'cot'])
    ans = {'sec': secv, 'cosec': cosecv, 'cot': 1 / tv}[want]
    method = {'sec': f'sec²θ = 1 + tan²θ = {P(1 + tv ** 2)}', 'cosec': f'cosec²θ = 1 + cot²θ = {P(1 + 1 / tv ** 2)}', 'cot': 'cot θ = 1/tan θ'}[want]
    return mk(f'Given that tan θ = {P(tv)} and {QUAD_TXT[q]}, find the exact value of {want} θ.', P(ans),
              f'{method} (M1 A1); sign chosen for quadrant {q} (R1); {want} θ = {P(ans)} (A1).', 4)


@R.add('ch01-st3', 'C2', (2, 4), 'explain', style='p1')
def inv_principal(rng, slot):
    fn, base = rng.choice([('arcsin', 'sin'), ('arccos', 'cos'), ('arctan', 'tan')])
    a = rng.choice({'arcsin': [2 * pi / 3, 3 * pi / 4, 5 * pi / 6, 7 * pi / 6, 4 * pi / 3, 5 * pi / 3],
                    'arccos': [4 * pi / 3, 5 * pi / 4, 7 * pi / 6, 5 * pi / 3, 7 * pi / 4, -pi / 3],
                    'arctan': [3 * pi / 4, 5 * pi / 6, 2 * pi / 3, 5 * pi / 4, 7 * pi / 6, 4 * pi / 3]}[fn])
    inner = sp.nsimplify({'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan}[base](a))
    res = {'arcsin': sp.asin, 'arccos': sp.acos, 'arctan': sp.atan}[fn](inner)
    nm = who(rng)
    return mk(f'{nm} writes {fn}({base}({P(a)})) = {P(a)}. Explain why this is incorrect and find the correct exact value.', P(res),
              f'{base}({P(a)}) = {P(inner)} (A1); the range of {fn} is {"[−π/2, π/2]" if fn == "arcsin" else "[0, π]" if fn == "arccos" else "(−π/2, π/2)"} and {P(a)} is outside it (R1); {fn}({P(inner)}) = {P(res)} (A1).', 3, 'explain', 'G2')


@R.add('ch01-st3', 'C4', (3, 5), 'multi_step')
def inv_sum(rng, slot):
    (a1, b1, c1), (a2, b2, c2) = rng.sample(PYTH[:4], 2)
    A_s, A_c = sp.Rational(a1, c1), sp.Rational(b1, c1)
    B_s, B_c = sp.Rational(a2, c2), sp.Rational(b2, c2)
    sAB = A_s * B_c + A_c * B_s
    cAB = A_c * B_c - A_s * B_s
    return mk(f'Let α = arcsin({a1}/{c1}) and β = arccos({b2}/{c2}).\n(a) Find the exact values of cos α and sin β.\n(b) Find the exact value of sin(α + β).\n(c) Find the exact value of cos(α + β).\n(d) Hence determine whether α + β is greater or less than π/2, justifying your answer.',
              f'(a) cos α = {P(A_c)}, sin β = {P(B_s)} (b) {P(sAB)} (c) {P(cAB)} (d) {"less than" if cAB > 0 else "greater than"} π/2',
              f'(a) α, β acute (R1); cos α = {P(A_c)} A1, sin β = {P(B_s)} A1. (b) compound angle formula M1, {P(sAB)} A1. (c) {P(cAB)} A1. (d) α + β ∈ (0, π) and cos(α + β) {"> 0" if cAB > 0 else "< 0"} R1 so α + β is {"less" if cAB > 0 else "greater"} than π/2 A1.', 8)


R.static('ch01-st3', 'C4', (2, 4), [
    ('Prove the identity (1 + tan²x)/(1 + cot²x) ≡ tan²x.', 'sec²x/cosec²x = sin²x/cos²x = tan²x',
     '1 + tan²x = sec²x (A1); 1 + cot²x = cosec²x (A1); sec²x/cosec²x = (1/cos²x)(sin²x) (M1) = tan²x AG (A1).'),
    ('Prove that sec²x + cosec²x ≡ sec²x cosec²x.', '(sin²x + cos²x)/(sin²x cos²x) = 1/(sin²x cos²x)',
     'Common denominator sin²x cos²x (M1); numerator sin²x + cos²x = 1 (A1); 1/(sin²x cos²x) = sec²x cosec²x AG (A1). Total 4 with clear presentation (R1).'),
    ('Prove that cosec x − sin x ≡ cos x cot x.', '(1 − sin²x)/sin x = cos²x/sin x = cos x cot x',
     'Write cosec x as 1/sin x and combine (M1); 1 − sin²x = cos²x (A1); cos x · (cos x/sin x) (A1) AG (R1).'),
    ('Prove that (sec x − cos x)/sin x ≡ tan x.', '(1 − cos²x)/(cos x sin x) = sin²x/(sin x cos x) = tan x',
     'Combine the numerator (M1); use 1 − cos²x = sin²x (A1); cancel sin x (A1); tan x AG (R1).'),
    ('Show that arctan(1/2) + arctan(1/3) = π/4.', 'tan(A + B) = (1/2 + 1/3)/(1 − 1/6) = 1, A + B ∈ (0, π/2), so A + B = π/4',
     'Let A = arctan(1/2), B = arctan(1/3) (M1); tan(A + B) formula (M1); = (5/6)/(5/6) = 1 (A1); both acute so 0 < A + B < π (R1); A + B = π/4 AG.'),
    ('Show that for x > 0, arctan x + arctan(1/x) = π/2.', 'tan(π/2 − arctan x) = cot(arctan x) = 1/x, and π/2 − arctan x ∈ (0, π/2)',
     'Let θ = arctan x ∈ (0, π/2) (M1); tan(π/2 − θ) = cot θ = 1/x (A1); π/2 − θ ∈ (0, π/2) so it equals arctan(1/x) (R1); rearrange AG (A1).'),
], type='multi_step', marks=4)


@R.add('ch01-st3', 'C4', (3, 5), 'multi_step', style='p1')
def arctan_sum_gen(rng, slot):
    p_, q_ = rng.choice([(1, 2), (1, 3), (1, 4), (2, 3), (1, 5), (2, 5), (3, 4), (1, 7)])
    a = sp.Rational(p_, q_)
    b = (1 - a) / (1 + a)
    c = rng.choice([sp.Rational(1, 2), sp.Rational(1, 3), 2, 3])
    tot = (a + c) / (1 - a * c) if a * c != 1 else None
    if tot is None:
        return None
    return mk(f'(a) Show that arctan({P(a)}) + arctan({P(b)}) = π/4.\n(b) Find the exact value of tan(arctan({P(a)}) + arctan({P(c)})).\n(c) Hence state whether arctan({P(a)}) + arctan({P(c)}) is less than or greater than π/2, giving a reason.',
              f'(a) tan of the sum = 1 and the sum lies in (0, π/2) (b) {P(tot)} (c) {"less than π/2" if tot > 0 else "greater than π/2"}',
              f'(a) Let A = arctan({P(a)}), B = arctan({P(b)}) M1; tan(A + B) = ({P(a + b)})/({P(1 - a * b)}) = 1 A1; A, B ∈ (0, π/4] so A + B ∈ (0, π/2) R1 AG. (b) ({P(a)} + {P(c)})/(1 − {P(a * c)}) M1 = {P(tot)} A1. (c) both angles in (0, π/2), so the sum is in (0, π); tan of it is {"positive" if tot > 0 else "negative"} R1, so the sum is {"less" if tot > 0 else "greater"} than π/2 A1.', 7)


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st4', F(
    terms=[('compound angle identity for sine', 'the identity sin(A ± B) = sin A cos B ± cos A sin B'),
           ('compound angle identity for cosine', 'the identity cos(A ± B) = cos A cos B ∓ sin A sin B (note the sign change)'),
           ('compound angle identity for tangent', 'the identity tan(A ± B) = (tan A ± tan B)/(1 ∓ tan A tan B)'),
           ('double angle identity for tangent', 'the identity tan 2θ = 2 tan θ/(1 − tan²θ), valid when tan²θ ≠ 1')],
    facts=[('Which of the following is equal to cos(A − B)?', 'cos A cos B + sin A sin B', ['cos A cos B − sin A sin B', 'cos A − cos B', 'sin A cos B − cos A sin B'], 'cos(A − B) = cos A cos B + sin A sin B: the sign inside is opposite.'),
           ('What is the exact value of sin 75°?', '(√6 + √2)/4', ['(√6 − √2)/4', '√3/2 + √2/2', '(√3 + 1)/2'], 'sin(45° + 30°) = (√2/2)(√3/2) + (√2/2)(1/2).'),
           ('What is the exact value of tan 15°?', '2 − √3', ['2 + √3', '√3 − 1', '1/√3'], 'tan(45° − 30°) = (1 − 1/√3)/(1 + 1/√3) = 2 − √3.'),
           ('For which value of θ is tan 2θ = 2 tan θ/(1 − tan²θ) not defined?', 'θ = π/4', ['θ = π/6', 'θ = 0', 'θ = π/3'], 'tan²(π/4) = 1 makes the denominator zero (2θ = π/2).')],
    why=[('Explain why sin(A + B) ≠ sin A + sin B in general.', 'Sine is not linear; e.g. A = B = π/2: sin π = 0 but sin(π/2) + sin(π/2) = 2. The correct expansion is sin A cos B + cos A sin B.'),
         ('Explain how the identity for sin 2θ follows from the compound angle identity.', 'Put B = A in sin(A + B) = sin A cos B + cos A sin B to get sin 2A = 2 sin A cos A.'),
         ('Explain how tan(A + B) is derived from the sine and cosine compound angle identities.', 'tan(A + B) = sin(A + B)/cos(A + B); divide numerator and denominator by cos A cos B to obtain (tan A + tan B)/(1 − tan A tan B).'),
         ('Explain why tan(θ + π/4) = (1 + tan θ)/(1 − tan θ).', 'Use tan(A + B) with B = π/4 and tan(π/4) = 1.')],
    misc=[('cos(A + B) = cos A cos B + sin A sin B.', 'The sign is reversed: cos(A + B) = cos A cos B − sin A sin B.'),
          ('tan(A + B) = tan A + tan B.', 'tan(A + B) = (tan A + tan B)/(1 − tan A tan B); e.g. A = B = π/4 gives tan(π/2) undefined, not 2.'),
          ('tan 2θ = 2 tan θ.', 'tan 2θ = 2 tan θ/(1 − tan²θ); for θ = π/6, tan(π/3) = √3 but 2 tan(π/6) = 2/√3.')],
))


def _std_pair(rng):
    pool = [pi / 6, pi / 4, pi / 3, pi / 2, 2 * pi / 3, 3 * pi / 4]
    while True:
        a, b = rng.sample(pool, 2)
        s_ = rng.choice([1, -1])
        tot = a + s_ * b
        if tot not in STD and float(tot) > 0:
            return a, b, s_, tot


@R.add('ch01-st4', 'C3', (1, 4), 'short', style='p1')
def compound_exact(rng, slot):
    a, b, s_, tot = _std_pair(rng)
    fn = rng.choice(['sin', 'cos', 'tan'] if slot.d >= 3 else ['sin', 'cos'])
    if fn == 'tan' and pi / 2 in (a, b):
        return None
    sa, ca, sb, cb = sp.sin(a), sp.cos(a), sp.sin(b), sp.cos(b)
    v = {'sin': sa * cb + s_ * ca * sb, 'cos': ca * cb - s_ * sa * sb,
         'tan': (sa / ca + s_ * sb / cb) / (1 - s_ * (sa / ca) * (sb / cb))}[fn]
    use_deg = rng.random() < 0.5
    ang = f'{deg(tot)}°' if use_deg else P(tot)
    hint = f'{deg(a)}° {"+" if s_ > 0 else "−"} {deg(b)}°' if use_deg else f'{P(a)} {"+" if s_ > 0 else "−"} {P(b)}'
    return mk(f'By writing {ang} as {hint}, find the exact value of {fn} {ang}.', nice(v),
              f'Correct compound angle identity for {fn} (M1); exact values of {fn}/{"cos" if fn != "cos" else "sin"} of the two angles substituted (A1); simplified: {nice(v)} (A1).', 3)


@R.add('ch01-st4', 'C3', (2, 4), 'short', style='p1')
def compound_triples(rng, slot):
    (a1, b1, c1), (a2, b2, c2) = rng.sample(PYTH[:5], 2)
    qa, qb = rng.choice([1, 2]), rng.choice([1, 4])
    sa, ca = sp.Rational(QSIGN[qa][1] * a1, c1), sp.Rational(QSIGN[qa][0] * b1, c1)
    sb, cb = sp.Rational(QSIGN[qb][1] * a2, c2), sp.Rational(QSIGN[qb][0] * b2, c2)
    want, val = rng.choice([('sin(A + B)', sa * cb + ca * sb), ('sin(A − B)', sa * cb - ca * sb),
                            ('cos(A + B)', ca * cb - sa * sb), ('cos(A − B)', ca * cb + sa * sb),
                            ('tan(A + B)', (sa / ca + sb / cb) / (1 - sa * sb / (ca * cb)))])
    if want.startswith('tan') and (1 - sa * sb / (ca * cb)) == 0:
        return None
    rA = f'0 < A < π/2' if qa == 1 else 'π/2 < A < π'
    rB = f'0 < B < π/2' if qb == 1 else '3π/2 < B < 2π'
    return mk(f'Angles A and B are such that sin A = {P(sa)} with {rA}, and cos B = {P(cb)} with {rB}. Find the exact value of {want}.', P(val),
              f'cos A = {P(ca)} (A1), sin B = {P(sb)} (A1) with correct signs; correct expansion of {want} (M1); {P(val)} (A1).', 4)


@R.add('ch01-st4', 'C3', (2, 4), 'short', style='p1')
def tan_double(rng, slot):
    p_, q_ = rng.choice([(1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (2, 5), (3, 2), (4, 3), (1, 5)])
    tv = sp.Rational(p_, q_) * rng.choice([1, -1])
    want = rng.choice(['tan 2θ', 'tan(θ + π/4)', 'tan(θ − π/4)'])
    val = {'tan 2θ': 2 * tv / (1 - tv ** 2), 'tan(θ + π/4)': (tv + 1) / (1 - tv), 'tan(θ − π/4)': (tv - 1) / (1 + tv)}[want]
    return mk(f'Given that tan θ = {P(tv)}, find the exact value of {want}.', P(val),
              f'Correct identity for {want} (M1); substitution of {P(tv)} (A1); {P(val)} (A1).', 3)


@R.add('ch01-st4', 'C1', (1, 3), 'mcq')
def compound_expand_mcq(rng, slot):
    a = rng.choice(['x', '2x', '3θ', 'θ'])
    b = rng.choice(['π/3', 'π/6', 'π/4', 'α'])
    kind = rng.choice(['sin+', 'sin-', 'cos+', 'cos-'])
    fn, sg = kind[:3], kind[3]
    if fn == 'sin':
        right = f'sin {a} cos {b} {"+" if sg == "+" else "−"} cos {a} sin {b}'
        wrong = [f'sin {a} cos {b} {"−" if sg == "+" else "+"} cos {a} sin {b}', f'sin {a} sin {b} {"+" if sg == "+" else "−"} cos {a} cos {b}', f'sin {a} {"+" if sg == "+" else "−"} sin {b}']
    else:
        right = f'cos {a} cos {b} {"−" if sg == "+" else "+"} sin {a} sin {b}'
        wrong = [f'cos {a} cos {b} {"+" if sg == "+" else "−"} sin {a} sin {b}', f'cos {a} sin {b} {"−" if sg == "+" else "+"} sin {a} cos {b}', f'cos {a} {"+" if sg == "+" else "−"} cos {b}']
    return mcq(rng, f'Which of the following is equal to {fn}({a} {"+" if sg == "+" else "−"} {b})?', right, wrong,
               f'Compound angle identity: {fn}({a} {sg} {b}) = {right}.')


@R.add('ch01-st4', 'C2', (2, 4), 'explain', style='p1')
def compound_show(rng, slot):
    c = rng.choice([pi / 6, pi / 4, pi / 3])
    fn = rng.choice(['sin', 'cos'])
    sg = rng.choice([1, -1])
    if fn == 'sin':
        cs_, cc_ = sp.cos(c), sg * sp.sin(c)
    else:
        cs_, cc_ = -sg * sp.sin(c), sp.cos(c)
    first, second = (('sin x', cs_), ('cos x', cc_)) if fn == 'sin' else (('cos x', cc_), ('sin x', cs_))
    e_txt = f'({P(first[1])}) {first[0]} {"+" if second[1] > 0 else "−"} ({P(abs(second[1]))}) {second[0]}'
    return mk(f'Show that {fn}(x {"+" if sg > 0 else "−"} {P(c)}) can be written as {e_txt}.', e_txt,
              f'Correct compound angle identity (M1); exact values cos({P(c)}) = {P(sp.cos(c))}, sin({P(c)}) = {P(sp.sin(c))} substituted (A1); result {e_txt} AG (A1).', 3, 'explain')


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def tan_sum_quarter(rng, slot):
    p_, q_ = rng.choice([(1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (1, 6), (2, 7), (3, 7), (1, 7), (3, 8)])
    ta = sp.Rational(p_, q_)
    tb = (1 - ta) / (1 + ta)
    t2a = 2 * ta / (1 - ta ** 2)
    return mk(f'The acute angles A and B satisfy tan A = {P(ta)} and tan B = {P(tb)}.\n(a) Show that tan(A + B) = 1.\n(b) Hence find the exact value of A + B, justifying your answer.\n(c) Find the exact value of tan 2A.\n(d) Find the exact value of tan(2A + B).',
              f'(a) ({P(ta)} + {P(tb)})/(1 − {P(ta * tb)}) = 1 (b) π/4 (c) {P(t2a)} (d) {P((t2a + tb) / (1 - t2a * tb))}',
              f'(a) tan(A + B) formula M1, numerator {P(ta + tb)} and denominator {P(1 - ta * tb)} A1, = 1 AG. (b) A, B acute so 0 < A + B < π R1; A + B = π/4 A1. (c) tan 2A = 2tan A/(1 − tan²A) M1 = {P(t2a)} A1. (d) 2A + B = A + π/4 so tan = (tan A + 1)/(1 − tan A) M1 = {P((ta + 1) / (1 - ta))} A1.', 8)


@R.add('ch01-st4', 'C4', (2, 4), 'multi_step', style='p1')
def triple_angle(rng, slot):
    sv = rng.choice([sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(3, 5), sp.Rational(1, 4), sp.Rational(4, 5), sp.Rational(3, 4), sp.Rational(2, 5)])
    s3v = 3 * sv - 4 * sv ** 3
    return mk(f'(a) By writing sin 3θ as sin(2θ + θ), show that sin 3θ ≡ 3 sin θ − 4 sin³θ.\n(b) Given that sin θ = {P(sv)}, find the exact value of sin 3θ.',
              f'(a) shown (b) {P(s3v)}',
              f'(a) sin 2θ cos θ + cos 2θ sin θ M1; 2 sin θ cos²θ + (1 − 2sin²θ) sin θ A1; cos²θ = 1 − sin²θ M1; simplifies to 3 sin θ − 4sin³θ AG. (b) 3({P(sv)}) − 4({P(sv)})³ M1 = {P(s3v)} A1.', 6)


@R.add('ch01-st4', 'C2', (2, 4), 'explain', style='p1')
def compound_error(rng, slot):
    a, b = rng.sample([pi / 6, pi / 4, pi / 3, pi / 2], 2)
    fn = rng.choice(['sin', 'cos', 'tan'])
    if fn == 'tan' and (pi / 2 in (a, b) or a + b == pi / 2):
        return None
    true = nice(sp.expand_trig(TRIG[fn](x + y)).subs({x: a, y: b}))
    wrong = nice(TRIG[fn](a) + TRIG[fn](b))
    nm = who(rng)
    return mk(f'{nm} says that {fn}({P(a)} + {P(b)}) = {fn}({P(a)}) + {fn}({P(b)}) = {wrong}. Explain the error and find the correct exact value of {fn}({P(a + b)}).',
              true, f'{fn} is not linear, so it does not distribute over addition (R1); correct compound angle identity (M1); exact substitution (A1); {fn}({P(a + b)}) = {true} (A1).', 4, 'explain', 'G2')


@R.add('ch01-st4', 'C2', (2, 4), 'explain')
def tan_double_undefined(rng, slot):
    a = rng.choice([pi / 4, 3 * pi / 4, 5 * pi / 4, 7 * pi / 4])
    b = rng.choice([pi / 6, pi / 3, pi / 8, 2 * pi / 3])
    kind = rng.choice([1, 2])
    if kind == 1:
        return mk(f'Explain why the formula tan 2θ = 2 tan θ/(1 − tan²θ) cannot be used when θ = {P(a)}, and state what happens to tan 2θ there.',
                  f'tan²({P(a)}) = 1 so the denominator is 0; 2θ = {P(2 * a)} where tan is undefined.',
                  f'tan({P(a)}) = {P(sp.tan(a))} so 1 − tan²θ = 0 (R1); 2θ = {P(2 * a)} is an odd multiple of π/2 (A1) where tan 2θ is undefined (R1).', 3, 'explain')
    tv = sp.tan(b)
    return mk(f'Explain how the double angle formula for tangent shows that tan({P(2 * b)}) = {P(sp.radsimp(2 * tv / (1 - tv ** 2)))}, starting from tan({P(b)}) = {P(tv)}.',
              P(sp.radsimp(2 * tv / (1 - tv ** 2))), f'Substitute tan θ = {P(tv)} (M1); 2({P(tv)})/(1 − {P(tv ** 2)}) (A1); simplify to {P(sp.radsimp(2 * tv / (1 - tv ** 2)))} (A1).', 3, 'explain')


# ---------------------------------------------------------------------------------------------
R.facts('ch01-st5', F(
    terms=[('odd function', 'a function with f(−x) = −f(x) for all x in its domain; its graph has rotational symmetry of order 2 about the origin (e.g. sin x, tan x)'),
           ('even function', 'a function with f(−x) = f(x) for all x in its domain; its graph is symmetric in the y-axis (e.g. cos x)'),
           ('periodic function', 'a function for which f(x + p) = f(x) for all x, for some smallest positive constant p, the period'),
           ('cofunction identity', 'an identity such as sin(π/2 − θ) = cos θ or cos(π/2 − θ) = sin θ relating complementary angles')],
    facts=[('Which identity shows that cosine is an even function?', 'cos(−θ) = cos θ', ['cos(π − θ) = −cos θ', 'cos(θ + 2π) = cos θ', 'cos(π/2 − θ) = sin θ'], 'Even means f(−θ) = f(θ).'),
           ('sin(π − θ) is equal to', 'sin θ', ['−sin θ', 'cos θ', '−cos θ'], 'Reflection in the y-axis of the unit circle keeps the y-coordinate.'),
           ('tan(π + θ) is equal to', 'tan θ', ['−tan θ', 'cot θ', '−cot θ'], 'tan has period π.'),
           ('cos(π + θ) is equal to', '−cos θ', ['cos θ', 'sin θ', '−sin θ'], 'A half-turn sends (x, y) to (−x, −y).'),
           ('The graph of y = sin x is symmetric about which vertical line?', 'x = π/2', ['x = π', 'x = 0', 'x = π/4'], 'sin(π/2 + h) = sin(π/2 − h) = cos h.')],
    why=[('Explain why sin(−θ) = −sin θ using the unit circle.', 'The angle −θ is the reflection of θ in the x-axis; reflection keeps x and changes the sign of y, so sin(−θ) = −sin θ.'),
         ('Explain why the graph of y = cos x is symmetric in the y-axis.', 'cos(−x) = cos x for all x (reflection in the x-axis keeps the x-coordinate on the unit circle), so cos is an even function and its graph is symmetric in the y-axis.'),
         ('Explain why tan x has period π while sin x and cos x have period 2π.', 'Adding π sends (cos x, sin x) to (−cos x, −sin x); both change sign, so their ratio tan x is unchanged, whereas sin and cos only repeat after a full turn 2π.'),
         ('Explain why the product of an odd function and an even function is odd.', 'If f is odd and g is even, (fg)(−x) = f(−x)g(−x) = −f(x)g(x) = −(fg)(x).')],
    misc=[('cos(π − θ) = cos θ.', 'Reflecting in the y-axis changes the sign of the x-coordinate: cos(π − θ) = −cos θ.'),
          ('sin x is an even function because sin(π − x) = sin x.', 'Even means f(−x) = f(x); sin(−x) = −sin x, so sine is odd. sin(π − x) = sin x describes symmetry about x = π/2, not the y-axis.'),
          ('x sin x is odd because sin x is odd.', 'x is odd and sin x is odd; (−x)sin(−x) = x sin x, so the product is even.')],
))

SYM_RULES = [('sin(−θ)', lambda s, c: -s, 'sin'), ('cos(−θ)', lambda s, c: c, 'cos'), ('sin(π − θ)', lambda s, c: s, 'sin'),
             ('cos(π − θ)', lambda s, c: -c, 'cos'), ('sin(π + θ)', lambda s, c: -s, 'sin'), ('cos(π + θ)', lambda s, c: -c, 'cos'),
             ('sin(2π − θ)', lambda s, c: -s, 'sin'), ('cos(2π − θ)', lambda s, c: c, 'cos'), ('sin(π/2 − θ)', lambda s, c: c, 'cos'),
             ('cos(π/2 − θ)', lambda s, c: s, 'sin'), ('sin(θ + π/2)', lambda s, c: c, 'cos'), ('cos(θ + π/2)', lambda s, c: -s, 'sin')]


@R.add('ch01-st5', 'C1', (1, 3), 'mcq')
def sym_mcq(rng, slot):
    a, b, c = rng.choice(PYTH)
    s_, c_ = sp.Rational(a, c), sp.Rational(b, c)
    nm, f_, base = rng.choice(SYM_RULES)
    v = f_(s_, c_)
    wr = [P(-v), P(s_ if base == 'cos' else c_), P(-(s_ if base == 'cos' else c_))]
    return mcq(rng, f'θ is acute with sin θ = {P(s_)} and cos θ = {P(c_)}. Write down the value of {nm}.', P(v), wr,
               f'Symmetry of the unit circle: {nm} = {"−" if v < 0 else ""}{base} θ = {P(v)}.')


@R.add('ch01-st5', 'C3', (1, 4), 'short')
def sym_decimal(rng, slot):
    kv = round(rng.uniform(0.1, 0.95), 2)
    fn = rng.choice(['sin', 'cos'])
    rules = [r for r in SYM_RULES if r[2] == fn]
    picks = rng.sample(rules, 2 if slot.d <= 2 else 3)
    parts, ans = [], []
    for nm, f_, base in picks:
        nm2 = nm.replace('θ', 'α')
        sgn = 1 if f_(1, 1) > 0 else -1
        parts.append(nm2)
        ans.append(f'{nm2} = {"−" if sgn < 0 else ""}{kv}')
    letters = 'abc'
    return mk(f'Given that {fn} α = {kv}, write down the value of ' + ', '.join(f'({letters[i]}) {p}' for i, p in enumerate(parts)) + '.',
              '; '.join(ans), 'A1 for each correct value, using the symmetries of the unit circle / graph: ' + '; '.join(ans) + '.', len(parts))


@R.add('ch01-st5', 'C4', (2, 5), 'multi_step')
def odd_even(rng, slot):
    funcs = [('x sin x', 'even'), ('x² tan x', 'odd'), ('sin x + cos x', 'neither'), ('x cos x', 'odd'), ('sin²x', 'even'),
             ('x³ cos x', 'odd'), ('cos x − x²', 'even'), ('sin x cos x', 'odd'), ('x + cos x', 'neither'), ('tan x sin x', 'even'),
             ('sin(x³)', 'odd'), ('cos(x²) + x⁴', 'even'), ('e^x sin x', 'neither'), ('sin x / x', 'even'), ('x² + sin x', 'neither')]
    (f1, a1), (f2, a2) = rng.sample(funcs, 2)
    return mk(f'For each function, determine whether it is odd, even or neither, justifying your answer algebraically: (a) f(x) = {f1} (b) g(x) = {f2}.',
              f'(a) {a1} (b) {a2}', f'For each: substitute −x (M1), use sin(−x) = −sin x, cos(−x) = cos x, tan(−x) = −tan x (A1), compare with f(x) and −f(x) and conclude (R1). (a) {a1} (b) {a2}. For "neither", a numerical counter-example (e.g. x = π/4) is required.', 6, gap='G5')


@R.add('ch01-st5', 'C2', (2, 4), 'explain')
def sym_explain(rng, slot):
    a = rng.choice([pi / 6, pi / 4, pi / 3, pi / 5, pi / 8, 2 * pi / 7])
    nm, f_, base = rng.choice(SYM_RULES)
    expr = nm.replace('θ', P(a))
    sgn = '−' if f_(1, 1) < 0 else ''
    return mk(f'Without evaluating either side, explain why {expr} = {sgn}{base}({P(a)}).', f'{expr} = {sgn}{base}({P(a)})',
              f'Locate the angle on the unit circle relative to {P(a)} (M1); the transformation (reflection/rotation) changes the coordinates as described (R1); hence {expr} = {sgn}{base}({P(a)}) (A1).', 3, 'explain')


@R.add('ch01-st5', 'C3', (2, 4), 'short')
def sym_sum_zero(rng, slot):
    n = rng.choice([6, 8, 12, 4, 10])
    fn = rng.choice(['sin', 'cos'])
    total = sum(TRIG[fn](2 * pi * k / n) for k in range(n))
    total = sp.nsimplify(sp.simplify(total))
    return mk(f'Use the symmetry of the unit circle to find the value of Σ (k = 0 to {n - 1}) {fn}(2πk/{n}).', P(total),
              f'The angles 2πk/{n} are equally spaced, so the points pair up symmetrically (opposite points for even {n}) (R1); contributions cancel (M1); sum = {P(total)} (A1).', 3)


# =============================================================================================
# ch02 Trigonometric graphs and equations
# =============================================================================================
def solve_basic(fn, kk, c, v, lo, hi):
    """Exact solutions of fn(kk·x + c) = v for x in [lo, hi] (fn in sin/cos/tan)."""
    v = sp.nsimplify(v)
    if fn in ('sin', 'cos') and abs(float(v)) > 1:
        return []
    if fn == 'sin':
        u0 = sp.asin(v)
        fams = [(u0, 2 * pi), (pi - u0, 2 * pi)]
    elif fn == 'cos':
        u0 = sp.acos(v)
        fams = [(u0, 2 * pi), (-u0, 2 * pi)]
    else:
        fams = [(sp.atan(v), pi)]
    out = {}
    flo, fhi, fk, fc = float(lo), float(hi), float(kk), float(c)
    for base, per in fams:
        fb, fp = float(base), float(per)
        for n in range(-30, 31):
            f = (fb + n * fp - fc) / fk
            if flo - 1e-9 <= f <= fhi + 1e-9:
                out[round(f, 9)] = sp.expand((base + n * per - c) / kk)
    return [out[k] for k in sorted(out)]


def lst(vals):
    return ', '.join(P(v_) for v_ in vals) if vals else 'no solutions'


def xs(vals, f=None):
    f = f or lst
    return ('x = ' + f(vals)) if vals else 'no solutions'


def lst3(vals):
    return ', '.join(s3(float(v_)) for v_ in vals) if vals else 'no solutions'


def _ang(kk, c):
    """text for kk·x + c"""
    e = kk * x + c
    return P(e)


R.facts('ch02-st1', F(
    terms=[('amplitude', 'half the distance between the maximum and minimum values of a sinusoidal function; for y = a sin(b(x − c)) + d it is |a|'),
           ('period', 'the horizontal length of one complete cycle; for y = a sin(b(x − c)) + d it is 2π/|b|'),
           ('principal axis', 'the horizontal line y = d about which a sinusoidal graph oscillates, midway between its maximum and minimum'),
           ('phase shift', 'the horizontal translation c in y = a sin(b(x − c)) + d'),
           ('sinusoidal model', 'a function of the form y = a sin(b(x − c)) + d or y = a cos(b(x − c)) + d used to model periodic behaviour')],
    facts=[('What is the period of y = 3 sin(4x) − 1?', 'π/2', ['4', '2π', '8π'], 'Period = 2π/4 = π/2.'),
           ('What is the range of y = 5 − 2cos x?', '3 ≤ y ≤ 7', ['−2 ≤ y ≤ 2', '5 ≤ y ≤ 7', '−7 ≤ y ≤ −3'], 'cos x ∈ [−1, 1] so 5 − 2cos x ∈ [3, 7].'),
           ('The graph of y = sin x is translated by the vector (π/4, 2). What is its new equation?', 'y = sin(x − π/4) + 2', ['y = sin(x + π/4) + 2', 'y = sin(x − π/4) − 2', 'y = 2 sin(x − π/4)'], 'A translation of p right replaces x by x − p; a translation of q up adds q.'),
           ('Which transformation maps y = cos x onto y = cos(3x)?', 'A horizontal stretch, scale factor 1/3', ['A horizontal stretch, scale factor 3', 'A vertical stretch, scale factor 3', 'A translation of 3 units left'], 'Replacing x by 3x compresses horizontally by factor 1/3.')],
    why=[('Explain why the period of y = sin(bx) is 2π/b for b > 0.', 'sin repeats when its argument increases by 2π; bx increases by 2π when x increases by 2π/b.'),
         ('Explain why y = cos x can be written as a sine function.', 'cos x = sin(x + π/2): the cosine graph is the sine graph translated π/2 to the left.'),
         ('Explain why the principal axis of a sinusoidal graph is midway between the maximum and minimum.', 'The function is d + a·(sine), and the sine part takes values symmetrically in [−1, 1], so values range from d − |a| to d + |a| with d in the middle.'),
         ('Explain why a negative value of a in y = a sin x reflects the graph in the x-axis.', 'Each y-value is multiplied by a negative number, so positive values become negative and vice versa, which is a reflection in the x-axis (combined with a stretch of |a|).')],
    misc=[('The period of y = sin(2x) is 4π because the 2 doubles the period.', 'Multiplying x by 2 halves the period: 2π/2 = π.'),
          ('y = sin(x + π/3) is sin x translated π/3 to the right.', 'Replacing x by x + π/3 translates π/3 to the LEFT.'),
          ('The amplitude of y = −4cos x + 1 is −4.', 'Amplitude is a distance, so it is |−4| = 4.')],
))


def _sinus_txt(a, fn, b, c, d):
    inner = P(b * (x - c)) if c != 0 else P(b * x)
    if b != 1 and c != 0:
        bt = P(b) if sp.nsimplify(b).is_Integer else f'({P(b)})'
        inner = f'{bt}(x {"−" if c > 0 else "+"} {P(abs(c))})'
    lead = '' if a == 1 else '−' if a == -1 else P(a)
    tail = '' if d == 0 else (f' + {P(d)}' if d > 0 else f' − {P(-d)}')
    return f'{lead}{fn}({inner}){tail}'


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def sinus_feature_mcq(rng, slot):
    a, b, d = nz(rng, -6, 6, (0, 1, -1)), rng.choice([2, 3, 4, sp.Rational(1, 2), sp.Rational(1, 3), pi / 6, pi / 12]), nz(rng, -5, 8)
    fn = rng.choice(['sin', 'cos'])
    c = rng.choice([0, pi / 4, pi / 3, 1, 2]) if slot.d >= 2 else 0
    f_txt = _sinus_txt(a, fn, b, c, d)
    what = rng.choice(['period', 'amplitude', 'range', 'principal axis'])
    per = sp.simplify(2 * pi / b)
    if what == 'period':
        right, wr = P(per), [P(b), P(2 * pi * b), P(pi / b)]
    elif what == 'amplitude':
        right, wr = str(abs(a)), [P(a) if a < 0 else P(-a), P(abs(a) + d), P(2 * abs(a)), P(abs(a) + 1)]
    elif what == 'range':
        right = f'{d - abs(a)} ≤ y ≤ {d + abs(a)}'.replace('-', '−')
        wr = [f'{-abs(a)} ≤ y ≤ {abs(a)}'.replace('-', '−'), f'{d} ≤ y ≤ {d + abs(a)}'.replace('-', '−'), f'{d - 2 * abs(a)} ≤ y ≤ {d + 2 * abs(a)}'.replace('-', '−')]
    else:
        right, wr = f'y = {d}'.replace('-', '−'), [f'y = {a}'.replace('-', '−'), f'y = {d + abs(a)}'.replace('-', '−'), f'y = {-d}'.replace('-', '−')]
    return mcq(rng, f'Consider f(x) = {f_txt}. What is the {what} of the graph of f?', right, wr,
               f'For a sin(b(x − c)) + d: amplitude |a| = {abs(a)}, period 2π/b = {P(per)}, principal axis y = {d}, range [{d - abs(a)}, {d + abs(a)}].')


@R.add('ch02-st1', 'C1', (1, 3), 'short')
def sinus_features_short(rng, slot):
    a, b, d = nz(rng, -7, 7, (0, 1, -1)), rng.choice([2, 3, 4, 5, sp.Rational(1, 2), pi / 4, pi / 6, pi / 12, pi / 3]), nz(rng, -6, 10)
    fn = rng.choice(['sin', 'cos'])
    f_txt = _sinus_txt(a, fn, b, 0, d)
    return mk(f'For the function g(x) = {f_txt}, write down (a) the amplitude (b) the period (c) the range.',
              f'(a) {abs(a)} (b) {P(sp.simplify(2 * pi / b))} (c) {d - abs(a)} ≤ g(x) ≤ {d + abs(a)}'.replace('-', '−'),
              f'(a) |a| = {abs(a)} A1 (b) 2π/{P(b)} = {P(sp.simplify(2 * pi / b))} A1 (c) [{d - abs(a)}, {d + abs(a)}] A1.', 3)


@R.add('ch02-st1', 'C3', (2, 4), 'short', style='p1')
def sinus_from_extrema(rng, slot):
    if rng.random() < 0.5:
        p_, half = rng.choice([1, 2, 3, 4]), rng.choice([2, 3, 4, 6, 5])
    else:
        p_, half = rng.choice([pi / 6, pi / 4, pi / 2, pi / 3, pi]), rng.choice([pi / 2, pi, pi / 3, pi / 4, pi / 6])
    q_, s_ = sorted(rng.sample(range(-4, 15), 2), reverse=True)
    if q_ == s_:
        return None
    r_ = p_ + half
    a = sp.Rational(q_ - s_, 2)
    d = sp.Rational(q_ + s_, 2)
    b = sp.simplify(pi / half)
    return mk(f'The graph of y = a cos(b(x − c)) + d, with a, b > 0 and the smallest possible c ≥ 0, has a maximum point at ({P(p_)}, {q_}) and the next minimum point at ({P(r_)}, {s_}). Find the values of a, b, c and d.'.replace('-', '−'),
              f'a = {P(a)}, b = {P(b)}, c = {P(p_)}, d = {P(d)}',
              f'a = ({q_} − ({s_}))/2 = {P(a)} A1; d = ({q_} + ({s_}))/2 = {P(d)} A1; period = 2 × {P(half)} = {P(2 * half)} (M1) so b = 2π/{P(2 * half)} = {P(b)} A1; cosine has its maximum where b(x − c) = 0, so c = {P(p_)} A1.', 5)


@R.add('ch02-st1', 'C3', (1, 4), 'short', style='p1')
def sinus_max_point(rng, slot):
    a, d = rng.randint(2, 8), nz(rng, -5, 9)
    b = rng.choice([2, 3, 4])
    c = rng.choice([pi / 6, pi / 4, pi / 3, pi / 12])
    fn = rng.choice(['sin', 'cos'])
    f_txt = _sinus_txt(a, fn, b, c, d)
    # first max for x >= 0
    base = c + (pi / (2 * b) if fn == 'sin' else 0)
    per = 2 * pi / b
    while float(base) < 0:
        base += per
    while float(base - per) >= 0:
        base -= per
    mn = base + per / 2
    while float(mn - per) >= 0:
        mn -= per
    return mk(f'Let f(x) = {f_txt}, x ≥ 0. Find the coordinates of the first maximum point and of the first minimum point of the graph of f.',
              f'maximum ({P(sp.simplify(base))}, {d + a}); minimum ({P(sp.simplify(mn))}, {d - a})'.replace('-', '−'),
              f'Max value {d} + {a} = {d + a}, min value {d - a} (A1 A1); {fn} is maximal when its argument is {"π/2" if fn == "sin" else "0"} (+2πn) (M1); x = {P(sp.simplify(base))} (A1); minimum half a period ({P(sp.simplify(per / 2))}) away: x = {P(sp.simplify(mn))} (A1).', 5)


@R.add('ch02-st1', 'C2', (2, 4), 'explain')
def sinus_transform_explain(rng, slot):
    a, b, d = rng.choice([2, 3, 4, sp.Rational(1, 2), -2, -3]), rng.choice([2, 3, 4, sp.Rational(1, 2), sp.Rational(1, 3)]), nz(rng, -4, 5)
    c = rng.choice([pi / 6, pi / 4, pi / 3, pi / 2])
    fn = rng.choice(['sin', 'cos'])
    f_txt = _sinus_txt(a, fn, b, c, d)
    steps = [f'horizontal stretch scale factor {P(1 / sp.nsimplify(b))} (period becomes {P(sp.simplify(2 * pi / b))})',
             f'translation of {P(c)} to the right', f'vertical stretch scale factor {P(abs(a))}' + (' and reflection in the x-axis' if a < 0 else ''),
             f'translation of {P(abs(d))} {"up" if d > 0 else "down"}']
    return mk(f'Describe a sequence of transformations that maps the graph of y = {fn} x onto the graph of y = {f_txt}, explaining the effect of each parameter.',
              '; '.join(steps), 'A1 for each correct transformation with its parameter (order: horizontal stretch before the horizontal translation of c, which is applied to x − c); R1 for explaining the effect on period/amplitude/axis. ' + '; '.join(steps), 4, 'explain')


@R.add('ch02-st1', 'C4', (3, 5), 'multi_step', style='ext')
def sinus_model_data(rng, slot):
    city = rng.choice(CITIES)
    hot_m = rng.choice([1, 7])
    Tmax, Tmin = rng.randint(24, 34), rng.randint(-4, 14)
    a, d = (Tmax - Tmin) / 2, (Tmax + Tmin) / 2
    b = 2 * math.pi / 12
    thr = rng.randint(int(d) - 3, int(d) + 4)
    T = lambda tt: a * math.cos(b * (tt - hot_m)) + d
    roots = nsols(lambda tt: T(tt) - thr, 0, 12)
    t1 = rng.choice([3.5, 4.5, 9.5, 10.5])
    if len(roots) != 2:
        return None
    above = 12 - (roots[1] - roots[0]) if T((roots[0] + roots[1]) / 2) < thr else roots[1] - roots[0]
    return mk(f'The mean monthly temperature T (°C) in {city} is modelled by T(t) = a cos(b(t − c)) + d, where t is the time in months after the start of the year (t = 1 is mid-January). The highest mean temperature, {Tmax} °C, occurs at t = {hot_m}; the lowest, {str(Tmin).replace("-", "−")} °C, occurs six months later.\n(a) Find the values of a, b, c and d (b > 0, a > 0).\n(b) Use the model to estimate T at t = {t1}.\n(c) Find the length of time in each year for which T > {thr} °C.\n(d) Comment on one limitation of the model.',
              f'(a) a = {fmt(a)}, b = π/6 ≈ 0.524, c = {hot_m}, d = {fmt(d)} (b) {s3(T(t1))} °C (c) {s3(above)} months (d) e.g. real temperatures are not exactly sinusoidal / vary year to year',
              f'(a) a = ({Tmax} − {Tmin})/2 A1, d = ({Tmax} + {Tmin})/2 A1, period 12 so b = 2π/12 (M1) A1, c = {hot_m} A1. (b) substitution (M1) {s3(T(t1))} A1. (c) solve T(t) = {thr} with GDC: t = {s3(roots[0])}, {s3(roots[1])} (A1); length {s3(above)} months A1. (d) R1 for a sensible limitation.', 10)


@R.add('ch02-st1', 'C3', (2, 4), 'short', style='p2')
def sinus_value_p2(rng, slot):
    a, d = round(rng.uniform(1.5, 6), 1), round(rng.uniform(2, 10), 1)
    b = rng.choice([0.5, 1.2, 1.5, 2, 2.5, 3])
    c = round(rng.uniform(0.2, 1.5), 1)
    fn = rng.choice(['sin', 'cos'])
    f = (lambda xx: a * math.sin(b * (xx - c)) + d) if fn == 'sin' else (lambda xx: a * math.cos(b * (xx - c)) + d)
    kv = round(rng.uniform(d - a * 0.8, d + a * 0.8), 1)
    per = 2 * math.pi / b
    roots = nsols(lambda xx: f(xx) - kv, 0, per)
    if not roots:
        return None
    return mk(f'Let h(x) = {a} {fn}({b}(x − {c})) + {d}. (a) Find the period of h. (b) Find the values of x in the interval 0 ≤ x ≤ {s3(per)} for which h(x) = {kv}.',
              f'(a) {s3(per)} (b) x = {lst3(roots)}', f'(a) 2π/{b} = {s3(per)} A1. (b) Graph/solver with h(x) = {kv} (M1); x = {lst3(roots)} A1 A1.', 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch02-st2', F(
    terms=[('principal value', 'the single solution of a trigonometric equation returned by the inverse function (arcsin, arccos, arctan), lying in its restricted range'),
           ('general solution', 'the set of all solutions of a trigonometric equation, e.g. x = π/6 + 2πn or x = 5π/6 + 2πn for sin x = 1/2'),
           ('quadratic in sin x', 'an equation such as 2sin²x − sin x − 1 = 0 that becomes a quadratic when sin x is replaced by a single variable')],
    facts=[('How many solutions does sin x = 0.4 have for 0 ≤ x ≤ 2π?', '2', ['1', '3', '4'], 'The line y = 0.4 meets one full cycle of y = sin x twice.'),
           ('How many solutions does cos(3x) = 0.5 have for 0 ≤ x ≤ 2π?', '6', ['2', '3', '4'], 'cos 3x completes 3 cycles in [0, 2π], with 2 solutions per cycle.'),
           ('Which equation has no real solutions?', '2 sin x = 3', ['tan x = 5', '3 cos x = 2', 'sin x = −1'], 'sin x = 1.5 is impossible since −1 ≤ sin x ≤ 1.'),
           ('Solving sin x cos x = cos x by dividing by cos x loses the solutions where', 'cos x = 0', ['sin x = 0', 'sin x = 1', 'tan x = 1'], 'Factorise instead: cos x (sin x − 1) = 0.')],
    why=[('Explain why the equation sin(2x) = k for 0 < k < 1 has four solutions in [0, 2π].', 'As x runs over [0, 2π], 2x runs over [0, 4π], two full cycles of sine; each cycle meets the horizontal line y = k twice.'),
         ('Explain why it is better to factorise than to divide by sin x when solving sin²x = sin x.', 'Dividing by sin x assumes sin x ≠ 0 and loses the solutions sin x = 0; factorising sin x (sin x − 1) = 0 keeps both cases.'),
         ('Explain why you must adjust the interval when solving sin(3x) = 1/2 for 0 ≤ x ≤ π.', 'Substituting u = 3x, the interval for u becomes 0 ≤ u ≤ 3π; all u-solutions in that interval are needed before dividing by 3.'),
         ('Explain why squaring both sides of a trigonometric equation can introduce extra solutions.', 'Squaring cannot distinguish a = b from a = −b, so solutions of the squared equation must be checked in the original.')],
    misc=[('cos x = −0.5 has no solutions because cosine is never negative.', 'Cosine is negative in quadrants 2 and 3: x = 2π/3 and 4π/3 on [0, 2π].'),
          ('The solutions of tan x = 1 on [0, 2π] are π/4 and 3π/4.', 'tan has period π: x = π/4 and 5π/4. tan(3π/4) = −1.'),
          ('2sin²x = sin x gives sin x = 1/2, so x = π/6, 5π/6 only on [0, 2π].', 'Dividing by sin x lost sin x = 0: also x = 0, π, 2π.')],
))

BASIC_V = {'sin': [sp.Rational(1, 2), r2 / 2, r3 / 2, -sp.Rational(1, 2), -r2 / 2, -r3 / 2, sp.Integer(1), sp.Integer(-1), sp.Integer(0)],
           'cos': [sp.Rational(1, 2), r2 / 2, r3 / 2, -sp.Rational(1, 2), -r2 / 2, -r3 / 2, sp.Integer(1), sp.Integer(-1), sp.Integer(0)],
           'tan': [sp.Integer(1), sp.Integer(-1), r3, -r3, r3 / 3, -r3 / 3, sp.Integer(0)]}
INTERVALS = [(0, 2 * pi, '0 ≤ x ≤ 2π'), (0, pi, '0 ≤ x ≤ π'), (-pi, pi, '−π ≤ x ≤ π'), (0, 3 * pi, '0 ≤ x ≤ 3π'), (-pi / 2, 3 * pi / 2, '−π/2 ≤ x ≤ 3π/2')]


@R.add('ch02-st2', 'C1', (1, 3), 'short', style='p1')
def trig_eq_basic(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    v = rng.choice(BASIC_V[fn])
    lo, hi, itxt = rng.choice(INTERVALS[:3] if slot.d <= 2 else INTERVALS)
    sols = solve_basic(fn, 1, 0, v, lo, hi)
    return mk(f'Solve {fn} x = {P(v)} for {itxt}.', xs(sols),
              f'Principal value {P({"sin": sp.asin, "cos": sp.acos, "tan": sp.atan}[fn](v))} (A1); use symmetry/period to find all solutions in the interval (M1); x = {lst(sols)} (A1).', 2 if len(sols) <= 2 else 3)


@R.add('ch02-st2', 'C1', (1, 3), 'mcq')
def trig_eq_count_mcq(rng, slot):
    fn = rng.choice(['sin', 'cos'])
    kk = rng.choice([1, 2, 3, 4])
    v = rng.choice([sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(-3, 4), sp.Rational(1, 2), sp.Rational(-1, 5), sp.Rational(7, 10)])
    lo, hi, itxt = rng.choice(INTERVALS[:2])
    n_ = len(solve_basic(fn, kk, 0, v, lo, hi))
    wr = [str(n_ + 1), str(max(n_ - 1, 0)), str(2 * n_ if n_ else 2), str(kk), str(n_ // 2 if n_ > 1 else 3)]
    return mcq(rng, f'How many solutions does {fn}({kk if kk > 1 else ""}x) = {P(v)} have in the interval {itxt}?', str(n_), wr,
               f'{fn}({kk}x) completes {kk}{"" if hi == 2 * pi else "/2"} cycle(s) on the interval; each full cycle gives 2 solutions; count = {n_}.')


@R.add('ch02-st2', 'C3', (1, 4), 'short', style='p1')
def trig_eq_multiple(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    kk = rng.choice([2, 3]) if slot.d >= 2 else 2
    c = rng.choice([0, 0, pi / 6, -pi / 3, pi / 4, -pi / 4]) if slot.d >= 3 else 0
    v = rng.choice([w for w in BASIC_V[fn] if w not in (0,)])
    lo, hi, itxt = rng.choice(INTERVALS[:3])
    sols = solve_basic(fn, kk, c, v, lo, hi)
    if not sols or len(sols) > 8:
        return None
    lead = rng.choice([1, 2]) if fn != 'tan' else 1
    rhs = P(lead * v)
    lhs = f'{"2" if lead == 2 else ""}{fn}({_ang(kk, c)})'
    if fn == 'tan' and rng.random() < 0.4 and v != 0:
        lhs, rhs = f'{fn}({_ang(kk, c)}) {"+" if v < 0 else "−"} {P(abs(v))}', '0'
    return mk(f'Solve {lhs} = {rhs} for {itxt}.', xs(sols),
              f'{fn}(u) = {P(v)} with u = {_ang(kk, c)} (M1); interval for u adjusted (M1); u values (A1); x = {lst(sols)} (A1 A1). Award A1 only for a complete list with no extra values.', 5 if slot.d >= 3 else 4)


def _quad_roots(rng, fn):
    if fn == 'tan':
        cands = [sp.Integer(1), sp.Integer(-1), sp.Integer(0), r3, -r3]
        r1, r2_ = rng.sample(cands[:3], 2)
        return r1, r2_
    cands = [sp.Rational(1, 2), -sp.Rational(1, 2), sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(2), sp.Integer(-2), sp.Rational(3, 2), sp.Integer(3)]
    r1 = rng.choice(cands[:5])
    r2_ = rng.choice([c for c in cands if c != r1])
    return r1, r2_


def _poly_in(fn, coeffs):
    a, b, c = coeffs
    s = ''
    for coef, term in ((a, f'{fn}²x'), (b, f'{fn} x'), (c, '')):
        if coef == 0:
            continue
        mag = abs(coef)
        body = (P(mag) if (mag != 1 or term == '') else '') + term
        if not s:
            s = ('−' if coef < 0 else '') + body
        else:
            s += (' − ' if coef < 0 else ' + ') + body
    return s


@R.add('ch02-st2', 'C3', (2, 5), 'short', style='p1')
def trig_eq_quadratic(rng, slot):
    fn = rng.choice(['sin', 'cos', 'tan'])
    r1, r2_ = _quad_roots(rng, fn)
    den = sp.ilcm(sp.fraction(r1)[1], sp.fraction(r2_)[1])
    A, B, C = den, -den * (r1 + r2_), den * r1 * r2_
    if not all(sp.nsimplify(z).is_Integer for z in (A, B, C)):
        return None
    lo, hi, itxt = rng.choice(INTERVALS[:3])
    sols = sorted(solve_basic(fn, 1, 0, r1, lo, hi) + solve_basic(fn, 1, 0, r2_, lo, hi), key=float)
    out = {}
    for z in sols:
        out[round(float(z), 9)] = z
    sols = [out[k] for k in sorted(out)]
    rej = [r for r in (r1, r2_) if fn != 'tan' and abs(r) > 1]
    return mk(f'Solve {_poly_in(fn, (A, B, C))} = 0 for {itxt}.', xs(sols),
              f'Factorise as a quadratic in {fn} x (M1): {fn} x = {P(r1)} or {fn} x = {P(r2_)} (A1)' + (f'; reject {fn} x = {", ".join(P(r) for r in rej)} since |{fn} x| ≤ 1 (R1)' if rej else '') + f'; x = {lst(sols)} (A1 A1).', 5)


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step', style='ext')
def trig_eq_identity(rng, slot):
    kind = rng.choice(['cos2_sin', 'cos2_cos', 'sin2', 'sec_tan'])
    lo, hi, itxt = rng.choice(INTERVALS[:3])
    if kind in ('cos2_sin', 'cos2_cos'):
        fn = 'sin' if kind == 'cos2_sin' else 'cos'
        r1, r2_ = _quad_roots(rng, fn)
        # 2s² − 2(r1+r2)s + 2r1r2 = 0 ; for sin use 2s² = 1 − cos2x ; for cos use 2c² = 1 + cos2x
        p_, q_ = -2 * (r1 + r2_), 2 * r1 * r2_
        if not (p_.is_Integer and q_.is_Integer):
            return None
        if fn == 'sin':
            # 1 − cos2x + p sin x + q = 0  ->  cos 2x − p sin x = 1 + q
            lhs = f'cos 2x {"−" if p_ > 0 else "+"} {P(abs(p_)) if abs(p_) != 1 else ""}sin x' if p_ != 0 else 'cos 2x'
            rhs = 1 + q_
            ident = 'cos 2x = 1 − 2sin²x'
        else:
            # 1 + cos2x + p cos x + q = 0 -> cos 2x + p cos x = −1 − q
            lhs = f'cos 2x {"+" if p_ > 0 else "−"} {P(abs(p_)) if abs(p_) != 1 else ""}cos x' if p_ != 0 else 'cos 2x'
            rhs = -1 - q_
            ident = 'cos 2x = 2cos²x − 1'
        quad = _poly_in(fn, (2, p_, q_))
    elif kind == 'sin2':
        fn = 'cos'
        r1, r2_ = sp.Integer(0), rng.choice([sp.Rational(1, 2), -sp.Rational(1, 2), r3 / 2, r2 / 2])
        # sin 2x = 2 r2 sin x? -> 2 sin x cos x − 2 r2 sin x = 0 -> sin x (cos x − r2) = 0
        lhs, rhs = f'sin 2x', f'{P(2 * r2_)} sin x'
        ident = 'sin 2x = 2 sin x cos x'
        quad = f'2 sin x (cos x − ({P(r2_)})) = 0'
        sols = sorted(solve_basic('sin', 1, 0, 0, lo, hi) + solve_basic('cos', 1, 0, r2_, lo, hi), key=float)
    else:
        fn = 'tan'
        r1, r2_ = _quad_roots(rng, 'tan')
        # sec²x = 1 + tan²x : tan² − (r1+r2) tan + r1r2 = 0 -> sec²x − (r1+r2)tan x + r1r2 − 1 = 0
        p_, q_ = -(r1 + r2_), r1 * r2_ - 1
        lhs = 'sec²x' + (f' {"−" if p_ < 0 else "+"} {P(abs(p_)) if abs(p_) != 1 else ""}tan x' if p_ != 0 else '') + (f' {"−" if q_ < 0 else "+"} {P(abs(q_))}' if q_ != 0 else '')
        rhs = 0
        ident = 'sec²x = 1 + tan²x'
        quad = _poly_in('tan', (1, p_, r1 * r2_))
    if kind != 'sin2':
        sols = sorted(solve_basic(fn, 1, 0, r1, lo, hi) + solve_basic(fn, 1, 0, r2_, lo, hi), key=float)
    out = {}
    for z in sols:
        out[round(float(z), 9)] = z
    sols = [out[k] for k in sorted(out)]
    # numerical check of every solution
    fx = sp.lambdify(x, sp.sympify(0))
    return mk(f'(a) Show that the equation {lhs} = {P(rhs)} can be written as {quad} = 0.\n(b) Hence solve {lhs} = {P(rhs)} for {itxt}.'.replace('= 0 = 0', '= 0'),
              f'(b) x = {lst(sols)}',
              f'(a) Use {ident} (M1); rearrange and simplify to {quad} = 0 (A1) AG. (b) Factorise (M1): {fn} x = {P(r1)} or {P(r2_)} (A1); reject any value outside [−1, 1] (R1); x = {lst(sols)} (A1 A1 A1).', 8)


@R.add('ch02-st2', 'C3', (2, 4), 'short', style='p2')
def trig_eq_gdc(rng, slot):
    a, b = rng.randint(2, 6), rng.choice([1, 2, 3])
    c = round(rng.uniform(-0.9, 0.9) * a, 1)
    fn = rng.choice(['sin', 'cos'])
    lo, hi, itxt = rng.choice([(0, 2 * math.pi, '0 ≤ x ≤ 2π'), (0, math.pi, '0 ≤ x ≤ π'), (0, 6, '0 ≤ x ≤ 6'), (-math.pi, math.pi, '−π ≤ x ≤ π')])
    f = lambda xx: a * getattr(math, fn)(b * xx) - c
    roots = nsols(f, lo, hi)
    if not roots or abs(c) < 0.05:
        return None
    return mk(f'Solve {a} {fn}({b if b > 1 else ""}x) = {c} for {itxt}, giving your answers to 3 significant figures.'.replace('-', '−').replace('2π', '2π'),
              xs(roots, lst3), f'{fn}({b}x) = {c}/{a} (M1); principal value {"arcsin" if fn == "sin" else "arccos"}({s3(c / a)}) (A1) or GDC graph; all solutions: {lst3(roots)} (A1 A1).', 4)


@R.add('ch02-st2', 'C2', (2, 4), 'explain', style='p1')
def trig_eq_lost(rng, slot):
    fn = rng.choice(['sin', 'cos'])
    v = rng.choice([sp.Rational(1, 2), r3 / 2, r2 / 2, -sp.Rational(1, 2)])
    lo, hi, itxt = INTERVALS[0]
    zero = solve_basic(fn, 1, 0, 0, lo, hi)
    other = solve_basic('cos' if fn == 'sin' else 'sin', 1, 0, v, lo, hi)
    allv = sorted(zero + other, key=float)
    nm = who(rng)
    g = 'cos' if fn == 'sin' else 'sin'
    return mk(f'{nm} solves {fn} x {g} x = ({P(v)}) {fn} x for {itxt} by dividing both sides by {fn} x, and obtains x = {lst(other)}. Explain why this is incomplete and give the complete solution set.',
              xs(allv), f'Dividing by {fn} x assumes {fn} x ≠ 0 (R1); factorise: {fn} x ({g} x − ({P(v)})) = 0 (M1); {fn} x = 0 gives x = {lst(zero)} (A1); complete set {lst(allv)} (A1).', 4, 'explain', 'G2')


@R.add('ch02-st2', 'C2', (2, 4), 'explain')
def trig_eq_nosol(rng, slot):
    fn = rng.choice(['sin', 'cos'])
    a = rng.randint(2, 6)
    c = rng.choice([a + 1, a + 2, -(a + 1), a + 3])
    d = rng.randint(1, 4)
    kind = rng.choice([1, 2])
    if kind == 1:
        return mk(f'Explain why the equation {a} {fn} x = {c} has no real solutions.'.replace('-', '−'), f'{fn} x = {P(sp.Rational(c, a))}, which is outside [−1, 1].',
                  f'Rearranging gives {fn} x = {P(sp.Rational(c, a))} (A1); |{fn} x| ≤ 1 for all real x (R1), so no solutions (R1).', 3, 'explain')
    return mk(f'Explain why the equation {fn}²x + {d if d > 1 else ""}{fn} x + {d + 2} = 0 has no real solutions.', 'The discriminant is negative (or roots outside [−1, 1]).',
              f'As a quadratic in {fn} x: discriminant {d}² − 4({d + 2}) = {d * d - 4 * (d + 2)} < 0 (M1 A1), so there is no real value of {fn} x and hence no solution (R1).', 3, 'explain')


# ---------------------------------------------------------------------------------------------
R.facts('ch02-st3', F(
    terms=[('periodic model', 'a function that repeats at regular intervals, used for phenomena such as tides, daylight hours and rotating wheels'),
           ('angular frequency b', 'the constant b in a sin(b(t − c)) + d, related to the period T by b = 2π/T')],
    facts=[('A Ferris wheel completes one revolution every 30 minutes. In h(t) = d − a cos(bt), t in minutes, what is b?', 'π/15', ['30', 'π/30', '2π'], 'b = 2π/30 = π/15.'),
           ('High tide is 6.2 m and low tide is 1.4 m. What is the amplitude of a sinusoidal tide model?', '2.4 m', ['4.8 m', '3.8 m', '7.6 m'], '(6.2 − 1.4)/2 = 2.4.'),
           ('Hours of daylight are modelled with a period of', '365 days (one year)', ['24 hours', '30 days', '12 months of 28 days'], 'The seasonal cycle repeats annually.')],
    why=[('Explain why h(t) = d − a cos(bt) is a natural model for the height of a seat on a Ferris wheel that starts at the bottom.', 'At t = 0, cos 0 = 1 so h = d − a, the lowest point; as the wheel turns the height oscillates sinusoidally about the axle height d with amplitude equal to the radius a.'),
         ('Explain what the constant d represents in a tide model D(t) = a sin(bt) + d.', 'd is the mean water depth, midway between high and low tide (the principal axis).'),
         ('Explain why a sinusoidal model of daylight hours might be less accurate near the poles.', 'Near the poles there are periods of 24-hour daylight or darkness, so daylight is capped at 0 and 24 hours and the curve is flattened rather than sinusoidal.')],
    misc=[('If high tide is at 02:00 and the next low tide at 08:15, the period is 6.25 hours.', 'High to low is half a cycle, so the period is 12.5 hours.'),
          ('The amplitude of a Ferris wheel model equals its diameter.', 'The height varies by the radius above and below the axle, so the amplitude is the radius.')],
))


@R.add('ch02-st3', 'C3', (2, 5), 'short', style='p2')
def ferris(rng, slot):
    rad = rng.randint(8, 60)
    axle = rad + rng.randint(1, 6)
    per = rng.choice([10, 12, 15, 20, 24, 30, 32])
    b = 2 * math.pi / per
    h = lambda tt: axle - rad * math.cos(b * tt)
    hk = rng.randint(axle - rad + 2, axle + rad - 2)
    roots = nsols(lambda tt: h(tt) - hk, 0, per)
    if len(roots) != 2:
        return None
    t1 = round(rng.uniform(1, per - 1), 1)
    nm = who(rng)
    frame = rng.choice([f'{nm} boards a Ferris wheel of radius {rad} m at its lowest point, {axle - rad} m above the ground. The wheel rotates once every {per} minutes.',
                        f'A Ferris wheel in {rng.choice(CITIES)} has its axle {axle} m above the ground and a radius of {rad} m; one revolution takes {per} minutes. A passenger joins at the lowest point at t = 0.'])
    return mk(f'{frame} The height is h(t) = {axle} − {rad} cos({P(2 * pi * t / per)}) metres, t in minutes. (a) Find the height after {t1} minutes. (b) Find the length of time during one revolution for which the passenger is more than {hk} m above the ground.',
              f'(a) {s3(h(t1))} m (b) {s3(roots[1] - roots[0])} minutes', f'(a) substitution (M1) {s3(h(t1))} m (A1). (b) solve h(t) = {hk}: t = {s3(roots[0])}, {s3(roots[1])} (M1 A1); time = {s3(roots[1] - roots[0])} min (A1).', 5)


@R.add('ch02-st3', 'C3', (2, 4), 'short', style='p2')
def tides(rng, slot):
    hi_, lo_ = round(rng.uniform(4, 9), 1), round(rng.uniform(0.5, 3), 1)
    t_hi = round(rng.uniform(1, 5), 2)
    per = rng.choice([12.4, 12.5, 12.4])
    a, d = (hi_ - lo_) / 2, (hi_ + lo_) / 2
    b = 2 * math.pi / per
    D = lambda tt: a * math.cos(b * (tt - t_hi)) + d
    need = round(rng.uniform(lo_ + 0.5, hi_ - 0.5), 1)
    roots = nsols(lambda tt: D(tt) - need, 0, per)
    city = rng.choice(['Lisbon', 'Cape Town', 'Melbourne', 'Kuala Lumpur', 'Dubai', 'Lima', 'Oslo', 'Mumbai'])
    if len(roots) != 2:
        return None
    above = roots[1] - roots[0] if D((roots[0] + roots[1]) / 2) > need else per - (roots[1] - roots[0])
    return mk(f'The depth of water in the harbour at {city} is modelled by D(t) = {fmt(a, 3)} cos(2π(t − {t_hi})/{per}) + {fmt(d, 3)} metres, t hours after midnight. A ship needs at least {need} m of water. (a) Write down the depth at high tide. (b) Find the total time in the first {per} hours for which the ship can safely enter the harbour.',
              f'(a) {s3(a + d)} m (b) {s3(above)} hours', f'(a) a + d = {s3(a + d)} (A1). (b) solve D(t) = {need} (M1): t = {lst3(roots)} (A1 A1); time with D ≥ {need}: {s3(above)} h (A1).', 5)


@R.add('ch02-st3', 'C4', (3, 5), 'multi_step', style='ext')
def daylight(rng, slot):
    city = rng.choice(['Oslo', 'Toronto', 'Vienna', 'Seoul', 'Melbourne', 'Cape Town', 'Lisbon', 'Geneva'])
    longest, shortest = round(rng.uniform(14, 19), 1), round(rng.uniform(6, 10), 1)
    south = city in ('Melbourne', 'Cape Town')
    peak = 355 if south else 172
    a, d = (longest - shortest) / 2, (longest + shortest) / 2
    b = 2 * math.pi / 365
    L = lambda n: a * math.cos(b * (n - peak)) + d
    thr = rng.choice([10, 11, 12, 13, 14])
    if not (shortest < thr < longest):
        return None
    roots = nsols(lambda n: L(n) - thr, 0, 365)
    if len(roots) != 2:
        return None
    above = roots[1] - roots[0] if L((roots[0] + roots[1]) / 2) > thr else 365 - (roots[1] - roots[0])
    day = rng.randint(20, 340)
    return mk(f'In {city} the longest day has {longest} hours of daylight (day {peak} of the year) and the shortest has {shortest} hours, half a year later. The number of hours of daylight, L, on day n is modelled by L(n) = a cos(b(n − c)) + d.\n(a) Find the values of a, b, c and d.\n(b) Estimate the daylight on day {day}.\n(c) Find the number of days in the year on which there are more than {thr} hours of daylight.\n(d) Find the rate of change of L on day {day}, and interpret its sign.',
              f'(a) a = {s3(a)}, b = 2π/365 ≈ 0.0172, c = {peak}, d = {s3(d)} (b) {s3(L(day))} h (c) {s3(above)} days (about {round(above)}) (d) {s3(-a * b * math.sin(b * (day - peak)))} h per day',
              f'(a) A1 A1 (M1)A1 A1. (b) {s3(L(day))} A1. (c) solve L(n) = {thr}: n = {lst3(roots)} (M1 A1); {s3(above)} days A1. (d) L′(n) = −ab sin(b(n − c)) (M1) = {s3(-a * b * math.sin(b * (day - peak)))} (A1); {"days are lengthening" if -a * b * math.sin(b * (day - peak)) > 0 else "days are shortening"} (R1).', 12)


@R.add('ch02-st3', 'C2', (2, 4), 'explain')
def model_interpret(rng, slot):
    a, d = rng.randint(2, 9), rng.randint(10, 30)
    per = rng.choice([6, 8, 10, 12, 24])
    ctx = rng.choice([('the temperature (°C) inside a greenhouse', 'hours after midnight'), ('the height (m) of a point on a wind-turbine blade', 'seconds'),
                      ('the number of visitors (hundreds) to a ski resort', 'weeks after 1 January'), ('the depth (m) of a tidal estuary', 'hours after noon')])
    return mk(f'The function f(t) = {a} sin((2π/{per})t) + {d} models {ctx[0]}, where t is measured in {ctx[1]}. Explain the meaning of each of the numbers {a}, {per} and {d} in this context.',
              f'{a}: amplitude (maximum variation from the mean); {per}: period (one full cycle takes {per} units of t); {d}: mean / principal axis value.',
              f'Amplitude {a}: the quantity rises and falls {a} above and below its mean (R1); period {per}: the pattern repeats every {per} {ctx[1].split()[0]} (R1); {d}: the mean level, midway between max {a + d} and min {d - a} (R1).', 3, 'explain')


@R.add('ch02-st3', 'C1', (1, 3), 'mcq')
def model_param_mcq(rng, slot):
    per = rng.choice([4, 6, 8, 10, 12, 20, 24, 40, 60])
    b = sp.Rational(2, per) * pi
    ctx = rng.choice(['a pendulum', 'a Ferris wheel', 'a tide', 'a spring', 'a heartbeat sensor', 'a lighthouse beam'])
    return mcq(rng, f'The motion of {ctx} is modelled by y = a sin(bt) + d with a period of {per} seconds. What is the value of b?', P(b),
               [str(per), P(sp.Rational(1, per)), P(pi * per / 2), P(per * pi)], f'b = 2π/period = 2π/{per} = {P(b)}.')


@R.add('ch02-st3', 'C3', (1, 3), 'short', style='p1')
def model_build(rng, slot):
    mx, mn = rng.randint(12, 40), rng.randint(2, 11)
    per = rng.choice([4, 6, 8, 12, 24])
    ctx = rng.choice(['A buoy bobs on the sea', 'The temperature in a cold-storage room cycles', 'A piston moves up and down', 'The water level in a lock varies'])
    a, d = sp.Rational(mx - mn, 2), sp.Rational(mx + mn, 2)
    return mk(f'{ctx} between a maximum of {mx} and a minimum of {mn} units, with period {per} minutes, and is at its maximum at t = 0. Write down a model of the form y = a cos(bt) + d.',
              f'y = {P(a)} cos({P(sp.Rational(2, per) * pi)}t) + {P(d)}', f'a = {P(a)} (A1); b = 2π/{per} = {P(sp.Rational(2, per) * pi)} (A1); d = {P(d)} (A1).', 3)


# =============================================================================================
# ch03 Vectors
# =============================================================================================
def rv(rng, lo=-6, hi=6, n=3, nonzero=True):
    while True:
        v = [rng.randint(lo, hi) for _ in range(n)]
        if not nonzero or any(v):
            return sp.Matrix(v)


def V(v):
    """column vector shown inline"""
    return '(' + ', '.join(P(c) for c in v) + ')'


def pt(v):
    return '(' + ', '.join(P(c) for c in v) + ')'


def gcdv(vals):
    g = 0
    for c in vals:
        g = math.gcd(g, int(c))
    return g or 1


def mag(v):
    return sp.sqrt(sum(c ** 2 for c in v))


def dot(a, b):
    return sum(p_ * q_ for p_, q_ in zip(a, b))


def crossv(a, b):
    return sp.Matrix(a).cross(sp.Matrix(b))


def deg_of(cosv):
    return math.degrees(math.acos(max(-1, min(1, float(cosv)))))


R.facts('ch03-st1', F(
    terms=[('position vector', 'the vector from the origin O to a point; the position vector of A is OA, often written a'),
           ('unit vector', 'a vector of magnitude 1; the unit vector in the direction of v is v/|v|'),
           ('magnitude of a vector', 'its length; for v = (v₁, v₂, v₃), |v| = √(v₁² + v₂² + v₃²)'),
           ('displacement vector AB', 'the vector from A to B, given by b − a'),
           ('parallel vectors', 'non-zero vectors that are scalar multiples of each other, u = kv for some real k ≠ 0')],
    facts=[('If a = 2i − j + 3k, what is |a|?', '√14', ['14', '4', '√12'], '√(4 + 1 + 9) = √14.'),
           ('Which vector is parallel to (2, −1, 4)?', '(−6, 3, −12)', ['(6, 3, 12)', '(2, 1, 4)', '(−2, −1, −4)'], '(−6, 3, −12) = −3(2, −1, 4).'),
           ('The points A and B have position vectors a and b. What is the position vector of the midpoint of AB?', '(a + b)/2', ['(b − a)/2', 'b − a', 'a + b'], 'OM = a + ½(b − a) = ½(a + b).'),
           ('Which of the following is a unit vector?', '(3/5, 0, −4/5)', ['(1, 1, 0)', '(1/2, 1/2, 1/2)', '(3, 0, −4)'], '(3/5)² + (4/5)² = 1.')],
    why=[('Explain why AB = b − a.', 'Travel from A back to O and then from O to B: AB = AO + OB = −a + b.'),
         ('Explain why multiplying a vector by a negative scalar reverses its direction.', 'kv has components k times those of v; for k < 0 every component changes sign, so the vector points the opposite way with length |k||v|.'),
         ('Explain why two vectors with equal magnitudes need not be equal.', 'Equality needs the same magnitude AND the same direction, e.g. (3, 4, 0) and (0, 0, 5) both have length 5 but are different vectors.'),
         ('Explain how to tell from components whether two vectors are parallel.', 'They are parallel exactly when one is a scalar multiple of the other, i.e. the ratios of corresponding components are all equal (allowing for zero components).')],
    misc=[('|a + b| = |a| + |b| for all vectors a and b.', 'This only holds if a and b point in the same direction; in general |a + b| ≤ |a| + |b| (triangle inequality).'),
          ('The magnitude of (3, −4) is −1 because 3 + (−4) = −1.', 'Magnitude is √(3² + (−4)²) = 5; it is never negative.'),
          ('AB and BA are the same vector because they join the same points.', 'BA = −AB: same length, opposite direction.')],
))


@R.add('ch03-st1', 'C1', (1, 3), 'mcq')
def vec_mag_mcq(rng, slot):
    v = rv(rng, -7, 7)
    m2 = sum(c * c for c in v)
    right = P(sp.sqrt(m2))
    wr = [str(m2), P(sp.sqrt(abs(sum(v)))) if sum(v) != 0 else '0', P(sp.sqrt(m2 + 2)), str(sum(abs(c) for c in v))]
    form = rng.choice(['ijk', 'col'])
    vt = ijk(v) if form == 'ijk' else V(v)
    return mcq(rng, f'Find the magnitude of the vector v = {vt}.', right, wr, f'|v| = √({" + ".join(str(c * c) for c in v)}) = {right}.')


@R.add('ch03-st1', 'C1', (1, 2), 'short')
def vec_AB(rng, slot):
    A, B = rv(rng, -8, 8), rv(rng, -8, 8)
    if A == B:
        return None
    return mk(f'The points A and B have coordinates {pt(A)} and {pt(B)}. Write down the vector AB.', V(B - A),
              f'AB = b − a = {V(B - A)} (A1 for each two components correct: A1 A1).', 2)


@R.add('ch03-st1', 'C3', (1, 4), 'short', style='p1')
def vec_unit_scaled(rng, slot):
    v = rv(rng, -6, 6)
    m = mag(v)
    kind = rng.choice(['unit', 'scaled', 'scaled'])
    if kind == 'unit':
        u = sp.Matrix([sp.radsimp(c / m) for c in v])
        return mk(f'Find a unit vector in the direction of {ijk(v)}.', V(u), f'|v| = {P(m)} (A1); v/|v| (M1) = {V(u)} (A1).', 3)
    kk = rng.choice([2, 3, 5, 6, 10, 12, 7])
    w = sp.Matrix([sp.radsimp(kk * c / m) for c in v])
    return mk(f'Find the vector of magnitude {kk} that has the same direction as {V(v)}.', V(w),
              f'|v| = {P(m)} (A1); {kk}v/|v| (M1); {V(w)} (A1).', 3)


@R.add('ch03-st1', 'C3', (2, 4), 'short', style='p1')
def vec_find_p(rng, slot):
    a, b = nz(rng, -6, 6), nz(rng, -6, 6)
    p0 = rng.randint(1, 9)
    m2 = a * a + b * b + p0 * p0
    pos = rng.randint(0, 2)
    comps = [a, b]
    comps.insert(pos, 'p')
    return mk(f'The vector v = ({", ".join(str(c) if c != "p" else "p" for c in comps)}) has magnitude √{m2}. Find the possible values of p.'.replace('-', '−'),
              f'p = ±{p0}', f'p² + {a * a} + {b * b} = {m2} (M1 A1); p² = {p0 * p0} (A1); p = ±{p0} (A1).', 4)


@R.add('ch03-st1', 'C3', (2, 4), 'short')
def vec_ratio_point(rng, slot):
    A, B = rv(rng, -6, 6), rv(rng, -6, 6)
    m_, n_ = rng.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
    Pp = A + sp.Rational(m_, m_ + n_) * (B - A)
    if A == B:
        return None
    frame = rng.choice([f'The point P lies on the line segment AB, where A{pt(A)} and B{pt(B)}, such that AP : PB = {m_} : {n_}. Find the position vector of P.',
                        f'Given A{pt(A)} and B{pt(B)}, find the coordinates of the point P on AB with AP = {m_}/{m_ + n_} of AB.'])
    return mk(frame, V(Pp), f'OP = a + ({m_}/{m_ + n_})AB (M1); AB = {V(B - A)} (A1); OP = {V(Pp)} (A1).', 3)


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def vec_parallel_explain(rng, slot):
    v = rv(rng, -5, 5)
    kk = rng.choice([2, 3, -2, -3, sp.Rational(1, 2), -sp.Rational(3, 2)])
    w = kk * v
    par = rng.random() < 0.5
    if not par:
        i = rng.randint(0, 2)
        w = sp.Matrix(w)
        w[i] = w[i] + rng.choice([1, -1, 2])
    if any(not sp.nsimplify(c).is_Integer for c in w):
        return None
    ans = f'parallel: second = {P(kk)} × first' if par else 'not parallel: the component ratios are not all equal'
    return mk(f'Determine whether the vectors {V(v)} and {V(w)} are parallel, explaining your reasoning.', ans,
              f'Parallel iff one is a scalar multiple of the other (R1); compare component ratios (M1); conclusion: {ans} (A1).', 3, 'explain')


@R.add('ch03-st1', 'C4', (3, 5), 'multi_step', style='ext')
def vec_parallelogram(rng, slot):
    A, B, C = rv(rng, -5, 6), rv(rng, -5, 6), rv(rng, -5, 6)
    D = A + C - B
    AB, BC = B - A, C - B
    if crossv(AB, BC) == sp.zeros(3, 1):
        return None
    M = (A + C) / 2
    diag1, diag2 = mag(C - A), mag(D - B)
    return mk(f'The points A{pt(A)}, B{pt(B)} and C{pt(C)} are three vertices of the parallelogram ABCD.\n(a) Find the vectors AB and BC.\n(b) Find the coordinates of D.\n(c) Find the coordinates of the point where the diagonals intersect.\n(d) Find the exact lengths of the diagonals AC and BD and hence determine whether ABCD is a rectangle.',
              f'(a) AB = {V(AB)}, BC = {V(BC)} (b) D{pt(D)} (c) {pt(M)} (d) AC = {P(diag1)}, BD = {P(diag2)}; {"rectangle" if diag1 == diag2 else "not a rectangle"}',
              f'(a) A1 A1. (b) AD = BC so OD = a + BC (M1) = {V(D)} (A1). (c) midpoint of AC (M1) {pt(M)} (A1). (d) |AC| = {P(diag1)}, |BD| = {P(diag2)} (A1 A1); a parallelogram is a rectangle iff its diagonals are equal (R1): {"rectangle" if diag1 == diag2 else "not a rectangle"} (A1).', 10)


@R.add('ch03-st1', 'C4', (2, 4), 'multi_step', style='p1')
def vec_collinear_k(rng, slot):
    A = rv(rng, -5, 5)
    d = rv(rng, -3, 3)
    s_ = rng.choice([2, 3, -1, -2, sp.Rational(1, 2)])
    B = A + d
    C = A + s_ * d
    i = rng.randint(0, 2)
    if d[i] == 0 or any(not sp.nsimplify(c).is_Integer for c in C):
        return None
    Ct = [P(c) for c in C]
    Ct[i] = 'k'
    return mk(f'The points A{pt(A)}, B{pt(B)} and C({", ".join(Ct)}) are collinear. Find the value of k and the ratio AB : BC.',
              f'k = {P(C[i])}; AB : BC = {P(abs(1))} : {P(abs(s_ - 1))}' if s_ > 1 else f'k = {P(C[i])}',
              f'AC = λAB (M1); compare the known components to get λ = {P(s_)} (A1); k = {P(C[i])} (A1); ratio from λ (A1).', 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch03-st2', F(
    terms=[('scalar product', 'v·w = v₁w₁ + v₂w₂ + v₃w₃ = |v||w|cos θ, where θ is the angle between v and w'),
           ('perpendicular vectors', 'non-zero vectors whose scalar product is zero, so the angle between them is π/2'),
           ('angle between two vectors', 'the angle θ, 0 ≤ θ ≤ π, given by cos θ = v·w/(|v||w|) when the vectors are placed tail to tail')],
    facts=[('If v·w < 0, the angle between v and w is', 'obtuse', ['acute', 'a right angle', 'zero'], 'cos θ < 0 means π/2 < θ ≤ π.'),
           ('What is (i + 2j − k)·(3i − j + 2k)?', '−1', ['1', '3', '(3, −2, −2)'], '3 − 2 − 2 = −1; the scalar product is a number, not a vector.'),
           ('For any vector v, v·v equals', '|v|²', ['|v|', '0', '2|v|'], 'v·v = v₁² + v₂² + v₃².'),
           ('Which pair of vectors is perpendicular?', '(2, 1, −1) and (1, −1, 1)', ['(1, 2, 3) and (3, 2, 1)', '(1, 0, 1) and (1, 1, 0)', '(2, −1, 0) and (1, 2, 1)'], '2 − 1 − 1 = 0.')],
    why=[('Explain why v·w = 0 implies that non-zero vectors v and w are perpendicular.', 'v·w = |v||w|cos θ with |v|, |w| ≠ 0, so cos θ = 0 and θ = π/2.'),
         ('Explain why the scalar product is commutative.', 'v·w = Σvᵢwᵢ = Σwᵢvᵢ = w·v, since multiplication of numbers is commutative.'),
         ('Explain how the sign of v·w tells you whether the angle between v and w is acute or obtuse.', 'v·w has the sign of cos θ: positive for acute θ, zero for a right angle, negative for obtuse θ.'),
         ('Explain why, to find angle ABC, you must use BA and BC rather than AB and BC.', 'The angle at B is between the two vectors drawn from B; using AB reverses one vector and gives the supplementary angle π − θ.')],
    misc=[('The scalar product of (1, 2, 3) and (4, 5, 6) is (4, 10, 18).', 'The scalar product is a number: 4 + 10 + 18 = 32.'),
          ('If a·b = a·c then b = c.', 'It only means a·(b − c) = 0, i.e. b − c is perpendicular to a (or zero); b and c can differ.'),
          ('cos θ = v·w/(|v| + |w|).', 'The denominator is the product |v||w|, not the sum.')],
))


@R.add('ch03-st2', 'C1', (1, 3), 'mcq')
def dot_mcq(rng, slot):
    a, b = rv(rng, -6, 6), rv(rng, -6, 6)
    dv = dot(a, b)
    wr = [str(dv + rng.choice([2, -2, 4])), V(sp.Matrix([p_ * q_ for p_, q_ in zip(a, b)])), str(-dv) if dv != 0 else '1', str(sum(a) * sum(b)) if sum(a) * sum(b) != dv else str(dv + 1)]
    return mcq(rng, f'Given a = {ijk(a)} and b = {ijk(b)}, find a·b.', str(dv).replace('-', '−'), [w.replace('-', '−') for w in wr],
               f'a·b = {" + ".join(f"({p_})({q_})" for p_, q_ in zip(a, b))} = {dv}.')


@R.add('ch03-st2', 'C3', (1, 4), 'short', style='p2')
def dot_angle_p2(rng, slot):
    a, b = rv(rng, -7, 7), rv(rng, -7, 7)
    cosv = dot(a, b) / (mag(a) * mag(b))
    if abs(float(cosv)) > 0.999:
        return None
    unit = rng.choice(['degrees', 'radians'])
    ang = deg_of(cosv) if unit == 'degrees' else math.acos(float(cosv))
    frame = rng.choice([f'Find the angle between the vectors {V(a)} and {V(b)}, giving your answer in {unit}.',
                        f'Calculate, in {unit}, the angle between u = {ijk(a)} and v = {ijk(b)}.'])
    return mk(frame, f'{s3(ang)}{"°" if unit == "degrees" else ""}',
              f'Scalar product {dot(a, b)} (A1); magnitudes {P(mag(a))}, {P(mag(b))} (A1); cos θ = {dot(a, b)}/({P(mag(a))} × {P(mag(b))}) (M1); θ = {s3(ang)}{"°" if unit == "degrees" else " rad"} (A1).', 4)


@R.add('ch03-st2', 'C3', (1, 4), 'short', style='p1')
def dot_perp_k(rng, slot):
    a = rv(rng, -6, 6)
    b = rv(rng, -6, 6)
    i = rng.choice([j for j in range(3) if a[j] != 0])
    rest = sum(a[j] * b[j] for j in range(3) if j != i)
    kv = sp.Rational(-rest, a[i])
    lin = rng.random() < 0.4 and slot.d >= 3
    bt = [P(c) for c in b]
    if lin:
        bt[i] = '2k + 1'
        kv = (kv - 1) / 2
    else:
        bt[i] = 'k'
    return mk(f'The vectors {V(a)} and ({", ".join(bt)}) are perpendicular. Find the value of k.', f'k = {P(kv)}',
              f'Set the scalar product equal to zero (M1); {P(a[i])}({bt[i]}) + {rest} = 0 (A1); k = {P(kv)} (A1).', 3)


@R.add('ch03-st2', 'C3', (2, 4), 'short', style='p1')
def dot_exact_cos(rng, slot):
    A, B, C = rv(rng, -4, 5), rv(rng, -4, 5), rv(rng, -4, 5)
    BA, BC = A - B, C - B
    if mag(BA) == 0 or mag(BC) == 0:
        return None
    cosv = sp.radsimp(dot(BA, BC) / (mag(BA) * mag(BC)))
    return mk(f'The points A{pt(A)}, B{pt(B)} and C{pt(C)} are given. Find the exact value of cos(ABC).', P(cosv),
              f'BA = {V(BA)}, BC = {V(BC)} (A1 A1); BA·BC = {dot(BA, BC)} (A1); cos ABC = {dot(BA, BC)}/({P(mag(BA))} × {P(mag(BC))}) (M1) = {P(cosv)} (A1).', 5)


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def dot_sign_explain(rng, slot):
    a, b = rv(rng, -6, 6), rv(rng, -6, 6)
    dv = dot(a, b)
    kind = 'obtuse' if dv < 0 else 'acute' if dv > 0 else 'a right angle'
    return mk(f'Without finding the angle, explain whether the angle between {V(a)} and {V(b)} is acute, obtuse or a right angle.', kind,
              f'a·b = {dv} (A1); a·b = |a||b|cos θ and |a||b| > 0 so cos θ has the sign of a·b (R1); hence the angle is {kind} (A1).', 3, 'explain')


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def dot_error(rng, slot):
    A, B, C = rv(rng, -4, 5), rv(rng, -4, 5), rv(rng, -4, 5)
    AB, BC = B - A, C - B
    if mag(AB) == 0 or mag(BC) == 0 or abs(float(dot(AB, BC) / (mag(AB) * mag(BC)))) > 0.99:
        return None
    wrong = deg_of(dot(AB, BC) / (mag(AB) * mag(BC)))
    right = 180 - wrong
    nm = who(rng)
    return mk(f'{nm} finds angle ABC for A{pt(A)}, B{pt(B)}, C{pt(C)} using the vectors AB and BC and obtains {s3(wrong)}°. Explain the error and find the correct angle.',
              f'{s3(right)}°', f'The angle at B is between BA and BC (both from B) (R1); using AB reverses one vector and gives the supplement (R1); correct angle 180° − {s3(wrong)}° = {s3(right)}° (A1).', 3, 'explain', 'G2')


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step', style='ext')
def dot_triangle(rng, slot):
    A, B, C = rv(rng, -4, 6), rv(rng, -4, 6), rv(rng, -4, 6)
    AB, AC = B - A, C - A
    if crossv(AB, AC) == sp.zeros(3, 1):
        return None
    cosA = sp.radsimp(dot(AB, AC) / (mag(AB) * mag(AC)))
    sinA = sp.radsimp(sp.sqrt(1 - cosA ** 2))
    area = sp.radsimp(mag(AB) * mag(AC) * sinA / 2)
    area2 = sp.radsimp(mag(crossv(AB, AC)) / 2)
    return mk(f'The triangle ABC has vertices A{pt(A)}, B{pt(B)} and C{pt(C)}.\n(a) Find AB and AC.\n(b) Find the exact value of cos(BAC).\n(c) Hence find the exact value of sin(BAC).\n(d) Find the exact area of triangle ABC.',
              f'(a) AB = {V(AB)}, AC = {V(AC)} (b) {P(cosA)} (c) {P(sinA)} (d) {P(sp.simplify(area2))}',
              f'(a) A1 A1. (b) AB·AC = {dot(AB, AC)} (A1); |AB| = {P(mag(AB))}, |AC| = {P(mag(AC))} (A1); cos = {P(cosA)} (M1 A1). (c) sin²A = 1 − cos²A (M1), sin A = {P(sinA)} (A1, positive as 0 < A < π). (d) ½|AB||AC| sin A (M1) = {P(sp.simplify(area2))} (A1).', 10)


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step', style='p2')
def dot_right_angle(rng, slot):
    A = rv(rng, -4, 4)
    u = rv(rng, -3, 3)
    w = rv(rng, -3, 3)
    w = w - (dot(w, u) / dot(u, u)) * u
    w = w * sp.ilcm(*[sp.fraction(c)[1] for c in w])
    if mag(w) == 0 or max(abs(c) for c in w) > 12:
        return None
    B, C = A + u, A + w
    BC = C - B
    angB = deg_of(dot(A - B, C - B) / (mag(A - B) * mag(BC)))
    return mk(f'The points A{pt(A)}, B{pt(B)} and C{pt(C)} are given.\n(a) Show that triangle ABC is right-angled at A.\n(b) Find the area of the triangle.\n(c) Find the size of angle ABC in degrees.',
              f'(a) AB·AC = 0 (b) {s3(mag(u) * mag(w) / 2)} (exact {P(sp.radsimp(mag(u) * mag(w) / 2))}) (c) {s3(angB)}°',
              f'(a) AB = {V(u)}, AC = {V(w)} (A1); AB·AC = 0 (M1) so AB ⟂ AC AG (R1). (b) ½|AB||AC| (M1) = {s3(mag(u) * mag(w) / 2)} (A1). (c) tan B = |AC|/|AB| or scalar product (M1) = {s3(angB)}° (A1).', 7)


# ---------------------------------------------------------------------------------------------
R.facts('ch03-st3', F(
    terms=[('collinear points', 'points lying on one straight line; A, B, C are collinear if AC = λAB for some scalar λ'),
           ('ratio theorem', 'if P divides AB in the ratio m : n then p = (n a + m b)/(m + n)')],
    facts=[('A, B, C are collinear if', 'AC is a scalar multiple of AB', ['AB·AC = 0', '|AB| = |AC|', 'AB + AC = 0'], 'Parallel vectors through a common point lie on one line.'),
           ('In parallelogram OABC with OA = a and OC = c, the vector OB is', 'a + c', ['a − c', 'c − a', '(a + c)/2'], 'OB = OA + AB = a + c.'),
           ('ABCD is a rhombus. Which is always true?', 'AC·BD = 0', ['AB·BC = 0', 'AC = BD', '|AC| = |AB|'], 'The diagonals of a rhombus are perpendicular.')],
    why=[('Explain how vectors can be used to show that the diagonals of a parallelogram bisect each other.', 'With OA = a, OC = c, OB = a + c: the midpoint of OB is (a + c)/2 and the midpoint of AC is (a + c)/2; they coincide.'),
         ('Explain why showing AB = DC proves that ABCD is a parallelogram.', 'Equal vectors have the same length and direction, so AB and DC are parallel and equal; a quadrilateral with one pair of opposite sides parallel and equal is a parallelogram.'),
         ('Explain how to use the scalar product to show that a parallelogram is a rectangle.', 'Show that two adjacent sides have scalar product zero, so the angle between them is a right angle.')],
    misc=[('If AB is parallel to CD then A, B, C and D are collinear.', 'Parallel vectors can lie on different parallel lines; collinearity needs a common point as well.'),
          ('A quadrilateral with equal diagonals is a rectangle.', 'Equal diagonals alone are not enough (an isosceles trapezium also has them); a parallelogram with equal diagonals is a rectangle.')],
))


@R.add('ch03-st3', 'C3', (1, 4), 'short')
def geo_collinear(rng, slot):
    A = rv(rng, -5, 5)
    d = rv(rng, -3, 3)
    lam = rng.choice([2, 3, -1, -2, 4])
    col_ = rng.random() < 0.6
    B = A + d
    C = A + lam * d
    if not col_:
        C = C + sp.Matrix([0, 0, rng.choice([1, -1])])
    ans = f'collinear: AC = {lam}AB' if col_ else 'not collinear: AC is not a multiple of AB'
    return mk(f'Determine whether the points A{pt(A)}, B{pt(B)} and C{pt(C)} are collinear.', ans,
              f'AB = {V(B - A)}, AC = {V(C - A)} (A1 A1); compare for a scalar multiple (M1); {ans} (A1).', 4)


@R.add('ch03-st3', 'C3', (2, 4), 'short', style='p1')
def geo_rhombus(rng, slot):
    a, b = rng.choice([(3, 4), (5, 12), (1, 2), (2, 3), (6, 8), (4, 1)])
    O = rv(rng, -3, 3)
    u = sp.Matrix([a, b, 0])
    w = sp.Matrix([b, a, 0])
    A, B, C = O, O + u, O + u + w
    D = O + w
    return mk(f'The points A{pt(A)}, B{pt(B)}, C{pt(C)} and D{pt(D)} form a quadrilateral. Show that ABCD is a rhombus and find the exact lengths of its diagonals.',
              f'AB = DC = {V(u)}, |AB| = |BC| = {P(mag(u))}; diagonals {P(mag(C - A))} and {P(mag(D - B))}',
              f'AB = DC so parallelogram (M1 A1); |AB| = |BC| = {P(mag(u))} so rhombus (R1); AC = {P(mag(C - A))}, BD = {P(mag(D - B))} (A1 A1).', 5)


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def geo_ratio_proof(rng, slot):
    m_, n_ = rng.choice([(1, 2), (2, 1), (1, 3), (2, 3), (3, 1)])
    shape = rng.choice(['triangle', 'parallelogram'])
    if shape == 'triangle':
        return mk(f'In triangle OAB, OA = a and OB = b. M is the midpoint of OA and N is the point on OB with ON : NB = {m_} : {n_}.\n(a) Express AB, MN and AN in terms of a and b.\n(b) The point P lies on AN such that MP is parallel to OB. Find AP : PN.',
                  f'(a) AB = b − a, MN = {P(sp.Rational(m_, m_ + n_))}b − ½a, AN = {P(sp.Rational(m_, m_ + n_))}b − a (b) AP : PN = 1 : 1',
                  f'(a) A1 A1 A1. (b) Let OP = a + λAN (M1); MP = OP − OM = (½ − λ)a + λ({P(sp.Rational(m_, m_ + n_))})b (A1); parallel to b requires ½ − λ = 0 (M1), λ = ½ (A1) so P is the midpoint of AN, AP : PN = 1 : 1 (A1).', 8)
    return mk(f'OABC is a parallelogram with OA = a and OC = c. The point D divides AB in the ratio {m_} : {n_}, and E is the midpoint of BC.\n(a) Find OD and OE in terms of a and c.\n(b) Find DE in terms of a and c.\n(c) The line OD meets AC at X. Find OX in terms of a and c.',
              f'(a) OD = a + {P(sp.Rational(m_, m_ + n_))}c, OE = ½a + c (b) DE = −½a + {P(1 - sp.Rational(m_, m_ + n_))}c (c) OX = {P(1 / (1 + sp.Rational(m_, m_ + n_)))}(a + {P(sp.Rational(m_, m_ + n_))}c)',
              f'(a) AB = c so OD = a + ({m_}/{m_ + n_})c (A1); OE = c + ½a (A1). (b) OE − OD (M1) (A1). (c) OX = μ OD and OX = a + ν(c − a) (M1); equate coefficients of a and c (M1); μ = {P(1 / (1 + sp.Rational(m_, m_ + n_)))} (A1); OX as stated (A1).', 9)


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step', style='p1')
def geo_kite(rng, slot):
    A = rv(rng, -3, 3)
    u = rv(rng, -3, 3)
    w = rv(rng, -3, 3)
    if crossv(u, w) == sp.zeros(3, 1):
        return None
    B, D = A + u, A + w
    lam = rng.choice([2, 3, sp.Rational(3, 2), sp.Rational(1, 2)])
    C = B + D - A if rng.random() < 0.5 else A + lam * (u + w)
    AC, BD = C - A, D - B
    par = (C == B + D - A)
    perp = dot(AC, BD) == 0
    shape = ('rhombus' if perp else 'parallelogram') if par else ('kite' if mag(B - A) == mag(D - A) and mag(C - B) == mag(C - D) else 'quadrilateral with AC along the diagonal direction AB + AD')
    return mk(f'The points A{pt(A)}, B{pt(B)}, C{pt(C)} and D{pt(D)} are given.\n(a) Find AB, AD and AC.\n(b) Show that AC = k(AB + AD) and state the value of k.\n(c) Find AC·BD and interpret your answer.\n(d) Determine whether ABCD is a parallelogram, giving a reason.',
              f'(a) AB = {V(u)}, AD = {V(w)}, AC = {V(AC)} (b) k = {P(1 if par else lam)} (c) {dot(AC, BD)}; diagonals {"perpendicular" if perp else "not perpendicular"} (d) {"yes" if par else "no"}',
              f'(a) A1 A1 A1. (b) AB + AD = {V(u + w)} (A1) so k = {P(1 if par else lam)} (A1). (c) BD = {V(BD)} (A1); AC·BD = {dot(AC, BD)} (A1); {"zero, so the diagonals are perpendicular" if perp else "non-zero, so the diagonals are not perpendicular"} (R1). (d) ABCD is a parallelogram iff AC = AB + AD, i.e. k = 1 (R1): {"yes" if par else "no"} (A1).', 10)


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step', style='p2')
def geo_cube(rng, slot):
    a = rng.randint(2, 9)
    h = rng.randint(2, 12)
    b = rng.randint(2, 9)
    O = sp.Matrix([0, 0, 0])
    G = sp.Matrix([a, b, h])
    E = sp.Matrix([a, 0, h])
    M = sp.Matrix([sp.Rational(a, 2), b, 0])
    ang_base = math.degrees(math.atan(h / math.hypot(a, b)))
    cosv = dot(G - O, M - O) / (mag(G) * mag(M))
    ctx = rng.choice(['A cuboid-shaped storage container', 'A rectangular room', 'A glass display case'])
    return mk(f'{ctx} OABCDEFG has O at the origin, OA along the x-axis with OA = {a} m, OC along the y-axis with OC = {b} m and OD vertical with OD = {h} m; G is the vertex opposite O. M is the midpoint of the edge CB.\n(a) Write down the position vectors of G and M.\n(b) Find the length of the diagonal OG.\n(c) Find the angle between OG and the base OABC.\n(d) Find the angle GOM.',
              f'(a) OG = {V(G)}, OM = {V(M)} (b) {s3(math.sqrt(float(dot(G, G))))} m (c) {s3(ang_base)}° (d) {s3(deg_of(cosv))}°',
              f'(a) A1 A1. (b) √({a}² + {b}² + {h}²) (M1) = {s3(math.sqrt(float(dot(G, G))))} (A1). (c) angle with projection (√({a * a + b * b}) on base) (M1); tan θ = {h}/√{a * a + b * b} (A1); {s3(ang_base)}° (A1). (d) OG·OM = {P(dot(G, M))} (A1); cos θ = OG·OM/(|OG||OM|) (M1); {s3(deg_of(cosv))}° (A1).', 10)


@R.add('ch03-st3', 'C2', (2, 4), 'explain')
def geo_explain_shape(rng, slot):
    a, b = rng.randint(1, 5), rng.randint(1, 5)
    c = rng.randint(1, 4)
    O = rv(rng, -3, 3)
    u = sp.Matrix([a, 0, 0])
    w = sp.Matrix([0, b, c])
    A, B, C, D = O, O + u, O + u + w, O + w
    return mk(f'Explain how you would use vectors to decide whether A{pt(A)}, B{pt(B)}, C{pt(C)}, D{pt(D)} is a rectangle, and carry out the test.', 'rectangle',
              f'AB = DC = {V(u)} so ABCD is a parallelogram (M1 R1); AB·AD = {dot(u, w)} = 0 so adjacent sides are perpendicular (M1); hence a rectangle (R1).', 4, 'explain')


@R.add('ch03-st3', 'C1', (1, 3), 'mcq')
def geo_mid_mcq(rng, slot):
    A, B = rv(rng, -8, 8), rv(rng, -8, 8)
    M = (A + B) / 2
    return mcq(rng, f'A{pt(A)} and B{pt(B)} are the ends of a diameter of a sphere. What is the centre of the sphere?', pt(M),
               [pt(B - A), pt((B - A) / 2), pt(A + B)], 'The centre is the midpoint (a + b)/2.')


@R.add('ch03-st3', 'C3', (2, 5), 'short', style='p2')
def geo_ship(rng, slot):
    p0 = rv(rng, -5, 5, 2)
    v = rv(rng, -4, 4, 2)
    q0 = rv(rng, -5, 5, 2)
    w = rv(rng, -4, 4, 2)
    if v == w:
        return None
    # distance squared between positions as function of t
    dvec = (p0 - q0) + t * (v - w)
    D2 = sp.expand(dvec.dot(dvec))
    tm = sp.solve(sp.diff(D2, t), t)[0]
    if tm < 0:
        return None
    dmin = math.sqrt(float(D2.subs(t, tm)))
    ctx = rng.choice(['Two ships', 'Two drones flying at the same altitude', 'Two cyclists crossing a park'])
    return mk(f'{ctx} A and B have position vectors rA = {V(p0)} + t{V(v)} and rB = {V(q0)} + t{V(w)} (km) at time t hours. Find the time at which they are closest together and the minimum distance between them.',
              f't = {s3(tm)} h, minimum distance {s3(dmin)} km', f'AB = rB − rA = {V(-(dvec))} (M1 A1); |AB|² = {P(D2)} (A1); minimise: d/dt = 0 (M1) t = {s3(tm)} (A1); distance {s3(dmin)} km (A1).', 6)


# =============================================================================================
# ch04 Lines and planes in 3D
# =============================================================================================
def line_txt(a, d, par='λ'):
    return f'r = {V(a)} + {par}{V(d)}'


R.facts('ch04-st1', F(
    terms=[('vector equation of a line', 'r = a + λb, where a is the position vector of a point on the line, b is a direction vector and λ is a real parameter'),
           ('direction vector', 'any non-zero vector parallel to a line'),
           ('parametric equations of a line', 'x = x₀ + λl, y = y₀ + λm, z = z₀ + λn, obtained from the components of r = a + λb'),
           ('Cartesian equation of a line', '(x − x₀)/l = (y − y₀)/m = (z − z₀)/n for a line through (x₀, y₀, z₀) with direction (l, m, n)')],
    facts=[('Which point lies on the line r = (1, 2, −1) + λ(2, 0, 3)?', '(5, 2, 5)', ['(3, 2, 1)', '(2, 0, 3)', '(5, 4, 5)'], 'λ = 2 gives (5, 2, 5).'),
           ('A direction vector of the line (x − 3)/2 = (y + 1)/5 = z/(−4) is', '(2, 5, −4)', ['(3, −1, 0)', '(−3, 1, 0)', '(2, 5, 4)'], 'The denominators give the direction.'),
           ('Two lines are parallel if', 'their direction vectors are scalar multiples of each other', ['they have a common point', 'their position vectors are equal', 'their direction vectors are perpendicular'], 'Parallel means the same direction.')],
    why=[('Explain why the vector equation of a line is not unique.', 'Any point on the line can be used as a, and any non-zero multiple of the direction vector can be used as b, giving different-looking equations of the same line.'),
         ('Explain how to check whether a point lies on a given line r = a + λb.', 'Set the coordinates equal to the components of a + λb; find λ from one equation and check that the same λ satisfies the other two.'),
         ('Explain why the angle between two lines is found from their direction vectors only.', 'The angle depends only on the directions of the lines, not on where they are; the position vectors simply locate the lines.')],
    misc=[('The line r = (2, 1, 0) + λ(1, 3, −2) passes through (1, 3, −2).', '(1, 3, −2) is the direction vector, not a point; check: (2 + λ, 1 + 3λ, −2λ) = (1, 3, −2) needs λ = −1 and λ = 2/3 – inconsistent.'),
          ('The angle between two lines is always the angle given by cos θ = d₁·d₂/(|d₁||d₂|), even if it is obtuse.', 'The angle between lines is taken as the acute angle: use |d₁·d₂| in the numerator.')],
))


@R.add('ch04-st1', 'C1', (1, 2), 'short')
def line_through_two(rng, slot):
    A, B = rv(rng, -6, 6), rv(rng, -6, 6)
    if A == B:
        return None
    return mk(f'Write down a vector equation of the line through A{pt(A)} and B{pt(B)}.', line_txt(A, B - A),
              f'Direction AB = {V(B - A)} (A1); r = {V(A)} + λ{V(B - A)} (A1). Any correct equivalent form is accepted.', 2)


@R.add('ch04-st1', 'C1', (1, 3), 'mcq')
def line_point_mcq(rng, slot):
    a, d = rv(rng, -5, 5), rv(rng, -3, 3)
    lam = nz(rng, -3, 3)
    Pp = a + lam * d
    wr = [pt(Pp + sp.Matrix([0, 1, 0])), pt(d), pt(a + d + sp.Matrix([1, 0, 0])), pt(a - lam * d + sp.Matrix([0, 0, 1]))]
    return mcq(rng, f'Which of the following points lies on the line {line_txt(a, d)}?', pt(Pp), wr, f'λ = {lam} gives {pt(Pp)}.')


@R.add('ch04-st1', 'C3', (1, 4), 'short')
def line_cartesian(rng, slot):
    a, d = rv(rng, -6, 6), rv(rng, -5, 5)
    if 0 in list(d):
        return None
    def part(v, c, dd):
        num = v if c == 0 else f'{v} {"−" if c > 0 else "+"} {abs(c)}'
        return f'({num})/{dd}'.replace('-', '−') if dd != 1 else f'{num}'
    cart = ' = '.join(part(v, c, dd) for v, c, dd in zip('xyz', a, d))
    if rng.random() < 0.5:
        return mk(f'Find the Cartesian equation of the line {line_txt(a, d)}.', cart,
                  f'Parametric: x = {P(a[0] + d[0] * k_)}, ... (M1); make λ the subject of each (M1); {cart} (A1).', 3)
    return mk(f'A line has Cartesian equation {cart}. Write down a vector equation of the line.', line_txt(a, d),
              f'Point {pt(a)} from the numerators (A1); direction {V(d)} from the denominators (A1); r = ... (A1).', 3)


@R.add('ch04-st1', 'C3', (2, 4), 'short')
def line_on_check(rng, slot):
    a, d = rv(rng, -5, 5), rv(rng, -3, 3)
    if 0 in list(d):
        return None
    lam = nz(rng, -4, 4)
    Pp = a + lam * d
    on = rng.random() < 0.5
    if not on:
        Pp = Pp + sp.Matrix([0, 0, rng.choice([1, 2, -1])])
    ans = f'yes, λ = {lam}' if on else 'no: the three equations give different values of λ'
    return mk(f'Determine whether the point P{pt(Pp)} lies on the line {line_txt(a, d)}.', ans,
              f'Equate components (M1); solve for λ from each equation (A1); {"consistent λ = " + str(lam) if on else "values of λ differ"} (R1); conclusion (A1).', 4)


@R.add('ch04-st1', 'C3', (2, 4), 'short', style='p2')
def line_angle(rng, slot):
    d1, d2 = rv(rng, -5, 5), rv(rng, -5, 5)
    c = abs(dot(d1, d2)) / (mag(d1) * mag(d2))
    if float(c) > 0.995:
        return None
    a1, a2 = rv(rng, -5, 5), rv(rng, -5, 5)
    ang = deg_of(c)
    return mk(f'Find the acute angle between the lines {line_txt(a1, d1)} and {line_txt(a2, d2, "μ")}.', f'{s3(ang)}°',
              f'Use the direction vectors (M1); d₁·d₂ = {dot(d1, d2)} (A1); |d₁| = {P(mag(d1))}, |d₂| = {P(mag(d2))} (A1); acute angle {s3(ang)}° (A1).', 4)


@R.add('ch04-st1', 'C2', (2, 4), 'explain')
def line_same(rng, slot):
    a, d = rv(rng, -5, 5), rv(rng, -3, 3)
    lam = nz(rng, -3, 3)
    kk = rng.choice([2, -1, 3, -2])
    b = a + lam * d
    nm = who(rng)
    return mk(f'{nm} writes the equation of a line as {line_txt(a, d)} and a friend writes {line_txt(b, kk * d, "μ")}. Explain why both equations describe the same line.', 'Same direction (parallel) and a common point.',
              f'Direction vectors are parallel: {V(kk * d)} = {kk}{V(d)} (R1); the point {pt(b)} lies on the first line with λ = {lam} (M1 A1); so the lines coincide (R1).', 4, 'explain')


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step', style='ext')
def line_closest_origin(rng, slot):
    d = rv(rng, -3, 3)
    a = rv(rng, -6, 6)
    lam0 = -dot(a, d) / dot(d, d)
    F_ = a + lam0 * d
    dist = sp.radsimp(mag(F_))
    plane_hit = None
    i = rng.choice([j for j in range(3) if d[j] != 0])
    lam_i = sp.Rational(-a[i], d[i])
    Q = a + lam_i * d
    ax = 'xyz'[i]
    return mk(f'The line L has equation {line_txt(a, d)}.\n(a) Find the coordinates of the point where L meets the plane {ax} = 0.\n(b) The point F on L is the foot of the perpendicular from the origin O. Show that λ = {P(lam0)} at F.\n(c) Find the coordinates of F and the exact shortest distance from O to L.',
              f'(a) {pt(Q)} (b) OF·d = 0 gives λ = {P(lam0)} (c) F{pt(F_)}, distance {P(dist)}',
              f'(a) {ax}-component = 0 gives λ = {P(lam_i)} (M1) point {pt(Q)} (A1). (b) OF = a + λd (M1); OF·d = 0 (M1); {dot(a, d)} + {dot(d, d)}λ = 0 (A1) AG. (c) F = {pt(F_)} (A1); |OF| = {P(dist)} (M1 A1).', 8)


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st2', F(
    terms=[('skew lines', 'lines in three dimensions that are not parallel and do not intersect'),
           ('coincident lines', 'equations that describe the same line: parallel direction vectors and a common point'),
           ('intersecting lines', 'non-parallel lines that share exactly one point')],
    facts=[('Two lines in 2D that are not parallel', 'must intersect', ['may be skew', 'must be perpendicular', 'never meet'], 'Skew lines only exist in three dimensions.'),
           ('To show that two non-parallel lines in 3D are skew, you show that', 'the system λ, μ from equating components has no solution', ['their direction vectors are perpendicular', 'their direction vectors are parallel', 'they pass through the origin'], 'Equate the parametric forms; inconsistency of the third equation proves they do not meet.'),
           ('Lines with direction vectors (2, −4, 6) and (−1, 2, −3) are', 'parallel or coincident', ['skew', 'perpendicular', 'intersecting'], '(2, −4, 6) = −2(−1, 2, −3).')],
    why=[('Explain why two lines in 3D can fail to intersect even if they are not parallel.', 'In three dimensions lines can pass above/below each other in different planes; such skew lines have no common point but are not parallel.'),
         ('Explain why different parameters (λ and μ) must be used for two lines when finding their intersection.', 'The point of intersection is reached at generally different parameter values on each line; using the same letter forces them to be equal and can miss the intersection.'),
         ('Explain the steps to classify two lines as parallel, intersecting or skew.', 'First compare direction vectors: multiples → parallel (check a common point for coincidence). Otherwise equate components, solve two equations for λ and μ, and test the third: consistent → intersecting, inconsistent → skew.')],
    misc=[('The lines r = (1, 0, 0) + λ(1, 1, 0) and r = (0, 0, 1) + λ(0, 1, 1) do not intersect because no λ makes them equal.', 'Different parameters must be used (λ and μ); the conclusion must come from solving for both.'),
          ('Two lines with non-parallel direction vectors must intersect.', 'Only in 2D; in 3D they may be skew.')],
))


def _two_lines(rng, kind):
    d1 = rv(rng, -3, 3)
    if kind == 'par':
        d2 = rng.choice([2, -1, -2, 3]) * d1
    else:
        while True:
            d2 = rv(rng, -3, 3)
            if crossv(d1, d2) != sp.zeros(3, 1):
                break
    Pp = rv(rng, -4, 4)
    s0, t0 = nz(rng, -3, 3), nz(rng, -3, 3)
    a1 = Pp - s0 * d1
    a2 = Pp - t0 * d2
    if kind == 'skew':
        nrm = crossv(d1, d2)
        a2 = a2 + nrm / gcdv(nrm) * rng.choice([1, -1])
    if kind == 'par':
        a2 = a2 + rv(rng, -2, 2)
        if crossv(a2 - a1, d1) == sp.zeros(3, 1):
            return None
    return a1, d1, a2, d2, Pp, s0, t0


def classify(a1, d1, a2, d2):
    if crossv(d1, d2) == sp.zeros(3, 1):
        return ('coincident' if crossv(a2 - a1, d1) == sp.zeros(3, 1) else 'parallel'), None
    lam, mu = sp.symbols('lam mu')
    sol = sp.solve(list(a1 + lam * d1 - a2 - mu * d2), [lam, mu], dict=True)
    if not sol:
        return 'skew', None
    return 'intersecting', a1 + sol[0][lam] * d1


@R.add('ch04-st2', 'C3', (2, 4), 'short')
def lines_intersect(rng, slot):
    r_ = _two_lines(rng, 'int')
    if not r_:
        return None
    a1, d1, a2, d2, Pp, s0, t0 = r_
    kind, pnt = classify(a1, d1, a2, d2)
    if kind != 'intersecting':
        return None
    return mk(f'The lines L₁: {line_txt(a1, d1)} and L₂: {line_txt(a2, d2, "μ")} intersect. Find the coordinates of the point of intersection.', pt(pnt),
              f'Equate components (M1); solve two equations simultaneously (M1): λ = {s0}, μ = {t0} (A1); check the third equation (R1); point {pt(pnt)} (A1).', 5)


@R.add('ch04-st2', 'C3', (2, 5), 'short')
def lines_classify(rng, slot):
    kind = rng.choice(['int', 'skew', 'par'])
    r_ = _two_lines(rng, kind)
    if not r_:
        return None
    a1, d1, a2, d2, Pp, s0, t0 = r_
    k2, pnt = classify(a1, d1, a2, d2)
    ans = {'intersecting': f'intersecting at {pt(pnt) if pnt is not None else ""}', 'skew': 'skew', 'parallel': 'parallel (distinct)', 'coincident': 'coincident'}[k2]
    return mk(f'Determine whether the lines L₁: {line_txt(a1, d1)} and L₂: {line_txt(a2, d2, "μ")} are parallel, intersecting or skew. Justify your answer.', ans,
              f'Compare direction vectors: {"multiples" if k2 in ("parallel", "coincident") else "not multiples, so not parallel"} (R1); ' +
              ('equate components and solve for λ, μ (M1 A1); third equation ' + ('satisfied (R1) – intersect at ' + pt(pnt) if k2 == 'intersecting' else 'not satisfied (R1) – skew') if k2 in ('intersecting', 'skew') else 'a point of L₂ is not on L₁ (M1 R1)') + f' (A1). Conclusion: {ans}.', 5)


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step', style='ext')
def lines_find_p(rng, slot):
    r_ = _two_lines(rng, 'int')
    if not r_:
        return None
    a1, d1, a2, d2, Pp, s0, t0 = r_
    i = rng.randint(0, 2)
    a2t = [P(c) for c in a2]
    a2t[i] = 'p'
    cosv = abs(dot(d1, d2)) / (mag(d1) * mag(d2))
    return mk(f'The lines L₁: {line_txt(a1, d1)} and L₂: r = ({", ".join(a2t)}) + μ{V(d2)} intersect at the point Q.\n(a) Find the value of p.\n(b) Find the coordinates of Q.\n(c) Find the acute angle between L₁ and L₂, in degrees.',
              f'(a) p = {P(a2[i])} (b) Q{pt(Pp)} (c) {s3(deg_of(cosv))}°',
              f'(a) Equate components (M1); use the two equations without p to find λ = {s0}, μ = {t0} (M1 A1); substitute into the third: p = {P(a2[i])} (A1). (b) Q = {pt(Pp)} (A1). (c) direction vectors (M1); |d₁·d₂| = {abs(dot(d1, d2))} (A1); {s3(deg_of(cosv))}° (A1).', 8)


@R.add('ch04-st2', 'C2', (2, 4), 'explain')
def lines_explain_skew(rng, slot):
    r_ = _two_lines(rng, 'skew')
    if not r_:
        return None
    a1, d1, a2, d2, *_ = r_
    k2, _p = classify(a1, d1, a2, d2)
    if k2 != 'skew':
        return None
    return mk(f'{who(rng)} says that L₁: {line_txt(a1, d1)} and L₂: {line_txt(a2, d2, "μ")} must meet because their direction vectors are not parallel. Explain why this reasoning is wrong for lines in 3D, and show that these lines are in fact skew.', 'skew',
              'In 3D non-parallel lines need not meet (R1); equate components and solve two equations for λ and μ (M1); the third equation is not satisfied (A1); so the lines are skew (R1).', 4, 'explain', 'G2')


@R.add('ch04-st2', 'C1', (1, 3), 'mcq')
def lines_rel_mcq(rng, slot):
    d1 = rv(rng, -3, 3)
    kk = rng.choice([2, -2, 3, -1])
    a = rv(rng, -4, 4)
    return mcq(rng, f'The lines r = {V(a)} + λ{V(d1)} and r = {V(a + sp.Matrix([1, 0, 0]))} + μ{V(kk * d1)} are', 'parallel', ['skew', 'perpendicular', 'intersecting at one point'],
               f'The direction vectors are multiples ({V(kk * d1)} = {kk}{V(d1)}), and the lines have different positions, so they are parallel.')


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st3', F(
    terms=[('vector product', 'v × w, the vector perpendicular to both v and w with magnitude |v||w| sin θ and direction given by the right-hand rule'),
           ('right-hand rule', 'the convention fixing the direction of v × w: v, w and v × w form a right-handed set'),
           ('area of a parallelogram (vectors)', '|v × w|, where v and w are adjacent sides')],
    facts=[('What is i × j?', 'k', ['−k', 'i', '0'], 'i, j, k form a right-handed set.'),
           ('For any vectors v and w, w × v equals', '−(v × w)', ['v × w', '0', 'v·w'], 'The vector product is anti-commutative.'),
           ('If v × w = 0 for non-zero v and w, then v and w are', 'parallel', ['perpendicular', 'unit vectors', 'equal in magnitude'], '|v × w| = |v||w| sin θ = 0 means θ = 0 or π.'),
           ('The area of triangle ABC is', '½|AB × AC|', ['|AB × AC|', '½ AB·AC', '|AB||AC|'], 'Half the parallelogram on AB and AC.')],
    why=[('Explain why v × w is perpendicular to both v and w.', 'Computing (v × w)·v and (v × w)·w gives zero by the determinant formula (each expansion has two equal rows), so the vector product is perpendicular to each.'),
         ('Explain why v × v = 0.', '|v × v| = |v||v| sin 0 = 0, so the vector product of a vector with itself is the zero vector.'),
         ('Explain why |v × w| gives the area of the parallelogram with sides v and w.', 'Area = base × height = |v| × |w| sin θ, which is exactly |v × w|.')],
    misc=[('(1, 0, 0) × (0, 1, 0) = (0, 0, 0) because the components multiply to zero.', 'The vector product is not component-wise multiplication; i × j = k = (0, 0, 1).'),
          ('v × w = w × v.', 'v × w = −(w × v): swapping the order reverses the direction.')],
))


@R.add('ch04-st3', 'C3', (1, 3), 'short')
def cross_compute(rng, slot):
    a, b = rv(rng, -5, 5), rv(rng, -5, 5)
    c = crossv(a, b)
    return mk(f'Given a = {ijk(a)} and b = {ijk(b)}, find a × b.', ijk(c) if c != sp.zeros(3, 1) else '0',
              f'Determinant set-up (M1); i: ({a[1]})({b[2]}) − ({a[2]})({b[1]}) = {c[0]}, j: −[({a[0]})({b[2]}) − ({a[2]})({b[0]})] = {c[1]}, k: ({a[0]})({b[1]}) − ({a[1]})({b[0]}) = {c[2]} (A1 A1 A1).', 4)


@R.add('ch04-st3', 'C1', (1, 3), 'mcq')
def cross_mcq(rng, slot):
    a, b = rv(rng, -4, 4), rv(rng, -4, 4)
    c = crossv(a, b)
    if c == sp.zeros(3, 1):
        return None
    return mcq(rng, f'Find {V(a)} × {V(b)}.', V(c), [V(-c), V(sp.Matrix([a[i] * b[i] for i in range(3)])), V(c + sp.Matrix([0, 2, 0]))],
               f'Using the determinant: {V(c)}. Note that b × a = {V(-c)}.')


@R.add('ch04-st3', 'C3', (2, 4), 'short', style='p1')
def cross_area(rng, slot):
    A, B, C = rv(rng, -4, 5), rv(rng, -4, 5), rv(rng, -4, 5)
    c = crossv(B - A, C - A)
    if c == sp.zeros(3, 1):
        return None
    shape = rng.choice(['triangle ABC', 'parallelogram with adjacent sides AB and AC'])
    area = sp.radsimp(mag(c) / (2 if shape.startswith('tri') else 1))
    return mk(f'The points A{pt(A)}, B{pt(B)} and C{pt(C)} are given. Find the exact area of the {shape}.', P(area),
              f'AB = {V(B - A)}, AC = {V(C - A)} (A1); AB × AC = {V(c)} (M1 A1); area = {"½" if shape.startswith("tri") else ""}|AB × AC| = {P(area)} (A1).', 4)


@R.add('ch04-st3', 'C3', (2, 4), 'short', style='p1')
def cross_unit_perp(rng, slot):
    a, b = rv(rng, -4, 4), rv(rng, -4, 4)
    c = crossv(a, b)
    if c == sp.zeros(3, 1):
        return None
    g = gcdv(c)
    c = c / g
    u = sp.Matrix([sp.radsimp(z / mag(c)) for z in c])
    return mk(f'Find a unit vector perpendicular to both {V(a)} and {V(b)}.', f'±{V(u)}',
              f'Vector product {V(c * g)} (M1 A1); simplify/scale (direction {V(c)}); divide by magnitude {P(mag(c))} (M1); ±{V(u)} (A1).', 4)


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def cross_explain(rng, slot):
    a = rv(rng, -4, 4)
    kk = rng.choice([2, -3, 4, -2])
    b = kk * a
    kind = rng.choice([1, 2])
    if kind == 1:
        return mk(f'Without computing it fully, explain why {V(a)} × {V(b)} = 0.', '0', f'{V(b)} = {kk}{V(a)} so the vectors are parallel (R1); θ = 0 or π so |a × b| = |a||b| sin θ = 0 (R1); the zero vector (A1).', 3, 'explain')
    c = rv(rng, -4, 4)
    d = crossv(a, c)
    if d == sp.zeros(3, 1):
        return None
    return mk(f'Given a × b = {V(d)}, explain why b × a = {V(-d)} and why a·(a × b) = 0.', f'b × a = {V(-d)}; a·(a × b) = 0',
              'Anti-commutativity / right-hand rule: swapping the order reverses direction (R1); a × b is perpendicular to a (R1), so its scalar product with a is 0 (A1).', 3, 'explain')


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step', style='ext')
def cross_triangle_height(rng, slot):
    A, B, C = rv(rng, -4, 5), rv(rng, -4, 5), rv(rng, -4, 5)
    AB, AC = B - A, C - A
    c = crossv(AB, AC)
    if c == sp.zeros(3, 1):
        return None
    area = sp.radsimp(mag(c) / 2)
    h = sp.radsimp(2 * area / mag(AB))
    sinA = sp.radsimp(mag(c) / (mag(AB) * mag(AC)))
    return mk(f'The points A{pt(A)}, B{pt(B)} and C{pt(C)} are vertices of a triangle.\n(a) Find AB × AC.\n(b) Hence find the exact area of triangle ABC.\n(c) Find the exact perpendicular distance from C to the line AB.\n(d) Find sin(BAC) exactly and verify it with the scalar product.',
              f'(a) {V(c)} (b) {P(area)} (c) {P(h)} (d) {P(sinA)}',
              f'(a) AB = {V(AB)}, AC = {V(AC)} (A1); {V(c)} (M1 A1). (b) ½|AB × AC| = {P(area)} (M1 A1). (c) area = ½|AB|h (M1) so h = {P(h)} (A1). (d) |AB × AC|/(|AB||AC|) (M1) = {P(sinA)} (A1); cos² + sin² = 1 check (R1).', 10)


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st4', F(
    terms=[('normal vector to a plane', 'a non-zero vector perpendicular to every line in the plane'),
           ('vector equation of a plane', 'r = a + λb + μc, where a is a point in the plane and b, c are non-parallel vectors in the plane'),
           ('scalar product form of a plane', 'r·n = a·n, where n is a normal vector and a a point in the plane'),
           ('Cartesian equation of a plane', 'ax + by + cz = d, where (a, b, c) is a normal vector')],
    facts=[('A normal vector to the plane 3x − y + 2z = 7 is', '(3, −1, 2)', ['(3, −1, 7)', '(1, 1, 1)', '(7, 0, 0)'], 'The coefficients of x, y, z give the normal.'),
           ('The plane through (1, 2, 3) with normal (2, 0, −1) has equation', '2x − z = −1', ['2x − z = 1', 'x + 2y + 3z = 1', '2x − z = 5'], '2(1) − 3 = −1.'),
           ('A normal to the plane r = a + λb + μc is', 'b × c', ['b·c', 'a × b', 'a + b + c'], 'b × c is perpendicular to both directions in the plane.')],
    why=[('Explain why r·n = a·n describes a plane.', 'For any point R in the plane, AR = r − a lies in the plane so is perpendicular to n: (r − a)·n = 0, i.e. r·n = a·n.'),
         ('Explain why three collinear points do not determine a unique plane.', 'Infinitely many planes contain a given line, so collinear points do not fix the orientation; three non-collinear points are needed.'),
         ('Explain why the vector product is useful for finding the equation of a plane through three points.', 'The two vectors AB and AC lie in the plane; their vector product is perpendicular to both, so it is a normal to the plane.')],
    misc=[('The plane 2x + 3y − z = 4 has normal vector (2, 3, 4).', 'The constant 4 is not part of the normal; n = (2, 3, −1).'),
          ('Planes 2x + y − z = 3 and 4x + 2y − 2z = 5 intersect in a line.', 'Their normals are parallel (one is twice the other), so the planes are parallel and do not meet.')],
))


def plane_txt(n, dval):
    terms = []
    for c, v in zip(n, 'xyz'):
        if c == 0:
            continue
        mag_ = abs(c)
        body = ('' if mag_ == 1 else P(mag_)) + v
        terms.append(('−' if c < 0 else '+', body))
    s = ('−' if terms[0][0] == '−' else '') + terms[0][1]
    for sg, b in terms[1:]:
        s += f' {sg} {b}'
    return f'{s} = {P(dval)}'


@R.add('ch04-st4', 'C3', (2, 4), 'short')
def plane_three_points(rng, slot):
    A, B, C = rv(rng, -4, 4), rv(rng, -4, 4), rv(rng, -4, 4)
    n = crossv(B - A, C - A)
    if n == sp.zeros(3, 1):
        return None
    g = gcdv(n)
    n = n / g
    if n[[i for i in range(3) if n[i] != 0][0]] < 0:
        n = -n
    dval = dot(n, A)
    return mk(f'Find the Cartesian equation of the plane containing the points A{pt(A)}, B{pt(B)} and C{pt(C)}.', plane_txt(n, dval),
              f'Two vectors in the plane AB = {V(B - A)}, AC = {V(C - A)} (A1); normal AB × AC ∝ {V(n)} (M1 A1); substitute A: d = {dval} (M1); {plane_txt(n, dval)} (A1).', 5)


@R.add('ch04-st4', 'C1', (1, 3), 'short')
def plane_point_normal(rng, slot):
    A, n = rv(rng, -5, 5), rv(rng, -5, 5)
    dval = dot(n, A)
    return mk(f'Find the Cartesian equation of the plane that passes through {pt(A)} and has normal vector {V(n)}.', plane_txt(n, dval),
              f'n·r = n·a (M1); {plane_txt(n, dval)} (A1).', 2)


@R.add('ch04-st4', 'C1', (1, 3), 'mcq')
def plane_normal_mcq(rng, slot):
    n = rv(rng, -5, 5)
    if 0 in list(n):
        return None
    dval = rng.randint(-9, 9)
    return mcq(rng, f'Which vector is normal to the plane {plane_txt(n, dval)}?', V(2 * n), [V(sp.Matrix([n[0], n[1], dval])), V(sp.Matrix([n[2], n[1], n[0]])), V(sp.Matrix([-n[0], n[1], n[2]]))],
               f'The normal is the coefficient vector {V(n)}, or any multiple such as {V(2 * n)}.')


@R.add('ch04-st4', 'C3', (2, 4), 'short')
def plane_vector_to_cart(rng, slot):
    a, b, c = rv(rng, -4, 4), rv(rng, -3, 3), rv(rng, -3, 3)
    n = crossv(b, c)
    if n == sp.zeros(3, 1):
        return None
    g = gcdv(n)
    n = n / g
    if n[[i for i in range(3) if n[i] != 0][0]] < 0:
        n = -n
    dval = dot(n, a)
    return mk(f'A plane has vector equation r = {V(a)} + λ{V(b)} + μ{V(c)}. Find its Cartesian equation.', plane_txt(n, dval),
              f'Normal = {V(b)} × {V(c)} (M1) ∝ {V(n)} (A1); d = n·{V(a)} = {dval} (M1); {plane_txt(n, dval)} (A1).', 4)


@R.add('ch04-st4', 'C2', (2, 4), 'explain')
def plane_check_point(rng, slot):
    n, A = rv(rng, -4, 4), rv(rng, -4, 4)
    dval = dot(n, A)
    Q = rv(rng, -4, 4)
    on = dot(n, Q) == dval
    return mk(f'Explain how to decide whether the point Q{pt(Q)} lies in the plane {plane_txt(n, dval)}, and give the conclusion.', 'lies in the plane' if on else 'does not lie in the plane',
              f'Substitute the coordinates of Q into the left-hand side (M1): {dot(n, Q)} (A1); compare with {dval} (R1): Q {"lies" if on else "does not lie"} in the plane.', 3, 'explain')


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step', style='ext')
def plane_multi(rng, slot):
    A, B, C = rv(rng, -3, 4), rv(rng, -3, 4), rv(rng, -3, 4)
    n = crossv(B - A, C - A)
    if n == sp.zeros(3, 1):
        return None
    g = gcdv(n)
    n = n / g
    dval = dot(n, A)
    D = rv(rng, -4, 4)
    kk = rng.randint(-6, 6)
    while kk == dval:
        kk += 1
    lam = sp.symbols('lam')
    # line through D perpendicular to plane, meet plane
    l0 = sp.solve(dot(n, D + lam * n) - dval, lam)[0]
    F_ = D + l0 * n
    dist = sp.radsimp(abs(l0) * mag(n))
    return mk(f'The plane Π contains the points A{pt(A)}, B{pt(B)} and C{pt(C)}.\n(a) Find a normal vector to Π.\n(b) Find the Cartesian equation of Π.\n(c) The point D has coordinates {pt(D)}. Write down a vector equation of the line through D perpendicular to Π.\n(d) Find the coordinates of the foot of the perpendicular from D to Π and the exact distance from D to Π.',
              f'(a) {V(n)} (b) {plane_txt(n, dval)} (c) r = {V(D)} + λ{V(n)} (d) {pt(F_)}, distance {P(dist)}',
              f'(a) AB × AC (M1 A1). (b) {plane_txt(n, dval)} (M1 A1). (c) direction = normal (A1). (d) substitute the line into Π (M1): λ = {P(l0)} (A1); foot {pt(F_)} (A1); distance |λ||n| = {P(dist)} (M1 A1).', 10)


# ---------------------------------------------------------------------------------------------
R.facts('ch04-st5', F(
    terms=[('angle between a line and a plane', 'the angle θ between the line and its projection on the plane; sin θ = |d·n|/(|d||n|)'),
           ('angle between two planes', 'the acute angle between their normals; cos θ = |n₁·n₂|/(|n₁||n₂|)'),
           ('line of intersection', 'the line common to two non-parallel planes; its direction is n₁ × n₂')],
    facts=[('To find the angle between a line with direction d and a plane with normal n, you use', 'sin θ = |d·n|/(|d||n|)', ['cos θ = |d·n|/(|d||n|)', 'tan θ = |d × n|', 'θ = d·n'], 'The angle with the normal is 90° − θ.'),
           ('Three planes whose normals are linearly independent meet in', 'a single point', ['a line', 'no point', 'a plane'], 'The 3 × 3 system has a unique solution.'),
           ('If a line is parallel to a plane, then d·n is', '0', ['1', '|d||n|', 'undefined'], 'The direction is perpendicular to the normal.')],
    why=[('Explain why sin is used rather than cos when finding the angle between a line and a plane.', 'The scalar product with the normal gives the angle φ between the line and the normal; the required angle is θ = 90° − φ, and cos φ = sin θ.'),
         ('Explain why the direction of the line of intersection of two planes is n₁ × n₂.', 'The line lies in both planes so it is perpendicular to both normals; n₁ × n₂ is perpendicular to both.'),
         ('Explain how to decide whether a line meets a plane, is parallel to it, or lies in it.', 'Compute d·n: if non-zero the line meets the plane in one point; if zero the line is parallel – it lies in the plane if a point of the line satisfies the plane equation, otherwise it never meets it.')],
    misc=[('The angle between the planes x + y = 1 and y + z = 2 is found from the cross product of their normals.', 'Use the scalar product of the normals: cos θ = |n₁·n₂|/(|n₁||n₂|) = 1/2, θ = 60°.'),
          ('If d·n = 0 then the line lies in the plane.', 'd·n = 0 means parallel; the line lies in the plane only if one of its points satisfies the plane equation.')],
))


@R.add('ch04-st5', 'C3', (2, 4), 'short')
def line_plane_meet(rng, slot):
    n = rv(rng, -4, 4)
    a, d = rv(rng, -4, 4), rv(rng, -3, 3)
    if dot(d, n) == 0:
        return None
    Q = rv(rng, -4, 4)
    dval = dot(n, Q)
    lam = sp.Rational(dval - dot(n, a), dot(n, d))
    Pp = a + lam * d
    return mk(f'Find the coordinates of the point where the line {line_txt(a, d)} meets the plane {plane_txt(n, dval)}.', pt(Pp),
              f'Substitute the parametric form into the plane (M1); {dot(n, a)} + ({dot(n, d)})λ = {dval} (A1); λ = {P(lam)} (A1); point {pt(Pp)} (A1).', 4)


@R.add('ch04-st5', 'C3', (2, 4), 'short', style='p2')
def line_plane_angle(rng, slot):
    n = rv(rng, -4, 4)
    a, d = rv(rng, -4, 4), rv(rng, -3, 3)
    sv = abs(dot(d, n)) / (mag(d) * mag(n))
    if sv == 0 or float(sv) > 0.999:
        return None
    dval = rng.randint(-8, 8)
    ang = math.degrees(math.asin(float(sv)))
    return mk(f'Find the acute angle between the line {line_txt(a, d)} and the plane {plane_txt(n, dval)}.', f'{s3(ang)}°',
              f'd·n = {dot(d, n)} (A1); |d| = {P(mag(d))}, |n| = {P(mag(n))} (A1); sin θ = |d·n|/(|d||n|) (M1); θ = {s3(ang)}° (A1).', 4)


@R.add('ch04-st5', 'C3', (2, 4), 'short', style='p2')
def plane_plane_angle(rng, slot):
    n1, n2 = rv(rng, -4, 4), rv(rng, -4, 4)
    c = abs(dot(n1, n2)) / (mag(n1) * mag(n2))
    if float(c) > 0.999:
        return None
    d1, d2 = rng.randint(-8, 8), rng.randint(-8, 8)
    return mk(f'Find the acute angle between the planes {plane_txt(n1, d1)} and {plane_txt(n2, d2)}.', f'{s3(deg_of(c))}°',
              f'Normals {V(n1)} and {V(n2)} (A1); |n₁·n₂| = {abs(dot(n1, n2))} (A1); cos θ = |n₁·n₂|/(|n₁||n₂|) (M1); θ = {s3(deg_of(c))}° (A1).', 4)


@R.add('ch04-st5', 'C4', (3, 5), 'multi_step', style='ext')
def planes_line(rng, slot):
    n1, n2 = rv(rng, -3, 3), rv(rng, -3, 3)
    dirv = crossv(n1, n2)
    if dirv == sp.zeros(3, 1):
        return None
    Pp = rv(rng, -3, 3)
    d1, d2 = dot(n1, Pp), dot(n2, Pp)
    # point with z = 0 if possible
    xx, yy, zz = sp.symbols('xx yy zz')
    for fix in ('z', 'y', 'x'):
        eqs = [n1[0] * xx + n1[1] * yy + n1[2] * zz - d1, n2[0] * xx + n2[1] * yy + n2[2] * zz - d2]
        sub = {'z': {zz: 0}, 'y': {yy: 0}, 'x': {xx: 0}}[fix]
        sol = sp.solve([e.subs(sub) for e in eqs], [v for v in (xx, yy, zz) if v not in sub], dict=True)
        if sol and all(v in sol[0] or v in sub for v in (xx, yy, zz)):
            sol = sol[0]
            sol.update(sub)
            Q = sp.Matrix([sol[xx], sol[yy], sol[zz]])
            break
    else:
        return None
    g = gcdv(dirv)
    dirv = dirv / g
    c = abs(dot(n1, n2)) / (mag(n1) * mag(n2))
    return mk(f'The planes Π₁: {plane_txt(n1, d1)} and Π₂: {plane_txt(n2, d2)} intersect in the line L.\n(a) Show that the direction of L is parallel to {V(dirv)}.\n(b) Find a vector equation of L.\n(c) Find the acute angle between Π₁ and Π₂.',
              f'(a) n₁ × n₂ ∝ {V(dirv)} (b) r = {V(Q)} + λ{V(dirv)} (c) {s3(deg_of(c))}°',
              f'(a) n₁ × n₂ (M1) = {V(dirv * g)} (A1) AG. (b) find a point on both planes, e.g. setting one coordinate to 0 (M1): {pt(Q)} (A1); r = {V(Q)} + λ{V(dirv)} (A1). (c) cos θ = |n₁·n₂|/(|n₁||n₂|) (M1) = {s3(float(c))} (A1); θ = {s3(deg_of(c))}° (A1).', 8)


@R.add('ch04-st5', 'C4', (3, 5), 'multi_step', style='p3')
def three_planes(rng, slot):
    while True:
        M = sp.Matrix([[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)])
        if M.det() != 0 and all(any(M[i, j] for j in range(3)) for i in range(3)):
            break
    Pp = rv(rng, -4, 4, nonzero=False)
    rhs = M * Pp
    planes = [plane_txt(M.row(i).T, rhs[i]) for i in range(3)]
    return mk(f'Find the coordinates of the point of intersection of the three planes\nΠ₁: {planes[0]}\nΠ₂: {planes[1]}\nΠ₃: {planes[2]}\nand explain why the three planes meet in exactly one point.',
              f'{pt(Pp)}; the determinant of the coefficient matrix is {M.det()} ≠ 0 (normals not coplanar), so the solution is unique',
              f'Eliminate one variable from two pairs (M1 M1); solve the 2 × 2 system (A1 A1); back-substitute (A1): {pt(Pp)}. Reasoning: the normals are not coplanar / determinant {M.det()} ≠ 0 so a unique solution (R1 R1).', 7)


@R.add('ch04-st5', 'C2', (2, 4), 'explain')
def line_plane_parallel_explain(rng, slot):
    n = rv(rng, -4, 4)
    d = rv(rng, -3, 3)
    d = d - (dot(d, n) / dot(n, n)) * n
    d = d * sp.ilcm(*[sp.fraction(c)[1] for c in d])
    if d == sp.zeros(3, 1) or max(abs(c) for c in d) > 15:
        return None
    a = rv(rng, -4, 4)
    dval = dot(n, a) + rng.choice([0, 3, -2])
    lies = dot(n, a) == dval
    return mk(f'Explain why the line {line_txt(a, d)} does not meet the plane {plane_txt(n, dval)} in a single point, and state whether it lies in the plane.', 'lies in the plane' if lies else 'parallel to the plane, never meets it',
              f'd·n = {dot(d, n)} = 0 so the line is parallel to the plane (M1 R1); test the point {pt(a)}: {dot(n, a)} {"=" if lies else "≠"} {dval} (A1); so the line {"lies in the plane" if lies else "never meets the plane"} (R1).', 4, 'explain')


@R.add('ch04-st5', 'C1', (1, 3), 'mcq')
def line_plane_mcq(rng, slot):
    n = rv(rng, -3, 3)
    kk = rng.choice([1, 2, -1, 3])
    return mcq(rng, f'The line r = (1, 0, 2) + λ{V(kk * n)} and the plane {plane_txt(n, rng.randint(-5, 5))} are', 'perpendicular', ['parallel', 'at an angle of 45°', 'coincident'],
               'The direction of the line is a multiple of the normal to the plane, so the line is perpendicular to the plane.')


@R.add('ch04-st5', 'C3', (2, 4), 'short', style='p1')
def point_plane_distance(rng, slot):
    n = rv(rng, -4, 4)
    Q = rv(rng, -5, 5)
    dval = rng.randint(-9, 9)
    dist = sp.radsimp(abs(dot(n, Q) - dval) / mag(n))
    return mk(f'Find the exact shortest distance from the point {pt(Q)} to the plane {plane_txt(n, dval)}.', P(dist),
              f'Line through the point along the normal, meet the plane (M1), or |n·q − d|/|n| (M1); |{dot(n, Q)} − ({dval})| = {abs(dot(n, Q) - dval)} (A1); |n| = {P(mag(n))}; distance {P(dist)} (A1).', 4)


# =============================================================================================
# ch05 Limits and introduction to differentiation
# =============================================================================================
def term_txt(a, n, v='x'):
    """IB-friendly text for a·x^n with rational n (roots and fractions written out)."""
    a, n = sp.nsimplify(a), sp.nsimplify(n)
    sign = '−' if a < 0 else ''
    A = abs(a)
    coef = '' if A == 1 else P(A)
    if n == 0:
        return sign + P(A)
    if n == 1:
        return f'{sign}{coef}{v}'
    if n.is_Integer and n > 0:
        return f'{sign}{coef}{v}{str(n).translate(_SUP)}'
    if n == sp.Rational(1, 2):
        return f'{sign}{coef}√{v}'
    if n == sp.Rational(1, 3):
        return f'{sign}{coef}∛{v}'
    if n == -1:
        return f'{sign}{P(A)}/{v}'
    if n.is_Integer and n < 0:
        return f'{sign}{P(A)}/{v}{str(-n).translate(_SUP)}'
    if n == -sp.Rational(1, 2):
        return f'{sign}{P(A)}/√{v}'
    if n == sp.Rational(3, 2):
        return f'{sign}{coef}{v}√{v}'
    return f'{sign}{coef}{v}^({P(n)})'


def sum_txt(terms, v='x'):
    s = ''
    for a, n in terms:
        tt = term_txt(a, n, v)
        if not s:
            s = tt
        else:
            s += (' − ' + tt[1:]) if tt.startswith('−') else (' + ' + tt)
    return s


def sum_expr(terms, v=x):
    return sum(sp.nsimplify(a) * v ** sp.nsimplify(n) for a, n in terms)


def line_eq(m, c):
    m, c = sp.nsimplify(m), sp.nsimplify(c)
    if isinstance(m, sp.Add):
        s_ = f'({P(m)})x'
        if c != 0:
            s_ += f' − {P(-c)}' if (c.is_number and c < 0) else f' + {P(c)}'
        return 'y = ' + s_
    return 'y = ' + P(sp.expand(m * x + c))


POW_N = [2, 3, 4, -1, -2, sp.Rational(1, 2), -sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(1, 3), 5]


def rand_terms(rng, k, allow_frac=True):
    ns = rng.sample(POW_N if allow_frac else [1, 2, 3, 4, 5], k)
    return [(nz(rng, -6, 8), n) for n in ns]


R.facts('ch05-st1', F(
    terms=[('limit', 'the value that f(x) approaches as x approaches a, written lim(x→a) f(x); it may exist even if f(a) is undefined'),
           ('derivative', "f′(x) = lim(h→0) (f(x + h) − f(x))/h, the gradient of the tangent to y = f(x) and the instantaneous rate of change"),
           ('gradient of a chord', 'the average rate of change (f(b) − f(a))/(b − a) between two points on a curve'),
           ('tangent', 'the line that touches a curve at a point and has the same gradient as the curve there')],
    facts=[('As the point Q moves along a curve towards P, the gradient of chord PQ approaches', 'the gradient of the tangent at P', ['zero', 'the gradient of the normal at P', 'the y-coordinate of P'], 'This limiting process defines the derivative.'),
           ('If s(t) is displacement in metres and t is time in seconds, the units of s′(t) are', 'm s⁻¹', ['m', 's m⁻¹', 'm s⁻²'], 'A derivative is a rate: units of s per unit of t.'),
           ('What is lim(x→2) (x² − 4)/(x − 2)?', '4', ['0', 'undefined', '2'], 'Factorise: (x − 2)(x + 2)/(x − 2) = x + 2 → 4.'),
           ('Which notation means the derivative of y with respect to x?', 'dy/dx', ['Δy', 'y/x', '∫y dx'], 'dy/dx is Leibniz notation for the derivative.')],
    why=[('Explain why the gradient of a curve at a point cannot be found directly from the gradient formula (y₂ − y₁)/(x₂ − x₁).', 'The formula needs two distinct points; at a single point it gives 0/0, so we take the limit of chord gradients as the second point approaches the first.'),
         ('Explain the difference between an average rate of change and an instantaneous rate of change.', 'The average rate is the gradient of a chord over an interval; the instantaneous rate is the gradient of the tangent at one point, the limit of average rates as the interval shrinks to zero.'),
         ('Explain why lim(x→3) (x² − 9)/(x − 3) exists even though the expression is undefined at x = 3.', 'For x ≠ 3 it simplifies to x + 3, whose values approach 6 as x → 3; the limit depends on nearby values, not on the value at 3.')],
    misc=[('If f(a) is undefined then lim(x→a) f(x) cannot exist.', 'A limit depends only on values near a; e.g. (x² − 1)/(x − 1) is undefined at 1 but tends to 2.'),
          ('f′(2) = 5 means f(2) = 5.', 'f′(2) = 5 is the gradient (rate of change) of f at x = 2, not its value.')],
))


@R.add('ch05-st1', 'C1', (1, 3), 'mcq', style='p1')
def limit_factor_mcq(rng, slot):
    a = nz(rng, -5, 6)
    kind = rng.choice(['sq', 'cube', 'quad'])
    if kind == 'sq':
        e = (x ** 2 - a ** 2) / (x - a)
        txt = f'({P(x ** 2 - a ** 2)})/({P(x - a)})'
    elif kind == 'cube':
        e = (x ** 3 - a ** 3) / (x - a)
        txt = f'({P(x ** 3 - a ** 3)})/({P(x - a)})'
    else:
        b = nz(rng, -5, 5)
        e = sp.expand((x - a) * (x + b)) / (x - a)
        txt = f'({P(sp.expand((x - a) * (x + b)))})/({P(x - a)})'
    L = sp.limit(e, x, a)
    return mcq(rng, f'Find lim(x→{P(a)}) {txt}.', P(L), ['0', 'undefined', P(L + 1), P(-L) if L != 0 else '1', P(2 * L) if L != 0 else '2'],
               f'Factorise and cancel (x − {P(a)}), then substitute x = {P(a)}: {P(L)}.')


@R.add('ch05-st1', 'C3', (1, 4), 'short', style='p2')
def chord_table(rng, slot):
    f_terms = rand_terms(rng, 2, allow_frac=False)
    f = sum_expr(f_terms)
    a = rng.randint(-2, 4)
    hs = [0.1, 0.01, 0.001]
    vals = [float((f.subs(x, a + h) - f.subs(x, a)) / h) for h in hs]
    der = sp.diff(f, x).subs(x, a)
    return mk(f'For f(x) = {sum_txt(f_terms)}, the point P has x-coordinate {a} and Q has x-coordinate {a} + h. Find the gradient of the chord PQ for h = 0.1, 0.01 and 0.001, and hence suggest the value of f′({a}).',
              f'{", ".join(f"{v:.4f}" for v in vals)}; f′({a}) = {P(der)}'.replace('-', '−'),
              f'(f({a} + h) − f({a}))/h (M1) for each h: {", ".join(f"{v:.4f}" for v in vals)} (A1 A1); the values approach {P(der)} (R1).', 4)


@R.add('ch05-st1', 'C3', (2, 4), 'short', style='p1')
def limit_rational(rng, slot):
    a = nz(rng, -4, 4)
    b, c = nz(rng, -5, 5), nz(rng, -5, 5)
    if b == a or c == a:
        return None
    num = sp.expand((x - a) * (x - b))
    den = sp.expand((x - a) * (x - c))
    L = sp.limit(num / den, x, a)
    return mk(f'Find lim(x→{P(a)}) ({P(num)})/({P(den)}).', P(L),
              f'Both numerator and denominator are 0 at x = {P(a)} (R1); factorise: (x − {P(a)})(x − ({b}))/((x − {P(a)})(x − ({c}))) (M1 A1); cancel and substitute: {P(L)} (A1).', 4)


@R.add('ch05-st1', 'C2', (2, 4), 'explain')
def rate_interpret(rng, slot):
    ctx = rng.choice([('V(t)', 'the volume of water in a tank, in litres', 't minutes', 'litres per minute', 'the water is flowing in'),
                      ('P(t)', 'the population of bacteria in a culture, in thousands', 't hours', 'thousand bacteria per hour', 'the population is growing'),
                      ('C(n)', 'the cost, in euros, of producing n items', 'n items', 'euros per item', 'the cost is increasing'),
                      ('T(t)', 'the temperature of a cup of coffee, in °C', 't minutes', '°C per minute', 'the coffee is warming'),
                      ('h(t)', 'the height of a rocket, in metres', 't seconds', 'metres per second', 'the rocket is rising')])
    a = rng.randint(2, 20)
    val = rng.choice([-1, 1]) * rng.randint(2, 40)
    fn, desc, var, unit, posmeaning = ctx
    return mk(f'{fn} is {desc}, after {var}. Interpret the statement {fn[0]}′({a}) = {val} in context, including units.'.replace('-', '−'),
              f'At {var.split()[0]} = {a}, {fn[0]} is {"increasing" if val > 0 else "decreasing"} at a rate of {abs(val)} {unit}.',
              f'Instantaneous rate of change at {var.split()[0]} = {a} (R1); {"increasing" if val > 0 else "decreasing"} (A1); magnitude {abs(val)} with units {unit} (A1).', 3, 'explain')


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step', style='ext')
def chord_to_tangent(rng, slot):
    a_, b_ = nz(rng, -3, 3), nz(rng, -5, 5)
    p = rng.randint(-3, 3)
    h = sp.Symbol('h')
    f = a_ * x ** 3 + b_ * x
    grad = sp.expand(sp.cancel((f.subs(x, p + h) - f.subs(x, p)) / h))
    der = grad.subs(h, 0)
    yp = f.subs(x, p)
    return mk(f'Let f(x) = {P(f)}. The points P and Q on the graph of f have x-coordinates {p} and {p} + h respectively.\n(a) Show that the gradient of the chord PQ is {P(grad)}.\n(b) Hence find f′({p}), explaining your reasoning.\n(c) Find the equation of the tangent to the graph at P.',
              f'(a) shown (b) {P(der)} (c) {line_eq(der, yp - der * p)}',
              f'(a) f({p} + h) expanded (M1 A1); subtract f({p}) = {yp} and divide by h (M1) AG. (b) as h → 0 the chord gradient → {P(der)} (R1 A1). (c) y − {yp} = {P(der)}(x − {p}) (M1) {line_eq(der, yp - der * p)} (A1).', 8)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st2', F(
    terms=[('increasing function', 'f is increasing on an interval if f′(x) ≥ 0 there (strictly increasing if f′(x) > 0)'),
           ('decreasing function', 'f is decreasing on an interval if f′(x) ≤ 0 there (strictly decreasing if f′(x) < 0)'),
           ('stationary point', 'a point where f′(x) = 0, so the tangent is horizontal')],
    facts=[("If f′(x) < 0 for 1 < x < 4, then on that interval f is", 'decreasing', ['increasing', 'concave down', 'negative'], 'A negative gradient means the function is decreasing.'),
           ("The graph of y = f′(x) crosses the x-axis from positive to negative at x = 3. At x = 3, f has", 'a local maximum', ['a local minimum', 'a point of inflection', 'a root'], 'f changes from increasing to decreasing.'),
           ("Which function is increasing for all real x?", 'f(x) = x³ + 2x', ['f(x) = x² + 2x', 'f(x) = x³ − 2x', 'f(x) = −x³'], "f′(x) = 3x² + 2 > 0 for all x.")],
    why=[("Explain why f(x) = x³ + kx is increasing for all x when k > 0.", "f′(x) = 3x² + k, and 3x² ≥ 0 so f′(x) ≥ k > 0 for every x."),
         ("Explain how the graph of y = f′(x) shows where f is increasing.", "f is increasing exactly where f′(x) > 0, i.e. where the graph of y = f′(x) lies above the x-axis."),
         ("Explain why f(x) = 1/x is decreasing on each of its intervals but f(−1) < f(1).", "f′(x) = −1/x² < 0 on (−∞, 0) and on (0, ∞) separately; the function is not defined at 0, so 'decreasing' does not compare values across the asymptote.")],
    misc=[("If f′(2) = 0 then f has a maximum or a minimum at x = 2.", "Not necessarily: f(x) = x³ has f′(0) = 0 but a stationary point of inflection; the sign of f′ must change."),
          ("If f(x) is positive then f is increasing.", "The sign of f says nothing about its gradient; increasing depends on the sign of f′(x).")],
))


def _cubic_from_roots(rng):
    p, q = sorted(rng.sample(range(-4, 6), 2))
    kk = rng.choice([6, -6, 3, -3]) if (p + q) % 2 == 0 else rng.choice([6, -6])
    c = rng.randint(-8, 8)
    f = sp.expand(kk * (x ** 3 / 3 - (p + q) * x ** 2 / 2 + p * q * x) + c)
    return f, p, q, kk


@R.add('ch05-st2', 'C3', (2, 4), 'short', style='p1')
def inc_dec_intervals(rng, slot):
    f, p, q, kk = _cubic_from_roots(rng)
    inc = f'x < {p} or x > {q}' if kk > 0 else f'{p} < x < {q}'
    dec = f'{p} < x < {q}' if kk > 0 else f'x < {p} or x > {q}'
    want = rng.choice(['increasing', 'decreasing'])
    return mk(f'Find the set of values of x for which f(x) = {P(f)} is {want}.'.replace('-', '−'), (inc if want == 'increasing' else dec).replace('-', '−'),
              f"f′(x) = {P(sp.diff(f, x))} (A1) = {kk}(x − {p})(x − {q}) (M1); f′(x) {'>' if want == 'increasing' else '<'} 0 (M1); {(inc if want == 'increasing' else dec)} (A1).".replace('-', '−').replace('− −', '+ '), 4)


@R.add('ch05-st2', 'C3', (3, 5), 'short', style='p1')
def inc_all_k(rng, slot):
    b = nz(rng, -6, 6)
    kc = sp.Rational(b * b, 3)
    return mk(f'The function f(x) = x³ {"+" if b > 0 else "−"} {abs(b)}x² + kx + 1 is increasing for all real x. Find the set of possible values of k.',
              f'k ≥ {P(kc)}', f"f′(x) = 3x² {'+' if b > 0 else '−'} {abs(2 * b)}x + k ≥ 0 for all x (M1); discriminant ≤ 0 (M1): {4 * b * b} − 12k ≤ 0 (A1); k ≥ {P(kc)} (A1).", 4)


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def inc_explain_value(rng, slot):
    f, p, q, kk = _cubic_from_roots(rng)
    xv = rng.choice([p - 1, (p + q) / 2 if (p + q) % 2 == 0 else q + 1, q + 1])
    g = sp.diff(f, x).subs(x, xv)
    if g == 0:
        return None
    return mk(f'For f(x) = {P(f)}, determine whether f is increasing or decreasing at x = {P(xv)}, explaining your reasoning.', 'increasing' if g > 0 else 'decreasing',
              f"f′(x) = {P(sp.diff(f, x))} (A1); f′({P(xv)}) = {P(g)} (A1), which is {'positive' if g > 0 else 'negative'} so f is {'increasing' if g > 0 else 'decreasing'} (R1).", 3, 'explain')


@R.add('ch05-st2', 'C1', (1, 3), 'mcq')
def inc_mcq_graph(rng, slot):
    p, q = sorted(rng.sample(range(-5, 6), 2))
    return mcq(rng, f"The graph of y = f′(x) is a parabola that crosses the x-axis at x = {P(p)} and x = {P(q)} and is positive between them. On which interval is f decreasing?",
               f'x > {q}'.replace('-', '−'), [f'{p} < x < {q}'.replace('-', '−'), f'x > {p}'.replace('-', '−'), f'x < {q}'.replace('-', '−')],
               f"f is decreasing where f′(x) < 0, i.e. outside [{p}, {q}]; of the options only x > {q} lies there.")


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step', style='ext')
def inc_repeated_root(rng, slot):
    a, b = rng.sample(range(-3, 5), 2)
    kk = rng.choice([1, -1, 2, -2, 3])
    fp = kk * (x - a) * (x - b) ** 2
    c0 = rng.randint(-5, 5)
    f = sp.integrate(sp.expand(fp), x) + c0
    parts = [('Find the x-coordinates of the stationary points of f.', f'x = {P(a)}, x = {P(b)}', 'f′(x) = 0 (M1) A1 A1', 3, True),
             ('Determine the nature of each stationary point, justifying your answer.', f"x = {P(a)}: {'local minimum' if kk > 0 else 'local maximum'}; x = {P(b)}: stationary point of inflection",
              f"sign of f′ changes {'− to +' if kk > 0 else '+ to −'} at x = {P(a)} (R1 A1); (x − ({b}))² ≥ 0 so no sign change at x = {P(b)} (R1 A1)", 4, True),
             ('State the set of values of x for which f is increasing.', f"x > {P(a)}" if kk > 0 else f"x < {P(a)}", 'A1 (x = ' + P(b) + ' may be included)', 1, False),
             (f'Given that f(0) = {c0}, find f(x).', f'f(x) = {P(f)}', 'expand f′ and integrate term by term (M1) A1; constant from f(0) (A1)', 3, False),
             ('Find f″(x) and verify that f″ is zero at one of the stationary points.', f'f″(x) = {P(sp.expand(sp.diff(fp, x)))}; f″({P(b)}) = 0', 'differentiate (M1) A1; substitute (A1)', 3, False)]
    return build_parts(rng, [f"The derivative of a function f is given by f′(x) = {P(sp.factor(fp))}.", f"A function f has gradient function f′(x) = {P(sp.factor(fp))}.", f"For a function f, f′(x) = {P(sp.factor(fp))} for all real x."], parts, 3)


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step', style='p1')
def inc_find_coeffs(rng, slot):
    p, q = sorted(rng.sample(range(-4, 5), 2))
    if (p + q) % 2:
        q += 1
        if q == p:
            return None
    a, b = -sp.Rational(3 * (p + q), 2), 3 * p * q
    c = rng.randint(-6, 6)
    f = x ** 3 + a * x ** 2 + b * x + c
    parts = [(f'Find the values of a and b.', f'a = {P(a)}, b = {P(b)}', f"f′(x) = 3x² + 2ax + b (A1); f′({p}) = 0 and f′({q}) = 0 (M1); solve: a = {P(a)}, b = {P(b)} (A1 A1)", 4, True),
             ('Find the intervals on which f is decreasing.', f'{P(p)} < x < {P(q)}', f'f′(x) = 3(x − ({p}))(x − ({q})) < 0 (M1) A1', 2, True),
             (f'Given also that f(0) = {c}, find the coordinates of the local maximum point.', pt([p, f.subs(x, p)]), f'local maximum at the smaller root x = {p} (R1); y = {P(f.subs(x, p))} (A1)', 2, False),
             ('Explain why f has no other stationary points.', 'f′ is quadratic so it has at most two zeros', 'R1', 1, False)]
    return build_parts(rng, [f'The function f(x) = x³ + ax² + bx + c has stationary points at x = {P(p)} and x = {P(q)}.', f'The graph of y = x³ + ax² + bx + c has horizontal tangents where x = {P(p)} and x = {P(q)}.'], parts, 2)


@R.add('ch05-st2', 'C4', (3, 5), 'multi_step', style='p2')
def inc_gdc(rng, slot):
    a = round(rng.uniform(0.5, 2.5), 1)
    b = rng.randint(1, 4)
    kind = rng.choice(['exp', 'trig'])
    if kind == 'exp':
        f = x ** 2 * sp.exp(-a * x / b)
        txt = f'x²e^(−{a}x/{b})' if b > 1 else f'x²e^(−{a}x)'
    else:
        f = x * sp.sin(a * x) if False else sp.sin(x) + a * sp.cos(b * x)
        txt = f'sin x + {a} cos({b}x)' if b > 1 else f'sin x + {a} cos x'
    fp = sp.diff(f, x)
    g = sp.lambdify(x, fp, 'math')
    roots = nsols(g, 0, 6)
    if not roots or len(roots) > 6:
        return None
    parts = [('Find f′(x).', P(fp), 'product/chain rule as needed (M1) A1', 2, True),
             ('Use your GDC to find the x-coordinates of the stationary points of f for 0 ≤ x ≤ 6.', lst3(roots), 'solve f′(x) = 0 (M1) A1 A1', 3, True),
             ('Hence write down the intervals in [0, 6] on which f is increasing.', 'between the stationary points where f′ > 0 (check sign on the GDC graph)', 'R1 A1', 2, True)]
    return build_parts(rng, [f'Let f(x) = {txt}, for 0 ≤ x ≤ 6.', f'A function is defined by f(x) = {txt}, 0 ≤ x ≤ 6.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st3', F(
    terms=[('power rule', 'if f(x) = axⁿ then f′(x) = naxⁿ⁻¹, for any rational n'),
           ('derivative of a constant', 'zero, since the graph of y = c is horizontal')],
    facts=[('If f(x) = 6x^(2/3), then f′(x) =', '4x^(−1/3)', ['4x^(1/3)', '6x^(−1/3)', '9x^(5/3)'], '(2/3)(6)x^(2/3 − 1).'),
           ('What is the derivative of 5/x²?', '−10/x³', ['10/x³', '5/(2x)', '−5/x³'], '5x⁻² → −10x⁻³.'),
           ('What is dy/dx if y = 4√x?', '2/√x', ['2√x', '4/√x', '8√x'], '4x^(1/2) → 2x^(−1/2).'),
           ('The derivative of f(x) = 7 is', '0', ['7', '7x', '1'], 'Constants have zero gradient.')],
    why=[('Explain why expressions such as 3/√x should be rewritten before differentiating.', 'The power rule applies to terms axⁿ; 3/√x = 3x^(−1/2), which can then be differentiated to −(3/2)x^(−3/2).'),
         ('Explain why the derivative of f(x) + g(x) is f′(x) + g′(x).', 'The limit of a sum is the sum of the limits, so the difference quotient of f + g splits into the difference quotients of f and of g.'),
         ('Explain why you cannot differentiate (x² + 1)(x − 3) by multiplying the derivatives of the two brackets.', 'The derivative of a product is not the product of derivatives; expand first (or use the product rule): x³ − 3x² + x − 3 → 3x² − 6x + 1.')],
    misc=[('d/dx (1/x³) = 1/(3x²).', 'Write x⁻³: derivative −3x⁻⁴ = −3/x⁴.'),
          ('d/dx (√x) = √x/2.', '√x = x^(1/2) so the derivative is ½x^(−1/2) = 1/(2√x).'),
          ('d/dx (x²/4) = x²/2.', 'x²/4 = ¼x², derivative ½x.')],
))


@R.add('ch05-st3', 'C1', (1, 3), 'mcq')
def power_mcq(rng, slot):
    a, n = nz(rng, -8, 9), rng.choice(POW_N)
    f = a * x ** n
    d = sp.diff(f, x)
    right = P(d)
    wr = [P(a * x ** (n - 1)), P(n * a * x ** (n + 1)), P(a * n * x ** n), P(d + x ** (n - 1))]
    return mcq(rng, f'Differentiate f(x) = {term_txt(a, n)} with respect to x.', right, wr, f'Write as {P(f)}; power rule: {right}.')


@R.add('ch05-st3', 'C3', (1, 4), 'short')
def power_sum_diff(rng, slot):
    k = 2 if slot.d <= 2 else 3
    terms = rand_terms(rng, k, allow_frac=slot.d >= 2)
    c = rng.randint(-9, 9) if slot.d >= 2 else 0
    f = sum_expr(terms) + c
    d = sp.diff(f, x)
    txt = sum_txt(terms) + (f' {"+" if c > 0 else "−"} {abs(c)}' if c else '')
    return mk(f'Find f′(x) given that f(x) = {txt}.', P(d), f'Rewrite in index form (M1); differentiate term by term: {P(d)} (A1 per correct term, up to {k}).', k + 1)


@R.add('ch05-st3', 'C3', (2, 4), 'short', style='p1')
def power_gradient_at(rng, slot):
    terms = rand_terms(rng, 2)
    f = sum_expr(terms)
    xv = rng.choice([1, 4, 9, 8, 16, 2]) if any(not sp.nsimplify(n).is_Integer for _, n in terms) else rng.choice([1, 2, 3, -1, -2])
    if any(sp.nsimplify(n) == sp.Rational(1, 3) for _, n in terms):
        xv = rng.choice([1, 8, 27])
    g = sp.diff(f, x).subs(x, xv)
    return mk(f'The curve y = {sum_txt(terms)} passes through a point P with x = {xv}. Find the exact gradient of the curve at P.', P(sp.nsimplify(g)),
              f'dy/dx = {P(sp.diff(f, x))} (M1 A1); substitute x = {xv} (M1); {P(sp.nsimplify(g))} (A1).', 4)


@R.add('ch05-st3', 'C3', (2, 4), 'short', style='p1')
def power_find_x(rng, slot):
    a, b = nz(rng, -4, 4), nz(rng, -6, 6)
    m = rng.randint(-8, 8)
    f = a * x ** 2 + b * x
    xv = sp.Rational(m - b, 2 * a)
    return mk(f'Find the coordinates of the point on the curve y = {P(f)} at which the gradient is {m}.'.replace('-', '−'), pt([xv, f.subs(x, xv)]),
              f'dy/dx = {P(sp.diff(f, x))} (A1); set equal to {m} (M1); x = {P(xv)} (A1); y = {P(f.subs(x, xv))} (A1).', 4)


@R.add('ch05-st3', 'C2', (2, 4), 'explain')
def power_error(rng, slot):
    a, n = rng.randint(2, 9), rng.choice([-1, -2, -3, sp.Rational(1, 2), -sp.Rational(1, 2)])
    f = a * x ** n
    wrongs = {-1: f'{a}', -2: f'{a}/(2x)', -3: f'{a}/(3x²)', sp.Rational(1, 2): f'{a}√x/2', -sp.Rational(1, 2): f'{a}/(√x/2)'}
    nm = who(rng)
    return mk(f'{nm} differentiates y = {term_txt(a, n)} and writes dy/dx = {wrongs[n]}. Explain the error and give the correct derivative.', P(sp.diff(f, x)),
              f'The term must be written in index form {P(f)} before using the power rule (R1); bring down the power {P(n)} and reduce the index by 1 (M1); {P(sp.diff(f, x))} (A1).', 3, 'explain', 'G2')


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step', style='ext')
def power_find_ab(rng, slot):
    a0, b0 = nz(rng, -4, 5), nz(rng, -6, 6)
    n = rng.choice([-1, -2, sp.Rational(1, 2)])
    xv = rng.choice([1, 2, 4]) if n != sp.Rational(1, 2) else rng.choice([1, 4, 9])
    f = a0 * x ** 2 + b0 * x ** n
    fv, gv = f.subs(x, xv), sp.diff(f, x).subs(x, xv)
    return mk(f'A curve has equation y = ax² + {term_txt(1, n).replace("1/", "b/") if n in (-1, -2) else "b√x"}, where a and b are constants. The curve passes through the point ({xv}, {P(fv)}) and its gradient at this point is {P(gv)}.\n(a) Write down two equations in a and b.\n(b) Find the values of a and b.\n(c) Find the gradient of the curve at x = {xv * 4 if n == sp.Rational(1, 2) else xv + 1}.',
              f'(a) {P(xv ** 2)}a + {P(sp.nsimplify(xv) ** n)}b = {P(fv)}; {2 * xv}a + {P(n * sp.nsimplify(xv) ** (n - 1))}b = {P(gv)} (b) a = {a0}, b = {b0} (c) {P(sp.diff(f, x).subs(x, xv * 4 if n == sp.Rational(1, 2) else xv + 1))}',
              f'(a) substitute the point (M1 A1); differentiate (M1) and substitute (A1). (b) solve simultaneously (M1) a = {a0} (A1), b = {b0} (A1). (c) substitution (M1) (A1).', 9)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st4', F(
    terms=[('normal to a curve', 'the line through a point of the curve perpendicular to the tangent there; its gradient is −1/m where m is the tangent gradient'),
           ('equation of a tangent', 'y − y₁ = f′(x₁)(x − x₁), the line through (x₁, f(x₁)) with gradient f′(x₁)')],
    facts=[('If the tangent at P has gradient 4, the normal at P has gradient', '−1/4', ['4', '−4', '1/4'], 'Perpendicular gradients multiply to −1.'),
           ('The tangent to y = x² at the origin is', 'y = 0', ['x = 0', 'y = x', 'y = 2x'], 'dy/dx = 2x = 0 at x = 0.'),
           ('At a point where the tangent is horizontal, the normal is', 'vertical', ['horizontal', 'at 45°', 'undefined'], 'Perpendicular to a horizontal line.')],
    why=[('Explain why the gradient of the normal is −1/f′(a).', 'The normal is perpendicular to the tangent, and perpendicular lines (neither vertical) have gradients whose product is −1.'),
         ('Explain why the normal at a stationary point is a vertical line.', 'At a stationary point the tangent is horizontal; the line perpendicular to it is vertical, with equation x = a.'),
         ('Explain why you need both f(a) and f′(a) to write down the tangent at x = a.', 'A line needs a point and a gradient: f(a) gives the point (a, f(a)) and f′(a) gives the gradient.')],
    misc=[('The tangent at x = 2 to y = x³ is y = 3x², since the derivative is 3x².', 'The tangent is a straight line: gradient 3(2)² = 12 through (2, 8): y = 12x − 16.'),
          ('The normal gradient is the negative of the tangent gradient.', 'It is the negative reciprocal: −1/m.')],
))


def _curve(rng):
    kind = rng.choice(['poly', 'poly', 'pow'])
    if kind == 'poly':
        terms = [(nz(rng, -3, 3), 3), (nz(rng, -5, 5), 2), (nz(rng, -6, 6), 1)] if rng.random() < 0.5 else [(nz(rng, -4, 4), 2), (nz(rng, -6, 6), 1)]
        c = rng.randint(-6, 6)
        return terms, c, rng.choice([-2, -1, 1, 2, 3])
    terms = [(nz(rng, -4, 4), rng.choice([2, 1])), (nz(rng, -8, 8), rng.choice([-1, -2, sp.Rational(1, 2)]))]
    return terms, 0, rng.choice([1, 2, 4]) if any(n == sp.Rational(1, 2) for _, n in terms) else rng.choice([1, 2, -1])


@R.add('ch05-st4', 'C3', (1, 4), 'short', style='p1')
def tangent_eq(rng, slot):
    terms, c, a = _curve(rng)
    f = sum_expr(terms) + c
    m = sp.diff(f, x).subs(x, a)
    ya = f.subs(x, a)
    want = rng.choice(['tangent', 'normal']) if slot.d >= 2 else 'tangent'
    if want == 'normal' and m == 0:
        ans = f'x = {a}'
    elif want == 'normal':
        mn = -1 / m
        ans = line_eq(mn, ya - mn * a)
    else:
        ans = line_eq(m, ya - m * a)
    txt = sum_txt(terms) + (f' {"+" if c > 0 else "−"} {abs(c)}' if c else '')
    return mk(f'Find the equation of the {want} to the curve y = {txt} at the point where x = {a}.', ans,
              f'y-coordinate {P(ya)} (A1); dy/dx = {P(sp.diff(f, x))} (M1), gradient at x = {a}: {P(m)} (A1)' + (f'; normal gradient {P(-1 / m) if m != 0 else "undefined (vertical)"} (M1)' if want == 'normal' else '') + f'; {ans} (A1).', 4 if want == 'tangent' else 5)


@R.add('ch05-st4', 'C3', (2, 4), 'short', style='p1')
def tangent_parallel(rng, slot):
    p, q = sorted(rng.sample(range(-3, 5), 2))
    m = rng.randint(-5, 5)
    # f' = 3(x−p)(x−q) + m  -> f = x³ − 3(p+q)/2 x² + 3pq x + m x ; require integer coefficients
    if (p + q) % 2:
        return None
    f = sp.expand(x ** 3 - sp.Rational(3, 2) * (p + q) * x ** 2 + 3 * p * q * x + m * x)
    pts_ = [pt([v, f.subs(x, v)]) for v in (p, q)]
    return mk(f'Find the coordinates of the points on the curve y = {P(f)} at which the tangent is parallel to the line {line_eq(m, 1)}.',
              ' and '.join(pts_), f'dy/dx = {P(sp.diff(f, x))} (A1); set equal to {m} (M1); 3x² {"−" if p + q > 0 else "+"} {abs(3 * (p + q))}x + {3 * p * q} = 0 → x = {p}, {q} (A1); points {", ".join(pts_)} (A1 A1).'.replace('+ -', '− '), 5)


@R.add('ch05-st4', 'C2', (2, 4), 'explain')
def normal_explain(rng, slot):
    terms, c, a = _curve(rng)
    f = sum_expr(terms) + c
    m = sp.diff(f, x).subs(x, a)
    if m == 0:
        return None
    nm = who(rng)
    return mk(f'{nm} says that the normal to y = {sum_txt(terms)}{f" {chr(43) if c > 0 else chr(8722)} {abs(c)}" if c else ""} at x = {a} has gradient {P(-m)}. Explain the error and state the correct gradient of the normal.', P(-1 / m),
              f'Tangent gradient {P(m)} (A1); the normal is perpendicular so m₁m₂ = −1 (R1); gradient −1/({P(m)}) = {P(-1 / m)}, not just the negative (A1).', 3, 'explain', 'G2')


@R.add('ch05-st4', 'C4', (3, 5), 'multi_step', style='ext')
def tangent_triangle(rng, slot):
    a = rng.choice([1, 2, 3, -1, -2])
    k = rng.choice([4, 6, 8, 12, 2, 3, 9, 16])
    kind = rng.choice(['recip', 'quad', 'cubic', 'recip2'])
    f = {'recip': k / x, 'quad': k - x ** 2, 'cubic': x ** 3 - k * x, 'recip2': k / x ** 2}[kind]
    ya, m = f.subs(x, a), sp.diff(f, x).subs(x, a)
    if m == 0:
        return None
    c = ya - m * a
    xi = -c / m
    area = sp.Abs(c * xi) / 2
    parts = [(f'Find the gradient of the curve at P.', P(m), f'dy/dx = {P(sp.diff(f, x))} (M1), m = {P(m)} (A1)', 2, False),
             (f'Find the equation of the tangent at P.', line_eq(m, c), f'P({a}, {P(ya)}) (A1); y − {P(ya)} = {P(m)}(x − {a}) (M1) {line_eq(m, c)} (A1)', 3, True),
             (f'The tangent meets the x-axis at A and the y-axis at B. Find the coordinates of A and B.', f'A({P(xi)}, 0), B(0, {P(c)})', 'set y = 0 and x = 0 (M1) A1 A1', 3, True),
             (f'Find the area of triangle OAB, where O is the origin.', P(area), f'½ × {P(abs(xi))} × {P(abs(c))} (M1) = {P(area)} (A1)', 2, False),
             (f'Find the equation of the normal at P.', line_eq(-1 / m, ya + a / m), f'gradient {P(-1 / m)} (A1); {line_eq(-1 / m, ya + a / m)} (A1)', 2, False)]
    intro = [f'Consider the curve y = {P(f)} and the point P on it with x-coordinate {a}.',
             f'The point P({a}, {P(ya)}) lies on the graph of f(x) = {P(f)}.',
             f'Let f(x) = {P(f)}. The tangent to the graph of f at x = {a} is drawn.']
    return build_parts(rng, intro, parts, 3)


@R.add('ch05-st4', 'C4', (3, 5), 'multi_step', style='p1')
def tangent_meets_again(rng, slot):
    a = nz(rng, -2, 2)
    b, c = rng.randint(-3, 3), rng.randint(-5, 5)
    f = x ** 3 + b * x ** 2 + c
    m = sp.diff(f, x).subs(x, a)
    ya = f.subs(x, a)
    # tangent meets again where x = -b - 2a (sum of roots)
    xr = -b - 2 * a
    if xr == a:
        return None
    yr = f.subs(x, xr)
    parts = [(f'Show that the equation of the tangent at P is {line_eq(m, ya - m * a)}.', 'shown', f'dy/dx = {P(sp.diff(f, x))} (M1); gradient {P(m)} at x = {a} (A1); line through ({a}, {P(ya)}) (A1) AG', 3, True),
             (f'The tangent meets the curve again at Q. Show that the x-coordinates of P and Q satisfy (x − ({a}))²(x − ({xr})) = 0.', 'shown', 'equate curve and tangent (M1); cubic with a repeated root at the point of contact (R1); factorise (A1) AG', 3, True),
             (f'Find the coordinates of Q.', pt([xr, yr]), f'x = {xr} (A1), y = {P(yr)} (A1)', 2, True),
             (f'Find the gradient of the curve at Q.', P(sp.diff(f, x).subs(x, xr)), f'substitute x = {xr} (M1) {P(sp.diff(f, x).subs(x, xr))} (A1)', 2, False)]
    return build_parts(rng, [f'The point P on the curve y = {P(f)} has x-coordinate {a}.', f'Let C be the curve y = {P(f)} and P the point on C where x = {a}.'], parts, 3)


@R.add('ch05-st4', 'C3', (2, 4), 'short', style='p2')
def tangent_p2(rng, slot):
    a = round(rng.uniform(0.5, 3), 1)
    k = rng.randint(2, 9)
    n = rng.choice([sp.Rational(1, 2), sp.Rational(3, 2), -1, sp.Rational(1, 3)])
    f = k * x ** n - x
    m = float(sp.diff(f, x).subs(x, a))
    ya = float(f.subs(x, a))
    return mk(f'Find the equation of the tangent to y = {term_txt(k, n)} − x at x = {a}, giving the gradient and intercept to 3 significant figures.',
              f'y = {s3(m)}x {"+" if ya - m * a >= 0 else "−"} {s3(abs(ya - m * a))}', f'dy/dx = {P(sp.diff(f, x))} (M1); gradient {s3(m)} (A1) [GDC]; point ({a}, {s3(ya)}) (A1); y = {s3(m)}x + {s3(ya - m * a)} (A1).', 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch05-st5', F(
    terms=[('continuous at x = a', 'f(a) is defined, lim(x→a) f(x) exists and lim(x→a) f(x) = f(a)'),
           ('differentiable at x = a', 'the limit lim(h→0) (f(a + h) − f(a))/h exists (left and right limits agree)'),
           ('first principles', 'finding the derivative directly from the definition f′(x) = lim(h→0) (f(x + h) − f(x))/h')],
    facts=[('Which function is continuous at x = 0 but not differentiable there?', 'f(x) = |x|', ['f(x) = x²', 'f(x) = 1/x', 'f(x) = sin x'], 'The left and right gradients of |x| at 0 are −1 and 1.'),
           ('If f is differentiable at x = a, then f must be', 'continuous at x = a', ['zero at x = a', 'stationary at x = a', 'increasing at x = a'], 'Differentiability implies continuity, not conversely.'),
           ('A piecewise function is continuous at the join x = a if', 'both pieces give the same value at x = a', ['both pieces have the same gradient everywhere', 'the pieces are both linear', 'f′(a) = 0'], 'Left and right limits must equal f(a).')],
    why=[('Explain why |x| is not differentiable at x = 0.', 'For h > 0 the difference quotient (|h| − 0)/h = 1, for h < 0 it is −1; the one-sided limits differ, so the limit does not exist.'),
         ('Explain why differentiability at a point implies continuity there.', 'f(a + h) − f(a) = h × (f(a + h) − f(a))/h → 0 × f′(a) = 0 as h → 0, so f(a + h) → f(a).'),
         ('Explain why, when differentiating from first principles, you cannot simply substitute h = 0 at the start.', 'At h = 0 the quotient is 0/0; you must first simplify (expand and cancel the factor h), then let h → 0.')],
    misc=[('A function that is continuous at a point must be differentiable there.', '|x| is continuous at 0 but has a corner there, so it is not differentiable.'),
          ('In first principles, (f(x + h) − f(x))/h with h = 0 gives f′(x).', 'Substituting h = 0 gives 0/0; the limit as h → 0 is taken after cancelling h.')],
))


@R.add('ch05-st5', 'C3', (2, 4), 'short', style='p1')
def first_principles(rng, slot):
    h = sp.Symbol('h')
    kind = rng.choice(['quad', 'cubic', 'recip']) if slot.d >= 3 else 'quad'
    if kind == 'quad':
        a, b, c = nz(rng, -5, 5), rng.randint(-6, 6), rng.randint(-6, 6)
        f = a * x ** 2 + b * x + c
    elif kind == 'cubic':
        a, b = nz(rng, -3, 3), rng.randint(-4, 4)
        f = a * x ** 3 + b * x
    else:
        a = nz(rng, -6, 6)
        f = a / x
    dq = sp.factor(sp.cancel((f.subs(x, x + h) - f) / h))
    return mk(f'Differentiate f(x) = {P(f)} from first principles.', f"f′(x) = {P(sp.diff(f, x))}",
              f'(f(x + h) − f(x))/h set up (M1); f(x + h) correctly expanded (A1); simplified to {P(sp.expand(dq)) if kind != "recip" else P(dq)} after cancelling h (A1); limit as h → 0: {P(sp.diff(f, x))} (A1).', 4)


@R.add('ch05-st5', 'C3', (3, 5), 'short', style='p1')
def piecewise_diff(rng, slot):
    a = rng.choice([1, 2, -1, 3])
    p = nz(rng, -3, 3)
    q = rng.randint(-4, 4)
    # f = p x^2 + q for x<=a ; m x + c for x > a  ; continuity & differentiability -> m = 2pa, c = p a^2 + q − m a
    m = 2 * p * a
    c = p * a * a + q - m * a
    return mk(f'The function f is defined by f(x) = {P(p * x ** 2 + q)} for x ≤ {a} and f(x) = mx + c for x > {a}. Given that f is differentiable at x = {a}, find m and c.',
              f'm = {m}, c = {c}', f'Differentiable ⇒ gradients agree: 2({p})({a}) = m (M1) m = {m} (A1); continuous ⇒ values agree: {P(p * a * a + q)} = {m}({a}) + c (M1); c = {c} (A1).', 4)


@R.add('ch05-st5', 'C2', (2, 4), 'explain')
def continuity_check(rng, slot):
    a = rng.choice([0, 1, 2, -1])
    p, q, r_ = nz(rng, -3, 3), rng.randint(-4, 4), nz(rng, -3, 3)
    left = p * a + q
    s = left - r_ * a + rng.choice([0, 0, 1, -2])
    right = r_ * a + s
    cont = left == right
    diff = cont and p == r_
    return mk(f'f(x) = {P(p * x + q)} for x < {a} and f(x) = {P(r_ * x + s)} for x ≥ {a}. Determine whether f is continuous at x = {a}, and whether it is differentiable there, explaining your reasoning.',
              f'{"continuous" if cont else "not continuous"}; {"differentiable" if diff else "not differentiable"}',
              f'Left limit {left}, f({a}) = {right} (A1); {"equal so continuous" if cont else "not equal so discontinuous"} (R1); gradients {p} and {r_} {"equal" if p == r_ else "differ"} (A1); {"differentiable" if diff else "not differentiable" + (" (a discontinuous function cannot be differentiable)" if not cont else " (a corner)")} (R1).', 4, 'explain')


@R.add('ch05-st5', 'C1', (1, 3), 'mcq')
def fp_definition_mcq(rng, slot):
    return mcq(rng, 'Which expression defines f′(x) from first principles?', 'lim(h→0) (f(x + h) − f(x))/h',
               ['lim(h→0) (f(x + h) − f(x))', 'lim(h→∞) (f(x + h) − f(x))/h', '(f(x + h) − f(x))/h with h = 0'], 'The derivative is the limit of the difference quotient as h → 0.') if rng.random() < 0.5 else \
        mcq(rng, f'When differentiating f(x) = x² from first principles, (f(x + h) − f(x))/h simplifies to', '2x + h', ['2x', 'h²', '2xh + h²'], '(x² + 2xh + h² − x²)/h = 2x + h → 2x.')


@R.add('ch05-st5', 'C4', (3, 5), 'multi_step', style='p3')
def fp_sqrt(rng, slot):
    k = rng.choice([1, 2, 3, 4, 5])
    a = rng.choice([1, 4, 9])
    return mk(f'(a) Show that (√(x + h) − √x)/h = 1/(√(x + h) + √x).\n(b) Hence differentiate f(x) = {"" if k == 1 else k}√x from first principles.\n(c) Explain why f is not differentiable at x = 0, and find the gradient of the curve at x = {a}.',
              f'(b) f′(x) = {P(sp.Rational(k, 2))}/√x (c) gradient {P(sp.Rational(k, 2) / sp.sqrt(a))}',
              f'(a) multiply numerator and denominator by √(x + h) + √x (M1); numerator becomes h (A1); cancel AG. (b) limit h → 0 gives {k}/(2√x) (M1 A1). (c) at x = 0 the one-sided difference quotient {k}/√h → ∞, so no finite limit (R1); gradient {P(sp.Rational(k, 2) / sp.sqrt(a))} (A1).', 7)


@R.add('ch05-st5', 'C4', (3, 5), 'multi_step', style='ext')
def piecewise_full(rng, slot):
    a = rng.choice([1, 2, -1, 3])
    p = nz(rng, -3, 3)
    b = sp.Rational(3 * a * a + p, 2 * a)
    c = a ** 3 + p * a - b * a * a
    form = rng.choice(['x³ + px', 'x³ + px (second piece quadratic)'])
    parts = [(f'Write down two conditions that must hold for g to be differentiable at x = {a}.', 'continuity (values match) and equal one-sided derivatives', 'R1 R1', 2, True),
             ('Find the values of b and c.', f'b = {P(b)}, c = {P(c)}', f'{3 * a * a + p} = {2 * a}b (M1) b = {P(b)} (A1); {a ** 3 + p * a} = {a * a}b + c (M1) c = {P(c)} (A1)', 4, True),
             (f'Find g′(x) for x > {a} and verify that g′ is continuous at x = {a}.', f'g′(x) = {P(2 * b * x)}; both sides give {3 * a * a + p}', f'(A1); substitution on both sides (R1)', 2, False),
             (f'Determine whether g″ is continuous at x = {a}.', f"{'yes' if 6 * a == 2 * b else 'no'}: 6({a}) = {6 * a} vs 2b = {P(2 * b)}", 'compare second derivatives (M1) A1', 2, False)]
    return build_parts(rng, [f'The function g is defined by g(x) = {P(x ** 3 + p * x)} for x ≤ {a} and g(x) = bx² + c for x > {a}, where b and c are constants.',
                             f'A piecewise function is given by g(x) = {P(x ** 3 + p * x)} (x ≤ {a}), g(x) = bx² + c (x > {a}). It is known that g is differentiable everywhere.'], parts, 2)


@R.add('ch05-st5', 'C4', (3, 5), 'multi_step', style='p3')
def fp_sqrt(rng, slot):
    k = rng.choice([1, 2, 3, 4, 5, 6])
    a = rng.choice([1, 4, 9, 16, 25])
    kind = rng.choice(['sqrt', 'recip_sqrt'])
    if kind == 'sqrt':
        parts = [('Show that (√(x + h) − √x)/h = 1/(√(x + h) + √x).', 'shown', 'multiply by the conjugate √(x + h) + √x (M1); numerator h (A1) AG', 2, True),
                 (f'Hence differentiate f(x) = {"" if k == 1 else k}√x from first principles.', f'f′(x) = {P(sp.Rational(k, 2))}/√x' if k != 2 else "f′(x) = 1/√x", 'limit as h → 0 (M1) A1', 2, True),
                 ('Explain why f is not differentiable at x = 0.', 'the difference quotient k/√h → ∞ as h → 0⁺', 'R1 R1', 2, False),
                 (f'Find the equation of the tangent at x = {a}.', line_eq(sp.Rational(k, 2) / sp.sqrt(a), k * sp.sqrt(a) - sp.Rational(k, 2) / sp.sqrt(a) * a), 'gradient (A1) line (M1 A1)', 3, False)]
        return build_parts(rng, ['This question is about differentiation from first principles.', f'Let f(x) = {"" if k == 1 else k}√x, x ≥ 0.'], parts, 3)
    parts = [('Show that 1/√(x + h) − 1/√x = −h/(√x√(x + h)(√(x + h) + √x)).', 'shown', 'common denominator (M1); multiply by conjugate (M1) A1 AG', 3, True),
             (f'Hence find the derivative of f(x) = {k}/√x from first principles.', f"f′(x) = {P(-sp.Rational(k, 2))}x^(−3/2)", 'divide by h, limit h → 0 (M1) A1', 2, True),
             (f'Find the gradient of the curve at x = {a}.', P(-sp.Rational(k, 2) * sp.Integer(a) ** sp.Rational(-3, 2)), 'A1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {k}/√x, x > 0.', 'This question uses the definition of the derivative.'], parts, 2)


@R.add('ch05-st5', 'C4', (3, 5), 'multi_step', style='p1')
def fp_cubic_parts(rng, slot):
    h = sp.Symbol('h')
    a, b = nz(rng, -3, 3), rng.randint(-5, 5)
    f = a * x ** 3 + b * x ** 2
    num = sp.expand(f.subs(x, x + h) - f)
    q = sp.expand(sp.cancel(num / h))
    xv = rng.randint(-2, 3)
    parts = [(f'Show that f(x + h) − f(x) = {P(num)}.', 'shown', 'expand (x + h)³ and (x + h)² (M1) A1 AG', 2, True),
             ('Hence find f′(x) from first principles.', P(sp.diff(f, x)), f'divide by h: {P(q)} (M1); limit h → 0 (A1)', 2, True),
             (f'Find the gradient of the chord between x = {xv} and x = {xv} + h when h = 0.1, and compare it with f′({xv}).', f'{s3(q.subs({x: xv, h: 0.1}))} vs {P(sp.diff(f, x).subs(x, xv))}', 'substitute (A1); difference tends to 0 (R1)', 2, False),
             ('Find the x-coordinates of the points where the tangent is horizontal.', lst(sorted(set(sp.solve(sp.diff(f, x), x)), key=float)), 'f′(x) = 0 (M1) A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}.', f'Consider the cubic function f(x) = {P(f)}.'], parts, 3)


# =============================================================================================
# ch06 Differentiation rules
# =============================================================================================
E = sp.E


def dd(f):
    return sp.simplify(sp.diff(f, x))


def dfac(f):
    """derivative in a tidy factorised form"""
    d = sp.diff(f, x)
    cands = [sp.factor(d), sp.simplify(d), sp.expand(d)]
    return min(cands, key=lambda e: len(sp.sstr(e)))


R.facts('ch06-st1', F(
    terms=[('derivative of sin x', 'cos x (x in radians)'), ('derivative of cos x', '−sin x (x in radians)'),
           ('derivative of eˣ', 'eˣ: the exponential function is its own derivative'), ('derivative of ln x', '1/x, for x > 0')],
    facts=[('What is the derivative of 3eˣ − 2 sin x?', '3eˣ − 2 cos x', ['3eˣ + 2 cos x', '3xeˣ⁻¹ − 2 cos x', 'eˣ − 2 cos x'], 'd/dx eˣ = eˣ, d/dx sin x = cos x.'),
           ('If f(x) = ln x, then f′(e) =', '1/e', ['1', 'e', '0'], 'f′(x) = 1/x.'),
           ('The gradient of y = cos x at x = π/2 is', '−1', ['0', '1', 'π/2'], 'dy/dx = −sin x = −1 at π/2.'),
           ('Why must x be in radians when using d/dx(sin x) = cos x?', 'the result relies on lim(h→0) sin h/h = 1, true only in radians', ['calculators require it', 'degrees are not real numbers', 'cos x is undefined in degrees'], 'In degrees an extra factor π/180 appears.')],
    why=[('Explain why the derivative of ln(5x) is the same as the derivative of ln x.', 'ln(5x) = ln 5 + ln x, and ln 5 is a constant with derivative 0, so both derivatives are 1/x.'),
         ('Explain, using the graph of y = sin x, why its derivative is cos x at x = 0, π/2 and π.', 'The gradient of sin x is 1 at 0, 0 at the maximum π/2 and −1 at π, matching cos 0 = 1, cos(π/2) = 0, cos π = −1.'),
         ('Explain why the graph of y = eˣ is always increasing and concave up.', 'Its first and second derivatives are both eˣ, which is positive for all x.')],
    misc=[('d/dx (eˣ) = xeˣ⁻¹ by the power rule.', 'The power rule applies to xⁿ (variable base, constant power); eˣ has a constant base, and d/dx eˣ = eˣ.'),
          ('d/dx (cos x) = sin x.', 'd/dx (cos x) = −sin x: cos x is decreasing on (0, π) where sin x > 0.')],
))

ST1_BASIS = [('sin x', sp.sin(x)), ('cos x', sp.cos(x)), ('eˣ', sp.exp(x)), ('ln x', sp.log(x)), ('x²', x ** 2), ('√x', sp.sqrt(x))]


def _st1_func(rng, k=2):
    picks = rng.sample(ST1_BASIS, k)
    terms, expr = [], 0
    for txt, e in picks:
        c = nz(rng, -6, 6)
        expr += c * e
        terms.append(('−' if c < 0 else '') + ('' if abs(c) == 1 else str(abs(c))) + ('' if abs(c) == 1 else ' ' if txt[0] in 'sclei' else '') + txt)
    s = terms[0]
    for tm in terms[1:]:
        s += (' − ' + tm[1:]) if tm.startswith('−') else (' + ' + tm)
    return s, expr


@R.add('ch06-st1', 'C1', (1, 3), 'mcq')
def std_deriv_mcq(rng, slot):
    s, f = _st1_func(rng, 2)
    d = sp.diff(f, x)
    wr = [P(sp.diff(f.subs(sp.cos(x), -sp.cos(x)), x)) if f.has(sp.cos) else P(d + 1), P(sp.integrate(f, x)) if not f.has(sp.log) else P(d + 1 / x), P(-d), P(d + x)]
    return mcq(rng, f'Find dy/dx for y = {s}.', P(d), wr, f'Differentiate term by term: {P(d)}.')


@R.add('ch06-st1', 'C3', (1, 4), 'short', style='p1')
def std_deriv_value(rng, slot):
    s, f = _st1_func(rng, 2 if slot.d <= 2 else 3)
    if (f.has(sp.sin) or f.has(sp.cos)) and (f.has(sp.log) or f.has(sp.sqrt(x)) or f.has(sp.exp)):
        return None
    if f.has(sp.log) or f.has(sp.sqrt(x)):
        xv = rng.choice([1, 4, sp.E]) if not f.has(sp.sin(x)) else rng.choice([pi, pi / 2])
    else:
        xv = rng.choice([0, pi / 6, pi / 3, pi / 2, pi, sp.log(2)])
    g = sp.simplify(sp.diff(f, x).subs(x, xv))
    if g.has(sp.sin) or g.has(sp.cos) or g.has(sp.log(sp.pi)):
        return None
    return mk(f'Given f(x) = {s}, find the exact value of f′({P(xv)}).', P(sp.radsimp(g)),
              f"f′(x) = {P(sp.diff(f, x))} (A1 A1); substitute x = {P(xv)} (M1); {P(sp.radsimp(g))} (A1).", 4)


@R.add('ch06-st1', 'C3', (2, 4), 'short', style='p1')
def exp_ln_stationary(rng, slot):
    kk = rng.choice([2, 3, 4, 5, 6, sp.Rational(1, 2)])
    kind = rng.choice(['e', 'ln'])
    if kind == 'e':
        f = sp.exp(x) - kk * x
        xs_ = sp.log(kk)
        ys = sp.simplify(f.subs(x, xs_))
        txt = P(f).replace('e^x', 'eˣ')
    else:
        f = kk * x - sp.log(x)
        xs_ = 1 / sp.nsimplify(kk)
        ys = sp.simplify(f.subs(x, xs_))
        txt = P(f).replace('ln(x)', 'ln x')
    return mk(f'Find the exact coordinates of the stationary point on the curve y = {txt}{", x > 0" if kind == "ln" else ""}.', f'({P(xs_)}, {P(sp.expand_log(ys, force=True))})',
              f"dy/dx = {P(sp.diff(f, x))} (A1); set dy/dx = 0 (M1); x = {P(xs_)} (A1); y = {P(sp.expand_log(ys, force=True))} (A1).", 4)


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def std_deriv_explain(rng, slot):
    kk = rng.randint(2, 12)
    kind = rng.choice(['ln', 'trig', 'exp'])
    if kind == 'ln':
        return mk(f'Explain why the graphs of y = ln({kk}x) and y = ln x have the same gradient at every x > 0.', 'Both derivatives equal 1/x.',
                  f'ln({kk}x) = ln {kk} + ln x (M1 R1); ln {kk} is constant so the derivatives are equal, 1/x (A1).', 3, 'explain')
    if kind == 'trig':
        a = rng.choice([pi / 6, pi / 4, pi / 3, 2 * pi / 3])
        return mk(f'Explain, without a calculator, why the tangent to y = sin x at x = {P(a)} and the tangent to y = cos x at x = {P(pi / 2 - a)} are perpendicular or parallel, stating which.',
                  'perpendicular' if sp.cos(a) * (-sp.sin(pi / 2 - a)) == -1 else 'neither in general – compare gradients',
                  f'gradients cos({P(a)}) = {P(sp.cos(a))} and −sin({P(pi / 2 - a)}) = {P(-sp.sin(pi / 2 - a))} (A1 A1); product {P(sp.cos(a) * (-sp.sin(pi / 2 - a)))} (M1); conclusion (R1).', 4, 'explain')
    return mk(f'Explain why the graph of y = {kk}eˣ has gradient equal to its y-coordinate at every point.', f'dy/dx = {kk}eˣ = y',
              f'd/dx(eˣ) = eˣ (R1), so dy/dx = {kk}eˣ (A1), which equals y (R1).', 3, 'explain')


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step', style='ext')
def exp_tangent_parts(rng, slot):
    a = rng.choice([0, 1, 2, -1, sp.log(2), sp.log(3)])
    kk = rng.randint(1, 4)
    f = kk * sp.exp(x) + rng.choice([-1, 1]) * x
    ya, m = sp.simplify(f.subs(x, a)), sp.simplify(sp.diff(f, x).subs(x, a))
    c = sp.simplify(ya - m * a)
    yi = c
    parts = [('Find f′(x).', P(sp.diff(f, x)), 'A1 A1', 2, True),
             (f'Find the equation of the tangent to the graph of f at x = {P(a)}.', line_eq(m, c), f'f({P(a)}) = {P(ya)} (A1); gradient {P(m)} (A1); line (M1 A1)', 4, True),
             ('Find the exact y-intercept of this tangent.', P(yi), 'A1', 1, False),
             ('Show that f″(x) > 0 for all x and interpret this for the tangent you found.', f'f″(x) = {P(sp.diff(f, x, 2))} > 0; the curve lies above the tangent (concave up)', 'R1 R1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}.', f'The function f is defined by f(x) = {P(f)} for all real x.'], parts, 3)


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step', style='p1')
def trig_stationary_parts(rng, slot):
    a, b = rng.choice([(1, 1), (1, -1), (r3, 1), (1, r3), (2, 2)])
    f = a * sp.sin(x) + b * sp.cos(x)
    sols = solve_basic('tan', 1, 0, sp.nsimplify(a / b), 0, 2 * pi)
    vals = [sp.radsimp(f.subs(x, s_)) for s_ in sols]
    parts = [('Find f′(x).', P(sp.diff(f, x)), 'A1 A1', 2, True),
             ('Find the x-coordinates of the stationary points for 0 ≤ x ≤ 2π.', lst(sols), f'f′(x) = 0 ⇒ tan x = {P(sp.nsimplify(a / b))} (M1 A1); both solutions (A1)', 3, True),
             ('Find the maximum value of f.', P(max(vals, key=float)), 'substitute (M1) A1', 2, True),
             ('Use f″ to confirm the nature of the point with the smaller x-coordinate.', 'f″ = −f; ' + ('maximum' if float(vals[0]) > 0 else 'minimum'), 'f″(x) = −f(x) (A1) sign (R1)', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}, for 0 ≤ x ≤ 2π.', f'Consider f(x) = {P(f)}, 0 ≤ x ≤ 2π.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch06-st2', F(
    terms=[('chain rule', 'if y = g(u) and u = f(x), then dy/dx = (dy/du)(du/dx)'),
           ('product rule', 'if y = uv, then dy/dx = u dv/dx + v du/dx'),
           ('quotient rule', 'if y = u/v, then dy/dx = (v du/dx − u dv/dx)/v²')],
    facts=[('Which rule is needed first to differentiate y = sin(x²)?', 'the chain rule', ['the product rule', 'the quotient rule', 'the power rule only'], 'sin of a function of x is a composite.'),
           ('d/dx (e^(3x)) =', '3e^(3x)', ['e^(3x)', 'e^(3x)/3', '3xe^(3x − 1)'], 'Chain rule: derivative of 3x is 3.'),
           ('d/dx (x eˣ) =', '(x + 1)eˣ', ['eˣ', 'xeˣ', 'x²eˣ/2'], 'Product rule: eˣ + xeˣ.'),
           ('d/dx (ln(2x + 1)) =', '2/(2x + 1)', ['1/(2x + 1)', '2 ln(2x + 1)', '1/(2x)'], 'Chain rule: (1/u)(du/dx).')],
    why=[('Explain why the derivative of (3x + 1)⁵ is not 5(3x + 1)⁴.', 'It is a composite function; the chain rule multiplies by the derivative of the inner function 3x + 1, which is 3, giving 15(3x + 1)⁴.'),
         ('Explain why the product rule is needed for x² sin x but not for 5 sin x.', '5 is a constant multiple, so its derivative is 5 cos x; x² is a function of x, so both factors change and the product rule u′v + uv′ applies.'),
         ('Explain how the quotient rule can be obtained from the product rule.', 'Write u/v = u·v⁻¹; the product rule with the chain rule gives u′v⁻¹ − uv⁻²v′ = (u′v − uv′)/v².')],
    misc=[('d/dx (x² eˣ) = 2x eˣ.', 'Use the product rule: 2x eˣ + x² eˣ = x(x + 2)eˣ.'),
          ('d/dx (sin 3x) = cos 3x.', 'Chain rule: 3 cos 3x.'),
          ('In the quotient rule the numerator is u v′ − v u′.', 'It is v u′ − u v′ (derivative of the top times the bottom first); the order matters because of the minus sign.')],
))

CHAIN = [lambda rng: (rng.choice([2, 3, -1, 5]) * x + nz(rng, -5, 5)) ** rng.choice([3, 4, 5, -1, -2, sp.Rational(1, 2)]),
         lambda rng: sp.sin(rng.choice([2, 3, 4, 5]) * x + rng.choice([0, 1, -2])),
         lambda rng: sp.cos(rng.choice([2, 3, -2]) * x ** 2),
         lambda rng: sp.exp(rng.choice([2, -3, 5]) * x ** 2 + nz(rng, -3, 3) * x),
         lambda rng: sp.log(rng.choice([2, 3]) * x ** 2 + rng.randint(1, 5)),
         lambda rng: sp.sqrt(rng.choice([1, 2, 3]) * x ** 2 + rng.randint(1, 9)),
         lambda rng: sp.sin(x) ** rng.choice([2, 3, 4]),
         lambda rng: sp.exp(sp.sin(x)) if rng.random() < 0.5 else sp.log(sp.cos(x))]
PROD = [lambda rng: x ** rng.choice([2, 3]) * sp.exp(rng.choice([2, -1, 3]) * x),
        lambda rng: x * sp.sin(rng.choice([2, 3]) * x),
        lambda rng: x ** 2 * sp.log(x),
        lambda rng: sp.exp(rng.choice([2, -1]) * x) * sp.cos(rng.choice([1, 3]) * x),
        lambda rng: x * (rng.choice([2, 3]) * x + rng.randint(1, 4)) ** rng.choice([3, 4]),
        lambda rng: sp.sqrt(x) * sp.log(x),
        lambda rng: x ** 3 * sp.cos(x)]
QUOT = [lambda rng: (nz(rng, -4, 4) * x + rng.randint(-5, 5)) / (rng.choice([1, 2, 3]) * x + nz(rng, -5, 5)),
        lambda rng: sp.exp(rng.choice([1, 2]) * x) / x,
        lambda rng: sp.log(x) / x ** rng.choice([1, 2]),
        lambda rng: sp.sin(x) / (1 + sp.cos(x)) if rng.random() < 0.5 else x / sp.cos(x),
        lambda rng: x ** 2 / (x + nz(rng, -4, 4)),
        lambda rng: (x ** 2 + rng.randint(1, 5)) / (x ** 2 + rng.randint(6, 9))]


@R.add('ch06-st2', 'C3', (1, 4), 'short')
def rules_diff(rng, slot):
    fam = rng.choice(['chain', 'prod', 'quot']) if slot.d >= 2 else 'chain'
    f = rng.choice({'chain': CHAIN, 'prod': PROD, 'quot': QUOT}[fam])(rng)
    d = dfac(f)
    verb = rng.choice(['Differentiate', 'Find dy/dx for', 'Find the derivative of'])
    yname = rng.choice(['y', 'f(x)', 'g(x)'])
    return mk(f'{verb} {yname} = {P(f)}.' if verb != 'Find the derivative of' else f'Find the derivative of {P(f)} with respect to x.', P(d),
              f'{"Chain" if fam == "chain" else "Product" if fam == "prod" else "Quotient"} rule identified and applied (M1); correct parts (A1 A1); simplified: {P(d)} (A1). Equivalent forms accepted.', 4)


@R.add('ch06-st2', 'C1', (1, 3), 'mcq')
def chain_mcq(rng, slot):
    a = rng.choice([2, 3, 4, 5, -2, -3])
    kind = rng.choice(['exp', 'sin', 'cos', 'ln', 'pow'])
    f = {'exp': sp.exp(a * x), 'sin': sp.sin(a * x), 'cos': sp.cos(a * x), 'ln': sp.log(a * x + 1) if a > 0 else sp.log(1 - a * x), 'pow': (a * x + 1) ** 4}[kind]
    d = sp.diff(f, x)
    wr = [P(d / a) if kind != 'ln' else P(sp.diff(f, x) * (a * x + 1) if a > 0 else d + 1), P(-d), P(d * a), P(sp.integrate(f, x)) if kind != 'pow' else P(4 * (a * x + 1) ** 3)]
    return mcq(rng, f'Find the derivative of {P(f)}.', P(d), wr, f'Chain rule: multiply by the derivative of the inner function. {P(d)}.')


@R.add('ch06-st2', 'C3', (2, 4), 'short', style='p1')
def rules_gradient(rng, slot):
    f = rng.choice(PROD + QUOT)(rng)
    xv = rng.choice([1, 2, 0, -1]) if not f.has(sp.log) else rng.choice([1, sp.E])
    if f.has(sp.sin) or f.has(sp.cos):
        xv = rng.choice([0, pi, pi / 2])
    try:
        g = sp.simplify(sp.diff(f, x).subs(x, xv))
    except Exception:
        return None
    if not g.is_finite or g.has(sp.zoo) or g.has(sp.nan):
        return None
    return mk(f'Find the exact gradient of the curve y = {P(f)} at the point where x = {P(xv)}.', P(g),
              f'dy/dx = {P(dfac(f))} (M1 A1); substitute x = {P(xv)} (M1); {P(g)} (A1).', 4)


@R.add('ch06-st2', 'C2', (2, 4), 'explain')
def rules_error(rng, slot):
    a = rng.randint(2, 6)
    n = rng.randint(3, 6)
    kind = rng.choice(['chain', 'prod', 'quot'])
    nm = who(rng)
    if kind == 'chain':
        f = (a * x + 1) ** n
        return mk(f'{nm} writes d/dx ({P(f)}) = {n}({P(a * x + 1)}){str(n - 1).translate(_SUP)}. Explain the error and correct it.', P(sp.diff(f, x)),
                  f'The chain rule requires multiplying by the derivative of the inner function, {a} (R1); correct derivative {P(sp.diff(f, x))} (A1).', 2, 'explain', 'G2')
    if kind == 'prod':
        f = x ** n * sp.exp(a * x)
        return mk(f'{nm} says that d/dx (x{str(n).translate(_SUP)}e^({a}x)) = {n}x{str(n - 1).translate(_SUP)} × {a}e^({a}x). Explain why this is wrong and find the correct derivative.', P(dfac(f)),
                  f'The derivative of a product is not the product of the derivatives (R1); product rule u′v + uv′ (M1); {P(dfac(f))} (A1).', 3, 'explain', 'G2')
    f = sp.sin(x) / x ** a
    return mk(f'{nm} differentiates y = sin x / x{str(a).translate(_SUP)} using the quotient rule as (sin x · {a}x{str(a - 1).translate(_SUP) if a > 2 else ""} − x{str(a).translate(_SUP)} cos x)/x{str(2 * a).translate(_SUP)}. Explain the error and give the correct derivative.', P(dfac(f)),
              f'The numerator must be v u′ − u v′ = x{str(a).translate(_SUP)} cos x − {a}x{str(a - 1).translate(_SUP) if a > 2 else ""} sin x; the terms are reversed, giving the wrong sign (R1); correct: {P(dfac(f))} (A1 A1).', 3, 'explain', 'G2')


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step', style='ext')
def xexp_stationary(rng, slot):
    n = rng.choice([1, 2])
    a = rng.choice([1, 2, 3, sp.Rational(1, 2)])
    f = x ** n * sp.exp(-a * x)
    d = sp.factor(sp.diff(f, x))
    st = sorted(set(sp.solve(sp.diff(f, x), x)), key=float)
    vals = [sp.simplify(f.subs(x, s_)) for s_ in st]
    parts = [(f'Show that f′(x) = {P(d)}.', 'shown', 'product rule (M1) A1; factorise AG', 2, True),
             ('Find the exact coordinates of the stationary point(s) of f.', '; '.join(f'({P(s_)}, {P(v)})' for s_, v in zip(st, vals)), 'f′(x) = 0 (M1); e^(−ax) ≠ 0 (R1); A1 A1', 4, True),
             ('Write down the equation of the horizontal asymptote of the graph of f.', 'y = 0', 'as x → ∞, f(x) → 0 (A1)', 1, False),
             ('Find the range of f for x ≥ 0.', f'0 ≤ f(x) ≤ {P(max(vals, key=float))}', 'A1 A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}.', f'The function f is defined by f(x) = {P(f)}, x ∈ ℝ.'], parts, 3)


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step', style='p2')
def rules_gdc(rng, slot):
    f = rng.choice(PROD)(rng)
    g = sp.lambdify(x, sp.diff(f, x), 'math')
    xv = round(rng.uniform(0.5, 2.5), 2)
    try:
        val = g(xv)
    except Exception:
        return None
    parts = [('Find f′(x).', P(dfac(f)), 'product rule (M1) A1 A1', 3, True),
             (f'Find the gradient of the graph at x = {xv}.', s3(val), 'A1', 1, True),
             (f'Find the equation of the normal at x = {xv}.', f'y = {s3(-1 / val)}x + {s3(float(f.subs(x, xv)) + xv / val)}'.replace('+ −', '− '), 'gradient −1/f′ (M1); point (A1); equation (A1)', 3, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}, x > 0.', f'Consider the curve y = {P(f)} for x > 0.'], parts, 2)


# ---------------------------------------------------------------------------------------------
R.facts('ch06-st3', F(
    terms=[('derivative of tan x', 'sec²x'), ('derivative of sec x', 'sec x tan x'), ('derivative of cosec x', '−cosec x cot x'),
           ('derivative of cot x', '−cosec²x'), ('derivative of aˣ', 'aˣ ln a, for a > 0'), ('derivative of logₐx', '1/(x ln a)'),
           ('derivative of arcsin x', '1/√(1 − x²)'), ('derivative of arctan x', '1/(1 + x²)')],
    facts=[('d/dx (arccos x) =', '−1/√(1 − x²)', ['1/√(1 − x²)', '−1/(1 + x²)', 'arcsin x'], 'arccos x = π/2 − arcsin x.'),
           ('d/dx (2ˣ) =', '2ˣ ln 2', ['x2ˣ⁻¹', '2ˣ', '2ˣ/ln 2'], '2ˣ = e^(x ln 2).'),
           ('d/dx (log₁₀x) =', '1/(x ln 10)', ['1/x', 'ln 10/x', '10/x'], 'Change of base: log₁₀x = ln x/ln 10.'),
           ('d/dx (tan 3x) =', '3sec²3x', ['sec²3x', '3tan²3x', '3sec 3x tan 3x'], 'Chain rule.')],
    why=[('Explain why d/dx(aˣ) = aˣ ln a.', 'aˣ = e^(x ln a); by the chain rule its derivative is ln a · e^(x ln a) = aˣ ln a.'),
         ('Explain how implicit differentiation gives the derivative of arcsin x.', 'y = arcsin x ⇒ sin y = x; differentiate: cos y dy/dx = 1, so dy/dx = 1/cos y = 1/√(1 − x²), taking the positive root since −π/2 ≤ y ≤ π/2.'),
         ('Explain why the derivative of tan x is always positive where it is defined.', 'd/dx tan x = sec²x = 1/cos²x > 0 wherever cos x ≠ 0.')],
    misc=[('d/dx (3ˣ) = x·3ˣ⁻¹.', 'The power rule needs a constant power; for aˣ, the derivative is 3ˣ ln 3.'),
          ('d/dx (arctan x) = sec²x.', 'sec²x is the derivative of tan x; d/dx arctan x = 1/(1 + x²).')],
))

ST3 = [lambda a: sp.tan(a * x), lambda a: sp.sec(a * x), lambda a: sp.csc(a * x), lambda a: sp.cot(a * x),
       lambda a: sp.Integer(a + 1) ** x, lambda a: sp.log(x) / sp.log(a + 1), lambda a: sp.asin(a * x) if a < 4 else sp.asin(x / a),
       lambda a: sp.acos(x / a), lambda a: sp.atan(a * x), lambda a: sp.atan(x / a), lambda a: x * sp.atan(x) if a == 2 else sp.tan(x) ** 2]


def _st3_txt(f):
    s_ = P(f)
    m_ = re.fullmatch(r'ln\(x\)/ln\((\d+)\)', s_)
    if m_:
        return f'log{m_.group(1).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))}x'
    return s_


@R.add('ch06-st3', 'C3', (1, 4), 'short')
def ahl_deriv(rng, slot):
    a = rng.choice([1, 2, 3, 4, 5])
    f = rng.choice(ST3)(a)
    d = sp.simplify(sp.diff(f, x))
    if f.has(sp.log) and not f.has(sp.atan):
        d = sp.diff(f, x)
    return mk(f'Differentiate y = {_st3_txt(f)} with respect to x.', P(d), f'Standard result from the formula booklet with chain rule as needed (M1); {P(d)} (A1 A1).', 3)


@R.add('ch06-st3', 'C1', (1, 3), 'mcq')
def ahl_deriv_mcq(rng, slot):
    a = rng.choice([1, 2, 3])
    f = rng.choice(ST3[:4] + ST3[6:10])(a)
    d = sp.simplify(sp.diff(f, x))
    wr = [P(-d), P(d / a) if a != 1 else P(d + 1), P(sp.simplify(d * a + 1))]
    return mcq(rng, f'What is the derivative of {P(f)}?', P(d), wr, f'{P(d)}.')


@R.add('ch06-st3', 'C3', (2, 4), 'short', style='p1')
def ahl_value(rng, slot):
    kind = rng.choice(['tan', 'sec', 'atan', 'asin', 'ax'])
    if kind == 'tan':
        a = rng.choice([1, 2, 3]); xv = rng.choice([pi / 6, pi / 4, pi / 3]) / a; f = sp.tan(a * x)
    elif kind == 'sec':
        f = sp.sec(x); xv = rng.choice([pi / 6, pi / 4, pi / 3])
    elif kind == 'atan':
        a = rng.choice([1, 2, 3]); f = sp.atan(a * x); xv = rng.choice([1, sp.Rational(1, 2), r3])
    elif kind == 'asin':
        f = sp.asin(x); xv = rng.choice([sp.Rational(1, 2), r3 / 2, r2 / 2, sp.Rational(3, 5)])
    else:
        a = rng.choice([2, 3, 5, 10]); f = sp.Integer(a) ** x; xv = rng.choice([0, 1, 2, -1])
    g = sp.radsimp(sp.simplify(sp.diff(f, x).subs(x, xv)))
    return mk(f'Find the exact value of the gradient of y = {P(f)} at x = {P(xv)}.', P(g), f'dy/dx = {P(sp.diff(f, x))} (M1 A1); exact substitution (M1); {P(g)} (A1).', 4)


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def ahl_explain(rng, slot):
    a = rng.choice([2, 3, 5, 7, 10])
    kind = rng.choice(['ax', 'log', 'arc'])
    if kind == 'ax':
        return mk(f'By writing {a}ˣ as a power of e, explain why d/dx({a}ˣ) = {a}ˣ ln {a}.', f'{a}ˣ ln {a}', f'{a}ˣ = e^(x ln {a}) (M1); chain rule: ln {a} · e^(x ln {a}) (R1) = {a}ˣ ln {a} (A1).', 3, 'explain')
    if kind == 'log':
        return mk(f'Use the change of base formula to explain why d/dx(log_{a} x) = 1/(x ln {a}).', f'1/(x ln {a})', f'log_{a} x = ln x/ln {a} (M1); ln {a} is a constant (R1); derivative 1/(x ln {a}) (A1).', 3, 'explain')
    return mk(f'Explain why d/dx(arcsin(x/{a})) = 1/√({a * a} − x²).', f'1/√({a * a} − x²)', f'chain rule: (1/{a})·1/√(1 − x²/{a * a}) (M1 A1); simplify √(1 − x²/{a * a}) = √({a * a} − x²)/{a} (R1).', 3, 'explain')


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step', style='p3')
def arctan_proof_parts(rng, slot):
    a = rng.choice([1, 2, 3, 4])
    f = sp.atan(x / a) if a > 1 else sp.atan(x)
    d = sp.simplify(sp.diff(f, x))
    xv = rng.choice([a, a * r3, a / r3])
    g = sp.radsimp(d.subs(x, xv))
    parts = [('Given y = arctan x, show that dy/dx = 1/(1 + x²).', 'shown', 'tan y = x (M1); sec²y dy/dx = 1 (A1); sec²y = 1 + tan²y = 1 + x² (R1) AG', 3, True),
             (f'Hence find d/dx(arctan(x/{a})).' if a > 1 else 'Hence find d/dx(arctan x²).', P(d) if a > 1 else P(sp.diff(sp.atan(x ** 2), x)), 'chain rule (M1) A1', 2, True),
             (f'Find the exact gradient of y = {P(f)} at x = {P(xv)}.', P(g), 'substitute (A1)', 1, a > 1),
             ('Explain why the graph of y = arctan x has no stationary points.', '1/(1 + x²) > 0 for all x', 'R1', 1, False)]
    return build_parts(rng, ['This question concerns the derivative of the inverse tangent function.', 'Let y = arctan x, −π/2 < y < π/2.'], parts, 3)


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step', style='ext')
def sec_tan_parts(rng, slot):
    a = rng.choice([1, 2])
    f = sp.sec(a * x) + sp.tan(a * x)
    xv = rng.choice([pi / 6, pi / 4]) if a == 1 else rng.choice([pi / 12, pi / 8])
    d = sp.diff(f, x)
    g = sp.radsimp(sp.simplify(d.subs(x, xv)))
    parts = [('Find f′(x).', P(sp.simplify(d)), 'A1 A1', 2, True),
             (f'Show that f′(x) = {a}f(x)sec({a}x).' if a > 1 else 'Show that f′(x) = f(x) sec x.', 'shown', 'factorise sec(ax) (M1) A1 AG', 2, True),
             (f'Find the exact value of f′({P(xv)}).', P(g), 'substitute (M1) A1', 2, True),
             ('Explain why f is increasing on (−π/(2a), π/(2a)).'.replace('a)', f'{a})'), 'f(x) > 0 and sec(ax) > 0 there', 'R1 R1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}, for −π/{2 * a} < x < π/{2 * a}.', f'A function is defined by f(x) = {P(f)}, |x| < π/{2 * a}.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch06-st4', F(
    terms=[('implicit differentiation', 'differentiating both sides of an equation in x and y with respect to x, treating y as a function of x and using the chain rule for terms in y'),
           ('implicit function', 'a relation such as x² + y² = 25 where y is not given explicitly as a function of x')],
    facts=[('d/dx (y³) =', '3y² dy/dx', ['3y²', '3x²', 'y³ dy/dx'], 'Chain rule: y depends on x.'),
           ('d/dx (xy) =', 'y + x dy/dx', ['dy/dx', 'x + y dy/dx', '1'], 'Product rule.'),
           ('For the circle x² + y² = 25, dy/dx at (3, 4) is', '−3/4', ['3/4', '−4/3', '4/3'], 'dy/dx = −x/y.')],
    why=[('Explain why d/dx(y²) = 2y dy/dx and not 2y.', 'y is a function of x, so y² is a composite; by the chain rule d/dx(y²) = d/dy(y²) × dy/dx = 2y dy/dx.'),
         ('Explain why, at a point where a curve has a vertical tangent, the denominator of the implicit derivative is zero.', 'A vertical tangent has undefined gradient; dy/dx = N/D becomes infinite when D = 0 (and N ≠ 0).'),
         ('Explain why implicit differentiation is useful for the circle x² + y² = r².', 'Solving for y gives two branches ±√(r² − x²); implicit differentiation gives one formula dy/dx = −x/y valid on both.')],
    misc=[('Differentiating x² + y² = 9 gives 2x + 2y = 0.', 'The y term needs the chain rule: 2x + 2y dy/dx = 0.'),
          ('d/dx(3xy) = 3 dy/dx.', 'Product rule: 3y + 3x dy/dx.')],
))


def _implicit_curve(rng):
    kind = rng.choice(['conic', 'cubic', 'exp', 'trig'])
    while True:
        x0, y0 = nz(rng, -3, 3), nz(rng, -3, 3)
        if kind == 'conic':
            a, b, c = rng.randint(1, 3), nz(rng, -3, 3), rng.randint(1, 3)
            G = a * x ** 2 + b * x * y + c * y ** 2
        elif kind == 'cubic':
            a, b = nz(rng, -2, 2), nz(rng, -4, 4)
            G = x ** 3 + y ** 3 + b * x * y
        elif kind == 'exp':
            x0 = 0 if rng.random() < 0.5 else x0
            y0 = 0 if x0 != 0 else y0
            G = sp.exp(x * y) + x ** 2 + nz(rng, -3, 3) * y
        else:
            x0, y0 = 0, 0
            G = sp.sin(x + y) + nz(rng, 2, 4) * x * rng.choice([1, -1]) + y ** 2
        K = G.subs({x: x0, y: y0})
        Gy = sp.diff(G, y).subs({x: x0, y: y0})
        if Gy != 0:
            return G, K, x0, y0


@R.add('ch06-st4', 'C3', (1, 4), 'short')
def implicit_dydx(rng, slot):
    G, K, x0, y0 = _implicit_curve(rng)
    d = sp.simplify(-sp.diff(G, x) / sp.diff(G, y))
    return mk(f'Find dy/dx in terms of x and y for the curve {P(G)} = {P(K)}.', f'dy/dx = {P(sp.factor(d))}',
              f'Differentiate implicitly (M1); terms in y carry dy/dx and products use the product rule (A1 A1); rearrange: {P(sp.factor(d))} (A1).', 4)


@R.add('ch06-st4', 'C3', (2, 4), 'short', style='p1')
def implicit_tangent(rng, slot):
    G, K, x0, y0 = _implicit_curve(rng)
    m = sp.simplify((-sp.diff(G, x) / sp.diff(G, y)).subs({x: x0, y: y0}))
    want = rng.choice(['gradient', 'tangent', 'normal'])
    if want == 'gradient':
        ans = P(m)
    elif want == 'tangent':
        ans = line_eq(m, y0 - m * x0)
    else:
        if m == 0:
            ans = f'x = {x0}'
        else:
            ans = line_eq(-1 / m, y0 + x0 / m)
    q = {'gradient': 'Find the gradient of the curve', 'tangent': 'Find the equation of the tangent to the curve', 'normal': 'Find the equation of the normal to the curve'}[want]
    return mk(f'The point {pt([x0, y0])} lies on the curve {P(G)} = {P(K)}. {q} at this point.', ans,
              f'Implicit differentiation (M1 A1); substitute {pt([x0, y0])}: dy/dx = {P(m)} (A1)' + ('' if want == 'gradient' else f'; equation {ans} (M1 A1)'), 3 if want == 'gradient' else 5)


@R.add('ch06-st4', 'C2', (2, 4), 'explain')
def implicit_error(rng, slot):
    a, b = rng.randint(1, 5), nz(rng, -5, 5)
    G = a * x ** 2 + b * x * y + y ** 2
    nm = who(rng)
    return mk(f'{nm} differentiates {P(G)} = 10 term by term and writes {2 * a}x + {b} + 2y = 0. Explain the two errors and write the correct derivative equation.'.replace('+ -', '− '),
              f'{2 * a}x + {b}y + {b}x dy/dx + 2y dy/dx = 0'.replace('+ -', '− '),
              f'{P(b * x * y)} is a product: derivative {b}y + {b}x dy/dx (R1); y² gives 2y dy/dx by the chain rule (R1); correct equation (A1).', 3, 'explain', 'G2')


@R.add('ch06-st4', 'C4', (3, 5), 'multi_step', style='ext')
def implicit_horizontal(rng, slot):
    a, c = rng.randint(1, 3), rng.randint(1, 3)
    b = rng.choice([v for v in range(-3, 4) if v != 0 and v * v < 4 * a * c])
    K = rng.choice([4, 9, 12, 16, 24, 28])
    G = a * x ** 2 + b * x * y + c * y ** 2
    # horizontal tangents: dG/dx = 0 -> 2a x + b y = 0 -> x = -b y/(2a)
    yy = sp.solve(G.subs(x, -b * y / (2 * a)) - K, y)
    pts_ = [(sp.radsimp(-b * v / (2 * a)), sp.radsimp(v)) for v in yy]
    d = sp.simplify(-sp.diff(G, x) / sp.diff(G, y))
    parts = [('Find an expression for dy/dx in terms of x and y.', P(sp.factor(d)), 'implicit differentiation (M1) A1 A1', 3, True),
             (f'Show that at the points where the tangent is horizontal, {2 * a}x + {b}y = 0.'.replace('+ -', '− '), 'shown', 'numerator = 0 (M1) AG', 1, True),
             ('Hence find the exact coordinates of these points.', '; '.join(f'({P(p_)}, {P(q_)})' for p_, q_ in pts_), 'substitute into the curve (M1) A1 A1', 3, True),
             ('Find the coordinates of the points where the curve meets the x-axis and the gradient there.', '; '.join(f'({P(v)}, 0)' for v in sp.solve(G.subs(y, 0) - K, x)), 'y = 0 (M1) A1', 2, False)]
    return build_parts(rng, [f'A curve C has equation {P(G)} = {K}.', f'Consider the curve {P(G)} = {K}.', f'The ellipse E is given by {P(G)} = {K}.'], parts, 3)


@R.add('ch06-st4', 'C1', (1, 3), 'mcq')
def implicit_mcq(rng, slot):
    a = rng.randint(2, 6)
    kind = rng.choice(['xy', 'y3', 'ey', 'siny'])
    if kind == 'xy':
        return mcq(rng, f'Differentiating {a}xy with respect to x gives', f'{a}y + {a}x dy/dx', [f'{a} dy/dx', f'{a}x + {a}y dy/dx', f'{a}y dy/dx'], 'Product rule with y = y(x).')
    if kind == 'y3':
        return mcq(rng, f'Differentiating {a}y³ with respect to x gives', f'{3 * a}y² dy/dx', [f'{3 * a}y²', f'{a}y³ dy/dx', f'{3 * a}x²'], 'Chain rule.')
    if kind == 'ey':
        return mcq(rng, f'Differentiating e^({a}y) with respect to x gives', f'{a}e^({a}y) dy/dx', [f'{a}e^({a}y)', f'e^({a}y) dy/dx', f'{a}ye^({a}y − 1)'], 'Chain rule.')
    return mcq(rng, f'Differentiating sin({a}y) with respect to x gives', f'{a}cos({a}y) dy/dx', [f'{a}cos({a}y)', f'cos({a}y) dy/dx', f'−{a}cos({a}y) dy/dx'], 'Chain rule.')


# =============================================================================================
# ch07 Applications of differentiation
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('second derivative', "f″(x), the derivative of f′(x); it measures the rate of change of the gradient"),
           ('concave up', "a curve is concave up on an interval where f″(x) > 0: the gradient is increasing and the curve lies above its tangents"),
           ('concave down', "a curve is concave down where f″(x) < 0: the gradient is decreasing"),
           ('point of inflection', 'a point where the curve changes concavity, so f″ changes sign')],
    facts=[("If f″(x) > 0 on an interval then the graph of f′ is", 'increasing', ['decreasing', 'positive', 'zero'], 'f″ is the gradient of f′.'),
           ("f(x) = x⁴ has f″(0) = 0. At x = 0 the graph has", 'a minimum, not a point of inflection', ['a point of inflection', 'a maximum', 'a vertical tangent'], 'f″ = 12x² does not change sign.'),
           ("At a point of inflection on y = f(x), the graph of y = f′(x) has", 'a local maximum or minimum', ['a root', 'an asymptote', 'a point of inflection'], 'f′ changes from increasing to decreasing (or vice versa).'),
           ("Which notation represents the second derivative of y with respect to x?", 'd²y/dx²', ['(dy/dx)²', 'dy²/dx²', 'd²y/dx'], 'Leibniz notation.')],
    why=[("Explain why f″(a) = 0 is not sufficient for a point of inflection at x = a.", "Concavity must change, i.e. f″ must change sign; e.g. f(x) = x⁴ has f″(0) = 0 but f″ ≥ 0 on both sides, giving a minimum."),
         ("Explain how the graph of y = f′(x) can be used to find where f is concave down.", "f is concave down where f″ < 0, i.e. where the graph of y = f′(x) is decreasing."),
         ("Explain why every cubic f(x) = ax³ + bx² + cx + d has exactly one point of inflection.", "f″(x) = 6ax + 2b is linear with a ≠ 0, so it has exactly one zero, x = −b/(3a), and changes sign there.")],
    misc=[("If f″(x) < 0 then f is decreasing.", "f″ < 0 means the gradient is decreasing (concave down); f itself may still be increasing, e.g. √x."),
          ("A point of inflection must be a stationary point.", "Most points of inflection are non-stationary (e.g. x³ − 3x at x = 0 has gradient −3)."),
          ("d²y/dx² = (dy/dx)².", "d²y/dx² is the derivative of dy/dx, not its square; for y = x³, d²y/dx² = 6x but (dy/dx)² = 9x⁴.")],
))


def _poly_rand(rng, deg):
    co = [nz(rng, -3, 3)] + [rng.randint(-6, 6) for _ in range(deg)]
    return sum(c * x ** (deg - i) for i, c in enumerate(co))


@R.add('ch07-st1', 'C1', (1, 3), 'mcq')
def second_deriv_mcq(rng, slot):
    kind = rng.choice(['poly', 'exp', 'trig', 'pow'])
    f = {'poly': _poly_rand(rng, 3), 'exp': rng.randint(2, 5) * sp.exp(rng.choice([2, -1, 3]) * x), 'trig': rng.randint(2, 5) * sp.sin(rng.choice([2, 3]) * x), 'pow': rng.randint(2, 8) * x ** sp.Rational(rng.choice([1, 3, 5]), 2)}[kind]
    d2 = sp.diff(f, x, 2)
    wr = [P(sp.diff(f, x)), P(-d2), P(sp.diff(f, x) ** 2) if kind != 'poly' else P(d2 + 2), P(sp.diff(f, x, 3)) if sp.diff(f, x, 3) != 0 else P(d2 * 2)]
    return mcq(rng, f'Find d²y/dx² for y = {P(f)}.', P(d2), wr, f"dy/dx = {P(sp.diff(f, x))}, d²y/dx² = {P(d2)}.")


@R.add('ch07-st1', 'C3', (2, 4), 'short', style='p1')
def concavity_interval(rng, slot):
    a = nz(rng, -3, 3)
    p = rng.randint(-3, 3)
    b = -3 * a * p
    c, d = rng.randint(-6, 6), rng.randint(-6, 6)
    f = a * x ** 3 + b * x ** 2 + c * x + d
    want = rng.choice(['concave up', 'concave down'])
    up = f'x > {p}' if a > 0 else f'x < {p}'
    dn = f'x < {p}' if a > 0 else f'x > {p}'
    return mk(f'Find the set of values of x for which the graph of y = {P(f)} is {want}, and the coordinates of its point of inflection.',
              f'{(up if want == "concave up" else dn)}; inflection at ({p}, {P(f.subs(x, p))})'.replace('-', '−'),
              f"f″(x) = {P(sp.diff(f, x, 2))} (M1 A1); f″ {'>' if want == 'concave up' else '<'} 0 gives {(up if want == 'concave up' else dn)} (A1); f″ changes sign at x = {p}, y = {P(f.subs(x, p))} (A1).".replace('-', '−'), 4)


@R.add('ch07-st1', 'C3', (2, 4), 'short', style='p1')
def inflection_quartic(rng, slot):
    p, q = sorted(rng.sample(range(-3, 4), 2))
    a = rng.choice([1, -1, 2])
    # f'' = 12a(x-p)(x-q) -> f = a(x^4 - 2(p+q)x^3 + 6pq x^2)
    f = sp.expand(a * (x ** 4 - 2 * (p + q) * x ** 3 + 6 * p * q * x ** 2))
    return mk(f'Find the x-coordinates of the points of inflection of y = {P(f)}, justifying that they are points of inflection.', f'x = {p} and x = {q}',
              f"f″(x) = {P(sp.diff(f, x, 2))} = {12 * a}(x − ({p}))(x − ({q})) (M1 A1); f″ = 0 at x = {p}, {q} (A1); f″ changes sign at each (distinct simple roots) (R1).", 4)


@R.add('ch07-st1', 'C2', (2, 4), 'explain')
def concavity_explain(rng, slot):
    kind = rng.choice(['x4', 'graph', 'sign'])
    n = rng.choice([4, 6])
    if kind == 'x4':
        return mk(f'Explain why the curve y = x{str(n).translate(_SUP)} does not have a point of inflection at the origin, even though d²y/dx² = 0 there.', 'f″ does not change sign',
                  f"d²y/dx² = {n * (n - 1)}x{str(n - 2).translate(_SUP)} ≥ 0 on both sides of 0 (A1 R1); concavity does not change, so no inflection (it is a minimum) (R1).", 3, 'explain')
    if kind == 'graph':
        p, q = sorted(rng.sample(range(-4, 5), 2))
        return mk(f"The graph of y = f′(x) has a local maximum at x = {p} and a local minimum at x = {q}. Explain what happens on the graph of y = f at these x-values.", 'points of inflection',
                  f"At x = {p} and x = {q}, f′ changes from increasing to decreasing / decreasing to increasing, so f″ changes sign (R1 R1); hence f has points of inflection there (A1).", 3, 'explain')
    a = rng.randint(1, 5)
    return mk(f"For x > 0, f(x) = {a}√x. Explain why f is increasing but concave down for all x > 0.", 'f′ > 0, f″ < 0',
              f"f′(x) = {P(sp.Rational(a, 2))}x^(−1/2) > 0 (A1 R1); f″(x) = {P(-sp.Rational(a, 4))}x^(−3/2) < 0 (A1 R1).", 4, 'explain')


def _concave_down(f2, pos):
    xr = sp.Symbol('xr', real=True)
    S = sp.solve_univariate_inequality(f2.subs(x, xr) < 0, xr, relational=False)
    if pos:
        S = S.intersect(sp.Interval.open(0, sp.oo))
    return S


def _iv_txt(S):
    parts = S.args if isinstance(S, sp.Union) else [S]
    out = []
    for I in parts:
        a, b = I.start, I.end
        if a == -sp.oo:
            out.append(f'x < {P(b)}')
        elif b == sp.oo:
            out.append(f'x > {P(a)}')
        else:
            out.append(f'{P(a)} < x < {P(b)}')
    return ' or '.join(out)


@R.add('ch07-st1', 'C4', (3, 5), 'multi_step', style='ext')
def second_deriv_parts(rng, slot):
    kind = rng.choice(['xe', 'gauss', 'lnx'])
    a = rng.choice([1, 2, 3])
    if kind == 'xe':
        f = x * sp.exp(-x / a) if a > 1 else x * sp.exp(-x)
    elif kind == 'gauss':
        f = sp.exp(-x ** 2 / (2 * a)) if a > 1 else sp.exp(-x ** 2)
    else:
        f = sp.log(x) / x ** a if a < 3 else x ** 2 * sp.log(x)
    f1, f2 = sp.factor(sp.diff(f, x)), sp.factor(sp.diff(f, x, 2))
    infl = [v for v in sp.solve(sp.diff(f, x, 2), x) if v.is_real and (kind != 'lnx' or v > 0)]
    parts = [('Find f′(x).', P(f1), 'product/chain/quotient rule (M1) A1', 2, True),
             (f'Show that f″(x) = {P(f2)}.', 'shown', 'differentiate again (M1) A1 AG', 2, True),
             ('Find the exact x-coordinate(s) of the point(s) of inflection of the graph of f.', lst(sorted(infl, key=float)), 'f″(x) = 0 (M1) A1; sign change justified (R1)', 3, True),
             ('State the set of values of x for which the graph of f is concave down.', _iv_txt(_concave_down(f2, kind == 'lnx')), 'f″(x) < 0 (M1) A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}{", x > 0" if kind == "lnx" else ""}.', f'The function f is defined by f(x) = {P(f)}{" for x > 0" if kind == "lnx" else ""}.'], parts, 3)


@R.add('ch07-st1', 'C4', (3, 5), 'multi_step', style='p1')
def cubic_full_parts(rng, slot):
    f, p, q, kk = _cubic_from_roots(rng)
    xi = sp.Rational(p + q, 2)
    parts = [("Find f′(x) and f″(x).", f"f′(x) = {P(sp.diff(f, x))}, f″(x) = {P(sp.diff(f, x, 2))}", 'A1 A1', 2, True),
             ('Find the coordinates of the stationary points and use f″ to classify them.', f"({p}, {P(f.subs(x, p))}) {'max' if kk > 0 else 'min'}, ({q}, {P(f.subs(x, q))}) {'min' if kk > 0 else 'max'}", 'f′ = 0 (M1) A1 A1; f″ sign (R1 R1)', 5, True),
             ('Find the coordinates of the point of inflection.', pt([xi, f.subs(x, xi)]), 'f″ = 0 (M1) A1', 2, True),
             ('Show that the point of inflection is the midpoint of the two stationary points.', 'shown', 'midpoint calculation (M1) AG (A1)', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}.', f'Consider the cubic curve y = {P(f)}.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch07-st2', F(
    terms=[('local maximum', 'a point where f changes from increasing to decreasing; f′ = 0 and f″ < 0 is sufficient'),
           ('local minimum', 'a point where f changes from decreasing to increasing; f′ = 0 and f″ > 0 is sufficient'),
           ('optimisation', 'finding the maximum or minimum value of a quantity, usually by expressing it as a function of one variable and solving f′ = 0'),
           ('global maximum', 'the largest value of f on its whole domain, which may occur at a stationary point or at an endpoint')],
    facts=[("If f′(a) = 0 and f″(a) < 0 then at x = a f has", 'a local maximum', ['a local minimum', 'a point of inflection', 'a root'], 'Concave down at a stationary point.'),
           ("A rectangle has perimeter 40 cm. Its maximum possible area is", '100 cm²', ['400 cm²', '80 cm²', '200 cm²'], 'A = x(20 − x) is maximised at x = 10.'),
           ("On a closed interval, the global minimum of a function can occur", 'at a stationary point or at an endpoint', ['only at a stationary point', 'only where f = 0', 'only at an endpoint'], 'Always check endpoints.')],
    why=[('Explain why, in an optimisation problem, you should check the endpoints of the domain.', 'The greatest or least value on a closed interval may occur at an endpoint where f′ ≠ 0, not only at a stationary point.'),
         ('Explain how the second derivative test classifies a stationary point.', 'At a stationary point, f″ < 0 means concave down so a maximum; f″ > 0 means concave up so a minimum; f″ = 0 is inconclusive and the sign of f′ must be checked.'),
         ('Explain why an optimisation problem must be reduced to a function of one variable before differentiating.', 'Ordinary differentiation finds rates with respect to one variable; constraints are used to eliminate the others so that a single derivative can be set to zero.')],
    misc=[("If f″(a) = 0 at a stationary point, it must be a point of inflection.", "The test is inconclusive: x⁴ has f′(0) = f″(0) = 0 but a minimum; use the sign of f′ either side."),
          ("The maximum value of a function is the x-value of the stationary point.", "The maximum value is f at that point (the y-value); the x-value is where it occurs.")],
))


@R.add('ch07-st2', 'C3', (1, 4), 'short', style='p1')
def stationary_classify(rng, slot):
    f, p, q, kk = _cubic_from_roots(rng)
    return mk(f'Find the coordinates of the stationary points of the curve y = {P(f)} and determine their nature.',
              f"({p}, {P(f.subs(x, p))}) local {'maximum' if kk > 0 else 'minimum'}; ({q}, {P(f.subs(x, q))}) local {'minimum' if kk > 0 else 'maximum'}",
              f"dy/dx = {P(sp.diff(f, x))} (A1); = 0 at x = {p}, {q} (M1 A1); y-values (A1); d²y/dx² = {P(sp.diff(f, x, 2))}: {P(sp.diff(f, x, 2).subs(x, p))} at x = {p}, {P(sp.diff(f, x, 2).subs(x, q))} at x = {q} (M1 R1).", 6)


@R.add('ch07-st2', 'C1', (1, 3), 'mcq')
def stationary_mcq(rng, slot):
    a = nz(rng, -5, 5)
    b = rng.randint(-8, 8)
    c = rng.randint(-5, 5)
    f = a * x ** 2 + b * x + c
    xs_ = sp.Rational(-b, 2 * a)
    return mcq(rng, f'The curve y = {P(f)} has a stationary point at', pt([xs_, f.subs(x, xs_)]), [pt([-xs_, f.subs(x, -xs_)]), pt([xs_, c]), pt([sp.Rational(b, a), f.subs(x, sp.Rational(b, a))])],
               f'dy/dx = {P(sp.diff(f, x))} = 0 at x = {P(xs_)}.')


@R.add('ch07-st2', 'C3', (2, 5), 'short', style='p2')
def optim_box(rng, slot):
    L, W = rng.randint(20, 60), rng.randint(15, 50)
    V = x * (L - 2 * x) * (W - 2 * x)
    crit = [float(v) for v in sp.solve(sp.diff(V, x), x) if 0 < float(v) < min(L, W) / 2]
    if not crit:
        return None
    xc = crit[0]
    Vm = float(V.subs(x, xc))
    ctx = rng.choice(['sheet of cardboard', 'sheet of metal', 'piece of card'])
    return mk(f'A rectangular {ctx} measures {L} cm by {W} cm. Equal squares of side x cm are cut from each corner and the sides are folded up to make an open box. Find the value of x that maximises the volume, and the maximum volume.',
              f'x = {s3(xc)} cm, V = {s3(Vm)} cm³', f'V = x({L} − 2x)({W} − 2x) (M1 A1); dV/dx = 0 or GDC maximum (M1); x = {s3(xc)} (A1); V = {s3(Vm)} cm³ (A1).', 5)


@R.add('ch07-st2', 'C3', (2, 4), 'short', style='p1')
def optim_fence(rng, slot):
    Ltot = rng.choice([40, 60, 80, 100, 120, 200, 240])
    kind = rng.choice(['wall', 'divided', 'rect'])
    if kind == 'wall':
        xo = sp.Rational(Ltot, 4)
        A = xo * (Ltot - 2 * xo)
        stem = f'A farmer in {rng.choice(CITIES)} has {Ltot} m of fencing to enclose a rectangular field against a straight wall (no fence needed along the wall). Find the dimensions that maximise the area and the maximum area.'
        ans = f'{P(xo)} m by {P(Ltot - 2 * xo)} m (parallel to the wall); area {P(A)} m²'
        key = f'Let the sides perpendicular to the wall be x: A = x({Ltot} − 2x) (M1 A1); dA/dx = {Ltot} − 4x = 0 (M1); x = {P(xo)} (A1); area {P(A)} m² (A1).'
    elif kind == 'divided':
        xo = sp.Rational(Ltot, 6)
        y_ = sp.Rational(Ltot - 4 * xo, 2) if False else sp.Rational(Ltot, 4)
        # 3 widths x + 2 lengths y? use: 2y + 3x = Ltot -> A = x y = x (Ltot - 3x)/2, max at x = Ltot/6
        y_ = sp.Rational(Ltot - 3 * xo, 2)
        A = xo * y_
        stem = f'A rectangular enclosure is divided into two equal pens by a fence parallel to one side. The total length of fencing is {Ltot} m. Find the maximum total area.'
        ans = f'{P(A)} m² (sides {P(xo)} m and {P(y_)} m)'
        key = f'3x + 2y = {Ltot} (M1); A = x({Ltot} − 3x)/2 (A1); dA/dx = 0 (M1); x = {P(xo)}, y = {P(y_)} (A1); A = {P(A)} (A1).'
    else:
        Aval = rng.choice([100, 144, 400, 900, 625])
        s_ = sp.sqrt(Aval)
        stem = f'A rectangle has area {Aval} m². Show that its perimeter is least when it is a square, and find this least perimeter.'
        ans = f'{P(4 * s_)} m'
        key = f'P = 2x + 2({Aval}/x) (M1 A1); dP/dx = 2 − {2 * Aval}/x² = 0 (M1); x = {P(s_)} so y = {P(s_)} (A1); second derivative positive (R1); P = {P(4 * s_)} (A1).'
    return mk(stem, ans, key, 5)


@R.add('ch07-st2', 'C2', (2, 4), 'explain')
def stationary_explain(rng, slot):
    f, p, q, kk = _cubic_from_roots(rng)
    lo, hi = p - rng.randint(1, 3), q + rng.randint(1, 3)
    vals = {v: f.subs(x, v) for v in (lo, p, q, hi)}
    gmax = max(vals, key=lambda v: vals[v])
    return mk(f'f(x) = {P(f)} on the domain {lo} ≤ x ≤ {hi}. {who(rng)} says the greatest value of f is at the local maximum. Explain whether this is correct and find the greatest value of f.',
              f'greatest value {P(vals[gmax])} at x = {gmax}', f"Local max/min at x = {p}, {q} (A1); compare with endpoints f({lo}) = {P(vals[lo])}, f({hi}) = {P(vals[hi])} (M1 R1); greatest value {P(vals[gmax])} at x = {gmax} (A1).", 4, 'explain')


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step', style='ext')
def optim_cylinder(rng, slot):
    V = rng.choice([250, 500, 1000, 330, 750, 2000])
    kind = rng.choice(['closed', 'open'])
    r = sp.Symbol('r', positive=True)
    h = V / (pi * r ** 2)
    A = 2 * pi * r ** 2 + 2 * pi * r * h if kind == 'closed' else pi * r ** 2 + 2 * pi * r * h
    rc = sp.solve(sp.diff(A, r), r)[0]
    Am = sp.simplify(A.subs(r, rc))
    ctx = rng.choice(['A drinks can', 'A food tin', 'A cylindrical water tank', 'A paint pot'])
    parts = [(f'Show that the surface area is A = {P(sp.simplify(A))}.', 'shown', f'V = πr²h = {V} so h = {V}/(πr²) (M1); substitute into the area formula (A1) AG', 2, True),
             ('Find dA/dr.', P(sp.diff(A, r)), 'A1 A1', 2, True),
             ('Find the value of r that minimises A, justifying that it is a minimum.', f'r = {s3(rc)} cm', f'dA/dr = 0 (M1); r = ({V}/{"2" if kind == "closed" else ""}π)^(1/3) = {s3(rc)} (A1); d²A/dr² > 0 (R1)', 3, True),
             ('Find the minimum surface area.', f'{s3(Am)} cm²', 'substitute (A1)', 1, True),
             ('Find the ratio h : r for the optimal shape.', ('2 : 1' if kind == 'closed' else '1 : 1'), 'A1', 1, False)]
    return build_parts(rng, [f'{ctx} is a {"closed" if kind == "closed" else "open-topped"} cylinder of radius r cm and height h cm with volume {V} cm³.',
                             f'A manufacturer designs {"a closed" if kind == "closed" else "an open"} cylindrical container holding {V} cm³, with radius r cm and height h cm.'], parts, 4)


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step', style='p2')
def optim_profit(rng, slot):
    a, b, c = round(rng.uniform(0.002, 0.02), 3), rng.randint(5, 40), rng.randint(100, 900)
    p_ = rng.randint(60, 150)
    q = sp.Symbol('q', positive=True)
    C = a * q ** 3 - b * q ** 2 / 10 + 20 * q + c
    Pr = p_ * q - C
    crit = [float(v) for v in sp.solve(sp.diff(Pr, q), q) if v.is_real and v > 0]
    if not crit:
        return None
    qc = max(crit)
    if float(sp.diff(Pr, q, 2).subs(q, qc)) >= 0:
        return None
    parts = [('Write down an expression for the profit P(q).', P(sp.expand(Pr)), 'P = Rq − C (M1) A1', 2, True),
             ('Find the number of units that maximises profit.', s3(qc), "P′(q) = 0 (M1) GDC (A1); P″ < 0 (R1)", 3, True),
             ('Find the maximum profit.', s3(float(Pr.subs(q, qc))), 'A1', 1, True),
             ('Find the rate of change of cost when q = 50 and interpret it.', s3(float(sp.diff(C, q).subs(q, 50))), 'C′(50) (M1) A1; marginal cost per unit (R1)', 3, False)]
    return build_parts(rng, [f'A company sells each unit for ${p_}. The cost of producing q units is C(q) = {a}q³ − {b / 10}q² + 20q + {c} dollars.',
                             f'The weekly cost (in dollars) of making q items is C(q) = {a}q³ − {b / 10}q² + 20q + {c}; each item sells for ${p_}.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch07-st3', F(
    terms=[('related rates', 'rates of change of two or more quantities linked by an equation, related through the chain rule, e.g. dV/dt = (dV/dr)(dr/dt)'),
           ('chain rule for rates', 'dy/dt = (dy/dx)(dx/dt)')],
    facts=[('A spherical balloon has dV/dt = 10 cm³ s⁻¹. To find dr/dt you use', 'dr/dt = (dV/dt)/(dV/dr)', ['dr/dt = (dV/dt)(dV/dr)', 'dr/dt = dV/dt', 'dr/dt = V/t'], 'Chain rule: dV/dt = (dV/dr)(dr/dt).'),
           ('The area of a circle increases at 6 cm² s⁻¹. When r = 3, dr/dt =', '1/π cm s⁻¹', ['π cm s⁻¹', '6 cm s⁻¹', '1/(3π) cm s⁻¹'], 'dA/dt = 2πr dr/dt: 6 = 6π dr/dt.'),
           ('If a quantity is decreasing, its rate of change is', 'negative', ['positive', 'zero', 'undefined'], 'Decreasing quantities have negative derivatives.')],
    why=[('Explain why the rate at which the radius of an inflating balloon grows decreases even if air is pumped in at a constant rate.', 'dr/dt = (dV/dt)/(4πr²); with dV/dt constant, dr/dt falls as r increases because the same volume spreads over a larger surface.'),
         ('Explain why you should substitute numerical values only after differentiating in a related-rates problem.', 'Substituting a fixed value first turns a variable into a constant, whose derivative is zero; the relationship must be differentiated while the quantities are still variables.'),
         ('Explain why, for a ladder sliding down a wall, the top and bottom move with rates of opposite sign.', 'x² + y² = L² gives 2x dx/dt + 2y dy/dt = 0, so dy/dt = −(x/y)dx/dt; as the foot moves out (dx/dt > 0) the top moves down.')],
    misc=[('If dV/dt is constant then dr/dt is constant for a sphere.', 'dr/dt = (dV/dt)/(4πr²) depends on r, so it changes as the sphere grows.'),
          ('In related rates you can substitute r = 5 into V = (4/3)πr³ before differentiating.', 'Then V would be a constant and dV/dt = 0; differentiate first, then substitute.')],
))


@R.add('ch07-st3', 'C3', (2, 5), 'short', style='p1')
def rr_sphere_circle(rng, slot):
    kind = rng.choice(['sphere_r', 'sphere_area', 'circle', 'cube', 'square'])
    rate = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 20])
    r0 = rng.choice([2, 3, 4, 5, 6, 10])
    if kind == 'sphere_r':
        ans = sp.Rational(rate, 4 * r0 ** 2) / pi
        stem = f'Air is pumped into a spherical balloon at {rate} cm³ s⁻¹. Find the exact rate at which the radius is increasing when r = {r0} cm.'
        key = f'V = (4/3)πr³, dV/dr = 4πr² (A1); dr/dt = (dV/dt)/(dV/dr) (M1) = {rate}/(4π × {r0 ** 2}) (A1) = {P(ans)} cm s⁻¹ (A1).'
        a_ = f'{P(ans)} cm s⁻¹'
    elif kind == 'sphere_area':
        drdt = sp.Rational(rate, 10)
        ans = 8 * pi * r0 * drdt
        stem = f'The radius of a spherical snowball decreases at {P(drdt)} cm per minute as it melts. Find the exact rate of change of its surface area when the radius is {r0} cm.'
        key = f'S = 4πr², dS/dr = 8πr (A1); dS/dt = 8πr × (−{P(drdt)}) (M1 A1) = −{P(ans)} cm² min⁻¹ (A1).'
        a_ = f'−{P(ans)} cm² min⁻¹ (decreasing)'
    elif kind == 'circle':
        ans = sp.Rational(rate, 2 * r0) / pi
        stem = f'A stone is dropped into a pond and the area of the circular ripple increases at {rate} m² s⁻¹. Find the exact rate of increase of the radius when the radius is {r0} m.'
        key = f'A = πr², dA/dr = 2πr (A1); dr/dt = {rate}/(2π × {r0}) (M1 A1) = {P(ans)} m s⁻¹ (A1).'
        a_ = f'{P(ans)} m s⁻¹'
    elif kind == 'cube':
        ans = sp.Rational(rate, 3 * r0 ** 2)
        stem = f'The volume of a cube increases at {rate} cm³ s⁻¹. Find the rate of increase of the edge length when the edge is {r0} cm.'
        key = f'V = x³, dV/dx = 3x² (A1); dx/dt = {rate}/(3 × {r0 ** 2}) (M1 A1) = {P(ans)} cm s⁻¹ (A1).'
        a_ = f'{P(ans)} cm s⁻¹'
    else:
        ans = 2 * r0 * rate
        stem = f'The side of a square metal plate expands at {rate} mm per minute when heated. Find the rate of increase of its area when the side is {r0 * 10} mm.'
        ans = 2 * r0 * 10 * rate
        key = f'A = s², dA/ds = 2s (A1); dA/dt = 2({r0 * 10})({rate}) (M1 A1) = {ans} mm² min⁻¹ (A1).'
        a_ = f'{ans} mm² min⁻¹'
    return mk(stem, a_, key, 4)


@R.add('ch07-st3', 'C3', (2, 5), 'short', style='p2')
def rr_ladder(rng, slot):
    L = rng.choice([5, 6, 8, 10, 13, 15, 25])
    xx = rng.choice([v for v in range(2, L) if v < L])
    yy = math.sqrt(L * L - xx * xx)
    rate = rng.choice([0.2, 0.3, 0.5, 0.4, 1.0, 1.5])
    dy = -(xx / yy) * rate
    return mk(f'A ladder {L} m long leans against a vertical wall. The foot of the ladder slides away from the wall at {rate} m s⁻¹. Find the rate at which the top of the ladder is sliding down the wall when the foot is {xx} m from the wall.',
              f'{s3(abs(dy))} m s⁻¹ (downwards)', f'x² + y² = {L * L} (M1); 2x dx/dt + 2y dy/dt = 0 (M1 A1); y = {s3(yy)} (A1); dy/dt = −({xx}/{s3(yy)})({rate}) = {s3(dy)} (A1).', 5)


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step', style='ext')
def rr_cone(rng, slot):
    R_, H = rng.choice([(3, 6), (4, 8), (5, 10), (2, 6), (3, 9), (6, 8), (4, 10)])
    rate = rng.choice([2, 3, 5, 10, 12, 15])
    h0 = rng.choice([v for v in range(2, H)])
    hh = sp.Symbol('h', positive=True)
    k = sp.Rational(R_, H)
    Vh = pi * k ** 2 * hh ** 3 / 3
    dhdt = sp.Rational(rate) / sp.diff(Vh, hh).subs(hh, h0)
    parts = [(f'Show that, when the depth of water is h cm, the volume is V = {P(Vh)}.', 'shown', f'similar triangles r/h = {R_}/{H} (M1); V = (1/3)πr²h (A1) AG', 2, True),
             (f'Find the exact rate at which the depth is increasing when h = {h0} cm.', f'{P(dhdt)} cm s⁻¹', f'dV/dh = {P(sp.diff(Vh, hh))} (A1); dh/dt = {rate}/(dV/dh) (M1) = {P(dhdt)} (A1)', 3, True),
             (f'Find the rate at which the surface radius is increasing at that moment.', f'{P(k * dhdt)} cm s⁻¹', f'r = {P(k)}h so dr/dt = {P(k)} dh/dt (M1) A1', 2, False),
             ('Explain why dh/dt decreases as the cone fills.', 'dh/dt = (dV/dt)/(πr²); the surface area grows', 'R1', 1, False)]
    return build_parts(rng, [f'Water is poured at {rate} cm³ s⁻¹ into an inverted conical funnel of radius {R_} cm and height {H} cm.',
                             f'A conical tank, vertex down, has top radius {R_} cm and height {H} cm. Water flows in at a constant {rate} cm³ s⁻¹.'], parts, 3)


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step', style='p2')
def rr_shadow_plane(rng, slot):
    kind = rng.choice(['shadow', 'plane'])
    if kind == 'shadow':
        H, h = rng.choice([(6, 1.8), (5, 1.6), (8, 1.7), (4.5, 1.5)])
        v = rng.choice([1.2, 1.5, 2.0, 0.8])
        ds = h * v / (H - h)
        parts = [(f'Show that the length s of the shadow satisfies s = {h}x/({H} − {h}), where x is the distance from the foot of the lamp post.', 'shown', 'similar triangles (M1) A1 AG', 2, True),
                 ('Find the rate at which the shadow is lengthening.', f'{s3(ds)} m s⁻¹', 'differentiate with respect to t (M1) A1', 2, True),
                 ('Find the rate at which the tip of the shadow moves.', f'{s3(v + ds)} m s⁻¹', 'tip = x + s (M1) A1', 2, True)]
        return build_parts(rng, [f'A person {h} m tall walks away from a lamp post of height {H} m at {v} m s⁻¹.', f'{who(rng)}, who is {h} m tall, walks directly away from a {H} m street light at {v} m s⁻¹.'], parts, 3)
    alt = rng.choice([3, 4, 5, 6])
    sp_ = rng.choice([400, 500, 600, 700])
    d = rng.choice([v for v in (4, 5, 6, 8, 10, 12) if v > alt])
    gx = math.sqrt(d * d - alt * alt)
    rate = gx / d * sp_
    parts = [('Show that the horizontal distance x and the direct distance s from the radar satisfy s² = x² + ' + f'{alt * alt}.', 'shown', 'Pythagoras (A1) AG', 1, True),
             (f'Find the rate at which s is increasing when s = {d} km.', f'{s3(rate)} km h⁻¹', 'differentiate implicitly (M1 A1); x = ' + s3(gx) + ' (A1); ds/dt (A1)', 4, True),
             ('Find the rate of change of the angle of elevation of the plane from the radar at that moment, in radians per hour.', s3(-alt * sp_ / (gx * gx + alt * alt)), 'tan θ = h/x (M1); differentiate (A1); value (A1)', 3, False)]
    return build_parts(rng, [f'A plane flies horizontally at an altitude of {alt} km at {sp_} km h⁻¹ directly away from a radar station.', f'An aircraft at constant height {alt} km moves away from a ground radar at {sp_} km h⁻¹.'], parts, 2)


@R.add('ch07-st3', 'C2', (2, 4), 'explain')
def rr_explain(rng, slot):
    rate = rng.randint(2, 20)
    r1, r2 = rng.sample([1, 2, 3, 4, 5, 6, 8, 10], 2)
    d1, d2 = sp.Rational(rate, 4 * r1 ** 2) / pi, sp.Rational(rate, 4 * r2 ** 2) / pi
    return mk(f'Gas is pumped into a spherical balloon at a constant {rate} cm³ s⁻¹. Explain why the radius grows faster when r = {min(r1, r2)} cm than when r = {max(r1, r2)} cm, supporting your answer with calculations.',
              f'dr/dt = {P(d1 if r1 < r2 else d2)} vs {P(d2 if r1 < r2 else d1)}', f'dr/dt = {rate}/(4πr²) (M1 A1); decreases as r increases (R1); values {P(d1)} at r = {r1}, {P(d2)} at r = {r2} (A1).', 4, 'explain')


@R.add('ch07-st3', 'C1', (1, 3), 'mcq')
def rr_mcq(rng, slot):
    a = rng.randint(2, 9)
    r0 = rng.randint(2, 6)
    return mcq(rng, f'The radius of a circle increases at {a} cm s⁻¹. At the instant r = {r0} cm, the area is increasing at', f'{2 * a * r0}π cm² s⁻¹',
               [f'{a * r0 * r0}π cm² s⁻¹', f'{a * r0}π cm² s⁻¹', f'{2 * a}π cm² s⁻¹'], f'dA/dt = 2πr dr/dt = 2π({r0})({a}).')


# ---------------------------------------------------------------------------------------------
R.facts('ch07-st4', F(
    terms=[('vertical asymptote', 'a line x = a near which |f(x)| → ∞; for rational functions, a zero of the denominator that is not cancelled'),
           ('horizontal asymptote', 'a line y = b that f(x) approaches as x → ±∞'),
           ('oblique asymptote', 'a non-horizontal line y = mx + c that the graph approaches as x → ±∞, found by polynomial division'),
           ('key features of a graph', 'intercepts, asymptotes, stationary points, points of inflection, and behaviour as x → ±∞')],
    facts=[('The graph of y = (2x + 1)/(x − 3) has horizontal asymptote', 'y = 2', ['y = 3', 'x = 3', 'y = −1/3'], 'Ratio of leading coefficients as x → ∞.'),
           ('Which function has an oblique asymptote?', 'y = (x² + 1)/x', ['y = (x + 1)/x', 'y = 1/(x² + 1)', 'y = eˣ'], 'Numerator degree is one more than the denominator degree.'),
           ('The graph of y = x e⁻ˣ approaches which asymptote as x → ∞?', 'y = 0', ['y = 1', 'x = 0', 'y = x'], 'e⁻ˣ dominates.')],
    why=[('Explain how to find the vertical asymptotes of a rational function.', 'Factorise and cancel common factors; the remaining zeros of the denominator give vertical asymptotes because the function grows without bound there.'),
         ('Explain why y = (ax + b)/(cx + d) has horizontal asymptote y = a/c.', 'Divide numerator and denominator by x: (a + b/x)/(c + d/x) → a/c as x → ±∞.'),
         ('Explain why technology alone may give a misleading sketch of a function.', 'A GDC window may hide asymptotic behaviour, merge close stationary points or miss features outside the window; analysis with derivatives and limits confirms the key features.')],
    misc=[('y = (x² − 4)/(x − 2) has a vertical asymptote at x = 2.', 'It simplifies to x + 2 for x ≠ 2: there is a hole at (2, 4), not an asymptote.'),
          ('A graph can never cross its horizontal asymptote.', 'It can cross it for finite x; the asymptote only describes behaviour as x → ±∞ (e.g. y = x/(x² + 1) crosses y = 0).')],
))


@R.add('ch07-st4', 'C3', (1, 4), 'short', style='p1')
def asymptotes_rational(rng, slot):
    a, b, c, d = nz(rng, -5, 5), rng.randint(-6, 6), nz(rng, -3, 3), rng.randint(-6, 6)
    if a * d - b * c == 0:
        return None
    f = (a * x + b) / (c * x + d)
    return mk(f'Write down the equations of the asymptotes of the graph of y = ({P(a * x + b)})/({P(c * x + d)}), and find its axis intercepts.',
              f'x = {P(sp.Rational(-d, c))}, y = {P(sp.Rational(a, c))}; intercepts ' + ('(0, 0)' if b == 0 else f'({P(sp.Rational(-b, a))}, 0)' + (f', (0, {P(sp.Rational(b, d))})' if d != 0 else ' (no y-intercept)')),
              f'Vertical: {P(c * x + d)} = 0 (A1); horizontal y = {a}/{c} (A1); x-intercept from numerator (A1); y-intercept at x = 0 (A1).', 4)


@R.add('ch07-st4', 'C3', (3, 5), 'short', style='p1')
def oblique(rng, slot):
    p = nz(rng, -4, 4)
    m, c = nz(rng, -3, 3), rng.randint(-5, 5)
    r_ = nz(rng, -6, 6)
    num = sp.expand((m * x + c) * (x - p) + r_)
    return mk(f'Find the equations of all asymptotes of the graph of y = ({P(num)})/({P(x - p)}).', f'x = {p}; {line_eq(m, c)}',
              f'Vertical asymptote x = {p} (A1); polynomial division: {P(num)} = ({P(m * x + c)})({P(x - p)}) + {r_} (M1 A1); oblique asymptote {line_eq(m, c)} (A1).', 4)


@R.add('ch07-st4', 'C3', (2, 4), 'short', style='p2')
def sketch_gdc(rng, slot):
    a = rng.randint(1, 4)
    b = round(rng.uniform(0.5, 2), 1)
    kind = rng.choice(['xexp', 'lnx', 'trigexp'])
    f = {'xexp': x ** 2 * sp.exp(-b * x) - a / 10, 'lnx': x * sp.log(x) - b, 'trigexp': sp.exp(-x / 2) * sp.sin(a * x)}[kind]
    g = sp.lambdify(x, sp.diff(f, x), 'math')
    lo, hi = (0.05, 6)
    roots = nsols(g, lo, hi)
    if not roots:
        return None
    r0 = roots[0]
    return mk(f'Use your GDC to sketch y = {P(f)} for 0 < x ≤ 6, and find the coordinates of the first stationary point.',
              f'({s3(r0)}, {s3(float(f.subs(x, r0)))})', f'Correct shape on the domain (A1 A1); stationary point by GDC (M1) ({s3(r0)}, {s3(float(f.subs(x, r0)))}) (A1).', 4)


@R.add('ch07-st4', 'C2', (2, 4), 'explain')
def hole_explain(rng, slot):
    p = nz(rng, -5, 5)
    q = rng.choice([v for v in range(-5, 6) if v != p])
    num = sp.expand((x - p) * (x - q))
    return mk(f'Explain why the graph of y = ({P(num)})/({P(x - p)}) has no vertical asymptote at x = {p}, and describe its graph.', f'straight line y = {P(x - q)} with a hole at ({p}, {p - q})',
              f'Factorise the numerator: (x − ({p}))(x − ({q})) (M1); cancel for x ≠ {p} (R1); graph is y = {P(x - q)} with the point ({p}, {p - q}) missing (A1).', 3, 'explain')


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step', style='ext')
def sketch_rational_full(rng, slot):
    a = rng.choice([1, 2, 3, 4, 5])
    kind = rng.choice(['quad_over_lin', 'lin_over_quad'])
    if kind == 'quad_over_lin':
        f = (x ** 2 + a) / x
        st = [v for v in sp.solve(sp.diff(f, x), x) if v.is_real]
        asym = 'x = 0 and y = x'
    else:
        f = a * x / (x ** 2 + 1)
        st = sp.solve(sp.diff(f, x), x)
        asym = 'y = 0'
    sts = '; '.join(f'({P(v)}, {P(sp.simplify(f.subs(x, v)))})' for v in sorted(st, key=float))
    parts = [('Find the equations of the asymptotes of the graph of f.', asym, 'A1 A1', 2, True),
             ('Find f′(x).', P(sp.factor(sp.diff(f, x))), 'quotient rule (M1) A1', 2, True),
             ('Find the exact coordinates of the stationary points and classify them.', sts, 'f′ = 0 (M1) A1 A1; nature (R1)', 4, True),
             ('Hence sketch the graph of f, showing the features found.', 'sketch with asymptotes, stationary points, symmetry (odd function)', 'A1 A1 A1', 3, False),
             ('State the range of f.', 'see the stationary values', 'A1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}{", x ≠ 0" if kind == "quad_over_lin" else ""}.', f'Consider the function f(x) = {P(f)}.'], parts, 3)


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step', style='p2')
def sketch_exp_full(rng, slot):
    a = rng.choice([1, 2, 3])
    b = rng.choice([1, 2])
    f = (x - a) * sp.exp(-x / b)
    d = sp.factor(sp.diff(f, x))
    xs_ = sp.solve(sp.diff(f, x), x)[0]
    xi = sp.solve(sp.diff(f, x, 2), x)[0]
    parts = [('Find the x-intercept and the y-intercept.', f'({a}, 0), (0, {P(f.subs(x, 0))})', 'A1 A1', 2, True),
             (f'Show that f′(x) = {P(d)}.', 'shown', 'product rule (M1) A1 AG', 2, True),
             ('Find the coordinates of the maximum point.', f'({P(xs_)}, {P(sp.simplify(f.subs(x, xs_)))}) ≈ ({s3(xs_)}, {s3(float(f.subs(x, xs_)))})', 'M1 A1', 2, True),
             ('Find the coordinates of the point of inflection.', f'({P(xi)}, {s3(float(f.subs(x, xi)))})', 'f″ = 0 (M1) A1', 2, False),
             ('Describe the behaviour of f as x → ∞ and as x → −∞.', 'f → 0 as x → ∞; f → −∞ as x → −∞', 'A1 A1', 2, False)]
    return build_parts(rng, [f'Let f(x) = {P(f)}.', f'The function f is given by f(x) = {P(f)}, x ∈ ℝ.'], parts, 3)


@R.add('ch07-st4', 'C1', (1, 3), 'mcq')
def asym_mcq(rng, slot):
    a, c, d = nz(rng, -6, 6), nz(rng, -4, 4), nz(rng, -6, 6)
    b = rng.randint(-5, 5)
    if a * d == b * c:
        return None
    return mcq(rng, f'The vertical asymptote of y = ({P(a * x + b)})/({P(c * x + d)}) is', f'x = {P(sp.Rational(-d, c))}',
               [f'x = {P(sp.Rational(d, c))}', f'y = {P(sp.Rational(a, c))}', f'x = {P(sp.Rational(-b, a))}'], f'Denominator zero at x = {P(sp.Rational(-d, c))}.')


# =============================================================================================
# ch08 Integration
# =============================================================================================
def integ_txt(F_):
    """antiderivative text with + C, writing ln|…| for logarithms."""
    s_ = P(sp.expand(F_)) if not (F_.has(sp.log) or F_.has(sp.exp)) else P(F_)
    s_ = re.sub(r'ln\(([^()]*)\)', r'ln|\1|', s_)
    return s_ + ' + C'


R.facts('ch08-st1', F(
    terms=[('anti-derivative', 'a function F with F′(x) = f(x); also called an indefinite integral, written ∫f(x) dx = F(x) + C'),
           ('constant of integration', 'the arbitrary constant C added to an indefinite integral, because constants differentiate to zero'),
           ('boundary condition', 'a given value such as f(a) = b that fixes the constant of integration')],
    facts=[('∫ x⁴ dx =', 'x⁵/5 + C', ['4x³ + C', 'x⁵ + C', '5x⁵ + C'], 'Increase the power by 1 and divide by the new power.'),
           ('If f′(x) = 6x and f(0) = 2, then f(x) =', '3x² + 2', ['3x²', '6x² + 2', '3x² − 2'], 'Integrate: 3x² + C; f(0) = 2 gives C = 2.'),
           ('The curves y = F(x) + C for different values of C are related by', 'vertical translations', ['horizontal translations', 'reflections', 'stretches'], 'Adding a constant shifts the graph vertically.')],
    why=[('Explain why an indefinite integral includes a constant of integration.', 'Differentiation removes constants, so many functions (differing by a constant) have the same derivative; all of them are anti-derivatives.'),
         ('Explain why ∫xⁿ dx = xⁿ⁺¹/(n + 1) + C fails when n = −1.', 'It would require dividing by n + 1 = 0; instead ∫x⁻¹ dx = ln|x| + C.'),
         ('Explain how one point on a curve determines its equation from its gradient function.', 'Integrating the gradient function gives a family y = F(x) + C; substituting the coordinates of the point gives one equation for C.')],
    misc=[('∫ 3x² dx = x³.', 'An indefinite integral needs + C: x³ + C.'),
          ('∫ (1/x²) dx = ln(x²) + C.', '1/x² = x⁻²; ∫x⁻² dx = −x⁻¹ + C = −1/x + C. ln only arises for x⁻¹.')],
))


@R.add('ch08-st1', 'C1', (1, 3), 'mcq')
def antider_mcq(rng, slot):
    a, n = nz(rng, -8, 9), rng.choice([2, 3, 4, 5, -2, -3, sp.Rational(1, 2), sp.Rational(3, 2), -sp.Rational(1, 2)])
    f = a * x ** n
    F_ = sp.integrate(f, x)
    wr = [P(sp.diff(f, x)) + ' + C', P(a * x ** (n + 1)) + ' + C', P(a * x ** (n + 1) * (n + 1)) + ' + C', P(F_ * 2) + ' + C']
    return mcq(rng, f'Find ∫ {term_txt(a, n)} dx.', P(F_) + ' + C', wr, f'Power rule for integration: {P(F_)} + C.')


@R.add('ch08-st1', 'C3', (1, 4), 'short', style='p1')
def antider_boundary(rng, slot):
    terms = rand_terms(rng, 2 if slot.d <= 2 else 3, allow_frac=slot.d >= 3)
    if any(sp.nsimplify(n) == -1 for _, n in terms):
        return None
    fp = sum_expr(terms)
    F_ = sp.integrate(fp, x)
    x0 = rng.choice([1, 4]) if any(not sp.nsimplify(n).is_Integer for _, n in terms) else rng.choice([0, 1, 2, -1]) if all(sp.nsimplify(n) > 0 for _, n in terms) else rng.choice([1, 2])
    y0 = rng.randint(-10, 12)
    C = y0 - F_.subs(x, x0)
    frame = rng.choice([f"Given that f′(x) = {sum_txt(terms)} and f({x0}) = {y0}, find f(x).",
                        f"A curve has gradient function dy/dx = {sum_txt(terms)} and passes through the point ({x0}, {y0}). Find the equation of the curve."])
    return mk(frame, ('f(x) = ' if frame.startswith('Given') else 'y = ') + P(F_ + C),
              f'Integrate term by term: {P(F_)} + C (M1 A1); substitute ({x0}, {y0}) (M1); C = {P(C)} (A1).', 4)


@R.add('ch08-st1', 'C3', (3, 5), 'short', style='p1')
def antider_second(rng, slot):
    a, b = nz(rng, -6, 6), rng.randint(-6, 6)
    f2 = a * x + b
    v0, f0 = rng.randint(-5, 5), rng.randint(-5, 5)
    fp = sp.integrate(f2, x) + v0
    f = sp.integrate(fp, x) + f0
    return mk(f"A function satisfies f″(x) = {P(f2)}, f′(0) = {v0} and f(0) = {f0}. Find f(x).", f'f(x) = {P(f)}',
              f"f′(x) = {P(sp.integrate(f2, x))} + C₁ (M1), C₁ = {v0} (A1); f(x) = {P(sp.integrate(sp.integrate(f2, x), x))} + {v0}x + C₂ (M1); C₂ = {f0} (A1).", 4)


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def antider_explain(rng, slot):
    a, n = rng.randint(2, 9), rng.randint(2, 5)
    c1, c2 = rng.sample(range(-9, 10), 2)
    return mk(f'Explain why both y = {P(a * x ** n + c1)} and y = {P(a * x ** n + c2)} are anti-derivatives of {P(a * n * x ** (n - 1))}, and describe how their graphs are related.', 'Both differentiate to the same function; vertical translation.',
              f'd/dx of each = {P(a * n * x ** (n - 1))} since constants differentiate to 0 (R1 A1); the graphs differ by a vertical translation of {abs(c1 - c2)} units (R1).', 3, 'explain')


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step', style='ext')
def antider_parts(rng, slot):
    p, q = sorted(rng.sample(range(-3, 4), 2))
    kk = rng.choice([3, -3, 6]) if (p + q) % 2 == 0 else rng.choice([6, -6])
    fp = sp.expand(kk * (x - p) * (x - q))
    x0 = rng.choice([0, 1, -1])
    y0 = rng.randint(-6, 6)
    F_ = sp.integrate(fp, x)
    f = F_ + y0 - F_.subs(x, x0)
    parts = [('Find the equation of the curve.', f'y = {P(f)}', 'integrate (M1) A1; constant from the point (M1) A1', 4, True),
             ('Find the coordinates of the stationary points of the curve.', f'({p}, {P(f.subs(x, p))}), ({q}, {P(f.subs(x, q))})', 'dy/dx = 0 (M1) A1 A1', 3, True),
             ('Determine the nature of each stationary point.', f"({p}): {'max' if kk > 0 else 'min'}; ({q}): {'min' if kk > 0 else 'max'}", 'second derivative or sign test (M1) A1', 2, False),
             (f'Find the equation of the tangent at x = {q + 1}.', line_eq(fp.subs(x, q + 1), f.subs(x, q + 1) - fp.subs(x, q + 1) * (q + 1)), 'gradient (A1); line (A1)', 2, False)]
    return build_parts(rng, [f'A curve has gradient function dy/dx = {P(fp)} and passes through the point {pt([x0, y0])}.', f'The gradient of a curve at any point is given by {P(fp)}; the curve contains {pt([x0, y0])}.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch08-st2', F(
    terms=[('integration by inspection', 'recognising an integrand as the result of the chain rule, e.g. ∫ f′(x)eᶠ⁽ˣ⁾ dx = eᶠ⁽ˣ⁾ + C, and adjusting constants'),
           ('integral of 1/x', 'ln|x| + C, valid for x ≠ 0'),
           ('linear composite rule', '∫ f(ax + b) dx = (1/a)F(ax + b) + C where F′ = f')],
    facts=[('∫ e^(5x) dx =', 'e^(5x)/5 + C', ['5e^(5x) + C', 'e^(5x) + C', 'e^(6x)/6 + C'], 'Divide by the coefficient of x.'),
           ('∫ cos(3x) dx =', 'sin(3x)/3 + C', ['3sin(3x) + C', '−sin(3x)/3 + C', 'sin(3x) + C'], 'Reverse the chain rule.'),
           ('∫ 1/(2x + 1) dx =', '½ ln|2x + 1| + C', ['ln|2x + 1| + C', '2 ln|2x + 1| + C', '−1/(2x + 1)² + C'], 'Linear composite of 1/x.'),
           ('∫ 2x/(x² + 4) dx =', 'ln(x² + 4) + C', ['2 ln(x² + 4) + C', 'ln|2x| + C', 'x²/(x² + 4) + C'], 'Numerator is the derivative of the denominator.')],
    why=[('Explain why ∫ sin(4x) dx = −¼cos(4x) + C.', 'd/dx(−cos 4x) = 4 sin 4x by the chain rule, so dividing by 4 gives the anti-derivative −¼cos 4x.'),
         ('Explain why ∫ x e^(x²) dx can be found by inspection but ∫ e^(x²) dx cannot.', 'd/dx e^(x²) = 2x e^(x²), so x e^(x²) is half a chain-rule derivative; without the factor x there is no elementary anti-derivative.'),
         ('Explain why the modulus is needed in ∫ 1/x dx = ln|x| + C.', 'ln x is only defined for x > 0; for x < 0, d/dx ln(−x) = 1/x as well, so ln|x| covers both cases.')],
    misc=[('∫ e^(3x) dx = 3e^(3x) + C.', 'Differentiating 3e^(3x) gives 9e^(3x); the correct result divides by 3: e^(3x)/3 + C.'),
          ('∫ cos x dx = −sin x + C.', 'd/dx sin x = cos x, so ∫ cos x dx = sin x + C.'),
          ('∫ (x² + 1)³ dx = (x² + 1)⁴/4 + C.', 'Differentiating gives 2x(x² + 1)³, not (x² + 1)³; expand first instead.')],
))


def _lin_txt(a, b):
    return P(a * x + b)


def _indef(rng, d):
    kind = rng.choice(['pow', 'sin', 'cos', 'exp', 'recip'] + (['insp_pow', 'insp_exp', 'insp_log', 'insp_trig'] if d >= 3 else []))
    a, b = rng.choice([2, 3, 4, 5, -2, sp.Rational(1, 2)]), rng.randint(-5, 5)
    u = a * x + b
    if kind == 'pow':
        n = rng.choice([3, 4, 5, -2, -3, sp.Rational(1, 2)])
        f = u ** n
        F_ = u ** (n + 1) / (a * (n + 1))
    elif kind == 'sin':
        f, F_ = sp.sin(u), -sp.cos(u) / a
    elif kind == 'cos':
        f, F_ = sp.cos(u), sp.sin(u) / a
    elif kind == 'exp':
        f, F_ = sp.exp(u), sp.exp(u) / a
    elif kind == 'recip':
        k = rng.randint(1, 6)
        f, F_ = k / u, k * sp.log(u) / a
    elif kind == 'insp_pow':
        c, n = rng.randint(1, 9), rng.choice([3, 4, 5])
        k = rng.randint(1, 4)
        f = k * x * (x ** 2 + c) ** n
        F_ = sp.Rational(k, 2 * (n + 1)) * (x ** 2 + c) ** (n + 1)
    elif kind == 'insp_exp':
        k = rng.randint(1, 6)
        f = k * x * sp.exp(x ** 2)
        F_ = sp.Rational(k, 2) * sp.exp(x ** 2)
    elif kind == 'insp_log':
        c, k = rng.randint(1, 9), rng.randint(1, 5)
        f = k * x / (x ** 2 + c)
        F_ = sp.Rational(k, 2) * sp.log(x ** 2 + c)
    else:
        n = rng.choice([2, 3, 4])
        f = sp.sin(x) * sp.cos(x) ** n
        F_ = -sp.cos(x) ** (n + 1) / (n + 1)
    assert sp.simplify(sp.diff(F_, x) - f) == 0
    return kind, f, F_


@R.add('ch08-st2', 'C3', (1, 4), 'short')
def indef_integral(rng, slot):
    kind, f, F_ = _indef(rng, slot.d)
    return mk(f'Find ∫ {P(f)} dx.', integ_txt(F_),
              f'{"Recognise the reverse chain rule (by inspection)" if kind.startswith("insp") else "Standard integral of a linear composite"} (M1); correct form (A1); correct constant factor (A1); + C (A1 for the complete answer).', 3 if not kind.startswith('insp') else 4)


@R.add('ch08-st2', 'C1', (1, 3), 'mcq')
def indef_mcq(rng, slot):
    kind, f, F_ = _indef(rng, 2)
    wrong = [integ_txt(sp.diff(f, x)), integ_txt(F_ * 2), integ_txt(-F_), integ_txt(F_ * 4)]
    return mcq(rng, f'Which of the following is ∫ {P(f)} dx?', integ_txt(F_), wrong, f'Check by differentiating {P(F_)}: you recover {P(f)}.')


@R.add('ch08-st2', 'C3', (2, 4), 'short')
def indef_sum(rng, slot):
    a, b = nz(rng, -5, 6), rng.choice([2, 3, 4])
    c = rng.randint(1, 5)
    k = rng.choice([1, 2, 3])
    f = a * sp.exp(b * x) + c * sp.cos(k * x) + rng.choice([2, 3, 5]) / x
    F_ = sp.integrate(f, x)
    return mk(f'Find ∫ ({P(f)}) dx.', integ_txt(F_), 'Each term integrated correctly (A1 A1 A1); + C (A1).', 4)


@R.add('ch08-st2', 'C2', (2, 4), 'explain')
def indef_error(rng, slot):
    kind, f, F_ = _indef(rng, rng.choice([2, 3]))
    nm = who(rng)
    wrongF = F_ * rng.choice([2, -1, 4]) if kind not in ('recip',) else F_ * 2
    return mk(f'{nm} claims that ∫ {P(f)} dx = {integ_txt(wrongF)}. Explain how differentiation can be used to check this, and correct the answer.', integ_txt(F_),
              f'Differentiate the claimed answer: {P(sp.simplify(sp.diff(wrongF, x)))} ≠ {P(f)} (M1 R1); the constant factor is wrong (R1); correct: {integ_txt(F_)} (A1).', 4, 'explain', 'G2')


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step', style='p1')
def inspect_parts(rng, slot):
    kind = rng.choice(['ln', 'exp', 'pow', 'trig'])
    k = rng.randint(2, 5)
    if kind == 'ln':
        g = x ** 2 + k
        F_ = sp.log(g)
        f = sp.diff(F_, x)
        target = 3 * x / g
        Ft = sp.Rational(3, 2) * sp.log(g)
    elif kind == 'exp':
        g = sp.exp(x ** 3)
        F_ = g
        f = sp.diff(F_, x)
        target = x ** 2 * sp.exp(x ** 3)
        Ft = sp.exp(x ** 3) / 3
    elif kind == 'pow':
        g = (x ** 2 + k) ** 5
        F_ = g
        f = sp.factor(sp.diff(F_, x))
        target = x * (x ** 2 + k) ** 4
        Ft = (x ** 2 + k) ** 5 / 10
    else:
        F_ = sp.sin(x) ** 4
        f = sp.diff(F_, x)
        target = sp.sin(x) ** 3 * sp.cos(x)
        Ft = sp.sin(x) ** 4 / 4
    a, b = (0, 1) if kind != 'trig' else (0, pi / 2)
    val = sp.simplify(Ft.subs(x, b) - Ft.subs(x, a))
    parts = [(f'Find d/dx({P(F_)}).', P(f), 'chain rule (M1) A1', 2, True),
             (f'Hence find ∫ {P(target)} dx.', integ_txt(Ft), 'recognise multiple of (a) (M1) A1', 2, True),
             (f'Hence find the exact value of ∫ from {P(a)} to {P(b)} of {P(target)} dx.', P(val), 'substitute limits (M1) A1', 2, False)]
    return build_parts(rng, ['This question is about integration by inspection.', f'Let g(x) = {P(F_)}.'], parts, 2)


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step', style='ext')
def boundary_trig_exp(rng, slot):
    a = rng.choice([2, 3, 4])
    c1 = rng.randint(1, 5)
    fp = c1 * sp.cos(a * x) + sp.exp(-x)
    F_ = sp.integrate(fp, x)
    y0 = rng.randint(-3, 5)
    f = F_ + y0 - F_.subs(x, 0)
    xv = pi / (2 * a)
    parts = [('Find f(x).', f'f(x) = {P(f)}', 'integrate each term (A1 A1); constant (M1 A1)', 4, True),
             (f'Find the exact value of f({P(xv)}).', P(sp.simplify(f.subs(x, xv))), 'substitute (A1)', 1, True),
             ('Write down the behaviour of f′(x) as x → ∞.', f'oscillates between −{c1} and {c1}', 'e^(−x) → 0 (R1)', 1, False)]
    return build_parts(rng, [f'A function f satisfies f′(x) = {P(fp)} and f(0) = {y0}.', f'The derivative of f is {P(fp)}, and the graph of f passes through (0, {y0}).'], parts, 2)


# ---------------------------------------------------------------------------------------------
R.facts('ch08-st3', F(
    terms=[('definite integral', '∫ from a to b of f(x) dx = F(b) − F(a), where F is any anti-derivative of f'),
           ('area under a curve', 'for f(x) ≥ 0 on [a, b], the area between the curve and the x-axis is ∫ from a to b of f(x) dx'),
           ('area between two curves', '∫ from a to b of (upper − lower) dx between consecutive intersection points')],
    facts=[('∫ from 0 to 2 of 3x² dx =', '8', ['12', '6', '24'], '[x³] from 0 to 2 = 8.'),
           ('If f(x) < 0 on [a, b], then ∫ from a to b of f(x) dx is', 'negative', ['positive', 'zero', 'the area'], 'The integral is signed; the area is its modulus.'),
           ('∫ from a to a of f(x) dx =', '0', ['f(a)', '1', 'undefined'], 'F(a) − F(a) = 0.'),
           ('∫ from b to a of f(x) dx equals', '−∫ from a to b of f(x) dx', ['∫ from a to b of f(x) dx', '0', '2∫ from a to b of f(x) dx'], 'Swapping limits changes the sign.')],
    why=[('Explain why the constant of integration can be ignored when evaluating a definite integral.', 'F(b) + C − (F(a) + C) = F(b) − F(a): the constants cancel.'),
         ('Explain why ∫ from 0 to 2π of sin x dx = 0 although the curve encloses a non-zero area with the x-axis.', 'The parts above and below the axis have equal area; the integral adds them with opposite signs so they cancel, while the total area is 4.'),
         ('Explain how to find the area enclosed between a curve and the x-axis when the curve crosses the axis.', 'Find the roots, integrate separately on each sub-interval and add the absolute values (or integrate |f(x)| with technology).')],
    misc=[('The area between y = x³ and the x-axis from −1 to 1 is ∫ from −1 to 1 of x³ dx = 0.', 'The region below the axis gives a negative integral; the area is 2∫ from 0 to 1 of x³ dx = 1/2.'),
          ('∫ from 1 to 3 of f(x)g(x) dx = (∫ f dx)(∫ g dx).', 'Integrals do not split over products; only over sums and constant multiples.')],
))


@R.add('ch08-st3', 'C3', (1, 4), 'short', style='p1')
def definite_exact(rng, slot):
    kind = rng.choice(['poly', 'trig', 'exp', 'recip', 'root'])
    if kind == 'poly':
        f = _poly_rand(rng, 2)
        a, b = sorted(rng.sample(range(-2, 4), 2))
    elif kind == 'trig':
        k = rng.choice([1, 2, 3])
        f = rng.choice([sp.sin(k * x), sp.cos(k * x)])
        a, b = 0, rng.choice([pi / 6, pi / 4, pi / 3, pi / 2]) / k
    elif kind == 'exp':
        k = rng.choice([1, 2, 3, -1])
        f = sp.exp(k * x)
        a, b = 0, rng.choice([1, sp.log(2), sp.log(3), 2])
    elif kind == 'recip':
        k = rng.randint(1, 6)
        f = k / x
        a, b = 1, rng.choice([sp.E, sp.E ** 2, 2, 3, 4])
    else:
        f = rng.randint(1, 6) * sp.sqrt(x)
        a, b = rng.choice([(0, 4), (1, 9), (0, 1), (4, 9)])
    val = sp.simplify(sp.integrate(f, (x, a, b)))
    ftxt = f'({P(f)})' if isinstance(f, sp.Add) else P(f)
    return mk(f'Find the exact value of ∫ from {P(a)} to {P(b)} of {ftxt} dx.', P(sp.nsimplify(val) if val.is_Rational else val),
              f'Anti-derivative {P(sp.integrate(f, x))} (A1 A1); substitute limits (M1); {P(val)} (A1).', 4)


@R.add('ch08-st3', 'C3', (2, 5), 'short', style='p1')
def area_between_exact(rng, slot):
    kind = rng.choice(['line_parab', 'two_parab', 'cubic_line'])
    if kind == 'line_parab':
        k = rng.randint(1, 6)
        g, h = x ** 2, k * x
    elif kind == 'two_parab':
        k = rng.choice([1, 2, 4, 8, 9])
        g, h = x ** 2 - k, k - x ** 2
    else:
        k = rng.choice([1, 4, 9])
        g, h = x ** 3, k * x
    roots = sorted(set(sp.solve(g - h, x)), key=float)
    area = sum(abs(sp.integrate(h - g, (x, roots[i], roots[i + 1]))) for i in range(len(roots) - 1))
    return mk(f'Find the exact area of the region enclosed by the curves y = {P(g)} and y = {P(h)}.', P(sp.simplify(area)),
              f'Intersections x = {lst(roots)} (M1 A1); area = ∫ |upper − lower| dx over each interval (M1); {P(sp.simplify(area))} (A1).', 5)


@R.add('ch08-st3', 'C3', (2, 5), 'short', style='p2')
def area_gdc(rng, slot):
    kind = rng.choice(['cross', 'between'])
    if kind == 'cross':
        p, q = sorted(rng.sample(range(0, 5), 2))
        a_ = round(rng.uniform(0.5, 2), 1)
        f = a_ * (x - p) * (x - q) * sp.Rational(1, 1)
        lo, hi = p - 1, q + 1
        g = sp.lambdify(x, f, 'math')
        import math as _m
        # numeric area of |f|
        N = 4000
        hstep = (hi - lo) / N
        area = sum(abs(g(lo + (i + 0.5) * hstep)) for i in range(N)) * hstep
        integ = float(sp.integrate(f, (x, lo, hi)))
        return mk(f'Let f(x) = {a_}(x − {p})(x − {q}). Find (a) ∫ from {lo} to {hi} of f(x) dx (b) the total area between the graph of f and the x-axis for {lo} ≤ x ≤ {hi}.'.replace('x − 0', 'x'),
                  f'(a) {s3(integ)} (b) {s3(area)}', f'(a) GDC (A1). (b) the graph crosses the axis at {p} and {q} (R1); area = ∫|f(x)|dx (M1) = {s3(area)} (A1).', 4)
    c = rng.randint(1, 4)
    f1, f2 = sp.exp(x / 2), x + c
    g = sp.lambdify(x, f1 - f2, 'math')
    r_ = nsols(g, -6, 8)
    if len(r_) != 2:
        return None
    N = 4000
    hstep = (r_[1] - r_[0]) / N
    area = sum(abs(g(r_[0] + (i + 0.5) * hstep)) for i in range(N)) * hstep
    return mk(f'The curves y = e^(x/2) and y = x + {c} intersect at two points. Find the x-coordinates of the intersection points and the area of the region enclosed between the curves.',
              f'x = {lst3(r_)}; area {s3(area)}', f'GDC intersections (A1 A1); area = ∫(x + {c} − e^(x/2))dx between them (M1); {s3(area)} (A1).', 4)


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def area_sign_explain(rng, slot):
    p = rng.randint(1, 4)
    f = x * (x - p)
    I = sp.integrate(f, (x, 0, p))
    nm = who(rng)
    return mk(f'{nm} calculates ∫ from 0 to {p} of ({P(sp.expand(f))}) dx = {P(I)} and says the area is {P(I)}. Explain the issue and state the area.', P(-I),
              f'On 0 < x < {p}, {P(sp.expand(f))} < 0 so the region is below the x-axis (R1); the integral is negative (R1); area = |{P(I)}| = {P(-I)} (A1).', 3, 'explain', 'G2')


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step', style='ext')
def area_parts(rng, slot):
    k = rng.choice([1, 2, 3, 4])
    m = rng.choice([1, 2, 3])
    f = k * x - x ** 2 + m * x
    s_ = k + m
    g = m * x
    A_total = sp.integrate(f, (x, 0, s_))
    A_between = sp.integrate(f - g, (x, 0, k))
    parts = [(f'Find the x-intercepts of y = {P(f)}.', f'x = 0, x = {s_}', 'factorise (M1) A1', 2, True),
             ('Find the exact area of the region R₁ enclosed by the curve and the x-axis.', P(A_total), 'integral set up (M1) A1 A1', 3, True),
             (f'The line y = {P(g)} meets the curve at the origin and at P. Find the coordinates of P.', pt([k, g.subs(x, k)]), 'equate (M1) A1', 2, True),
             (f'Find the exact area of the region R₂ enclosed between the curve and the line y = {P(g)}.', P(A_between), '∫(curve − line) (M1) A1 A1', 3, True),
             ('Find the ratio of the areas R₂ : R₁.', f'{P(A_between / A_total)}', 'A1', 1, False)]
    return build_parts(rng, [f'Consider the curve y = {P(f)}.', f'The graph of f(x) = {P(f)} is shown for x ≥ 0 (no diagram provided).'], parts, 3)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step', style='p2')
def area_trig_parts(rng, slot):
    a = rng.choice([1, 2, 3])
    c = rng.choice([0.5, 1, 1.5])
    f = a * sp.sin(x) + c
    g = sp.lambdify(x, f, 'math')
    r_ = nsols(g, 0, 2 * math.pi)
    N = 4000
    hstep = 2 * math.pi / N
    absA = sum(abs(g((i + 0.5) * hstep)) for i in range(N)) * hstep
    I = float(sp.integrate(f, (x, 0, 2 * pi)))
    parts = [('Find the x-intercepts of the graph for 0 ≤ x ≤ 2π.', lst3(r_) if r_ else 'none', 'GDC (A1 A1)', 2, True),
             ('Find ∫ from 0 to 2π of f(x) dx exactly.', P(sp.integrate(f, (x, 0, 2 * pi))), 'A1', 1, True),
             ('Find the total area enclosed between the graph and the x-axis for 0 ≤ x ≤ 2π.', s3(absA), '∫|f| (M1) A1', 2, True),
             ('Explain why your answers to the two previous parts differ.', 'part of the graph lies below the x-axis' if r_ else 'they are equal since f > 0', 'R1', 1, False)]
    return build_parts(rng, [f'Let f(x) = {a} sin x + {c}, for 0 ≤ x ≤ 2π.'.replace('1 sin', 'sin'), f'The function f(x) = {a} sin x + {c} is defined on [0, 2π].'.replace('1 sin', 'sin')], parts, 3)


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def odd_integral_explain(rng, slot):
    a = rng.choice([1, 2, 3, pi / 2, pi])
    f = rng.choice([x ** 3, x ** 5 - x, sp.sin(x), x * sp.cos(x), x ** 3 * sp.cos(x), sp.sin(x) ** 3])
    return mk(f'Explain, without integrating, why ∫ from −{P(a)} to {P(a)} of {P(f)} dx = 0, and explain why this is not the area enclosed by the curve and the x-axis.', '0; the area is 2∫ from 0 to a of |f| dx',
              f'f(−x) = −f(x), so f is odd (M1 R1); the contributions on [−{P(a)}, 0] and [0, {P(a)}] are equal and opposite (R1); area counts both parts as positive (R1).', 4, 'explain')


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def integral_properties(rng, slot):
    a, b, c = sorted(rng.sample(range(-3, 8), 3))
    I1, I2 = nz(rng, -9, 12), nz(rng, -9, 12)
    k = rng.randint(2, 5)
    kind = rng.choice([1, 2, 3])
    if kind == 1:
        return mk(f'Given ∫ from {a} to {b} of f(x) dx = {I1} and ∫ from {b} to {c} of f(x) dx = {I2}, find ∫ from {a} to {c} of f(x) dx and ∫ from {c} to {a} of f(x) dx, explaining the properties used.',
                  f'{I1 + I2}; {-(I1 + I2)}', f'Additivity over adjacent intervals (R1): {I1 + I2} (A1); reversing the limits changes the sign (R1): {-(I1 + I2)} (A1).', 4, 'explain')
    if kind == 2:
        return mk(f'Given ∫ from {a} to {b} of f(x) dx = {I1}, explain how to find ∫ from {a} to {b} of ({k}f(x) + {I2}) dx and find its value.',
                  f'{k * I1 + I2 * (b - a)}', f'Linearity: {k}∫f dx + ∫{I2} dx (R1); ∫ from {a} to {b} of {I2} dx = {I2}({b} − ({a})) (A1); total {k * I1 + I2 * (b - a)} (A1).', 3, 'explain')
    return mk(f'Explain why ∫ from {a} to {b} of f(x) dx = {I1} does not mean that ∫ from {a} to {b} of (f(x))² dx = {I1 * I1}.', 'integrals do not commute with squaring',
              f'The integral of a square is not the square of the integral (R1); e.g. f = 1 on [0, 2]: ∫f = 2 but ∫f² = 2 ≠ 4 (A1 R1).', 3, 'explain')


@R.add('ch08-st3', 'C1', (1, 3), 'mcq')
def definite_mcq(rng, slot):
    a, b = sorted(rng.sample(range(0, 5), 2))
    k = rng.randint(1, 5)
    f = k * x
    val = sp.integrate(f, (x, a, b))
    return mcq(rng, f'Evaluate ∫ from {a} to {b} of {P(f)} dx.', P(val), [P(k * (b - a)), P(k * b ** 2 / 2), P(val + k)], f'[{P(sp.integrate(f, x))}] from {a} to {b} = {P(val)}.')


# =============================================================================================
# ch09 Kinematics
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('displacement', 's(t), the position of a particle relative to a fixed origin; it can be negative'),
           ('velocity', 'v(t) = ds/dt, the rate of change of displacement'),
           ('acceleration', 'a(t) = dv/dt = d²s/dt², the rate of change of velocity'),
           ('at rest', 'a particle is instantaneously at rest when v(t) = 0')],
    facts=[('If s is measured in metres and t in seconds, acceleration is measured in', 'm s⁻²', ['m s⁻¹', 'm', 's m⁻²'], 'Rate of change of m s⁻¹ per second.'),
           ('A particle is speeding up when', 'v and a have the same sign', ['a > 0', 'v > 0', 'a = 0'], 'Speed increases when velocity and acceleration act in the same direction.'),
           ('Given v(t), displacement from t = 0 to t = T is', '∫ from 0 to T of v(t) dt', ['v(T) − v(0)', '∫ from 0 to T of |a(t)| dt', 'v(T)·T'], 'Displacement is the integral of velocity.')],
    why=[('Explain why a particle can have zero velocity but non-zero acceleration.', 'At a turning point the velocity is momentarily 0 while it is still changing, e.g. a ball at the top of its flight has v = 0 but a = −9.8 m s⁻².'),
         ('Explain why the particle is slowing down when v > 0 and a < 0.', 'The acceleration acts opposite to the motion, so the speed |v| decreases.'),
         ('Explain how to find the displacement function s(t) from the acceleration a(t).', 'Integrate a to get v plus a constant fixed by an initial velocity, then integrate v to get s plus a constant fixed by an initial position.')],
    misc=[('If a(t) < 0 the particle is moving backwards.', 'Negative acceleration means v is decreasing; the particle moves backwards only if v < 0.'),
          ('v(t) = 0 means the particle is at the origin.', 'v = 0 means instantaneously at rest; the position s can be anything.')],
))


@R.add('ch09-st1', 'C3', (1, 4), 'short', style='p1')
def kin_diff(rng, slot):
    p, q = sorted(rng.sample(range(1, 7), 2))
    kk = rng.choice([1, 2, 3]) if (p + q) % 2 == 0 else 2
    # v = 3k(t-p)(t-q) -> s = k(t^3 - 3(p+q)/2 t^2 + 3pq t) + c
    c = rng.randint(-5, 5)
    s_ = sp.expand(kk * (t ** 3 - sp.Rational(3 * (p + q), 2) * t ** 2 + 3 * p * q * t) + c)
    v, a = sp.diff(s_, t), sp.diff(s_, t, 2)
    t1 = rng.randint(0, 6)
    want = rng.choice(['rest', 'acc', 'vel'])
    if want == 'rest':
        q_, ans = 'Find the times at which the particle is instantaneously at rest.', f't = {p} and t = {q}'
        key = f'v = ds/dt = {P(v)} (A1); v = 0 (M1); t = {p}, {q} (A1 A1).'
    elif want == 'acc':
        q_, ans = f'Find the acceleration of the particle when t = {t1}.', f'{P(a.subs(t, t1))} m s⁻²'
        key = f'v = {P(v)} (A1); a = dv/dt = {P(a)} (M1 A1); a({t1}) = {P(a.subs(t, t1))} (A1).'
    else:
        q_, ans = f'Find the velocity of the particle when t = {t1}, and state its direction of motion.', f'{P(v.subs(t, t1))} m s⁻¹, ' + ('moving in the positive direction' if v.subs(t, t1) > 0 else 'moving in the negative direction' if v.subs(t, t1) < 0 else 'at rest')
        key = f'v = ds/dt = {P(v)} (M1 A1); v({t1}) = {P(v.subs(t, t1))} (A1); direction from the sign (R1).'
    return mk(f'A particle moves in a straight line so that its displacement from O after t seconds is s = {P(s_)} metres, t ≥ 0. {q_}', ans, key, 4)


@R.add('ch09-st1', 'C3', (2, 5), 'short', style='p1')
def kin_integrate(rng, slot):
    a_ = nz(rng, -4, 6) * t + rng.randint(-6, 6)
    v0, s0 = rng.randint(-5, 8), rng.randint(-5, 5)
    v = sp.integrate(a_, t) + v0
    s_ = sp.integrate(v, t) + s0
    T = rng.randint(1, 5)
    return mk(f'The acceleration of a particle is a(t) = {P(a_)} m s⁻². When t = 0 its velocity is {v0} m s⁻¹ and its displacement from O is {s0} m. Find its displacement when t = {T}.',
              f'{P(s_.subs(t, T))} m', f'v = {P(sp.integrate(a_, t))} + c (M1), c = {v0} (A1); s = {P(sp.integrate(v - v0, t))} + {v0}t + d (M1), d = {s0} (A1); s({T}) = {P(s_.subs(t, T))} (A1).', 5)


@R.add('ch09-st1', 'C2', (2, 4), 'explain')
def kin_speed_explain(rng, slot):
    s_ = _poly_rand(rng, 3).subs(x, t)
    T = rng.randint(1, 5)
    v, a = sp.diff(s_, t).subs(t, T), sp.diff(s_, t, 2).subs(t, T)
    if v == 0 or a == 0:
        return None
    sp_up = (v > 0) == (a > 0)
    return mk(f'A particle has displacement s = {P(s_)} m at time t s. Determine whether the particle is speeding up or slowing down at t = {T}, explaining your reasoning.', 'speeding up' if sp_up else 'slowing down',
              f'v({T}) = {P(v)} (A1); a({T}) = {P(a)} (A1); {"same sign" if sp_up else "opposite signs"} so the speed is {"increasing" if sp_up else "decreasing"} (R1).', 3, 'explain')


@R.add('ch09-st1', 'C1', (1, 3), 'mcq')
def kin_mcq(rng, slot):
    k, n = rng.randint(2, 6), rng.randint(2, 4)
    s_ = k * t ** n
    return mcq(rng, f'A particle has displacement s(t) = {P(s_)}. Its acceleration at time t is', P(sp.diff(s_, t, 2)), [P(sp.diff(s_, t)), P(sp.integrate(s_, t)), P(sp.diff(s_, t, 2) * t)], 'a = d²s/dt².')


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step', style='ext')
def kin_parts(rng, slot):
    p = rng.randint(1, 5)
    q = p + rng.choice([2, 4, 6])
    s_ = sp.expand(t ** 3 - sp.Rational(3 * (p + q), 2) * t ** 2 + 3 * p * q * t)
    v, a = sp.diff(s_, t), sp.diff(s_, t, 2)
    tm = sp.Rational(p + q, 2)
    parts = [('Find expressions for the velocity and acceleration.', f'v = {P(v)}, a = {P(a)}', 'A1 A1', 2, True),
             ('Find the times when the particle is at rest.', f't = {p}, {q}', 'v = 0 (M1) A1', 2, True),
             ('Find the displacement of the particle at each of these times.', f's({p}) = {P(s_.subs(t, p))}, s({q}) = {P(s_.subs(t, q))}', 'A1 A1', 2, True),
             ('Find the minimum velocity of the particle and when it occurs.', f'{P(v.subs(t, tm))} m s⁻¹ at t = {P(tm)}', 'a = 0 (M1) A1 A1', 3, False),
             (f'Find the total distance travelled in the first {q} seconds.', P(abs(s_.subs(t, p)) + abs(s_.subs(t, q) - s_.subs(t, p))), 'split at the turning point (M1) A1', 2, False)]
    return build_parts(rng, [f'A particle P moves along a straight line so that its displacement from a fixed point O after t seconds is s = {P(s_)} m.', f'The position of a car on a test track is s(t) = {P(s_)} metres, t ≥ 0 seconds, measured from the start line.'], parts, 3)


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step', style='p1')
def kin_accel_parts(rng, slot):
    k = rng.randint(1, 4)
    v0 = rng.randint(2, 12)
    kind = rng.choice(['lin', 'root', 'exp'])
    if kind == 'lin':
        a_ = -2 * k * t
        v = v0 * k * k - k * t ** 2
        T0 = sp.sqrt(v0) * k ** 0
        v = sp.Integer(v0) - k * t ** 2
        T0 = sp.sqrt(sp.Rational(v0, k))
    elif kind == 'root':
        a_ = -sp.Rational(k, 2) / sp.sqrt(t + 1)
        v = v0 - k * (sp.sqrt(t + 1) - 1)
        T0 = (sp.Rational(v0, k) + 1) ** 2 - 1
    else:
        a_ = -k * sp.exp(t / 2) / 2
        v = v0 + k - k * sp.exp(t / 2)
        T0 = 2 * sp.log(sp.Rational(v0 + k, k))
    assert sp.simplify(sp.diff(v, t) - a_) == 0
    s_ = sp.integrate(v, (t, 0, t))
    parts = [(f'Show that v(t) = {P(v)}.', 'shown', 'integrate a (M1) A1; use v(0) (A1) AG', 3, True),
             ('Find the exact time at which the particle comes to instantaneous rest.', f't = {P(sp.simplify(T0))}', 'v = 0 (M1) A1', 2, True),
             ('Find the displacement from O at that time.', P(sp.simplify(s_.subs(t, T0))), '∫ v dt from 0 (M1) A1 A1', 3, False),
             ('Explain why the particle is slowing down for 0 < t < T, where T is the time found above.', 'v > 0 and a < 0', 'R1 R1', 2, False)]
    return build_parts(rng, [f'A particle starts from O with velocity {v0} m s⁻¹ and moves in a straight line with acceleration a(t) = {P(a_)} m s⁻² for t ≥ 0.',
                             f'A sledge leaves the point O at {v0} m s⁻¹; its acceleration t seconds later is a = {P(a_)} m s⁻².'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch09-st2', F(
    terms=[('distance travelled', 'the total length of path covered, ∫ from t₁ to t₂ of |v(t)| dt; never negative'),
           ('displacement over an interval', 'the change in position, ∫ from t₁ to t₂ of v(t) dt, which can be negative or zero'),
           ('speed', 'the magnitude of velocity, |v(t)|')],
    facts=[('A particle moves 5 m forwards and then 3 m backwards. Its displacement and distance travelled are', '2 m and 8 m', ['8 m and 2 m', '2 m and 2 m', '8 m and 8 m'], 'Displacement is net change; distance adds lengths.'),
           ('Distance travelled from t = 0 to t = 4 is given by', '∫ from 0 to 4 of |v(t)| dt', ['∫ from 0 to 4 of v(t) dt', '|∫ from 0 to 4 of v(t) dt|', 'v(4) − v(0)'], 'Integrate speed.'),
           ('If v(t) > 0 for the whole interval, distance travelled equals', 'displacement', ['zero', 'twice the displacement', 'the final velocity'], 'No change of direction.')],
    why=[('Explain why ∫ v dt and ∫ |v| dt give different results if the particle changes direction.', 'When v < 0 the integral of v subtracts that part of the motion, whereas |v| counts it as positive distance.'),
         ('Explain why you must find when v = 0 before calculating distance by hand.', 'The particle can change direction only where v = 0; the integral must be split there so each part can be made positive.'),
         ('Explain why a displacement of 0 does not mean the particle did not move.', 'It may have moved away and returned to its starting point; the net change is 0 but the distance travelled is positive.')],
    misc=[('Distance travelled = |∫ v dt|.', 'Taking the modulus of the total still cancels forward and backward motion; use ∫|v| dt.'),
          ('If the displacement over an interval is negative, the particle moved only backwards.', 'It may have moved forwards and then further backwards; only the net change is negative.')],
))


@R.add('ch09-st2', 'C3', (2, 5), 'short', style='p1')
def dist_exact(rng, slot):
    k = rng.randint(2, 6)
    T = rng.randint(k + 1, k + 4)
    kind = rng.choice(['quad', 'lin'])
    v = t * (t - k) if kind == 'quad' else rng.choice([2, 3]) * (t - k)
    disp = sp.integrate(v, (t, 0, T))
    dist = sp.integrate(-v if (v.subs(t, k / 2) < 0) else v, (t, 0, k)) + sp.integrate(v if v.subs(t, k + 0.5) > 0 else -v, (t, k, T))
    return mk(f'A particle moves with velocity v(t) = {P(sp.expand(v))} m s⁻¹, for 0 ≤ t ≤ {T}. Find (a) the displacement (b) the total distance travelled, over this interval.',
              f'(a) {P(disp)} m (b) {P(dist)} m', f'(a) ∫ from 0 to {T} of v dt (M1) = {P(disp)} (A1). (b) v = 0 at t = {k} (A1); split the integral and take moduli (M1); {P(dist)} m (A1).', 5)


@R.add('ch09-st2', 'C3', (2, 5), 'short', style='p2')
def dist_gdc(rng, slot):
    a, b = round(rng.uniform(1, 4), 1), round(rng.uniform(0.3, 1.2), 1)
    kind = rng.choice(['trig', 'poly_exp'])
    if kind == 'trig':
        v = a * sp.cos(b * t) + rng.choice([0, 0.5, -0.5])
    else:
        a = int(round(a)) or 1
        v = (t ** 2 - a * t) * sp.exp(-sp.nsimplify(b) * t / 2)
    T = rng.choice([4, 5, 6, 8, 10])
    g = sp.lambdify(t, v, 'math')
    N = 6000
    hstep = T / N
    dist = sum(abs(g((i + 0.5) * hstep)) for i in range(N)) * hstep
    disp = sum(g((i + 0.5) * hstep) for i in range(N)) * hstep
    if abs(dist - abs(disp)) < 0.01:
        return None
    return mk(f'The velocity of a particle is v(t) = {P(v)} m s⁻¹, 0 ≤ t ≤ {T}. Find (a) the displacement of the particle from its initial position at t = {T} (b) the total distance travelled.',
              f'(a) {s3(disp)} m (b) {s3(dist)} m', f'(a) ∫ v dt with GDC (M1) {s3(disp)} (A1). (b) ∫ |v| dt (M1) {s3(dist)} (A1).', 4)


@R.add('ch09-st2', 'C2', (2, 4), 'explain')
def dist_explain(rng, slot):
    k = rng.randint(2, 5)
    T = 2 * k if rng.random() < 0.5 else k + rng.randint(1, 3)
    v = t - k
    disp = sp.integrate(v, (t, 0, T))
    dist = sp.integrate(k - t, (t, 0, k)) + sp.integrate(t - k, (t, k, T))
    return mk(f'{who(rng)} says that a particle with velocity v = {P(v)} m s⁻¹ travels {P(abs(disp))} m between t = 0 and t = {T}, because ∫ from 0 to {T} of v dt = {P(disp)}. Explain the error and find the actual distance travelled.', f'{P(dist)} m',
              f'v changes sign at t = {k}, so the particle changes direction (R1); the integral of v gives net displacement, not distance (R1); distance = ∫|v| dt = {P(dist)} m (M1 A1).', 4, 'explain', 'G2')


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step', style='ext')
def dist_parts(rng, slot):
    p, q = sorted(rng.sample(range(1, 6), 2))
    v = sp.expand((t - p) * (t - q))
    T = q + rng.randint(1, 2)
    s0 = rng.randint(-3, 3)
    s_ = sp.integrate(v, t) + s0
    dist = sum(abs(sp.integrate(v, (t, a_, b_))) for a_, b_ in ((0, p), (p, q), (q, T)))
    parts = [('Find the times at which the particle changes direction.', f't = {p}, {q}', 'v = 0 (M1) A1', 2, True),
             ('Find an expression for the displacement s(t).', f's = {P(s_)}', 'integrate (M1) A1; constant (A1)', 3, True),
             (f'Find the total distance travelled in the first {T} seconds.', P(dist), 'split at turning points (M1) A1 A1', 3, True),
             (f'Find the displacement from the start at t = {T}.', P(s_.subs(t, T) - s0), 'A1', 1, False),
             ('Find the acceleration at the first instant the particle is at rest.', P(sp.diff(v, t).subs(t, p)), 'a = dv/dt (M1) A1', 2, False)]
    return build_parts(rng, [f'A particle moves along a line with velocity v = {P(v)} m s⁻¹ for t ≥ 0. Initially it is {s0} m from O.'.replace(' −', ' −'),
                             f'The velocity of a bead on a wire is v(t) = {P(v)} m s⁻¹ and s(0) = {s0} m.'], parts, 3)


@R.add('ch09-st2', 'C1', (1, 3), 'mcq')
def dist_mcq(rng, slot):
    a, b = rng.randint(2, 9), rng.randint(1, 8)
    return mcq(rng, f'A runner jogs {a} km east and then {b} km west along a straight road. What are her distance travelled and displacement?', f'{a + b} km; {abs(a - b)} km {"east" if a > b else "west" if b > a else ""}'.strip(),
               [f'{abs(a - b)} km; {a + b} km east', f'{a + b} km; {a + b} km east', f'{abs(a - b)} km; {abs(a - b)} km east'], 'Distance adds the lengths; displacement is the net change.')


# ---------------------------------------------------------------------------------------------
R.facts('ch09-st3', F(
    terms=[('simple harmonic motion (model)', 'motion with displacement of the form s = A sin(ωt + φ), which oscillates about a centre with period 2π/ω'),
           ('exponential decay of velocity', 'a model v = v₀e^(−kt) in which a body slows down, approaching rest but never reaching it')],
    facts=[('If s = 3 sin(2t), the maximum speed is', '6', ['3', '2', '12'], 'v = 6 cos 2t, max |v| = 6.'),
           ('If v = 10e^(−0.5t), as t → ∞ the velocity', 'tends to 0', ['tends to 10', 'becomes negative', 'tends to −0.5'], 'e^(−0.5t) → 0.'),
           ('For s = 4 cos(πt), the particle first returns to its starting position at t =', '2', ['1', 'π', '4'], 'Period 2π/π = 2.')],
    why=[('Explain why a particle with v = 5e^(−0.2t) never reaches a distance of 25 m from its start.', 's = ∫ from 0 to t of 5e^(−0.2u) du = 25(1 − e^(−0.2t)) < 25 for all t, approaching 25 as t → ∞.'),
         ('Explain why for s = A sin(ωt) the acceleration is always directed towards the centre.', 'a = −Aω² sin(ωt) = −ω² s, which has the opposite sign to s.'),
         ('Explain why the speed of an oscillating particle is greatest at the centre of the motion.', 'For s = A sin ωt, v = Aω cos ωt; |v| is largest when sin ωt = 0, i.e. s = 0.')],
    misc=[('If s = 2 sin 3t then v = 2 cos 3t.', 'Chain rule: v = 6 cos 3t.'),
          ('If v = 4e^(−t) then the distance travelled up to t = 10 is 4e^(−10).', 'Integrate: 4(1 − e^(−10)) ≈ 4.00 m.')],
))


@R.add('ch09-st3', 'C3', (2, 5), 'short', style='p1')
def kin_trig_exact(rng, slot):
    A, w = rng.randint(2, 8), rng.choice([1, 2, 3, sp.Rational(1, 2), pi / 2])
    fn = rng.choice(['sin', 'cos'])
    s_ = A * (sp.sin(w * t) if fn == 'sin' else sp.cos(w * t))
    v, a = sp.diff(s_, t), sp.diff(s_, t, 2)
    T1 = rng.choice([pi / 6, pi / 4, pi / 3, pi / 2]) / w if w != pi / 2 else rng.choice([sp.Rational(1, 3), sp.Rational(1, 2), 1])
    want = rng.choice(['v', 'a', 'max', 'rest'])
    if want == 'v':
        q_, ans, key = f'Find the exact velocity at t = {P(T1)}.', P(sp.radsimp(v.subs(t, T1))), f'v = ds/dt = {P(v)} (M1 A1); substitute (A1).'
    elif want == 'a':
        q_, ans, key = f'Find the exact acceleration at t = {P(T1)}.', P(sp.radsimp(a.subs(t, T1))), f'a = {P(a)} (M1 A1); substitute (A1).'
    elif want == 'max':
        q_, ans, key = 'Find the maximum speed of the particle.', P(A * w), f'v = {P(v)} (M1 A1); max |v| = {P(A * w)} (A1).'
    else:
        first = sp.simplify((pi / 2) / w) if fn == 'sin' else sp.simplify(pi / w)
        q_, ans, key = 'Find the first time t > 0 at which the particle is at rest.', f't = {P(first)}', f'v = {P(v)} = 0 (M1 A1); t = {P(first)} (A1).'
    return mk(f'A particle oscillates so that its displacement is s = {P(s_)} cm at time t seconds. {q_}', ans, key, 3)


@R.add('ch09-st3', 'C3', (2, 5), 'short', style='p2')
def kin_exp(rng, slot):
    v0, k = rng.randint(5, 30), round(rng.uniform(0.1, 0.8), 2)
    T = rng.randint(2, 10)
    dist = v0 / k * (1 - math.exp(-k * T))
    want = rng.choice(['dist', 'half', 'acc'])
    ctx = rng.choice(['A boat cuts its engine and drifts', 'A puck slides across ice', 'A cyclist stops pedalling and freewheels'])
    if want == 'dist':
        return mk(f'{ctx}; its velocity is v = {v0}e^(−{k}t) m s⁻¹, t seconds later. Find the distance travelled in the first {T} seconds and the limiting distance as t → ∞.',
                  f'{s3(dist)} m; {s3(v0 / k)} m', f'∫ from 0 to {T} of v dt (M1) = ({v0}/{k})(1 − e^(−{k * T:g})) (A1) = {s3(dist)} (A1); limit {v0}/{k} = {s3(v0 / k)} (A1).', 4)
    if want == 'half':
        th = math.log(2) / k
        return mk(f'{ctx}; its velocity is v = {v0}e^(−{k}t) m s⁻¹. Find the time taken for the velocity to halve, and the distance travelled in that time.',
                  f't = {s3(th)} s; {s3(v0 / (2 * k))} m', f'e^(−{k}t) = 0.5 (M1); t = ln 2/{k} = {s3(th)} (A1); distance ∫ v dt = {v0}/(2 × {k}) = {s3(v0 / (2 * k))} (M1 A1).', 4)
    return mk(f'{ctx}; its velocity is v = {v0}e^(−{k}t) m s⁻¹. Find its acceleration at t = {T} and explain the sign.', f'{s3(-k * v0 * math.exp(-k * T))} m s⁻²',
              f'a = dv/dt = −{s3(k * v0)}e^(−{k}t) (M1 A1); a({T}) = {s3(-k * v0 * math.exp(-k * T))} (A1); negative because it is slowing down (R1).', 4)


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step', style='ext')
def kin_trig_parts(rng, slot):
    A, w = rng.randint(2, 6), rng.choice([1, 2, 3])
    c = rng.randint(1, 3)
    v = A * sp.cos(w * t)
    s0 = c
    s_ = sp.integrate(v, t) + s0
    T = pi / w
    parts = [('Find an expression for the displacement s(t).', f's = {P(s_)}', 'integrate (M1) A1; constant (A1)', 3, True),
             (f'Find the times in 0 ≤ t ≤ {P(2 * pi / w)} when the particle is at rest.', lst([pi / (2 * w), 3 * pi / (2 * w)]), 'v = 0 (M1) A1 A1', 3, True),
             ('Find the maximum displacement from O.', P(A / sp.Integer(w) + c), 'A1', 1, True),
             (f'Find the total distance travelled in 0 ≤ t ≤ {P(T)}.', P(sp.Rational(2 * A, w)), 'split at rest point (M1) A1', 2, False),
             ('Show that a = −' + (f'{w * w}' if w > 1 else '') + '(s − ' + str(c) + ').', 'shown', 'a = dv/dt (M1) substitute (A1) AG', 2, False)]
    return build_parts(rng, [f'A particle moves in a straight line with velocity v = {P(v)} m s⁻¹. When t = 0 it is {s0} m from O.', f'The velocity of a piston is v(t) = {P(v)} m s⁻¹ and its initial displacement from O is {s0} m.'], parts, 3)


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step', style='p2')
def kin_damped_parts(rng, slot):
    A, k, w = rng.randint(3, 10), round(rng.uniform(0.1, 0.5), 2), rng.choice([2, 3, 1.5, 2.5])
    v = A * sp.exp(-k * t) * sp.sin(w * t)
    g = sp.lambdify(t, v, 'math')
    T = rng.choice([4, 5, 6, 8])
    r_ = [r for r in nsols(g, 0.01, T) if r > 0.02]
    N = 6000
    hstep = T / N
    dist = sum(abs(g((i + 0.5) * hstep)) for i in range(N)) * hstep
    disp = sum(g((i + 0.5) * hstep) for i in range(N)) * hstep
    parts = [(f'Find the times in 0 < t ≤ {T} at which the particle changes direction.', lst3(r_) if r_ else 'none', 'GDC (A1 A1)', 2, True),
             (f'Find the displacement of the particle from its starting point at t = {T}.', s3(disp), '∫ v dt (M1) A1', 2, True),
             (f'Find the total distance travelled in the first {T} seconds.', s3(dist), '∫|v| dt (M1) A1', 2, True),
             ('Find the maximum speed of the particle in this interval.', s3(max(abs(g((i + 0.5) * hstep)) for i in range(N))), 'GDC (A1)', 1, False)]
    return build_parts(rng, [f'A particle moves in a straight line with velocity v(t) = {A}e^(−{k}t) sin({w}t) m s⁻¹, t ≥ 0.', f'The velocity of a damped oscillating spring is modelled by v(t) = {A}e^(−{k}t) sin({w}t) m s⁻¹.'], parts, 3)


@R.add('ch09-st3', 'C2', (2, 4), 'explain')
def kin_shm_explain(rng, slot):
    A, w = rng.randint(2, 9), rng.randint(2, 5)
    return mk(f'A particle has displacement s = {A} sin({w}t). Explain why its acceleration is always directed towards O and find where its speed is greatest.', f'a = −{w * w}s; greatest speed {A * w} at s = 0',
              f'v = {A * w} cos({w}t), a = −{A * w * w} sin({w}t) = −{w * w}s (M1 A1); opposite sign to s so towards O (R1); |v| max = {A * w} when sin({w}t) = 0, i.e. at O (A1).', 4, 'explain')


@R.add('ch09-st3', 'C1', (1, 3), 'mcq')
def kin_trig_mcq(rng, slot):
    A, w = rng.randint(2, 9), rng.randint(2, 6)
    return mcq(rng, f'A particle moves with s = {A} cos({w}t). Its velocity is', f'−{A * w} sin({w}t)', [f'{A * w} sin({w}t)', f'−{A} sin({w}t)', f'{A} sin({w}t)/{w}'], 'Chain rule.')


# =============================================================================================
# ch10 Further integration
# =============================================================================================
def check_anti(F_, f):
    return sp.simplify(sp.diff(F_, x) - f) == 0


R.facts('ch10-st1', F(
    terms=[('integration by substitution', 'replacing part of the integrand by u = g(x), with du = g′(x)dx, to turn the integral into a standard one in u'),
           ('change of limits', 'in a definite integral by substitution, converting the x-limits to the corresponding u-limits so there is no need to return to x')],
    facts=[('To find ∫ x(x² + 1)⁵ dx, a suitable substitution is', 'u = x² + 1', ['u = x', 'u = (x² + 1)⁵', 'u = x⁵'], 'du = 2x dx matches the factor x.'),
           ('With u = ln x, ∫ (ln x)/x dx becomes', '∫ u du', ['∫ u/x du', '∫ ln u du', '∫ eᵘ du'], 'du = dx/x.'),
           ('Using u = 2x + 1 in ∫ from 0 to 1 of (2x + 1)³ dx, the new limits are', 'u = 1 to u = 3', ['u = 0 to u = 1', 'u = 0 to u = 3', 'u = 1 to u = 2'], 'Substitute x = 0 and x = 1.')],
    why=[('Explain why the substitution u = x² + 4 works well for ∫ x√(x² + 4) dx.', 'du/dx = 2x, so x dx = ½ du; the integrand becomes ½√u, a standard power of u.'),
         ('Explain why changing the limits avoids substituting back in a definite integral.', 'The definite integral in u over the corresponding u-interval has the same value, so it can be evaluated directly in u.'),
         ('Explain how to decide whether a substitution will succeed.', 'After writing dx in terms of du, every x must disappear (or be expressible in u); if a factor of x remains that cannot be written in u, the substitution fails.')],
    misc=[('∫ x(x² + 1)³ dx = (x² + 1)⁴/4 + C.', 'With u = x² + 1, x dx = du/2, so the result is (x² + 1)⁴/8 + C.'),
          ('When substituting in a definite integral you may keep the x-limits while integrating in u.', 'The limits must be changed to u-values (or the answer converted back to x before substituting).')],
))


def _subst(rng):
    kind = rng.choice(['poly', 'sqrt_lin', 'exp_frac', 'trig_pow', 'lnx', 'quart', 'exp_sq', 'lin_frac'])
    k = rng.randint(1, 6)
    n = rng.choice([2, 3, 4, 5])
    if kind == 'poly':
        a = rng.choice([1, 2, 3])
        f = x * (a * x ** 2 + k) ** n
        F_ = (a * x ** 2 + k) ** (n + 1) / (2 * a * (n + 1))
        sub = f'u = {P(a * x ** 2 + k)}'
    elif kind == 'sqrt_lin':
        f = x * sp.sqrt(x + k)
        F_ = sp.Rational(2, 5) * (x + k) ** sp.Rational(5, 2) - sp.Rational(2 * k, 3) * (x + k) ** sp.Rational(3, 2)
        sub = f'u = x + {k}'
    elif kind == 'exp_frac':
        f = sp.exp(x) / (sp.exp(x) + k)
        F_ = sp.log(sp.exp(x) + k)
        sub = f'u = eˣ + {k}'
    elif kind == 'trig_pow':
        f = sp.cos(x) * sp.sin(x) ** n
        F_ = sp.sin(x) ** (n + 1) / (n + 1)
        sub = 'u = sin x'
    elif kind == 'lnx':
        f = sp.log(x) ** n / x
        F_ = sp.log(x) ** (n + 1) / (n + 1)
        sub = 'u = ln x'
    elif kind == 'quart':
        f = x ** 3 / (x ** 4 + k)
        F_ = sp.log(x ** 4 + k) / 4
        sub = f'u = x⁴ + {k}'
    elif kind == 'exp_sq':
        f = x * sp.exp(k * x ** 2)
        F_ = sp.exp(k * x ** 2) / (2 * k)
        sub = f'u = {P(k * x ** 2)}'
    else:
        f = x / (x + k) ** n
        F_ = sp.integrate(f, x)
        sub = f'u = x + {k}'
    assert check_anti(F_, f), (kind, f)
    return kind, f, F_, sub


@R.add('ch10-st1', 'C3', (1, 4), 'short')
def subst_indef(rng, slot):
    kind, f, F_, sub = _subst(rng)
    hint = rng.random() < (0.7 if slot.d <= 3 else 0.3)
    return mk(f'Find ∫ {P(f)} dx{", using the substitution " + sub if hint else ""}.', integ_txt(sp.factor(F_) if kind == 'sqrt_lin' else F_),
              f'{sub} and du in terms of dx (M1); integrand written entirely in u (A1); integrate in u (A1); substitute back, + C (A1).', 4 if hint else 5)


@R.add('ch10-st1', 'C3', (2, 5), 'short', style='p1')
def subst_definite(rng, slot):
    kind, f, F_, sub = _subst(rng)
    if kind in ('lnx',):
        a, b = 1, sp.E
    elif kind == 'trig_pow':
        a, b = 0, rng.choice([pi / 2, pi / 6])
    elif kind == 'sqrt_lin':
        k = int(str(sub).split('+')[1])
        a, b = -k + rng.choice([0, 1]), rng.choice([v * v - k for v in range(2, 4)])
    elif kind == 'exp_frac':
        a, b = 0, sp.log(rng.choice([2, 3]))
    else:
        a, b = 0, rng.choice([1, 2])
    val = sp.simplify(F_.subs(x, b) - F_.subs(x, a))
    return mk(f'Use the substitution {sub} to find the exact value of ∫ from {P(a)} to {P(b)} of {P(f)} dx.', P(sp.nsimplify(val) if val.is_Rational else val),
              f'du in terms of dx (M1); change the limits to u-values using {sub} (A1); integral in u (A1); exact value {P(val)} (A1).', 5)


@R.add('ch10-st1', 'C1', (1, 3), 'mcq')
def subst_mcq(rng, slot):
    kind, f, F_, sub = _subst(rng)
    others = ['u = x', 'u = x²', 'u = sin x', 'u = ln x', 'u = eˣ', 'u = 1/x', 'u = cos x', 'u = x³']
    wr = [o for o in others if o != sub]
    rng.shuffle(wr)
    return mcq(rng, f'Which substitution is most suitable for ∫ {P(f)} dx?', sub, wr[:3], f'{sub}: its derivative appears as a factor of the integrand.')


@R.add('ch10-st1', 'C2', (2, 4), 'explain')
def subst_explain(rng, slot):
    kind, f, F_, sub = _subst(rng)
    return mk(f'Explain why the substitution {sub} is effective for ∫ {P(f)} dx, and state the integral in terms of u.', 'du is (a multiple of) the remaining factor',
              f'Differentiate: du/dx gives the remaining factor of the integrand up to a constant (R1); dx replaced correctly (M1); integral entirely in u (A1).', 3, 'explain')


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step', style='ext')
def subst_parts(rng, slot):
    k = rng.randint(1, 5)
    kind = rng.choice(['sqrt', 'frac'])
    if kind == 'sqrt':
        f = x ** 3 * sp.sqrt(x ** 2 + k)
        sub = f'u = x² + {k}'
        F_ = sp.integrate(f, x)
        a, b = 0, sp.sqrt(rng.choice([v * v - k for v in range(2, 4) if v * v - k > 0]))
    else:
        f = x / sp.sqrt(2 * x + k)
        sub = f'u = 2x + {k}'
        F_ = sp.integrate(f, x)
        a, b = 0, sp.Rational(rng.choice([v * v - k for v in range(2, 5) if v * v - k > 0]), 2)
    val = sp.simplify(F_.subs(x, b) - F_.subs(x, a))
    parts = [(f'Using {sub}, show that the integral ∫ {P(f)} dx can be written as an integral of powers of u.', 'shown', 'du in terms of dx (M1); x in terms of u (A1); integrand in u (A1) AG', 3, True),
             ('Hence find ∫ ' + P(f) + ' dx.', integ_txt(sp.simplify(F_)), 'integrate powers of u (A1 A1); back-substitute (A1)', 3, True),
             (f'Find the exact value of ∫ from {P(a)} to {P(b)} of {P(f)} dx.', P(val), 'limits (M1) A1', 2, True),
             ('Verify your answer to the indefinite integral by differentiation.', 'derivative returns the integrand', 'R1', 1, False)]
    return build_parts(rng, ['This question is about integration by substitution.', f'Let I = ∫ {P(f)} dx.'], parts, 3)


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step')
def subst_reduction(rng, slot):
    n = rng.choice([3, 5])
    k = rng.randint(1, 3)
    f = sp.sin(x) ** n
    F_ = sp.integrate(f, x)
    val = sp.integrate(f, (x, 0, pi / 2))
    parts = [(f'Write sin{str(n).translate(_SUP)}x in terms of sin x and cos x so that the substitution u = cos x can be used.', f'sin x (1 − cos²x){"²" if n == 5 else ""}', 'Pythagorean identity (M1) A1', 2, True),
             (f'Hence find ∫ sin{str(n).translate(_SUP)}x dx.', integ_txt(sp.expand(F_)), 'u = cos x, du = −sin x dx (M1); integrate polynomial in u (A1 A1)', 3, True),
             (f'Find the exact value of ∫ from 0 to π/2 of sin{str(n).translate(_SUP)}x dx.', P(val), 'limits u = 1 to 0 (M1) A1', 2, True),
             ('Generalise: suggest a strategy for ∫ sinᵐx cosⁿx dx when m is odd, and justify it.', 'keep one sin x, convert the rest using sin²x = 1 − cos²x, then u = cos x', 'R1 R1', 2, False)]
    return build_parts(rng, ['This question investigates integrals of odd powers of sine.', f'Consider I = ∫ sin{str(n).translate(_SUP)}x dx.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st2', F(
    terms=[('integration by parts', '∫ u (dv/dx) dx = uv − ∫ v (du/dx) dx, from the product rule'),
           ('LIATE heuristic', 'a guide for choosing u in integration by parts: Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential'),
           ('repeated integration by parts', 'applying the parts formula more than once, e.g. for x²eˣ, or until the original integral reappears, e.g. for eˣ sin x')],
    facts=[('In ∫ x eˣ dx by parts, choose', 'u = x, dv/dx = eˣ', ['u = eˣ, dv/dx = x', 'u = x eˣ, dv/dx = 1', 'u = 1, dv/dx = x eˣ'], 'Differentiating x simplifies it.'),
           ('∫ ln x dx =', 'x ln x − x + C', ['1/x + C', 'x ln x + C', '(ln x)²/2 + C'], 'Parts with u = ln x, dv/dx = 1.'),
           ('∫ x cos x dx =', 'x sin x + cos x + C', ['x sin x − cos x + C', '−x sin x + cos x + C', 'x²sin x/2 + C'], 'u = x: x sin x − ∫ sin x dx.')],
    why=[('Explain why integration by parts is derived from the product rule.', 'd/dx(uv) = u v′ + v u′; integrating both sides and rearranging gives ∫ u v′ dx = uv − ∫ v u′ dx.'),
         ('Explain why for ∫ x ln x dx you should choose u = ln x rather than u = x.', 'ln x is hard to integrate but simple to differentiate (1/x); with u = ln x the new integral ∫ (x²/2)(1/x) dx is a simple power.'),
         ('Explain how ∫ eˣ sin x dx can be found even though the integral never becomes simpler.', 'After two applications of parts the original integral I reappears: I = eˣ sin x − eˣ cos x − I, so 2I = eˣ(sin x − cos x) and I can be solved for algebraically.')],
    misc=[('∫ x eˣ dx = x eˣ + C.', 'Differentiating x eˣ gives eˣ + x eˣ; by parts the answer is x eˣ − eˣ + C.'),
          ('∫ uv dx = (∫u dx)(∫v dx).', 'There is no product rule of that form for integrals; use ∫ u v′ dx = uv − ∫ v u′ dx.')],
))

PARTS = [lambda rng: x * sp.exp(rng.choice([1, 2, 3, -1]) * x), lambda rng: x * sp.sin(rng.choice([1, 2, 3]) * x), lambda rng: x * sp.cos(rng.choice([1, 2, 3]) * x),
         lambda rng: sp.log(x), lambda rng: x ** rng.choice([1, 2, 3]) * sp.log(x), lambda rng: x ** 2 * sp.exp(x), lambda rng: x ** 2 * sp.sin(x),
         lambda rng: sp.exp(x) * sp.sin(x), lambda rng: sp.exp(rng.choice([1, 2])) * 0 + sp.exp(x) * sp.cos(x), lambda rng: sp.atan(x), lambda rng: sp.asin(x),
         lambda rng: sp.log(x) / x ** 2]


@R.add('ch10-st2', 'C3', (1, 5), 'short')
def parts_indef(rng, slot):
    f = rng.choice(PARTS[:5] if slot.d <= 2 else PARTS)(rng)
    F_ = sp.simplify(sp.integrate(f, x))
    rep = f.has(sp.exp) and (f.has(sp.sin) or f.has(sp.cos)) or f.has(x ** 2)
    return mk(f'Find ∫ {P(f)} dx.', integ_txt(F_) if not f.has(sp.asin) else P(F_) + ' + C',
              ('Parts applied twice / cyclic (M1 M1); ' if rep else 'Choose u and dv/dx sensibly (M1); ') + f'uv − ∫ v du/dx (A1); remaining integral correct (A1); {P(F_)} + C (A1).', 6 if rep else 4)


@R.add('ch10-st2', 'C3', (2, 5), 'short', style='p1')
def parts_definite(rng, slot):
    f = rng.choice(PARTS[:6])(rng)
    if f.has(sp.log):
        a, b = 1, rng.choice([sp.E, 2, sp.E ** 2])
    elif f.has(sp.sin) or f.has(sp.cos):
        a, b = 0, rng.choice([pi / 2, pi])
    else:
        a, b = 0, rng.choice([1, 2, sp.log(2)])
    val = sp.simplify(sp.integrate(f, (x, a, b)))
    return mk(f'Find the exact value of ∫ from {P(a)} to {P(b)} of {P(f)} dx.', P(val),
              f'Integration by parts (M1); anti-derivative {P(sp.simplify(sp.integrate(f, x)))} (A1 A1); limits substituted (M1); {P(val)} (A1).', 5)


@R.add('ch10-st2', 'C1', (1, 3), 'mcq')
def parts_choice_mcq(rng, slot):
    pairs = [('x e^(3x)', 'u = x', ['u = e^(3x)', 'u = x e^(3x)', 'u = 3x']), ('x² ln x', 'u = ln x', ['u = x²', 'u = x² ln x', 'u = 1/x']),
             ('x sin(2x)', 'u = x', ['u = sin(2x)', 'u = 2x', 'u = cos(2x)']), ('arctan x', 'u = arctan x', ['u = 1', 'u = x', 'u = 1/(1 + x²)']),
             ('ln x', 'u = ln x', ['u = 1', 'u = x', 'u = 1/x']), ('x cos(5x)', 'u = x', ['u = cos(5x)', 'u = 5x', 'u = sin(5x)'])]
    f, r_, w = rng.choice(pairs)
    return mcq(rng, f'When using integration by parts for ∫ {f} dx, the best choice of u is', r_, w, 'Choose u so that du/dx is simpler and dv/dx is easy to integrate (LIATE).')


@R.add('ch10-st2', 'C2', (2, 4), 'explain')
def parts_explain(rng, slot):
    a = rng.choice([2, 3, 4, 5])
    kind = rng.choice(['badchoice', 'cyclic'])
    if kind == 'badchoice':
        return mk(f'{who(rng)} tries ∫ x e^({a}x) dx by parts with u = e^({a}x) and dv/dx = x. Explain why this choice makes the problem harder and state the better choice and result.',
                  P(sp.simplify(sp.integrate(x * sp.exp(a * x), x))) + ' + C',
                  f'With u = e^({a}x) the new integral ∫ (x²/2)({a}e^({a}x)) dx has a higher power of x (R1); choose u = x, dv/dx = e^({a}x) (M1); result (A1).', 3, 'explain')
    return mk(f'Explain why integrating e^({a}x) cos x by parts twice allows the integral to be found, and give the result.', P(sp.simplify(sp.integrate(sp.exp(a * x) * sp.cos(x), x))) + ' + C',
              'After two applications the original integral reappears with a coefficient ≠ 1 (R1); collect I terms and solve (M1); result (A1).', 3, 'explain')


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step', style='p3')
def parts_reduction(rng, slot):
    n = rng.choice([2, 3, 4])
    kind = rng.choice(['exp', 'ln'])
    if kind == 'exp':
        In = lambda m: sp.integrate(x ** m * sp.exp(x), (x, 0, 1))
        parts = [('Show that Iₙ = e − nIₙ₋₁ for n ≥ 1, where Iₙ = ∫ from 0 to 1 of xⁿeˣ dx.', 'shown', 'u = xⁿ, dv/dx = eˣ (M1); [xⁿeˣ] from 0 to 1 = e (A1); − n∫xⁿ⁻¹eˣ dx (A1) AG', 3, True),
                 ('Find I₀.', P(In(0)), 'A1', 1, True),
                 (f'Hence find the exact value of I{str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))}.', P(sp.simplify(In(n))), 'repeated use of the reduction formula (M1) A1', 2, True),
                 ('Explain why Iₙ > 0 and Iₙ decreases as n increases.', 'for 0 < x < 1, xⁿeˣ is positive and decreases as n increases', 'R1 R1', 2, False)]
        return build_parts(rng, ['Let Iₙ = ∫ from 0 to 1 of xⁿeˣ dx, for n ∈ ℕ.', 'This question develops a reduction formula.'], parts, 3)
    Jn = lambda m: sp.integrate(sp.log(x) ** m, (x, 1, sp.E))
    parts = [('Show that Jₙ = e − nJₙ₋₁, where Jₙ = ∫ from 1 to e of (ln x)ⁿ dx.', 'shown', 'u = (ln x)ⁿ, dv/dx = 1 (M1); [x(ln x)ⁿ] from 1 to e = e (A1); − n∫(ln x)ⁿ⁻¹ dx (A1) AG', 3, True),
             ('Find J₁.', P(Jn(1)), 'A1', 1, True),
             (f'Hence find J{str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))}.', P(sp.simplify(Jn(n))), 'M1 A1', 2, True)]
    return build_parts(rng, ['Let Jₙ = ∫ from 1 to e of (ln x)ⁿ dx.', 'A reduction formula is used to integrate powers of ln x.'], parts, 3)


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step', style='ext')
def parts_area(rng, slot):
    a = rng.choice([1, 2])
    f = x * sp.exp(-x / a) if a > 1 else x * sp.exp(-x)
    xm = a
    T = rng.choice([1, 2, 3]) * a
    A_ = sp.simplify(sp.integrate(f, (x, 0, T)))
    parts = [('Find the coordinates of the maximum point of the curve.', f'({a}, {P(sp.simplify(f.subs(x, a)))})', 'product rule (M1) A1 A1', 3, True),
             ('Use integration by parts to find ∫ ' + P(f) + ' dx.', integ_txt(sp.simplify(sp.integrate(f, x))), 'M1 A1 A1', 3, True),
             (f'Find the exact area enclosed by the curve, the x-axis and the line x = {T}.', P(A_), 'limits (M1) A1', 2, True),
             ('Find the limit of this area as the right-hand boundary tends to infinity.', P(sp.integrate(f, (x, 0, sp.oo))), 'limit of x e^(−x/a) → 0 (R1) A1', 2, False)]
    return build_parts(rng, [f'Consider the curve y = {P(f)}, x ≥ 0.', f'The graph of f(x) = {P(f)} for x ≥ 0 is considered.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st3', F(
    terms=[('partial fractions', 'writing a rational function as a sum of simpler fractions, e.g. (5x + 1)/((x − 1)(x + 2)) = 2/(x − 1) + 3/(x + 2)'),
           ('standard arctan integral', '∫ 1/(a² + x²) dx = (1/a) arctan(x/a) + C'),
           ('standard arcsin integral', '∫ 1/√(a² − x²) dx = arcsin(x/a) + C, for |x| < a')],
    facts=[('∫ 1/(9 + x²) dx =', '(1/3)arctan(x/3) + C', ['arctan(x/3) + C', '3arctan(3x) + C', 'ln(9 + x²) + C'], 'a = 3.'),
           ('∫ 1/√(4 − x²) dx =', 'arcsin(x/2) + C', ['2arcsin(x/2) + C', '(1/2)arcsin(x/2) + C', 'arctan(x/2) + C'], 'a = 2.'),
           ('Before integrating 1/(x² + 4x + 13) you should', 'complete the square: (x + 2)² + 9', ['use partial fractions', 'substitute u = x²', 'use integration by parts'], 'The quadratic has no real roots.')],
    why=[('Explain why 1/(x² − 4) is integrated with partial fractions but 1/(x² + 4) with arctan.', 'x² − 4 = (x − 2)(x + 2) factorises into real linear factors; x² + 4 does not, so it matches the standard form 1/(a² + x²).'),
         ('Explain why ∫ 2x/(x² + 9) dx is not an arctan integral.', 'The numerator is the derivative of the denominator, so the integral is ln(x² + 9) + C by inspection.'),
         ('Explain how completing the square turns ∫ 1/(x² + 6x + 10) dx into a standard result.', 'x² + 6x + 10 = (x + 3)² + 1; with u = x + 3 it becomes ∫ 1/(u² + 1) du = arctan(x + 3) + C.')],
    misc=[('∫ 1/(x² + 16) dx = arctan(x/4) + C.', 'The coefficient is missing: (1/4)arctan(x/4) + C.'),
          ('∫ 1/((x − 1)(x + 1)) dx = ln|x − 1| · ln|x + 1| + C.', 'Use partial fractions: ½ln|x − 1| − ½ln|x + 1| + C.')],
))


@R.add('ch10-st3', 'C3', (2, 5), 'short')
def partial_frac_int(rng, slot):
    a, b = rng.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    A, B = nz(rng, -5, 5), nz(rng, -5, 5)
    num = sp.expand(A * (x - b) + B * (x - a))
    if num == 0:
        return None
    den = sp.expand((x - a) * (x - b))
    F_ = A * sp.log(x - a) + B * sp.log(x - b)
    return mk(f'(a) Express ({P(num)})/({P(den)}) in partial fractions. (b) Hence find ∫ ({P(num)})/({P(den)}) dx.',
              f'(a) {P(A)}/({P(x - a)}) + {P(B)}/({P(x - b)}) (b) {integ_txt(F_)}'.replace('+ −', '− '),
              f'(a) factorise denominator (A1); {P(num)} = A({P(x - b)}) + B({P(x - a)}) (M1); A = {A}, B = {B} (A1 A1). (b) {integ_txt(F_)} (A1 A1).', 6)


@R.add('ch10-st3', 'C3', (1, 4), 'short', style='p1')
def arctan_arcsin_int(rng, slot):
    a = rng.choice([1, 2, 3, 4, 5, sp.sqrt(3), sp.sqrt(2)])
    kind = rng.choice(['tan', 'sin', 'tan_k'])
    if kind == 'tan':
        f = 1 / (a ** 2 + x ** 2)
        F_ = sp.atan(x / a) / a
    elif kind == 'sin':
        f = 1 / sp.sqrt(a ** 2 - x ** 2)
        F_ = sp.asin(x / a)
    else:
        c = rng.choice([4, 9, 16])
        k = rng.randint(1, 3)
        f = 1 / (c * x ** 2 + k ** 2)
        F_ = sp.atan(sp.sqrt(c) * x / k) / (sp.sqrt(c) * k)
    assert check_anti(F_, f)
    definite = slot.d >= 3 and kind != 'tan_k'
    if definite:
        b = a * rng.choice([1, sp.sqrt(3), 1 / sp.sqrt(3)]) if kind == 'tan' else a * rng.choice([sp.Rational(1, 2), sp.sqrt(3) / 2, sp.sqrt(2) / 2])
        val = sp.simplify(F_.subs(x, b) - F_.subs(x, 0))
        return mk(f'Find the exact value of ∫ from 0 to {P(b)} of {P(f)} dx.', P(val), f'standard result {P(F_)} (M1 A1); exact inverse-trig value (A1); {P(val)} (A1).', 4)
    return mk(f'Find ∫ {P(f)} dx.', P(F_) + ' + C', f'Recognise the standard form (M1); {P(F_)} + C (A1 A1).', 3)


@R.add('ch10-st3', 'C3', (3, 5), 'short', style='p1')
def complete_square_int(rng, slot):
    h = nz(rng, -4, 4)
    k = rng.choice([1, 2, 3, 4])
    den = sp.expand((x + h) ** 2 + k ** 2)
    F_ = sp.atan((x + h) / k) / k
    return mk(f'By completing the square, find ∫ 1/({P(den)}) dx.', P(F_) + ' + C',
              f'{P(den)} = ({P(x + h)})² + {k ** 2} (M1 A1); u = {P(x + h)} (M1); {P(F_)} + C (A1).', 4)


@R.add('ch10-st3', 'C2', (2, 4), 'explain')
def pf_choose_explain(rng, slot):
    k = rng.choice([1, 4, 9, 16, 25])
    c = rng.choice([1, 2, 3])
    choices = [(f'1/(x² − {k})', 'partial fractions (x² − ' + str(k) + ' factorises)'), (f'1/(x² + {k})', f'arctan: (1/{P(sp.sqrt(k))})arctan(x/{P(sp.sqrt(k))})'),
               (f'{2 * c}x/(x² + {k})', f'inspection: {c} ln(x² + {k})'), (f'1/√({k} − x²)', f'arcsin(x/{P(sp.sqrt(k))})')]
    f, m_ = rng.choice(choices)
    return mk(f'Explain which method you would use to find ∫ {f} dx and why, then state the result.', m_,
              'Identify the structure of the integrand (R1); justify the method (R1); correct result (A1).', 3, 'explain')


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step', style='ext')
def pf_parts(rng, slot):
    a, b = rng.sample([1, 2, 3, 4], 2)
    A, B = rng.randint(1, 4), rng.randint(1, 4)
    num = sp.expand(A * (x + b) + B * (x + a))
    den = sp.expand((x + a) * (x + b))
    val = sp.simplify(sp.integrate(num / den, (x, 0, 1)))
    parts = [(f'Express ({P(num)})/({P(den)}) in partial fractions.', f'{A}/(x + {a}) + {B}/(x + {b})', 'M1 A1 A1', 3, True),
             (f'Hence show that ∫ from 0 to 1 of ({P(num)})/({P(den)}) dx = {P(sp.expand_log(val, force=True))}.', 'shown', 'integrate (A1 A1); limits (M1) AG', 3, True),
             ('Write your answer as a single logarithm.', P(sp.logcombine(sp.expand_log(val, force=True), force=True)), 'log laws (M1) A1', 2, False),
             (f'Explain why the integral from −{max(a, b) + 1} to 0 of the same function cannot be evaluated in this way.', 'the integrand has vertical asymptotes in that interval', 'R1', 1, False)]
    return build_parts(rng, ['This question is about integration using partial fractions.', f'Let f(x) = ({P(num)})/({P(den)}), x ≥ 0.'], parts, 3)


@R.add('ch10-st3', 'C1', (1, 3), 'mcq')
def pf_mcq(rng, slot):
    a = rng.choice([2, 3, 4, 5, 6])
    return mcq(rng, f'Find ∫ 1/({a * a} + x²) dx.', f'(1/{a}) arctan(x/{a}) + C', [f'arctan(x/{a}) + C', f'{a} arctan(x/{a}) + C', f'ln({a * a} + x²) + C'], f'Standard result with a = {a}.')


# ---------------------------------------------------------------------------------------------
R.facts('ch10-st4', F(
    terms=[('volume of revolution about the x-axis', 'V = π∫ from a to b of y² dx for the region under y = f(x) rotated 2π about the x-axis'),
           ('volume of revolution about the y-axis', 'V = π∫ from c to d of x² dy, with x expressed in terms of y'),
           ('area between a curve and the y-axis', '∫ from c to d of |x| dy, with x written as a function of y')],
    facts=[('Rotating y = √x, 0 ≤ x ≤ 4, through 2π about the x-axis gives volume', '8π', ['4π', '16π', '2π'], 'π∫x dx from 0 to 4 = 8π.'),
           ('For a volume about the y-axis you integrate', 'πx² with respect to y', ['πy² with respect to x', '2πxy', 'πx² with respect to x'], 'Discs are horizontal.'),
           ('A cone of radius r and height h can be generated by rotating', 'y = (r/h)x, 0 ≤ x ≤ h, about the x-axis', ['y = rx about the y-axis', 'y = x² about the x-axis', 'y = r about the x-axis'], 'The line from the origin to (h, r).')],
    why=[('Explain why the formula for a volume of revolution about the x-axis contains y².', 'Each thin slice is a disc of radius y and thickness δx with volume πy²δx; summing and taking the limit gives π∫y² dx.'),
         ('Explain why, to rotate about the y-axis, the equation must be rearranged to x = g(y).', 'The discs are perpendicular to the y-axis with radius x, so the integrand πx² must be a function of y and the limits are y-values.'),
         ('Explain how to find the volume generated by rotating the region between two curves about the x-axis.', 'Subtract the inner volume from the outer: π∫(y_outer² − y_inner²) dx, which is not π∫(y_outer − y_inner)² dx.')],
    misc=[('The volume obtained by rotating the region between y = 2 and y = x about the x-axis is π∫(2 − x)² dx.', 'Use washers: π∫(2² − x²) dx over the region; squaring the difference is wrong.'),
          ('Area between y = x² and the y-axis from y = 0 to 4 is ∫ from 0 to 4 of x² dx.', 'Integrate x as a function of y: ∫ from 0 to 4 of √y dy = 16/3.')],
))


@R.add('ch10-st4', 'C3', (2, 5), 'short', style='p1')
def vol_x(rng, slot):
    kind = rng.choice(['sqrt', 'poly', 'exp', 'recip', 'sin'])
    if kind == 'sqrt':
        k = rng.randint(1, 4); f = sp.sqrt(k * x); a, b = 0, rng.choice([1, 2, 4])
    elif kind == 'poly':
        f = x ** 2 + rng.randint(0, 2); a, b = 0, rng.choice([1, 2])
    elif kind == 'exp':
        f = sp.exp(rng.choice([1, -1]) * x); a, b = 0, rng.choice([1, sp.log(2)])
    elif kind == 'recip':
        f = 1 / x; a, b = 1, rng.choice([2, 3, 4])
    else:
        f = sp.sin(x); a, b = 0, pi
    V = sp.simplify(pi * sp.integrate(f ** 2, (x, a, b)))
    ft = ('√x' if k == 1 else f'√({k}x)') if kind == 'sqrt' else P(f)
    return mk(f'The region bounded by y = {ft}, the x-axis and the lines x = {P(a)} and x = {P(b)} is rotated through 2π about the x-axis. Find the exact volume generated.', P(V),
              f'V = π∫ y² dx (M1); integrand {P(sp.expand(f ** 2))} (A1); integrate (A1); {P(V)} (A1).', 4)


@R.add('ch10-st4', 'C3', (2, 5), 'short', style='p1')
def vol_y_area_y(rng, slot):
    kind = rng.choice(['vol', 'area'])
    n = rng.choice([2, 3])
    c, d = 0, rng.choice([1, 4, 8, 9])
    f = x ** n
    g = y ** sp.Rational(1, n)
    if kind == 'vol':
        V = sp.simplify(pi * sp.integrate(g ** 2, (y, c, d)))
        return mk(f'The region between the curve y = {P(f)} (x ≥ 0), the y-axis and the line y = {d} is rotated through 2π about the y-axis. Find the exact volume.', P(V),
                  f'x = {P(g)} (M1); V = π∫ x² dy (M1); π∫ from 0 to {d} of {P(g ** 2)} dy (A1); {P(V)} (A1).', 4)
    A_ = sp.integrate(g, (y, c, d))
    return mk(f'Find the exact area of the region enclosed by the curve y = {P(f)} (x ≥ 0), the y-axis and the line y = {d}.', P(A_),
              f'x = {P(g)} (M1); area = ∫ x dy from 0 to {d} (M1); {P(A_)} (A1 A1).', 4)


@R.add('ch10-st4', 'C3', (3, 5), 'short', style='p2')
def vol_gdc(rng, slot):
    a = rng.choice([1, 2, 3])
    f = rng.choice([sp.exp(-x ** 2 / 2), x * sp.sin(x), sp.log(x + 1), sp.sqrt(x) * sp.exp(-x / a)])
    lo, hi = 0, rng.choice([1, 2, 3])
    g = sp.lambdify(x, f ** 2, 'math')
    N = 4000
    hstep = (hi - lo) / N
    V = math.pi * sum(g(lo + (i + 0.5) * hstep) for i in range(N)) * hstep
    return mk(f'The region under y = {P(f)} from x = {lo} to x = {hi} is rotated 2π about the x-axis. Find the volume of the solid formed.', s3(V),
              f'V = π∫ from {lo} to {hi} of ({P(f)})² dx (M1 A1); GDC: {s3(V)} (A1).', 3)


@R.add('ch10-st4', 'C2', (2, 4), 'explain')
def vol_explain(rng, slot):
    r, h = rng.randint(2, 9), rng.randint(2, 12)
    return mk(f'Explain how rotating the line y = ({r}/{h})x for 0 ≤ x ≤ {h} about the x-axis produces a cone, and use integration to verify that its volume is (1/3)πr²h.', f'{P(sp.Rational(r * r * h, 3) * pi)}',
              f'The line joins (0, 0) to ({h}, {r}); rotating gives circular cross-sections with radius growing linearly (R1); V = π∫ from 0 to {h} of ({r}/{h})²x² dx (M1) = π({r * r}/{h * h})({h ** 3}/3) (A1) = {P(sp.Rational(r * r * h, 3) * pi)} = (1/3)π({r})²({h}) (A1).', 4, 'explain')


@R.add('ch10-st4', 'C4', (3, 5), 'multi_step', style='ext')
def vol_washer_parts(rng, slot):
    k = rng.choice([1, 2, 3, 4, 5])
    kind = rng.choice(['line_par', 'root_line', 'par_par', 'cubic_line'])
    if kind == 'line_par':
        f, g = k * x, x ** 2
    elif kind == 'root_line':
        f, g = sp.sqrt(k * x), x
    elif kind == 'par_par':
        f, g = 2 * k * x - x ** 2, x ** 2
    else:
        f, g = k * k * x, x ** 3
    xs_ = sorted([r for r in sp.solve(sp.Eq(f, g), x) if r.is_real and r >= 0], key=float)
    if len(xs_) < 2:
        return None
    a_, b_ = xs_[0], xs_[1]
    A_ = sp.simplify(sp.integrate(f - g, (x, a_, b_)))
    V = sp.simplify(pi * sp.integrate(f ** 2 - g ** 2, (x, a_, b_)))
    pts = ', '.join(f'({P(v)}, {P(g.subs(x, v))})' for v in (a_, b_))
    parts = [(f'Find the coordinates of the points of intersection of y = {P(f)} and y = {P(g)}.', pts, 'equate (M1) A1 A1', 3, True),
             ('Find the exact area of the region R between the curves.', P(A_), f'∫ from {P(a_)} to {P(b_)} of ({P(f)} − ({P(g)})) dx (M1) A1', 2, True),
             ('Find the exact volume generated when R is rotated through 2π about the x-axis.', P(V), 'washer π∫(y₁² − y₂²) dx (M1) A1 A1', 3, True),
             ('Explain why the volume is not π∫(y₁ − y₂)² dx.', 'each cross-section is an annulus of area π(y₁² − y₂²)', 'R1', 1, False)]
    if kind in ('line_par', 'root_line'):
        if kind == 'line_par':
            Vy = sp.simplify(pi * sp.integrate(y - y ** 2 / k ** 2, (y, 0, k * k)))
        else:
            Vy = sp.simplify(pi * sp.integrate(y ** 2 - y ** 4 / k ** 2, (y, 0, k)))
        parts.append(('Find the exact volume generated when R is rotated through 2π about the y-axis.', P(Vy), 'x in terms of y for each curve (M1); π∫(x_outer² − x_inner²) dy (M1) A1', 3, False))
    out = build_parts(rng, [f'The region R is enclosed by the curves y = {P(f)} and y = {P(g)}.', f'Let R be the finite region bounded by y = {P(g)} and y = {P(f)}, x ≥ 0.',
                             f'This question concerns the region R between y = {P(f)} and y = {P(g)}.'], parts, 3)
    if kind == 'root_line':
        for kk in ('stem', 'markingKey'):
            out[kk] = out[kk].replace(P(f), '√x' if k == 1 else f'√({k}x)')
    return out


@R.add('ch10-st4', 'C4', (4, 5), 'multi_step', style='p3')
def vol_family(rng, slot):
    n = rng.choice([1, 2, 3])
    a = rng.choice([1, 2, 3, 4])
    f = x ** n
    m = sp.Symbol('n', positive=True)
    Vx = sp.simplify(pi * sp.integrate(f ** 2, (x, 0, a)))
    Vcyl = pi * a * (a ** n) ** 2
    parts = [(f'Find the exact volume V₁ generated when the region under y = {P(f)} from x = 0 to x = {a} is rotated 2π about the x-axis.', P(Vx), 'π∫y² dx (M1) A1', 2, True),
             (f'Find the ratio of V₁ to the volume of the cylinder of radius {P(a ** n)} and height {a}.', P(sp.Rational(1, 2 * n + 1)), 'cylinder πr²h (M1) A1', 2, True),
             ('Show that, for the curve y = xⁿ, the ratio in part (b) is 1/(2n + 1) for all n > 0.', 'shown', 'π∫ x²ⁿ dx = πa²ⁿ⁺¹/(2n + 1) (M1 A1); divide by πa·a²ⁿ (M1) AG', 3, True),
             ('Hence state the ratio for the cone (n = 1) and explain its geometric meaning.', '1/3', 'a cone has one third of the volume of the enclosing cylinder (R1) A1', 2, False),
             ('Find the limit of the ratio as n → ∞ and interpret it.', '0', 'A1; the solid becomes thin except near x = a (R1)', 2, False)]
    return build_parts(rng, [f'This question investigates volumes of solids formed by rotating y = xⁿ about the x-axis.', f'Consider the family of curves y = xⁿ, 0 ≤ x ≤ {a}, n > 0.'], parts, 3)


@R.add('ch10-st4', 'C1', (1, 3), 'mcq')
def vol_mcq(rng, slot):
    r = rng.randint(1, 6)
    h = rng.randint(1, 8)
    return mcq(rng, f'The region under y = {r}, 0 ≤ x ≤ {h}, is rotated 2π about the x-axis. The volume is', f'{r * r * h}π', [f'{r * h}π', f'{2 * r * h}π', f'{r * r * h}'], 'A cylinder: π∫ r² dx = πr²h.')


# =============================================================================================
# ch11 Differential equations (AHL 5.18)
# =============================================================================================
def sfig(v, n=4):
    v = float(v)
    if v == 0:
        return '0'
    mag = math.floor(math.log10(abs(v)))
    dec = max(0, n - 1 - mag)
    return (f'{round(v, dec):.{dec}f}' if dec else str(int(round(v, n - 1 - mag)))).replace('-', '−')


def de_ok(sol, rhs, var=x):
    """sol is y(var); rhs a sympy expression in var and y. True if dy/dvar = rhs."""
    d = sp.diff(sol, var) - rhs.subs(y, sol)
    try:
        if sp.simplify(d) == 0:
            return True
    except Exception:
        pass
    for v in (0.37, 0.81, 1.23):
        try:
            if abs(complex(d.subs(var, v).evalf())) > 1e-8:
                return False
        except Exception:
            return False
    return True


R.facts('ch11-st1', F(
    terms=[('differential equation', 'an equation relating a function and one or more of its derivatives, e.g. dy/dx = ky'),
           ('first-order differential equation', 'a differential equation in which the highest derivative that appears is the first derivative dy/dx'),
           ('general solution', 'the family of all solutions of a differential equation, containing an arbitrary constant'),
           ('particular solution', 'the single solution of a differential equation that satisfies a given initial condition'),
           ('initial condition', 'a known value of the dependent variable at a given value of the independent variable, used to fix the arbitrary constant'),
           ("Newton's law of cooling", 'the rate of change of temperature of a body is proportional to the difference between its temperature and the surrounding temperature: dT/dt = −k(T − Tₐ)'),
           ('logistic model', 'dP/dt = kP(1 − P/L): growth proportional to the population and to the fraction of capacity remaining, levelling off at the carrying capacity L')],
    facts=[('"The rate of increase of N is proportional to N" is written as', 'dN/dt = kN, k > 0', ['N = kt', 'dN/dt = k', 'dN/dt = k/N'], 'Proportional to N means a constant multiple of N.'),
           ('"The rate of decrease of mass m is proportional to the square of m" is written as', 'dm/dt = −km², k > 0', ['dm/dt = km²', 'dm/dt = −2km', 'm = −kt²'], 'A decrease gives the negative sign.'),
           ('In dT/dt = −k(T − 20), the constant 20 represents', 'the temperature of the surroundings', ['the initial temperature', 'the rate of cooling', 'the time taken to cool'], 'T → 20 as t → ∞.'),
           ('In the logistic equation dP/dt = 0.3P(1 − P/500), the carrying capacity is', '500', ['0.3', '150', '1500'], 'dP/dt = 0 when P = 500.'),
           ('The order of the differential equation dy/dx + 3y = x² is', '1', ['2', '3', '0'], 'The highest derivative is dy/dx.')],
    why=[('Explain why the general solution of a first-order differential equation contains one arbitrary constant.', 'Solving requires one integration, which introduces one constant; one initial condition is then needed to determine it.'),
         ('Explain why the model dP/dt = kP predicts unlimited growth and how the logistic model corrects this.', 'With k > 0, dP/dt grows as P grows, so P increases exponentially without bound; the factor (1 − P/L) makes dP/dt → 0 as P → L, so the population levels off at the carrying capacity.'),
         ("Explain why, under Newton's law of cooling, a cup of coffee cools quickly at first and then more slowly.", 'The rate of cooling is proportional to the temperature difference with the room; as the coffee cools the difference shrinks, so the rate decreases.'),
         ('Explain how to check that a given function is a solution of a differential equation.', 'Differentiate the function, substitute it and its derivative into the equation, and show that both sides are identical for all x (and that any initial condition holds).')],
    contrast=[('a general solution', 'a particular solution', 'A general solution contains an arbitrary constant and represents a family of curves; a particular solution has the constant fixed by an initial condition and is a single curve.'),
              ('exponential growth dP/dt = kP', 'logistic growth dP/dt = kP(1 − P/L)', 'Exponential growth has a rate proportional to P and grows without bound; logistic growth slows as P approaches L and has a horizontal asymptote at the carrying capacity.')],
    misc=[('"The rate of decay of a radioactive substance is proportional to its mass" means dm/dt = km with k > 0.', 'The mass is decreasing, so dm/dt = −km with k > 0.'),
          ('A solution of dy/dx = 2y is y = 2x.', 'Substituting gives 2 = 4x, which is not true for all x; the solutions are y = Ae^(2x).'),
          ('In dT/dt = −k(T − 18), k must be negative because the object is cooling.', 'k > 0; the negative sign already makes dT/dt < 0 when T > 18.')],
))


def _de_context(rng):
    """(stem, DE text, k value (float), k formula text, follow-up question, follow-up answer)."""
    kind = rng.choice(['growth', 'decay', 'cool', 'tank', 'drug', 'rumour', 'learn'])
    if kind == 'growth':
        P0 = rng.choice([200, 250, 400, 500, 800, 1200]); r = rng.choice([12, 15, 18, 24, 30, 40])
        P1 = P0 * rng.choice([2, 3])
        k = r / P0
        return (f'A population of bacteria, P, grows at a rate proportional to its size. When P = {P0}, the population is increasing at {r} bacteria per hour.',
                'dP/dt = kP', k, f'{r} = k × {P0}', f'Find the rate of increase when P = {P1}.', f'{s3(k * P1)} bacteria per hour')
    if kind == 'decay':
        m0 = rng.choice([40, 50, 80, 120, 160]); r = rng.choice([2, 3, 4, 5, 6])
        m1 = m0 // 2
        k = r / m0
        return (f'A radioactive sample of mass m grams decays at a rate proportional to its mass. When m = {m0}, the mass is decreasing at {r} grams per day.',
                'dm/dt = −km', k, f'−{r} = −k × {m0}', f'Find the rate of decrease when m = {m1}.', f'{s3(k * m1)} grams per day')
    if kind == 'cool':
        T0 = rng.choice([85, 90, 95, 100, 80]); Ta = rng.choice([15, 18, 20, 22, 25]); r = rng.choice([3, 4, 5, 6, 8])
        T1 = rng.choice([40, 50, 60])
        k = r / (T0 - Ta)
        return (f"A cup of tea at {T0} °C is placed in a room at {Ta} °C. It cools according to Newton's law of cooling, and initially its temperature is falling at {r} °C per minute.",
                f'dT/dt = −k(T − {Ta})', k, f'−{r} = −k({T0} − {Ta})', f'Find the rate of cooling when T = {T1} °C.', f'{s3(k * (T1 - Ta))} °C per minute')
    if kind == 'tank':
        H = rng.choice([64, 81, 100, 121, 144]); r = rng.choice([2, 3, 4, 5])
        H1 = rng.choice([16, 25, 36])
        k = r / math.sqrt(H)
        return (f'Water drains from a tank so that the depth h cm decreases at a rate proportional to √h. When h = {H}, the depth is decreasing at {r} cm per minute.',
                'dh/dt = −k√h', k, f'−{r} = −k√{H}', f'Find the rate at which the depth is decreasing when h = {H1}.', f'{s3(k * math.sqrt(H1))} cm per minute')
    if kind == 'drug':
        a = rng.choice([10, 12, 15, 20]); A = rng.choice([20, 25, 40, 50]); r = rng.choice([4, 5, 6, 8])
        k = (a - r) / A
        A1 = rng.choice([60, 80, 100])
        return (f'A drug is fed into a patient at a constant rate of {a} mg per hour and is removed by the body at a rate proportional to the amount A mg present. When A = {A}, the amount is increasing at {r} mg per hour.',
                f'dA/dt = {a} − kA', k, f'{r} = {a} − k × {A}', f'Find the long-term amount of drug in the body.', f'{s3(a / k)} mg', 'in the long term dA/dt = 0')
    if kind == 'rumour':
        N = rng.choice([400, 500, 600, 800, 1000]); n = rng.choice([20, 40, 50, 100]); r = rng.choice([6, 8, 9, 12, 15])
        k = r / (n * (N - n))
        return (f'A rumour spreads through a school of {N} students. The rate at which the number n who have heard it increases is proportional to the product of n and the number who have not heard it. When n = {n}, it is spreading at {r} students per hour.',
                f'dn/dt = kn({N} − n)', k, f'{r} = k × {n} × {N - n}', 'Find the value of n at which the rumour spreads fastest.', f'{N // 2}', f'dn/dt is a quadratic in n with roots 0 and {N}, so it is greatest at the midpoint')
    M = rng.choice([50, 60, 80, 100]); L1 = rng.choice([10, 20, 30]); r = rng.choice([2, 3, 4, 5])
    k = r / (M - L1)
    return (f'When learning vocabulary, the rate at which the number of words W known increases is proportional to the number still to be learned from a list of {M}. When W = {L1}, words are being learned at {r} per day.',
            f'dW/dt = k({M} − W)', k, f'{r} = k({M} − {L1})', f'Find the rate of learning when W = {M - 5}.', f'{s3(k * 5)} words per day')


@R.add('ch11-st1', 'C3', (2, 5), 'short', style='p2')
def de_setup_short(rng, slot):
    stem, de, k, eq, fq, fa, *fk = _de_context(rng)
    fk = fk[0] if fk else 'substitute into the DE'
    if slot.d <= 2:
        return mk(f'{stem}\n(a) Write down a differential equation for this model. (b) Find the value of the constant k.', f'(a) {de} (b) k = {s3(k)}',
                  f'(a) {de} (A1). (b) {eq} (M1); k = {s3(k)} (A1).', 3)
    return mk(f'{stem}\n(a) Write down a differential equation for this model. (b) Find the value of the constant k. (c) {fq}', f'(a) {de} (b) k = {s3(k)} (c) {fa}',
              f'(a) {de} (A1). (b) {eq} (M1); k = {s3(k)} (A1). (c) {fk} (M1); {fa} (A1).', 5)


@R.add('ch11-st1', 'C3', (2, 5), 'short', style='p1')
def de_verify(rng, slot):
    kind = rng.choice(['lin', 'xy', 'pow', 'sq', 'circ'])
    if kind == 'lin':
        a, b = rng.randint(1, 5), nz(rng, -8, 8)
        y0 = rng.randint(-3, 6)
        C = sp.Symbol('C')
        gen = sp.Rational(b, a) + C * sp.exp(-a * x)
        de = f'dy/dx + {a if a > 1 else ""}y = {b}'
        part = gen.subs(C, y0 - sp.Rational(b, a))
        ic = f'y = {y0} when x = 0'
        fam = f'y = {P(sp.Rational(b, a))} + Ce^(−{a if a > 1 else ""}x)'
    elif kind == 'xy':
        a = rng.choice([1, 2, 3, 4, 6]); y0 = rng.randint(1, 5)
        part = y0 * sp.exp(a * x ** 2 / 2)
        de = f'dy/dx = {a if a > 1 else ""}xy'
        ic = f'y = {y0} when x = 0'
        fam = f'y = Ce^({P(sp.Rational(a, 2))}x²)' if a != 2 else 'y = Ce^(x²)'
    elif kind == 'pow':
        n = rng.choice([2, 3, -1, -2]); x0 = rng.choice([1, 2]); y0 = rng.randint(1, 8)
        part = sp.Rational(y0, 1) / sp.Integer(x0) ** n * x ** n
        de = f'x dy/dx = {n if n != 1 else ""}y'.replace('= −1y', '= −y')
        ic = f'y = {y0} when x = {x0}'
        fam = f'y = Cx{str(n).translate(_SUP)}'
    elif kind == 'sq':
        y0 = rng.choice([1, 2, 3, sp.Rational(1, 2), -1])
        part = 1 / (1 / sp.nsimplify(y0) - x)
        de = 'dy/dx = y²'
        ic = f'y = {P(y0)} when x = 0'
        fam = 'y = 1/(C − x)'
    else:
        a, b = rng.choice([(3, 4), (5, 12), (6, 8), (1, 1), (2, 3), (1, 2)])
        de = 'y dy/dx = −x'
        ic = f'y = {b} when x = {a}'
        fam = 'x² + y² = C'
        return mk(f'Show that the curves {fam} satisfy the differential equation {de}, and find the particular solution for which {ic}.', f'x² + y² = {a * a + b * b}',
                  f'Implicit differentiation: 2x + 2y dy/dx = 0 (M1) so y dy/dx = −x (A1) AG; substitute ({a}, {b}): C = {a * a + b * b} (M1 A1).', 4)
    rhs = {'lin': b - a * y if kind == 'lin' else None, 'xy': a * x * y if kind == 'xy' else None, 'pow': n * y / x if kind == 'pow' else None, 'sq': y ** 2}[kind]
    assert de_ok(part, rhs)
    return mk(f'Show that y = {fam[4:]} is a solution of the differential equation {de} for any constant C, and find the particular solution for which {ic}.', f'y = {P(sp.simplify(part)) if kind != "lin" else P(part)}',
              f'Differentiate (M1); substitute y and dy/dx into the equation (M1); both sides agree for all x (A1) AG; use the initial condition to find C (M1); y = {P(part)} (A1).', 5)


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def de_interpret(rng, slot):
    kind = rng.choice(['logistic', 'cool', 'drug'])
    if kind == 'logistic':
        k = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.15]); L = rng.choice([200, 400, 500, 800, 1000, 1500])
        return mk(f'A population satisfies dP/dt = {k}P(1 − P/{L}). Explain why the population grows fastest when P = {L // 2}, and find this maximum rate of growth.', f'{s3(k * L / 4)} per unit time',
                  f'dP/dt = {k}P − ({k}/{L})P² is a quadratic in P with roots 0 and {L}, so its maximum is at the midpoint P = {L // 2} (R1); max rate = {k} × {L // 2} × ½ (M1) = {s3(k * L / 4)} (A1).', 3, 'explain')
    if kind == 'cool':
        k = rng.choice([0.05, 0.08, 0.1, 0.12, 0.04]); Ta = rng.choice([16, 18, 20, 22]); T1 = rng.choice([60, 70, 80, 90])
        return mk(f'The temperature T °C of an object satisfies dT/dt = −{k}(T − {Ta}). Explain what happens to T in the long term, and find the rate of change of T when T = {T1}.', f'T → {Ta}; rate = −{s3(k * (T1 - Ta))} °C per unit time',
                  f'dT/dt < 0 while T > {Ta} and dT/dt → 0 as T → {Ta}, so T decreases towards {Ta} (R1 R1); dT/dt = −{k}({T1} − {Ta}) = −{s3(k * (T1 - Ta))} (A1).', 3, 'explain')
    a = rng.choice([5, 8, 10, 12, 20]); k = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5])
    return mk(f'The amount A of a substance in a tank satisfies dA/dt = {a} − {k}A. Explain the meaning of each term and find the equilibrium amount.', f'A = {s3(a / k)}',
              f'{a} is the constant rate of input; {k}A is a removal rate proportional to the amount present (R1 R1); equilibrium when dA/dt = 0: A = {a}/{k} = {s3(a / k)} (A1).', 3, 'explain')


@R.add('ch11-st1', 'C1', (1, 3), 'mcq')
def de_form_mcq(rng, slot):
    v = rng.choice(['P', 'N', 'm', 'V', 'h', 'A'])
    M = rng.choice([50, 100, 200, 500])
    forms = [(f'proportional to {v}', f'd{v}/dt = k{v}'), (f'inversely proportional to {v}', f'd{v}/dt = k/{v}'),
             (f'proportional to the square root of {v}', f'd{v}/dt = k√{v}'), (f'proportional to the square of {v}', f'd{v}/dt = k{v}²'),
             (f'proportional to the product of {v} and ({M} − {v})', f'd{v}/dt = k{v}({M} − {v})'), (f'proportional to the difference between {M} and {v}', f'd{v}/dt = k({M} − {v})')]
    i = rng.randrange(len(forms))
    words, ans = forms[i]
    wr = [f for j, (_, f) in enumerate(forms) if j != i]
    rng.shuffle(wr)
    noun = rng.choice(['The rate of change of', 'The rate of increase of'])
    return mcq(rng, f'{noun} {v} with respect to time t is {words}. Which differential equation models this?', ans, wr[:3], f'"{words}" translates to {ans} for a constant k.')


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step', style='ext')
def cooling_parts(rng, slot):
    T0 = rng.choice([80, 85, 90, 95, 100]); Ta = rng.choice([15, 18, 20, 22, 25])
    t1 = rng.choice([5, 10, 4, 8]); T1 = rng.choice([v for v in (50, 55, 60, 65, 70) if v < T0 - 10])
    k = math.log((T0 - Ta) / (T1 - Ta)) / t1
    t2 = rng.choice([15, 20, 30]); T2 = Ta + (T0 - Ta) * math.exp(-k * t2)
    T3 = rng.choice([v for v in (30, 35, 40) if v > Ta + 4])
    t3 = math.log((T0 - Ta) / (T3 - Ta)) / k
    obj = rng.choice(['a bowl of soup', 'a metal rod', 'a cup of coffee', 'a loaf of bread'])
    parts = [(f"Write down a differential equation satisfied by T, using Newton's law of cooling.", f'dT/dt = −k(T − {Ta})', 'A1', 1, True),
             (f'Solve the differential equation to show that T = {Ta} + {T0 - Ta}e^(−kt).', 'shown', f'separate: ∫ 1/(T − {Ta}) dT = −∫k dt (M1); ln(T − {Ta}) = −kt + c (A1); use T = {T0} at t = 0 (M1) AG', 3, True),
             (f'Find the value of k.', f'k = {s3(k)}', f'{T1} = {Ta} + {T0 - Ta}e^(−{t1}k) (M1); k = (1/{t1})ln({T0 - Ta}/{T1 - Ta}) = {s3(k)} (A1)', 2, True),
             (f'Find the temperature after {t2} minutes.', f'{s3(T2)} °C', 'substitute (M1) A1', 2, False),
             (f'Find the time taken for the temperature to fall to {T3} °C.', f'{s3(t3)} minutes', 'set up equation (M1); solve with logarithms or GDC (A1)', 2, True),
             ('State what happens to T as t → ∞ and comment on the validity of the model.', f'T → {Ta} °C; it never reaches room temperature exactly, but in practice it does', 'A1 R1', 2, False)]
    return build_parts(rng, [f'{obj[0].upper() + obj[1:]} at {T0} °C is left in a room at a constant {Ta} °C. After {t1} minutes its temperature is {T1} °C. Let T °C be its temperature t minutes after it was left.',
                             f'The temperature T °C of {obj}, t minutes after being placed in a room at {Ta} °C, is modelled by Newton\'s law of cooling. Initially T = {T0}, and when t = {t1}, T = {T1}.'], parts, 4)


@R.add('ch11-st1', 'C4', (4, 5), 'multi_step', style='p3')
def logistic_parts(rng, slot):
    L = rng.choice([200, 500, 1000, 1200, 2000]); P0 = rng.choice([L // 10, L // 20, L // 5, L // 4]); k = rng.choice([0.2, 0.3, 0.4, 0.5, 0.25])
    A = sp.Rational(L - P0, P0)
    t1 = rng.choice([5, 10, 8])
    Pt = L / (1 + float(A) * math.exp(-k * t1))
    th = math.log(float(A)) / k
    parts = [(f'Show that P = {L}/(1 + Ae^(−{k}t)) satisfies the differential equation for any constant A.', 'shown', 'differentiate (M1); express dP/dt in terms of P (M1); simplify to the DE (A1) AG', 3, True),
             (f'Given that P = {P0} when t = 0, find A.', P(A), f'{P0} = {L}/(1 + A) (M1) A1', 2, True),
             (f'Find the population when t = {t1}.', s3(Pt), 'substitute (M1) A1', 2, True),
             (f'Find the time at which the population is growing most rapidly.', f't = {s3(th)}', f'max rate when P = {L // 2} (R1); solve {L // 2} = {L}/(1 + {P(A)}e^(−{k}t)) (M1); t = ln({P(A)})/{k} = {s3(th)} (A1)', 3, True),
             ('Find this maximum rate of growth.', s3(k * L / 4), f'{k} × {L // 2} × ½ (M1) A1', 2, False),
             ('Explain why the model is more realistic than exponential growth for a population in a limited habitat.', 'growth slows and P approaches the carrying capacity', f'P → {L} as t → ∞ (R1)', 1, False)]
    return build_parts(rng, [f'A population P of fish in a lake is modelled by dP/dt = {k}P(1 − P/{L}), where t is in years.',
                             f'This question explores the logistic model dP/dt = {k}P(1 − P/{L}) for a population P at time t years.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch11-st2', F(
    terms=[('separation of variables', 'a method for solving dy/dx = f(x)g(y) by writing ∫ 1/g(y) dy = ∫ f(x) dx and integrating both sides'),
           ('separable differential equation', 'a first-order equation that can be written in the form dy/dx = f(x)g(y)'),
           ('arbitrary constant', 'the single constant of integration in the general solution, fixed by an initial condition')],
    facts=[('Separating the variables in dy/dx = xy gives', '∫ (1/y) dy = ∫ x dx', ['∫ y dy = ∫ x dx', '∫ x y dx = y', '∫ (1/x) dx = ∫ y dy'], 'Divide by y, then integrate.'),
           ('The general solution of dy/dx = ky is', 'y = Ae^(kx)', ['y = e^(kx) + C', 'y = kx + C', 'y = Ce^x + k'], 'ln|y| = kx + c gives y = ±e^c e^(kx).'),
           ('Which equation is NOT separable?', 'dy/dx = x + y', ['dy/dx = xy', 'dy/dx = eˣ⁺ʸ', 'dy/dx = x/y'], 'x + y cannot be written as f(x)g(y).'),
           ('Solving dy/dx = y/x gives the general solution', 'y = Ax', ['y = x + C', 'y = Ax²', 'y = ln x + C'], 'ln|y| = ln|x| + c.')],
    why=[('Explain why only one constant of integration is needed when both sides of a separated equation are integrated.', 'Constants from each side can be combined into a single constant on one side: ln|y| + c₁ = x² + c₂ is equivalent to ln|y| = x² + c.'),
         ('Explain why dividing by y when separating dy/dx = ky may lose a solution.', 'Dividing assumes y ≠ 0, but y = 0 is itself a solution of dy/dx = ky; it corresponds to A = 0 in y = Ae^(kx).'),
         ('Explain why the solution of dy/dx = ky is written as y = Ae^(kx) rather than y = e^(kx) + C.', 'Integrating gives ln|y| = kx + c, so |y| = e^(kx + c) = e^c e^(kx); the constant multiplies, it does not add, so y = Ae^(kx).')],
    misc=[('From ln y = 3x + c it follows that y = e^(3x) + c.', 'Exponentiating gives y = e^(3x + c) = Ae^(3x): the constant becomes a multiplying factor.'),
          ('dy/dx = x + y can be solved by separating the variables.', 'x + y is not a product f(x)g(y); this linear equation needs an integrating factor.'),
          ('To solve dy/dx = xy, integrate both sides with respect to x: y = (x²/2)y + C.', 'y cannot be treated as a constant; separate first: ∫ (1/y) dy = ∫ x dx, so ln|y| = x²/2 + c.')],
))


def _sep(rng):
    """(DE text, initial-condition text, particular solution sympy expr in x, key text, rhs, x0)."""
    kind = rng.choice(['xny', 'xovery', 'ysq', 'exp', 'arctan', 'cos', 'pow', 'shift', 'atanx'])
    if kind == 'xny':
        a = rng.choice([1, 2, 3, 4, 6]); n = rng.choice([1, 2]); y0 = rng.randint(1, 6)
        rhs = a * x ** n * y
        sol = y0 * sp.exp(sp.Rational(a, n + 1) * x ** (n + 1))
        key = f'∫ (1/y) dy = ∫ {P(a * x ** n)} dx (M1); ln y = {P(sp.Rational(a, n + 1) * x ** (n + 1))} + c (A1 A1); y = {y0} at x = 0 gives c = ln {y0} (M1)'
        return P(rhs), f'y = {y0} when x = 0', sol, key, rhs, 0
    if kind == 'xovery':
        a = rng.choice([1, 2, 3, 4, 8]); y0 = rng.randint(1, 5)
        rhs = a * x / y
        sol = sp.sqrt(a * x ** 2 + y0 ** 2)
        key = f'∫ y dy = ∫ {P(a * x)} dx (M1); y²/2 = {P(sp.Rational(a, 2) * x ** 2)} + c (A1 A1); c = {P(sp.Rational(y0 * y0, 2))} (M1)'
        return f'{a if a > 1 else ""}x/y', f'y = {y0} when x = 0 (y > 0)', sol, key, rhs, 0
    if kind == 'ysq':
        k = rng.choice([1, 2, 3]); y0 = rng.choice([1, 2, sp.Rational(1, 2), -1, 3])
        rhs = k * y ** 2
        sol = sp.simplify(1 / (1 / sp.nsimplify(y0) - k * x))
        key = f'∫ y⁻² dy = ∫ {k} dx (M1); −1/y = {k if k > 1 else ""}x + c (A1 A1); c = {P(-1 / sp.nsimplify(y0))} (M1)'
        return P(rhs), f'y = {P(y0)} when x = 0', sol, key, rhs, 0
    if kind == 'exp':
        a = rng.choice([1, 2, 3]); b = rng.choice([1, 2, 0])
        rhs = sp.exp(a * x - y)
        sol = sp.log(sp.exp(a * x) / a + sp.exp(b) - sp.Rational(1, a))
        if b == 0 and a == 1:
            return None
        key = f'∫ e^y dy = ∫ {P(sp.exp(a * x))} dx (M1); e^y = {P(sp.exp(a * x) / a)} + c (A1 A1); c = {P(sp.exp(b) - sp.Rational(1, a))} (M1)'
        return f'e^({P(a * x - y)})', f'y = {b} when x = 0', sol, key, rhs, 0
    if kind == 'arctan':
        a = rng.choice([1, 2, 4]); y0, ang = rng.choice([(0, 0), (1, pi / 4), (r3, pi / 3)])
        rhs = a * x * (1 + y ** 2)
        sol = sp.tan(sp.Rational(a, 2) * x ** 2 + ang)
        key = f'∫ 1/(1 + y²) dy = ∫ {P(a * x)} dx (M1); arctan y = {P(sp.Rational(a, 2) * x ** 2)} + c (A1 A1); c = arctan {P(y0)} = {P(ang)} (M1)'
        return f'{P(a * x)}(1 + y²)', f'y = {P(y0)} when x = 0', sol, key, rhs, 0
    if kind == 'cos':
        a = rng.choice([1, 2, 3]); y0 = rng.randint(1, 5)
        rhs = a * y * sp.cos(x)
        sol = y0 * sp.exp(a * sp.sin(x))
        key = f'∫ (1/y) dy = ∫ {a if a > 1 else ""}cos x dx (M1); ln y = {a if a > 1 else ""}sin x + c (A1 A1); c = ln {y0} (M1)'
        return f'{a if a > 1 else ""}y cos x', f'y = {y0} when x = 0', sol, key, rhs, 0
    if kind == 'pow':
        k = rng.choice([2, 3, -1, -2, sp.Rational(1, 2)]); y0 = rng.randint(1, 6)
        rhs = k * y / x
        sol = y0 * x ** k
        key = f'∫ (1/y) dy = ∫ {P(k)}/x dx (M1); ln y = {P(k)} ln x + c (A1 A1); c = ln {y0} (M1)'
        return f'{P(k)}y/x'.replace('1/2y/x', 'y/(2x)'), f'y = {y0} when x = 1 (x > 0)', sol, key, rhs, 1
    if kind == 'shift':
        a = rng.choice([1, 2, 3, -1, -2]); c_ = nz(rng, -5, 5); y0 = rng.randint(-2, 6)
        if y0 + c_ == 0:
            return None
        rhs = a * (y + c_)
        sol = -c_ + (y0 + c_) * sp.exp(a * x)
        key = f'∫ 1/(y {"+" if c_ > 0 else "−"} {abs(c_)}) dy = ∫ {a} dx (M1); ln|y {"+" if c_ > 0 else "−"} {abs(c_)}| = {P(a * x)} + c (A1 A1); use y({0}) = {y0} (M1)'
        return P(rhs), f'y = {y0} when x = 0', sol, key, rhs, 0
    a = rng.choice([1, 2, 3, 4]); y0 = rng.randint(1, 5)
    rhs = a * y / (1 + x ** 2)
    sol = y0 * sp.exp(a * sp.atan(x))
    key = f'∫ (1/y) dy = ∫ {a}/(1 + x²) dx (M1); ln y = {a if a > 1 else ""}arctan x + c (A1 A1); c = ln {y0} (M1)'
    return f'{a if a > 1 else ""}y/(1 + x²)', f'y = {y0} when x = 0', sol, key, rhs, 0


@R.add('ch11-st2', 'C3', (2, 5), 'short', style='p1')
def sep_particular(rng, slot):
    r_ = _sep(rng)
    if not r_:
        return None
    de, ic, sol, key, rhs, x0 = r_
    if not de_ok(sol, rhs):
        return None
    return mk(f'Solve the differential equation dy/dx = {de}, given that {ic}. Give your answer in the form y = f(x).', f'y = {P(sol)}',
              f'{key}; y = {P(sol)} (A1).', 6)


@R.add('ch11-st2', 'C3', (2, 5), 'short', style='p2')
def sep_value(rng, slot):
    r_ = _sep(rng)
    if not r_:
        return None
    de, ic, sol, key, rhs, x0 = r_
    x1 = rng.choice([0.5, 1.5, 2, 1.2, 0.8, 3])
    try:
        v = complex(sol.subs(x, x1).evalf())
    except Exception:
        return None
    if abs(v.imag) > 1e-9 or not math.isfinite(v.real) or abs(v.real) > 1e6:
        return None
    if sol.has(sp.tan) and x1 > 0.9:
        return None
    if r_[0].endswith('y²') and not sp.Abs(sp.denom(sp.together(sol)).subs(x, x1)).evalf() > 0.05:
        return None
    den = sp.denom(sp.together(sol))
    if den.has(x) and any(0 <= float(r) <= x1 for r in sp.solve(den, x) if r.is_real):
        return None
    return mk(f'Given that dy/dx = {de} and {ic}, find the value of y when x = {x1}.', s3(v.real),
              f'{key}; particular solution y = {P(sol)} (A1); y({x1}) = {s3(v.real)} (A1).', 6)


@R.add('ch11-st2', 'C3', (2, 5), 'short', style='p2')
def sep_growth(rng, slot):
    kind = rng.choice(['grow', 'decay'])
    noun = rng.choice(['a colony of bacteria', 'the number of users of an app', 'a population of rabbits', 'a culture of yeast cells'])
    if kind == 'grow':
        N0 = rng.choice([100, 200, 250, 500, 1000]); f = rng.choice([1.5, 2, 3, 1.8]); T = rng.choice([2, 3, 4, 5, 10])
        N1 = int(N0 * f)
        k = math.log(N1 / N0) / T
        tgt = N0 * rng.choice([5, 8, 10])
        tt = math.log(tgt / N0) / k
        return mk(f'The size N of {noun} satisfies dN/dt = kN, where t is in days. Initially N = {N0}, and after {T} days N = {N1}. (a) Find k. (b) Find the time when N first reaches {tgt}.',
                  f'(a) k = {s3(k)} (b) t = {s3(tt)} days', f'Separate: ln N = kt + c, N = {N0}e^(kt) (M1 A1); (a) {N1} = {N0}e^({T}k) (M1); k = {s3(k)} (A1). (b) {tgt} = {N0}e^(kt) (M1); t = {s3(tt)} (A1).', 6)
    m0 = rng.choice([50, 80, 100, 200]); h = rng.choice([3, 5, 8, 12, 20])
    k = math.log(2) / h
    t1 = rng.choice([10, 15, 25, 30])
    left = m0 * math.exp(-k * t1)
    return mk(f'A radioactive isotope decays according to dm/dt = −km, where m is the mass in grams and t is in years. Its half-life is {h} years and initially m = {m0}. (a) Find k. (b) Find the mass remaining after {t1} years.',
              f'(a) k = {s3(k)} (b) {s3(left)} g', f'Separate: m = {m0}e^(−kt) (M1 A1); (a) ½ = e^(−{h}k) (M1); k = ln 2/{h} = {s3(k)} (A1). (b) {m0}e^(−{s3(k)} × {t1}) (M1) = {s3(left)} (A1).', 6)


@R.add('ch11-st2', 'C2', (2, 4), 'explain')
def sep_error_explain(rng, slot):
    a = rng.choice([2, 3, 4, 5, -2, -3]); y0 = rng.randint(2, 9)
    kind = rng.choice(['addC', 'noC', 'treat'])
    sol = f'y = {y0}e^({P(a * x)})' if kind != 'treat' else f'y = {y0}e^({P(sp.Rational(a, 2) * x ** 2)})'
    if kind == 'addC':
        return mk(f'{who(rng)} solves dy/dx = {a}y with y = {y0} when x = 0 and writes: "ln y = {P(a * x)} + c, so y = e^({P(a * x)}) + c, and c = {y0 - 1}." Explain the error and give the correct solution.', sol,
                  f'e^({P(a * x)} + c) = e^c e^({P(a * x)}), so the constant multiplies rather than adds (R1); y = Ae^({P(a * x)}) (M1); A = {y0}: {sol} (A1).', 3, 'explain')
    if kind == 'noC':
        return mk(f'{who(rng)} solves dy/dx = {a}y with y = {y0} when x = 0 and writes: "ln y = {P(a * x)}, so y = e^({P(a * x)})." Explain why this cannot be correct and give the correct solution.', sol,
                  f'The constant of integration is missing, and y = e^({P(a * x)}) gives y = 1 at x = 0, not {y0} (R1); ln y = {P(a * x)} + c (M1); {sol} (A1).', 3, 'explain')
    return mk(f'{who(rng)} tries to solve dy/dx = {P(a * x)}y by integrating both sides with respect to x, writing y = {P(sp.Rational(a, 2) * x ** 2)}y + c. Explain the error and solve the equation given y = {y0} when x = 0.', sol,
              f'y depends on x, so ∫ {P(a * x)}y dx ≠ {P(sp.Rational(a, 2) * x ** 2)}y (R1); separate: ∫ (1/y) dy = ∫ {P(a * x)} dx (M1); {sol} (A1).', 3, 'explain')


@R.add('ch11-st2', 'C1', (1, 3), 'mcq')
def sep_mcq(rng, slot):
    fx = rng.choice(['x²', 'cos x', 'eˣ', '1/x', '(x + 1)', 'sin x', '√x'])
    gy = rng.choice([('y', '1/y'), ('y²', '1/y²'), ('sin y', '1/sin y'), ('eʸ', 'e⁻ʸ'), ('(1 + y²)', '1/(1 + y²)'), ('(y − 2)', '1/(y − 2)')])
    rhs = (f'{gy[0]} {fx}' if fx in ('cos x', 'sin x', '√x', 'eˣ') else f'{fx}{gy[0]}') if not fx.startswith('1/') else f'{gy[0]}/x'
    f_int = fx if not fx.startswith('1/') else '1/x'
    ans = f'∫ {gy[1]} dy = ∫ {f_int} dx'
    wr = [f'∫ {gy[0]} dy = ∫ {f_int} dx', f'∫ {gy[1]} dy = ∫ 1/{f_int} dx' if not f_int.startswith('1/') else f'∫ {gy[1]} dy = ∫ x dx', f'y = ∫ {rhs} dx']
    return mcq(rng, f'Separating the variables in dy/dx = {rhs} gives', ans, wr, 'Divide both sides by the function of y and integrate each side with respect to its own variable.')


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step', style='ext')
def tank_parts(rng, slot):
    H = rng.choice([36, 49, 64, 81, 100, 144]); rH = int(math.isqrt(H))
    H1 = rng.choice([v * v for v in range(2, rH - 1)])
    T1 = rng.choice([5, 10, 12, 20])
    kk = sp.Rational(2 * (rH - math.isqrt(H1)), T1)
    Te = sp.Rational(2 * rH, 1) / kk
    t2 = rng.choice([v for v in (2, 3, 4, 6, 8) if v < float(Te)])
    h2 = (rH - kk * t2 / 2) ** 2
    parts = [('Show that 2√h = −kt + c for some constant c.', 'shown', '∫ h^(−½) dh = −∫ k dt (M1); 2√h = −kt + c (A1) AG', 2, True),
             (f'Using h = {H} when t = 0, find c.', f'c = {2 * rH}', 'A1', 1, True),
             (f'Given that h = {H1} when t = {T1}, find the exact value of k.', f'k = {P(kk)}', f'2√{H1} = −{T1}k + {2 * rH} (M1) A1', 2, True),
             (f'Find the depth of water after {t2} minutes.', f'{P(h2)} cm', 'substitute and square (M1) A1', 2, False),
             ('Find the time taken for the tank to empty.', f'{P(Te)} minutes', f'h = 0: t = {2 * rH}/k (M1) A1', 2, True),
             ('Explain why the model predicts that the tank empties more slowly as the depth decreases.', 'dh/dt = −k√h becomes smaller in magnitude as h decreases', 'R1', 1, False)]
    return build_parts(rng, [f'A tank is being drained. The depth of water h cm at time t minutes satisfies dh/dt = −k√h, where k > 0. Initially the depth is {H} cm.',
                             f'Water leaks from a cylindrical container through a hole in its base. The depth h cm after t minutes is modelled by dh/dt = −k√h, with h = {H} when t = 0.'], parts, 4)


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step', style='ext')
def sep_general_parts(rng, slot):
    k = rng.choice([1, 2, 4, 6]); y0 = rng.choice([1, 2, sp.Rational(1, 2), 4])
    sol = sp.simplify(1 / (1 / sp.nsimplify(y0) - sp.Rational(k, 2) * x ** 2))
    assert de_ok(sol, k * x * y ** 2)
    xa = sp.sqrt(2 / (k * sp.nsimplify(y0)))
    x1 = sp.Rational(1, 2) * xa
    parts = [(f'Find the general solution of dy/dx = {P(k * x)}y².', f'y = 1/(c − {P(sp.Rational(k, 2) * x ** 2)})', f'∫ y⁻² dy = ∫ {P(k * x)} dx (M1); −1/y = {P(sp.Rational(k, 2) * x ** 2)} − c (A1 A1)', 3, True),
             (f'Find the particular solution for which y = {P(y0)} when x = 0.', f'y = {P(sol)}', 'substitute (M1) A1', 2, True),
             ('Find the values of x for which the particular solution is not defined.', f'x = ±{P(sp.radsimp(xa))}', 'denominator = 0 (M1) A1', 2, True),
             (f'Find the exact value of y when x = {P(sp.radsimp(x1))}.', P(sp.simplify(sol.subs(x, x1))), 'A1', 1, False),
             ('Describe the behaviour of the solution as x approaches the positive value found above from below.', 'y → +∞ (vertical asymptote)', 'R1', 1, False)]
    return build_parts(rng, [f'Consider the differential equation dy/dx = {P(k * x)}y².', f'This question is about solving dy/dx = {P(k * x)}y² by separating the variables.'], parts, 3)


@R.add('ch11-st2', 'C4', (4, 5), 'multi_step', style='p3')
def logistic_pf_parts(rng, slot):
    L = rng.choice([10, 20, 50, 100]); k = rng.choice([sp.Rational(1, 5), sp.Rational(1, 4), sp.Rational(2, 5), sp.Rational(1, 2), sp.Rational(1, 10)]) / L
    P0 = rng.choice([v for v in (1, 2, 4, 5, 10) if v < L / 2])
    A = sp.Rational(L - P0, P0)
    kL = k * L
    t1 = rng.choice([5, 10, 20])
    Pt = L / (1 + float(A) * math.exp(-float(kL) * t1))
    th = math.log(float(A)) / float(kL)
    p_ = sp.Symbol('P', positive=True)
    de = P(k * p_ * (L - p_))
    tt = sp.Symbol('t', positive=True)
    Atx = P(A) if A.is_Integer else f'({P(A)})'
    parts = [(f'Write 1/(P({L} − P)) in partial fractions.', f'(1/{L})(1/P + 1/({L} − P))', 'M1 A1', 2, True),
             (f'Hence show that ln(P/({L} − P)) = {P(kL * tt)} + c.', 'shown', f'separate (M1); integrate both fractions (A1 A1); multiply by {L} (M1) AG', 4, True),
             (f'Given that P = {P0} when t = 0, show that P = {L}/(1 + {Atx}e^({P(-kL * tt)})).', 'shown', f'c = {P(sp.log(sp.Rational(P0, L - P0)))} (A1); rearrange (M1) AG', 2, True),
             (f'Find P when t = {t1}.', s3(Pt), 'A1', 1, True),
             (f'Find the time at which P = {sp.Rational(L, 2)}.', f't = {s3(th)}', f'1 + {Atx}e^({P(-kL * tt)}) = 2 (M1) A1', 2, False),
             ('Generalise: for dP/dt = kP(L − P) with P(0) = P₀ < L/2, find the time at which the growth rate is greatest, in terms of k, L and P₀.', 't = (1/(kL)) ln((L − P₀)/P₀)', 'P = L/2 (R1); solve (M1) A1', 3, False)]
    return build_parts(rng, [f'The number of infected people P (in thousands) at time t days satisfies dP/dt = {de}.',
                             f'A model for the spread of a virus is dP/dt = {de}, where P thousand people are infected after t days.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch11-st3', F(
    terms=[('homogeneous differential equation', 'a first-order equation that can be written as dy/dx = f(y/x); it is solved with the substitution y = vx'),
           ('integrating factor', 'for dy/dx + P(x)y = Q(x), the function I(x) = e^(∫P(x) dx); multiplying by it turns the left side into d/dx(I y)'),
           ('linear first-order differential equation', 'an equation of the form dy/dx + P(x)y = Q(x), in which y and dy/dx appear only to the first power')],
    facts=[('The integrating factor for dy/dx + 3y = eˣ is', 'e^(3x)', ['e^(x)', '3x', 'e^(−3x)'], 'e^(∫3 dx) = e^(3x).'),
           ('The integrating factor for dy/dx + (2/x)y = x, x > 0, is', 'x²', ['e^(2x)', '2 ln x', '1/x²'], 'e^(2 ln x) = x².'),
           ('With y = vx, dy/dx equals', 'v + x dv/dx', ['dv/dx', 'x dv/dx', 'v dv/dx'], 'Product rule.'),
           ('Which equation is homogeneous?', 'dy/dx = (x² + y²)/(xy)', ['dy/dx = x + y²', 'dy/dx = xy + 1', 'dy/dx = eˣ + y'], 'Dividing by x² gives a function of y/x only.')],
    why=[('Explain why multiplying dy/dx + P(x)y = Q(x) by e^(∫P dx) allows it to be integrated directly.', 'With I = e^(∫P dx), dI/dx = P I, so I dy/dx + P I y = d/dx(I y) by the product rule; the equation becomes d/dx(Iy) = I Q, which can be integrated.'),
         ('Explain why the substitution y = vx turns a homogeneous equation into a separable one.', 'dy/dx = v + x dv/dx and f(y/x) = f(v), so x dv/dx = f(v) − v, where the variables v and x can be separated.'),
         ('Explain why the constant of integration must be included before dividing by the integrating factor.', 'Iy = ∫ IQ dx + C; dividing by I gives y = (∫ IQ dx)/I + C/I, so the constant term becomes C/I — adding C afterwards gives the wrong family of solutions.')],
    misc=[('The integrating factor for dy/dx − 2y = x is e^(2x).', 'P(x) = −2, so the integrating factor is e^(−2x).'),
          ('After multiplying by the integrating factor x³, the solution of d/dx(x³y) = x⁴ is y = x²/5 + C.', 'x³y = x⁵/5 + C, so y = x²/5 + C/x³: the constant must also be divided by x³.')],
))


@R.add('ch11-st3', 'C3', (2, 5), 'short', style='p1')
def if_solve(rng, slot):
    kind = rng.choice(['const_exp', 'kx', 'kx_neg', 'tan', 'twox', 'const_lin'])
    if kind == 'const_exp':
        a, b, c = rng.randint(1, 4), nz(rng, -6, 6), rng.choice([1, 2, -1, 3])
        if a + c == 0:
            return None
        Pp, Q, x0, y0 = sp.Integer(a), b * sp.exp(c * x), 0, rng.randint(-2, 4)
    elif kind == 'kx':
        k, m = rng.choice([1, 2, 3]), rng.choice([0, 1, 2])
        Pp, Q, x0, y0 = sp.Integer(k) / x, (m + k + 1) * x ** m, 1, rng.randint(0, 5)
    elif kind == 'kx_neg':
        k, m = rng.choice([1, 2, 3]), rng.choice([1, 2, 3])
        if m + 1 == k:
            return None
        Pp, Q, x0, y0 = -sp.Integer(k) / x, x ** m * (m + 1 - k), 1, rng.randint(0, 5)
    elif kind == 'tan':
        a = rng.randint(1, 4)
        Pp, Q, x0, y0 = sp.tan(x), a * sp.cos(x), 0, rng.randint(0, 4)
    elif kind == 'twox':
        a = rng.choice([1, 2, 3]); b = rng.choice([2, 4, 6])
        Pp, Q, x0, y0 = a * x, b * x, 0, rng.randint(0, 5)
    else:
        a, b = rng.randint(1, 3), rng.choice([2, 3, 4, 6])
        Pp, Q, x0, y0 = sp.Integer(a), b * x, 0, rng.randint(0, 4)
    I = sp.simplify(sp.exp(sp.integrate(Pp, x)))
    if kind == 'kx_neg':
        I = x ** (-sp.Integer(-Pp * x))
    if kind == 'kx':
        I = x ** sp.Integer(Pp * x)
    if kind == 'tan':
        I = 1 / sp.cos(x)
    C = sp.Symbol('C')
    gen = (sp.integrate(sp.simplify(I * Q), x) + C) / I
    Cv = sp.solve(sp.Eq(gen.subs(x, x0), y0), C)
    if not Cv:
        return None
    sol = sp.simplify(gen.subs(C, Cv[0]))
    if kind in ('const_exp', 'twox', 'const_lin'):
        sol = sp.expand(sol)
    if not de_ok(sol, Q - Pp * y):
        return None
    neg = float(Pp.subs(x, sp.Rational(1, 3))) < 0
    coef = P(-Pp if neg else Pp)
    coef = '' if coef == '1' else f'({coef})' if '/' in coef else coef
    lhs = f'dy/dx {"−" if neg else "+"} {coef}y'
    if kind == 'tan':
        lhs = 'dy/dx + y tan x'
    Itxt = P(I) if kind != 'tan' else 'sec x'
    return mk(f'Use an integrating factor to solve {lhs} = {P(Q)}{", x > 0" if kind in ("kx", "kx_neg") else ""}, given that y = {y0} when x = {x0}.', f'y = {P(sol)}',
              f'Integrating factor e^(∫{P(Pp)} dx) = {Itxt} (M1 A1); d/dx({Itxt} · y) = {P(sp.simplify(I * Q))} (M1); integrate, including + C (A1); use y({x0}) = {y0} (M1); y = {P(sol)} (A1).', 6)


@R.add('ch11-st3', 'C3', (3, 5), 'short', style='p1')
def homog_solve(rng, slot):
    kind = rng.choice(['lin', 'sq', 'recip', 'exp', 'sin'])
    if kind == 'lin':
        a = nz(rng, -4, 4); y0 = rng.randint(-3, 5)
        rhs = (a * x + y) / x
        de = f'({P(a * x + y)})/x'
        sol = x * (a * sp.log(x) + y0)
        key = f'v + x dv/dx = {a} + v (M1 A1); dv/dx = {a}/x (A1); v = {P(a * sp.log(x))} + c (A1); c = {y0} (M1)'
    elif kind == 'sq':
        k = rng.choice([1, 2, 3]); y0 = rng.randint(1, 4)
        rhs = (y ** 2 + k * x ** 2) / (x * y)
        de = f'({P(y ** 2 + k * x ** 2)})/(xy)'
        sol = x * sp.sqrt(2 * k * sp.log(x) + y0 ** 2)
        key = f'v + x dv/dx = v + {k if k > 1 else ""}/v'.replace(' /v', ' 1/v') + f' (M1 A1); ∫ v dv = ∫ {k}/x dx (A1); v²/2 = {k if k > 1 else ""} ln x + c (A1); c = {P(sp.Rational(y0 * y0, 2))} (M1)'
    elif kind == 'recip':
        y0 = rng.choice([1, 2, 3, -1, sp.Rational(1, 2)])
        rhs = y / x + y ** 2 / x ** 2
        de = '(xy + y²)/x²'
        sol = sp.simplify(x * y0 / (1 - y0 * sp.log(x)))
        key = f'v + x dv/dx = v + v² (M1 A1); ∫ v⁻² dv = ∫ 1/x dx (A1); −1/v = ln x + c (A1); c = {P(-1 / sp.nsimplify(y0))} (M1)'
    elif kind == 'exp':
        k = rng.choice([1, 2, 3]); y0 = rng.choice([0, 1, 2])
        rhs = y / x + k * sp.exp(-y / x)
        de = f'y/x + {k if k > 1 else ""}e^(−y/x)'
        sol = x * sp.log(k * sp.log(x) + sp.exp(y0))
        key = f'v + x dv/dx = v + {k if k > 1 else ""}e^(−v) (M1 A1); ∫ e^v dv = ∫ {k}/x dx (A1); e^v = {k if k > 1 else ""} ln x + c (A1); c = {P(sp.exp(y0))} (M1)'
    else:
        ang, sv = rng.choice([(pi / 6, sp.Rational(1, 2)), (pi / 4, r2 / 2), (pi / 3, r3 / 2)])
        rhs = y / x + sp.tan(y / x)
        de = 'y/x + tan(y/x)'
        sol = x * sp.asin(sv * x)
        key = f'v + x dv/dx = v + tan v (M1 A1); ∫ cot v dv = ∫ 1/x dx (A1); ln|sin v| = ln x + c, sin v = Ax (A1); A = sin({P(ang)}) = {P(sv)} (M1)'
        y0 = ang
    if not de_ok(sol, rhs):
        return None
    st_ = P(sol).replace('ln(x)', 'ln x')
    st_ = re.sub(r'(\d)ln x', r'\1 ln x', st_)
    return mk(f'Use the substitution y = vx to solve the differential equation dy/dx = {de}, x > 0, given that y = {P(y0)} when x = 1.', f'y = {st_}',
              f'{key}; y = {st_} (A1).'.replace('=  ', '= ').replace('ln(x)', 'ln x'), 6)


@R.add('ch11-st3', 'C1', (1, 3), 'mcq')
def if_mcq(rng, slot):
    k = rng.choice([2, 3, 4, 5])
    opts = [(f'{k}', f'e^({k}x)'), (f'{k}/x', f'x{str(k).translate(_SUP)}'), (f'−{k}/x', f'x⁻{str(k).translate(_SUP)}'), (f'{2 * k}x', f'e^({k}x²)'),
            ('tan x', 'sec x'), ('cot x', 'sin x'), (f'−{k}', f'e^(−{k}x)'), ('1/x', 'x')]
    i = rng.randrange(len(opts))
    Pp, I = opts[i]
    wr = [o[1] for j, o in enumerate(opts) if j != i]
    rng.shuffle(wr)
    Pt = f'{Pp}y' if '/' not in Pp and not Pp[-1].isalpha() else (f'({Pp})y' if '/' in Pp else f'y {Pp}')
    sgn = '+'
    if Pt.startswith('−') or Pt.startswith('(−'):
        sgn, Pt = '−', Pt.replace('−', '', 1)
    return mcq(rng, f'An integrating factor for dy/dx {sgn} {Pt} = Q(x) is', I, wr[:3], f'I = e^(∫P dx) with P(x) = {Pp}.')


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def if_explain(rng, slot):
    kind = rng.choice(['if', 'homog'])
    if kind == 'if':
        k = rng.choice([1, 2, 3, 4]); m = rng.choice([1, 2, 3])
        I = f'x{str(k).translate(_SUP)}' if k > 1 else 'x'
        return mk(f'For the equation dy/dx + {"(" + str(k) + "/x)" if k > 1 else "(1/x)"}y = x{str(m).translate(_SUP) if m > 1 else ""}, x > 0, explain why multiplying by {I} allows the equation to be integrated, and write down the resulting equation.',
                  f'd/dx({I}y) = x{str(m + k).translate(_SUP)}',
                  (f'{I} = e^(∫{k}/x dx) = e^({k} ln x) (R1); {I} dy/dx + {k}x{str(k - 1).translate(_SUP) if k > 2 else ""}y is the derivative of {I}y by the product rule (R1); d/dx({I}y) = x{str(m + k).translate(_SUP)} (A1).' if k > 1 else
                   f'x = e^(∫1/x dx) = e^(ln x) (R1); x dy/dx + y is the derivative of xy by the product rule (R1); d/dx(xy) = x{str(m + 1).translate(_SUP)} (A1).'), 3, 'explain')
    a, b = rng.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3)])
    return mk(f'Explain why the differential equation dy/dx = ({a if a > 1 else ""}x² + {b if b > 1 else ""}y²)/(xy) is homogeneous, and show that y = vx reduces it to x dv/dx = {P(sp.Rational(a, 1))}/v{" − " + str(1 - b) + "v" if b != 1 else ""}.'.replace('− -', '+ ').replace('+ -', '− '),
              f'x dv/dx = {a}/v + {b - 1}v' if b != 1 else f'x dv/dx = {a}/v',
              f'Dividing numerator and denominator by x² gives ({a} + {b}v²)/v, a function of v = y/x only (R1); dy/dx = v + x dv/dx (M1); x dv/dx = {a}/v + {b}v − v (A1).', 3, 'explain')


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step', style='ext')
def mixing_parts(rng, slot):
    V = rng.choice([100, 200, 400, 500]); r = rng.choice([2, 4, 5, 10]); c = rng.choice([sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(1, 4)])
    S0 = rng.choice([0, 5, 10, 20])
    Sinf = V * c
    if S0 == Sinf:
        return None
    a = sp.Rational(r, V)
    t1 = rng.choice([10, 20, 30, 60])
    St = float(Sinf + (S0 - Sinf) * sp.exp(-a * t1))
    tt = sp.Symbol('t', positive=True)
    half = (S0 + Sinf) / 2
    th = float(sp.log(2) / a)
    S_ = sp.Symbol('S')
    parts = [(f'Show that dS/dt + {P(a * S_)} = {P(r * c)}.', 'shown', f'rate in = {r} × {P(c)} = {P(r * c)} kg/min (A1); rate out = {r} × S/{V} (A1) AG', 2, True),
             ('Find an integrating factor for this differential equation.', f'e^({P(a * tt)})', 'M1 A1', 2, True),
             (f'Hence show that S = {P(Sinf)} {"+" if S0 > Sinf else "−"} {P(abs(S0 - Sinf))}e^({P(-a * tt)}).', 'shown', f'd/dt(Se^({P(a * tt)})) = {P(r * c)}e^({P(a * tt)}) (M1); integrate (A1); use S(0) = {S0} (M1) AG', 3, True),
             (f'Find the amount of salt in the tank after {t1} minutes.', f'{s3(St)} kg', 'A1', 1, True),
             ('State the long-term amount of salt in the tank and explain it.', f'{P(Sinf)} kg', f'e^(−{P(a)}t) → 0 (R1); the tank tends to the inflow concentration {P(c)} × {V} (A1)', 2, False),
             (f'Find the time taken for the amount of salt to reach {P(half)} kg.', f'{s3(th)} minutes', 'set up (M1) A1', 2, False)]
    return build_parts(rng, [f'A tank contains {V} litres of water in which {S0} kg of salt is dissolved. Brine containing {P(c)} kg of salt per litre flows in at {r} litres per minute and the well-mixed solution flows out at the same rate. Let S kg be the amount of salt after t minutes.',
                             f'Brine with concentration {P(c)} kg/litre enters a {V}-litre tank at {r} litres/min; the mixture leaves at {r} litres/min. Initially the tank holds {S0} kg of salt. S kg of salt is present at time t minutes.'], parts, 4)


@R.add('ch11-st3', 'C4', (4, 5), 'multi_step', style='p3')
def homog_parts(rng, slot):
    k = rng.choice([1, 2, 3, 4]); y0 = rng.choice([1, 2, 3])
    sol = x * sp.sqrt(2 * k * sp.log(x) + y0 ** 2)
    assert de_ok(sol, (y ** 2 + k * x ** 2) / (x * y))
    ye = sp.simplify(sol.subs(x, sp.E))
    xmin = sp.exp(-sp.Rational(y0 * y0, 2 * k))
    parts = [(f'Show that the equation dy/dx = (y² + {k if k > 1 else ""}x²)/(xy) is homogeneous.', 'shown', 'divide by x²: (v² + k)/v (R1) AG', 1, True),
             ('Use the substitution y = vx to show that v dv/dx = ' + (f'{k}/x.' if k > 1 else '1/x.'), 'shown', 'dy/dx = v + x dv/dx (M1); simplify (A1) AG', 2, True),
             (f'Hence find y in terms of x, given that y = {y0} when x = 1 and y > 0.', f'y = {P(sol)}', f'v² = {2 * k} ln x + c (A1); c = {y0 * y0} (M1); y = x√(…) (A1)', 3, True),
             ('Find the exact value of y when x = e.', P(ye), 'A1', 1, True),
             ('Find the smallest value of x for which the solution is defined.', f'x = {P(xmin)}', f'{2 * k} ln x + {y0 * y0} ≥ 0 (M1) A1', 2, False),
             ('Generalise your method to dy/dx = (y² + ax²)/(xy) with y(1) = b > 0, giving y in terms of a, b and x.', 'y = x√(2a ln x + b²)', 'M1 A1', 2, False)]
    return build_parts(rng, ['This question investigates a homogeneous differential equation.', f'Consider dy/dx = (y² + {k if k > 1 else ""}x²)/(xy), x > 0.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch11-st4', F(
    terms=[("Euler's method", 'a numerical method for dy/dx = f(x, y): yₙ₊₁ = yₙ + h f(xₙ, yₙ), xₙ₊₁ = xₙ + h, following the tangent for a step h'),
           ('slope field', 'a diagram of short line segments whose gradients equal dy/dx = f(x, y) at grid points, showing the shape of solution curves'),
           ('isocline', 'a curve on which f(x, y) is constant, so all slope-field segments on it are parallel; the isocline f(x, y) = 0 joins points with horizontal segments'),
           ('step length', 'the increment h in x used in each iteration of a numerical method')],
    facts=[("Euler's method for dy/dx = f(x, y) uses", 'yₙ₊₁ = yₙ + h f(xₙ, yₙ)', ['yₙ₊₁ = yₙ + f(xₙ, yₙ)', 'yₙ₊₁ = h f(xₙ, yₙ)', 'yₙ₊₁ = yₙ + h f(xₙ₊₁, yₙ)'], 'Follow the tangent at the current point.'),
           ("Halving the step length in Euler's method typically", 'roughly halves the error', ['doubles the error', 'has no effect', 'makes the error zero'], 'Euler is a first-order method.'),
           ('In the slope field for dy/dx = x − y, the segments are horizontal along', 'the line y = x', ['the x-axis', 'the y-axis', 'the line y = −x'], 'dy/dx = 0 when y = x.'),
           ("For a solution curve that is concave up, Euler's method gives", 'an underestimate', ['an overestimate', 'the exact value', 'no information'], 'Tangent lines lie below a convex curve.')],
    why=[("Explain why Euler's method gives an underestimate when the solution curve is concave up.", 'Each step follows the tangent line, and the tangent to a concave-up curve lies below the curve, so each new estimate is too low and the errors accumulate.'),
         ("Explain how the accuracy of Euler's method can be improved, and state a drawback.", 'Use a smaller step length h: the tangent is followed for a shorter distance so the error decreases (roughly in proportion to h), but more iterations are needed.'),
         ('Explain how a slope field can be used to sketch a particular solution.', 'Start at the point given by the initial condition and draw a curve that follows the direction of the nearby segments everywhere, so it is tangent to the field at each point.')],
    misc=[("Euler's method gives the exact solution if the step length is small enough.", 'Any positive h gives an approximation; the error decreases as h decreases but is generally non-zero.'),
          ('In the slope field of dy/dx = y, all segments in the same column are parallel.', 'dy/dx depends on y only, so segments in the same row (same y) are parallel; columns vary.')],
))


def _euler_f(rng):
    a, b, c = nz(rng, -2, 3), nz(rng, -2, 2), rng.randint(-2, 2)
    kind = rng.choice(['lin', 'prod', 'sq', 'sin', 'exp', 'root'])
    if kind == 'lin':
        f = a * x + b * y + c
    elif kind == 'prod':
        f = a * x * y + c
    elif kind == 'sq':
        f = x ** 2 + b * y
    elif kind == 'sin':
        f = sp.sin(x) + b * y
    elif kind == 'exp':
        f = sp.exp(-x) + b * y
    else:
        f = sp.sqrt(x + y)
    return f


def _euler_run(f, x0, y0, h, n):
    g = sp.lambdify((x, y), f, 'math')
    xs_, ys_ = [x0], [y0]
    for _ in range(n):
        try:
            ys_.append(ys_[-1] + h * g(xs_[-1], ys_[-1]))
        except ValueError:
            return None
        xs_.append(round(xs_[-1] + h, 10))
    return xs_, ys_


@R.add('ch11-st4', 'C3', (2, 5), 'short', style='p2')
def euler_steps(rng, slot):
    f = _euler_f(rng)
    x0 = rng.choice([0, 1]); y0 = rng.choice([1, 2, 3, 0.5])
    h = rng.choice([0.1, 0.2, 0.25, 0.5]); n = rng.choice([2, 3, 4]) if slot.d <= 3 else rng.choice([4, 5])
    r_ = _euler_run(f, x0, y0, h, n)
    if not r_:
        return None
    xs_, ys_ = r_
    if any(abs(v) > 1e4 for v in ys_):
        return None
    tbl = '; '.join(f'x = {a_:g}, y ≈ {sfig(b_)}' for a_, b_ in zip(xs_[1:], ys_[1:]))
    return mk(f"Use Euler's method with step length {h} to find an approximation for y when x = {xs_[-1]:g}, given that dy/dx = {P(f)} and y = {y0} when x = {x0}.", s3(ys_[-1]),
              f'yₙ₊₁ = yₙ + {h} × ({P(f)}) (M1); first step correct (A1); {tbl} (M1 A1); y ≈ {s3(ys_[-1])} (A1).', 5)


@R.add('ch11-st4', 'C3', (3, 5), 'short', style='p2')
def euler_vs_exact(rng, slot):
    kind = rng.choice(['ky', 'xy_lin'])
    h = rng.choice([0.1, 0.2, 0.25]); X = rng.choice({0.1: [0.5, 1.0], 0.2: [0.4, 0.6, 1.0], 0.25: [0.5, 1.0]}[h])
    n = int(round(X / h))
    if kind == 'ky':
        k = rng.choice([0.5, 1, 2, -1, -0.5]); y0 = rng.choice([1, 2, 5])
        f = k * y
        exact = y0 * math.exp(k * X)
        ex_txt = f'y = {y0 if y0 > 1 else ""}e^({ {0.5: "0.5x", 1: "x", 2: "2x", -1: "−x", -0.5: "−0.5x"}[k] })'.replace('e^(x)', 'eˣ')
    else:
        a = rng.choice([1, 2]); y0 = rng.choice([0, 1, 2])
        f = y + a * x
        exact = (y0 + a) * math.exp(X) - a * X - a
        ex_txt = f'y = {y0 + a}eˣ − {a if a > 1 else ""}x − {a}'
    xs_, ys_ = _euler_run(f, 0, y0, h, n)
    err = abs(exact - ys_[-1]) / abs(exact) * 100
    return mk(f"The solution of dy/dx = {P(f)}, y(0) = {y0}, is {ex_txt}. (a) Use Euler's method with h = {h} to estimate y({X:g}). (b) Find the percentage error in this estimate.",
              f'(a) {s3(ys_[-1])} (b) {s3(err)}%', f'(a) iteration yₙ₊₁ = yₙ + {h}({P(f)}) (M1) over {n} steps (A1); {s3(ys_[-1])} (A1). (b) exact {s3(exact)} (A1); |exact − approx|/exact × 100 (M1) = {s3(err)}% (A1).', 6)


@R.add('ch11-st4', 'C3', (2, 4), 'short', style='p1')
def slope_field_calc(rng, slot):
    a, b = nz(rng, -3, 3), nz(rng, -3, 3)
    kind = rng.choice(['lin', 'quad', 'prod'])
    if kind == 'lin':
        f = a * x + b * y
    elif kind == 'quad':
        f = x ** 2 + b * y
    else:
        f = x * (y + a)
    pts = rng.sample([(0, 1), (1, 1), (1, 2), (2, 1), (-1, 2), (2, -1), (1, -1), (0, 2)], 2)
    vals = [f.subs({x: p_[0], y: p_[1]}) for p_ in pts]
    iso = sp.solve(f, y)
    iso_txt = ' or '.join(f'y = {P(s_)}' for s_ in iso) if kind != 'prod' else f'x = 0 or y = {-a}'
    return mk(f'A slope field is drawn for dy/dx = {P(f)}. (a) Find the gradient of the segments at {pt(pts[0])} and at {pt(pts[1])}. (b) Find the equation of the curve(s) on which all segments are horizontal.',
              f'(a) {P(vals[0])}, {P(vals[1])} (b) {iso_txt}', f'(a) substitute each point (M1); {P(vals[0])} (A1); {P(vals[1])} (A1). (b) dy/dx = 0 (M1); {iso_txt} (A1).', 5)


@R.add('ch11-st4', 'C1', (1, 3), 'mcq')
def euler_one_mcq(rng, slot):
    a, b = rng.randint(1, 3), rng.randint(1, 3)
    x0, y0 = rng.randint(0, 2), rng.randint(1, 4)
    h = rng.choice([Fr(1, 10), Fr(1, 5), Fr(1, 2)])
    fv = a * x0 + b * y0
    right = y0 + h * fv
    wr = [y0 + fv, h * fv, y0 + h * (a * (x0 + h) + b * y0)]
    f2 = lambda q: f'{float(q):g}'
    if len({f2(right)} | {f2(w) for w in wr}) < 4:
        return None
    return mcq(rng, f"For dy/dx = {a if a > 1 else ''}x + {b if b > 1 else ''}y with y = {y0} when x = {x0}, one step of Euler's method with h = {float(h):g} gives y ≈", f2(right), [f2(w) for w in wr],
               f'y₁ = {y0} + {float(h):g} × ({a}×{x0} + {b}×{y0}) = {f2(right)}.')


@R.add('ch11-st4', 'C2', (2, 4), 'explain')
def euler_concavity_explain(rng, slot):
    k = rng.choice([1, 2, 3]); y0 = rng.choice([1, 2, 4]); m = rng.choice([2, 5, 10])
    cases = [(f'x + {k if k > 1 else ""}y', f'd²y/dx² = 1 + {k if k > 1 else ""}dy/dx > 0 for x, y > 0', 'an underestimate'),
             (f'−{k if k > 1 else ""}y', f'd²y/dx² = {k * k}y > 0 for y > 0', 'an underestimate'),
             ('x² + y²', 'd²y/dx² = 2x + 2y dy/dx > 0 for x, y > 0', 'an underestimate'),
             (f'{m} − y', f'd²y/dx² = −dy/dx = y − {m} < 0 while y < {m}', 'an overestimate'),
             (f'{k if k > 1 else ""}/y', f'd²y/dx² = −{k if k > 1 else ""}/y² · dy/dx < 0 for y > 0', 'an overestimate')]
    f, conc, res = rng.choice(cases)
    if f.startswith(f'{m}') and y0 >= m:
        return None
    return mk(f"Euler's method is used to estimate y(1) for dy/dx = {f}, y(0) = {y0}. Explain whether the estimate is likely to be an overestimate or an underestimate.", res,
              f'{conc} (M1 A1); the curve is concave {"up" if "under" in res else "down"}, so tangents lie {"below" if "under" in res else "above"} it and Euler gives {res} (R1).', 3, 'explain')


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step', style='ext')
def euler_parts(rng, slot):
    a = rng.choice([1, 2, 3]); y0 = rng.choice([0, 1, 2]); h = rng.choice([0.1, 0.2, 0.25]); X = rng.choice({0.1: [0.5, 1.0], 0.2: [0.4, 0.6, 1.0], 0.25: [0.5, 1.0]}[h])
    n = int(round(X / h))
    f = y + a * x
    xs_, ys_ = _euler_run(f, 0, y0, h, n)
    exact = (y0 + a) * math.exp(X) - a * X - a
    xs2, ys2 = _euler_run(f, 0, y0, h / 2, 2 * n)
    parts = [(f"Use Euler's method with h = {h} to estimate y({X:g}).", s3(ys_[-1]), 'M1 A1 A1', 3, True),
             ('Use an integrating factor to solve the differential equation exactly.', f'y = {y0 + a}eˣ − {a if a > 1 else ""}x − {a}', f'I = e^(−x) (M1); d/dx(ye^(−x)) = {a if a > 1 else ""}xe^(−x) (A1); integrate by parts (M1); constant from y(0) (A1)', 4, True),
             (f'Find the percentage error in the estimate from part (a).', f'{s3(abs(exact - ys_[-1]) / exact * 100)}%', 'M1 A1', 2, True),
             (f'Repeat part (a) with h = {h / 2:g} and comment on the result.', f'{s3(ys2[-1])}; error roughly halves', 'A1 R1', 2, False),
             ('Explain, with reference to the shape of the solution curve, why the estimates are too small.', f'd²y/dx² = dy/dx + {a} = y + {a if a > 1 else ""}x + {a} > 0 for x, y ≥ 0, so the curve is concave up and tangents lie below it', 'R1 R1', 2, False)]
    return build_parts(rng, [f'Consider the differential equation dy/dx = y + {a if a > 1 else ""}x, with y = {y0} when x = 0.', f'A curve passes through (0, {y0}) and satisfies dy/dx = {a if a > 1 else ""}x + y.'], parts, 3)


@R.add('ch11-st4', 'C4', (4, 5), 'multi_step', style='p3')
def euler_limit_parts(rng, slot):
    k = rng.choice([1, 2, 3, -1]); y0 = rng.choice([1, 2, 3]); X = 1
    N = rng.choice([4, 5, 10])
    yN = y0 * (1 + k / N) ** N
    y2N = y0 * (1 + k / (2 * N)) ** (2 * N)
    ex_ = y0 * math.exp(k)
    e1, e2 = abs(ex_ - yN), abs(ex_ - y2N)
    parts = [(f"Show that Euler's method with step h applied to dy/dx = {k if k not in (1, -1) else ('' if k == 1 else '−')}y, y(0) = {y0}, gives yₙ = {y0 if y0 > 1 else ''}(1 + {'' if k == 1 else '−' if k == -1 else k}h)ⁿ.".replace('+ −', '− '), 'shown', 'yₙ₊₁ = yₙ(1 + kh) (M1); geometric sequence (R1) AG', 2, True),
             (f'With h = 1/{N}, find the estimate of y(1).', s3(yN), 'A1', 1, True),
             (f'With h = 1/{2 * N}, find the estimate of y(1).', s3(y2N), 'A1', 1, True),
             ('Find the exact value of y(1) and the error in each estimate.', f'{s3(ex_)}; errors {s3(e1)} and {s3(e2)}', 'A1 A1', 2, True),
             ('Comment on the ratio of the errors and what it suggests about the method.', f'ratio ≈ {s3(e1 / e2)} ≈ 2: error is roughly proportional to h', 'R1 R1', 2, True),
             (f'Show that as n → ∞ with h = 1/n, the estimate tends to the exact value.', f'(1 + {k}/n)ⁿ → e^{k}' if k != 1 else '(1 + 1/n)ⁿ → e', 'standard limit (R1) A1', 2, False)]
    return build_parts(rng, [f"This question investigates the error in Euler's method for a simple growth equation.", f"Consider dy/dx = {k if k not in (1, -1) else ('' if k == 1 else '−')}y with y = {y0} when x = 0."], parts, 4)


# =============================================================================================
# ch12 Maclaurin series and limits (AHL 5.13, 5.19)
# =============================================================================================
def ser_txt(e, n, var=x):
    """Maclaurin polynomial up to and including x^n, written in ascending powers."""
    poly = sp.series(e, var, 0, n + 1).removeO()
    terms = sorted(sp.Add.make_args(sp.expand(poly)), key=lambda tm: sp.degree(tm, var) if tm.has(var) else 0)
    out = ''
    for i, tm in enumerate(terms):
        s_ = P(tm)
        if i == 0:
            out = s_
        elif s_.startswith('−'):
            out += ' − ' + s_[1:]
        else:
            out += ' + ' + s_
    return out or '0'


def nonzero_terms(e, k, var=x, maxn=14):
    """First k non-zero terms of the Maclaurin series, as text, and the highest power used."""
    poly = sp.expand(sp.series(e, var, 0, maxn).removeO())
    terms = sorted([tm for tm in sp.Add.make_args(poly) if tm != 0], key=lambda tm: sp.degree(tm, var) if tm.has(var) else 0)[:k]
    n = max((sp.degree(tm, var) if tm.has(var) else 0) for tm in terms)
    return ser_txt(sum(terms), n, var), n


R.facts('ch12-st1', F(
    terms=[("L'Hôpital's rule", 'if lim f(x) = lim g(x) = 0 (or both ±∞) as x → a, then lim f(x)/g(x) = lim f′(x)/g′(x), provided the latter limit exists'),
           ('indeterminate form', 'a limit of the type 0/0 or ∞/∞ (or 0·∞, ∞ − ∞) whose value cannot be found by direct substitution'),
           ('limit of a function', 'the value that f(x) approaches as x approaches a given value, written lim as x → a of f(x)')],
    facts=[("L'Hôpital's rule can be applied directly to", 'lim as x → 0 of sin x / x', ['lim as x → 0 of (x + 1)/(x + 2)', 'lim as x → 1 of x² / (x + 1)', 'lim as x → 0 of cos x / (1 + x)'], 'Only sin x / x gives 0/0 at x = 0.'),
           ('lim as x → 0 of (1 − cos x)/x² =', '1/2', ['0', '1', '∞'], "Apply L'Hôpital twice: sin x/(2x) → cos x/2 → 1/2."),
           ('lim as x → ∞ of ln x / x =', '0', ['1', '∞', 'e'], "∞/∞: (1/x)/1 → 0."),
           ("In L'Hôpital's rule you differentiate", 'the numerator and the denominator separately', ['the quotient f/g using the quotient rule', 'only the numerator', 'the product f·g'], 'f′/g′, not (f/g)′.')],
    why=[("Explain why L'Hôpital's rule cannot be used for lim as x → 0 of (eˣ + 1)/(x + 1).", 'Direct substitution gives 2/1 = 2, which is not an indeterminate form; the rule only applies to 0/0 or ∞/∞, and here it would give the wrong answer eˣ/1 → 1.'),
         ('Explain how a limit of the form 0 × ∞ such as lim as x → 0⁺ of x ln x can be evaluated.', "Rewrite as ln x / (1/x), which is ∞/∞; L'Hôpital gives (1/x)/(−1/x²) = −x → 0."),
         ("Explain why L'Hôpital's rule may need to be applied more than once.", 'After one application the new quotient f′/g′ may still be of the form 0/0; the rule is applied again (each time checking the form) until the limit can be found by substitution.')],
    misc=[("By L'Hôpital, lim as x → 0 of sin(3x)/x = lim of (sin 3x)′/(x)′ = cos(3x) → 1.", 'The chain rule was missed: (sin 3x)′ = 3cos 3x, so the limit is 3.'),
          ("lim as x → 0 of (x + 2)/(x + 1) = lim of 1/1 = 1 by L'Hôpital.", 'The form is 2/1, not indeterminate; the limit is 2 by substitution.')],
))

LIM_POOL = [
    lambda rng, a, b: ((sp.exp(a * x) - 1) / (b * x), 0),
    lambda rng, a, b: (sp.sin(a * x) / (b * x), 0),
    lambda rng, a, b: ((1 - sp.cos(a * x)) / x ** 2, 0),
    lambda rng, a, b: (sp.log(1 + a * x) / (b * x), 0),
    lambda rng, a, b: ((x ** (a + 1) - b ** (a + 1)) / (x - b), b),
    lambda rng, a, b: ((sp.exp(a * x) - 1 - a * x) / x ** 2, 0),
    lambda rng, a, b: (sp.tan(a * x) / sp.sin(b * x), 0),
    lambda rng, a, b: ((sp.exp(a * x) - sp.exp(b * x)) / x, 0),
    lambda rng, a, b: ((x - sp.sin(x)) / x ** 3, 0),
    lambda rng, a, b: (sp.log(x) / (x - 1), 1),
    lambda rng, a, b: ((sp.cos(a * x) - sp.cos(b * x)) / x ** 2, 0),
    lambda rng, a, b: (sp.sin(a * x) ** 2 / (b * x ** 2), 0),
]

LIM_INF = [
    lambda rng, a, b: (sp.log(x) / x ** a, sp.oo),
    lambda rng, a, b: (x ** a * sp.exp(-b * x), sp.oo),
    lambda rng, a, b: ((a * x ** 2 + b) / (b * x ** 2 + a * x), sp.oo),
    lambda rng, a, b: (x * sp.sin(sp.Integer(a) / x), sp.oo),
]


def _lim_txt(f, a):
    to = '∞' if a == sp.oo else P(a)
    ft = re.sub(r'(sin|cos|tan)\(([^()]*)\)²', r'\1²(\2)', P(f))
    return f'lim as x → {to} of {ft}'


@R.add('ch12-st1', 'C3', (2, 5), 'short', style='p1')
def lhop_limit(rng, slot):
    pool = LIM_POOL[:5] if slot.d <= 2 else LIM_POOL + LIM_INF
    a, b = rng.choice([1, 2, 3, 4, 5]), rng.choice([1, 2, 3, 4, 5])
    if a == b:
        b = a + 1
    f, at = rng.choice(pool)(rng, a, b)
    v = sp.limit(f, x, at)
    if v.has(sp.oo) or v.has(sp.zoo) or isinstance(v, sp.AccumBounds):
        return None
    num, den = sp.fraction(sp.together(f))
    reps = 1
    g, h_ = num, den
    for _ in range(4):
        try:
            gv, hv = sp.limit(g, x, at), sp.limit(h_, x, at)
        except Exception:
            return None
        if (gv == 0 and hv == 0) or (abs(gv) == sp.oo and abs(hv) == sp.oo):
            g, h_ = sp.diff(g, x), sp.diff(h_, x)
            reps += 1
        else:
            break
    reps -= 1
    form = '0/0' if at != sp.oo else '∞/∞'
    how = "L'Hôpital's rule" + (f' {reps} times' if reps > 1 else '')
    return mk(f'Find {_lim_txt(f, at)}.', P(v),
              f'Recognise the indeterminate form {form} (R1); apply {how}: differentiate numerator and denominator (M1 A1); evaluate the limit (M1); {P(v)} (A1).', 5)


@R.add('ch12-st1', 'C3', (3, 5), 'short', style='p1')
def lhop_param(rng, slot):
    a = rng.choice([1, 2, 3, 4, 6])
    kind = rng.choice(['sin', 'exp', 'cos'])
    k = sp.Symbol('k')
    if kind == 'sin':
        L = rng.choice([2, 3, 4, 6, sp.Rational(1, 2)])
        f = sp.sin(k * x) / (a * x)
        kv = L * a
        stem = f'Given that lim as x → 0 of sin(kx)/({a if a > 1 else ""}x) = {P(L)}, find the value of k.'.replace('/(x)', '/x')
        key = f'0/0 (R1); k cos(kx)/{a} → k/{a} (M1 A1); k = {P(kv)} (A1).'.replace('/1 ', ' ').replace('/1 (', ' (')
    elif kind == 'exp':
        L = rng.choice([2, 3, sp.Rational(1, 2), 4])
        f = (sp.exp(k * x) - 1) / (a * x)
        kv = L * a
        stem = f'Given that lim as x → 0 of (e^(kx) − 1)/({a if a > 1 else ""}x) = {P(L)}, find the value of k.'.replace('/(x)', '/x')
        key = f'0/0 (R1); ke^(kx)/{a} → k/{a} (M1 A1); k = {P(kv)} (A1).'.replace('/1 ', ' ').replace('/1 (', ' (')
    else:
        L = rng.choice([2, 8, sp.Rational(9, 2), 18])
        kv = sp.sqrt(2 * L)
        f = (1 - sp.cos(k * x)) / x ** 2
        stem = f'Given that lim as x → 0 of (1 − cos(kx))/x² = {P(L)}, where k > 0, find the value of k.'
        key = f"L'Hôpital twice: k sin(kx)/(2x) → k² cos(kx)/2 → k²/2 (M1 A1 A1); k = {P(kv)} (A1)."
    assert sp.simplify(sp.limit(f.subs(k, kv), x, 0) - L) == 0
    return mk(stem, f'k = {P(kv)}', key, 4)


@R.add('ch12-st1', 'C1', (1, 3), 'mcq')
def lhop_mcq(rng, slot):
    a, b = rng.sample([1, 2, 3, 4, 5, 6], 2)
    kind = rng.choice(['sin', 'exp', 'ln', 'tan'])
    f = {'sin': sp.sin(a * x) / (b * x), 'exp': (sp.exp(a * x) - 1) / (b * x), 'ln': sp.log(1 + a * x) / (b * x), 'tan': sp.tan(a * x) / (b * x)}[kind]
    v = sp.limit(f, x, 0)
    wr = [P(sp.Rational(b, a)), P(sp.Integer(a * b)) if a * b != v else '0', '1' if v != 1 else '0']
    if len({P(v)} | set(wr)) < 4:
        wr = [P(sp.Rational(b, a)), '0', '∞']
    return mcq(rng, f'{_lim_txt(f, 0)} =', P(v), wr, f"0/0; L'Hôpital: differentiate numerator and denominator, then substitute x = 0 to get {P(v)}.")


@R.add('ch12-st1', 'C2', (2, 4), 'explain')
def lhop_explain(rng, slot):
    a, b, c = rng.randint(1, 5), rng.randint(1, 5), rng.randint(2, 6)
    kind = rng.choice(['notindet', 'chain', 'zeroinf'])
    if kind == 'notindet':
        f = (sp.exp(a * x) + b) / (x + c)
        v = sp.Rational(1 + b, c)
        return mk(f"{who(rng)} uses L'Hôpital's rule to claim that lim as x → 0 of ({P(sp.exp(a * x))} + {b})/(x + {c}) = {a}. Explain the error and find the correct limit.", P(v),
                  f'At x = 0 the quotient is {1 + b}/{c}, not 0/0 or ∞/∞, so the rule does not apply (R1 R1); the limit is {P(v)} by substitution (A1).', 3, 'explain')
    if kind == 'chain':
        f = sp.sin(a * x + 0) / sp.sin(c * x)
        v = sp.Rational(a, c)
        return mk(f"A student writes lim as x → 0 of sin({a if a > 1 else ''}x)/sin({c}x) = lim of cos({a if a > 1 else ''}x)/cos({c}x) = 1. Explain the error and find the correct value.".replace('sin(x)', 'sin x').replace('cos(x)', 'cos x'), P(v),
                  f'The chain rule was not applied: derivatives are {a}cos({a}x) and {c}cos({c}x) (R1 M1); limit {P(v)} (A1).', 3, 'explain')
    v = 0
    return mk(f'Explain how to evaluate lim as x → 0⁺ of x{str(a).translate(_SUP) if a > 1 else ""} ln x, and find its value.', '0',
              f"0 × (−∞) form; rewrite as ln x / x{('⁻' + str(a).translate(_SUP)) if a > 1 else '⁻¹'}, which is ∞/∞ (R1); L'Hôpital: (1/x)/(−{a}x^(−{a + 1})) = −x{str(a).translate(_SUP) if a > 1 else ''}/{a} (M1); → 0 (A1).", 3, 'explain')


@R.add('ch12-st1', 'C4', (3, 5), 'multi_step', style='ext')
def lhop_parts(rng, slot):
    a = rng.choice([1, 2, 3]); b = rng.choice([2, 3, 4])
    f = (sp.exp(a * x) - 1 - a * x) / x ** 2
    v1 = sp.limit(f, x, 0)
    g = (x - sp.sin(x)) / (x ** 2 * sp.tan(b * x))
    v2 = sp.limit(g, x, 0)
    h_ = (1 + sp.Integer(a) / x) ** x
    parts = [(f'Find lim as x → 0 of ({P(sp.exp(a * x))} − 1 − {P(a * x)})/x².', P(v1), "0/0 (R1); L'Hôpital twice (M1 A1); A1", 4, True),
             (f'Find lim as x → 0 of (x − sin x)/(x² tan({b}x)).', P(v2), "repeated L'Hôpital or standard limits (M1 M1) A1", 3, True),
             (f'By considering ln y, where y = (1 + {a}/x)ˣ, find lim as x → ∞ of (1 + {a}/x)ˣ.', P(sp.exp(a)), f"ln y = ln(1 + {a}/x)/(1/x), 0/0 (M1); L'Hôpital: → {a} (A1); y → {P(sp.exp(a))} (A1)", 3, True),
             ('Explain why the limit in the previous part is not 1, even though 1 + a/x → 1.', '1^∞ is indeterminate; the exponent grows as the base tends to 1', 'R1', 1, False)]
    return build_parts(rng, ["This question uses L'Hôpital's rule.", 'This question is about evaluating limits of indeterminate forms.'], parts, 3)


@R.add('ch12-st1', 'C4', (4, 5), 'multi_step')
def lhop_family(rng, slot):
    n = rng.choice([2, 3, 4]); a = rng.choice([1, 2, 3])
    val = lambda m: sp.limit((sp.exp(a * x) - sum((a * x) ** j / sp.factorial(j) for j in range(m))) / x ** m, x, 0)
    parts = [(f'Find L₁ = lim as x → 0 of (e^({a if a > 1 else ""}x) − 1)/x.'.replace('e^(x)', 'eˣ'), P(val(1)), "L'Hôpital (M1) A1", 2, True),
             (f'Find L₂ = lim as x → 0 of (e^({a if a > 1 else ""}x) − 1 − {a if a > 1 else ""}x)/x².'.replace('e^(x)', 'eˣ'), P(val(2)), "L'Hôpital twice (M1) A1", 2, True),
             (f'Find L₃, the corresponding limit with x³ in the denominator and the first three terms of the series of e^({a if a > 1 else ""}x) subtracted.'.replace('e^(x)', 'eˣ'), P(val(3)), 'M1 A1', 2, True),
             (f'Conjecture a formula for Lₙ and use it to state L₄.', f'Lₙ = {a if a > 1 else ""}{"ⁿ" if a > 1 else ""}/n!'.replace('/n!', '/n!' if a > 1 else '1/n!') + f'; L₄ = {P(val(4))}', 'pattern (R1) A1', 2, True),
             ("Explain why applying L'Hôpital's rule n times proves the conjecture.", 'each application lowers the power of x by one and the numerator to a^k e^(ax) minus a polynomial; after n steps the limit is aⁿ/n!', 'R1 R1', 2, False)]
    out = build_parts(rng, [f'This question investigates a family of limits involving e^({a if a > 1 else ""}x).'.replace('e^(x)', 'eˣ'), 'A sequence of limits is defined using the Maclaurin polynomial of an exponential function.'], parts, 4)
    out['answer'] = out['answer'].replace('Lₙ = 1/n!', 'Lₙ = 1/n!').replace('Lₙ = /n!', 'Lₙ = 1/n!')
    return out


# ---------------------------------------------------------------------------------------------
R.facts('ch12-st2', F(
    terms=[('Maclaurin series', 'the expansion f(x) = f(0) + f′(0)x + f″(0)x²/2! + f‴(0)x³/3! + …, a power series about x = 0'),
           ('interval of convergence', 'the set of x-values for which a power series converges, e.g. −1 < x ≤ 1 for ln(1 + x)'),
           ('extended binomial theorem', '(1 + x)ᵖ = 1 + px + p(p − 1)x²/2! + p(p − 1)(p − 2)x³/3! + … for any rational p, valid for |x| < 1')],
    facts=[('The Maclaurin series of eˣ is', '1 + x + x²/2! + x³/3! + …', ['1 + x + x² + x³ + …', 'x − x³/3! + x⁵/5! − …', '1 − x²/2! + x⁴/4! − …'], 'Every derivative of eˣ equals 1 at 0.'),
           ('The Maclaurin series of sin x contains', 'only odd powers of x', ['only even powers of x', 'all powers of x', 'no powers of x above 3'], 'sin x is an odd function.'),
           ('The series for ln(1 + x) is valid for', '−1 < x ≤ 1', ['all real x', '|x| < 2', 'x > −1'], 'Interval of convergence from the data booklet.'),
           ('The coefficient of x² in the Maclaurin series of f(x) is', 'f″(0)/2', ['f″(0)', 'f′(0)/2', '2f″(0)'], 'General term f⁽ⁿ⁾(0)xⁿ/n!.'),
           ('The first three terms of (1 + x)^(−1) are', '1 − x + x²', ['1 + x + x²', '1 − x − x²', '−1 + x − x²'], 'p = −1.')],
    why=[('Explain why the Maclaurin series of cos x contains only even powers of x.', 'cos x is an even function, cos(−x) = cos x, so its odd-order derivatives (±sin x) are zero at x = 0 and those coefficients vanish.'),
         ('Explain why a Maclaurin polynomial gives a good approximation only for x close to 0.', 'The series is built from the derivatives at x = 0; the neglected terms contain higher powers of x, which are small only when |x| is small (and the series may diverge outside its interval of convergence).'),
         ('Explain why the series for ln(1 + x) cannot be used directly to find ln 5.', 'ln 5 needs x = 4, which is outside the interval of convergence −1 < x ≤ 1, so the series diverges.')],
    misc=[('The Maclaurin series of sin x is x − x³/3 + x⁵/5 − …', 'The denominators are factorials: x − x³/3! + x⁵/5! − …'),
          ('(1 + x)^(1/2) = 1 + ½x + ¼x² + …', 'The x² coefficient is (½)(−½)/2! = −⅛, so (1 + x)^(1/2) = 1 + ½x − ⅛x² + …')],
))


def _std_fn(rng, allow_binom=True):
    a = rng.choice([1, 2, 3, -1, -2, sp.Rational(1, 2), 4])
    kinds = ['exp', 'sin', 'cos', 'ln'] + (['binom', 'binom'] if allow_binom else [])
    kind = rng.choice(kinds)
    if kind == 'exp':
        return kind, sp.exp(a * x), None
    if kind == 'sin':
        return kind, sp.sin(abs(a) * x), None
    if kind == 'cos':
        return kind, sp.cos(abs(a) * x), None
    if kind == 'ln':
        return kind, sp.log(1 + a * x), f'{P(-1 / sp.Abs(a))} < x ≤ {P(1 / sp.Abs(a))}' if a > 0 else f'{P(-1 / sp.Abs(a))} ≤ x < {P(1 / sp.Abs(a))}'
    p_ = rng.choice([-1, -2, sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(1, 3), -3, sp.Rational(3, 2)])
    return kind, (1 + a * x) ** p_, f'|x| < {P(1 / sp.Abs(a))}'


def _ftxt(f):
    s_ = P(f)
    s_ = re.sub(r'\(([^()]*?x) \+ 1\)', r'(1 + \1)', s_)
    s_ = re.sub(r'\((−[^()]*?x) \+ 1\)', lambda m_: '(1 − ' + m_.group(1)[1:] + ')', s_)
    return s_


def sci(v):
    """3 s.f., in standard form when very small."""
    v = float(v)
    if v == 0 or abs(v) >= 0.001:
        return s3(v)
    e_ = math.floor(math.log10(abs(v)))
    m_ = v / 10 ** e_
    return f'{m_:.2f} × 10{str(e_).translate(_SUP)}'


@R.add('ch12-st2', 'C3', (1, 5), 'short', style='p1')
def mac_std(rng, slot):
    kind, f, rng_txt = _std_fn(rng)
    k = 3 if slot.d <= 3 else 4
    txt, n = nonzero_terms(f, k)
    valid = slot.d >= 4 and rng_txt
    return mk(f'Find the first {k} non-zero terms of the Maclaurin series for {_ftxt(f)}' + (', and state the values of x for which the series is valid.' if valid else '.'),
              txt + (f'; valid for {rng_txt}' if valid else ''),
              f'Use the standard series with x replaced by {P(f.args[0] if kind != "binom" else sp.expand(f.args[0] - 1))} (M1); {txt} (A1 A1 A1)' + (f'; {rng_txt} (A1).' if valid else '.'), 5 if valid else 4)


DERIVE_POOL = [
    lambda rng: (sp.tan(x), 3), lambda rng: (1 / sp.cos(x), 2), lambda rng: (sp.log(sp.cos(x)), 2), lambda rng: (sp.exp(sp.sin(x)), 2),
    lambda rng: (sp.log(rng.choice([2, 3, 4, 5]) + x), 2), lambda rng: (sp.atan(x), 3), lambda rng: (sp.asin(x), 3),
    lambda rng: (sp.sqrt(rng.choice([4, 9, 16]) + x), 2), lambda rng: (sp.exp(rng.choice([1, 2, 3]) * x + rng.choice([1, 2])), 2),
    lambda rng: (sp.log(1 + sp.sin(x)), 2), lambda rng: (sp.exp(x) * sp.cos(x), 3), lambda rng: (1 / (rng.choice([2, 3, 4]) - x), 2),
    lambda rng: (sp.sin(x + pi / rng.choice([4, 6, 3])), 2), lambda rng: (sp.cos(x) ** 2, 2),
]


@R.add('ch12-st2', 'C3', (2, 5), 'short', style='p1')
def mac_derive(rng, slot):
    f, n = rng.choice(DERIVE_POOL)(rng)
    ds = [sp.simplify(sp.diff(f, x, j).subs(x, 0)) for j in range(n + 1)]
    names = ['f(0)', 'f′(0)', 'f″(0)', 'f‴(0)']
    vals = ', '.join(f'{names[j]} = {P(sp.nsimplify(ds[j]) if ds[j].is_number and not ds[j].has(sp.log) else ds[j])}' for j in range(n + 1))
    txt = ser_txt(f, n)
    return mk(f'Let f(x) = {P(f)}. By finding {", ".join(names[:n])} and {names[n]}, find the Maclaurin series for f(x) up to and including the term in x{str(n).translate(_SUP)}.',
              f'{vals}; f(x) ≈ {txt}', f'Successive derivatives (M1 A1 A1); {vals} (A1); use f⁽ⁿ⁾(0)xⁿ/n! (M1); {txt} (A1).', 6)


@R.add('ch12-st2', 'C3', (2, 5), 'short', style='p1')
def mac_coeff(rng, slot):
    a = rng.choice([2, 3, -2, -3, sp.Rational(1, 2), 4])
    kk = rng.choice([2, 3, 4])
    kind = rng.choice(['binom', 'exp', 'ln'])
    if kind == 'binom':
        p_ = rng.choice([-1, -2, sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(1, 3), -3])
        f = (1 + a * x) ** p_
    elif kind == 'exp':
        f = sp.exp(a * x)
    else:
        f = sp.log(1 + a * x)
    c = sp.series(f, x, 0, kk + 1).removeO().coeff(x, kk)
    return mk(f'Find the coefficient of x{str(kk).translate(_SUP)} in the Maclaurin series for {_ftxt(f)}.', P(c),
              f'General term of the standard series (M1); substitute {P(a * x)} (M1); ({P(a)}){str(kk).translate(_SUP)} handled correctly (A1); {P(c)} (A1).', 4)


@R.add('ch12-st2', 'C3', (2, 5), 'short', style='p2')
def mac_approx(rng, slot):
    kind = rng.choice(['exp', 'sin', 'cos', 'ln', 'sqrt', 'recip'])
    v = rng.choice([0.1, 0.2, 0.3, 0.05, 0.15])
    k = rng.choice([2, 3])
    if kind == 'exp':
        f, lab, true = sp.exp(x), f'e^{v}', math.exp(v)
    elif kind == 'sin':
        f, lab, true = sp.sin(x), f'sin({v})', math.sin(v)
    elif kind == 'cos':
        f, lab, true = sp.cos(x), f'cos({v})', math.cos(v)
    elif kind == 'ln':
        f, lab, true = sp.log(1 + x), f'ln({1 + v:g})', math.log(1 + v)
    elif kind == 'sqrt':
        f, lab, true = sp.sqrt(1 + x), f'√{1 + v:g}', math.sqrt(1 + v)
    else:
        f, lab, true = 1 / (1 + x), f'1/{1 + v:g}', 1 / (1 + v)
    txt, n = nonzero_terms(f, k)
    poly = sp.series(f, x, 0, n + 1).removeO()
    approx = float(poly.subs(x, v))
    err = abs(true - approx)
    return mk(f'Use the first {k} non-zero terms of the Maclaurin series for {_ftxt(f)} to find an approximation for {lab}. Give your answer to 6 decimal places and find the absolute error compared with the GDC value.',
              f'{approx:.6f}; error {sci(err)}', f'Series {txt} (M1 A1); substitute x = {v} (M1); {approx:.6f} (A1); GDC {true:.6f}, error {sci(err)} (A1).', 5)


@R.add('ch12-st2', 'C1', (1, 3), 'mcq')
def mac_mcq(rng, slot):
    kind, f, _ = _std_fn(rng)
    txt, n = nonzero_terms(f, 3)
    g = f.subs(x, -x)
    wr = []
    for alt in (sp.exp(x) if kind != 'exp' else sp.sin(x), g, f.subs(x, 2 * x)):
        t_, _ = nonzero_terms(alt, 3)
        if t_ != txt and t_ not in wr:
            wr.append(t_)
    wr.append(ser_txt(sp.integrate(sp.series(f, x, 0, n + 1).removeO(), x), n + 1) if len(wr) < 3 else '')
    wr = [w for w in wr if w and w != txt][:3]
    if len(wr) < 3:
        return None
    return mcq(rng, f'The first three non-zero terms of the Maclaurin series for {_ftxt(f)} are', txt, wr, f'Standard series with the appropriate substitution: {txt}.')


@R.add('ch12-st2', 'C2', (2, 4), 'explain')
def mac_valid_explain(rng, slot):
    kind = rng.choice(['ln', 'binom'])
    if kind == 'ln':
        c = rng.choice([3, 4, 5, 6, 10, 2.5])
        return mk(f'Explain why the Maclaurin series for ln(1 + x) cannot be used directly to evaluate ln {c:g}, and suggest how ln {c:g} could be found using series.',
                  f'x = {c - 1:g} is outside −1 < x ≤ 1; e.g. use ln((1 + x)/(1 − x)) with x = {P(sp.nsimplify((c - 1) / (c + 1)))}',
                  f'ln {c:g} needs x = {c - 1:g} (R1); the series converges only for −1 < x ≤ 1 (R1); a valid alternative such as ln((1 + x)/(1 − x)) = 2(x + x³/3 + …) with x = {P(sp.nsimplify((c - 1) / (c + 1)))} (A1).', 3, 'explain')
    a = rng.choice([2, 3, 4, 5]); v = rng.choice([sp.Rational(1, 2), sp.Rational(1, 3), 1])
    p_ = rng.choice([sp.Rational(1, 2), -1, -2, sp.Rational(-1, 2)])
    ok = abs(a * v) < 1
    return mk(f'Explain whether the Maclaurin series for (1 + {a}x)^({P(p_)}) can be used to approximate its value at x = {P(v)}.',
              f'{"yes" if ok else "no"}: the series is valid only for |x| < 1/{a}',
              f'Valid for |{a}x| < 1, i.e. |x| < 1/{a} (R1); at x = {P(v)}, |{a}x| = {P(a * v)} {"<" if ok else "≥"} 1 (M1); so the series {"converges and can" if ok else "diverges and cannot"} be used (A1).', 3, 'explain')


@R.add('ch12-st2', 'C4', (3, 5), 'multi_step', style='ext')
def mac_ln_ratio_parts(rng, slot):
    m = sp.sympify(rng.choice([2, 3, sp.Rational(3, 2), sp.Rational(5, 3), 5]))
    xv = (m - 1) / (m + 1)
    k = rng.choice([2, 3])
    terms = sum(2 * xv ** (2 * j + 1) / (2 * j + 1) for j in range(k))
    approx = float(terms)
    true = math.log(float(m))
    parts = [('Write down the first four terms of the Maclaurin series for ln(1 + x).', 'x − x²/2 + x³/3 − x⁴/4', 'A1', 1, True),
             ('Hence find the first four terms of the Maclaurin series for ln(1 − x).', '−x − x²/2 − x³/3 − x⁴/4', 'replace x by −x (M1) A1', 2, True),
             ('Show that ln((1 + x)/(1 − x)) = 2x + (2/3)x³ + (2/5)x⁵ + …', 'shown', 'subtract (M1); even powers cancel (A1) AG', 2, True),
             (f'Find the value of x for which (1 + x)/(1 − x) = {P(m)}.', P(xv), 'solve (M1) A1', 2, True),
             (f'Hence use the first {k} non-zero terms to approximate ' + (f'ln {P(m)}' if m.is_Integer else f'ln({P(m)})') + ', giving your answer to 5 decimal places.', f'{approx:.5f}', 'substitute (M1) A1', 2, True),
             ('Find the percentage error of this approximation.', f'{s3(abs(true - approx) / true * 100)}%', 'M1 A1', 2, False)]
    lnm = f'ln {P(m)}' if m.is_Integer else f'ln({P(m)})'
    return build_parts(rng, [f'This question uses Maclaurin series to approximate {lnm}.', 'In this question, logarithms are approximated using Maclaurin series.'], parts, 4)


@R.add('ch12-st2', 'C4', (4, 5), 'multi_step', style='p3')
def mac_sqrt_parts(rng, slot):
    A, d = rng.choice([(3, 1), (4, 1), (5, 1), (7, 1), (8, 1), (10, 1), (4, -1), (5, -1), (6, -1), (8, -1), (10, -1), (7, 2), (9, 2)])
    N = A * A + d
    u = sp.Rational(d, A * A)
    ser = 1 + u / 2 - u ** 2 / 8 + u ** 3 / 16
    approx = float(A * ser)
    true = math.sqrt(N)
    parts = [('Find the first four terms of the Maclaurin series for (1 + x)^(1/2).', '1 + x/2 − x²/8 + x³/16', 'binomial series with p = ½ (M1) A1 A1', 3, True),
             ('State the values of x for which the series is valid.', '|x| < 1', 'A1', 1, True),
             (f'Show that √{N} = {A}(1 {"+" if d > 0 else "−"} {P(abs(u))})^(1/2).', 'shown', f'{N} = {A * A}(1 {"+" if d > 0 else "−"} {P(abs(u))}) (M1) AG', 1, True),
             (f'Hence find an approximation for √{N}, giving your answer to 7 significant figures.', sfig(approx, 7), 'substitute x = ' + P(u) + ' (M1) A1', 2, True),
             ('Find the absolute error of this approximation.', sci(abs(true - approx)), 'GDC value (M1) A1', 2, True),
             (f'Explain why the square number {A * A} was chosen when rewriting √{N}.', f'x = {P(u)} is small, so the omitted terms are tiny and the series converges quickly', 'R1 R1', 2, False)]
    out = build_parts(rng, [f'This question investigates approximating square roots with the binomial series.', f'Maclaurin series can be used to approximate √{N} without a calculator.'], parts, 4)
    return out


# ---------------------------------------------------------------------------------------------
R.facts('ch12-st3', F(
    terms=[('substitution into a series', 'obtaining a new Maclaurin series by replacing x in a known series, e.g. e^(−x²) = 1 − x² + x⁴/2! − … from eˣ'),
           ('term-by-term integration', 'integrating each term of a power series to obtain the series of an antiderivative, e.g. arctan x from 1/(1 + x²)'),
           ('term-by-term differentiation', 'differentiating each term of a power series to obtain the series of the derivative, e.g. cos x from sin x')],
    facts=[('The Maclaurin series for e^(x²) begins', '1 + x² + x⁴/2', ['1 + x + x²/2', '1 + 2x + 2x²', 'x² + x⁴ + x⁶'], 'Substitute x² for x in eˣ.'),
           ('Integrating 1 − x² + x⁴ − … term by term gives the series of', 'arctan x', ['ln(1 + x)', 'sin x', 'arcsin x'], '∫ 1/(1 + x²) dx = arctan x.'),
           ('Differentiating the series for sin x gives the series for', 'cos x', ['−cos x', 'sin x', 'tan x'], 'd/dx sin x = cos x.'),
           ('The coefficient of x² in eˣ sin x is', '1', ['0', '1/2', '2'], '(1 + x + …)(x − …): x · x = x².')],
    why=[('Explain why the series for e^(−x²) can be used to approximate ∫ from 0 to 1 of e^(−x²) dx even though the integral has no elementary antiderivative.', 'The series 1 − x² + x⁴/2 − … converges for all x and can be integrated term by term; the resulting alternating series can be summed to any accuracy.'),
         ('Explain how series can be used to find lim as x → 0 of (sin x − x)/x³.', 'Replace sin x by x − x³/6 + x⁵/120 − …; the numerator becomes −x³/6 + …, so dividing by x³ gives −1/6 + (terms in x²) → −1/6.'),
         ('Explain why, when multiplying two series to find terms up to x³, you do not need terms beyond x³ in either series.', 'Any product involving a term of degree greater than 3 has degree greater than 3 (all terms have non-negative powers), so it does not affect coefficients up to x³.')],
    misc=[('The series for sin(2x) is 2x − 2x³/3! + 2x⁵/5! − …', 'Every x is replaced by 2x: 2x − (2x)³/3! + … = 2x − 8x³/6 + …'),
          ('To find the series of eˣ cos x, multiply the coefficients of the same powers: 1 + 0x − x²/2 + …', 'Products of all pairs of terms contribute: 1 + x + 0x² − x³/3 + …')],
))


def _sub_fn(rng):
    a = rng.choice([1, 2, 3])
    m = rng.choice([2, 3])
    u = rng.choice([1, -1]) * a * x ** m if m == 2 else rng.choice([1, -1]) * x ** 3
    base = rng.choice(['exp', 'sin', 'cos', 'ln', 'recip'])
    if base == 'exp':
        return sp.exp(u), f'eˣ with x replaced by {P(u)}'
    if base == 'sin':
        up = -u if u.could_extract_minus_sign() else u
        return sp.sin(up), f'sin x with x replaced by {P(up)}'
    if base == 'cos':
        up = -u if u.could_extract_minus_sign() else u
        return sp.cos(up), f'cos x with x replaced by {P(up)}'
    if base == 'ln':
        return sp.log(1 + u), f'ln(1 + x) with x replaced by {P(u)}'
    return 1 / (1 + u), f'(1 + x)⁻¹ with x replaced by {P(u)}'


@R.add('ch12-st3', 'C3', (1, 4), 'short', style='p1')
def mac_sub(rng, slot):
    f, how = _sub_fn(rng)
    k = 3
    txt, n = nonzero_terms(f, k, maxn=20)
    return mk(f'Use a standard Maclaurin series to find the first {k} non-zero terms of the series for {_ftxt(f)}.', txt,
              f'{how} (M1); {txt} (A1 A1 A1).', 4)


PROD_POOL = [lambda a, b: sp.exp(a * x) * sp.sin(b * x), lambda a, b: sp.exp(a * x) * sp.log(1 + b * x), lambda a, b: sp.exp(b * x) / (1 + a * x),
             lambda a, b: sp.cos(a * x) * sp.log(1 + b * x), lambda a, b: (1 + a * x) * sp.exp(b * x), lambda a, b: sp.sin(a * x) * sp.cos(b * x),
             lambda a, b: sp.exp(a * x) * sp.cos(b * x), lambda a, b: sp.sqrt(1 + a * x) * sp.exp(b * x)]


@R.add('ch12-st3', 'C3', (2, 5), 'short', style='p1')
def mac_prod(rng, slot):
    a, b = rng.choice([1, 2, -1, 3]), rng.choice([1, 2, 3, -1])
    f = rng.choice(PROD_POOL)(a, b)
    n = rng.choice([2, 3])
    txt = ser_txt(f, n)
    return mk(f'Find the Maclaurin series for {_ftxt(f)} up to and including the term in x{str(n).translate(_SUP)}.', txt,
              f'Write down both series to the required order (A1 A1); multiply, collecting all products up to x{str(n).translate(_SUP)} (M1); {txt} (A1 A1).', 5)


@R.add('ch12-st3', 'C3', (2, 5), 'short', style='p2')
def mac_int_approx(rng, slot):
    kind = rng.choice(['gauss', 'sinsq', 'sinc', 'cossq'])
    c = rng.choice([0.5, 0.3, 0.4, 0.6, 1.0, 0.8])
    k = rng.choice([2, 3])
    f = {'gauss': sp.exp(-x ** 2), 'sinsq': sp.sin(x ** 2), 'sinc': sp.sin(x) / x, 'cossq': sp.cos(x ** 2)}[kind]
    txt, n = nonzero_terms(f, k)
    poly = sp.series(f, x, 0, n + 1).removeO()
    approx = float(sp.integrate(poly, (x, 0, sp.nsimplify(c))))
    g = sp.lambdify(x, f, 'math')
    N = 2000
    hh = c / N
    true = sum(g((i + 0.5) * hh) for i in range(N)) * hh
    return mk(f'(a) Find the first {k} non-zero terms of the Maclaurin series for {P(f)}. (b) Hence find an approximation for ∫ from 0 to {c:g} of {P(f)} dx, giving your answer to 5 decimal places. (c) Find the percentage error compared with the GDC value.',
              f'(a) {txt} (b) {approx:.5f} (c) {sci(abs(true - approx) / true * 100)}%',
              f'(a) substitution into a standard series (M1); {txt} (A1). (b) integrate term by term (M1); limits (A1); {approx:.5f} (A1). (c) GDC {true:.6f} (A1); percentage error {sci(abs(true - approx) / true * 100)}% (A1).', 7)


@R.add('ch12-st3', 'C3', (2, 5), 'short', style='p1')
def mac_limit(rng, slot):
    a = rng.choice([1, 2, 3, 4])
    ax_ = '' if a == 1 else str(a)
    pool = [((sp.sin(a * x) - a * x) / x ** 3, f'(sin({ax_}x) − {ax_}x)/x³'), ((sp.exp(x ** 2) - 1 - x ** 2) / x ** 4, '(e^(x²) − 1 − x²)/x⁴'), ((1 - sp.cos(a * x)) / x ** 2, f'(1 − cos({ax_}x))/x²'),
            ((sp.log(1 + a * x) - a * x) / x ** 2, f'(ln(1 + {ax_}x) − {ax_}x)/x²'), ((x - sp.atan(x)) / x ** 3, '(x − arctan x)/x³'), ((sp.exp(a * x) - 1 - a * x) / (x * sp.sin(x)), f'(e^({ax_}x) − 1 − {ax_}x)/(x sin x)'),
            ((sp.cos(x) - 1 + x ** 2 / 2) / x ** 4, '(cos x − 1 + x²/2)/x⁴')]
    f, ft = rng.choice(pool)
    ft = ft.replace('(x)', ' x').replace('e^(x)', 'eˣ')
    v = sp.limit(f, x, 0)
    return mk(f'Use Maclaurin series to find lim as x → 0 of {ft}.', P(v),
              f'Substitute the series of the function(s) (M1 A1); simplify the numerator so the lowest power cancels with the denominator (M1); limit {P(v)} (A1).', 4)


@R.add('ch12-st3', 'C1', (1, 3), 'mcq')
def mac_sub_mcq(rng, slot):
    f, how = _sub_fn(rng)
    txt, n = nonzero_terms(f, 3, maxn=20)
    alts = []
    for g in (f.subs(x, -x), f.subs(x, 2 * x), sp.exp(x ** 2) if not f.has(sp.exp) else sp.cos(x ** 2), sp.sin(x ** 3), 1 / (1 - x ** 2)):
        t_, _ = nonzero_terms(g, 3, maxn=20)
        if t_ != txt and t_ not in alts:
            alts.append(t_)
    if len(alts) < 3:
        return None
    return mcq(rng, f'The first three non-zero terms of the Maclaurin series for {_ftxt(f)} are', txt, alts[:3], f'{how}.')


@R.add('ch12-st3', 'C2', (2, 4), 'explain')
def mac_ops_explain(rng, slot):
    kind = rng.choice(['diff', 'int', 'arctan'])
    a = rng.choice([1, 2, 3])
    if kind == 'diff':
        f = sp.log(1 + a * x)
        txt = ser_txt(f, 4)
        d = ser_txt(sp.diff(f, x), 3)
        return mk(f'Given that {_ftxt(f)} = {txt} + …, explain how to obtain the Maclaurin series for {_ftxt(sp.diff(f, x))} and write down its first four terms.', d,
                  f'd/dx {_ftxt(f)} = {_ftxt(sp.diff(f, x))} (R1); differentiate term by term (M1); {d} (A1).', 3, 'explain')
    if kind == 'int':
        f = sp.exp(-a * x ** 2)
        txt = ser_txt(f, 4)
        I = ser_txt(sp.integrate(sp.series(f, x, 0, 5).removeO(), x), 5)
        return mk(f'Explain how the Maclaurin series of {P(f)} can be used to find a series for ∫ from 0 to x of {P(f).replace("x", "t")} dt, and give the first three terms.', I,
                  f'Substitute {P(-a * x ** 2)} into the series for eˣ: {txt} (M1); integrate term by term from 0 to x (R1); {I} (A1).', 3, 'explain')
    return mk(f'Explain how the Maclaurin series for arctan x can be found from the series for 1/(1 + x²), and give the first three terms. Hence state the series for arctan({a if a > 1 else ""}x).'.replace('arctan(x)', 'arctan x'),
              ser_txt(sp.atan(a * x), 5), f'1/(1 + x²) = 1 − x² + x⁴ − … (A1); integrate term by term, constant 0 since arctan 0 = 0 (R1); substitute: {ser_txt(sp.atan(a * x), 5)} (A1).', 3, 'explain')


@R.add('ch12-st3', 'C4', (3, 5), 'multi_step', style='ext')
def arctan_pi_parts(rng, slot):
    k = rng.choice([3, 4, 5])
    xv, ang, lab = rng.choice([(1 / sp.sqrt(3), pi / 6, '1/√3'), (sp.Integer(1), pi / 4, '1')])
    S = sum((-1) ** j * xv ** (2 * j + 1) / (2 * j + 1) for j in range(k))
    mult = 6 if ang == pi / 6 else 4
    est = float(mult * S)
    parts = [('Write down the first four terms of the Maclaurin series for 1/(1 + x²).', '1 − x² + x⁴ − x⁶', 'replace x by x² in (1 + x)⁻¹ (M1) A1', 2, True),
             ('Hence find the first four non-zero terms of the Maclaurin series for arctan x.', 'x − x³/3 + x⁵/5 − x⁷/7', 'integrate term by term (M1); constant = 0 (R1) A1', 3, True),
             (f'By substituting x = {lab}, find an approximation for π using the first {k} non-zero terms. Give your answer to 5 decimal places.', f'{est:.5f}', f'arctan({lab}) = {P(ang)} (A1); multiply by {mult} (M1) A1', 3, True),
             ('Find the percentage error of this approximation.', f'{s3(abs(est - math.pi) / math.pi * 100)}%', 'M1 A1', 2, True),
             ('Explain why substituting x = 1/√3 gives a better approximation than x = 1 for the same number of terms.', 'terms decrease much faster because |x| < 1, so the series converges more quickly', 'R1 R1', 2, False)]
    return build_parts(rng, ['This question uses the Maclaurin series of arctan x to approximate π.', 'Series can be used to estimate π.'], parts, 4)


@R.add('ch12-st3', 'C4', (4, 5), 'multi_step', style='p3')
def gauss_int_parts(rng, slot):
    c = rng.choice([sp.Rational(1, 2), sp.Integer(1), sp.Rational(1, 3)])
    k = rng.choice([3, 4])
    terms = [(-1) ** j * c ** (2 * j + 1) / (sp.factorial(j) * (2 * j + 1)) for j in range(k + 1)]
    approx = float(sum(terms[:k]))
    bound = abs(float(terms[k]))
    true = float(sp.integrate(sp.exp(-x ** 2), (x, 0, c)).evalf())
    parts = [('Find the first four non-zero terms of the Maclaurin series for e^(−x²).', '1 − x² + x⁴/2 − x⁶/6', 'substitute −x² into eˣ (M1) A1', 2, True),
             (f'Hence show that ∫ from 0 to {P(c)} of e^(−x²) dx = Σ (−1)ⁿ({P(c)})^(2n+1)/(n!(2n + 1)).', 'shown', 'integrate term by term (M1); general term (A1) AG', 2, True),
             (f'Use the first {k} terms of this series to approximate the integral, giving your answer to 6 decimal places.', f'{approx:.6f}', 'M1 A1', 2, True),
             ('Use the alternating series estimation (the first omitted term) to give an upper bound for the error.', sci(bound), f'next term {P(abs(terms[k]))} (M1) A1', 2, True),
             ('Compare your approximation with the GDC value and comment.', f'GDC {true:.6f}; actual error {sci(abs(true - approx))} is below the bound', 'A1 R1', 2, False),
             ('Explain why the series converges for every value of the upper limit.', 'the series for eˣ converges for all real x, so the integrated series does too', 'R1', 1, False)]
    return build_parts(rng, [f'This question investigates approximating ∫ from 0 to {P(c)} of e^(−x²) dx.', 'The function e^(−x²) has no elementary antiderivative; series are used instead.'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch12-st4', F(
    terms=[('Maclaurin series from a differential equation', 'finding y(0), y′(0), y″(0), … by repeatedly differentiating the equation (implicitly) and substituting the initial condition'),
           ('implicit differentiation of a differential equation', 'differentiating both sides of dy/dx = f(x, y) with respect to x, using the chain rule on terms in y')],
    facts=[('If dy/dx = x + y and y(0) = 1, then y″(0) =', '2', ['1', '0', '3'], "y″ = 1 + y′, and y′(0) = 1."),
           ('Differentiating dy/dx = y² with respect to x gives', 'd²y/dx² = 2y dy/dx', ['d²y/dx² = 2y', 'd²y/dx² = y²', 'd²y/dx² = 2 dy/dx'], 'Chain rule on y².'),
           ('The coefficient of x² in the Maclaurin series of y is', 'y″(0)/2', ['y″(0)', 'y′(0)/2', '2y″(0)'], 'f⁽ⁿ⁾(0)/n!.')],
    why=[('Explain why a Maclaurin series can be found for the solution of a differential equation even when the equation cannot be solved exactly.', 'Only the values of the derivatives at x = 0 are needed; these come from the equation and the initial condition by repeated differentiation, without solving for y.'),
         ('Explain why the chain rule is needed when differentiating dy/dx = xy² to find d²y/dx².', 'y is a function of x, so d/dx(y²) = 2y dy/dx; combined with the product rule this gives d²y/dx² = y² + 2xy dy/dx.')],
    misc=[('From dy/dx = x + y², differentiating gives d²y/dx² = 1 + 2y.', 'd/dx(y²) = 2y dy/dx, so d²y/dx² = 1 + 2y dy/dx.')],
))


def de_series(f, y0, n):
    """Values y(0), y'(0), ..., y^(n)(0) for dy/dx = f(x, y), y(0) = y0, and the derivative expressions."""
    Y = sp.Function('Y')(x)
    e = f.subs(y, Y)
    exprs = [Y, e]
    vals = [sp.nsimplify(y0)]
    cur = e
    for _ in range(2, n + 1):
        cur = sp.expand(sp.diff(cur, x).subs(sp.Derivative(Y, x), e))
        exprs.append(cur)
    for ex_ in exprs[1:]:
        vals.append(sp.simplify(ex_.subs(Y, sp.nsimplify(y0)).subs(x, 0)))
    D1, D2 = sp.Symbol('zD1'), sp.Symbol('zD2')
    raw = [Y, e] + [sp.expand(sp.diff(e, x, j)) for j in range(1, n)]
    pretty = []
    for ex_ in raw:
        ex_ = ex_.subs(sp.Derivative(Y, (x, 2)), D2).subs(sp.Derivative(Y, x), D1).subs(Y, y)
        t_ = P(ex_).replace('zD1²', '(dy/dx)²').replace('zD1', ' dy/dx').replace('zD2', ' d²y/dx²').replace('( ', '(').replace('  ', ' ')
        t_ = re.sub(r'(^|[\s(−])\s?(\d*) dy/dx', lambda m_: m_.group(1) + (m_.group(2) + ' ' if m_.group(2) else '') + 'dy/dx', t_).strip()
        pretty.append(t_)
    return vals, pretty


def _de_f(rng):
    a, b = rng.choice([1, 2, 3]), rng.choice([1, 2, -1])
    return rng.choice([x + y ** 2, x * y + a, sp.exp(x) + b * y, sp.sin(x) + y, y ** 2 - a * x, a * x + b * y, x ** 2 + y ** 2, 1 + x * y ** 2, x - y ** 2, sp.cos(x) * y])


@R.add('ch12-st4', 'C3', (2, 5), 'short', style='p1')
def mac_de(rng, slot):
    f = _de_f(rng)
    y0 = rng.choice([0, 1, 2, -1])
    n = 3 if slot.d >= 3 else 2
    vals, pr = de_series(f, y0, n)
    poly = sum(vals[j] * x ** j / sp.factorial(j) for j in range(n + 1))
    if poly == 0:
        return None
    txt = ser_txt(poly, n)
    names = ['y(0)', 'y′(0)', 'y″(0)', 'y‴(0)']
    return mk(f'The function y = f(x) satisfies dy/dx = {P(f)} and y = {y0} when x = 0. Find the Maclaurin series for y up to and including the term in x{str(n).translate(_SUP)}.', txt,
              f'y′(0) = {P(vals[1])} (A1); d²y/dx² = {pr[2]} (M1 A1); y″(0) = {P(vals[2])} (A1)' + (f'; d³y/dx³ = {pr[3]} (M1); y‴(0) = {P(vals[3])} (A1)' if n == 3 else '') + f'; y ≈ {txt} (A1).', 7 if n == 3 else 5)


@R.add('ch12-st4', 'C1', (1, 3), 'mcq')
def mac_de_mcq(rng, slot):
    f = _de_f(rng)
    y0 = rng.choice([1, 2, -1])
    vals, pr = de_series(f, y0, 2)
    right = P(vals[2])
    wr = [P(w) for w in {vals[1], vals[2] + 1, vals[2] - 1, 2 * vals[2], f.subs({x: 0, y: y0}) * 0 + vals[1] * 2} if P(w) != right]
    wr = list(dict.fromkeys(wr))[:3]
    if len(wr) < 3:
        return None
    return mcq(rng, f'Given dy/dx = {P(f)} with y(0) = {y0}, the value of d²y/dx² at x = 0 is', right, wr, f'd²y/dx² = {pr[2]}; substitute x = 0, y = {y0}, y′(0) = {P(vals[1])}.')


@R.add('ch12-st4', 'C2', (2, 4), 'explain')
def mac_de_explain(rng, slot):
    f = _de_f(rng)
    vals, pr = de_series(f, 1, 2)
    return mk(f'Explain how to find d²y/dx² for the differential equation dy/dx = {P(f)}, and state the result in terms of x, y and dy/dx.', f'd²y/dx² = {pr[2]}',
              f'Differentiate both sides with respect to x (M1); treat y as a function of x, using the chain/product rule on y-terms (R1); d²y/dx² = {pr[2]} (A1).', 3, 'explain')


@R.add('ch12-st4', 'C4', (3, 5), 'multi_step', style='ext')
def mac_de_parts(rng, slot):
    f = _de_f(rng)
    y0 = rng.choice([1, 2, 0])
    vals, pr = de_series(f, y0, 3)
    poly = sum(vals[j] * x ** j / sp.factorial(j) for j in range(4))
    if poly == 0 or vals[3] == 0:
        return None
    xv = rng.choice([0.1, 0.2])
    est = float(poly.subs(x, xv))
    g = sp.lambdify((x, y), f, 'math')
    # RK4 reference value
    hh, yy, xx = xv / 200, float(y0), 0.0
    for _ in range(200):
        k1 = g(xx, yy); k2 = g(xx + hh / 2, yy + hh * k1 / 2); k3 = g(xx + hh / 2, yy + hh * k2 / 2); k4 = g(xx + hh, yy + hh * k3)
        yy += hh * (k1 + 2 * k2 + 2 * k3 + k4) / 6; xx += hh
    parts = [('Find the value of dy/dx when x = 0.', P(vals[1]), 'A1', 1, True),
             ('Show that d²y/dx² = ' + pr[2] + '.', 'shown', 'implicit differentiation (M1) A1 AG', 2, True),
             ('Find d³y/dx³ in terms of x, y and their derivatives.', pr[3], 'M1 A1', 2, True),
             ('Hence find the Maclaurin series for y up to and including the term in x³.', ser_txt(poly, 3), f'y″(0) = {P(vals[2])}, y‴(0) = {P(vals[3])} (A1 A1); series (A1)', 3, True),
             (f'Use your series to estimate y({xv}).', sfig(est, 4), 'M1 A1', 2, False),
             (f'A numerical method gives y({xv}) ≈ {sfig(yy, 5)}. Comment on the accuracy of your estimate.', f'close agreement, error ≈ {sci(abs(yy - est))}', 'R1', 1, False)]
    return build_parts(rng, [f'Consider the differential equation dy/dx = {P(f)}, with y = {y0} when x = 0.', f'A curve y = f(x) passes through (0, {y0}) and satisfies dy/dx = {P(f)}.'], parts, 4)


# =============================================================================================
# ch13 Mathematical exploration (IA) and Paper 3 problem-solving
# =============================================================================================
R.facts('ch13-st1', F(
    terms=[('mathematical exploration', 'the internal assessment: a written piece of 12 to 20 pages in which a student investigates an area of mathematics of their own choosing'),
           ('aim (of an exploration)', 'a clear, focused statement of what the exploration sets out to investigate, against which its success can be judged'),
           ('rationale', 'the explanation at the start of an exploration of why the topic was chosen and why it is of personal interest'),
           ('scope', 'the extent of the investigation: narrow enough to be explored in depth within 12 to 20 pages, broad enough to use mathematics commensurate with the course')],
    facts=[('The recommended length of the exploration is', '12 to 20 pages', ['6 to 10 pages', '25 to 30 pages', 'at least 40 pages'], 'Stated in the subject guide.'),
           ('The exploration is marked out of', '20', ['24', '30', '40'], 'Criteria A–E total 4 + 4 + 3 + 3 + 6.'),
           ('The internal assessment contributes', '20% of the final grade', ['30% of the final grade', '10% of the final grade', '50% of the final grade'], 'Both SL and HL.'),
           ('A good exploration aim is', 'focused and answerable with mathematics', ['as broad as possible', 'a historical summary of a topic', 'a list of formulae'], 'Focus allows depth.')],
    why=[('Explain why a narrowly focused aim usually leads to a better exploration than a broad one.', 'A focused aim can be investigated in depth within the page limit, allows sophisticated mathematics to be developed and makes it possible to reflect on whether the aim was achieved.'),
         ('Explain why the topic of an exploration should be of genuine personal interest to the student.', 'Personal interest drives independent thinking, creativity and ownership, which are rewarded under personal engagement, and sustains the effort needed to explore the mathematics in depth.'),
         ('Explain why a topic that is mainly historical or descriptive is not suitable for an exploration.', 'The exploration is assessed mainly on the student\'s own use of mathematics; describing the history of a result does not allow mathematics commensurate with the course to be applied and understood.')],
    contrast=[('a research report', 'a mathematical exploration', 'A research report summarises what others have found; an exploration requires the student to apply and develop mathematics themselves, making their own decisions and reflecting on them.'),
              ('the rationale', 'the aim', 'The rationale explains why the topic was chosen; the aim states precisely what the exploration will investigate.')],
    misc=[('My aim is to explore everything about the Fibonacci sequence.', 'This is far too broad: choose a specific question, e.g. investigating the limit of the ratio of consecutive terms and proving it equals the golden ratio.'),
          ('The more different topics I include, the higher my mark for use of mathematics.', 'Criterion E rewards relevant, correct mathematics commensurate with the course and demonstrated understanding, not the number of topics.')],
    evaluate=[('A student should choose an exploration topic that uses the most advanced mathematics possible.', ['sophisticated mathematics can score highly in criterion E', 'shows ambition and engagement'], ['mathematics beyond the student\'s understanding cannot be explained clearly', 'communication and reflection may suffer'], 'The mathematics should be commensurate with the course and genuinely understood; ambition is valuable only if the student can use and explain it correctly.'),
              ('Using real data always makes an exploration better.', ['real data can show personal engagement', 'allows modelling and critical reflection'], ['data collection can take over the exploration', 'pure mathematical topics can score full marks'], 'Real data helps only when it supports a clear mathematical aim; it is not required.')],
))

AIM_POOL = [  # interest, good aim, poor aims
    ('basketball', 'to model the trajectory of a free throw with a quadratic and find the launch angle that maximises the margin for error',
     ['to explore the history of basketball', 'to explain the rules of basketball', 'to list the statistics of famous players']),
    ('music', 'to investigate how Fourier series can approximate the waveform of a guitar string',
     ['to explore everything about music and mathematics', 'to describe how instruments are made', 'to write a biography of Pythagoras']),
    ('cryptography', 'to investigate the RSA algorithm and prove why decryption recovers the original message using modular arithmetic',
     ['to explore the history of codes', 'to describe how the Enigma machine looked', 'to list famous code breakers']),
    ('epidemics', 'to fit a logistic model to the early spread of an outbreak and evaluate its predictions',
     ['to describe the symptoms of diseases', 'to explore all of epidemiology', 'to report government policies']),
    ('architecture', 'to find the volume of a dome by modelling its profile with a function and using a volume of revolution',
     ['to describe famous buildings', 'to explore every shape in architecture', 'to discuss the history of domes']),
    ('running', 'to model the decrease of world-record times with distance using a power law and test its accuracy',
     ['to explain how to train for a marathon', 'to list the fastest runners', 'to explore all sports statistics']),
    ('art', 'to investigate the fractal dimension of the Koch snowflake and compare it with a coastline photograph',
     ['to describe paintings that contain patterns', 'to explore everything about fractals', 'to write about the life of Escher']),
    ('finance', 'to compare the total interest paid on a loan under different repayment schedules using geometric series',
     ['to describe how banks work', 'to explore the history of money', 'to give advice on investing']),
    ('games', 'to calculate the probability of winning a game of Snakes and Ladders within n moves using a Markov chain',
     ['to explain the rules of board games', 'to explore all games of chance', 'to describe the history of dice']),
    ('cooking', 'to model the cooling of a cake with Newton\'s law of cooling and determine the constant from measured data',
     ['to share favourite recipes', 'to describe kitchen equipment', 'to explore the chemistry of baking']),
    ('astronomy', 'to use Kepler\'s third law and regression on planetary data to estimate the orbital period of a dwarf planet',
     ['to describe the planets', 'to explore the whole of astronomy', 'to discuss the history of telescopes']),
    ('photography', 'to investigate how the depth of field depends on aperture using rational functions and derivatives',
     ['to describe types of camera', 'to explore the history of photography', 'to show my best photographs']),
    ('cycling', 'to optimise the gear ratio of a bicycle for a hill climb using calculus',
     ['to describe the Tour de France', 'to explain how bicycles are built', 'to explore all forms of transport']),
    ('voting', 'to compare the outcomes of plurality and Borda count voting on the same set of preferences and investigate when they differ',
     ['to describe election campaigns', 'to explore politics', 'to list election results']),
]

POOR_AIMS = [
    ('to explore the mathematics of everything in nature', 'far too broad to be investigated in depth', 'to investigate whether the spirals of a sunflower head follow consecutive Fibonacci numbers and model them with a polar equation'),
    ('to describe the history of calculus', 'historical and descriptive; no mathematics of the student\'s own is used', 'to compare Archimedes\' method of exhaustion for the area of a parabolic segment with integration'),
    ('to prove the Riemann hypothesis', 'unrealistic and far beyond the level of the course', 'to investigate the distribution of primes up to 10 000 and compare it with x/ln x'),
    ('to calculate the mean height of my class', 'too narrow and too elementary for mathematics commensurate with the course', 'to model the relationship between height and arm span and test the model with regression and residuals'),
    ('to show that mathematics is used in sport', 'vague, with no clear question that can be answered', 'to model the optimal angle for a long-jump take-off using projectile motion and calculus'),
    ('to learn about complex numbers', 'a learning goal, not an investigation with a clear outcome', 'to use complex numbers to find the coordinates of the vertices of regular polygons inscribed in a circle'),
    ('to look at the golden ratio in famous paintings', 'relies on measuring photographs without a mathematical question', 'to prove that the ratio of consecutive Fibonacci numbers tends to the golden ratio and investigate the rate of convergence'),
    ('to find out what happens to a bouncing ball', 'no clear mathematical focus or measurable aim', 'to model the heights of successive bounces with a geometric sequence and find the total distance travelled'),
    ('to explain how GPS works', 'largely descriptive physics and technology', 'to use vectors and systems of equations to locate a receiver from three sphere equations'),
    ('to investigate all types of probability distributions', 'too broad to explore in 12 to 20 pages', 'to test whether the number of goals per football match follows a Poisson distribution'),
    ('to summarise a YouTube video about π', 'reproduces someone else\'s work rather than the student\'s own', 'to compare the rates of convergence of two series that approximate π'),
    ('to see if maths is in music', 'vague and not answerable', 'to model the frequencies of notes in equal temperament with a geometric sequence and compare with just intonation'),
]

TOPIC_MATH = [
    ('the spread of a rumour on social media', 'logistic differential equation, separation of variables, parameter estimation', 'to model the number of shares of a post with a logistic model and estimate its carrying capacity'),
    ('the shape of a suspension bridge cable', 'functions, calculus (arc length), curve fitting', 'to compare a parabola and a catenary as models of a cable and find which fits better'),
    ('designing a drinks can', 'optimisation with derivatives, surface area and volume', 'to find the dimensions of a cylinder of fixed volume that minimise the surface area and compare with real cans'),
    ('the Monty Hall problem', 'conditional probability, Bayes\' theorem, simulation', 'to prove that switching doubles the probability of winning and generalise to n doors'),
    ('population of a city', 'exponential and logistic models, regression, residuals', 'to compare exponential and logistic models for a city\'s population and assess their predictions'),
    ('a roller coaster', 'piecewise functions, continuity and differentiability, calculus', 'to design a smooth track using piecewise polynomials that join with equal gradients'),
    ('medicine dosage', 'geometric series, exponential decay, limits', 'to model the long-term amount of a drug in the body under repeated doses'),
    ('the shape of a wine glass', 'volumes of revolution, curve fitting, integration', 'to model the profile of a glass with a polynomial and calculate its volume'),
    ('card shuffling', 'permutations, modular arithmetic, proof', 'to find how many perfect riffle shuffles return a deck of n cards to its original order'),
    ('coastline length', 'sequences, limits, logarithms (fractal dimension)', 'to estimate the fractal dimension of a coastline using the box-counting method'),
    ('traffic flow', 'differential equations, optimisation, modelling', 'to find the speed that maximises the flow of cars on a road using a density–speed model'),
    ('a satellite dish', 'conics, the reflective property of a parabola, calculus', 'to prove the reflective property of a parabola and find the focus of a real dish'),
    ('the birthday problem', 'probability, complementary events, approximation with exponentials', 'to find the smallest group size for which a shared birthday is more likely than not, and test an exponential approximation'),
    ('the growth of a plant', 'regression, logistic models, differential equations', 'to compare models for the height of a sunflower over time using data and residuals'),
    ('shadows and sundials', 'trigonometry, vectors, periodic functions', 'to model the length of a sundial\'s shadow over a day with a trigonometric function'),
    ('chess', 'combinatorics, recursion, proof by induction', 'to count the number of ways of placing n non-attacking rooks on an n × n board and prove the formula'),
]


@R.add('ch13-st1', 'C1', (1, 3), 'mcq')
def aim_mcq(rng, slot):
    interest, good, poor = rng.choice(AIM_POOL)
    nm = who(rng)
    return mcq(rng, f'{nm} is interested in {interest}. Which aim is most suitable for a mathematical exploration?', good[0].upper() + good[1:], [p_[0].upper() + p_[1:] for p_ in poor],
               'A suitable aim is focused, answerable with mathematics commensurate with the course, and allows personal engagement and reflection.')


@R.add('ch13-st1', 'C2', (2, 4), 'explain')
def aim_critique(rng, slot):
    aim, why_, better = rng.choice(POOR_AIMS)
    frame = rng.choice([f'A student proposes the exploration aim: "{aim[0].upper() + aim[1:]}". Explain why this aim is unsuitable and suggest an improved aim.',
                        f'{who(rng)} writes in their proposal: "My aim is {aim}." Comment on the suitability of this aim and suggest a better one.'])
    return mk(frame, f'Unsuitable: {why_}. Better: {better}.', f'Identifies the weakness: {why_} (R1); explains the effect on the assessment criteria, e.g. use of mathematics or reflection (R1); a focused, mathematical alternative such as "{better}" (A1).', 3, 'explain')


@R.add('ch13-st1', 'C3', (2, 4), 'short')
def topic_math(rng, slot):
    topic, maths, aim = rng.choice(TOPIC_MATH)
    frame = rng.choice([f'A student wants to write an exploration about {topic}. (a) Identify mathematics from the AA course that could be used. (b) Write a focused aim for the exploration.',
                        f'An exploration is planned on {topic}. Suggest relevant mathematics and state a precise aim that could be answered in 12 to 20 pages.'])
    return mk(frame, f'(a) {maths} (b) {aim[0].upper() + aim[1:]}', f'Relevant mathematics commensurate with the course: {maths} (A1 A1); focused, answerable aim (A1); the aim links to the mathematics identified (R1).', 4)


@R.add('ch13-st1', 'C3', (2, 4), 'short')
def topic_risk(rng, slot):
    topic, maths, aim = rng.choice(TOPIC_MATH)
    risk = rng.choice([('relying on data that is difficult to collect', 'use a published data set or a smaller experiment that can be repeated'),
                       ('the mathematics becoming too advanced to explain', 'restrict the aim to a case that can be fully understood and justified'),
                       ('the exploration becoming descriptive rather than mathematical', 'make every section answer part of the aim with calculations or proofs'),
                       ('the page limit being exceeded', 'remove repetitive calculations to an appendix or summarise them in a table')])
    return mk(f'A student plans an exploration with the aim "{aim}". Explain how the risk of {risk[0]} could affect this exploration, and how the student could reduce it.',
              f'Risk: {risk[0]}; mitigation: {risk[1]}', f'A risk specific to {topic} (A1); explanation of its impact on the criteria (R1); a realistic mitigation: {risk[1]} (A1).', 3)


@R.add('ch13-st1', 'C4', (3, 5), 'multi_step', style='ext')
def exploration_plan(rng, slot):
    topic, maths, aim = rng.choice(TOPIC_MATH)
    parts = [('Write a precise aim for the exploration.', aim[0].upper() + aim[1:], 'focused, answerable (A1 A1)', 2, True),
             ('Identify the mathematics that will be used and explain why it is appropriate.', maths, 'relevant mathematics (A1); justification (R1)', 2, True),
             ('Describe how personal engagement could be demonstrated.', 'own data, own questions, own approach, links to personal interest', 'R1 R1', 2, True),
             ('Explain how reflection could be shown throughout the exploration.', 'comment on results, limitations of the model, the meaning of the mathematics and possible extensions', 'R1 R1', 2, True),
             ('Identify one limitation of the approach and how it could be addressed.', 'e.g. simplifying assumptions in the model; test sensitivity or refine the model', 'R1 A1', 2, False),
             ('Suggest how technology could be used appropriately.', 'GDC/GeoGebra/spreadsheet for regression, graphs or iteration, with results interpreted', 'A1', 1, False)]
    return build_parts(rng, [f'A student is planning a mathematical exploration about {topic}.', f'Plan an exploration on the topic of {topic}.'], parts, 4)


# ---------------------------------------------------------------------------------------------
CRIT = {'A': ('Presentation', 4), 'B': ('Mathematical communication', 4), 'C': ('Personal engagement', 3), 'D': ('Reflection', 3), 'E': ('Use of mathematics', 6)}

R.facts('ch13-st2', F(
    terms=[('Criterion A: presentation', 'assesses the organisation and coherence of the exploration: a clear introduction, aim, development and conclusion, and conciseness (maximum 4 marks)'),
           ('Criterion B: mathematical communication', 'assesses the use of appropriate mathematical language, notation, symbols, terminology, multiple forms of representation and correctly defined key terms (maximum 4 marks)'),
           ('Criterion C: personal engagement', 'assesses the extent to which the student engages with the exploration and makes it their own, e.g. independent thinking, creativity, own questions (maximum 3 marks)'),
           ('Criterion D: reflection', 'assesses how the student reviews, analyses and evaluates the exploration, e.g. discussing implications of results, limitations and extensions (maximum 3 marks)'),
           ('Criterion E: use of mathematics', 'assesses the relevance, correctness and sophistication of the mathematics and the understanding demonstrated, commensurate with the course (maximum 6 marks)')],
    facts=[('The criterion with the greatest maximum mark is', 'E: use of mathematics (6 marks)', ['A: presentation (4 marks)', 'C: personal engagement (3 marks)', 'B: mathematical communication (4 marks)'], 'A 4, B 4, C 3, D 3, E 6.'),
           ('Using "x^2" instead of x² and "*" for multiplication mainly affects', 'Criterion B: mathematical communication', ['Criterion C: personal engagement', 'Criterion D: reflection', 'Criterion E: use of mathematics'], 'Notation is part of communication.'),
           ('At HL, the top band of criterion E requires mathematics that is', 'precise and demonstrates sophistication and rigour', ['taken from a textbook', 'entirely computer-generated', 'beyond the syllabus in every section'], 'HL descriptors include rigour and sophistication.'),
           ('Discussing the limitations of a model is credited mainly under', 'Criterion D: reflection', ['Criterion A: presentation', 'Criterion B: mathematical communication', 'Criterion E: use of mathematics'], 'Critical reflection.'),
           ('The maximum total mark for the exploration is', '20', ['24', '18', '30'], '4 + 4 + 3 + 3 + 6 = 20.')],
    why=[('Explain why "meaningful reflection" requires more than a concluding paragraph.', 'Reflection is credited when the student critically examines results throughout — linking them to the aim, considering limitations, accuracy and implications — not when a brief summary is added at the end.'),
         ('Explain why copying a sophisticated proof from a textbook may not score highly in criterion E.', 'Criterion E rewards demonstrated understanding; a reproduced proof without explanation, adaptation or application shows little of the student\'s own understanding.'),
         ('Explain why defining variables and key terms is important in an exploration.', 'Undefined variables make the mathematics ambiguous to a peer reader; criterion B requires key terms and variables to be defined so the work can be followed.')],
    contrast=[('Criterion A: presentation', 'Criterion B: mathematical communication', 'A concerns the structure and coherence of the whole document; B concerns the mathematical language, notation and representations used within it.'),
              ('Criterion C: personal engagement', 'Criterion D: reflection', 'C rewards making the exploration one\'s own (independent thinking, creativity); D rewards critically reviewing and evaluating results and the process.')],
    misc=[('Personal engagement is shown by saying how much I enjoyed the topic.', 'Statements of interest alone earn little; engagement is shown through independent thinking, own questions, own data and creative approaches.'),
          ('Including many graphs automatically scores full marks in mathematical communication.', 'Representations must be appropriate, labelled and referred to; unnecessary or unlabelled graphs can reduce the mark.')],
    evaluate=[('Use of mathematics is the only criterion that really matters in the exploration.', ['E carries the most marks (6 of 20)', 'mathematics is the purpose of the exploration'], ['A–D carry 14 of the 20 marks', 'poor communication can hide good mathematics'], 'E is the largest single criterion, but 70% of the marks reward presentation, communication, engagement and reflection, so all criteria matter.')],
))

FEATURES = [
    ('has no clear introduction or conclusion and the sections do not follow logically', 'A'), ('is 35 pages long with much repetition', 'A'),
    ('is well organised, concise and easy to follow', 'A'), ('includes a clear table of contents and the aim is stated at the start', 'A'),
    ('uses calculator notation such as 3*x^2 and E-05', 'B'), ('does not define the variables used in the model', 'B'),
    ('uses graphs without axes labels or units', 'B'), ('moves between algebraic, graphical and tabular representations appropriately', 'B'),
    ('collects its own data from a self-designed experiment', 'C'), ('asks and pursues the student\'s own questions beyond the textbook example', 'C'),
    ('follows a standard textbook investigation step by step', 'C'), ('shows creativity in choosing a novel approach to the problem', 'C'),
    ('discusses the limitations of the model and the effect of assumptions', 'D'), ('ends with a sentence saying the exploration was interesting', 'D'),
    ('critically compares two models and explains which is better and why', 'D'), ('considers possible extensions and the implications of the results', 'D'),
    ('contains a correct derivation of a result commensurate with the HL course', 'E'), ('has several errors in differentiation', 'E'),
    ('uses only mean, median and bar charts', 'E'), ('demonstrates a thorough understanding of why the method works', 'E'),
]


GOOD_FEATURES = {'is well organised, concise and easy to follow', 'includes a clear table of contents and the aim is stated at the start',
                 'moves between algebraic, graphical and tabular representations appropriately', 'collects its own data from a self-designed experiment',
                 'asks and pursues the student\'s own questions beyond the textbook example', 'shows creativity in choosing a novel approach to the problem',
                 'discusses the limitations of the model and the effect of assumptions', 'critically compares two models and explains which is better and why',
                 'considers possible extensions and the implications of the results', 'contains a correct derivation of a result commensurate with the HL course',
                 'demonstrates a thorough understanding of why the method works'}


@R.add('ch13-st2', 'C1', (1, 3), 'mcq')
def crit_mcq(rng, slot):
    feat, c = rng.choice(FEATURES)
    right = f'{c}: {CRIT[c][0]}'
    wr = [f'{k}: {v[0]}' for k, v in CRIT.items() if k != c]
    rng.shuffle(wr)
    return mcq(rng, f'An exploration {feat}. Which assessment criterion is most directly affected?', right, wr[:3], f'This is assessed under criterion {c} ({CRIT[c][0]}).')


@R.add('ch13-st2', 'C1', (1, 2), 'short')
def crit_max(rng, slot):
    c = rng.choice(list(CRIT))
    frame = rng.choice([f'State the maximum mark available for criterion {c} ({CRIT[c][0].lower()}) in the exploration.', f'Write down the number of marks available for {CRIT[c][0].lower()} (criterion {c}).'])
    return mk(frame, str(CRIT[c][1]), f'{CRIT[c][1]} (A1).', 1, 'short')


@R.add('ch13-st2', 'C2', (2, 4), 'explain')
def crit_explain(rng, slot):
    feat, c = rng.choice(FEATURES)
    good = feat in GOOD_FEATURES
    tail = 'explain why this would be credited' if good else 'explain how the student could improve it'
    return mk(f'An exploration {feat}. Identify the criterion most affected and {tail}.', f'Criterion {c} ({CRIT[c][0]})',
              f'Criterion {c}: {CRIT[c][0]} (A1); link the feature to the descriptor for this criterion (R1); ' + ('justification of why it meets a high band (R1).' if good else 'a specific, practical improvement (R1).'), 3, 'explain')


@R.add('ch13-st2', 'C3', (2, 5), 'short')
def crit_total(rng, slot):
    marks = {c: rng.randint(max(0, m - 3), m) for c, (n_, m) in CRIT.items()}
    tot = sum(marks.values())
    lvl = 'HL' if rng.random() < 0.6 else 'SL'
    w = 20
    contrib = tot / 20 * w
    worst = min(CRIT, key=lambda c: marks[c] / CRIT[c][1])
    if sum(1 for c in CRIT if marks[c] / CRIT[c][1] == marks[worst] / CRIT[worst][1]) > 1:
        return None
    desc = ', '.join(f'{c} {marks[c]}' for c in CRIT)
    return mk(f'An {lvl} student\'s exploration is awarded: {desc}. (a) Find the total mark. (b) The exploration is worth {w}% of the final assessment; find the percentage of the overall course mark gained. (c) Identify the criterion in which the student achieved the lowest proportion of the available marks.',
              f'(a) {tot}/20 (b) {s3(contrib)}% (c) {worst} ({CRIT[worst][0]}): {marks[worst]}/{CRIT[worst][1]}',
              f'(a) {" + ".join(str(marks[c]) for c in CRIT)} = {tot} (A1). (b) {tot}/20 × {w} (M1) = {s3(contrib)}% (A1). (c) compare mark/maximum for each criterion (M1); {worst} with {marks[worst]}/{CRIT[worst][1]} (A1).', 5)


AWARD = [
    ('A', 'The exploration has an introduction and conclusion, but the middle sections jump between ideas and some calculations are repeated several times.', '2', 'some coherence but not well organised or concise'),
    ('A', 'The exploration is coherent, well organised and concise, with a clear aim and conclusion.', '4', 'meets every element of the top descriptor'),
    ('B', 'Notation is mostly correct, but several variables are not defined and one graph has no labels.', '2', 'some relevant notation, but key terms not consistently defined'),
    ('B', 'Mathematical language is precise throughout, multiple representations are used appropriately and all key terms are defined.', '4', 'consistently appropriate and precise communication'),
    ('C', 'The student collects their own data and asks their own questions, but the approach closely follows a published example.', '2', 'significant but not outstanding engagement'),
    ('C', 'There is little evidence of independent thinking; the work mirrors a textbook example.', '1', 'limited personal engagement'),
    ('C', 'The student develops an original approach, explores their own questions and shows creativity throughout.', '3', 'abundant evidence of outstanding personal engagement'),
    ('D', 'The only reflection is a final paragraph stating that the aim was achieved.', '1', 'limited, superficial reflection'),
    ('D', 'Limitations of the model are discussed after each stage, and results are linked back to the aim and to possible extensions.', '3', 'substantial, critical reflection throughout'),
    ('E', 'The mathematics is relevant and mostly correct, at the level of the course, with some understanding demonstrated.', '3', 'relevant, partially correct, some understanding'),
    ('E', 'HL mathematics is used correctly with thorough understanding, and the work is precise, rigorous and sophisticated.', '6', 'top HL descriptor: correct, thorough understanding, rigour and sophistication'),
    ('E', 'The mathematics is mostly correct and relevant but contains a significant error in an integral, and understanding is only partly shown.', '2', 'relevant mathematics with significant errors'),
]


@R.add('ch13-st2', 'C3', (2, 4), 'short')
def crit_award(rng, slot):
    c, desc, m, why_ = rng.choice(AWARD)
    frame = rng.choice([f'Criterion {c} ({CRIT[c][0].lower()}) is marked out of {CRIT[c][1]}. {desc} Suggest a mark for this criterion and justify it.',
                        f'A teacher reads the following comment about criterion {c} ({CRIT[c][0].lower()}): "{desc}" Suggest the mark out of {CRIT[c][1]} and give a reason.'])
    return mk(frame, f'{m}/{CRIT[c][1]}: {why_}', f'Mark {m} (±1 accepted with justification) (A1); justification linked to the descriptor: {why_} (R1 R1).', 3)


@R.add('ch13-st2', 'C4', (3, 5), 'multi_step', style='ext')
def moderation_parts(rng, slot):
    pick_ = {c: rng.choice([a_ for a_ in AWARD if a_[0] == c]) for c in CRIT}
    order = list(CRIT)
    summary = ' '.join(f'{c}: {pick_[c][1]}' for c in order)
    tot = sum(int(pick_[c][2]) for c in order)
    parts = [(f'Suggest a mark for criterion {c} ({CRIT[c][0].lower()}), out of {CRIT[c][1]}, and justify it.', f'{pick_[c][2]}/{CRIT[c][1]}: {pick_[c][3]}', 'A1 R1', 2, True) for c in order]
    parts.append(('Find the total mark for the exploration based on your suggested marks.', f'{tot}/20', 'A1', 1, True))
    lo = min(int(pick_[c][2]) / CRIT[c][1] for c in order)
    weak = [c for c in order if int(pick_[c][2]) / CRIT[c][1] == lo]
    wtxt = ' or '.join(f'{c} ({CRIT[c][0].lower()})' for c in weak)
    parts.append(('Recommend, with a reason, the single change that would most improve the mark.', f'improve criterion {wtxt}, where the lowest proportion of marks was gained', 'identify lowest proportion (R1); specific improvement (R1)', 2, True))
    return build_parts(rng, [f'A teacher summarises an exploration as follows. {summary}', f'Notes made while marking an exploration: {summary}'], parts, 4)


# ---------------------------------------------------------------------------------------------
R.facts('ch13-st3', F(
    terms=[('conjecture', 'a statement believed to be true on the basis of evidence, such as a pattern in calculated cases, but not yet proved'),
           ('proof by induction', 'proving P(n) for all n ≥ n₀ by showing P(n₀) is true and that P(k) true implies P(k + 1) true'),
           ('counterexample', 'a single case that shows a general statement is false'),
           ('generalisation', 'extending a result found for particular cases to a wider family, e.g. replacing a number by a parameter')],
    facts=[('Checking a formula for n = 1, 2, …, 10', 'does not prove it holds for all n', ['proves it for all n', 'proves it for all n ≤ 100', 'is a proof by induction'], 'Patterns can fail later.'),
           ('The number of regions formed by joining n points on a circle begins 1, 2, 4, 8, 16. The next value is', '31', ['32', '30', '24'], 'C(n,4) + C(n,2) + 1: the doubling pattern fails.'),
           ('The inductive step of a proof by induction shows that', 'if P(k) is true then P(k + 1) is true', ['P(k + 1) is true for one value of k', 'P(1) is true', 'P(k) is true for all k'], 'Together with the base case.'),
           ('To disprove "n² − n + 41 is prime for all n ∈ ℕ" it is enough to', 'find one value of n for which it is composite', ['check n = 1 to 40', 'use induction', 'show it is prime for n = 41'], 'n = 41 gives 41².')],
    why=[('Explain why the pattern 1, 2, 4, 8, 16 for the number of regions in a circle does not prove that the number of regions is 2ⁿ⁻¹.', 'Finitely many cases cannot establish a general rule; in fact the sixth value is 31, not 32, so the conjecture is false.'),
         ('Explain the role of the base case and the inductive step in a proof by induction.', 'The base case shows the statement is true for the first value; the inductive step shows truth for any k implies truth for k + 1; together they give truth for every integer from the base value onwards.'),
         ('Explain why Paper 3 questions often ask you to test a conjecture on further cases before proving it.', 'Testing builds confidence and can reveal a counterexample early; it also suggests the structure that the general proof must follow.')],
    misc=[('Since the formula works for n = 1, 2 and 3 it is true for all positive integers.', 'Checking cases is evidence, not proof; a general argument such as induction is required.'),
          ('In the inductive step I assume P(k + 1) is true and show P(k) is true.', 'The direction is reversed: assume P(k) and deduce P(k + 1).')],
))


def _family(rng):
    """(description of S(n), python function n -> value, closed form text, sympy closed form in n, induction hint)."""
    n_ = sp.Symbol('n', positive=True, integer=True)
    kind = rng.choice(['odd', 'kk1', 'tele', 'diag', 'lines', 'kfact', 'cubes', 'geo', 'k2k', 'deriv', 'hand', 'arith'])
    if kind == 'odd':
        return 'the sum of the first n odd numbers, Sₙ = 1 + 3 + … + (2n − 1)', lambda m: m * m, 'Sₙ = n²', n_ ** 2, 'Sₖ₊₁ = k² + (2k + 1) = (k + 1)²'
    if kind == 'kk1':
        return 'Sₙ = 1×2 + 2×3 + … + n(n + 1)', lambda m: sum(j * (j + 1) for j in range(1, m + 1)), 'Sₙ = n(n + 1)(n + 2)/3', n_ * (n_ + 1) * (n_ + 2) / 3, 'k(k + 1)(k + 2)/3 + (k + 1)(k + 2) = (k + 1)(k + 2)(k + 3)/3'
    if kind == 'tele':
        return 'Sₙ = 1/(1×2) + 1/(2×3) + … + 1/(n(n + 1))', lambda m: sum(Fr(1, j * (j + 1)) for j in range(1, m + 1)), 'Sₙ = n/(n + 1)', n_ / (n_ + 1), 'k/(k + 1) + 1/((k + 1)(k + 2)) = (k + 1)/(k + 2)'
    if kind == 'diag':
        return 'Dₙ, the number of diagonals of a convex polygon with n + 3 sides', lambda m: (m + 3) * m // 2, 'Dₙ = n(n + 3)/2', n_ * (n_ + 3) / 2, 'adding a vertex adds n + 2 diagonals'
    if kind == 'lines':
        return 'Rₙ, the maximum number of regions into which n straight lines divide the plane', lambda m: (m * m + m + 2) // 2, 'Rₙ = (n² + n + 2)/2', (n_ ** 2 + n_ + 2) / 2, 'the (k + 1)th line crosses k lines, adding k + 1 regions'
    if kind == 'kfact':
        return 'Sₙ = 1×1! + 2×2! + … + n×n!', lambda m: sum(j * math.factorial(j) for j in range(1, m + 1)), 'Sₙ = (n + 1)! − 1', sp.factorial(n_ + 1) - 1, '(k + 1)! − 1 + (k + 1)(k + 1)! = (k + 2)! − 1'
    if kind == 'cubes':
        return 'Sₙ = 1³ + 2³ + … + n³', lambda m: sum(j ** 3 for j in range(1, m + 1)), 'Sₙ = n²(n + 1)²/4', n_ ** 2 * (n_ + 1) ** 2 / 4, 'k²(k + 1)²/4 + (k + 1)³ = (k + 1)²(k + 2)²/4'
    if kind == 'geo':
        r = rng.choice([2, 3, 4, 5])
        return f'Sₙ = 1 + {r} + {r}² + … + {r}ⁿ⁻¹', lambda m, r=r: sum(r ** j for j in range(m)), f'Sₙ = ({r}ⁿ − 1)/{r - 1}'.replace('/1', ''), (r ** n_ - 1) / (r - 1), f'Sₖ + {r}ᵏ = ({r}ᵏ⁺¹ − 1)/{r - 1}'.replace('/1', '')
    if kind == 'k2k':
        return 'Sₙ = 1×2 + 2×2² + … + n×2ⁿ', lambda m: sum(j * 2 ** j for j in range(1, m + 1)), 'Sₙ = (n − 1)2ⁿ⁺¹ + 2', (n_ - 1) * 2 ** (n_ + 1) + 2, '(k − 1)2ᵏ⁺¹ + 2 + (k + 1)2ᵏ⁺¹ = k·2ᵏ⁺² + 2'
    if kind == 'deriv':
        a = rng.choice([1, 2, 3])
        ax = f'{a}x' if a > 1 else 'x'
        return f'fₙ(0), where fₙ(x) is the nth derivative of x e^({ax})'.replace('e^(x)', 'eˣ'), lambda m, a=a: int(sp.diff(x * sp.exp(a * x), x, m).subs(x, 0)), (f'fₙ(0) = n·{a}ⁿ⁻¹' if a > 1 else 'fₙ(0) = n'), n_ * a ** (n_ - 1), f'fₙ(x) = {a}ⁿ⁻¹({ax} + n)e^({ax}); differentiate once more'.replace('1ⁿ⁻¹', '').replace('e^(x)', 'eˣ')
    if kind == 'hand':
        return 'Hₙ, the number of handshakes when each of n + 1 people shakes hands once with every other person', lambda m: (m + 1) * m // 2, 'Hₙ = n(n + 1)/2', n_ * (n_ + 1) / 2, 'a new person shakes hands with all n + 1 others'
    a, d = rng.randint(2, 6), rng.randint(2, 5)
    return f'Sₙ = {a} + {a + d} + {a + 2 * d} + … (n terms)', lambda m, a=a, d=d: sum(a + j * d for j in range(m)), f'Sₙ = n({2 * a - d} + {d}n)/2'.replace('+ -', '− '), n_ * (2 * a - d + d * n_) / 2, f'add the (k + 1)th term {a} + {d}k'


def _fv(v):
    return str(v) if not isinstance(v, Fr) else (f'{v.numerator}/{v.denominator}' if v.denominator != 1 else str(v.numerator))


@R.add('ch13-st3', 'C3', (2, 5), 'short', style='p1')
def pattern_compute(rng, slot):
    desc, fn, form, expr, hint = _family(rng)
    n_ = list(expr.free_symbols)[0] if expr.free_symbols else sp.Symbol('n')
    vals = [fn(m) for m in range(1, 6)]
    for m in range(1, 6):
        if sp.nsimplify(expr.subs(n_, m)) != sp.nsimplify(str(_fv(vals[m - 1]))):
            return None
    N = rng.choice([10, 12, 15, 20, 25])
    vN = sp.nsimplify(expr.subs(n_, N))
    return mk(f'Consider {desc}. (a) Find the values for n = 1, 2, 3, 4 and 5. (b) Conjecture a formula in terms of n. (c) Use your formula to find the value when n = {N}.',
              f'(a) {", ".join(_fv(v) for v in vals)} (b) {form} (c) {P(vN)}', f'(a) values (A1 A1). (b) pattern recognised (M1); {form} (A1). (c) substitute n = {N} (M1); {P(vN)} (A1).', 6)


@R.add('ch13-st3', 'C1', (1, 3), 'mcq')
def pattern_mcq(rng, slot):
    desc, fn, form, expr, hint = _family(rng)
    vals = [fn(m) for m in range(1, 5)]
    others = []
    for _ in range(20):
        d2 = _family(rng)
        if d2[2] != form and d2[2] not in others and [d2[1](m) for m in range(1, 3)] != vals[:2]:
            others.append(d2[2])
        if len(others) == 3:
            break
    if len(others) < 3:
        return None
    return mcq(rng, f'For {desc}, the first four values are {", ".join(_fv(v) for v in vals)}. Which formula fits?', form, others, f'{form} gives {", ".join(_fv(v) for v in vals)}.')


@R.add('ch13-st3', 'C2', (2, 4), 'explain')
def pattern_proof_explain(rng, slot):
    desc, fn, form, expr, hint = _family(rng)
    m = rng.choice([5, 6, 8, 10])
    return mk(f'A student checks that {form} for {desc} is correct for n = 1, 2, …, {m} and claims this proves it. Explain why this is not a proof and outline how the result could be proved.',
              'checking finitely many cases is not a proof; use induction', f'Finitely many cases do not establish the result for all n (R1); base case n = 1 (M1); inductive step: {hint} (R1).', 3, 'explain')


@R.add('ch13-st3', 'C4', (4, 5), 'multi_step', style='p3')
def investigation_parts(rng, slot):
    desc, fn, form, expr, hint = _family(rng)
    n_ = list(expr.free_symbols)[0]
    vals = [fn(m) for m in range(1, 6)]
    for m in range(1, 6):
        if sp.nsimplify(expr.subs(n_, m)) != sp.nsimplify(str(_fv(vals[m - 1]))):
            return None
    M = rng.choice([100, 500, 1000, 5000])
    big = next((m for m in range(1, 400) if sp.nsimplify(expr.subs(n_, m)) > M), None)
    parts = [('Find the values for n = 1, 2, 3, 4 and 5.', ', '.join(_fv(v) for v in vals), 'A1 A1', 2, True),
             ('Conjecture a formula in terms of n.', form, 'M1 A1', 2, True),
             ('Prove your conjecture by mathematical induction.', 'proof', f'base case (A1); assume true for n = k (M1); {hint} (M1 A1); conclusion (R1)', 5, True),
             (f'Find the smallest n for which the value exceeds {M}.', str(big) if big else 'none for n < 400', 'set up inequality (M1) A1', 2, big is not None),
             ('Describe one way in which the result could be generalised, and state the generalised result if possible.', 'e.g. replace a fixed number by a parameter and repeat the investigation', 'R1 R1', 2, False)]
    return build_parts(rng, [f'This question investigates {desc}.', f'In this question you will investigate {desc} and prove a general result.'], parts, 4)


@R.add('ch13-st3', 'C4', (4, 5), 'multi_step', style='p3')
def circle_regions_parts(rng, slot):
    kind = rng.choice(['circle', 'prime'])
    if kind == 'circle':
        nmax = rng.choice([6, 7])
        vals = [math.comb(m, 4) + math.comb(m, 2) + 1 for m in range(1, nmax + 1)]
        parts = [('Write down the number of regions for n = 1, 2, 3, 4 and 5 points.', ', '.join(map(str, vals[:5])), 'A1 A1', 2, True),
                 ('State a conjecture suggested by these values.', 'Rₙ = 2ⁿ⁻¹', 'A1', 1, True),
                 (f'Given that the number of regions is C(n, 4) + C(n, 2) + 1, find the value for n = {nmax} and comment on your conjecture.', f'{vals[-1]}; the conjecture is false (2ⁿ⁻¹ = {2 ** (nmax - 1)})', 'M1 A1 R1', 3, True),
                 ('Explain why C(n, 4) + C(n, 2) + 1 counts the regions.', 'each set of 4 points gives one interior intersection; each chord and each intersection adds a region', 'R1 R1', 2, False),
                 ('Show that the formula can be written as (n⁴ − 6n³ + 23n² − 18n + 24)/24.', 'shown', 'expand (M1) A1 AG', 2, True)]
        return build_parts(rng, ['Points are placed on a circle and every pair is joined by a chord, with no three chords meeting at a point. Let Rₙ be the number of regions formed inside the circle for n points.',
                                 'This question investigates the regions formed by chords between n points on a circle (in general position).'], parts, 4)
    a = rng.choice([41, 17, 11])
    vals = [m * m - m + a for m in range(1, 6)]
    fail = next(m for m in range(1, 200) if not sp.isprime(m * m - m + a))
    parts = [(f'Find f(n) = n² − n + {a} for n = 1, …, 5 and verify that each value is prime.', ', '.join(map(str, vals)), 'A1 A1', 2, True),
             ('A student conjectures that f(n) is prime for every positive integer n. Without a calculator, show that the conjecture is false.', f'f({a}) = {a}² is not prime', f'f({a}) = {a}({a} − 1) + {a} = {a}² (M1 A1)', 2, True),
             ('Find the smallest positive integer n for which f(n) is not prime.', str(fail), 'systematic search with technology (M1) A1', 2, True),
             ('Explain why no polynomial with integer coefficients and positive leading coefficient can be prime for every positive integer n.', 'if f(1) = p then f(1 + mp) ≡ f(1) ≡ 0 (mod p), and f(1 + mp) > p for large m', 'R1 R1 R1', 3, False)]
    return build_parts(rng, [f'This question explores the "prime-generating" polynomial n² − n + {a}.', f'Let f(n) = n² − n + {a}, n ∈ ℤ⁺.'], parts, 3)


# ---------------------------------------------------------------------------------------------
R.facts('ch13-st4', F(
    terms=[('graphical display calculator (GDC)', 'a calculator used to graph functions, solve equations numerically, find intersections, maxima and integrals, and perform regression'),
           ('dynamic geometry software', 'software such as GeoGebra in which objects can be constructed and dragged so that conjectures can be tested on many cases'),
           ('spreadsheet', 'a grid of cells in which formulae can be copied to compute sequences, iterations or tables of values quickly')],
    facts=[('A spreadsheet is most efficient for', 'computing many terms of an iteration xₙ₊₁ = g(xₙ)', ['proving a result by induction', 'sketching an exact graph', 'finding an exact surd value'], 'Copying a formula down a column.'),
           ('Dragging a point in GeoGebra and observing that a property persists', 'supports a conjecture but does not prove it', ['proves the result', 'disproves the result', 'is a proof by exhaustion'], 'Finitely many cases.'),
           ('Solutions found with a GDC "solver" are usually', 'numerical approximations', ['exact values', 'proofs', 'always all of the solutions'], 'Check the graph for further roots.')],
    why=[('Explain why a GDC graph might suggest an incorrect number of solutions to an equation.', 'The viewing window may hide intersections, or curves that are very close may appear to touch; the window should be adjusted and the result checked algebraically.'),
         ('Explain how technology can support, but not replace, proof in an investigation.', 'Technology can generate many cases quickly, reveal patterns and test conjectures, but a general argument is still needed to show the result holds for all cases.'),
         ('Explain why answers from a GDC should be given to an appropriate degree of accuracy and labelled.', 'GDC values are approximations; stating 3 significant figures (or as required) and what the value represents communicates the result honestly and clearly.')],
    misc=[('My GDC shows the curves y = eˣ and y = 3x intersect once, so there is exactly one solution.', 'Zooming out shows a second intersection (x ≈ 0.619 and x ≈ 1.51), so a single window can miss solutions.'),
          ('The spreadsheet shows the sequence gets closer to 0.739 after 30 terms, so the limit is exactly 0.739.', 'The values suggest a limit near 0.739085…, the solution of x = cos x; the numerical value is an approximation.')],
))


GDC_EQ = [lambda rng, a, b: (sp.exp(x) - a * x - b, f'eˣ = {a}x + {b}', -3, 4), lambda rng, a, b: (sp.cos(x) - x / a, f'cos x = x/{a}', -6, 6),
          lambda rng, a, b: (sp.log(x) - (x - a) / b, f'ln x = (x − {a})/{b}', 0.05, 30), lambda rng, a, b: (x ** 3 - a * x - b, f'x³ = {a}x + {b}', -5, 5),
          lambda rng, a, b: (sp.sin(x) - sp.Rational(1, a) * x ** 2 + b / 10, f'sin x = x²/{a} − {b / 10:g}', -6, 6), lambda rng, a, b: (x * sp.exp(-x) - sp.Rational(1, a + 2), f'xe^(−x) = 1/{a + 2}', -2, 12)]


@R.add('ch13-st4', 'C3', (2, 5), 'short', style='p2')
def gdc_solve(rng, slot):
    a, b = rng.randint(2, 5), rng.randint(1, 4)
    g, txt, lo, hi = rng.choice(GDC_EQ)(rng, a, b)
    fn = sp.lambdify(x, g, 'math')
    roots = nsols(fn, lo, hi, 3000)
    if not roots or len(roots) > 4:
        return None
    return mk(f'Use technology to solve the equation {txt}' + (f' for {lo:g} < x < {hi:g}' if 'cos' in txt or 'sin' in txt else '') + '.', ', '.join(f'x = {s3(r)}' for r in roots),
              f'Graph both sides or the difference with a suitable window (M1); {len(roots)} intersection{"s" if len(roots) > 1 else ""} found (A1); {", ".join(s3(r) for r in roots)} (A1{" A1" if len(roots) > 1 else ""}).', 3 + (len(roots) > 1))


@R.add('ch13-st4', 'C3', (2, 5), 'short', style='p2')
def gdc_extreme(rng, slot):
    a, b = rng.randint(1, 4), rng.randint(1, 3)
    pool = [(x * sp.exp(-x / a), 0, 10), (x ** 2 * sp.exp(-x) * b, 0, 10), (sp.sin(x) + sp.cos(a * x) / 2, 0, 3), (sp.log(x + 1) - x ** 2 / (a + 1), 0, 5), (x * sp.sqrt(a + 1 - x), 0, a + 1), ((x ** 2 + b) / (x + a), 0, 10)]
    f, lo, hi = rng.choice(pool)
    df = sp.lambdify(x, sp.diff(f, x), 'math')
    fv = sp.lambdify(x, f, 'math')
    cr = [r for r in nsols(df, lo + 1e-6, hi - 1e-6, 3000) if sp.diff(f, x, 2).subs(x, r) < 0]
    if not cr:
        cr2 = [r for r in nsols(df, lo + 1e-6, hi - 1e-6, 3000)]
        if not cr2:
            return None
        xm = cr2[0]
        kind = 'minimum'
    else:
        xm = cr[0]
        kind = 'maximum'
    return mk(f'Use technology to find the coordinates of the local {kind} point of y = {P(f)} for {lo} < x < {hi}.', f'({s3(xm)}, {s3(fv(xm))})',
              f'Graph in a suitable window (M1); use the {kind} feature or solve dy/dx = 0 (M1); x = {s3(xm)} (A1); y = {s3(fv(xm))} (A1).', 4)


@R.add('ch13-st4', 'C3', (2, 5), 'short', style='p2')
def gdc_area(rng, slot):
    a = rng.randint(2, 5)
    pool = [(sp.exp(-x ** 2) * a, x ** 2, -5, 5), (sp.cos(x) * a, x ** 2 - 1, -3, 3), (sp.sqrt(x) * a, x ** 2 / a, 0, 10), (sp.log(x + 2), (x - 1) ** 2 / a, -1.99, 6)]
    f, g, L0, L1 = rng.choice(pool)
    h = sp.lambdify(x, f - g, 'math')
    r = nsols(h, L0, L1, 4000)
    if len(r) < 2:
        return None
    lo, hi = r[0], r[-1]
    N = 4000
    hh = (hi - lo) / N
    A_ = sum(abs(h(lo + (i + 0.5) * hh)) for i in range(N)) * hh
    return mk(f'Use technology to find the area of the region enclosed by y = {P(f)} and y = {P(g)}.', s3(A_),
              f'Intersections x = {s3(lo)} and x = {s3(hi)} (A1 A1); ∫ |f − g| dx between them (M1); {s3(A_)} (A1).', 4)


TECH_TASKS = [('find the first 50 terms of the sequence uₙ₊₁ = 0.8uₙ + 3', 'a spreadsheet'), ('test whether the angle in a semicircle is always 90° for many positions of a point', 'dynamic geometry software'),
              ('find the line of best fit for a set of 30 data points', 'the regression feature of a GDC or spreadsheet'), ('find where e^(−x) = x to 3 s.f.', 'the GDC equation solver or graph intersection'),
              ('investigate how the graph of y = a sin(bx) changes as a and b vary', 'graphing software with sliders'), ('evaluate ∫ from 0 to 1 of e^(−x²) dx to 5 s.f.', 'the GDC numerical integration feature'),
              ('simulate 10 000 rolls of two dice', 'a spreadsheet or programming tool with random numbers'), ('check that the medians of many triangles are concurrent', 'dynamic geometry software')]


@R.add('ch13-st4', 'C1', (1, 3), 'mcq')
def tech_mcq(rng, slot):
    i = rng.randrange(len(TECH_TASKS))
    task, tool = TECH_TASKS[i]
    wr = list(dict.fromkeys(t for j, (_, t) in enumerate(TECH_TASKS) if t != tool))
    rng.shuffle(wr)
    if len(wr) < 3:
        return None
    return mcq(rng, f'Which technology is most appropriate to {task}?', tool, wr[:3], f'{tool[0].upper() + tool[1:]} is designed for this kind of task.')


@R.add('ch13-st4', 'C2', (2, 4), 'explain')
def tech_explain(rng, slot):
    kind = rng.choice(['window', 'limit', 'proof'])
    if kind == 'window':
        a = rng.choice([3, 4, 5, 6])
        roots = nsols(lambda v: math.exp(v) - a * v, -2, 5, 2000)
        return mk(f'A student graphs y = eˣ and y = {a}x on a GDC with window 0 ≤ x ≤ 1 and concludes the equation eˣ = {a}x has exactly one solution. Explain the error and give all solutions.', ', '.join(f'x = {s3(r)}' for r in roots),
                  f'The window hides the second intersection (R1); widen the window / consider the growth of eˣ (R1); {", ".join(s3(r) for r in roots)} (A1).', 3, 'explain')
    if kind == 'limit':
        k = rng.choice([2, 3, 5])
        v = math.sqrt(k)
        return mk(f'A spreadsheet computes xₙ₊₁ = ½(xₙ + {k}/xₙ) with x₀ = 1, and the values settle at {v:.6f}. Explain what this suggests and how it could be justified algebraically.', f'the limit is √{k}',
                  f'Values suggest convergence to {v:.6f} ≈ √{k} (R1); if the limit L exists, L = ½(L + {k}/L) (M1); so L² = {k}, L = √{k} (A1).', 3, 'explain')
    nm = rng.choice(['the angle in a semicircle is 90°', 'the diagonals of a parallelogram bisect each other', 'the perpendicular bisectors of a triangle are concurrent', 'opposite angles of a cyclic quadrilateral sum to 180°'])
    return mk(f'A student uses GeoGebra to drag points and observes that {nm} in every case tried. Explain the value and the limitation of this evidence.', 'strong evidence for a conjecture, but not a proof',
              'Many cases can be tested quickly and suggest the result is true (R1); finitely many cases do not prove it (R1); a general geometric/vector proof is required (R1).', 3, 'explain')


@R.add('ch13-st4', 'C4', (3, 5), 'multi_step', style='ext')
def fixed_point_parts(rng, slot):
    kind = rng.choice(['cos', 'exp', 'sqrt', 'gold'])
    if kind == 'cos':
        g, eq, x0, lab = sp.cos(x), 'x = cos x', rng.choice([0, 1, 0.5]), 'xₙ₊₁ = cos xₙ'
    elif kind == 'exp':
        g, eq, x0, lab = sp.exp(-x), 'x = e^(−x)', rng.choice([0, 1, 0.5]), 'xₙ₊₁ = e^(−xₙ)'
    elif kind == 'sqrt':
        k = rng.choice([2, 3, 5, 7, 10])
        g, eq, x0, lab = (x + k / x) / 2, f'x² = {k}', rng.choice([1, 2, 3]), f'xₙ₊₁ = ½(xₙ + {k}/xₙ)'
    else:
        g, eq, x0, lab = 1 + 1 / x, 'x² = x + 1', rng.choice([1, 2]), 'xₙ₊₁ = 1 + 1/xₙ'
    gf = sp.lambdify(x, g, 'math')
    xs_ = [float(x0)]
    for _ in range(60):
        xs_.append(gf(xs_[-1]))
    L = xs_[-1]
    n3 = next(i for i in range(1, 60) if abs(xs_[i] - L) < 0.5e-3 and all(abs(xs_[j] - L) < 0.5e-3 for j in range(i, 60)))
    dg = abs(float(sp.diff(g, x).subs(x, L)))
    parts = [(f'Use a spreadsheet to find x₁, x₂ and x₃, giving answers to 4 significant figures.', ', '.join(sfig(v) for v in xs_[1:4]), 'M1 A1 A1', 3, True),
             ('Find the limit L of the sequence to 6 significant figures.', sfig(L, 6), 'A1', 1, True),
             (f'Show that L satisfies the equation {eq}.', 'shown', 'if xₙ → L then L = g(L) (M1); rearrange (A1) AG', 2, True),
             ('Find the smallest n for which xₙ agrees with L to 3 decimal places for all later terms.', str(n3), 'A1', 1, False),
             ("Find |g′(L)| and explain how it relates to the speed of convergence.", f'{s3(dg)}; |g′(L)| < 1 ensures convergence, and smaller values mean faster convergence', 'A1 R1', 2, True)]
    return build_parts(rng, [f'The sequence {lab}, with x₀ = {x0}, is investigated using technology.', f'A student uses a spreadsheet to iterate {lab}, starting from x₀ = {x0}.'], parts, 4)


@R.add('ch13-st4', 'C4', (4, 5), 'multi_step', style='p3')
def tech_limit_parts(rng, slot):
    a = rng.choice([1, 2, 3, -1])
    vals = [(n, (1 + a / n) ** n) for n in (10, 100, 1000, 10000)]
    parts = [(f'Use technology to evaluate (1 + {a}/n)ⁿ for n = 10, 100, 1000 and 10 000, giving answers to 6 s.f.'.replace('+ −', '− ').replace('+ -', '− '), ', '.join(sfig(v, 6) for _, v in vals), 'A1 A1', 2, True),
             ('Make a conjecture about the limit as n → ∞.', f'e^{a}' if a != 1 else 'e', 'A1', 1, True),
             (f"By writing (1 + {a}/n)ⁿ = e^(n ln(1 + {a}/n)) and using L'Hôpital's rule, prove your conjecture.".replace('+ −', '− ').replace('+ -', '− '), 'proof', "n ln(1 + a/n) = ln(1 + a/n)/(1/n), 0/0 (M1); L'Hôpital → a (A1); continuity of exp (R1)", 3, True),
             ('Use the Maclaurin series of ln(1 + x) to show that the error is approximately a²eᵃ/(2n) for large n.', 'shown', 'n ln(1 + a/n) = a − a²/(2n) + … (M1); e^(a − a²/(2n)) ≈ eᵃ(1 − a²/(2n)) (A1) AG', 2, False),
             (f'Use this to estimate the error when n = 100, and compare with the value from technology.', f'{sci(a * a * math.exp(a) / 200)}; actual {sci(abs(math.exp(a) - vals[1][1]))}', 'A1 R1', 2, False)]
    return build_parts(rng, [f'This question uses technology and calculus to investigate lim as n → ∞ of (1 + {a}/n)ⁿ.'.replace('+ −', '− ').replace('+ -', '− '), 'A spreadsheet is used to explore a sequence related to compound interest.'], parts, 3)
