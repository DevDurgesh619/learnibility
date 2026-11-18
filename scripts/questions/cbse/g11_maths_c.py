"""CBSE class 11 maths (NCERT Mathematics XI) families, chapters 11-14."""
from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Fr
from math import comb

from qbank import F, ar, mcq, num, sup, frac, name, two_names, inr, CITIES  # noqa: F401
from g11_physics_util import polish, sig, g, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401
from g11_maths_a import fs, surd, poly, lin, setstr, Q, ordn, sq_split, term, mpolish
from g11_maths_b import M, pt, pp, ind

S = 'cbse-g11-maths-ch'


def dp(x, n=2) -> str:
    """round half-up to n decimal places, with a proper minus sign."""
    q = Decimal(1).scaleb(-n)
    s = str(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))
    return s.replace('-', '−')


def p3(*xs) -> str:
    return '(' + ', '.join(fs(x) for x in xs) + ')'


def sqrt_txt(x) -> str:
    """√x simplified, exact (x a non-negative Fraction or int)."""
    return surd(Fr(x))


# ======================================================== ch11 Introduction to 3D geometry
# st1 axes, planes and octants

OCT = {(1, 1, 1): 'I', (-1, 1, 1): 'II', (-1, -1, 1): 'III', (1, -1, 1): 'IV', (1, 1, -1): 'V', (-1, 1, -1): 'VI', (-1, -1, -1): 'VII', (1, -1, -1): 'VIII'}


def _nz(r):
    return r.choice([x for x in range(-9, 10) if x])


def c11s1_octant(r):
    p = (_nz(r), _nz(r), _nz(r))
    sg = tuple(1 if v > 0 else -1 for v in p)
    o = OCT[sg]
    return mcq(f'The point {p3(*p)} lies in octant', o, r.sample([v for v in OCT.values() if v != o], 3),
               f'Signs of (x, y, z) are ({", ".join("+" if s > 0 else "−" for s in sg)}), which is octant {o}.', r)


def c11s1_plane(r):
    a, b = _nz(r), _nz(r)
    k = r.choice(['xy', 'yz', 'zx', 'x', 'y', 'z'])
    P = {'xy': (a, b, 0), 'yz': (0, a, b), 'zx': (a, 0, b), 'x': (a, 0, 0), 'y': (0, a, 0), 'z': (0, 0, a)}[k]
    ans = {'xy': 'the XY-plane', 'yz': 'the YZ-plane', 'zx': 'the ZX-plane', 'x': 'the x-axis', 'y': 'the y-axis', 'z': 'the z-axis'}[k]
    opts = ['the XY-plane', 'the YZ-plane', 'the ZX-plane', 'the x-axis', 'the y-axis', 'the z-axis']
    wrong = [o for o in opts if o != ans]
    if len(k) == 1:
        wrong = [o for o in wrong if 'plane' not in o or k not in o.lower()[4:6]]
    return mcq(f'The point {p3(*P)} lies on', ans, r.sample(wrong, 3),
               f'Zero coordinates: {", ".join(c for c, v in zip("xyz", P) if v == 0)} = 0, so the point lies on {ans}' + ('' if len(k) == 2 else ' (it lies on two coordinate planes as well)') + '.', r)


def c11s1_box(r):
    a, b, c = r.sample(range(2, 10), 3)
    who = name(r)
    verts = [(x, y, z) for x in (0, a) for y in (0, b) for z in (0, c)]
    on_xy = [v for v in verts if v[2] == 0]
    return Q(f'{who} places a closed box (cuboid) of length {a}, breadth {b} and height {c} units with one corner at the origin O and its edges along the positive x-, y- and z-axes. '
             'Write the coordinates of all eight vertices and say which of them lie in the XY-plane.',
             'vertices ' + ', '.join(p3(*v) for v in verts) + '; in the XY-plane: ' + ', '.join(p3(*v) for v in on_xy),
             f'Each coordinate is either 0 or the full edge length along that axis (2); points with z = 0 lie in the XY-plane (1).')


def c11s1_signs(r):
    sg = r.choice(list(OCT))
    o = OCT[sg]
    cond = ', '.join(f'{c} {"> 0" if s > 0 else "< 0"}' for c, s in zip('xyz', sg))
    return mcq(f'All points with {cond} lie in octant', o, r.sample([v for v in OCT.values() if v != o], 3), f'The sign pattern ({", ".join("+" if s > 0 else "−" for s in sg)}) is octant {o}.', r)


c11s1_terms = term_mcq([('XY-plane', 'the plane z = 0'), ('YZ-plane', 'the plane x = 0'), ('ZX-plane', 'the plane y = 0'), ('x-axis', 'the set of points (x, 0, 0)'),
                        ('origin', 'the point (0, 0, 0)'), ('octant', 'one of the eight regions into which the coordinate planes divide space')],
                       'Which of the following describes the {a}?', 'Which name is given to {b}?', '{a}: {b}.')

c11s1_tf = tf_mcq('coordinate axes and planes in space',
                  ['The three coordinate planes divide space into eight octants.', 'Every point on the z-axis has the form (0, 0, z).', 'The equation of the YZ-plane is x = 0.',
                   'The point (−2, 3, 4) lies in octant II.', 'Points in the XY-plane have z-coordinate 0.'],
                  ['The coordinate planes divide space into four quadrants.', 'Every point on the x-axis has the form (0, y, z).', 'The equation of the XY-plane is x = 0.',
                   'The point (2, −3, −4) lies in octant I.', 'Points on the y-axis have y-coordinate 0.'])

c11s1_ar = pool_ar([
    ('The point (0, 4, 0) lies on the y-axis.', 'Its x- and z-coordinates are both zero.', 'a', 'R explains A.'),
    ('The point (3, −2, 5) lies in octant IV.', 'In octant IV, x > 0, y < 0 and z > 0.', 'a', 'R explains A.'),
    ('The point (−1, −1, −1) lies in octant I.', 'Octant VII contains points with all coordinates negative.', 'd', 'A is false (octant VII); R is true.'),
])

c11s1_explain = pool_txt([
    ('Explain how the coordinate planes divide space into octants, and name the signs of the coordinates in octants I and VII.', 'The XY-, YZ- and ZX-planes cut space into 8 regions; I: (+, +, +), VII: (−, −, −).', '2 marks.'),
    ('Write the general forms of a point on each coordinate axis and in each coordinate plane.', 'x-axis (x, 0, 0), y-axis (0, y, 0), z-axis (0, 0, z); XY (x, y, 0), YZ (0, y, z), ZX (x, 0, z).', '2 marks.'),
])

# st2 coordinates of a point


def c11s2_foot(r):
    P = (_nz(r), _nz(r), _nz(r))
    k = r.choice(['XY', 'YZ', 'ZX', 'x', 'y', 'z'])
    x, y, z = P
    ans = {'XY': (x, y, 0), 'YZ': (0, y, z), 'ZX': (x, 0, z), 'x': (x, 0, 0), 'y': (0, y, 0), 'z': (0, 0, z)}[k]
    where = f'the {k}-plane' if len(k) == 2 else f'the {k}-axis'
    alts = [(x, y, 0), (0, y, z), (x, 0, z), (x, 0, 0), (0, y, 0), (0, 0, z)]
    return Q(f'Find the coordinates of the foot of the perpendicular from P{p3(*P)} to {where}.', p3(*ans),
             f'Dropping a perpendicular to {where} makes the coordinate{"" if len(k) == 2 else "s"} along the {"normal" if len(k) == 2 else "other two axes"} zero: {p3(*ans)}.',
             [p3(*a) for a in alts if a != ans][:3])


def c11s2_dplane(r):
    P = (_nz(r), _nz(r), _nz(r))
    k = r.choice(['XY', 'YZ', 'ZX'])
    i = {'XY': 2, 'YZ': 0, 'ZX': 1}[k]
    u = lambda v: f'{v} unit{"" if v == 1 else "s"}'
    return Q(f'Find the distance of the point {p3(*P)} from the {k}-plane.', u(abs(P[i])), f'The distance from the {k}-plane is |{"xyz"[i]}| = {abs(P[i])}.',
             [u(abs(P[(i + 1) % 3])) if abs(P[(i + 1) % 3]) != abs(P[i]) else u(abs(P[i]) + 1), f'{fs(P[i])} units' if P[i] < 0 else u(abs(P[(i + 2) % 3]) + abs(P[i])),
              f'{surd(P[0] ** 2 + P[1] ** 2 + P[2] ** 2)} units'])


def c11s2_image(r):
    P = (_nz(r), _nz(r), _nz(r))
    k = r.choice(['XY', 'YZ', 'ZX', 'origin'])
    x, y, z = P
    ans = {'XY': (x, y, -z), 'YZ': (-x, y, z), 'ZX': (x, -y, z), 'origin': (-x, -y, -z)}[k]
    where = 'the origin' if k == 'origin' else f'the {k}-plane'
    alts = [(x, y, -z), (-x, y, z), (x, -y, z), (-x, -y, -z), (x, y, 0)]
    return Q(f'Find the image (reflection) of the point {p3(*P)} in {where}.', p3(*ans),
             f'Reflection in {where} changes the sign of {"all three coordinates" if k == "origin" else "the coordinate measured perpendicular to the plane"}: {p3(*ans)}.',
             [p3(*a) for a in alts if a != ans][:3])


def c11s2_cuboid(r):
    x1, y1, z1 = r.randint(-3, 3), r.randint(-3, 3), r.randint(-3, 3)
    a, b, c = r.sample(range(2, 8), 3)
    x2, y2, z2 = x1 + a, y1 + b, z1 + c
    verts = [(x, y, z) for x in (x1, x2) for y in (y1, y2) for z in (z1, z2)]
    rest = [v for v in verts if v not in ((x1, y1, z1), (x2, y2, z2))]
    return Q(f'A cuboid has its edges parallel to the coordinate axes, and two opposite vertices at A{p3(x1, y1, z1)} and B{p3(x2, y2, z2)}. Find the coordinates of the other six vertices and the lengths of its edges.',
             ', '.join(p3(*v) for v in rest) + f'; edges {a}, {b} and {c} units',
             f'Each vertex takes its x from {{{fs(x1)}, {fs(x2)}}}, y from {{{fs(y1)}, {fs(y2)}}} and z from {{{fs(z1)}, {fs(z2)}}} (2); list the six remaining combinations (1); edge lengths are the differences of the coordinates (1).')


def c11s2_case(r):
    L, B, H = r.choice([(6, 4, 3), (8, 5, 3), (10, 6, 4), (5, 4, 3), (7, 5, 3)])
    x, y, z = r.randint(1, L - 1), r.randint(1, B - 1), r.randint(1, H - 1)
    who = name(r)
    return {'stem': f'{who} is flying a small drone inside a classroom {L} m long, {B} m wide and {H} m high. One corner of the floor is the origin, the floor edges are the x- and y-axes and the vertical edge is the z-axis. '
                    f'The drone is at P{p3(x, y, z)} (in metres).\n(i) How high is the drone above the floor? (ii) Write the coordinates of the point on the floor directly below it. '
                    f'(iii) How far is the drone from the wall in the YZ-plane? (iv) Write the coordinates of the opposite top corner of the room.',
            'answer': f'(i) {z} m (ii) {p3(x, y, 0)} (iii) {x} m (iv) {p3(L, B, H)}',
            'key': '(i) z-coordinate (1). (ii) Foot on the XY-plane (1). (iii) |x| (1). (iv) (length, breadth, height) (1).'}


c11s2_tf = tf_mcq('coordinates of a point in space',
                  ['The distance of (x, y, z) from the XY-plane is |z|.', 'The foot of the perpendicular from (x, y, z) to the YZ-plane is (0, y, z).',
                   'The image of (x, y, z) in the ZX-plane is (x, −y, z).', 'A point is determined by an ordered triple of real numbers.'],
                  ['The distance of (x, y, z) from the XY-plane is |x|.', 'The foot of the perpendicular from (x, y, z) to the x-axis is (0, y, z).',
                   'The image of (x, y, z) in the XY-plane is (−x, −y, z).', 'Each point in space needs only two coordinates.'])

c11s2_ar = pool_ar([
    ('The foot of the perpendicular from (3, −4, 5) to the XY-plane is (3, −4, 0).', 'On the XY-plane z = 0.', 'a', 'R explains A.'),
    ('The distance of (2, −3, 6) from the YZ-plane is 2.', 'The distance from the YZ-plane is the absolute value of the x-coordinate.', 'a', 'R explains A.'),
    ('The image of (1, 2, 3) in the YZ-plane is (1, −2, −3).', 'Reflection in the YZ-plane changes only the sign of x.', 'd', 'A is false: the image is (−1, 2, 3); R is true.'),
])

c11s2_explain = pool_txt([
    ('Explain how the coordinates of a point P in space are found using perpendiculars to the coordinate planes.', 'Draw perpendiculars from P to the YZ-, ZX- and XY-planes; their signed lengths are x, y and z.', '2 marks.'),
    ('How do the coordinates of a point change on reflection in each coordinate plane?', 'XY: z → −z; YZ: x → −x; ZX: y → −y.', '2 marks.'),
])

# st3 distance formula


def _d2(P, Q_):
    return sum((a - b) ** 2 for a, b in zip(P, Q_))


def c11s3_dist(r):
    P = tuple(r.randint(-6, 7) for _ in range(3))
    Q_ = tuple(r.randint(-6, 7) for _ in range(3))
    if P == Q_:
        raise ValueError
    d2 = _d2(P, Q_)
    return Q(f'Find the distance between the points {p3(*P)} and {p3(*Q_)}.', f'{surd(d2)} units',
             f'd = √[(x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²] = √{d2}' + (f' = {surd(d2)}' if surd(d2) != f'√{d2}' else '') + '.', [f'{surd(sum(abs(a - b) for a, b in zip(P, Q_)))} units', f'{d2} units', f'{surd(sum((a + b) ** 2 for a, b in zip(P, Q_)) or 1)} units'])


def c11s3_origin(r):
    P = (_nz(r), _nz(r), _nz(r))
    d2 = sum(v * v for v in P)
    return mcq(f'The distance of the point {p3(*P)} from the origin is', surd(d2), [surd(d2 + 1), str(d2), surd(abs(P[0] + P[1] + P[2])) if abs(P[0] + P[1] + P[2]) not in (d2, d2 + 1) and P[0] + P[1] + P[2] else surd(d2 + 3)],
               f'√(x² + y² + z²) = √{d2}' + (f' = {surd(d2)}' if surd(d2) != f'√{d2}' else '') + '.', r)


def c11s3_collinear(r):
    A = tuple(r.randint(-4, 4) for _ in range(3))
    d = tuple(r.choice([-2, -1, 1, 2, 3]) for _ in range(3))
    s, t = sorted(r.sample([1, 2, 3, -1, -2], 2))
    B = tuple(a + s * k for a, k in zip(A, d))
    C = tuple(a + t * k for a, k in zip(A, d))
    pts_ = sorted([(0, A), (s, B), (t, C)])
    P1, P2, P3 = (p for _, p in pts_)
    u = surd(sum(k * k for k in d))
    l12, l23, l13 = surd(_d2(P1, P2)), surd(_d2(P2, P3)), surd(_d2(P1, P3))
    return Q(f'Show that the points P{p3(*A)}, Q{p3(*B)} and R{p3(*C)} are collinear.', f'the two shorter distances {l12} and {l23} add up to the longest, {l13}, so the points are collinear',
             f'Find the three distances: {l12}, {l23}, {l13} (2); the sum of the two smaller equals the largest (1); hence collinear (1).',
             ['the points form a right triangle', 'the points form an equilateral triangle', 'the points are not collinear'])


