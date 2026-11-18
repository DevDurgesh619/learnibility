"""Shared helpers for the IB DP Physics packs (ib-g11-physics, ib-g12-physics).

IB Physics data booklet (first assessment 2025) constants, significant-figure formatting, numeric MCQs
with error-based distractors, IA-skills factories (repeat readings, linearising, Paper 1B gradient fits),
Paper 2 composites assembled from a subtopic's own templates, and a templates() builder.
Factories take the pack's Registry R as their first argument.
"""
from __future__ import annotations

import math
import re

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from engine import Slot

MOCK = [
    dict(section='Paper 1A – multiple-choice questions', count=40, c=['C1', 'C2', 'C3', 'C3', 'C2'], d=[2, 3, 2, 3, 4], type='mcq', marks=1),
    dict(section='Paper 1B – data-based questions on experimental work', count=4, c=['C3', 'C4'], d=[3, 4], type='case', marks=5, style='p1b'),
    dict(section='Paper 2 – structured short-response questions', count=6, c=['C3', 'C4'], d=[3, 4, 4], type='multi_step', marks=10, style='p2'),
    dict(section='Paper 2 – extended-response questions', count=2, c=['C4'], d=[4, 5], type='long', marks=15, style='p2x'),
]

# ---------------------------------------------------------------------------------------------
# IB data booklet constants
# ---------------------------------------------------------------------------------------------
g0 = 9.81
G = 6.67e-11
K = 8.99e9
E = 1.60e-19
H = 6.63e-34
C = 3.00e8
ME = 9.11e-31
MP = 1.673e-27
MN = 1.675e-27
U = 1.661e-27
UMEV = 931.5
EPS0 = 8.85e-12
MU0 = 4 * math.pi * 1e-7
SIGMA = 5.67e-8
WIEN = 2.90e-3
R0 = 1.20e-15
NA = 6.02e23
EV = 1.60e-19
KB = 1.38e-23
RGAS = 8.31
M_EARTH, R_EARTH = 5.97e24, 6.37e6
M_SUN, R_SUN, L_SUN = 1.99e30, 6.96e8, 3.83e26
M_MOON, R_MOON = 7.35e22, 1.74e6
AU, LY, PC = 1.50e11, 9.46e15, 3.09e16
MP_U, MN_U, ME_U = 1.007276, 1.008665, 0.000549


def sf(x, n=3):
    """x to n significant figures; scientific form with superscript powers outside 10⁻³ … 10⁴."""
    if x == 0:
        return '0'
    mag = math.floor(math.log10(abs(x)))
    xr = round(x, -mag + n - 1)
    if xr == 0:
        return '0'
    mag = math.floor(math.log10(abs(xr)))
    if -3 <= mag < 4:
        dec = max(0, n - 1 - mag)
        return f'{xr:.{dec}f}'.replace('-', '−')
    m_ = xr / 10 ** mag
    return f'{m_:.{n - 1}f} × 10{sup(mag)}'.replace('-', '−')


def q(x, unit='', n=3):
    s = sf(x, n)
    return f'{s} {unit}'.strip()


def deg(x, n=3):
    return f'{sf(x, n)}°'


def sind(a):
    return math.sin(math.radians(a))


def cosd(a):
    return math.cos(math.radians(a))


def asind(x):
    return math.degrees(math.asin(x))


def nmcq(rng, stem, v, wrongs, unit, key, n=3, extra=True):
    """Numeric MCQ: wrongs are plausible error values (listed first), then generic fall-backs."""
    c = q(v, unit, n)
    ws = []
    pool = list(wrongs) + ([v * 2, v / 2, v * 10, v / 10, v * 4, v / 4, v * 1.5] if extra else [])
    for w in pool:
        if w is None or w == 0:
            continue
        s = q(w, unit, n)
        if s != c and s not in ws:
            ws.append(s)
    if len(ws) < 3:
        return None
    return mcq(rng, stem, c, ws[:3], key)


