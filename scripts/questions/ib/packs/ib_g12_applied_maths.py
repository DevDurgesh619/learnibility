"""IB DP Mathematics: Applications and Interpretation SL/HL (2019 guide), DP year 2 – ib-g12-applied-maths.

Topic 3 Geometry and trigonometry (SL 3.1-3.6, AHL 3.7-3.16), topic 5 Calculus (SL 5.1-5.8, AHL 5.9-5.18),
topic 4 inferential statistics (SL 4.11, AHL 4.15-4.19) and the mathematical exploration / Paper 3.

Every numerical item is parametric and computes its own answer (numpy, sympy and small numerical routines
standing in for the GDC: normal, t, chi-squared, binomial and Poisson distributions, graph algorithms,
Euler's method, numerical integration). Answers are exact or correct to 3 significant figures; angles in
degrees to 3 s.f. unless radians are asked for. Marking keys use markscheme notation (M1, A1, R1, AG, FT).

Shared helpers (number formatting, distributions, mock-paper assembly) come from the year-1 pack
ib_g11_applied_maths.py so both years present answers and markschemes identically.

Mock = HL-style paper set (calculator throughout): Paper 1 short-response, Paper 2 extended-response and a
Paper 3 extended problem; every mock carries the same marks (13 × 7 + 8 × 13 + 2 × 20 = 235).
"""
from __future__ import annotations

import math
import re
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
import ib_g11_applied_maths as Y1
from ib_g11_applied_maths import (sf, sfv, sci, money, m, sgn, poly, ret, nmcq, pick, cur, ncdf, ninv, binpmf, bincdf,  # noqa: F401
                                  poipmf, poicdf, bisect, pearson, strength, _num, mat, lin3, fr, frd, _roots_num, MINUS, ALL, frs)

CONFIG = {'minutesPerMark': 1.1, 'mcqMinutes': 1.5}

MOCK = [
    dict(section='Paper 1 – short-response questions (calculator)', count=13, c=['C3', 'C2', 'C3', 'C4'], d=[2, 3, 3, 4], type='multi_step', marks=7, style='p1'),
    dict(section='Paper 2 – extended-response questions (calculator)', count=8, c=['C3', 'C4'], d=[3, 4, 4], type='multi_step', marks=13, style='p2'),
    dict(section='Paper 3 – extended problem (HL)', count=2, c=['C4'], d=[4, 5], type='long', marks=20, style='p3'),
]

R = Registry()


def init(subject_id):
    pass


_CACHE: dict = {}


def templates(st):
    if st['id'] in _CACHE:
        return _CACHE[st['id']]
    base = R.build(st)
    out = list(base)
    for i, spec in enumerate(Y1.P1_SPECS):
        out.append(T(('C2', 'C3', 'C4'), (2, 5), Y1.composite(st, base, spec, 'p1', 7), 'multi_step', 'p1', f'p1_{i}'))
    for i, spec in enumerate(Y1.P2_SPECS):
        out.append(T(('C3', 'C4'), (3, 5), Y1.composite(st, base, spec, 'p2', 13), 'multi_step', 'p2', f'p2_{i}'))
    for i, spec in enumerate(Y1.P3_SPECS):
        out.append(T('C4', (4, 5), Y1.composite(st, base, spec, 'p3', 20), 'long', 'p3', f'p3_{i}'))
    _CACHE[st['id']] = out
    return out


def nv(v, n=3):
    """exact short decimal if v is one (≤ 4 dp), else n s.f."""
    v = float(v)
    return m(_num(round(v, 4))) if abs(v - round(v, 4)) < 1e-9 else sf(v, n)


def sind(a):
    return math.sin(math.radians(a))


def cosd(a):
    return math.cos(math.radians(a))


def tand(a):
    return math.tan(math.radians(a))


def deg(x):
    return math.degrees(x)


def vec(v):
    return '(' + ', '.join(m(_num(float(x))) for x in v) + ')'


def pt(p):
    return '(' + ', '.join(m(_num(float(x))) for x in p) + ')'


x_ = sp.Symbol('x')


def pe(expr):
    s = sp.sstr(expr)
    s = re.sub(r'\*\*\((-?\d+)/(\d+)\)', r'^(\1/\2)', s)
    s = re.sub(r'\*\*(\d+)', lambda mm: sup(mm.group(1)), s)
    s = re.sub(r'\*\*\(?(-\d+)\)?', lambda mm: sup(mm.group(1)), s)
    s = s.replace('exp(', 'e^(').replace('log(', 'ln(').replace('sqrt(', '√(')
    s = re.sub(r'(\d)\*([a-zA-Z(√])', r'\1\2', s)
    s = s.replace('*', '·')
    return m(s)


# ---- distributions for inference -----------------------------------------------------------
def _gser(a, x):
    s = term = 1.0 / a
    ap = a
    for _ in range(500):
        ap += 1
        term *= x / ap
        s += term
        if abs(term) < abs(s) * 1e-15:
            break
    return s * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a, x):
    b = x + 1 - a
    c = 1e300
    d = 1 / b
    h = d
    for i in range(1, 500):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1 / d
        de = d * c
        h *= de
        if abs(de - 1) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def gammp(a, x):
    if x <= 0:
        return 0.0
    return _gser(a, x) if x < a + 1 else 1 - _gcf(a, x)


def chi2_sf(x, k):
    return 1 - gammp(k / 2, x / 2)


def chi2_inv(p, k):
    """critical value c with P(χ² > c) = p"""
    return bisect(lambda c: chi2_sf(c, k) - p, 1e-9, 200)


def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m_ in range(1, 300):
        m2 = 2 * m_
        aa = m_ * (b - m_) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c
        h *= d * c
        aa = -(a + m_) * (qab + m_) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c
        de = d * c
        h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def betai(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1 - bt * _betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t)
    tail = 0.5 * betai(df / 2, 0.5, x)
    return 1 - tail if t > 0 else tail


def t_inv(p, df):
    return bisect(lambda t: t_cdf(t, df) - p, -50, 50)


def pv(p):
    """p-value text"""
    if p < 1e-10:
        return '< 1 × 10⁻¹⁰'
    return sf(p) if p >= 0.0001 else sci(p)


# =============================================================================================
# ch01 Geometry and trigonometry in 2D and 3D
# =============================================================================================
SOLIDS = {
    'cone': (lambda r, h: math.pi * r * r * h / 3, lambda r, h: math.pi * r * (r + math.hypot(r, h)), 'V = (1/3)πr²h', 'A = πr² + πrl, l = √(r² + h²)'),
    'cylinder': (lambda r, h: math.pi * r * r * h, lambda r, h: 2 * math.pi * r * (r + h), 'V = πr²h', 'A = 2πr² + 2πrh'),
    'square-based pyramid': (lambda r, h: (2 * r) ** 2 * h / 3, lambda r, h: (2 * r) ** 2 + 4 * r * math.hypot(r, h), 'V = (1/3)(base area)h', 'A = base + 4 triangles (slant height √(h² + (b/2)²))'),
    'hemisphere': (lambda r, h: 2 * math.pi * r ** 3 / 3, lambda r, h: 3 * math.pi * r * r, 'V = (2/3)πr³', 'A = 2πr² + πr² (curved + base)'),
    'sphere': (lambda r, h: 4 * math.pi * r ** 3 / 3, lambda r, h: 4 * math.pi * r * r, 'V = (4/3)πr³', 'A = 4πr²'),
}

R.facts('ch01-st1', F(
    terms=[('distance between two points in 3D', 'd = √((x₁ − x₂)² + (y₁ − y₂)² + (z₁ − z₂)²)'),
           ('midpoint in 3D', '((x₁ + x₂)/2, (y₁ + y₂)/2, (z₁ + z₂)/2)'),
           ('angle between a line and a plane', 'the angle between the line and its projection (orthogonal shadow) onto the plane'),
           ('slant height of a cone', 'l = √(r² + h²), the distance from the apex to a point on the circumference of the base')],
    facts=[('What is the volume of a cone with radius 3 cm and height 4 cm?', '12π cm³', ['36π cm³', '4π cm³', '15π cm³'], '(1/3)π × 9 × 4 = 12π.'),
           ('Which formula gives the surface area of a sphere?', '4πr²', ['(4/3)πr³', '2πr²', 'πr²'], 'From the IB formula booklet.'),
           ('The angle between a line and a plane is measured between the line and…', 'its projection onto the plane', ['the normal to the plane', 'any line in the plane', 'the x-axis'], 'Use the shadow of the line on the plane.')],
    why=[('Explain why the 3D distance formula is an extension of Pythagoras\' theorem.', 'Apply Pythagoras in the base plane to get √(Δx² + Δy²), then again in the vertical right-angled triangle with the height difference Δz: d² = Δx² + Δy² + Δz².'),
         ('Explain why a cone has one-third of the volume of a cylinder with the same base and height.', 'The cone tapers linearly to a point; summing its circular cross-sections (or by experiment/calculus) gives exactly one-third of the prism volume, as for any pyramid.')],
    misc=[('The curved surface area of a cone is πrh.', 'It is πrl, where l is the slant height √(r² + h²), not the vertical height h.')],
))


@R.add('ch01-st1', ALL, (1, 5), 'short')
def solids_core(rng, slot):
    c, d = slot.c, slot.d
    if c in ('C1', 'C2') and rng.random() < 0.5:
        A = np.array([rng.randint(-6, 8) for _ in range(3)])
        B = np.array([rng.randint(-6, 8) for _ in range(3)])
        dist = float(np.linalg.norm(A - B))
        mid = (A + B) / 2
        if c == 'C1':
            return ret(f'Find the distance between A{pt(A)} and B{pt(B)} and the coordinates of the midpoint of AB.', f'{sf(dist)}; {pt(mid)}',
                       f'√({" + ".join(f"({m(_num(a - b))})²" for a, b in zip(A, B))}) (M1) = {sf(dist)} (A1); midpoint {pt(mid)} (A1).', 3)
        return ret(f'A drone flies in a straight line from A{pt(A)} to B{pt(B)} (units: hundreds of metres). {name(rng)} says the distance is |{_num(B[0] - A[0])}| + |{_num(B[1] - A[1])}| + |{_num(B[2] - A[2])}|. Explain why this is wrong and find the correct distance.',
                   f'{sf(dist)} hundred metres', f'R1 that adds components along the axes (a path along the edges of a box), not the straight-line distance; M1 √(Δx² + Δy² + Δz²); A1 {sf(dist)}.', 3, 'explain', gap='G2')
    solid = pick(rng, list(SOLIDS))
    V, S, vf, sfm = SOLIDS[solid]
    r, h = round(rng.uniform(2, 15), 1), round(rng.uniform(4, 30), 1)
    use = pick(rng, ['a grain silo', 'a paperweight', 'a traffic cone', 'a water tank', 'a perfume bottle cap', 'a garden planter'])
    dims = f'radius {r} cm' + ('' if solid in ('hemisphere', 'sphere') else f' and height {h} cm') if solid != 'square-based pyramid' else f'base side {_num(2 * r)} cm and height {h} cm'
    if c == 'C1':
        return ret(f'A {solid} has {dims}. Find its volume.', f'{sf(V(r, h))} cm³', f'{vf} (M1) = {sf(V(r, h))} cm³ (A1).', 2)
    if c == 'C2':
        k = rng.choice([2, 3, 0.5])
        return ret(f'A {solid} has {dims}. Explain what happens to its volume and its surface area if every length is multiplied by {_num(k)}.', f'volume × {_num(k ** 3)}, surface area × {_num(k ** 2)}',
                   f'R1 areas scale by the square of the length factor: × {_num(k ** 2)}; R1 volumes scale by the cube: × {_num(k ** 3)}; A1 e.g. V from {sf(V(r, h))} to {sf(V(k * r, k * h))} cm³.', 3, 'explain')
    if c == 'C3':
        return ret(f'{use[0].upper() + use[1:]} is modelled as a {solid} with {dims}. Find its volume and its total surface area.', f'V = {sf(V(r, h))} cm³, A = {sf(S(r, h))} cm²',
                   f'{vf} (M1) = {sf(V(r, h))} (A1); {sfm} (M1) = {sf(S(r, h))} (A1).', 4, 'numerical')
    # C4: cuboid diagonal angle with base / composite solid
    L, W, H = rng.randint(3, 15), rng.randint(2, 12), rng.randint(2, 10)
    diag = math.sqrt(L * L + W * W + H * H)
    ang = deg(math.atan(H / math.hypot(L, W)))
    cap = pick(rng, [('a storage box', 'cm'), ('a shipping container', 'm'), ('a classroom', 'm'), ('a fish tank', 'dm')])
    return ret(f'{cap[0][0].upper() + cap[0][1:]} is a cuboid ABCDEFGH with base ABCD, AB = {L} {cap[1]}, BC = {W} {cap[1]} and height AE = {H} {cap[1]}. (a) Find the length of the base diagonal AC. (b) Find the length of the space diagonal AG. '
               f'(c) Find the angle between AG and the base ABCD. (d) A rod of length {sf(diag * rng.uniform(0.85, 1.1))} {cap[1]} is to fit inside; determine whether it fits.',
               f'(a) {sf(math.hypot(L, W))} (b) {sf(diag)} (c) {sf(ang)}°', f'(a) √({L}² + {W}²) = {sf(math.hypot(L, W))} (M1 A1). (b) √({L}² + {W}² + {H}²) = {sf(diag)} (A1). (c) tan θ = {H}/{sf(math.hypot(L, W))} (M1) ⇒ {sf(ang)}° (A1). '
               f'(d) R1 compare with the space diagonal {sf(diag)}.', 7, 'multi_step', gap='G5')


R.facts('ch01-st2', F(
    terms=[('sine rule', 'a/sin A = b/sin B = c/sin C, used when a side and its opposite angle are known'),
           ('cosine rule', 'c² = a² + b² − 2ab cos C, used with two sides and the included angle, or three sides'),
           ('area of a triangle', 'A = ½ab sin C, using two sides and the included angle'),
           ('ambiguous case', 'when two sides and a non-included acute angle are known, the sine rule can give two possible triangles')],
    facts=[('In triangle ABC, a = 7, b = 9 and C = 60°. Which rule finds c?', 'cosine rule', ['sine rule', 'Pythagoras\' theorem', 'area formula'], 'Two sides and the included angle.'),
           ('What is the area of a triangle with sides 6 cm and 10 cm and included angle 30°?', '15 cm²', ['30 cm²', '60 cm²', '26.0 cm²'], '½ × 6 × 10 × sin 30° = 15.')],
    why=[('Explain why the sine rule can give two possible values for an angle.', 'sin θ = sin(180° − θ), so an equation sin B = k (0 < k < 1) has an acute and an obtuse solution; both may give valid triangles if the angles sum to less than 180°.'),
         ('Explain why the cosine rule reduces to Pythagoras\' theorem when C = 90°.', 'cos 90° = 0, so the term −2ab cos C vanishes, leaving c² = a² + b².')],
    misc=[('In any triangle, sin A = opposite/hypotenuse.', 'SOH-CAH-TOA applies only to right-angled triangles; for other triangles use the sine and cosine rules.')],
))


@R.add('ch01-st2', ALL, (1, 5), 'short')
def trig_core(rng, slot):
    c, d = slot.c, slot.d
    a, b = round(rng.uniform(4, 25), 1), round(rng.uniform(4, 25), 1)
    C = rng.randint(25, 140)
    cc = math.sqrt(a * a + b * b - 2 * a * b * cosd(C))
    area = 0.5 * a * b * sind(C)
    if c == 'C1':
        if rng.random() < 0.5:
            hyp = round(rng.uniform(5, 30), 1)
            th = rng.randint(15, 75)
            return ret(f'A ladder of length {hyp} m leans against a vertical wall, making an angle of {th}° with the horizontal ground. Find how high up the wall it reaches.', f'{sf(hyp * sind(th))} m',
                       f'{hyp} sin {th}° (M1) = {sf(hyp * sind(th))} m (A1).', 2)
        return ret(f'In triangle PQR, PQ = {a} cm, PR = {b} cm and angle QPR = {C}°. Find the area of the triangle.', f'{sf(area)} cm²', f'½ × {a} × {b} × sin {C}° (M1) = {sf(area)} cm² (A1).', 2)
    if c == 'C2':
        A_ = rng.randint(25, 60)
        side_a = round(rng.uniform(5, 12), 1)
        side_b = round(side_a / sind(A_) * rng.uniform(0.6, 0.95) * 1.0, 1)
        side_b = round(side_a * rng.uniform(1.05, 1.6), 1)
        sB = side_b * sind(A_) / side_a
        if sB >= 1:
            return None
        B1 = deg(math.asin(sB))
        B2 = 180 - B1
        two = A_ + B2 < 180
        return ret(f'In triangle ABC, angle A = {A_}°, BC = {side_a} cm and AC = {side_b} cm. Explain why there may be two possible triangles and find the possible values of angle B.',
                   f'B = {sf(B1)}°' + (f' or {sf(B2)}°' if two else ''), f'sin B = {side_b} sin {A_}°/{side_a} = {sf(sB)} (M1 A1); B = {sf(B1)}° (A1); R1 {"also B = 180° − " + sf(B1) + "° = " + sf(B2) + "° since A + B < 180°" if two else "180° − " + sf(B1) + "° is too large, so only one triangle"}.',
                   4, 'explain')
    if c == 'C3':
        return ret(f'Two straight paths leave a point P at an angle of {C}° to each other. A walker goes {a} km along one and a cyclist {b} km along the other. Find the direct distance between them and the area of the triangle formed.',
                   f'{sf(cc)} km; {sf(area)} km²', f'c² = {a}² + {b}² − 2({a})({b})cos {C}° (M1 A1); c = {sf(cc)} km (A1); area = ½({a})({b}) sin {C}° = {sf(area)} km² (A1).', 4, 'numerical')
    B = deg(math.asin(b * sind(C) / cc))
    A_ = 180 - C - B
    per = a + b + cc
    return ret(f'A triangular plot of land XYZ has XY = {a} m, XZ = {b} m and angle YXZ = {C}°. (a) Find YZ. (b) Find angle XYZ. (c) Find the area of the plot. (d) Fencing costs {rng.randint(12, 40)} {cur(rng)} per metre; find the cost of fencing the perimeter.',
               f'(a) {sf(cc)} m (b) {sf(B)}° (c) {sf(area)} m² (d) see key', f'(a) cosine rule (M1) {sf(cc)} (A1). (b) sine rule sin Y = {b} sin {C}°/{sf(cc)} (M1) ⇒ {sf(B)}° (A1). (c) ½ × {a} × {b} × sin {C}° = {sf(area)} (A1). '
               f'(d) perimeter {sf(per)} m (M1) × rate (A1).', 8, 'multi_step', gap='G5')


R.facts('ch01-st3', F(
    terms=[('angle of elevation', 'the angle measured upwards from the horizontal to the line of sight'),
           ('angle of depression', 'the angle measured downwards from the horizontal to the line of sight'),
           ('true bearing', 'a direction given as a three-figure angle measured clockwise from north, e.g. 075°')],
    facts=[('The bearing of B from A is 070°. What is the bearing of A from B?', '250°', ['110°', '290°', '070°'], 'Add 180°.'),
           ('Due south-west as a three-figure bearing is…', '225°', ['045°', '135°', '315°'], 'Clockwise from north.')],
    why=[('Explain why the angle of elevation of A from B equals the angle of depression of B from A.', 'The horizontals at A and B are parallel; the line of sight is a transversal, so the two angles are alternate angles and are equal.'),
         ('Explain why a labelled diagram is important when solving bearings problems.', 'It shows north lines at each point and which angles are known, so that the correct triangle and angle relationships (e.g. co-interior angles) can be identified.')],
    misc=[('A bearing of 30° from north is written as 30°.', 'True bearings are written with three figures: 030°.')],
))


@R.add('ch01-st3', ALL, (1, 5), 'short')
def bearings_core(rng, slot):
    c, d = slot.c, slot.d
    if c in ('C1', 'C3') and rng.random() < 0.5:
        dist = rng.randint(20, 300)
        ang = rng.randint(8, 60)
        thing = pick(rng, [('a lighthouse', 'a boat at sea', 'the top of'), ('a cliff', 'a kayak', 'the edge of'), ('a tower', 'a car', 'the top of'), ('a hot-air balloon', 'a landing field', '')])
        h = dist * tand(ang)
        if c == 'C1':
            return ret(f'From a point on level ground {dist} m from the base of {thing[0]}, the angle of elevation of its top is {ang}°. Find the height of {thing[0]}.', f'{sf(h)} m', f'tan {ang}° = h/{dist} (M1); h = {sf(h)} m (A1).', 2)
        ang2 = ang + rng.randint(5, 20)
        d2 = h / tand(ang2)
        return ret(f'From the top of {thing[0]} of height {sf(h, 4)} m, the angle of depression of {thing[1]} changes from {ang}° to {ang2}° as it moves directly towards the base. Find the distance travelled.', f'{sf(dist - d2)} m',
                   f'Initial distance {sf(h, 4)}/tan {ang}° = {sf(dist)} (M1 A1); final {sf(h, 4)}/tan {ang2}° = {sf(d2)} (A1); travelled {sf(dist - d2)} m (A1).', 4, 'numerical')
    b1 = rng.randint(10, 170)
    b2 = rng.randint(b1 + 30, b1 + 160) % 360
    d1, d2_ = rng.randint(5, 40), rng.randint(5, 40)
    P1 = np.array([d1 * sind(b1), d1 * cosd(b1)])
    P2 = P1 + np.array([d2_ * sind(b2), d2_ * cosd(b2)])
    dist = float(np.linalg.norm(P2))
    back = (deg(math.atan2(-P2[0], -P2[1])) + 360) % 360
    br = (deg(math.atan2(P2[0], P2[1])) + 360) % 360
    who = pick(rng, ['A ship', 'A hiker', 'A drone', 'A yacht', 'A search-and-rescue helicopter'])
    if c == 'C1':
        return mcq(rng, f'The bearing of a hut H from a camp C is {b1:03d}°. What is the bearing of C from H?', f'{(b1 + 180) % 360:03d}°', [f'{(180 - b1) % 360:03d}°', f'{(360 - b1) % 360:03d}°', f'{(b1 + 90) % 360:03d}°'], 'Back bearing = bearing ± 180°.')
    if c == 'C2':
        return ret(f'{who} travels {d1} km on a bearing of {b1:03d}° and then {d2_} km on a bearing of {b2:03d}°. Explain how to find the angle at the turning point in the triangle formed, and find it.', f'{sf(180 - abs(b2 - b1)) if abs(b2 - b1) < 180 else sf(abs(b2 - b1) - 180)}°',
                   f'R1 draw north lines at both points; R1 the angle between the reverse of the first leg ({(b1 + 180) % 360:03d}°) and the second leg ({b2:03d}°); A1 {sf(min(abs(((b1 + 180) % 360) - b2), 360 - abs(((b1 + 180) % 360) - b2)))}°.', 3, 'explain')
    if c == 'C3':
        return ret(f'{who} leaves port P and travels {d1} km on a bearing of {b1:03d}° and then {d2_} km on a bearing of {b2:03d}°. Find its distance from P.', f'{sf(dist)} km',
                   f'Angle at the turn found from the bearings (M1 A1); cosine rule (M1); {sf(dist)} km (A1).', 4, 'numerical')
    return ret(f'{who} leaves port P and travels {d1} km on a bearing of {b1:03d}° to A, then {d2_} km on a bearing of {b2:03d}° to B. (a) Draw a labelled diagram. (b) Find the distance PB. (c) Find the bearing of B from P. (d) Find the bearing on which it must travel to return directly to P.',
               f'(b) {sf(dist)} km (c) {br:05.1f}° (d) {back:05.1f}°', f'(a) A1 diagram with north lines. (b) angle PAB (M1 A1), cosine rule (M1) {sf(dist)} (A1). (c) sine rule for angle APB (M1), bearing {br:05.1f}° (A1). (d) {back:05.1f}° (A1).', 8, 'multi_step', gap='G5')


R.facts('ch01-st4', F(
    terms=[('arc length (degrees)', 'l = (θ/360) × 2πr for a sector of angle θ° and radius r'),
           ('area of a sector (degrees)', 'A = (θ/360) × πr²'),
           ('perimeter of a sector', 'two radii plus the arc: 2r + l')],
    facts=[('A sector has radius 6 cm and angle 60°. What is its arc length?', '2π cm', ['6π cm', 'π cm', '12π cm'], '(60/360) × 12π.'),
           ('A sector has radius 10 cm and angle 90°. What is its area?', '25π cm²', ['50π cm²', '100π cm²', '5π cm²'], '¼ × 100π.')],
    why=[('Explain why the arc length of a sector is (θ/360) × 2πr.', 'The full circle (360°) has circumference 2πr; a sector of θ° is the fraction θ/360 of the circle, so its arc is that fraction of the circumference.')],
    misc=[('The perimeter of a sector is its arc length.', 'The perimeter also includes the two radii: P = 2r + arc length.')],
))


@R.add('ch01-st4', ALL, (1, 5), 'short')
def sector_core(rng, slot):
    c, d = slot.c, slot.d
    r = round(rng.uniform(2, 40), 1)
    th = rng.randint(20, 300)
    L = th / 360 * 2 * math.pi * r
    A = th / 360 * math.pi * r * r
    ctx = pick(rng, ['a slice of pizza', 'a garden flower bed', 'a fan blade sweep', 'a windscreen wiper path', 'a sprinkler coverage area', 'a pendulum swing'])
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'A sector has radius {r} cm and angle {th}°. Find its arc length.', L, [A, th / 360 * math.pi * r, th * r], f'({th}/360) × 2π × {r} = {sf(L)}.')
        return ret(f'{ctx[0].upper() + ctx[1:]} is modelled as a sector of radius {r} cm and angle {th}°. Find its area.', f'{sf(A)} cm²', f'({th}/360) × π × {r}² (M1) = {sf(A)} cm² (A1).', 2)
    if c == 'C2':
        return ret(f'Explain why doubling the radius of a sector (keeping the angle {th}°) doubles the arc length but quadruples the area. Use r = {r} cm to illustrate.', f'arc {sf(L)} → {sf(2 * L)}; area {sf(A)} → {sf(4 * A)}',
                   f'R1 arc ∝ r; R1 area ∝ r²; A1 values {sf(L)} → {sf(2 * L)} and {sf(A)} → {sf(4 * A)}.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            return ret(f'{ctx[0].upper() + ctx[1:]} is a sector of radius {r} cm and angle {th}°. Find its perimeter and area.', f'P = {sf(2 * r + L)} cm, A = {sf(A)} cm²',
                       f'arc = {sf(L)} (M1 A1); perimeter = 2 × {r} + {sf(L)} = {sf(2 * r + L)} (A1); area = {sf(A)} (A1).', 4, 'numerical')
        th2 = 360 * A / (math.pi * r * r)
        return ret(f'A sector of radius {r} cm has area {sf(A, 4)} cm². Find the angle of the sector and its arc length.', f'{sf(th2)}°; {sf(L)} cm', f'(θ/360)π{r}² = {sf(A, 4)} (M1) ⇒ θ = {sf(th2)}° (A1); arc = {sf(L)} cm (A1).', 3, 'numerical')
    seg = A - 0.5 * r * r * sind(th) if th < 180 else None
    if seg is None:
        th = rng.randint(30, 160)
        L = th / 360 * 2 * math.pi * r
        A = th / 360 * math.pi * r * r
        seg = A - 0.5 * r * r * sind(th)
    chord = 2 * r * sind(th / 2)
    return ret(f'A window is designed as a sector OAB of a circle with centre O, radius {r} cm and angle AOB = {th}°. (a) Find the arc length AB. (b) Find the length of the chord AB. (c) Find the area of the segment between the chord and the arc. (d) Glass costs {rng.randint(2, 9)} {cur(rng)} per 100 cm²; find the cost of glass for the segment.',
               f'(a) {sf(L)} cm (b) {sf(chord)} cm (c) {sf(seg)} cm²', f'(a) M1 A1. (b) cosine rule or 2r sin(θ/2) (M1) = {sf(chord)} (A1). (c) sector − triangle = {sf(A)} − ½({r})² sin {th}° (M1) = {sf(seg)} (A1). (d) A1 cost.', 7, 'multi_step', gap='G5')


# =============================================================================================
# ch02 Voronoi diagrams
# =============================================================================================
def perp_bis(P, Q):
    """returns (gradient Fraction or None for vertical, intercept Fraction, midpoint)"""
    mx, my = Fr(P[0] + Q[0], 2), Fr(P[1] + Q[1], 2)
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    if dy == 0:
        return None, mx, (mx, my)
    g = Fr(-dx, dy)
    return g, my - g * mx, (mx, my)


def bis_text(P, Q):
    g, c0, mid = perp_bis(P, Q)
    if g is None:
        return f'x = {Y1.frs(c0)}'
    return Y1.line_eq(g, c0)


def circumcentre(A, B, C):
    ax, ay = A
    bx, by = B
    cx_, cy = C
    dd = 2 * (ax * (by - cy) + bx * (cy - ay) + cx_ * (ay - by))
    if dd == 0:
        return None
    ux = Fr((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx_ * cx_ + cy * cy) * (ay - by), dd)
    uy = Fr((ax * ax + ay * ay) * (cx_ - bx) + (bx * bx + by * by) * (ax - cx_) + (cx_ * cx_ + cy * cy) * (bx - ax), dd)
    return ux, uy


def _sites(rng, k, lo=0, hi=12):
    pts = set()
    while len(pts) < k:
        pts.add((rng.randint(lo, hi), rng.randint(lo, hi)))
    return sorted(pts)


def fpt(p):
    return '(' + ', '.join(Y1.frs(v) if isinstance(v, Fr) else m(_num(v)) for v in p) + ')'


R.facts('ch02-st1', F(
    terms=[('perpendicular bisector', 'the line through the midpoint of a segment AB at right angles to AB; every point on it is equidistant from A and B'),
           ('equidistant', 'at equal distances from two or more points')],
    facts=[('The perpendicular bisector of the segment joining (0, 0) and (4, 0) is…', 'x = 2', ['y = 2', 'y = x', 'x = 4'], 'Vertical line through the midpoint (2, 0).'),
           ('If AB has gradient 3/4, what is the gradient of its perpendicular bisector?', '−4/3', ['3/4', '4/3', '−3/4'], 'Negative reciprocal.')],
    why=[('Explain why every point on the perpendicular bisector of AB is the same distance from A and from B.', 'For a point P on the bisector, triangles PMA and PMB (M the midpoint) are congruent (SAS: MA = MB, PM common, right angles), so PA = PB.'),
         ('Explain why perpendicular bisectors are the building blocks of Voronoi diagrams.', 'A Voronoi edge separates points nearer to one site from points nearer to another; the boundary of points equidistant from two sites is their perpendicular bisector.')],
    misc=[('The perpendicular bisector of AB passes through A.', 'It passes through the midpoint of AB, not through A or B.')],
))


@R.add('ch02-st1', ALL, (1, 5), 'short')
def perpbis_core(rng, slot):
    c, d = slot.c, slot.d
    P, Q = _sites(rng, 2, -6, 10)
    if (Q[0] - P[0]) % 2 or (Q[1] - P[1]) % 2:
        pass
    g, c0, mid = perp_bis(P, Q)
    eq = bis_text(P, Q)
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'Find the midpoint of the segment joining A{pt(P)} and B{pt(Q)}.', fpt(mid), [fpt((P[0] + Q[0], P[1] + Q[1])), fpt((Fr(Q[0] - P[0], 2), Fr(Q[1] - P[1], 2))), fpt((mid[1], mid[0])) if mid[0] != mid[1] else fpt((mid[0] + 1, mid[1]))],
                       'Average the coordinates.')
        return ret(f'Find the equation of the perpendicular bisector of the segment joining A{pt(P)} and B{pt(Q)}.', eq,
                   f'midpoint {fpt(mid)} (A1); gradient of AB = {Y1.frs(Fr(Q[1] - P[1], Q[0] - P[0])) if Q[0] != P[0] else "undefined"} (A1) so bisector gradient {Y1.frs(g) if g is not None else "0 (horizontal)" if False else (Y1.frs(g) if g is not None else "undefined (vertical)")} (M1); {eq} (A1).', 4)
    if c == 'C2':
        Xp = (mid[0] + (Q[1] - P[1]), mid[1] - (Q[0] - P[0]))
        dA = math.dist([float(v) for v in Xp], P)
        return ret(f'Show that the point X{fpt(Xp)} lies on the perpendicular bisector of A{pt(P)} and B{pt(Q)} and explain what this means.', f'XA = XB = {sf(dA)}',
                   f'XA = √(...) = {sf(dA)} (A1); XB = {sf(math.dist([float(v) for v in Xp], Q))} (A1); R1 equal distances, so X is equidistant from A and B and lies on the bisector.', 3, 'explain')
    if c == 'C3':
        towns = rng.sample(['Ashby', 'Brinton', 'Carlow', 'Dunmore', 'Elgin', 'Fenwick'], 2)
        return ret(f'Two mobile-phone masts are at {towns[0]} {pt(P)} and {towns[1]} {pt(Q)} (km). Phones connect to the nearer mast. Find the equation of the boundary between the two coverage regions, giving it in the form ax + by + d = 0.',
                   _gen_form(P, Q), f'midpoint {fpt(mid)} (A1); perpendicular gradient (M1 A1); {_gen_form(P, Q)} (A1).', 4, 'numerical')
    R3 = _sites(rng, 1, -6, 10)[0]
    if R3 in (P, Q):
        return None
    cc = circumcentre(P, Q, R3)
    if cc is None:
        return None
    rad = math.dist([float(v) for v in cc], P)
    return ret(f'Three schools are at A{pt(P)}, B{pt(Q)} and C{pt(R3)}. (a) Find the equations of the perpendicular bisectors of AB and BC. (b) Hence find the point equidistant from all three schools. (c) Find this common distance. (d) Explain why the perpendicular bisector of AC also passes through this point.',
               f'(a) {bis_text(P, Q)}; {bis_text(Q, R3)} (b) {fpt(cc)} (c) {sf(rad)}', f'(a) A1 A1 (M1 for method). (b) solve simultaneously (M1) ⇒ {fpt(cc)} (A1). (c) {sf(rad)} (A1). (d) R1 it is equidistant from A and C, so it lies on that bisector too.',
               7, 'multi_step', gap='G5')


def _gen_form(P, Q):
    # (Q - P)·(X - M) = 0  ->  2(qx-px)x + 2(qy-py)y - (qx²+qy² - px² - py²) = 0
    a, b = 2 * (Q[0] - P[0]), 2 * (Q[1] - P[1])
    dd = -(Q[0] ** 2 + Q[1] ** 2 - P[0] ** 2 - P[1] ** 2)
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(dd)) or 1
    a, b, dd = a // g, b // g, dd // g
    if a < 0 or (a == 0 and b < 0):
        a, b, dd = -a, -b, -dd
    out = lin3([a, b], ('x', 'y'))
    return f'{out} {sgn(dd)} = 0' if dd else f'{out} = 0'


R.facts('ch02-st2', F(
    terms=[('Voronoi diagram', 'a division of the plane into cells, one for each site, where every point of a cell is closer to its site than to any other site'),
           ('site', 'one of the given points around which the Voronoi cells are constructed'),
           ('Voronoi edge', 'a segment of a perpendicular bisector forming the boundary between two cells'),
           ('Voronoi vertex', 'a point where three or more cells meet; it is equidistant from the three nearest sites')],
    facts=[('A point P lies in the cell of site S in a Voronoi diagram. What can be said?', 'S is the nearest site to P', ['P is equidistant from all sites', 'S is the farthest site from P', 'P lies on an edge'], 'Definition of a cell.'),
           ('A Voronoi vertex is equidistant from at least how many sites?', '3', ['2', '1', '4'], 'Three cells meet at a vertex.')],
    why=[('Explain why Voronoi diagrams are useful for deciding which hospital serves which part of a city.', 'Each cell contains the points closest to one hospital, so (assuming straight-line distance) residents in a cell should go to that cell\'s hospital.'),
         ('Explain why some Voronoi cells are unbounded.', 'Sites on the outer boundary (convex hull) of the set have no sites beyond them, so their cells extend to infinity in that direction.')],
    misc=[('A Voronoi edge is the line segment joining two sites.', 'Edges are parts of the perpendicular bisectors between sites, not the segments joining them.')],
))


@R.add('ch02-st2', ALL, (1, 5), 'short')
def voronoi_core(rng, slot):
    c, d = slot.c, slot.d
    k = rng.randint(3, 5)
    S = _sites(rng, k, 0, 12)
    labels = 'ABCDE'[:k]
    kind = pick(rng, [('fire stations', 'emergency calls'), ('supermarkets', 'shoppers'), ('wells', 'villagers'), ('Wi-Fi routers', 'devices'), ('ambulance bases', 'patients')])
    sites = ', '.join(f'{labels[i]}{pt(S[i])}' for i in range(k))
    X = (rng.randint(0, 12), rng.randint(0, 12))
    ds = [math.dist(X, s) for s in S]
    near = labels[int(np.argmin(ds))]
    if sorted(ds)[0] == sorted(ds)[1]:
        return None
    if c == 'C1':
        return mcq(rng, f'The {kind[0]} in a town are at {sites} (km). In the Voronoi diagram of these sites, in which cell does the point {pt(X)} lie?', near, [l for l in labels if l != near][:3] if k > 3 else [l for l in labels if l != near] + ['on an edge'],
                   f'Nearest site: {near} (distance {sf(min(ds))}).')
    if c == 'C2':
        return ret(f'The {kind[0]} in a town are at {sites} (km). Explain how the Voronoi diagram can be used to decide which station should respond to {kind[1]} at {pt(X)}, and identify that station.', near,
                   f'R1 the point lies in the cell of the nearest site; R1 cells are bounded by perpendicular bisectors; A1 {near} (distance {sf(min(ds))} km).', 3, 'explain')
    i, j, l = 0, 1, 2
    cc = circumcentre(S[i], S[j], S[l])
    if cc is None:
        return None
    rad = math.dist([float(v) for v in cc], S[i])
    empty = all(math.dist([float(v) for v in cc], s) >= rad - 1e-9 for s in S)
    if c == 'C3':
        return ret(f'Sites A{pt(S[i])}, B{pt(S[j])} and C{pt(S[l])} are three of the {kind[0]} in a town. Find the coordinates of the point equidistant from A, B and C, and its distance from each site.', f'{fpt(cc)}; {sf(rad)}',
                   f'Perpendicular bisectors of two sides (M1 A1 A1); intersection {fpt(cc)} (A1); distance {sf(rad)} (A1).', 5, 'numerical')
    return ret(f'The {kind[0]} in a town are at {sites} (km). (a) Find the perpendicular bisector of A and B. (b) Find the point V equidistant from A, B and C. (c) Determine whether V is a vertex of the Voronoi diagram of all {k} sites, justifying your answer. '
               f'(d) State which site serves {kind[1]} at {pt(X)}.',
               f'(a) {bis_text(S[0], S[1])} (b) {fpt(cc)} (c) {"yes" if empty else "no"} (d) {near}',
               f'(a) A1 A1. (b) M1 A1. (c) R1 V is a vertex only if no other site is closer than {sf(rad)}: {"none is" if empty else "another site is closer"} (A1). (d) A1 {near}.', 8, 'multi_step', gap='G5')


R.facts('ch02-st3', F(
    terms=[('nearest-neighbour interpolation', 'estimating the value of a quantity at a point by using the value at the nearest site, i.e. the site of the Voronoi cell containing the point'),
           ('incremental algorithm', 'building a Voronoi diagram by adding one site at a time, drawing the new bisectors and removing edges that are no longer needed')],
    facts=[('When a new site is added to a Voronoi diagram, what happens to the neighbouring cells?', 'they shrink', ['they grow', 'they stay the same', 'they disappear completely'], 'Part of each neighbouring cell becomes closer to the new site.'),
           ('Rainfall is measured at weather stations. Nearest-neighbour interpolation estimates the rainfall at a farm as…', 'the rainfall at the station whose cell contains the farm', ['the mean of all stations', 'the maximum of all stations', 'zero'], 'Definition.')],
    why=[('Explain one limitation of nearest-neighbour interpolation.', 'The estimate jumps abruptly at cell boundaries and ignores all sites except the nearest, so it may be inaccurate when values vary smoothly over space.')],
    misc=[('Adding a new site to a Voronoi diagram changes every cell.', 'Only cells adjacent to the new site change; distant cells are unaffected.')],
))


@R.add('ch02-st3', ALL, (1, 5), 'short')
def addsite_core(rng, slot):
    c, d = slot.c, slot.d
    k = rng.randint(3, 5)
    S = _sites(rng, k, 0, 14)
    labels = 'ABCDE'[:k]
    vals = [round(rng.uniform(5, 60), 1) for _ in S]
    what = pick(rng, [('rainfall (mm)', 'weather stations'), ('air-quality index', 'monitoring stations'), ('soil pH × 10', 'sampling points'), ('temperature (°C)', 'sensors')])
    sites = ', '.join(f'{labels[i]}{pt(S[i])} with {vals[i]}' for i in range(k))
    X = (rng.randint(0, 14), rng.randint(0, 14))
    ds = [math.dist(X, s) for s in S]
    o = sorted(range(k), key=lambda i: ds[i])
    if abs(ds[o[0]] - ds[o[1]]) < 1e-9:
        return None
    if c == 'C1':
        return ret(f'{what[1][0].upper() + what[1][1:]} record {what[0]}: {sites}. Use nearest-neighbour interpolation to estimate the value at {pt(X)}.', _num(vals[o[0]]),
                   f'Nearest site {labels[o[0]]} (distance {sf(ds[o[0]])}) (M1); estimate {_num(vals[o[0]])} (A1).', 2)
    if c == 'C2':
        return ret(f'{what[1][0].upper() + what[1][1:]} record {what[0]}: {sites}. Explain why nearest-neighbour interpolation might give a poor estimate at {pt(X)}.', 'uses only the nearest site',
                   f'R1 the estimate uses only site {labels[o[0]]} although {labels[o[1]]} is almost as close ({sf(ds[o[0]])} vs {sf(ds[o[1]])}); R1 values change abruptly at cell edges.', 2, 'explain')
    N = (rng.randint(0, 14), rng.randint(0, 14))
    if N in S:
        return None
    dN = math.dist(X, N)
    newv = round(rng.uniform(5, 60), 1)
    nearN = [labels[i] for i in range(k) if True]
    if c == 'C3':
        return ret(f'Sites {", ".join(f"{labels[i]}{pt(S[i])}" for i in range(k))} form a Voronoi diagram. A new site N{pt(N)} is added. Find the equation of the perpendicular bisector of N and {labels[o[0]]}, which forms part of the boundary of the new cell.',
                   bis_text(N, S[o[0]]), f'midpoint (A1); gradient (M1 A1); {bis_text(N, S[o[0]])} (A1).', 4, 'numerical')
    before, after = vals[o[0]], (newv if dN < ds[o[0]] else vals[o[0]])
    return ret(f'{what[1][0].upper() + what[1][1:]} record {what[0]}: {sites}. (a) Estimate the value at P{pt(X)} by nearest-neighbour interpolation. (b) A new station N{pt(N)} recording {newv} is added. Find the perpendicular bisector of N and {labels[o[0]]}. '
               f'(c) Determine whether P now lies in the cell of N and state the new estimate. (d) Explain which cells of the diagram change when N is added.',
               f'(a) {_num(before)} (b) {bis_text(N, S[o[0]])} (c) {"yes" if dN < ds[o[0]] else "no"}; {_num(after)} (d) only cells adjacent to N',
               f'(a) A1. (b) M1 A1. (c) PN = {sf(dN)} vs P{labels[o[0]]} = {sf(ds[o[0]])} (M1); conclusion (R1) estimate {_num(after)} (A1). (d) R1 only neighbouring cells lose area to the new cell.', 8, 'multi_step', gap='G5')


R.facts('ch02-st4', F(
    terms=[('toxic waste dump problem', 'finding the point in a region that is as far as possible from every site, i.e. the centre of the largest empty circle'),
           ('largest empty circle', 'the largest circle with centre in the region that contains no site in its interior; its centre is at a Voronoi vertex or on the boundary of the region')],
    facts=[('Where can the solution to the toxic waste dump problem be found (inside a bounded region)?', 'at a Voronoi vertex or on the boundary of the region', ['at one of the sites', 'at the centroid of the sites', 'at the midpoint of two sites'], 'The distance to the nearest site is maximised there.')],
    why=[('Explain why the centre of the largest empty circle (inside the convex hull of the sites) lies at a Voronoi vertex.', 'Moving the centre along a Voronoi edge or within a cell increases the distance to at least one nearest site until three sites are equidistant – a Voronoi vertex – so the maximum occurs there.')],
    misc=[('The best place for a toxic waste dump is as far as possible from the centre of town.', 'The aim is to maximise the distance to the nearest site (town), which is found at Voronoi vertices, not just far from one point.')],
))


@R.add('ch02-st4', ALL, (1, 5), 'short')
def toxic_core(rng, slot):
    c, d = slot.c, slot.d
    k = 4
    S = _sites(rng, k, 0, 16)
    labels = 'ABCD'
    import itertools
    verts = []
    for tri in itertools.combinations(range(k), 3):
        cc = circumcentre(*[S[i] for i in tri])
        if cc is None:
            continue
        ccf = [float(v) for v in cc]
        rad = math.dist(ccf, S[tri[0]])
        if all(math.dist(ccf, S[i]) >= rad - 1e-9 for i in range(k)) and 0 <= ccf[0] <= 16 and 0 <= ccf[1] <= 16:
            verts.append((cc, rad, tri))
    if len(verts) < 2:
        return None
    verts.sort(key=lambda v: -v[1])
    best = verts[0]
    towns = ', '.join(f'{labels[i]}{pt(S[i])}' for i in range(k))
    vtxt = ', '.join(fpt(v[0]) for v in verts)
    if c == 'C1':
        return ret(f'Towns are at {towns} (km) inside the square 0 ≤ x, y ≤ 16. The Voronoi vertices inside the square are {vtxt}. Find the distance from {fpt(best[0])} to the nearest town.', f'{sf(best[1])} km',
                   f'Distance to {labels[best[2][0]]} = {sf(best[1])} (A1), equal for the three nearest towns (A1).', 2)
    if c == 'C2':
        return ret(f'Towns are at {towns} (km). Explain why a Voronoi vertex is a good candidate location for a waste facility that must be as far as possible from all towns.', 'maximises the distance to the nearest town locally',
                   'R1 at a vertex the three nearest towns are equidistant; R1 moving away from the vertex brings the site closer to one of them; R1 the boundary of the region must also be checked.', 3, 'explain')
    if c == 'C3':
        return ret(f'Towns are at {towns} (km). The Voronoi vertices inside the region 0 ≤ x, y ≤ 16 are {vtxt}. Find which vertex is farthest from its nearest town, and that distance.', f'{fpt(best[0])}; {sf(best[1])} km',
                   'Distance from each vertex to its three equidistant towns (M1): ' + '; '.join(f'{fpt(v[0])}: {sf(v[1])}' for v in verts) + f' (A2); largest {fpt(best[0])} (A1).', 4, 'numerical')
    return ret(f'A region 0 ≤ x, y ≤ 16 (km) contains towns at {towns}. (a) Find the coordinates of the Voronoi vertex equidistant from {", ".join(labels[i] for i in best[2])}. (b) Verify that no other town is closer to this point. '
               f'(c) The other Voronoi vertices are {", ".join(fpt(v[0]) for v in verts[1:])}. Determine the best location for a toxic waste dump among the Voronoi vertices. (d) Explain why the corners of the region should also be checked.',
               f'(a) {fpt(best[0])} (c) {fpt(best[0])}, {sf(best[1])} km from the nearest towns',
               f'(a) bisectors (M1 A1), vertex {fpt(best[0])} (A1). (b) distances to all towns (M1), remaining town farther (R1). (c) compare ' + '; '.join(f'{fpt(v[0])}: {sf(v[1])}' for v in verts) + ' (A1). (d) R1 the largest empty circle may have its centre on the boundary of the region.',
               8, 'multi_step', gap='G5')


# =============================================================================================
# ch03 Radians, trig identities and matrix transformations
# =============================================================================================
def pis(q):
    """Fraction q -> 'qπ' text, e.g. 5/6 -> 5π/6."""
    q = Fr(q).limit_denominator(1000)
    if q == 0:
        return '0'
    n, dd = q.numerator, q.denominator
    top = ('' if abs(n) == 1 else str(abs(n))) + 'π'
    s = top if dd == 1 else f'{top}/{dd}'
    return (MINUS if n < 0 else '') + s


R.facts('ch03-st1', F(
    terms=[('radian', 'the angle subtended at the centre of a circle by an arc equal in length to the radius; π radians = 180°'),
           ('arc length (radians)', 'l = rθ, where θ is the angle at the centre in radians'),
           ('area of a sector (radians)', 'A = ½r²θ, where θ is in radians'),
           ('area of a segment (radians)', 'A = ½r²(θ − sin θ), the sector minus the isosceles triangle')],
    facts=[('How many degrees is 1 radian, to 3 s.f.?', '57.3°', ['180°', '3.14°', '60.0°'], '180/π ≈ 57.3.'),
           ('Convert 135° to radians.', '3π/4', ['3π/2', '4π/3', '2π/3'], '135 × π/180 = 3π/4.'),
           ('A sector has radius 4 cm and angle 1.5 rad. What is its arc length?', '6 cm', ['12 cm', '3 cm', '2.67 cm'], 'l = rθ = 4 × 1.5.'),
           ('A sector has radius 6 cm and angle π/3. What is its area?', '6π cm²', ['12π cm²', '2π cm²', '3π cm²'], '½ × 36 × π/3 = 6π.')],
    why=[('Explain why arc length is l = rθ when θ is measured in radians.', 'A full turn of 2π radians has arc 2πr; the arc is proportional to the angle, so an angle θ gives (θ/2π) × 2πr = rθ.'),
         ('Explain why calculators must be in radian mode when using l = rθ.', 'The formula only holds when θ is in radians; in degree mode trigonometric values and conversions are wrong (e.g. sin θ in the segment formula).')],
    misc=[('The area of a sector of radius 5 cm and angle 40° is ½ × 5² × 40 = 500 cm².', 'The formula ½r²θ needs θ in radians: 40° = 0.698 rad, so the area is ½ × 25 × 0.698 = 8.73 cm².')],
))


@R.add('ch03-st1', ALL, (1, 5), 'short')
def radian_core(rng, slot):
    c, d = slot.c, slot.d
    r = round(rng.uniform(2, 30), 1)
    if c == 'C1':
        if rng.random() < 0.5:
            q = Fr(rng.choice([1, 2, 3, 4, 5, 7, 11, 13]), rng.choice([2, 3, 4, 6, 12, 9, 10]))
            if q >= 2:
                q -= 1
            dg = float(q) * 180
            return nmcq(rng, f'Convert {pis(q)} radians to degrees.', dg, [float(q) * 360, float(q) * 90, float(q) * 57.3 * math.pi], f'{pis(q)} × 180/π = {sf(dg)}°.', fmtf=lambda z: sf(z) + '°')
        th = round(rng.uniform(0.3, 5.5), 2)
        return ret(f'A sector has radius {r} cm and angle {th} radians. Find its arc length and area.', f'{sf(r * th)} cm; {sf(0.5 * r * r * th)} cm²', f'l = rθ = {r} × {th} (M1) = {sf(r * th)} cm (A1); A = ½ × {r}² × {th} = {sf(0.5 * r * r * th)} cm² (A1).', 3)
    if c == 'C2':
        dg = rng.choice([40, 50, 72, 100, 110, 135, 150, 200, 225, 250])
        th = math.radians(dg)
        wrong = 0.5 * r * r * dg
        return ret(f'{name(rng)} finds the area of a sector of radius {r} cm and angle {dg}° as ½ × {r}² × {dg} = {sf(wrong)} cm². Explain the error and find the correct area.', f'{sf(0.5 * r * r * th)} cm²',
                   f'R1 the formula ½r²θ requires θ in radians; M1 {dg}° = {sf(th)} rad; A1 ½ × {r}² × {sf(th)} = {sf(0.5 * r * r * th)} cm².', 3, 'explain')
    th = round(rng.uniform(0.4, 2.8), 2)
    seg = 0.5 * r * r * (th - math.sin(th))
    if c == 'C3':
        if rng.random() < 0.5:
            A = round(0.5 * r * r * th, 1)
            th2 = 2 * A / (r * r)
            return ret(f'A lawn sprinkler waters a sector of radius {r} m with area {A} m². Find the angle of the sector in radians and the length of the arc watered.', f'{sf(th2)} rad; {sf(r * th2)} m',
                       f'½ × {r}² × θ = {A} (M1) ⇒ θ = {sf(th2)} (A1); l = {r} × {sf(th2)} = {sf(r * th2)} m (A1).', 3, 'numerical')
        return ret(f'A circular table top of radius {r} cm has a segment cut off by a straight chord that subtends {th} radians at the centre. Find the area of the segment removed and the length of the chord.', f'{sf(seg)} cm²; {sf(2 * r * math.sin(th / 2))} cm',
                   f'½r²(θ − sin θ) (M1) = ½ × {r}² × ({th} − sin {th}) (A1) = {sf(seg)} cm² (A1); chord 2r sin(θ/2) = {sf(2 * r * math.sin(th / 2))} cm (A1).', 4, 'numerical')
    if rng.random() < 0.5:
        rpm = rng.randint(5, 60)
        R_ = round(rng.uniform(0.2, 1.5), 2)
        t = rng.randint(2, 20)
        ang = rpm * 2 * math.pi * t / 60
        return ret(f'A wheel of radius {R_} m turns at {rpm} revolutions per minute. (a) Find its angular speed in radians per second. (b) Find the angle turned in {t} seconds. (c) Find the distance travelled by a point on the rim in this time. (d) Explain why using degrees would make part (c) harder.',
                   f'(a) {sf(rpm * 2 * math.pi / 60)} rad s⁻¹ (b) {sf(ang)} rad (c) {sf(R_ * ang)} m', f'(a) {rpm} × 2π/60 (M1) = {sf(rpm * 2 * math.pi / 60)} (A1). (b) × {t} = {sf(ang)} rad (A1). (c) l = rθ (M1) = {sf(R_ * ang)} m (A1). (d) R1 l = rθ holds only in radians; degrees need the factor π/180.', 6, 'multi_step', gap='G5')
    return ret(f'A pendulum of length {r} cm swings through an angle of {th} radians. (a) Find the arc length of one swing. (b) Find the straight-line distance between the extreme positions of the bob. (c) Find the area swept out by the string. (d) Find the area between the arc and the straight line in (b).',
               f'(a) {sf(r * th)} cm (b) {sf(2 * r * math.sin(th / 2))} cm (c) {sf(0.5 * r * r * th)} cm² (d) {sf(seg)} cm²',
               f'(a) rθ (M1) {sf(r * th)} (A1). (b) 2r sin(θ/2) or cosine rule (M1) {sf(2 * r * math.sin(th / 2))} (A1). (c) ½r²θ = {sf(0.5 * r * r * th)} (A1). (d) ½r²(θ − sin θ) (M1) = {sf(seg)} (A1).', 7, 'multi_step', gap='G5')


def _trig_sol(fn, k, lo, hi):
    """solutions of fn(u) = k for u in [lo, hi] (radians), fn in sin/cos."""
    if abs(k) > 1:
        return []
    out = []
    if fn == 'sin':
        base = [math.asin(k), math.pi - math.asin(k)]
    else:
        base = [math.acos(k), -math.acos(k)]
    for b in base:
        n0 = math.floor((lo - b) / (2 * math.pi)) - 1
        for n in range(n0, n0 + int((hi - lo) / (2 * math.pi)) + 4):
            u = b + 2 * math.pi * n
            if lo - 1e-9 <= u <= hi + 1e-9 and all(abs(u - v) > 1e-7 for v in out):
                out.append(u)
    return sorted(out)


R.facts('ch03-st2', F(
    terms=[('unit circle', 'the circle x² + y² = 1; a point at angle θ from the positive x-axis has coordinates (cos θ, sin θ)'),
           ('Pythagorean identity', 'sin²θ + cos²θ = 1 for every angle θ'),
           ('tan identity', 'tan θ = sin θ / cos θ (cos θ ≠ 0)'),
           ('principal value', 'the single value returned by the inverse function on a calculator, e.g. sin⁻¹ gives an angle in [−π/2, π/2]')],
    facts=[('If θ is obtuse and sin θ = 3/5, what is cos θ?', '−4/5', ['4/5', '3/4', '−3/4'], 'cos²θ = 1 − 9/25; cosine is negative in the second quadrant.'),
           ('How many solutions does sin x = 0.4 have for 0 ≤ x ≤ 2π?', '2', ['1', '3', '4'], 'One in each of the first and second quadrants.'),
           ('What is the exact value of cos(2π/3)?', '−1/2', ['1/2', '√3/2', '−√3/2'], 'Second quadrant, reference angle π/3.'),
           ('Which is equivalent to 1 − cos²θ?', 'sin²θ', ['tan²θ', 'cos²θ − 1', '1'], 'Rearrange sin²θ + cos²θ = 1.')],
    why=[('Explain why sin(π − θ) = sin θ using the unit circle.', 'The points at angles θ and π − θ are reflections of each other in the y-axis, so they have the same y-coordinate, which is the sine.'),
         ('Explain why a calculator gives only one solution to sin x = k, and how to find the others.', 'sin⁻¹ returns only the principal value; further solutions come from symmetry (π − x) and the period 2π, added until the interval is covered.')],
    misc=[('sin²θ + cos²θ = 1 only for acute angles.', 'The identity holds for all θ, because (cos θ, sin θ) always lies on the unit circle x² + y² = 1.'),
          ('If 2 sin x = 1 then sin x = 1/2 so x = 30° is the only answer.', 'In 0 ≤ x ≤ 360° there is a second solution x = 150°, since sin(180° − x) = sin x.')],
))


@R.add('ch03-st2', ALL, (1, 5), 'short')
def trigeq_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        if rng.random() < 0.5:
            p, h = rng.choice([(3, 5), (5, 13), (8, 17), (7, 25), (20, 29), (12, 13), (4, 5)])
            adj = int(round(math.sqrt(h * h - p * p)))
            quad = rng.choice(['acute', 'obtuse'])
            cv = Fr(adj, h) * (1 if quad == 'acute' else -1)
            return mcq(rng, f'Given that θ is {quad} and sin θ = {p}/{h}, find the exact value of cos θ.', frs(cv), [frs(-cv), frs(Fr(p, adj)), frs(Fr(h, adj) * (1 if quad == 'acute' else -1))],
                       f'cos²θ = 1 − ({p}/{h})² = {adj * adj}/{h * h}; θ {quad} ⇒ cos θ = {frs(cv)}.')
        k = round(rng.uniform(-0.95, 0.95), 2)
        if abs(k) < 0.05:
            k = 0.35
        fn = rng.choice(['sin', 'cos'])
        sols = _trig_sol(fn, k, 0, 2 * math.pi)
        return ret(f'Solve {fn} x = {m(k)} for 0 ≤ x ≤ 2π.', 'x = ' + ', '.join(sf(s) for s in sols),
                   f'{fn}⁻¹({m(k)}) = {sf(math.asin(k) if fn == "sin" else math.acos(k))} (M1); ' + ', '.join(sf(s) for s in sols) + ' (A1 A1).', 3)
    if c == 'C2':
        k = round(rng.uniform(0.1, 0.9), 2)
        n = rng.choice([2, 3])
        sols = _trig_sol('sin', k, 0, n * 2 * math.pi / 1)
        sols2 = [s / n for s in _trig_sol('sin', k, 0, n * 2 * math.pi)]
        return ret(f'Explain why the equation sin({n}x) = {k} has {len(sols2)} solutions for 0 ≤ x ≤ 2π, and find the smallest two.', f'{len(sols2)} solutions; {sf(sols2[0])}, {sf(sols2[1])}',
                   f'R1 the period of sin({n}x) is 2π/{n}, so there are {n} cycles in [0, 2π]; R1 each full cycle gives 2 solutions; A1 {n}x = {sf(math.asin(k))}, {sf(math.pi - math.asin(k))} ⇒ x = {sf(sols2[0])}, {sf(sols2[1])}.', 4, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            a, b = rng.randint(2, 5), rng.randint(-3, 3)
            k = rng.randint(b - a + 1, b + a - 1)
            if k == b:
                k += 1
            kv = (k - b) / a
            if abs(kv) >= 1:
                return None
            fn = rng.choice(['sin', 'cos'])
            sols = [math.degrees(s) for s in _trig_sol(fn, kv, 0, 2 * math.pi)]
            return ret(f'Solve {a} {fn} θ {sgn(b)} = {k} for 0° ≤ θ ≤ 360°.' if b else f'Solve {a} {fn} θ = {k} for 0° ≤ θ ≤ 360°.', 'θ = ' + ', '.join(sf(s) + '°' for s in sols),
                       f'{fn} θ = {frs(Fr(k - b, a))} (M1); principal value {sf(math.degrees(math.asin(kv) if fn == "sin" else math.acos(kv)))}° (A1); ' + ', '.join(sf(s) + '°' for s in sols) + ' (A1 A1).', 4, 'numerical')
        # quadratic in sin
        r1, r2 = rng.choice([(Fr(1, 2), -1), (Fr(1, 2), 1), (Fr(-1, 2), 1), (Fr(1, 3), -1), (Fr(2, 3), -1), (Fr(1, 4), Fr(-1, 2)), (Fr(3, 4), -1)])
        A2 = r1.denominator * (r2.denominator if isinstance(r2, Fr) else 1)
        # A(s - r1)(s - r2) with integer coefficients
        aa = A2
        bb = -aa * (r1 + r2)
        cc = aa * r1 * r2
        g = math.gcd(math.gcd(int(aa), abs(int(bb))), abs(int(cc))) or 1
        aa, bb, cc = int(aa) // g, int(bb) // g, int(cc) // g
        fn = rng.choice(['sin', 'cos'])
        sols = sorted(set(round(math.degrees(s), 6) for r_ in (r1, r2) for s in _trig_sol(fn, float(r_), 0, 2 * math.pi)))
        eqn = f'{"" if aa == 1 else aa}{fn}²x {sgn(bb)}{fn} x {sgn(cc)} = 0'.replace(f'{sgn(bb)}{fn}', f'{sgn(bb)} {fn}').replace('+ 1 ' + fn, '+ ' + fn).replace('− 1 ' + fn, '− ' + fn)
        return ret(f'Solve {eqn} for 0° ≤ x ≤ 360°.', 'x = ' + ', '.join(sf(s) + '°' for s in sols),
                   f'Factorise: ({fn} x {sgn(-r1, fmtf=frs) if False else ("− " + frs(r1) if r1 > 0 else "+ " + frs(-r1))})({fn} x {("− " + frs(r2) if r2 > 0 else "+ " + frs(-r2))}) = 0 (M1); {fn} x = {frs(r1)} or {frs(r2)} (A1); ' + ', '.join(sf(s) + '°' for s in sols) + ' (A1 A1).', 4, 'numerical')
    # C4 tide model
    A_ = round(rng.uniform(1.2, 4.5), 1)
    D = round(rng.uniform(A_ + 0.5, A_ + 6), 1)
    per = rng.choice([12, 12.4, 24])
    b = sfv(2 * math.pi / per)
    lvl = round(rng.uniform(D - 0.8 * A_, D + 0.8 * A_), 1)
    kv = (lvl - D) / A_
    sols = [s / b for s in _trig_sol('sin', kv, 0, b * 24)]
    if len(sols) < 2:
        return None
    t1, t2 = sols[0], sols[1]
    place = pick(rng, ['a harbour in Brittany', 'a port in Nova Scotia', 'a jetty in Queensland', 'a quay in Cornwall', 'a pier in Busan'])
    return ret(f'The depth of water at {place} is modelled by h(t) = {A_} sin({sf(b)}t) + {D}, where h is in metres and t is the time in hours after midnight. (a) Find the maximum and minimum depths. (b) Show that the period is about {_num(per)} hours. '
               f'(c) Find the first two times after midnight when the depth is {lvl} m. (d) A boat needs at least {lvl} m of water; {"find the length of time per cycle it can enter" if kv < 0 else "find the length of time in the first cycle it can enter"}.',
               f'(a) {sf(D + A_)} m, {sf(D - A_)} m (c) t = {sf(t1)}, {sf(t2)} h (d) {sf((t2 - t1) if kv >= 0 else 2 * math.pi / b - (t2 - t1))} h',
               f'(a) D ± A (A1 A1). (b) 2π/{sf(b)} = {sf(2 * math.pi / b)} (AG). (c) sin({sf(b)}t) = {sf(kv)} (M1) ⇒ {sf(t1)}, {sf(t2)} (A1 A1). (d) depth ≥ {lvl} between consecutive solutions (R1) ⇒ {sf((t2 - t1) if kv >= 0 else 2 * math.pi / b - (t2 - t1))} h (A1).', 8, 'multi_step', gap='G5')


def _tf_matrices(rng):
    """(description, 2x2 matrix) of a random standard transformation."""
    kind = rng.choice(['rot', 'ref', 'enl', 'str'])
    if kind == 'rot':
        a = rng.choice([90, 180, 270, 30, 45, 60, 120, 135, 150, 210, 300])
        t = math.radians(a)
        M = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
        return f'an anticlockwise rotation of {a}° about the origin', M, kind, a
    if kind == 'ref':
        a = rng.choice([0, 90, 45, 135, 30, 60])
        t = math.radians(a)
        M = np.array([[math.cos(2 * t), math.sin(2 * t)], [math.sin(2 * t), -math.cos(2 * t)]])
        line = {0: 'the x-axis', 90: 'the y-axis', 45: 'the line y = x', 135: 'the line y = −x'}.get(a, f'the line y = (tan {a}°)x')
        return f'a reflection in {line}', M, kind, a
    if kind == 'enl':
        k = rng.choice([2, 3, 0.5, -2, 1.5, 4])
        return f'an enlargement with scale factor {m(_num(k))}, centre the origin', np.array([[k, 0], [0, k]]), kind, k
    k = rng.choice([2, 3, 0.5, 1.5, 4])
    ax = rng.choice(['x', 'y'])
    M = np.array([[k, 0], [0, 1]]) if ax == 'x' else np.array([[1, 0], [0, k]])
    inv = 'y-axis' if ax == 'x' else 'x-axis'
    return f'a horizontal stretch with scale factor {_num(k)}, {inv} invariant' if ax == 'x' else f'a vertical stretch with scale factor {_num(k)}, {inv} invariant', M, kind, k


def _clean(M):
    M = np.array(M, dtype=float)
    M[np.abs(M) < 1e-12] = 0.0
    return M


def cross2(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


def _pts(P):
    return ', '.join(pt(p) for p in P)


R.facts('ch03-st3', F(
    terms=[('rotation matrix', '[cos θ, −sin θ; sin θ, cos θ], an anticlockwise rotation of θ about the origin'),
           ('reflection matrix', '[cos 2θ, sin 2θ; sin 2θ, −cos 2θ], a reflection in the line y = (tan θ)x'),
           ('stretch matrix', '[k, 0; 0, 1] (horizontal, y-axis invariant) or [1, 0; 0, k] (vertical, x-axis invariant)'),
           ('enlargement matrix', '[k, 0; 0, k], an enlargement with scale factor k centred on the origin'),
           ('invariant point', 'a point that is mapped onto itself by a transformation')],
    facts=[('Which matrix represents a reflection in the y-axis?', '[−1, 0; 0, 1]', ['[1, 0; 0, −1]', '[0, 1; 1, 0]', '[−1, 0; 0, −1]'], 'x changes sign, y unchanged.'),
           ('Which matrix represents a rotation of 90° anticlockwise about the origin?', '[0, −1; 1, 0]', ['[0, 1; −1, 0]', '[1, 0; 0, −1]', '[−1, 0; 0, −1]'], 'cos 90° = 0, sin 90° = 1.'),
           ('The columns of a transformation matrix are…', 'the images of (1, 0) and (0, 1)', ['the images of (1, 1) and (0, 0)', 'the eigenvalues', 'the invariant points'], 'M(1, 0) is the first column, M(0, 1) the second.'),
           ('Which matrix represents a rotation of 180° about the origin?', '[−1, 0; 0, −1]', ['[1, 0; 0, 1]', '[0, −1; −1, 0]', '[−1, 0; 0, 1]'], 'cos 180° = −1, sin 180° = 0.')],
    why=[('Explain why the columns of a 2 × 2 transformation matrix are the images of the unit vectors i and j.', 'M(1, 0)ᵀ picks out the first column and M(0, 1)ᵀ the second, so the matrix is fixed by where the unit vectors go.'),
         ('Explain why the origin is always an invariant point of a matrix transformation.', 'M times the zero vector is the zero vector for any matrix, so (0, 0) maps to itself.')],
    misc=[('A stretch [3, 0; 0, 1] triples every length in the plane.', 'It only scales distances in the x-direction by 3; vertical lengths are unchanged.')],
))


@R.add('ch03-st3', ALL, (1, 5), 'short')
def transf_core(rng, slot):
    c, d = slot.c, slot.d
    desc, M, kind, par = _tf_matrices(rng)
    M = _clean(M)
    P = [np.array([rng.randint(-4, 6), rng.randint(-4, 6)]) for _ in range(3)]
    if len({tuple(p) for p in P}) < 3 or abs(cross2(P[1] - P[0], P[2] - P[0])) < 1e-9:
        return None
    img = [M @ p for p in P]
    if c == 'C1':
        if d <= 2:
            wrongs = [mat(_clean(M.T)), mat(_clean(-M)), mat(_clean(np.array([[M[1, 1], M[0, 1]], [M[1, 0], M[0, 0]]])))]
            if len({mat(M), *wrongs}) < 4:
                wrongs = [mat(_clean(M.T + 0)), mat(_clean(2 * M)), mat(_clean(M @ np.array([[0, 1], [1, 0]])))]
            if len({mat(M), *wrongs}) < 4:
                return None
            return mcq(rng, f'Which matrix represents {desc}?', mat(M), wrongs, f'Images of (1, 0) and (0, 1) form the columns: {mat(M)}.')
        return ret(f'Find the image of the point {pt(P[0])} under {desc}.', pt(img[0]), f'M = {mat(M)} (A1); M{pt(P[0])} = {pt(img[0])} (M1 A1).', 3)
    if c == 'C2':
        dt = float(np.linalg.det(M))
        return ret(f'The matrix {mat(M)} represents {desc}. Explain the geometric meaning of its determinant and state what happens to the area and orientation of a shape.', f'det = {m(_num(dt))}',
                   f'A1 det = {m(_num(dt))}; R1 |det| = {_num(abs(dt))} is the area scale factor; R1 {"negative: orientation reversed" if dt < 0 else "positive: orientation preserved"}.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            area = 0.5 * abs(cross2(P[1] - P[0], P[2] - P[0]))
            return ret(f'Triangle T has vertices {_pts(P)}. It is transformed by {desc}. Write down the matrix of the transformation, find the vertices of the image and its area.', f'{_pts(img)}; area {_num(area * abs(np.linalg.det(M)))}',
                       f'M = {mat(M)} (A1); images {_pts(img)} (M1 A1); area of T = {_num(area)} (A1), × |det M| = {_num(abs(np.linalg.det(M)))} ⇒ {_num(area * abs(np.linalg.det(M)))} (A1).', 5, 'numerical')
        A_ = np.array([[rng.randint(-3, 4) for _ in range(2)] for _ in range(2)])
        if abs(np.linalg.det(A_)) < 0.5:
            return None
        u, v = np.array([1, rng.randint(-2, 3)]), np.array([rng.randint(-2, 3), 1])
        if abs(cross2(u, v)) < 0.5:
            return None
        return ret(f'A transformation with matrix [a, b; c, d] maps {pt(u)} to {pt(A_ @ u)} and {pt(v)} to {pt(A_ @ v)}. Find the matrix.', mat(A_),
                   f'M{mat(np.array([[u[0], v[0]], [u[1], v[1]]]))} = {mat(np.array([[(A_ @ u)[0], (A_ @ v)[0]], [(A_ @ u)[1], (A_ @ v)[1]]]))} (M1); M = image matrix × inverse (M1); {mat(A_)} (A1 A1).', 4, 'numerical')
    area = 0.5 * abs(cross2(P[1] - P[0], P[2] - P[0]))
    inv = None
    if abs(np.linalg.det(M)) > 1e-9:
        inv = _clean(np.linalg.inv(M))
    return ret(f'A logo designer works with the triangle with vertices {_pts(P)}. (a) Write down the matrix M representing {desc}. (b) Find the images of the vertices under M. (c) Find the area of the image triangle. (d) State the matrix that maps the image back to the original.',
               f'(a) {mat(M)} (b) {_pts(img)} (c) {_num(area * abs(np.linalg.det(M)))} (d) {mat(inv)}',
               f'(a) A1. (b) M1 A1 A1. (c) original area {_num(area)} (M1) × |det M| (A1). (d) M⁻¹ = {mat(inv)} (A1).', 7, 'multi_step', gap='G5')


R.facts('ch03-st4', F(
    terms=[('composite transformation', 'the result of applying one transformation followed by another; "A then B" has matrix BA'),
           ('area scale factor', '|det M|: the factor by which a matrix transformation multiplies every area'),
           ('inverse transformation', 'the transformation with matrix M⁻¹ that undoes M; it exists only if det M ≠ 0')],
    facts=[('Transformation A is followed by transformation B. Which matrix represents the combined transformation?', 'BA', ['AB', 'A + B', 'A⁻¹B'], 'The first transformation is applied to the vector first, so it sits next to the vector.'),
           ('A shape of area 12 cm² is transformed by M with det M = −3. What is the area of the image?', '36 cm²', ['−36 cm²', '4 cm²', '12 cm²'], 'Area × |det M|.'),
           ('What is det M for any rotation matrix?', '1', ['0', '−1', 'cos θ'], 'cos²θ + sin²θ = 1.'),
           ('What is det M for any reflection matrix?', '−1', ['1', '0', '2'], '−cos²2θ − sin²2θ = −1.')],
    why=[('Explain why the matrix for "M followed by N" is NM and not MN.', 'The image of a vector x under M is Mx; applying N gives N(Mx) = (NM)x, so the matrix acting first is written on the right.'),
         ('Explain why a transformation with determinant 0 has no inverse.', 'It maps the plane onto a line or point, squashing area to zero; different points share images, so the original cannot be recovered.')],
    misc=[('Since det(AB) = det(BA), the composite AB is the same transformation as BA.', 'Equal determinants only mean equal area scale factors; in general AB ≠ BA, e.g. reflect-then-rotate differs from rotate-then-reflect.')],
))


@R.add('ch03-st4', ALL, (1, 5), 'short')
def compose_core(rng, slot):
    c, d = slot.c, slot.d
    d1, M1, k1, _ = _tf_matrices(rng)
    d2, M2, k2, _ = _tf_matrices(rng)
    if d1 == d2:
        return None
    M1, M2 = _clean(M1), _clean(M2)
    C = _clean(M2 @ M1)
    dt = float(np.linalg.det(C))
    if c == 'C1':
        A_ = round(rng.uniform(2, 40), 1)
        return nmcq(rng, f'A shape of area {A_} cm² is transformed by {d1}, followed by {d2}. Find the area of the image.', A_ * abs(dt), [A_ * abs(np.linalg.det(M1)), A_ * abs(np.linalg.det(M2)), A_ * (abs(np.linalg.det(M1)) + abs(np.linalg.det(M2)))],
                    f'|det| of each: {_num(abs(np.linalg.det(M1)))} and {_num(abs(np.linalg.det(M2)))}; product {_num(abs(dt))}; area {sf(A_ * abs(dt))} cm².', fmtf=lambda z: sf(z) + ' cm²')
    if c == 'C2':
        CR = _clean(M1 @ M2)
        same = np.allclose(C, CR)
        if same and rng.random() < 0.75:
            return None
        return ret(f'Let A = {mat(M1)} ({d1}) and B = {mat(M2)} ({d2}). Explain which product represents "A followed by B" and whether the order matters here.', f'BA = {mat(C)}; ' + ('order does not matter here' if same else f'AB = {mat(CR)} differs'),
                   f'R1 the first transformation acts on the vector first: B(Ax) = (BA)x; A1 BA = {mat(C)}; R1 ' + ('AB happens to be equal (the transformations commute)' if same else f'AB = {mat(CR)} ≠ BA, so order matters') + '.', 4, 'explain')
    if c == 'C3':
        P = np.array([rng.randint(-5, 6), rng.randint(-5, 6)])
        if not P.any():
            return None
        return ret(f'The point P{pt(P)} is transformed by {d1}, followed by {d2}. Find the single matrix representing the combined transformation and the image of P.', f'{mat(C)}; {pt(C @ P)}',
                   f'{mat(M1)} (A1), {mat(M2)} (A1); combined = {mat(M2)}{mat(M1)} (M1) = {mat(C)} (A1); image {pt(C @ P)} (A1).', 5, 'numerical')
    P = [np.array([0, 0]), np.array([rng.randint(2, 6), 0]), np.array([rng.randint(0, 5), rng.randint(2, 6)])]
    area = 0.5 * abs(cross2(P[1] - P[0], P[2] - P[0]))
    inv = _clean(np.linalg.inv(C)) if abs(dt) > 1e-9 else None
    if inv is None:
        return None
    return ret(f'A computer game moves a sprite, the triangle with vertices {_pts(P)}, by {d1}, followed by {d2}. (a) Write down both matrices. (b) Find the matrix T of the combined transformation. (c) Find the vertices of the image and its area. '
               f'(d) Find T⁻¹ and explain what it represents. (e) State whether the sprite\'s orientation is reversed.',
               f'(b) {mat(C)} (c) {_pts([C @ p for p in P])}; {_num(area * abs(dt))} (d) {mat(inv)} (e) {"yes" if dt < 0 else "no"}',
               f'(a) A1 A1. (b) second × first (M1) {mat(C)} (A1). (c) A1; area {_num(area)} × |{m(_num(dt))}| (M1 A1). (d) A1 inverse; R1 undoes the combined move. (e) R1 det {m(_num(dt))} {"< 0" if dt < 0 else "> 0"}.', 10, 'multi_step', gap='G5')


# =============================================================================================
# ch04 Vectors and vector kinematics
# =============================================================================================
def ijk(v):
    names = ['i', 'j', 'k'][:len(v)]
    out = []
    for cf, nm in zip(v, names):
        cf = float(cf)
        if abs(cf) < 1e-12:
            continue
        mag = '' if abs(abs(cf) - 1) < 1e-12 else _num(abs(cf))
        if not out:
            out.append((MINUS if cf < 0 else '') + mag + nm)
        else:
            out.append(('− ' if cf < 0 else '+ ') + mag + nm)
    return ' '.join(out) or '0'


def rvec(rng, n=3, lo=-6, hi=7, nz=True):
    while True:
        v = np.array([rng.randint(lo, hi) for _ in range(n)])
        if not nz or v.any():
            return v


def ang(u, v):
    cs = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))
    return deg(math.acos(max(-1, min(1, cs))))


def surd(n):
    """√n simplified text for integer n"""
    n = int(n)
    a, b = 1, n
    for k in range(int(math.isqrt(n)), 1, -1):
        if n % (k * k) == 0:
            a, b = k, n // (k * k)
            break
    if b == 1:
        return str(a)
    return (str(a) if a > 1 else '') + f'√{b}'


R.facts('ch04-st1', F(
    terms=[('vector', 'a quantity with both magnitude and direction, e.g. displacement, velocity or force'),
           ('position vector', 'the vector OA from the origin to the point A'),
           ('unit vector', 'a vector of magnitude 1; the unit vector in the direction of v is v/|v|'),
           ('magnitude of a vector', '|v| = √(v₁² + v₂² + v₃²), the length of the vector'),
           ('parallel vectors', 'vectors that are scalar multiples of each other, u = kv')],
    facts=[('A is (1, 2, 3) and B is (4, 6, 3). What is |AB|?', '5', ['7', '√74', '25'], 'AB = (3, 4, 0), |AB| = √(9 + 16).'),
           ('Which vector is parallel to 2i − j + 3k?', '−4i + 2j − 6k', ['2i + j + 3k', '4i − 2j + 3k', 'i − 2j + 3k'], 'It is −2 times the vector.'),
           ('What is the unit vector in the direction of 3i + 4j?', '0.6i + 0.8j', ['3i + 4j', '0.75i + j', '(3i + 4j)/7'], 'Divide by the magnitude 5.'),
           ('If OA = a and OB = b, then AB = …', 'b − a', ['a − b', 'a + b', '½(a + b)'], 'AB = AO + OB = −a + b.')],
    why=[('Explain why AB = b − a, where a and b are the position vectors of A and B.', 'To go from A to B you can travel A → O → B: AO = −a then OB = b, so AB = −a + b = b − a.'),
         ('Explain why dividing a vector by its magnitude gives a unit vector in the same direction.', 'Dividing by the positive scalar |v| scales every component equally, so the direction is unchanged and the new magnitude is |v|/|v| = 1.')],
    misc=[('The magnitude of 3i − 4j is 3 − 4 = −1.', 'Magnitude is √(3² + (−4)²) = 5; it is never negative.')],
))


@R.add('ch04-st1', ALL, (1, 5), 'short')
def vecbasic_core(rng, slot):
    c, d = slot.c, slot.d
    A, B = rvec(rng, 3, -5, 8), rvec(rng, 3, -5, 8)
    AB = B - A
    if not AB.any():
        return None
    L = float(np.linalg.norm(AB))
    sq = int(AB @ AB)
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'Find the magnitude of the vector {ijk(AB)}.', L, [abs(AB).sum(), sq, abs(AB.sum())], f'√({" + ".join(f"({m(_num(x))})²" for x in AB)}) = √{sq} = {sf(L)}.')
        return ret(f'A is the point {pt(A)} and B is {pt(B)}. Find the vector AB and its magnitude.', (f'AB = {ijk(AB)}; |AB| = {_num(L)}' if L.is_integer() else f'AB = {ijk(AB)}; |AB| = {surd(sq)} ({sf(L)})'),
                   f'AB = b − a = {ijk(AB)} (M1 A1); |AB| = √{sq} = {sf(L)} (A1).', 3)
    if c == 'C2':
        k = rng.choice([2, 3, -2, Fr(1, 2), -3])
        u = rvec(rng, 3, -4, 5)
        v = u * float(k)
        w = v + np.array([0, 0, rng.choice([1, -1, 2])])
        par = rng.random() < 0.5
        vv = v if par else w
        return ret(f'Determine whether the vectors p = {ijk(u)} and q = {ijk(vv)} are parallel, explaining your reasoning.', 'parallel' if par else 'not parallel',
                   (f'R1 q = ({frs(k)})p (each component multiplied by {frs(k)}); A1 so they are parallel' + (' (opposite directions)' if k < 0 else '') + '.') if par else
                   f'R1 the ratios of components are not all equal (' + ', '.join(frs(Fr(int(round(b_ * 2)), 2) / a_) if a_ else 'undefined' for a_, b_ in zip(u, vv)) + '); A1 not parallel.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            spd = rng.randint(5, 40)
            uv = AB / L
            vel = uv * spd
            return ret(f'A drone flies from A{pt(A)} towards B{pt(B)} (units: metres) at a constant speed of {spd} m s⁻¹. Find the unit vector in the direction AB and the velocity vector of the drone.', f'{vec(np.round(uv, 6))}; {vec(vel)}',
                       f'AB = {ijk(AB)} (A1); |AB| = {sf(L)} (A1); unit vector AB/|AB| (M1) = ({", ".join(sf(x) for x in uv)}) (A1); velocity {spd} × unit vector = ({", ".join(sf(x) for x in vel)}) m s⁻¹ (A1).', 5, 'numerical')
        C = rvec(rng, 3, -5, 8)
        D = A + C - B
        return ret(f'ABCD is a parallelogram with A{pt(A)}, B{pt(B)} and C{pt(C)}. Find the coordinates of D and the length of the diagonal AC.', f'D{pt(D)}; AC = {sf(np.linalg.norm(C - A))}',
                   f'AD = BC (R1) = {ijk(C - B)} (A1); d = a + BC = {pt(D)} (A1); AC = {ijk(C - A)}, |AC| = {sf(np.linalg.norm(C - A))} (M1 A1).', 5, 'numerical')
    F1, F2 = rvec(rng, 2, -20, 25), rvec(rng, 2, -20, 25)
    Rf = F1 + F2
    Rm = float(np.linalg.norm(Rf))
    if Rm < 1:
        return None
    br = (deg(math.atan2(Rf[0], Rf[1])) + 360) % 360
    who = pick(rng, ['A barge is pulled by two tugboats', 'A crate is dragged by two ropes', 'A sailing boat is driven by wind and current', 'A float is towed by two jet-skis'])
    return ret(f'{who}. The forces (in newtons) are F₁ = {ijk(F1)} and F₂ = {ijk(F2)}, where i points east and j points north. (a) Find the resultant force. (b) Find its magnitude. (c) Find the bearing of the resultant. (d) Find the unit vector in the direction of the resultant. (e) A third force F₃ is added so that the object is in equilibrium; write down F₃.',
               f'(a) {ijk(Rf)} (b) {sf(Rm)} N (c) {br:05.1f}° (d) ({", ".join(sf(x) for x in Rf / Rm)}) (e) {ijk(-Rf)}',
               f'(a) A1. (b) √({int(Rf @ Rf)}) (M1) = {sf(Rm)} (A1). (c) tan⁻¹ of east/north components (M1), {br:05.1f}° (A1). (d) R/|R| (A1). (e) F₃ = −R (A1).', 7, 'multi_step', gap='G5')


R.facts('ch04-st2', F(
    terms=[('vector equation of a line', 'r = a + λb, where a is the position vector of a point on the line, b a direction vector and λ a scalar parameter'),
           ('direction vector', 'a vector parallel to the line; any non-zero multiple of it describes the same direction'),
           ('skew lines', 'lines in 3D that are not parallel and do not intersect'),
           ('angle between two lines', 'the acute angle between their direction vectors, found from cos θ = |b₁ · b₂| / (|b₁||b₂|)')],
    facts=[('Which point lies on the line r = (1, 2, 0) + λ(2, −1, 3)?', '(5, 0, 6)', ['(3, 2, 3)', '(2, −1, 3)', '(4, 1, 6)'], 'λ = 2 gives (5, 0, 6).'),
           ('Two lines in 3D have direction vectors (1, 2, −1) and (−2, −4, 2). The lines are…', 'parallel or coincident', ['perpendicular', 'skew', 'intersecting at 45°'], 'One direction is −2 times the other.'),
           ('Lines with direction vectors (1, 2, 2) and (2, −1, 0) meet at an angle of…', '90°', ['0°', '45°', '60°'], 'Scalar product 2 − 2 + 0 = 0.')],
    why=[('Explain why two lines in 3D can be neither parallel nor intersecting, unlike in 2D.', 'In 3D lines can lie in different planes (e.g. one above the other at different heights), so they may never meet even though their directions differ; in 2D non-parallel lines always meet.'),
         ('Explain why the angle between two lines uses only their direction vectors.', 'The angle depends only on the directions of the lines, not on where they are positioned; position vectors only fix the location.')],
    misc=[('The line r = (2, 1, 0) + λ(1, 3, −1) has direction vector (2, 1, 0).', 'The direction vector is the vector multiplied by the parameter, (1, 3, −1); (2, 1, 0) is the position of a point on the line.')],
))


@R.add('ch04-st2', ALL, (1, 5), 'short')
def vline_core(rng, slot):
    c, d = slot.c, slot.d
    a1, b1 = rvec(rng, 3, -5, 6), rvec(rng, 3, -4, 5)
    if not b1.any():
        return None
    eq1 = f'r = {vec(a1)} + λ{vec(b1)}'
    if c == 'C1':
        if d <= 1:
            lam = rng.choice([-2, -1, 2, 3])
            P = a1 + lam * b1
            return mcq(rng, f'Which point lies on the line {eq1}?', pt(P), [pt(a1 + lam * b1 + np.array([1, 0, 0])), pt(b1 + lam * a1), pt(a1 - lam * b1 + np.array([0, 1, 0]))], f'λ = {lam}: {pt(P)}.')
        P, Q = rvec(rng, 3, -5, 8), rvec(rng, 3, -5, 8)
        if (P == Q).all():
            return None
        return ret(f'Write down a vector equation of the line through A{pt(P)} and B{pt(Q)}.', f'r = {vec(P)} + λ{vec(Q - P)}', f'direction AB = {vec(Q - P)} (M1 A1); r = {vec(P)} + λ{vec(Q - P)} (A1) (any equivalent form).', 3)
    b2 = rvec(rng, 3, -4, 5)
    if not b2.any() or np.linalg.norm(np.cross(b1, b2)) < 1e-9:
        return None
    th = ang(b1, b2)
    th = min(th, 180 - th)
    if c == 'C2':
        P = a1 + rng.randint(-3, 4) * b1
        on = rng.random() < 0.5
        Q = P if on else P + np.array([0, 0, rng.choice([1, 2, -1])])
        lam = [(Q[i] - a1[i]) / b1[i] for i in range(3) if b1[i] != 0]
        return ret(f'Determine whether the point {pt(Q)} lies on the line {eq1}, explaining your method.', 'yes' if on else 'no',
                   f'M1 set {vec(Q)} = {vec(a1)} + λ{vec(b1)}; R1 ' + ('all non-zero components give the same λ = ' + frs(Fr(lam[0]).limit_denominator(100)) + ' (and zero components match); A1 it lies on the line.' if on else 'the components do not give a consistent λ; A1 it does not lie on the line.'), 3, 'explain')
    if c == 'C3':
        return ret(f'Find the acute angle between the lines L₁: r = {vec(a1)} + λ{vec(b1)} and L₂: r = {vec(rvec(rng, 3, -5, 6))} + μ{vec(b2)}.', f'{sf(th)}°',
                   f'b₁ · b₂ = {int(b1 @ b2)} (A1); |b₁| = √{int(b1 @ b1)}, |b₂| = √{int(b2 @ b2)} (A1); cos θ = |{int(b1 @ b2)}|/(√{int(b1 @ b1)} √{int(b2 @ b2)}) (M1) ⇒ θ = {sf(th)}° (A1).', 4, 'numerical')
    # C4: intersecting or skew in 3D
    lam0, mu0 = rng.randint(-3, 4), rng.randint(-3, 4)
    X = a1 + lam0 * b1
    inter = rng.random() < 0.6
    a2 = X - mu0 * b2 + (np.array([0, 0, 0]) if inter else np.array([0, 0, rng.choice([1, 2, -2])]))
    # check skew truly when not inter
    Mx = np.array([b1, -b2]).T
    sol, res, *_ = np.linalg.lstsq(Mx, a2 - a1, rcond=None)
    ok = np.allclose(Mx @ sol, a2 - a1)
    if ok != inter:
        return None
    who = pick(rng, [('two aircraft flight paths', 'km'), ('two cables in a building', 'm'), ('two tunnels being drilled through a mountain', 'm'), ('two laser beams in a stage show', 'm')])
    return ret(f'In a model of {who[0]} (units {who[1]}), L₁: r = {vec(a1)} + λ{vec(b1)} and L₂: r = {vec(a2)} + μ{vec(b2)}. (a) Show that the lines are not parallel. (b) Determine whether the lines intersect; if they do, find the point of intersection. (c) Find the acute angle between the lines. (d) Interpret your answer to (b) in context.',
               f'(b) ' + (f'intersect at {pt(X)}' if inter else 'skew (do not intersect)') + f' (c) {sf(th)}°',
               f'(a) R1 direction vectors are not multiples. (b) equate components (M1), solve two equations (M1) λ = {m(lam0) if inter else "…"}, μ = {m(mu0) if inter else "…"} (A1), ' + ('third equation satisfied (R1), point ' + pt(X) + ' (A1).' if inter else 'third equation not satisfied (R1), so the lines are skew (A1).') +
               f' (c) cos θ = |b₁ · b₂|/(|b₁||b₂|) (M1) = {sf(th)}° (A1). (d) R1 ' + ('the paths cross, so there is a potential collision point (if both arrive at the same time).' if inter else 'the paths never meet, so they cannot collide.'), 10, 'multi_step', gap='G5')


R.facts('ch04-st3', F(
    terms=[('constant velocity motion', 'r = r₀ + tv: the position after time t of an object starting at r₀ and moving with constant velocity v'),
           ('speed', 'the magnitude of the velocity vector, |v|'),
           ('closest approach', 'the time and distance at which two moving objects are nearest; found by minimising the distance between their position vectors'),
           ('projectile motion', 'motion under gravity alone: r = (ut cos θ, ut sin θ − ½gt²) for launch speed u at angle θ')],
    facts=[('A boat starts at (2, 3) km and moves with velocity (4, −1) km h⁻¹. Where is it after 2 hours?', '(10, 1)', ['(8, −2)', '(6, 2)', '(4, 1)'], 'r = (2, 3) + 2(4, −1).'),
           ('What is the speed of an object with velocity 6i + 8j m s⁻¹?', '10 m s⁻¹', ['14 m s⁻¹', '48 m s⁻¹', '2 m s⁻¹'], '√(36 + 64).'),
           ('In projectile motion without air resistance, the horizontal component of velocity…', 'stays constant', ['decreases at 9.8 m s⁻²', 'increases', 'is zero at the top'], 'Gravity only acts vertically.')],
    why=[('Explain why two ships whose paths cross need not collide.', 'Collision requires them to be at the same point at the same time; their paths may cross at a point they reach at different times.'),
         ('Explain why the vertical velocity of a projectile is zero at its maximum height.', 'The vertical component decreases steadily under gravity; at the top it changes from upward to downward, so it is momentarily zero.')],
    misc=[('If an object has velocity (3, 4) m s⁻¹, it travels 7 m every second.', 'Distance per second is the speed |v| = √(3² + 4²) = 5 m, not the sum of the components.')],
))


@R.add('ch04-st3', ALL, (1, 5), 'short')
def vkin_core(rng, slot):
    c, d = slot.c, slot.d
    r0, v = rvec(rng, 2, -10, 11), rvec(rng, 2, -8, 9)
    t = rng.randint(2, 9)
    who = pick(rng, ['A ferry', 'A container ship', 'A fishing boat', 'A research vessel', 'A coastguard launch'])
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'{who} starts at {pt(r0)} km and moves with constant velocity {vec(v)} km h⁻¹. Find its position after {t} hours.', pt(r0 + t * v), [pt(t * r0 + v), pt(r0 + v), pt(t * (r0 + v))], f'r = {vec(r0)} + {t}{vec(v)} = {pt(r0 + t * v)}.')
        return ret(f'{who} moves with velocity {ijk(v)} km h⁻¹. Find its speed and the distance it travels in {t} hours.', f'{sf(np.linalg.norm(v))} km h⁻¹; {sf(t * np.linalg.norm(v))} km',
                   f'speed |v| = √{int(v @ v)} (M1) = {sf(np.linalg.norm(v))} km h⁻¹ (A1); distance = {t} × {sf(np.linalg.norm(v))} = {sf(t * np.linalg.norm(v))} km (A1).', 3)
    if c == 'C2':
        u = rng.randint(12, 40)
        thd = rng.randint(20, 70)
        tf = 2 * u * sind(thd) / 9.8
        rng_x = u * cosd(thd) * tf
        return ret(f'A ball is kicked at {u} m s⁻¹ at {thd}° above horizontal ground. Its position is r = ({sf(u * cosd(thd))}t, {sf(u * sind(thd))}t − 4.9t²). Explain how to find when it lands, and find the horizontal distance travelled.', f't = {sf(tf)} s; {sf(rng_x)} m',
                   f'R1 it lands when the vertical component is 0 (t ≠ 0); M1 {sf(u * sind(thd))}t − 4.9t² = 0 ⇒ t = {sf(tf)} s; A1 x = {sf(u * cosd(thd))} × {sf(tf)} = {sf(rng_x)} m.', 3, 'explain')
    r1, v1 = r0, v
    for _ in range(50):
        r2, v2 = rvec(rng, 2, -10, 11), rvec(rng, 2, -8, 9)
        dr, dv = r2 - r1, v2 - v1
        if not dv.any():
            continue
        tc = -float(dr @ dv) / float(dv @ dv)
        if tc > 0.2:
            break
    else:
        return None
    dmin = float(np.linalg.norm(dr + tc * dv))
    if c == 'C3':
        return ret(f'Ship A starts at {pt(r1)} and has velocity {vec(v1)}; ship B starts at {pt(r2)} with velocity {vec(v2)} (km, km h⁻¹, same start time). Find an expression for the displacement from A to B after t hours and the time at which they are closest.', f'{vec(dr)} + t{vec(dv)}; t = {sf(tc)} h',
                   f'AB = (r₂ − r₁) + t(v₂ − v₁) = {vec(dr)} + t{vec(dv)} (M1 A1); minimise |AB|² (or AB·(v₂ − v₁) = 0) (M1) ⇒ t = {sf(tc)} h (A1).', 4, 'numerical')
    return ret(f'At noon, {who.lower()} A is at {pt(r1)} and moves with velocity {vec(v1)}, while yacht B is at {pt(r2)} with velocity {vec(v2)} (units km and km h⁻¹; i east, j north). (a) Find the speed of A. (b) Write down the position vectors of A and B after t hours. (c) Show that the distance between them is d(t) = |{vec(dr)} + t{vec(dv)}|. '
               f'(d) Find the time of closest approach and the minimum distance. (e) Visibility is 3 km; determine whether the crews can see each other.',
               f'(a) {sf(np.linalg.norm(v1))} km h⁻¹ (d) t = {sf(tc)} h, {sf(dmin)} km (e) {"yes" if dmin < 3 else "no"}',
               f'(a) A1. (b) A1 A1. (c) AG subtraction (M1). (d) differentiate |d|² or use technology (M1), t = {sf(tc)} (A1), d = {sf(dmin)} (A1). (e) R1 compare with 3 km.', 8, 'multi_step', gap='G5')


R.facts('ch04-st4', F(
    terms=[('scalar product', 'v · w = v₁w₁ + v₂w₂ + v₃w₃ = |v||w| cos θ, a scalar'),
           ('vector product', 'v × w, a vector perpendicular to both v and w with magnitude |v||w| sin θ'),
           ('perpendicular vectors', 'non-zero vectors whose scalar product is zero'),
           ('component of a vector', 'the projection of v in the direction of w, (v · w)/|w|')],
    facts=[('What is (2, −1, 3) · (1, 4, 2)?', '4', ['(2, −4, 6)', '9', '−4'], '2 − 4 + 6 = 4.'),
           ('The magnitude of v × w equals…', 'the area of the parallelogram formed by v and w', ['the volume of a cube', 'v · w', 'the angle between v and w'], '|v||w| sin θ.'),
           ('If v · w = 0 for non-zero vectors, then v and w are…', 'perpendicular', ['parallel', 'equal', 'unit vectors'], 'cos θ = 0.'),
           ('What is i × j?', 'k', ['−k', '0', '1'], 'Right-hand rule.')],
    why=[('Explain why the scalar product of perpendicular vectors is zero.', 'v · w = |v||w| cos θ and cos 90° = 0, so the product is 0 regardless of the magnitudes.'),
         ('Explain why v × w = −(w × v).', 'Swapping the order reverses the direction given by the right-hand rule while keeping the magnitude |v||w| sin θ.')],
    misc=[('The scalar product of two vectors is a vector.', 'It is a scalar (a number); the vector product v × w is a vector.')],
))


@R.add('ch04-st4', ALL, (1, 5), 'short')
def products_core(rng, slot):
    c, d = slot.c, slot.d
    u, v = rvec(rng, 3, -5, 6), rvec(rng, 3, -5, 6)
    cr = np.cross(u, v)
    if not cr.any():
        return None
    dp = int(u @ v)
    th = ang(u, v)
    if c == 'C1':
        if d <= 1:
            ws = [m(str(int(dp - 2 * u[2] * v[2]))), m(str(int(abs(u) @ abs(v)))), vec(u * v)]
            if len({m(str(dp)), *ws}) < 4:
                return None
            return mcq(rng, f'Find the scalar product of {ijk(u)} and {ijk(v)}.', m(str(dp)), ws, f'{" + ".join(f"({m(_num(a))})({m(_num(b))})" for a, b in zip(u, v))} = {m(str(dp))}.')
        return ret(f'Find the vector product of a = {ijk(u)} and b = {ijk(v)}.', ijk(cr), f'Determinant/component formula (M1); a × b = {ijk(cr)} (A1 A1).', 3)
    if c == 'C2':
        w = rvec(rng, 3, -4, 5)
        # make perpendicular sometimes
        if rng.random() < 0.5:
            w = np.cross(u, rvec(rng, 3, -2, 3))
            if not w.any():
                return None
        perp = int(u @ w) == 0
        return ret(f'Determine whether the vectors {ijk(u)} and {ijk(w)} are perpendicular, explaining your reasoning.', 'perpendicular' if perp else 'not perpendicular',
                   f'M1 scalar product = {m(str(int(u @ w)))}; R1 ' + ('it is zero, so cos θ = 0 and θ = 90°; A1 perpendicular.' if perp else 'it is non-zero, so θ ≠ 90°; A1 not perpendicular.'), 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            return ret(f'Find the angle between the vectors {ijk(u)} and {ijk(v)}.', f'{sf(th)}°', f'scalar product {dp} (A1); magnitudes √{int(u @ u)}, √{int(v @ v)} (A1); cos θ = {dp}/(√{int(u @ u)}√{int(v @ v)}) (M1) ⇒ {sf(th)}° (A1).', 4, 'numerical')
        A_ = rvec(rng, 3, -4, 6)
        B, C = A_ + u, A_ + v
        return ret(f'Find the area of the triangle with vertices A{pt(A_)}, B{pt(B)} and C{pt(C)}.', _num(0.5 * np.linalg.norm(cr)),
                   f'AB = {ijk(u)}, AC = {ijk(v)} (A1); AB × AC = {ijk(cr)} (M1 A1); area = ½|AB × AC| = ½√{int(cr @ cr)} = {_num(0.5 * np.linalg.norm(cr))} (A1).', 4, 'numerical')
    Fv = rvec(rng, 3, 1, 15)
    dv = rvec(rng, 3, -3, 12)
    if not dv.any():
        return None
    W = float(Fv @ dv)
    comp = W / float(np.linalg.norm(dv))
    thF = ang(Fv, dv)
    return ret(f'A crane applies a force F = {ijk(Fv)} N to move a load along the displacement d = {ijk(dv)} m. (a) Find the work done, W = F · d. (b) Find the angle between the force and the displacement. (c) Find the component of F in the direction of d. (d) Find a vector perpendicular to both F and d. (e) Explain what a negative value in (a) would mean.',
               f'(a) {sf(W) if not float(W).is_integer() else _num(W)} J (b) {sf(thF)}° (c) {sf(comp)} N (d) {ijk(np.cross(Fv, dv))}',
               f'(a) scalar product (M1) {m(_num(W))} J (A1). (b) cos θ = W/(|F||d|) (M1) {sf(thF)}° (A1). (c) F · d/|d| (M1) {sf(comp)} (A1). (d) F × d (M1) {ijk(np.cross(Fv, dv))} (A1). (e) R1 the force would oppose the motion (angle > 90°).', 9, 'multi_step', gap='G5')


# =============================================================================================
# ch05 Graph theory
# =============================================================================================
import itertools as _it


def rgraph(rng, n, extra, wlo=2, whi=20, weighted=True):
    """random connected simple graph: dict {(u, v): w} with u < v, vertices 'A'.. ."""
    V = 'ABCDEFGH'[:n]
    order = list(range(n))
    rng.shuffle(order)
    E = {}
    for i in range(1, n):
        j = order[rng.randrange(i)]
        a, b = sorted((order[i], j))
        E[(a, b)] = rng.randint(wlo, whi) if weighted else 1
    pairs = [p for p in _it.combinations(range(n), 2) if p not in E]
    rng.shuffle(pairs)
    for p in pairs[:extra]:
        E[p] = rng.randint(wlo, whi) if weighted else 1
    return V, E


def etext(V, E, weighted=True):
    return ', '.join(f'{V[a]}{V[b]}' + (f' ({w})' if weighted else '') for (a, b), w in sorted(E.items()))


def degrees(n, E):
    dg = [0] * n
    for a, b in E:
        dg[a] += 1
        dg[b] += 1
    return dg


def kruskal(n, E):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    out = []
    for (a, b), w in sorted(E.items(), key=lambda kv: (kv[1], kv[0])):
        ra, rb = f(a), f(b)
        if ra != rb:
            par[ra] = rb
            out.append(((a, b), w))
    return out


def prim(n, E, start=0):
    inT = {start}
    out = []
    while len(inT) < n:
        best = min(((e, w) for e, w in E.items() if (e[0] in inT) != (e[1] in inT)), key=lambda kv: (kv[1], kv[0]))
        out.append(best)
        inT |= set(best[0])
    return out


def floyd(n, E):
    INF = 10 ** 9
    D = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for (a, b), w in E.items():
        D[a][b] = D[b][a] = min(D[a][b], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    return D


def pairings(lst):
    if not lst:
        yield []
        return
    a = lst[0]
    for i in range(1, len(lst)):
        rest = lst[1:i] + lst[i + 1:]
        for p in pairings(rest):
            yield [(a, lst[i])] + p


def postman(n, E):
    dg = degrees(n, E)
    odd = [i for i in range(n) if dg[i] % 2]
    D = floyd(n, E)
    best = None
    opts = []
    for p in pairings(odd):
        cst = sum(D[a][b] for a, b in p)
        opts.append((p, cst))
        if best is None or cst < best[1]:
            best = (p, cst)
    return odd, opts, best, sum(E.values())


def metric_table(rng, n):
    pts = [(rng.uniform(0, 30), rng.uniform(0, 30)) for _ in range(n)]
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            D[i][j] = D[j][i] = max(2, int(round(math.dist(pts[i], pts[j]))))
    # enforce triangle inequality by shortest paths
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    return D


def nn_tour(D, s):
    n = len(D)
    tour, tot, cur_ = [s], 0, s
    while len(tour) < n:
        nxt = min((j for j in range(n) if j not in tour), key=lambda j: (D[cur_][j], j))
        if sorted(D[cur_][j] for j in range(n) if j not in tour)[:2].count(D[cur_][nxt]) > 1:
            return None
        tot += D[cur_][nxt]
        tour.append(nxt)
        cur_ = nxt
    tot += D[cur_][s]
    return tour + [s], tot


def deleted_lb(D, dv):
    n = len(D)
    rest = [i for i in range(n) if i != dv]
    E = {(a, b): D[a][b] for a, b in _it.combinations(rest, 2)}
    idx = {v: i for i, v in enumerate(rest)}
    E2 = {(idx[a], idx[b]): w for (a, b), w in E.items()}
    mst = kruskal(len(rest), E2)
    w_mst = sum(w for _, w in mst)
    two = sorted(D[dv][j] for j in rest)[:2]
    return w_mst, two, w_mst + sum(two)


def dtable(V, D):
    n = len(D)
    return '; '.join(f'{V[i]}{V[j]} = {D[i][j]}' for i in range(n) for j in range(i + 1, n))


R.facts('ch05-st1', F(
    terms=[('degree of a vertex', 'the number of edges meeting at the vertex (a loop counts twice)'),
           ('simple graph', 'a graph with no loops and no multiple edges between the same pair of vertices'),
           ('complete graph Kₙ', 'a simple graph on n vertices in which every pair of vertices is joined by an edge; it has n(n − 1)/2 edges'),
           ('Eulerian circuit', 'a closed walk that uses every edge exactly once; it exists in a connected graph exactly when every vertex has even degree'),
           ('Hamiltonian cycle', 'a cycle that visits every vertex exactly once and returns to the start'),
           ('tree', 'a connected graph with no cycles; a tree on n vertices has n − 1 edges'),
           ('directed graph', 'a graph whose edges have a direction, shown by arrows; each vertex has an in-degree and an out-degree')],
    facts=[('How many edges does K₆ have?', '15', ['30', '12', '36'], '6 × 5/2.'),
           ('A graph has degrees 3, 3, 4, 2, 2. How many edges does it have?', '7', ['14', '5', '12'], 'Sum of degrees = 14 = 2 × edges.'),
           ('A connected graph has exactly two odd vertices. It has…', 'an Eulerian trail but not an Eulerian circuit', ['an Eulerian circuit', 'neither an Eulerian trail nor circuit', 'a Hamiltonian cycle necessarily'], 'Start and end at the odd vertices.'),
           ('Why can no graph have degrees 3, 3, 3, 2?', 'the sum of degrees is odd', ['there are too many vertices', 'it contains a loop', 'it is complete'], 'The sum must be 2 × number of edges.')],
    why=[('Explain why the sum of the degrees in any graph is even.', 'Each edge has two ends and contributes 1 to the degree of each, so the degree sum is 2 × (number of edges).'),
         ('Explain why every vertex must have even degree for an Eulerian circuit to exist.', 'Each time the circuit passes through a vertex it uses one edge in and one edge out, so the edges at every vertex pair up.')],
    contrast=[('Eulerian circuit', 'Hamiltonian cycle', 'an Eulerian circuit uses every edge once; a Hamiltonian cycle visits every vertex once')],
    misc=[('A graph with an Eulerian circuit must also have a Hamiltonian cycle.', 'The properties are independent: e.g. two triangles joined at a single vertex have an Eulerian circuit but no Hamiltonian cycle.')],
))


@R.add('ch05-st1', ALL, (1, 5), 'short')
def gterm_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.randint(5, 7)
    V, E = rgraph(rng, n, rng.randint(1, 5), weighted=False)
    dg = degrees(n, E)
    odd = [V[i] for i in range(n) if dg[i] % 2]
    el = etext(V, E, False)
    if c == 'C1':
        if d <= 1:
            k = rng.randint(4, 12)
            return nmcq(rng, f'How many edges does the complete graph K{"₀₁₂₃₄₅₆₇₈₉"[k] if k < 10 else "₁" + "₀₁₂₃₄₅₆₇₈₉"[k - 10]} have?', k * (k - 1) // 2, [k * (k - 1), k * k, k * (k + 1) // 2], f'n(n − 1)/2 = {k}({k - 1})/2 = {k * (k - 1) // 2}.', fmtf=lambda z: str(int(z)))
        return ret(f'A simple graph has vertices {", ".join(V)} and edges {el}. Write down the degree of each vertex and verify the handshaking lemma.', ', '.join(f'{V[i]}: {dg[i]}' for i in range(n)),
                   f'degrees (A2 for all correct, A1 for at least {n - 2}); sum = {sum(dg)} = 2 × {len(E)} edges (R1).', 3)
    if c == 'C2':
        kind = 'an Eulerian circuit' if not odd else ('an Eulerian trail (but no circuit)' if len(odd) == 2 else 'neither an Eulerian circuit nor an Eulerian trail')
        return ret(f'A park has junctions {", ".join(V)} joined by paths {el}. Explain whether a jogger can run along every path exactly once, and whether she can finish where she started.', kind,
                   f'A1 degrees ' + ', '.join(f'{V[i]} {dg[i]}' for i in range(n)) + f'; R1 {len(odd)} odd vertices' + (f' ({", ".join(odd)})' if odd else '') + '; R1 ' +
                   ('all even ⇒ Eulerian circuit: yes and yes.' if not odd else (f'exactly two odd ⇒ trail from {odd[0]} to {odd[1]}, but cannot return to the start.' if len(odd) == 2 else 'more than two odd vertices ⇒ impossible without repeating paths.')), 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            nv = rng.randint(6, 15)
            k = rng.randint(2, 6)
            if (nv * k) % 2:
                nv += 1
            return ret(f'A communication network has {nv} servers, each directly connected to exactly {k} others. Find the number of connections, and the number of extra connections needed to make every server connected to every other.', f'{nv * k // 2}; {nv * (nv - 1) // 2 - nv * k // 2}',
                       f'handshaking: edges = {nv} × {k}/2 (M1) = {nv * k // 2} (A1); K{nv} has {nv}×{nv - 1}/2 = {nv * (nv - 1) // 2} (M1); extra {nv * (nv - 1) // 2 - nv * k // 2} (A1).', 4, 'numerical')
        tree_n = rng.randint(6, 20)
        return ret(f'A tree has {tree_n} vertices. Find the number of edges and the sum of the degrees, and determine whether the tree can have exactly 3 leaves (vertices of degree 1).', f'{tree_n - 1} edges; degree sum {2 * (tree_n - 1)}',
                   f'tree ⇒ n − 1 = {tree_n - 1} edges (A1); sum = 2 × {tree_n - 1} = {2 * (tree_n - 1)} (A1); R1 with 3 leaves the other {tree_n - 3} vertices would need degree total {2 * (tree_n - 1) - 3}, which needs one vertex of degree 3 – possible (e.g. a "Y" shape) (A1).', 4, 'numerical')
    town = pick(rng, ['a village', 'a university campus', 'a botanical garden', 'an old town centre'])
    added = None
    if len(odd) == 2:
        added = f'{odd[0]}{odd[1]}'
    return ret(f'The footpaths of {town} are modelled by the graph with vertices {", ".join(V)} and edges {el}. (a) Write down the degree of each vertex. (b) State, with a reason, whether the graph is simple and whether it is connected. (c) Determine whether there is an Eulerian circuit, an Eulerian trail or neither. '
               f'(d) State the minimum number of paths that would need to be added to make an Eulerian circuit possible, and suggest which. (e) Explain whether a Hamiltonian cycle would help a gardener who must walk every path.',
               f'(a) ' + ', '.join(f'{V[i]} {dg[i]}' for i in range(n)) + f' (c) {"circuit" if not odd else ("trail" if len(odd) == 2 else "neither")} (d) {len(odd) // 2}',
               f'(a) A2. (b) R1 no loops/multiple edges; R1 every vertex reachable. (c) {len(odd)} odd vertices (M1) conclusion (A1). (d) pair up the odd vertices {", ".join(odd) if odd else "(none)"} (R1) ⇒ {len(odd) // 2} (A1). (e) R1 no: a Hamiltonian cycle visits vertices, not every edge.', 9, 'multi_step', gap='G5')


R.facts('ch05-st2', F(
    terms=[('adjacency matrix', 'a square matrix whose (i, j) entry is the number of edges from vertex i to vertex j'),
           ('walk', 'a sequence of edges in which consecutive edges share a vertex; vertices and edges may repeat'),
           ('transition matrix', 'a matrix of probabilities of moving between vertices in one step; for a random walk each column sums to 1'),
           ('number of walks of length k', 'the (i, j) entry of Aᵏ, where A is the adjacency matrix')],
    facts=[('For an undirected graph, the adjacency matrix is always…', 'symmetric', ['diagonal', 'the identity', 'upper triangular'], 'Edge i–j is also j–i.'),
           ('The (2, 3) entry of A³ gives…', 'the number of walks of length 3 from vertex 2 to vertex 3', ['the number of edges from 2 to 3', 'the shortest path length from 2 to 3', 'the degree of vertex 3'], 'Powers count walks.'),
           ('In the adjacency matrix of a simple graph, the sum of a row equals…', 'the degree of that vertex', ['the number of edges in the graph', 'zero', 'the number of vertices'], 'Each 1 is an edge at that vertex.')],
    why=[('Explain why the entries of A² count walks of length 2.', 'The (i, j) entry of A² is Σₖ aᵢₖaₖⱼ; each term is 1 exactly when there is an edge i–k and an edge k–j, i.e. a two-step walk through k.'),
         ('Explain why the columns of the transition matrix of a random walk sum to 1.', 'From a given vertex the walker must move to one of its neighbours, so the probabilities of all possible next vertices add up to 1.')],
    misc=[('The (i, j) entry of A³ is the number of paths of length 3 from i to j.', 'It counts walks, which may repeat vertices and edges; paths do not repeat vertices.')],
))


def amat(n, E, directed=False):
    A = np.zeros((n, n), dtype=int)
    for (a, b), w in E.items():
        A[a, b] += 1
        if not directed:
            A[b, a] += 1
    return A


@R.add('ch05-st2', ALL, (1, 5), 'short')
def adj_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.randint(4, 5)
    V, E = rgraph(rng, n, rng.randint(1, 3), weighted=False)
    A = amat(n, E)
    el = etext(V, E, False)
    i, j = rng.sample(range(n), 2)
    if c == 'C1':
        k = 2
        Ak = np.linalg.matrix_power(A, k)
        if d <= 1:
            return ret(f'Write down the adjacency matrix of the graph with vertices {", ".join(V)} (in that order) and edges {el}.', mat(A), f'A1 symmetric 0/1 entries; A1 all correct: {mat(A)}.', 2)
        return nmcq(rng, f'A graph has adjacency matrix {mat(A)} (vertices {", ".join(V)}). How many walks of length 2 are there from {V[i]} to {V[j]}?', int(Ak[i, j]), [int(A[i, j]), int(Ak[i, j]) + 1, int(Ak[i, i])] if int(Ak[i, i]) != int(Ak[i, j]) else [int(A[i, j]) + 2, int(Ak[i, j]) + 1, int(Ak[i, j]) + 3],
                    f'(A²) entry ({V[i]}, {V[j]}) = Σ a{V[i]}k ak{V[j]} = {int(Ak[i, j])}.', fmtf=lambda z: str(int(z)))
    if c == 'C2':
        A3 = np.linalg.matrix_power(A, 3)
        if A3[i, j] < 2:
            return None
        return ret(f'For the graph with adjacency matrix {mat(A)} (vertices {", ".join(V)}), {name(rng)} says there are {int(A3[i, j])} different routes of three roads from {V[i]} to {V[j]} that never revisit a town. Explain why this may be incorrect.', 'A³ counts walks, which may revisit vertices',
                   f'A1 ({V[i]}, {V[j]}) entry of A³ = {int(A3[i, j])}; R1 A³ counts all walks of length 3; R1 walks may repeat vertices/edges (e.g. go back and forth), so the number of paths can be smaller.', 3, 'explain')
    deg_ = A.sum(axis=0)
    Tm = A / deg_
    if c == 'C3':
        k = rng.randint(3, 5)
        Ak = np.linalg.matrix_power(A, k)
        tot = int(sum(np.linalg.matrix_power(A, q)[i, j] for q in range(1, k + 1)))
        return ret(f'A graph has adjacency matrix {mat(A)} with vertices {", ".join(V)}. Find the number of walks of length {k} from {V[i]} to {V[j]} and the total number of walks from {V[i]} to {V[j]} of length at most {k}.', f'{int(Ak[i, j])}; {tot}',
                   f'A{sup(k)} (M1) entry = {int(Ak[i, j])} (A1); sum of entries of A + … + A{sup(k)} (M1) = {tot} (A1).', 4, 'numerical')
    s0 = np.zeros(n)
    s0[i] = 1
    s2 = np.linalg.matrix_power(Tm, 2) @ s0
    s3 = np.linalg.matrix_power(Tm, 3) @ s0
    # steady state ∝ degree
    st_ = deg_ / deg_.sum()
    who = pick(rng, ['A tourist wanders between the attractions', 'A delivery robot moves at random between depots', 'A bird flies at random between feeding stations'])
    return ret(f'{who} {", ".join(V)}, joined by routes {el}; at each step it chooses one of the routes from its current position at random. (a) Write down the transition matrix T (columns give the current position). (b) Starting at {V[i]}, find the probability of being at {V[j]} after 2 steps. '
               f'(c) Find the probability of being at {V[j]} after 3 steps. (d) Find the long-term proportion of time spent at each location. (e) Explain the link between your answer to (d) and the degrees.',
               f'(b) {sf(s2[j])} (c) {sf(s3[j])} (d) ' + ', '.join(f'{V[q]}: {frs(Fr(int(deg_[q]), int(deg_.sum())))}' for q in range(n)),
               f'(a) column q has 1/deg(q) in rows of neighbours (A2). (b) T²s₀ (M1) {sf(s2[j])} (A1). (c) T³s₀ (A1). (d) solve Ts = s or high power of T (M1) ' + ', '.join(f'{frs(Fr(int(deg_[q]), int(deg_.sum())))}' for q in range(n)) + f' (A1). (e) R1 proportion = degree/{int(deg_.sum())} (sum of degrees).', 8, 'multi_step', gap='G5')


R.facts('ch05-st3', F(
    terms=[('spanning tree', 'a subgraph that is a tree and includes every vertex of the graph'),
           ('minimum spanning tree', 'a spanning tree of least total weight'),
           ("Kruskal's algorithm", 'choose edges in increasing order of weight, rejecting any that would form a cycle, until n − 1 edges are chosen'),
           ("Prim's algorithm", 'grow a tree from a starting vertex, each time adding the least-weight edge joining the tree to a new vertex')],
    facts=[('A minimum spanning tree of a connected graph with 8 vertices has how many edges?', '7', ['8', '28', '16'], 'Any tree on n vertices has n − 1 edges.'),
           ("Kruskal's algorithm rejects an edge when…", 'it would create a cycle', ['it is the heaviest edge', 'it joins two vertices of even degree', 'it is adjacent to the previous edge'], 'The result must be a tree.'),
           ("Which algorithm is easier to apply to a distance table (matrix)?", "Prim's algorithm", ["Kruskal's algorithm", 'nearest neighbour', 'Euler’s method'], 'Prim works column by column on the table.')],
    why=[("Explain why Prim's and Kruskal's algorithms give spanning trees of the same total weight.", 'Both are greedy algorithms proven to give a minimum spanning tree; if edge weights are distinct the minimum spanning tree is unique, otherwise any minimum spanning tree has the same minimum total.'),
         ('Explain why a minimum spanning tree is useful for planning a cable network.', 'It connects every site using the least total length of cable without redundant loops.')],
    misc=[("Kruskal's algorithm must start at vertex A.", "Kruskal's algorithm starts from the lightest edge anywhere in the graph; it is Prim's algorithm that starts at a chosen vertex.")],
))


@R.add('ch05-st3', ALL, (1, 5), 'short')
def mst_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.randint(5, 7)
    V, E = rgraph(rng, n, rng.randint(3, 6), 2, 25)
    if len(set(E.values())) < len(E):
        # distinct weights for unambiguous order
        ws = rng.sample(range(2, 40), len(E))
        E = {e: w for e, w in zip(E, ws)}
    K = kruskal(n, E)
    tot = sum(w for _, w in K)
    el = etext(V, E)
    kord = ', '.join(f'{V[a]}{V[b]}' for (a, b), _ in K)
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'A connected weighted graph has vertices {", ".join(V)} and edges (weights) {el}. What is the weight of its minimum spanning tree?', tot, [tot + sorted(E.values())[n - 1], sum(sorted(E.values())[:n - 1]) if sum(sorted(E.values())[:n - 1]) != tot else tot - 1, sum(E.values())],
                        f"Kruskal: {kord}; total {tot}.", fmtf=lambda z: str(int(z)))
        return ret(f'Use Kruskal\'s algorithm to find a minimum spanning tree of the graph with vertices {", ".join(V)} and edges (weights) {el}. State the order in which edges are added and the total weight.', f'{kord}; {tot}',
                   f'edges in increasing order, rejecting cycles (M1); {kord} (A1 A1); total {tot} (A1).', 4)
    if c == 'C2':
        st0 = rng.randrange(n)
        P = prim(n, E, st0)
        pord = ', '.join(f'{V[a]}{V[b]}' for (a, b), _ in P)
        return ret(f'For the graph with edges (weights) {el}, explain how Prim\'s algorithm differs from Kruskal\'s algorithm, and give the order in which Prim\'s algorithm, starting at {V[st0]}, adds edges.', pord,
                   f"R1 Prim grows one connected tree from a start vertex; R1 Kruskal picks the cheapest edge anywhere (forest may be disconnected mid-way); A1 Prim order {pord} (total {sum(w for _, w in P)}, same as Kruskal).", 3, 'explain')
    if c == 'C3':
        D = metric_table(rng, n)
        E2 = {(a, b): D[a][b] for a, b in _it.combinations(range(n), 2)}
        if len(set(E2.values())) < len(E2) - 2:
            pass
        P = prim(n, E2, 0)
        tot2 = sum(w for _, w in P)
        return ret(f'The table gives road distances (km) between {n} villages: {dtable(V, D)}. Use Prim\'s algorithm starting at A to find the minimum length of cable needed to connect all the villages (cables run along roads).', f'{tot2} km',
                   f'Prim from A (M1): ' + ', '.join(f'{V[a]}{V[b]} ({w})' for (a, b), w in P) + f' (A1 A1); total {tot2} km (A1).', 4, 'numerical')
    must = rng.choice([e for e in E if e not in [k for k, _ in K]] or [None])
    if must is None:
        return None
    E3 = dict(E)
    w_must = E3.pop(must)
    # MST with forced edge
    par_n = n
    K2 = kruskal(n, {must: -1, **E3})
    tot_forced = sum(E[e] for e, _ in K2)
    cost = rng.randint(2, 9) * 100
    cu = cur(rng)
    ctx = pick(rng, ['fibre-optic cable between campus buildings', 'irrigation pipes between fields', 'power lines between villages', 'cycle lanes between parks'])
    return ret(f'Planners want to lay {ctx}. The possible links and their lengths (km) are {el}. (a) Use Kruskal\'s algorithm to find a minimum spanning tree, listing edges in the order added. (b) Find its total length. (c) Installation costs {cost} {cu} per km; find the cost. '
               f'(d) Edge {V[must[0]]}{V[must[1]]} must be included for political reasons. Find the new minimum total length. (e) Explain why the minimum spanning tree has exactly {n - 1} edges.',
               f'(a) {kord} (b) {tot} km (c) {money(tot * cost, 0)} {cu} (d) {tot_forced} km',
               f'(a) M1 A2. (b) A1. (c) A1. (d) include {V[must[0]]}{V[must[1]]} first then continue Kruskal (M1) ⇒ {tot_forced} (A1). (e) R1 a tree on {n} vertices has {n - 1} edges; fewer would disconnect, more would create a cycle.', 8, 'multi_step', gap='G5')


R.facts('ch05-st4', F(
    terms=[('Chinese postman problem', 'finding the shortest closed route that traverses every edge of a weighted graph at least once'),
           ('travelling salesman problem', 'finding the shortest Hamiltonian cycle (visiting every vertex once) in a weighted complete graph'),
           ('nearest-neighbour algorithm', 'from the current vertex go to the nearest unvisited vertex, returning to the start at the end; gives an upper bound for the TSP'),
           ('deleted-vertex algorithm', 'delete a vertex, find the MST of the rest, and add the two shortest edges from the deleted vertex; gives a lower bound for the TSP')],
    facts=[('In the Chinese postman problem, a graph with all even vertices requires a route of length…', 'equal to the total weight of all edges', ['twice the total weight', 'the MST weight', 'the total weight plus the shortest edge'], 'An Eulerian circuit exists.'),
           ('The nearest-neighbour algorithm gives…', 'an upper bound for the travelling salesman problem', ['a lower bound', 'the exact optimum always', 'a minimum spanning tree'], 'It produces an actual tour.'),
           ('With 4 odd vertices, how many ways can they be paired in the Chinese postman problem?', '3', ['2', '4', '6'], 'AB/CD, AC/BD, AD/BC.')],
    why=[('Explain why the deleted-vertex method gives a lower bound for the TSP.', 'Removing the deleted vertex from an optimal tour leaves a spanning path of the remaining vertices, which weighs at least the MST; the two edges at the deleted vertex weigh at least its two shortest edges.'),
         ('Explain why odd vertices must be paired in the Chinese postman problem.', 'A closed route needs every vertex to have even degree; repeating the shortest path between pairs of odd vertices makes their degrees even at minimum extra cost.')],
    contrast=[('Chinese postman problem', 'travelling salesman problem', 'the postman must cover every edge, the salesman must visit every vertex')],
    misc=[('If the nearest-neighbour tour has length 50 and the deleted-vertex bound is 44, the optimal tour is 47.', 'We only know 44 ≤ optimum ≤ 50; the optimum could be any value in this interval.')],
))


@R.add('ch05-st4', ALL, (1, 5), 'short')
def cpp_tsp_core(rng, slot):
    c, d = slot.c, slot.d
    if c in ('C1', 'C3') and rng.random() < 0.5 or c == 'C2' and rng.random() < 0.5:
        n = rng.randint(5, 6)
        V, E = rgraph(rng, n, rng.randint(2, 5), 2, 20)
        odd, opts, best, tot = postman(n, E)
        if len(odd) not in (2, 4):
            return None
        el = etext(V, E)
        D = floyd(n, E)
        pr = '; '.join(f'{" + ".join(V[a] + V[b] for a, b in p)} = ' + (' + '.join(str(D[a][b]) for a, b in p) + f' = {cst}' if len(p) > 1 else f'{cst}') for p, cst in opts)
        bp = ' and '.join(f'the shortest path {V[a]}–{V[b]}' for a, b in best[0])
        if c == 'C1':
            return ret(f'A road sweeper must travel along every street of the network with edges (lengths in km) {el}, returning to the depot. Identify the odd vertices and find the length of the shortest route.', f'odd: {", ".join(V[i] for i in odd)}; {tot + best[1]} km',
                       f'odd vertices {", ".join(V[i] for i in odd)} (A1); total weight {tot} (A1); repeat {bp} ({best[1]}) (M1); {tot + best[1]} km (A1).', 4)
        if c == 'C2':
            return ret(f'For the network with edges (lengths) {el}, explain why the shortest route covering every edge and returning to the start is longer than the total length {tot}, and find the extra distance.', f'{best[1]}',
                       f'R1 odd vertices {", ".join(V[i] for i in odd)} mean no Eulerian circuit; R1 the shortest paths between paired odd vertices must be repeated; A1 {pr}; minimum {best[1]}.', 4, 'explain')
        return ret(f'A postal worker must walk along every street in the network with edges (lengths in hundreds of metres) {el}, starting and finishing at A. Find the length of the shortest route, showing your pairings.', f'{tot + best[1]}',
                   f'odd vertices (A1); pairings {pr} (M1 A1); total {tot} + {best[1]} = {tot + best[1]} (A1).', 5, 'numerical')
    n = rng.randint(5, 6)
    V = 'ABCDEF'[:n]
    D = metric_table(rng, n)
    s = rng.randrange(n)
    t = nn_tour(D, s)
    if t is None:
        return None
    tour, ub = t
    dv = rng.choice([i for i in range(n) if i != s])
    w_mst, two, lb = deleted_lb(D, dv)
    # optimum by brute force
    best = min(sum(D[p[i]][p[(i + 1) % n]] for i in range(n)) for p in ([0] + list(q) for q in _it.permutations(range(1, n))))
    tt = '–'.join(V[i] for i in tour)
    if lb > ub:
        return None
    if c == 'C1':
        return ret(f'A courier must visit {n} towns and return to the start. The distances (km) are {dtable(V, D)}. Use the nearest-neighbour algorithm starting at {V[s]} to find an upper bound for the shortest tour.', f'{tt}; {ub} km',
                   f'nearest unvisited each step (M1); tour {tt} (A1); upper bound {ub} km (A1).', 3)
    if c == 'C2':
        return ret(f'For the towns with distances {dtable(V, D)}, a nearest-neighbour tour from {V[s]} has length {ub} km and deleting {V[dv]} gives a lower bound of {lb} km. Explain what these values tell you about the optimal tour.', f'{lb} ≤ optimal ≤ {ub}',
                   f'R1 the nearest-neighbour tour is an actual tour so the optimum is at most {ub}; R1 the deleted-vertex value cannot exceed the optimum, so the optimum ≥ {lb}; A1 {lb} ≤ L ≤ {ub} km (the optimum is in fact {best} km).', 3, 'explain')
    if c == 'C3':
        return ret(f'The distances (km) between {n} warehouses are {dtable(V, D)}. Use the deleted-vertex algorithm, deleting {V[dv]}, to find a lower bound for the travelling salesman problem.', f'{lb} km',
                   f'MST of the remaining vertices (M1) weight {w_mst} (A1); two shortest edges from {V[dv]}: {two[0]} + {two[1]} (A1); lower bound {lb} km (A1).', 4, 'numerical')
    return ret(f'A band plans a tour of {n} cities and must return home. The travel distances (×100 km) are {dtable(V, D)}. (a) Use the nearest-neighbour algorithm starting at {V[s]} to find an upper bound. (b) By deleting {V[dv]}, use the deleted-vertex algorithm to find a lower bound. '
               f'(c) Write down an inequality for the length L of the optimal tour. (d) Explain why the nearest-neighbour algorithm may not give the optimal tour. (e) The optimal tour is in fact {best}; comment on the quality of your bounds.',
               f'(a) {tt}, {ub} (b) {lb} (c) {lb} ≤ L ≤ {ub}',
               f'(a) M1 A1 A1. (b) MST of the rest {w_mst} (M1 A1) + {two[0]} + {two[1]} (A1) = {lb}. (c) A1. (d) R1 greedy choices early on can force long edges later. (e) R1 compare {best} with the interval (upper bound {"exact" if ub == best else f"{ub - best} too high"}, lower bound {"exact" if lb == best else f"{best - lb} too low"}).', 10, 'multi_step', gap='G5')


@R.add('ch05-st1', ('C3', 'C4'), (2, 5), 'numerical')
def gterm_extra(rng, slot):
    n = rng.randint(5, 7)
    V, E = rgraph(rng, n, rng.randint(2, 6), weighted=False)
    dg = degrees(n, E)
    if slot.c == 'C3':
        if rng.random() < 0.5:
            # directed version
            Dd = [(a, b) if rng.random() < 0.5 else (b, a) for a, b in E]
            outd = [sum(1 for a, b in Dd if a == i) for i in range(n)]
            ind = [sum(1 for a, b in Dd if b == i) for i in range(n)]
            el = ', '.join(f'{V[a]}→{V[b]}' for a, b in sorted(Dd))
            src = [V[i] for i in range(n) if ind[i] == 0]
            return ret(f'A one-way street system is modelled by a directed graph with edges {el}. Find the in-degree and out-degree of each vertex and state any vertex that cannot be reached from any other.',
                       '; '.join(f'{V[i]}: in {ind[i]}, out {outd[i]}' for i in range(n)) + f'; unreachable: {", ".join(src) if src else "none"}',
                       f'in-degrees (A1), out-degrees (A1); Σ in = Σ out = {len(E)} (R1); vertices with in-degree 0: {", ".join(src) if src else "none"} (A1).', 4, 'numerical')
        seq = sorted(dg, reverse=True)
        return ret(f'A simple connected graph has degree sequence {", ".join(map(str, seq))}. Find the number of edges, the number of edges that must be added to make it complete, and state whether it has an Eulerian circuit.',
                   f'{len(E)}; {n * (n - 1) // 2 - len(E)}; {"yes" if all(x % 2 == 0 for x in dg) else "no"}',
                   f'Σ degrees = {sum(dg)} (M1) ⇒ {len(E)} edges (A1); K{n} has {n * (n - 1) // 2} (A1) ⇒ add {n * (n - 1) // 2 - len(E)} (A1); R1 ' + ('all degrees even' if all(x % 2 == 0 for x in dg) else 'some degrees are odd') + '.', 5, 'numerical')
    # C4: complete/bipartite and planning
    k = rng.randint(5, 9)
    teams, act = pick(rng, [('teams in a round-robin tournament', 'games can be played'), ('delegates who each shake hands with every other delegate', 'handshakes can take place'), ('cities each linked to every other by a direct flight', 'of these routes can be inspected')])
    games = k * (k - 1) // 2
    days = rng.randint(2, 4)
    return ret(f'There are {k} {teams}. (a) Model the situation as a graph and state its name. (b) Find the number of edges. (c) Find the degree of each vertex and verify the handshaking lemma. (d) Determine whether the graph has an Eulerian circuit. (e) If at most {days} {act} per hour, find the minimum time needed to cover every edge once.',
               f'(a) K{k} (b) {games} (c) {k - 1} (d) {"yes" if (k - 1) % 2 == 0 else "no"} (e) {math.ceil(games / days)} h',
               f'(a) complete graph K{k} (A1). (b) {k}×{k - 1}/2 (M1) = {games} (A1). (c) {k - 1} each, sum {k * (k - 1)} = 2 × {games} (R1). (d) R1 degree {k - 1} is {"even" if (k - 1) % 2 == 0 else "odd"}. (e) ⌈{games}/{days}⌉ = {math.ceil(games / days)} (A1).', 7, 'multi_step', gap='G5')


# =============================================================================================
# ch06 Introduction to differentiation
# =============================================================================================
def pterms(terms, var='x'):
    """[(coef, power)] -> text, powers may be negative; coef int/Fraction/float."""
    out = []
    for cf, p in terms:
        if cf == 0:
            continue
        mag = abs(cf)
        if isinstance(mag, Fr):
            ms = frs(mag) if mag.denominator == 1 else f'({frs(mag)})'
            ms = '' if mag == 1 and p != 0 else ms
        else:
            ms = '' if mag == 1 and p != 0 else _num(mag)
        core = ms + ((var + (sup(p) if p != 1 else '')) if p != 0 else '')
        if not out:
            out.append((MINUS if cf < 0 else '') + core)
        else:
            out.append((f'{MINUS} ' if cf < 0 else '+ ') + core)
    return ' '.join(out) if out else '0'


def dterms(terms):
    return [(cf * p, p - 1) for cf, p in terms if p != 0]


def evt(terms, x):
    return sum(float(cf) * x ** p for cf, p in terms)


def rterms(rng, neg=False, k=None):
    k = k or rng.randint(2, 3)
    pw = rng.sample([4, 3, 2, 1] + ([-1, -2] if neg else []), k)
    pw = sorted(pw, reverse=True)
    t = [(rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]), p) for p in pw]
    if rng.random() < 0.6:
        t.append((rng.randint(-9, 12), 0))
    return t


R.facts('ch06-st1', F(
    terms=[('derivative', "f′(x), the gradient of the tangent to y = f(x) at x, and the instantaneous rate of change of f with respect to x"),
           ('limit', 'the value that an expression approaches as the variable approaches a given value, e.g. the chord gradient as h → 0'),
           ('gradient of a chord', '(f(x + h) − f(x))/h, the average rate of change of f between x and x + h'),
           ('dy/dx', 'Leibniz notation for the derivative of y with respect to x')],
    facts=[('As h → 0, the gradient of the chord from (x, f(x)) to (x + h, f(x + h)) approaches…', "the gradient of the tangent at x, f′(x)", ['zero', 'f(x)', 'infinity'], 'Definition of the derivative.'),
           ('If V is volume in litres and t is time in minutes, the units of dV/dt are…', 'litres per minute', ['litres', 'minutes per litre', 'litres × minutes'], 'Rate of change of V with respect to t.'),
           ('If f′(3) = −2, then at x = 3 the graph of f is…', 'decreasing', ['increasing', 'at a maximum', 'at a minimum'], 'Negative gradient.')],
    why=[('Explain why the derivative is described as an instantaneous rate of change.', 'It is the limit of average rates of change (chord gradients) over smaller and smaller intervals h → 0, so it measures the rate at a single instant.'),
         ('Explain why we cannot simply put h = 0 in (f(x + h) − f(x))/h.', 'It gives 0/0, which is undefined; instead we simplify or look at the values as h approaches 0.')],
    misc=[('If s(t) is distance, s′(2) = 5 means the object has travelled 5 m after 2 s.', 's′(2) = 5 means that at t = 2 the distance is increasing at 5 m s⁻¹ (the speed), not the distance travelled.')],
))


@R.add('ch06-st1', ALL, (1, 5), 'short')
def limit_core(rng, slot):
    c, d = slot.c, slot.d
    t = rterms(rng, k=2)
    x0 = rng.randint(-3, 4)
    f = lambda x: evt(t, x)
    fp = evt(dterms(t), x0)
    if c == 'C1':
        if d <= 1:
            q = pick(rng, [('V', 'litres', 't', 'minutes'), ('h', 'metres', 't', 'seconds'), ('C', 'dollars', 'n', 'items'), ('P', 'people', 't', 'years'), ('T', '°C', 't', 'hours')])
            return mcq(rng, f'{q[0]} is measured in {q[1]} and {q[2]} in {q[3]}. What are the units of d{q[0]}/d{q[2]}?', f'{q[1]} per {q[3][:-1] if q[3].endswith("s") and q[3] != "items" else q[3]}'.replace('items per items', 'dollars per item'),
                       [f'{q[1]}', f'{q[3]} per {q[1]}', f'{q[1]} × {q[3]}'], 'A derivative is a rate: units of the numerator per unit of the denominator.')
        hs = [0.1, 0.01, 0.001]
        g = [(f(x0 + h) - f(x0)) / h for h in hs]
        return ret(f'For f(x) = {pterms(t)}, the gradients of chords from x = {m(x0)} to x = {m(x0)} + h are {", ".join(m(_num(round(v, 6))) for v in g)} for h = 0.1, 0.01, 0.001. Write down the value of f′({m(x0)}) suggested by these values.', m(_num(fp)),
                   f'The chord gradients approach {m(_num(fp))} as h → 0 (A1); f′({m(x0)}) = {m(_num(fp))} (A1).', 2)
    if c == 'C2':
        h = rng.choice([1, 0.5, 2])
        g = (f(x0 + h) - f(x0)) / h
        return ret(f'{name(rng)} estimates the gradient of y = {pterms(t)} at x = {m(x0)} using the chord to x = {m(_num(x0 + h))} and gets {sf(g, 4)}. Explain why this is only an estimate and how to improve it.', f'f′({m(x0)}) = {m(_num(fp))}',
                   f'R1 the chord gives the average rate over an interval of width {_num(h)}, not the gradient at a point; R1 use smaller h, the chord gradient approaches the tangent gradient as h → 0; A1 the limit is {m(_num(fp))}.', 3, 'explain')
    if c == 'C3':
        hs = [1, 0.1, 0.01]
        g = [(f(x0 + h) - f(x0)) / h for h in hs]
        gs = ', '.join(m(_num(round(v, 6))) for v in g)
        return ret(f'For f(x) = {pterms(t)}, find the gradient of the chord from x = {m(x0)} to x = {m(x0)} + h for h = 1, 0.1 and 0.01, and hence estimate f′({m(x0)}).', f'{gs}; f′({m(x0)}) ≈ {m(_num(fp))}',
                   f'f({m(x0)}) = {m(_num(f(x0)))} (A1); (f({m(x0)} + h) − f({m(x0)}))/h (M1): {gs} (A1); limit {m(_num(fp))} (A1).', 4, 'numerical')
    a, b = rng.randint(20, 90), rng.choice([2, 3, 4, 5])
    T0 = rng.randint(70, 95)
    k = round(rng.uniform(0.04, 0.12), 3)
    t1 = rng.randint(3, 15)
    Tf = lambda tt: 20 + (T0 - 20) * math.exp(-k * tt)
    rate = (Tf(t1 + 0.001) - Tf(t1 - 0.001)) / 0.002
    avg = (Tf(t1) - Tf(0)) / t1
    return ret(f'The temperature of a cup of coffee is T(t) = 20 + {T0 - 20}e^(−{k}t) °C, t minutes after it is poured. (a) Find the average rate of change of T over the first {t1} minutes. (b) Use technology to find T′({t1}). (c) State the units of T′(t) and interpret your answer to (b). '
               f'(d) Explain why the answers to (a) and (b) differ. (e) State what happens to T′(t) as t becomes large.',
               f'(a) {sf(avg)} °C min⁻¹ (b) {sf(rate)} °C min⁻¹ (e) T′(t) → 0',
               f'(a) (T({t1}) − T(0))/{t1} (M1) = {sf(avg)} (A1). (b) {sf(rate)} (A1). (c) °C per minute; at t = {t1} the coffee is cooling at {sf(-rate)} °C per minute (R1). (d) R1 (a) is an average over an interval, (b) instantaneous; the cooling slows down. (e) A1 approaches 0 as T → 20 °C.', 7, 'multi_step', gap='G5')


R.facts('ch06-st2', F(
    terms=[('increasing function', 'a function for which f′(x) > 0 on an interval: y increases as x increases'),
           ('decreasing function', 'a function for which f′(x) < 0 on an interval: y decreases as x increases'),
           ('stationary point', 'a point where f′(x) = 0; the tangent is horizontal')],
    facts=[('If f′(x) = 3x² + 1, then f is…', 'increasing for all x', ['decreasing for all x', 'increasing only for x > 0', 'stationary at x = 0'], '3x² + 1 > 0 always.'),
           ('f′(x) = (x − 1)(x − 4). On which interval is f decreasing?', '1 < x < 4', ['x < 1', 'x > 4', 'x < 1 or x > 4'], 'The product is negative between the roots.'),
           ('A company\'s profit P(t) has P′(t) < 0 for 0 < t < 2. This means…', 'profit is falling during that time', ['profit is negative', 'the company makes a loss', 'profit is constant'], 'A negative derivative means decreasing.')],
    why=[('Explain how the sign of f′(x) tells you whether f is increasing or decreasing.', 'f′(x) is the gradient of the tangent; a positive gradient means the graph rises from left to right (increasing), a negative gradient means it falls.'),
         ('Explain why f(x) = x³ is increasing everywhere even though f′(0) = 0.', 'f′(x) = 3x² ≥ 0 and equals 0 only at the single point x = 0; the function still rises on both sides, so it is increasing throughout.')],
    misc=[('If f(x) is negative then f is decreasing.', 'The sign of f(x) says where the graph is below the axis; increasing/decreasing depends on the sign of f′(x).')],
))


def _cubic_from_roots(rng):
    """f′(x) = 3a(x − p)(x − q) with integer p < q; f(x) = a x³ − (3a/2)(p+q) x² + 3apq x + c with even coefficients."""
    a = rng.choice([1, -1, 2, -2])
    p, q = sorted(rng.sample(range(-4, 6), 2))
    if (p + q) % 2:
        a *= 2 if abs(a) == 1 else 1
    c3 = a
    c2 = Fr(-3 * a * (p + q), 2)
    c1 = 3 * a * p * q
    c0 = rng.randint(-10, 10)
    return [(c3, 3), (c2, 2), (c1, 1), (c0, 0)], a, p, q


@R.add('ch06-st2', ALL, (1, 5), 'short')
def incdec_core(rng, slot):
    c, d = slot.c, slot.d
    t, a, p, q = _cubic_from_roots(rng)
    fs = pterms(t)
    dt = dterms(t)
    dec = f'{m(p)} < x < {m(q)}' if a > 0 else f'x < {m(p)} or x > {m(q)}'
    inc = f'x < {m(p)} or x > {m(q)}' if a > 0 else f'{m(p)} < x < {m(q)}'
    if c == 'C1':
        x0 = rng.randint(-5, 6)
        g = evt(dt, x0)
        if g == 0:
            return None
        return mcq(rng, f'For f(x) = {fs}, is f increasing or decreasing at x = {m(x0)}?', 'increasing' if g > 0 else 'decreasing', ['decreasing' if g > 0 else 'increasing', 'stationary', 'cannot be determined'], f"f′({m(x0)}) = {m(_num(g))} {'> 0' if g > 0 else '< 0'}.")
    if c == 'C2':
        x0 = rng.randint(-5, 6)
        fv_ = evt(t, x0)
        g = evt(dt, x0)
        if g == 0 or (fv_ > 0) == (g > 0):
            return None
        return ret(f'For f(x) = {fs}, {name(rng)} notices that f({m(x0)}) = {m(_num(fv_))} and claims that f is therefore {"increasing" if fv_ > 0 else "decreasing"} at x = {m(x0)}. Explain the error.', f'f′({m(x0)}) = {m(_num(g))}, so f is {"increasing" if g > 0 else "decreasing"}',
                   f'R1 the sign of f(x) does not determine whether f is increasing; M1 f′(x) = {pterms(dt)}; A1 f′({m(x0)}) = {m(_num(g))} so f is {"increasing" if g > 0 else "decreasing"}.', 3, 'explain')
    if c == 'C3':
        return ret(f'Find the values of x for which f(x) = {fs} is decreasing.', dec,
                   f"f′(x) = {pterms(dt)} (A1) = {m(_num(3 * a))}(x {sgn(-p)})(x {sgn(-q)}) (M1); f′(x) < 0 (M1) for {dec} (A1).".replace('(x + 0)', 'x').replace('(x − 0)', 'x'), 4, 'numerical')
    # C4 context: profit/population model
    sc = rng.choice([10, 100, 1000])
    ctx = pick(rng, [('the change in water level of a reservoir since 1 January (cm)', 't', 'the time in weeks'), ('the profit of a start-up relative to its launch (thousand euros)', 't', 'the time in months'),
                     ('the height of a roller-coaster track relative to the platform (m)', 'x', 'the horizontal distance in tens of metres'), ('the change in a city\'s population since 2000 (thousands)', 't', 'the time in years')])
    if p < 0:
        return None
    return ret(f'Model: {ctx[0]} is f(x) = {fs}, where x is {ctx[2]}, 0 ≤ x ≤ {q + 3}. (a) Find f′(x). (b) Find the values of x where f′(x) = 0. (c) Find the interval(s) where f is increasing. (d) Find the rate of change when x = {q + 2} and interpret it. (e) Explain why the model may not be valid for large x.',
               f'(a) {pterms(dt)} (b) x = {p}, {q} (c) {inc} (within the domain) (d) {m(_num(evt(dt, q + 2)))}',
               f'(a) A1 A1. (b) set f′ = 0 (M1) x = {p}, {q} (A1). (c) sign analysis (M1) {inc} (A1). (d) f′({q + 2}) = {m(_num(evt(dt, q + 2)))} (A1), units per unit x (R1). (e) R1 a cubic grows without bound / becomes negative, which is unrealistic.', 9, 'multi_step', gap='G5')


R.facts('ch06-st3', F(
    terms=[('power rule', 'if f(x) = axⁿ then f′(x) = naxⁿ⁻¹, for any integer n'),
           ('derivative of a constant', 'zero, since the graph of y = c is horizontal'),
           ('sum rule', 'the derivative of a sum is the sum of the derivatives: (f + g)′ = f′ + g′')],
    facts=[('What is the derivative of 5x³?', '15x²', ['15x³', '5x²', '3x²'], 'n a xⁿ⁻¹ = 3 × 5 x².'),
           ('What is the derivative of 4/x²?', '−8x⁻³', ['8x⁻³', '−8x⁻¹', '4x⁻³'], '4x⁻² → −8x⁻³.'),
           ('What is the derivative of 7?', '0', ['7', '7x', '1'], 'Constants have zero gradient.'),
           ('If y = 2x⁴ − 3x, then dy/dx at x = 1 is…', '5', ['−1', '8', '11'], '8x³ − 3 = 5.')],
    why=[('Explain why a term like 6/x must be rewritten before differentiating with the power rule.', 'The power rule applies to axⁿ; 6/x = 6x⁻¹, which then differentiates to −6x⁻².'),
         ('Explain why the derivative of a constant is zero.', 'The graph of y = c is a horizontal line, whose gradient is zero everywhere; a constant does not change as x changes.')],
    misc=[('The derivative of 1/x³ is 1/(3x²).', 'Write 1/x³ = x⁻³; the derivative is −3x⁻⁴ = −3/x⁴.')],
))


@R.add('ch06-st3', ALL, (1, 5), 'short')
def power_core(rng, slot):
    c, d = slot.c, slot.d
    t = rterms(rng, neg=(c != 'C1' or d >= 2))
    dt = dterms(t)
    fs, ds = pterms(t), pterms(dt)
    if c == 'C1':
        if d <= 1:
            cf, p = rng.choice([2, 3, 4, 5, 6, -2, -3]), rng.choice([2, 3, 4, 5, -1, -2])
            wr = [pterms([(cf * p, p)]), pterms([(cf, p - 1)]), pterms([(cf * p, p + 1)])]
            return mcq(rng, f'Differentiate f(x) = {pterms([(cf, p)])}.', pterms([(cf * p, p - 1)]), wr, f'n a xⁿ⁻¹ = {pterms([(cf * p, p - 1)])}.')
        return ret(f'Find f′(x) for f(x) = {fs}.', ds, f'power rule term by term (M1); {ds} (A1 A1).', 3)
    if c == 'C2':
        cf, p = rng.choice([2, 3, 4, 5, 6, 8]), rng.choice([1, 2, 3])
        wrong = f'{cf}/({p}x{sup(p - 1) if p > 2 else ""})' if p > 1 else f'{cf}/1 = {cf}'
        right = pterms([(-cf * p, -p - 1)])
        return ret(f'{name(rng)} differentiates y = {cf}/x{sup(p) if p > 1 else ""} and writes dy/dx = {wrong}. Explain the mistake and find the correct derivative.', right,
                   f'R1 the power rule cannot be applied to the denominator alone; M1 rewrite as {cf}x{sup(-p)}; A1 dy/dx = {right} = −{cf * p}/x{sup(p + 1)}.', 3, 'explain')
    if c == 'C3':
        x0 = rng.choice([1, 2, -1, 3, -2])
        g = evt(dt, x0)
        if rng.random() < 0.5:
            return ret(f'Given y = {fs}, find dy/dx and the gradient of the curve at x = {m(x0)}.', f'{ds}; {m(_num(g))}', f'dy/dx = {ds} (A1 A1); at x = {m(x0)}: {m(_num(g))} (M1 A1).', 4, 'numerical')
        a_, b_ = rng.choice([1, 2, 3]), rng.randint(-6, 6)
        k = rng.randint(-8, 8)
        # f = a x^2 + b x + 1/x?  -> use quadratic so gradient = k solvable
        t2 = [(a_, 2), (b_, 1), (rng.randint(-5, 9), 0)]
        xg = Fr(k - b_, 2 * a_)
        return ret(f'Find the coordinates of the point on the curve y = {pterms(t2)} where the gradient is {m(k)}.', f'({frs(xg)}, {frs(a_ * xg * xg + b_ * xg + t2[2][0])})',
                   f'dy/dx = {pterms(dterms(t2))} (A1); {pterms(dterms(t2))} = {m(k)} (M1) ⇒ x = {frs(xg)} (A1); y = {frs(a_ * xg * xg + b_ * xg + t2[2][0])} (A1).', 4, 'numerical')
    k = rng.choice([200, 400, 500, 800, 1000, 1500])
    a_ = rng.choice([2, 3, 4])
    # cost per unit area: C(x) = a x^2 + k/x
    x0 = rng.randint(2, 8)
    Cp = lambda x: 2 * a_ * x - k / x ** 2
    xs = (k / (2 * a_)) ** (1 / 3)
    return ret(f'The cost (in hundreds of {cur(rng)}) of producing a box with base side x m is modelled by C(x) = {a_}x² + {k}/x, x > 0. (a) Write C(x) in the form axⁿ + bxᵐ. (b) Find C′(x). (c) Find C′({x0}) and interpret its sign. (d) Find the value of x where C′(x) = 0. (e) Explain what this value of x represents for the manufacturer.',
               f'(a) {a_}x² + {k}x⁻¹ (b) {2 * a_}x − {k}x⁻² (c) {sf(Cp(x0))} (d) {sf(xs)}',
               f'(a) A1. (b) A1 A1. (c) {2 * a_}({x0}) − {k}/{x0}² = {sf(Cp(x0))} (A1); R1 {"cost decreasing as x increases" if Cp(x0) < 0 else "cost increasing as x increases"}. (d) {2 * a_}x³ = {k} (M1) x = {sf(xs)} (A1). (e) R1 the base side giving minimum cost.', 8, 'multi_step', gap='G5')


R.facts('ch06-st4', F(
    terms=[('tangent to a curve', 'the straight line that touches the curve at a point and has gradient f′(a) there'),
           ('normal to a curve', 'the line through the point of contact perpendicular to the tangent, with gradient −1/f′(a)'),
           ('equation of the tangent', 'y − f(a) = f′(a)(x − a)')],
    facts=[('The gradient of the tangent at a point is 4. What is the gradient of the normal?', '−1/4', ['4', '−4', '1/4'], 'Negative reciprocal.'),
           ('At a point where f′(a) = 0, the normal is…', 'a vertical line x = a', ['horizontal', 'y = x', 'undefined everywhere'], 'Perpendicular to a horizontal tangent.'),
           ('The tangent to y = x² at (3, 9) has equation…', 'y = 6x − 9', ['y = 6x + 9', 'y = 2x + 3', 'y = 3x'], 'Gradient 6; 9 = 18 + c.')],
    why=[('Explain why the gradient of the normal is −1/f′(a).', 'The normal is perpendicular to the tangent, and perpendicular gradients multiply to −1.'),
         ('Explain why the tangent line gives a good approximation to the curve near the point of contact.', 'It has the same value and the same gradient as the curve at that point, so for small changes in x the curve and line are very close.')],
    misc=[('The tangent at x = 2 to y = x³ is y = 3x².', 'The tangent is a straight line: gradient f′(2) = 12 through (2, 8), so y = 12x − 16.')],
))


@R.add('ch06-st4', ALL, (1, 5), 'short')
def tangent_core(rng, slot):
    c, d = slot.c, slot.d
    t = rterms(rng, neg=(rng.random() < 0.3), k=2)
    dt = dterms(t)
    a = rng.choice([1, 2, -1, 3, -2])
    ya, g = evt(t, a), evt(dt, a)
    if g == 0:
        return None
    ya, g = Fr(ya).limit_denominator(1000), Fr(g).limit_denominator(1000)
    tan = Y1.line_eq(g, ya - g * a)
    nor = Y1.line_eq(-1 / g, ya + a / g)
    fs = pterms(t)
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'The gradient of y = {fs} at x = {m(a)} is {frs(g)}. What is the gradient of the normal at this point?', frs(-1 / g), [frs(g), frs(-g), frs(1 / g)] if abs(g) != 1 else [frs(g * 2), frs(-g * 2), '0'], 'Normal gradient = −1/f′(a).')
        return ret(f'Find the equation of the tangent to y = {fs} at the point where x = {m(a)}.', tan, f'y = {frs(ya)} (A1); dy/dx = {pterms(dt)} = {frs(g)} at x = {m(a)} (M1 A1); {tan} (A1).', 4)
    if c == 'C2':
        return ret(f'{name(rng)} finds the normal to y = {fs} at x = {m(a)} using gradient {frs(-g)}. Explain the error and find the correct gradient of the normal.', frs(-1 / g),
                   f'R1 the normal is perpendicular to the tangent, so its gradient is the negative reciprocal, not the negative; M1 tangent gradient {frs(g)}; A1 −1/({frs(g)}) = {frs(-1 / g)}.', 3, 'explain')
    if c == 'C3':
        return ret(f'Find the equation of the normal to the curve y = {fs} at the point where x = {m(a)}, giving your answer in the form y = mx + c.', nor,
                   f'point ({m(a)}, {frs(ya)}) (A1); f′({m(a)}) = {frs(g)} (M1 A1); normal gradient {frs(-1 / g)} (A1); {nor} (A1).', 5, 'numerical')
    c0 = ya - g * a
    if c0 == 0:
        return None
    xi = -c0 / g
    area = abs(float(c0) * float(xi)) / 2
    return ret(f'A ski slope profile is modelled by y = {fs} (units 10 m). (a) Find dy/dx. (b) Find the equation of the tangent at x = {m(a)}. (c) Find where this tangent crosses the x- and y-axes. (d) Find the area of the triangle formed by the tangent and the coordinate axes. (e) Find the equation of the normal at x = {m(a)}.',
               f'(a) {pterms(dt)} (b) {tan} (c) ({frs(xi)}, 0), (0, {frs(c0)}) (d) {sf(area)} (e) {nor}',
               f'(a) A1. (b) M1 A1. (c) A1 A1. (d) ½ × |{frs(xi)}| × |{frs(c0)}| (M1) = {sf(area)} (A1). (e) gradient {frs(-1 / g)} (M1) {nor} (A1).', 9, 'multi_step', gap='G5')


@R.add('ch06-st4', 'C4', (2, 5), 'multi_step')
def tangent_c4(rng, slot):
    v = rng.randrange(3)
    a2, b2, c2 = rng.choice([1, 2, -1, 3, Fr(1, 2)]), rng.randint(-6, 6), rng.randint(-8, 10)
    t = [(a2, 2), (b2, 1), (c2, 0)]
    fs = pterms(t)
    if v == 0:
        a = rng.choice([1, 2, 3, -1, -2])
        g = 2 * a2 * a + b2
        if g == 0:
            return None
        ya = a2 * a * a + b2 * a + c2
        ng = Fr(-1, 1) / g
        # normal y = ng(x − a) + ya meets curve: a2 x² + (b2 − ng) x + (c2 + ng a − ya) = 0, one root is a
        other = Fr(-(b2 - ng), a2) - a
        yo = a2 * other * other + b2 * other + c2
        ctx = pick(rng, ['the cross-section of a satellite dish', 'the arch of a footbridge', 'the profile of a skateboard ramp', 'a water fountain jet'])
        return ret(f'The curve y = {fs} models {ctx}. (a) Find dy/dx. (b) Find the gradient of the curve at P where x = {m(a)}. (c) Find the equation of the normal to the curve at P. (d) Find the coordinates of the point Q where the normal meets the curve again. (e) Find the distance PQ.',
                   f'(b) {frs(g)} (c) {Y1.line_eq(ng, ya - ng * a)} (d) ({frs(other)}, {frs(yo)}) (e) {sf(math.hypot(float(other - a), float(yo - ya)))}',
                   f'(a) {pterms(dterms(t))} (A1). (b) A1. (c) gradient −1/({frs(g)}) (M1) equation (A1). (d) solve normal = curve (M1) x = {frs(other)} (A1), y = {frs(yo)} (A1). (e) distance formula (M1) {sf(math.hypot(float(other - a), float(yo - ya)))} (A1).', 9, 'multi_step', gap='G5')
    if v == 1:
        k = rng.randint(-6, 8)
        x1 = Fr(k - b2, 2 * a2)
        y1 = a2 * x1 * x1 + b2 * x1 + c2
        cc = y1 - k * x1
        q = rng.randint(-5, 5)
        road = pick(rng, ['A straight road', 'A railway line', 'A zip-line cable', 'A laser beam'])
        return ret(f'{road} is to touch the curved edge of a lake modelled by y = {fs} and must be parallel to the line y = {m(k)}x {sgn(q)}. (a) Find dy/dx. (b) Find the coordinates of the point where the gradient of the curve is {m(k)}. (c) Find the equation of the tangent at this point. (d) Explain why the tangent and the line y = {m(k)}x {sgn(q)} never meet. (e) Find the equation of the normal at the same point.',
                   f'(b) ({frs(x1)}, {frs(y1)}) (c) {Y1.line_eq(k, cc)} (e) {Y1.line_eq(Fr(-1, k), y1 + x1 / k) if k else "x = " + frs(x1)}',
                   f'(a) {pterms(dterms(t))} (A1). (b) set equal to {m(k)} (M1) x = {frs(x1)} (A1) y = {frs(y1)} (A1). (c) {Y1.line_eq(k, cc)} (A1). (d) R1 same gradient, different intercept ⇒ parallel. (e) gradient {frs(Fr(-1, k)) if k else "undefined"} (M1) (A1).', 8, 'multi_step', gap='G5')
    # tangent through an external point / tangent linear approximation
    a = rng.randint(1, 5)
    h_ = rng.choice([0.1, 0.2, 0.05, -0.1])
    g = 2 * a2 * a + b2
    ya = a2 * a * a + b2 * a + c2
    approx = float(ya) + float(g) * h_
    exact = evt(t, a + h_)
    unit = pick(rng, [('profit (thousand dollars)', 'number of units produced (hundreds)'), ('vertical displacement of a spring (cm)', 'time (s)'), ('temperature (°C)', 'time (hours after midnight)'), ('net cash flow (million yen)', 'time (years)')])
    return ret(f'The {unit[0]} is modelled by y = {fs}, where x is the {unit[1]}. (a) Find dy/dx and its value at x = {a}. (b) Find the equation of the tangent at x = {a}. (c) Use the tangent to estimate y when x = {_num(a + h_)}. (d) Find the exact value of y at x = {_num(a + h_)} and the percentage error of the estimate. (e) Explain why the estimate is close.',
               f'(a) {pterms(dterms(t))}; {frs(g)} (b) {Y1.line_eq(g, ya - g * a)} (c) {m(_num(approx))} (d) {m(_num(exact))}; {sf(abs(approx - exact) / abs(exact) * 100) if exact else "–"}%',
               f'(a) A1 A1. (b) M1 A1. (c) substitute (M1) {m(_num(approx))} (A1). (d) {m(_num(exact))} (A1); |approx − exact|/exact × 100 (M1) (A1). (e) R1 near the point of contact the tangent and the curve almost coincide (small h).', 10, 'multi_step', gap='G5')


# =============================================================================================
# ch07 Further differentiation
# =============================================================================================
def _lin(rng, allow0=True):
    a = rng.choice([1, 2, 3, 4, 5, -2, -3])
    b = rng.choice([0, 1, 2, -1, 3, -4, 5]) if allow0 else rng.choice([1, 2, -1, 3, -4, 5])
    return a * x_ + b


def _inner_fn(rng):
    """a simple function u(x) for chain/product/quotient, sympy expr."""
    k = rng.randrange(6)
    a = rng.choice([1, 2, 3, -2, 4])
    if k == 0:
        return sp.sin(a * x_)
    if k == 1:
        return sp.cos(a * x_)
    if k == 2:
        return sp.exp(a * x_)
    if k == 3:
        return sp.log(_lin(rng, False) if rng.random() < 0.5 else x_)
    if k == 4:
        return x_ ** rng.choice([2, 3, 4])
    return (_lin(rng)) ** rng.choice([2, 3, 4, -1])


def dval(expr, a):
    v = float(sp.N(sp.diff(expr, x_).subs(x_, a)))
    return v


def ok_at(expr, a):
    try:
        v = complex(sp.N(expr.subs(x_, a)))
        dv = complex(sp.N(sp.diff(expr, x_).subs(x_, a)))
        return abs(v.imag) < 1e-12 and abs(dv.imag) < 1e-12 and math.isfinite(v.real) and math.isfinite(dv.real)
    except Exception:
        return False


def dshow(expr):
    d = sp.diff(expr, x_)
    a, b = pe(sp.factor(d)), pe(sp.expand(d)) if not d.has(sp.exp, sp.sin, sp.cos, sp.log) else pe(d)
    return min((a, b, pe(d)), key=len)


R.facts('ch07-st1', F(
    terms=[('chain rule', 'if y = g(u) and u = f(x), then dy/dx = (dy/du)(du/dx)'),
           ('product rule', 'if y = uv, then dy/dx = u(dv/dx) + v(du/dx)'),
           ('quotient rule', 'if y = u/v, then dy/dx = (v(du/dx) − u(dv/dx))/v²'),
           ('derivative of eˣ', 'eˣ: the exponential function is its own derivative'),
           ('derivative of ln x', '1/x, for x > 0')],
    facts=[('What is the derivative of sin(3x)?', '3cos(3x)', ['cos(3x)', '−3cos(3x)', '3sin(3x)'], 'Chain rule: cos(3x) × 3.'),
           ('What is the derivative of e^(5x)?', '5e^(5x)', ['e^(5x)', '5xe^(5x − 1)', 'e^(5x)/5'], 'Chain rule.'),
           ('What is the derivative of ln(2x)?', '1/x', ['1/(2x)', '2/x', 'ln 2'], '2/(2x) = 1/x.'),
           ('What is the derivative of tan x?', '1/cos²x', ['sec x', '−1/cos²x', 'sin x/cos x'], 'Formula booklet: sec²x.'),
           ('What is the derivative of √x?', '1/(2√x)', ['2√x', '√x/2', '−1/(2√x)'], 'x^(1/2) → ½x^(−1/2).')],
    why=[('Explain why the derivative of a product is not the product of the derivatives.', 'When both factors change, the change in uv comes from u changing while v is fixed and v changing while u is fixed; this gives u′v + uv′, e.g. (x · x)′ = 2x, not 1 × 1 = 1.'),
         ('Explain when the chain rule is needed.', 'Whenever a function is applied to an expression other than x itself (a composite function such as sin(3x²) or e^(2x+1)); the derivative of the outer function is multiplied by the derivative of the inner one.')],
    misc=[('The derivative of cos x is sin x.', 'd/dx(cos x) = −sin x.'),
          ('The derivative of e^(x²) is e^(x²).', 'By the chain rule it is 2x e^(x²).')],
))


@R.add('ch07-st1', ALL, (1, 5), 'short')
def rules_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        u = _inner_fn(rng)
        if rng.random() < 0.5:
            a_ = rng.choice([2, 3, 4, 5, -2])
            u2 = u.subs(x_, a_ * x_) if not u.is_Pow else u
            e = u2
        else:
            e = u
        if not ok_at(e, 1.0) and not ok_at(e, 2.0):
            return None
        return ret(f'Differentiate y = {pe(e)} with respect to x.', dshow(e), f'standard derivative (A1) with chain rule factor where needed (M1): dy/dx = {dshow(e)} (A1).', 3)
    if c == 'C2':
        u, v = _inner_fn(rng), x_ ** rng.choice([2, 3])
        if u.is_Pow:
            return None
        e = v * u
        wrong = sp.diff(u, x_) * sp.diff(v, x_)
        return ret(f'{name(rng)} differentiates y = {pe(e)} and writes dy/dx = {pe(wrong)}. Explain the error and find the correct derivative.', dshow(e),
                   f'R1 the derivative of a product is not the product of the derivatives; M1 product rule u′v + uv′ with u = {pe(v)}, v = {pe(u)}; A1 {dshow(e)}.', 3, 'explain')
    a = rng.choice([1, 2, 0.5, 3])
    if c == 'C3':
        kind = rng.choice(['product', 'quotient', 'chain'])
        u, v = _inner_fn(rng), _inner_fn(rng)
        if kind == 'product':
            e = u * v
        elif kind == 'quotient':
            e = u / (v if not v.has(sp.sin, sp.cos) else (x_ ** 2 + rng.randint(1, 4)))
        else:
            e = sp.exp(rng.choice([1, -1, 2]) * x_ ** 2) if rng.random() < 0.3 else sp.sqrt(rng.choice([1, 2, 3]) * x_ ** 2 + rng.randint(1, 9))
        if e.is_number or not ok_at(e, a):
            return None
        dv = dval(e, a)
        return ret(f'Given f(x) = {pe(e)}, find f′(x) and the value of f′({_num(a)}).', f"f′(x) = {dshow(e)}; f′({_num(a)}) = {sf(dv)}",
                   f'{kind} rule (M1) correct terms (A1 A1); f′(x) = {dshow(e)}; substitute x = {_num(a)} (M1) ⇒ {sf(dv)} (A1).', 5, 'numerical')
    A = rng.randint(5, 40)
    k = round(rng.uniform(0.1, 0.8), 2)
    t = sp.Symbol('t')
    C = A * t * sp.exp(-k * t)
    t1 = rng.randint(1, 6)
    dC = sp.diff(C, t)
    tm = 1 / k
    v1 = float(dC.subs(t, t1))
    drug = pick(rng, ['an antibiotic', 'a painkiller', 'caffeine', 'an anaesthetic'])
    return ret(f'The concentration of {drug} in the blood t hours after a dose is C(t) = {A}te^(−{k}t) mg L⁻¹. (a) Use the product rule to show that C′(t) = {A}e^(−{k}t)(1 − {k}t). (b) Find the rate of change of concentration at t = {t1} and interpret its sign. (c) Find the time at which the concentration is greatest. (d) Find the maximum concentration. (e) Explain why C′(t) → 0 as t → ∞.',
               f'(b) {sf(v1)} mg L⁻¹ h⁻¹ (c) t = {sf(tm)} h (d) {sf(A * tm * math.exp(-1))} mg L⁻¹',
               f'(a) u = {A}t, v = e^(−{k}t) (M1); {A}e^(−{k}t) − {sf(A * k)}te^(−{k}t) (A1) AG. (b) {sf(v1)} (A1); R1 {"increasing" if v1 > 0 else "decreasing"}. (c) 1 − {k}t = 0 (M1) t = {sf(tm)} (A1). (d) C({sf(tm)}) = {sf(A * tm * math.exp(-1))} (A1). (e) R1 the exponential factor tends to 0 faster than t grows.', 9, 'multi_step', gap='G5')


R.facts('ch07-st2', F(
    terms=[('related rates', 'rates of change of connected quantities, linked by the chain rule, e.g. dV/dt = (dV/dr)(dr/dt)'),
           ('rate of change with respect to time', 'the derivative d/dt of a quantity, measured in units per unit time')],
    facts=[('The radius of a circle grows at 2 cm s⁻¹. When r = 5 cm, how fast is the area growing?', '20π cm² s⁻¹', ['10π cm² s⁻¹', '25π cm² s⁻¹', '4π cm² s⁻¹'], 'dA/dt = 2πr × dr/dt.'),
           ('If V = x³ and dx/dt = 0.1, then dV/dt = …', '0.3x²', ['3x²', '0.1x³', '0.3x'], 'Chain rule.'),
           ('Which equation links the rates for a sphere of radius r?', 'dV/dt = 4πr² dr/dt', ['dV/dt = (4/3)πr³ dr/dt', 'dV/dt = 4πr dr/dt', 'dV/dt = 2πr dr/dt'], 'dV/dr = 4πr².')],
    why=[('Explain why the chain rule is the key step in related-rates problems.', 'The quantity whose rate is wanted is a function of another variable, which itself changes with time; dy/dt = (dy/dx)(dx/dt) connects the two rates.'),
         ('Explain why the rate at which the area of a ripple grows increases even if its radius grows at a constant rate.', 'dA/dt = 2πr dr/dt; with dr/dt constant, dA/dt is proportional to r, so it increases as the ripple gets bigger.')],
    misc=[('If the radius of a balloon increases at 1 cm s⁻¹, its volume increases at 1 cm³ s⁻¹.', 'dV/dt = 4πr² dr/dt, which depends on r; at r = 10 cm it is 400π ≈ 1260 cm³ s⁻¹.')],
))

RR = [
    ('circle', 'A circular oil spill', 'radius', 'r', 'cm', 'area', 'A = πr²', lambda r: math.pi * r * r, lambda r: 2 * math.pi * r, 'cm²'),
    ('sphere', 'A spherical balloon is being inflated;', 'radius', 'r', 'cm', 'volume', 'V = (4/3)πr³', lambda r: 4 / 3 * math.pi * r ** 3, lambda r: 4 * math.pi * r * r, 'cm³'),
    ('cube', 'A cube of ice is melting;', 'edge', 'x', 'cm', 'volume', 'V = x³', lambda r: r ** 3, lambda r: 3 * r * r, 'cm³'),
    ('square', 'A square solar panel array is being extended;', 'side', 'x', 'm', 'area', 'A = x²', lambda r: r * r, lambda r: 2 * r, 'm²'),
    ('sphereS', 'A spherical snowball is melting;', 'radius', 'r', 'cm', 'surface area', 'S = 4πr²', lambda r: 4 * math.pi * r * r, lambda r: 8 * math.pi * r, 'cm²'),
]


@R.add('ch07-st2', ALL, (1, 5), 'short')
def rates_core(rng, slot):
    c, d = slot.c, slot.d
    kind, intro, lname, lv, lu, qname, formula, Q, dQ, qu = pick(rng, RR)
    r0 = rng.randint(2, 30)
    dr = round(rng.uniform(0.1, 3), 2) * (-1 if 'melting' in intro else 1)
    dq = dQ(r0) * dr
    if c == 'C1':
        return ret(f'{intro} its {lname} {lv} {"decreases" if dr < 0 else "increases"} at {_num(abs(dr))} {lu} per second. Find the rate of change of its {qname} when {lv} = {r0} {lu}.', f'{sf(dq)} {qu} s⁻¹',
                   f'{formula} ⇒ d{formula[0]}/d{lv} = … (A1); d{formula[0]}/dt = d{formula[0]}/d{lv} × d{lv}/dt (M1) = {sf(dQ(r0))} × ({m(_num(dr))}) = {sf(dq)} {qu} s⁻¹ (A1).', 3)
    if c == 'C2':
        r1 = r0 * 2
        return ret(f'{intro} its {lname} changes at a constant rate of {_num(abs(dr))} {lu} s⁻¹. Explain why its {qname} does not change at a constant rate, comparing {lv} = {r0} and {lv} = {r1}.', f'{sf(abs(dq))} vs {sf(abs(dQ(r1) * dr))} {qu} s⁻¹',
                   f'R1 d{formula[0]}/dt = (d{formula[0]}/d{lv})(d{lv}/dt) and d{formula[0]}/d{lv} depends on {lv}; A1 at {lv} = {r0}: {sf(abs(dq))}; A1 at {lv} = {r1}: {sf(abs(dQ(r1) * dr))} {qu} s⁻¹.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            rate = round(rng.uniform(5, 200), 1)
            drn = rate / dQ(r0)
            return ret(f'{intro} its {qname} {"decreases" if dr < 0 else "increases"} at {_num(rate)} {qu} s⁻¹. Find the rate of change of its {lname} when {lv} = {r0} {lu}.', f'{sf(drn * (-1 if dr < 0 else 1))} {lu} s⁻¹',
                       f'{formula} (A1); d{formula[0]}/d{lv} = {sf(dQ(r0))} at {lv} = {r0} (A1); d{lv}/dt = {"−" if dr < 0 else ""}{_num(rate)}/{sf(dQ(r0))} (M1) = {sf(drn * (-1 if dr < 0 else 1))} (A1).', 4, 'numerical')
        L = rng.randint(5, 13)
        x0 = rng.randint(1, L - 1)
        y0 = math.sqrt(L * L - x0 * x0)
        vx = round(rng.uniform(0.2, 1.5), 1)
        vy = -x0 * vx / y0
        return ret(f'A ladder of length {L} m leans against a vertical wall. Its foot slides away from the wall at {vx} m s⁻¹. Find the rate at which the top slides down the wall when the foot is {x0} m from the wall.', f'{sf(-vy)} m s⁻¹ (downwards)',
                   f'x² + y² = {L * L} (M1); 2x dx/dt + 2y dy/dt = 0 (M1 A1); y = {sf(y0)} (A1); dy/dt = −{x0} × {vx}/{sf(y0)} = {sf(vy)} m s⁻¹ (A1).', 5, 'numerical')
    # cone tank
    R_, H = rng.randint(2, 6), rng.randint(5, 15)
    q = round(rng.uniform(0.2, 3), 1)
    h0 = rng.randint(1, H - 1)
    # V = (1/3)π (R h/H)^2 h = π R² h³/(3H²)
    dVdh = math.pi * R_ * R_ * h0 * h0 / (H * H)
    dh = q / dVdh
    r_ = R_ * h0 / H
    return ret(f'Water is poured at {q} m³ per minute into a conical tank with vertex downwards, radius {R_} m at the top and depth {H} m. (a) Show that when the depth of water is h, the radius of the surface is r = ({frs(Fr(R_, H))})h. (b) Show that V = ({frs(Fr(R_ * R_, 3 * H * H))})πh³. (c) Find dV/dh. (d) Find the rate at which the depth is increasing when h = {h0} m. (e) Find the rate at which the area of the water surface is increasing at that moment.',
               f'(c) ({frs(Fr(R_ * R_, H * H))})πh² (d) {sf(dh)} m min⁻¹ (e) {sf(2 * math.pi * r_ * R_ / H * dh)} m² min⁻¹',
               f'(a) similar triangles r/h = {R_}/{H} (R1). (b) V = ⅓πr²h (M1) AG. (c) A1. (d) dh/dt = (dV/dt)/(dV/dh) (M1) = {q}/{sf(dVdh)} = {sf(dh)} (A1). (e) A = πr² = ({frs(Fr(R_ * R_, H * H))})πh², dA/dt = (dA/dh)(dh/dt) (M1) = {sf(2 * math.pi * r_ * R_ / H * dh)} (A1).', 9, 'multi_step', gap='G5')


R.facts('ch07-st3', F(
    terms=[('second derivative', "f″(x) or d²y/dx², the derivative of f′(x): the rate of change of the gradient"),
           ('concave up', "a section of a curve where f″(x) > 0: the gradient is increasing (the curve bends upwards)"),
           ('concave down', "a section of a curve where f″(x) < 0: the gradient is decreasing"),
           ('point of inflection', "a point where the concavity changes; f″(x) = 0 and f″ changes sign")],
    facts=[("At a stationary point f′(a) = 0 and f″(a) = 6. The point is…", 'a local minimum', ['a local maximum', 'a point of inflection', 'impossible to classify'], 'Concave up at a stationary point.'),
           ("For f(x) = x³, what is f″(x)?", '6x', ['3x²', '6', 'x'], 'Differentiate twice.'),
           ("f″(a) = 0 at x = a. Which statement is true?", 'it may or may not be a point of inflection', ['it is always a point of inflection', 'it is a maximum', 'it is a minimum'], 'f″ must change sign; e.g. x⁴ at 0.')],
    why=[("Explain how the second derivative can be used to classify a stationary point.", "If f′(a) = 0 and f″(a) > 0 the gradient is increasing through zero, so the point is a minimum; if f″(a) < 0 it is a maximum; if f″(a) = 0 the test is inconclusive."),
         ('Explain what a point of inflection means for the rate of spread of a disease.', 'Before the inflection the number of cases grows faster and faster (concave up); after it the growth slows (concave down); the inflection is where the rate of increase is greatest.')],
    misc=[("If f″(2) = 0 then (2, f(2)) is a point of inflection.", "f″ must also change sign at x = 2; for f(x) = (x − 2)⁴, f″(2) = 0 but there is a minimum, not an inflection.")],
))


@R.add('ch07-st3', ALL, (1, 5), 'short')
def second_core(rng, slot):
    c, d = slot.c, slot.d
    t, a, p, q = _cubic_from_roots(rng)
    d1, d2 = dterms(t), dterms(dterms(t))
    xi = Fr(p + q, 2)
    yi = sum(Fr(cf) * xi ** pw for cf, pw in t)
    fs = pterms(t)
    if c == 'C1':
        if d <= 1:
            return ret(f'Find f″(x) for f(x) = {fs}.', pterms(d2), f"f′(x) = {pterms(d1)} (A1); f″(x) = {pterms(d2)} (A1).", 2)
        x0 = rng.choice([p, q])
        v2 = evt(d2, x0)
        return mcq(rng, f'For f(x) = {fs}, f′({m(x0)}) = 0 and f″({m(x0)}) = {m(_num(v2))}. What is the nature of the stationary point at x = {m(x0)}?', 'local minimum' if v2 > 0 else 'local maximum',
                   ['local maximum' if v2 > 0 else 'local minimum', 'point of inflection', 'cannot be determined'], f"f″ {'> 0: concave up, minimum' if v2 > 0 else '< 0: concave down, maximum'}.")
    if c == 'C2':
        k = rng.choice([4, 6])
        b = rng.randint(-3, 4)
        return ret(f'For f(x) = (x {sgn(-b)})^{k}'.replace('(x + 0)', 'x').replace('(x − 0)', 'x').replace(f'^{k}', sup(k)) + f', {name(rng)} says that since f″({m(b)}) = 0 there is a point of inflection at x = {m(b)}. Explain why this is wrong.', f'minimum at x = {m(b)}',
                   f"R1 f″(x) = {k * (k - 1)}(x {sgn(-b)}){sup(k - 2)} ≥ 0 does not change sign at x = {m(b)}; R1 f″ = 0 is necessary but not sufficient; A1 f′ changes from negative to positive so it is a minimum.".replace('(x + 0)', 'x').replace('(x − 0)', 'x'), 3, 'explain')
    if c == 'C3':
        up = f'x > {frs(xi)}' if a > 0 else f'x < {frs(xi)}'
        return ret(f'For f(x) = {fs}, find the coordinates of the point of inflection and the interval on which f is concave up.', f'({frs(xi)}, {frs(yi)}); {up}',
                   f"f″(x) = {pterms(d2)} (A1); f″(x) = 0 (M1) ⇒ x = {frs(xi)} (A1); y = {frs(yi)} (A1); f″ > 0 for {up} (A1).", 5, 'numerical')
    if p < 0:
        return None
    lo = min(evt(t, z) for z in (0, p, q, q + 2))
    t = t[:3] + [(int(t[3][0] - math.floor(lo)) + rng.randint(5, 40), 0)]
    fs = pterms(t)
    yi = sum(Fr(cf) * xi ** pw for cf, pw in t)
    yp, yq = evt(t, p), evt(t, q)
    ctx = pick(rng, ['the number of active users of an app (thousands), t months after launch', 'the depth of snow (cm) t days into the season', 'the value of an investment fund (million francs) after t years', 'the amount of water (thousand m³) in a reservoir t weeks after the start of summer'])
    return ret(f'A model for {ctx} is f(t) = {fs.replace("x", "t")}, 0 ≤ t ≤ {q + 2}. (a) Find f′(t) and f″(t). (b) Find the coordinates of the stationary points and use f″ to classify them. (c) Find the coordinates of the point of inflection. (d) Interpret the point of inflection in context. (e) State the interval on which the graph is concave down.',
               f'(b) ({m(p)}, {m(_num(yp))}) {"max" if evt(d2, p) < 0 else "min"}, ({m(q)}, {m(_num(yq))}) {"max" if evt(d2, q) < 0 else "min"} (c) ({frs(xi)}, {frs(yi)}) (e) ' + (f't < {frs(xi)}' if a > 0 else f't > {frs(xi)}'),
               f"(a) A1 A1. (b) f′ = 0 (M1) t = {m(p)}, {m(q)} (A1); f″({m(p)}) = {m(_num(evt(d2, p)))}, f″({m(q)}) = {m(_num(evt(d2, q)))} (R1) classification (A1). (c) f″ = 0 (M1) (A1). (d) R1 where the rate of change is greatest in magnitude (fastest growth/decline). (e) A1.".replace('x', 't'), 10, 'multi_step', gap='G5')


@R.add('ch07-st3', 'C4', (2, 5), 'multi_step')
def second_c4(rng, slot):
    if rng.random() < 0.5:
        L = rng.choice([500, 800, 1200, 2000, 5000, 10000, 25000])
        A = rng.randint(5, 80)
        k = round(rng.uniform(0.15, 0.9), 2)
        ti = math.log(A) / k
        what = pick(rng, [('the number of people who have heard a rumour', 'days'), ('the number of infected plants in a greenhouse', 'days'), ('the number of downloads of a new game (thousands)', 'weeks'), ('the number of fish in a stocked lake', 'months')])
        return ret(f'{what[0][0].upper() + what[0][1:]} t {what[1]} after the start is modelled by N(t) = {L}/(1 + {A}e^(−{k}t)). (a) Find N(0). (b) Use technology to sketch N and N′, and state the limiting value of N. (c) Given that N″(t) = 0 when 1 = {A}e^(−{k}t), find the time of the point of inflection. '
                   f'(d) Find N at this time and the maximum rate of increase. (e) Explain the meaning of the point of inflection in context.',
                   f'(a) {sf(L / (1 + A))} (b) {L} (c) t = {sf(ti)} (d) N = {L // 2}, rate {sf(k * L / 4)} per {what[1][:-1]}',
                   f'(a) {L}/{1 + A} (A1). (b) A1 graphs, limit {L} (A1). (c) e^(−{k}t) = 1/{A} (M1) t = ln {A}/{k} = {sf(ti)} (A1). (d) N = {L}/2 (A1); N′ = kN(1 − N/L) at N = L/2 gives {k} × {L}/4 = {sf(k * L / 4)} (M1 A1). (e) R1 growth is fastest here; afterwards it slows towards the limit.', 9, 'multi_step', gap='G5')
    k = rng.choice([0.5, 0.25, 0.2, 0.1, 0.4])
    A = rng.randint(2, 40)
    t = sp.Symbol('t')
    f = A * t * sp.exp(-k * t)
    d1 = sp.diff(f, t)
    d2 = sp.diff(f, t, 2)
    tm, ti = 1 / k, 2 / k
    what = pick(rng, [('the electrical current (mA) in a circuit', 'milliseconds'), ('the rate of rainfall (mm h⁻¹) during a storm', 'hours'), ('the number of visitors per hour at a festival (hundreds)', 'hours'), ('the power output (kW) of a wind gust', 'seconds')])
    return ret(f'{what[0][0].upper() + what[0][1:]} t {what[1]} after the start is modelled by f(t) = {A}te^(−{_num(k)}t), t ≥ 0. (a) Show that f′(t) = {A}e^(−{_num(k)}t)(1 − {_num(k)}t). (b) Find the maximum value of f and justify that it is a maximum. (c) Find f″(t). (d) Find the coordinates of the point of inflection. (e) Interpret the point of inflection in context.',
               f'(b) {sf(A * tm * math.exp(-1))} at t = {_num(tm)} (d) ({_num(ti)}, {sf(A * ti * math.exp(-2))})',
               f'(a) product rule (M1) A1 AG. (b) f′ = 0 at t = {_num(tm)} (M1) f = {sf(A * tm * math.exp(-1))} (A1); f″({_num(tm)}) = {sf(float(d2.subs(t, tm)))} < 0 (R1). (c) f″(t) = {_num(A * k)}e^(−{_num(k)}t)({_num(k)}t − 2) (A1). (d) f″ = 0 ⇒ t = {_num(ti)} (M1) ({_num(ti)}, {sf(A * ti * math.exp(-2))}) (A1). (e) R1 after this time the decrease in f begins to slow down (the rate of decrease is greatest here).', 9, 'multi_step', gap='G5')


# =============================================================================================
# ch08 Optimisation
# =============================================================================================
def argopt(f, lo, hi, mx=False, n=4000):
    g = (lambda z: -f(z)) if mx else f
    xs = np.linspace(lo, hi, n)
    vals = [g(z) for z in xs]
    i = int(np.argmin(vals))
    a, b = xs[max(i - 1, 0)], xs[min(i + 1, n - 1)]
    for _ in range(100):
        c1, c2 = a + (b - a) * 0.382, a + (b - a) * 0.618
        if g(c1) < g(c2):
            b = c2
        else:
            a = c1
    xm = (a + b) / 2
    return xm, f(xm)


R.facts('ch08-st1', F(
    terms=[('local maximum', 'a point where f′(x) = 0 and f′ changes from positive to negative; higher than nearby points'),
           ('local minimum', 'a point where f′(x) = 0 and f′ changes from negative to positive; lower than nearby points'),
           ('global (absolute) maximum', 'the greatest value of f on its whole domain; it may occur at a local maximum or at an end point'),
           ('first derivative test', 'classifying a stationary point by the sign of f′ just before and just after it')],
    facts=[('f′(x) changes from − to + at x = 2. The point at x = 2 is…', 'a local minimum', ['a local maximum', 'a point of inflection', 'a discontinuity'], 'Decreasing then increasing.'),
           ('On a closed interval, the greatest value of f may occur…', 'at a stationary point or at an end point', ['only at a stationary point', 'only at x = 0', 'only where f″ = 0'], 'Always check the end points.'),
           ('How many stationary points can a cubic function have?', '0, 1 or 2', ['exactly 3', 'exactly 2', 'any number'], 'f′ is a quadratic.')],
    why=[('Explain why the end points must be checked when finding the maximum of a function on a closed interval.', 'The function may still be increasing (or decreasing) at the edge of the domain, so the largest value can occur at an end point where f′ ≠ 0.'),
         ('Explain why f′(x) = 0 at a smooth local maximum.', 'Just before the maximum the function increases (f′ > 0) and just after it decreases (f′ < 0); the gradient passes through zero, so the tangent is horizontal.')],
    misc=[('Every stationary point is a maximum or a minimum.', 'A stationary point can be a horizontal point of inflection, e.g. y = x³ at x = 0.')],
))


@R.add('ch08-st1', ALL, (1, 5), 'short')
def stat_core(rng, slot):
    c, d = slot.c, slot.d
    t, a, p, q = _cubic_from_roots(rng)
    d1 = dterms(t)
    fs = pterms(t)
    yp, yq = evt(t, p), evt(t, q)
    # a > 0: max at p, min at q
    if a > 0:
        maxp, minp = (p, yp), (q, yq)
    else:
        maxp, minp = (q, yq), (p, yp)
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'For f(x) = {fs}, which values of x give stationary points?', f'x = {m(p)} and x = {m(q)}', [f'x = {m(-p)} and x = {m(-q)}', f'x = {m(p + q)} only', f'x = {m(p * q)} and x = 0'] if p * q != 0 and p + q != 0 else [f'x = {m(p - 1)} and x = {m(q + 1)}', f'x = {m(p + q + 1)} only', 'there are none'],
                       f"f′(x) = {pterms(d1)} = 0 ⇒ x = {m(p)}, {m(q)}.")
        return ret(f'Find the coordinates of the stationary points of y = {fs}.', f'({m(p)}, {m(_num(yp))}), ({m(q)}, {m(_num(yq))})',
                   f"dy/dx = {pterms(d1)} (A1); = 0 (M1) ⇒ x = {m(p)}, {m(q)} (A1); y-values {m(_num(yp))}, {m(_num(yq))} (A1).", 4)
    if c == 'C2':
        x0 = maxp[0]
        return ret(f'For f(x) = {fs}, explain how the sign of f′(x) either side of x = {m(x0)} shows the nature of the stationary point there.', 'local maximum',
                   f"M1 f′({m(_num(x0 - 0.5))}) = {m(_num(evt(d1, x0 - 0.5)))} > 0 and f′({m(_num(x0 + 0.5))}) = {m(_num(evt(d1, x0 + 0.5)))} < 0; R1 increasing then decreasing; A1 local maximum at ({m(x0)}, {m(_num(maxp[1]))}).", 3, 'explain')
    lo, hi = p - rng.randint(1, 3), q + rng.randint(1, 3)
    cand = {lo: evt(t, lo), p: yp, q: yq, hi: evt(t, hi)}
    gmx = max(cand, key=cand.get)
    gmn = min(cand, key=cand.get)
    xmx = ' and '.join(m(z) for z in sorted(cand) if abs(cand[z] - cand[gmx]) < 1e-9)
    xmn = ' and '.join(m(z) for z in sorted(cand) if abs(cand[z] - cand[gmn]) < 1e-9)
    if c == 'C3':
        return ret(f'Find the maximum and minimum values of f(x) = {fs} for {m(lo)} ≤ x ≤ {m(hi)}.', f'max {m(_num(cand[gmx]))} at x = {xmx}; min {m(_num(cand[gmn]))} at x = {xmn}',
                   f"stationary points x = {m(p)}, {m(q)} (M1 A1); f at end points {m(_num(cand[lo]))}, {m(_num(cand[hi]))} (M1); compare: max {m(_num(cand[gmx]))}, min {m(_num(cand[gmn]))} (A1 A1).", 5, 'numerical')
    if p < 0:
        return None
    T1 = q + rng.randint(1, 3)
    lo_ = min(evt(t, z) for z in (0, p, q, T1))
    t = t[:3] + [(int(t[3][0] - math.floor(lo_)) + rng.randint(5, 30), 0)]
    vals = {z: evt(t, z) for z in (0, p, q, T1)}
    g = max(vals, key=vals.get)
    ctx = pick(rng, ['the height (m) of a drone above the ground', 'the temperature (°C) in a greenhouse', 'the share price (dollars) of a company', 'the water level (cm) in a tidal pool'])
    ft = pterms(t).replace('x', 't')
    return ret(f'For 0 ≤ t ≤ {T1}, {ctx} at time t hours is modelled by f(t) = {ft}. (a) Find f′(t). (b) Find the times when f′(t) = 0. (c) Classify each stationary point. (d) Find the greatest value of f in the domain and when it occurs. (e) Explain why the greatest value might occur at an end point.',
               f'(b) t = {p}, {q} (c) ' + ('max at t = ' + str(p) + ', min at t = ' + str(q) if a > 0 else 'min at t = ' + str(p) + ', max at t = ' + str(q)) + f' (d) {m(_num(vals[g]))} at t = {g}',
               f"(a) {pterms(d1).replace('x', 't')} (A1). (b) M1 A1. (c) sign of f′ or f″ (M1) A1. (d) compare f(0) = {m(_num(vals[0]))}, f({p}) = {m(_num(vals[p]))}, f({q}) = {m(_num(vals[q]))}, f({T1}) = {m(_num(vals[T1]))} (M1) ⇒ {m(_num(vals[g]))} (A1). (e) R1 the function may still be increasing at the end of the domain.", 8, 'multi_step', gap='G5')


R.facts('ch08-st2', F(
    terms=[('optimisation', 'finding the maximum or minimum value of a quantity, often by setting its derivative to zero'),
           ('constraint', 'a condition linking the variables (e.g. a fixed perimeter or volume) used to write the quantity in terms of one variable'),
           ('objective function', 'the quantity to be maximised or minimised, written in terms of a single variable')],
    facts=[('A rectangle has perimeter 40 m. Which dimensions give the greatest area?', '10 m × 10 m', ['5 m × 15 m', '20 m × 20 m', '8 m × 12 m'], 'A = x(20 − x), maximum at x = 10.'),
           ('In an optimisation problem, after finding x where dA/dx = 0, you should…', 'verify it is a maximum or minimum (e.g. using the second derivative)', ['stop: it is always the maximum', 'set x = 0', 'differentiate the constraint'], 'Justify the nature of the optimum.')],
    why=[('Explain why the constraint is used before differentiating in an optimisation problem.', 'The objective usually involves two variables; the constraint lets us eliminate one, so we can differentiate a function of a single variable.'),
         ('Explain why the domain of the variable matters in an optimisation problem.', 'Physical restrictions (lengths positive, cut less than half the side, etc.) limit the possible values, and the optimum must lie in this domain; end points may need checking.')],
    misc=[('If dV/dx = 0 at x = 3 then V is a maximum at x = 3.', 'It might be a minimum or inflection; the nature must be checked with f″ or the sign of f′.')],
))


@R.add('ch08-st2', ALL, (1, 5), 'short')
def optctx_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randrange(4)
    if kind == 0:
        L = rng.choice([12, 18, 24, 30, 36, 42, 48, 60])
        xm = L / 6
        V = lambda z: z * (L - 2 * z) ** 2
        intro = f'An open box is made from a square sheet of card of side {L} cm by cutting squares of side x cm from each corner and folding up the sides.'
        obj, form, dform, dom, ans, uu = 'volume', f'V = x({L} − 2x)²', f'dV/dx = ({L} − 2x)({L} − 6x)', f'0 < x < {L // 2}', V(xm), 'cm³'
    elif kind == 1:
        P = rng.choice([40, 60, 80, 100, 120, 150, 200])
        xm = P / 4
        V = lambda z: z * (P - 2 * z)
        intro = f'A farmer has {P} m of fencing to make a rectangular pen against a long straight wall (no fence needed along the wall). The two sides perpendicular to the wall have length x m.'
        obj, form, dform, dom, ans, uu = 'area', f'A = x({P} − 2x)', f'dA/dx = {P} − 4x', f'0 < x < {P // 2}', V(xm), 'm²'
    elif kind == 2:
        Vv = rng.choice([330, 500, 750, 1000, 2000])
        xm = (Vv / (2 * math.pi)) ** (1 / 3)
        V = lambda r: 2 * math.pi * r * r + 2 * Vv / r
        intro = f'A closed cylindrical can must hold {Vv} cm³. Its radius is r cm.'
        obj, form, dform, dom, ans, uu = 'surface area', f'A = 2πr² + {2 * Vv}/r', f'dA/dr = 4πr − {2 * Vv}/r²', 'r > 0', V(xm), 'cm²'
    else:
        b = rng.choice([20, 25, 40, 50, 60, 80])
        q0 = b * rng.randint(8, 15)
        cst = rng.randint(1, 4)
        # demand q = q0 − b p ; profit = (p − cst)(q0 − b p)
        xm = (q0 / b + cst) / 2
        V = lambda pp: (pp - cst) * (q0 - b * pp)
        cu = cur(rng)
        intro = f'A café sells smoothies. At a price of p {cu} it sells {q0} − {b}p smoothies per week; each smoothie costs {cst} {cu} to make.'
        obj, form, dform, dom, ans, uu = 'weekly profit', f'P = (p − {cst})({q0} − {b}p)', f'dP/dp = {q0 + b * cst} − {2 * b}p', f'{cst} < p < {frs(Fr(q0, b))}', V(xm), cu
    var = 'x' if kind < 2 else ('r' if kind == 2 else 'p')
    mxmn = 'minimum' if kind == 2 else 'maximum'
    if c == 'C1':
        return ret(f'{intro} Show that the {obj} is {form} and write down its derivative.', dform, f'R1 forming the expression from the dimensions; A1 {form}; A1 {dform}.', 3)
    if c == 'C2':
        return ret(f'{intro} The {obj} is {form}. Explain why the domain is {dom} and how you would confirm that your stationary value is a {mxmn}.', f'{dom}; second derivative or sign test',
                   f'R1 lengths/quantities must be positive and the construction must be possible; R1 d²/d{var}² {"> 0" if mxmn == "minimum" else "< 0"} at the stationary point (or sign change of the first derivative); A1 stationary value at {var} = {nv(xm)}.', 3, 'explain')
    if c == 'C3':
        return ret(f'{intro} Given that the {obj} is {form}, find the value of {var} that gives the {mxmn} {obj} and find this {mxmn}.', f'{var} = {nv(xm)}; {nv(ans)} {uu}'.strip(),
                   f'{dform} (A1); = 0 (M1) ⇒ {var} = {nv(xm)} (A1); {mxmn} {obj} = {nv(ans)} (A1); R1 justification of {mxmn}.', 5, 'numerical')
    return ret(f'{intro} (a) Show that the {obj} is given by {form}. (b) State the domain of {var}. (c) Find d/d{var} of the {obj}. (d) Find the value of {var} that gives the {mxmn} {obj}, justifying that it is a {mxmn}. (e) Find the {mxmn} {obj}.',
               f'(c) {dform} (d) {var} = {nv(xm)} (e) {nv(ans)} {uu}'.strip(),
               f'(a) R1 A1. (b) {dom} (A1). (c) A1. (d) set to zero (M1) {var} = {nv(xm)} (A1), second derivative / sign test (R1). (e) {nv(ans)} (A1).', 8, 'multi_step', gap='G5')


R.facts('ch08-st3', F(
    terms=[('technology-based optimisation', 'using a GDC or graphing software to find a maximum or minimum of a function that is hard to solve algebraically'),
           ('constraint equation', 'an equation such as a fixed volume or budget used to eliminate a variable before optimising')],
    facts=[('A GDC finds a maximum of V(x) on 0 < x < 5 at x = 1.83. What should you report?', 'x = 1.83 and the value V(1.83), with units', ['only V′(1.83) = 0', 'x = 2 (rounded)', 'the derivative formula'], 'Give the optimum and its value.'),
           ('When minimising cost for a cylinder of fixed volume with different prices for top and side, the best shape is found by…', 'writing cost in terms of r and minimising (often with technology)', ['always using h = 2r', 'making r as small as possible', 'making h as small as possible'], 'Prices change the optimum.')],
    why=[('Explain why technology is useful in optimisation problems.', 'Many realistic objective functions (with several cost rates, roots or exponentials) give equations that are hard to solve algebraically; a GDC can find the maximum/minimum numerically and display the graph to check it is global.'),
         ('Explain why a graph should be inspected even when a GDC gives a maximum.', 'The GDC may return a local maximum in the chosen window; the graph confirms whether it is the global maximum on the domain and whether end points give larger values.')],
    misc=[('The cheapest cylinder always has height equal to its diameter.', 'That is true only when all surfaces cost the same per unit area; different material prices change the optimal ratio.')],
))


@R.add('ch08-st3', ALL, (1, 5), 'short')
def techopt_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randrange(3)
    cu = cur(rng)
    if kind == 0:
        Vv = rng.choice([500, 1000, 1500, 2000, 3000])
        pt_, ps = round(rng.uniform(0.02, 0.09), 3), round(rng.uniform(0.01, 0.05), 3)
        C = lambda r: 2 * math.pi * r * r * pt_ + 2 * Vv / r * ps
        rm, cm = argopt(C, 0.5, 40)
        h = Vv / (math.pi * rm * rm)
        intro = f'A cylindrical tin must hold {Vv} cm³. Metal for the top and bottom costs {pt_} {cu} per cm² and for the curved side {ps} {cu} per cm².'
        form = f'C(r) = {sf(2 * pt_, 3)}πr² + {sf(2 * Vv * ps, 3)}/r'
        res = f'r = {sf(rm)} cm, h = {sf(h)} cm, cost {sf(cm)} {cu}'
        var, ext = 'r', (rm, cm)
    elif kind == 1:
        a_ = rng.randint(200, 900)
        w = rng.randint(100, 600)
        vs, vr = rng.choice([(1.2, 0.5), (1.5, 0.8), (5, 2), (60, 20), (4, 1.5)])
        T = lambda x: math.hypot(x, a_) / vr + (w - x) / vs if x <= w else 1e9
        xm, tm = argopt(T, 0, w)
        intro = f'A lifeguard at A on the beach, {w} m along the shore from a swimmer\'s nearest shore point, runs at {vs} m s⁻¹ and swims at {vr} m s⁻¹. The swimmer is {a_} m out to sea. She runs to a point x m from the swimmer\'s nearest shore point and then swims straight to the swimmer.'
        form = f'T(x) = ({w} − x)/{vs} + √(x² + {a_}²)/{vr}'
        res = f'x = {sf(xm)} m, T = {sf(tm)} s'
        var, ext = 'x', (xm, tm)
    else:
        P = rng.choice([6, 8, 10, 12])
        # Norman window: rectangle width 2r, height h, semicircle: perimeter 2r + 2h + πr = P; light: rectangle clear (1), semicircle tinted (k)
        k = rng.choice([0.5, 0.6, 0.75])
        Lf = lambda r: 2 * r * (P - 2 * r - math.pi * r) / 2 + k * 0.5 * math.pi * r * r
        rmax = P / (2 + math.pi)
        rm, lm = argopt(Lf, 0.01, rmax, mx=True)
        intro = f'A window is a rectangle of width 2r m topped by a semicircle of radius r m. The total perimeter is {P} m. The rectangle is clear glass and the semicircle is tinted, letting through only {_num(k)} times as much light per m².'
        form = f'L(r) = r({P} − 2r − πr) + {_num(k / 2)}πr²'
        res = f'r = {sf(rm)} m, L = {sf(lm)}'
        var, ext = 'r', (rm, lm)
    if c == 'C1':
        return ret(f'{intro} The quantity to optimise is {form}. Use technology to find the optimal value of {var}.', f'{var} = {sf(ext[0])}', f'graph or solver (M1); {var} = {sf(ext[0])} (A1).', 2)
    if c == 'C2':
        return ret(f'{intro} The model is {form}. Explain why technology is appropriate here and how you would check your answer.', f'{var} ≈ {sf(ext[0])}',
                   f'R1 setting the derivative to zero gives an equation that is awkward to solve by hand; R1 use a graph/solver to locate the turning point and check values either side (or the end points of the domain); A1 {var} ≈ {sf(ext[0])}.', 3, 'explain')
    if c == 'C3':
        return ret(f'{intro} Show that the model is {form} and use technology to find the optimum.', res,
                   f'R1 setting up the constraint; A1 {form}; M1 technology/derivative = 0; A1 {res}.', 4, 'numerical')
    return ret(f'{intro} (a) Show that the model is {form}. (b) State a suitable domain for {var}. (c) Sketch the graph of the model on your GDC. (d) Find the optimal value of {var} and the optimal value of the quantity. (e) Comment on one limitation of the model.',
               f'(d) {res}', f'(a) R1 constraint, A1 expression. (b) A1 domain. (c) A1 sketch with turning point. (d) M1 technology A1 A1 {res}. (e) R1 e.g. thickness of material/waste/realistic speeds ignored.', 8, 'multi_step', gap='G5')


# =============================================================================================
# ch09 Integration
# =============================================================================================
def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s_ = f(a) + f(b)
    for i in range(1, n):
        s_ += (4 if i % 2 else 2) * f(a + i * h)
    return s_ * h / 3


def iterms(terms):
    """antiderivative of [(coef, power)] with power != -1, Fraction coefficients"""
    return [(Fr(cf) / (p + 1), p + 1) for cf, p in terms]


R.facts('ch09-st1', F(
    terms=[('anti-differentiation', 'the reverse of differentiation: finding F(x) with F′(x) = f(x)'),
           ('indefinite integral', '∫f(x) dx = F(x) + C, the family of all antiderivatives'),
           ('constant of integration', 'the arbitrary constant C in an indefinite integral, fixed by a boundary condition'),
           ('definite integral', '∫ₐᵇ f(x) dx = F(b) − F(a); for f ≥ 0 it is the area under the curve between x = a and x = b')],
    facts=[('What is ∫x⁴ dx?', 'x⁵/5 + C', ['4x³ + C', 'x⁵ + C', '5x⁵ + C'], 'Increase the power by 1 and divide by the new power.'),
           ('What is ∫6 dx?', '6x + C', ['0', '6 + C', '3x² + C'], 'The integral of a constant k is kx.'),
           ('If f′(x) = 2x and f(1) = 5, what is f(x)?', 'x² + 4', ['x² + 5', '2x² + 3', 'x² − 4'], 'f = x² + C; 1 + C = 5.'),
           ('A curve lies below the x-axis between x = 1 and x = 3. Its definite integral over [1, 3] is…', 'negative', ['positive', 'zero', 'undefined'], 'Area below the axis gives a negative integral.')],
    why=[('Explain why an indefinite integral includes "+ C".', 'Differentiating a constant gives zero, so infinitely many functions differing by a constant have the same derivative; C represents all of them.'),
         ('Explain why the area between a curve and the x-axis may not equal the definite integral.', 'Parts of the curve below the axis contribute negative values that cancel positive parts; for area, integrate |f(x)| or split the interval at the roots.')],
    misc=[('∫x⁻¹ dx = x⁰/0 + C.', 'The power rule fails for n = −1; ∫(1/x) dx = ln|x| + C.')],
))


@R.add('ch09-st1', ALL, (1, 5), 'short')
def integ_core(rng, slot):
    c, d = slot.c, slot.d
    t = rterms(rng, k=2)
    t = [(cf, p) for cf, p in t if p != -1]
    F_ = iterms(t)
    if c == 'C1':
        if d <= 1:
            cf, p = rng.choice([2, 3, 4, 5, 6, 8, 10, 12]), rng.choice([1, 2, 3, 4, 5])
            right = pterms([(Fr(cf, p + 1), p + 1)]) + ' + C'
            return mcq(rng, f'Find ∫{pterms([(cf, p)])} dx.', right, [pterms([(cf * p, p - 1)]) + ' + C', pterms([(cf, p + 1)]) + ' + C', pterms([(Fr(cf, p), p + 1)]) + ' + C'] if p != 0 else None, 'Add 1 to the power, divide by the new power.')
        return ret(f'Find ∫({pterms(t)}) dx.', pterms(F_) + ' + C', f'power rule for integration (M1); {pterms(F_)} (A1) + C (A1).', 3)
    if c == 'C2':
        x0, y0 = rng.randint(-2, 3), rng.randint(-10, 15)
        C0 = Fr(y0) - sum(Fr(cf) * Fr(x0) ** p for cf, p in F_)
        return ret(f"{name(rng)} is told f′(x) = {pterms(t)} and that the curve passes through ({m(x0)}, {m(y0)}). She writes f(x) = {pterms(F_)}. Explain what is missing and find f(x).", f'f(x) = {pterms(F_ + [(C0, 0)])}',
                   f'R1 the constant of integration is missing: f(x) = {pterms(F_)} + C; M1 substitute ({m(x0)}, {m(y0)}); A1 C = {frs(C0)}, f(x) = {pterms(F_ + [(C0, 0)])}.', 3, 'explain')
    a, b = sorted(rng.sample(range(0, 6), 2))
    if c == 'C3':
        t2, a2, p2, q2 = _cubic_from_roots(rng)
        f = lambda z: evt(t, z)
        val = simpson(f, a, b)
        roots = [r for r in _roots_num(f, a, b) if a < r < b]
        area = sum(abs(simpson(f, u, v)) for u, v in zip([a] + roots, roots + [b]))
        return ret(f'Use technology to find ∫ from {a} to {b} of ({pterms(t)}) dx, and the total area enclosed between the curve y = {pterms(t)}, the x-axis and the lines x = {a} and x = {b}.', f'{sf(val)}; area {sf(area)}',
                   f'definite integral = {sf(val)} (A1); ' + (f'curve crosses the axis at x = {", ".join(sf(r) for r in roots)} (M1); split and add absolute values (M1) = {sf(area)} (A1).' if roots else f'curve does not cross the axis on the interval (R1); area = |{sf(val)}| = {sf(area)} (A1 A1).'), 4, 'numerical')
    # C4: rate integrated
    k = rng.randint(2, 6)
    r0 = rng.randint(20, 80)
    T = rng.randint(4, 12)
    u_ = rng.randint(1, max(1, T // 2))
    rate = [(Fr(-k, 1), 2), (Fr(k * (T + u_)), 1), (Fr(r0), 0)]
    tot = sum(float(cf) / (p + 1) * T ** (p + 1) for cf, p in rate)
    half = bisect(lambda z: sum(float(cf) / (p + 1) * z ** (p + 1) for cf, p in rate) - tot / 2, 0, T)
    what = pick(rng, [('Water flows into a reservoir', 'thousand m³ per hour', 'thousand m³'), ('Vehicles enter a car park', 'vehicles per hour', 'vehicles'), ('Oil leaks from a damaged pipe', 'litres per minute', 'litres'), ('Visitors arrive at a museum', 'people per hour', 'people')])
    return ret(f'{what[0]} at a rate of r(t) = {pterms(rate).replace("x", "t")} {what[1]}, 0 ≤ t ≤ {T}. (a) Find the rate at t = 0 and the time of the greatest rate. (b) Find ∫r(t) dt. (c) Find the total amount over the {T} time units. (d) Use technology to find the time by which half of this total has arrived. (e) Explain what the area under the graph of r represents.',
               f'(a) {r0}; t = {_num((T + u_) / 2)} (c) {sf(tot)} {what[2]} (d) t = {sf(half)}',
               f'(a) A1; r′(t) = 0 (M1) t = {_num((T + u_) / 2)} (A1). (b) {pterms(iterms(rate)).replace("x", "t")} + C (A1). (c) definite integral from 0 to {T} (M1) = {sf(tot)} (A1). (d) solve ∫₀ᵏ r dt = {sf(tot / 2)} (M1) k = {sf(half)} (A1). (e) R1 the total amount accumulated.', 9, 'multi_step', gap='G5')


def trap(ys, h):
    return h / 2 * (ys[0] + ys[-1] + 2 * sum(ys[1:-1]))


R.facts('ch09-st2', F(
    terms=[('trapezoidal rule', '∫ₐᵇ y dx ≈ (h/2)[y₀ + yₙ + 2(y₁ + … + yₙ₋₁)], with n strips of width h = (b − a)/n'),
           ('strip width', 'h = (b − a)/n, the width of each trapezium in the trapezoidal rule')],
    facts=[('Using the trapezoidal rule with 4 strips on [0, 2], the strip width is…', '0.5', ['2', '0.25', '4'], 'h = (2 − 0)/4.'),
           ('For a curve that is concave up on [a, b], the trapezoidal rule gives…', 'an overestimate', ['an underestimate', 'the exact area', 'a negative value'], 'The chords lie above the curve.'),
           ('How can the accuracy of the trapezoidal rule be improved?', 'use more, narrower strips', ['use fewer strips', 'use wider strips', 'ignore the end values'], 'Smaller h reduces the error.')],
    why=[('Explain why the trapezoidal rule overestimates the area under a curve that is concave up.', 'Each trapezium\'s top edge is a chord, which lies above a concave-up curve, so each trapezium contains slightly more area than the region under the curve.'),
         ('Explain why the trapezoidal rule is useful when a function is only known from data.', 'It only needs the y-values at equally spaced x-values, such as measurements of depth across a river, and does not require a formula.')],
    misc=[('In the trapezoidal rule every y-value is multiplied by 2.', 'Only the interior values are doubled; the first and last values are counted once.')],
))


@R.add('ch09-st2', ALL, (1, 5), 'short')
def trap_core(rng, slot):
    c, d = slot.c, slot.d
    n = rng.choice([4, 5, 6])
    h = rng.choice([0.5, 1, 2, 5, 10])
    xs = [i * h for i in range(n + 1)]
    if c in ('C1', 'C3') and rng.random() < 0.5 or c == 'C4':
        vv, dp_, pr_ = round(rng.uniform(0.3, 1.5), 1), round(rng.uniform(0.3, 1.2), 1), round(rng.uniform(0.1, 0.4), 2)
        cu = cur(rng)
        ctx = pick(rng, [('The depth of a river is measured across its width', 'depth (m)', 'm', 'cross-sectional area', 'm²', [1, 2, 5], (0.4, 4), (f'The water flows at {vv} m s⁻¹; estimate the volume of water passing per second.', lambda A_: f'{sf(A_ * vv)} m³ s⁻¹')),
                         ('The speed of a cyclist is recorded', 'speed (m s⁻¹)', 's', 'distance travelled', 'm', [2, 5, 10], (2, 12), ('Estimate the average speed over the whole time.', None)),
                         ('The width of a garden pond is measured along its length', 'width (m)', 'm', 'surface area', 'm²', [0.5, 1, 2], (0.5, 6), (f'The pond has a constant depth of {dp_} m; estimate the volume of water it holds.', lambda A_: f'{sf(A_ * dp_)} m³')),
                         ('The power output of a solar panel is recorded during the day', 'power (kW)', 'h', 'energy generated', 'kWh', [1, 2], (0.2, 4.5), (f'Electricity is valued at {pr_} {cu} per kWh; estimate the value of the energy.', lambda A_: f'{sf(A_ * pr_)} {cu}')),
                         ('The rate of water flow from a spring is recorded', 'flow rate (litres per minute)', 'min', 'volume of water', 'litres', [5, 10, 15], (3, 30), ('Estimate the mean flow rate over the period.', None))])
        h = rng.choice(ctx[5])
        xs = [i * h for i in range(n + 1)]
        ys = [round(rng.uniform(*ctx[6]), 1) for _ in xs]
        if 'river' in ctx[0]:
            ys[0] = ys[-1] = 0
        A = trap(ys, h)
        tbl = '; '.join(f'x = {_num(x)}: {_num(y)}' for x, y in zip(xs, ys))
        intro = f'{ctx[0]} at equal intervals: {tbl} (x in {ctx[2]}; values give the {ctx[1]}).'
        if c == 'C1':
            return ret(f'{intro} Use the trapezoidal rule to estimate the {ctx[3]}.', f'{sf(A)} {ctx[4]}', f'h = {_num(h)} (A1); (h/2)[{_num(ys[0])} + {_num(ys[-1])} + 2({" + ".join(_num(y) for y in ys[1:-1])})] (M1) = {sf(A)} {ctx[4]} (A1).', 3)
        if c == 'C3':
            A2 = trap(ys[::2], 2 * h) if n % 2 == 0 else None
            if A2 is None:
                return ret(f'{intro} Use the trapezoidal rule with all the data to estimate the {ctx[3]}, and state the strip width used.', f'{sf(A)} {ctx[4]}; h = {_num(h)}',
                           f'h = {_num(h)} (A1); end values {_num(ys[0])}, {_num(ys[-1])}, interior sum {_num(sum(ys[1:-1]))} (M1 A1); {sf(A)} {ctx[4]} (A1).', 4, 'numerical')
            return ret(f'{intro} Estimate the {ctx[3]} using the trapezoidal rule with (i) all {n} strips and (ii) only {n // 2} strips, and comment on which is more reliable.', f'(i) {sf(A)} (ii) {sf(A2)} {ctx[4]}',
                       f'(i) M1 A1 {sf(A)}; (ii) h = {_num(2 * h)} (M1) {sf(A2)} (A1); R1 more strips (narrower) usually gives a better estimate.', 5, 'numerical')
        etxt, ef = ctx[7]
        eans = ef(A) if ef else f'{sf(A / xs[-1])} {ctx[1].split("(")[1].rstrip(")")}'
        return ret(f'{intro} (a) Use the trapezoidal rule to estimate the {ctx[3]}. (b) State the strip width h. (c) Explain whether the estimate is likely to be too large or too small, given that the true curve is smooth and concave down between the measurements. (d) Explain how the estimate could be improved. (e) {etxt}',
                   f'(a) {sf(A)} {ctx[4]} (b) {_num(h)} (c) too small (e) {eans}',
                   f'(a) M1 A1 A1. (b) A1. (c) R1 chords lie below a concave-down curve, so an underestimate. (d) R1 measure at more points (smaller h). (e) A1.', 8, 'multi_step', gap='G5')
    # function based
    fk = rng.randrange(3)
    a = rng.randint(0, 2)
    if fk == 0:
        k = rng.choice([0.5, 0.3, 0.2, 0.8])
        f = lambda z: math.exp(k * z)
        fs, conc = f'e^({_num(k)}x)', 'up'
    elif fk == 1:
        f = lambda z: math.sqrt(z + 1)
        fs, conc = '√(x + 1)', 'down'
    else:
        f = lambda z: 1 / (z + 1)
        fs, conc = '1/(x + 1)', 'up'
    hh = rng.choice([0.5, 1])
    b = a + n * hh
    ys = [f(a + i * hh) for i in range(n + 1)]
    A = trap(ys, hh)
    ex = simpson(f, a, b)
    if c == 'C1':
        return nmcq(rng, f'Use the trapezoidal rule with {n} strips to estimate ∫ from {a} to {_num(b)} of {fs} dx.', A, [A * 2, hh * sum(ys), trap(ys, hh) + hh * ys[0]], f'h = {_num(hh)}; (h/2)[y₀ + y{"₀₁₂₃₄₅₆₇₈₉"[n]} + 2(sum of interior)] = {sf(A)}.')
    if c == 'C2':
        return ret(f'The trapezoidal rule with {n} strips gives {sf(A, 4)} for ∫ from {a} to {_num(b)} of {fs} dx, while technology gives {sf(ex, 4)}. Explain why the trapezoidal value is {"larger" if conc == "up" else "smaller"}.', f'{"over" if conc == "up" else "under"}estimate',
                   f'R1 the curve is concave {conc} on the interval; R1 chords lie {"above" if conc == "up" else "below"} the curve, so each trapezium {"over" if conc == "up" else "under"}estimates; A1 percentage error {sf(abs(A - ex) / ex * 100)}%.', 3, 'explain')
    return ret(f'Use the trapezoidal rule with {n} strips to estimate ∫ from {a} to {_num(b)} of {fs} dx, and find the percentage error compared with the value from technology.', f'{sf(A)}; {sf(abs(A - ex) / ex * 100)}%',
               f'h = {_num(hh)} (A1); y-values {", ".join(sf(y) for y in ys)} (M1); estimate {sf(A)} (A1); exact {sf(ex)}, error {sf(abs(A - ex) / ex * 100)}% (A1).', 4, 'numerical')


R.facts('ch09-st3', F(
    terms=[('standard integrals', '∫xⁿ dx = xⁿ⁺¹/(n + 1) + C (n ≠ −1), ∫(1/x) dx = ln|x| + C, ∫eˣ dx = eˣ + C, ∫sin x dx = −cos x + C, ∫cos x dx = sin x + C, ∫(1/cos²x) dx = tan x + C'),
           ('integration by inspection', 'recognising an integrand as the result of the chain rule, e.g. ∫f′(x)e^(f(x)) dx = e^(f(x)) + C'),
           ('integration by substitution', 'replacing an inner function u = g(x) with du = g′(x) dx to turn the integral into a standard form')],
    facts=[('What is ∫cos(3x) dx?', '(1/3)sin(3x) + C', ['3sin(3x) + C', '−(1/3)sin(3x) + C', 'sin(3x) + C'], 'Divide by the inner coefficient.'),
           ('What is ∫e^(2x) dx?', '(1/2)e^(2x) + C', ['2e^(2x) + C', 'e^(2x) + C', 'e^(2x + 1)/(2x + 1) + C'], 'Reverse the chain rule.'),
           ('What is ∫5/x dx?', '5ln|x| + C', ['5x⁻² + C', 'ln|5x| + C', '−5/x² + C'], 'Standard integral.'),
           ('What is ∫sin x dx?', '−cos x + C', ['cos x + C', '−sin x + C', 'sin²x/2 + C'], 'd/dx(−cos x) = sin x.')],
    why=[('Explain why ∫2x e^(x²) dx = e^(x²) + C.', 'By the chain rule d/dx e^(x²) = 2x e^(x²); the integrand is exactly this derivative, so the integral is e^(x²) + C.'),
         ('Explain why ∫(2x + 3)⁵ dx is not (2x + 3)⁶/6 + C.', 'Differentiating (2x + 3)⁶/6 gives 2(2x + 3)⁵, twice the integrand; we must also divide by the inner derivative 2, giving (2x + 3)⁶/12 + C.')],
    misc=[('∫sin x dx = cos x + C.', 'The derivative of cos x is −sin x, so ∫sin x dx = −cos x + C.')],
))


@R.add('ch09-st3', ALL, (1, 5), 'short')
def stdint_core(rng, slot):
    c, d = slot.c, slot.d
    a = rng.choice([2, 3, 4, 5, 6])
    k = rng.choice([2, 3, 4, 5, 0.5])
    choices = [
        (f'cos({a}x)', f'(1/{a})sin({a}x) + C', [f'{a}sin({a}x) + C', f'−(1/{a})sin({a}x) + C', f'sin({a}x) + C'], sp.cos(a * x_)),
        (f'sin({a}x)', f'−(1/{a})cos({a}x) + C', [f'(1/{a})cos({a}x) + C', f'−{a}cos({a}x) + C', f'{a}cos({a}x) + C'], sp.sin(a * x_)),
        (f'e^({a}x)', f'(1/{a})e^({a}x) + C', [f'{a}e^({a}x) + C', f'e^({a}x) + C', f'e^({a + 1}x)/{a + 1} + C'], sp.exp(a * x_)),
        (f'{a}/x', f'{a}ln|x| + C', [f'−{a}/x² + C', f'ln|{a}x| + C', f'{a}x⁻² + C'], a / x_),
        (f'1/({a}x + 1)', f'(1/{a})ln|{a}x + 1| + C', [f'ln|{a}x + 1| + C', f'{a}ln|{a}x + 1| + C', f'−1/({a}x + 1)² + C'], 1 / (a * x_ + 1)),
        (f'1/cos²({a}x)', f'(1/{a})tan({a}x) + C', [f'{a}tan({a}x) + C', f'tan({a}x) + C', f'−(1/{a})tan({a}x) + C'], 1 / sp.cos(a * x_) ** 2),
    ]
    q, right, wrongs, expr = pick(rng, choices)
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'Find ∫{q} dx.', right, wrongs, 'Standard integral, dividing by the coefficient of x.')
        return ret(f'Find ∫{q} dx.', right, f'standard form (M1); correct coefficient (A1); + C (A1).', 3)
    inner = rng.choice([1, 2, 3])
    b_ = rng.randint(1, 9)
    n = rng.choice([3, 4, 5, 6])
    subs = [
        (f'{2 * inner}x(x² + {b_}){sup(n)}' if inner > 1 else f'2x(x² + {b_}){sup(n)}', f'(1/{n + 1})(x² + {b_}){sup(n + 1)} + C' if inner == 1 else f'({frs(Fr(inner, n + 1))})(x² + {b_}){sup(n + 1)} + C', 'u = x² + ' + str(b_), 2 * inner * x_ * (x_ ** 2 + b_) ** n),
        (f'x·e^(x²)', '(1/2)e^(x²) + C', 'u = x²', x_ * sp.exp(x_ ** 2)),
        (f'{2 * inner}x/(x² + {b_})', f'{inner}ln(x² + {b_}) + C', f'u = x² + {b_}', 2 * inner * x_ / (x_ ** 2 + b_)),
        (f'sin x·cos{sup(n)}x', f'−(1/{n + 1})cos{sup(n + 1)}x + C', 'u = cos x', sp.sin(x_) * sp.cos(x_) ** n),
        (f'({a}x {sgn(-b_)}){sup(n)}', f'(1/{a * (n + 1)})({a}x {sgn(-b_)}){sup(n + 1)} + C', f'u = {a}x {sgn(-b_)}', (a * x_ - b_) ** n),
        (f'x²·e^(x³)', '(1/3)e^(x³) + C', 'u = x³', x_ ** 2 * sp.exp(x_ ** 3)),
    ]
    q2, r2, us, e2 = pick(rng, subs)
    # verify by differentiation
    if c == 'C2':
        return ret(f'{name(rng)} claims that ∫{q2} dx can be found by integrating each factor separately and multiplying. Explain why this is wrong and find the integral using a suitable substitution.', r2,
                   f'R1 there is no product rule for integration (∫uv ≠ ∫u ∫v); M1 substitution {us} (the integrand contains the derivative of the inner function); A1 {r2}.', 3, 'explain')
    lo_, hi_ = 0, rng.choice([1, 2])
    val = float(sp.N(sp.integrate(e2, (x_, lo_, hi_))))
    if c == 'C3':
        return ret(f'Use the substitution {us} to find ∫{q2} dx, and hence evaluate the integral from {lo_} to {hi_}.', f'{r2}; {sf(val)}',
                   f'du/dx correct (A1); integral in terms of u (M1 A1); {r2} (A1); definite value {sf(val)} (A1).', 5, 'numerical')
    v0 = rng.randint(2, 20)
    T_ = rng.choice([2, 3, 4, 5])
    kk = rng.choice([0.5, 0.2, 0.25, 0.4])
    # velocity v = v0 e^{-k t}; position s = v0/k (1 - e^{-kt})
    dist = v0 / kk * (1 - math.exp(-kk * T_))
    return ret(f'A boat cuts its engine and its velocity t seconds later is v(t) = {v0}e^(−{_num(kk)}t) m s⁻¹. (a) Find ∫v(t) dt. (b) Given that s(0) = 0, find an expression for the displacement s(t). (c) Find the distance travelled in the first {T_} s. (d) Find the limiting distance as t → ∞. (e) Find the time taken to travel half of this limiting distance.',
               f'(b) s = {_num(v0 / kk)}(1 − e^(−{_num(kk)}t)) (c) {sf(dist)} m (d) {_num(v0 / kk)} m (e) {sf(math.log(2) / kk)} s',
               f'(a) −{_num(v0 / kk)}e^(−{_num(kk)}t) + C (M1 A1). (b) C = {_num(v0 / kk)} (A1). (c) {sf(dist)} (A1). (d) R1 e^(−{_num(kk)}t) → 0 (A1). (e) e^(−{_num(kk)}t) = 1/2 (M1) t = ln 2/{_num(kk)} = {sf(math.log(2) / kk)} (A1).', 8, 'multi_step', gap='G5')


R.facts('ch09-st4', F(
    terms=[('area between two curves', '∫ₐᵇ (f(x) − g(x)) dx where f(x) ≥ g(x) on [a, b]; a and b are often the intersection points'),
           ('area between a curve and the y-axis', '∫ x dy from y = c to y = d, with x written in terms of y'),
           ('volume of revolution about the x-axis', 'V = π∫ₐᵇ y² dx'),
           ('volume of revolution about the y-axis', 'V = π∫꜀ᵈ x² dy')],
    facts=[('The region under y = x from x = 0 to x = 3 is rotated 360° about the x-axis. The volume is…', '9π', ['3π', '27π', '4.5π'], 'π∫₀³ x² dx = 9π.'),
           ('To find the area between y = f(x) and y = g(x), you integrate…', 'the upper curve minus the lower curve', ['the product of the curves', 'f(x) + g(x)', 'the lower curve minus the upper curve'], 'Height of each thin strip.'),
           ('For a volume about the y-axis, the integrand is…', 'πx² written in terms of y', ['πy²', '2πx', 'πxy'], 'Discs perpendicular to the y-axis.')],
    why=[('Explain why the volume of revolution formula contains πy².', 'Rotating a thin strip of height y about the x-axis gives a disc of radius y and thickness δx with volume πy²δx; summing the discs and letting δx → 0 gives π∫y² dx.'),
         ('Explain why the intersection points are found first when calculating the area between two curves.', 'They give the limits of integration, and they show where the upper and lower curves may swap, which would require splitting the integral.')],
    misc=[('The volume of revolution about the x-axis is π(∫y dx)².', 'The formula is π∫y² dx: square y first, then integrate.')],
))


@R.add('ch09-st4', ALL, (1, 5), 'short')
def areavol_core(rng, slot):
    c, d = slot.c, slot.d
    r1, r2 = sorted(rng.sample(range(-3, 6), 2))
    k = rng.choice([1, 2, -1, Fr(1, 2)])
    # f = line, g = parabola with intersections at r1, r2: f − g = −k(x − r1)(x − r2) >= 0 if k > 0
    k = abs(k)
    m_, c_ = rng.randint(-3, 4), rng.randint(-5, 6)
    gpar = [(k, 2), (-k * (r1 + r2) + m_, 1), (k * r1 * r2 + c_, 0)]
    fline = [(m_, 1), (c_, 0)]
    area = Fr(k) * (r2 - r1) ** 3 / 6
    if c == 'C1':
        a_ = rng.choice([1, 2, 3])
        b_ = rng.choice([2, 3, 4])
        vol = math.pi * (a_ ** 2) * b_ ** 3 / 3
        if d <= 1:
            return nmcq(rng, f'The region between y = {_num(a_) if a_ != 1 else ""}x, the x-axis and x = {b_} is rotated 360° about the x-axis. Find the volume.', vol, [vol / math.pi, math.pi * a_ * b_ ** 2 / 2, vol * 3], f'π∫₀^{b_} ({a_}x)² dx = π{a_ * a_}x³/3 from 0 to {b_} = {sf(vol)}.')
        return ret(f'Find the area enclosed between y = {pterms(fline)} and y = {pterms(gpar)}.', frd(area),
                   f'intersections x = {m(r1)}, {m(r2)} (M1 A1); ∫({pterms(fline)} − ({pterms(gpar)})) dx (M1) = {frd(area)} (A1).', 4)
    if c == 'C2':
        b_ = rng.choice([2, 3, 4, 5, 6])
        v = rng.randrange(3)
        if v == 1:
            return ret(f'To find the area between y = {pterms(fline)} and y = {pterms(gpar)}, {name(rng)} evaluates ∫ from {m(r1)} to {m(r2)} of (({pterms(gpar)}) − ({pterms(fline)})) dx and gets {m(frd(-area))}. Explain the error and state the area.', frd(area),
                       f'R1 the integrand must be (upper curve − lower curve); R1 between x = {m(r1)} and {m(r2)} the line y = {pterms(fline)} is above the parabola, so the sign is reversed; A1 area = {frd(area)}.', 3, 'explain')
        if v == 2:
            q_ = rng.randint(1, 4)
            tt = [(1, 2), (-q_ - b_, 1), (q_ * b_, 0)]
            I = Fr(b_ ** 3, 3) - Fr(q_ + b_, 2) * b_ ** 2 + q_ * b_ * b_
            A1_ = abs(Fr(q_ ** 3, 3) - Fr(q_ + b_, 2) * q_ ** 2 + q_ * b_ * q_)
            A2_ = abs(I - (Fr(q_ ** 3, 3) - Fr(q_ + b_, 2) * q_ ** 2 + q_ * b_ * q_))
            if q_ >= b_:
                return None
            return ret(f'{name(rng)} says the area between y = {pterms(tt)} and the x-axis from x = 0 to x = {b_} is ∫₀^{b_} ({pterms(tt)}) dx = {frd(I)}. Explain why this is not the area and find the correct area.', frd(A1_ + A2_),
                       f'R1 the curve crosses the x-axis at x = {q_} (between 0 and {b_}), and the part below the axis gives a negative integral; M1 split: |∫₀^{q_}| + |∫_{q_}^{b_}| = {frd(A1_)} + {frd(A2_)}; A1 {frd(A1_ + A2_)}.', 4, 'explain')
        fn, fsq, Vf = pick(rng, [('√x', 'x', lambda bb: math.pi * bb * bb / 2), ('x', 'x²', lambda bb: math.pi * bb ** 3 / 3), ('2√x', '4x', lambda bb: 2 * math.pi * bb * bb), ('x²', 'x⁴', lambda bb: math.pi * bb ** 5 / 5)])
        return ret(f'{name(rng)} calculates the volume when the region under y = {fn} from x = 0 to x = {b_} is rotated about the x-axis as π(∫₀^{b_} {fn} dx)². Explain the error and find the correct volume.', f'{sf(Vf(b_))}',
                   f'R1 the formula is π∫y² dx (sum of disc volumes), not π times the square of the area; M1 π∫₀^{b_} {fsq} dx; A1 {sf(Vf(b_))}.', 3, 'explain')
        return ret(f'{name(rng)} calculates the volume when the region under y = √x from x = 0 to x = {b_} is rotated about the x-axis as π(∫₀^{b_} √x dx)². Explain the error and find the correct volume.', f'{sf(math.pi * b_ * b_ / 2)}',
                   f'R1 the formula is π∫y² dx (sum of disc volumes), not π times the square of the area; M1 π∫₀^{b_} x dx; A1 π × {b_}²/2 = {sf(math.pi * b_ * b_ / 2)}.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            a_ = rng.choice([1, 2, 4])
            y1, y2 = sorted(rng.sample(range(1, 7), 2))
            # x = sqrt(y/a)  for y = a x^2 ; area with y-axis: ∫ sqrt(y/a) dy
            ar = (2 / 3) * (y2 ** 1.5 - y1 ** 1.5) / math.sqrt(a_)
            vy = math.pi * (y2 * y2 - y1 * y1) / (2 * a_)
            return ret(f'The curve y = {_num(a_) if a_ != 1 else ""}x² for x ≥ 0 is considered between y = {y1} and y = {y2}. Find the area between the curve and the y-axis and the volume generated when this region is rotated 360° about the y-axis.', f'{sf(ar)}; {sf(vy)}',
                       f'x = {"√y" if a_ == 1 else f"√(y/{a_})"} (A1); area = ∫ x dy from {y1} to {y2} (M1) = {sf(ar)} (A1); V = π∫ x² dy = π∫ {"y" if a_ == 1 else f"y/{a_}"} dy (M1) = {sf(vy)} (A1).', 5, 'numerical')
        f = lambda z: evt(fline, z)
        g = lambda z: evt(gpar, z)
        return ret(f'Find the area of the region enclosed by y = {pterms(fline)} and y = {pterms(gpar)}.', frd(area),
                   f'solve {pterms(fline)} = {pterms(gpar)} (M1) ⇒ x = {m(r1)}, {m(r2)} (A1); ∫ (upper − lower) dx (M1) = {frd(area)} (A1).', 4, 'numerical')
    H = rng.randint(6, 20)
    Rr = rng.randint(3, 9)
    # vase: rotate y = R + a sin(x) ... use y = sqrt(x) scaled: radius r(x) = Rr - (Rr - 2) x / H  (frustum) -> volume
    r_ = lambda z: Rr * math.sqrt(1 - 0.5 * z / H) if True else 0
    V = math.pi * simpson(lambda z: r_(z) ** 2, 0, H)
    exact = math.pi * Rr * Rr * (H - 0.25 * H)
    return ret(f'The inside of a vase is modelled by rotating the curve r = {Rr}√(1 − x/{2 * H}), 0 ≤ x ≤ {H}, through 360° about the x-axis (lengths in cm). (a) Write down an integral for the volume. (b) Find the volume exactly in terms of π. (c) Find the volume in litres to 3 s.f. (d) The vase is filled to depth {H // 2} cm from the base x = 0; find the volume of water. (e) Explain one way the model might differ from a real vase.',
               f'(b) {_num(Rr * Rr * 0.75 * H)}π cm³ (c) {sf(exact / 1000)} L (d) {sf(math.pi * Rr * Rr * (H // 2 - (H // 2) ** 2 / (4 * H)))} cm³',
               f'(a) π∫₀^{H} {Rr * Rr}(1 − x/{2 * H}) dx (M1 A1). (b) π{Rr * Rr}[x − x²/{4 * H}] (M1) = {_num(Rr * Rr * 0.75 * H)}π (A1). (c) {sf(exact)} cm³ = {sf(exact / 1000)} L (A1). (d) integrate to {H // 2} (M1) (A1). (e) R1 e.g. wall thickness, base shape.', 9, 'multi_step', gap='G5')


@R.add('ch09-st3', 'C4', (2, 5), 'multi_step')
def stdint_c4(rng, slot):
    v = rng.randrange(3)
    if v == 0:
        a = rng.randint(2, 12)
        h0 = round(rng.uniform(0.3, 2), 1)
        T = rng.randint(5, 30)
        tree = pick(rng, ['a eucalyptus sapling', 'a bamboo shoot', 'an oak seedling', 'a teak sapling'])
        H = h0 + a / 10 * math.log(T + 1)
        return ret(f'The height h metres of {tree} t years after planting grows at a rate dh/dt = {_num(a / 10)}/(t + 1). It was {h0} m tall when planted. (a) Find ∫{_num(a / 10)}/(t + 1) dt. (b) Find h in terms of t. (c) Find the height after {T} years. (d) Find how long it takes to reach {sf(2 * H, 2)} m. (e) Comment on the long-term behaviour of the model.',
                   f'(b) h = {_num(a / 10)}ln(t + 1) + {h0} (c) {sf(H)} m (d) {sf(math.exp((float(sf(2 * H, 2)) - h0) / (a / 10)) - 1)} years',
                   f'(a) {_num(a / 10)}ln(t + 1) + C (M1 A1). (b) C = {h0} (A1). (c) {sf(H)} (A1). (d) solve (M1) {sf(math.exp((float(sf(2 * H, 2)) - h0) / (a / 10)) - 1)} (A1). (e) R1 h grows without bound, but very slowly – unrealistic for very large t.', 8, 'multi_step', gap='G5')
    if v == 1:
        A = rng.randint(20, 120)
        P = rng.choice([12, 24])
        T = rng.randint(2, P // 2)
        w = math.pi / P
        tot = A * P / math.pi * (1 - math.cos(w * T))
        place = pick(rng, ['a desalination plant', 'a city water tower', 'a hydro-electric dam', 'a sewage works'])
        return ret(f'Water flows into {place} at a rate R(t) = {A} sin(πt/{P}) m³ per hour, 0 ≤ t ≤ {P}. (a) Find ∫{A} sin(πt/{P}) dt. (b) Find the total volume in the first {T} hours. (c) Find the total volume over the whole {P} hours. (d) Find the mean rate of flow over the {P} hours. (e) State the time at which the rate is greatest.',
                   f'(b) {sf(tot)} m³ (c) {sf(2 * A * P / math.pi)} m³ (d) {sf(2 * A / math.pi)} m³ h⁻¹ (e) t = {_num(P / 2)}',
                   f'(a) −({A * P}/π)cos(πt/{P}) + C (M1 A1). (b) limits 0 to {T} (M1) {sf(tot)} (A1). (c) {sf(2 * A * P / math.pi)} (A1). (d) total ÷ {P} (A1). (e) A1.', 8, 'multi_step', gap='G5')
    a, b, k = rng.randint(5, 30), rng.randint(20, 80), rng.choice([0.1, 0.05, 0.2, 0.02])
    F0 = rng.randint(500, 5000)
    X = rng.randint(20, 100)
    cu = cur(rng)
    Cx = F0 + a * X + b / k * (1 - math.exp(-k * X))
    return ret(f'The marginal cost of producing x items is C′(x) = {a} + {b}e^(−{_num(k)}x) {cu} per item. The fixed cost is {F0} {cu}. (a) Find ∫({a} + {b}e^(−{_num(k)}x)) dx. (b) Find C(x). (c) Find the cost of producing {X} items. (d) Find the average cost per item for {X} items. (e) Explain why the marginal cost approaches {a} {cu} for large x.',
               f'(b) C(x) = {a}x − {_num(b / k)}e^(−{_num(k)}x) + {_num(F0 + b / k)} (c) {sf(Cx)} {cu} (d) {sf(Cx / X)} {cu}',
               f'(a) {a}x − {_num(b / k)}e^(−{_num(k)}x) + K (M1 A1). (b) C(0) = {F0} ⇒ K = {_num(F0 + b / k)} (A1). (c) {sf(Cx)} (A1). (d) ÷ {X} (A1). (e) R1 e^(−{_num(k)}x) → 0.', 8, 'multi_step', gap='G5')


# =============================================================================================
# ch10 Kinematics and differential equations
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('displacement', 's, the position of a particle relative to a fixed origin; it can be negative'),
           ('velocity', 'v = ds/dt, the rate of change of displacement'),
           ('acceleration', 'a = dv/dt = d²s/dt², the rate of change of velocity'),
           ('total distance travelled', '∫|v| dt over the time interval, which counts motion in both directions as positive'),
           ('speed', '|v|, the magnitude of the velocity')],
    facts=[('s(t) = t³ − 6t. What is the velocity at t = 2?', '6', ['−4', '12', '2'], 'v = 3t² − 6.'),
           ('A particle is at rest when…', 'v = 0', ['a = 0', 's = 0', 'v = a'], 'At rest means zero velocity.'),
           ('∫₀⁵ v dt gives…', 'the displacement after 5 seconds (change in position)', ['the total distance always', 'the acceleration', 'the speed at t = 5'], 'Distance needs |v|.')],
    why=[('Explain why the displacement and the total distance travelled can be different.', 'Displacement is the net change in position; if the particle reverses direction, motion backwards cancels some forward motion, while distance counts both as positive.'),
         ('Explain how to tell whether a particle is speeding up.', 'It speeds up when v and a have the same sign (both positive or both negative), because the acceleration acts in the direction of motion.')],
    misc=[('A negative acceleration always means the particle is slowing down.', 'If the velocity is also negative, the particle is speeding up in the negative direction.')],
))


@R.add('ch10-st1', ALL, (1, 5), 'short')
def kin_core(rng, slot):
    c, d = slot.c, slot.d
    # v(t) = k(t − p)(t − q), p < q positive
    k = rng.choice([1, 2, 3, -1, Fr(1, 2)])
    p, q = sorted(rng.sample(range(1, 7), 2))
    T = q + rng.randint(1, 3)
    vt = [(Fr(k), 2), (Fr(-k * (p + q)), 1), (Fr(k * p * q), 0)]
    at = dterms(vt)
    st = iterms(vt)
    s0 = rng.randint(-5, 8)
    st_ = st + [(Fr(s0), 0)]
    V = lambda z: evt(vt, z)
    disp = evt(st, T)
    dist = sum(abs(evt(st, b) - evt(st, a)) for a, b in [(0, p), (p, q), (q, T)])
    vs = pterms(vt).replace('x', 't')
    if c == 'C1':
        t0 = rng.randint(0, T)
        if d <= 1:
            return nmcq(rng, f'A particle moves with velocity v(t) = {vs} m s⁻¹. Find its acceleration at t = {t0}.', evt(at, t0), [V(t0), evt(at, t0) + float(k), evt(at, t0) * t0 if t0 not in (0, 1) else evt(at, t0) - 2], f'a = dv/dt = {pterms(at).replace("x", "t")}; at t = {t0}: {m(_num(evt(at, t0)))}.', fmtf=lambda z: m(_num(z)))
        return ret(f'A particle moves in a straight line with velocity v(t) = {vs} m s⁻¹. Find the times when the particle is at rest and its acceleration at those times.', f't = {p}, {q}; a = {m(_num(evt(at, p)))}, {m(_num(evt(at, q)))} m s⁻²',
                   f'v = 0 (M1) ⇒ t = {p}, {q} (A1); a = {pterms(at).replace("x", "t")} (A1); values {m(_num(evt(at, p)))}, {m(_num(evt(at, q)))} (A1).', 4)
    if c == 'C2':
        return ret(f'For a particle with v(t) = {vs} m s⁻¹, {name(rng)} finds the distance travelled in the first {T} seconds as ∫₀^{T} v dt = {m(_num(disp))} m. Explain why this is not the total distance and find it.', f'{sf(dist)} m',
                   f'R1 v changes sign at t = {p} and t = {q}, so the particle changes direction; R1 total distance = ∫|v| dt (split at the roots); A1 {sf(dist)} m.', 3, 'explain')
    if c == 'C3':
        return ret(f'A particle starts at s = {m(s0)} m and moves with velocity v(t) = {vs} m s⁻¹. Find its displacement from the origin at t = {T} and the total distance travelled in the first {T} seconds.', f's({T}) = {m(_num(s0 + disp))} m; distance {sf(dist)} m',
                   f's(t) = {pterms(st_).replace("x", "t")} (M1 A1); s({T}) = {m(_num(s0 + disp))} (A1); distance ∫₀^{T}|v| dt (M1) = {sf(dist)} (A1).', 5, 'numerical')
    obj = pick(rng, ['A lift in a skyscraper', 'A robot arm on an assembly line', 'A cable car', 'A model train on a straight track'])
    vmin_t = Fr(p + q, 2)
    return ret(f'{obj} moves along a straight line with velocity v(t) = {vs} m s⁻¹ for 0 ≤ t ≤ {T}; at t = 0 it is {m(s0)} m from a reference point O. (a) Find the acceleration at t = {T}. (b) Find when it changes direction. (c) Find the displacement function s(t). (d) Find the total distance travelled. (e) Find the {"minimum" if k > 0 else "maximum"} velocity and when it occurs. (f) State the intervals on which it is speeding up.',
               f'(a) {m(_num(evt(at, T)))} m s⁻² (b) t = {p}, {q} (c) s = {pterms(st_).replace("x", "t")} (d) {sf(dist)} m (e) {m(_num(V(float(vmin_t))))} m s⁻¹ at t = {frs(vmin_t)} (f) {p} < t < {frs(vmin_t)}, {q} < t ≤ {T}',
               f'(a) A1. (b) v = 0 with sign change (M1 A1). (c) integrate (M1) with constant {m(s0)} (A1). (d) ∫|v| (M1) {sf(dist)} (A1). (e) a = 0 (M1) (A1). (f) R1 v and a have the same sign: {p} < t < {frs(vmin_t)} and {q} < t ≤ {T} (A1).', 11, 'multi_step', gap='G5')


R.facts('ch10-st2', F(
    terms=[('differential equation', 'an equation involving a derivative, such as dy/dx = ky'),
           ('separation of variables', 'rearranging dy/dx = f(x)g(y) to ∫(1/g(y)) dy = ∫f(x) dx and integrating both sides'),
           ('general solution', 'the solution containing an arbitrary constant'),
           ('particular solution', 'the solution satisfying a given initial condition')],
    facts=[('The general solution of dy/dx = 3y is…', 'y = Ae^(3x)', ['y = 3x + C', 'y = e^(3x) + C', 'y = 3e^x'], 'Separate: ln|y| = 3x + c.'),
           ('A population grows at a rate proportional to its size. The model is…', 'dP/dt = kP', ['dP/dt = k', 'dP/dt = kt', 'P = kt'], 'Rate ∝ size.'),
           ("Newton's law of cooling for a room at 20 °C is…", 'dT/dt = −k(T − 20)', ['dT/dt = −kT', 'dT/dt = k(T + 20)', 'T = 20e^(−kt)'], 'Rate ∝ temperature difference.')],
    why=[('Explain why only one constant of integration is needed when separating variables.', 'Constants from both sides can be combined into a single constant: ∫(1/y)dy + c₁ = ∫k dx + c₂ gives ln|y| = kx + C.'),
         ('Explain what dP/dt = kP with k < 0 models.', 'Exponential decay: the rate of decrease is proportional to the current amount, e.g. radioactive decay or a drug clearing from the body.')],
    misc=[('The solution of dy/dx = 2y is y = y² + C.', 'Separate variables: dy/y = 2 dx ⇒ ln|y| = 2x + C ⇒ y = Ae^(2x).')],
))


@R.add('ch10-st2', ALL, (1, 5), 'short')
def sepvar_core(rng, slot):
    c, d = slot.c, slot.d
    if c == 'C1':
        k = rng.choice([2, 3, 0.5, -2, -0.4, 0.1])
        y0 = rng.randint(2, 50)
        x1 = rng.randint(1, 5)
        if d <= 1:
            return mcq(rng, f'Which is the general solution of dy/dx = {m(_num(k))}y?', f'y = Ae^({m(_num(k))}x)', [f'y = {m(_num(k))}x + C', f'y = e^({m(_num(k))}x) + C', f'y = Ax^{m(_num(k))}'], 'Separate the variables and integrate.')
        return ret(f'Solve dy/dx = {m(_num(k))}y given that y = {y0} when x = 0, and find y when x = {x1}.', f'y = {y0}e^({m(_num(k))}x); {sf(y0 * math.exp(k * x1))}',
                   f'∫dy/y = ∫{m(_num(k))} dx (M1); ln y = {m(_num(k))}x + C (A1); y = {y0}e^({m(_num(k))}x) (A1); y({x1}) = {sf(y0 * math.exp(k * x1))} (A1).', 4)
    if c == 'C2' and rng.random() < 0.6:
        k = rng.choice([2, 3, 4, 5, 0.5, 0.2, -2, -3, -0.5])
        y0 = rng.randint(2, 40)
        x1 = rng.randint(1, 4)
        if rng.random() < 0.5:
            return ret(f'{name(rng)} solves dy/dx = {m(_num(k))}y with y(0) = {y0} and writes ln y = {m(_num(k))}x + C, so y = e^({m(_num(k))}x) + C, giving y = e^({m(_num(k))}x) + {y0 - 1}. Explain the error and find the correct particular solution.', f'y = {y0}e^({m(_num(k))}x)',
                       f'R1 exponentiating ln y = {m(_num(k))}x + C gives y = e^C e^({m(_num(k))}x) = Ae^({m(_num(k))}x), a multiplicative constant; M1 y(0) = {y0} ⇒ A = {y0}; A1 y = {y0}e^({m(_num(k))}x) (e.g. y({x1}) = {sf(y0 * math.exp(k * x1))}).', 3, 'explain')
        return ret(f'{name(rng)} says that because dy/dx = {m(_num(k))}y, the graph of y against x is a straight line with gradient {m(_num(k))}. Explain why this is wrong and state the general solution.', f'y = Ae^({m(_num(k))}x)',
                   f'R1 the gradient {m(_num(k))}y changes as y changes, so it is not constant; R1 the rate is proportional to y, giving exponential {"growth" if k > 0 else "decay"}; A1 y = Ae^({m(_num(k))}x).', 3, 'explain')
    if c == 'C2':
        a = rng.choice([1, 2, 3])
        return ret(f'{name(rng)} solves dy/dx = {a if a > 1 else ""}xy by writing y = {"½" if a == 1 else _num(a / 2)}x²y + C. Explain the error and find the general solution.', f'y = Ae^({_num(a / 2)}x²)',
                   f'R1 y depends on x, so it cannot be treated as a constant when integrating with respect to x; M1 separate: ∫dy/y = ∫{a if a > 1 else ""}x dx; A1 ln|y| = {_num(a / 2)}x² + C ⇒ y = Ae^({_num(a / 2)}x²).', 3, 'explain')
    if c == 'C3':
        v = rng.randrange(3)
        if v == 0:
            a, x0, y0 = rng.choice([1, 2, 3]), 0, rng.randint(1, 6)
            x1 = round(rng.uniform(0.5, 1.5), 1)
            yv = y0 * math.exp(a * x1 * x1 / 2)
            return ret(f'Solve the differential equation dy/dx = {a if a > 1 else ""}xy, given that y = {y0} when x = 0. Hence find y when x = {x1}.', f'y = {y0}e^({_num(a / 2)}x²); {sf(yv)}',
                       f'separate (M1); ln y = {_num(a / 2)}x² + C (A1 A1); y = {y0}e^({_num(a / 2)}x²) (A1); {sf(yv)} (A1).', 5, 'numerical')
        if v == 1:
            x0, y0 = rng.randint(0, 3), rng.randint(2, 6)
            C0 = y0 * y0 - x0 * x0
            x1 = x0 + rng.randint(1, 4)
            return ret(f'Solve dy/dx = x/y given that y = {y0} when x = {x0} (y > 0), and find y when x = {x1}.', f'y = √(x² + {C0})'.replace('+ -', '− ') + f'; {sf(math.sqrt(x1 * x1 + C0))}',
                       f'∫y dy = ∫x dx (M1); y²/2 = x²/2 + C (A1); y² = x² {sgn(C0)} (A1); y({x1}) = {sf(math.sqrt(x1 * x1 + C0))} (A1).', 4, 'numerical')
        T0, Ta = rng.randint(70, 98), rng.randint(15, 25)
        T1 = rng.randint(Ta + 15, T0 - 5)
        t1 = rng.randint(3, 15)
        k = math.log((T0 - Ta) / (T1 - Ta)) / t1
        Tq = rng.randint(Ta + 5, T1 - 2)
        tq = math.log((T0 - Ta) / (Tq - Ta)) / k
        return ret(f'A cup of tea at {T0} °C cools in a room at {Ta} °C according to dT/dt = −k(T − {Ta}). After {t1} minutes it is at {T1} °C. Solve the differential equation, find k and find when the tea reaches {Tq} °C.', f'T = {Ta} + {T0 - Ta}e^(−kt), k = {sf(k)}; t = {sf(tq)} min',
                   f'separate: ∫dT/(T − {Ta}) = −∫k dt (M1); T = {Ta} + Ae^(−kt) (A1), A = {T0 - Ta} (A1); {T1 - Ta} = {T0 - Ta}e^(−{t1}k) ⇒ k = {sf(k)} (A1); t = {sf(tq)} (A1).', 5, 'numerical')
    P0 = rng.choice([200, 500, 1000, 1500, 2500])
    r = round(rng.uniform(0.05, 0.4), 2)
    t1 = rng.randint(2, 10)
    mult = rng.choice([2, 3, 5, 10])
    who = pick(rng, ['bacteria in a culture', 'rabbits on an island', 'users of a social-media app', 'cases of a mild virus'])
    return ret(f'The number N of {who} t days after observation begins satisfies dN/dt = {r}N, with N = {P0} when t = 0. (a) Solve the differential equation. (b) Find N when t = {t1}. (c) Find the time taken for N to become {mult} times its initial value. (d) Find the rate of growth when N = {P0 * mult}. (e) Explain one reason why this model is unrealistic for large t, and suggest an improvement.',
               f'(a) N = {P0}e^({r}t) (b) {sf(P0 * math.exp(r * t1))} (c) {sf(math.log(mult) / r)} days (d) {sf(r * P0 * mult)} per day',
               f'(a) separate (M1) ln N = {r}t + C (A1), N = {P0}e^({r}t) (A1). (b) A1. (c) e^({r}t) = {mult} (M1) t = ln {mult}/{r} (A1). (d) {r} × {P0 * mult} (A1). (e) R1 unlimited growth is impossible (resources); R1 logistic model dN/dt = kN(1 − N/L).', 9, 'multi_step', gap='G5')


DE_FIELDS = [
    ('x + y', lambda x, y: x + y), ('x − y', lambda x, y: x - y), ('xy', lambda x, y: x * y), ('y − x²', lambda x, y: y - x * x),
    ('x² + y² − 4', lambda x, y: x * x + y * y - 4), ('2x − y', lambda x, y: 2 * x - y), ('y(1 − y)', lambda x, y: y * (1 - y)), ('x/y', lambda x, y: x / y if y else float('nan')),
    ('y − 2x', lambda x, y: y - 2 * x), ('x − 2y', lambda x, y: x - 2 * y), ('x²y', lambda x, y: x * x * y), ('y + x − 1', lambda x, y: y + x - 1),
]

R.facts('ch10-st3', F(
    terms=[('slope field', 'a diagram of short line segments showing the gradient dy/dx = f(x, y) at points of a grid'),
           ('isocline', 'a curve along which dy/dx takes a constant value, e.g. the curve where f(x, y) = 0'),
           ('solution curve', 'a curve that follows the direction of the slope field everywhere; each initial condition gives one curve')],
    facts=[('For dy/dx = x + y, what is the slope at (1, 2)?', '3', ['2', '1', '−1'], 'Substitute x = 1, y = 2.'),
           ('On a slope field for dy/dx = y − x, where are the line segments horizontal?', 'along the line y = x', ['along the x-axis', 'along the y-axis', 'nowhere'], 'dy/dx = 0 when y = x.'),
           ('Two different solution curves of the same slope field…', 'never cross (for well-behaved equations)', ['always cross at the origin', 'are parallel lines', 'always meet at isoclines'], 'Each point has one gradient.')],
    why=[('Explain how a slope field helps to sketch a solution curve without solving the differential equation.', 'The segments show the gradient of any solution through each point; starting at the initial point and following the directions gives the shape of the solution.'),
         ('Explain why the slope field for dy/dx = f(x) has the same slopes along every vertical line.', 'The gradient depends only on x, so all points with the same x have the same slope; solution curves are vertical translations of each other.')],
    misc=[('In a slope field, a line segment at (2, 3) shows the value of y there.', 'It shows the gradient dy/dx at that point, not the y-value.')],
))


@R.add('ch10-st3', ALL, (1, 5), 'short')
def slope_core(rng, slot):
    c, d = slot.c, slot.d
    fs, f = pick(rng, DE_FIELDS)
    pts = [(rng.randint(-2, 3), rng.randint(-2, 3)) for _ in range(4)]
    pts = list(dict.fromkeys(pts))
    vals = [f(x, y) for x, y in pts]
    if any(isinstance(v, float) and math.isnan(v) for v in vals):
        return None
    if c == 'C1':
        x0, y0 = pts[0]
        return nmcq(rng, f'For the slope field of dy/dx = {fs}, find the gradient of the line segment at ({m(x0)}, {m(y0)}).', vals[0], [f(y0, x0) if f(y0, x0) != vals[0] else vals[0] + 1, vals[0] + 2, -vals[0] if vals[0] else 3], f'Substitute x = {m(x0)}, y = {m(y0)}: {m(_num(vals[0]))}.', fmtf=lambda z: m(_num(z)))
    iso = {'x + y': 'y = −x', 'x − y': 'y = x', 'xy': 'x = 0 or y = 0', 'y − x²': 'y = x²', 'x² + y² − 4': 'the circle x² + y² = 4', '2x − y': 'y = 2x', 'y(1 − y)': 'y = 0 or y = 1', 'x/y': 'x = 0 (y ≠ 0)', 'y − 2x': 'y = 2x', 'x − 2y': 'y = x/2', 'x²y': 'x = 0 or y = 0', 'y + x − 1': 'y = 1 − x'}[fs]
    if c == 'C2':
        return ret(f'Explain how to identify where the line segments in the slope field of dy/dx = {fs} are horizontal, and state where this happens.', iso,
                   f'R1 horizontal segments have gradient 0; M1 solve {fs} = 0; A1 {iso}.', 3, 'explain')
    if c == 'C3':
        return ret(f'For dy/dx = {fs}, find the gradients of the slope field at ' + ', '.join(f'({m(x)}, {m(y)})' for x, y in pts) + ', and state the isocline on which the gradient is zero.',
                   '; '.join(m(_num(v)) for v in vals) + f'; {iso}', 'substitution at each point (A2 for all, A1 for most); ' + ', '.join(m(_num(v)) for v in vals) + f'; isocline {iso} (M1 A1).', 4, 'numerical')
    x0, y0 = rng.randint(-1, 1), rng.randint(1, 3)
    h = 0.5
    xs_, ys_ = [x0], [y0]
    for _ in range(2):
        g = f(xs_[-1], ys_[-1])
        ys_.append(ys_[-1] + h * g)
        xs_.append(xs_[-1] + h)
    return ret(f'Consider the differential equation dy/dx = {fs}. (a) Find the gradient of the slope field at ({m(x0)}, {m(y0)}), ({m(x0 + 1)}, {m(y0)}) and ({m(x0)}, {m(y0 + 1)}). (b) Find the isocline where dy/dx = 0. (c) Describe the gradient of a solution curve as it crosses this isocline. (d) A solution curve passes through ({m(x0)}, {m(y0)}); use two steps along the slope field of width 0.5 to estimate y at x = {m(_num(x0 + 1))}. (e) Explain why your estimate in (d) may be inaccurate.',
               f'(a) {m(_num(f(x0, y0)))}, {m(_num(f(x0 + 1, y0)))}, {m(_num(f(x0, y0 + 1)))} (b) {iso} (d) {sf(ys_[-1])}',
               f'(a) A1 A1 A1. (b) {fs} = 0 (M1) {iso} (A1). (c) R1 horizontal tangent (stationary point of the solution). (d) y₁ = {m(_num(ys_[1]))} (M1 A1), y₂ = {sf(ys_[-1])} (A1). (e) R1 the gradient changes within each step; smaller steps would be better.', 10, 'multi_step', gap='G5')


def euler(f, x0, y0, h, n):
    xs, ys = [x0], [y0]
    for _ in range(n):
        ys.append(ys[-1] + h * f(xs[-1], ys[-1]))
        xs.append(xs[-1] + h)
    return xs, ys


R.facts('ch10-st4', F(
    terms=[("Euler's method", 'a numerical method for dy/dx = f(x, y): yₙ₊₁ = yₙ + h f(xₙ, yₙ), xₙ₊₁ = xₙ + h'),
           ('step length', 'h, the increase in x at each step of a numerical method'),
           ('coupled differential equations', 'a system such as dx/dt = f(x, y, t), dy/dt = g(x, y, t) in which the rates of two variables depend on each other')],
    facts=[("Euler's method with dy/dx = y, y(0) = 1 and h = 0.1 gives y₁ = …", '1.1', ['1.01', '1.105', '2'], 'y₁ = 1 + 0.1 × 1.'),
           ("Halving the step length in Euler's method usually…", 'improves the accuracy', ['doubles the error', 'has no effect', 'gives the exact answer'], 'Error is roughly proportional to h.'),
           ("For a concave-up solution, Euler's method tends to…", 'underestimate', ['overestimate', 'be exact', 'give negative values'], 'The tangent lies below the curve.')],
    why=[("Explain why Euler's method uses the gradient at the start of each step.", 'It follows the tangent line at the known point for a small step h, because the gradient is known only at points already computed.'),
         ("Explain why Euler's method is useful for coupled systems such as predator–prey models.", 'Such systems usually cannot be solved exactly; Euler\'s method updates both variables step by step using their current rates.')],
    misc=[("Euler's method gives the exact solution if enough decimal places are used.", 'It has a truncation error from following tangents; reducing h, not rounding, improves accuracy.')],
))


@R.add('ch10-st4', ALL, (1, 5), 'short')
def euler_core(rng, slot):
    c, d = slot.c, slot.d
    fs, f = pick(rng, [x for x in DE_FIELDS if x[0] != 'x/y'])
    x0, y0 = rng.randint(0, 2), rng.randint(1, 3)
    h = rng.choice([0.1, 0.2, 0.25, 0.5])
    n = rng.choice([2, 3, 4]) if c != 'C1' else 2
    xs, ys = euler(f, x0, y0, h, n)
    if c == 'C1':
        e4 = lambda z: m(_num(round(z, 6))) if abs(round(z, 4) - z) < 1e-9 else sf(z, 4)
        return ret(f"Use Euler's method with step length {_num(h)} to estimate y at x = {_num(x0 + 2 * h)} for dy/dx = {fs}, y({x0}) = {y0}.", e4(ys[-1]),
                   f'y₁ = {y0} + {_num(h)} × f({x0}, {y0}) = {e4(ys[1])} (M1 A1); y₂ = {e4(ys[2])} (A1).', 3)
    if c == 'C2':
        k = round(rng.uniform(0.2, 1), 1)
        h2 = rng.choice([0.5, 1])
        _, y1 = euler(lambda x, y: k * y, 0, 1, h2, int(2 / h2))
        _, y2 = euler(lambda x, y: k * y, 0, 1, h2 / 2, int(4 / h2))
        ex = math.exp(2 * k)
        return ret(f"For dy/dx = {_num(k)}y, y(0) = 1, Euler's method gives y(2) ≈ {sf(y1[-1], 4)} with h = {_num(h2)} and {sf(y2[-1], 4)} with h = {_num(h2 / 2)}. The exact value is {sf(ex, 4)}. Explain these results.", 'underestimates; smaller h is more accurate',
                   f'R1 the solution y = e^({_num(k)}x) is concave up, so tangent steps fall below the curve (underestimate); R1 halving h reduces the error (from {sf(ex - y1[-1])} to {sf(ex - y2[-1])}); A1 roughly halves, as the error is proportional to h.', 3, 'explain')
    if c == 'C3':
        if rng.random() < 0.5:
            return ret(f"Use Euler's method with h = {_num(h)} to estimate y({_num(x0 + n * h)}) for dy/dx = {fs}, y({x0}) = {y0}. Show each step.", sf(ys[-1], 4),
                       'M1 yₙ₊₁ = yₙ + h f(xₙ, yₙ); ' + '; '.join(f'x = {_num(round(xs[i], 6))}: y = {sf(ys[i], 4)}' for i in range(1, n + 1)) + ' (A2 for all values, A1 for most); final answer (A1).', 4, 'numerical')
        a, b, cc, dd = rng.choice([0.5, 1, 0.2]), rng.choice([0.1, 0.02, 0.05]), rng.choice([0.3, 0.5, 0.8]), rng.choice([0.01, 0.02, 0.05])
        X0, Y0 = rng.randint(20, 60), rng.randint(5, 15)
        hh = rng.choice([0.1, 0.2])
        X, Y = [X0], [Y0]
        for _ in range(2):
            x_, y_ = X[-1], Y[-1]
            X.append(x_ + hh * (a * x_ - b * x_ * y_))
            Y.append(y_ + hh * (-cc * y_ + dd * x_ * y_))
        return ret(f"A predator–prey model is dx/dt = {_num(a)}x − {_num(b)}xy, dy/dt = −{_num(cc)}y + {_num(dd)}xy, where x is the number of prey (hundreds) and y the number of predators (hundreds). At t = 0, x = {X0}, y = {Y0}. Use Euler's method with h = {_num(hh)} to estimate x and y at t = {_num(2 * hh)}.",
                   f'x ≈ {sf(X[2], 4)}, y ≈ {sf(Y[2], 4)}', f'M1 both equations updated using the values from the previous step; step 1: x = {sf(X[1], 4)}, y = {sf(Y[1], 4)} (A1 A1); step 2: x = {sf(X[2], 4)}, y = {sf(Y[2], 4)} (A1 A1).', 5, 'numerical')
    k = round(rng.uniform(0.1, 0.5), 2)
    L = rng.choice([100, 500, 1000, 2000])
    N0 = rng.choice([10, 20, 50]) * L // 1000 if L >= 500 else rng.choice([5, 10])
    hh = rng.choice([0.5, 1])
    steps = int(4 / hh)
    _, Ns = euler(lambda t, N: k * N * (1 - N / L), 0, N0, hh, steps)
    exact = L / (1 + (L - N0) / N0 * math.exp(-k * 4))
    return ret(f"A logistic model for a population is dN/dt = {k}N(1 − N/{L}), N(0) = {N0}. (a) Find the initial rate of growth. (b) Use Euler's method with h = {_num(hh)} to estimate N(4). (c) The exact solution gives N(4) = {sf(exact, 4)}; find the percentage error. (d) Explain how the accuracy could be improved. (e) State the long-term value of N and explain why.",
               f'(a) {sf(k * N0 * (1 - N0 / L))} (b) {sf(Ns[-1], 4)} (c) {sf(abs(Ns[-1] - exact) / exact * 100)}% (e) {L}',
               f'(a) A1. (b) M1 iterative formula, A2 {sf(Ns[-1], 4)}. (c) M1 A1. (d) R1 smaller step length. (e) R1 dN/dt = 0 when N = {L}, the carrying capacity (A1).', 9, 'multi_step', gap='G5')


R.facts('ch10-st5', F(
    terms=[('phase portrait', 'a diagram of trajectories of a system dx/dt = ax + by, dy/dt = cx + dy in the (x, y) plane'),
           ('equilibrium point', 'a point where dx/dt = dy/dt = 0; for linear systems this is the origin'),
           ('saddle point', 'an equilibrium where the eigenvalues are real with opposite signs; most trajectories move away'),
           ('stable spiral', 'an equilibrium where the eigenvalues are complex with negative real part; trajectories spiral in'),
           ('centre', 'an equilibrium with purely imaginary eigenvalues; trajectories are closed ellipses')],
    facts=[('A linear system has eigenvalues −2 and −5. The origin is…', 'a stable node (sink)', ['a saddle point', 'an unstable node', 'a centre'], 'Both negative: trajectories approach the origin.'),
           ('A linear system has eigenvalues 3 and −1. The origin is…', 'a saddle point', ['a stable node', 'a centre', 'a stable spiral'], 'Opposite signs.'),
           ('Eigenvalues 1 ± 2i indicate…', 'an unstable spiral', ['a stable spiral', 'a centre', 'a saddle'], 'Positive real part, complex.'),
           ('The second-order equation d²x/dt² + 3dx/dt + 2x = 0 can be written as a system using…', 'y = dx/dt', ['y = x²', 'y = d²x/dt²', 'y = t'], 'Then dy/dt = −2x − 3y.')],
    why=[('Explain why the eigenvectors of the matrix give straight-line trajectories in the phase portrait.', 'If the initial point lies along an eigenvector v, then the solution is x = e^(λt)v, which stays on the line through v, moving towards or away from the origin depending on the sign of λ.'),
         ('Explain why complex eigenvalues produce spirals or ellipses.', 'The solution involves e^(at)(cos bt, sin bt): the trigonometric part makes trajectories rotate, and e^(at) makes them shrink (a < 0), grow (a > 0) or stay closed (a = 0).')],
    misc=[('If one eigenvalue is negative the equilibrium is stable.', 'All eigenvalues must have negative real parts; with one positive eigenvalue the origin is a saddle (unstable).')],
))


def classify(ev):
    ev = [complex(e) for e in ev]
    if abs(ev[0].imag) > 1e-9:
        re_ = ev[0].real
        return 'centre' if abs(re_) < 1e-9 else ('stable spiral' if re_ < 0 else 'unstable spiral')
    a, b = sorted([e.real for e in ev])
    if a < 0 < b:
        return 'saddle point'
    if b < 0:
        return 'stable node (sink)'
    if a > 0:
        return 'unstable node (source)'
    return 'degenerate'


def evtext(ev):
    ev = [complex(e) for e in ev]
    if abs(ev[0].imag) > 1e-9:
        r_, i_ = ev[0].real, abs(ev[0].imag)
        rs = m(_num(r_)) if abs(r_) > 1e-12 else ''
        return f'{rs} ± {_num(i_) if abs(i_ - 1) > 1e-12 else ""}i'.strip() if rs else f'±{_num(i_) if abs(i_ - 1) > 1e-12 else ""}i'
    return ', '.join(m(_num(e.real)) for e in sorted(ev, key=lambda z: z.real))


def nice_system(rng):
    for _ in range(200):
        M = np.array([[rng.randint(-4, 4), rng.randint(-4, 4)], [rng.randint(-4, 4), rng.randint(-4, 4)]])
        tr, det = M[0, 0] + M[1, 1], round(np.linalg.det(M))
        disc = tr * tr - 4 * det
        if det == 0:
            continue
        if disc >= 0 and math.isqrt(disc) ** 2 != disc:
            continue
        ev = np.linalg.eigvals(M)
        return M, ev, tr, det, disc
    return None


@R.add('ch10-st5', ALL, (1, 5), 'short')
def phase_core(rng, slot):
    c, d = slot.c, slot.d
    r = nice_system(rng)
    if r is None:
        return None
    M, ev, tr, det, disc = r
    sysx = f'dx/dt = {lin3(M[0], ("x", "y"))}, dy/dt = {lin3(M[1], ("x", "y"))}'
    kind = classify(ev)
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'The matrix of a linear system has eigenvalues {evtext(ev)}. Classify the equilibrium at the origin.', kind,
                       [k for k in ['saddle point', 'stable node (sink)', 'unstable node (source)', 'stable spiral', 'unstable spiral', 'centre'] if k != kind][:3] if rng.random() < 0.5 else [k for k in ['centre', 'unstable spiral', 'saddle point', 'stable spiral', 'stable node (sink)', 'unstable node (source)'] if k != kind][:3],
                       'Real parts and imaginary parts determine the type.')
        return ret(f'Find the eigenvalues of the system {sysx}.', evtext(ev), f'characteristic equation λ² {sgn(-tr)}λ {sgn(det)} = 0 (M1 A1); λ = {evtext(ev)} (A1).'.replace('+ 0λ ', '').replace('− 0λ ', ''), 3)
    if c == 'C2':
        return ret(f'For the system {sysx}, explain what the eigenvalues tell you about the behaviour of trajectories near the origin.', kind,
                   f'A1 eigenvalues {evtext(ev)}; R1 ' + ({'saddle point': 'real with opposite signs: trajectories approach along one eigenvector and leave along the other', 'stable node (sink)': 'real and negative: all trajectories approach the origin', 'unstable node (source)': 'real and positive: trajectories move away from the origin',
                                                          'stable spiral': 'complex with negative real part: trajectories spiral in', 'unstable spiral': 'complex with positive real part: trajectories spiral out', 'centre': 'purely imaginary: closed elliptical orbits'}[kind]) + f'; A1 {kind}.', 3, 'explain')
    if c == 'C3':
        if abs(complex(ev[0]).imag) < 1e-9:
            vecs = []
            for lam in sorted(set(round(float(np.real(e)), 9) for e in ev)):
                A_ = M - lam * np.eye(2)
                v = np.array([-A_[0, 1], A_[0, 0]]) if abs(A_[0]).sum() > 1e-9 else np.array([-A_[1, 1], A_[1, 0]])
                g = math.gcd(int(round(v[0])), int(round(v[1]))) or 1
                v = v / g
                if v[0] < 0 or (v[0] == 0 and v[1] < 0):
                    v = -v
                vecs.append((lam, v))
            return ret(f'For the system {sysx}, find the eigenvalues and corresponding eigenvectors, and classify the equilibrium at the origin.', '; '.join(f'λ = {m(_num(l))}: {vec(v)}' for l, v in vecs) + f'; {kind}',
                       f'λ² {sgn(-tr)}λ {sgn(det)} = 0 (M1) (A1); eigenvectors '.replace('+ 0λ ', '').replace('− 0λ ', '') + ', '.join(vec(v) for _, v in vecs) + f' (M1 A1); {kind} (A1).', 5, 'numerical')
        x0, y0 = 1, 0
        dxdt, dydt = M[0, 0] * x0 + M[0, 1] * y0, M[1, 0] * x0 + M[1, 1] * y0
        rot = 'anticlockwise' if M[1, 0] > 0 else 'clockwise'
        return ret(f'For the system {sysx}, find the eigenvalues, classify the origin, and use the velocity vector at (1, 0) to decide the direction of rotation of the trajectories.', f'{evtext(ev)}; {kind}; {rot}',
                   f'λ² {sgn(-tr)}λ {sgn(det)} = 0 (M1); λ = {evtext(ev)} (A1); {kind} (A1); at (1, 0): (dx/dt, dy/dt) = ({m(dxdt)}, {m(dydt)}) (M1) ⇒ {rot} (A1).'.replace('+ 0λ ', '').replace('− 0λ ', ''), 5, 'numerical')
    b_, c_ = rng.randint(0, 6), rng.randint(1, 9)
    Ms = np.array([[0, 1], [-c_, -b_]])
    ev2 = np.linalg.eigvals(Ms)
    k2 = classify(ev2)
    h = 0.1
    xv, yv = 1.0, 0.0
    for _ in range(2):
        xv, yv = xv + h * yv, yv + h * (-c_ * xv - b_ * yv)
    phys = pick(rng, ['A car suspension spring', 'A mass on a spring in a laboratory', 'A swinging gate with a damper', 'A seismometer needle'])
    return ret(f'{phys} is modelled by d²x/dt² + {b_}dx/dt + {c_}x = 0'.replace(' + 0dx/dt', '').replace('+ 1x', '+ x') + f', with x = 1 and dx/dt = 0 at t = 0. (a) Using y = dx/dt, write the equation as a system of first-order equations. (b) Write down the matrix of the system and find its eigenvalues. (c) Classify the equilibrium and describe the motion. '
               f"(d) Use Euler's method with h = 0.1 to estimate x and dx/dt at t = 0.2. (e) Explain the physical meaning of the term {b_}dx/dt.".replace(' the term 0dx/dt', ' a term in dx/dt being absent'),
               f'(b) [0, 1; {m(-c_)}, {m(-b_)}], λ = {evtext(ev2)} (c) {k2} (d) x ≈ {sf(xv, 4)}, dx/dt ≈ {sf(yv, 4)}',
               f'(a) dx/dt = y, dy/dt = −{c_}x − {b_}y (A1 A1). (b) A1; λ² + {b_}λ + {c_} = 0 (M1) A1. (c) R1 {k2}: ' + ('oscillations die away' if 'spiral' in k2 else 'no oscillation, returns to rest' if 'node' in k2 else 'undamped oscillation') + f'. (d) M1 A1 A1. (e) R1 damping (resistance proportional to velocity).', 11, 'multi_step', gap='G5')


@R.add('ch10-st5', 'C4', (2, 5), 'multi_step')
def phase_c4(rng, slot):
    r = nice_system(rng)
    if r is None:
        return None
    M, ev, tr, det, disc = r
    kind = classify(ev)
    sysx = f'dx/dt = {lin3(M[0], ("x", "y"))}, dy/dt = {lin3(M[1], ("x", "y"))}'
    x0, y0 = rng.randint(1, 4), rng.randint(-3, 3)
    h = rng.choice([0.1, 0.05, 0.2])
    X, Y = float(x0), float(y0)
    for _ in range(2):
        X, Y = X + h * (M[0, 0] * X + M[0, 1] * Y), Y + h * (M[1, 0] * X + M[1, 1] * Y)
    ctx = pick(rng, ['Two competing species of fish (deviations from equilibrium, in thousands)', 'The deviations of two connected tank levels from equilibrium (cm)', 'The prices of two rival products relative to their equilibrium values (euros)', 'Two interacting chemical concentrations relative to equilibrium (mol L⁻¹)'])
    return ret(f'{ctx} satisfy {sysx}. Initially x = {x0}, y = {m(y0)}. (a) Write the system in the form dX/dt = MX. (b) Find the eigenvalues of M. (c) Classify the equilibrium point at the origin. (d) Find dy/dx at the initial point and interpret it. (e) Use Euler\'s method with h = {_num(h)} to estimate x and y after two steps. (f) Describe the long-term behaviour of the system.',
               f'(b) {evtext(ev)} (c) {kind} (d) {frs(Fr(int(M[1, 0] * x0 + M[1, 1] * y0), int(M[0, 0] * x0 + M[0, 1] * y0))) if (M[0, 0] * x0 + M[0, 1] * y0) else "undefined (vertical)"} (e) x ≈ {sf(X, 4)}, y ≈ {sf(Y, 4)}',
               f'(a) M = {mat(M)} (A1). (b) det(M − λI) = 0 (M1) λ = {evtext(ev)} (A1). (c) {kind} (A1). (d) dy/dx = (dy/dt)/(dx/dt) (M1) (A1) gives the direction of the trajectory. (e) M1 A1 A1. (f) R1 ' + ({'saddle point': 'trajectories eventually move away along the eigenvector of the positive eigenvalue', 'stable node (sink)': 'both variables return to equilibrium', 'unstable node (source)': 'both deviations grow without bound', 'stable spiral': 'oscillations of decreasing size about equilibrium', 'unstable spiral': 'oscillations of increasing size', 'centre': 'periodic oscillation about equilibrium', 'degenerate': 'see eigenvalues'}[kind]) + '.', 10, 'multi_step', gap='G5')


# =============================================================================================
# ch11 Inferential statistics: χ² and t-tests
# =============================================================================================
HYP = [
    ('the mean time spent on homework by students at a school is {v} hours per week', 'μ = {v}', ['μ ≠ {v}', 'μ > {v}', 'μ < {v}'], 'mean'),
    ('a coin used in a game is fair', 'p = 0.5', ['p ≠ 0.5', 'p > 0.5', 'p < 0.5'], 'proportion'),
    ('favourite sport is independent of age group', 'favourite sport and age group are independent', ['they are not independent'], 'independence'),
    ('a die is fair', 'the outcomes follow a uniform distribution', ['the outcomes do not follow a uniform distribution'], 'gof'),
    ('there is no difference between the mean reaction times of two groups', 'μ₁ = μ₂', ['μ₁ ≠ μ₂', 'μ₁ > μ₂', 'μ₁ < μ₂'], 'two-mean'),
]

R.facts('ch11-st1', F(
    terms=[('null hypothesis', 'H₀, the default statement of no effect, no difference or independence, assumed true unless the evidence is strong'),
           ('alternative hypothesis', 'H₁, the statement accepted if H₀ is rejected; it may be one-tailed (<, >) or two-tailed (≠)'),
           ('significance level', 'the probability threshold (e.g. 5%) used to decide whether to reject H₀'),
           ('p-value', 'the probability, assuming H₀ is true, of obtaining a result at least as extreme as the one observed'),
           ('critical value', 'the boundary value of a test statistic beyond which H₀ is rejected')],
    facts=[('A test gives p = 0.031 at the 5% level. The conclusion is…', 'reject H₀', ['do not reject H₀', 'accept H₀ as proven', 'increase the sample until p < 0.01'], '0.031 < 0.05.'),
           ('A test gives p = 0.083 at the 5% level. The conclusion is…', 'there is insufficient evidence to reject H₀', ['reject H₀', 'H₀ is proven true', 'H₁ is true'], '0.083 > 0.05.'),
           ('"The new fertiliser increases mean yield." This alternative hypothesis is…', 'one-tailed: μ > μ₀', ['two-tailed: μ ≠ μ₀', 'one-tailed: μ < μ₀', 'the null hypothesis'], 'Direction is specified.'),
           ('Which statement about a p-value of 0.002 is correct?', 'if H₀ were true, a result this extreme would be very unlikely', ['H₀ is true with probability 0.002', 'H₁ is true with probability 0.998', 'the sample is too small'], 'Definition of a p-value.')],
    why=[('Explain why we say "do not reject H₀" rather than "accept H₀".', 'A large p-value only shows that the data are consistent with H₀; it does not prove H₀ is true – the sample may be too small to detect a real effect.'),
         ('Explain the difference between a one-tailed and a two-tailed test.', 'A one-tailed test looks for an effect in one specified direction (H₁: μ > μ₀ or μ < μ₀); a two-tailed test looks for any difference (H₁: μ ≠ μ₀), splitting the significance level between both tails.')],
    misc=[('A p-value of 0.04 means there is a 4% chance that H₀ is true.', 'The p-value is the probability of data at least this extreme assuming H₀ is true, not the probability that H₀ is true.')],
))


@R.add('ch11-st1', ALL, (1, 5), 'short')
def hyp_core(rng, slot):
    c, d = slot.c, slot.d
    alpha = rng.choice([0.01, 0.05, 0.1])
    pval = round(rng.choice([rng.uniform(0.001, 0.2), rng.uniform(alpha * 0.4, alpha * 1.6)]), 4)
    rej = pval < alpha
    ctxs = [('a café claims its mean waiting time is {v} minutes; a customer group suspects it is longer', 'μ = {v}', 'μ > {v}', 'mean waiting time', [4, 5, 6, 8]),
            ('a sports scientist believes a new training plan changes the mean 100 m time from {v} s', 'μ = {v}', 'μ ≠ {v}', 'mean 100 m time', [12, 13, 14]),
            ('a factory says the mean mass of its cereal boxes is {v} g; a consumer group suspects under-filling', 'μ = {v}', 'μ < {v}', 'mean mass', [500, 750, 1000]),
            ('a teacher believes a revision app raises the mean test score above {v}%', 'μ = {v}', 'μ > {v}', 'mean score', [60, 65, 70]),
            ('a doctor investigates whether a drug changes mean systolic blood pressure from {v} mmHg', 'μ = {v}', 'μ ≠ {v}', 'mean blood pressure', [120, 125, 130])]
    ctx, h0, h1, what, vals = pick(rng, ctxs)
    v = rng.choice(vals)
    ctx, h0, h1 = ctx.format(v=v), h0.format(v=v), h1.format(v=v)
    tail = 'two-tailed' if '≠' in h1 else 'one-tailed'
    if c == 'C1':
        if d <= 1:
            return mcq(rng, f'A test at the {_num(alpha * 100)}% significance level gives a p-value of {pv(pval)}. What is the correct decision?', 'reject H₀' if rej else 'do not reject H₀', ['do not reject H₀' if rej else 'reject H₀', 'accept H₁ as proven', 'the test is invalid'], f'Compare {pv(pval)} with {alpha}.')
        return ret(f'In a study, {ctx}. Write down suitable null and alternative hypotheses and state whether the test is one-tailed or two-tailed.', f'H₀: {h0}; H₁: {h1}; {tail}',
                   f'H₀: {h0} (A1); H₁: {h1} (A1); {tail} (A1).', 3)
    if c == 'C2':
        return ret(f'In a study, {ctx}. The test gives p = {pv(pval)}. {name(rng)} concludes: "{"H₁ is proven true" if rej else "H₀ is proven true"}." Explain why this conclusion is not appropriate and write a correct conclusion at the {_num(alpha * 100)}% level.',
                   ('reject H₀' if rej else 'do not reject H₀'),
                   f'R1 hypothesis tests give evidence, not proof (there is a chance of a type {"I" if rej else "II"} error); A1 {pv(pval)} {"<" if rej else ">"} {alpha}; R1 ' + (f'there is significant evidence at the {_num(alpha * 100)}% level that {h1.replace("μ", "the " + what)}.' if rej else f'there is insufficient evidence at the {_num(alpha * 100)}% level to reject H₀.'), 3, 'explain')
    if c == 'C3':
        tval = round(rng.uniform(0.5, 3.2), 2)
        df = rng.randint(8, 30)
        p1 = 1 - t_cdf(tval, df)
        pp = 2 * p1 if tail == 'two-tailed' else p1
        return ret(f'In a study, {ctx}. A t-test statistic of {tval} (in the direction of H₁) is obtained with {df} degrees of freedom. Find the p-value and state the conclusion at the {_num(alpha * 100)}% level.', f'p = {pv(pp)}; {"reject H₀" if pp < alpha else "do not reject H₀"}',
                   f'H₁: {h1} ⇒ {tail} (R1); p = {"2 × " if tail == "two-tailed" else ""}P(T > {tval}) (M1) = {pv(pp)} (A1); compare with {alpha} (A1) {"reject" if pp < alpha else "do not reject"} H₀.', 4, 'numerical')
    a2 = [0.01, 0.05, 0.1]
    dec = ', '.join(f'{_num(a * 100)}%: {"reject" if pval < a else "do not reject"}' for a in a2)
    return ret(f'In a study, {ctx}. (a) State the null and alternative hypotheses. (b) Explain whether the test should be one- or two-tailed. (c) The test gives p = {pv(pval)}. State the conclusion at the 1%, 5% and 10% levels. (d) Interpret the p-value in context. (e) Explain what a type I error would mean here.',
               f'(a) H₀: {h0}; H₁: {h1} (b) {tail} (c) {dec}',
               f'(a) A1 A1. (b) R1 the claim {"specifies a direction" if tail == "one-tailed" else "is about any change"}. (c) A1 A1. (d) R1 if H₀ were true, the probability of a result at least this extreme is {pv(pval)}. (e) R1 concluding the {what} has changed when in fact it has not.', 8, 'multi_step', gap='G5')


def chi_ind(table):
    T = np.array(table, dtype=float)
    rs, cs, n = T.sum(axis=1), T.sum(axis=0), T.sum()
    E = np.outer(rs, cs) / n
    chi = float(((T - E) ** 2 / E).sum())
    df = (T.shape[0] - 1) * (T.shape[1] - 1)
    return E, chi, df, chi2_sf(chi, df)


CT = [
    (['under 30', '30–50', 'over 50'], ['football', 'tennis', 'swimming'], 'age group', 'favourite sport'),
    (['Year 11', 'Year 12'], ['bus', 'car', 'walk/cycle'], 'year group', 'mode of transport to school'),
    (['male', 'female'], ['agree', 'neutral', 'disagree'], 'gender', 'opinion on a new park'),
    (['city', 'suburb', 'rural'], ['yes', 'no'], 'area of residence', 'whether they own a car'),
    (['vaccinated', 'not vaccinated'], ['caught flu', 'did not'], 'vaccination status', 'flu outcome'),
    (['morning', 'afternoon', 'evening'], ['coffee', 'tea', 'juice'], 'time of day', 'drink ordered'),
]


def gen_table(rng, R_, C_, n_per=(15, 60), assoc=True):
    base_r = [rng.uniform(0.7, 1.3) for _ in range(R_)]
    base_c = [rng.uniform(0.6, 1.4) for _ in range(C_)]
    T = []
    for i in range(R_):
        row = []
        for j in range(C_):
            mu = 30 * base_r[i] * base_c[j] * (rng.uniform(0.6, 1.5) if assoc else rng.uniform(0.9, 1.1))
            row.append(max(6, int(round(mu))))
        T.append(row)
    return T


def ttext(rows, cols, T):
    return '; '.join(f'{r}: ' + ', '.join(f'{c} {T[i][j]}' for j, c in enumerate(cols)) for i, r in enumerate(rows))


R.facts('ch11-st2', F(
    terms=[('contingency table', 'a two-way table of observed frequencies for two categorical variables'),
           ('expected frequency', '(row total × column total)/grand total, the frequency expected if the variables are independent'),
           ('χ² test for independence', 'a test of H₀: the two variables are independent, using χ² = Σ (O − E)²/E'),
           ('degrees of freedom (contingency table)', '(r − 1)(c − 1) for a table with r rows and c columns')],
    facts=[('A 3 × 4 contingency table has how many degrees of freedom?', '6', ['12', '7', '5'], '(3 − 1)(4 − 1).'),
           ('Row total 40, column total 30, grand total 120. The expected frequency is…', '10', ['30', '40', '12'], '40 × 30/120.'),
           ('A large χ² statistic suggests…', 'the observed frequencies differ greatly from those expected under independence', ['the variables are independent', 'the sample is too small', 'the expected values are wrong'], 'Large deviations.'),
           ('Why should expected frequencies usually be at least 5?', 'the χ² approximation is unreliable for small expected values', ['to make χ² larger', 'to reduce the degrees of freedom', 'to make the test one-tailed'], 'Rule of thumb in IB.')],
    why=[('Explain why the χ² test for independence is always one-tailed (upper tail).', 'Any departure from independence makes (O − E)² larger, so only large values of χ² provide evidence against H₀.'),
         ('Explain why categories may need to be combined in a χ² test.', 'If some expected frequencies are below 5 the χ² distribution is a poor approximation; combining adjacent categories increases the expected values (and reduces the degrees of freedom).')],
    misc=[('Rejecting H₀ in a χ² test proves that one variable causes the other.', 'It only shows evidence of an association; causation needs further reasoning or an experiment.')],
))


@R.add('ch11-st2', ALL, (1, 5), 'short')
def chiind_core(rng, slot):
    c, d = slot.c, slot.d
    rows, cols, rv, cv = pick(rng, CT)
    T = gen_table(rng, len(rows), len(cols), assoc=rng.random() < 0.6)
    E, chi, df, p = chi_ind(T)
    if E.min() < 5:
        return None
    alpha = rng.choice([0.05, 0.01, 0.1])
    crit = chi2_inv(alpha, df)
    tt = ttext(rows, cols, T)
    i, j = rng.randrange(len(rows)), rng.randrange(len(cols))
    who = pick(rng, ['A survey of residents', 'A sample of students', 'A market researcher', 'A public-health study'])
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{who} gives the table: {tt}. Find the expected frequency for "{rows[i]}, {cols[j]}" under independence.', E[i, j], [T[i][j], sum(T[i]) / len(cols), sum(r[j] for r in T) / len(rows) if abs(sum(r[j] for r in T) / len(rows) - E[i, j]) > 0.01 else E[i, j] + 2],
                        f'(row total × column total)/grand total = {sum(T[i])} × {sum(r[j] for r in T)}/{int(np.sum(T))} = {sf(E[i, j])}.')
        return ret(f'{who} records {rv} against {cv}: {tt}. Write down the null and alternative hypotheses and the number of degrees of freedom for a χ² test for independence.', f'H₀: {rv} and {cv} are independent; H₁: they are not; df = {df}',
                   f'H₀ (A1); H₁ (A1); ({len(rows)} − 1)({len(cols)} − 1) = {df} (A1).', 3)
    if c == 'C2':
        return ret(f'{who} records {rv} against {cv}: {tt}. A χ² test gives p = {pv(p)}. Explain what this means at the {_num(alpha * 100)}% level, and why the result does not show that {rv} causes {cv}.', f'{"reject" if p < alpha else "do not reject"} H₀',
                   f'A1 {pv(p)} {"<" if p < alpha else ">"} {alpha}, so {"reject" if p < alpha else "do not reject"} H₀; R1 ' + ('there is evidence of an association' if p < alpha else 'insufficient evidence of an association') + '; R1 association is not causation (other factors may be involved; the study is observational).', 3, 'explain')
    if c == 'C3':
        return ret(f'{who} records {rv} against {cv}: {tt}. Perform a χ² test for independence at the {_num(alpha * 100)}% level, giving the χ² statistic, the p-value and your conclusion.', f'χ² = {sf(chi)}, p = {pv(p)}; {"reject H₀" if p < alpha else "do not reject H₀"}',
                   f'H₀: independent (A1); df = {df} (A1); χ² = {sf(chi)} (A1); p = {pv(p)} (A1); {pv(p)} {"<" if p < alpha else ">"} {alpha} ⇒ {"reject H₀: there is evidence of association" if p < alpha else "insufficient evidence to reject independence"} (R1).', 5, 'numerical')
    return ret(f'{who} records {rv} against {cv}: {tt}. (a) State the null and alternative hypotheses. (b) Find the expected frequency for "{rows[i]}, {cols[j]}". (c) Write down the number of degrees of freedom. (d) Find the χ² statistic and the p-value. (e) The critical value at the {_num(alpha * 100)}% level is {sf(crit)}; state the conclusion in context. (f) Explain why all expected frequencies must be checked.',
               f'(b) {sf(E[i, j])} (c) {df} (d) χ² = {sf(chi)}, p = {pv(p)} (e) {"reject H₀" if chi > crit else "do not reject H₀"}',
               f'(a) A1. (b) M1 A1. (c) A1. (d) A1 A1. (e) compare {sf(chi)} with {sf(crit)} (M1) conclusion in context (R1). (f) R1 expected values below 5 make the test unreliable (smallest here {sf(E.min())}).', 10, 'multi_step', gap='G5')


GOF = [
    ('a six-sided die is rolled {n} times', ['1', '2', '3', '4', '5', '6'], [1] * 6, 'the die is fair'),
    ('the number of customers on each weekday is recorded ({n} in total)', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [1] * 5, 'customers are equally likely on each weekday'),
    ('a geneticist classifies {n} pea plants', ['round yellow', 'round green', 'wrinkled yellow', 'wrinkled green'], [9, 3, 3, 1], 'the plants follow the ratio 9 : 3 : 3 : 1'),
    ('the colours of {n} sweets in a bag are recorded', ['red', 'orange', 'yellow', 'green', 'blue'], [3, 2, 2, 2, 1], 'the colours are in the ratio 3 : 2 : 2 : 2 : 1 claimed by the maker'),
    ('the blood groups of {n} donors are recorded', ['O', 'A', 'B', 'AB'], [45, 40, 11, 4], 'the blood groups follow the national percentages 45%, 40%, 11%, 4%'),
    ('the results of {n} penalty kicks are classified by direction', ['left', 'centre', 'right'], [2, 1, 2], 'the directions follow the ratio 2 : 1 : 2'),
]


R.facts('ch11-st3', F(
    terms=[('χ² goodness of fit test', 'a test of whether observed frequencies fit a proposed distribution, using χ² = Σ (O − E)²/E'),
           ('degrees of freedom (goodness of fit)', 'number of categories − 1 (minus one more for each parameter estimated from the data)'),
           ('expected frequency (goodness of fit)', 'total frequency × probability of the category under H₀')],
    facts=[('A die is rolled 120 times to test fairness. The expected frequency for each face is…', '20', ['120', '6', '10'], '120 × 1/6.'),
           ('A goodness of fit test with 5 categories and no estimated parameters has how many degrees of freedom?', '4', ['5', '6', '3'], 'n − 1.'),
           ('In a goodness of fit test, H₀ states that…', 'the data follow the proposed distribution', ['the data do not follow the distribution', 'the mean is zero', 'the variables are independent'], 'Null hypothesis of fit.')],
    why=[('Explain why the degrees of freedom are one less than the number of categories in a goodness of fit test.', 'The expected frequencies must add up to the same total as the observed ones, so once all but one category are known the last is fixed.'),
         ('Explain why a small χ² value supports the null hypothesis.', 'It means the observed frequencies are close to those expected under the proposed distribution.')],
    misc=[('A χ² goodness of fit test can use percentages instead of frequencies.', 'The test must use actual frequencies (counts); using percentages changes the χ² value and the conclusion.')],
))


@R.add('ch11-st3', ALL, (1, 5), 'short')
def gof_core(rng, slot):
    c, d = slot.c, slot.d
    ctx, cats, ratio, h0 = pick(rng, GOF)
    k = len(cats)
    n = rng.choice([60, 80, 100, 120, 150, 200, 240, 300])
    probs = np.array(ratio, float) / sum(ratio)
    E = n * probs
    if E.min() < 5:
        return None
    noise = rng.uniform(0.05, 0.35)
    obs = [max(0, int(round(e * (1 + rng.uniform(-noise, noise))))) for e in E]
    big = int(np.argmax(E))
    obs[big] += n - sum(obs)
    if min(obs) < 0:
        return None
    chi = float(sum((o - e) ** 2 / e for o, e in zip(obs, E)))
    df = k - 1
    p = chi2_sf(chi, df)
    alpha = rng.choice([0.05, 0.01, 0.1])
    crit = chi2_inv(alpha, df)
    ot = ', '.join(f'{cn} {o}' for cn, o in zip(cats, obs))
    intro = ctx.format(n=n)[0].upper() + ctx.format(n=n)[1:]
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'{intro}: {ot}. To test whether {h0}, find the expected frequency for "{cats[0]}".', E[0], [obs[0], n / k if abs(n / k - E[0]) > 0.01 else E[0] + 5, E[0] * 2], f'{n} × {frs(Fr(ratio[0], sum(ratio)))} = {_num(E[0])}.', fmtf=lambda z: _num(round(z, 2)))
        return ret(f'{intro}: {ot}. Write down suitable hypotheses for a χ² goodness of fit test of whether {h0}, and the number of degrees of freedom.', f'H₀: {h0}; H₁: not; df = {df}', f'H₀ (A1); H₁ (A1); df = {k} − 1 = {df} (A1).', 3)
    if c == 'C2':
        return ret(f'{intro}: {ot}. To test whether {h0}, {name(rng)} calculates χ² using the percentages of each category instead of the frequencies. Explain why this is wrong.', 'χ² must use frequencies',
                   f'R1 χ² = Σ(O − E)²/E depends on the sample size; R1 using percentages pretends the sample size is 100, changing the statistic (here χ² = {sf(chi)} with n = {n}); A1 the conclusion could change.', 3, 'explain')
    if c == 'C3':
        return ret(f'{intro}: {ot}. Test at the {_num(alpha * 100)}% significance level whether {h0}.', f'χ² = {sf(chi)}, p = {pv(p)}; {"reject H₀" if p < alpha else "do not reject H₀"}',
                   f'expected ' + ', '.join(_num(round(e, 2)) for e in E) + f' (M1 A1); df = {df} (A1); χ² = {sf(chi)}, p = {pv(p)} (A1); conclusion (R1).', 5, 'numerical')
    return ret(f'{intro}: {ot}. (a) State the hypotheses for testing whether {h0}. (b) Find the expected frequencies. (c) State the degrees of freedom. (d) Find the χ² statistic and the p-value. (e) The critical value at the {_num(alpha * 100)}% level is {sf(crit)}. State the conclusion in context. (f) State one condition that must hold for the test to be valid.',
               f'(b) ' + ', '.join(_num(round(e, 2)) for e in E) + f' (c) {df} (d) χ² = {sf(chi)}, p = {pv(p)} (e) {"reject" if chi > crit else "do not reject"} H₀',
               f'(a) A1. (b) M1 A1. (c) A1. (d) A1 A1. (e) M1 R1. (f) R1 all expected frequencies at least 5 (smallest {_num(round(E.min(), 2))}); observations independent.', 9, 'multi_step', gap='G5')


def pooled_t(a, b):
    n1, n2 = len(a), len(b)
    m1, m2 = np.mean(a), np.mean(b)
    s1, s2 = np.std(a, ddof=1), np.std(b, ddof=1)
    sp_ = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    t = (m1 - m2) / (sp_ * math.sqrt(1 / n1 + 1 / n2))
    return m1, m2, s1, s2, sp_, t, n1 + n2 - 2


TT = [('reaction times (ms) of gamers', 'non-gamers', 'ms', (240, 330), 25),
      ('masses (g) of apples from orchard A', 'orchard B', 'g', (140, 200), 15),
      ('times (s) to solve a puzzle with music', 'without music', 's', (40, 90), 10),
      ('fuel consumption (L per 100 km) of cars with tyre type X', 'tyre type Y', 'L/100 km', (5.5, 9), 0.6),
      ('heights (cm) of sunflowers grown with fertiliser', 'without fertiliser', 'cm', (150, 220), 18),
      ('daily screen times (h) of students in school A', 'school B', 'h', (2, 6), 0.8)]


R.facts('ch11-st4', F(
    terms=[('two-sample t-test', 'a test comparing the means of two independent samples when population standard deviations are unknown'),
           ('pooled t-test', 'a two-sample t-test that assumes the two populations have equal variances and combines the sample variances'),
           ('assumptions of the t-test', 'independent random samples from normally distributed populations (with equal variances for the pooled test)')],
    facts=[('A pooled two-sample t-test with samples of size 8 and 10 has how many degrees of freedom?', '16', ['18', '17', '9'], 'n₁ + n₂ − 2.'),
           ('H₁: μ₁ > μ₂ is…', 'one-tailed', ['two-tailed', 'the null hypothesis', 'a χ² hypothesis'], 'A direction is stated.'),
           ('Which assumption does the t-test need?', 'the populations are approximately normally distributed', ['the samples have equal size', 'the means are equal', 'the data are categorical'], 'Normality.')],
    why=[('Explain why a t-test rather than a z-test is used to compare two means from small samples.', 'The population standard deviations are unknown and estimated from small samples; the t-distribution allows for the extra uncertainty in these estimates.'),
         ('Explain why the samples in a two-sample t-test must be independent.', 'The test statistic assumes the variability of the difference is the sum of the two separate variances; if the samples are paired or related, this is not true.')],
    misc=[('If the sample means differ, the population means must differ.', 'Sample means vary by chance; the t-test assesses whether the difference is larger than expected by chance.')],
))


@R.add('ch11-st4', ALL, (1, 5), 'short')
def ttest_core(rng, slot):
    c, d = slot.c, slot.d
    g1, g2, unit, (lo, hi), sd = pick(rng, TT)
    n1, n2 = rng.randint(6, 9), rng.randint(6, 9)
    mu = rng.uniform(lo, hi)
    diff = rng.choice([0, 0.5, 1, 1.5]) * sd
    dp = 1 if sd < 2 else 0
    A = [round(rng.gauss(mu + diff, sd), dp) for _ in range(n1)]
    B = [round(rng.gauss(mu, sd), dp) for _ in range(n2)]
    m1, m2, s1, s2, spool, t, df = pooled_t(A, B)
    tail = rng.choice(['two', 'one'])
    p1 = 1 - t_cdf(t, df)
    p = 2 * min(p1, 1 - p1) if tail == 'two' else p1
    alpha = rng.choice([0.05, 0.1, 0.01])
    fmt = lambda L: ', '.join(_num(v) for v in L)
    h1 = 'μ₁ ≠ μ₂' if tail == 'two' else 'μ₁ > μ₂'
    data = f'Group 1 ({g1}): {fmt(A)}. Group 2 ({g2}): {fmt(B)}.'
    if c == 'C1':
        if d <= 1:
            return nmcq(rng, f'A pooled two-sample t-test compares samples of sizes {n1} and {n2}. How many degrees of freedom are used?', df, [n1 + n2, n1 + n2 - 1, max(n1, n2) - 1], f'{n1} + {n2} − 2 = {df}.', fmtf=lambda z: str(int(z)))
        return ret(f'{data} Find the mean and standard deviation of each sample.', f'x̄₁ = {sf(m1, 4)}, s₁ = {sf(s1)}; x̄₂ = {sf(m2, 4)}, s₂ = {sf(s2)}', f'GDC 1-var stats (M1); means (A1); standard deviations with n − 1 (A1).', 3)
    if c == 'C2':
        return ret(f'{data} A researcher wants to test whether the {"means differ" if tail == "two" else "first group has a higher mean"}. Explain why a pooled t-test is appropriate, stating any assumptions, and write down the hypotheses.', f'H₀: μ₁ = μ₂; H₁: {h1}',
                   f'R1 two independent samples, population standard deviations unknown; R1 assume both populations normal with equal variances (s₁ = {sf(s1)}, s₂ = {sf(s2)} are similar); A1 H₀: μ₁ = μ₂, H₁: {h1}.', 3, 'explain')
    if c == 'C3':
        return ret(f'{data} Test at the {_num(alpha * 100)}% level whether {"the population means differ" if tail == "two" else "the mean for group 1 is greater"}, using a pooled two-sample t-test.', f't = {sf(t)}, p = {pv(p)}; {"reject H₀" if p < alpha else "do not reject H₀"}',
                   f'H₀: μ₁ = μ₂, H₁: {h1} (A1); t = {sf(t)} (A1), df = {df}; p = {pv(p)} (A1); {pv(p)} {"<" if p < alpha else ">"} {alpha} (M1) ⇒ {"reject" if p < alpha else "do not reject"} H₀ (R1).', 5, 'numerical')
    return ret(f'{data} (a) Find the sample means and standard deviations. (b) State hypotheses to test whether {"the means differ" if tail == "two" else "group 1 has a larger mean"}. (c) Find the t statistic and the p-value of a pooled two-sample t-test. (d) State the conclusion at the {_num(alpha * 100)}% level in context. (e) State two assumptions of the test. (f) Explain whether the conclusion would change at the {"10" if alpha != 0.1 else "1"}% level.',
               f'(a) x̄₁ = {sf(m1, 4)}, s₁ = {sf(s1)}; x̄₂ = {sf(m2, 4)}, s₂ = {sf(s2)} (c) t = {sf(t)}, p = {pv(p)} (d) {"reject H₀" if p < alpha else "do not reject H₀"}',
               f'(a) A1 A1. (b) A1. (c) A1 A1 (df = {df}). (d) M1 R1. (e) R1 R1 normality, equal variances, independent random samples. (f) R1 compare {pv(p)} with {"0.1" if alpha != 0.1 else "0.01"}: {"reject" if p < (0.1 if alpha != 0.1 else 0.01) else "do not reject"}.', 11, 'multi_step', gap='G5')


STUDIES = [
    ('whether the proportion of left-handed people differs between three countries (counts of left/right-handed in each)', 'χ² test for independence', 'handedness and country are independent'),
    ('whether a spinner with five sectors is fair, from 200 spins', 'χ² goodness of fit test', 'each sector is equally likely'),
    ('whether the mean commuting time differs between cyclists and bus users (two small samples of times)', 'two-sample t-test', 'μ₁ = μ₂'),
    ('whether the number of goals per match follows a Poisson distribution with mean 2.5', 'χ² goodness of fit test', 'goals per match follow Po(2.5)'),
    ('whether choice of school subject is associated with gender (survey counts)', 'χ² test for independence', 'subject choice and gender are independent'),
    ('whether a new diet reduces mean cholesterol more than the standard diet (two groups of patients)', 'two-sample t-test', 'μ_new = μ_standard'),
    ('whether customers\' satisfaction rating (low/medium/high) depends on the branch visited', 'χ² test for independence', 'rating and branch are independent'),
    ('whether births are equally likely on each day of the week at a hospital', 'χ² goodness of fit test', 'births are uniformly distributed over the days'),
    ('whether boys and girls in a class have different mean reaction times', 'two-sample t-test', 'μ_boys = μ_girls'),
    ('whether the colours of cars in a car park match national sales proportions', 'χ² goodness of fit test', 'colours follow the national proportions'),
]


@R.add('ch11-st1', 'C4', (2, 5), 'multi_step')
def hyp_c4(rng, slot):
    S = rng.sample(STUDIES, 3)
    ps = [round(rng.uniform(0.001, 0.15), 3) for _ in S]
    alpha = rng.choice([0.05, 0.01, 0.1])
    body = ' '.join(f'Study {i + 1} investigates {s_[0]}.' for i, s_ in enumerate(S))
    return ret(f'{body} (a) For each study, name an appropriate test. (b) For each study, write the null hypothesis. (c) The p-values are {", ".join(pv(q) for q in ps)} respectively. State the conclusion of each at the {_num(alpha * 100)}% level. (d) Explain, for one study, what a type II error would mean. (e) Explain why a smaller significance level makes a type I error less likely.',
               '(a) ' + '; '.join(s_[1] for s_ in S) + ' (c) ' + '; '.join('reject H₀' if q < alpha else 'do not reject H₀' for q in ps),
               '(a) A1 A1 A1. (b) ' + '; '.join(f'H₀: {s_[2]}' for s_ in S) + ' (A1 A1 A1). (c) ' + '; '.join(f'{pv(q)} {"<" if q < alpha else ">"} {alpha}' for q in ps) + f' (A1 A1). (d) R1 failing to detect a real effect. (e) R1 H₀ is rejected only for more extreme results (P(type I error) = significance level).', 10, 'multi_step', gap='G5')


# =============================================================================================
# ch12 Further statistics: CLT, confidence intervals, tests, Markov chains
# =============================================================================================
POPS = [('the masses of apples from an orchard', 'g', (120, 220), (10, 30)), ('the lengths of phone calls to a help line', 'minutes', (5, 15), (2, 6)),
        ('the daily step counts of office workers', 'steps', (6000, 11000), (1200, 3000)), ('the lifetimes of LED bulbs', 'hours', (20000, 40000), (2000, 6000)),
        ('the volumes of juice in cartons', 'mL', (995, 1010), (3, 8)), ('the waiting times at a clinic', 'minutes', (15, 45), (5, 15)),
        ('the weekly incomes of student part-time workers', 'euros', (120, 300), (30, 80))]


def popp(rng):
    what, u, (a, b), (c, d) = pick(rng, POPS)
    mu = rng.uniform(a, b)
    sg = rng.uniform(c, d)
    mag = 10 ** max(0, math.floor(math.log10(mu)) - 2)
    return what, u, round(mu / mag) * mag, round(sg / mag) * mag if sg >= mag else round(sg, 1)


R.facts('ch12-st1', F(
    terms=[('central limit theorem', 'for large n (usually n ≥ 30), the sample mean X̄ of n independent observations is approximately N(μ, σ²/n), whatever the population distribution'),
           ('standard error of the mean', 'σ/√n, the standard deviation of the sampling distribution of X̄'),
           ('sampling distribution', 'the distribution of a statistic (such as X̄) over all possible samples of a given size')],
    facts=[('X has mean 50 and standard deviation 12. For samples of size 36, the standard deviation of X̄ is…', '2', ['12', '0.333', '4'], '12/√36.'),
           ('If X ~ N(μ, σ²), then X̄ for samples of size n is…', 'exactly N(μ, σ²/n) for any n', ['approximately normal only for n ≥ 30', 'N(μ, σ²)', 'N(μ/n, σ²/n)'], 'Means of normal variables are normal.'),
           ('Increasing the sample size makes the distribution of X̄…', 'narrower (less spread)', ['wider', 'shifted to the right', 'more skewed'], 'Variance σ²/n decreases.')],
    why=[('Explain why the central limit theorem is useful when the population distribution is unknown.', 'For large samples X̄ is approximately normal regardless of the population shape, so normal probabilities can be used for the sample mean.'),
         ('Explain why the mean of a sample of 50 is less variable than a single observation.', 'High and low values within the sample tend to balance out; the variance of the mean is σ²/50, much smaller than σ².')],
    misc=[('The central limit theorem says that a large sample is normally distributed.', 'It says the sample mean is approximately normally distributed; the individual data keep the population\'s shape.')],
))


@R.add('ch12-st1', ALL, (1, 5), 'short')
def clt_core(rng, slot):
    c, d = slot.c, slot.d
    what, u, mu, sg = popp(rng)
    n = rng.choice([30, 36, 40, 49, 50, 64, 80, 100])
    se = sg / math.sqrt(n)
    if c == 'C1':
        return nmcq(rng, f'{what[0].upper() + what[1:]} have mean {_num(mu)} {u} and standard deviation {_num(sg)} {u}. For random samples of size {n}, find the standard deviation of the sample mean.', se, [sg, sg / n, sg * math.sqrt(n)], f'σ/√n = {_num(sg)}/√{n} = {sf(se)}.')
    if c == 'C2':
        return ret(f'{what[0].upper() + what[1:]} are known to be skewed, with mean {_num(mu)} {u} and standard deviation {_num(sg)} {u}. Explain why the mean of a random sample of {n} can be modelled by a normal distribution, and state its parameters.', f'X̄ ≈ N({_num(mu)}, {sf(se ** 2)})',
                   f'R1 by the central limit theorem, as n = {n} is large (≥ 30); R1 the shape of the population does not matter for large n; A1 mean {_num(mu)}, variance σ²/n = {sf(se ** 2)} (standard deviation {sf(se)}).', 3, 'explain')
    a = round(mu + rng.uniform(-2, 2) * se, 1 if se < 5 else 0)
    if c == 'C3':
        pr = 1 - ncdf((a - mu) / se)
        return ret(f'{what[0].upper() + what[1:]} have mean {_num(mu)} {u} and standard deviation {_num(sg)} {u}. A random sample of {n} is taken. Find the probability that the sample mean exceeds {_num(a)} {u}.', sf(pr),
                   f'X̄ ~ N({_num(mu)}, {_num(sg)}²/{n}) (M1 A1); P(X̄ > {_num(a)}) (M1) = {sf(pr)} (A1).', 4, 'numerical')
    k = round(rng.uniform(0.6, 1.8) * se, 2 if se < 1 else (1 if se < 20 else 0))
    if k <= 0:
        return None
    target = rng.choice([0.9, 0.95, 0.99])
    z = ninv((1 + target) / 2)
    nreq = math.ceil((z * sg / k) ** 2)
    pr = 2 * ncdf(k / se) - 1
    return ret(f'{what[0].upper() + what[1:]} have mean {_num(mu)} {u} and standard deviation {_num(sg)} {u}. (a) State the distribution of the mean X̄ of a random sample of {n}, justifying your answer. (b) Find P({_num(mu - k)} < X̄ < {_num(mu + k)}). (c) Find the smallest sample size for which P(|X̄ − {_num(mu)}| < {_num(k)}) ≥ {target}. (d) Explain what happens to the distribution of X̄ as n increases.',
               f'(a) N({_num(mu)}, {sf(se ** 2)}) (b) {sf(pr)} (c) n = {nreq}',
               f'(a) CLT, n large (R1); A1. (b) M1 A1. (c) {_num(k)}/(σ/√n) ≥ {sf(z, 4)} (M1) ⇒ n ≥ {sf((z * sg / k) ** 2, 4)} (A1) ⇒ {nreq} (A1). (d) R1 the spread decreases (standard deviation σ/√n).', 8, 'multi_step', gap='G5')


R.facts('ch12-st2', F(
    terms=[('confidence interval', 'a range of values, calculated from a sample, that contains the population parameter with a stated level of confidence'),
           ('z-interval', 'x̄ ± z*σ/√n, used when the population standard deviation σ is known'),
           ('t-interval', 'x̄ ± t*s/√n with n − 1 degrees of freedom, used when σ is unknown and estimated by the sample standard deviation'),
           ('confidence level', 'the long-run proportion of such intervals that contain the true parameter, e.g. 95%')],
    facts=[('Which value of z* is used for a 95% confidence interval?', '1.96', ['1.645', '2.576', '0.95'], 'P(−1.96 < Z < 1.96) = 0.95.'),
           ('To halve the width of a confidence interval, the sample size must be…', 'multiplied by 4', ['doubled', 'halved', 'multiplied by 2√2'], 'Width ∝ 1/√n.'),
           ('A 99% confidence interval is ___ than a 95% interval from the same data.', 'wider', ['narrower', 'the same width', 'shifted'], 'Larger critical value.')],
    why=[('Explain the meaning of a 95% confidence interval for μ.', 'If many samples were taken and an interval calculated from each, about 95% of these intervals would contain the true mean μ; it is not the probability that μ lies in this particular interval.'),
         ('Explain why a t-interval is wider than a z-interval for the same data.', 'The t-distribution has heavier tails to allow for the uncertainty in estimating σ by s, so its critical value is larger, especially for small samples.')],
    misc=[('A 95% confidence interval contains 95% of the data values.', 'It is an interval for the population mean, not a range containing 95% of individual observations.')],
))


@R.add('ch12-st2', ALL, (1, 5), 'short')
def ci_core(rng, slot):
    c, d = slot.c, slot.d
    what, u, mu, sg = popp(rng)
    dpv = 2 if mu < 100 else 1
    fx = lambda v: f'{v:.{dpv}f}'
    lvl = rng.choice([0.9, 0.95, 0.99])
    n = rng.choice([10, 12, 15, 20, 25, 40, 50, 60])
    xb = round(mu + rng.uniform(-1, 1) * sg / math.sqrt(n), 1)
    if c == 'C1':
        z = ninv((1 + lvl) / 2)
        lo, hi = xb - z * sg / math.sqrt(n), xb + z * sg / math.sqrt(n)
        return ret(f'For {what}, σ = {_num(sg)} {u}. A random sample of {n} has mean {_num(xb)} {u}. Find a {_num(lvl * 100)}% confidence interval for the population mean.', f'({fx(lo)}, {fx(hi)})',
                   f'x̄ ± z*σ/√n with z* = {sf(z, 4)} (M1 A1); ({fx(lo)}, {fx(hi)}) (A1).', 3)
    if c == 'C2':
        z = ninv((1 + lvl) / 2)
        lo, hi = xb - z * sg / math.sqrt(n), xb + z * sg / math.sqrt(n)
        return ret(f'A {_num(lvl * 100)}% confidence interval for the mean of {what} is ({fx(lo)}, {fx(hi)}) {u}. {name(rng)} says: "There is a {_num(lvl * 100)}% probability that the true mean is in this interval, and {_num(lvl * 100)}% of individual values lie in it." Explain what is wrong.', 'misinterpretation of the interval',
                   f'R1 μ is fixed; the {_num(lvl * 100)}% refers to the method: {_num(lvl * 100)}% of intervals constructed this way contain μ; R1 it is an interval for the mean, not for individual values (which are much more spread out, σ = {_num(sg)}).', 2, 'explain')
    data = [round(rng.gauss(mu, sg), 1 if sg < 20 else 0) for _ in range(rng.randint(8, 12))]
    nn = len(data)
    xbar, s_ = float(np.mean(data)), float(np.std(data, ddof=1))
    tc = t_inv((1 + lvl) / 2, nn - 1)
    lo, hi = xbar - tc * s_ / math.sqrt(nn), xbar + tc * s_ / math.sqrt(nn)
    dtxt = ', '.join(_num(v) for v in data)
    if c == 'C3':
        return ret(f'A random sample of {what} ({u}) gives: {dtxt}. Assuming the population is normal, find a {_num(lvl * 100)}% confidence interval for the population mean.', f'({fx(lo)}, {fx(hi)})',
                   f'x̄ = {fx(xbar)}, s = {fx(s_)} (A1); t-interval with {nn - 1} df, t* = {sf(tc, 4)} (M1 A1); ({fx(lo)}, {fx(hi)}) (A1).', 4, 'numerical')
    claim = round(mu + rng.uniform(-2, 2) * s_ / math.sqrt(nn), 1)
    inside = lo < claim < hi
    w = rng.choice([0.5, 0.25]) * (hi - lo)
    zz = ninv((1 + lvl) / 2)
    nreq = math.ceil((2 * zz * s_ / w) ** 2)
    return ret(f'A random sample of {what} ({u}) gives: {dtxt}. (a) Find the sample mean and the unbiased estimate of the population standard deviation. (b) Explain why a t-interval is appropriate. (c) Find a {_num(lvl * 100)}% confidence interval for μ. (d) A supplier claims μ = {_num(claim)}; comment on this claim. (e) Using s as an estimate for σ, find the sample size needed for a {_num(lvl * 100)}% z-interval of width at most {sf(w)}.',
               f'(a) {fx(xbar)}, {fx(s_)} (c) ({fx(lo)}, {fx(hi)}) (d) {"consistent" if inside else "not supported"} (e) {nreq}',
               f'(a) A1 A1. (b) R1 σ unknown, small sample, population assumed normal. (c) M1 A1 A1. (d) R1 {_num(claim)} {"lies inside" if inside else "lies outside"} the interval. (e) 2z*s/√n ≤ {sf(w)} (M1) ⇒ n = {nreq} (A1).', 10, 'multi_step', gap='G5')


def bcdf(k, n, p):
    return bincdf(n, p, int(k)) if k >= 0 else 0.0


def pcdf(k, lam):
    return poicdf(lam, int(k)) if k >= 0 else 0.0


def ppmf(k, lam):
    return poipmf(lam, int(k))


def binom_cr(n, p0, alpha, tail):
    """critical region for X ~ B(n, p0): returns (k, actual size)"""
    if tail == 'upper':
        for k in range(n + 1):
            sz = 1 - bcdf(k - 1, n, p0) if k > 0 else 1
            if sz <= alpha:
                return k, sz
    else:
        best = None
        for k in range(n + 1):
            sz = bcdf(k, n, p0)
            if sz <= alpha:
                best = (k, sz)
            else:
                break
        return best
    return None


R.facts('ch12-st3', F(
    terms=[('type I error', 'rejecting H₀ when it is true; its probability equals the (actual) significance level'),
           ('type II error', 'not rejecting H₀ when it is false'),
           ('critical region', 'the set of values of the test statistic for which H₀ is rejected'),
           ("test for Pearson's correlation coefficient", 'a test of H₀: ρ = 0 using the sample correlation r and n − 2 degrees of freedom')],
    facts=[('In a hypothesis test, a type I error is…', 'rejecting a true null hypothesis', ['accepting a false null hypothesis', 'using the wrong test', 'a calculation error'], 'Definition.'),
           ('For a discrete distribution, the actual significance level is…', 'P(test statistic in the critical region | H₀ true)', ['always exactly 5%', 'the p-value', 'P(H₀ true)'], 'It may be less than the nominal level.'),
           ('A test of H₀: ρ = 0 is used to decide whether…', 'there is linear correlation in the population', ['the regression line is accurate', 'the data are normal', 'the means are equal'], 'ρ is the population correlation coefficient.')],
    why=[('Explain why reducing the probability of a type I error usually increases the probability of a type II error.', 'Making the critical region smaller means H₀ is rejected less often, so a false H₀ is also more likely not to be rejected.'),
         ('Explain why a Poisson test for an increased rate uses the upper tail.', 'If the rate has increased, larger counts are more likely, so evidence against H₀ comes from unusually large observed values.')],
    misc=[('A significance level of 5% means the binomial test always rejects H₀ with probability exactly 0.05 when H₀ is true.', 'For discrete distributions the actual size of the critical region is usually less than 5% because probabilities jump in steps.')],
))


@R.add('ch12-st3', ALL, (1, 5), 'short')
def btest_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randrange(3)
    alpha = rng.choice([0.05, 0.1, 0.01])
    if kind == 0:
        n = rng.choice([10, 12, 15, 20, 25, 30])
        p0 = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5])
        tail = rng.choice(['upper', 'lower'])
        cr = binom_cr(n, p0, alpha, tail)
        if cr is None:
            return None
        k, sz = cr
        x = rng.randint(max(0, int(n * p0) - 4), min(n, int(n * p0) + 6))
        pval = 1 - bcdf(x - 1, n, p0) if tail == 'upper' else bcdf(x, n, p0)
        ctx = pick(rng, [('a basketball player claims to score', 'free throws'), ('a seed company claims that', 'seeds germinate late'), ('a website claims that', 'visitors click an advert'), ('a manufacturer claims', 'items are defective')])
        h1 = f'p {">" if tail == "upper" else "<"} {_num(p0)}'
        cdesc = f'X ≥ {k}' if tail == 'upper' else f'X ≤ {k}'
        intro = f'Historically {_num(p0 * 100)}% of {ctx[1]}. In a sample of {n}, {x} were observed. Test H₀: p = {_num(p0)} against H₁: {h1}.'
        if c == 'C1':
            return ret(f'{intro} Find the p-value.', pv(pval), f'X ~ B({n}, {_num(p0)}) (M1); P({"X ≥ " + str(x) if tail == "upper" else "X ≤ " + str(x)}) = {pv(pval)} (A1).', 2)
        if c == 'C2':
            p1 = p0 + (0.2 if tail == 'upper' else -0.15)
            if not 0 < p1 < 1:
                return None
            t2 = bcdf(k - 1, n, p1) if tail == 'upper' else 1 - bcdf(k, n, p1)
            return ret(f'For X ~ B({n}, p), H₀: p = {_num(p0)}, H₁: {h1}, the critical region at the {_num(alpha * 100)}% level is {cdesc}. Explain what a type II error is here and find its probability if in fact p = {_num(round(p1, 2))}.', sf(t2),
                       f'R1 not rejecting p = {_num(p0)} when p is actually {_num(round(p1, 2))}; M1 P({"X ≤ " + str(k - 1) if tail == "upper" else "X ≥ " + str(k + 1)} | p = {_num(round(p1, 2))}); A1 {sf(t2)}.', 3, 'explain')
        if c == 'C3':
            return ret(f'X ~ B({n}, p). Find the critical region for a test of H₀: p = {_num(p0)} against H₁: {h1} at the {_num(alpha * 100)}% level, and the probability of a type I error.', f'{cdesc}; {sf(sz)}',
                       f'cumulative probabilities (M1); {"P(X ≥ " + str(k) + ") = " + sf(sz) + " ≤ " + str(alpha) + ", P(X ≥ " + str(k - 1) + ") = " + sf(1 - bcdf(k - 2, n, p0)) + " > " + str(alpha) if tail == "upper" else "P(X ≤ " + str(k) + ") = " + sf(sz) + " ≤ " + str(alpha) + ", P(X ≤ " + str(k + 1) + ") = " + sf(bcdf(k + 1, n, p0)) + " > " + str(alpha)} (A1 A1); critical region {cdesc} (A1); P(type I) = {sf(sz)} (A1).', 5, 'numerical')
        return ret(f'{intro} (a) Define the test statistic and state its distribution under H₀. (b) Find the critical region at the {_num(alpha * 100)}% level. (c) State the actual significance level. (d) State the conclusion. (e) Explain what a type I error would mean in context.',
                   f'(b) {cdesc} (c) {sf(sz)} (d) {"reject H₀" if (x >= k if tail == "upper" else x <= k) else "do not reject H₀"}',
                   f'(a) X = number of successes, B({n}, {_num(p0)}) (A1 A1). (b) M1 A1. (c) A1. (d) {x} {"is" if (x >= k if tail == "upper" else x <= k) else "is not"} in the critical region (R1). (e) R1 concluding p has changed when it has not.', 8, 'multi_step', gap='G5')
    if kind == 1:
        lam = rng.choice([2, 3, 3.5, 4, 5, 6, 8])
        x = int(lam + rng.randint(1, 6))
        pval = 1 - pcdf(x - 1, lam)
        ev = pick(rng, ['calls per hour to a help desk', 'accidents per month at a junction', 'emails per hour to a shop', 'faults per 100 m of cable'])
        intro = f'The number of {ev} has historically followed Po({_num(lam)}). After a change, {x} were observed in one period. Test at the {_num(alpha * 100)}% level whether the mean has increased.'
        k = next(kk for kk in range(200) if 1 - pcdf(kk - 1, lam) <= alpha)
        if c == 'C1':
            return ret(f'{intro} Find the p-value.', pv(pval), f'P(X ≥ {x}) for X ~ Po({_num(lam)}) (M1) = {pv(pval)} (A1).', 2)
        if c == 'C2':
            return ret(f'{intro} {name(rng)} uses P(X = {x}) = {sf(ppmf(x, lam))} as the p-value. Explain the error.', f'p-value = P(X ≥ {x}) = {pv(pval)}',
                       f'R1 the p-value is the probability of a result at least as extreme, P(X ≥ {x}), not exactly {x}; A1 {pv(pval)}; R1 conclusion {"reject" if pval < alpha else "do not reject"} H₀.', 3, 'explain')
        if c == 'C3':
            return ret(f'{intro} State the hypotheses, find the p-value and give a conclusion in context.', f'H₀: λ = {_num(lam)}, H₁: λ > {_num(lam)}; p = {pv(pval)}; {"reject H₀" if pval < alpha else "do not reject H₀"}',
                       f'H₀, H₁ (A1); P(X ≥ {x}) (M1) = {pv(pval)} (A1); conclusion in context (R1).', 4, 'numerical')
        return ret(f'{intro} (a) State suitable hypotheses. (b) Find the critical region. (c) Find the probability of a type I error. (d) State the conclusion. (e) If the mean is actually {_num(lam + 3)}, find the probability of a type II error.',
                   f'(b) X ≥ {k} (c) {sf(1 - pcdf(k - 1, lam))} (d) {"reject H₀" if x >= k else "do not reject H₀"} (e) {sf(pcdf(k - 1, lam + 3))}',
                   f'(a) A1. (b) M1 A1. (c) A1. (d) R1. (e) P(X ≤ {k - 1} | λ = {_num(lam + 3)}) (M1) (A1).', 8, 'multi_step', gap='G5')
    n = rng.randint(8, 20)
    r = round(rng.uniform(0.3, 0.9) * rng.choice([1, -1]), 3)
    t = r * math.sqrt((n - 2) / (1 - r * r))
    tail = rng.choice(['two', 'pos' if r > 0 else 'neg'])
    p1 = 1 - t_cdf(abs(t), n - 2)
    pval = 2 * p1 if tail == 'two' else p1
    h1 = {'two': 'ρ ≠ 0', 'pos': 'ρ > 0', 'neg': 'ρ < 0'}[tail]
    vars_ = pick(rng, [('hours of revision', 'test score'), ('temperature', 'ice-cream sales'), ('altitude', 'air pressure'), ('age of a car', 'resale value'), ('screen time', 'hours of sleep')])
    intro = f'For {n} randomly chosen cases, the correlation between {vars_[0]} and {vars_[1]} is r = {m(r)}.'
    if c == 'C1':
        return ret(f'{intro} Write down the hypotheses for testing whether there is {"correlation" if tail == "two" else ("positive" if tail == "pos" else "negative") + " correlation"} in the population.', f'H₀: ρ = 0; H₁: {h1}', f'H₀: ρ = 0 (A1); H₁: {h1} (A1).', 2)
    if c == 'C2':
        return ret(f'{intro} Explain why a value of r this large may still not be significant, and what significance would show.', f'p = {pv(pval)}',
                   f'R1 with a small sample a large r can arise by chance; R1 the test uses n − 2 = {n - 2} degrees of freedom: p = {pv(pval)}; R1 significance shows evidence of linear correlation in the population, not causation.', 3, 'explain')
    if c == 'C3':
        return ret(f'{intro} Test at the {_num(alpha * 100)}% level H₀: ρ = 0 against H₁: {h1}.', f'p = {pv(pval)}; {"reject H₀" if pval < alpha else "do not reject H₀"}',
                   f't = r√((n − 2)/(1 − r²)) = {sf(t)} (M1 A1) or GDC; p = {pv(pval)} (A1); conclusion (R1).', 4, 'numerical')
    return ret(f'{intro} (a) State the hypotheses for a test of {"correlation" if tail == "two" else ("positive" if tail == "pos" else "negative") + " correlation"}. (b) Find the test statistic t = r√((n − 2)/(1 − r²)) and the degrees of freedom. (c) Find the p-value. (d) State the conclusion at the {_num(alpha * 100)}% level. (e) Explain why a significant result does not prove causation.',
               f'(b) t = {sf(t)}, df = {n - 2} (c) {pv(pval)} (d) {"reject H₀" if pval < alpha else "do not reject H₀"}',
               f'(a) A1. (b) A1 A1. (c) M1 A1. (d) R1. (e) R1 a third variable or coincidence may explain the association.', 8, 'multi_step', gap='G5')


R.facts('ch12-st4', F(
    terms=[('Markov chain', 'a sequence of states in which the probability of the next state depends only on the current state'),
           ('transition matrix', 'a square matrix T whose entry in row i, column j is the probability of moving from state j to state i; each column sums to 1'),
           ('steady state', 'a state vector s with Ts = s; the long-term proportions in each state'),
           ('initial state vector', 's₀, the proportions (or probabilities) in each state at the start; after n steps the state is Tⁿs₀')],
    facts=[('A transition matrix (columns = current state) must have…', 'each column summing to 1', ['each row summing to 1', 'determinant 1', 'all entries equal'], 'Probabilities from each state.'),
           ('The steady-state vector s satisfies…', 'Ts = s', ['Ts = 0', 'T² = T', 's = Tⁿ for small n'], 'Eigenvector with eigenvalue 1.'),
           ('The steady state is an eigenvector of T with eigenvalue…', '1', ['0', '−1', 'the trace of T'], 'Ts = 1s.')],
    why=[('Explain why the steady state does not depend on the initial state for a regular Markov chain.', 'Tⁿ converges to a matrix whose columns are all the steady-state vector, so Tⁿs₀ tends to the same s whatever s₀ is (its entries sum to 1).'),
         ('Explain why each column of a transition matrix sums to 1.', 'From any current state the system must move to (or stay in) one of the states, so the probabilities of all next states add up to 1.')],
    misc=[('After many steps the state vector is Tⁿ + s₀.', 'It is the matrix product Tⁿs₀.')],
))


@R.add('ch12-st4', ALL, (1, 5), 'short')
def markov_core(rng, slot):
    c, d = slot.c, slot.d
    k = rng.choice([2, 2, 3])
    MK = [(['sunny', 'rainy', 'cloudy'], 'the weather on consecutive days', None), (['brand A', 'brand B', 'brand C'], 'customers\' choice of brand each month', ('customers', 'the brand each customer buys each month')),
          (['gym', 'pool', 'track'], 'where an athlete trains each day', ('club members', 'where each member trains each day')),
          (['bus', 'car', 'bike'], 'how a commuter travels each week', ('commuters', 'how each commuter travels each week')), (['level 1', 'level 2', 'level 3'], 'the level a player is on after each game', ('players of an online game', 'the level each player is on after each game'))]
    states, ctx, popd = pick(rng, MK if c != 'C4' else MK[1:])
    states = states[:k]
    T = np.zeros((k, k))
    for j in range(k):
        stay = round(rng.uniform(0.4, 0.85), 2)
        rest = 1 - stay
        if k == 2:
            T[j, j], T[1 - j, j] = stay, round(rest, 2)
        else:
            o = [i for i in range(k) if i != j]
            a = round(rng.uniform(0.05, rest - 0.05), 2)
            T[j, j], T[o[0], j], T[o[1], j] = stay, a, round(rest - a, 2)
    s0 = np.zeros(k)
    s0[rng.randrange(k)] = 1
    ev, V = np.linalg.eig(T)
    i1 = int(np.argmin(abs(ev - 1)))
    ss = np.real(V[:, i1])
    ss = ss / ss.sum()
    desc = '; '.join(f'from {states[j]}: ' + ', '.join(f'{states[i]} {_num(T[i, j])}' for i in range(k)) for j in range(k))
    if c == 'C1':
        if d <= 1:
            return ret(f'For {ctx}, the transition probabilities are: {desc}. Write down the transition matrix T (columns give the current state, in the order {", ".join(states)}).', mat(T), 'A1 columns sum to 1; A1 all entries correctly placed.', 2)
        s2 = np.linalg.matrix_power(T, 2) @ s0
        st0 = states[int(np.argmax(s0))]
        return ret(f'For {ctx}, the transition matrix is T = {mat(T)} (states {", ".join(states)}). Today it is {st0}. Find the probability that it is {states[0]} in 2 steps\' time.', sf(s2[0]), f'T²s₀ (M1) with s₀ = {vec(s0)}; P = {sf(s2[0])} (A1).', 2)
    if c == 'C2':
        return ret(f'For {ctx}, the transition matrix is T = {mat(T)} (states {", ".join(states)}). Explain why the long-term proportions do not depend on the initial state, and find them.', ', '.join(f'{states[i]} {sf(ss[i])}' for i in range(k)),
                   f'R1 all entries of T are positive (regular chain), so Tⁿ converges to a matrix with identical columns; R1 Tⁿs₀ → s for any s₀; A1 solve Ts = s with Σs = 1: ' + ', '.join(sf(v) for v in ss) + '.', 3, 'explain')
    if c == 'C3':
        n = rng.randint(3, 8)
        sn = np.linalg.matrix_power(T, n) @ s0
        return ret(f'For {ctx}, the transition matrix is T = {mat(T)} (states {", ".join(states)}), and the initial state is {states[int(np.argmax(s0))]}. Find the state vector after {n} steps and the steady-state vector.', f'{vec(np.round(sn, 6))}'.replace(vec(np.round(sn, 6)), '(' + ', '.join(sf(v) for v in sn) + ')') + '; (' + ', '.join(sf(v) for v in ss) + ')',
                   f'T{sup(n)}s₀ (M1) = (' + ', '.join(sf(v) for v in sn) + ') (A1); Ts = s, Σs = 1 (M1) ⇒ (' + ', '.join(sf(v) for v in ss) + ') (A1).', 4, 'numerical')
    N = rng.choice([1000, 2000, 5000, 12000])
    s0b = np.array([round(rng.uniform(0.2, 0.6), 2) for _ in range(k)])
    s0b[-1] = round(1 - s0b[:-1].sum(), 2)
    if s0b[-1] <= 0:
        return None
    s1 = T @ s0b
    s3 = np.linalg.matrix_power(T, 3) @ s0b
    return ret(f'A study follows {N} {popd[0]}: {popd[1]} follows a Markov chain with T = {mat(T)} (states {", ".join(states)}). Initially the proportions are {vec(s0b)}. (a) Explain what the entry in row 1, column 2 represents. (b) Find the expected number in each state after one period. (c) Find the proportions after three periods. (d) Find the steady-state vector. (e) Find the eigenvalues of T and explain the role of the eigenvalue 1.',
               '(b) ' + ', '.join(f'{states[i]} {sf(s1[i] * N)}' for i in range(k)) + ' (c) (' + ', '.join(sf(v) for v in s3) + ') (d) (' + ', '.join(sf(v) for v in ss) + ') (e) ' + ', '.join(nv(float(np.real(e))) for e in sorted(ev, key=lambda z: -np.real(z))),
               f'(a) R1 probability of moving from {states[1]} to {states[0]} in one period. (b) Ts₀ × {N} (M1 A1). (c) T³s₀ (A1). (d) Ts = s (M1) A1. (e) A1; R1 the eigenvector for λ = 1 is the steady state; other eigenvalues have |λ| < 1, so their contributions die away.', 9, 'multi_step', gap='G5')


# =============================================================================================
# ch13 Mathematical exploration (IA) and Paper 3
# =============================================================================================
IA_TOPICS = [
    ('the spread of a rumour in a school', 'logistic models and differential equations', 'collect data on how many students have heard a rumour each day', 'Maths and gossip'),
    ('the optimal route for a delivery driver in my town', 'graph theory: travelling salesman bounds', 'measure road distances between the delivery points', 'Maths on the road'),
    ('whether the 100 m sprint world record has a limit', 'regression and asymptotic models', 'use published world-record times since 1912', 'Running fast'),
    ('the shape of a suspension bridge cable', 'quadratic and catenary curve fitting', 'measure points on a photograph of a local bridge', 'Bridges'),
    ('the fairness of a local lottery', 'probability, expected value and χ² tests', 'record past draw results', 'Luck'),
    ('cooling of coffee in different cups', 'Newton\'s law of cooling and exponential regression', 'measure temperatures every minute with a thermometer', 'Hot drinks'),
    ('the location of a new hospital in my region', 'Voronoi diagrams and the largest empty circle', 'use map coordinates of the existing hospitals', 'Maths in health care'),
    ('my family\'s mortgage options', 'financial mathematics and amortisation', 'use real interest rates from local banks', 'Money and houses'),
    ('the volume of a vase in my house', 'volumes of revolution and the trapezoidal rule', 'measure the radius at regular heights', 'Shapes at home'),
    ('predator–prey cycles of lynx and hares', 'coupled differential equations and Euler\'s method', 'use historical fur-trade data', 'Animals and maths'),
    ('the relationship between height and arm span in my class', 'correlation, regression and t-tests', 'measure classmates with consent', 'Human bodies'),
    ('the best strategy in a board game', 'Markov chains and steady states', 'record board positions over many simulated games', 'Games'),
]

R.facts('ch13-st1', F(
    terms=[('mathematical exploration', 'the internally assessed piece of written work (12–20 pages) in which a student investigates an area of mathematics, worth 20% of the final grade'),
           ('aim of an exploration', 'a clear, focused statement of what the exploration sets out to investigate or answer'),
           ('scope of an exploration', 'the extent of the investigation: narrow enough to treat in depth within 12–20 pages, broad enough to use mathematics commensurate with the course')],
    facts=[('What is the recommended length of the mathematical exploration?', '12–20 pages', ['3–5 pages', '40–50 pages', 'no limit'], 'IB guidance.'),
           ('What percentage of the final DP grade does the exploration contribute?', '20%', ['10%', '25%', '40%'], 'Internal assessment weighting.'),
           ('Which is the best aim for an exploration?', '"To model the cooling of coffee in different cups and compare the cooling constants."', ['"To learn about calculus."', '"To show that maths is everywhere."', '"To copy a textbook proof."'], 'Specific and testable.'),
           ('Which source of data is most appropriate for an exploration?', 'data the student collects or a cited reliable database', ['made-up numbers', 'an uncited website', 'a classmate\'s finished exploration'], 'Academic honesty and validity.')],
    why=[('Explain why a focused aim is important in the exploration.', 'A focused aim gives the exploration direction, allows depth rather than superficial coverage and lets the student judge whether the aim was achieved in the conclusion.'),
         ('Explain why a topic of personal interest helps a student\'s exploration.', 'It encourages independent thinking and creativity (personal engagement), motivates data collection and leads to more meaningful reflection.')],
    evaluate=[('Choosing a well-known textbook topic (e.g. the golden ratio) is a safe choice for the exploration.', ['plenty of sources', 'mathematics is accessible'], ['hard to show personal engagement', 'often reproduces existing work without new insight'], 'It can work only if the student adds a genuinely personal angle or data; otherwise a more personal, focused question is better.')],
    misc=[('The exploration should cover as many topics from the course as possible.', 'Depth matters more than breadth: a focused exploration using relevant mathematics well scores higher than a superficial survey.')],
))


@R.add('ch13-st1', ALL, (1, 5), 'short')
def topic_core(rng, slot):
    c, d = slot.c, slot.d
    t1, t2, t3 = rng.sample(IA_TOPICS, 3)
    if c == 'C1':
        return mcq(rng, f'A student wants to investigate {t1[0]}. Which area of mathematics is most relevant?', t1[1], [t2[1], t3[1], 'Pythagoras\' theorem only'], f'{t1[0][0].upper() + t1[0][1:]} is naturally modelled with {t1[1]}.')
    if c == 'C2':
        return ret(f'A student\'s proposed exploration title is "{t1[3]}". Explain why this needs refining and suggest a focused aim using {t1[1]}.', f'e.g. "To investigate {t1[0]} using {t1[1]}."',
                   f'R1 the title is too broad/vague to explore in depth; R1 a focused aim states the specific question and method; A1 e.g. "To investigate {t1[0]} using {t1[1]}", with data: {t1[2]}.', 3, 'explain')
    if c == 'C3' and rng.random() < 0.5:
        good, bad = t1, t2
        return ret(f'Two students submit aims. Student P: "To investigate {good[0]} using {good[1]}, based on data where I {good[2]}." Student Q: "My exploration is about {bad[3].lower()}." Evaluate the two aims and suggest how Student Q could improve theirs.', 'P is focused and testable; Q is too vague',
                   f'R1 P names a specific question, the mathematics ({good[1]}) and a data source; R1 Q gives no question, method or data; A1 e.g. "To investigate {bad[0]} using {bad[1]}"; R1 Q should also say how data will be obtained ({bad[2]}).', 4, 'short')
    if c == 'C3':
        return ret(f'A student plans an exploration on {t1[0]}. Outline (i) a suitable aim, (ii) the mathematics to be used, (iii) a data source, and (iv) one possible limitation.', f'aim on {t1[0]}; {t1[1]}; {t1[2]}',
                   f'(i) A1 a specific, answerable aim; (ii) A1 {t1[1]}; (iii) A1 {t1[2]}; (iv) R1 e.g. small or biased sample, measurement error or model assumptions.', 4, 'short')
    return ret(f'Three students propose explorations: A on {t1[0]}, B on {t2[0]}, C on {t3[0]}. (a) For each, state a suitable area of mathematics. (b) Choose one and write a focused aim. (c) Describe how the student could collect or obtain data. (d) Explain how the student could show personal engagement. (e) Identify one ethical or practical issue to consider.',
               f'(a) {t1[1]}; {t2[1]}; {t3[1]}', f'(a) A1 A1 A1. (b) A1 specific aim. (c) A1 e.g. {t1[2]}. (d) R1 own data/questions, independent decisions. (e) R1 e.g. consent, safety, data privacy or reliability of sources.', 8, 'multi_step', gap='G5')


IA_CRIT = [('A', 'presentation', 4, 'the exploration is well organised, coherent and concise'),
           ('B', 'mathematical communication', 4, 'appropriate notation, symbols, terminology, diagrams and graphs are used correctly'),
           ('C', 'personal engagement', 3, 'the student shows significant independent thinking, creativity and ownership'),
           ('D', 'reflection', 3, 'there is substantial critical reflection on the results, methods, limitations and implications'),
           ('E', 'use of mathematics', 6, 'relevant mathematics commensurate with the course is used correctly, with sophistication and rigour')]

ISSUES = [('uses "x^2" and "*" from a calculator instead of proper notation', 'B', 'mathematical communication', 'write x² and use × or juxtaposition; define variables'),
          ('has no introduction stating the aim and no conclusion', 'A', 'presentation', 'add an introduction with a clear aim and a conclusion that answers it'),
          ('only reproduces a textbook derivation with no personal data or questions', 'C', 'personal engagement', 'collect personal data or pose and pursue own questions'),
          ('states the results without discussing their meaning or limitations', 'D', 'reflection', 'discuss the meaning, reliability and limitations of the results and suggest extensions'),
          ('contains errors in the differentiation used to find a maximum', 'E', 'use of mathematics', 'check and correct the mathematics; verify with technology'),
          ('includes pages of raw data tables in the main text', 'A', 'presentation', 'move raw data to an appendix and summarise the key data in the text'),
          ('uses graphs without axis labels or units', 'B', 'mathematical communication', 'label axes with quantities and units, and add titles'),
          ('uses only simple percentages, well below the level of the course', 'E', 'use of mathematics', 'use mathematics commensurate with the course, e.g. regression or calculus'),
          ('never explains why the chosen model is appropriate', 'D', 'reflection', 'justify the choice of model and compare alternatives critically'),
          ('copies a method from a website without explaining how the student adapted it', 'C', 'personal engagement', 'explain own decisions and adapt the method to the student\'s own context')]

R.facts('ch13-st2', F(
    terms=[('criterion A: presentation', 'organisation, coherence and conciseness of the exploration (maximum 4 marks)'),
           ('criterion B: mathematical communication', 'use of appropriate mathematical language, notation, multiple forms of representation and definition of key terms (maximum 4 marks)'),
           ('criterion C: personal engagement', 'evidence of significant independent thinking, creativity and ownership (maximum 3 marks)'),
           ('criterion D: reflection', 'critical reflection on results, methods, limitations and links (maximum 3 marks)'),
           ('criterion E: use of mathematics', 'relevant mathematics commensurate with the course, used correctly and with understanding (maximum 6 marks)')],
    facts=[('What is the maximum total mark for the exploration?', '20', ['24', '30', '16'], '4 + 4 + 3 + 3 + 6.'),
           ('Which criterion carries the most marks?', 'E: use of mathematics', ['A: presentation', 'C: personal engagement', 'D: reflection'], 'Six marks.'),
           ('Defining variables and labelling graphs is assessed mainly under…', 'criterion B', ['criterion C', 'criterion D', 'criterion E'], 'Mathematical communication.'),
           ('Critically discussing the limitations of a model is assessed under…', 'criterion D', ['criterion A', 'criterion B', 'criterion C'], 'Reflection.')],
    why=[('Explain why reflection should appear throughout the exploration rather than only at the end.', 'Critical reflection on each decision and result (why a model was chosen, what a value means, how reliable it is) shows depth of understanding and can reach the top descriptors, which require substantial, meaningful reflection.'),
         ('Explain why using technology alone, without explanation, may limit marks for criterion E.', 'Criterion E rewards understanding of the mathematics; results from a GDC or software must be explained and interpreted, not just reported.')],
    misc=[('Personal engagement means writing about why you like maths.', 'It is shown through independent thinking and creativity in the mathematics (own data, own questions, own approaches), not through statements of interest.')],
))


@R.add('ch13-st2', ALL, (1, 5), 'short')
def crit_core(rng, slot):
    c, d = slot.c, slot.d
    iss = rng.sample(ISSUES, 3)
    if c == 'C1':
        i = iss[0]
        return mcq(rng, f'A draft exploration {i[0]}. Which criterion is most affected?', f'{i[1]}: {i[2]}', [f'{k}: {n}' for k, n, _, _ in IA_CRIT if k != i[1]][:3], f'This concerns {i[2]}.')
    if c == 'C2' and rng.random() < 0.5:
        i, j_ = iss[0], iss[1]
        return ret(f'A teacher comments that a draft exploration {i[0]} and also {j_[0]}. Explain which criteria are affected and suggest one improvement for each.', f'criteria {i[1]} and {j_[1]}',
                   f'A1 {i[1]} ({i[2]}) and {j_[1]} ({j_[2]}); R1 {i[3]}; R1 {j_[3]}.', 3, 'explain')
    if c == 'C2':
        i = iss[0]
        return ret(f'A teacher comments that a draft exploration {i[0]}. Explain which criterion this affects and how the student should improve it.', f'criterion {i[1]} ({i[2]})',
                   f'A1 criterion {i[1]}: {i[2]}; R1 why the issue limits the descriptor achieved; R1 improvement: {i[3]}.', 3, 'explain')
    hit = {i_[1] for i_ in iss}
    sc = [rng.randint(1, mx - 1) if k in hit else rng.randint(1, mx) for k, _, mx, _ in IA_CRIT]
    tot = sum(sc)
    if c == 'C3':
        w = round(tot / 20 * 20, 2)
        return ret(f'A student\'s exploration scores A{sc[0]}, B{sc[1]}, C{sc[2]}, D{sc[3]}, E{sc[4]}. Find the total mark, the percentage of the maximum, and the contribution to the overall course score if the IA is worth 20%.', f'{tot}/20; {_num(tot * 5)}%; {_num(w)}% of the final score',
                   f'sum of criteria (M1) = {tot} (A1); {tot}/20 = {_num(tot * 5)}% (A1); × 20% = {_num(w)}% (A1).', 4, 'numerical')
    return ret(f'A draft exploration has these issues: (1) it {iss[0][0]}; (2) it {iss[1][0]}; (3) it {iss[2][0]}. (a) For each issue, identify the criterion most affected. (b) Suggest an improvement for each. (c) State the maximum mark for each criterion identified. (d) Explain why the use of mathematics (criterion E) carries the largest weighting. (e) The current scores are A{sc[0]}, B{sc[1]}, C{sc[2]}, D{sc[3]}, E{sc[4]}; find the total and the maximum possible gain.',
               f'(a) {iss[0][1]}, {iss[1][1]}, {iss[2][1]} (e) {tot}/20; gain up to {20 - tot}',
               f'(a) A1 A1 A1. (b) R1 R1 R1: {iss[0][3]}; {iss[1][3]}; {iss[2][3]}. (c) A1 ' + ', '.join(f'{k}: {mx}' for k, _, mx, _ in IA_CRIT if k in {iss[0][1], iss[1][1], iss[2][1]}) + f'. (d) R1 E (6 marks) rewards the correct, relevant and sophisticated mathematics that is the core of the exploration. (e) A1 {tot}, {20 - tot}.', 10, 'multi_step', gap='G5')


def _ssr(x, y, f):
    return float(sum((yy - f(xx)) ** 2 for xx, yy in zip(x, y)))


R.facts('ch13-st3', F(
    terms=[('modelling cycle', 'pose a question, make assumptions, build a model, test it against data, reflect and refine'),
           ('sum of squared residuals', 'SSᵣₑₛ = Σ(yᵢ − f(xᵢ))², a measure of how well a model fits the data; smaller is better'),
           ('coefficient of determination', 'R², the proportion of the variation in y explained by the model'),
           ('Paper 3 (HL)', 'a one-hour paper of two extended problems (55 marks) in which students develop and interpret a model in an unfamiliar context')],
    facts=[('Which value indicates the better fit when comparing two models of the same data?', 'the smaller sum of squared residuals', ['the larger sum of squared residuals', 'the larger number of parameters', 'the larger intercept'], 'Residuals measure misfit.'),
           ('A model fits the data well but predicts negative populations for large t. This shows…', 'the model has a limited domain of validity', ['the data are wrong', 'R² must be 0', 'the model is exact'], 'Reflect on domain.'),
           ('In Paper 3, what is usually expected at the end of a problem?', 'an interpretation or evaluation of the model in context', ['a formal proof from axioms', 'a full essay on history', 'only a numerical answer'], 'Modelling questions end with reflection.')],
    why=[('Explain why a model with a very small residual sum on the given data may still be a poor model.', 'It may overfit the data (e.g. a high-degree polynomial) and behave unrealistically outside the data range; a good model should also be consistent with the context.'),
         ('Explain why assumptions should be stated when building a model.', 'They define the conditions under which the model is valid and allow its limitations to be evaluated and refined.')],
    misc=[('If R² = 0.98 the model is correct.', 'A high R² shows a good fit to the data, but the model may still be inappropriate (wrong shape outside the range, ignored factors).')],
))


@R.add('ch13-st3', ALL, (1, 5), 'short')
def model_core(rng, slot):
    c, d = slot.c, slot.d
    xs = list(range(0, rng.choice([6, 7, 8])))
    kind = rng.choice(['exp', 'lin', 'quad'])
    a0, k = rng.uniform(20, 80), rng.uniform(0.1, 0.35)
    if kind == 'exp':
        ys = [round(a0 * math.exp(k * x) * rng.uniform(0.95, 1.05), 1) for x in xs]
    elif kind == 'lin':
        ys = [round(a0 + 8 * k * 10 * x * rng.uniform(0.9, 1.1), 1) for x in xs]
    else:
        ys = [round(a0 + 3 * x * x * rng.uniform(0.9, 1.1) + 2 * x, 1) for x in xs]
    X, Y = np.array(xs, float), np.array(ys, float)
    b1, b0 = np.polyfit(X, Y, 1)
    lin = lambda z: b0 + b1 * z
    kk, la = np.polyfit(X, np.log(Y), 1)
    ea = math.exp(la)
    ex = lambda z: ea * math.exp(kk * z)
    q2, q1, q0 = np.polyfit(X, Y, 2)
    qd = lambda z: q2 * z * z + q1 * z + q0
    S = {'linear': _ssr(xs, ys, lin), 'exponential': _ssr(xs, ys, ex), 'quadratic': _ssr(xs, ys, qd)}
    best2 = min(['linear', 'exponential'], key=S.get)
    ctx = pick(rng, [('the number of followers (thousands) of a new podcast', 'months'), ('the population of an invasive plant (hundreds of plants)', 'years'), ('the cumulative downloads (thousands) of an app', 'weeks'), ('the number of electric cars registered in a city (hundreds)', 'years')])
    data = ', '.join(f'({x}, {_num(y)})' for x, y in zip(xs, ys))
    lin_s = f'y = {sf(b1)}t {sgn(sfv(b0), fmtf=sf)}'
    ex_s = f'y = {sf(ea)}e^({sf(kk)}t)'
    if c == 'C1':
        return ret(f'Data for {ctx[0]} t {ctx[1]} after launch are (t, y): {data}. Use technology to find the equation of the exponential model y = ae^(kt) (a, k to 3 s.f.).', ex_s, f'exponential regression or linearise ln y against t (M1); a = {sf(ea)}, k = {sf(kk)} (A1 A1).', 3)
    if c == 'C2':
        return ret(f'Data for {ctx[0]} t {ctx[1]} after launch are (t, y): {data}. A linear model gives SSᵣₑₛ = {sf(S["linear"])} and an exponential model gives SSᵣₑₛ = {sf(S["exponential"])}. Explain which model fits better and why the context should also be considered.', f'{best2} fits better',
                   f'A1 smaller SSᵣₑₛ for the {best2} model; R1 SSᵣₑₛ measures the total squared vertical distance from the data; R1 e.g. exponential growth cannot continue indefinitely, so long-term predictions need a bounded (logistic) model.', 3, 'explain')
    if c == 'C3':
        return ret(f'Data for {ctx[0]} t {ctx[1]} after launch are (t, y): {data}. Find the linear model and the exponential model for the data, and calculate the sum of squared residuals for each. State which fits better.', f'{lin_s}, SS = {sf(S["linear"])}; {ex_s}, SS = {sf(S["exponential"])}; {best2}',
                   f'linear regression (A1); exponential regression (A1); SSᵣₑₛ for each (M1 A1); comparison (R1).', 5, 'numerical')
    tp = xs[-1] + rng.randint(2, 5)
    best3 = min(S, key=S.get)
    return ret(f'Data for {ctx[0]} t {ctx[1]} after launch are (t, y): {data}. (a) Find a linear model and its SSᵣₑₛ. (b) Find an exponential model y = ae^(kt) and its SSᵣₑₛ. (c) Find a quadratic model and its SSᵣₑₛ. (d) Use the best-fitting model to predict y when t = {tp}, and comment on its reliability. (e) Suggest a refinement of the model if growth is expected to level off, and identify one assumption you have made.',
               f'(a) {lin_s}, {sf(S["linear"])} (b) {ex_s}, {sf(S["exponential"])} (c) y = {sf(q2)}t² {sgn(sfv(q1), fmtf=sf)}t {sgn(sfv(q0), fmtf=sf)}, {sf(S["quadratic"])} (d) {best3}: {sf({"linear": lin, "exponential": ex, "quadratic": qd}[best3](tp))}',
               f'(a) A1 A1. (b) A1 A1. (c) A1 A1. (d) M1 A1; R1 extrapolation beyond t = {xs[-1]} is unreliable. (e) R1 logistic model with carrying capacity; R1 assumption e.g. conditions remain constant.', 12, 'multi_step', gap='G5')


R.facts('ch13-st4', F(
    terms=[('GDC', 'graphical display calculator, used in all IB AI papers for graphs, equation solving, statistics, regression and numerical calculus'),
           ('spreadsheet', 'a grid of cells in which formulas can be filled down to iterate a process, e.g. a recurrence, Euler\'s method or a loan balance'),
           ('dynamic geometry software', 'software such as GeoGebra for constructing and manipulating geometric figures and graphs, e.g. Voronoi diagrams or slider-controlled models'),
           ('statistical software', 'software for summarising data, running tests (χ², t-tests) and fitting regression models to large data sets')],
    facts=[('Which tool is most efficient for iterating uₙ₊₁ = 1.05uₙ − 20 for 30 steps?', 'a spreadsheet (fill a formula down)', ['a protractor', 'drawing a graph by hand', 'a dictionary'], 'Formulas copy down rows.'),
           ('When reporting a GDC result in an exam, you should…', 'write down the method/equation used and the answer to 3 s.f.', ['only write "by GDC"', 'give 10 decimal places', 'avoid stating the function'], 'Show the process.'),
           ('Which tool is best for quickly checking a Voronoi diagram?', 'dynamic geometry software', ['a spreadsheet', 'a χ² table', 'a scientific calculator only'], 'Interactive construction.')],
    why=[('Explain why technology does not replace understanding in modelling.', 'Software produces numbers and graphs, but the student must choose an appropriate model, check that the output is reasonable and interpret it in context.'),
         ('Explain one risk of relying on a spreadsheet for a long iterative calculation.', 'A single wrong cell reference or rounding choice is copied to every row, so errors propagate; results should be checked against a few hand calculations or a known value.')],
    misc=[('If the GDC gives a value it must be correct.', 'The result depends on the input: window settings, mode (degrees/radians) and correctly entered functions all matter, so outputs should be checked for reasonableness.')],
))


@R.add('ch13-st4', ALL, (1, 5), 'short')
def tech_core(rng, slot):
    c, d = slot.c, slot.d
    kind = rng.randrange(3)
    if kind == 0:
        u0 = rng.randint(500, 5000)
        r = rng.choice([1.02, 1.03, 1.05, 1.08, 0.95, 0.9])
        b = rng.randint(10, 200) * (1 if r < 1 else -1) * rng.choice([1, -1])
        n = rng.randint(5, 12)
        u = [u0]
        for _ in range(n):
            u.append(u[-1] * r + b)
        desc = f'uₙ₊₁ = {_num(r)}uₙ {sgn(b)}, u₀ = {u0}'
        cell = f'=A1*{_num(r)}{"+" if b >= 0 else "-"}{abs(b)}'
        ctx = pick(rng, ['the balance of a savings account (euros)', 'the number of fish in a managed lake', 'the amount of a medicine in the body (mg)', 'the population of a small town'])
        if c == 'C1':
            return ret(f'{ctx[0].upper() + ctx[1:]} is modelled by {desc}. A spreadsheet has u₀ in cell A1. Write down the formula for cell A2 that can be filled down, and use it to find u{"₀₁₂₃₄₅₆₇₈₉"[3]}.', f'{cell}; {sf(u[3], 4)}', f'A1 formula {cell}; M1 fill down; A1 u₃ = {sf(u[3], 4)}.', 3)
        if c == 'C2':
            return ret(f'{ctx[0].upper() + ctx[1:]} is modelled by {desc}. Explain why a spreadsheet is a good tool for this model and how to check it is set up correctly.', f'u₁ = {sf(u[1], 4)}',
                       f'R1 one formula filled down computes every term quickly and allows parameters to be changed; R1 check the first term or two by hand, e.g. u₁ = {_num(r)} × {u0} {sgn(b)} = {sf(u[1], 4)}; R1 use absolute references for parameters stored in cells.', 3, 'explain')
        if c == 'C3':
            sub_n = ''.join('₀₁₂₃₄₅₆₇₈₉'[int(ch)] for ch in str(n))
            return ret(f'{ctx[0].upper() + ctx[1:]} is modelled by {desc}. Use technology to find u{sub_n} and describe the long-term behaviour of the sequence.',
                       f'{sf(u[-1], 4)}; ' + (f'tends to {sf(b / (1 - r), 4)}' if r < 1 else 'grows without bound' if (u0 + b / (r - 1)) > 0 else 'decreases without bound'),
                       f'iterate (M1) u{"".join("₀₁₂₃₄₅₆₇₈₉"[int(ch)] for ch in str(n))} = {sf(u[-1], 4)} (A1); ' + (f'fixed point L = {_num(b)}/(1 − {_num(r)}) = {sf(b / (1 - r), 4)} (M1 A1).' if r < 1 else f'r > 1 so the terms move away from the fixed point {sf(b / (1 - r), 4)} (M1 A1).'), 4, 'numerical')
    if kind == 1 or c == 'C4':
        a, b2 = rng.randint(2, 9), rng.randint(5, 30)
        roots = sorted(_roots_num(lambda z: a * math.log(z + 1) - 0.1 * b2 * z + 1, 0, 200))
        f_s = f'{a}ln(x + 1) − {_num(0.1 * b2)}x + 1'
        mx, mv = argopt(lambda z: a * math.log(z + 1) - 0.1 * b2 * z + 1, 0, 100, mx=True)
        if not roots:
            return None
        if c == 'C1':
            return ret(f'Use technology to find the positive root of f(x) = {f_s}.', sf(roots[-1]), f'graph/solver (M1); x = {sf(roots[-1])} (A1).', 2)
        if c == 'C2':
            return ret(f'{name(rng)} graphs f(x) = {f_s} in the standard window −10 ≤ x ≤ 10 and reports that f has no positive root. Explain the error.', f'root at x = {sf(roots[-1])}',
                       f'R1 the window does not show the whole relevant domain; R1 f is still positive at x = 10 (f(10) = {sf(a * math.log(11) - b2 + 1)}) and decreasing; A1 a wider window shows the root x = {sf(roots[-1])}.' if a * math.log(11) - b2 + 1 > 0 else f'R1 a root lies inside the window, so it was misread; A1 x = {sf(roots[-1])}; R1 zoom in/use the solver to locate it.', 3, 'explain')
        if c == 'C3':
            return ret(f'For f(x) = {f_s}, x ≥ 0, use technology to find the maximum point and the positive root.', f'max ({sf(mx)}, {sf(mv)}); root {sf(roots[-1])}', f'max via GDC (M1) ({sf(mx)}, {sf(mv)}) (A1 A1); root {sf(roots[-1])} (A1).', 4, 'numerical')
        prof = pick(rng, ['the profit (thousand dollars) from x hundred units', 'the height (m) of a drone x seconds after launch', 'the net benefit of x hours of tutoring'])
        return ret(f'A model for {prof} is f(x) = {f_s}, x ≥ 0. (a) Sketch the graph using technology, choosing a suitable window. (b) Find the maximum value and where it occurs. (c) Find where f(x) = 0 for x > 0. (d) Find f′(x) and verify the x-coordinate of the maximum algebraically. (e) Explain one advantage of using technology here.',
                   f'(b) {sf(mv)} at x = {_num(round(mx, 4)) if abs(mx - round(mx, 4)) < 1e-6 else sf(mx)} (c) {sf(roots[-1])} (d) f′(x) = {a}/(x + 1) − {_num(0.1 * b2)} ⇒ x = {_num(round(a / (0.1 * b2) - 1, 4)) if abs(a / (0.1 * b2) - 1 - round(a / (0.1 * b2) - 1, 4)) < 1e-9 else sf(a / (0.1 * b2) - 1)}',
                   f'(a) A1 window showing max and root. (b) A1 A1. (c) A1. (d) A1; set to 0 (M1) x = {a}/{_num(0.1 * b2)} − 1 = {_num(round(a / (0.1 * b2) - 1, 4)) if abs(a / (0.1 * b2) - 1 - round(a / (0.1 * b2) - 1, 4)) < 1e-9 else sf(a / (0.1 * b2) - 1)} (A1). (e) R1 solves equations (like f(x) = 0) that have no algebraic solution.', 8, 'multi_step', gap='G5')
    n = rng.randint(6, 9)
    xs = sorted(rng.sample(range(1, 30), n))
    m_, c_ = rng.uniform(-3, 4), rng.uniform(5, 50)
    ys = [round(m_ * x + c_ + rng.gauss(0, 4), 1) for x in xs]
    r = pearson(xs, ys)
    b1, b0 = np.polyfit(xs, ys, 1)
    data = ', '.join(f'({x}, {_num(y)})' for x, y in zip(xs, ys))
    if c == 'C1':
        return ret(f'Use technology to find Pearson\'s correlation coefficient for the data (x, y): {data}.', sf(r), f'GDC/spreadsheet (M1); r = {sf(r)} (A1).', 2)
    if c == 'C2':
        return ret(f'For the data (x, y): {data}, a spreadsheet gives r = {sf(r)}. Explain how to interpret this value and why a scatter diagram should also be drawn.', f'{strength(r)} correlation',
                   f'A1 {strength(r)} correlation; R1 r only measures linear association; R1 a scatter diagram reveals non-linear patterns or outliers that r may hide.', 3, 'explain')
    return ret(f'For the data (x, y): {data}, use technology to find r and the equation of the regression line of y on x, and predict y when x = {xs[n // 2] + 1}.', f'r = {sf(r)}; y = {sf(b1)}x {sgn(sfv(b0), fmtf=sf)}; {sf(b1 * (xs[n // 2] + 1) + b0)}',
               f'r = {sf(r)} (A1); y = {sf(b1)}x {sgn(sfv(b0), fmtf=sf)} (A1 A1); prediction {sf(b1 * (xs[n // 2] + 1) + b0)} (A1) within the data range (R1).', 5, 'numerical')


@R.add('ch13-st4', 'C4', (2, 5), 'multi_step')
def tech_c4(rng, slot):
    if rng.random() < 0.5:
        P = rng.choice([150000, 220000, 300000, 450000])
        r = rng.choice([3.2, 3.8, 4.5, 5.1, 6.0])
        yrs = rng.choice([15, 20, 25, 30])
        cu = cur(rng)
        i_ = r / 1200
        n = yrs * 12
        pm = P * i_ / (1 - (1 + i_) ** -n)
        b = [P]
        for _ in range(12):
            b.append(b[-1] * (1 + i_) - pm)
        k = rng.randint(2, 5)
        pm2 = pm + k * 100
        bb, mo = P, 0
        while bb > 0 and mo < 2000:
            bb = bb * (1 + i_) - pm2
            mo += 1
        return ret(f'A family borrows {money(P, 0)} {cu} at {r}% per year, compounded monthly, over {yrs} years, and models it in a spreadsheet: column A is the month, column B the balance at the start of the month, column C the interest and column D the balance after the payment. (a) Find the monthly payment using a financial solver. (b) Write a spreadsheet formula for the interest in C2 if B2 holds the balance. (c) Find the balance after 12 payments. (d) Find the total interest paid over the whole loan. (e) Using the spreadsheet, find how many months are saved by paying an extra {k * 100} {cu} each month.',
                   f'(a) {money(pm)} {cu} (b) =B2*{_num(r)}/1200 (c) {money(b[12])} {cu} (d) {money(pm * n - P)} {cu} (e) {n - mo} months',
                   f'(a) TVM: N = {n}, I% = {r}, PV = {P}, FV = 0 (M1) A1. (b) A1. (c) iterate 12 rows or TVM with N = 12 (M1) A1. (d) {n} × payment − {P} (M1) A1. (e) fill down with payment {money(pm2)} until balance ≤ 0: {mo} months (M1) ⇒ {n - mo} saved (A1).', 10, 'multi_step', gap='G5')
    n = rng.randint(8, 12)
    xs = sorted(rng.sample(range(1, 40), n))
    a, k = rng.uniform(2, 10), rng.uniform(0.04, 0.09)
    ys = [round(a * math.exp(k * x) * rng.uniform(0.92, 1.08), 1) for x in xs]
    r = pearson(xs, ys)
    lr = pearson(xs, [math.log(y) for y in ys])
    kk, la = np.polyfit(xs, np.log(ys), 1)
    what = pick(rng, [('the number of bacteria colonies (hundreds)', 'hours'), ('the price of a collectable card (dollars)', 'months'), ('the number of solar panels installed in a region (thousands)', 'months')])
    data = ', '.join(f'({x}, {_num(y)})' for x, y in zip(xs, ys))
    return ret(f'A student uses statistical software to model {what[0]} t {what[1]} after the start: (t, y) = {data}. (a) Find Pearson\'s r for y against t. (b) Create a column of ln y and find r for ln y against t. (c) Explain which model (linear or exponential) is more appropriate. (d) Find the exponential model y = ae^(kt). (e) Use it to estimate y at t = {xs[-1] + 5} and comment on reliability.',
               f'(a) {sf(r)} (b) {sf(lr)} (c) {"exponential" if abs(lr) > abs(r) else "linear"} (d) y = {sf(math.exp(la))}e^({sf(kk)}t) (e) {sf(math.exp(la + kk * (xs[-1] + 5)))}',
               f'(a) A1. (b) M1 A1. (c) R1 |r| closer to 1 for the transformed data. (d) ln y = {sf(kk)}t {sgn(sfv(la), fmtf=sf)} (M1) ⇒ a = {sf(math.exp(la))} (A1). (e) A1; R1 extrapolation beyond the data.', 9, 'multi_step', gap='G5')


@R.add('ch04-st3', 'C4', (2, 5), 'multi_step')
def proj_c4(rng, slot):
    u = rng.randint(12, 45)
    th = rng.randint(15, 70)
    h0 = rng.choice([0, 0, 1.5, 2, 10, 20])
    ux, uy = u * cosd(th), u * sind(th)
    tf = (uy + math.sqrt(uy * uy + 2 * 9.8 * h0)) / 9.8
    R_ = ux * tf
    H = h0 + uy * uy / (2 * 9.8)
    ts = rng.choice([0.5, 1, 1.5, 2])
    if ts >= tf:
        ts = round(tf / 2, 1)
    vx, vy = ux, uy - 9.8 * ts
    who = pick(rng, [f'A golf ball is struck from a tee {"" if h0 == 0 else f"on a platform {_num(h0)} m above the fairway"}', f'A footballer kicks a ball {"from ground level" if h0 == 0 else f"from a bank {_num(h0)} m above the pitch"}', f'A water jet leaves a nozzle {"at ground level" if h0 == 0 else f"{_num(h0)} m above the ground"}', f'A stone is thrown {"from the beach" if h0 == 0 else f"from a cliff top {_num(h0)} m above the sea"}'])
    return ret(f'{who} with speed {u} m s⁻¹ at {th}° above the horizontal. Take g = 9.8 m s⁻² and ignore air resistance. (a) Show that its position vector after t seconds is r = ({sf(ux)}t, {_num(h0) + " + " if h0 else ""}{sf(uy)}t − 4.9t²). (b) Find its velocity vector and speed at t = {_num(ts)}. (c) Find the maximum height. (d) Find the time of flight and the horizontal range. (e) Explain one reason why the model overestimates the range.',
               f'(b) ({sf(vx)}, {sf(vy)}), {sf(math.hypot(vx, vy))} m s⁻¹ (c) {sf(H)} m (d) {sf(tf)} s, {sf(R_)} m',
               f'(a) components u cos θ, u sin θ (M1) AG. (b) v = ({sf(ux)}, {sf(uy)} − 9.8t) (A1); speed (M1) {sf(math.hypot(vx, vy))} (A1). (c) vertical velocity 0 (M1) {sf(H)} (A1). (d) solve height = 0 (M1) t = {sf(tf)} (A1), range {sf(R_)} (A1). (e) R1 air resistance slows the ball.', 10, 'multi_step', gap='G5')


Y1.fix_terms(R)