def c11s3_tri(r):
    kind = r.choice(['right', 'iso', 'equi'])
    if kind == 'right':
        A = tuple(r.randint(-3, 3) for _ in range(3))
        u = (r.choice([1, 2, -1]), r.choice([1, 2, -2]), 0)
        v = (-u[1], u[0], r.choice([1, 2, 3]))
        B = tuple(a + k for a, k in zip(A, u))
        C = tuple(a + k for a, k in zip(A, v))
        ans = 'right-angled'
    elif kind == 'iso':
        A = tuple(r.randint(-3, 3) for _ in range(3))
        k = r.choice([1, 2])
        B = (A[0] + 3 * k, A[1] + 4 * k, A[2])
        C = (A[0] + 4 * k, A[1] + 3 * k, A[2] + r.choice([0, 1, 2]))
        if _d2(A, B) != _d2(A, C) or _d2(B, C) in (_d2(A, B), 0):
            C = (A[0] + 5 * k, A[1], A[2])
        ans = 'isosceles'
    else:
        a = r.choice([1, 2, 3])
        A, B, C = (a, 0, 0), (0, a, 0), (0, 0, a)
        ans = 'equilateral'
    ds = sorted([_d2(A, B), _d2(B, C), _d2(A, C)])
    if kind == 'right' and ds[0] + ds[1] != ds[2]:
        raise ValueError
    if kind == 'iso' and not (ds[0] == ds[1] or ds[1] == ds[2]):
        raise ValueError
    if kind != 'equi' and ds[0] == ds[2]:
        raise ValueError
    if kind == 'iso' and ds[0] + ds[1] == ds[2]:
        ans = 'right-angled isosceles'
    if kind == 'right' and (ds[0] == ds[1]):
        ans = 'right-angled isosceles'
    sides = ', '.join(surd(x) for x in [_d2(A, B), _d2(B, C), _d2(A, C)])
    return Q(f'Show that the points A{p3(*A)}, B{p3(*B)} and C{p3(*C)} are the vertices of {"an" if ans[0] in "ie" else "a"} {ans} triangle.', f'AB, BC, CA = {sides}; the triangle is {ans}',
             f'Find AB², BC², CA² = {_d2(A, B)}, {_d2(B, C)}, {_d2(A, C)} (2); compare: ' + ('two are equal' if 'isosceles' in ans else '') + (' and ' if ans == 'right-angled isosceles' else '') +
             ('the sum of two squares equals the third (Pythagoras)' if 'right' in ans else '') + ('all three are equal' if ans == 'equilateral' else '') + ' (2).')


def c11s3_k(r):
    P = tuple(r.randint(-4, 5) for _ in range(3))
    dx, dy, dz = r.choice([(2, 3, 6), (1, 2, 2), (2, 6, 9), (4, 4, 7), (3, 4, 12), (6, 2, 3)])
    i = r.randrange(3)
    dlt = [dx, dy, dz]
    d = math.isqrt(dx * dx + dy * dy + dz * dz)
    Q_ = list(P)
    for j in range(3):
        if j != i:
            Q_[j] = P[j] + dlt[j] * r.choice([1, -1])
    ks = sorted({P[i] + dlt[i], P[i] - dlt[i]})
    shown = ['k' if j == i else fs(Q_[j]) for j in range(3)]
    return Q(f'Find the value(s) of k if the distance between {p3(*P)} and ({", ".join(shown)}) is {d} units.', ' or '.join(f'k = {fs(k)}' for k in ks),
             f'Square both sides: (k − {pp(P[i])})² + {sum(dlt[j] ** 2 for j in range(3) if j != i)} = {d * d} (1) ⇒ (k − {pp(P[i])})² = {dlt[i] ** 2} (1) ⇒ k = {" or ".join(fs(k) for k in ks)} (1).',
             [f'k = {fs(ks[1])} only', ' or '.join(f'k = {fs(-k)}' for k in ks), ' or '.join(f'k = {fs(k + 1)}' for k in ks)])