def num(stem, ans, key, marks=2, type='numerical', gap=None):
    d = dict(stem=stem, answer=ans, markingKey=key, marks=marks, type=type)
    if gap:
        d['gap'] = gap
    return d


def pick(rng, seq):
    return seq[rng.randrange(len(seq))]


# ---------------------------------------------------------------------------------------------
# Generic IA-skills / Nature-of-Science factories
# ---------------------------------------------------------------------------------------------
def repeat_readings(R, key, quantity, unit, lo, hi, n_dp, context_list, c='C3', d=(1, 4)):
    """Mean, absolute (half-range) and percentage uncertainty of repeated readings."""
    def fn(rng, slot):
        true = rng.uniform(lo, hi)
        k = 4 if slot.d <= 2 else 5
        spread = true * rng.uniform(0.01, 0.05)
        vals = [round(true + rng.uniform(-spread, spread), n_dp) for _ in range(k)]
        if len(set(vals)) < 3:
            return None
        mean = sum(vals) / k
        half = (max(vals) - min(vals)) / 2
        pct = 100 * half / mean
        ctx = pick(rng, context_list)
        who = name(rng)
        vs = ', '.join(f'{v:.{n_dp}f}' for v in vals)
        if slot.d <= 2:
            stem = f'{who} {ctx} The repeated readings of {quantity} were {vs} {unit}. Calculate the mean value and its absolute uncertainty.'
            ans = f'{mean:.{n_dp}f} ± {half:.{n_dp}f} {unit}'
            key_ = f'Mean = {mean:.{n_dp}f} {unit} (A1); uncertainty = half the range = ({max(vals):.{n_dp}f} − {min(vals):.{n_dp}f})/2 = {half:.{n_dp}f} {unit} (A1).'
            return num(stem, ans, key_, 2)
        stem = f'{who} {ctx} The {k} readings of {quantity} were {vs} {unit}. Determine the mean, the absolute uncertainty and the percentage uncertainty, and state the result to an appropriate number of significant figures.'
        ans = f'{mean:.{n_dp}f} ± {half:.{n_dp}f} {unit} ({pct:.1f} %)'
        key_ = (f'Mean = {mean:.{n_dp}f} {unit} (A1); absolute uncertainty = half range = {half:.{n_dp}f} {unit} (A1); '
                f'percentage uncertainty = {half:.{n_dp}f}/{mean:.{n_dp}f} × 100 = {pct:.1f} % (A1). Result quoted to the same decimal place as the uncertainty.')
        return num(stem, ans, key_, 3)
    R.t.setdefault(key, []).append(T(c, d, fn, 'numerical', None, 'repeat_readings'))


def linearise(R, key, rows, c='C2', d=(2, 4)):
    """rows: (relationship text, what to plot y, what to plot x, gradient meaning, intercept note)."""
    def fn(rng, slot):
        rel, yv, xv, grad, icpt = pick(rng, rows)
        frame = rng.randrange(3)
        if frame == 0:
            stem = f'A student wants to test the relationship {rel}. State which quantities should be plotted on the axes to obtain a straight-line graph, and state what the gradient represents.'
        elif frame == 1:
            stem = f'In an investigation the relationship {rel} is expected. Explain how a linear graph can be used to verify this relationship and to determine a value from the gradient.'
        else:
            stem = f'Outline how the data from an experiment testing {rel} should be linearised, and state the features of the graph that would confirm the relationship.'
        ans = f'Plot {yv} (y-axis) against {xv} (x-axis); gradient = {grad}. {icpt}'
        return dict(stem=stem, answer=ans, type='explain', marks=3,
                    markingKey=f'Correct choice of axes: {yv} against {xv} (M1); straight line expected (R1); gradient = {grad} (A1). {icpt}')
    R.t.setdefault(key, []).append(T(c, d, fn, 'explain', None, 'linearise'))


