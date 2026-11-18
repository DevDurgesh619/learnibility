"""CBSE class 12 maths (NCERT Mathematics XII, 041) families, chapters 10-13 (vectors, 3D geometry, LPP, probability)."""
from __future__ import annotations

import itertools
import math
from fractions import Fraction as Fr

from qbank import F, mcq, ar, num, name, two_names, inr, num_distractors, CITIES
from g12_maths_h import (Q, mcqbank, arbank, xbank, fn, fz, fpar, poly, term, dist3, vstr, dot, cross, sq, surd, gcdl, prim,
                         lpp_vertices, cons_str)

S = 'cbse-g12-maths-ch'
QUADS = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (1, 12, 12, 17), (8, 9, 12, 17), (2, 5, 14, 15), (4, 8, 1, 9)]


def qvec(r):
    a, b, c, n = r.choice(QUADS)
    v = [a, b, c]
    r.shuffle(v)
    v = [x * r.choice([1, -1]) for x in v]
    return v, n


def rvec(r, lo=-5, hi=6, nz=True):
    while True:
        v = [r.randint(lo, hi - 1) for _ in range(3)]
        if not nz or any(v):
            return v


def P3(p):
    return '(' + ', '.join(fz(x) for x in p) + ')'


def unit_txt(v):
    n2 = sq(v)
    sn = surd(n2)
    sn = f'({sn})' if ('√' in sn and not sn.startswith('√')) else sn
    return f'(1/{sn})({vstr(v)})' if sn != '1' else vstr(v)


# ======================================================================= ch10 Vector Algebra

def c10s1_mag(r):
    v, n = qvec(r)
    kind = r.randint(0, 2)
    if kind == 0:
        return Q(f'Find the magnitude of the vector a⃗ = {vstr(v)}.', str(n), '|a⃗| = √(' + ' + '.join(f'({fz(x)})²' if x < 0 else f'{x}²' for x in v) + f') = √{n * n} = {n}.',
                 num_distractors(n, sum(abs(x) for x in v), n * n, n + 1))
    if kind == 1:
        ans = ', '.join(fz(Fr(x, n)) for x in v)
        return Q(f'Find the unit vector in the direction of a⃗ = {vstr(v)}.', f'(1/{n})({vstr(v)})', f'â = a⃗/|a⃗| with |a⃗| = {n}.',
                 [f'{vstr(v)}', f'(1/{n * n})({vstr(v)})', f'(1/{sum(abs(x) for x in v)})({vstr(v)})'])
    k = r.choice([2, 3, 5, 7, 10, 14])
    w = [Fr(k * x, n) for x in v]
    return Q(f'Find a vector in the direction of {vstr(v)} which has magnitude {k} units.', vstr(w), f'{k}â = ({k}/{n})({vstr(v)}) = {vstr(w)}.',
             [vstr([k * x for x in v]), vstr([Fr(x, n) for x in v]), vstr([Fr(k * x, n * n) for x in v])])


def c10s1_dc(r):
    v, n = qvec(r)
    ans = ', '.join(fz(Fr(x, n)) for x in v)
    return Q(f'Find the direction cosines of the vector {vstr(v)}.', ans, f'Divide each component by |a⃗| = {n}.',
             [', '.join(str(x) for x in v), ', '.join(fz(Fr(x, n * n)) for x in v), ', '.join(fz(Fr(-x, n)) for x in v)])


def c10s1_mcq(r):
    return mcqbank([
        ('A vector whose initial and terminal points coincide is called …', 'a zero vector', ['a unit vector', 'a collinear vector', 'an equal vector'], 'Definition.'),
        ('Two or more vectors having the same initial point are called …', 'coinitial vectors', ['collinear vectors', 'equal vectors', 'unit vectors'], 'Definition.'),
        ('Vectors that are parallel to the same line, irrespective of their magnitudes and directions, are called …', 'collinear vectors', ['coinitial vectors', 'equal vectors', 'negative vectors'], 'Definition.'),
        ('A vector whose magnitude is unity is called …', 'a unit vector', ['a zero vector', 'a position vector', 'a free vector'], 'Definition.'),
        ('If l, m, n are the direction cosines of a vector, then l² + m² + n² = …', '1', ['0', '3', '−1'], 'Standard identity.'),
        ('The direction cosines of a vector making equal angles with the three axes are …', '±(1/√3, 1/√3, 1/√3)', ['(1, 1, 1)', '(1/3, 1/3, 1/3)', '(1/√2, 1/√2, 0)'], '3l² = 1.'),
        ('Two vectors are equal if …', 'they have the same magnitude and direction', ['they have the same magnitude', 'they are collinear', 'they have the same initial point'], 'Definition.'),
    ])(r)


def c10s1_ar(r):
    v, n = qvec(r)
    return arbank([
        (f'The vector (1/{n})({vstr(v)}) is a unit vector.', f'|{vstr(v)}| = {n}.', 'a', 'Dividing by the magnitude gives magnitude 1.'),
        (f'{vstr(v)} is a unit vector.', 'A unit vector has magnitude 1.', 'd', f'Its magnitude is {n}; A false, R true.'),
        ('A vector cannot have direction cosines (1/2, 1/2, 1/2).', 'The sum of squares of direction cosines is 1.', 'a', '1/4 + 1/4 + 1/4 = 3/4 ≠ 1.'),
        ('The zero vector has no definite direction.', 'The zero vector has magnitude 0.', 'b', 'Both true; R does not explain why its direction is arbitrary.'),
    ])(r)