def c11s3_locus(r):
    A = tuple(r.randint(-4, 5) for _ in range(3))
    B = tuple(r.randint(-4, 5) for _ in range(3))
    if A == B:
        raise ValueError
    # PA = PB: 2(b-a).P = |B|^2 - |A|^2
    co = [2 * (b - a) for a, b in zip(A, B)]
    rhs = sum(b * b for b in B) - sum(a * a for a in A)
    gg = math.gcd(math.gcd(math.gcd(abs(co[0]), abs(co[1])), abs(co[2])), abs(rhs)) or 1
    co = [c // gg for c in co]
    rhs //= gg
    if next(c for c in co if c) < 0:
        co = [-c for c in co]
        rhs = -rhs
    out = ''
    for c, v in zip(co, 'xyz'):
        out += term(c, v, out == '')
    out += term(-rhs, '', False)
    eq = out + ' = 0'
    return Q(f'Find the equation of the set of points P(x, y, z) that are equidistant from A{p3(*A)} and B{p3(*B)}.', eq,
             f'PA² = PB² (1); expand (x − {pp(A[0])})² + … = (x − {pp(B[0])})² + … (2); the squares of x, y, z cancel (1): {eq}, a plane (1).')


def c11s3_case(r):
    who = name(r)
    A = (0, 0, 0)
    B = (r.randint(3, 8), r.randint(2, 6), 0)
    C = (B[0], B[1], r.randint(2, 6))
    ab2, ac2 = _d2(A, B), _d2(A, C)
    return {'stem': f'{who} models a tent pole set-up with coordinates in metres. The peg is at the origin O, the foot of a vertical pole is at F{p3(*B)} and the top of the pole is at T{p3(*C)}. A rope runs straight from O to T.\n'
                    '(i) Find the distance OF along the ground. (ii) Find the height of the pole. (iii) Find the length of the rope OT. (iv) Verify your answer to (iii) using Pythagoras in triangle OFT.',
            'answer': f'(i) {surd(ab2)} m (ii) {C[2]} m (iii) {surd(ac2)} m (iv) OF² + FT² = {ab2} + {C[2] ** 2} = {ac2} = OT²',
            'key': '(i) distance formula in the XY-plane (1). (ii) difference of z-coordinates (1). (iii) 3D distance formula (1). (iv) FT is vertical, so angle OFT = 90° (1).'}


c11s3_tf = tf_mcq('the distance formula in space',
                  ['The distance between (x₁, y₁, z₁) and (x₂, y₂, z₂) is √[(x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²].', 'The distance of (x, y, z) from the origin is √(x² + y² + z²).',
                   'Three points A, B, C are collinear if AB + BC = AC.', 'The distance between (1, 2, 3) and (1, 2, 7) is 4.'],
                  ['The distance between two points in space is |x₂ − x₁| + |y₂ − y₁| + |z₂ − z₁|.', 'The distance of (3, 4, 12) from the origin is 19.',
                   'The distance between (1, 1, 1) and (2, 2, 2) is 3.', 'Distance in space can be negative.'])

c11s3_ar = pool_ar([
    ('The distance of (2, 3, 6) from the origin is 7.', '√(4 + 9 + 36) = √49.', 'a', 'R explains A.'),
    ('The points (0, 7, −10), (1, 6, −6) and (4, 9, −6) form an isosceles triangle.', 'Two of the three sides have length √18.', 'a', 'R explains A.'),
    ('The distance between (1, 2, 3) and (4, 6, 3) is 7.', 'The distance formula in space adds the squares of the differences of the coordinates.', 'd', 'A is false (distance 5); R is true.'),
])

c11s3_explain = pool_txt([
    ('Derive the distance formula between two points in space.', 'Draw a cuboid with PQ as a diagonal; apply Pythagoras twice: PQ² = (x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)².', '2 marks.'),
    ('How can the distance formula be used to show that three points are collinear?', 'Find the three distances; if the sum of two equals the third, the points lie on a line.', '2 marks.'),
])


# ======================================================== ch12 Limits and Derivatives
# st1 intuitive limits, LHL and RHL

def c12s1_piece(r):
    c = r.randint(-2, 4)
    a, b = r.choice([1, 2, 3, -1]), r.randint(-5, 5)
    p, q = r.choice([1, 2, -2, 3]), r.randint(-5, 5)
    same = r.random() < 0.4
    if same:
        q = a * c + b - p * c
    L, R = a * c + b, p * c + q
    exist = L == R
    f1, f2 = lin(a, b), lin(p, q)
    ans = f'LHL = {fs(L)}, RHL = {fs(R)}; ' + (f'the limit exists and equals {fs(L)}' if exist else 'the limit does not exist')
    return Q(M(f'f(x) = {f1} for x < {c} and f(x) = {f2} for x ≥ {c}. Find the left- and right-hand limits of f at x = {c}. Does lim(x→{c}) f(x) exist?'), ans,
             f'LHL: use {f1} as x → {c}⁻: {fs(L)} (1); RHL: use {f2} as x → {c}⁺: {fs(R)} (1); the limit exists only if LHL = RHL (1).'.replace('→ -', '→ −'),
             [f'LHL = {fs(R)}, RHL = {fs(L)}; ' + ('the limit does not exist' if exist else f'the limit exists and equals {fs(L)}'), f'LHL = {fs(L)}, RHL = {fs(R)}; ' + ('the limit does not exist' if exist else f'the limit exists and equals {fs(R)}'),
              f'LHL = {fs(L + 1)}, RHL = {fs(R)}; the limit does not exist'])


def c12s1_k(r):
    c = r.randint(-2, 4)
    a, b = r.choice([1, 2, 3]), r.randint(-5, 5)
    m = r.choice([2, 3, -1, 1])
    L = a * c * c + b
    k = L - m * c
    return Q(M(f'f(x) = {poly([a, 0, b])} for x ≤ {c} and f(x) = {m if abs(m) != 1 else ("" if m == 1 else "−")}x + k for x > {c}. Find k if lim(x→{c}) f(x) exists.'), f'k = {fs(k)}',
             f'LHL = {a} × {pp(c)}² + {pp(b)} = {fs(L)} (1); RHL = {m} × {pp(c)} + k (1); equate: k = {fs(k)} (1).',
             [f'k = {fs(L)}', f'k = {fs(L + m * c)}', f'k = {fs(-k)}' if k else 'k = 1'])


def c12s1_special(r):
    return pool_mcq([
        ('lim(x→0) |x|/x', 'does not exist (LHL = −1, RHL = 1)', ['equals 1', 'equals 0', 'equals −1'], 'For x < 0, |x|/x = −1; for x > 0 it is 1.'),
        ('lim(x→2⁻) [x], where [x] is the greatest integer function, equals', '1', ['2', '0', 'does not exist'], 'Just left of 2, [x] = 1.'),
        ('lim(x→2⁺) [x], where [x] is the greatest integer function, equals', '2', ['1', '3', 'does not exist'], 'Just right of 2, [x] = 2.'),
        ('lim(x→3) [x], where [x] is the greatest integer function,', 'does not exist (LHL = 2, RHL = 3)', ['equals 3', 'equals 2', 'equals 2.5'], 'LHL ≠ RHL.'),
        ('lim(x→0) x/|x| as x → 0⁺ equals', '1', ['−1', '0', 'does not exist'], 'For x > 0, |x| = x.'),
        ('lim(x→1) (x² − 1)/(x − 1)', 'equals 2', ['does not exist since the function is undefined at 1', 'equals 0', 'equals 1'], 'The limit depends on values near 1, not at 1: x + 1 → 2.'),
    ])(r)


def c12s1_direct(r):
    a = r.randint(-4, 6)
    cs = [r.randint(-3, 4) for _ in range(3)]
    if cs[0] == 0:
        cs[0] = 1
    v = cs[0] * a * a + cs[1] * a + cs[2]
    return Q(M(f'Evaluate lim(x→{a}) ({poly(cs)}).'), fs(v), f'A polynomial is continuous, so substitute x = {fs(a)}: {fs(v)}.',
             [fs(v + 1), fs(cs[0] * a * a - cs[1] * a + cs[2]) if cs[1] * a else fs(v - 2), fs(cs[2])])


c12s1_tf = tf_mcq('limits',
                  ['lim(x→a) f(x) exists if and only if the left-hand and right-hand limits exist and are equal.', 'A function may have a limit at a point where it is not defined.',
                   'lim(x→0) |x|/x does not exist.', 'For a polynomial p, lim(x→a) p(x) = p(a).'],
                  ['lim(x→a) f(x) is always equal to f(a).', 'If f(a) is not defined, lim(x→a) f(x) cannot exist.', 'The left-hand limit is found by taking x slightly greater than a.',
                   'lim(x→3) [x] = 3, where [x] is the greatest integer function.'])

c12s1_ar = pool_ar([
    ('lim(x→0) |x|/x does not exist.', 'The left-hand limit is −1 and the right-hand limit is 1.', 'a', 'R explains A.'),
    ('lim(x→1) (x² − 1)/(x − 1) = 2.', 'The function is not defined at x = 1.', 'b', 'Both true; R does not explain the value of the limit.'),
    ('lim(x→2) [x] = 2, where [x] is the greatest integer function.', 'The left-hand limit of [x] at 2 is 1.', 'd', 'A is false (LHL 1, RHL 2); R is true.'),
])

c12s1_explain = pool_txt([
    ('Explain the meaning of lim(x→a) f(x) = l, and the roles of the left-hand and right-hand limits.', 'f(x) gets arbitrarily close to l as x approaches a from both sides; LHL and RHL must both equal l.', '2 marks.'),
    ('Why does lim(x→0) 1/x not exist?', 'As x → 0⁺, 1/x grows without bound; as x → 0⁻, it decreases without bound; no finite common value.', '2 marks.'),
])

# st2 algebra of limits


def c12s2_factor(r):
    a = r.choice([x for x in range(-5, 6) if x])
    b = r.randint(-6, 6)
    k = r.choice([1, 1, 2, 3])
    # (x - a)(k x + b) / (x - a) style, numerator expanded
    num_ = [k, b - k * a, -a * b]
    v = k * a + b
    den = lin(1, -a)
    return Q(M(f'Evaluate lim(x→{a}) ({poly(num_)})/({den}).'), fs(v),
             M(f'Direct substitution gives 0/0 (1); factorise: ({den})({lin(k, b)})/({den}) = {lin(k, b)} (1); put x = {a}: {fs(v)} (1).'),
             [fs(v + 2 * k * a) if 2 * k * a else fs(v + 1), '0', fs(-v) if v else '1'])


def c12s2_xn(r):
    a = r.choice([1, 2, 3, -1, -2])
    m, n = r.sample(range(2, 8), 2)
    kind = r.choice(['one', 'ratio'])
    if kind == 'one':
        v = n * Fr(a) ** (n - 1)
        return Q(f'Evaluate lim(x→{fs(a)}) (x{sup(n)} − {pp(a)}{sup(n)})/(x − {pp(a)}).', fs(v),
                 f'Use lim(x→a) (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹ (1): {n}({fs(a)}){sup(n - 1)} = {fs(v)} (1).', [fs(Fr(a) ** (n - 1)), fs(n * Fr(a) ** n), fs((n - 1) * Fr(a) ** (n - 2))])
    v = Fr(m, n) * Fr(a) ** (m - n)
    return Q(f'Evaluate lim(x→{fs(a)}) (x{sup(m)} − {pp(a)}{sup(m)})/(x{sup(n)} − {pp(a)}{sup(n)}).', fs(v),
             f'Divide numerator and denominator by (x − a) and use (xⁿ − aⁿ)/(x − a) → naⁿ⁻¹ (2): ({m}a{sup(m - 1)})/({n}a{sup(n - 1)}) = {fs(Fr(m, n))}a{sup(m - n) if m - n > 0 else "^(" + str(m - n) + ")"} = {fs(v)} (1).'.replace('^(-', '^(−'),
             [fs(Fr(m, n)), fs(Fr(n, m) * Fr(a) ** (n - m)), fs(Fr(m, n) * Fr(a) ** (m - n + 1))])


def c12s2_rational(r):
    a = r.choice([1, 2, 3, -1, -2])
    b, c = r.randint(-4, 4), r.randint(-4, 4)
    if b == a or c == a:
        raise ValueError
    # numerator (x - a)(x - b)(x + 0)?  use (x-a)(x-b) / ((x-a)(x-c))
    num_ = [1, -(a + b), a * b]
    den = [1, -(a + c), a * c]
    v = Fr(a - b, a - c)
    return Q(M(f'Evaluate lim(x→{a}) ({poly(num_)})/({poly(den)}).'), fs(v),
             M(f'Both vanish at x = {a} (1); factorise: ({lin(1, -a)})({lin(1, -b)})/(({lin(1, -a)})({lin(1, -c)})) (1); cancel and substitute: ({fs(a - b)})/({fs(a - c)}) = {fs(v)} (1).'),
             [fs(Fr(b, c)) if c else '0', fs(1 / v) if v else '1', '0' if v else '1'])


def c12s2_sqrt(r):
    a = r.choice([1, 4, 9, 16, 25])
    k = r.choice([1, 2, 3])
    s = math.isqrt(a)
    v = Fr(k, 2 * s)
    kx = 'x' if k == 1 else f'{k}x'
    return Q(f'Evaluate lim(x→0) (√({a} + {kx}) − {s})/x.', fs(v),
             f'Rationalise: multiply by (√({a} + {kx}) + {s}) (1); numerator becomes {kx} (1); limit = {k}/(√{a} + {s}) (1) = {fs(v)} (1).',
             [fs(Fr(k, s)), fs(Fr(1, 2 * s)) if k != 1 else fs(Fr(1, s)), fs(2 * s * k)])


def c12s2_algebra(r):
    a = r.randint(1, 4)
    f_ = r.randint(-5, 8)
    g_ = r.choice([x for x in range(-5, 8) if x])
    c = r.randint(2, 5)
    kind = r.choice(['sum', 'prod', 'quot'])
    if kind == 'sum':
        v, e = c * f_ + g_, f'{c}f(x) + g(x)'
    elif kind == 'prod':
        v, e = Fr(f_ * g_), 'f(x)·g(x)'
    else:
        v, e = Fr(f_, g_), 'f(x)/g(x)'
    return mcq(f'If lim(x→{a}) f(x) = {fs(f_)} and lim(x→{a}) g(x) = {fs(g_)}, then lim(x→{a}) [{e}] equals', fs(v),
               [fs(v + 1), fs(Fr(g_, f_)) if f_ and Fr(g_, f_) != v else fs(v - 2), fs(f_ + g_) if f_ + g_ != v else fs(v + 3)], f'Algebra of limits: {fs(v)}.', r)


c12s2_tf = tf_mcq('the algebra of limits',
                  ['lim [f(x) + g(x)] = lim f(x) + lim g(x), when both limits exist.', 'lim [f(x)/g(x)] = lim f(x)/lim g(x), provided lim g(x) ≠ 0.',
                   'lim(x→a) (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹.', 'A 0/0 form can often be removed by factorising and cancelling.'],
                  ['lim [f(x)/g(x)] = lim f(x)/lim g(x) even if lim g(x) = 0.', 'A 0/0 form means the limit is 0.', 'lim(x→a) (xⁿ − aⁿ)/(x − a) = aⁿ.',
                   'lim(x→a) k f(x) = k + lim f(x).'])

c12s2_ar = pool_ar([
    ('lim(x→2) (x² − 4)/(x − 2) = 4.', '(x² − 4)/(x − 2) = x + 2 for x ≠ 2.', 'a', 'R explains A.'),
    ('lim(x→1) (x¹⁰ − 1)/(x − 1) = 10.', 'lim(x→a) (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹.', 'a', 'R explains A.'),
    ('lim(x→3) (x² − 9)/(x − 3) = 0.', 'Substituting x = 3 gives 0/0.', 'd', 'A is false (limit 6); R is true.'),
])

c12s2_explain = pool_txt([
    ('Prove that lim(x→a) (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹ for a positive integer n.', 'xⁿ − aⁿ = (x − a)(xⁿ⁻¹ + xⁿ⁻²a + … + aⁿ⁻¹); cancel and let x → a: n terms each aⁿ⁻¹.', '2 marks.'),
    ('What does the 0/0 form mean and how is it handled in limits of rational functions?', 'It is indeterminate; factorise, cancel the common factor (x − a) and substitute.', '2 marks.'),
])

# st3 trigonometric limits


def c12s3_sin(r):
    a, b = r.sample([1, 2, 3, 4, 5, 7], 2)
    kind = r.choice(['sinx', 'sinsin', 'tan'])
    if kind == 'sinx':
        e, v = f'sin {a}x/({b}x)' if b != 1 else f'sin {a}x/x', Fr(a, b)
    elif kind == 'sinsin':
        e, v = f'sin {a}x/sin {b}x', Fr(a, b)
    else:
        e, v = f'tan {a}x/({b}x)' if b != 1 else f'tan {a}x/x', Fr(a, b)
    e = e.replace(' 1x', ' x')
    return Q(f'Evaluate lim(x→0) {e}.', fs(v), f'Write it in terms of sin θ/θ → 1 (and tan θ/θ → 1) with θ = {a if a != 1 else ""}x{" and " + (str(b) if b != 1 else "") + "x" if kind == "sinsin" else ""}: limit = {a}/{b}{" = " + fs(v) if fs(v) != f"{a}/{b}" else ""}.',
             [fs(Fr(b, a)), '1', fs(a * b)])


def c12s3_cos(r):
    a = r.choice([1, 2, 3, 4, 5])
    kind = r.choice(['sq', 'ratio'])
    if kind == 'sq':
        v = Fr(a * a, 2)
        ax = 'x' if a == 1 else f'{a}x'
        return Q(f'Evaluate lim(x→0) (1 − cos {ax})/x².', fs(v), f'1 − cos {ax} = 2 sin²({fs(Fr(a, 2))}x) (1); = 2 × ({fs(Fr(a, 2))})² × [sin({fs(Fr(a, 2))}x)/({fs(Fr(a, 2))}x)]² → {fs(v)} (2).'.replace('(1x)', '(x)').replace('1x', 'x'),
                 [fs(a * a), fs(Fr(a, 2)), '0'])
    b = r.choice([x for x in [1, 2, 3, 4, 5] if x != a])
    v = Fr(a * a, b * b)
    return Q(f'Evaluate lim(x→0) (1 − cos {a}x)/(1 − cos {b}x).'.replace(' 1x', ' x'), fs(v), f'Use 1 − cos kx = 2 sin²(kx/2) and sin θ/θ → 1 (2): ({a}²/2)/({b}²/2) = {fs(v)} (1).',
             [fs(Fr(a, b)), fs(Fr(b * b, a * a)), '1'])


def c12s3_combo(r):
    a, b = r.randint(1, 5), r.randint(1, 5)
    kind = r.choice(['axcos', 'sin+'])
    if kind == 'axcos':
        v = Fr(a + 1, b)
        return Q(f'Evaluate lim(x→0) ({a if a > 1 else ""}x + x cos x)/({b if b > 1 else ""} sin x).'.replace('( sin', '(sin'), fs(v),
                 f'Divide numerator and denominator by x (1): ({a} + cos x)/({b} × sin x/x) (2) → ({a} + 1)/{b} = {fs(v)} (1).', [fs(Fr(a, b)), fs(Fr(a + 1, b + 1)), fs(Fr(b, a + 1))])
    c, d = r.randint(1, 4), r.randint(1, 4)
    v = Fr(a + b, c + d)
    return Q(f'Evaluate lim(x→0) (sin {a}x + {b}x)/({c}x + sin {d}x).'.replace(' 1x', ' x').replace('+ 1x', '+ x').replace('(1x', '(x'), fs(v),
             f'Divide by x (1): (sin {a}x/x + {b})/({c} + sin {d}x/x) (2) → ({a} + {b})/({c} + {d}) = {fs(v)} (1).', [fs(Fr(a, d)), fs(Fr(b, c)), fs(Fr(a * b, c * d)) if Fr(a * b, c * d) != v else '1'])


def c12s3_mcq(r):
    a, b = r.sample([1, 2, 3, 4], 2)
    v = Fr(a * a, b * b)
    return mcq(f'lim(x→0) (cos {a}x − 1)/(cos {b}x − 1) equals'.replace(' 1x', ' x'), fs(v), [fs(Fr(a, b)), fs(Fr(b * b, a * a)), fs(-v)],
               f'Both are of the form −2 sin²(kx/2); the ratio tends to ({a}/{b})² = {fs(v)}.', r)


c12s3_tf = tf_mcq('trigonometric limits',
                  ['lim(x→0) sin x/x = 1, with x in radians.', 'lim(x→0) (1 − cos x)/x = 0.', 'lim(x→0) tan x/x = 1.', 'For 0 < x < π/2, cos x < sin x/x < 1.'],
                  ['lim(x→0) sin x/x = 0.', 'lim(x→0) sin x/x = 1 when x is in degrees.', 'lim(x→0) (1 − cos x)/x = 1.', 'lim(x→0) sin 3x/x = 1.'])

c12s3_ar = pool_ar([
    ('lim(x→0) sin 4x/x = 4.', 'sin 4x/x = 4 × (sin 4x/4x) and sin θ/θ → 1.', 'a', 'R explains A.'),
    ('lim(x→0) tan x/x = 1.', 'tan x/x = (sin x/x) × (1/cos x).', 'a', 'R explains A.'),
    ('lim(x→0) sin x°/x = 1, where x° means x degrees.', 'x° = πx/180 radians.', 'd', 'A is false (limit π/180); R is true.'),
])

c12s3_explain = pool_txt([
    ('Prove that lim(x→0) (1 − cos x)/x = 0.', '(1 − cos x)/x = 2 sin²(x/2)/x = sin(x/2) × [sin(x/2)/(x/2)] → 0 × 1 = 0.', '2 marks.'),
    ('Outline the proof of lim(x→0) sin x/x = 1 using areas in a unit circle.', 'Compare areas: triangle < sector < triangle gives cos x < sin x/x < 1; squeeze as x → 0.', '2 marks.'),
])

# st4 derivative from first principles


def c12s4_point(r):
    a, b, c = r.choice([1, 2, 3, -1]), r.randint(-5, 5), r.randint(-5, 9)
    x0 = r.randint(-3, 4)
    v = 2 * a * x0 + b
    return Q(M(f'Using the definition f′(a) = lim(h→0) [f(a + h) − f(a)]/h, find the derivative of f(x) = {poly([a, b, c])} at x = {x0}.'), fs(v),
             M(f'f({x0} + h) − f({x0}) = {poly([a, 2 * a * x0 + b, 0], "h")} (2); divide by h and let h → 0 (1): f′({x0}) = {fs(v)} (1).'),
             [fs(a * x0 * x0 + b * x0 + c), fs(a * x0 + b), fs(2 * a * x0)])


def c12s4_fp(r):
    kind = r.choice(['quad', 'cube', 'lin'])
    if kind == 'lin':
        a, b = r.choice([2, 3, -4, 5]), r.randint(-7, 7)
        f_, d = lin(a, b), fs(a)
        steps = f'f(x + h) − f(x) = {a}h (1); [f(x + h) − f(x)]/h = {a} (1); limit = {a} (1).'
    elif kind == 'quad':
        a, b = r.choice([1, 2, 3]), r.randint(-5, 5)
        f_, d = poly([a, b, r.randint(-5, 5)]), lin(2 * a, b)
        steps = f'f(x + h) − f(x) = {2 * a}xh + {a}h² + ({b})h (1); divide by h: {2 * a}x + {a}h + ({b}) (1); let h → 0: {d} (1).'
    else:
        a = r.choice([1, 2])
        f_, d = poly([a, 0, 0, 0]), poly([3 * a, 0, 0])
        steps = f'(x + h)³ − x³ = 3x²h + 3xh² + h³ (1); divide by h and let h → 0 (1): {d} (1).'
    return Q(M(f'Find the derivative of f(x) = {f_} from first principles.'), M(f'f′(x) = {d}'), M(steps),
             [M(f'f′(x) = {f_}'), M(f"f′(x) = {lin(2 * a, 0) if kind != 'lin' else '0'}"), M(f"f′(x) = {poly([a, 0]) if kind == 'quad' else '1'}")])


def c12s4_recip(r):
    kind = r.choice(['recip', 'sqrt', 'recip2'])
    a = r.randint(-5, 5)
    if kind == 'recip':
        xa = lin(1, a)
        return Q(M(f'Find the derivative of f(x) = 1/({xa}) from first principles.'), M(f'f′(x) = −1/({xa})²'),
                 M(f'f(x + h) − f(x) = [({xa}) − ({xa} + h)]/[({xa} + h)({xa})] = −h/[({xa} + h)({xa})] (2); divide by h (1); let h → 0 (1): −1/({xa})² (1).'))
    if kind == 'sqrt':
        return Q('Find the derivative of f(x) = √x (x > 0) from first principles.', 'f′(x) = 1/(2√x)',
                 '[√(x + h) − √x]/h (1); rationalise: h/[h(√(x + h) + √x)] (2); let h → 0: 1/(2√x) (2).')
    return Q('Find the derivative of f(x) = 1/x² from first principles.', 'f′(x) = −2/x³',
             '[1/(x + h)² − 1/x²]/h = −(2x + h)/[x²(x + h)²] (3); let h → 0: −2x/x⁴ = −2/x³ (2).')


def c12s4_trig(r):
    kind = r.choice(['sin', 'cos', 'sinax', 'tan'])
    if kind == 'sin':
        return Q('Find the derivative of sin x from first principles.', 'cos x',
                 '[sin(x + h) − sin x]/h = 2 cos(x + h/2) sin(h/2)/h (2) = cos(x + h/2) × [sin(h/2)/(h/2)] (1) → cos x × 1 = cos x (2).')
    if kind == 'cos':
        return Q('Find the derivative of cos x from first principles.', '−sin x',
                 '[cos(x + h) − cos x]/h = −2 sin(x + h/2) sin(h/2)/h (2) = −sin(x + h/2) × [sin(h/2)/(h/2)] (1) → −sin x (2).')
    if kind == 'tan':
        return Q('Find the derivative of tan x from first principles.', 'sec²x',
                 '[tan(x + h) − tan x]/h = sin h/[h cos(x + h) cos x] (2); sin h/h → 1 (1); limit = 1/cos²x = sec²x (2).')
    a = r.choice([2, 3, 4, 5])
    return Q(f'Find the derivative of sin {a}x from first principles.', f'{a} cos {a}x',
             f'[sin({a}x + {a}h) − sin {a}x]/h = 2 cos({a}x + {a}h/2) sin({a}h/2)/h (2) = {a} cos({a}x + {a}h/2) × [sin({a}h/2)/({a}h/2)] (1) → {a} cos {a}x (2).')


c12s4_def = pool_mcq([
    ('The derivative of f at x = a is defined as', 'lim(h→0) [f(a + h) − f(a)]/h', ['[f(a + h) − f(a)]/h for h = 1', 'lim(h→0) [f(a + h) + f(a)]/h', 'lim(h→0) f(a + h)/h'], 'Definition of the derivative.'),
    ('Geometrically, f′(a) is', 'the slope of the tangent to y = f(x) at x = a', ['the y-intercept of the curve', 'the area under the curve up to a', 'the value of f at a'], 'Limit of chord slopes.'),
    ('The derivative of a constant function is', '0', ['1', 'the constant itself', 'not defined'], 'f(x + h) − f(x) = 0.'),
    ('If s(t) is the position of a particle, s′(t) gives its', 'instantaneous velocity', ['acceleration', 'average speed over [0, t]', 'distance from the origin'], 'Rate of change of position.'),
])


def c12s4_case(r):
    a = r.choice([2, 3, 4, 5])
    b = r.choice([1, 2, 3, 4, 5])
    t0 = r.randint(2, 6)
    h = Fr(1, 10)
    avg = (a * (t0 + h) ** 2 + b * (t0 + h) - a * t0 * t0 - b * t0) / h
    who = name(r)
    return {'stem': f'{who} rolls a ball down a slope. The distance travelled is s(t) = {a}t² + {b if b > 1 else ""}t metres after t seconds.\n'
                    f'(i) Find the average velocity between t = {t0} s and t = {t0}.1 s. (ii) Write [s({t0} + h) − s({t0})]/h in simplest form. '
                    f'(iii) Find the instantaneous velocity at t = {t0} s. (iv) Find the velocity at any time t.',
            'answer': f'(i) {dp(avg, 1)} m/s (ii) {2 * a * t0 + b} + {a}h (iii) {2 * a * t0 + b} m/s (iv) v(t) = {2 * a}t + {b} m/s',
            'key': '(i) [s(t₂) − s(t₁)]/(t₂ − t₁) (1). (ii) expand and divide by h (1). (iii) let h → 0 (1). (iv) s′(t) from first principles (1).'}


c12s4_tf = tf_mcq('the derivative',
                  ["f′(a) = lim(h→0) [f(a + h) − f(a)]/h, if the limit exists.", 'The derivative of f(x) = x² is 2x.', 'The derivative of a constant is zero.',
                   'f′(a) is the slope of the tangent to y = f(x) at x = a.', 'The derivative of x is 1.'],
                  ['f′(a) = [f(a + h) − f(a)]/h for any h.', 'The derivative of x² is x.', 'The derivative of a constant is 1.', 'f′(a) is the area under the curve.', 'The derivative of 1/x is 1/x².'])

c12s4_ar = pool_ar([
    ('The derivative of x² at x = 3 is 6.', '[(3 + h)² − 9]/h = 6 + h → 6.', 'a', 'R explains A.'),
    ('The derivative of 5x + 7 is 5.', 'The slope of the line y = 5x + 7 is 5 everywhere.', 'a', 'R explains A.'),
    ('The derivative of √x at x = 0 is 0.', 'f(x) = √x is defined at x = 0.', 'd', 'A is false: the limit 1/√h does not exist; R is true.'),
])

c12s4_explain = pool_txt([
    ('Explain the geometric meaning of the derivative of f at x = a.', 'The chord slope [f(a + h) − f(a)]/h tends to the slope of the tangent at (a, f(a)) as h → 0.', '2 marks.'),
    ('Find, from first principles, the derivative of f(x) = x and of f(x) = c, a constant.', 'x: [(x + h) − x]/h = 1; c: (c − c)/h = 0.', '1 + 1 marks.'),
])

# st5 algebra of derivatives


def c12s5_poly(r):
    n = r.randint(3, 5)
    cs = [r.randint(-6, 7) for _ in range(n + 1)]
    if cs[0] == 0:
        cs[0] = 2
    d = [c * (n - i) for i, c in enumerate(cs[:-1])]
    return Q(f'Differentiate f(x) = {poly(cs)}.', f'f′(x) = {poly(d)}', 'Use d/dx(xⁿ) = nxⁿ⁻¹ term by term; the derivative of the constant is 0.',
             [f'f′(x) = {poly(d[:-1] + [d[-1] + cs[-1]])}' if cs[-1] else f'f′(x) = {poly(cs[:-1])}', f'f′(x) = {poly([c * (n - i - 1) for i, c in enumerate(cs[:-1])])}', f'f′(x) = {poly(cs[:-1])}'])


def c12s5_prod(r):
    a, b = r.choice([1, 2, 3]), r.randint(-5, 5)
    c, d = r.choice([1, 2, -1]), r.randint(-5, 5)
    # (a x + b)(c x^2 + d)
    prod_ = [a * c, b * c, a * d, b * d]
    der = [3 * a * c, 2 * b * c, a * d]
    x0 = r.randint(-2, 3)
    val = 3 * a * c * x0 * x0 + 2 * b * c * x0 + a * d
    f1, f2 = lin(a, b), poly([c, 0, d])
    return Q(M(f'Using the product rule, find the derivative of ({f1})({f2}) and its value at x = {x0}.'), M(f'{poly(der)}; at x = {x0}: {fs(val)}'),
             M(f"(uv)′ = u′v + uv′ = {a}({f2}) + ({f1})({2 * c}x) (1) = {poly(der)} (1); substitute x = {x0}: {fs(val)} (1)."),
             [M(f'{poly([2 * a * c, 0])}; at x = {x0}: {fs(2 * a * c * x0)}'), M(f'{poly([3 * a * c, 2 * b * c, a * d + 1])}; at x = {x0}: {fs(val + 1)}'), M(f'{poly(prod_)}; at x = {x0}: {fs(a * c * x0 ** 3 + b * c * x0 * x0 + a * d * x0 + b * d)}')])


def c12s5_quot(r):
    a, b, c, d = r.choice([1, 2, 3]), r.randint(-5, 5), r.choice([1, 2, -1]), r.randint(-5, 5)
    nume = a * d - b * c
    if nume == 0:
        raise ValueError
    f1, f2 = lin(a, b), lin(c, d)
    return Q(M(f'Differentiate ({f1})/({f2}).'), M(f'{fs(nume)}/({f2})²'),
             M(f"(u/v)′ = (u′v − uv′)/v² = [{a}({f2}) − {c}({f1})]/({f2})² (2) = {fs(nume)}/({f2})² (1)."),
             [M(f'{fs(-nume)}/({f2})²'), M(f'{fs(Fr(a, c))}'), M(f'{fs(a * d + b * c)}/({f2})²')])


def c12s5_trig(r):
    return pool_mcq([
        ('The derivative of x sin x is', 'sin x + x cos x', ['x cos x', 'cos x', 'sin x − x cos x'], 'Product rule.'),
        ('The derivative of sin x/x is', '(x cos x − sin x)/x²', ['cos x', '(sin x − x cos x)/x²', 'cos x/x'], 'Quotient rule.'),
        ('The derivative of sec x is', 'sec x tan x', ['tan²x', '−sec x tan x', 'cosec x'], 'd/dx (1/cos x) = sin x/cos²x.'),
        ('The derivative of cot x is', '−cosec²x', ['cosec²x', 'sec²x', '−sec²x'], 'Quotient rule on cos x/sin x.'),
        ('The derivative of 2 sin x − 3 cos x is', '2 cos x + 3 sin x', ['2 cos x − 3 sin x', '−2 cos x + 3 sin x', '2 sin x + 3 cos x'], '(cos x)′ = −sin x.'),
        ('The derivative of sin x cos x is', 'cos 2x', ['−sin 2x', 'cos²x', '2 sin x cos x'], 'cos²x − sin²x = cos 2x.'),
        ('The derivative of tan x is', 'sec²x', ['sec x tan x', '−cosec²x', 'cot x'], 'Quotient rule on sin x/cos x.'),
        ('The derivative of x² cos x is', '2x cos x − x² sin x', ['−2x sin x', '2x cos x + x² sin x', 'x² sin x'], 'Product rule.'),
    ])(r)


def c12s5_value(r):
    n = r.choice([50, 60, 80, 100, 120])
    return Q(f'For f(x) = x{sup(n)}/{n} + x{sup(n - 1)}/{n - 1} + … + x²/2 + x + 1, prove that f′(1) = {n} f′(0).', f'f′(1) = {n} and f′(0) = 1, so f′(1) = {n} f′(0)',
             f'f′(x) = x{sup(n - 1)} + x{sup(n - 2)} + … + x + 1 (2); f′(1) = 1 + 1 + … ({n} terms) = {n} (1); f′(0) = 1 (1); hence f′(1) = {n} f′(0) (1).')


def c12s5_case(r):
    a, b, c = r.choice([Fr(1, 10), Fr(1, 5), Fr(1, 20)]), r.choice([10, 15, 20, 25]), r.choice([500, 800, 1000, 1200])
    x0 = r.choice([10, 20, 30, 40, 50])
    firm = r.choice(['a handloom unit', 'a pickle maker', 'a bicycle workshop', 'a furniture shop'])
    city = r.choice(CITIES)
    mc = 2 * a * x0 + b
    cx2 = f'x²/{a.denominator}'
    d2 = 2 * a
    cx = f'x/{d2.denominator}' if d2.numerator == 1 else f'{d2.numerator}x/{d2.denominator}'
    return {'stem': f'For {firm} in {city}, the cost of making x items is C(x) = {cx2} + {b}x + {c} rupees.\n'
                    f'(i) What is the fixed cost? (ii) Find the marginal cost C′(x). (iii) Find the marginal cost when {x0} items are made. (iv) Interpret your answer to (iii).',
            'answer': f'(i) {inr(c)} (ii) C′(x) = {cx} + {b} (iii) ₹{fs(mc)} (iv) making one more item after {x0} costs about ₹{fs(mc)}',
            'key': '(i) C(0) (1). (ii) derivative term by term (1). (iii) substitute (1). (iv) rate of change of cost (1).'}


c12s5_tf = tf_mcq('the algebra of derivatives',
                  ['(u + v)′ = u′ + v′.', '(uv)′ = u′v + uv′.', '(u/v)′ = (u′v − uv′)/v², v ≠ 0.', 'd/dx (xⁿ) = nxⁿ⁻¹.', 'd/dx (cos x) = −sin x.'],
                  ['(uv)′ = u′v′.', '(u/v)′ = u′/v′.', 'd/dx (cos x) = sin x.', 'd/dx (xⁿ) = xⁿ⁻¹.', 'd/dx (tan x) = sec x tan x.'])

c12s5_ar = pool_ar([
    ('The derivative of x³ + 2x is 3x² + 2.', 'The derivative of a sum is the sum of the derivatives.', 'a', 'R explains A.'),
    ('The derivative of x sin x is sin x + x cos x.', 'The product rule is (uv)′ = u′v + uv′.', 'a', 'R explains A.'),
    ('The derivative of sin x/x is cos x.', '(u/v)′ = (u′v − uv′)/v².', 'd', 'A is false: it is (x cos x − sin x)/x²; R is true.'),
])

c12s5_explain = pool_txt([
    ('State the product and quotient rules for derivatives and use one to differentiate x² sin x.', '(uv)′ = u′v + uv′; (u/v)′ = (u′v − uv′)/v²; (x² sin x)′ = 2x sin x + x² cos x.', '2 marks.'),
    ('Why is the derivative of a product not the product of the derivatives? Give an example.', 'For x × x = x², (x²)′ = 2x but (x)′(x)′ = 1.', '2 marks.'),
])


# ======================================================== ch13 Statistics
# st1 range and mean deviation (ungrouped)

def _data_int_mean(r, n=None, lo=2, hi=60):
    n = n or r.randint(6, 10)
    while True:
        xs = [r.randint(lo, hi) for _ in range(n)]
        if sum(xs) % n == 0 and len(set(xs)) > 2:
            return xs


def _median(xs):
    s = sorted(xs)
    n = len(s)
    return Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)