def gradient_fit(R, key, spec, c=('C3', 'C4'), d=(3, 5), style='p1b'):
    """Paper 1B style: a table of data from an experiment; linearise, find gradient, deduce a quantity.

    spec(rng) -> dict(intro, xname, xunit, yname, yunit, xs, ys, xfmt, yfmt, plot_x, plot_y (functions), what,
                      deduce (fn grad, icpt -> (value, unit, text)), extra_q, extra_a, plot_label)
    """
    def fn(rng, slot):
        s = spec(rng)
        if s is None:
            return None
        xs, ys = s['xs'], s['ys']
        X = [s['plot_x'](v) for v in xs]
        Y = [s['plot_y'](v) for v in ys]
        n = len(X)
        mx, my = sum(X) / n, sum(Y) / n
        sxx = sum((a - mx) ** 2 for a in X)
        if sxx == 0:
            return None
        m_ = sum((a - mx) * (b - my) for a, b in zip(X, Y)) / sxx
        b_ = my - m_ * mx
        val, unit, text = s['deduce'](m_, b_)
        gtxt = f'{sf(m_, 3)} {s.get("gunit", "")}'.strip()
        rows = '\n'.join(f'{s["xfmt"](a)} | {s["yfmt"](b)}' for a, b in zip(xs, ys))
        table = f'{s["xname"]} / {s["xunit"]} | {s["yname"]} / {s["yunit"]}\n{rows}'
        unc = rng.choice([2, 3, 4, 5])
        stem = (f'{s["intro"]}\n\n{table}\n\n(a) State the quantities that should be plotted to obtain a straight line. [1]\n'
                f'(b) Using the data, determine the gradient of the best-fit line. [2]\n'
                f'(c) Hence determine {s["what"]}. [1]\n'
                f'(d) The gradients of the maximum and minimum lines differ from the best-fit gradient by ±{unc} %. State {s["what_short"]} with its absolute uncertainty. [1]')
        ans = (f'(a) {s["plot_label"]}; (b) gradient ≈ {gtxt}; (c) {q(val, unit)}; '
               f'(d) {_with_unc(val, abs(val) * unit_frac(unc), unit)}').replace('  ', ' ')
        key_ = (f'(a) {s["plot_label"]} (A1). (b) Best-fit line through the plotted points (M1); gradient ≈ {gtxt} – accept ±3 % (A1). '
                f'(c) {text} = {q(val, unit)} (A1). (d) absolute uncertainty = {unc} % of the value = {q(abs(val) * unit_frac(unc), unit, 1)}; value quoted to the same precision (A1).')
        return dict(stem=stem, answer=ans, markingKey=key_, type='case', marks=5, gap='G7')
    R.t.setdefault(key, []).append(T(c, d, fn, 'case', style, 'gradient_fit'))


def _with_unc(val, u, unit):
    """Value ± uncertainty, the value rounded to the decimal place of the 1 s.f. uncertainty (plain range only)."""
    us = sf(u, 1)
    if 1e-3 <= abs(val) < 1e4 and 1e-3 <= u < 1e4:
        uu = float(us)
        dec = -math.floor(math.log10(uu))
        vs = f'{round(val, dec):.{max(0, dec)}f}'.replace('-', '−')
        return f'({vs} ± {us}) {unit}'.replace(' )', ')').strip() if unit else f'{vs} ± {us}'
    return f'{q(val, unit)} ± {q(u, unit, 1)}'


def unit_frac(p):
    return p / 100


# ---------------------------------------------------------------------------------------------
# Paper-style composites (only used to fill mock sections)
# ---------------------------------------------------------------------------------------------
def _part(rng, tpls, c, d, used, slot):
    pool = [t for t in tpls if (c in (t.c if isinstance(t.c, tuple) else (t.c,))) and t.type != 'mcq'
            and t.style is None and t.name not in used and t.d[0] <= d <= t.d[1] + 1]
    rng.shuffle(pool)
    for t in pool[:6]:
        try:
            out = t.fn(rng, Slot(slot.subtopic, slot.chapter, c, d, set='part'))
        except IndexError:
            out = None
        if out and out.get('type') != 'mcq' and not out.get('options'):
            used.add(t.name)
            return out
    return None


