"""CBSE class 9 maths (Ganita Manjari) families, chapters 6-10."""
from __future__ import annotations

import math
import statistics
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, frac, name, two_names, inr, num_distractors
from g9_maths_h import nz, Q, mcqbank, arbank, xbank, P, fn, rad, is_sq, poly, lin, term, triple, signed, bracket, PI, pistr, ordinal

S = 'cbse-g9-maths-ch'


def heron(a, b, c):
    s = Fr(a + b + c, 2)
    v = s * (s - a) * (s - b) * (s - c)
    return s, v


HERON_INT = [(13, 14, 15), (5, 12, 13), (9, 10, 17), (10, 13, 13), (7, 15, 20), (13, 20, 21), (11, 13, 20), (17, 25, 28), (8, 15, 17),
             (6, 25, 29), (12, 17, 25), (5, 5, 6), (5, 5, 8), (10, 10, 12), (25, 25, 14), (3, 4, 5), (6, 8, 10), (9, 12, 15)]


def heron_tri(r):
    a, b, c = r.choice(HERON_INT)
    k = r.choice([1, 1, 2, 3])
    a, b, c = a * k, b * k, c * k
    s, v = heron(a, b, c)
    A = math.isqrt(int(v))
    assert A * A == v
    return a, b, c, int(s), A


# ---------------- ch06 Perimeter and area ----------------

def c6s1_formula(r):
    return mcqbank([
        ('The area of a trapezium with parallel sides a and b and height h is …', '½ (a + b) h', ['(a + b) h', '½ a b h', 'a b h'], 'Split into two triangles or join two copies to form a parallelogram.'),
        ('The area of a parallelogram with base b and corresponding height h is …', 'b × h', ['½ b × h', '2(b + h)', 'b × slant side'], 'Cut and move a triangle to form a rectangle b × h.'),
        ('The area of a rhombus with diagonals d₁ and d₂ is …', '½ d₁ d₂', ['d₁ d₂', '2 d₁ d₂', '¼ d₁ d₂'], 'The diagonals are perpendicular; four right triangles.'),
        ('A triangle and a parallelogram on the same base and between the same parallels have areas in the ratio …', '1 : 2', ['1 : 1', '2 : 1', '1 : 4'], 'Triangle = ½ b h, parallelogram = b h.'),
    ])(r)


def c6s1_tri(r):
    b, h = r.randint(4, 30), r.randint(3, 24)
    return Q(f'Find the area of a triangle with base {b} cm and height {h} cm.', f'{num(b * h / 2)} cm²', f'½ × {b} × {h} = {num(b * h / 2)}.',
             [f'{b * h} cm²', f'{num(b * h / 4)} cm²', f'{b + h} cm²'])


def c6s1_trap(r):
    a, b, h = r.randint(5, 30), r.randint(5, 30), r.randint(4, 20)
    if a == b:
        b += 3
    return Q(f'The parallel sides of a trapezium are {a} m and {b} m, and the distance between them is {h} m. Find its area.', f'{num((a + b) * h / 2)} m²',
             f'½ ({a} + {b}) × {h} = {num((a + b) * h / 2)}.', [f'{(a + b) * h} m²', f'{num(a * b * h / 2)} m²', f'{num((a + b) * h / 4)} m²'])


def c6s1_height(r):
    b = r.randint(6, 25)
    h = r.randint(4, 20)
    A = b * h
    other = r.randint(b + 1, b + 10)
    return Q(f'A parallelogram has sides {b} cm and {other} cm. The height on the {b} cm side is {h} cm. Find the height on the {other} cm side.', f'{num(A / other)} cm',
             f'Area = {b} × {h} = {A} cm²; height = {A} ÷ {other} = {num(A / other)} cm.', [f'{h} cm', f'{num(other * h / b)} cm', f'{num(A / (b + other))} cm'])


def c6s1_explain(r):
    return xbank([
        ('Explain how the area formula of a trapezium can be obtained by joining two copies of it.', 'Two copies form a parallelogram of base (a + b) and height h; one trapezium is half: ½(a + b)h.', '2 marks.'),
        ('Explain why the area of a parallelogram equals base × height.', 'Cut a right triangle from one end and fix it at the other end to get a rectangle of the same base and height.', '2 marks.'),
        ('Explain why all triangles on the same base and between the same parallels have equal areas.', 'They have the same base and the same height (the distance between the parallels).', '2 marks.'),
        ('Explain why the area of a rhombus is half the product of its diagonals.', 'Diagonals bisect at right angles, giving four right triangles each ½ (d₁/2)(d₂/2); total ½ d₁d₂.', '2 marks.'),
    ])(r)


def c6s1_ar(r):
    b, h = r.randint(4, 20), r.randint(3, 15)
    return arbank([
        (f'A triangle and a parallelogram on the same base {b} cm and between the same parallels {h} cm apart have areas {num(b * h / 2)} cm² and {b * h} cm².', 'The area of a triangle is half the area of a parallelogram on the same base and between the same parallels.', 'a', 'R explains A.'),
        (f'A rhombus with diagonals {b} cm and {h + 1} cm has area {b * (h + 1)} cm².', 'The diagonals of a rhombus bisect each other at right angles.', 'd', f'Area = ½ × {b} × {h + 1} = {num(b * (h + 1) / 2)}; A false, R true.'),
        ('Two parallelograms with equal areas must be congruent.', 'Area of a parallelogram = base × height.', 'd', 'e.g. 6 × 2 and 4 × 3 have equal areas but are not congruent; A false, R true.'),
    ])(r)


def c6s1_rhombus(r):
    d1, d2 = r.choice([(6, 8), (10, 24), (16, 30), (12, 16), (14, 48), (18, 24)])
    return Q(f'The diagonals of a rhombus are {d1} cm and {d2} cm. Find its area and its perimeter.', f'Area {d1 * d2 // 2} cm², perimeter {4 * int(math.hypot(d1 / 2, d2 / 2))} cm',
             f'Area = ½ d₁d₂ = {d1 * d2 // 2}; side = √({d1 // 2}² + {d2 // 2}²) = {int(math.hypot(d1 / 2, d2 / 2))}; perimeter = 4 × side (3 marks).')


def c6s1_field(r):
    a, b, h = r.randint(20, 60), r.randint(20, 60), r.randint(10, 40)
    rate = r.choice([5, 8, 10, 12, 15])
    A = Fr((a + b) * h, 2)
    return Q((f'A farmer near Nashik has a field in the shape of a trapezium with parallel sides {a} m and {b} m, {h} m apart. '
              f'(i) Find the area of the field. (ii) Find the cost of ploughing it at ₹{rate} per m². (iii) If the farmer divides it by a diagonal into two triangles, find the area of each triangle.'),
             f'(i) {pistr(A)} m² (ii) {inr(float(A) * rate)} (iii) {pistr(Fr(a * h, 2))} m² and {pistr(Fr(b * h, 2))} m²',
             'Trapezium formula (1), cost (1), each triangle has height h and base one parallel side (2).')


# st2 Heron's formula

def c6s2_mcq(r):
    a, b, c, s, A = heron_tri(r)
    return mcq(f'The semi-perimeter of a triangle with sides {a} cm, {b} cm and {c} cm is …', f'{s} cm', [f'{2 * s} cm', f'{a + b} cm', f'{s + 1} cm'],
               f's = ({a} + {b} + {c})/2 = {s}.', r)


def c6s2_formula(r):
    return mcqbank([
        ("Heron's formula for the area of a triangle with sides a, b, c and semi-perimeter s is …", '√[s(s − a)(s − b)(s − c)]', ['s(s − a)(s − b)(s − c)', '√[(s − a)(s − b)(s − c)]', '½ √[abc]'], "Heron's formula."),
        ('The area of an equilateral triangle of side a is …', '(√3/4) a²', ['(√3/2) a²', '(1/2) a²', '√3 a²'], 'Height = (√3/2) a.'),
        ("Heron's formula is most useful when we know …", 'all three sides of the triangle', ['the base and height', 'two angles', 'only the perimeter'], 'It needs a, b and c.'),
    ])(r)


def c6s2_area(r):
    a, b, c, s, A = heron_tri(r)
    return Q(f"Find the area of a triangle with sides {a} cm, {b} cm and {c} cm using Heron's formula.", f'{A} cm²',
             f's = {s}; area = √[{s} × {s - a} × {s - b} × {s - c}] = √{A * A} = {A}.', [f'{A * 2} cm²', f'{s * 2} cm²', f'{A + s} cm²'])


def c6s2_perimeter(r):
    a, b, c, s, A = heron_tri(r)
    g = math.gcd(math.gcd(a, b), c)
    ra, rb, rc = a // g, b // g, c // g
    per = 2 * s
    return Q(f'The sides of a triangle are in the ratio {ra} : {rb} : {rc} and its perimeter is {per} cm. Find its area.', f'{A} cm²',
             f'Sides {a}, {b}, {c} (k = {g}); s = {s}; area = √[{s}·{s - a}·{s - b}·{s - c}] = {A} (3 marks).')


def c6s2_equi(r):
    a = r.choice([4, 6, 8, 10, 12, 14, 20])
    area_c = Fr(a * a, 4)
    return Q(f'Find the area of an equilateral triangle of side {a} cm.', f'{fn(area_c)}√3 cm²', f'(√3/4) × {a}² = {fn(area_c)}√3 ≈ {num(float(area_c) * 1.732, 2)} cm².',
             [f'{fn(area_c * 2)}√3 cm²', f'{fn(area_c)} cm²', f'{a * a}√3 cm²'])


def c6s2_explain(r):
    a, b, c, s, A = heron_tri(r)
    return Q(f"A triangle has sides {a} cm, {b} cm, {c} cm. Explain why Heron's formula is convenient here and state the first two steps.", f's = {s}; then s − a, s − b, s − c = {s - a}, {s - b}, {s - c}',
             'Height is not known, but all sides are; find s, then the three differences (2 marks).')


def c6s2_ar(r):
    a, b, c, s, A = heron_tri(r)
    return arbank([
        (f'The area of a triangle with sides {a}, {b}, {c} cm is {A} cm².', "Heron's formula gives area = √[s(s − a)(s − b)(s − c)].", 'a', f's = {s}; R gives A.'),
        ('A triangle with sides 3 cm, 4 cm and 8 cm has area found by Heron\'s formula.', 'The sum of any two sides of a triangle is greater than the third side.', 'd', '3 + 4 < 8 so no such triangle exists; A false, R true.'),
        ('An isosceles right triangle with legs 4 cm has area 8 cm².', "Heron's formula can be used for any triangle.", 'b', 'Both true, but ½ × 4 × 4 is the direct reason.'),
    ])(r)


def c6s2_quad(r):
    # quadrilateral: right triangle + Heron triangle on hypotenuse
    p, q, h = triple(r)
    opts = [(x, y) for x in range(h // 2 + 1, h + 15) for y in range(x, h + 15) if x + y > h and (x * 0 == 0)]
    r.shuffle(opts)
    for x, y in opts:
        s, v = heron(h, x, y)
        if v > 0 and v.denominator == 1 and is_sq(int(v)):
            A2 = math.isqrt(int(v))
            break
    else:
        raise ValueError
    A1 = Fr(p * q, 2)
    return Q((f'ABCD is a quadrilateral with AB = {p} m, BC = {q} m, ∠B = 90°, CD = {x} m and DA = {y} m. Find its area.'),
             f'{fn(A1 + A2)} m²', f'AC = √({p}² + {q}²) = {h}; area △ABC = {fn(A1)}; area △ACD by Heron (s = {fn(s)}) = {A2}; total {fn(A1 + A2)} (5 marks).')


def c6s2_case_fix(r):
    a, b, c, s, A = heron_tri(r)
    rate = r.choice([20, 30, 40, 50])
    g = r.choice([2, 3, 4])
    return Q((f'A triangular park in Bengaluru has sides {a} m, {b} m and {c} m. (i) Find its semi-perimeter. (ii) Find its area. '
              f'(iii) Find the cost of laying grass at ₹{rate} per m². (iv) A fence is put on all sides except a {g} m gate. How much fencing is needed?'),
             f'(i) {s} m (ii) {A} m² (iii) {inr(A * rate)} (iv) {2 * s - g} m', 'Heron (2), cost (1), perimeter − gate (1).')


def c6s2_iso(r):
    a, b = r.choice([(5, 6), (5, 8), (10, 12), (13, 10), (17, 16), (25, 14), (13, 24), (10, 16)])
    h2 = a * a - (b / 2) ** 2
    A = b / 2 * math.sqrt(h2)
    return Q(f"An isosceles triangle has equal sides {a} cm and base {b} cm. Find its area using Heron's formula.", f'{num(A)} cm²',
             f's = {num((2 * a + b) / 2)}; area = √[s(s − {a})(s − {a})(s − {b})] = {num(A)}.', [f'{num(A * 2)} cm²', f'{num(a * b / 2)} cm²', f'{num(A / 2)} cm²'])


# st3 circles, sectors, rings

def c6s3_mcq(r):
    return mcqbank([
        ('The area of a sector of angle θ in a circle of radius r is …', '(θ/360) × πr²', ['(θ/360) × 2πr', 'θ × πr²', '(θ/180) × πr²'], 'Fraction θ/360 of the full circle.'),
        ('The area of a ring between circles of radii R and r (R > r) is …', 'π(R² − r²)', ['π(R − r)²', '2π(R − r)', 'π(R + r)'], 'Outer area minus inner area.'),
        ('If the radius of a circle is doubled, its area becomes …', '4 times', ['2 times', '8 times', 'half'], 'Area ∝ r².'),
        ('The length of an arc of angle θ in a circle of radius r is …', '(θ/360) × 2πr', ['(θ/360) × πr²', 'θr', '(θ/180) × πr²'], 'Fraction of the circumference.'),
    ])(r)


def c6s3_circ(r):
    rr = 7 * r.randint(1, 8)
    return Q(f'Find the circumference of a circle of radius {rr} cm (π = 22/7).', f'{2 * 22 * rr // 7} cm', f'2πr = 2 × 22/7 × {rr} = {2 * 22 * rr // 7}.',
             [f'{22 * rr * rr // 7} cm', f'{22 * rr // 7} cm', f'{4 * 22 * rr // 7} cm'])


def c6s3_area(r):
    rr = r.choice([7, 14, 21, 3.5, 10.5, 28, 35])
    A = PI * Fr(rr) ** 2
    return Q(f'Find the area of a circle of radius {num(rr)} cm (π = 22/7).', f'{pistr(A)} cm²', f'πr² = 22/7 × {num(rr)}² = {pistr(A)}.',
             [f'{pistr(2 * PI * Fr(rr))} cm²', f'{pistr(A * 2)} cm²', f'{pistr(PI * Fr(rr) * 2 * Fr(rr) * 2)} cm²'])


def c6s3_sector(r):
    rr = r.choice([7, 14, 21, 28])
    th = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 210])
    A = Fr(th, 360) * PI * rr * rr
    return Q(f'Find the area of a sector of angle {th}° in a circle of radius {rr} cm (π = 22/7).', f'{pistr(A)} cm²', f'({th}/360) × 22/7 × {rr}² = {pistr(A)}.',
             [f'{pistr(Fr(th, 360) * 2 * PI * rr)} cm²', f'{pistr(Fr(th, 180) * PI * rr * rr)} cm²', f'{pistr(PI * rr * rr)} cm²'])