def c13s1_range(r):
    xs = [r.randint(5, 95) for _ in range(r.randint(7, 11))]
    v = max(xs) - min(xs)
    return Q(f'Find the range of the data: {", ".join(map(str, xs))}.', str(v), f'Range = largest − smallest = {max(xs)} − {min(xs)} = {v}.',
             [str(max(xs) + min(xs)), str(max(xs)), str(v - 1)])


def c13s1_mdmean(r):
    xs = _data_int_mean(r)
    m = Fr(sum(xs), len(xs))
    md = sum(abs(x - m) for x in xs) / len(xs)
    return Q(f'Find the mean deviation about the mean for the data: {", ".join(map(str, xs))}.', dp(md, 2),
             f'Mean = {sum(xs)}/{len(xs)} = {fs(m)} (1); Σ|xᵢ − x̄| = {fs(sum(abs(x - m) for x in xs))} (1); MD = {fs(sum(abs(x - m) for x in xs))}/{len(xs)} = {dp(md, 2)} (1).',
             [dp(md * len(xs) / (len(xs) - 1), 2), dp(sum(abs(x - _median(xs)) for x in xs) / len(xs) + Fr(1, 2), 2), dp(m, 2)])


def c13s1_mdmed(r):
    xs = [r.randint(3, 60) for _ in range(r.choice([7, 9, 11, 8, 10]))]
    md_ = _median(xs)
    s = sum(abs(x - md_) for x in xs)
    v = s / len(xs)
    return Q(f'Find the mean deviation about the median for the data: {", ".join(map(str, xs))}.', dp(v, 2),
             f'Arrange in order; median = {fs(md_)} (1); Σ|xᵢ − M| = {fs(s)} (1); MD = {fs(s)}/{len(xs)} = {dp(v, 2)} (1).',
             [dp(sum(abs(x - Fr(sum(xs), len(xs))) for x in xs) / len(xs) + Fr(3, 10), 2), dp(s / (len(xs) - 1), 2), dp(md_, 2)])


def c13s1_compare(r):
    a, b = two_names(r)
    xa = _data_int_mean(r, 6, 20, 80)
    xb = _data_int_mean(r, 6, 20, 80)
    ma, mb = Fr(sum(xa), 6), Fr(sum(xb), 6)
    da, db = sum(abs(x - ma) for x in xa) / 6, sum(abs(x - mb) for x in xb) / 6
    if da == db:
        raise ValueError
    more = a if da < db else b
    return Q(f'The runs scored by {a} in 6 innings are {", ".join(map(str, xa))} and by {b} are {", ".join(map(str, xb))}. Using the mean deviation about the mean, who is more consistent?',
             f'MD: {a} {dp(da)}, {b} {dp(db)}; {more} is more consistent',
             f'Means: {fs(ma)} and {fs(mb)} (1); mean deviations: {dp(da)} and {dp(db)} (2); the smaller MD means less scatter, so {more} is more consistent (1).',
             [f'MD: {a} {dp(da)}, {b} {dp(db)}; {b if more == a else a} is more consistent', f'Means: {a} {fs(ma)}, {b} {fs(mb)}; {a if ma > mb else b} is more consistent', 'Both are equally consistent'])


def c13s1_change(r):
    k = r.randint(2, 9)
    md = Fr(r.randint(10, 60), 10)
    kind = r.choice(['add', 'mul'])
    if kind == 'add':
        return mcq(f'The mean deviation of a data set is {dp(md, 1)}. If {k} is added to every observation, the new mean deviation is', dp(md, 1),
                   [dp(md + k, 1), dp(md * k, 1), dp(md - k, 1) if md > k else dp(md + 2 * k, 1)], 'Adding a constant shifts every value and the mean equally; deviations are unchanged.', r)
    return mcq(f'The mean deviation of a data set is {dp(md, 1)}. If every observation is multiplied by {k}, the new mean deviation is', dp(md * k, 1),
               [dp(md, 1), dp(md + k, 1), dp(md * k * k, 1)], f'Every deviation is multiplied by {k}, so the MD becomes {k} × {dp(md, 1)}.', r)


c13s1_terms = term_mcq([('range', 'the difference between the largest and the smallest observation'), ('mean deviation about a', 'Σ|xᵢ − a|/n'),
                        ('measure of dispersion', 'a number describing how scattered the data are'), ('median', 'the middle value of the data arranged in order')],
                       'Which of the following describes the {a}?', 'Which term means {b}?', '{a}: {b}.')

c13s1_tf = tf_mcq('range and mean deviation',
                  ['The range depends only on the two extreme observations.', 'The mean deviation about the median is never greater than the mean deviation about any other point.',
                   'Adding a constant to every observation does not change the mean deviation.', 'Absolute values are used so that deviations do not cancel.'],
                  ['The range uses every observation.', 'Σ(xᵢ − x̄) is a good measure of dispersion.', 'Multiplying every observation by 3 leaves the mean deviation unchanged.',
                   'The mean deviation can be negative.'])

