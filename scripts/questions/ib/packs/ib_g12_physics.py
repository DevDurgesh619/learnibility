"""IB DP Physics SL/HL (first assessment 2025), DP year 2 – ib-g12-physics.

Themes C.3–C.5 (wave phenomena, standing waves, Doppler), D.1–D.4 (fields and induction) and
E.1–E.5 (atom, quantum, radioactivity, fission, fusion and stars).

Numerical items are parametric and compute their answers with IB data-booklet constants
(g = 9.81 m s⁻², G = 6.67 × 10⁻¹¹ N m² kg⁻², k = 8.99 × 10⁹ N m² C⁻², e = 1.60 × 10⁻¹⁹ C,
h = 6.63 × 10⁻³⁴ J s, c = 3.00 × 10⁸ m s⁻¹, mₑ = 9.11 × 10⁻³¹ kg, u = 931.5 MeV c⁻², …).
Answers are given to 3 significant figures unless the data justify fewer.

Mock = HL Paper 1 (1A: 40 MCQ, 1B: data-based questions on experimental work, 60 marks) +
Paper 2 (structured and extended response, 90 marks): 52 items, 150 marks.
"""
from __future__ import annotations

import math
import re

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from engine import Slot

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

MOCK = [
    dict(section='Paper 1A – multiple-choice questions', count=40, c=['C1', 'C2', 'C3', 'C3', 'C2'], d=[2, 3, 2, 3, 4], type='mcq', marks=1),
    dict(section='Paper 1B – data-based questions on experimental work', count=4, c=['C3', 'C4'], d=[3, 4], type='case', marks=5, style='p1b'),
    dict(section='Paper 2 – structured short-response questions', count=6, c=['C3', 'C4'], d=[3, 4, 4], type='multi_step', marks=10, style='p2'),
    dict(section='Paper 2 – extended-response questions', count=2, c=['C4'], d=[4, 5], type='long', marks=15, style='p2x'),
]

R = Registry()

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
M_EARTH, R_EARTH = 5.97e24, 6.37e6
M_SUN, R_SUN, L_SUN = 1.99e30, 6.96e8, 3.83e26
M_MOON, R_MOON = 7.35e22, 1.74e6
AU, LY, PC = 1.50e11, 9.46e15, 3.09e16
MP_U, MN_U, ME_U = 1.007276, 1.008665, 0.000549


def init(subject_id):
    pass


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
def repeat_readings(key, quantity, unit, lo, hi, n_dp, context_list, c='C3', d=(1, 4)):
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


def linearise(key, rows, c='C2', d=(2, 4)):
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


def gradient_fit(key, spec, c=('C3', 'C4'), d=(3, 5), style='p1b'):
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
        rows = '\n'.join(f'{s["xfmt"](a)} | {s["yfmt"](b)}' for a, b in zip(xs, ys))
        table = f'{s["xname"]} / {s["xunit"]} | {s["yname"]} / {s["yunit"]}\n{rows}'
        unc = rng.choice([2, 3, 4, 5])
        stem = (f'{s["intro"]}\n\n{table}\n\n(a) State the quantities that should be plotted to obtain a straight line. [1]\n'
                f'(b) Using the data, determine the gradient of the best-fit line. [2]\n'
                f'(c) Hence determine {s["what"]}. [1]\n'
                f'(d) The gradients of the maximum and minimum lines differ from the best-fit gradient by ±{unc} %. State {s["what_short"]} with its absolute uncertainty. [1]')
        ans = (f'(a) {s["plot_label"]}; (b) gradient ≈ {sf(m_, 3)} {s.get("gunit", "")}; (c) {q(val, unit)}; '
               f'(d) {q(val, unit)} ± {sf(abs(val) * unit_frac(unc), 1)} {unit}').replace('  ', ' ')
        key_ = (f'(a) {s["plot_label"]} (A1). (b) Best-fit line through the plotted points (M1); gradient ≈ {sf(m_, 3)} {s.get("gunit", "")} – accept ±3 % (A1). '
                f'(c) {text} = {q(val, unit)} (A1). (d) absolute uncertainty = {unc} % of the value = {sf(abs(val) * unit_frac(unc), 1)} {unit}; value quoted to the same precision (A1).')
        return dict(stem=stem, answer=ans, markingKey=key_, type='case', marks=5, gap='G7')
    R.t.setdefault(key, []).append(T(c, d, fn, 'case', style, 'gradient_fit'))


def unit_frac(p):
    return p / 100


# ---------------------------------------------------------------------------------------------
# Paper-style composites (only used to fill mock sections)
# ---------------------------------------------------------------------------------------------
_CACHE: dict = {}


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


PROPER = ("Snell's", 'Doppler', "Kepler's", "Faraday's", 'Bohr', 'Compton', 'Hertzsprung-Russell')


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
    return t[0].upper() + t[1:]


def statement_mcq(st):
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
        fixes = [f_ for _, f_ in own.misc]
        sib_fix = [f_ for ff in sib for _, f_ in ff.misc]
        who = name(rng)
        city = rng.choice(CITIES)
        if rng.random() < 0.5:
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


def templates(st):
    if st['id'] in _CACHE:
        return _CACHE[st['id']]
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
    # Paper 1B: borrow a data-based question from a sibling subtopic if this one has none.
    if not any(t.style == 'p1b' for t in base):
        key = st['id'].rsplit('-', 2)[-2]
        for k2, ts in R.t.items():
            if k2.startswith(key + '-'):
                out += [_mock_only(t) for t in ts if t.style == 'p1b']
    out.append(T('C2', (1, 4), statement_mcq(st), 'mcq', None, 'statement_mcq'))
    for i, spec in enumerate(P2_SPECS):
        out.append(T(('C3', 'C4'), (3, 5), composite(st, base, spec, 'p2'), 'multi_step', 'p2', f'p2_{i}'))
    for i, spec in enumerate(P2X_SPECS):
        out.append(T('C4', (3, 5), composite(st, base, spec, 'p2x'), 'long', 'p2x', f'p2x_{i}'))
    out = [_guard(t, st) if t.type == 'mcq' else t for t in out]
    _CACHE[st['id']] = out
    return out


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


# =============================================================================================
# ch01 C.3 Wave phenomena
# =============================================================================================
MEDIA = {'crown glass': 1.52, 'water': 1.33, 'perspex (acrylic)': 1.49, 'diamond': 2.42, 'flint glass': 1.62,
         'ice': 1.31, 'ethanol': 1.36, 'glycerol': 1.47, 'sapphire': 1.77, 'quartz': 1.54}

R.facts('ch01-st1', F(
    terms=[('wavefront', 'a line or surface joining neighbouring points on a wave that oscillate in phase'),
           ('ray', 'a line showing the direction in which a wave transfers energy; it is perpendicular to the wavefronts'),
           ('refraction', 'the change in direction of a wave when it crosses a boundary at an angle and its speed changes'),
           ('normal', 'a line drawn perpendicular to a boundary at the point where a ray meets it'),
           ('angle of incidence', 'the angle between the incident ray and the normal at the boundary')],
    facts=[('Which quantity is unchanged when a wave passes from one medium into another?', 'frequency', ['speed', 'wavelength', 'direction of travel at oblique incidence'], 'The frequency is set by the source; speed and wavelength change at the boundary.'),
           ('What is the angle between a ray and the wavefronts it crosses?', '90°', ['0°', '45°', 'equal to the angle of incidence'], 'Rays are always perpendicular to the wavefronts.'),
           ('Water waves in a ripple tank pass from deep into shallow water. Which statement is correct?', 'The wavefronts become closer together.', ['The frequency decreases.', 'The waves speed up.', 'The wavefronts become further apart.'], 'Waves travel more slowly in shallow water; with f fixed, λ = v/f decreases.'),
           ('According to the law of reflection, which angles are equal?', 'the angle of incidence and the angle of reflection, both measured from the normal', ['the angle of incidence and the angle of refraction', 'the angles between each ray and the surface and the normal', 'the angle of reflection and the critical angle'], 'i = r with both measured from the normal.'),
           ('A ray meets a boundary along the normal. What happens to the transmitted ray?', 'It continues without a change of direction but with a change of speed.', ['It is bent towards the normal.', 'It is totally internally reflected.', 'It travels along the boundary.'], 'At normal incidence sin θ₁ = 0, so θ₂ = 0: speed and wavelength change but direction does not.')],
    why=[('Explain why the frequency of a wave does not change when it crosses a boundary between two media.', 'Each wavefront arriving at the boundary produces one wavefront on the other side; the boundary cannot create or destroy cycles, so the number of waves per second (set by the source) is the same in both media.'),
         ('Explain, using wavefronts, why a wave bends towards the normal when it enters a medium in which it travels more slowly.', 'The part of an oblique wavefront that reaches the boundary first slows down while the rest continues at the higher speed; the wavefront swings round so that it travels closer to the normal.'),
         ('Explain why the wavelength of water waves decreases as they move into shallower water.', 'Wave speed decreases in shallower water while the frequency stays the same, so λ = v/f must decrease.'),
         ('Explain why rays are drawn perpendicular to wavefronts.', 'Energy is transferred in the direction of propagation, which is normal to the surfaces of constant phase (the wavefronts).'),
         ('Explain why sound bends away from the normal when it passes from air into water.', 'Sound travels faster in water (about 1500 m s⁻¹) than in air (about 340 m s⁻¹); a wave entering a faster medium at an angle bends away from the normal.')],
    contrast=[('a wavefront', 'a ray', 'A wavefront joins points that are in phase; a ray shows the direction of energy transfer and is perpendicular to the wavefronts.'),
              ('reflection', 'refraction', 'In reflection the wave returns into the same medium with unchanged speed and wavelength (i = r); in refraction the wave enters a new medium, its speed and wavelength change and (at oblique incidence) its direction changes.'),
              ('specular reflection', 'diffuse reflection', 'Specular reflection from a smooth surface keeps parallel rays parallel and forms an image; diffuse reflection from a rough surface scatters parallel rays in many directions, though each ray still obeys i = r locally.')],
    misc=[('When light enters glass it slows down, so its frequency decreases.', 'The frequency stays constant; it is the wavelength that decreases (λ = v/f) because the speed decreases.'),
          ('The angle of incidence is measured between the ray and the surface.', 'Angles of incidence, reflection and refraction are measured from the normal, not from the surface.'),
          ('A wave always changes direction when it crosses a boundary.', 'At normal incidence (along the normal) the wave changes speed and wavelength but not direction.'),
          ('Waves bend towards the normal whenever they pass into a denser material.', 'What matters is wave speed, not density: sound travels faster in water than in air and so bends away from the normal on entering water.')],
    evaluate=[('The ray model of light is sufficient to explain all optical phenomena.', ['rays predict reflection, refraction and image formation accurately', 'ray diagrams are simple and useful for lens and mirror design'], ['rays cannot explain diffraction or interference, which need a wave (wavefront) model', 'polarisation and the photoelectric effect need wave and photon models respectively'], 'The ray model is a useful simplification valid when apertures are much larger than the wavelength; a complete account needs wave and photon models – an example of models having limited domains of validity (NOS).')],
    extended=[('A plane water wave of frequency 5.0 Hz travels at 0.30 m s⁻¹ in deep water and meets a straight boundary with shallow water at an angle of incidence of 40°. In the shallow water its speed is 0.20 m s⁻¹. (a) Calculate the wavelength in each region. (b) Calculate the angle of refraction. (c) Sketch and describe the wavefronts in both regions.', '(a) 6.0 cm in deep water and 4.0 cm in shallow water; (b) sin θ₂ = (0.20/0.30) sin 40° → θ₂ = 25.4°; (c) wavefronts closer together in the shallow region and turned towards the boundary, rays bent towards the normal.', 6, 'multi_step')],
))


@R.add('ch01-st1', 'C3', (1, 4), 'numerical')
def c3_wave_boundary(rng, slot):
    frames = [
        ('ripple', 'Water waves in a ripple tank', 'deep water', 'shallow water', (0.18, 0.35), (0.6, 0.9), (4, 12), 'Hz'),
        ('sound', 'A sound wave', 'air', 'water', (330, 345), (4.2, 4.5), (200, 2000), 'Hz'),
        ('ocean', 'Ocean swell', 'the open ocean', 'a shallow coastal shelf', (8, 15), (0.35, 0.6), (0.06, 0.12), 'Hz'),
        ('seismic', 'A seismic P-wave', 'granite', 'sediment', (5500, 6200), (0.3, 0.5), (2, 10), 'Hz'),
    ]
    tag, what, m1, m2, vr, ratio, fr, fu = pick(rng, frames)
    v1 = round(rng.uniform(*vr), 3 if v1_small(vr) else 0)
    v2 = v1 * rng.uniform(*ratio)
    f = rng.uniform(*fr)
    f = round(f, 2 if f < 1 else 1 if f < 20 else 0)
    l1, l2 = v1 / f, v2 / f
    if slot.d <= 2:
        stem = f'{what} of frequency {sf(f)} {fu} travels at {sf(v1)} m s⁻¹ in {m1}. Calculate its wavelength in {m1}.'
        return num(stem, q(l1, 'm'), f'λ = v/f = {sf(v1)}/{sf(f)} (M1) = {q(l1, "m")} (A1).', 2)
    stem = f'{what} of frequency {sf(f)} {fu} has wavelength {q(l1, "m")} in {m1}. On entering {m2} its speed becomes {sf(v2)} m s⁻¹. Determine its frequency and wavelength in {m2}.'
    return num(stem, f'f = {sf(f)} {fu}; λ = {q(l2, "m")}', f'Frequency unchanged at {sf(f)} {fu} (R1); λ = v/f = {sf(v2)}/{sf(f)} (M1) = {q(l2, "m")} (A1).', 3)


def v1_small(vr):
    return vr[1] < 1


@R.add('ch01-st1', 'C3', (1, 3), 'mcq')
def c3_wave_boundary_mcq(rng, slot):
    n1, n2 = rng.sample(list(MEDIA), 2)
    lam0 = rng.choice([405, 450, 488, 532, 589, 633, 650, 694])
    lam = lam0 / MEDIA[n1]
    return nmcq(rng, f'Light of wavelength {lam0} nm in a vacuum enters {n1} (refractive index {MEDIA[n1]}). What is its wavelength in {n1}?',
                lam, [lam0 * MEDIA[n1], lam0, lam0 / MEDIA[n1] ** 2], 'nm',
                f'λ = λ₀/n = {lam0}/{MEDIA[n1]} = {q(lam, "nm")}; frequency is unchanged so the wavelength falls by the factor n.', extra=False)


@R.add('ch01-st1', 'C1', (1, 2), 'numerical')
def c1_reflection(rng, slot):
    a = rng.randint(12, 78)
    frames = [(f'A ray strikes a plane mirror making an angle of {a}° with the mirror surface. State the angle of reflection.', 90 - a),
              (f'A laser beam hits a flat reflecting surface at an angle of incidence of {a}°. State the angle between the incident and the reflected beam.', 2 * a),
              (f'A ray makes an angle of {a}° with the normal to a mirror. State the angle between the reflected ray and the mirror surface.', 90 - a)]
    s, v = pick(rng, frames)
    return num(s, f'{v}°', f'{v}° – angles of incidence and reflection are equal and measured from the normal (A1).', 1)


R.mcqs('ch01-st1', 'C2', (1, 4), [
    ('Plane waves travelling at speed v cross into a region where they travel at v/2. The angle of incidence is 0°. Which describes the transmitted waves?', 'same direction, half the wavelength', ['bent towards the normal, half the wavelength', 'same direction, double the wavelength', 'same direction, half the frequency'], 'At normal incidence there is no change in direction; f is unchanged so λ halves.'),
    ('Which change makes a ray refract more strongly at a boundary?', 'a larger ratio of wave speeds in the two media', ['a larger amplitude of the wave', 'a smaller frequency with the same speeds', 'a smaller angle of incidence'], 'sin θ₁/sin θ₂ = v₁/v₂: the bending depends on the speed ratio and increases with the angle of incidence.'),
    ('Sound passes obliquely from air into water. Compared with the incident ray, the refracted ray is', 'further from the normal', ['closer to the normal', 'along the normal', 'reflected back into the air'], 'Sound is faster in water, so it bends away from the normal.'),
    ('A ripple-tank stroboscope is set to the wave frequency. The wavefronts appear stationary in both deep and shallow regions. This shows that', 'the frequency is the same in both regions', ['the speed is the same in both regions', 'the wavelength is the same in both regions', 'the waves do not refract'], 'A single strobe frequency freezes both regions, so both have the same frequency.'),
])

repeat_readings('ch01-st1', 'the distance spanned by ten wavefronts', 'cm', 8.0, 20.0, 1,
                ['used a stroboscope to freeze the waves in a ripple tank and measured the waves on a ruler on the screen.',
                 'photographed the shadows of ripple-tank waves and measured them from the photograph.'])

R.static('ch01-st1', 'C4', (3, 5), [
    ('Water waves of wavelength 3.0 cm travel in deep water at 24 cm s⁻¹ towards a straight boundary with shallow water, where their speed is 16 cm s⁻¹. The wavefronts make 35° with the boundary. (a) State the angle of incidence of the rays. (b) Determine the angle of refraction and the new wavelength. (c) Explain whether the waves could be totally internally reflected if they travelled the other way.',
     '(a) 35°; (b) 22.5°, 2.0 cm; (c) yes – going from shallow to deep the waves speed up, so above the critical angle of 41.8° they are totally reflected.',
     'Angle between wavefront and boundary equals angle between ray and normal = 35° (A1); sin θ₂ = (16/24) sin 35° (M1), θ₂ = 22.5° (A1); λ = 3.0 × 16/24 = 2.0 cm (A1); TIR possible from slow to fast medium, critical angle sin⁻¹(16/24) = 41.8° (R1).'),
    ('An engineer models how ocean waves approaching a beach at an angle become almost parallel to the shoreline. Using the idea of wave speed decreasing with depth, explain this observation and suggest why headlands receive more wave energy than bays.',
     'As the water gets shallower the wave slows, so the part of each wavefront in shallower water lags behind and the wavefronts turn until they are nearly parallel to the depth contours (the shoreline). Near a headland the depth contours curve round the headland, so refraction concentrates (converges) rays on the headland and spreads (diverges) them in bays.',
     'Speed decreases with depth (M1); wavefronts turn towards the depth contours / rays turn towards the normal (R1); waves arrive nearly parallel to the shore (A1); convergence of rays on headlands, divergence in bays (R1); link to energy concentration and erosion (A1).'),
], type='multi_step', marks=5)

gradient_fit('ch01-st1', lambda rng: _ripple_spec(rng))


def _ripple_spec(rng):
    depth_v = rng.uniform(0.9, 1.1)
    fs = [4.0, 6.0, 8.0, 10.0, 12.0]
    v = round(rng.uniform(0.18, 0.30), 3)
    lams = [round(100 * v / f_ * rng.uniform(0.97, 1.03), 2) for f_ in fs]
    return dict(intro=f'A student investigates water waves in a ripple tank of constant depth. The dipper frequency f is varied and the wavelength λ is measured with a stroboscope. Theory predicts λ = v/f.',
                xname='f', xunit='Hz', yname='λ', yunit='cm', xs=fs, ys=lams, xfmt=lambda a: f'{a:.1f}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: 1 / a, plot_y=lambda b: b / 100, plot_label='λ against 1/f (λ in m)', what='the speed of the waves', what_short='the wave speed',
                gunit='m s⁻¹', deduce=lambda m_, b_: (m_, 'm s⁻¹', 'v = gradient'))


R.facts('ch01-st2', F(
    terms=[('refractive index', 'the ratio of the speed of light in a vacuum to the speed of light in the medium, n = c/v'),
           ("Snell's law", 'n₁ sin θ₁ = n₂ sin θ₂ for a ray crossing a boundary between media of refractive indices n₁ and n₂'),
           ('critical angle', 'the angle of incidence in the denser medium for which the angle of refraction is 90°'),
           ('total internal reflection', 'complete reflection of a wave at a boundary with a medium of lower refractive index when the angle of incidence exceeds the critical angle')],
    facts=[('Which conditions are both needed for total internal reflection?', 'light travels towards a medium of lower refractive index and the angle of incidence exceeds the critical angle', ['light travels towards a medium of higher refractive index and the angle exceeds the critical angle', 'the angle of incidence is less than the critical angle', 'the surface is silvered'], 'TIR needs n₁ > n₂ and θ₁ > θc.'),
           ('What is the refractive index of a medium in which light travels at 2.0 × 10⁸ m s⁻¹?', '1.5', ['0.67', '2.0', '6.0'], 'n = c/v = 3.0 × 10⁸/2.0 × 10⁸ = 1.5.'),
           ('Which expression gives the critical angle c for light in glass of refractive index n surrounded by air?', 'sin c = 1/n', ['sin c = n', 'cos c = 1/n', 'tan c = 1/n'], 'n sin c = 1 × sin 90°.'),
           ('In an optical fibre, why is the core given a higher refractive index than the cladding?', 'so that light can be totally internally reflected at the core–cladding boundary', ['so that light travels faster in the core', 'so that the cladding absorbs stray light', 'so that light refracts out of the fibre'], 'TIR only occurs going from higher to lower refractive index.')],
    why=[('Explain why total internal reflection cannot occur when light passes from air into glass.', 'Going into a medium of higher refractive index the ray bends towards the normal, so the refraction angle is always smaller than the incidence angle and can never reach 90°; there is no critical angle.'),
         ('Explain why a diamond sparkles more than a glass replica of the same shape.', 'Diamond has a much higher refractive index (2.42), so its critical angle is small (about 24°); more light entering the stone is totally internally reflected many times before leaving, and its strong dispersion separates the colours.'),
         ('Explain why the cladding of an optical fibre improves its performance.', 'Cladding of lower refractive index protects the core surface from scratches and contamination that would spoil TIR, prevents light leaking to neighbouring fibres and reduces the range of ray paths, reducing multipath (modal) dispersion.'),
         ('Explain why a ray entering a glass block along the normal is not deviated.', 'For θ₁ = 0, Snell’s law gives sin θ₂ = 0, so θ₂ = 0; the wavefronts are parallel to the boundary and all parts slow down at the same time.'),
         ('Explain why a swimming pool appears shallower than it really is.', 'Light from the bottom bends away from the normal as it leaves the water; the eye traces the rays back in straight lines to a point above the real position, so the bottom appears raised.')],
    contrast=[('refractive index', 'critical angle', 'Refractive index n = c/v is a property of a medium; the critical angle is the angle of incidence (in the denser medium) giving 90° refraction at a particular boundary, given by sin c = n₂/n₁.'),
              ('partial reflection', 'total internal reflection', 'Partial reflection happens at any boundary with some light also refracted; total internal reflection happens only for light going into a lower-index medium above the critical angle, when no light is refracted.')],
    misc=[('Light speeds up when it enters glass because glass is denser.', 'Light slows down in glass: v = c/n with n ≈ 1.5, so v ≈ 2.0 × 10⁸ m s⁻¹.'),
          ('Snell’s law says that the ratio of the angles θ₁/θ₂ is constant.', 'It is the ratio of the sines that is constant: n₁ sin θ₁ = n₂ sin θ₂; θ₁/θ₂ is not constant except approximately at small angles.'),
          ('At the critical angle all the light is totally internally reflected.', 'At exactly the critical angle the refracted ray grazes the surface (90°); total internal reflection occurs only for angles of incidence greater than the critical angle.')],
    evaluate=[('Optical fibres have completely replaced copper cables for communication.', ['fibres carry far higher bandwidth with low attenuation', 'immune to electromagnetic interference and harder to tap', 'lighter and cheaper per bit over long distances'], ['copper is still used for the "last mile", power supply and short links', 'fibres need precise splicing and optical-electrical conversion', 'dispersion and attenuation still limit range without repeaters'], 'Fibres dominate long-distance and high-bandwidth links, but copper remains common for short connections and power, so "completely replaced" overstates the case.')],
))


@R.add('ch01-st2', 'C3', (1, 4), 'numerical')
def c3_snell(rng, slot):
    m = pick(rng, list(MEDIA))
    n = MEDIA[m]
    th1 = rng.randint(15, 75)
    th2 = asind(sind(th1) / n)
    frame = rng.randrange(4)
    if frame == 0:
        return num(f'A ray of light in air is incident on the surface of {m} (n = {n}) at an angle of incidence of {th1}°. Calculate the angle of refraction.',
                   deg(th2), f'1.00 × sin {th1}° = {n} sin θ₂ (M1); θ₂ = {deg(th2)} (A1).', 2)
    if frame == 1:
        return num(f'A laser beam in air strikes a block of an unknown transparent plastic at an angle of incidence of {th1}°. The angle of refraction is {sf(th2)}°. Determine the refractive index of the plastic and the speed of light in it.',
                   f'n = {sf(n)}; v = {q(C / n, "m s⁻¹")}', f'n = sin {th1}°/sin {sf(th2)}° (M1) = {sf(n)} (A1); v = c/n = {q(C / n, "m s⁻¹")} (A1).', 3)
    if frame == 2:
        m2 = pick(rng, [x for x in MEDIA if MEDIA[x] < n] or ['water'])
        n2 = MEDIA[m2]
        if n2 >= n:
            return None
        crit = asind(n2 / n)
        th = rng.randint(10, max(11, int(crit) - 2))
        out = asind(n * sind(th) / n2)
        return num(f'Light travels in {m} (n = {n}) and meets a boundary with {m2} (n = {n2}) at an angle of incidence of {th}°. Calculate the angle of refraction in {m2}.',
                   deg(out), f'{n} sin {th}° = {n2} sin θ₂ (M1); θ₂ = {deg(out)} (A1).', 2)
    v = C / n
    return num(f'The speed of light in {m} is {q(v, "m s⁻¹")}. A ray in air enters it at {th1}° to the normal. Determine the angle of refraction.',
               deg(th2), f'n = c/v = {sf(n)} (M1); sin θ₂ = sin {th1}°/{sf(n)} (M1); θ₂ = {deg(th2)} (A1).', 3)


@R.add('ch01-st2', 'C3', (2, 5), 'numerical')
def c3_critical(rng, slot):
    m = pick(rng, list(MEDIA))
    n = MEDIA[m]
    outside, n2 = pick(rng, [('air', 1.00), ('water', 1.33)])
    if n2 >= n:
        outside, n2 = 'air', 1.00
    c_ = asind(n2 / n)
    th = rng.choice([int(c_) - rng.randint(3, 8), int(c_) + rng.randint(3, 8)])
    if slot.d <= 2:
        return num(f'Calculate the critical angle for light travelling in {m} (n = {n}) towards a boundary with {outside}.',
                   deg(c_), f'sin c = {n2}/{n} (M1); c = {deg(c_)} (A1).', 2)
    tir = th > c_
    return num(f'A ray travelling inside {m} (n = {n}) meets the boundary with {outside} (n = {n2}) at an angle of incidence of {th}°. Determine whether the ray is totally internally reflected, and justify your answer with a calculation.',
               f'critical angle {deg(c_)}; {"total internal reflection occurs" if tir else "the ray is refracted out, at " + deg(asind(n * sind(th) / n2))}',
               f'sin c = {n2}/{n} (M1), c = {deg(c_)} (A1); {th}° {">" if tir else "<"} c so {"TIR occurs" if tir else "the ray refracts out (some partial reflection)"} (R1).', 3)


@R.add('ch01-st2', 'C3', (1, 4), 'mcq')
def c3_snell_mcq(rng, slot):
    m = pick(rng, list(MEDIA))
    n = MEDIA[m]
    th1 = rng.choice([25, 30, 35, 40, 45, 50, 55, 60, 65])
    th2 = asind(sind(th1) / n)
    w = [th1 / n, asind(min(0.999, sind(90 - th1) / n)), 90 - th2]
    return nmcq(rng, f'Light in air is incident at {th1}° to the normal on a flat surface of {m} of refractive index {n}. What is the angle of refraction?',
                th2, w, '°', f'sin θ₂ = sin {th1}°/{n}; θ₂ = {deg(th2)}. Dividing the angle itself by n, or measuring from the surface, gives the distractors.')


@R.add('ch01-st2', 'C3', (2, 4), 'mcq')
def c3_crit_mcq(rng, slot):
    m = pick(rng, list(MEDIA))
    n = MEDIA[m]
    c_ = asind(1 / n)
    return nmcq(rng, f'What is the critical angle for light in {m} (n = {n}) at a boundary with air?', c_,
                [90 - c_, math.degrees(math.acos(1 / n)) + 1.0 if abs(math.degrees(math.acos(1 / n)) - (90 - c_)) < 0.05 else math.degrees(math.acos(1 / n)), math.degrees(math.atan(1 / n)), 90 / n],
                '°', f'sin c = 1/n = 1/{n}; c = {deg(c_)}.')


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step')
def c4_fibre(rng, slot):
    n1 = round(rng.uniform(1.46, 1.52), 3)
    n2 = round(n1 - rng.uniform(0.010, 0.030), 3)
    L = rng.choice([1.0, 2.0, 5.0, 10.0, 20.0])
    c_ = asind(n2 / n1)
    acc = asind(math.sqrt(n1 ** 2 - n2 ** 2))
    t_ax = L * 1000 * n1 / C
    t_max = t_ax * n1 / n2
    dt = t_max - t_ax
    frame = rng.randrange(2)
    if frame == 0:
        stem = (f'A step-index optical fibre has a core of refractive index {n1} and cladding of refractive index {n2}. (a) Calculate the critical angle at the core–cladding boundary. '
                f'(b) Show that the maximum angle of incidence in air at the end of the fibre for which light is guided is about {sf(acc, 2)}°. (c) The fibre is {sf(L, 2)} km long. Calculate the difference in travel time between a ray along the axis and a ray at the critical angle, and explain why this limits the data rate.')
        ans = f'(a) {deg(c_)}; (b) {deg(acc)}; (c) {q(dt, "s")} – pulses spread out (multipath dispersion) and overlap if sent too frequently'
        key = (f'(a) sin c = {n2}/{n1}, c = {deg(c_)} (M1 A1). (b) Angle in core at entry = 90° − c (M1); sin θₐ = {n1} sin(90° − c) = √(n₁² − n₂²) (M1), θₐ = {deg(acc)} (A1). '
               f'(c) axial t = n₁L/c = {q(t_ax, "s")}; critical ray path longer by n₁/n₂: t = {q(t_max, "s")} (M1); Δt = {q(dt, "s")} (A1); pulse broadening → pulses must be separated by more than Δt (R1).')
        return num(stem, ans, key, 8, 'multi_step', 'G5')
    stem = (f'An engineer must choose cladding for a fibre core of refractive index {n1} so that light entering the fibre end at up to {sf(acc, 3)}° from the axis is guided. '
            f'(a) Determine the maximum refractive index the cladding may have. (b) Explain, with reference to multipath dispersion, one advantage and one disadvantage of choosing a cladding index closer to {n1}.')
    ans = f'(a) n₂ = {sf(n2, 4)}; (b) closer indices → less multipath dispersion (higher data rate) but a smaller acceptance angle (less light collected, more bending loss)'
    key = (f'(a) sin θₐ = √(n₁² − n₂²) (M1); n₂ = √({n1}² − sin² {sf(acc, 3)}°) (M1) = {sf(n2, 4)} (A1). (b) smaller critical-angle range → smaller path differences → less pulse spreading (R1); '
           f'but smaller acceptance angle and greater leakage at bends (R1).')
    return num(stem, ans, key, 5, 'multi_step', 'G5')


R.mcqs('ch01-st2', 'C2', (1, 4), [
    ('Light passes from glass (n = 1.5) into water (n = 1.33). Which statement is correct?', 'The light speeds up and bends away from the normal.', ['The light slows down and bends towards the normal.', 'The light speeds up and bends towards the normal.', 'The frequency of the light increases.'], 'Lower refractive index → higher speed → bends away from the normal.'),
    ('The critical angle for a glass–air boundary is 42°. If the glass is placed in water instead of air, the critical angle', 'increases', ['decreases', 'stays at 42°', 'becomes undefined'], 'sin c = n_water/n_glass is larger than 1/n_glass, so c increases.'),
    ('A ray in glass meets the glass–air boundary at an angle slightly larger than the critical angle. Which is correct?', 'All of the light is reflected and none is refracted.', ['Most light is refracted along the surface.', 'Half the light is reflected.', 'The light is absorbed by the surface.'], 'Above the critical angle there is no refracted ray: total internal reflection.'),
    ('Monochromatic light enters glass from air. Which pair of quantities both decrease?', 'speed and wavelength', ['speed and frequency', 'frequency and wavelength', 'wavelength and photon energy'], 'v = c/n decreases and λ = v/f decreases; f is unchanged.'),
])

R.static('ch01-st2', 'C4', (3, 5), [
    ('A right-angled isosceles glass prism (angles 45°, 45°, 90°) is used in binoculars to turn light through 180°. (a) Determine the minimum refractive index of the glass for the light to be totally internally reflected at each hypotenuse face. (b) Explain why prisms are preferred to silvered mirrors in high-quality instruments. (c) Discuss what would happen if the prism were immersed in water (n = 1.33) and its index were 1.52.',
     '(a) n ≥ 1/sin 45° = 1.41; (b) TIR reflects almost 100 % with no tarnishing or double images; (c) critical angle becomes sin⁻¹(1.33/1.52) = 61°, so 45° incidence no longer gives TIR – light escapes into the water.',
     'Angle of incidence at the face is 45° (M1); n sin 45° ≥ 1 → n ≥ 1.41 (A1); TIR loses no energy, no coating to degrade (R1); new critical angle 61° calculated (M1); 45° < 61°, so TIR fails (R1).'),
    ('Evaluate the use of a semicircular glass block, rather than a rectangular block, to measure the critical angle of glass in a school laboratory.',
     'A semicircular block lets the ray enter along a radius at the curved face without refraction, so the angle at the flat face can be varied smoothly and the refracted ray observed grazing the surface; with a rectangular block light cannot reach the critical angle at the far face after refracting in. Limitations: judging the exact grazing position is subjective, the beam has finite width and the block’s centre must be marked accurately.',
     'Ray along the radius is undeviated at the curved surface (R1); angle at the flat face can be adjusted until refraction angle = 90° (R1); rectangular block limits the internal angle (R1); random/systematic uncertainty in locating the grazing ray (R1); suggestion such as repeating and averaging or finding c from a graph (R1).'),
], type='multi_step', marks=5)

linearise('ch01-st2', [
    ('n₁ sin θ₁ = n₂ sin θ₂ for light entering a glass block from air', 'sin θ₁', 'sin θ₂', 'the refractive index of the glass', 'A straight line through the origin confirms Snell’s law.'),
    ('v = c/n for light in a series of sugar solutions of different concentration', 'n', 'concentration', 'the rate of change of refractive index with concentration', 'The intercept is the refractive index of pure water (≈ 1.33).'),
])


def _snell_spec(rng):
    n = round(rng.uniform(1.45, 1.60), 2)
    th1 = [10, 20, 30, 40, 50, 60]
    th2 = [round(asind(sind(a) / n) + rng.uniform(-0.6, 0.6)) for a in th1]
    return dict(intro=f'In an experiment to find the refractive index of a glass block, the angle of incidence θ₁ in air and angle of refraction θ₂ in the glass were measured with a protractor (uncertainty ±1°).',
                xname='θ₁', xunit='°', yname='θ₂', yunit='°', xs=th1, ys=th2, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b}',
                plot_x=lambda a: sind(a), plot_y=lambda b: sind(b), plot_label='sin θ₂ (y) against sin θ₁ (x)', what='the refractive index of the glass',
                what_short='the refractive index', gunit='', deduce=lambda m_, b_: (1 / m_, '', 'n = 1/gradient'))


gradient_fit('ch01-st2', _snell_spec)


R.facts('ch01-st3', F(
    terms=[('diffraction', 'the spreading of a wave as it passes through an aperture or around an obstacle'),
           ('principle of superposition', 'when two or more waves meet, the resultant displacement at any point is the vector sum of the individual displacements'),
           ('coherent sources', 'sources that emit waves of the same frequency with a constant phase difference'),
           ('constructive interference', 'superposition of waves arriving in phase, giving a resultant amplitude equal to the sum of the amplitudes'),
           ('destructive interference', 'superposition of waves arriving in antiphase, giving a resultant amplitude equal to the difference of the amplitudes')],
    facts=[('Diffraction of a wave through a gap is most noticeable when the width of the gap is', 'similar to the wavelength', ['much larger than the wavelength', 'much smaller than the amplitude', 'equal to the amplitude'], 'Spreading is greatest when gap ≈ λ.'),
           ('What happens to the frequency of a wave as it diffracts through a gap?', 'It is unchanged.', ['It increases.', 'It decreases.', 'It halves.'], 'Diffraction changes the shape of the wavefronts, not speed, frequency or wavelength.'),
           ('Two waves of amplitude 3 cm and 5 cm meet in antiphase. What is the resultant amplitude?', '2 cm', ['8 cm', '0 cm', '4 cm'], 'Antiphase: 5 − 3 = 2 cm.'),
           ('Why can you hear someone talking around a corner but not see them?', 'Sound wavelengths (≈ 1 m) are comparable to doorways, light wavelengths are far smaller', ['Sound travels faster than light', 'Light cannot be diffracted', 'Sound is a transverse wave'], 'Diffraction is significant only when λ is comparable to the obstacle or gap.')],
    why=[('Explain why sustained interference requires coherent sources.', 'If the phase difference between the sources changed randomly, the positions of maxima and minima would move continuously and the pattern would average out; a constant phase difference keeps them fixed.'),
         ('Explain why long-wave radio signals can be received behind hills where FM signals cannot.', 'Long-wave radio has wavelengths of the order of kilometres, comparable to hills, so it diffracts strongly around them; FM wavelengths (~3 m) are much smaller, so diffraction is weak and hills cast a "radio shadow".'),
         ('Explain why energy is conserved in an interference pattern even though there are points of zero intensity.', 'Energy is redistributed: intensity missing from minima appears at maxima (where intensity ∝ (2A)² = 4A²), so the average intensity is unchanged.'),
         ('Explain why the wavelength does not change when a wave diffracts through a gap.', 'The wave stays in the same medium, so its speed is unchanged, and the frequency is set by the source; hence λ = v/f is unchanged.')],
    contrast=[('diffraction', 'refraction', 'Diffraction is spreading at an aperture or edge in the same medium, with no change of speed; refraction is a change of direction caused by a change of speed at a boundary between media.'),
              ('constructive interference', 'destructive interference', 'Constructive: waves arrive in phase (path difference nλ) and amplitudes add; destructive: waves arrive in antiphase (path difference (n + ½)λ) and amplitudes subtract.')],
    misc=[('Two waves that superpose destructively destroy each other’s energy permanently.', 'Superposition is temporary: after crossing, each wave continues unchanged; energy is redistributed, not destroyed.'),
          ('A narrower gap always gives less diffraction.', 'A narrower gap (closer to λ) gives MORE spreading; only very wide gaps compared with λ give little diffraction.'),
          ('Interference only happens with light.', 'Interference is a property of all waves – sound, water waves, microwaves and matter waves (electrons) all show it.')],
    evaluate=[('Young’s observation of interference proved that light is a wave.', ['interference fringes are explained naturally by superposition of waves', 'the corpuscular model could not explain dark fringes'], ['the photoelectric effect later required a particle (photon) model', 'single photons still build up an interference pattern, so the wave picture alone is incomplete', 'evidence supports but never "proves" a theory (NOS)'], 'Interference was strong evidence for wave behaviour, but modern physics treats light with wave–particle duality; scientific evidence supports rather than proves models.')],
))


@R.add('ch01-st3', 'C3', (1, 4), 'numerical')
def c3_superpose(rng, slot):
    a1 = rng.randint(2, 9)
    a2 = rng.randint(2, 9)
    frame = rng.randrange(3)
    if frame == 0:
        s1, s2 = rng.choice([1, -1]), rng.choice([1, -1])
        res = s1 * a1 + s2 * a2
        return num(f'Two pulses travel towards each other along a rope. One has a displacement of {"+" if s1 > 0 else "−"}{a1} cm and the other {"+" if s2 > 0 else "−"}{a2} cm at their peaks. State the displacement when the peaks coincide.',
                   f'{res:+d} cm'.replace('-', '−'), f'Principle of superposition: displacements add as vectors: ({s1 * a1}) + ({s2 * a2}) = {res} cm (A1).', 1)
    lam = rng.choice([0.40, 0.50, 0.60, 0.80, 1.20, 2.0])
    dx = round(lam * rng.choice([0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]), 3)
    ph = 2 * math.pi * dx / lam
    phd = (360 * dx / lam)
    kind = 'constructive' if abs((dx / lam) - round(dx / lam)) < 1e-9 else ('destructive' if abs((dx / lam) - round(dx / lam) - 0.5) < 1e-9 or abs((dx / lam) - round(dx / lam) + 0.5) < 1e-9 else 'neither fully constructive nor destructive')
    if frame == 1:
        return num(f'Two coherent sources emit waves in phase with wavelength {sf(lam, 2)} m. At point P the path difference is {sf(dx, 3)} m. Calculate the phase difference at P (in radians) and state the type of interference.',
                   f'{sf(ph, 3)} rad ({sf(phd, 3)}°); {kind}', f'φ = 2πΔx/λ = 2π × {sf(dx, 3)}/{sf(lam, 2)} (M1) = {sf(ph, 3)} rad (A1); {kind} (R1).', 3)
    A = a1
    res = 2 * A * abs(math.cos(ph / 2))
    return num(f'Two waves of equal amplitude {A} mm and wavelength {sf(lam, 2)} m meet at a point with a path difference of {sf(dx, 3)} m. Determine the resultant amplitude.',
               q(res, 'mm', 2), f'Phase difference = 2π × {sf(dx, 3)}/{sf(lam, 2)} = {sf(ph, 3)} rad (M1); resultant amplitude = 2A|cos(φ/2)| = {q(res, "mm", 2)} (A1).', 2)


@R.add('ch01-st3', 'C2', (2, 4), 'explain')
def c2_diffraction_predict(rng, slot):
    situations = [
        ('the gap in a ripple-tank barrier is reduced from 6 cm to 2 cm while the wavelength stays at 1.5 cm', 'more', 'the gap is now closer to the wavelength'),
        ('the frequency of the ripple-tank dipper is increased while the gap stays the same', 'less', 'higher frequency gives a shorter wavelength (λ = v/f), smaller compared with the gap'),
        ('a loudspeaker playing a low note of 200 Hz is replaced by a whistle at 4000 Hz in the same doorway', 'less', 'the 4000 Hz sound has a wavelength of about 8.5 cm, much smaller than the doorway, compared with 1.7 m at 200 Hz'),
        ('red laser light through a narrow slit is replaced by blue laser light', 'less', 'blue light has a shorter wavelength, so θ ≈ λ/b is smaller'),
        ('the water in a ripple tank is made shallower with the same frequency and gap', 'less', 'the waves slow down, so the wavelength decreases relative to the gap'),
        ('a harbour entrance is narrowed from 200 m to 60 m for ocean waves of wavelength 50 m', 'more', 'the gap becomes comparable to the wavelength'),
    ]
    sit, more, reason = pick(rng, situations)
    stem = rng.choice([f'Predict and explain how the diffraction pattern changes when {sit}.',
                       f'Explain whether the waves spread out more or less after the gap when {sit}.'])
    return dict(stem=stem, answer=f'The waves spread {more} after the gap, because {reason}.', type='explain', marks=2,
                markingKey=f'Spreading {more} (A1); because {reason} – diffraction depends on λ/gap (R1).')


@R.add('ch01-st3', 'C3', (1, 3), 'mcq')
def c3_phase_mcq(rng, slot):
    lam = rng.choice([2.0, 4.0, 6.0, 8.0, 12.0])
    frac_ = rng.choice([0.25, 0.75, 1.5, 0.5, 1.25])
    dx = lam * frac_
    ph = 360 * frac_ % 360
    return nmcq(rng, f'Two coherent waves of wavelength {sf(lam, 2)} cm, emitted in phase, meet with a path difference of {sf(dx, 3)} cm. What is their phase difference (between 0° and 360°)?',
                ph if ph else 360, [180 * frac_ % 360 or 90, (360 - ph) if ph != 180 else 90, 360 * frac_ if 360 * frac_ != ph else ph + 45], '°',
                f'Phase difference = 360° × Δx/λ = 360° × {frac_} = {360 * frac_:g}°, i.e. {ph:g}° within one cycle.', n=3)


R.mcqs('ch01-st3', 'C2', (1, 4), [
    ('Two loudspeakers connected to the same signal generator produce a pattern of loud and quiet regions. If the generator frequency is doubled, the spacing between loud regions', 'roughly halves', ['roughly doubles', 'is unchanged', 'becomes zero'], 'λ halves, so the positions where path difference = nλ move closer together.'),
    ('Two light bulbs do not produce an observable interference pattern because they', 'are not coherent', ['have different amplitudes', 'emit transverse waves', 'are too bright'], 'Their phase relationship changes randomly, so fringes average out.'),
    ('At a point of total destructive interference between two waves of equal amplitude, the intensity is', 'zero', ['half the intensity of one wave', 'equal to the intensity of one wave', 'twice the intensity of one wave'], 'Resultant amplitude is zero, so intensity is zero.'),
    ('Which observation is evidence for the wave nature of a beam?', 'it produces a diffraction pattern after passing through a narrow gap', ['it travels in straight lines', 'it carries energy', 'it can be reflected from a mirror'], 'Diffraction and interference are characteristic wave behaviours.'),
])

R.static('ch01-st3', 'C4', (3, 5), [
    ('Two loudspeakers, 1.5 m apart, are driven in phase at 680 Hz (speed of sound 340 m s⁻¹). A student walks along a line parallel to the speakers 4.0 m away. (a) Calculate the wavelength. (b) Explain why the sound intensity rises and falls. (c) Explain why the minima are not completely silent in a real classroom.',
     '(a) 0.50 m; (b) the path difference to the two speakers changes along the line; where it equals nλ there is constructive interference (loud), where (n + ½)λ destructive (quiet); (c) reflections from walls, unequal distances so unequal amplitudes, and background noise.',
     'λ = v/f = 0.50 m (A1); path difference varies (R1); nλ loud, (n + ½)λ quiet (R1); amplitudes at the minimum are unequal because distances differ (R1); reflections/background noise (R1).'),
    ('Noise-cancelling headphones use a microphone to detect ambient sound and emit a sound wave to cancel it. Discuss the physics of this method and explain why it works better for low-frequency engine hum than for high-frequency speech.',
     'The headphone produces a wave of equal amplitude in antiphase with the incoming sound, so superposition gives near-zero resultant displacement at the ear. For low frequencies the wavelength is long and the waveform changes slowly, so small time delays or position differences cause only small phase errors; at high frequencies, wavelengths are short (a few cm) and processing delays produce large phase errors, so cancellation fails.',
     'Antiphase wave of equal amplitude (M1); superposition gives destructive interference (R1); requires coherent (matched) signal, continuous processing (R1); phase error = 2πΔt·f grows with frequency (R1); conclusion supported (A1).'),
], type='multi_step', marks=5)

repeat_readings('ch01-st3', 'the angular width of the central diffraction maximum', '°', 3.0, 8.0, 1,
                ['shone a laser through an adjustable slit and measured the pattern on a screen.',
                 'used a microwave transmitter and a receiver on a turntable to map diffraction through a metal gap.'])


R.facts('ch01-st4', F(
    terms=[('path difference', 'the difference in the distances travelled by two waves from their sources to a point'),
           ('fringe spacing', 'the distance between the centres of adjacent bright (or dark) fringes, s = λD/d in a double-slit pattern'),
           ('order of a fringe', 'the integer n such that the path difference to the fringe is nλ for a bright fringe')],
    facts=[('In a double-slit experiment, which change increases the fringe spacing?', 'moving the screen further from the slits', ['moving the slits closer to the light source', 'using slits that are further apart', 'using light of shorter wavelength'], 's = λD/d increases with D.'),
           ('For a dark fringe in a two-source interference pattern (sources in phase), the path difference is', '(n + ½)λ', ['nλ', '2nλ', 'λ/n'], 'Antiphase arrival requires a half-wavelength odd multiple.'),
           ('What happens to a double-slit pattern if white light is used?', 'The central fringe is white and other fringes show coloured edges.', ['No fringes are seen.', 'All fringes are white.', 'The central fringe is dark.'], 'Every wavelength has a maximum at the centre, but s ∝ λ separates the colours elsewhere.'),
           ('Young’s double-slit formula s = λD/d is valid when', 'D is much larger than d and angles are small', ['d is larger than D', 'the light is white', 'the slits are wider than the wavelength'], 'The small-angle approximation tan θ ≈ sin θ is used.')],
    why=[('Explain why the light from the two slits in Young’s experiment is coherent.', 'Both slits are illuminated by the same wavefront from a single (laser or slit) source, so the light leaving them has the same frequency and a constant phase difference.'),
         ('Explain why the central fringe of a double-slit pattern is bright.', 'At the centre the distances from both slits are equal, so the path difference is zero and the waves arrive in phase, interfering constructively.'),
         ('Explain why the fringes become further apart when red light replaces green light.', 'Red light has a longer wavelength; the path difference needed for each successive bright fringe (λ) is larger, so the fringes occur at larger angles: s = λD/d increases.'),
         ('Explain why it is better to measure the distance across several fringes than across one.', 'The absolute uncertainty in the ruler reading is about the same, so measuring over n fringes divides the percentage uncertainty in s by roughly n.')],
    contrast=[('path difference', 'phase difference', 'Path difference is a distance (in m) between the routes of two waves; phase difference is the corresponding fraction of a cycle, φ = 2πΔx/λ (in rad).'),
              ('a double-slit pattern', 'a single-slit pattern', 'A double-slit pattern has equally spaced fringes of (nearly) equal width from interference of two coherent sources; a single-slit pattern has a central maximum twice as wide as the others and intensity falling rapidly outwards, from diffraction across one slit.')],
    misc=[('Bright fringes occur where the path difference is λ/2.', 'Bright fringes need path difference nλ (whole wavelengths); λ/2 gives a dark fringe.'),
          ('Increasing the slit separation spreads the fringes further apart.', 's = λD/d: increasing d makes the fringes closer together.'),
          ('Two separate lasers of the same colour will give stable Young’s fringes.', 'Two independent lasers are not phase-locked; their phase difference drifts, so stable fringes are not normally observed.')],
    evaluate=[('Young’s double-slit experiment is the best school method for measuring the wavelength of laser light.', ['simple apparatus and a direct formula', 'measuring across many fringes reduces uncertainty'], ['fringes are close together, so D must be large', 'slit separation d is hard to measure precisely', 'a diffraction grating gives sharper maxima at larger angles and smaller uncertainty'], 'The double slit is a valid method, but a diffraction grating usually gives a lower percentage uncertainty, so it is not the best method.')],
))


@R.add('ch01-st4', 'C3', (1, 5), 'numerical')
def c3_young(rng, slot):
    src = pick(rng, [('a red laser', 633), ('a green laser', 532), ('a violet laser', 405), ('a sodium lamp with a filter', 589), ('a red laser pointer', 650)])
    lam = src[1] * 1e-9
    d = rng.choice([0.20, 0.25, 0.30, 0.40, 0.50]) * 1e-3
    D = rng.choice([1.50, 2.00, 2.50, 3.00, 3.50, 4.00])
    s = lam * D / d
    frame = rng.randrange(4)
    if frame == 0:
        return num(f'Light from {src[0]} of wavelength {src[1]} nm illuminates two slits {sf(d * 1e3, 2)} mm apart. The screen is {sf(D, 3)} m away. Calculate the fringe spacing.',
                   q(s * 1e3, 'mm'), f's = λD/d = {src[1]} × 10⁻⁹ × {sf(D, 3)}/{sf(d, 2)} (M1) = {q(s * 1e3, "mm")} (A1).', 2)
    if frame == 1:
        N = rng.choice([5, 8, 10, 12])
        x = N * s
        return num(f'In a double-slit experiment with slit separation {sf(d * 1e3, 2)} mm and screen distance {sf(D, 3)} m, {N + 1} consecutive bright fringes span {sf(x * 1e3, 3)} mm. Determine the wavelength of the light.',
                   q(lam * 1e9, 'nm'), f'{N + 1} bright fringes = {N} spacings, s = {sf(x * 1e3, 3)}/{N} mm (M1); λ = sd/D (M1) = {q(lam * 1e9, "nm")} (A1).', 3)
    if frame == 2:
        return num(f'A student wants a fringe spacing of {sf(s * 1e3, 2)} mm on a screen {sf(D, 3)} m from a double slit illuminated with {src[1]} nm light. Calculate the slit separation needed.',
                   q(lam * D / round(s, 5) * 1e3, 'mm', 2), f'd = λD/s (M1) = {q(lam * D / round(s, 5) * 1e3, "mm", 2)} (A1).', 2)
    lam_m = rng.choice([2.8, 3.0, 3.2]) * 1e-2
    dm = rng.choice([0.10, 0.12, 0.15])
    th = asind(lam_m / dm)
    return num(f'Microwaves of wavelength {sf(lam_m * 100, 2)} cm pass through two gaps {sf(dm * 100, 2)} cm apart in a metal sheet. Calculate the angle from the centre line to the first-order maximum. (The small-angle formula is not valid here.)',
               deg(th), f'd sin θ = nλ with n = 1 (M1); θ = sin⁻¹({sf(lam_m, 2)}/{sf(dm, 2)}) = {deg(th)} (A1).', 2)


@R.add('ch01-st4', 'C3', (2, 4), 'numerical')
def c3_path_point(rng, slot):
    lam = rng.choice([0.25, 0.40, 0.50, 0.68, 0.85, 1.0])
    k = rng.choice([1, 1.5, 2, 2.5, 3, 3.5])
    d1 = round(rng.uniform(3, 8), 2)
    d2 = round(d1 + k * lam, 3)
    bright = float(k).is_integer()
    f = 340 / lam
    who = name(rng)
    return num(f'Two loudspeakers driven in phase emit sound of frequency {sf(f, 3)} Hz (speed of sound 340 m s⁻¹). {who} stands {sf(d1, 3)} m from one speaker and {sf(d2, 4)} m from the other. Determine whether {who} hears a loud or a quiet sound.',
               f'path difference = {sf(k * lam, 3)} m = {k:g}λ, so {"loud (constructive)" if bright else "quiet (destructive)"}',
               f'λ = 340/{sf(f, 3)} = {sf(lam, 2)} m (A1); path difference = {sf(k * lam, 3)} m (M1); = {k:g}λ, {"whole number → constructive" if bright else "odd multiple of λ/2 → destructive"} (R1).', 3)


@R.add('ch01-st4', 'C3', (1, 4), 'mcq')
def c3_young_mcq(rng, slot):
    lam = rng.choice([450, 500, 550, 600, 650])
    d = rng.choice([0.2, 0.25, 0.4, 0.5])
    D = rng.choice([1.0, 1.2, 1.6, 2.0, 2.5])
    s = lam * 1e-9 * D / (d * 1e-3) * 1e3
    return nmcq(rng, f'Monochromatic light of wavelength {lam} nm passes through two slits {d} mm apart. What is the fringe separation on a screen {D} m away?',
                s, [lam * 1e-9 * d * 1e-3 / D * 1e3 * 1e6, s / 2, s * 1000 / 1000 * 10], 'mm',
                f's = λD/d = {lam} × 10⁻⁹ × {D}/({d} × 10⁻³) = {q(s, "mm")}.')


@R.add('ch01-st4', 'C2', (2, 4), 'explain')
def c2_young_change(rng, slot):
    ch = [('the slit separation is halved', 'doubles', 's ∝ 1/d'),
          ('the screen is moved twice as far away', 'doubles', 's ∝ D'),
          ('blue light replaces red light', 'decreases', 's ∝ λ and blue light has a shorter wavelength'),
          ('the whole apparatus is immersed in water (n = 1.33)', 'decreases by a factor of 1.33', 'the wavelength in water is λ/1.33'),
          ('one slit is covered with a filter that halves its intensity', 'is unchanged, but the dark fringes are no longer completely dark', 'the amplitudes are unequal, so cancellation is incomplete; spacing depends only on λ, D and d'),
          ('the slits are made narrower but kept the same distance apart', 'is unchanged, but the pattern becomes dimmer and the fringes extend over a wider region', 'narrower slits diffract more, widening the single-slit envelope')]
    c, eff, why = pick(rng, ch)
    return dict(stem=f'In a Young’s double-slit experiment, state and explain the effect on the fringe spacing when {c}.', answer=f'The fringe spacing {eff}; {why}.',
                markingKey=f'Effect: spacing {eff} (A1); reason: {why} (R1).', type='explain', marks=2)


R.mcqs('ch01-st4', 'C2', (1, 4), [
    ('In a double-slit experiment the third bright fringe from the centre is at point P. What is the path difference to P?', '3λ', ['1.5λ', '2.5λ', '6λ'], 'nth bright fringe: path difference nλ with n = 3.'),
    ('The second dark fringe from the centre corresponds to a path difference of', '1.5λ', ['2λ', '0.5λ', '2.5λ'], 'Dark fringes at (n + ½)λ: first at 0.5λ, second at 1.5λ.'),
    ('One of the two slits is covered. Compared with the double-slit pattern, the screen shows', 'a single-slit diffraction pattern with no regularly spaced interference fringes', ['the same fringes but dimmer', 'the same fringes twice as far apart', 'complete darkness'], 'Interference needs two sources; one slit gives only diffraction.'),
    ('Why does a laser make Young’s experiment easier than a filament lamp?', 'Its light is monochromatic and coherent across the slits', ['Its light travels faster', 'Its light has a longer wavelength', 'It produces circular wavefronts'], 'A laser gives a single wavelength and a constant phase relationship.'),
])


def _young_unc(rng, slot):
    lam = rng.choice([532, 633, 650]) * 1e-9
    d = rng.choice([0.25, 0.30, 0.50]) * 1e-3
    D = round(rng.uniform(1.5, 3.0), 2)
    N = 10
    x = N * lam * D / d
    x_mm = round(x * 1e3, 0)
    ux, uD, ud = 1.0, 0.01, 0.01e-3
    lam_c = (x_mm / 1e3 / N) * d / D
    p = 100 * (ux / x_mm + uD / D + ud / d)
    stem = (f'A student measures the wavelength of a laser with a double slit. Data: distance across 10 fringe spacings x = ({x_mm:.0f} ± 1) mm; slit-to-screen distance D = ({D:.2f} ± 0.01) m; '
            f'slit separation d = ({d * 1e3:.2f} ± 0.01) mm.\n\n(a) Calculate the wavelength. [2]\n(b) Determine the percentage uncertainty in the wavelength. [2]\n(c) Identify which measurement contributes most to the uncertainty and suggest one improvement. [1]')
    contrib = max([('x', ux / x_mm), ('D', uD / D), ('d', ud / d)], key=lambda t: t[1])[0]
    imp = {'x': 'measure across more fringes or use a travelling microscope/vernier calliper', 'D': 'increase D or use a longer, finer tape', 'd': 'measure d with a travelling microscope or use a slit pair with a larger, better-known separation'}[contrib]
    ans = f'(a) λ = {q(lam_c * 1e9, "nm")}; (b) {p:.1f} %; (c) {contrib} – {imp}'
    key = (f'(a) s = x/10 = {x_mm / 10:.1f} mm (M1); λ = sd/D = {q(lam_c * 1e9, "nm")} (A1). (b) %Δλ = %Δx + %ΔD + %Δd = {100 * ux / x_mm:.1f} + {100 * uD / D:.1f} + {100 * ud / d:.1f} (M1) = {p:.1f} % (A1). '
           f'(c) largest contribution from {contrib}; {imp} (A1).')
    return dict(stem=stem, answer=ans, markingKey=key, type='case', marks=5, gap='G7')


R.t.setdefault('ch01-st4', []).append(T(('C3', 'C4'), (3, 5), _young_unc, 'case', 'p1b', 'young_unc'))
R.t.setdefault('ch01-st4', []).append(T(('C4',), (3, 5), _young_unc, 'case', None, 'young_unc_bank'))


R.facts('ch01-st5', F(
    terms=[('diffraction grating', 'a plate with a large number of equally spaced parallel slits that produces sharp, widely separated maxima at angles given by n λ = d sin θ'),
           ('grating spacing', 'the distance between adjacent slits of a grating, d = 1/N where N is the number of lines per metre'),
           ('single-slit first minimum', 'the angle θ = λ/b at which waves from the two halves of a slit of width b cancel'),
           ('missing order', 'a double-slit (or grating) maximum that is absent because it coincides with a minimum of the single-slit diffraction envelope')],
    facts=[('Compared with a double slit, a diffraction grating with the same slit spacing produces maxima that are', 'sharper and brighter at the same angles', ['wider and dimmer', 'at smaller angles', 'equally spaced on the screen at all angles'], 'Many slits narrow the maxima; positions still obey d sin θ = nλ.'),
           ('The width of the central maximum of a single-slit pattern is', 'twice the width of each subsidiary maximum', ['equal to the subsidiary maxima', 'half the subsidiary maxima', 'independent of the slit width'], 'Central max spans −λ/b to +λ/b.'),
           ('When the slit width b of a single slit is halved, the angular width of the central maximum', 'doubles', ['halves', 'is unchanged', 'quadruples'], 'θ = λ/b.'),
           ('In a double-slit pattern observed carefully, the intensity of the interference fringes varies because', 'it is modulated by the single-slit diffraction envelope of each slit', ['the slits are incoherent', 'the wavelength changes across the screen', 'the screen absorbs light unevenly'], 'Each slit has finite width, so the fringes lie under a diffraction envelope.')],
    why=[('Explain why the maxima produced by a diffraction grating are much sharper than those from a double slit.', 'With many slits, waves from all slits are in phase only at angles very close to d sin θ = nλ; a tiny change in angle makes contributions from distant slits cancel, so each maximum is very narrow and, with more slits, brighter.'),
         ('Explain why a diffraction grating is used in spectrometers to measure wavelengths.', 'Its maxima are sharp and at large, well-defined angles, so angles can be measured precisely; different wavelengths are separated into distinct lines, giving accurate λ = d sin θ / n.'),
         ('Explain why there is a maximum number of orders produced by a grating.', 'sin θ cannot exceed 1, so n ≤ d/λ; the highest order is the largest integer below d/λ.'),
         ('Explain why the first minimum of a single slit occurs at θ = λ/b.', 'Divide the slit into two halves; at this angle each point in the top half has a partner in the bottom half with path difference λ/2, so all pairs cancel.')],
    contrast=[('a single-slit diffraction pattern', 'a diffraction grating pattern', 'A single slit gives a broad central maximum (width 2λ/b) and weak subsidiary maxima; a grating gives very sharp, bright principal maxima at angles where d sin θ = nλ with darkness in between.')],
    misc=[('A grating with more lines per millimetre produces maxima at smaller angles.', 'More lines per mm means smaller d, so sin θ = nλ/d is larger: maxima at larger angles.'),
          ('A wider slit gives a wider central diffraction maximum.', 'θ = λ/b: a wider slit gives a narrower central maximum.'),
          ('The small-angle formula s = λD/d is used to find the angles from a diffraction grating.', 'Grating angles are large, so the exact relation n λ = d sin θ must be used.')],
    evaluate=[('Gratings with as many lines per millimetre as possible are always best for a spectrometer.', ['smaller d spreads the spectrum over larger angles, improving angular resolution', 'more illuminated lines give sharper maxima'], ['fewer orders are available (n ≤ d/λ)', 'high orders may be lost entirely and the spectrum may not fit the instrument', 'manufacturing cost'], 'Higher line density helps resolution, but the optimum depends on the wavelength range and number of orders required.')],
))


@R.add('ch01-st5', 'C3', (1, 5), 'numerical')
def c3_grating(rng, slot):
    N = rng.choice([100, 300, 500, 600, 750])
    d = 1e-3 / N
    lam_nm = rng.choice([405, 450, 486, 532, 589, 633, 656])
    lam = lam_nm * 1e-9
    nmax = int(d / lam)
    frame = rng.randrange(4)
    n = rng.randint(1, max(1, min(3, nmax)))
    th = asind(n * lam / d)
    if frame == 0:
        return num(f'Light of wavelength {lam_nm} nm is incident normally on a grating with {N} lines per mm. Calculate the angle of the order-{n} maximum.',
                   deg(th), f'd = 1/{N} mm = {q(d, "m")} (A1); sin θ = nλ/d = {n} × {lam_nm} × 10⁻⁹/{sf(d)} (M1); θ = {deg(th)} (A1).', 3)
    if frame == 1:
        return num(f'A diffraction grating has {N} lines per mm. Determine the highest order maximum that can be observed for light of wavelength {lam_nm} nm.',
                   f'n = {nmax}', f'd = {q(d, "m")}; n ≤ d/λ = {sf(d / lam)} (M1); highest whole order n = {nmax} (A1).', 2)
    if frame == 2:
        return num(f'The first-order maximum for a spectral line seen through a {N} lines per mm grating is at {sf(asind(lam / d), 3)}°. Calculate the wavelength of the line.',
                   q(lam_nm, 'nm'), f'λ = d sin θ = ({q(d, "m")}) × sin {sf(asind(lam / d), 3)}° (M1) = {q(lam_nm, "nm")} (A1).', 2)
    b = rng.choice([0.05, 0.08, 0.10, 0.12, 0.20]) * 1e-3
    D = rng.choice([1.5, 2.0, 2.5, 3.0])
    w = 2 * lam * D / b
    return num(f'Light of wavelength {lam_nm} nm passes through a single slit of width {sf(b * 1e3, 2)} mm. Calculate the angle of the first minimum and the width of the central maximum on a screen {sf(D, 2)} m away.',
               f'{q(lam / b, "rad")}; width {q(w * 1e3, "mm")}', f'θ = λ/b = {q(lam / b, "rad")} (M1 A1); width = 2Dθ = {q(w * 1e3, "mm")} (A1).', 3)


@R.add('ch01-st5', 'C4', (3, 5), 'multi_step')
def c4_grating_sodium(rng, slot):
    N = rng.choice([300, 500, 600])
    d = 1e-3 / N
    l1, l2 = 589.0e-9, 589.6e-9
    n = rng.choice([1, 2])
    if n * l2 / d >= 1:
        n = 1
    t1, t2 = asind(n * l1 / d), asind(n * l2 / d)
    return num(f'The sodium "D lines" have wavelengths 589.0 nm and 589.6 nm. Light from a sodium lamp falls normally on a grating with {N} lines per mm. (a) Calculate the angle of each line in order {n}. (b) Determine their angular separation. (c) Explain why a grating with more lines illuminated, rather than a double slit, is needed to see the two lines separately.',
               f'(a) {sf(t1, 5)}° and {sf(t2, 5)}°; (b) {sf(t2 - t1, 2)}°; (c) many slits make each maximum very narrow so the two close maxima do not overlap',
               f'd = {q(d, "m")} (A1); sin θ = nλ/d for each (M1), θ = {sf(t1, 5)}° and {sf(t2, 5)}° (A1); Δθ = {sf(t2 - t1, 2)}° (A1); grating maxima narrower than the separation, double-slit fringes far too broad (R1 R1).', 6, 'multi_step', 'G5')


@R.add('ch01-st5', 'C4', (3, 5), 'multi_step')
def c4_missing_order(rng, slot):
    ratio = rng.choice([2, 3, 4])
    b = rng.choice([0.04, 0.05, 0.06]) * 1e-3
    d = ratio * b
    lam_nm = rng.choice([532, 633])
    th1 = math.degrees(lam_nm * 1e-9 / b)
    return num(f'A double slit has slit width b = {sf(b * 1e3, 2)} mm and slit separation d = {sf(d * 1e3, 2)} mm and is lit with {lam_nm} nm laser light. (a) Calculate the angle of the first single-slit minimum. (b) Determine how many bright interference fringes lie within the central diffraction maximum. (c) Explain why the order-{ratio} fringe is missing.',
               f'(a) {q(lam_nm * 1e-9 / b, "rad")} ({deg(th1)}); (b) {2 * ratio - 1}; (c) the order-{ratio} maximum (d sin θ = {ratio}λ) falls at the same angle as the first single-slit minimum (b sin θ = λ)',
               f'(a) θ = λ/b (M1) = {q(lam_nm * 1e-9 / b, "rad")} (A1). (b) d/b = {ratio}, so orders −{ratio - 1} … +{ratio - 1}: {2 * ratio - 1} fringes (M1 A1). (c) at sin θ = λ/b = {ratio}λ/d the envelope is zero, so the interference maximum has zero intensity (R1).', 5, 'multi_step', 'G5')


@R.add('ch01-st5', 'C3', (1, 4), 'mcq')
def c3_grating_mcq(rng, slot):
    N = rng.choice([200, 300, 400, 500, 600])
    lam = rng.choice([450, 500, 550, 600, 650])
    d = 1e-3 / N
    th = asind(lam * 1e-9 / d)
    wr = [math.degrees(lam * 1e-9 / d) * 57.3 / 57.3 + 2.5, asind(min(0.99, 2 * lam * 1e-9 / d)), math.degrees(math.atan(lam * 1e-9 / d)) + 0.0 if abs(math.degrees(math.atan(lam * 1e-9 / d)) - th) > 0.05 else th + 4]
    return nmcq(rng, f'Light of wavelength {lam} nm is incident normally on a grating with {N} lines per mm. At what angle is the first-order maximum?',
                th, wr, '°', f'd = 1/{N} mm; sin θ = λ/d = {sf(lam * 1e-9 / d)}; θ = {deg(th)}.')


R.mcqs('ch01-st5', 'C2', (1, 4), [
    ('The number of lines per mm of a grating is doubled. The angle of the first-order maximum', 'increases, with sin θ doubling', ['halves', 'is unchanged', 'doubles exactly'], 'd halves so sin θ = λ/d doubles (the angle itself less than doubles).'),
    ('White light passes through a diffraction grating. In the first-order spectrum, which colour is deviated most?', 'red', ['violet', 'green', 'all equally'], 'sin θ ∝ λ: red has the longest visible wavelength.'),
    ('A single slit is illuminated with light of wavelength λ. The first minimum is at angle θ. The slit width is', 'λ/θ (θ in radians, small angle)', ['λθ', '2λ/θ', 'θ/λ'], 'θ = λ/b → b = λ/θ.'),
    ('Two-slit interference fringes are seen inside a single-slit diffraction envelope. If the slit width is reduced (slit separation fixed), the number of fringes within the central envelope', 'increases', ['decreases', 'is unchanged', 'becomes zero'], 'Envelope half-width λ/b grows while fringe spacing λ/d stays the same.'),
])

gradient_fit('ch01-st5', lambda rng: _grating_spec(rng))


def _grating_spec(rng):
    lam = rng.choice([532, 589, 633]) * 1e-9
    Ns = [100, 200, 300, 400, 500, 600]
    ths = [round(asind(lam * N_ * 1e3) + rng.uniform(-0.2, 0.2), 1) for N_ in Ns]
    return dict(intro='A student shines a laser normally onto gratings with different numbers of lines per mm, N, and measures the angle θ of the first-order maximum. Theory: sin θ = λN.',
                xname='N', xunit='lines mm⁻¹', yname='θ', yunit='°', xs=Ns, ys=ths, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b:.1f}',
                plot_x=lambda a: a * 1e3, plot_y=lambda b: sind(b), plot_label='sin θ (y) against N (in lines per metre)', what='the wavelength of the laser',
                what_short='the wavelength', gunit='m', deduce=lambda m_, b_: (m_ * 1e9, 'nm', 'λ = gradient'))


# =============================================================================================
# ch02 C.4 Standing waves and resonance
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('standing wave', 'a wave pattern formed by the superposition of two waves of the same frequency and amplitude travelling in opposite directions, in which energy is not transferred along the wave'),
           ('node', 'a point on a standing wave where the displacement is always zero'),
           ('antinode', 'a point on a standing wave where the amplitude of oscillation is a maximum'),
           ('travelling wave', 'a wave that transfers energy from one place to another through a medium or space')],
    facts=[('What is the distance between two adjacent nodes in a standing wave of wavelength λ?', 'λ/2', ['λ', 'λ/4', '2λ'], 'Nodes are half a wavelength apart.'),
           ('What is the phase difference between two points in adjacent loops (on either side of one node) of a standing wave?', 'π rad', ['0', 'π/2 rad', '2π rad'], 'Points in adjacent loops oscillate in antiphase.'),
           ('What is the phase difference between any two points within the same loop of a standing wave?', '0', ['π/2 rad', 'π rad', 'it depends on their separation'], 'All points between adjacent nodes oscillate in phase.'),
           ('How far is a node from the nearest antinode?', 'λ/4', ['λ/2', 'λ', 'λ/8'], 'Antinodes lie midway between nodes.')],
    why=[('Explain how a standing wave is formed on a string fixed at both ends.', 'A wave travels along the string and is reflected at the fixed ends; the incident and reflected waves have the same frequency, speed and (approximately) amplitude and travel in opposite directions, so they superpose to give fixed nodes and antinodes.'),
         ('Explain why a standing wave does not transfer energy along the medium.', 'The two component travelling waves carry equal energy in opposite directions; at nodes there is no motion, so no net energy passes along the medium – energy is stored, oscillating between kinetic and potential forms in each loop.'),
         ('Explain why the amplitude varies with position along a standing wave but is constant along a travelling wave.', 'In a standing wave the phase difference between the two component waves depends on position, so they interfere constructively at antinodes and destructively at nodes; in a travelling wave every point receives the same wave with the same amplitude.'),
         ('Explain why microwaves reflected from a metal plate produce a series of maxima and minima as a detector is moved towards the plate.', 'The incident and reflected microwaves superpose to form a standing wave; the detector registers maxima at antinodes and minima at nodes, which are λ/2 apart.')],
    contrast=[('a standing wave', 'a travelling wave', 'A standing wave has nodes and antinodes, amplitude that varies with position, all points between adjacent nodes in phase and no net energy transfer; a travelling wave has constant amplitude, phase that changes continuously along the wave and transfers energy.'),
              ('a node', 'an antinode', 'A node has zero amplitude at all times (destructive interference); an antinode has maximum amplitude (constructive interference); they are λ/4 apart.')],
    misc=[('Nodes are a wavelength apart.', 'Adjacent nodes are half a wavelength (λ/2) apart.'),
          ('All points on a standing wave oscillate with the same amplitude, like a travelling wave.', 'The amplitude varies from zero at nodes to a maximum at antinodes.'),
          ('In a standing wave, the energy travels from one end to the other.', 'There is no net energy transfer along a standing wave; energy is stored in the oscillating loops.')],
    evaluate=[('Standing waves are simply travelling waves that have stopped moving.', ['the pattern does appear stationary', 'it is made of travelling waves'], ['the medium still oscillates; only the pattern of nodes and antinodes is fixed', 'it results from superposition of two waves travelling in opposite directions', 'its properties (amplitude variation, phase relations, no energy transfer) differ fundamentally'], 'Misleading: a standing wave is a superposition of two travelling waves; the medium oscillates, only the pattern is stationary.')],
))


@R.add('ch02-st1', 'C3', (1, 4), 'numerical')
def c3_node_spacing(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        x = rng.choice([1.2, 1.4, 1.5, 1.6, 1.8])
        N = rng.choice([5, 6, 8, 10])
        dist = x * N
        lam = 2 * dist / N
        return num(f'A microwave detector moved along the line between a transmitter and a metal plate passes through {N + 1} consecutive minima over a distance of {sf(dist, 3)} cm. Calculate the wavelength and frequency of the microwaves.',
                   f'λ = {q(lam, "cm")}; f = {q(C / (lam / 100), "Hz")}', f'{N + 1} minima = {N} node spacings of λ/2 (M1); λ = 2 × {sf(dist, 3)}/{N} = {q(lam, "cm")} (A1); f = c/λ = {q(C / (lam / 100), "Hz")} (A1).', 3)
    if frame == 1:
        v = rng.choice([24, 30, 36, 48, 60, 72])
        f = rng.choice([20, 30, 40, 50, 60])
        return num(f'A standing wave forms on a stretched cord in which waves travel at {v} m s⁻¹. The vibrator frequency is {f} Hz. Calculate the distance between adjacent nodes.',
                   q(v / f / 2, 'm'), f'λ = v/f = {sf(v / f)} m (M1); node spacing = λ/2 = {q(v / f / 2, "m")} (A1).', 2)
    if frame == 2:
        f = rng.choice([256, 320, 400, 512, 640])
        v = 340
        return num(f'Sound of frequency {f} Hz from a loudspeaker is reflected by a wall, forming a standing wave (speed of sound 340 m s⁻¹). Calculate the distance between a node and the nearest antinode.',
                   q(v / f / 4, 'm'), f'λ = 340/{f} = {sf(v / f)} m (M1); node–antinode distance = λ/4 = {q(v / f / 4, "m")} (A1).', 2)
    lam = rng.choice([0.40, 0.60, 0.80, 1.20])
    x = round(lam * rng.choice([0.125, 0.375, 0.625, 0.875]), 3)
    A = rng.choice([4, 5, 6, 8])
    amp = A * abs(math.sin(2 * math.pi * x / lam))
    return num(f'A standing wave of wavelength {sf(lam, 2)} m has antinode amplitude {A} mm and a node at x = 0. Determine the amplitude of oscillation of the point at x = {sf(x, 3)} m.',
               q(amp, 'mm', 2), f'Amplitude = A|sin(2πx/λ)| (M1) = {A}|sin(2π × {sf(x, 3)}/{sf(lam, 2)})| = {q(amp, "mm", 2)} (A1).', 2)


@R.add('ch02-st1', 'C3', (1, 4), 'mcq')
def c3_node_mcq(rng, slot):
    L = rng.choice([0.60, 0.90, 1.20, 1.50, 1.80])
    loops = rng.choice([2, 3, 4, 5, 6])
    lam = 2 * L / loops
    return nmcq(rng, f'A string of length {sf(L, 2)} m fixed at both ends vibrates with {loops} loops. What is the wavelength?', lam,
                [L / loops, L * loops / 2, 2 * L / (loops + 1)], 'm', f'{loops} loops = {loops} × λ/2 = {sf(L, 2)} m, so λ = {q(lam, "m")}.')


R.mcqs('ch02-st1', 'C2', (1, 4), [
    ('Two points P and Q on a standing wave are 1.5λ apart and both are antinodes. Their phase difference is', 'π rad', ['0', '3π rad shown as 3π', 'π/2 rad'], '1.5λ = 3 loops; crossing an odd number of nodes gives antiphase.'),
    ('At the instant a string forming a standing wave is momentarily straight, the energy of the string is', 'entirely kinetic', ['entirely potential', 'zero', 'half kinetic and half potential'], 'When the displacement is zero everywhere, the points move at maximum speed.'),
    ('A standing wave can be formed with which pair of waves?', 'two waves of equal frequency travelling in opposite directions', ['two waves of different frequency in the same direction', 'a transverse and a longitudinal wave', 'two waves of equal frequency in the same direction'], 'Opposite directions and the same frequency are essential.'),
    ('Which property is the same for all points between two adjacent nodes?', 'phase', ['amplitude', 'displacement at each instant equal to the antinode', 'maximum speed'], 'All points in one loop oscillate in phase but with different amplitudes.'),
])

R.static('ch02-st1', 'C4', (3, 5), [
    ('A student sets up microwaves (from a 10.5 GHz transmitter) reflecting off a metal plate and finds detector minima are not of zero intensity, becoming deeper closer to the plate. (a) Calculate the expected distance between minima. (b) Explain why the minima are not zero. (c) Explain why they are deeper near the plate.',
     '(a) λ = 2.86 cm, so minima 1.43 cm apart; (b) the reflected wave has smaller amplitude than the incident wave (spreading and absorption), so cancellation is incomplete; (c) near the plate the reflected wave has travelled less distance and spread less, so its amplitude is closer to the incident amplitude.',
     'λ = c/f = 2.86 cm (M1), spacing λ/2 = 1.43 cm (A1); unequal amplitudes (R1); reflected wave weakened by spreading/partial reflection (R1); amplitudes nearly equal close to the plate (R1).'),
    ('Discuss how the standing wave pattern on a string differs from that of sound in a pipe, with reference to the type of wave, what the nodes represent and how the pattern can be detected.',
     'On a string the wave is transverse and nodes are points of zero transverse displacement, visible directly (or with a stroboscope). In a pipe the sound is longitudinal; displacement nodes are where air molecules do not move (pressure antinodes), detected with a microphone or Kundt’s tube dust; patterns are drawn as displacement envelopes but represent longitudinal motion.',
     'Transverse vs longitudinal (A1); displacement nodes and pressure antinodes coincide in pipes (R1); boundary conditions (fixed ends vs open/closed ends) (R1); detection methods compared (R1); recognition that drawn "loops" in pipes are a representation (R1).'),
], type='multi_step', marks=5)


def _micro_spec(rng):
    f_ = rng.choice([9.4, 10.0, 10.5, 11.2])
    lam = C / (f_ * 1e9) * 100
    ns = [1, 2, 3, 4, 5, 6]
    xs = [round(n_ * lam / 2 + 2.0 + rng.uniform(-0.05, 0.05), 2) for n_ in ns]
    return dict(intro=f'A microwave detector is moved away from a metal reflector. The position x of the n-th minimum (node) from a reference mark is recorded.',
                xname='n', xunit='–', yname='x', yunit='cm', xs=ns, ys=xs, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: a, plot_y=lambda b: b, plot_label='x (y) against n (x)', what='the wavelength of the microwaves', what_short='the wavelength',
                gunit='cm', deduce=lambda m_, b_: (2 * m_, 'cm', 'λ = 2 × gradient'))


gradient_fit('ch02-st1', _micro_spec)


R.facts('ch02-st2', F(
    terms=[('fundamental (first harmonic)', 'the lowest-frequency mode of standing wave that can be set up in a string or pipe'),
           ('harmonic', 'a standing-wave mode whose frequency is a whole-number multiple of the fundamental frequency'),
           ('closed pipe', 'a pipe with one end closed (a displacement node) and one end open (a displacement antinode)'),
           ('open pipe', 'a pipe open at both ends, with displacement antinodes at both ends')],
    facts=[('A pipe closed at one end has length L. What is the wavelength of its fundamental?', '4L', ['2L', 'L', 'L/2'], 'A node at the closed end and antinode at the open end: L = λ/4.'),
           ('Which harmonics can a pipe closed at one end produce?', 'odd harmonics only', ['even harmonics only', 'all harmonics', 'only the fundamental'], 'f = (2n − 1)v/4L.'),
           ('A string fixed at both ends has fundamental frequency f. What is the frequency of the third harmonic?', '3f', ['f/3', '9f', '1.5f'], 'All whole-number harmonics nf are possible on a string.'),
           ('A pipe open at both ends has length L. What is the wavelength of its fundamental?', '2L', ['4L', 'L', 'L/4'], 'Antinodes at both ends: L = λ/2.')],
    why=[('Explain why a pipe closed at one end produces only odd harmonics.', 'The closed end must be a displacement node and the open end an antinode, so the length must be an odd number of quarter-wavelengths (L = (2n − 1)λ/4); frequencies are therefore odd multiples of v/4L.'),
         ('Explain why a guitar string sounds a higher note when it is pressed against a fret.', 'Pressing at the fret shortens the vibrating length L; with the wave speed unchanged, the fundamental f = v/2L increases.'),
         ('Explain why the frequency of an organ pipe rises slightly on a hot day.', 'The speed of sound in air increases with temperature; the wavelengths are fixed by the pipe length, so f = v/λ increases.'),
         ('Explain why a closed pipe of length L has the same fundamental frequency as an open pipe of length 2L.', 'Closed: λ = 4L; open of length 2L: λ = 2(2L) = 4L; same wavelength and same speed of sound give the same frequency.')],
    contrast=[('a closed pipe', 'an open pipe', 'A closed pipe has a node at the closed end and an antinode at the open end, λ₁ = 4L and only odd harmonics; an open pipe has antinodes at both ends, λ₁ = 2L and all harmonics.'),
              ('the fundamental', 'the second harmonic of a string', 'The fundamental has one loop (L = λ/2); the second harmonic has two loops with a node at the centre (L = λ) and twice the frequency.')],
    misc=[('A closed pipe can play its second harmonic at twice the fundamental frequency.', 'A closed pipe has no even harmonics; the next mode after the fundamental is at 3f₁.'),
          ('Doubling the length of a string doubles its fundamental frequency.', 'f₁ = v/2L: doubling L halves the fundamental frequency.'),
          ('In an open pipe there are nodes at both open ends.', 'Open ends are displacement antinodes; the air there is free to move.')],
    evaluate=[('The resonance-tube method is an accurate way to measure the speed of sound in air.', ['two successive resonance lengths remove the unknown end correction', 'simple, cheap apparatus', 'tuning forks have precise frequencies'], ['judging the loudest point is subjective', 'end correction depends on tube diameter', 'temperature changes alter the speed during the experiment'], 'With successive resonances and repeat readings it can give v to within a few per cent – adequate, though less accurate than electronic time-of-flight methods.')],
))


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def c3_harmonics(rng, slot):
    frame = rng.randrange(5)
    v = rng.choice([336, 340, 343, 346])
    if frame == 0:
        L = rng.choice([0.30, 0.45, 0.60, 0.85, 1.20])
        n = rng.choice([1, 3, 5])
        f = n * v / (4 * L)
        return num(f'A pipe of length {sf(L, 2)} m is closed at one end. The speed of sound is {v} m s⁻¹. Calculate the frequency of the {["", "fundamental", "", "third harmonic", "", "fifth harmonic"][n]}.',
                   q(f, 'Hz'), f'Closed pipe: f = nv/4L with n odd (M1); f = {n} × {v}/(4 × {sf(L, 2)}) = {q(f, "Hz")} (A1).', 2)
    if frame == 1:
        L = rng.choice([0.32, 0.50, 0.66, 0.90])
        n = rng.choice([1, 2, 3, 4])
        f = n * v / (2 * L)
        return num(f'A flute can be modelled as a pipe of length {sf(L, 2)} m open at both ends. Calculate the frequency of harmonic number {n} (speed of sound {v} m s⁻¹).',
                   q(f, 'Hz'), f'Open pipe: f = nv/2L (M1) = {n} × {v}/(2 × {sf(L, 2)}) = {q(f, "Hz")} (A1).', 2)
    if frame == 2:
        L = rng.choice([0.55, 0.65, 0.70, 0.80])
        f1 = rng.choice([110, 147, 196, 220, 247, 330])
        vs = 2 * L * f1
        n = rng.choice([2, 3, 4])
        return num(f'A guitar string of vibrating length {sf(L, 2)} m has a fundamental frequency of {f1} Hz. Calculate the speed of waves on the string and the frequency of harmonic {n}.',
                   f'v = {q(vs, "m s⁻¹")}; f = {q(n * f1, "Hz")}', f'λ₁ = 2L = {sf(2 * L, 3)} m (M1); v = fλ = {q(vs, "m s⁻¹")} (A1); f_{n} = {n}f₁ = {q(n * f1, "Hz")} (A1).', 3)
    if frame == 3:
        f1 = rng.choice([180, 220, 260, 300])
        kind = rng.choice(['closed', 'open'])
        f2 = 3 * f1 if kind == 'closed' else 2 * f1
        L = v / (4 * f1) if kind == 'closed' else v / (2 * f1)
        return num(f'A pipe resonates at {f1} Hz and next at {f2} Hz, with no resonance in between. Deduce whether the pipe is open or closed at one end and calculate its length (speed of sound {v} m s⁻¹).',
                   f'{kind}{" at one end" if kind == "closed" else " at both ends"}; L = {q(L, "m")}',
                   f'ratio {f2}/{f1} = {f2 // f1} → {"odd harmonics only, closed pipe" if kind == "closed" else "consecutive harmonics, open pipe"} (R1); λ₁ = {4 if kind == "closed" else 2}L (M1); L = {q(L, "m")} (A1).', 3)
    L = rng.choice([0.60, 0.75, 0.90])
    fr = rng.choice([2, 3])
    f_open = v / (2 * L)
    f_cl = v / (4 * L)
    return num(f'A tube of length {sf(L, 2)} m is open at both ends. One end is then closed. Determine the change in its fundamental frequency (speed of sound {v} m s⁻¹).',
               f'{q(f_open, "Hz")} → {q(f_cl, "Hz")} (halved)', f'open f = v/2L = {q(f_open, "Hz")} (A1); closed f = v/4L = {q(f_cl, "Hz")} (A1); halves (R1).', 3)


@R.add('ch02-st2', 'C3', (1, 4), 'mcq')
def c3_pipe_mcq(rng, slot):
    L = rng.choice([0.25, 0.34, 0.50, 0.68, 0.85])
    v = 340
    f = v / (4 * L)
    return nmcq(rng, f'What is the fundamental frequency of a pipe of length {sf(L, 2)} m closed at one end? (speed of sound = 340 m s⁻¹)', f,
                [v / (2 * L), v / L, 3 * f], 'Hz', f'λ = 4L = {sf(4 * L)} m; f = v/λ = {q(f, "Hz")}.', extra=True)


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def c4_resonance_tube(rng, slot):
    v = rng.uniform(338, 348)
    f = rng.choice([384, 426.7, 480, 512])
    lam = v / f
    e = rng.uniform(0.008, 0.016)
    L1, L2 = lam / 4 - e, 3 * lam / 4 - e
    L1r, L2r = round(L1 * 100, 1), round(L2 * 100, 1)
    lam_c = 2 * (L2r - L1r) / 100
    v_c = f * lam_c
    e_c = lam_c / 4 - L1r / 100
    return num(f'In a resonance-tube experiment a tuning fork of frequency {f:g} Hz is held over a tube whose closed end is a water surface. Loud resonances are heard at air-column lengths of {L1r:.1f} cm and {L2r:.1f} cm. (a) Show that the wavelength is {sf(lam_c, 3)} m. (b) Calculate the speed of sound. (c) Determine the end correction and explain why using two resonance lengths removes it.',
               f'(a) λ = 2(L₂ − L₁) = {sf(lam_c, 3)} m; (b) v = {q(v_c, "m s⁻¹")}; (c) e = {q(e_c * 100, "cm", 2)}',
               f'(a) L₁ + e = λ/4 and L₂ + e = 3λ/4 (M1), subtract: L₂ − L₁ = λ/2 (A1). (b) v = fλ = {q(v_c, "m s⁻¹")} (A1). (c) e = λ/4 − L₁ = {q(e_c * 100, "cm", 2)} (A1); e cancels in the difference (R1).', 5, 'multi_step', 'G5')


R.mcqs('ch02-st2', 'C2', (1, 4), [
    ('The air temperature in a closed organ pipe increases. Which change occurs to the fundamental?', 'its frequency increases and its wavelength is unchanged', ['its frequency decreases', 'its wavelength increases and frequency is unchanged', 'both are unchanged'], 'λ is fixed by L; v increases so f increases.'),
    ('A string vibrates in its third harmonic. How many nodes are there, including the ends?', '4', ['3', '2', '6'], 'Three loops require four nodes.'),
    ('A pipe closed at one end resonates at 150 Hz, 450 Hz and 750 Hz. Its fundamental is', '150 Hz', ['300 Hz', '75 Hz', '50 Hz'], 'Odd multiples of 150 Hz.'),
    ('The open end of a pipe is a', 'displacement antinode and pressure node', ['displacement node and pressure antinode', 'displacement node and pressure node', 'displacement antinode and pressure antinode'], 'Air moves freely and pressure is atmospheric at an open end.'),
])

linearise('ch02-st2', [
    ('f = v/(2L) for the fundamental of a string of variable length L', 'f', '1/L', 'v/2 (half the wave speed)', 'A straight line through the origin confirms f ∝ 1/L.'),
    ('L + e = v/(4f) for the first resonance of a closed tube, where e is the end correction', 'L', '1/f', 'v/4', 'The y-intercept is −e, giving the end correction.'),
])


def _tube_spec(rng):
    v = rng.uniform(336, 348)
    e = rng.uniform(0.008, 0.015)
    fs = [256, 288, 320, 384, 426.7, 512]
    Ls = [round((v / (4 * f_) - e) * 100 + rng.uniform(-0.2, 0.2), 1) for f_ in fs]
    return dict(intro='The first resonance length L of a tube closed at one end is measured for tuning forks of different frequency f. Theory: L = v/(4f) − e, where e is the end correction.',
                xname='f', xunit='Hz', yname='L', yunit='cm', xs=fs, ys=Ls, xfmt=lambda a: f'{a:g}', yfmt=lambda b: f'{b:.1f}',
                plot_x=lambda a: 1 / a, plot_y=lambda b: b / 100, plot_label='L in m (y) against 1/f in s (x)', what='the speed of sound in air', what_short='the speed of sound',
                gunit='m s', deduce=lambda m_, b_: (4 * m_, 'm s⁻¹', 'v = 4 × gradient'))


gradient_fit('ch02-st2', _tube_spec)


R.facts('ch02-st3', F(
    terms=[('natural frequency', 'the frequency at which a system oscillates when displaced and released with no driving force'),
           ('forced oscillation', 'an oscillation of a system driven by a periodic external force at the driving frequency'),
           ('resonance', 'the large increase in amplitude that occurs when the driving frequency equals (or is close to) the natural frequency of the system'),
           ('driving frequency', 'the frequency of the periodic external force applied to an oscillating system')],
    facts=[('A system undergoing forced oscillations oscillates at', 'the driving frequency', ['its natural frequency', 'twice the driving frequency', 'a frequency that decreases with time'], 'In the steady state the system follows the driver.'),
           ('Resonance occurs when', 'the driving frequency equals the natural frequency', ['the amplitude of the driver is large', 'damping is removed completely', 'the driver is twice the natural frequency'], 'Maximum energy transfer from driver to oscillator.'),
           ('At resonance, the phase difference between the driver and a lightly damped oscillator is', 'π/2', ['0', 'π', '2π'], 'The displacement lags the driver by π/2 at resonance.'),
           ('Which is an example of useful resonance?', 'tuning a radio circuit to a station', ['vibration of a car mirror at certain engine speeds', 'collapse of a bridge in wind', 'rattling of windows near traffic'], 'Tuned circuits select one frequency by resonance.')],
    why=[('Explain why soldiers are ordered to break step when marching over a bridge.', 'Marching in step applies a periodic force at the step frequency; if it matches a natural frequency of the bridge, resonance builds up large, possibly damaging oscillations. Breaking step removes the regular driving force.'),
         ('Explain why the amplitude at resonance is limited in a real system.', 'At resonance energy is transferred from the driver every cycle, but damping forces remove energy at a rate that increases with amplitude; the amplitude grows until energy lost per cycle equals energy supplied.'),
         ('Explain how resonance is used in a microwave oven, and why the description "resonance of water molecules" is a simplification.', 'Microwaves (2.45 GHz) drive polar water molecules to rotate, transferring energy that becomes internal energy; however 2.45 GHz is not a sharp natural frequency of water – the heating is broad dielectric absorption, so "resonance" is a simplification.'),
         ('Explain why a washing machine shakes violently at one particular spin speed during spin-up.', 'As the drum speeds up the driving frequency passes through the natural frequency of the machine on its mounts; at that speed resonance gives large amplitude, which decreases again as the frequency increases further.')],
    contrast=[('free oscillation', 'forced oscillation', 'A free oscillation occurs at the natural frequency after an initial displacement with no further input; a forced oscillation is maintained by a periodic driver and takes place at the driving frequency.'),
              ('natural frequency', 'driving frequency', 'Natural frequency is a property of the system (set by its mass and stiffness); driving frequency is set by the external periodic force.')],
    misc=[('A forced oscillator always vibrates at its natural frequency.', 'In the steady state it vibrates at the driving frequency; it only vibrates at its natural frequency when this equals the driving frequency (resonance) or when free.'),
          ('The Tacoma Narrows Bridge collapsed simply because the wind blew at its natural frequency.', 'The wind was steady, not periodic; the collapse is better explained by aeroelastic flutter, a self-exciting oscillation – a case where the textbook "resonance" story is an oversimplification.'),
          ('Resonance means that the amplitude becomes infinite.', 'With any damping the amplitude is finite; energy lost per cycle balances energy supplied.')],
    cases=[('the London Millennium Bridge in 2000', 'the bridge swayed sideways when crowds crossed on opening day; pedestrians adjusted their step to the sway, synchronising their footfalls', 'resonance and positive feedback in forced oscillations', 'the lateral natural frequency (~1 Hz) matched half the walking frequency and people locked into it, so the driving force grew; dampers were fitted to fix it'),
           ('the quartz crystal in a watch', 'a quartz crystal is driven electrically and oscillates at its sharp natural frequency of 32 768 Hz', 'useful resonance', 'the crystal responds strongly only at its natural frequency, giving a very stable reference for timekeeping'),
           ('MRI scanners in hospitals', 'protons in a strong magnetic field absorb radio waves strongly only at the Larmor frequency', 'resonance as selective energy absorption', 'energy is absorbed only when the driving (radio) frequency equals the natural precession frequency')],
    evaluate=[('Engineers should design structures with as much damping as possible.', ['damping limits resonant amplitude and fatigue', 'tuned mass dampers protect tall buildings in earthquakes and wind'], ['damping adds cost, weight and maintenance', 'excessive damping can make structures stiff in other ways', 'shifting natural frequencies away from likely driving frequencies may be cheaper'], 'Damping is valuable but must be balanced against cost; good design combines appropriate damping with natural frequencies away from expected driving frequencies.')],
))


@R.add('ch02-st3', 'C3', (1, 5), 'numerical')
def c3_resonance_num(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        m_ = rng.choice([0.20, 0.35, 0.50, 0.80, 1.2])
        k = rng.choice([20, 40, 60, 80, 120])
        f0 = math.sqrt(k / m_) / (2 * math.pi)
        return num(f'A mass of {m_} kg hangs from a spring of spring constant {k} N m⁻¹. The top of the spring is driven up and down by a vibration generator. Calculate the driving frequency at which resonance occurs. (f = (1/2π)√(k/m))',
                   q(f0, 'Hz'), f'Resonance at the natural frequency (R1); f₀ = (1/2π)√({k}/{m_}) = {q(f0, "Hz")} (A1).', 2)
    if frame == 1:
        l = rng.choice([0.40, 0.60, 0.80, 1.00, 1.50])
        f0 = math.sqrt(g0 / l) / (2 * math.pi)
        return num(f'A simple pendulum of length {sf(l, 2)} m is pushed gently by a child once every cycle. Calculate the period of pushing that gives the largest amplitude (T = 2π√(l/g), g = 9.81 m s⁻²).',
                   q(1 / f0, 's'), f'Driving period = natural period (R1) = 2π√({sf(l, 2)}/9.81) = {q(1 / f0, "s")} (A1).', 2)
    if frame == 2:
        f0 = rng.choice([8, 12, 15, 18, 25])
        rpm = f0 * 60
        return num(f'A washing machine on its mounts has a natural frequency of {f0} Hz. At what drum speed, in revolutions per minute, will the machine shake most violently?',
                   f'{rpm} rpm', f'Resonance when rotation frequency = {f0} Hz (R1); {f0} × 60 = {rpm} rpm (A1).', 2)
    v = rng.choice([4, 6, 8, 10])
    s = rng.choice([1.6, 2.0, 2.5, 3.2])
    f0 = v / s
    return num(f'A car crosses speed bumps spaced {s} m apart. Its suspension has a natural frequency of {sf(f0, 2)} Hz. Calculate the speed at which the car bounces most.',
               q(v, 'm s⁻¹', 2), f'Driving frequency = v/s (M1); resonance when v/s = {sf(f0, 2)} Hz → v = {q(v, "m s⁻¹", 2)} (A1).', 2)


@R.add('ch02-st3', 'C3', (1, 4), 'mcq')
def c3_res_mcq(rng, slot):
    m_ = rng.choice([0.10, 0.25, 0.40, 0.50])
    k = rng.choice([10, 25, 40, 64, 100])
    f0 = math.sqrt(k / m_) / (2 * math.pi)
    return nmcq(rng, f'A {m_} kg mass on a spring of stiffness {k} N m⁻¹ is driven by a variable-frequency vibrator. At which frequency is the amplitude largest?', f0,
                [math.sqrt(k / m_), 2 * math.pi * math.sqrt(k / m_), math.sqrt(m_ / k) / (2 * math.pi)], 'Hz', f'f₀ = (1/2π)√(k/m) = {q(f0, "Hz")}; resonance occurs here.')


R.mcqs('ch02-st3', 'C2', (1, 4), [
    ('Two identical pendulums hang from a horizontal string; a third, much longer pendulum is set swinging. What happens?', 'the two identical pendulums oscillate with small amplitude at the frequency of the long pendulum', ['the identical pendulums swing with large amplitude at their natural frequency', 'nothing happens', 'the long pendulum stops at once'], 'Off-resonance forced oscillations are small and at the driving frequency (Barton’s pendulums).'),
    ('In Barton’s pendulums, the paper-cone pendulum with the largest amplitude is the one that', 'has the same length as the driver pendulum', ['is shortest', 'is longest', 'is heaviest'], 'Same length → same natural frequency → resonance.'),
    ('As the driving frequency is increased well above the natural frequency, the amplitude of a forced oscillator', 'decreases towards a small value', ['continues to increase', 'stays at the resonant value', 'becomes zero exactly'], 'Response falls off above resonance.'),
    ('A radio is tuned by changing the natural frequency of its circuit. This is an application of', 'resonance', ['damping', 'diffraction', 'refraction'], 'The circuit responds strongly only to the station at its natural frequency.'),
])

R.static('ch02-st3', 'C4', (3, 5), [
    ('A tall building in a windy city has a natural sway frequency of 0.18 Hz. Engineers install a tuned mass damper (a large mass on springs near the top). (a) Explain what is meant by resonance in this context. (b) Explain why the damper must be tuned to 0.18 Hz. (c) Discuss one limitation of relying on a tuned mass damper.',
     '(a) Gusts or vortex shedding at about 0.18 Hz would drive the building at its natural frequency, giving large sway amplitude; (b) the damper oscillates out of phase with the building at that frequency, absorbing energy and reducing the amplitude; (c) it is effective only near its tuned frequency, the building’s frequency can change with loading or ageing, and it is heavy and expensive.',
     'Driving frequency = natural frequency → large amplitude (R1); periodic forcing source identified (A1); damper resonates in antiphase, transfers energy away and dissipates it (R1 R1); limitation with justification (R1).'),
], type='multi_step', marks=5)


R.facts('ch02-st4', F(
    terms=[('damping', 'the reduction in amplitude of an oscillation as energy is transferred out of the system by resistive forces'),
           ('light damping (under-damping)', 'damping in which the system oscillates with gradually decreasing amplitude'),
           ('critical damping', 'damping that returns a displaced system to equilibrium in the shortest time without oscillating'),
           ('heavy damping (over-damping)', 'damping so large that the system returns slowly to equilibrium without oscillating')],
    facts=[('Car suspension systems are designed to be approximately', 'critically damped', ['undamped', 'lightly damped', 'very heavily damped'], 'Critical damping returns the car to equilibrium quickly without bouncing.'),
           ('Increasing the damping of a driven oscillator', 'reduces the resonant amplitude and broadens the resonance curve', ['increases the resonant amplitude', 'narrows the resonance peak', 'increases the natural frequency greatly'], 'More energy is lost per cycle.'),
           ('With light damping, the peak of the resonance curve occurs at a frequency', 'slightly below the natural frequency', ['well above the natural frequency', 'at twice the natural frequency', 'at zero frequency'], 'Damping shifts the peak slightly lower.')],
    why=[('Explain why increasing damping reduces the amplitude at resonance.', 'At resonance the amplitude grows until the energy lost per cycle to damping equals the energy supplied; with more damping this balance is reached at a smaller amplitude.'),
         ('Explain why critical damping is used in moving-coil meters and door closers.', 'The pointer or door reaches its final position as quickly as possible without overshooting or oscillating, so it can be read (or closes) quickly and safely.'),
         ('Explain why a lightly damped oscillation loses the same fraction of its amplitude every cycle.', 'The damping force is proportional to velocity, so the energy removed per cycle is a fixed fraction of the energy present; the amplitude therefore decays exponentially.')],
    contrast=[('light damping', 'heavy damping', 'With light damping the system oscillates with slowly decreasing amplitude; with heavy damping it does not oscillate and returns to equilibrium slowly.'),
              ('critical damping', 'heavy damping', 'Both give no oscillation, but critical damping returns to equilibrium in the shortest possible time, whereas heavy damping takes longer.')],
    misc=[('Damping changes the period of an oscillation dramatically.', 'Light damping hardly changes the period; it mainly reduces the amplitude over time.'),
          ('Critical damping means the system stops instantly.', 'It returns to equilibrium in the minimum time without oscillating, not instantly.')],
    evaluate=[('Critical damping is always the best choice for any oscillating system.', ['fastest return without overshoot for meters, suspensions and doors'], ['musical instruments and clocks need light damping to oscillate', 'earthquake isolation may need different behaviour', 'heavy damping may be safer where any overshoot is dangerous'], 'Critical damping suits systems that must settle quickly; others, such as instruments and resonators, need light damping.')],
))


@R.add('ch02-st4', 'C3', (1, 5), 'numerical')
def c3_damping(rng, slot):
    A0 = rng.choice([8.0, 10.0, 12.0, 15.0, 20.0])
    r = rng.choice([0.90, 0.92, 0.95, 0.80, 0.85])
    n = rng.choice([3, 5, 8, 10])
    An = A0 * r ** n
    frame = rng.randrange(3)
    if frame == 0:
        return num(f'A lightly damped pendulum starts with amplitude {sf(A0, 3)} cm. Each oscillation the amplitude falls to {int(r * 100)} % of its previous value. Calculate the amplitude after {n} oscillations.',
                   q(An, 'cm'), f'A = {sf(A0, 3)} × {r}^{n} (M1) = {q(An, "cm")} (A1).', 2)
    if frame == 1:
        Ef = r ** (2 * n)
        return num(f'The amplitude of a damped mass–spring system decreases by a factor of {r} every cycle. Determine the fraction of the original energy that remains after {n} cycles.',
                   f'{sf(Ef, 3)}', f'E ∝ A² (R1); fraction = ({r}^{n})² (M1) = {sf(Ef, 3)} (A1).', 3)
    N = math.ceil(math.log(0.5) / math.log(r))
    return num(f'A guitar string’s amplitude decreases by {round((1 - r) * 100)} % each cycle. Determine the number of complete cycles before its amplitude has fallen below half its starting value.',
               f'{N} cycles', f'{r}^N < 0.5 (M1); N > ln 0.5/ln {r} = {sf(math.log(0.5) / math.log(r))} (M1); N = {N} (A1).', 3)


@R.add('ch02-st4', 'C2', (1, 4), 'mcq')
def c2_damping_mcq(rng, slot):
    items = [
        ('A shock absorber is replaced by one with much thicker oil. After the car goes over a bump it will', 'return to equilibrium slowly without oscillating', ['bounce several times', 'oscillate with increasing amplitude', 'return faster than with critical damping'], 'Thicker oil → heavy damping.'),
        ('A displacement–time graph shows oscillations whose successive peaks decrease by the same ratio. The damping is', 'light, with exponential decay of amplitude', ['critical', 'heavy', 'zero'], 'Constant-ratio decay is characteristic of light damping.'),
        ('Two resonance curves are drawn for the same oscillator with different damping. The more heavily damped curve has', 'a lower, broader peak', ['a higher, sharper peak', 'a peak at a much higher frequency', 'the same height peak'], 'More damping → lower and broader.'),
        ('Energy lost from a damped oscillator is mainly transferred to', 'internal (thermal) energy of the system and surroundings', ['the driving frequency', 'potential energy of the spring', 'nuclear energy'], 'Resistive forces dissipate energy.'),
    ]
    q_, a, w, why = pick(rng, items)
    return mcq(rng, q_, a, w, why)


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3_damping_mcq(rng, slot):
    A0 = rng.choice([10, 12, 16, 20])
    r = rng.choice([0.8, 0.9, 0.75])
    n = rng.choice([2, 3, 4])
    An = A0 * r ** n
    return nmcq(rng, f'An oscillator of initial amplitude {A0} mm loses {round((1 - r) * 100)} % of its amplitude each cycle. What is the amplitude after {n} cycles?', An,
                [A0 * (1 - n * (1 - r)), A0 * r ** (n - 1), A0 * r ** (2 * n)], 'mm', f'A = {A0} × {r}^{n} = {q(An, "mm")}.')


R.static('ch02-st4', 'C4', (3, 5), [
    ('A student displaces a mass–spring system immersed in (i) air, (ii) water and (iii) thick syrup and records displacement against time. (a) Sketch and describe the three graphs. (b) Identify which might be close to critical damping and justify. (c) Explain, in terms of energy, why the amplitude in air decreases slowly.',
     '(a) Air: many oscillations, slowly decreasing amplitude (light damping); water: few oscillations quickly dying out; syrup: no oscillation, slow creep back to equilibrium (heavy damping). (b) Water could be near critical if it returns without overshoot in about a quarter-period; syrup is over-damped because it takes longer. (c) Air resistance removes only a small fraction of the energy each cycle, so the amplitude decays slowly and exponentially.',
     'Three correct descriptions (A1 A1); critical damping identified by fastest return without oscillation (R1); energy dissipated per cycle small in air (R1); link E ∝ A² (R1).'),
], type='multi_step', marks=5)

repeat_readings('ch02-st4', 'the time for the amplitude to halve', 's', 8.0, 20.0, 1,
                ['released a damped pendulum with a card sail and timed how long its amplitude took to fall to half its initial value.',
                 'filmed a mass–spring system oscillating in water and measured the halving time of the amplitude from the video.'])


# =============================================================================================
# ch03 C.5 Doppler effect
# =============================================================================================
def _dop_src(f, v, u, approach=True):
    return f * v / (v - u) if approach else f * v / (v + u)


def _dop_obs(f, v, u, approach=True):
    return f * (v + u) / v if approach else f * (v - u) / v


SOUND_SRC = ['an ambulance siren', 'a train horn', 'a police car siren', 'a racing car engine note', 'a drone’s buzzing motor', 'a motorbike horn', 'a fire engine siren']

R.facts('ch03-st1', F(
    terms=[('Doppler effect', 'the change in observed frequency (and wavelength) of a wave when the source and the observer move relative to each other'),
           ('observed frequency', 'the frequency of the waves received by an observer, which differs from the emitted frequency when there is relative motion along the line joining source and observer')],
    facts=[('A source of sound moves towards a stationary observer. Compared with the emitted sound, the observer hears', 'a higher frequency', ['a lower frequency', 'a higher speed of sound', 'the same frequency but louder'], 'Wavefronts are bunched up in front of the moving source.'),
           ('A source moves towards a stationary observer. Which quantity is unchanged for the observer?', 'the speed of the sound in the air', ['the wavelength', 'the frequency', 'the number of wavefronts received per second'], 'The speed of sound depends on the medium, not on the source motion.'),
           ('What happens to the wavelength in front of a moving sound source?', 'it decreases', ['it increases', 'it is unchanged', 'it becomes zero'], 'λ′ = (v − u_s)/f.'),
           ('An observer moves towards a stationary source. The observed frequency increases because', 'the observer meets wavefronts more often', ['the wavelength in the air decreases', 'the source frequency increases', 'the speed of sound in air increases'], 'The wavelength is unchanged; the relative speed of the waves past the observer increases.')],
    why=[('Explain, using wavefronts, why the pitch of a siren is higher as it approaches and lower as it moves away.', 'The source moves between emitting successive wavefronts, so in front they are closer together (shorter λ, higher f) and behind further apart (longer λ, lower f); the wave speed in air is unchanged, so the observed frequency changes.'),
         ('Explain why a moving observer and a moving source do not have exactly symmetrical Doppler formulae for sound.', 'For sound there is a medium: a moving source changes the wavelength in the air, whereas a moving observer changes the speed of the waves relative to themselves with the wavelength unchanged; the two effects give different formulae.'),
         ('Explain why there is no Doppler shift when a source moves perpendicular to the line joining it to the observer.', 'At that instant the source has no velocity component along the line of sight, so the distance to the observer is not changing and successive wavefronts take the same time to arrive (for sound, at non-relativistic speeds).')],
    contrast=[('a moving source', 'a moving observer', 'A moving source changes the wavelength of the waves in the medium (λ′ = (v ∓ u_s)/f); a moving observer leaves the wavelength unchanged but meets wavefronts at a different rate (relative speed v ± u_o).')],
    misc=[('The siren gets louder as it approaches, and that is what the Doppler effect means.', 'Loudness change is due to distance; the Doppler effect is the change in frequency (pitch), which stays higher throughout the approach.'),
          ('The pitch of an approaching siren rises steadily as it gets closer.', 'For a source approaching at constant speed along the line of sight, the observed frequency is constant (and higher); it drops suddenly as it passes.'),
          ('The speed of sound increases in front of a moving source.', 'The speed of sound depends only on the medium; it is the wavelength that decreases in front of the source.')],
    evaluate=[('The Doppler formula for sound applies equally to light.', ['both are wave phenomena showing frequency shifts with relative motion', 'for low speeds both give Δf/f ≈ v/c'], ['light needs no medium, so only relative velocity matters', 'at high speeds relativistic effects apply', 'the sound formulae distinguish source and observer motion'], 'Only at speeds much less than c does the simple light formula resemble the sound case; the underlying physics differs because light needs no medium.')],
))


@R.add('ch03-st1', 'C3', (1, 5), 'numerical')
def c3_doppler_sound(rng, slot):
    src = pick(rng, SOUND_SRC)
    f = rng.choice([400, 480, 520, 600, 700, 750, 850, 960, 1200])
    v = rng.choice([330, 340, 343])
    u = rng.choice([12, 15, 18, 20, 25, 30, 35, 40])
    frame = rng.randrange(5)
    if frame == 0:
        fo = _dop_src(f, v, u, True)
        return num(f'{src[0].upper() + src[1:]} emits sound of frequency {f} Hz while approaching a stationary observer at {u} m s⁻¹. The speed of sound is {v} m s⁻¹. Calculate the frequency heard.',
                   q(fo, 'Hz'), f'f′ = f v/(v − u_s) (M1) = {f} × {v}/({v} − {u}) = {q(fo, "Hz")} (A1).', 2)
    if frame == 1:
        fo = _dop_src(f, v, u, False)
        return num(f'{src[0].upper() + src[1:]} of frequency {f} Hz moves away from a listener at {u} m s⁻¹ (speed of sound {v} m s⁻¹). Calculate the frequency the listener hears.',
                   q(fo, 'Hz'), f'f′ = f v/(v + u_s) (M1) = {q(fo, "Hz")} (A1).', 2)
    if frame == 2:
        fo = _dop_obs(f, v, u, True)
        who = name(rng)
        return num(f'{who} cycles at {u} m s⁻¹ directly towards a stationary loudspeaker emitting {f} Hz (speed of sound {v} m s⁻¹). Calculate the frequency {who} hears.',
                   q(fo, 'Hz'), f'f′ = f (v + u_o)/v (M1) = {q(fo, "Hz")} (A1).', 2)
    if frame == 3:
        lam = (v - u) / f
        return num(f'{src[0].upper() + src[1:]} emits {f} Hz while moving at {u} m s⁻¹ (speed of sound {v} m s⁻¹). Calculate the wavelength of the sound in front of the source and behind it.',
                   f'{q(lam, "m")} in front; {q((v + u) / f, "m")} behind', f'λ_front = (v − u)/f = {q(lam, "m")} (A1); λ_behind = (v + u)/f = {q((v + u) / f, "m")} (A1); M1 for the idea that the source moves u/f between wavefronts.', 3)
    f1 = _dop_src(f, v, u, True)
    f2 = _dop_src(f, v, u, False)
    us = v * (f1 - f2) / (f1 + f2)
    return num(f'As {src} passes a stationary observer, the frequency heard falls from {sf(f1, 4)} Hz to {sf(f2, 4)} Hz. The speed of sound is {v} m s⁻¹. Determine the speed of the source and the emitted frequency.',
               f'u = {q(us, "m s⁻¹")}; f = {q(f, "Hz")}', f'f₁ = fv/(v − u), f₂ = fv/(v + u) (M1); f₁/f₂ = (v + u)/(v − u) (M1); u = v(f₁ − f₂)/(f₁ + f₂) = {q(us, "m s⁻¹")} (A1); f = f₁(v − u)/v = {q(f, "Hz")} (A1).', 4, 'multi_step')


@R.add('ch03-st1', 'C3', (1, 4), 'mcq')
def c3_doppler_mcq(rng, slot):
    f = rng.choice([500, 600, 800, 900, 1000])
    v = 340
    u = rng.choice([17, 20, 34, 40])
    fo = _dop_src(f, v, u, True)
    return nmcq(rng, f'A source of frequency {f} Hz moves towards a stationary observer at {u} m s⁻¹. The speed of sound is {v} m s⁻¹. What frequency is observed?', fo,
                [_dop_src(f, v, u, False), _dop_obs(f, v, u, True), f * (v - u) / v], 'Hz', f'f′ = fv/(v − u) = {q(fo, "Hz")}. Using the observer formula or the wrong sign gives the distractors.', n=3, extra=False)


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def c2_doppler_predict(rng, slot):
    sits = [('the source speed is doubled while it still approaches', 'the observed frequency increases further (f′ = fv/(v − u) with a larger u)'),
            ('the observer moves towards the source instead of the source moving towards the observer at the same speed', 'the observed frequency is still higher, but slightly less than when the source moves (the formulae differ for sound)'),
            ('a strong wind blows from the source towards a stationary observer, with neither moving', 'there is no Doppler shift: the wavelength and frequency are unchanged because source and observer are at rest relative to each other'),
            ('the source moves in a circle around the observer at constant speed', 'there is no change in frequency because the source has no velocity component along the line of sight'),
            ('the source moves away at the same speed instead of approaching', 'the observed frequency is lower than the emitted frequency (f′ = fv/(v + u))')]
    s, a = pick(rng, sits)
    return dict(stem=f'A loudspeaker emits a steady note while moving relative to an observer. Predict and explain the effect on the observed frequency if {s}.', answer=a, type='explain', marks=2,
                markingKey=f'{a} (A1 for the prediction, R1 for the reasoning in terms of wavefronts or relative motion).')


R.mcqs('ch03-st1', 'C2', (1, 4), [
    ('A whistle is whirled in a horizontal circle. A distant observer in the plane of the circle hears a note whose frequency', 'rises and falls periodically', ['is constant and higher', 'is constant and lower', 'rises steadily'], 'The line-of-sight velocity alternates between towards and away.'),
    ('Source and observer move in the same direction at the same speed through still air. The observed frequency is', 'equal to the emitted frequency', ['higher', 'lower', 'zero'], 'No relative motion: the effects of source and observer motion cancel.'),
    ('A train sounds its horn while approaching a station at constant speed. A passenger on the platform hears a frequency that', 'is constant and higher, then drops as the train passes', ['rises steadily as the train approaches', 'is constant and equal to the emitted frequency', 'falls steadily as the train approaches'], 'Constant velocity gives a constant shift.'),
])

R.static('ch03-st1', 'C4', (3, 5), [
    ('A bat flying at 6.0 m s⁻¹ towards a wall emits ultrasound at 40.0 kHz (speed of sound 340 m s⁻¹). (a) Calculate the frequency received by the wall. (b) The wall reflects this as a stationary source; calculate the frequency the bat hears. (c) Explain how the bat could use the difference to judge its speed relative to the wall.',
     '(a) 40.0 × 340/334 = 40.7 kHz; (b) 40.72 × 346/340 = 41.4 kHz; (c) the frequency shift (≈ 1.4 kHz) depends on the speed of approach: Δf ≈ 2fu/v, so a larger shift means faster closing speed.',
     'Moving source formula (M1) 40.7 kHz (A1); moving-observer formula for the reflection (M1) 41.4 kHz (A1); interpretation of Δf ∝ u (R1).'),
], type='multi_step', marks=5)


def _dop_data_spec(rng):
    v = 340
    us = [5, 10, 15, 20, 25, 30]
    f = rng.choice([500, 600, 800])
    fo = [round(_dop_src(f, v, u, True) + rng.uniform(-1, 1)) for u in us]
    return dict(intro=f'A loudspeaker emitting a fixed frequency is carried on a track towards a microphone at different speeds u. The observed frequency f′ is recorded. Theory: 1/f′ = 1/f − u/(fv), speed of sound v = 340 m s⁻¹.',
                xname='u', xunit='m s⁻¹', yname='f′', yunit='Hz', xs=us, ys=fo, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b}',
                plot_x=lambda a: a, plot_y=lambda b: 1 / b, plot_label='1/f′ (y) against u (x)', what='the emitted frequency f (from the y-intercept, using v from the gradient as a check)', what_short='the emitted frequency',
                gunit='s² m⁻¹', deduce=lambda m_, b_: (1 / b_, 'Hz', 'f = 1/(y-intercept)'))


gradient_fit('ch03-st1', _dop_data_spec)

LINES = [('hydrogen-alpha', 656.3), ('hydrogen-beta', 486.1), ('calcium K', 393.4), ('sodium D', 589.0), ('magnesium b', 517.3), ('calcium H', 396.8)]

R.facts('ch03-st2', F(
    terms=[('redshift', 'the increase in observed wavelength (decrease in frequency) of light from a source moving away from the observer'),
           ('blueshift', 'the decrease in observed wavelength of light from a source moving towards the observer'),
           ('redshift z', 'the fractional change in wavelength, z = Δλ/λ₀, which for v ≪ c is approximately v/c')],
    facts=[('For a galaxy receding at speed v ≪ c, the fractional change in wavelength of its spectral lines is approximately', 'v/c', ['c/v', 'v²/c²', '2v/c'], 'Δλ/λ ≈ v/c.'),
           ('The light from a star moving towards Earth shows absorption lines that are', 'shifted to shorter wavelengths', ['shifted to longer wavelengths', 'unchanged', 'broadened only'], 'Approach → blueshift.'),
           ('The Doppler formula Δf/f ≈ v/c for light is valid only when', 'the relative speed is much less than c', ['the source is a star', 'the light is visible', 'the source is stationary'], 'At high speeds relativistic formulae are needed.'),
           ('Light from opposite edges of the rotating Sun shows', 'a blueshift on one edge and a redshift on the other', ['redshift on both edges', 'blueshift on both edges', 'no shift'], 'One limb approaches, the other recedes.')],
    why=[('Explain how spectral lines allow astronomers to measure the speed of a distant galaxy along the line of sight.', 'Elements in the galaxy produce absorption lines at known laboratory wavelengths; comparing observed and laboratory wavelengths gives Δλ/λ ≈ v/c, so v is found from the shift; redshift means recession.'),
         ('Explain why the Doppler shift of light depends only on relative velocity, unlike sound.', 'Light needs no medium and its speed is the same for all observers, so there is no distinction between source and observer motion; only their relative velocity matters.'),
         ('Explain why the redshift of distant galaxies supports the idea that the universe is expanding.', 'Almost all distant galaxies show redshifts, and the redshift increases with distance (Hubble’s law); this is consistent with space itself expanding, so every galaxy moves away from every other.')],
    contrast=[('redshift', 'blueshift', 'Redshift is an increase in wavelength from a receding source; blueshift is a decrease in wavelength from an approaching source.')],
    misc=[('Redshift means the galaxy looks red.', 'Redshift means that all spectral lines are shifted towards longer wavelengths; the galaxy need not appear red.'),
          ('A blueshift shows that the source is getting hotter.', 'Blueshift indicates motion towards the observer; temperature is found from the spectrum’s peak (Wien’s law), not from line shifts.')],
    evaluate=[('Measured redshifts prove that the universe began in a Big Bang.', ['systematic redshift with distance indicates expansion', 'combined with the CMB and abundances of light elements it strongly supports the Big Bang model'], ['redshift alone shows expansion, not a beginning', 'other evidence is needed; models can be revised (NOS)', 'local galaxies (e.g. Andromeda) show blueshift'], 'Redshifts are strong evidence for expansion and, with other evidence, support the Big Bang, but science provides support rather than proof.')],
))


@R.add('ch03-st2', 'C3', (1, 5), 'numerical')
def c3_redshift(rng, slot):
    ln, l0 = pick(rng, LINES)
    v = rng.choice([1.2e5, 3.6e5, 8.0e5, 1.5e6, 2.4e6, 4.5e6, 9.0e6, 1.2e7])
    sign = rng.choice([1, 1, -1])
    dl = sign * l0 * v / C
    lo = l0 + dl
    obj = pick(rng, ['a distant galaxy', 'a quasar host galaxy', 'a star in a nearby galaxy', 'a galaxy in the Virgo cluster', 'a radio galaxy'])
    frame = rng.randrange(3)
    if frame == 0:
        return num(f'The {ln} line has a laboratory wavelength of {l0} nm. In the spectrum of {obj} it is observed at {sf(lo, 5)} nm. Determine the speed of {obj} along the line of sight and state whether it is approaching or receding.',
                   f'{q(abs(dl) / l0 * C, "m s⁻¹")}, {"receding" if sign > 0 else "approaching"}', f'Δλ = {sf(dl, 3)} nm (A1); v = cΔλ/λ₀ (M1) = {q(abs(dl) / l0 * C, "m s⁻¹")} (A1); {"redshift → receding" if sign > 0 else "blueshift → approaching"} (R1).', 4)
    if frame == 1:
        return num(f'{obj[0].upper() + obj[1:]} recedes from Earth at {q(v, "m s⁻¹")}. Calculate the observed wavelength of its {ln} line (laboratory wavelength {l0} nm).',
                   q(l0 * (1 + v / C), 'nm', 5), f'Δλ = λ₀ v/c = {sf(l0 * v / C, 3)} nm (M1); λ = {q(l0 * (1 + v / C), "nm", 5)} (A1).', 2)
    f0 = C / (l0 * 1e-9)
    return num(f'Calculate the change in frequency of the {ln} line ({l0} nm) in light from {obj} moving away at {q(v, "m s⁻¹")}.',
               f'decrease of {q(f0 * v / C, "Hz")}', f'f = c/λ = {q(f0, "Hz")} (A1); Δf = f v/c = {q(f0 * v / C, "Hz")} (A1), a decrease (A1).', 3)


@R.add('ch03-st2', 'C3', (1, 4), 'mcq')
def c3_redshift_mcq(rng, slot):
    ln, l0 = pick(rng, LINES)
    z = rng.choice([0.002, 0.004, 0.005, 0.01, 0.015, 0.02])
    v = z * C
    return nmcq(rng, f'The {ln} line ({l0} nm) in a galaxy’s spectrum is observed at {sf(l0 * (1 + z), 5)} nm. What is the recession speed of the galaxy?', v,
                [C / z / 1e6 if C / z / 1e6 < 1e9 else v * 3, v * 2, v / 2], 'm s⁻¹', f'v = cΔλ/λ = 3.00 × 10⁸ × {z} = {q(v, "m s⁻¹")}.', extra=False)


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step')
def c4_rotation(rng, slot):
    ln, l0 = pick(rng, LINES[:2])
    vrot = rng.choice([1.5e5, 2.0e5, 2.2e5, 2.5e5])
    vsys = rng.choice([1.0e6, 2.0e6, 3.0e6])
    l1 = l0 * (1 + (vsys + vrot) / C)
    l2 = l0 * (1 + (vsys - vrot) / C)
    return num(f'A spiral galaxy is viewed edge-on. The {ln} line ({l0} nm) is observed at {sf(l1, 6)} nm from one edge and {sf(l2, 6)} nm from the opposite edge. (a) Determine the speed of the galaxy as a whole. (b) Determine the rotation speed of the outer edge. (c) Outline how such measurements provide evidence for dark matter.',
               f'(a) {q(vsys, "m s⁻¹")} receding; (b) {q(vrot, "m s⁻¹")}; (c) rotation speeds stay high at large radii, implying more mass than the visible matter',
               f'Mean wavelength gives the systemic shift: v = c(λ̄ − λ₀)/λ₀ = {q(vsys, "m s⁻¹")} (M1 A1); half the difference gives rotation: v = cΔλ/(2λ₀) = {q(vrot, "m s⁻¹")} (M1 A1); flat rotation curves → unseen mass (R1).', 5, 'multi_step', 'G5')


R.mcqs('ch03-st2', 'C2', (1, 4), [
    ('A spectral line from a binary star periodically splits into two lines and recombines. This is because', 'the two stars alternately approach and recede along the line of sight', ['the stars change temperature', 'the light is diffracted by dust', 'the stars change chemical composition'], 'Orbital motion gives opposite Doppler shifts.'),
    ('The light from a galaxy shows a redshift z = 0.010. If a second galaxy has z = 0.030, it is', 'receding three times as fast', ['approaching three times as fast', 'three times closer', 'receding at the same speed'], 'v ≈ zc.'),
    ('Which statement about the Doppler effect for light is correct?', 'It depends on the relative velocity of source and observer along the line of sight', ['It requires a medium', 'It only occurs for visible light', 'It changes the speed of light'], 'No medium; c is invariant.'),
])


R.facts('ch03-st3', F(
    terms=[('radar speed gun', 'a device that emits microwaves at a moving vehicle and finds its speed from the Doppler shift of the reflected waves'),
           ('beat frequency', 'the frequency of the periodic variation in intensity when two waves of slightly different frequency superpose; equal to their frequency difference'),
           ('Doppler ultrasound', 'a medical technique that measures the speed of blood flow from the frequency shift of ultrasound reflected by moving blood cells')],
    facts=[('A radar wave reflects off a car approaching at speed v ≪ c. The frequency shift of the reflected wave is approximately', '2fv/c', ['fv/c', 'fv/2c', '4fv/c'], 'The car first receives a shifted frequency and then re-emits it as a moving source: a double shift.'),
           ('Which astronomical observation uses the Doppler effect to detect exoplanets?', 'periodic shifts in the star’s spectral lines as it wobbles', ['the planet’s brightness', 'the star’s parallax', 'the planet’s colour'], 'Radial-velocity method.'),
           ('In Doppler ultrasound, why is the shift of the reflected wave doubled?', 'the blood cells act first as a moving observer, then as a moving source', ['the ultrasound travels twice as fast', 'two transducers are used', 'ultrasound has two frequencies'], 'Reception and re-emission both introduce a shift.')],
    why=[('Explain why a radar speed gun measures the beat frequency rather than the reflected frequency directly.', 'The shift (hundreds or thousands of hertz) is tiny compared with the emitted frequency (~10¹⁰ Hz); mixing reflected and emitted waves produces beats at the difference frequency, which can be measured precisely.'),
         ('Explain why a speed gun reads low if it is aimed at an angle to the road.', 'Only the component of the car’s velocity along the line of the beam (v cos θ) produces a Doppler shift, so the measured speed is smaller than the true speed.'),
         ('Explain how the Doppler effect is used to detect exoplanets by the radial-velocity method.', 'A planet and its star orbit their common centre of mass; the star’s velocity along our line of sight oscillates, so its spectral lines shift periodically to red and blue; the period gives the orbital period and the amplitude gives the planet’s minimum mass.')],
    misc=[('A radar gun measures speed using the time for the echo to return.', 'The speed gun uses the frequency (Doppler) shift of the reflected wave; timing gives distance, not speed directly.'),
          ('Doppler ultrasound measures blood flow speed from how loud the echo is.', 'It uses the frequency shift of the echo, proportional to the speed of the blood cells along the beam.')],
    evaluate=[('The Doppler effect is the most important tool in modern astronomy.', ['measures radial velocities, rotation, binary orbits, exoplanets and cosmic expansion'], ['parallax, photometry and spectroscopy of composition and temperature are equally essential', 'only gives line-of-sight velocity'], 'It is one of the most powerful tools, but astronomy relies on several complementary methods.')],
))


@R.add('ch03-st3', 'C3', (1, 5), 'numerical')
def c3_radar(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        f = rng.choice([10.5e9, 24.15e9, 34.7e9])
        v = rng.choice([22.0, 25.0, 27.8, 31.0, 33.3, 36.1])
        df = 2 * f * v / C
        return num(f'A police radar gun emits microwaves of frequency {sf(f / 1e9, 4)} GHz towards a car approaching at {sf(v, 3)} m s⁻¹. Calculate the frequency difference between the emitted and reflected waves.',
                   q(df, 'Hz'), f'Δf = 2fv/c (M1) = 2 × {sf(f)} × {sf(v, 3)}/3.00 × 10⁸ = {q(df, "Hz")} (A1).', 2)
    if frame == 1:
        f = rng.choice([10.5e9, 24.15e9])
        df = rng.choice([1500, 1800, 2100, 2600, 4200, 5500])
        v = df * C / (2 * f)
        lim = rng.choice([20, 25, 30])
        return num(f'A speed camera emits {sf(f / 1e9, 4)} GHz microwaves. The beat frequency between the emitted and reflected waves from an approaching car is {df} Hz. The speed limit is {lim} m s⁻¹. Determine whether the car is speeding.',
                   f'v = {q(v, "m s⁻¹")}; {"speeding" if v > lim else "not speeding"}', f'v = cΔf/(2f) (M1) = {q(v, "m s⁻¹")} (A1); compare with {lim} m s⁻¹ (R1).', 3)
    if frame == 2:
        f = rng.choice([2.0e6, 4.0e6, 5.0e6, 8.0e6])
        vs = 1540
        vb = rng.choice([0.15, 0.25, 0.30, 0.45, 0.60])
        th = rng.choice([0, 30, 45, 60])
        df = 2 * f * vb * cosd(th) / vs
        return num(f'Ultrasound of frequency {sf(f / 1e6, 2)} MHz is directed at blood flowing at {sf(vb, 2)} m s⁻¹, at {th}° to the flow. The speed of sound in tissue is 1540 m s⁻¹. Calculate the frequency shift of the echo (Δf = 2fv cos θ/c_s).',
                   q(df, 'Hz'), f'Δf = 2 × {sf(f)} × {sf(vb, 2)} × cos {th}°/1540 (M1) = {q(df, "Hz")} (A1).', 2)
    P = rng.choice([3.5, 4.2, 10.0, 50.0, 365.0])
    K_ = rng.choice([12, 30, 55, 120, 200])
    ln, l0 = LINES[0]
    dl = l0 * K_ / C
    return num(f'A star’s {ln} line ({l0} nm) shifts back and forth with a period of {P} days and a maximum shift of ±{q(dl * 1e6, "fm", 3)} (1 fm = 10⁻⁶ nm). Calculate the maximum line-of-sight speed of the star and state what the period tells astronomers.',
               f'{q(K_, "m s⁻¹")}; the period is the orbital period of the planet', f'v = cΔλ/λ (M1) = {q(K_, "m s⁻¹")} (A1); periodic shift → orbital period of the companion planet (R1).', 3)


@R.add('ch03-st3', 'C3', (1, 4), 'mcq')
def c3_radar_mcq(rng, slot):
    f = rng.choice([10e9, 20e9, 24e9, 30e9])
    v = rng.choice([15, 20, 25, 30, 40])
    df = 2 * f * v / C
    return nmcq(rng, f'A radar emits {sf(f / 1e9, 2)} GHz microwaves towards a vehicle approaching at {v} m s⁻¹. What is the frequency shift of the reflected wave?', df,
                [df / 2, df * 2, f * v / 340 if f * v / 340 != df else df * 3], 'Hz', f'Δf = 2fv/c = {q(df, "Hz")}; forgetting the factor 2 gives half this value.', extra=False)


R.mcqs('ch03-st3', 'C2', (1, 4), [
    ('Why do radar speed guns use microwaves rather than visible light?', 'microwaves pass through rain and fog and are easily generated and detected electronically', ['microwaves travel faster than light', 'light has no Doppler effect', 'microwaves do not reflect from cars'], 'Practical generation, detection and weather penetration.'),
    ('A star shows a periodic radial-velocity variation of 50 m s⁻¹. Doubling the planet’s mass (same orbit) would make the variation approximately', '100 m s⁻¹', ['25 m s⁻¹', '50 m s⁻¹', '200 m s⁻¹'], 'The star’s wobble is proportional to planet mass for small planets.'),
    ('A speed gun aimed along the road reads 30 m s⁻¹. An officer then measures the same car at 60° to its path. The reading is', '15 m s⁻¹', ['30 m s⁻¹', '26 m s⁻¹', '60 m s⁻¹'], 'Component v cos 60° = 15 m s⁻¹.'),
])

R.static('ch03-st3', 'C4', (3, 5), [
    ('Evaluate the use of the Doppler radial-velocity method for discovering Earth-like planets around Sun-like stars.',
     'Strengths: it measures the star’s line-of-sight wobble and gives the orbital period and minimum planet mass; it has found hundreds of planets. Limitations: an Earth-mass planet at 1 AU makes the Sun wobble by only ~0.1 m s⁻¹, requiring extreme spectrometer stability; stellar activity (spots, granulation) mimics signals; it gives only m sin i unless the inclination is known; long periods need years of data. Judgement: excellent for giant and close-in planets; for Earth analogues it needs combination with transit observations.',
     'States the principle (A1); strength with physics (R1); size of the effect quantified or explained (R1); two limitations (R1 R1); supported judgement (A1).', 6),
], type='multi_step', marks=6)

repeat_readings('ch03-st3', 'the measured speed', 'm s⁻¹', 12.0, 30.0, 1,
                ['tested a radar speed gun by measuring the speed of a car driven past at a nominally constant speed several times.',
                 'checked the precision of a hand-held Doppler radar by repeating measurements on a cyclist on a velodrome.'])


# =============================================================================================
# ch04 D.1 Gravitational fields
# =============================================================================================
BODIES = [('Earth', 5.97e24, 6.37e6), ('Mars', 6.42e23, 3.39e6), ('the Moon', 7.35e22, 1.74e6), ('Jupiter', 1.90e27, 6.99e7),
          ('Venus', 4.87e24, 6.05e6), ('Mercury', 3.30e23, 2.44e6), ('Saturn', 5.68e26, 5.82e7)]
MOONS = [('Io', 'Jupiter', 4.22e8, 1.77), ('Europa', 'Jupiter', 6.71e8, 3.55), ('Titan', 'Saturn', 1.22e9, 15.9),
         ('Phobos', 'Mars', 9.38e6, 0.319), ('the Moon', 'Earth', 3.84e8, 27.3), ('Ganymede', 'Jupiter', 1.07e9, 7.15)]

R.facts('ch04-st1', F(
    terms=[("Newton's law of gravitation", 'every pair of point masses attracts with a force proportional to the product of their masses and inversely proportional to the square of their separation, F = GMm/r²'),
           ("Kepler's first law", 'planets move in elliptical orbits with the Sun at one focus'),
           ("Kepler's second law", 'the line joining a planet to the Sun sweeps out equal areas in equal times'),
           ("Kepler's third law", 'the square of the orbital period is proportional to the cube of the mean orbital radius, T² ∝ r³')],
    facts=[('The distance between two masses is tripled. The gravitational force between them becomes', 'one-ninth as large', ['one-third as large', 'three times as large', 'nine times as large'], 'F ∝ 1/r².'),
           ('According to Kepler’s second law, a planet in an elliptical orbit moves', 'fastest when closest to the Sun', ['fastest when furthest from the Sun', 'at constant speed', 'fastest at the ends of the minor axis'], 'Equal areas in equal times → faster near perihelion.'),
           ('What are the units of the gravitational constant G?', 'N m² kg⁻²', ['N kg⁻¹', 'N m kg⁻¹', 'kg m s⁻²'], 'G = Fr²/(Mm).'),
           ('Newton’s law of gravitation applies directly to spherical bodies such as planets because', 'a uniform sphere acts as if all its mass were at its centre', ['planets are point masses', 'G is very small', 'planets are hollow'], 'Shell theorem.')],
    why=[('Explain how Newton’s law of gravitation together with circular motion leads to Kepler’s third law.', 'Gravity provides the centripetal force: GMm/r² = m(4π²r/T²); rearranging gives T² = (4π²/GM)r³, so T² ∝ r³ with the same constant for all bodies orbiting the same central mass.'),
         ('Explain why Kepler’s laws are described as empirical whereas Newton’s law of gravitation is explanatory.', 'Kepler found his laws by fitting Tycho Brahe’s observations without a cause; Newton’s law explains them as consequences of an inverse-square force and also predicts tides, comet orbits and satellite motion (NOS: theories explain laws).'),
         ('Explain why the gravitational force between two students is not noticeable.', 'G is very small (6.67 × 10⁻¹¹ N m² kg⁻²); for masses of ~60 kg a metre apart the force is ~10⁻⁷ N, far smaller than friction and other forces.')],
    contrast=[("Kepler's laws", "Newton's law of gravitation", 'Kepler’s laws describe how planets move (ellipses, equal areas, T² ∝ r³) from observation; Newton’s law gives the force that causes this motion and applies to all masses.')],
    misc=[('The Moon is not falling towards Earth because gravity is balanced by a centrifugal force.', 'In the inertial frame there is only one force, gravity, which provides the centripetal force; the Moon is continuously falling towards Earth while moving sideways.'),
          ('Doubling both masses doubles the gravitational force.', 'F ∝ Mm, so doubling both masses quadruples the force.'),
          ('Astronauts on the ISS are weightless because there is no gravity in orbit.', 'At ISS altitude g is about 8.7 N kg⁻¹; they are in free fall with the station, so they feel weightless.')],
    evaluate=[("Newton's law of universal gravitation has been replaced by general relativity, so it is no longer useful.", ['general relativity explains the precession of Mercury and gravitational lensing', 'GPS needs relativistic corrections'], ['Newton’s law is extremely accurate for most engineering and spaceflight', 'it is far simpler to use', 'theories are used within their domains of validity (NOS)'], 'Newton’s law remains an excellent approximation in weak fields and low speeds; general relativity is needed only for precise or strong-field situations.')],
))


@R.add('ch04-st1', 'C3', (1, 5), 'numerical')
def c3_newton_grav(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        b, M, Rb = pick(rng, BODIES)
        m_ = rng.choice([500, 850, 1200, 2500, 4200])
        h = rng.choice([200, 400, 800, 2000, 20000]) * 1e3
        F_ = G * M * m_ / (Rb + h) ** 2
        return num(f'A satellite of mass {m_} kg orbits {b} (mass {q(M, "kg")}, radius {q(Rb, "m")}) at a height of {sf(h / 1e3, 3)} km above the surface. Calculate the gravitational force on the satellite.',
                   q(F_, 'N'), f'r = R + h = {q(Rb + h, "m")} (M1); F = GMm/r² (M1) = {q(F_, "N")} (A1).', 3)
    if frame == 1:
        m1, m2 = rng.choice([50, 60, 75]), rng.choice([55, 65, 80])
        r = rng.choice([0.5, 1.0, 1.5, 2.0])
        F_ = G * m1 * m2 / r ** 2
        n1, n2 = two_names(rng)
        return num(f'{n1} ({m1} kg) and {n2} ({m2} kg) sit {r} m apart. Estimate the gravitational force between them, treating them as point masses.',
                   q(F_, 'N'), f'F = Gm₁m₂/r² = 6.67 × 10⁻¹¹ × {m1} × {m2}/{r}² (M1) = {q(F_, "N")} (A1).', 2)
    if frame == 2:
        moon, planet, r, Td = pick(rng, MOONS)
        T_ = Td * 86400
        M = 4 * math.pi ** 2 * r ** 3 / (G * T_ ** 2)
        return num(f'{moon} orbits {planet} with a mean orbital radius of {q(r, "m")} and a period of {Td} days. Determine the mass of {planet}.',
                   q(M, 'kg'), f'GM = 4π²r³/T² (M1); T = {q(T_, "s")} (A1); M = {q(M, "kg")} (A1).', 3)
    moon, planet, r, Td = pick(rng, [m for m in MOONS if m[1] == 'Jupiter'])
    other = pick(rng, [m for m in MOONS if m[1] == 'Jupiter' and m[0] != moon])
    T2 = Td * (other[2] / r) ** 1.5
    return num(f'{moon} orbits Jupiter at {q(r, "m")} with period {Td} days. {other[0]} orbits at {q(other[2], "m")}. Use Kepler’s third law to predict the orbital period of {other[0]}.',
               q(T2, 'days'), f'T₂ = T₁ (r₂/r₁)^(3/2) (M1) = {Td} × ({sf(other[2] / r)})^1.5 (M1) = {q(T2, "days")} (A1).', 3)


@R.add('ch04-st1', 'C3', (1, 4), 'mcq')
def c3_grav_mcq(rng, slot):
    F0 = rng.choice([12, 36, 48, 72, 90])
    k = rng.choice([2, 3, 4])
    mm = rng.choice([1, 2, 3])
    F1 = F0 * mm / k ** 2
    return nmcq(rng, f'The gravitational force between two spheres is {F0} N. One mass is multiplied by {mm} and the separation is multiplied by {k}. What is the new force?', F1,
                [F0 * mm / k, F0 * mm * k ** 2, F0 / k ** 2 if mm != 1 else F0 * mm / k ** 3], 'N', f'F ∝ Mm/r²: F = {F0} × {mm}/{k}² = {q(F1, "N")}.', extra=True)


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step')
def c4_kepler_derive(rng, slot):
    moon, planet, r, Td = pick(rng, MOONS)
    T_ = Td * 86400
    M = 4 * math.pi ** 2 * r ** 3 / (G * T_ ** 2)
    r2 = r * rng.choice([0.5, 1.6, 2.0, 3.0])
    T2 = T_ * (r2 / r) ** 1.5
    return num(f'(a) Show that for a moon in a circular orbit of radius r around a planet of mass M, T² = (4π²/GM) r³. (b) {moon} orbits {planet} at {q(r, "m")} with period {Td} days; calculate the mass of {planet}. (c) Predict the period of a probe placed in a circular orbit of radius {q(r2, "m")} around {planet}, and comment on whether its mass matters.',
               f'(b) {q(M, "kg")}; (c) {q(T2 / 86400, "days")}; the probe’s mass cancels',
               f'(a) GMm/r² = m·4π²r/T² (M1), rearranged (A1). (b) T = {q(T_, "s")}, M = 4π²r³/(GT²) = {q(M, "kg")} (M1 A1). (c) T₂ = T(r₂/r)^1.5 = {q(T2 / 86400, "days")} (A1); m cancels from both sides (R1).', 6, 'multi_step', 'G5')


R.mcqs('ch04-st1', 'C2', (1, 4), [
    ('A planet’s orbital radius around a star is four times that of another planet. The ratio of their periods T_outer/T_inner is', '8', ['4', '16', '2'], 'T ∝ r^(3/2): 4^1.5 = 8.'),
    ('Which observation led Newton to suggest that gravity is universal?', 'the same inverse-square force explains both falling objects on Earth and the Moon’s orbit', ['planets are spherical', 'the Sun is very hot', 'apples are heavier than leaves'], 'The "Moon test" compared the Moon’s centripetal acceleration with g scaled by 1/r².'),
    ('Kepler’s third law constant T²/r³ is the same for all planets of the Sun because it depends only on', 'the mass of the Sun', ['the mass of each planet', 'the radius of each planet', 'the speed of each planet'], 'T²/r³ = 4π²/GM.'),
])

R.static('ch04-st1', 'C4', (3, 5), [
    ('Cavendish’s torsion-balance experiment (1798) measured the tiny attraction between lead spheres. (a) Explain why the experiment was so difficult. (b) Explain why it is often described as "weighing the Earth". (c) Discuss one way modern measurements of G still disagree, and what this shows about the nature of science.',
     '(a) Forces of ~10⁻⁷ N had to be detected against air currents, temperature changes and vibrations; a long, fine fibre and enclosure were needed. (b) With G known, g = GM/R² gives M = gR²/G for the Earth. (c) Modern values of G from different methods differ by more than their stated uncertainties, suggesting unknown systematic errors; it shows that measurements carry uncertainty and are refined over time (NOS).',
     'Very small force and sources of disturbance (R1 R1); M = gR²/G (M1 A1); systematic discrepancies between labs and NOS comment (R1).'),
], type='multi_step', marks=5)


R.facts('ch04-st2', F(
    terms=[('gravitational field strength', 'the gravitational force per unit mass on a small test mass placed at a point, g = F/m'),
           ('gravitational field line', 'a line showing the direction of the gravitational force on a small test mass; the density of lines indicates field strength'),
           ('uniform gravitational field', 'a region where the field strength has the same magnitude and direction at all points, shown by parallel, equally spaced field lines')],
    facts=[('What is the gravitational field strength at a height equal to one Earth radius above the surface (surface g = 9.81 N kg⁻¹)?', '2.45 N kg⁻¹', ['4.91 N kg⁻¹', '9.81 N kg⁻¹', '1.09 N kg⁻¹'], 'r doubles, so g falls by a factor of 4.'),
           ('Gravitational field lines around an isolated planet are', 'radial and directed towards the centre', ['radial and directed outwards', 'parallel and equally spaced', 'circles around the planet'], 'Gravity is always attractive.'),
           ('The unit N kg⁻¹ for g is equivalent to', 'm s⁻²', ['m s⁻¹', 'kg m s⁻²', 'J kg⁻¹'], '1 N = 1 kg m s⁻².'),
           ('Close to the surface of Earth the field can be treated as uniform because', 'the height change is tiny compared with Earth’s radius', ['Earth is flat', 'g does not depend on distance', 'the field lines are circles'], 'Over small distances the radial lines are nearly parallel.')],
    why=[('Explain why the gravitational field strength at the surface of a planet is the same for all objects regardless of their mass.', 'g = F/m = GM/R²; the force is proportional to the object’s mass, so the force per unit mass depends only on the planet’s mass and radius.'),
         ('Explain why there is a point between Earth and the Moon where the net gravitational field strength is zero, and why it is much closer to the Moon.', 'Earth’s field points towards Earth and the Moon’s towards the Moon, so on the line between them they are opposite; they cancel where GM_E/x² = GM_M/(d − x)²; because the Moon’s mass is ~1/81 of Earth’s, this occurs at about 0.9 of the distance from Earth.'),
         ('Explain why g measured at the equator is slightly smaller than at the poles.', 'Earth is slightly flattened, so the equator is further from the centre; and part of the gravitational force provides the centripetal force for Earth’s rotation at the equator.')],
    contrast=[('gravitational force', 'gravitational field strength', 'Gravitational force (N) acts on a particular mass, F = GMm/r²; field strength (N kg⁻¹) is the force per unit mass at a point, independent of the test mass.')],
    misc=[('Gravitational field strength is zero at the altitude of the International Space Station.', 'At about 400 km g ≈ 8.7 N kg⁻¹; astronauts feel weightless because they are in free fall.'),
          ('Halving the distance from the centre of a planet halves the gravitational field strength.', 'Outside the planet g ∝ 1/r², so halving r makes g four times larger.')],
    evaluate=[('Field lines are real physical objects that surround a mass.', ['field lines correctly predict direction and relative strength'], ['they are a visual model; the field is continuous', 'the number of lines drawn is arbitrary', 'models help reasoning but are not reality (NOS)'], 'Field lines are a representation of the field, not physical objects; the field itself is real and measurable.')],
))


@R.add('ch04-st2', 'C3', (1, 5), 'numerical')
def c3_gfield(rng, slot):
    b, M, Rb = pick(rng, BODIES)
    frame = rng.randrange(4)
    if frame == 0:
        gs = G * M / Rb ** 2
        return num(f'{b[0].upper() + b[1:]} has a mass of {q(M, "kg")} and a radius of {q(Rb, "m")}. Calculate the gravitational field strength at its surface.',
                   q(gs, 'N kg⁻¹'), f'g = GM/R² (M1) = {q(gs, "N kg⁻¹")} (A1).', 2)
    if frame == 1:
        h = rng.choice([300, 600, 1000, 5000, 20200, 35800]) * 1e3
        gh = G * M / (Rb + h) ** 2 if b == 'Earth' else G * M_EARTH / (R_EARTH + h) ** 2
        return num(f'Calculate the gravitational field strength at a height of {sf(h / 1e3, 3)} km above the surface of Earth (M = 5.97 × 10²⁴ kg, R = 6.37 × 10⁶ m).',
                   q(gh, 'N kg⁻¹'), f'r = {q(R_EARTH + h, "m")} (M1); g = GM/r² = {q(gh, "N kg⁻¹")} (A1).', 2)
    if frame == 2:
        k = rng.choice([1.5, 2, 3, 4])
        g_s = G * M / Rb ** 2
        return num(f'The gravitational field strength at the surface of {b} is {sf(g_s)} N kg⁻¹. Determine the field strength at a distance of {k} planetary radii from its centre.',
                   q(g_s / k ** 2, 'N kg⁻¹'), f'g ∝ 1/r² (M1); g = {sf(g_s)}/{k}² = {q(g_s / k ** 2, "N kg⁻¹")} (A1).', 2)
    fm, fr = rng.choice([(2, 2), (0.5, 0.8), (3, 1.5), (0.1, 0.5), (8, 2)])
    return num(f'An exoplanet has {fm} times the mass of Earth and {fr} times its radius. Calculate the gravitational field strength at its surface (g on Earth = 9.81 N kg⁻¹).',
               q(9.81 * fm / fr ** 2, 'N kg⁻¹'), f'g ∝ M/R² (M1); g = 9.81 × {fm}/{fr}² = {q(9.81 * fm / fr ** 2, "N kg⁻¹")} (A1).', 2)


@R.add('ch04-st2', 'C3', (1, 4), 'mcq')
def c3_gfield_mcq(rng, slot):
    fm, fr = rng.choice([(2, 2), (4, 2), (0.5, 0.5), (9, 3), (3, 2), (6, 2)])
    gp = 9.81 * fm / fr ** 2
    return nmcq(rng, f'A planet has {fm} times the mass and {fr} times the radius of Earth. What is the gravitational field strength at its surface? (g_Earth = 9.81 N kg⁻¹)', gp,
                [9.81 * fm / fr, 9.81 * fm * fr ** 2, 9.81 * fr ** 2 / fm], 'N kg⁻¹', f'g = 9.81 × {fm}/{fr}² = {q(gp, "N kg⁻¹")}.')


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step')
def c4_null_point(rng, slot):
    pair = pick(rng, [('Earth', M_EARTH, 'the Moon', M_MOON, 3.84e8), ('Jupiter', 1.90e27, 'Io', 8.93e22, 4.22e8), ('the Sun', M_SUN, 'Earth', M_EARTH, 1.50e11)])
    a, Ma, b, Mb, d = pair
    x = d / (1 + math.sqrt(Mb / Ma))
    return num(f'{a[0].upper() + a[1:]} (mass {q(Ma, "kg")}) and {b} (mass {q(Mb, "kg")}) are {q(d, "m")} apart, centre to centre. (a) Explain why there is a point on the line between them where the net gravitational field strength is zero. (b) Determine its distance from the centre of {a}. (c) Sketch how the net field strength varies along the line and state its direction on either side of the point.',
               f'(b) {q(x, "m")} ({sf(x / d, 3)} of the separation)', f'(a) fields from the two bodies point in opposite directions between them (R1). (b) GMa/x² = GMb/(d − x)² (M1); x = d/(1 + √(Mb/Ma)) (M1) = {q(x, "m")} (A1). (c) towards {a} on its side of the point, towards {b} beyond it, zero at the point (R1).', 5, 'multi_step', 'G5')


R.mcqs('ch04-st2', 'C2', (1, 4), [
    ('A mass is moved from the surface of Earth to a height of 3R above the surface. Its weight becomes', 'one-sixteenth of its surface weight', ['one-ninth', 'one-third', 'one-quarter'], 'Distance from the centre goes from R to 4R.'),
    ('Two planets have the same density, but planet X has twice the radius of planet Y. The ratio g_X/g_Y is', '2', ['4', '1/2', '8'], 'g = GM/R² = (4/3)πGρR ∝ R.'),
    ('Inside a uniform spherical shell of matter, the gravitational field strength due to the shell is', 'zero', ['the same as at the surface', 'infinite', 'greater than at the surface'], 'Shell theorem.'),
])

repeat_readings('ch04-st2', 'the time for a ball to fall 1.20 m (used to find g)', 's', 0.48, 0.51, 3,
                ['dropped a steel ball through light gates and recorded the fall time on a timer.',
                 'used an electromagnet release and a trapdoor switch to time a falling ball.'])


def _g_drop_spec(rng):
    hs = [0.20, 0.40, 0.60, 0.80, 1.00, 1.20]
    ts = [round(math.sqrt(2 * h_ / g0) * rng.uniform(0.99, 1.01), 3) for h_ in hs]
    return dict(intro='A ball is dropped from rest from different heights h and its fall time t is measured with light gates. Theory: h = ½gt².',
                xname='h', xunit='m', yname='t', yunit='s', xs=hs, ys=ts, xfmt=lambda a: f'{a:.2f}', yfmt=lambda b: f'{b:.3f}',
                plot_x=lambda a: a, plot_y=lambda b: b * b, plot_label='t² (y) against h (x)', what='the acceleration of free fall g', what_short='g',
                gunit='s² m⁻¹', deduce=lambda m_, b_: (2 / m_, 'm s⁻²', 'g = 2/gradient'))


gradient_fit('ch04-st2', _g_drop_spec)


R.facts('ch04-st3', F(
    terms=[('orbital speed', 'the speed of a satellite in a circular orbit, v = √(GM/r)'),
           ('geostationary orbit', 'an equatorial orbit with a period of 24 hours (one sidereal day) in the same direction as Earth’s rotation, so the satellite stays above one point'),
           ('orbital period', 'the time for one complete orbit, T = 2πr/v')],
    facts=[('As the radius of a satellite’s circular orbit increases, its orbital speed', 'decreases', ['increases', 'is unchanged', 'first increases then decreases'], 'v = √(GM/r).'),
           ('A geostationary satellite must orbit', 'above the equator with a period of one day', ['over the poles', 'at any altitude with a period of one day', 'at the same height as the ISS'], 'Only an equatorial orbit can stay above one point.'),
           ('The centripetal force on an orbiting satellite is provided by', 'the gravitational force of the planet', ['the satellite’s engines', 'air resistance', 'the centrifugal force'], 'Gravity is the only force in orbit.'),
           ('The orbital speed of a satellite does not depend on', 'the mass of the satellite', ['the mass of the planet', 'the orbital radius', 'G'], 'm cancels.')],
    why=[('Explain why astronauts in orbit appear weightless.', 'The astronauts and their spacecraft are both in free fall with the same acceleration (the local g), so there is no normal contact force between them; they feel weightless although gravity acts.'),
         ('Explain why a satellite in a low orbit gradually spirals inwards and speeds up.', 'Drag from the thin upper atmosphere removes energy; the satellite falls to a lower orbit, where v = √(GM/r) is greater – loss of potential energy exceeds the gain in kinetic energy.'),
         ('Explain why the orbital speed of a satellite is independent of its mass.', 'Gravity provides the centripetal force: GMm/r² = mv²/r; the satellite mass m cancels, leaving v² = GM/r.')],
    contrast=[('a geostationary orbit', 'a polar orbit', 'A geostationary orbit is equatorial, at about 36 000 km altitude with a 24 h period, staying above one point (communications); a polar orbit is low with a period of ~100 minutes and passes over every part of Earth as it rotates beneath (mapping, weather).')],
    misc=[('Heavier satellites must travel faster to stay in the same orbit.', 'Orbital speed v = √(GM/r) is independent of the satellite mass.'),
          ('A satellite needs to fire its engines continuously to stay in orbit.', 'No force is needed along the motion; gravity alone supplies the centripetal force. Engines are only used to change orbit or correct for drag.')],
    evaluate=[('Low-Earth-orbit satellite constellations are better than geostationary satellites for internet access.', ['much lower signal delay (~20 ms vs ~250 ms)', 'smaller, cheaper satellites'], ['thousands are needed for coverage', 'increase collision and space-debris risk', 'shorter lifetimes due to drag', 'brightness interferes with astronomy'], 'LEO constellations offer lower latency but bring sustainability and debris costs; the "better" choice depends on use and how these costs are managed.')],
))


@R.add('ch04-st3', 'C3', (1, 5), 'numerical')
def c3_orbit(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        h = rng.choice([350, 420, 550, 800, 1200, 2000]) * 1e3
        r = R_EARTH + h
        v = math.sqrt(G * M_EARTH / r)
        T_ = 2 * math.pi * r / v
        return num(f'A satellite orbits Earth at a height of {sf(h / 1e3, 3)} km. Calculate its orbital speed and period (M_E = 5.97 × 10²⁴ kg, R_E = 6.37 × 10⁶ m).',
                   f'v = {q(v, "m s⁻¹")}; T = {q(T_ / 60, "min")}', f'r = {q(r, "m")} (A1); v = √(GM/r) (M1) = {q(v, "m s⁻¹")} (A1); T = 2πr/v = {q(T_, "s")} = {q(T_ / 60, "min")} (A1).', 4)
    if frame == 1:
        T_ = 86164
        r = (G * M_EARTH * T_ ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
        return num('Show that the orbital radius of a geostationary satellite is about 4.2 × 10⁷ m, and calculate its height above Earth’s surface. (Sidereal day = 86 164 s, M_E = 5.97 × 10²⁴ kg, R_E = 6.37 × 10⁶ m)',
                   f'r = {q(r, "m")}; h = {q(r - R_EARTH, "m")}', f'GMm/r² = m4π²r/T² (M1); r³ = GMT²/4π² (M1); r = {q(r, "m")} (A1); h = r − R_E = {q(r - R_EARTH, "m")} (A1).', 4)
    if frame == 2:
        b, M, Rb = pick(rng, BODIES[1:])
        h = rng.choice([100, 200, 500]) * 1e3
        v = math.sqrt(G * M / (Rb + h))
        return num(f'A probe orbits {b} (mass {q(M, "kg")}, radius {q(Rb, "m")}) {sf(h / 1e3, 3)} km above its surface. Calculate its orbital speed.',
                   q(v, 'm s⁻¹'), f'v = √(GM/(R + h)) (M1) = {q(v, "m s⁻¹")} (A1).', 2)
    T_h = rng.choice([2, 3, 6, 12])
    T_ = T_h * 3600
    r = (G * M_EARTH * T_ ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
    return num(f'A navigation satellite must orbit Earth with a period of {T_h} hours. Determine the radius of its orbit and its orbital speed.',
               f'r = {q(r, "m")}; v = {q(2 * math.pi * r / T_, "m s⁻¹")}', f'r³ = GMT²/4π² (M1); r = {q(r, "m")} (A1); v = 2πr/T = {q(2 * math.pi * r / T_, "m s⁻¹")} (A1).', 3)


@R.add('ch04-st3', 'C3', (1, 4), 'mcq')
def c3_orbit_mcq(rng, slot):
    v0 = rng.choice([4000, 6000, 7000, 7600])
    k = rng.choice([2, 4, 9, 16])
    v1 = v0 / math.sqrt(k)
    return nmcq(rng, f'A satellite orbits a planet at speed {v0} m s⁻¹. Another satellite orbits the same planet at {k} times the orbital radius. What is its orbital speed?', v1,
                [v0 / k, v0 * math.sqrt(k), v0 / k ** 2], 'm s⁻¹', f'v ∝ 1/√r: v = {v0}/√{k} = {q(v1, "m s⁻¹")}.', extra=False)


R.mcqs('ch04-st3', 'C2', (1, 4), [
    ('Two satellites P and Q orbit Earth; P has the larger orbital radius. Which is correct?', 'P has the longer period and the lower speed', ['P has the shorter period and the higher speed', 'P has the longer period and the higher speed', 'both have the same period'], 'T ∝ r^1.5 and v ∝ r^−0.5.'),
    ('The International Space Station orbits at about 400 km. The gravitational field strength there is about', '90 % of the surface value', ['zero', '10 % of the surface value', 'the same as at the surface'], '(6.37/6.77)² ≈ 0.89.'),
    ('A satellite in a circular orbit has its speed suddenly increased slightly by a rocket burn. It will', 'move into an elliptical orbit that takes it further away', ['fall towards the planet', 'stay in the same circular orbit', 'escape immediately'], 'Extra kinetic energy raises the opposite side of the orbit.'),
])

R.static('ch04-st3', 'C4', (3, 5), [
    ('Discuss the physics and the trade-offs involved in choosing between a polar low-Earth orbit (height ~800 km) and a geostationary orbit for a weather satellite.',
     'Polar LEO: period ~100 min (from T² = 4π²r³/GM), Earth rotates beneath so the satellite eventually views every region at high resolution, but each location is seen only a few times a day. Geostationary: r ≈ 4.2 × 10⁷ m, period 24 h, continuous view of one hemisphere for tracking storms, but low resolution and poor view of polar regions; launching there needs more energy. Weather agencies use both.',
     'LEO period calculated or justified (M1 A1); geostationary conditions stated (R1); coverage/resolution trade-off (R1); energy cost of launch (R1); balanced judgement (A1).', 6),
], type='multi_step', marks=6)

linearise('ch04-st3', [
    ('T² = (4π²/GM) r³ for the moons of Jupiter', 'T²', 'r³', '4π²/(GM), from which M = 4π²/(G × gradient)', 'The line should pass through the origin.'),
    ('v² = GM/r for satellites in circular orbits around Earth', 'v²', '1/r', 'GM for Earth', 'A straight line through the origin confirms v ∝ r^−½.'),
])


def _kepler_spec(rng):
    data = [(4.22e8, 1.769), (6.71e8, 3.551), (1.07e9, 7.155), (1.88e9, 16.69), (1.81e8, 0.498), (1.29e8, 0.295)]
    data.sort()
    rs = [r for r, _ in data]
    Ts = [round(t * rng.uniform(0.995, 1.005), 3) for _, t in data]
    return dict(intro='Data for six moons of Jupiter: orbital radius r and period T. Kepler’s third law predicts T² = (4π²/GM) r³.',
                xname='r', xunit='10⁸ m', yname='T', yunit='days', xs=[r / 1e8 for r in rs], ys=Ts, xfmt=lambda a: f'{a:.2f}', yfmt=lambda b: f'{b:.3f}',
                plot_x=lambda a: (a * 1e8) ** 3, plot_y=lambda b: (b * 86400) ** 2, plot_label='T² in s² (y) against r³ in m³ (x)', what='the mass of Jupiter', what_short='the mass of Jupiter',
                gunit='s² m⁻³', deduce=lambda m_, b_: (4 * math.pi ** 2 / (G * m_), 'kg', 'M = 4π²/(G × gradient)'))


gradient_fit('ch04-st3', _kepler_spec)


R.facts('ch04-st4', F(
    terms=[('gravitational potential', 'the work done per unit mass in bringing a small test mass from infinity to a point in a gravitational field, V = −GM/r'),
           ('gravitational potential energy', 'the work done in bringing a mass from infinity to a point in a field, Eₚ = −GMm/r'),
           ('escape speed', 'the minimum speed an object needs at the surface of a body to escape to infinity without further propulsion, v = √(2GM/R)'),
           ('equipotential surface', 'a surface on which every point has the same gravitational potential; no work is done moving along it')],
    facts=[('Why is gravitational potential always negative?', 'zero is defined at infinity and work must be done to move a mass away to infinity', ['mass can be negative', 'gravity is repulsive', 'potential energy is never conserved'], 'V = −GM/r < 0 for all finite r.'),
           ('The total energy of a satellite in a circular orbit of radius r is', '−GMm/2r', ['−GMm/r', '+GMm/2r', 'GMm/r²'], 'Eₖ = GMm/2r, Eₚ = −GMm/r.'),
           ('Gravitational field lines and equipotential surfaces meet at', '90°', ['0°', '45°', 'any angle'], 'g = −ΔV/Δr: the field is along the steepest potential change.'),
           ('The escape speed from a planet depends on', 'the mass and radius of the planet', ['the mass of the escaping object', 'the direction of launch only', 'the planet’s temperature'], 'v = √(2GM/R).')],
    why=[('Explain why a satellite moving to a higher circular orbit gains total energy even though its kinetic energy decreases.', 'Total energy is −GMm/2r, which becomes less negative (increases) as r increases; the gain in potential energy (GMm/r₁ − GMm/r₂) is twice the loss of kinetic energy.'),
         ('Explain why the Moon has no atmosphere while Earth does.', 'The Moon’s escape speed (2.4 km s⁻¹) is low; at lunar day-side temperatures a significant fraction of gas molecules exceed it (or a sizeable fraction of the escape speed), so gas leaks away over geological time; Earth’s escape speed (11.2 km s⁻¹) is large enough to retain N₂ and O₂.'),
         ('Explain why the gravitational field strength is equal to the negative potential gradient.', 'The work done per unit mass moving a small distance Δr against the field is −gΔr = ΔV, so g = −ΔV/Δr; the field points towards decreasing potential.')],
    contrast=[('gravitational potential', 'gravitational potential energy', 'Potential (J kg⁻¹) is a property of a point in the field, V = −GM/r; potential energy (J) belongs to a mass at that point, Eₚ = mV = −GMm/r.')],
    misc=[('Escape speed depends on the mass of the rocket.', 'v_esc = √(2GM/R) does not depend on the escaping mass; a heavier rocket needs more energy, not more speed.'),
          ('mgh can be used to find the energy needed to send a probe from Earth’s surface to the Moon.', 'mgh assumes uniform g; over large distances g changes, so ΔEₚ = GMm(1/r₁ − 1/r₂) must be used.'),
          ('The potential energy of a satellite is zero at the surface of Earth.', 'With zero at infinity the potential energy is negative everywhere, most negative at the surface.')],
    evaluate=[('Escape speed is the speed a rocket must reach to leave Earth.', ['it is the minimum launch speed for an unpowered projectile to reach infinity'], ['rockets keep firing their engines and need not reach 11.2 km s⁻¹ at the surface', 'air resistance and Earth’s rotation also matter', 'reaching orbit needs less than escape speed'], 'The concept applies to unpowered projectiles; real rockets gain energy gradually and need not reach escape speed near the surface.')],
))


@R.add('ch04-st4', 'C3', (1, 5), 'numerical')
def c3_potential(rng, slot):
    b, M, Rb = pick(rng, BODIES)
    frame = rng.randrange(5)
    if frame == 0:
        ve = math.sqrt(2 * G * M / Rb)
        return num(f'Calculate the escape speed from the surface of {b} (mass {q(M, "kg")}, radius {q(Rb, "m")}).', q(ve, 'm s⁻¹'),
                   f'½mv² = GMm/R (M1); v = √(2GM/R) = {q(ve, "m s⁻¹")} (A1).', 2)
    if frame == 1:
        V = -G * M / Rb
        return num(f'Calculate the gravitational potential at the surface of {b} (mass {q(M, "kg")}, radius {q(Rb, "m")}).', q(V, 'J kg⁻¹').replace('-', '−'),
                   f'V = −GM/R (M1) = {q(V, "J kg⁻¹")} (A1).'.replace('-', '−'), 2)
    m_ = rng.choice([500, 1000, 2500, 4000])
    h1, h2 = sorted(rng.sample([300, 500, 800, 2000, 20000, 35800], 2))
    r1, r2 = R_EARTH + h1 * 1e3, R_EARTH + h2 * 1e3
    if frame == 2:
        dE = G * M_EARTH * m_ * (1 / r1 - 1 / r2)
        return num(f'A {m_} kg satellite is moved from a circular orbit {h1} km above Earth to one {h2} km above Earth. Calculate the change in its gravitational potential energy.',
                   f'increase of {q(dE, "J")}', f'ΔEₚ = GMm(1/r₁ − 1/r₂) (M1); r₁ = {q(r1, "m")}, r₂ = {q(r2, "m")} (A1); ΔEₚ = {q(dE, "J")} (A1).', 3)
    if frame == 3:
        Et1, Et2 = -G * M_EARTH * m_ / (2 * r1), -G * M_EARTH * m_ / (2 * r2)
        return num(f'Determine the minimum energy needed to move a {m_} kg satellite from a circular orbit {h1} km above Earth to a circular orbit {h2} km above Earth.',
                   q(Et2 - Et1, 'J'), f'E_total = −GMm/2r (M1); E₂ − E₁ = GMm/2 (1/r₁ − 1/r₂) (M1) = {q(Et2 - Et1, "J")} (A1).', 3)
    v = rng.choice([3000, 5000, 7000, 9000])
    vmax = math.sqrt(2 * G * M_EARTH / R_EARTH)
    rmax = 1 / (1 / R_EARTH - v * v / (2 * G * M_EARTH))
    return num(f'A projectile is launched vertically from Earth’s surface at {v} m s⁻¹. Ignoring air resistance, determine the maximum distance from Earth’s centre that it reaches.',
               q(rmax, 'm'), f'½v² − GM/R = −GM/r (M1); 1/r = 1/R − v²/(2GM) (M1); r = {q(rmax, "m")} (A1). (Less than escape speed {q(vmax, "m s⁻¹")}.)', 3)


@R.add('ch04-st4', 'C3', (1, 4), 'mcq')
def c3_escape_mcq(rng, slot):
    fm, fr = rng.choice([(2, 2), (4, 1), (8, 2), (0.5, 2), (9, 4)])
    ve = 11.2 * math.sqrt(fm / fr)
    return nmcq(rng, f'The escape speed from Earth is 11.2 km s⁻¹. What is the escape speed from a planet with {fm} times Earth’s mass and {fr} times its radius?', ve,
                [11.2 * fm / fr, 11.2 * math.sqrt(fm) / fr, 11.2 * fm / fr ** 2], 'km s⁻¹', f'v ∝ √(M/R): 11.2 × √({fm}/{fr}) = {q(ve, "km s⁻¹")}.')


@R.add('ch04-st4', 'C4', (3, 5), 'multi_step')
def c4_orbit_energy(rng, slot):
    m_ = rng.choice([800, 1500, 3000])
    h = rng.choice([400, 600, 1000]) * 1e3
    r = R_EARTH + h
    Ek = G * M_EARTH * m_ / (2 * r)
    Ep = -G * M_EARTH * m_ / r
    Esurf = -G * M_EARTH * m_ / R_EARTH
    need = (Ek + Ep) - Esurf
    return num(f'A {m_} kg satellite is to be placed in a circular orbit {sf(h / 1e3, 3)} km above Earth. (a) Calculate its kinetic, potential and total energy in orbit. (b) Determine the minimum energy required to put it there from rest on Earth’s surface (ignore Earth’s rotation and air resistance). (c) Explain why launch sites near the equator reduce this energy.',
               f'(a) Eₖ = {q(Ek, "J")}, Eₚ = {q(Ep, "J")}, E = {q(Ek + Ep, "J")}; (b) {q(need, "J")}; (c) Earth’s rotation already gives the rocket up to 465 m s⁻¹ eastwards'.replace('-', '−'),
               f'(a) Eₖ = GMm/2r (M1) = {q(Ek, "J")} (A1); Eₚ = −GMm/r = {q(Ep, "J")} (A1); E = {q(Ek + Ep, "J")} (A1). (b) E_orbit − E_surface (M1) = {q(need, "J")} (A1). (c) rotational speed largest at the equator (R1).'.replace('-', '−'), 7, 'multi_step', 'G5')


R.mcqs('ch04-st4', 'C2', (1, 4), [
    ('The gravitational potential at distance r from a planet’s centre is −V. At distance 2r it is', '−V/2', ['−V/4', '−2V', '+V/2'], 'V ∝ −1/r.'),
    ('A mass moves along an equipotential surface. The work done by the gravitational field is', 'zero', ['positive', 'negative', 'equal to mgh'], 'ΔV = 0.'),
    ('When a satellite moves to a lower circular orbit, its kinetic energy', 'increases and its total energy decreases', ['decreases and its total energy increases', 'increases and its total energy increases', 'is unchanged'], 'Eₖ = GMm/2r grows; E = −GMm/2r becomes more negative.'),
])


# =============================================================================================
# ch05 D.2 Electric and magnetic fields
# =============================================================================================
def esc(x, unit=''):
    return q(x, unit).replace('-', '−')


R.facts('ch05-st1', F(
    terms=[("Coulomb's law", 'the electric force between two point charges is proportional to the product of the charges and inversely proportional to the square of their separation, F = kq₁q₂/r²'),
           ('conservation of charge', 'the total electric charge of an isolated system remains constant'),
           ('elementary charge', 'the magnitude of the charge on a proton or electron, e = 1.60 × 10⁻¹⁹ C; all free charges are whole-number multiples of it'),
           ('charging by friction', 'the transfer of electrons from one insulating material to another when they are rubbed together')],
    facts=[('A plastic rod becomes negatively charged when rubbed with a cloth. This is because', 'electrons are transferred from the cloth to the rod', ['protons are transferred from the rod to the cloth', 'electrons are created in the rod', 'positive charge is destroyed in the rod'], 'Only electrons move; charge is conserved.'),
           ('The force between two point charges is F. Both charges are doubled and their separation is doubled. The new force is', 'F', ['2F', '4F', 'F/2'], '(2 × 2)/2² = 1.'),
           ('The value of the Coulomb constant k is', '8.99 × 10⁹ N m² C⁻²', ['6.67 × 10⁻¹¹ N m² kg⁻²', '8.85 × 10⁻¹² C² N⁻¹ m⁻²', '1.60 × 10⁻¹⁹ C'], 'k = 1/(4πε₀).'),
           ('A metal sphere is charged by induction using a negatively charged rod. The final charge on the sphere is', 'positive', ['negative', 'zero', 'the same sign as the rod'], 'Electrons are repelled to earth, leaving the sphere positive.')],
    why=[('Explain why a charged balloon sticks to an uncharged wall.', 'The negative balloon repels electrons in the wall’s surface molecules slightly (polarisation), so the nearby surface is slightly positive; attraction to the nearer positive charge exceeds repulsion from the farther negative charge because force decreases with distance.'),
         ('Explain why electric forces dominate over gravitational forces between an electron and a proton.', 'The ratio F_e/F_g = ke²/(Gmₑmₚ) ≈ 2 × 10³⁹ because k is enormous compared with G and the masses are tiny; gravity only dominates for large neutral bodies.'),
         ('Explain what is meant by the statement that charge is quantised, and how Millikan’s experiment showed this.', 'Charge exists only in whole-number multiples of e; Millikan balanced oil drops in an electric field and found that all their charges were multiples of 1.6 × 10⁻¹⁹ C.')],
    contrast=[('a conductor', 'an insulator', 'A conductor has free charge carriers (electrons) that move through it, so charge spreads over its surface; an insulator has no free carriers, so charge stays where it is placed.'),
              ("Coulomb's law", "Newton's law of gravitation", 'Both are inverse-square laws for point sources; electric forces can attract or repel and depend on charge with k = 8.99 × 10⁹ N m² C⁻², while gravity only attracts, depends on mass and G is about 10²⁰ times smaller.')],
    misc=[('Rubbing a rod creates charge on it.', 'Charge is transferred, not created: the cloth gains an equal and opposite charge (conservation of charge).'),
          ('A positively charged object has gained protons.', 'It has lost electrons; protons are bound in nuclei and do not move in everyday charging.'),
          ('Coulomb’s law applies to any two charged objects at any separation.', 'It applies to point charges (or spherically symmetric charge distributions) in a vacuum; for other shapes the force must be summed over the distribution.')],
    evaluate=[('The inverse-square form of Coulomb’s law is exact.', ['experiments limit deviations of the exponent from 2 to less than 10⁻¹⁶', 'it follows from field lines spreading over 4πr²'], ['at sub-atomic distances quantum effects modify the interaction', 'in materials ε differs from ε₀', 'all laws are tested to finite precision (NOS)'], 'It is one of the most precisely tested laws in physics, accurate to extraordinary precision in its domain; "exact" is a claim science can only support to a measured limit.')],
))


@R.add('ch05-st1', 'C3', (1, 5), 'numerical')
def c3_coulomb(rng, slot):
    frame = rng.randrange(5)
    if frame == 0:
        q1 = rng.choice([1.5, 2.0, 3.0, 4.5, 6.0]) * 1e-6
        q2 = rng.choice([-2.0, 2.5, -4.0, 5.0, -1.2]) * 1e-6
        r = rng.choice([0.02, 0.05, 0.10, 0.15, 0.30])
        F_ = K * q1 * abs(q2) / r ** 2
        return num(f'Two small charged spheres carry charges of +{sf(q1 * 1e6, 2)} μC and {sf(q2 * 1e6, 2).replace("-", "−")} μC. Their centres are {sf(r * 100, 2)} cm apart. Calculate the magnitude of the electric force between them and state whether it is attractive or repulsive.',
                   f'{q(F_, "N")}, {"attractive" if q2 < 0 else "repulsive"}', f'F = kq₁q₂/r² (M1) = 8.99 × 10⁹ × {sf(q1)} × {sf(abs(q2))}/{sf(r)}² = {q(F_, "N")} (A1); {"opposite" if q2 < 0 else "like"} charges (A1).', 3)
    if frame == 1:
        Q = rng.choice([-3.2e-9, -8.0e-9, 4.8e-9, 1.6e-8, -2.4e-8])
        N = abs(Q) / E
        return num(f'A dust particle has a charge of {esc(Q, "C")}. Determine the number of electrons it has {"gained" if Q < 0 else "lost"}.',
                   f'{sf(N, 3)} electrons', f'N = |Q|/e = {sf(abs(Q))}/1.60 × 10⁻¹⁹ (M1) = {sf(N, 3)} (A1).', 2)
    if frame == 2:
        r = rng.choice([5.3e-11, 1.0e-10, 2.0e-15])
        Fe = K * E * E / r ** 2
        Fg = G * ME * MP / r ** 2
        return num(f'An electron and a proton are separated by {q(r, "m")}. Calculate the electric force and the gravitational force between them and the ratio of the two.',
                   f'F_e = {q(Fe, "N")}; F_g = {q(Fg, "N")}; ratio {sf(Fe / Fg)}', f'F_e = ke²/r² = {q(Fe, "N")} (A1); F_g = Gmₑmₚ/r² = {q(Fg, "N")} (A1); ratio = {sf(Fe / Fg)}, independent of r (A1).', 3)
    if frame == 3:
        qa, qb = rng.choice([2, 3, 4, 5]) * 1e-6, rng.choice([-1, -2, 6, 8]) * 1e-6
        tot = (qa + qb) / 2
        r = rng.choice([0.05, 0.10, 0.20])
        F_ = K * tot * tot / r ** 2
        return num(f'Two identical small conducting spheres carry charges of +{sf(qa * 1e6, 2)} μC and {sf(qb * 1e6, 2).replace("-", "−")} μC. They are touched together and then separated to {sf(r * 100, 2)} cm apart. Determine the charge on each sphere and the force between them.',
                   f'{sf(tot * 1e6, 2).replace("-", "−")} μC each; {q(F_, "N")} repulsive', f'Charge is conserved and shared equally: ({sf(qa * 1e6, 2)} + ({sf(qb * 1e6, 2)}))/2 = {sf(tot * 1e6, 2)} μC (M1 A1); F = kq²/r² = {q(F_, "N")} (A1), repulsive (like charges).', 3)
    q1, q2, q3 = rng.choice([2, 4]) * 1e-6, rng.choice([-3, 3, 5]) * 1e-6, rng.choice([1, 2]) * 1e-6
    a, b = rng.choice([0.10, 0.20]), rng.choice([0.10, 0.15, 0.30])
    F13 = K * q1 * q3 / a ** 2
    F23 = K * q2 * q3 / b ** 2
    net = F13 - F23
    return num(f'Three point charges lie on a straight line: A (+{sf(q1 * 1e6, 2)} μC), then C (+{sf(q3 * 1e6, 2)} μC) {sf(a * 100, 2)} cm to the right of A, then B ({sf(q2 * 1e6, 2).replace("-", "−")} μC) {sf(b * 100, 2)} cm to the right of C. Determine the resultant force on C.',
               f'{q(abs(net), "N")} to the {"right" if net > 0 else "left"}', f'Force from A: {q(F13, "N")} to the right (A1); force from B: {q(abs(F23), "N")} to the {"left" if q2 > 0 else "right"} (A1); vector sum (M1) = {q(abs(net), "N")} to the {"right" if net > 0 else "left"} (A1).', 4, 'multi_step')


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def c3_coulomb_mcq(rng, slot):
    F0 = rng.choice([8, 12, 18, 24, 36])
    a, b = rng.choice([(2, 2), (3, 1), (1, 3), (2, 0.5), (4, 2)])
    F1 = F0 * a / b ** 2
    return nmcq(rng, f'Two point charges exert a force of {F0} N on each other. One charge is multiplied by {a} and the separation is multiplied by {b}. What is the new force?', F1,
                [F0 * a / b, F0 * a * b ** 2, F0 / (a * b ** 2)], 'N', f'F ∝ q₁q₂/r²: {F0} × {a}/{b}² = {q(F1, "N")}.', extra=True)


R.mcqs('ch05-st1', 'C2', (1, 4), [
    ('A positively charged rod is brought near (but not touching) an uncharged, isolated metal sphere. The sphere', 'is attracted, because electrons gather on the near side', ['is repelled', 'experiences no force', 'becomes positively charged overall'], 'Induced separation: near side negative, net attraction.'),
    ('Which of these charges could NOT exist on an isolated object?', '2.4 × 10⁻¹⁹ C', ['3.2 × 10⁻¹⁹ C', '4.8 × 10⁻¹⁹ C', '1.6 × 10⁻¹⁸ C'], '2.4 × 10⁻¹⁹ C = 1.5e is not a whole multiple of e.'),
    ('Two point charges +Q and +4Q are a distance d apart. A third charge feels no force at a point between them that is', 'd/3 from +Q', ['d/2 from +Q', 'd/4 from +Q', '2d/3 from +Q'], 'Q/x² = 4Q/(d − x)² → x = d/3.'),
])

repeat_readings('ch05-st1', 'the deflection angle of a charged pith ball near a charged sphere', '°', 8.0, 16.0, 1,
                ['investigated Coulomb’s law using a charged pith ball on a thread and measured its deflection.',
                 'used a light conducting ball on an insulating thread and a protractor scale to estimate electric forces.'])

R.static('ch05-st1', 'C4', (3, 5), [
    ('Two identical small balls, each of mass 0.20 g, hang from a common point on insulating threads 0.50 m long. They are given equal charges and come to rest with each thread at 10° to the vertical. (a) Draw a free-body diagram for one ball. (b) Determine the electric force on each ball. (c) Determine the charge on each ball.',
     '(a) weight down, tension along the thread, electric force horizontal away from the other ball; (b) F = mg tan 10° = 3.46 × 10⁻⁴ N; (c) separation = 2 × 0.50 sin 10° = 0.174 m; q = r√(F/k) = 3.4 × 10⁻⁸ C.',
     'Three forces correctly shown (A1); T cos θ = mg and T sin θ = F (M1); F = 3.46 × 10⁻⁴ N (A1); separation 0.174 m (A1); q = 3.4 × 10⁻⁸ C (A1).'),
], type='multi_step', marks=5)


R.facts('ch05-st2', F(
    terms=[('electric field strength', 'the electric force per unit positive charge on a small test charge placed at a point, E = F/q'),
           ('electric field line', 'a line showing the direction of the force on a small positive test charge'),
           ('uniform electric field', 'a field of constant magnitude and direction, as between parallel charged plates, where E = V/d')],
    facts=[('Electric field lines start on', 'positive charges and end on negative charges', ['negative charges and end on positive charges', 'neutral objects', 'any conductor'], 'Direction of force on a positive test charge.'),
           ('The field strength between parallel plates 4.0 mm apart with a p.d. of 200 V is', '5.0 × 10⁴ V m⁻¹', ['800 V m⁻¹', '50 V m⁻¹', '5.0 × 10⁻⁴ V m⁻¹'], 'E = V/d = 200/0.004.'),
           ('The unit N C⁻¹ is equivalent to', 'V m⁻¹', ['V m', 'J C', 'C m⁻¹'], '1 V = 1 J C⁻¹ so N C⁻¹ = J m⁻¹ C⁻¹ = V m⁻¹.'),
           ('The field lines near the surface of a charged conductor are', 'perpendicular to the surface', ['parallel to the surface', 'at 45° to the surface', 'circles around the conductor'], 'Otherwise charges would move along the surface.')],
    why=[('Explain why the field between two large parallel plates is uniform except near the edges.', 'Between the plates the field lines run straight from one plate to the other, parallel and equally spaced, so E = V/d everywhere; at the edges the lines bulge outwards (fringing) and the field weakens.'),
         ('Explain why there is no electric field inside a hollow charged conductor.', 'Free charges in a conductor move until there is no field inside the metal; the charge resides on the outer surface and the fields from all parts cancel inside – the basis of a Faraday cage.'),
         ('Explain how the separation of field lines represents the strength of an electric field.', 'Field strength is proportional to the number of lines passing through unit area perpendicular to them; where lines are closer together the field is stronger.')],
    contrast=[('electric field strength', 'electric force', 'Field strength (N C⁻¹) is a property of the point, independent of the test charge; force (N) is the field multiplied by the charge placed there, F = qE.'),
              ('a radial field', 'a uniform field', 'A radial field around a point charge has E = kQ/r², decreasing with distance and lines spreading out; a uniform field between parallel plates has E = V/d, the same everywhere, with parallel equally spaced lines.')],
    misc=[('Field lines show the path a charged particle will follow.', 'Field lines show the direction of the force (and acceleration), not the trajectory; a moving particle can cross field lines.'),
          ('Doubling the plate separation at constant voltage doubles the field strength.', 'E = V/d, so doubling d halves E.'),
          ('An electron in an electric field is pushed along the direction of the field lines.', 'Field lines show the force on a positive charge; an electron is pushed in the opposite direction.')],
    evaluate=[('The concept of a field is merely a calculation tool rather than a physical reality.', ['forces can be computed by Coulomb’s law without mentioning fields'], ['fields carry energy and momentum (e.g. electromagnetic waves)', 'changes propagate at finite speed c', 'field theories underpin modern physics'], 'Fields began as a model (Faraday), but the propagation of electromagnetic waves carrying energy shows they are physical entities.')],
))


@R.add('ch05-st2', 'C3', (1, 5), 'numerical')
def c3_efield(rng, slot):
    frame = rng.randrange(5)
    if frame == 0:
        V = rng.choice([50, 120, 250, 400, 1500, 5000])
        d = rng.choice([2.0, 4.0, 5.0, 8.0, 12.0, 25.0]) * 1e-3
        Ef = V / d
        F_ = E * Ef
        return num(f'Two parallel plates are {sf(d * 1e3, 2)} mm apart with a potential difference of {V} V. Calculate the field strength between the plates and the force on an electron between them.',
                   f'E = {q(Ef, "V m⁻¹")}; F = {q(F_, "N")}', f'E = V/d (M1) = {q(Ef, "V m⁻¹")} (A1); F = eE = {q(F_, "N")} (A1).', 3)
    if frame == 1:
        Q = rng.choice([1.0, 2.5, 5.0, 8.0]) * 1e-9
        r = rng.choice([0.02, 0.05, 0.10, 0.25])
        return num(f'Calculate the electric field strength {sf(r * 100, 2)} cm from a point charge of +{sf(Q * 1e9, 2)} nC.',
                   q(K * Q / r ** 2, 'N C⁻¹'), f'E = kQ/r² (M1) = {q(K * Q / r ** 2, "N C⁻¹")} (A1).', 2)
    if frame == 2:
        mdrop = rng.choice([1.2, 2.4, 3.3, 4.9]) * 1e-15
        n = rng.choice([2, 3, 4, 5, 6])
        Ef = mdrop * g0 / (n * E)
        d = 5.0e-3
        return num(f'In a Millikan-type experiment an oil drop of mass {q(mdrop, "kg")} is held stationary between horizontal plates {sf(d * 1e3, 2)} mm apart. The drop carries {n} excess electrons. Calculate the field strength and the potential difference required.',
                   f'E = {q(Ef, "N C⁻¹")}; V = {q(Ef * d, "V")}', f'qE = mg (M1); E = mg/(ne) = {q(Ef, "N C⁻¹")} (A1); V = Ed = {q(Ef * d, "V")} (A1).', 3)
    if frame == 3:
        Q1 = rng.choice([2, 4, 6]) * 1e-9
        Q2 = rng.choice([2, 3, 8]) * 1e-9 * rng.choice([1, -1])
        d = rng.choice([0.10, 0.20])
        mid = d / 2
        E1 = K * Q1 / mid ** 2
        E2 = K * Q2 / mid ** 2
        net = E1 - E2
        return num(f'Point charges of +{sf(Q1 * 1e9, 2)} nC and {sf(Q2 * 1e9, 2).replace("-", "−")} nC are {sf(d * 100, 2)} cm apart. Determine the magnitude and direction of the electric field at the midpoint.',
                   f'{q(abs(net), "N C⁻¹")} directed {"away from" if net > 0 else "towards"} the +{sf(Q1 * 1e9, 2)} nC charge',
                   f'E from each = kQ/r² with r = {sf(mid * 100, 2)} cm (M1): {q(E1, "N C⁻¹")} and {q(abs(E2), "N C⁻¹")} (A1); combine as vectors (M1); {q(abs(net), "N C⁻¹")} (A1).', 4, 'multi_step')
    Q1 = rng.choice([1, 2, 4]) * 1e-9
    k_ = rng.choice([4, 9, 16])
    Q2 = k_ * Q1
    d = rng.choice([0.12, 0.30, 0.60])
    x = d / (1 + math.sqrt(k_))
    return num(f'Two positive point charges, +{sf(Q1 * 1e9, 2)} nC and +{sf(Q2 * 1e9, 2)} nC, are {sf(d * 100, 2)} cm apart. Find the position between them where the electric field strength is zero.',
               f'{q(x * 100, "cm")} from the +{sf(Q1 * 1e9, 2)} nC charge', f'kQ₁/x² = kQ₂/(d − x)² (M1); (d − x)/x = √{k_} = {int(math.sqrt(k_))} (M1); x = {q(x * 100, "cm")} (A1).', 3)


@R.add('ch05-st2', 'C3', (1, 4), 'mcq')
def c3_efield_mcq(rng, slot):
    V = rng.choice([100, 200, 300, 500, 600])
    d = rng.choice([2, 4, 5, 10])
    Ef = V / (d * 1e-3)
    return nmcq(rng, f'Parallel plates {d} mm apart have a p.d. of {V} V. What is the electric field strength between them?', Ef,
                [V * d * 1e-3, V / d, V / (d * 1e-2)], 'V m⁻¹', f'E = V/d = {V}/{d} × 10⁻³ = {q(Ef, "V m⁻¹")}.', extra=False)


R.mcqs('ch05-st2', 'C2', (1, 4), [
    ('At a point P the electric field due to a point charge is E. At twice the distance from the charge, the field is', 'E/4', ['E/2', '2E', 'E'], 'E ∝ 1/r².'),
    ('An electron is released from rest in a uniform electric field. Its subsequent motion is', 'uniform acceleration opposite to the field direction', ['uniform velocity along the field', 'circular', 'uniform acceleration along the field'], 'F = −eE is constant.'),
    ('Which field pattern has straight, parallel, equally spaced lines?', 'between two oppositely charged parallel plates', ['around a point charge', 'around two like charges', 'around a charged sphere'], 'Uniform field.'),
    ('The plate separation of a parallel-plate arrangement is halved while the plates stay connected to the same battery. The field strength', 'doubles', ['halves', 'is unchanged', 'quadruples'], 'E = V/d.'),
])

R.static('ch05-st2', 'C4', (3, 5), [
    ('An inkjet printer uses charged droplets deflected by a uniform electric field. Discuss how the deflection of a droplet depends on its charge, mass, speed and the field, and suggest why the printer charges droplets by different amounts.',
     'In the plates the droplet has acceleration a = qE/m perpendicular to its velocity; time between plates t = L/v; deflection y = ½(qE/m)(L/v)². So y ∝ q, ∝ E, ∝ 1/m and ∝ 1/v². By giving each droplet a different charge, the printer places drops at different positions on the paper with fixed plates.',
     'a = qE/m (M1); t = L/v (M1); y = qEL²/(2mv²) (A1); dependence on each variable stated (R1); charge controls landing position (R1).'),
], type='multi_step', marks=5)


R.facts('ch05-st3', F(
    terms=[('magnetic field', 'a region in which a moving charge, a current-carrying conductor or a magnet experiences a force'),
           ('magnetic flux density', 'the strength of a magnetic field, measured in tesla (T); 1 T is the field in which a 1 m wire carrying 1 A at right angles experiences a force of 1 N'),
           ('solenoid', 'a long coil of wire which, when carrying a current, produces a nearly uniform magnetic field inside it'),
           ('right-hand grip rule', 'with the thumb along the conventional current, the curled fingers show the direction of the magnetic field lines around the wire')],
    facts=[('The magnetic field lines around a long straight wire carrying a current are', 'concentric circles centred on the wire', ['straight lines parallel to the wire', 'radial lines from the wire', 'ellipses along the wire'], 'Right-hand grip rule.'),
           ('Inside a long solenoid carrying a steady current, the field is', 'strong and nearly uniform, parallel to the axis', ['zero', 'circular around the axis', 'strongest at the walls'], 'Like a bar magnet with parallel internal field lines.'),
           ('The field strength at distance r from a long straight wire is proportional to', '1/r', ['1/r²', 'r', 'r²'], 'B = μ₀I/(2πr).'),
           ('Which change does NOT increase the field inside a solenoid?', 'increasing its length while keeping the same number of turns', ['increasing the current', 'adding more turns over the same length', 'inserting an iron core'], 'B = μ₀nI with n = N/L.')],
    why=[('Explain why an iron core greatly increases the field of an electromagnet.', 'The iron becomes magnetised: its magnetic domains align with the solenoid’s field and add their own field, multiplying the flux density many times.'),
         ('Explain why magnetic field lines never cross.', 'The field at any point has a single direction; if two lines crossed, the field would have two directions there.'),
         ('Explain why Earth’s field must be considered when measuring the field of a wire with a compass.', 'A compass aligns with the resultant of Earth’s horizontal field and the wire’s field, so the deflection depends on both.')],
    contrast=[('the field of a long straight wire', 'the field inside a long solenoid', 'Around a wire, the lines are concentric circles and B = μ₀I/(2πr) decreases with distance; inside a solenoid, the lines are parallel to the axis and B = μ₀nI is uniform, independent of position.'),
              ('a magnetic field', 'an electric field', 'Magnetic fields act on moving charges and magnets, have closed field lines with no isolated "poles"; electric fields act on all charges, stationary or moving, and lines start and end on charges.')],
    misc=[('Magnetic field lines start on the north pole and end on the south pole, like electric field lines.', 'Magnetic field lines form closed loops: outside a magnet they go N to S, inside S to N; there are no magnetic monopoles.'),
          ('A longer solenoid with the same turns and current has a stronger field.', 'B = μ₀NI/L: spreading the same turns over a longer length reduces n and so reduces B.')],
    evaluate=[('Ørsted’s discovery that a current deflects a compass was a lucky accident.', ['it was reportedly observed during a lecture demonstration'], ['Ørsted had been searching for a link between electricity and magnetism, guided by natural philosophy', '"chance favours the prepared mind" – serendipity requires recognising significance (NOS)'], 'Partly serendipitous, but significant because Ørsted was looking for such a link and recognised its importance.')],
))


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def c3_bfield(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        I = rng.choice([2.0, 5.0, 8.0, 12.0, 20.0])
        r = rng.choice([0.5, 1.0, 2.0, 4.0, 10.0]) * 1e-2
        B = MU0 * I / (2 * math.pi * r)
        return num(f'A long straight wire carries a current of {sf(I, 2)} A. Calculate the magnetic flux density {sf(r * 100, 2)} cm from the wire. (B = μ₀I/2πr)',
                   q(B, 'T'), f'B = 4π × 10⁻⁷ × {sf(I, 2)}/(2π × {sf(r, 2)}) (M1) = {q(B, "T")} (A1).', 2)
    if frame == 1:
        N = rng.choice([200, 400, 500, 800, 1200])
        L = rng.choice([0.20, 0.25, 0.40, 0.50])
        I = rng.choice([0.50, 1.0, 1.5, 2.5])
        B = MU0 * N / L * I
        return num(f'A solenoid of length {sf(L, 2)} m has {N} turns and carries a current of {sf(I, 2)} A. Calculate the flux density inside it. (B = μ₀NI/L)',
                   q(B, 'T'), f'n = N/L = {sf(N / L)} m⁻¹ (A1); B = μ₀nI = {q(B, "T")} (A1).', 2)
    if frame == 2:
        I1, I2 = rng.choice([4, 6, 10]), rng.choice([2, 5, 8])
        d = rng.choice([0.04, 0.06, 0.10])
        same = rng.choice([True, False])
        B1 = MU0 * I1 / (2 * math.pi * d / 2)
        B2 = MU0 * I2 / (2 * math.pi * d / 2)
        net = abs(B1 - B2) if same else B1 + B2
        return num(f'Two long parallel wires {sf(d * 100, 2)} cm apart carry currents of {I1} A and {I2} A in {"the same direction" if same else "opposite directions"}. Determine the magnetic flux density at the point midway between them.',
                   q(net, 'T'), f'Each B = μ₀I/(2πr) with r = {sf(d / 2 * 100, 2)} cm: {q(B1, "T")} and {q(B2, "T")} (M1 A1); fields {"oppose" if same else "add"} at the midpoint (R1); B = {q(net, "T")} (A1).', 4, 'multi_step')
    BE = 2.0e-5
    r = rng.choice([2, 3, 5]) * 1e-2
    I = rng.choice([1.0, 2.0, 3.0, 5.0])
    Bw = MU0 * I / (2 * math.pi * r)
    ang = math.degrees(math.atan(Bw / BE))
    return num(f'A compass is placed {sf(r * 100, 2)} cm east of a long vertical wire carrying {sf(I, 2)} A. The horizontal component of Earth’s field is 2.0 × 10⁻⁵ T (north). Determine the angle through which the compass needle is deflected from north.',
               deg(ang), f'B_wire = μ₀I/2πr = {q(Bw, "T")} (M1 A1); wire field perpendicular to Earth’s field (R1); tan θ = B_wire/B_E → θ = {deg(ang)} (A1).', 4)


@R.add('ch05-st3', 'C3', (1, 4), 'mcq')
def c3_bfield_mcq(rng, slot):
    B0 = rng.choice([2.0, 4.0, 6.0, 8.0])
    a, b = rng.choice([(2, 2), (3, 1), (2, 4), (1, 3), (4, 2)])
    B1 = B0 * a / b
    return nmcq(rng, f'The flux density 5 cm from a long wire is {B0} mT. The current is multiplied by {a} and the distance by {b}. What is the new flux density?', B1,
                [B0 * a / b ** 2, B0 * a * b, B0 * b / a if b != a else B0 * 2], 'mT', f'B ∝ I/r: {B0} × {a}/{b} = {q(B1, "mT")}.', extra=True)


R.mcqs('ch05-st3', 'C2', (1, 4), [
    ('Looking along a wire with the current flowing away from you, the field lines circulate', 'clockwise', ['anticlockwise', 'radially outwards', 'parallel to the wire'], 'Right-hand grip rule.'),
    ('The field outside a long solenoid resembles the field of', 'a bar magnet', ['a straight wire', 'two parallel plates', 'a point charge'], 'Closed loops from N end to S end.'),
    ('The number of turns per metre of a solenoid is doubled and the current halved. The field inside', 'is unchanged', ['doubles', 'halves', 'quadruples'], 'B = μ₀nI.'),
])

linearise('ch05-st3', [
    ('B = μ₀I/(2πr) for the field of a long straight wire measured with a Hall probe at different distances r', 'B', '1/r', 'μ₀I/2π, from which μ₀ can be found', 'A straight line through the origin confirms B ∝ 1/r.'),
    ('B = μ₀nI for a solenoid as the current I is varied', 'B', 'I', 'μ₀n, from which μ₀ can be found', 'A non-zero intercept suggests a background field (e.g. Earth’s) or a probe zero error.'),
])


def _wire_spec(rng):
    I = rng.choice([3.0, 4.0, 5.0])
    rs = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    Bs = [round(MU0 * I / (2 * math.pi * r_ / 100) * 1e6 * rng.uniform(0.98, 1.02), 1) for r_ in rs]
    return dict(intro=f'A Hall probe measures the magnetic flux density B at distances r from a long straight wire carrying {I} A. Theory: B = μ₀I/(2πr).',
                xname='r', xunit='cm', yname='B', yunit='μT', xs=rs, ys=Bs, xfmt=lambda a: f'{a:.1f}', yfmt=lambda b: f'{b:.1f}',
                plot_x=lambda a: 100 / a, plot_y=lambda b: b * 1e-6, plot_label='B in T (y) against 1/r in m⁻¹ (x)', what='the permeability of free space μ₀', what_short='μ₀',
                gunit='T m', deduce=lambda m_, b_: (2 * math.pi * m_ / I, 'T m A⁻¹', f'μ₀ = 2π × gradient/I'))


gradient_fit('ch05-st3', _wire_spec)


R.facts('ch05-st4', F(
    terms=[('electric potential', 'the work done per unit positive charge in bringing a small test charge from infinity to a point, V = kQ/r'),
           ('electric potential energy', 'the work done in bringing a charge from infinity to a point in an electric field, Eₚ = kq₁q₂/r'),
           ('equipotential surface', 'a surface on which all points have the same electric potential'),
           ('electronvolt', 'the energy gained by an electron accelerated through a potential difference of 1 V, 1 eV = 1.60 × 10⁻¹⁹ J')],
    facts=[('The potential near a negative point charge is', 'negative', ['positive', 'zero', 'infinite everywhere'], 'V = kQ/r with Q < 0.'),
           ('The electric field strength is related to the potential by', 'E = −ΔV/Δr', ['E = ΔV × Δr', 'E = V/r²', 'E = −V/r'], 'Field is the negative potential gradient.'),
           ('An α particle (charge +2e) is accelerated through 5000 V. It gains', '10 keV of kinetic energy', ['5 keV', '2.5 keV', '20 keV'], 'ΔE = qV = 2e × 5000 V.'),
           ('Equipotentials around a point charge are', 'concentric spheres', ['parallel planes', 'radial lines', 'helices'], 'V depends only on r.')],
    why=[('Explain why no work is done when a charge moves along an equipotential surface.', 'W = qΔV and ΔV = 0 along an equipotential; equivalently, the force (along the field) is perpendicular to the motion.'),
         ('Explain why the electric potential energy of two like charges increases as they are pushed together.', 'Work must be done against the repulsive force to bring them closer; this work is stored as electric potential energy, Eₚ = kq₁q₂/r, which increases as r decreases.'),
         ('Explain why the electric potential is a scalar while the field is a vector, and why this makes potentials easier to combine.', 'Potential is work per unit charge (energy), which has no direction; potentials from several charges add algebraically, whereas fields must be added as vectors.')],
    contrast=[('electric potential', 'electric potential energy', 'Potential (V = J C⁻¹) is a property of a point, V = kQ/r; potential energy (J) belongs to a charge placed there, Eₚ = qV.')],
    misc=[('Where the electric field is zero the potential must also be zero.', 'Zero field means zero potential gradient, not zero potential: e.g. inside a charged conducting sphere E = 0 but V = kQ/R.'),
          ('Potential and field both fall as 1/r² around a point charge.', 'V = kQ/r falls as 1/r; E = kQ/r² falls as 1/r².')],
    evaluate=[('Gravitational and electric fields are fundamentally the same.', ['both inverse-square fields with similar potential formulae', 'field and potential concepts apply identically'], ['gravity is only attractive; electric forces attract and repel', 'there is no gravitational shielding', 'magnitudes differ by ~10³⁶', 'gravity is described by general relativity, electric fields by electromagnetism'], 'They share mathematical structure but differ in sign behaviour, strength and underlying theory, so "the same" overstates the analogy.')],
))


@R.add('ch05-st4', 'C3', (1, 5), 'numerical')
def c3_epot(rng, slot):
    frame = rng.randrange(5)
    if frame == 0:
        Q = rng.choice([1.5, 3.0, 5.0, 8.0]) * 1e-9 * rng.choice([1, -1])
        r = rng.choice([0.02, 0.05, 0.10, 0.30])
        V = K * Q / r
        return num(f'Calculate the electric potential {sf(r * 100, 2)} cm from a point charge of {sf(Q * 1e9, 2).replace("-", "−")} nC.',
                   esc(V, 'V'), f'V = kQ/r (M1) = {esc(V, "V")} (A1).', 2)
    if frame == 1:
        Z = 79
        Ek_MeV = rng.choice([4.0, 5.0, 5.5, 7.7])
        d = K * 2 * E * Z * E / (Ek_MeV * 1e6 * EV)
        return num(f'An α particle with kinetic energy {Ek_MeV} MeV travels directly towards a gold nucleus (Z = 79). Calculate its distance of closest approach.',
                   q(d, 'm'), f'Eₖ = k(2e)(79e)/d (M1); Eₖ = {sf(Ek_MeV * 1e6 * EV)} J (A1); d = {q(d, "m")} (A1).', 3)
    if frame == 2:
        V = rng.choice([50, 200, 500, 1200, 2000, 5000])
        part = pick(rng, [('an electron', E, ME), ('a proton', E, MP)])
        v = math.sqrt(2 * part[1] * V / part[2])
        return num(f'{part[0][0].upper() + part[0][1:]} is accelerated from rest through a potential difference of {V} V. Calculate the energy gained in eV and in J, and its final speed.',
                   f'{V} eV = {q(E * V, "J")}; v = {q(v, "m s⁻¹")}', f'ΔEₖ = qV = {V} eV (A1) = {q(E * V, "J")} (A1); v = √(2qV/m) = {q(v, "m s⁻¹")} (A1).', 3)
    if frame == 3:
        q1, q2 = rng.choice([2, 3, 4]) * 1e-6, rng.choice([1, 2, 5]) * 1e-6
        r1, r2 = rng.choice([0.30, 0.50]), rng.choice([0.05, 0.10])
        W = K * q1 * q2 * (1 / r2 - 1 / r1)
        return num(f'A +{sf(q2 * 1e6, 2)} μC charge is moved from {sf(r1 * 100, 2)} cm to {sf(r2 * 100, 2)} cm from a fixed +{sf(q1 * 1e6, 2)} μC charge. Calculate the work done on it.',
                   q(W, 'J'), f'W = ΔEₚ = kq₁q₂(1/r₂ − 1/r₁) (M1) = {q(W, "J")} (A1).', 2)
    V1, V2 = rng.choice([100, 150, 200]), rng.choice([20, 40, 60])
    dx = rng.choice([1.0, 2.0, 4.0]) * 1e-2
    Ef = (V1 - V2) / dx
    return num(f'Two equipotential surfaces at {V1} V and {V2} V are {sf(dx * 100, 2)} cm apart in a uniform field. Calculate the field strength and the work done on an electron moving from the {V2} V surface to the {V1} V surface.',
               f'E = {q(Ef, "V m⁻¹")}; W = {esc(-E * (V1 - V2), "J")} (the field does +{q(E * (V1 - V2), "J")} of work on the electron)',
               f'E = ΔV/Δx = {q(Ef, "V m⁻¹")} (M1 A1); work done by an external agent = qΔV = (−e)({V1 - V2} V) = {esc(-E * (V1 - V2), "J")}: the electron moves to higher potential and loses potential energy (A1).', 3)


@R.add('ch05-st4', 'C3', (1, 4), 'mcq')
def c3_epot_mcq(rng, slot):
    V = rng.choice([100, 250, 500, 1000, 2000])
    charge = rng.choice([1, 2])
    Ek = charge * V * E
    return nmcq(rng, f'A particle of charge {"+e" if charge == 1 else "+2e"} is accelerated from rest through {V} V. What kinetic energy does it gain?', Ek,
                [V * E / charge if charge == 2 else V * E * 4, Ek * 1e3, V / E * 1e-38 if False else Ek / 2 if charge == 1 else Ek * 2], 'J', f'Eₖ = qV = {charge} × 1.60 × 10⁻¹⁹ × {V} = {q(Ek, "J")}.', extra=True)


R.mcqs('ch05-st4', 'C2', (1, 4), [
    ('The potential at a distance r from a point charge is V. At 3r it is', 'V/3', ['V/9', '3V', 'V'], 'V ∝ 1/r.'),
    ('At the midpoint between charges +Q and −Q, which is correct?', 'the potential is zero but the field is not', ['the field is zero but the potential is not', 'both are zero', 'neither is zero, and both are maximal'], 'Potentials cancel (scalars); fields add (both point to −Q).'),
    ('An electron moves from a point at 0 V to a point at +100 V. Its electric potential energy', 'decreases by 100 eV', ['increases by 100 eV', 'is unchanged', 'decreases by 100 J'], 'ΔEₚ = qΔV = (−e)(+100 V).'),
])

R.static('ch05-st4', 'C4', (3, 5), [
    ('Compare and contrast the gravitational potential around Earth with the electric potential around an isolated positive point charge, referring to formulae, sign, the shape of equipotentials and the work done in moving a test object to infinity.',
     'Both: potential ∝ 1/r with zero at infinity, spherical equipotentials, field = −potential gradient. Gravitational V = −GM/r is negative everywhere (attractive), work must be done ON a mass to take it to infinity. Electric V = +kQ/r is positive for a positive source; a positive test charge is repelled, so the field does work on it as it moves to infinity (energy released).',
     'Correct formulae (A1); 1/r dependence and spherical equipotentials common (R1); sign difference linked to attraction/repulsion (R1); work to infinity compared (R1); field as negative gradient in both (A1).'),
], type='multi_step', marks=5)


# =============================================================================================
# ch06 D.3 Motion in electromagnetic fields
# =============================================================================================
PARTICLES = [('an electron', E, ME, '−'), ('a proton', E, MP, '+'), ('an α particle', 2 * E, 6.64e-27, '+'), ('a deuteron', E, 3.34e-27, '+')]

R.facts('ch06-st1', F(
    terms=[('uniform electric field (motion in)', 'a region where a charged particle experiences a constant force qE and so a constant acceleration qE/m'),
           ('electron gun', 'a device that produces a beam of electrons by thermionic emission from a hot cathode and accelerates them through a potential difference'),
           ('deflecting plates', 'a pair of parallel plates with a p.d. between them that deflects a beam of charged particles passing between them')],
    facts=[('An electron enters a uniform electric field at right angles to the field lines. Its path inside the field is', 'a parabola', ['a circle', 'a straight line', 'a helix'], 'Constant acceleration perpendicular to the initial velocity, like a projectile.'),
           ('A proton and an electron enter the same uniform electric field. Which is correct?', 'they experience equal and opposite forces, but the electron accelerates much more', ['they accelerate equally', 'the proton accelerates more', 'they experience no force'], 'F = eE for both; a = F/m.'),
           ('The kinetic energy gained by a charge q accelerated through a p.d. V is', 'qV', ['qV²', 'q/V', '½qV'], 'Work done by the field = qV.')],
    why=[('Explain why the horizontal velocity of an electron passing between horizontal deflecting plates is unchanged.', 'The electric force is vertical (perpendicular to the plates); there is no horizontal component of force, so the horizontal velocity component is constant.'),
         ('Explain why gravitational effects can be neglected for electrons in a cathode-ray tube.', 'The electric force eE (~10⁻¹⁵ N for E ~10⁴ V m⁻¹) is about 10¹⁴ times larger than the weight mₑg (~9 × 10⁻³⁰ N).'),
         ('Explain why the speed gained by a charged particle accelerated from rest depends only on the p.d. and not on the plate separation.', 'The work done by the field is qV regardless of the distance; a larger separation gives a smaller field but over a longer distance, so qEd = qV is unchanged.')],
    contrast=[('motion in a uniform electric field', 'motion in a uniform gravitational field', 'Both give constant acceleration and parabolic paths for perpendicular entry; in an electric field a = qE/m depends on the charge-to-mass ratio and may be in either direction, whereas in a gravitational field a = g for all masses.')],
    misc=[('An electron moves in the direction of the electric field lines.', 'The force on an electron is opposite to the field direction.'),
          ('An electron between deflecting plates follows a circular arc.', 'A constant force perpendicular to the plates gives a parabolic path; circular paths occur in magnetic fields.')],
    evaluate=[('Thomson’s cathode-ray experiments discovered the electron.', ['he measured e/m and showed it was the same for all cathode materials', 'his interpretation as a universal particle was new'], ['many others (Crookes, Schuster, Kaufmann) worked on cathode rays', 'the charge was later measured by Millikan', 'discovery is a process involving a community (NOS)'], 'Thomson is credited because he interpreted measurements as evidence for a universal sub-atomic particle, but discovery built on earlier and later work.')],
))


@R.add('ch06-st1', 'C3', (1, 5), 'numerical')
def c3_e_motion(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        pn, qq, m_, s = pick(rng, PARTICLES)
        V = rng.choice([100, 400, 1000, 2500, 5000])
        v = math.sqrt(2 * qq * V / m_)
        return num(f'{pn[0].upper() + pn[1:]} is accelerated from rest through a p.d. of {V} V. Calculate its final speed.',
                   q(v, 'm s⁻¹'), f'qV = ½mv² (M1); v = √(2qV/m) = {q(v, "m s⁻¹")} (A1).', 2)
    if frame == 1:
        Ef = rng.choice([2.0, 5.0, 8.0, 12.0]) * 1e3
        pn, qq, m_, s = pick(rng, PARTICLES)
        a = qq * Ef / m_
        return num(f'Calculate the acceleration of {pn} in a uniform electric field of strength {q(Ef, "N C⁻¹")}.', q(a, 'm s⁻²'),
                   f'a = qE/m (M1) = {q(a, "m s⁻²")} (A1).', 2)
    v0 = rng.choice([1.5, 2.0, 2.5, 3.0]) * 1e7
    V = rng.choice([50, 80, 120, 200])
    d = rng.choice([1.0, 1.5, 2.0]) * 1e-2
    L = rng.choice([4.0, 5.0, 6.0]) * 1e-2
    a = E * V / d / ME
    t = L / v0
    y = 0.5 * a * t * t
    if y > d / 2:
        return None
    if frame == 2:
        return num(f'An electron travelling at {q(v0, "m s⁻¹")} enters midway between two horizontal plates {sf(L * 100, 2)} cm long and {sf(d * 100, 2)} cm apart, with a p.d. of {V} V across them. Calculate the vertical deflection of the electron as it leaves the plates.',
                   q(y * 1e3, 'mm'), f'E = V/d = {q(V / d, "V m⁻¹")}; a = eE/mₑ = {q(a, "m s⁻²")} (M1); t = L/v = {q(t, "s")} (M1); y = ½at² = {q(y * 1e3, "mm")} (A1).', 3)
    vy = a * t
    ang = math.degrees(math.atan(vy / v0))
    return num(f'An electron beam with speed {q(v0, "m s⁻¹")} passes between deflecting plates {sf(L * 100, 2)} cm long, {sf(d * 100, 2)} cm apart, with {V} V across them. Determine the angle through which the beam is deflected.',
               deg(ang), f'a = eV/(mₑd) = {q(a, "m s⁻²")} (M1); v_y = at = {q(vy, "m s⁻¹")} (M1); tan θ = v_y/v_x → θ = {deg(ang)} (A1).', 3)


@R.add('ch06-st1', 'C3', (1, 4), 'mcq')
def c3_e_motion_mcq(rng, slot):
    V = rng.choice([100, 200, 500, 1000])
    v = math.sqrt(2 * E * V / ME)
    return nmcq(rng, f'An electron is accelerated from rest through {V} V. What is its final speed?', v,
                [math.sqrt(E * V / ME), 2 * E * V / ME / 1e7, math.sqrt(2 * E * V / MP)], 'm s⁻¹', f'v = √(2eV/mₑ) = {q(v, "m s⁻¹")}.', extra=False)


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step')
def c4_crt(rng, slot):
    Va = rng.choice([1000, 1500, 2000, 3000])
    v0 = math.sqrt(2 * E * Va / ME)
    V = rng.choice([40, 60, 100])
    d, L, D = 1.0e-2, rng.choice([3.0, 4.0]) * 1e-2, rng.choice([0.15, 0.20, 0.25])
    a = E * V / d / ME
    t = L / v0
    y1 = 0.5 * a * t * t
    vy = a * t
    Y = y1 + vy * (D / v0)
    return num(f'In an oscilloscope tube, electrons are accelerated through {Va} V, then pass between deflecting plates {sf(L * 100, 2)} cm long and 1.0 cm apart with {V} V across them. The screen is {sf(D * 100, 2)} cm beyond the end of the plates. (a) Calculate the speed of the electrons entering the plates. (b) Calculate the deflection at the exit of the plates. (c) Determine the total deflection on the screen. (d) Explain why doubling the accelerating voltage halves the deflection.',
               f'(a) {q(v0, "m s⁻¹")}; (b) {q(y1 * 1e3, "mm")}; (c) {q(Y * 1e3, "mm")}; (d) y ∝ 1/v² ∝ 1/V_a',
               f'(a) v = √(2eV/m) = {q(v0, "m s⁻¹")} (A1). (b) a = {q(a, "m s⁻²")}, t = {q(t, "s")} (M1), y = ½at² = {q(y1 * 1e3, "mm")} (A1). (c) straight line after plates: extra v_y·D/v (M1); total {q(Y * 1e3, "mm")} (A1). (d) deflection ∝ 1/v² and v² ∝ V_a (R1).', 6, 'multi_step', 'G5')


R.mcqs('ch06-st1', 'C2', (1, 4), [
    ('A proton and an α particle are accelerated from rest through the same p.d. The ratio of their kinetic energies Eₚ/E_α is', '1/2', ['2', '1', '1/4'], 'Eₖ = qV and q_α = 2e.'),
    ('An electron enters a uniform electric field travelling along the field direction. It will', 'slow down, stop and then accelerate back', ['speed up', 'move in a circle', 'be deflected sideways'], 'Force opposite to field and velocity.'),
    ('The deflection of an electron beam between deflecting plates is doubled by', 'doubling the deflecting p.d.', ['doubling the electron speed', 'doubling the plate separation', 'halving the plate length'], 'y = eVL²/(2mdv²) ∝ V.'),
])


R.facts('ch06-st2', F(
    terms=[('magnetic force on a moving charge', 'the force F = qvB sin θ on a charge q moving with velocity v at angle θ to a magnetic field B, perpendicular to both v and B'),
           ('cyclotron (gyro) frequency', 'the frequency f = qB/(2πm) at which a charged particle circles in a uniform magnetic field, independent of its speed'),
           ('velocity selector', 'crossed electric and magnetic fields that allow only particles with speed v = E/B to pass undeflected'),
           ('mass spectrometer', 'an instrument that separates ions by their mass-to-charge ratio using the radius of their circular paths in a magnetic field')],
    facts=[('A charged particle moves parallel to a uniform magnetic field. The magnetic force on it is', 'zero', ['qvB', 'maximum', 'along the field'], 'sin 0° = 0.'),
           ('Why does the magnetic force do no work on a moving charge?', 'it is always perpendicular to the velocity', ['it is too small', 'the charge is moving too fast', 'magnetic fields store no energy'], 'W = Fs cos 90° = 0, so speed is constant.'),
           ('The radius of the circular path of a charged particle in a magnetic field is', 'r = mv/(qB)', ['r = qB/(mv)', 'r = mvB/q', 'r = qv/(mB)'], 'qvB = mv²/r.'),
           ('A particle moving at an angle to a uniform field (not 0° or 90°) follows', 'a helical path', ['a circle', 'a parabola', 'a straight line'], 'Parallel component unaffected; perpendicular component circular.')],
    why=[('Explain why a charged particle moving perpendicular to a uniform magnetic field moves in a circle.', 'The magnetic force qvB is always perpendicular to the velocity, so it changes the direction but not the speed; a force of constant magnitude always perpendicular to the velocity provides a centripetal force, giving uniform circular motion.'),
         ('Explain why the period of a charged particle in a uniform magnetic field does not depend on its speed.', 'r = mv/(qB), so a faster particle moves in a proportionally larger circle; T = 2πr/v = 2πm/(qB) is independent of v – the principle of the cyclotron.'),
         ('Explain how crossed electric and magnetic fields select particles of one speed.', 'The electric force qE and magnetic force qvB act in opposite directions; they balance only when v = E/B, so only particles of that speed pass undeflected; faster particles are deflected by the magnetic force, slower by the electric force.'),
         ('Explain why charged particles from the solar wind cause aurorae mainly near the poles.', 'Particles spiral along Earth’s magnetic field lines (helical motion), which converge towards the magnetic poles and enter the atmosphere there, exciting gas atoms.')],
    contrast=[('the force on a charge in an electric field', 'the force on a charge in a magnetic field', 'An electric force qE acts on any charge, moving or not, along the field, and can change speed; a magnetic force qvB sin θ acts only on moving charges, perpendicular to v and B, and changes only direction.')],
    misc=[('A magnetic field can be used to speed up an electron beam.', 'The magnetic force is perpendicular to the velocity and does no work, so it cannot change the speed; an electric field is needed.'),
          ('A stationary electron in a magnetic field experiences a force along the field lines.', 'A stationary charge experiences no magnetic force (v = 0).'),
          ('Doubling the speed of a proton in a magnetic field doubles its period.', 'T = 2πm/(qB) is independent of speed; the radius doubles instead.')],
    evaluate=[('Mass spectrometry is the most reliable way to identify isotopes.', ['separates ions by m/q with high precision', 'needs only tiny samples'], ['ions of the same m/q (e.g. different molecules) can overlap', 'requires ionisation and vacuum', 'nuclear methods give different information (e.g. decay)'], 'Very powerful and widely used, but results need careful interpretation; overlaps mean it is best combined with other techniques.')],
))


@R.add('ch06-st2', 'C3', (1, 5), 'numerical')
def c3_b_motion(rng, slot):
    pn, qq, m_, s = pick(rng, PARTICLES)
    frame = rng.randrange(5)
    B = rng.choice([0.020, 0.050, 0.10, 0.25, 0.50, 1.2])
    v = rng.choice([2.0e5, 5.0e5, 1.0e6, 3.0e6, 1.5e7]) if pn != 'an electron' else rng.choice([1.0e6, 5.0e6, 2.0e7])
    if pn == 'an electron':
        B = rng.choice([1.0e-3, 2.5e-3, 5.0e-3, 1.0e-2])
    r = m_ * v / (qq * B)
    if frame == 0:
        return num(f'{pn[0].upper() + pn[1:]} moves at {q(v, "m s⁻¹")} perpendicular to a uniform magnetic field of {q(B, "T")}. Calculate the magnetic force on it and the radius of its path.',
                   f'F = {q(qq * v * B, "N")}; r = {q(r, "m")}', f'F = qvB = {q(qq * v * B, "N")} (A1); qvB = mv²/r (M1); r = mv/qB = {q(r, "m")} (A1).', 3)
    if frame == 1:
        T_ = 2 * math.pi * m_ / (qq * B)
        return num(f'Calculate the period and frequency of the circular motion of {pn} in a uniform magnetic field of {q(B, "T")}.',
                   f'T = {q(T_, "s")}; f = {q(1 / T_, "Hz")}', f'T = 2πm/(qB) (M1) = {q(T_, "s")} (A1); f = {q(1 / T_, "Hz")} (A1).', 3)
    if frame == 2:
        Ef = v * B
        return num(f'In a velocity selector the magnetic flux density is {q(B, "T")}. Calculate the electric field strength needed for {pn.split()[-1]}s travelling at {q(v, "m s⁻¹")} to pass undeflected, and explain why the result does not depend on the charge.',
                   f'E = {q(Ef, "V m⁻¹")}', f'qE = qvB (M1); E = vB = {q(Ef, "V m⁻¹")} (A1); q cancels, so selection depends only on speed (R1).', 3)
    if frame == 3:
        V = rng.choice([500, 1000, 2000, 4000])
        vv = math.sqrt(2 * qq * V / m_)
        rr = m_ * vv / (qq * B)
        return num(f'{pn[0].upper() + pn[1:]} is accelerated from rest through {V} V and then enters a uniform magnetic field of {q(B, "T")} at right angles. Determine the radius of its circular path.',
                   q(rr, 'm'), f'v = √(2qV/m) = {q(vv, "m s⁻¹")} (M1 A1); r = mv/(qB) = {q(rr, "m")} (A1).', 3)
    m1, m2 = 20 * U, 22 * U
    vv = rng.choice([1.0e5, 2.0e5, 5.0e5])
    BB = rng.choice([0.10, 0.20, 0.40])
    r1, r2 = m1 * vv / (E * BB), m2 * vv / (E * BB)
    return num(f'Singly charged ions of neon-20 and neon-22, all moving at {q(vv, "m s⁻¹")}, enter a mass spectrometer field of {q(BB, "T")} and travel through semicircles. Determine the separation of the points where they land. (1 u = 1.661 × 10⁻²⁷ kg)',
               q(2 * (r2 - r1) * 1e3, 'mm'), f'r = mv/(qB) for each: {q(r1, "m")} and {q(r2, "m")} (M1 A1); separation = 2(r₂ − r₁) (M1) = {q(2 * (r2 - r1) * 1e3, "mm")} (A1).', 4, 'multi_step')


@R.add('ch06-st2', 'C3', (1, 4), 'mcq')
def c3_b_motion_mcq(rng, slot):
    v = rng.choice([1.0e6, 2.0e6, 4.0e6])
    B = rng.choice([0.10, 0.20, 0.50])
    r = MP * v / (E * B)
    return nmcq(rng, f'A proton moves at {q(v, "m s⁻¹")} perpendicular to a {B} T magnetic field. What is the radius of its path?', r,
                [ME * v / (E * B), E * B / (MP * v) * 1e-3, MP * v * B / E * 1e3 if MP * v * B / E * 1e3 != r else r * 4], 'm', f'r = mv/(qB) = {q(r, "m")}.', extra=True)


R.mcqs('ch06-st2', 'C2', (1, 4), [
    ('An electron and a proton enter the same magnetic field perpendicularly with the same speed. Which is correct?', 'they curve in opposite directions and the electron’s radius is much smaller', ['they curve the same way with equal radii', 'the proton’s radius is smaller', 'neither is deflected'], 'Opposite charges; r ∝ m.'),
    ('A charged particle circles in a magnetic field. If the field strength is doubled, the period', 'halves', ['doubles', 'is unchanged', 'quadruples'], 'T = 2πm/(qB).'),
    ('The magnetic force on a moving charge is greatest when the velocity is', 'perpendicular to the field', ['parallel to the field', 'at 45° to the field', 'zero'], 'F = qvB sin θ.'),
    ('A beam of positive ions passes undeflected through crossed E and B fields. Faster ions in the beam will be', 'deflected in the direction of the magnetic force', ['deflected in the direction of the electric force', 'undeflected', 'stopped'], 'For v > E/B, qvB > qE.'),
])

R.static('ch06-st2', 'C4', (3, 5), [
    ('A cyclotron accelerates protons between two D-shaped electrodes in a uniform magnetic field of 1.5 T; the D radius is 0.50 m. (a) Show that the frequency of the alternating voltage must be about 23 MHz. (b) Calculate the maximum kinetic energy of the protons in MeV. (c) Explain why this design fails for electrons accelerated to similar energies.',
     '(a) f = qB/(2πm) = 1.60 × 10⁻¹⁹ × 1.5/(2π × 1.673 × 10⁻²⁷) = 2.3 × 10⁷ Hz; (b) v = qBR/m = 7.2 × 10⁷ m s⁻¹; Eₖ = ½mv² = 4.3 × 10⁻¹² J = 27 MeV; (c) electrons become relativistic at much lower energies, their mass effectively increases, so the frequency changes and they fall out of step.',
     'f = qB/2πm (M1) value (A1); v_max = qBR/m (M1); Eₖ ≈ 27 MeV (A1); relativistic argument (R1).'),
], type='multi_step', marks=5)


R.facts('ch06-st3', F(
    terms=[('force on a current-carrying conductor', 'the force F = BIL sin θ on a length L of wire carrying current I at angle θ to a magnetic field B'),
           ("Fleming's left-hand rule", 'a rule giving the direction of the force on a current in a magnetic field: First finger = Field, seCond finger = Current, thuMb = Motion (force)'),
           ('force between parallel wires', 'the force per unit length F/L = μ₀I₁I₂/(2πr) between two long parallel wires; attractive for currents in the same direction')],
    facts=[('Two long parallel wires carry currents in the same direction. They', 'attract each other', ['repel each other', 'exert no force', 'rotate'], 'Like currents attract.'),
           ('The force on a wire in a magnetic field is zero when the wire is', 'parallel to the field', ['perpendicular to the field', 'at 45° to the field', 'carrying a large current'], 'sin 0° = 0.'),
           ('Since 2019 the ampere is defined by', 'fixing the numerical value of the elementary charge e', ['the force between parallel wires', 'the mass of the international prototype kilogram', 'the speed of sound'], 'SI redefinition: 1 A = flow of 1/(1.602176634 × 10⁻¹⁹) e per second.'),
           ('The SI unit of magnetic flux density, the tesla, is equivalent to', 'N A⁻¹ m⁻¹', ['N A m', 'A m N⁻¹', 'N m² A⁻¹'], 'B = F/(IL).')],
    why=[('Explain why two parallel wires carrying currents in opposite directions repel.', 'Each wire is in the magnetic field of the other; using the right-hand grip rule for one wire and Fleming’s left-hand rule for the other shows the force on each points away from the other wire (Newton’s third law pair).'),
         ('Explain how a current balance can be used to measure the flux density of a magnet.', 'A wire of known length carries a known current across the field; the force BIL is balanced by known weights (or measured on a top-pan balance), so B = F/(IL).'),
         ('Explain why the forces between two parallel wires are equal even if the currents are different.', 'The force on wire 2 is B₁I₂L = μ₀I₁I₂L/(2πr) and on wire 1 is B₂I₁L = the same expression; they form a Newton’s third law pair.')],
    contrast=[('the motor effect', 'electromagnetic induction', 'In the motor effect a current in a magnetic field produces a force (electrical → mechanical); in induction relative motion or changing flux produces an emf (mechanical → electrical).')],
    misc=[('A current-carrying wire in a magnetic field is pushed along the field lines.', 'The force is perpendicular to both the field and the current, as given by Fleming’s left-hand rule.'),
          ('If one wire carries twice the current of the other, it feels twice the force.', 'Both wires feel the same force μ₀I₁I₂L/(2πr), by Newton’s third law.')],
    evaluate=[('Redefining the ampere in terms of the elementary charge (2019) was an improvement over the parallel-wire definition.', ['the new definition is based on an invariant constant of nature', 'it can be realised by single-electron devices and links electrical units to quantum standards'], ['the old definition was conceptually simple and familiar', 'practical realisation of the new definition is technically demanding'], 'An improvement: tying units to fixed constants makes them universal and stable, although the old definition remains useful for teaching (NOS: measurement standards evolve).')],
))


@R.add('ch06-st3', 'C3', (1, 5), 'numerical')
def c3_bil(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        B = rng.choice([0.040, 0.080, 0.15, 0.25, 0.60])
        I = rng.choice([1.5, 2.0, 3.5, 5.0, 8.0])
        L = rng.choice([0.05, 0.08, 0.10, 0.20, 0.50])
        th = rng.choice([90, 90, 30, 45, 60])
        F_ = B * I * L * sind(th)
        return num(f'A straight wire of length {sf(L * 100, 2)} cm carries a current of {sf(I, 2)} A at {th}° to a uniform magnetic field of {sf(B, 2)} T. Calculate the force on the wire.',
                   q(F_, 'N'), f'F = BIL sin θ (M1) = {sf(B, 2)} × {sf(I, 2)} × {sf(L, 2)} × sin {th}° = {q(F_, "N")} (A1).', 2)
    if frame == 1:
        I1, I2 = rng.choice([5, 10, 15, 20]), rng.choice([3, 8, 12, 25])
        r = rng.choice([0.5, 1.0, 2.0, 5.0]) * 1e-2
        FL = MU0 * I1 * I2 / (2 * math.pi * r)
        same = rng.choice([True, False])
        return num(f'Two long parallel wires {sf(r * 100, 2)} cm apart carry {I1} A and {I2} A in {"the same direction" if same else "opposite directions"}. Calculate the force per unit length between them and state whether it is attractive or repulsive.',
                   f'{q(FL, "N m⁻¹")}, {"attractive" if same else "repulsive"}', f'F/L = μ₀I₁I₂/(2πr) (M1) = {q(FL, "N m⁻¹")} (A1); {"same direction → attract" if same else "opposite → repel"} (A1).', 3)
    if frame == 2:
        m_ = rng.choice([2.0, 5.0, 8.0, 12.0]) * 1e-3
        L = rng.choice([0.05, 0.10, 0.20])
        B = rng.choice([0.05, 0.10, 0.25])
        I = m_ * g0 / (B * L)
        return num(f'A horizontal rod of mass {sf(m_ * 1e3, 2)} g and length {sf(L * 100, 2)} cm lies at right angles to a horizontal magnetic field of {sf(B, 2)} T. Calculate the current needed for the magnetic force to support the rod’s weight.',
                   q(I, 'A'), f'BIL = mg (M1); I = mg/(BL) = {q(I, "A")} (A1).', 2)
    dm = rng.choice([0.50, 1.20, 2.40, 3.60]) * 1e-3
    I = rng.choice([2.0, 3.0, 4.0, 5.0])
    L = rng.choice([0.040, 0.050, 0.080])
    B = dm * g0 / (I * L)
    return num(f'A magnet sits on a top-pan balance with a fixed wire passing horizontally through its field. With {sf(I, 2)} A in the wire, the balance reading changes by {sf(dm * 1e3, 2)} g. The length of wire in the field is {sf(L * 100, 2)} cm. Determine the magnetic flux density.',
               q(B, 'T'), f'Force = Δm g = {q(dm * g0, "N")} (A1); B = F/(IL) (M1) = {q(B, "T")} (A1).', 3)


@R.add('ch06-st3', 'C3', (1, 4), 'mcq')
def c3_bil_mcq(rng, slot):
    B, I, L = rng.choice([0.1, 0.2, 0.5]), rng.choice([2, 4, 5]), rng.choice([0.1, 0.2, 0.3])
    th = rng.choice([30, 90])
    F_ = B * I * L * sind(th)
    return nmcq(rng, f'A wire {sf(L * 100, 2)} cm long carries {I} A at {th}° to a {B} T field. What is the force on it?', F_,
                [B * I * L * cosd(th) if th != 90 else B * I * L / 2, B * I * L * 100 * sind(th), B * I / L * sind(th)], 'N', f'F = BIL sin θ = {q(F_, "N")}.', extra=True)


R.mcqs('ch06-st3', 'C2', (1, 4), [
    ('In a simple d.c. motor, the turning effect on the coil is due to', 'forces on the sides of the coil that are perpendicular to the field', ['forces on the sides parallel to the field', 'induced currents in the magnet', 'the weight of the coil'], 'F = BIL on sides at right angles to B form a couple.'),
    ('The separation of two parallel current-carrying wires is halved. The force per unit length', 'doubles', ['halves', 'quadruples', 'is unchanged'], 'F/L ∝ 1/r.'),
    ('A vertical wire carries current upwards in a horizontal magnetic field pointing north. The force on the wire is towards the', 'west', ['east', 'north', 'south'], 'Fleming’s left-hand rule: field N, current up → force W.'),
])

R.static('ch06-st3', 'C4', (3, 5), [
    ('Design an experiment, using a top-pan balance, to verify that the force on a current-carrying wire is proportional to the current and to determine the flux density between the poles of a magnet. Include the variables, the graph and the main sources of uncertainty.',
     'Independent variable: current I (varied with a rheostat, measured with an ammeter); dependent: change in balance reading Δm; control: length of wire in the field, orientation (90°), magnet. Plot Δm g against I: a straight line through the origin confirms F ∝ I; gradient = BL, so B = gradient/L. Uncertainties: length of wire in the field (field not uniform at edges), heating of the wire changes resistance (current drift), balance resolution; reverse the current to cancel systematic offsets.',
     'Variables identified (A1); method of measuring force (A1); graph and gradient = BL (M1 A1); two valid uncertainty sources with improvements (R1 R1).', 6),
], type='multi_step', marks=6)

linearise('ch06-st3', [
    ('F = BIL for a wire in the field of a magnet on a top-pan balance as the current I is varied', 'F (= Δm g)', 'I', 'BL, so B = gradient/L', 'A line through the origin confirms F ∝ I.'),
    ('F/L = μ₀I²/(2πr) for two parallel wires carrying the same current I', 'F/L', 'I²', 'μ₀/(2πr)', 'A straight line through the origin confirms F ∝ I².'),
])


def _em_spec(rng):
    B = rng.choice([0.8, 1.0, 1.2, 1.5]) * 1e-3
    Vs = [150, 200, 250, 300, 350, 400]
    em = E / ME
    rs = [round(math.sqrt(2 * V_ / (em * B * B)) * 100 * rng.uniform(0.985, 1.015), 2) for V_ in Vs]
    return dict(intro=f'In a fine-beam tube, electrons accelerated through a p.d. V move in circles of radius r in a uniform magnetic field of {sf(B * 1e3, 2)} mT. Theory: r² = (2m/(eB²)) V.',
                xname='V', xunit='V', yname='r', yunit='cm', xs=Vs, ys=rs, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: a, plot_y=lambda b: (b / 100) ** 2, plot_label='r² in m² (y) against V (x)', what='the specific charge e/m of the electron', what_short='e/m',
                gunit='m² V⁻¹', deduce=lambda m_, b_: (2 / (m_ * B * B), 'C kg⁻¹', 'e/m = 2/(gradient × B²)'))


gradient_fit('ch06-st2', _em_spec)


def _defl_spec(rng):
    v0 = rng.choice([2.0, 2.5, 3.0]) * 1e7
    d, L = 0.010, 0.040
    Vs = [20, 40, 60, 80, 100, 120]
    ys = [round(0.5 * (E * V_ / (d * ME)) * (L / v0) ** 2 * 1e3 * rng.uniform(0.97, 1.03), 2) for V_ in Vs]
    return dict(intro=f'An electron beam of speed v passes between plates 4.0 cm long and 1.0 cm apart. The vertical deflection y at the exit is measured for different deflecting voltages V. Theory: y = eL²V/(2mₑdv²).',
                xname='V', xunit='V', yname='y', yunit='mm', xs=Vs, ys=ys, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: a, plot_y=lambda b: b / 1000, plot_label='y in m (y) against V (x)', what='the speed v of the electrons', what_short='the electron speed',
                gunit='m V⁻¹', deduce=lambda m_, b_: (math.sqrt(E * L * L / (2 * ME * d * m_)), 'm s⁻¹', 'v = √(eL²/(2mₑd × gradient))'))


gradient_fit('ch06-st1', _defl_spec)


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def c2_e_motion_predict(rng, slot):
    ch = [('the deflecting voltage is doubled', 'the vertical deflection doubles', 'the acceleration eE/m doubles while the time between the plates is unchanged'),
          ('the electrons enter the plates at twice the speed', 'the deflection falls to a quarter', 'the time between the plates halves and y ∝ t²'),
          ('protons replace electrons at the same speed', 'the deflection is in the opposite direction and about 1800 times smaller', 'the force is reversed and a = eE/m is smaller by mₚ/mₑ'),
          ('the plate separation is doubled at the same voltage', 'the deflection halves', 'E = V/d halves, so the acceleration halves'),
          ('the plates are made twice as long', 'the deflection at the exit becomes four times larger', 'the time in the field doubles and y ∝ t²')]
    c, eff, why = pick(rng, ch)
    return dict(stem=f'An electron beam is deflected by a uniform electric field between parallel plates. Predict and explain how the deflection at the exit of the plates changes if {c}.',
                answer=f'{eff[0].upper() + eff[1:]}, because {why}.', type='explain', marks=2, markingKey=f'{eff} (A1); {why} (R1).')


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def c4_spectrometer(rng, slot):
    Ef = rng.choice([2.0, 4.0, 6.0]) * 1e4
    B1 = rng.choice([0.10, 0.20])
    v = Ef / B1
    B2 = rng.choice([0.25, 0.40, 0.50])
    iso = pick(rng, [('carbon-12', 12, 'carbon-13', 13), ('chlorine-35', 35, 'chlorine-37', 37), ('magnesium-24', 24, 'magnesium-26', 26)])
    m1, m2 = iso[1] * U, iso[3] * U
    r1, r2 = m1 * v / (E * B2), m2 * v / (E * B2)
    return num(f'In a Bainbridge mass spectrometer, singly charged ions first pass through a velocity selector with E = {q(Ef, "V m⁻¹")} and B = {sf(B1, 2)} T, then enter a region of uniform field {sf(B2, 2)} T where they travel in semicircles onto a detector. (a) Calculate the speed of the selected ions. (b) Calculate the radii of the paths of {iso[0]} and {iso[2]} ions. (c) Determine their separation on the detector. (d) Explain why the velocity selector is essential.',
               f'(a) {q(v, "m s⁻¹")}; (b) {q(r1, "m")} and {q(r2, "m")}; (c) {q(2 * (r2 - r1) * 1e3, "mm")}; (d) r depends on v as well as m, so only with one speed is r ∝ m',
               f'(a) v = E/B (M1) = {q(v, "m s⁻¹")} (A1). (b) r = mv/(qB) (M1); {q(r1, "m")}, {q(r2, "m")} (A1). (c) Δ = 2(r₂ − r₁) = {q(2 * (r2 - r1) * 1e3, "mm")} (A1). (d) same v makes r ∝ m/q (R1).', 6, 'multi_step', 'G5')


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def c4_helix(rng, slot):
    v = rng.choice([2.0, 4.0, 5.0]) * 1e6
    th = rng.choice([20, 30, 45, 60])
    B = rng.choice([1.0, 2.0, 5.0]) * 1e-3
    vp, vl = v * sind(th), v * cosd(th)
    r = ME * vp / (E * B)
    T_ = 2 * math.pi * ME / (E * B)
    pitch = vl * T_
    return num(f'An electron moving at {q(v, "m s⁻¹")} enters a uniform magnetic field of {q(B, "T")} with its velocity at {th}° to the field lines. (a) Explain why its path is a helix. (b) Calculate the radius of the helix. (c) Calculate the distance it travels along the field in one revolution (the pitch).',
               f'(b) {q(r, "m")}; (c) {q(pitch, "m")}',
               f'(a) component parallel to B (v cos θ) is unaffected; perpendicular component (v sin θ) gives circular motion (R1 R1). (b) r = mv sin θ/(eB) (M1) = {q(r, "m")} (A1). (c) T = 2πm/(eB) = {q(T_, "s")}; pitch = v cos θ × T (M1) = {q(pitch, "m")} (A1).', 6, 'multi_step', 'G5')


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def c4_current_balance(rng, slot):
    I = rng.choice([5.0, 10.0, 20.0])
    r = rng.choice([2.0, 5.0, 10.0]) * 1e-3
    L = rng.choice([0.50, 1.00])
    FL = MU0 * I * I / (2 * math.pi * r)
    mass = FL * L / g0
    return num(f'Two long parallel wires each carrying {sf(I, 2)} A are {sf(r * 1e3, 2)} mm apart; the currents are in the same direction. (a) Calculate the magnetic flux density at one wire due to the other. (b) Determine the force on a {sf(L * 100, 2)} cm length of either wire and its direction. (c) A student claims the force would be detectable on a balance reading to 0.01 g. Evaluate this claim. (d) Explain how the forces illustrate Newton’s third law.',
               f'(a) {q(MU0 * I / (2 * math.pi * r), "T")}; (b) {q(FL * L, "N")}, attractive; (c) equivalent mass {q(mass * 1e3, "g")}, {"detectable" if mass * 1e3 > 0.01 else "not detectable"}; (d) equal and opposite forces on the two wires',
               f'(a) B = μ₀I/(2πr) (M1) = {q(MU0 * I / (2 * math.pi * r), "T")} (A1). (b) F = BIL = {q(FL * L, "N")} (A1), wires attract (A1). (c) F/g = {q(mass * 1e3, "g")} compared with 0.01 g (R1). (d) each wire is in the other’s field; forces equal, opposite, same type (R1).', 6, 'multi_step', 'G5')


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def c4_motor_coil(rng, slot):
    N = rng.choice([50, 100, 200])
    B = rng.choice([0.10, 0.20, 0.35])
    I = rng.choice([0.5, 1.0, 2.0])
    a, b = rng.choice([0.04, 0.05]), rng.choice([0.03, 0.06])
    F_ = N * B * I * a
    tq = F_ * b
    return num(f'A rectangular coil of {N} turns, with sides {sf(a * 100, 2)} cm (perpendicular to the field) and {sf(b * 100, 2)} cm, carries {sf(I, 2)} A in a uniform field of {sf(B, 2)} T. The plane of the coil is parallel to the field. (a) Calculate the force on each {sf(a * 100, 2)} cm side. (b) Calculate the maximum torque on the coil. (c) Explain why the torque falls to zero when the plane of the coil is perpendicular to the field, and why a commutator is needed.',
               f'(a) {q(F_, "N")}; (b) {q(tq, "N m")}; (c) forces then act along the same line (no moment); the commutator reverses the current every half turn to keep rotation in one direction',
               f'(a) F = NBIL (M1) = {q(F_, "N")} (A1). (b) torque = F × {sf(b * 100, 2)} cm = {q(tq, "N m")} (M1 A1). (c) forces collinear/perpendicular distance zero (R1); current reversal maintains rotation (R1).', 6, 'multi_step', 'G5')


R.static('ch06-st1', 'C4', (3, 5), [
    ('In Millikan’s oil-drop experiment, a drop is first held stationary between plates 8.0 mm apart by a p.d. of 2400 V. When the field is switched off it falls at a constant (terminal) speed, from which its mass is found to be 4.9 × 10⁻¹⁵ kg. (a) Determine the charge on the drop. (b) Deduce how many electronic charges it carries. (c) Explain why Millikan’s results supported the idea that charge is quantised, and comment on the controversy over his data selection.',
     '(a) q = mgd/V = 4.9 × 10⁻¹⁵ × 9.81 × 8.0 × 10⁻³/2400 = 1.6 × 10⁻¹⁹ C; (b) 1 electronic charge; (c) all measured charges were integer multiples of 1.6 × 10⁻¹⁹ C; historians found that he excluded some drops from publication, raising questions about selective reporting (NOS: ethics of data).',
     'qV/d = mg (M1); q = 1.6 × 10⁻¹⁹ C (A1); n = q/e = 1 (A1); multiples of e (R1); data-selection issue discussed (R1).'),
    ('An electron is projected at 4.0 × 10⁶ m s⁻¹ along the direction of a uniform electric field of 500 V m⁻¹. (a) Determine how far it travels before coming momentarily to rest. (b) Determine the time taken. (c) Explain what happens next and how the answers change for a proton with the same initial speed.',
     '(a) a = eE/m = 8.78 × 10¹³ m s⁻²; s = v²/(2a) = 9.1 cm; (b) t = v/a = 4.6 × 10⁻⁸ s; (c) it accelerates back in the opposite direction; a proton is pushed forward along the field and speeds up instead (positive charge).',
     'a = eE/m (M1) (A1); s = v²/2a (M1) = 9.1 cm (A1); t = 4.6 × 10⁻⁸ s and direction/proton comment (R1).'),
], type='multi_step', marks=5)


# =============================================================================================
# ch07 D.4 Induction (HL)
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('magnetic flux', 'the product of the magnetic flux density and the area perpendicular to it, Φ = BA cos θ, measured in webers (Wb)'),
           ('flux linkage', 'the product of the number of turns of a coil and the flux through each turn, NΦ, measured in Wb (or Wb-turns)'),
           ('weber', 'the unit of magnetic flux; 1 Wb = 1 T m²')],
    facts=[('A coil of area A is in a uniform field B with its plane parallel to the field. The flux through it is', 'zero', ['BA', 'BA/2', 'NBA'], 'θ between B and the normal is 90°, cos 90° = 0.'),
           ('The flux through a loop is maximum when', 'the plane of the loop is perpendicular to the field', ['the plane is parallel to the field', 'the loop is at 45° to the field', 'the loop is moving'], 'Normal parallel to B gives cos 0° = 1.'),
           ('Which unit is equivalent to the weber?', 'T m²', ['T m⁻²', 'T A', 'N A⁻¹'], 'Φ = BA.'),
           ('A coil of 200 turns has 3.0 × 10⁻⁴ Wb through each turn. Its flux linkage is', '6.0 × 10⁻² Wb', ['3.0 × 10⁻⁴ Wb', '1.5 × 10⁻⁶ Wb', '6.0 × 10⁻⁴ Wb'], 'NΦ = 200 × 3.0 × 10⁻⁴.')],
    why=[('Explain why the angle in Φ = BA cos θ is measured between the field and the normal to the area.', 'Only the component of B perpendicular to the surface passes through it; this is B cos θ when θ is the angle between B and the normal.'),
         ('Explain why flux linkage, rather than flux, determines the emf induced in a coil.', 'Each turn has an emf −ΔΦ/Δt induced in it; the turns are in series so the emfs add, giving ε = −NΔΦ/Δt = −Δ(NΦ)/Δt.'),
         ('Explain why rotating a coil in a uniform field changes the flux through it even though B and the area are constant.', 'The angle between the field and the normal to the coil changes, so the effective (perpendicular) area A cos θ changes.')],
    contrast=[('magnetic flux', 'magnetic flux density', 'Flux density B (T) is the field strength at a point; flux Φ = BA cos θ (Wb) is the total "amount" of field passing through a given area.'),
              ('flux', 'flux linkage', 'Flux is through one loop (BA cos θ); flux linkage is flux multiplied by the number of turns (NΦ).')],
    misc=[('The flux through a coil is greatest when its plane is parallel to the field.', 'Flux is zero then; it is greatest when the plane is perpendicular to the field (normal parallel to B).'),
          ('Adding more turns increases the flux through a coil.', 'More turns increase the flux linkage NΦ; the flux through each turn is unchanged.')],
    evaluate=[('Faraday’s concept of field lines (flux) was essential to the development of electromagnetism.', ['flux gave an intuitive picture leading to the law of induction', 'Maxwell built his equations on Faraday’s field ideas'], ['the mathematics could in principle be developed without the picture', 'action-at-a-distance theories also predicted forces'], 'Faraday’s visual model was a crucial creative step that guided Maxwell, an example of models driving theory (NOS).')],
))


@R.add('ch07-st1', 'C3', (1, 5), 'numerical')
def c3_flux(rng, slot):
    frame = rng.randrange(4)
    B = rng.choice([0.020, 0.050, 0.12, 0.25, 0.40, 0.80])
    if frame == 0:
        a = rng.choice([2.0, 4.0, 5.0, 8.0, 10.0]) * 1e-2
        b_ = rng.choice([3.0, 5.0, 6.0]) * 1e-2
        th = rng.choice([0, 30, 45, 60])
        Phi = B * a * b_ * cosd(th)
        return num(f'A rectangular loop measuring {sf(a * 100, 2)} cm by {sf(b_ * 100, 2)} cm is placed in a uniform field of {sf(B, 2)} T, with the normal to the loop at {th}° to the field. Calculate the magnetic flux through the loop.',
                   q(Phi, 'Wb'), f'Φ = BA cos θ (M1) = {sf(B, 2)} × {sf(a * b_)} × cos {th}° = {q(Phi, "Wb")} (A1).', 2)
    if frame == 1:
        N = rng.choice([50, 100, 250, 500])
        r = rng.choice([1.0, 1.5, 2.0, 3.0]) * 1e-2
        A = math.pi * r * r
        return num(f'A circular coil of {N} turns and radius {sf(r * 100, 2)} cm is placed with its plane perpendicular to a field of {sf(B, 2)} T. Calculate the flux linkage.',
                   q(N * B * A, 'Wb'), f'A = πr² = {q(A, "m²")} (A1); NΦ = NBA = {q(N * B * A, "Wb")} (A1).', 2)
    if frame == 2:
        N = rng.choice([20, 40, 80])
        A = rng.choice([4.0, 6.0, 9.0]) * 1e-4
        th = rng.choice([30, 60, 90])
        d = N * B * A * (1 - cosd(th))
        return num(f'A {N}-turn coil of area {sf(A * 1e4, 2)} cm² starts with its plane perpendicular to a {sf(B, 2)} T field and is rotated through {th}°. Calculate the change in flux linkage.',
                   q(d, 'Wb'), f'Initial NBA = {q(N * B * A, "Wb")}; final NBA cos {th}° = {q(N * B * A * cosd(th), "Wb")} (M1); change = {q(d, "Wb")} (A1).', 2)
    n = rng.choice([500, 1000, 2000])
    I = rng.choice([0.5, 1.0, 2.0])
    Bs = MU0 * n * I
    Nc = rng.choice([10, 30, 50])
    Ac = rng.choice([2.0, 5.0]) * 1e-4
    return num(f'A long solenoid with {n} turns per metre carries {sf(I, 2)} A. A small coil of {Nc} turns and area {sf(Ac * 1e4, 2)} cm² is placed inside, coaxial with the solenoid. Determine the flux linkage of the small coil.',
               q(Nc * Bs * Ac, 'Wb'), f'B = μ₀nI = {q(Bs, "T")} (M1); NΦ = NBA = {q(Nc * Bs * Ac, "Wb")} (A1).', 2)


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3_flux_mcq(rng, slot):
    B = rng.choice([0.2, 0.4, 0.5])
    A = rng.choice([0.01, 0.02, 0.05])
    th = rng.choice([30, 60])
    Phi = B * A * cosd(th)
    return nmcq(rng, f'A loop of area {A} m² is in a uniform field of {B} T. The normal to the loop makes {th}° with the field. What is the flux through the loop?', Phi,
                [B * A * sind(th), B * A, B * A / cosd(th)], 'Wb', f'Φ = BA cos θ = {q(Phi, "Wb")}; using sin θ gives the value for the angle measured from the plane.', extra=False)


R.mcqs('ch07-st1', 'C2', (1, 4), [
    ('A coil’s flux linkage is doubled by', 'doubling the number of turns', ['halving the area', 'doubling the resistance', 'rotating it to be parallel to the field'], 'NΦ ∝ N.'),
    ('A loop in a uniform field is rotated from perpendicular to the field to parallel to it. The flux', 'decreases from BA to zero', ['increases from zero to BA', 'is unchanged', 'reverses'], 'cos θ goes from 1 to 0.'),
    ('A flat coil is moved without rotating within a uniform field. Its flux linkage', 'does not change', ['increases', 'decreases', 'oscillates'], 'B, A and θ are all unchanged.'),
])

R.static('ch07-st1', 'C4', (3, 5), [
    ('A square coil of side 5.0 cm and 100 turns is pulled at constant speed 0.20 m s⁻¹ through a region of uniform field 0.30 T that is 15 cm wide, with its plane perpendicular to the field. (a) Sketch the flux linkage against time from just before the coil enters until just after it leaves. (b) Calculate the maximum flux linkage. (c) Sketch and explain the corresponding emf–time graph.',
     '(a) flux linkage rises linearly for 0.25 s (entering), constant 0.075 Wb for 0.50 s (fully inside), falls linearly for 0.25 s; (b) NBA = 100 × 0.30 × 2.5 × 10⁻³ = 0.075 Wb; (c) emf = gradient = 0.30 V while entering, zero while fully inside, −0.30 V (opposite sign) while leaving.',
     'Correct shape with timings (A1 A1); NBA = 0.075 Wb (A1); emf = −d(NΦ)/dt = 0.30 V (M1); zero inside and reversed on exit (R1).', 6),
], type='multi_step', marks=6)


R.facts('ch07-st2', F(
    terms=[("Faraday's law", 'the induced emf in a circuit is equal to the rate of change of magnetic flux linkage, ε = −NΔΦ/Δt'),
           ("Lenz's law", 'the direction of an induced current is such that it opposes the change in flux that produces it'),
           ('electromagnetic induction', 'the production of an emf in a conductor when the magnetic flux linking it changes'),
           ('eddy currents', 'induced currents that circulate within a conductor when the flux through it changes')],
    facts=[('A magnet is pushed into a coil connected to a meter. Which change gives a larger induced emf?', 'pushing the magnet in faster', ['holding the magnet still inside the coil', 'using a coil with fewer turns', 'using a weaker magnet'], 'ε = rate of change of flux linkage.'),
           ('Lenz’s law is a consequence of conservation of', 'energy', ['charge', 'momentum', 'mass'], 'If the induced current aided the change, energy would be created.'),
           ('The minus sign in Faraday’s law ε = −NΔΦ/Δt represents', 'Lenz’s law', ['negative charge', 'energy loss', 'resistance'], 'The emf opposes the change.'),
           ('A magnet is held stationary inside a coil. The induced emf is', 'zero', ['maximum', 'equal to NBA', 'reversing direction'], 'No change of flux linkage.')],
    why=[('Explain, using Lenz’s law, why work must be done to push a magnet into a coil connected in a closed circuit.', 'The induced current makes the coil end facing the magnet a like pole, which repels the approaching magnet; work must be done against this force, and that work becomes the electrical energy dissipated in the circuit.'),
         ('Explain why a magnet falls more slowly through a copper tube than through a plastic tube.', 'As the magnet falls the flux through each section of copper changes, inducing eddy currents; by Lenz’s law their magnetic field opposes the motion, giving an upward force; plastic is an insulator so no currents flow.'),
         ('Explain why transformer cores are laminated.', 'The changing flux induces eddy currents in the core; thin insulated laminations increase the resistance of current paths, reducing eddy currents and the energy lost as heat.'),
         ('Explain why the induced emf is larger when a coil with more turns is used.', 'Each turn has the same rate of change of flux and so the same emf; the turns are in series, so the total emf is N times larger.')],
    contrast=[("Faraday's law", "Lenz's law", 'Faraday’s law gives the magnitude of the induced emf (rate of change of flux linkage); Lenz’s law gives its direction (opposing the change).')],
    misc=[('A strong magnet held still next to a coil induces a large current.', 'Induction requires a changing flux; a stationary magnet induces nothing, however strong.'),
          ('The induced current always flows in the direction that helps the magnet move.', 'By Lenz’s law it opposes the change; helping it would create energy from nothing.'),
          ('An emf is only induced if the circuit is complete.', 'An emf is induced whenever flux linkage changes; a complete circuit is needed only for a current to flow.')],
    evaluate=[('Eddy currents are always undesirable.', ['they cause energy loss in transformer cores and motors'], ['they are used in induction braking for trains and rollercoasters', 'induction hobs and metal detectors rely on them', 'electromagnetic damping of meters'], 'Undesirable in cores, but deliberately exploited in braking, heating and detection, so "always" is incorrect.')],
))


@R.add('ch07-st2', 'C3', (1, 5), 'numerical')
def c3_faraday(rng, slot):
    frame = rng.randrange(5)
    N = rng.choice([50, 100, 200, 400, 600])
    A = rng.choice([2.0, 4.0, 6.0, 10.0, 25.0]) * 1e-4
    if frame == 0:
        B1, B2 = rng.choice([0.0, 0.10, 0.20]), rng.choice([0.40, 0.50, 0.80])
        t = rng.choice([0.020, 0.050, 0.10, 0.25])
        emf = N * A * (B2 - B1) / t
        return num(f'The field through a {N}-turn coil of area {sf(A * 1e4, 2)} cm² increases uniformly from {sf(B1, 2)} T to {sf(B2, 2)} T in {sf(t * 1000, 2)} ms. The field is perpendicular to the coil. Calculate the magnitude of the induced emf.',
                   q(emf, 'V'), f'ε = NAΔB/Δt (M1) = {N} × {sf(A)} × {sf(B2 - B1, 2)}/{sf(t)} = {q(emf, "V")} (A1).', 2)
    if frame == 1:
        B = rng.choice([0.10, 0.25, 0.50])
        t = rng.choice([0.10, 0.20, 0.50])
        Rr = rng.choice([2.0, 5.0, 10.0, 20.0])
        emf = N * B * A / t
        return num(f'A {N}-turn coil of area {sf(A * 1e4, 2)} cm² and resistance {sf(Rr, 2)} Ω is pulled out of a {sf(B, 2)} T field (perpendicular to its plane) in {sf(t, 2)} s. Calculate the average induced emf, the average current and the total charge that flows.',
                   f'ε = {q(emf, "V")}; I = {q(emf / Rr, "A")}; Q = {q(emf / Rr * t, "C")}', f'ε = NBA/Δt = {q(emf, "V")} (M1 A1); I = ε/R = {q(emf / Rr, "A")} (A1); Q = IΔt = NBA/R = {q(emf / Rr * t, "C")} (A1).', 4, 'multi_step')
    if frame == 2:
        B = rng.choice([0.10, 0.20, 0.40])
        t = rng.choice([0.05, 0.10, 0.20])
        emf = 2 * N * B * A / t
        return num(f'A {N}-turn coil of area {sf(A * 1e4, 2)} cm² lies perpendicular to a {sf(B, 2)} T field. The coil is flipped through 180° in {sf(t, 2)} s. Calculate the average induced emf.',
                   q(emf, 'V'), f'Flux linkage changes from +NBA to −NBA: Δ(NΦ) = 2NBA (M1 A1); ε = 2NBA/Δt = {q(emf, "V")} (A1).', 3)
    if frame == 3:
        rate = rng.choice([0.020, 0.050, 0.10, 0.40])
        emf = N * A * rate
        return num(f'The magnetic field through a {N}-turn coil of cross-sectional area {sf(A * 1e4, 2)} cm² changes at a steady rate of {sf(rate, 2)} T s⁻¹. Calculate the induced emf.',
                   q(emf, 'V'), f'ε = NA dB/dt (M1) = {q(emf, "V")} (A1).', 2)
    pts = [(0, 0), (2, 6), (5, 6), (6, 0)]
    scale = rng.choice([1, 2, 3])
    Nn = rng.choice([10, 20, 50])
    e1 = Nn * 6 * scale * 1e-3 / 2e-3 / 1000
    e2 = Nn * 6 * scale * 1e-3 / 1e-3 / 1000
    return num(f'The flux through each turn of a {Nn}-turn coil rises linearly from 0 to {6 * scale} mWb in the first 2.0 ms, stays constant for 3.0 ms, then falls to zero in 1.0 ms. Calculate the induced emf in each stage.',
               f'{q(Nn * 6 * scale * 1e-3 / 2e-3, "V")}; 0; {q(Nn * 6 * scale * 1e-3 / 1e-3, "V")} in the opposite direction',
               f'ε = NΔΦ/Δt (M1): stage 1 = {Nn} × {6 * scale} × 10⁻³/2.0 × 10⁻³ = {q(Nn * 6 * scale * 1e-3 / 2e-3, "V")} (A1); stage 2 zero (A1); stage 3 = {q(Nn * 6 * scale * 1e-3 / 1e-3, "V")}, opposite sign (A1).', 4, 'multi_step')


@R.add('ch07-st2', 'C3', (1, 4), 'mcq')
def c3_faraday_mcq(rng, slot):
    N = rng.choice([100, 200, 500])
    dPhi = rng.choice([2.0, 4.0, 6.0]) * 1e-3
    t = rng.choice([0.1, 0.2, 0.5])
    emf = N * dPhi / t
    return nmcq(rng, f'The flux through each turn of a {N}-turn coil changes by {q(dPhi, "Wb")} in {t} s. What is the average induced emf?', emf,
                [dPhi / t, N * dPhi * t, N * dPhi / t ** 2], 'V', f'ε = NΔΦ/Δt = {q(emf, "V")}; forgetting N gives {q(dPhi / t, "V")}.', extra=False)


@R.add('ch07-st2', 'C2', (2, 4), 'explain')
def c2_lenz(rng, slot):
    sits = [('the north pole of a magnet is pushed towards the end of a coil', 'that end of the coil becomes a north pole, repelling the magnet'),
            ('the north pole of a magnet is pulled away from the end of a coil', 'that end of the coil becomes a south pole, attracting the retreating magnet'),
            ('the current in a nearby coil is switched on', 'the induced current flows in the opposite sense to the primary current, opposing the growth of flux'),
            ('the current in a nearby coil is switched off', 'the induced current flows in the same sense as the original current, opposing the decrease in flux'),
            ('an aluminium ring sits on an iron core and the current in a coil around the core is switched on', 'the induced current in the ring makes it repel the coil, so the ring jumps up (Thomson’s jumping ring)'),
            ('a metal plate swings as a pendulum between the poles of a magnet', 'eddy currents in the plate produce forces opposing its motion, so the swing is damped quickly')]
    s, a = pick(rng, sits)
    return dict(stem=f'Use Lenz’s law to explain the direction of the induced current or force when {s}.', answer=a[0].upper() + a[1:] + '.',
                type='explain', marks=3, markingKey=f'Changing flux identified (M1); induced effect opposes the change (R1); {a} (A1).')


R.mcqs('ch07-st2', 'C2', (1, 4), [
    ('A bar magnet is dropped through a coil connected to a data logger. Compared with the emf pulse as the magnet enters, the pulse as it leaves is', 'larger and of opposite sign', ['smaller and of the same sign', 'identical', 'zero'], 'The magnet is faster when leaving, and the flux change is reversed.'),
    ('The emf induced in a coil is 4.0 V. The number of turns is doubled and the rate of change of flux halved. The emf becomes', '4.0 V', ['8.0 V', '2.0 V', '16 V'], 'ε ∝ N × dΦ/dt.'),
    ('An induction hob heats a steel pan but not a glass pan because', 'the changing magnetic field induces eddy currents only in the conducting pan', ['glass reflects microwaves', 'steel has a higher melting point', 'glass is magnetic'], 'Eddy currents need a conductor.'),
])


def _faraday_spec(rng):
    N, A = rng.choice([200, 400]), rng.choice([3.0, 5.0]) * 1e-4
    rates = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    emfs = [round(N * A * r_ * 1e3 * rng.uniform(0.97, 1.03), 2) for r_ in rates]
    return dict(intro=f'A search coil of {N} turns is placed in a field that increases at a controlled rate dB/dt; the induced emf ε is measured. Theory: ε = NA dB/dt.',
                xname='dB/dt', xunit='T s⁻¹', yname='ε', yunit='mV', xs=rates, ys=emfs, xfmt=lambda a: f'{a:.2f}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: a, plot_y=lambda b: b / 1000, plot_label='ε in V (y) against dB/dt (x)', what='the cross-sectional area of the coil', what_short='the area',
                gunit='V s T⁻¹', deduce=lambda m_, b_: (m_ / N, 'm²', f'A = gradient/N'))


gradient_fit('ch07-st2', _faraday_spec)


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step')
def c4_falling_magnet(rng, slot):
    N = rng.choice([200, 500, 1000])
    dPhi = rng.choice([1.0, 2.0, 3.0]) * 1e-4
    h = rng.choice([0.20, 0.40, 0.60])
    v = math.sqrt(2 * g0 * h)
    L = rng.choice([0.02, 0.03])
    t = L / v
    emf = N * dPhi / t
    return num(f'A small magnet is dropped from rest {sf(h * 100, 2)} cm above a short coil of {N} turns. As it passes through, the flux through each turn changes by about {q(dPhi, "Wb")} over a distance of {sf(L * 100, 2)} cm. (a) Estimate the speed of the magnet at the coil. (b) Estimate the average induced emf as it enters. (c) Explain why the emf pulse on leaving is larger and reversed. (d) Explain, using energy, why the magnet arrives slightly slower if the coil is connected to a resistor.',
               f'(a) {q(v, "m s⁻¹")}; (b) {q(emf, "V")}; (c) faster on leaving and flux decreasing instead of increasing; (d) energy transferred to the circuit comes from the magnet’s kinetic energy (Lenz’s law)',
               f'(a) v = √(2gh) = {q(v, "m s⁻¹")} (A1). (b) Δt ≈ L/v = {q(t, "s")} (M1); ε = NΔΦ/Δt = {q(emf, "V")} (A1). (c) greater speed → shorter time; ΔΦ reversed (R1 R1). (d) induced current opposes motion; work done against it becomes thermal energy in R (R1).', 6, 'multi_step', 'G5')


R.facts('ch07-st3', F(
    terms=[('motional emf', 'the emf ε = BvL induced across a straight conductor of length L moving at speed v perpendicular to a magnetic field B'),
           ('alternating current (a.c.) generator', 'a device in which a coil rotates in a magnetic field, producing a sinusoidal emf ε = BANω sin ωt'),
           ('peak emf', 'the maximum value of a sinusoidal emf, ε₀ = BANω for a rotating coil'),
           ('root-mean-square (rms) value', 'the value of the steady (d.c.) voltage or current that would dissipate the same average power in a resistor, V_rms = V₀/√2 for a sine wave')],
    facts=[('The emf of an a.c. generator is maximum when the plane of the coil is', 'parallel to the magnetic field', ['perpendicular to the magnetic field', 'at 45° to the field', 'moving slowest'], 'Flux is then zero but changing fastest.'),
           ('The rotation frequency of a generator is doubled. The peak emf', 'doubles and the frequency doubles', ['doubles and the frequency is unchanged', 'is unchanged and the frequency doubles', 'quadruples'], 'ε₀ = BANω.'),
           ('The rms value of a sinusoidal voltage of peak 325 V is', '230 V', ['163 V', '460 V', '325 V'], 'V_rms = V₀/√2.'),
           ('A metal rod moves through a field parallel to the field lines. The emf across it is', 'zero', ['BvL', 'maximum', 'BvL/2'], 'No field lines are cut.')],
    why=[('Explain why the emf of a rotating coil is zero when the flux through it is a maximum.', 'The emf depends on the rate of change of flux; at the position of maximum flux (plane perpendicular to B) the flux–time graph is at a turning point, so its gradient – and the emf – is zero.'),
         ('Explain, in terms of the forces on free electrons, why an emf is induced across a rod moving through a magnetic field.', 'The free electrons move with the rod, so each experiences a magnetic force evB along the rod; electrons accumulate at one end until the resulting electric field balances the magnetic force (eE = evB), giving a potential difference BvL.'),
         ('Explain why a generator becomes harder to turn when more current is drawn from it.', 'The current in the coil experiences a force in the magnetic field (motor effect) which, by Lenz’s law, opposes the rotation; larger current means larger opposing torque, so more mechanical work is needed – conservation of energy.')],
    contrast=[('peak emf', 'rms emf', 'Peak emf ε₀ is the maximum instantaneous value; rms emf ε₀/√2 is the equivalent d.c. value for power calculations.'),
              ('a generator', 'a motor', 'A generator converts mechanical work into electrical energy by induction; a motor converts electrical energy into mechanical work by the motor effect; the same machine can do either.')],
    misc=[('A generator coil produces maximum emf when it is perpendicular to the magnetic field.', 'Maximum emf occurs when the plane of the coil is parallel to the field, where flux changes fastest.'),
          ('The mains supply of 230 V means the voltage never exceeds 230 V.', '230 V is the rms value; the peak voltage is 230√2 ≈ 325 V.')],
    evaluate=[('Generators violate conservation of energy because they produce electricity from magnets.', ['the magnet itself is not used up'], ['the energy comes from the mechanical work done to turn the coil', 'Lenz’s law opposition means work is needed whenever current flows', 'efficiency is always below 100 %'], 'No violation: electrical energy comes from the mechanical work done against the opposing magnetic force.')],
))


@R.add('ch07-st3', 'C3', (1, 5), 'numerical')
def c3_generator(rng, slot):
    frame = rng.randrange(5)
    if frame == 0:
        B = rng.choice([0.05, 0.10, 0.20, 0.50])
        v = rng.choice([2.0, 5.0, 8.0, 12.0])
        L = rng.choice([0.10, 0.20, 0.30, 0.50])
        return num(f'A metal rod of length {sf(L * 100, 2)} cm moves at {sf(v, 2)} m s⁻¹ perpendicular to a uniform magnetic field of {sf(B, 2)} T. Calculate the emf induced across the rod.',
                   q(B * v * L, 'V'), f'ε = BvL (M1) = {sf(B, 2)} × {sf(v, 2)} × {sf(L, 2)} = {q(B * v * L, "V")} (A1).', 2)
    if frame == 1:
        Bv = rng.choice([2.0, 3.5, 5.0]) * 1e-5
        span = rng.choice([30, 40, 60, 65])
        v = rng.choice([200, 230, 250])
        return num(f'An aircraft with a wingspan of {span} m flies horizontally at {v} m s⁻¹ where the vertical component of Earth’s field is {q(Bv, "T")}. Calculate the emf between the wingtips.',
                   q(Bv * v * span, 'V'), f'ε = BvL with the vertical component (M1) = {q(Bv * v * span, "V")} (A1).', 2)
    N = rng.choice([50, 100, 200, 500])
    A = rng.choice([4.0, 10.0, 20.0, 50.0]) * 1e-4
    B = rng.choice([0.10, 0.20, 0.40])
    f = rng.choice([10, 25, 50, 60])
    w = 2 * math.pi * f
    e0 = B * A * N * w
    if frame == 2:
        return num(f'A generator coil of {N} turns, each of area {sf(A * 1e4, 2)} cm², rotates at {f} revolutions per second in a uniform field of {sf(B, 2)} T. Calculate the peak and rms emf.',
                   f'ε₀ = {q(e0, "V")}; ε_rms = {q(e0 / math.sqrt(2), "V")}', f'ω = 2πf = {sf(w)} rad s⁻¹ (A1); ε₀ = BANω = {q(e0, "V")} (M1 A1); ε_rms = ε₀/√2 = {q(e0 / math.sqrt(2), "V")} (A1).', 4)
    if frame == 3:
        return num(f'A generator produces a peak emf of {sf(e0, 3)} V at {f} Hz. State the peak emf and frequency when the rotation rate is (a) doubled, (b) halved.',
                   f'(a) {q(2 * e0, "V")}, {2 * f} Hz; (b) {q(e0 / 2, "V")}, {f / 2:g} Hz', f'ε₀ ∝ ω and f is the rotation frequency (R1); (a) {q(2 * e0, "V")} and {2 * f} Hz (A1); (b) {q(e0 / 2, "V")} and {f / 2:g} Hz (A1).', 3)
    Rr = rng.choice([10, 20, 50, 100])
    P = (e0 / math.sqrt(2)) ** 2 / Rr
    return num(f'A generator with a peak emf of {sf(e0, 3)} V (negligible internal resistance) is connected to a {Rr} Ω resistor. Calculate the rms current and the mean power dissipated.',
               f'I_rms = {q(e0 / math.sqrt(2) / Rr, "A")}; P = {q(P, "W")}', f'V_rms = ε₀/√2 = {q(e0 / math.sqrt(2), "V")} (M1); I_rms = V_rms/R = {q(e0 / math.sqrt(2) / Rr, "A")} (A1); P = V_rms²/R = {q(P, "W")} (A1).', 3)


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3_gen_mcq(rng, slot):
    B, A, N = rng.choice([0.1, 0.2]), rng.choice([0.01, 0.02]), rng.choice([50, 100])
    f = rng.choice([25, 50])
    e0 = B * A * N * 2 * math.pi * f
    return nmcq(rng, f'A coil of {N} turns, area {A} m², rotates at {f} Hz in a field of {B} T. What is the peak emf?', e0,
                [B * A * N * f, e0 / math.sqrt(2), B * A * 2 * math.pi * f], 'V', f'ε₀ = BANω = BAN(2πf) = {q(e0, "V")}.', extra=False)


R.mcqs('ch07-st3', 'C2', (1, 4), [
    ('The graph of flux linkage against time for a rotating coil is a cosine curve. The emf–time graph is', 'a sine curve (shifted by a quarter-cycle)', ['an identical cosine curve', 'a straight line', 'a square wave'], 'ε = −d(NΦ)/dt.'),
    ('A rod slides along conducting rails in a magnetic field, completing a circuit. If the rod speed doubles, the power dissipated in the circuit', 'quadruples', ['doubles', 'is unchanged', 'halves'], 'ε ∝ v and P = ε²/R.'),
    ('A slip-ring generator is changed to use a split-ring commutator. The output becomes', 'a rectified (one-direction) varying emf', ['a steady d.c. emf', 'an a.c. emf of double frequency', 'zero'], 'The commutator reverses connections every half-turn.'),
])

R.static('ch07-st3', 'C4', (3, 5), [
    ('A conducting rod of length 0.25 m and mass 40 g slides without friction on horizontal rails connected by a 2.0 Ω resistor, in a vertical field of 0.80 T. It is pushed at a constant 3.0 m s⁻¹. (a) Calculate the induced emf and current. (b) Determine the force needed to keep it moving at constant speed. (c) Show that the mechanical power input equals the electrical power dissipated. (d) Describe the motion if the push is removed.',
     '(a) ε = BvL = 0.60 V; I = 0.30 A; (b) F = BIL = 0.060 N; (c) Fv = 0.18 W and I²R = 0.18 W; (d) the opposing force decelerates the rod; as v falls the force falls, so it slows with decreasing deceleration (exponentially) towards rest.',
     'ε = BvL (A1); I = ε/R (A1); F = BIL (M1 A1); power balance shown (R1); qualitative motion with reasoning (R1).', 6),
], type='multi_step', marks=6)

linearise('ch07-st3', [
    ('ε₀ = BANω for a generator coil turned at different rotation rates', 'peak emf ε₀', 'angular frequency ω', 'BAN', 'A straight line through the origin confirms ε₀ ∝ ω.'),
    ('ε = BvL for a rod moving at different speeds on rails', 'ε', 'v', 'BL, from which B can be found', 'A non-zero intercept would suggest a contact emf or meter offset.'),
])


# =============================================================================================
# ch08 E.1 Structure of the atom
# =============================================================================================
NUCLIDES = [('H', 1, 1), ('He', 2, 4), ('Li', 3, 7), ('C', 6, 12), ('C', 6, 14), ('N', 7, 14), ('O', 8, 16), ('Na', 11, 23), ('Al', 13, 27),
            ('K', 19, 40), ('Fe', 26, 56), ('Co', 27, 60), ('Sr', 38, 90), ('I', 53, 131), ('Cs', 55, 137), ('Au', 79, 197), ('Pb', 82, 208),
            ('Ra', 88, 226), ('U', 92, 235), ('U', 92, 238), ('Pu', 94, 239), ('Am', 95, 241)]

R.facts('ch08-st1', F(
    terms=[('nuclear model of the atom', 'a model in which almost all the mass and all the positive charge of an atom is concentrated in a tiny central nucleus, with electrons occupying the much larger surrounding volume'),
           ('Geiger–Marsden experiment', 'the scattering of alpha particles by thin gold foil, in which a small fraction were deflected through large angles'),
           ('distance of closest approach', 'the minimum separation between an alpha particle and a nucleus in a head-on collision, where all its kinetic energy has become electric potential energy')],
    facts=[('In the Geiger–Marsden experiment, most alpha particles passed straight through the foil. This showed that', 'most of the atom is empty space', ['the nucleus is negatively charged', 'electrons are heavy', 'gold atoms are hollow spheres of charge'], 'Few encounters with anything massive.'),
           ('A very small fraction of alpha particles were deflected through more than 90°. This showed that', 'the positive charge and mass are concentrated in a tiny nucleus', ['electrons are concentrated at the centre', 'alpha particles are negative', 'the foil was too thick'], 'Only a massive, concentrated charge can reverse an α particle.'),
           ('Why was the gold foil in the Geiger–Marsden experiment made very thin?', 'so that most alpha particles were scattered by at most one nucleus', ['to make it transparent', 'to reduce the cost', 'to keep it cool'], 'Single scattering events could be analysed.'),
           ('Why was the apparatus evacuated?', 'so that alpha particles were not absorbed or scattered by air', ['to remove electrons from the gold', 'to cool the source', 'to accelerate the particles'], 'α range in air is only a few cm.')],
    why=[('Explain why the Geiger–Marsden results were inconsistent with Thomson’s "plum pudding" model.', 'In the plum-pudding model the positive charge is spread through the atom, so the electric field inside is weak and alpha particles would only be deflected through tiny angles; the observed large-angle scattering requires a strong field from a concentrated charge.'),
         ('Explain why the distance of closest approach gives only an upper limit for the radius of the nucleus.', 'At closest approach the alpha particle is still outside the nucleus (it has been repelled by the Coulomb force without touching), so the nuclear radius must be smaller than this distance, unless deviations from Rutherford scattering are seen.'),
         ('Explain why high-energy electrons, rather than alpha particles, are used to measure nuclear radii accurately.', 'Electrons are not affected by the strong nuclear force, so they probe the charge distribution cleanly; at high energy their de Broglie wavelength is ~10⁻¹⁵ m, comparable to nuclei, giving a diffraction minimum from which the radius is found.')],
    contrast=[('the plum-pudding model', 'the nuclear model', 'The plum-pudding model spreads positive charge throughout the atom with embedded electrons; the nuclear model concentrates the positive charge and nearly all the mass in a tiny nucleus with electrons outside.')],
    misc=[('Most alpha particles bounced back from the gold foil.', 'Most passed straight through; only about 1 in 8000 was deflected through more than 90°.'),
          ('The Geiger–Marsden experiment showed that electrons orbit in fixed shells.', 'It showed the existence of a small, dense, positive nucleus; electron energy levels came later from Bohr and spectroscopy.')],
    evaluate=[('The Geiger–Marsden experiment is a good example of how unexpected results drive scientific change.', ['large-angle scattering contradicted the accepted model and led to the nuclear model'], ['the model still had problems (electron stability) that required quantum theory', 'Rutherford’s mathematical analysis, not just the observation, was crucial'], 'Yes: an anomalous result led to a paradigm shift, but it required careful theory and further revision (NOS).')],
))


@R.add('ch08-st1', 'C3', (1, 5), 'numerical')
def c3_closest(rng, slot):
    tgt = pick(rng, [('gold', 79), ('silver', 47), ('aluminium', 13), ('lead', 82), ('copper', 29), ('platinum', 78)])
    Ek = rng.choice([2.0, 4.0, 4.8, 5.3, 6.0, 7.7, 10.0])
    d = K * 2 * tgt[1] * E * E / (Ek * 1e6 * EV)
    frame = rng.randrange(3)
    if frame == 0:
        return num(f'An alpha particle of kinetic energy {Ek} MeV approaches a {tgt[0]} nucleus (Z = {tgt[1]}) head-on. Calculate the distance of closest approach.',
                   q(d, 'm'), f'Eₖ = k(2e)(Ze)/d (M1); Eₖ = {Ek} × 10⁶ × 1.60 × 10⁻¹⁹ J (A1); d = {q(d, "m")} (A1).', 3)
    if frame == 1:
        A = rng.choice([27, 64, 108, 197, 208])
        Rn = R0 * A ** (1 / 3)
        Emin = K * 2 * tgt[1] * E * E / Rn / EV / 1e6
        return num(f'Estimate the minimum kinetic energy, in MeV, an alpha particle would need to reach the surface of a {tgt[0]} nucleus (Z = {tgt[1]}, A = {A}), using R = R₀A^(1/3) with R₀ = 1.20 fm.',
                   q(Emin, 'MeV'), f'R = 1.20 × 10⁻¹⁵ × {A}^(1/3) = {q(Rn, "m")} (A1); Eₖ = k(2e)(Ze)/R (M1) = {q(Emin, "MeV")} (A1).', 3)
    d2 = d / 2
    return num(f'In a head-on collision with a {tgt[0]} nucleus an alpha particle of {Ek} MeV comes within {q(d, "m")}. Determine the energy needed to come within {q(d2, "m")}, and explain the reasoning.',
               q(2 * Ek, 'MeV'), f'Eₖ = kqQ/d, so Eₖ ∝ 1/d (R1); halving d needs twice the energy: {q(2 * Ek, "MeV")} (A1).', 2)


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def c3_closest_mcq(rng, slot):
    Ek = rng.choice([4.0, 5.0, 8.0])
    Z = 79
    d = K * 2 * Z * E * E / (Ek * 1e6 * EV)
    return nmcq(rng, f'An alpha particle of {Ek} MeV is fired directly at a gold nucleus (Z = 79). What is the distance of closest approach?', d,
                [d / 2, K * Z * E * E / (Ek * 1e6 * EV) / 2 if False else d * 2, K * 2 * Z * E / (Ek * 1e6)], 'm', f'd = k(2e)(79e)/Eₖ = {q(d, "m")}; using charge e instead of 2e gives half this.', extra=True)


R.mcqs('ch08-st1', 'C2', (1, 4), [
    ('If the alpha-particle energy in Geiger–Marsden scattering is increased, the number scattered through large angles', 'decreases, because faster particles are deflected less', ['increases', 'is unchanged', 'becomes zero'], 'Deflection depends on closest approach; higher Eₖ means smaller deflection for the same impact parameter.'),
    ('Using aluminium foil (Z = 13) instead of gold (Z = 79) at the same α energy would', 'reduce the fraction scattered through large angles', ['increase it', 'make no difference', 'stop all alpha particles'], 'Weaker repulsion from smaller nuclear charge.'),
    ('Which feature of the nuclear model could classical physics NOT explain?', 'why orbiting electrons do not radiate energy and spiral into the nucleus', ['why the nucleus is positive', 'why most alpha particles pass through', 'why atoms are neutral'], 'Accelerating charges radiate classically; quantum theory was required.'),
])

R.static('ch08-st1', 'C4', (3, 5), [
    ('Describe the Geiger–Marsden experiment and explain how the observations led to the nuclear model of the atom. Include the purpose of each part of the apparatus and the significance of the angular distribution of scattered alpha particles.',
     'A collimated beam of alpha particles from a radium source in an evacuated chamber struck thin gold foil; a zinc sulfide screen viewed by microscope was moved around to count scintillations at different angles. Most particles passed undeviated (atom mostly empty), some were deflected through small angles, and about 1 in 8000 through more than 90° (concentrated positive charge and mass). Rutherford showed the number scattered at angle θ follows 1/sin⁴(θ/2), consistent with a Coulomb force from a point-like nucleus of radius < 10⁻¹⁴ m.',
     'Source, collimation, vacuum, thin foil, ZnS detector (A1 A1); three observations with interpretation (R1 R1 R1); quantitative angular distribution / size estimate (A1).', 6),
], type='multi_step', marks=6)


R.facts('ch08-st2', F(
    terms=[('nucleon number (mass number) A', 'the total number of protons and neutrons in a nucleus'),
           ('proton number (atomic number) Z', 'the number of protons in a nucleus, which defines the element'),
           ('isotopes', 'nuclides of the same element with the same proton number but different numbers of neutrons'),
           ('nuclide', 'a particular species of nucleus characterised by its proton number and nucleon number')],
    facts=[('The nucleus of ²³⁵₉₂U contains', '92 protons and 143 neutrons', ['92 protons and 235 neutrons', '143 protons and 92 neutrons', '235 protons and 92 neutrons'], 'N = A − Z.'),
           ('Isotopes of an element have the same', 'number of protons', ['number of neutrons', 'nucleon number', 'nuclear mass'], 'Same Z, different N.'),
           ('The radius of a nucleus is proportional to', 'A^(1/3)', ['A', 'A²', 'A^(−1/3)'], 'R = R₀A^(1/3).'),
           ('The density of nuclear matter', 'is approximately the same for all nuclei', ['increases with A', 'decreases with A', 'equals the density of water'], 'Volume ∝ A, mass ∝ A.')],
    why=[('Explain why all nuclei have approximately the same density.', 'Volume ∝ R³ = R₀³A, and mass ≈ A × u, so density = mass/volume ≈ 3u/(4πR₀³), independent of A; nucleons pack together at constant spacing.'),
         ('Explain why isotopes of an element have the same chemical properties.', 'Chemical behaviour depends on the electron arrangement, which is determined by the proton number Z; isotopes have the same Z and so the same electron configuration.'),
         ('Explain why the nucleus is described as being about 10⁵ times smaller than the atom.', 'Nuclear radii are ~10⁻¹⁵ m (fm) while atomic radii are ~10⁻¹⁰ m; the ratio is ~10⁵, so the atom is mostly empty space.')],
    contrast=[('proton number', 'nucleon number', 'Proton number Z counts protons (identifying the element); nucleon number A counts protons plus neutrons (giving the approximate mass in u).'),
              ('isotopes', 'isobars (same A, different Z)', 'Isotopes have the same Z but different A (same element); nuclides with the same A but different Z are different elements with similar masses.')],
    misc=[('Isotopes have the same mass number but different proton numbers.', 'Isotopes have the same proton number but different numbers of neutrons, so different mass numbers.'),
          ('A heavier nucleus is denser than a lighter one.', 'Nuclear density is roughly constant (~2 × 10¹⁷ kg m⁻³) for all nuclei.')],
    evaluate=[('The formula R = R₀A^(1/3) shows that nuclei are hard spheres with sharp edges.', ['it fits electron-scattering data well', 'it implies constant density'], ['scattering shows a diffuse surface region about 2 fm thick', 'R₀ differs slightly for charge and matter radii', 'nuclei may be deformed'], 'The formula is an excellent approximation for the average size but nuclei have diffuse surfaces and can be non-spherical.')],
))


@R.add('ch08-st2', 'C3', (1, 5), 'numerical')
def c3_nucleus(rng, slot):
    sym, Z, A = pick(rng, NUCLIDES)
    frame = rng.randrange(4)
    if frame == 0:
        return num(f'State the number of protons, neutrons and electrons in a neutral atom of {sup(A)} {sym} (Z = {Z}).',
                   f'{Z} protons, {A - Z} neutrons, {Z} electrons', f'Z = {Z} protons (A1); N = A − Z = {A - Z} (A1); neutral atom: {Z} electrons (A1).', 2)
    Rn = R0 * A ** (1 / 3)
    if frame == 1:
        return num(f'Calculate the radius of the nucleus of {sup(A)}{sym}, using R = R₀A^(1/3) with R₀ = 1.20 × 10⁻¹⁵ m.',
                   q(Rn, 'm'), f'R = 1.20 × 10⁻¹⁵ × {A}^(1/3) (M1) = {q(Rn, "m")} (A1).', 2)
    if frame == 2:
        rho = A * U / (4 / 3 * math.pi * Rn ** 3)
        return num(f'Estimate the density of the nucleus of {sup(A)}{sym}. (R₀ = 1.20 × 10⁻¹⁵ m, 1 u = 1.661 × 10⁻²⁷ kg)',
                   q(rho, 'kg m⁻³'), f'R = {q(Rn, "m")} (A1); mass ≈ {A} u = {q(A * U, "kg")} (A1); ρ = m/(4/3 πR³) = {q(rho, "kg m⁻³")} (A1).', 3)
    s2, Z2, A2 = pick(rng, [n for n in NUCLIDES if n[2] != A])
    ratio = (A2 / A) ** (1 / 3)
    return num(f'Calculate the ratio of the nuclear radius of {sup(A2)}{s2} to that of {sup(A)}{sym}.',
               sf(ratio, 3), f'R ∝ A^(1/3) (M1); ratio = ({A2}/{A})^(1/3) = {sf(ratio, 3)} (A1).', 2)


@R.add('ch08-st2', 'C3', (1, 4), 'mcq')
def c3_nucleus_mcq(rng, slot):
    A1 = rng.choice([8, 27, 64, 125])
    k = rng.choice([8, 27])
    A2 = A1 * k
    if A2 > 260:
        A2 = A1 * 8
        k = 8
    r = round(k ** (1 / 3))
    return mcq(rng, f'A nucleus has nucleon number {A1} and radius R. What is the radius of a nucleus with nucleon number {A2}?', f'{r}R', [f'{k}R', f'{k ** 2}R' if k ** 2 != r else f'{k + 1}R', f'{round(math.sqrt(k), 2):g}R'],
               f'R ∝ A^(1/3): ({A2}/{A1})^(1/3) = {r}.')


R.mcqs('ch08-st2', 'C2', (1, 4), [
    ('Carbon-12 and carbon-14 differ in', 'the number of neutrons', ['the number of protons', 'their chemical reactions', 'the number of electrons in the neutral atom'], 'Both have Z = 6.'),
    ('The approximate ratio of atomic radius to nuclear radius is', '10⁵', ['10²', '10¹⁰', '10'], '10⁻¹⁰ m / 10⁻¹⁵ m.'),
    ('Which pair are isotopes?', '³⁵₁₇Cl and ³⁷₁₇Cl', ['¹⁴₆C and ¹⁴₇N', '⁴⁰₁₈Ar and ⁴⁰₂₀Ca', '¹²₆C and ¹⁶₈O'], 'Same Z = 17.'),
])

linearise('ch08-st2', [
    ('R = R₀A^(1/3) for nuclear radii measured by electron scattering', 'R', 'A^(1/3)', 'R₀ (about 1.2 fm)', 'A straight line through the origin confirms constant nuclear density.'),
    ('R = R₀A^(1/3) for nuclear radii, tested using logarithms', 'ln R', 'ln A', '1/3 (the power), with intercept ln R₀', 'A gradient of 1/3 confirms the cube-root dependence.'),
])

R.static('ch08-st2', 'C4', (3, 5), [
    ('Electrons of energy 420 MeV are diffracted by oxygen-16 nuclei and the first diffraction minimum is observed at about 44°. (a) Show that the de Broglie wavelength of the electrons is about 3.0 × 10⁻¹⁵ m (treat them as ultra-relativistic, E = pc). (b) Using sin θ ≈ 1.22λ/(2R), estimate the nuclear radius. (c) Compare with R = R₀A^(1/3) and comment.',
     '(a) p = E/c = 420 × 10⁶ × 1.60 × 10⁻¹⁹/3.00 × 10⁸ = 2.24 × 10⁻¹⁹ kg m s⁻¹; λ = h/p = 2.96 × 10⁻¹⁵ m; (b) R = 1.22λ/(2 sin 44°) = 2.6 × 10⁻¹⁵ m; (c) R₀A^(1/3) = 1.20 × 16^(1/3) = 3.0 fm – the same order, agreeing within the approximations.',
     'p = E/c (M1); λ = h/p ≈ 3.0 fm (A1); R ≈ 2.6 fm (M1 A1); comparison and comment on approximations (R1).'),
], type='multi_step', marks=5)


R.facts('ch08-st3', F(
    terms=[('emission spectrum', 'a set of discrete bright lines of specific wavelengths emitted by a hot, low-pressure gas'),
           ('absorption spectrum', 'a continuous spectrum crossed by dark lines at specific wavelengths, produced when white light passes through a cool gas'),
           ('energy level', 'one of the discrete values of energy that an electron bound in an atom may have'),
           ('photon', 'a quantum of electromagnetic radiation of energy E = hf')],
    facts=[('Line spectra provide evidence that', 'electrons in atoms have discrete energy levels', ['atoms are mostly empty space', 'electrons have mass', 'light travels at a constant speed'], 'Each line is a transition between fixed levels.'),
           ('An electron drops from a level at −1.5 eV to one at −3.4 eV. The emitted photon has energy', '1.9 eV', ['4.9 eV', '3.4 eV', '1.5 eV'], 'ΔE = 3.4 − 1.5.'),
           ('The dark lines in the solar spectrum (Fraunhofer lines) are caused by', 'absorption by cooler gases in the Sun’s outer atmosphere', ['emission from the Sun’s core', 'diffraction in the telescope', 'Earth’s magnetic field'], 'Photons at transition energies are absorbed and re-emitted in all directions.'),
           ('How many different photon energies can be emitted by atoms excited to the n = 4 level?', '6', ['4', '3', '10'], 'n(n − 1)/2 = 6.')],
    why=[('Explain why the dark lines in an absorption spectrum occur at the same wavelengths as the bright lines in the emission spectrum of the same element.', 'Both correspond to transitions between the same pairs of energy levels; a photon of energy ΔE = hc/λ is absorbed to raise an electron and emitted when it falls back, so the wavelengths coincide.'),
         ('Explain why absorption lines are dark even though the excited atoms re-emit photons.', 'Re-emission occurs in random directions, so very little of the absorbed light continues towards the observer along the original beam; the line therefore appears dark relative to the continuum.'),
         ('Explain how spectra are used to identify the elements present in a distant star.', 'Each element has a unique set of energy levels and therefore a unique pattern of spectral lines (a "fingerprint"); matching observed lines to laboratory spectra identifies the elements.')],
    contrast=[('an emission spectrum', 'an absorption spectrum', 'An emission spectrum shows bright lines on a dark background from a hot gas; an absorption spectrum shows dark lines on a continuous spectrum where a cooler gas absorbs specific wavelengths.'),
              ('ground state', 'excited state', 'The ground state is the lowest energy level of the atom; an excited state is any higher level, from which the electron returns by emitting photons.')],
    misc=[('An atom can absorb a photon of any energy to raise an electron to a higher level.', 'A photon is absorbed only if its energy exactly matches the difference between two levels (or exceeds the ionisation energy).'),
          ('Shorter-wavelength lines come from transitions with smaller energy differences.', 'E = hc/λ: shorter wavelength means larger energy difference.')],
    evaluate=[('Spectroscopy is the most important source of information about stars.', ['gives composition, temperature, radial velocity, magnetic fields', 'works at any distance'], ['distances need parallax or standard candles', 'masses need binary orbits', 'luminosity needs brightness and distance'], 'Spectroscopy is arguably the richest single source, but it must be combined with other methods to determine distance and mass.')],
))


def _levels(rng):
    sets = [('hydrogen', [-13.6, -3.40, -1.51, -0.85, -0.54]), ('a mercury-like atom', [-10.4, -5.5, -3.7, -2.7, -1.6]),
            ('sodium', [-5.14, -3.03, -1.95, -1.52, -1.39]), ('a hypothetical atom', [-12.0, -6.0, -3.5, -2.0, -1.2])]
    return pick(rng, sets)


@R.add('ch08-st3', 'C3', (1, 5), 'numerical')
def c3_spectra(rng, slot):
    at, lv = _levels(rng)
    i, j = sorted(rng.sample(range(len(lv)), 2))
    dE = lv[j] - lv[i]
    lam = H * C / (dE * EV)
    frame = rng.randrange(4)
    lvtxt = ', '.join(f'{v:.2f} eV'.replace('-', '−') for v in lv)
    if frame == 0:
        return num(f'The energy levels of {at} include {lvtxt}. Calculate the wavelength of the photon emitted when an electron falls from the {lv[j]:.2f} eV level to the {lv[i]:.2f} eV level.'.replace('-', '−'),
                   q(lam * 1e9, 'nm'), f'ΔE = {dE:.2f} eV = {q(dE * EV, "J")} (M1); λ = hc/ΔE (M1) = {q(lam * 1e9, "nm")} (A1).', 3)
    if frame == 1:
        return num(f'A photon of wavelength {sf(lam * 1e9, 3)} nm is absorbed by {at} in its {lv[i]:.2f} eV level. Determine the energy of the level to which the electron is raised.'.replace('-', '−'),
                   f'{lv[j]:.2f} eV'.replace('-', '−'), f'E = hc/λ = {q(H * C / lam, "J")} = {dE:.2f} eV (M1 A1); new level = {lv[i]:.2f} + {dE:.2f} = {lv[j]:.2f} eV (A1).'.replace('-', '−'), 3)
    if frame == 2:
        n = rng.choice([3, 4, 5])
        return num(f'Atoms of a gas are excited to the {["", "first", "second", "third", "fourth"][n - 1]} excited state (level n = {n}). How many different spectral lines can be emitted as they return to the ground state?',
                   f'{n * (n - 1) // 2}', f'Each pair of levels gives one line (M1): n(n − 1)/2 = {n * (n - 1) // 2} (A1).', 2)
    f = dE * EV / H
    return num(f'In {at} an electron makes a transition from {lv[j]:.2f} eV to {lv[i]:.2f} eV. Calculate the frequency of the emitted photon and identify the region of the electromagnetic spectrum.'.replace('-', '−'),
               f'{q(f, "Hz")}; {"ultraviolet" if lam < 400e-9 else "visible" if lam < 700e-9 else "infrared"}', f'f = ΔE/h (M1) = {q(f, "Hz")} (A1); λ = {q(lam * 1e9, "nm")} → {"ultraviolet" if lam < 400e-9 else "visible" if lam < 700e-9 else "infrared"} (A1).', 3)


@R.add('ch08-st3', 'C3', (1, 4), 'mcq')
def c3_spectra_mcq(rng, slot):
    dE = rng.choice([1.89, 2.55, 2.86, 3.02, 10.2, 1.51, 2.10])
    lam = H * C / (dE * EV) * 1e9
    return nmcq(rng, f'An electron falls between two energy levels separated by {dE} eV. What is the wavelength of the emitted photon?', lam,
                [H * C / dE * 1e9 / 1e-19 * 1e-28, lam / 2, H / (dE * EV) * 1e9 * 1e8], 'nm', f'λ = hc/ΔE = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/({dE} × 1.60 × 10⁻¹⁹) = {q(lam, "nm")}.', extra=True)


R.mcqs('ch08-st3', 'C2', (1, 4), [
    ('White light passes through cool sodium vapour. The spectrum observed shows', 'a continuous spectrum with dark lines at sodium wavelengths', ['bright sodium lines on a dark background', 'only a continuous spectrum', 'no light at all'], 'Absorption spectrum.'),
    ('Which transition in an atom emits the photon of highest frequency?', 'the transition with the largest energy difference', ['the transition between the two highest levels', 'any transition to the ground state', 'the transition with the smallest energy difference'], 'f = ΔE/h.'),
    ('An electron in the ground state at −13.6 eV absorbs a photon of 15.0 eV. The electron', 'is ionised and leaves with 1.4 eV of kinetic energy', ['is raised to n = 2', 'cannot absorb the photon', 'is raised to n = 3'], 'Energy above the ionisation energy becomes kinetic energy.'),
])

R.static('ch08-st3', 'C4', (3, 5), [
    ('A fluorescent tube contains mercury vapour. Electrons in the discharge excite mercury atoms, which emit ultraviolet at 254 nm; a phosphor coating then emits visible light. (a) Calculate the energy of a 254 nm photon in eV. (b) Explain why the phosphor emits light of longer wavelength than it absorbs. (c) Explain why the light from the tube is not a continuous spectrum and why this affects how colours look.',
     '(a) E = hc/λ = 7.83 × 10⁻¹⁹ J = 4.89 eV; (b) the phosphor atoms are raised to a high level and return in several smaller steps, each emitting a lower-energy (longer-wavelength) photon; (c) emission is from discrete level differences in the phosphors, so the spectrum consists of bands/lines; objects reflecting wavelengths absent from the spectrum appear different (poor colour rendering).',
     'E = hc/λ (M1) 4.89 eV (A1); cascade through intermediate levels (R1); discrete energy levels give line/band spectrum (R1); colour rendering consequence (R1).'),
], type='multi_step', marks=5)


def _spec_spec(rng):
    lam = [410.2, 434.0, 486.1, 656.3]
    lam_meas = [round(l_ * rng.uniform(0.998, 1.002), 1) for l_ in lam]
    ns = [6, 5, 4, 3]
    return dict(intro='The wavelengths λ of four visible lines of the hydrogen (Balmer) series, ending on n = 2, are measured with a spectrometer. Theory: 1/λ = R_H(1/4 − 1/n²).',
                xname='n', xunit='–', yname='λ', yunit='nm', xs=ns, ys=lam_meas, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b:.1f}',
                plot_x=lambda a: 1 / 4 - 1 / a ** 2, plot_y=lambda b: 1 / (b * 1e-9), plot_label='1/λ in m⁻¹ (y) against (1/4 − 1/n²) (x)', what='the Rydberg constant R_H', what_short='R_H',
                gunit='m⁻¹', deduce=lambda m_, b_: (m_, 'm⁻¹', 'R_H = gradient'))


gradient_fit('ch08-st3', _spec_spec)


R.facts('ch08-st4', F(
    terms=[('Bohr model', 'a model of the hydrogen atom in which the electron moves in circular orbits whose angular momentum is quantised, mvr = nh/2π, with energies Eₙ = −13.6/n² eV'),
           ('ionisation energy', 'the minimum energy needed to remove an electron from an atom in its ground state; 13.6 eV for hydrogen'),
           ('principal quantum number', 'the integer n labelling the allowed orbits and energy levels in the Bohr model'),
           ('Lyman series', 'the hydrogen spectral lines from transitions down to n = 1, all in the ultraviolet')],
    facts=[('In the Bohr model, the energy of the hydrogen electron in level n is', '−13.6/n² eV', ['−13.6n² eV', '−13.6/n eV', '+13.6/n² eV'], 'Eₙ ∝ −1/n².'),
           ('The visible lines of hydrogen (Balmer series) are transitions that end on', 'n = 2', ['n = 1', 'n = 3', 'n = ∞'], 'Lyman ends on n = 1 (UV), Balmer on n = 2.'),
           ('Bohr’s quantisation condition states that', 'the angular momentum of the electron is a whole-number multiple of h/2π', ['the energy is a multiple of hf', 'the radius is a multiple of the wavelength', 'the electron’s speed is quantised in units of c'], 'mvr = nh/2π.'),
           ('A major limitation of the Bohr model is that it', 'works accurately only for hydrogen-like (one-electron) atoms', ['cannot explain line spectra at all', 'predicts the wrong ionisation energy for hydrogen', 'ignores the nucleus'], 'Multi-electron atoms need full quantum mechanics.')],
    why=[('Explain why the energy levels of hydrogen get closer together as n increases.', 'Eₙ = −13.6/n² eV; the difference between successive levels, 13.6(1/n² − 1/(n+1)²), decreases rapidly with n, so levels crowd towards the ionisation limit at 0 eV.'),
         ('Explain how the Bohr condition mvr = nh/2π can be interpreted using de Broglie waves.', 'Using λ = h/(mv), the condition becomes 2πr = nλ: a whole number of electron wavelengths fits around the orbit, forming a standing wave, so only these orbits are stable.'),
         ('Explain why the Bohr model was regarded as a step forward despite being incorrect in detail.', 'It explained the hydrogen spectrum quantitatively (Rydberg formula), introduced quantisation into atomic structure and predicted ionisation energy, paving the way for quantum mechanics (NOS: models can be useful though limited).')],
    contrast=[('the Bohr model', 'the quantum-mechanical model', 'The Bohr model has definite circular orbits with quantised angular momentum; quantum mechanics replaces orbits with probability distributions (orbitals) given by wavefunctions and applies to all atoms.')],
    misc=[('In the Bohr model the electron radiates energy continuously as it orbits.', 'Bohr postulated that electrons in allowed orbits do NOT radiate; photons are emitted only during transitions between orbits.'),
          ('The n = 2 level of hydrogen is at −6.8 eV.', 'E₂ = −13.6/2² = −3.4 eV.')],
    evaluate=[('The Bohr model should no longer be taught because it is wrong.', ['orbits are not real; electrons are described by wavefunctions'], ['it gives correct energy levels for hydrogen with simple mathematics', 'it introduces quantisation and shows how models evolve (NOS)', 'it is a useful stepping stone'], 'It should be taught as a historically important, limited model, with its limitations made explicit.')],
))


@R.add('ch08-st4', 'C3', (1, 5), 'numerical')
def c3_bohr(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        ni, nf = rng.choice([(2, 1), (3, 1), (3, 2), (4, 2), (5, 2), (4, 3), (6, 2), (5, 3)])
        dE = 13.6 * (1 / nf ** 2 - 1 / ni ** 2)
        lam = H * C / (dE * EV)
        return num(f'Using the Bohr model (Eₙ = −13.6/n² eV), calculate the wavelength of the photon emitted when a hydrogen electron moves from n = {ni} to n = {nf}.',
                   q(lam * 1e9, 'nm'), f'E_{ni} = {-13.6 / ni ** 2:.3f} eV, E_{nf} = {-13.6 / nf ** 2:.3f} eV (M1); ΔE = {dE:.3f} eV (A1); λ = hc/ΔE = {q(lam * 1e9, "nm")} (A1).'.replace('-', '−'), 3)
    if frame == 1:
        n = rng.choice([2, 3, 4, 5])
        Ei = 13.6 / n ** 2
        return num(f'Calculate the energy needed to ionise a hydrogen atom whose electron is in the n = {n} level, in eV and in J.',
                   f'{sf(Ei, 3)} eV = {q(Ei * EV, "J")}', f'Eₙ = −13.6/{n}² = −{sf(Ei, 3)} eV (M1); ionisation energy = {sf(Ei, 3)} eV = {q(Ei * EV, "J")} (A1).', 2)
    if frame == 2:
        n = rng.choice([1, 2, 3])
        r1 = 5.29e-11
        rn = r1 * n * n
        v = n * H / (2 * math.pi * ME * rn)
        return num(f'In the Bohr model the radius of the n-th orbit is rₙ = n² × 5.29 × 10⁻¹¹ m. Calculate the speed of the electron in the n = {n} orbit using mvr = nh/2π.',
                   q(v, 'm s⁻¹'), f'r = {q(rn, "m")} (A1); v = nh/(2πmₑr) (M1) = {q(v, "m s⁻¹")} (A1).', 3)
    lam = rng.choice([97.3, 102.6, 121.6, 486.1, 656.3, 434.0])
    dE = H * C / (lam * 1e-9) / EV
    pairs = {(i, j): 13.6 * (1 / j ** 2 - 1 / i ** 2) for i in range(2, 8) for j in range(1, i)}
    (ni, nf), _ = min(pairs.items(), key=lambda kv: abs(kv[1] - dE))
    return num(f'A hydrogen spectral line has wavelength {lam} nm. Use the Bohr energy levels to identify the transition that produces it.',
               f'n = {ni} → n = {nf}', f'ΔE = hc/λ = {sf(dE, 3)} eV (M1 A1); matches E_{ni} − E_{nf} = {sf(pairs[(ni, nf)], 3)} eV (A1).', 3)


@R.add('ch08-st4', 'C3', (1, 4), 'mcq')
def c3_bohr_mcq(rng, slot):
    n = rng.choice([2, 3, 4, 5])
    En = -13.6 / n ** 2
    return nmcq(rng, f'According to the Bohr model, what is the energy of the hydrogen electron in the n = {n} level?', En,
                [-13.6 / n, -13.6 * n ** 2 / 10, 13.6 / n ** 2], 'eV', f'Eₙ = −13.6/n² = {sf(En, 3)} eV.', extra=False)


R.mcqs('ch08-st4', 'C2', (1, 4), [
    ('According to the Bohr model, as n increases, the radius of the orbit', 'increases in proportion to n²', ['decreases', 'increases in proportion to n', 'is constant'], 'rₙ = n²r₁.'),
    ('Which hydrogen series lies entirely in the ultraviolet?', 'Lyman', ['Balmer', 'Paschen', 'Brackett'], 'Transitions to n = 1 have ΔE ≥ 10.2 eV.'),
    ('The longest-wavelength line of the Balmer series corresponds to the transition', 'n = 3 → n = 2', ['n = ∞ → n = 2', 'n = 2 → n = 1', 'n = 4 → n = 2'], 'Smallest ΔE ending on n = 2.'),
])

R.static('ch08-st4', 'C4', (3, 5), [
    ('(a) Show that the Bohr condition mvr = nh/2π combined with ke²/r² = mv²/r gives rₙ ∝ n². (b) Show that the total energy of the electron is E = −ke²/(2r). (c) Hence explain why Eₙ ∝ −1/n² and calculate E₁ given r₁ = 5.29 × 10⁻¹¹ m.',
     '(a) v = nh/(2πmr); substituting into mv² = ke²/r gives r = n²h²/(4π²mke²) ∝ n²; (b) Eₖ = ½mv² = ke²/(2r), Eₚ = −ke²/r, total −ke²/(2r); (c) E ∝ −1/r ∝ −1/n²; E₁ = −8.99 × 10⁹ × (1.60 × 10⁻¹⁹)²/(2 × 5.29 × 10⁻¹¹) = −2.18 × 10⁻¹⁸ J = −13.6 eV.',
     'Substitution for v (M1); r ∝ n² (A1); Eₖ and Eₚ (M1); total energy (A1); E₁ = −13.6 eV (A1).', 6),
], type='multi_step', marks=6)


# =============================================================================================
# ch09 E.2 Quantum physics (HL)
# =============================================================================================
METALS = [('caesium', 2.1), ('potassium', 2.3), ('sodium', 2.3), ('calcium', 2.9), ('magnesium', 3.7), ('zinc', 4.3), ('copper', 4.7), ('silver', 4.3), ('platinum', 5.6)]

R.facts('ch09-st1', F(
    terms=[('photoelectric effect', 'the emission of electrons from a metal surface when electromagnetic radiation above a certain frequency falls on it'),
           ('work function', 'the minimum energy needed to remove an electron from the surface of a metal, Φ'),
           ('threshold frequency', 'the minimum frequency of radiation that causes photoelectric emission from a given metal, f₀ = Φ/h'),
           ('stopping potential', 'the minimum potential difference needed to stop the most energetic photoelectrons reaching the collector, eVₛ = Eₖ,max')],
    facts=[('Increasing the intensity of light above the threshold frequency', 'increases the number of photoelectrons emitted per second', ['increases the maximum kinetic energy', 'decreases the threshold frequency', 'increases the work function'], 'More photons per second, same photon energy.'),
           ('The gradient of a graph of maximum kinetic energy of photoelectrons against frequency is', 'the Planck constant h', ['the work function', 'the threshold frequency', 'the charge on the electron'], 'Eₖ,max = hf − Φ.'),
           ('Light below the threshold frequency falls on a metal. Increasing its intensity', 'still produces no photoelectrons', ['eventually causes emission', 'increases Eₖ,max', 'reduces the work function'], 'Each photon has too little energy, however many arrive.'),
           ('Einstein’s photoelectric equation is', 'hf = Φ + Eₖ,max', ['hf = Φ − Eₖ,max', 'Eₖ,max = Φ/hf', 'hf = eV + mc²'], 'Photon energy = work function + max KE.')],
    why=[('Explain why the wave model of light cannot explain the existence of a threshold frequency.', 'In the wave model energy arrives continuously and depends on intensity, so any frequency should eventually liberate electrons if the light is intense enough or shines long enough; the observation that no electrons are emitted below f₀ regardless of intensity contradicts this.'),
         ('Explain why photoelectrons are emitted with a range of kinetic energies up to a maximum.', 'Each photon gives all its energy hf to one electron; electrons deeper in the metal or more tightly bound lose extra energy escaping, so only electrons at the surface needing just Φ emerge with the maximum Eₖ = hf − Φ.'),
         ('Explain why photoemission is observed to be instantaneous, even at very low intensity.', 'Energy is delivered in discrete photons; a single photon above threshold gives enough energy to one electron immediately, whereas the wave model predicts a delay while energy accumulates.')],
    contrast=[('the wave model of light', 'the photon model of light', 'The wave model treats light energy as continuous and spread over the wavefront, depending on intensity; the photon model treats light as quanta of energy hf, each absorbed by a single electron, so frequency determines whether emission occurs.')],
    misc=[('Brighter light makes photoelectrons faster.', 'Brighter light (more photons) increases the number of electrons emitted per second, not their maximum kinetic energy, which depends only on frequency.'),
          ('If the frequency is doubled, the maximum kinetic energy of the photoelectrons doubles.', 'Eₖ,max = hf − Φ: doubling f more than doubles Eₖ,max because Φ is subtracted.'),
          ('The stopping potential depends on the intensity of the light.', 'eVₛ = hf − Φ depends only on frequency and work function.')],
    evaluate=[('The photoelectric effect proves that light is made of particles.', ['threshold frequency, instantaneous emission and Eₖ independent of intensity are explained by photons'], ['interference and diffraction need a wave description', 'light shows wave–particle duality', 'experiments support models rather than prove them (NOS)'], 'It is strong evidence for the photon (quantum) model of energy exchange, but light is best described by wave–particle duality.')],
))


@R.add('ch09-st1', 'C3', (1, 5), 'numerical')
def c3_photoelectric(rng, slot):
    mt, phi = pick(rng, METALS)
    frame = rng.randrange(5)
    if frame == 0:
        f0 = phi * EV / H
        return num(f'The work function of {mt} is {phi} eV. Calculate its threshold frequency and the corresponding wavelength.',
                   f'f₀ = {q(f0, "Hz")}; λ₀ = {q(C / f0 * 1e9, "nm")}', f'Φ = {q(phi * EV, "J")} (A1); f₀ = Φ/h = {q(f0, "Hz")} (A1); λ₀ = c/f₀ = {q(C / f0 * 1e9, "nm")} (A1).', 3)
    lam = rng.choice([200, 250, 300, 350, 400, 450])
    Eph = H * C / (lam * 1e-9) / EV
    Ek = Eph - phi
    if Ek <= 0.05:
        return None
    if frame == 1:
        return num(f'Ultraviolet light of wavelength {lam} nm falls on a {mt} surface (work function {phi} eV). Calculate the maximum kinetic energy of the emitted electrons in eV.',
                   q(Ek, 'eV'), f'E_photon = hc/λ = {q(Eph * EV, "J")} = {sf(Eph, 3)} eV (M1 A1); Eₖ,max = {sf(Eph, 3)} − {phi} = {q(Ek, "eV")} (A1).', 3)
    if frame == 2:
        return num(f'Light of wavelength {lam} nm illuminates a {mt} photocell (Φ = {phi} eV). Determine the stopping potential.',
                   q(Ek, 'V'), f'hc/λ = {sf(Eph, 3)} eV (M1); eVₛ = hf − Φ (M1); Vₛ = {q(Ek, "V")} (A1).', 3)
    if frame == 3:
        v = math.sqrt(2 * Ek * EV / ME)
        return num(f'Calculate the maximum speed of electrons emitted from {mt} (Φ = {phi} eV) by radiation of wavelength {lam} nm.',
                   q(v, 'm s⁻¹'), f'Eₖ,max = hc/λ − Φ = {sf(Ek, 3)} eV = {q(Ek * EV, "J")} (M1 A1); v = √(2Eₖ/mₑ) = {q(v, "m s⁻¹")} (A1).', 3)
    P = rng.choice([1.0, 2.0, 5.0]) * 1e-3
    eff = rng.choice([0.01, 0.02, 0.05])
    n = P / (Eph * EV)
    I = n * eff * E
    return num(f'A {sf(P * 1e3, 2)} mW beam of {lam} nm light falls on a {mt} cathode. If {int(eff * 100)} % of the photons release an electron, calculate the photoelectric current.',
               q(I, 'A'), f'Photon energy = {q(Eph * EV, "J")} (A1); photons per second = P/E = {q(n, "s⁻¹")} (M1); I = ne × efficiency = {q(I, "A")} (A1).', 3)


@R.add('ch09-st1', 'C3', (1, 4), 'mcq')
def c3_pe_mcq(rng, slot):
    mt, phi = pick(rng, METALS)
    Eph = rng.choice([4.0, 5.0, 6.0, 6.5, 7.0])
    if Eph <= phi:
        Eph = phi + 1.5
    Ek = Eph - phi
    return nmcq(rng, f'Photons of energy {Eph} eV fall on {mt} (work function {phi} eV). What is the maximum kinetic energy of the photoelectrons?', Ek,
                [Eph + phi, Eph, phi], 'eV', f'Eₖ,max = hf − Φ = {Eph} − {phi} = {q(Ek, "eV")}.', extra=False)


@R.add('ch09-st1', 'C2', (2, 4), 'explain')
def c2_pe_predict(rng, slot):
    ch = [('the intensity of the light is doubled at constant frequency', 'the photocurrent doubles but the stopping potential is unchanged', 'twice as many photons per second, each with the same energy hf'),
          ('the frequency is increased at constant intensity (power)', 'the stopping potential increases, but the photocurrent decreases slightly', 'each photon has more energy, but fewer photons arrive per second for the same power'),
          ('the metal is replaced by one with a larger work function', 'the stopping potential decreases and the threshold frequency increases', 'more energy is needed to release each electron, so Eₖ,max = hf − Φ falls'),
          ('red light is used instead of ultraviolet on zinc', 'no electrons are emitted', 'red photons have energy below the work function of zinc (≈ 4.3 eV)')]
    c, eff, why = pick(rng, ch)
    return dict(stem=f'In a photoelectric experiment, predict and explain the effect on the photocurrent and the stopping potential when {c}.', answer=f'{eff[0].upper() + eff[1:]}: {why}.',
                type='explain', marks=3, markingKey=f'{eff} (A1 A1); {why} (R1).')


R.mcqs('ch09-st1', 'C2', (1, 4), [
    ('Graphs of Eₖ,max against frequency for two different metals are', 'parallel lines with different intercepts', ['lines of different gradient through the origin', 'identical lines', 'curves'], 'Gradient h for all; intercept −Φ differs.'),
    ('The intercept on the frequency axis of a graph of stopping potential against frequency gives', 'the threshold frequency', ['the work function in eV', 'h/e', 'the photocurrent'], 'Vₛ = 0 at f = f₀.'),
    ('The gradient of a graph of stopping potential Vₛ against frequency f is', 'h/e', ['h', 'e/h', 'Φ/e'], 'Vₛ = (h/e)f − Φ/e.'),
])


def _pe_spec(rng):
    mt, phi = pick(rng, METALS[:6])
    lams = [365, 405, 436, 492, 546, 578]
    fs = [C / (l_ * 1e-9) for l_ in lams]
    vs = [round((H * f_ / E - phi) * rng.uniform(0.98, 1.02), 2) for f_ in fs]
    pts = [(f_ / 1e14, v_) for f_, v_ in zip(fs, vs) if v_ > 0.05]
    if len(pts) < 4:
        return None
    return dict(intro=f'Light from a mercury lamp with filters illuminates a photocell with a {mt} cathode. The stopping potential Vₛ is measured for each frequency f. Theory: eVₛ = hf − Φ.',
                xname='f', xunit='10¹⁴ Hz', yname='Vₛ', yunit='V', xs=[p[0] for p in pts], ys=[p[1] for p in pts], xfmt=lambda a: f'{a:.2f}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: a * 1e14, plot_y=lambda b: b, plot_label='Vₛ (y) against f in Hz (x)', what='the Planck constant', what_short='h',
                gunit='V s', deduce=lambda m_, b_: (m_ * E, 'J s', 'h = e × gradient'))


gradient_fit('ch09-st1', _pe_spec)


@R.add('ch09-st1', 'C4', (3, 5), 'multi_step')
def c4_pe_graph(rng, slot):
    mt, phi = pick(rng, METALS)
    f1 = rng.choice([7.0, 8.0, 9.0]) * 1e14
    f2 = f1 + rng.choice([2.0, 3.0, 4.0]) * 1e14
    V1, V2 = H * f1 / E - phi, H * f2 / E - phi
    if V1 <= 0:
        return None
    return num(f'In a photoelectric experiment on an unknown metal, the stopping potential is {sf(V1, 3)} V for light of frequency {q(f1, "Hz")} and {sf(V2, 3)} V for {q(f2, "Hz")}. (a) Determine a value for the Planck constant. (b) Determine the work function of the metal in eV and suggest its identity. (c) Sketch the graph of Vₛ against f and state the significance of its intercepts. (d) Explain why a graph of photocurrent against intensity at constant frequency is a straight line through the origin.',
               f'(a) h = {q(E * (V2 - V1) / (f2 - f1), "J s")}; (b) Φ = {sf(phi, 2)} eV ({mt}); (c) f-intercept = threshold frequency {q(phi * EV / H, "Hz")}, V-intercept = −Φ/e; (d) number of photons ∝ intensity, each releasing at most one electron',
               f'(a) gradient = ΔVₛ/Δf = {q((V2 - V1) / (f2 - f1), "V s")} (M1); h = e × gradient = {q(E * (V2 - V1) / (f2 - f1), "J s")} (A1). (b) Φ = hf₁ − eV₁ = {sf(phi, 2)} eV (M1 A1). (c) intercepts identified (R1). (d) photon model (R1).', 6, 'multi_step', 'G5')


R.facts('ch09-st2', F(
    terms=[('de Broglie wavelength', 'the wavelength λ = h/p associated with a particle of momentum p'),
           ('wave–particle duality', 'the idea that matter and radiation both show wave-like and particle-like properties depending on the experiment'),
           ('electron diffraction', 'the diffraction of an electron beam by the regular array of atoms in a crystal, demonstrating the wave nature of electrons')],
    facts=[('The de Broglie wavelength of a particle is', 'inversely proportional to its momentum', ['proportional to its momentum', 'proportional to its kinetic energy', 'independent of its speed'], 'λ = h/p.'),
           ('Electrons accelerated through a larger potential difference have', 'a shorter de Broglie wavelength', ['a longer de Broglie wavelength', 'the same wavelength', 'no wavelength'], 'More momentum.'),
           ('Which experiment first confirmed the wave nature of electrons?', 'Davisson and Germer’s scattering of electrons from a nickel crystal', ['Millikan’s oil drop', 'Geiger and Marsden’s gold foil', 'Thomson’s e/m experiment'], '1927 diffraction maxima matched λ = h/p.'),
           ('Why are the wave properties of a cricket ball never observed?', 'its de Broglie wavelength is far too small compared with any aperture', ['it has no momentum', 'it is not charged', 'it travels too slowly'], 'λ ~ 10⁻³⁴ m.')],
    why=[('Explain why electron diffraction through graphite produces rings rather than spots.', 'Graphite powder (or polycrystalline film) contains many tiny crystals in random orientations; for each lattice spacing, diffraction at the Bragg angle occurs in all directions around the beam, forming cones that hit the screen as rings.'),
         ('Explain why electron microscopes can resolve much finer detail than optical microscopes.', 'Electrons accelerated through kilovolts have de Broglie wavelengths of ~10⁻¹¹ m, far smaller than visible light (~5 × 10⁻⁷ m); resolution is limited by diffraction, which is smaller for shorter wavelengths.'),
         ('Explain what happens to the diffraction rings when the accelerating voltage in an electron-diffraction tube is increased.', 'The electrons gain momentum, so their wavelength λ = h/p decreases; diffraction angles (sin θ ∝ λ) decrease, so the rings become smaller.')],
    contrast=[('the de Broglie wavelength of an electron', 'the wavelength of a photon of the same energy', 'For an electron λ = h/√(2mEₖ); for a photon λ = hc/E. For the same (non-relativistic) energy the electron’s wavelength is much shorter because its momentum is much larger.')],
    misc=[('Only electrons have a de Broglie wavelength.', 'All matter has a de Broglie wavelength λ = h/p; diffraction has been observed for neutrons, atoms and even large molecules (C₆₀).'),
          ('Doubling the speed of an electron doubles its de Broglie wavelength.', 'λ = h/(mv): doubling v halves λ.')],
    evaluate=[('Wave–particle duality means electrons are sometimes waves and sometimes particles.', ['some experiments show interference (wave), others localised detection (particle)'], ['electrons are quantum objects described by wavefunctions; "wave" and "particle" are classical models', 'complementarity: each experiment reveals one aspect'], 'Electrons are neither classical waves nor particles; both models are partial descriptions of quantum behaviour (NOS: models and their limits).')],
))


@R.add('ch09-st2', 'C3', (1, 5), 'numerical')
def c3_debroglie(rng, slot):
    frame = rng.randrange(5)
    if frame == 0:
        V = rng.choice([50, 100, 150, 500, 1000, 3000, 5000])
        p = math.sqrt(2 * ME * E * V)
        lam = H / p
        return num(f'An electron is accelerated from rest through a p.d. of {V} V. Calculate its de Broglie wavelength.',
                   q(lam, 'm'), f'p = √(2meV) = {q(p, "kg m s⁻¹")} (M1 A1); λ = h/p = {q(lam, "m")} (A1).', 3)
    if frame == 1:
        obj = pick(rng, [('a tennis ball', 0.058, 50), ('a 70 kg sprinter', 70, 10), ('a bullet', 0.010, 400), ('a dust grain', 1e-12, 0.01)])
        lam = H / (obj[1] * obj[2])
        return num(f'Calculate the de Broglie wavelength of {obj[0]} of mass {q(obj[1], "kg")} moving at {sf(obj[2], 2)} m s⁻¹, and comment on whether its wave nature could be observed.',
                   f'{q(lam, "m")}; far too small to observe', f'λ = h/(mv) (M1) = {q(lam, "m")} (A1); much smaller than any aperture or atom, so no observable diffraction (R1).', 3)
    if frame == 2:
        part = pick(rng, [('a neutron', MN), ('a proton', MP), ('an electron', ME)])
        v = rng.choice([2.0e3, 5.0e3, 1.0e5, 2.2e6])
        return num(f'Calculate the de Broglie wavelength of {part[0]} travelling at {q(v, "m s⁻¹")}.', q(H / (part[1] * v), 'm'),
                   f'λ = h/(mv) (M1) = {q(H / (part[1] * v), "m")} (A1).', 2)
    if frame == 3:
        lam = rng.choice([0.10, 0.15, 0.20, 0.25]) * 1e-9
        p = H / lam
        Ek = p * p / (2 * ME)
        return num(f'In an electron-diffraction experiment the electrons need a de Broglie wavelength of {q(lam * 1e9, "nm")}, comparable to atomic spacing. Determine the accelerating voltage required.',
                   q(Ek / E, 'V'), f'p = h/λ = {q(p, "kg m s⁻¹")} (M1); Eₖ = p²/2m = {q(Ek, "J")} (A1); V = Eₖ/e = {q(Ek / E, "V")} (A1).', 3)
    V = rng.choice([2000, 3000, 4000, 5000])
    d = rng.choice([0.123, 0.213]) * 1e-9
    lam = H / math.sqrt(2 * ME * E * V)
    th = asind(lam / d)
    return num(f'Electrons accelerated through {V} V are diffracted by graphite with an atomic plane spacing of {q(d * 1e9, "nm")}. Using d sin θ = λ, calculate the angle θ of the first diffraction maximum.',
               deg(th), f'λ = h/√(2meV) = {q(lam, "m")} (M1 A1); sin θ = λ/d → θ = {deg(th)} (A1).', 3)


@R.add('ch09-st2', 'C3', (1, 4), 'mcq')
def c3_db_mcq(rng, slot):
    V = rng.choice([100, 400, 900, 1600])
    lam = H / math.sqrt(2 * ME * E * V)
    k = rng.choice([4, 9, 16])
    return nmcq(rng, f'Electrons accelerated through {V} V have a de Broglie wavelength λ = {q(lam, "m")}. What is their wavelength if the accelerating voltage is multiplied by {k}?', lam / math.sqrt(k),
                [lam / k, lam * math.sqrt(k), lam * k], 'm', f'λ ∝ 1/√V: λ/√{k} = {q(lam / math.sqrt(k), "m")}.', extra=False)


R.mcqs('ch09-st2', 'C2', (1, 4), [
    ('A proton and an electron have the same de Broglie wavelength. They have the same', 'momentum', ['speed', 'kinetic energy', 'mass'], 'λ = h/p.'),
    ('A proton and an electron have the same kinetic energy. Which has the longer de Broglie wavelength?', 'the electron', ['the proton', 'they are equal', 'it depends on the charge'], 'p = √(2mEₖ) is smaller for the electron.'),
    ('Electron diffraction is evidence that', 'electrons have wave properties', ['electrons are charged', 'electrons have mass', 'atoms are mostly empty'], 'Diffraction is a wave phenomenon.'),
])

R.static('ch09-st2', 'C4', (3, 5), [
    ('In an electron-diffraction tube, electrons accelerated through 4.0 kV pass through a graphite film and produce rings on a screen 0.14 m away. (a) Calculate the de Broglie wavelength. (b) The inner ring has radius 11 mm; using sin θ ≈ r/(2L) for the Bragg geometry, estimate the atomic spacing. (c) Predict and explain the change in ring size at 6.0 kV. (d) Explain how this experiment supports de Broglie’s hypothesis.',
     '(a) λ = h/√(2meV) = 1.94 × 10⁻¹¹ m; (b) θ ≈ 0.011/0.28 = 0.0393 rad, d = λ/(2 sin θ) ≈ 2.5 × 10⁻¹⁰ m; (c) λ ∝ 1/√V, so the rings shrink by a factor √(4/6) = 0.82 (radius ≈ 9.0 mm); (d) the rings are a diffraction pattern whose size changes with V exactly as λ = h/p predicts.',
     'λ (M1 A1); spacing estimate (M1 A1); prediction with factor (R1); link between observed scaling and λ = h/p (R1).', 6),
], type='multi_step', marks=6)


R.facts('ch09-st3', F(
    terms=[('Compton scattering', 'the scattering of an X-ray or gamma-ray photon by a free electron, in which the photon loses energy and its wavelength increases'),
           ('Compton wavelength', 'the quantity h/(mₑc) = 2.43 × 10⁻¹² m, the scale of the wavelength shift in Compton scattering'),
           ('photon momentum', 'the momentum of a photon, p = h/λ = E/c')],
    facts=[('In Compton scattering, the scattered photon has', 'a longer wavelength than the incident photon', ['a shorter wavelength', 'the same wavelength', 'a higher frequency'], 'It transfers energy to the electron.'),
           ('The Compton shift is greatest for a scattering angle of', '180°', ['0°', '90°', '45°'], '1 − cos θ is maximum at 180°.'),
           ('Compton scattering provides evidence that photons', 'carry momentum', ['have mass at rest', 'travel slower in matter', 'are charged'], 'Momentum conservation in a particle collision fits the data.'),
           ('The Compton wavelength shift does not depend on', 'the wavelength of the incident photon', ['the scattering angle', 'the electron mass', 'the Planck constant'], 'Δλ = (h/mₑc)(1 − cos θ).')],
    why=[('Explain why the Compton effect is noticeable for X-rays but not for visible light.', 'The shift is at most ~5 pm; for X-rays of λ ~ 10⁻¹¹ m this is a large fractional change, but for visible light (~5 × 10⁻⁷ m) it is a fractional change of ~10⁻⁵, too small to notice.'),
         ('Explain why the Compton effect could not be explained by the classical wave model.', 'Classically, an electromagnetic wave would make electrons oscillate at the incident frequency and re-radiate at the same frequency; the observed angle-dependent increase in wavelength requires a particle-like collision with photon momentum h/λ.'),
         ('Explain why the scattered electron recoils with kinetic energy in Compton scattering.', 'Energy and momentum are conserved in the photon–electron collision; the photon’s energy decreases (λ increases), and the difference appears as the electron’s kinetic energy.')],
    contrast=[('the photoelectric effect', 'Compton scattering', 'In the photoelectric effect a photon is completely absorbed and its energy frees a bound electron; in Compton scattering the photon is scattered by an essentially free electron, losing only part of its energy and continuing with a longer wavelength.')],
    misc=[('In Compton scattering, the photon slows down.', 'Photons always travel at c; the photon’s energy and frequency decrease, so its wavelength increases.'),
          ('The Compton shift increases with the energy of the incident photon.', 'Δλ = (h/mₑc)(1 − cos θ) depends only on angle; the fractional shift Δλ/λ is larger for higher-energy photons.')],
    evaluate=[('Compton’s experiment settled the debate about the nature of light.', ['showed photons have momentum h/λ, convincing many physicists of the photon model'], ['wave effects (diffraction) still needed a wave model', 'quantum electrodynamics later gave a unified description', 'scientific debates are rarely settled by one experiment (NOS)'], 'It was decisive in establishing photon momentum, but the full picture required wave–particle duality and later quantum theory.')],
))


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def c3_compton(rng, slot):
    lc = H / (ME * C)
    th = rng.choice([30, 45, 60, 90, 120, 135, 180])
    dl = lc * (1 - cosd(th))
    frame = rng.randrange(4)
    if frame == 0:
        return num(f'X-ray photons are Compton-scattered by free electrons through {th}°. Calculate the change in wavelength.',
                   q(dl, 'm'), f'Δλ = (h/mₑc)(1 − cos θ) (M1) = 2.43 × 10⁻¹² × (1 − cos {th}°) = {q(dl, "m")} (A1).', 2)
    lam = rng.choice([7.1, 10.0, 20.0, 50.0, 71.0]) * 1e-12
    lam2 = lam + dl
    if frame == 1:
        return num(f'X-rays of wavelength {q(lam, "m")} are scattered through {th}° by free electrons. Calculate the wavelength of the scattered X-rays and the kinetic energy gained by the electron.',
                   f'λ′ = {q(lam2, "m")}; Eₖ = {q(H * C / lam - H * C / lam2, "J")}', f'Δλ = {q(dl, "m")} (M1); λ′ = {q(lam2, "m")} (A1); Eₖ = hc/λ − hc/λ′ (M1) = {q(H * C / lam - H * C / lam2, "J")} (A1).', 4, 'multi_step')
    if frame == 2:
        p = H / lam
        return num(f'Calculate the momentum of an X-ray photon of wavelength {q(lam, "m")} and its energy in keV.', f'p = {q(p, "kg m s⁻¹")}; E = {q(H * C / lam / EV / 1e3, "keV")}',
                   f'p = h/λ (M1) = {q(p, "kg m s⁻¹")} (A1); E = pc = {q(H * C / lam / EV / 1e3, "keV")} (A1).', 3)
    E_kev = rng.choice([100, 300, 662, 1000])
    lam0 = H * C / (E_kev * 1e3 * EV)
    lam1 = lam0 + 2 * lc
    E1 = H * C / lam1 / EV / 1e3
    return num(f'A {E_kev} keV gamma-ray photon is back-scattered (θ = 180°) by a free electron. Calculate the energy of the scattered photon.',
               q(E1, 'keV'), f'λ = hc/E = {q(lam0, "m")} (A1); Δλ = 2h/(mₑc) = {q(2 * lc, "m")} (M1); E′ = hc/λ′ = {q(E1, "keV")} (A1).', 3)


@R.add('ch09-st3', 'C3', (1, 4), 'mcq')
def c3_compton_mcq(rng, slot):
    th = rng.choice([60, 90, 120, 180])
    dl = H / (ME * C) * (1 - cosd(th))
    return nmcq(rng, f'What is the Compton shift for photons scattered by free electrons through {th}°?', dl,
                [H / (ME * C) * cosd(th) if th != 90 else H / (ME * C) / 2, H / (MP * C) * (1 - cosd(th)), H / (ME * C) * (1 + cosd(th)) if th not in (180,) else H / (ME * C)], 'm',
                f'Δλ = (h/mₑc)(1 − cos {th}°) = {q(dl, "m")}.', extra=True)


R.mcqs('ch09-st3', 'C2', (1, 4), [
    ('X-rays scattered at 90° by a block of carbon show two wavelengths: the incident one and a longer one. The unshifted component comes from', 'scattering by tightly bound electrons (effectively the whole atom)', ['free electrons', 'the photoelectric effect', 'protons in the nuclei'], 'Recoil of the whole atom gives a negligible shift.'),
    ('If the scattering electron were replaced by a proton, the maximum Compton shift would be', 'about 1800 times smaller', ['about 1800 times larger', 'the same', 'zero'], 'Δλ ∝ 1/m.'),
    ('In Compton scattering through 180°, the recoiling electron moves', 'forward, in the original direction of the photon', ['backwards with the photon', 'at 90°', 'not at all'], 'Momentum conservation.'),
])

R.static('ch09-st3', 'C4', (3, 5), [
    ('Discuss how Compton scattering and the photoelectric effect together support the photon model of electromagnetic radiation, explaining what each experiment shows about photon energy and photon momentum.',
     'The photoelectric effect shows that energy is absorbed in quanta E = hf (threshold frequency, Eₖ independent of intensity, instant emission). Compton scattering shows photons also carry momentum p = h/λ: the angle-dependent wavelength shift Δλ = (h/mₑc)(1 − cos θ) follows exactly from conserving energy and momentum in a photon–electron collision. Together they show light interacts as particles with both energy and momentum, while interference still requires wave behaviour.',
     'Photoelectric evidence for E = hf (R1 R1); Compton evidence for p = h/λ (R1 R1); conservation laws used (R1); duality comment (A1).', 6),
], type='multi_step', marks=6)

linearise('ch09-st3', [
    ('Δλ = (h/mₑc)(1 − cos θ) for X-rays scattered at different angles', 'Δλ', '(1 − cos θ)', 'h/(mₑc), the Compton wavelength', 'A straight line through the origin confirms the Compton formula.'),
])


# =============================================================================================
# ch10 E.3 Radioactive decay
# =============================================================================================
EL = {1: 'H', 2: 'He', 6: 'C', 7: 'N', 8: 'O', 11: 'Na', 12: 'Mg', 13: 'Al', 15: 'P', 16: 'S', 19: 'K', 20: 'Ca', 26: 'Fe', 27: 'Co', 28: 'Ni', 36: 'Kr', 37: 'Rb',
      38: 'Sr', 39: 'Y', 40: 'Zr', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra',
      89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 9: 'F', 10: 'Ne', 14: 'Si', 5: 'B', 3: 'Li', 4: 'Be', 18: 'Ar', 52: 'Te'}
DECAYS = [('U', 92, 238, 'α'), ('Ra', 88, 226, 'α'), ('Po', 84, 210, 'α'), ('Am', 95, 241, 'α'), ('Pu', 94, 239, 'α'), ('Rn', 86, 222, 'α'), ('Th', 90, 232, 'α'),
          ('C', 6, 14, 'β⁻'), ('Sr', 38, 90, 'β⁻'), ('I', 53, 131, 'β⁻'), ('Cs', 55, 137, 'β⁻'), ('Co', 27, 60, 'β⁻'), ('P', 15, 32, 'β⁻'), ('K', 19, 40, 'β⁻'),
          ('Na', 11, 22, 'β⁺'), ('F', 9, 18, 'β⁺'), ('C', 6, 11, 'β⁺'), ('O', 8, 15, 'β⁺')]


def nucl(sym, Z, A):
    return f'{sup(A)}{sym} (Z = {Z})'


def daughter(Z, A, mode):
    if mode == 'α':
        return Z - 2, A - 4
    if mode == 'β⁻':
        return Z + 1, A
    return Z - 1, A


R.facts('ch10-st1', F(
    terms=[('alpha particle', 'a helium-4 nucleus (two protons and two neutrons) emitted from an unstable nucleus'),
           ('beta-minus decay', 'the decay of a neutron in the nucleus into a proton, an electron (emitted) and an electron antineutrino'),
           ('beta-plus decay', 'the decay of a proton in the nucleus into a neutron, a positron (emitted) and an electron neutrino'),
           ('gamma ray', 'a high-energy photon emitted when a nucleus drops from an excited state to a lower energy state')],
    facts=[('In alpha decay, the proton number and nucleon number change by', '−2 and −4', ['−4 and −2', '+1 and 0', '−1 and 0'], 'An ⁴₂He nucleus is lost.'),
           ('In β⁻ decay, which particles are emitted?', 'an electron and an electron antineutrino', ['a positron and a neutrino', 'an electron and a neutrino', 'a helium nucleus and a photon'], 'n → p + e⁻ + ν̄ₑ.'),
           ('The continuous energy spectrum of beta particles led Pauli to propose', 'the neutrino (antineutrino)', ['the positron', 'the neutron', 'the gamma photon'], 'A third particle shares the energy.'),
           ('Gamma emission changes', 'neither Z nor A', ['Z by −1', 'A by −4', 'Z by +1'], 'Only the nuclear energy state changes.')],
    why=[('Explain why the energy spectrum of beta particles is continuous while that of alpha particles is discrete.', 'In alpha decay there are two products, so momentum and energy conservation fix each one’s kinetic energy; in beta decay the energy is shared among three particles (daughter, electron and antineutrino), so the electron can have any energy up to a maximum.'),
         ('Explain why gamma emission often follows alpha or beta decay.', 'The daughter nucleus is frequently left in an excited nuclear energy state; it then drops to its ground state by emitting a gamma photon of discrete energy.'),
         ('Explain why charge and nucleon number are conserved in nuclear equations, and how this helps to balance them.', 'Charge and baryon (nucleon) number are conserved in all nuclear reactions, so the totals of Z and A must be equal on both sides; unknown products are found from the differences.')],
    contrast=[('β⁻ decay', 'β⁺ decay', 'β⁻: a neutron becomes a proton, emitting an electron and an antineutrino (Z increases by 1); β⁺: a proton becomes a neutron, emitting a positron and a neutrino (Z decreases by 1). A is unchanged in both.')],
    misc=[('A beta-minus particle is an electron that was orbiting the atom.', 'The β⁻ electron is created in the nucleus when a neutron changes into a proton; it is not an orbital electron.'),
          ('In alpha decay the nucleon number decreases by 2.', 'It decreases by 4 (two protons and two neutrons); the proton number decreases by 2.'),
          ('Gamma decay changes the element.', 'Gamma emission does not change Z or A; the element is unchanged.')],
    evaluate=[('The neutrino was accepted by physicists as soon as Pauli proposed it.', ['it rescued energy and momentum conservation in beta decay'], ['Pauli himself called it a "desperate remedy"; some (e.g. Bohr) considered abandoning conservation of energy', 'it was not detected until Cowan and Reines in 1956'], 'Acceptance was gradual; the hypothesis was supported by theory (Fermi) and later confirmed by detection – an example of a prediction preceding evidence (NOS).')],
))


@R.add('ch10-st1', 'C3', (1, 5), 'numerical')
def c3_decay_eq(rng, slot):
    sym, Z, A, mode = pick(rng, DECAYS)
    Zd, Ad = daughter(Z, A, mode)
    ds = EL.get(Zd, 'X')
    frame = rng.randrange(3)
    part = {'α': '⁴₂He', 'β⁻': '⁰₋₁e + ν̄ₑ', 'β⁺': '⁰₊₁e + νₑ'}[mode]
    if frame == 0:
        return num(f'{sup(A)}{sym} (Z = {Z}) decays by {mode} emission. Write the nuclear equation and identify the daughter nuclide.',
                   f'{sup(A)}{sym} → {sup(Ad)}{ds} + {part}; daughter {ds}-{Ad} (Z = {Zd})', f'Correct particle(s) including the (anti)neutrino for β (A1); A and Z balanced: A {A} = {Ad} + {A - Ad}, Z {Z} = {Zd} + {Z - Zd} (M1); daughter {ds}-{Ad} (A1).', 3)
    if frame == 1:
        return num(f'A nucleus decays to {sup(Ad)}{ds} (Z = {Zd}) by {mode} emission. Identify the parent nucleus (proton number and nucleon number).',
                   f'{sym}-{A} (Z = {Z}, A = {A})', f'Reverse the changes for {mode} decay (M1): Z = {Z}, A = {A}, i.e. {sym}-{A} (A1).', 2)
    na = rng.randint(2, 8)
    nb = rng.randint(1, 6)
    Z0, A0 = rng.choice([(92, 238), (90, 232), (92, 235), (94, 239)])
    Zf, Af = Z0 - 2 * na + nb, A0 - 4 * na
    return num(f'A decay chain starts at {sup(A0)}{EL[Z0]} (Z = {Z0}) and ends at a nuclide with Z = {Zf} and A = {Af}. Determine the number of α and β⁻ decays in the chain.',
               f'{na} α and {nb} β⁻', f'A changes only in α decay: ({A0} − {Af})/4 = {na} α (M1 A1); Z: {Z0} − 2×{na} + n_β = {Zf} → n_β = {nb} (M1 A1).', 4, 'multi_step')


@R.add('ch10-st1', 'C3', (1, 4), 'mcq')
def c3_decay_mcq(rng, slot):
    sym, Z, A, mode = pick(rng, DECAYS)
    Zd, Ad = daughter(Z, A, mode)
    right = f'Z = {Zd}, A = {Ad}'
    wr = [f'Z = {Z - 4}, A = {A - 2}', f'Z = {Z + 1}, A = {A}', f'Z = {Z - 1}, A = {A}', f'Z = {Z - 2}, A = {A - 4}', f'Z = {Z}, A = {A - 1}']
    wr = [w for w in wr if w != right]
    return mcq(rng, f'{sup(A)}{sym} (Z = {Z}) undergoes {mode} decay. What are the proton number and nucleon number of the daughter?', right, wr[:3],
               f'{mode} decay: {"Z − 2, A − 4" if mode == "α" else "Z + 1, A unchanged" if mode == "β⁻" else "Z − 1, A unchanged"}.')


R.mcqs('ch10-st1', 'C2', (1, 4), [
    ('Which quark change occurs in β⁻ decay?', 'a down quark changes to an up quark', ['an up quark changes to a down quark', 'a strange quark changes to an up quark', 'no quark changes'], 'udd (n) → uud (p).'),
    ('A nucleus emits an α particle and then two β⁻ particles. The final nuclide is', 'an isotope of the original element', ['the same nuclide', 'an element two places lower', 'an element two places higher'], 'Z: −2 + 2 = 0; A: −4.'),
    ('Which interaction is responsible for beta decay?', 'the weak interaction', ['the strong interaction', 'the electromagnetic interaction', 'gravity'], 'Weak force changes quark flavour.'),
])

R.static('ch10-st1', 'C4', (3, 5), [
    ('Potassium-40 (Z = 19) can decay either by β⁻ emission (89 %) or by electron capture (11 %). (a) Write equations for both decays. (b) Explain why the β⁻ electrons have a continuous energy spectrum while the electron-capture neutrinos have a single energy. (c) Explain how this decay is used to date volcanic rocks (the K–Ar method).',
     '(a) ⁴⁰₁₉K → ⁴⁰₂₀Ca + ⁰₋₁e + ν̄ₑ; ⁴⁰₁₉K + ⁰₋₁e → ⁴⁰₁₈Ar + νₑ; (b) three products share the energy in β⁻ decay, two (Ar recoil and neutrino) in capture, so the neutrino energy is fixed; (c) argon gas escapes molten lava but is trapped once rock solidifies; the ratio of ⁴⁰Ar to ⁴⁰K, with the known half-life (1.25 × 10⁹ y) and branching ratio, gives the time since solidification.',
     'Both equations balanced (A1 A1); three-body vs two-body argument (R1); argon trapped after solidification (R1); age from ratio and half-life (R1).'),
], type='multi_step', marks=5)


ISOTOPES = [('iodine-131', 8.02, 'days'), ('cobalt-60', 5.27, 'years'), ('carbon-14', 5730, 'years'), ('strontium-90', 28.8, 'years'), ('technetium-99m', 6.01, 'hours'),
            ('radon-222', 3.82, 'days'), ('caesium-137', 30.2, 'years'), ('phosphorus-32', 14.3, 'days'), ('fluorine-18', 110, 'minutes'), ('polonium-210', 138, 'days')]

R.facts('ch10-st2', F(
    terms=[('half-life', 'the time taken for the number of undecayed nuclei (or the activity) of a sample to fall to half its initial value'),
           ('activity', 'the number of nuclei decaying per second in a sample, A = λN, measured in becquerels (Bq)'),
           ('decay constant', 'the probability per unit time that a nucleus will decay, λ = ln 2/T½'),
           ('random decay', 'the property that it is impossible to predict when a particular nucleus will decay, only the probability of decay in a given time')],
    facts=[('After three half-lives, the fraction of the original nuclei remaining is', '1/8', ['1/3', '1/6', '1/9'], '(1/2)³.'),
           ('Radioactive decay is described as spontaneous because', 'it is not affected by external conditions such as temperature or pressure', ['it happens quickly', 'it occurs only in heavy nuclei', 'it can be predicted for each nucleus'], 'Decay is a nuclear process unaffected by chemistry or environment.'),
           ('The unit of activity, the becquerel, is', 'one decay per second', ['one decay per minute', 'one joule per kilogram', 'one gray'], '1 Bq = 1 s⁻¹.'),
           ('The relationship between decay constant and half-life is', 'λT½ = ln 2', ['λ = T½ ln 2', 'λT½ = 1/2', 'λ = 2T½'], 'From N = N₀e^(−λt).')],
    why=[('Explain why the count rate from a radioactive source fluctuates even though the half-life is constant.', 'Decay is random: the number of decays in each counting interval varies statistically about the mean (roughly ±√N), so individual readings fluctuate; the half-life describes the average behaviour of very large numbers of nuclei.'),
         ('Explain why background radiation must be measured and subtracted when determining half-life.', 'The detector also records counts from cosmic rays and natural radioactivity; these do not decay with the sample, so if not subtracted they make the measured count rate fall less steeply, overestimating the half-life.'),
         ('Explain why a radioisotope used as a medical tracer should have a half-life of a few hours.', 'Long enough for preparation, injection and imaging, but short enough that the activity (and dose to the patient) falls quickly afterwards; e.g. technetium-99m with T½ = 6 h.')],
    contrast=[('half-life', 'decay constant', 'Half-life is the time for half the nuclei to decay; the decay constant is the probability per unit time of decay for one nucleus; they are related by λ = ln 2/T½.'),
              ('activity', 'count rate', 'Activity is the actual number of decays per second in the source; count rate is the number detected per second, which is smaller because the detector intercepts only some radiation and includes background.')],
    misc=[('After two half-lives all of the sample has decayed.', 'After two half-lives a quarter of the original nuclei remain; in principle decay never reaches zero.'),
          ('Heating a radioactive source shortens its half-life.', 'Half-life is independent of temperature and chemical state.'),
          ('The half-life is half the time it takes for the whole sample to decay.', 'The whole sample never decays completely in a finite time; the half-life is the time for the number of nuclei to halve.')],
    evaluate=[('Radiocarbon dating can be used to date any ancient object.', ['excellent for organic material up to ~50 000 years', 'calibrated against tree rings'], ['only for once-living material containing carbon', 'too few ¹⁴C nuclei remain after ~10 half-lives', 'atmospheric ¹⁴C levels have varied (calibration needed)', 'contamination with modern carbon'], 'Powerful but limited to organic materials younger than about 50 000 years, with calibration; other isotopes are needed for rocks.')],
))


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def c3_halflife(rng, slot):
    iso, T, unit = pick(rng, ISOTOPES)
    frame = rng.randrange(6)
    if frame == 0:
        n = rng.choice([2, 3, 4, 5])
        A0 = rng.choice([800, 1200, 1600, 3200, 6400])
        return num(f'A sample of {iso} (half-life {T} {unit}) has an initial activity of {A0} Bq. Calculate its activity after {sf(n * T, 3)} {unit}.',
                   q(A0 / 2 ** n, 'Bq'), f'{sf(n * T, 3)} {unit} = {n} half-lives (M1); A = {A0}/2^{n} = {q(A0 / 2 ** n, "Bq")} (A1).', 2)
    if frame == 1:
        t = T * rng.uniform(0.3, 4.5)
        f = 0.5 ** (t / T)
        return num(f'Calculate the fraction of {iso} nuclei (half-life {T} {unit}) remaining after {sf(t, 3)} {unit}.',
                   sf(f, 3), f'N/N₀ = (1/2)^(t/T½) (M1) = (1/2)^({sf(t / T, 3)}) = {sf(f, 3)} (A1).', 2)
    if frame == 2:
        lam = math.log(2) / T
        return num(f'The half-life of {iso} is {T} {unit}. Calculate its decay constant in {unit}⁻¹ and in s⁻¹.',
                   f'{sf(lam, 3)} {unit}⁻¹ = {q(lam / {"days": 86400, "years": 3.156e7, "hours": 3600, "minutes": 60}[unit], "s⁻¹")}',
                   f'λ = ln 2/T½ (M1) = {sf(lam, 3)} {unit}⁻¹ (A1); converted = {q(lam / {"days": 86400, "years": 3.156e7, "hours": 3600, "minutes": 60}[unit], "s⁻¹")} (A1).', 3)
    if frame == 3:
        frac_ = rng.choice([0.40, 0.25, 0.60, 0.15, 0.70])
        age = T * math.log(1 / frac_) / math.log(2) if iso == 'carbon-14' else None
        T14 = 5730
        age = T14 * math.log(1 / frac_) / math.log(2)
        return num(f'A wooden artefact has a carbon-14 activity per gram that is {int(frac_ * 100)} % of that of living wood. Taking the half-life of carbon-14 as 5730 years, estimate the age of the artefact.',
                   q(age, 'years'), f'A/A₀ = (1/2)^(t/T½) = {frac_} (M1); t = T½ × ln(1/{frac_})/ln 2 (M1) = {q(age, "years")} (A1).', 3)
    if frame == 4:
        N = rng.choice([2.0, 5.0, 8.0]) * 10 ** rng.choice([15, 18, 20])
        Ts = T * {"days": 86400, "years": 3.156e7, "hours": 3600, "minutes": 60}[unit]
        Act = N * math.log(2) / Ts
        return num(f'A source contains {q(N, "")} nuclei of {iso} (half-life {T} {unit}). Calculate its activity.',
                   q(Act, 'Bq'), f'λ = ln 2/T½ = {q(math.log(2) / Ts, "s⁻¹")} (M1); A = λN = {q(Act, "Bq")} (A1).', 2)
    bg = rng.choice([20, 25, 30, 40])
    c0 = rng.choice([800, 1000, 1200])
    n = rng.choice([2, 3])
    later = (c0 - bg) / 2 ** n + bg
    return num(f'A detector near a source records {c0} counts per minute; the background count is {bg} counts per minute. After {n * 10} hours the reading is {sf(later, 3)} counts per minute. Determine the half-life of the source.',
               q(10, 'hours'), f'Corrected: {c0 - bg} → {sf(later - bg, 3)} counts min⁻¹ (M1); ratio 1/{2 ** n} = {n} half-lives (M1); T½ = {n * 10}/{n} = 10 hours (A1).', 3)


@R.add('ch10-st2', 'C3', (1, 4), 'mcq')
def c3_hl_mcq(rng, slot):
    T = rng.choice([2, 3, 5, 8, 10])
    n = rng.choice([2, 3, 4])
    m0 = rng.choice([80, 96, 120, 160, 240])
    m1 = m0 / 2 ** n
    return nmcq(rng, f'A sample contains {m0} mg of a radioisotope with a half-life of {T} days. What mass of the isotope remains after {n * T} days?', m1,
                [m0 / (2 * n), m0 - m0 / 2 ** n, m0 / 2 ** (n + 1)], 'mg', f'{n} half-lives: {m0}/2^{n} = {q(m1, "mg")}.', extra=False)


R.mcqs('ch10-st2', 'C2', (1, 4), [
    ('Two samples of the same isotope have masses 2 g and 8 g. Compared with the small sample, the large sample has', 'four times the activity and the same half-life', ['the same activity and four times the half-life', 'four times the half-life', 'a quarter of the half-life'], 'A = λN; λ fixed for the isotope.'),
    ('A graph of ln(activity) against time for a pure radioisotope is', 'a straight line of gradient −λ', ['an exponential curve', 'a straight line through the origin', 'a horizontal line'], 'ln A = ln A₀ − λt.'),
    ('An isotope has a half-life of 10 minutes. The probability that a given nucleus decays in the next 10 minutes is', '0.5', ['1.0', '0.1', 'it depends on how long it has existed'], 'Decay has no memory.'),
])


def _hl_spec(rng):
    T = rng.choice([50, 80, 120, 150])
    A0 = rng.choice([400, 600, 900])
    ts = [0, 60, 120, 180, 240, 300]
    As = [round(A0 * 0.5 ** (t_ / T) * rng.uniform(0.96, 1.04)) for t_ in ts]
    return dict(intro='The background-corrected count rate C from a short-lived source is recorded every 60 s. Theory: C = C₀e^(−λt).',
                xname='t', xunit='s', yname='C', yunit='counts s⁻¹', xs=ts, ys=As, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b}',
                plot_x=lambda a: a, plot_y=lambda b: math.log(b), plot_label='ln C (y) against t (x)', what='the half-life of the source', what_short='the half-life',
                gunit='s⁻¹', deduce=lambda m_, b_: (math.log(2) / -m_, 's', 'T½ = ln 2/|gradient|'))


gradient_fit('ch10-st2', _hl_spec)


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step')
def c4_tracer(rng, slot):
    T = 6.01
    A0 = rng.choice([400, 500, 600]) * 1e6
    t1 = rng.choice([2, 3, 4])
    lam = math.log(2) / (T * 3600)
    N0 = A0 / lam
    At = A0 * 0.5 ** (t1 / T)
    tday = T * math.log(A0 / 1e6) / math.log(2)
    return num(f'A patient is injected with technetium-99m (half-life 6.01 h) of activity {sf(A0 / 1e6, 3)} MBq. (a) Calculate the decay constant in s⁻¹. (b) Calculate the number of Tc-99m nuclei injected. (c) Determine the activity when imaging begins {t1} h later. (d) Determine how long it takes for the activity to fall below 1 MBq. (e) Suggest why a gamma emitter with this half-life is suitable.',
               f'(a) {q(lam, "s⁻¹")}; (b) {q(N0, "")}; (c) {q(At / 1e6, "MBq")}; (d) {q(tday, "h")}; (e) gamma escapes the body for detection with little ionisation; short half-life limits dose',
               f'(a) λ = ln 2/(6.01 × 3600) (M1) = {q(lam, "s⁻¹")} (A1). (b) N = A/λ = {q(N0, "")} (A1). (c) A = A₀(1/2)^({t1}/6.01) = {q(At / 1e6, "MBq")} (A1). (d) t = 6.01 × log₂({sf(A0 / 1e6, 3)}) = {q(tday, "h")} (A1). (e) (R1).', 7, 'multi_step', 'G5')


@R.add('ch09-st2', 'C2', (2, 4), 'explain')
def c2_db_predict(rng, slot):
    ch = [('electrons are replaced by protons with the same speed', 'the de Broglie wavelength becomes about 1840 times smaller and the diffraction rings shrink almost to nothing', 'λ = h/(mv) and the proton mass is 1840 times larger'),
          ('the accelerating voltage of an electron beam is quadrupled', 'the de Broglie wavelength halves and the diffraction rings shrink', 'p ∝ √V, so λ = h/p ∝ 1/√V'),
          ('neutrons from a reactor are slowed (thermalised) before striking a crystal', 'their wavelength increases to about 10⁻¹⁰ m, comparable to atomic spacing, so they diffract strongly', 'lower speed → smaller momentum → longer λ'),
          ('an electron and a proton have the same kinetic energy', 'the electron has the longer wavelength', 'p = √(2mEₖ) is smaller for the smaller mass')]
    c, eff, why = pick(rng, ch)
    return dict(stem=f'Predict and explain what happens to the de Broglie wavelength and the observed diffraction when {c}.', answer=f'{eff[0].upper() + eff[1:]}, because {why}.',
                type='explain', marks=2, markingKey=f'{eff} (A1); {why} (R1).')


BEA = {('H', 1, 2): 1.112, ('H', 1, 3): 2.827, ('He', 2, 3): 2.573, ('He', 2, 4): 7.074, ('Li', 3, 7): 5.606, ('C', 6, 12): 7.680, ('N', 7, 14): 7.476,
       ('O', 8, 16): 7.976, ('Ne', 10, 20): 8.032, ('Fe', 26, 56): 8.790, ('Co', 27, 60): 8.747, ('Ni', 28, 62): 8.795, ('Sr', 38, 90): 8.696,
       ('Kr', 36, 92): 8.513, ('Ba', 56, 141): 8.326, ('Cs', 55, 137): 8.389, ('Xe', 54, 140): 8.290, ('Pb', 82, 208): 7.867, ('U', 92, 235): 7.591, ('U', 92, 238): 7.570}


def nuc_mass(sym, Z, A):
    return Z * MP_U + (A - Z) * MN_U - A * BEA[(sym, Z, A)] / UMEV


R.facts('ch10-st3', F(
    terms=[('mass defect', 'the difference between the total mass of the separated nucleons and the mass of the nucleus'),
           ('binding energy', 'the energy required to separate a nucleus completely into its individual protons and neutrons; equal to the mass defect × c²'),
           ('binding energy per nucleon', 'the binding energy of a nucleus divided by its number of nucleons; a measure of nuclear stability'),
           ('unified atomic mass unit', 'one-twelfth of the mass of a carbon-12 atom, 1 u = 1.661 × 10⁻²⁷ kg = 931.5 MeV c⁻²')],
    facts=[('Which nuclide has the highest binding energy per nucleon?', 'iron-56 (or nickel-62), about 8.8 MeV', ['uranium-235', 'helium-4', 'hydrogen-2'], 'The peak of the curve is near A ≈ 56–62.'),
           ('Energy is released in fission and fusion because', 'the products have a greater binding energy per nucleon than the reactants', ['mass is created', 'the products have less binding energy', 'nucleons are destroyed'], 'Total binding energy increases; mass decreases.'),
           ('1 u of mass is equivalent to', '931.5 MeV', ['1.661 MeV', '0.511 MeV', '938 MeV'], 'From E = mc².'),
           ('The mass of a nucleus is', 'less than the total mass of its separate nucleons', ['equal to the mass of its nucleons', 'greater than the mass of its nucleons', 'equal to A × 1 u exactly'], 'The difference is the mass defect.')],
    why=[('Explain why the binding energy per nucleon curve explains why both fission of heavy nuclei and fusion of light nuclei release energy.', 'The curve rises steeply for light nuclei to a peak near iron and falls slowly for heavy nuclei; fusing light nuclei or splitting heavy nuclei both move the products towards the peak, increasing total binding energy and releasing the difference as kinetic energy of the products.'),
         ('Explain why the mass of a nucleus is less than the sum of the masses of its nucleons.', 'When nucleons bind, energy (the binding energy) is released; by E = mc² the nucleus has less mass-energy than the separated nucleons by Δm = E_B/c².'),
         ('Explain why helium-4 is unusually stable compared with its neighbours.', 'It has a very high binding energy per nucleon (7.07 MeV) compared with nuclides of similar A (e.g. Li-7 at 5.6 MeV), because two protons and two neutrons form a tightly bound, filled arrangement; this is why α particles are emitted as a unit.')],
    contrast=[('binding energy', 'binding energy per nucleon', 'Binding energy is the total energy to separate all nucleons of a nucleus; per-nucleon binding energy divides this by A and is the better measure of stability for comparing nuclei.')],
    misc=[('Binding energy is the energy stored in a nucleus that is released when it forms bonds.', 'Binding energy is the energy needed to pull the nucleus apart; it is released when the nucleus forms, so bound nuclei have LESS energy (mass) than free nucleons.'),
          ('Uranium-238 is more stable than iron-56 because it has a larger total binding energy.', 'Stability is compared using binding energy per nucleon: Fe-56 ≈ 8.8 MeV vs U-238 ≈ 7.6 MeV.')],
    evaluate=[('Einstein’s equation E = mc² explains where the energy in nuclear reactions comes from.', ['mass defect × c² gives the energy released accurately'], ['the energy arises from the strong nuclear force doing work as nucleons rearrange; E = mc² is the accounting', 'mass–energy equivalence applies to chemical reactions too, but the changes are tiny'], 'E = mc² quantifies the release, while the underlying cause is the change in nuclear binding (strong force); both perspectives are needed.')],
))


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def c3_binding(rng, slot):
    (sym, Z, A), bea = pick(rng, list(BEA.items()))
    if A < 3:
        return None
    m = nuc_mass(sym, Z, A)
    dm = Z * MP_U + (A - Z) * MN_U - m
    BE = dm * UMEV
    frame = rng.randrange(3)
    if frame == 0:
        return num(f'The nuclear mass of {sup(A)}{sym} (Z = {Z}) is {m:.6f} u. Calculate (a) its mass defect, (b) its binding energy in MeV, (c) its binding energy per nucleon. (mₚ = 1.007276 u, mₙ = 1.008665 u)',
                   f'(a) {dm:.6f} u; (b) {sf(BE, 4)} MeV; (c) {sf(BE / A, 3)} MeV', f'Δm = {Z}mₚ + {A - Z}mₙ − m = {dm:.6f} u (M1 A1); E_B = Δm × 931.5 = {sf(BE, 4)} MeV (A1); per nucleon {sf(BE / A, 3)} MeV (A1).', 4)
    if frame == 1:
        return num(f'The binding energy per nucleon of {sup(A)}{sym} is {bea} MeV. Calculate the total binding energy and the mass defect in kg.',
                   f'{sf(bea * A, 4)} MeV; {q(bea * A / UMEV * U, "kg")}', f'E_B = {A} × {bea} = {sf(bea * A, 4)} MeV (A1); Δm = E_B/931.5 u = {sf(bea * A / UMEV, 4)} u (M1) = {q(bea * A / UMEV * U, "kg")} (A1).', 3)
    E_J = BE * 1e6 * EV
    return num(f'Calculate the minimum energy in joules needed to separate a {sup(A)}{sym} nucleus (binding energy per nucleon {bea} MeV) into its individual nucleons, and the mass equivalent of this energy.',
               f'{q(E_J, "J")}; {q(E_J / C ** 2, "kg")}', f'E_B = {A} × {bea} MeV = {sf(BE, 4)} MeV (A1) = {q(E_J, "J")} (A1); m = E/c² = {q(E_J / C ** 2, "kg")} (A1).', 3)


@R.add('ch10-st3', 'C3', (1, 4), 'mcq')
def c3_be_mcq(rng, slot):
    (sym, Z, A), bea = pick(rng, [kv for kv in BEA.items() if kv[0][2] > 3])
    BE = bea * A
    return nmcq(rng, f'The binding energy per nucleon of {sup(A)}{sym} (Z = {Z}) is {bea} MeV. What is its total binding energy?', BE,
                [bea * Z, bea * (A - Z), bea / A * 100], 'MeV', f'E_B = A × (E_B/A) = {A} × {bea} = {q(BE, "MeV")}; multiplying by Z or N is a common error.', extra=False, n=4)


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step')
def c4_q_value(rng, slot):
    rx = pick(rng, [
        ('fission', [('U', 92, 235)], [('Ba', 56, 141), ('Kr', 36, 92)], 3, 1),
        ('fission', [('U', 92, 235)], [('Xe', 54, 140), ('Sr', 38, 90)], 6, 1),
        ('fusion', [('H', 1, 2), ('H', 1, 3)], [('He', 2, 4)], 1, 0),
        ('fusion', [('H', 1, 2), ('H', 1, 2)], [('He', 2, 3)], 1, 0),
    ])
    kind, reac, prod, nout, nin = rx
    be_r = sum(BEA[x] * x[2] for x in reac)
    be_p = sum(BEA[x] * x[2] for x in prod)
    Q = be_p - be_r
    lhs = ' + '.join(f'{sup(a)}{s}' for s, z, a in reac) + (' + ¹₀n' if nin else '')
    rhs = ' + '.join(f'{sup(a)}{s}' for s, z, a in prod) + (f' + {nout} ¹₀n' if nout else '')
    tbl = '; '.join(f'{sup(a)}{s}: {BEA[(s, z, a)]} MeV' for s, z, a in reac + prod)
    A_in = sum(x[2] for x in reac)
    per_kg = Q * 1e6 * EV / (A_in * U)
    return num(f'Consider the {kind} reaction {lhs} → {rhs}. Binding energies per nucleon: {tbl} (free neutrons have zero binding energy). (a) Calculate the energy released per reaction in MeV. (b) Calculate the energy released per kilogram of reactant. (c) Explain, with reference to the binding-energy curve, why this reaction releases energy.',
               f'(a) {sf(Q, 3)} MeV; (b) {q(per_kg, "J kg⁻¹")}; (c) products have higher binding energy per nucleon',
               f'(a) total BE of products − reactants (M1) = {sf(be_p, 4)} − {sf(be_r, 4)} = {sf(Q, 3)} MeV (A1). (b) reactant mass ≈ {A_in} u = {q(A_in * U, "kg")} (M1); {q(Q * 1e6 * EV, "J")}/{q(A_in * U, "kg")} = {q(per_kg, "J kg⁻¹")} (A1). (c) moves towards the peak near Fe-56 (R1).', 5, 'multi_step', 'G5')


R.mcqs('ch10-st3', 'C2', (1, 4), [
    ('A nucleus X has a larger total binding energy than nucleus Y. Which statement must be true?', 'more energy is needed to separate X completely into nucleons', ['X is more stable than Y', 'X has more binding energy per nucleon', 'X has fewer nucleons'], 'Total BE measures complete separation energy; stability needs BE/A.'),
    ('On a graph of binding energy per nucleon against nucleon number, fusion releases energy for nuclides', 'to the left of the peak', ['to the right of the peak', 'at the peak', 'for all nuclides'], 'Light nuclei gain BE/A when they combine.'),
    ('The mass defect of a nucleus is 0.030 u. Its binding energy is about', '28 MeV', ['0.030 MeV', '931 MeV', '2.7 × 10¹⁵ J'], '0.030 × 931.5.'),
])

R.static('ch10-st3', 'C4', (3, 5), [
    ('Sketch the graph of binding energy per nucleon against nucleon number from A = 1 to 240 and use it to explain (a) why iron is the end product of fusion in massive stars, (b) why the energy per nucleon released in fusion of hydrogen is larger than in fission of uranium, and (c) why helium-4 lies above the general trend.',
     'Graph: rises steeply from 1.1 MeV (²H) with a spike at ⁴He (7.1 MeV), peaks at ~8.8 MeV near A = 56–62, then falls gradually to ~7.6 MeV at A = 238. (a) beyond iron, fusion lowers BE/A, so it absorbs energy and cannot sustain the star; (b) the curve is much steeper at low A, so the increase in BE/A in fusing hydrogen (~6–7 MeV per nucleon) far exceeds the ~0.8 MeV per nucleon gained in uranium fission; (c) ⁴He is an especially tightly bound arrangement of two protons and two neutrons.',
     'Correct sketch with values (A1 A1); iron argument (R1); steepness comparison (R1); He-4 explanation (R1).'),
], type='multi_step', marks=5)


R.facts('ch10-st4', F(
    terms=[('ionising radiation', 'radiation with enough energy to remove electrons from atoms, producing ions'),
           ('background radiation', 'the low level of ionising radiation always present, from natural sources (radon, rocks, cosmic rays, food) and artificial sources (medical, fallout)'),
           ('penetrating power', 'the ability of radiation to pass through matter before being absorbed')],
    facts=[('Which radiation is stopped by a few centimetres of air or a sheet of paper?', 'alpha', ['beta', 'gamma', 'X-rays'], 'Alpha particles are highly ionising and lose energy rapidly.'),
           ('Which radiation is most strongly ionising?', 'alpha', ['beta', 'gamma', 'all are equal'], 'Large charge and mass, slow speed.'),
           ('Beta-minus particles are typically stopped by', 'a few millimetres of aluminium', ['paper', 'several centimetres of lead', 'a few centimetres of air'], 'Typical range in aluminium ~mm.'),
           ('The largest contributor to background radiation for most people is', 'radon gas from rocks and soil', ['nuclear power stations', 'mobile phones', 'cosmic rays at sea level'], 'Radon and its daughters dominate natural dose.')],
    why=[('Explain why alpha particles are the most ionising but least penetrating radiation.', 'They have charge +2e and are slow and massive, so they interact strongly with electrons along their path, producing many ions per mm and losing their energy quickly; they are therefore stopped within a few cm of air.'),
         ('Explain why alpha sources are dangerous inside the body but relatively harmless outside it.', 'Outside, alpha particles are stopped by the dead outer layer of skin; inside (inhaled or ingested), all their energy is deposited in a small volume of living tissue, causing intense ionisation and cell damage.'),
         ('Explain why gamma radiation intensity decreases with distance from a point source even in air.', 'Gamma rays spread out in all directions, so the intensity follows an inverse-square law (I ∝ 1/r²); absorption in air is very small.')],
    contrast=[('alpha radiation', 'gamma radiation', 'Alpha: helium nuclei, charge +2e, strongly ionising, stopped by paper/few cm of air; gamma: high-energy photons, uncharged, weakly ionising, reduced significantly only by several cm of lead or metres of concrete.')],
    misc=[('Gamma rays are completely stopped by a thin sheet of lead.', 'Gamma intensity decreases gradually (exponentially) with thickness; even several cm of lead only reduce it by a large factor.'),
          ('Background radiation comes mainly from nuclear power stations.', 'Nuclear power contributes a tiny fraction (<0.1 %); radon, rocks, cosmic rays, food and medical uses dominate.')],
    evaluate=[('Smoke detectors containing americium-241 are a safe use of radioactivity in the home.', ['Am-241 emits alpha particles that cannot penetrate the casing', 'activity is small (~37 kBq)', 'saves many lives from fires'], ['long half-life (432 y) needs careful disposal', 'danger if the source is removed and ingested'], 'Safe in normal use because alpha particles are contained; risks arise only from misuse or disposal.')],
))


@R.add('ch10-st4', 'C3', (1, 5), 'numerical')
def c3_background(rng, slot):
    frame = rng.randrange(3)
    if frame == 0:
        bg = rng.choice([18, 24, 30, 36])
        rd = [rng.choice([450, 520, 610]) + bg, None, None]
        paper = rng.choice([0.6, 0.0]) * rd[0]
        types = rng.choice([('α and γ', True, False, True), ('β only', False, True, False), ('α and β', True, True, False), ('β and γ', False, True, True)])
        name_, a, b, gma = types
        n0 = 900
        na = 300 if a else 0
        nb = 350 if b else 0
        ng = 250 if gma else 0
        tot = na + nb + ng + bg
        p = nb + ng + bg
        al = ng + bg
        pb = bg + (ng // 10 if gma else 0)
        return num(f'A student measures the count rate (counts per minute) from a source with different absorbers: no absorber {tot}; paper {p}; 5 mm aluminium {al}; 5 cm lead {pb}. The background count rate is {bg} counts per minute. Identify the radiation(s) emitted and justify your answer.',
                   name_, f'Drop with paper ({tot} → {p}) {"shows α" if a else "is negligible, so no α"} (R1); drop with aluminium ({p} → {al}) {"shows β" if b else "is negligible, so no β"} (R1); count after aluminium above background {"shows γ" if gma else "is at background, so no γ"} (R1); conclusion: {name_} (A1).', 4)
    if frame == 1:
        I0 = rng.choice([800, 1200, 2000])
        r1, r2 = rng.choice([0.10, 0.20, 0.25]), rng.choice([0.40, 0.50, 0.60])
        bg = rng.choice([20, 30])
        I2 = I0 * (r1 / r2) ** 2
        return num(f'A gamma source gives a corrected count rate of {I0} counts per minute at {sf(r1 * 100, 2)} cm from a detector. Assuming an inverse-square law, predict the corrected and measured count rates at {sf(r2 * 100, 2)} cm if the background is {bg} counts per minute.',
                   f'corrected {sf(I2, 3)}; measured {sf(I2 + bg, 3)} counts per minute', f'I ∝ 1/r² (M1); I = {I0} × ({sf(r1, 2)}/{sf(r2, 2)})² = {sf(I2, 3)} (A1); add background: {sf(I2 + bg, 3)} (A1).', 3)
    mu = rng.choice([0.05, 0.08, 0.12]) * 10
    x12 = math.log(2) / mu
    x = rng.choice([1, 2, 3, 5])
    return num(f'Gamma rays from a source are absorbed by lead with a half-value thickness of {sf(x12, 3)} cm. Calculate the fraction of the gamma intensity transmitted through {x} cm of lead.',
               sf(0.5 ** (x / x12), 3), f'I/I₀ = (1/2)^(x/x½) (M1) = (1/2)^({sf(x / x12, 3)}) = {sf(0.5 ** (x / x12), 3)} (A1).', 2)


R.mcqs('ch10-st4', 'C2', (1, 4), [
    ('A source’s count rate is unaffected by paper but falls to background with 3 mm of aluminium. The source emits', 'beta only', ['alpha only', 'gamma only', 'alpha and gamma'], 'Not α (paper), not γ (would penetrate Al).'),
    ('In a cloud chamber, alpha tracks are', 'short, thick and straight', ['long, thin and wavy', 'invisible', 'spiral'], 'Heavy, strongly ionising particles travel straight and stop quickly.'),
    ('Workers using gamma sources reduce their dose mainly by', 'increasing distance, reducing time and using lead or concrete shielding', ['wearing paper gloves', 'cooling the source', 'using magnets to deflect the radiation'], 'Inverse-square law, exposure time and absorption.'),
])

R.mcqs('ch10-st4', 'C3', (1, 4), [
    ('A detector reads 340 counts in 5 minutes with no source and 2840 counts in 5 minutes with a source present. The corrected count rate is', '500 counts per minute', ['568 counts per minute', '2500 counts per minute', '636 counts per minute'], '(2840 − 340)/5 = 500.'),
    ('A gamma source gives 1600 counts per minute at 10 cm. At 40 cm (corrected for background) the count rate is about', '100 counts per minute', ['400 counts per minute', '800 counts per minute', '25 counts per minute'], 'Inverse square: 1600/16.'),
    ('The half-value thickness of lead for a gamma source is 1.2 cm. The fraction transmitted by 3.6 cm of lead is', '1/8', ['1/3', '1/4', '1/6'], 'Three half-value thicknesses.'),
    ('A count of 400 is recorded in a counting interval. The approximate statistical uncertainty is', '± 20 counts', ['± 4 counts', '± 40 counts', '± 200 counts'], 'Random decay: uncertainty ≈ √N.'),
])

R.static('ch10-st4', 'C4', (3, 5), [
    ('Design an experiment to show that gamma radiation obeys an inverse-square law, using a Geiger–Müller tube and counter. Include how you would deal with background radiation, the random nature of decay and the unknown position of the effective detection point in the tube.',
     'Measure background for 10 min. Measure counts over a fixed time at several distances d from a ruler mark, repeating each; subtract background. Since C = k/(d + e)², plot 1/√C against d: a straight line confirms the law and the x-intercept gives −e (the offset of the detection point). Use long counting times (N > 1000) to reduce the relative uncertainty (≈ 1/√N), handle the source with tongs, keep distance, minimise exposure time.',
     'Background measured and subtracted (A1); range of distances and repeat counts (A1); linearisation 1/√C vs d (M1 A1); random uncertainty ∝ √N addressed (R1); safety (R1).', 6),
], type='multi_step', marks=6)

repeat_readings('ch10-st4', 'the background count in one minute', 'counts', 18, 30, 0,
                ['measured the background radiation in the laboratory with a Geiger–Müller tube before an experiment.',
                 'recorded the background count with no sources present, over several separate minutes.'])


R.facts('ch10-st5', F(
    terms=[('strong nuclear force', 'a short-range (~10⁻¹⁵ m) attractive force between nucleons that holds the nucleus together, repulsive at very short separations (< ~0.5 fm)'),
           ('weak nuclear force', 'the fundamental interaction responsible for beta decay, which changes the flavour of quarks'),
           ('band of stability', 'the region on a plot of neutron number against proton number containing the stable nuclides'),
           ('neutron-to-proton ratio', 'N/Z, which is about 1 for light stable nuclei and rises to about 1.5 for the heaviest stable nuclei')],
    facts=[('The range of the strong nuclear force is about', '10⁻¹⁵ m', ['10⁻¹⁰ m', '10⁻⁶ m', 'infinite'], 'Femtometre scale – about the size of a nucleon.'),
           ('Heavy stable nuclei have more neutrons than protons because', 'extra neutrons add strong-force attraction without adding electric repulsion', ['neutrons are lighter', 'protons attract each other', 'neutrons carry negative charge'], 'Coulomb repulsion grows as Z².'),
           ('A nuclide lies above the band of stability (too many neutrons). It is likely to decay by', 'β⁻ emission', ['β⁺ emission', 'alpha emission only', 'gamma emission only'], 'β⁻ converts a neutron to a proton.'),
           ('The four fundamental interactions in order of decreasing strength (at nuclear distances) are', 'strong, electromagnetic, weak, gravitational', ['gravitational, weak, electromagnetic, strong', 'electromagnetic, strong, weak, gravitational', 'weak, strong, electromagnetic, gravitational'], 'Relative strengths ~1, 1/137, 10⁻⁶, 10⁻³⁹.')],
    why=[('Explain why very heavy nuclei (Z > 83) are all unstable.', 'Electric repulsion acts between every pair of protons (long range, ∝ Z²) while the strong force acts only between neighbouring nucleons; beyond Z ≈ 83 repulsion makes the nucleus unstable, usually decaying by alpha emission.'),
         ('Explain why the strong force must become repulsive at very short distances.', 'Otherwise nucleons would be pulled together and the nucleus would collapse; the repulsive core (< ~0.5 fm) keeps nucleons at a typical separation, giving the constant nuclear density.'),
         ('Explain how the position of a nuclide relative to the band of stability predicts its decay mode.', 'Neutron-rich nuclides (above the band) decay by β⁻ (n → p), proton-rich ones (below) by β⁺ or electron capture (p → n), and very heavy ones (beyond the end) by alpha emission, each moving the nuclide towards stability.')],
    contrast=[('the strong nuclear force', 'the electromagnetic force', 'The strong force is very strong, attractive between all nucleons, short-range (~fm) and charge-independent; the electromagnetic force is weaker at nuclear distances, acts only between charges, can repel and has infinite range.')],
    misc=[('Neutrons are held in the nucleus by electric attraction to protons.', 'Neutrons are uncharged; they are held by the strong nuclear force.'),
          ('The strong force holds electrons in their orbits.', 'Electrons are bound by the electromagnetic force; the strong force does not act on electrons (leptons).')],
    evaluate=[('The strong nuclear force alone determines whether a nucleus is stable.', ['strong force binds nucleons and its short range limits nuclear size'], ['electromagnetic repulsion between protons is crucial for heavy nuclei', 'the Pauli principle favours N ≈ Z in light nuclei', 'the weak force allows β decay towards stability'], 'Stability results from the balance of strong attraction, electromagnetic repulsion and quantum effects, with the weak force allowing adjustments.')],
))


@R.add('ch10-st5', 'C3', (1, 5), 'numerical')
def c3_stability(rng, slot):
    cand = [('C', 6, 14, 'above (neutron-rich)', 'β⁻'), ('Na', 11, 22, 'below (proton-rich)', 'β⁺'), ('Sr', 38, 90, 'above (neutron-rich)', 'β⁻'), ('F', 9, 18, 'below (proton-rich)', 'β⁺'),
            ('U', 92, 238, 'beyond the end of the band (very heavy)', 'α'), ('Co', 27, 60, 'above (neutron-rich)', 'β⁻'), ('O', 8, 15, 'below (proton-rich)', 'β⁺'),
            ('Ra', 88, 226, 'beyond the end of the band (very heavy)', 'α'), ('I', 53, 131, 'above (neutron-rich)', 'β⁻')]
    sym, Z, A, pos, mode = pick(rng, cand)
    frame = rng.randrange(3)
    if frame == 0:
        return num(f'{sup(A)}{sym} (Z = {Z}) is unstable. Calculate its neutron-to-proton ratio, state where it lies relative to the band of stability and predict its likely decay mode.',
                   f'N/Z = {sf((A - Z) / Z, 3)}; {pos}; {mode}', f'N = {A - Z}, N/Z = {sf((A - Z) / Z, 3)} (A1); position: {pos} (R1); decay {mode} moves it towards stability (A1).', 3)
    if frame == 1:
        r = rng.choice([1.0, 2.0, 3.0]) * 1e-15
        Fc = K * E * E / r ** 2
        return num(f'Calculate the electric force between two protons {q(r * 1e15, "fm")} apart (1 fm = 10⁻¹⁵ m), and explain what this implies about the strong force.',
                   f'{q(Fc, "N")} (repulsive); the strong force must be attractive and larger than this at nuclear separations',
                   f'F = ke²/r² (M1) = {q(Fc, "N")} (A1); nucleus is stable, so an attractive force of greater magnitude acts (R1).', 3)
    Fe = K * E * E / (2e-15) ** 2
    Fg = G * MP * MP / (2e-15) ** 2
    return num('Two protons in a nucleus are 2.0 × 10⁻¹⁵ m apart. Calculate the ratio of the electric force to the gravitational force between them, and comment on the role of gravity in nuclear stability.',
               f'{sf(Fe / Fg, 3)}; gravity is negligible', f'F_e = {q(Fe, "N")}, F_g = {q(Fg, "N")} (M1 A1); ratio {sf(Fe / Fg, 3)} – gravity plays no role (R1).', 3)


@R.add('ch10-st5', 'C3', (1, 4), 'mcq')
def c3_stab_mcq(rng, slot):
    cand = [('C', 6, 14, 'β⁻'), ('Na', 11, 22, 'β⁺'), ('Sr', 38, 90, 'β⁻'), ('F', 9, 18, 'β⁺'), ('Po', 84, 210, 'α'), ('P', 15, 32, 'β⁻'), ('C', 6, 11, 'β⁺')]
    sym, Z, A, mode = pick(rng, cand)
    others = [m for m in ['α', 'β⁻', 'β⁺', 'γ only'] if m != mode]
    return mcq(rng, f'{sup(A)}{sym} has {Z} protons and {A - Z} neutrons. Which decay mode is most likely?', mode, others,
               f'N/Z = {sf((A - Z) / Z, 3)}; {"neutron-rich → β⁻" if mode == "β⁻" else "proton-rich → β⁺" if mode == "β⁺" else "heavy → α"}.')


R.mcqs('ch10-st5', 'C2', (1, 4), [
    ('Why is the strong nuclear force not noticed in everyday life?', 'its range is only about 10⁻¹⁵ m', ['it is weaker than gravity', 'it only acts on electrons', 'it is cancelled by the weak force'], 'Short range.'),
    ('Which exchange particle mediates the weak interaction?', 'W and Z bosons', ['photons', 'gluons', 'gravitons'], 'W± and Z⁰.'),
    ('Light stable nuclei have N ≈ Z, but heavy stable nuclei have N > Z. This is mainly because', 'electric repulsion between protons grows faster with Z than the strong attraction', ['neutrons are attracted to electrons', 'the weak force adds neutrons', 'protons decay in heavy nuclei'], 'Coulomb energy ∝ Z².'),
])

R.static('ch10-st5', 'C4', (3, 5), [
    ('Using a sketch of the N–Z plot of stable nuclides, discuss how the competition between the strong nuclear force and the electromagnetic force accounts for (a) the shape of the band of stability, (b) the existence of alpha decay, and (c) the decay modes of nuclides on either side of the band.',
     '(a) For low Z the band follows N = Z; as Z increases it curves above the line (N/Z ≈ 1.5 at Pb) because extra neutrons supply strong attraction without Coulomb repulsion; the band ends near Z = 83. (b) In heavy nuclei Coulomb repulsion makes emission of a tightly bound α particle energetically favourable, reducing Z and A together. (c) Above the band (neutron-rich) β⁻ converts n → p; below (proton-rich) β⁺ or electron capture converts p → n; both are weak-force processes moving the nuclide towards the band.',
     'Correct sketch and N = Z line (A1); explanation of curvature (R1); end of the band and alpha decay (R1); β⁻ and β⁺ regions (R1 R1); role of weak force (A1).', 6),
], type='multi_step', marks=6)


# =============================================================================================
# ch11 E.4 Fission
# =============================================================================================
FISSIONS = [(('Ba', 56, 141), ('Kr', 36, 92)), (('Xe', 54, 140), ('Sr', 38, 94)), (('Cs', 55, 137), ('Rb', 37, 96)), (('Ba', 56, 144), ('Kr', 36, 89)),
            (('Te', 52, 134), ('Zr', 40, 99)), (('Xe', 54, 139), ('Sr', 38, 95))]

R.facts('ch11-st1', F(
    terms=[('nuclear fission', 'the splitting of a heavy nucleus into two smaller nuclei of comparable mass, with the release of neutrons and energy'),
           ('neutron-induced fission', 'fission triggered when a heavy nucleus such as uranium-235 absorbs a (usually slow) neutron'),
           ('chain reaction', 'a self-sustaining sequence of fissions in which neutrons released by one fission cause further fissions'),
           ('critical mass', 'the minimum mass of fissile material needed for a chain reaction to be self-sustaining')],
    facts=[('The energy released in a single fission of uranium-235 is about', '200 MeV', ['2 MeV', '20 keV', '2000 MeV'], 'Typical Q ≈ 170 MeV kinetic + γ and decay energy ≈ 200 MeV.'),
           ('Most of the energy released in fission appears initially as', 'kinetic energy of the fission fragments', ['gamma radiation', 'kinetic energy of neutrons', 'light'], 'The fragments are repelled by Coulomb forces.'),
           ('Spontaneous fission differs from induced fission in that it', 'occurs without the absorption of a neutron', ['releases no energy', 'only occurs in light nuclei', 'produces no neutrons'], 'Some very heavy nuclides (e.g. Cf-252) fission spontaneously.'),
           ('For a chain reaction to be sustained, on average', 'at least one neutron from each fission must cause another fission', ['every neutron must cause a fission', 'no neutrons may escape', 'two neutrons must be absorbed'], 'Multiplication factor k ≥ 1.')],
    why=[('Explain why a mass of uranium below the critical mass cannot sustain a chain reaction.', 'In a small mass the surface area is large compared with the volume, so many neutrons escape before causing fission; fewer than one neutron per fission goes on to cause another fission (k < 1) and the reaction dies out.'),
         ('Explain why fission fragments are usually radioactive.', 'The fragments have roughly the same N/Z ratio as uranium (~1.55), which is too high for medium-mass nuclei; they are neutron-rich and decay by successive β⁻ emissions towards stability.'),
         ('Explain why slow (thermal) neutrons are more effective than fast neutrons at causing fission of uranium-235.', 'The probability (cross-section) of absorption by U-235 is far greater for slow neutrons, which spend longer near the nucleus; fast neutrons tend to scatter or pass through.')],
    contrast=[('spontaneous fission', 'neutron-induced fission', 'Spontaneous fission happens randomly without an external trigger (rare except in very heavy nuclides); induced fission follows absorption of a neutron, forming an excited compound nucleus (e.g. U-236) that splits.'),
              ('a controlled chain reaction', 'an uncontrolled chain reaction', 'In a controlled reaction (reactor) the multiplication factor is held at exactly 1 by control rods; in an uncontrolled one (weapon) k > 1 and the number of fissions grows exponentially in microseconds.')],
    misc=[('In fission the uranium nucleus breaks into many small pieces like an explosion of protons and neutrons.', 'It splits mainly into two medium-mass fragments plus 2–3 neutrons.'),
          ('The energy released in fission comes from the neutrons’ kinetic energy.', 'It comes from the increase in binding energy (decrease in mass) as the heavy nucleus splits into more tightly bound fragments.')],
    evaluate=[('Meitner and Frisch’s interpretation of Hahn and Strassmann’s results is a model case of collaboration in science.', ['chemists detected barium; physicists explained it using the liquid-drop model and E = mc²', 'shows the value of international communication'], ['Meitner was excluded from the Nobel Prize, raising issues of recognition and gender bias', 'political circumstances (exile) shaped the collaboration'], 'It illustrates productive interdisciplinary collaboration and also how social factors affect credit in science (NOS).')],
))


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def c3_fission(rng, slot):
    (a, b) = pick(rng, FISSIONS)
    n = 236 - a[2] - b[2]
    frame = rng.randrange(4)
    if frame == 0:
        return num(f'Complete the equation for the fission of uranium-235: ¹₀n + ²³⁵₉₂U → {sup(a[2])}{a[0]} (Z = {a[1]}) + {b[0]} (Z = {b[1]}) + 3 ¹₀n. Determine the nucleon number of the {b[0]} nucleus, and check that charge is conserved.'.replace('3 ¹₀n', f'{n} ¹₀n') if n > 0 else None,
                   f'A = {b[2]}; 92 = {a[1]} + {b[1]}', f'Nucleons: 1 + 235 = {a[2]} + A + {n} → A = {b[2]} (M1 A1); protons {a[1]} + {b[1]} = 92 (A1).', 3) if n > 0 else None
    if frame == 1:
        return num(f'In one fission of uranium-235 by a neutron, the products are {sup(a[2])}{a[0]} and {sup(b[2])}{b[0]} plus some neutrons. Determine the number of neutrons released.',
                   f'{n}', f'Conservation of nucleon number: 236 = {a[2]} + {b[2]} + n (M1); n = {n} (A1).', 2) if n > 0 else None
    if frame == 2:
        P = rng.choice([500, 900, 1000, 1200, 1600]) * 1e6
        Ef = 200e6 * EV
        rate = P / Ef
        return num(f'A reactor core produces {sf(P / 1e6, 3)} MW of thermal power. Each fission releases 200 MeV. Calculate the number of fissions per second.',
                   q(rate, 's⁻¹'), f'E per fission = 200 × 10⁶ × 1.60 × 10⁻¹⁹ = 3.20 × 10⁻¹¹ J (A1); N = P/E (M1) = {q(rate, "s⁻¹")} (A1).', 3)
    k = rng.choice([1.05, 1.1, 1.2, 2.0])
    gens = rng.choice([10, 20, 50])
    return num(f'In a chain reaction each generation produces k = {k} times as many fissions as the previous one. Starting with one fission, how many fissions occur in generation {gens}? Comment on the significance of k > 1.',
               f'{sf(k ** gens, 3)}; growth is exponential (supercritical)', f'N = k^n (M1) = {k}^{gens} = {sf(k ** gens, 3)} (A1); k > 1 → exponential growth, must be kept at 1 in a reactor (R1).', 3)


@R.add('ch11-st1', 'C3', (1, 4), 'mcq')
def c3_fission_mcq(rng, slot):
    a, b = pick(rng, FISSIONS)
    n = 236 - a[2] - b[2]
    if n < 1:
        return None
    return mcq(rng, f'¹₀n + ²³⁵₉₂U → {sup(a[2])}{a[0]} + {sup(b[2])}{b[0]} + x ¹₀n. What is x?', str(n), [str(n + 1), str(max(0, n - 1)) if n > 1 else str(n + 2), str(n + 3)],
               f'Nucleons: 236 = {a[2]} + {b[2]} + x, so x = {n}.')


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def c4_fuel(rng, slot):
    P = rng.choice([1000, 1200, 1500]) * 1e6
    eff = rng.choice([0.30, 0.33, 0.35])
    Ef = 200e6 * EV
    rate = P / eff / Ef
    m_yr = rate * 3.156e7 * 235 * U
    coal = P / eff * 3.156e7 / 3.0e7
    return num(f'A nuclear power station produces {sf(P / 1e6, 3)} MW of electrical power with an overall efficiency of {int(eff * 100)} %. Each fission of U-235 releases 200 MeV. (a) Calculate the thermal power of the reactor. (b) Determine the number of fissions per second. (c) Determine the mass of U-235 used per year. (d) Compare with the mass of coal (energy density 30 MJ kg⁻¹) needed for the same thermal output, and comment.',
               f'(a) {q(P / eff, "W")}; (b) {q(rate, "s⁻¹")}; (c) {q(m_yr, "kg")}; (d) {q(coal, "kg")} of coal – about {sf(coal / m_yr, 2)} times more',
               f'(a) P/η = {q(P / eff, "W")} (A1). (b) N = P_th/(3.20 × 10⁻¹¹ J) = {q(rate, "s⁻¹")} (M1 A1). (c) mass = N × t × 235 u = {q(m_yr, "kg")} (M1 A1). (d) coal mass = E/(3.0 × 10⁷) = {q(coal, "kg")} (A1); far greater energy density of nuclear fuel (R1).', 7, 'multi_step', 'G5')


R.mcqs('ch11-st1', 'C2', (1, 4), [
    ('Uranium-235 absorbs a neutron and forms uranium-236 in an excited state. The excited nucleus then', 'oscillates, deforms and splits into two fragments', ['emits an electron and becomes neptunium', 'returns to U-235 by emitting a neutron', 'fuses with another nucleus'], 'Liquid-drop picture of fission.'),
    ('The total mass of the products of a fission reaction is', 'slightly less than the mass of the reactants', ['slightly more than the reactants', 'exactly equal to the reactants', 'about half the reactants'], 'Mass defect becomes released energy.'),
    ('Why is the critical mass smaller for a sphere than for a flat sheet of the same material?', 'a sphere has the smallest surface area for its volume, so fewer neutrons escape', ['spheres absorb more neutrons', 'neutrons travel faster in spheres', 'flat sheets reflect neutrons'], 'Surface-to-volume ratio controls leakage.'),
])

R.static('ch11-st1', 'C4', (3, 5), [
    ('Fission of U-235 typically releases about 200 MeV per event. (a) Explain the origin of this energy using the binding-energy-per-nucleon curve (U-235 ≈ 7.6 MeV, fragments ≈ 8.5 MeV). (b) Use these values to estimate the energy released. (c) Account for the forms in which the energy appears and explain why not all of it can be used in a power station.',
     '(a) Fragments are more tightly bound than uranium, so total binding energy increases; the increase equals the energy released. (b) ≈ 235 × (8.5 − 7.6) ≈ 210 MeV. (c) ~165 MeV kinetic energy of fragments, ~5 MeV neutrons, ~7 MeV prompt γ, plus delayed β and γ from fragment decay and ~10 MeV carried by antineutrinos that escape; the thermal energy is converted to electricity with ~33 % efficiency (second law of thermodynamics).',
     'Binding-energy argument (R1); estimate ≈ 200 MeV (M1 A1); forms of energy including neutrinos (R1); efficiency limitation (R1).'),
], type='multi_step', marks=5)


R.facts('ch11-st2', F(
    terms=[('moderator', 'a material (such as water or graphite) that slows fast neutrons to thermal speeds by elastic collisions so that they are more likely to cause fission'),
           ('control rods', 'rods of a strong neutron absorber (boron or cadmium) moved into or out of the core to control the rate of fission'),
           ('heat exchanger', 'the part of a reactor system in which thermal energy from the hot coolant is transferred to water to make steam for the turbines'),
           ('coolant', 'a fluid (water, heavy water, CO₂ or liquid sodium) that carries thermal energy away from the reactor core')],
    facts=[('A good moderator has nuclei that are', 'light, so that neutrons lose a large fraction of their energy in each collision, and that rarely absorb neutrons', ['heavy and strongly absorbing', 'radioactive', 'magnetic'], 'Energy transfer is greatest when masses are similar.'),
           ('Control rods are made of boron or cadmium because these materials', 'absorb neutrons strongly', ['slow neutrons down', 'reflect neutrons', 'conduct heat well'], 'High neutron-capture cross-section.'),
           ('Inserting the control rods further into the core', 'reduces the rate of fission', ['increases the rate of fission', 'speeds up the neutrons', 'increases the critical mass of fuel removed'], 'More neutrons are absorbed, k falls.'),
           ('In a pressurised water reactor, the water in the primary circuit acts as', 'both moderator and coolant', ['only fuel', 'only shielding', 'control rods'], 'Light water both slows neutrons and removes heat.')],
    why=[('Explain why the moderator slows neutrons by elastic collisions and why light nuclei are best.', 'In an elastic collision kinetic energy and momentum are conserved; a neutron colliding with a nucleus of similar mass (e.g. hydrogen) can transfer most of its kinetic energy, whereas with a heavy nucleus it bounces off with nearly the same speed.'),
         ('Explain the role of the thick concrete and steel shielding around a reactor.', 'The core emits intense neutron and gamma radiation; dense concrete and steel absorb these, protecting workers and the environment.'),
         ('Explain why a reactor is designed to operate with a multiplication factor of exactly 1.', 'With k = 1 each fission causes one further fission on average, so the power output is steady; k > 1 would make the power grow, k < 1 would shut down the reaction.')],
    contrast=[('the moderator', 'the control rods', 'The moderator slows neutrons (without absorbing them) to make fission more likely; control rods absorb neutrons to reduce the number available for fission.')],
    misc=[('The moderator absorbs neutrons to control the reaction rate.', 'The moderator slows neutrons; absorption is the job of the control rods. A good moderator absorbs as few neutrons as possible.'),
          ('In a nuclear power station, the reactor produces electricity directly.', 'The reactor produces thermal energy; a heat exchanger makes steam that drives turbines and generators, as in other thermal power stations.')],
    evaluate=[('Water is the best choice of moderator for a nuclear reactor.', ['hydrogen nuclei slow neutrons in few collisions', 'water is cheap and also acts as coolant'], ['ordinary hydrogen absorbs some neutrons, requiring enriched fuel', 'heavy water or graphite allow natural uranium', 'graphite can burn (Windscale, Chernobyl)'], 'Light water is practical and widely used, but the best moderator depends on fuel enrichment and safety design.')],
))


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def c3_moderator(rng, slot):
    frame = rng.randrange(3)
    if frame == 0:
        f = rng.choice([0.5, 0.63, 0.72, 0.84])
        E0 = rng.choice([1.0, 2.0, 2.5]) * 1e6
        Ef = 0.025
        Nc = math.log(Ef / E0) / math.log(f)
        mat = {0.5: 'hydrogen (in water)', 0.63: 'deuterium (heavy water)', 0.72: 'beryllium', 0.84: 'carbon (graphite)'}[f]
        return num(f'In each collision with {mat}, a neutron keeps on average {int(f * 100)} % of its kinetic energy. Estimate the number of collisions needed to slow a {sf(E0 / 1e6, 2)} MeV neutron to thermal energy (0.025 eV).',
                   f'about {math.ceil(Nc)} collisions', f'E = E₀f^N (M1); N = ln(0.025/{sf(E0, 2)})/ln {f} (M1) = {sf(Nc, 3)} → {math.ceil(Nc)} (A1).', 3)
    if frame == 1:
        m = rng.choice([1, 2, 12])
        u_ = rng.choice([1.0, 2.0, 1.5]) * 1e7
        v1 = (1 - m) / (1 + m) * u_
        frac_ = 1 - ((1 - m) / (1 + m)) ** 2
        mat = {1: 'a hydrogen nucleus (1 u)', 2: 'a deuterium nucleus (2 u)', 12: 'a carbon-12 nucleus (12 u)'}[m]
        return num(f'A neutron (mass 1 u) moving at {q(u_, "m s⁻¹")} collides elastically and head-on with {mat} at rest. Calculate the fraction of the neutron’s kinetic energy transferred to the nucleus. (v_neutron after = (1 − M)/(1 + M) × u, masses in u)',
                   sf(frac_, 3), f'v after = {sf((1 - m) / (1 + m), 3)}u (M1); fraction kept = ({sf((1 - m) / (1 + m), 3)})² (M1); transferred = {sf(frac_, 3)} (A1).', 3)
    T = rng.choice([290, 300, 320, 560])
    Ek = 1.5 * 1.38e-23 * T
    v = math.sqrt(2 * Ek / MN)
    return num(f'Thermal neutrons in a moderator at {T} K have mean kinetic energy (3/2)k_BT (k_B = 1.38 × 10⁻²³ J K⁻¹). Calculate this energy in eV and the corresponding neutron speed.',
               f'{sf(Ek / EV, 3)} eV; {q(v, "m s⁻¹")}', f'Eₖ = 1.5 × 1.38 × 10⁻²³ × {T} = {q(Ek, "J")} (A1) = {sf(Ek / EV, 3)} eV (A1); v = √(2E/mₙ) = {q(v, "m s⁻¹")} (A1).', 3)


@R.add('ch11-st2', 'C2', (1, 4), 'mcq')
def c2_reactor_mcq(rng, slot):
    items = [
        ('During a sudden power surge, the reactor operators should', 'insert the control rods further', ['withdraw the control rods', 'remove the moderator', 'turn off the coolant pumps'], 'More absorption reduces k below 1.'),
        ('Why is the fuel in a reactor arranged in many thin rods rather than one large block?', 'neutrons can leave each rod, be moderated, and enter another rod, and heat is removed efficiently', ['to make the fuel critical in each rod', 'to stop the coolant boiling', 'to absorb more neutrons'], 'Slowing between rods and heat transfer.'),
        ('Which property makes graphite a suitable moderator?', 'its carbon nuclei are light and absorb few neutrons', ['it is a good neutron absorber', 'it is radioactive', 'it is a good electrical conductor'], 'Light nuclei, low absorption.'),
        ('What is the purpose of the heat exchanger in a pressurised water reactor?', 'to transfer energy from the radioactive primary coolant to a separate secondary circuit that makes steam', ['to slow neutrons', 'to absorb gamma rays', 'to enrich the fuel'], 'Keeps radioactive water separate from the turbines.'),
    ]
    q_, a, w, why = pick(rng, items)
    return mcq(rng, q_, a, w, why)


@R.add('ch11-st2', 'C3', (1, 4), 'mcq')
def c3_reactor_mcq(rng, slot):
    f = rng.choice([0.5, 0.84])
    E0 = 2.0e6
    n = rng.choice([5, 10, 20])
    En = E0 * f ** n
    return nmcq(rng, f'A 2.0 MeV neutron keeps {int(f * 100)} % of its energy in each collision with moderator nuclei. What is its energy after {n} collisions?', En,
                [E0 * (1 - n * (1 - f)) if E0 * (1 - n * (1 - f)) > 0 else E0 * f ** (n + 2), E0 * f ** (n / 2), E0 * (1 - f) ** n], 'eV', f'E = E₀f^n = 2.0 × 10⁶ × {f}^{n} = {q(En, "eV")}.', extra=True)


R.static('ch11-st2', 'C4', (3, 5), [
    ('Describe the energy transfers in a pressurised-water nuclear power station, from fission in the core to electrical energy, and explain the role of the moderator, control rods, coolant, heat exchanger and shielding.',
     'Fission converts nuclear (binding) energy into kinetic energy of fragments, which becomes internal energy of the fuel; the coolant (pressurised water) carries it to the heat exchanger, where water in the secondary circuit boils; steam drives turbines (kinetic) and generators (electrical); waste heat is rejected in cooling towers. Moderator slows neutrons for efficient fission; control rods absorb neutrons to keep k = 1; coolant removes heat and keeps fuel safe; heat exchanger isolates radioactive primary water; shielding absorbs neutrons and gamma rays.',
     'Correct chain of energy transfers (A1 A1); moderator (R1); control rods (R1); coolant and heat exchanger (R1); shielding (R1).', 6),
    ('Compare graphite-moderated and light-water-moderated reactors in terms of the fuel enrichment required, the number of collisions needed to thermalise neutrons and safety considerations.',
     'Graphite (carbon, 12 u) keeps ~84 % of neutron energy per collision, needing ~110 collisions, but absorbs very few neutrons, so natural or slightly enriched uranium can be used; it is flammable at high temperature. Light water (hydrogen, 1 u) thermalises in ~20 collisions but absorbs more neutrons, needing ~3–5 % enriched fuel; if the water boils away the moderation is lost and the reaction slows (negative void coefficient), an inherent safety feature, whereas in some graphite designs (RBMK) loss of water increased reactivity.',
     'Collision fractions and numbers (A1 A1); absorption and enrichment (R1); void coefficient / safety (R1); balanced conclusion (R1).', 5),
], type='multi_step', marks=5)


R.facts('ch11-st3', F(
    terms=[('high-level waste', 'highly radioactive waste, mainly spent fuel and fission products, that generates significant heat and must be cooled and isolated for thousands of years'),
           ('low-level waste', 'slightly contaminated material (clothing, tools) with low activity that can be compacted and buried'),
           ('deep geological repository', 'an engineered facility hundreds of metres underground in stable rock for long-term isolation of high-level waste'),
           ('meltdown', 'severe overheating of a reactor core so that the fuel melts, usually after failure of cooling')],
    facts=[('Spent fuel rods are first stored in cooling ponds because', 'they continue to release large amounts of heat from radioactive decay', ['they are still undergoing fission at full power', 'water makes them non-radioactive', 'they need to be cleaned'], 'Decay heat persists after shutdown.'),
           ('Some fission products are especially hazardous because they', 'have chemical behaviour that concentrates them in the body (e.g. iodine-131 in the thyroid)', ['are not radioactive', 'have half-lives of seconds', 'are heavier than uranium'], 'I-131 and Sr-90 are absorbed biologically.'),
           ('Which accident followed a tsunami that disabled reactor cooling systems in 2011?', 'Fukushima Daiichi', ['Chernobyl', 'Three Mile Island', 'Windscale'], 'Loss of power to cooling pumps.'),
           ('Long-lived actinides such as plutonium-239 in nuclear waste have half-lives of about', 'tens of thousands of years', ['a few days', 'a few years', 'a few seconds'], 'Pu-239: 24 100 years.')],
    why=[('Explain why high-level nuclear waste must be isolated for thousands of years.', 'It contains long-lived radionuclides (e.g. Pu-239 with T½ ≈ 24 000 y) whose activity falls only slowly; it remains hazardous until the activity has decayed to safe levels, requiring many half-lives.'),
         ('Explain why the decay heat of a reactor must be removed even after the chain reaction has stopped.', 'Fission products continue to decay, initially producing about 6–7 % of full thermal power; without cooling the fuel overheats and can melt.'),
         ('Explain why vitrification is used to treat liquid high-level waste.', 'Mixing the waste into molten glass and solidifying it immobilises the radionuclides in a stable, insoluble solid that resists leaching by groundwater for long periods.')],
    contrast=[('low-level waste', 'high-level waste', 'Low-level waste has low activity and little heat output and can be compacted and buried near the surface; high-level waste is intensely radioactive and hot, requiring cooling, vitrification and deep geological disposal.')],
    misc=[('Nuclear waste becomes safe after one half-life.', 'After one half-life the activity has only halved; many half-lives are needed for hazardous waste to reach safe levels.'),
          ('A nuclear reactor can explode like an atomic bomb.', 'Reactor fuel is not enriched enough and cannot be assembled supercritically fast enough for a nuclear explosion; accidents involve steam or hydrogen explosions and release of radioactive material.')],
    cases=[('the Chernobyl accident (1986)', 'during a safety test with safety systems disabled, a power surge in an RBMK reactor caused a steam explosion and graphite fire that spread radioactive material over Europe', 'the importance of reactor design and safety culture', 'the positive void coefficient made the power rise as water boiled, and operators had withdrawn too many control rods'),
           ('Fukushima Daiichi (2011)', 'a tsunami knocked out the backup diesel generators, so decay heat could not be removed and three cores melted', 'decay heat and the need for passive cooling', 'even with the chain reaction stopped, fission-product decay heat must be removed'),
           ('the Onkalo repository in Finland', 'spent fuel is sealed in copper canisters and placed 400 m deep in granite surrounded by bentonite clay', 'long-term geological disposal of high-level waste', 'multiple barriers isolate the waste over the ~100 000 years needed for its activity to decay')],
    evaluate=[('Nuclear power should be part of the solution to climate change despite the problems of waste and safety.', ['very low lifecycle CO₂ emissions', 'reliable baseload power', 'small land use and fuel volume'], ['long-lived waste with no operating repository in most countries', 'rare but severe accidents', 'high construction cost and long build times', 'proliferation concerns'], 'Many energy analysts see a role for nuclear power alongside renewables; the judgement depends on weighing low-carbon reliability against waste, cost and risk.')],
))


@R.add('ch11-st3', 'C3', (1, 5), 'numerical')
def c3_waste(rng, slot):
    iso = pick(rng, [('caesium-137', 30.2), ('strontium-90', 28.8), ('plutonium-239', 24100), ('iodine-131', 8.02 / 365.25), ('americium-241', 432), ('technetium-99', 211000)])
    nm, T = iso
    frame = rng.randrange(3)
    if frame == 0:
        fr = rng.choice([0.01, 0.001, 0.10, 0.05])
        t = T * math.log(1 / fr) / math.log(2)
        return num(f'Calculate the time taken for the activity of {nm} (half-life {sf(T, 3)} years) in nuclear waste to fall to {fr * 100:g} % of its initial value.',
                   q(t, 'years'), f'(1/2)^(t/T½) = {fr} (M1); t = T½ log₂(1/{fr}) = {sf(math.log(1 / fr) / math.log(2), 3)} half-lives (M1) = {q(t, "years")} (A1).', 3)
    if frame == 1:
        n = rng.choice([3, 5, 10])
        return num(f'Determine the fraction of the original activity of {nm} remaining after {n} half-lives, and the time this takes.',
                   f'{sf(0.5 ** n, 3)}; {q(n * T, "years")}', f'(1/2)^{n} = {sf(0.5 ** n, 3)} (A1); t = {n} × {sf(T, 3)} y = {q(n * T, "years")} (A1).', 2)
    P = rng.choice([1000, 3000]) * 1e6
    frac_ = rng.choice([0.065, 0.015, 0.006])
    tl = {0.065: 'immediately after shutdown', 0.015: 'one hour after shutdown', 0.006: 'one day after shutdown'}[frac_]
    m_water = P * frac_ / (4200 * 80)
    return num(f'Decay heat {tl} is about {frac_ * 100:g} % of a reactor’s full thermal power of {sf(P / 1e6, 3)} MW. Calculate the decay power and the mass of cooling water per second needed if the water warms by 80 K (c = 4200 J kg⁻¹ K⁻¹).',
               f'{q(P * frac_, "W")}; {q(m_water, "kg s⁻¹")}', f'P_decay = {frac_} × {sf(P)} = {q(P * frac_, "W")} (A1); P = ṁcΔT (M1) → ṁ = {q(m_water, "kg s⁻¹")} (A1).', 3)


R.mcqs('ch11-st3', 'C2', (1, 4), [
    ('Why is spent nuclear fuel more radioactive than fresh fuel?', 'it contains many short-lived, neutron-rich fission products and transuranic elements', ['it contains more uranium-235', 'it has been heated', 'it has absorbed protons'], 'Fission products are highly active.'),
    ('Iodine tablets are distributed after a reactor accident to', 'saturate the thyroid with stable iodine so less radioactive I-131 is absorbed', ['neutralise radiation', 'speed up the decay of I-131', 'absorb gamma rays'], 'Blocking uptake.'),
    ('Which design feature makes a reactor safer if coolant is lost?', 'a negative void coefficient, so reactivity falls as water boils', ['a positive void coefficient', 'graphite control rod tips', 'removing containment buildings'], 'Loss of moderation shuts the reaction down.'),
])

R.mcqs('ch11-st3', 'C3', (1, 4), [
    ('Strontium-90 has a half-life of 29 years. Approximately how long until its activity falls to 1/16 of its initial value?', '116 years', ['58 years', '464 years', '29 years'], '4 half-lives.'),
    ('A waste sample’s activity falls from 8000 Bq to 1000 Bq in 90 years. Its half-life is', '30 years', ['45 years', '11 years', '90 years'], 'Three halvings in 90 y.'),
    ('Plutonium-239 (half-life 24 100 years) must decay to about 0.1 % of its activity. This takes roughly', '240 000 years', ['24 000 years', '2400 years', '2.4 million years'], '≈ 10 half-lives (2⁻¹⁰ ≈ 0.001).'),
])

R.static('ch11-st3', 'C4', (3, 5), [
    ('Evaluate deep geological disposal as a solution for high-level nuclear waste, referring to the half-lives involved, the engineered and natural barriers, and the ethical issue of responsibility to future generations.',
     'Waste contains fission products (Cs-137, Sr-90, ~30 y) and actinides (Pu-239, 24 100 y), so isolation for ~10⁵ years is needed. Multiple barriers: vitrified waste or ceramic fuel, corrosion-resistant canisters (copper/steel), bentonite clay buffer, and stable rock with slow groundwater flow. Strengths: passive safety, no need for active management; Finland’s Onkalo is operating. Limitations: uncertainty in predicting geology and climate over 100 000 years, communicating danger to future people, public opposition. Ethical: the generation that benefits from the power should deal with its waste, but also not foreclose future options (retrievability).',
     'Half-lives linked to timescale (A1); barriers described (R1 R1); strength with example (R1); limitation/uncertainty (R1); ethical judgement (A1).', 6),
], type='multi_step', marks=6)


# =============================================================================================
# ch12 E.5 Fusion and stars
# =============================================================================================
STARS = [('Sirius A', 9500, 25.4, 2.64), ('Betelgeuse', 3500, 1.0e5, 168), ('Vega', 9600, 40, 7.7), ('Proxima Centauri', 3040, 0.0017, 1.30),
         ('Rigel', 12100, 1.2e5, 264), ('Aldebaran', 3900, 440, 20.0), ('Polaris', 6000, 1260, 133), ('Barnard’s Star', 3130, 0.0035, 1.83),
         ('Arcturus', 4290, 170, 11.3), ('Spica', 22400, 2.0e4, 77)]

R.facts('ch12-st1', F(
    terms=[('nuclear fusion', 'the joining of two light nuclei to form a heavier nucleus, releasing energy when the product has a greater binding energy per nucleon'),
           ('stellar equilibrium', 'the balance in a main-sequence star between the inward gravitational force and the outward pressure of hot gas and radiation'),
           ('proton–proton chain', 'the sequence of fusion reactions by which stars like the Sun convert four protons into a helium-4 nucleus, releasing about 26.7 MeV'),
           ('plasma', 'a state of matter of separated nuclei and electrons at very high temperatures, as in stellar cores and fusion reactors')],
    facts=[('Fusion requires extremely high temperatures because', 'nuclei must move fast enough to overcome their electric repulsion and come within range of the strong force', ['electrons must be removed by heating', 'the strong force is repulsive', 'neutrons are only produced when hot'], 'Coulomb barrier.'),
           ('The net result of the proton–proton chain is', '4 ¹H → ⁴He + 2e⁺ + 2νₑ + energy', ['2 ¹H → ²H + energy only', '¹H + ¹H → ⁴He', '⁴He → 4 ¹H'], 'Four protons → helium-4.'),
           ('A main-sequence star is stable because', 'gravitational contraction is balanced by thermal and radiation pressure from fusion', ['it is not rotating', 'it has stopped fusing', 'its magnetic field holds it together'], 'Hydrostatic equilibrium.'),
           ('Fusion in the core of the Sun occurs at a temperature of about', '1.5 × 10⁷ K', ['5800 K', '10⁴ K', '10¹² K'], 'Core temperature ~15 million K.')],
    why=[('Explain why fusion of hydrogen in stars is possible at temperatures lower than those predicted classically for overcoming the Coulomb barrier.', 'Quantum tunnelling allows nuclei with less energy than the barrier height to fuse with a small probability; with the enormous number of nuclei in the core, enough reactions occur.'),
         ('Explain how a main-sequence star responds if its core temperature rises slightly.', 'The fusion rate increases, raising the pressure; the core expands and cools, reducing the fusion rate again – a negative feedback that keeps the star stable.'),
         ('Explain why fusion is difficult to achieve in a reactor on Earth.', 'Temperatures above 10⁸ K are needed (higher than the Sun’s core, because densities are lower); the plasma must be confined (by magnetic fields in a tokamak) long enough and at high enough density, while no material container can touch it.')],
    contrast=[('nuclear fusion', 'nuclear fission', 'Fusion joins light nuclei (left of the BE/A peak) and needs extreme temperatures to overcome repulsion; fission splits heavy nuclei (right of the peak), triggered by neutrons at room temperature; both release energy from increases in binding energy per nucleon.')],
    misc=[('Stars shine by burning hydrogen in a chemical reaction with oxygen.', 'Stars release energy by nuclear fusion of hydrogen into helium, millions of times more energy per kg than any chemical reaction.'),
          ('Gravity and radiation pressure balance because they are equal and opposite forces from fusion.', 'Gravity pulls inward from the star’s mass; the outward pressure gradient comes from hot gas and radiation heated by fusion; they balance at each layer (hydrostatic equilibrium).')],
    evaluate=[('Fusion power will solve the world’s energy problems within the next decade.', ['abundant fuel (deuterium from water, tritium bred from lithium)', 'no long-lived high-level waste or runaway chain reaction', 'recent milestones such as ignition at NIF in 2022'], ['net energy gain for a whole power plant has not been achieved', 'materials damaged by 14 MeV neutrons', 'tritium supply and engineering challenges', 'ITER first plasma delayed into the 2030s'], 'Fusion is promising in the long term, but technical and economic barriers make a decade far too optimistic.')],
))


@R.add('ch12-st1', 'C3', (1, 5), 'numerical')
def c3_fusion(rng, slot):
    frame = rng.randrange(4)
    if frame == 0:
        L = L_SUN * rng.choice([1, 1, 25.4, 0.0017, 40]) if rng.random() < 0.5 else L_SUN
        dm = L / C ** 2
        return num(f'A star has a luminosity of {q(L, "W")}. Calculate the rate at which it loses mass by converting mass into radiated energy.',
                   q(dm, 'kg s⁻¹'), f'Δm/Δt = L/c² (M1) = {q(L, "W")}/(3.00 × 10⁸)² = {q(dm, "kg s⁻¹")} (A1).', 2)
    if frame == 1:
        md, mt, ma, mn = 2.013553, 3.015501, 4.001506, 1.008665
        Q = (md + mt - ma - mn) * UMEV
        return num(f'In the D–T fusion reaction ²H + ³H → ⁴He + ¹n, the nuclear masses are: ²H {md} u, ³H {mt} u, ⁴He {ma} u, neutron {mn} u. Calculate the energy released in MeV.',
                   q(Q, 'MeV'), f'Δm = ({md} + {mt}) − ({ma} + {mn}) = {sf(md + mt - ma - mn, 4)} u (M1 A1); E = Δm × 931.5 = {q(Q, "MeV")} (A1).', 3)
    if frame == 2:
        Q = 26.7
        L = L_SUN
        rate = L / (Q * 1e6 * EV)
        return num('Each completion of the proton–proton chain releases 26.7 MeV. Calculate the number of helium nuclei produced per second in the Sun (luminosity 3.83 × 10²⁶ W) and the rate of hydrogen consumption in kg s⁻¹.',
                   f'{q(rate, "s⁻¹")}; {q(rate * 4 * MP, "kg s⁻¹")}', f'26.7 MeV = {q(Q * 1e6 * EV, "J")} (A1); N = L/E = {q(rate, "s⁻¹")} (M1 A1); 4 protons each: {q(rate * 4 * MP, "kg s⁻¹")} (A1).', 4)
    T = rng.choice([1.5e7, 1.0e8, 1.5e8])
    Ek = 1.5 * 1.38e-23 * T
    d = K * E * E / (2 * Ek)
    return num(f'Two protons approach head-on, each with the mean kinetic energy (3/2)k_BT at T = {q(T, "K")} (k_B = 1.38 × 10⁻²³ J K⁻¹). Estimate their distance of closest approach and comment on whether fusion is possible classically.',
               f'{q(d, "m")}; far larger than ~10⁻¹⁵ m, so fusion requires tunnelling (or higher energies)', f'Eₖ each = {q(Ek, "J")} (A1); 2Eₖ = ke²/d (M1); d = {q(d, "m")} (A1); compare with range of strong force (R1).', 4)


@R.add('ch12-st1', 'C3', (1, 4), 'mcq')
def c3_fusion_mcq(rng, slot):
    L = rng.choice([1.0, 2.0, 4.0, 3.83]) * 1e26
    dm = L / C ** 2
    return nmcq(rng, f'A star radiates energy at {q(L, "W")}. At what rate does it lose mass?', dm,
                [L / C, L * C ** 2 / 1e40, L / (2 * C ** 2)], 'kg s⁻¹', f'Δm/Δt = L/c² = {q(dm, "kg s⁻¹")}.', extra=True)


R.mcqs('ch12-st1', 'C2', (1, 4), [
    ('If the rate of fusion in a star’s core decreased, the core would', 'contract and heat up, increasing the fusion rate again', ['expand and cool further', 'explode', 'stop fusing permanently'], 'Negative feedback.'),
    ('Why is deuterium–tritium fusion chosen for reactors rather than proton–proton fusion?', 'it has a much higher reaction rate at achievable temperatures', ['it releases no neutrons', 'it needs no confinement', 'it is a fission reaction'], 'p–p fusion needs the weak interaction and is extremely slow.'),
    ('A tokamak confines plasma using', 'strong magnetic fields', ['gravitational fields', 'solid steel walls in contact with the plasma', 'electric fields only'], 'Charged particles spiral along field lines.'),
])

R.static('ch12-st1', 'C4', (3, 5), [
    ('Explain how a main-sequence star like the Sun maintains stellar equilibrium, and discuss what happens to this equilibrium when hydrogen in the core is exhausted.',
     'At every layer the inward gravitational force on the gas is balanced by the outward force due to the pressure gradient of hot gas and radiation, maintained by energy from hydrogen fusion in the core (negative feedback stabilises the rate). When core hydrogen runs out, fusion there stops, pressure falls and the core contracts and heats; hydrogen fusion begins in a shell around the core and the outer layers expand and cool (red giant). Eventually the core becomes hot enough (~10⁸ K) for helium fusion.',
     'Forces identified (A1); energy source and feedback (R1); core contraction when H exhausted (R1); shell burning and envelope expansion (R1); helium ignition (R1).'),
], type='multi_step', marks=5)


def lum_class(T, Lr):
    if Lr > 5000 and T < 5000:
        return 'red supergiant'
    if Lr > 1e4:
        return 'supergiant'
    if Lr > 50 and T < 5500:
        return 'red giant'
    if Lr < 0.01 and T > 6000:
        return 'white dwarf'
    return 'main-sequence star'


R.facts('ch12-st2', F(
    terms=[('Hertzsprung–Russell (HR) diagram', 'a plot of stellar luminosity against surface temperature (decreasing to the right), on which stars fall into groups such as the main sequence, giants, supergiants and white dwarfs'),
           ('main sequence', 'the band on the HR diagram from hot luminous stars to cool dim stars, occupied by stars fusing hydrogen in their cores'),
           ('red giant', 'a large, cool, luminous star in a late stage of evolution, fusing hydrogen in a shell around a helium core'),
           ('white dwarf', 'a small, hot, dense remnant of a low-mass star, supported by electron degeneracy pressure, no longer fusing')],
    facts=[('On a standard HR diagram, the temperature axis', 'increases to the left', ['increases to the right', 'is linear starting at zero', 'shows apparent brightness'], 'Convention from spectral classes O B A F G K M.'),
           ('A star at the top right of the HR diagram is', 'cool and very luminous, so very large (a red supergiant)', ['hot and dim', 'a white dwarf', 'a main-sequence star like the Sun'], 'L = σ4πR²T⁴: large L with low T needs large R.'),
           ('White dwarfs are found', 'at the bottom left of the HR diagram', ['at the top right', 'in the middle of the main sequence', 'at the top left'], 'Hot but small, so low luminosity.'),
           ('The Sun will eventually become', 'a red giant and then a white dwarf', ['a neutron star', 'a black hole', 'a supernova'], 'Its mass is below the Chandrasekhar limit.')],
    why=[('Explain why red giants are more luminous than the Sun although their surface temperature is lower.', 'L = 4πR²σT⁴; a red giant’s radius is tens to hundreds of times the Sun’s, so its surface area is enormous, more than compensating for the lower T⁴.'),
         ('Explain why stars spend most of their lives on the main sequence.', 'Core hydrogen fusion is a long-lasting, stable energy source; later stages (helium and heavier fusion) release less energy per kg and proceed much faster, so a star spends ~90 % of its life on the main sequence.'),
         ('Explain why the position of a main-sequence star on the HR diagram is determined mainly by its mass.', 'More massive stars need higher core pressure and temperature to support themselves, so they fuse faster, giving higher luminosity (L ∝ M^3.5) and higher surface temperature.')],
    contrast=[('a red giant', 'a white dwarf', 'A red giant is a large, cool, luminous star still undergoing fusion in a shell; a white dwarf is a small, hot, dim stellar remnant that is no longer fusing and slowly cools.'),
              ('the evolution of a low-mass star', 'the evolution of a high-mass star', 'Low-mass stars (< ~8 M☉) become red giants, shed planetary nebulae and leave white dwarfs; high-mass stars become red supergiants, fuse up to iron, explode as supernovae and leave neutron stars or black holes.')],
    misc=[('The HR diagram shows how a single star moves along the main sequence as it ages.', 'Stars stay at almost the same place on the main sequence while fusing core hydrogen; they leave it (towards giants) when core hydrogen runs out.'),
          ('All red stars are small and dim.', 'Red dwarfs are small and dim, but red giants and supergiants are red (cool) and extremely luminous because they are huge.')],
    evaluate=[('The HR diagram is the most important single tool in stellar astrophysics.', ['shows stellar groups and evolution', 'allows distances by spectroscopic parallax', 'cluster HR diagrams give ages (turn-off point)'], ['it summarises but does not explain; models of nuclear fusion and stellar structure are needed', 'requires accurate distances and luminosities'], 'It is a central organising tool that, combined with physical models, underpins our understanding of stellar evolution.')],
))


@R.add('ch12-st2', 'C3', (1, 5), 'numerical')
def c3_hr(rng, slot):
    st, T, Lr, Rr = pick(rng, STARS)
    frame = rng.randrange(4)
    if frame == 0:
        lm = WIEN / T
        return num(f'The surface temperature of {st} is about {T} K. Calculate the wavelength at which its emission peaks, and state its colour.',
                   f'{q(lm * 1e9, "nm")}; {"blue-white" if T > 8000 else "white" if T > 6500 else "yellow-white" if T > 5200 else "orange" if T > 3800 else "red"}',
                   f'λ_max = b/T = 2.90 × 10⁻³/{T} (M1) = {q(lm * 1e9, "nm")} (A1); colour (A1).', 3)
    if frame == 1:
        R_ = math.sqrt(Lr * L_SUN / (4 * math.pi * SIGMA * T ** 4))
        cls = lum_class(T, Lr)
        return num(f'{st} has a luminosity of {sf(Lr, 3)} L☉ (L☉ = 3.83 × 10²⁶ W) and a surface temperature of {T} K. Calculate its radius and deduce its type.',
                   f'{q(R_, "m")} ({sf(R_ / R_SUN, 3)} R☉); {cls}', f'L = 4πR²σT⁴ (M1); R = √(L/(4πσT⁴)) = {q(R_, "m")} (A1); ≈ {sf(R_ / R_SUN, 3)} R☉ → {cls} (R1).', 3)
    if frame == 2:
        lm = rng.choice([290, 400, 500, 725, 850, 1000])
        return num(f'The spectrum of a star peaks at {lm} nm. Calculate its surface temperature.', q(WIEN / (lm * 1e-9), 'K'),
                   f'T = b/λ_max (M1) = 2.90 × 10⁻³/{lm} × 10⁻⁹ = {q(WIEN / (lm * 1e-9), "K")} (A1).', 2)
    a, b_ = rng.sample(STARS, 2)
    ratioL = (a[3] / b_[3]) ** 2 * (a[1] / b_[1]) ** 4
    return num(f'{a[0]} has radius {a[3]} R☉ and temperature {a[1]} K; {b_[0]} has radius {b_[3]} R☉ and temperature {b_[1]} K. Calculate the ratio of their luminosities L({a[0]})/L({b_[0]}).',
               sf(ratioL, 3), f'L ∝ R²T⁴ (M1); ratio = ({a[3]}/{b_[3]})² × ({a[1]}/{b_[1]})⁴ (M1) = {sf(ratioL, 3)} (A1).', 3)


@R.add('ch12-st2', 'C3', (1, 4), 'mcq')
def c3_hr_mcq(rng, slot):
    lm = rng.choice([250, 300, 400, 500, 600, 800])
    T = WIEN / (lm * 1e-9)
    return nmcq(rng, f'The peak wavelength in the spectrum of a star is {lm} nm. What is its surface temperature?', T,
                [lm * 1e-9 / WIEN * 1e10, WIEN * lm * 1e-9 * 1e15, T / 2], 'K', f'T = 2.90 × 10⁻³/λ_max = {q(T, "K")}.', extra=True)


@R.add('ch12-st2', 'C2', (2, 4), 'explain')
def c2_hr_place(rng, slot):
    st, T, Lr, Rr = pick(rng, STARS)
    cls = lum_class(T, Lr)
    return dict(stem=f'{st} has a surface temperature of {T} K and a luminosity of {sf(Lr, 2)} L☉. State its region on the HR diagram and explain what this tells you about its size and stage of evolution.',
                answer=f'{cls}; radius ≈ {sf(Rr, 2)} R☉',
                markingKey=f'Region: {cls} (A1); size inferred from L = 4πR²σT⁴ (R1); evolutionary stage consistent with region (R1).', type='explain', marks=3)


R.mcqs('ch12-st2', 'C2', (1, 4), [
    ('Two stars have the same surface temperature, but star P is 100 times more luminous than star Q. The ratio of their radii R_P/R_Q is', '10', ['100', '10 000', '2.5'], 'L ∝ R² at fixed T.'),
    ('The "turn-off point" of a star cluster’s HR diagram is used to estimate', 'the age of the cluster', ['its distance only', 'its chemical composition', 'the temperature of its gas'], 'More massive stars leave the main sequence first.'),
    ('A star with three times the Sun’s mass leaves the main sequence. It will next become', 'a red giant', ['a white dwarf directly', 'a black hole directly', 'a brown dwarf'], 'Shell burning makes the envelope expand.'),
])

R.static('ch12-st2', 'C4', (3, 5), [
    ('Sketch an HR diagram with labelled axes and use it to describe the evolutionary path of (a) a star of 1 M☉ and (b) a star of 15 M☉, from the main sequence to their final states.',
     'Axes: luminosity (log, L☉) against temperature (log, decreasing to the right). (a) 1 M☉: main sequence near 5800 K, 1 L☉ for ~10¹⁰ y → moves up and right to red giant branch → helium flash and horizontal branch → asymptotic giant branch → ejects planetary nebula → white dwarf at bottom left, cooling. (b) 15 M☉: upper-left main sequence (~30 000 K, ~10⁴ L☉) for ~10⁷ y → moves right across to red supergiant, fusing successively heavier elements to iron → core collapse supernova → neutron star (or black hole), off the diagram.',
     'Correct axes with scale direction (A1); 1 M☉ path with stages (R1 R1); 15 M☉ path with stages (R1 R1); final states and reasons (mass limits) (A1).', 6),
], type='multi_step', marks=6)


R.facts('ch12-st3', F(
    terms=[('luminosity', 'the total power radiated by a star, L = σAT⁴ = 4πR²σT⁴'),
           ('apparent brightness', 'the power received per unit area at the observer, b = L/(4πd²)'),
           ('stellar parallax', 'the apparent shift in position of a nearby star against distant background stars as Earth orbits the Sun; distance d (pc) = 1/p (arcsec)'),
           ('parsec', 'the distance at which a star has a parallax angle of one arcsecond, 1 pc = 3.26 ly = 3.09 × 10¹⁶ m')],
    facts=[('A star’s parallax angle is 0.25 arcseconds. Its distance is', '4.0 pc', ['0.25 pc', '25 pc', '13 ly'], 'd = 1/p.'),
           ('If the distance to a star doubles, its apparent brightness', 'falls to one quarter', ['halves', 'is unchanged', 'doubles'], 'b ∝ 1/d².'),
           ('Stellar parallax is limited to relatively nearby stars because', 'parallax angles of distant stars are too small to measure', ['distant stars do not move', 'light from distant stars is red-shifted', 'distant stars are too hot'], 'p ∝ 1/d.'),
           ('The unit of apparent brightness is', 'W m⁻²', ['W', 'W m⁻¹', 'lm'], 'Power per unit area.')],
    why=[('Explain why the parallax method only works for stars within a few thousand parsecs, even with space telescopes.', 'Parallax angles fall as 1/d; beyond a few kiloparsecs they are smaller than ~10⁻⁴ arcsec, comparable to the measurement precision even for Gaia, so the distance uncertainty becomes too large.'),
         ('Explain why two stars with the same apparent brightness need not have the same luminosity.', 'b = L/(4πd²); a more luminous star further away can appear as bright as a less luminous star nearby, so distance must also be known.'),
         ('Explain how the luminosity, temperature and radius of a star are linked.', 'A star approximates a black body, so its luminosity equals σT⁴ multiplied by its surface area 4πR²; knowing any two quantities gives the third.')],
    contrast=[('luminosity', 'apparent brightness', 'Luminosity (W) is the intrinsic total power output of a star; apparent brightness (W m⁻²) is the power per unit area received at a distance d, b = L/(4πd²).'),
              ('a parsec', 'a light-year', 'A light-year is the distance light travels in a year (9.46 × 10¹⁵ m); a parsec is defined by a parallax of one arcsecond (3.09 × 10¹⁶ m = 3.26 ly).')],
    misc=[('The brightest stars in the night sky are the most luminous.', 'Apparent brightness depends on both luminosity and distance; many bright stars (e.g. Sirius) appear bright mainly because they are close.'),
          ('A star with twice the parallax angle is twice as far away.', 'd = 1/p: twice the parallax means half the distance.')],
    evaluate=[('Parallax is the foundation of all astronomical distance measurements.', ['it is a direct geometric method with no assumptions about stars', 'it calibrates Cepheid variables and other standard candles (the distance ladder)'], ['it only reaches nearby stars', 'galaxy distances need standard candles and redshift', 'errors propagate up the ladder'], 'It is the essential first rung of the distance ladder, though other methods are needed beyond our galaxy.')],
))


@R.add('ch12-st3', 'C3', (1, 5), 'numerical')
def c3_lum(rng, slot):
    st, T, Lr, Rr = pick(rng, STARS)
    frame = rng.randrange(5)
    if frame == 0:
        p = rng.choice([0.379, 0.768, 0.130, 0.0889, 0.0075, 0.0476])
        d = 1 / p
        return num(f'The parallax angle of a star is {p} arcseconds. Calculate its distance in parsecs, light-years and metres.',
                   f'{sf(d, 3)} pc = {sf(d * 3.26, 3)} ly = {q(d * PC, "m")}', f'd = 1/p (M1) = {sf(d, 3)} pc (A1); ×3.26 = {sf(d * 3.26, 3)} ly; ×3.09 × 10¹⁶ = {q(d * PC, "m")} (A1).', 3)
    if frame == 1:
        L = Lr * L_SUN
        d_pc = rng.choice([2.6, 7.7, 11.3, 20.0, 77.0, 133])
        b = L / (4 * math.pi * (d_pc * PC) ** 2)
        return num(f'{st} has a luminosity of {q(L, "W")} and is {d_pc} pc away. Calculate its apparent brightness at Earth.',
                   q(b, 'W m⁻²'), f'd = {q(d_pc * PC, "m")} (A1); b = L/(4πd²) (M1) = {q(b, "W m⁻²")} (A1).', 3)
    if frame == 2:
        R_ = Rr * R_SUN
        L = 4 * math.pi * R_ ** 2 * SIGMA * T ** 4
        return num(f'{st} has a radius of {sf(Rr, 3)} R☉ (R☉ = 6.96 × 10⁸ m) and a surface temperature of {T} K. Calculate its luminosity.',
                   q(L, 'W'), f'L = 4πR²σT⁴ (M1) with R = {q(R_, "m")} (A1) = {q(L, "W")} (A1).', 3)
    if frame == 3:
        b = rng.choice([1.2, 2.5, 5.0, 8.0]) * 10 ** rng.choice([-9, -10, -11])
        d_pc = rng.choice([5, 10, 25, 50])
        L = b * 4 * math.pi * (d_pc * PC) ** 2
        return num(f'A star {d_pc} pc away has an apparent brightness of {q(b, "W m⁻²")}. Determine its luminosity in watts and in solar luminosities.',
                   f'{q(L, "W")} = {sf(L / L_SUN, 3)} L☉', f'L = 4πd²b (M1) = {q(L, "W")} (A1); /3.83 × 10²⁶ = {sf(L / L_SUN, 3)} L☉ (A1).', 3)
    a, b_ = rng.sample(STARS, 2)
    k = rng.choice([2, 4, 10])
    return num(f'Two stars appear equally bright from Earth. Star X is {k} times further away than star Y. Determine the ratio of their luminosities L_X/L_Y, and if both have the same temperature, the ratio of their radii.',
               f'L ratio {k * k}; radius ratio {k}', f'b = L/(4πd²) equal → L ∝ d² (M1): {k}² = {k * k} (A1); same T → L ∝ R² → R ratio {k} (A1).', 3)


@R.add('ch12-st3', 'C3', (1, 4), 'mcq')
def c3_lum_mcq(rng, slot):
    p = rng.choice([0.1, 0.2, 0.25, 0.5, 0.05])
    d = 1 / p
    return nmcq(rng, f'A star has a parallax angle of {p} arcsec. What is its distance?', d,
                [p, d * 3.26, 2 * d], 'pc', f'd (pc) = 1/p (arcsec) = {q(d, "pc")}; ×3.26 would give light-years.', extra=False)


R.mcqs('ch12-st3', 'C2', (1, 4), [
    ('Star A has twice the radius and the same temperature as star B. The luminosity of A is', '4 times that of B', ['2 times', '16 times', 'the same'], 'L ∝ R².'),
    ('Star A has the same radius as star B but twice the surface temperature. The luminosity of A is', '16 times that of B', ['2 times', '4 times', '8 times'], 'L ∝ T⁴.'),
    ('Why are parallax measurements made six months apart?', 'Earth is then at opposite ends of its orbit, giving the largest baseline (2 AU)', ['the star moves in six months', 'the sky is darker', 'the Sun is closest to the star'], 'Maximum baseline.'),
])

R.static('ch12-st3', 'C4', (3, 5), [
    ('The star Vega has a parallax of 0.130 arcsec, an apparent brightness of 2.2 × 10⁻⁸ W m⁻² and a peak emission wavelength of 302 nm. (a) Determine its distance. (b) Determine its luminosity. (c) Determine its surface temperature and radius. (d) State its likely position on the HR diagram.',
     '(a) d = 7.69 pc = 2.38 × 10¹⁷ m; (b) L = 4πd²b = 1.6 × 10²⁸ W (≈ 41 L☉); (c) T = 2.90 × 10⁻³/302 × 10⁻⁹ = 9600 K; R = √(L/4πσT⁴) = 1.6 × 10⁹ m (≈ 2.3 R☉); (d) upper main sequence (A-type star).',
     'd = 1/p converted to m (A1); L (M1 A1); T by Wien (A1); R from Stefan–Boltzmann (A1); main sequence (R1).', 6),
], type='multi_step', marks=6)


def _sb_spec(rng):
    Ts = [1200, 1400, 1600, 1800, 2000, 2200]
    A = rng.choice([2.0, 3.0, 4.0]) * 1e-5
    eps = rng.choice([0.30, 0.35, 0.40])
    Ps = [round(eps * SIGMA * A * T_ ** 4 * rng.uniform(0.97, 1.03), 2) for T_ in Ts]
    return dict(intro=f'A student tests the Stefan–Boltzmann law using a filament lamp of surface area {q(A, "m²")}; the filament temperature T is estimated from its resistance and the power P supplied is measured. Theory: P = eσAT⁴, where e is the emissivity.',
                xname='T', xunit='K', yname='P', yunit='W', xs=Ts, ys=Ps, xfmt=lambda a: f'{a}', yfmt=lambda b: f'{b:.2f}',
                plot_x=lambda a: a ** 4, plot_y=lambda b: b, plot_label='P (y) against T⁴ (x)', what='the emissivity e of the filament', what_short='the emissivity',
                gunit='W K⁻⁴', deduce=lambda m_, b_: (m_ / (SIGMA * A), '', 'e = gradient/(σA)'))


gradient_fit('ch12-st3', _sb_spec)


R.facts('ch12-st4', F(
    terms=[('main-sequence lifetime', 'the time a star spends fusing hydrogen in its core, approximately proportional to M/L and hence to M^(−2.5)'),
           ('mass–luminosity relation', 'for main-sequence stars, luminosity is approximately proportional to mass to the power 3.5, L ∝ M^3.5'),
           ('Chandrasekhar limit', 'the maximum mass (about 1.4 M☉) of a white dwarf that can be supported by electron degeneracy pressure'),
           ('neutron star', 'an extremely dense stellar remnant of about 1.4–3 M☉ supported by neutron degeneracy pressure, formed in a core-collapse supernova')],
    facts=[('A main-sequence star has twice the Sun’s mass. Its luminosity is about', '11 L☉', ['2 L☉', '4 L☉', '0.18 L☉'], '2^3.5 ≈ 11.3.'),
           ('More massive main-sequence stars have', 'shorter lifetimes', ['longer lifetimes', 'the same lifetime', 'lower luminosity'], 'Lifetime ∝ M^−2.5.'),
           ('A stellar core remnant of 2 M☉ will become', 'a neutron star', ['a white dwarf', 'a red giant', 'a main-sequence star'], 'Above 1.4 M☉ (Chandrasekhar) but below ~3 M☉ (Oppenheimer–Volkoff).'),
           ('A white dwarf is prevented from collapsing by', 'electron degeneracy pressure', ['radiation pressure from fusion', 'neutron degeneracy pressure', 'magnetic pressure'], 'Pauli exclusion principle for electrons.')],
    why=[('Explain why more massive stars have shorter main-sequence lifetimes even though they have more fuel.', 'Lifetime ∝ fuel/rate ∝ M/L; since L ∝ M^3.5 the luminosity increases much faster than the mass, so lifetime ∝ M^−2.5 decreases with mass.'),
         ('Explain why a remnant core above about 3 M☉ becomes a black hole.', 'Above the Oppenheimer–Volkoff limit not even neutron degeneracy pressure can resist gravity, so the core collapses until its escape speed exceeds c and an event horizon forms.'),
         ('Explain why elements heavier than iron are not produced by fusion in stellar cores.', 'Fusing nuclei beyond iron decreases binding energy per nucleon and absorbs energy; heavier elements are made by neutron capture (s- and r-processes) in giant stars, supernovae and neutron-star mergers.')],
    contrast=[('a white dwarf', 'a neutron star', 'A white dwarf (≤ 1.4 M☉, Earth-sized) is supported by electron degeneracy pressure; a neutron star (1.4–3 M☉, ~10 km radius) is supported by neutron degeneracy pressure and is far denser.')],
    misc=[('The most massive stars live the longest because they have the most hydrogen.', 'Massive stars burn their fuel so fast (L ∝ M^3.5) that they live much shorter lives (∝ M^−2.5).'),
          ('The Sun will end its life as a black hole.', 'The Sun’s core remnant will be well below 1.4 M☉, so it will become a white dwarf.')],
    evaluate=[('Supernovae are essential for the existence of life on Earth.', ['they disperse elements made in stars (C, O, Fe) into space', 'r-process elements formed in explosive events', 'shock waves may trigger star formation (possibly the Solar System)'], ['many heavy elements also come from neutron-star mergers and AGB stars', 'nearby supernovae can be harmful to life'], 'Supernovae are a major source of the heavy elements and dispersal needed for rocky planets and life, though not the only source.')],
))


@R.add('ch12-st4', 'C3', (1, 5), 'numerical')
def c3_lifetime(rng, slot):
    M = rng.choice([0.5, 0.8, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0])
    frame = rng.randrange(4)
    if frame == 0:
        Lr = M ** 3.5
        return num(f'Use the mass–luminosity relation L ∝ M^3.5 to estimate the luminosity of a main-sequence star of {M} M☉, in terms of L☉.',
                   f'{sf(Lr, 3)} L☉', f'L/L☉ = ({M})^3.5 (M1) = {sf(Lr, 3)} (A1).', 2)
    if frame == 1:
        t = 1.0e10 * M ** -2.5
        return num(f'The Sun’s main-sequence lifetime is about 1.0 × 10¹⁰ years. Estimate the main-sequence lifetime of a star of {M} M☉, given L ∝ M^3.5.',
                   q(t, 'years'), f'Lifetime ∝ M/L ∝ M^(−2.5) (M1 R1); t = 10¹⁰ × {M}^(−2.5) = {q(t, "years")} (A1).', 3)
    if frame == 2:
        Lr = rng.choice([5, 20, 100, 1000, 10000])
        Mm = Lr ** (1 / 3.5)
        return num(f'A main-sequence star has luminosity {Lr} L☉. Estimate its mass and the likely type of its final remnant.',
                   f'{sf(Mm, 3)} M☉; {"white dwarf" if Mm < 8 else "neutron star or black hole"}', f'M = L^(1/3.5) (M1) = {sf(Mm, 3)} M☉ (A1); {"low/intermediate mass → white dwarf" if Mm < 8 else "massive → supernova → neutron star/black hole"} (R1).', 3)
    Mc = rng.choice([0.6, 1.1, 1.8, 2.5, 4.0, 7.0])
    rem = 'white dwarf' if Mc < 1.4 else 'neutron star' if Mc < 3 else 'black hole'
    return num(f'After a star’s final stage, its collapsed core has a mass of {Mc} M☉. State and explain the type of remnant formed.',
               rem, f'Compare with the Chandrasekhar limit (1.4 M☉) and the Oppenheimer–Volkoff limit (~3 M☉) (M1); {Mc} M☉ → {rem} (A1); supported by {"electron degeneracy pressure" if rem == "white dwarf" else "neutron degeneracy pressure" if rem == "neutron star" else "nothing – collapse continues"} (R1).', 3)


@R.add('ch12-st4', 'C3', (1, 4), 'mcq')
def c3_life_mcq(rng, slot):
    M = rng.choice([2, 4, 9, 0.5])
    t = 1e10 * M ** -2.5
    return nmcq(rng, f'The Sun’s main-sequence lifetime is 10¹⁰ years. What is the approximate lifetime of a {M} M☉ star? (L ∝ M^3.5)', t,
                [1e10 * M ** -3.5, 1e10 / M, 1e10 * M ** 2.5], 'years', f'Lifetime ∝ M^−2.5 = 10¹⁰ × {M}^(−2.5) = {q(t, "years")}.', extra=False)


R.mcqs('ch12-st4', 'C2', (1, 4), [
    ('A star cluster contains only main-sequence stars below 2 M☉ plus many red giants. This suggests that', 'the cluster is old enough for stars above ~2 M☉ to have left the main sequence', ['the cluster is very young', 'massive stars never formed', 'the cluster is moving away'], 'Turn-off mass indicates age.'),
    ('Pulsars are evidence for the existence of', 'rapidly rotating neutron stars', ['white dwarfs', 'black holes', 'red giants'], 'Regular radio pulses from rotating, magnetised neutron stars.'),
    ('A Type Ia supernova occurs when', 'a white dwarf in a binary accretes mass and exceeds the Chandrasekhar limit', ['a red giant sheds its envelope', 'a neutron star cools', 'two main-sequence stars merge gently'], 'Thermonuclear explosion at ~1.4 M☉ – a standard candle.'),
])

R.static('ch12-st4', 'C4', (3, 5), [
    ('A star of 20 M☉ and a star of 0.5 M☉ form together in the same cloud. (a) Use L ∝ M^3.5 to compare their luminosities. (b) Compare their main-sequence lifetimes, given the Sun’s is 10¹⁰ years. (c) Describe and explain the different end states of the two stars. (d) Discuss whether either star could host a planet with life that evolved as on Earth.',
     '(a) L ratio = 40^3.5 ≈ 4 × 10⁵ (20 M☉: ~3.6 × 10⁴ L☉; 0.5 M☉: ~0.09 L☉); (b) 20 M☉: 10¹⁰ × 20^−2.5 ≈ 5.6 × 10⁶ y; 0.5 M☉: ≈ 5.7 × 10¹⁰ y; (c) the massive star becomes a red supergiant, explodes as a core-collapse supernova and leaves a neutron star or black hole; the low-mass star will eventually become a white dwarf (after ~10¹⁰+ years); (d) the 20 M☉ star lives far too briefly for complex life (Earth took ~4 × 10⁹ y); the 0.5 M☉ star lives long enough but its habitable zone is close in, with flares and tidal locking as complications.',
     'Luminosity ratio (A1); lifetimes (M1 A1); end states with mass limits (R1); evaluation of habitability using timescales (R1 R1).', 6),
], type='multi_step', marks=6)


# --- ch11 extra depth -------------------------------------------------------------------------
@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def c4_fission_energy(rng, slot):
    a, b = pick(rng, [f for f in FISSIONS if (f[0][0], f[0][1], f[0][2]) in BEA and (f[1][0], f[1][1], f[1][2]) in BEA] or FISSIONS[:1])
    n = 236 - a[2] - b[2]
    Q = BEA[a] * a[2] + BEA[b] * b[2] - BEA[('U', 92, 235)] * 235
    m = rng.choice([0.5, 1.0, 2.0])
    N = m / (235 * U)
    Etot = N * Q * 1e6 * EV
    dm = Etot / C ** 2
    return num(f'Uranium-235 undergoes the fission ¹₀n + ²³⁵U → {sup(a[2])}{a[0]} + {sup(b[2])}{b[0]} + {n} ¹₀n. Binding energies per nucleon: U-235 7.591 MeV, {a[0]}-{a[2]} {BEA[a]} MeV, {b[0]}-{b[2]} {BEA[b]} MeV. (a) Calculate the energy released per fission. (b) Determine the energy released if {m} kg of U-235 undergoes this fission. (c) Calculate the mass converted to energy and express it as a percentage of the fuel mass. (d) Explain why the released energy is mostly kinetic energy of the fragments.',
               f'(a) {sf(Q, 3)} MeV; (b) {q(Etot, "J")}; (c) {q(dm, "kg")} ({sf(100 * dm / m, 2)} %); (d) Coulomb repulsion between the two positively charged fragments',
               f'(a) Q = {a[2]}×{BEA[a]} + {b[2]}×{BEA[b]} − 235×7.591 (M1) = {sf(Q, 3)} MeV (A1). (b) N = {m}/(235 u) = {q(N, "")} (M1); E = {q(Etot, "J")} (A1). (c) Δm = E/c² = {q(dm, "kg")}, {sf(100 * dm / m, 2)} % (A1). (d) fragments repel electrically after scission (R1).', 6, 'multi_step', 'G5')


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def c4_critical(rng, slot):
    k = rng.choice([0.95, 0.98, 1.00, 1.02, 1.05])
    tau = rng.choice([1e-3, 0.1])
    t = rng.choice([1.0, 5.0, 10.0])
    gen = t / tau
    grow = k ** gen
    state = 'subcritical' if k < 1 else 'critical' if k == 1 else 'supercritical'
    return num(f'A reactor has an effective neutron multiplication factor k = {k} and an effective generation time of {q(tau, "s")}. (a) State whether the reactor is subcritical, critical or supercritical. (b) Determine the factor by which the fission rate changes in {sf(t, 2)} s. (c) Explain the role of delayed neutrons in making the reactor controllable, and how operators would respond.',
               f'(a) {state}; (b) ×{sf(grow, 3)}; (c) delayed neutrons from fission-product decay lengthen the effective generation time to ~0.1 s, giving time for control-rod adjustment',
               f'(a) k {"<" if k < 1 else "=" if k == 1 else ">"} 1 → {state} (A1). (b) number of generations = {sf(gen, 3)} (M1); factor = k^n = {sf(grow, 3)} (A1). (c) delayed neutrons (R1); operators insert/withdraw rods to restore k = 1 (R1).', 5, 'multi_step', 'G5')


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def c3_reactor_ops(rng, slot):
    frame = rng.randrange(3)
    if frame == 0:
        P = rng.choice([1500, 2500, 3000, 3400]) * 1e6
        dT = rng.choice([30, 35, 40])
        cw = 5500
        mdot = P / (cw * dT)
        return num(f'The coolant of a pressurised water reactor (specific heat capacity at operating conditions 5500 J kg⁻¹ K⁻¹) is heated by {dT} K as it passes through a core producing {sf(P / 1e6, 3)} MW. Calculate the mass flow rate of coolant required.',
                   q(mdot, 'kg s⁻¹'), f'P = ṁcΔT (M1); ṁ = {sf(P)}/(5500 × {dT}) = {q(mdot, "kg s⁻¹")} (A1).', 2)
    if frame == 1:
        Pt = rng.choice([2000, 3000, 3600]) * 1e6
        Pe = Pt * rng.choice([0.32, 0.34, 0.36])
        return num(f'A nuclear power station has a thermal power of {sf(Pt / 1e6, 3)} MW and an electrical output of {sf(Pe / 1e6, 3)} MW. Calculate its efficiency and the rate at which energy is transferred to the cooling water, and explain why this energy cannot be avoided.',
                   f'{sf(100 * Pe / Pt, 3)} %; {q(Pt - Pe, "W")}', f'η = {sf(Pe / 1e6, 3)}/{sf(Pt / 1e6, 3)} = {sf(100 * Pe / Pt, 3)} % (A1); waste = {q(Pt - Pe, "W")} (A1); heat engines must transfer energy to a cold reservoir (second law) (R1).', 3)
    Ef = 200e6 * EV
    P = rng.choice([1000, 3000]) * 1e6
    d = rng.choice([1, 7, 30])
    m = P * d * 86400 / Ef * 235 * U
    return num(f'Estimate the mass of uranium-235 fissioned in a reactor core producing {sf(P / 1e6, 3)} MW of thermal power for {d} day{"s" if d > 1 else ""} (200 MeV per fission).',
               q(m, 'kg'), f'E = Pt = {q(P * d * 86400, "J")} (A1); fissions = E/(3.20 × 10⁻¹¹ J) (M1); mass = N × 235 u = {q(m, "kg")} (A1).', 3)


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step')
def c4_moderator_design(rng, slot):
    mod = pick(rng, [('light water (hydrogen, 1 u)', 1), ('heavy water (deuterium, 2 u)', 2), ('graphite (carbon, 12 u)', 12), ('beryllium (9 u)', 9)])
    M = mod[1]
    keep = ((M - 1) / (M + 1)) ** 2
    if M == 1:
        keep = 0.5
        note = ' (for hydrogen, the average over all collision angles is about 50 %)'
    else:
        keep = (M ** 2 + 1) / (M + 1) ** 2
        note = ' (averaged over collision angles)'
    E0, Ef = 2.0e6, 0.025
    n = math.log(Ef / E0) / math.log(keep)
    return num(f'A reactor designer considers {mod[0]} as a moderator. In an average collision a neutron keeps a fraction f = {sf(keep, 3)} of its kinetic energy{note}. (a) Show that a head-on elastic collision with a nucleus of mass M u transfers the fraction 4M/(1 + M)² of the neutron’s energy. (b) Estimate the number of collisions needed to slow a 2.0 MeV neutron to 0.025 eV. (c) Other than the number of collisions, state and explain two properties the designer must consider.',
               f'(b) about {math.ceil(n)} collisions; (c) neutron absorption cross-section, cost/availability, ability to act as coolant, chemical/fire safety',
               f'(a) momentum and kinetic energy conservation for masses 1 and M (M1); v_n′ = (1 − M)/(1 + M)u, fraction transferred = 1 − ((1 − M)/(1 + M))² = 4M/(1 + M)² (A1). (b) n = ln(0.025/2.0 × 10⁶)/ln {sf(keep, 3)} (M1) ≈ {math.ceil(n)} (A1). (c) two valid properties with reasons (R1 R1).', 6, 'multi_step', 'G5')


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step')
def c4_waste_mix(rng, slot):
    A1, T1 = rng.choice([800, 1000, 1200]), 30.2
    A2, T2 = rng.choice([20, 40, 60]), 24100
    t = rng.choice([100, 300, 500, 1000])
    a1 = A1 * 0.5 ** (t / T1)
    a2 = A2 * 0.5 ** (t / T2)
    return num(f'A sample of vitrified waste contains caesium-137 (half-life 30.2 y) with activity {A1} GBq and plutonium-239 (half-life 24 100 y) with activity {A2} GBq. (a) Determine the activity of each after {t} years. (b) State which isotope dominates the activity at that time. (c) Explain why the long-term hazard of waste is dominated by actinides even though fission products are initially far more active. (d) Discuss one implication for repository design.',
               f'(a) Cs-137 {q(a1, "GBq")}, Pu-239 {q(a2, "GBq")}; (b) {"Cs-137" if a1 > a2 else "Pu-239"}; (c) short-lived fission products decay away within centuries; long half-life actinides remain; (d) barriers must last ~10⁵ years',
               f'(a) A = A₀(1/2)^(t/T½) for each (M1): {q(a1, "GBq")} and {q(a2, "GBq")} (A1 A1). (b) comparison (A1). (c) half-life argument (R1). (d) repository implication, e.g. long-lived containment, stable geology (R1).', 6, 'multi_step', 'G5')


R.static('ch11-st3', 'C4', (3, 5), [
    ('Compare the Chernobyl (1986) and Fukushima (2011) accidents in terms of their physical causes, the role of decay heat and reactor design, and the lessons learned for reactor safety.',
     'Chernobyl: an RBMK graphite-moderated reactor with a positive void coefficient; during a low-power test with safety systems disabled and most control rods withdrawn, steam voids raised reactivity, causing a power surge, steam explosion and graphite fire with large releases. Fukushima: boiling-water reactors shut down correctly when the earthquake struck, but the tsunami destroyed backup power, so decay heat (several % of full power) could not be removed; cores melted and hydrogen explosions released radioactivity. Lessons: inherent negative feedback (negative void coefficient), robust passive cooling and multiple independent power supplies, siting against natural hazards, independent regulation and safety culture.',
     'Chernobyl cause including void coefficient (R1 R1); Fukushima cause including decay heat (R1 R1); comparison of design factors (R1); lessons (A1).', 6),
    ('A town debates whether to accept a nuclear waste storage facility. Evaluate the scientific arguments for and against, using ideas about half-life, types of radiation and pathways to people.',
     'For: waste is solid and encapsulated, so alpha and beta emitters cannot reach people unless released; gamma is shielded by metres of rock; activity falls over time and the most active fission products (~30 y half-lives) fall by a factor of ~1000 in 300 years; monitored storage is safer than scattered surface stores. Against: actinides with half-lives of 10⁴–10⁵ years remain hazardous; leaks into groundwater could allow ingestion of alpha emitters (most damaging inside the body); transport risks; uncertainty over very long timescales. Judgement: risks are low if geology and engineering are sound, but long-term uncertainty and public trust matter.',
     'Half-life argument (R1); radiation types and shielding (R1); internal hazard of alpha (R1); groundwater/transport pathways (R1); balanced judgement (A1).', 5),
], type='multi_step', marks=6)


def _mod_spec(rng):
    f = rng.choice([0.84, 0.72, 0.63])
    ns = [0, 5, 10, 15, 20, 25]
    Es = [float(f'{2.0 * f ** n_ * rng.uniform(0.95, 1.05):.3g}') for n_ in ns]
    return dict(intro='A computer simulation tracks the mean kinetic energy E of neutrons after n collisions with nuclei of a moderator. Theory: E = E₀fⁿ, where f is the fraction of energy kept per collision.',
                xname='n', xunit='–', yname='E', yunit='MeV', xs=ns, ys=Es, xfmt=lambda a: f'{a}', yfmt=lambda b: sf(b, 3),
                plot_x=lambda a: a, plot_y=lambda b: math.log(b), plot_label='ln E (y) against n (x)', what='the fraction f of energy kept per collision', what_short='f',
                gunit='', deduce=lambda m_, b_: (math.exp(m_), '', 'f = e^(gradient)'))


gradient_fit('ch11-st2', _mod_spec)


@R.add('ch11-st3', 'C3', (1, 4), 'mcq')
def c3_waste_mcq(rng, slot):
    nm, T = pick(rng, [('caesium-137', 30), ('strontium-90', 29), ('americium-241', 432), ('cobalt-60', 5.3), ('krypton-85', 10.8)])
    n = rng.choice([2, 3, 4, 5, 6])
    A0 = rng.choice([1600, 3200, 6400, 12800])
    return nmcq(rng, f'Waste containing {nm} (half-life {T} years) has an activity of {A0} GBq. What is its activity after {sf(n * T, 3)} years?', A0 / 2 ** n,
                [A0 / (2 * n), A0 / 2 ** (n - 1), A0 * (1 - n / 10)], 'GBq', f'{n} half-lives: {A0}/2^{n} = {q(A0 / 2 ** n, "GBq")}.', extra=False)


@R.add('ch10-st4', 'C3', (1, 4), 'mcq')
def c3_absorb_mcq(rng, slot):
    if rng.random() < 0.5:
        C0 = rng.choice([900, 1600, 2500, 3600])
        r1 = rng.choice([10, 15, 20])
        k = rng.choice([2, 3, 4])
        return nmcq(rng, f'A gamma source gives a corrected count rate of {C0} counts per minute at {r1} cm from a detector. What is the corrected count rate at {r1 * k} cm?', C0 / k ** 2,
                    [C0 / k, C0 / k ** 3, C0 / (2 * k)], 'counts min⁻¹', f'Inverse-square law: {C0}/{k}² = {sf(C0 / k ** 2)}.', extra=False)
    x12 = rng.choice([0.8, 1.0, 1.2, 1.5])
    n = rng.choice([2, 3, 4])
    return nmcq(rng, f'The half-value thickness of lead for a gamma source is {x12} cm. What percentage of the gamma rays pass through {sf(n * x12, 2)} cm of lead?', 100 / 2 ** n,
                [100 / (2 * n), 100 - 100 / 2 ** n, 100 / 2 ** (n + 1)], '%', f'{n} half-value thicknesses: 100 %/2^{n} = {sf(100 / 2 ** n)} %.', extra=False)


# =============================================================================================
# Extra Paper 1A numerical MCQs (several frames each, numbers mid-stem for variety)
# =============================================================================================
def mframe(rng, frames):
    stem, v, wr, unit, key = pick(rng, frames)
    return nmcq(rng, stem, v, wr, unit, key, extra=True)


@R.add('ch02-st2', 'C3', (1, 4), 'mcq')
def m_harm(rng, slot):
    L = rng.choice([0.30, 0.40, 0.55, 0.65, 0.80, 1.10])
    v = rng.choice([330, 340, 345])
    n = rng.choice([2, 3, 4])
    vs = rng.choice([180, 250, 320, 400])
    return mframe(rng, [
        (f'An organ pipe {sf(L, 2)} m long is open at both ends; sound travels at {v} m s⁻¹ in the pipe. What is its fundamental frequency?', v / (2 * L), [v / (4 * L), v / L, 2 * v / L], 'Hz', f'Open pipe: f = v/2L = {q(v / (2 * L), "Hz")}.'),
        (f'Waves travel at {vs} m s⁻¹ on a {sf(L, 2)} m string fixed at both ends. What is the frequency of harmonic {n}?', n * vs / (2 * L), [n * vs / L, vs / (2 * L), n * vs / (4 * L)], 'Hz', f'f = nv/2L = {q(n * vs / (2 * L), "Hz")}.'),
        (f'A pipe closed at one end must have a fundamental of {sf(v / (4 * L), 3)} Hz when the speed of sound is {v} m s⁻¹. How long must it be?', L, [2 * L, L / 2, 4 * L], 'm', f'L = v/4f = {q(L, "m")}.'),
    ])


@R.add('ch04-st2', 'C3', (1, 4), 'mcq')
def m_g(rng, slot):
    b, M, Rb = pick(rng, BODIES)
    h = rng.choice([0.5, 1.0, 2.0, 3.0])
    gs = G * M / Rb ** 2
    return mframe(rng, [
        (f'The surface field strength of {b} is {sf(gs)} N kg⁻¹. What is the field strength at a height of {h} planetary radii above its surface?', gs / (1 + h) ** 2, [gs / h ** 2 if h != 1 else gs / 2, gs / (1 + h), gs * (1 + h) ** 2 / 10], 'N kg⁻¹', f'r = {1 + h}R, so g = {sf(gs)}/{1 + h}² = {q(gs / (1 + h) ** 2, "N kg⁻¹")}.'),
        (f'Using M = {q(M, "kg")} and R = {q(Rb, "m")}, what is the gravitational field strength at the surface of {b}?', gs, [G * M / Rb, G * M / Rb ** 3 * 1e6, gs * 2], 'N kg⁻¹', f'g = GM/R² = {q(gs, "N kg⁻¹")}.'),
        (f'A {rng.choice([2, 5, 10])} kg probe rests on {b} (M = {q(M, "kg")}, R = {q(Rb, "m")}). What is the gravitational field strength there?', gs, [gs * 5, G * M / Rb, gs / 2], 'N kg⁻¹', f'g = GM/R² = {q(gs, "N kg⁻¹")}; it does not depend on the probe mass.'),
    ])


@R.add('ch04-st4', 'C3', (1, 4), 'mcq')
def m_pot(rng, slot):
    b, M, Rb = pick(rng, BODIES)
    V = -G * M / Rb
    ve = math.sqrt(2 * G * M / Rb)
    k = rng.choice([2, 3, 4])
    return mframe(rng, [
        (f'For {b} (mass {q(M, "kg")}, radius {q(Rb, "m")}), what is the gravitational potential at the surface?', V, [-G * M / Rb ** 2, G * M / Rb, V / 2], 'J kg⁻¹', f'V = −GM/R = {q(V, "J kg⁻¹")}.'),
        (f'What is the escape speed from {b}, whose mass is {q(M, "kg")} and radius {q(Rb, "m")}?', ve, [math.sqrt(G * M / Rb), 2 * G * M / Rb / 1e4, ve * 2], 'm s⁻¹', f'v = √(2GM/R) = {q(ve, "m s⁻¹")}; √(GM/R) is the orbital speed at the surface.'),
        (f'The gravitational potential at the surface of {b} is {q(V, "J kg⁻¹")}. What is the potential at a distance of {k} radii from its centre?', V / k, [V / k ** 2, V * k, -V / k], 'J kg⁻¹', f'V ∝ −1/r: {q(V / k, "J kg⁻¹")}.'),
    ])


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def m_coul(rng, slot):
    q1, q2 = rng.choice([1, 2, 3, 5]) * 1e-6, rng.choice([2, 4, 6]) * 1e-6
    r = rng.choice([0.05, 0.10, 0.20, 0.30])
    F_ = K * q1 * q2 / r ** 2
    Q = rng.choice([3.2, 4.8, 8.0, 16.0]) * 1e-18
    return mframe(rng, [
        (f'Charges of {sf(q1 * 1e6, 2)} μC and {sf(q2 * 1e6, 2)} μC are placed {sf(r * 100, 2)} cm apart in a vacuum. What is the magnitude of the force between them?', F_, [K * q1 * q2 / r, F_ / 100, F_ * 1e4], 'N', f'F = kq₁q₂/r² = {q(F_, "N")}.'),
        (f'A small sphere carries a charge of −{q(Q, "C")}. How many excess electrons are on it?', Q / E, [Q * E * 1e37, Q / E / 2, Q / E * 10], '', f'N = Q/e = {sf(Q / E)}.'),
        (f'Two equal charges {sf(r * 100, 2)} cm apart repel with a force of {q(F_, "N")}. If the separation is doubled, what is the force?', F_ / 4, [F_ / 2, F_ * 2, F_ * 4], 'N', 'F ∝ 1/r².'),
    ])


@R.add('ch05-st3', 'C3', (1, 4), 'mcq')
def m_bwire(rng, slot):
    I = rng.choice([2, 5, 10, 15, 20])
    r = rng.choice([1, 2, 4, 5]) * 1e-2
    N, L, Is = rng.choice([200, 500, 1000]), rng.choice([0.2, 0.25, 0.5]), rng.choice([0.5, 1, 2])
    Bw = MU0 * I / (2 * math.pi * r)
    Bs = MU0 * N / L * Is
    return mframe(rng, [
        (f'A long straight wire carries {I} A. What is the magnetic flux density at {sf(r * 100, 2)} cm from it?', Bw, [MU0 * I / (2 * math.pi * r * r), MU0 * I / r, Bw * 2 * math.pi], 'T', f'B = μ₀I/(2πr) = {q(Bw, "T")}.'),
        (f'A solenoid {sf(L * 100, 2)} cm long has {N} turns and carries {Is} A. What is the field inside?', Bs, [MU0 * N * Is, MU0 * Is / L, Bs / (2 * math.pi)], 'T', f'B = μ₀(N/L)I = {q(Bs, "T")}.'),
        (f'The field {sf(r * 100, 2)} cm from a long wire is {q(Bw, "T")}. What current flows in the wire?', I, [I * 2 * math.pi, I / 2, I * r * 100], 'A', f'I = 2πrB/μ₀ = {q(I, "A")}.'),
    ])


@R.add('ch06-st1', 'C3', (1, 4), 'mcq')
def m_emotion(rng, slot):
    V = rng.choice([100, 200, 400, 600])
    d = rng.choice([1, 2, 5]) * 1e-2
    Ef = V / d
    a = E * Ef / ME
    ap = E * Ef / MP
    return mframe(rng, [
        (f'Plates {sf(d * 100, 2)} cm apart have {V} V across them. What is the acceleration of an electron between the plates?', a, [E * V / ME, ap, a / 100], 'm s⁻²', f'a = eV/(mₑd) = {q(a, "m s⁻²")}.'),
        (f'A proton is between parallel plates {sf(d * 100, 2)} cm apart with a p.d. of {V} V. What force acts on it?', E * Ef, [E * V, E * Ef * 100, E * V * d], 'N', f'F = eV/d = {q(E * Ef, "N")}.'),
        (f'An α particle (charge +2e) is accelerated from rest through {V} V. What kinetic energy does it gain?', 2 * E * V, [E * V, 4 * E * V, E * V / 2], 'J', f'Eₖ = qV = 2eV = {q(2 * E * V, "J")}.'),
    ])


@R.add('ch06-st2', 'C3', (1, 4), 'mcq')
def m_bmotion(rng, slot):
    B = rng.choice([0.05, 0.1, 0.2, 0.5])
    v = rng.choice([1, 2, 5]) * 1e6
    Ef = rng.choice([1, 2, 5]) * 1e4
    T_ = 2 * math.pi * MP / (E * B)
    return mframe(rng, [
        (f'Protons circle in a uniform {B} T magnetic field. What is their period of revolution?', T_, [MP / (E * B), 2 * math.pi * ME / (E * B), T_ * 2], 's', f'T = 2πm/(qB) = {q(T_, "s")}.'),
        (f'Crossed fields of E = {q(Ef, "V m⁻¹")} and B = {B} T form a velocity selector. Which speed passes undeflected?', Ef / B, [Ef * B, B / Ef * 1e8, Ef / B ** 2], 'm s⁻¹', f'v = E/B = {q(Ef / B, "m s⁻¹")}.'),
        (f'An electron moves at {q(v, "m s⁻¹")} at right angles to a {B} T field. What force acts on it?', E * v * B, [E * v / B, E * B, ME * v * B], 'N', f'F = evB = {q(E * v * B, "N")}.'),
    ])


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def m_flux(rng, slot):
    N = rng.choice([50, 100, 200, 500])
    B = rng.choice([0.05, 0.1, 0.2, 0.4])
    A = rng.choice([2, 4, 5, 10]) * 1e-4
    return mframe(rng, [
        (f'A coil of {N} turns, each of area {sf(A * 1e4, 2)} cm², lies perpendicular to a {B} T field. What is its flux linkage?', N * B * A, [B * A, N * B * A * 1e4, N * B / A * 1e-8], 'Wb', f'NΦ = NBA = {q(N * B * A, "Wb")}.'),
        (f'A {N}-turn coil of area {sf(A * 1e4, 2)} cm² perpendicular to a {B} T field is turned so that its plane is parallel to the field. What is the change in flux linkage?', N * B * A, [2 * N * B * A, B * A, N * B * A / 2], 'Wb', f'NBA → 0: change = {q(N * B * A, "Wb")}.'),
        (f'A {N}-turn coil perpendicular to a {B} T field is flipped through 180°. Each turn has area {sf(A * 1e4, 2)} cm². What is the change in flux linkage?', 2 * N * B * A, [N * B * A, 0.5 * N * B * A, 4 * N * B * A], 'Wb', f'+NBA → −NBA: Δ = 2NBA = {q(2 * N * B * A, "Wb")}.'),
    ])


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def m_closest(rng, slot):
    tgt = pick(rng, [('gold', 79), ('silver', 47), ('aluminium', 13), ('lead', 82), ('copper', 29)])
    Ek = rng.choice([3.0, 4.0, 5.0, 6.0, 8.0])
    d = K * 2 * tgt[1] * E * E / (Ek * 1e6 * EV)
    return mframe(rng, [
        (f'Alpha particles of {Ek} MeV are fired head-on at {tgt[0]} nuclei (Z = {tgt[1]}). What is the distance of closest approach?', d, [d / 2, d * 2, d * 4], 'm', f'd = k(2e)(Ze)/Eₖ = {q(d, "m")}.'),
        (f'An α particle approaches a {tgt[0]} nucleus (Z = {tgt[1]}) and stops momentarily {q(d, "m")} from it. What was its initial kinetic energy?', Ek, [Ek / 2, Ek * 2, Ek * 4], 'MeV', f'Eₖ = k(2e)(Ze)/d = {q(Ek, "MeV")}.'),
    ])


@R.add('ch08-st2', 'C3', (1, 4), 'mcq')
def m_nuc(rng, slot):
    sym, Z, A = pick(rng, NUCLIDES[3:])
    Rn = R0 * A ** (1 / 3)
    return mframe(rng, [
        (f'Using R = R₀A^(1/3) with R₀ = 1.20 fm, what is the radius of the {sym}-{A} nucleus?', Rn, [R0 * A, R0 * A ** 0.5, R0 * A ** (1 / 3) / 2], 'm', f'R = 1.20 × 10⁻¹⁵ × {A}^(1/3) = {q(Rn, "m")}.'),
        (f'A neutral atom of {sym}-{A} has proton number {Z}. How many neutrons does its nucleus contain?', A - Z, [A, Z, A + Z], '', f'N = A − Z = {A - Z}.'),
    ])


@R.add('ch08-st3', 'C3', (1, 4), 'mcq')
def m_spec(rng, slot):
    lam = rng.choice([410, 434, 486, 589, 656, 254, 122])
    Eph = H * C / (lam * 1e-9) / EV
    n = rng.choice([3, 4, 5, 6])
    return mframe(rng, [
        (f'A spectral line has wavelength {lam} nm. What is the energy of each photon in eV?', Eph, [Eph * 2, H * C / (lam * 1e-9) * 1e18, 1240 / lam * 10], 'eV', f'E = hc/λ = {q(Eph, "eV")}.'),
        (f'Hydrogen atoms are excited to level n = {n}. How many different wavelengths can they emit as they return to the ground state?', n * (n - 1) / 2, [n - 1, n, n * (n - 1)], '', f'n(n − 1)/2 = {n * (n - 1) // 2}.'),
    ])


@R.add('ch08-st4', 'C3', (1, 4), 'mcq')
def m_bohr(rng, slot):
    ni, nf = rng.choice([(2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 2)])
    dE = 13.6 * (1 / nf ** 2 - 1 / ni ** 2)
    lam = H * C / (dE * EV) * 1e9
    n = rng.choice([2, 3, 4])
    return mframe(rng, [
        (f'In the Bohr model, what photon energy is emitted when a hydrogen electron falls from n = {ni} to n = {nf}?', dE, [13.6 * (1 / nf - 1 / ni), 13.6 / ni ** 2, 13.6 / nf ** 2], 'eV', f'ΔE = 13.6(1/{nf}² − 1/{ni}²) = {q(dE, "eV")}.'),
        (f'What is the wavelength of the photon emitted in the hydrogen transition n = {ni} → n = {nf}?', lam, [lam * 2, lam / 2, 1240 / (13.6 / ni ** 2)], 'nm', f'ΔE = {sf(dE)} eV, λ = hc/ΔE = {q(lam, "nm")}.'),
        (f'How much energy is needed to ionise a hydrogen atom from the n = {n} level?', 13.6 / n ** 2, [13.6 / n, 13.6, 13.6 * (1 - 1 / n ** 2)], 'eV', f'|Eₙ| = 13.6/{n}² = {q(13.6 / n ** 2, "eV")}.'),
    ])


@R.add('ch09-st2', 'C3', (1, 4), 'mcq')
def m_db(rng, slot):
    V = rng.choice([50, 100, 250, 500, 1000, 2500])
    lam = H / math.sqrt(2 * ME * E * V)
    part = pick(rng, [('neutron', MN), ('proton', MP)])
    v = rng.choice([1, 2, 4]) * 1e3
    return mframe(rng, [
        (f'An electron is accelerated from rest through {V} V. What is its de Broglie wavelength?', lam, [H / (2 * ME * E * V), lam * 2, H / math.sqrt(2 * MP * E * V)], 'm', f'λ = h/√(2meV) = {q(lam, "m")}.'),
        (f'A {part[0]} moves at {q(v, "m s⁻¹")}. What is its de Broglie wavelength?', H / (part[1] * v), [H * part[1] * v * 1e60, H / (ME * v), H / (part[1] * v) * 2], 'm', f'λ = h/(mv) = {q(H / (part[1] * v), "m")}.'),
        (f'What momentum must a particle have for its de Broglie wavelength to be {q(lam, "m")}?', H / lam, [lam / H * 1e-45, H / lam * 2, H * lam * 1e45], 'kg m s⁻¹', f'p = h/λ = {q(H / lam, "kg m s⁻¹")}.'),
    ])


@R.add('ch09-st3', 'C3', (1, 4), 'mcq')
def m_compton(rng, slot):
    lam = rng.choice([5, 10, 20, 50, 71]) * 1e-12
    th = rng.choice([60, 90, 120, 180])
    lc = H / (ME * C)
    lam2 = lam + lc * (1 - cosd(th))
    return mframe(rng, [
        (f'X-rays of wavelength {q(lam, "m")} are scattered through {th}° by free electrons. What is the scattered wavelength?', lam2, [lam + lc, lam - lc * (1 - cosd(th)), lam * 2], 'm', f'λ′ = λ + (h/mₑc)(1 − cos θ) = {q(lam2, "m")}.'),
        (f'What is the momentum of an X-ray photon of wavelength {q(lam, "m")}?', H / lam, [H * C / lam, H / lam / C, lam / H * 1e-45], 'kg m s⁻¹', f'p = h/λ = {q(H / lam, "kg m s⁻¹")}.'),
        (f'A photon of wavelength {q(lam, "m")} is Compton-scattered by a free electron through {th}°. By how much does its wavelength increase?', lc * (1 - cosd(th)), [lc, lc * cosd(th) if th != 90 else lc / 2, H / (MP * C) * (1 - cosd(th))], 'm', f'Δλ = (h/mₑc)(1 − cos {th}°) = {q(lc * (1 - cosd(th)), "m")}, independent of λ.'),
    ])


@R.add('ch10-st5', 'C3', (1, 4), 'mcq')
def m_stab(rng, slot):
    r = rng.choice([1.0, 1.5, 2.0, 3.0]) * 1e-15
    sym, Z, A = pick(rng, [('C', 6, 14), ('Sr', 38, 90), ('Pb', 82, 208), ('U', 92, 238), ('Fe', 26, 56), ('Cs', 55, 137)])
    return mframe(rng, [
        (f'Two protons in a nucleus are {sf(r * 1e15, 2)} fm apart. What is the electric force between them?', K * E * E / r ** 2, [K * E / r ** 2 * 1e-19 * 10, K * E * E / r, G * MP * MP / r ** 2 * 1e36], 'N', f'F = ke²/r² = {q(K * E * E / r ** 2, "N")} (repulsive).'),
        (f'The nuclide {sym}-{A} has proton number {Z}. What is its neutron-to-proton ratio?', (A - Z) / Z, [A / Z, Z / (A - Z), (A - Z) / A], '', f'N/Z = {A - Z}/{Z} = {sf((A - Z) / Z)}.'),
    ])


@R.add('ch11-st1', 'C3', (1, 4), 'mcq')
def m_fiss(rng, slot):
    P = rng.choice([100, 500, 1000, 3000]) * 1e6
    Ef = rng.choice([180, 200, 210])
    rate = P / (Ef * 1e6 * EV)
    n = rng.choice([1, 2, 5]) * 1e20
    return mframe(rng, [
        (f'A reactor core produces {sf(P / 1e6, 3)} MW, with {Ef} MeV released per fission. How many fissions occur each second?', rate, [P / (Ef * EV), rate * 1e3, rate / 2], 's⁻¹', f'N = P/E = {q(rate, "s⁻¹")}.'),
        (f'If {q(n, "")} uranium-235 nuclei undergo fission, each releasing {Ef} MeV, how much energy is released?', n * Ef * 1e6 * EV, [n * Ef * EV, n * Ef * 1e6, n * Ef * 1e6 * EV * 235], 'J', f'E = N × {Ef} × 10⁶ × 1.60 × 10⁻¹⁹ = {q(n * Ef * 1e6 * EV, "J")}.'),
    ])


@R.add('ch11-st2', 'C3', (1, 4), 'mcq')
def m_reactor(rng, slot):
    Pt = rng.choice([2000, 2500, 3000, 3600]) * 1e6
    eta = rng.choice([0.30, 0.33, 0.35, 0.38])
    dT = rng.choice([20, 30, 40])
    mdot = Pt / (5500 * dT)
    return mframe(rng, [
        (f'A reactor of thermal power {sf(Pt / 1e6, 3)} MW runs at an overall efficiency of {int(eta * 100)} %. What is its electrical power output?', Pt * eta, [Pt * (1 - eta), Pt / eta, Pt * eta / 10], 'W', f'P_e = ηP_th = {q(Pt * eta, "W")}.'),
        (f'Coolant (c = 5500 J kg⁻¹ K⁻¹) removes {sf(Pt / 1e6, 3)} MW from a core while warming by {dT} K. What is its mass flow rate?', mdot, [Pt / 5500, mdot * dT, Pt / (4200 * dT)], 'kg s⁻¹', f'ṁ = P/(cΔT) = {q(mdot, "kg s⁻¹")}.'),
    ])


@R.add('ch12-st1', 'C3', (1, 4), 'mcq')
def m_fus(rng, slot):
    dm = rng.choice([0.0188, 0.0247, 0.0035, 0.0266])
    n = rng.choice([1, 2, 5]) * 1e38
    return mframe(rng, [
        (f'A fusion reaction has a mass defect of {dm} u. How much energy is released per reaction?', dm * UMEV, [dm * 931.5 * 1e-3, dm * 1.661, dm * UMEV * 2], 'MeV', f'E = {dm} × 931.5 = {q(dm * UMEV, "MeV")}.'),
        (f'A star completes {q(n, "")} proton–proton chains per second, each releasing 26.7 MeV. What is its luminosity?', n * 26.7e6 * EV, [n * 26.7 * EV, n * 26.7e6, n * 26.7e6 * EV / 4], 'W', f'L = N × 26.7 MeV = {q(n * 26.7e6 * EV, "W")}.'),
    ])


@R.add('ch12-st2', 'C3', (1, 4), 'mcq')
def m_hr(rng, slot):
    a, b_ = rng.sample(STARS, 2)
    k = rng.choice([2, 3, 4, 10])
    return mframe(rng, [
        (f'Two stars have equal luminosity, but star X has {k} times the surface temperature of star Y. What is the ratio of radii R_Y/R_X?', k ** 2, [k, k ** 4, math.sqrt(k)], '', f'L ∝ R²T⁴ with L equal → R ∝ 1/T² → R_Y/R_X = {k}² = {k * k}.'),
        (f'{a[0]} has a surface temperature of {a[1]} K. At what wavelength does its emission peak?', WIEN / a[1] * 1e9, [WIEN * a[1], WIEN / a[1] * 1e6, a[1] / WIEN * 1e-3], 'nm', f'λ = b/T = {q(WIEN / a[1] * 1e9, "nm")}.'),
    ])


@R.add('ch12-st3', 'C3', (1, 4), 'mcq')
def m_lum(rng, slot):
    Lr = rng.choice([0.5, 1, 2, 10, 25])
    d = rng.choice([2, 5, 10, 20])
    L = Lr * L_SUN
    b = L / (4 * math.pi * (d * PC) ** 2)
    k = rng.choice([2, 3])
    return mframe(rng, [
        (f'A star of luminosity {q(L, "W")} is {d} pc from Earth. What is its apparent brightness?', b, [L / (4 * math.pi * d * PC), b * 4, L / (d * PC) ** 2], 'W m⁻²', f'b = L/(4πd²) with d = {q(d * PC, "m")}: {q(b, "W m⁻²")}.'),
        (f'Star P has {k} times the radius and {k} times the surface temperature of star Q. What is L_P/L_Q?', k ** 6, [k ** 2, k ** 4, k ** 3], '', f'L ∝ R²T⁴ = {k}² × {k}⁴ = {k ** 6}.'),
    ])


@R.add('ch12-st4', 'C3', (1, 4), 'mcq')
def m_life(rng, slot):
    M = rng.choice([0.5, 2, 3, 5, 10, 15])
    return mframe(rng, [
        (f'Using L ∝ M^3.5, what is the luminosity of a {M} M☉ main-sequence star in solar units?', M ** 3.5, [M ** 2.5, M ** 3, M ** 4], 'L☉', f'{M}^3.5 = {sf(M ** 3.5)}.'),
        (f'Given L ∝ M^3.5 and a solar lifetime of 1.0 × 10¹⁰ y, what is the main-sequence lifetime of a {M} M☉ star?', 1e10 * M ** -2.5, [1e10 * M ** -3.5, 1e10 / M, 1e10 * M ** 2.5], 'y', f'τ ∝ M^−2.5: {q(1e10 * M ** -2.5, "y")}.'),
    ])


@R.add('ch05-st4', 'C3', (1, 4), 'mcq')
def m_epot(rng, slot):
    Q = rng.choice([1, 2, 5, 8]) * 1e-9
    r = rng.choice([0.02, 0.05, 0.1, 0.2])
    V = K * Q / r
    q2 = rng.choice([1, 2, 3]) * 1e-6
    return mframe(rng, [
        (f'What is the electric potential at {sf(r * 100, 2)} cm from a +{sf(Q * 1e9, 2)} nC point charge?', V, [K * Q / r ** 2, V / 2, V * 100], 'V', f'V = kQ/r = {q(V, "V")}.'),
        (f'A +{sf(q2 * 1e6, 2)} μC charge is placed {sf(r * 100, 2)} cm from a fixed +{sf(Q * 1e9, 2)} nC charge. What is the electric potential energy of the pair?', K * Q * q2 / r, [K * Q * q2 / r ** 2, K * Q / r, K * Q * q2 / r * 2], 'J', f'Eₚ = kQq/r = {q(K * Q * q2 / r, "J")}.'),
    ])


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step')
def c4_compton_full(rng, slot):
    E_kev = rng.choice([20, 50, 100, 200, 500])
    th = rng.choice([45, 60, 90, 120, 180])
    lam = H * C / (E_kev * 1e3 * EV)
    lc = H / (ME * C)
    lam2 = lam + lc * (1 - cosd(th))
    E2 = H * C / lam2 / EV / 1e3
    Ke = E_kev - E2
    frame = rng.randrange(2)
    if frame == 0:
        return num(f'A {E_kev} keV X-ray photon is Compton-scattered through {th}° by a free electron. (a) Calculate the wavelength of the incident photon. (b) Calculate the wavelength and energy of the scattered photon. (c) Determine the kinetic energy of the recoiling electron. (d) Explain why the fractional energy loss is greater for higher-energy photons.',
                   f'(a) {q(lam, "m")}; (b) {q(lam2, "m")}, {q(E2, "keV")}; (c) {q(Ke, "keV")}; (d) Δλ is fixed by θ, so Δλ/λ is larger when λ is small',
                   f'(a) λ = hc/E (M1) = {q(lam, "m")} (A1). (b) λ′ = λ + (h/mₑc)(1 − cos {th}°) = {q(lam2, "m")} (A1); E′ = hc/λ′ = {q(E2, "keV")} (A1). (c) energy conservation: Eₖ = E − E′ = {q(Ke, "keV")} (A1). (d) argument (R1).', 6, 'multi_step', 'G5')
    pin = H / lam
    pout = H / lam2
    return num(f'In a Compton experiment, {E_kev} keV photons scattered at {th}° are detected. (a) Determine the energy of the scattered photons. (b) Calculate the momenta of the incident and scattered photons. (c) Explain how conservation of momentum determines the direction of the recoiling electron. (d) Suggest why the effect was first observed with X-rays rather than visible light.',
               f'(a) {q(E2, "keV")}; (b) {q(pin, "kg m s⁻¹")} and {q(pout, "kg m s⁻¹")}; (c) electron momentum = vector difference of photon momenta; (d) Δλ ≈ pm, negligible compared with visible wavelengths',
               f'(a) λ = {q(lam, "m")}, λ′ = {q(lam2, "m")} (M1), E′ = {q(E2, "keV")} (A1). (b) p = h/λ (M1) values (A1). (c) vector diagram: p_e = p − p′ (R1). (d) fractional shift argument (R1).', 6, 'multi_step', 'G5')


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step')
def c4_matter_wave(rng, slot):
    V = rng.choice([54, 100, 150])
    lam = H / math.sqrt(2 * ME * E * V)
    d = 2.15e-10
    th = asind(lam / d) if lam / d < 1 else None
    if th is None:
        return None
    Vm = rng.choice([10e3, 50e3, 100e3])
    lm = H / math.sqrt(2 * ME * E * Vm)
    return num(f'(a) Davisson and Germer directed {V} eV electrons at a nickel crystal whose surface atoms are 2.15 × 10⁻¹⁰ m apart. Calculate the de Broglie wavelength of the electrons and the angle of the first-order maximum given by d sin θ = λ. (b) An electron microscope uses electrons accelerated through {sf(Vm / 1e3, 3)} kV. Calculate their (non-relativistic) wavelength and compare it with visible light. (c) Explain why the non-relativistic formula becomes inaccurate at the highest voltages.',
               f'(a) {q(lam, "m")}, {deg(th)}; (b) {q(lm, "m")}, about {sf(5.0e-7 / lm, 2)} times shorter than 500 nm light; (c) electron speeds approach c, so p ≠ √(2meV)',
               f'(a) λ = h/√(2meV) (M1) = {q(lam, "m")} (A1); θ = sin⁻¹(λ/d) = {deg(th)} (A1). (b) λ = {q(lm, "m")} (A1); comparison (A1). (c) relativistic momentum needed as v → c (R1).', 6, 'multi_step', 'G5')


R.facts('ch09-st3', F(**{**R.f['ch09-st3'].__dict__, 'evaluate': R.f['ch09-st3'].evaluate + [
    ('Photons have momentum but no mass, so the idea of photon momentum is contradictory.', ['in Newtonian mechanics p = mv requires mass'], ['relativity gives E² = (pc)² + (mc²)², so massless particles have p = E/c', 'Compton scattering and radiation pressure (solar sails) confirm photon momentum'], 'Not contradictory: the Newtonian definition is a special case; relativity and experiment show light carries momentum p = h/λ.')]}))
R.facts('ch09-st2', F(**{**R.f['ch09-st2'].__dict__, 'evaluate': R.f['ch09-st2'].evaluate + [
    ('De Broglie’s hypothesis was accepted because it was mathematically elegant.', ['it linked Bohr’s quantisation to standing waves', 'symmetry between light and matter was appealing'], ['acceptance followed experimental confirmation by Davisson–Germer and G. P. Thomson (1927)', 'elegance alone is not sufficient evidence (NOS)'], 'Elegance made the idea attractive, but acceptance came from experimental confirmation of electron diffraction.')]}))


def add_f(key, **kw):
    f = R.f[key]
    for k, v in kw.items():
        getattr(f, k).extend(v)


add_f('ch01-st4',
      evaluate=[('Interference experiments with single photons show that light is fundamentally a wave.', ['the fringe pattern builds up even when photons pass one at a time', 'positions of bright fringes match wave predictions'], ['each photon is detected at a single point, as a particle', 'the pattern is a probability distribution (quantum mechanics)'], 'Neither model alone suffices: single-photon interference shows quantum behaviour, with wave-like probability and particle-like detection.'),
                ('Young’s double-slit experiment was immediately accepted as decisive evidence against Newton’s corpuscular theory.', ['it gave a clear wave explanation of fringes and measured wavelengths'], ['Newton’s authority meant many resisted Young’s ideas for years', 'acceptance grew only after Fresnel’s mathematical theory and Arago’s spot', 'social and authority factors influence acceptance (NOS)'], 'It became decisive only over time, after further theory and experiments; scientific acceptance is a community process.')],
      extended=[('A student shines a 650 nm laser through a double slit (d = 0.25 mm) onto a wall 3.20 m away and measures the distance across 10 fringe spacings as 8.3 cm. (a) Determine the wavelength from the data and compare it with 650 nm. (b) Identify two systematic errors that could explain the difference. (c) Explain why the outer fringes appear dimmer.', '(a) s = 8.3 mm, λ = sd/D = 648 nm, within 0.3 % of 650 nm; (b) slit separation not exactly as labelled, D measured to the wrong point, wall not perpendicular; (c) the pattern is modulated by the single-slit diffraction envelope, which falls off with angle.', 6, 'multi_step'),
                ('Two radio transmitters 300 m apart broadcast the same 1.0 MHz signal in phase. A car drives along a road parallel to the line joining them, 5.0 km away. (a) Calculate the wavelength. (b) Determine the distance between positions of minimum signal along the road. (c) Explain why the minima are not of zero signal.', '(a) λ = c/f = 300 m; (b) s = λD/d = 300 × 5000/300 = 5.0 km (small-angle approximation only roughly valid); (c) the two signals arrive with unequal amplitudes (different distances, ground reflections), so cancellation is incomplete.', 6, 'multi_step')])

add_f('ch03-st1',
      evaluate=[('The Doppler effect for sound is a useful everyday example for teaching relativity.', ['familiar frequency shifts motivate the idea of relative motion'], ['sound needs a medium so the formulae depend on who moves', 'light’s Doppler effect depends only on relative velocity; time dilation adds a transverse effect'], 'Useful as an analogy, but the differences must be emphasised to avoid misconceptions.'),
                ('A stationary observer can always tell whether a source or the observer is moving from the Doppler shift alone.', ['for sound the two cases give slightly different formulae'], ['at low speeds the difference is tiny and within measurement uncertainty', 'wind complicates the medium frame', 'for light there is no difference in principle'], 'Only for sound at appreciable speeds and with careful measurement; generally the shift alone is ambiguous.')],
      extended=[('A train sounding a 600 Hz horn travels at 30 m s⁻¹ along a straight track; a cyclist rides at 8.0 m s⁻¹ towards the approaching train (speed of sound 340 m s⁻¹). (a) Calculate the frequency the cyclist hears. (b) Calculate the frequency after the train has passed, both still moving at the same speeds. (c) Explain why the frequency drop is not instantaneous for a listener standing beside the track.', '(a) f′ = 600 × (340 + 8)/(340 − 30) = 674 Hz; (b) f′ = 600 × (340 − 8)/(340 + 30) = 538 Hz; (c) the source’s velocity component along the line of sight changes gradually as the train passes, so the frequency falls smoothly over a short time.', 6, 'multi_step'),
                ('Describe how you could use a smartphone recording of a passing car’s horn to estimate the car’s speed. Include the measurements, the equations and the main sources of uncertainty.', 'Record the horn as the car approaches and recedes; use a frequency-analysis app to find f₁ (approaching) and f₂ (receding); u = v(f₁ − f₂)/(f₁ + f₂) with v ≈ 340 m s⁻¹ (adjusted for temperature). Uncertainties: frequency resolution of the app, car not moving directly along the line of sight, speed changes, wind, temperature-dependent v.', 6, 'multi_step')])

add_f('ch03-st2',
      evaluate=[('Redshift measurements alone are enough to determine the distances of galaxies.', ['Hubble’s law d = v/H₀ converts redshift to distance'], ['H₀ must be calibrated with independent distances (Cepheids, supernovae)', 'peculiar velocities distort nearby galaxy redshifts', 'at high z relativistic and cosmological models are needed'], 'Redshift gives distance only through a calibrated Hubble constant and a cosmological model.')],
      extended=[('Light from a distant galaxy shows the hydrogen-alpha line at 669.4 nm (laboratory 656.3 nm). (a) Calculate the galaxy’s recession speed. (b) Taking H₀ = 70 km s⁻¹ Mpc⁻¹, estimate its distance. (c) Explain one reason why this distance estimate may be inaccurate.', '(a) z = 13.1/656.3 = 0.0200, v = zc = 5.99 × 10⁶ m s⁻¹; (b) d = v/H₀ = 5990/70 = 86 Mpc; (c) peculiar motion within its cluster, uncertainty in H₀, or measurement of the line centre.', 5, 'multi_step')])

add_f('ch03-st3',
      evaluate=[('Doppler ultrasound is safer than X-ray imaging for monitoring blood flow in pregnancy.', ['ultrasound is non-ionising', 'gives real-time velocity information'], ['heating at high intensity must be limited', 'image quality depends on operator and angle of insonation', 'cannot image through bone or gas'], 'Yes for this purpose, because it avoids ionising radiation, provided intensity guidelines are followed.'),
                ('Radar speed guns are completely reliable evidence of speeding.', ['precise frequency measurements give accurate speeds'], ['cosine error from aiming angle (reads low)', 'reflections from other vehicles or moving fans', 'calibration must be checked regularly'], 'Reliable when correctly calibrated and used, but procedural safeguards are needed.')],
      extended=[('A Doppler weather radar emits 2.8 GHz microwaves. Echoes from raindrops in a storm show a frequency shift of +560 Hz. (a) Calculate the radial speed of the raindrops and state whether they approach or recede. (b) Explain why the radar can only measure one component of the wind velocity. (c) Suggest how meteorologists obtain the full wind field.', '(a) v = cΔf/(2f) = 3.00 × 10⁸ × 560/(2 × 2.8 × 10⁹) = 30 m s⁻¹, approaching; (b) only motion along the beam changes the path length; (c) combine data from two or more radars viewing from different directions.', 5, 'multi_step'),
                ('An exoplanet survey detects a Sun-like star whose spectral lines shift by ±1.2 × 10⁻⁴ nm at 656 nm with a period of 4.2 days. (a) Determine the star’s radial-velocity amplitude. (b) Explain what the period tells us. (c) Discuss why this method favours finding massive planets close to their stars.', '(a) v = cΔλ/λ = 3.00 × 10⁸ × 1.2 × 10⁻⁴/656 = 55 m s⁻¹; (b) the orbital period of the planet; (c) heavier, closer planets pull the star more strongly, giving larger, faster wobbles that are easier to detect within a short survey.', 5, 'multi_step')])

for _k in ('ch09-st1', 'ch09-st2', 'ch09-st3'):
    add_f(_k, extended=[])
add_f('ch09-st1',
      evaluate=[('Einstein’s explanation of the photoelectric effect was accepted immediately.', ['it explained threshold frequency and Eₖ independent of intensity'], ['many physicists, including Planck, resisted light quanta for years', 'Millikan set out to disprove it and confirmed it in 1916', 'acceptance required experimental tests (NOS)'], 'It was accepted only after precise experiments confirmed its predictions.')],
      extended=[('Solar panels work by absorbing photons, not by the photoelectric effect itself. Compare the two processes, explaining why both show a threshold photon energy and why sunlight of longer wavelength cannot be used by either.', 'In the photoelectric effect photons eject electrons from the metal surface (needs hf ≥ Φ, a few eV); in a solar cell photons raise electrons across the band gap (≈ 1.1 eV for silicon) to create current. Both need a minimum photon energy, set by Φ or the band gap; longer-wavelength photons have hf below this threshold.', 5, 'multi_step')])
add_f('ch09-st2',
      extended=[('Neutrons from a reactor are slowed to 2.2 km s⁻¹ and diffracted by a crystal. (a) Calculate their de Broglie wavelength. (b) Explain why neutrons, rather than X-rays, are used to locate hydrogen atoms in crystals. (c) Explain why electrons of the same wavelength would not penetrate the crystal as far.', '(a) λ = h/(mv) = 6.63 × 10⁻³⁴/(1.675 × 10⁻²⁷ × 2200) = 1.8 × 10⁻¹⁰ m; (b) X-rays scatter from electrons, and hydrogen has only one; neutrons scatter from nuclei; (c) electrons are charged and interact strongly with atoms via electric forces, so they are absorbed near the surface.', 5, 'multi_step')])
add_f('ch09-st3',
      extended=[('Gamma photons of 662 keV from caesium-137 are detected after Compton scattering in a detector. (a) Show that the maximum energy that can be transferred to an electron (the "Compton edge") is about 478 keV. (b) Explain why the detector records a continuous range of electron energies below this. (c) Explain why the photopeak at 662 keV also appears.', '(a) back-scatter: λ′ = λ + 2h/mₑc; E′ = 184 keV, so Eₖ,max = 662 − 184 = 478 keV; (b) scattering angles from 0° to 180° give all energies from 0 to 478 keV; (c) some photons are fully absorbed (photoelectric absorption or multiple scatters), depositing all 662 keV.', 6, 'multi_step')])


# --- extra C4 depth: evaluation claims and extended problems ------------------------------------
add_f('ch01-st3',
      evaluate=[('Diffraction is a nuisance that limits the performance of optical instruments.', ['it limits the resolution of telescopes and microscopes', 'it spreads laser beams over long distances'], ['diffraction gratings and X-ray crystallography rely on it', 'radio reception behind hills depends on it'], 'Diffraction limits resolution but is also exploited in spectroscopy and structure determination, so it is not merely a nuisance.')],
      extended=[('Two coherent sources S₁ and S₂ in a ripple tank are 6.0 cm apart and vibrate in phase at 12 Hz; the wave speed is 0.18 m s⁻¹. (a) Calculate the wavelength. (b) Point P is 10.5 cm from S₁ and 13.5 cm from S₂: determine the type of interference at P. (c) Describe how the pattern changes if the two dippers vibrate in antiphase.', '(a) λ = 0.18/12 = 1.5 cm; (b) path difference 3.0 cm = 2λ → constructive (antinodal line); (c) all maxima and minima swap: P becomes a point of destructive interference and the central line becomes a nodal line.', 5, 'multi_step')])

add_f('ch02-st3',
      evaluate=[('Resonance is always destructive and engineers should always avoid it.', ['bridges, buildings and machines can be damaged by resonant vibrations'], ['musical instruments, radio tuning, MRI and quartz clocks depend on resonance', 'microwave ovens and ultrasonic cleaners exploit forced oscillation'], 'Resonance can be harmful but is also essential in many technologies; engineers avoid it in structures and exploit it in devices.')],
      extended=[('An aircraft wing has a natural frequency of 4.5 Hz. The engine propellers rotate at 2400 revolutions per minute with three blades. (a) Calculate the frequency at which blades pass the wing. (b) Explain whether resonance of the wing is likely at this rotation rate. (c) Explain what could happen during engine start-up as the propeller speed increases from zero.', '(a) 2400/60 × 3 = 120 Hz; (b) 120 Hz is far from 4.5 Hz, so the wing is not driven at resonance at cruise; (c) during start-up the blade-passing frequency passes through 4.5 Hz (at 90 rpm), so a brief large-amplitude vibration may occur; damping limits it.', 5, 'multi_step')])

add_f('ch02-st4',
      evaluate=[('A tuned mass damper is simply a form of critical damping.', ['both reduce the amplitude of unwanted oscillations'], ['a tuned mass damper is a second oscillator resonating in antiphase that transfers energy away', 'critical damping refers to the decay of free oscillations without overshoot', 'dampers are effective only near the tuned frequency'], 'No: a tuned mass damper uses resonance of a secondary system plus damping; it is not the same as critical damping.')],
      extended=[('A car of mass 1200 kg sits on four springs, each of stiffness 3.0 × 10⁴ N m⁻¹. (a) Calculate the natural frequency of vertical oscillation, f = (1/2π)√(k_total/m). (b) The car drives over a washboard road with ridges 0.80 m apart; find the speed at which resonance occurs. (c) Explain why the shock absorbers are designed for near-critical damping.', '(a) k_total = 1.2 × 10⁵ N m⁻¹, f = (1/2π)√(1.2 × 10⁵/1200) = 1.59 Hz; (b) v = fλ = 1.59 × 0.80 = 1.27 m s⁻¹; (c) the body returns to equilibrium quickly after each bump without bouncing, improving comfort and keeping tyres in contact with the road.', 5, 'multi_step')])

add_f('ch04-st1',
      evaluate=[('The discovery of Neptune is a triumph of Newton’s law of gravitation.', ['Le Verrier and Adams predicted Neptune’s position from anomalies in Uranus’s orbit', 'the planet was found within 1° of the prediction in 1846'], ['the same reasoning predicted "Vulcan" to explain Mercury’s orbit, which does not exist; general relativity was needed', 'predictions can succeed or fail; both test a theory (NOS)'], 'It is a striking successful prediction, but the Vulcan episode shows the limits of the theory, which general relativity later resolved.')],
      extended=[('A spacecraft travels from Earth to the Moon (separation 3.84 × 10⁸ m). (a) Calculate the gravitational force of Earth and of the Moon on a 2000 kg spacecraft halfway between them. (b) State the direction of the resultant force. (c) Explain why the spacecraft needs no engine thrust for most of the journey.', '(a) Earth: GMm/r² = 6.67 × 10⁻¹¹ × 5.97 × 10²⁴ × 2000/(1.92 × 10⁸)² = 21.6 N; Moon: 6.67 × 10⁻¹¹ × 7.35 × 10²² × 2000/(1.92 × 10⁸)² = 0.266 N; (b) towards Earth (resultant 21.3 N); (c) it coasts in free fall under gravity after the initial burn; no force is needed to maintain motion (Newton’s first law), only to change the trajectory.', 6, 'multi_step')])

add_f('ch04-st4',
      evaluate=[('Black holes are objects whose escape speed exceeds the speed of light, so Newtonian gravitation fully explains them.', ['setting √(2GM/R) = c gives the Schwarzschild radius R = 2GM/c², the correct result'], ['the agreement is a coincidence: Newtonian theory allows light to rise and fall back, unlike an event horizon', 'general relativity predicts time dilation, horizons and singularities', 'models outside their domain can give right numbers for wrong reasons (NOS)'], 'Newtonian reasoning gives the right radius but not the physics; general relativity is needed.')],
      extended=[('Show that the Schwarzschild radius R = 2GM/c² can be obtained by setting the escape speed equal to c, and calculate it for (a) the Sun and (b) Earth. Comment on what these values mean.', '√(2GM/R) = c → R = 2GM/c². (a) Sun: 2 × 6.67 × 10⁻¹¹ × 1.99 × 10³⁰/(3.00 × 10⁸)² = 2.95 km; (b) Earth: 8.85 mm. They are the sizes to which each mass would have to be compressed to become a black hole – far smaller than their actual radii.', 5, 'multi_step')])

add_f('ch05-st1',
      evaluate=[('Static electricity is only a curiosity with no practical importance.', ['everyday sparks and clinging clothes seem trivial'], ['electrostatic precipitators clean power-station emissions', 'photocopiers and laser printers use electrostatic charging', 'sparks can ignite fuel vapour, so earthing is vital'], 'Electrostatics has important industrial applications and safety implications, so it is far more than a curiosity.')],
      extended=[('Point charges +4.0 μC at A and −2.0 μC at B are 0.30 m apart. (a) Calculate the force between them. (b) Find the point on the line AB (outside the segment) where a third charge would feel no resultant force. (c) Explain why no such point exists between A and B.', '(a) F = 8.99 × 10⁹ × 4.0 × 10⁻⁶ × 2.0 × 10⁻⁶/0.09 = 0.80 N, attractive; (b) beyond B: 4/(0.30 + x)² = 2/x² → x = 0.72 m beyond B; (c) between the charges the forces from +4 μC and −2 μC on a test charge point in the same direction, so they cannot cancel.', 6, 'multi_step')])

add_f('ch05-st2',
      evaluate=[('A Faraday cage gives complete protection from all electric fields and radiation.', ['static fields inside a closed conductor are zero', 'cars protect occupants from lightning'], ['holes allow radiation of wavelength smaller than the mesh to enter', 'magnetic fields at low frequency are not blocked', 'contact with the cage can still be dangerous'], 'It shields static fields and long-wavelength radiation effectively, but not all fields, so "complete" is an overstatement.')],
      extended=[('In a Millikan-type experiment, plates are 6.0 mm apart. A drop of mass 2.9 × 10⁻¹⁵ kg is held stationary when the p.d. is 355 V. (a) Determine the charge on the drop. (b) How many electrons does it carry? (c) The p.d. is increased to 500 V; calculate the initial acceleration of the drop and its direction.', '(a) q = mgd/V = 2.9 × 10⁻¹⁵ × 9.81 × 0.006/355 = 4.8 × 10⁻¹⁹ C; (b) 3 electrons; (c) F = qV/d = 4.0 × 10⁻¹⁴ N up, weight 2.84 × 10⁻¹⁴ N down, a = (4.0 − 2.84) × 10⁻¹⁴/2.9 × 10⁻¹⁵ = 4.0 m s⁻² upwards.', 6, 'multi_step')])

add_f('ch05-st4',
      evaluate=[('Electric potential is a more useful concept than electric field.', ['potential is a scalar so contributions add simply', 'energy calculations use ΔV directly'], ['the field gives the force and direction of motion', 'the two are linked by E = −ΔV/Δr, so each is used where convenient'], 'Neither is more useful in general; potential simplifies energy problems while field describes forces.')],
      extended=[('Two point charges, +3.0 nC at x = 0 and −3.0 nC at x = 0.40 m, lie on the x-axis. (a) Calculate the electric potential at x = 0.10 m and at x = 0.20 m. (b) Calculate the work done by an external agent moving a +1.0 nC charge from x = 0.10 m to x = 0.20 m. (c) Explain why the field at x = 0.20 m is not zero although the potential is.', '(a) at 0.10 m: V = k(3.0 × 10⁻⁹/0.10 − 3.0 × 10⁻⁹/0.30) = 180 V; at 0.20 m: 0 V; (b) W = qΔV = 1.0 × 10⁻⁹ × (0 − 180) = −1.8 × 10⁻⁷ J (the field does positive work); (c) the field is the negative potential gradient; potentials cancel at the midpoint but the potential is still decreasing there, so E points from + to −.', 6, 'multi_step')])

add_f('ch07-st1',
      evaluate=[('Flux linkage is just a mathematical convenience with no physical meaning.', ['NΦ can be computed without picturing field lines'], ['it directly determines the induced emf through Faraday’s law', 'search coils measure changes in flux linkage', 'it links to measurable charge flow Q = Δ(NΦ)/R'], 'It is a physically meaningful quantity because its rate of change is what is measured as induced emf.')],
      extended=[('A search coil of 500 turns and area 1.2 cm² is connected to a charge-measuring meter; the total circuit resistance is 40 Ω. It is placed between the poles of a magnet with its plane perpendicular to the field and then pulled out quickly. A charge of 1.8 × 10⁻⁵ C flows. (a) Show that Q = Δ(NΦ)/R. (b) Determine the flux density between the poles. (c) Explain why the result does not depend on how quickly the coil is removed.', '(a) I = ε/R = Δ(NΦ)/(RΔt), Q = IΔt = Δ(NΦ)/R; (b) NBA = QR → B = 1.8 × 10⁻⁵ × 40/(500 × 1.2 × 10⁻⁴) = 0.012 T; (c) faster removal gives larger current for a shorter time; the product (charge) depends only on the change in flux linkage.', 5, 'multi_step')])

add_f('ch07-st3',
      evaluate=[('Alternating current is better than direct current for transmitting electrical energy over long distances.', ['transformers make it easy to step a.c. up to high voltage, reducing I²R losses'], ['HVDC links now carry power over very long distances and undersea with lower losses', 'a.c. has reactive losses and skin effect; d.c. avoids synchronisation problems'], 'A.c. dominates grids because of transformers, but HVDC is better for very long or undersea links; the choice depends on distance and cost.')],
      extended=[('A bicycle dynamo has a magnet rotating inside a 400-turn coil of area 4.0 cm²; the field at the coil is 0.15 T. (a) Calculate the peak emf when the magnet rotates at 30 revolutions per second. (b) Calculate the rms emf. (c) Explain why the lamp becomes brighter and flickers less as the cyclist speeds up.', '(a) ε₀ = BANω = 0.15 × 4.0 × 10⁻⁴ × 400 × 2π × 30 = 4.5 V; (b) ε_rms = 3.2 V; (c) ε₀ ∝ ω, so higher speed gives a larger emf and power (∝ ε²); the frequency also increases, so the brightness variations become too rapid to notice.', 5, 'multi_step')])

add_f('ch08-st1',
      evaluate=[('Rutherford’s nuclear model was the final correct model of the atom.', ['explained large-angle scattering and introduced the nucleus'], ['could not explain atomic stability or line spectra', 'Bohr and then quantum mechanics replaced electron orbits', 'the nucleus itself has structure (protons, neutrons, quarks)'], 'It was a major step but not final; models are refined as evidence accumulates (NOS).')],
      extended=[('In a modern version of the Geiger–Marsden experiment, 5.5 MeV alpha particles are scattered by thin gold foil. (a) Calculate the distance of closest approach for a head-on collision. (b) Compare this with the radius of a gold nucleus (A = 197) from R = R₀A^(1/3). (c) Predict and explain what would be observed if the alpha energy were raised to 30 MeV.', '(a) d = k(2e)(79e)/Eₖ = 4.1 × 10⁻¹⁴ m; (b) R = 1.20 × 10⁻¹⁵ × 197^(1/3) = 7.0 × 10⁻¹⁵ m – the alpha particle stays well outside the nucleus, so pure Coulomb (Rutherford) scattering is observed; (c) at 30 MeV d ≈ 7.6 fm, comparable to R, so the alpha reaches the strong-force range and deviations from Rutherford’s formula appear at large angles, revealing the nuclear size.', 6, 'multi_step')])

add_f('ch08-st2',
      evaluate=[('A neutron star can be thought of as a giant atomic nucleus.', ['density ~10¹⁷ kg m⁻³, similar to nuclear density', 'made mostly of neutrons held at nuclear separations'], ['it is bound by gravity, not the strong force', 'contains electrons, protons and possibly exotic matter', 'its radius (~10 km) does not follow R₀A^(1/3) scaling physics in the same way'], 'The density comparison is apt, but the binding mechanism differs, so the analogy is partial.')],
      extended=[('Show that the density of nuclear matter is independent of nucleon number using R = R₀A^(1/3), and calculate it (R₀ = 1.20 fm, nucleon mass ≈ 1.66 × 10⁻²⁷ kg). Then estimate the radius a sphere of nuclear density would have if it contained the mass of Earth (5.97 × 10²⁴ kg).', 'ρ = A m_u/((4/3)πR₀³A) = 3m_u/(4πR₀³) = 2.3 × 10¹⁷ kg m⁻³, independent of A. Radius: (3M/(4πρ))^(1/3) = (3 × 5.97 × 10²⁴/(4π × 2.3 × 10¹⁷))^(1/3) ≈ 180 m.', 5, 'multi_step')])

add_f('ch08-st4',
      evaluate=[('The success of the Bohr model for hydrogen proves that electrons orbit the nucleus in circles.', ['it reproduces the hydrogen energy levels exactly'], ['it fails for multi-electron atoms and fine structure', 'quantum mechanics gives the same energies without definite orbits', 'agreement of predictions does not prove the mechanism (NOS)'], 'No: correct predictions support but do not prove a model; the orbit picture was replaced by wavefunctions.')],
      extended=[('A hydrogen atom in its ground state absorbs a photon of wavelength 97.3 nm. (a) Determine the energy level reached. (b) List all possible photon energies emitted as the atom returns to the ground state. (c) Identify which of these lie in the visible region and to which series they belong.', '(a) E = 1240/97.3 = 12.75 eV, so −13.6 + 12.75 = −0.85 eV, n = 4; (b) transitions 4→3 (0.66 eV), 4→2 (2.55 eV), 4→1 (12.75 eV), 3→2 (1.89 eV), 3→1 (12.09 eV), 2→1 (10.2 eV); (c) 2.55 eV (486 nm) and 1.89 eV (656 nm) are visible – Balmer series.', 6, 'multi_step')])

add_f('ch10-st1',
      evaluate=[('Nuclear equations show that matter can be transformed from one element into another, as alchemists claimed.', ['α and β decay change Z, so one element becomes another'], ['transmutation is a nuclear process, not chemical, and alchemists’ methods could never achieve it', 'only tiny quantities are produced in decay chains'], 'Transmutation is real, but by nuclear processes far beyond alchemy; the claim conflates nuclear and chemical change.')],
      extended=[('Thorium-232 (Z = 90) decays through a chain to lead-208 (Z = 82). (a) Determine the numbers of α and β⁻ decays. (b) Explain why the chain contains both types of decay. (c) Explain why radon-220, an intermediate member, is a hazard in buildings on granite.', '(a) ΔA = 24 → 6 α; Z: 90 − 12 + n_β = 82 → 4 β⁻; (b) α decay lowers Z and A but raises N/Z relative to the stability band, so β⁻ decays convert neutrons to protons to return towards stability; (c) radon is a gas that seeps out of the rock and is inhaled; its alpha-emitting daughters lodge in the lungs.', 6, 'multi_step')])

add_f('ch10-st3',
      evaluate=[('Mass is not conserved in nuclear reactions.', ['products of fission and fusion have less rest mass than the reactants'], ['mass–energy is conserved: the "missing" mass appears as kinetic energy and radiation', 'in chemical reactions mass changes too, though unmeasurably small'], 'Rest mass alone is not conserved, but total mass–energy is, so the claim needs qualification.')],
      extended=[('Deuterium (²H, nuclear mass 2.013553 u) can be split into a proton and a neutron by a gamma photon (photodisintegration). (a) Calculate the binding energy of the deuteron. (b) Determine the minimum photon frequency needed. (c) Explain why in practice a slightly larger photon energy is needed (consider momentum).', '(a) Δm = 1.007276 + 1.008665 − 2.013553 = 0.002388 u; E_B = 2.22 MeV; (b) f = E/h = 2.22 × 10⁶ × 1.60 × 10⁻¹⁹/6.63 × 10⁻³⁴ = 5.4 × 10²⁰ Hz; (c) the photon carries momentum, so the products must move, requiring extra kinetic energy beyond E_B.', 5, 'multi_step')])

add_f('ch10-st4',
      evaluate=[('The risk from background radiation is so small that it can be ignored.', ['average dose ~2–3 mSv per year, with no clear detectable harm at this level'], ['radon is a leading cause of lung cancer among non-smokers', 'doses vary widely with location, altitude and occupation (aircrew)', 'linear no-threshold model assumes some risk at any dose'], 'For most people the risk is small, but radon in some homes is significant and worth reducing.')],
      extended=[('A Geiger–Müller tube records 54 counts per minute with no source present. A beta source is placed 4.0 cm away and the count rate rises to 1254 counts per minute. (a) Determine the corrected count rate. (b) An aluminium sheet of thickness 2.0 mm reduces the measured rate to 354 counts per minute; calculate the fraction of beta particles transmitted. (c) Explain why the uncertainty in the count rate is larger when the counts are low.', '(a) 1200 counts per minute; (b) (354 − 54)/1200 = 0.25; (c) radioactive counts fluctuate randomly with uncertainty ≈ √N, so the fractional uncertainty 1/√N is larger for small N.', 5, 'multi_step')])

add_f('ch10-st5',
      evaluate=[('The strong nuclear force is the most important of the fundamental forces.', ['it binds nuclei and makes atoms and chemistry possible', 'it is the strongest at nuclear distances'], ['gravity governs planets, stars and galaxies', 'electromagnetism governs chemistry and materials', 'the weak force drives stellar fusion (p → n)'], 'Each force dominates at its own scale; "most important" depends on the phenomenon considered.')],
      extended=[('Explain, using the forces between nucleons, why (a) the binding energy per nucleon is roughly constant for medium and heavy nuclei, (b) very light nuclei have low binding energy per nucleon, and (c) the curve falls slowly for the heaviest nuclei.', '(a) The strong force is short-range, so each nucleon interacts only with its nearest neighbours (saturation), giving a roughly constant BE per nucleon; (b) in light nuclei a large fraction of nucleons are at the surface with fewer neighbours; (c) electric repulsion acts between all pairs of protons and grows as Z², reducing BE per nucleon for large Z.', 5, 'multi_step')])

add_f('ch11-st3',
      evaluate=[('Small modular reactors will solve the safety concerns of nuclear power.', ['passive cooling designs remove decay heat without pumps or power', 'smaller cores have less decay heat and inventory'], ['waste is still produced', 'more sites could increase security and proliferation challenges', 'designs are not yet proven at commercial scale'], 'They may reduce some risks through passive safety, but waste, security and cost issues remain.')],
      extended=[('Spent fuel containing caesium-137 (half-life 30.2 y) has an activity of 4.0 × 10¹⁵ Bq when removed from a reactor. (a) Calculate the decay constant of Cs-137. (b) Determine the number of Cs-137 nuclei present. (c) Calculate the time for its activity to fall to 4.0 × 10¹² Bq. (d) Explain why cooling ponds are used for the first few years.', '(a) λ = ln 2/(30.2 × 3.156 × 10⁷) = 7.27 × 10⁻¹⁰ s⁻¹; (b) N = A/λ = 5.5 × 10²⁴; (c) factor 1000 ≈ 10 half-lives, t = 30.2 × log₂1000 = 301 years; (d) short-lived fission products produce intense decay heat and radiation, which water removes and shields.', 6, 'multi_step')])

add_f('ch12-st1',
      evaluate=[('The Sun will run out of fuel in the near future.', ['fusion consumes about 6 × 10¹¹ kg of hydrogen per second'], ['the Sun contains ~10³⁰ kg of hydrogen; only the core fuses', 'the main-sequence lifetime is ~10¹⁰ years, with about 5 × 10⁹ years remaining'], 'No: although the consumption rate is huge, the Sun has billions of years of core hydrogen remaining.')],
      extended=[('The Sun’s luminosity is 3.83 × 10²⁶ W and its mass 1.99 × 10³⁰ kg. (a) Calculate the mass converted to energy each second. (b) The fusion of hydrogen to helium converts 0.7 % of the mass of hydrogen to energy; calculate the mass of hydrogen fused each second. (c) If 10 % of the Sun’s mass is available for core fusion, estimate the Sun’s main-sequence lifetime in years.', '(a) Δm/Δt = L/c² = 4.26 × 10⁹ kg s⁻¹; (b) 4.26 × 10⁹/0.007 = 6.1 × 10¹¹ kg s⁻¹; (c) 1.99 × 10²⁹/6.1 × 10¹¹ = 3.3 × 10¹⁷ s ≈ 1.0 × 10¹⁰ years.', 6, 'multi_step')])

add_f('ch12-st2',
      evaluate=[('The Hertzsprung–Russell diagram shows that stars evolve along the main sequence from hot to cool.', ['the main sequence is a continuous band from hot luminous to cool dim stars'], ['position on the main sequence is set by mass, not age', 'stars stay near one point while fusing hydrogen and then move off towards giants', 'the diagram is a snapshot of many stars, not one star’s track'], 'Incorrect: the main sequence is a mass sequence; evolution moves stars off it, not along it.')],
      extended=[('Star X has surface temperature 3500 K and luminosity 4.0 × 10⁴ L☉; star Y has surface temperature 14 000 K and luminosity 0.010 L☉. (a) Calculate the ratio of their radii R_X/R_Y. (b) Identify each type of star and its position on the HR diagram. (c) Describe the evolutionary connection between the two types.', '(a) R ∝ √L/T²: R_X/R_Y = √(4.0 × 10⁶) × (14 000/3500)² = 2000 × 16 = 3.2 × 10⁴; (b) X: red supergiant (top right); Y: white dwarf (bottom left); (c) not directly: a red supergiant is too massive and will end as a neutron star or black hole; white dwarfs come from low-mass stars after the red-giant and planetary-nebula stages.', 6, 'multi_step')])

add_f('ch12-st4',
      evaluate=[('Black holes are the inevitable end point of all massive stars.', ['cores above ~3 M☉ cannot be supported by neutron degeneracy pressure'], ['many massive stars lose mass through winds and end as neutron stars', 'some very massive stars may be completely disrupted (pair-instability supernovae)', 'core mass, not initial mass alone, decides the outcome'], 'Only stars whose remnant cores exceed about 3 M☉ form black holes; others leave neutron stars or nothing.')],
      extended=[('A main-sequence star has 6 times the mass of the Sun. (a) Using L ∝ M^3.5, estimate its luminosity. (b) Estimate its main-sequence lifetime given the Sun’s is 1.0 × 10¹⁰ years. (c) Describe its likely evolution and final state, referring to the Chandrasekhar limit.', '(a) 6^3.5 ≈ 530 L☉; (b) 10¹⁰ × 6^−2.5 ≈ 1.1 × 10⁸ years; (c) it becomes a red giant, fuses helium (and possibly carbon), sheds its outer layers as a planetary nebula; its core, below 1.4 M☉, becomes a carbon–oxygen white dwarf.', 5, 'multi_step')])


@R.add('ch09-st2', 'C4', (4, 5), 'multi_step')
def c4_dual_frames(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        T_ = rng.choice([290, 300, 320, 350])
        Ek = 1.5 * 1.38e-23 * T_
        lam = H / math.sqrt(2 * MN * Ek)
        return num(f'At the Institut Laue–Langevin in Grenoble, neutrons from a reactor are slowed in a moderator at {T_} K and used to study crystal structures. (a) Estimate the mean kinetic energy of a thermal neutron, using E = (3/2)k_B T. (b) Hence determine its de Broglie wavelength. (c) Explain why thermal neutrons, rather than visible light, are suitable for probing atomic spacings of about 10⁻¹⁰ m. (d) Suggest one advantage neutrons have over X-rays for locating hydrogen atoms.',
                   f'(a) {q(Ek, "J")}; (b) λ = {q(lam, "m")}; (c) λ is comparable with atomic spacing, so measurable diffraction occurs (visible light ≈ 5 × 10⁻⁷ m is far too long); (d) neutrons scatter from nuclei, so light atoms such as hydrogen scatter strongly, whereas X-rays scatter from electrons.',
                   f'(a) E = 1.5 × 1.38 × 10⁻²³ × {T_} (M1) = {q(Ek, "J")} (A1). (b) λ = h/√(2mE) (M1) = {q(lam, "m")} (A1). (c) λ ≈ atomic spacing → diffraction (R1). (d) nuclear scattering / independent of electron number (R1).', 6, 'multi_step')
    if k == 1:
        V = rng.choice([20e3, 40e3, 80e3])
        lam = H / math.sqrt(2 * ME * E * V)
        return num(f'A transmission electron microscope in Tokyo accelerates electrons through {sf(V / 1e3, 2)} kV. (a) Calculate the non-relativistic de Broglie wavelength of the electrons. (b) Compare the result with the shortest wavelength of visible light (400 nm) and explain why electron microscopes resolve much finer detail. (c) The engineers double the accelerating voltage. Determine the factor by which the wavelength changes. (d) Discuss whether the non-relativistic formula remains reliable at this voltage.',
                   f'(a) λ = {q(lam, "m")}; (b) about {sf(4.0e-7 / lam, 2)} times shorter, and resolution scales with wavelength; (c) λ ∝ V^(−1/2), so λ falls by 1/√2 = 0.707; (d) the kinetic energy is a noticeable fraction of mₑc² = 511 keV, so relativistic corrections of a few per cent or more are needed.',
                   f'(a) p = √(2meV) (M1), λ = h/p = {q(lam, "m")} (A1). (b) ratio (A1) + resolution argument (R1). (c) factor 0.707 (A1). (d) compares eV with 511 keV (R1).', 6, 'multi_step')
    if k == 2:
        V = rng.choice([100, 200, 500])
        le = H / math.sqrt(2 * ME * E * V)
        vp = H / (MP * le)
        Ep = 0.5 * MP * vp ** 2 / E
        return num(f'A physicist claims that an electron and a proton can be given equal de Broglie wavelengths. (a) An electron is accelerated from rest through {V} V. Calculate its de Broglie wavelength. (b) Determine the speed a proton must have to share this wavelength. (c) Calculate the kinetic energy of that proton in eV and comment on the ratio of the two kinetic energies. (d) Evaluate whether such a proton would produce the same diffraction pattern as the electron.',
                   f'(a) {q(le, "m")}; (b) v = h/(mₚλ) = {q(vp, "m s⁻¹")}; (c) {q(Ep, "eV")}, smaller by mₑ/mₚ ≈ 1/1836, because equal p means E = p²/2m; (d) yes, same λ gives the same angles, though the proton detection and charge effects differ.',
                   f'(a) λ (M1 A1). (b) v = {q(vp, "m s⁻¹")} (A1). (c) E = {q(Ep, "eV")} (A1) with ratio explained (R1). (d) equal λ → equal pattern (R1).', 6, 'multi_step')
    if k == 3:
        m = 720 * U
        v = rng.choice([150, 200, 220])
        lam = H / (m * v)
        return num(f'In 1999, Arndt and Zeilinger’s group in Vienna observed interference of C₆₀ fullerene molecules (mass 720 u) passing through a grating with 100 nm period. (a) Calculate the de Broglie wavelength of a molecule moving at {v} m s⁻¹. (b) Estimate the first-order diffraction angle. (c) Explain why such an experiment is far harder than electron diffraction. (d) Discuss what the result suggests about the limits of wave–particle duality.',
                   f'(a) λ = {q(lam, "m")}; (b) θ ≈ λ/d = {q(lam / 1e-7, "rad")}; (c) the very small λ gives tiny angles, so a narrow, well-collimated beam and long flight path are needed, and collisions or thermal emission can destroy coherence; (d) duality appears to apply to large, complex objects, with no clear quantum–classical boundary yet found.',
                   f'(a) m = 720 × 1.661 × 10⁻²⁷ kg (M1), λ = {q(lam, "m")} (A1). (b) θ = {q(lam / 1e-7, "rad")} (A1). (c) two valid difficulties (R1 R1). (d) reasoned comment (R1).', 6, 'multi_step')
    Ek = rng.choice([5.0, 7.7, 10.0])
    p = math.sqrt(2 * 4 * U * Ek * 1e6 * E)
    lam = H / p
    rN = R0 * 197 ** (1 / 3)
    return num(f'Rutherford’s alpha particles had kinetic energies of a few MeV. (a) Calculate the de Broglie wavelength of a {sf(Ek, 2)} MeV alpha particle (mass 4.00 u). (b) Calculate the radius of a gold-197 nucleus using R = R₀A^(1/3). (c) Compare the two lengths and explain why the alpha particles probe nuclear size only roughly. (d) Suggest why high-energy electrons are used instead to measure nuclear radii precisely.',
               f'(a) λ = {q(lam, "m")}; (b) R = {q(rN, "m")}; (c) λ is of the same order as R, so diffraction blurs fine detail; (d) electrons are not subject to the strong force, and at high energy they have λ well below 10⁻¹⁵ m, giving a clean diffraction minimum.',
               f'(a) p = √(2mE) (M1), λ = {q(lam, "m")} (A1). (b) R (A1). (c) comparison (R1). (d) two reasons (R1 R1).', 6, 'multi_step')
