"""CBSE class 12 physics (NCERT Physics XII) families, chapters 6-10."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, name, two_names, CITIES  # noqa: F401
from g11_physics_util import polish, sig, g, NUM, NUM2, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401

S = 'cbse-g12-physics-ch'
E0 = 8.854e-12
MU0 = 4 * math.pi * 1e-7
C = 3e8
G = 9.8


def dg(x):
    return f'{num(x, 1)}°'


# ======================================================== ch06 Electromagnetic Induction
# st1 Faraday's experiments, flux, Faraday's law

c6s1_terms = term_mcq([('magnetic flux', 'Φ = B·A = BA cos θ'), ('weber', 'the SI unit of magnetic flux, 1 Wb = 1 T m²'),
                       ('Faraday\'s law of induction', 'the induced emf equals the negative rate of change of magnetic flux linked'),
                       ('induced emf in a coil of N turns', 'ε = −N dΦ/dt'), ('electromagnetic induction', 'production of emf in a circuit by a changing magnetic flux')],
                      'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c6s1_tf = tf_mcq('electromagnetic induction',
                 ['An emf is induced only while the flux through a coil is changing.', 'A faster-moving magnet induces a larger emf in a coil.', 'Induced emf is larger for a coil with more turns.',
                  'Flux can be changed by changing B, the area, or the orientation of the coil.'],
                 ['A steady magnetic field through a coil induces a steady emf.', 'The induced emf depends on the flux, not on its rate of change.', 'A magnet held at rest inside a coil induces a current.',
                  'Induced emf is independent of the number of turns.'])

c6s1_explain = pool_txt([
    ('Describe one of Faraday\'s experiments with a magnet and a coil, and the conclusion drawn.', 'Moving a magnet towards or away from a coil deflects a galvanometer; no deflection when at rest. A changing flux induces emf.', '2 marks.'),
    ('A coil and a galvanometer form a closed loop. Why is there a deflection when the current in a nearby coil is switched on or off, but not while it is steady?', 'The flux linked with the first coil changes only while the current changes.', '2 marks.'),
    ('How can the emf induced in a coil by a moving magnet be increased? Give two ways.', 'Move the magnet faster, use more turns, use a stronger magnet, or use a soft iron core.', '2 marks.'),
])

c6s1_ar = pool_ar([
    ('An emf is induced in a closed loop when the magnetic flux through it changes.', 'Faraday\'s law: ε = −dΦ/dt.', 'a', 'R explains A.'),
    ('When a magnet is held at rest near a coil, no current is induced.', 'The flux linked with the coil is then constant.', 'a', 'R explains A.'),
    ('The induced emf depends on the magnitude of the flux linked.', 'Induced emf is proportional to the rate of change of flux.', 'd', 'A is false: it depends on the rate of change; R is true.'),
])


def c6s1_flux(r):
    B = r.choice([0.1, 0.2, 0.5, 0.8, 1.2])
    A = r.choice([20, 50, 100, 200, 400])
    th = r.choice([0, 30, 60])
    phi = B * A * 1e-4 * math.cos(math.radians(th))
    return NUM(f'A plane loop of area {A} cm² is placed in a uniform field of {g(B)} T with its normal at {th}° to the field. Find the magnetic flux through the loop.', phi, 'Wb',
               f'Φ = BA cos θ = {g(B)} × {g(A * 1e-4)} × cos {th}° = {{ans}}.', wrongs=[B * A * 1e-4 * math.sin(math.radians(th)) or phi * 2, B * A * math.cos(math.radians(th)), phi / 2], gap='G3')


def c6s1_emf(r):
    N = r.choice([50, 100, 200, 500])
    A = r.choice([10, 20, 50, 100])
    B1 = r.choice([0, 0.1, 0.2])
    B2 = B1 + r.choice([0.2, 0.3, 0.5, 0.8])
    t = r.choice([0.1, 0.2, 0.5, 0.05])
    e = N * A * 1e-4 * (B2 - B1) / t
    return NUM(f'A coil of {N} turns and area {A} cm² is placed with its plane perpendicular to a magnetic field. The field changes uniformly from {g(B1)} T to {g(B2)} T in {g(t)} s. Find the magnitude of the induced emf.', e, 'V',
               f'|ε| = NAΔB/Δt = {N} × {g(A * 1e-4)} × {g(B2 - B1)}/{g(t)} = {{ans}}.', wrongs=[A * 1e-4 * (B2 - B1) / t, N * A * 1e-4 * B2 / t if B1 else e * 2, e * t * t])


def c6s1_turn(r):
    N = r.choice([50, 100, 200])
    A = r.choice([50, 100, 200])
    B = r.choice([0.1, 0.2, 0.4, 0.5])
    t1, t2 = r.choice([(0, 90), (0, 180), (90, 0), (0, 60)])
    dt = r.choice([0.1, 0.2, 0.25, 0.5])
    e = N * B * A * 1e-4 * abs(math.cos(math.radians(t1)) - math.cos(math.radians(t2))) / dt
    return NUM(f'A coil of {N} turns and area {A} cm² is in a uniform field of {g(B)} T. It is rotated in {g(dt)} s so that the angle between its normal and the field changes from {t1}° to {t2}°. Find the average induced emf.', e, 'V',
               f'ΔΦ per turn = BA|cos θ₁ − cos θ₂| = {sig(B * A * 1e-4 * abs(math.cos(math.radians(t1)) - math.cos(math.radians(t2))))} Wb (1); ε = NΔΦ/Δt (1) = {{ans}} (1).',
               wrongs=[N * B * A * 1e-4 / dt if abs(math.cos(math.radians(t1)) - math.cos(math.radians(t2))) != 1 else 2 * e, e / N, e * dt])


def c6s1_charge(r):
    N = r.choice([50, 100, 200, 500])
    A = r.choice([10, 20, 50])
    B = r.choice([0.1, 0.2, 0.5])
    R = r.choice([2, 5, 10, 20])
    rev = r.random() < 0.5
    dphi = (2 if rev else 1) * B * A * 1e-4
    Q = N * dphi / R
    what = 'turned through 180° (reversing the flux)' if rev else 'pulled out of the field completely'
    return NUM(f'A coil of {N} turns, area {A} cm² and resistance {R} Ω is placed perpendicular to a uniform field of {g(B)} T. It is {what}. Find the charge that flows through the coil.', Q, 'C',
               f'Q = ∫I dt = NΔΦ/R (2); ΔΦ = {"2BA" if rev else "BA"} = {sig(dphi)} Wb (1); Q = {N} × {sig(dphi)}/{R} = {{ans}} (1). It does not depend on how fast it is done.',
               wrongs=[N * B * A * 1e-4 / R if rev else 2 * Q, dphi / R, N * dphi * R], gap='G5')


def c6s1_ramp(r):
    N = r.choice([100, 200, 500])
    A = r.choice([10, 20, 25, 50])
    k = r.choice([0.01, 0.02, 0.05, 0.1])
    R = r.choice([5, 10, 20])
    e = N * A * 1e-4 * k
    return NUM2(f'The magnetic field through a coil of {N} turns and area {A} cm² (normal along the field) varies as B = (0.2 + {g(k)}t) T, t in seconds. The coil has resistance {R} Ω. Find the induced emf and current.', (e, e / R), ('V', 'A'),
                f'dB/dt = {g(k)} T s⁻¹ (1); ε = NA dB/dt = {sig(e)} V (1); I = ε/R = {sig(e / R)} A (1).', wrongs=[(N * A * 1e-4 * (0.2 + k), (0.2 + k) * N * A * 1e-4 / R), (A * 1e-4 * k, A * 1e-4 * k / R), (e, e * R)])


# st2 Lenz's law, motional emf

c6s2_terms = term_mcq([('Lenz\'s law', 'the induced current flows in a direction that opposes the change producing it'), ('motional emf', 'ε = Blv for a rod moving perpendicular to B'),
                       ('emf across a rod rotating about one end', 'ε = ½Bωl²'), ('Fleming\'s right-hand rule', 'gives the direction of induced current in a conductor moving in a field')],
                      'Which statement describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c6s2_tf = tf_mcq("Lenz's law and motional emf",
                 ['Lenz\'s law is a consequence of conservation of energy.', 'A magnet falling through a copper tube falls slower than in free fall.', 'The emf across a rod moving parallel to B is zero.',
                  'Work done against the magnetic force on the induced current appears as heat.'],
                 ['Lenz\'s law follows from conservation of charge.', 'An induced current always helps the change producing it.', 'A magnet falls faster through a copper tube.',
                  'A rod moving along its own length in a field has the largest emf.'])

c6s2_explain = pool_txt([
    ('Show that Lenz\'s law is a consequence of conservation of energy.', 'If the induced current aided the change, the magnet would accelerate without work being done, creating energy; so it must oppose.', '2 marks.'),
    ('The N-pole of a bar magnet is moved towards a closed coil. What is the direction of the induced current as seen from the magnet\'s side?', 'Anticlockwise: the near face becomes an N-pole to repel the approaching magnet.', '2 marks.'),
    ('A metal ring is placed on top of a solenoid. When the current is switched on, the ring jumps. Explain.', 'The increasing flux induces a current in the ring opposing the change; the ring is repelled.', '2 marks.'),
])

c6s2_ar = pool_ar([
    ('A bar magnet dropped through a long copper tube reaches a terminal velocity.', 'Induced currents in the tube oppose the motion of the magnet.', 'a', 'R explains A.'),
    ('An external agent must do work to move a conductor through a magnetic field in a closed circuit.', 'The induced current experiences a force opposing the motion.', 'a', 'R explains A.'),
    ('Lenz\'s law violates conservation of energy.', 'The induced current opposes the change in flux.', 'd', 'A is false: Lenz\'s law is required by energy conservation; R is true.'),
])

c6s2_lenz = pool_mcq([
    ('The N-pole of a magnet is moved away from a coil. Seen from the magnet\'s side, the induced current in the coil is', 'clockwise (the near face becomes S, attracting the magnet)', ['anticlockwise', 'zero', 'alternating'], 'Lenz: oppose the recession.'),
    ('A rectangular loop is being pulled out of a uniform field directed into the page. The induced current in the loop is', 'clockwise, to maintain the inward flux', ['anticlockwise', 'zero', 'first clockwise then anticlockwise'], 'Inward flux decreasing, so induced field is inward: clockwise.'),
    ('The current in a long straight wire is increasing towards the north. A loop lies to the east of the wire in the same horizontal plane. The induced current in the loop, seen from above, is', 'anticlockwise', ['clockwise', 'zero', 'along the wire direction'], 'The wire\'s field there points down and is increasing; induced field points up: anticlockwise from above.'),
    ('The S-pole of a magnet is moved towards a coil. Seen from the magnet\'s side, the induced current in the coil is', 'clockwise (the near face becomes S, repelling the magnet)', ['anticlockwise', 'zero', 'alternating'], 'Lenz: oppose the approach.'),
])


def c6s2_blv(r):
    B = r.choice([0.1, 0.2, 0.5, 0.8])
    l = r.choice([10, 20, 25, 50, 100])
    v = r.choice([2, 5, 10, 15])
    e = B * l / 100 * v
    return NUM(f'A straight rod {l} cm long moves at {v} m s⁻¹ perpendicular to its length and to a uniform field of {g(B)} T. Find the emf induced across its ends.', e, 'V',
               f'ε = Blv = {g(B)} × {g(l / 100)} × {v} = {{ans}}.', wrongs=[B * l * v, B * v / (l / 100), e / 2], gap='G3')


def c6s2_rod(r):
    B = r.choice([0.2, 0.5, 1])
    l = r.choice([20, 50, 100])
    v = r.choice([2, 4, 5, 10])
    R = r.choice([1, 2, 5, 10])
    e = B * l / 100 * v
    I = e / R
    Fv = B * I * l / 100
    return NUM2(f'A metal rod of length {l} cm slides at a steady {v} m s⁻¹ along two parallel rails connected by a {R} Ω resistor. A field of {g(B)} T acts perpendicular to the plane of the rails. Find the current and the force needed to keep the rod moving (ignore friction).',
                (I, Fv), ('A', 'N'), f'ε = Blv = {sig(e)} V (1); I = ε/R = {sig(I)} A (1); F = BIl = B²l²v/R = {sig(Fv)} N (1).', wrongs=[(e, B * e * l / 100), (I, Fv * 2), (e / R, B * I)])


def c6s2_power(r):
    B = r.choice([0.5, 1])
    l = r.choice([20, 50])
    v = r.choice([2, 5, 10])
    R = r.choice([1, 2, 4])
    e = B * l / 100 * v
    I = e / R
    Fv = B * I * l / 100
    P = Fv * v
    return NUM2(f'In a sliding-rod generator, a rod of length {l} cm moves at {v} m s⁻¹ on rails in a field of {g(B)} T; the circuit resistance is {R} Ω. Find the mechanical power supplied by the external agent and the electrical power dissipated in the resistor. Comment.',
                (P, I * I * R), ('W', 'W'), f'F = B²l²v/R = {sig(Fv)} N (1); P_mech = Fv = {sig(P)} W (1); P_elec = I²R = ε²/R = {sig(I * I * R)} W (1): equal, as energy conservation requires (Lenz\'s law).',
                wrongs=[(P, P / 2), (Fv, I * I * R), (P * 2, I * R)], gap='G5')


def c6s2_rotate(r):
    B = r.choice([0.2, 0.4, 0.5, 1])
    l = r.choice([0.5, 1, 1.5])
    w = r.choice([10, 20, 50, 100])
    e = 0.5 * B * w * l * l
    return NUM(f'A metal rod of length {g(l)} m rotates with angular speed {w} rad s⁻¹ about an axis through one end, perpendicular to the rod and parallel to a uniform field of {g(B)} T. Find the emf between its ends.', e, 'V',
               f'Each element at x moves at ωx: ε = ∫Bωx dx = ½Bωl² (2) = ½ × {g(B)} × {w} × {g(l)}² = {{ans}} (1).', wrongs=[B * w * l * l, B * w * l, e / 2], gap='G5')


def c6s2_terminal(r):
    m = r.choice([10, 20, 50]) / 1000
    B = r.choice([0.5, 1])
    l = r.choice([0.2, 0.5])
    R = r.choice([0.5, 1, 2])
    v = m * G * R / (B * B * l * l)
    return NUM(f'A horizontal conducting rod of mass {g(m * 1000)} g and length {g(l)} m slides down two long vertical frictionless rails joined at the top by a {g(R)} Ω resistor. A horizontal field of {g(B)} T is perpendicular to the plane of the rails. Find the terminal velocity of the rod. (g = 9.8 m s⁻²)',
               v, 'm s⁻¹', f'At terminal velocity, magnetic force = weight: B²l²v/R = mg (3) ⇒ v = mgR/(B²l²) (1) = {{ans}} (1).', wrongs=[m * G * R / (B * l), m * G / (B * B * l * l * R), v * 2], gap='G5')


c6s2_derive = pool_txt([
    ('Derive the expression ε = Blv for the motional emf of a rod sliding on rails in a uniform magnetic field, using Faraday\'s law.', 'ε = Blv', 'Φ = Blx (2); dΦ/dt = Bl dx/dt = Blv (2); direction by Lenz (1).'),
    ('Derive the expression for the motional emf using the Lorentz force on the free charges in the rod.', 'ε = Blv', 'F = qvB along the rod (2); work per unit charge over length l (2); ε = Blv (1).'),
])


def c6s2_case(r):
    who = name(r)
    B = r.choice([0.1, 0.2, 0.5])
    l = r.choice([10, 20, 30])
    v = r.choice([1, 2, 5])
    R = r.choice([2, 5, 10])
    e = B * l / 100 * v
    return {'stem': (f'In a demonstration, {who} pulls a square wire loop of side {l} cm and resistance {R} Ω at a steady {v} m s⁻¹ out of a region of uniform field {g(B)} T directed into the page.\n'
                     '(i) What is the emf induced while the loop is leaving the field? (ii) Find the induced current. (iii) State its direction. (iv) What happens to the emf once the loop is completely outside the field?'),
            'answer': f'(i) {sig(e)} V (ii) {sig(e / R)} A (iii) clockwise (opposes the decrease of inward flux) (iv) it becomes zero',
            'key': '(i) ε = Blv (1). (ii) I = ε/R (1). (iii) Lenz\'s law (1). (iv) flux no longer changes (1).'}


# st3 eddy currents

c6s3_tf = tf_mcq('eddy currents',
                 ['Eddy currents are induced in bulk conductors when the flux through them changes.', 'Laminating a transformer core reduces eddy current losses.', 'Eddy currents are used in electromagnetic braking of trains.',
                  'Eddy currents heat the metal in an induction furnace.'],
                 ['Eddy currents are produced only in insulators.', 'A solid core reduces eddy currents more than a laminated one.', 'Eddy currents always increase the efficiency of transformers.',
                  'Eddy currents flow only along a straight line.'])

c6s3_uses = term_mcq([('magnetic braking in trains', 'electromagnets near the rails induce eddy currents that oppose the motion'),
                      ('electromagnetic damping in galvanometers', 'eddy currents in the metal core bring the coil to rest quickly'),
                      ('induction furnace', 'a high-frequency alternating field induces large eddy currents that melt the metal'),
                      ('electric power meter', 'a rotating aluminium disc driven by eddy currents measures energy used'),
                      ('laminated transformer core', 'thin insulated sheets increase resistance to eddy currents and reduce losses')],
                     'How does the use of eddy currents (or their reduction) work in {a}?', 'Which application is described by: {b}?', '{a}: {b}.')

c6s3_explain = pool_txt([
    ('Why are the cores of transformers laminated?', 'Insulated thin sheets cut the paths of eddy currents, reducing them and hence the heat (energy) loss.', '2 marks.'),
    ('A copper plate swings like a pendulum between the poles of a magnet. It stops quickly. Why? What happens if slots are cut in it?', 'Eddy currents oppose the motion (damping); slots reduce the eddy currents, so it swings longer.', '2 marks.'),
    ('Explain the principle of electromagnetic damping in a moving coil galvanometer.', 'Eddy currents in the metallic frame oppose the motion of the coil so it comes to rest quickly.', '2 marks.'),
])

c6s3_ar = pool_ar([
    ('A slotted metal plate swinging between magnetic poles is damped less than a solid plate.', 'Slots reduce the area available for eddy currents.', 'a', 'R explains A.'),
    ('Transformer cores are made of thin laminated sheets.', 'Lamination reduces eddy current losses.', 'a', 'R explains A.'),
    ('Eddy currents are undesirable in all situations.', 'Eddy currents produce heat.', 'd', 'A is false: they are useful in braking, furnaces, damping; R is true.'),
])

c6s3_mcq = pool_mcq([
    ('A magnet dropped through a vertical copper pipe takes longer to fall than through a plastic pipe because', 'eddy currents in the copper oppose its motion', ['copper attracts magnets', 'air resistance is larger in copper', 'plastic repels magnets'], 'Lenz\'s law.'),
    ('Which of the following would have the largest eddy currents when placed in a changing field?', 'a solid copper block', ['a laminated iron core', 'a copper block with many slots', 'a stack of insulated thin wires'], 'Large unbroken conducting path.'),
    ('Induction cooktops work only with vessels made of', 'conducting (preferably ferromagnetic) metals', ['glass', 'ceramic', 'plastic'], 'Eddy currents are induced in the vessel.'),
    ('The main purpose of laminating the core of a transformer is to', 'reduce eddy current losses', ['increase the flux', 'reduce copper losses', 'reduce hysteresis loss to zero'], 'Thin insulated sheets.'),
])


def c6s3_case(r):
    who = name(r)
    city = r.choice(CITIES)
    return {'stem': (f'In the {city} metro, {who} learns that trains use electromagnetic brakes in addition to friction brakes. Strong electromagnets near the rails are switched on when the train has to slow down.\n'
                     '(i) What is induced in the rails (or in a metal disc on the axle)? (ii) Why does this slow the train? (iii) Why is the braking effect smaller at low speed? (iv) Name one other application of the same effect.'),
            'answer': '(i) eddy currents (ii) by Lenz\'s law they oppose the relative motion (iii) the rate of change of flux, and hence the eddy currents, are smaller at low speed (iv) induction furnace / galvanometer damping / power meter',
            'key': '(i) eddy currents (1). (ii) Lenz\'s law (1). (iii) emf ∝ speed (1). (iv) any valid application (1).'}


# st4 self and mutual inductance; AC generator

c6s4_terms = term_mcq([('self-inductance', 'the flux linkage per unit current in the same coil, NΦ = LI'), ('mutual inductance', 'flux linkage in one coil per unit current in another, N₂Φ₂ = MI₁'),
                       ('henry', 'the SI unit of inductance, 1 H = 1 V s A⁻¹'), ('energy stored in an inductor', '½LI²'),
                       ('self-inductance of a long solenoid', 'μ₀N²A/l'), ('peak emf of an AC generator', 'NBAω')],
                      'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c6s4_tf = tf_mcq('inductance and the AC generator',
                 ['Self-inductance is the electrical analogue of inertia (mass).', 'A soft iron core increases the self-inductance of a coil.', 'The emf of an AC generator is ε = NBAω sin ωt.',
                  'Mutual inductance depends on the separation and relative orientation of the coils.'],
                 ['Self-inductance depends on the current in the coil.', 'Inductance is measured in tesla.', 'An AC generator converts electrical energy to mechanical energy.',
                  'The mutual inductance of two coils is independent of their separation.'])

c6s4_explain = pool_txt([
    ('Why is self-inductance called the inertia of electricity?', 'It opposes any change of current in a circuit, just as mass opposes change of velocity; energy ½LI² is like ½mv².', '2 marks.'),
    ('Why does a spark appear at the switch when a circuit containing a large inductor is broken?', 'The rapid fall of current induces a large back emf L dI/dt which ionises the air in the gap.', '2 marks.'),
    ('State the principle of an AC generator and write the expression for the emf.', 'A coil rotated in a magnetic field has a changing flux; ε = NBAω sin ωt.', '2 marks.'),
])

c6s4_ar = pool_ar([
    ('The self-inductance of a coil increases when a soft iron core is inserted.', 'L = μᵣμ₀N²A/l.', 'a', 'R explains A.'),
    ('The emf of an AC generator is maximum when the plane of the coil is parallel to the field.', 'The rate of change of flux is then maximum.', 'a', 'R explains A.'),
    ('Self-inductance of a coil depends on the current through it.', 'Flux linkage NΦ = LI.', 'd', 'A is false: L depends on geometry and core; R is true.'),
])


def c6s4_L(r):
    N = r.choice([200, 500, 1000])
    l = r.choice([20, 25, 50, 100])
    A = r.choice([2, 5, 10, 20])
    L = MU0 * N * N * A * 1e-4 / (l / 100)
    return NUM(f'Find the self-inductance of an air-cored solenoid of length {l} cm, {N} turns and cross-sectional area {A} cm².', L, 'H',
               f'L = μ₀N²A/l = 4π × 10⁻⁷ × {N}² × {g(A * 1e-4)}/{g(l / 100)} = {{ans}}.', wrongs=[MU0 * N * A * 1e-4 / (l / 100), L * 100, MU0 * N * N * A / l], gap='G3')


def c6s4_back(r):
    L = r.choice([0.1, 0.2, 0.5, 1, 2])
    I1 = r.choice([0, 1, 2])
    I2 = I1 + r.choice([2, 3, 5])
    t = r.choice([0.01, 0.05, 0.1, 0.2])
    e = L * (I2 - I1) / t
    return NUM(f'The current in a coil of self-inductance {g(L)} H rises uniformly from {I1} A to {I2} A in {g(t)} s. Find the magnitude of the self-induced emf.', e, 'V',
               f'|ε| = L ΔI/Δt = {g(L)} × {I2 - I1}/{g(t)} = {{ans}}.', wrongs=[L * I2 / t if I1 else e * 2, (I2 - I1) / (L * t), e * t])


def c6s4_U(r):
    L = r.choice([0.05, 0.1, 0.2, 0.5, 2])
    I = r.choice([1, 2, 3, 4, 5])
    return NUM(f'Find the energy stored in the magnetic field of an inductor of {g(L)} H carrying a steady current of {I} A.', 0.5 * L * I * I, 'J', f'U = ½LI² = ½ × {g(L)} × {I}² = {{ans}}.', wrongs=[L * I * I, 0.5 * L * I, L * I])


def c6s4_M(r):
    n1 = r.choice([500, 1000, 2000])
    N2 = r.choice([50, 100, 200])
    A = r.choice([5, 10, 20])
    dI = r.choice([1, 2, 5])
    dt = r.choice([0.01, 0.05, 0.1])
    M = MU0 * n1 * N2 * A * 1e-4
    e = M * dI / dt
    return NUM2(f'A long solenoid has {n1} turns per metre and cross-sectional area {A} cm². A coil of {N2} turns is wound tightly over its middle. Find the mutual inductance, and the emf induced in the coil when the solenoid current changes by {dI} A in {g(dt)} s.', (M, e), ('H', 'V'),
                f'B = μ₀n₁I; flux linkage of coil = N₂μ₀n₁IA (1) ⇒ M = μ₀n₁N₂A = {sig(M)} H (2); ε = M ΔI/Δt = {sig(e)} V (2).', wrongs=[(M * 10, e * 10), (MU0 * n1 * A * 1e-4, MU0 * n1 * A * 1e-4 * dI / dt), (M, M * dt / dI)], gap='G5')


def c6s4_gen(r):
    N = r.choice([50, 100, 200, 500])
    A = r.choice([100, 200, 300, 500])
    B = r.choice([0.05, 0.1, 0.2, 0.5])
    f = r.choice([50, 25, 60])
    e0 = N * B * A * 1e-4 * 2 * math.pi * f
    return NUM(f'A coil of {N} turns, each of area {A} cm², rotates at {f} rev s⁻¹ about an axis perpendicular to a uniform field of {g(B)} T. Find the peak emf generated.', e0, 'V',
               f'ω = 2πν = {sig(2 * math.pi * f)} rad s⁻¹; ε₀ = NBAω = {N} × {g(B)} × {g(A * 1e-4)} × {sig(2 * math.pi * f)} = {{ans}}.', wrongs=[N * B * A * 1e-4 * f, e0 / math.sqrt(2), e0 * 2])


def c6s4_inst(r):
    N = r.choice([100, 200])
    A = r.choice([100, 200])
    B = r.choice([0.1, 0.2])
    w = r.choice([100, 314, 50])
    th = r.choice([30, 60, 90])
    e0 = N * B * A * 1e-4 * w
    e = e0 * math.sin(math.radians(th))
    return NUM2(f'A generator coil has {N} turns of area {A} cm² and rotates at ω = {w} rad s⁻¹ in a field of {g(B)} T. Find the peak emf, and the emf at the instant the normal to the coil makes {th}° with the field.', (e0, e), ('V', 'V'),
                f'ε₀ = NBAω = {sig(e0)} V (1.5); ε = ε₀ sin ωt with ωt = {th}°: ε = {sig(e)} V (1.5).', wrongs=[(e0, e0 * math.cos(math.radians(th))), (e0 / math.sqrt(2), e / math.sqrt(2)), (e0 * 2, e * 2)])


c6s4_derive = pool_txt([
    ('Derive an expression for the self-inductance of a long air-cored solenoid.', 'L = μ₀n²Al = μ₀N²A/l', 'B = μ₀nI (1); flux linkage NBA = μ₀n²AlI (2); L = NΦ/I (2).'),
    ('Derive the expression for the energy stored in an inductor carrying current I.', 'U = ½LI²', 'Work against back emf dW = LI dI (3); integrate (2).'),
    ('Explain the working of an AC generator and derive the expression for the induced emf.', 'ε = NBAω sin ωt', 'Diagram and parts (2); Φ = NBA cos ωt (1); ε = −dΦ/dt (2).'),
])


def c6s4_case(r):
    who = name(r)
    N = r.choice([100, 200])
    A = r.choice([0.01, 0.02, 0.05])
    B = r.choice([0.1, 0.2])
    f = 50
    e0 = N * B * A * 2 * math.pi * f
    return {'stem': (f'{who} visits a small hydro-electric plant. A model generator there has a coil of {N} turns, each of area {g(A)} m², rotating at {f} rev s⁻¹ in a field of {g(B)} T.\n'
                     '(i) Write the expression for the instantaneous emf. (ii) Find the peak emf. (iii) Find the rms emf. (iv) At what position of the coil is the emf zero?'),
            'answer': f'(i) ε = NBAω sin ωt (ii) {sig(e0)} V (iii) {sig(e0 / math.sqrt(2))} V (iv) when the plane of the coil is perpendicular to the field (flux maximum)',
            'key': '(i) (1). (ii) ε₀ = NBA × 2πν (1). (iii) ε₀/√2 (1). (iv) dΦ/dt = 0 there (1).'}


# ======================================================== ch07 Alternating Current
# st1 R, L, C, phasors and reactance

c7s1_terms = term_mcq([('rms value of an alternating current', 'I₀/√2, the steady current giving the same heating effect'), ('inductive reactance', 'X_L = ωL'),
                       ('capacitive reactance', 'X_C = 1/(ωC)'), ('phase relation in a pure inductor', 'current lags the voltage by π/2'),
                       ('phase relation in a pure capacitor', 'current leads the voltage by π/2'), ('phasor', 'a rotating vector whose projection on the vertical axis gives the instantaneous value')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c7s1_tf = tf_mcq('AC through R, L and C',
                 ['In a pure resistor, voltage and current are in phase.', 'Inductive reactance increases with frequency.', 'A capacitor blocks DC but passes AC.',
                  'The average power over a cycle in a pure inductor is zero.', 'AC voltmeters read rms values.'],
                 ['In a pure inductor the current leads the voltage by π/2.', 'Capacitive reactance increases with frequency.', 'An inductor blocks AC more at lower frequency.',
                  'AC voltmeters read peak values.', 'The rms value of an AC current is I₀√2.'])

c7s1_explain = pool_txt([
    ('Why does a capacitor block DC but allow AC to pass?', 'X_C = 1/ωC is infinite for ω = 0 and finite for AC.', '2 marks.'),
    ('Why is the average power in a pure inductor zero over a complete cycle?', 'Current lags voltage by π/2; energy stored in one quarter-cycle is returned in the next, so ⟨P⟩ = V I cos 90° = 0.', '2 marks.'),
    ('What is meant by the rms value of an alternating current? Why is it used?', 'The steady current producing the same heat in a resistor; meters and ratings (e.g. 220 V) use it because power is computed simply.', '2 marks.'),
])

c7s1_ar = pool_ar([
    ('A capacitor offers infinite resistance to DC.', 'X_C = 1/(2πνC) and ν = 0 for DC.', 'a', 'R explains A.'),
    ('The current in a pure inductor lags the voltage by π/2.', 'The back emf L dI/dt balances the applied voltage.', 'a', 'R explains A.'),
    ('The average value of AC over a complete cycle is equal to its rms value.', 'The rms value of AC is I₀/√2.', 'd', 'A is false: the average over a cycle is zero; R is true.'),
])


def c7s1_rms(r):
    V0 = r.choice([100, 141, 200, 311, 340])
    return NUM(f'The peak value of an alternating voltage is {V0} V. Find its rms value.', V0 / math.sqrt(2), 'V', f'V_rms = V₀/√2 = {V0}/1.414 = {{ans}}.', wrongs=[V0 * math.sqrt(2), V0 / 2, 2 * V0 / math.pi], gap='G3')


def c7s1_res(r):
    V = r.choice([220, 230, 110])
    R = r.choice([20, 40, 50, 100])
    I = V / R
    return NUM2(f'A {R} Ω resistor is connected to a {V} V, 50 Hz AC supply. Find the rms current and the peak current.', (I, I * math.sqrt(2)), ('A', 'A'),
                f'I_rms = V_rms/R = {V}/{R} = {sig(I)} A (1); I₀ = √2 I_rms = {sig(I * math.sqrt(2))} A (1).', wrongs=[(I, I / math.sqrt(2)), (I * math.sqrt(2), I), (V * R, V * R * 1.414)])


def c7s1_XL(r):
    L = r.choice([0.1, 0.2, 0.44, 0.5, 1])
    V = r.choice([220, 230, 110])
    f = r.choice([50, 60])
    XL = 2 * math.pi * f * L
    return NUM2(f'A pure inductor of {g(L)} H is connected to a {V} V, {f} Hz supply. Find the inductive reactance and the rms current.', (XL, V / XL), ('Ω', 'A'),
                f'X_L = 2πνL = 2π × {f} × {g(L)} = {sig(XL)} Ω (1); I = V/X_L = {sig(V / XL)} A (1).', wrongs=[(f * L, V / (f * L)), (XL, V * XL), (1 / XL, V * XL)])


def c7s1_XC(r):
    Cv = r.choice([10, 15, 20, 50, 100])
    V = r.choice([220, 110, 230])
    f = r.choice([50, 60])
    XC = 1 / (2 * math.pi * f * Cv * 1e-6)
    return NUM2(f'A {Cv} μF capacitor is connected to a {V} V, {f} Hz supply. Find the capacitive reactance and the rms current.', (XC, V / XC), ('Ω', 'A'),
                f'X_C = 1/(2πνC) = 1/(2π × {f} × {g(Cv * 1e-6)}) = {sig(XC)} Ω (1); I = V/X_C = {sig(V / XC)} A (1).', wrongs=[(2 * math.pi * f * Cv * 1e-6, V * 2 * math.pi * f * Cv * 1e-6 * 1e3), (XC * 2 * math.pi, V / XC / (2 * math.pi)), (XC, V * XC)])


def c7s1_freq(r):
    k = r.choice([2, 3, 4])
    el = r.choice(['an inductor', 'a capacitor'])
    f = k if el == 'an inductor' else 1 / k
    return NUM(f'The frequency of the AC supply connected to {el} is made {k} times, the rms voltage staying the same. By what factor does the rms current change?', 1 / f, '',
               f'{"X_L = ωL becomes " + str(k) + " times" if el == "an inductor" else "X_C = 1/ωC becomes 1/" + str(k)}; I = V/X, so the current factor is {{ans}}.', wrongs=[f, 1.0, f * f], gap='G3')


def c7s1_eqn(r):
    V0 = r.choice([100, 200, 300, 311])
    w = r.choice([100 * math.pi, 120 * math.pi, 314])
    wn = {100 * math.pi: '100π', 120 * math.pi: '120π', 314: '314'}[w]
    R = r.choice([10, 20, 50])
    f = w / (2 * math.pi)
    return NUM2(f'The voltage across a {R} Ω resistor is v = {V0} sin({wn}t) volt. Find (i) the frequency, (ii) the rms voltage and (iii) the rms current.', (f, V0 / math.sqrt(2), V0 / math.sqrt(2) / R), ('Hz', 'V', 'A'),
                f'(i) ω = {wn} rad s⁻¹ ⇒ ν = ω/2π = {sig(f)} Hz (1). (ii) V_rms = V₀/√2 = {sig(V0 / math.sqrt(2))} V (1). (iii) I_rms = V_rms/R = {sig(V0 / math.sqrt(2) / R)} A (1).',
                wrongs=[(w, V0 / math.sqrt(2), V0 / R), (f, V0 * 1.0, V0 / R), (f, V0 / 2, V0 / 2 / R)], sep='; ')


# st2 LCR, impedance, resonance

c7s2_terms = term_mcq([('impedance of a series LCR circuit', 'Z = √[R² + (X_L − X_C)²]'), ('resonant frequency', 'ω₀ = 1/√(LC)'),
                       ('quality factor', 'Q = ω₀L/R, a measure of the sharpness of resonance'), ('current at resonance', 'V/R, the maximum value'),
                       ('phase angle of a series LCR circuit', 'tan φ = (X_L − X_C)/R')],
                      'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c7s2_tf = tf_mcq('the series LCR circuit',
                 ['At resonance, X_L = X_C and the impedance equals R.', 'At resonance the current is maximum.', 'A smaller R gives a sharper resonance.',
                  'The voltages across L and C at resonance can be larger than the supply voltage.', 'Above resonance, the circuit is inductive.'],
                 ['At resonance the impedance is maximum.', 'At resonance the current is minimum.', 'A larger R gives a sharper resonance.',
                  'Resonance is possible in an RL circuit without a capacitor.', 'Below resonance, the circuit is inductive.'])

c7s2_explain = pool_txt([
    ('What is resonance in a series LCR circuit? Draw the variation of current with frequency.', 'At ω₀ = 1/√(LC), X_L = X_C, Z = R and the current is maximum; the curve peaks at ω₀, sharper for small R.', '2 marks.'),
    ('How is a radio tuned to a particular station?', 'The capacitance of the LC circuit is varied until its resonant frequency equals the station\'s frequency, giving maximum current for that signal.', '2 marks.'),
    ('Why can the voltage across the inductor in a series LCR circuit be larger than the supply voltage?', 'V_L = IX_L and V_C = IX_C are 180° out of phase and cancel; each can exceed V when Q > 1.', '2 marks.'),
])

c7s2_ar = pool_ar([
    ('At resonance a series LCR circuit behaves as a purely resistive circuit.', 'X_L = X_C at resonance.', 'a', 'R explains A.'),
    ('The sharpness of resonance increases as the resistance decreases.', 'Q = ω₀L/R.', 'a', 'R explains A.'),
    ('Resonance can occur in a circuit containing only R and L.', 'Resonance requires X_L = X_C.', 'd', 'A is false: both L and C are needed; R is true.'),
])


def c7s2_Z(r):
    R = r.choice([30, 40, 60, 80])
    XL = r.choice([50, 80, 100, 120])
    XC = r.choice([20, 40, 50, 60])
    Z = math.sqrt(R * R + (XL - XC) ** 2)
    return NUM(f'In a series LCR circuit, R = {R} Ω, X_L = {XL} Ω and X_C = {XC} Ω. Find the impedance.', Z, 'Ω', f'Z = √[R² + (X_L − X_C)²] = √[{R}² + {XL - XC}²] = {{ans}}.',
               wrongs=[R + XL - XC, math.sqrt(R * R + XL * XL + XC * XC), math.sqrt(R * R + (XL + XC) ** 2)], gap='G3')


def c7s2_f0(r):
    L = r.choice([0.1, 0.2, 0.5, 1, 2, 5]) * r.choice([1, 1e-3])
    Cv = r.choice([10, 20, 50, 100]) * r.choice([1e-6, 1e-12])
    f0 = 1 / (2 * math.pi * math.sqrt(L * Cv))
    return NUM(f'Find the resonant frequency of a series circuit with L = {g(L)} H and C = {g(Cv)} F.', f0, 'Hz', f'ν₀ = 1/(2π√(LC)) = 1/(2π√({g(L)} × {g(Cv)})) = {{ans}}.',
               wrongs=[1 / math.sqrt(L * Cv), 1 / (2 * math.pi * L * Cv), f0 * 2], gap='G3')


def c7s2_full(r):
    R = r.choice([10, 20, 40, 50])
    L = r.choice([0.1, 0.2, 0.5])
    Cv = r.choice([20, 50, 100])
    V = r.choice([200, 220, 230])
    f = 50
    XL = 2 * math.pi * f * L
    XC = 1 / (2 * math.pi * f * Cv * 1e-6)
    Z = math.sqrt(R * R + (XL - XC) ** 2)
    I = V / Z
    ph = math.degrees(math.atan((XL - XC) / R))
    nature = 'current lags the voltage' if XL > XC else 'current leads the voltage'
    return NUM2(f'A series LCR circuit with R = {R} Ω, L = {g(L)} H and C = {Cv} μF is connected to a {V} V, 50 Hz supply. Find the impedance, the rms current and the phase angle between voltage and current.',
                (Z, I, abs(ph)), ('Ω', 'A', '°'), f'X_L = {sig(XL)} Ω, X_C = {sig(XC)} Ω (1); Z = {sig(Z)} Ω (1.5); I = V/Z = {sig(I)} A (1); tan φ = (X_L − X_C)/R ⇒ |φ| = {sig(abs(ph))}°, {nature} (1.5).',
                wrongs=[(R + XL + XC, V / (R + XL + XC), 45.0), (Z, V / R, abs(ph)), (math.sqrt(R * R + XL * XL), V / math.sqrt(R * R + XL * XL), math.degrees(math.atan(XL / R)))], gap='G5')


def c7s2_resI(r):
    R = r.choice([5, 10, 20])
    L = r.choice([0.1, 0.5, 1])
    Cv = r.choice([10, 40, 100])
    V = r.choice([10, 20, 50, 100])
    w0 = 1 / math.sqrt(L * Cv * 1e-6)
    I = V / R
    VL = I * w0 * L
    return NUM2(f'A series LCR circuit with R = {R} Ω, L = {g(L)} H, C = {Cv} μF is connected to a variable-frequency {V} V source. At resonance, find the angular frequency, the rms current, and the rms voltage across the inductor.', (w0, I, VL), ('rad s⁻¹', 'A', 'V'),
                f'ω₀ = 1/√(LC) = {sig(w0)} rad s⁻¹ (1); I = V/R = {sig(I)} A (1); V_L = Iω₀L = {sig(VL)} V (1), equal to V_C and much larger than V.',
                wrongs=[(w0 / (2 * math.pi), I, VL / (2 * math.pi)), (w0, V / (R + w0 * L), float(V)), (w0, I, float(V))])


def c7s2_Q(r):
    R = r.choice([2, 5, 10, 20])
    L = r.choice([0.1, 0.2, 0.5, 1])
    Cv = r.choice([1, 2, 5, 10])
    w0 = 1 / math.sqrt(L * Cv * 1e-6)
    Q = w0 * L / R
    return NUM(f'Find the quality factor Q of a series LCR circuit with R = {R} Ω, L = {g(L)} H and C = {Cv} μF.', Q, '', f'ω₀ = 1/√(LC) = {sig(w0)} rad s⁻¹; Q = ω₀L/R = {{ans}}.',
               wrongs=[R / (w0 * L), w0 * L, Q * 2 * math.pi])


def c7s2_tune(r):
    L = r.choice([1, 2, 5, 10]) * 1e-6
    f = r.choice([0.8, 1, 1.2, 1.5]) * 1e6
    Cv = 1 / ((2 * math.pi * f) ** 2 * L)
    return NUM(f'A radio receiver uses a coil of inductance {g(L * 1e6)} μH. What capacitance is needed to tune it to a station broadcasting at {g(f / 1e6)} MHz?', Cv, 'F',
               f'ν = 1/(2π√(LC)) ⇒ C = 1/(4π²ν²L) (2) = 1/(4π² × ({g(f)})² × {g(L)}) = {{ans}} (1).', wrongs=[1 / (f * f * L), 1 / (2 * math.pi * f * L), Cv * 2 * math.pi], gap='G5')


c7s2_derive = pool_txt([
    ('Using a phasor diagram, derive an expression for the impedance of a series LCR circuit and the phase angle.', 'Z = √[R² + (X_L − X_C)²]; tan φ = (X_L − X_C)/R',
     'Phasors V_R along I, V_L leading, V_C lagging (2); resultant (2); phase (1).'),
    ('Derive the condition for resonance in a series LCR circuit and find the resonant frequency.', 'X_L = X_C ⇒ ω₀ = 1/√(LC)', 'Impedance minimum (2); ω₀L = 1/ω₀C (2); ν₀ = 1/(2π√LC) (1).'),
])


def c7s2_case(r):
    who = name(r)
    L = r.choice([1, 2, 4]) * 1e-6
    f1, f2 = r.choice([(0.6e6, 1.5e6), (0.8e6, 1.6e6), (0.55e6, 1.6e6)])
    c1 = 1 / ((2 * math.pi * f1) ** 2 * L)
    c2 = 1 / ((2 * math.pi * f2) ** 2 * L)
    return {'stem': (f'{who} is studying the tuning circuit of an old AM radio. The coil has inductance {g(L * 1e6)} μH and a variable capacitor is used to tune stations from {g(f1 / 1e6)} MHz to {g(f2 / 1e6)} MHz.\n'
                     '(i) What is the condition for maximum current for a station? (ii) What capacitance is needed for the lowest frequency? (iii) For the highest frequency? (iv) Why should the resistance of the circuit be small?'),
            'answer': f'(i) resonance: X_L = X_C (ii) {sig(c1)} F (iii) {sig(c2)} F (iv) for a sharp resonance (high Q), so nearby stations are rejected',
            'key': '(i) ω = 1/√(LC) (1). (ii) C = 1/(4π²ν²L) (1). (iii) same (1). (iv) Q = ω₀L/R (1).'}


# st3 power, power factor, wattless current

c7s3_terms = term_mcq([('average power in an AC circuit', 'P = V_rms I_rms cos φ'), ('power factor', 'cos φ = R/Z'), ('wattless current', 'the component I sin φ, which consumes no power'),
                       ('power factor of a pure resistor', '1'), ('power factor of a pure inductor or capacitor', '0')],
                      'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c7s3_tf = tf_mcq('power in AC circuits',
                 ['A pure inductor consumes no average power.', 'Power factor is 1 at resonance in a series LCR circuit.', 'A choke coil limits current with very little power loss.',
                  'Low power factor in supply lines increases line losses.'],
                 ['A pure capacitor consumes maximum power.', 'Power factor can be greater than 1.', 'A resistor is preferred to a choke for limiting AC current because it wastes no energy.',
                  'Power factor at resonance is zero.'])

c7s3_explain = pool_txt([
    ('What is wattless current? When does it arise?', 'The current component in quadrature with voltage (I sin φ); average power due to it is zero; it arises in inductive or capacitive circuits.', '2 marks.'),
    ('Why is a choke coil preferred to a resistor for reducing current in AC circuits (e.g. tube lights)?', 'The choke has large reactance but little resistance, so it limits current while consuming almost no power.', '2 marks.'),
    ('Why do industries install capacitors in parallel with their inductive loads?', 'To raise the power factor towards 1, reducing the current and line losses for the same power.', '2 marks.'),
])

c7s3_ar = pool_ar([
    ('The power factor of a series LCR circuit at resonance is 1.', 'At resonance, Z = R so cos φ = R/Z = 1.', 'a', 'R explains A.'),
    ('No power is consumed in a purely capacitive AC circuit.', 'Current and voltage are π/2 out of phase.', 'a', 'cos 90° = 0; R explains A.'),
    ('A choke coil wastes a lot of energy as heat.', 'A choke coil has large inductance and small resistance.', 'd', 'A is false; R is true.'),
])


def c7s3_P(r):
    V = r.choice([220, 230, 110])
    I = r.choice([1, 2, 2.5, 4, 5])
    pf = r.choice([0.5, 0.6, 0.8, 0.9, 1])
    return NUM(f'In an AC circuit the rms voltage is {V} V, the rms current is {g(I)} A and the power factor is {g(pf)}. Find the average power consumed.', V * I * pf, 'W',
               f'P = V_rms I_rms cos φ = {V} × {g(I)} × {g(pf)} = {{ans}}.', wrongs=[V * I, V * I / pf, V * I * pf * 2], gap='G3')


def c7s3_pf(r):
    R = r.choice([30, 40, 60, 80])
    X = r.choice([30, 40, 60, 80])
    Z = math.sqrt(R * R + X * X)
    return NUM(f'A coil has resistance {R} Ω and inductive reactance {X} Ω at the supply frequency. Find its power factor.', R / Z, '', f'Z = √(R² + X_L²) = {sig(Z)} Ω; cos φ = R/Z = {{ans}}.',
               wrongs=[X / Z, R / X, Z / R], n=3)


def c7s3_full(r):
    R = r.choice([20, 30, 40])
    XL = r.choice([60, 80, 100])
    XC = r.choice([20, 30, 40])
    V = r.choice([200, 220])
    Z = math.sqrt(R * R + (XL - XC) ** 2)
    I = V / Z
    pf = R / Z
    P = V * I * pf
    return NUM2(f'A series circuit has R = {R} Ω, X_L = {XL} Ω and X_C = {XC} Ω, and is connected to a {V} V AC supply. Find the power factor and the average power consumed. Show that this equals I²R.', (pf, P), ('', 'W'),
                f'Z = {sig(Z)} Ω (1); cos φ = R/Z = {sig(pf)} (1); I = V/Z = {sig(I)} A; P = VI cos φ = {sig(P)} W = I²R (1).', wrongs=[(1.0, V * V / R), (pf, V * I), ((XL - XC) / Z, P)], gap='G5')


def c7s3_choke(r):
    Vs = 220
    VR, P = r.choice([(110, 60), (100, 40), (120, 60), (110, 100)])
    I = P / VR
    XL = math.sqrt(Vs * Vs - VR * VR) / I
    L = XL / (2 * math.pi * 50)
    return NUM(f'A lamp rated {VR} V, {P} W is to be run on a 220 V, 50 Hz supply using a pure inductor (choke) in series. Find the inductance required.', L, 'H',
               f'I = P/V = {sig(I)} A (1); V_L = √(220² − {VR}²) = {sig(math.sqrt(Vs * Vs - VR * VR))} V (1); X_L = V_L/I = {sig(XL)} Ω (1); L = X_L/(2π × 50) = {{ans}} (1). No power is wasted in the choke.',
               wrongs=[(Vs - VR) / I / (2 * math.pi * 50), XL, L * 2 * math.pi], gap='G5')


c7s3_mcq = pool_mcq([
    ('The average power consumed over a cycle in a pure inductor connected to AC is', 'zero', ['V_rms I_rms', 'V₀I₀', 'V₀I₀/2'], 'cos 90° = 0.'),
    ('The power factor of an AC circuit having only resistance is', '1', ['0', '0.5', '1/√2'], 'φ = 0.'),
    ('The current in an AC circuit is wattless when the phase difference between current and voltage is', '90°', ['0°', '45°', '180°'], 'P = VI cos 90° = 0.'),
    ('Power factor of a series LCR circuit is maximum when', 'X_L = X_C', ['X_L > X_C', 'X_L < X_C', 'R = 0'], 'Resonance: Z = R.'),
])


# st4 transformers

c7s4_terms = term_mcq([('step-up transformer', 'N_s > N_p, gives a higher output voltage'), ('step-down transformer', 'N_s < N_p, gives a lower output voltage'),
                       ('turns ratio relation', 'V_s/V_p = N_s/N_p'), ('ideal transformer current relation', 'I_s/I_p = N_p/N_s'), ('copper loss', 'Joule heating I²R in the windings')],
                      'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c7s4_tf = tf_mcq('transformers',
                 ['A transformer works on the principle of mutual induction.', 'A transformer cannot work on steady DC.', 'In a step-up transformer the current in the secondary is less than in the primary.',
                  'Laminated cores reduce eddy current losses.'],
                 ['A transformer increases both voltage and current.', 'A transformer works on DC.', 'A step-up transformer increases power.', 'Thick wire is used for the high-voltage winding.'])

c7s4_explain = pool_txt([
    ('Why can\'t a transformer be used with a steady DC supply?', 'Steady DC gives constant flux, so no emf is induced in the secondary.', '2 marks.'),
    ('List four sources of energy loss in a transformer.', 'Flux leakage, copper (I²R) loss, eddy current loss, hysteresis loss.', '2 marks.'),
    ('Why is electrical power transmitted over long distances at high voltage using step-up transformers?', 'For the same power the current is lower, so I²R loss in the lines is much smaller.', '2 marks.'),
])

c7s4_ar = pool_ar([
    ('A transformer does not work on DC.', 'A transformer works on the principle of mutual induction, which needs a changing flux.', 'a', 'R explains A.'),
    ('A step-up transformer increases the power supplied.', 'In a step-up transformer V_s > V_p.', 'd', 'A is false: power is (at best) conserved; R is true.'),
    ('The low-voltage winding of a transformer is made of thicker wire.', 'The low-voltage winding carries a larger current.', 'a', 'R explains A.'),
])


def c7s4_ratio(r):
    Vp = r.choice([220, 230, 110, 11000])
    Np = r.choice([500, 1000, 2000, 4000])
    Ns = r.choice([50, 100, 200, 4000, 6000])
    Vs = Vp * Ns / Np
    return NUM(f'The primary of a transformer has {Np} turns and the secondary {Ns} turns. If the primary is connected to {Vp} V AC, find the secondary voltage. Is it step-up or step-down?', Vs, 'V',
               f'V_s = V_p N_s/N_p = {Vp} × {Ns}/{Np} = {{ans}}; {"step-up" if Ns > Np else "step-down"}.', wrongs=[Vp * Np / Ns, Vp * Ns, Vs * 2], gap='G3')


def c7s4_current(r):
    Vp = r.choice([220, 230])
    Vs = r.choice([6, 9, 12, 24])
    Is = r.choice([0.5, 1, 2, 5])
    Ip = Vs * Is / Vp
    return NUM(f'An ideal step-down transformer converts {Vp} V to {Vs} V. The secondary delivers {g(Is)} A to a load. Find the current in the primary.', Ip, 'A',
               f'Ideal: V_pI_p = V_sI_s ⇒ I_p = V_sI_s/V_p = {Vs} × {g(Is)}/{Vp} = {{ans}}.', wrongs=[Vp * Is / Vs, Is, Ip * 10])


def c7s4_eff(r):
    Vp, Ip = r.choice([(220, 2), (230, 4), (220, 5), (240, 3)])
    Vs, Is = r.choice([(12, 30), (24, 15), (110, 3.6), (440, 0.9)])
    Pin, Pout = Vp * Ip, Vs * Is
    if Pout >= Pin:
        raise ValueError
    return NUM(f'A transformer takes {Ip} A from a {Vp} V supply and delivers {g(Is)} A at {Vs} V. Find its efficiency.', 100 * Pout / Pin, '%',
               f'P_in = {Pin} W, P_out = {g(Pout)} W; η = P_out/P_in × 100 = {{ans}}.', wrongs=[100 * Pin / Pout, 100 * Vs / Vp, 100 * Is / Ip / 10])


def c7s4_line(r):
    P = r.choice([100, 200, 500, 800]) * 1e3
    R = r.choice([2, 4, 5, 10])
    V1 = r.choice([2200, 4000, 5000])
    V2 = V1 * r.choice([10, 20])
    L1 = (P / V1) ** 2 * R
    L2 = (P / V2) ** 2 * R
    return NUM2(f'A power of {g(P / 1000)} kW is transmitted through lines of total resistance {R} Ω. Find the power lost in the lines when it is transmitted at (i) {V1} V and (ii) {V2} V. Comment.', (L1, L2), ('W', 'W'),
                f'(i) I = P/V = {sig(P / V1)} A, loss I²R = {sig(L1)} W (2). (ii) I = {sig(P / V2)} A, loss = {sig(L2)} W (2): {V2 // V1}× voltage cuts the loss {(V2 // V1) ** 2}× (1).',
                wrongs=[(V1 ** 2 / R, V2 ** 2 / R), (P / V1 * R, P / V2 * R), (L1, L1 / (V2 / V1))], sep='; ', gap='G5')


def c7s4_turns(r):
    Vp = r.choice([220, 230])
    Vs = r.choice([6, 9, 11, 12, 22])
    Ns = r.choice([30, 40, 50, 60, 100])
    Np = Ns * Vp / Vs
    return NUM(f'A phone charger uses a transformer to step down {Vp} V to {Vs} V. If the secondary has {Ns} turns, how many turns should the primary have?', Np, '',
               f'N_p = N_s V_p/V_s = {Ns} × {Vp}/{Vs} = {{ans}}.', wrongs=[Ns * Vs / Vp, Np / 2, Np * 2], n=3)


def c7s4_case(r):
    who = name(r)
    city = r.choice(CITIES)
    P = r.choice([500, 800, 1000]) * 1e3
    V = r.choice([11000, 22000, 33000])
    R = r.choice([5, 10])
    I = P / V
    return {'stem': (f'A power station near {city} sends {g(P / 1000)} kW to a town at {V} V through lines of total resistance {R} Ω. At the town, a step-down transformer reduces the voltage to 220 V. {who} studies this arrangement.\n'
                     '(i) Find the current in the line. (ii) Find the power loss in the line. (iii) Find the turns ratio N_p : N_s of the step-down transformer. (iv) Why is the transformer core laminated?'),
            'answer': f'(i) {sig(I)} A (ii) {sig(I * I * R)} W (iii) {V // 220} : 1 (iv) to reduce eddy current losses',
            'key': '(i) I = P/V (1). (ii) I²R (1). (iii) V_p/V_s (1). (iv) eddy currents (1).'}


# ======================================================== ch08 Electromagnetic Waves
# st1 displacement current, sources

c8s1_terms = term_mcq([('displacement current', 'i_d = ε₀ dΦ_E/dt, due to a changing electric field'), ('Ampere-Maxwell law', '∮B·dl = μ₀(i_c + ε₀ dΦ_E/dt)'),
                       ('source of electromagnetic waves', 'an accelerated (oscillating) charge'), ('speed of light in vacuum', 'c = 1/√(μ₀ε₀)')],
                      'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c8s1_tf = tf_mcq('displacement current',
                 ['Displacement current exists between the plates of a charging capacitor.', 'Displacement current produces a magnetic field just like conduction current.',
                  'A charge moving with constant velocity does not radiate EM waves.', 'An oscillating charge produces EM waves of the same frequency.'],
                 ['Displacement current is due to flow of charges between capacitor plates.', 'Displacement current exists in a steady DC circuit after charging is complete.',
                  'A stationary charge radiates EM waves.', 'Displacement current produces no magnetic field.'])

c8s1_explain = pool_txt([
    ('Why did Maxwell introduce the idea of displacement current?', 'Ampere\'s law gave inconsistent results for a charging capacitor (different surfaces, same loop); adding ε₀ dΦ_E/dt made the current continuous.', '2 marks.'),
    ('Show that the displacement current between the plates of a charging capacitor equals the conduction current in the leads.', 'Φ_E = q/ε₀, so ε₀ dΦ_E/dt = dq/dt = i.', '2 marks.'),
])

c8s1_ar = pool_ar([
    ('A changing electric field produces a magnetic field.', 'Displacement current is a source of magnetic field in the Ampere-Maxwell law.', 'a', 'R explains A.'),
    ('An electron moving in a circle radiates electromagnetic waves.', 'An accelerated charge radiates electromagnetic waves.', 'a', 'R explains A.'),
    ('Displacement current flows in a capacitor connected to a steady DC source after it is fully charged.', 'Displacement current depends on the rate of change of electric flux.', 'd', 'A is false: E is steady, so i_d = 0; R is true.'),
])


def c8s1_id(r):
    Cv = r.choice([1, 2, 5, 10]) * 1e-9
    dv = r.choice([1, 2, 5, 10]) * 1e6
    i = Cv * dv
    return NUM(f'A capacitor of {g(Cv)} F is being charged so that the voltage across it rises at {g(dv)} V s⁻¹. Find the displacement current between its plates.', i, 'A',
               f'q = CV ⇒ i_d = dq/dt = C dV/dt = {g(Cv)} × {g(dv)} = {{ans}}, equal to the conduction current in the leads.', wrongs=[Cv / dv, dv / Cv, i * 2], gap='G3')


def c8s1_dE(r):
    A = r.choice([0.01, 0.02, 0.05, 0.1])
    dE = r.choice([1, 2, 5]) * 1e12
    i = E0 * A * dE
    return NUM(f'The electric field between the plates of a parallel plate capacitor of plate area {g(A)} m² changes at {g(dE)} V m⁻¹ s⁻¹. Find the displacement current.', i, 'A',
               f'i_d = ε₀ dΦ_E/dt = ε₀A dE/dt = 8.854 × 10⁻¹² × {g(A)} × {g(dE)} = {{ans}}.', wrongs=[A * dE, E0 * dE, i / A])


def c8s1_B(r):
    R = r.choice([5, 10, 12])
    rr = r.choice([2, 3, 4, 6])
    if rr >= R:
        rr = R // 2
    i = r.choice([0.1, 0.15, 0.2, 0.5])
    B = MU0 * i * (rr / 100) / (2 * math.pi * (R / 100) ** 2)
    return NUM(f'A parallel plate capacitor with circular plates of radius {R} cm is being charged by a current of {g(i)} A. Find the magnetic field between the plates at a distance {rr} cm from the axis (inside the plates).', B, 'T',
               f'The displacement current through a circle of radius r is i_d r²/R² (2); Ampere-Maxwell: B·2πr = μ₀i r²/R² (2) ⇒ B = μ₀ir/(2πR²) = {{ans}} (1).',
               wrongs=[MU0 * i / (2 * math.pi * rr / 100), MU0 * i / (2 * math.pi * R / 100), B * 2], gap='G5')


c8s1_mcq = pool_mcq([
    ('Electromagnetic waves are produced by', 'accelerated charges', ['charges at rest', 'charges moving with uniform velocity', 'neutral particles at rest'], 'Only accelerated charges radiate.'),
    ('The frequency of the EM wave radiated by a charge oscillating at frequency ν is', 'ν', ['2ν', 'ν/2', 'zero'], 'Same as the oscillation.'),
    ('Hertz first produced and detected', 'electromagnetic waves in the laboratory', ['X-rays', 'cathode rays', 'the photoelectric effect only'], 'Spark-gap experiments, 1887.'),
])


# st2 nature, spectrum

SPEC = [('radio waves', '> 0.1 m'), ('microwaves', '1 mm to 0.1 m'), ('infrared', '700 nm to 1 mm'), ('visible light', '400 nm to 700 nm'),
        ('ultraviolet', '1 nm to 400 nm'), ('X-rays', '1 nm to 10⁻³ nm'), ('gamma rays', '< 10⁻³ nm')]

c8s2_terms = term_mcq(SPEC, 'The approximate wavelength range of {a} is', 'Which part of the spectrum has wavelengths {b}?', '{a}: {b}.')

c8s2_tf = tf_mcq('electromagnetic waves',
                 ['Electromagnetic waves are transverse.', 'In an EM wave, E and B are in phase and perpendicular to each other.', 'EM waves do not need a medium.',
                  'E₀/B₀ = c in vacuum.', 'All EM waves travel at the same speed in vacuum.'],
                 ['Electromagnetic waves are longitudinal.', 'In an EM wave, E and B are 90° out of phase.', 'EM waves need a material medium.',
                  'X-rays travel faster than radio waves in vacuum.', 'E and B in an EM wave are parallel.'])

c8s2_explain = pool_txt([
    ('State four properties of electromagnetic waves.', 'Transverse; E ⟂ B ⟂ direction of travel; speed c = 1/√μ₀ε₀ in vacuum; no medium needed; carry energy and momentum.', '2 marks.'),
    ('How is the speed of an EM wave in a medium related to its permittivity and permeability?', 'v = 1/√(με); refractive index n = √(μᵣεᵣ).', '2 marks.'),
])

c8s2_ar = pool_ar([
    ('Electromagnetic waves are transverse.', 'E and B oscillate perpendicular to the direction of propagation.', 'a', 'R explains A.'),
    ('Electromagnetic waves can travel through vacuum.', 'They are self-sustaining oscillations of electric and magnetic fields.', 'a', 'R explains A.'),
    ('Gamma rays travel faster than visible light in vacuum.', 'Gamma rays have higher frequency than visible light.', 'd', 'A is false; R is true.'),
])


def c8s2_order(r):
    idx = sorted(r.sample(range(len(SPEC)), 4))
    names = [SPEC[i][0] for i in idx]
    inc_f = r.random() < 0.5
    if inc_f:
        stem = 'Arrange in increasing order of frequency:'
        right = ' < '.join(names)  # SPEC is in decreasing wavelength order, so increasing frequency
    else:
        stem = 'Arrange in increasing order of wavelength:'
        right = ' < '.join(reversed(names))
    perms = set()
    while len(perms) < 3:
        p = names[:]
        r.shuffle(p)
        s = ' < '.join(p)
        if s != right:
            perms.add(s)
    return mcq(f'{stem} {", ".join(sorted(names))}.', right, list(perms), f'Wavelength decreases (frequency increases) from radio waves to gamma rays: {right}.', r)


def c8s2_lam(r):
    f = r.choice([1, 2.4, 5, 100, 98.3, 600]) * r.choice([1e6, 1e9])
    lam = C / f
    return NUM(f'Find the wavelength of an electromagnetic wave of frequency {g(f)} Hz in vacuum.', lam, 'm', f'λ = c/ν = 3 × 10⁸/{g(f)} = {{ans}}.', wrongs=[f / C, C * f, lam * 10], gap='G3')


def c8s2_B0(r):
    E_0 = r.choice([3, 6, 12, 30, 48, 120])
    B0 = E_0 / C
    return NUM(f'The peak electric field of a plane EM wave in vacuum is {E_0} V m⁻¹. Find the peak magnetic field.', B0, 'T', f'B₀ = E₀/c = {E_0}/(3 × 10⁸) = {{ans}}.', wrongs=[E_0 * C, E_0 / C ** 2, B0 * 2 * math.pi])


def c8s2_wave(r):
    E_0 = r.choice([30, 48, 60, 120])
    k = r.choice([1, 2, 5, 10, 20])
    w = k * C
    lam = 2 * math.pi / k
    f = w / (2 * math.pi)
    return NUM2(f'The electric field of a plane EM wave in vacuum is E_y = {E_0} sin({g(k)}x − {g(w)}t) V m⁻¹ (SI units). Find (i) the wavelength, (ii) the frequency and (iii) the amplitude of the magnetic field, and state its direction.',
                (lam, f, E_0 / C), ('m', 'Hz', 'T'), f'(i) λ = 2π/k = {sig(lam)} m (1). (ii) ν = ω/2π = {sig(f)} Hz (1). (iii) B₀ = E₀/c = {sig(E_0 / C)} T, along z (1).',
                wrongs=[(1 / k, w, E_0 * C), (lam, w, E_0 / C), (2 * lam, f / 2, E_0 / C)], sep='; ')


def c8s2_medium(r):
    er = r.choice([2.25, 4, 1.69, 2.56])
    n = math.sqrt(er)
    return NUM2(f'Find the speed of an EM wave and the refractive index of a non-magnetic medium (μᵣ = 1) whose relative permittivity is {g(er)}.', (C / n, n), ('m s⁻¹', ''),
                f'v = c/√(μᵣεᵣ) = 3 × 10⁸/√{g(er)} = {sig(C / n)} m s⁻¹ (1); n = c/v = {sig(n)} (1).', wrongs=[(C / er, er), (C * n, 1 / n), (C, 1.0)])


# st3 uses

USES = [('radio waves', 'radio and TV broadcasting, mobile phones'), ('microwaves', 'radar and microwave ovens'), ('infrared waves', 'TV remote controls and physical therapy'),
        ('visible light', 'vision and photography'), ('ultraviolet rays', 'killing germs in water purifiers and LASIK eye surgery'), ('X-rays', 'diagnosing bone fractures'),
        ('gamma rays', 'treating cancer and in nuclear medicine')]

c8s3_uses = term_mcq(USES, 'A typical use of {a} is', 'Which part of the EM spectrum is used for {b}?', '{a}: {b}.')

c8s3_tf = tf_mcq('the uses of EM waves',
                 ['The ozone layer absorbs most of the Sun\'s ultraviolet radiation.', 'Infrared radiation keeps the Earth warm (greenhouse effect).', 'Microwave ovens heat food by making water molecules vibrate.',
                  'X-rays are produced when fast electrons hit a metal target.'],
                 ['Gamma rays are used in TV remote controls.', 'Radio waves are produced by radioactive nuclei.', 'Infrared rays are used to kill germs in water purifiers.',
                  'X-rays have longer wavelength than microwaves.'])

c8s3_explain = pool_txt([
    ('Why is the ozone layer important for life on Earth?', 'It absorbs most of the harmful ultraviolet radiation from the Sun.', '2 marks.'),
    ('Why are infrared rays sometimes called heat waves?', 'They are readily absorbed by water molecules and many substances, raising their internal energy (temperature).', '2 marks.'),
    ('Why are microwaves suitable for radar and satellite communication?', 'Short wavelength gives a narrow beam and they pass through the atmosphere/ionosphere.', '2 marks.'),
])

c8s3_ar = pool_ar([
    ('Welders wear special goggles.', 'Welding arcs produce intense UV radiation.', 'a', 'R explains A.'),
    ('Microwave ovens use frequencies that match the resonant frequency of water molecules.', 'Energy is then absorbed efficiently by the water in food.', 'a', 'R explains A.'),
    ('Radio waves are used to see bone fractures.', 'Radio waves have long wavelengths.', 'd', 'A is false: X-rays are used; R is true.'),
])


def c8s3_region(r):
    lam, reg = r.choice([(500e-9, 'visible light'), (10e-6, 'infrared'), (3e-2, 'microwaves'), (200e-9, 'ultraviolet'), (0.1e-9, 'X-rays'), (100, 'radio waves'), (1e-13, 'gamma rays')])
    others = [x[0] for x in SPEC if x[0] != reg]
    return mcq(f'An electromagnetic wave has a wavelength of {g(lam)} m. To which part of the spectrum does it belong?', reg, r.sample(others, 3), f'{g(lam)} m lies in the {reg} range.', r)


def c8s3_station(r):
    f = r.choice([91.1, 93.5, 98.3, 104.8, 106.4])
    lam = C / (f * 1e6)
    return NUM(f'An FM radio station in {r.choice(CITIES)} broadcasts at {g(f)} MHz. Find the wavelength of its waves. To which band of the spectrum do they belong?', lam, 'm',
               f'λ = c/ν = 3 × 10⁸/({g(f)} × 10⁶) = {{ans}}: radio waves.', wrongs=[lam * 10, lam / 10, f / 3], gap='G3')


def c8s3_case(r):
    who = name(r)
    return {'stem': (f'{who} lists everyday devices: (a) a TV remote control, (b) a microwave oven, (c) an airport baggage scanner, (d) a UV water purifier.\n'
                     '(i) Name the part of the EM spectrum used in each. (ii) Arrange them in increasing order of frequency. (iii) Which of these has the highest energy photons? (iv) Why must exposure to (c) be limited?'),
            'answer': '(i) (a) infrared (b) microwaves (c) X-rays (d) ultraviolet (ii) microwaves < infrared < ultraviolet < X-rays (iii) X-rays (iv) X-rays can damage living tissue/cells',
            'key': '(i) (1). (ii) (1). (iii) (1). (iv) ionising radiation (1).'}


# ======================================================== ch09 Ray Optics
# st1 mirrors

c9s1_terms = term_mcq([('mirror equation', '1/v + 1/u = 1/f'), ('magnification by a mirror', 'm = −v/u'), ('focal length of a spherical mirror', 'f = R/2'),
                       ('Cartesian sign convention', 'distances measured from the pole; along the incident light positive'), ('image by a convex mirror', 'always virtual, erect and diminished')],
                      'Which of the following gives {a}?', 'Which term is {b}?', '{a}: {b}.')

c9s1_tf = tf_mcq('spherical mirrors',
                 ['A convex mirror always forms a virtual, erect, diminished image.', 'A concave mirror forms a virtual image when the object is between F and P.', 'f = R/2 for small apertures.',
                  'Convex mirrors are used as rear-view mirrors.'],
                 ['A convex mirror can form a real image of a real object.', 'A concave mirror always forms a real image.', 'f = 2R for a spherical mirror.',
                  'Concave mirrors give a wider field of view than convex mirrors.'])

c9s1_explain = pool_txt([
    ('Why are convex mirrors used as rear-view mirrors in vehicles?', 'They always give an erect, diminished image and a wide field of view.', '2 marks.'),
    ('Why does a dentist use a concave mirror?', 'With the tooth inside the focal length, it gives an enlarged, erect, virtual image.', '2 marks.'),
    ('Does the focal length of a mirror depend on the medium in which it is placed? Explain.', 'No; reflection does not depend on refractive index, so f = R/2 is unchanged.', '2 marks.'),
])

c9s1_ar = pool_ar([
    ('A convex mirror always forms a virtual image of a real object.', 'Reflected rays from a convex mirror always diverge.', 'a', 'R explains A.'),
    ('The focal length of a mirror does not change when it is immersed in water.', 'Laws of reflection do not depend on the medium.', 'a', 'R explains A.'),
    ('A concave mirror cannot form a magnified image.', 'A concave mirror converges parallel rays.', 'd', 'A is false: magnified images form for objects within 2F; R is true.'),
])


def c9s1_mirror(r):
    f = r.choice([10, 12, 15, 20])
    u = r.choice([15, 18, 25, 30, 40, 50])
    if u == f:
        u += 5
    v = 1 / (1 / (-f) - 1 / (-u))
    m = -v / (-u)
    nature = 'real, inverted' if v < 0 else 'virtual, erect'
    return NUM2(f'An object is placed {u} cm in front of a concave mirror of focal length {f} cm. Find the image position and magnification (use the Cartesian sign convention).', (v, m), ('cm', ''),
                f'1/v = 1/f − 1/u = 1/(−{f}) − 1/(−{u}) ⇒ v = {sig(v)} cm (1.5); m = −v/u = {sig(m)}: {nature} (1.5).', wrongs=[(-v, -m), (v, -m), (1 / (1 / f + 1 / u), m)])


def c9s1_convex(r):
    f = r.choice([15, 20, 25, 30])
    u = r.choice([10, 20, 30, 45, 60])
    v = 1 / (1 / f + 1 / u)
    m = v / u
    return NUM2(f'A convex rear-view mirror has a radius of curvature of {2 * f} cm. An object is {u} cm in front of it. Find the image position and magnification.',
                (v, m), ('cm', ''), f'f = R/2 = +{f} cm (1); 1/v = 1/f − 1/u = 1/{f} + 1/{u} ⇒ v = +{sig(v)} cm (behind the mirror) (1); m = −v/u = +{sig(m)}: virtual, erect, diminished (1).',
                wrongs=[(-v, -m), (1 / (1 / f - 1 / u) if u != f else v * 2, m), (v, -m)])


def c9s1_magn(r):
    f = r.choice([10, 15, 20, 24])
    m = r.choice([-2, -3, 2, 3, -0.5])
    # m = -v/u, 1/v + 1/u = 1/f with f negative (concave)
    u = (-f) * (m - 1) / m  # from m = -v/u and 1/v + 1/u = 1/F with F = -f
    return NUM(f'A concave mirror of focal length {f} cm forms an image that is {"real and" if m < 0 else "virtual and"} {g(abs(m))} times the size of the object. Find the object distance.', abs(u), 'cm',
               f'm = −v/u = {g(m)} ⇒ v = {g(-m)}u (1); 1/v + 1/u = 1/f (f = −{f}) ⇒ u = f(m − 1)/m (1) = {sig(u)} cm, i.e. {{ans}} in front of the mirror (1).',
               wrongs=[abs((-f) * (m + 1) / m), abs(f * m), abs(f / m)], gap='G5')


def c9s1_fR(r):
    R = r.choice([20, 24, 30, 40, 50])
    return NUM(f'Find the focal length of a spherical mirror of radius of curvature {R} cm.', R / 2, 'cm', f'f = R/2 = {{ans}}.', wrongs=[2 * R, R, R / 4], gap='G3', n=2)


c9s1_derive = pool_txt([
    ('Derive the mirror equation 1/v + 1/u = 1/f for a concave mirror forming a real image.', '1/v + 1/u = 1/f', 'Ray diagram (1); similar triangles (2); f = R/2 and sign convention (2).'),
    ('Derive the relation f = R/2 for a spherical mirror of small aperture.', 'f = R/2', 'Paraxial ray, angle of incidence θ (2); CF = FP for small θ (2); result (1).'),
])


# st2 refraction, TIR, spherical surfaces, lens maker

c9s2_terms = term_mcq([('critical angle', 'the angle of incidence in the denser medium for which the angle of refraction is 90°'), ('total internal reflection', 'complete reflection of light at a denser-to-rarer interface for i > C'),
                       ('lens maker\'s formula', '1/f = (n − 1)(1/R₁ − 1/R₂)'), ('power of a lens', 'P = 1/f (f in metres), unit dioptre'),
                       ('refraction at a spherical surface', 'n₂/v − n₁/u = (n₂ − n₁)/R')],
                      'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c9s2_tf = tf_mcq('refraction and lenses',
                 ['Total internal reflection needs light to travel from a denser to a rarer medium.', 'Optical fibres work on total internal reflection.', 'The power of a convex lens is positive.',
                  'A convex lens of glass acts as a diverging lens in a liquid of higher refractive index.', 'Apparent depth = real depth/n for viewing from above.'],
                 ['Total internal reflection can occur when light goes from rarer to denser medium.', 'The power of a concave lens is positive.', 'Diamond sparkles because of its low refractive index.',
                  'The focal length of a lens is the same in all media.', 'Apparent depth is greater than real depth for a pond viewed from above.'])

c9s2_explain = pool_txt([
    ('Why does a diamond sparkle?', 'Its large n (≈2.42) gives a small critical angle (≈24°), so light undergoes repeated total internal reflection before emerging.', '2 marks.'),
    ('Why does a swimming pool appear shallower than it is?', 'Light from the bottom bends away from the normal at the surface; the eye sees an image at depth h/n.', '2 marks.'),
    ('Explain how an optical fibre transmits light with very little loss.', 'Light enters at an angle so that it strikes the core-cladding boundary at more than the critical angle; repeated TIR guides it.', '2 marks.'),
    ('Why does a mirage appear on a hot road?', 'Air near the road is hotter and less dense (lower n); light from the sky bends and undergoes TIR, appearing as reflection from water.', '2 marks.'),
])

c9s2_ar = pool_ar([
    ('A convex lens made of glass (n = 1.5) behaves as a diverging lens in carbon disulphide (n = 1.63).', 'The lens is then optically rarer than its surroundings.', 'a', 'R explains A.'),
    ('Optical fibres transmit light by total internal reflection.', 'The core has a higher refractive index than the cladding.', 'a', 'R explains A.'),
    ('Total internal reflection can occur when light goes from air into glass.', 'Critical angle depends on the refractive index.', 'd', 'A is false: needs denser to rarer; R is true.'),
])


def c9s2_snell(r):
    n = r.choice([1.33, 1.5, 1.6, 1.44])
    i = r.choice([30, 40, 45, 50, 60])
    rr = math.degrees(math.asin(math.sin(math.radians(i)) / n))
    return NUM(f'A ray of light in air strikes a surface of a medium of refractive index {g(n)} at {i}°. Find the angle of refraction.', rr, '°',
               f'sin r = sin i/n = sin {i}°/{g(n)} = {num(math.sin(math.radians(i)) / n, 4)} ⇒ r = {{ans}}.', wrongs=[i / n, math.degrees(math.asin(min(1, math.sin(math.radians(i)) * n / 2))), i * n], gap='G3')


def c9s2_depth(r):
    h = r.choice([1, 1.5, 2, 3, 4])
    n = r.choice([1.33, 4 / 3])
    ap = h / n
    return NUM(f'A coin lies at the bottom of a tank filled with water (n = 4/3) to a depth of {g(h)} m. How far is the coin apparently raised when viewed from directly above?', h - h * 3 / 4, 'm',
               f'Apparent depth = h/n = {g(h)} × 3/4 = {sig(h * 0.75)} m; rise = h − h/n = {{ans}}.', wrongs=[h * 0.75, h * 4 / 3 - h, h / 3], n=3)


def c9s2_critical(r):
    n = r.choice([1.33, 1.5, 1.6, 2.42, 1.414])
    Cc = math.degrees(math.asin(1 / n))
    return NUM(f'Find the critical angle for light going from a medium of refractive index {g(n)} to air.', Cc, '°', f'sin C = 1/n = 1/{g(n)} = {num(1 / n, 4)} ⇒ C = {{ans}}.',
               wrongs=[math.degrees(math.acos(1 / n)), 90 / n, math.degrees(math.atan(1 / n))])


def c9s2_lens(r):
    f = r.choice([10, 15, 20, 25]) * r.choice([1, -1])
    u = -r.choice([15, 20, 30, 40, 60])
    if abs(1 / f + 1 / u) < 1e-9:
        raise ValueError
    v = 1 / (1 / f + 1 / u)
    m = v / u
    kind = 'convex' if f > 0 else 'concave'
    return NUM2(f'An object is placed {-u} cm in front of a {kind} lens of focal length {abs(f)} cm. Find the position and magnification of the image.', (v, m), ('cm', ''),
                f'1/v − 1/u = 1/f ⇒ 1/v = 1/{f} + 1/({u}) ⇒ v = {sig(v)} cm (1.5); m = v/u = {sig(m)} (1.5); {"real, inverted" if v > 0 else "virtual, erect"}.'.replace('(-', '(−'),
                wrongs=[(1 / (1 / f - 1 / u), m), (-v, -m), (v, -m)])


def c9s2_maker(r):
    n = r.choice([1.5, 1.6, 1.55])
    R1 = r.choice([10, 15, 20, 30])
    R2 = r.choice([10, 15, 20, 30, 40])
    bi = r.random() < 0.6
    if bi:
        inv = (n - 1) * (1 / R1 + 1 / R2)
        t = f'a double-convex lens with radii of curvature {R1} cm and {R2} cm'
    else:
        if R1 == R2:
            R2 = R1 * 2
        a, b = min(R1, R2), max(R1, R2)
        inv = (n - 1) * (1 / a - 1 / b)
        t = f'a convex-meniscus lens with radii of curvature {a} cm and {b} cm (both surfaces curved the same way, the more curved surface convex towards the object)'
    f = 1 / inv
    return NUM(f'Find the focal length of {t}, made of glass of refractive index {g(n)}.', f, 'cm',
               f'1/f = (n − 1)(1/R₁ − 1/R₂) with sign convention (1) = {g(n - 1)} × {sig(inv / (n - 1))} cm⁻¹ (1) ⇒ f = {{ans}} (1).', wrongs=[1 / (n * inv / (n - 1)), f * 2, 1 / ((n - 1) * abs(1 / R1 - 1 / R2)) if R1 != R2 else f / 2])


def c9s2_combo(r):
    f1 = r.choice([10, 20, 25, 40, 50])
    f2 = r.choice([20, 25, 40, 50, 100]) * r.choice([1, -1])
    P = 100 / f1 + 100 / f2
    if abs(P) < 1e-9:
        raise ValueError
    return NUM2(f'A convex lens of focal length {f1} cm is placed in contact with a {"convex" if f2 > 0 else "concave"} lens of focal length {abs(f2)} cm. Find the power and focal length of the combination.', (P, 100 / P), ('D', 'cm'),
                f'P = P₁ + P₂ = 100/{f1} + 100/({f2}) = {sig(P)} D (1.5); f = 100/P = {sig(100 / P)} cm (1.5).'.replace('(-', '(−'), wrongs=[(100 / f1 - 100 / f2, 100 / (100 / f1 - 100 / f2) if 100 / f1 != 100 / f2 else 1), (P / 100, 1 / P), (P, P)])


def c9s2_surface(r):
    n1, n2 = 1.0, r.choice([1.5, 1.33])
    R = r.choice([10, 20, 25, 30])
    u = -r.choice([20, 30, 40, 50, 100])
    inv = (n2 - n1) / R + n1 / u
    if abs(inv) < 1e-12:
        raise ValueError
    v = n2 / inv
    return NUM(f'A point object in air is {-u} cm from the convex spherical surface (radius of curvature {R} cm) of a long glass rod of refractive index {g(n2)}. Find the position of the image.', v, 'cm',
               f'n₂/v − n₁/u = (n₂ − n₁)/R (2) ⇒ {g(n2)}/v = {g(n2 - 1)}/{R} + 1/({u}) (1) ⇒ v = {{ans}} (2) {"(real, inside the glass)" if v > 0 else "(virtual, on the object side)"}.'.replace('(-', '(−'),
               wrongs=[1 / inv, n2 / ((n2 - n1) / R - n1 / u), -v], gap='G5')


def c9s2_liquid(r):
    ng = 1.5
    nl = r.choice([1.33, 1.25, 1.65])
    fa = r.choice([10, 20, 30])
    fl = fa * (ng - 1) / (ng / nl - 1)
    return NUM(f'A thin glass lens (n = 1.5) has focal length {fa} cm in air. Find its focal length when immersed in a liquid of refractive index {g(nl)}.', fl, 'cm',
               f'1/f ∝ (n_g/n_medium − 1) (2); f_l/f_a = (n_g − 1)/(n_g/n_l − 1) = 0.5/{num(ng / nl - 1, 4)} (2) ⇒ f_l = {{ans}} (1){"; negative: the lens becomes diverging" if fl < 0 else ""}.',
               wrongs=[fa * nl, fa / nl, -fl], gap='G5')


c9s2_derive = pool_txt([
    ('Derive the relation n₂/v − n₁/u = (n₂ − n₁)/R for refraction at a convex spherical surface.', 'n₂/v − n₁/u = (n₂ − n₁)/R', 'Diagram (1); Snell\'s law for small angles (2); geometry and sign convention (2).'),
    ('Derive the lens maker\'s formula for a thin double-convex lens.', '1/f = (n₂₁ − 1)(1/R₁ − 1/R₂)', 'Refraction at first surface (2); second surface (2); add, object at infinity (1).'),
])


def c9s2_case(r):
    n1 = r.choice([1.6, 1.62, 1.68])
    n2 = r.choice([1.44, 1.45, 1.5])
    Cc = math.degrees(math.asin(n2 / n1))
    return {'stem': (f'Optical fibres connect homes in many Indian cities. A fibre has a core of refractive index {g(n1)} and a cladding of refractive index {g(n2)}.\n'
                     '(i) On what principle does it work? (ii) Find the critical angle at the core-cladding boundary. (iii) What happens to a ray striking the boundary at an angle smaller than this? (iv) Give one advantage of optical fibres over copper cables.'),
            'answer': f'(i) total internal reflection (ii) {sig(Cc)}° (iii) it is partly refracted into the cladding and lost (iv) very low loss / large bandwidth / no electrical interference',
            'key': '(i) TIR (1). (ii) sin C = n₂/n₁ (1). (iii) refraction (1). (iv) any valid advantage (1).'}


# st3 prism

c9s3_terms = term_mcq([('angle of minimum deviation', 'the deviation when the ray passes symmetrically through the prism (r₁ = r₂ = A/2)'), ('prism formula', 'n = sin[(A + D_m)/2]/sin(A/2)'),
                       ('deviation by a thin prism', 'δ = (n − 1)A'), ('relation of angles in a prism', 'r₁ + r₂ = A and i + e = A + δ')],
                      'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c9s3_tf = tf_mcq('refraction through a prism',
                 ['At minimum deviation the ray inside the prism is parallel to the base (for an isosceles prism).', 'Deviation by a thin prism is δ = (n − 1)A.', 'At minimum deviation, i = e.',
                  'Violet light deviates more than red light in a glass prism.'],
                 ['Red light deviates more than violet in a glass prism.', 'At minimum deviation, i ≠ e.', 'The deviation is the same for all angles of incidence.',
                  'The deviation by a prism is independent of its refractive index.'])

c9s3_explain = pool_txt([
    ('Draw the graph of deviation against angle of incidence for a prism and mark the minimum deviation.', 'U-shaped curve; the lowest point is D_m, where i = e.', '2 marks.'),
    ('Why does white light split into colours on passing through a prism?', 'The refractive index of glass depends on wavelength (dispersion); violet is deviated most, red least.', '2 marks.'),
])

c9s3_ar = pool_ar([
    ('At minimum deviation, the angle of incidence equals the angle of emergence.', 'The path of the ray is then symmetric about the prism.', 'a', 'R explains A.'),
    ('Violet light is deviated more than red light by a glass prism.', 'The refractive index of glass is greater for violet light.', 'a', 'R explains A.'),
    ('The angle of minimum deviation is the same for all colours.', 'The prism formula involves n.', 'd', 'A is false: n varies with colour; R is true.'),
])


def c9s3_min(r):
    A = r.choice([60, 60, 45, 30])
    Dm = r.choice([30, 37, 38, 40, 45, 51]) if A == 60 else r.choice([20, 25, 30]) if A == 45 else r.choice([10, 15, 18])
    n = math.sin(math.radians((A + Dm) / 2)) / math.sin(math.radians(A / 2))
    return NUM(f'The angle of minimum deviation for a prism of angle {A}° is {Dm}°. Find the refractive index of the prism material.', n, '',
               f'n = sin[(A + D_m)/2]/sin(A/2) = sin {g((A + Dm) / 2)}°/sin {g(A / 2)}° = {{ans}}.', wrongs=[(A + Dm) / A, math.sin(math.radians(A + Dm)) / math.sin(math.radians(A)), 1 + Dm / A], gap='G3')


def c9s3_Dm(r):
    A = 60
    n = r.choice([1.414, 1.5, 1.6, 1.732])
    Dm = 2 * math.degrees(math.asin(n * math.sin(math.radians(A / 2)))) - A
    return NUM(f'A prism of angle 60° is made of glass of refractive index {g(n)}. Find the angle of minimum deviation.', Dm, '°',
               f'sin[(A + D_m)/2] = n sin(A/2) = {num(n * 0.5, 4)} (1) ⇒ (A + D_m)/2 = {sig(Dm / 2 + 30)}° (1) ⇒ D_m = {{ans}} (1).', wrongs=[(n - 1) * A, Dm / 2, Dm + 10])


def c9s3_thin(r):
    A = r.choice([3, 4, 5, 6, 8, 10])
    n = r.choice([1.5, 1.52, 1.6, 1.65])
    return NUM(f'Find the deviation produced by a thin prism of angle {A}° and refractive index {g(n)}.', (n - 1) * A, '°', f'δ = (n − 1)A = {g(n - 1)} × {A}° = {{ans}}.', wrongs=[n * A, A / n, (n + 1) * A], gap='G3')


def c9s3_i(r):
    A = 60
    n = r.choice([1.414, 1.5, 1.6, 1.732])
    i = math.degrees(math.asin(n * math.sin(math.radians(A / 2))))
    return NUM2(f'A ray passes through an equilateral glass prism (n = {g(n)}) in the position of minimum deviation. Find the angle of refraction at the first face and the angle of incidence.', (30.0, i), ('°', '°'),
                f'At minimum deviation r₁ = r₂ = A/2 = 30° (1); sin i = n sin 30° = {num(n / 2, 4)} (1) ⇒ i = {sig(i)}° (1).', wrongs=[(60.0, i), (30.0, 2 * i - 60), (30.0, n * 30)])


c9s3_derive = pool_txt([
    ('Derive the prism formula n = sin[(A + D_m)/2]/sin(A/2).', 'n = sin[(A + D_m)/2]/sin(A/2)', 'r₁ + r₂ = A, δ = i + e − A (2); at minimum deviation r = A/2, i = (A + D_m)/2 (2); Snell (1).'),
    ('Show that the deviation produced by a thin prism of angle A is δ = (n − 1)A.', 'δ = (n − 1)A', 'Start from the prism formula with small angles (2); sin x ≈ x (2); result (1).'),
    ('Show that for a prism r₁ + r₂ = A and δ = i + e − A, using a ray diagram.', 'r₁ + r₂ = A; δ = i + e − A', 'Quadrilateral angles (2); triangle of deviations (2); result (1).'),
])


# st4 optical instruments

c9s4_terms = term_mcq([('magnifying power of a simple microscope (image at D)', 'm = 1 + D/f'), ('magnifying power of a compound microscope', 'm ≈ (L/f_o)(D/f_e)'),
                       ('magnifying power of an astronomical telescope (normal adjustment)', 'm = f_o/f_e'), ('length of a telescope in normal adjustment', 'f_o + f_e'),
                       ('near point of a normal eye', 'D = 25 cm')],
                      'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c9s4_tf = tf_mcq('optical instruments',
                 ['A telescope objective has a large focal length and large aperture.', 'A microscope objective has a short focal length.', 'A reflecting telescope has no chromatic aberration.',
                  'The final image in an astronomical telescope is inverted.'],
                 ['A telescope objective should have a short focal length.', 'A microscope eyepiece should have a long focal length.', 'Lenses are free of chromatic aberration while mirrors are not.',
                  'The final image in a compound microscope is real and erect.'])

c9s4_explain = pool_txt([
    ('Why should the objective of a telescope have a large aperture?', 'To gather more light (brighter image) and to give better resolving power.', '2 marks.'),
    ('Give two advantages of a reflecting telescope over a refracting telescope.', 'No chromatic aberration; a large mirror is easier to make and support; parabolic mirror removes spherical aberration.', '2 marks.'),
    ('Why are both the objective and the eyepiece of a compound microscope of short focal length?', 'Magnifying power ∝ 1/(f_o f_e); short focal lengths give a large magnification.', '2 marks.'),
])

c9s4_ar = pool_ar([
    ('The objective of a telescope has a large focal length.', 'Magnifying power of a telescope is f_o/f_e.', 'a', 'R explains A.'),
    ('Reflecting telescopes are preferred for large astronomical telescopes.', 'Mirrors are free from chromatic aberration.', 'a', 'R explains A (one of the reasons).'),
    ('The final image in an astronomical telescope is erect.', 'The objective forms a real inverted image.', 'd', 'A is false: final image is inverted; R is true.'),
])


def c9s4_simple(r):
    f = r.choice([2.5, 5, 6.25, 10])
    near = r.random() < 0.5
    m = 1 + 25 / f if near else 25 / f
    return NUM(f'Find the magnifying power of a simple microscope (convex lens) of focal length {g(f)} cm when the image is formed at {"the near point (25 cm)" if near else "infinity"}.', m, '',
               f'm = {"1 + D/f" if near else "D/f"} = {"1 + " if near else ""}25/{g(f)} = {{ans}}.', wrongs=[25 / f if near else 1 + 25 / f, f / 25, 2 * m], gap='G3', n=3)


def c9s4_tele(r):
    fo = r.choice([100, 120, 150, 200, 15 * 100])
    fe = r.choice([2, 4, 5, 10])
    if fo > 1000:
        fo = 1500
    return NUM2(f'An astronomical telescope has an objective of focal length {g(fo)} cm and an eyepiece of focal length {fe} cm. Find its magnifying power and length in normal adjustment.', (fo / fe, fo + fe), ('', 'cm'),
                f'm = f_o/f_e = {g(fo)}/{fe} = {sig(fo / fe)} (1); L = f_o + f_e = {g(fo + fe)} cm (1).', wrongs=[(fe / fo, fo - fe), (fo / fe, fo * fe), (fo * fe, fo + fe)])


def c9s4_compound(r):
    fo = r.choice([1, 1.25, 2, 0.5])
    fe = r.choice([2.5, 5, 6.25])
    L = r.choice([10, 12, 15, 16, 20])
    m = L / fo * 25 / fe
    return NUM(f'A compound microscope has an objective of focal length {g(fo)} cm and an eyepiece of focal length {g(fe)} cm, with tube length {L} cm. Find its magnifying power in normal adjustment (final image at infinity).', m, '',
               f'm = (L/f_o)(D/f_e) = ({L}/{g(fo)}) × (25/{g(fe)}) = {{ans}}.', wrongs=[L / fo * (1 + 25 / fe), fo * fe / L, L / fo + 25 / fe])


def c9s4_full(r):
    fo = r.choice([1, 2])
    fe = r.choice([5, 6.25])
    uo = r.choice([1.2, 1.25, 1.5]) * fo
    vo = 1 / (1 / fo - 1 / uo)
    mo = -vo / uo
    me = 1 + 25 / fe
    ue = 1 / (1 / 25 + 1 / fe)
    return NUM2(f'In a compound microscope, the objective (f_o = {g(fo)} cm) and the eyepiece (f_e = {g(fe)} cm) are arranged so that the final image is at the near point (25 cm). The object is {g(uo)} cm from the objective. Find the magnifying power and the separation between the lenses.',
                (abs(mo) * me, vo + ue), ('', 'cm'), f'Objective: 1/v − 1/u = 1/f ⇒ v_o = {sig(vo)} cm (1); m_o = v_o/u_o = {sig(-mo)} (1); eyepiece m_e = 1 + D/f_e = {sig(me)} (1); total m = {sig(abs(mo) * me)} (1); u_e = {sig(ue)} cm so separation = v_o + |u_e| = {sig(vo + ue)} cm (1).',
                wrongs=[(abs(mo) * 25 / fe, vo + fe), (abs(mo) + me, vo + ue), (abs(mo) * me, vo)], gap='G5')


def c9s4_moon(r):
    fo = r.choice([5, 10, 15, 20])
    dm, Dm = 3.48e6, 3.8e8
    d = fo * dm / Dm
    return NUM(f'A telescope objective has a focal length of {fo} m. Find the diameter of the image of the Moon formed by it. (diameter of Moon = 3.48 × 10⁶ m, radius of lunar orbit = 3.8 × 10⁸ m)', d * 100, 'cm',
               f'The image is at the focal plane; angle subtended α = d_moon/D = {sig(dm / Dm)} rad (1); image size = f_o α = {sig(d)} m = {{ans}} (2).', wrongs=[d * 1000, dm / (Dm * fo) * 100, d * 50])


def c9s4_case(r):
    who = name(r)
    fo = r.choice([90, 100, 120])
    fe = r.choice([3, 4, 5])
    return {'stem': (f'{who} builds a simple astronomical telescope for a school astronomy club using a lens of focal length {fo} cm and another of focal length {fe} cm.\n'
                     '(i) Which lens should be the objective? (ii) Find the magnifying power in normal adjustment. (iii) What is the length of the telescope then? (iv) Is the final image erect or inverted?'),
            'answer': f'(i) the {fo} cm lens (ii) {sig(fo / fe)} (iii) {fo + fe} cm (iv) inverted',
            'key': '(i) long focal length objective (1). (ii) f_o/f_e (1). (iii) f_o + f_e (1). (iv) inverted (1).'}


# ======================================================== ch10 Wave Optics
# st1 Huygens

c10s1_terms = term_mcq([('wavefront', 'a surface of constant phase'), ('Huygens\' principle', 'every point on a wavefront acts as a source of secondary wavelets'),
                        ('wavefront from a point source', 'spherical'), ('wavefront from a distant source', 'plane'), ('ray', 'a line normal to the wavefront, giving the direction of energy flow')],
                       'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c10s1_tf = tf_mcq("Huygens' principle",
                  ['On refraction, the frequency of light does not change.', 'Light travels slower in a denser medium (wave theory).', 'A convex lens converts a plane wavefront into a spherical converging one.',
                   'Rays are perpendicular to wavefronts.'],
                  ['On refraction, the frequency of light changes.', 'Wave theory predicts light travels faster in glass than in air.', 'Rays are parallel to wavefronts.',
                   'A prism converts a plane wavefront into a spherical one.'])

c10s1_explain = pool_txt([
    ('When light passes from air into glass, which of frequency, wavelength and speed change?', 'Frequency stays the same; speed and wavelength decrease by a factor n.', '2 marks.'),
    ('What type of wavefront emerges from (a) a point source, (b) a convex lens with a point source at its focus?', '(a) spherical (b) plane.', '1 + 1 marks.'),
    ('Why does the colour of light not change on refraction?', 'Colour depends on frequency, which is fixed by the source and does not change.', '2 marks.'),
])

c10s1_ar = pool_ar([
    ('The frequency of light does not change when it is refracted.', 'Frequency is a characteristic of the source.', 'a', 'R explains A.'),
    ('Light bends towards the normal on entering glass from air.', 'Light travels slower in glass.', 'a', 'Huygens\' construction; R explains A.'),
    ('The wavelength of light increases when it enters water from air.', 'The speed of light decreases in water.', 'd', 'A is false: λ decreases; R is true.'),
])


def c10s1_medium(r):
    lam = r.choice([450, 500, 589, 600, 650])
    n = r.choice([1.33, 1.5, 1.6])
    return NUM2(f'Light of wavelength {lam} nm in air enters glass of refractive index {g(n)}. Find its speed, wavelength and frequency in the glass.', (C / n, lam / n, C / (lam * 1e-9)), ('m s⁻¹', 'nm', 'Hz'),
                f'v = c/n = {sig(C / n)} m s⁻¹ (1); λ\' = λ/n = {sig(lam / n)} nm (1); ν = c/λ = {sig(C / (lam * 1e-9))} Hz, unchanged (1).',
                wrongs=[(C * n, lam * n, C / (lam * 1e-9)), (C / n, lam / n, C / (lam * 1e-9) / n), (C, float(lam), C / (lam * 1e-9))], sep='; ')


def c10s1_ratio(r):
    n1 = r.choice([1.33, 1.5])
    n2 = r.choice([1.5, 1.6, 2.42])
    if n1 == n2:
        n2 = 1.6
    return NUM(f'Find the ratio of the speed of light in a medium of refractive index {g(n1)} to that in a medium of refractive index {g(n2)}.', n2 / n1, '', f'v ∝ 1/n ⇒ v₁/v₂ = n₂/n₁ = {g(n2)}/{g(n1)} = {{ans}}.', wrongs=[n1 / n2, n1 * n2, (n2 / n1) ** 2], gap='G3')


c10s1_mcq = pool_mcq([
    ('The wavefront of light from a distant star reaching the Earth is', 'plane', ['spherical', 'cylindrical', 'elliptical'], 'Very far source: a small part of a huge sphere is flat.'),
    ('A plane wavefront passes through a thin convex lens. The emerging wavefront is', 'spherical, converging to the focus', ['plane', 'spherical, diverging', 'cylindrical'], 'The middle part is delayed more.'),
    ('The wavefront from a linear (line) source of light is', 'cylindrical', ['plane', 'spherical', 'conical'], 'Equidistant points from a line form cylinders.'),
    ('A plane wavefront reflected from a concave mirror becomes', 'spherical, converging', ['plane', 'spherical, diverging', 'cylindrical'], 'Converges to F.'),
])

c10s1_derive = pool_txt([
    ('Using Huygens\' principle, verify the laws of refraction (Snell\'s law).', 'sin i/sin r = v₁/v₂ = n₂₁', 'Construction with wavefront AB and wavelets (2); geometry of triangles (2); result (1).'),
    ('Using Huygens\' principle, verify the laws of reflection.', 'i = r', 'Construction (2); congruent triangles (2); result (1).'),
])


# st2 interference, YDSE

c10s2_terms = term_mcq([('coherent sources', 'sources with a constant phase difference and the same frequency'), ('fringe width', 'β = λD/d'),
                        ('condition for constructive interference', 'path difference = nλ'), ('condition for destructive interference', 'path difference = (n + ½)λ'),
                        ('resultant intensity for two equal waves', 'I = 4I₀ cos²(φ/2)')],
                       'Which of the following gives {a}?', 'Which term is {b}?', '{a}: {b}.')

c10s2_tf = tf_mcq("Young's double-slit experiment",
                  ['Fringe width increases when the screen is moved away from the slits.', 'Fringe width decreases if the slit separation is increased.', 'Fringes are narrower in water than in air.',
                   'With white light the central fringe is white.', 'Two independent bulbs are not coherent sources.'],
                  ['Fringe width increases when the slits are moved apart.', 'Two independent sodium lamps give a stable interference pattern.', 'Fringes are wider in water than in air.',
                   'With white light the central fringe is dark.', 'Fringe width is independent of wavelength.'])

c10s2_explain = pool_txt([
    ('Why are two independent light sources not coherent?', 'Light comes from many atoms emitting randomly; their phase difference changes rapidly (~10⁻⁸ s), so no steady pattern.', '2 marks.'),
    ('How does the fringe pattern change if the whole YDSE apparatus is immersed in water?', 'λ becomes λ/n, so fringe width becomes β/n (narrower).', '2 marks.'),
    ('What happens to the interference pattern if one slit is covered?', 'Interference disappears; a single-slit diffraction pattern (broad central band) is seen.', '2 marks.'),
])

c10s2_ar = pool_ar([
    ('In YDSE, fringe width decreases when the experiment is done in water.', 'The wavelength of light decreases in water.', 'a', 'β = λD/d; R explains A.'),
    ('Two independent sodium lamps cannot produce a sustained interference pattern.', 'Their phase difference does not remain constant.', 'a', 'R explains A.'),
    ('Energy is destroyed at the dark fringes in interference.', 'Interference only redistributes energy.', 'd', 'A is false; R is true.'),
])


def c10s2_beta(r):
    lam = r.choice([500, 550, 589, 600, 650])
    D = r.choice([1, 1.2, 1.5, 2])
    d = r.choice([0.2, 0.25, 0.5, 1])
    b = lam * 1e-9 * D / (d * 1e-3)
    return NUM(f'In a Young\'s double-slit experiment, the slits are {g(d)} mm apart and the screen is {g(D)} m away. Light of wavelength {lam} nm is used. Find the fringe width.', b * 1000, 'mm',
               f'β = λD/d = {lam} × 10⁻⁹ × {g(D)}/({g(d)} × 10⁻³) = {sig(b)} m = {{ans}}.', wrongs=[b * 1e4, lam * 1e-9 * d / D * 1e6, b * 500], gap='G3')


def c10s2_lambda(r):
    lamt = r.choice([480, 500, 560, 600, 640])
    D = r.choice([1, 1.5, 2])
    d = r.choice([0.5, 1, 0.8])
    b = round(lamt * 1e-9 * D / (d * 1e-3) * 1000, 3)
    lam = b * 1e-3 * d * 1e-3 / D
    return NUM(f'In YDSE with slit separation {g(d)} mm and screen distance {g(D)} m, the fringe width is found to be {g(b)} mm. Find the wavelength of the light.', lam * 1e9, 'nm',
               f'λ = βd/D = {g(b)} × 10⁻³ × {g(d)} × 10⁻³/{g(D)} = {{ans}}.', wrongs=[b * D / d * 1e3, lam * 1e9 * 2, lam * 1e6])


def c10s2_nth(r):
    lam = r.choice([500, 600, 650])
    D = r.choice([1, 1.5, 2])
    d = r.choice([0.5, 1])
    n = r.choice([2, 3, 4, 5])
    b = lam * 1e-9 * D / (d * 1e-3) * 1000
    bright = r.random() < 0.5
    y = n * b if bright else (n - 0.5) * b
    what = f'{n}{"nd" if n == 2 else "rd" if n == 3 else "th"} bright fringe' if bright else f'{n}{"nd" if n == 2 else "rd" if n == 3 else "th"} dark fringe'
    return NUM(f'In YDSE (d = {g(d)} mm, D = {g(D)} m, λ = {lam} nm), find the distance of the {what} from the central bright fringe.', y, 'mm',
               f'β = λD/d = {sig(b)} mm (1); y = {"nβ" if bright else "(n − ½)β"} = {{ans}} (2).', wrongs=[(n - 0.5) * b if bright else n * b, (n + 0.5) * b, b], gap='G3')


def c10s2_coincide(r):
    l1, l2 = r.choice([(650, 520), (600, 400), (500, 600), (450, 600), (480, 600)])
    from math import gcd
    D = r.choice([1, 1.2, 1.5])
    d = r.choice([0.5, 1, 2])
    L = l1 * l2 // gcd(l1, l2)
    n1 = L // l1
    y = n1 * l1 * 1e-9 * D / (d * 1e-3) * 1000
    return NUM(f'A beam containing wavelengths {l1} nm and {l2} nm is used in YDSE with d = {g(d)} mm and D = {g(D)} m. Find the least distance from the central maximum where the bright fringes of both wavelengths coincide.', y, 'mm',
               f'Coincidence: n₁λ₁ = n₂λ₂ (2); least n₁ = {n1}, n₂ = {L // l2} (LCM {L} nm) (1); y = n₁λ₁D/d = {{ans}} (2).', wrongs=[l1 * 1e-9 * D / (d * 1e-3) * 1000, l2 * 1e-9 * D / (d * 1e-3) * 1000, y * 2], gap='G5')


def c10s2_water(r):
    b = r.choice([0.4, 0.6, 0.8, 1.2])
    n = 4 / 3
    return NUM(f'The fringe width in a YDSE in air is {g(b)} mm. What is it when the apparatus is immersed in water (n = 4/3)?', b / n, 'mm', f'λ → λ/n so β\' = β/n = {g(b)} × 3/4 = {{ans}}.', wrongs=[b * n, b, b / n ** 2])


def c10s2_I(r):
    I0 = r.choice([1, 2, 4, 5])
    pd = r.choice([('λ/4', math.pi / 2), ('λ/3', 2 * math.pi / 3), ('λ/6', math.pi / 3), ('λ/2', math.pi), ('λ', 2 * math.pi)])
    I = 4 * I0 * math.cos(pd[1] / 2) ** 2
    if I < 1e-9:
        I = 0.0
    return NUM(f'In YDSE, each slit alone gives intensity I₀ = {I0} units on the screen. Find the intensity at a point where the path difference between the waves is {pd[0]}.', I, 'units',
               f'Phase difference φ = (2π/λ) × path difference = {num(pd[1] / math.pi, 3)}π (1); I = 4I₀ cos²(φ/2) (2) = {{ans}} (2).', wrongs=[2 * I0, 4 * I0 * math.cos(pd[1]) ** 2, 4 * I0], gap='G5') if I else {
        'stem': f'In YDSE, each slit alone gives intensity I₀ = {I0} units on the screen. Find the intensity at a point where the path difference between the waves is {pd[0]}.', 'answer': '0 units',
        'key': 'φ = π (1); I = 4I₀ cos²(π/2) = 0 (2): a dark fringe (2).', 'distractors': [f'{2 * I0} units', f'{4 * I0} units', f'{I0} units']}


c10s2_derive = pool_txt([
    ('Derive the expression for fringe width in Young\'s double-slit experiment.', 'β = λD/d', 'Path difference xd/D (2); bright at nλ, dark at (n + ½)λ (2); spacing (1).'),
    ('Show that the resultant intensity of two coherent waves of equal intensity I₀ with phase difference φ is 4I₀ cos²(φ/2).', 'I = 4I₀ cos²(φ/2)', 'Superpose y₁ and y₂ (2); amplitude 2a cos(φ/2) (2); I ∝ A² (1).'),
])


def c10s2_case(r):
    who = name(r)
    lam = r.choice([589, 632.8, 650])
    d = r.choice([0.2, 0.25, 0.5])
    D = r.choice([1, 1.5, 2])
    b = lam * 1e-9 * D / (d * 1e-3) * 1000
    return {'stem': (f'{who} performs Young\'s double-slit experiment in the school lab with light of wavelength {g(lam)} nm. The slits are {g(d)} mm apart and the screen is {g(D)} m away.\n'
                     '(i) Find the fringe width. (ii) Find the distance between the central bright fringe and the 3rd dark fringe. (iii) What happens to the fringe width if the screen is moved closer? (iv) What is seen if white light is used?'),
            'answer': f'(i) {sig(b)} mm (ii) {sig(2.5 * b)} mm (iii) it decreases (β ∝ D) (iv) a white central fringe with a few coloured fringes on either side',
            'key': '(i) β = λD/d (1). (ii) 2.5β (1). (iii) (1). (iv) (1).'}


# st3 single slit diffraction

c10s3_terms = term_mcq([('first minimum of single-slit diffraction', 'a sin θ = λ'), ('angular width of the central maximum', '2λ/a'),
                        ('Fresnel distance', 'z_F = a²/λ, beyond which diffraction spreading dominates'), ('secondary maxima of single slit', 'approximately at a sin θ = (n + ½)λ')],
                       'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c10s3_tf = tf_mcq('single-slit diffraction',
                  ['The central maximum is twice as wide as the other maxima.', 'Narrowing the slit widens the central maximum.', 'Diffraction is more noticeable when the slit width is comparable to λ.',
                   'The intensity of the secondary maxima falls off rapidly.'],
                  ['Widening the slit widens the central maximum.', 'All diffraction maxima have equal intensity.', 'Diffraction of sound is less noticeable than of light in daily life.',
                   'The central maximum is the same width as the secondary maxima.'])

c10s3_explain = pool_txt([
    ('Why is diffraction of sound waves more easily observed than diffraction of light?', 'Sound wavelengths (≈1 m) are comparable to everyday openings; light wavelengths are much smaller.', '2 marks.'),
    ('How does the single-slit pattern change when (a) the slit is made narrower, (b) red light is replaced by blue?', '(a) central maximum widens; (b) it narrows (smaller λ).', '1 + 1 marks.'),
    ('Distinguish between interference and diffraction fringes.', 'Interference: equal-width fringes of nearly equal intensity, from two sources. Diffraction: central maximum twice as wide, intensity falls for others, from one wavefront.', '2 marks.'),
])

c10s3_ar = pool_ar([
    ('The central maximum of a single-slit pattern becomes wider when the slit is narrowed.', 'Angular width of the central maximum is 2λ/a.', 'a', 'R explains A.'),
    ('Ray optics is valid for distances much less than the Fresnel distance.', 'Diffraction spreading is negligible over such distances.', 'a', 'R explains A.'),
    ('Diffraction does not occur for light because its wavelength is small.', 'Diffraction is significant when the aperture is comparable to λ.', 'd', 'A is false: it occurs but is small for large apertures; R is true.'),
])


def c10s3_width(r):
    lam = r.choice([500, 600, 650])
    a = r.choice([0.1, 0.2, 0.5])
    D = r.choice([1, 1.5, 2])
    w = 2 * lam * 1e-9 * D / (a * 1e-3) * 1000
    return NUM(f'Light of wavelength {lam} nm falls on a single slit of width {g(a)} mm. Find the linear width of the central maximum on a screen {g(D)} m away.', w, 'mm',
               f'Width = 2λD/a (2) = 2 × {lam} × 10⁻⁹ × {g(D)}/({g(a)} × 10⁻³) = {{ans}} (1).', wrongs=[w / 2, w * 2, lam * 1e-9 * a / D * 1e6])


def c10s3_first(r):
    lam = r.choice([500, 589, 600])
    a = r.choice([1, 2, 5, 10]) * 1e-6
    th = math.degrees(math.asin(lam * 1e-9 / a))
    return NUM(f'Find the angle of the first minimum when light of wavelength {lam} nm falls on a slit of width {g(a * 1e6)} μm.', th, '°', f'sin θ = λ/a = {lam} × 10⁻⁹/{g(a)} = {num(lam * 1e-9 / a, 4)} ⇒ θ = {{ans}}.',
               wrongs=[2 * th, math.degrees(lam * 1e-9 / a) * 2, math.degrees(math.asin(lam * 1e-9 / (2 * a)))], gap='G3')


def c10s3_a(r):
    lam = r.choice([500, 600, 650])
    D = r.choice([1, 2])
    y = r.choice([2, 2.5, 3, 5])
    a = lam * 1e-9 * D / (y * 1e-3)
    return NUM(f'In a single-slit diffraction experiment with light of wavelength {lam} nm, the first minimum is {g(y)} mm from the centre of the pattern on a screen {D} m away. Find the slit width.', a * 1000, 'mm',
               f'y = λD/a ⇒ a = λD/y = {lam} × 10⁻⁹ × {D}/({g(y)} × 10⁻³) = {{ans}}.', wrongs=[2 * a * 1000, a * 1e6, a * 500])


def c10s3_fresnel(r):
    a = r.choice([1, 2, 3, 4])
    lam = r.choice([500, 600])
    z = (a * 1e-3) ** 2 / (lam * 1e-9)
    return NUM(f'Estimate the Fresnel distance for an aperture of {a} mm and light of wavelength {lam} nm. Up to what distance is ray optics a good approximation?', z, 'm',
               f'z_F = a²/λ (2) = ({a} × 10⁻³)²/({lam} × 10⁻⁹) = {{ans}} (2); ray optics holds for distances much less than this (1).', wrongs=[a * 1e-3 / (lam * 1e-9), z * 2, z / 1000], gap='G5')


# st4 polarisation

c10s4_terms = term_mcq([('Brewster\'s law', 'tan i_B = n'), ('Malus\'s law', 'I = I₀ cos²θ'), ('polaroid', 'a sheet that transmits light vibrating in one direction only'),
                        ('unpolarised light through one polaroid', 'transmitted intensity is I₀/2'), ('angle between reflected and refracted rays at Brewster angle', '90°')],
                       'Which of the following gives {a}?', 'Which term is {b}?', '{a}: {b}.')

c10s4_tf = tf_mcq('polarisation',
                  ['Polarisation shows that light waves are transverse.', 'At Brewster\'s angle the reflected light is completely plane polarised.', 'Sound waves in air cannot be polarised.',
                   'Light scattered by the sky at 90° to the sunlight is polarised.'],
                  ['Polarisation shows that light is longitudinal.', 'Sound waves in air can be polarised.', 'At Brewster\'s angle the refracted light is completely polarised.',
                   'A polaroid transmits all of the unpolarised light falling on it.'])

c10s4_explain = pool_txt([
    ('What does polarisation tell us about the nature of light?', 'Only transverse waves can be polarised, so light waves are transverse.', '2 marks.'),
    ('Why are polaroid sunglasses useful while driving?', 'Glare reflected from roads and water is partly polarised; the polaroid blocks it.', '2 marks.'),
])

c10s4_ar = pool_ar([
    ('Sound waves cannot be polarised.', 'Sound waves in air are longitudinal.', 'a', 'R explains A.'),
    ('At the Brewster angle, the reflected and refracted rays are perpendicular.', 'tan i_B = n.', 'a', 'From Snell\'s law with tan i_B = n, r = 90° − i_B; R explains A.'),
    ('Unpolarised light passing through a polaroid keeps its full intensity.', 'A polaroid transmits only one direction of vibration.', 'd', 'A is false: intensity halves; R is true.'),
])


def c10s4_brewster(r):
    n = r.choice([1.33, 1.5, 1.6, 1.732])
    iB = math.degrees(math.atan(n))
    return NUM2(f'Find the Brewster angle for light reflected from a surface of refractive index {g(n)}, and the angle of refraction at that angle.', (iB, 90 - iB), ('°', '°'),
                f'tan i_B = n ⇒ i_B = {sig(iB)}° (1); reflected and refracted rays are at 90°, so r = 90° − i_B = {sig(90 - iB)}° (1).', wrongs=[(math.degrees(math.asin(1 / n)), 90 - math.degrees(math.asin(1 / n))), (iB, iB), (math.degrees(math.atan(1 / n)), iB)])


def c10s4_malus(r):
    I0 = r.choice([16, 32, 40, 64, 100])
    th = r.choice([30, 45, 60])
    I1 = I0 / 2
    I2 = I1 * math.cos(math.radians(th)) ** 2
    return NUM2(f'Unpolarised light of intensity {I0} W m⁻² falls on a polaroid P₁. The light then passes through a second polaroid P₂ whose axis is at {th}° to that of P₁. Find the intensity after P₁ and after P₂.', (I1, I2), ('W m⁻²', 'W m⁻²'),
                f'After P₁: I₀/2 = {sig(I1)} W m⁻² (1); Malus\'s law: I = (I₀/2)cos²{th}° = {sig(I2)} W m⁻² (2).', wrongs=[(float(I0), I0 * math.cos(math.radians(th)) ** 2), (I1, I1 * math.cos(math.radians(th))), (I1, I1 * math.sin(math.radians(th)) ** 2)])


def c10s4_n(r):
    iB = r.choice([53, 56.3, 57, 60])
    return NUM(f'Light reflected from a glass surface is completely plane polarised when the angle of incidence is {g(iB)}°. Find the refractive index of the glass.', math.tan(math.radians(iB)), '',
               f'n = tan i_B = tan {g(iB)}° = {{ans}}.', wrongs=[1 / math.sin(math.radians(iB)), math.sin(math.radians(iB)), 1 / math.tan(math.radians(iB))], gap='G3')


# ======================================================== families

FAMILIES = {
    S + '06-st1': [F('C1', 'D1', 'mcq', c6s1_terms), F('C1', 'D2', 'mcq', c6s1_tf), F('C2', 'D2', 'explain', c6s1_explain), F('C2', 'D3', 'mcq', c6s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c6s1_flux), F('C3', 'D2', 'numerical', c6s1_emf), F('C3', 'D3', 'numerical', c6s1_turn), F('C4', 'D3', 'multi_step', c6s1_ramp),
                   F('C4', 'D4', 'multi_step', c6s1_charge)],
    S + '06-st2': [F('C1', 'D1', 'mcq', c6s2_terms), F('C1', 'D2', 'mcq', c6s2_tf), F('C2', 'D2', 'explain', c6s2_explain), F('C2', 'D3', 'mcq', c6s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c6s2_derive), F('C3', 'D2', 'mcq', c6s2_lenz), F('C3', 'D1', 'short', c6s2_blv), F('C3', 'D3', 'numerical', c6s2_rod),
                   F('C4', 'D3', 'numerical', c6s2_rotate), F('C4', 'D4', 'long', c6s2_power), F('C4', 'D5', 'long', c6s2_terminal), F('C3', 'D3', 'case', c6s2_case)],
    S + '06-st3': [F('C1', 'D1', 'mcq', c6s3_uses), F('C1', 'D2', 'mcq', c6s3_tf), F('C2', 'D2', 'explain', c6s3_explain), F('C2', 'D3', 'mcq', c6s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c6s3_mcq), F('C4', 'D3', 'case', c6s3_case)],
    S + '06-st4': [F('C1', 'D1', 'mcq', c6s4_terms), F('C1', 'D2', 'mcq', c6s4_tf), F('C2', 'D2', 'explain', c6s4_explain), F('C2', 'D3', 'mcq', c6s4_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c6s4_derive), F('C3', 'D1', 'short', c6s4_U), F('C3', 'D2', 'numerical', c6s4_back), F('C3', 'D2', 'numerical', c6s4_L),
                   F('C3', 'D3', 'numerical', c6s4_gen), F('C4', 'D3', 'numerical', c6s4_inst), F('C4', 'D4', 'long', c6s4_M), F('C3', 'D3', 'case', c6s4_case)],
    S + '07-st1': [F('C1', 'D1', 'mcq', c7s1_terms), F('C1', 'D2', 'mcq', c7s1_tf), F('C2', 'D2', 'explain', c7s1_explain), F('C2', 'D3', 'mcq', c7s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c7s1_rms), F('C3', 'D2', 'numerical', c7s1_res), F('C3', 'D2', 'numerical', c7s1_XL), F('C3', 'D3', 'numerical', c7s1_XC),
                   F('C4', 'D3', 'numerical', c7s1_freq), F('C4', 'D4', 'multi_step', c7s1_eqn)],
    S + '07-st2': [F('C1', 'D1', 'mcq', c7s2_terms), F('C1', 'D2', 'mcq', c7s2_tf), F('C2', 'D2', 'explain', c7s2_explain), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c7s2_derive), F('C3', 'D1', 'short', c7s2_f0), F('C3', 'D2', 'numerical', c7s2_Z), F('C3', 'D3', 'numerical', c7s2_resI),
                   F('C4', 'D3', 'numerical', c7s2_Q), F('C4', 'D4', 'long', c7s2_full), F('C4', 'D5', 'multi_step', c7s2_tune), F('C3', 'D3', 'case', c7s2_case)],
    S + '07-st3': [F('C1', 'D1', 'mcq', c7s3_terms), F('C1', 'D2', 'mcq', c7s3_tf), F('C2', 'D2', 'explain', c7s3_explain), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'mcq', c7s3_mcq), F('C3', 'D2', 'numerical', c7s3_P), F('C3', 'D3', 'numerical', c7s3_pf), F('C4', 'D3', 'multi_step', c7s3_full),
                   F('C4', 'D4', 'long', c7s3_choke)],
    S + '07-st4': [F('C1', 'D1', 'mcq', c7s4_terms), F('C1', 'D2', 'mcq', c7s4_tf), F('C2', 'D2', 'explain', c7s4_explain), F('C2', 'D3', 'mcq', c7s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c7s4_ratio), F('C3', 'D2', 'numerical', c7s4_current), F('C3', 'D3', 'numerical', c7s4_eff), F('C4', 'D3', 'numerical', c7s4_turns),
                   F('C4', 'D4', 'long', c7s4_line), F('C4', 'D3', 'case', c7s4_case)],
    S + '08-st1': [F('C1', 'D1', 'mcq', c8s1_terms), F('C1', 'D2', 'mcq', c8s1_tf), F('C1', 'D1', 'mcq', c8s1_mcq), F('C2', 'D2', 'explain', c8s1_explain), F('C2', 'D3', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s1_id), F('C3', 'D3', 'numerical', c8s1_dE), F('C4', 'D4', 'long', c8s1_B)],
    S + '08-st2': [F('C1', 'D1', 'mcq', c8s2_terms), F('C1', 'D2', 'mcq', c8s2_tf), F('C2', 'D2', 'explain', c8s2_explain), F('C2', 'D3', 'mcq', c8s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'mcq', c8s2_order), F('C3', 'D1', 'short', c8s2_lam), F('C3', 'D2', 'numerical', c8s2_B0), F('C3', 'D3', 'multi_step', c8s2_wave),
                   F('C4', 'D3', 'numerical', c8s2_medium)],
    S + '08-st3': [F('C1', 'D1', 'mcq', c8s3_uses), F('C1', 'D2', 'mcq', c8s3_tf), F('C2', 'D2', 'explain', c8s3_explain), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c8s3_region), F('C3', 'D2', 'numerical', c8s3_station), F('C4', 'D3', 'case', c8s3_case)],
    S + '09-st1': [F('C1', 'D1', 'mcq', c9s1_terms), F('C1', 'D2', 'mcq', c9s1_tf), F('C2', 'D2', 'explain', c9s1_explain), F('C2', 'D3', 'mcq', c9s1_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c9s1_derive), F('C3', 'D1', 'short', c9s1_fR), F('C3', 'D2', 'numerical', c9s1_mirror), F('C3', 'D3', 'numerical', c9s1_convex),
                   F('C4', 'D4', 'multi_step', c9s1_magn)],
    S + '09-st2': [F('C1', 'D1', 'mcq', c9s2_terms), F('C1', 'D2', 'mcq', c9s2_tf), F('C2', 'D2', 'explain', c9s2_explain), F('C2', 'D3', 'mcq', c9s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c9s2_derive), F('C3', 'D1', 'short', c9s2_snell), F('C3', 'D2', 'numerical', c9s2_critical), F('C3', 'D2', 'numerical', c9s2_depth),
                   F('C3', 'D3', 'numerical', c9s2_lens), F('C3', 'D3', 'numerical', c9s2_maker), F('C4', 'D3', 'numerical', c9s2_combo), F('C4', 'D4', 'long', c9s2_surface),
                   F('C4', 'D5', 'multi_step', c9s2_liquid), F('C4', 'D3', 'case', c9s2_case)],
    S + '09-st3': [F('C1', 'D1', 'mcq', c9s3_terms), F('C1', 'D2', 'mcq', c9s3_tf), F('C2', 'D2', 'explain', c9s3_explain), F('C2', 'D3', 'mcq', c9s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c9s3_derive), F('C3', 'D1', 'short', c9s3_thin), F('C3', 'D2', 'numerical', c9s3_min), F('C3', 'D3', 'numerical', c9s3_Dm),
                   F('C4', 'D3', 'multi_step', c9s3_i)],
    S + '09-st4': [F('C1', 'D1', 'mcq', c9s4_terms), F('C1', 'D2', 'mcq', c9s4_tf), F('C2', 'D2', 'explain', c9s4_explain), F('C2', 'D3', 'mcq', c9s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c9s4_simple), F('C3', 'D2', 'numerical', c9s4_tele), F('C3', 'D3', 'numerical', c9s4_compound), F('C4', 'D3', 'numerical', c9s4_moon),
                   F('C4', 'D4', 'long', c9s4_full), F('C3', 'D3', 'case', c9s4_case)],
    S + '10-st1': [F('C1', 'D1', 'mcq', c10s1_terms), F('C1', 'D2', 'mcq', c10s1_tf), F('C2', 'D2', 'explain', c10s1_explain), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c10s1_derive), F('C3', 'D1', 'short', c10s1_ratio), F('C3', 'D2', 'mcq', c10s1_mcq), F('C4', 'D3', 'multi_step', c10s1_medium)],
    S + '10-st2': [F('C1', 'D1', 'mcq', c10s2_terms), F('C1', 'D2', 'mcq', c10s2_tf), F('C2', 'D2', 'explain', c10s2_explain), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c10s2_derive), F('C3', 'D1', 'short', c10s2_beta), F('C3', 'D2', 'numerical', c10s2_lambda), F('C3', 'D3', 'numerical', c10s2_nth),
                   F('C4', 'D3', 'numerical', c10s2_water), F('C4', 'D4', 'long', c10s2_coincide), F('C4', 'D5', 'multi_step', c10s2_I), F('C3', 'D3', 'case', c10s2_case)],
    S + '10-st3': [F('C1', 'D1', 'mcq', c10s3_terms), F('C1', 'D2', 'mcq', c10s3_tf), F('C2', 'D2', 'explain', c10s3_explain), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c10s3_first), F('C3', 'D2', 'numerical', c10s3_width), F('C3', 'D3', 'numerical', c10s3_a), F('C4', 'D4', 'multi_step', c10s3_fresnel)],
    S + '10-st4': [F('C1', 'D1', 'mcq', c10s4_terms), F('C1', 'D2', 'mcq', c10s4_tf), F('C2', 'D2', 'explain', c10s4_explain), F('C2', 'D3', 'mcq', c10s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c10s4_n), F('C3', 'D2', 'numerical', c10s4_brewster), F('C4', 'D3', 'numerical', c10s4_malus)],
}

FAMILIES = polish(FAMILIES)
