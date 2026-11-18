"""CBSE class 10 maths (NCERT Mathematics X) families, chapters 6-10."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, name, two_names, num_distractors, CITIES
from g9_maths_h import nz, Q, mcqbank, arbank, xbank, P, fn, rad, is_sq, lin, triple, bracket, TRIPLES
import g9_maths_a as g9a

S = 'cbse-g10-maths-ch'
R3V = 1.732


def _raise():
    raise ValueError


def dec(x, dp=2):
    return num(round(float(x), dp), dp)


# ---------------- ch06 Triangles ----------------
# st1 similar figures

def c6s1_mcq(r):
    return mcqbank([
        ('Which of the following pairs of figures are always similar?', 'Any two circles', ['Any two rectangles', 'Any two isosceles triangles', 'Any two rhombuses'], 'All circles have the same shape.'),
        ('Two polygons with the same number of sides are similar if …', 'their corresponding angles are equal and corresponding sides are in the same ratio', ['their corresponding sides are equal', 'only their corresponding angles are equal', 'only their corresponding sides are proportional'], 'Both conditions are needed for polygons.'),
        ('All … are similar.', 'equilateral triangles', ['isosceles triangles', 'right triangles', 'scalene triangles'], 'All angles 60°.'),
        ('Two congruent figures are …', 'always similar', ['never similar', 'similar only if they are triangles', 'similar only if they are squares'], 'Congruent figures have the same shape and size.'),
        ('Which pair is NOT necessarily similar?', 'Two rectangles', ['Two squares', 'Two circles', 'Two equilateral triangles'], 'Rectangles may have different length-breadth ratios.'),
        ('A square and a rhombus with equal sides are …', 'not necessarily similar', ['always similar', 'always congruent', 'similar only if the rhombus has a 45° angle'], 'Their angles may differ.'),
    ])(r)


def c6s1_scale(r):
    k = Fr(r.choice([2, 3, 4, 5, 3, 5]), r.choice([1, 2, 3, 4]))
    if k == 1:
        raise ValueError
    sides = sorted(r.sample(range(3, 15), 3))
    fig = r.choice(['quadrilateral', 'pentagon', 'triangle'])
    i = r.randrange(3)
    new = [s * k for s in sides]
    if any(Fr(x).denominator not in (1, 2) for x in new):
        raise ValueError
    return Q(f'A {fig} has sides (among others) {sides[0]} cm, {sides[1]} cm and {sides[2]} cm. A similar {fig} has scale factor {fn(k)}. Find the side corresponding to {sides[i]} cm.',
             f'{dec(new[i])} cm', f'Corresponding sides are proportional: {sides[i]} × {fn(k)} = {dec(new[i])} cm.',
             num_distractors(float(new[i]), sides[i] + float(k), float(sides[i] / k), sides[i] * 2))


def c6s1_rect(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    if a == b:
        raise ValueError
    k = r.choice([Fr(3, 2), 2, 3, Fr(5, 2), 4])
    sim = r.random() < 0.5
    c, d = a * k, b * k + (0 if sim else r.choice([1, 2]))
    ans = 'Yes, similar' if sim else 'Not similar'
    return Q(f'Is a rectangle of {a} cm × {b} cm similar to a rectangle of {dec(c)} cm × {dec(d)} cm? Justify.', ans,
             f'All angles are 90°; compare ratios {a}/{dec(c)} = {fn(Fr(a) / Fr(c))} and {b}/{dec(d)} = {fn(Fr(b) / Fr(d))}: ' + ('equal, so similar.' if sim else 'not equal, so not similar.'),
             ['Not similar' if sim else 'Yes, similar', 'Yes, congruent', 'Cannot be decided without angles'])


def c6s1_explain(r):
    return xbank([
        ('Explain why a square and a rhombus of the same side need not be similar.', 'Sides are proportional (ratio 1) but corresponding angles need not be equal (rhombus angles may not be 90°).', '2 marks.'),
        ('Explain why a rectangle and a square need not be similar even though all their angles are equal.', 'Angles are equal but sides are not proportional unless the rectangle is a square.', '2 marks.'),
        ('Explain the difference between congruent and similar figures, with an example.', 'Similar: same shape (proportional sides, equal angles); congruent: same shape and size. e.g. two circles of radii 2 cm and 5 cm are similar, not congruent.', '2 marks.'),
        ('Explain why all circles are similar but not all ellipses-like ovals or rectangles are.', 'A circle is fixed by its radius alone, so any circle is a scaled copy of another; rectangles need the same length-to-breadth ratio.', '2 marks.'),
        ('Is the statement "all isosceles triangles are similar" true? Explain.', 'False; e.g. isosceles triangles with vertex angles 40° and 100° have different angles.', '2 marks.'),
    ])(r)


def c6s1_ar(r):
    return arbank([
        ('All equilateral triangles are similar.', 'Each angle of an equilateral triangle is 60°.', 'a', 'Equal angles and proportional sides.'),
        ('Any two rectangles are similar.', 'All angles of a rectangle are right angles.', 'd', 'Sides need not be proportional; A false, R true.'),
        ('Two squares of sides 3 cm and 7 cm are similar.', 'Similar figures have the same shape but not necessarily the same size.', 'a', 'R explains A.'),
        ('A square and a rhombus of equal side are similar.', 'Their sides are in the same ratio.', 'd', 'Angles may differ; A false, R true.'),
        ('Congruent figures are similar.', 'Similar figures must be congruent.', 'c', 'A true; R false.'),
    ])(r)


def c6s1_case(r):
    w, h = r.choice([(4, 6), (5, 7), (6, 8), (8, 10), (10, 15), (3, 5)])
    k = r.choice([2, 3, 4, 5])
    who = name(r)
    return Q((f'{who} prints a photograph of size {w} cm × {h} cm and then enlarges it to {w * k} cm × {h * k} cm for a school exhibition. '
              f'(i) Are the two prints similar? Why? (ii) What is the scale factor? (iii) If the original shows a tree 2.5 cm tall, how tall is it in the enlargement? (iv) Would a {w * k} cm × {h * k + 2} cm print be similar to the original?'),
             f'(i) yes: angles 90° and sides in ratio 1 : {k} (ii) {k} (iii) {dec(2.5 * k)} cm (iv) no, {w}/{w * k} ≠ {h}/{h * k + 2}', '1 mark each part.')


def c6s1_map(r):
    s = r.choice([50000, 100000, 200000, 25000])
    d = r.choice([2.5, 3, 4.2, 6, 7.5, 8, 1.8, 5.4])
    real = d * s / 100000
    return Q(f'On a map with scale 1 : {s:,}, two towns are {dec(d)} cm apart. Using the idea of similar figures, find the actual distance in km.', f'{dec(real)} km',
             f'Actual = {dec(d)} × {s:,} cm = {dec(d * s)} cm = {dec(real)} km.', num_distractors(real, real * 10, real / 10, d))


# st2 BPT

def c6s2_find(r):
    p, q = r.sample(range(1, 8), 2)
    g = math.gcd(p, q)
    p, q = p // g, q // g
    s1, s2 = r.choice([1, 1.5, 2, 2.5, 3]), r.choice([1, 1.5, 2, 3, 0.5])
    vals = {'AD': p * s1, 'DB': q * s1, 'AE': p * s2, 'EC': q * s2}
    ask = r.choice(list(vals))
    given = ', '.join(f'{k} = {dec(v)} cm' for k, v in vals.items() if k != ask)
    ans = vals[ask]
    return Q(f'In △ABC, D and E are points on AB and AC such that DE ∥ BC. If {given}, find {ask}.', f'{dec(ans)} cm',
             f'By the Basic Proportionality Theorem, AD/DB = AE/EC; substitute and solve: {ask} = {dec(ans)} cm.',
             num_distractors(ans, vals['AD'] + vals['EC'] - vals['DB'] if ask == 'AE' else ans + 1, ans * 2, ans + 0.5))


def c6s2_alg(r):
    for _ in range(200):
        p, q, s, t = [r.randint(-3, 4) for _ in range(4)]
        k = p + t - q - s
        if k == 0 or (q * s - p * t) % k or len({p, q, s, t}) < 3:
            continue
        x = (q * s - p * t) // k
        if 2 <= x <= 15 and min(x + p, x + q, x + s, x + t) > 0:
            break
    else:
        raise ValueError
    return Q(f'In △ABC, DE ∥ BC with D on AB and E on AC. If AD = {lin(1, p)}, DB = {lin(1, q)}, AE = {lin(1, s)} and EC = {lin(1, t)} (in cm), find x.', f'x = {x}',
             f'AD/DB = AE/EC ⇒ ({lin(1, p)})({lin(1, t)}) = ({lin(1, q)})({lin(1, s)}); the x² terms cancel ⇒ x = {x} (3 marks).',
             num_distractors(x, x + 1, x - 1, x + 2))


def c6s2_converse(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    k = r.choice([Fr(3, 2), 2, Fr(1, 2), 3])
    par = r.random() < 0.55
    c = a * k
    d = b * k if par else b * k + r.choice([Fr(1, 2), 1])
    return Q(f'D and E are points on sides PQ and PR of △PQR with PD = {a} cm, DQ = {b} cm, PE = {dec(c)} cm and ER = {dec(d)} cm. Is DE ∥ QR? Justify.', 'Yes' if par else 'No',
             f'PD/DQ = {fn(Fr(a, b))}, PE/ER = {fn(Fr(c) / Fr(d))}; ' + ('equal, so DE ∥ QR by the converse of BPT.' if par else 'not equal, so DE is not parallel to QR.'),
             ['No' if par else 'Yes', 'Only if PD = PE', 'Cannot be decided'])


def c6s2_whole(r):
    p, q = r.sample(range(1, 7), 2)
    s = r.choice([1, 2, 3])
    AD, AB = p * s, (p + q) * s
    AC = (p + q) * r.choice([1, 2, 3, Fr(3, 2)])
    AE = Fr(AD, AB) * AC
    return Q(f'In △ABC, DE ∥ BC, D on AB and E on AC. If AD = {AD} cm, AB = {AB} cm and AC = {dec(AC)} cm, find AE.', f'{dec(AE)} cm',
             f'AD/AB = AE/AC (corollary of BPT) ⇒ AE = {AD} × {dec(AC)} / {AB} = {dec(AE)} cm.', num_distractors(float(AE), float(AC - AE), float(AC) * AB / AD, float(AE) + 1))


def c6s2_trap(r):
    p, q = r.sample(range(2, 9), 2)
    s1, s2 = r.choice([1, 2, 3]), r.choice([1, 2, 3])
    AO, OC, BO, OD = p * s1, q * s1, p * s2, q * s2
    vals = {'AO': AO, 'OC': OC, 'BO': BO, 'OD': OD}
    ask = r.choice(list(vals))
    given = ', '.join(f'{k} = {v} cm' for k, v in vals.items() if k != ask)
    return Q(f'ABCD is a trapezium with AB ∥ DC; its diagonals meet at O. If {given}, find {ask}.', f'{vals[ask]} cm',
             f'Draw EO ∥ AB through O; by BPT, AO/OC = BO/OD. Solve: {ask} = {vals[ask]} cm (3 marks).', num_distractors(vals[ask], vals[ask] + 2, vals[ask] * 2, abs(vals[ask] - 1)))


def c6s2_trap_alg(r):
    for _ in range(100):
        try:
            return _trap_alg(r)
        except ValueError:
            pass
    raise ValueError


def _trap_alg(r):
    x = r.randint(5, 14)
    a, b = r.randint(2, 4), r.randint(1, 3)
    c2, c3 = r.randint(1, x - 2), r.randint(1, x - 2)
    OC, BO = x - c2, x - c3
    OD = r.randint(2, 6)
    # need AO/OC = BO/OD ⇒ AO = OC·BO/OD
    if (OC * BO) % OD:
        raise ValueError
    AO = OC * BO // OD
    c1 = a * x - AO
    if c1 <= 0:
        raise ValueError
    # equation: (a x − c1)·OD = (x − c2)(x − c3) is quadratic; give the two roots and reject.
    co = [1, -(c2 + c3) - a * OD, c2 * c3 + c1 * OD]
    D = co[1] ** 2 - 4 * co[2]
    if D < 0 or not is_sq(D):
        raise ValueError
    r1, r2 = (-co[1] + math.isqrt(D)) // 2, (-co[1] - math.isqrt(D)) // 2
    other = r1 if r2 == x else r2
    if x not in (r1, r2):
        raise ValueError
    note = '' if other == x else (f'; x = {other} is rejected because a length would be negative or zero' if min(a * other - c1, other - c2, other - c3) <= 0 else f'; x = {other} also gives positive lengths')
    if other != x and min(a * other - c1, other - c2, other - c3) > 0:
        raise ValueError
    return Q(f'The diagonals of a quadrilateral ABCD intersect at O such that AO/OC = BO/OD. If AO = {a}x − {c1}, OC = x − {c2}, BO = x − {c3} and OD = {OD} (in cm), find x.', f'x = {x}',
             f'({a}x − {c1}) × {OD} = (x − {c2})(x − {c3}) ⇒ x² {"−" if co[1] < 0 else "+"} {abs(co[1])}x + {co[2]} = 0 ⇒ x = {x}{note} (4 marks).')


def c6s2_mcq(r):
    return mcqbank([
        ('If a line is drawn parallel to one side of a triangle to intersect the other two sides in distinct points, the other two sides are divided …', 'in the same ratio', ['equally', 'in the ratio 1 : 2', 'in the ratio of the squares of the sides'], 'Basic Proportionality Theorem.'),
        ('The Basic Proportionality Theorem is also known as …', 'Thales theorem', ['Pythagoras theorem', 'Euclid\'s lemma', 'the mid-point theorem'], 'Named after Thales.'),
        ('If a line divides two sides of a triangle in the same ratio, then the line is … the third side.', 'parallel to', ['perpendicular to', 'equal to', 'half of'], 'Converse of BPT.'),
        ('In △ABC, DE ∥ BC with D on AB and E on AC. Then AD/AB = …', 'AE/AC', ['EC/AC', 'DE/AD', 'AB/AE'], 'Corollary of BPT.'),
        ('The line joining the mid-points of two sides of a triangle is parallel to the third side. This follows from …', 'the converse of BPT', ['the SSS criterion', 'Pythagoras theorem', 'the RHS rule'], 'Both sides divided in ratio 1 : 1.'),
    ])(r)


def c6s2_prove(r):
    return xbank([
        ('Prove the Basic Proportionality Theorem: if a line is drawn parallel to one side of a triangle to intersect the other two sides in distinct points, the other two sides are divided in the same ratio.',
         'In △ABC with DE ∥ BC: ar(ADE)/ar(BDE) = AD/DB and ar(ADE)/ar(DEC) = AE/EC; ar(BDE) = ar(DEC) (same base DE, between the same parallels), so AD/DB = AE/EC.',
         'Figure and given/to prove (1), draw EM ⟂ AB, DN ⟂ AC and write the area ratios (2), equal areas of BDE and DEC (1), conclusion (1).'),
        ('ABCD is a trapezium with AB ∥ DC and diagonals meeting at O. Prove that AO/BO = CO/DO.',
         'Draw EO ∥ DC through O meeting AD at E. In △ADC, EO ∥ DC ⇒ AE/ED = AO/OC; in △DAB, EO ∥ AB ⇒ AE/ED = BO/OD; hence AO/OC = BO/OD, i.e. AO/BO = CO/DO.',
         'Construction (1), two applications of BPT (2 + 1), conclusion (1).'),
        ('Using BPT, prove that a line drawn through the mid-point of one side of a triangle parallel to another side bisects the third side.',
         'In △ABC, D is the mid-point of AB and DE ∥ BC. By BPT AD/DB = AE/EC; AD = DB ⇒ AE = EC.', 'Statement (1), BPT (2), conclusion (2).'),
    ])(r)


def c6s2_ar(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return arbank([
        (f'In △ABC, DE ∥ BC with AD = {a} cm, DB = {b} cm and AE = {2 * a} cm; then EC = {2 * b} cm.', 'A line parallel to one side of a triangle divides the other two sides in the same ratio.', 'a', 'BPT gives EC.'),
        (f'If AD/DB = AE/EC = {a}/{b} in △ABC, then DE ∥ BC.', 'If a line divides two sides of a triangle in the same ratio, it is parallel to the third side.', 'a', 'Converse of BPT.'),
        ('In △ABC, if DE ∥ BC, then AD/DB = DE/BC.', 'BPT states that AD/DB = AE/EC.', 'd', 'DE/BC = AD/AB, not AD/DB; A false, R true.'),
        ('The line joining the mid-points of two sides of a triangle is parallel to the third side.', 'In a triangle, the sum of any two sides is greater than the third side.', 'b', 'Both true, but R is not the reason (it follows from the converse of BPT).'),
    ])(r)


def c6s2_case(r):
    p, q = r.sample(range(2, 7), 2)
    s = r.choice([10, 20, 25, 50])
    AD, DB = p * s, q * s
    AC = (p + q) * r.choice([12, 15, 20, 30])
    AE = AC * p // (p + q)
    return Q((f'A triangular park ABC in {r.choice(CITIES)} has a straight walking path DE parallel to the boundary BC, with D on AB and E on AC. AD = {AD} m, DB = {DB} m and AC = {AC} m. '
              f'(i) State the theorem that relates these lengths. (ii) Find AE. (iii) Find EC. (iv) If instead D were the mid-point of AB, where would E lie?'),
             f'(i) Basic Proportionality Theorem: AD/DB = AE/EC (ii) {AE} m (iii) {AC - AE} m (iv) at the mid-point of AC', '1 mark each part.')


# st3 criteria

CRIT = [
    ('∠A = ∠P and ∠B = ∠Q', 'AA (AAA) similarity'),
    ('AB/PQ = BC/QR = CA/RP', 'SSS similarity'),
    ('AB/PQ = AC/PR and ∠A = ∠P', 'SAS similarity'),
    ('∠A = ∠P, ∠B = ∠Q and ∠C = ∠R', 'AAA similarity'),
]


def c6s3_which(r):
    cond, crit = r.choice(CRIT)
    wrong = [c for c in ['AA (AAA) similarity', 'SSS similarity', 'SAS similarity', 'RHS congruence', 'ASA congruence'] if c != crit and not (crit == 'AAA similarity' and c.startswith('AA ('))]
    return mcq(f'In △ABC and △PQR, {cond}. Which criterion shows that △ABC ~ △PQR?', crit, wrong[:3], 'Match the given equal angles or proportional sides to the criterion.', r)


def c6s3_sss(r):
    while True:
        a, b, c = sorted(r.sample(range(3, 16), 3))
        if a + b > c:
            break
    k = r.choice([Fr(3, 2), 2, Fr(5, 2), 3, Fr(1, 2)])
    sim = r.random() < 0.5
    d, e, f = a * k, b * k, c * k + (0 if sim else r.choice([1, 2]))
    return Q(f'The sides of △ABC are {a} cm, {b} cm and {c} cm, and the sides of △DEF are {dec(d)} cm, {dec(e)} cm and {dec(f)} cm. Are the triangles similar? Justify.', 'Yes, by SSS' if sim else 'No',
             f'Ratios of corresponding (smallest to largest) sides: {fn(Fr(a) / Fr(d))}, {fn(Fr(b) / Fr(e))}, {fn(Fr(c) / Fr(f))}; ' + ('all equal, so similar (SSS).' if sim else 'not all equal, so not similar.'),
             ['No' if sim else 'Yes, by SSS', 'Yes, by AA', 'Yes, by SAS'])


def c6s3_angle(r):
    A = r.randint(30, 80)
    B = r.randint(30, 150 - A)
    C = 180 - A - B
    ask = r.choice(['∠P', '∠Q', '∠R'])
    ans = {'∠P': A, '∠Q': B, '∠R': C}[ask]
    giv = r.choice([(f'∠A = {A}° and ∠B = {B}°'), (f'∠A = {A}° and ∠C = {C}°'), (f'∠B = {B}° and ∠C = {C}°')])
    return Q(f'△ABC ~ △PQR. If {giv}, find {ask}.', f'{ans}°', f'Corresponding angles of similar triangles are equal; the third angle is 180° minus the other two. {ask} = {ans}°.',
             num_distractors(ans, 180 - ans, 90 - ans if ans < 90 else ans - 30, (180 - ans) // 2))


def c6s3_sas(r):
    a, b = r.randint(3, 12), r.randint(3, 12)
    k = r.choice([2, 3, Fr(3, 2), Fr(5, 2)])
    ang = r.choice([40, 50, 60, 70, 75, 80, 100, 110])
    sim = r.random() < 0.5
    ang2 = ang if sim else ang + r.choice([5, 10, -10])
    return Q(f'In △ABC, AB = {a} cm, AC = {b} cm, ∠A = {ang}°. In △PQR, PQ = {dec(a * k)} cm, PR = {dec(b * k)} cm, ∠P = {ang2}°. Are the triangles similar? If yes, state the criterion.',
             'Yes, by SAS' if sim else 'No', f'AB/PQ = AC/PR = {fn(1 / Fr(k))}; ' + ('included angles equal, so similar (SAS).' if sim else 'but the included angles differ, so SAS fails.'),
             ['No' if sim else 'Yes, by SAS', 'Yes, by SSS', 'Yes, by AA'])


def c6s3_explain(r):
    return xbank([
        ('Explain why two triangles are similar if two angles of one are equal to two angles of the other.', 'The third angles are then also equal (angle sum 180°), so AAA holds.', '2 marks.'),
        ('Explain why, unlike triangles, two quadrilaterals with equal corresponding angles need not be similar. Give an example.', 'A square and a non-square rectangle have equal angles but sides not proportional.', '2 marks.'),
        ('Explain why SSA (two sides and a non-included angle) is not a criterion for similarity.', 'Two different triangle shapes can have the same two sides and non-included angle, so the shape is not fixed.', '2 marks.'),
        ('In △ABC and △DEF, AB/DE = BC/EF and ∠B = ∠E. Explain which criterion gives similarity and which angles are then equal.', 'SAS similarity; ∠A = ∠D and ∠C = ∠F.', '2 marks.'),
    ])(r)


def c6s3_ar(r):
    return arbank([
        ('If two angles of one triangle are equal to two angles of another, the triangles are similar.', 'The sum of the angles of a triangle is 180°.', 'a', 'Third angles equal; AA follows.'),
        ('Two triangles with sides 3, 4, 5 and 6, 8, 10 are similar.', 'If the corresponding sides of two triangles are proportional, the triangles are similar.', 'a', 'SSS similarity.'),
        ('Two triangles with two pairs of proportional sides are always similar.', 'For SAS similarity the included angles must be equal.', 'd', 'A false, R true.'),
        ('In similar triangles, corresponding angles are equal.', 'Similar triangles are always congruent.', 'c', 'A true, R false.'),
    ])(r)


def c6s3_prove(r):
    return xbank([
        ('In △PQR, S and T are points on QR and PR such that ∠P = ∠RTS. Show that △RPQ ~ △RTS.', '∠R is common and ∠RPQ = ∠RTS, so △RPQ ~ △RTS by AA.', 'Identify equal angles (2), state criterion (1).'),
        ('In the figure, AB ∥ DC and the diagonals AC and BD of trapezium ABCD meet at O. Prove △OAB ~ △OCD.', '∠OAB = ∠OCD and ∠OBA = ∠ODC (alternate angles), so AA similarity.', '3 marks.'),
        ('CD and GH are the bisectors of ∠ACB and ∠EGF of similar triangles ABC ~ EFG, meeting AB and EF at D and H. Prove △DCB ~ △HGF.', '∠B = ∠F and ∠DCB = ½∠C = ½∠G = ∠HGF; AA similarity.', '3 marks.'),
        ('E is a point on side AD produced of parallelogram ABCD, and BE meets CD at F. Prove △ABE ~ △CFB.', '∠A = ∠C (opposite angles) and ∠AEB = ∠CBF (alternate angles, AE ∥ BC); AA.', '3 marks.'),
    ])(r)


def c6s3_case(r):
    a, b, c = r.choice([(4, 6, 8), (5, 7, 9), (3, 5, 6), (6, 8, 9), (4, 5, 7)])
    k = r.choice([2, 3, Fr(3, 2)])
    return Q((f'An architect makes a model triangle of sides {a} cm, {b} cm and {c} cm for a roof truss. The real truss has sides {dec(a * k * 100)} cm, {dec(b * k * 100)} cm and {dec(c * k * 100)} cm. '
              f'(i) Find the ratio of corresponding sides. (ii) Which criterion shows the triangles are similar? (iii) Is the model triangle right-angled? Check using {a}² + {b}² and {c}². (iv) What is the perimeter of the real truss in metres?'),
             f'(i) 1 : {fn(k * 100)} (ii) SSS similarity (iii) {a * a + b * b} {"=" if a * a + b * b == c * c else "≠"} {c * c}, so the largest angle is {"90°" if a * a + b * b == c * c else "not 90°"} (iv) {dec((a + b + c) * k)} m',
             '1 mark each part.')


# st4 using similarity

def c6s4_shadow(r):
    h1 = r.choice([1.2, 1.5, 1.6, 2, 2.4, 3, 6])
    s1 = r.choice([0.8, 1, 1.2, 1.5, 2, 2.5, 3, 4])
    k = r.choice([5, 8, 10, 12, 15, 20, 25])
    s2 = round(s1 * k, 2)
    h2 = round(h1 * k, 2)
    obj = r.choice(['a vertical pole', 'a student', 'a lamp post'])
    big = r.choice(['tower', 'tree', 'building', 'water tank'])
    return Q(f'{obj.capitalize()} of height {dec(h1)} m casts a shadow {dec(s1)} m long on the ground, and at the same time a {big} casts a shadow {dec(s2)} m long. Find the height of the {big}.',
             f'{dec(h2)} m', f'The sun\'s rays make equal angles, so the triangles are similar (AA): h/{dec(s2)} = {dec(h1)}/{dec(s1)} ⇒ h = {dec(h2)} m.',
             num_distractors(h2, s2 * s1 / h1, h1 + s2 - s1, h2 * 2))


def c6s4_sides(r):
    while True:
        a, b, c = sorted(r.sample(range(3, 16), 3))
        if a + b > c:
            break
    k = r.choice([2, 3, Fr(3, 2), Fr(5, 2), Fr(1, 2)])
    names = ['AB', 'BC', 'CA']
    corr = {'AB': 'PQ', 'BC': 'QR', 'CA': 'RP'}
    sides = dict(zip(names, [a, b, c]))
    i = r.choice(names)
    j = r.choice([n for n in names if n != i])
    ans = sides[j] * k
    return Q(f'△ABC ~ △PQR with AB = {a} cm, BC = {b} cm, CA = {c} cm and {corr[i]} = {dec(sides[i] * k)} cm. Find {corr[j]}.', f'{dec(ans)} cm',
             f'{i}/{corr[i]} = {j}/{corr[j]} ⇒ {corr[j]} = {sides[j]} × {dec(sides[i] * k)}/{sides[i]} = {dec(ans)} cm.',
             num_distractors(float(ans), float(sides[j] + sides[i] * k - sides[i]), float(sides[j] / k), float(ans) + 2))


def c6s4_lamp(r):
    L = r.choice([3.6, 4.8, 5.4, 6, 4.5, 7.2])
    h = r.choice([0.9, 1.2, 1.5, 1.8])
    if h >= L:
        raise ValueError
    v = r.choice([0.6, 0.9, 1.2, 1.5])
    t = r.choice([2, 3, 4, 5])
    d = round(v * t, 2)
    s = h * d / (L - h)
    if abs(round(s, 2) - s) > 1e-9:
        raise ValueError
    who = name(r)
    return Q(f'{who}, who is {dec(h * 100)} cm tall, walks away from the base of a lamp post at {dec(v)} m/s. The lamp is {dec(L)} m above the ground. Find the length of {who}\'s shadow after {t} seconds.',
             f'{dec(s)} m', f'Distance from the post = {dec(d)} m. Similar triangles: {dec(h)}/s = {dec(L)}/({dec(d)} + s) ⇒ s = {dec(h)} × {dec(d)}/({dec(L)} − {dec(h)}) = {dec(s)} m (3 marks).')


def c6s4_altitude(r):
    m, n = r.sample(range(1, 6), 2)
    k = r.choice([1, 2, 3])
    BD, DC, AD = k * m * m, k * n * n, k * m * n
    return Q(f'In △ABC, ∠A = 90° and AD ⟂ BC with D on BC. If BD = {BD} cm and DC = {DC} cm, find AD.', f'{AD} cm',
             f'△ADB ~ △CDA (AA), so BD/AD = AD/DC ⇒ AD² = BD × DC = {BD * DC} ⇒ AD = {AD} cm (3 marks).', num_distractors(AD, (BD + DC) / 2, BD * DC, abs(BD - DC)))


def c6s4_perim(r):
    while True:
        k = Fr(r.choice([2, 3, 4, 5]), r.choice([1, 2, 3]))
        side = r.choice([4, 5, 6, 8, 9, 10, 12])
        p1 = r.choice([12, 18, 24, 30, 36, 45, 60])
        if k != 1 and (side * k).denominator in (1, 2) and (p1 * k).denominator in (1, 2):
            break
    p2 = p1 * k
    return Q(f'△ABC ~ △DEF, the perimeter of △ABC is {p1} cm and that of △DEF is {dec(p2)} cm. If AB = {side} cm, find DE.', f'{dec(side * k)} cm',
             f'The ratio of perimeters of similar triangles equals the ratio of corresponding sides: DE = {side} × {dec(p2)}/{p1} = {dec(side * k)} cm.',
             num_distractors(float(side * k), float(side / k), float(side * k) + 2, float(side * k * k)))


def c6s4_ar(r):
    return arbank([
        ('A vertical pole and a tower cast shadows at the same time; their heights are proportional to the lengths of their shadows.', 'The triangles formed are similar by AA, since the sun\'s rays are parallel.', 'a', 'R explains A.'),
        ('If △ABC ~ △DEF and AB = 2DE, then BC = 2EF.', 'Corresponding sides of similar triangles are proportional.', 'a', 'R explains A.'),
        ('If △ABC ~ △PQR, then AB/PQ = BC/PR.', 'In similar triangles, corresponding sides are proportional.', 'd', 'BC corresponds to QR; A false, R true.'),
        ('In right △ABC with ∠A = 90° and AD ⟂ BC, AD² = BD × DC.', '△ADB ~ △CDA.', 'a', 'R gives BD/AD = AD/DC.'),
    ])(r)


def c6s4_explain(r):
    return xbank([
        ('Explain how similar triangles help find the height of a tree from its shadow without climbing it.', 'Measure a stick and its shadow at the same time; the triangles are similar (AA), so tree height = stick height × tree shadow ÷ stick shadow.', '2 marks.'),
        ('Explain why, if △ABC ~ △DEF, then AB/DE = (AB + BC + CA)/(DE + EF + FD).', 'Each side ratio equals k, so the sum of sides also has ratio k.', '2 marks.'),
        ('Explain how a mirror placed on the ground can be used to find the height of a building using similar triangles.', 'Angle of incidence equals angle of reflection, so the triangles formed by the observer and the building with the mirror are similar (AA).', '2 marks.'),
    ])(r)


def c6s4_case(r):
    h = r.choice([1.5, 1.6, 1.8])
    d1 = r.choice([1.2, 1.5, 2, 2.4])
    k = r.choice([6, 8, 10, 12, 15])
    who = name(r)
    return Q((f'{who} places a small mirror on the ground {dec(d1 * k)} m from the foot of a building. Walking back {dec(d1)} m from the mirror, {who} sees the top of the building in it. {who}\'s eyes are {dec(h)} m above the ground. '
              f'(i) Why are the two triangles similar? (ii) Write the proportion. (iii) Find the height of the building. (iv) If {who} stood 0.5 m further back, would the height found change? Explain.'),
             f'(i) right angles at the feet and equal angles of incidence and reflection (AA) (ii) H/{dec(d1 * k)} = {dec(h)}/{dec(d1)} (iii) {dec(h * k)} m (iv) no, the building height is fixed; the mirror would have to move', '1 mark each part.')


# ---------------- ch07 Coordinate Geometry ----------------
# st1 distance

def c7s1_mcq(r):
    a, b = r.randint(1, 12), r.randint(1, 12)
    k = r.choice([0, 1])
    if k:
        return mcq(f'The distance of the point ({a}, {fn(-b)}) from the origin is …', rad(a * a + b * b),
                   [rad(a * a + b * b + 1) if not is_sq(a * a + b * b + 1) else str(a * a + b * b + 1), str(a + b), str(a * a + b * b)], '√(x² + y²).', r)
    return mcq(f'The distance of the point ({a}, {fn(-b)}) from the x-axis is …', str(b) if a != b else str(b), [str(a) if a != b else str(a + 1), rad(a * a + b * b) if rad(a * a + b * b) not in (str(b),) else str(b + 2), str(-b).replace('-', '−')],
               'Distance from the x-axis is |y|.', r)


def c7s1_relation(r):
    a, b, c, d = [r.randint(-6, 6) for _ in range(4)]
    if (a, b) == (c, d):
        raise ValueError
    A = 2 * (c - a)
    B = 2 * (d - b)
    C = c * c + d * d - a * a - b * b
    g = math.gcd(math.gcd(abs(A), abs(B)), abs(C)) or 1
    A, B, C = A // g, B // g, C // g
    if A < 0 or (A == 0 and B < 0):
        A, B, C = -A, -B, -C
    from g9_maths_h import eq2
    return Q(f'Find a relation between x and y such that the point (x, y) is equidistant from A{P(a, b)} and B{P(c, d)}.', eq2(A, B, C),
             f'(x − {bracket(a)})² + (y − {bracket(b)})² = (x − {bracket(c)})² + (y − {bracket(d)})²; expand and simplify: {eq2(A, B, C)} (3 marks).')


def c7s1_collinear(r):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    a, b, c = triple(r)
    t = r.choice([1, 2])
    pts = [(x1, y1), (x1 + a, y1 + b), (x1 + a * (t + 1), y1 + b * (t + 1))]
    col = r.random() < 0.6
    if not col:
        pts[2] = (pts[2][0], pts[2][1] + r.choice([1, -1, 2]))
    AB2 = (pts[1][0] - pts[0][0]) ** 2 + (pts[1][1] - pts[0][1]) ** 2
    BC2 = (pts[2][0] - pts[1][0]) ** 2 + (pts[2][1] - pts[1][1]) ** 2
    AC2 = (pts[2][0] - pts[0][0]) ** 2 + (pts[2][1] - pts[0][1]) ** 2
    return Q(f'Using the distance formula, determine whether the points A{P(*pts[0])}, B{P(*pts[1])} and C{P(*pts[2])} are collinear.', 'Collinear' if col else 'Not collinear',
             f'AB = {rad(AB2)}, BC = {rad(BC2)}, AC = {rad(AC2)}; ' + ('AB + BC = AC, so collinear (3 marks).' if col else 'no sum of two equals the third, so not collinear (3 marks).'),
             ['Not collinear' if col else 'Collinear', 'They form a right triangle', 'They form an equilateral triangle'])


def c7s1_yaxis(r):
    while True:
        a, b, c, d = [r.randint(-7, 7) for _ in range(4)]
        if d != b:
            y = Fr(c * c + d * d - a * a - b * b, 2 * (d - b))
            if y.denominator == 1 and (a, c) != (0, 0):
                break
    return Q(f'Find the point on the y-axis which is equidistant from A{P(a, b)} and B{P(c, d)}.', f'(0, {fn(y)})',
             f'Let P = (0, y). PA² = PB²: {a * a} + (y − {bracket(b)})² = {c * c} + (y − {bracket(d)})² ⇒ y = {fn(y)} (3 marks).')


def c7s1_explain(r):
    return xbank([
        ('Explain how the distance formula is obtained from the Pythagoras theorem.', 'Join A(x₁, y₁), B(x₂, y₂) and drop perpendiculars to form a right triangle with legs |x₂ − x₁| and |y₂ − y₁|; AB = √[(x₂ − x₁)² + (y₂ − y₁)²].', '2 marks.'),
        ('Explain why the distance between two points does not depend on the order in which we subtract the coordinates.', '(x₂ − x₁)² = (x₁ − x₂)² and similarly for y.', '2 marks.'),
        ('Explain how to use the distance formula to check whether three points are collinear.', 'Find the three distances; the points are collinear if the sum of two equals the third.', '2 marks.'),
        ('Explain why the distance of (x, y) from the origin is √(x² + y²).', 'Use the distance formula with (0, 0) as the second point.', '2 marks.'),
    ])(r)


def c7s1_ar(r):
    a, b, c = triple(r)
    return arbank([
        (f'The distance of ({a}, {b}) from the origin is {c} units.', 'The distance of P(x, y) from the origin is √(x² + y²).', 'a', 'R explains A.'),
        (f'The distance between ({a}, 0) and (0, {b}) is {a + b} units.', 'Distance = √[(x₂ − x₁)² + (y₂ − y₁)²].', 'd', f'It is {c}; A false, R true.'),
        ('The points (1, 1), (2, 2) and (3, 3) are collinear.', 'The distance between (1, 1) and (3, 3) equals the sum of the other two distances.', 'a', '√2 + √2 = 2√2.'),
        (f'The distance of ({a}, {fn(-b)}) from the y-axis is {a} units.', 'The distance of a point from the y-axis is the absolute value of its y-coordinate.', 'c', 'It is |x|; A true, R false.'),
    ])(r)


def c7s1_case(r):
    a, b, c = triple(r)
    s = r.choice([1, 2, 3])
    v = r.sample(['Rampur', 'Sonpur', 'Devgaon', 'Kalyani', 'Nandgaon', 'Bhimtal'], 3)
    x0, y0 = r.randint(0, 4), r.randint(0, 4)
    A, B = (x0, y0), (x0 + a, y0 + b)
    C = (x0 + a, y0)
    return Q((f'On a district map with grid unit 1 km, the villages {v[0]}, {v[1]} and {v[2]} are at A{P(*A)}, B{P(*B)} and C{P(*C)}. '
              f'(i) Find the distance AC. (ii) Find the distance BC. (iii) Find the straight-line distance AB. (iv) How much shorter is the direct road AB than going A → C → B?'),
             f'(i) {a} km (ii) {b} km (iii) {c} km (iv) {a + b - c} km', '1 mark each part.')


# st2 section formula

def sect(r, ints=True):
    while True:
        m, n = r.randint(1, 4), r.randint(1, 4)
        if math.gcd(m, n) != 1 or (m == n == 1 and r.random() < 0.6):
            continue
        x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
        dx, dy = r.randint(-4, 4) * (m + n), r.randint(-4, 4) * (m + n)
        if dx == 0 and dy == 0:
            continue
        x2, y2 = x1 + dx, y1 + dy
        px, py = x1 + dx * m // (m + n), y1 + dy * m // (m + n)
        return m, n, (x1, y1), (x2, y2), (px, py)


def c7s2_find(r):
    m, n, A, B, Pp = sect(r)
    return Q(f'Find the coordinates of the point which divides the line segment joining A{P(*A)} and B{P(*B)} internally in the ratio {m} : {n}.', P(*Pp),
             f'P = ((m x₂ + n x₁)/(m + n), (m y₂ + n y₁)/(m + n)) = (({m} × {bracket(B[0])} + {n} × {bracket(A[0])})/{m + n}, ({m} × {bracket(B[1])} + {n} × {bracket(A[1])})/{m + n}) = {P(*Pp)}.',
             [P(Fr(n * B[0] + m * A[0], m + n), Fr(n * B[1] + m * A[1], m + n)), P(Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2)), P(Pp[1], Pp[0]) if Pp[0] != Pp[1] else P(Pp[0] + 1, Pp[1])])


def c7s2_mcq(r):
    return mcqbank([
        ('The coordinates of the point dividing the join of (x₁, y₁) and (x₂, y₂) internally in the ratio m₁ : m₂ are …', '((m₁x₂ + m₂x₁)/(m₁ + m₂), (m₁y₂ + m₂y₁)/(m₁ + m₂))',
         ['((m₁x₁ + m₂x₂)/(m₁ + m₂), (m₁y₁ + m₂y₂)/(m₁ + m₂))', '((x₁ + x₂)/2, (y₁ + y₂)/2)', '((m₁x₂ − m₂x₁)/(m₁ − m₂), (m₁y₂ − m₂y₁)/(m₁ − m₂))'], 'Section formula.'),
        ('The section formula with ratio 1 : 1 gives …', 'the mid-point formula', ['the distance formula', 'the point of trisection', 'the origin'], 'm₁ = m₂.'),
        ('If P divides AB internally in the ratio 2 : 3, then AP : AB is …', '2 : 5', ['2 : 3', '3 : 5', '3 : 2'], 'AB = AP + PB = 5 parts.'),
        ('If P divides AB in the ratio k : 1, then P divides BA in the ratio …', '1 : k', ['k : 1', 'k : 2', '2 : k'], 'Reverse the order.'),
    ])(r)


def c7s2_ar(r):
    m, n, A, B, Pp = sect(r)
    return arbank([
        (f'The point dividing the join of {P(*A)} and {P(*B)} in the ratio {m} : {n} is {P(*Pp)}.', 'By the section formula, x = (m₁x₂ + m₂x₁)/(m₁ + m₂) and y = (m₁y₂ + m₂y₁)/(m₁ + m₂).', 'a', 'R explains A.'),
        ('The mid-point of a segment divides it in the ratio 1 : 1.', 'The mid-point is equidistant from both end-points.', 'a', 'R explains A.'),
        ('The point dividing AB in the ratio 1 : 2 is nearer to B than to A.', 'If P divides AB in the ratio m : n, then AP : PB = m : n.', 'd', 'AP < PB, so P is nearer A; A false, R true.'),
    ])(r)


def c7s2_explain(r):
    return xbank([
        ('Explain how the section formula is derived using similar triangles.', 'Drop perpendiculars to the x-axis; the triangles formed are similar (AA), so (x − x₁)/(x₂ − x) = m₁/m₂ ⇒ x = (m₁x₂ + m₂x₁)/(m₁ + m₂); similarly for y.', '2 marks.'),
        ('Explain why the point dividing AB in the ratio 3 : 1 lies closer to B.', 'AP is three times PB, so PB is the shorter part.', '2 marks.'),
        ('Explain how the mid-point formula is a special case of the section formula.', 'Put m₁ = m₂ = 1: x = (x₁ + x₂)/2, y = (y₁ + y₂)/2.', '2 marks.'),
    ])(r)


def c7s2_endpoint(r):
    m, n, A, B, Pp = sect(r)
    return Q(f'The point P{P(*Pp)} divides the line segment joining A{P(*A)} and B(x, y) internally in the ratio {m} : {n}. Find B.', P(*B),
             f'{fn(Pp[0])} = ({"" if m == 1 else m}x + {n} × {bracket(A[0])})/{m + n} ⇒ x = {fn(B[0])}; {fn(Pp[1])} = ({"" if m == 1 else m}y + {n} × {bracket(A[1])})/{m + n} ⇒ y = {fn(B[1])} (3 marks).')


def c7s2_case(r):
    m, n, A, B, Pp = sect(r)
    who1, who2 = two_names(r)
    return Q((f'In a school sports day, a straight race track runs from the start flag A{P(*A)} to the finish flag B{P(*B)} (units: metres on a field grid). '
              f'{who1} places a water station P dividing AB in the ratio {m} : {n}. (i) Write the section formula. (ii) Find P. (iii) Find the mid-point M of AB, where {who2} stands. (iv) In what ratio does M divide AB?'),
             f'(i) ((m₁x₂ + m₂x₁)/(m₁ + m₂), (m₁y₂ + m₂y₁)/(m₁ + m₂)) (ii) {P(*Pp)} (iii) {P(Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))} (iv) 1 : 1', '1 mark each part.')


# st3 trisection and ratio

def c7s3_trisect(r):
    x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
    dx, dy = 3 * nz(r, 1, 4), 3 * r.randint(-4, 4)
    x2, y2 = x1 + dx, y1 + dy
    p1, p2 = (x1 + dx // 3, y1 + dy // 3), (x1 + 2 * dx // 3, y1 + 2 * dy // 3)
    return Q(f'Find the coordinates of the points of trisection of the line segment joining A{P(x1, y1)} and B{P(x2, y2)}.', f'{P(*p1)} and {P(*p2)}',
             f'They divide AB in the ratios 1 : 2 and 2 : 1. Using the section formula: {P(*p1)} and {P(*p2)} (3 marks).',
             [f'{P(Fr(x1 + x2, 2), Fr(y1 + y2, 2))} and {P(*p2)}', f'{P(x1 + dx // 2 if dx % 2 == 0 else x1 + 1, y1)} and {P(x2, y2)}', f'{P(*p1)} and {P(x2 - 1, y2)}'])


def c7s3_ratio(r):
    m, n, A, B, Pp = sect(r)
    if A[0] == B[0]:
        raise ValueError
    return Q(f'In what ratio does the point {P(*Pp)} divide the line segment joining A{P(*A)} and B{P(*B)}?', f'{m} : {n}',
             f'Let the ratio be k : 1: {fn(Pp[0])} = (k × {bracket(B[0])} + {bracket(A[0])})/(k + 1) ⇒ k = {fn(Fr(m, n))}, i.e. {m} : {n} (check with y).',
             [f'{n} : {m}', f'{m} : {m + n}', f'{m + n} : {n}'])


def c7s3_axis(r):
    while True:
        x1, y1, x2, y2 = r.randint(-9, 9), r.randint(-9, 9), r.randint(-9, 9), r.randint(-9, 9)
        ax = r.choice(['x', 'y'])
        a, b = (y1, y2) if ax == 'x' else (x1, x2)
        if a * b < 0:
            k = Fr(-a, b)
            break
    pt = (Fr(k * x2 + x1, k + 1), 0) if ax == 'x' else (0, Fr(k * y2 + y1, k + 1))
    return Q(f'Find the ratio in which the {ax}-axis divides the line segment joining A{P(x1, y1)} and B{P(x2, y2)}. Also find the point of division.', f'{k.numerator} : {k.denominator}; {P(*pt)}',
             f'On the {ax}-axis the {"y" if ax == "x" else "x"}-coordinate is 0: (k × {bracket(b)} + {bracket(a)})/(k + 1) = 0 ⇒ k = {fn(k)}; point {P(*pt)} (3 marks).',
             [f'{k.denominator} : {k.numerator}; {P(*pt)}', f'{k.numerator} : {k.denominator}; {P(pt[1], pt[0])}' if pt[0] != pt[1] else f'1 : 1; {P(*pt)}', f'{abs(a)} : {abs(a) + abs(b)}; {P(*pt)}'])


def c7s3_k(r):
    m, n, A, B, Pp = sect(r)
    which = r.randint(0, 1)
    kv = Pp[which]
    pt = f'(k, {fn(Pp[1])})' if which == 0 else f'({fn(Pp[0])}, k)'
    return Q(f'The point {pt} divides the line segment joining A{P(*A)} and B{P(*B)} in the ratio {m} : {n}. Find k.', f'k = {fn(kv)}',
             f'Use the section formula for the {"x" if which == 0 else "y"}-coordinate: k = ({m} × {bracket(B[which])} + {n} × {bracket(A[which])})/{m + n} = {fn(kv)}.',
             num_distractors(kv, Fr(n * B[which] + m * A[which], m + n), Fr(A[which] + B[which], 2), kv + 1))


def c7s3_four(r):
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    dx, dy = 4 * nz(r, 1, 3), 4 * r.randint(-3, 3)
    pts = [(x1 + dx * i // 4, y1 + dy * i // 4) for i in range(1, 4)]
    return Q(f'Find the coordinates of the points which divide the line segment joining A{P(x1, y1)} and B{P(x1 + dx, y1 + dy)} into four equal parts.', ', '.join(P(*p) for p in pts),
             f'The middle point is the mid-point {P(*pts[1])}; the others are the mid-points of each half: {P(*pts[0])} and {P(*pts[2])} (4 marks).')


def c7s3_ar(r):
    return arbank([
        ('The points of trisection of AB divide it in the ratios 1 : 2 and 2 : 1.', 'Points of trisection divide a segment into three equal parts.', 'a', 'R explains A.'),
        ('The x-axis divides the join of (2, −3) and (5, 6) in the ratio 1 : 2.', 'On the x-axis the y-coordinate is 0.', 'a', '(6k − 3)/(k + 1) = 0 ⇒ k = 1/2.'),
        ('The y-axis divides the join of (4, 1) and (−2, 3) in the ratio 1 : 2.', 'On the y-axis the x-coordinate is 0.', 'd', '(−2k + 4) = 0 ⇒ k = 2, ratio 2 : 1; A false, R true.'),
        ('The mid-point of the join of (a, b) and (−a, −b) is the origin.', 'The origin is the only point on both axes.', 'b', 'Both true, but R does not explain A.'),
    ])(r)


def c7s3_explain(r):
    return xbank([
        ('Explain why it is convenient to take the ratio as k : 1 when finding the ratio in which a point divides a segment.', 'It leaves one unknown k, found from one coordinate equation.', '2 marks.'),
        ('Explain how to find the points of trisection of AB using the section formula.', 'Apply the section formula with ratios 1 : 2 and 2 : 1.', '2 marks.'),
        ('A student says the point dividing AB in the ratio 2 : 3 is the same as the point dividing BA in the ratio 2 : 3. Explain the error.', 'Reversing the segment reverses the ratio: it divides BA in 3 : 2.', '2 marks.'),
    ])(r)


def c7s3_case(r):
    x1, y1 = r.randint(0, 3), r.randint(0, 3)
    dx, dy = 3 * r.randint(2, 5), 3 * r.randint(1, 4)
    p1, p2 = (x1 + dx // 3, y1 + dy // 3), (x1 + 2 * dx // 3, y1 + 2 * dy // 3)
    return Q((f'In a garden, a straight row of plants runs from A{P(x1, y1)} to B{P(x1 + dx, y1 + dy)} (in metres). The gardener plants marigolds at the two points that divide AB into three equal parts. '
              f'(i) In what ratios do these points divide AB? (ii) Find the point nearer to A. (iii) Find the point nearer to B. (iv) Find the mid-point of AB.'),
             f'(i) 1 : 2 and 2 : 1 (ii) {P(*p1)} (iii) {P(*p2)} (iv) {P(Fr(2 * x1 + dx, 2), Fr(2 * y1 + dy, 2))}', '1 mark each part.')


# st4 classify figures

def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def c7s4_quad(r):
    a, b = r.randint(1, 5), r.randint(-4, 4)
    kind = r.choice(['square', 'rhombus', 'rectangle', 'parallelogram'])
    x, y = r.randint(-4, 4), r.randint(-4, 4)
    A = (x, y)
    if kind == 'square':
        u, v = (a, b), (-b, a)
    elif kind == 'rectangle':
        k = r.choice([2, 3])
        u, v = (a, b), (-b * k, a * k)
    elif kind == 'rhombus':
        c, d, e = triple(r)
        u, v = (c, d), (e, 0) if r.random() < 0.5 else (0, e)
        if u[0] * v[0] + u[1] * v[1] == 0:
            raise ValueError
    else:
        u, v = (a, b), (r.randint(1, 4), r.randint(2, 5))
        if u[0] * v[0] + u[1] * v[1] == 0 or d2((0, 0), u) == d2((0, 0), v) or u[0] * v[1] - u[1] * v[0] == 0:
            raise ValueError
    if u[0] * v[1] - u[1] * v[0] == 0:
        raise ValueError
    B = (A[0] + u[0], A[1] + u[1])
    C = (B[0] + v[0], B[1] + v[1])
    D = (A[0] + v[0], A[1] + v[1])
    sides = [d2(A, B), d2(B, C), d2(C, D), d2(D, A)]
    diags = [d2(A, C), d2(B, D)]
    eqs = len(set(sides)) == 1
    eqd = diags[0] == diags[1]
    truth = 'square' if eqs and eqd else 'rhombus' if eqs else 'rectangle' if eqd else 'parallelogram'
    names = ['Square', 'Rhombus (not a square)', 'Rectangle (not a square)', 'Parallelogram (not a rectangle or rhombus)']
    ans = {'square': names[0], 'rhombus': names[1], 'rectangle': names[2], 'parallelogram': names[3]}[truth]
    return Q(f'Name the type of quadrilateral formed by the points A{P(*A)}, B{P(*B)}, C{P(*C)} and D{P(*D)}, giving reasons.', ans,
             f'AB = {rad(sides[0])}, BC = {rad(sides[1])}, CD = {rad(sides[2])}, DA = {rad(sides[3])}; AC = {rad(diags[0])}, BD = {rad(diags[1])}. ' +
             {'square': 'All sides equal and diagonals equal: square.', 'rhombus': 'All sides equal, diagonals unequal: rhombus.', 'rectangle': 'Opposite sides equal and diagonals equal: rectangle.',
              'parallelogram': 'Opposite sides equal, diagonals unequal: parallelogram.'}[truth] + ' (4 marks)', [n for n in names if n != ans])


def c7s4_tri(r):
    kind = r.choice(['isosceles', 'right', 'scalene', 'right isosceles'])
    x, y = r.randint(-4, 4), r.randint(-4, 4)
    a, b, c = triple(r)
    if kind == 'isosceles':
        h = r.randint(2, 6)
        k = r.randint(1, 5)
        A, B, C = (x - k, y), (x + k, y), (x, y + h)
    elif kind == 'right':
        A, B, C = (x, y), (x + a, y), (x, y + b)
    elif kind == 'right isosceles':
        k = r.randint(2, 6)
        A, B, C = (x, y), (x + k, y), (x, y + k)
    else:
        A, B, C = (x, y), (x + r.randint(3, 7), y + 1), (x + 1, y + r.randint(4, 8))
    s = sorted([d2(A, B), d2(B, C), d2(C, A)])
    right = s[0] + s[1] == s[2]
    iso = len(set(s)) < 3
    ans = 'Right-angled isosceles triangle' if right and iso else 'Right-angled triangle' if right else 'Isosceles triangle' if iso else 'Scalene triangle'
    opts = ['Right-angled isosceles triangle', 'Right-angled triangle', 'Isosceles triangle', 'Scalene triangle', 'Equilateral triangle']
    return Q(f'Determine the type of triangle with vertices A{P(*A)}, B{P(*B)} and C{P(*C)}.', ans,
             f'AB² = {d2(A, B)}, BC² = {d2(B, C)}, CA² = {d2(C, A)}. ' + ('Two sides equal. ' if iso else 'All sides different. ') + ('The squares satisfy Pythagoras: right angle.' if right else 'No Pythagoras relation: not right-angled.'),
             [o for o in opts if o != ans][:3])


def c7s4_fourth(r):
    return g9a.c1s3_parallelogram(r)


def c7s4_ar(r):
    return arbank([
        ('(0, 0), (4, 0), (4, 4) and (0, 4) are the vertices of a square.', 'All four sides are 4 units and both diagonals are 4√2 units.', 'a', 'R explains A.'),
        ('A quadrilateral with all sides equal is a square.', 'A square has all sides equal and equal diagonals.', 'd', 'It may be a rhombus; A false, R true.'),
        ('(1, 1), (4, 1) and (1, 5) form a right-angled triangle.', 'The sides are 3, 4 and 5 units and 3² + 4² = 5².', 'a', 'Converse of Pythagoras.'),
        ('To show four points form a parallelogram, it is enough to show the diagonals bisect each other.', 'The mid-points of both diagonals coincide in a parallelogram.', 'a', 'R explains A.'),
    ])(r)


def c7s4_explain(r):
    return xbank([
        ('Explain how you would use the distance formula to distinguish a rhombus from a square.', 'Both have four equal sides; a square also has equal diagonals.', '2 marks.'),
        ('Explain why showing that opposite sides are equal is enough to prove four points (in order) form a parallelogram.', 'A quadrilateral with both pairs of opposite sides equal is a parallelogram.', '2 marks.'),
        ('Explain how to check, using coordinates, whether three points form an equilateral triangle.', 'Find all three distances; the triangle is equilateral if all are equal.', '2 marks.'),
    ])(r)


def c7s4_case(r):
    a = r.randint(2, 6)
    x, y = r.randint(1, 5), r.randint(1, 5)
    A, B, C, D = (x, y), (x + a, y), (x + a, y + a), (x, y + a)
    return Q((f'In a classroom drill, four students stand at A{P(*A)}, B{P(*B)}, C{P(*C)} and D{P(*D)} on a grid with unit 1 m. '
              f'(i) Find AB and BC. (ii) Find the diagonals AC and BD. (iii) What figure do the students form? Justify. (iv) Find the distance of the centre of the figure from A.'),
             f'(i) {a} m, {a} m (ii) {rad(2 * a * a)} m each (iii) square: equal sides and equal diagonals (iv) {rad(2 * a * a)}/2 m'.replace(f'{rad(2 * a * a)}/2', f'{a}√2/2' if a % 2 else f'{a // 2}√2'),
             '1 mark each part.')


# ---------------- ch08 Introduction to Trigonometry ----------------

def tri_pick(r):
    a, b, c = triple(r)
    g = math.gcd(math.gcd(a, b), c)
    return a // g, b // g, c // g


RN = {'sin': 'opposite/hypotenuse', 'cos': 'adjacent/hypotenuse', 'tan': 'opposite/adjacent', 'cosec': 'hypotenuse/opposite', 'sec': 'hypotenuse/adjacent', 'cot': 'adjacent/opposite'}


def ratio(f, o, a, h):
    return {'sin': Fr(o, h), 'cos': Fr(a, h), 'tan': Fr(o, a), 'cosec': Fr(h, o), 'sec': Fr(h, a), 'cot': Fr(a, o)}[f]


def c8s1_find(r):
    o, a, h = tri_pick(r)
    f = r.choice(list(RN))
    v = ratio(f, o, a, h)
    return Q(f'In △ABC right-angled at B, AB = {a} cm and BC = {o} cm. Find AC and {f} A.', f'AC = {h} cm; {f} A = {fn(v)}',
             f'AC² = {a}² + {o}² = {h * h} ⇒ AC = {h}. For angle A, BC is opposite and AB adjacent: {f} A = {RN[f]} = {fn(v)}.',
             [f'AC = {h} cm; {f} A = {fn(1 / v)}', f'AC = {h} cm; {f} A = {fn(ratio({"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan", "sec": "cosec", "cosec": "sec"}[f], o, a, h))}', f'AC = {o + a} cm; {f} A = {fn(v)}'])


def c8s1_others(r):
    o, a, h = tri_pick(r)
    f = r.choice(['sin', 'cos', 'tan', 'sec', 'cot', 'cosec'])
    v = ratio(f, o, a, h)
    want = r.sample([g for g in RN if g != f], 2)
    return Q(f'If {f} A = {fn(v)}, where A is acute, find {want[0]} A and {want[1]} A.', f'{want[0]} A = {fn(ratio(want[0], o, a, h))}, {want[1]} A = {fn(ratio(want[1], o, a, h))}',
             f'Take a right triangle with opposite side {o}k, adjacent side {a}k, hypotenuse {h}k (Pythagoras). Then {want[0]} A = {fn(ratio(want[0], o, a, h))}, {want[1]} A = {fn(ratio(want[1], o, a, h))} (3 marks).')


def c8s1_mcq(r):
    return mcqbank([
        ('In a right triangle, sin A is the ratio …', 'side opposite to A : hypotenuse', ['side adjacent to A : hypotenuse', 'side opposite to A : side adjacent to A', 'hypotenuse : side opposite to A'], 'Definition.'),
        ('tan A is equal to …', 'sin A / cos A', ['cos A / sin A', '1 / sin A', 'sin A × cos A'], '(opp/hyp)/(adj/hyp).'),
        ('cosec A is the reciprocal of …', 'sin A', ['cos A', 'tan A', 'sec A'], 'Definition.'),
        ('For an acute angle A, which value is impossible?', 'sin A = 4/3', ['tan A = 4/3', 'cot A = 4/3', 'sec A = 4/3'], 'sin A ≤ 1 because the hypotenuse is the longest side.'),
        ('If cot A = 12/5, then tan A = …', '5/12', ['12/5', '12/13', '5/13'], 'Reciprocal.'),
        ('In △PQR right-angled at Q, cos P = …', 'PQ/PR', ['QR/PR', 'PQ/QR', 'PR/PQ'], 'Adjacent side to P is PQ.'),
    ])(r)


def c8s1_ar(r):
    o, a, h = tri_pick(r)
    return arbank([
        (f'If sin A = {o}/{h}, then cos A = {a}/{h}.', 'sin²A + cos²A = 1.', 'a', 'Or by Pythagoras on the triangle.'),
        ('The value of sin A can be greater than 1 for some acute angle A.', 'The hypotenuse is the longest side of a right triangle.', 'd', 'sin A < 1; A false, R true.'),
        ('sec A ≥ 1 for every acute angle A.', 'sec A = hypotenuse/adjacent side and the hypotenuse is the longest side.', 'a', 'R explains A.'),
        ('tan A = cot A for every acute angle A.', 'tan A × cot A = 1.', 'd', 'Only for A = 45°; A false, R true.'),
        ('The values of the trigonometric ratios of an angle do not depend on the lengths of the sides of the triangle.', 'Right triangles with the same acute angle are similar.', 'a', 'R explains A.'),
    ])(r)


def c8s1_explain(r):
    return xbank([
        ('Explain why the trigonometric ratios of angle A depend only on A and not on the size of the right triangle.', 'All right triangles with acute angle A are similar (AA), so the side ratios are the same.', '2 marks.'),
        ('Explain why tan A can take any positive value but sin A cannot exceed 1.', 'tan A = opp/adj can be any positive ratio; sin A = opp/hyp and the hypotenuse is the longest side.', '2 marks.'),
        ('Explain why "cos A" is not "cos × A".', 'cos A is one symbol for the ratio adjacent/hypotenuse of angle A, not a product.', '2 marks.'),
    ])(r)


def c8s1_case(r):
    o, a, h = tri_pick(r)
    k = r.choice([1, 2, 3, 0.5])
    return Q((f'A ramp for wheelchairs at a school entrance rises {dec(o * k)} m over a horizontal distance of {dec(a * k)} m. Let θ be the angle the ramp makes with the ground. '
              f'(i) Find the length of the ramp. (ii) Find sin θ. (iii) Find cos θ. (iv) Find tan θ and say what it represents.'),
             f'(i) {dec(h * k)} m (ii) {fn(Fr(o, h))} (iii) {fn(Fr(a, h))} (iv) {fn(Fr(o, a))}, the rise per metre of horizontal run (steepness)', '1 mark each part.')


def c8s1_verify(r):
    o, a, h = tri_pick(r)
    f = r.choice(['tan', 'sec', 'cot', 'cosec'])
    v = ratio(f, o, a, h)
    exprs = {
        'sin²θ + cos²θ': Fr(1),
        '(1 + tan²θ)': Fr(h * h, a * a),
        'sin θ cos θ': Fr(o * a, h * h),
        '(sec θ − tan θ)(sec θ + tan θ)': Fr(1),
        '(1 − tan²θ)/(1 + tan²θ)': Fr(a * a - o * o, h * h),
        'cos²θ − sin²θ': Fr(a * a - o * o, h * h),
    }
    e = r.choice(list(exprs))
    return Q(f'If {f} θ = {fn(v)}, evaluate {e}.', fn(exprs[e]), f'From {f} θ = {fn(v)}, take sides opposite {o}, adjacent {a}, hypotenuse {h}: sin θ = {fn(Fr(o, h))}, cos θ = {fn(Fr(a, h))}, tan θ = {fn(Fr(o, a))}. Substitute: {fn(exprs[e])} (3 marks).',
             num_distractors(float(exprs[e]), float(exprs[e]) + 1 if exprs[e] != 0 else 2, float(Fr(o, a)), float(Fr(a, h))))


# st2 standard angles

SQ = {
    'sin': {0: Fr(0), 30: Fr(1, 4), 45: Fr(1, 2), 60: Fr(3, 4), 90: Fr(1)},
    'cos': {0: Fr(1), 30: Fr(3, 4), 45: Fr(1, 2), 60: Fr(1, 4), 90: Fr(0)},
    'tan': {0: Fr(0), 30: Fr(1, 3), 45: Fr(1), 60: Fr(3)},
    'cot': {30: Fr(3), 45: Fr(1), 60: Fr(1, 3), 90: Fr(0)},
    'sec': {0: Fr(1), 30: Fr(4, 3), 45: Fr(2), 60: Fr(4)},
    'cosec': {30: Fr(4), 45: Fr(2), 60: Fr(4, 3), 90: Fr(1)},
}
VAL = {
    'sin': {0: '0', 30: '1/2', 45: '1/√2', 60: '√3/2', 90: '1'},
    'cos': {0: '1', 30: '√3/2', 45: '1/√2', 60: '1/2', 90: '0'},
    'tan': {0: '0', 30: '1/√3', 45: '1', 60: '√3', 90: 'not defined'},
    'cot': {0: 'not defined', 30: '√3', 45: '1', 60: '1/√3', 90: '0'},
    'sec': {0: '1', 30: '2/√3', 45: '√2', 60: '2', 90: 'not defined'},
    'cosec': {0: 'not defined', 30: '2', 45: '√2', 60: '2/√3', 90: '1'},
}


def c8s2_eval(r):
    n = r.choice([2, 3, 3])
    terms, val = [], Fr(0)
    used = set()
    for i in range(n):
        while True:
            f = r.choice(list(SQ))
            ang = r.choice(list(SQ[f]))
            if (f, ang) not in used and SQ[f][ang] != 0:
                break
        used.add((f, ang))
        c = r.choice([1, 2, 3, 4]) * (1 if i == 0 else r.choice([1, -1]))
        val += c * SQ[f][ang]
        terms.append((c, f, ang))
    txt = ''
    for i, (c, f, ang) in enumerate(terms):
        sign = ('' if c > 0 else '−') if i == 0 else (' + ' if c > 0 else ' − ')
        txt += f'{sign}{"" if abs(c) == 1 else str(abs(c)) + " "}{f}²{ang}°'
    sub_ = ' '.join(f'{"+" if c > 0 else "−"} {abs(c)} × ({VAL[f][ang]})²' for c, f, ang in terms).lstrip('+ ')
    return Q(f'Evaluate: {txt}', fn(val), f'= {sub_} = {fn(val)}.', num_distractors(float(val), float(val) + 1, float(-val) if val else 2, float(val) * 2 if val else 3))


def c8s2_mcq(r):
    f = r.choice(list(VAL))
    ang = r.choice([0, 30, 45, 60, 90])
    v = VAL[f][ang]
    pool = sorted({x for g in VAL.values() for x in g.values()} - {v})
    return mcq(f'The value of {f} {ang}° is …', v, r.sample(pool, 3), 'Standard values table.', r)


def c8s2_solve(r):
    s, d = r.choice([(90, 30), (90, 60), (60, 0), (90, 0), (60, 30), (60, 30)])
    A, B = (s + d) // 2, (s - d) // 2
    e1 = r.choice({60: [('sin', '√3/2'), ('tan', '√3'), ('cos', '1/2')], 90: [('sin', '1'), ('cos', '0')]}[s])
    e2 = r.choice({30: [('cos', '√3/2'), ('tan', '1/√3'), ('sin', '1/2')], 60: [('cos', '1/2'), ('tan', '√3'), ('sin', '√3/2')], 0: [('cos', '1'), ('sin', '0'), ('tan', '0')]}[d])
    return Q(f'If {e1[0]}(A + B) = {e1[1]} and {e2[0]}(A − B) = {e2[1]}, where 0° < A + B ≤ 90° and A ≥ B, find A and B.', f'A = {A}°, B = {B}°',
             f'{e1[0]}(A + B) = {e1[1]} ⇒ A + B = {s}°; {e2[0]}(A − B) = {e2[1]} ⇒ A − B = {d}°; adding, A = {A}°, B = {B}° (3 marks).',
             [f'A = {B}°, B = {A}°' if A != B else f'A = {A + 15}°, B = {B - 15}°', f'A = {s}°, B = {d}°', f'A = {s - d}°, B = {d // 2 + 5}°'])


def c8s2_identity(r):
    a = r.choice([30, 60, 45])
    return xbank([
        ('Evaluate sin 60° cos 30° + sin 30° cos 60°.', '1', '(√3/2)(√3/2) + (1/2)(1/2) = 3/4 + 1/4 = 1.'),
        ('Evaluate cos 60° cos 30° − sin 60° sin 30°.', '0', '(1/2)(√3/2) − (√3/2)(1/2) = 0.'),
        ('Evaluate 2 tan 30° / (1 + tan²30°).', '√3/2', '(2/√3)/(4/3) = √3/2 (= sin 60°).'),
        ('Evaluate (1 − tan²45°)/(1 + tan²45°).', '0', '(1 − 1)/(1 + 1) = 0.'),
        ('Evaluate 2 tan 45° / (1 − tan²45°) and explain the result.', 'not defined', 'The denominator is 1 − 1 = 0 (tan 90° is not defined).'),
        ('Evaluate (sin 30° + tan 45° − cosec 60°)/(sec 30° + cos 60° + cot 45°).', '(43 − 24√3)/11', 'Numerator 3/2 − 2/√3, denominator 3/2 + 2/√3; rationalise: (3√3 − 4)/(3√3 + 4) = (43 − 24√3)/11.'),
        ('Evaluate (5 cos²60° + 4 sec²30° − tan²45°)/(sin²30° + cos²30°).', '67/12', '(5/4 + 16/3 − 1)/1 = 67/12.'),
    ])(r)


def c8s2_check(r):
    return mcqbank([
        ('sin 2A = 2 sin A is true when A = …', '0°', ['30°', '45°', '60°'], 'Only when sin A cos A = sin A, i.e. sin A = 0 for acute/zero A.'),
        ('The value of 2 tan 30° / (1 − tan²30°) is …', '√3', ['1/√3', '1', '√3/2'], '(2/√3)/(2/3) = √3 = tan 60°.'),
        ('As A increases from 0° to 90°, the value of sin A …', 'increases from 0 to 1', ['decreases from 1 to 0', 'stays constant', 'increases from 0 to ∞'], 'From the table.'),
        ('As A increases from 0° to 90°, the value of cos A …', 'decreases from 1 to 0', ['increases from 0 to 1', 'stays the same', 'increases without limit'], 'From the table.'),
        ('Which of these is not defined?', 'tan 90°', ['sin 90°', 'cos 90°', 'cot 90°'], 'cos 90° = 0 in the denominator.'),
        ('sin 45° + cos 45° = …', '√2', ['1', '2', '1/√2'], '1/√2 + 1/√2 = 2/√2.'),
    ])(r)


def c8s2_ar(r):
    return arbank([
        ('tan 90° is not defined.', 'tan 90° = sin 90°/cos 90° and cos 90° = 0.', 'a', 'R explains A.'),
        ('sin (A + B) = sin A + sin B for all A and B.', 'For A = 30° and B = 60°, sin (A + B) = 1 and sin A + sin B = (1 + √3)/2.', 'd', 'The example shows A is false; R true.'),
        ('The value of sin θ increases as θ increases from 0° to 90°.', 'sin 0° = 0 and sin 90° = 1.', 'b', 'Both true; two end values alone do not prove it increases.'),
        ('2 sin 45° cos 45° = 1.', 'sin 45° = cos 45° = 1/√2.', 'a', '2 × 1/2 = 1.'),
    ])(r)


def c8s2_case(r):
    a = r.choice([30, 45, 60])
    L = r.choice([6, 8, 10, 12, 20])
    hs = {30: f'{fn(Fr(L, 2))} m', 45: f'{fn(Fr(L, 2))}√2 m' if L % 2 == 0 else f'{L}/√2 m', 60: f'{fn(Fr(L, 2))}√3 m'}[a]
    ds = {30: f'{fn(Fr(L, 2))}√3 m', 45: f'{fn(Fr(L, 2))}√2 m', 60: f'{fn(Fr(L, 2))} m'}[a]
    return Q((f'A ladder {L} m long leans against a wall in a housing society, making an angle of {a}° with the ground. '
              f'(i) Write sin {a}° and cos {a}°. (ii) How high up the wall does the ladder reach? (iii) How far is its foot from the wall? (iv) If the angle increased to 60°, would the ladder reach higher? Why?'),
             f'(i) {VAL["sin"][a]}, {VAL["cos"][a]} (ii) {hs} (iii) {ds} (iv) ' + ('it is already 60°' if a == 60 else 'yes, sin A increases as A increases'), '1 mark each part.')


# st3 one ratio in terms of another

def c8s3_given(r):
    o, a, h = tri_pick(r)
    f = r.choice(['tan', 'cot', 'sec', 'cosec', 'cos', 'sin'])
    v = ratio(f, o, a, h)
    others = [g for g in RN if g != f]
    return Q(f'Given {f} A = {fn(v)}, A acute, find the other five trigonometric ratios of A.', ', '.join(f'{g} A = {fn(ratio(g, o, a, h))}' for g in others),
             f'Take sides opposite {o}k, adjacent {a}k; hypotenuse {h}k by Pythagoras. Then ' + ', '.join(f'{g} A = {fn(ratio(g, o, a, h))}' for g in others) + ' (4 marks).')


def c8s3_express(r):
    return xbank([
        ('Express sin A, sec A and tan A in terms of cot A.', 'sin A = 1/√(1 + cot²A); sec A = √(1 + cot²A)/cot A; tan A = 1/cot A.', 'Use cosec²A = 1 + cot²A (3 marks).'),
        ('Express sin A, tan A and cot A in terms of sec A.', 'sin A = √(sec²A − 1)/sec A; tan A = √(sec²A − 1); cot A = 1/√(sec²A − 1).', 'Use tan²A = sec²A − 1 (3 marks).'),
        ('Express cos A in terms of sin A, and tan A in terms of sin A.', 'cos A = √(1 − sin²A); tan A = sin A/√(1 − sin²A).', 'From sin²A + cos²A = 1 (2 marks).'),
        ('Express cosec A and cot A in terms of cos A.', 'cosec A = 1/√(1 − cos²A); cot A = cos A/√(1 − cos²A).', '2 marks.'),
        ('Express sec A in terms of tan A, and cos A in terms of tan A.', 'sec A = √(1 + tan²A); cos A = 1/√(1 + tan²A).', '2 marks.'),
    ])(r)


def c8s3_mcq(r):
    return mcqbank([
        ('In terms of cos A, sin A (A acute) = …', '√(1 − cos²A)', ['1 − cos A', '√(cos²A − 1)', '1/cos A'], 'sin²A + cos²A = 1.'),
        ('In terms of tan A, sec A (A acute) = …', '√(1 + tan²A)', ['1 + tan A', '√(tan²A − 1)', '1/tan A'], 'sec²A = 1 + tan²A.'),
        ('In terms of cot A, cosec A (A acute) = …', '√(1 + cot²A)', ['1 + cot A', '1/cot A', '√(cot²A − 1)'], 'cosec²A = 1 + cot²A.'),
        ('In terms of sin A, tan A (A acute) = …', 'sin A/√(1 − sin²A)', ['√(1 − sin²A)/sin A', 'sin A/(1 − sin A)', '1/sin A'], 'tan A = sin A/cos A.'),
    ])(r)


def c8s3_value(r):
    o, a, h = tri_pick(r)
    f = r.choice(['tan', 'cot'])
    v = ratio(f, o, a, h)
    exprs = [('(sin A + cos A)/(sin A − cos A)', Fr(o + a, o - a) if o != a else None),
             ('(2 sin A − cos A)/(2 sin A + cos A)', Fr(2 * o - a, 2 * o + a)),
             ('(1 + sin A)(1 − sin A)/((1 + cos A)(1 − cos A))', Fr(a * a, o * o)),
             ('(cosec A + sec A)/(cosec A − sec A)', Fr(a + o, a - o) if a != o else None)]
    e, val = r.choice(exprs)
    if val is None:
        raise ValueError
    return Q(f'If {f} A = {fn(v)}, evaluate {e}.', fn(val), f'Divide numerator and denominator by a suitable ratio (or use sides {o}, {a}, {h}): value = {fn(val)} (3 marks).',
             num_distractors(float(val), float(-val), float(1 / val) if val else 2, float(val) + 1))


def c8s3_ar(r):
    return arbank([
        ('If tan A = 1, then sin A = cos A.', 'tan A = sin A/cos A.', 'a', 'R explains A.'),
        ('For acute A, sec A = √(1 + tan²A).', '1 + tan²A = sec²A and sec A > 0 for acute A.', 'a', 'R explains A.'),
        ('If sin A = 3/5, then tan A = 4/3.', 'cos A = √(1 − sin²A).', 'd', 'cos A = 4/5 so tan A = 3/4; A false, R true.'),
    ])(r)


def c8s3_explain(r):
    return xbank([
        ('Explain why, for acute A, we take the positive square root when writing cos A = √(1 − sin²A).', 'For an acute angle, all trigonometric ratios are positive (they are ratios of lengths).', '2 marks.'),
        ('Explain how knowing one trigonometric ratio of an acute angle determines all the others.', 'One ratio fixes two sides in proportion; Pythagoras gives the third; then all ratios follow.', '2 marks.'),
    ])(r)


def c8s3_case(r):
    o, a, h = tri_pick(r)
    k = r.choice([2, 5, 10, 20])
    return Q((f'A kite flies at the end of a straight string. The angle θ of the string with the ground satisfies tan θ = {o}/{a}. The horizontal distance from the child to the point below the kite is {a * k} m. '
              f'(i) Find the height of the kite. (ii) Find sin θ and cos θ. (iii) Find the length of the string. (iv) Express sec θ in terms of tan θ and check its value.'),
             f'(i) {o * k} m (ii) {o}/{h}, {a}/{h} (iii) {h * k} m (iv) sec θ = √(1 + tan²θ) = {fn(Fr(h, a))}', '1 mark each part.')


# st4 identities

PROOFS = [
    ('Prove that (1 + tan²A) cos²A = 1.', 'sec²A × cos²A = 1.'),
    ('Prove that (cosec θ − cot θ)² = (1 − cos θ)/(1 + cos θ).', 'LHS = ((1 − cos θ)/sin θ)² = (1 − cos θ)²/(1 − cos²θ) = (1 − cos θ)/(1 + cos θ).'),
    ('Prove that cos A/(1 + sin A) + (1 + sin A)/cos A = 2 sec A.', 'Combine: (cos²A + 1 + 2 sin A + sin²A)/(cos A(1 + sin A)) = 2(1 + sin A)/(cos A(1 + sin A)) = 2 sec A.'),
    ('Prove that √((1 + sin A)/(1 − sin A)) = sec A + tan A.', 'Multiply inside by (1 + sin A)/(1 + sin A): √((1 + sin A)²/cos²A) = (1 + sin A)/cos A.'),
    ('Prove that (sin θ − 2 sin³θ)/(2 cos³θ − cos θ) = tan θ.', 'sin θ(1 − 2 sin²θ)/(cos θ(2 cos²θ − 1)); 1 − 2 sin²θ = 2 cos²θ − 1, so the ratio is tan θ.'),
    ('Prove that (sin A + cosec A)² + (cos A + sec A)² = 7 + tan²A + cot²A.', 'Expand: sin²A + cos²A + cosec²A + sec²A + 4 = 1 + (1 + cot²A) + (1 + tan²A) + 4.'),
    ('Prove that (1 + sec A)/sec A = sin²A/(1 − cos A).', 'LHS = 1 + cos A; RHS = (1 − cos²A)/(1 − cos A) = 1 + cos A.'),
    ('Prove that (1 + 1/tan²A)(1 + 1/cot²A) = 1/(sin²A − sin⁴A).', 'LHS = cosec²A sec²A = 1/(sin²A cos²A) = 1/(sin²A(1 − sin²A)).'),
    ('Prove that sec⁴θ − sec²θ = tan⁴θ + tan²θ.', 'sec²θ(sec²θ − 1) = (1 + tan²θ) tan²θ.'),
    ('Prove that (tan θ)/(1 − cot θ) + (cot θ)/(1 − tan θ) = 1 + sec θ cosec θ.', 'Write in sin and cos, combine and factorise a³ − b³: result 1 + 1/(sin θ cos θ).'),
    ('Prove that (cos A − sin A + 1)/(cos A + sin A − 1) = cosec A + cot A.', 'Divide by sin A and use cosec²A − cot²A = 1 to replace 1 in the numerator.'),
    ('Prove that (cosec A − sin A)(sec A − cos A) = 1/(tan A + cot A).', 'LHS = (cos²A/sin A)(sin²A/cos A) = sin A cos A; RHS = 1/(1/(sin A cos A)) = sin A cos A.'),
]


def c8s4_prove(r):
    s, k = r.choice(PROOFS)
    return Q(s, 'Proof', f'{k} (Marks: correct identity used, simplification, conclusion.)')


def c8s4_num(r):
    k = r.randint(2, 12)
    forms = [
        (f'{k} sec²A − {k} tan²A', k),
        (f'{k}(cosec²A − cot²A)', k),
        (f'(1 + tan²A)(1 − sin²A) × {k}', k),
        (f'{k} sin²A + {k} cos²A', k),
        (f'(sec A + tan A)(1 − sin A) × {k} / cos A', k),
        (f'{k}(1 + cot²A) sin²A', k),
    ]
    e, v = r.choice(forms)
    return mcq(f'For an acute angle A, the value of {e} is …', str(v), [str(v + 1), str(2 * v), '1' if v != 1 else '0'] if v != 1 else ['0', '2', '3'],
               'Use sin²A + cos²A = 1, sec²A − tan²A = 1, cosec²A − cot²A = 1.', r)


def c8s4_sectan(r):
    p = Fr(r.randint(2, 9), r.randint(1, 4))
    if p <= 1:
        raise ValueError
    which = r.choice(['sec θ + tan θ', 'cosec θ + cot θ'])
    other = which.replace('+', '−')
    q = 1 / p
    if which.startswith('sec'):
        sec, tan = (p + q) / 2, (p - q) / 2
        extra = f'sec θ = {fn(sec)}, tan θ = {fn(tan)}'
    else:
        sec, tan = (p + q) / 2, (p - q) / 2
        extra = f'cosec θ = {fn(sec)}, cot θ = {fn(tan)}'
    return Q(f'If {which} = {fn(p)}, find {other} and hence {extra.split(",")[0].split(" =")[0]}.', f'{other} = {fn(q)}; {extra.split(",")[0]}',
             f'({which})({other}) = {"sec²θ − tan²θ" if which.startswith("sec") else "cosec²θ − cot²θ"} = 1 ⇒ {other} = {fn(q)}; adding, 2{extra.split(",")[0].split(" =")[0]} = {fn(p + q)} (3 marks).')


def c8s4_mcq(r):
    return mcqbank([
        ('sin²A + cos²A = …', '1', ['0', '2', 'tan²A'], 'Basic identity.'),
        ('1 + tan²A = …', 'sec²A', ['cosec²A', 'cot²A', 'sin²A'], 'Divide sin²A + cos²A = 1 by cos²A.'),
        ('cosec²A − cot²A = …', '1', ['0', '−1', 'sec²A'], 'Identity.'),
        ('(1 + cos A)(1 − cos A) = …', 'sin²A', ['cos²A', '1', 'tan²A'], '1 − cos²A.'),
        ('(sec A + tan A)(1 − sin A) = …', 'cos A', ['sec A', 'sin A', 'cosec A'], '((1 + sin A)/cos A)(1 − sin A) = cos²A/cos A.'),
        ('(1 + tan²A)/(1 + cot²A) = …', 'tan²A', ['cot²A', 'sec²A', '−1'], 'sec²A/cosec²A = sin²A/cos²A.'),
    ])(r)


def c8s4_ar(r):
    return arbank([
        ('9 sec²A − 9 tan²A = 9.', 'sec²A − tan²A = 1.', 'a', 'R explains A.'),
        ('sin²A + cos²A = 1 for every acute angle A.', 'In a right triangle, (opposite)² + (adjacent)² = (hypotenuse)².', 'a', 'Divide by hypotenuse².'),
        ('sin A + cos A = 1 for every acute angle A.', 'sin²A + cos²A = 1.', 'd', 'e.g. A = 45°: √2 ≠ 1; A false, R true.'),
        ('If sec θ + tan θ = 2, then sec θ − tan θ = 1/2.', 'sec²θ − tan²θ = 1.', 'a', 'Product of the two is 1.'),
    ])(r)


def c8s4_explain(r):
    return xbank([
        ('Explain how the identity 1 + tan²A = sec²A is obtained from sin²A + cos²A = 1, and for which angles it holds.', 'Divide by cos²A; valid for 0° ≤ A < 90° (cos A ≠ 0).', '2 marks.'),
        ('Explain why an identity is different from an equation.', 'An identity holds for all values of the angle for which both sides are defined; an equation holds only for particular values.', '2 marks.'),
        ('Explain why cosec²A − cot²A = 1 is not defined at A = 0°.', 'cosec 0° and cot 0° are not defined (sin 0° = 0).', '2 marks.'),
    ])(r)


def c8s4_case(r):
    o, a, h = tri_pick(r)
    return Q((f'In a quiz, a team is told that for an acute angle θ, sin θ = {o}/{h}. '
              f'(i) Find cos θ using an identity. (ii) Find tan θ. (iii) Verify 1 + tan²θ = sec²θ. (iv) Find sec θ + tan θ and sec θ − tan θ, and their product.'),
             f'(i) {a}/{h} (ii) {fn(Fr(o, a))} (iii) 1 + {fn(Fr(o * o, a * a))} = {fn(Fr(h * h, a * a))} = ({fn(Fr(h, a))})² (iv) {fn(Fr(h + o, a))}, {fn(Fr(h - o, a))}; product 1', '1 mark each part.')


# ---------------- ch09 Some Applications of Trigonometry ----------------

class R3:
    """p + q√3 with rational p, q."""

    def __init__(self, p, q=0):
        self.p, self.q = Fr(p), Fr(q)

    def __add__(self, o):
        o = o if isinstance(o, R3) else R3(o)
        return R3(self.p + o.p, self.q + o.q)

    def __mul__(self, o):
        o = o if isinstance(o, R3) else R3(o)
        return R3(self.p * o.p + 3 * self.q * o.q, self.p * o.q + self.q * o.p)

    __rmul__ = __mul__

    def inv(self):
        d = self.p * self.p - 3 * self.q * self.q
        return R3(self.p / d, -self.q / d)

    def __truediv__(self, o):
        o = o if isinstance(o, R3) else R3(o)
        return self * o.inv()

    def val(self):
        return float(self.p) + float(self.q) * R3V

    def __str__(self):
        p, q = self.p, self.q
        ps = dec(p) if p.denominator in (1, 2, 4, 5, 10) else fn(p)
        if q == 0:
            return ps
        aq = abs(q)
        if aq.denominator == 1:
            qt = ('' if aq == 1 else fn(aq)) + '√3'
        else:
            qt = ('' if aq.numerator == 1 else str(aq.numerator)) + f'√3/{aq.denominator}'
        if p == 0:
            return ('−' if q < 0 else '') + qt
        if p < 0 and q > 0:
            return f'{qt} − {dec(-p) if p.denominator in (1, 2, 4, 5, 10) else fn(-p)}'
        return f'{ps} {"+" if q > 0 else "−"} {qt}'

    def show(self, unit='m'):
        s = str(self)
        if self.q == 0:
            return f'{s} {unit}'
        if self.p != 0:
            s = f'({s})'
        return f'{s} {unit} ≈ {dec(self.val())} {unit}'

    def ok(self):
        return self.p.denominator == 1 and self.q.denominator in (1, 3)


TAN = {30: R3(0, Fr(1, 3)), 45: R3(1), 60: R3(0, 1)}
COT = {30: R3(0, 1), 45: R3(1), 60: R3(0, Fr(1, 3))}
SIN_ = {30: R3(Fr(1, 2)), 60: R3(0, Fr(1, 2))}


def c9s1_mcq(r):
    return mcqbank([
        ('The angle of elevation of an object above the horizontal level of the eye is the angle formed by …', 'the line of sight with the horizontal', ['the line of sight with the vertical', 'the object with the ground', 'two lines of sight'], 'Definition.'),
        ('The angle of elevation of the top of a tower from a point on the ground is θ. As the observer moves towards the tower, θ …', 'increases', ['decreases', 'remains the same', 'first increases then decreases'], 'Closer means steeper line of sight.'),
        ('If the angle of depression of a boat from a lighthouse is 30°, then the angle of elevation of the top of the lighthouse from the boat is …', '30°', ['60°', '90°', '45°'], 'Alternate angles with the parallel horizontal lines.'),
        ('The line of sight is the line drawn from …', 'the eye of the observer to the point being viewed', ['the foot of the observer to the object', 'the object to the ground', 'the sun to the object'], 'Definition.'),
        ('If a pole of height h casts a shadow of length h, the sun\'s altitude is …', '45°', ['30°', '60°', '90°'], 'tan θ = h/h = 1.'),
        ('The angle of depression is measured …', 'below the horizontal through the observer\'s eye', ['above the horizontal', 'from the vertical', 'at the object'], 'Definition.'),
    ])(r)


def c9s1_shadow(r):
    h = r.choice([3, 6, 9, 12, 15, 18, 24, 30])
    ang = r.choice([30, 45, 60])
    sh = h * COT[ang]
    return Q(f'A vertical pole {h} m high casts a shadow {sh} m long on the ground. Find the angle of elevation of the sun.', f'{ang}°',
             f'tan θ = {h}/({sh}) = {VAL["tan"][ang]} ⇒ θ = {ang}°.', [f'{a}°' for a in (30, 45, 60, 90) if a != ang])


def c9s1_ar(r):
    return arbank([
        ('The angle of depression of a car from the top of a building equals the angle of elevation of the top of the building from the car.', 'They are alternate angles between parallel horizontal lines.', 'a', 'R explains A.'),
        ('As a person walks away from a tower, the angle of elevation of its top increases.', 'tan θ = height/distance.', 'd', 'Distance increases so θ decreases; A false, R true.'),
        ('If the length of the shadow of a tower is √3 times its height, the sun\'s elevation is 30°.', 'tan 30° = 1/√3.', 'a', 'tan θ = h/(√3 h).'),
        ('The angle of elevation can be greater than 90°.', 'Angles of elevation are measured from the horizontal.', 'd', 'It lies between 0° and 90°; A false, R true.'),
    ])(r)


def c9s1_explain(r):
    return xbank([
        ('Explain the difference between the angle of elevation and the angle of depression, with a diagram description.', 'Elevation: line of sight above the horizontal (looking up); depression: below the horizontal (looking down).', '2 marks.'),
        ('Explain why the angle of depression from A to B equals the angle of elevation from B to A.', 'The horizontals at A and B are parallel; the line of sight is a transversal, so the angles are alternate angles.', '2 marks.'),
        ('Explain why the sun\'s altitude decreases as shadows get longer in the evening.', 'tan θ = height/shadow; a longer shadow gives a smaller tan θ, so a smaller angle.', '2 marks.'),
        ('Explain what "height of the observer is negligible" means in height and distance problems.', 'We take the eye at ground level, so the angle is measured from the ground.', '2 marks.'),
    ])(r)


def c9s1_case(r):
    h = r.choice([20, 30, 40, 50, 60, 75])
    ang = r.choice([30, 45, 60])
    d = R3(h) * COT[ang]
    return Q((f'A lighthouse is {h} m tall. A boat is seen from its top at an angle of depression of {ang}°. '
              f'(i) What is the angle of elevation of the top of the lighthouse from the boat? Why? (ii) Draw a rough figure and name the right angle. (iii) Find the distance of the boat from the foot of the lighthouse. (iv) If the boat moves towards the lighthouse, what happens to the angle of depression?'),
             f'(i) {ang}°, alternate angles (ii) the right angle is at the foot of the lighthouse (iii) {d.show()} (iv) it increases', '1 mark each part.')


# st2 one triangle

def c9s2_height(r):
    ang = r.choice([30, 45, 60])
    d = r.choice([10, 12, 15, 18, 20, 24, 30, 36, 45, 50, 60]) * (3 if ang == 30 and r.random() < 0.5 else 1)
    h = R3(d) * TAN[ang]
    obj = r.choice(['tower', 'tree', 'building', 'temple spire', 'flagpole'])
    return Q(f'The angle of elevation of the top of a {obj} from a point on the ground {d} m away from its foot is {ang}°. Find the height of the {obj}.', h.show(),
             f'tan {ang}° = h/{d} ⇒ h = {d} × {VAL["tan"][ang]} = {h}' + (f' ≈ {dec(h.val())} m (√3 ≈ 1.732).' if h.q else ' m.'),
             [(R3(d) * COT[ang]).show() if ang != 45 else f'{d * 2} m', f'{d} m' if ang != 45 else f'{d}√3 m', (R3(d) * SIN_.get(ang, R3(Fr(1, 2)))).show()])


def c9s2_distance(r):
    ang = r.choice([30, 45, 60])
    h = r.choice([10, 15, 20, 25, 30, 40, 50, 60, 75, 100]) * (3 if ang == 60 and r.random() < 0.5 else 1)
    d = R3(h) * COT[ang]
    ctx = r.choice([('the top of a cliff', 'a boat', 'the boat from the foot of the cliff'), ('the top of a building', 'a car parked on the road', 'the car from the foot of the building'),
                    ('the top of a tower', 'a cow grazing in a field', 'the cow from the foot of the tower'), ('a bridge', 'a boat on the river', 'the boat from the point directly below the observer')])
    return Q(f'From {ctx[0]} {h} m high, the angle of depression of {ctx[1]} is {ang}°. Find the horizontal distance of {ctx[2]}.',
             d.show(), f'Angle of elevation from the object = {ang}° (alternate). tan {ang}° = {h}/x ⇒ x = {h} × cot {ang}° = {d}' + (f' ≈ {dec(d.val())} m.' if d.q else ' m.'),
             [(R3(h) * TAN[ang]).show() if ang != 45 else f'{h}√3 m ≈ {dec(h * R3V)} m', f'{2 * h} m', f'{h}√2 m'])


def c9s2_kite(r):
    ang = r.choice([30, 60])
    L = r.choice([20, 40, 60, 80, 100, 120, 150])
    h = R3(L) * SIN_[ang]
    return Q(f'A kite is flying at the end of a {L} m long string, which makes an angle of {ang}° with the ground. Assuming the string is straight, find the height of the kite.', h.show(),
             f'sin {ang}° = h/{L} ⇒ h = {L} × {VAL["sin"][ang]} = {h}' + (f' ≈ {dec(h.val())} m.' if h.q else ' m.'),
             [(R3(L) * SIN_[90 - ang]).show(), f'{L} m', f'{L * 2} m'])


def c9s2_string(r):
    ang = r.choice([30, 45, 60])
    h = r.choice([30, 45, 60, 75, 90])
    L = {30: R3(2 * h), 45: None, 60: R3(0, Fr(2 * h, 3))}[ang]
    if ang == 45:
        txt = f'{h}√2 m ≈ {dec(h * 1.414)} m'
        why = f'sin 45° = {h}/L ⇒ L = {h}√2'
    else:
        txt = L.show()
        why = f'sin {ang}° = {h}/L ⇒ L = {h} ÷ ({VAL["sin"][ang]}) = {L}'
    obj = r.choice(['A circus artist climbs a rope tied from the top of a vertical pole to the ground', 'A slide for children has its top'])
    if obj.startswith('A slide'):
        return Q(f'A slide in a park has its top {fn(Fr(h, 15))} m above the ground and is inclined at {ang}° to the ground. Find the length of the slide.',
                 (R3(Fr(h, 15)) / SIN_[ang]).show() if ang != 45 else f'{fn(Fr(h, 15))}√2 m ≈ {dec(h / 15 * 1.414)} m', f'sin {ang}° = height/length.')
    return Q(f'{obj}. The pole is {h} m high and the rope makes an angle of {ang}° with the ground. Find the length of the rope.', txt, why + '.')


def c9s2_broken(r):
    d = r.choice([6, 8, 9, 10, 12, 15])
    ang = r.choice([30, 60])
    # tree broken: top touches ground at distance d, broken part makes ang with ground
    upright = R3(d) * TAN[ang]
    broken = R3(d) / R3(Fr(1, 2) if ang == 60 else 0, 0 if ang == 60 else Fr(1, 2))
    total = upright + broken
    return Q(f'A tree breaks due to a storm and the broken part bends so that its top touches the ground, making an angle of {ang}° with the ground. The top touches the ground {d} m from the foot of the tree. Find the original height of the tree.',
             total.show(), f'Standing part = {d} tan {ang}° = {upright}; broken part = {d}/cos {ang}° = {broken}; height = {total} (4 marks).')


def c9s2_ar(r):
    return arbank([
        ('If a tower 30 m high casts a shadow 10√3 m long, the angle of elevation of the sun is 60°.', 'tan 60° = √3.', 'a', '30/(10√3) = √3.'),
        ('In height and distance problems we use tan θ when the height and the horizontal distance are involved.', 'tan θ = opposite/adjacent in the right triangle formed.', 'a', 'R explains A.'),
        ('A 10 m ladder at 60° to the ground reaches 5 m up the wall.', 'sin 60° = √3/2.', 'd', 'It reaches 5√3 m; A false, R true.'),
    ])(r)


def c9s2_explain(r):
    return xbank([
        ('Explain which trigonometric ratio you would use to find the height of a tower when the distance from its foot and the angle of elevation are known.', 'tan θ = height/distance, because both sides are the legs of the right triangle.', '2 marks.'),
        ('Explain which ratio to use for the height of a kite when the string length and its angle with the ground are known.', 'sin θ = height/string length (the string is the hypotenuse).', '2 marks.'),
    ])(r)


def c9s2_case(r):
    h = r.choice([1.5, 1.2, 1.6])
    d = r.choice([20, 25, 30, 40, 45])
    ang = r.choice([30, 45, 60])
    top = R3(d) * TAN[ang] + R3(Fr(str(h)))
    who = name(r)
    return Q((f'{who}, whose eyes are {dec(h)} m above the ground, stands {d} m from a chimney and finds the angle of elevation of its top to be {ang}°. '
              f'(i) Draw a figure and mark the right triangle. (ii) Find the height of the chimney above {who}\'s eye level. (iii) Find the total height of the chimney. (iv) If {who} moved closer, would the angle increase or decrease?'),
             f'(i) right angle at the point on the chimney at eye level (ii) {(R3(d) * TAN[ang]).show()} (iii) {top.show()} (iv) increase', '1 mark each part.')


# st3 two angles

def c9s3_same_side(r):
    pair = r.choice([(30, 60), (30, 45), (45, 60)])
    d = r.choice([10, 20, 30, 40, 50, 60, 100])
    a, b = pair
    # h = d / (cot a − cot b)
    h = R3(d) / (COT[a] + R3(-1) * COT[b])
    x = h * COT[b]
    obj = r.choice(['tower', 'building', 'tree', 'statue on a hill', 'minar'])
    return Q(f'The angle of elevation of the top of a {obj} from a point on the ground is {a}°. On walking {d} m towards the {obj}, the angle becomes {b}°. Find the height of the {obj}.', h.show(),
             f'Let height h and the nearer distance x. h = x tan {b}° and h = (x + {d}) tan {a}° ⇒ h = {d}/(cot {a}° − cot {b}°) = {h}' + (f' ≈ {dec(h.val())} m' if h.q else ' m') + f'; x = {x} (4 marks).')


def c9s3_opposite(r):
    a, b = r.choice([(30, 60), (45, 45), (30, 45), (45, 60), (60, 60), (30, 30)])
    D = r.choice([40, 60, 80, 100, 120])
    h = R3(D) / (COT[a] + COT[b])
    return Q(f'Two people are on opposite sides of a vertical pole, on a straight road through its foot, {D} m apart. The angles of elevation of the top of the pole from them are {a}° and {b}°. Find the height of the pole.',
             h.show(), f'Distances x and {D} − x: h = x tan {a}° = ({D} − x) tan {b}° ⇒ h = {D}/(cot {a}° + cot {b}°) = {h}' + (f' ≈ {dec(h.val())} m (4 marks).' if h.q else ' m (4 marks).'))


def c9s3_building(r):
    b = r.choice([7, 8, 10, 12, 15, 20, 24, 30])
    up, dn = r.choice([(60, 45), (60, 30), (45, 30), (30, 45), (45, 60)])
    x = R3(b) * COT[dn]
    H = R3(b) + x * TAN[up]
    return Q(f'From the top of a {b} m high building, the angle of elevation of the top of a cable tower is {up}° and the angle of depression of its foot is {dn}°. Find the height of the tower.',
             H.show(), f'Distance between them x = {b} cot {dn}° = {x}; height above the building top = x tan {up}° = {x * TAN[up]}; tower = {b} + {x * TAN[up]}' + ('' if str(H) == f'{b} + {x * TAN[up]}' else f' = {H}') + ' (4 marks).')


def c9s3_two_depr(r):
    a, b = r.choice([(30, 45), (30, 60), (45, 60)])
    h = r.choice([60, 75, 90, 100, 120, 150])
    d = R3(h) * (COT[a] + R3(-1) * COT[b])
    return Q(f'From the top of a {h} m high lighthouse, the angles of depression of two ships on the same side, in line with its foot, are {a}° and {b}°. Find the distance between the ships.',
             d.show(), f'Distances from the foot: {h} cot {a}° = {R3(h) * COT[a]} and {h} cot {b}° = {R3(h) * COT[b]}; difference = {d} (4 marks).')


def c9s3_flag(r):
    d = r.choice([10, 15, 20, 30, 40])
    a, b = r.choice([(45, 60), (30, 45), (30, 60)])
    h1 = R3(d) * TAN[a]
    h2 = R3(d) * TAN[b]
    flag = h2 + R3(-1) * h1
    obj = r.choice(['flagstaff', 'transmission tower', 'statue'])
    base = r.choice(['building', 'pedestal', 'hill'])
    return Q(f'From a point on the ground {d} m from the foot of a {base}, the angles of elevation of the bottom and the top of a {obj} fixed on the {base} are {a}° and {b}°. Find the height of the {base} and of the {obj}.',
             f'{base.capitalize()}: {h1.show()}; {obj}: {flag.show()}', f'{base} height = {d} tan {a}° = {h1}; top height = {d} tan {b}° = {h2}; difference = {flag} (4 marks).')


def c9s3_ar(r):
    return arbank([
        ('When an observer walks towards a tower, the angle of elevation of its top increases.', 'For a fixed height, tan θ = height/distance increases as distance decreases.', 'a', 'R explains A.'),
        ('If the angles of elevation of a tower from two points at distances a and b from its foot on the same line are complementary, the height is √(ab).', 'tan θ × tan (90° − θ) = 1.', 'a', 'h/a × h/b = 1 ⇒ h² = ab.'),
        ('Two-angle problems can always be solved with only one right triangle.', 'Each angle gives a separate right triangle with the common height.', 'd', 'Two triangles are needed; A false, R true.'),
    ])(r)


def c9s3_comp(r):
    a, b = r.choice([(4, 9), (2, 8), (3, 12), (4, 16), (9, 16), (1, 4), (5, 20), (6, 24)])
    return Q(f'The angles of elevation of the top of a tower from two points at distances {a} m and {b} m from its base, on the same straight line, are complementary. Find the height of the tower.', f'{math.isqrt(a * b)} m',
             f'tan θ = h/{b} and tan (90° − θ) = cot θ = h/{a}; multiplying, 1 = h²/({a * b}) ⇒ h = {math.isqrt(a * b)} m (3 marks).',
             num_distractors(math.isqrt(a * b), (a + b) / 2, a * b, b - a))


def c9s3_explain(r):
    return xbank([
        ('Explain the strategy for solving a problem where the angle of elevation of a tower changes from 30° to 60° as you walk towards it.', 'Draw two right triangles sharing the height; write tan 30° and tan 60° equations with the unknown distance; eliminate it to find the height.', '2 marks.'),
        ('Explain why, in a two-observer problem on opposite sides of a tower, the distances add up but on the same side they subtract.', 'On opposite sides the foot lies between the observers; on the same side one distance contains the other.', '2 marks.'),
    ])(r)


def c9s3_case(r):
    d = r.choice([20, 30, 40, 50, 60])
    h = R3(d) / (COT[30] + R3(-1) * COT[60])
    who = name(r)
    return Q((f'{who} sees the top of a mobile tower at an angle of elevation of 30°. After walking {d} m straight towards it, the angle becomes 60°. '
              f'(i) Draw the figure with two right triangles. (ii) Write equations for the height h using both angles. (iii) Find h. (iv) How far is {who} from the tower at the end?'),
             f'(i) two triangles with common vertical side h (ii) h = x√3 and h = (x + {d})/√3 (iii) {h.show()} (iv) {fn(Fr(d, 2))} m', '1 mark each part.')


# ---------------- ch10 Circles ----------------

def c10s1_tangent_len(r):
    a, b, c = triple(r)
    k = r.choice([1, 1, 2])
    rr, t, d = a * k, b * k, c * k
    ask = r.choice(['t', 't', 'r', 'd'])
    if ask == 't':
        return Q(f'From a point Q, the length of the tangent to a circle is to be found. The radius is {rr} cm and the distance of Q from the centre is {d} cm. Find the length of the tangent.', f'{t} cm',
                 f'The radius is perpendicular to the tangent at the point of contact; by Pythagoras, tangent = √({d}² − {rr}²) = {t} cm.', num_distractors(t, d - rr, d + rr, t + 2))
    if ask == 'r':
        return Q(f'From a point Q, {d} cm from the centre O of a circle, the length of the tangent is {t} cm. Find the radius of the circle.', f'{rr} cm',
                 f'OP ⟂ PQ, so OP² = OQ² − PQ² = {d * d} − {t * t} = {rr * rr} ⇒ r = {rr} cm.', num_distractors(rr, d - t, d + t, rr + 1))
    return Q(f'The length of a tangent from a point A to a circle of radius {rr} cm is {t} cm. Find the distance of A from the centre.', f'{d} cm',
             f'OA² = {rr}² + {t}² = {d * d} ⇒ OA = {d} cm.', num_distractors(d, rr + t, d + 1, abs(t - rr)))


def c10s1_mcq(r):
    return mcqbank([
        ('The tangent at any point of a circle is … the radius through the point of contact.', 'perpendicular to', ['parallel to', 'equal to', 'inclined at 45° to'], 'Theorem 10.1.'),
        ('A tangent to a circle intersects it in …', 'exactly one point', ['two points', 'no point', 'infinitely many points'], 'Definition of a tangent.'),
        ('A line intersecting a circle in two points is called a …', 'secant', ['tangent', 'chord', 'radius'], 'Definition.'),
        ('How many tangents can a circle have?', 'infinitely many', ['one', 'two', 'four'], 'One at each point of the circle.'),
        ('The number of tangents parallel to a given secant of a circle is …', '2', ['1', '0', 'infinitely many'], 'One on each side.'),
        ('The tangents drawn at the ends of a diameter of a circle are …', 'parallel', ['perpendicular', 'intersecting at the centre', 'equal to the diameter'], 'Both are perpendicular to the same diameter.'),
        ('The common point of a tangent and the circle is called the …', 'point of contact', ['centre', 'point of intersection of chords', 'vertex'], 'Definition.'),
    ])(r)


def c10s1_angle(r):
    x = r.randint(20, 70)
    kind = r.randint(0, 2)
    if kind == 0:
        return Q(f'PT is a tangent at T to a circle with centre O. If ∠TOP = {x}°, find ∠OPT.', f'{90 - x}°', f'∠OTP = 90° (radius ⟂ tangent), so ∠OPT = 180° − 90° − {x}° = {90 - x}°.',
                 num_distractors(90 - x, x, 180 - x, 90 + x))
    if kind == 1:
        return Q(f'AB is a tangent to a circle with centre O at A, and AC is a chord with ∠BAC = {x}°. Find ∠OAC.', f'{90 - x}°', f'∠OAB = 90° (radius ⟂ tangent) ⇒ ∠OAC = 90° − {x}° = {90 - x}°.',
                 num_distractors(90 - x, x, 2 * x, 180 - 2 * x))
    return Q(f'A tangent PQ at a point P of a circle of radius {x // 4 + 3} cm meets a line through the centre O at Q. If ∠PQO = {x}°, find ∠POQ.', f'{90 - x}°',
             f'∠OPQ = 90°; ∠POQ = 180° − 90° − {x}° = {90 - x}°.', num_distractors(90 - x, x, 180 - x, 2 * x))


def c10s1_prove(r):
    return xbank([
        ('Prove that the tangent at any point of a circle is perpendicular to the radius through the point of contact.',
         'Let XY be the tangent at P. Take any point Q ≠ P on XY; Q lies outside the circle, so OQ > OP. Thus OP is the shortest distance from O to XY, hence OP ⟂ XY.',
         'Figure (1), any other point outside (1), OQ > OP (1), shortest distance is perpendicular (1), conclusion (1).'),
        ('Prove that the tangents drawn at the ends of a diameter of a circle are parallel.',
         'Tangents at A and B are perpendicular to diameter AB; two lines perpendicular to the same line are parallel (alternate/co-interior angles 90°).', '3 marks.'),
        ('Prove that the perpendicular at the point of contact to the tangent to a circle passes through the centre.',
         'The radius at the point of contact is perpendicular to the tangent; there is only one perpendicular at that point, so it contains the radius and hence the centre.', '3 marks.'),
    ])(r)


def c10s1_ar(r):
    a, b, c = triple(r)
    return arbank([
        (f'The length of the tangent from a point {c} cm from the centre of a circle of radius {a} cm is {b} cm.', 'The tangent is perpendicular to the radius at the point of contact.', 'a', 'Pythagoras on the right triangle.'),
        ('A circle can have at most two parallel tangents in a given direction.', 'Tangents at the ends of a diameter are parallel.', 'a', 'R explains A.'),
        ('A tangent to a circle can pass through the centre.', 'A tangent meets the circle at exactly one point.', 'd', 'A line through the centre meets the circle twice; A false, R true.'),
        ('From a point inside a circle, no tangent can be drawn.', 'Every line through a point inside the circle is a secant.', 'a', 'R explains A.'),
    ])(r)


def c10s1_explain(r):
    return xbank([
        ('Explain why no tangent can be drawn to a circle from a point inside it.', 'Any line through an interior point cuts the circle at two points (it is a secant).', '2 marks.'),
        ('Explain how a tangent can be thought of as a special case of a secant.', 'As the two intersection points of a secant move together and coincide, the secant becomes the tangent.', '2 marks.'),
        ('Explain why the shortest distance from the centre to a tangent is the radius.', 'Every other point of the tangent lies outside the circle, so its distance from the centre is greater than the radius.', '2 marks.'),
    ])(r)


def c10s1_case(r):
    a, b, c = triple(r)
    k = r.choice([1, 2, 10])
    return Q((f'A circular fountain in a park has radius {a * k} m. A straight footpath touches the fountain\'s boundary at point P. A lamp post L stands on the path {b * k} m from P. '
              f'(i) What is the angle between the radius OP and the path? Why? (ii) Find the distance OL. (iii) Is the lamp post inside or outside the fountain? (iv) How many such straight paths through L can touch the fountain?'),
             f'(i) 90°, the tangent is perpendicular to the radius at the point of contact (ii) {c * k} m (iii) outside, since {c * k} > {a * k} (iv) 2', '1 mark each part.')


# st2 tangents from a point

def c10s2_angle(r):
    t = r.choice([30, 40, 50, 60, 70, 80, 100, 110, 120, 70, 50])
    kind = r.randint(0, 2)
    if kind == 0:
        return Q(f'Two tangents PA and PB are drawn to a circle with centre O from an external point P. If ∠APB = {t}°, find ∠AOB.', f'{180 - t}°',
                 f'∠OAP = ∠OBP = 90°, so in quadrilateral OAPB, ∠AOB = 360° − 90° − 90° − {t}° = {180 - t}°.', num_distractors(180 - t, t, 90 - t // 2, 360 - t))
    if kind == 1:
        return Q(f'From an external point P, tangents PA and PB are drawn to a circle with centre O. If ∠AOB = {180 - t}°, find ∠OPA.', f'{t // 2}°',
                 f'∠APB = 180° − {180 - t}° = {t}°; OP bisects ∠APB ⇒ ∠OPA = {t // 2}°.', num_distractors(t // 2, t, 90 - t // 2, 180 - t))
    return Q(f'PA and PB are tangents from P to a circle with centre O. If ∠APB = {t}°, find ∠PAB.', f'{(180 - t) // 2}°' if t % 2 == 0 else f'{fn(Fr(180 - t, 2))}°',
             f'PA = PB, so △PAB is isosceles: ∠PAB = (180° − {t}°)/2 = {fn(Fr(180 - t, 2))}°.', num_distractors(float(Fr(180 - t, 2)), t, 180 - t, t / 2))


def c10s2_equal(r):
    t = r.randint(4, 15)
    a, b = r.randint(2, 9), r.randint(2, 9)
    return Q(f'PA and PB are tangents from an external point P to a circle. If PA = {a}x + {b} and PB = {a + 1}x − {t} (in cm), find x and PA.', f'x = {b + t}; PA = {a * (b + t) + b} cm',
             f'Tangents from an external point are equal: {a}x + {b} = {a + 1}x − {t} ⇒ x = {b + t}; PA = {a * (b + t) + b} cm (3 marks).')


def c10s2_quad(r):
    a, b, c = r.randint(4, 15), r.randint(4, 15), r.randint(4, 15)
    d = a + c - b
    if d <= 2:
        raise ValueError
    sides = {'AB': a, 'BC': b, 'CD': c, 'DA': d}
    ask = r.choice(list(sides))
    giv = ', '.join(f'{k} = {v} cm' for k, v in sides.items() if k != ask)
    return Q(f'A quadrilateral ABCD is drawn to circumscribe a circle. If {giv}, find {ask}.', f'{sides[ask]} cm',
             f'Tangent lengths from each vertex are equal, so AB + CD = AD + BC. Solve: {ask} = {sides[ask]} cm (3 marks).',
             num_distractors(sides[ask], sides[ask] + 2, (a + b + c) // 3, abs(sides[ask] - 3) or 1))


def c10s2_perim(r):
    t = r.randint(6, 20)
    return Q(f'From an external point P, two tangents PA and PB of length {t} cm are drawn to a circle. A third tangent touches the circle at a point R on the minor arc AB and meets PA at Q and PB at S. Find the perimeter of △PQS.', f'{2 * t} cm',
             f'QA = QR and SB = SR, so PQ + QS + SP = PQ + QA + SB + SP = PA + PB = {2 * t} cm (3 marks).', num_distractors(2 * t, t, 3 * t, t + 4))


def c10s2_mcq(r):
    return mcqbank([
        ('The number of tangents that can be drawn to a circle from a point outside it is …', '2', ['1', '0', 'infinitely many'], 'Theorem.'),
        ('The lengths of tangents drawn from an external point to a circle are …', 'equal', ['unequal', 'in the ratio 1 : 2', 'equal to the radius'], 'Theorem 10.2.'),
        ('From a point on the circle, the number of tangents is …', '1', ['2', '0', 'infinitely many'], 'Exactly one tangent at that point.'),
        ('If PA and PB are tangents from P to a circle with centre O, then OP …', 'bisects ∠APB', ['is perpendicular to PA', 'is equal to PA', 'bisects AB at right angles only when ∠APB = 90°'], 'Congruent triangles OAP and OBP.'),
        ('If two tangents inclined at 60° are drawn from P to a circle of radius 3 cm, each tangent has length …', '3√3 cm', ['3 cm', '6 cm', '√3 cm'], 'tan 30° = 3/PA.'),
    ])(r)


def c10s2_prove(r):
    return xbank([
        ('Prove that the lengths of tangents drawn from an external point to a circle are equal.',
         'Join OA, OB, OP. In right △OAP and △OBP: OA = OB (radii), OP common, ∠OAP = ∠OBP = 90°; by RHS they are congruent, so PA = PB.', 'Figure (1), right angles (1), RHS (2), conclusion (1).'),
        ('Prove that the angle between the two tangents drawn from an external point to a circle is supplementary to the angle subtended by the line segment joining the points of contact at the centre.',
         'In quadrilateral OAPB, ∠OAP = ∠OBP = 90°; the angle sum is 360°, so ∠APB + ∠AOB = 180°.', '3 marks.'),
        ('Two tangents TP and TQ are drawn to a circle with centre O from an external point T. Prove that ∠PTQ = 2∠OPQ.',
         'TP = TQ ⇒ ∠TPQ = ∠TQP = (180° − ∠PTQ)/2. ∠OPQ = 90° − ∠TPQ = ∠PTQ/2.', '3 marks.'),
        ('Prove that a parallelogram circumscribing a circle is a rhombus.',
         'Equal tangents give AB + CD = AD + BC; with AB = CD and AD = BC this gives 2AB = 2AD, so all sides are equal.', '3 marks.'),
    ])(r)


def c10s2_ar(r):
    t = r.randint(5, 15)
    return arbank([
        (f'If PA and PB are tangents from P with PA = {t} cm, then PB = {t} cm.', 'The lengths of tangents from an external point to a circle are equal.', 'a', 'R explains A.'),
        ('If two tangents from P make an angle of 80°, then ∠AOB = 100°.', 'The angle between the tangents and the angle at the centre are supplementary.', 'a', 'R explains A.'),
        ('A parallelogram circumscribing a circle is a rectangle.', 'In a quadrilateral circumscribing a circle, the sums of opposite sides are equal.', 'd', 'It is a rhombus; A false, R true.'),
        ('From an external point, exactly two tangents can be drawn to a circle.', 'A tangent is perpendicular to the radius at the point of contact.', 'b', 'Both true; R does not explain A.'),
    ])(r)


def c10s2_explain(r):
    return xbank([
        ('Explain why the centre of a circle lies on the bisector of the angle between two tangents from an external point.', '△OAP ≅ △OBP (RHS), so ∠OPA = ∠OPB.', '2 marks.'),
        ('Explain why AB + CD = AD + BC for a quadrilateral ABCD circumscribing a circle.', 'Each side is split into two tangent segments; equal tangents from each vertex pair up on both sides.', '2 marks.'),
    ])(r)


def c10s2_case(r):
    rr = r.choice([3, 4, 5, 6, 7])
    t = r.choice([60, 90, 120])
    PA = {60: f'{rr}√3 cm', 90: f'{rr} cm', 120: f'{rr}√3/3 cm' if rr % 3 else f'{rr // 3}√3 cm'}[t]
    return Q((f'A circular wheel of radius {rr} cm rests against two straight rods PA and PB that touch it at A and B and meet at P, with ∠APB = {t}°. '
              f'(i) Why are PA and PB equal? (ii) Find ∠AOB. (iii) Find ∠OPA. (iv) Find the length PA.'),
             f'(i) tangents from an external point are equal (ii) {180 - t}° (iii) {t // 2}° (iv) {PA}', '1 mark each part.')


# st3 polygons and concentric circles

def c10s3_concentric(r):
    a, b, c = triple(r)
    k = r.choice([1, 1, 2])
    R, rr, half = c * k, a * k, b * k
    if r.random() < 0.6:
        return Q(f'Two concentric circles have radii {R} cm and {rr} cm. Find the length of the chord of the larger circle which touches the smaller circle.', f'{2 * half} cm',
                 f'The chord is tangent to the smaller circle, so the radius {rr} is perpendicular to it and bisects it: half-chord = √({R}² − {rr}²) = {half}; chord = {2 * half} cm (3 marks).',
                 num_distractors(2 * half, half, R - rr, R + rr))
    return Q(f'A chord of length {2 * half} cm of the larger of two concentric circles touches the smaller circle. If the larger radius is {R} cm, find the smaller radius.', f'{rr} cm',
             f'Half-chord = {half}; r = √({R}² − {half}²) = {rr} cm.', num_distractors(rr, R - half, half, R - 2))


def c10s3_triangle(r):
    while True:
        x, y, z = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
        if len({x, y, z}) >= 2:
            break
    AB, BC, CA = x + y, y + z, z + x
    ask = r.choice([('AF (tangent length from A)', x), ('BD (tangent length from B)', y), ('CE (tangent length from C)', z)])
    return Q(f'A circle is inscribed in △ABC, touching BC at D, CA at E and AB at F. If AB = {AB} cm, BC = {BC} cm and CA = {CA} cm, find {ask[0]}.', f'{ask[1]} cm',
             f'Let AF = AE = x, BF = BD = y, CD = CE = z. x + y = {AB}, y + z = {BC}, z + x = {CA}; x + y + z = {x + y + z}; so x = {x}, y = {y}, z = {z} (3 marks).',
             num_distractors(ask[1], (AB + BC + CA) / 3, AB - ask[1], ask[1] + 1))


def c10s3_inradius(r):
    a, b, c = triple(r)
    k = r.choice([1, 1, 2])
    a, b, c = a * k, b * k, c * k
    return Q(f'A circle is inscribed in a right triangle with legs {a} cm and {b} cm. Find its radius.', f'{(a + b - c) // 2} cm' if (a + b - c) % 2 == 0 else f'{fn(Fr(a + b - c, 2))} cm',
             f'Hypotenuse = {c} cm. Tangents from the right-angle vertex equal r, so (a − r) + (b − r) = c ⇒ r = (a + b − c)/2 = {fn(Fr(a + b - c, 2))} cm (3 marks).',
             num_distractors(float(Fr(a + b - c, 2)), (a + b + c) / 2, c / 2, a * b / c))


def c10s3_mcq(r):
    return mcqbank([
        ('A quadrilateral ABCD circumscribes a circle. Then …', 'AB + CD = BC + DA', ['AB + BC = CD + DA', 'AB = CD and BC = DA always', 'AC = BD'], 'Equal tangent lengths.'),
        ('A parallelogram that circumscribes a circle must be a …', 'rhombus', ['rectangle', 'trapezium', 'kite that is not a rhombus'], 'Using AB + CD = AD + BC.'),
        ('In two concentric circles, a chord of the larger circle that touches the smaller circle is … at the point of contact.', 'bisected', ['trisected', 'divided in the ratio 1 : 2', 'not divided equally'], 'The perpendicular from the centre bisects the chord.'),
        ('Two concentric circles have radii 5 cm and 3 cm. The length of the chord of the larger circle touching the smaller one is …', '8 cm', ['4 cm', '6 cm', '10 cm'], '2√(25 − 9).'),
    ])(r)


def c10s3_ar(r):
    return arbank([
        ('A chord of the larger of two concentric circles that touches the smaller circle is bisected at the point of contact.', 'The perpendicular from the centre to a chord bisects the chord.', 'a', 'The radius to the point of contact is that perpendicular.'),
        ('If a circle is inscribed in a triangle, the tangent segments from each vertex are equal.', 'Tangents from an external point to a circle are equal.', 'a', 'R explains A.'),
        ('A rectangle that is not a square can circumscribe a circle.', 'In a quadrilateral circumscribing a circle, AB + CD = AD + BC.', 'd', 'Then 2AB = 2BC, forcing a square; A false, R true.'),
    ])(r)


def c10s3_explain(r):
    return xbank([
        ('Explain why the opposite sides of a quadrilateral circumscribing a circle subtend supplementary angles at the centre.', 'The centre joins to the vertices and points of contact form 8 angles in 4 equal pairs; opposite-side angles add to half of 360°.', '3 marks.'),
        ('Explain why the sum of the tangent segments from the three vertices of a triangle equals its semi-perimeter.', 'Each side is the sum of two tangent segments; adding all three sides counts each segment twice.', '2 marks.'),
    ])(r)


def c10s3_case(r):
    a, b, c = triple(r)
    k = r.choice([1, 2])
    R, rr, half = c * k, a * k, b * k
    return Q((f'A circular running track has two concentric boundaries of radii {R} m (outer) and {rr} m (inner). A straight cable is laid across the outer boundary so that it just touches the inner boundary at P. '
              f'(i) What angle does the radius OP make with the cable? (ii) Find half the length of the cable. (iii) Find the full length of the cable. (iv) Find the width of the track.'),
             f'(i) 90° (ii) {half} m (iii) {2 * half} m (iv) {R - rr} m', '1 mark each part.')


FAMILIES = {
    S + '06-st1': [F('C1', 'D1', 'mcq', c6s1_mcq), F('C1', 'D2', 'mcq', c6s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c6s1_explain), F('C3', 'D2', 'numerical', c6s1_scale),
                   F('C3', 'D3', 'short', c6s1_rect), F('C3', 'D2', 'numerical', c6s1_map), F('C4', 'D3', 'case', c6s1_case), F('C2', 'D3', 'short', c6s1_rect)],
    S + '06-st2': [F('C1', 'D2', 'mcq', c6s2_mcq), F('C2', 'D2', 'mcq', c6s2_ar, kinds=('ar',)), F('C2', 'D3', 'long', c6s2_prove), F('C3', 'D1', 'numerical', c6s2_find),
                   F('C3', 'D2', 'numerical', c6s2_whole), F('C3', 'D3', 'numerical', c6s2_alg), F('C3', 'D3', 'short', c6s2_converse), F('C3', 'D4', 'multi_step', c6s2_trap),
                   F('C4', 'D4', 'multi_step', c6s2_trap_alg), F('C4', 'D3', 'case', c6s2_case), F('C4', 'D5', 'long', c6s2_trap_alg)],
    S + '06-st3': [F('C1', 'D2', 'mcq', c6s3_which), F('C2', 'D2', 'mcq', c6s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c6s3_explain), F('C3', 'D1', 'short', c6s3_angle),
                   F('C3', 'D2', 'short', c6s3_sss), F('C3', 'D3', 'short', c6s3_sas), F('C3', 'D4', 'multi_step', c6s3_prove), F('C4', 'D3', 'case', c6s3_case)],
    S + '06-st4': [F('C1', 'D2', 'mcq', c6s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c6s4_explain), F('C3', 'D1', 'numerical', c6s4_sides), F('C3', 'D2', 'numerical', c6s4_shadow),
                   F('C3', 'D3', 'numerical', c6s4_perim), F('C3', 'D3', 'multi_step', c6s4_altitude), F('C4', 'D4', 'multi_step', c6s4_lamp, gap='G7'), F('C4', 'D3', 'case', c6s4_case, gap='G7'),
                   F('C2', 'D2', 'numerical', c6s4_shadow)],
    S + '07-st1': [F('C1', 'D1', 'mcq', c7s1_mcq), F('C2', 'D2', 'mcq', c7s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c7s1_explain), F('C3', 'D1', 'numerical', g9a.c1s2_dist),
                   F('C3', 'D2', 'numerical', g9a.c1s2_dist_surd), F('C3', 'D3', 'numerical', g9a.c1s2_find_k), F('C3', 'D3', 'multi_step', c7s1_collinear), F('C3', 'D4', 'multi_step', g9a.c1s2_equidistant),
                   F('C4', 'D4', 'multi_step', c7s1_yaxis), F('C4', 'D5', 'long', c7s1_relation), F('C4', 'D3', 'case', c7s1_case)],
    S + '07-st2': [F('C1', 'D2', 'mcq', c7s2_mcq), F('C2', 'D2', 'mcq', c7s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c7s2_explain), F('C3', 'D1', 'numerical', c7s2_find),
                   F('C3', 'D2', 'numerical', c7s2_find), F('C3', 'D3', 'numerical', c7s2_endpoint), F('C4', 'D4', 'multi_step', c7s2_endpoint), F('C4', 'D3', 'case', c7s2_case)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c7s3_explain), F('C3', 'D1', 'numerical', g9a.c1s3_other_end), F('C3', 'D2', 'numerical', c7s3_trisect),
                   F('C3', 'D3', 'numerical', c7s3_ratio), F('C3', 'D3', 'numerical', c7s3_k), F('C3', 'D4', 'multi_step', c7s3_axis), F('C4', 'D4', 'long', c7s3_four), F('C4', 'D3', 'case', c7s3_case),
                   F('C2', 'D2', 'numerical', c7s3_k)],
    S + '07-st4': [F('C1', 'D2', 'mcq', c7s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c7s4_explain), F('C3', 'D2', 'short', c7s4_tri), F('C3', 'D3', 'multi_step', c7s4_tri),
                   F('C3', 'D3', 'numerical', c7s4_fourth), F('C3', 'D4', 'long', c7s4_quad), F('C4', 'D4', 'long', g9a.c1s2_right_tri), F('C4', 'D3', 'case', c7s4_case), F('C4', 'D5', 'long', c7s4_quad)],
    S + '08-st1': [F('C1', 'D1', 'mcq', c8s1_mcq), F('C2', 'D2', 'mcq', c8s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c8s1_explain), F('C3', 'D1', 'short', c8s1_find),
                   F('C3', 'D2', 'short', c8s1_find), F('C3', 'D3', 'multi_step', c8s1_others), F('C3', 'D4', 'multi_step', c8s1_verify), F('C4', 'D3', 'case', c8s1_case), F('C4', 'D4', 'multi_step', c8s1_verify)],
    S + '08-st2': [F('C1', 'D1', 'mcq', c8s2_mcq), F('C1', 'D2', 'mcq', c8s2_check), F('C2', 'D2', 'mcq', c8s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c8s2_eval),
                   F('C3', 'D3', 'numerical', c8s2_eval), F('C3', 'D3', 'explain', c8s2_identity), F('C3', 'D4', 'multi_step', c8s2_solve), F('C4', 'D3', 'case', c8s2_case)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_mcq), F('C2', 'D2', 'mcq', c8s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c8s3_explain), F('C3', 'D2', 'multi_step', c8s3_given),
                   F('C3', 'D3', 'numerical', c8s3_value), F('C3', 'D3', 'explain', c8s3_express), F('C4', 'D4', 'long', c8s3_given), F('C4', 'D3', 'case', c8s3_case)],
    S + '08-st4': [F('C1', 'D2', 'mcq', c8s4_mcq), F('C1', 'D1', 'mcq', c8s4_num), F('C2', 'D2', 'mcq', c8s4_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c8s4_explain),
                   F('C3', 'D3', 'multi_step', c8s4_prove), F('C3', 'D3', 'numerical', c8s4_sectan), F('C3', 'D4', 'long', c8s4_prove), F('C4', 'D4', 'multi_step', c8s4_sectan),
                   F('C4', 'D5', 'long', c8s4_prove), F('C4', 'D3', 'case', c8s4_case)],
    S + '09-st1': [F('C1', 'D1', 'mcq', c9s1_mcq), F('C2', 'D2', 'mcq', c9s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c9s1_explain), F('C3', 'D2', 'short', c9s1_shadow),
                   F('C3', 'D3', 'numerical', c9s2_distance), F('C4', 'D3', 'case', c9s1_case, gap='G7'), F('C1', 'D2', 'short', c9s1_shadow), F('C3', 'D1', 'numerical', c9s2_height)],
    S + '09-st2': [F('C1', 'D2', 'mcq', c9s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c9s2_explain), F('C3', 'D1', 'numerical', c9s2_height), F('C3', 'D2', 'numerical', c9s2_distance),
                   F('C3', 'D2', 'numerical', c9s2_kite), F('C3', 'D3', 'numerical', c9s2_string), F('C3', 'D4', 'multi_step', c9s2_broken, gap='G7'), F('C4', 'D3', 'case', c9s2_case, gap='G7'),
                   F('C4', 'D4', 'long', c9s2_broken, gap='G7'), F('C2', 'D3', 'numerical', c9s2_height), F('C3', 'D3', 'multi_step', c9s2_distance)],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c9s3_explain), F('C3', 'D3', 'multi_step', c9s3_comp), F('C3', 'D3', 'multi_step', c9s3_two_depr),
                   F('C3', 'D4', 'long', c9s3_same_side, gap='G7'), F('C4', 'D4', 'long', c9s3_opposite, gap='G7'), F('C4', 'D4', 'long', c9s3_building, gap='G7'), F('C4', 'D5', 'long', c9s3_flag, gap='G7'),
                   F('C4', 'D3', 'case', c9s3_case, gap='G7'), F('C3', 'D2', 'numerical', c9s3_comp), F('C4', 'D3', 'multi_step', c9s3_flag, gap='G7')],
    S + '10-st1': [F('C1', 'D1', 'mcq', c10s1_mcq), F('C2', 'D2', 'mcq', c10s1_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c10s1_explain), F('C3', 'D1', 'numerical', c10s1_tangent_len),
                   F('C3', 'D2', 'numerical', c10s1_tangent_len), F('C3', 'D2', 'short', c10s1_angle), F('C3', 'D3', 'long', c10s1_prove), F('C4', 'D3', 'case', c10s1_case),
                   F('C4', 'D4', 'long', c10s1_prove), F('C2', 'D3', 'numerical', c10s1_angle)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_mcq), F('C2', 'D2', 'mcq', c10s2_ar, kinds=('ar',)), F('C2', 'D2', 'explain', c10s2_explain), F('C3', 'D1', 'numerical', c10s2_angle),
                   F('C3', 'D2', 'numerical', c10s2_angle), F('C3', 'D3', 'numerical', c10s2_equal), F('C3', 'D3', 'multi_step', c10s2_quad), F('C3', 'D4', 'multi_step', c10s2_perim),
                   F('C4', 'D4', 'long', c10s2_prove), F('C4', 'D3', 'case', c10s2_case), F('C4', 'D5', 'long', c10s2_prove)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_mcq), F('C2', 'D2', 'mcq', c10s3_ar, kinds=('ar',)), F('C2', 'D3', 'explain', c10s3_explain), F('C3', 'D2', 'numerical', c10s3_concentric),
                   F('C3', 'D3', 'numerical', c10s3_triangle), F('C3', 'D3', 'multi_step', c10s3_inradius), F('C3', 'D4', 'multi_step', c10s3_triangle), F('C4', 'D4', 'multi_step', c10s2_quad),
                   F('C4', 'D3', 'case', c10s3_case), F('C3', 'D1', 'numerical', c10s3_concentric), F('C4', 'D5', 'long', c10s3_inradius)],
}