c13s1_ar = pool_ar([
    ('Σ(xᵢ − x̄) cannot be used as a measure of dispersion.', 'The sum of deviations from the mean is always zero.', 'a', 'R explains A.'),
    ('The range is not a good measure of dispersion when there are outliers.', 'The range depends only on the largest and smallest values.', 'a', 'R explains A.'),
    ('The mean deviation of 4, 4, 4, 4 is 4.', 'All the observations are equal.', 'd', 'A is false (MD = 0); R is true.'),
])

c13s1_explain = pool_txt([
    ('Why are absolute values taken in the definition of mean deviation?', 'Deviations from the mean add up to zero; absolute values measure the size of the spread.', '2 marks.'),
    ('Explain why the range is a crude measure of dispersion.', 'It uses only the two extreme values and ignores how the rest are spread.', '2 marks.'),
])

# st2 mean deviation for grouped data


def _freq_table(r, xs_choices=None):
    while True:
        xs = xs_choices or sorted(r.sample(range(2, 40, r.choice([2, 3, 5])), r.randint(5, 6)))
        fs_ = [r.randint(2, 12) for _ in xs]
        N = sum(fs_)
        S_ = sum(x * f for x, f in zip(xs, fs_))
        if S_ % N == 0:
            return xs, fs_, N, Fr(S_, N)


def c13s2_discrete(r):
    xs, fq, N, m = _freq_table(r)
    s = sum(f * abs(x - m) for x, f in zip(xs, fq))
    v = s / N
    return Q(f'Find the mean deviation about the mean for the data:\nxᵢ: {", ".join(map(str, xs))}\nfᵢ: {", ".join(map(str, fq))}', dp(v),
             f'N = {N}, Σfᵢxᵢ = {int(m * N)}, mean = {fs(m)} (1); Σfᵢ|xᵢ − x̄| = {fs(s)} (2); MD = {fs(s)}/{N} = {dp(v)} (1).',
             [dp(s / len(xs)), dp(v + Fr(1, 2)), dp(m)])


def _classes(r):
    w = r.choice([10, 5, 20])
    start = r.choice([0, 10, 20, 0])
    k = r.randint(5, 6)
    cls = [(start + i * w, start + (i + 1) * w) for i in range(k)]
    fq = [r.randint(2, 15) for _ in cls]
    return cls, fq, w


def c13s2_cont(r):
    cls, fq, w = _classes(r)
    N = sum(fq)
    mids = [Fr(a + b, 2) for a, b in cls]
    m = sum(f * x for f, x in zip(fq, mids)) / N
    s = sum(f * abs(x - m) for f, x in zip(fq, mids))
    v = s / N
    return Q(f'Find the mean deviation about the mean for the data:\nClass: {", ".join(f"{a}–{b}" for a, b in cls)}\nFrequency: {", ".join(map(str, fq))}', dp(v),
             f'Class marks {", ".join(fs(x) for x in mids)} (1); N = {N}, mean = {fs(sum(f * x for f, x in zip(fq, mids)))}/{N} = {dp(m)} (1); Σfᵢ|xᵢ − x̄| = {dp(s)} (2); MD = {dp(v)} (1).',
             [dp(s / len(cls)), dp(m), dp(v * 2)])


def _grouped_median(cls, fq):
    N = sum(fq)
    cf = 0
    for (a, b), f in zip(cls, fq):
        if cf + f >= Fr(N, 2):
            return a + (Fr(N, 2) - cf) / f * (b - a), (a, b), cf, f
        cf += f


def c13s2_median(r):
    cls, fq, w = _classes(r)
    N = sum(fq)
    M_, (l, u), cf, f = _grouped_median(cls, fq)
    mids = [Fr(a + b, 2) for a, b in cls]
    s = sum(fi * abs(x - M_) for fi, x in zip(fq, mids))
    v = s / N
    return Q(f'Find the mean deviation about the median for the data:\nClass: {", ".join(f"{a}–{b}" for a, b in cls)}\nFrequency: {", ".join(map(str, fq))}', f'median {dp(M_)}; MD {dp(v)}',
             f'N = {N}, N/2 = {fs(Fr(N, 2))}; median class {l}–{u} (cf before it {cf}, f = {f}) (1); median = {l} + ({fs(Fr(N, 2))} − {cf})/{f} × {u - l} = {dp(M_)} (2); '
             f'Σfᵢ|xᵢ − M| = {dp(s)} (1); MD = {dp(v)} (1).',
             [f'median {dp(M_)}; MD {dp(s / len(cls))}', f'median {dp(Fr(l + u, 2))}; MD {dp(v + 1)}', f'median {dp(M_ + w)}; MD {dp(v)}'])


def c13s2_case(r):
    city = r.choice(CITIES)
    w0 = r.choice([300, 350, 400, 450])
    wages = [w0 + 50 * i for i in range(5)]
    fq = [r.randint(3, 12) for _ in wages]
    N = sum(fq)
    m = Fr(sum(w * f for w, f in zip(wages, fq)), N)
    s = sum(f * abs(w - m) for w, f in zip(wages, fq))
    return {'stem': f'A small factory in {city} pays daily wages as follows.\nWage (₹): {", ".join(map(str, wages))}\nNumber of workers: {", ".join(map(str, fq))}\n'
                    '(i) How many workers are there? (ii) Find the mean daily wage. (iii) Find the mean deviation of the wages about the mean. (iv) What does the mean deviation tell the owner?',
            'answer': f'(i) {N} (ii) ₹{dp(m)} (iii) ₹{dp(s / N)} (iv) on average a worker\'s wage differs from the mean wage by about ₹{dp(s / N)}',
            'key': '(i) Σf (1). (ii) Σfx/Σf (1). (iii) Σf|x − x̄|/N (1). (iv) interpretation as typical spread (1).'}


c13s2_formula = pool_mcq([
    ('For a frequency distribution, the mean deviation about the mean is', 'Σfᵢ|xᵢ − x̄|/N', ['Σ|xᵢ − x̄|/N', 'Σfᵢ(xᵢ − x̄)/N', 'Σfᵢ(xᵢ − x̄)²/N'], 'N = Σfᵢ.'),
    ('For continuous classes, the xᵢ used in the mean deviation are', 'the class marks (mid-points)', ['the upper class limits', 'the lower class limits', 'the frequencies'], 'Each class is represented by its mid-point.'),
    ('The median of grouped data is found from', 'l + [(N/2 − C)/f] × h', ['l + [(N − C)/f] × h', '(l + u)/2 of the first class', 'Σfᵢxᵢ/N'], 'Standard median formula.'),
    ('In the median formula for grouped data, C stands for', 'the cumulative frequency of the class before the median class', ['the frequency of the median class', 'the class width', 'the total frequency'], 'Definition.'),
])

c13s2_tf = tf_mcq('mean deviation of grouped data',
                  ['For grouped data, MD about the mean = Σfᵢ|xᵢ − x̄|/Σfᵢ.', 'In continuous classes, deviations are measured from class marks.',
                   'To find MD about the median, first find the median class using cumulative frequencies.', 'The mean deviation has the same unit as the data.'],
                  ['For grouped data, MD = Σ|xᵢ − x̄|/n, ignoring frequencies.', 'The median class is the class with the highest frequency.',
                   'The mean deviation is measured in square units.', 'Class limits are used as xᵢ in continuous distributions.'])

c13s2_ar = pool_ar([
    ('Class marks are used as xᵢ when finding the mean deviation of continuous data.', 'All observations in a class are assumed to be at its mid-point.', 'a', 'R explains A.'),
    ('The median class is the class whose cumulative frequency first reaches N/2.', 'Half the observations lie on either side of the median.', 'a', 'R explains A.'),
    ('The mean deviation about the mean of grouped data is Σfᵢ(xᵢ − x̄)/N.', 'The mean deviation uses absolute deviations.', 'd', 'A is false: Σfᵢ(xᵢ − x̄) = 0; R is true.'),
])

c13s2_explain = pool_txt([
    ('Write the steps to find the mean deviation about the median for a continuous frequency distribution.', 'Find cumulative frequencies, the median class and the median; find |xᵢ − M| from class marks; MD = Σfᵢ|xᵢ − M|/N.', '2 marks.'),
    ('What assumption is made when using class marks in the mean deviation of grouped data?', 'That all observations in a class are concentrated at its mid-point.', '2 marks.'),
])

# st3 variance and standard deviation


def c13s3_raw(r):
    xs = _data_int_mean(r, r.randint(5, 8), 2, 30)
    n = len(xs)
    m = Fr(sum(xs), n)
    var = sum((x - m) ** 2 for x in xs) / n
    return Q(f'Find the mean and variance of the data: {", ".join(map(str, xs))}. Also find the standard deviation (to 2 decimal places).',
             f'mean {fs(m)}; variance {fs(var)}; SD {dp(math.sqrt(var))}',
             f'x̄ = {sum(xs)}/{n} = {fs(m)} (1); Σ(xᵢ − x̄)² = {fs(var * n)} (1); σ² = {fs(var * n)}/{n} = {fs(var)} (1); σ = √({fs(var)}) ≈ {dp(math.sqrt(var))} (1).',
             [f'mean {fs(m)}; variance {fs(var * n / (n - 1))}; SD {dp(math.sqrt(var * n / (n - 1)))}', f'mean {fs(m)}; variance {dp(math.sqrt(var))}; SD {fs(var)}',
              f'mean {fs(m)}; variance {fs(sum(abs(x - m) for x in xs) / n)}; SD {dp(math.sqrt(sum(abs(x - m) for x in xs) / n))}'])


def c13s3_natural(r):
    n = r.randint(5, 30)
    kind = r.choice(['nat', 'even', 'mult'])
    if kind == 'nat':
        v = Fr(n * n - 1, 12)
        what = f'the first {n} natural numbers'
        key = f'σ² = (n² − 1)/12 = ({n * n} − 1)/12 = {fs(v)}.'
    elif kind == 'even':
        v = Fr(4 * (n * n - 1), 12)
        what = f'the first {n} even natural numbers'
        key = f'2, 4, …, {2 * n} is 2 × (1, …, {n}), so σ² = 4 × (n² − 1)/12 = {fs(v)}.'
    else:
        k = r.choice([3, 5, 10])
        v = Fr(k * k * (n * n - 1), 12)
        what = f'the first {n} multiples of {k}'
        key = f'{k}, {2 * k}, …, {k * n} is {k} × (1, …, {n}), so σ² = {k}² × (n² − 1)/12 = {fs(v)}.'
    return Q(f'Find the variance of {what}.', fs(v), key, [fs(Fr(n * n + 1, 12)), fs(Fr(n + 1, 2)), fs(v * 2)])


def c13s3_freq(r):
    xs, fq, N, m = _freq_table(r)
    S2 = sum(f * (x - m) ** 2 for x, f in zip(xs, fq))
    var = S2 / N
    return Q(f'Find the variance and standard deviation of the data:\nxᵢ: {", ".join(map(str, xs))}\nfᵢ: {", ".join(map(str, fq))}', f'variance {dp(var)}; SD {dp(math.sqrt(var))}',
             f'N = {N}, x̄ = {fs(m)} (1); Σfᵢ(xᵢ − x̄)² = {fs(S2)} (2); σ² = {fs(S2)}/{N} = {dp(var)} (1); σ = {dp(math.sqrt(var))} (1).',
             [f'variance {dp(S2 / len(xs))}; SD {dp(math.sqrt(S2 / len(xs)))}', f'variance {dp(math.sqrt(var))}; SD {dp(var)}', f'variance {dp(var + 1)}; SD {dp(math.sqrt(var + 1))}'])


def c13s3_cv(r):
    m1, s1 = r.choice([40, 50, 60, 80, 100]), r.choice([4, 5, 6, 8, 10, 12])
    m2, s2 = r.choice([30, 45, 55, 70, 90]), r.choice([3, 5, 7, 9, 11])
    c1, c2 = Fr(s1 * 100, m1), Fr(s2 * 100, m2)
    if c1 == c2:
        raise ValueError
    who = r.choice([('Shop A', 'Shop B'), ('Factory P', 'Factory Q'), ('Batch X', 'Batch Y')])
    more = who[0] if c1 > c2 else who[1]
    return Q(f'The daily sales of {who[0]} have mean ₹{m1}k and SD ₹{s1}k; those of {who[1]} have mean ₹{m2}k and SD ₹{s2}k. Find the coefficient of variation of each and say which shows greater variability.',
             f'CV {who[0]} {dp(c1)}%, {who[1]} {dp(c2)}%; {more} is more variable',
             f'CV = σ/x̄ × 100 (1); {who[0]}: {s1}/{m1} × 100 = {dp(c1)}% (1); {who[1]}: {s2}/{m2} × 100 = {dp(c2)}% (1); the larger CV is more variable: {more} (1).',
             [f'CV {who[0]} {dp(c1)}%, {who[1]} {dp(c2)}%; {who[1] if more == who[0] else who[0]} is more variable', f'{who[0] if s1 > s2 else who[1]} is more variable because its SD is larger',
              f'CV {who[0]} {dp(Fr(m1, s1))}%, {who[1]} {dp(Fr(m2, s2))}%; {more} is more variable'])


def c13s3_correct(r):
    n = r.choice([10, 20, 25, 30, 40])
    m = r.choice([20, 30, 40, 50])
    sd = r.choice([2, 3, 4, 5])
    wrong, right = r.sample(range(10, 70), 2)
    Sx = n * m
    Sx2 = n * (sd * sd + m * m)
    Sx_c = Sx - wrong + right
    Sx2_c = Sx2 - wrong * wrong + right * right
    mc = Fr(Sx_c, n)
    var_c = Fr(Sx2_c, n) - mc * mc
    if var_c <= 0:
        raise ValueError
    return Q(f'The mean and standard deviation of {n} observations are {m} and {sd}. It was later found that one observation was wrongly copied as {wrong} instead of {right}. Find the correct mean and standard deviation.',
             f'mean {dp(mc)}; SD {dp(math.sqrt(var_c))}',
             f'Σx = {Sx}, Σx² = n(σ² + x̄²) = {Sx2} (2); correct: Σx = {Sx_c}, Σx² = {Sx2_c} (1); mean = {fs(mc)} = {dp(mc)} (1); σ² = Σx²/n − x̄² = {dp(var_c, 4)}, σ = {dp(math.sqrt(var_c))} (1).',
             [f'mean {dp(mc)}; SD {sd}', f'mean {m}; SD {dp(math.sqrt(var_c))}', f'mean {dp(mc)}; SD {dp(var_c)}'])


def c13s3_case(r):
    a, b = two_names(r)
    while True:
        xa = _data_int_mean(r, 5, 20, 90)
        xb = _data_int_mean(r, 5, 20, 90)
        ma, mb = Fr(sum(xa), 5), Fr(sum(xb), 5)
        va = sum((x - ma) ** 2 for x in xa) / 5
        vb = sum((x - mb) ** 2 for x in xb) / 5
        ca, cb = math.sqrt(va) / ma * 100, math.sqrt(vb) / mb * 100
        if abs(ca - cb) > 1:
            break
    more = a if ca < cb else b
    return {'stem': f'Scores of two school cricketers in five matches are:\n{a}: {", ".join(map(str, xa))}\n{b}: {", ".join(map(str, xb))}\n'
                    '(i) Find the mean score of each. (ii) Find the standard deviation of each (2 d.p.). (iii) Find the coefficient of variation of each. (iv) Who is more consistent?',
            'answer': f'(i) {a} {fs(ma)}, {b} {fs(mb)} (ii) {a} {dp(math.sqrt(va))}, {b} {dp(math.sqrt(vb))} (iii) {a} {dp(ca)}%, {b} {dp(cb)}% (iv) {more} (smaller CV)',
            'key': '(i) Σx/n (1). (ii) √(Σ(x − x̄)²/n) (1). (iii) σ/x̄ × 100 (1). (iv) smaller CV ⇒ more consistent (1).'}