def c10s1_case(r):
    v, n = qvec(r)
    v = [abs(x) for x in v]
    who = name(r)
    return Q((f'A drone flown by {who} at a school event in {r.choice(CITIES)} moves from the launch pad O to a point A with displacement OA⃗ = {vstr(v)} (in metres; î east, ĵ north, k̂ up). '
              f'(i) How far is the drone from O? (ii) Find the unit vector along OA⃗. (iii) Find the direction cosines of OA⃗ and the cosine of the angle it makes with the vertical.'),
             f'(i) {n} m (ii) (1/{n})({vstr(v)}) (iii) {", ".join(fz(Fr(x, n)) for x in v)}; cos γ = {fz(Fr(v[2], n))}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c10s1_explain(r):
    return xbank([
        ('Explain why the vectors 2î + 3ĵ and 4î + 6ĵ are collinear but not equal.', '4î + 6ĵ = 2(2î + 3ĵ).', 'Parallel (scalar multiple) but magnitudes differ (2 marks).'),
        ('Explain the difference between a scalar and a vector, with one example of each.', 'A scalar has magnitude only (mass, 5 kg); a vector has magnitude and direction (velocity, 20 m/s north).', '1 mark each.'),
        ('Can a vector have direction angles 45°, 60° and 120°? Explain.', 'Yes.', 'cos²45° + cos²60° + cos²120° = 1/2 + 1/4 + 1/4 = 1 (2 marks).'),
        ('Can a vector have direction angles 45°, 45° and 60°? Explain.', 'No.', 'cos²45° + cos²45° + cos²60° = 1/2 + 1/2 + 1/4 ≠ 1 (2 marks).'),
    ])(r)


# ---- st2 addition, components, section formula

def c10s2_join(r):
    P, Qp = rvec(r, -6, 8), rvec(r, -6, 8)
    d = [b - a for a, b in zip(P, Qp)]
    if not any(d):
        raise ValueError
    return Q(f'Find the vector joining the points P{P3(P)} and Q{P3(Qp)} directed from P to Q, and its magnitude.', f'PQ⃗ = {vstr(d)}, |PQ⃗| = {surd(sq(d))}',
             f'PQ⃗ = OQ⃗ − OP⃗ = {vstr(d)}; |PQ⃗| = √{sq(d)} = {surd(sq(d))}.', [f'PQ⃗ = {vstr([-x for x in d])}, |PQ⃗| = {surd(sq(d))}', f'PQ⃗ = {vstr([a + b for a, b in zip(P, Qp)])}, |PQ⃗| = {surd(sq([a + b for a, b in zip(P, Qp)]))}',
                                                                                  f'PQ⃗ = {vstr(d)}, |PQ⃗| = {sum(abs(x) for x in d)}'])


def c10s2_section(r):
    A, B = rvec(r, -6, 7), rvec(r, -6, 7)
    m, n = r.sample([1, 2, 3, 4], 2)
    ext = r.random() < 0.4
    if ext:
        Pt = [Fr(m * b - n * a, m - n) for a, b in zip(A, B)]
        how = 'externally'
    else:
        Pt = [Fr(m * b + n * a, m + n) for a, b in zip(A, B)]
        how = 'internally'
    other = [Fr(m * a + n * b, m + n) for a, b in zip(A, B)]
    return Q(f'Find the position vector of the point R which divides the line joining P({vstr(A)}) and Q({vstr(B)}) {how} in the ratio {m} : {n}.', vstr(Pt),
             f'r⃗ = ({m}q⃗ {"−" if ext else "+"} {n}p⃗)/({m} {"−" if ext else "+"} {n}) = {vstr(Pt)}.',
             dist3(vstr(Pt), [vstr(other), vstr([Fr(m * b - n * a, m - n) for a, b in zip(A, B)] if not ext else [Fr(m * b + n * a, m + n) for a, b in zip(A, B)]), vstr([Fr(a + b, 2) for a, b in zip(A, B)])]))


def c10s2_sum(r):
    a, b = rvec(r), rvec(r)
    p, q = r.choice([1, 2, 3]), r.choice([1, -1, 2, -2, 3])
    s = [p * x + q * y for x, y in zip(a, b)]
    if not any(s):
        raise ValueError
    expr = f'{"" if p == 1 else p}a⃗ {"+" if q > 0 else "−"} {"" if abs(q) == 1 else abs(q)}b⃗'
    return Q(f'If a⃗ = {vstr(a)} and b⃗ = {vstr(b)}, find {expr} and the unit vector in its direction.', f'{vstr(s)}; unit vector {unit_txt(s)}',
             f'{expr} = {vstr(s)}; magnitude √{sq(s)} = {surd(sq(s))} (1 mark each).',
             [f'{vstr([p * x - q * y for x, y in zip(a, b)])}; unit vector {unit_txt([p * x - q * y for x, y in zip(a, b)]) if any(p * x - q * y for x, y in zip(a, b)) else "0⃗"}', f'{vstr(s)}; unit vector {vstr(s)}', f'{vstr([x + y for x, y in zip(a, b)])}; unit vector {unit_txt([x + y for x, y in zip(a, b)]) if any(x + y for x, y in zip(a, b)) else "0⃗"}'])


def c10s2_col(r):
    A = rvec(r, -4, 5, False)
    d = rvec(r, -3, 4)
    t1, t2 = r.sample([-2, -1, 2, 3], 2)
    B = [a + t1 * x for a, x in zip(A, d)]
    C = [a + t2 * x for a, x in zip(A, d)]
    k = Fr(t2, t1)
    return Q(f'Show that the points A({vstr(A) if any(A) else "0⃗"}), B({vstr(B)}) and C({vstr(C)}) are collinear.', f'AC⃗ = ({fz(k)})AB⃗, so A, B, C are collinear',
             f'AB⃗ = {vstr([t1 * x for x in d])}, AC⃗ = {vstr([t2 * x for x in d])} (1 mark); AC⃗ = ({fz(k)})AB⃗ with common point A (1 mark).',
             ['They form a triangle', f'AB⃗ = AC⃗', 'They are collinear only if A is the origin'])


def c10s2_equal(r):
    x, y, z = r.randint(-5, 6), r.randint(-5, 6), r.randint(-5, 6)
    p, q = r.randint(1, 4), r.randint(-4, 4)
    return Q(f'Find the values of x, y and z so that the vectors a⃗ = {p}xî + (y {"+" if q >= 0 else "−"} {abs(q)})ĵ + zk̂ and b⃗ = {vstr([p * x, y + q, z]) if any([p * x, y + q, z]) else "0⃗"} are equal.'.replace('1xî', 'xî'),
             f'x = {x}, y = {y}, z = {z}', 'Equal vectors have equal corresponding components.', [f'x = {p * x}, y = {y + q}, z = {z}', f'x = {x}, y = {y + 2 * q}, z = {z}', f'x = {-x}, y = {-y}, z = {-z}' if (x or y or z) else 'x = 1, y = 1, z = 1'])


def c10s2_mcq(r):
    return mcqbank([
        ('If a⃗ and b⃗ are position vectors of A and B, the position vector of the midpoint of AB is …', '(a⃗ + b⃗)/2', ['(a⃗ − b⃗)/2', 'a⃗ + b⃗', '(b⃗ − a⃗)/2'], 'Section formula with ratio 1 : 1.'),
        ('For points A and B with position vectors a⃗ and b⃗, AB⃗ = …', 'b⃗ − a⃗', ['a⃗ − b⃗', 'a⃗ + b⃗', '(a⃗ + b⃗)/2'], 'Head minus tail.'),
        ('In triangle ABC, AB⃗ + BC⃗ + CA⃗ = …', '0⃗', ['2AC⃗', 'AC⃗', '3AB⃗'], 'Triangle law: closed path.'),
        ('Vector addition is …', 'commutative and associative', ['commutative but not associative', 'associative but not commutative', 'neither commutative nor associative'], 'Properties of vector addition.'),
        ('If a⃗ = λb⃗ for a scalar λ, then a⃗ and b⃗ are …', 'collinear', ['perpendicular', 'equal', 'coinitial'], 'Scalar multiples are parallel.'),
        ('The position vector of the point dividing a⃗ and b⃗ internally in the ratio m : n is …', '(mb⃗ + na⃗)/(m + n)', ['(ma⃗ + nb⃗)/(m + n)', '(mb⃗ − na⃗)/(m − n)', '(a⃗ + b⃗)/2'], 'Section formula.'),
    ])(r)


def c10s2_ar(r):
    a = rvec(r)
    k = r.choice([2, 3, -2, 4])
    return arbank([
        (f'The vectors {vstr(a)} and {vstr([k * x for x in a])} are collinear.', f'{vstr([k * x for x in a])} = {k}({vstr(a)}).', 'a', 'Scalar multiple ⇒ collinear.'),
        ('In any triangle ABC, AB⃗ + BC⃗ = AC⃗.', 'Vector addition follows the triangle law.', 'a', 'R is the triangle law.'),
        (f'The vectors {vstr(a)} and {vstr([a[0] + 1, a[1], a[2]])} are collinear.', 'Two vectors are collinear if one is a scalar multiple of the other.', 'd', 'No scalar works; A false, R true.'),
        ('The midpoint of AB has position vector (a⃗ + b⃗)/2.', 'Vector addition is commutative.', 'b', 'Both true; the midpoint comes from the section formula.'),
    ])(r)


def c10s2_case(r):
    A, B = rvec(r, 0, 9, False), rvec(r, 0, 9, False)
    m, n = r.sample([1, 2, 3], 2)
    R = [Fr(m * b + n * a, m + n) for a, b in zip(A, B)]
    d = [b - a for a, b in zip(A, B)]
    if not any(d):
        raise ValueError
    who = name(r)
    return Q((f'In a 3D model of a bridge made by {who}, two pillars stand at A{P3(A)} and B{P3(B)} (metres). A lamp is to be fixed at R on AB with AR : RB = {m} : {n}. '
              f'(i) Find AB⃗. (ii) Find the length AB. (iii) Find the position vector of R.'),
             f'(i) {vstr(d)} (ii) {surd(sq(d))} m (iii) {vstr(R)}', '(i) 1 mark (ii) 1 mark (iii) section formula (2 marks).')


# ---- st3 dot product and projection

def c10s3_angle(r):
    a, na = qvec(r)
    b, nb = qvec(r)
    d = dot(a, b)
    c = Fr(d, na * nb)
    nice = {Fr(0): 'π/2', Fr(1): '0', Fr(-1): 'π'}
    ans = nice.get(c, f'cos⁻¹({fz(c)})')
    return Q(f'Find the angle between the vectors {vstr(a)} and {vstr(b)}.', ans, f'cos θ = a⃗·b⃗/(|a⃗||b⃗|) = {fz(d)}/({na} × {nb}) = {fz(c)}.',
             dist3(ans, [f'cos⁻¹({fz(-c)})' if c else 'π/4', f'cos⁻¹({fz(Fr(d, na * na + nb * nb))})' if d else 'π/3', f'sin⁻¹({fz(c)})' if c else 'π', f'cos⁻¹({fz(Fr(d + 1, na * nb))})']))


def c10s3_perp(r):
    while True:
        a = rvec(r)
        b = rvec(r)
        j = r.randint(0, 2)
        if b[j] == 0 or any(a[i] == 0 for i in range(3) if i != j):
            continue
        rest = sum(a[i] * b[i] for i in range(3) if i != j)
        lam = Fr(-rest, b[j])
        if lam.denominator <= 2:
            break
    comps = [fz(x) for x in a]
    comps[j] = 'λ'
    av = ' + '.join((c + e) if c not in ('1', '−1') and not c.startswith('−') else ('' if c == '1' else '−' if c == '−1' else c) + e for c, e in zip(comps, ['î', 'ĵ', 'k̂'])).replace('+ −', '− ')
    return Q(f'Find λ if the vectors {av} and {vstr(b)} are perpendicular.', f'λ = {fz(lam)}', f'a⃗·b⃗ = 0 ⇒ {fz(rest)} + {fz(b[j])}λ = 0 ⇒ λ = {fz(lam)}.',
             dist3(f'λ = {fz(lam)}', [f'λ = {fz(-lam)}' if lam else 'λ = 1', f'λ = {fz(Fr(rest, b[j]) + 1)}', f'λ = {fz(lam * 2) if lam else 2}']))


def c10s3_proj(r):
    a = rvec(r)
    b, nb = qvec(r)
    d = dot(a, b)
    return Q(f'Find the projection of the vector a⃗ = {vstr(a)} on the vector b⃗ = {vstr(b)}.', fz(Fr(d, nb)), f'a⃗·b⃗ = {fz(d)}, |b⃗| = {nb}; projection = a⃗·b⃗/|b⃗| = {fz(Fr(d, nb))}.',
             dist3(fz(Fr(d, nb)), [fz(d), fz(Fr(d, nb * nb)), fz(Fr(d, int(surd(sq(a)))) if surd(sq(a)).isdigit() else Fr(d, nb) + 1), fz(Fr(-d, nb)) if d else '1']))


def c10s3_mod(r):
    p, q = r.randint(2, 9), r.randint(2, 9)
    kind = r.randint(0, 2)
    if kind == 0:
        d = r.randint(-p * q + 1, p * q - 1)
        v = p * p + q * q + 2 * d
        return Q(f'If |a⃗| = {p}, |b⃗| = {q} and a⃗·b⃗ = {d}, find |a⃗ + b⃗|.', surd(v), f'|a⃗ + b⃗|² = |a⃗|² + |b⃗|² + 2a⃗·b⃗ = {p * p} + {q * q} + 2({d}) = {v}.', dist3(surd(v), [surd(p * p + q * q), str(p + q), surd(abs(p * p + q * q - 2 * d))]))
    if kind == 1:
        return Q(f'If |a⃗| = {p} and |b⃗| = {q}, find (a⃗ + b⃗)·(a⃗ − b⃗).', str(p * p - q * q), '(a⃗ + b⃗)·(a⃗ − b⃗) = |a⃗|² − |b⃗|².', num_distractors(p * p - q * q, p - q, p * p + q * q, q * q - p * p))
    d = r.choice([Fr(1, 2), Fr(1), Fr(0), Fr(-1, 2)])
    th = {Fr(1, 2): 'π/3', Fr(1): '0', Fr(0): 'π/2', Fr(-1, 2): '2π/3'}[d]
    return Q(f'Find a⃗·b⃗ if |a⃗| = {p}, |b⃗| = {q} and the angle between them is {th}.', fz(d * p * q), f'a⃗·b⃗ = |a⃗||b⃗| cos θ = {p} × {q} × {fz(d)}.', num_distractors(float(d * p * q), p * q, -d * p * q, p + q))


def c10s3_work(r):
    Fv, d = rvec(r, -4, 8), rvec(r, -4, 8)
    W = dot(Fv, d)
    who = name(r)
    return Q(f'{who} pulls a trolley with a constant force F⃗ = {vstr(Fv)} newtons, moving it through the displacement d⃗ = {vstr(d)} metres. Find the work done (W = F⃗·d⃗).', f'{fz(W)} J',
             f'W = {" + ".join(f"({x})({y})" for x, y in zip(Fv, d))} = {fz(W)} J.', num_distractors(float(W), W + 2, -W, sum(Fv) * sum(d)))


def c10s3_mcq(r):
    return mcqbank([
        ('If a⃗·b⃗ = 0 for non-zero vectors a⃗ and b⃗, then …', 'a⃗ and b⃗ are perpendicular', ['a⃗ and b⃗ are parallel', 'a⃗ = b⃗', '|a⃗| = |b⃗|'], 'cos θ = 0.'),
        ('î·î + ĵ·ĵ + k̂·k̂ = …', '3', ['0', '1', '−3'], 'Each is 1.'),
        ('î·ĵ = …', '0', ['1', 'k̂', '−1'], 'Perpendicular unit vectors.'),
        ('The projection of a⃗ on b⃗ is …', 'a⃗·b⃗/|b⃗|', ['a⃗·b⃗/|a⃗|', 'a⃗·b⃗', '|a⃗||b⃗|'], 'Scalar projection.'),
        ('a⃗·a⃗ equals …', '|a⃗|²', ['|a⃗|', '0', '1'], 'cos 0 = 1.'),
        ('The scalar product is …', 'commutative', ['not commutative', 'always a vector', 'always zero'], 'a⃗·b⃗ = b⃗·a⃗.'),
    ])(r)


def c10s3_ar(r):
    a, na = qvec(r)
    return arbank([
        (f'The vectors {vstr([2, 1, -1])} and {vstr([1, -1, 1])} are perpendicular.', 'Two non-zero vectors are perpendicular if and only if their scalar product is zero.', 'a', '2 − 1 − 1 = 0.'),
        (f'|{vstr(a)}|² = {na * na}.', 'a⃗·a⃗ = |a⃗|².', 'a', 'Sum of squares of components.'),
        ('If a⃗·b⃗ = a⃗·c⃗ and a⃗ ≠ 0⃗, then b⃗ = c⃗.', 'a⃗·(b⃗ − c⃗) = 0 means b⃗ − c⃗ is perpendicular to a⃗ (or zero).', 'd', 'b⃗ − c⃗ may be a non-zero vector perpendicular to a⃗; A false, R true.'),
        ('The angle θ between a⃗ and b⃗ satisfies cos θ = a⃗·b⃗/(|a⃗||b⃗|).', 'a⃗·b⃗ = |a⃗||b⃗| cos θ.', 'a', 'Rearranging R.'),
    ])(r)


def c10s3_case(r):
    a, na = qvec(r)
    b, nb = qvec(r)
    d = dot(a, b)
    who = name(r)
    return Q((f'Two ropes tied to a pole by {who}\'s scout troop pull along the vectors a⃗ = {vstr(a)} and b⃗ = {vstr(b)}. '
              f'(i) Find a⃗·b⃗. (ii) Find the cosine of the angle between the ropes. (iii) Find the projection of a⃗ on b⃗ and state whether the angle is acute, right or obtuse.'),
             f'(i) {fz(d)} (ii) {fz(Fr(d, na * nb))} (iii) {fz(Fr(d, nb))}; {"acute" if d > 0 else "right angle" if d == 0 else "obtuse"}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c10s3_long(r):
    a, na = qvec(r)
    b, nb = qvec(r)
    c = [x + y for x, y in zip(a, b)]
    e = [x - y for x, y in zip(a, b)]
    if not any(c) or not any(e):
        raise ValueError
    d = dot(c, e)
    return Q(f'If a⃗ = {vstr(a)} and b⃗ = {vstr(b)}, show that a⃗ + b⃗ and a⃗ − b⃗ are perpendicular' + (', and find the angle between a⃗ and b⃗.' if na == nb else f' only if |a⃗| = |b⃗|; here find (a⃗ + b⃗)·(a⃗ − b⃗) and the angle between a⃗ and b⃗.'),
             (f'(a⃗ + b⃗)·(a⃗ − b⃗) = |a⃗|² − |b⃗|² = {na * na - nb * nb}; ' + ('perpendicular; ' if d == 0 else 'not perpendicular; ')) + f'angle = cos⁻¹({fz(Fr(dot(a, b), na * nb))})',
             '(a⃗ + b⃗)·(a⃗ − b⃗) = |a⃗|² − |b⃗|² (2 marks); magnitudes (1 mark); angle via the dot product (2 marks).')


# ---- st4 cross product

def c10s4_cross(r):
    a, b = rvec(r), rvec(r)
    c = cross(a, b)
    if not any(c):
        raise ValueError
    return Q(f'Find a⃗ × b⃗ and |a⃗ × b⃗| if a⃗ = {vstr(a)} and b⃗ = {vstr(b)}.', f'{vstr(c)}; |a⃗ × b⃗| = {surd(sq(c))}',
             f'a⃗ × b⃗ = |î ĵ k̂; {a[0]} {a[1]} {a[2]}; {b[0]} {b[1]} {b[2]}| = {vstr(c)} (1 mark); magnitude √{sq(c)} (1 mark).',
             [f'{vstr([-x for x in c])}; |a⃗ × b⃗| = {surd(sq(c))}', f'{vstr([a[i] * b[i] for i in range(3)]) if any(a[i] * b[i] for i in range(3)) else "0⃗"}; |a⃗ × b⃗| = {surd(sq([a[i] * b[i] for i in range(3)]))}', f'{vstr(c)}; |a⃗ × b⃗| = {surd(sq(c) + 1)}'])


def c10s4_area(r):
    kind = r.randint(0, 2)
    if kind == 0:
        a, b = rvec(r), rvec(r)
        c = cross(a, b)
        if not any(c):
            raise ValueError
        return Q(f'Find the area of the parallelogram whose adjacent sides are given by the vectors {vstr(a)} and {vstr(b)}.', f'{surd(sq(c))} sq units',
                 f'Area = |a⃗ × b⃗| = |{vstr(c)}| = {surd(sq(c))}.', [f'{surd(Fr(sq(c), 4))} sq units', f'{surd(sq(c) + 4)} sq units', f'{abs(dot(a, b))} sq units'])
    if kind == 1:
        A, B, C = rvec(r, -3, 5, False), rvec(r, -3, 5, False), rvec(r, -3, 5, False)
        u = [b - a for a, b in zip(A, B)]
        v = [c - a for a, c in zip(A, C)]
        c = cross(u, v)
        if not any(c):
            raise ValueError
        return Q(f'Find the area of the triangle with vertices A{P3(A)}, B{P3(B)} and C{P3(C)}.', f'{surd(Fr(sq(c), 4))} sq units',
                 f'AB⃗ = {vstr(u)}, AC⃗ = {vstr(v)} (1 mark); AB⃗ × AC⃗ = {vstr(c)} (1 mark); area = ½|AB⃗ × AC⃗| = {surd(Fr(sq(c), 4))} (1 mark).',
                 [f'{surd(sq(c))} sq units', f'{surd(Fr(sq(c), 2))} sq units', f'{surd(Fr(sq(c), 4) + 1)} sq units'])
    d1, d2 = rvec(r), rvec(r)
    c = cross(d1, d2)
    if not any(c):
        raise ValueError
    return Q(f'Find the area of the parallelogram whose diagonals are given by {vstr(d1)} and {vstr(d2)}.', f'{surd(Fr(sq(c), 4))} sq units', f'Area = ½|d⃗₁ × d⃗₂| = ½|{vstr(c)}| = {surd(Fr(sq(c), 4))}.',
             [f'{surd(sq(c))} sq units', f'{surd(Fr(sq(c), 16))} sq units', f'{surd(Fr(sq(c), 2))} sq units'])


def c10s4_unit(r):
    a, b = rvec(r), rvec(r)
    c = cross(a, b)
    if not any(c):
        raise ValueError
    return Q(f'Find a unit vector perpendicular to each of the vectors {vstr(a)} and {vstr(b)}.', f'±{unit_txt(c)}', f'a⃗ × b⃗ = {vstr(c)}, |a⃗ × b⃗| = {surd(sq(c))}; unit vector ±(a⃗ × b⃗)/|a⃗ × b⃗| (2 marks).',
             [f'±{unit_txt([x + y for x, y in zip(a, b)])}' if any(x + y for x, y in zip(a, b)) else '±k̂', f'±{vstr(c)}', f'±{unit_txt([a[i] * b[i] + 1 for i in range(3)])}'])


def c10s4_lagrange(r):
    p, q = r.randint(2, 9), r.randint(2, 9)
    d = r.randint(1, p * q - 1)
    c2 = p * p * q * q - d * d
    return Q(f'If |a⃗| = {p}, |b⃗| = {q} and a⃗·b⃗ = {d}, find |a⃗ × b⃗|.', surd(c2), f'|a⃗ × b⃗|² + (a⃗·b⃗)² = |a⃗|²|b⃗|² ⇒ |a⃗ × b⃗|² = {p * p * q * q} − {d * d} = {c2}.',
             dist3(surd(c2), [str(p * q - d), surd(p * p * q * q + d * d), str(p * q)]))


def c10s4_mcq(r):
    return mcqbank([
        ('î × ĵ = …', 'k̂', ['−k̂', '0⃗', '1'], 'Right-handed system.'),
        ('a⃗ × a⃗ = …', '0⃗', ['|a⃗|²', '1', 'a⃗'], 'sin 0 = 0.'),
        ('a⃗ × b⃗ = …', '−(b⃗ × a⃗)', ['b⃗ × a⃗', 'a⃗·b⃗', '0⃗ always'], 'Anti-commutative.'),
        ('If a⃗ × b⃗ = 0⃗ for non-zero vectors, then a⃗ and b⃗ are …', 'parallel (collinear)', ['perpendicular', 'unit vectors', 'equal in magnitude'], 'sin θ = 0.'),
        ('The area of a triangle with adjacent sides a⃗ and b⃗ is …', '½|a⃗ × b⃗|', ['|a⃗ × b⃗|', 'a⃗·b⃗', '½ a⃗·b⃗'], 'Half the parallelogram.'),
        ('ĵ × k̂ = …', 'î', ['−î', 'ĵ', '0⃗'], 'Cyclic order.'),
        ('k̂ × ĵ = …', '−î', ['î', 'k̂', '0⃗'], 'Reverse of the cyclic order.'),
    ])(r)


def c10s4_ar(r):
    a = rvec(r)
    k = r.choice([2, 3, -2])
    return arbank([
        (f'({vstr(a)}) × ({vstr([k * x for x in a])}) = 0⃗.', 'The cross product of two collinear vectors is the zero vector.', 'a', 'sin 0 = 0.'),
        ('a⃗ × b⃗ = b⃗ × a⃗ for all vectors a⃗, b⃗.', 'a⃗ × b⃗ is perpendicular to both a⃗ and b⃗.', 'd', 'a⃗ × b⃗ = −(b⃗ × a⃗); A false, R true.'),
        ('The area of the parallelogram with adjacent sides a⃗ and b⃗ is |a⃗ × b⃗|.', '|a⃗ × b⃗| = |a⃗||b⃗| sin θ.', 'a', 'Base × height.'),
        ('î × (ĵ × k̂) = 0⃗.', 'ĵ × k̂ = î.', 'a', 'î × î = 0⃗.'),
    ])(r)


def c10s4_case(r):
    A, B, C = rvec(r, 0, 7, False), rvec(r, 0, 7, False), rvec(r, 0, 7, False)
    u = [b - a for a, b in zip(A, B)]
    v = [c - a for a, c in zip(A, C)]
    c = cross(u, v)
    if not any(c):
        raise ValueError
    who = name(r)
    return Q((f'{who} designs a triangular sail with corners A{P3(A)}, B{P3(B)} and C{P3(C)} (metres). (i) Find AB⃗ and AC⃗. (ii) Find AB⃗ × AC⃗. (iii) Find the area of the sail.'),
             f'(i) {vstr(u)}, {vstr(v)} (ii) {vstr(c)} (iii) {surd(Fr(sq(c), 4))} m²', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c10s4_long(r):
    a, b = rvec(r), rvec(r)
    c = cross(a, b)
    if not any(c):
        raise ValueError
    s, d = [x + y for x, y in zip(a, b)], [x - y for x, y in zip(a, b)]
    c2 = cross(s, d)
    return Q(f'Let a⃗ = {vstr(a)} and b⃗ = {vstr(b)}. Find a unit vector perpendicular to both a⃗ + b⃗ and a⃗ − b⃗, and verify that (a⃗ + b⃗) × (a⃗ − b⃗) = −2(a⃗ × b⃗).',
             f'±{unit_txt(c2)}; (a⃗ + b⃗) × (a⃗ − b⃗) = {vstr(c2)} = −2({vstr(c)})', 'a⃗ + b⃗ and a⃗ − b⃗ (1 mark); cross product (2 marks); unit vector (1 mark); verification (1 mark).')


# ======================================================================= ch11 Three Dimensional Geometry

def c11s1_dr(r):
    P, Qp = rvec(r, -5, 8, False), rvec(r, -5, 8, False)
    d = [b - a for a, b in zip(P, Qp)]
    if not any(d):
        raise ValueError
    n2 = sq(d)
    sd = surd(n2)
    sd = f'({sd})' if ('√' in sd and not sd.startswith('√')) else sd
    dc = ', '.join(fz(Fr(x, 1)) + f'/{sd}' if sd != '1' else fz(x) for x in d) if not surd(n2).isdigit() else ', '.join(fz(Fr(x, int(surd(n2)))) for x in d)
    return Q(f'Find the direction cosines of the line passing through the points P{P3(P)} and Q{P3(Qp)}.', f'±({dc})',
             f'Direction ratios {", ".join(map(str, d))} (1 mark); divide by √{n2}' + (f' = {surd(n2)}' if surd(n2) != f'√{n2}' else '') + ' (1 mark).', [f'±({", ".join(map(str, d))})', f'±({", ".join(fz(Fr(x, n2)) for x in d)})', f'±({", ".join(str(a + b) for a, b in zip(P, Qp))})'])


def c11s1_third(r):
    kind = r.randint(0, 2)
    if kind == 0:
        angs = r.choice([('90°', '135°', '45°', '0, −1/√2, 1/√2'), ('90°', '60°', '30°', '0, 1/2, √3/2'), ('60°', '60°', '45°', '1/2, 1/2, 1/√2'),
                         ('45°', '60°', '120°', '1/√2, 1/2, −1/2'), ('120°', '60°', '135°', '−1/2, 1/2, −1/√2'), ('90°', '45°', '135°', '0, 1/√2, −1/√2')])
        return Q(f'A line makes angles {angs[0]}, {angs[1]} and {angs[2]} with the positive x-, y- and z-axes. Find its direction cosines.', angs[3],
                 'l = cos α, m = cos β, n = cos γ; check l² + m² + n² = 1.', [x for x in ['1, 0, 0', '0, 1/2, 1/2', '1/√2, 1/√2, 0', '1/2, 1/2, 1/2', '0, −1/2, √3/2'] if x != angs[3]][:3])
    if kind == 1:
        v, n = qvec(r)
        l, m = Fr(v[0], n), Fr(v[1], n)
        nn = Fr(v[2], n)
        return Q(f'If a line has direction cosines l = {fz(l)}, m = {fz(m)} and n, find the possible values of n.', f'n = ±{fz(abs(nn))}', f'l² + m² + n² = 1 ⇒ n² = 1 − {fz(l * l)} − {fz(m * m)} = {fz(nn * nn)}.',
                 [f'n = {fz(1 - abs(l) - abs(m))}', f'n = ±{fz(nn * nn)}', f'n = ±{fz(abs(nn) + Fr(1, n))}'])
    return Q('Find the direction cosines of a line which makes equal angles with the coordinate axes.', '±(1/√3, 1/√3, 1/√3)', '3l² = 1 ⇒ l = ±1/√3.', ['(1, 1, 1)', '(1/3, 1/3, 1/3)', '±(1/√2, 1/√2, 0)'])


def c11s1_col(r):
    A = rvec(r, -4, 5, False)
    d = rvec(r, -3, 4)
    t1, t2 = r.sample([-2, -1, 2, 3], 2)
    B = [a + t1 * x for a, x in zip(A, d)]
    C = [a + t2 * x for a, x in zip(A, d)]
    return Q(f'Using direction ratios, show that the points A{P3(A)}, B{P3(B)} and C{P3(C)} are collinear.', 'Collinear',
             f'DRs of AB: {", ".join(str(t1 * x) for x in d)}; of BC: {", ".join(str((t2 - t1) * x) for x in d)}; they are proportional and B is common (2 marks).', ['Not collinear', 'Collinear only if A is the origin', 'Cannot be decided from direction ratios'])


def c11s1_mcq(r):
    return mcqbank([
        ('If l, m, n are the direction cosines of a line, then …', 'l² + m² + n² = 1', ['l + m + n = 1', 'l² + m² + n² = 0', 'lmn = 1'], 'Standard identity.'),
        ('The direction cosines of the x-axis are …', '1, 0, 0', ['0, 1, 0', '0, 0, 1', '1, 1, 1'], 'α = 0, β = γ = 90°.'),
        ('Direction ratios of a line are …', 'any three numbers proportional to its direction cosines', ['always its direction cosines', 'always integers', 'unique for a line'], 'Definition.'),
        ('If a line makes angles α, β, γ with the axes, then sin²α + sin²β + sin²γ = …', '2', ['1', '3', '0'], '3 − (cos²α + cos²β + cos²γ) = 2.'),
        ('The direction ratios of the line joining (x₁, y₁, z₁) and (x₂, y₂, z₂) are …', 'x₂ − x₁, y₂ − y₁, z₂ − z₁', ['x₁ + x₂, y₁ + y₂, z₁ + z₂', 'x₁x₂, y₁y₂, z₁z₂', 'x₂/x₁, y₂/y₁, z₂/z₁'], 'Differences of coordinates.'),
    ])(r)


def c11s1_ar(r):
    v, n = qvec(r)
    return arbank([
        (f'{", ".join(fz(Fr(x, n)) for x in v)} are the direction cosines of a line.', 'The sum of the squares of the direction cosines of a line is 1.', 'a', f'Squares sum to {n * n}/{n * n} = 1.'),
        ('1/2, 1/2, 1/2 can be the direction cosines of a line.', 'Direction cosines satisfy l² + m² + n² = 1.', 'd', '3/4 ≠ 1; A false, R true.'),
        (f'{", ".join(str(x) for x in v)} are direction ratios of a line with direction cosines {", ".join(fz(Fr(x, n)) for x in v)}.', 'Direction ratios are proportional to direction cosines.', 'a', 'Multiply by the magnitude.'),
    ])(r)


def c11s1_case(r):
    P, Qp = rvec(r, 0, 9, False), rvec(r, 0, 9, False)
    d = [b - a for a, b in zip(P, Qp)]
    if not any(d):
        raise ValueError
    n2 = sq(d)
    who = name(r)
    return Q((f'{who} stretches a zip-line from P{P3(P)} to Q{P3(Qp)} (metres) for a school camp. (i) Find the direction ratios of PQ. (ii) Find the length PQ. (iii) Find the direction cosines of PQ.'),
             f'(i) {", ".join(map(str, d))} (ii) {surd(n2)} m (iii) {", ".join(fz(x) + "/" + surd(n2) if not surd(n2).isdigit() else fz(Fr(x, int(surd(n2)))) for x in d)}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ---- st2 equation of a line

def _cart(a, b):
    parts = []
    for v, p, q in zip('xyz', a, b):
        top = v if p == 0 else f'{v} {"−" if p > 0 else "+"} {abs(p)}'
        parts.append(f'({top})/{fz(q)}' if p else f'{v}/{fz(q)}')
    return ' = '.join(parts)


def c11s2_vec(r):
    a = rvec(r, -5, 6, False)
    b = rvec(r)
    if 0 in b:
        b = [x or 1 for x in b]
    kind = r.randint(0, 1)
    if kind == 0:
        ans = f'r⃗ = ({vstr(a) if any(a) else "0⃗"}) + λ({vstr(b)}); {_cart(a, b)}'
        return Q(f'Find the vector and Cartesian equations of the line through the point {P3(a)} and parallel to the vector {vstr(b)}.', ans,
                 'r⃗ = a⃗ + λb⃗ (1 mark); (x − x₁)/b₁ = (y − y₁)/b₂ = (z − z₁)/b₃ (1 mark).',
                 [f'r⃗ = ({vstr(b)}) + λ({vstr(a) if any(a) else "î"}); {_cart(b, [x or 1 for x in a])}', f'r⃗ = ({vstr(a) if any(a) else "0⃗"}) + λ({vstr(b)}); {_cart([-x for x in a], b)}', f'r⃗ = λ({vstr(b)}); {_cart([0, 0, 0], b)}'])
    B = [x + y for x, y in zip(a, b)]
    return Q(f'Find the vector equation of the line passing through the points {P3(a)} and {P3(B)}.', f'r⃗ = ({vstr(a) if any(a) else "0⃗"}) + λ({vstr(b)})',
             'r⃗ = a⃗ + λ(b⃗ − a⃗).', [f'r⃗ = ({vstr(a) if any(a) else "0⃗"}) + λ({vstr(B)})', f'r⃗ = ({vstr(B)}) + λ({vstr([x + y for x, y in zip(a, B)])})', f'r⃗ = λ({vstr(B)})'])


def c11s2_conv(r):
    a = rvec(r, -5, 6, False)
    b = [x or 1 for x in rvec(r)]
    j = r.randint(0, 2)
    v = 'xyz'[j]
    parts = []
    for i, (p, q) in enumerate(zip(a, b)):
        vv = 'xyz'[i]
        if i == j:
            parts.append(f'({fz(p)} − {vv})/{fz(-q)}' if p else f'−{vv}/{fz(-q)}')
        else:
            parts.append(f'({vv} {"−" if p > 0 else "+"} {abs(p)})/{fz(q)}' if p else f'{vv}/{fz(q)}')
    return Q(f'The Cartesian equation of a line is {" = ".join(parts)}. Write its vector equation and its direction ratios.', f'r⃗ = ({vstr(a) if any(a) else "0⃗"}) + λ({vstr(b)}); DRs {", ".join(map(str, b))}',
             f'Rewrite ({fz(a[j])} − {v})/{fz(-b[j])} as ({v} − {fz(a[j])})/{fz(b[j])} (1 mark); read off the point and direction (1 mark).'.replace('(0 − ', '(−').replace('− 0)', ')'),
             [f'r⃗ = ({vstr(a) if any(a) else "0⃗"}) + λ({vstr([(-q if i == j else q) for i, q in enumerate(b)])}); DRs {", ".join(str(-q if i == j else q) for i, q in enumerate(b))}',
              f'r⃗ = ({vstr([-x for x in a]) if any(a) else "0⃗"}) + λ({vstr(b)}); DRs {", ".join(map(str, b))}', f'r⃗ = ({vstr(b)}) + λ({vstr(a) if any(a) else "î"}); DRs {", ".join(map(str, a))}'])


def c11s2_point(r):
    a = rvec(r, -5, 6, False)
    b = [x or 1 for x in rvec(r)]
    lam = r.choice([-2, -1, 2, 3])
    Pt = [x + lam * y for x, y in zip(a, b)]
    if r.random() < 0.5:
        return Q(f'Show that the point {P3(Pt)} lies on the line {_cart(a, b)}, and find the value of the parameter λ for it.', f'Yes; λ = {lam}',
                 f'Each ratio equals {lam}: ({Pt[0]} − {a[0]})/{b[0]} = ({Pt[1]} − {a[1]})/{b[1]} = ({Pt[2]} − {a[2]})/{b[2]} = {lam}.'.replace('− -', '+ '), ['No', f'Yes; λ = {-lam}', f'Yes; λ = {lam + 1}'])
    Pt2 = Pt[:]
    Pt2[2] += r.choice([1, -1, 2])
    return Q(f'Does the point {P3(Pt2)} lie on the line {_cart(a, b)}? Justify.', 'No', 'The three ratios are not all equal.', ['Yes', 'Only if λ = 0', 'Yes, with λ = 1'])


def c11s2_mcq(r):
    return mcqbank([
        ('The vector equation of the line through the point with position vector a⃗ and parallel to b⃗ is …', 'r⃗ = a⃗ + λb⃗', ['r⃗ = b⃗ + λa⃗', 'r⃗ = λ(a⃗ + b⃗)', 'r⃗·b⃗ = a⃗·b⃗'], 'Standard form.'),
        ('The direction ratios of the line (x − 1)/2 = (y + 3)/(−1) = (z − 4)/5 are …', '2, −1, 5', ['1, −3, 4', '−1, 3, −4', '2, 1, 5'], 'Denominators.'),
        ('The line (x − 2)/3 = (y + 1)/4 = (z − 5)/(−2) passes through …', '(2, −1, 5)', ['(3, 4, −2)', '(−2, 1, −5)', '(2, 1, 5)'], 'Numerators set to zero.'),
        ('The Cartesian equation of the line through (x₁, y₁, z₁) and (x₂, y₂, z₂) is …', '(x − x₁)/(x₂ − x₁) = (y − y₁)/(y₂ − y₁) = (z − z₁)/(z₂ − z₁)', ['(x − x₁)/x₂ = (y − y₁)/y₂ = (z − z₁)/z₂', 'x/x₁ = y/y₁ = z/z₁', '(x + x₁)/(x₂ + x₁) = …'], 'Two-point form.'),
        ('The x-axis can be written as …', 'x/1 = y/0 = z/0', ['x/0 = y/1 = z/1', 'x = y = z', 'x/1 = y/1 = z/0'], 'Direction 1, 0, 0 through the origin.'),
    ])(r)


def c11s2_ar(r):
    a = rvec(r, -5, 6, False)
    b = [x or 1 for x in rvec(r)]
    return arbank([
        (f'The line {_cart(a, b)} has direction ratios {", ".join(map(str, b))}.', 'In (x − x₁)/a = (y − y₁)/b = (z − z₁)/c, the denominators are direction ratios.', 'a', 'Read off the denominators.'),
        (f'The line ({fz(a[0])} − x)/{b[0]} = (y − {a[1]})/{b[1]} = (z − {a[2]})/{b[2]} has direction ratios {", ".join(map(str, b))}.'.replace('− -', '+ '), 'In the standard form, x, y, z must have coefficient +1 in the numerators.', 'd',
         f'Rewrite as (x − {fz(a[0])})/({-b[0]}): DRs are {-b[0]}, {b[1]}, {b[2]}; A false, R true.'),
        ('A line in space is fixed by a point on it and its direction.', 'r⃗ = a⃗ + λb⃗ represents a line for all real λ.', 'a', 'The vector equation uses exactly a point and a direction.'),
    ])(r)


def c11s2_case(r):
    a = rvec(r, 0, 9, False)
    b = [abs(x) or 1 for x in rvec(r, 1, 6)]
    t = r.choice([2, 3, 4])
    Pt = [x + t * y for x, y in zip(a, b)]
    who = name(r)
    return Q((f'An aircraft spotted by {who} at the {r.choice(CITIES)} airport passes through the point A{P3(a)} (km) and flies in the direction of {vstr(b)}. '
              f'(i) Write the vector equation of its path. (ii) Write the Cartesian equation. (iii) Find its position when λ = {t}.'),
             f'(i) r⃗ = ({vstr(a)}) + λ({vstr(b)}) (ii) {_cart(a, b)} (iii) {P3(Pt)}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ---- st3 angle between two lines

def c11s3_angle(r):
    b1, n1 = qvec(r)
    b2, n2 = qvec(r)
    c = Fr(abs(dot(b1, b2)), n1 * n2)
    ans = 'π/2' if c == 0 else f'cos⁻¹({fz(c)})'
    a1, a2 = rvec(r, -4, 5, False), rvec(r, -4, 5, False)
    if 0 in b1 or 0 in b2:
        raise ValueError
    return Q(f'Find the angle between the lines {_cart(a1, b1)} and {_cart(a2, b2)}.', ans, f'cos θ = |b⃗₁·b⃗₂|/(|b⃗₁||b⃗₂|) = {abs(dot(b1, b2))}/({n1} × {n2}) = {fz(c)}.',
             dist3(ans, [f'cos⁻¹({fz(Fr(abs(dot(b1, b2)), n1 * n1 + n2 * n2))})', f'sin⁻¹({fz(c)})' if c else 'π/3', f'cos⁻¹({fz(Fr(abs(dot(a1, a2)), n1 * n2))})' if Fr(abs(dot(a1, a2)), n1 * n2) <= 1 and Fr(abs(dot(a1, a2)), n1 * n2) != c else 'π/4']))


def c11s3_perp(r):
    while True:
        b1 = [x or 1 for x in rvec(r)]
        b2 = [x or 1 for x in rvec(r)]
        j = r.randint(0, 2)
        rest = sum(b1[i] * b2[i] for i in range(3) if i != j)
        if b1[j] == 0:
            continue
        k = Fr(-rest, b1[j])
        if k.denominator == 1 and k != 0:
            break
    d2 = [fz(x) for x in b2]
    d2[j] = 'k'
    a1, a2 = rvec(r, -4, 5, False), rvec(r, -4, 5, False)
    l1 = _cart(a1, b1)
    l2 = ' = '.join((f'({v} {"−" if p > 0 else "+"} {abs(p)})/{q}' if p else f'{v}/{q}') for v, p, q in zip('xyz', a2, d2))
    return Q(f'Find the value of k so that the lines {l1} and {l2} are perpendicular to each other.', f'k = {fz(k)}', f'a₁a₂ + b₁b₂ + c₁c₂ = 0 ⇒ {fz(rest)} + {fz(b1[j])}k = 0 ⇒ k = {fz(k)}.',
             dist3(f'k = {fz(k)}', [f'k = {fz(-k)}', f'k = {fz(k + 1)}', f'k = {fz(Fr(rest, b1[j]) * 2) if rest else 3}']))


def c11s3_par(r):
    b = [x or 1 for x in rvec(r)]
    k = r.choice([2, 3, -2, -1])
    b2 = [k * x for x in b]
    a1, a2 = rvec(r, -4, 5, False), rvec(r, -4, 5, False)
    return Q(f'Show that the lines {_cart(a1, b)} and {_cart(a2, b2)} are parallel.', 'Parallel: direction ratios are proportional',
             f'{", ".join(map(str, b2))} = {k} × ({", ".join(map(str, b))}).', ['Perpendicular', 'Intersecting at right angles', 'Skew'])


def c11s3_mcq(r):
    return mcqbank([
        ('The angle θ between the lines with direction ratios a₁, b₁, c₁ and a₂, b₂, c₂ is given by cos θ = …', '|a₁a₂ + b₁b₂ + c₁c₂|/(√(a₁² + b₁² + c₁²)√(a₂² + b₂² + c₂²))', ['a₁a₂ + b₁b₂ + c₁c₂', '|a₁b₂ − a₂b₁|', '(a₁ + a₂)(b₁ + b₂)(c₁ + c₂)'], 'Standard formula.'),
        ('Two lines with direction ratios a₁, b₁, c₁ and a₂, b₂, c₂ are perpendicular if …', 'a₁a₂ + b₁b₂ + c₁c₂ = 0', ['a₁/a₂ = b₁/b₂ = c₁/c₂', 'a₁ + b₁ + c₁ = 0', 'a₁a₂ = b₁b₂'], 'Zero dot product.'),
        ('Two lines with direction ratios a₁, b₁, c₁ and a₂, b₂, c₂ are parallel if …', 'a₁/a₂ = b₁/b₂ = c₁/c₂', ['a₁a₂ + b₁b₂ + c₁c₂ = 0', 'a₁ = b₂', 'a₁ + a₂ = 0'], 'Proportional DRs.'),
        ('The angle between the lines x/1 = y/0 = z/0 and x/0 = y/1 = z/0 is …', 'π/2', ['0', 'π/4', 'π'], 'x- and y-axes.'),
        ('The angle between two lines is taken so that cos θ is …', 'non-negative (0 ≤ θ ≤ π/2)', ['always negative', 'always 1', 'any value'], 'Acute angle between lines.'),
    ])(r)


def c11s3_ar(r):
    b, n = qvec(r)
    k = r.choice([2, 3, -2])
    return arbank([
        (f'The lines with direction ratios {", ".join(map(str, b))} and {", ".join(str(k * x) for x in b)} are parallel.', 'Lines with proportional direction ratios are parallel.', 'a', 'R explains A.'),
        ('Lines with direction ratios 1, 2, 3 and 3, −3, 1 are perpendicular.', 'Two lines are perpendicular if a₁a₂ + b₁b₂ + c₁c₂ = 0.', 'a', '3 − 6 + 3 = 0.'),
        ('Lines with direction ratios 1, 1, 1 and 1, −1, 1 are perpendicular.', 'Two lines are perpendicular if a₁a₂ + b₁b₂ + c₁c₂ = 0.', 'd', '1 − 1 + 1 = 1 ≠ 0; A false, R true.'),
    ])(r)


def c11s3_case(r):
    b1, n1 = qvec(r)
    b2, n2 = qvec(r)
    b1 = [abs(x) for x in b1]
    c = Fr(abs(dot(b1, b2)), n1 * n2)
    who = name(r)
    return Q((f'Two straight metal rods in {who}\'s sculpture lie along lines with direction ratios {", ".join(map(str, b1))} and {", ".join(map(str, b2))}. '
              f'(i) Find the direction cosines of the first rod. (ii) Find the cosine of the angle between the rods. (iii) Are the rods perpendicular? Justify.'),
             f'(i) {", ".join(fz(Fr(x, n1)) for x in b1)} (ii) {fz(c)} (iii) {"Yes" if c == 0 else "No"}: b⃗₁·b⃗₂ = {dot(b1, b2)}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ---- st4 shortest distance

def c11s4_skew(r):
    while True:
        a1, a2 = rvec(r, -4, 5, False), rvec(r, -4, 5, False)
        b1, b2 = [x or 1 for x in rvec(r, -3, 4)], [x or 1 for x in rvec(r, -3, 4)]
        c = cross(b1, b2)
        if any(c):
            d = abs(dot([y - x for x, y in zip(a1, a2)], c))
            if d != 0:
                break
    sd = Fr(d) / 1
    n2 = sq(c)
    ans = surd(Fr(d * d, n2))
    return Q(f'Find the shortest distance between the lines r⃗ = ({vstr(a1) if any(a1) else "0⃗"}) + λ({vstr(b1)}) and r⃗ = ({vstr(a2) if any(a2) else "0⃗"}) + μ({vstr(b2)}).', f'{ans} units',
             f'a⃗₂ − a⃗₁ = {vstr([y - x for x, y in zip(a1, a2)])} (1 mark); b⃗₁ × b⃗₂ = {vstr(c)}, |b⃗₁ × b⃗₂| = √{n2} (2 marks); d = |(a⃗₂ − a⃗₁)·(b⃗₁ × b⃗₂)|/|b⃗₁ × b⃗₂| = {d}/√{n2} = {ans} (2 marks).')


def c11s4_par(r):
    while True:
        a1, a2 = rvec(r, -4, 5, False), rvec(r, -4, 5, False)
        b = [x or 1 for x in rvec(r, -3, 4)]
        k = r.choice([1, 2])
        w = [y - x for x, y in zip(a1, a2)]
        c = cross(b, w)
        if any(c):
            break
    ans = surd(Fr(sq(c), sq(b)))
    return Q(f'Find the distance between the parallel lines r⃗ = ({vstr(a1) if any(a1) else "0⃗"}) + λ({vstr(b)}) and r⃗ = ({vstr(a2) if any(a2) else "0⃗"}) + μ({vstr([k * x for x in b])}).', f'{ans} units',
             f'd = |b⃗ × (a⃗₂ − a⃗₁)|/|b⃗| with b⃗ × (a⃗₂ − a⃗₁) = {vstr(c)} (2 marks); d = √{sq(c)}/√{sq(b)} = {ans} (1 mark).',
             [f'{surd(sq(c))} units', f'{surd(Fr(sq(w), 1))} units', f'{surd(Fr(sq(c), sq(b)) + 1)} units'])


def c11s4_int(r):
    a1 = rvec(r, -4, 5, False)
    b1, b2 = [x or 1 for x in rvec(r, -3, 4)], [x or 1 for x in rvec(r, -3, 4)]
    if not any(cross(b1, b2)):
        raise ValueError
    l, m = r.choice([-1, 1, 2]), r.choice([-2, -1, 1, 2])
    P = [x + l * y for x, y in zip(a1, b1)]
    a2 = [p - m * y for p, y in zip(P, b2)]
    return Q(f'Show that the lines {_cart(a1, b1)} and {_cart(a2, b2)} intersect, by finding the shortest distance between them. Also find the point of intersection.',
             f'Shortest distance 0; they meet at {P3(P)}', '(a⃗₂ − a⃗₁)·(b⃗₁ × b⃗₂) = 0 (3 marks); equate general points to find λ, μ (2 marks).',
             ['They are skew', 'They are parallel', f'They meet at {P3(a1)}'])


def c11s4_mcq(r):
    return mcqbank([
        ('Lines in space which are neither parallel nor intersecting are called …', 'skew lines', ['coplanar lines', 'perpendicular lines', 'concurrent lines'], 'Definition.'),
        ('The shortest distance between two intersecting lines is …', '0', ['1', 'infinite', 'the distance between their direction vectors'], 'They have a common point.'),
        ('The shortest distance between the skew lines r⃗ = a⃗₁ + λb⃗₁ and r⃗ = a⃗₂ + μb⃗₂ is …', '|(a⃗₂ − a⃗₁)·(b⃗₁ × b⃗₂)|/|b⃗₁ × b⃗₂|', ['|a⃗₂ − a⃗₁|', '|b⃗₁ × b⃗₂|', '|(a⃗₂ − a⃗₁) × b⃗₁|'], 'Standard formula.'),
        ('The distance between parallel lines r⃗ = a⃗₁ + λb⃗ and r⃗ = a⃗₂ + μb⃗ is …', '|b⃗ × (a⃗₂ − a⃗₁)|/|b⃗|', ['|(a⃗₂ − a⃗₁)·b⃗|/|b⃗|', '|a⃗₂ − a⃗₁|', '|b⃗|'], 'Standard formula.'),
        ('The shortest distance between two skew lines is measured along …', 'the line perpendicular to both', ['either line', 'the x-axis', 'the line joining their given points'], 'Common perpendicular.'),
    ])(r)


def c11s4_ar(r):
    return arbank([
        ('The shortest distance between the lines r⃗ = î + λĵ and r⃗ = k̂ + μî is 1.', 'b⃗₁ × b⃗₂ = ĵ × î = −k̂ and (a⃗₂ − a⃗₁)·(b⃗₁ × b⃗₂) = (k̂ − î)·(−k̂) = −1.', 'a', 'd = |−1|/1 = 1.'),
        ('Two lines with zero shortest distance are always parallel.', 'If the shortest distance is zero, the lines intersect (or coincide).', 'd', 'A is false; R is true.'),
        ('The shortest distance between parallel lines is |b⃗ × (a⃗₂ − a⃗₁)|/|b⃗|.', 'For parallel lines b⃗₁ × b⃗₂ = 0⃗, so the skew-line formula cannot be used.', 'b', 'Both true; R explains why a different formula is needed, not the formula itself.'),
    ])(r)


def c11s4_case(r):
    while True:
        a1, a2 = rvec(r, 0, 6, False), rvec(r, 0, 6, False)
        b1, b2 = [x or 1 for x in rvec(r, -2, 4)], [x or 1 for x in rvec(r, -2, 4)]
        c = cross(b1, b2)
        if any(c):
            d = abs(dot([y - x for x, y in zip(a1, a2)], c))
            if d:
                break
    who = name(r)
    return Q((f'Two straight pipes in a factory where {who} works follow the lines r⃗ = ({vstr(a1) if any(a1) else "0⃗"}) + λ({vstr(b1)}) and r⃗ = ({vstr(a2) if any(a2) else "0⃗"}) + μ({vstr(b2)}) (metres). '
              f'(i) Show that the pipes are not parallel. (ii) Find b⃗₁ × b⃗₂. (iii) Find the shortest distance between the pipes.'),
             f'(i) direction ratios not proportional (ii) {vstr(c)} (iii) {surd(Fr(d * d, sq(c)))} m', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch12 Linear Programming

PRODUCTS = [('tables', 'chairs', 'a furniture dealer'), ('cricket bats', 'hockey sticks', 'a sports goods factory'), ('pedestal fans', 'table fans', 'an electricals unit'),
            ('necklaces', 'bracelets', 'a jewellery workshop'), ('toys of type A', 'toys of type B', 'a toy maker'), ('screws A', 'screws B', 'a small factory'),
            ('cakes of kind P', 'cakes of kind Q', 'a bakery'), ('souvenirs of type A', 'souvenirs of type B', 'a cottage industry')]


def _max_lpp(r, tries=200):
    for _ in range(tries):
        a1, b1, a2, b2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
        x0, y0 = r.randint(1, 10), r.randint(1, 10)
        c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
        cons = [(a1, b1, c1, '<='), (a2, b2, c2, '<=')]
        V = lpp_vertices(cons)
        if len(V) == 4 and all(x.denominator == 1 and y.denominator == 1 for x, y in V):
            p, q = r.randint(1, 9), r.randint(1, 9)
            vals = {v: p * v[0] + q * v[1] for v in V}
            best = max(vals.values())
            if sum(1 for v in vals.values() if v == best) == 1:
                return cons, V, p, q, vals
    raise ValueError


def c12s1_form(r):
    A, B, who = r.choice(PRODUCTS)
    a1, b1, a2, b2 = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    T1, T2 = r.randint(12, 60), r.randint(12, 60)
    p, q = r.choice([10, 20, 25, 30, 40, 50, 60, 75, 80, 100]), r.choice([10, 15, 20, 30, 35, 40, 50, 60, 90])
    return Q(f'{who.capitalize()} makes {A} and {B}. Each unit of {A} needs {a1} hours on machine M₁ and {a2} hours on machine M₂; each unit of {B} needs {b1} hours on M₁ and {b2} hours on M₂. '
             f'M₁ and M₂ are available for at most {T1} and {T2} hours a day. The profit is ₹{p} per unit of {A} and ₹{q} per unit of {B}. Formulate the linear programming problem to maximise profit.',
             f'Maximise Z = {p}x + {q}y subject to {a1}x + {b1}y ≤ {T1}, {a2}x + {b2}y ≤ {T2}, x ≥ 0, y ≥ 0 (x, y = units of {A}, {B})'.replace(' 1x', ' x').replace(' 1y', ' y').replace('(1x', '(x'),
             'Decision variables (1 mark); objective function (1 mark); constraints including non-negativity (1 mark).',
             [f'Maximise Z = {q}x + {p}y subject to {a1}x + {a2}y ≤ {T1}, {b1}x + {b2}y ≤ {T2}, x, y ≥ 0', f'Minimise Z = {p}x + {q}y subject to {a1}x + {b1}y ≥ {T1}, {a2}x + {b2}y ≥ {T2}, x, y ≥ 0',
              f'Maximise Z = {p}x + {q}y subject to {a1}x + {b1}y ≥ {T1}, {a2}x + {b2}y ≥ {T2}, x, y ≥ 0'])


def c12s1_diet(r):
    f1, f2 = r.sample(['Food P', 'Food Q', 'Food X', 'Food Y', 'millet mix', 'pulse mix'], 2)
    a1, b1, a2, b2 = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    N1, N2 = r.randint(8, 40), r.randint(8, 40)
    c1, c2 = r.randint(2, 9) * 5, r.randint(2, 9) * 5
    return Q(f'A dietician wants a mixture of {f1} and {f2}. One kg of {f1} contains {a1} unit{"s" if a1 != 1 else ""} of vitamin A and {a2} unit{"s" if a2 != 1 else ""} of vitamin C; one kg of {f2} contains {b1} unit{"s" if b1 != 1 else ""} of vitamin A and {b2} unit{"s" if b2 != 1 else ""} of vitamin C. '
             f'The mixture must contain at least {N1} units of vitamin A and {N2} units of vitamin C. {f1} costs ₹{c1}/kg and {f2} costs ₹{c2}/kg. Formulate the LPP to minimise cost.',
             f'Minimise Z = {c1}x + {c2}y subject to {a1}x + {b1}y ≥ {N1}, {a2}x + {b2}y ≥ {N2}, x ≥ 0, y ≥ 0'.replace(' 1x', ' x').replace(' 1y', ' y'),
             'Variables x, y = kg of each food (1 mark); objective (1 mark); constraints (1 mark).',
             [f'Maximise Z = {c1}x + {c2}y subject to {a1}x + {b1}y ≤ {N1}, {a2}x + {b2}y ≤ {N2}, x, y ≥ 0', f'Minimise Z = {c1}x + {c2}y subject to {a1}x + {a2}y ≥ {N1}, {b1}x + {b2}y ≥ {N2}, x, y ≥ 0',
              f'Minimise Z = {c2}x + {c1}y subject to {a1}x + {b1}y ≥ {N1}, {a2}x + {b2}y ≥ {N2}, x, y ≥ 0'])


def c12s1_mcq(r):
    return mcqbank([
        ('In a linear programming problem, the linear function to be optimised is called …', 'the objective function', ['a constraint', 'the feasible region', 'a decision variable'], 'Definition.'),
        ('The conditions x ≥ 0, y ≥ 0 in an LPP are called …', 'non-negative constraints', ['objective functions', 'optimal solutions', 'corner points'], 'Definition.'),
        ('In an LPP, the variables x and y are called …', 'decision variables', ['constants', 'objective functions', 'slack values'], 'Definition.'),
        ('Linear programming problems involve …', 'a linear objective function and linear constraints', ['quadratic objective functions', 'only equality constraints', 'non-linear constraints'], 'Definition.'),
        ('A problem that seeks to minimise cost is …', 'a minimisation LPP', ['a maximisation LPP', 'not an LPP', 'always unbounded'], 'Objective: minimise.'),
    ])(r)


def c12s1_ar(r):
    return arbank([
        ('In an LPP, the objective function Z = ax + by is linear.', 'In a linear programming problem, the objective function and all constraints are linear.', 'a', 'Definition.'),
        ('Z = x² + y can be the objective function of an LPP.', 'An LPP has a linear objective function.', 'd', 'x² is not linear; A false, R true.'),
        ('The constraints x ≥ 0, y ≥ 0 are included when x, y count items produced.', 'Quantities produced cannot be negative.', 'a', 'Non-negativity constraints.'),
    ])(r)


def c12s1_explain(r):
    return xbank([
        ('Explain the terms objective function, constraints and decision variables in an LPP, with an example.', 'Objective: Z = 5x + 3y to maximise; constraints: x + y ≤ 10, x, y ≥ 0; decision variables x, y.', 'Each term with example (2 marks).'),
        ('Why are non-negativity constraints always included when formulating a manufacturing LPP?', 'Numbers of items produced cannot be negative.', 'Real-world meaning of x, y (2 marks).'),
        ('Explain the difference between a feasible solution and an optimal solution of an LPP.', 'Feasible: satisfies all constraints; optimal: feasible and gives the best value of Z.', '1 mark each.'),
    ])(r)


def _one(A):
    """Singular of a product name: 'souvenirs of type A' -> 'souvenir of type A', 'cricket bats' -> 'cricket bat'."""
    head, sep, tail = A.partition(' of ')
    head = head[:-1] if head.endswith('s') else head
    return head + sep + tail


def c12s1_case(r):
    A, B, who = r.choice(PRODUCTS)
    a1, b1 = r.randint(2, 5), r.randint(2, 5)
    T = r.randint(20, 60)
    cap = r.randint(10, 30)
    p, q = r.choice([20, 30, 40, 50]), r.choice([25, 35, 45, 60])
    return Q((f'{who.capitalize()} in {r.choice(CITIES)} makes {A} (x units) and {B} (y units) per week. Each {_one(A)} takes {a1} hours of labour and each {_one(B)} takes {b1} hours; at most {T} labour hours are available. '
              f'The store can hold at most {cap} units in all. Profits are ₹{p} and ₹{q} per unit. (i) Write the objective function. (ii) Write all the constraints. (iii) Is (x, y) = (1, 1) a feasible point? Justify.'),
             f'(i) Maximise Z = {p}x + {q}y (ii) {a1}x + {b1}y ≤ {T}, x + y ≤ {cap}, x ≥ 0, y ≥ 0 (iii) Yes: {a1 + b1} ≤ {T} and 2 ≤ {cap}'.replace(' 1x', ' x').replace(' 1y', ' y'),
             '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ---- st2 graphical method

def c12s2_max(r):
    cons, V, p, q, vals = _max_lpp(r)
    best = max(vals, key=vals.get)
    ctxt = ', '.join(cons_str(*c) for c in cons) + ', x ≥ 0, y ≥ 0'
    table = '; '.join(f'Z({fz(x)}, {fz(y)}) = {fz(v)}' for (x, y), v in sorted(vals.items()))
    return Q(f'Solve the following LPP graphically: Maximise Z = {p}x + {q}y subject to {ctxt}.'.replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
             f'Maximum Z = {fz(vals[best])} at ({fz(best[0])}, {fz(best[1])})',
             f'Corner points of the bounded feasible region: {", ".join(f"({fz(x)}, {fz(y)})" for x, y in V)} (2 marks); {table} (2 marks); maximum (1 mark).')


def c12s2_corner(r):
    cons, V, p, q, vals = _max_lpp(r)
    best = max(vals, key=vals.get)
    wrong = [f'({fz(x)}, {fz(y)})' for (x, y) in V if (x, y) != best]
    return Q(f'The corner points of the feasible region of an LPP are {", ".join(f"({fz(x)}, {fz(y)})" for x, y in V)}. At which point is Z = {p}x + {q}y maximum?'.replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
             f'({fz(best[0])}, {fz(best[1])})', f'Evaluate Z at each corner: ' + '; '.join(f'({fz(x)}, {fz(y)}): {fz(v)}' for (x, y), v in sorted(vals.items())) + '.', wrong[:3])


def c12s2_vertices(r):
    cons, V, p, q, vals = _max_lpp(r)
    ctxt = ', '.join(cons_str(*c) for c in cons) + ', x ≥ 0, y ≥ 0'
    inter = [v for v in V if v[0] > 0 and v[1] > 0][0]
    return Q(f'Find the corner points of the feasible region determined by {ctxt}.'.replace(' 1x', ' x').replace(' 1y', ' y'), ', '.join(f'({fz(x)}, {fz(y)})' for x, y in V),
             f'Intercepts of the boundary lines and their intersection ({fz(inter[0])}, {fz(inter[1])}) (2 marks); keep points satisfying all constraints (1 mark).',
             [', '.join(f'({fz(y)}, {fz(x)})' for x, y in V), ', '.join(f'({fz(x)}, {fz(y)})' for x, y in V if (x, y) != inter), ', '.join(f'({fz(x)}, {fz(y)})' for x, y in V[:-1]) + f', ({fz(inter[0] + 1)}, {fz(inter[1])})'])


def c12s2_mcq(r):
    return mcqbank([
        ('Corner point theorem: if the feasible region is bounded, the objective function Z = ax + by has …', 'both a maximum and a minimum, each at a corner point', ['only a maximum', 'no optimal value', 'an optimum only at the origin'], 'Theorem 2 (NCERT).'),
        ('The common region determined by all the constraints including x, y ≥ 0 is called …', 'the feasible region', ['the infeasible region', 'the objective region', 'the optimal line'], 'Definition.'),
        ('Points within and on the boundary of the feasible region are called …', 'feasible solutions', ['optimal solutions only', 'infeasible solutions', 'corner points only'], 'Definition.'),
        ('The corner points of the feasible region of an LPP are (0, 0), (5, 0), (3, 4), (0, 6). The maximum of Z = 2x + 3y is …', '18', ['10', '17', '0'], 'Z(3, 4) = Z(0, 6) = 18 is the largest.'),
        ('The corner points of the feasible region are (0, 2), (3, 0), (6, 0), (6, 8), (0, 5). The minimum of Z = 4x + 6y occurs at …', '(0, 2)', ['(3, 0)', '(0, 5)', '(6, 0)'], 'Z: 12, 12, 24, 72, 30 — minimum 12 at (0, 2) and (3, 0), i.e. on the segment joining them.'),
    ])(r)


def c12s2_ar(r):
    cons, V, p, q, vals = _max_lpp(r)
    best = max(vals, key=vals.get)
    return arbank([
        (f'The maximum of Z = {p}x + {q}y over the bounded region with corners {", ".join(f"({fz(x)}, {fz(y)})" for x, y in V)} is {fz(vals[best])}.'.replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
         'If the feasible region is bounded, the maximum of Z occurs at a corner point.', 'a', 'Compare Z at the corners.'),
        ('The optimal value of an LPP can occur at a point inside the feasible region but not on its boundary.', 'Optimal values of Z occur at corner points of the feasible region.', 'd', 'A is false (for non-constant Z); R is true.'),
        ('A bounded feasible region of an LPP is enclosed within a circle.', 'A bounded region can be enclosed in a circle.', 'a', 'That is the definition of bounded.'),
    ])(r)


def c12s2_case(r):
    cons, V, p, q, vals = _max_lpp(r)
    A, B, who = r.choice(PRODUCTS)
    best = max(vals, key=vals.get)
    return Q((f'{who.capitalize()} makes x {A} and y {B} a day, subject to {", ".join(cons_str(*c) for c in cons)}, x, y ≥ 0. The daily profit is Z = {p}x + {q}y rupees. '
              f'(i) Find the corner points of the feasible region. (ii) Find Z at each corner point. (iii) How many of each should be made for maximum profit, and what is the maximum profit?').replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
             f'(i) {", ".join(f"({fz(x)}, {fz(y)})" for x, y in V)} (ii) ' + '; '.join(f'{fz(v)}' for _, v in sorted(vals.items())) + f' (iii) {fz(best[0])} {A} and {fz(best[1])} {B}; ₹{fz(vals[best])}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ---- st3 bounded/unbounded, multiple optima

def _min_lpp(r, tries=300):
    for _ in range(tries):
        a1, b1, a2, b2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
        x0, y0 = r.randint(1, 8), r.randint(1, 8)
        c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
        cons = [(a1, b1, c1, '>='), (a2, b2, c2, '>=')]
        V = lpp_vertices(cons)
        if len(V) == 3 and all(x.denominator == 1 and y.denominator == 1 for x, y in V):
            p, q = r.randint(1, 9), r.randint(1, 9)
            vals = {v: p * v[0] + q * v[1] for v in V}
            m = min(vals.values())
            if sum(1 for v in vals.values() if v == m) == 1:
                return cons, V, p, q, vals
    raise ValueError


def c12s3_min(r):
    cons, V, p, q, vals = _min_lpp(r)
    best = min(vals, key=vals.get)
    m = vals[best]
    ctxt = ', '.join(cons_str(*c) for c in cons) + ', x ≥ 0, y ≥ 0'
    return Q(f'Minimise Z = {p}x + {q}y subject to {ctxt}, using the graphical method.'.replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
             f'Minimum Z = {fz(m)} at ({fz(best[0])}, {fz(best[1])})',
             f'The feasible region is unbounded with corners {", ".join(f"({fz(x)}, {fz(y)})" for x, y in V)} (1 mark); Z values {", ".join(fz(v) for _, v in sorted(vals.items()))} (2 marks); '
             f'the half-plane {p}x + {q}y < {fz(m)} has no point in common with the region, so {fz(m)} is the minimum (2 marks).'.replace(' 1x', ' x').replace(' 1y', ' y'))


def c12s3_unb(r):
    cons, V, p, q, vals = _min_lpp(r)
    ctxt = ', '.join(cons_str(*c) for c in cons) + ', x ≥ 0, y ≥ 0'
    return Q(f'For the feasible region given by {ctxt}, does Z = {p}x + {q}y have a maximum value? Give a reason.'.replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'), 'No maximum',
             'The region is unbounded and Z increases without bound along it (e.g. along the x-axis), so no maximum exists.', ['Yes, at the largest corner point', 'Yes, at the origin', 'Yes, at every corner'])


def c12s3_multi(r):
    for _ in range(200):
        cons, V, p, q, vals = _max_lpp(r)
        k = r.choice([1, 2, 3, 5, 10])
        a, b, c, s = cons[r.randint(0, 1)]
        vals2 = {v: k * (a * v[0] + b * v[1]) for v in V}
        best = max(vals2.values())
        top = [v for v, z in vals2.items() if z == best]
        if len(top) == 2:
            ctxt = ', '.join(cons_str(*cc) for cc in cons) + ', x ≥ 0, y ≥ 0'
            pts = ' and '.join(f'({fz(x)}, {fz(y)})' for x, y in top)
            return Q(f'Maximise Z = {k * a}x + {k * b}y subject to {ctxt}. Comment on the optimal solution.'.replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
                     f'Maximum Z = {fz(best)} at both {pts}, hence at every point of the segment joining them (infinitely many optimal solutions)',
                     f'Corner values {", ".join(fz(v) for _, v in sorted(vals2.items()))} (3 marks); equal maxima at two adjacent corners ⇒ multiple optima (2 marks).')
    raise ValueError


def c12s3_infeas(r):
    a, b = r.randint(1, 4), r.randint(1, 4)
    c = r.randint(2, 8)
    d = c + r.randint(2, 8)
    return Q(f'Show that the LPP: Maximise Z = x + y subject to {a}x + {b}y ≤ {c}, {a}x + {b}y ≥ {d}, x, y ≥ 0 has no feasible solution.'.replace(' 1x', ' x').replace(' 1y', ' y'), 'The feasible region is empty',
             f'{term(a, "x", first=True)}{term(b, "y")} cannot be both ≤ {c} and ≥ {d}; the two half-planes do not overlap (2 marks).', ['A unique optimal solution', 'Infinitely many optimal solutions', 'An unbounded maximum'])


def c12s3_mcq(r):
    return mcqbank([
        ('If the feasible region of an LPP is unbounded, then a maximum or minimum of Z …', 'may not exist', ['always exists', 'never exists', 'is always at the origin'], 'Theorem 2 needs a bounded region.'),
        ('If two corner points of the feasible region give the same maximum value of Z, then …', 'every point on the segment joining them is optimal', ['the LPP has no solution', 'only those two points are optimal', 'the region is unbounded'], 'Multiple optimal solutions.'),
        ('An LPP whose feasible region is empty is said to have …', 'no feasible solution', ['infinitely many solutions', 'a unique solution', 'an unbounded solution'], 'Infeasible.'),
        ('For an unbounded region, M is the maximum value of Z = ax + by if the open half-plane ax + by > M …', 'has no point in common with the feasible region', ['contains the feasible region', 'passes through the origin', 'touches every corner'], 'NCERT test.'),
        ('The feasible region of x + y ≥ 4, x, y ≥ 0 is …', 'unbounded', ['bounded', 'empty', 'a single point'], 'It extends to infinity.'),
    ])(r)


def c12s3_ar(r):
    return arbank([
        ('The LPP: Maximise Z = x + y subject to x + y ≥ 2, x, y ≥ 0 has no maximum.', 'The feasible region is unbounded and Z can be made as large as we like.', 'a', 'R explains A.'),
        ('Every LPP with an unbounded feasible region has no optimal solution.', 'A minimum of Z = ax + by (a, b > 0) over an unbounded region can still exist.', 'd', 'A is false; R is true.'),
        ('If Z = 3x + 6y takes the same maximum value at (0, 4) and (2, 3), then all points on the segment joining them are optimal.', 'The line Z = M through both points is parallel to an edge of the region.', 'a', 'Multiple optima along the edge.'),
    ])(r)


def c12s3_case(r):
    cons, V, p, q, vals = _min_lpp(r)
    best = min(vals, key=vals.get)
    who = name(r)
    return Q((f'{who}, a hostel warden, mixes two cereals so that the vitamin and mineral needs are met: {", ".join(cons_str(*c) for c in cons)}, x, y ≥ 0 (x, y in kg). The cost is Z = {p}x + {q}y rupees. '
              f'(i) Is the feasible region bounded or unbounded? (ii) Find its corner points. (iii) Find the minimum cost and explain why it really is the minimum.').replace(' 1x', ' x').replace(' 1y', ' y').replace('= 1x', '= x'),
             f'(i) unbounded (ii) {", ".join(f"({fz(x)}, {fz(y)})" for x, y in V)} (iii) ₹{fz(vals[best])} at ({fz(best[0])}, {fz(best[1])}); the half-plane {p}x + {q}y < {fz(vals[best])} has no common point with the region'.replace(' 1x', ' x').replace(' 1y', ' y'),
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch13 Probability

DICE2 = [(a, b) for a in range(1, 7) for b in range(1, 7)]
COINS3 = list(itertools.product('HT', repeat=3))
EV2 = [
    ('the sum of the numbers is {k}', lambda o, k: o[0] + o[1] == k, range(4, 11)),
    ('the sum of the numbers is at least {k}', lambda o, k: o[0] + o[1] >= k, range(6, 11)),
    ('the first die shows {k}', lambda o, k: o[0] == k, range(1, 7)),
    ('at least one die shows {k}', lambda o, k: k in o, range(1, 7)),
    ('the numbers are different', lambda o, k: o[0] != o[1], [0]),
    ('the sum is even', lambda o, k: (o[0] + o[1]) % 2 == 0, [0]),
    ('the product of the numbers is a multiple of {k}', lambda o, k: (o[0] * o[1]) % k == 0, [2, 3, 4, 6]),
    ('both numbers are greater than {k}', lambda o, k: o[0] > k and o[1] > k, [1, 2, 3, 4]),
    ('the first number is less than the second', lambda o, k: o[0] < o[1], [0]),
]
EV3 = [
    ('at least two heads appear', lambda o, k: o.count('H') >= 2, [0]),
    ('the first coin shows a head', lambda o, k: o[0] == 'H', [0]),
    ('exactly one tail appears', lambda o, k: o.count('T') == 1, [0]),
    ('at most one head appears', lambda o, k: o.count('H') <= 1, [0]),
    ('the last coin shows a tail', lambda o, k: o[2] == 'T', [0]),
    ('all three coins show the same face', lambda o, k: len(set(o)) == 1, [0]),
    ('at least one head appears', lambda o, k: 'H' in o, [0]),
]


def _ev(r, lib):
    t, f, ks = r.choice(lib)
    k = r.choice(list(ks))
    return t.format(k=k), (lambda o, f=f, k=k: f(o, k))


def c13s1_dice(r):
    space, lib, what = r.choice([(DICE2, EV2, 'A pair of dice is thrown'), (COINS3, EV3, 'Three fair coins are tossed')])
    for _ in range(50):
        (ta, fa), (tb, fb) = _ev(r, lib), _ev(r, lib)
        if ta == tb:
            continue
        nb = sum(1 for o in space if fb(o))
        nab = sum(1 for o in space if fa(o) and fb(o))
        if nb and 0 < nab < nb:
            p = Fr(nab, nb)
            na = sum(1 for o in space if fa(o))
            return Q(f'{what}. Find the probability that {ta}, given that {tb}.', fz(p), f'n(B) = {nb}, n(A ∩ B) = {nab}; P(A|B) = {nab}/{nb}' + (f' = {fz(p)}.' if Fr(nab, nb).denominator != nb else '.'),
                     dist3(fz(p), [fz(Fr(nab, len(space))), fz(Fr(na, len(space))), fz(Fr(nab, na)) if na else '1/2', fz(Fr(nb - nab, nb))]))
    raise ValueError


def c13s1_formula(r):
    while True:
        pb = Fr(r.randint(2, 9), 10)
        pab = Fr(r.randint(1, 9), 20)
        if pab < pb:
            break
    pa = pab + Fr(r.randint(0, 6), 20)
    if pa > 1 or pa < pab or pa + pb - pab > 1:
        raise ValueError
    kind = r.randint(0, 1)
    if kind == 0:
        return Q(f'If P(A) = {fz(pa)}, P(B) = {fz(pb)} and P(A ∩ B) = {fz(pab)}, find P(A|B) and P(B|A).', f'P(A|B) = {fz(pab / pb)}, P(B|A) = {fz(pab / pa)}',
                 'P(A|B) = P(A ∩ B)/P(B); P(B|A) = P(A ∩ B)/P(A).', [f'P(A|B) = {fz(pab / pa)}, P(B|A) = {fz(pab / pb)}', f'P(A|B) = {fz(pab)}, P(B|A) = {fz(pab)}', f'P(A|B) = {fz(pa * pb)}, P(B|A) = {fz(pa / pb) if pa < pb else fz(pb)}'])
    pu = pa + pb - pab
    return Q(f'Given P(A) = {fz(pa)}, P(B) = {fz(pb)} and P(A ∪ B) = {fz(pu)}, find P(A|B).', fz(pab / pb), f'P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = {fz(pab)}; P(A|B) = ({fz(pab)})/({fz(pb)}) = {fz(pab / pb)}.',
             dist3(fz(pab / pb), [fz(pab), fz(pu / pb) if pu < pb else fz(pab / pu), fz(pab / pa)]))


def c13s1_family(r):
    kind = r.randint(0, 2)
    if kind == 0:
        return Q('A family has two children. What is the probability that both the children are boys, given that at least one of them is a boy?', '1/3',
                 'S = {BB, BG, GB, GG}; at least one boy: {BB, BG, GB}; P = 1/3.', ['1/2', '1/4', '2/3'])
    if kind == 1:
        return Q('A family has two children. What is the probability that both the children are boys, given that the elder child is a boy?', '1/2', 'Given {BB, BG}: P(BB) = 1/2.', ['1/3', '1/4', '2/3'])
    n = r.choice([10, 20, 30, 40, 50])
    k = r.choice([2, 3, 4, 5])
    ev = [x for x in range(1, n + 1) if x % 2 == 0]
    mk = [x for x in ev if x % k == 0]
    return Q(f'A number is chosen at random from 1 to {n}. Given that it is even, find the probability that it is divisible by {k}.', fz(Fr(len(mk), len(ev))),
             f'{len(ev)} even numbers, of which {len(mk)} are divisible by {k}.', dist3(fz(Fr(len(mk), len(ev))), [fz(Fr(len(mk), n)), fz(Fr(n // k, n)), fz(Fr(len(mk) + 1, len(ev)))]))


def c13s1_mcq(r):
    return mcqbank([
        ('If P(B) ≠ 0, then P(A|B) = …', 'P(A ∩ B)/P(B)', ['P(A ∩ B)/P(A)', 'P(A)P(B)', 'P(A) + P(B)'], 'Definition.'),
        ('P(S|F) = …, where S is the sample space and P(F) ≠ 0', '1', ['0', 'P(F)', 'P(S)'], 'Property 1.'),
        ('P(A′|B) = …', '1 − P(A|B)', ['P(A|B)', '1 − P(B|A)', 'P(A′)'], 'Property 3.'),
        ('If A and B are mutually exclusive with P(B) ≠ 0, then P(A|B) = …', '0', ['1', 'P(A)', 'P(A)/P(B)'], 'A ∩ B = φ.'),
        ('If A ⊂ B and P(B) ≠ 0, then P(A|B) = …', 'P(A)/P(B)', ['P(B)/P(A)', '1', 'P(A)'], 'A ∩ B = A.'),
        ('P((A ∪ B)|F) = …', 'P(A|F) + P(B|F) − P((A ∩ B)|F)', ['P(A|F) + P(B|F)', 'P(A|F)P(B|F)', 'P(A ∪ B)/P(F) − 1'], 'Property 2.'),
    ])(r)


def c13s1_ar(r):
    pb = Fr(r.randint(2, 8), 10)
    pab = pb * Fr(r.randint(1, 4), 5)
    return arbank([
        (f'If P(B) = {fz(pb)} and P(A ∩ B) = {fz(pab)}, then P(A|B) = {fz(pab / pb)}.', 'P(A|B) = P(A ∩ B)/P(B) when P(B) ≠ 0.', 'a', 'Direct use of R.'),
        ('P(A|B) = P(B|A) for all events A and B.', 'P(A ∩ B) = P(B ∩ A).', 'd', 'P(A|B) = P(A ∩ B)/P(B) and P(B|A) = P(A ∩ B)/P(A) differ unless P(A) = P(B); A false, R true.'),
        ('P(A|A) = 1 when P(A) ≠ 0.', 'P(A ∩ A)/P(A) = P(A)/P(A).', 'a', 'R computes A.'),
    ])(r)


def c13s1_case(r):
    n1, n2 = r.randint(20, 60), r.randint(20, 60)
    g1, g2 = r.randint(5, n1 - 5), r.randint(5, n2 - 5)
    tot = n1 + n2
    city = r.choice(CITIES)
    return Q((f'In a school in {city}, {n1} students of Class XII opted for Mathematics and {n2} for Applied Mathematics (no student took both). Of these, {g1} and {g2} respectively are girls. '
              f'A student is chosen at random. (i) Find the probability that the student is a girl. (ii) Find the probability that the student opted for Mathematics, given that the student is a girl. '
              f'(iii) Find the probability that the student is a girl, given that the student opted for Applied Mathematics.'),
             f'(i) {fz(Fr(g1 + g2, tot))} (ii) {fz(Fr(g1, g1 + g2))} (iii) {fz(Fr(g2, n2))}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ---- st2 multiplication theorem and independence

def c13s2_indep(r):
    pa, pb = Fr(r.randint(1, 9), 10), Fr(r.randint(1, 9), 10)
    kind = r.randint(0, 2)
    if kind == 0:
        pu = pa + pb - pa * pb
        return Q(f'A and B are independent events with P(A) = {fz(pa)} and P(B) = {fz(pb)}. Find P(A ∪ B) and P(A′ ∩ B′).', f'P(A ∪ B) = {fz(pu)}, P(A′ ∩ B′) = {fz(1 - pu)}',
                 f'P(A ∩ B) = P(A)P(B) = {fz(pa * pb)}; P(A ∪ B) = {fz(pu)}; P(A′ ∩ B′) = (1 − P(A))(1 − P(B)) = {fz(1 - pu)}.',
                 [f'P(A ∪ B) = {fz(min(pa + pb, Fr(1)))}, P(A′ ∩ B′) = {fz(1 - min(pa + pb, Fr(1)))}', f'P(A ∪ B) = {fz(pa * pb)}, P(A′ ∩ B′) = {fz(1 - pa * pb)}', f'P(A ∪ B) = {fz(pu)}, P(A′ ∩ B′) = {fz(pu)}' if pu != 1 - pu else f'P(A ∪ B) = {fz(pu)}, P(A′ ∩ B′) = 0'])
    if kind == 1:
        who1, who2 = two_names(r)
        p = 1 - (1 - pa) * (1 - pb)
        return Q(f'The probabilities that {who1} and {who2} can solve a problem independently are {fz(pa)} and {fz(pb)}. Find the probability that the problem is solved.', fz(p),
                 f'P(solved) = 1 − P(neither) = 1 − ({fz(1 - pa)})({fz(1 - pb)}) = {fz(p)}.', dist3(fz(p), [fz(min(pa + pb, Fr(1))), fz(pa * pb), fz((1 - pa) * (1 - pb)), fz(p - Fr(1, 20))]))
    pab = pa * pb if r.random() < 0.5 else pa * pb + Fr(1, 100) * r.choice([-2, -1, 1, 2, 3])
    if pab <= 0 or pab > min(pa, pb):
        raise ValueError
    ind = pab == pa * pb
    return Q(f'Given P(A) = {fz(pa)}, P(B) = {fz(pb)} and P(A ∩ B) = {fz(pab)}, are A and B independent? Justify.', 'Yes' if ind else 'No',
             f'P(A)P(B) = {fz(pa * pb)} {"=" if ind else "≠"} P(A ∩ B).', ['No' if ind else 'Yes', 'Only if they are mutually exclusive', 'Cannot be decided'])


def c13s2_draw(r):
    a, b = r.randint(3, 9), r.randint(3, 9)
    kind = r.randint(0, 2)
    c1, c2 = r.sample(['red', 'black', 'white', 'green', 'blue', 'yellow'], 2)
    n = a + b
    if kind == 0:
        p = Fr(a, n) * Fr(a - 1, n - 1)
        return Q(f'A bag contains {a} {c1} and {b} {c2} balls. Two balls are drawn at random one after the other without replacement. Find the probability that both are {c1}.', fz(p),
                 f'P = {a}/{n} × {a - 1}/{n - 1} = {fz(p)} (multiplication theorem).', dist3(fz(p), [fz(Fr(a * a, n * n)), fz(Fr(a, n) * Fr(a - 1, n)), fz(Fr(a * (a - 1), n * (n - 1)) * 2)]))
    if kind == 1:
        p = Fr(a, n) * Fr(b, n - 1)
        return Q(f'A bag contains {a} {c1} and {b} {c2} balls. Two balls are drawn one after the other without replacement. Find the probability that the first is {c1} and the second is {c2}.', fz(p),
                 f'P = {a}/{n} × {b}/{n - 1} = {fz(p)}.', dist3(fz(p), [fz(Fr(a * b, n * n)), fz(2 * p), fz(Fr(a, n) * Fr(b, n))]))
    p = Fr(a, n) * Fr(a, n)
    return Q(f'A bag contains {a} {c1} and {b} {c2} balls. Two balls are drawn one after the other with replacement. Find the probability that both are {c1}.', fz(p),
             f'Independent draws: ({a}/{n})² = {fz(p)}.', dist3(fz(p), [fz(Fr(a, n) * Fr(a - 1, n - 1)), fz(Fr(2 * a, n)), fz(Fr(a, n))]))


def c13s2_cards(r):
    kind = r.randint(0, 2)
    if kind == 0:
        return Q('Three cards are drawn successively, without replacement, from a pack of 52 well-shuffled cards. What is the probability that the first two are kings and the third is an ace?', '2/5525',
                 '4/52 × 3/51 × 4/50 = 2/5525.', ['1/2197', '4/5525', '1/5525'])
    if kind == 1:
        return Q('A card is drawn from a well-shuffled pack of 52 cards. E: the card is a spade; F: the card is an ace. Are E and F independent?', 'Yes',
                 'P(E) = 1/4, P(F) = 1/13, P(E ∩ F) = 1/52 = P(E)P(F).', ['No', 'They are mutually exclusive', 'Cannot be decided'])
    return Q('A die is thrown. E: the number is a multiple of 3; F: the number is even. Are E and F independent?', 'Yes', 'P(E) = 1/3, P(F) = 1/2, P(E ∩ F) = P({6}) = 1/6 = P(E)P(F).', ['No', 'They are mutually exclusive', 'Only if the die is biased'])


def c13s2_mcq(r):
    return mcqbank([
        ('Events A and B are independent if …', 'P(A ∩ B) = P(A)P(B)', ['P(A ∩ B) = 0', 'P(A ∪ B) = P(A) + P(B)', 'P(A|B) = P(B)'], 'Definition.'),
        ('If A and B are independent, then A′ and B′ are …', 'independent', ['mutually exclusive', 'exhaustive', 'dependent'], 'Theorem.'),
        ('Two events with non-zero probabilities that are mutually exclusive …', 'cannot be independent', ['are always independent', 'have P(A ∩ B) = P(A)P(B)', 'are exhaustive'], 'P(A ∩ B) = 0 ≠ P(A)P(B).'),
        ('By the multiplication theorem, P(A ∩ B) = …', 'P(A)P(B|A)', ['P(A) + P(B|A)', 'P(A|B)P(A)', 'P(A)/P(B)'], 'For P(A) ≠ 0.'),
        ('If A and B are independent with P(A) = 0.3 and P(B) = 0.4, then P(A ∩ B) = …', '0.12', ['0.7', '0.1', '0.58'], '0.3 × 0.4.'),
    ])(r)


def c13s2_ar(r):
    pa, pb = Fr(r.randint(1, 9), 10), Fr(r.randint(1, 9), 10)
    return arbank([
        (f'If A and B are independent with P(A) = {fz(pa)} and P(B) = {fz(pb)}, then P(A ∩ B) = {fz(pa * pb)}.', 'For independent events, P(A ∩ B) = P(A)P(B).', 'a', 'Definition.'),
        (f'If A and B are mutually exclusive with P(A) = {fz(pa)} and P(B) = {fz(pb)}, they are independent.', 'Mutually exclusive events have P(A ∩ B) = 0.', 'd', f'P(A)P(B) = {fz(pa * pb)} ≠ 0; A false, R true.'),
        ('If A and B are independent, then P(A|B) = P(A).', 'P(A|B) = P(A ∩ B)/P(B) = P(A)P(B)/P(B).', 'a', 'R derives A.'),
    ])(r)


def c13s2_case(r):
    pa, pb, pc = Fr(r.randint(5, 9), 10), Fr(r.randint(4, 9), 10), Fr(r.randint(3, 8), 10)
    who = r.sample(['Ananya', 'Kabir', 'Meera', 'Rohan', 'Diya', 'Arjun', 'Ishita', 'Farhan'], 3)
    return Q((f'In a school archery event, {who[0]}, {who[1]} and {who[2]} hit the target independently with probabilities {fz(pa)}, {fz(pb)} and {fz(pc)}. '
              f'(i) Find the probability that all three hit the target. (ii) Find the probability that none hits. (iii) Find the probability that at least one hits.'),
             f'(i) {fz(pa * pb * pc)} (ii) {fz((1 - pa) * (1 - pb) * (1 - pc))} (iii) {fz(1 - (1 - pa) * (1 - pb) * (1 - pc))}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c13s2_long(r):
    a, b = r.randint(3, 8), r.randint(3, 8)
    pa, pb = Fr(r.randint(2, 8), 10), Fr(r.randint(2, 8), 10)
    p_only_one = pa * (1 - pb) + pb * (1 - pa)
    return Q(f'A and B appear for an interview for two vacancies independently. The probability of A\'s selection is {fz(pa)} and of B\'s selection is {fz(pb)}. Find the probability that (i) both are selected (ii) only one of them is selected (iii) none is selected (iv) at least one is selected.',
             f'(i) {fz(pa * pb)} (ii) {fz(p_only_one)} (iii) {fz((1 - pa) * (1 - pb))} (iv) {fz(1 - (1 - pa) * (1 - pb))}', '(i) 1 mark (ii) 2 marks (iii) 1 mark (iv) 1 mark.')


# ---- st3 total probability and Bayes

def c13s3_bags(r):
    r1, b1, r2, b2 = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    c1, c2 = r.sample(['red', 'black', 'white', 'green', 'blue'], 2)
    pr = Fr(1, 2) * Fr(r1, r1 + b1) + Fr(1, 2) * Fr(r2, r2 + b2)
    post = Fr(1, 2) * Fr(r1, r1 + b1) / pr
    kind = r.randint(0, 1)
    if kind == 0:
        return Q(f'Bag I contains {r1} {c1} and {b1} {c2} balls, and Bag II contains {r2} {c1} and {b2} {c2} balls. One bag is chosen at random and a ball drawn from it is {c1}. Find the probability that it was drawn from Bag I.',
                 fz(post), f'P(E₁) = P(E₂) = 1/2; P(A|E₁) = {fz(Fr(r1, r1 + b1))}, P(A|E₂) = {fz(Fr(r2, r2 + b2))} (1 mark); P(A) = {fz(pr)} by total probability (1 mark); Bayes: P(E₁|A) = {fz(post)} (1 mark).',
                 dist3(fz(post), [fz(Fr(r1, r1 + b1)), fz(1 - post), fz(Fr(r1, r1 + r2)), fz(pr)]))
    return Q(f'Bag I contains {r1} {c1} and {b1} {c2} balls, and Bag II contains {r2} {c1} and {b2} {c2} balls. A bag is chosen at random and one ball is drawn. Find the probability that the ball is {c1}.',
             fz(pr), f'Theorem of total probability: ½({fz(Fr(r1, r1 + b1))}) + ½({fz(Fr(r2, r2 + b2))}) = {fz(pr)}.', dist3(fz(pr), [fz(Fr(r1 + r2, r1 + b1 + r2 + b2)), fz(post), fz(Fr(r1, r1 + b1) * Fr(r2, r2 + b2))]))


def c13s3_machines(r):
    while True:
        s = sorted(r.sample(range(10, 90, 5), 2))
        shares = [s[0], s[1] - s[0], 100 - s[1]]
        if min(shares) >= 10:
            break
    defects = [r.choice([1, 2, 3, 4, 5]) for _ in range(3)]
    P = [Fr(x, 100) for x in shares]
    D = [Fr(d, 100) for d in defects]
    tot = sum(p * d for p, d in zip(P, D))
    k = r.randint(0, 2)
    post = P[k] * D[k] / tot
    names = r.choice([('A', 'B', 'C'), ('E₁', 'E₂', 'E₃'), ('X', 'Y', 'Z')])
    city = r.choice(CITIES)
    return Q(f'A factory in {city} has three machines {names[0]}, {names[1]} and {names[2]} which produce {shares[0]}%, {shares[1]}% and {shares[2]}% of the bolts, of which {defects[0]}%, {defects[1]}% and {defects[2]}% respectively are defective. '
             f'A bolt drawn at random is found to be defective. What is the probability that it was produced by machine {names[k]}?', fz(post),
             f'P(D) = Σ P(Eᵢ)P(D|Eᵢ) = {fz(tot)} (2 marks); P({names[k]}|D) = ({fz(P[k])} × {fz(D[k])})/({fz(tot)}) = {fz(post)} (2 marks); identification of events (1 mark).',
             dist3(fz(post), [fz(P[k]), fz(D[k]), fz(tot), fz(P[k] * D[k])]))


def _pct(x):
    v = Fr(x) * 100
    return fz(v) if v.denominator == 1 else ('%g' % float(v))


def c13s3_test(r):
    prev = r.choice([Fr(1, 1000), Fr(1, 100), Fr(1, 200), Fr(1, 50), Fr(1, 10)])
    sens = r.choice([Fr(99, 100), Fr(95, 100), Fr(9, 10), Fr(98, 100)])
    fp = r.choice([Fr(1, 100), Fr(5, 1000), Fr(2, 100), Fr(5, 100)])
    tot = prev * sens + (1 - prev) * fp
    post = prev * sens / tot
    return Q(f'A blood test is {_pct(sens)}% effective in detecting a certain disease when it is present, but it also gives a false positive for {_pct(fp)}% of healthy people tested. '
             f'If {_pct(prev)}% of the population has the disease, find the probability that a person who tests positive actually has the disease.', fz(post),
             f'P(positive) = ({fz(prev)})({fz(sens)}) + ({fz(1 - prev)})({fz(fp)}) = {fz(tot)} (2 marks); Bayes: {fz(post)} (3 marks).', dist3(fz(post), [fz(sens), fz(prev * sens), fz(tot), fz(1 - post)]))


def c13s3_mcq(r):
    return mcqbank([
        ('If E₁, E₂, …, Eₙ form a partition of S and A is any event, then P(A) = …', 'Σ P(Eᵢ)P(A|Eᵢ)', ['Σ P(A|Eᵢ)', 'Π P(Eᵢ)', 'P(A|E₁)'], 'Theorem of total probability.'),
        ('In Bayes\' theorem, the probabilities P(Eᵢ) are called …', 'prior (a priori) probabilities', ['posterior probabilities', 'conditional probabilities of A', 'likelihoods'], 'Terminology.'),
        ('In Bayes\' theorem, the probabilities P(Eᵢ|A) are called …', 'posterior probabilities', ['prior probabilities', 'total probabilities', 'independent probabilities'], 'Terminology.'),
        ('Events E₁, E₂, E₃ form a partition of S if they are …', 'pairwise disjoint, exhaustive and have non-zero probabilities', ['independent', 'equally likely only', 'complementary'], 'Definition.'),
        ('Bayes\' theorem is used to find …', 'the probability of a cause given an observed effect', ['the probability of an effect given its cause only', 'the mean of a distribution', 'the number of outcomes'], 'Reverse (inverse) probability.'),
    ])(r)


def c13s3_ar(r):
    return arbank([
        ('If a ball drawn is red, the probability that it came from the bag with more red balls is higher.', 'By Bayes\' theorem, the posterior probability is proportional to P(Eᵢ)P(A|Eᵢ).', 'a', 'With equal priors, the larger likelihood gives the larger posterior.'),
        ('The posterior probabilities P(E₁|A), …, P(Eₙ|A) always add to 1.', 'E₁, …, Eₙ form a partition of the sample space.', 'a', 'Given A, exactly one Eᵢ occurs.'),
        ('In Bayes\' theorem the events E₁, E₂, …, Eₙ must be independent.', 'In Bayes\' theorem the events E₁, …, Eₙ must form a partition of S.', 'd', 'A partition (disjoint, exhaustive) is needed, not independence; A false, R true.'),
    ])(r)


def c13s3_case(r):
    pa = Fr(r.choice([1, 2, 3, 4]), 10)
    who = name(r)
    modes = [('train', Fr(3, 10), Fr(1, 4)), ('bus', Fr(1, 5), Fr(1, 3)), ('scooter', Fr(1, 10), Fr(1, 12)), ('other means', Fr(2, 5), Fr(0))]
    m = r.sample(modes[:3], 3)
    probs = [Fr(r.randint(1, 4), 10) for _ in range(3)]
    probs[2] = 1 - probs[0] - probs[1]
    if probs[2] <= 0:
        raise ValueError
    late = [Fr(r.randint(1, 5), 12) for _ in range(3)]
    tot = sum(p * l for p, l in zip(probs, late))
    post = probs[0] * late[0] / tot
    return Q((f'{who}, a doctor, visits a patient by {m[0][0]}, {m[1][0]} or {m[2][0]} with probabilities {fz(probs[0])}, {fz(probs[1])} and {fz(probs[2])}. The probabilities of being late are {fz(late[0])}, {fz(late[1])} and {fz(late[2])} respectively. '
              f'(i) Find the probability that {who} is late. (ii) If {who} is late, find the probability of having come by {m[0][0]}. (iii) Which mode is most likely, given that {who} is late?'),
             f'(i) {fz(tot)} (ii) {fz(post)} (iii) ' + max(zip([x[0] for x in m], [p * l / tot for p, l in zip(probs, late)]), key=lambda t: t[1])[0],
             '(i) total probability (1 mark) (ii) Bayes (2 marks) (iii) compare posteriors (1 mark).')


# ---- st4 random variables and mean

def c13s4_coins(r):
    n = r.choice([2, 3, 4])
    obj = r.choice(['heads', 'tails'])
    dist = [Fr(math.comb(n, k), 2 ** n) for k in range(n + 1)]
    table = ', '.join(f'P(X = {k}) = {fz(p)}' for k, p in enumerate(dist))
    return Q(f'A fair coin is tossed {n} times. Let X be the number of {obj}. Find the probability distribution of X and its mean.', f'{table}; mean = {fz(Fr(n, 2))}',
             f'Count outcomes with k {obj} among 2{"²³⁴"[n - 2]} = {2 ** n} (2 marks); E(X) = Σ x P(x) = {fz(Fr(n, 2))} (1 mark).', None)


def c13s4_k(r):
    n = r.choice([3, 4, 5])
    w = [r.randint(1, 4) for _ in range(n)]
    k = Fr(1, sum(w))
    xs = list(range(n))
    mean = sum(x * wi * k for x, wi in zip(xs, w))
    table = ', '.join(f'P(X = {x}) = {"" if wi == 1 else wi}k' for x, wi in zip(xs, w))
    return Q(f'A random variable X has the probability distribution {table}. Find k and the mean of X.', f'k = {fz(k)}, mean = {fz(mean)}',
             f'Σ P = {sum(w)}k = 1 ⇒ k = {fz(k)} (1 mark); E(X) = Σ x P(x) = {fz(mean)} (1 mark).', [f'k = {fz(k)}, mean = {fz(mean + Fr(1, 2))}', f'k = {sum(w)}, mean = {fz(mean * sum(w) * sum(w))}', f'k = {fz(Fr(1, n))}, mean = {fz(Fr(n - 1, 2))}'])


def c13s4_draw(r):
    a, b = r.randint(2, 6), r.randint(3, 8)
    c1, c2 = r.choice([('red', 'white'), ('white', 'red'), ('black', 'green'), ('green', 'black'), ('red', 'black'), ('defective', 'good'), ('good', 'defective')])
    n = a + b
    dist = [Fr(math.comb(a, k) * math.comb(b, 2 - k), math.comb(n, 2)) for k in range(3)]
    mean = sum(k * p for k, p in enumerate(dist))
    item = 'bulbs' if 'defective' in (c1, c2) or 'good' in (c1, c2) else 'balls'
    return Q(f'Two {item} are drawn at random without replacement from a box of {a} {c1} and {b} {c2} {item}. Let X be the number of {c1} {item} drawn. Find the probability distribution of X and E(X).',
             f'P(X = 0) = {fz(dist[0])}, P(X = 1) = {fz(dist[1])}, P(X = 2) = {fz(dist[2])}; E(X) = {fz(mean)}',
             f'P(X = k) = ᵃCₖ × ᵇC₂₋ₖ / ⁿC₂ (3 marks); E(X) = {fz(mean)} (2 marks).')


def c13s4_dice(r):
    kind = r.randint(0, 2)
    if kind == 0:
        dist = {}
        for a, b in DICE2:
            m = max(a, b)
            dist[m] = dist.get(m, 0) + 1
        mean = Fr(sum(k * v for k, v in dist.items()), 36)
        return Q('Two dice are thrown. Let X denote the larger of the two numbers obtained. Find the mean of X.', fz(mean), 'P(X = k) = (2k − 1)/36 for k = 1, …, 6; E(X) = Σ k(2k − 1)/36 = 161/36.', ['7/2', '7', '91/36'])
    if kind == 1:
        return Q('Two dice are thrown. Let X be the sum of the numbers. Find E(X).', '7', 'E(X) = 2 × 7/2 = 7, or Σ x P(x) over 2 to 12.', ['6', '7/2', '12'])
    n = r.choice([6, 8, 10, 12])
    return Q(f'A fair die with faces numbered 1 to {n} is rolled. Let X be the number shown. Find E(X).', fz(Fr(n + 1, 2)), f'E(X) = (1 + 2 + … + {n})/{n} = {fz(Fr(n + 1, 2))}.', [str(n // 2), fz(Fr(n, 2) + 1), fz(Fr(n * (n + 1), 2))])


def c13s4_mcq(r):
    return mcqbank([
        ('A random variable is …', 'a real-valued function whose domain is the sample space', ['a number that never changes', 'an event of the sample space', 'the probability of an event'], 'Definition.'),
        ('For a probability distribution, Σ P(X = xᵢ) = …', '1', ['0', 'the mean', 'the number of outcomes'], 'Total probability.'),
        ('The mean of a random variable X is also called …', 'the expectation E(X)', ['the variance', 'the median', 'the mode'], 'Terminology.'),
        ('The mean of the number obtained on throwing a fair die is …', '7/2', ['3', '6', '21'], '(1 + … + 6)/6.'),
        ('Which of these can be a probability distribution of X taking values 0, 1, 2?', '0.4, 0.4, 0.2', ['0.5, 0.6, −0.1', '0.3, 0.3, 0.3', '0.6, 0.5, 0.1'], 'Non-negative values adding to 1.'),
    ])(r)


def c13s4_ar(r):
    n = r.choice([2, 3, 4])
    return arbank([
        (f'If X is the number of heads in {n} tosses of a fair coin, E(X) = {fz(Fr(n, 2))}.', 'E(X) = Σ xᵢ P(X = xᵢ).', 'a', 'Direct computation gives n/2.'),
        ('P(X = 0) = 0.6, P(X = 1) = 0.5 is a probability distribution.', 'Probabilities in a distribution must add up to 1.', 'd', '0.6 + 0.5 = 1.1; A false, R true.'),
        ('The mean of a random variable need not be one of its values.', 'E(X) is a weighted average of the values of X.', 'a', 'e.g. 7/2 for a die.'),
    ])(r)


def c13s4_case(r):
    prizes = sorted(r.sample([0, 10, 20, 50, 100, 200, 500], 3))
    w = [r.randint(2, 8) for _ in range(3)]
    tot = sum(w)
    mean = Fr(sum(p * x for p, x in zip(prizes, w)), tot)
    fee = r.choice([20, 30, 40, 50, 60])
    city = r.choice(CITIES)
    return Q((f'At a charity fair in {city}, a spinner has {tot} equal sectors: {w[0]} marked ₹{prizes[0]}, {w[1]} marked ₹{prizes[1]} and {w[2]} marked ₹{prizes[2]}. X is the prize won in one spin. '
              f'(i) Write the probability distribution of X. (ii) Find E(X). (iii) If a spin costs ₹{fee}, is the game fair, favourable or unfavourable to the player?'),
             f'(i) P(₹{prizes[0]}) = {fz(Fr(w[0], tot))}, P(₹{prizes[1]}) = {fz(Fr(w[1], tot))}, P(₹{prizes[2]}) = {fz(Fr(w[2], tot))} (ii) ₹{fz(mean)} (iii) ' +
             ('fair' if mean == fee else 'favourable to the player' if mean > fee else 'unfavourable to the player'), '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= table

FAMILIES = {
    S + '10-st1': [F('C1', 'D2', 'mcq', c10s1_mcq), F('C1', 'D1', 'short', c10s1_mag), F('C2', 'D2', 'explain', c10s1_explain), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s1_mag), F('C3', 'D3', 'numerical', c10s1_dc), F('C4', 'D3', 'case', c10s1_case), F('C3', 'D4', 'numerical', c10s1_dc), F('C3', 'D1', 'numerical', c10s1_mag), F('C2', 'D2', 'numerical', c10s1_dc)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_mcq), F('C1', 'D1', 'short', c10s2_join), F('C2', 'D2', 'explain', c10s2_col), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s2_section), F('C3', 'D3', 'multi_step', c10s2_sum), F('C4', 'D3', 'case', c10s2_case), F('C3', 'D4', 'numerical', c10s2_section), F('C3', 'D1', 'numerical', c10s2_equal), F('C2', 'D2', 'numerical', c10s2_join)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_mcq), F('C1', 'D1', 'short', c10s3_mod), F('C2', 'D2', 'numerical', c10s3_mod), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s3_proj), F('C3', 'D3', 'numerical', c10s3_angle), F('C3', 'D4', 'numerical', c10s3_perp), F('C4', 'D3', 'case', c10s3_case),
                   F('C4', 'D4', 'long', c10s3_long), F('C3', 'D1', 'numerical', c10s3_work, gap='G7'), F('C4', 'D5', 'long', c10s3_long)],
    S + '10-st4': [F('C1', 'D2', 'mcq', c10s4_mcq), F('C1', 'D1', 'short', c10s4_lagrange), F('C2', 'D2', 'numerical', c10s4_lagrange), F('C2', 'D3', 'mcq', c10s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s4_cross), F('C3', 'D3', 'multi_step', c10s4_area), F('C4', 'D3', 'case', c10s4_case), F('C4', 'D4', 'long', c10s4_long), F('C3', 'D4', 'numerical', c10s4_unit), F('C3', 'D1', 'numerical', c10s4_cross)],
    S + '11-st1': [F('C1', 'D2', 'mcq', c11s1_mcq), F('C1', 'D1', 'short', c11s1_third), F('C2', 'D2', 'numerical', c11s1_third), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s1_dr), F('C3', 'D3', 'numerical', c11s1_col), F('C4', 'D3', 'case', c11s1_case), F('C3', 'D4', 'numerical', c11s1_dr), F('C3', 'D1', 'numerical', c11s1_dr)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_mcq), F('C1', 'D1', 'short', c11s2_vec), F('C2', 'D2', 'numerical', c11s2_conv), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s2_vec), F('C3', 'D3', 'numerical', c11s2_point), F('C4', 'D3', 'case', c11s2_case), F('C3', 'D4', 'numerical', c11s2_conv), F('C3', 'D1', 'numerical', c11s2_point)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_mcq), F('C1', 'D1', 'short', c11s3_par), F('C2', 'D2', 'explain', c11s3_par), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s3_angle), F('C3', 'D3', 'numerical', c11s3_perp), F('C4', 'D3', 'case', c11s3_case), F('C3', 'D4', 'numerical', c11s3_perp), F('C3', 'D1', 'numerical', c11s3_angle)],
    S + '11-st4': [F('C1', 'D2', 'mcq', c11s4_mcq), F('C2', 'D2', 'numerical', c11s4_par), F('C2', 'D3', 'mcq', c11s4_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c11s4_par),
                   F('C3', 'D2', 'numerical', c11s4_par), F('C3', 'D3', 'multi_step', c11s4_par), F('C3', 'D4', 'long', c11s4_skew), F('C4', 'D3', 'case', c11s4_case),
                   F('C4', 'D4', 'long', c11s4_skew), F('C4', 'D5', 'long', c11s4_int), F('C1', 'D1', 'mcq', c11s4_mcq)],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_mcq), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s1_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c12s1_form, gap='G7'),
                   F('C3', 'D2', 'numerical', c12s1_form, gap='G7'), F('C3', 'D3', 'multi_step', c12s1_diet, gap='G7'), F('C4', 'D3', 'case', c12s1_case, gap='G7'), F('C3', 'D4', 'multi_step', c12s1_diet, gap='G7'), F('C1', 'D1', 'mcq', c12s1_mcq)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_mcq), F('C1', 'D1', 'short', c12s2_corner), F('C2', 'D2', 'numerical', c12s2_corner), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s2_vertices), F('C3', 'D3', 'multi_step', c12s2_vertices), F('C3', 'D4', 'long', c12s2_max), F('C4', 'D3', 'case', c12s2_case, gap='G7'),
                   F('C4', 'D4', 'long', c12s2_max), F('C4', 'D5', 'long', c12s3_multi), F('C3', 'D1', 'numerical', c12s2_corner)],
    S + '12-st3': [F('C1', 'D2', 'mcq', c12s3_mcq), F('C1', 'D1', 'short', c12s3_unb), F('C2', 'D2', 'explain', c12s3_infeas), F('C2', 'D3', 'mcq', c12s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s3_unb), F('C3', 'D3', 'long', c12s3_min), F('C4', 'D3', 'case', c12s3_case, gap='G7'), F('C4', 'D4', 'long', c12s3_multi), F('C3', 'D4', 'long', c12s3_min), F('C3', 'D1', 'numerical', c12s3_infeas)],
    S + '13-st1': [F('C1', 'D2', 'mcq', c13s1_mcq), F('C1', 'D1', 'short', c13s1_formula), F('C2', 'D2', 'numerical', c13s1_formula), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s1_dice), F('C3', 'D3', 'numerical', c13s1_family), F('C3', 'D4', 'numerical', c13s1_dice), F('C4', 'D3', 'case', c13s1_case, gap='G7'),
                   F('C4', 'D4', 'numerical', c13s1_dice), F('C3', 'D1', 'numerical', c13s1_dice)],
    S + '13-st2': [F('C1', 'D2', 'mcq', c13s2_mcq), F('C1', 'D1', 'short', c13s2_indep), F('C2', 'D2', 'explain', c13s2_cards), F('C2', 'D3', 'mcq', c13s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s2_draw), F('C3', 'D3', 'numerical', c13s2_indep), F('C4', 'D3', 'case', c13s2_case), F('C4', 'D4', 'long', c13s2_long, gap='G7'), F('C3', 'D4', 'numerical', c13s2_draw), F('C3', 'D1', 'numerical', c13s2_draw)],
    S + '13-st3': [F('C1', 'D2', 'mcq', c13s3_mcq), F('C1', 'D1', 'short', c13s3_bags), F('C2', 'D2', 'numerical', c13s3_bags), F('C2', 'D3', 'mcq', c13s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s3_bags), F('C3', 'D3', 'multi_step', c13s3_bags), F('C3', 'D4', 'long', c13s3_machines, gap='G7'), F('C4', 'D3', 'case', c13s3_case, gap='G7'),
                   F('C4', 'D4', 'long', c13s3_machines, gap='G7'), F('C4', 'D5', 'long', c13s3_test, gap='G7'), F('C3', 'D1', 'numerical', c13s3_bags)],
    S + '13-st4': [F('C1', 'D2', 'mcq', c13s4_mcq), F('C1', 'D1', 'short', c13s4_dice), F('C2', 'D2', 'numerical', c13s4_k), F('C2', 'D3', 'mcq', c13s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s4_k), F('C3', 'D3', 'multi_step', c13s4_coins), F('C4', 'D3', 'case', c13s4_case, gap='G7'), F('C4', 'D4', 'long', c13s4_draw), F('C3', 'D4', 'long', c13s4_draw), F('C3', 'D1', 'numerical', c13s4_k)],
}
