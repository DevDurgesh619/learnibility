"""CBSE class 11 physics (NCERT Physics XI) families, chapters 6-10."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, name, two_names, CITIES
from g11_physics_util import polish, sig, g, NUM, NUM2, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq, ordn

S = 'cbse-g11-physics-ch'
G = 9.8
GC = 6.67e-11
ME, RE = 6.0e24, 6.4e6


def vec(x):
    s = f'{x[0]}î'
    for c, u in zip(x[1:], ['ĵ', 'k̂']):
        s += f' {"+" if c >= 0 else "−"} {abs(c)}{u}'
    return s.replace('-', '−')


# ======================================================== ch06 System of Particles and Rotational Motion
# st1 centre of mass

c6s1_tf = tf_mcq('the centre of mass',
                 ['The centre of mass of a system moves as if all the mass were concentrated there and all external forces acted there.', 'Internal forces cannot change the motion of the centre of mass.',
                  'The centre of mass of a uniform rod is at its midpoint.', 'The centre of mass of a body need not lie within the body.'],
                 ['The centre of mass must always lie inside the material of the body.', 'Internal forces can accelerate the centre of mass of an isolated system.',
                  'The centre of mass of two particles is always at the midpoint between them.', 'When a shell explodes in mid-air, its centre of mass stops following the parabolic path.'])

c6s1_explain = pool_txt([
    ('A shell fired as a projectile explodes into fragments in mid-air. Describe the path of the centre of mass after the explosion.', 'It continues along the same parabolic path.',
     'Explosion forces are internal (1 mark); only gravity acts externally, so the CM motion is unchanged (1 mark).'),
    ('Why does the centre of mass of a ring lie at its centre, where there is no material?', 'By symmetry, mass elements on opposite sides balance about the centre.', 'Symmetry argument (2 marks).'),
    ('A person stands at one end of a boat floating on still water and walks to the other end. Why does the boat move?', 'No external horizontal force acts, so the CM stays fixed; the boat moves backward as the person moves forward.',
     'CM of isolated system fixed (1 mark); boat moves opposite (1 mark).'),
])

c6s1_ar = pool_ar([
    ('The centre of mass of a shell exploding in mid-air continues on its parabolic path.', 'The forces of the explosion are internal forces.', 'a', 'R explains A.'),
    ('The centre of mass of a body must lie within the body.', 'The centre of mass of a ring lies at its geometric centre.', 'd', 'A is false; R is true and is a counter-example.'),
    ('For two particles, the centre of mass lies closer to the heavier particle.', 'The distances of the particles from the centre of mass are inversely proportional to their masses.', 'a', 'm₁r₁ = m₂r₂; R explains A.'),
])


def c6s1_two(r):
    m1, m2 = r.sample([1, 2, 3, 4, 5, 6, 8, 10], 2)
    x1, x2 = 0, r.choice([0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0])
    X = m2 * x2 / (m1 + m2)
    return NUM(f'Two particles of masses {m1} kg and {m2} kg are placed {g(x2)} m apart. How far from the {m1} kg particle is their centre of mass?', X, 'm',
               f'X = (m₁x₁ + m₂x₂)/(m₁ + m₂) = ({m1} × 0 + {m2} × {g(x2)})/{m1 + m2} = {{ans}}.', wrongs=[m1 * x2 / (m1 + m2), x2 / 2, m2 * x2 / m1])


def c6s1_three(r):
    pts = [(r.randint(0, 6), r.randint(0, 6)) for _ in range(3)]
    ms = [r.choice([1, 2, 3, 4, 5]) for _ in range(3)]
    M = sum(ms)
    X = sum(m * p[0] for m, p in zip(ms, pts)) / M
    Y = sum(m * p[1] for m, p in zip(ms, pts)) / M
    desc = ', '.join(f'{m} kg at ({p[0]}, {p[1]})' for m, p in zip(ms, pts))
    return {'stem': f'Three particles are placed in the x-y plane: {desc} (coordinates in metres). Find the coordinates of their centre of mass.',
            'answer': f'({g(X)}, {g(Y)}) m', 'key': f'X = Σmx/Σm = {sum(m * p[0] for m, p in zip(ms, pts))}/{M} = {g(X)} m; Y = Σmy/Σm = {sum(m * p[1] for m, p in zip(ms, pts))}/{M} = {g(Y)} m.',
            'distractors': [f'({g(sum(p[0] for p in pts) / 3)}, {g(sum(p[1] for p in pts) / 3)}) m', f'({g(Y)}, {g(X)}) m', f'({g(X * 2)}, {g(Y * 2)}) m']}


def c6s1_heavier(r):
    m1, m2 = sorted(r.sample([2, 3, 4, 5, 6, 8], 2))
    d = r.choice([30, 40, 60, 90, 120])
    return NUM(f'A {m1} kg ball and a {m2} kg ball are joined by a light rod {d} cm long. How far from the {m2} kg ball is the centre of mass?', m1 * d / (m1 + m2), 'cm',
               f'Distance from the heavier ball = m₁d/(m₁ + m₂) = {m1} × {d}/{m1 + m2} = {{ans}}.', wrongs=[m2 * d / (m1 + m2), d / 2, m1 * d / m2])


def c6s1_boat(r):
    m, M = r.choice([50, 60, 70, 80]), r.choice([100, 150, 200, 250])
    L = r.choice([3, 4, 5, 6])
    x = m * L / (m + M)
    who = name(r)
    return {'stem': f'{who} (mass {m} kg) stands at one end of a {L} m long boat of mass {M} kg at rest in still water. {who} walks to the other end. How far does the boat move, and in which direction? (Neglect water resistance.)',
            'answer': f'{sig(x)} m, opposite to {who}\'s motion', 'key': f'CM fixed: m(L − x) = Mx ⇒ x = mL/(m + M) = {m} × {L}/{m + M} = {sig(x)} m (2); boat moves backward (1).', 'gap': 'G7'}


def c6s1_explode(r):
    R = r.choice([400, 600, 800, 1000, 1200])
    m1, m2 = r.choice([(1, 1), (1, 2), (2, 1), (1, 3)])
    x2 = ((m1 + m2) * R - m1 * R / 2) / m2
    return {'stem': f'A shell fired from a gun would have landed {R} m away on level ground. At the highest point it explodes into two fragments with masses in the ratio {m1} : {m2}. The {"lighter" if m1 < m2 else ("heavier" if m1 > m2 else "first")} fragment falls vertically down. Where does the other fragment land?',
            'answer': f'{sig(x2)} m from the gun', 'key': f'CM still lands at {R} m (1). First fragment lands at R/2 = {R // 2} m (1). {m1}(R/2) + {m2}x = {m1 + m2}R ⇒ x = {sig(x2)} m (2).', 'gap': 'G5'}


# st2 vector product, angular velocity, torque

c6s2_tf = tf_mcq('the vector product',
                 ['A × B = −B × A.', 'The vector product of two parallel vectors is zero.', 'A × B is perpendicular to both A and B.', 'î × ĵ = k̂.'],
                 ['A × B = B × A.', 'The vector product of two perpendicular vectors is zero.', 'î × î = 1.', 'A × B lies in the plane of A and B.'])

c6s2_terms = term_mcq([('torque', 'τ = r × F'), ('angular momentum of a particle', 'l = r × p'), ('linear velocity of a point on a rotating body', 'v = ω × r'), ('magnitude of a vector product', '|A × B| = AB sin θ')],
                      'Which relation gives the {a}?', 'The relation {b} gives the', '{a}: {b}.')

c6s2_explain = pool_txt([
    ('Why is it easier to open a door by pushing at the handle (far from the hinges) than near the hinges?', 'Torque = rF sin θ; a larger r gives the needed torque with a smaller force.', 'Torque formula (1 mark); larger moment arm (1 mark).'),
    ('Why is the torque zero when the force passes through the axis of rotation?', 'The moment arm (perpendicular distance from axis to line of force) is zero.', 'τ = F × perpendicular distance (2 marks).'),
    ('Explain why the vector product is not commutative.', 'Reversing the order reverses the direction given by the right-hand rule: A × B = −B × A.', 'Right-hand rule (1 mark); sign change (1 mark).'),
])

c6s2_ar = pool_ar([
    ('A × B is perpendicular to both A and B.', 'The direction of A × B is given by the right-hand screw rule.', 'b', 'Both true; R gives the sense, not the reason it is perpendicular.'),
    ('The torque of a force about a point on its line of action is zero.', 'The position vector r is parallel to F in that case.', 'a', 'r × F = 0 for parallel vectors; R explains A.'),
    ('A long spanner makes it easier to loosen a nut.', 'Torque increases with the perpendicular distance of the force from the axis.', 'a', 'R explains A.'),
    ('î × ĵ = −k̂.', 'The unit vectors î, ĵ, k̂ form a right-handed system.', 'd', 'A is false (î × ĵ = k̂); R is true.'),
])


def c6s2_torque(r):
    F_ = r.choice([10, 20, 25, 40, 50, 80])
    d = r.choice([0.15, 0.2, 0.25, 0.3, 0.4, 0.5])
    th = r.choice([30, 45, 60, 90])
    tau = F_ * d * math.sin(math.radians(th))
    tool = r.choice(['a spanner', 'a door handle', 'a wheel spanner on a car nut', 'a tap handle'])
    return NUM(f'A force of {F_} N is applied at the end of {tool} {g(d * 100)} cm from the axis, at {th}° to the arm. Find the torque about the axis.', tau, 'N m',
               f'τ = rF sin θ = {g(d)} × {F_} × sin {th}° = {{ans}}.', wrongs=[F_ * d, F_ * d * math.cos(math.radians(th)) or F_ * d / 2, F_ / d])


def c6s2_cross(r):
    a = [r.randint(-4, 5) for _ in range(3)]
    b = [r.randint(-4, 5) for _ in range(3)]
    c = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    if c == [0, 0, 0]:
        raise ValueError
    return {'stem': f'Find the torque τ = r × F of the force F = ({vec(b)}) N acting at the point r = ({vec(a)}) m about the origin.',
            'answer': f'τ = ({vec(c)}) N m', 'key': f'Determinant: τx = ({a[1]})({b[2]}) − ({a[2]})({b[1]}) = {c[0]}; τy = ({a[2]})({b[0]}) − ({a[0]})({b[2]}) = {c[1]}; τz = ({a[0]})({b[1]}) − ({a[1]})({b[0]}) = {c[2]}.'.replace('-', '−'),
            'distractors': [f'τ = ({vec([-x for x in c])}) N m', f'τ = ({vec([a[i] * b[i] for i in range(3)])}) N m', f'τ = ({vec([c[1], c[0], c[2]])}) N m']}


def c6s2_wheel(r):
    rpm = r.choice([60, 120, 300, 600, 900, 1200, 1500])
    rad = r.choice([0.1, 0.2, 0.25, 0.3, 0.35])
    w = 2 * math.pi * rpm / 60
    return NUM2(f'A wheel of radius {g(rad * 100)} cm rotates at {rpm} rpm about a fixed axis. Find its angular velocity and the linear speed of a point on its rim.', (w, w * rad), ('rad s⁻¹', 'm s⁻¹'),
                f'ω = 2πn = 2π × {rpm}/60 = {sig(w)} rad s⁻¹ (1.5); v = ωr = {sig(w)} × {g(rad)} = {sig(w * rad)} m s⁻¹ (1.5).',
                wrongs=[(rpm / 60, rpm / 60 * rad), (2 * math.pi * rpm, 2 * math.pi * rpm * rad), (w, w / rad)])


def c6s2_angle(r):
    a = [r.randint(-3, 4) for _ in range(3)]
    b = [r.randint(-3, 4) for _ in range(3)]
    c = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    ma, mb, mc = (math.sqrt(sum(x * x for x in v)) for v in (a, b, c))
    if ma == 0 or mb == 0 or mc == 0:
        raise ValueError
    return {'stem': f'For A = {vec(a)} and B = {vec(b)}, find A × B, its magnitude, and hence the area of the parallelogram formed by A and B.',
            'answer': f'A × B = {vec(c)}; |A × B| = {sig(mc)}; area = {sig(mc)} square units',
            'key': f'Expand the determinant (2): A × B = {vec(c)}; magnitude √({c[0] ** 2} + {c[1] ** 2} + {c[2] ** 2}) = {sig(mc)} (1); area of parallelogram = |A × B| (1).'}


# st3 angular momentum and its conservation; equilibrium of a rigid body

c6s3_tf = tf_mcq('angular momentum and equilibrium',
                 ['If no external torque acts, the angular momentum of a system is conserved.', 'Torque equals the rate of change of angular momentum.', 'A rigid body is in mechanical equilibrium when net force and net torque on it are both zero.',
                  'A couple produces rotation without translation.'],
                 ['Angular momentum is conserved only when no external force acts, even if there is a torque.', 'A body is in equilibrium if the net force on it is zero, whatever the torque.',
                  'A couple produces translation without rotation.', 'An ice skater spins slower when she pulls her arms in.'])

c6s3_explain = pool_txt([
    ('Why does an ice skater spin faster when she pulls her arms close to her body?', 'Pulling arms in reduces I; with no external torque, L = Iω is constant, so ω increases.', 'Conservation of L (1 mark); I decreases ⇒ ω increases (1 mark).'),
    ('A diver performs somersaults by curling up during the dive. Explain the physics.', 'Curling reduces the moment of inertia, so the angular speed increases as angular momentum is conserved.', 'L = Iω constant (1 mark); smaller I ⇒ larger ω (1 mark).'),
    ('State the two conditions for the mechanical equilibrium of a rigid body.', 'Net external force is zero (translational) and net external torque about any point is zero (rotational).', 'Each condition 1 mark.'),
    ('What is a couple? Give an everyday example.', 'Two equal and opposite forces with different lines of action; e.g. turning a steering wheel or a bottle cap.', 'Definition (1 mark); example (1 mark).'),
])

c6s3_ar = pool_ar([
    ('An ice skater spins faster when she folds her arms.', 'Her angular momentum is conserved while her moment of inertia decreases.', 'a', 'R explains A.'),
    ('A body may be in translational equilibrium but still rotate with increasing angular speed.', 'A couple gives zero net force but non-zero torque.', 'a', 'R explains A.'),
    ('The angular momentum of a planet about the Sun is conserved.', 'The gravitational force on the planet is central and exerts no torque about the Sun.', 'a', 'R explains A.'),
    ('A couple can be replaced by a single force.', 'A couple has zero resultant force.', 'd', 'A is false; R is true (a single force cannot have zero resultant and non-zero torque).'),
])


def c6s3_skater(r):
    I1 = r.choice([2.5, 3, 3.6, 4, 4.8, 5])
    f = r.choice([0.4, 0.5, 0.6, 0.75])
    I2 = round(I1 * f, 2)
    n1 = r.choice([1, 1.5, 2, 2.5])
    n2 = n1 * I1 / I2
    who = name(r)
    return NUM(f'{who}, an ice skater, spins at {g(n1)} rev s⁻¹ with arms stretched (moment of inertia {g(I1)} kg m²). On pulling the arms in, the moment of inertia becomes {g(I2)} kg m². Find the new rate of spin.', n2, 'rev s⁻¹',
               f'I₁ω₁ = I₂ω₂ ⇒ n₂ = I₁n₁/I₂ = {g(I1)} × {g(n1)}/{g(I2)} = {{ans}}.', wrongs=[n1 * I2 / I1, n1 * (I1 / I2) ** 2, n1 + I1 - I2])


def c6s3_balance(r):
    m1 = r.choice([10, 20, 25, 30, 40, 50])
    x1 = r.choice([10, 15, 20, 25, 30])
    m2 = r.choice([10, 20, 25, 40, 50])
    x2 = 50 + m1 * (50 - x1) / m2
    if not 55 <= x2 <= 100:
        raise ValueError
    return NUM(f'A metre stick is balanced on a knife edge at its centre (the 50 cm mark). A {m1} g mass hangs at the {x1} cm mark. Where must a {m2} g mass be hung to balance the stick?', x2, 'cm mark',
               f'Moments about 50 cm: {m1} × ({50} − {x1}) = {m2} × (x − 50) ⇒ x = 50 + {m1 * (50 - x1)}/{m2} = {{ans}}.', wrongs=[50 + m2 * (50 - x1) / m1, 100 - x1, 50 + (50 - x1)])


def c6s3_plank(r):
    L = r.choice([2, 3, 4, 5, 6])
    W = r.choice([200, 300, 400, 500])
    m = r.choice([300, 400, 500, 600, 800])
    x = round(L * r.choice([0.2, 0.25, 0.3, 0.4, 0.6, 0.7]), 2)
    R2 = (W * L / 2 + m * x) / L
    R1 = W + m - R2
    return {'stem': f'A uniform plank of length {L} m and weight {W} N rests on two supports A and B at its ends. A boy of weight {m} N stands {g(x)} m from A. Find the reactions at A and B.',
            'answer': f'R_A = {sig(R1)} N, R_B = {sig(R2)} N',
            'key': f'Moments about A: R_B × {L} = {W} × {g(L / 2)} + {m} × {g(x)} ⇒ R_B = {sig(R2)} N (2); R_A = {W + m} − R_B = {sig(R1)} N (1).'}


def c6s3_ladder(r):
    L = r.choice([3, 4, 5, 6])
    a = r.choice([1, 1.5, 2]) if L > 3 else r.choice([1, 1.5])
    m = r.choice([15, 20, 25, 30])
    h = math.sqrt(L * L - a * a)
    W = m * G
    Fw = W * (a / 2) / h
    return {'stem': f'A {L} m long ladder weighing {m} kg leans on a frictionless wall. Its feet rest on the floor {g(a)} m from the wall. Find the reaction forces of the wall and the floor. (g = 9.8 m s⁻²; weight acts at the middle of the ladder)',
            'answer': f'Wall: {sig(Fw)} N (horizontal); floor: {sig(math.hypot(W, Fw))} N at {num(math.degrees(math.atan2(W, Fw)), 1)}° to the horizontal',
            'key': f'Height of top = √({L}² − {g(a)}²) = {sig(h)} m (1). Moments about the foot: F₁ × {sig(h)} = {g(W)} × {g(a / 2)} ⇒ F₁ = {sig(Fw)} N (2). '
                   f'Floor: vertical {g(W)} N, horizontal (friction) {sig(Fw)} N; resultant {sig(math.hypot(W, Fw))} N (2).', 'gap': 'G5'}


def c6s3_L(r):
    m = r.choice([0.1, 0.2, 0.5, 1, 2])
    v = r.choice([2, 3, 4, 5, 10])
    rr = r.choice([0.5, 1, 1.5, 2])
    return NUM(f'A particle of mass {g(m)} kg moves with speed {v} m s⁻¹ in a circle of radius {g(rr)} m. Find the magnitude of its angular momentum about the centre.', m * v * rr, 'kg m² s⁻¹',
               f'L = mvr = {g(m)} × {v} × {g(rr)} = {{ans}}.', wrongs=[m * v / rr, m * v * v * rr, m * v])


# st4 moment of inertia; dynamics of rotation about a fixed axis

MI = [('thin ring about its axis', 'MR²'), ('uniform disc about its axis', 'MR²/2'), ('solid sphere about a diameter', '2MR²/5'), ('hollow (thin) spherical shell about a diameter', '2MR²/3'),
      ('thin rod about a perpendicular axis through its centre', 'ML²/12'), ('thin rod about a perpendicular axis through one end', 'ML²/3'), ('solid cylinder about its axis', 'MR²/2')]
c6s4_mi = term_mcq(MI[:6], 'The moment of inertia of a {a} is', None, 'I({a}) = {b}.')

c6s4_tf = tf_mcq('moment of inertia',
                 ['Moment of inertia depends on the axis of rotation.', 'A ring has a larger moment of inertia than a disc of the same mass and radius about their axes.', 'The radius of gyration k is given by I = Mk².',
                  'Moment of inertia plays the role of mass in rotational motion.'],
                 ['Moment of inertia depends only on the mass of the body.', 'A disc has a larger moment of inertia than a ring of the same mass and radius about their axes.',
                  'Moment of inertia is a vector quantity.', 'The radius of gyration of a body is always equal to its geometrical radius.'])

c6s4_explain = pool_txt([
    ('Why does a ring have a greater moment of inertia than a disc of the same mass and radius?', 'All the mass of the ring is at distance R from the axis; much of the disc\'s mass is nearer the axis.', 'I = Σmr² (1 mark); comparison (1 mark).'),
    ('Why are flywheels made with most of their mass at the rim?', 'A large moment of inertia resists changes in angular speed and smooths out the motion.', 'Mass at rim ⇒ large I (1 mark); resists change in ω (1 mark).'),
    ('What is meant by the radius of gyration of a body about an axis?', 'The distance k from the axis at which the whole mass, if concentrated, would have the same moment of inertia: I = Mk².', 'Definition (2 marks).'),
    ('Write the rotational analogues of mass, force, linear momentum and Newton\'s second law.', 'Moment of inertia I, torque τ, angular momentum L, τ = Iα.', 'Each pair ½ mark.'),
])

c6s4_ar = pool_ar([
    ('A flywheel has most of its mass near the rim.', 'Moment of inertia increases with distance of mass from the axis.', 'a', 'R explains A.'),
    ('The moment of inertia of a body is fixed and does not depend on the axis.', 'Moment of inertia depends on mass distribution about the axis.', 'd', 'A is false; R is true.'),
    ('For a given torque, a disc has a larger angular acceleration than a ring of equal mass and radius.', 'α = τ/I and the disc has the smaller moment of inertia.', 'a', 'R explains A.'),
    ('Work done by a constant torque τ turning a body through angle θ is τθ.', 'Rotational work is the analogue of force × displacement.', 'a', 'R explains A.'),
])


def c6s4_alpha(r):
    shape, k, kn = r.choice([('disc', 0.5, 'MR²/2'), ('ring', 1.0, 'MR²'), ('solid cylinder', 0.5, 'MR²/2')])
    M = r.choice([2, 4, 5, 10, 20])
    R = r.choice([0.1, 0.2, 0.25, 0.4, 0.5])
    tau = r.choice([0.5, 1, 2, 4, 5, 8])
    I = k * M * R * R
    return NUM(f'A torque of {g(tau)} N m acts on a {shape} of mass {M} kg and radius {g(R * 100)} cm, free to rotate about its axis. Find its angular acceleration.', tau / I, 'rad s⁻²',
               f'I = {kn} = {g(I, 4)} kg m²; α = τ/I = {g(tau)}/{g(I, 4)} = {{ans}}.', wrongs=[tau / (M * R * R) if k != 1 else tau / (0.5 * M * R * R), tau * I, tau / (M * R)])


def c6s4_ke(r):
    I = r.choice([0.5, 1, 2, 2.5, 4, 5, 10])
    rpm = r.choice([60, 120, 180, 300, 600])
    w = 2 * math.pi * rpm / 60
    return NUM(f'A flywheel of moment of inertia {g(I)} kg m² rotates at {rpm} rpm. Find its rotational kinetic energy.', 0.5 * I * w * w, 'J',
               f'ω = 2π × {rpm}/60 = {sig(w)} rad s⁻¹; K = ½Iω² = {{ans}}.', wrongs=[I * w * w, 0.5 * I * (rpm / 60) ** 2, 0.5 * I * w])


def c6s4_cord(r):
    M = r.choice([10, 20, 25, 40])
    R = r.choice([0.2, 0.25, 0.3, 0.4])
    F_ = r.choice([20, 25, 30, 40, 50])
    L = r.choice([1, 2, 3])
    I = M * R * R
    a = F_ * R / I
    W = F_ * L
    w = math.sqrt(2 * W / I)
    return {'stem': f'A cord of negligible mass is wound round the rim of a flywheel (treat as a ring) of mass {M} kg and radius {g(R * 100)} cm. A steady pull of {F_} N is applied on the cord. The flywheel is mounted on a horizontal axle with frictionless bearings. '
                    f'Find (i) the angular acceleration, (ii) the work done by the pull when {L} m of cord is unwound and (iii) the angular speed then.',
            'answer': f'(i) {sig(a)} rad s⁻² (ii) {W} J (iii) {sig(w)} rad s⁻¹',
            'key': f'(i) I = MR² = {g(I)} kg m²; τ = FR = {g(F_ * R)} N m; α = τ/I = {sig(a)} rad s⁻² (1). (ii) W = F × l = {W} J (1). (iii) ½Iω² = W ⇒ ω = {sig(w)} rad s⁻¹ (1).'}


def c6s4_gyration(r):
    shape, k, kn = r.choice([('disc about its axis', 0.5, 'R/√2'), ('solid sphere about a diameter', 0.4, 'R√(2/5)'), ('thin rod about a perpendicular axis through its end', 1 / 3, 'L/√3'),
                             ('thin rod about a perpendicular axis through its centre', 1 / 12, 'L/√12')])
    R = r.choice([0.2, 0.3, 0.5, 0.6, 1.0, 1.2])
    kk = math.sqrt(k) * R
    sym = 'L' if 'rod' in shape else 'R'
    return NUM(f'Find the radius of gyration of a {shape}, if {sym} = {g(R * 100)} cm.', kk * 100, 'cm', f'I = Mk² ⇒ k = {kn} = {{ans}}.', wrongs=[k * R * 100, R * 100, R * 100 / 2])


def c6s4_rpm(r):
    n1, n2 = sorted(r.sample([600, 900, 1200, 1500, 1800, 2400, 3000], 2))
    t = r.choice([4, 5, 8, 10, 12, 15, 16])
    w1, w2 = 2 * math.pi * n1 / 60, 2 * math.pi * n2 / 60
    al = (w2 - w1) / t
    th = (w1 + w2) / 2 * t
    return {'stem': f'The angular speed of a motor wheel is increased from {n1} rpm to {n2} rpm in {t} s. (i) What is its angular acceleration, assuming it to be uniform? (ii) How many revolutions does the wheel make during this time?',
            'answer': f'(i) {sig(al)} rad s⁻² (ii) {sig(th / (2 * math.pi))} revolutions',
            'key': f'(i) ω₁ = {sig(w1)}, ω₂ = {sig(w2)} rad s⁻¹; α = (ω₂ − ω₁)/t = {sig(al)} rad s⁻² (1.5). (ii) θ = ½(ω₁ + ω₂)t = {sig(th)} rad = {sig(th / (2 * math.pi))} rev (1.5).'}


def c6s4_combine(r):
    I1, I2 = r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, 5])
    w1, w2 = r.choice([10, 20, 30, 40]), r.choice([0, 5, 10])
    w = (I1 * w1 + I2 * w2) / (I1 + I2)
    k1 = 0.5 * I1 * w1 * w1 + 0.5 * I2 * w2 * w2
    k2 = 0.5 * (I1 + I2) * w * w
    return {'stem': f'Two discs of moments of inertia {I1} kg m² and {I2} kg m² are on a common axis. The first rotates at {w1} rad s⁻¹ and the second {"is at rest" if w2 == 0 else f"at {w2} rad s⁻¹ in the same sense"}. They are brought into contact face to face and rotate together. '
                    'Find the common angular speed and the loss of kinetic energy. Where does this energy go?',
            'answer': f'{sig(w)} rad s⁻¹; loss {sig(k1 - k2)} J (to heat by friction)',
            'key': f'No external torque: I₁ω₁ + I₂ω₂ = (I₁ + I₂)ω ⇒ ω = {sig(w)} rad s⁻¹ (2). KE before {g(k1)} J, after {sig(k2)} J; loss {sig(k1 - k2)} J (2), dissipated by friction between the discs (1).', 'gap': 'G5'}


c6s4_derive = pool_txt([
    ('Show that the angular momentum of a rigid body rotating about a fixed axis is L = Iω, and hence that τ = Iα.', 'L = Σm r² ω = Iω; τ = dL/dt = I dω/dt = Iα',
     'l = m v r = m r² ω for each particle (2); sum to Iω (1); differentiate with I constant (2).'),
    ('Show that the rate of change of angular momentum of a particle is equal to the torque acting on it.', 'dl/dt = τ', 'l = r × p (1); dl/dt = (dr/dt × p) + (r × dp/dt) (2); first term v × mv = 0, second r × F = τ (2).'),
    ('Show that the work done by a constant torque τ in rotating a body through an angle θ is τθ, and that the power is τω.', 'W = τθ; P = τω', 'dW = F ds = F r dθ = τ dθ (2); integrate (1); P = dW/dt = τω (2).'),
])


def c6s4_case(r):
    who = name(r)
    M, R = r.choice([(2, 0.3), (1.5, 0.25), (3, 0.4), (1, 0.2)])
    w = r.choice([10, 15, 20, 25])
    t = r.choice([5, 8, 10, 20])
    I = 0.5 * M * R * R
    return {'stem': (f'{who} spins a potter\'s wheel (a uniform disc of mass {M} kg and radius {g(R * 100)} cm) up to {w} rad s⁻¹ and lets it go. Friction brings it to rest uniformly in {t} s.\n'
                     '(i) Find the moment of inertia. (ii) Find the angular deceleration. (iii) Find the frictional torque. (iv) Find the number of revolutions before it stops.'),
            'answer': f'(i) {sig(I)} kg m² (ii) {sig(w / t)} rad s⁻² (iii) {sig(I * w / t)} N m (iv) {sig(w * t / 2 / (2 * math.pi))}',
            'key': f'(i) ½MR² (1). (ii) α = ω/t (1). (iii) τ = Iα (1). (iv) θ = ½ωt = {sig(w * t / 2)} rad ÷ 2π (1).'}


# ======================================================== ch07 Gravitation
# st1 Kepler's laws and universal law

c7s1_kepler = pool_mcq([
    ('Kepler\'s first law (law of orbits) states that', 'every planet moves in an elliptical orbit with the Sun at one focus', ['every planet moves in a circle with the Sun at the centre', 'the Sun moves in an ellipse round the Earth', 'planets move in elliptical orbits with the Sun at the centre of the ellipse'], 'Ellipse, Sun at one focus.'),
    ('Kepler\'s second law (law of areas) states that the line joining the Sun and a planet', 'sweeps out equal areas in equal intervals of time', ['sweeps out equal angles in equal times', 'has constant length', 'sweeps out areas proportional to the square of time'], 'Equal areas in equal times (angular momentum conservation).'),
    ('Kepler\'s third law (law of periods) states that', 'T² ∝ a³, where a is the semi-major axis', ['T ∝ a²', 'T² ∝ a²', 'T³ ∝ a²'], 'Square of period ∝ cube of semi-major axis.'),
    ('Which of Kepler\'s laws follows directly from the conservation of angular momentum?', 'the law of areas (second law)', ['the law of orbits (first law)', 'the law of periods (third law)', 'none of them'], 'dA/dt = L/2m is constant when L is conserved.'),
])

c7s1_tf = tf_mcq('the universal law of gravitation',
                 ['The gravitational force between two bodies is always attractive.', 'G is a universal constant; g varies from place to place.', 'The gravitational force obeys Newton\'s third law.',
                  'Doubling the distance between two masses reduces the force to one-fourth.'],
                 ['The gravitational force between two bodies depends on the medium between them.', 'G and g are both universal constants.', 'Doubling the distance halves the gravitational force.',
                  'A heavier body attracts a lighter body more strongly than the lighter body attracts it.'])

c7s1_explain = pool_txt([
    ('Kepler\'s second law follows from the conservation of angular momentum. Explain.', 'Areal velocity dA/dt = L/2m; with a central force there is no torque, L is constant, so dA/dt is constant.', 'dA/dt = L/2m (1 mark); central force ⇒ L constant (1 mark).'),
    ('Why does a planet move faster when it is closer to the Sun?', 'By the law of areas (angular momentum conservation), mvr is constant, so v is larger when r is smaller.', 'L = mvr constant (1 mark); conclusion (1 mark).'),
    ('Distinguish between G and g.', 'G is the universal gravitational constant (6.67 × 10⁻¹¹ N m² kg⁻²); g is the acceleration due to gravity, which varies with place.', 'Each 1 mark.'),
])

c7s1_ar = pool_ar([
    ('A planet moves fastest at perihelion.', 'Its angular momentum about the Sun is conserved.', 'a', 'mvr constant ⇒ v largest when r is smallest.'),
    ('The value of G on the Moon is one-sixth of its value on the Earth.', 'The acceleration due to gravity on the Moon is about one-sixth of that on the Earth.', 'd', 'A is false (G is universal); R is true.'),
    ('The Earth attracts an apple with the same force as the apple attracts the Earth.', 'Gravitational forces obey Newton\'s third law.', 'a', 'R explains A.'),
])


def c7s1_force(r):
    m1, m2 = r.choice([50, 60, 70, 100, 1000]), r.choice([40, 50, 80, 100, 2000])
    d = r.choice([0.5, 1, 2, 5, 10])
    F_ = GC * m1 * m2 / (d * d)
    return NUM(f'Find the gravitational force between two bodies of masses {m1} kg and {m2} kg kept {g(d)} m apart. (G = 6.67 × 10⁻¹¹ N m² kg⁻²)', F_, 'N',
               f'F = Gm₁m₂/r² = 6.67 × 10⁻¹¹ × {m1} × {m2}/{g(d * d)} = {{ans}}.', wrongs=[GC * m1 * m2 / d, GC * m1 * m2 * d * d, GC * (m1 + m2) / (d * d)])


def c7s1_kepler3(r):
    k = r.choice([1.52, 4, 5.2, 9.5, 0.39, 0.72, 2, 3])
    T = k ** 1.5
    return NUM(f'A planet revolves round the Sun in a nearly circular orbit of radius {g(k)} times that of the Earth. Using Kepler\'s third law, find its period of revolution in Earth years.', T, 'years',
               f'T² ∝ r³ ⇒ T = (r/r_E)^(3/2) × 1 year = {g(k)}^1.5 = {{ans}}.', wrongs=[k * k, k, k ** (2 / 3)])


def c7s1_null(r):
    m1 = 1
    k = r.choice([4, 9, 16, 25, 81])
    d = r.choice([1, 2, 3, 6, 10])
    x = d / (1 + math.sqrt(k))
    return NUM(f'Two point masses m and {k}m are fixed {d} m apart. At what distance from the mass m is the net gravitational force on a third mass zero?', x, 'm',
               f'Gm/x² = G({k}m)/({d} − x)² ⇒ ({d} − x)/x = √{k} = {g(math.sqrt(k))} ⇒ x = {d}/(1 + {g(math.sqrt(k))}) = {{ans}}.', wrongs=[d / (1 + k), d / 2, d * math.sqrt(k) / (1 + math.sqrt(k))])


def c7s1_aphelion(r):
    rp, ra = r.choice([(1.47, 1.52), (0.31, 0.47), (1.38, 1.67), (0.46, 0.70)])
    vp = r.choice([30.3, 58.9, 26.5, 38.9])
    va = vp * rp / ra
    return {'stem': f'A planet\'s distance from the Sun is {g(rp)} × 10¹¹ m at perihelion and {g(ra)} × 10¹¹ m at aphelion. Its speed at perihelion is {g(vp)} km s⁻¹. Find its speed at aphelion and state the law used.',
            'answer': f'{sig(va)} km s⁻¹ (conservation of angular momentum / Kepler\'s second law)',
            'key': f'mv_p r_p = mv_a r_a (2) ⇒ v_a = {g(vp)} × {g(rp)}/{g(ra)} = {sig(va)} km s⁻¹ (1).'}


def c7s1_ratio(r):
    k = r.choice([2, 3, 4, 0.5])
    f = 1 / (k * k)
    return NUM(f'The distance between two bodies is made {g(k)} times. By what factor does the gravitational force between them change?', f, '',
               f'F ∝ 1/r² ⇒ factor = 1/{g(k)}² = {{ans}}.', wrongs=[1 / k, k * k, k], n=3)


# st2 acceleration due to gravity and its variation

c7s2_tf = tf_mcq('the acceleration due to gravity',
                 ['g decreases with height above the Earth\'s surface.', 'g decreases with depth below the Earth\'s surface.', 'g is zero at the centre of the Earth.', 'g = GM/R² at the surface.'],
                 ['g increases with depth below the surface.', 'g is maximum at the centre of the Earth.', 'g is independent of the radius of the planet.', 'g at a height h equals g at a depth h.'])

c7s2_explain = pool_txt([
    ('Why is the acceleration due to gravity zero at the centre of the Earth?', 'At depth d, g(d) = g(1 − d/R); at the centre d = R, so g = 0. Mass around pulls equally in all directions.', 'Formula (1 mark); d = R (1 mark).'),
    ('Show that g = GM/R² and explain why g is independent of the mass of the falling body.', 'mg = GMm/R² ⇒ g = GM/R²; the body\'s mass cancels.', 'Equating weight and gravitational force (1 mark); cancellation (1 mark).'),
    ('Why does a body weigh slightly less at the top of a mountain?', 'g decreases with height (g_h ≈ g(1 − 2h/R)), so the weight mg_h is smaller.', 'g falls with h (1 mark); weight ∝ g (1 mark).'),
])

c7s2_ar = pool_ar([
    ('The weight of a body is zero at the centre of the Earth.', 'g at depth d is g(1 − d/R).', 'a', 'At d = R, g = 0; R explains A.'),
    ('g decreases faster with height than with depth (for small distances).', 'g_h ≈ g(1 − 2h/R) while g_d = g(1 − d/R).', 'a', 'R explains A.'),
    ('A body weighs more on the Moon than on the Earth.', 'The Moon\'s mass is smaller than the Earth\'s.', 'd', 'A is false; R is true.'),
])


def c7s2_height(r):
    h = r.choice([32, 64, 100, 160, 320, 640, 3200, 6400])
    gh = G * (RE / (RE + h * 1000)) ** 2
    return NUM(f'Find the value of g at a height of {h} km above the Earth\'s surface. (g = 9.8 m s⁻² at the surface, R = 6400 km)', gh, 'm s⁻²',
               f'g_h = g R²/(R + h)² = 9.8 × (6400/{6400 + h})² = {{ans}}.', wrongs=[G * (1 - h / 6400), G * (1 - 2 * h / 6400) if h < 3200 else G / 2, G * RE / (RE + h * 1000)])


def c7s2_depth(r):
    d = r.choice([16, 32, 64, 100, 160, 320, 1600, 3200])
    return NUM(f'Find the value of g at a depth of {d} km below the Earth\'s surface. (g = 9.8 m s⁻² at the surface, R = 6400 km)', G * (1 - d / 6400), 'm s⁻²',
               f'g_d = g(1 − d/R) = 9.8 × (1 − {d}/6400) = {{ans}}.', wrongs=[G * (1 - 2 * d / 6400), G * (6400 / (6400 + d)) ** 2, G * (1 + d / 6400)])


def c7s2_equal(r):
    d = r.choice([2, 4, 5, 8, 10, 16])
    return {'stem': f'At what height above the Earth\'s surface is g the same as its value at a depth of {d} km? (Assume the height and depth are small compared with R.)',
            'answer': f'{g(d / 2)} km', 'key': f'g(1 − 2h/R) = g(1 − d/R) ⇒ 2h = d ⇒ h = {g(d / 2)} km (3 steps, 1 mark each).',
            'distractors': [f'{d} km', f'{2 * d} km', f'{g(d / 4)} km']}


def c7s2_planet(r):
    km, kr = r.choice([(2, 2), (4, 2), (0.5, 0.5), (8, 2), (1 / 81, 0.27), (0.11, 0.53), (95, 9.4)])
    gp = G * km / (kr * kr)
    nm = {(1 / 81, 0.27): 'the Moon (mass 1/81 and radius 0.27 of the Earth\'s)', (0.11, 0.53): 'Mars (mass 0.11 and radius 0.53 of the Earth\'s)',
          (95, 9.4): 'Saturn (mass 95 and radius 9.4 of the Earth\'s)'}.get((km, kr), f'a planet whose mass is {g(km)} times and radius {g(kr)} times that of the Earth')
    return NUM(f'Find the acceleration due to gravity on the surface of {nm}. (g on Earth = 9.8 m s⁻²)', gp, 'm s⁻²', f'g ∝ M/R² ⇒ g_p = 9.8 × {g(km, 4)}/{g(kr)}² = {{ans}}.',
               wrongs=[G * km / kr, G * km * kr * kr, G * kr / km])


def c7s2_fraction(r):
    f = r.choice([0.25, 0.5, 0.64, 0.81, 0.36])
    h = RE * (1 / math.sqrt(f) - 1)
    return {'stem': f'At what height above the Earth\'s surface does g become {int(f * 100)}% of its value at the surface? (R = 6400 km)',
            'answer': f'{sig(h / 1000)} km', 'key': f'g_h/g = R²/(R + h)² = {f} ⇒ (R + h)/R = 1/√{f} = {g(1 / math.sqrt(f))} (2) ⇒ h = {sig(h / 1000)} km (1).'}


def c7s2_gcalc(r):
    M, R, nm = r.choice([(6.0e24, 6.4e6, 'the Earth'), (7.35e22, 1.74e6, 'the Moon'), (6.4e23, 3.4e6, 'Mars'), (1.9e27, 7.0e7, 'Jupiter')])
    return NUM(f'The mass of {nm} is {g(M)} kg and its radius is {g(R)} m. Calculate the acceleration due to gravity at its surface. (G = 6.67 × 10⁻¹¹ N m² kg⁻²)', GC * M / (R * R), 'm s⁻²',
               f'g = GM/R² = 6.67 × 10⁻¹¹ × {g(M)}/({g(R)})² = {{ans}}.', wrongs=[GC * M / R, GC * M / (R * R) * 2, GC * M / (R * R) / 6])


# st3 gravitational PE, escape speed, orbital speed

c7s3_terms = term_mcq([('escape speed from the Earth\'s surface', '√(2gR)'), ('orbital speed of a satellite close to the Earth\'s surface', '√(gR)'),
                       ('gravitational potential energy of mass m at distance r from the centre of mass M', '−GMm/r'), ('gravitational potential at distance r from mass M', '−GM/r')],
                      'The {a} is', 'Which quantity is given by {b}?', '{a} = {b}.')

c7s3_tf = tf_mcq('escape speed and orbital speed',
                 ['Escape speed does not depend on the mass of the body projected.', 'Escape speed from the Earth is about 11.2 km s⁻¹.', 'Escape speed is √2 times the orbital speed close to the surface.',
                  'Gravitational potential energy is negative and zero at infinity.'],
                 ['Escape speed depends on the direction of projection.', 'Escape speed from the Earth is about 8 km s⁻¹.', 'Orbital speed increases with the height of the orbit.',
                  'Gravitational potential energy is zero at the Earth\'s surface (in the −GMm/r convention).'])

c7s3_explain = pool_txt([
    ('Why does the Moon have no atmosphere?', 'Its escape speed (about 2.4 km s⁻¹) is small; gas molecules with thermal speeds comparable to it escape over time.', 'Low escape speed (1 mark); molecular speeds (1 mark).'),
    ('Why is gravitational potential energy taken as negative?', 'Zero is chosen at infinity; gravity is attractive, so work must be done on a body to take it to infinity, meaning its PE is less than zero at finite r.', 'Reference at infinity (1 mark); attractive force (1 mark).'),
    ('Show that the escape speed from the Earth\'s surface is √2 times the orbital speed of a satellite close to the surface.', 'v_e = √(2gR), v_o = √(gR), so v_e = √2 v_o.', 'Both formulas (1 mark); ratio (1 mark).'),
])

c7s3_ar = pool_ar([
    ('The escape speed of a body does not depend on its mass.', 'Both kinetic energy and gravitational PE are proportional to the mass of the body.', 'a', 'Mass cancels in ½mv² = GMm/R; R explains A.'),
    ('A satellite in a higher orbit moves more slowly.', 'Orbital speed v = √(GM/r).', 'a', 'R explains A.'),
    ('The escape speed from the Earth depends on the angle of projection.', 'Escape needs the total energy to be at least zero.', 'd', 'A is false (energy, not direction, decides escape); R is true.'),
    ('The Moon has no atmosphere.', 'The escape speed from the Moon is small.', 'a', 'R explains A.'),
])


def c7s3_escape(r):
    M, R, nm = r.choice([(6.0e24, 6.4e6, 'the Earth'), (7.35e22, 1.74e6, 'the Moon'), (6.4e23, 3.4e6, 'Mars'), (1.9e27, 7.0e7, 'Jupiter')])
    ve = math.sqrt(2 * GC * M / R)
    return NUM(f'Calculate the escape speed from the surface of {nm} (mass {g(M)} kg, radius {g(R)} m). (G = 6.67 × 10⁻¹¹ N m² kg⁻²)', ve / 1000, 'km s⁻¹',
               f'v_e = √(2GM/R) = √(2 × 6.67 × 10⁻¹¹ × {g(M)}/{g(R)}) = {sig(ve)} m s⁻¹ = {{ans}}.', wrongs=[math.sqrt(GC * M / R) / 1000, 2 * GC * M / R / 1e6, math.sqrt(2 * GC * M) / R])


def c7s3_orbit(r):
    h = r.choice([400, 600, 800, 1000, 1600, 3600])
    rr = RE + h * 1000
    v = math.sqrt(GC * ME / rr)
    T = 2 * math.pi * rr / v
    return NUM2(f'A satellite orbits the Earth at a height of {h} km above the surface. Find its orbital speed and period. (G = 6.67 × 10⁻¹¹ N m² kg⁻², M = 6.0 × 10²⁴ kg, R = 6400 km)', (v / 1000, T / 60),
                ('km s⁻¹', 'min'), f'r = R + h = {g(rr)} m (1); v = √(GM/r) = {sig(v / 1000)} km s⁻¹ (1); T = 2πr/v = {sig(T)} s = {sig(T / 60)} min (1).',
                wrongs=[(math.sqrt(GC * ME / RE) / 1000, 2 * math.pi * RE / math.sqrt(GC * ME / RE) / 60), (math.sqrt(2 * GC * ME / rr) / 1000, T / 60 / math.sqrt(2)), (v / 1000, T / 3600)])


def c7s3_work(r):
    m = r.choice([100, 200, 400, 500, 1000])
    k = r.choice([1, 2, 3, 0.5])
    h = k * RE
    W = GC * ME * m * h / (RE * (RE + h))
    return NUM(f'How much energy is needed to raise a satellite of mass {m} kg from the Earth\'s surface to a height {g(k)}R above it (just lifting, not putting into orbit)? (G = 6.67 × 10⁻¹¹ N m² kg⁻², M = 6.0 × 10²⁴ kg, R = 6.4 × 10⁶ m)',
               W, 'J', f'ΔU = GMm[1/R − 1/(R + h)] = GMm h/(R(R + h)) = {{ans}}.', wrongs=[m * G * h, GC * ME * m / (RE + h), GC * ME * m / RE])


def c7s3_ratio(r):
    km, kr = r.choice([(2, 2), (4, 2), (8, 2), (9, 4), (16, 4), (2, 0.5)])
    f = math.sqrt(km / kr)
    return NUM(f'A planet has {g(km)} times the mass and {g(kr)} times the radius of the Earth. If the escape speed from the Earth is 11.2 km s⁻¹, find the escape speed from the planet.', 11.2 * f, 'km s⁻¹',
               f'v_e ∝ √(M/R) ⇒ v = 11.2 × √({g(km)}/{g(kr)}) = {{ans}}.', wrongs=[11.2 * km / kr, 11.2 * math.sqrt(km * kr), 11.2 * math.sqrt(kr / km)])


def c7s3_maxh(r):
    v = r.choice([2, 3, 4, 5, 6, 8])
    gR = G * RE
    h = RE * v * v * 1e6 / (2 * gR - v * v * 1e6)
    return {'stem': f'A body is projected vertically upward from the Earth\'s surface with a speed of {v} km s⁻¹. Find the maximum height it reaches. (g = 9.8 m s⁻², R = 6400 km; do not use h = v²/2g)',
            'answer': f'{sig(h / 1000)} km', 'key': f'½mv² − GMm/R = −GMm/(R + h) (1); with GM = gR²: h = Rv²/(2gR − v²) (1) = 6.4 × 10⁶ × {g(v * v * 1e6)}/({g(2 * gR)} − {g(v * v * 1e6)}) = {sig(h / 1000)} km (1). '
                                                         f'(The constant-g formula would give {sig(v * v * 1e6 / (2 * G) / 1000)} km.)', 'gap': 'G5'}


def c7s3_infinity(r):
    v = r.choice([12, 13, 14, 15, 16, 20])
    vi = math.sqrt(v * v - 11.2 ** 2)
    return {'stem': f'A rocket is fired vertically from the Earth\'s surface with a speed of {v} km s⁻¹. What will its speed be far away from the Earth? (Escape speed = 11.2 km s⁻¹; neglect air resistance and the Sun.)',
            'answer': f'{sig(vi)} km s⁻¹', 'key': f'½mv² − GMm/R = ½mv∞² and GMm/R = ½mv_e² (2) ⇒ v∞ = √(v² − v_e²) = √({v * v} − {g(11.2 ** 2)}) = {sig(vi)} km s⁻¹ (3).', 'gap': 'G5'}


c7s3_derive = pool_txt([
    ('Derive an expression for the escape speed from the surface of a planet of mass M and radius R.', 'v_e = √(2GM/R) = √(2gR)', 'Energy at surface ½mv² − GMm/R (2); at infinity ≥ 0 (1); solve and use GM = gR² (2).'),
    ('Derive an expression for the variation of g with height h above the Earth\'s surface, and its approximate form for h ≪ R.', 'g_h = g R²/(R + h)² ≈ g(1 − 2h/R)', 'GM/(R + h)² (2); ratio with g (1); binomial approximation (2).'),
    ('Derive an expression for the acceleration due to gravity at depth d below the Earth\'s surface.', 'g_d = g(1 − d/R)', 'Only inner sphere of radius R − d attracts (2); M_s = M(R − d)³/R³ (1); g_d = GM_s/(R − d)² = g(1 − d/R) (2).'),
    ('Derive the orbital speed and time period of a satellite at height h above the Earth\'s surface.', 'v = √(GM/(R + h)); T = 2π√((R + h)³/GM)', 'mv²/r = GMm/r² (2); v (1); T = 2πr/v (2).'),
])


# st4 energy of an orbiting satellite; geostationary satellites

c7s4_tf = tf_mcq('an orbiting satellite',
                 ['The total energy of a satellite in a circular orbit is negative.', 'The kinetic energy of a satellite is half the magnitude of its potential energy.', 'A geostationary satellite has a period of 24 h and orbits in the equatorial plane.',
                  'A polar satellite passes over the poles and scans the whole Earth over a day.'],
                 ['The total energy of a satellite in orbit is positive.', 'A geostationary satellite orbits from pole to pole.', 'The kinetic energy of a satellite equals its potential energy.',
                  'A geostationary satellite orbits about 600 km above the Earth.'])

c7s4_explain = pool_txt([
    ('Why must a geostationary satellite be placed in the equatorial plane and move from west to east?', 'To stay above the same point it must rotate with the Earth, about the Earth\'s axis, with the same sense and period (24 h).', 'Equatorial plane (1 mark); same sense and period (1 mark).'),
    ('Why is the total energy of a bound satellite negative?', 'E = K + U = GMm/2r − GMm/r = −GMm/2r; it is bound, so energy must be supplied to free it.', 'Expression (1 mark); bound system (1 mark).'),
    ('State one use each of geostationary and polar satellites.', 'Geostationary: communication/TV broadcasting (e.g. INSAT/GSAT); polar: remote sensing, weather and mapping.', 'Each 1 mark.'),
])

c7s4_ar = pool_ar([
    ('The kinetic energy of a satellite is half the magnitude of its potential energy.', 'For a circular orbit, mv²/r = GMm/r².', 'a', 'R gives K = GMm/2r and U = −GMm/r.'),
    ('A geostationary satellite appears fixed in the sky.', 'Its period equals the Earth\'s rotation period and it orbits in the equatorial plane in the same sense.', 'a', 'R explains A.'),
    ('Moving a satellite to a higher orbit decreases its total energy.', 'E = −GMm/2r.', 'd', 'A is false: E becomes less negative (increases); R is true.'),
])


def c7s4_energy(r):
    m = r.choice([200, 400, 500, 1000, 1200])
    h = r.choice([400, 600, 1000, 1600])
    rr = RE + h * 1000
    K = GC * ME * m / (2 * rr)
    return {'stem': f'A {m} kg satellite orbits the Earth at a height of {h} km. Find its kinetic, potential and total energy. (G = 6.67 × 10⁻¹¹ N m² kg⁻², M = 6.0 × 10²⁴ kg, R = 6400 km)',
            'answer': f'K = {sig(K)} J, U = {sig(-2 * K)} J, E = {sig(-K)} J', 'key': f'r = {g(rr)} m; K = GMm/2r = {sig(K)} J (1); U = −GMm/r = {sig(-2 * K)} J (1); E = −GMm/2r = {sig(-K)} J (1).'}


def c7s4_raise(r):
    m = r.choice([200, 400, 500, 1000])
    k1, k2 = r.choice([(2, 4), (2, 3), (1.5, 3), (3, 6)])
    r1, r2 = k1 * RE, k2 * RE
    W = GC * ME * m / 2 * (1 / r1 - 1 / r2)
    return NUM(f'How much energy must be supplied to shift a satellite of mass {m} kg from a circular orbit of radius {g(k1)}R to one of radius {g(k2)}R around the Earth? (G = 6.67 × 10⁻¹¹ N m² kg⁻², M = 6.0 × 10²⁴ kg, R = 6.4 × 10⁶ m)',
               W, 'J', f'ΔE = −GMm/2r₂ − (−GMm/2r₁) = (GMm/2)(1/r₁ − 1/r₂) = {{ans}}.', wrongs=[2 * W, GC * ME * m * (1 / r1 - 1 / r2) * 1.5, W / 2])


c7s4_geo = pool_mcq([
    ('The period of a geostationary satellite is', '24 hours', ['12 hours', '1 hour', '27.3 days'], 'It must rotate with the Earth.'),
    ('A geostationary satellite orbits at a height of about', '36,000 km above the Earth', ['600 km above the Earth', '6,400 km above the Earth', '3,84,000 km above the Earth'], 'r ≈ 42,000 km from the centre, about 36,000 km above the surface.'),
    ('Polar satellites are used mainly for', 'remote sensing and weather monitoring', ['live television broadcasting to a fixed dish', 'global positioning only', 'holding the Moon in orbit'], 'They scan strips of the Earth on each pass.'),
    ('The total energy of a satellite in a circular orbit of radius r is', '−GMm/2r', ['−GMm/r', '+GMm/2r', 'zero'], 'E = K + U = GMm/2r − GMm/r.'),
])


def c7s4_case(r):
    m = r.choice([1500, 2000, 2500, 3000])
    who = name(r)
    rr = 4.22e7
    v = math.sqrt(GC * ME / rr)
    return {'stem': (f'{who} reads that ISRO\'s communication satellite GSAT has a mass of about {m} kg and is placed in a geostationary orbit of radius about 42,200 km from the Earth\'s centre. (G = 6.67 × 10⁻¹¹ N m² kg⁻², M = 6.0 × 10²⁴ kg)\n'
                     '(i) What is its period? (ii) Find its orbital speed. (iii) Find its total energy. (iv) Why is a geostationary orbit useful for TV broadcasting?'),
            'answer': f'(i) 24 h (ii) {sig(v / 1000)} km s⁻¹ (iii) {sig(-GC * ME * m / (2 * rr))} J (iv) Dish antennas can point at a fixed spot in the sky',
            'key': f'(i) 24 h (1). (ii) √(GM/r) (1). (iii) −GMm/2r (1). (iv) appears stationary, so fixed dishes work (1).'}


# ======================================================== ch08 Mechanical Properties of Solids
# st1 stress, strain, stress-strain curve

c8s1_terms = term_mcq([('elastic limit (yield point)', 'the stress beyond which the body does not regain its original dimensions'), ('proportional limit', 'the point up to which stress is proportional to strain'),
                       ('ultimate tensile strength', 'the maximum stress a material can withstand before it begins to fail'), ('fracture point', 'the point at which the wire breaks'),
                       ('permanent set', 'the deformation that remains when the load is removed after crossing the elastic limit')],
                      'On a stress-strain curve, what is meant by the {a}?', 'What is the name for {b}?', '{a}: {b}.')

c8s1_tf = tf_mcq('stress and strain',
                 ['Strain has no unit.', 'Stress has the same unit as pressure.', 'Ductile materials have a large plastic region before fracture.', 'Within the proportional limit, stress is proportional to strain.'],
                 ['Strain is measured in N m⁻².', 'Brittle materials have a large plastic region.', 'Stress is a dimensionless quantity.', 'Rubber is more elastic than steel.'])

c8s1_explain = pool_txt([
    ('Steel is said to be more elastic than rubber. Explain.', 'For the same stress steel has a much smaller strain, so its Young\'s modulus (and restoring tendency) is much larger.', 'Y = stress/strain (1 mark); steel has larger Y (1 mark).'),
    ('Distinguish between ductile and brittle materials using the stress-strain curve.', 'Ductile materials (copper) have a large gap between elastic limit and fracture; brittle materials (glass) fracture soon after the elastic limit.', 'Each with curve feature 1 mark.'),
    ('What are elastomers? Give an example and a feature of their stress-strain curve.', 'Substances like rubber or the aorta tissue that can be stretched to large strains; the curve has no well-defined linear region.', 'Definition/example (1 mark); curve feature (1 mark).'),
])

c8s1_ar = pool_ar([
    ('Strain is a dimensionless quantity.', 'Strain is the ratio of change in dimension to original dimension.', 'a', 'R explains A.'),
    ('Glass is a brittle material.', 'Glass fractures soon after its elastic limit is crossed.', 'a', 'R explains A.'),
    ('Rubber is more elastic than steel.', 'Rubber can be stretched much more than steel.', 'd', 'A is false (steel has much larger Y); R is true.'),
])


def c8s1_stress(r):
    m = r.choice([5, 10, 20, 50, 100])
    d = r.choice([0.5, 0.8, 1, 1.5, 2])
    L, dL = r.choice([1, 2, 2.5, 3]), r.choice([0.2, 0.3, 0.5, 0.8, 1.0])
    A = math.pi * (d / 2000) ** 2
    st = m * G / A
    return NUM2(f'A wire of diameter {g(d)} mm and length {g(L)} m hangs vertically with a {m} kg load. It stretches by {g(dL)} mm. Find the stress and the strain in the wire. (g = 9.8 m s⁻²)',
                (st, dL / 1000 / L), ('N m⁻²', ''), f'A = πd²/4 = {sig(A)} m² (1); stress = mg/A = {sig(st)} N m⁻² (1); strain = ΔL/L = {g(dL / 1000)}/{g(L)} = {sig(dL / 1000 / L)} (1).',
                wrongs=[(m * G / (math.pi * (d / 1000) ** 2), dL / L), (m / A, dL / 1000 / L), (st, L / dL)])


def c8s1_simple(r):
    F_ = r.choice([100, 200, 500, 1000, 2000])
    A = r.choice([1, 2, 4, 5])
    return NUM(f'A force of {F_} N is applied normally to a rod of cross-sectional area {A} mm². What is the stress?', F_ / (A * 1e-6), 'N m⁻²', f'Stress = F/A = {F_}/({A} × 10⁻⁶) = {{ans}}.', wrongs=[F_ / A, F_ * A, F_ / (A * 1e-3)])


def c8s1_load(r):
    mat, bs = r.choice([('steel', 4.0e8), ('copper', 2.2e8), ('aluminium', 1.1e8), ('brass', 3.0e8)])
    d = r.choice([0.5, 1, 1.5, 2])
    A = math.pi * (d / 2000) ** 2
    m = bs * A / G
    return NUM(f'The breaking stress of {mat} is about {g(bs)} N m⁻². What is the largest mass that can be hung from a {mat} wire of diameter {g(d)} mm without breaking it? (g = 9.8 m s⁻²)', m, 'kg',
               f'F_max = σA = {g(bs)} × π({g(d / 2000)})² = {sig(bs * A)} N; m = F/g = {{ans}}.', wrongs=[bs * math.pi * (d / 1000) ** 2 / G, bs * A, m * 2])


def c8s1_graph(r):
    mat = r.choice(['steel', 'copper', 'aluminium', 'brass'])
    Y = {'steel': 2.0e11, 'copper': 1.1e11, 'aluminium': 0.7e11, 'brass': 0.9e11}[mat]
    s1 = r.choice([1, 1.5, 2, 2.5]) * 1e8
    e1 = float(f'{s1 / Y:.1e}')
    ys = round(r.choice([2.5, 3, 3.5]) * s1 / 1e8, 1) * 1e8
    return {'stem': f'The linear part of the stress-strain graph of a {mat} wire passes through the origin and the point (strain {sig(e1, 2)}, stress {g(s1)} N m⁻²). The yield strength is about {g(ys)} N m⁻². '
                    '(i) Find Young\'s modulus. (ii) Find the strain at a stress of half the yield strength. (iii) What happens if the stress exceeds the yield strength?',
            'answer': f'(i) {sig(s1 / e1, 2)} N m⁻² (ii) {sig(ys / 2 / (s1 / e1), 2)} (iii) the wire is permanently deformed (plastic region)',
            'key': f'(i) Y = slope = stress/strain (1). (ii) strain = (ys/2)/Y (1). (iii) beyond yield point it does not regain its length (1).'}


# st2 Hooke's law and elastic moduli

c8s2_terms = term_mcq([('Young\'s modulus', 'longitudinal stress ÷ longitudinal strain'), ('bulk modulus', 'hydraulic stress ÷ volume strain, B = −p/(ΔV/V)'),
                       ('shear modulus (modulus of rigidity)', 'shearing stress ÷ shearing strain'), ('compressibility', 'the reciprocal of bulk modulus, 1/B')],
                      'Which statement defines the {a}?', 'Which elastic quantity is {b}?', '{a}: {b}.')

c8s2_tf = tf_mcq('Hooke\'s law and elastic moduli',
                 ['Hooke\'s law holds only within the proportional limit.', 'Young\'s modulus is a property of the material, not of the shape of the wire.', 'Fluids have a bulk modulus but no shear modulus.',
                  'Solids are much less compressible than gases.'],
                 ['Young\'s modulus of a wire doubles when its length is doubled.', 'Liquids have a large shear modulus.', 'Hooke\'s law holds up to the fracture point.',
                  'Gases are the least compressible of all states of matter.'])

c8s2_explain = pool_txt([
    ('Two wires of the same material, one twice as thick as the other, carry the same load. Compare their extensions if their lengths are equal.', 'The thicker wire stretches one-fourth as much.', 'ΔL = FL/(AY) (1 mark); A ∝ d² (1 mark).'),
    ('Why does Young\'s modulus not depend on the length or area of a wire?', 'It is a ratio of stress to strain, both of which already account for size; it depends only on the material (and temperature).', '2 marks for reasoning.'),
    ('Why do liquids and gases have no shear modulus?', 'Fluids cannot sustain a shearing stress; they flow under it.', 'Fluids flow (2 marks).'),
])

c8s2_ar = pool_ar([
    ('For a given load, a thicker wire of the same material stretches less.', 'Extension ΔL = FL/(AY) is inversely proportional to the cross-sectional area.', 'a', 'R explains A.'),
    ('Young\'s modulus of a wire depends on its length.', 'Longer wires stretch more under the same load.', 'd', 'A is false (Y is a material property); R is true.'),
    ('Liquids have zero shear modulus.', 'Liquids cannot sustain shearing stress.', 'a', 'R explains A.'),
])

YM = [('steel', 2.0e11), ('copper', 1.1e11), ('aluminium', 0.70e11), ('brass', 0.91e11), ('iron', 1.9e11)]


def c8s2_extension(r):
    mat, Y = r.choice(YM)
    m = r.choice([5, 10, 20, 50, 100])
    L = r.choice([1, 2, 3, 4, 5])
    d = r.choice([1, 2, 3, 4])
    A = math.pi * (d / 2000) ** 2
    dL = m * G * L / (A * Y)
    return NUM(f'A {mat} wire {L} m long and {d} mm in diameter supports a load of {m} kg. Find the extension. (Y = {g(Y)} N m⁻², g = 9.8 m s⁻²)', dL * 1000, 'mm',
               f'ΔL = FL/(AY) = {g(m * G)} × {L}/({sig(A)} × {g(Y)}) = {sig(dL)} m = {{ans}}.', wrongs=[m * G * L / (math.pi * (d / 1000) ** 2 * Y) * 1000, m * L / (A * Y) * 1000, dL * 1000 * L])


def c8s2_young(r):
    L = r.choice([1, 1.5, 2, 2.5, 3])
    d = r.choice([0.5, 0.6, 0.8, 1.0])
    m = r.choice([2, 4, 5, 6, 8])
    A = math.pi * (d / 2000) ** 2
    Y0 = r.choice([2.0e11, 1.1e11, 0.9e11, 0.7e11])
    dL = float(f'{m * G * L / (A * Y0) * 1000:.1e}')
    Y = m * G * L / (A * dL / 1000)
    who = name(r)
    return NUM(f'In a Searle\'s apparatus experiment, {who} finds that a wire of length {g(L)} m and diameter {g(d)} mm extends by {g(dL)} mm when a load of {m} kg is added. Find Young\'s modulus of the material. (g = 9.8 m s⁻²)',
               Y, 'N m⁻²', f'Y = FL/(AΔL) = {g(m * G)} × {g(L)}/({sig(A)} × {g(dL / 1000)}) = {{ans}}.', wrongs=[m * G * L / (math.pi * (d / 1000) ** 2 * dL / 1000), m * L / (A * dL / 1000), Y / L])


def c8s2_series(r):
    m = r.choice([10, 14, 20, 25])
    L1, L2 = r.choice([(1.5, 1.0), (2.0, 1.5), (1.0, 1.0), (2.5, 2.0)])
    d = r.choice([0.25, 0.5, 1.0])
    A = math.pi * (d / 2000) ** 2
    e1 = m * G * L1 / (A * 2.0e11)
    e2 = m * G * L2 / (A * 1.1e11)
    return {'stem': f'A steel wire of length {g(L1)} m and a copper wire of length {g(L2)} m, both of diameter {g(d)} mm, are joined end to end. The combination is loaded with {m} kg. Find the extension of each wire. (Y_steel = 2.0 × 10¹¹ N m⁻², Y_copper = 1.1 × 10¹¹ N m⁻², g = 9.8 m s⁻²)',
            'answer': f'Steel {sig(e1 * 1000)} mm; copper {sig(e2 * 1000)} mm', 'key': f'Same tension {g(m * G)} N in both (1); A = {sig(A)} m² (0.5); ΔL = FL/(AY): steel {sig(e1)} m, copper {sig(e2)} m (1.5).'}


def c8s2_bulk(r):
    depth = r.choice([1000, 2000, 3000, 4000, 6000])
    B = 2.2e9
    p = 1000 * G * depth
    return NUM(f'A submarine-research team lowers a water sample to a depth of {depth} m in the Bay of Bengal. Estimate the fractional compression ΔV/V of the water there. (Bulk modulus of water = 2.2 × 10⁹ N m⁻², density 1000 kg m⁻³, g = 9.8 m s⁻²; ignore atmospheric pressure)',
               p / B, '', f'p = ρgh = {sig(p)} Pa (1); ΔV/V = p/B = {sig(p)}/2.2 × 10⁹ = {{ans}} (2).', wrongs=[B / p, p / B * 100, 1000 * depth / B])


def c8s2_shear(r):
    L = r.choice([0.5, 0.6, 1.0])
    F_ = r.choice([1e4, 5e4, 9.4e4, 1e5])
    Gm = r.choice([(25e9, 'aluminium'), (79e9, 'steel'), (42e9, 'copper')])
    dx = F_ * L / (L * L * Gm[0])
    return NUM(f'A cube of {Gm[1]} of side {g(L * 100)} cm has its lower face fixed. A tangential force of {g(F_)} N acts on the top face. Find the lateral displacement of the top face. (Shear modulus = {g(Gm[0])} N m⁻²)',
               dx * 1000, 'mm', f'Shear strain Δx/L = F/(AG) ⇒ Δx = FL/(AG) = {g(F_)} × {g(L)}/({g(L * L)} × {g(Gm[0])}) = {sig(dx)} m = {{ans}}.', wrongs=[F_ / (L * L * Gm[0]) * 1000, F_ * L / Gm[0] * 1000, dx * 1e6])


def c8s2_rod(r):
    L = r.choice([1.05, 1.2, 1.5, 2.0])
    ratio = r.choice([2, 1.5, 3])
    YsYa = 2.0 / 0.7
    x_stress = L / (1 + ratio)
    x_strain = L / (1 + ratio * YsYa)
    return {'stem': f'A light rod of length {g(L)} m is supported at its ends by two wires of equal length, steel (A) and aluminium (B). The cross-sectional area of A is {g(ratio)} times that of B. '
                    'At what distance from A should a mass be hung to produce (i) equal stresses and (ii) equal strains in the two wires? (Y_steel = 2.0 × 10¹¹ N m⁻², Y_Al = 7.0 × 10¹⁰ N m⁻²)',
            'answer': f'(i) {sig(x_stress)} m from A (ii) {sig(x_strain)} m from A',
            'key': f'Let x from A. Moments: T_A x = T_B (L − x) (1). (i) equal stress ⇒ T_A/T_B = A_A/A_B = {g(ratio)} ⇒ x = L/(1 + {g(ratio)}) = {sig(x_stress)} m (2). '
                   f'(ii) equal strain ⇒ T_A/T_B = (A_A Y_A)/(A_B Y_B) = {g(ratio * YsYa)} ⇒ x = {sig(x_strain)} m (2).', 'gap': 'G5'}


def c8s2_case(r):
    who = name(r)
    m = r.choice([1000, 1500, 2000])
    n = r.choice([4, 6, 8])
    d = r.choice([10, 12, 15])
    A = math.pi * (d / 2000) ** 2
    L = r.choice([10, 15, 20])
    st = m * G / n / A
    return {'stem': (f'{who} visits a construction site where a lift cage of mass {m} kg hangs from {n} identical steel cables, each {d} mm in diameter and {L} m long. (Y = 2.0 × 10¹¹ N m⁻², g = 9.8 m s⁻²)\n'
                     '(i) Find the tension in each cable. (ii) Find the stress in each cable. (iii) Find the extension of each cable. (iv) Why are several thin cables used instead of one thick rod?'),
            'answer': f'(i) {sig(m * G / n)} N (ii) {sig(st)} N m⁻² (iii) {sig(st * L / 2e11 * 1000)} mm (iv) cables are flexible, easy to handle and failure of one does not cause collapse',
            'key': f'(i) mg/n (1). (ii) T/A (1). (iii) stress × L/Y (1). (iv) flexibility and safety (1).'}


# st3 applications of elastic behaviour

c8s3_tf = tf_mcq('applications of elasticity',
                 ['Beams used in buildings are often I-shaped.', 'Crane ropes are made of many thin wires twisted together.', 'The sag of a beam decreases sharply as its depth increases.',
                  'The height of mountains on Earth is limited by the elastic properties of rocks.'],
                 ['A beam sags less when it is laid on its broad face than on its narrow edge.', 'Crane ropes are made from a single thick steel rod for flexibility.',
                  'The sag of a beam is independent of its length.', 'Mountains on Earth can be of any height.'])

c8s3_explain = pool_txt([
    ('Why are girders and rails given an I-shaped cross-section?', 'The I-section puts most material far from the neutral axis, giving large resistance to bending with less material and weight.', 'Bending resistance (1 mark); saving material (1 mark).'),
    ('Why are crane ropes made of a number of thin wires braided together rather than one thick wire?', 'They have the same strength but are flexible and easier to handle; damage to one wire does not cause failure.', 'Flexibility (1 mark); safety/strength (1 mark).'),
    ('Why does a beam bend less when laid on its narrow edge than on its broad face?', 'Sag δ ∝ 1/(b d³); laying on edge increases the depth d, which reduces sag greatly.', 'δ ∝ 1/(bd³) (1 mark); larger d (1 mark).'),
])

c8s3_ar = pool_ar([
    ('A beam bends less when its depth is increased than when its breadth is increased by the same factor.', 'The sag of a beam is proportional to 1/(bd³).', 'a', 'R explains A.'),
    ('Mountains on Earth cannot be much higher than about 10 km.', 'Rock at the base would flow under the stress if the mountain were much higher.', 'a', 'R explains A.'),
    ('An I-shaped girder bends more than a solid rectangular one of the same mass.', 'The I-section concentrates material away from the neutral axis.', 'd', 'A is false; R is true.'),
])


def c8s3_rope(r):
    m = r.choice([5000, 10000, 20000])
    sy = 300e6
    sf = r.choice([1, 2])
    rad = math.sqrt(m * G * sf / (math.pi * sy))
    return NUM(f'A crane must lift a load of {m // 1000} tonne. The yield strength of steel is 300 × 10⁶ N m⁻². Find the minimum radius of the steel rope{" with a safety factor of 2" if sf == 2 else ""}. (g = 9.8 m s⁻²)',
               rad * 100, 'cm', f'πr² σ_y ≥ {sf if sf > 1 else ""}mg ⇒ r = √({sf if sf > 1 else ""}mg/(πσ_y)) = {sig(rad)} m = {{ans}}.'.replace('≥ mg', '≥ mg'), wrongs=[rad * 100 * 2, m * G / (math.pi * sy) * 100, rad * 1000])


def c8s3_sag(r):
    fd, fb, fl = r.choice([(2, 1, 1), (1, 2, 1), (1, 1, 2), (2, 2, 1), (1, 1, 0.5)])
    f = fl ** 3 / (fb * fd ** 3)
    ch = []
    if fd != 1:
        ch.append(f'depth {"doubled" if fd == 2 else "halved"}')
    if fb != 1:
        ch.append(f'breadth {"doubled" if fb == 2 else "halved"}')
    if fl != 1:
        ch.append(f'length {"doubled" if fl == 2 else "halved"}')
    return NUM(f'The sag of a beam loaded at its centre is δ = Wl³/(4bd³Y). By what factor does the sag change if the {" and ".join(ch)} (same load)?', f, '',
               f'δ ∝ l³/(bd³) ⇒ factor = {g(fl)}³/({g(fb)} × {g(fd)}³) = {{ans}}.', wrongs=[1 / f, fl / (fb * fd), f * 2])


def c8s3_mountain(r):
    sy = r.choice([3.0e8, 2.5e8, 3.2e8])
    rho = r.choice([2700, 3000, 3200])
    h = sy / (rho * G)
    return {'stem': f'Rock at the base of a mountain begins to flow when the stress exceeds about {g(sy)} N m⁻². If the density of rock is {rho} kg m⁻³, estimate the maximum height of a mountain on Earth. Why could mountains on Mars (g ≈ 3.7 m s⁻²) be taller? (g = 9.8 m s⁻²)',
            'answer': f'About {sig(h / 1000, 2)} km; on Mars smaller g means a taller column for the same stress',
            'key': f'Stress at base = hρg (1); hρg ≤ σ ⇒ h = σ/(ρg) = {g(sy)}/({rho} × 9.8) = {sig(h)} m ≈ {sig(h / 1000, 2)} km (1); h ∝ 1/g, so mountains on Mars can be about 2.6 times taller (Olympus Mons ≈ 22 km) (1).'}


c8s3_mcq = pool_mcq([
    ('Bridges are designed with an allowance for elastic behaviour mainly because they must', 'bear changing loads without permanent deformation', ['look attractive', 'reduce the cost of paint', 'become lighter with time'], 'Stresses must stay below the elastic limit.'),
    ('For a beam of rectangular cross-section, the property that most reduces bending for a given amount of material is a', 'large depth', ['large breadth', 'large length', 'small depth'], 'δ ∝ 1/d³.'),
    ('The maximum height of a mountain on Earth is of the order of', '10 km', ['1 km', '100 km', '1000 km'], 'Shear stress at the base limits the height to about 10 km.'),
])


# ======================================================== ch09 Mechanical Properties of Fluids
# st1 pressure, Pascal's law, hydraulic machines

c9s1_tf = tf_mcq('pressure in fluids',
                 ['Pressure at a point in a fluid at rest is the same in all directions.', 'Pressure in a liquid increases linearly with depth.', 'The pressure at a given depth does not depend on the shape of the container.',
                  'Pascal\'s law is the principle behind the hydraulic lift.'],
                 ['Pressure in a liquid is independent of depth.', 'Pressure at the bottom of a vessel depends on the area of its base.', 'Pressure is a vector quantity.',
                  'A hydraulic lift multiplies energy.'])

c9s1_explain = pool_txt([
    ('Why are dams made thicker at the bottom?', 'Water pressure increases with depth (P = ρgh), so the bottom must withstand the greatest force.', 'P ∝ h (1 mark); design (1 mark).'),
    ('State Pascal\'s law and explain how a hydraulic lift works.', 'Pressure applied to an enclosed fluid is transmitted undiminished to every part; a small force on a small piston creates a large force on a larger piston (F₂ = F₁A₂/A₁).', 'Statement (1 mark); application (1 mark).'),
    ('Why does a dropper or syringe work, in terms of pressure?', 'Pressing the bulb lowers the pressure inside when released; atmospheric pressure pushes the liquid in.', 'Pressure difference (2 marks).'),
    ('Why is it painful to stand on a pointed nail but not on a flat board with many nails?', 'The same weight spread over many points gives a much smaller pressure.', 'P = F/A (1 mark); larger area (1 mark).'),
])

c9s1_ar = pool_ar([
    ('A hydraulic lift can lift a car with a small force.', 'Pressure applied to an enclosed liquid is transmitted equally in all directions.', 'a', 'Pascal\'s law gives F₂ = F₁A₂/A₁; R explains A.'),
    ('The pressure at the bottom of a tank depends on the area of the base.', 'Pressure = force/area.', 'd', 'A is false (P = P₀ + ρgh); R is true.'),
    ('Dams are thicker at the base.', 'Pressure in a liquid increases with depth.', 'a', 'R explains A.'),
])


def c9s1_depth(r):
    h = r.choice([5, 10, 20, 50, 100, 1000])
    rho = r.choice([1000, 1030])
    liq = 'fresh water' if rho == 1000 else 'sea water'
    P = 1.01e5 + rho * G * h
    return NUM2(f'Find the absolute pressure and the gauge pressure at a depth of {h} m in {liq} (density {rho} kg m⁻³). (Atmospheric pressure = 1.01 × 10⁵ Pa, g = 9.8 m s⁻²)', (P, rho * G * h), ('Pa', 'Pa'),
                f'Gauge P = ρgh = {rho} × 9.8 × {h} = {sig(rho * G * h)} Pa; absolute = P₀ + ρgh = {sig(P)} Pa.',
                wrongs=[(rho * G * h, P), (1.01e5 + rho * h, rho * h), (1.01e5 * h, rho * G * h)])


def c9s1_lift(r):
    r1, r2 = r.choice([(1, 10), (2, 20), (1.5, 15), (2, 25), (5, 50)])
    m = r.choice([1000, 1200, 1500, 3000])
    F1 = m * G * (r1 / r2) ** 2
    return NUM(f'In a car service station hydraulic lift, the small piston has a radius of {g(r1)} cm and the large piston {g(r2)} cm. What force on the small piston can lift a car of mass {m} kg? (g = 9.8 m s⁻²)',
               F1, 'N', f'F₁/A₁ = F₂/A₂ ⇒ F₁ = mg (r₁/r₂)² = {g(m * G)} × ({g(r1)}/{g(r2)})² = {{ans}}.', wrongs=[m * G * r1 / r2, m * G * (r2 / r1) ** 2, m * (r1 / r2) ** 2])


def c9s1_utube(r):
    liq, rho = r.choice([('oil', 800), ('kerosene', 810), ('spirit', 790), ('turpentine', 870)])
    h = r.choice([10, 12, 15, 20])
    hw = h * rho / 1000
    return NUM(f'Water is poured into a U-tube and then {liq} (density {rho} kg m⁻³) is poured into one arm. The {liq} column is {h} cm high. How high is the water column in the other arm above the interface level?', hw, 'cm',
               f'Pressures equal at the interface level: ρ_o g h_o = ρ_w g h_w ⇒ h_w = {h} × {rho}/1000 = {{ans}}.', wrongs=[h * 1000 / rho, h, h - hw])


def c9s1_heel(r):
    m = r.choice([45, 50, 55, 60])
    A = r.choice([0.5, 1, 1.5, 2])
    return NUM(f'A {m} kg girl balances on one heel of area {g(A)} cm². What pressure does the heel exert on the floor? (g = 9.8 m s⁻²)', m * G / (A * 1e-4), 'Pa',
               f'P = F/A = {g(m * G)}/({g(A)} × 10⁻⁴) = {{ans}}.', wrongs=[m / (A * 1e-4), m * G / A, m * G / (A * 1e-2)])


def c9s1_barometer(r):
    hm = r.choice([76, 75, 74, 72, 70])
    P = 13600 * G * hm / 100
    return {'stem': f'At a hill station the mercury barometer reads {hm} cm. (i) What is the atmospheric pressure there in pascal? (ii) How tall would a water barometer be at the same place? (density of mercury 13,600 kg m⁻³, of water 1000 kg m⁻³, g = 9.8 m s⁻²)',
            'answer': f'(i) {sig(P)} Pa (ii) {sig(P / (1000 * G))} m', 'key': f'(i) P = ρgh = 13600 × 9.8 × {g(hm / 100)} = {sig(P)} Pa (1.5). (ii) h_w = P/(ρ_w g) = {sig(P / (1000 * G))} m (1.5).'}


# st2 streamline flow, continuity, Bernoulli

c9s2_tf = tf_mcq('streamline flow and Bernoulli\'s principle',
                 ['In steady flow the velocity at a given point does not change with time.', 'Two streamlines can never cross.', 'For an incompressible fluid, Av = constant along a tube of flow.',
                  'Where the speed of a fluid increases, its pressure decreases (same height).'],
                 ['Where the speed of a fluid increases, its pressure also increases.', 'Two streamlines can cross each other.', 'Water flows faster in the wider part of a pipe.',
                  'Bernoulli\'s principle applies to viscous turbulent flow without change.'])

c9s2_terms = term_mcq([('streamline (steady) flow', 'the velocity of the fluid at each point does not change with time'), ('turbulent flow', 'irregular flow with eddies, occurring above a critical speed'),
                       ('equation of continuity', 'A v = constant for an incompressible fluid'), ('Bernoulli\'s principle', 'P + ½ρv² + ρgh = constant along a streamline')],
                      'Which statement describes {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c9s2_explain = pool_txt([
    ('Why does the speed of water increase when you partly close the mouth of a garden hose with your thumb?', 'By the equation of continuity, Av is constant; reducing A increases v.', 'A₁v₁ = A₂v₂ (1 mark); smaller A, larger v (1 mark).'),
    ('Why are roofs sometimes blown off during a storm?', 'Fast wind over the roof lowers the pressure above it (Bernoulli); the higher pressure inside pushes the roof up.', 'Pressure difference (2 marks).'),
    ('How does an aeroplane wing produce lift?', 'Its shape makes air flow faster over the top, so pressure above is lower than below; the pressure difference gives an upward force.', 'Faster flow on top (1 mark); pressure difference (1 mark).'),
    ('Explain why two ships moving side by side close together tend to be drawn towards each other.', 'Water between them flows faster, lowering the pressure; higher pressure outside pushes them together.', '2 marks.'),
])

c9s2_ar = pool_ar([
    ('Water comes out faster when the mouth of a hose is narrowed.', 'For an incompressible fluid A v is constant.', 'a', 'R explains A.'),
    ('Wind blowing fast over a tin roof can lift it.', 'The pressure is lower where the air speed is higher.', 'a', 'R explains A.'),
    ('In steady flow, streamlines can intersect.', 'At any point the fluid has a unique velocity in steady flow.', 'd', 'A is false; R is true (and shows why they cannot cross).'),
    ('The speed of efflux from a hole at depth h is √(2gh).', 'It equals the speed of a body falling freely through h.', 'b', 'Both true; R is a comparison, not the explanation (Bernoulli\'s equation is).'),
])


def c9s2_cont(r):
    d1, d2 = r.choice([(4, 2), (6, 3), (10, 5), (8, 4), (3, 1.5), (5, 2)])
    v1 = r.choice([0.5, 1, 1.5, 2, 2.5])
    v2 = v1 * (d1 / d2) ** 2
    return NUM(f'Water flows through a horizontal pipe whose diameter changes from {g(d1)} cm to {g(d2)} cm. If the speed in the wider part is {g(v1)} m s⁻¹, find the speed in the narrower part.', v2, 'm s⁻¹',
               f'A₁v₁ = A₂v₂ ⇒ v₂ = v₁(d₁/d₂)² = {g(v1)} × ({g(d1)}/{g(d2)})² = {{ans}}.', wrongs=[v1 * d1 / d2, v1 * (d2 / d1) ** 2, v1 * (d1 / d2) ** 3])


def c9s2_efflux(r):
    h = r.choice([0.8, 1.25, 2, 2.5, 3.2, 5, 4.9])
    v = math.sqrt(2 * G * h)
    return NUM(f'A water tank on the roof has a small hole {g(h)} m below the water surface. Find the speed of efflux of water from the hole. (g = 9.8 m s⁻²)', v, 'm s⁻¹',
               f'Torricelli\'s law: v = √(2gh) = √(2 × 9.8 × {g(h)}) = {{ans}}.', wrongs=[math.sqrt(G * h), 2 * G * h, G * h])


def c9s2_venturi(r):
    d1, d2 = r.choice([(4, 2), (6, 3), (10, 5), (5, 2.5)])
    v1 = r.choice([0.5, 1, 1.5, 2])
    v2 = v1 * (d1 / d2) ** 2
    dP = 0.5 * 1000 * (v2 * v2 - v1 * v1)
    return {'stem': f'Water (density 1000 kg m⁻³) flows through a Venturi meter whose main pipe has diameter {g(d1)} cm and throat {g(d2)} cm. The speed in the main pipe is {g(v1)} m s⁻¹. Find the speed at the throat and the pressure difference between the main pipe and the throat.',
            'answer': f'{sig(v2)} m s⁻¹; {sig(dP)} Pa', 'key': f'v₂ = v₁(d₁/d₂)² = {sig(v2)} m s⁻¹ (1); P₁ − P₂ = ½ρ(v₂² − v₁²) = ½ × 1000 × ({g(v2 * v2)} − {g(v1 * v1)}) = {sig(dP)} Pa (2).'}


def c9s2_wing(r):
    v1, v2 = r.choice([(70, 63), (80, 72), (100, 90), (60, 54)])
    A = r.choice([20, 25, 30, 40])
    rho = 1.3
    dP = 0.5 * rho * (v1 * v1 - v2 * v2)
    return {'stem': f'Air (density 1.3 kg m⁻³) flows over the top surface of an aircraft wing at {v1} m s⁻¹ and over the bottom surface at {v2} m s⁻¹. The wing area is {A} m². Find the pressure difference and the lift on the wing.',
            'answer': f'{sig(dP)} Pa; {sig(dP * A)} N', 'key': f'ΔP = ½ρ(v_top² − v_bottom²) = ½ × 1.3 × ({v1 * v1} − {v2 * v2}) = {sig(dP)} Pa (2); lift = ΔP × A = {sig(dP * A)} N (1).'}


def c9s2_pipe(r):
    P1 = r.choice([1.5, 2, 2.5, 3]) * 1e5
    v1 = r.choice([1, 2, 3])
    k = r.choice([2, 3, 4])
    v2 = v1 * k
    P2 = P1 - 0.5 * 1000 * (v2 * v2 - v1 * v1)
    return {'stem': f'Water flows steadily through a horizontal pipe. At point A the pressure is {g(P1)} Pa and the speed {v1} m s⁻¹. At point B the cross-sectional area is 1/{k} of that at A. Find the speed and pressure at B.',
            'answer': f'{v2} m s⁻¹; {sig(P2)} Pa', 'key': f'Continuity: v_B = {k} × {v1} = {v2} m s⁻¹ (1). Bernoulli: P_B = P_A − ½ρ(v_B² − v_A²) = {g(P1)} − {g(0.5 * 1000 * (v2 * v2 - v1 * v1))} = {sig(P2)} Pa (2).'}


def c9s2_tank(r):
    H = r.choice([2, 3, 4, 5])
    hh = round(H * r.choice([0.25, 0.4, 0.5, 0.6]), 2)
    d = H - hh
    x = 2 * math.sqrt(hh * d)
    return {'stem': f'A cylindrical tank stands on the ground and holds water up to a height of {H} m. A small hole is made in its side {g(hh)} m below the water surface. (i) Find the speed of efflux. (ii) How far from the tank does the jet strike the ground? (iii) At what depth below the surface should the hole be to give the maximum range?',
            'answer': f'(i) {sig(math.sqrt(2 * G * hh))} m s⁻¹ (ii) {sig(x)} m (iii) {g(H / 2)} m (range {g(H)} m)',
            'key': f'(i) v = √(2gh) with h = {g(hh)} m (1). (ii) hole is {g(d)} m above ground; t = √(2 × {g(d)}/g); x = vt = 2√(h(H − h)) = {sig(x)} m (2). (iii) x is maximum when h = H/2 = {g(H / 2)} m, giving x = H (2).', 'gap': 'G5'}


def c9s2_case(r):
    who = name(r)
    d1, d2 = r.choice([(2, 1), (2.5, 1), (2, 0.5)])
    Q = r.choice([10, 12, 15, 20])
    A1 = math.pi * (d1 / 200) ** 2
    A2 = math.pi * (d2 / 200) ** 2
    v1 = Q / 1000 / 60 / A1
    v2 = Q / 1000 / 60 / A2
    return {'stem': (f'{who} waters a kitchen garden with a hose of internal diameter {g(d1)} cm fitted with a nozzle of diameter {g(d2)} cm. The tap delivers {Q} litres per minute.\n'
                     '(i) Find the speed of water in the hose. (ii) Find the speed at the nozzle. (iii) Which principle did you use? (iv) If the nozzle points straight up, how high could the water rise (ignore air resistance; g = 9.8 m s⁻²)?'),
            'answer': f'(i) {sig(v1)} m s⁻¹ (ii) {sig(v2)} m s⁻¹ (iii) equation of continuity (iv) {sig(v2 * v2 / (2 * G))} m',
            'key': f'(i) v = Q/A (1). (ii) A₁v₁ = A₂v₂ (1). (iii) continuity (1). (iv) v²/2g (1).'}


c9s2_derive = pool_txt([
    ('State and derive Bernoulli\'s principle for the steady flow of an ideal fluid.', 'P + ½ρv² + ρgh = constant along a streamline',
     'Work done by pressure forces (P₁ − P₂)ΔV (2); change in KE and PE of the fluid element (2); equate and rearrange (1).'),
    ('Derive the equation of continuity for the steady flow of an incompressible fluid.', 'A₁v₁ = A₂v₂', 'Mass in = mass out per unit time: ρA₁v₁Δt = ρA₂v₂Δt (3); ρ constant ⇒ Av constant (2).'),
    ('Using Bernoulli\'s principle, derive Torricelli\'s law for the speed of efflux from a hole at depth h in an open tank.', 'v = √(2gh)', 'Apply Bernoulli at surface and hole (2); P = P₀ at both, v_surface ≈ 0 (2); solve (1).'),
])


# st3 viscosity, Stokes' law, terminal velocity

c9s3_tf = tf_mcq('viscosity',
                 ['The viscosity of liquids decreases as temperature rises.', 'The viscosity of gases increases as temperature rises.', 'The SI unit of coefficient of viscosity is the poiseuille (Pa s).',
                  'A sphere falling through a viscous fluid reaches a terminal velocity.'],
                 ['The viscosity of liquids increases as temperature rises.', 'Terminal velocity is independent of the radius of the sphere.', 'The SI unit of viscosity is N m⁻¹.',
                  'Viscous force on a sphere is independent of its speed.'])

c9s3_explain = pool_txt([
    ('Why do raindrops fall with a constant speed near the ground?', 'Viscous drag (6πηrv) grows with speed until it balances weight minus buoyancy; then the drop moves at terminal velocity.', 'Forces balance (1 mark); terminal velocity (1 mark).'),
    ('Why does honey flow more easily when warmed?', 'The viscosity of liquids decreases with increasing temperature.', '2 marks.'),
    ('Why do bigger raindrops fall faster than smaller ones?', 'Terminal velocity ∝ r², so larger drops have higher terminal speed.', 'Formula (1 mark); conclusion (1 mark).'),
])

c9s3_ar = pool_ar([
    ('A larger raindrop falls with a higher terminal velocity.', 'Terminal velocity is proportional to the square of the radius.', 'a', 'R explains A.'),
    ('Warm honey flows faster than cold honey.', 'The viscosity of liquids decreases with temperature.', 'a', 'R explains A.'),
    ('An air bubble rising in water has zero viscous force on it.', 'Viscous force opposes relative motion.', 'd', 'A is false; R is true.'),
])


def c9s3_stokes(r):
    eta = r.choice([1.0e-3, 1.8e-5, 0.5, 1.5])
    rr = r.choice([0.1, 0.5, 1, 2, 5]) * 1e-3
    v = r.choice([0.01, 0.05, 0.1, 0.5, 1])
    F_ = 6 * math.pi * eta * rr * v
    return NUM(f'Find the viscous drag on a sphere of radius {g(rr * 1000)} mm moving at {g(v)} m s⁻¹ through a fluid of viscosity {g(eta)} Pa s.', F_, 'N',
               f'F = 6πηrv = 6π × {g(eta)} × {g(rr)} × {g(v)} = {{ans}}.', wrongs=[6 * math.pi * eta * rr * rr * v, math.pi * eta * rr * v, 6 * math.pi * eta * v / rr])


def c9s3_terminal(r):
    rr = r.choice([1, 2, 2.5, 3]) * 1e-3
    rho, sg = r.choice([(7800, 'steel'), (2700, 'aluminium'), (8900, 'copper')])
    liq, sigma, eta = r.choice([('glycerine', 1260, 1.5), ('castor oil', 960, 0.99), ('honey', 1400, 10)])
    v = 2 * rr * rr * (rho - sigma) * G / (9 * eta)
    return NUM(f'A {sg} ball (density {rho} kg m⁻³) of radius {g(rr * 1000)} mm falls through {liq} (density {sigma} kg m⁻³, viscosity {g(eta)} Pa s). Find its terminal velocity. (g = 9.8 m s⁻²)',
               v * 100, 'cm s⁻¹', f'v_t = 2r²(ρ − σ)g/(9η) = 2 × ({g(rr)})² × {rho - sigma} × 9.8/(9 × {g(eta)}) = {sig(v)} m s⁻¹ = {{ans}}.',
               wrongs=[2 * rr * rr * rho * G / (9 * eta) * 100, 2 * rr * (rho - sigma) * G / (9 * eta), v * 100 * 2])


def c9s3_ratio(r):
    k = r.choice([2, 3, 0.5])
    vt = r.choice([1, 2, 4, 5, 10])
    return NUM(f'A small sphere has a terminal velocity of {vt} cm s⁻¹ in a liquid. What is the terminal velocity of a sphere of the same material with {g(k)} times the radius in the same liquid?', vt * k * k, 'cm s⁻¹',
               f'v_t ∝ r² ⇒ v = {vt} × {g(k)}² = {{ans}}.', wrongs=[vt * k, vt * k ** 3, vt / k])


def c9s3_plate(r):
    A = r.choice([0.1, 0.2, 0.25, 0.5])
    v = r.choice([0.05, 0.1, 0.2, 0.5])
    d = r.choice([0.5, 1, 2]) * 1e-3
    eta = r.choice([0.1, 0.5, 0.9, 1.5])
    F_ = eta * A * v / d
    return NUM(f'A flat plate of area {g(A)} m² is pulled at {g(v)} m s⁻¹ over a layer of oil {g(d * 1000)} mm thick resting on a fixed plate. If the viscosity of the oil is {g(eta)} Pa s, what force is needed?', F_, 'N',
               f'F = ηA(v/d) = {g(eta)} × {g(A)} × {g(v)}/{g(d)} = {{ans}}.', wrongs=[eta * A * v * d, eta * v / d, eta * A * d / v])


def c9s3_eta(r):
    rr = r.choice([1, 1.5, 2]) * 1e-3
    vt = r.choice([1, 2, 3, 5]) * 1e-2
    rho, sigma = 7800, 1260
    eta = 2 * rr * rr * (rho - sigma) * G / (9 * vt)
    return {'stem': f'In a laboratory experiment, a steel ball (density 7800 kg m⁻³) of radius {g(rr * 1000)} mm falls through glycerine (density 1260 kg m⁻³) and reaches a terminal velocity of {g(vt * 100)} cm s⁻¹. Find the viscosity of glycerine and state one precaution in this experiment. (g = 9.8 m s⁻²)',
            'answer': f'{sig(eta)} Pa s', 'key': f'η = 2r²(ρ − σ)g/(9v_t) = {sig(eta)} Pa s (2); precaution: measure speed only after the ball has reached terminal velocity / the jar must be wide (1).'}


# st4 surface tension, angle of contact, capillary rise

c9s4_tf = tf_mcq('surface tension',
                 ['Surface tension has the unit N m⁻¹.', 'Surface tension decreases as temperature increases.', 'The angle of contact of mercury with glass is obtuse.',
                  'Liquid rises in a capillary tube when the angle of contact is acute.', 'Detergents reduce the surface tension of water.'],
                 ['Surface tension increases as temperature increases.', 'Mercury rises in a glass capillary tube.', 'The unit of surface tension is N m⁻².',
                  'Capillary rise is greater in a wider tube.', 'A soap bubble has only one surface.'])

c9s4_explain = pool_txt([
    ('Why do small liquid drops take a spherical shape?', 'Surface tension tends to minimise surface area, and a sphere has the least area for a given volume.', 'Minimise area (1 mark); sphere (1 mark).'),
    ('Why does water rise in a thin glass tube while mercury is depressed?', 'Water wets glass (acute contact angle), so adhesion pulls it up; mercury has an obtuse angle, so it is depressed.', 'Contact angle (1 mark); capillary rise/fall (1 mark).'),
    ('Why are detergents added to water for washing clothes?', 'They lower the surface tension, so water wets the fabric and penetrates the fine spaces, removing greasy dirt.', '2 marks.'),
    ('Why is the excess pressure inside a soap bubble 4S/r but inside a liquid drop only 2S/r?', 'A soap bubble has two surfaces (inner and outer), a drop only one.', '2 marks.'),
])

c9s4_ar = pool_ar([
    ('Small drops of mercury are nearly spherical.', 'Surface tension tends to minimise the surface area of a liquid.', 'a', 'R explains A.'),
    ('Water rises higher in a narrower capillary tube.', 'Capillary rise h = 2S cos θ/(ρgr).', 'a', 'h ∝ 1/r; R explains A.'),
    ('Mercury rises in a glass capillary.', 'The angle of contact of mercury with glass is obtuse.', 'd', 'A is false (mercury is depressed); R is true.'),
    ('The excess pressure in a soap bubble is twice that in a liquid drop of the same radius.', 'A soap bubble has two free surfaces.', 'a', 'R explains A.'),
])


def c9s4_pressure(r):
    S = r.choice([0.025, 0.03, 0.0727, 0.072, 0.465])
    rr = r.choice([0.5, 1, 2, 3, 5]) * 1e-3
    bub = S < 0.04
    dP = (4 if bub else 2) * S / rr
    what = 'a soap bubble' if bub else ('a mercury drop' if S > 0.1 else 'a water drop')
    return NUM(f'Find the excess pressure inside {what} of radius {g(rr * 1000)} mm. (Surface tension = {g(S)} N m⁻¹)', dP, 'Pa',
               f'ΔP = {"4S/r (two surfaces)" if bub else "2S/r"} = {4 if bub else 2} × {g(S)}/{g(rr)} = {{ans}}.', wrongs=[(2 if bub else 4) * S / rr, S / rr, (4 if bub else 2) * S * rr])


def c9s4_capillary(r):
    rr = r.choice([0.1, 0.2, 0.25, 0.5]) * 1e-3
    S = 0.073
    h = 2 * S / (1000 * G * rr)
    return NUM(f'How high does water rise in a clean glass capillary tube of radius {g(rr * 1000)} mm? (Surface tension of water = 0.073 N m⁻¹, angle of contact ≈ 0°, density 1000 kg m⁻³, g = 9.8 m s⁻²)', h * 100, 'cm',
               f'h = 2S cos θ/(ρgr) = 2 × 0.073/(1000 × 9.8 × {g(rr)}) = {sig(h)} m = {{ans}}.', wrongs=[S / (1000 * G * rr) * 100, 2 * S / (1000 * G * rr * rr) / 100, h * 1000])


def c9s4_bubble(r):
    rr = r.choice([1, 2, 3, 5]) * 1e-2
    S = r.choice([0.025, 0.03, 0.04])
    W = 8 * math.pi * rr * rr * S
    return NUM(f'How much work is done in blowing a soap bubble of radius {g(rr * 100)} cm? (Surface tension of soap solution = {g(S)} N m⁻¹)', W, 'J',
               f'Two surfaces: W = S × 2 × 4πr² = 8πr²S = {{ans}}.', wrongs=[4 * math.pi * rr * rr * S, 8 * math.pi * rr * S, 2 * math.pi * rr * rr * S])


def c9s4_drops(r):
    n = r.choice([8, 27, 64, 125, 1000])
    rr = r.choice([0.5, 1, 2]) * 1e-3
    S = 0.072
    R = rr * round(n ** (1 / 3))
    E = 4 * math.pi * S * (n * rr * rr - R * R)
    return {'stem': f'{n} identical water drops, each of radius {g(rr * 1000)} mm, coalesce to form a single big drop. Find the radius of the big drop and the energy released. (S = 0.072 N m⁻¹)',
            'answer': f'R = {g(R * 1000)} mm; energy {sig(E)} J', 'key': f'Volume conserved: R = n^(1/3) r = {round(n ** (1 / 3))} × {g(rr * 1000)} mm (1); energy = S × 4π(nr² − R²) = {sig(E)} J (2).', 'gap': 'G5'}


def c9s4_frame(r):
    L = r.choice([5, 8, 10, 12, 15]) * 1e-2
    S = r.choice([0.025, 0.03, 0.072])
    return NUM(f'A wire of length {g(L * 100)} cm slides on a U-shaped frame that holds a soap film. What force is needed to hold the wire in equilibrium? (Surface tension = {g(S)} N m⁻¹)', 2 * S * L, 'N',
               f'The film has two surfaces: F = 2SL = 2 × {g(S)} × {g(L)} = {{ans}}.', wrongs=[S * L, S / L, 4 * S * L])


# ======================================================== ch10 Thermal Properties of Matter
# st1 temperature, heat, thermal expansion

c10s1_terms = term_mcq([('coefficient of linear expansion α', 'ΔL/(L ΔT)'), ('coefficient of volume expansion γ', 'ΔV/(V ΔT)'), ('relation between γ and α for an isotropic solid', 'γ = 3α'),
                        ('anomalous expansion of water', 'water contracts when heated from 0 °C to 4 °C')],
                       'Which expression or statement describes the {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c10s1_tf = tf_mcq('thermal expansion',
                 ['Water has its maximum density at 4 °C.', 'For an isotropic solid, γ = 3α.', 'Gaps are left between railway rails to allow for expansion.', 'A temperature difference of 1 °C equals a difference of 1 K.'],
                 ['Water has its maximum density at 0 °C.', 'For an isotropic solid, γ = α/3.', 'A temperature difference of 1 °C equals a difference of 1.8 K.', 'All liquids expand on heating from 0 °C to 4 °C.'])

c10s1_explain = pool_txt([
    ('Why do ponds freeze from the top while fish survive in the water below?', 'Water is densest at 4 °C; colder water and ice stay on top; ice is a poor conductor, insulating the water below.', 'Anomalous expansion (1 mark); insulating ice layer (1 mark).'),
    ('Why are small gaps left between sections of a railway track?', 'Rails expand in summer; without gaps they would buckle.', '2 marks.'),
    ('A glass bottle with a tight metal lid is hard to open. Why does dipping it in hot water help?', 'Metal expands more than glass (larger α), so the lid loosens.', '2 marks.'),
    ('Why is mercury used in thermometers?', 'It expands uniformly over a wide range, is opaque and does not wet glass.', 'Any two properties, 1 mark each.'),
])

c10s1_ar = pool_ar([
    ('Ice floats on water.', 'Water expands on freezing.', 'a', 'Ice is less dense; R explains A.'),
    ('A temperature interval of 10 °C equals 18 °F.', 'A Fahrenheit degree is 5/9 of a Celsius degree.', 'a', 'Δt_F = (9/5)Δt_C; R explains A.'),
    ('The coefficient of volume expansion of an isotropic solid is three times its linear coefficient.', 'An isotropic solid expands equally in all directions.', 'a', 'R explains A.'),
    ('Water has its maximum density at 0 °C.', 'Water expands when it freezes.', 'd', 'A is false (4 °C); R is true.'),
])


def c10s1_scale(r):
    if r.random() < 0.5:
        c = r.choice([-40, -10, 25, 37, 40, 100, 120, 300])
        f = 9 * c / 5 + 32
        return {'stem': f'Convert {c} °C to the Fahrenheit and Kelvin scales.', 'answer': f'{g(f)} °F; {g(c + 273.15)} K',
                'key': f't_F = (9/5)t_C + 32 = {g(f)} °F; T = t_C + 273.15 = {g(c + 273.15)} K.', 'distractors': [f'{g(5 * c / 9 + 32)} °F; {g(c + 273.15)} K', f'{g(9 * c / 5)} °F; {g(c - 273.15)} K', f'{g(f)} °F; {g(c + 373.15)} K']}
    f = r.choice([-40, 32, 50, 77, 98.6, 104, 212, 451])
    c = (f - 32) * 5 / 9
    return {'stem': f'Convert {g(f)} °F to Celsius and Kelvin.', 'answer': f'{g(c, 2)} °C; {g(c + 273.15, 2)} K', 'key': f't_C = (5/9)(t_F − 32) = {g(c, 2)} °C; T = {g(c + 273.15, 2)} K.',
            'distractors': [f'{g((f - 32) * 9 / 5, 2)} °C; {g((f - 32) * 9 / 5 + 273.15, 2)} K', f'{g(f * 5 / 9, 2)} °C; {g(f * 5 / 9 + 273.15, 2)} K', f'{g(c, 2)} °C; {g(c - 273.15, 2)} K']}


def c10s1_linear(r):
    obj, mat, a = r.choice([('steel rail', 'steel', 1.2e-5), ('copper rod', 'copper', 1.7e-5), ('aluminium pipe', 'aluminium', 2.5e-5), ('brass strip', 'brass', 1.9e-5)])
    L = r.choice([1, 2, 5, 10, 12.5, 25])
    dT = r.choice([20, 25, 30, 40, 50])
    dL = a * L * dT
    return NUM(f'A {obj} is {g(L)} m long at 10 °C. By how much does its length increase when it is heated to {10 + dT} °C? (α_{mat} = {g(a)} K⁻¹)', dL * 1000, 'mm',
               f'ΔL = αLΔT = {g(a)} × {g(L)} × {dT} = {sig(dL)} m = {{ans}}.', wrongs=[a * L * (10 + dT) * 1000, 3 * a * L * dT * 1000, a * L * dT * 100])


def c10s1_stress(r):
    a = 1.2e-5
    Y = 2.0e11
    A = r.choice([10, 20, 40, 50]) * 1e-4
    dT = r.choice([10, 20, 30, 40])
    F_ = Y * A * a * dT
    return {'stem': f'A steel rail of cross-sectional area {g(A * 1e4)} cm² is fixed rigidly at both ends so that it cannot expand. If its temperature rises by {dT} °C, find the thermal stress and the force on the supports. (α = 1.2 × 10⁻⁵ K⁻¹, Y = 2.0 × 10¹¹ N m⁻²)',
            'answer': f'Stress {sig(Y * a * dT)} N m⁻²; force {sig(F_)} N', 'key': f'Prevented strain = αΔT = {sig(a * dT)} (1); stress = Y αΔT = {sig(Y * a * dT)} N m⁻² (1); F = stress × A = {sig(F_)} N (1).'}


def c10s1_flask(r):
    V = r.choice([500, 1000, 250, 750])
    gl = r.choice([(1.82e-4, 'mercury'), (1.0e-3, 'kerosene'), (4.9e-4, 'glycerine')])
    gg = 1.0e-5 * 3
    dT = r.choice([20, 30, 40, 50])
    over = (gl[0] - gg) * V * dT
    return NUM(f'A glass flask of volume {V} cm³ is filled to the brim with {gl[1]} at 20 °C. How much {gl[1]} overflows when the temperature is raised to {20 + dT} °C? (γ_liquid = {g(gl[0])} K⁻¹, γ_glass = 3 × 10⁻⁵ K⁻¹)',
               over, 'cm³', f'Overflow = (γ_l − γ_g)VΔT = ({g(gl[0])} − 3 × 10⁻⁵) × {V} × {dT} = {{ans}}.', wrongs=[gl[0] * V * dT, (gl[0] + gg) * V * dT, (gl[0] - gg / 3) * V * dT])


def c10s1_hole(r):
    d = r.choice([4.24, 3.50, 5.00, 2.80])
    t1, t2 = 27, r.choice([127, 227, 327])
    a = 1.7e-5
    dd = a * d * (t2 - t1)
    return {'stem': f'A hole of diameter {d:.2f} cm is drilled in a copper sheet at {t1} °C. What is its diameter when the sheet is heated to {t2} °C? Explain why the hole becomes larger, not smaller. (α_copper = 1.7 × 10⁻⁵ K⁻¹)',
            'answer': f'{d + dd:.4f} cm (increase {sig(dd)} cm)', 'key': f'The hole expands like the material that would fill it (1). Δd = αdΔT = 1.7 × 10⁻⁵ × {d:.2f} × {t2 - t1} = {sig(dd)} cm (1); new diameter {d + dd:.4f} cm (1).'}


def c10s1_k(r):
    c = r.choice([0, 27, 37, 100, -73, -173])
    return NUM(f'Express {c} °C in kelvin.', c + 273.15, 'K', f'T = t + 273.15 = {{ans}}.', wrongs=[c - 273.15, c + 273, 9 * c / 5 + 32], n=5)


# st2 specific heat capacity, calorimetry, latent heat

c10s2_terms = term_mcq([('specific heat capacity', 'heat needed to raise the temperature of unit mass by one degree'), ('latent heat of fusion', 'heat needed to melt unit mass of a solid at its melting point without change of temperature'),
                        ('latent heat of vaporisation', 'heat needed to convert unit mass of liquid into vapour at its boiling point'), ('heat capacity', 'heat needed to raise the temperature of the whole body by one degree')],
                       'Which statement defines {a}?', 'Which quantity is the {b}?', '{a}: {b}.')

c10s2_tf = tf_mcq('calorimetry and change of state',
                 ['During melting, the temperature of ice at 0 °C stays constant.', 'Water has a high specific heat capacity compared with most substances.', 'The boiling point of water increases with pressure.',
                  'In a calorimeter (no losses), heat lost by the hot body equals heat gained by the cold body.'],
                 ['During melting, the temperature of ice rises steadily.', 'The boiling point of water decreases with increase in pressure.', 'Latent heat is the heat that changes the temperature of a body.',
                  'Steam at 100 °C and water at 100 °C cause equally severe burns.'])

c10s2_explain = pool_txt([
    ('Why does a burn from steam at 100 °C hurt more than one from boiling water at 100 °C?', 'Steam gives up its large latent heat of vaporisation on condensing, besides the heat from cooling.', 'Latent heat (2 marks).'),
    ('Why is water used as a coolant in car radiators?', 'Its high specific heat capacity lets it absorb much heat with a small rise in temperature.', '2 marks.'),
    ('Why does food cook faster in a pressure cooker?', 'Higher pressure raises the boiling point of water, so cooking happens at a higher temperature.', '2 marks.'),
    ('Why do coastal cities like Mumbai and Chennai have milder climates than inland cities?', 'The sea\'s high specific heat capacity moderates temperature changes and drives sea and land breezes.', '2 marks.'),
])

c10s2_ar = pool_ar([
    ('Steam burns are more severe than burns from boiling water.', 'Steam releases latent heat when it condenses.', 'a', 'R explains A.'),
    ('Food cooks faster in a pressure cooker.', 'The boiling point of water rises with pressure.', 'a', 'R explains A.'),
    ('The temperature of water rises while it is boiling at constant pressure.', 'Heat supplied during boiling is used as latent heat.', 'd', 'A is false; R is true.'),
])


def c10s2_q(r):
    m = r.choice([0.2, 0.5, 1, 2, 5])
    sub, c = r.choice([('water', 4186), ('aluminium', 900), ('copper', 387), ('iron', 450)])
    dT = r.choice([10, 20, 30, 40, 50, 60])
    return NUM(f'How much heat is needed to raise the temperature of {g(m)} kg of {sub} by {dT} °C? (Specific heat capacity of {sub} = {c} J kg⁻¹ K⁻¹)', m * c * dT, 'J',
               f'Q = mcΔT = {g(m)} × {c} × {dT} = {{ans}}.', wrongs=[m * c, c * dT, m * c * (dT + 273)])


def c10s2_mix(r):
    m1, t1 = r.choice([0.1, 0.2, 0.3, 0.5]), r.choice([60, 70, 80, 90])
    m2, t2 = r.choice([0.2, 0.3, 0.4, 0.5]), r.choice([10, 15, 20, 25, 30])
    T = (m1 * t1 + m2 * t2) / (m1 + m2)
    return NUM(f'{g(m1 * 1000)} g of water at {t1} °C is mixed with {g(m2 * 1000)} g of water at {t2} °C. Find the final temperature (no heat loss).', T, '°C',
               f'Heat lost = heat gained: {g(m1)}c({t1} − T) = {g(m2)}c(T − {t2}) ⇒ T = {{ans}}.'.replace(' °C', ' °C'), wrongs=[(t1 + t2) / 2, (m2 * t1 + m1 * t2) / (m1 + m2), t1 - t2])


def c10s2_ice(r):
    mi = r.choice([0.02, 0.03, 0.05, 0.1])
    mw, tw = r.choice([0.2, 0.3, 0.5]), r.choice([40, 50, 60, 80])
    L, c = 3.34e5, 4186
    T = (mw * c * tw - mi * L) / ((mi + mw) * c)
    if T <= 0:
        raise ValueError
    return {'stem': f'{g(mi * 1000)} g of ice at 0 °C is added to {g(mw * 1000)} g of water at {tw} °C. Find the final temperature (no heat loss). (L_f = 3.34 × 10⁵ J kg⁻¹, c_water = 4186 J kg⁻¹ K⁻¹)',
            'answer': f'{sig(T)} °C', 'key': f'Heat to melt ice = {g(mi)} × 3.34 × 10⁵ = {g(mi * L)} J (1). Then {g(mi * L)} + {g(mi)}c(T − 0) = {g(mw)}c({tw} − T) (1) ⇒ T = {sig(T)} °C (1).',
            'distractors': [f'{sig((mw * tw) / (mi + mw))} °C', f'{sig((mw * c * tw + mi * L) / ((mi + mw) * c))} °C', f'{sig(tw / 2)} °C']}


def c10s2_metal(r):
    mm = r.choice([0.1, 0.15, 0.2, 0.25])
    tm = r.choice([100, 150, 200])
    mw = r.choice([0.15, 0.2, 0.25, 0.3])
    c_true = r.choice([387, 450, 900])
    tw = r.choice([20, 25, 27])
    T = (mm * c_true * tm + mw * 4186 * tw) / (mm * c_true + mw * 4186)
    T = round(T, 1)
    c = mw * 4186 * (T - tw) / (mm * (tm - T))
    who = name(r)
    return {'stem': f'{who} heats a {g(mm * 1000)} g metal block to {tm} °C and drops it into {g(mw * 1000)} g of water at {tw} °C in an insulated vessel (neglect its heat capacity). The final temperature is {g(T)} °C. Find the specific heat capacity of the metal. (c_water = 4186 J kg⁻¹ K⁻¹)',
            'answer': f'{sig(c)} J kg⁻¹ K⁻¹', 'key': f'Heat lost by metal = mc({tm} − {g(T)}); heat gained by water = {g(mw)} × 4186 × ({g(T)} − {tw}) = {sig(mw * 4186 * (T - tw))} J (2); c = {sig(c)} J kg⁻¹ K⁻¹ (1).'}


def c10s2_steam(r):
    m = r.choice([0.01, 0.02, 0.05, 0.1])
    ti = r.choice([-10, -20, -5])
    ci, cw, Lf, Lv = 2100, 4186, 3.34e5, 2.256e6
    q = m * (ci * (-ti) + Lf + cw * 100 + Lv)
    return {'stem': f'How much heat is needed to convert {g(m * 1000)} g of ice at {num(ti)} °C completely into steam at 100 °C? (c_ice = 2100 J kg⁻¹ K⁻¹, c_water = 4186 J kg⁻¹ K⁻¹, L_f = 3.34 × 10⁵ J kg⁻¹, L_v = 2.256 × 10⁶ J kg⁻¹)',
            'answer': f'{sig(q)} J', 'key': f'Q₁ = m c_ice × {-ti} = {g(m * ci * -ti)} J; Q₂ = mL_f = {g(m * Lf)} J; Q₃ = m c_w × 100 = {g(m * cw * 100)} J; Q₄ = mL_v = {g(m * Lv)} J (1 each + 1 for total) = {sig(q)} J.'}


def c10s2_case(r):
    who = name(r)
    P = r.choice([1000, 1200, 1500, 2000])
    m = r.choice([1, 1.5, 2])
    t0 = r.choice([20, 25, 30])
    t = m * 4186 * (100 - t0) / P
    return {'stem': (f'{who}\'s family uses a {P} W electric kettle to boil {g(m)} kg of water starting at {t0} °C. (c = 4186 J kg⁻¹ K⁻¹, L_v = 2.256 × 10⁶ J kg⁻¹; assume no losses)\n'
                     '(i) How much heat brings the water to 100 °C? (ii) How long does this take? (iii) How much longer to boil away 0.1 kg of it? (iv) Why does the temperature stay at 100 °C while it boils?'),
            'answer': f'(i) {sig(m * 4186 * (100 - t0))} J (ii) {sig(t)} s (iii) {sig(0.1 * 2.256e6 / P)} s (iv) heat goes into latent heat of vaporisation',
            'key': f'(i) mcΔT (1). (ii) Q/P (1). (iii) mL/P (1). (iv) latent heat, no temperature change (1).'}


# st3 heat transfer: conduction, convection, radiation

c10s3_terms = term_mcq([('conduction', 'transfer of heat between adjacent parts of a body without bulk motion of matter'), ('convection', 'transfer of heat by actual motion of the fluid'),
                        ('radiation', 'transfer of heat by electromagnetic waves, needing no medium'), ('Wien\'s displacement law', 'λ_m T = constant (about 2.9 × 10⁻³ m K)'),
                        ('Stefan-Boltzmann law', 'power radiated per unit area ∝ T⁴')],
                       'Which statement describes {a}?', 'Which term is described by: {b}?', '{a}: {b}.')

c10s3_tf = tf_mcq('heat transfer',
                 ['Sea breeze is caused by convection.', 'Heat from the Sun reaches the Earth by radiation.', 'A body that is a good absorber of radiation is also a good emitter.',
                  'The rate of conduction through a rod is proportional to the temperature difference across it.'],
                 ['Heat from the Sun reaches the Earth by convection.', 'Conduction requires bulk motion of matter.', 'A good absorber of radiation is a poor emitter.',
                  'The rate of conduction is independent of the cross-sectional area.'])

c10s3_explain = pool_txt([
    ('Why are cooking utensils made of metal but given wooden or plastic handles?', 'Metal conducts heat well to the food; wood or plastic are poor conductors and protect the hand.', '2 marks.'),
    ('Explain the formation of a sea breeze during the day.', 'Land heats faster; air over land rises and cooler air from the sea flows in to replace it (convection).', '2 marks.'),
    ('Why are white or light-coloured clothes preferred in summer?', 'They reflect most radiation and absorb little, so the body stays cooler.', '2 marks.'),
    ('Why does a blacksmith\'s hot iron change colour from red to yellow to white as it gets hotter?', 'By Wien\'s law, λ_m ∝ 1/T, so the peak of emitted radiation shifts to shorter wavelengths.', '2 marks.'),
])

c10s3_ar = pool_ar([
    ('A metal plate feels colder than a wooden plate at the same temperature.', 'Metals are better conductors of heat than wood.', 'a', 'R explains A.'),
    ('The Sun\'s heat reaches the Earth through empty space.', 'Radiation does not need a material medium.', 'a', 'R explains A.'),
    ('As a body gets hotter, the wavelength at which it emits most strongly increases.', 'λ_m T = constant.', 'd', 'A is false (λ_m decreases); R is true.'),
])


def c10s3_cond(r):
    K, mat = r.choice([(385, 'copper'), (205, 'aluminium'), (50, 'steel'), (0.8, 'glass')])
    A = r.choice([1, 2, 4, 5]) * 1e-4 if K > 1 else r.choice([1, 2])
    L = r.choice([0.1, 0.2, 0.25, 0.5]) if K > 1 else r.choice([0.004, 0.005, 0.006])
    dT = r.choice([20, 50, 80, 100])
    H = K * A * dT / L
    return NUM(f'A {mat} {"rod" if K > 1 else "window pane"} of {"cross-sectional " if K > 1 else ""}area {g(A)} m² and {"length" if K > 1 else "thickness"} {g(L)} m has a temperature difference of {dT} °C between its faces. Find the rate of heat flow. (K = {g(K)} W m⁻¹ K⁻¹)',
               H, 'W', f'H = KAΔT/L = {g(K)} × {g(A)} × {dT}/{g(L)} = {{ans}}.', wrongs=[K * A * dT * L, K * dT / L, K * A / L])


def c10s3_wien(r):
    lam, nm = r.choice([(0.5, 'the Sun'), (0.29, 'a hot star'), (9.7, 'the human body'), (0.36, 'Sirius'), (2.9, 'a red-hot iron rod')])
    T = 2.9e-3 / (lam * 1e-6)
    return NUM(f'The wavelength of maximum emission (λ_m) of {nm} is about {g(lam)} μm. Estimate its surface temperature using Wien\'s law. (b = 2.9 × 10⁻³ m K)', T, 'K',
               f'T = b/λ_m = 2.9 × 10⁻³/({g(lam)} × 10⁻⁶) = {{ans}}.', wrongs=[2.9e-3 * lam * 1e-6, 2.9e-3 / lam, T - 273])


def c10s3_stefan(r):
    t1 = r.choice([27, 127, 227, 327, 527])
    k = r.choice([2, 3, 1.5])
    T1 = t1 + 273
    T2 = T1 * k
    f = k ** 4
    return NUM(f'A blackbody at {t1} °C is heated until its absolute temperature becomes {g(k)} times. By what factor does the power it radiates increase?', f, '',
               f'P ∝ T⁴ (Stefan-Boltzmann) ⇒ factor = {g(k)}⁴ = {{ans}}. (Note: use kelvin, {T1} K → {g(T2)} K.)', wrongs=[k, k * k, k ** 3])


def c10s3_slab(r):
    K1, K2 = r.choice([(385, 50), (205, 50), (110, 385), (1, 0.5)])
    L1, L2 = r.choice([(0.1, 0.1), (0.2, 0.1), (0.05, 0.1)])
    T1, T2 = r.choice([(100, 0), (200, 20), (150, 30)])
    Tj = (K1 * T1 / L1 + K2 * T2 / L2) / (K1 / L1 + K2 / L2)
    return {'stem': f'Two slabs of the same area are placed in contact: slab 1 (K₁ = {g(K1)} W m⁻¹ K⁻¹, thickness {g(L1 * 100)} cm) and slab 2 (K₂ = {g(K2)} W m⁻¹ K⁻¹, thickness {g(L2 * 100)} cm). The outer face of slab 1 is at {T1} °C and that of slab 2 at {T2} °C. Find the temperature of the interface in steady state.',
            'answer': f'{sig(Tj)} °C', 'key': f'Same heat current: K₁A({T1} − T)/L₁ = K₂A(T − {T2})/L₂ (2) ⇒ T = (K₁T₁/L₁ + K₂T₂/L₂)/(K₁/L₁ + K₂/L₂) = {sig(Tj)} °C (2).', 'gap': 'G5'}


# st4 Newton's law of cooling

c10s4_tf = tf_mcq('Newton\'s law of cooling',
                 ['The rate of cooling is proportional to the excess temperature over the surroundings (for small differences).', 'A hot body cools faster at first and slower later.',
                  'The cooling curve (temperature vs time) is exponential in shape.', 'Newton\'s law of cooling is a good approximation only for small temperature differences.'],
                 ['A hot body cools at a constant rate until it reaches room temperature.', 'The rate of cooling is independent of the temperature of the surroundings.',
                  'The cooling curve is a straight line.', 'A body cools slower when its temperature is higher.'])

c10s4_explain = pool_txt([
    ('Why does a cup of hot tea cool quickly at first and then more slowly?', 'The rate of cooling is proportional to the temperature difference with the surroundings, which decreases with time.', '2 marks.'),
    ('State Newton\'s law of cooling and write it mathematically.', 'The rate of loss of heat is proportional to the excess temperature: −dQ/dt = k(T − T_s).', 'Statement (1 mark); equation (1 mark).'),
    ('Why is Newton\'s law of cooling only approximate for very hot bodies?', 'It is derived for small temperature differences; for large ones radiation (∝ T⁴) dominates.', '2 marks.'),
])

c10s4_ar = pool_ar([
    ('Hot food cools faster when it is very hot.', 'Rate of cooling is proportional to the excess of temperature over the surroundings.', 'a', 'R explains A.'),
    ('According to Newton\'s law of cooling, a body cools at a constant rate.', 'The rate of cooling depends on the temperature difference.', 'd', 'A is false; R is true.'),
    ('The cooling curve of a hot body in a room is a straight line.', 'The rate of cooling decreases as the body approaches room temperature.', 'd', 'A is false (the curve is exponential); R is true.'),
    ('A body at 80 °C cools faster in a room at 10 °C than in a room at 30 °C.', 'The rate of cooling is proportional to the excess temperature over the surroundings.', 'a', 'R explains A.'),
])


def c10s4_rate(r):
    Ts = r.choice([20, 25, 30])
    T1, T2 = r.choice([(80, 50), (90, 60), (70, 45), (100, 60), (85, 55)])
    R1 = r.choice([1.5, 2, 2.5, 3, 4])
    R2 = R1 * (T2 - Ts) / (T1 - Ts)
    return NUM(f'A body in a room at {Ts} °C cools at {g(R1)} °C per minute when its temperature is {T1} °C. Using Newton\'s law of cooling, what is its rate of cooling at {T2} °C?',
               R2, '°C min⁻¹', f'Rate ∝ (T − T_s): rate₂ = {g(R1)} × ({T2} − {Ts})/({T1} − {Ts}) = {{ans}}.', wrongs=[R1 * T2 / T1, R1 * (T1 - Ts) / (T2 - Ts), R1])


def c10s4_time(r):
    Ts = r.choice([20, 25, 30])
    a, b, c = r.choice([(80, 60, 40), (90, 70, 50), (70, 60, 50), (100, 80, 60)])
    t1 = r.choice([2, 3, 4, 5])
    k = (a - b) / t1 / ((a + b) / 2 - Ts)
    t2 = (b - c) / (k * ((b + c) / 2 - Ts))
    return {'stem': f'A pan of water cools from {a} °C to {b} °C in {t1} minutes in a room at {Ts} °C. Using the average form of Newton\'s law of cooling, how long will it take to cool from {b} °C to {c} °C?',
            'answer': f'{sig(t2)} min', 'key': f'({a} − {b})/{t1} = k({g((a + b) / 2)} − {Ts}) ⇒ k = {sig(k)} min⁻¹ (1.5); ({b} − {c})/t = k({g((b + c) / 2)} − {Ts}) ⇒ t = {sig(t2)} min (1.5).',
            'distractors': [f'{sig(x)} min' for x in dict.fromkeys([t1 * (b - c) / (a - b), t2 / 2, t2 * 2, t1 * 1.5]) if abs(x - t2) > 0.05]}


def c10s4_compare(r):
    Ts = r.choice([20, 25])
    e1, e2 = r.sample([10, 20, 30, 40, 50, 60], 2)
    return NUM(f'Two identical cups of tea are in a room at {Ts} °C, one at {Ts + e1} °C and the other at {Ts + e2} °C. What is the ratio of their initial rates of cooling (first : second)?', e1 / e2, '',
               f'Rate ∝ excess temperature: {e1} : {e2} = {{ans}}.', wrongs=[(Ts + e1) / (Ts + e2), e2 / e1, (e1 / e2) ** 2]) | {'answer': f'{e1 // math.gcd(e1, e2)} : {e2 // math.gcd(e1, e2)}',
                                                                                                             'distractors': [f'{e2 // math.gcd(e1, e2)} : {e1 // math.gcd(e1, e2)}', f'{Ts + e1} : {Ts + e2}', '1 : 1']}


def c10s4_multi(r):
    Ts = 20
    a, b = r.choice([(80, 64), (90, 70), (70, 58)])
    t = r.choice([5, 10])
    k = (a - b) / t / ((a + b) / 2 - Ts)
    c = r.choice([50, 52, 45])
    if c >= b:
        c = b - 10
    t2 = (b - c) / (k * ((b + c) / 2 - Ts))
    who = name(r)
    return {'stem': f'{who} records that milk in a steel tumbler cools from {a} °C to {b} °C in {t} min in a room at {Ts} °C. (i) Find the cooling constant k (average form). (ii) Find the time to cool further from {b} °C to {c} °C. (iii) Why is the second interval longer per degree?',
            'answer': f'(i) {sig(k)} min⁻¹ (ii) {sig(t2)} min (iii) smaller excess temperature gives a slower rate of cooling',
            'key': f'(i) ({a} − {b})/{t} = k({g((a + b) / 2)} − {Ts}) (1). (ii) ({b} − {c})/t = k({g((b + c) / 2)} − {Ts}) (1). (iii) rate ∝ (T − T_s) (1).'}


# ======================================================== families
FAMILIES = {
    S + '06-st1': [F('C1', 'D2', 'mcq', c6s1_tf), F('C2', 'D2', 'explain', c6s1_explain), F('C2', 'D3', 'mcq', c6s1_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c6s1_two),
                   F('C3', 'D3', 'numerical', c6s1_three), F('C3', 'D1', 'short', c6s1_heavier), F('C4', 'D3', 'multi_step', c6s1_boat), F('C4', 'D4', 'long', c6s1_explode)],
    S + '06-st2': [F('C1', 'D2', 'mcq', c6s2_tf), F('C1', 'D1', 'mcq', c6s2_terms), F('C2', 'D2', 'explain', c6s2_explain), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s2_torque), F('C3', 'D3', 'numerical', c6s2_cross), F('C4', 'D3', 'numerical', c6s2_wheel), F('C4', 'D4', 'multi_step', c6s2_angle)],
    S + '06-st3': [F('C1', 'D2', 'mcq', c6s3_tf), F('C2', 'D2', 'explain', c6s3_explain), F('C2', 'D3', 'mcq', c6s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c6s3_skater),
                   F('C3', 'D3', 'numerical', c6s3_balance), F('C4', 'D3', 'multi_step', c6s3_plank), F('C4', 'D4', 'long', c6s3_ladder), F('C3', 'D1', 'short', c6s3_L)],
    S + '06-st4': [F('C1', 'D2', 'mcq', c6s4_mi), F('C1', 'D1', 'mcq', c6s4_tf), F('C2', 'D2', 'explain', c6s4_explain), F('C2', 'D3', 'mcq', c6s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c6s4_alpha), F('C3', 'D3', 'numerical', c6s4_ke), F('C3', 'D4', 'multi_step', c6s4_cord), F('C4', 'D3', 'numerical', c6s4_gyration),
                   F('C4', 'D4', 'multi_step', c6s4_rpm), F('C4', 'D5', 'long', c6s4_combine), F('C2', 'D3', 'long', c6s4_derive), F('C3', 'D3', 'case', c6s4_case)],
    S + '07-st1': [F('C1', 'D2', 'mcq', c7s1_kepler), F('C1', 'D1', 'mcq', c7s1_tf), F('C2', 'D2', 'explain', c7s1_explain), F('C2', 'D3', 'mcq', c7s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s1_force), F('C3', 'D3', 'numerical', c7s1_kepler3), F('C4', 'D3', 'numerical', c7s1_null), F('C4', 'D4', 'multi_step', c7s1_aphelion),
                   F('C3', 'D1', 'short', c7s1_ratio)],
    S + '07-st2': [F('C1', 'D2', 'mcq', c7s2_tf), F('C2', 'D2', 'explain', c7s2_explain), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c7s2_height),
                   F('C3', 'D3', 'numerical', c7s2_depth), F('C3', 'D4', 'multi_step', c7s2_equal), F('C4', 'D3', 'numerical', c7s2_planet), F('C4', 'D4', 'multi_step', c7s2_fraction),
                   F('C3', 'D1', 'short', c7s2_gcalc)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_terms), F('C1', 'D1', 'mcq', c7s3_tf), F('C2', 'D2', 'explain', c7s3_explain), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s3_escape), F('C3', 'D3', 'numerical', c7s3_orbit), F('C3', 'D4', 'multi_step', c7s3_work), F('C4', 'D3', 'numerical', c7s3_ratio),
                   F('C4', 'D4', 'multi_step', c7s3_maxh), F('C4', 'D5', 'long', c7s3_infinity), F('C2', 'D3', 'long', c7s3_derive)],
    S + '07-st4': [F('C1', 'D2', 'mcq', c7s4_tf), F('C1', 'D1', 'mcq', c7s4_geo), F('C2', 'D2', 'explain', c7s4_explain), F('C2', 'D3', 'mcq', c7s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'multi_step', c7s4_energy), F('C3', 'D3', 'numerical', c7s4_raise), F('C4', 'D3', 'case', c7s4_case)],
    S + '08-st1': [F('C1', 'D2', 'mcq', c8s1_terms), F('C1', 'D1', 'mcq', c8s1_tf), F('C2', 'D2', 'explain', c8s1_explain), F('C2', 'D3', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s1_stress), F('C3', 'D3', 'numerical', c8s1_load), F('C3', 'D1', 'short', c8s1_simple), F('C4', 'D3', 'case', c8s1_graph)],
    S + '08-st2': [F('C1', 'D2', 'mcq', c8s2_terms), F('C1', 'D1', 'mcq', c8s2_tf), F('C2', 'D2', 'explain', c8s2_explain), F('C2', 'D3', 'mcq', c8s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s2_extension), F('C3', 'D3', 'numerical', c8s2_young), F('C3', 'D4', 'multi_step', c8s2_series), F('C4', 'D3', 'numerical', c8s2_bulk),
                   F('C4', 'D4', 'numerical', c8s2_shear), F('C4', 'D5', 'long', c8s2_rod), F('C3', 'D3', 'case', c8s2_case)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_tf), F('C1', 'D1', 'mcq', c8s3_mcq), F('C2', 'D2', 'explain', c8s3_explain), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s3_rope), F('C3', 'D3', 'numerical', c8s3_sag), F('C4', 'D3', 'multi_step', c8s3_mountain)],
    S + '09-st1': [F('C1', 'D2', 'mcq', c9s1_tf), F('C2', 'D2', 'explain', c9s1_explain), F('C2', 'D3', 'mcq', c9s1_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c9s1_depth),
                   F('C3', 'D3', 'numerical', c9s1_lift), F('C4', 'D3', 'numerical', c9s1_utube), F('C3', 'D1', 'short', c9s1_heel), F('C4', 'D4', 'multi_step', c9s1_barometer)],
    S + '09-st2': [F('C1', 'D2', 'mcq', c9s2_tf), F('C2', 'D2', 'explain', c9s2_explain), F('C2', 'D3', 'mcq', c9s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c9s2_cont),
                   F('C3', 'D3', 'numerical', c9s2_efflux), F('C3', 'D4', 'multi_step', c9s2_venturi), F('C4', 'D3', 'multi_step', c9s2_wing), F('C4', 'D4', 'multi_step', c9s2_pipe),
                   F('C4', 'D5', 'long', c9s2_tank), F('C3', 'D3', 'case', c9s2_case), F('C2', 'D3', 'long', c9s2_derive), F('C1', 'D1', 'mcq', c9s2_terms)],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_tf), F('C2', 'D2', 'explain', c9s3_explain), F('C2', 'D3', 'mcq', c9s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c9s3_stokes),
                   F('C3', 'D3', 'numerical', c9s3_plate), F('C4', 'D3', 'numerical', c9s3_terminal), F('C3', 'D1', 'short', c9s3_ratio), F('C4', 'D4', 'multi_step', c9s3_eta)],
    S + '09-st4': [F('C1', 'D2', 'mcq', c9s4_tf), F('C2', 'D2', 'explain', c9s4_explain), F('C2', 'D3', 'mcq', c9s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c9s4_pressure),
                   F('C3', 'D3', 'numerical', c9s4_capillary), F('C4', 'D3', 'numerical', c9s4_bubble), F('C4', 'D4', 'multi_step', c9s4_drops), F('C3', 'D1', 'short', c9s4_frame)],
    S + '10-st1': [F('C1', 'D2', 'mcq', c10s1_terms), F('C1', 'D1', 'mcq', c10s1_tf), F('C2', 'D2', 'explain', c10s1_explain), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s1_scale), F('C3', 'D3', 'numerical', c10s1_linear), F('C3', 'D4', 'multi_step', c10s1_stress), F('C4', 'D3', 'numerical', c10s1_flask),
                   F('C4', 'D4', 'multi_step', c10s1_hole), F('C3', 'D1', 'short', c10s1_k)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_terms), F('C1', 'D1', 'mcq', c10s2_tf), F('C2', 'D2', 'explain', c10s2_explain), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s2_q), F('C3', 'D3', 'numerical', c10s2_mix), F('C3', 'D4', 'multi_step', c10s2_ice), F('C4', 'D3', 'multi_step', c10s2_metal),
                   F('C4', 'D4', 'multi_step', c10s2_steam), F('C3', 'D3', 'case', c10s2_case)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_terms), F('C1', 'D1', 'mcq', c10s3_tf), F('C2', 'D2', 'explain', c10s3_explain), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s3_cond), F('C3', 'D3', 'numerical', c10s3_wien), F('C4', 'D3', 'numerical', c10s3_stefan), F('C4', 'D4', 'long', c10s3_slab)],
    S + '10-st4': [F('C1', 'D2', 'mcq', c10s4_tf), F('C2', 'D2', 'explain', c10s4_explain), F('C2', 'D3', 'mcq', c10s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c10s4_rate),
                   F('C3', 'D3', 'numerical', c10s4_time), F('C4', 'D3', 'multi_step', c10s4_multi), F('C3', 'D1', 'short', c10s4_compare)],
}
FAMILIES = polish(FAMILIES)