c13s3_tf = tf_mcq('variance and standard deviation',
                  ['Variance is the mean of the squares of the deviations from the mean.', 'The standard deviation is the positive square root of the variance.',
                   'The variance of the first n natural numbers is (n² − 1)/12.', 'The series with the greater coefficient of variation is more variable.', 'σ² = Σx²/n − x̄².'],
                  ['The standard deviation can be negative.', 'The variance has the same unit as the data.', 'The variance of 5, 5, 5, 5 is 5.',
                   'The series with the greater mean is always more variable.', 'σ² = (Σx/n)² − Σx²/n.'])

c13s3_ar = pool_ar([
    ('The variance of 2, 4, 6, 8, 10 is 8.', 'σ² = Σ(xᵢ − x̄)²/n with x̄ = 6 gives 40/5.', 'a', 'R explains A.'),
    ('A batsman with CV 15% is more consistent than one with CV 25%.', 'A smaller coefficient of variation means less relative variability.', 'a', 'R explains A.'),
    ('The SD of 3, 3, 3, 3 is 3.', 'If all observations are equal, every deviation from the mean is zero.', 'd', 'A is false (SD 0); R is true.'),
])

c13s3_explain = pool_txt([
    ('Why is the standard deviation preferred to the mean deviation?', 'Squaring removes signs without the awkward modulus and makes further algebra (e.g. combining groups) possible.', '2 marks.'),
    ('Explain when the coefficient of variation should be used to compare two distributions.', 'When the means (or units) differ; CV = σ/x̄ × 100 compares relative spread.', '2 marks.'),
])

# st4 shortcut (step-deviation) method


