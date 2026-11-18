"""CBSE class 12 physics (NCERT Physics XII) families, chapters 1-5."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, name, two_names, CITIES  # noqa: F401
from g11_physics_util import polish, sig, g, NUM, NUM2, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401

S = 'cbse-g12-physics-ch'
K = 9e9
E0 = 8.854e-12
QE = 1.6e-19
ME = 9.1e-31
MP = 1.67e-27
MU0 = 4 * math.pi * 1e-7
G = 9.8


def uc(q):
    """Charge in coulomb -> short text in μC / nC."""
    if abs(q) >= 1e-6:
        return f'{g(q * 1e6)} μC'
    return f'{g(q * 1e9)} nC'


# ======================================================== ch01 Electric Charges and Fields
# st1 electric charge, conductors, insulators, induction, properties

c1s1_terms = term_mcq([('conductor', 'a substance that allows electric charge to move easily through it, e.g. metals'),
                       ('insulator', 'a substance that offers high resistance to the passage of charge, e.g. glass, plastic'),
                       ('charging by induction', 'charging a body without touching it, by bringing a charged body near and earthing'),
                       ('quantisation of charge', 'the charge on a body is always an integral multiple of e'),
                       ('conservation of charge', 'the total charge of an isolated system remains constant'),
                       ('additivity of charge', 'the total charge of a system is the algebraic sum of the individual charges')],
                      'Which statement describes {a}?', 'Which term is described by: {b}?', '{a}: {b}.')

c1s1_tf = tf_mcq('electric charge',
                 ['Charge is a scalar quantity.', 'Charge is quantised: q = ne.', 'The total charge of an isolated system is conserved.',
                  'When a glass rod is rubbed with silk, electrons move from glass to silk.', 'Like charges repel and unlike charges attract.'],
                 ['Charge can be created by rubbing two bodies.', 'A body can have a charge of 0.5e.', 'When a glass rod is rubbed with silk, protons move from silk to glass.',
                  'Charge is a vector quantity.', 'A charged body attracts only oppositely charged bodies.'])

c1s1_explain = pool_txt([
    ('Why does a charged comb attract small bits of paper?', 'The comb induces opposite charge on the near side of the paper; attraction on the near side exceeds repulsion on the far side.', 'Induction/polarisation (1); net attraction (1).'),
    ('Explain how a metal sphere can be given a positive charge by induction using a negatively charged rod.', 'Bring the rod near: electrons are pushed to the far side; earth the far side so electrons flow away; remove the earthing, then the rod; the sphere is left positive.', '2 marks.'),
    ('Why can quantisation of charge be ignored when dealing with macroscopic charges?', 'e = 1.6 × 10⁻¹⁹ C is so small that a charge of even 1 μC contains ~10¹³ electrons, so charge behaves as continuous.', '2 marks.'),
    ('Why do clothes sometimes crackle when taken out of a dryer or when a woollen sweater is removed?', 'Rubbing transfers electrons and charges the fabric; discharge sparks produce the crackle.', '2 marks.'),
])

c1s1_ar = pool_ar([
    ('A charge of 2.4 × 10⁻¹⁹ C cannot exist on a body.', 'Charge on a body is always an integral multiple of 1.6 × 10⁻¹⁹ C.', 'a', 'R explains A (2.4/1.6 = 1.5).'),
    ('When a glass rod is rubbed with silk, both acquire charges.', 'Charge is created by friction.', 'c', 'A is true; R is false: charge is transferred, not created.'),
    ('A positively charged body has lost electrons.', 'Protons are easily transferred by rubbing.', 'c', 'A is true; R is false: only electrons are transferred.'),
    ('The total charge of an isolated system remains constant.', 'Charges are always created or destroyed in equal and opposite pairs.', 'a', 'R explains A.'),
])


def c1s1_n(r):
    q = r.choice([1, 2, 3.2, 4.8, 8, 16]) * r.choice([1e-9, 1e-6, 1e-12])
    n = q / QE
    return NUM(f'How many electrons must be removed from a neutral body to give it a charge of +{g(q)} C? (e = 1.6 × 10⁻¹⁹ C)', n, '',
               f'n = q/e = {g(q)}/(1.6 × 10⁻¹⁹) = {{ans}}.', wrongs=[q * QE, n * 10, n / 10], gap='G3')


def c1s1_rub(r):
    q = r.choice([2, 3, 4, 5, 6, 8]) * 1e-7
    n = q / QE
    m = n * ME
    return NUM2(f'A polythene piece rubbed with wool is found to have a negative charge of {g(q)} C. (i) Estimate the number of electrons transferred. (ii) Find the mass transferred to the polythene. (mₑ = 9.1 × 10⁻³¹ kg)',
                (n, m), ('', 'kg'), f'(i) n = q/e = {g(q)}/(1.6 × 10⁻¹⁹) = {sig(n)} (1). (ii) m = n mₑ = {sig(m)} kg, from wool to polythene (1).',
                wrongs=[(n, n * MP), (n / 10, m / 10), (q * QE, m)])


def c1s1_which(r):
    n = r.randint(2, 9)
    bad = (n + 0.5) * 1.6
    goods = r.sample([k * 1.6 for k in range(1, 12) if k != n], 3)
    return mcq('Which of the following CANNOT be the charge on a body? (e = 1.6 × 10⁻¹⁹ C)', f'{num(bad, 2)} × 10⁻¹⁹ C', [f'{num(x, 2)} × 10⁻¹⁹ C' for x in goods],
               f'{num(bad, 2)}/1.6 = {num(n + 0.5, 1)}, not an integer; charge must be ne.', r)


def c1s1_water(r):
    m = r.choice([9, 18, 27, 36, 45, 90, 250])
    nmol = m / 18
    q = nmol * 6.02e23 * 10 * QE
    return NUM(f'Estimate the total positive charge carried by the protons in {m} g of water. (Each H₂O molecule has 10 protons; N_A = 6.02 × 10²³ mol⁻¹; molar mass 18 g mol⁻¹)', q, 'C',
               f'moles = {m}/18 = {sig(nmol)} (1); molecules = {sig(nmol * 6.02e23)} (1); protons ×10; q = N × 10 × e = {{ans}} (1).',
               wrongs=[q / 10, nmol * 6.02e23 * QE * 8, q * 2], gap='G5')


c1s1_mcq = pool_mcq([
    ('A glass rod rubbed with silk becomes positively charged because', 'electrons move from the glass to the silk', ['protons move from the silk to the glass', 'electrons move from the silk to the glass', 'protons are created on the glass'], 'Only electrons are transferred.'),
    ('The SI unit of electric charge is', 'coulomb', ['ampere', 'volt', 'farad'], '1 C = 1 A s.'),
    ('A gold-leaf electroscope is used to', 'detect charge on a body', ['measure current', 'store charge permanently', 'measure resistance'], 'The leaves diverge when charged.'),
    ('When a negatively charged rod is brought near the cap of an uncharged electroscope, the leaves', 'diverge, as they acquire negative charge by induction', ['stay closed', 'diverge, as they acquire positive charge', 'collapse permanently'], 'Electrons are repelled to the leaves.'),
])


# st2 Coulomb's law, superposition

c1s2_tf = tf_mcq("Coulomb's law",
                 ['The force between two point charges is inversely proportional to the square of the distance between them.', 'The force acts along the line joining the charges.',
                  'In a medium of dielectric constant K the force becomes 1/K times that in vacuum.', 'The forces two charges exert on each other are equal and opposite.'],
                 ['The force between two charges is inversely proportional to the distance between them.', 'The force between two charges is independent of the medium.',
                  'The force on a charge due to another charge changes when a third charge is brought nearby.', 'Coulomb force is always attractive.'])

c1s2_explain = pool_txt([
    ('State the principle of superposition for electrostatic forces.', 'The net force on a charge is the vector sum of the forces due to each of the other charges, each taken as if the others were absent.', '2 marks.'),
    ('Two identical metal spheres carry charges q and −3q. They are touched and separated to the same distance. How does the force between them change?', 'Each gets −q; force changes from attractive 3kq²/r² to repulsive kq²/r², i.e. 1/3 in magnitude.', '2 marks.'),
    ('Define 1 coulomb using Coulomb\'s law.', '1 C is the charge which, placed 1 m from an equal charge in vacuum, repels it with a force of 9 × 10⁹ N.', '2 marks.'),
    ('Compare electrostatic and gravitational forces between two protons.', 'Both obey inverse square laws; electric force is about 10³⁶ times stronger and can be attractive or repulsive; gravity only attracts.', '2 marks.'),
])

c1s2_ar = pool_ar([
    ('The force between two charges decreases when a dielectric medium is placed between them.', 'F = q₁q₂/(4πε₀Kr²), with K > 1.', 'a', 'R explains A.'),
    ('The force between two charges is unaffected by the presence of other charges.', 'Coulomb forces obey the principle of superposition.', 'a', 'Each pair interaction is independent; R explains A.'),
    ('Coulomb\'s law holds for point charges.', 'Coulomb force between charges is always attractive.', 'c', 'A is true; R is false.'),
    ('The electric force between two protons is much larger than the gravitational force between them.', 'The gravitational constant is much smaller than 1/(4πε₀).', 'a', 'Fₑ/F_g ≈ 10³⁶; R explains A.'),
])


def c1s2_force(r):
    q1 = r.choice([1, 2, 3, 4, 5]) * 1e-6
    q2 = r.choice([1, 2, 3, 6, 8]) * 1e-6 * r.choice([1, -1])
    d = r.choice([10, 20, 30, 40, 50])
    Fv = K * q1 * abs(q2) / (d / 100) ** 2
    kind = 'attractive' if q2 < 0 else 'repulsive'
    return NUM(f'Two point charges {uc(q1)} and {uc(q2).replace("-", "−")} are placed {d} cm apart in air. Find the magnitude of the force between them and state whether it is attractive or repulsive. (1/4πε₀ = 9 × 10⁹ N m² C⁻²)',
               Fv, 'N', f'F = kq₁q₂/r² = 9 × 10⁹ × {g(q1)} × {g(abs(q2))}/({g(d / 100)})² = {{ans}}, {kind}.', wrongs=[K * q1 * abs(q2) / (d / 100), Fv * 100, Fv / 2])


def c1s2_factor(r):
    a = r.choice([2, 3, 0.5])
    b = r.choice([2, 3, 4, 0.5])
    f = a * a / (b * b)
    ta = f'each charge is made {g(a)} times' if a != 0.5 else 'each charge is halved'
    tb = f'the distance is made {g(b)} times' if b != 0.5 else 'the distance is halved'
    return NUM(f'Two point charges repel each other with a force F. By what factor does the force change if {ta} and {tb}?', f, '',
               f'F ∝ q₁q₂/r² ⇒ factor = {g(a)}² / {g(b)}² = {{ans}}.', wrongs=[a / b, a * a / b, a / (b * b)], gap='G3')


def c1s2_medium(r):
    Kd = r.choice([2, 4, 5, 80, 6])
    Fv = r.choice([0.4, 0.9, 1.2, 1.6, 3.6])
    return NUM(f'Two charges in air exert a force of {g(Fv)} N on each other. What is the force when they are immersed, at the same separation, in a medium of dielectric constant {Kd}?', Fv / Kd, 'N',
               f'F_m = F/K = {g(Fv)}/{Kd} = {{ans}}.', wrongs=[Fv * Kd, Fv / Kd ** 2, Fv])


def c1s2_line(r):
    q = r.choice([1, 2, 3, 4]) * 1e-6
    qa = r.choice([2, 3, 4, 5]) * 1e-6
    qb = r.choice([1, 2, 6, 8]) * 1e-6
    a = r.choice([10, 20, 30])
    b = r.choice([10, 20, 40])
    fa = K * qa * q / (a / 100) ** 2
    fb = K * qb * q / (b / 100) ** 2
    net = fa - fb
    dirn = 'towards B' if net > 0 else 'towards A'
    if abs(net) < 1e-9:
        raise ValueError
    return NUM(f'Charges q_A = +{uc(qa)} and q_B = +{uc(qb)} are placed at points A and B. A charge +{uc(q)} is placed at C on the line AB, between them, with AC = {a} cm and CB = {b} cm. Find the net force on the charge at C. (k = 9 × 10⁹ N m² C⁻²)',
               abs(net), 'N', f'F_A = kq_Aq/AC² = {sig(fa)} N towards B (1); F_B = kq_Bq/CB² = {sig(fb)} N towards A (1); net = {{ans}} {dirn} (1).',
               wrongs=[fa + fb, fa, fb], gap='G5')


def c1s2_triangle(r):
    q = r.choice([1, 2, 3, 5]) * 1e-6
    a = r.choice([10, 20, 30, 50])
    f1 = K * q * q / (a / 100) ** 2
    Fn = math.sqrt(3) * f1
    return NUM(f'Three equal charges of +{uc(q)} each are placed at the corners of an equilateral triangle of side {a} cm. Find the magnitude of the net force on any one charge. (k = 9 × 10⁹ N m² C⁻²)', Fn, 'N',
               f'Each pair force F = kq²/a² = {sig(f1)} N (1); the two forces on a charge are at 60°: F_net = √(F² + F² + 2F² cos 60°) = √3 F (1) = {{ans}} (1), along the bisector, away from the triangle.',
               wrongs=[2 * f1, f1, f1 * math.sqrt(2)], gap='G5')


def c1s2_null(r):
    q1 = r.choice([1, 4, 9, 16])
    q2 = r.choice([1, 4, 9, 16, 25])
    if q1 == q2:
        q2 = 4 * q1
    d = r.choice([30, 40, 60, 90, 100])
    x = d / (1 + math.sqrt(q2 / q1))
    return NUM(f'Two point charges +{q1} μC and +{q2} μC are {d} cm apart. Where, on the line joining them, should a third charge be placed so that the net force on it is zero? Give its distance from the +{q1} μC charge.',
               x, 'cm', f'kq₁Q/x² = kq₂Q/(d − x)² ⇒ (d − x)/x = √(q₂/q₁) = {g(math.sqrt(q2 / q1))} (2) ⇒ x = d/(1 + √(q₂/q₁)) = {{ans}} (1). The result is independent of the third charge.',
               wrongs=[d * q1 / (q1 + q2), d - x, d / 2], gap='G5')


def c1s2_ratio(r):
    pair, val = r.choice([('two protons', K * QE ** 2 / (6.67e-11 * MP * MP)), ('an electron and a proton', K * QE ** 2 / (6.67e-11 * ME * MP)), ('two electrons', K * QE ** 2 / (6.67e-11 * ME * ME))])
    return NUM(f'Find the ratio of the electrostatic force to the gravitational force between {pair} at any separation. (k = 9 × 10⁹ N m² C⁻², G = 6.67 × 10⁻¹¹ N m² kg⁻², mₑ = 9.1 × 10⁻³¹ kg, m_p = 1.67 × 10⁻²⁷ kg)',
               val, '', 'Fₑ/F_g = ke²/(Gm₁m₂); the r² cancels (1); substitution (1) = {ans}.', wrongs=[val / 1000, val * 1000, math.sqrt(val)], gap='G3')


# st3 electric field, field lines, dipole

c1s3_lines = tf_mcq('electric field lines',
                    ['Field lines start on positive charges and end on negative charges.', 'Two field lines never intersect.', 'Electrostatic field lines do not form closed loops.',
                     'Field lines are crowded where the field is strong.', 'The tangent to a field line gives the direction of the field at that point.'],
                    ['Field lines can cross each other at a point.', 'Electrostatic field lines form closed loops.', 'Field lines are farther apart where the field is stronger.',
                     'A field line shows the actual path of any charged particle.', 'Field lines start on negative charges.'])

c1s3_terms = term_mcq([('electric field', 'force per unit positive test charge, E = F/q₀'), ('electric dipole moment', 'p = q × 2a, directed from −q to +q'),
                       ('torque on a dipole', 'τ = p × E'), ('uniform electric field', 'a field of the same magnitude and direction at every point'),
                       ('field of a point charge', 'E = q/(4πε₀r²), radially outward for q > 0')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c1s3_explain = pool_txt([
    ('Why must the test charge used to measure an electric field be very small?', 'A large test charge would disturb the source charges and change the very field being measured.', '2 marks.'),
    ('A dipole is placed in a uniform electric field. Explain why it experiences a torque but no net force.', 'Forces qE and −qE are equal and opposite, so net force is zero; they act at different points, so they form a couple of torque pE sin θ.', '2 marks.'),
    ('Why do two electric field lines never cross?', 'At the crossing point the field would have two directions, which is impossible.', '2 marks.'),
    ('What is the direction of the field on the equatorial line of a dipole, compared with the dipole moment?', 'Opposite to p (from +q towards −q, parallel to the axis).', '2 marks.'),
])

c1s3_ar = pool_ar([
    ('A dipole in a non-uniform field experiences a net force.', 'The forces on its two charges are then not equal.', 'a', 'R explains A.'),
    ('The field due to a dipole falls off as 1/r³ at large distances.', 'The fields of +q and −q nearly cancel at large distances.', 'a', 'R explains A.'),
    ('A dipole in a uniform field is in stable equilibrium when p is anti-parallel to E.', 'The torque on a dipole is zero when p is parallel or anti-parallel to E.', 'd', 'A is false: stable equilibrium is p parallel to E; R is true.'),
    ('Electric field lines are always perpendicular to the surface of a conductor.', 'There is no tangential field at the surface of a conductor in electrostatics.', 'a', 'R explains A.'),
])


def c1s3_E(r):
    q = r.choice([2, 4, 5, 8, 10]) * r.choice([1e-9, 1e-6])
    d = r.choice([5, 10, 20, 30, 50])
    Ev = K * q / (d / 100) ** 2
    return NUM(f'Find the magnitude of the electric field at a distance of {d} cm from a point charge of {uc(q)} in air. (k = 9 × 10⁹ N m² C⁻²)', Ev, 'N C⁻¹',
               f'E = kq/r² = 9 × 10⁹ × {g(q)}/({g(d / 100)})² = {{ans}}.', wrongs=[K * q / (d / 100), Ev * 1e4, Ev / 2], gap='G3')


def c1s3_acc(r):
    Ev = r.choice([1, 2, 5, 8]) * 10 ** r.choice([3, 4])
    p, m, qn = r.choice([('an electron', ME, 'e'), ('a proton', MP, 'e')])
    a = QE * Ev / m
    return NUM(f'Find the acceleration of {p} placed in a uniform electric field of {g(Ev)} N C⁻¹. (e = 1.6 × 10⁻¹⁹ C, mₑ = 9.1 × 10⁻³¹ kg, m_p = 1.67 × 10⁻²⁷ kg)', a, 'm s⁻²',
               f'F = eE; a = eE/m = 1.6 × 10⁻¹⁹ × {g(Ev)}/{g(m)} = {{ans}}.', wrongs=[QE * Ev, QE * Ev / (MP if m == ME else ME), a / 1000])


def c1s3_axial(r):
    q = r.choice([1, 2, 5]) * 1e-9
    a2 = r.choice([2, 4])
    d = r.choice([10, 15, 20, 30])
    p = q * a2 / 1000
    where = r.choice(['axial', 'equatorial'])
    Ev = (2 if where == 'axial' else 1) * K * p / (d / 100) ** 3
    return NUM(f'An electric dipole consists of charges ±{uc(q)} separated by {a2} mm. Find the electric field at a point on its {where} line {d} cm from its centre.', Ev, 'N C⁻¹',
               f'p = q × 2a = {g(p)} C m (1); for r ≫ 2a, E = {"2kp/r³" if where == "axial" else "kp/r³"} = {{ans}} (1){"" if where == "axial" else ", directed opposite to p"}.',
               wrongs=[(1 if where == 'axial' else 2) * K * p / (d / 100) ** 3, (2 if where == 'axial' else 1) * K * p / (d / 100) ** 2, Ev * 10], gap='G3')


def c1s3_torque(r):
    p = r.choice([2, 4, 5, 8]) * 1e-9
    Ev = r.choice([1, 2, 5]) * 1e4
    th = r.choice([30, 45, 60, 90])
    t = p * Ev * math.sin(math.radians(th))
    return NUM(f'An electric dipole of moment {g(p)} C m is placed in a uniform field of {g(Ev)} N C⁻¹ at {th}° to the field. Find the torque on it.', t, 'N m',
               f'τ = pE sin θ = {g(p)} × {g(Ev)} × sin {th}° = {{ans}}.', wrongs=[p * Ev * math.cos(math.radians(th)), p * Ev, p / Ev])


def c1s3_work(r):
    p = r.choice([2, 4, 5]) * 1e-9
    Ev = r.choice([1, 2, 5]) * 1e4
    t1, t2 = r.choice([(0, 90), (0, 180), (60, 180), (0, 60), (90, 180)])
    W = p * Ev * (math.cos(math.radians(t1)) - math.cos(math.radians(t2)))
    return NUM(f'A dipole of moment {g(p)} C m lies in a uniform field of {g(Ev)} N C⁻¹. Find the work done by an external agent in rotating it from θ = {t1}° to θ = {t2}° (θ measured from the field).', W, 'J',
               f'W = pE(cos θ₁ − cos θ₂) (2) = {g(p)} × {g(Ev)} × ({num(math.cos(math.radians(t1)), 2)} − ({num(math.cos(math.radians(t2)), 2)})) = {{ans}} (1). The potential energy rises by the same amount.',
               wrongs=[p * Ev * abs(math.sin(math.radians(t2)) - math.sin(math.radians(t1))) or W * 3, p * Ev, W / 2], gap='G5')


def c1s3_null(r):
    q1 = r.choice([1, 4, 9])
    q2 = r.choice([4, 16, 25, 36])
    d = r.choice([20, 30, 60, 90])
    x = d / (1 + math.sqrt(q2 / q1))
    return NUM(f'Charges +{q1} nC and +{q2} nC are placed {d} cm apart. Find the point between them where the electric field is zero; give its distance from the +{q1} nC charge.', x, 'cm',
               f'kq₁/x² = kq₂/(d − x)² ⇒ x = d/(1 + √(q₂/q₁)) (2) = {{ans}} (1).', wrongs=[d * q1 / (q1 + q2), d - x, d / 2], gap='G5')


def c1s3_stop(r):
    v = r.choice([1, 2, 3, 4]) * 1e6
    Ev = r.choice([1, 2, 5]) * 1e3
    s = ME * v * v / (2 * QE * Ev)
    return NUM(f'An electron moving at {g(v)} m s⁻¹ enters a uniform electric field of {g(Ev)} N C⁻¹ directed along its velocity. How far does it travel before coming momentarily to rest?', s, 'm',
               f'Force on electron opposes its motion: a = eE/m = {sig(QE * Ev / ME)} m s⁻² (1); s = v²/(2a) (1) = {{ans}} (1).', wrongs=[2 * s, ME * v / (QE * Ev), s * 1000], gap='G5')


c1s3_derive = pool_txt([
    ('Derive an expression for the electric field at a point on the axial line of an electric dipole. Show that it varies as 1/r³ for r ≫ a.', 'E = 2kpr/(r² − a²)² ≈ 2kp/r³, along p',
     'Fields of +q and −q (2); subtract (1); simplify (1); limit r ≫ a (1).'),
    ('Derive an expression for the electric field at a point on the equatorial line of a dipole.', 'E = kp/(r² + a²)^(3/2) ≈ kp/r³, opposite to p',
     'Equal magnitudes kq/(r² + a²) (1); components along the axis add, perpendicular cancel (2); result (1); limit (1).'),
    ('Derive the expression for the torque on an electric dipole in a uniform electric field, and state when it is maximum.', 'τ = pE sin θ; maximum pE at θ = 90°',
     'Forces ±qE, couple arm 2a sin θ (2); τ = qE × 2a sin θ = pE sin θ (2); vector form p × E, maximum at 90° (1).'),
])


def c1s3_case(r):
    who = name(r)
    v = r.choice([2, 3, 4, 5]) * 1e6
    Ev = r.choice([1, 2, 3]) * 1e3
    L = r.choice([2, 3, 4, 5])
    t = L / 100 / v
    a = QE * Ev / ME
    y = 0.5 * a * t * t
    return {'stem': (f'In a cathode-ray tube demonstration, {who} sends electrons horizontally at {g(v)} m s⁻¹ into the region between two horizontal plates {L} cm long. '
                     f'The field between the plates is {g(Ev)} N C⁻¹, directed upward. (e = 1.6 × 10⁻¹⁹ C, mₑ = 9.1 × 10⁻³¹ kg)\n'
                     '(i) In which direction are the electrons deflected? (ii) Find their acceleration. (iii) Find the time spent between the plates. (iv) Find the vertical deflection on leaving the plates.'),
            'answer': f'(i) downward (opposite to E) (ii) {sig(a)} m s⁻² (iii) {sig(t)} s (iv) {sig(y * 1000)} mm',
            'key': f'(i) force on electron is opposite to E (1). (ii) a = eE/m = {sig(a)} m s⁻² (1). (iii) t = L/v = {sig(t)} s (1). (iv) y = ½at² = {sig(y)} m (1). The path is a parabola.'}


# st4 flux and Gauss's law

c1s4_terms = term_mcq([('field of an infinitely long straight charged wire', 'λ/(2πε₀r)'), ('field of an infinite plane sheet of charge', 'σ/(2ε₀)'),
                       ('field outside a uniformly charged thin spherical shell', 'q/(4πε₀r²)'), ('field inside a uniformly charged thin spherical shell', 'zero'),
                       ('flux through a closed surface enclosing charge q', 'q/ε₀')],
                      'Using Gauss\'s law, the {a} is', 'Which result equals {b}?', '{a}: {b}.')

c1s4_tf = tf_mcq("electric flux and Gauss's law",
                 ['The flux through a closed surface depends only on the charge enclosed.', 'Charges outside a closed surface contribute zero net flux through it.', 'Electric flux is a scalar.',
                  'The SI unit of electric flux is N m² C⁻¹.', 'Gauss\'s law is valid for any closed surface, whatever its shape.'],
                 ['The flux through a closed surface depends on the shape of the surface.', 'Charges outside a closed surface change the net flux through it.', 'Electric flux is a vector.',
                  'Gauss\'s law holds only for spherical surfaces.', 'The field on a Gaussian surface is due only to the charges inside it.'])

c1s4_explain = pool_txt([
    ('Why is the electric field inside a charged conducting shell zero?', 'A Gaussian sphere inside encloses no charge, so the flux and, by symmetry, the field there are zero.', '2 marks.'),
    ('A point charge is at the centre of a cube. If the charge is moved off-centre (still inside), does the total flux change? Does the flux through each face change?', 'Total flux q/ε₀ does not change; the flux through individual faces changes.', '1 + 1 marks.'),
    ('What is a Gaussian surface? Why is it chosen to match the symmetry of the charge distribution?', 'An imaginary closed surface used to apply Gauss\'s law; with symmetry E is constant on it and can be taken out of the integral.', '2 marks.'),
    ('The net flux through a closed surface is zero. Does it mean the field is zero everywhere on the surface?', 'No; it means the net enclosed charge is zero. Field lines can enter and leave.', '2 marks.'),
])

c1s4_ar = pool_ar([
    ('The flux through a closed surface does not depend on charges outside it.', 'Every field line from an outside charge that enters the surface also leaves it.', 'a', 'R explains A.'),
    ('The field near an infinite plane sheet of charge is independent of distance from it.', 'Field lines of an infinite sheet are parallel and uniformly spaced.', 'a', 'R explains A.'),
    ('The field inside a uniformly charged thin spherical shell is zero.', 'There is no charge inside the shell.', 'a', 'A Gaussian sphere inside encloses no charge; R explains A.'),
    ('Gauss\'s law can be used to find the field of any charge distribution easily.', 'Gauss\'s law is true for any closed surface.', 'd', 'A is false: it is useful only with symmetry; R is true.'),
])


def c1s4_closed(r):
    q = r.choice([1, 2, 5, 8, 10]) * r.choice([1e-9, 1e-6])
    phi = q / E0
    return NUM(f'A point charge of {uc(q)} is placed inside a closed spherical surface of radius {r.choice([5, 10, 20])} cm. Find the net electric flux through the surface. (ε₀ = 8.854 × 10⁻¹² C² N⁻¹ m⁻²)', phi, 'N m² C⁻¹',
               f'Φ = q/ε₀ = {g(q)}/(8.854 × 10⁻¹²) = {{ans}}; independent of the radius.', wrongs=[q * E0, phi / (4 * math.pi), phi * 2], gap='G3')


def c1s4_flat(r):
    Ev = r.choice([100, 200, 300, 500])
    A = r.choice([10, 20, 25, 50, 100])
    th = r.choice([0, 30, 45, 60])
    phi = Ev * A * 1e-4 * math.cos(math.radians(th))
    return NUM(f'A uniform field of {Ev} N C⁻¹ passes through a flat square of area {A} cm². The normal to the square makes an angle of {th}° with the field. Find the flux through it.', phi, 'N m² C⁻¹',
               f'Φ = EA cos θ = {Ev} × {g(A * 1e-4)} × cos {th}° = {{ans}}.', wrongs=[Ev * A * 1e-4 * math.sin(math.radians(th)) or phi * 2, Ev * A * math.cos(math.radians(th)), phi / 2])


def c1s4_wire(r):
    lam = r.choice([1, 2, 3, 5]) * 1e-7
    d = r.choice([2, 5, 10, 20])
    Ev = lam / (2 * math.pi * E0 * d / 100)
    return NUM(f'An infinitely long straight wire carries a uniform linear charge density of {g(lam)} C m⁻¹. Find the electric field {d} cm from the wire. (ε₀ = 8.854 × 10⁻¹² C² N⁻¹ m⁻²)', Ev, 'N C⁻¹',
               f'E = λ/(2πε₀r) = {g(lam)}/(2π × 8.854 × 10⁻¹² × {g(d / 100)}) = {{ans}}.', wrongs=[lam / (4 * math.pi * E0 * (d / 100) ** 2), Ev * 2, Ev / 2])


def c1s4_sheet(r):
    sig_ = r.choice([1, 2, 5, 8, 17.7]) * 1e-6
    two = r.random() < 0.5
    Ev = sig_ / E0 if two else sig_ / (2 * E0)
    if two:
        st = f'Two large parallel plates carry equal and opposite surface charge densities of {g(sig_)} C m⁻². Find the field between them.'
        k = f'Between the plates the fields of the two sheets add: E = σ/ε₀ = {{ans}}; outside it is zero.'
    else:
        st = f'A large thin plane sheet carries a uniform surface charge density of {g(sig_)} C m⁻². Find the electric field near it.'
        k = 'E = σ/(2ε₀) = {ans}, perpendicular to the sheet.'
    return NUM(st + ' (ε₀ = 8.854 × 10⁻¹² C² N⁻¹ m⁻²)', Ev, 'N C⁻¹', k, wrongs=[sig_ / (2 * E0) if two else sig_ / E0, sig_ * E0, Ev / 2])


def c1s4_shell(r):
    Q = r.choice([1, 2, 4, 5]) * 1e-6
    R = r.choice([10, 20, 30])
    rr = r.choice([R // 2, R * 2, R * 3, R + 10])
    Ev = 0 if rr < R else K * Q / (rr / 100) ** 2
    if Ev == 0:
        return {'stem': f'A thin spherical shell of radius {R} cm carries a charge {uc(Q)} distributed uniformly. Find the field at a point {rr} cm from its centre.',
                'answer': '0 N C⁻¹', 'key': 'The point is inside the shell; a Gaussian sphere there encloses no charge, so E = 0.',
                'distractors': [f'{sig(K * Q / (rr / 100) ** 2)} N C⁻¹', f'{sig(K * Q / (R / 100) ** 2)} N C⁻¹', f'{sig(K * Q / (R / 100) ** 2 / 2)} N C⁻¹']}
    return NUM(f'A thin spherical shell of radius {R} cm carries a charge {uc(Q)} distributed uniformly. Find the field at a point {rr} cm from its centre.', Ev, 'N C⁻¹',
               f'The point is outside: E = kQ/r² = 9 × 10⁹ × {g(Q)}/({g(rr / 100)})² = {{ans}}.', wrongs=[K * Q / (R / 100) ** 2, K * Q / (rr / 100), 0.5 * Ev])


def c1s4_cube(r):
    q = r.choice([1, 2, 3, 6, 12]) * 1e-6
    phi = q / E0
    return NUM2(f'A point charge of {uc(q)} is at the centre of a cubical box. Find (i) the total flux through the box and (ii) the flux through one face. (ε₀ = 8.854 × 10⁻¹² C² N⁻¹ m⁻²)', (phi, phi / 6), ('N m² C⁻¹', 'N m² C⁻¹'),
                f'(i) Gauss\'s law: Φ = q/ε₀ = {sig(phi)} N m² C⁻¹ (1.5). (ii) by symmetry the six faces share equally: Φ/6 = {sig(phi / 6)} N m² C⁻¹ (1.5).',
                wrongs=[(phi, phi / 4), (phi * 6, phi), (q * E0, q * E0 / 6)])


def c1s4_net(r):
    out = r.choice([5, 8, 10, 12]) * 1e3
    inn = r.choice([1, 2, 3, 4]) * 1e3
    q = E0 * (out - inn)
    return NUM(f'For a closed surface, the flux leaving it is {g(out)} N m² C⁻¹ and the flux entering it is {g(inn)} N m² C⁻¹. Find the net charge enclosed. (ε₀ = 8.854 × 10⁻¹² C² N⁻¹ m⁻²)', q, 'C',
               f'Net outward flux = {g(out)} − {g(inn)} = {g(out - inn)} N m² C⁻¹ (1); q = ε₀Φ (1) = {{ans}}, positive (1).', wrongs=[E0 * (out + inn), (out - inn) / E0, E0 * out], gap='G5')


c1s4_derive = pool_txt([
    ('Using Gauss\'s law, derive the field due to an infinitely long straight uniformly charged wire.', 'E = λ/(2πε₀r), radial',
     'Cylindrical Gaussian surface (1); flux through ends zero (1); E × 2πrl = λl/ε₀ (2); result (1).'),
    ('Using Gauss\'s law, derive the field due to a uniformly charged infinite plane sheet.', 'E = σ/(2ε₀)', 'Pill-box Gaussian surface (1); flux 2EA (2); enclosed charge σA (1); result (1).'),
    ('Using Gauss\'s law, find the field outside and inside a uniformly charged thin spherical shell.', 'Outside: q/(4πε₀r²); inside: 0', 'Concentric Gaussian sphere (1); outside (2); inside (2).'),
])


def c1s4_case(r):
    R = r.choice([5, 10, 15, 20])
    Q = r.choice([1, 2, 4]) * 1e-8
    sigma = Q / (4 * math.pi * (R / 100) ** 2)
    Es = K * Q / (R / 100) ** 2
    rr = 2 * R
    return {'stem': (f'A Van de Graaff demonstration dome is modelled as a conducting sphere of radius {R} cm carrying a charge of {g(Q)} C.\n'
                     f'(i) Where does the charge reside? (ii) Find the surface charge density. (iii) Find the field just outside the surface. (iv) Find the field at {rr} cm from the centre and at the centre.'),
            'answer': f'(i) on the outer surface (ii) {sig(sigma)} C m⁻² (iii) {sig(Es)} N C⁻¹ (iv) {sig(Es / 4)} N C⁻¹; zero at the centre',
            'key': f'(i) outer surface (1). (ii) σ = Q/4πR² (1). (iii) E = kQ/R² = σ/ε₀ (1). (iv) at 2R the field is a quarter, E = 0 inside (1).'}


# ======================================================== ch02 Electrostatic Potential and Capacitance
# st1 potential and potential energy

c2s1_terms = term_mcq([('electrostatic potential at a point', 'work done per unit positive charge in bringing it from infinity to that point'),
                       ('potential difference', 'work done per unit charge in moving a charge between two points'),
                       ('electron volt', 'energy gained by an electron accelerated through 1 V, 1.6 × 10⁻¹⁹ J'),
                       ('potential energy of a system of two charges', 'q₁q₂/(4πε₀r₁₂)'), ('potential due to a dipole', 'p cos θ/(4πε₀r²)')],
                      'Which of the following describes the {a}?', 'Which quantity is {b}?', '{a}: {b}.')

c2s1_tf = tf_mcq('electrostatic potential',
                 ['Potential is a scalar quantity.', 'The potential due to a point charge varies as 1/r.', 'The potential on the equatorial line of a dipole is zero.',
                  'The electrostatic force is conservative, so work done is independent of path.', 'Potential due to a dipole falls off as 1/r².'],
                 ['Potential is a vector quantity.', 'The potential due to a point charge varies as 1/r².', 'Where the field is zero, the potential must also be zero.',
                  'Work done in moving a charge depends on the path taken.', 'The potential on the equatorial line of a dipole is maximum.'])

c2s1_explain = pool_txt([
    ('Can the electric field be zero at a point where the potential is not zero? Give an example.', 'Yes; inside a charged conducting sphere E = 0 but V = kQ/R.', '2 marks.'),
    ('Why is the work done in moving a charge along a closed path in an electrostatic field zero?', 'The electrostatic force is conservative; work depends only on end points, which coincide.', '2 marks.'),
    ('Two points are on the equatorial line of a dipole. How much work is done in moving a charge from one to the other?', 'Zero, because the potential at every point of the equatorial line is zero.', '2 marks.'),
    ('Why is the potential of the Earth taken as zero?', 'The Earth is a very large conductor; adding or removing charge hardly changes its potential, so it is a convenient reference.', '2 marks.'),
])

c2s1_ar = pool_ar([
    ('Work done in moving a charge between two points in an electrostatic field is independent of the path.', 'The electrostatic force is a conservative force.', 'a', 'R explains A.'),
    ('The potential at the midpoint of a dipole is zero, but the field there is not zero.', 'Potential is a scalar and field is a vector.', 'a', 'Potentials of ±q cancel; fields add. R explains A.'),
    ('The electron volt is a unit of potential.', '1 eV = 1.6 × 10⁻¹⁹ J.', 'd', 'A is false: eV is a unit of energy; R is true.'),
    ('An electron moves from a region of lower potential to higher potential on its own.', 'A negative charge experiences force opposite to the field.', 'a', 'R explains A.'),
])


def c2s1_V(r):
    q = r.choice([1, 2, 4, 5, 8]) * 1e-9
    d = r.choice([5, 9, 10, 15, 30])
    V = K * q / (d / 100)
    return NUM(f'Find the potential at a point {d} cm from a point charge of {uc(q)} in air.', V, 'V', f'V = kq/r = 9 × 10⁹ × {g(q)}/{g(d / 100)} = {{ans}}.',
               wrongs=[K * q / (d / 100) ** 2, V * 100, V / 2], gap='G3')


def c2s1_work(r):
    q = r.choice([2, 3, 5, 10]) * 1e-6
    V1 = r.choice([10, 20, 50, 100])
    V2 = V1 + r.choice([20, 40, 50, 100, 150])
    W = q * (V2 - V1)
    return NUM(f'How much work is done in moving a charge of {uc(q)} from a point at potential {V1} V to a point at potential {V2} V?', W, 'J',
               f'W = q(V_B − V_A) = {g(q)} × ({V2} − {V1}) = {{ans}}.', wrongs=[q * (V2 + V1), q * V2, (V2 - V1) / q], gap='G3')


def c2s1_square(r):
    qs = [r.choice([1, 2, 3, 4, 5]) * r.choice([1, -1]) for _ in range(4)]
    a = r.choice([10, 20, 30])
    d = a / 100 / math.sqrt(2)
    V = K * sum(qs) * 1e-6 / d
    t = ', '.join(f'{q:+d} μC'.replace('-', '−') for q in qs)
    if sum(qs) == 0:
        return {'stem': f'Charges {t} are placed at the four corners of a square of side {a} cm. Find the potential at the centre of the square.', 'answer': '0 V',
                'key': 'Each corner is a/√2 from the centre (1); V = kΣq/(a/√2) and Σq = 0, so V = 0 (2). (The field at the centre need not be zero.)',
                'distractors': [f'{sig(K * sum(abs(x) for x in qs) * 1e-6 / d)} V', f'{sig(K * 1e-6 / d)} V', f'{sig(K * sum(abs(x) for x in qs) * 1e-6 / (a / 100))} V']}
    return NUM(f'Charges {t} are placed at the four corners of a square of side {a} cm. Find the potential at the centre of the square.', V, 'V',
               f'Each corner is a/√2 = {sig(d)} m from the centre (1); V = kΣq/(a/√2) = 9 × 10⁹ × {sum(qs)} × 10⁻⁶/{sig(d)} (1) = {{ans}} (1).'.replace('× -', '× −'),
               wrongs=[K * sum(qs) * 1e-6 / (a / 100), K * sum(abs(x) for x in qs) * 1e-6 / d, V * math.sqrt(2)], gap='G5')


def c2s1_pe(r):
    q1 = r.choice([1, 2, 3, 4]) * 1e-6
    q2 = r.choice([1, 2, 5, 6]) * 1e-6 * r.choice([1, -1])
    d = r.choice([10, 20, 30, 50])
    U = K * q1 * q2 / (d / 100)
    return NUM(f'Find the electrostatic potential energy of a system of two charges {uc(q1)} and {uc(q2).replace("-", "−")} placed {d} cm apart in air.', U, 'J',
               f'U = kq₁q₂/r = 9 × 10⁹ × {g(q1)} × ({g(q2)})/{g(d / 100)} = {{ans}}.'.replace('(-', '(−'), wrongs=[-U, K * q1 * q2 / (d / 100) ** 2, U * 2])


def c2s1_three(r):
    q = r.choice([1, 2, 3]) * 1e-6
    a = r.choice([10, 20, 30])
    signs = r.choice([(1, 1, 1), (1, 1, -1), (1, -1, -1)])
    pairs = signs[0] * signs[1] + signs[1] * signs[2] + signs[0] * signs[2]
    U = K * q * q * pairs / (a / 100)
    t = ', '.join(('+' if s > 0 else '−') + uc(q) for s in signs)
    return NUM(f'Three charges {t} are placed at the vertices of an equilateral triangle of side {a} cm. Find the potential energy of the system, i.e. the work done in assembling it from infinity.', U, 'J',
               f'U = k(q₁q₂ + q₂q₃ + q₃q₁)/a (1) = 9 × 10⁹ × ({pairs}) × ({g(q)})²/{g(a / 100)} (1) = {{ans}} (1).', wrongs=[K * q * q * 3 / (a / 100) if pairs != 3 else U / 3, -U, U * 2], gap='G5')


def c2s1_dipole(r):
    p = r.choice([2, 4, 5, 6]) * 1e-10
    d = r.choice([10, 20, 30])
    th = r.choice([0, 60, 90, 180])
    V = K * p * math.cos(math.radians(th)) / (d / 100) ** 2
    if abs(V) < 1e-12:
        V = 0.0
        return {'stem': f'A dipole of moment {g(p)} C m is at the origin. Find the potential at a point {d} cm from it, along a direction making {th}° with p.', 'answer': '0 V',
                'key': 'V = kp cos θ/r² and cos 90° = 0, so V = 0 on the equatorial line.', 'distractors': [f'{sig(K * p / (d / 100) ** 2)} V', f'{sig(2 * K * p / (d / 100) ** 3)} V', f'{sig(K * p / (d / 100))} V']}
    return NUM(f'A dipole of moment {g(p)} C m is at the origin. Find the potential at a point {d} cm from it, along a direction making {th}° with p.', V, 'V',
               f'V = kp cos θ/r² = 9 × 10⁹ × {g(p)} × cos {th}°/({g(d / 100)})² = {{ans}}.', wrongs=[K * p / (d / 100) ** 3, -V, V * 2])


def c2s1_zero(r):
    q1 = r.choice([2, 3, 4, 5, 6])
    q2 = r.choice([1, 2, 3, 4])
    d = r.choice([10, 20, 30, 50])
    x = q1 * d / (q1 + q2)
    return NUM(f'Charges +{q1} × 10⁻⁸ C and −{q2} × 10⁻⁸ C are placed {d} cm apart. At what point between them is the electric potential zero? Give its distance from the positive charge.', x, 'cm',
               f'kq₁/x = kq₂/(d − x) (1) ⇒ x = q₁d/(q₁ + q₂) = {q1} × {d}/{q1 + q2} (1) = {{ans}} (1).', wrongs=[q2 * d / (q1 + q2), d / (1 + math.sqrt(q2 / q1)), d / 2], gap='G5')


def c2s1_speed(r):
    V = r.choice([100, 200, 500, 1000, 2000])
    v = math.sqrt(2 * QE * V / ME)
    return NUM2(f'An electron starting from rest is accelerated through a potential difference of {V} V. Find its kinetic energy (in J) and its final speed.', (QE * V, v), ('J', 'm s⁻¹'),
                f'K = eV = {V} eV = {sig(QE * V)} J (1); ½mv² = eV (1) ⇒ v = √(2eV/m) = {sig(v)} m s⁻¹ (1).',
                wrongs=[(QE * V, math.sqrt(QE * V / ME)), (QE * V / 2, v / math.sqrt(2)), (QE * V, math.sqrt(2 * QE * V / MP))], gap='G5')


c2s1_derive = pool_txt([
    ('Derive an expression for the potential due to an electric dipole at a point at distance r making angle θ with the dipole axis (r ≫ a).', 'V = p cos θ/(4πε₀r²)',
     'V = kq/r₁ − kq/r₂ (1); r₁, r₂ ≈ r ∓ a cos θ (2); simplify (1); special cases (1).'),
    ('Derive an expression for the potential energy of a dipole in a uniform electric field.', 'U = −pE cos θ = −p·E', 'Work done by torque from θ₀ = 90° to θ (3); result and stable/unstable positions (2).'),
    ('Derive an expression for the potential due to a point charge q at distance r.', 'V = q/(4πε₀r)', 'Work against force from ∞ to r (3); integrate kq/r² (1); result (1).'),
])


# st2 equipotentials and conductors

c2s2_terms = term_mcq([('equipotential surfaces of a point charge', 'concentric spheres centred on the charge'),
                       ('equipotential surfaces of a uniform field', 'planes perpendicular to the field'),
                       ('relation between E and V', 'E = −dV/dr, pointing in the direction of steepest fall of potential'),
                       ('electrostatic shielding', 'the field inside a cavity of a conductor is zero'),
                       ('field just outside a charged conductor', 'σ/ε₀, normal to the surface')],
                      'Which of the following correctly describes {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c2s2_tf = tf_mcq('conductors in electrostatics',
                 ['Inside a conductor the electrostatic field is zero.', 'The surface of a charged conductor is an equipotential.', 'Any excess charge on a conductor resides on its surface.',
                  'The field just outside a conductor is normal to its surface.', 'Equipotential surfaces are perpendicular to field lines.'],
                 ['Excess charge on a conductor is spread uniformly through its volume.', 'The field inside a charged conductor is maximum.', 'The potential inside a charged conductor is zero.',
                  'Two equipotential surfaces can intersect.', 'Work is needed to move a charge along an equipotential surface.'])

c2s2_explain = pool_txt([
    ('Why is it safer to sit inside a car than under a tree during a thunderstorm?', 'The car\'s metal body acts as a shield: charge stays on the outer surface and the field inside is zero.', '2 marks.'),
    ('Why do two equipotential surfaces never intersect?', 'At the intersection the potential would have two values and the field two directions, which is impossible.', '2 marks.'),
    ('Why is charge density larger at the pointed ends of a conductor?', 'σ ∝ 1/R for connected parts; sharp points have small radius of curvature, so σ and the field there are large.', '2 marks.'),
    ('Explain why the electric field is always normal to the surface of a conductor.', 'A tangential component would move the free charges on the surface; in equilibrium it must be zero.', '2 marks.'),
])

c2s2_ar = pool_ar([
    ('No work is done in moving a charge on an equipotential surface.', 'The potential difference between any two points on it is zero.', 'a', 'W = qΔV = 0; R explains A.'),
    ('The interior of a hollow conductor is shielded from external electric fields.', 'Charges on a conductor reside on its outer surface.', 'a', 'R explains A.'),
    ('Equipotential surfaces are closer together where the field is stronger.', 'E = −dV/dr.', 'a', 'For the same ΔV, smaller spacing means larger E; R explains A.'),
    ('The potential is zero inside a charged hollow conducting sphere.', 'The field is zero inside a charged hollow conducting sphere.', 'd', 'A is false: V is constant (= kQ/R), not zero; R is true.'),
])


def c2s2_Ed(r):
    dV = r.choice([5, 10, 20, 50])
    d = r.choice([1, 2, 5, 10])
    Ev = dV / (d / 100)
    return NUM(f'Equipotential surfaces in a region are parallel planes, the potential falling by {dV} V between successive surfaces {d} cm apart. Find the magnitude of the electric field.', Ev, 'V m⁻¹',
               f'E = ΔV/Δr = {dV}/{g(d / 100)} = {{ans}}, perpendicular to the planes towards lower potential.', wrongs=[dV * d / 100, dV / d, Ev * 10], gap='G3')


def c2s2_sphere(r):
    R = r.choice([5, 10, 15, 20])
    Q = r.choice([1, 2, 3, 5]) * 1e-9
    Vs = K * Q / (R / 100)
    return NUM2(f'A conducting sphere of radius {R} cm carries a charge of {uc(Q)}. Find (i) the potential at its surface and (ii) the potential and field at its centre.', (Vs, Vs), ('V', 'V'),
                f'(i) V = kQ/R = {sig(Vs)} V (1). (ii) the inside is equipotential with the surface: V = {sig(Vs)} V, E = 0 (1).', wrongs=[(Vs, 0), (K * Q / (R / 100) ** 2, Vs), (Vs, Vs * 2)], sep='; centre: ')


def c2s2_spheres(r):
    R1 = r.choice([1, 2, 3, 5])
    R2 = r.choice([4, 6, 9, 10])
    Q = r.choice([10, 20, 30, 60])
    q1 = Q * R1 / (R1 + R2)
    q2 = Q - q1
    return NUM2(f'Two isolated conducting spheres of radii {R1} cm and {R2} cm, far apart, are connected by a thin wire and given a total charge of {Q} nC. Find the charge on each sphere and the ratio σ₁/σ₂ of their surface charge densities.',
                (q1, q2, R2 / R1), ('nC', 'nC', ''), f'Equal potential: q₁/R₁ = q₂/R₂ (1) ⇒ q₁ = Q R₁/(R₁ + R₂) = {sig(q1)} nC, q₂ = {sig(q2)} nC (1); σ₁/σ₂ = R₂/R₁ = {sig(R2 / R1)} (1).',
                wrongs=[(q2, q1, R1 / R2), (Q / 2, Q / 2, 1.0), (q1, q2, (R2 / R1) ** 2)])


def c2s2_move(r):
    q = r.choice([2, 5, 10]) * 1e-6
    V = r.choice([20, 50, 100, 200])
    return mcq(f'A charge of {uc(q)} is moved along an equipotential surface of potential {V} V for a distance of {r.choice([2, 5, 10])} cm. The work done is', '0 J',
               [f'{sig(q * V)} J', f'{sig(q / V)} J', f'{sig(V / q)} J'], 'ΔV = 0 along an equipotential, so W = qΔV = 0.', r)


def c2s2_case(r):
    V1, V2, V3 = 10, 20, 30
    d = r.choice([1, 2, 5])
    Ev = 10 / (d / 100)
    q = r.choice([2, 5]) * 1e-6
    return {'stem': (f'In a region of uniform electric field, three equipotential planes of potential {V1} V, {V2} V and {V3} V are drawn {d} cm apart from each other.\n'
                     f'(i) What is the angle between the field lines and the equipotential planes? (ii) Which way does the field point? (iii) Find the magnitude of the field. (iv) Find the work done by the field when a charge of {uc(q)} moves from the {V3} V plane to the {V1} V plane.'),
            'answer': f'(i) 90° (ii) from the {V3} V plane towards the {V1} V plane (iii) {sig(Ev)} V m⁻¹ (iv) {sig(q * 20)} J',
            'key': f'(i) field ⟂ equipotentials (1). (ii) towards decreasing potential (1). (iii) E = ΔV/d = 10/{g(d / 100)} (1). (iv) W = q(V_A − V_B) = q × 20 V (1).'}


# st3 dielectrics and polarisation

c2s3_terms = term_mcq([('polar molecule', 'a molecule with a permanent dipole moment, e.g. H₂O'), ('non-polar molecule', 'a molecule whose positive and negative charge centres coincide, e.g. O₂'),
                       ('polarisation', 'dipole moment per unit volume of a dielectric'), ('dielectric constant', 'K = C/C₀, the factor by which capacitance increases'),
                       ('dielectric strength', 'the maximum field a dielectric can withstand without breakdown')],
                      'Which of the following describes a {a}?', 'Which term is {b}?', '{a}: {b}.')

c2s3_tf = tf_mcq('dielectrics',
                 ['A dielectric placed in an external field reduces the field inside it.', 'Water molecules are polar.', 'Inserting a dielectric slab between capacitor plates increases the capacitance.',
                  'Dielectric constant K = ε/ε₀ is always greater than 1 for a dielectric.'],
                 ['A dielectric increases the field inside it.', 'Oxygen molecules have a permanent dipole moment.', 'Inserting a dielectric decreases capacitance.',
                  'In a dielectric, charges move freely as in a conductor.'])

c2s3_explain = pool_txt([
    ('Explain how a non-polar dielectric gets polarised in an external electric field.', 'The field displaces the positive and negative charge centres of each molecule, inducing dipoles aligned with the field.', '2 marks.'),
    ('Why does the field inside a dielectric decrease when it is placed in an external field?', 'Induced surface charges of the polarised dielectric produce a field opposite to the applied field.', '2 marks.'),
    ('A capacitor is charged and disconnected from the battery. A dielectric slab is then inserted. What happens to Q, V and the stored energy?', 'Q stays the same, V decreases to V/K, and energy decreases to U/K.', '2 marks.'),
])

c2s3_ar = pool_ar([
    ('A dielectric slab inserted between the plates of an isolated charged capacitor reduces the potential difference.', 'The induced charges on the dielectric reduce the field between the plates.', 'a', 'R explains A.'),
    ('Polar molecules in a dielectric are randomly oriented in the absence of a field.', 'Thermal agitation disturbs their alignment.', 'a', 'R explains A.'),
    ('Metals have infinite dielectric constant.', 'The field inside a metal in electrostatics is zero.', 'a', 'K = E₀/E → ∞; R explains A.'),
    ('The capacitance of a capacitor decreases when a dielectric is inserted.', 'The field between the plates is reduced by the dielectric.', 'd', 'A is false: C increases K times; R is true.'),
])

c2s3_mcq = pool_mcq([
    ('A charged capacitor is kept connected to a battery while a dielectric slab (K) is inserted. The charge on it', 'becomes K times', ['becomes 1/K times', 'stays the same', 'becomes zero'], 'V is fixed by the battery; C → KC so Q → KQ.'),
    ('A charged capacitor is disconnected from the battery and a dielectric slab (K) is inserted. The energy stored', 'becomes 1/K times', ['becomes K times', 'stays the same', 'becomes K² times'], 'Q fixed, U = Q²/2C → U/K.'),
    ('A charged capacitor is kept connected to a battery while a dielectric slab (K) is inserted. The field between the plates', 'stays the same', ['becomes K times', 'becomes 1/K times', 'becomes zero'], 'E = V/d with V and d fixed.'),
    ('A charged capacitor is disconnected from the battery and a dielectric slab (K) fills the gap. The potential difference', 'becomes 1/K times', ['becomes K times', 'stays the same', 'doubles'], 'V = Q/C with C → KC.'),
])


def c2s3_K(r):
    A = r.choice([50, 100, 200, 400])
    d = r.choice([1, 2, 4, 5])
    Kd = r.choice([2, 3, 4, 5, 6])
    C = Kd * E0 * A * 1e-4 / (d * 1e-3)
    return NUM(f'A parallel plate capacitor has plates of area {A} cm² separated by {d} mm, and the space is filled with a dielectric of dielectric constant {Kd}. Find its capacitance.', C, 'F',
               f'C = Kε₀A/d = {Kd} × 8.854 × 10⁻¹² × {g(A * 1e-4)}/{g(d * 1e-3)} = {{ans}}.', wrongs=[E0 * A * 1e-4 / (d * 1e-3), C * 100, C / Kd ** 2])


def c2s3_slab(r):
    A = r.choice([100, 200, 400])
    d = r.choice([4, 6, 8, 10])
    t = r.choice([1, 2, 3]) * d / 4
    Kd = r.choice([2, 4, 5, 6])
    C0 = E0 * A * 1e-4 / (d * 1e-3)
    C = E0 * A * 1e-4 / ((d - t + t / Kd) * 1e-3)
    return NUM2(f'A parallel plate capacitor has plate area {A} cm² and plate separation {d} mm. A dielectric slab of thickness {g(t)} mm and dielectric constant {Kd} is inserted parallel to the plates. Find the capacitance before and after inserting the slab.',
                (C0, C), ('F', 'F'), f'C₀ = ε₀A/d = {sig(C0)} F (1); with slab C = ε₀A/(d − t + t/K) (1) = {sig(C)} F (1).',
                wrongs=[(C0, Kd * C0), (C0, E0 * A * 1e-4 / ((d - t) * 1e-3)), (C0 * 10, C * 10)], sep='; after: ')


def c2s3_field(r):
    E_0 = r.choice([1, 2, 3, 5]) * 1e5
    Kd = r.choice([2, 4, 5, 8])
    return NUM(f'The field between the plates of an isolated charged capacitor is {g(E_0)} V m⁻¹. A dielectric of constant {Kd} is introduced to fill the space. Find the new field inside the dielectric.', E_0 / Kd, 'V m⁻¹',
               f'E = E₀/K = {g(E_0)}/{Kd} = {{ans}}.', wrongs=[E_0 * Kd, E_0, E_0 / Kd ** 2])


def c2s3_Kfind(r):
    C0 = r.choice([2, 4, 5, 10, 20])
    Kd = r.choice([2, 2.5, 3, 4, 6])
    return NUM(f'A capacitor has capacitance {C0} pF in air. When the gap is completely filled with a dielectric its capacitance becomes {g(C0 * Kd)} pF. Find the dielectric constant.', Kd, '',
               f'K = C/C₀ = {g(C0 * Kd)}/{C0} = {{ans}}.', wrongs=[1 / Kd, Kd * 2, Kd - 1], gap='G3', n=2)


# st4 capacitors

c2s4_tf = tf_mcq('capacitors',
                 ['The capacitance of a parallel plate capacitor is ε₀A/d.', 'In series, the charge on each capacitor is the same.', 'In parallel, the potential difference across each capacitor is the same.',
                  'The energy stored in a capacitor is ½CV².', 'The energy density in an electric field is ½ε₀E².'],
                 ['The capacitance of a capacitor depends on the charge on it.', 'In series, the potential difference across each capacitor is the same.', 'Capacitors in series add like resistors in series.',
                  'The energy stored in a capacitor is CV².', 'Doubling the plate separation doubles the capacitance.'])

c2s4_explain = pool_txt([
    ('Why does the capacitance of a parallel plate capacitor increase when the plate area is increased?', 'C = ε₀A/d: a larger area holds more charge for the same potential difference.', '2 marks.'),
    ('Where is the energy of a charged capacitor stored?', 'In the electric field between the plates; energy density u = ½ε₀E².', '2 marks.'),
    ('Two capacitors are connected in series. Why does the smaller capacitor have the larger potential difference?', 'Same Q on each; V = Q/C, so smaller C gives larger V.', '2 marks.'),
])

c2s4_ar = pool_ar([
    ('The equivalent capacitance of capacitors in series is less than the smallest of them.', '1/C = 1/C₁ + 1/C₂ + …', 'a', 'R explains A.'),
    ('Some energy is lost when a charged capacitor is connected to an uncharged one.', 'Charge flows until the two potentials become equal; energy is dissipated as heat and radiation.', 'a', 'R explains A.'),
    ('The capacitance of a capacitor increases when it is charged to a higher potential.', 'Q = CV.', 'd', 'A is false: C depends only on geometry and medium; R is true.'),
    ('The plates of a charged capacitor attract each other.', 'They carry equal and opposite charges.', 'a', 'R explains A.'),
])


def c2s4_pp(r):
    A = r.choice([1, 2, 4, 6]) * 1e-2 if r.random() < 0.5 else r.choice([50, 100, 200]) * 1e-4
    d = r.choice([1, 2, 3, 5])
    C = E0 * A / (d * 1e-3)
    return NUM(f'Find the capacitance of a parallel plate capacitor whose plates each have area {g(A)} m² and are separated by {d} mm of air. (ε₀ = 8.854 × 10⁻¹² F m⁻¹)', C, 'F',
               f'C = ε₀A/d = 8.854 × 10⁻¹² × {g(A)}/{g(d * 1e-3)} = {{ans}}.', wrongs=[E0 * A / d, C * 1000, E0 * d * 1e-3 / A], gap='G3')


def c2s4_comb(r):
    cs = r.sample([1, 2, 3, 4, 6, 12], 3)
    ser = r.random() < 0.5
    V = r.choice([6, 12, 24, 100])
    if ser:
        Ceq = 1 / sum(1 / c for c in cs)
        Q = Ceq * V
        return NUM2(f'Three capacitors of {cs[0]} μF, {cs[1]} μF and {cs[2]} μF are connected in series across a {V} V supply. Find the equivalent capacitance and the charge on each capacitor.',
                    (Ceq, Q), ('μF', 'μC'), f'1/C = 1/{cs[0]} + 1/{cs[1]} + 1/{cs[2]} ⇒ C = {sig(Ceq)} μF (1); Q = CV = {sig(Q)} μC on each (1).', wrongs=[(sum(cs), sum(cs) * V), (Ceq, Q * 3), (Ceq, V / Ceq)])
    Ceq = sum(cs)
    return NUM2(f'Three capacitors of {cs[0]} μF, {cs[1]} μF and {cs[2]} μF are connected in parallel across a {V} V supply. Find the equivalent capacitance and the total charge drawn.',
                (Ceq, Ceq * V), ('μF', 'μC'), f'C = {cs[0]} + {cs[1]} + {cs[2]} = {Ceq} μF (1); Q = CV = {sig(Ceq * V)} μC (1).', wrongs=[(1 / sum(1 / c for c in cs), V / sum(1 / c for c in cs)), (Ceq, Ceq / V), (Ceq, Ceq * V * 2)])


def c2s4_network(r):
    C1, C2 = r.choice([(2, 2), (3, 6), (4, 4), (6, 12), (2, 6)])
    C3 = r.choice([1, 2, 3, 4])
    V = r.choice([10, 12, 20, 30])
    Cs = C1 * C2 / (C1 + C2)
    Ceq = Cs + C3
    Qs = Cs * V
    V1 = Qs / C1
    return NUM2(f'Capacitors C₁ = {C1} μF and C₂ = {C2} μF are connected in series, and this combination is connected in parallel with C₃ = {C3} μF. The network is connected to a {V} V battery. Find (i) the equivalent capacitance, (ii) the charge on C₁ and (iii) the potential difference across C₁.',
                (Ceq, Qs, V1), ('μF', 'μC', 'V'), f'(i) C₁₂ = C₁C₂/(C₁ + C₂) = {sig(Cs)} μF; C = C₁₂ + C₃ = {sig(Ceq)} μF (2). (ii) Q₁ = C₁₂V = {sig(Qs)} μC (1.5). (iii) V₁ = Q₁/C₁ = {sig(V1)} V (1.5).',
                wrongs=[(C1 + C2 + C3, C1 * V, float(V)), (1 / (1 / C1 + 1 / C2 + 1 / C3), Qs, V1), (Ceq, Ceq * V, V1)], sep='; ')


def c2s4_energy(r):
    C = r.choice([2, 5, 10, 20, 50, 100])
    V = r.choice([10, 20, 50, 100, 200])
    U = 0.5 * C * 1e-6 * V * V
    return NUM(f'A {C} μF capacitor is charged to {V} V. Find the energy stored in it.', U, 'J', f'U = ½CV² = ½ × {g(C * 1e-6)} × {V}² = {{ans}}.', wrongs=[C * 1e-6 * V * V, 0.5 * C * 1e-6 * V, U * 1e6])


def c2s4_share(r):
    C1 = r.choice([2, 4, 6, 10])
    C2 = r.choice([2, 3, 4, 5, 10])
    V0 = r.choice([50, 100, 200, 300])
    Vc = C1 * V0 / (C1 + C2)
    Ui = 0.5 * C1 * 1e-6 * V0 ** 2
    Uf = 0.5 * (C1 + C2) * 1e-6 * Vc ** 2
    return NUM2(f'A {C1} μF capacitor is charged to {V0} V and disconnected from the supply. It is then connected across an uncharged {C2} μF capacitor. Find (i) the common potential and (ii) the energy lost in the process.',
                (Vc, Ui - Uf), ('V', 'J'), f'(i) charge is conserved: V = C₁V₀/(C₁ + C₂) = {sig(Vc)} V (2). (ii) U_i = ½C₁V₀² = {sig(Ui)} J, U_f = ½(C₁ + C₂)V² = {sig(Uf)} J (2); loss = {sig(Ui - Uf)} J, as heat (1).',
                wrongs=[(V0 / 2, Ui / 2), (Vc, Uf), (C2 * V0 / (C1 + C2), Ui - Uf)], sep='; ')


def c2s4_change(r):
    k = r.choice([2, 3, 4])
    q = r.choice([('plate separation is made {k} times', 1 / k, 'C ∝ 1/d'), ('plate area is made {k} times', k, 'C ∝ A'), ('gap is filled with a dielectric of constant {k}', k, 'C ∝ K')])
    stem, f, why = q
    return NUM(f'A parallel plate capacitor has capacitance C. By what factor does its capacitance change if the {stem.format(k=k)}?', f, '', f'{why}, so the factor is {{ans}}.', wrongs=[1 / f, f * f, f * 2], gap='G3', n=3)


c2s4_derive = pool_txt([
    ('Derive an expression for the capacitance of a parallel plate capacitor.', 'C = ε₀A/d', 'E = σ/ε₀ between plates (2); V = Ed (1); C = Q/V = ε₀A/d (2).'),
    ('Derive an expression for the energy stored in a capacitor and hence the energy density of the field.', 'U = ½CV² = Q²/2C; u = ½ε₀E²', 'dW = (q/C) dq integrated (2); U = Q²/2C (1); with C = ε₀A/d, E = V/d: u = U/(Ad) = ½ε₀E² (2).'),
    ('Derive the formula for the equivalent capacitance of capacitors in series and in parallel.', '1/C = Σ1/Cᵢ (series); C = ΣCᵢ (parallel)', 'Series: same Q, V adds (2.5). Parallel: same V, Q adds (2.5).'),
])


def c2s4_case(r):
    who = name(r)
    C = r.choice([10, 20, 47, 100])
    V = r.choice([9, 12, 24])
    U = 0.5 * C * 1e-6 * V * V
    return {'stem': (f'{who} is building a camera flash circuit. A {C} μF capacitor is charged by a {V} V battery and then discharged through the flash bulb in a short time.\n'
                     '(i) Find the charge on the capacitor when fully charged. (ii) Find the energy stored. (iii) If two such capacitors were joined in series across the same battery, what would be the total energy stored? (iv) Why is a capacitor used rather than the battery directly?'),
            'answer': f'(i) {sig(C * V)} μC (ii) {sig(U)} J (iii) {sig(U / 2)} J (iv) it can release its energy very quickly, giving a large current for a short time',
            'key': '(i) Q = CV (1). (ii) U = ½CV² (1). (iii) series: C/2, U = ½(C/2)V² (1). (iv) rapid discharge (1).'}


# ======================================================== ch03 Current Electricity
# st1 drift velocity, mobility, Ohm's law, resistivity, temperature

c3s1_terms = term_mcq([('drift velocity', 'the average velocity acquired by free electrons in the direction opposite to the field'),
                       ('mobility', 'drift velocity per unit electric field, μ = v_d/E'), ('relaxation time', 'the average time between successive collisions of an electron'),
                       ('resistivity', 'the resistance of a conductor of unit length and unit cross-sectional area'), ('current density', 'current per unit area normal to the flow, j = I/A')],
                      'Which of the following defines {a}?', 'Which term is {b}?', '{a}: {b}.')

c3s1_tf = tf_mcq("Ohm's law and resistivity",
                 ['Resistivity of a metal increases with temperature.', 'Resistivity depends on the material, not on the length of the wire.', 'Manganin and constantan have very small temperature coefficients.',
                  'Resistivity of a semiconductor decreases as temperature rises.', 'ρ = m/(ne²τ) for a metal.'],
                 ['Resistivity of a wire increases with its length.', 'Resistivity of a metal decreases with temperature.', 'Ohm\'s law holds for all devices, including diodes.',
                  'Drift velocity of electrons is of the order of the speed of light.', 'Resistivity of a semiconductor increases with temperature.'])

c3s1_explain = pool_txt([
    ('Drift speed of electrons is only about 1 mm s⁻¹. Why then does a bulb light almost instantly when switched on?', 'The electric field is set up throughout the circuit almost instantly, so electrons everywhere start drifting at once.', '2 marks.'),
    ('Why does the resistance of a metallic conductor increase with temperature?', 'Ions vibrate more; collisions become more frequent, τ decreases, so ρ = m/(ne²τ) increases.', '2 marks.'),
    ('Why are manganin and constantan used for standard resistors?', 'Their resistivity is high and changes very little with temperature.', '2 marks.'),
    ('Give two examples of non-ohmic behaviour.', 'Diode (V-I not linear, depends on sign of V); GaAs (negative resistance region); filament lamp at high current.', '2 marks.'),
])

c3s1_ar = pool_ar([
    ('The resistance of a wire increases on stretching it to a greater length.', 'Resistance R = ρL/A, and stretching increases L and decreases A.', 'a', 'R explains A.'),
    ('The drift velocity of electrons increases when the temperature of a metal is raised (same field).', 'Relaxation time decreases with temperature.', 'd', 'A is false: v_d = eEτ/m falls; R is true.'),
    ('Current density is a vector but current is a scalar.', 'Currents add algebraically, not by the parallelogram law.', 'a', 'R explains A.'),
    ('Semiconductors have a negative temperature coefficient of resistivity.', 'The number density of charge carriers in a semiconductor rises with temperature.', 'a', 'R explains A.'),
])


def c3s1_vd(r):
    I = r.choice([1, 1.5, 2, 3, 5])
    A = r.choice([1, 1.5, 2, 2.5]) * 1e-6
    n = 8.5e28
    vd = I / (n * QE * A)
    return NUM(f'A copper wire of cross-sectional area {g(A * 1e6)} mm² carries a current of {g(I)} A. Find the drift speed of the electrons. (n = 8.5 × 10²⁸ m⁻³, e = 1.6 × 10⁻¹⁹ C)', vd, 'm s⁻¹',
               f'v_d = I/(neA) = {g(I)}/(8.5 × 10²⁸ × 1.6 × 10⁻¹⁹ × {g(A)}) = {{ans}}.', wrongs=[I / (n * A), vd * 1000, I * n * QE * A])


def c3s1_R(r):
    rho, mat = r.choice([(1.7e-8, 'copper'), (2.7e-8, 'aluminium'), (1e-6, 'nichrome'), (4.4e-7, 'manganin')])
    L = r.choice([1, 2, 5, 10, 20])
    A = r.choice([0.5, 1, 2]) * 1e-6
    R = rho * L / A
    return NUM(f'Find the resistance of a {mat} wire {L} m long with cross-sectional area {g(A * 1e6)} mm². (ρ = {g(rho)} Ω m)', R, 'Ω', f'R = ρL/A = {g(rho)} × {L}/{g(A)} = {{ans}}.', wrongs=[rho * A / L, rho * L / (A * 1e6), R * 2], gap='G3')


def c3s1_temp(r):
    R1 = r.choice([10, 20, 50, 100])
    T1 = r.choice([20, 27, 0])
    alpha = r.choice([4e-3, 4.3e-3, 1.7e-4, 3.9e-3])
    T2 = r.choice([100, 150, 200, 500])
    R2 = R1 * (1 + alpha * (T2 - T1))
    return NUM(f'A wire has a resistance of {R1} Ω at {T1} °C. Its temperature coefficient of resistance is {g(alpha)} °C⁻¹. Find its resistance at {T2} °C.', R2, 'Ω',
               f'R₂ = R₁[1 + α(T₂ − T₁)] = {R1}[1 + {g(alpha)} × {T2 - T1}] = {{ans}}.', wrongs=[R1 * alpha * (T2 - T1), R1 * (1 + alpha * T2), R1 * (1 - alpha * (T2 - T1))], n=4)


def c3s1_findT(r):
    R1 = r.choice([75, 80, 100, 120])
    T1 = 27
    alpha = r.choice([1.7e-4, 1.5e-4])
    R2 = R1 * r.choice([1.05, 1.07, 1.08, 1.1])
    T2 = T1 + (R2 / R1 - 1) / alpha
    return NUM(f'A heating element made of nichrome has resistance {g(R1)} Ω at {T1} °C. When it reaches its steady operating temperature, its resistance is {g(R2, 1)} Ω. Find that temperature. (α for nichrome = {g(alpha)} °C⁻¹)', T2, '°C',
               f'T₂ − T₁ = (R₂ − R₁)/(R₁α) (2) = {g(R2 - R1, 2)}/({g(R1)} × {g(alpha)}) = {sig(T2 - T1)} °C (2); T₂ = {{ans}} (1).', wrongs=[T2 - T1, (R2 - R1) / (R2 * alpha) + T1, T2 * 2], gap='G5')


def c3s1_stretch(r):
    n = r.choice([2, 3, 4, 1.5])
    R = r.choice([2, 4, 5, 10])
    return NUM(f'A wire of resistance {R} Ω is stretched uniformly to {g(n)} times its original length (volume unchanged). Find its new resistance.', R * n * n, 'Ω',
               f'Volume constant ⇒ A → A/{g(n)}; R ∝ L/A ⇒ R\' = n²R = {g(n * n)} × {R} = {{ans}}.', wrongs=[R * n, R / n, R * n ** 3])


def c3s1_mob(r):
    E_ = r.choice([1, 2, 5, 10])
    tau = r.choice([2, 2.5, 3, 4]) * 1e-14
    vd = QE * E_ * tau / ME
    mu = vd / E_
    return NUM2(f'In a metal the relaxation time of free electrons is {g(tau)} s. Find the drift speed when the electric field in the wire is {E_} V m⁻¹, and the mobility of the electrons.', (vd, mu), ('m s⁻¹', 'm² V⁻¹ s⁻¹'),
                f'v_d = eEτ/m = 1.6 × 10⁻¹⁹ × {E_} × {g(tau)}/(9.1 × 10⁻³¹) = {sig(vd)} m s⁻¹ (2); μ = v_d/E = eτ/m = {sig(mu)} m² V⁻¹ s⁻¹ (1).',
                wrongs=[(vd * 2, mu * 2), (QE * E_ / (ME * tau), mu), (vd, vd * E_)])


c3s1_derive = pool_txt([
    ('Derive the relation I = neAv_d between current and drift velocity.', 'I = neAv_d', 'Charge crossing area A in time t is neAv_d t (3); divide by t (2).'),
    ('Derive an expression for the resistivity of a metal in terms of number density and relaxation time, and hence explain Ohm\'s law.', 'ρ = m/(ne²τ)',
     'v_d = eEτ/m (2); j = nev_d = (ne²τ/m)E (2); hence j = σE, ρ = m/(ne²τ) (1).'),
])


# st2 power and combination of resistors

c3s2_tf = tf_mcq('electrical power and combination of resistors',
                 ['The power dissipated in a resistor is I²R.', 'In parallel, the equivalent resistance is less than the smallest resistance.', '1 kWh = 3.6 × 10⁶ J.',
                  'Household appliances are connected in parallel.'],
                 ['In series, the equivalent resistance is less than the smallest resistance.', '1 kWh = 3.6 × 10³ J.', 'Household appliances are connected in series.',
                  'Power transmission at high current reduces loss.'])

c3s2_explain = pool_txt([
    ('Why is electric power transmitted at high voltage?', 'For given P, high V means small current I = P/V, so the line loss I²R is small.', '2 marks.'),
    ('Two bulbs of 40 W and 100 W rated for 220 V are joined in series to 220 V. Which glows brighter? Why?', 'The 40 W bulb: it has larger R = V²/P, and in series the same current flows, so I²R is larger for it.', '2 marks.'),
    ('Why are household appliances connected in parallel?', 'Each gets the full supply voltage and can be switched independently; failure of one does not affect others.', '2 marks.'),
])

c3s2_ar = pool_ar([
    ('A 100 W, 220 V bulb has a smaller resistance than a 60 W, 220 V bulb.', 'R = V²/P.', 'a', 'R explains A.'),
    ('In a series circuit, the same current flows through each resistor.', 'Charge is conserved and there is only one path.', 'a', 'R explains A.'),
    ('The equivalent resistance of resistors in parallel is more than the largest of them.', '1/R = 1/R₁ + 1/R₂ + …', 'd', 'A is false: it is less than the smallest; R is true.'),
])


def c3s2_P(r):
    V = r.choice([220, 230, 12, 6])
    R = r.choice([2, 4, 6, 12, 24]) if V < 50 else r.choice([40, 50, 100, 400, 484])
    P = V * V / R
    return NUM(f'Find the power dissipated when a resistor of {R} Ω is connected across a {V} V supply.', P, 'W', f'P = V²/R = {V}²/{R} = {{ans}}.', wrongs=[V / R, V * R, V * V * R], gap='G3')


def c3s2_bill(r):
    who = name(r)
    P = r.choice([1000, 1500, 2000, 750])
    h = r.choice([1, 2, 3, 4])
    days = 30
    rate = r.choice([6, 6.5, 7, 7.5, 8])
    units = P / 1000 * h * days
    cost = units * rate
    return NUM(f'{who}\'s geyser is rated {P} W. It is used for {h} h a day for {days} days. Find the cost of the electricity at ₹{g(rate)} per unit (kWh).', cost, '',
               f'Energy = {g(P / 1000)} kW × {h * days} h = {g(units)} kWh (1); cost = {g(units)} × {g(rate)} = ₹{{ans}} (1).', wrongs=[units * rate / 30, P * h * days * rate, units], n=4)


def c3s2_mix(r):
    R1 = r.choice([2, 3, 4, 5])
    R2, R3 = r.choice([(6, 3), (4, 4), (12, 6), (10, 15), (6, 12)])
    V = r.choice([6, 9, 12, 24])
    Rp = R2 * R3 / (R2 + R3)
    Req = R1 + Rp
    I = V / Req
    I2 = I * R3 / (R2 + R3)
    return NUM2(f'A resistor R₁ = {R1} Ω is connected in series with a parallel combination of R₂ = {R2} Ω and R₃ = {R3} Ω, across a {V} V battery of negligible internal resistance. Find the current from the battery and the current through R₂.',
                (I, I2), ('A', 'A'), f'R₂ ∥ R₃ = {sig(Rp)} Ω; R_eq = {sig(Req)} Ω (1); I = V/R_eq = {sig(I)} A (1); I₂ = I R₃/(R₂ + R₃) = {sig(I2)} A (1).',
                wrongs=[(V / (R1 + R2 + R3), V / (R1 + R2 + R3)), (I, I - I2), (V / Rp, I2)])


def c3s2_bulbs(r):
    V = 220
    P1, P2 = r.choice([(40, 100), (60, 100), (25, 100), (40, 60)])
    R1, R2 = V * V / P1, V * V / P2
    I = V / (R1 + R2)
    p1, p2 = I * I * R1, I * I * R2
    return NUM2(f'Two bulbs rated {P1} W, 220 V and {P2} W, 220 V are connected in series across a 220 V supply. Find the power consumed by each. Which glows brighter?',
                (p1, p2), ('W', 'W'), f'R₁ = V²/P₁ = {sig(R1)} Ω, R₂ = {sig(R2)} Ω (1); I = 220/(R₁ + R₂) = {sig(I)} A (1); P₁ = I²R₁ = {sig(p1)} W, P₂ = I²R₂ = {sig(p2)} W (1): the {P1} W bulb glows brighter.',
                wrongs=[(float(P1), float(P2)), (p2, p1), (P1 / 2, P2 / 2)], gap='G5')


def c3s2_equal(r):
    n = r.choice([2, 3, 4, 5])
    R = r.choice([2, 4, 6, 10, 12])
    return NUM(f'{n} identical resistors of {R} Ω each are connected first in series and then in parallel. Find the ratio of the equivalent resistance in series to that in parallel.', n * n, '',
               f'R_s = {n}R, R_p = R/{n}; ratio = n² = {{ans}}.', wrongs=[n, n ** 3, 1 / n ** 2], n=2)


# st3 emf, internal resistance, cells

c3s3_terms = term_mcq([('emf of a cell', 'the potential difference between its terminals when no current is drawn'), ('internal resistance', 'the resistance offered by the electrolyte and electrodes of a cell'),
                       ('terminal voltage while discharging', 'V = ε − Ir'), ('terminal voltage while charging', 'V = ε + Ir'), ('cells in series', 'ε_eq = ε₁ + ε₂, r_eq = r₁ + r₂')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c3s3_tf = tf_mcq('cells, emf and internal resistance',
                 ['The terminal voltage of a cell is less than its emf when it supplies current.', 'Internal resistance of a cell increases as it ages.', 'Maximum current from a cell is ε/r.',
                  'For n identical cells in parallel, the internal resistance becomes r/n.'],
                 ['The terminal voltage of a discharging cell is greater than its emf.', 'Emf is a force measured in newton.', 'For cells in parallel, the emf adds.',
                  'A cell with large internal resistance is best for a car starter.'])

c3s3_explain = pool_txt([
    ('Why is the terminal voltage of a cell less than its emf when current is drawn?', 'Part of the emf drives current through the internal resistance: V = ε − Ir.', '2 marks.'),
    ('Why should a car battery have very low internal resistance?', 'The starter motor needs a very large current; I = ε/(R + r) is large only if r is small.', '2 marks.'),
    ('Under what condition is the current the same whether n identical cells are joined in series or in parallel?', 'When R = r: nε/(R + nr) = ε/(R + r/n) gives R = r.', '2 marks.'),
])

c3s3_ar = pool_ar([
    ('The terminal voltage of a cell can be greater than its emf.', 'While a cell is being charged, V = ε + Ir.', 'a', 'R explains A.'),
    ('A dry cell cannot provide a large current.', 'Its internal resistance is relatively high.', 'a', 'R explains A.'),
    ('The emf of a cell depends on the external resistance.', 'Terminal voltage depends on the current drawn.', 'd', 'A is false: emf depends on the electrodes and electrolyte; R is true.'),
])


def c3s3_terminal(r):
    e = r.choice([1.5, 2, 6, 9, 12])
    rr = r.choice([0.1, 0.2, 0.5, 1])
    R = r.choice([2, 4, 5, 10])
    I = e / (R + rr)
    return NUM2(f'A cell of emf {g(e)} V and internal resistance {g(rr)} Ω is connected to a resistor of {R} Ω. Find the current and the terminal voltage.', (I, I * R), ('A', 'V'),
                f'I = ε/(R + r) = {g(e)}/{g(R + rr)} = {sig(I)} A (1); V = IR = ε − Ir = {sig(I * R)} V (1).', wrongs=[(e / R, e), (I, e + I * rr), (e / rr, I * R)])


def c3s3_r(r):
    e = r.choice([1.5, 2, 6, 9])
    R = r.choice([2, 4, 5, 10])
    rr = r.choice([0.25, 0.5, 1, 2])
    V = e * R / (R + rr)
    return NUM(f'The emf of a cell is {g(e)} V. When it is connected to a {R} Ω resistor, the terminal voltage falls to {sig(V)} V. Find the internal resistance of the cell.', R * (e / float(sig(V)) - 1), 'Ω',
               f'r = R(ε/V − 1) = {R}({g(e)}/{sig(V)} − 1) = {{ans}}.', wrongs=[R * (float(sig(V)) / e), (e - float(sig(V))), R * e / float(sig(V))], n=2)


def c3s3_series(r):
    n = r.choice([2, 3, 4, 5, 6])
    e = r.choice([1.5, 2])
    rr = r.choice([0.2, 0.5, 1])
    R = r.choice([2, 5, 8, 10])
    par = r.random() < 0.5
    if par:
        I = e / (R + rr / n)
        return NUM(f'{n} identical cells, each of emf {g(e)} V and internal resistance {g(rr)} Ω, are connected in parallel, and the combination is connected to a {R} Ω resistor. Find the current in the resistor.', I, 'A',
                   f'Parallel: ε_eq = ε = {g(e)} V, r_eq = r/n = {sig(rr / n)} Ω (1); I = ε/(R + r/n) = {{ans}} (2).', wrongs=[n * e / (R + n * rr), n * e / (R + rr / n), e / (R + rr)])
    I = n * e / (R + n * rr)
    return NUM(f'{n} identical cells, each of emf {g(e)} V and internal resistance {g(rr)} Ω, are connected in series to a {R} Ω resistor. Find the current.', I, 'A',
               f'Series: ε_eq = nε = {g(n * e)} V, r_eq = nr = {g(n * rr)} Ω (1); I = nε/(R + nr) = {{ans}} (2).', wrongs=[n * e / R, e / (R + rr), n * e / (R + rr)])


def c3s3_two(r):
    e1, r1 = r.choice([(2, 1), (1.5, 0.5), (6, 2), (12, 1)])
    e2, r2 = r.choice([(1.5, 1), (2, 2), (4, 1), (9, 3)])
    R = r.choice([2, 4, 5, 10])
    eq = (e1 * r2 + e2 * r1) / (r1 + r2)
    req = r1 * r2 / (r1 + r2)
    I = eq / (R + req)
    return NUM2(f'Two cells of emf {g(e1)} V (internal resistance {g(r1)} Ω) and {g(e2)} V (internal resistance {g(r2)} Ω) are connected in parallel, positive to positive. A {R} Ω resistor is connected across them. Find the equivalent emf, the equivalent internal resistance and the current in the resistor.',
                (eq, req, I), ('V', 'Ω', 'A'), f'ε_eq = (ε₁r₂ + ε₂r₁)/(r₁ + r₂) = {sig(eq)} V (2); r_eq = r₁r₂/(r₁ + r₂) = {sig(req)} Ω (1); I = ε_eq/(R + r_eq) = {sig(I)} A (2).',
                wrongs=[(e1 + e2, r1 + r2, (e1 + e2) / (R + r1 + r2)), ((e1 + e2) / 2, req, (e1 + e2) / 2 / (R + req)), (eq, r1 + r2, eq / (R + r1 + r2))], gap='G5')


def c3s3_charge(r):
    e = r.choice([8, 10, 12])
    rr = r.choice([0.5, 1])
    Vs = r.choice([120, 220])
    I = r.choice([2, 4, 5])
    Rs = (Vs - e) / I - rr
    return NUM2(f'A storage battery of emf {e} V and internal resistance {g(rr)} Ω is being charged by a {Vs} V dc supply using a series resistor. What resistance is needed to give a charging current of {I} A? What is the terminal voltage of the battery during charging?',
                (Rs, e + I * rr), ('Ω', 'V'), f'I = (V_s − ε)/(R + r) (1) ⇒ R = ({Vs} − {e})/{I} − {g(rr)} = {sig(Rs)} Ω (1); V = ε + Ir = {sig(e + I * rr)} V (1).',
                wrongs=[((Vs + e) / I - rr, e - I * rr), (Vs / I, float(e)), ((Vs - e) / I, e + I * rr)])


def c3s3_maxP(r):
    e = r.choice([6, 9, 12, 24])
    rr = r.choice([0.5, 1, 2, 3])
    return NUM(f'A battery of emf {e} V and internal resistance {g(rr)} Ω is connected to an external resistor R. For what value of R is the power delivered to R maximum? Find this maximum power.', e * e / (4 * rr), 'W',
               f'P = ε²R/(R + r)² is maximum when dP/dR = 0, i.e. R = r = {g(rr)} Ω (3); P_max = ε²/4r = {{ans}} (2).', wrongs=[e * e / rr, e * e / (2 * rr), e * e / (8 * rr)], gap='G5')


def c3s3_case(r):
    e = r.choice([1.5, 2, 3, 6])
    rr = r.choice([0.5, 1, 1.5, 2])
    pts = [(i, e - i * rr) for i in (0.2, 0.4, 0.6)]
    return {'stem': (f'In an experiment, the terminal voltage V of a cell is measured for different currents I. The V-I graph is a straight line; two readings on it are '
                     f'(I = {g(pts[0][0])} A, V = {sig(pts[0][1])} V) and (I = {g(pts[2][0])} A, V = {sig(pts[2][1])} V).\n'
                     '(i) Write the equation of the line. (ii) Find the emf of the cell. (iii) Find its internal resistance. (iv) What is the maximum current the cell can supply?'),
            'answer': f'(i) V = ε − Ir (ii) {sig(e)} V (iii) {sig(rr)} Ω (iv) {sig(e / rr)} A',
            'key': '(i) V = ε − Ir (1). (ii) intercept on V-axis = ε (1). (iii) |slope| = r (1). (iv) short circuit: I = ε/r (1).'}


# st4 Kirchhoff and Wheatstone bridge

c3s4_terms = term_mcq([('junction rule', 'the sum of currents entering a junction equals the sum leaving it (conservation of charge)'),
                       ('loop rule', 'the algebraic sum of potential changes around any closed loop is zero (conservation of energy)'),
                       ('balanced Wheatstone bridge', 'P/Q = R/S, and no current flows through the galvanometer'),
                       ('metre bridge', 'a practical Wheatstone bridge using a 1 m uniform wire to find an unknown resistance')],
                      'Which statement describes the {a}?', 'Which term is: {b}?', '{a}: {b}.')

c3s4_tf = tf_mcq("Kirchhoff's rules and the Wheatstone bridge",
                 ['Kirchhoff\'s junction rule follows from conservation of charge.', 'Kirchhoff\'s loop rule follows from conservation of energy.',
                  'At balance, interchanging the cell and galvanometer keeps the bridge balanced.', 'A metre bridge is most sensitive when the balance point is near the middle.'],
                 ['Kirchhoff\'s junction rule follows from conservation of energy.', 'At balance, a current flows through the galvanometer.', 'A metre bridge is most sensitive when the balance point is near one end.',
                  'Kirchhoff\'s rules apply only to circuits with one battery.'])

c3s4_explain = pool_txt([
    ('Why is the metre bridge balance point preferably obtained near the middle of the wire?', 'End resistances and errors in reading the length then have the least percentage effect.', '2 marks.'),
    ('Why are connections in a metre bridge made with thick copper strips?', 'To make their resistance negligible so it does not add to the arms.', '2 marks.'),
    ('State Kirchhoff\'s two rules and the conservation law on which each is based.', 'Junction rule: ΣI = 0 (charge). Loop rule: ΣΔV = 0 (energy).', '1 + 1 marks.'),
])

c3s4_ar = pool_ar([
    ('In a balanced Wheatstone bridge, interchanging the galvanometer and the cell does not affect the balance.', 'The balance condition P/Q = R/S is unchanged on interchanging them.', 'a', 'R explains A.'),
    ('Kirchhoff\'s junction rule is a statement of conservation of charge.', 'Charge cannot accumulate at a junction in steady state.', 'a', 'R explains A.'),
    ('No current flows through the galvanometer of a balanced Wheatstone bridge.', 'At balance the two ends of the galvanometer are at the same potential.', 'a', 'R explains A.'),
    ('Kirchhoff\'s loop rule can be applied only to loops that contain a battery.', 'Kirchhoff\'s loop rule follows from conservation of energy.', 'd', 'A is false: it applies to any closed loop; R is true.'),
])


def c3s4_wb(r):
    P = r.choice([10, 20, 50, 100])
    Q = r.choice([10, 20, 40, 100])
    R = r.choice([5, 8, 12, 15, 30])
    S = Q * R / P
    return NUM(f'In a Wheatstone bridge, P = {P} Ω, Q = {Q} Ω and R = {R} Ω. What value of S balances the bridge?', S, 'Ω', f'P/Q = R/S ⇒ S = QR/P = {Q} × {R}/{P} = {{ans}}.', wrongs=[P * R / Q, P * Q / R, R], gap='G3')


def c3s4_metre(r):
    R = r.choice([2, 3, 4, 5, 10])
    l = r.choice([30, 35, 40, 45, 55, 60, 62.5])
    X = R * (100 - l) / l
    return NUM(f'In a metre bridge experiment, a known resistance of {R} Ω is in the left gap and the unknown resistance X in the right gap. The balance point is at {g(l)} cm from the left end. Find X.', X, 'Ω',
               f'R/X = l/(100 − l) ⇒ X = R(100 − l)/l = {R} × {g(100 - l)}/{g(l)} = {{ans}}.', wrongs=[R * l / (100 - l), R * (100 - l) / 100, R * l / 100])


def c3s4_shift(r):
    R = r.choice([2, 4, 5, 10])
    l = r.choice([20, 25, 30, 40])
    X = R * l / (100 - l)
    return NUM(f'In a metre bridge with X in the left gap and a standard {R} Ω in the right gap, the balance point is at {l} cm from the left end. When X and the {R} Ω resistor are interchanged, where is the new balance point? Find X.',
               X, 'Ω', f'X/{R} = {l}/{100 - l} ⇒ X = {{ans}} (2); on interchanging, balance length = {100 - l} cm (1).', wrongs=[R * (100 - l) / l, R * l / 100, float(R)], gap='G5')


def c3s4_loop(r):
    e1 = r.choice([2, 4, 6, 10, 12])
    e2 = r.choice([1, 2, 3, 4, 6])
    R1 = r.choice([1, 2, 4])
    R2 = r.choice([1, 2, 3])
    R3 = r.choice([2, 4, 6])
    # loop 1: e1 = I1 R1 + I3 R3, loop 2: e2 = I2 R2 + I3 R3, I3 = I1 + I2
    a11, a12, b1 = R1 + R3, R3, e1
    a21, a22, b2 = R3, R2 + R3, e2
    det = a11 * a22 - a12 * a21
    I1 = (b1 * a22 - a12 * b2) / det
    I2 = (a11 * b2 - a21 * b1) / det
    I3 = I1 + I2
    return NUM2(f'Two batteries of emf ε₁ = {e1} V and ε₂ = {e2} V (negligible internal resistance) are connected with resistors R₁ = {R1} Ω and R₂ = {R2} Ω in their branches, and both feed a common resistor R₃ = {R3} Ω '
                f'(the positive terminals of both batteries are joined through their resistors to the same end of R₃). Using Kirchhoff\'s rules, find the currents I₁ through R₁, I₂ through R₂, and I₃ through R₃.',
                (I1, I2, I3), ('A', 'A', 'A'), f'Junction: I₃ = I₁ + I₂ (1). Loop 1: {e1} = {R1}I₁ + {R3}I₃ (1). Loop 2: {e2} = {R2}I₂ + {R3}I₃ (1). Solving: I₁ = {sig(I1)} A, I₂ = {sig(I2)} A, I₃ = {sig(I3)} A (2). (A negative value means the current flows opposite to the assumed direction.)',
                wrongs=[(e1 / (R1 + R3), e2 / (R2 + R3), e1 / (R1 + R3) + e2 / (R2 + R3)), (I2, I1, I3), (I1, I2, I1 - I2)], gap='G5')


def c3s4_junction(r):
    ins = r.sample([1, 2, 3, 4, 5, 6], 2)
    out = r.choice([1, 2])
    x = sum(ins) - out
    if x <= 0:
        raise ValueError
    return NUM(f'At a junction, currents of {ins[0]} A and {ins[1]} A flow in, and a current of {out} A flows out along one wire. What current flows out along the only other wire?', x, 'A',
               f'Junction rule: {ins[0]} + {ins[1]} = {out} + I ⇒ I = {{ans}}.', wrongs=[sum(ins) + out, out - sum(ins) + 2 * sum(ins) + 1, float(sum(ins))], n=2)


c3s4_derive = pool_txt([
    ('Using Kirchhoff\'s rules, derive the balance condition of a Wheatstone bridge.', 'P/Q = R/S', 'Circuit and currents (1); I_g = 0 at balance (1); loop equations (2); ratio (1).'),
    ('Describe how a metre bridge is used to find an unknown resistance, with the formula and two precautions.', 'X = R(100 − l)/l', 'Circuit (2); formula (1); precautions: balance near middle, tight connections, current only while reading (2).'),
])


def c3s4_case(r):
    who = name(r)
    R = r.choice([2, 4, 5, 10])
    l = r.choice([40, 45, 55, 60])
    X = R * (100 - l) / l
    L, d = r.choice([(1, 0.4), (0.5, 0.3), (1.5, 0.5)])
    rho = X * math.pi * (d / 2000) ** 2 / L
    return {'stem': (f'{who} uses a metre bridge to find the resistivity of a wire. With a {R} Ω standard resistor in the left gap and {g(L * 100)} cm of the wire in the right gap, the null point is at {l} cm from the left end. '
                     f'The wire\'s diameter is {g(d)} mm.\n(i) Find the resistance of the wire. (ii) Find its resistivity. (iii) Why is the null point preferred near the middle? (iv) What happens to the balance point if the wire is heated?'),
            'answer': f'(i) {sig(X)} Ω (ii) {sig(rho)} Ω m (iii) to reduce the effect of end errors (iv) it shifts towards the left (X increases)',
            'key': '(i) X = R(100 − l)/l (1). (ii) ρ = XA/L with A = πd²/4 (1). (iii) end errors (1). (iv) X increases with temperature so l decreases (1).'}


# ======================================================== ch04 Moving Charges and Magnetism
# st1 Lorentz force and motion in B

c4s1_terms = term_mcq([('Lorentz force', 'F = q[E + v × B]'), ('magnetic force on a moving charge', 'qv × B, perpendicular to both v and B'),
                       ('radius of circular path in B', 'r = mv/(qB)'), ('cyclotron frequency', 'ν = qB/(2πm), independent of speed'),
                       ('velocity selector', 'crossed E and B fields that let through only particles with v = E/B')],
                      'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c4s1_tf = tf_mcq('the force on a moving charge in a magnetic field',
                 ['A magnetic field does no work on a moving charge.', 'The magnetic force is zero when v is parallel to B.', 'A charge moving perpendicular to a uniform B describes a circle.',
                  'The SI unit of B is tesla (1 T = 1 N A⁻¹ m⁻¹).', 'The period of circular motion in B does not depend on the speed.'],
                 ['A magnetic field changes the speed of a moving charge.', 'The magnetic force is maximum when v is parallel to B.', 'A charge at rest experiences a magnetic force.',
                  'The radius of the circular path is independent of the speed.', 'The magnetic force is along the direction of B.'])

c4s1_explain = pool_txt([
    ('Why does a magnetic field not change the kinetic energy of a moving charged particle?', 'The force qv × B is always perpendicular to v, so it does no work; only the direction changes.', '2 marks.'),
    ('A charged particle enters a uniform magnetic field at an angle θ (not 0° or 90°). Describe its path.', 'A helix: v cos θ along B is unchanged, v sin θ gives circular motion.', '2 marks.'),
    ('An electron and a proton enter a uniform magnetic field with the same velocity perpendicular to B. Compare their paths.', 'They curve in opposite senses; the electron\'s radius is much smaller since r = mv/qB.', '2 marks.'),
])

c4s1_ar = pool_ar([
    ('The kinetic energy of a charged particle moving in a magnetic field remains constant.', 'The magnetic force is always perpendicular to the velocity.', 'a', 'R explains A.'),
    ('The time period of a charged particle in a cyclotron is independent of its speed.', 'r = mv/qB grows in proportion to v.', 'a', 'T = 2πr/v = 2πm/qB; R explains A.'),
    ('A charge moving along the direction of a magnetic field is deflected.', 'F = qvB sin θ.', 'd', 'A is false: sin 0° = 0; R is true.'),
])


def c4s1_F(r):
    q, nm = r.choice([(QE, 'proton'), (QE, 'electron'), (2 * QE, 'alpha particle')])
    v = r.choice([1, 2, 3, 5]) * 1e6
    B = r.choice([0.1, 0.2, 0.5, 1, 1.5])
    th = r.choice([30, 60, 90])
    Fv = q * v * B * math.sin(math.radians(th))
    return NUM(f'A{"n" if nm[0] in "aeiou" else ""} {nm} moves with speed {g(v)} m s⁻¹ at {th}° to a uniform magnetic field of {g(B)} T. Find the magnitude of the magnetic force on it. (e = 1.6 × 10⁻¹⁹ C)', Fv, 'N',
               f'F = qvB sin θ = {g(q)} × {g(v)} × {g(B)} × sin {th}° = {{ans}}.', wrongs=[q * v * B * math.cos(math.radians(th)) or Fv * 2, q * v * B, Fv / 2], gap='G3')


def c4s1_radius(r):
    nm, m, q = r.choice([('an electron', ME, QE), ('a proton', MP, QE)])
    v = r.choice([1, 2, 3, 4]) * (1e6 if m == MP else 1e7)
    B = r.choice([0.01, 0.05, 0.1, 0.5]) if m == ME else r.choice([0.1, 0.5, 1])
    rad = m * v / (q * B)
    return NUM(f'Find the radius of the circular path of {nm} moving at {g(v)} m s⁻¹ perpendicular to a uniform magnetic field of {g(B)} T. (e = 1.6 × 10⁻¹⁹ C, mₑ = 9.1 × 10⁻³¹ kg, m_p = 1.67 × 10⁻²⁷ kg)', rad, 'm',
               f'qvB = mv²/r ⇒ r = mv/(qB) = {g(m)} × {g(v)}/({g(q)} × {g(B)}) = {{ans}}.', wrongs=[q * B / (m * v), m * v * v / (q * B), rad * 2])


def c4s1_freq(r):
    B = r.choice([0.5, 1, 1.5, 2])
    nm, m, q = r.choice([('a proton', MP, QE), ('a deuteron', 2 * MP, QE), ('an alpha particle', 4 * MP, 2 * QE)])
    nu = q * B / (2 * math.pi * m)
    return NUM(f'Find the frequency of revolution (cyclotron frequency) of {nm} in a uniform magnetic field of {g(B)} T. (m_p = 1.67 × 10⁻²⁷ kg, e = 1.6 × 10⁻¹⁹ C)', nu, 'Hz',
               f'ν = qB/(2πm) = {g(q)} × {g(B)}/(2π × {g(m)}) = {{ans}}; independent of speed.', wrongs=[q * B / m, 2 * math.pi * m / (q * B), nu * 2])


def c4s1_helix(r):
    v = r.choice([2, 3, 4, 5]) * 1e6
    B = r.choice([0.01, 0.02, 0.05])
    th = r.choice([30, 45, 60])
    vp = v * math.sin(math.radians(th))
    vl = v * math.cos(math.radians(th))
    rad = ME * vp / (QE * B)
    T = 2 * math.pi * ME / (QE * B)
    pitch = vl * T
    return NUM2(f'An electron moving at {g(v)} m s⁻¹ enters a uniform magnetic field of {g(B)} T at {th}° to the field. Find the radius and the pitch of its helical path. (mₑ = 9.1 × 10⁻³¹ kg, e = 1.6 × 10⁻¹⁹ C)', (rad, pitch), ('m', 'm'),
                f'v⊥ = v sin θ = {sig(vp)} m s⁻¹, v∥ = v cos θ = {sig(vl)} m s⁻¹ (1); r = mv⊥/(eB) = {sig(rad)} m (1); T = 2πm/(eB) = {sig(T)} s (1); pitch = v∥T = {sig(pitch)} m (1).',
                wrongs=[(ME * v / (QE * B), v * T), (ME * vl / (QE * B), vp * T), (rad, 2 * math.pi * rad)], gap='G5')


def c4s1_accel(r):
    V = r.choice([100, 500, 1000, 2000])
    B = r.choice([1, 2, 5]) * 1e-3
    v = math.sqrt(2 * QE * V / ME)
    rad = ME * v / (QE * B)
    return NUM2(f'An electron, starting from rest, is accelerated through {V} V and then enters a uniform magnetic field of {g(B)} T perpendicular to its velocity. Find its speed and the radius of its path.', (v, rad), ('m s⁻¹', 'm'),
                f'½mv² = eV ⇒ v = √(2eV/m) = {sig(v)} m s⁻¹ (1.5); r = mv/(eB) = {sig(rad)} m (1.5).', wrongs=[(math.sqrt(QE * V / ME), rad / math.sqrt(2)), (v, rad * 2), (2 * QE * V / ME, rad)])


def c4s1_selector(r):
    Ev = r.choice([1, 2, 3, 5]) * 1e4
    B = r.choice([0.01, 0.02, 0.05, 0.1])
    v = Ev / B
    return NUM(f'In a velocity selector, a uniform electric field of {g(Ev)} V m⁻¹ and a uniform magnetic field of {g(B)} T are perpendicular to each other and to the beam. Charged particles of what speed pass undeflected? Does it depend on their charge or mass?', v, 'm s⁻¹',
               f'qE = qvB ⇒ v = E/B = {g(Ev)}/{g(B)} = {{ans}} (2); independent of q and m (1).', wrongs=[Ev * B, B / Ev, v * 2], gap='G5')


# st2 Biot-Savart; field on axis of loop

c4s2_terms = term_mcq([('Biot-Savart law', 'dB = (μ₀/4π) I dl sin θ/r²'), ('field at the centre of a circular loop of N turns', 'μ₀NI/(2R)'),
                       ('field on the axis of a circular loop', 'μ₀IR²/[2(x² + R²)^(3/2)]'), ('μ₀ (permeability of free space)', '4π × 10⁻⁷ T m A⁻¹'),
                       ('field at the centre of a semicircular arc', 'μ₀I/(4R)')],
                      'Which of the following gives the {a}?', 'Which expression or term is {b}?', '{a}: {b}.')

c4s2_tf = tf_mcq('the Biot-Savart law',
                 ['The field due to a current element is zero along the line of the element.', 'The field of a current element falls off as 1/r².', 'The field at the centre of a loop is perpendicular to the plane of the loop.',
                  'The direction of dB is given by the vector product dl × r.'],
                 ['The field due to a current element is maximum along the element.', 'The field of a current element falls off as 1/r.', 'The field at the centre of a loop lies in the plane of the loop.',
                  'The Biot-Savart law applies only to straight wires.'])

c4s2_explain = pool_txt([
    ('State the right-hand thumb rule for the direction of the field of a circular loop.', 'Curl the fingers along the current; the thumb gives the field direction at the centre (along the axis).', '2 marks.'),
    ('Compare the Biot-Savart law with Coulomb\'s law.', 'Both are inverse-square and long range; Biot-Savart source is a vector element I dl, field depends on angle sin θ; Coulomb source is a scalar charge.', '2 marks.'),
    ('How does the field at the centre of a circular coil change if the current is doubled and the radius halved?', 'B = μ₀NI/2R becomes 4 times.', '2 marks.'),
])

c4s2_ar = pool_ar([
    ('There is no magnetic field at a point on the line of a straight current element.', 'dB ∝ sin θ, and θ = 0 along the element.', 'a', 'R explains A.'),
    ('The field on the axis of a loop decreases with distance from the centre.', 'B = μ₀IR²/[2(x² + R²)^(3/2)].', 'a', 'R explains A.'),
    ('The field at the centre of a circular loop lies in the plane of the loop.', 'Every current element is perpendicular to the radius drawn to it.', 'd', 'A is false: dl × r is perpendicular to the plane; R is true.'),
])


def c4s2_centre(r):
    N = r.choice([1, 10, 50, 100, 200])
    I = r.choice([0.5, 1, 2, 5])
    R = r.choice([5, 8, 10, 15, 20])
    B = MU0 * N * I / (2 * R / 100)
    return NUM(f'A circular coil of {N} turn{"s" if N > 1 else ""} and radius {R} cm carries a current of {g(I)} A. Find the magnetic field at its centre. (μ₀ = 4π × 10⁻⁷ T m A⁻¹)', B, 'T',
               f'B = μ₀NI/(2R) = 4π × 10⁻⁷ × {N} × {g(I)}/(2 × {g(R / 100)}) = {{ans}}.', wrongs=[MU0 * N * I / (2 * math.pi * R / 100), MU0 * N * I / (R / 100), B * 100], gap='G3')


def c4s2_axis(r):
    N = r.choice([10, 50, 100])
    I = r.choice([1, 2, 5])
    R = r.choice([3, 4, 5, 6, 10])
    x = r.choice([3, 4, 5, 8, 10])
    B = MU0 * N * I * (R / 100) ** 2 / (2 * ((x / 100) ** 2 + (R / 100) ** 2) ** 1.5)
    return NUM(f'A circular coil of {N} turns and radius {R} cm carries a current of {I} A. Find the magnetic field on its axis at a distance of {x} cm from the centre.', B, 'T',
               f'B = μ₀NIR²/[2(x² + R²)^(3/2)] = 4π × 10⁻⁷ × {N} × {I} × ({g(R / 100)})²/[2(({g(x / 100)})² + ({g(R / 100)})²)^(3/2)] = {{ans}}.',
               wrongs=[MU0 * N * I / (2 * R / 100), MU0 * N * I * (R / 100) ** 2 / (2 * (x / 100) ** 3), B * 2])


def c4s2_element(r):
    I = r.choice([1, 2, 5, 10])
    dl = r.choice([1, 2, 5])
    d = r.choice([0.5, 1, 2])
    th = r.choice([30, 45, 60, 90])
    B = 1e-7 * I * dl / 100 * math.sin(math.radians(th)) / d ** 2
    return NUM(f'A small element of length {dl} cm of a wire carries a current of {I} A along the x-axis. Find the magnitude of the field it produces at a point {g(d)} m away, in a direction making {th}° with the x-axis.', B, 'T',
               f'dB = (μ₀/4π) I dl sin θ/r² = 10⁻⁷ × {I} × {g(dl / 100)} × sin {th}°/{g(d)}² = {{ans}}.', wrongs=[1e-7 * I * dl / 100 * math.cos(math.radians(th)) / d ** 2 or B * 2, 1e-7 * I * dl / 100 / d, B * 4 * math.pi])


def c4s2_ratio(r):
    k = r.choice([1, 2, 3])
    t = {1: 'x = R', 2: 'x = 2R', 3: 'x = √3 R'}[k]
    xr = {1: 1, 2: 2, 3: math.sqrt(3)}[k]
    f = (1 + xr * xr) ** 1.5
    return NUM(f'Find the ratio of the magnetic field at the centre of a current-carrying circular loop to the field on its axis at a distance {t} from the centre.', f, '',
               f'B_centre/B_axis = (x² + R²)^(3/2)/R³ = (1 + {g(xr * xr)})^(3/2) = {{ans}}.', wrongs=[1 + xr * xr, 1 / f, (1 + xr * xr) ** 2], gap='G5')


def c4s2_semi(r):
    I = r.choice([2, 5, 10])
    R = r.choice([2, 5, 10])
    frac = r.choice([('a semicircular arc', 0.5), ('a quarter-circle arc', 0.25), ('three-quarters of a circle', 0.75)])
    B = frac[1] * MU0 * I / (2 * R / 100)
    return NUM(f'A wire carrying {I} A is bent into {frac[0]} of radius {R} cm; the straight lead-in wires are radial, so they contribute nothing at the centre. Find the field at the centre.', B, 'T',
               f'An arc of fraction f of a circle gives B = f μ₀I/(2R) (3) = {g(frac[1])} × 4π × 10⁻⁷ × {I}/(2 × {g(R / 100)}) = {{ans}} (2).', wrongs=[MU0 * I / (2 * R / 100), B * 2, MU0 * I / (2 * math.pi * R / 100)], gap='G5')


c4s2_derive = pool_txt([
    ('Using the Biot-Savart law, derive the field on the axis of a circular current loop.', 'B = μ₀IR²/[2(x² + R²)^(3/2)]', 'dB for element (1); components ⟂ axis cancel (1); integrate axial parts (2); result and centre value (1).'),
    ('State the Biot-Savart law in vector form and use it to find the field at the centre of a circular loop.', 'dB = (μ₀/4π) I dl × r/r³; B = μ₀I/(2R)', 'Statement (2); all elements give dB along the axis, sum (2); result (1).'),
])


# st3 Ampere's circuital law

c4s3_terms = term_mcq([('Ampere\'s circuital law', '∮B·dl = μ₀I_enclosed'), ('field of a long straight wire', 'μ₀I/(2πr)'), ('field inside a long solenoid', 'μ₀nI, uniform along the axis'),
                       ('field inside a toroid', 'μ₀NI/(2πr)'), ('field outside an ideal solenoid', 'approximately zero')],
                      'Which of the following gives {a}?', 'Which result is {b}?', '{a}: {b}.')

c4s3_tf = tf_mcq("Ampere's circuital law",
                 ['The field lines of a long straight wire are concentric circles.', 'The field inside a long solenoid is uniform.', 'The field in the open space inside a toroid is zero.',
                  'Ampere\'s law is useful when there is symmetry.'],
                 ['The field of a long straight wire is radial.', 'The field inside a long solenoid is zero.', 'The field of a long straight wire varies as 1/r².',
                  'Ampere\'s law holds only for circular loops.'])

c4s3_explain = pool_txt([
    ('Why is the field inside a long solenoid uniform and that outside nearly zero?', 'Fields of adjacent turns add inside and cancel outside; the lines spread over a huge area outside.', '2 marks.'),
    ('How does the field of a long straight wire vary with distance? Draw the field lines.', 'B = μ₀I/2πr, so B ∝ 1/r; lines are concentric circles.', '2 marks.'),
    ('Why does a toroid have no field outside it?', 'An Amperian loop outside encloses equal currents in opposite directions; net enclosed current is zero.', '2 marks.'),
])

c4s3_ar = pool_ar([
    ('The field inside a long solenoid is independent of its radius.', 'B = μ₀nI depends only on turns per unit length and current.', 'a', 'R explains A.'),
    ('The field outside an ideal toroid is zero.', 'The net current enclosed by an Amperian loop outside is zero.', 'a', 'R explains A.'),
    ('The field of a straight wire is the same at all distances.', 'Ampere\'s law gives B·2πr = μ₀I.', 'd', 'A is false: B ∝ 1/r; R is true.'),
])


def c4s3_wire(r):
    I = r.choice([1, 2, 5, 10, 20, 35])
    d = r.choice([1, 2, 5, 10, 20])
    B = MU0 * I / (2 * math.pi * d / 100)
    return NUM(f'A long straight wire carries a current of {I} A. Find the magnitude of the magnetic field at a point {d} cm from it.', B, 'T',
               f'B = μ₀I/(2πr) = 4π × 10⁻⁷ × {I}/(2π × {g(d / 100)}) = {{ans}}.', wrongs=[MU0 * I / (2 * d / 100), MU0 * I / (4 * math.pi * (d / 100) ** 2), B * 10], gap='G3')


def c4s3_sol(r):
    N = r.choice([200, 500, 1000, 1500])
    L = r.choice([20, 40, 50, 80, 100])
    I = r.choice([0.5, 1, 2, 4])
    B = MU0 * N / (L / 100) * I
    return NUM(f'A solenoid of length {L} cm has {N} turns and carries a current of {g(I)} A. Find the magnetic field inside it, near the centre.', B, 'T',
               f'n = N/L = {g(N / (L / 100))} m⁻¹; B = μ₀nI = {{ans}}.', wrongs=[MU0 * N * I, MU0 * N * I / (2 * L / 100), B / 2])


def c4s3_toroid(r):
    N = r.choice([500, 1000, 3500])
    I = r.choice([0.5, 1, 11, 2])
    rr = r.choice([10, 15, 20, 25])
    B = MU0 * N * I / (2 * math.pi * rr / 100)
    return NUM(f'A toroid has a core of mean radius {rr} cm wound with {N} turns carrying {g(I)} A. Find the field inside the core (along the mean circle).', B, 'T',
               f'B = μ₀NI/(2πr) = 4π × 10⁻⁷ × {N} × {g(I)}/(2π × {g(rr / 100)}) = {{ans}}.', wrongs=[MU0 * N * I / (rr / 100), MU0 * N * I, B * 2])


def c4s3_two(r):
    I1 = r.choice([2, 4, 5, 10])
    I2 = r.choice([2, 3, 6, 8, 10])
    d = r.choice([10, 20, 40])
    same = r.random() < 0.5
    B1 = MU0 * I1 / (2 * math.pi * d / 200)
    B2 = MU0 * I2 / (2 * math.pi * d / 200)
    B = abs(B1 - B2) if same else B1 + B2
    if B == 0:
        return {'stem': f'Two long parallel wires {d} cm apart carry currents of {I1} A and {I2} A in the same direction. Find the magnetic field at the point midway between them.', 'answer': '0 T',
                'key': 'The two fields at the midpoint are equal and opposite (equal currents, same direction), so B = 0.',
                'distractors': [f'{sig(2 * B1)} T', f'{sig(B1)} T', f'{sig(B1 / 2)} T']}
    return NUM(f'Two long parallel wires {d} cm apart carry currents of {I1} A and {I2} A in {"the same direction" if same else "opposite directions"}. Find the magnitude of the magnetic field at the point midway between them.', B, 'T',
               f'Each wire is {g(d / 200)} m from the midpoint: B₁ = {sig(B1)} T, B₂ = {sig(B2)} T (1); {"same-direction currents give opposite fields there" if same else "opposite currents give fields in the same direction there"} (1); B = {{ans}} (1).',
               wrongs=[B1 + B2 if same else abs(B1 - B2) or B * 2, B1, B / 2], gap='G5')


def c4s3_inside(r):
    I = r.choice([5, 10, 20])
    R = r.choice([2, 4, 5])
    rr = r.choice([1, 2]) * R / 4
    B = MU0 * I * (rr / 100) / (2 * math.pi * (R / 100) ** 2)
    return NUM(f'A long straight solid cylindrical wire of radius {R} mm carries a steady current of {I} A distributed uniformly over its cross-section. Using Ampere\'s law, find the field at a distance {g(rr)} mm from the axis.',
               B, 'T', f'Current enclosed I r²/R² (2); B·2πr = μ₀I r²/R² ⇒ B = μ₀Ir/(2πR²) (2) = {{ans}} (1).',
               wrongs=[MU0 * I / (2 * math.pi * rr / 1000), MU0 * I / (2 * math.pi * R / 1000), B * 2], gap='G5')


c4s3_derive = pool_txt([
    ('Using Ampere\'s circuital law, derive an expression for the magnetic field inside a long solenoid.', 'B = μ₀nI', 'Rectangular Amperian loop (1); only inside side contributes (2); BL = μ₀nLI (1); result (1).'),
    ('State Ampere\'s circuital law and use it to find the field of a long straight current-carrying wire.', '∮B·dl = μ₀I; B = μ₀I/(2πr)', 'Statement (2); circular loop, B constant and tangential (2); result (1).'),
    ('Using Ampere\'s law, find the field inside and outside a toroid.', 'Inside: μ₀NI/(2πr); outside and in the open space: zero', 'Three circular loops (3); results (2).'),
])


def c4s3_case(r):
    who = name(r)
    N = r.choice([500, 800, 1000])
    L = r.choice([40, 50, 80])
    I = r.choice([1, 2, 3])
    B = MU0 * N / (L / 100) * I
    return {'stem': (f'For a school project, {who} winds a solenoid of length {L} cm with {N} turns of insulated copper wire and passes a current of {I} A through it.\n'
                     '(i) Find the magnetic field near the centre inside the solenoid. (ii) How does the field near an end compare with that at the centre? (iii) What happens to the field if a soft iron core is inserted? (iv) How should the current be changed to double the field without changing the coil?'),
            'answer': f'(i) {sig(B)} T (ii) about half (iii) it increases greatly (by the relative permeability) (iv) double the current',
            'key': '(i) B = μ₀nI (1). (ii) μ₀nI/2 at the ends (1). (iii) B = μ₀μᵣnI (1). (iv) B ∝ I (1).'}


# st4 force between currents, torque on loop, galvanometer

c4s4_terms = term_mcq([('ampere (definition)', 'the current which, in two long parallel wires 1 m apart in vacuum, produces a force of 2 × 10⁻⁷ N per metre'),
                       ('magnetic moment of a current loop', 'm = NIA, perpendicular to the plane of the loop'), ('torque on a current loop', 'τ = m × B'),
                       ('current sensitivity of a galvanometer', 'φ/I = NAB/k'), ('voltage sensitivity of a galvanometer', 'φ/V = NAB/(kR_G)')],
                      'Which of the following defines {a}?', 'Which term is {b}?', '{a}: {b}.')

c4s4_tf = tf_mcq('forces and torques on currents',
                 ['Parallel currents in the same direction attract.', 'The torque on a current loop is maximum when its plane is parallel to B.', 'A radial magnetic field is used in a moving coil galvanometer.',
                  'An ammeter is made by connecting a low shunt resistance in parallel with a galvanometer.', 'A voltmeter has very high resistance.'],
                 ['Parallel currents in the same direction repel.', 'The torque on a current loop is maximum when its plane is perpendicular to B.', 'An ammeter is a galvanometer with a high resistance in series.',
                  'An ideal ammeter has infinite resistance.', 'A uniform field is used in a galvanometer to make the scale non-linear.'])

c4s4_explain = pool_txt([
    ('Why is the field made radial in a moving coil galvanometer?', 'The plane of the coil is always parallel to B, so torque NIAB does not depend on deflection, giving a linear scale.', '2 marks.'),
    ('Why does increasing current sensitivity not necessarily increase voltage sensitivity?', 'If N is doubled, current sensitivity doubles but resistance also doubles, so voltage sensitivity (NAB/kR) is unchanged.', '2 marks.'),
    ('Why should an ammeter have low resistance and a voltmeter high resistance?', 'The ammeter is in series and must not change the current; the voltmeter is in parallel and must draw negligible current.', '2 marks.'),
])

c4s4_ar = pool_ar([
    ('Two parallel wires carrying currents in the same direction attract each other.', 'Each wire lies in the magnetic field of the other, and the force is towards the other wire.', 'a', 'R explains A.'),
    ('A galvanometer is converted into an ammeter by connecting a low resistance in parallel.', 'Most of the current then bypasses the galvanometer.', 'a', 'R explains A.'),
    ('The torque on a current loop in a uniform field is zero when the plane of the loop is perpendicular to B.', 'τ = mB sin θ, where θ is the angle between m and B.', 'a', 'm ∥ B, θ = 0; R explains A.'),
    ('A galvanometer can be used directly as an ammeter for large currents.', 'A galvanometer gives full-scale deflection for very small currents.', 'd', 'A is false; R is true.'),
])


def c4s4_force(r):
    I1 = r.choice([2, 5, 10, 20])
    I2 = r.choice([3, 5, 10, 15])
    d = r.choice([2, 4, 5, 10])
    L = r.choice([1, 2, 5])
    f = MU0 * I1 * I2 / (2 * math.pi * d / 100) * L
    return NUM(f'Two long parallel wires {d} cm apart carry currents of {I1} A and {I2} A in the same direction. Find the force on a {L} m length of either wire. Is it attractive or repulsive?', f, 'N',
               f'F = μ₀I₁I₂L/(2πd) = 2 × 10⁻⁷ × {I1} × {I2} × {L}/{g(d / 100)} = {{ans}}, attractive.', wrongs=[MU0 * I1 * I2 * L / (d / 100), f * 2, f / L if L > 1 else f * 10])


def c4s4_torque(r):
    N = r.choice([10, 20, 50, 100])
    a = r.choice([5, 10, 2])
    b = r.choice([5, 8, 10])
    I = r.choice([0.5, 1, 2])
    B = r.choice([0.1, 0.2, 0.5])
    th = r.choice([30, 60, 90])
    t = N * I * a * b * 1e-4 * B * math.sin(math.radians(th))
    return NUM(f'A rectangular coil of {N} turns, {a} cm × {b} cm, carries a current of {g(I)} A and is placed in a uniform field of {g(B)} T, with the normal to its plane at {th}° to the field. Find the torque on the coil.', t, 'N m',
               f'm = NIA = {N} × {g(I)} × {g(a * b * 1e-4)} = {sig(N * I * a * b * 1e-4)} A m² (1); τ = mB sin θ = {{ans}} (2).', wrongs=[N * I * a * b * 1e-4 * B * math.cos(math.radians(th)) or t * 2, N * I * a * b * B, t / N])


def c4s4_ammeter(r):
    G_ = r.choice([10, 12, 20, 25, 50])
    Ig = r.choice([1, 2, 4, 5]) * 1e-3
    I = r.choice([1, 2, 5, 10])
    Sh = Ig * G_ / (I - Ig)
    return NUM(f'A galvanometer of resistance {G_} Ω gives full-scale deflection for {g(Ig * 1000)} mA. How can it be converted into an ammeter of range 0-{I} A?', Sh, 'Ω',
               f'Shunt S = I_gG/(I − I_g) (2) = {g(Ig)} × {G_}/({I} − {g(Ig)}) = {{ans}} (1), connected in parallel.', wrongs=[I * G_ / Ig, Ig * G_ / I * 1000, G_ * (I / Ig - 1)], gap='G3')


def c4s4_voltmeter(r):
    G_ = r.choice([10, 15, 20, 50])
    Ig = r.choice([1, 2, 5]) * 1e-3
    V = r.choice([5, 10, 15, 20, 50])
    R = V / Ig - G_
    return NUM(f'A galvanometer of resistance {G_} Ω gives full-scale deflection for {g(Ig * 1000)} mA. How can it be converted into a voltmeter of range 0-{V} V?', R, 'Ω',
               f'R = V/I_g − G (2) = {V}/{g(Ig)} − {G_} = {{ans}} (1), connected in series.', wrongs=[V / Ig, V / Ig + G_, Ig * G_ / V], gap='G3')


def c4s4_moment(r):
    N = r.choice([10, 50, 100])
    R = r.choice([2, 5, 10])
    I = r.choice([0.5, 1, 2])
    m = N * I * math.pi * (R / 100) ** 2
    return NUM(f'Find the magnetic moment of a circular coil of {N} turns, radius {R} cm, carrying a current of {g(I)} A.', m, 'A m²', f'm = NIA = {N} × {g(I)} × π × ({g(R / 100)})² = {{ans}}.', wrongs=[N * I * 2 * math.pi * R / 100, m * 1e4, m / N], gap='G3')


def c4s4_case(r):
    who = name(r)
    G_ = r.choice([20, 25, 50])
    Ig = r.choice([1, 2, 5]) * 1e-3
    I = r.choice([1, 5])
    V = r.choice([5, 10])
    return {'stem': (f'In the lab, {who} has a moving coil galvanometer with coil resistance {G_} Ω and full-scale current {g(Ig * 1000)} mA.\n'
                     f'(i) What is the voltage across it at full-scale deflection? (ii) What shunt converts it to a 0-{I} A ammeter? (iii) What series resistance converts it to a 0-{V} V voltmeter? (iv) Which of the two meters has the higher resistance?'),
            'answer': f'(i) {sig(Ig * G_)} V (ii) {sig(Ig * G_ / (I - Ig))} Ω in parallel (iii) {sig(V / Ig - G_)} Ω in series (iv) the voltmeter',
            'key': '(i) V = I_gG (1). (ii) S = I_gG/(I − I_g) (1). (iii) R = V/I_g − G (1). (iv) voltmeter (1).'}


# ======================================================== ch05 Magnetism and Matter
# st1 bar magnet, dipole in uniform field

c5s1_terms = term_mcq([('magnetic dipole moment of a bar magnet', 'a vector from its S-pole to its N-pole'), ('torque on a magnet in a uniform field', 'τ = m × B'),
                       ('potential energy of a magnetic dipole', 'U = −m·B'), ('field on the axis of a short bar magnet', 'μ₀2m/(4πr³)'),
                       ('field on the equatorial line of a short bar magnet', 'μ₀m/(4πr³), opposite to m')],
                      'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c5s1_tf = tf_mcq('the bar magnet',
                 ['A bar magnet behaves like an equivalent solenoid.', 'Magnetic monopoles do not exist.', 'Magnetic field lines form closed loops.',
                  'A magnet in a uniform field experiences a torque but no net force.', 'Inside a bar magnet, field lines run from S to N.'],
                 ['Isolated magnetic poles can be obtained by breaking a magnet.', 'Magnetic field lines start at N-poles and end at S-poles inside the magnet.', 'A magnet in a uniform field experiences a net force.',
                  'Magnetic field lines can intersect.', 'The dipole moment points from N to S.'])

c5s1_explain = pool_txt([
    ('Why is it impossible to obtain an isolated magnetic pole by cutting a magnet?', 'Each piece becomes a complete magnet with N and S poles; magnetic monopoles do not exist.', '2 marks.'),
    ('In what way is a bar magnet like a solenoid? Give one piece of evidence.', 'Its field lines are like those of a solenoid; a cut solenoid, like a cut magnet, gives two weaker magnets.', '2 marks.'),
    ('A compass needle placed in a uniform field oscillates before settling. Why?', 'A restoring torque −mB sin θ acts; with inertia it overshoots and oscillates (damped) about the field direction.', '2 marks.'),
])

c5s1_ar = pool_ar([
    ('A freely suspended bar magnet aligns along the field.', 'The torque on it is zero and its energy is minimum when m is parallel to B.', 'a', 'R explains A.'),
    ('Magnetic field lines are continuous closed loops.', 'There are no magnetic monopoles; the net flux through any closed surface is zero.', 'a', 'R explains A.'),
    ('A bar magnet placed in a uniform field moves along the field.', 'The forces on its two poles are equal and opposite.', 'd', 'A is false: no net force; R is true.'),
])


def c5s1_torque(r):
    m = r.choice([0.5, 1, 2, 4, 5])
    B = r.choice([0.1, 0.2, 0.4, 0.5]) * 1e-1
    th = r.choice([30, 45, 60, 90])
    t = m * B * math.sin(math.radians(th))
    return NUM(f'A bar magnet of magnetic moment {g(m)} J T⁻¹ is placed at {th}° to a uniform magnetic field of {g(B)} T. Find the torque on it.', t, 'N m',
               f'τ = mB sin θ = {g(m)} × {g(B)} × sin {th}° = {{ans}}.', wrongs=[m * B * math.cos(math.radians(th)) or t * 2, m * B, m / B])


def c5s1_work(r):
    m = r.choice([0.5, 1, 2, 4])
    B = r.choice([0.02, 0.04, 0.05, 0.1])
    t1, t2 = r.choice([(0, 90), (0, 180), (60, 90), (0, 60)])
    W = m * B * (math.cos(math.radians(t1)) - math.cos(math.radians(t2)))
    return NUM(f'A bar magnet of moment {g(m)} J T⁻¹ is in a uniform field of {g(B)} T. Find the work done in turning it from θ = {t1}° to θ = {t2}° (θ between m and B).', W, 'J',
               f'W = mB(cos θ₁ − cos θ₂) = {g(m)} × {g(B)} × ({num(math.cos(math.radians(t1)), 2)} − ({num(math.cos(math.radians(t2)), 2)})) = {{ans}}.', wrongs=[m * B, W * 2, m * B * math.sin(math.radians(t2))])


def c5s1_field(r):
    m = r.choice([0.4, 0.5, 1, 2])
    d = r.choice([10, 15, 20])
    ax = r.choice([True, False])
    B = 1e-7 * (2 if ax else 1) * m / (d / 100) ** 3
    return NUM(f'Find the magnetic field due to a short bar magnet of moment {g(m)} J T⁻¹ at a point {d} cm from its centre on its {"axis" if ax else "equatorial line"}.', B, 'T',
               f'B = (μ₀/4π){"2m" if ax else "m"}/r³ = 10⁻⁷ × {"2 × " if ax else ""}{g(m)}/({g(d / 100)})³ = {{ans}}.', wrongs=[1e-7 * (1 if ax else 2) * m / (d / 100) ** 3, 1e-7 * m / (d / 100) ** 2, B * 4 * math.pi])


def c5s1_osc(r):
    m = r.choice([0.5, 1, 2])
    B = r.choice([0.01, 0.02, 0.05])
    I_ = r.choice([2, 5, 6, 8]) * 1e-6
    T = 2 * math.pi * math.sqrt(I_ / (m * B))
    return NUM(f'A small compass needle of moment of inertia {g(I_)} kg m² and magnetic moment {g(m)} A m² oscillates in a uniform field of {g(B)} T. Find its period of small oscillations.', T, 's',
               f'For small θ, restoring torque −mBθ (1) ⇒ SHM with T = 2π√(I/mB) (2) = {{ans}}.', wrongs=[2 * math.pi * math.sqrt(m * B / I_), math.sqrt(I_ / (m * B)), T * 2], gap='G5')


def c5s1_sol(r):
    N = r.choice([200, 500, 800, 1000])
    I = r.choice([0.5, 1, 2, 3])
    A = r.choice([1, 2, 2.5, 4]) * 1e-4
    m = N * I * A
    return NUM(f'A closely wound solenoid of {N} turns and area of cross-section {g(A * 1e4)} cm² carries a current of {g(I)} A. Find its magnetic moment. It behaves like which object?', m, 'A m²',
               f'm = NIA = {N} × {g(I)} × {g(A)} = {{ans}}; it behaves like a bar magnet.', wrongs=[N * I / A, m * 1e4, I * A], gap='G3')


c5s1_mcq = pool_mcq([
    ('A bar magnet of moment m is cut into two equal halves perpendicular to its length. The moment of each half is', 'm/2', ['m', '2m', 'm/4'], 'Pole strength is unchanged; length halves.'),
    ('A bar magnet of moment m is cut into two equal halves along its length. The moment of each half is', 'm/2', ['m', '2m', 'm/4'], 'Pole strength halves; length unchanged.'),
    ('The potential energy of a magnetic dipole in a uniform field is minimum when the angle between m and B is', '0°', ['90°', '180°', '45°'], 'U = −mB cos θ is least at θ = 0°.'),
    ('The SI unit of magnetic dipole moment is', 'A m² (J T⁻¹)', ['T m', 'Wb', 'A m⁻¹'], 'm = IA.'),
])


# st2 magnetisation, H, susceptibility

c5s2_terms = term_mcq([('magnetisation M', 'net magnetic moment per unit volume'), ('magnetic intensity H', 'H = B/μ₀ − M, set up by the free currents, e.g. nI'),
                       ('magnetic susceptibility χ', 'χ = M/H'), ('relative permeability μᵣ', 'μᵣ = 1 + χ = μ/μ₀'), ('permeability μ', 'μ = μ₀μᵣ, so B = μH')],
                      'Which of the following defines {a}?', 'Which quantity is {b}?', '{a}: {b}.')

c5s2_tf = tf_mcq('magnetisation and magnetic intensity',
                 ['M and H have the same unit, A m⁻¹.', 'Susceptibility is dimensionless.', 'B = μ₀(H + M).', 'μᵣ = 1 + χ.'],
                 ['M is measured in tesla.', 'Susceptibility has the unit A m⁻¹.', 'B = μ₀(H − M).', 'μᵣ = 1 − χ.'])

c5s2_explain = pool_txt([
    ('What is the significance of the sign of magnetic susceptibility?', 'χ < 0: diamagnetic, M opposite to H; χ > 0: paramagnetic or ferromagnetic, M along H.', '2 marks.'),
    ('Write the relation between B, H and M, and explain each term.', 'B = μ₀(H + M): H from free (conduction) currents, M from the material\'s magnetisation.', '2 marks.'),
])

c5s2_ar = pool_ar([
    ('Susceptibility of a diamagnetic material is small and negative.', 'Induced magnetisation in a diamagnetic material opposes the applied field.', 'a', 'R explains A.'),
    ('The relative permeability of a ferromagnetic material is very large.', 'Its susceptibility is very large and positive.', 'a', 'μᵣ = 1 + χ; R explains A.'),
    ('Magnetic susceptibility has the unit A m⁻¹.', 'M and H both have the unit A m⁻¹.', 'd', 'A is false: χ = M/H is dimensionless; R is true.'),
])


def c5s2_core(r):
    n = r.choice([500, 1000, 2000])
    I = r.choice([0.5, 1, 2])
    mur = r.choice([400, 800, 1000, 2000])
    H = n * I
    M = (mur - 1) * H
    B = MU0 * mur * H
    return NUM2(f'A solenoid with {n} turns per metre carries a current of {g(I)} A. Its core has relative permeability {mur}. Find H, M and B inside the core.', (H, M, B), ('A m⁻¹', 'A m⁻¹', 'T'),
                f'H = nI = {sig(H)} A m⁻¹ (1); M = (μᵣ − 1)H = {sig(M)} A m⁻¹ (2); B = μ₀μᵣH = {sig(B)} T (2).', wrongs=[(H, mur * H, MU0 * H), (H, M, MU0 * H), (n / I, M, B)], gap='G5')


def c5s2_chi(r):
    chi = r.choice([2.3e-5, 5e-4, -1.7e-5, 1.2e-3, -9e-6])
    return NUM(f'A material has magnetic susceptibility {g(chi).replace("-", "−")}. Find its relative permeability. Is it diamagnetic or paramagnetic?', 1 + chi, '',
               f'μᵣ = 1 + χ = {{ans}}; {"diamagnetic (χ < 0)" if chi < 0 else "paramagnetic (small positive χ)"}.', wrongs=[1 - chi, chi, 1 + 2 * chi], n=7, gap='G3')


def c5s2_M(r):
    H = r.choice([1, 2, 5]) * 1e3
    chi = r.choice([1e-4, 2e-4, 5e-3, 499])
    M = chi * H
    return NUM(f'A material of susceptibility {g(chi)} is placed in a magnetising field of {g(H)} A m⁻¹. Find its magnetisation.', M, 'A m⁻¹', f'M = χH = {g(chi)} × {g(H)} = {{ans}}.', wrongs=[H / chi, M * MU0, M + H])


def c5s2_B(r):
    H = r.choice([1, 2, 4]) * 1e3
    mur = r.choice([1000, 2000, 5000])
    B = MU0 * mur * H
    return NUM(f'Find the magnetic field B in an iron core of relative permeability {mur} when the magnetic intensity is {g(H)} A m⁻¹.', B, 'T', f'B = μ₀μᵣH = 4π × 10⁻⁷ × {mur} × {g(H)} = {{ans}}.', wrongs=[MU0 * H, mur * H, B / (4 * math.pi)])


# st3 dia, para, ferro

DPF = [('bismuth', 'diamagnetic'), ('copper', 'diamagnetic'), ('water', 'diamagnetic'), ('silver', 'diamagnetic'), ('lead', 'diamagnetic'), ('nitrogen (at STP)', 'diamagnetic'),
       ('aluminium', 'paramagnetic'), ('sodium', 'paramagnetic'), ('calcium', 'paramagnetic'), ('oxygen (at STP)', 'paramagnetic'), ('copper chloride', 'paramagnetic'),
       ('iron', 'ferromagnetic'), ('cobalt', 'ferromagnetic'), ('nickel', 'ferromagnetic'), ('gadolinium', 'ferromagnetic'), ('alnico', 'ferromagnetic')]


def c5s3_class(r):
    m, c = r.choice(DPF)
    wrong = [x for x in ('diamagnetic', 'paramagnetic', 'ferromagnetic', 'non-magnetic (χ = 0 exactly)') if x != c]
    return mcq(f'{m[0].upper() + m[1:]} is', c, wrong, f'{m[0].upper() + m[1:]} is {c}.', r)


def c5s3_pick(r):
    cat = r.choice(['diamagnetic', 'paramagnetic', 'ferromagnetic'])
    right = r.choice([m for m, c in DPF if c == cat])
    wrong = r.sample([m for m, c in DPF if c != cat], 3)
    return mcq(f'Which of the following is {cat}?', right, wrong, f'{right} is {cat}; the others are not.', r)


c5s3_tf = tf_mcq('magnetic materials',
                 ['Diamagnetic materials are weakly repelled by a magnet.', 'Superconductors are perfect diamagnets (χ = −1).', 'Paramagnetic susceptibility varies inversely with absolute temperature.',
                  'A ferromagnet becomes paramagnetic above its Curie temperature.', 'Soft iron has low coercivity and is used in electromagnets.'],
                 ['Diamagnetic materials are strongly attracted by a magnet.', 'Paramagnetic susceptibility increases with temperature.', 'Ferromagnetism increases above the Curie temperature.',
                  'Steel is preferred for transformer cores because of its high coercivity.', 'Diamagnetism is found only in a few materials.'])

c5s3_explain = pool_txt([
    ('Explain why a diamagnetic rod placed in a non-uniform field moves towards the weaker field region.', 'It acquires a small magnetisation opposite to the field, so it is repelled from the strong field region.', '2 marks.'),
    ('Why is soft iron used for electromagnets and transformer cores, while steel is used for permanent magnets?', 'Soft iron: high permeability, low retentivity and coercivity, small hysteresis loss. Steel: high retentivity and coercivity.', '2 marks.'),
    ('State Curie\'s law and explain it in terms of alignment of atomic dipoles.', 'χ = C/T: thermal agitation disturbs alignment of atomic moments more at higher T, so magnetisation falls.', '2 marks.'),
    ('What are magnetic domains? How do they explain ferromagnetism?', 'Regions with all atomic moments aligned; in a field, favourably aligned domains grow, giving large M.', '2 marks.'),
])

c5s3_ar = pool_ar([
    ('A diamagnetic substance is repelled by a strong magnet.', 'Its magnetisation is opposite to the applied field.', 'a', 'R explains A.'),
    ('The susceptibility of a paramagnetic material decreases as temperature rises.', 'Thermal agitation disturbs the alignment of atomic dipoles.', 'a', 'Curie\'s law; R explains A.'),
    ('Iron is ferromagnetic at all temperatures.', 'Ferromagnetic materials have domains.', 'd', 'A is false: above the Curie temperature it is paramagnetic; R is true.'),
    ('Superconductors expel magnetic field lines (Meissner effect).', 'Superconductors are perfect diamagnets.', 'a', 'R explains A.'),
])


def c5s3_curie(r):
    chi1 = r.choice([1.2e-5, 2.4e-5, 3.6e-5, 8e-5])
    T1 = r.choice([200, 250, 300])
    T2 = r.choice([100, 150, 400, 500, 600])
    chi2 = chi1 * T1 / T2
    return NUM(f'A paramagnetic salt has susceptibility {g(chi1)} at {T1} K. Assuming Curie\'s law, find its susceptibility at {T2} K.', chi2, '',
               f'χ ∝ 1/T ⇒ χ₂ = χ₁T₁/T₂ = {g(chi1)} × {T1}/{T2} = {{ans}}.', wrongs=[chi1 * T2 / T1, chi1, chi1 * (T1 / T2) ** 2], gap='G3')


c5s3_hyst = pool_mcq([
    ('The magnetisation that remains in a ferromagnet when the magnetising field is reduced to zero is called', 'retentivity (remanence)', ['coercivity', 'susceptibility', 'permeability'], 'Retentivity is B at H = 0.'),
    ('The reverse magnetising field needed to bring the magnetisation of a ferromagnet to zero is called', 'coercivity', ['retentivity', 'Curie temperature', 'hysteresis loss'], 'Coercivity is |H| at B = 0.'),
    ('A material for a permanent magnet should have', 'high retentivity and high coercivity', ['low retentivity and low coercivity', 'high retentivity and low coercivity', 'low permeability and low retentivity'], 'Steel suits this.'),
    ('The area of the hysteresis loop represents', 'energy lost per unit volume per cycle', ['the retentivity', 'the coercivity', 'the permeability'], 'Energy dissipated as heat.'),
])


def c5s3_case(r):
    rows = r.sample([('A', -1.6e-5), ('B', 2.1e-5), ('C', 850), ('D', -2.2e-5), ('E', 1.8e-3)], 4)
    t = ', '.join(f'{a}: χ = {g(c).replace("-", "−")}' for a, c in rows)
    ans = '; '.join(f'{a} {"diamagnetic" if c < 0 else ("ferromagnetic" if c > 1 else "paramagnetic")}' for a, c in rows)
    return {'stem': (f'A student measures the susceptibility of four samples at room temperature: {t}.\n'
                     '(i) Classify each sample. (ii) Which sample would be attracted most strongly by a magnet? (iii) How would the susceptibility of a paramagnetic sample change if it were cooled? (iv) Which sample would move away from the stronger part of a non-uniform field?'),
            'answer': f'(i) {ans} (ii) the sample with the largest χ (iii) it increases (χ ∝ 1/T) (iv) a sample with negative χ',
            'key': '(i) sign and size of χ (1). (ii) ferromagnetic / largest χ (1). (iii) Curie\'s law (1). (iv) diamagnetic (1).'}


# ======================================================== families

FAMILIES = {
    S + '01-st1': [F('C1', 'D1', 'mcq', c1s1_terms), F('C1', 'D2', 'mcq', c1s1_tf), F('C1', 'D1', 'mcq', c1s1_mcq), F('C2', 'D2', 'explain', c1s1_explain), F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c1s1_n), F('C3', 'D2', 'numerical', c1s1_rub), F('C4', 'D3', 'mcq', c1s1_which), F('C4', 'D4', 'multi_step', c1s1_water)],
    S + '01-st2': [F('C1', 'D2', 'mcq', c1s2_tf), F('C2', 'D2', 'explain', c1s2_explain), F('C2', 'D3', 'mcq', c1s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c1s2_factor),
                   F('C3', 'D2', 'numerical', c1s2_force), F('C3', 'D2', 'numerical', c1s2_medium), F('C3', 'D3', 'numerical', c1s2_ratio), F('C4', 'D3', 'multi_step', c1s2_line),
                   F('C4', 'D4', 'multi_step', c1s2_triangle), F('C4', 'D5', 'numerical', c1s2_null)],
    S + '01-st3': [F('C1', 'D1', 'mcq', c1s3_terms), F('C1', 'D2', 'mcq', c1s3_lines), F('C2', 'D2', 'explain', c1s3_explain), F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c1s3_derive), F('C3', 'D1', 'short', c1s3_E), F('C3', 'D2', 'numerical', c1s3_acc), F('C3', 'D2', 'numerical', c1s3_torque),
                   F('C3', 'D3', 'numerical', c1s3_axial), F('C4', 'D3', 'numerical', c1s3_null), F('C4', 'D4', 'multi_step', c1s3_work), F('C4', 'D5', 'multi_step', c1s3_stop),
                   F('C3', 'D3', 'case', c1s3_case)],
    S + '01-st4': [F('C1', 'D1', 'mcq', c1s4_terms), F('C1', 'D2', 'mcq', c1s4_tf), F('C2', 'D2', 'explain', c1s4_explain), F('C2', 'D3', 'mcq', c1s4_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c1s4_derive), F('C3', 'D1', 'short', c1s4_closed), F('C3', 'D2', 'numerical', c1s4_flat), F('C3', 'D2', 'numerical', c1s4_sheet),
                   F('C3', 'D3', 'numerical', c1s4_wire), F('C4', 'D3', 'numerical', c1s4_shell), F('C4', 'D4', 'multi_step', c1s4_cube), F('C4', 'D4', 'multi_step', c1s4_net),
                   F('C4', 'D3', 'case', c1s4_case)],
    S + '02-st1': [F('C1', 'D1', 'mcq', c2s1_terms), F('C1', 'D2', 'mcq', c2s1_tf), F('C2', 'D2', 'explain', c2s1_explain), F('C2', 'D3', 'mcq', c2s1_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c2s1_derive), F('C3', 'D1', 'short', c2s1_V), F('C3', 'D2', 'numerical', c2s1_work), F('C3', 'D3', 'numerical', c2s1_pe),
                   F('C3', 'D3', 'numerical', c2s1_dipole), F('C4', 'D3', 'multi_step', c2s1_speed), F('C4', 'D4', 'multi_step', c2s1_square), F('C4', 'D4', 'multi_step', c2s1_three),
                   F('C4', 'D5', 'numerical', c2s1_zero)],
    S + '02-st2': [F('C1', 'D1', 'mcq', c2s2_terms), F('C1', 'D2', 'mcq', c2s2_tf), F('C2', 'D2', 'explain', c2s2_explain), F('C2', 'D3', 'mcq', c2s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'mcq', c2s2_move), F('C3', 'D2', 'numerical', c2s2_Ed), F('C3', 'D3', 'numerical', c2s2_sphere), F('C4', 'D4', 'multi_step', c2s2_spheres),
                   F('C3', 'D3', 'case', c2s2_case)],
    S + '02-st3': [F('C1', 'D1', 'mcq', c2s3_terms), F('C1', 'D2', 'mcq', c2s3_tf), F('C2', 'D2', 'explain', c2s3_explain), F('C2', 'D3', 'mcq', c2s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'mcq', c2s3_mcq), F('C3', 'D1', 'short', c2s3_Kfind), F('C3', 'D2', 'numerical', c2s3_K), F('C3', 'D2', 'numerical', c2s3_field),
                   F('C4', 'D4', 'multi_step', c2s3_slab)],
    S + '02-st4': [F('C1', 'D2', 'mcq', c2s4_tf), F('C2', 'D2', 'explain', c2s4_explain), F('C2', 'D3', 'mcq', c2s4_ar, kinds=('ar',)), F('C2', 'D3', 'long', c2s4_derive),
                   F('C3', 'D1', 'short', c2s4_change), F('C3', 'D2', 'numerical', c2s4_pp), F('C3', 'D2', 'numerical', c2s4_energy), F('C3', 'D3', 'numerical', c2s4_comb),
                   F('C4', 'D4', 'long', c2s4_network), F('C4', 'D5', 'multi_step', c2s4_share), F('C3', 'D3', 'case', c2s4_case)],
    S + '03-st1': [F('C1', 'D1', 'mcq', c3s1_terms), F('C1', 'D2', 'mcq', c3s1_tf), F('C2', 'D2', 'explain', c3s1_explain), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c3s1_derive), F('C3', 'D1', 'short', c3s1_R), F('C3', 'D2', 'numerical', c3s1_vd), F('C3', 'D3', 'numerical', c3s1_temp),
                   F('C4', 'D3', 'numerical', c3s1_stretch), F('C4', 'D4', 'multi_step', c3s1_mob), F('C4', 'D5', 'long', c3s1_findT)],
    S + '03-st2': [F('C1', 'D2', 'mcq', c3s2_tf), F('C2', 'D2', 'explain', c3s2_explain), F('C2', 'D3', 'mcq', c3s2_ar, kinds=('ar',)), F('C3', 'D1', 'short', c3s2_P),
                   F('C3', 'D2', 'numerical', c3s2_bill), F('C3', 'D3', 'numerical', c3s2_mix), F('C4', 'D3', 'numerical', c3s2_equal), F('C4', 'D4', 'multi_step', c3s2_bulbs)],
    S + '03-st3': [F('C1', 'D1', 'mcq', c3s3_terms), F('C1', 'D2', 'mcq', c3s3_tf), F('C2', 'D2', 'explain', c3s3_explain), F('C2', 'D3', 'mcq', c3s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c3s3_terminal), F('C3', 'D2', 'numerical', c3s3_r), F('C3', 'D3', 'numerical', c3s3_series), F('C4', 'D3', 'multi_step', c3s3_charge),
                   F('C4', 'D4', 'long', c3s3_two), F('C4', 'D5', 'long', c3s3_maxP), F('C3', 'D3', 'case', c3s3_case)],
    S + '03-st4': [F('C1', 'D1', 'mcq', c3s4_terms), F('C1', 'D2', 'mcq', c3s4_tf), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c3s4_derive), F('C3', 'D1', 'short', c3s4_junction), F('C3', 'D2', 'numerical', c3s4_wb), F('C3', 'D3', 'numerical', c3s4_metre),
                   F('C4', 'D4', 'multi_step', c3s4_shift), F('C4', 'D4', 'long', c3s4_loop), F('C4', 'D3', 'case', c3s4_case)],
    S + '04-st1': [F('C1', 'D1', 'mcq', c4s1_terms), F('C1', 'D2', 'mcq', c4s1_tf), F('C2', 'D2', 'explain', c4s1_explain), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c4s1_F), F('C3', 'D2', 'numerical', c4s1_radius), F('C3', 'D3', 'numerical', c4s1_freq), F('C4', 'D3', 'multi_step', c4s1_accel),
                   F('C4', 'D4', 'long', c4s1_helix), F('C4', 'D3', 'numerical', c4s1_selector)],
    S + '04-st2': [F('C1', 'D1', 'mcq', c4s2_terms), F('C1', 'D2', 'mcq', c4s2_tf), F('C2', 'D2', 'explain', c4s2_explain), F('C2', 'D3', 'mcq', c4s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c4s2_derive), F('C3', 'D1', 'short', c4s2_centre), F('C3', 'D2', 'numerical', c4s2_element), F('C3', 'D3', 'numerical', c4s2_axis),
                   F('C4', 'D3', 'numerical', c4s2_ratio), F('C4', 'D4', 'multi_step', c4s2_semi)],
    S + '04-st3': [F('C1', 'D1', 'mcq', c4s3_terms), F('C1', 'D2', 'mcq', c4s3_tf), F('C2', 'D2', 'explain', c4s3_explain), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c4s3_derive), F('C3', 'D1', 'short', c4s3_wire), F('C3', 'D2', 'numerical', c4s3_sol), F('C3', 'D3', 'numerical', c4s3_toroid),
                   F('C4', 'D4', 'multi_step', c4s3_two), F('C4', 'D5', 'long', c4s3_inside), F('C3', 'D3', 'case', c4s3_case)],
    S + '04-st4': [F('C1', 'D1', 'mcq', c4s4_terms), F('C1', 'D2', 'mcq', c4s4_tf), F('C2', 'D2', 'explain', c4s4_explain), F('C2', 'D3', 'mcq', c4s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c4s4_moment), F('C3', 'D2', 'numerical', c4s4_force), F('C3', 'D3', 'numerical', c4s4_torque), F('C4', 'D3', 'numerical', c4s4_ammeter),
                   F('C4', 'D4', 'multi_step', c4s4_voltmeter), F('C4', 'D3', 'case', c4s4_case)],
    S + '05-st1': [F('C1', 'D1', 'mcq', c5s1_terms), F('C1', 'D2', 'mcq', c5s1_tf), F('C2', 'D2', 'explain', c5s1_explain), F('C2', 'D3', 'mcq', c5s1_ar, kinds=('ar',)),
                   F('C2', 'D3', 'mcq', c5s1_mcq), F('C3', 'D1', 'short', c5s1_sol), F('C3', 'D2', 'numerical', c5s1_torque), F('C3', 'D3', 'numerical', c5s1_field),
                   F('C4', 'D3', 'numerical', c5s1_work), F('C4', 'D4', 'multi_step', c5s1_osc)],
    S + '05-st2': [F('C1', 'D1', 'mcq', c5s2_terms), F('C1', 'D2', 'mcq', c5s2_tf), F('C2', 'D2', 'explain', c5s2_explain), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c5s2_chi), F('C3', 'D2', 'numerical', c5s2_M), F('C3', 'D3', 'numerical', c5s2_B), F('C4', 'D4', 'long', c5s2_core)],
    S + '05-st3': [F('C1', 'D1', 'mcq', c5s3_class), F('C1', 'D2', 'mcq', c5s3_pick), F('C1', 'D2', 'mcq', c5s3_tf), F('C2', 'D2', 'explain', c5s3_explain), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', c5s3_hyst), F('C3', 'D2', 'numerical', c5s3_curie), F('C4', 'D3', 'case', c5s3_case)],
}

FAMILIES = polish(FAMILIES)