def c6s3_ring(r):
    R = 7 * r.randint(2, 6)
    rr = R - 7 * r.randint(1, R // 7 - 1)
    A = PI * (R * R - rr * rr)
    return Q(f'A circular path runs around a circular garden. The outer radius is {R} m and the inner radius is {rr} m. Find the area of the path (π = 22/7).', f'{pistr(A)} m²',
             f'π(R² − r²) = 22/7 × ({R * R} − {rr * rr}) = {pistr(A)}.', [f'{pistr(PI * (R - rr) ** 2)} m²', f'{pistr(2 * PI * (R - rr))} m²', f'{pistr(PI * (R * R + rr * rr))} m²'])


def c6s3_reverse(r):
    rr = 7 * r.randint(1, 6)
    C = 2 * 22 * rr // 7
    return Q(f'The circumference of a circle is {C} cm. Find its area (π = 22/7).', f'{22 * rr * rr // 7} cm²', f'r = {C} ÷ (2 × 22/7) = {rr}; area = 22/7 × {rr}² = {22 * rr * rr // 7} (3 marks).',
             [f'{C * 2} cm²', f'{22 * (2 * rr) ** 2 // 7} cm²', f'{11 * rr * rr // 7} cm²'])


def c6s3_explain(r):
    return xbank([
        ('Explain why a sector of angle 90° has one-fourth the area of the circle.', '90° is one-fourth of 360°, and the area of a sector is proportional to its angle.', '2 marks.'),
        ('Explain why the area of a ring is not π(R − r)².', 'Area of ring = πR² − πr² = π(R² − r²) = π(R − r)(R + r), not π(R − r)².', '2 marks.'),
        ('If the circumference of a circle doubles, what happens to its area? Explain.', 'It becomes 4 times.', 'C ∝ r so r doubles; A ∝ r² (2 marks).'),
    ])(r)


def c6s3_ar(r):
    rr = r.choice([7, 14])
    return arbank([
        (f'The area of a semicircle of radius {rr} cm is {11 * rr * rr // 7} cm².', 'A semicircle is a sector of angle 180°.', 'a', 'Half of πr²; R explains A.'),
        ('If the radius of a circle is tripled, its area is tripled.', 'The area of a circle is proportional to the square of its radius.', 'd', 'Area becomes 9 times; A false, R true.'),
        ('The perimeter of a semicircle of radius r is πr.', 'The arc of a semicircle has length πr.', 'd', 'Perimeter = πr + 2r (include the diameter); A false, R true.'),
    ])(r)


def c6s3_case(r):
    rr = 7 * r.randint(1, 3)
    w = r.choice([3.5, 7])
    rate = r.choice([10, 12, 15, 20])
    R = Fr(rr) + Fr(w)
    return Q((f'A circular pond in a park has radius {rr} m. A path {num(w)} m wide is built around it. (π = 22/7) (i) Find the outer radius. (ii) Find the area of the path. '
              f'(iii) Find the cost of tiling the path at ₹{rate} per m². (iv) Find the length of the outer boundary of the path.'),
             f'(i) {pistr(R)} m (ii) {pistr(PI * (R * R - rr * rr))} m² (iii) {inr(float(PI * (R * R - rr * rr)) * rate)} (iv) {pistr(2 * PI * R)} m',
             'Ring area π(R² − r²) and circumference 2πR (1 mark each).')


# st4 composite figures

def c6s4_path(r):
    l, b = r.randint(20, 80), r.randint(15, 60)
    w = r.choice([1, 1.5, 2, 2.5, 3])
    A = (l + 2 * w) * (b + 2 * w) - l * b
    rate = r.choice([20, 25, 40, 50])
    return Q(f'A rectangular lawn {l} m × {b} m has a path {num(w)} m wide all around it on the outside. Find the area of the path and the cost of gravelling it at ₹{rate} per m².',
             f'{num(A)} m²; {inr(A * rate)}', f'Outer {num(l + 2 * w)} × {num(b + 2 * w)} − {l} × {b} = {num(A)} m²; × ₹{rate} (3 marks).')


def c6s4_cross(r):
    l, b = r.randint(40, 90), r.randint(30, 70)
    w = r.randint(2, 5)
    A = w * l + w * b - w * w
    return Q(f'Two roads, each {w} m wide, cross each other at right angles through the centre of a rectangular park {l} m × {b} m, parallel to its sides. Find the area covered by the roads.', f'{A} m²',
             f'{w} × {l} + {w} × {b} − {w} × {w} (the central square is counted twice) = {A}.', [f'{w * l + w * b} m²', f'{w * (l + b) + w * w} m²', f'{2 * w * (l + b)} m²'])


def c6s4_semi(r):
    a = 14 * r.randint(1, 3)
    A = a * a + Fr(1, 2) * PI * Fr(a, 2) ** 2
    return Q(f'A window is made of a square of side {a} cm with a semicircle on its top side. Find the area of glass needed (π = 22/7).', f'{pistr(A)} cm²',
             f'{a}² + ½ × 22/7 × {a // 2}² = {a * a} + {pistr(Fr(1, 2) * PI * Fr(a, 2) ** 2)} = {pistr(A)}.', [f'{pistr(a * a + PI * Fr(a, 2) ** 2)} cm²', f'{pistr(a * a + Fr(1, 2) * PI * a * a)} cm²', f'{a * a} cm²'])


def c6s4_explain(r):
    return xbank([
        ('A plot is in the shape of an L. Explain two different ways to find its area.', 'Split into two rectangles, or subtract the missing rectangle from the enclosing rectangle.', '1 mark each method.'),
        ('Explain why, when two crossing roads are laid in a park, the area of the central square must be subtracted once.', 'The square where the roads cross is included in both road areas.', '2 marks.'),
        ('Explain how to find the area of a quadrilateral field if only its four sides and one diagonal are known.', 'Divide it along the diagonal into two triangles and use Heron\'s formula for each.', '2 marks.'),
    ])(r)


def c6s4_ar(r):
    return arbank([
        ('The area of a path around a rectangle is (outer area − inner area).', 'The path occupies exactly the region between the two rectangles.', 'a', 'R explains A.'),
        ('Doubling the width of a path around a lawn doubles the area of the path.', 'Area of a path = (l + 2w)(b + 2w) − lb.', 'd', 'Area = 2w(l + b) + 4w², not proportional to w; A false, R true.'),
        ('1 hectare = 10,000 m².', '1 hectare is the area of a square of side 100 m.', 'a', '100 m × 100 m.'),
    ])(r)


def c6s4_units(r):
    A = r.choice([25000, 12500, 40000, 7500, 150000])
    return Q(f'Convert {A:,} m² into hectares.'.replace(',', ','), f'{num(A / 10000)} ha', '1 ha = 10,000 m².', [f'{num(A / 1000)} ha', f'{num(A / 100)} ha', f'{num(A / 100000)} ha'])


def _heron_all():
    out = []
    for (a, b, c) in HERON_INT:
        for k in (1, 2, 3):
            s_, v = heron(a * k, b * k, c * k)
            out.append((a * k, b * k, c * k, int(s_), math.isqrt(int(v))))
    return out


def c6s4_quad_field(r):
    allt = _heron_all()
    t1 = r.choice(allt)
    side = r.choice(t1[:3])
    others = [t for t in allt if side in t[:3] and t != t1]
    if not others:
        raise ValueError
    t2 = r.choice(others)
    rest1 = list(t1[:3])
    rest1.remove(side)
    a, b = rest1
    rest2 = list(t2[:3])
    rest2.remove(side)
    a2, b2 = rest2
    A, A2 = t1[4], t2[4]
    c = side
    return Q((f'A quadrilateral field ABCD has diagonal AC = {c} m. Triangle ABC has AB = {a} m, BC = {b} m and triangle ACD has CD = {a2} m, DA = {b2} m. '
              f'Find the area of the field in m² and in hectares.'), f'{A + A2} m² = {num((A + A2) / 10000, 4)} ha',
             f"Heron's formula on each triangle: {A} + {A2} = {A + A2} m² (4 marks); ÷ 10,000 for hectares (1 mark).")


def c6s4_case(r):
    l, b = r.choice([(40, 30), (60, 45), (80, 60), (36, 27)])
    d = int(math.hypot(l, b))
    rate = r.choice([15, 20, 25])
    return Q((f'A school is planning a rectangular ground {l} m by {b} m. (i) Find its area. (ii) A straight diagonal path is planned from one corner to the opposite corner. Find its length. '
              f'(iii) The path is 2 m wide. Taking its area as length × width, find its approximate area. (iv) Find the cost of turfing the rest of the ground at ₹{rate} per m².'),
             f'(i) {l * b} m² (ii) {d} m (iii) ≈ {2 * d} m² (iv) ≈ {inr((l * b - 2 * d) * rate)}',
             'Area (1), Pythagoras (1), strip approximation (1), cost (1).')


# ---------------- ch07 Probability ----------------

def c7s1_mcq(r):
    return mcqbank([
        ('The probability of an event that is certain to happen is …', '1', ['0', '½', '100'], 'Certain events have probability 1.'),
        ('The probability of an impossible event is …', '0', ['1', '−1', '½'], 'It never happens.'),
        ('Which of these can NOT be the probability of an event?', '1.2', ['0', '0.75', '2/3'], 'Probabilities lie between 0 and 1.'),
        ('Getting a number greater than 6 on a single throw of a die is …', 'an impossible event', ['a sure event', 'an equally likely event', 'a likely event'], 'Faces are 1 to 6.'),
        ('When a fair coin is tossed, the outcomes head and tail are …', 'equally likely', ['impossible', 'certain', 'unequal in chance'], 'A fair coin has no bias.'),
        ('The set of all possible outcomes of an experiment is called the …', 'sample space', ['event', 'trial', 'frequency'], 'Definition.'),
    ])(r)


def c7s1_list(r):
    exp = r.choice([('a die is thrown once', '1, 2, 3, 4, 5, 6', 6), ('a coin is tossed once', 'H, T', 2), ('a coin is tossed twice', 'HH, HT, TH, TT', 4),
                    ('a spinner with sectors labelled A, B, C, D is spun once', 'A, B, C, D', 4), ('one day of the week is chosen at random', 'Monday, …, Sunday', 7)])
    return Q(f'List all the possible outcomes when {exp[0]}. How many are there?', f'{exp[1]}; {exp[2]} outcomes', 'Sample space listing.',
             [f'{exp[2] + 1} outcomes', f'{exp[2] - 1} outcomes', f'{2 * exp[2]} outcomes'])


def c7s1_classify(r):
    ev = r.choice([('the sun rises in the east tomorrow', 'certain'), ('a die shows 7', 'impossible'), ('a die shows an even number', 'even chance'),
                   ('a card drawn from cards numbered 1–10 shows a number less than 9', 'likely'), ('it snows in Chennai in May', 'very unlikely'),
                   ('a tossed coin shows a head', 'even chance'), ('a number picked from 1 to 100 is greater than 95', 'unlikely')])
    opts = ['certain', 'impossible', 'even chance', 'likely', 'unlikely', 'very unlikely']
    wrong = [o for o in opts if o != ev[1] and not (ev[1] == 'very unlikely' and o == 'unlikely') and not (ev[1] == 'unlikely' and o == 'very unlikely')]
    return mcq(f'On the scale impossible – unlikely – even chance – likely – certain, how would you describe the event "{ev[0]}"?', ev[1], r.sample(wrong, 3),
               'Place the event on the 0–1 probability scale.', r)


def c7s1_explain(r):
    return xbank([
        ('Explain why the probability of any event lies between 0 and 1.', 'P(E) = favourable/total, and 0 ≤ favourable ≤ total.', '2 marks.'),
        ('A student says: "A coin showed heads 5 times in a row, so tails is now more likely." Is this right? Explain.', 'No.', 'Each toss is independent; P(tail) is still ½ (2 marks).', ),
        ('Explain what is meant by "equally likely outcomes" with an example.', 'Each outcome has the same chance, e.g. the faces of a fair die.', '2 marks.'),
        ('Why are the outcomes "even" and "prime" on a die not equally likely as a pair of events, and do they overlap?', 'Both have 3 outcomes (equal chance) but they overlap at 2.', '2 marks.'),
    ])(r)


def c7s1_ar(r):
    return arbank([
        ('The probability of getting 7 on a single die is 0.', 'An impossible event has probability 0.', 'a', 'R explains A.'),
        ('In a single throw of a die, getting an odd number and getting an even number are equally likely.', 'A die has 3 odd and 3 even faces.', 'a', 'R explains A.'),
        ('A probability of 1.5 means the event is very likely.', 'Probability cannot exceed 1.', 'd', 'A false, R true.'),
        ('Winning or losing a cricket match are equally likely outcomes.', 'There are only two outcomes, win or lose.', 'd', 'Two outcomes need not be equally likely (and a match can be tied or drawn); A false.'),
    ])(r)


def c7s1_case(r):
    n = r.choice([10, 12, 15, 20])
    return Q((f'A bag has cards numbered 1 to {n}. A card is drawn at random. (i) List the sample space briefly. (ii) Is getting a number greater than {n} possible? '
              f'(iii) Describe the chance of getting a number less than or equal to {n}. (iv) Which is more likely: an even number or a multiple of 5?'),
             f'(i) {{1, 2, …, {n}}} (ii) no, impossible (iii) certain (iv) even number ({n // 2} outcomes vs {n // 5})', '1 mark each part.')


# st2 empirical probability

def c7s2_coin(r):
    n = r.choice([50, 100, 200, 250, 400, 500, 1000])
    h = r.randint(int(n * 0.4), int(n * 0.6))
    return Q(f'A coin is tossed {n} times and a head appears {h} times. Find the empirical probability of getting a tail.', frac(n - h, n),
             f'Tails = {n} − {h} = {n - h}; P(T) = {n - h}/{n} = {frac(n - h, n)}.', [frac(h, n), frac(n - h, h), '1/2' if frac(n - h, n) != '1/2' else frac(h + 1, n)])


def c7s2_die(r):
    n = r.choice([60, 120, 300, 600])
    counts = [n // 6 + r.randint(-n // 30, n // 30) for _ in range(5)]
    counts.append(n - sum(counts))
    face = r.randint(1, 6)
    k = counts[face - 1]
    tab = ', '.join(f'{i + 1}: {c}' for i, c in enumerate(counts))
    return Q(f'A die is thrown {n} times with these frequencies — {tab}. Find the empirical probability of getting {face}.', frac(k, n),
             f'{k}/{n}' + ('' if frac(k, n) == f'{k}/{n}' else f' = {frac(k, n)}') + '.', [frac(1, 6) if frac(k, n) != '1/6' else frac(k + 1, n), frac(k, n - k), frac(n - k, n)])


def c7s2_mcq(r):
    n = r.choice([20, 40, 50, 80, 100])
    k = r.randint(1, n - 1)
    return mcq(f'In {n} trials, an event happened {k} times. Its empirical probability is …', frac(k, n), [frac(n - k, n), f'{k}', frac(k, n - k) if n - k != n else frac(k, n + 1)],
               'Number of trials in which the event happened ÷ total trials.', r)


def c7s2_predict(r):
    who = name(r)
    n, k = r.choice([(50, 3), (200, 8), (100, 5), (400, 12), (250, 10)])
    big = r.choice([1000, 2000, 5000, 10000])
    return Q(f'{who} checks {n} bulbs from a factory and finds {k} defective. Estimate the number of defective bulbs in a batch of {big:,}.'.replace(',', ','), str(big * k // n),
             f'P(defective) ≈ {k}/{n}; expected = {k}/{n} × {big} = {big * k // n}.', num_distractors(big * k // n, big // n * (n - k), k * 10, big * k // n + k))


def c7s2_explain(r):
    return xbank([
        ('Explain the difference between empirical probability and theoretical probability.', 'Empirical is from the results of actual trials; theoretical is from equally likely outcomes before any trial.', '2 marks.'),
        ('A coin tossed 10 times gave 7 heads. Explain why this does not prove the coin is biased.', 'With few trials, results vary; the empirical probability settles near the true value only for a large number of trials.', '2 marks.'),
        ('Why do we expect the empirical probability of a head to come closer to ½ as the number of tosses increases?', 'Random fluctuations even out over many trials.', '2 marks.'),
    ])(r)


def c7s2_ar(r):
    return arbank([
        ('The empirical probability of an event can change from one experiment to another.', 'Empirical probability depends on the actual outcomes of the trials.', 'a', 'R explains A.'),
        ('If a coin gives 6 heads in 10 tosses, the empirical probability of a head is 0.6.', 'Empirical probability = number of times the event occurs ÷ number of trials.', 'a', 'R gives A.'),
        ('The empirical probability of an event can be 1.2 if the event happens many times.', 'An event cannot happen more times than the number of trials.', 'd', 'Empirical probability ≤ 1; A false, R true.'),
    ])(r)


def c7s2_table(r):
    n = r.choice([30, 40, 50, 60])
    a = r.randint(n // 6, n // 3)
    b = r.randint(n // 6, n // 3)
    c = n - a - b
    return Q((f'A survey of {n} families in a colony in Indore gave: 0 or 1 child: {a}, 2 children: {b}, 3 or more children: {c}. A family is chosen at random. '
              f'Find the probability that it has (i) 2 children (ii) at most 2 children (iii) at least 1 child is not determinable — explain why, and (iv) check that the three probabilities in the table add to 1.'),
             f'(i) {frac(b, n)} (ii) {frac(a + b, n)} (iii) the group "0 or 1" mixes 0 and 1 children, so "at least 1" cannot be separated (iv) {frac(a, n)} + {frac(b, n)} + {frac(c, n)} = 1',
             '1 mark each part.')


def c7s2_case(r):
    n = r.choice([100, 200, 365])
    rain = r.randint(int(n * 0.2), int(n * 0.5))
    city = r.choice(['Mumbai', 'Kolkata', 'Guwahati', 'Kochi'])
    return Q((f'Weather records for {city} show that it rained on {rain} of the last {n} days. (i) Find the empirical probability that it rains on a given day. (ii) Find the probability it does not rain. '
              f'(iii) Estimate the number of rainy days in the next 30 days. (iv) Why might this estimate be poor for a 30-day period in the monsoon?'),
             f'(i) {frac(rain, n)} (ii) {frac(n - rain, n)} (iii) ≈ {round(30 * rain / n)} days (iv) rain depends on the season; the data mixes all seasons',
             '1 mark each part.')


# st3 theoretical probability

def c7s3_bag(r):
    colours = r.sample(['red', 'blue', 'green', 'yellow', 'white', 'black'], 3)
    ns = [r.randint(2, 12) for _ in range(3)]
    i = r.randint(0, 2)
    tot = sum(ns)
    desc = ', '.join(f'{n} {c}' for n, c in zip(ns, colours))
    return Q(f'A bag contains {desc} balls. One ball is drawn at random. Find the probability that it is {colours[i]}.', frac(ns[i], tot),
             f'{ns[i]} favourable out of {tot}: {frac(ns[i], tot)}.', [frac(ns[i], tot - ns[i]), frac(tot - ns[i], tot), frac(1, 3) if frac(ns[i], tot) != '1/3' else frac(ns[i] + 1, tot)])


def c7s3_die(r):
    ev = r.choice([('a prime number', [2, 3, 5]), ('a number greater than 4', [5, 6]), ('an even number', [2, 4, 6]), ('a multiple of 3', [3, 6]),
                   ('a number less than 5', [1, 2, 3, 4]), ('a factor of 6', [1, 2, 3, 6]), ('a perfect square', [1, 4])])
    k = len(ev[1])
    return mcq(f'A fair die is thrown once. The probability of getting {ev[0]} is …', frac(k, 6), [frac(6 - k, 6) if k != 3 else '1/3', frac(k, 5), frac(k + 1, 6)],
               f'Favourable outcomes {ev[1]}: {k}/6 = {frac(k, 6)}.', r)


def c7s3_cards(r):
    n = r.choice([20, 25, 30, 40, 50])
    ev = r.choice(['a multiple of 4', 'a prime number', 'a perfect square', 'a number divisible by 3 and 5', 'an odd number'])
    nums = range(1, n + 1)
    f = {'a multiple of 4': lambda x: x % 4 == 0, 'a prime number': lambda x: x > 1 and all(x % d for d in range(2, int(x ** .5) + 1)),
         'a perfect square': lambda x: is_sq(x), 'a number divisible by 3 and 5': lambda x: x % 15 == 0, 'an odd number': lambda x: x % 2 == 1}[ev]
    fav = [x for x in nums if f(x)]
    return Q(f'Cards numbered 1 to {n} are put in a box and one is drawn at random. Find the probability that it shows {ev}.', frac(len(fav), n),
             f'Favourable: {", ".join(map(str, fav))} ({len(fav)} cards); P = {len(fav)}/{n} = {frac(len(fav), n)}.', [frac(len(fav) + 1, n), frac(n - len(fav), n), frac(len(fav), n - 1)])


def c7s3_find_n(r):
    red = r.randint(3, 12)
    p = r.choice([Fr(1, 3), Fr(1, 4), Fr(2, 5), Fr(1, 5), Fr(3, 7)])
    tot = red / p
    if tot.denominator != 1:
        raise ValueError
    tot = int(tot)
    return Q(f'A jar has {red} red marbles and some blue marbles. The probability of drawing a red marble is {fn(p)}. How many blue marbles are there?', str(tot - red),
             f'{red}/total = {fn(p)} ⇒ total = {tot}; blue = {tot} − {red} = {tot - red} (3 marks).', num_distractors(tot - red, tot, red, tot - red + 1))


def c7s3_explain(r):
    return xbank([
        ('A student says the probability of getting a 6 on a die is ½ because "either it is 6 or it is not". Explain the mistake.', 'The two outcomes "6" and "not 6" are not equally likely; P(6) = 1/6.', '2 marks.', ),
        ('Explain why P(E) + P(not E) = 1.', 'Every outcome is either in E or not in E, so the favourable counts add to the total.', '2 marks.'),
        ('Why must the outcomes be equally likely before using P(E) = favourable/total?', 'The formula counts outcomes; it gives the right chance only if each outcome has the same chance.', '2 marks.'),
    ])(r)


def c7s3_ar(r):
    k = r.randint(2, 9)
    return arbank([
        ('The probability of getting an even number on a die is ½.', 'Three of the six equally likely outcomes are even.', 'a', 'R explains A.'),
        (f'A bag has {k} red and {k} blue balls, so P(red) = ½.', 'P(E) = number of favourable outcomes ÷ number of equally likely outcomes.', 'a', 'R explains A.'),
        ('If P(E) = 0.3, then P(not E) = 0.3.', 'P(E) + P(not E) = 1.', 'd', 'P(not E) = 0.7; A false, R true.'),
    ])(r)


def c7s3_case(r):
    total = r.choice([30, 40, 50, 60])
    g = r.randint(total // 4, total // 2)
    sp = r.randint(5, total // 3)
    return Q((f'In a class of {total} students in Lucknow, {g} are girls. {sp} students play a musical instrument. A student is chosen at random to lead the assembly. '
              f'(i) Find P(girl). (ii) Find P(boy). (iii) Find P(plays an instrument). (iv) Can you find P(girl who plays an instrument) from this data? Explain.'),
             f'(i) {frac(g, total)} (ii) {frac(total - g, total)} (iii) {frac(sp, total)} (iv) no; we do not know how many instrument players are girls',
             '1 mark each part.')


# st4 outcome tables and trees

def c7s4_sum(r):
    s = r.randint(2, 12)
    k = 6 - abs(7 - s)
    return Q(f'Two dice are thrown together. Find the probability that the sum of the numbers is {s}.', frac(k, 36),
             f'36 equally likely outcomes; sum {s} occurs {k} times: {frac(k, 36)}.', [frac(k, 12), frac(1, 11), frac(k + 1, 36)])


def c7s4_coins(r):
    ev = r.choice([('exactly one head', 2), ('at least one head', 3), ('two heads', 1), ('no head', 1), ('at most one head', 3)])
    c = frac(ev[1], 4)
    wrong = [w for w in ['1/4', '1/2', '3/4', '1/3', '2/3', '1'] if w != c]
    return mcq(f'Two coins are tossed together. The probability of getting {ev[0]} is …', c, r.sample(wrong[:4], 3),
               f'Outcomes HH, HT, TH, TT; favourable {ev[1]} of 4.', r)


def c7s4_three(r):
    ev = r.choice([('exactly two heads', 3), ('at least one tail', 7), ('all heads', 1), ('at most one head', 4), ('exactly one tail', 3)])
    c = frac(ev[1], 8)
    return Q(f'Three coins are tossed. Using a tree diagram, find the probability of {ev[0]}.', c, f'8 outcomes (HHH … TTT); favourable {ev[1]}.',
             [w for w in ['1/8', '3/8', '1/2', '5/8', '7/8', '1/4'] if w != c][:3])


def c7s4_product(r):
    cond = r.choice([('even', lambda a, b: (a * b) % 2 == 0), ('odd', lambda a, b: (a * b) % 2 == 1), ('a multiple of 6', lambda a, b: (a * b) % 6 == 0), ('greater than 20', lambda a, b: a * b > 20)])
    k = sum(1 for a in range(1, 7) for b in range(1, 7) if cond[1](a, b))
    return Q(f'Two dice are thrown. Make an outcome table and find the probability that the product of the numbers is {cond[0]}.', frac(k, 36),
             f'Count the cells of the 6 × 6 table: {k}; P = {k}/36 = {frac(k, 36)} (3 marks).')


def c7s4_explain(r):
    return xbank([
        ('When two coins are tossed, a student lists the outcomes as "two heads, two tails, one of each" and says P(two heads) = 1/3. Explain the error.', 'The three outcomes are not equally likely; "one of each" covers HT and TH, so P(HH) = 1/4.', '2 marks.'),
        ('Explain why there are 36 outcomes when two dice are thrown.', 'Each of the 6 outcomes of the first die pairs with each of the 6 of the second: 6 × 6.', '2 marks.'),
        ('Explain how a tree diagram helps to count the outcomes of tossing a coin and then throwing a die.', 'Two branches (H, T), each splitting into 6: 2 × 6 = 12 outcomes.', '2 marks.'),
    ])(r)


def c7s4_ar(r):
    return arbank([
        ('When two dice are thrown, a sum of 7 is the most likely sum.', 'Sum 7 occurs in 6 of the 36 outcomes, more than any other sum.', 'a', 'R explains A.'),
        ('When two coins are tossed, P(one head and one tail) = ½.', 'HT and TH are two of the four equally likely outcomes.', 'a', 'R explains A.'),
        ('When a coin is tossed and a die is thrown, there are 8 outcomes.', 'The number of outcomes is found by multiplying the numbers of outcomes of each stage.', 'd', '2 × 6 = 12; A false, R true.'),
    ])(r)


def c7s4_spinner(r):
    a = r.randint(3, 6)
    b = r.randint(2, 4)
    return Q((f'A spinner has {a} equal sectors numbered 1 to {a}, and a bag has {b} cards lettered {", ".join("ABCDE"[:b])}. A student spins the spinner and then draws a card. '
              f'(i) How many outcomes are there? (ii) Find P(spinner shows 1 and card is A). (iii) Find P(spinner shows an even number). (iv) Find P(card is not A).'),
             f'(i) {a * b} (ii) {frac(1, a * b)} (iii) {frac(a // 2, a)} (iv) {frac(b - 1, b)}', 'Tree or table (1 mark each part).')


def c7s4_case(r):
    who1, who2 = two_names(r)
    return Q((f'{who1} and {who2} play a game with two dice. {who1} wins if the sum is 6, 7 or 8; otherwise {who2} wins. '
              f'(i) How many outcomes are there? (ii) Find P({who1} wins). (iii) Find P({who2} wins). (iv) Is the game fair? Explain.'),
             f'(i) 36 (ii) 16/36 = 4/9 (iii) 20/36 = 5/9 (iv) no, {who2} has a better chance', 'Sum 6: 5, sum 7: 6, sum 8: 5 outcomes (1 mark each part).')


# ---------------- ch08 Sequences ----------------

def c8s1_next(r):
    k = r.randint(0, 3)
    if k == 0:
        a, d = r.randint(-10, 20), nz(r, 2, 9)
        s = [a + i * d for i in range(5)]
        nx, rule = a + 5 * d, f'add {fn(d)}'
    elif k == 1:
        a, q = r.randint(1, 5), r.choice([2, 3, -2])
        s = [a * q ** i for i in range(5)]
        nx, rule = a * q ** 5, f'multiply by {fn(q)}'
    elif k == 2:
        a, b = r.randint(1, 5), r.randint(1, 6)
        s = [a, b]
        while len(s) < 6:
            s.append(s[-1] + s[-2])
        nx, rule, s = s[5], 'add the previous two terms', s[:5]
    else:
        a = r.randint(1, 4)
        s = [a]
        while len(s) < 6:
            s.append(2 * s[-1] + 1)
        nx, rule, s = s[5], 'double and add 1', s[:5]
    return Q(f'Write the next term of the sequence {", ".join(map(fn, s))}, … and state the rule.', f'{fn(nx)} ({rule})', f'Rule: {rule}.',
             num_distractors(nx, nx + 1, s[-1] * 2 if k != 1 else nx + s[-1], s[-1] + (s[-1] - s[-2])))


def c8s1_recursive(r):
    a = r.randint(1, 6)
    m, c = r.randint(2, 3), nz(r, 1, 5)
    t = [a]
    for _ in range(4):
        t.append(m * t[-1] + c)
    return Q(f'A sequence is defined by t₁ = {a} and tₙ₊₁ = {m}tₙ {signed(c)}. Find t₂, t₃ and t₄.', ', '.join(map(fn, t[1:4])), f'Apply the rule step by step: {", ".join(map(fn, t[:4]))}.',
             [', '.join(map(fn, [m * a, m * m * a, m ** 3 * a])), ', '.join(map(fn, [t[1], t[2] + 1, t[3]])), ', '.join(map(fn, [a + c, a + 2 * c, a + 3 * c]))])


def c8s1_mcq(r):
    return mcqbank([
        ('A rule that gives each term from the term before it is called …', 'a recursive rule', ['an explicit rule', 'a common ratio', 'an identity'], 'Definition.'),
        ('In the Virahanka–Fibonacci sequence 1, 2, 3, 5, 8, …, each term is …', 'the sum of the two previous terms', ['double the previous term', 'the previous term plus 2', 'the square of its position'], 'Rule tₙ = tₙ₋₁ + tₙ₋₂.'),
        ('The sequence 1, 4, 9, 16, … has nth term …', 'n²', ['3n − 2', '2n + 1', 'n + 3'], 'Square numbers.'),
        ('The sequence 2, 6, 18, 54, … is obtained by …', 'multiplying by 3 each time', ['adding 4 each time', 'adding 3 each time', 'squaring each term'], 'Ratio 3.'),
    ])(r)


def c8s1_explain(r):
    a = r.randint(2, 6)
    return Q(f'The sequence {a}, {a + 3}, {a + 6}, {a + 9}, … can be described recursively and explicitly. Explain both descriptions and say which is better for finding the 100th term.', f't₁ = {a}, tₙ₊₁ = tₙ + 3; tₙ = 3n {signed(a - 3)}; explicit is better (t₁₀₀ = {3 * 100 + a - 3})',
             'Recursive (1), explicit (1); explicit avoids computing all 99 earlier terms.')


def c8s1_ar(r):
    return arbank([
        ('The sequence 1, 1, 2, 3, 5, 8, … is not an arithmetic progression.', 'The differences between consecutive terms are not constant.', 'a', 'R explains A.'),
        ('Knowing a recursive rule alone is enough to list a sequence.', 'A recursive rule also needs the first term(s).', 'd', 'A is false without starting values; R is true.'),
        ('The 10th term of tₙ = 2n + 1 is 21.', 'An explicit rule gives a term directly from its position.', 'a', '2 × 10 + 1 = 21; R explains A.'),
    ])(r)


def c8s1_virahanka(r):
    n = r.randint(6, 12)
    f = [1, 2]
    while len(f) < n:
        f.append(f[-1] + f[-2])
    return Q(f'In how many ways can a poetic line of {n} beats be made using short syllables (1 beat) and long syllables (2 beats)? (Virahanka\'s problem)', str(f[n - 1]),
             f'Ways(n) = Ways(n − 1) + Ways(n − 2), starting 1, 2: {", ".join(map(str, f))} (3 marks).')


def c8s1_case(r):
    who = name(r)
    a, m = r.choice([(2, 2), (3, 2), (5, 2), (1, 3)])
    days = r.randint(5, 8)
    t = [a * m ** i for i in range(days)]
    return Q((f'{who} forwards a school announcement to {a} friends on day 1, and each person who receives it forwards it to {m} new people the next day. '
              f'(i) Write a recursive rule for the number of new people tₙ on day n. (ii) Find t₂, t₃ and t₄. (iii) How many new people receive it on day {days}? (iv) Is this an AP? Why?'),
             f'(i) t₁ = {a}, tₙ₊₁ = {m}tₙ (ii) {t[1]}, {t[2]}, {t[3]} (iii) {t[days - 1]} (iv) no; the differences are not constant (it is a GP)', '1 mark each part.')


# st2 AP

def ap(r):
    a = r.randint(-15, 25)
    d = nz(r, 1, 9)
    return a, d


def c8s2_nth(r):
    a, d = ap(r)
    n = r.randint(10, 40)
    return Q(f'Find the {ordinal(n)} term of the AP {", ".join(fn(a + i * d) for i in range(3))}, …', fn(a + (n - 1) * d),
             f'a = {fn(a)}, d = {fn(d)}; aₙ = a + (n − 1)d = {fn(a)} + {n - 1} × {bracket(d)} = {fn(a + (n - 1) * d)}.', num_distractors(a + (n - 1) * d, a + n * d, n * d, a + (n - 1) * d + d))


def c8s2_d(r):
    a = Fr(r.randint(-9, 9), r.choice([1, 2]))
    d = Fr(nz(r, 1, 7), r.choice([1, 2, 3]))
    return mcq(f'The common difference of the AP {", ".join(fn(a + i * d) for i in range(4))}, … is …', fn(d), [fn(-d), fn(a), fn(2 * d)], 'd = a₂ − a₁.', r)


def c8s2_which(r):
    a, d = ap(r)
    n = r.randint(12, 50)
    t = a + (n - 1) * d
    return Q(f'Which term of the AP {", ".join(fn(a + i * d) for i in range(3))}, … is {fn(t)}?', f'{ordinal(n)} term',
             f'{fn(a)} + (n − 1) × {bracket(d)} = {fn(t)} ⇒ n − 1 = {n - 1} ⇒ n = {n}.', [f'{ordinal(n - 1)} term', f'{ordinal(n + 1)} term', f'{ordinal(abs(t // d) if d and t // d > 0 else n + 2)} term'])


def c8s2_isterm(r):
    a, d = r.randint(2, 20), r.randint(2, 9)
    x = a + d * r.randint(10, 40) + r.choice([0, r.randint(1, d - 1)])
    ok = (x - a) % d == 0
    return Q(f'Is {x} a term of the AP {a}, {a + d}, {a + 2 * d}, …? Justify.', 'Yes' if ok else 'No',
             f'{a} + (n − 1){d} = {x} ⇒ n − 1 = {fn(Fr(x - a, d))}; {"a whole number, so yes" if ok else "not a whole number, so no"}.')


def c8s2_two_terms(r):
    a, d = ap(r)
    p, q = sorted(r.sample(range(3, 20), 2))
    return Q(f'The {ordinal(p)} term of an AP is {fn(a + (p - 1) * d)} and the {ordinal(q)} term is {fn(a + (q - 1) * d)}. Find the first term, the common difference and the {ordinal(q + p)} term.',
             f'a = {fn(a)}, d = {fn(d)}, {ordinal(q + p)} term = {fn(a + (q + p - 1) * d)}', f'Subtract: {q - p}d = {fn((q - p) * d)} ⇒ d = {fn(d)}; a = {fn(a)} (4 marks).')


def c8s2_explain(r):
    a, d = ap(r)
    return Q(f'Explain why the nth term of the AP {fn(a)}, {fn(a + d)}, {fn(a + 2 * d)}, … is a linear polynomial in n.', f'aₙ = {lin(d, a - d, "n")}',
             f'aₙ = a + (n − 1)d = {fn(d)}n {signed(a - d)}, degree 1 in n (2 marks).')


def c8s2_ar(r):
    a, d = ap(r)
    return arbank([
        (f'{fn(a)}, {fn(a + d)}, {fn(a + 2 * d)}, {fn(a + 3 * d)} is an AP.', 'In an AP the difference between consecutive terms is constant.', 'a', 'R explains A.'),
        ('1, 4, 9, 16, … is an AP.', 'Each term is a perfect square.', 'd', 'Differences 3, 5, 7 are not constant; A false, R true.'),
        (f'The {ordinal(10)} term of the AP with a = {fn(a)}, d = {fn(d)} is {fn(a + 10 * d)}.', 'aₙ = a + (n − 1)d.', 'd', f'a₁₀ = {fn(a + 9 * d)}; A false, R true.'),
    ])(r)


def c8s2_case(r):
    who = name(r)
    s, inc = r.choice([(15000, 1000), (12000, 800), (18000, 1500), (20000, 1200)])
    y = r.randint(5, 12)
    target = s + inc * r.randint(8, 15)
    return Q((f'{who} joins a job in Pune at a monthly salary of ₹{s:,} with a fixed increment of ₹{inc:,} every year. (i) Write the monthly salary in years 1, 2, 3 as an AP. '
              f'(ii) Find the monthly salary in year {y}. (iii) In which year does the monthly salary first become ₹{target:,}? (iv) Write the nth term.').replace(',', ','),
             f'(i) {s}, {s + inc}, {s + 2 * inc} (ii) {inr(s + (y - 1) * inc)} (iii) year {(target - s) // inc + 1} (iv) {s} + (n − 1){inc}', '1 mark each part.')


# st3 GP

def c8s3_ratio(r):
    a = nz(r, 1, 6)
    q = r.choice([2, 3, -2, -3, Fr(1, 2), Fr(1, 3), 4, 5])
    t = [a * Fr(q) ** i for i in range(4)]
    return mcq(f'The common ratio of the GP {", ".join(fn(x) for x in t)}, … is …', fn(q), [fn(-q), fn(t[1] - t[0]), fn(1 / Fr(q))], 'r = a₂ ÷ a₁.', r)


def c8s3_nth(r):
    a = r.randint(1, 5)
    q = r.choice([2, 3, -2])
    n = r.randint(5, 9)
    return Q(f'Find the {ordinal(n)} term of the GP {a}, {fn(a * q)}, {fn(a * q * q)}, …', fn(a * q ** (n - 1)), f'aₙ = arⁿ⁻¹ = {a} × {bracket(q)}^{n - 1} = {fn(a * q ** (n - 1))}.',
             num_distractors(a * q ** (n - 1), a * q ** n, a * q * (n - 1), a + (n - 1) * q))


def c8s3_which(r):
    a = r.randint(1, 5)
    q = r.choice([2, 3])
    n = r.randint(5, 10)
    return Q(f'Which term of the GP {a}, {a * q}, {a * q * q}, … is {a * q ** (n - 1)}?', f'{ordinal(n)} term', f'{a} × {q}ⁿ⁻¹ = {a * q ** (n - 1)} ⇒ {q}ⁿ⁻¹ = {q ** (n - 1)} = {q}^{n - 1} ⇒ n = {n}.',
             [f'{ordinal(n - 1)} term', f'{ordinal(n + 1)} term', f'{ordinal(2 * n)} term'])


def c8s3_explain(r):
    return xbank([
        ('Explain how to decide whether a sequence is an AP, a GP or neither, using 3, 6, 12, 24, …', 'Differences 3, 6, 12 are not constant (not an AP); ratios are all 2 (a GP).', '2 marks.'),
        ('Explain why 0 cannot be a term of a GP with first term 5.', 'Every term is 5 × rⁿ⁻¹; if a term were 0, then r = 0 and the ratio of the next pair would be undefined.', '2 marks.'),
        ('Explain why a GP with common ratio ½ gets closer and closer to 0 but never reaches it.', 'Each term is half the previous one; halving a positive number never gives 0.', '2 marks.'),
    ])(r)


def c8s3_ar(r):
    q = r.choice([2, 3, 5])
    return arbank([
        (f'1, {q}, {q * q}, {q ** 3}, … is a GP.', 'In a GP the ratio of consecutive terms is constant.', 'a', 'R explains A.'),
        ('2, 4, 6, 8, … is a GP.', 'Each term is 2 more than the previous one.', 'd', 'Ratios 2, 1.5, … are not constant; it is an AP; A false, R true.'),
        (f'The {ordinal(6)} term of the GP 1, {q}, {q * q}, … is {q ** 5}.', 'aₙ = arⁿ⁻¹.', 'a', 'R gives A.'),
    ])(r)


def c8s3_bacteria(r):
    n0 = r.choice([100, 200, 500, 50])
    h = r.choice([20, 30, 60])
    t = r.randint(3, 8)
    return Q(f'A bacteria culture starts with {n0} cells and doubles every {h} minutes. How many cells are there after {t * h} minutes? Write the answer as a GP term.', f'{n0 * 2 ** t}',
             f'Number of doublings = {t}; {n0} × 2^{t} = {n0 * 2 ** t} (3 marks).')


def c8s3_case(r):
    price = r.choice([800000, 500000, 1200000, 600000])
    pct = r.choice([10, 20])
    y = r.randint(3, 5)
    vals = [price * (100 - pct) ** i // 100 ** i for i in range(y + 1)]
    return Q((f'A car bought for {inr(price)} loses {pct}% of its value every year. (i) Show that its values at the start of each year form a GP and state the common ratio. '
              f'(ii) Find its value after 2 years. (iii) Find its value after {y} years. (iv) Will its value ever become 0? Explain.'),
             f'(i) r = {fn(Fr(100 - pct, 100))} (ii) {inr(vals[2])} (iii) {inr(vals[y])} (iv) no; multiplying by {fn(Fr(100 - pct, 100))} never gives 0', '1 mark each part.')


# st4 figurate and fractals

def c8s4_triangular(r):
    n = r.randint(5, 30)
    return Q(f'Triangular numbers are 1, 3, 6, 10, … Find the {ordinal(n)} triangular number.', str(n * (n + 1) // 2), f'Tₙ = n(n + 1)/2 = {n} × {n + 1}/2 = {n * (n + 1) // 2}.',
             num_distractors(n * (n + 1) // 2, n * n, n * (n - 1) // 2, n * (n + 1)))


def c8s4_mcq(r):
    return mcqbank([
        ('The sum of two consecutive triangular numbers is always …', 'a square number', ['a triangular number', 'a prime number', 'an odd number'], 'Tₙ + Tₙ₊₁ = (n + 1)².'),
        ('In the Sierpinski triangle, each step replaces every shaded triangle by …', '3 smaller shaded triangles', ['4 smaller triangles', '2 smaller triangles', '9 smaller triangles'], 'The middle quarter is removed.'),
        ('In the Koch snowflake, each side is replaced at the next step by …', '4 segments, each one-third as long', ['3 segments, each half as long', '2 segments of equal length', '4 segments, each half as long'], 'Middle third replaced by two sides of an equilateral triangle.'),
        ('The sum of the first n odd numbers is …', 'n²', ['n(n + 1)/2', '2n − 1', 'n(n + 1)'], 'Square numbers from odd numbers.'),
    ])(r)


def c8s4_sier(r):
    n = r.randint(2, 7)
    return Q(f'In the Sierpinski triangle, step 0 is one shaded triangle and each step replaces every shaded triangle by 3 smaller ones. How many shaded triangles are there at step {n}?', str(3 ** n),
             f'GP with ratio 3: 3^{n} = {3 ** n}.', num_distractors(3 ** n, 3 * n, 4 ** n, 3 ** (n - 1)))


def c8s4_koch(r):
    n = r.randint(1, 4)
    return Q(f'The Koch snowflake starts as an equilateral triangle (3 sides). Each step replaces every side by 4 smaller sides. How many sides are there after {n} step{"s" if n > 1 else ""}? What happens to the length of each side?',
             f'{3 * 4 ** n} sides, each (1/3)^{n} of the original', f'3 × 4^{n} = {3 * 4 ** n}; side length is divided by 3 at each step (3 marks).')


def c8s4_explain(r):
    n = r.randint(3, 9)
    return Q(f'Explain, using a dot picture, why the {ordinal(n)} square number is the sum of the first {n} odd numbers.', f'{n}² = 1 + 3 + … + {2 * n - 1}',
             'Each new L-shaped layer around a k × k square adds 2k + 1 dots (2 marks).')


def c8s4_ar(r):
    n = r.randint(3, 15)
    return arbank([
        (f'T{n} + T{n + 1} = {(n + 1) ** 2}, where Tₖ is the kth triangular number.', 'The sum of two consecutive triangular numbers is a square number.', 'a', f'{n * (n + 1) // 2} + {(n + 1) * (n + 2) // 2} = {(n + 1) ** 2}.'),
        ('The number of shaded triangles in the Sierpinski triangle forms an AP.', 'Each step multiplies the number of shaded triangles by 3.', 'd', 'It is a GP 1, 3, 9, …; A false, R true.'),
    ])(r)


def c8s4_case(r):
    k = r.randint(4, 8)
    return Q((f'A school stacks cans for a display: 1 can on top, 2 in the next row, 3 in the next, and so on. (i) How many cans are needed for {k} rows? '
              f'(ii) Write a formula for n rows. (iii) Can a full display use exactly 50 cans? (iv) What is the largest number of complete rows possible with 100 cans?'),
             f'(i) {k * (k + 1) // 2} (ii) n(n + 1)/2 (iii) no; 45 and 55 are consecutive triangular numbers (iv) 13 rows (91 cans)', 'Triangular numbers (1 mark each part).')


# ---------------- ch09 Propositions and converses ----------------

# (subject, P, Q, not P, not Q, statement true?, converse true?)
CONDS = [
    ('a number', 'is divisible by 6', 'is divisible by 3', 'is not divisible by 6', 'is not divisible by 3', True, False),
    ('a quadrilateral', 'is a square', 'has equal diagonals', 'is not a square', 'does not have equal diagonals', True, False),
    ('two angles', 'are vertically opposite', 'are equal', 'are not vertically opposite', 'are not equal', True, False),
    ('a triangle', 'is equilateral', 'has all its angles equal to 60°', 'is not equilateral', 'does not have all its angles equal to 60°', True, True),
    ('a number', 'ends in 0', 'is divisible by 5', 'does not end in 0', 'is not divisible by 5', True, False),
    ('a quadrilateral', 'is a rectangle', 'is a parallelogram', 'is not a rectangle', 'is not a parallelogram', True, False),
    ('two distinct lines in a plane', 'are parallel', 'do not meet', 'are not parallel', 'meet', True, True),
    ('an integer n', 'is even', 'has an even square', 'is odd', 'has an odd square', True, True),
    ('a triangle', 'has two equal sides', 'has two equal angles', 'does not have two equal sides', 'does not have two equal angles', True, True),
    ('a number', 'is prime', 'is odd', 'is not prime', 'is even', False, False),
    ('a number', 'is a multiple of 4', 'is even', 'is not a multiple of 4', 'is odd', True, False),
    ('a quadrilateral', 'is a rhombus', 'has perpendicular diagonals', 'is not a rhombus', 'does not have perpendicular diagonals', True, False),
]


def _st(c, p, q):
    """'If <subject> <p>, then <pronoun> <q>.'"""
    pron = 'they' if c[0].startswith('two') else 'it'
    qq = q
    if pron == 'it':
        qq = q.replace('are ', 'is ', 1) if q.startswith('are ') else q
    return f'If {c[0]} {p}, then {pron} {qq}.'


def c9s1_mcq(r):
    return mcqbank([
        ('Which of the following is a proposition?', 'The sum of the angles of a triangle is 180°.', ['Close the door.', 'What a beautiful day!', 'Is 7 a prime number?'], 'A proposition is a statement that is either true or false.'),
        ('Which of the following is NOT a proposition?', 'Please solve this problem.', ['7 is an odd number.', '2 + 3 = 6.', 'Every square is a rectangle.'], 'Commands are neither true nor false.'),
        ('In "If a number is divisible by 9, then it is divisible by 3", the hypothesis is …', 'a number is divisible by 9', ['it is divisible by 3', 'divisible by 27', 'the number is 3'], 'The "if" part is the hypothesis.'),
        ('The truth value of "Every rectangle is a square" is …', 'false', ['true', 'sometimes true', 'not a proposition'], 'A 2 × 3 rectangle is not a square.'),
        ('"x + 2 = 5" is …', 'not a proposition until x is known', ['always true', 'always false', 'a definition'], 'Its truth depends on x (an open sentence).'),
    ])(r)


def c9s1_truth(r):
    st = r.choice([('The square of every odd number is odd.', 'True'), ('Every prime number is odd.', 'False'), ('The sum of two even numbers is even.', 'True'),
                   ('Every rhombus is a square.', 'False'), ('√2 is a rational number.', 'False'), ('Every square is a rhombus.', 'True'),
                   ('The product of two negative numbers is negative.', 'False'), ('A triangle can have two right angles.', 'False'),
                   ('Every integer is a rational number.', 'True'), ('The diagonals of a rectangle are equal.', 'True')])
    return Q(f'State whether the proposition is true or false: "{st[0]}"', st[1], 'Check with the definition or a counterexample.', ['False' if st[1] == 'True' else 'True', 'Not a proposition', 'Sometimes true'])


def c9s1_hyp(r):
    c = r.choice(CONDS)
    return Q(f'Identify the hypothesis and the conclusion in: "{_st(c, c[1], c[2])}"', f'Hypothesis: {c[0]} {c[1]}; conclusion: it {c[2]}' if not c[0].startswith('two') else f'Hypothesis: {c[0]} {c[1]}; conclusion: they {c[2]}',
             'The "if" part is the hypothesis; the "then" part is the conclusion.',
             [f'Hypothesis: {c[0]} {c[2]}; conclusion: {c[0]} {c[1]}', f'Hypothesis: {c[0]} {c[3]}; conclusion: {c[0]} {c[4]}', f'Hypothesis: the whole statement; conclusion: none'])


def c9s1_explain(r):
    return xbank([
        ('Explain why "x > 5" is not a proposition but "For every natural number x, x > 5" is.', 'The first depends on x; the second has a definite truth value (false, e.g. x = 1).', '2 marks.'),
        ('Explain why the statement "This sentence is false" causes trouble if we call it a proposition.', 'If it is true then it is false, and if false then true; no definite truth value.', '2 marks.'),
        ('Rewrite "All squares are rectangles" as an if-then statement and state its truth value.', 'If a quadrilateral is a square, then it is a rectangle. True.', '2 marks.'),
    ])(r)


def c9s1_ar(r):
    return arbank([
        ('"7 is a prime number" is a proposition.', 'A proposition is a sentence that is either true or false, but not both.', 'a', 'R explains A.'),
        ('"Shut the window" is not a proposition.', 'A command cannot be true or false.', 'a', 'R explains A.'),
        ('The statement "If a number is odd, then it is prime" is true.', 'A single counterexample is enough to show an if-then statement is false.', 'd', '9 is odd and not prime; A false, R true.'),
    ])(r)


def c9s1_case(r):
    n = r.randint(12, 40)
    return Q((f'A maths club notice says: "If a number is divisible by 4 and by 6, then it is divisible by 24." (i) Identify the hypothesis and the conclusion. '
              f'(ii) Test it with 12. (iii) Is the statement true or false? (iv) Correct the conclusion so that the statement becomes true.'),
             '(i) H: divisible by 4 and 6; C: divisible by 24 (ii) 12 is divisible by 4 and 6 but not by 24 (iii) false (iv) "… then it is divisible by 12" (LCM of 4 and 6)', '1 mark each part.')


# st2 converse, inverse, contrapositive

def c9s2_converse(r):
    c = r.choice(CONDS)
    t, ct = c[5], c[6]
    T = lambda b: 'True' if b else 'False'
    return Q(f'Write the converse of "{_st(c, c[1], c[2])}" Is the converse true?', f'{_st(c, c[2], c[1])} ({T(ct)})',
             'Swap the hypothesis and the conclusion; test with an example or a counterexample.',
             [f'{_st(c, c[3], c[4])} ({T(ct)})', f'{_st(c, c[4], c[3])} ({T(t)})', f'{_st(c, c[2], c[1])} ({T(not ct)})'])


def c9s2_mcq(r):
    return mcqbank([
        ('The contrapositive of "If p, then q" is …', 'If not q, then not p', ['If q, then p', 'If not p, then not q', 'If p, then not q'], 'Negate and swap.'),
        ('The inverse of "If p, then q" is …', 'If not p, then not q', ['If q, then p', 'If not q, then not p', 'p and not q'], 'Negate both parts.'),
        ('A statement and its … always have the same truth value.', 'contrapositive', ['converse', 'inverse', 'negation'], 'Logically equivalent.'),
        ('The converse and the … of a statement always have the same truth value.', 'inverse', ['contrapositive', 'statement itself', 'negation'], 'The inverse is the contrapositive of the converse.'),
    ])(r)


def c9s2_contra(r):
    c = r.choice(CONDS)
    return Q(f'Write the contrapositive of "{_st(c, c[1], c[2])}" What is its truth value?', f'{_st(c, c[4], c[3])} ({"True" if c[5] else "False"})',
             'Negate both parts and swap them; the contrapositive has the same truth value as the original statement.')


def c9s2_explain(r):
    c = r.choice([c for c in CONDS if c[5] and not c[6]])
    return Q(f'"{_st(c, c[1], c[2])}" is true. Explain with an example why its converse is not necessarily true.', f'Converse: "{_st(c, c[2], c[1])}" is false.',
             'State the converse (1) and give a counterexample that satisfies its hypothesis but not its conclusion (1).')


def c9s2_ar(r):
    c = r.choice([c for c in CONDS if c[5] and not c[6]])
    return arbank([
        (f'The converse of "{_st(c, c[1], c[2])}" is false.', 'The converse of a true statement need not be true.', 'a', 'A counterexample to the converse exists; R explains why this is possible.'),
        ('A statement and its contrapositive have the same truth value.', 'The contrapositive is obtained by negating and swapping the hypothesis and conclusion.', 'b', 'Both true, but the bare description in R does not explain the equivalence.'),
        ('The inverse of a true statement is always true.', 'The inverse has the same truth value as the converse.', 'd', 'A false, R true.'),
    ])(r)


def c9s2_case(r):
    c = r.choice(CONDS)
    t, ct = c[5], c[6]
    T = lambda b: 'T' if b else 'F'
    return Q((f'Consider S: "{_st(c, c[1], c[2])}" (i) Write the converse. (ii) Write the inverse. (iii) Write the contrapositive. '
              f'(iv) Give the truth value of each of S, the converse, the inverse and the contrapositive.'),
             f'(i) {_st(c, c[2], c[1])} (ii) {_st(c, c[3], c[4])} (iii) {_st(c, c[4], c[3])} (iv) S: {T(t)}, converse: {T(ct)}, inverse: {T(ct)}, contrapositive: {T(t)}',
             '1 mark each part; the inverse matches the converse and the contrapositive matches S.')


def c9s2_biconditional(r):
    c = r.choice([c for c in CONDS if c[5] and c[6]])
    return Q(f'Both "{_st(c, c[1], c[2])}" and its converse are true. Combine them into one "if and only if" statement.', f'{c[0][0].upper() + c[0][1:]} {c[1]} if and only if {"they" if c[0].startswith("two") else "it"} {c[2]}.',
             'A true statement with a true converse gives a biconditional (2 marks).')


# st3 lines and angles

def c9s3_vert(r):
    x = r.randint(20, 160)
    return Q(f'Two lines intersect. One of the four angles formed is {x}°. Find the other three angles.', f'{180 - x}°, {x}°, {180 - x}°',
             'Vertically opposite angles are equal; a linear pair adds to 180°.', [f'{x}°, {x}°, {x}°', f'{90 - x if x < 90 else x - 90}°, {x}°, {180 - x}°', f'{360 - x}°, {x}°, {180 - x}°'])


def c9s3_linear(r):
    a, b = r.randint(2, 7), r.randint(1, 5)
    c = r.randint(0, 20)
    x = Fr(180 - c, a + b)
    if x.denominator != 1:
        raise ValueError
    return Q(f'Two angles forming a linear pair are ({a}x {signed(c)})° and {b}x°. Find x and both angles.', f'x = {fn(x)}; {fn(a * x + c)}° and {fn(b * x)}°',
             f'{a}x {signed(c)} + {b}x = 180 ⇒ x = {fn(x)}.', [f'x = {fn(x + 2)}; {fn(a * (x + 2) + c)}° and {fn(b * (x + 2))}°', f'x = {fn(Fr(90 - c, a + b))}', f'x = {fn(Fr(180 + c, a + b))}'])


def c9s3_parallel(r):
    x = r.randint(35, 145)
    which = r.choice(['alternate interior', 'corresponding', 'co-interior (same side interior)'])
    ans = 180 - x if which.startswith('co') else x
    return Q(f'A transversal cuts two parallel lines. One angle is {x}°. Find the {which} angle to it.', f'{ans}°',
             'Alternate and corresponding angles are equal; co-interior angles add to 180°.', [f'{180 - ans}°', f'{90 + x if x < 90 else x - 90}°', f'{360 - ans}°'])


def c9s3_mcq(r):
    return mcqbank([
        ('A statement accepted as true without proof is called …', 'an axiom', ['a theorem', 'a converse', 'a counterexample'], 'Axioms (postulates) are assumed.'),
        ('A statement that is proved using axioms and earlier results is called …', 'a theorem', ['an axiom', 'a definition', 'a hypothesis'], 'Definition.'),
        ("Euclid's fifth postulate is equivalent to …", "Playfair's axiom: through a point not on a line there is exactly one parallel", ['vertically opposite angles are equal', 'all right angles are equal', 'a line can be extended indefinitely'], 'The parallel postulate.'),
        ('If a transversal makes alternate interior angles equal, then the lines are …', 'parallel', ['perpendicular', 'intersecting at 60°', 'coincident'], 'Converse of the alternate-angles theorem.'),
    ])(r)


def c9s3_explain(r):
    return xbank([
        ('Prove that vertically opposite angles are equal.', '∠1 + ∠2 = 180° and ∠2 + ∠3 = 180° (linear pairs) ⇒ ∠1 = ∠3.', 'Two linear pairs (1), conclusion (1).'),
        ('Prove that the angles of a triangle add up to 180°, using a line through one vertex parallel to the opposite side.', 'Alternate angles transfer the two base angles to the vertex, where the three angles form a straight angle.', '3 marks.'),
        ('Explain the difference between an axiom and a theorem with one example of each.', 'Axiom assumed (e.g. a straight line can be drawn between two points); theorem proved (e.g. vertically opposite angles are equal).', '2 marks.'),
    ])(r)


def c9s3_ar(r):
    x = r.randint(30, 150)
    return arbank([
        (f'If two parallel lines are cut by a transversal and one interior angle is {x}°, the co-interior angle on the same side is {180 - x}°.', 'Co-interior angles on the same side of a transversal through parallel lines are supplementary.', 'a', 'R explains A.'),
        ('Vertically opposite angles are equal.', 'Angles in a linear pair add up to 180°.', 'a', 'The proof uses two linear pairs.'),
        ('An exterior angle of a triangle equals the sum of all three interior angles.', 'The angles of a triangle add up to 180°.', 'd', 'It equals the sum of the two interior opposite angles; A false, R true.'),
    ])(r)


def c9s3_tri(r):
    a, b = r.randint(30, 80), r.randint(30, 80)
    return Q(f'In △ABC, ∠A = {a}° and ∠B = {b}°. Side BC is produced to D. Find ∠ACD and ∠ACB.', f'∠ACD = {a + b}°, ∠ACB = {180 - a - b}°',
             'Exterior angle = sum of interior opposite angles; linear pair (3 marks).')


def c9s3_zigzag(r):
    a, b = r.randint(25, 70), r.randint(25, 70)
    return Q(f'AB ∥ CD. A point E lies between the lines. ∠BAE = {a}° and ∠DCE = {b}°, with E on the same side. Find ∠AEC, giving reasons.', f'{a + b}°',
             f'Draw EF ∥ AB through E: ∠AEF = {a}° and ∠FEC = {b}° (alternate angles); sum {a + b}° (4 marks).')


# st4 counterexamples and contradiction

def c9s4_counter(r):
    claims = [
        ('Every prime number is odd.', '2'), ('n² + n + 41 is prime for every whole number n.', 'n = 40 gives 41²'), ('The sum of two irrational numbers is irrational.', '√2 + (−√2) = 0'),
        ('For every integer n, n² > n.', 'n = 1 (or 0)'), ('Every quadrilateral with four equal sides is a square.', 'a rhombus with angles 60° and 120°'), ('If a² = b², then a = b.', 'a = 3, b = −3'),
        ('The product of two irrational numbers is irrational.', '√2 × √2 = 2'), ('Every number of the form 2ⁿ − 1 is prime.', 'n = 4: 15'), ('Any two right triangles with one equal side are congruent.', 'legs 3, 4 and 3, 5'),
        ('Every multiple of 3 is odd.', '6'),
    ]
    c, x = r.choice(claims)
    return Q(f'Give a counterexample to the claim: "{c}"', x, 'One example where the hypothesis holds but the conclusion fails disproves the claim (1 mark).')


def c9s4_mcq(r):
    return mcqbank([
        ('To show that a general statement is false, it is enough to give …', 'one counterexample', ['two examples where it is true', 'a proof by induction', 'a diagram'], 'One failure disproves "for all".'),
        ('Which number is a counterexample to "every odd number is prime"?', '9', ['7', '3', '11'], '9 = 3 × 3.'),
        ('In a proof by contradiction we begin by …', 'assuming the statement is false', ['assuming the statement is true', 'giving an example', 'drawing a figure'], 'Then reach a contradiction.'),
        ('Which is a counterexample to "if x² > 4 then x > 2"?', 'x = −3', ['x = 3', 'x = 1', 'x = 2'], '(−3)² = 9 > 4 but −3 < 2.'),
    ])(r)


def c9s4_explain(r):
    return xbank([
        ('Prove by contradiction that there is no largest natural number.', 'Suppose N is the largest; then N + 1 is a natural number larger than N, a contradiction.', '2 marks.'),
        ('Prove by contradiction that a triangle cannot have two right angles.', 'If two angles are 90°, the third is 180° − 180° = 0°, impossible.', '2 marks.'),
        ('Prove by contradiction that if n² is even then n is even.', 'If n were odd, n = 2k + 1 and n² = 4k² + 4k + 1 is odd, a contradiction.', '3 marks.'),
        ('Explain why checking a statement for 100 examples does not prove it.', 'A counterexample might exist beyond the cases checked (e.g. n² + n + 41 works up to n = 39).', '2 marks.'),
    ])(r)


def c9s4_ar(r):
    return arbank([
        ('The statement "every prime is odd" is false.', '2 is a prime number that is even.', 'a', 'R is a counterexample.'),
        ('Verifying a statement for many examples proves it.', 'A single counterexample disproves a general statement.', 'd', 'Examples cannot prove a general statement; A false, R true.'),
        ('√2 is irrational.', 'Assuming √2 = p/q in lowest terms leads to p and q both being even.', 'a', 'This contradiction is the proof.'),
    ])(r)


def c9s4_n2(r):
    f = r.choice([('n² − n + 11', lambda n: n * n - n + 11, 11), ('n² + n + 17', lambda n: n * n + n + 17, 16), ('2n² + 29', lambda n: 2 * n * n + 29, 29)])
    n = f[2]
    v = f[1](n)
    return Q(f'A student checks that {f[0]} is prime for n = 1, 2, 3, 4, 5 and claims it is prime for every natural number n. Find a counterexample.', f'n = {n}: {v}',
             f'At n = {n}, {f[0]} = {v}, which is composite (divisible by {[d for d in range(2, v) if v % d == 0][0]}) (3 marks).')


def c9s4_case(r):
    who = name(r)
    return Q((f'{who} claims: "For any two numbers a and b, if a > b then a² > b²." (i) Test the claim with a = 5, b = 3. (ii) Test it with a = 1, b = −4. '
              f'(iii) Is the claim true? (iv) Add a condition on a and b that makes it true, and justify.'),
             '(i) 25 > 9, holds (ii) 1 < 16, fails (iii) false; (ii) is a counterexample (iv) if a > b ≥ 0 then a² − b² = (a − b)(a + b) > 0',
             '1 mark each part.')


# st5 congruence

def c9s5_crit(r):
    c = r.choice([('AB = PQ, BC = QR, CA = RP', 'SSS'), ('AB = PQ, ∠B = ∠Q, BC = QR', 'SAS'), ('∠A = ∠P, AB = PQ, ∠B = ∠Q', 'ASA'),
                  ('∠B = ∠Q = 90°, hypotenuse AC = PR, side AB = PQ', 'RHS'), ('∠A = ∠P, ∠B = ∠Q, BC = QR', 'AAS')])
    return mcq(f'In △ABC and △PQR, {c[0]}. The triangles are congruent by …', c[1], [x for x in ['SSS', 'SAS', 'ASA', 'RHS', 'AAS'] if x != c[1]][:3], f'{c[1]} criterion.', r)


def c9s5_mcq(r):
    return mcqbank([
        ('Which of these is NOT a congruence criterion for triangles?', 'SSA', ['SSS', 'SAS', 'RHS'], 'Two sides and a non-included angle do not fix a triangle.'),
        ('In an isosceles triangle, the angles opposite the equal sides are …', 'equal', ['supplementary', 'complementary', 'right angles'], 'Theorem.'),
        ('CPCT stands for …', 'corresponding parts of congruent triangles', ['congruent parts of corresponding triangles', 'common perpendicular to chords', 'corresponding perimeters of congruent triangles'], 'Used after proving congruence.'),
        ('AAA is not a congruence criterion because …', 'triangles with equal angles can have different sizes', ['angles cannot be equal', 'it is the same as SSS', 'it only works for right triangles'], 'Similar, not necessarily congruent.'),
    ])(r)


def c9s5_isos(r):
    v = r.randint(20, 140)
    if v % 2:
        v += 1
    return Q(f'In △ABC, AB = AC and ∠A = {v}°. Find ∠B and ∠C.', f'{(180 - v) // 2}° each', f'∠B = ∠C (angles opposite equal sides); 2∠B = 180° − {v}°.',
             [f'{v}° each', f'{180 - v}° each', f'{90 - v // 2 + 10}° each'])


def c9s5_explain(r):
    return xbank([
        ('In △ABC, AD is the bisector of ∠A and AB = AC. Prove that BD = DC.', '△ABD ≅ △ACD by SAS (AB = AC, ∠BAD = ∠CAD, AD common) ⇒ BD = DC (CPCT).', '3 marks.'),
        ('Explain with a sketch why SSA does not guarantee congruence.', 'With two sides and a non-included angle, the third side can swing to two positions giving two different triangles.', '2 marks.'),
        ('Lines l and m are parallel and P is the mid-point of AB, where A is on l and B on m. A line through P meets l at C and m at D. Prove that P is the mid-point of CD.', '△APC ≅ △BPD (ASA/AAS: alternate angles, vertically opposite angles, AP = BP) ⇒ PC = PD.', '3 marks.'),
    ])(r)


def c9s5_ar(r):
    return arbank([
        ('Two triangles with all three angles equal need not be congruent.', 'Equal angles fix the shape but not the size of a triangle.', 'a', 'R explains A.'),
        ('Two right triangles with equal hypotenuses and one pair of equal sides are congruent.', 'RHS is a congruence criterion.', 'a', 'R explains A.'),
        ('In △ABC, if AB = AC then ∠B = ∠C.', 'Angles opposite equal sides of a triangle are equal.', 'a', 'R is the theorem.'),
        ('SSA is a valid congruence criterion.', 'SAS is a valid congruence criterion.', 'd', 'A false, R true.'),
    ])(r)


def c9s5_cpct(r):
    a, b = r.randint(30, 80), r.randint(5, 15)
    return Q(f'△ABC ≅ △PQR with AB = PQ = {b} cm, ∠A = ∠P = {a}° and AC = PR. If ∠B = {r.randint(40, 180 - a - 20)}°, which angle of △PQR equals ∠B and why? Also find PQ.', f'∠Q, by CPCT; PQ = {b} cm',
             'Correspondence A ↔ P, B ↔ Q, C ↔ R (SAS) and CPCT (2 marks).')


def c9s5_prove(r):
    return xbank([
        ('ABCD is a quadrilateral with AB = AD and CB = CD. Prove that AC bisects ∠A.', '△ABC ≅ △ADC (SSS) ⇒ ∠BAC = ∠DAC (CPCT).', 'SSS (3 marks), CPCT (2 marks).'),
        ('In △ABC, BE and CF are altitudes and BE = CF. Prove that △ABC is isosceles.', '△BEC ≅ △CFB (RHS: BC common, BE = CF) ⇒ ∠B = ∠C ⇒ AB = AC.', 'RHS (3 marks), CPCT and conclusion (2 marks).'),
        ('Prove that the angles opposite the equal sides of an isosceles triangle are equal.', 'Draw the bisector AD of ∠A; △ABD ≅ △ACD (SAS) ⇒ ∠B = ∠C.', 'Construction (1), SAS (3), CPCT (1).'),
        ('P is a point on the bisector of ∠ABC. PM ⟂ BA and PN ⟂ BC. Prove that PM = PN.', '△PMB ≅ △PNB (AAS: ∠PMB = ∠PNB = 90°, ∠PBM = ∠PBN, PB common) ⇒ PM = PN.', 'AAS (3 marks), CPCT (2 marks).'),
    ])(r)


def c9s5_case(r):
    s = r.randint(4, 12)
    a = r.choice([40, 50, 60, 70])
    return Q((f'Two triangular ramps at a school entrance are designed with the same base {s} m, the same slope angle {a}° at the base and the same height. '
              f'(i) Which congruence criterion shows the ramps are congruent? (ii) If one ramp\'s sloping side is measured, why does the other have the same length? '
              f'(iii) If only the three angles were the same, could the ramps differ? (iv) Name one more pair of measurements that would also guarantee congruence.'),
             '(i) ASA (base angle, base, right angle at the far end) or SAS (ii) CPCT (iii) yes; AAA gives the same shape but possibly a different size (iv) e.g. base and height with the right angle (SAS)',
             '1 mark each part.')


# ---------------- ch10 Data ----------------

def rand_data(r, n=None, lo=10, hi=60):
    n = n or r.randint(7, 11)
    return [r.randint(lo, hi) for _ in range(n)]


def c10s1_classmark(r):
    lo = r.choice([10, 20, 30, 40, 50, 100, 150])
    w = r.choice([5, 10, 20])
    return Q(f'Find the class mark of the class interval {lo}–{lo + w}.', num((2 * lo + w) / 2), f'Class mark = (lower + upper)/2 = ({lo} + {lo + w})/2 = {num((2 * lo + w) / 2)}.',
             [str(w), str(lo + w), num((2 * lo + w) / 4)])


def c10s1_mcq(r):
    return mcqbank([
        ('In the class interval 20–30 (exclusive form), the value 30 is counted in …', 'the class 30–40', ['the class 20–30', 'both classes', 'neither class'], 'The upper limit belongs to the next class.'),
        ('The difference between the upper and lower limits of a class is called the …', 'class size (width)', ['class mark', 'frequency', 'range'], 'Definition.'),
        ('The number of times an observation occurs is its …', 'frequency', ['class mark', 'range', 'mean'], 'Definition.'),
        ('The range of the data 12, 45, 7, 33, 28 is …', '38', ['45', '33', '7'], '45 − 7.'),
        ('Data collected by the investigator directly is called …', 'primary data', ['secondary data', 'grouped data', 'raw frequency'], 'Definition.'),
    ])(r)


def c10s1_count(r):
    data = rand_data(r, r.randint(15, 20), 0, 49)
    lo = r.choice([0, 10, 20, 30, 40])
    k = sum(1 for x in data if lo <= x < lo + 10)
    return Q(f'The marks (out of 50) of a group of students are: {", ".join(map(str, data))}. How many students scored in the class {lo}–{lo + 10} (lower limit included, upper limit excluded)?', str(k),
             f'Count values {lo} ≤ x < {lo + 10}: {k}.', num_distractors(k, k + 1, k - 1 if k else 2, k + 2))


def c10s1_explain(r):
    return xbank([
        ('Explain why grouped frequency tables are used for large data sets, and one disadvantage.', 'They summarise many values into a few classes; individual values are lost.', '2 marks.'),
        ('Why must class intervals not overlap in a frequency table?', 'Each observation must be counted in exactly one class.', '2 marks.'),
        ('Explain the difference between primary and secondary data with an example of each.', 'Primary: collected first-hand (survey of classmates); secondary: from another source (census tables).', '2 marks.'),
    ])(r)


def c10s1_ar(r):
    return arbank([
        ('The class mark of 40–50 is 45.', 'The class mark is the mid-point of a class interval.', 'a', 'R explains A.'),
        ('In the classes 10–20, 20–30, the observation 20 is counted in both classes.', 'In exclusive classes the upper limit is not included in the class.', 'd', '20 goes only to 20–30; A false, R true.'),
        ('The range of a data set tells us how spread out the data is.', 'Range = maximum value − minimum value.', 'a', 'R explains A.'),
    ])(r)


def c10s1_table(r):
    data = rand_data(r, 20, 0, 39)
    counts = [sum(1 for x in data if 10 * i <= x < 10 * i + 10) for i in range(4)]
    return Q((f'The number of minutes 20 students of a class in Patna spent reading on a day are: {", ".join(map(str, data))}. '
              f'(i) Make a grouped frequency table with classes 0–10, 10–20, 20–30, 30–40. (ii) Which class has the highest frequency? (iii) How many students read for at least 20 minutes?'),
             f'(i) {", ".join(f"{10 * i}–{10 * i + 10}: {c}" for i, c in enumerate(counts))} (ii) {10 * counts.index(max(counts))}–{10 * counts.index(max(counts)) + 10} (iii) {counts[2] + counts[3]}',
             'Tally into classes (2), mode class (1), add frequencies (1).')


def c10s1_inclusive(r):
    lo = r.choice([10, 20, 30, 50])
    return Q(f'Convert the inclusive classes {lo}–{lo + 9}, {lo + 10}–{lo + 19}, {lo + 20}–{lo + 29} into exclusive (continuous) classes.', f'{lo - 0.5}–{lo + 9.5}, {lo + 9.5}–{lo + 19.5}, {lo + 19.5}–{lo + 29.5}',
             'Gap between classes = 1; subtract 0.5 from each lower limit and add 0.5 to each upper limit (3 marks).')


# st2 graphs

def c10s2_mcq(r):
    return mcqbank([
        ('In a histogram, the class intervals are shown on …', 'the horizontal axis, with no gaps between bars', ['the vertical axis', 'the horizontal axis with equal gaps between bars', 'a pie chart'], 'Histograms show continuous classes.'),
        ('A frequency polygon is drawn by joining …', 'the mid-points of the tops of the histogram bars', ['the corners of the bars', 'the class limits', 'the frequencies on the x-axis'], 'Use class marks against frequencies.'),
        ('In a bar graph, the bars …', 'have equal widths and equal gaps between them', ['touch each other', 'have widths proportional to frequency', 'must be vertical only'], 'Bar graphs show discrete categories.'),
        ('For a histogram with unequal class widths, the heights of the rectangles should be proportional to …', 'frequency ÷ class width (frequency density)', ['frequency', 'class mark', 'cumulative frequency'], 'So that areas represent frequencies.'),
    ])(r)


def c10s2_adjust(r):
    w0 = r.choice([5, 10])
    w = w0 * r.choice([2, 3, 4])
    f = w // w0 * r.randint(2, 12)
    return Q(f'In a histogram, the minimum class width is {w0}. A class of width {w} has frequency {f}. What is the adjusted frequency (height) for this class?', num(f * w0 / w),
             f'Adjusted frequency = ({w0}/{w}) × {f} = {num(f * w0 / w)}.', [str(f), num(f * w / w0), num(f / 2)])


def c10s2_poly(r):
    lo = r.choice([0, 10, 20, 30])
    w = r.choice([10, 20])
    k = r.randint(4, 6)
    marks = [lo + w * i + w / 2 for i in range(k)]
    return Q(f'For classes {lo}–{lo + w}, {lo + w}–{lo + 2 * w}, … ({k} classes), list the x-values used to plot a frequency polygon, including the two extra points on the axis.',
             ', '.join(num(m) for m in [marks[0] - w] + marks + [marks[-1] + w]), f'Class marks plus one class mark before and after (frequency 0) (2 marks).')


def c10s2_read(r):
    cats = r.sample(['Cricket', 'Football', 'Kabaddi', 'Hockey', 'Badminton', 'Chess'], 4)
    vals = [r.randint(5, 40) for _ in cats]
    i, j = r.sample(range(4), 2)
    return Q(f'A bar graph shows the number of students who like each sport: {", ".join(f"{c} {v}" for c, v in zip(cats, vals))}. How many more students like {cats[i]} than {cats[j]}?' if vals[i] > vals[j] else
             f'A bar graph shows the number of students who like each sport: {", ".join(f"{c} {v}" for c, v in zip(cats, vals))}. How many fewer students like {cats[i]} than {cats[j]}?', str(abs(vals[i] - vals[j])),
             f'|{vals[i]} − {vals[j]}| = {abs(vals[i] - vals[j])}.', num_distractors(abs(vals[i] - vals[j]), vals[i] + vals[j], max(vals), abs(vals[i] - vals[j]) + 2))


def c10s2_explain(r):
    return xbank([
        ('Explain the difference between a bar graph and a histogram.', 'A bar graph shows separate categories with gaps; a histogram shows continuous class intervals with no gaps, area ∝ frequency.', '2 marks.'),
        ('Explain why heights must be adjusted when a histogram has unequal class widths.', 'Wider classes would look larger; the area, not the height, must show frequency.', '2 marks.'),
        ('Explain how a frequency polygon can be drawn without first drawing a histogram.', 'Plot (class mark, frequency) for each class and join the points with straight lines, closing at the class marks before and after.', '2 marks.'),
    ])(r)


def c10s2_ar(r):
    return arbank([
        ('In a histogram, there are no gaps between the bars.', 'A histogram represents continuous class intervals.', 'a', 'R explains A.'),
        ('A frequency polygon uses class limits on the x-axis.', 'In a frequency polygon each class is represented by its class mark.', 'd', 'Class marks are used; A false, R true.'),
        ('In a histogram with unequal widths, the area of each rectangle represents the frequency.', 'Height is taken as frequency density.', 'a', 'Height × width = frequency.'),
    ])(r)


def c10s2_case(r):
    classes = [(140, 145), (145, 150), (150, 160), (160, 170), (170, 180)]
    f = [r.randint(3, 10), r.randint(5, 12), r.randint(8, 20), r.randint(6, 18), r.randint(2, 8)]
    adj = [num(f[i] * 5 / (classes[i][1] - classes[i][0])) for i in range(5)]
    return Q((f'The heights (cm) of students of Class 9 in a school in Bhopal: ' + ', '.join(f'{a}–{b}: {x}' for (a, b), x in zip(classes, f)) +
              '. (i) Which classes have unequal widths? (ii) Find the adjusted heights of the bars, taking width 5 as standard. (iii) Find the class marks. (iv) How many students are 150 cm or taller?'),
             f'(i) 150–160, 160–170, 170–180 (width 10) (ii) {", ".join(adj)} (iii) 142.5, 147.5, 155, 165, 175 (iv) {f[2] + f[3] + f[4]}',
             '1 mark each part.')


# st3 mean, median, mode

def c10s3_mean(r):
    d = rand_data(r, r.randint(5, 9), 5, 60)
    m = Fr(sum(d), len(d))
    return Q(f'Find the mean of {", ".join(map(str, d))}.', fn(m) if m.denominator == 1 else num(float(m), 2), f'Sum = {sum(d)}, n = {len(d)}; mean = {sum(d)}/{len(d)} = {num(float(m), 2)}.',
             [num(float(m) + 1, 2), num(statistics.median(d)), num(sum(d) / (len(d) - 1), 2)])


def c10s3_median(r):
    d = rand_data(r, r.choice([7, 8, 9, 10]), 10, 90)
    med = statistics.median(d)
    s = sorted(d)
    return Q(f'Find the median of {", ".join(map(str, d))}.', num(med), f'Arrange in order: {", ".join(map(str, s))}; n = {len(d)}, median = {num(med)}.',
             [num(d[len(d) // 2]), num(sum(d) / len(d), 1), num(s[len(s) // 2 - 1] if len(s) % 2 else s[len(s) // 2 + 1])])


def c10s3_mode(r):
    base = rand_data(r, 7, 1, 20)
    m = r.choice(base)
    d = base + [m, m]
    r.shuffle(d)
    if list(statistics.multimode(d)) != [m]:
        raise ValueError
    return mcq(f'The mode of {", ".join(map(str, d))} is …', str(m), [str(x) for x in r.sample([x for x in set(d) if x != m] + [max(d) + 1, min(d) + 2], 3)],
               f'{m} occurs most often ({d.count(m)} times).', r)


def c10s3_missing(r):
    n = r.randint(5, 8)
    d = rand_data(r, n - 1, 5, 40)
    mean = r.randint(15, 35)
    x = mean * n - sum(d)
    if x <= 0:
        raise ValueError
    return Q(f'The mean of {", ".join(map(str, d))} and x is {mean}. Find x.', str(x), f'Sum = {mean} × {n} = {mean * n}; x = {mean * n} − {sum(d)} = {x}.',
             num_distractors(x, mean, x + mean, mean * n))


def c10s3_explain(r):
    return xbank([
        ('Explain why the median can be a better average than the mean for the salaries of 10 workers in a shop where the owner\'s salary is also included.', 'One very large value raises the mean a lot but hardly changes the median.', '2 marks.'),
        ('Explain why the mode is the best average for the most popular shoe size sold in a shop.', 'The shop needs the most common size, not an arithmetic average.', '2 marks.'),
        ('If 5 is added to every observation, what happens to the mean and the median? Explain.', 'Both increase by 5.', 'Every value shifts by 5 (2 marks).'),
    ])(r)


def c10s3_ar(r):
    return arbank([
        ('The median of 3, 8, 1, 9, 5 is 5.', 'The median is the middle value when the data is arranged in order.', 'a', 'Order: 1, 3, 5, 8, 9.'),
        ('A data set can have more than one mode.', 'The mode is the value that occurs most often.', 'a', 'If two values tie for most often, both are modes.'),
        ('If each observation is multiplied by 2, the mean is doubled.', 'Mean = sum of observations ÷ number of observations.', 'a', 'The sum doubles.'),
        ('The mean of a data set is always one of the observations.', 'The mean is sum ÷ number of observations.', 'd', 'e.g. mean of 1, 2 is 1.5; A false, R true.'),
    ])(r)


def c10s3_case(r):
    d = rand_data(r, 9, 20, 95)
    s = sorted(d)
    m = sum(d) / 9
    return Q((f'The runs scored by a batter in 9 innings of a school tournament are: {", ".join(map(str, d))}. (i) Find the mean. (ii) Find the median. '
              f'(iii) If the lowest score is replaced by 100, which of mean and median changes, and to what? (iv) Which average better describes a "typical" innings here?'),
             f'(i) {num(m, 2)} (ii) {s[4]} (iii) mean becomes {num((sum(d) - s[0] + 100) / 9, 2)}; median becomes {sorted(s[1:] + [100])[4]} (iv) median (less affected by extreme scores)',
             '1 mark each part.')


# st4 interpreting and misleading graphs

def c10s4_mcq(r):
    return mcqbank([
        ('A bar graph whose vertical axis starts at 90 instead of 0 can …', 'exaggerate small differences', ['hide all differences', 'change the data', 'make the bars equal'], 'A truncated axis magnifies differences.'),
        ('The average that is most affected by extreme values is the …', 'mean', ['median', 'mode', 'range'], 'Every value enters the sum.'),
        ('To show how a whole is divided into parts, the best graph is usually …', 'a pie chart', ['a histogram', 'a frequency polygon', 'a line graph'], 'Pie charts show proportions.'),
        ('To show how temperature changes over a day, the best graph is …', 'a line graph', ['a pie chart', 'a pictograph', 'a bar graph of categories'], 'Change over time.'),
    ])(r)


def c10s4_explain(r):
    a = r.randint(91, 95)
    b = a + r.randint(1, 4)
    return Q(f'A coaching centre\'s advertisement shows bars for pass rates {a}% (2024) and {b}% (2025) with the vertical axis starting at {a - 1}%, so the second bar looks several times taller. Explain why the graph is misleading.',
             f'The axis does not start at 0; the actual increase is only {b - a} percentage point{"s" if b - a > 1 else ""}.', 'Identify truncated axis (1), state true difference (1).')


def c10s4_ar(r):
    return arbank([
        ('A graph with a vertical axis not starting at zero can mislead readers.', 'Differences in bar heights then look larger than the true differences.', 'a', 'R explains A.'),
        ('The mean is always the best average to use.', 'The mean uses all the observations.', 'd', 'With extreme values the median may be better; A false, R true.'),
        ('A pie chart is suitable to show the change in rainfall over 12 months.', 'A pie chart shows parts of a whole.', 'd', 'A line or bar graph is better; A false, R true.'),
    ])(r)


def c10s4_choose(r):
    sit = r.choice([('the typical house price in a city where a few houses are extremely expensive', 'median'), ('the most common size of school uniform to order', 'mode'),
                    ('the average marks of a class for a report where all scores are close together', 'mean'), ('the favourite colour of students in a class', 'mode'),
                    ('the typical monthly income in a village where one landowner earns far more than others', 'median')])
    return Q(f'Which measure of central tendency (mean, median or mode) is most suitable for {sit[0]}? Give a reason.', sit[1].capitalize(),
             {'median': 'Not pulled by extreme values.', 'mode': 'Gives the most frequent category/value.', 'mean': 'Uses all values; no extremes to distort it.'}[sit[1]],
             [x.capitalize() for x in ['mean', 'median', 'mode', 'range'] if x != sit[1]])


def c10s4_case(r):
    who = name(r)
    sal = sorted([r.randint(12, 25) * 1000 for _ in range(6)]) + [r.randint(15, 30) * 10000]
    m = sum(sal) / 7
    return Q((f'A small shop has 7 people. Their monthly incomes are: {", ".join(inr(s) for s in sal)} (the last is the owner). {who}, a job seeker, is told "the average income here is {inr(round(m))}". '
              f'(i) Check this mean. (ii) Find the median income. (iii) Which figure better describes what a worker earns? (iv) Is the statement misleading? Explain.'),
             f'(i) {inr(round(m))} (ii) {inr(sal[3])} (iii) the median (iv) yes; the owner\'s large income pulls the mean up',
             '1 mark each part.')


def c10s4_compare(r):
    a = [r.randint(40, 90) for _ in range(5)]
    b = [r.randint(55, 75) for _ in range(5)]
    return Q(f'Two batters scored as follows in 5 matches — A: {", ".join(map(str, a))}; B: {", ".join(map(str, b))}. Compare their means and ranges, and say who is more consistent.',
             f'Mean A {num(sum(a) / 5, 1)}, B {num(sum(b) / 5, 1)}; range A {max(a) - min(a)}, B {max(b) - min(b)}; {"B" if max(b) - min(b) < max(a) - min(a) else "A"} is more consistent',
             'Means (1), ranges (1), smaller range ⇒ more consistent (1).')


FAMILIES = {
    S + '06-st1': [F('C1', 'D2', 'mcq', c6s1_formula), F('C1', 'D1', 'short', c6s1_tri), F('C2', 'D2', 'explain', c6s1_explain), F('C2', 'D3', 'mcq', c6s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s1_trap), F('C3', 'D3', 'numerical', c6s1_height), F('C3', 'D3', 'multi_step', c6s1_rhombus), F('C4', 'D3', 'case', c6s1_field)],
    S + '06-st2': [F('C1', 'D2', 'mcq', c6s2_formula), F('C1', 'D1', 'short', c6s2_mcq), F('C2', 'D2', 'explain', c6s2_explain), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s2_area), F('C3', 'D3', 'numerical', c6s2_iso), F('C3', 'D2', 'numerical', c6s2_equi), F('C3', 'D4', 'multi_step', c6s2_perimeter),
                   F('C4', 'D3', 'case', c6s2_case_fix), F('C4', 'D4', 'long', c6s2_quad), F('C4', 'D5', 'long', c6s2_quad)],
    S + '06-st3': [F('C1', 'D2', 'mcq', c6s3_mcq), F('C1', 'D1', 'short', c6s3_circ), F('C2', 'D2', 'explain', c6s3_explain), F('C2', 'D2', 'mcq', c6s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s3_area), F('C3', 'D3', 'numerical', c6s3_sector), F('C3', 'D3', 'numerical', c6s3_ring), F('C4', 'D3', 'numerical', c6s3_reverse),
                   F('C4', 'D4', 'case', c6s3_case)],
    S + '06-st4': [F('C1', 'D1', 'short', c6s4_units), F('C1', 'D2', 'short', c6s4_units), F('C2', 'D2', 'explain', c6s4_explain), F('C2', 'D3', 'mcq', c6s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s4_cross), F('C3', 'D3', 'numerical', c6s4_semi), F('C3', 'D4', 'multi_step', c6s4_path, gap='G7'), F('C4', 'D3', 'case', c6s4_case),
                   F('C4', 'D4', 'long', c6s4_quad_field), F('C4', 'D5', 'long', c6s4_quad_field)],
    S + '07-st1': [F('C1', 'D2', 'mcq', c7s1_mcq), F('C1', 'D1', 'short', c7s1_list), F('C2', 'D2', 'mcq', c7s1_classify), F('C2', 'D2', 'explain', c7s1_explain),
                   F('C2', 'D3', 'mcq', c7s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c7s1_list), F('C4', 'D3', 'case', c7s1_case)],
    S + '07-st2': [F('C1', 'D2', 'mcq', c7s2_mcq), F('C1', 'D1', 'short', c7s2_coin), F('C2', 'D2', 'explain', c7s2_explain), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s2_die), F('C3', 'D3', 'numerical', c7s2_predict), F('C4', 'D3', 'case', c7s2_case), F('C4', 'D4', 'case', c7s2_table)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_die), F('C1', 'D1', 'short', c7s3_bag), F('C2', 'D2', 'explain', c7s3_explain), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s3_bag), F('C3', 'D3', 'numerical', c7s3_cards), F('C3', 'D4', 'multi_step', c7s3_find_n), F('C4', 'D3', 'case', c7s3_case),
                   F('C4', 'D4', 'multi_step', c7s3_find_n, gap='G7')],
    S + '07-st4': [F('C1', 'D2', 'mcq', c7s4_coins), F('C2', 'D2', 'explain', c7s4_explain), F('C2', 'D3', 'mcq', c7s4_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c7s4_sum),
                   F('C3', 'D2', 'numerical', c7s4_three), F('C3', 'D3', 'multi_step', c7s4_product), F('C4', 'D3', 'case', c7s4_spinner), F('C4', 'D4', 'case', c7s4_case)],
    S + '08-st1': [F('C1', 'D2', 'mcq', c8s1_mcq), F('C1', 'D1', 'short', c8s1_next), F('C2', 'D2', 'explain', c8s1_explain), F('C2', 'D3', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c8s1_recursive), F('C3', 'D3', 'numerical', c8s1_virahanka), F('C4', 'D3', 'case', c8s1_case)],
    S + '08-st2': [F('C1', 'D2', 'mcq', c8s2_d), F('C1', 'D1', 'short', c8s2_nth), F('C2', 'D2', 'explain', c8s2_explain), F('C2', 'D3', 'explain', c8s2_isterm),
                   F('C2', 'D2', 'mcq', c8s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c8s2_nth), F('C3', 'D3', 'numerical', c8s2_which), F('C3', 'D4', 'multi_step', c8s2_two_terms),
                   F('C4', 'D3', 'case', c8s2_case), F('C4', 'D4', 'long', c8s2_two_terms)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_ratio), F('C1', 'D1', 'short', c8s3_nth), F('C2', 'D2', 'explain', c8s3_explain), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s3_nth), F('C3', 'D3', 'numerical', c8s3_which), F('C4', 'D3', 'multi_step', c8s3_bacteria, gap='G7'), F('C4', 'D4', 'case', c8s3_case)],
    S + '08-st4': [F('C1', 'D2', 'mcq', c8s4_mcq), F('C2', 'D2', 'explain', c8s4_explain), F('C2', 'D2', 'mcq', c8s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c8s4_triangular),
                   F('C3', 'D2', 'short', c8s4_sier), F('C3', 'D3', 'numerical', c8s4_koch), F('C4', 'D3', 'case', c8s4_case)],
    S + '09-st1': [F('C1', 'D2', 'mcq', c9s1_mcq), F('C1', 'D1', 'short', c9s1_truth), F('C2', 'D2', 'short', c9s1_hyp), F('C2', 'D3', 'explain', c9s1_explain),
                   F('C2', 'D2', 'mcq', c9s1_ar, kinds=('ar',)), F('C3', 'D2', 'short', c9s1_hyp), F('C4', 'D3', 'case', c9s1_case)],
    S + '09-st2': [F('C1', 'D2', 'mcq', c9s2_mcq), F('C2', 'D2', 'short', c9s2_converse), F('C2', 'D3', 'explain', c9s2_explain), F('C2', 'D2', 'mcq', c9s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'explain', c9s2_contra), F('C3', 'D3', 'explain', c9s2_biconditional), F('C3', 'D1', 'short', c9s2_converse), F('C4', 'D3', 'case', c9s2_case)],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_mcq), F('C1', 'D1', 'short', c9s3_vert), F('C2', 'D2', 'explain', c9s3_explain), F('C2', 'D3', 'mcq', c9s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c9s3_parallel), F('C3', 'D3', 'numerical', c9s3_linear), F('C3', 'D2', 'numerical', c9s3_tri), F('C4', 'D3', 'multi_step', c9s3_zigzag),
                   F('C4', 'D4', 'long', c9s3_zigzag)],
    S + '09-st4': [F('C1', 'D2', 'mcq', c9s4_mcq), F('C1', 'D1', 'short', c9s4_counter), F('C2', 'D2', 'explain', c9s4_explain), F('C2', 'D3', 'mcq', c9s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c9s4_counter), F('C3', 'D3', 'numerical', c9s4_n2), F('C4', 'D3', 'case', c9s4_case)],
    S + '09-st5': [F('C1', 'D2', 'mcq', c9s5_crit), F('C1', 'D1', 'mcq', c9s5_mcq), F('C2', 'D2', 'explain', c9s5_explain), F('C2', 'D3', 'mcq', c9s5_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c9s5_isos), F('C3', 'D3', 'short', c9s5_cpct), F('C3', 'D4', 'long', c9s5_prove), F('C4', 'D3', 'case', c9s5_case),
                   F('C4', 'D4', 'long', c9s5_prove)],
    S + '10-st1': [F('C1', 'D2', 'mcq', c10s1_mcq), F('C1', 'D1', 'short', c10s1_classmark), F('C2', 'D2', 'explain', c10s1_explain), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s1_count), F('C3', 'D3', 'numerical', c10s1_inclusive), F('C4', 'D3', 'case', c10s1_table)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_mcq), F('C1', 'D1', 'short', c10s2_read), F('C2', 'D2', 'explain', c10s2_explain), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s2_adjust), F('C3', 'D3', 'numerical', c10s2_poly), F('C3', 'D4', 'case', c10s2_case), F('C4', 'D3', 'numerical', c10s2_adjust),
                   F('C4', 'D4', 'case', c10s2_case)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_mode), F('C1', 'D1', 'short', c10s3_mean), F('C2', 'D2', 'explain', c10s3_explain), F('C2', 'D2', 'mcq', c10s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s3_median), F('C3', 'D3', 'numerical', c10s3_missing), F('C4', 'D3', 'case', c10s3_case)],
    S + '10-st4': [F('C1', 'D2', 'mcq', c10s4_mcq), F('C2', 'D2', 'explain', c10s4_explain), F('C2', 'D3', 'mcq', c10s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c10s4_choose),
                   F('C3', 'D2', 'short', c10s4_choose), F('C3', 'D3', 'numerical', c10s4_compare), F('C4', 'D3', 'case', c10s4_case)],
}