def c13s4_step(r):
    cls, fq, w = _classes(r)
    N = sum(fq)
    mids = [Fr(a + b, 2) for a, b in cls]
    A = mids[len(mids) // 2]
    ys = [(x - A) / w for x in mids]
    Sy = sum(f * y for f, y in zip(fq, ys))
    Sy2 = sum(f * y * y for f, y in zip(fq, ys))
    mean = A + w * Sy / N
    var = w * w * (Sy2 / N - (Sy / N) ** 2)
    return Q(f'Using the step-deviation (shortcut) method, find the mean, variance and standard deviation of:\nClass: {", ".join(f"{a}–{b}" for a, b in cls)}\nFrequency: {", ".join(map(str, fq))}',
             f'mean {dp(mean)}; variance {dp(var)}; SD {dp(math.sqrt(var))}',
             f'Take A = {fs(A)}, h = {w}, yᵢ = (xᵢ − A)/h = {", ".join(fs(y) for y in ys)} (1); N = {N}, Σfy = {fs(Sy)}, Σfy² = {fs(Sy2)} (2); '
             f'x̄ = A + h Σfy/N = {dp(mean)} (1); σ² = h²[Σfy²/N − (Σfy/N)²] = {dp(var)}, σ = {dp(math.sqrt(var))} (1).',
             [f'mean {dp(mean)}; variance {dp(var / (w * w))}; SD {dp(math.sqrt(var) / w)}', f'mean {dp(A + Sy / N)}; variance {dp(var)}; SD {dp(math.sqrt(var))}', f'mean {dp(mean)}; variance {dp(w * Sy2 / N)}; SD {dp(math.sqrt(w * Sy2 / N))}'])


def c13s4_coding(r):
    A = r.choice([25, 30, 45, 50, 55, 60])
    h = r.choice([2, 5, 10])
    my = Fr(r.randint(-20, 20), 10)
    vy = Fr(r.randint(5, 40), 10)
    mx, vx = A + h * my, h * h * vy
    return Q(f'For a data set, yᵢ = (xᵢ − {A})/{h}. The mean of y is {dp(my, 1)} and its variance is {dp(vy, 1)}. Find the mean and variance of x.', f'mean {dp(mx, 1)}; variance {dp(vx, 1)}',
             f'xᵢ = {A} + {h}yᵢ (1); x̄ = {A} + {h} × ({dp(my, 1)}) = {dp(mx, 1)} (1); σₓ² = {h}² × {dp(vy, 1)} = {dp(vx, 1)} (1).',
             [f'mean {dp(mx, 1)}; variance {dp(h * vy, 1)}', f'mean {dp(A + my, 1)}; variance {dp(vx, 1)}', f'mean {dp(mx, 1)}; variance {dp(vx + A, 1)}'])


def c13s4_effect(r):
    v = r.randint(4, 30)
    a, b = r.randint(2, 6), r.randint(1, 20)
    kind = r.choice(['ab', 'sd'])
    if kind == 'ab':
        return mcq(f'The variance of x is {v}. The variance of {a}x + {b} is', str(a * a * v), [str(a * v), str(a * a * v + b), str(a * v + b)],
                   f'Var(ax + b) = a² Var(x) = {a}² × {v} = {a * a * v}; adding {b} has no effect.', r)
    return mcq(f'The standard deviation of x is {v}. The standard deviation of {b} − {a}x is', str(a * v), [str(-a * v).replace('-', '−'), str(a * a * v), str(a * v + b)],
               f'SD(b − ax) = |a| SD(x) = {a} × {v} = {a * v}.', r)


def c13s4_missing(r):
    known = sorted(r.sample(range(1, 15), 3))
    x, y = sorted(r.sample([v for v in range(1, 15) if v not in known], 2))
    allv = known + [x, y]
    n = 5
    m = Fr(sum(allv), n)
    var = Fr(sum(v * v for v in allv), n) - m * m
    return Q(f'The mean and variance of five observations are {dp(m, 1)} and {dp(var, 2)}. Three of the observations are {", ".join(map(str, known))}. Find the other two.', f'{x} and {y}',
             f'x + y = 5 × {dp(m, 1)} − {sum(known)} = {x + y} (1); x² + y² = 5({dp(var, 2)} + {dp(m, 1)}²) − {sum(v * v for v in known)} = {x * x + y * y} (2); solve: {x} and {y} (1).',
             [f'{x + 1} and {y - 1}', f'{x - 1} and {y + 1}' if x > 1 else f'{y} and {y + 1}', f'{Fr(x + y, 2)} and {Fr(x + y, 2)}'])


c13s4_tf = tf_mcq('the shortcut method for variance',
                  ['If yᵢ = (xᵢ − A)/h, then σₓ² = h² σᵧ².', 'The assumed mean A does not affect the variance.', 'σ² = h²[Σfy²/N − (Σfy/N)²] in the step-deviation method.',
                   'Changing the origin does not change the standard deviation.'],
                  ['If yᵢ = (xᵢ − A)/h, then σₓ² = h σᵧ².', 'The assumed mean must be the true mean.', 'Changing the scale does not change the variance.', 'σₓ = σᵧ/h.'])

c13s4_ar = pool_ar([
    ('The variance of 101, 102, 103, 104, 105 equals the variance of 1, 2, 3, 4, 5.', 'Subtracting a constant from every value does not change the variance.', 'a', 'R explains A.'),
    ('If every value is doubled, the variance is doubled.', 'Var(kx) = k² Var(x).', 'd', 'A is false: the variance becomes 4 times; R is true.'),
    ('The step-deviation method gives the same SD as the direct method.', 'Coding changes origin and scale in a known way that is undone at the end.', 'a', 'R explains A.'),
])

c13s4_explain = pool_txt([
    ('Show that if yᵢ = (xᵢ − A)/h then σₓ² = h²σᵧ².', 'xᵢ = A + hyᵢ, x̄ = A + hȳ, so xᵢ − x̄ = h(yᵢ − ȳ); square and average.', '2 marks.'),
    ('Why does the shortcut method make calculation easier?', 'The coded values yᵢ are small integers, so Σfy and Σfy² are easy to find.', '2 marks.'),
])


# ======================================================== ch14 Probability
# st1 random experiments and sample spaces

def c14s1_coins(r):
    n = r.randint(2, 4)
    if n <= 3 and r.random() < 0.6:
        import itertools
        ss = [''.join(t) for t in itertools.product('HT', repeat=n)]
        return Q(f'Write the sample space when a coin is tossed {n} times (or {n} coins are tossed together).', '{' + ', '.join(ss) + '}; ' + f'{2 ** n} outcomes',
                 f'Each toss gives H or T; list all {2 ** n} ordered results.', ['{' + ', '.join(ss[:-1]) + '}; ' + f'{2 ** n - 1} outcomes', f'{{{", ".join("H" * k + "T" * (n - k) for k in range(n, -1, -1))}}}; {n + 1} outcomes'])
    return Q(f'How many outcomes are there in the sample space when a coin is tossed {n} times?', str(2 ** n), f'2 outcomes per toss: 2{sup(n)} = {2 ** n}.', [str(2 * n), str(n + 1), str(n * n)])


def c14s1_count(r):
    kind = r.choice(['coin_die', 'two_dice', 'die_coins', 'bag', 'cards_coin'])
    if kind == 'coin_die':
        return Q('A coin is tossed and then a die is rolled. How many outcomes are in the sample space? Write two of them.', '12; e.g. H1, T6', '2 × 6 = 12 outcomes: H1, …, H6, T1, …, T6.', ['8', '6', '36'])
    if kind == 'two_dice':
        return Q('Two dice are rolled. How many outcomes are in the sample space?', '36', 'Each die has 6 faces: 6 × 6 = 36 ordered pairs.', ['12', '21', '11'])
    if kind == 'die_coins':
        k = r.randint(2, 3)
        return Q(f'A die is rolled and {k} coins are tossed. How many outcomes are in the sample space?', str(6 * 2 ** k), f'6 × 2{sup(k)} = {6 * 2 ** k}.', [str(6 + 2 * k), str(6 * 2 * k), str(6 ** k)])
    if kind == 'bag':
        R, B = r.randint(2, 5), r.randint(2, 5)
        return Q(f'A bag has {R} red and {B} blue balls (all distinguishable). Two balls are drawn one after another without replacement. How many outcomes are in the sample space?',
                 str((R + B) * (R + B - 1)), f'{R + B} × {R + B - 1} ordered draws = {(R + B) * (R + B - 1)}.', [str((R + B) ** 2), str(comb(R + B, 2)), str(R * B)])
    return Q('A card is drawn from a well-shuffled pack of 52 cards and a coin is tossed. How many outcomes are in the sample space?', '104', '52 × 2 = 104.', ['54', '52', '26'])


def c14s1_cond(r):
    return pool_txt([
        ('A coin is tossed. If it shows a head, a die is rolled; if it shows a tail, the coin is tossed again. Write the sample space.', '{H1, H2, H3, H4, H5, H6, TH, TT}', 'Branch on the first toss (1); list the 6 + 2 outcomes (2).',
         ['{H1, …, H6, T1, …, T6}', '{HH, HT, TH, TT}', '{H1, H2, H3, H4, H5, H6}']),
        ('A coin is tossed. If it shows a tail, a die is rolled; if it shows a head, the coin is tossed twice more. Write the sample space and count its outcomes.',
         '{T1, T2, T3, T4, T5, T6, HHH, HHT, HTH, HTT}; 10 outcomes', 'Tail branch: 6 outcomes (1); head branch: 4 outcomes (1); total 10 (1).', ['{T1, …, T6, HH, HT}; 8 outcomes', '12 outcomes', '16 outcomes']),
        ('A die is rolled. If the number is even, a coin is tossed; if it is odd, the experiment stops. Write the sample space.', '{1, 3, 5, 2H, 2T, 4H, 4T, 6H, 6T}',
         'Odd results stop (1); each even result is followed by H or T (2).', ['{1H, 1T, …, 6H, 6T}', '{2H, 2T, 4H, 4T, 6H, 6T}', '{1, 2, 3, 4, 5, 6, H, T}']),
        ('A box has 1 red and 3 identical white balls. Two balls are drawn one by one without replacement. Write the sample space.', '{RW, WR, WW}',
         'The white balls are identical, so only colours matter (1); RR is impossible (1); list the outcomes (1).', ['{RW, WR, WW, RR}', '{RW, WW}', '{R, W}']),
    ])(r)


c14s1_terms = term_mcq([('random experiment', 'an experiment with more than one possible outcome that cannot be predicted in advance'),
                        ('outcome', 'a possible result of a random experiment'), ('sample space', 'the set of all possible outcomes'), ('sample point', 'an element of the sample space')],
                       'Which of the following describes a {a}?', 'Which term means {b}?', '{a}: {b}.')

c14s1_tf = tf_mcq('random experiments and sample spaces',
                  ['Tossing a coin is a random experiment.', 'The sample space for tossing two coins has 4 outcomes.', 'Each element of the sample space is a sample point.',
                   'When a die is rolled, the sample space is {1, 2, 3, 4, 5, 6}.'],
                  ['The sample space for tossing two coins is {HH, HT, TT}.', 'A random experiment has exactly one outcome.', 'Rolling two dice gives 12 outcomes.',
                   'The outcome of a random experiment can always be predicted.'])

c14s1_ar = pool_ar([
    ('Tossing three coins gives 8 outcomes.', 'Each coin has 2 outcomes and 2 × 2 × 2 = 8.', 'a', 'R explains A.'),
    ('The sample space for rolling two dice has 36 elements.', 'The outcomes are ordered pairs (a, b) with a, b ∈ {1, …, 6}.', 'a', 'R explains A.'),
    ('The sample space for tossing two coins is {two heads, one head, no head}.', 'Each toss has two outcomes.', 'd', 'A is false as a sample space of equally likely outcomes ({HH, HT, TH, TT} is used); R is true.'),
])

c14s1_explain = pool_txt([
    ('What is a random experiment? Give two examples.', 'An experiment with more than one possible outcome that cannot be predicted in advance; tossing a coin, rolling a die.', '2 marks.'),
    ('Explain why HT and TH are different outcomes when two coins are tossed.', 'The coins (or tosses) are distinguishable, so the order matters.', '2 marks.'),
])

# st2 events

DIE_EVENTS = {
    'even': ('a number is even', {2, 4, 6}), 'odd': ('a number is odd', {1, 3, 5}), 'prime': ('a prime number', {2, 3, 5}),
    'gt3': ('a number greater than 3', {4, 5, 6}), 'lt4': ('a number less than 4', {1, 2, 3}), 'mul3': ('a multiple of 3', {3, 6}), 'le2': ('a number at most 2', {1, 2}),
}


def c14s2_ops(r):
    a, b = r.sample(list(DIE_EVENTS), 2)
    (da, A), (db, B) = DIE_EVENTS[a], DIE_EVENTS[b]
    U = set(range(1, 7))
    op = r.choice(['∪', '∩', 'A′', 'A − B', 'B′ ∩ A'])
    res = {'∪': A | B, '∩': A & B, 'A′': U - A, 'A − B': A - B, 'B′ ∩ A': A - B}[op]
    lab = {'∪': 'A ∪ B', '∩': 'A ∩ B', 'A′': 'A′ (not A)', 'A − B': 'A − B', 'B′ ∩ A': 'A ∩ B′'}[op]
    wr = [A | B, A & B, U - A, A - B, B - A, U - B]
    return Q(f'A die is rolled. A is the event "{da}" and B is the event "{db}". Write the event {lab}.', setstr(sorted(res)),
             f'A = {setstr(sorted(A))}, B = {setstr(sorted(B))} (1); {lab} = {setstr(sorted(res))} (1).', [setstr(sorted(w)) for w in wr if w != res][:4])


def c14s2_mutex(r):
    a, b = r.sample(list(DIE_EVENTS), 2)
    (da, A), (db, B) = DIE_EVENTS[a], DIE_EVENTS[b]
    me = not (A & B)
    ex = (A | B) == set(range(1, 7))
    ans = 'mutually exclusive and exhaustive' if me and ex else 'mutually exclusive but not exhaustive' if me else 'exhaustive but not mutually exclusive' if ex else 'neither mutually exclusive nor exhaustive'
    opts = ['mutually exclusive and exhaustive', 'mutually exclusive but not exhaustive', 'exhaustive but not mutually exclusive', 'neither mutually exclusive nor exhaustive']
    return mcq(f'A die is rolled. A: "{da}", B: "{db}". The events A and B are', ans, [o for o in opts if o != ans],
               f'A = {setstr(sorted(A))}, B = {setstr(sorted(B))}; A ∩ B = {setstr(sorted(A & B))}, A ∪ B = {setstr(sorted(A | B))}.', r)


def c14s2_dice(r):
    s = r.randint(4, 10)
    k = r.randint(1, 6)
    A = [(i, j) for i in range(1, 7) for j in range(1, 7) if i + j == s]
    B = [(i, j) for i in range(1, 7) for j in range(1, 7) if i == k]
    AB = [p for p in A if p in B]
    t = lambda ps: '{' + ', '.join(f'({i}, {j})' for i, j in ps) + '}' if ps else 'φ'
    return Q(f'Two dice are rolled. A is the event "the sum is {s}" and B is the event "the first die shows {k}". Write A, B and A ∩ B, and say whether A and B are mutually exclusive.',
             f'A = {t(A)}; B = {t(B)}; A ∩ B = {t(AB)}; ' + ('mutually exclusive' if not AB else 'not mutually exclusive'),
             f'List the pairs with sum {s} (1); list the pairs with first entry {k} (1); common pairs (1); mutually exclusive only if A ∩ B = φ (1).')


c14s2_kinds = term_mcq([('impossible event', 'the empty set φ'), ('sure event', 'the whole sample space S'), ('simple event', 'an event with exactly one sample point'),
                        ('compound event', 'an event with more than one sample point'), ('complementary event of A', 'the set S − A, written A′')],
                       'Which of the following is the {a}?', 'Which event is {b}?', '{a}: {b}.')

c14s2_tf = tf_mcq('events',
                  ['Events A and B are mutually exclusive if A ∩ B = φ.', 'Events are exhaustive if their union is the sample space.', 'A and A′ are mutually exclusive and exhaustive.',
                   'The event "A or B" is A ∪ B.', 'The event "A but not B" is A ∩ B′.'],
                  ['Mutually exclusive events always have A ∪ B = S.', 'The event "A and B" is A ∪ B.', 'An impossible event is the sample space.', 'A simple event has two sample points.',
                   'A and A′ can occur together.'])

c14s2_ar = pool_ar([
    ('When a die is rolled, "an even number" and "an odd number" are mutually exclusive and exhaustive.', 'They have no common outcome and together make up {1, …, 6}.', 'a', 'R explains A.'),
    ('"A head" and "a tail" in one toss of a coin are mutually exclusive.', 'Both cannot happen at the same time.', 'a', 'R explains A.'),
    ('When a die is rolled, "a prime" and "an even number" are mutually exclusive.', '2 is both prime and even.', 'd', 'A is false; R is true and shows why.'),
])

c14s2_explain = pool_txt([
    ('Distinguish between mutually exclusive and exhaustive events with an example from rolling a die.', 'Mutually exclusive: no common outcome (even/odd, or {1, 2} and {5}); exhaustive: union is S ({1, 2, 3} and {3, 4, 5, 6}).', '2 marks.'),
    ('What is meant by the complement of an event? Write the complement of "a number greater than 4" for a die.', 'A′ = S − A, the outcomes not in A; here {1, 2, 3, 4}.', '2 marks.'),
])

# st3 axiomatic probability


def c14s3_die(r):
    k, (d, A) = r.choice(list(DIE_EVENTS.items()))
    p = Fr(len(A), 6)
    return Q(f'A fair die is rolled. Find the probability of getting {d}.', fs(p), f'Favourable outcomes {setstr(sorted(A))}: {len(A)} of 6, so P = {fs(p)}.',
             [fs(1 - p) if 1 - p != p else fs(Fr(1, 6)), fs(Fr(len(A), 5)) if len(A) < 5 else '1', fs(Fr(1, len(A)))])


CARD_EV = [('a king', 4), ('a heart', 13), ('a red card', 26), ('a face card', 12), ('a black king', 2), ('the ace of spades', 1), ('a red face card', 6), ('a number card (2 to 10)', 36),
           ('a spade or a club', 26), ('not a diamond', 39)]


def c14s3_cards(r):
    d, n = r.choice(CARD_EV)
    p = Fr(n, 52)
    return Q(f'A card is drawn at random from a well-shuffled pack of 52 cards. Find the probability that it is {d}.', fs(p), f'{n} favourable cards out of 52: {n}/52 = {fs(p)}.',
             [fs(1 - p), fs(Fr(n, 13)) if Fr(n, 13) <= 1 and Fr(n, 13) != p else fs(Fr(n + 1, 52)), fs(Fr(1, n)) if n > 1 else fs(Fr(1, 13))])


def c14s3_sum(r):
    s = r.randint(2, 12)
    kind = r.choice(['eq', 'lt', 'gt', 'mul'])
    pairs = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    if kind == 'eq':
        fav, d = [p for p in pairs if sum(p) == s], f'the sum is {s}'
    elif kind == 'lt':
        s = max(s, 4)
        fav, d = [p for p in pairs if sum(p) < s], f'the sum is less than {s}'
    elif kind == 'gt':
        s = min(s, 10)
        fav, d = [p for p in pairs if sum(p) > s], f'the sum is greater than {s}'
    else:
        s = r.choice([3, 4, 5])
        fav, d = [p for p in pairs if sum(p) % s == 0], f'the sum is a multiple of {s}'
    p = Fr(len(fav), 36)
    return Q(f'Two fair dice are rolled. Find the probability that {d}.', fs(p), f'{len(fav)} favourable pairs out of 36: P = {fs(p)}.',
             [fs(Fr(len(fav), 11)) if len(fav) <= 11 else fs(Fr(len(fav), 21)), fs(1 - p), fs(Fr(len(fav) + 1, 36))])


def c14s3_valid(r):
    def mk(valid):
        while True:
            if valid:
                cuts = sorted(r.sample(range(1, 20), 3))
                ps = [Fr(b - a, 20) for a, b in zip([0] + cuts, cuts + [20])]
            else:
                ps = [Fr(r.randint(1, 9), 20) for _ in range(4)]
                if r.random() < 0.3:
                    ps[0] = -ps[0]
            if all(x > 0 for x in ps) == valid and (sum(ps) == 1) == valid or (not valid and (sum(ps) != 1 or any(x < 0 for x in ps))):
                if valid and sum(ps) == 1 and all(x > 0 for x in ps):
                    return ps
                if not valid:
                    return ps
    good = mk(True)
    bads = [mk(False) for _ in range(3)]
    t = lambda ps: ', '.join(dp(x) for x in ps)
    if len({t(good)} | {t(b) for b in bads}) < 4:
        raise ValueError
    return mcq('A sample space is S = {ω₁, ω₂, ω₃, ω₄}. Which of the following is a valid assignment of probabilities P(ω₁), P(ω₂), P(ω₃), P(ω₄)?', t(good), [t(b) for b in bads],
               'Each probability must lie in [0, 1] and the four must add up to 1.', r)


def c14s3_comm(r):
    m, w = r.randint(4, 8), r.randint(3, 6)
    k = r.randint(3, 4)
    j = r.randint(1, min(k, w))
    fav = comb(w, j) * comb(m, k - j)
    tot = comb(m + w, k)
    p = Fr(fav, tot)
    return Q(f'A committee of {k} is to be chosen at random from {m} men and {w} women. Find the probability that it has exactly {j} wom{"an" if j == 1 else "en"}.', fs(p),
             f'Total selections {m + w}C{k} = {tot} (1); favourable {w}C{j} × {m}C{k - j} = {fav} (2); P = {fs(p)} (1).',
             [fs(Fr(comb(w, j), tot)), fs(Fr(j, k)), fs(1 - p)])


def c14s3_case(r):
    n = r.choice([20, 25, 30, 40, 50])
    city = r.choice(CITIES)
    g = r.randint(5, n - 5)
    b = n - g
    p = Fr(g, n)
    return {'stem': f'In a lucky draw at a school fair in {city}, tickets numbered 1 to {n} are put in a box and one is drawn at random. Tickets 1 to {g} were bought by girls and the rest by boys.\n'
                    f'(i) Write the sample space and its number of outcomes. (ii) Find the probability that the ticket was bought by a girl. (iii) Find the probability that the number is a multiple of 5. '
                    f'(iv) Find the probability that it was bought by a boy and is a multiple of 5.',
            'answer': f'(i) {{1, 2, …, {n}}}, {n} outcomes (ii) {fs(p)} (iii) {fs(Fr(n // 5, n))} (iv) {fs(Fr(len([x for x in range(g + 1, n + 1) if x % 5 == 0]), n))}',
            'key': '(i) (1). (ii) favourable/total (1). (iii) count multiples of 5 (1). (iv) multiples of 5 above ' + str(g) + ' (1).'}


c14s3_tf = tf_mcq('the axiomatic approach to probability',
                  ['For any event E, 0 ≤ P(E) ≤ 1.', 'P(S) = 1 for the sample space S.', 'P(φ) = 0.', 'For mutually exclusive E and F, P(E ∪ F) = P(E) + P(F).',
                   'For equally likely outcomes, P(E) = n(E)/n(S).'],
                  ['A probability can be greater than 1.', 'P(S) = 0.', 'P(E) can be negative for an unlikely event.', 'For any events, P(E ∪ F) = P(E) + P(F).',
                   'The probabilities of the sample points may add up to more than 1.'])

c14s3_ar = pool_ar([
    ('The probability of getting a sum of 7 with two dice is 1/6.', 'Six of the 36 equally likely pairs give a sum of 7.', 'a', 'R explains A.'),
    ('P(ω₁) = 0.5, P(ω₂) = 0.3, P(ω₃) = 0.3 is a valid assignment on S = {ω₁, ω₂, ω₃}.', 'Each value lies between 0 and 1.', 'd', 'A is false (sum 1.1); R is true.'),
    ('The probability of drawing a king or a queen from a pack is 2/13.', 'The events are mutually exclusive, so P = 4/52 + 4/52.', 'a', 'R explains A.'),
])

c14s3_explain = pool_txt([
    ('State the three axioms of probability.', 'P(E) ≥ 0; P(S) = 1; for mutually exclusive events P(E ∪ F) = P(E) + P(F).', '2 marks.'),
    ('Show that for equally likely outcomes P(E) = n(E)/n(S) follows from the axioms.', 'Each of the n outcomes has probability 1/n (they add to 1); E has n(E) of them.', '2 marks.'),
])

# st4 addition rule and complement


def c14s4_not(r):
    p = Fr(r.randint(1, 19), 20) if r.random() < 0.5 else Fr(r.randint(1, 9), 10)
    return Q(f'If P(A) = {dp(p)}, find P(not A).', dp(1 - p), f'P(A′) = 1 − P(A) = 1 − {dp(p)} = {dp(1 - p)}.', [dp(p), dp(1 / (1 + p)), '1'])


def c14s4_add(r):
    a, b = Fr(r.randint(2, 7), 10), Fr(r.randint(2, 7), 10)
    lo = max(Fr(0), a + b - 1)
    hi = min(a, b)
    c = Fr(r.randint(int(lo * 10) + 1, int(hi * 10)), 10) if hi * 10 > lo * 10 + 1 else lo
    u = a + b - c
    kind = r.choice(['u', 'c', 'b'])
    if kind == 'u':
        return Q(f'P(A) = {dp(a, 1)}, P(B) = {dp(b, 1)} and P(A ∩ B) = {dp(c, 1)}. Find P(A ∪ B).', dp(u, 1), f'P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = {dp(u, 1)}.', [dp(a + b, 1) if a + b <= 1 else dp(a * b, 2), dp(u - c, 1), dp(1 - u, 1)])
    if kind == 'c':
        return Q(f'P(A) = {dp(a, 1)}, P(B) = {dp(b, 1)} and P(A ∪ B) = {dp(u, 1)}. Find P(A ∩ B).', dp(c, 1), f'P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = {dp(c, 1)}.', [dp(a * b, 2), dp(1 - u, 1), dp(a + b - c + Fr(1, 10), 1)])
    return Q(f'P(A) = {dp(a, 1)}, P(A ∪ B) = {dp(u, 1)} and P(A ∩ B) = {dp(c, 1)}. Find P(B).', dp(b, 1), f'P(B) = P(A ∪ B) − P(A) + P(A ∩ B) = {dp(b, 1)}.', [dp(u - a, 1), dp(1 - b, 1), dp(b + Fr(1, 10), 1)])


def c14s4_cards(r):
    a, na, b, nb, nab = r.choice([('a king', 4, 'a heart', 13, 1), ('a red card', 26, 'a king', 4, 2), ('a face card', 12, 'a spade', 13, 3), ('an ace', 4, 'a black card', 26, 2),
                                  ('a diamond', 13, 'a face card', 12, 3), ('a queen', 4, 'a red card', 26, 2)])
    p = Fr(na + nb - nab, 52)
    return Q(f'A card is drawn from a well-shuffled pack of 52 cards. Find the probability that it is {a} or {b}.', fs(p),
             f'P = P(first) + P(second) − P(both) = {na}/52 + {nb}/52 − {nab}/52 (2) = {fs(p)} (1).', [fs(Fr(na + nb, 52)), fs(Fr(nab, 52)), fs(1 - p)])


def c14s4_survey(r):
    n = r.choice([40, 50, 60, 80, 100])
    e = r.randint(n // 4, n // 2)
    h = r.randint(n // 4, n // 2)
    both = r.randint(3, min(e, h) // 2)
    either = e + h - both
    if either > n:
        raise ValueError
    city = r.choice(CITIES)
    pn = Fr(n - either, n)
    return Q(f'In a class of {n} students in {city}, {e} opted for English elocution, {h} for Hindi debate and {both} for both. A student is chosen at random. Find the probability that the student opted for (a) English or Hindi, (b) neither, (c) Hindi but not English.',
             f'(a) {fs(Fr(either, n))} (b) {fs(pn)} (c) {fs(Fr(h - both, n))}',
             f'n(E ∪ H) = {e} + {h} − {both} = {either} (2); (a) {either}/{n} (1); (b) 1 − {fs(Fr(either, n))} (1); (c) ({h} − {both})/{n} (1).',
             [f'(a) {fs(Fr(e + h, n))} (b) {fs(Fr(n - e - h, n)) if n > e + h else "0"} (c) {fs(Fr(h, n))}', f'(a) {fs(Fr(either, n))} (b) {fs(pn)} (c) {fs(Fr(h, n))}', f'(a) {fs(Fr(both, n))} (b) {fs(1 - Fr(both, n))} (c) {fs(Fr(h - both, n))}'])


def c14s4_long(r):
    a, b = Fr(r.randint(30, 60), 100), Fr(r.randint(30, 60), 100)
    c = Fr(r.randint(max(5, int((a + b - 1) * 100) + 1), int(min(a, b) * 100) - 5), 100)
    u = a + b - c
    return Q(f'For events A and B, P(A) = {dp(a)}, P(B) = {dp(b)} and P(A and B) = {dp(c)}. Find (i) P(not A), (ii) P(not B), (iii) P(A or B), (iv) P(neither A nor B), (v) P(A but not B).',
             f'(i) {dp(1 - a)} (ii) {dp(1 - b)} (iii) {dp(u)} (iv) {dp(1 - u)} (v) {dp(a - c)}',
             f'(i), (ii) complements (1 + 1); (iii) P(A) + P(B) − P(A ∩ B) (1); (iv) 1 − P(A ∪ B) (1); (v) P(A) − P(A ∩ B) (1).',
             [f'(i) {dp(1 - a)} (ii) {dp(1 - b)} (iii) {dp(a + b)} (iv) {dp(1 - a - b)} (v) {dp(a)}', f'(i) {dp(a)} (ii) {dp(b)} (iii) {dp(u)} (iv) {dp(u)} (v) {dp(c)}'])


def c14s4_case(r):
    n = r.choice([50, 60, 80, 100, 120])
    city = r.choice(CITIES)
    t = r.randint(n // 3, n // 2)
    c = r.randint(n // 4, n // 3)
    both = r.randint(4, min(t, c) // 2)
    nei = n - (t + c - both)
    if nei < 0:
        raise ValueError
    return {'stem': f'A survey of {n} families in a housing society in {city} found that {t} read a Hindi newspaper, {c} read an English newspaper and {both} read both. A family is chosen at random.\n'
                    '(i) Find P(reads Hindi). (ii) Find P(reads Hindi or English). (iii) Find P(reads neither). (iv) Find P(reads exactly one of the two).',
            'answer': f'(i) {fs(Fr(t, n))} (ii) {fs(Fr(t + c - both, n))} (iii) {fs(Fr(nei, n))} (iv) {fs(Fr(t + c - 2 * both, n))}',
            'key': '(i) n(H)/n (1). (ii) addition rule (1). (iii) complement of (ii) (1). (iv) P(H ∪ E) − P(H ∩ E) (1).'}


c14s4_tf = tf_mcq("the addition rule and 'not' events",
                  ['P(A ∪ B) = P(A) + P(B) − P(A ∩ B).', 'P(A′) = 1 − P(A).', 'If A and B are mutually exclusive, P(A ∩ B) = 0.', 'P(A − B) = P(A) − P(A ∩ B).', 'P(A ∪ B) ≤ P(A) + P(B).'],
                  ['P(A ∪ B) = P(A) + P(B) for all events.', 'P(A′) = P(A) − 1.', 'P(A ∩ B) can exceed P(A).', 'P(neither A nor B) = 1 − P(A ∩ B).', 'P(A ∪ B) can be greater than 1.'])

c14s4_ar = pool_ar([
    ('If P(A) = 0.35, then P(not A) = 0.65.', 'A and A′ are mutually exclusive and exhaustive.', 'a', 'R explains A: P(A) + P(A′) = 1.'),
    ('P(A) = 0.5, P(B) = 0.6 and P(A ∩ B) = 0.3 give P(A ∪ B) = 0.8.', 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B).', 'a', 'R explains A.'),
    ('P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.6 is possible.', 'P(A ∩ B) ≤ min(P(A), P(B)).', 'd', 'A is false; R is true.'),
])

c14s4_explain = pool_txt([
    ('Explain why P(A ∩ B) is subtracted in the addition rule P(A ∪ B) = P(A) + P(B) − P(A ∩ B).', 'Outcomes in A ∩ B are counted in both P(A) and P(B), so they are counted twice.', '2 marks.'),
    ('Show that P(A′) = 1 − P(A).', 'A and A′ are mutually exclusive with A ∪ A′ = S, so P(A) + P(A′) = P(S) = 1.', '2 marks.'),
])


# ======================================================== extra families (D1 / D4 coverage)

def c11s1_many(r):
    pts_ = []
    while len(pts_) < 4:
        p = tuple(r.choice([x for x in range(-7, 8) if x]) for _ in range(3))
        if p not in pts_:
            pts_.append(p)
    j = r.randrange(3)
    pts_[r.randrange(4)] = tuple(0 if i == j else v for i, v in enumerate(pts_[0]))
    lab = []
    for p in pts_:
        if 0 in p:
            zs = [c for c, v in zip('xyz', p) if v == 0]
            planes = {'x': 'YZ', 'y': 'ZX', 'z': 'XY'}
            lab.append(f'{p3(*p)}: on the {planes[zs[0]]}-plane' if len(zs) == 1 else f'{p3(*p)}: on the {[c for c, v in zip("xyz", p) if v][0]}-axis')
        else:
            lab.append(f'{p3(*p)}: octant {OCT[tuple(1 if v > 0 else -1 for v in p)]}')
    return Q('For each of the points ' + ', '.join(p3(*p) for p in pts_) + ', name the octant in which it lies, or the coordinate plane on which it lies.', '; '.join(lab),
             'Read the signs of (x, y, z) and match them with the octant table (3); a zero coordinate puts the point on a coordinate plane (1).')


def c12s1_three(r):
    c1 = r.randint(-2, 1)
    c2 = c1 + r.randint(2, 4)
    a, b = r.choice([1, 2, -1]), r.randint(-4, 4)
    p, q = r.choice([1, 2, 3, -2]), r.randint(-4, 6)
    s_, t = r.choice([1, -1, 2]), r.randint(-4, 6)
    if r.random() < 0.5:
        q = a * c1 + b - p * c1
    if r.random() < 0.5:
        t = p * c2 + q - s_ * c2
    L1, R1 = a * c1 + b, p * c1 + q
    L2, R2 = p * c2 + q, s_ * c2 + t
    e = lambda L, R: f'limit exists and equals {fs(L)}' if L == R else f'limit does not exist (LHL {fs(L)}, RHL {fs(R)})'
    return Q(M(f'f(x) = {lin(a, b)} for x < {c1}; f(x) = {lin(p, q)} for {c1} ≤ x < {c2}; f(x) = {lin(s_, t)} for x ≥ {c2}. Examine lim f(x) at x = {c1} and at x = {c2}.'),
             M(f'At x = {c1}: {e(L1, R1)}; at x = {c2}: {e(L2, R2)}'),
             M(f'At x = {c1}: LHL from {lin(a, b)} = {fs(L1)}, RHL from {lin(p, q)} = {fs(R1)} (2); at x = {c2}: LHL = {fs(L2)}, RHL = {fs(R2)} (2); compare (1).'))


c13s3_terms = term_mcq([('variance', 'the mean of the squared deviations from the mean'), ('standard deviation', 'the positive square root of the variance'),
                        ('coefficient of variation', '(σ/x̄) × 100, used to compare variability'), ('mean deviation', 'the mean of the absolute deviations from a central value')],
                       'Which of the following describes the {a}?', 'Which measure is {b}?', '{a}: {b}.')

c13s4_formula = pool_mcq([
    ('In the step-deviation method with yᵢ = (xᵢ − A)/h, the variance of x is', 'h²[Σfᵢyᵢ²/N − (Σfᵢyᵢ/N)²]', ['h[Σfᵢyᵢ²/N − (Σfᵢyᵢ/N)²]', 'Σfᵢyᵢ²/N', 'A + h Σfᵢyᵢ/N'], 'σₓ² = h²σᵧ².'),
    ('In the step-deviation method, the mean is', 'x̄ = A + h × Σfᵢyᵢ/N', ['x̄ = A − h × Σfᵢyᵢ/N', 'x̄ = Σfᵢyᵢ/N', 'x̄ = h × Σfᵢyᵢ'], 'xᵢ = A + hyᵢ.'),
    ('The shortcut formula for the variance of raw data is', 'σ² = Σxᵢ²/n − (Σxᵢ/n)²', ['σ² = (Σxᵢ)²/n', 'σ² = Σxᵢ²/n', 'σ² = Σxᵢ/n − (Σxᵢ²/n)'], 'Expand Σ(xᵢ − x̄)².'),
    ('If yᵢ = (xᵢ − A)/h, then σₓ equals', 'hσᵧ (h > 0)', ['σᵧ/h', 'h²σᵧ', 'σᵧ + A'], 'Taking the square root of h²σᵧ².'),
])


def c14s1_family(r):
    import itertools
    n = r.choice([2, 3])
    k = r.randint(1, n)
    ss = [''.join(t) for t in itertools.product('BG', repeat=n)]
    ev = [x for x in ss if x.count('G') >= k]
    return Q(f'A family has {n} children. Writing B for a boy and G for a girl in order of birth, write the sample space. Also write the event "at least {k} girl{"s" if k > 1 else ""}" and count its outcomes.',
             '{' + ', '.join(ss) + '}; event {' + ', '.join(ev) + f'}}, {len(ev)} outcome{"s" if len(ev) > 1 else ""}',
             f'Each child is B or G, in order of birth: 2{sup(n)} = {2 ** n} outcomes (2); keep those with {k} or more G (1); count (1).')


# ======================================================== families

FAMILIES = {
    S + '11-st1': [F('C1', 'D1', 'mcq', c11s1_terms), F('C1', 'D2', 'mcq', c11s1_tf), F('C2', 'D2', 'explain', c11s1_explain), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'mcq', c11s1_octant), F('C3', 'D2', 'mcq', c11s1_plane), F('C3', 'D3', 'mcq', c11s1_signs), F('C4', 'D3', 'multi_step', c11s1_box)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_tf), F('C2', 'D2', 'explain', c11s2_explain), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c11s2_dplane),
                   F('C3', 'D2', 'short', c11s2_foot), F('C3', 'D3', 'numerical', c11s2_image), F('C4', 'D4', 'multi_step', c11s2_cuboid), F('C3', 'D3', 'case', c11s2_case)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_tf), F('C2', 'D1', 'mcq', c11s3_origin), F('C2', 'D2', 'explain', c11s3_explain), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c11s3_dist), F('C3', 'D3', 'numerical', c11s3_k), F('C4', 'D3', 'multi_step', c11s3_collinear), F('C4', 'D4', 'long', c11s3_tri),
                   F('C4', 'D5', 'long', c11s3_locus), F('C3', 'D3', 'case', c11s3_case)],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_tf), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s1_ar, kinds=('ar',)), F('C3', 'D1', 'short', c12s1_direct),
                   F('C3', 'D2', 'mcq', c12s1_special), F('C3', 'D2', 'numerical', c12s1_piece), F('C4', 'D3', 'numerical', c12s1_k)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_tf), F('C2', 'D2', 'explain', c12s2_explain), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)), F('C3', 'D1', 'mcq', c12s2_algebra),
                   F('C3', 'D2', 'numerical', c12s2_factor), F('C3', 'D3', 'numerical', c12s2_xn), F('C4', 'D3', 'numerical', c12s2_rational), F('C4', 'D4', 'multi_step', c12s2_sqrt)],
    S + '12-st3': [F('C1', 'D2', 'mcq', c12s3_tf), F('C2', 'D2', 'explain', c12s3_explain), F('C2', 'D3', 'mcq', c12s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c12s3_sin),
                   F('C3', 'D3', 'numerical', c12s3_cos), F('C4', 'D3', 'mcq', c12s3_mcq), F('C4', 'D4', 'multi_step', c12s3_combo)],
    S + '12-st4': [F('C1', 'D1', 'mcq', c12s4_def), F('C1', 'D2', 'mcq', c12s4_tf), F('C2', 'D2', 'explain', c12s4_explain), F('C2', 'D3', 'mcq', c12s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s4_point), F('C3', 'D3', 'multi_step', c12s4_fp), F('C4', 'D4', 'long', c12s4_recip), F('C4', 'D5', 'long', c12s4_trig),
                   F('C3', 'D3', 'case', c12s4_case)],
    S + '12-st5': [F('C1', 'D2', 'mcq', c12s5_tf), F('C2', 'D2', 'explain', c12s5_explain), F('C2', 'D3', 'mcq', c12s5_ar, kinds=('ar',)), F('C3', 'D1', 'short', c12s5_poly),
                   F('C3', 'D2', 'numerical', c12s5_prod), F('C3', 'D3', 'numerical', c12s5_quot), F('C4', 'D3', 'mcq', c12s5_trig), F('C4', 'D4', 'long', c12s5_value),
                   F('C3', 'D3', 'case', c12s5_case)],
    S + '13-st1': [F('C1', 'D1', 'mcq', c13s1_terms), F('C1', 'D2', 'mcq', c13s1_tf), F('C2', 'D2', 'explain', c13s1_explain), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c13s1_range), F('C3', 'D2', 'numerical', c13s1_mdmean), F('C3', 'D3', 'numerical', c13s1_mdmed), F('C4', 'D3', 'mcq', c13s1_change),
                   F('C4', 'D4', 'multi_step', c13s1_compare)],
    S + '13-st2': [F('C1', 'D1', 'mcq', c13s2_formula), F('C1', 'D2', 'mcq', c13s2_tf), F('C2', 'D2', 'explain', c13s2_explain), F('C2', 'D3', 'mcq', c13s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s2_discrete), F('C4', 'D4', 'long', c13s2_cont), F('C4', 'D5', 'long', c13s2_median), F('C3', 'D3', 'case', c13s2_case)],
    S + '13-st3': [F('C1', 'D2', 'mcq', c13s3_tf), F('C2', 'D2', 'explain', c13s3_explain), F('C2', 'D3', 'mcq', c13s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c13s3_natural),
                   F('C3', 'D3', 'multi_step', c13s3_raw), F('C4', 'D4', 'long', c13s3_freq), F('C4', 'D3', 'multi_step', c13s3_cv), F('C4', 'D5', 'long', c13s3_correct),
                   F('C3', 'D3', 'case', c13s3_case)],
    S + '13-st4': [F('C1', 'D2', 'mcq', c13s4_tf), F('C2', 'D2', 'explain', c13s4_explain), F('C2', 'D3', 'mcq', c13s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c13s4_coding),
                   F('C3', 'D3', 'mcq', c13s4_effect), F('C4', 'D4', 'long', c13s4_step), F('C4', 'D4', 'multi_step', c13s4_missing)],
    S + '14-st1': [F('C1', 'D1', 'mcq', c14s1_terms), F('C1', 'D2', 'mcq', c14s1_tf), F('C2', 'D2', 'explain', c14s1_explain), F('C2', 'D3', 'mcq', c14s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c14s1_coins), F('C3', 'D2', 'short', c14s1_count), F('C4', 'D3', 'multi_step', c14s1_cond)],
    S + '14-st2': [F('C1', 'D1', 'mcq', c14s2_kinds), F('C1', 'D2', 'mcq', c14s2_tf), F('C2', 'D2', 'explain', c14s2_explain), F('C2', 'D3', 'mcq', c14s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c14s2_ops), F('C3', 'D3', 'mcq', c14s2_mutex), F('C4', 'D4', 'multi_step', c14s2_dice)],
    S + '14-st3': [F('C1', 'D2', 'mcq', c14s3_tf), F('C2', 'D2', 'explain', c14s3_explain), F('C2', 'D3', 'mcq', c14s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c14s3_die),
                   F('C3', 'D2', 'numerical', c14s3_cards), F('C3', 'D3', 'numerical', c14s3_sum), F('C4', 'D3', 'mcq', c14s3_valid), F('C4', 'D4', 'multi_step', c14s3_comm),
                   F('C3', 'D3', 'case', c14s3_case)],
    S + '14-st4': [F('C1', 'D2', 'mcq', c14s4_tf), F('C2', 'D2', 'explain', c14s4_explain), F('C2', 'D3', 'mcq', c14s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c14s4_not),
                   F('C3', 'D2', 'numerical', c14s4_add), F('C3', 'D3', 'numerical', c14s4_cards), F('C4', 'D4', 'multi_step', c14s4_survey), F('C4', 'D5', 'long', c14s4_long),
                   F('C3', 'D3', 'case', c14s4_case)],
}

FAMILIES[S + '11-st1'].append(F('C4', 'D4', 'multi_step', c11s1_many))
FAMILIES[S + '12-st1'].append(F('C4', 'D4', 'long', c12s1_three))
FAMILIES[S + '13-st3'].append(F('C1', 'D1', 'mcq', c13s3_terms))
FAMILIES[S + '13-st4'].append(F('C1', 'D1', 'mcq', c13s4_formula))
FAMILIES[S + '14-st1'].append(F('C4', 'D4', 'multi_step', c14s1_family))

FAMILIES = polish(mpolish(FAMILIES))