PROPER = ("Snell's", 'Doppler', "Kepler's", "Faraday's", 'Bohr', 'Compton', 'Hertzsprung-Russell', "Newton's", "Kirchhoff's", "Ohm's", "Stokes'", 'Galilean', 'Lorentz', 'Minkowski', "Wien's", 'Stefan-Boltzmann')


def lc_topic(t):
    w = t.split(' ')[0]
    if w in PROPER:
        return t
    return t[0].lower() + t[1:]


_ROMAN = {'a': 'i', 'b': 'ii', 'c': 'iii', 'd': 'iv', 'e': 'v', 'f': 'vi'}


def _roman(t):
    return re.sub(r'\(([a-f])\)', lambda m_: f'({_ROMAN[m_.group(1)]})', t)


def _fix_marks(key, m_):
    return re.sub(r'\(\d+ marks?:', f'({m_} marks:', key)


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
            parts.append((p, m_))
        parts = [(dict(p, stem=_roman(p['stem']), answer=_roman(str(p['answer'])), markingKey=_roman(p['markingKey'])), m_) for p, m_ in parts]
        stems = [p['stem'] for p, _ in parts]
        if len(set(stems)) < len(stems):
            return None
        intro = f'This question is about {lc_topic(st["name"])}.'
        letters = 'abcdef'
        stem = intro + '\n\n' + '\n\n'.join(f'({letters[i]}) {p["stem"]} [{m_}]' for i, (p, m_) in enumerate(parts))
        ans = ' '.join(f'({letters[i]}) {p["answer"]}' for i, (p, m_) in enumerate(parts))
        key = ' '.join(f'({letters[i]}) [{m_} marks] {_fix_marks(p["markingKey"], m_)}' for i, (p, m_) in enumerate(parts))
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


def _cap(t):
    t = t.strip()
    w = t.split(' ', 1)[0]
    if not any(ch in 'aeiouAEIOU' for ch in w) or any(ch in w for ch in '=²³/'):
        return t  # starts with a symbol or formula such as mgh, pV, ΔU
    return t[0].upper() + t[1:]


_DANGLING = {'It', 'They', 'That', 'Its', 'Both', 'Their', 'This', 'These', 'Those', 'He', 'She', 'Her', 'His'}


def _standalone(s):
    """A correction that reads as a complete statement without the claim it corrects."""
    return s.split(' ', 1)[0] not in _DANGLING


def statement_mcq(R, st):
    """C2 conceptual MCQ: pick the correct statement (or the misconception) from authored misconceptions."""
    key = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
    ch = key.split('-')[0]
    own = R.f.get(key)
    sib = [ff for k, ff in R.f.items() if k.startswith(ch + '-') and k != key]
    topic = lc_topic(st['name'])

    def fn(rng, slot):
        if own is None or not own.misc:
            return None
        claims = [c for c, _ in own.misc] + [c for ff in sib for c, _ in ff.misc]
        fixes = [f_ for _, f_ in own.misc if _standalone(f_)]
        sib_fix = [f_ for ff in sib for _, f_ in ff.misc if _standalone(f_)]
        who = name(rng)
        city = rng.choice(CITIES)
        if fixes and rng.random() < 0.5:
            right = rng.choice(fixes)
            wr = [c for c in claims if c != right]
            if len(wr) < 3:
                return None
            wr = list(dict.fromkeys(wr))
            if len(wr) < 3:
                return None
            wr = rng.sample(wr, 3)
            stem = rng.choice([f'{who} is revising {topic}. Which of the following statements is correct?',
                               f'A teacher in {city} asks a class to choose the one correct statement about {topic}. Which statement should be chosen?',
                               f'{who} and a classmate in {city} disagree about {topic}. Which statement is correct?'])
            return mcq(rng, stem, _cap(right), [_cap(w) for w in wr], f'The other options are common misconceptions. {_cap(right)}')
        cl, fx = rng.choice(own.misc)
        trues = [f_ for f_ in fixes if f_ != fx] + sib_fix
        if len(trues) < 3:
            return None
        wr = rng.sample(trues, 3)
        stem = rng.choice([f'{who} writes four statements while revising {topic}. Which one is a misconception?',
                           f'A student in {city} is checking notes on {topic}. Which statement is incorrect?',
                           f'Which of the following statements about {topic} is a common misconception? (Revision quiz set by {who}.)'])
        return mcq(rng, stem, _cap(cl), [_cap(w) for w in wr], f'This is incorrect: {fx}')
    return fn


