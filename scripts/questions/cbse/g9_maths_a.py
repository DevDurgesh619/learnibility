"""CBSE class 9 maths (Ganita Manjari) families, chapters 1-5."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, frac, name, two_names, inr, num_distractors
from g9_maths_h import Q, mcqbank, arbank, xbank, P, fn, rad, is_sq, poly, lin, term, triple, signed, bracket, sub

S = 'cbse-g9-maths-ch'
QUAD = ['Quadrant I', 'Quadrant II', 'Quadrant III', 'Quadrant IV']


def nz(r, lo=1, hi=9):
    return r.choice([-1, 1]) * r.randint(lo, hi)


def quad_of(x, y):
    if x > 0 and y > 0:
        return 0
    if x < 0 and y > 0:
        return 1
    if x < 0:
        return 2
    return 3


# ---------------- ch01 Coordinates ----------------

def c1s1_quadrant(r):
    x, y = nz(r, 1, 15), nz(r, 1, 15)
    q = quad_of(x, y)
    return mcq(f'In which quadrant does the point {P(x, y)} lie?', QUAD[q], [s for i, s in enumerate(QUAD) if i != q],
               f'x is {"positive" if x > 0 else "negative"} and y is {"positive" if y > 0 else "negative"}, so the point is in {QUAD[q]}.', r)


def c1s1_axis(r):
    k = nz(r, 1, 12)
    if r.random() < 0.5:
        pt, ans = P(k, 0), 'On the x-axis'
    else:
        pt, ans = P(0, k), 'On the y-axis'
    return Q(f'Where does the point {pt} lie on the Cartesian plane?', ans,
             'A point with ordinate 0 lies on the x-axis; a point with abscissa 0 lies on the y-axis.',
             [d for d in ['On the x-axis', 'On the y-axis', 'At the origin', f'In {QUAD[r.randint(0, 3)]}'] if d != ans])


def c1s1_abscissa(r):
    x, y = nz(r, 1, 20), nz(r, 1, 20)
    which = r.choice(['abscissa', 'ordinate'])
    ans = x if which == 'abscissa' else y
    return Q(f'Write the {which} of the point {P(x, y)}.', fn(ans),
             f'The abscissa is the x-coordinate ({fn(x)}) and the ordinate is the y-coordinate ({fn(y)}).',
             num_distractors(ans, y if which == 'abscissa' else x, -ans, abs(ans) + 1))


def c1s1_sign_explain(r):
    q = r.randint(0, 3)
    sx, sy = [('positive', 'positive'), ('negative', 'positive'), ('negative', 'negative'), ('positive', 'negative')][q]
    who = name(r)
    return Q(f'{who} says that a point whose abscissa is {sx} and whose ordinate is {sy} must lie in {QUAD[q]}. Is {who} right? Explain using the signs of the coordinates in each quadrant.',
             f'Yes, it lies in {QUAD[q]}.',
             f'Signs: I (+, +), II (−, +), III (−, −), IV (+, −). ({"+" if sx == "positive" else "−"}, {"+" if sy == "positive" else "−"}) is {QUAD[q]} (2 marks: sign table 1, conclusion 1).')


def c1s1_ar(r):
    k = r.randint(2, 12)
    c = r.random()
    if c < 0.35:
        return ar(f'The point ({-k}, 0) lies on the x-axis.', 'Every point on the x-axis has its ordinate equal to 0.', 'a',
                  'Both true; R explains A.')
    if c < 0.7:
        return ar(f'The point (0, {k}) lies on the x-axis.', 'Every point on the y-axis has its abscissa equal to 0.', 'd',
                  f'(0, {k}) has abscissa 0, so it lies on the y-axis: A is false, R is true.')
    return ar(f'The points ({k}, {-k}) and ({-k}, {k}) lie in different quadrants.', 'The points (a, b) and (b, a) always lie in the same quadrant.', 'c',
              f'({k}, −{k}) is in IV and (−{k}, {k}) is in II, so A is true; R is false.')


def c1s1_reflect(r):
    x, y = nz(r, 1, 12), nz(r, 1, 12)
    axis = r.choice(['x-axis', 'y-axis', 'origin'])
    img = {'x-axis': (x, -y), 'y-axis': (-x, y), 'origin': (-x, -y)}[axis]
    wrong = [P(*w) for w in [(x, -y), (-x, y), (-x, -y), (y, x)] if w != img][:3]
    return Q(f'The point A{P(x, y)} is reflected in the {axis}. Write the coordinates of its image.', P(*img),
             f'Reflection in the {axis} changes the sign of {"y" if axis == "x-axis" else "x" if axis == "y-axis" else "both coordinates"}: image {P(*img)}.', wrong)


def c1s1_dist_axes(r):
    x, y = nz(r, 1, 15), nz(r, 1, 15)
    ax = r.choice(['x-axis', 'y-axis'])
    ans = abs(y) if ax == 'x-axis' else abs(x)
    u = lambda n: f'{n} unit' + ('' if n == 1 else 's')
    other = abs(x) if ax == 'x-axis' else abs(y)
    ds = [u(d) for d in dict.fromkeys([other, ans + 1, abs(x) + abs(y), ans + 2]) if d != ans][:3]
    return Q(f'How far is the point {P(x, y)} from the {ax}?', u(ans),
             f'Distance from the x-axis = |y| = {abs(y)}; distance from the y-axis = |x| = {abs(x)}.', ds)


def c1s1_on_axis_k(r):
    a, b = r.randint(2, 5), r.randint(1, 12)
    c, d = r.randint(1, 4), nz(r, 1, 9)
    ax = r.choice(['x-axis', 'y-axis'])
    # point (a k - a*b, c k + d) ; on y-axis => a k - a b = 0 => k = b
    if ax == 'y-axis':
        k = b
        pt = f'({a}k − {a * b}, {c}k {signed(d)})'
        res = (0, c * k + d)
    else:
        # ordinate c k + d*c ... make y = c k - c*b
        k = b
        pt = f'({c}k {signed(d)}, {a}k − {a * b})'
        res = (c * k + d, 0)
    return Q(f'The point P{pt} lies on the {ax}. Find k and the coordinates of P.', f'k = {k}, P = {P(*res)}',
             f'On the {ax} the {"abscissa" if ax == "y-axis" else "ordinate"} is 0: solve to get k = {k}; substitute to get P{P(*res)} (3 marks).')


def c1s1_case(r):
    who = name(r)
    rows = r.randint(5, 8)
    a, b = r.randint(1, 6), r.randint(1, rows)
    da, db = r.randint(1, 3), r.randint(1, 3)
    return Q((f'In a school assembly ground, students stand on a grid. The flag post is taken as the origin O, the line to the east as the positive x-axis and the line to the north as the positive y-axis (1 unit = 1 m). '
              f'{who} stands at ({a}, {b}). (i) In which quadrant is {who}? (ii) {who} walks {da} m west and {db} m south. Write the new position. '
              f'(iii) How far is the new position from the x-axis? (iv) Write the point that is the mirror image of {who}\'s first position in the y-axis.'),
             f'(i) Quadrant I (ii) {P(a - da, b - db)} (iii) {abs(b - db)} m (iv) {P(-a, b)}',
             '1 mark each part: west decreases x, south decreases y; distance from x-axis = |y|; reflection in y-axis changes the sign of x.')


# st2 distance

def c1s2_formula(r):
    return mcqbank([
        ('The distance between the points (x₁, y₁) and (x₂, y₂) is …', '√[(x₂ − x₁)² + (y₂ − y₁)²]',
         ['(x₂ − x₁)² + (y₂ − y₁)²', '√[(x₂ + x₁)² + (y₂ + y₁)²]', '|x₂ − x₁| + |y₂ − y₁|'], 'From the Baudhayana-Pythagoras theorem on the right triangle with legs |x₂ − x₁| and |y₂ − y₁|.'),
        ('The distance of the point (x, y) from the origin is …', '√(x² + y²)', ['x² + y²', 'x + y', '√(x + y)'], 'Put (x₁, y₁) = (0, 0) in the distance formula.'),
        ('The distance between (a, 0) and (0, b) is …', '√(a² + b²)', ['a + b', 'a² + b²', '√(a − b)'], 'The two legs are a and b.'),
    ])(r)


def c1s2_origin(r):
    a, b, c = triple(r)
    k = r.choice([1, 1, 2])
    x, y = r.choice([-1, 1]) * a * k, r.choice([-1, 1]) * b * k
    return Q(f'Find the distance of the point {P(x, y)} from the origin.', f'{c * k} units',
             f'√({bracket(x)}² + {bracket(y)}²) = √{x * x + y * y} = {c * k}.',
             [f'{abs(x) + abs(y)} units', f'{x * x + y * y} units', f'{c * k + 1} units'])


def c1s2_same_line(r):
    y = nz(r, 1, 9)
    x1, x2 = r.sample(range(-12, 13), 2)
    if r.random() < 0.5:
        return Q(f'Find the distance between the points {P(x1, y)} and {P(x2, y)}.', f'{abs(x1 - x2)} units',
                 f'Both points have ordinate {fn(y)}, so the distance is |{fn(x2)} − {bracket(x1)}| = {abs(x1 - x2)}.',
                 [f'{abs(x1 + x2)} units', f'{abs(x1 - x2) + 1} units', f'{abs(x1) + abs(x2) + 2 * abs(y)} units'])
    return Q(f'Find the distance between the points {P(y, x1)} and {P(y, x2)}.', f'{abs(x1 - x2)} units',
             f'Both points have abscissa {fn(y)}, so the distance is |{fn(x2)} − {bracket(x1)}| = {abs(x1 - x2)}.',
             [f'{abs(x1 + x2)} units', f'{abs(x1 - x2) + 1} units', f'{abs(x1) + abs(x2) + 2 * abs(y)} units'])


def c1s2_pts(r):
    a, b, c = triple(r)
    x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
    x2, y2 = x1 + r.choice([-1, 1]) * a, y1 + r.choice([-1, 1]) * b
    return x1, y1, x2, y2, a, b, c


def c1s2_dist(r):
    x1, y1, x2, y2, a, b, c = c1s2_pts(r)
    return Q(f'Find the distance between A{P(x1, y1)} and B{P(x2, y2)}.', f'{c} units',
             f'AB = √[({fn(x2)} − {bracket(x1)})² + ({fn(y2)} − {bracket(y1)})²] = √({a * a} + {b * b}) = √{c * c} = {c}.',
             [f'{a + b} units', f'{c * c} units', f'{abs(x1 + x2) + abs(y1 + y2)} units'])


def c1s2_dist_surd(r):
    while True:
        x1, y1, x2, y2 = [r.randint(-7, 7) for _ in range(4)]
        d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        if d2 > 0 and not is_sq(d2) and x1 != x2 and y1 != y2:
            break
    return Q(f'Find the distance between P{P(x1, y1)} and Q{P(x2, y2)}. Leave your answer in simplest surd form.', f'{rad(d2)} units',
             f'PQ² = ({fn(x2 - x1)})² + ({fn(y2 - y1)})² = {(x2 - x1) ** 2} + {(y2 - y1) ** 2} = {d2}; PQ = √{d2}' + ('' if rad(d2) == f'√{d2}' else f' = {rad(d2)}') + '.',
             [f'{rad(d2 + 2)} units', f'{abs(x2 - x1) + abs(y2 - y1)} units', f'{d2} units'])


def c1s2_explain(r):
    x1, y1, x2, y2, a, b, c = c1s2_pts(r)
    return Q(f'Plot A{P(x1, y1)} and B{P(x2, y2)} mentally and explain, using the Baudhayana-Pythagoras theorem, how to find AB without a ruler. State AB.',
             f'AB = {c} units', f'Complete the right triangle with C{P(x2, y1)}: AC = {a}, BC = {b} (1 mark); AB² = {a}² + {b}² = {c * c}, AB = {c} (1 mark).')


def c1s2_ar(r):
    x1, y1, x2, y2, a, b, c = c1s2_pts(r)
    if r.random() < 0.5:
        return ar(f'The distance between {P(x1, y1)} and {P(x2, y2)} is {c} units.', 'The distance between two points is found by applying the Baudhayana-Pythagoras theorem to the horizontal and vertical separations.', 'a',
                  f'√({a}² + {b}²) = {c}; R is the reason.')
    return ar(f'The distance between {P(x1, y1)} and {P(x2, y2)} is {a + b} units.', 'The distance between two points is the square root of the sum of the squares of the differences of their coordinates.', 'd',
              f'The distance is √({a * a} + {b * b}) = {c}, not {a + b}; A is false and R is true.')


def c1s2_find_k(r):
    a, b, c = triple(r)
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    y2 = y1 + r.choice([-1, 1]) * b
    k1, k2 = x1 + a, x1 - a
    return Q(f'The distance between the points ({fn(x1)}, {fn(y1)}) and (k, {fn(y2)}) is {c} units. Find all possible values of k.', f'k = {fn(k2)} or k = {fn(k1)}',
             f'(k − {bracket(x1)})² + ({fn(y2 - y1)})² = {c * c} ⇒ (k − {bracket(x1)})² = {a * a} ⇒ k − {bracket(x1)} = ±{a} ⇒ k = {fn(k1)} or {fn(k2)} (3 marks; 1 mark lost if only one value).')


def c1s2_right_tri(r):
    a, b, c = triple(r)
    x, y = r.randint(-4, 4), r.randint(-4, 4)
    A, B, C = (x, y), (x + a, y), (x, y + b)
    return Q(f'Show that the points A{P(*A)}, B{P(*B)} and C{P(*C)} are the vertices of a right-angled triangle. Which angle is the right angle?',
             f'Right angle at A (AB² + AC² = BC²: {a * a} + {b * b} = {c * c})',
             f'AB = {a}, AC = {b}, BC = √({a * a} + {b * b}) = {c}; AB² + AC² = BC², so by the converse of the Baudhayana-Pythagoras theorem ∠A = 90° (4 marks).')


def c1s2_equidistant(r):
    # point on x-axis equidistant from (a,b) and (c,d): (x-a)^2+b^2=(x-c)^2+d^2 -> x = (c^2+d^2-a^2-b^2)/(2(c-a))
    while True:
        a, b, c, d = r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6)
        if c != a:
            x = Fr(c * c + d * d - a * a - b * b, 2 * (c - a))
            if x.denominator == 1 and (b, d) != (0, 0):
                break
    return Q(f'Find the point on the x-axis which is equidistant from A{P(a, b)} and B{P(c, d)}.', f'({fn(x)}, 0)',
             f'Let P = (x, 0). PA² = PB²: (x − {bracket(a)})² + {b * b} = (x − {bracket(c)})² + {d * d} ⇒ {fn(2 * (c - a))}x = {c * c + d * d - a * a - b * b} ⇒ x = {fn(x)} (4 marks).')


def c1s2_case(r):
    s = r.choice([1, 2])
    a, b, c = triple(r)
    rate = r.choice([800, 1200, 1500, 2000])
    v1, v2 = r.sample(['Rampur', 'Sonpur', 'Devgaon', 'Kalyani', 'Bhimtal', 'Nandgaon'], 2)
    return Q((f'On a district map, each unit is {s} km. Village {v1} is at (0, 0), village {v2} is at ({a}, {b}) and a health centre H is at ({a}, 0). '
              f'(i) Find the distance {v1}–H. (ii) Find the distance H–{v2}. (iii) A straight road is built from {v1} to {v2}. Find its length. '
              f'(iv) At {inr(rate)} per km, what does the straight road cost, and how many km shorter is it than going via H?'),
             f'(i) {a * s} km (ii) {b * s} km (iii) {c * s} km (iv) {inr(rate * c * s)}; {(a + b - c) * s} km shorter',
             f'Distances in units × {s} km; straight road √({a}² + {b}²) = {c} units (1 mark each part).')


# st3 midpoint

def c1s3_formula(r):
    return mcqbank([
        ('The mid-point of the segment joining (x₁, y₁) and (x₂, y₂) is …', '((x₁ + x₂)/2, (y₁ + y₂)/2)',
         ['((x₂ − x₁)/2, (y₂ − y₁)/2)', '(x₁ + x₂, y₁ + y₂)', '((x₁ + y₁)/2, (x₂ + y₂)/2)'], 'Each coordinate of the mid-point is the average of the corresponding coordinates.'),
        ('If M is the mid-point of AB, then …', 'AM = MB = AB/2', ['AM = 2MB', 'AM + AB = MB', 'AM = MB = 2AB'], 'The mid-point divides the segment into two equal halves.'),
        ('The mid-point of the segment joining (a, b) and (−a, −b) is …', '(0, 0)', ['(a, b)', '(2a, 2b)', '(−a, b)'], 'The averages of a and −a, and of b and −b, are 0.'),
    ])(r)


def c1s3_mid(r):
    x1, y1 = r.randint(-12, 12), r.randint(-12, 12)
    x2, y2 = x1 + 2 * r.randint(-6, 6), y1 + 2 * r.randint(-6, 6)
    if (x1, y1) == (x2, y2):
        x2 += 4
    m = ((x1 + x2) // 2, (y1 + y2) // 2)
    return Q(f'Find the mid-point of the segment joining A{P(x1, y1)} and B{P(x2, y2)}.', P(*m),
             f'(({fn(x1)} + {bracket(x2)})/2, ({fn(y1)} + {bracket(y2)})/2) = {P(*m)}.',
             [P(x2 - x1, y2 - y1), P((x2 - x1) // 2, (y2 - y1) // 2), P(m[1], m[0]) if m[0] != m[1] else P(m[0] + 1, m[1])])


def c1s3_mid_frac(r):
    x1, y1, x2, y2 = [r.randint(-9, 9) for _ in range(4)]
    if (x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0:
        x2 += 1
    m = (Fr(x1 + x2, 2), Fr(y1 + y2, 2))
    return Q(f'Find the mid-point of the line segment joining P{P(x1, y1)} and Q{P(x2, y2)}.', P(*m),
             f'Average the coordinates: ({fn(x1 + x2)}/2, {fn(y1 + y2)}/2) = {P(*m)}.',
             [P(Fr(x2 - x1, 2), Fr(y2 - y1, 2)), P(x1 + x2, y1 + y2), P(m[1], m[0]) if m[0] != m[1] else P(m[0] + 1, m[1])])


def c1s3_other_end(r):
    x1, y1, mx, my = [r.randint(-8, 8) for _ in range(4)]
    x2, y2 = 2 * mx - x1, 2 * my - y1
    if (x1, y1) == (mx, my):
        mx += 1
        x2 = 2 * mx - x1
    return Q(f'M{P(mx, my)} is the mid-point of AB, where A is {P(x1, y1)}. Find the coordinates of B.', P(x2, y2),
             f'({fn(x1)} + x)/2 = {fn(mx)} ⇒ x = {fn(x2)}; ({fn(y1)} + y)/2 = {fn(my)} ⇒ y = {fn(y2)}.',
             [P(Fr(x1 + mx, 2), Fr(y1 + my, 2)), P(mx - x1, my - y1), P(x1 - 2 * mx, y1 - 2 * my)])


def c1s3_explain(r):
    a, b = sorted(r.sample(range(-15, 16), 2))
    if (a + b) % 2:
        b += 1
    return Q(f'Explain, using a number line, why the point half-way between {fn(a)} and {fn(b)} is ({fn(a)} + {bracket(b)})/2, and find it.', fn((a + b) // 2),
             f'The gap is {fn(b)} − {bracket(a)} = {b - a}; half of it is {fn(Fr(b - a, 2))}; {fn(a)} + {fn(Fr(b - a, 2))} = {fn(Fr(a + b, 2))}, which equals (a + b)/2 (2 marks).')


def c1s3_ar(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if r.random() < 0.5:
        return ar(f'The mid-point of the segment joining ({a}, {-b}) and ({-a}, {b}) is the origin.', 'The mid-point has coordinates equal to the averages of the coordinates of the end-points.', 'a', 'Both true; averaging gives (0, 0).')
    return ar(f'The mid-point of ({a}, {b}) and ({a + 4}, {b + 6}) is (2, 3).', 'The mid-point has coordinates equal to the averages of the coordinates of the end-points.', 'd',
              f'The mid-point is ({a + 2}, {b + 3}); (2, 3) is half the difference, so A is false and R is true.')


def c1s3_parallelogram(r):
    A = (r.randint(-5, 5), r.randint(-5, 5))
    B = (A[0] + r.randint(3, 7), A[1] + r.randint(-2, 2))
    C = (B[0] + r.randint(1, 4), B[1] + r.randint(3, 7))
    D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
    return Q(f'A{P(*A)}, B{P(*B)} and C{P(*C)} are three vertices of parallelogram ABCD. Using the fact that the diagonals of a parallelogram bisect each other, find D.', P(*D),
             f'Mid-point of AC = {P(Fr(A[0] + C[0], 2), Fr(A[1] + C[1], 2))} = mid-point of BD ⇒ D = (A + C − B) = {P(*D)} (3 marks).')


def c1s3_diameter(r):
    a, b, c = triple(r)
    cx, cy = r.randint(-5, 5), r.randint(-5, 5)
    A = (cx - a, cy - b)
    B = (cx + a, cy + b)
    return Q(f'The end-points of a diameter of a circle are A{P(*A)} and B{P(*B)}. Find the centre and the radius of the circle.', f'Centre {P(cx, cy)}, radius {c} units',
             f'Centre = mid-point of AB = {P(cx, cy)} (2 marks); radius = distance from centre to A = √({a * a} + {b * b}) = {c} (2 marks).')


def c1s3_case(r):
    who1, who2 = two_names(r)
    x1, y1, x2, y2 = r.randint(0, 4) * 2, r.randint(0, 4) * 2, r.randint(5, 10) * 2, r.randint(5, 10) * 2
    return Q((f'{who1} lives at A({x1}, {y1}) and {who2} at B({x2}, {y2}) on a town grid (1 unit = 100 m). They agree to meet exactly half-way. '
              f'(i) Find the meeting point M. (ii) Check that AM = MB by finding AM² and MB². (iii) If they walk along the straight line at 50 m per minute, how long does each take to reach M?'),
             f'(i) M{P((x1 + x2) // 2, (y1 + y2) // 2)} (ii) AM² = MB² = {((x2 - x1) // 2) ** 2 + ((y2 - y1) // 2) ** 2} (iii) {num(100 * math.sqrt(((x2 - x1) // 2) ** 2 + ((y2 - y1) // 2) ** 2) / 50, 1)} min each (approx.)',
             'Mid-point formula (1); distance check (1); time = distance ÷ speed with distance in metres (2).')


# st4 maps and figures

def c1s4_rect_area(r):
    x1, y1 = r.randint(-6, 2), r.randint(-6, 2)
    w, h = r.randint(2, 9), r.randint(2, 9)
    return Q(f'A rectangle has vertices A{P(x1, y1)}, B{P(x1 + w, y1)}, C{P(x1 + w, y1 + h)} and D{P(x1, y1 + h)}. Find its area and perimeter.', f'Area {w * h} sq units, perimeter {2 * (w + h)} units',
             f'AB = {w}, BC = {h}; area = {w * h}, perimeter = 2({w} + {h}) = {2 * (w + h)}.',
             [f'Area {2 * (w + h)} sq units, perimeter {w * h} units', f'Area {w * h} sq units, perimeter {w + h} units', f'Area {(w + 1) * (h + 1)} sq units, perimeter {2 * (w + h) + 4} units'])


def c1s4_fourth(r):
    x1, y1 = r.randint(-6, 3), r.randint(-6, 3)
    s = r.randint(2, 8)
    pts = [(x1, y1), (x1 + s, y1), (x1 + s, y1 + s)]
    ans = (x1, y1 + s)
    return mcq(f'Three vertices of a square are {P(*pts[0])}, {P(*pts[1])} and {P(*pts[2])}. The fourth vertex is …', P(*ans),
               [P(x1 + s, y1 - s), P(x1 - s, y1 + s), P(x1 + 2 * s, y1 + s)], f'The sides are parallel to the axes with side {s}, so the fourth vertex is {P(*ans)}.', r)


def c1s4_move(r):
    who = name(r)
    x, y = r.randint(-5, 5), r.randint(-5, 5)
    e, n = nz(r, 1, 6), nz(r, 1, 6)
    de = f'{abs(e)} units {"east" if e > 0 else "west"}'
    dn = f'{abs(n)} units {"north" if n > 0 else "south"}'
    return Q(f'On a grid map (east = positive x, north = positive y), {who} starts at {P(x, y)}, walks {de} and then {dn}. Where does {who} end up?', P(x + e, y + n),
             f'East/west changes x by {fn(e)}; north/south changes y by {fn(n)}: {P(x + e, y + n)}.',
             [P(x + n, y + e), P(x - e, y - n), P(x + e, y - n)])


def c1s4_explain(r):
    s = r.randint(2, 7)
    x, y = r.randint(-4, 4), r.randint(-4, 4)
    return Q(f'Points A{P(x, y)}, B{P(x + s, y)}, C{P(x + s, y + s)}, D{P(x, y + s)} are plotted. Explain using coordinates why ABCD is a square and not just a rectangle.', 'All four sides equal (each ' + str(s) + ' units) and adjacent sides are along horizontal and vertical lines, so all angles are 90°.',
             f'AB and DC horizontal, AD and BC vertical ⇒ right angles (1); each side = {s} (1).')


def c1s4_ar(r):
    s = r.randint(2, 9)
    return arbank([
        (f'The triangle with vertices (0, 0), ({s}, 0) and (0, {s}) has area {s * s / 2:g} square units.', 'The two legs of the triangle lie along the axes and are perpendicular.', 'a', f'Area = ½ × {s} × {s}; R explains why base × height works.'),
        (f'The points (0, 0), ({s}, 0), ({s}, {s}) and (0, {s}) form a rectangle that is not a square.', 'A square is a rectangle with all four sides equal.', 'd', f'All sides are {s}: it is a square, so A is false; R is true.'),
        (f'The points (1, {s}), (2, {s}) and (7, {s}) lie on one straight line.', 'Points having the same ordinate lie on a line parallel to the x-axis.', 'a', 'Same y-coordinate ⇒ on the line y = constant.'),
    ])(r)


def c1s4_tri_area(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    sx, sy = r.choice([-1, 1]), r.choice([-1, 1])
    return Q(f'Find the area of the triangle formed by the points O(0, 0), A({fn(sx * a)}, 0) and B(0, {fn(sy * b)}).', f'{num(a * b / 2)} square units',
             f'Right angle at O; legs {a} and {b}; area = ½ × {a} × {b} = {num(a * b / 2)}.',
             [f'{a * b} square units', f'{num(a * b / 4)} square units', f'{a + b} square units'])


def c1s4_case(r):
    s = r.choice([50, 100, 200])
    sch = (r.randint(1, 5), r.randint(1, 5))
    mkt = (-r.randint(1, 6), r.randint(1, 5))
    hos = (r.randint(1, 6), -r.randint(1, 5))
    return Q((f'A town map uses the bus stand as the origin (1 unit = {s} m). The school is at {P(*sch)}, the market at {P(*mkt)} and the hospital at {P(*hos)}. '
              f'(i) Which place lies in Quadrant II? (ii) How far east of the market is the school? (iii) Find the straight-line distance from the bus stand to the hospital, correct to the nearest metre. '
              f'(iv) A new park is to be built exactly half-way between the school and the hospital. Give its coordinates.'),
             f'(i) Market (ii) {(sch[0] - mkt[0]) * s} m (iii) ≈ {round(s * math.hypot(*hos))} m (iv) {P(Fr(sch[0] + hos[0], 2), Fr(sch[1] + hos[1], 2))}',
             'Quadrant signs (1); horizontal difference × scale (1); distance formula × scale (1); mid-point (1).')


def c1s4_kite(r):
    a, b, c = triple(r)
    return Q(f'Plot A(0, {b}), B({a}, 0), C(0, {-b}) and D({-a}, 0). Name the quadrilateral ABCD, find the length of each side and its area.', f'Rhombus; each side {c} units; area {2 * a * b} sq units',
             f'Each side = √({a}² + {b}²) = {c}; diagonals {2 * b} and {2 * a} are perpendicular, area = ½ × {2 * a} × {2 * b} = {2 * a * b} (5 marks).')


# ---------------- ch02 Linear polynomials ----------------

def rand_poly(r, deg=2):
    c = [nz(r, 1, 9) for _ in range(deg + 1)]
    return c


def c2s1_coeff(r):
    c = rand_poly(r, 2)
    which = r.choice([('x', 1), ('x²', 0)])
    ans = c[which[1]]
    return mcq(f'What is the coefficient of {which[0]} in {poly(c)}?', fn(ans), [fn(-ans), fn(c[2]) if c[2] != ans and c[2] != -ans else fn(ans + 2), fn(c[1 - which[1]]) if abs(c[1 - which[1]]) != abs(ans) else fn(ans + 1)],
               'The coefficient is the number multiplying that power of x, with its sign.', r)


def c2s1_terms(r):
    k = r.randint(2, 4)
    c = [nz(r, 1, 9) for _ in range(k)]
    vs = r.sample(['x', 'y', 'xy', 'x²', 'p', 'm'], k - 1)
    e = term(c[0], vs[0], first=True) + ''.join(term(cc, v) for cc, v in zip(c[1:-1], vs[1:])) + f' {signed(c[-1])}'
    return Q(f'How many terms does the expression {e} have? Name the constant term.', f'{k} terms; constant term {fn(c[-1])}',
             'Terms are separated by + or − signs; the term without a variable is the constant.',
             [f'{k - 1} terms; constant term {fn(c[-1])}', f'{k} terms; constant term {fn(c[0])}', f'{k + 1} terms; constant term {fn(-c[-1])}'])


def c2s1_ispoly(r):
    return mcqbank([
        ('Which of the following is a polynomial in x?', '3x² − √5 x + 1', ['x + 1/x', '√x + 4', '2/x² − 7'], 'Exponents of x must be whole numbers; 1/x, √x and 1/x² have exponents −1, ½ and −2.'),
        ('Which of the following is a linear polynomial?', '7 − 2x', ['x² − 4', 'x³ + x', '5'], 'A linear polynomial has degree 1.'),
        ('Which of the following is NOT a polynomial?', 'y + 3/y', ['y² − 2y', '√3 y + 1', '−4'], '3/y = 3y⁻¹ has a negative exponent.'),
        ('In the expression 4πr, which is the variable?', 'r', ['π', '4', '4π'], 'π and 4 are constants; r varies.'),
        ('The degree of a non-zero constant polynomial is …', '0', ['1', 'not defined', '−1'], 'c = c·x⁰.'),
    ])(r)


def c2s1_explain(r):
    return xbank([
        ('Is x + 1/x a polynomial? Give a reason.', 'No.', '1/x = x⁻¹; in a polynomial every exponent of the variable must be a whole number (2 marks).'),
        ('Explain the difference between a variable and a constant using the formula for the perimeter of a square, P = 4s.', 's and P are variables (they change with the square); 4 is a constant.', 'Correct identification (1) with reason (1).'),
        ('Explain why 5x and 5x² are not like terms.', 'They have different powers of x.', 'Like terms have the same variables raised to the same powers (2 marks).'),
        ('Is √2 x + 3 a polynomial? Explain.', 'Yes, a linear polynomial.', 'The coefficient √2 may be irrational; the exponent of x is 1, a whole number (2 marks).'),
        ('Why is 0 called the zero polynomial and why is its degree not defined?', 'All its coefficients are 0, so no power of x has a non-zero coefficient.', 'Statement (1), reason (1).'),
    ])(r)


def c2s1_ar(r):
    return arbank([
        ('The degree of 5x³ − 2x + 7 is 3.', 'The degree of a polynomial is the highest power of the variable with a non-zero coefficient.', 'a', 'Both true and R explains A.'),
        ('x² + 1/x² is a polynomial of degree 2.', 'In a polynomial all exponents of the variable are whole numbers.', 'd', '1/x² has exponent −2, so A is false; R is true.'),
        ('3x and −7x are like terms.', 'Like terms must have the same coefficient.', 'c', 'A is true; like terms need the same variable part, not the same coefficient.'),
        ('2x + 3 is a linear polynomial.', 'A linear polynomial has degree 1.', 'a', 'Both true; R explains A.'),
        ('The constant term of 4x² − 9 is 4.', 'The constant term is the term that has no variable.', 'd', 'The constant term is −9; A is false, R is true.'),
    ])(r)


def c2s1_simplify(r):
    a, b, c, d, e, f = [nz(r, 1, 9) for _ in range(6)]
    res = [a + d, b + e, c + f]
    return Q(f'Simplify ({poly([a, b, c])}) + ({poly([d, e, f])}).', poly(res),
             'Add the coefficients of like terms: x², x and the constants.',
             [poly([a - d, b - e, c - f]), poly([a + d, b - e, c + f]), poly([a * d, b + e, c + f])])


def c2s1_degree(r):
    k = r.randint(2, 5)
    c = [nz(r, 1, 9) for _ in range(k + 1)]
    c[r.randint(1, k - 1)] = 0
    return Q(f'Write the degree of the polynomial {poly(c)}.', str(k),
             'The highest power of x with a non-zero coefficient.', num_distractors(k, k + 1, k - 1, len([x for x in c if x])))


def c2s1_perimeter(r):
    a, b, c, d = r.randint(2, 6), r.randint(1, 9), r.randint(1, 4), r.randint(1, 9)
    k = r.randint(2, 6)
    return Q(f'A rectangle has length ({lin(a, b)}) cm and breadth ({lin(c, d)}) cm. Write its perimeter as a polynomial and find the perimeter when x = {k}.',
             f'({lin(2 * (a + c), 2 * (b + d))}) cm; {2 * (a + c) * k + 2 * (b + d)} cm',
             f'P = 2[({lin(a, b)}) + ({lin(c, d)})] = {lin(2 * (a + c), 2 * (b + d))}; at x = {k}: {2 * (a + c) * k + 2 * (b + d)} (3 marks).')


def c2s1_context(r):
    who = name(r)
    p, q = r.choice([25, 30, 40, 45, 60]), r.choice([10, 12, 15, 20])
    f = r.choice([20, 30, 50])
    n, m = r.randint(3, 9), r.randint(2, 8)
    return Q((f'{who} buys n notebooks at ₹{p} each and m pens at ₹{q} each, and pays a fixed delivery charge of ₹{f}. '
              f'(i) Write an algebraic expression for the total cost. (ii) Name the variables, the coefficients and the constant term. (iii) Find the cost when n = {n} and m = {m}.'),
             f'(i) {p}n + {q}m + {f} (ii) variables n, m; coefficients {p}, {q}; constant {f} (iii) {inr(p * n + q * m + f)}',
             f'1 + 1 + 2 marks; {p} × {n} + {q} × {m} + {f} = {p * n + q * m + f}.')


# st2 value and zero

def lin_ab(r):
    a = nz(r, 1, 9)
    b = nz(r, 1, 20)
    return a, b


def c2s2_zero(r):
    a, b = lin_ab(r)
    z = Fr(-b, a)
    return mcq(f'The zero of the polynomial p(x) = {lin(a, b)} is …', fn(z), [fn(-z), fn(Fr(a, -b)) if Fr(a, -b) not in (z, -z) else fn(z + 1), fn(Fr(b, 1)) if b not in (z, -z) else fn(z + 2)],
               f'p(x) = 0 ⇒ {lin(a, b)} = 0 ⇒ x = {fn(z)}.', r)


def c2s2_value(r):
    a, b = lin_ab(r)
    k = nz(r, 1, 8)
    return Q(f'If p(x) = {lin(a, b)}, find p({fn(k)}).', fn(a * k + b), f'p({fn(k)}) = {fn(a)} × {bracket(k)} {signed(b)} = {fn(a * k + b)}.',
             num_distractors(a * k + b, a * k - b, -a * k + b, a + b + k))


def c2s2_check(r):
    a = nz(r, 1, 6)
    z = nz(r, 1, 6)
    b = -a * z
    k = z if r.random() < 0.5 else z + r.choice([-1, 1])
    val = a * k + b
    return Q(f'Is x = {fn(k)} a zero of p(x) = {lin(a, b)}? Justify.', 'Yes' if val == 0 else 'No', f'p({fn(k)}) = {fn(val)}; it is a zero only if the value is 0.')


def c2s2_explain(r):
    a, b = lin_ab(r)
    return Q(f'Explain why the linear polynomial {lin(a, b)} has exactly one zero, and find it.', fn(Fr(-b, a)),
             f'{lin(a, b)} = 0 is a linear equation with a ≠ 0, which has exactly one solution x = −b/a = {fn(Fr(-b, a))} (2 marks).')


def c2s2_ar(r):
    a, b = lin_ab(r)
    z = Fr(-b, a)
    if r.random() < 0.5:
        return ar(f'The zero of {lin(a, b)} is {fn(z)}.', 'The zero of ax + b (a ≠ 0) is −b/a.', 'a', 'Both true; R gives A.')
    return ar('The polynomial p(x) = 5 has no zero.', 'Every linear polynomial has exactly one zero.', 'b', 'Both true, but 5 is a constant polynomial, so R does not explain A.')


def c2s2_find_a(r):
    a, b = lin_ab(r)
    k = nz(r, 1, 6)
    v = a * k + b
    return Q(f'If p(x) = ax {signed(b)} and p({fn(k)}) = {fn(v)}, find a.', fn(a), f'{term(k, "a", first=True)} {signed(b)} = {fn(v)} ⇒ a = ' + (f'{fn(v - b)}/{bracket(k)} = ' if k != 1 else '') + f'{fn(a)}.',
             num_distractors(a, -a, v - b, a + 1))


def c2s2_two_cond(r):
    a, b = lin_ab(r)
    k1, k2 = r.sample(range(-5, 6), 2)
    return Q(f'A linear polynomial p(x) = ax + b satisfies p({fn(k1)}) = {fn(a * k1 + b)} and p({fn(k2)}) = {fn(a * k2 + b)}. Find a and b, and hence the zero of p(x).',
             f'a = {fn(a)}, b = {fn(b)}; zero {fn(Fr(-b, a))}',
             f'Subtracting: a({fn(k1)} − {bracket(k2)}) = {fn(a * (k1 - k2))} ⇒ a = {fn(a)}; then b = {fn(b)}; zero = −b/a = {fn(Fr(-b, a))} (3 marks).')


def c2s2_taxi(r):
    city = r.choice(['Pune', 'Jaipur', 'Kochi', 'Indore', 'Lucknow'])
    base, rate = r.choice([30, 40, 50, 60]), r.choice([12, 14, 15, 16, 18])
    d = r.randint(4, 25)
    return Q((f'A taxi in {city} charges ₹{base} as a fixed charge plus ₹{rate} per km. (i) Write the fare F(d) for d km as a linear polynomial. '
              f'(ii) Find F({d}). (iii) A passenger paid ₹{base + rate * d + rate * 3}. How far did the passenger travel? (iv) Does F(d) have a zero that makes sense in this context? Explain.'),
             f'(i) F(d) = {rate}d + {base} (ii) ₹{base + rate * d} (iii) {d + 3} km (iv) zero is d = {fn(Fr(-base, rate))}, a negative distance, so it has no meaning here',
             '1 mark each part.')


def c2s2_breakeven(r):
    who = name(r)
    cost, price = r.choice([(1200, 40), (1500, 50), (900, 30), (2400, 60), (1800, 45)])
    return Q((f'{who} sets up a lemonade stall at a school fair. The fixed cost of the stall is ₹{cost} and each glass sells for ₹{price}. '
              f'Write the profit P(n) after selling n glasses as a linear polynomial, find its zero and explain what the zero means. How many glasses give a profit of ₹{price * 10}?'),
             f'P(n) = {price}n − {cost}; zero n = {cost // price} (break-even: no profit, no loss); {cost // price + 10} glasses',
             f'P(n) (1), zero {cost}/{price} = {cost // price} (1), meaning (1), {cost // price + 10} glasses (1).')


# st3 linear rules from tables

def c2s3_table_vals(r):
    a, b = r.randint(2, 9), r.randint(-9, 12)
    xs = [1, 2, 3, 4]
    ys = [a * x + b for x in xs]
    return a, b, xs, ys


def c2s3_rule_mcq(r):
    a, b, xs, ys = c2s3_table_vals(r)
    tab = ', '.join(f'x = {x}: y = {fn(y)}' for x, y in zip(xs, ys))
    return mcq(f'A table gives {tab}. Which rule fits the table?', f'y = {lin(a, b)}',
               [f'y = {lin(a + 1, b - 1)}', f'y = {lin(b if b > 0 else a + 2, a)}', f'y = {lin(a, b + a)}'],
               f'The constant difference is {a}, so y = {a}x + c; x = 1 gives c = {fn(b)}.', r)


def c2s3_next(r):
    a, b, xs, ys = c2s3_table_vals(r)
    return Q(f'The values of y for x = 1, 2, 3, 4 are {", ".join(map(fn, ys))}. What is y when x = 5?', fn(5 * a + b),
             f'y increases by {a} each time: {fn(ys[-1])} + {a} = {fn(5 * a + b)}.', num_distractors(5 * a + b, ys[-1] + 1, 2 * ys[-1], 5 * a))


def c2s3_find_rule(r):
    a, b, xs, ys = c2s3_table_vals(r)
    k = r.randint(15, 60)
    return Q(f'Find a linear rule y = ax + b for the table x: 1, 2, 3, 4 and y: {", ".join(map(fn, ys))}. Use it to find y when x = {k}.', f'y = {lin(a, b)}; y = {fn(a * k + b)}',
             f'Constant difference a = {a}; b = {fn(ys[0])} − {a} = {fn(b)}; y({k}) = {fn(a * k + b)}.',
             [f'y = {lin(a, b + a)}; y = {fn(a * k + b + a)}', f'y = {lin(a, b)}; y = {fn(a * k)}', f'y = {lin(a + 1, b)}; y = {fn((a + 1) * k + b)}'])


def c2s3_matchstick(r):
    shape, a, b = r.choice([('squares', 3, 1), ('triangles', 2, 1), ('pentagons', 4, 1), ('hexagons', 5, 1)])
    n = r.randint(12, 60)
    return Q(f'Matchsticks are used to make a row of {shape} joined side by side. Find a rule for the number of matchsticks M needed for n {shape}, and use it to find M for n = {n}.',
             f'M = {a}n + {b}; {a * n + b} matchsticks', f'The first shape needs {a + b}; each new shape adds {a}: M = {a}n + {b}; {a} × {n} + {b} = {a * n + b} (3 marks).',
             [f'{(a + 1) * n} matchsticks', f'{a * n} matchsticks', f'{(a + 1) * n + b} matchsticks'])


def c2s3_explain(r):
    a, b, xs, ys = c2s3_table_vals(r)
    return Q(f'The table x: 1, 2, 3, 4 and y: {", ".join(map(fn, ys))} is said to follow a linear rule. Explain how you can tell from the table alone.', f'The differences in y are constant ({a}) for equal steps in x.',
             'Constant first difference for equal steps in x ⇒ linear (2 marks).')


def c2s3_ar(r):
    a, b = r.randint(2, 6), r.randint(1, 9)
    sq = [1, 4, 9, 16]
    if r.random() < 0.5:
        return ar(f'The table x: 1, 2, 3, 4; y: {", ".join(str(a * x + b) for x in range(1, 5))} follows a linear rule.', 'A rule is linear when y changes by the same amount for each unit increase in x.', 'a', f'Differences are all {a}.')
    return ar(f'The table x: 1, 2, 3, 4; y: {", ".join(str(s + b) for s in sq)} follows a linear rule.', 'A rule is linear when y changes by the same amount for each unit increase in x.', 'd', 'Differences 3, 5, 7 are not constant; A is false, R true.')


def c2s3_which_step(r):
    shape, a, b = r.choice([('squares', 3, 1), ('triangles', 2, 1), ('pentagons', 4, 1)])
    n = r.randint(20, 90)
    M = a * n + b
    left = r.randint(0, a - 1)
    who = name(r)
    return Q(f'For a row of {shape} made with matchsticks, M = {a}n + {b}. {who} has {M + left} matchsticks. What is the largest number of {shape} that can be made, and how many sticks are left over?',
             f'{n} {shape}; {left} left over', f'{a}n + {b} ≤ {M + left} ⇒ n ≤ {fn(Fr(M + left - b, a))}, so n = {n}; sticks used {M}, left over {M + left} − {M} = {left} (3 marks).')


def c2s3_plans(r):
    f1, r1 = r.choice([(20, 4), (100, 2), (50, 3)])
    f2, r2 = f1 + r.choice([150, 200, 300]), r1 - 1 if r1 > 1 else r1
    if r2 == r1:
        r2 = r1 - 0.5
    m = (f2 - f1) / (r1 - r2)
    return Q((f'Plan A for a mobile data pack costs ₹{f1} plus ₹{num(r1)} per GB; Plan B costs ₹{f2} plus ₹{num(r2)} per GB. '
              f'Write the cost of each plan for g GB as a linear rule, find for how many GB both plans cost the same, and say which plan is cheaper for heavy users.'),
             f'A = {num(r1)}g + {f1}, B = {num(r2)}g + {f2}; equal at g = {num(m)} GB; Plan B is cheaper beyond {num(m)} GB',
             'Two rules (1), equate (1), solve (1), interpret (1).')


# st4 graph y = ax + b

def c2s4_intercept(r):
    a, b = nz(r, 1, 6), nz(r, 1, 9)
    return mcq(f'The graph of y = {lin(a, b)} cuts the y-axis at …', P(0, b), [P(b, 0), P(0, a), P(Fr(-b, a), 0)],
               f'On the y-axis x = 0, so y = {fn(b)}.', r)


def c2s4_rate(r):
    a, b = nz(r, 1, 9), nz(r, 1, 9)
    return Q(f'For the line y = {lin(a, b)}, by how much does y change when x increases by 1?', f'y {"increases" if a > 0 else "decreases"} by {abs(a)}',
             f'The coefficient of x ({fn(a)}) is the rate of change.', [f'y {"increases" if a > 0 else "decreases"} by {abs(b)}', f'y {"decreases" if a > 0 else "increases"} by {abs(a)}', f'y {"increases" if a > 0 else "decreases"} by {abs(a + b)}'])


def c2s4_onpoint(r):
    a, b = nz(r, 1, 6), nz(r, 1, 9)
    x = nz(r, 1, 5)
    y = a * x + b + (0 if r.random() < 0.5 else r.choice([-1, 1]))
    ok = y == a * x + b
    return Q(f'Does the point {P(x, y)} lie on the graph of y = {lin(a, b)}? Show your check.', 'Yes' if ok else 'No',
             f'At x = {fn(x)}, y = {fn(a)} × {bracket(x)} {signed(b)} = {fn(a * x + b)}; {"equal" if ok else "not equal to " + fn(y)}.')


def c2s4_explain(r):
    who = name(r)
    a, b = r.choice([5, 8, 10, 12, 15]), r.choice([20, 50, 100, 150])
    return Q(f'{who}\'s savings S (in ₹) after w weeks follow S = {a}w + {b}. Explain what {a} and {b} mean in this situation, and how they appear on the graph.', f'{b} = savings at the start (y-intercept); {a} = amount added each week (rate of change, steepness).',
             'Intercept meaning (1), rate meaning (1).')


def c2s4_ar(r):
    a, b = nz(r, 1, 6), nz(r, 1, 9)
    return arbank([
        (f'The graph of y = {fn(a)}x passes through the origin.', 'For y = ax + b, the graph passes through the origin exactly when b = 0.', 'a', 'Both true; R explains A.'),
        (f'The lines y = {lin(a, b)} and y = {lin(a, b + 3)} never meet.', 'Lines with the same rate of change and different intercepts are parallel.', 'a', 'Both true; R explains A.'),
        (f'The graph of y = {lin(a, b)} passes through ({fn(b)}, 0).', 'A line cuts the x-axis where y = 0.', 'd', f'It cuts the x-axis at x = {fn(Fr(-b, a))}; A is false, R true.'),
    ])(r)


def c2s4_two_pts(r):
    a, b = nz(r, 1, 6), nz(r, 1, 9)
    x1, x2 = r.sample(range(-4, 6), 2)
    return Q(f'A line y = ax + b passes through {P(x1, a * x1 + b)} and {P(x2, a * x2 + b)}. Find a and b.', f'a = {fn(a)}, b = {fn(b)}',
             f'a = change in y ÷ change in x = {fn(a * (x2 - x1))}/{fn(x2 - x1)} = {fn(a)}; b = {fn(a * x1 + b)} − {bracket(a)} × {bracket(x1)} = {fn(b)}.',
             [f'a = {fn(b)}, b = {fn(a)}', f'a = {fn(-a)}, b = {fn(b)}', f'a = {fn(a)}, b = {fn(-b)}'])


def c2s4_triangle(r):
    a = r.choice([1, 2, 3, 4, 6])
    k = r.randint(1, 4)
    b = a * k * r.choice([1, 2, 3])
    a = -a
    xi = Fr(-b, a)
    return Q(f'The line y = {lin(a, b)} meets the x-axis at A and the y-axis at B. Find A and B and the area of triangle OAB, where O is the origin.', f'A{P(xi, 0)}, B{P(0, b)}, area {fn(abs(xi * b) / 2)} sq units',
             f'y = 0 ⇒ x = {fn(xi)}; x = 0 ⇒ y = {fn(b)}; area = ½ × {fn(abs(xi))} × {abs(b)} = {fn(abs(xi * b) / 2)} (3 marks).')


def c2s4_tank(r):
    cap, start, rate = r.choice([(1000, 100, 50), (2000, 200, 120), (1500, 300, 80), (1200, 0, 60)])
    t = (cap - start) / rate
    return Q((f'A water tank of capacity {cap} L already has {start} L in it. A pump adds {rate} L per minute. (i) Write V(t), the volume after t minutes. '
              f'(ii) What are the intercept and the rate of change of the graph of V against t? (iii) After how many minutes is the tank full? (iv) Why is the graph only drawn for 0 ≤ t ≤ {num(t)}?'),
             f'(i) V = {rate}t + {start} (ii) intercept {start} L, rate {rate} L/min (iii) {num(t)} min (iv) before t = 0 nothing is pumped and after {num(t)} min the tank overflows',
             '1 mark each part.')


def c2s4_meet(r):
    who1, who2 = two_names(r)
    s1, d1 = r.choice([(500, 200), (300, 500), (1000, 100)])
    s2, d2 = s1 + r.choice([400, 600, 1000]), d1 - r.choice([50, 100])
    if d2 <= 0:
        raise ValueError
    w = (s2 - s1) / (d1 - d2)
    return Q((f'{who1} has ₹{s1} and saves ₹{d1} every month; {who2} has ₹{s2} and saves ₹{d2} every month. '
              f'Write each person\'s savings as y = ax + b (x months), and find after how many months they will have equal savings and how much each will have then.'),
             f'{who1}: y = {d1}x + {s1}; {who2}: y = {d2}x + {s2}; after {num(w)} months, ₹{num(d1 * w + s1)} each',
             'Two linear rules (2), equating (1), solving and value (2).')


# ---------------- ch03 The World of Numbers ----------------

def c3s1_classify(r):
    return mcqbank([
        ('−7 is …', 'an integer and a rational number but not a natural number', ['a natural number', 'a whole number but not an integer', 'an irrational number'], '−7 = −7/1 is rational; it is an integer but not natural or whole.'),
        ('0 is …', 'a whole number, an integer and a rational number', ['a natural number', 'irrational', 'neither rational nor an integer'], '0 = 0/1; it is whole but not natural.'),
        ('Which of these is a rational number that is not an integer?', '−3/4', ['−12', '0', '√16'], '√16 = 4 is an integer; −3/4 is not.'),
        ('Every natural number is …', 'a whole number', ['an irrational number', 'a negative integer', 'a non-terminating decimal'], 'ℕ ⊂ 𝕎 ⊂ ℤ ⊂ ℚ.'),
        ('Which statement is true?', 'Every integer is a rational number.', ['Every rational number is an integer.', 'Every whole number is a natural number.', 'Every rational number is a natural number.'], 'n = n/1.'),
        ('Which number is a rational number?', '0.75', ['√3', 'π', '√7'], '0.75 = 3/4.'),
    ])(r)


def c3s1_pq(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    while math.gcd(a, b) != 1:
        b += 1
    k = r.randint(2, 6)
    return Q(f'Write {fn(-a * k)}/{b * k} in standard form (lowest terms, positive denominator).', f'{frac(-a, b)}',
             f'HCF of {a * k} and {b * k} is {k}; divide both by it.', [frac(-a * k, b), frac(a, b), frac(-a, b * k)])


def c3s1_order(r):
    fr = set()
    while len(fr) < 3:
        fr.add(Fr(nz(r, 1, 9), r.randint(2, 9)))
    fr = list(fr)
    s = sorted(fr)
    return Q(f'Arrange in ascending order: {", ".join(fn(x) for x in fr)}.', ', '.join(fn(x) for x in s),
             f'Convert to a common denominator or to decimals ({", ".join(num(float(x), 3) for x in fr)}).',
             [', '.join(fn(x) for x in reversed(s)), ', '.join(fn(x) for x in [s[1], s[0], s[2]]), ', '.join(fn(x) for x in [s[0], s[2], s[1]])])


def c3s1_sum(r):
    a, b, c = [Fr(nz(r, 1, 9), r.randint(2, 9)) for _ in range(3)]
    res = a + b - c
    return Q(f'Simplify {fn(a)} + ({fn(b)}) − ({fn(c)}) and write the answer as p/q in lowest terms.', fn(res),
             f'LCM of denominators, then combine: {fn(res)}.', [fn(a + b + c), fn(a - b - c), fn(res + 1)])


def c3s1_explain(r):
    return xbank([
        ('Explain why every integer is a rational number. Give an example.', 'Any integer n can be written as n/1, a ratio of integers with non-zero denominator.', 'Definition (1) and example such as −5 = −5/1 (1).'),
        ('Are the integers closed under division? Justify with an example.', 'No.', 'e.g. 3 ÷ 4 = 3/4 is not an integer (2 marks).'),
        ('Are the rational numbers closed under subtraction? Explain.', 'Yes.', 'a/b − c/d = (ad − bc)/bd is again a ratio of integers with bd ≠ 0 (2 marks).'),
        ('Is the set of whole numbers closed under subtraction? Give an example.', 'No.', 'e.g. 3 − 5 = −2 is not a whole number (2 marks).'),
        ('Why can the denominator q in p/q never be 0?', 'Division by 0 is not defined.', 'p/0 would need a number that multiplied by 0 gives p ≠ 0, which does not exist (2 marks).'),
    ])(r)


def c3s1_ar(r):
    return arbank([
        ('−5 is a rational number.', 'Every integer n can be written as n/1.', 'a', 'Both true; R explains A.'),
        ('Every rational number is an integer.', 'Every integer is a rational number.', 'd', '1/2 is rational but not an integer; A false, R true.'),
        ('Zero is a rational number.', 'Zero can be written as 0/q for any non-zero integer q.', 'a', 'Both true; R explains A.'),
        ('The sum of two rational numbers is always rational.', 'The rational numbers are closed under addition.', 'a', 'R is the closure property behind A.'),
        ('The quotient of two integers is always an integer.', 'Integers are closed under multiplication.', 'd', 'A is false (e.g. 1 ÷ 2 = 1/2); R is true.'),
    ])(r)


def c3s1_between_ints(r):
    a = Fr(r.randint(5, 60), r.randint(2, 9))
    if a.denominator == 1:
        a += Fr(1, 3)
    lo = math.floor(a)
    return Q(f'Between which two consecutive integers does {fn(a)} lie?', f'{lo} and {lo + 1}', f'{fn(a)} ≈ {num(float(a), 3)}.',
             [f'{lo - 1} and {lo}', f'{lo + 1} and {lo + 2}', f'{lo} and {lo + 2}'])


def c3s1_closure_case(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return Q((f'A teacher writes four sets on the board: natural numbers ℕ, whole numbers 𝕎, integers ℤ and rational numbers ℚ. '
              f'(i) Is {a} − {a + b} in ℕ? in ℤ? (ii) Is {a} ÷ {a + b} in ℤ? in ℚ? (iii) Which of these sets is closed under subtraction? (iv) Which of these sets is closed under division by non-zero numbers?'),
             f'(i) not in ℕ, in ℤ ({-b}) (ii) not in ℤ, in ℚ ({frac(a, a + b)}) (iii) ℤ and ℚ (iv) ℚ only (over non-zero divisors)',
             '1 mark each part.')


# st2 density and decimals

def c3s2_terminating(r):
    good_d = r.choice([8, 16, 20, 25, 40, 50, 80, 125, 32])
    bad = r.sample([3, 6, 7, 9, 12, 14, 15, 21, 24, 30], 3)
    n = r.choice([1, 3, 7, 9, 11, 13])
    while math.gcd(n, good_d) != 1:
        n += 2
    opts_bad = []
    for d in bad:
        m = r.choice([1, 2, 5, 7, 11])
        while math.gcd(m, d) != 1:
            m += 1
        opts_bad.append(f'{m}/{d}')
    return mcq('Which of the following has a terminating decimal expansion?', f'{n}/{good_d}', opts_bad,
               f'{good_d} has only 2 and 5 as prime factors, so {n}/{good_d} terminates; the others have a factor 3 or 7 in the denominator.', r)


def c3s2_decimal(r):
    d = r.choice([8, 16, 20, 25, 40, 32])
    n = r.choice([x for x in range(1, 2 * d) if math.gcd(x, d) == 1])
    return Q(f'Write {n}/{d} as a decimal.', num(n / d, 6), f'Divide: {n} ÷ {d} = {num(n / d, 6)} (terminates, as {d} = 2ᵐ5ⁿ).',
             [num(n / d * 10, 6), num(d / n, 4), num(n / d + 0.1, 6)])


def c3s2_rec(r):
    k = r.choice([1, 2])
    if k == 1:
        a = r.randint(1, 8)
        f = Fr(a, 9)
        s = f'0.{a}{a}{a}…'
    else:
        a = r.randint(10, 98)
        f = Fr(a, 99)
        s = f'0.{a:02d}{a:02d}…'
    return Q(f'Express {s} (the block repeats) in the form p/q.', fn(f),
             f'Let x = {s}. Multiply by {10 ** k}: {10 ** k}x − x = {a} ⇒ x = {a}/{10 ** k - 1} = {fn(f)}.',
             [frac(a, 10 ** k), frac(a, 10 ** k + 1), frac(a, 10 ** k - 10 if k == 2 else 90)])


def c3s2_mixed(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if a == b:
        b = (b % 9) + 1
    f = Fr(10 * a + b - a, 90)
    return Q(f'Express 0.{a}{b}{b}{b}… (only the digit {b} repeats) in the form p/q.', fn(f),
             f'x = 0.{a}{b}{b}…; 100x − 10x = {a}{b}.{b}… − {a}.{b}… = {10 * a + b - a} ⇒ x = {10 * a + b - a}/90' + ('' if f.denominator == 90 else f' = {fn(f)}') + ' (3 marks).')


def c3s2_between(r):
    a = Fr(r.randint(1, 5), r.randint(2, 7))
    b = a + Fr(r.randint(1, 3), r.randint(5, 9))
    k = r.choice([3, 4, 5])
    m = 10 * (k + 1)
    xs = [a + (b - a) * i / (k + 1) for i in range(1, k + 1)]
    return Q(f'Find any {k} rational numbers between {fn(a)} and {fn(b)}.', ', '.join(fn(x) for x in xs),
             f'One method: divide the gap into {k + 1} equal parts, a + i(b − a)/{k + 1} for i = 1 … {k}. Any {k} correct numbers strictly between earn full marks.')


def c3s2_explain(r):
    d = r.choice([12, 24, 30, 15, 6, 14, 21, 35, 18, 28])
    n = r.choice([m for m in range(1, 2 * d) if math.gcd(m, d) == 1 and m % 3 and m % 7])
    return Q(f'Without long division, explain whether {n}/{d} has a terminating or a non-terminating recurring decimal expansion.', 'Non-terminating recurring',
             f'{d} has a prime factor other than 2 or 5 ({[p for p in (3, 7) if d % p == 0][0]}), and {n}/{d} is in lowest terms ⇒ non-terminating recurring (2 marks).')


def c3s2_ar(r):
    return arbank([
        ('Between any two rational numbers there are infinitely many rational numbers.', 'The average of two rational numbers lies between them and is rational.', 'a', 'Repeated averaging gives infinitely many; R explains A.'),
        ('13/40 has a terminating decimal expansion.', '40 = 2³ × 5.', 'a', 'A denominator with only 2s and 5s gives a terminating decimal.'),
        ('1/7 has a terminating decimal expansion.', 'Every rational number has a decimal expansion that either terminates or recurs.', 'd', '1/7 = 0.142857… recurs; A false, R true.'),
        ('0.999… (9 recurring) equals 1.', 'Every recurring decimal can be written as p/q.', 'b', 'Both true (x = 0.9̄ ⇒ 9x = 9); R does not explain why the value is exactly 1.'),
        ('There is a smallest positive rational number.', 'Rational numbers are dense.', 'd', 'Halving any positive rational gives a smaller one: A false, R true.'),
    ])(r)


def c3s2_case(r):
    who = name(r)
    d = r.choice([7, 11, 13])
    return Q((f'{who} is exploring the decimals of fractions with denominator {d} for a maths club poster. '
              f'(i) Find the decimal expansion of 1/{d}. (ii) Is it terminating? Why? (iii) What is the length of the repeating block? (iv) Use (i) to write 3/{d} without dividing again (if possible, by multiplying).'),
             {7: '(i) 0.142857142857… (ii) no, 7 is not of the form 2ᵐ5ⁿ (iii) 6 (iv) 3/7 = 0.428571…',
              11: '(i) 0.0909… (ii) no, 11 is not of the form 2ᵐ5ⁿ (iii) 2 (iv) 3/11 = 0.2727…',
              13: '(i) 0.076923076923… (ii) no, 13 is not of the form 2ᵐ5ⁿ (iii) 6 (iv) 3/13 = 0.230769…'}[d],
             '1 mark each part; (iv) 3 × the block (or long division) accepted.')


def c3s2_order_dec(r):
    a = r.randint(1, 8)
    b = r.randint(1, 8)
    x1 = Fr(a, 9)
    vals = [(f'0.{a}', Fr(a, 10)), (f'0.{a}{a}{a}… (recurring)', x1), (f'0.{a}{b}', Fr(10 * a + b, 100)), (f'{a}/{10 if a % 2 else 11}', Fr(a, 10 if a % 2 else 11))]
    s = sorted(vals, key=lambda t: t[1])
    return Q(f'Arrange in increasing order: {", ".join(v[0] for v in vals)}.', ', '.join(v[0] for v in s),
             'Compare decimal values digit by digit (write each to 4 places).')


# st3 irrational numbers

def c3s3_which(r):
    sq = r.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 121])
    nsq = r.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15])
    rats = [f'√{sq}', f'{r.randint(1, 9)}/{r.randint(2, 9)}', f'0.{r.randint(1, 9)}{r.randint(1, 9)}{r.randint(1, 9)}', f'√{sq}/{r.randint(2, 5)}', '1.2̅']
    return mcq('Which of the following is an irrational number?', f'√{nsq}', r.sample(rats, 3),
               f'{nsq} is not a perfect square, so √{nsq} is irrational; the others are ratios of integers.', r)


def c3s3_is_rational(r):
    n = r.randint(2, 200)
    ok = is_sq(n)
    return Q(f'Is √{n} rational or irrational?', 'Rational' if ok else 'Irrational',
             f'{n} {"= " + str(math.isqrt(n)) + "²" if ok else "is not a perfect square"}, so √{n} is {"rational" if ok else "irrational"}.',
             ['Irrational' if ok else 'Rational', 'Neither', 'Both'])


def c3s3_proof_steps(r):
    return xbank([
        ('In the proof that √2 is irrational, we assume √2 = p/q in lowest terms and get p² = 2q². What do we conclude about p, and why?', 'p is even.',
         'p² is even ⇒ p is even (if p were odd, p² would be odd) (2 marks).'),
        ('In the proof that √2 is irrational, after showing p and q are both even, why is that a contradiction?', 'We assumed p/q in lowest terms, so p and q have no common factor 2.',
         'Contradiction with "lowest terms" (2 marks).'),
        ('What kind of proof is used to show √2 is irrational, and what is assumed at the start?', 'Proof by contradiction; assume √2 = p/q with p, q co-prime integers, q ≠ 0.',
         'Method (1), assumption (1).'),
    ])(r)


def c3s3_ar_fixed(r):
    a, p = r.randint(1, 9), r.choice([2, 3, 5, 7])
    items = [
        (f'{a} + √{p} is irrational.', 'The sum of a rational number and an irrational number is irrational.', 'a', 'Both true; R explains A.'),
        ('π is irrational.', 'π = 22/7.', 'c', 'A is true; 22/7 is only an approximation of π, so R is false.'),
        (f'√{p * 4} is irrational.', f'√{p * 4} = 2√{p}, and a non-zero rational multiple of an irrational number is irrational.', 'a', 'R explains A.'),
        (f'√{p} × √{p} is rational.', 'The product of two irrational numbers is always irrational.', 'c', f'√{p} × √{p} = {p}, so A is true and R is false.'),
    ]
    return ar(*r.choice(items))


def c3s3_count(r):
    pool = [('√' + str(n), not is_sq(n)) for n in r.sample(range(2, 50), 4)] + [('π', True), ('3.14', False), ('22/7', False), ('0.1010010001…', True), ('1.5̅', False)]
    pick = r.sample(pool, 6)
    k = sum(1 for _, irr in pick if irr)
    return Q(f'How many of the following are irrational? {", ".join(s for s, _ in pick)}', str(k),
             'Irrational: ' + ', '.join(s for s, irr in pick if irr) + '. (Non-terminating non-recurring, or roots of non-squares.)',
             num_distractors(k, k + 1, k - 1, 6 - k))


def c3s3_between(r):
    a = r.randint(1, 6)
    b = a + 1
    return Q(f'Find one rational number and one irrational number between {a} and {b}.', f'e.g. rational {a}.5, irrational √{a * a + 1}',
             f'Rational: any terminating decimal such as {a}.5. Irrational: √n with {a * a} < n < {b * b} and n not a square, e.g. √{a * a + 1}, or {a}.101001000… (1 mark each).')


def c3s3_prove(r):
    a, b, p = r.randint(1, 9), r.randint(2, 7), r.choice([2, 3, 5])
    return Q(f'Given that √{p} is irrational, prove that {a} + {b}√{p} is irrational.', 'Proof by contradiction.',
             f'Suppose {a} + {b}√{p} = r, rational. Then √{p} = (r − {a})/{b}, which is rational (closure of ℚ), contradicting that √{p} is irrational. Hence {a} + {b}√{p} is irrational (3 marks: assumption 1, rearrangement 1, contradiction 1).')


def c3s3_product(r):
    p = r.choice([2, 3, 5, 6, 7])
    return Q(f'Give examples to show that the product of two irrational numbers can be rational and can also be irrational. Use √{p} in your examples.',
             f'√{p} × √{p} = {p} (rational); √{p} × √{p + 1 if not is_sq(p + 1) else p + 2} = √{p * (p + 1 if not is_sq(p + 1) else p + 2)} (irrational)',
             'One rational example (1), one irrational example with reason (2).')


def c3s3_pi(r):
    who = name(r)
    d = r.choice([7, 14, 21])
    return Q((f'{who} measures a circular plate: circumference ≈ {num(d * 3.1416, 1)} cm and diameter {d} cm, and says "π = C/d is a ratio, so π must be rational". '
              f'(i) Find C/d to 3 decimal places. (ii) Explain the error in {who}\'s reasoning. (iii) Why is 22/7 used in calculations? (iv) Is 22/7 more or less than π?'),
             '(i) ≈ 3.142 (ii) C and d cannot both be integers; measured values are approximations, and π is irrational (iii) a convenient rational approximation (iv) more (22/7 = 3.1428… > 3.14159…)',
             '1 mark each part.')


# st4 number line and spiral

def c3s4_between(r):
    n = r.choice([x for x in range(3, 150) if not is_sq(x)])
    lo = math.isqrt(n)
    return mcq(f'√{n} lies between …', f'{lo} and {lo + 1}', [f'{lo - 1} and {lo}', f'{lo + 1} and {lo + 2}', f'{lo + 2} and {lo + 3}'],
               f'{lo}² = {lo * lo} < {n} < {(lo + 1) ** 2} = {lo + 1}².', r)


def c3s4_spiral(r):
    k = r.choice([3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15])
    return Q(f'In the square root spiral, start with OP₁ = 1 unit and at each step draw a 1-unit segment perpendicular to the previous hypotenuse. What is the length of the hypotenuse OP' + sub(k) + '?',
             f'√{k}', f'OP₁ = 1, OP₂ = √2, …; each step adds 1 under the square root by the Baudhayana-Pythagoras theorem (OPₙ² = OPₙ₋₁² + 1), so OP' + sub(k) + f' = √{k}.',
             [f'√{k + 1}', f'{k}', f'√{k - 1}'])


def c3s4_construct(r):
    pairs = [(n, a, b) for a in range(1, 6) for b in range(a, 6) for n in [a * a + b * b] if not is_sq(n)]
    n, a, b = r.choice(pairs)
    return Q(f'Describe how to locate √{n} on the number line using a right triangle with whole-number legs.', f'Legs {a} and {b}: hypotenuse √({a}² + {b}²) = √{n}.',
             f'Mark OA = {a} on the number line, draw AB = {b} perpendicular at A; OB = √{n}; with centre O and radius OB, cut the number line (3 marks).')


def c3s4_explain(r):
    k = r.choice([2, 3, 5, 6, 7, 10, 11, 12])
    return Q(f'In the square root spiral, the hypotenuse after one step is √{k}. Explain why the next hypotenuse is √{k + 1}.', f'√{k + 1}',
             f'The new right triangle has legs √{k} and 1, so hypotenuse² = {k} + 1 = {k + 1} (2 marks).')


def c3s4_ar(r):
    n = r.choice([2, 3, 5, 6, 7, 10])
    return arbank([
        (f'√{n} can be located exactly on the number line.', 'Every real number corresponds to a unique point on the number line.', 'a', 'Both true; R explains A.'),
        ('Every point on the number line represents a rational number.', 'Rational numbers are dense on the number line.', 'd', 'Points such as √2 are irrational; A false, R true.'),
        (f'The hypotenuse of a right triangle with legs 1 and {n} is √{n * n + 1}.', 'By the Baudhayana-Pythagoras theorem, hypotenuse² = sum of squares of the legs.', 'a', 'R explains A.'),
    ])(r)


def c3s4_order(r):
    n = r.choice([x for x in range(5, 60) if not is_sq(x)])
    s = math.sqrt(n)
    a = round(s + r.choice([-0.3, 0.2, 0.4]), 1)
    f = Fr(round((s - 0.15) * 4), 4)
    vals = [(f'√{n}', s), (num(a), a), (fn(f), float(f))]
    o = sorted(vals, key=lambda t: t[1])
    if len({round(v[1], 6) for v in vals}) < 3:
        raise ValueError
    return Q(f'Arrange in ascending order: {", ".join(v[0] for v in vals)}.', ', '.join(v[0] for v in o), f'√{n} ≈ {num(s, 3)}; compare the decimals.',
             [', '.join(v[0] for v in reversed(o)), ', '.join(v[0] for v in [o[1], o[0], o[2]]), ', '.join(v[0] for v in [o[0], o[2], o[1]])])


def c3s4_semicircle(r):
    x = r.choice([3.5, 4.5, 5, 6, 7, 8.5, 9.3, 2.6])
    return Q((f'To locate √{num(x)} on the number line: mark AB = {num(x)} units and BC = 1 unit on a line, find the mid-point O of AC, draw a semicircle with centre O and radius OC, and draw a perpendicular at B meeting the semicircle at D. '
              f'Show that BD = √{num(x)}.'), f'BD = √{num(x)}',
             f'OD = OC = (x + 1)/2 and OB = (x + 1)/2 − 1 = (x − 1)/2. BD² = OD² − OB² = [(x + 1)² − (x − 1)²]/4 = x, so BD = √x with x = {num(x)} (4 marks).')


def c3s4_case(r):
    k = r.randint(4, 8)
    return Q((f'Students of Class 9 draw a square root spiral on chart paper (1 unit = 2 cm). '
              f'(i) Write the lengths of OP₁ to OP{k} in units. (ii) Which of these lengths are rational? (iii) What is the actual length of OP{k} in cm, to one decimal place? (iv) How many steps are needed until a hypotenuse of exactly 4 units appears?'),
             f'(i) √1, √2, …, √{k} (ii) √1 = 1 and √4 = 2{" and √9 = 3" if k >= 9 else ""} (iii) {num(2 * math.sqrt(k), 1)} cm (iv) 16 (OP₁₆ = 4)',
             '1 mark each part.')


# st5 surds

def c3s5_mult(r):
    a, b = r.sample([2, 3, 5, 6, 7, 8, 10, 12], 2)
    return mcq(f'√{a} × √{b} = …', rad(a * b), [f'√{a + b}', rad(a * b * 2), f'{a * b}'], f'√a × √b = √(ab) = √{a * b}' + ('' if rad(a * b) == f'√{a * b}' else f' = {rad(a * b)}') + '.', r)


def c3s5_simplify(r):
    k = r.randint(2, 9)
    m = r.choice([2, 3, 5, 6, 7])
    return Q(f'Simplify √{k * k * m}.', f'{k}√{m}', f'{k * k * m} = {k * k} × {m}, so √{k * k * m} = {k}√{m}.', [f'{m}√{k}', f'{k * k}√{m}', f'{k}√{m * 2}'])


def c3s5_explain(r):
    a, b = r.choice([(9, 16), (36, 64), (16, 9), (25, 144), (64, 36)])
    return Q(f'A student writes √{a} + √{b} = √{a + b}. Show by calculation that this is wrong, and state the correct rule.', f'√{a} + √{b} = {math.isqrt(a) + math.isqrt(b)} but √{a + b} = {math.sqrt(a + b):g}',
             '√(a + b) ≠ √a + √b in general; the true rule is √(ab) = √a √b (2 marks).', gap='G2')


def c3s5_ar(r):
    p = r.choice([2, 3, 5])
    a = r.choice([n for n in (2, 3, 5, 6, 7) if n != p and not is_sq(n * p)])
    return arbank([
        (f'1/√{p} = √{p}/{p}.', 'Multiplying numerator and denominator by the same non-zero number does not change the value.', 'a', 'R explains the rationalising step.'),
        (f'(√{a} + √{p})² = {a} + {p}.', '(x + y)² = x² + 2xy + y².', 'd', f'It equals {a + p} + 2√{a * p}; A false, R true.'),
        (f'√{a * a * p} = {a}√{p}.', '√(mn) = √m × √n for positive m and n.', 'a', 'R explains A.'),
    ])(r)


def c3s5_add(r):
    m = r.choice([2, 3, 5, 6, 7])
    a, b, c = r.sample(range(1, 7), 3)
    s = a - b + c
    return Q(f'Simplify √{a * a * m} − √{b * b * m} + √{c * c * m}.', rad(s * s * m) if s > 0 else ('−' + rad(s * s * m) if s else '0'),
             f'= {a}√{m} − {b}√{m} + {c}√{m} = {s}√{m}.', [f'√{a * a * m - b * b * m + c * c * m}', f'{a + b + c}√{m}', f'{s}√{3 * m}'])


def c3s5_rationalise(r):
    a = r.randint(1, 6)
    b = r.choice([n for n in [2, 3, 5, 6, 7, 10, 11] if n != a * a])
    den = a * a - b
    return Q(f'Rationalise the denominator of 1/({a} + √{b}).', f'({a} − √{b})/{den}' if den > 0 else f'(√{b} − {a})/{-den}',
             f'Multiply by ({a} − √{b})/({a} − √{b}): denominator {a}² − {b} = {den}.',
             [f'({a} + √{b})/{den}', f'({a} − √{b})/{a * a + b}', f'({a} − √{b})/{abs(den) + 1}'])


def c3s5_pq(r):
    a = r.randint(2, 5)
    b = r.choice([n for n in [2, 3, 5, 6, 7] if n != a * a and n < a * a])
    d = a * a - b
    # (a+√b)/(a−√b) = (a+√b)²/d = (a²+b + 2a√b)/d
    p, q = Fr(a * a + b, d), Fr(2 * a, d)
    return Q(f'If ({a} + √{b})/({a} − √{b}) = p + q√{b}, find the rational numbers p and q.', f'p = {fn(p)}, q = {fn(q)}',
             f'Multiply by ({a} + √{b})/({a} + √{b}): ({a * a + b} + {2 * a}√{b})/{d}; compare (4 marks).')


def c3s5_expo(r):
    base, root, pw = r.choice([(8, 3, 2), (27, 3, 2), (16, 4, 3), (32, 5, 2), (64, 3, 2), (125, 3, 2), (81, 4, 3), (64, 6, 5), (243, 5, 3), (49, 2, 3)])
    val = round(base ** (1 / root)) ** pw
    return Q(f'Evaluate {base}^({pw}/{root}).', str(val), f'{base}^(1/{root}) = {round(base ** (1 / root))}; raise to the power {pw}: {val}.',
             num_distractors(val, base * pw // root, round(base ** (1 / root)) * pw, val * 2))


def c3s5_square(r):
    a, b = r.randint(1, 7), r.choice([2, 3, 5, 6, 7])
    return Q(f'Expand and simplify ({a} + √{b})².', f'{a * a + b} + {2 * a}√{b}', f'a² + 2ab + b² with b = √{b}: {a * a} + {2 * a}√{b} + {b}.',
             [f'{a * a + b}', f'{a * a + b} + {a}√{b}', f'{a * a + b * b} + {2 * a}√{b}'])


def c3s5_x_inv(r):
    a = r.randint(2, 6)
    b = a * a - 1
    s = 2 * a
    return Q(f'If x = {a} + √{b}, find x + 1/x and x² + 1/x².', f'x + 1/x = {s}; x² + 1/x² = {s * s - 2}',
             f'1/x = {a} − √{b} because ({a} + √{b})({a} − √{b}) = {a * a} − {b} = 1; x + 1/x = {s}; x² + 1/x² = (x + 1/x)² − 2 = {s * s - 2} (5 marks).')


def c3s5_case(r):
    s = r.choice([2, 3, 5])
    k = r.randint(2, 6)
    return Q((f'A square tile has area {k * k * s} cm². (i) Find the side of the tile in simplest surd form. (ii) Find its perimeter. '
              f'(iii) Find the length of its diagonal. (iv) Is the perimeter rational or irrational? Explain.'),
             f'(i) {k}√{s} cm (ii) {4 * k}√{s} cm (iii) {k}√{2 * s} cm' + (f' = {2 * k} cm' if 2 * s == 4 else '') + ' (iv) irrational: a non-zero rational times an irrational',
             f'side = √{k * k * s}; diagonal = side × √2 (1 mark each).')


# ---------------- ch04 Algebraic identities ----------------

def c4s1_expand_mcq(r):
    a, b = r.randint(1, 6), r.randint(1, 9)
    sgn = r.choice([1, -1])
    correct = poly([a * a, 2 * a * b * sgn, b * b])
    return mcq(f'({term(a, "x", first=True)} {"+" if sgn > 0 else "−"} {b})² = …', correct,
               [poly([a * a, 0, b * b]), poly([a * a, a * b * sgn, b * b]), poly([a * a, 2 * a * b * sgn, -b * b])],
               f'(p ± q)² = p² ± 2pq + q² with p = {term(a, "x", first=True)}, q = {b}.', r)


def c4s1_which(r):
    return mcqbank([
        ('Which identity is shown by a square of side (a + b) cut into a square a², a square b² and two rectangles ab?', '(a + b)² = a² + 2ab + b²',
         ['(a − b)² = a² − 2ab + b²', '(a + b)(a − b) = a² − b²', '(a + b)² = a² + b²'], 'The four pieces add up to the large square.'),
        ('Which identity is used to compute 99 × 101 quickly?', '(a + b)(a − b) = a² − b²', ['(a + b)² = a² + 2ab + b²', '(a − b)² = a² − 2ab + b²', '(x + a)(x + b) = x² + (a + b)x + ab'], '99 × 101 = (100 − 1)(100 + 1).'),
        ('a² − b² factorises as …', '(a + b)(a − b)', ['(a − b)²', '(a + b)²', 'a(a − b) − b²'], 'Difference of two squares.'),
        ('(a − b)² − (a + b)² equals …', '−4ab', ['4ab', '−2b²', '0'], 'Expanding gives a² − 2ab + b² − a² − 2ab − b².'),
    ])(r)


def c4s1_explain(r):
    a, b = r.randint(5, 9), r.randint(1, 4)
    return Q(f'Using a square of side {a} cm from which a strip is removed, explain with a diagram (in words) why ({a} − {b})² = {a}² − 2 × {a} × {b} + {b}².', f'Both sides equal {(a - b) ** 2}.',
             f'Remove two strips {a} × {b} from {a}²; the corner {b} × {b} is removed twice, so add {b}² back. Check: {a * a} − {2 * a * b} + {b * b} = {(a - b) ** 2} (2 marks).')


def c4s1_ar(r):
    a, b = r.randint(2, 9), r.randint(1, 9)
    return arbank([
        (f'({a} + {b})² = {a}² + {b}².', '(x + y)² = x² + 2xy + y².', 'd', f'({a + b})² = {(a + b) ** 2} ≠ {a * a + b * b}; A false, R true.'),
        (f'{a + 10}² − {a}² = {10 * (2 * a + 10)}.', 'x² − y² = (x + y)(x − y).', 'a', f'({2 * a + 10})(10) = {10 * (2 * a + 10)}.'),
        ('(a − b)² = (b − a)².', 'A number and its negative have the same square.', 'a', 'b − a = −(a − b); R explains A.'),
    ])(r)


def c4s1_expand(r):
    a, b, c = r.randint(1, 7), r.randint(1, 7), r.randint(1, 9)
    if r.random() < 0.5:
        c_ = lambda k, v: f'{k if k != 1 else ""}{v}'
        return Q(f'Expand ({c_(a, "x")} + {c_(b, "y")})².', f'{c_(a * a, "x²")} + {2 * a * b}xy + {c_(b * b, "y²")}',
                 '(p + q)² = p² + 2pq + q².', [f'{c_(a * a, "x²")} + {c_(b * b, "y²")}', f'{c_(a * a, "x²")} + {c_(a * b, "xy")} + {c_(b * b, "y²")}', f'{c_(a * a, "x²")} − {2 * a * b}xy + {c_(b * b, "y²")}'])
    return Q(f'Expand ({a}x + {c})({a}x − {c}).', poly([a * a, 0, -c * c]), '(p + q)(p − q) = p² − q².', [poly([a * a, 0, c * c]), poly([a * a, -2 * a * c, -c * c]), poly([a, 0, -c])])


def c4s1_eval(r):
    n = r.choice([100, 200, 50, 1000])
    d = r.randint(1, 9)
    kind = r.randint(0, 2)
    if kind == 0:
        return Q(f'Use a suitable identity to evaluate {n + d}².', str((n + d) ** 2), f'({n} + {d})² = {n * n} + {2 * n * d} + {d * d} = {(n + d) ** 2}.', num_distractors((n + d) ** 2, n * n + d * d, n * n + n * d + d * d))
    if kind == 1:
        return Q(f'Use a suitable identity to evaluate {n - d}².', str((n - d) ** 2), f'({n} − {d})² = {n * n} − {2 * n * d} + {d * d} = {(n - d) ** 2}.', num_distractors((n - d) ** 2, n * n - d * d, n * n - 2 * n * d - d * d))
    return Q(f'Use a suitable identity to evaluate {n - d} × {n + d}.', str(n * n - d * d), f'({n} − {d})({n} + {d}) = {n}² − {d}² = {n * n - d * d}.', num_distractors(n * n - d * d, n * n + d * d, n * n - 2 * d))


def c4s1_sumsq(r):
    a, b = r.sample(range(-8, 10), 2)
    s, p = a + b, a * b
    k = r.choice(['a² + b²', '(a − b)²'])
    ans = a * a + b * b if k == 'a² + b²' else (a - b) ** 2
    return Q(f'If a + b = {fn(s)} and ab = {fn(p)}, find {k}.', fn(ans),
             f'a² + b² = (a + b)² − 2ab = {s * s} − {bracket(2 * p)} = {a * a + b * b}; (a − b)² = (a + b)² − 4ab = {(a - b) ** 2}.',
             num_distractors(ans, s * s + 2 * p, s * s - p, s * s))


def c4s1_border(r):
    who = name(r)
    x = r.randint(10, 40)
    w = r.randint(1, 4)
    return Q((f'{who} makes a square photo frame. The photo is x cm by x cm and the frame adds a border {w} cm wide all round. '
              f'Write the area of the border as a polynomial in x using an identity, and find it when x = {x}.'),
             f'({4 * w}x + {4 * w * w}) cm²; {4 * w * x + 4 * w * w} cm²',
             f'(x + {2 * w})² − x² = {4 * w}x + {4 * w * w} (3 marks); at x = {x}: {4 * w * x + 4 * w * w} (1 mark).')


# st2 (x+a)(x+b), (a+b+c)²

def c4s2_mcq(r):
    a, b = r.sample([n for n in range(-9, 10) if n], 2)
    return mcq(f'(x {signed(a)})(x {signed(b)}) = …', poly([1, a + b, a * b]),
               [poly([1, a * b, a + b]), poly([1, a - b, -a * b]) if a - b != a + b else poly([1, a + b + 1, a * b]), poly([1, a + b, -a * b])],
               '(x + a)(x + b) = x² + (a + b)x + ab.', r)


def c4s2_product(r):
    n = r.choice([100, 50, 10, 1000])
    a, b = r.sample(range(1, 10), 2)
    return Q(f'Use the identity (x + a)(x + b) = x² + (a + b)x + ab to find {n + a} × {n + b}.', str((n + a) * (n + b)),
             f'{n}² + ({a} + {b}) × {n} + {a * b} = {n * n} + {(a + b) * n} + {a * b} = {(n + a) * (n + b)}.', num_distractors((n + a) * (n + b), n * n + a * b, n * n + (a + b) * n))


def c4s2_abc(r):
    a, b, c = [nz(r, 1, 5) for _ in range(3)]
    co = f'{a * a}x² + {b * b}y² + {c * c}z² {signed(2 * a * b)}xy {signed(2 * b * c)}yz {signed(2 * a * c)}zx'
    co = co.replace(' 1x²', ' x²').replace('+ 1y²', '+ y²').replace('+ 1z²', '+ z²')
    if co.startswith('1x²'):
        co = co[1:]
    p = lambda k, v: term(k, v, first=True)
    return Q(f'Expand ({p(a, "x")} {"+" if b > 0 else "−"} {term(abs(b), "y", first=True)} {"+" if c > 0 else "−"} {term(abs(c), "z", first=True)})².', co,
             '(p + q + r)² = p² + q² + r² + 2pq + 2qr + 2rp; signs carried with each term.')


def c4s2_sq_sum(r):
    a, b, c = [r.randint(-6, 8) for _ in range(3)]
    s, q = a + b + c, a * b + b * c + c * a
    return Q(f'If a + b + c = {fn(s)} and ab + bc + ca = {fn(q)}, find a² + b² + c².', fn(a * a + b * b + c * c),
             f'(a + b + c)² = a² + b² + c² + 2(ab + bc + ca) ⇒ a² + b² + c² = {s * s} − {bracket(2 * q)} = {a * a + b * b + c * c}.',
             num_distractors(a * a + b * b + c * c, s * s - q, s * s + 2 * q, s * s))


def c4s2_explain(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    return Q(f'A rectangle has sides (x + {a}) and (x + {b}). Explain, by splitting it into four parts, why its area is x² + {a + b}x + {a * b}.', f'x² + {a + b}x + {a * b}',
             f'Parts: x × x, {a} × x, {b} × x, {a} × {b}; total x² + ({a} + {b})x + {a * b} (2 marks).')


def c4s2_ar(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    return arbank([
        (f'(x + {a})(x + {b}) = x² + {a + b}x + {a * b}.', '(x + a)(x + b) = x² + (a + b)x + ab.', 'a', 'R is the identity used.'),
        (f'(x − {a})(x − {b}) = x² − {a + b}x − {a * b}.', '(x + a)(x + b) = x² + (a + b)x + ab.', 'd', f'Product of −{a} and −{b} is +{a * b}; A false, R true.'),
        ('(a + b + c)² = a² + b² + c².', '(a + b + c)² contains the cross terms 2ab + 2bc + 2ca.', 'd', 'A false, R true.'),
    ])(r)


def c4s2_area(r):
    a, b = r.randint(1, 8), r.randint(1, 8)
    x = r.randint(5, 20)
    rate = r.choice([40, 50, 60])
    ex = (a + b) * x + a * b
    return Q((f'A rectangular garden in a housing society measures (x + {a}) m by (x + {b}) m. (i) Write its area as a polynomial. (ii) Find the area when x = {x}. '
              f'(iii) How much more area does it have than a square plot of side x m? (iv) If turf costs ₹{rate} per m², find the cost of turfing this extra area when x = {x}.'),
             f'(i) x² + {a + b}x + {a * b} (ii) {(x + a) * (x + b)} m² (iii) ({a + b}x + {a * b}) m² (iv) {inr(ex * rate)}',
             f'(iv) extra area = {ex} m² × ₹{rate} (1 mark each part).')


def c4s2_find(r):
    a, b = r.sample(range(1, 10), 2)
    return Q(f'If (x + {a})(x + k) = x² + {a + b}x + {a * b}, find k.', str(b), f'Compare: {a} + k = {a + b} and {a}k = {a * b} ⇒ k = {b}.', num_distractors(b, a + b, a * b, b + 1))


# st3 cube identities

def c4s3_mcq(r):
    a = r.randint(1, 5)
    sgn = r.choice([1, -1])
    c = poly([1, 3 * a * sgn, 3 * a * a, a ** 3 * sgn])
    return mcq(f'(x {"+" if sgn > 0 else "−"} {a})³ = …', c,
               [poly([1, 0, 0, a ** 3 * sgn]), poly([1, a * sgn, a * a, a ** 3 * sgn]), poly([1, 3 * a * sgn, -3 * a * a, a ** 3 * sgn])],
               '(x ± a)³ = x³ ± 3x²a + 3xa² ± a³.', r)


def c4s3_zero_sum(r):
    a, b = r.sample([n for n in range(-15, 16) if n], 2)
    c = -a - b
    if c == 0:
        c, b = 1, -a - 1
    return Q(f'Without calculating the cubes, find ({fn(a)})³ + ({fn(b)})³ + ({fn(c)})³.', fn(3 * a * b * c),
             f'{fn(a)} + {bracket(b)} + {bracket(c)} = 0, so a³ + b³ + c³ = 3abc = 3 × {bracket(a)} × {bracket(b)} × {bracket(c)} = {fn(3 * a * b * c)}.',
             num_distractors(3 * a * b * c, a * b * c, -3 * a * b * c, 0))


def c4s3_cube_num(r):
    n = r.choice([100, 10, 1000])
    d = r.randint(1, 4)
    s = r.choice([1, -1])
    v = (n + s * d) ** 3
    return Q(f'Use an identity to evaluate {n + s * d}³.', str(v), f'({n} {"+" if s > 0 else "−"} {d})³ = {n}³ {"+" if s > 0 else "−"} 3 × {n}² × {d} + 3 × {n} × {d}² {"+" if s > 0 else "−"} {d}³ = {v}.',
             num_distractors(v, n ** 3 + s * d ** 3, n ** 3 + s * 3 * n * n * d))


def c4s3_sum_cubes(r):
    a, b = r.sample(range(-6, 9), 2)
    s, p = a + b, a * b
    return Q(f'If x + y = {fn(s)} and xy = {fn(p)}, find x³ + y³.', fn(a ** 3 + b ** 3),
             f'x³ + y³ = (x + y)³ − 3xy(x + y) = {fn(s ** 3)} − 3 × {bracket(p)} × {bracket(s)} = {fn(a ** 3 + b ** 3)} (3 marks).', num_distractors(a ** 3 + b ** 3, s ** 3, s ** 3 + 3 * p * s))


def c4s3_explain(r):
    return xbank([
        ('Explain why, if a + b + c = 0, then a³ + b³ + c³ = 3abc.', 'Use a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca).', 'With a + b + c = 0 the right side is 0 (2 marks).'),
        ('Explain why (a + b)³ is not equal to a³ + b³, using a = b = 1.', '(1 + 1)³ = 8 but 1³ + 1³ = 2.', 'Counterexample (1); missing terms 3a²b + 3ab² (1).'),
        ('Show that (a − b)³ = −(b − a)³.', 'a − b = −(b − a) and (−t)³ = −t³.', '2 marks.'),
    ])(r)


def c4s3_ar(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    c = -(a + b)
    return arbank([
        (f'{a}³ + {b}³ + ({c})³ = {3 * a * b * c}.', 'If a + b + c = 0, then a³ + b³ + c³ = 3abc.', 'a', 'Sum is 0, so R gives A.'),
        ('(x + 1)³ = x³ + 1.', '(a + b)³ = a³ + b³ + 3ab(a + b).', 'd', 'The 3x(x + 1) term is missing; A false, R true.'),
        ('x³ − y³ = (x − y)(x² + xy + y²).', '(x − y)³ = x³ − y³ − 3xy(x − y).', 'b', 'Both true, but A follows from multiplying out, not from R.'),
    ])(r)


def c4s3_factor(r):
    a = r.randint(1, 5)
    k = r.choice([1, 2, 3])
    s = r.choice([1, -1])
    pre = '' if k == 1 else str(k)
    e = f'{k ** 3 if k > 1 else ""}x³ {"+" if s > 0 else "−"} {a ** 3}'
    ans = f'({pre}x {"+" if s > 0 else "−"} {a})({k * k if k > 1 else ""}x² {"−" if s > 0 else "+"} {k * a if k * a > 1 else ""}x + {a * a})'
    return Q(f'Factorise {e}.', ans, f'Use p³ {"+" if s > 0 else "−"} q³ = (p {"+" if s > 0 else "−"} q)(p² {"−" if s > 0 else "+"} pq + q²) with p = {pre}x, q = {a}.')


def c4s3_abc(r):
    a, b, c = r.sample(range(1, 8), 3)
    s = a + b + c
    q = a * a + b * b + c * c - a * b - b * c - c * a
    return Q(f'Find the value of a³ + b³ + c³ − 3abc when a = {a}, b = {b}, c = {c}, using the identity (a + b + c)(a² + b² + c² − ab − bc − ca).', str(s * q),
             f'a + b + c = {s}; a² + b² + c² − ab − bc − ca = {q}; product {s * q} (check: {a ** 3 + b ** 3 + c ** 3} − {3 * a * b * c}).')


def c4s3_case(r):
    x = r.randint(4, 12)
    a = r.randint(1, 3)
    return Q((f'A toy company makes cube-shaped boxes of edge (x + {a}) cm. (i) Write the volume as a polynomial in x. (ii) Find the volume when x = {x}. '
              f'(iii) How much greater is this than the volume of a cube of edge x cm? Give a polynomial. (iv) Check (iii) at x = {x}.'),
             f'(i) {poly([1, 3 * a, 3 * a * a, a ** 3])} (ii) {(x + a) ** 3} cm³ (iii) {poly([3 * a, 3 * a * a, a ** 3])} (iv) {(x + a) ** 3 - x ** 3} cm³',
             '(x + a)³ identity (1 each part).')


# st4 factorisation

def quad_fact(r):
    while True:
        p, q, s, t = r.randint(1, 3), nz(r, 1, 7), r.randint(1, 3), nz(r, 1, 7)
        if math.gcd(p, q) == 1 and math.gcd(s, t) == 1 and (p, q) != (s, t):
            return p, q, s, t


def fac_str(p, q):
    return f'({term(p, "x", first=True)} {signed(q)})'


def c4s4_split(r):
    p, q, s_, t = quad_fact(r)
    co = [p * s_, p * t + q * s_, q * t]
    if co[1] == 0:
        raise ValueError
    ans = fac_str(p, q) + fac_str(s_, t)
    wrong = []
    for (a1, b1, a2, b2) in [(p, -q, s_, -t), (p, t, s_, q), (p, -q, s_, t), (p, q, s_, -t), (s_, q, p, t)]:
        if sorted([(a1, b1), (a2, b2)]) != sorted([(p, q), (s_, t)]) and [a1 * a2, a1 * b2 + b1 * a2, b1 * b2] != co:
            w = fac_str(a1, b1) + fac_str(a2, b2)
            if w not in wrong:
                wrong.append(w)
    return Q(f'Factorise {poly(co)} by splitting the middle term.', ans,
             f'Product {co[0]} × {bracket(co[2])} = {fn(co[0] * co[2])}; split {term(co[1], "x", first=True)} as {term(p * t, "x", first=True)} and {term(q * s_, "x", first=True)}; group.',
             wrong[:3])


def c4s4_mcq(r):
    a, b = r.sample([n for n in range(-9, 10) if n], 2)
    return mcq(f'Which is a factor of {poly([1, a + b, a * b])}?', f'(x {signed(a)})', [f'(x {signed(-a)})', f'(x {signed(a * b)})', f'(x {signed(a + b)})'],
               f'{poly([1, a + b, a * b])} = (x {signed(a)})(x {signed(b)}).', r)


def c4s4_diff_sq(r):
    while True:
        a, b = r.randint(1, 9), r.randint(1, 9)
        if math.gcd(a, b) == 1:
            break
    k = r.choice([1, 2, 3, 5])
    A = lambda c, v: f'{c if c > 1 else ""}{v}'
    return Q(f'Factorise {A(k * a * a, "x²")} − {A(k * b * b, "y²")} completely.', f'{k if k > 1 else ""}({A(a, "x")} + {A(b, "y")})({A(a, "x")} − {A(b, "y")})',
             f'{"Take out the common factor " + str(k) + "; then " if k > 1 else ""}p² − q² = (p + q)(p − q) with p = {A(a, "x")}, q = {A(b, "y")}.',
             [f'{k if k > 1 else ""}({A(a, "x")} − {A(b, "y")})²', f'{k if k > 1 else ""}({A(a, "x")} + {A(b, "y")})²', f'({A(k * a, "x")} + {A(b, "y")})({A(a, "x")} − {A(b, "y")})'])


def c4s4_explain(r):
    p, q, s, t = quad_fact(r)
    co = [p * s, p * t + q * s, q * t]
    return Q(f'To factorise {poly(co)}, explain how you choose the two numbers to split the middle term.', f'Two numbers with product {fn(co[0] * co[2])} and sum {fn(co[1])}: {fn(p * t)} and {fn(q * s)}.',
             'Product = (coefficient of x²) × (constant), sum = middle coefficient (2 marks).')


def c4s4_ar(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    return arbank([
        (f'x² + {a + b}x + {a * b} = (x + {a})(x + {b}).', 'To factorise x² + px + q, find two numbers with sum p and product q.', 'a', 'R gives the method.'),
        ('x² + 4 = (x + 2)(x − 2).', 'a² − b² = (a + b)(a − b).', 'd', 'x² + 4 is a sum, not a difference, of squares; A false, R true.'),
        (f'x² − {a * a} = (x − {a})².', '(x − a)² = x² − 2ax + a².', 'd', f'x² − {a * a} = (x − {a})(x + {a}); A false, R true.'),
    ])(r)


def c4s4_group(r):
    a, b, c = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    return Q(f'Factorise x² + {a}x + {b}x + {a * b} and hence {poly([1, a + b, a * b])} using grouping; then factorise {c}x² + {c * (a + b)}x + {c * a * b}.',
             f'(x + {a})(x + {b}); {c}(x + {a})(x + {b})', 'Group x(x + a) + b(x + a) (2); take out the common factor c (1).')


def c4s4_area_fact(r):
    p, q, s, t = quad_fact(r)
    if q < 0 or t < 0:
        q, t = abs(q), abs(t)
    co = [p * s, p * t + q * s, q * t]
    x = r.randint(2, 9)
    return Q((f'The area of a rectangular plot is ({poly(co)}) m². (i) Factorise to find possible expressions for its length and breadth. '
              f'(ii) Find the actual dimensions when x = {x}. (iii) Find the perimeter as a polynomial.'),
             f'(i) {fac_str(p, q)} and {fac_str(s, t)} (ii) {p * x + q} m and {s * x + t} m (iii) ({lin(2 * (p + s), 2 * (q + t))}) m',
             '(i) splitting the middle term (2) (ii) substitution (1) (iii) 2(l + b) (1).')


# st5 mental computation

def c4s5_sq(r):
    n = r.choice([1000, 100, 500, 50])
    d = r.randint(1, 5)
    s = r.choice([-1, 1])
    v = (n + s * d) ** 2
    return Q(f'Find {n + s * d}² mentally using an identity.', str(v), f'({n} {"+" if s > 0 else "−"} {d})² = {n * n} {"+" if s > 0 else "−"} {2 * n * d} + {d * d} = {v}.',
             num_distractors(v, n * n + d * d, n * n + s * n * d, v - 2 * d * d))


def c4s5_diff(r):
    a = r.randint(30, 99)
    b = r.randint(10, a - 5)
    if (a + b) % 10 and (a - b) % 10:
        b = (b // 10) * 10 + (10 - a % 10) % 10 if (b // 10) * 10 + (10 - a % 10) % 10 < a else b
    return Q(f'Evaluate {a}² − {b}² using an identity.', str(a * a - b * b), f'({a} + {b})({a} − {b}) = {a + b} × {a - b} = {a * a - b * b}.',
             num_distractors(a * a - b * b, (a - b) ** 2, a * a + b * b))


def c4s5_mcq(r):
    n = r.choice([50, 100, 30, 70])
    d = r.randint(1, 6)
    return mcq(f'{n - d} × {n + d} = …', str(n * n - d * d), [str(n * n + d * d), str(n * n - 2 * d), str(n * n - d)], f'({n} − {d})({n} + {d}) = {n * n} − {d * d}.', r)


def c4s5_explain(r):
    a = r.randint(2, 9)
    return Q(f'Explain the trick: to square a number ending in 5, such as {a}5, multiply {a} by {a + 1} and write 25 after it.', f'{a}5² = {(10 * a + 5) ** 2}',
             f'(10a + 5)² = 100a² + 100a + 25 = 100a(a + 1) + 25 (2 marks).')


def c4s5_ar(r):
    n = r.randint(11, 49)
    return arbank([
        (f'{n}² − {n - 1}² = {2 * n - 1}.', 'a² − b² = (a + b)(a − b).', 'a', f'({2 * n - 1})(1).'),
        (f'{n + 1} × {n - 1} = {n}² − 1.', '(a + b)(a − b) = a² − b².', 'a', 'Direct use of R.'),
        (f'{n}² = {(n // 10) ** 2 * 100 + (n % 10) ** 2}.', '(a + b)² = a² + 2ab + b².', 'd', f'{n}² = {n * n}; the cross term 2 × {n // 10 * 10} × {n % 10} is missing, so A is false; R is true.'),
    ])(r)


def c4s5_simplify(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return Q(f'Simplify (x + {a})² − (x − {a})² and use it to evaluate {100 + a}² − {100 - a}².', f'{4 * a}x; {400 * a}',
             f'(x + a)² − (x − a)² = 4ax = {4 * a}x; at x = 100: {400 * a} (3 marks).')


def c4s5_case(r):
    who = name(r)
    n = r.choice([102, 98, 104, 96, 103, 97])
    return Q((f'{who} runs a stationery shop and sells {n} pens at ₹{n} each. (i) Use an identity to find the total amount. '
              f'(ii) Next day {who} sells {n - 2} pens at ₹{n + 2} each. Find the amount using (a − b)(a + b). (iii) Which day gave more money, and by how much?'),
             f'(i) {inr(n * n)} (ii) {inr((n - 2) * (n + 2))} (iii) first day, by ₹4', f'(i) ({n} as 100 ± {abs(n - 100)})² (ii) {n}² − 4 (iii) difference 2² = 4.')


# ---------------- ch05 Circles ----------------

def c5s1_parts(r):
    return mcqbank([
        ('The longest chord of a circle is …', 'a diameter', ['a radius', 'an arc', 'a tangent'], 'A diameter passes through the centre.'),
        ('The region between a chord and its arc is called …', 'a segment', ['a sector', 'a radius', 'a semicircle always'], 'Segment: bounded by a chord and an arc.'),
        ('The region between two radii and the arc between them is called …', 'a sector', ['a segment', 'a chord', 'a secant'], 'Sector: bounded by two radii and an arc.'),
        ('A line segment joining two points on a circle is called …', 'a chord', ['a radius', 'a sector', 'an arc'], 'Definition of a chord.'),
        ('If the arc AB is smaller than a semicircle, it is called …', 'a minor arc', ['a major arc', 'a segment', 'a diameter'], 'Arcs less than a semicircle are minor.'),
        ('Circles with the same centre and different radii are called …', 'concentric circles', ['congruent circles', 'equal circles', 'intersecting circles'], 'Same centre.'),
    ])(r)


def c5s1_diam(r):
    rr = r.choice([3.5, 4, 5.5, 6, 7, 8.5, 9, 10.5, 12])
    return Q(f'The radius of a circle is {num(rr)} cm. What is the length of its longest chord?', f'{num(2 * rr)} cm', 'The longest chord is the diameter = 2r.',
             [f'{num(rr)} cm', f'{num(rr / 2)} cm', f'{num(4 * rr)} cm'])


def c5s1_explain(r):
    return xbank([
        ('Explain why a diameter is the longest chord of a circle.', 'Any chord AB satisfies AB ≤ OA + OB = 2r, with equality only when O lies on AB.', 'Triangle inequality (2 marks).'),
        ('Explain the difference between a sector and a segment of a circle.', 'A sector is bounded by two radii and an arc; a segment by a chord and an arc.', '1 mark each.'),
        ('How many circles can pass through one given point? Through two given points? Explain briefly.', 'Infinitely many through one point; infinitely many through two points.', 'Centres lie anywhere / on the perpendicular bisector (2 marks).'),
        ('Explain why a semicircle is both a major and a minor arc in neither sense.', 'It is exactly half the circle, so it is neither major nor minor.', 'Definition based on comparison with a semicircle (2 marks).'),
    ])(r)


def c5s1_ar(r):
    return arbank([
        ('A diameter of a circle is a chord.', 'A chord joins any two points on the circle.', 'a', 'A diameter joins two points on the circle through the centre.'),
        ('A radius of a circle is a chord.', 'A chord joins any two points on a circle.', 'd', 'A radius has one end at the centre, not on the circle; A false, R true.'),
        ('Two circles of radius 5 cm are congruent.', 'Circles with equal radii are congruent.', 'a', 'R explains A.'),
        ('A segment and a sector of a circle are the same region.', 'A sector is bounded by two radii and an arc.', 'd', 'A segment is bounded by a chord and an arc; A false, R true.'),
    ])(r)


def c5s1_count(r):
    n = r.randint(3, 9)
    return Q(f'{n} points are marked on a circle. How many chords can be drawn joining them in pairs?', str(n * (n - 1) // 2), f'Each pair gives one chord: {n} × {n - 1} ÷ 2 = {n * (n - 1) // 2}.',
             num_distractors(n * (n - 1) // 2, n * (n - 1), n, n - 1))


def c5s1_case(r):
    rr = r.choice([14, 21, 28, 35])
    return Q((f'A circular rangoli of radius {rr} cm is made at the entrance of a school. A straight line of flowers AB passes through the centre O, and another line of flowers CD does not pass through O. '
              f'(i) Name AB and CD. (ii) What is the length of AB? (iii) Can CD be longer than AB? Why? (iv) The part of the rangoli between CD and the smaller arc CD is coloured red. What is this region called?'),
             f'(i) AB diameter, CD chord (ii) {2 * rr} cm (iii) No; the diameter is the longest chord (iv) minor segment',
             '1 mark each part.')


def c5s1_angle(r):
    th = r.choice([60, 72, 90, 120, 135, 150])
    return Q(f'An arc of a circle subtends {th}° at the centre. What fraction of the circumference is the arc, and is it a minor or major arc?', f'{frac(th, 360)}; minor arc',
             f'Fraction = {th}/360 = {frac(th, 360)}; less than half ⇒ minor.', [f'{frac(th, 180)}; minor arc', f'{frac(th, 360)}; major arc', f'{frac(360 - th, 360)}; minor arc'])


# st2 chords

def chord_triple(r):
    a, b, c = triple(r)
    k = r.choice([1, 1, 2])
    return a * k, b * k, c * k   # half chord a, distance b, radius c


def c5s2_chord_len(r):
    h, d, R = chord_triple(r)
    return Q(f'A chord of a circle of radius {R} cm is at a distance of {d} cm from the centre. Find the length of the chord.', f'{2 * h} cm',
             f'The perpendicular from the centre bisects the chord: half-chord = √({R}² − {d}²) = {h}; chord = {2 * h}.', [f'{h} cm', f'{2 * R} cm', f'{R + d} cm'])


def c5s2_dist(r):
    h, d, R = chord_triple(r)
    return Q(f'A chord of length {2 * h} cm is drawn in a circle of radius {R} cm. Find the distance of the chord from the centre.', f'{d} cm',
             f'd = √({R}² − {h}²) = √{R * R - h * h} = {d}.', [f'{2 * d} cm', f'{R - h} cm', f'{h} cm'])


def c5s2_radius(r):
    h, d, R = chord_triple(r)
    return Q(f'A chord of length {2 * h} cm is at a distance of {d} cm from the centre of a circle. Find the radius.', f'{R} cm',
             f'r = √({h}² + {d}²) = {R}.', [f'{h + d} cm', f'{2 * R} cm', f'{round(math.sqrt(4 * h * h + d * d), 1)} cm'])


def c5s2_mcq(r):
    return mcqbank([
        ('The perpendicular from the centre of a circle to a chord …', 'bisects the chord', ['is equal to the chord', 'is always equal to the radius', 'passes through an end of the chord'], 'Theorem: the perpendicular from the centre bisects the chord.'),
        ('Equal chords of a circle are …', 'equidistant from the centre', ['parallel', 'perpendicular to each other', 'always diameters'], 'Equal chords are equidistant from the centre.'),
        ('The line joining the centre of a circle to the mid-point of a chord is …', 'perpendicular to the chord', ['parallel to the chord', 'equal to the diameter', 'a tangent'], 'Converse of the perpendicular-bisector theorem.'),
        ('Of two chords of a circle, the one nearer the centre is …', 'longer', ['shorter', 'equal', 'a radius'], 'Half-chord = √(r² − d²) grows as d decreases.'),
    ])(r)


def c5s2_explain(r):
    h, d, R = chord_triple(r)
    return Q(f'In a circle with centre O, OM ⟂ AB where AB is a chord. Explain why AM = MB, and hence find AB if OA = {R} cm and OM = {d} cm.', f'AB = {2 * h} cm',
             f'△OMA ≅ △OMB (RHS: OA = OB, OM common, ∠M = 90°) ⇒ AM = MB (1); AM = √({R * R} − {d * d}) = {h} (1).')


def c5s2_ar(r):
    h, d, R = chord_triple(r)
    return arbank([
        (f'A chord of length {2 * h} cm in a circle of radius {R} cm is {d} cm from the centre.', 'The perpendicular from the centre to a chord bisects it.', 'a', 'Using R, d = √(R² − h²).'),
        ('Two chords of a circle that are equidistant from the centre are equal.', 'Equal chords of a circle subtend equal angles at the centre.', 'b', 'Both true, but A follows from the distance theorem, not from R.'),
        ('The perpendicular bisector of any chord passes through the centre.', 'The centre is equidistant from the ends of every chord.', 'a', 'Points equidistant from A and B lie on the perpendicular bisector of AB.'),
    ])(r)


def c5s2_parallel(r):
    R = r.choice([5, 10, 13, 17, 25])
    opts = [(a, b) for (a, b, c) in [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (15, 20, 25), (12, 16, 20)] if c == R]
    if R == 25:
        opts = [(7, 24), (15, 20)]
    if R == 10:
        opts = [(6, 8)]
    if R == 5:
        opts = [(3, 4)]
    (h1, d1) = opts[0]
    h2, d2 = d1, h1
    side = r.choice(['same', 'opposite'])
    dist = abs(d1 - d2) if side == 'same' else d1 + d2
    if dist == 0:
        raise ValueError
    return Q(f'Two parallel chords of lengths {2 * h1} cm and {2 * h2} cm are drawn in a circle of radius {R} cm, on {"the same side" if side == "same" else "opposite sides"} of the centre. Find the distance between them.', f'{dist} cm',
             f'Distances from centre: √({R}² − {h1}²) = {d1} and √({R}² − {h2}²) = {d2}; {"difference" if side == "same" else "sum"} = {dist} (4 marks).')


def c5s2_case(r):
    h, d, R = chord_triple(r)
    s = r.choice([10, 20, 50])
    return Q((f'A circular park has radius {R * s} m. A straight path AB of length {2 * h * s} m is laid as a chord. A fountain is at the centre O. '
              f'(i) Find the shortest distance from the fountain to the path. (ii) Where on the path is the point nearest to the fountain? (iii) Another path of the same length is laid elsewhere. How far is it from O? Why? '
              f'(iv) If a third path is {(d - 1) * s if d > 1 else d * s // 2} m from O, is it longer or shorter than AB?'),
             f'(i) {d * s} m (ii) at the mid-point of AB (iii) {d * s} m; equal chords are equidistant from the centre (iv) longer',
             '1 mark each part.')


# st3 angles in a circle

def c5s3_centre(r):
    x = r.randint(20, 85)
    if r.random() < 0.5:
        return Q(f'An arc subtends an angle of {x}° at a point on the remaining part of the circle. What angle does it subtend at the centre?', f'{2 * x}°',
                 'The angle at the centre is double the angle at any point on the remaining part of the circle.', [f'{x}°', f'{180 - x}°', f'{x // 2}°' if x % 2 == 0 else f'{x + 90}°'])
    y = 2 * x
    return Q(f'The angle subtended by an arc at the centre is {y}°. Find the angle subtended by it at any point on the remaining part of the circle.', f'{x}°',
             'Angle at circumference = half the angle at the centre.', [f'{y}°', f'{180 - y}°' if y < 180 else f'{360 - y}°', f'{2 * y}°' if 2 * y < 360 else f'{x + 10}°'])


def c5s3_mcq(r):
    return mcqbank([
        ('The angle in a semicircle is …', 'a right angle', ['an acute angle', 'an obtuse angle', '180°'], 'The angle at the centre is 180°, so the angle at the circumference is 90°.'),
        ('Angles in the same segment of a circle are …', 'equal', ['supplementary', 'complementary', 'always 90°'], 'Each is half the angle at the centre.'),
        ('If an arc subtends 100° at the centre, the angle it subtends at a point on the major arc is …', '50°', ['100°', '200°', '130°'], 'Half of 100°.'),
        ('Equal chords of a circle subtend … at the centre.', 'equal angles', ['supplementary angles', 'right angles', 'unequal angles'], 'Theorem on equal chords.'),
    ])(r)


def c5s3_same_seg(r):
    a = r.randint(25, 70)
    return Q(f'A, B, C, D lie on a circle and AB is a chord. If ∠ACB = {a}°, find ∠ADB, where C and D are on the same side of AB.', f'{a}°', 'Angles in the same segment are equal.',
             [f'{180 - a}°', f'{2 * a}°', f'{90 - a}°'])


def c5s3_semicircle(r):
    a = r.randint(20, 70)
    return Q(f'AB is a diameter of a circle and C is a point on the circle. If ∠CAB = {a}°, find ∠CBA.', f'{90 - a}°',
             f'∠ACB = 90° (angle in a semicircle), so ∠CBA = 180° − 90° − {a}° = {90 - a}°.', [f'{a}°', f'{180 - a}°', f'{2 * a}°' if 2 * a != 90 - a else f'{a + 10}°'])


def c5s3_isos(r):
    x = r.randint(25, 75)
    c = 180 - 2 * x
    return Q(f'O is the centre of a circle and A, B, C lie on it. If ∠OAB = {x}°, find ∠AOB and the angle ∠ACB, where C is on the major arc.', f'∠AOB = {c}°, ∠ACB = {c // 2 if c % 2 == 0 else num(c / 2)}°',
             f'OA = OB ⇒ ∠OBA = {x}°; ∠AOB = 180° − {2 * x}° = {c}°; ∠ACB = half of it (3 marks).')


def c5s3_explain(r):
    return xbank([
        ('Explain why the angle in a semicircle is 90°.', 'The diameter subtends 180° at the centre; the angle at the circumference is half, i.e. 90°.', 'Use of the centre-angle theorem (2 marks).'),
        ('Explain why angles in the same segment of a circle are equal.', 'Each equals half of the angle subtended by the same arc at the centre.', '2 marks.'),
        ('A, B, P, Q lie on a circle with P, Q on opposite sides of AB. Are ∠APB and ∠AQB equal? Explain.', 'Not in general; they are supplementary (ABPQ… is cyclic).', 'Opposite segments give angles adding to 180° (2 marks).'),
    ])(r)


def c5s3_ar(r):
    x = r.randint(20, 80)
    return arbank([
        (f'If ∠AOB = {2 * x}° at the centre, then ∠ACB = {x}° for C on the major arc.', 'The angle subtended by an arc at the centre is double the angle subtended at any point on the remaining part of the circle.', 'a', 'R explains A.'),
        ('The angle in a semicircle is 90°.', 'A diameter subtends a straight angle at the centre.', 'a', 'Half of 180° is 90°.'),
        (f'∠ACB = {x}° and ∠ADB = {x + 10}° can both be angles in the same segment on chord AB.', 'Angles in the same segment are equal.', 'd', 'They must be equal; A false, R true.'),
    ])(r)


def c5s3_find(r):
    a, b = r.randint(20, 60), r.randint(20, 60)
    return Q(f'In a circle with centre O, AB is a diameter and C, D are points on the circle on opposite sides of AB. If ∠BAC = {a}° and ∠ABD = {b}°, find ∠ABC, ∠BAD and ∠ACB + ∠ADB.', f'∠ABC = {90 - a}°, ∠BAD = {90 - b}°, sum = 180°',
             'Angles in a semicircle ∠ACB = ∠ADB = 90° (2); angle sums in triangles (2).')


def c5s3_case(r):
    x = r.randint(25, 60)
    return Q((f'In a stadium shaped like a circle, a camera at the centre O sees the goal-posts A and B at an angle ∠AOB = {2 * x}°. '
              f'Players P and Q stand on the boundary on the major arc. (i) Find ∠APB. (ii) Is ∠AQB the same as ∠APB? Why? (iii) If a player R stands on the minor arc AB, find ∠ARB. (iv) Where should a player stand so that the goal subtends 90°?'),
             f'(i) {x}° (ii) yes; same segment (iii) {180 - x}° (iv) only if AB were a diameter; with ∠AOB = {2 * x}° no point on the circle sees AB at 90°',
             '1 mark each; (iii) uses the cyclic quadrilateral APBR.')


# st4 cyclic quadrilaterals

def c5s4_opp(r):
    a = r.randint(55, 130)
    return Q(f'ABCD is a cyclic quadrilateral with ∠A = {a}°. Find ∠C.', f'{180 - a}°', 'Opposite angles of a cyclic quadrilateral are supplementary.', [f'{a}°', f'{360 - a}°', f'{90 - a if a < 90 else a - 90}°'])


def c5s4_mcq(r):
    return mcqbank([
        ('The sum of either pair of opposite angles of a cyclic quadrilateral is …', '180°', ['90°', '360°', '270°'], 'Theorem.'),
        ('An exterior angle of a cyclic quadrilateral is equal to …', 'the interior opposite angle', ['the adjacent interior angle', '90°', 'twice the opposite angle'], 'Follows from opposite angles being supplementary.'),
        ('Which of these quadrilaterals is always cyclic?', 'a rectangle', ['a rhombus', 'a parallelogram', 'a kite'], 'Opposite angles 90° + 90°.'),
        ('A parallelogram that is cyclic must be a …', 'rectangle', ['rhombus', 'trapezium', 'kite'], 'Opposite angles equal and supplementary ⇒ 90° each.'),
    ])(r)


def c5s4_expr(r):
    x = r.randint(10, 30)
    a, b = r.randint(2, 4), r.randint(1, 3)
    c = 180 - (a + b) * x
    if c <= 0:
        raise ValueError
    # ∠A = a x + c1, ∠C = b x + c2 sum 180
    c1 = r.randint(5, 20)
    c2 = 180 - (a + b) * x - c1
    if c2 <= -60:
        raise ValueError
    return Q(f'In cyclic quadrilateral PQRS, ∠P = ({a}x {signed(c1)})° and ∠R = ({b}x {signed(c2)})°. Find x and ∠P.', f'x = {x}, ∠P = {a * x + c1}°',
             f'{a}x {signed(c1)} + {b}x {signed(c2)} = 180 ⇒ {a + b}x = {180 - c1 - c2} ⇒ x = {x}.')


def c5s4_ext(r):
    a = r.randint(60, 130)
    return Q(f'Side AB of cyclic quadrilateral ABCD is produced to E. If ∠CBE = {180 - a}°... find ∠ADC.'.replace('... ', ', '), f'{180 - a}°',
             f'∠ABC = {a}°; ∠ADC = 180° − {a}° = {180 - a}° (exterior angle = interior opposite angle).', [f'{a}°', f'{90 - (180 - a) // 2}°', f'{360 - a}°'])


def c5s4_explain(r):
    return xbank([
        ('Explain why a rhombus that is not a square cannot be cyclic.', 'Its opposite angles are equal but not 90°, so they cannot add to 180°.', '2 marks.'),
        ('Explain why every rectangle is a cyclic quadrilateral.', 'Each pair of opposite angles is 90° + 90° = 180°.', 'Converse of the cyclic-quadrilateral theorem (2 marks).'),
        ('Explain why an isosceles trapezium is cyclic.', 'Its base angles are equal and co-interior angles are supplementary, so opposite angles add to 180°.', '2 marks.'),
    ])(r)


def c5s4_ar(r):
    a = r.randint(60, 120)
    return arbank([
        (f'In cyclic quadrilateral ABCD, if ∠B = {a}°, then ∠D = {180 - a}°.', 'Opposite angles of a cyclic quadrilateral are supplementary.', 'a', 'R explains A.'),
        ('Every parallelogram is cyclic.', 'Opposite angles of a parallelogram are equal.', 'd', 'Only rectangles are cyclic; A false, R true.'),
        ('A square is a cyclic quadrilateral.', 'All the sides of a square are equal.', 'b', 'Both true; A follows from 90° + 90°, not from equal sides.'),
    ])(r)


def c5s4_find(r):
    a, b = r.randint(30, 60), r.randint(30, 60)
    return Q(f'ABCD is a cyclic quadrilateral whose diagonals meet at E. If ∠DBC = {a}° and ∠BAC = {b}°, find ∠BCD.', f'{180 - a - b}°',
             f'∠CAD = ∠CBD = {a}° (same segment); ∠BAD = {a + b}°; ∠BCD = 180° − {a + b}° = {180 - a - b}° (4 marks).')


def c5s4_case(r):
    a, b = r.randint(70, 110), r.randint(65, 115)
    return Q((f'Four lamp-posts P, Q, R, S stand on the edge of a circular garden, in that order. The angle at P between the paths to S and Q is {a}°, and the angle at Q between the paths to P and R is {b}°. '
              f'(i) Find ∠R. (ii) Find ∠S. (iii) Check the angle sum of PQRS. (iv) If the path PQ is extended beyond Q to T, find ∠RQT.'),
             f'(i) {180 - a}° (ii) {180 - b}° (iii) 360° (iv) {180 - b}°', '1 mark each part.')


FAMILIES = {
    S + '01-st1': [F('C1', 'D2', 'mcq', c1s1_quadrant), F('C1', 'D1', 'short', c1s1_axis), F('C1', 'D1', 'short', c1s1_abscissa), F('C2', 'D2', 'explain', c1s1_sign_explain),
                   F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c1s1_reflect), F('C3', 'D2', 'short', c1s1_dist_axes), F('C3', 'D3', 'numerical', c1s1_on_axis_k),
                   F('C4', 'D3', 'case', c1s1_case)],
    S + '01-st2': [F('C1', 'D2', 'mcq', c1s2_formula), F('C1', 'D1', 'short', c1s2_same_line), F('C2', 'D2', 'short', c1s2_origin), F('C2', 'D3', 'explain', c1s2_explain),
                   F('C2', 'D2', 'mcq', c1s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c1s2_dist), F('C3', 'D3', 'numerical', c1s2_dist_surd), F('C3', 'D4', 'multi_step', c1s2_find_k),
                   F('C4', 'D3', 'multi_step', c1s2_right_tri), F('C4', 'D4', 'case', c1s2_case), F('C4', 'D5', 'multi_step', c1s2_equidistant)],
    S + '01-st3': [F('C1', 'D2', 'mcq', c1s3_formula), F('C1', 'D1', 'short', c1s3_mid), F('C2', 'D2', 'explain', c1s3_explain), F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c1s3_mid_frac), F('C3', 'D3', 'numerical', c1s3_other_end), F('C4', 'D3', 'multi_step', c1s3_parallelogram), F('C4', 'D4', 'multi_step', c1s3_diameter),
                   F('C4', 'D3', 'case', c1s3_case)],
    S + '01-st4': [F('C1', 'D2', 'mcq', c1s4_fourth), F('C1', 'D1', 'short', c1s4_move), F('C2', 'D2', 'explain', c1s4_explain), F('C2', 'D2', 'mcq', c1s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c1s4_rect_area), F('C3', 'D3', 'numerical', c1s4_tri_area), F('C4', 'D3', 'case', c1s4_case), F('C4', 'D4', 'long', c1s4_kite)],
    S + '02-st1': [F('C1', 'D2', 'mcq', c2s1_coeff), F('C1', 'D2', 'mcq', c2s1_ispoly), F('C1', 'D1', 'short', c2s1_terms), F('C2', 'D2', 'explain', c2s1_explain),
                   F('C2', 'D3', 'mcq', c2s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c2s1_simplify), F('C3', 'D1', 'short', c2s1_degree), F('C3', 'D3', 'numerical', c2s1_perimeter),
                   F('C4', 'D3', 'case', c2s1_context)],
    S + '02-st2': [F('C1', 'D2', 'mcq', c2s2_zero), F('C1', 'D1', 'short', c2s2_value), F('C2', 'D2', 'explain', c2s2_check), F('C2', 'D3', 'explain', c2s2_explain),
                   F('C2', 'D2', 'mcq', c2s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c2s2_find_a), F('C3', 'D3', 'multi_step', c2s2_two_cond), F('C3', 'D4', 'case', c2s2_taxi),
                   F('C4', 'D3', 'multi_step', c2s2_breakeven), F('C4', 'D4', 'multi_step', c2s2_breakeven, gap='G7')],
    S + '02-st3': [F('C1', 'D2', 'mcq', c2s3_rule_mcq), F('C1', 'D1', 'short', c2s3_next), F('C2', 'D2', 'explain', c2s3_explain), F('C2', 'D3', 'mcq', c2s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c2s3_find_rule), F('C3', 'D3', 'numerical', c2s3_matchstick), F('C4', 'D3', 'multi_step', c2s3_which_step, gap='G7'), F('C4', 'D4', 'case', c2s3_plans, gap='G7')],
    S + '02-st4': [F('C1', 'D2', 'mcq', c2s4_intercept), F('C1', 'D1', 'short', c2s4_rate), F('C2', 'D2', 'explain', c2s4_explain), F('C2', 'D3', 'mcq', c2s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c2s4_onpoint), F('C3', 'D3', 'numerical', c2s4_two_pts), F('C3', 'D4', 'multi_step', c2s4_triangle), F('C4', 'D3', 'case', c2s4_tank),
                   F('C4', 'D4', 'long', c2s4_meet, gap='G7')],
    S + '03-st1': [F('C1', 'D2', 'mcq', c3s1_classify), F('C1', 'D1', 'short', c3s1_pq), F('C2', 'D2', 'explain', c3s1_explain), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c3s1_order), F('C3', 'D3', 'numerical', c3s1_sum), F('C3', 'D1', 'short', c3s1_between_ints), F('C4', 'D3', 'case', c3s1_closure_case)],
    S + '03-st2': [F('C1', 'D2', 'mcq', c3s2_terminating), F('C1', 'D1', 'short', c3s2_decimal), F('C2', 'D2', 'explain', c3s2_explain), F('C2', 'D2', 'mcq', c3s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s2_rec), F('C3', 'D3', 'numerical', c3s2_between), F('C3', 'D4', 'multi_step', c3s2_mixed), F('C4', 'D3', 'case', c3s2_case),
                   F('C3', 'D3', 'short', c3s2_order_dec)],
    S + '03-st3': [F('C1', 'D2', 'mcq', c3s3_which), F('C1', 'D1', 'short', c3s3_is_rational), F('C2', 'D2', 'explain', c3s3_proof_steps), F('C2', 'D3', 'mcq', c3s3_ar_fixed, kinds=('ar',)),
                   F('C3', 'D2', 'short', c3s3_count), F('C3', 'D3', 'explain', c3s3_between), F('C3', 'D4', 'multi_step', c3s3_prove), F('C4', 'D3', 'explain', c3s3_product),
                   F('C4', 'D4', 'case', c3s3_pi)],
    S + '03-st4': [F('C1', 'D2', 'mcq', c3s4_between), F('C1', 'D1', 'short', c3s4_spiral), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c3s4_order), F('C3', 'D3', 'explain', c3s4_construct), F('C4', 'D4', 'long', c3s4_semicircle), F('C4', 'D3', 'case', c3s4_case)],
    S + '03-st5': [F('C1', 'D2', 'mcq', c3s5_mult), F('C1', 'D1', 'short', c3s5_simplify), F('C2', 'D2', 'explain', c3s5_explain), F('C2', 'D3', 'mcq', c3s5_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c3s5_add), F('C3', 'D3', 'numerical', c3s5_rationalise), F('C3', 'D2', 'short', c3s5_square), F('C3', 'D4', 'multi_step', c3s5_pq),
                   F('C4', 'D3', 'numerical', c3s5_expo), F('C4', 'D5', 'long', c3s5_x_inv), F('C4', 'D4', 'case', c3s5_case)],
    S + '04-st1': [F('C1', 'D2', 'mcq', c4s1_expand_mcq), F('C1', 'D1', 'mcq', c4s1_which), F('C2', 'D2', 'explain', c4s1_explain), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c4s1_expand), F('C3', 'D3', 'numerical', c4s1_eval), F('C4', 'D3', 'numerical', c4s1_sumsq), F('C4', 'D4', 'multi_step', c4s1_border, gap='G7')],
    S + '04-st2': [F('C1', 'D2', 'mcq', c4s2_mcq), F('C1', 'D1', 'short', c4s2_find), F('C2', 'D2', 'explain', c4s2_explain), F('C2', 'D2', 'mcq', c4s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c4s2_product), F('C3', 'D3', 'numerical', c4s2_abc), F('C4', 'D3', 'numerical', c4s2_sq_sum), F('C4', 'D4', 'case', c4s2_area)],
    S + '04-st3': [F('C1', 'D2', 'mcq', c4s3_mcq), F('C2', 'D2', 'explain', c4s3_explain), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c4s3_cube_num),
                   F('C3', 'D2', 'numerical', c4s3_zero_sum), F('C3', 'D3', 'numerical', c4s3_factor), F('C3', 'D4', 'multi_step', c4s3_abc), F('C4', 'D3', 'numerical', c4s3_sum_cubes),
                   F('C4', 'D4', 'case', c4s3_case)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_mcq), F('C2', 'D2', 'explain', c4s4_explain), F('C2', 'D3', 'mcq', c4s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c4s4_diff_sq),
                   F('C3', 'D2', 'numerical', c4s4_split), F('C3', 'D3', 'numerical', c4s4_split), F('C3', 'D4', 'multi_step', c4s4_group), F('C4', 'D3', 'case', c4s4_area_fact),
                   F('C4', 'D4', 'long', c4s4_area_fact, gap='G7')],
    S + '04-st5': [F('C1', 'D2', 'mcq', c4s5_mcq), F('C2', 'D2', 'explain', c4s5_explain), F('C2', 'D2', 'mcq', c4s5_ar, kinds=('ar',)), F('C3', 'D1', 'short', c4s5_sq),
                   F('C3', 'D2', 'short', c4s5_diff), F('C3', 'D3', 'numerical', c4s5_simplify), F('C4', 'D3', 'case', c4s5_case)],
    S + '05-st1': [F('C1', 'D2', 'mcq', c5s1_parts), F('C1', 'D1', 'short', c5s1_diam), F('C2', 'D2', 'explain', c5s1_explain), F('C2', 'D2', 'mcq', c5s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c5s1_angle), F('C3', 'D3', 'numerical', c5s1_count), F('C4', 'D3', 'case', c5s1_case)],
    S + '05-st2': [F('C1', 'D2', 'mcq', c5s2_mcq), F('C1', 'D1', 'short', c5s2_radius), F('C2', 'D2', 'explain', c5s2_explain), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s2_chord_len), F('C3', 'D3', 'numerical', c5s2_dist), F('C3', 'D4', 'multi_step', c5s2_parallel), F('C4', 'D3', 'case', c5s2_case),
                   F('C4', 'D4', 'long', c5s2_parallel)],
    S + '05-st3': [F('C1', 'D2', 'mcq', c5s3_mcq), F('C1', 'D1', 'short', c5s3_centre), F('C2', 'D2', 'explain', c5s3_explain), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c5s3_same_seg), F('C3', 'D2', 'short', c5s3_semicircle), F('C3', 'D3', 'numerical', c5s3_isos), F('C3', 'D4', 'multi_step', c5s3_find),
                   F('C4', 'D3', 'case', c5s3_case), F('C4', 'D4', 'multi_step', c5s3_find)],
    S + '05-st4': [F('C1', 'D2', 'mcq', c5s4_mcq), F('C1', 'D1', 'short', c5s4_opp), F('C2', 'D2', 'explain', c5s4_explain), F('C2', 'D2', 'mcq', c5s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c5s4_ext), F('C3', 'D3', 'numerical', c5s4_expr), F('C4', 'D3', 'multi_step', c5s4_find), F('C4', 'D4', 'case', c5s4_case)],
}
