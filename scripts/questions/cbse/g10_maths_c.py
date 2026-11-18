"""CBSE class 10 maths (NCERT Mathematics X) families, chapters 11-14."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, frac, name, two_names, inr, num_distractors, CITIES
from g9_maths_h import Q, mcqbank, arbank, xbank, fn, is_sq, triple, PI, pistr
import g9_maths_b as g9b

S = 'cbse-g10-maths-ch'
P314 = Fr(314, 100)
R173 = Fr(173, 100)
R7 = [Fr(7), Fr(14), Fr(21), Fr(7, 2), Fr(21, 2), Fr(28), Fr(35)]


def dec(x, dp=2):
    return num(round(float(x), dp), dp)


def ds(x):
    """Decimal text for a Fraction: exact if it terminates in 2 places, else ≈."""
    x = Fr(x)
    if (x * 100).denominator == 1:
        return dec(x)
    return f'{dec(x)} (approx.)'


def rr_(r, pool=None):
    return r.choice(pool or R7)


# ---------------- ch11 Areas related to circles ----------------
# st1 revisit

def c11s1_area(r):
    rad_ = rr_(r)
    C, A = 2 * PI * rad_, PI * rad_ * rad_
    if r.random() < 0.5:
        return Q(f'Find the circumference and area of a circle of radius {dec(rad_)} cm (π = 22/7).', f'C = {pistr(C)} cm, A = {pistr(A)} cm²', f'C = 2πr = {pistr(C)} cm; A = πr² = {pistr(A)} cm².',
                 [f'C = {pistr(A)} cm, A = {pistr(C)} cm²', f'C = {pistr(C / 2)} cm, A = {pistr(A)} cm²', f'C = {pistr(C)} cm, A = {pistr(2 * A)} cm²'])
    return Q(f'The circumference of a circle is {pistr(C)} cm. Find its area (π = 22/7).', f'{pistr(A)} cm²', f'2πr = {pistr(C)} ⇒ r = {dec(rad_)} cm; area = πr² = {pistr(A)} cm².',
             [f'{pistr(4 * A)} cm²', f'{pistr(A / 2)} cm²', f'{pistr(C * 2)} cm²'])


def c11s1_wheel(r):
    d = r.choice([Fr(70), Fr(84), Fr(56), Fr(42), Fr(140), Fr(98), Fr(126)])
    n = r.choice([100, 200, 250, 400, 500, 750, 1000, 1250])
    D = PI * d * n / 100
    return Q(f'The wheels of a cycle have diameter {dec(d)} cm. How many complete revolutions does each wheel make to cover {dec(D)} m (π = 22/7)?', str(n),
             f'Circumference = πd = {dec(PI * d)} cm; revolutions = {dec(D * 100)} ÷ {dec(PI * d)} = {n}.', num_distractors(n, n * 2, n // 2, n + 50))


def c11s1_sum(r):
    a, b, c = triple(r)
    k = r.choice([1, 2])
    if r.random() < 0.5:
        r1, r2 = a * k, b * k
        return Q(f'The radii of two circles are {r1} cm and {r2} cm. Find the radius of the circle whose area is equal to the sum of their areas.', f'{c * k} cm',
                 f'πR² = π({r1})² + π({r2})² ⇒ R² = {r1 * r1 + r2 * r2} ⇒ R = {c * k} cm (2 marks).', num_distractors(c * k, r1 + r2, r1 * r2 // (r1 + r2) + 1, c * k + 1))
    r1, r2 = r.randint(5, 25), r.randint(5, 25)
    return Q(f'The radii of two circles are {r1} cm and {r2} cm. Find the radius of the circle whose circumference is equal to the sum of their circumferences.', f'{r1 + r2} cm',
             f'2πR = 2π({r1}) + 2π({r2}) ⇒ R = {r1 + r2} cm.', num_distractors(r1 + r2, math.isqrt(r1 * r1 + r2 * r2), abs(r1 - r2), (r1 + r2) * 2))


def c11s1_ring(r):
    R, w = Fr(7 * r.randint(2, 10)), r.choice([Fr(7), Fr(7, 2), Fr(7, 4), Fr(14)])
    rr = R - w
    A = PI * (R * R - rr * rr)
    return Q(f'A circular park of radius {dec(rr)} m has a path {dec(w)} m wide running around it on the outside. Find the area of the path (π = 22/7).', f'{pistr(A)} m²',
             f'Outer radius {dec(R)} m; area = π(R² − r²) = 22/7 × ({dec(R * R)} − {dec(rr * rr)}) = {pistr(A)} m² (3 marks).', [f'{pistr(PI * w * w)} m²', f'{pistr(PI * R * R)} m²', f'{pistr(2 * PI * w * R)} m²'])


def c11s1_mcq(r):
    return mcqbank([
        ('If the radius of a circle is doubled, its area becomes …', '4 times', ['2 times', '8 times', 'half'], 'Area ∝ r².'),
        ('If the circumference and the area of a circle are numerically equal, the radius is …', '2 units', ['1 unit', '4 units', 'π units'], '2πr = πr² ⇒ r = 2.'),
        ('The perimeter of a semicircle of radius r is …', 'πr + 2r', ['πr', '2πr', 'πr + r'], 'Arc plus diameter.'),
        ('The ratio of the areas of two circles with radii 3 cm and 5 cm is …', '9 : 25', ['3 : 5', '6 : 10', '27 : 125'], 'Ratio of r².'),
        ('The area of a circle with diameter d is …', 'πd²/4', ['πd²', 'πd²/2', '2πd'], 'r = d/2.'),
    ])(r)


def c11s1_ar(r):
    return arbank([
        ('If the radius of a circle is tripled, its circumference is tripled.', 'The circumference of a circle is directly proportional to its radius.', 'a', 'C = 2πr.'),
        ('If the radius of a circle is tripled, its area is tripled.', 'The area of a circle is πr².', 'd', 'It becomes 9 times; A false, R true.'),
        ('The area of a ring between circles of radii 5 cm and 3 cm is 16π cm².', 'Area of a ring = π(R² − r²).', 'a', 'π(25 − 9).'),
        ('A circle of circumference 44 cm has radius 7 cm (π = 22/7).', 'The area of a circle is πr².', 'b', 'Both true, but R is about area; A uses C = 2πr.'),
    ])(r)


def c11s1_explain(r):
    return xbank([
        ('Explain why the area of the path around a circular park is not π × (width)².', 'The path is a ring: its area is π(R² − r²) = π(R + r)(R − r), which depends on both radii.', '2 marks.'),
        ('Explain how the number of revolutions of a wheel is found when the distance covered is known.', 'In one revolution the wheel covers its circumference; revolutions = distance ÷ circumference.', '2 marks.'),
        ('Explain why the area of a circle with radius equal to the sum of two radii is more than the sum of their areas.', '(r₁ + r₂)² = r₁² + r₂² + 2r₁r₂ > r₁² + r₂².', '2 marks.'),
    ])(r)


def c11s1_case(r):
    rad_ = rr_(r, [Fr(14), Fr(21), Fr(28), Fr(35)])
    w = Fr(7, 2)
    rate = r.choice([20, 25, 40, 50])
    A = PI * ((rad_ + w) ** 2 - rad_ ** 2)
    return Q((f'A circular garden of radius {dec(rad_)} m in {r.choice(CITIES)} is to be fenced, and a gravel path {dec(w)} m wide is laid around it on the outside (π = 22/7). '
              f'(i) Find the length of the fence along the garden boundary. (ii) Find the area of the garden. (iii) Find the area of the path. (iv) Find the cost of laying gravel at ₹{rate} per m².'),
             f'(i) {pistr(2 * PI * rad_)} m (ii) {pistr(PI * rad_ * rad_)} m² (iii) {pistr(A)} m² (iv) {inr(float(A * rate))}', '1 mark each part.')


# st2 sector and arc

ANG = [30, 40, 45, 60, 72, 80, 90, 120, 135, 150, 210, 240]


def c11s2_sector(r):
    rad_, t = rr_(r), r.choice(ANG)
    A = Fr(t, 360) * PI * rad_ * rad_
    return Q(f'Find the area of a sector of a circle with radius {dec(rad_)} cm and angle {t}° (π = 22/7).', f'{pistr(A)} cm²', f'Area = (θ/360) × πr² = ({t}/360) × 22/7 × {dec(rad_)}² = {pistr(A)} cm².',
             [f'{pistr(Fr(t, 180) * PI * rad_ * rad_)} cm²', f'{pistr(Fr(t, 360) * 2 * PI * rad_)} cm²', f'{pistr(PI * rad_ * rad_ - A)} cm²'])


def c11s2_arc(r):
    rad_, t = rr_(r), r.choice(ANG)
    L = Fr(t, 360) * 2 * PI * rad_
    return Q(f'Find the length of the arc of a circle of radius {dec(rad_)} cm subtending an angle of {t}° at the centre (π = 22/7).', f'{pistr(L)} cm',
             f'Arc = (θ/360) × 2πr = {pistr(L)} cm.', [f'{pistr(L / 2)} cm', f'{pistr(Fr(t, 360) * PI * rad_ * rad_)} cm', f'{pistr(L + 2 * rad_)} cm'])


def c11s2_clock(r):
    L = rr_(r, [Fr(7), Fr(14), Fr(21, 2), Fr(7, 2), Fr(21)])
    t = r.choice([5, 10, 15, 20, 25, 35, 40, 45])
    A = Fr(6 * t, 360) * PI * L * L
    return Q(f'The minute hand of a clock is {dec(L)} cm long. Find the area swept by it in {t} minutes (π = 22/7).', f'{pistr(A)} cm²',
             f'In {t} minutes the hand turns {6 * t}°; area = ({6 * t}/360) × πr² = {pistr(A)} cm² (2 marks).', [f'{pistr(A * 2)} cm²', f'{pistr(Fr(6 * t, 360) * 2 * PI * L)} cm²', f'{pistr(Fr(t, 360) * PI * L * L)} cm²'])


def c11s2_theta(r):
    rad_, t = rr_(r, [Fr(7), Fr(14), Fr(21), Fr(21, 2), Fr(28)]), r.choice(ANG)
    L = Fr(t, 360) * 2 * PI * rad_
    return Q(f'An arc of length {pistr(L)} cm subtends an angle θ at the centre of a circle of radius {dec(rad_)} cm. Find θ (π = 22/7).', f'{t}°',
             f'(θ/360) × 2 × 22/7 × {dec(rad_)} = {pistr(L)} ⇒ θ = {t}° (3 marks).', num_distractors(t, t * 2, t // 2, 360 - t))


def c11s2_perim(r):
    rad_, t = rr_(r), r.choice(ANG)
    L = Fr(t, 360) * 2 * PI * rad_
    return Q(f'Find the perimeter of a sector of a circle of radius {dec(rad_)} cm with central angle {t}° (π = 22/7).', f'{pistr(L + 2 * rad_)} cm',
             f'Perimeter = arc + 2r = {pistr(L)} + {dec(2 * rad_)} = {pistr(L + 2 * rad_)} cm (3 marks).', [f'{pistr(L)} cm', f'{pistr(L + rad_)} cm', f'{pistr(2 * PI * rad_ + 2 * rad_)} cm'])


def c11s2_major(r):
    rad_, t = rr_(r), r.choice([30, 45, 60, 72, 90, 120])
    A = Fr(t, 360) * PI * rad_ * rad_
    return Q(f'A chord of a circle of radius {dec(rad_)} cm subtends an angle of {t}° at the centre. Find the areas of the minor and major sectors (π = 22/7).', f'Minor {pistr(A)} cm², major {pistr(PI * rad_ * rad_ - A)} cm²',
             f'Minor = ({t}/360)πr² = {pistr(A)}; major = πr² − minor = {pistr(PI * rad_ * rad_ - A)} (3 marks).')


def c11s2_mcq(r):
    return mcqbank([
        ('The area of a sector of angle θ (in degrees) of a circle of radius r is …', '(θ/360) × πr²', ['(θ/180) × πr²', '(θ/360) × 2πr', '(θ/720) × πr²'], 'Proportion of the full circle.'),
        ('The length of an arc of angle θ of a circle of radius r is …', '(θ/360) × 2πr', ['(θ/360) × πr²', '(θ/180) × 2πr', 'θ × r'], 'Proportion of the circumference.'),
        ('The angle described by the minute hand of a clock in 1 minute is …', '6°', ['1°', '30°', '0.5°'], '360° in 60 minutes.'),
        ('Area of a sector of angle θ = …', '½ × arc length × r', ['arc length × r', '2 × arc length × r', 'arc length ÷ r'], '(θ/360)πr² = ½ × (θ/360)2πr × r.'),
        ('If the arc length of a sector equals its radius, its area is …', 'r²/2', ['r²', 'πr²/2', '2r²'], '½ × ℓ × r.'),
    ])(r)


def c11s2_ar(r):
    return arbank([
        ('The area of a quadrant of a circle of radius 14 cm is 154 cm² (π = 22/7).', 'A quadrant is a sector of angle 90°.', 'a', '¼ × 22/7 × 196 = 154.'),
        ('The minute hand of a clock sweeps a sector of angle 90° in 15 minutes.', 'It turns 6° per minute.', 'a', '15 × 6 = 90.'),
        ('The area of a sector of angle 60° is one-third of the area of the circle.', 'The area of a sector of angle θ is (θ/360)πr².', 'd', 'It is one-sixth; A false, R true.'),
        ('The major sector has the larger angle at the centre.', 'Minor and major sector angles add to 360°.', 'b', 'Both true; R is not why A holds by itself.'),
    ])(r)


def c11s2_explain(r):
    return xbank([
        ('Explain how the formula for the area of a sector follows from the area of a circle.', 'A 360° angle gives πr²; by proportion, angle θ gives (θ/360) × πr².', '2 marks.'),
        ('Explain why the perimeter of a sector is not just the arc length.', 'The boundary also includes the two radii, so perimeter = arc + 2r.', '2 marks.'),
        ('Explain why the area swept by the minute hand in 20 minutes is one-third of the circle.', '20 minutes is 120°, and 120/360 = 1/3.', '2 marks.'),
    ])(r)


def c11s2_case(r):
    rad_ = rr_(r, [Fr(14), Fr(21), Fr(7), Fr(28)])
    n = r.choice([6, 8, 10, 12])
    t = Fr(360, n)
    A = PI * rad_ * rad_ / n
    return Q((f'A pizza of radius {dec(rad_)} cm is cut into {n} equal slices at a food stall in {r.choice(CITIES)} (π = 22/7). '
              f'(i) What is the angle of each slice at the centre? (ii) Find the area of one slice. (iii) Find the length of the crust (arc) of one slice. (iv) Find the perimeter of one slice.'),
             f'(i) {fn(t)}° (ii) {pistr(A)} cm² (iii) {pistr(2 * PI * rad_ / n)} cm (iv) {pistr(2 * PI * rad_ / n + 2 * rad_)} cm', '1 mark each part.')


# st3 segment (π = 3.14, √3 = 1.73)

def seg(rad_, t):
    sec = Fr(t, 360) * P314 * rad_ * rad_
    tri = rad_ * rad_ / 2 if t == 90 else R173 / 4 * rad_ * rad_
    return sec, tri, sec - tri


def c11s3_minor(r):
    rad_ = Fr(r.choice([5, 6, 8, 10, 12, 14, 15, 20, 21]))
    t = r.choice([60, 90, 120])
    sec, tri, m = seg(rad_, t)
    tri_txt = f'½ × {dec(rad_)} × {dec(rad_)} = {dec(tri)}' if t == 90 else (f'(√3/4) r² = {dec(tri)}' if t == 60 else f'½ r² sin 120° = (√3/4) r² = {dec(tri)}')
    return Q(f'A chord of a circle of radius {dec(rad_)} cm subtends an angle of {t}° at the centre. Find the area of the corresponding minor segment (π = 3.14, √3 = 1.73).', f'{ds(m)} cm²',
             f'Sector = ({t}/360) × 3.14 × {dec(rad_ * rad_)} = {dec(sec)}; triangle = {tri_txt}; segment = {dec(sec)} − {dec(tri)} = {ds(m)} cm² (3 marks).',
             [f'{ds(sec)} cm²', f'{ds(sec + tri)} cm²', f'{ds(P314 * rad_ * rad_ - m)} cm²'])


def c11s3_major(r):
    rad_ = Fr(r.choice([10, 12, 14, 15, 20, 21]))
    t = r.choice([60, 90, 120])
    sec, tri, m = seg(rad_, t)
    M = P314 * rad_ * rad_ - m
    return Q(f'A chord of a circle of radius {dec(rad_)} cm subtends an angle of {t}° at the centre. Find the areas of the minor and the major segments (π = 3.14, √3 = 1.73).', f'Minor {ds(m)} cm², major {ds(M)} cm²',
             f'Minor = sector − triangle = {dec(sec)} − {dec(tri)} = {ds(m)}; major = πr² − minor = {dec(P314 * rad_ * rad_)} − {ds(m)} = {ds(M)} (4 marks).')


def c11s3_square(r):
    rad_ = Fr(r.choice([5, 6, 7, 8, 10, 12, 14, 15, 20, 21, 25, 28, 30]))
    A = P314 * rad_ * rad_ - 2 * rad_ * rad_
    return Q(f'A square is inscribed in a circle of radius {dec(rad_)} cm. Find the area of the circle lying outside the square (π = 3.14).', f'{ds(A)} cm²',
             f'Diagonal of square = diameter = {dec(2 * rad_)}; area of square = ½ × d² = {dec(2 * rad_ * rad_)}; required = {dec(P314 * rad_ * rad_)} − {dec(2 * rad_ * rad_)} = {ds(A)} cm² (3 marks).',
             [f'{ds(2 * rad_ * rad_)} cm²', f'{ds(A / 4)} cm²', f'{ds(P314 * rad_ * rad_ - rad_ * rad_)} cm²'])


def c11s3_mcq(r):
    return mcqbank([
        ('Area of a minor segment = …', 'area of the corresponding sector − area of the corresponding triangle', ['area of sector + area of triangle', 'area of circle − area of sector', 'area of triangle − area of sector'], 'Definition.'),
        ('Area of the major segment = …', 'πr² − area of the minor segment', ['πr² − area of the minor sector', 'area of the major sector − area of the minor segment', 'area of the minor segment × 2'], 'The two segments make the circle.'),
        ('The area of the triangle formed by two radii r at 90° is …', 'r²/2', ['r²', '√3r²/4', 'πr²/4'], '½ × r × r.'),
        ('The area of the triangle formed by two radii r making 60° at the centre is …', '(√3/4) r²', ['r²/2', '(√3/2) r²', 'r²/4'], 'It is equilateral.'),
        ('A segment of a circle is the region between …', 'a chord and the corresponding arc', ['two radii and an arc', 'two chords', 'a tangent and the circle'], 'Definition.'),
    ])(r)


def c11s3_ar(r):
    return arbank([
        ('The triangle formed by a 60° chord and the two radii is equilateral.', 'Two sides are radii and the angle between them is 60°, so the base angles are 60° each.', 'a', 'R explains A.'),
        ('The area of a minor segment is always less than the area of the corresponding sector.', 'Minor segment = sector − triangle, and the triangle has positive area.', 'a', 'R explains A.'),
        ('The minor segment for a 90° chord in a circle of radius 10 cm has area 78.5 cm² (π = 3.14).', 'The area of the quadrant is 78.5 cm².', 'd', 'Segment = 78.5 − 50 = 28.5; A false, R true.'),
    ])(r)


def c11s3_explain(r):
    return xbank([
        ('Explain the steps to find the area of a minor segment when the central angle is 120°.', 'Find the sector area (120/360)πr², find the triangle area ½r² sin 120° = (√3/4)r² (via the perpendicular from the centre), and subtract.', '2 marks.'),
        ('Explain why the area of a semicircle is also the area of a segment.', 'A diameter is a chord; the semicircle is the segment cut off by it (triangle area 0).', '2 marks.'),
    ])(r)


def c11s3_case(r):
    rad_ = Fr(r.choice([10, 12, 14, 20]))
    sec, tri, m = seg(rad_, 90)
    rate = r.choice([2, 5, 10])
    return Q((f'A circular table top of radius {dec(rad_)} cm has a design made by drawing a chord that subtends 90° at the centre; the minor segment is painted gold (π = 3.14). '
              f'(i) Find the area of the quadrant. (ii) Find the area of the right triangle formed. (iii) Find the area painted gold. (iv) Find the cost of painting at ₹{rate} per cm².'),
             f'(i) {dec(sec)} cm² (ii) {dec(tri)} cm² (iii) {dec(m)} cm² (iv) {inr(float(m * rate))}', '1 mark each part.')


# st4 real life

def c11s4_horse(r):
    L = r.choice([5, 6, 7, 8, 10, 12, 14])
    L2 = L + r.choice([2, 3, 4, 5])
    side = r.choice([15, 20, 25, 30])
    A1 = Fr(1, 4) * P314 * L * L
    A2 = Fr(1, 4) * P314 * L2 * L2
    return Q(f'A horse is tied to a peg at one corner of a square grass field of side {side} m by a {L} m long rope. Find (a) the area of the part of the field the horse can graze and (b) the increase in grazing area if the rope were {L2} m long (π = 3.14).',
             f'(a) {ds(A1)} m² (b) {ds(A2 - A1)} m²', f'The horse grazes a quadrant: ¼ × 3.14 × {L}² = {ds(A1)} m²; with {L2} m rope: {ds(A2)} m²; increase = {ds(A2 - A1)} m² (4 marks).')


def c11s4_wiper(r):
    L = rr_(r, [Fr(21), Fr(14), Fr(28), Fr(35), Fr(42)])
    t = r.choice([90, 100, 105, 110, 115, 120])
    A = Fr(t, 360) * PI * L * L
    return Q(f'A car has two wipers which do not overlap. Each wiper has a blade of length {dec(L)} cm sweeping through an angle of {t}°. Find the total area cleaned at each sweep of the blades (π = 22/7).', f'{pistr(2 * A)} cm²',
             f'Each wiper sweeps a sector: ({t}/360) × 22/7 × {dec(L * L)} = {pistr(A)}; two wipers: {pistr(2 * A)} cm² (3 marks).', [f'{pistr(A)} cm²', f'{pistr(4 * A)} cm²', f'{pistr(Fr(t, 360) * 2 * PI * L * 2)} cm²'])


def c11s4_light(r):
    rad_ = Fr(r.choice([10, 12, 15, 16, 20])) if r.random() < 0.7 else Fr(33, 2)
    t = r.choice([60, 72, 80, 90, 120])
    A = Fr(t, 360) * P314 * rad_ * rad_
    return Q(f'To warn ships of underwater rocks, a lighthouse spreads a red light over a sector of angle {t}° to a distance of {dec(rad_)} km. Find the area of the sea over which the ships are warned (π = 3.14).', f'{ds(A)} km²',
             f'({t}/360) × 3.14 × {dec(rad_)}² = {ds(A)} km² (2 marks).', [f'{ds(A * 2)} km²', f'{ds(Fr(t, 360) * 2 * P314 * rad_)} km²', f'{ds(P314 * rad_ * rad_ - A)} km²'])


def c11s4_umbrella(r):
    n = r.choice([6, 8, 10, 12])
    rad_ = rr_(r, [Fr(42), Fr(35), Fr(28), Fr(49), Fr(56)])
    A = PI * rad_ * rad_ / n
    return Q(f'An umbrella has {n} ribs which are equally spaced. Assuming the umbrella to be a flat circle of radius {dec(rad_)} cm, find the area between two consecutive ribs (π = 22/7).', f'{pistr(A)} cm²',
             f'Each sector has angle 360°/{n} = {fn(Fr(360, n))}°; area = πr²/{n} = {pistr(A)} cm².', [f'{pistr(A * 2)} cm²', f'{pistr(2 * PI * rad_ / n)} cm²', f'{pistr(PI * rad_ * rad_ / (n - 1))} cm²'])


def c11s4_corners(r):
    a, b, c = triple(r)
    k = r.choice([2, 3, 4])
    a, b, c = a * k, b * k, c * k
    rad_ = Fr(r.choice([7, 7, 14])) if min(a, b) > 28 else Fr(7, 2)
    if 2 * rad_ > min(a, b):
        raise ValueError
    tri = Fr(a * b, 2)
    secs = PI * rad_ * rad_ / 2
    return Q(f'A triangular plot has sides {a} m, {b} m and {c} m (right-angled). At each corner a cow is tied with a rope {dec(rad_)} m long. Find the area of the plot that cannot be grazed (π = 22/7).', f'{pistr(tri - secs)} m²',
             f'Area of plot = ½ × {a} × {b} = {dec(tri)} m². The three sectors have angles summing to 180°, so together they make a semicircle: ½ × 22/7 × {dec(rad_)}² = {pistr(secs)}. Ungrazed = {pistr(tri - secs)} m² (4 marks).')


def c11s4_brooch(r):
    d = rr_(r, [Fr(35), Fr(28), Fr(42), Fr(21), Fr(14)])
    k = r.choice([3, 4, 5])
    wire = PI * d + k * d
    A = PI * (d / 2) ** 2 / (2 * k)
    return Q(f'A brooch is made with silver wire in the form of a circle of diameter {dec(d)} mm. The wire is also used to make {k} diameters which divide the circle into {2 * k} equal sectors. Find the total length of wire and the area of each sector (π = 22/7).',
             f'Wire {pistr(wire)} mm; each sector {pistr(A)} mm²', f'Circumference = {pistr(PI * d)} mm; diameters = {k} × {dec(d)}; total {pistr(wire)} mm. Each sector = πr²/{2 * k} = {pistr(A)} mm² (4 marks).')


def c11s4_ar(r):
    return arbank([
        ('A goat tied at a corner of a rectangular field with a short rope grazes a quadrant.', 'The angle at the corner of a rectangle is 90°.', 'a', 'R explains A.'),
        ('Sectors of equal radius at the three corners of a triangle together form a semicircle.', 'The angles of a triangle add up to 180°.', 'a', 'R explains A.'),
        ('Two non-overlapping wipers each sweeping 120° clean an area equal to the whole circle.', 'Two sectors of 120° make 240°.', 'd', '240° is two-thirds of the circle; A false, R true.'),
    ])(r)


def c11s4_explain(r):
    return xbank([
        ('Explain why the area grazed by a cow tied at a corner of a square field (rope shorter than the side) is a quadrant.', 'The cow can move in a circle of radius equal to the rope, but the field allows only the 90° part at the corner.', '2 marks.'),
        ('Explain how to find the area of the region in a square of side a left after drawing quadrants of radius a/2 at all four corners.', 'The four quadrants make one full circle of radius a/2; subtract π(a/2)² from a².', '2 marks.'),
    ])(r)


def c11s4_case(r):
    a = r.choice([14, 28, 42, 56, 70, 21, 35])
    rad_ = Fr(a, 2)
    q = PI * rad_ * rad_
    obj = r.choice(['handkerchief', 'tile', 'table mat', 'rangoli board'])
    return Q((f'A square {obj} of side {a} cm has a design: quadrants of radius {dec(rad_)} cm are drawn at all four corners and coloured (π = 22/7). '
              f'(i) What is the angle of each quadrant? (ii) Find the area of one quadrant. (iii) Find the total coloured area. (iv) Find the area left uncoloured.'),
             f'(i) 90° (ii) {pistr(q / 4)} cm² (iii) {pistr(q)} cm² (iv) {pistr(a * a - q)} cm²', '1 mark each part.')


# ---------------- ch12 Surface areas and volumes ----------------

CONES = [(Fr(7), 24, 25), (Fr(7, 2), 12, Fr(25, 2)), (Fr(21), 20, 29), (Fr(21, 2), 10, Fr(29, 2)), (Fr(21), 28, 35), (Fr(21, 2), 14, Fr(35, 2)), (Fr(14), 48, 50),
         (Fr(28), 21, 35), (Fr(14), Fr(21, 2), Fr(35, 2)), (Fr(35), 12, 37), (Fr(35, 2), 6, Fr(37, 2)), (Fr(42), 40, 58), (Fr(21), 72, 75), (Fr(28), 45, 53), (Fr(14), Fr(45, 2), Fr(53, 2))]
RS = [Fr(7), Fr(14), Fr(7, 2), Fr(21), Fr(21, 2)]


def cone(r, rmax=None):
    rr, h, l = r.choice([c for c in CONES if rmax is None or c[0] <= rmax])
    return Fr(rr), Fr(h), Fr(l)


def c12s1_toy(r):
    rr, h, l = cone(r)
    A = PI * rr * l + 2 * PI * rr * rr
    return Q(f'A toy is in the form of a cone of radius {dec(rr)} cm mounted on a hemisphere of the same radius. The slant height of the cone is {dec(l)} cm. Find the total surface area of the toy (π = 22/7).', f'{pistr(A)} cm²',
             f'TSA = CSA of cone + CSA of hemisphere = πrl + 2πr² = {pistr(PI * rr * l)} + {pistr(2 * PI * rr * rr)} = {pistr(A)} cm² (3 marks).',
             [f'{pistr(A + PI * rr * rr)} cm²', f'{pistr(2 * PI * rr * l + 2 * PI * rr * rr)} cm²', f'{pistr(PI * rr * l + PI * rr * rr)} cm²'])


def c12s1_capsule(r):
    rr = r.choice([Fr(7, 4), Fr(7, 2), Fr(7), Fr(1, 2) * 7])
    h = r.choice([Fr(5), Fr(7), Fr(10), Fr(14), Fr(21, 2)])
    L = h + 2 * rr
    A = 2 * PI * rr * h + 4 * PI * rr * rr
    return Q(f'A capsule is in the shape of a cylinder with two hemispheres stuck to its ends. Its total length is {dec(L)} mm and its diameter is {dec(2 * rr)} mm. Find its surface area (π = 22/7).', f'{pistr(A)} mm²',
             f'Cylinder length = {dec(L)} − {dec(2 * rr)} = {dec(h)}; SA = 2πrh + 4πr² = {pistr(2 * PI * rr * h)} + {pistr(4 * PI * rr * rr)} = {pistr(A)} mm² (3 marks).',
             [f'{pistr(2 * PI * rr * L + 4 * PI * rr * rr)} mm²', f'{pistr(2 * PI * rr * h + 2 * PI * rr * rr)} mm²', f'{pistr(2 * PI * rr * h)} mm²'])


def c12s1_cube(r):
    a = r.choice([Fr(7), Fr(14), Fr(21), Fr(10), Fr(28), Fr(35), Fr(7, 2), Fr(21, 2), Fr(42)])
    rr = a / 2
    A = 6 * a * a + PI * rr * rr
    return Q(f'A cubical block of side {dec(a)} cm is surmounted by a hemisphere. What is the greatest diameter the hemisphere can have? Find the surface area of the solid (π = 22/7).', f'Diameter {dec(a)} cm; SA {pistr(A)} cm²',
             f'Greatest diameter = side = {dec(a)} cm. SA = 6a² − πr² + 2πr² = 6a² + πr² = {dec(6 * a * a)} + {pistr(PI * rr * rr)} = {pistr(A)} cm² (3 marks).')


def c12s1_tent(r):
    rr, hc, l = cone(r, 14)
    h = r.choice([Fr(3), Fr(4), Fr(5), Fr(6), Fr(21, 10)])
    A = 2 * PI * rr * h + PI * rr * l
    return Q(f'A tent is in the shape of a cylinder of height {dec(h)} m and diameter {dec(2 * rr)} m surmounted by a cone of the same base and slant height {dec(l)} m. Find the area of canvas used (π = 22/7).', f'{pistr(A)} m²',
             f'Canvas = CSA of cylinder + CSA of cone = 2πrh + πrl = {pistr(2 * PI * rr * h)} + {pistr(PI * rr * l)} = {pistr(A)} m² (3 marks).',
             [f'{pistr(A + PI * rr * rr)} m²', f'{pistr(2 * PI * rr * h)} m²', f'{pistr(PI * rr * h + PI * rr * l)} m²'])


def c12s1_scooped(r):
    rr = r.choice([Fr(7, 2), Fr(7), Fr(21, 4), Fr(14)])
    h = r.choice([Fr(10), Fr(12), Fr(15), Fr(20), Fr(21)])
    if 2 * rr > h:
        raise ValueError
    A = 2 * PI * rr * h + 4 * PI * rr * rr
    return Q(f'A wooden article is made by scooping out a hemisphere from each end of a solid cylinder of height {dec(h)} cm and base radius {dec(rr)} cm. Find its total surface area (π = 22/7).', f'{pistr(A)} cm²',
             f'TSA = CSA of cylinder + 2 × CSA of hemisphere = 2πrh + 4πr² = {pistr(A)} cm² (3 marks).', [f'{pistr(2 * PI * rr * h + 2 * PI * rr * rr)} cm²', f'{pistr(2 * PI * rr * h)} cm²', f'{pistr(2 * PI * rr * h + 6 * PI * rr * rr)} cm²'])


def c12s1_cavity(r):
    rr, h, l = cone(r)
    A = 2 * PI * rr * h + PI * rr * rr + PI * rr * l
    return Q(f'From a solid cylinder of height {dec(h)} cm and radius {dec(rr)} cm, a cone of the same height and radius is hollowed out (slant height {dec(l)} cm). Find the total surface area of the remaining solid (π = 22/7).', f'{pistr(A)} cm²',
             f'TSA = 2πrh + πr² + πrl = {pistr(2 * PI * rr * h)} + {pistr(PI * rr * rr)} + {pistr(PI * rr * l)} = {pistr(A)} cm² (4 marks).')


def c12s1_mcq(r):
    return mcqbank([
        ('The total surface area of a solid hemisphere of radius r is …', '3πr²', ['2πr²', '4πr²', 'πr²'], 'Curved 2πr² + base πr².'),
        ('When a cone is placed on a hemisphere of the same radius, the surface area of the combined solid is …', 'CSA of cone + CSA of hemisphere', ['TSA of cone + TSA of hemisphere', 'CSA of cone + TSA of hemisphere', 'TSA of cone + CSA of hemisphere'], 'The common circular face is hidden.'),
        ('Two cubes of side 5 cm are joined end to end. The surface area of the cuboid formed is …', '250 cm²', ['300 cm²', '150 cm²', '275 cm²'], '2(10 × 5 + 5 × 5 + 10 × 5).'),
        ('The surface area of a capsule (cylinder with two hemispherical ends) is …', '2πrh + 4πr²', ['2πrh + 2πr²', '2πr(h + r)', 'πr²h + 4πr²'], 'Cylinder CSA + sphere SA.'),
    ])(r)


def c12s1_ar(r):
    return arbank([
        ('The surface area of a toy made of a cone on a hemisphere does not include the area of the circular base.', 'The circular faces are joined and lie inside the toy.', 'a', 'R explains A.'),
        ('Two cubes of side 4 cm joined end to end form a cuboid of surface area 192 cm².', 'Joining hides two faces of 16 cm² each.', 'd', '2 × 96 − 32 = 160 cm²; A false, R true.'),
        ('Scooping a hemisphere out of a cube increases the surface area.', 'The curved surface 2πr² replaces a flat circle of area πr².', 'a', 'Net increase πr².'),
    ])(r)


def c12s1_explain(r):
    return xbank([
        ('Explain why the surface area of a combination of solids is not the sum of the total surface areas of the parts.', 'The faces where the parts are joined are hidden and must not be counted.', '2 marks.'),
        ('Explain how the surface area changes when a hemisphere of radius r is scooped out of one face of a cube.', 'A circle of area πr² is removed and the curved surface 2πr² is added: increase of πr².', '2 marks.'),
    ])(r)


def c12s1_case(r):
    rr = r.choice([Fr(7, 2), Fr(7)])
    h = r.choice([Fr(7), Fr(10), Fr(14)])
    rate = r.choice([5, 10])
    A = 2 * PI * rr * h + 2 * PI * rr * rr
    return Q((f'A bird-bath in a garden is a cylinder of height {dec(h * 10)} cm and radius {dec(rr * 10)} cm with a hemispherical depression at the top (π = 22/7). '
              f'(i) Write the CSA of the cylinder. (ii) Write the CSA of the hemisphere. (iii) Find the total surface area of the bird-bath (excluding the base). (iv) Find the cost of painting it at ₹{rate} per 100 cm².'),
             f'(i) {pistr(2 * PI * rr * h * 100)} cm² (ii) {pistr(2 * PI * rr * rr * 100)} cm² (iii) {pistr(A * 100)} cm² (iv) {inr(float(A * rate))}', '1 mark each part.')


# st2 volume

def c12s2_toy(r):
    rr, h, l = cone(r)
    V = PI * rr * rr * h / 3 + 2 * PI * rr ** 3 / 3
    return Q(f'A solid is in the shape of a cone of height {dec(h)} cm standing on a hemisphere, both of radius {dec(rr)} cm. Find its volume (π = 22/7).', f'{pistr(V)} cm³',
             f'V = ⅓πr²h + ⅔πr³ = {pistr(PI * rr * rr * h / 3)} + {pistr(2 * PI * rr ** 3 / 3)} = {pistr(V)} cm³ (3 marks).',
             [f'{pistr(PI * rr * rr * h + 2 * PI * rr ** 3 / 3)} cm³', f'{pistr(PI * rr * rr * h / 3 + 4 * PI * rr ** 3 / 3)} cm³', f'{pistr(PI * rr * rr * h / 3)} cm³'])


def c12s2_capsule(r):
    rr = r.choice([Fr(7, 2), Fr(7), Fr(7, 4), Fr(21, 2)])
    h = r.choice([Fr(6), Fr(7), Fr(10), Fr(14), Fr(20)])
    V = PI * rr * rr * h + 4 * PI * rr ** 3 / 3
    return Q(f'A solid is a cylinder of length {dec(h)} cm with a hemisphere of radius {dec(rr)} cm fixed at each end. Find its volume (π = 22/7).', f'{pistr(V)} cm³',
             f'V = πr²h + 4/3 πr³ = {pistr(PI * rr * rr * h)} + {pistr(4 * PI * rr ** 3 / 3)} = {pistr(V)} cm³ (3 marks).',
             [f'{pistr(PI * rr * rr * h + 2 * PI * rr ** 3 / 3)} cm³', f'{pistr(PI * rr * rr * (h + 2 * rr))} cm³', f'{pistr(PI * rr * rr * h)} cm³'])


def c12s2_rocket(r):
    rr = r.choice([Fr(7, 2), Fr(7), Fr(21, 2), Fr(14)])
    h1 = r.choice([Fr(10), Fr(12), Fr(15), Fr(20)])
    h2 = r.choice([Fr(6), Fr(9), Fr(12)])
    V = PI * rr * rr * h1 + PI * rr * rr * h2 / 3
    return Q(f'A model rocket is a cylinder of height {dec(h1)} cm and radius {dec(rr)} cm surmounted by a cone of height {dec(h2)} cm with the same radius. Find the volume of the model (π = 22/7).', f'{pistr(V)} cm³',
             f'V = πr²h₁ + ⅓πr²h₂ = {pistr(PI * rr * rr * h1)} + {pistr(PI * rr * rr * h2 / 3)} = {pistr(V)} cm³ (3 marks).',
             [f'{pistr(PI * rr * rr * (h1 + h2))} cm³', f'{pistr(PI * rr * rr * (h1 + h2) / 3)} cm³', f'{pistr(PI * rr * rr * h1 - PI * rr * rr * h2 / 3)} cm³'])


def c12s2_pen(r):
    l, b, h = r.choice([(15, 10, Fr(7, 2)), (20, 12, 5), (14, 10, 4), (18, 12, 6)])
    n = r.choice([2, 3, 4, 5])
    cr, ch = r.choice([(Fr(1, 2), Fr(7, 5)), (Fr(7, 10), Fr(3)), (Fr(7, 10), Fr(2)), (Fr(1), Fr(21, 10))])
    V = Fr(l * b) * h - n * PI * cr * cr * ch / 3
    return Q(f'A pen stand made of wood is a cuboid {l} cm × {b} cm × {dec(h)} cm with {n} conical depressions, each of radius {dec(cr)} cm and depth {dec(ch)} cm, to hold pens. Find the volume of wood in the stand (π = 22/7).', f'{pistr(V)} cm³',
             f'Cuboid = {dec(l * b * h)}; each cone = ⅓ × 22/7 × {dec(cr)}² × {dec(ch)} = {pistr(PI * cr * cr * ch / 3)}; wood = {dec(l * b * h)} − {n} × {pistr(PI * cr * cr * ch / 3)} = {pistr(V)} cm³ (3 marks).')


def c12s2_hollow(r):
    rr = r.choice([Fr(7, 2), Fr(7), Fr(21, 4), Fr(7, 4)])
    h = r.choice([Fr(10), Fr(14), Fr(20)])
    V = PI * rr * rr * h - 2 * PI * rr ** 3 / 3
    return Q(f'A hemisphere of radius {dec(rr)} cm is scooped out from one end of a solid cylinder of height {dec(h)} cm and the same radius. Find the volume of the remaining solid (π = 22/7).', f'{pistr(V)} cm³',
             f'V = πr²h − ⅔πr³ = {pistr(PI * rr * rr * h)} − {pistr(2 * PI * rr ** 3 / 3)} = {pistr(V)} cm³.',
             [f'{pistr(PI * rr * rr * h + 2 * PI * rr ** 3 / 3)} cm³', f'{pistr(PI * rr * rr * h - 4 * PI * rr ** 3 / 3)} cm³', f'{pistr(PI * rr * rr * h)} cm³'])


def c12s2_gulab(r):
    n = r.choice([30, 40, 45, 50, 60])
    L, d = r.choice([(5, Fr(14, 5)), (6, Fr(14, 5)), (5, Fr(7, 2)), (7, Fr(7, 2))])
    rr = d / 2
    h = L - d
    one = PI * rr * rr * h + 4 * PI * rr ** 3 / 3
    pct = r.choice([20, 25, 30])
    syrup = n * one * pct / 100
    return Q(f'Gulab jamuns contain sugar syrup up to about {pct}% of their volume. Each gulab jamun is a cylinder with two hemispherical ends, of length {L} cm and diameter {dec(d)} cm. Find approximately how much syrup is in {n} gulab jamuns (π = 22/7).',
             f'about {dec(syrup, 0)} cm³', f'Cylinder length = {L} − {dec(d)} = {dec(h)}; volume of one = πr²h + 4/3 πr³ ≈ {dec(one)} cm³; syrup = {n} × {dec(one)} × {pct}/100 ≈ {dec(syrup, 0)} cm³ (4 marks).')


def c12s2_mcq(r):
    return mcqbank([
        ('The volume of a hemisphere of radius r is …', '⅔πr³', ['4/3 πr³', '2πr²', '⅓πr³'], 'Half of 4/3 πr³.'),
        ('A cone and a cylinder have the same base and height. The ratio of their volumes is …', '1 : 3', ['3 : 1', '1 : 2', '2 : 3'], '⅓πr²h : πr²h.'),
        ('A solid is made of a cylinder with a cone on top. Its volume is …', 'volume of cylinder + volume of cone', ['volume of cylinder − volume of cone', 'TSA of cylinder + TSA of cone', 'volume of cylinder only'], 'Volumes add, unlike surface areas.'),
        ('A cone, a hemisphere and a cylinder have equal bases and equal heights (h = r). Their volumes are in the ratio …', '1 : 2 : 3', ['1 : 3 : 2', '3 : 2 : 1', '2 : 1 : 3'], '⅓πr³ : ⅔πr³ : πr³.'),
    ])(r)


def c12s2_ar(r):
    return arbank([
        ('The volume of a solid made of a cone on a hemisphere is the sum of their volumes.', 'Volume is additive for solids joined without overlap.', 'a', 'R explains A.'),
        ('When a cone is hollowed out of a cylinder, the volume of the remaining solid is ⅔ of the cylinder.', 'The volume of a cone is ⅓ of a cylinder with the same base and height.', 'a', 'Remaining = 1 − ⅓.'),
        ('The volume of a capsule is πr²h + 2πr³.', 'Two hemispheres make one sphere of volume 4/3 πr³.', 'd', 'It is πr²h + 4/3 πr³; A false, R true.'),
    ])(r)


def c12s2_explain(r):
    return xbank([
        ('Explain why, for a combination of solids, volumes are simply added though surface areas are not.', 'Joining hides surfaces but does not remove any space occupied; total space = sum of parts.', '2 marks.'),
        ('Explain how to find the volume of wood in a pen stand with conical depressions.', 'Volume of cuboid minus the total volume of the conical depressions.', '2 marks.'),
    ])(r)


def c12s2_case(r):
    rr = r.choice([Fr(7, 2), Fr(7)])
    h = r.choice([Fr(6), Fr(9), Fr(12)])
    k = r.choice([10, 20, 50])
    one = PI * rr * rr * h / 3 + 2 * PI * rr ** 3 / 3
    return Q((f'An ice-cream cone is filled completely with ice cream and topped with a hemisphere of ice cream. The cone has radius {dec(rr)} cm and height {dec(h)} cm (π = 22/7). '
              f'(i) Find the volume of the cone. (ii) Find the volume of the hemispherical top. (iii) Find the total ice cream in one cone. (iv) How much ice cream is needed for {k} such cones (in litres)?'),
             f'(i) {pistr(PI * rr * rr * h / 3)} cm³ (ii) {pistr(2 * PI * rr ** 3 / 3)} cm³ (iii) {pistr(one)} cm³ (iv) {dec(one * k / 1000, 3)} litres', '1 mark each part.')


# st3 real life

def c12s3_tentcost(r):
    rr, hc, l = cone(r, 14)
    h = r.choice([Fr(2), Fr(3), Fr(4), Fr(21, 10)])
    rate = r.choice([100, 200, 300, 500, 150])
    A = 2 * PI * rr * h + PI * rr * l
    return Q(f'A tent for a school camp is a cylinder of height {dec(h)} m and base radius {dec(rr)} m surmounted by a cone of slant height {dec(l)} m. Find the cost of the canvas at ₹{rate} per m² (π = 22/7).', inr(float(A * rate)),
             f'Canvas = 2πrh + πrl = {pistr(2 * PI * rr * h)} + {pistr(PI * rr * l)} = {pistr(A)} m²; cost = {pistr(A)} × {rate} = {inr(float(A * rate))} (4 marks).')


def c12s3_vessel(r):
    rr = r.choice([Fr(7), Fr(21, 2), Fr(14), Fr(7, 2)])
    H = r.choice([Fr(13), Fr(20), Fr(25), Fr(30)])
    if H <= rr:
        raise ValueError
    h = H - rr
    V = 2 * PI * rr ** 3 / 3 + PI * rr * rr * h
    return Q(f'A vessel is a hollow hemisphere of diameter {dec(2 * rr)} cm mounted by a hollow cylinder of the same diameter. The total height of the vessel is {dec(H)} cm. Find the capacity of the vessel in litres (π = 22/7).',
             f'{dec(V / 1000, 3)} litres', f'Cylinder height = {dec(H)} − {dec(rr)} = {dec(h)}; V = ⅔πr³ + πr²h = {pistr(2 * PI * rr ** 3 / 3)} + {pistr(PI * rr * rr * h)} = {pistr(V)} cm³ = {dec(V / 1000, 3)} L (4 marks).',
             [f'{dec((PI * rr * rr * H) / 1000, 3)} litres', f'{dec((4 * PI * rr ** 3 / 3 + PI * rr * rr * h) / 1000, 3)} litres', f'{dec(V / 100, 3)} litres'])


def c12s3_tank(r):
    rr = r.choice([Fr(7, 10), Fr(7, 5), Fr(21, 10), Fr(7, 2)])
    h = r.choice([Fr(2), Fr(3), Fr(4), Fr(5)])
    V = PI * rr * rr * h + 2 * PI * rr ** 3 / 3
    return Q(f'A water tank is a cylinder of radius {dec(rr)} m and height {dec(h)} m with a hemispherical bottom of the same radius. How many litres of water can it hold (π = 22/7)?', f'{dec(V * 1000, 1)} litres',
             f'V = πr²h + ⅔πr³ = {dec(V, 4)} m³; 1 m³ = 1000 L ⇒ {dec(V * 1000, 1)} L (3 marks).',
             [f'{dec(V * 100, 1)} litres', f'{dec((PI * rr * rr * h) * 1000, 1)} litres', f'{dec((PI * rr * rr * h + 4 * PI * rr ** 3 / 3) * 1000, 1)} litres'])


def c12s3_paint(r):
    rr, h, l = cone(r)
    rate = r.choice([2, 3, 5, 7])
    A = PI * rr * l + 2 * PI * rr * rr
    return Q(f'A wooden toy top is a cone of radius {dec(rr)} cm and slant height {dec(l)} cm on a hemisphere of the same radius. Find the cost of painting it at ₹{rate} per 10 cm² (π = 22/7).', inr(float(A * rate / 10)),
             f'SA = πrl + 2πr² = {pistr(A)} cm²; cost = {pistr(A)} × {rate}/10 = {inr(float(A * rate / 10))} (3 marks).')


def c12s3_mcq(r):
    return mcqbank([
        ('1 m³ is equal to …', '1000 litres', ['100 litres', '10 litres', '10000 litres'], '1 L = 1000 cm³ and 1 m³ = 10⁶ cm³.'),
        ('To find the canvas needed for a tent (cylinder with conical top), we add …', 'CSA of cylinder and CSA of cone', ['TSA of cylinder and TSA of cone', 'volume of cylinder and cone', 'CSA of cylinder and base area'], 'Floor is not canvas; joined circle hidden.'),
        ('The capacity of a vessel is measured by its …', 'volume', ['curved surface area', 'total surface area', 'perimeter'], 'Capacity is the space inside.'),
        ('1 litre equals …', '1000 cm³', ['100 cm³', '10 cm³', '1 m³'], 'Definition.'),
    ])(r)


def c12s3_ar(r):
    return arbank([
        ('The cost of canvas for a tent depends on its surface area, not its volume.', 'Canvas covers the surface of the tent.', 'a', 'R explains A.'),
        ('A tank of volume 2.2 m³ holds 2200 litres.', '1 m³ = 1000 litres.', 'a', 'R explains A.'),
        ('The cost of painting a solid toy depends on its volume.', 'Paint covers only the outer surface.', 'd', 'It depends on surface area; A false, R true.'),
    ])(r)


def c12s3_explain(r):
    return xbank([
        ('Explain whether you need surface area or volume to find (a) the cost of painting a water tank and (b) how much water it holds.', '(a) surface area (b) volume (capacity).', '2 marks.'),
        ('Explain why the floor of a tent is not included when finding the canvas required.', 'The tent stands on the ground; only the curved surfaces are covered with canvas.', '2 marks.'),
    ])(r)


def c12s3_case(r):
    rr = r.choice([Fr(7, 4), Fr(7, 2)])
    h = r.choice([Fr(5), Fr(8), Fr(10)])
    n = r.choice([100, 500, 1000])
    V = PI * rr * rr * h + 4 * PI * rr ** 3 / 3
    A = 2 * PI * rr * h + 4 * PI * rr * rr
    return Q((f'A pharmaceutical company makes capsules: each is a cylinder of length {dec(h)} mm with hemispherical ends of radius {dec(rr)} mm (π = 22/7). '
              f'(i) Find the total length of a capsule. (ii) Find the volume of medicine one capsule holds. (iii) Find the surface area of one capsule shell. (iv) Find the medicine needed for {n} capsules in cm³.'),
             f'(i) {dec(h + 2 * rr)} mm (ii) {pistr(V)} mm³ (iii) {pistr(A)} mm² (iv) {dec(V * n / 1000, 3)} cm³', '1 mark each part.')


# ---------------- ch13 Statistics ----------------

def table(r, k=None, lo=2, hi=20):
    k = k or r.choice([5, 5, 6, 7])
    h = r.choice([5, 10, 10, 20])
    a0 = r.choice([0, 0, 10, 20, 100, 5]) if h != 20 else r.choice([0, 100, 20])
    a0 -= a0 % h
    cls = [(a0 + i * h, a0 + (i + 1) * h) for i in range(k)]
    f = [r.randint(lo, hi) for _ in range(k)]
    return cls, f, h


def ctxt(cls, f, what='Class interval', fw='Frequency'):
    return f'{what}: ' + ', '.join(f'{a}–{b}' for a, b in cls) + f'; {fw}: ' + ', '.join(map(str, f))


CTX13 = [('Marks', 'Number of students'), ('Daily wages (₹)', 'Number of workers'), ('Age (years)', 'Number of patients'), ('Weight (kg)', 'Number of students'),
         ('Daily pocket allowance (₹)', 'Number of children'), ('Length of leaves (mm)', 'Number of leaves'), ('Monthly electricity units', 'Number of consumers')]


def c13s1_mean(r):
    cls, f, h = table(r)
    what, fw = r.choice(CTX13)
    xs = [Fr(a + b, 2) for a, b in cls]
    N, Sx = sum(f), sum(fi * x for fi, x in zip(f, xs))
    m = Sx / N
    method = r.choice(['direct method', 'assumed mean method', 'step-deviation method'])
    A = xs[len(xs) // 2]
    if method == 'direct method':
        key = f'Class marks {", ".join(dec(x) for x in xs)}; Σf = {N}, Σfx = {dec(Sx)}; mean = Σfx/Σf = {ds(m)}.'
    elif method == 'assumed mean method':
        Sd = sum(fi * (x - A) for fi, x in zip(f, xs))
        key = f'Take a = {dec(A)}; d = x − a; Σf = {N}, Σfd = {dec(Sd)}; mean = a + Σfd/Σf = {dec(A)} + ({dec(Sd)})/{N} = {ds(m)}.'
    else:
        Su = sum(fi * (x - A) / h for fi, x in zip(f, xs))
        key = f'a = {dec(A)}, h = {h}, u = (x − a)/h; Σf = {N}, Σfu = {dec(Su)}; mean = a + h × Σfu/Σf = {ds(m)}.'
    return Q(f'Find the mean of the following data using the {method}. {ctxt(cls, f, what, fw)}.', ds(m), key + ' (3 marks)',
             num_distractors(float(m), float(sum(xs) / len(xs)), float(A), float(m) + h / 2))


def c13s1_missing(r):
    for _ in range(200):
        cls, f, h = table(r, k=5)
        j = r.randrange(5)
        xs = [Fr(a + b, 2) for a, b in cls]
        N, Sx = sum(f), sum(fi * x for fi, x in zip(f, xs))
        m = Sx / N
        if (m * 100).denominator == 1 and xs[j] != m:
            break
    else:
        raise ValueError
    what, fw = r.choice(CTX13)
    shown = [str(v) if i != j else 'p' for i, v in enumerate(f)]
    return Q(f'The mean of the following distribution is {dec(m)}. Find the missing frequency p. {what}: ' + ', '.join(f'{a}–{b}' for a, b in cls) + f'; {fw}: ' + ', '.join(shown) + '.', f'p = {f[j]}',
             f'Σf = {N - f[j]} + p; Σfx = {dec(Sx - f[j] * xs[j])} + {dec(xs[j])}p. ({dec(Sx - f[j] * xs[j])} + {dec(xs[j])}p)/({N - f[j]} + p) = {dec(m)} ⇒ p = {f[j]} (4 marks).')


def c13s1_mcq(r):
    return mcqbank([
        ('The class mark of the class 10–25 is …', '17.5', ['15', '12.5', '35'], '(10 + 25)/2.'),
        ('In the assumed mean method, mean = …', 'a + Σfᵢdᵢ/Σfᵢ', ['a − Σfᵢdᵢ/Σfᵢ', 'Σfᵢdᵢ/Σfᵢ', 'a × Σfᵢdᵢ/Σfᵢ'], 'dᵢ = xᵢ − a.'),
        ('In the step-deviation method, uᵢ = …', '(xᵢ − a)/h', ['(xᵢ + a)/h', 'xᵢ − a', 'h(xᵢ − a)'], 'Definition.'),
        ('For calculating the mean of grouped data, we assume that the frequency of each class is centred at …', 'its class mark', ['its upper limit', 'its lower limit', 'the modal class'], 'Assumption.'),
        ('If each observation is increased by 5, the mean …', 'increases by 5', ['stays the same', 'is multiplied by 5', 'increases by 5 times the number of observations'], 'Shift of origin.'),
    ])(r)


def c13s1_ar(r):
    return arbank([
        ('The direct, assumed mean and step-deviation methods give the same mean.', 'They differ only by a change of origin and scale that is undone at the end.', 'a', 'R explains A.'),
        ('The step-deviation method is convenient when all class widths are equal.', 'Then every deviation dᵢ is a multiple of the common width h.', 'a', 'R explains A.'),
        ('The mean of grouped data is always exactly equal to the mean of the raw data.', 'We assume all values in a class are at the class mark.', 'd', 'It is an approximation; A false, R true.'),
    ])(r)


def c13s1_explain(r):
    return xbank([
        ('Explain why the mean of grouped data is only an estimate.', 'Each value in a class is replaced by the class mark; actual values may differ.', '2 marks.'),
        ('Explain the advantage of the step-deviation method over the direct method.', 'Dividing deviations by h makes the numbers small, reducing calculation.', '2 marks.'),
        ('Explain how to choose the assumed mean a.', 'Choose a class mark near the middle of the data, so deviations are small.', '2 marks.'),
    ])(r)


def c13s1_case(r):
    cls, f, h = table(r, k=5, lo=3, hi=15)
    xs = [Fr(a + b, 2) for a, b in cls]
    N, Sx = sum(f), sum(fi * x for fi, x in zip(f, xs))
    A = xs[2]
    Su = sum(fi * (x - A) / h for fi, x in zip(f, xs))
    return Q((f'A survey of daily water use (in litres, per person) of {N} families in a colony gave: {ctxt(cls, f, "Water used (L)", "Number of families")}. '
              f'(i) Find the class marks. (ii) Taking a = {dec(A)} and h = {h}, find Σfu. (iii) Find the mean water use. (iv) Which class contains the mean?'),
             f'(i) {", ".join(dec(x) for x in xs)} (ii) {dec(Su)} (iii) {ds(Sx / N)} L (iv) ' + next(f'{a}–{b}' for a, b in cls if a <= Sx / N < b), '1 mark each part.')


# st2 mode

def mode_data(r):
    while True:
        cls, f, h = table(r)
        j = max(range(len(f)), key=lambda i: f[i])
        if 0 < j < len(f) - 1 and f.count(f[j]) == 1:
            f0, f1, f2 = f[j - 1], f[j], f[j + 1]
            mo = cls[j][0] + Fr(f1 - f0, 2 * f1 - f0 - f2) * h
            return cls, f, h, j, f0, f1, f2, mo


def c13s2_mode(r):
    cls, f, h, j, f0, f1, f2, mo = mode_data(r)
    what, fw = r.choice(CTX13)
    return Q(f'Find the mode of the following data. {ctxt(cls, f, what, fw)}.', ds(mo),
             f'Modal class {cls[j][0]}–{cls[j][1]} (highest frequency {f1}); l = {cls[j][0]}, f₁ = {f1}, f₀ = {f0}, f₂ = {f2}, h = {h}. Mode = l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h = {cls[j][0]} + {f1 - f0}/{2 * f1 - f0 - f2} × {h} = {ds(mo)} (3 marks).',
             num_distractors(float(mo), float(cls[j][0] + Fr(f1 - f0, f1 + f2) * h), float(Fr(sum(cls[j]), 2)), float(cls[j][1])))


def c13s2_modal(r):
    cls, f, h, j, *_ = mode_data(r)
    what, fw = r.choice(CTX13)
    others = [f'{a}–{b}' for a, b in cls if (a, b) != cls[j]]
    return mcq(f'For the data {ctxt(cls, f, what, fw)}, the modal class is …', f'{cls[j][0]}–{cls[j][1]}', r.sample(others, 3), 'The class with the highest frequency.', r)


def c13s2_mcq(r):
    return mcqbank([
        ('The mode of grouped data is given by …', 'l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h', ['l + (n/2 − cf)/f × h', 'l + (f₁ − f₀)/(f₁ + f₂) × h', 'a + h Σfu/Σf'], 'Mode formula.'),
        ('In the mode formula, f₀ is the frequency of …', 'the class preceding the modal class', ['the modal class', 'the class succeeding the modal class', 'the first class'], 'Definition.'),
        ('The modal class is the class with …', 'the maximum frequency', ['the maximum class mark', 'the median', 'the minimum frequency'], 'Definition.'),
        ('A data set can have …', 'more than one mode', ['only one mode always', 'no mean', 'only one median and no mode ever'], 'Two classes may share the highest frequency.'),
    ])(r)


def c13s2_ar(r):
    return arbank([
        ('The mode always lies in the modal class.', 'In the formula, (f₁ − f₀)/(2f₁ − f₀ − f₂) lies between 0 and 1 when f₁ is the largest frequency.', 'a', 'So l ≤ mode ≤ l + h.'),
        ('The modal class is the class with the largest class mark.', 'The modal class has the highest frequency.', 'd', 'A false, R true.'),
        ('Mode is the most suitable measure for the most popular shoe size.', 'Mode gives the most frequent value.', 'a', 'R explains A.'),
    ])(r)


def c13s2_explain(r):
    return xbank([
        ('Explain why the mode of grouped data lies in the modal class.', 'With f₁ greater than f₀ and f₂, the fraction (f₁ − f₀)/(2f₁ − f₀ − f₂) is between 0 and 1, so the mode is between l and l + h.', '2 marks.'),
        ('Explain the meaning of each letter in the mode formula l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h.', 'l: lower limit of modal class; f₁: its frequency; f₀, f₂: frequencies of the classes before and after; h: class size.', '2 marks.'),
    ])(r)


def c13s2_case(r):
    cls, f, h, j, f0, f1, f2, mo = mode_data(r)
    return Q((f'A shopkeeper in {r.choice(CITIES)} records the number of customers by amount spent: {ctxt(cls, f, "Amount spent (₹)", "Number of customers")}. '
              f'(i) Identify the modal class. (ii) Write l, f₀, f₁, f₂ and h. (iii) Find the mode. (iv) Interpret the mode for the shopkeeper.'),
             f'(i) {cls[j][0]}–{cls[j][1]} (ii) l = {cls[j][0]}, f₀ = {f0}, f₁ = {f1}, f₂ = {f2}, h = {h} (iii) ₹{ds(mo)} (iv) the most common amount spent is about ₹{dec(mo, 0)}', '1 mark each part.')


# st3 median

def med_data(r, k=None):
    cls, f, h = table(r, k=k)
    N = sum(f)
    cf, c = [], 0
    for x in f:
        c += x
        cf.append(c)
    j = next(i for i, c in enumerate(cf) if c >= Fr(N, 2))
    prev = cf[j - 1] if j else 0
    med = cls[j][0] + (Fr(N, 2) - prev) / f[j] * h
    return cls, f, h, N, cf, j, prev, med


def c13s3_median(r):
    cls, f, h, N, cf, j, prev, med = med_data(r)
    what, fw = r.choice(CTX13)
    return Q(f'Find the median of the following data. {ctxt(cls, f, what, fw)}.', ds(med),
             f'n = {N}, n/2 = {dec(Fr(N, 2))}; cumulative frequencies {", ".join(map(str, cf))}; median class {cls[j][0]}–{cls[j][1]}; l = {cls[j][0]}, cf = {prev}, f = {f[j]}, h = {h}. Median = l + (n/2 − cf)/f × h = {ds(med)} (3 marks).',
             num_distractors(float(med), float(cls[j][0] + (Fr(N, 2) - cf[j]) / f[j] * h), float(Fr(sum(cls[j]), 2)), float(cls[j][1])))


def c13s3_class(r):
    cls, f, h, N, cf, j, prev, med = med_data(r)
    others = [f'{a}–{b}' for a, b in cls if (a, b) != cls[j]]
    return mcq(f'For the data {ctxt(cls, f)}, the median class is …', f'{cls[j][0]}–{cls[j][1]}', r.sample(others, 3),
               f'n/2 = {dec(Fr(N, 2))}; the first cumulative frequency ≥ n/2 is {cf[j]}.', r)


def c13s3_missing(r):
    for _ in range(300):
        cls, f, h, N, cf, j, prev, med = med_data(r, k=r.choice([5, 6]))
        if 1 <= j <= len(f) - 2 and (med * 100).denominator == 1 and cls[j][0] < med < cls[j][1]:
            break
    else:
        raise ValueError
    x, y = f[j - 1], f[j + 1]
    shown = [str(v) for v in f]
    shown[j - 1], shown[j + 1] = 'x', 'y'
    return Q(f'The median of the following data is {dec(med)} and the total frequency is {N}. Find x and y. Class interval: ' + ', '.join(f'{a}–{b}' for a, b in cls) + '; Frequency: ' + ', '.join(shown) + '.',
             f'x = {x}, y = {y}', f'Median class {cls[j][0]}–{cls[j][1]} (it contains {dec(med)}); cf before it = {prev - x} + x. {dec(med)} = {cls[j][0]} + ({dec(Fr(N, 2))} − ({prev - x} + x))/{f[j]} × {h} ⇒ x = {x}; then y = {N} − {N - x - y} − {x} = {y} (5 marks).')


def c13s3_mcq(r):
    return mcqbank([
        ('The median of grouped data is given by …', 'l + ((n/2 − cf)/f) × h', ['l + (f₁ − f₀)/(2f₁ − f₀ − f₂) × h', 'a + h Σfu/Σf', 'l + (n − cf)/f × h'], 'Median formula.'),
        ('In the median formula, cf is …', 'the cumulative frequency of the class preceding the median class', ['the cumulative frequency of the median class', 'the frequency of the median class', 'the total frequency'], 'Definition.'),
        ('The median class is the class whose cumulative frequency is …', 'the first to be greater than or equal to n/2', ['the largest', 'equal to n', 'less than n/2'], 'Definition.'),
        ('To find the median of grouped data we first make a … table.', 'cumulative frequency', ['class mark', 'deviation', 'tally only'], 'Needed to locate n/2.'),
    ])(r)


def c13s3_ar(r):
    return arbank([
        ('The median divides the data into two equal halves.', 'Half the observations lie below the median and half above.', 'a', 'R explains A.'),
        ('The median class is the class with the highest frequency.', 'The median class contains the (n/2)th observation.', 'd', 'A describes the modal class; A false, R true.'),
        ('The median is not affected much by a few very large values.', 'The median depends on the position of the middle observation.', 'a', 'R explains A.'),
    ])(r)


def c13s3_explain(r):
    return xbank([
        ('Explain how to locate the median class in grouped data.', 'Make cumulative frequencies, find n/2, and take the first class whose cumulative frequency is at least n/2.', '2 marks.'),
        ('Explain why cf in the median formula is the cumulative frequency of the class before the median class.', 'We count observations below the median class, then interpolate within the class.', '2 marks.'),
    ])(r)


def c13s3_case(r):
    cls, f, h, N, cf, j, prev, med = med_data(r, k=5)
    return Q((f'The heights (in cm) of {N} plants in a school nursery are: {ctxt(cls, f, "Height (cm)", "Number of plants")}. '
              f'(i) Write the cumulative frequencies. (ii) Find n/2 and the median class. (iii) Find the median height. (iv) How many plants are shorter than {cls[j][0]} cm?'),
             f'(i) {", ".join(map(str, cf))} (ii) {dec(Fr(N, 2))}; {cls[j][0]}–{cls[j][1]} (iii) {ds(med)} cm (iv) {prev}', '1 mark each part.')


# st4 choosing measures

def c13s4_emp(r):
    mean = r.randint(20, 80)
    d = r.choice([1, 2, 3, 4, 5, Fr(3, 2), Fr(5, 2)])
    med = mean + d * r.choice([1, -1])
    mode = 3 * med - 2 * mean
    which = r.choice(['mode', 'mean', 'median'])
    if which == 'mode':
        return Q(f'For a moderately skewed distribution, the mean is {dec(mean)} and the median is {dec(med)}. Using the empirical relationship, find the mode.', dec(mode),
                 f'3 Median = Mode + 2 Mean ⇒ Mode = 3 × {dec(med)} − 2 × {dec(mean)} = {dec(mode)}.', num_distractors(float(mode), float(3 * mean - 2 * med), float(med), float(mode) + 1))
    if which == 'mean':
        return Q(f'For a moderately skewed distribution, the mode is {dec(mode)} and the median is {dec(med)}. Using the empirical relationship, find the mean.', dec(mean),
                 f'Mean = (3 × Median − Mode)/2 = (3 × {dec(med)} − {dec(mode)})/2 = {dec(mean)}.', num_distractors(float(mean), float(med), float(Fr(3 * med + mode, 2)), float(mean) + 1))
    return Q(f'For a moderately skewed distribution, the mode is {dec(mode)} and the mean is {dec(mean)}. Using the empirical relationship, find the median.', dec(med),
             f'Median = (Mode + 2 Mean)/3 = ({dec(mode)} + 2 × {dec(mean)})/3 = {dec(med)}.', num_distractors(float(med), float(Fr(mode + mean, 2)), float(mean), float(med) + 1))


def c13s4_mcq(r):
    return mcqbank([
        ('The most appropriate measure for the most popular size of shirt sold in a shop is …', 'mode', ['mean', 'median', 'range'], 'Most frequent value.'),
        ('When there are a few extreme values, the most suitable measure of central tendency is usually …', 'median', ['mean', 'mode', 'sum'], 'Median is not affected by extremes.'),
        ('To compare the average marks of two sections, we generally use …', 'mean', ['mode', 'cumulative frequency', 'modal class'], 'Mean uses all observations.'),
        ('The empirical relationship between the three measures is …', '3 Median = Mode + 2 Mean', ['3 Mean = Mode + 2 Median', '2 Median = Mode + 3 Mean', 'Mode = Mean + Median'], 'Moderately skewed data.'),
        ('Which measure can be found from a cumulative frequency table directly?', 'median', ['mode', 'mean', 'range'], 'Uses positions.'),
    ])(r)


def c13s4_ar(r):
    return arbank([
        ('The median is a better average than the mean for incomes in a village with a few very rich families.', 'The mean is pulled up by extreme values; the median is not.', 'a', 'R explains A.'),
        ('If mean = 20 and median = 22, then mode = 26.', '3 Median = Mode + 2 Mean.', 'a', '66 − 40 = 26.'),
        ('Mode can be used for data that is not numerical, such as favourite colours.', 'The mean of grouped data uses class marks.', 'b', 'Both true; R does not explain A.'),
    ])(r)


def c13s4_explain(r):
    return xbank([
        ('A cricket coach wants a typical score for a batter who has a few very high scores. Which measure should he use? Explain.', 'Median, because a few very high scores raise the mean.', '2 marks.'),
        ('A shoe company wants to know which size to make most of. Which measure should it use? Explain.', 'Mode, the most frequent size.', '2 marks.'),
        ('Explain when the mean is the best measure of central tendency.', 'When the data has no extreme values and we want all observations to count, e.g. comparing averages.', '2 marks.'),
        ('Explain why the empirical relationship 3 Median = Mode + 2 Mean is only approximate.', 'It is observed for moderately skewed distributions; it is not a theorem for all data.', '2 marks.'),
    ])(r)


def c13s4_case(r):
    mean = r.randint(30, 60)
    med = mean + r.choice([1, 2, 3])
    mode = 3 * med - 2 * mean
    return Q((f'A report on the daily earnings (₹ hundreds) of shopkeepers in a market gives mean {mean} and median {med}. '
              f'(i) Use the empirical relation to estimate the mode. (ii) Which measure tells the most common earning? (iii) If one shopkeeper earns far more than all others, which measure is most affected? (iv) Which measure would you report as a "typical" earning? Why?'),
             f'(i) {mode} (ii) mode (iii) mean (iv) median, as it is not affected by extreme values', '1 mark each part.')


# ---------------- ch14 Probability ----------------

DECK = [
    ('a red card', 26), ('a black card', 26), ('a king', 4), ('a red king', 2), ('a face card', 12), ('a red face card', 6), ('an ace', 4), ('a spade', 13),
    ('a heart', 13), ('the queen of diamonds', 1), ('the jack of hearts', 1), ('a black face card', 6), ('a card that is not a face card', 40), ('a card that is not an ace', 48),
    ('a red ace', 2), ('a king or a queen', 8), ('a spade or an ace', 16), ('neither a king nor a queen', 44), ('the 2 of spades', 1), ('a red card that is not a face card', 20),
    ('a black king', 2), ('a diamond', 13), ('a numbered card (2 to 10)', 36), ('a club that is a face card', 3),
]


def c14s3_card(r):
    ev, k = r.choice(DECK)
    return Q(f'One card is drawn at random from a well-shuffled deck of 52 playing cards. Find the probability of getting {ev}.', frac(k, 52),
             f'Favourable outcomes {k}, total 52: P = {k}/52' + ('' if frac(k, 52) == f'{k}/52' else f' = {frac(k, 52)}') + '.', [frac(k, 48) if frac(k, 48) != frac(k, 52) else frac(k + 1, 52), frac(52 - k, 52), frac(k, 26) if k < 26 else frac(k - 4, 52)])


def c14s3_removed(r):
    rem, n_rem, evs = r.choice([
        ('all the face cards are removed', 12, [('a red card', 20), ('an ace', 4), ('a spade', 10), ('a number card less than 5 (aces count as 1)', 16)]),
        ('the four aces are removed', 4, [('a king', 4), ('a red card', 24), ('a face card', 12), ('a heart', 12)]),
        ('all the red face cards are removed', 6, [('a red card', 20), ('a face card', 6), ('a king', 2), ('a black card', 26)]),
        ('the king, queen and jack of clubs are removed', 3, [('a club', 10), ('a face card', 9), ('a heart', 13), ('a red king', 2)]),
    ])
    ev, k = r.choice(evs)
    tot = 52 - n_rem
    return Q(f'From a deck of 52 playing cards, {rem}. A card is then drawn at random from the remaining cards. Find the probability that it is {ev}.', frac(k, tot),
             f'Remaining cards = {tot}; favourable = {k}; P = {frac(k, tot)} (3 marks).', [frac(k, 52), frac(tot - k, tot), frac(k + 1, tot)])


def c14s3_dice(r):
    evs = [('a doublet (the same number on both dice)', lambda a, b: a == b), ('a sum less than 6', lambda a, b: a + b < 6), ('a sum that is a prime number', lambda a, b: a + b in (2, 3, 5, 7, 11)),
           ('a difference of 2 between the numbers', lambda a, b: abs(a - b) == 2), ('a sum of at least 10', lambda a, b: a + b >= 10), ('a 6 on at least one die', lambda a, b: 6 in (a, b)),
           ('a sum that is a multiple of 3', lambda a, b: (a + b) % 3 == 0), ('a product less than 9', lambda a, b: a * b < 9), ('a sum of 13', lambda a, b: a + b == 13),
           ('a sum that is a perfect square', lambda a, b: a + b in (4, 9)), ('the first number greater than the second', lambda a, b: a > b)]
    ev, f = r.choice(evs)
    k = sum(1 for a in range(1, 7) for b in range(1, 7) if f(a, b))
    return Q(f'Two dice are thrown at the same time. Find the probability of getting {ev}.', frac(k, 36) if k else '0',
             f'There are 36 equally likely outcomes; favourable outcomes = {k}; P = {frac(k, 36) if k else "0 (impossible event)"}.', [frac(k + 1, 36), frac(36 - k, 36) if k != 18 else frac(1, 3), frac(k, 12) if k <= 12 and frac(k, 12) != frac(k, 36) else frac(k + 2, 36)])


def c14s3_mcq(r):
    return mcqbank([
        ('The number of face cards in a deck of 52 cards is …', '12', ['16', '4', '13'], 'J, Q, K in four suits.'),
        ('When two dice are thrown, the number of possible outcomes is …', '36', ['12', '6', '18'], '6 × 6.'),
        ('When a coin is tossed twice, the probability of at least one head is …', '3/4', ['1/2', '1/4', '1'], 'HH, HT, TH out of 4.'),
        ('The probability of getting a sum of 7 with two dice is …', '1/6', ['7/36', '1/12', '5/36'], '6 outcomes.'),
        ('The number of red cards in a deck of 52 cards is …', '26', ['13', '12', '24'], 'Hearts and diamonds.'),
    ])(r)


def c14s3_ar(r):
    return arbank([
        ('The probability of drawing a red king from a deck of 52 cards is 1/26.', 'There are 2 red kings in the deck.', 'a', '2/52 = 1/26.'),
        ('When two coins are tossed, the outcomes "two heads", "two tails" and "one of each" are equally likely.', 'There are four equally likely outcomes HH, HT, TH, TT.', 'd', 'P(one of each) = 1/2; A false, R true.'),
        ('The probability of getting a sum of 13 with two dice is 0.', 'The largest possible sum is 12.', 'a', 'Impossible event.'),
        ('A card drawn from a deck is a face card with probability 3/13.', 'Each suit has 13 cards.', 'b', 'Both true; R alone does not explain 12/52.'),
    ])(r)


def c14s3_explain(r):
    return xbank([
        ('Explain why the outcomes of tossing two coins are not "0, 1 or 2 heads" with probability 1/3 each.', 'HT and TH are different outcomes; there are 4 equally likely outcomes, so P(1 head) = 1/2.', '2 marks.'),
        ('Explain how to count the outcomes when two dice are thrown.', 'Each of the 6 numbers on the first die can pair with each of the 6 on the second: 36 ordered pairs.', '2 marks.'),
        ('Explain the composition of a standard deck of 52 playing cards.', '4 suits (spades, clubs black; hearts, diamonds red) of 13 cards each: A, 2–10, J, Q, K; 12 face cards.', '2 marks.'),
    ])(r)


def c14s3_case(r):
    who1, who2 = two_names(r)
    t = r.choice([7, 8, 9, 6])
    k_ge = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= t)
    return Q((f'{who1} and {who2} play a game: two dice are thrown; {who1} scores a point if the sum is {t} or more, otherwise {who2} scores. '
              f'(i) Write the number of possible outcomes. (ii) Find P({who1} scores). (iii) Find P({who2} scores). (iv) Is the game fair? Explain.'),
             f'(i) 36 (ii) {frac(k_ge, 36)} (iii) {frac(36 - k_ge, 36)} (iv) ' + ('yes, both have probability 1/2' if k_ge == 18 else f'no, {who1 if k_ge > 18 else who2} has a better chance'),
             '1 mark each part.')


# st1 theoretical probability

def c14s1_word(r):
    w = r.choice(['ASSOCIATION', 'MATHEMATICS', 'PROBABILITY', 'EXAMINATION', 'INDEPENDENCE', 'BANANA', 'MISSISSIPPI', 'COMMITTEE'])
    vow = sum(1 for c in w if c in 'AEIOU')
    which = r.choice(['a vowel', 'a consonant'])
    k = vow if which == 'a vowel' else len(w) - vow
    return Q(f'A letter is chosen at random from the letters of the word "{w}". Find the probability that it is {which}.', frac(k, len(w)),
             f'{len(w)} letters, {vow} vowels; P = {k}/{len(w)}' + ('' if frac(k, len(w)) == f'{k}/{len(w)}' else f' = {frac(k, len(w))}') + '.', [frac(len(w) - k, len(w)), frac(k, 26), frac(k, 5) if k < 5 else frac(k + 1, len(w))])


def c14s1_disc(r):
    n = r.choice([20, 25, 30, 50, 90, 100])
    lo = 1
    ev = r.choice([('a two-digit number', lambda x: 10 <= x <= 99), ('a perfect square', lambda x: is_sq(x)), ('a number divisible by 5', lambda x: x % 5 == 0),
                   ('a prime number', lambda x: x > 1 and all(x % d for d in range(2, int(x ** .5) + 1))), ('an even number', lambda x: x % 2 == 0), ('a multiple of 7', lambda x: x % 7 == 0)])
    k = sum(1 for x in range(lo, n + 1) if ev[1](x))
    return Q(f'A box contains {n} discs numbered 1 to {n}. One disc is drawn at random. Find the probability that it bears {ev[0]}.', frac(k, n),
             f'Favourable discs = {k}; P = {k}/{n} = {frac(k, n)}.', [frac(k + 1, n), frac(n - k, n), frac(k, n - 1)])


def c14s1_mcq(r):
    return mcqbank([
        ('The sum of the probabilities of all the elementary events of an experiment is …', '1', ['0', '0.5', 'the number of outcomes'], 'They cover every outcome once.'),
        ('An event having only one outcome of the experiment is called …', 'an elementary event', ['an impossible event', 'a sure event', 'a complementary event'], 'Definition.'),
        ('The theoretical probability of an event E is …', 'number of outcomes favourable to E ÷ number of all possible outcomes', ['number of trials ÷ number of successes', 'favourable − unfavourable', '1 ÷ favourable outcomes'], 'Definition (equally likely outcomes).'),
        ('A die is thrown once. The probability of getting a number less than 7 is …', '1', ['0', '6/7', '1/6'], 'Sure event.'),
        ('Which of the following cannot be the probability of an event?', '1.5', ['0', '2/3', '0.7'], '0 ≤ P(E) ≤ 1.'),
    ])(r)


def c14s1_ar(r):
    return arbank([
        ('When a die is thrown, the probability of getting 3 is 1/6.', 'All six outcomes are equally likely.', 'a', 'R explains A.'),
        ('The probability of an event can be 1.2.', 'For any event E, 0 ≤ P(E) ≤ 1.', 'd', 'A false, R true.'),
        ('The sum of probabilities of all elementary events of a coin toss is 1.', 'P(H) = P(T) = 1/2.', 'a', 'R shows A for the coin.'),
    ])(r)


def c14s1_explain(r):
    return xbank([
        ('Explain the difference between experimental and theoretical probability.', 'Experimental: based on actual trials (frequency ratio); theoretical: computed from equally likely outcomes, without doing the experiment.', '2 marks.'),
        ('A student says a cricket match is either won or lost, so P(win) = 1/2. Explain whether this is correct.', 'Not correct; the outcomes are not equally likely (and a match can also be drawn/tied).', '2 marks.'),
        ('Explain why the probability of an event lies between 0 and 1.', 'Favourable outcomes are at least 0 and at most the total number of outcomes.', '2 marks.'),
    ])(r)


def c14s1_case(r):
    a, b, c = r.randint(3, 10), r.randint(3, 10), r.randint(3, 10)
    tot = a + b + c
    return Q((f'A jar at a school fete contains {a} mango, {b} orange and {c} lemon-flavoured candies. A child picks one at random. '
              f'(i) How many outcomes are possible? (ii) Find P(orange). (iii) Find P(not lemon). (iv) Find P(mango) + P(orange) + P(lemon) and explain the result.'),
             f'(i) {tot} (ii) {frac(b, tot)} (iii) {frac(a + b, tot)} (iv) 1; the three are all the elementary outcomes', '1 mark each part.')


# st2 complementary

def c14s2_comp(r):
    kind = r.randint(0, 2)
    if kind == 0:
        p = Fr(r.randint(1, 99), 100)
        return Q(f'If P(E) = {dec(p)}, what is the probability of "not E"?', dec(1 - p), f'P(not E) = 1 − P(E) = 1 − {dec(p)} = {dec(1 - p)}.', num_distractors(float(1 - p), float(p), float(1 + p), float(1 - p) + 0.1))
    if kind == 1:
        p = Fr(r.randint(1, 12), r.randint(13, 25))
        return Q(f'The probability that it will rain tomorrow is {fn(p)}. What is the probability that it will not rain tomorrow?', fn(1 - p), f'1 − {fn(p)} = {fn(1 - p)}.', [fn(p), fn(1 + p) if 1 + p != 1 - p else '1', fn(Fr(1, 2))] if fn(1 - p) != '1/2' else [fn(p), '1', '0'])
    p = r.choice([5, 8, 10, 12, 15, 20, 25])
    return Q(f'The probability of a pen drawn at random from a lot being defective is {p}%. What is the probability that it is not defective?', f'{dec(Fr(100 - p, 100))}',
             f'P(not defective) = 1 − {dec(Fr(p, 100))} = {dec(Fr(100 - p, 100))}.', num_distractors(float(Fr(100 - p, 100)), p / 100, (100 + p) / 100, 1 - p / 1000))


def c14s2_defect(r):
    good = r.choice([120, 132, 144, 150, 180, 200])
    bad = r.choice([6, 8, 10, 12, 15, 20, 24])
    who = name(r)
    return Q(f'{bad} defective pens are accidentally mixed with {good} good ones. {who} takes out one pen at random. What is the probability that it is a good one?', frac(good, good + bad),
             f'Total {good + bad}; P(good) = {good}/{good + bad} = {frac(good, good + bad)}.', [frac(bad, good + bad), frac(good, good + 2 * bad), frac(good - bad, good + bad)])


def c14s2_mcq(r):
    return mcqbank([
        ('The probability of an impossible event is …', '0', ['1', '−1', '0.5'], 'No favourable outcomes.'),
        ('The probability of a sure event is …', '1', ['0', '0.5', 'more than 1'], 'Every outcome favourable.'),
        ('If P(E) = 0.05, then P(not E) = …', '0.95', ['0.05', '1.05', '0.5'], '1 − 0.05.'),
        ('Which of these is an impossible event when a die is thrown?', 'getting 8', ['getting an even number', 'getting a number less than 7', 'getting 1'], 'Faces show 1 to 6.'),
        ('Events E and "not E" are called …', 'complementary events', ['elementary events', 'sure events', 'impossible events'], 'Definition.'),
        ('P(E) + P(not E) = …', '1', ['0', '2', 'P(E)'], 'Complementary events.'),
    ])(r)


def c14s2_ar(r):
    return arbank([
        ('If P(E) = 0.3, then P(not E) = 0.7.', 'P(E) + P(not E) = 1.', 'a', 'R explains A.'),
        ('Getting a number greater than 6 on a die is an impossible event.', 'The probability of an impossible event is 0.', 'b', 'Both true; R states a property, not why the event is impossible.'),
        ('The probability of getting a number less than 7 on a die is 1.', 'Every outcome is favourable to a sure event, so its probability is 1.', 'a', 'All six outcomes are less than 7, so it is a sure event.'),
        ('If the probability of winning a game is 0.4, the probability of losing it is 0.4.', 'Winning and losing are complementary events here.', 'd', 'It is 0.6; A false, R true.'),
    ])(r)


def c14s2_explain(r):
    return xbank([
        ('Explain why P(E) + P(not E) = 1.', 'Every outcome is either favourable to E or to "not E", so the favourable counts add to the total.', '2 marks.'),
        ('Give one example each of a sure event and an impossible event for throwing a die.', 'Sure: a number less than 7; impossible: the number 8.', '2 marks.'),
        ('Explain how finding P(not E) first can make a probability easier to calculate, with an example.', 'e.g. P(at least one head in 3 tosses) = 1 − P(no head) = 1 − 1/8 = 7/8.', '2 marks.'),
    ])(r)


def c14s2_case(r):
    good = r.randint(100, 180)
    bad = r.randint(5, 20)
    return Q((f'A lot of {good + bad} electric bulbs at a shop in {r.choice(CITIES)} contains {bad} defective ones. One bulb is drawn at random. '
              f'(i) Find P(defective). (ii) Find P(not defective). (iii) Check that the two add to 1. (iv) If the bulb drawn is defective and not replaced, find the probability that the next bulb drawn is not defective.'),
             f'(i) {frac(bad, good + bad)} (ii) {frac(good, good + bad)} (iii) yes (complementary events) (iv) {frac(good, good + bad - 1)}', '1 mark each part.')


# st4 real life

def c14s4_piggy(r):
    c = {'50 p': r.choice([50, 100]), '₹1': r.choice([30, 50]), '₹2': r.choice([20, 25]), '₹5': r.choice([10, 15])}
    tot = sum(c.values())
    ev = r.choice([('a 50 p coin', c['50 p']), ('a ₹5 coin', c['₹5']), ('not a ₹5 coin', tot - c['₹5']), ('a ₹1 or ₹2 coin', c['₹1'] + c['₹2'])])
    return Q(f'A piggy bank contains {c["50 p"]} fifty-paise coins, {c["₹1"]} one-rupee coins, {c["₹2"]} two-rupee coins and {c["₹5"]} five-rupee coins. If it is equally likely that one of the coins falls out when it is turned upside down, what is the probability that the coin is {ev[0]}?',
             frac(ev[1], tot), f'Total coins {tot}; favourable {ev[1]}; P = {frac(ev[1], tot)}.', [frac(tot - ev[1], tot), frac(ev[1], tot - ev[1]), frac(1, 4) if frac(ev[1], tot) != '1/4' else frac(1, 3)])


def c14s4_fish(r):
    m, f = r.randint(3, 12), r.randint(3, 12)
    who = name(r)
    return Q(f'{who} buys a fish from a shop for an aquarium. The shopkeeper takes out one fish at random from a tank containing {m} male fish and {f} female fish. What is the probability that the fish is male?',
             frac(m, m + f), f'{m} out of {m + f}.', [frac(f, m + f), frac(m, f) if m != f else frac(1, 3), frac(1, 2) if frac(m, m + f) != '1/2' else frac(m + 1, m + f)])


def c14s4_tickets(r):
    n = r.choice([200, 500, 1000, 1500, 2000])
    k = r.choice([1, 2, 4, 5, 10, 20])
    who = name(r)
    return Q(f'In a lucky draw at a school fair, {n} tickets are sold and {k} prize{"s are" if k > 1 else " is"} to be given. {who} has bought one ticket. What is the probability that {who} wins a prize?', frac(k, n),
             f'{k} favourable out of {n}: {frac(k, n)}.', [frac(n - k, n), frac(1, n) if k > 1 else frac(2, n), frac(k, 100)])


def c14s4_game(r):
    who = name(r)
    kind = r.choice(['all same', 'two heads', 'at least two heads'])
    k = {'all same': 2, 'two heads': 3, 'at least two heads': 4}[kind]
    txt = {'all same': 'all three results are the same (three heads or three tails)', 'two heads': 'exactly two heads appear', 'at least two heads': 'at least two heads appear'}[kind]
    return Q(f'A game consists of tossing a one-rupee coin 3 times and noting the outcome each time. {who} wins if {txt}, and loses otherwise. Find the probability that {who} loses the game.', frac(8 - k, 8),
             f'8 equally likely outcomes; winning outcomes {k}; P(lose) = 1 − {frac(k, 8)} = {frac(8 - k, 8)} (3 marks).', [w for w in dict.fromkeys([frac(k, 8), frac(8 - k - 1, 8), '1/2', '3/8', '5/8', '1/4']) if w != frac(8 - k, 8)][:3])


def c14s4_ar(r):
    return arbank([
        ('In a lucky draw with 1000 tickets and 5 prizes, the probability that a person with one ticket wins is 1/200.', 'P(E) = favourable outcomes ÷ total outcomes.', 'a', '5/1000.'),
        ('A batsman either scores a century or does not, so the probability of a century is 1/2.', 'Probability is favourable ÷ total for equally likely outcomes only.', 'd', 'The two outcomes are not equally likely; A false, R true.'),
        ('The probability of drawing a winning ticket does not depend on when a person buys the ticket.', 'Every ticket in the draw is equally likely to be chosen.', 'a', 'R explains A.'),
    ])(r)


def c14s4_explain(r):
    return xbank([
        ('Explain why a lucky draw is fair to everyone who buys one ticket.', 'Each ticket has the same chance of being drawn: all outcomes are equally likely.', '2 marks.'),
        ('A weather forecast says "70% chance of rain". Explain what this means as a probability and what the probability of no rain is.', 'P(rain) = 0.7; P(no rain) = 1 − 0.7 = 0.3.', '2 marks.'),
    ])(r)


def c14s4_case(r):
    b, g = r.randint(10, 25), r.randint(10, 25)
    cap = r.randint(2, 4)
    return Q((f'A class in {r.choice(CITIES)} has {b} boys and {g} girls. The teacher selects one student at random to be the class monitor. '
              f'(i) Find P(a girl is selected). (ii) Find P(a boy is selected). (iii) If {cap} of the girls are already prefects and cannot be chosen, find P(a girl is selected) now. (iv) Is the selection a random experiment with equally likely outcomes? Explain.'),
             f'(i) {frac(g, b + g)} (ii) {frac(b, b + g)} (iii) {frac(g - cap, b + g - cap)} (iv) yes, each eligible student has the same chance', '1 mark each part.')


FAMILIES = {
    S + '11-st1': [F('C1', 'D1', 'mcq', c11s1_mcq), F('C2', 'D2', 'mcq', c11s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c11s1_explain), F('C3', 'D1', 'numerical', c11s1_area),
                   F('C3', 'D2', 'numerical', c11s1_wheel), F('C3', 'D2', 'short', c11s1_sum), F('C3', 'D3', 'multi_step', c11s1_ring), F('C4', 'D3', 'case', c11s1_case)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_mcq), F('C2', 'D2', 'mcq', c11s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c11s2_explain), F('C3', 'D1', 'numerical', c11s2_sector),
                   F('C3', 'D2', 'numerical', c11s2_arc), F('C3', 'D2', 'numerical', c11s2_clock), F('C3', 'D3', 'numerical', c11s2_perim), F('C3', 'D4', 'multi_step', c11s2_theta),
                   F('C4', 'D3', 'multi_step', c11s2_major), F('C4', 'D3', 'case', c11s2_case), F('C4', 'D4', 'long', c11s2_major)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_mcq), F('C2', 'D2', 'mcq', c11s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c11s3_explain), F('C3', 'D2', 'numerical', c11s3_minor),
                   F('C3', 'D3', 'multi_step', c11s3_minor), F('C3', 'D3', 'numerical', c11s3_square), F('C4', 'D4', 'long', c11s3_major), F('C4', 'D3', 'case', c11s3_case)],
    S + '11-st4': [F('C1', 'D2', 'mcq', c11s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c11s4_explain), F('C3', 'D2', 'numerical', c11s4_umbrella, gap='G7'), F('C3', 'D2', 'numerical', c11s4_light, gap='G7'),
                   F('C3', 'D3', 'multi_step', c11s4_wiper, gap='G7'), F('C3', 'D4', 'multi_step', c11s4_horse, gap='G7'), F('C4', 'D4', 'long', c11s4_corners, gap='G7'), F('C4', 'D5', 'long', c11s4_brooch, gap='G7'),
                   F('C4', 'D3', 'case', c11s4_case, gap='G7'), F('C3', 'D1', 'numerical', c11s4_umbrella, gap='G7')],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_mcq), F('C2', 'D2', 'mcq', c12s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c12s1_explain), F('C3', 'D2', 'numerical', c12s1_toy),
                   F('C3', 'D2', 'numerical', c12s1_capsule), F('C3', 'D3', 'numerical', c12s1_tent), F('C3', 'D3', 'multi_step', c12s1_cube), F('C3', 'D4', 'multi_step', c12s1_scooped),
                   F('C4', 'D4', 'long', c12s1_cavity), F('C4', 'D3', 'case', c12s1_case), F('C3', 'D1', 'numerical', c12s1_toy)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_mcq), F('C2', 'D2', 'mcq', c12s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c12s2_explain), F('C3', 'D1', 'numerical', c12s2_toy),
                   F('C3', 'D2', 'numerical', c12s2_capsule), F('C3', 'D2', 'numerical', c12s2_rocket), F('C3', 'D3', 'numerical', c12s2_hollow), F('C3', 'D4', 'multi_step', c12s2_pen),
                   F('C4', 'D4', 'long', c12s2_gulab), F('C4', 'D3', 'case', c12s2_case), F('C4', 'D5', 'long', c12s2_pen), F('C3', 'D3', 'multi_step', c12s2_rocket)],
    S + '12-st3': [F('C1', 'D2', 'mcq', c12s3_mcq), F('C2', 'D2', 'mcq', c12s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c12s3_explain), F('C3', 'D2', 'numerical', c12s3_tank, gap='G7'),
                   F('C3', 'D3', 'multi_step', c12s3_vessel, gap='G7'), F('C3', 'D3', 'multi_step', c12s3_paint, gap='G7'), F('C4', 'D4', 'long', c12s3_tentcost, gap='G7'), F('C4', 'D3', 'case', c12s3_case, gap='G7'),
                   F('C4', 'D5', 'long', c12s3_vessel, gap='G7'), F('C3', 'D1', 'numerical', c12s3_tank, gap='G7'), F('C3', 'D4', 'multi_step', c12s3_tentcost, gap='G7')],
    S + '13-st1': [F('C1', 'D2', 'mcq', c13s1_mcq), F('C2', 'D2', 'mcq', c13s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c13s1_explain), F('C3', 'D2', 'numerical', c13s1_mean),
                   F('C3', 'D3', 'multi_step', c13s1_mean), F('C3', 'D4', 'multi_step', c13s1_missing), F('C4', 'D4', 'long', c13s1_missing), F('C4', 'D3', 'case', c13s1_case), F('C3', 'D1', 'numerical', c13s1_mean)],
    S + '13-st2': [F('C1', 'D2', 'mcq', c13s2_mcq), F('C1', 'D1', 'mcq', c13s2_modal), F('C2', 'D2', 'mcq', c13s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c13s2_explain),
                   F('C3', 'D2', 'numerical', c13s2_mode), F('C3', 'D3', 'multi_step', c13s2_mode), F('C4', 'D3', 'case', c13s2_case), F('C4', 'D4', 'multi_step', c13s2_mode)],
    S + '13-st3': [F('C1', 'D2', 'mcq', c13s3_mcq), F('C1', 'D1', 'mcq', c13s3_class), F('C2', 'D2', 'mcq', c13s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c13s3_explain),
                   F('C3', 'D2', 'numerical', c13s3_median), F('C3', 'D3', 'multi_step', c13s3_median), F('C4', 'D4', 'long', c13s3_missing), F('C4', 'D5', 'long', c13s3_missing), F('C4', 'D3', 'case', c13s3_case)],
    S + '13-st4': [F('C1', 'D2', 'mcq', c13s4_mcq), F('C2', 'D2', 'mcq', c13s4_ar, kinds=('ar',)), F('C2', 'D3', 'explain', c13s4_explain), F('C3', 'D2', 'short', c13s4_emp),
                   F('C3', 'D3', 'numerical', c13s4_emp), F('C4', 'D3', 'case', c13s4_case)],
    S + '14-st1': [F('C1', 'D1', 'mcq', c14s1_mcq), F('C2', 'D2', 'mcq', c14s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c14s1_explain), F('C3', 'D1', 'short', g9b.c7s3_bag),
                   F('C3', 'D2', 'short', c14s1_word), F('C3', 'D2', 'mcq', g9b.c7s3_die), F('C3', 'D3', 'short', c14s1_disc), F('C3', 'D3', 'numerical', g9b.c7s3_find_n), F('C4', 'D3', 'case', c14s1_case)],
    S + '14-st2': [F('C1', 'D2', 'mcq', c14s2_mcq), F('C2', 'D2', 'mcq', c14s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c14s2_explain), F('C3', 'D1', 'short', c14s2_comp),
                   F('C3', 'D2', 'short', c14s2_defect), F('C3', 'D3', 'numerical', c14s2_comp), F('C4', 'D3', 'case', c14s2_case)],
    S + '14-st3': [F('C1', 'D2', 'mcq', c14s3_mcq), F('C2', 'D2', 'mcq', c14s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c14s3_explain), F('C3', 'D1', 'short', c14s3_card),
                   F('C3', 'D2', 'short', c14s3_card), F('C3', 'D2', 'numerical', c14s3_dice), F('C3', 'D3', 'numerical', c14s3_dice), F('C3', 'D3', 'mcq', g9b.c7s4_coins),
                   F('C3', 'D4', 'multi_step', c14s3_removed), F('C4', 'D4', 'multi_step', g9b.c7s4_product), F('C4', 'D3', 'case', c14s3_case), F('C3', 'D3', 'numerical', g9b.c7s4_three)],
    S + '14-st4': [F('C1', 'D2', 'mcq', c14s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c14s4_explain), F('C3', 'D1', 'short', c14s4_fish, gap='G7'), F('C3', 'D2', 'short', c14s4_tickets, gap='G7'),
                   F('C3', 'D2', 'numerical', c14s4_piggy, gap='G7'), F('C3', 'D3', 'multi_step', c14s4_game, gap='G7'), F('C4', 'D3', 'case', c14s4_case, gap='G7'), F('C4', 'D4', 'multi_step', g9b.c7s4_case, gap='G7')],
}