def make_templates(R, p2_specs=None, p2x_specs=None):
    """Return a pack-level templates(st) that adds fact_q, borrowed p1b, statement MCQs and Paper 2 composites."""
    cache: dict = {}
    p2s = p2_specs or P2_SPECS
    p2xs = p2x_specs or P2X_SPECS

    def templates(st):
        if st['id'] in cache:
            return cache[st['id']]
        base = [t for t in R.build(st) if t.name != 'fact_short']
        key0 = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
        if key0 in R.f:
            qs = [f_ for f_ in R.f[key0].facts if f_[0].rstrip().endswith('?')]
            if qs:
                def fact_q(rng, slot, qs=qs):
                    q_, a, w, why = pick(rng, qs)
                    return dict(stem=q_.replace('Which of the following', 'What').replace('which of the following', 'what'), answer=_cap(a),
                                markingKey=f'{_cap(a)} (A1). {why}', type='short', marks=1)
                base.append(T('C1', (2, 3), fact_q, 'short', None, 'fact_q'))
        out = list(base)
        # Paper 1B: borrow a data-based question from a sibling subtopic (mocks only) if this one has none.
        if not any(t.style == 'p1b' for t in base):
            key = st['id'].rsplit('-', 2)[-2]
            for k2, ts in R.t.items():
                if k2.startswith(key + '-'):
                    out += [_mock_only(t) for t in ts if t.style == 'p1b']
        out.append(T('C2', (1, 4), statement_mcq(R, st), 'mcq', None, 'statement_mcq'))
        for i, spec in enumerate(p2s):
            out.append(T(('C3', 'C4'), (3, 5), composite(st, base, spec, 'p2'), 'multi_step', 'p2', f'p2_{i}'))
        for i, spec in enumerate(p2xs):
            out.append(T('C4', (3, 5), composite(st, base, spec, 'p2x'), 'long', 'p2x', f'p2x_{i}'))
        out = [_guard(t, st) if t.type == 'mcq' else t for t in out]
        cache[st['id']] = out
        return out
    return templates


def _mock_only(t):
    def fn(rng, slot):
        return t.fn(rng, slot) if slot.set == 'mock' else None
    return T(t.c, t.d, fn, t.type, t.style, t.name + '_borrowed')


_OPTSETS: dict = {}


def _guard(t, st):
    """Avoid re-using the same four options in one chapter (the validator compares stem + options)."""
    chk = st['id'].rsplit('-', 1)[0]
    fn0 = t.fn

    def fn(rng, slot):
        o = fn0(rng, slot)
        if not o or not o.get('options'):
            return o
        k = frozenset(o['options'])
        seen = _OPTSETS.setdefault(chk, set())
        if k in seen:
            return None
        seen.add(k)
        return o
    return T(t.c, t.d, fn, t.type, t.style, t.name)




def add_f(R, key, **kw):
    f = R.f[key]
    for k, v in kw.items():
        getattr(f, k).extend(v)
