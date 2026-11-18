"""CBSE class 9 science families, chapters 5-8 (Forces and Motion; Work, Energy and Simple Machines;
Journey Inside the Atom; Atomic Foundations of Matter)."""
from __future__ import annotations

import math

from qbank import name, two_names, num, num_distractors, mcq, inr
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g9-science-ch'
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def sub(s: str) -> str:
    return s.translate(SUB)


# ======================= ch05 Forces and Motion
c5s1_defs = [
    ('inertia', 'the natural tendency of an object to resist a change in its state of rest or of uniform motion'),
    ('balanced forces', 'forces acting on an object whose resultant is zero, so they do not change its state of motion'),
    ('unbalanced forces', 'forces whose resultant is not zero, which change the speed or direction of motion of an object'),
    ('Newton\'s first law of motion', 'the law that an object remains at rest or in uniform motion in a straight line unless acted upon by an unbalanced force'),
    ('force', 'a push or pull that can change the state of motion, shape or size of an object'),
]
c5s1_mc = [
    ('The mass of an object is a measure of its:', 'inertia', 'velocity', 'momentum', 'acceleration'),
    ('Which has more inertia?', 'A loaded truck', 'A bicycle', 'A football', 'A cricket ball'),
    ('When a bus suddenly starts, passengers fall backwards because of:', 'inertia of rest', 'inertia of motion', 'friction', 'gravity'),
    ('Dust comes out of a carpet when it is beaten with a stick because:', 'the carpet moves but the dust tends to stay at rest due to inertia', 'the stick attracts dust', 'friction pushes dust out', 'dust is pulled by gravity only'),
    ('Seat belts are worn in cars to:', 'prevent passengers from being thrown forward when the car stops suddenly', 'increase the speed of the car', 'reduce the mass of passengers', 'balance the forces on the car'),
    ('If the net force on a moving object becomes zero, the object will:', 'continue to move with the same velocity', 'stop immediately', 'speed up', 'move in a circle'),
]
c5s1_why = [
    ('Why do passengers in a moving bus lean forward when the driver applies brakes suddenly?', 'The lower body stops with the bus, but the upper body tends to continue moving due to inertia of motion.', '1 mark: inertia of motion. 1 mark: explanation.'),
    ('When a card on a glass is flicked quickly, the coin on it falls into the glass. Explain.', 'The card moves away quickly, but the coin, due to inertia of rest, stays in place and falls into the glass under gravity.', '1 mark: inertia of rest. 1 mark: gravity.'),
    ('Why is it advised to tie luggage kept on the roof of a bus with a rope?', 'When the bus starts, stops or turns suddenly, the luggage tends to continue in its state due to inertia and may fall off.', '1 mark: inertia. 1 mark: falls off.'),
]
c5s1_ar = [
    ('A heavier object has more inertia.', 'Inertia depends on the mass of an object.', 'a', 'R explains A.'),
    ('An object in uniform motion must have an unbalanced force on it.', 'Balanced forces do not change the state of motion.', 'd', 'A false: no net force needed for uniform motion; R true.'),
    ('Passengers lean sideways when a car takes a sharp turn.', 'The body tends to continue moving in a straight line due to inertia.', 'a', 'R explains A.'),
]


def c5s1_net(r):
    f1, f2 = r.sample([10, 15, 20, 25, 30, 40, 50, 60], 2)
    obj = r.choice(['a wooden block on a table', 'a trolley', 'a box on the floor'])
    net = abs(f1 - f2)
    return {'stem': f'Two forces of {f1} N to the right and {f2} N to the left act on {obj}. Are the forces balanced? Find the net force and its effect.',
            'answer': f'Unbalanced; net force {net} N towards the {"right" if f1 > f2 else "left"}; the object accelerates in that direction.',
            'key': f'Net force = {max(f1, f2)} − {min(f1, f2)} = {net} N (1 mark); unbalanced, so it changes the state of motion (1 mark).'}


c5s2_defs = [
    ('momentum', 'the product of the mass and the velocity of an object'),
    ('Newton\'s second law of motion', 'the law that the rate of change of momentum of an object is proportional to the applied unbalanced force in the direction of the force'),
    ('one newton', 'the force that produces an acceleration of 1 m/s² in an object of mass 1 kg'),
    ('impulse', 'the product of force and the time for which it acts, equal to the change in momentum'),
]


def c5s2_p(r):
    obj = r.choice([('a cricket ball', 0.16, (20, 40)), ('a car', 1200, (10, 30)), ('a bullet', 0.01, (300, 500)), ('a scooter with rider', 150, (10, 20)), ('a football', 0.45, (10, 25))])
    m = obj[1]
    v = r.randint(*obj[2])
    p = m * v
    return {'stem': f'Find the momentum of {obj[0]} of mass {num(m, 3)} kg moving at {v} m/s.', 'answer': f'{sig(p, 4)} kg m/s',
            'key': f'p = mv = {num(m, 3)} × {v} = {sig(p, 4)} kg m/s.', 'distractors': [f'{sig(m / v, 3)} kg m/s', f'{sig(0.5 * m * v * v, 4)} kg m/s', f'{sig(m + v, 4)} kg m/s']}


def c5s2_fma(r):
    m = r.choice([2, 5, 10, 50, 100, 500, 1000, 1500])
    a = r.choice([0.5, 1, 2, 2.5, 3, 4, 5])
    F = m * a
    return {'stem': f'What force is needed to give a mass of {m} kg an acceleration of {num(a)} m/s²?', 'answer': f'{num(F)} N', 'key': f'F = ma = {m} × {num(a)} = {num(F)} N.',
            'distractors': [f'{num(m / a)} N', f'{num(m + a)} N', f'{num(F * 10)} N']}


def c5s2_stop(r):
    m = r.choice([800, 1000, 1200, 1500])
    v = r.choice([10, 15, 20, 25])
    t = r.choice([2, 4, 5, 8, 10])
    F = m * v / t
    return {'stem': f'A car of mass {m} kg moving at {v} m/s is brought to rest in {t} s. Find the average braking force.', 'answer': f'{num(F)} N (opposite to motion)',
            'key': f'a = (0 − {v})/{t} = −{num(v / t, 2)} m/s²; F = ma = {m} × {num(v / t, 2)} = {num(F)} N, opposite to the motion. (or F = change in momentum ÷ time = {m * v}/{t})',
            'distractors': [f'{num(m * v * t)} N', f'{num(m / v / t, 4)} N', f'{num(m * v)} N']}


def c5s2_change(r):
    m = r.choice([0.15, 0.2, 0.4, 0.5])
    u = r.choice([10, 15, 20])
    v = r.choice([20, 25, 30])
    t = r.choice([0.01, 0.02, 0.05, 0.1])
    dp = m * (v + u)
    F = dp / t
    return {'stem': f'A ball of mass {num(m)} kg moving at {u} m/s is hit back by a bat with a speed of {v} m/s in the opposite direction. The contact lasts {num(t)} s. Find the change in momentum and the average force.',
            'answer': f'Change in momentum {sig(dp, 3)} kg m/s; force {sig(F, 3)} N', 'key': f'Taking the return direction as positive: Δp = m(v − (−u)) = {num(m)} × ({v} + {u}) = {sig(dp, 3)} kg m/s; F = Δp/t = {sig(dp, 3)}/{num(t)} = {sig(F, 3)} N.',
            'gap': 'G2'}


c5s2_mc = [
    ('The SI unit of momentum is:', 'kg m/s', 'N', 'kg m/s²', 'J'),
    ('A cricket fielder draws his hands back while catching a fast ball to:', 'increase the time of impact and reduce the force', 'increase the force', 'reduce the mass of the ball', 'increase the momentum'),
    ('If the same force acts on two masses m and 2m, the acceleration of 2m is:', 'half that of m', 'twice that of m', 'the same as m', 'four times that of m'),
    ('1 N is equal to:', '1 kg m/s²', '1 kg m/s', '1 kg m²/s²', '1 g cm/s²'),
    ('A high jumper lands on a sand bed or foam because it:', 'increases the time to stop and so reduces the force', 'increases the force', 'increases momentum', 'reduces gravity'),
]
c5s2_why = [
    ('Why do high jumpers land on soft foam beds?', 'The foam increases the time taken to stop; for the same change in momentum, the force on the body is less.', '1 mark: time increases. 1 mark: force decreases (F = Δp/t).'),
    ('Why is it easier to stop a tennis ball than a cricket ball moving at the same speed?', 'The cricket ball has more mass, so more momentum; more force or time is needed to stop it.', '1 mark: more mass/momentum. 1 mark: more force needed.'),
    ('Why do vehicles have crumple zones and airbags?', 'They increase the time over which the momentum of passengers changes in a collision, reducing the force on them.', '1 mark: increase time. 1 mark: reduce force.'),
]
c5s2_ar = [
    ('A fielder pulls his hands back while catching a ball.', 'Increasing the time of impact reduces the force for the same change in momentum.', 'a', 'R explains A.'),
    ('A bullet fired from a gun can kill though its mass is small.', 'Its momentum is large because of its very high velocity.', 'a', 'R explains A.'),
    ('Force is equal to mass divided by acceleration.', 'Newton\'s second law gives F = ma.', 'd', 'A false; R true.'),
]

c5s3_defs = [
    ('Newton\'s third law of motion', 'the law that to every action there is an equal and opposite reaction, acting on different objects'),
    ('the law of conservation of momentum', 'the law that the total momentum of a system of objects remains constant if no external unbalanced force acts on it'),
    ('recoil', 'the backward motion of a gun when a bullet is fired'),
]


def c5s3_recoil(r):
    M = r.choice([2, 3, 4, 5])
    m = r.choice([10, 20, 25, 50]) / 1000
    v = r.choice([200, 300, 400, 500])
    V = m * v / M
    return {'stem': f'A bullet of mass {num(m * 1000)} g is fired from a gun of mass {M} kg with a velocity of {v} m/s. Find the recoil velocity of the gun.', 'answer': f'{sig(V, 3)} m/s (backwards)',
            'key': f'Initial momentum = 0. {num(m, 3)} × {v} + {M} × V = 0 ⇒ V = −{sig(V, 3)} m/s (opposite to the bullet).', 'distractors': [f'{sig(V * 1000, 3)} m/s (backwards)', f'{sig(M * v / m, 3)} m/s (backwards)', f'{sig(V, 3)} m/s (forwards)'], 'gap': 'G2'}


def c5s3_stick(r):
    m1, m2 = r.choice([(1, 1), (2, 1), (1.5, 0.5), (3, 2), (4, 1)])
    u1 = r.choice([2, 3, 4, 5, 6])
    v = m1 * u1 / (m1 + m2)
    return {'stem': f'A trolley of mass {num(m1)} kg moving at {u1} m/s collides with a stationary trolley of mass {num(m2)} kg, and they move together. Find their common velocity.',
            'answer': f'{sig(v, 3)} m/s', 'key': f'{num(m1)} × {u1} + {num(m2)} × 0 = ({num(m1)} + {num(m2)}) v ⇒ v = {num(m1 * u1)}/{num(m1 + m2)} = {sig(v, 3)} m/s.',
            'distractors': [f'{sig(u1, 3)} m/s', f'{sig(u1 / 2, 3)} m/s', f'{sig(m2 * u1 / (m1 + m2), 3)} m/s']}


def c5s3_coll(r):
    m1, m2 = r.choice([(0.1, 0.2), (0.2, 0.3), (0.5, 1.0), (1.0, 2.0)])
    u1, u2 = r.choice([(4, 0), (5, 1), (6, 2), (3, -1)])
    v1 = r.choice([1, 0, -1, 2])
    v2 = (m1 * u1 + m2 * u2 - m1 * v1) / m2
    return {'stem': f'Ball A ({num(m1)} kg) moving at {num(u1)} m/s hits ball B ({num(m2)} kg) moving at {num(u2)} m/s along the same line. After the collision A moves at {num(v1)} m/s in its original direction (negative means reversed). Find the velocity of B.',
            'answer': f'{sig(v2, 3)} m/s', 'key': f'm₁u₁ + m₂u₂ = m₁v₁ + m₂v₂ ⇒ {num(m1)}×{num(u1)} + {num(m2)}×{num(u2)} = {num(m1)}×{num(v1)} + {num(m2)}v₂ ⇒ v₂ = {sig(v2, 3)} m/s.'}


c5s3_mc = [
    ('Action and reaction forces:', 'act on different objects', 'act on the same object', 'cancel each other', 'are unequal'),
    ('A rocket moves forward because:', 'hot gases pushed backward exert an equal and opposite force on it', 'air pushes it from behind', 'gravity pulls it up', 'it has inertia'),
    ('When you jump from a boat to the shore, the boat moves:', 'backward', 'forward', 'upward', 'not at all'),
    ('While swimming, a person pushes water backwards. The water pushes the person:', 'forwards', 'backwards', 'downwards', 'sideways'),
    ('In a closed system of colliding balls, which quantity is conserved?', 'Total momentum', 'Velocity of each ball', 'Speed of each ball', 'Direction of each ball'),
]
c5s3_why = [
    ('If action and reaction are equal and opposite, why do they not cancel each other?', 'They act on two different objects, so each produces its own effect.', '1 mark: different objects. 1 mark: no cancellation.'),
    ('Why does a gun recoil when a bullet is fired?', 'The gun pushes the bullet forward; the bullet pushes the gun back with an equal force; total momentum stays zero, so the gun moves backward.', '1 mark: third law. 1 mark: momentum conservation.'),
    ('Why does a fireman find it difficult to hold a hose that ejects water at high speed?', 'The water is pushed forward at high speed; by the third law, an equal reaction force pushes the hose backwards.', '1 mark: reaction. 1 mark: backward push.'),
]
c5s3_ar = [
    ('A gun recoils when a bullet is fired.', 'The total momentum of the gun and bullet remains zero.', 'a', 'R explains A.'),
    ('Action and reaction cancel each other.', 'Action and reaction act on different bodies.', 'd', 'A false; R true.'),
    ('A heavier gun recoils more slowly than a lighter gun for the same bullet.', 'Recoil velocity is inversely proportional to the mass of the gun.', 'a', 'R explains A.'),
]

c5s4_defs = [
    ('friction', 'the force that opposes the relative motion between two surfaces in contact'),
    ('static friction', 'the friction that prevents an object from starting to move'),
    ('rolling friction', 'the friction when one object rolls over another, much smaller than sliding friction'),
]
c5s4_mc = [
    ('A ball rolling on the ground slows down and stops because of:', 'friction', 'inertia', 'momentum', 'reaction'),
    ('Friction can be reduced by:', 'using lubricants and ball bearings', 'roughening surfaces', 'increasing the weight', 'using sand'),
    ('A force of 20 N is needed to keep a box moving at constant speed on a floor. The friction on it is:', '20 N opposite to motion', 'zero', '40 N', '10 N'),
    ('Which friction is the largest?', 'Static friction', 'Sliding friction', 'Rolling friction', 'Fluid friction'),
]


def c5s4_fr(r):
    F = r.choice([50, 60, 80, 100, 120])
    f = r.choice([20, 30, 40])
    m = r.choice([10, 20, 25])
    a = (F - f) / m
    return {'stem': f'A box of mass {m} kg is pushed along a floor with a force of {F} N. The friction force is {f} N. Find the acceleration of the box.', 'answer': f'{num(a, 2)} m/s²',
            'key': f'Net force = {F} − {f} = {F - f} N; a = {F - f}/{m} = {num(a, 2)} m/s².', 'distractors': [f'{num(F / m, 2)} m/s²', f'{num((F + f) / m, 2)} m/s²', f'{num(f / m, 2)} m/s²']}


c5s4_why = [
    ('Why does a car need a continuous push from its engine to move at constant velocity on a level road?', 'Friction and air resistance oppose the motion; the engine force balances them, so the net force is zero and velocity stays constant.', '1 mark: opposing forces. 1 mark: balanced, constant velocity.'),
    ('Why do roads become dangerous after the first rain of the season?', 'Water mixes with oil and dust to make a slippery layer, reducing friction between tyres and road.', '1 mark: slippery layer. 1 mark: less friction.'),
]
c5s4_ar = [
    ('Friction always opposes motion.', 'Friction acts opposite to the direction of relative motion.', 'a', 'R explains A.'),
    ('An object moving at constant velocity on a rough floor has no force on it.', 'The applied force balances friction.', 'd', 'A false: forces act but are balanced; R true.'),
]
c5_hots = [
    ('A truck and a car are moving with the same momentum. If the same braking force acts on both, which stops first? Which travels farther before stopping?', 'Same momentum and same force ⇒ same stopping time (t = p/F). Car has smaller mass, hence greater velocity, so it travels farther (s = p²/2mF is larger for the smaller mass).', '1 mark: same time. 1 mark: car farther. 1 mark: reasoning.'),
    ('An astronaut floating in space throws a 2 kg tool at 3 m/s away from the spacecraft. If her mass with suit is 100 kg, what happens to her and why?', 'She moves in the opposite direction at 2 × 3 ÷ 100 = 0.06 m/s, because total momentum must stay zero (no external force).', '1 mark: direction. 1 mark: 0.06 m/s. 1 mark: conservation.'),
    ('Explain using Newton\'s laws why it is dangerous to jump out of a moving bus.', 'Feet stop on touching the ground, but the body keeps moving forward due to inertia (first law), so the person falls forward; the large change in momentum in a short time gives a large force (second law).', '1 mark: inertia. 1 mark: falls forward. 1 mark: force.'),
    ('Two identical trolleys are tied together with a compressed spring between them and are at rest. The string is cut. Predict their motion and explain.', 'They move apart in opposite directions with equal speeds: the spring pushes both equally (third law) and the total momentum stays zero.', '1 mark: opposite directions. 1 mark: equal speeds. 1 mark: reasoning.'),
]


def c5_case(r):
    who = name(r)
    m = r.choice([60, 70, 80])
    v = r.choice([10, 15, 20])
    t1, t2 = r.choice([(0.1, 0.5), (0.05, 0.4), (0.1, 1.0)])
    p = m * v
    return {'stem': (f'Read: In a crash test, a dummy of mass {m} kg moving at {v} m/s is stopped in {num(t1)} s when it hits the dashboard, but in {num(t2)} s when an airbag opens.\n'
                     f'(i) Find the momentum of the dummy before the crash. (ii) Find the average force without the airbag. (iii) Find the average force with the airbag. (iv) Which law explains why the airbag reduces injury?'),
            'answer': f'(i) {p} kg m/s. (ii) {num(p / t1)} N. (iii) {num(p / t2)} N. (iv) Newton\'s second law (F = change in momentum ÷ time).',
            'key': '1 mark each part.'}


c5_long = [
    ('State Newton\'s three laws of motion with one everyday example of each. A force of 5 N gives a mass m₁ an acceleration of 10 m/s² and a mass m₂ an acceleration of 20 m/s². What acceleration will it give if both masses are tied together?',
     'First: object stays at rest or uniform motion unless an unbalanced force acts (passengers jerk forward on braking). Second: F = ma / rate of change of momentum (catching a ball by pulling hands back). Third: equal and opposite reaction on different bodies (recoil of a gun). m₁ = 0.5 kg, m₂ = 0.25 kg; a = 5/0.75 = 6.67 m/s².',
     '3 marks laws with examples; 2 marks numerical.'),
    ('State the law of conservation of momentum and derive it from Newton\'s third law for two colliding balls. A 50 g bullet is fired from a 4 kg rifle at 35 m/s; find the recoil velocity of the rifle.',
     'Total momentum of an isolated system stays constant. In a collision, F_AB = −F_BA over the same time t, so m_A(v_A − u_A) = −m_B(v_B − u_B), giving m_Au_A + m_Bu_B = m_Av_A + m_Bv_B. Recoil: 0.05 × 35 = 4 × v ⇒ v = 0.4375 ≈ 0.44 m/s backward.',
     '1 mark law; 2 marks derivation; 2 marks numerical.'),
]

# ======================= ch06 Work, Energy and Simple Machines
c6s1_defs = [
    ('work', 'the product of the force and the displacement of the object in the direction of the force'),
    ('one joule', 'the work done when a force of 1 N moves an object through 1 m in the direction of the force'),
    ('negative work', 'work done when the force acts opposite to the direction of displacement, such as friction'),
]


def c6s1_w(r):
    F = r.choice([5, 10, 20, 25, 40, 50, 75, 100, 150])
    s = r.choice([2, 3, 4, 5, 8, 10, 12, 20])
    return {'stem': f'A force of {F} N moves a trolley through {s} m in the direction of the force. How much work is done?', 'answer': f'{F * s} J',
            'key': f'W = F × s = {F} × {s} = {F * s} J.', 'distractors': [f'{num(F / s, 2)} J', f'{F + s} J', f'{F * s * 10} J']}


def c6s1_lift(r):
    who = name(r)
    m = r.choice([5, 10, 15, 20, 25, 40])
    h = r.choice([1.5, 2, 3, 4, 5, 6, 10])
    W = m * 10 * h
    return {'stem': f'{who} lifts a {m} kg bag of wheat to a shelf {num(h)} m high. How much work is done against gravity? (g = 10 m/s²)', 'answer': f'{num(W)} J',
            'key': f'W = mgh = {m} × 10 × {num(h)} = {num(W)} J.', 'distractors': [f'{num(m * h)} J', f'{num(m * 10 / h, 2)} J', f'{num(W / 10)} J']}


c6s1_cats = {
    'a case where work is done (scientifically)': ['a girl pulling a trolley across a room', 'a crane lifting a load', 'a boy climbing stairs', 'a horse pulling a cart', 'pushing a car to start it'],
    'a case where no work is done (scientifically)': ['a porter standing still with a load on his head', 'pushing a wall that does not move', 'a satellite moving in a circular orbit due to gravity', 'holding a heavy book still in your hand'],
}
c6s1_mc = [
    ('Work done is zero when the displacement is:', 'perpendicular to the force', 'along the force', 'opposite to the force', 'very large'),
    ('The SI unit of work is:', 'joule', 'watt', 'newton', 'pascal'),
    ('The work done by friction on a sliding box is:', 'negative', 'positive', 'zero', 'infinite'),
    ('1 J is equal to:', '1 N m', '1 N/m', '1 kg m/s', '1 W/s'),
]
c6s1_why = [
    ('A porter carries a box on his head and walks on a level platform. Is he doing work against gravity? Explain.', 'No. The force he applies is upward while the displacement is horizontal (perpendicular), so work against gravity is zero.', '1 mark: no. 1 mark: perpendicular.'),
    ('Why is no work done when you push a wall with all your strength?', 'There is no displacement of the wall, so W = F × 0 = 0.', '1 mark: no displacement. 1 mark: W = 0.'),
]
c6s1_ar = [
    ('No work is done on a satellite by the gravitational force in a circular orbit.', 'The force of gravity is perpendicular to the direction of motion of the satellite.', 'a', 'R explains A.'),
    ('Work is a vector quantity.', 'Work has magnitude only.', 'd', 'A false; R true.'),
]

c6s2_defs = [
    ('kinetic energy', 'the energy possessed by an object due to its motion'),
    ('potential energy', 'the energy possessed by an object due to its position or change in shape'),
    ('the law of conservation of energy', 'the law that energy can neither be created nor destroyed but only changed from one form to another'),
    ('mechanical energy', 'the sum of the kinetic and potential energies of an object'),
]


def c6s2_ke(r):
    m = r.choice([0.5, 1, 2, 5, 10, 50, 60, 1000])
    v = r.choice([2, 3, 4, 5, 6, 10, 20])
    K = 0.5 * m * v * v
    return {'stem': f'Find the kinetic energy of an object of mass {num(m)} kg moving with a velocity of {v} m/s.', 'answer': f'{num(K)} J',
            'key': f'KE = ½mv² = ½ × {num(m)} × {v}² = {num(K)} J.', 'distractors': [f'{num(m * v * v)} J', f'{num(0.5 * m * v)} J', f'{num(m * v)} J']}


def c6s2_pe(r):
    m = r.choice([1, 2, 5, 10, 20, 50])
    h = r.choice([2, 3, 5, 8, 10, 15, 20])
    P = m * 10 * h
    return {'stem': f'An object of mass {m} kg is raised to a height of {h} m. Find its potential energy. (g = 10 m/s²)', 'answer': f'{P} J',
            'key': f'PE = mgh = {m} × 10 × {h} = {P} J.', 'distractors': [f'{m * h} J', f'{num(0.5 * m * h * h)} J', f'{P * 10} J']}


def c6s2_fall(r):
    m = r.choice([1, 2, 4, 5])
    h = r.choice([5, 10, 20, 45, 80])
    v = math.sqrt(2 * 10 * h)
    half = h / 2
    return {'stem': f'A ball of mass {m} kg is dropped from a height of {h} m. Find (i) its potential energy at the top, (ii) its kinetic energy and potential energy halfway down, (iii) its speed just before hitting the ground. (g = 10 m/s², ignore air resistance)',
            'answer': f'(i) {m * 10 * h} J (ii) KE = PE = {num(m * 10 * half)} J (iii) {sig(v, 3)} m/s',
            'key': f'(i) mgh = {m * 10 * h} J. (ii) At {num(half)} m: PE = {num(m * 10 * half)} J, KE = {m * 10 * h} − {num(m * 10 * half)} = {num(m * 10 * half)} J. (iii) ½mv² = mgh ⇒ v = √(2gh) = √{2 * 10 * h} = {sig(v, 3)} m/s.'}


def c6s2_double(r):
    k = r.choice([2, 3, 4])
    return {'stem': f'By what factor does the kinetic energy of a car change if its speed becomes {k} times?', 'answer': f'{k * k} times',
            'key': f'KE ∝ v²; ({k})² = {k * k}.', 'distractors': [f'{k} times', f'{2 * k} times', f'{k * k * k} times']}


c6s2_cats = {
    'an object possessing kinetic energy': ['a moving cricket ball', 'flowing river water', 'wind turning a windmill', 'a running athlete', 'a speeding bullet'],
    'an object possessing potential energy': ['water stored in a dam', 'a stretched rubber band', 'a wound-up spring of a toy car', 'a stone kept on a rooftop', 'a drawn bow'],
}
c6s2_mc = [
    ('When a ball is thrown upwards, at its highest point its:', 'kinetic energy is minimum and potential energy is maximum', 'kinetic energy is maximum', 'potential energy is zero', 'total energy is zero'),
    ('The energy stored in a wound-up spring of a toy car is:', 'elastic potential energy', 'kinetic energy', 'chemical energy', 'heat energy'),
    ('When the speed of an object is doubled, its kinetic energy becomes:', 'four times', 'double', 'half', 'the same'),
    ('In a hydroelectric power station, the energy of water stored in a dam changes from:', 'potential to kinetic to electrical', 'kinetic to chemical', 'chemical to electrical', 'electrical to potential'),
]
c6s2_why = [
    ('A freely falling ball: does the law of conservation of energy hold? Explain.', 'Yes. As it falls, potential energy decreases and kinetic energy increases by the same amount; the sum stays constant (ignoring air resistance).', '1 mark: PE → KE. 1 mark: total constant.'),
    ('Why does a stretched bow have energy?', 'Work done in stretching it is stored as elastic potential energy, which is released as kinetic energy of the arrow.', '1 mark: work stored. 1 mark: released as KE.'),
    ('What happens to the energy of a ball bouncing on the floor that finally stops?', 'It is converted into heat and sound at each bounce; energy is not destroyed but changes form.', '1 mark: heat and sound. 1 mark: conservation.'),
]
c6s2_ar = [
    ('The kinetic energy of an object becomes four times when its speed is doubled.', 'Kinetic energy is proportional to the square of velocity.', 'a', 'R explains A.'),
    ('An object at rest has no energy.', 'An object at rest can have potential energy due to its position.', 'd', 'A false; R true.'),
    ('The total mechanical energy of a freely falling body stays constant.', 'Loss in potential energy equals gain in kinetic energy.', 'a', 'R explains A.'),
]

c6s3_defs = [
    ('power', 'the rate of doing work or of transferring energy'),
    ('one watt', 'the power of an agent that does work at the rate of 1 joule per second'),
    ('a kilowatt hour', 'the energy used in one hour at the rate of 1000 J/s; the commercial unit of energy equal to 3.6 × 10⁶ J'),
]


def c6s3_p(r):
    who = name(r)
    m = r.choice([40, 45, 50, 55, 60])
    h = r.choice([3, 4.5, 6, 9, 12])
    t = r.choice([5, 6, 8, 10, 12, 15])
    P = m * 10 * h / t
    return {'stem': f'{who} (mass {m} kg) runs up a staircase of height {num(h)} m in {t} s. Find the power developed. (g = 10 m/s²)', 'answer': f'{sig(P, 3)} W',
            'key': f'Work = mgh = {m} × 10 × {num(h)} = {num(m * 10 * h)} J; P = W/t = {num(m * 10 * h)}/{t} = {sig(P, 3)} W.',
            'distractors': [f'{sig(m * h / t, 3)} W', f'{sig(m * 10 * h * t, 3)} W', f'{sig(m * 10 * h, 3)} W']}


def c6s3_bill(r):
    apps = r.sample([('LED bulbs', 10, 5, 6), ('ceiling fans', 75, 3, 10), ('a television', 120, 1, 4), ('a refrigerator', 200, 1, 24), ('an electric iron', 1000, 1, 0.5), ('a geyser', 2000, 1, 1)], 2)
    rate = r.choice([6, 7, 7.5, 8])
    days = 30
    rows = []
    units = 0
    for n, w, k, hrs in apps:
        e = w * k * hrs / 1000
        units += e
        rows.append(f'{k} {n} of {w} W each for {num(hrs)} h a day' if k > 1 else f'{n} of {w} W for {num(hrs)} h a day')
    U = units * days
    cost = U * rate
    return {'stem': f'A house in Indore uses {rows[0]} and {rows[1]}. Find the electricity used in {days} days in kWh and the cost at ₹{num(rate)} per unit.',
            'answer': f'{num(U, 2)} kWh; {inr(round(cost, 2))}', 'key': f'Daily energy = ' + ' + '.join(f'{w * k} W × {num(hrs)} h' for n, w, k, hrs in apps) + f' = {num(units, 3)} kWh; × {days} = {num(U, 2)} kWh; cost = {num(U, 2)} × {num(rate)} = {inr(round(cost, 2))}.'}


def c6s3_kwh(r):
    k = r.choice([2, 3, 5, 10, 0.5, 1.5])
    return {'stem': f'Express {num(k)} kWh in joules.', 'answer': f'{sig(k * 3.6, 3)} × 10⁶ J', 'key': f'1 kWh = 1000 W × 3600 s = 3.6 × 10⁶ J; {num(k)} × 3.6 × 10⁶ = {sig(k * 3.6, 3)} × 10⁶ J.',
            'distractors': [f'{sig(k * 3.6, 3)} × 10³ J', f'{num(k * 1000)} J', f'{sig(k * 36, 3)} × 10⁶ J']}


c6s3_mc = [
    ('The commercial unit of energy is:', 'kilowatt hour', 'watt', 'joule', 'kilowatt'),
    ('1 horsepower is about:', '746 W', '1000 W', '100 W', '3.6 × 10⁶ W'),
    ('An electric bulb is rated 60 W. This means it uses:', '60 J of energy every second', '60 J every hour', '60 kWh every second', '60 W every hour'),
]
c6s3_why = [
    ('Two students of the same mass climb the same staircase, one in 10 s and the other in 20 s. Who does more work and who develops more power?', 'Both do the same work (mgh); the one who takes 10 s develops twice the power.', '1 mark: same work. 1 mark: faster has more power.'),
    ('Why is the kilowatt hour used for electricity bills instead of the joule?', 'The joule is too small; household energy use is millions of joules, so the larger unit kWh (3.6 × 10⁶ J) is convenient.', '1 mark: J too small. 1 mark: conversion.'),
]
c6s3_ar = [
    ('A 100 W bulb uses more energy than a 60 W bulb in the same time.', 'Energy used = power × time.', 'a', 'R explains A.'),
    ('The kilowatt hour is a unit of power.', '1 kWh = 3.6 × 10⁶ J.', 'd', 'A false: it is a unit of energy; R true.'),
]

c6s4_defs = [
    ('a simple machine', 'a device that makes work easier by changing the size or direction of a force'),
    ('mechanical advantage', 'the ratio of the load to the effort applied in a machine'),
    ('velocity ratio', 'the ratio of the distance moved by the effort to the distance moved by the load'),
    ('efficiency of a machine', 'the ratio of useful work output to the work input, usually expressed as a percentage'),
    ('the fulcrum', 'the fixed point about which a lever turns'),
]
c6s4_lev = {
    'a class I lever (fulcrum between load and effort)': ['a see-saw', 'a pair of scissors', 'a crowbar', 'a beam balance', 'pliers'],
    'a class II lever (load between fulcrum and effort)': ['a nutcracker', 'a wheelbarrow', 'a bottle opener', 'a paper cutter'],
    'a class III lever (effort between fulcrum and load)': ['a pair of tongs', 'a fishing rod', 'the human forearm', 'a broom used for sweeping', 'tweezers'],
}


def c6s4_ma(r):
    L = r.choice([200, 300, 400, 500, 600, 800, 1000])
    E = r.choice([50, 80, 100, 125, 150, 200, 250])
    if E >= L:
        E = L // 4
    return {'stem': f'A machine lifts a load of {L} N with an effort of {E} N. What is its mechanical advantage?', 'answer': num(L / E, 2),
            'key': f'MA = load/effort = {L}/{E} = {num(L / E, 2)}.', 'distractors': [num(E / L, 3), num(L * E), num(L - E)]}


def c6s4_eff(r):
    L = r.choice([500, 600, 800, 1000, 1200])
    E = r.choice([150, 200, 250, 300])
    d_l = r.choice([1, 2])
    d_e = r.choice([4, 5, 6, 8])
    MA = L / E
    VR = d_e / d_l
    eff = 100 * MA / VR
    if eff > 100 or eff < 30:
        raise ValueError
    return {'stem': f'Using a pulley system, an effort of {E} N moving through {d_e} m raises a load of {L} N through {d_l} m. Find the mechanical advantage, velocity ratio and efficiency.',
            'answer': f'MA = {num(MA, 2)}; VR = {num(VR, 2)}; efficiency = {sig(eff, 3)}%', 'key': f'MA = {L}/{E} = {num(MA, 2)}; VR = {d_e}/{d_l} = {num(VR, 2)}; efficiency = MA/VR × 100 = {sig(eff, 3)}% (or work out/work in = {L * d_l}/{E * d_e} × 100).'}


def c6s4_lever(r):
    load = r.choice([100, 150, 200, 300, 400])
    lb = r.choice([0.2, 0.25, 0.3, 0.4, 0.5])
    eb = r.choice([1, 1.2, 1.5, 2])
    E = load * lb / eb
    return {'stem': f'A crowbar is used to lift a stone of weight {load} N. The stone is {num(lb)} m from the fulcrum and the effort is applied {num(eb)} m from the fulcrum on the other side. Find the effort needed.',
            'answer': f'{sig(E, 3)} N', 'key': f'Load × load arm = effort × effort arm ⇒ {load} × {num(lb)} = E × {num(eb)} ⇒ E = {sig(E, 3)} N.', 'distractors': [f'{sig(load * eb / lb, 3)} N', f'{load} N', f'{sig(load / eb, 3)} N']}


def c6s4_incline(r):
    L = r.choice([500, 600, 800, 1000])
    h = r.choice([1, 1.5, 2])
    l = r.choice([4, 5, 6, 8])
    E = L * h / l
    return {'stem': f'A loader pushes a {L} N drum up a smooth ramp {l} m long onto a truck {num(h)} m high. Find the effort needed (ignore friction) and the mechanical advantage of the ramp.',
            'answer': f'Effort {sig(E, 3)} N; MA = {num(l / h, 2)}', 'key': f'Work in = work out: E × {l} = {L} × {num(h)} ⇒ E = {sig(E, 3)} N; MA = {L}/{sig(E, 3)} = {num(l / h, 2)} (= length/height).'}


c6s4_mc = [
    ('A single fixed pulley:', 'changes the direction of the force but gives MA = 1', 'reduces the effort to half', 'increases the load', 'has MA = 2'),
    ('The efficiency of a real machine is always less than 100% because:', 'some energy is lost in overcoming friction', 'machines create energy', 'the load is too small', 'effort is always zero'),
    ('A ramp makes it easier to load a truck because:', 'a smaller force is applied over a longer distance', 'it reduces the weight of the load', 'it reduces the work done to zero', 'it increases the height'),
    ('A machine with mechanical advantage less than 1, such as tongs, is used to gain:', 'speed or convenience of movement', 'force', 'energy', 'mass'),
]
c6s4_why = [
    ('Why do we use a long handle to open a heavy door or a tight nut?', 'A longer effort arm means a smaller effort is needed for the same turning effect (moment).', '1 mark: long effort arm. 1 mark: less effort.'),
    ('Why are mountain roads made winding instead of going straight up?', 'A winding road is like an inclined plane with a gentle slope; vehicles need less force (over a longer distance) to climb.', '1 mark: inclined plane. 1 mark: less force.'),
    ('Can a machine give more work output than input? Explain.', 'No. By conservation of energy, output can at most equal input; friction makes it less.', '1 mark: no. 1 mark: conservation/friction.'),
]
c6s4_ar = [
    ('A nutcracker is a class II lever.', 'In a nutcracker, the load lies between the fulcrum and the effort.', 'a', 'R explains A.'),
    ('A simple machine reduces the work needed to lift a load.', 'A simple machine reduces the effort needed.', 'd', 'A false: work is not reduced; R true.'),
    ('Efficiency of a machine can never exceed 100%.', 'Energy cannot be created.', 'a', 'R explains A.'),
]
c6_hots = [
    ('A 1500 W electric motor lifts 300 kg of water to a tank 15 m high in 1 minute. Find the useful work done, the electrical energy used and the efficiency of the motor. (g = 10 m/s²)', 'Useful work = 300 × 10 × 15 = 45 000 J; energy used = 1500 × 60 = 90 000 J; efficiency = 45 000/90 000 × 100 = 50%.', '1 mark each.'),
    ('A cyclist stops pedalling on a level road and the cycle slows down. Where has the kinetic energy gone? Is energy conserved?', 'It is converted into heat (and some sound) by friction in the bearings and between tyres and road and by air resistance; total energy is conserved.', '1 mark: heat/sound. 1 mark: friction/air. 1 mark: conserved.'),
    ('Why does a car use much more fuel when driven at 120 km/h than at 60 km/h over the same distance?', 'Kinetic energy at 120 km/h is four times that at 60 km/h, and air resistance grows rapidly with speed, so the engine must do much more work per kilometre.', '1 mark: KE ∝ v². 1 mark: air resistance. 1 mark: more work.'),
    ('A ball is dropped from 5 m and bounces back to 3.2 m. What fraction of its energy is lost on the bounce, and where does it go?', 'Energy is proportional to height: lost = (5 − 3.2)/5 = 0.36, i.e. 36%; it turns into heat and sound at impact.', '1 mark: proportional to height. 1 mark: 36%. 1 mark: heat and sound.'),
]


def c6_case(r):
    m = r.choice([1000, 1500, 2000])
    h = r.choice([20, 30, 45, 50])
    t = r.choice([20, 30, 40, 60])
    P = m * 10 * h / t
    return {'stem': (f'Read: At a construction site in Gurugram, a crane lifts a {m} kg slab of concrete to the {h} m high floor in {t} s at steady speed.\n'
                     f'(i) Find the work done against gravity. (ii) Find the power of the crane. (iii) How much potential energy does the slab gain? (iv) If the crane\'s motor is 80% efficient, what electrical power does it draw? (g = 10 m/s²)'),
            'answer': f'(i) {m * 10 * h} J. (ii) {num(P)} W. (iii) {m * 10 * h} J. (iv) {num(P / 0.8)} W.', 'key': '1 mark each part.'}


c6_long = [
    ('Define kinetic and potential energy and derive the expression for kinetic energy. Show that the mechanical energy of a freely falling body is conserved at the top, midway and just before hitting the ground.',
     'KE = energy of motion; PE = energy due to position/shape. Work done to accelerate m from rest to v: W = F × s = ma × v²/2a = ½mv². Falling from h: top PE = mgh, KE = 0; midway PE = mgh/2, KE = mgh/2; bottom PE = 0, KE = ½mv² = mgh. Sum = mgh throughout.',
     '1 mark definitions; 2 marks derivation; 2 marks conservation.'),
    ('What is power? Distinguish between watt and kilowatt hour. A family uses 4 tube lights of 40 W for 6 h, a 1 kW heater for 2 h and a 200 W refrigerator for 24 h daily. Find the energy used in 30 days and the bill at ₹8 per unit.',
     'Power = work/time. Watt = 1 J/s (unit of power); kWh = 3.6 × 10⁶ J (unit of energy). Daily: 0.96 + 2 + 4.8 = 7.76 kWh; 30 days = 232.8 kWh; bill = ₹1,862.40.',
     '1 mark definition; 1 mark distinction; 3 marks numerical.'),
]

# ======================= ch07 Journey Inside the Atom
c7s1_disc = [
    ('electron', 'J. J. Thomson', 'cathode rays'), ('proton', 'E. Goldstein', 'canal rays (anode rays)'), ('neutron', 'J. Chadwick', 'bombarding beryllium with alpha particles'),
]
c7s1_defs = [
    ('an electron', 'a negatively charged sub-atomic particle with a mass about 1/2000 of that of a hydrogen atom'),
    ('a proton', 'a positively charged sub-atomic particle with a mass of about 1 u'),
    ('a neutron', 'a sub-atomic particle with no charge and a mass nearly equal to that of a proton'),
    ('canal rays', 'positively charged radiations discovered by Goldstein in a gas discharge tube'),
    ('the nucleus', 'the small, dense, positively charged centre of an atom containing protons and neutrons'),
]


def c7s1_who(r):
    p, s, how = r.choice(c7s1_disc)
    wrong = [x[1] for x in c7s1_disc if x[1] != p and x[1] != s] + ['E. Rutherford', 'Niels Bohr']
    return mcq(f'Who is credited with the discovery of the {p}?', s, r.sample([w for w in wrong if w != s], 3), f'The {p} was discovered by {s} ({how}).', r)


c7s1_mc = [
    ('Which sub-atomic particle is absent in an ordinary hydrogen atom (protium)?', 'Neutron', 'Proton', 'Electron', 'None'),
    ('The mass of an electron is about:', '1/2000 of the mass of a proton', 'equal to the mass of a proton', 'twice the mass of a neutron', 'zero'),
    ('The charge on a proton is:', '+1', '−1', '0', '+2'),
    ('Which particles are found in the nucleus?', 'Protons and neutrons', 'Electrons and protons', 'Electrons only', 'Electrons and neutrons'),
]
c7s1_why = [
    ('Why is an atom electrically neutral?', 'It has equal numbers of protons (positive) and electrons (negative), whose charges cancel.', '1 mark: equal numbers. 1 mark: charges cancel.'),
    ('Why was the neutron discovered last?', 'It has no charge, so it is not deflected by electric or magnetic fields and is hard to detect.', '1 mark: no charge. 1 mark: hard to detect.'),
]
c7s1_ar = [
    ('An atom is electrically neutral.', 'The number of protons equals the number of electrons in an atom.', 'a', 'R explains A.'),
    ('The mass of an atom is concentrated in its electrons.', 'Electrons are much lighter than protons.', 'd', 'A false; R true.'),
]

c7s2_defs = [
    ('Thomson\'s model of the atom', 'the model in which an atom is a positively charged sphere with electrons embedded in it, like seeds in a watermelon'),
    ('Rutherford\'s model of the atom', 'the model with a small, dense, positive nucleus at the centre and electrons revolving around it'),
    ('Bohr\'s model of the atom', 'the model in which electrons revolve only in certain discrete orbits (energy levels) without radiating energy'),
    ('a shell (energy level)', 'a discrete orbit around the nucleus in which electrons revolve, named K, L, M, N'),
]
c7s2_obs = [
    ('Most α-particles passed straight through the gold foil.', 'Most of the space inside the atom is empty.'),
    ('Some α-particles were deflected through small angles.', 'The positive charge occupies very little space.'),
    ('Very few (about 1 in 12 000) α-particles bounced back.', 'All the positive charge and most of the mass are concentrated in a very small nucleus.'),
]


def c7s2_concl(r):
    o, c = r.choice(c7s2_obs)
    wrong = [x[1] for x in c7s2_obs if x[1] != c] + ['Electrons are embedded in a positive sphere.']
    return mcq(f'In Rutherford\'s α-particle scattering experiment: "{o}" What did he conclude from this?', c, wrong, f'{o} ⇒ {c}', r)


c7s2_mc = [
    ('Rutherford used a gold foil because:', 'gold can be beaten into a very thin foil (about 1000 atoms thick)', 'gold is magnetic', 'gold is a non-metal', 'gold has no nucleus'),
    ('The main drawback of Rutherford\'s model was that:', 'a revolving electron should lose energy and fall into the nucleus, so the atom would be unstable', 'it had no nucleus', 'it had no electrons', 'it showed electrons embedded in a sphere'),
    ('Thomson\'s model failed to explain:', 'the results of Rutherford\'s scattering experiment', 'the neutrality of the atom', 'the presence of electrons', 'the positive charge'),
    ('The radius of the nucleus is about ______ times smaller than the radius of the atom.', '10⁵', '10', '100', '10²⁰'),
    ('In Bohr\'s model, electrons in discrete orbits:', 'do not radiate energy', 'continuously radiate energy', 'fall into the nucleus', 'have no energy'),
]
c7s2_why = [
    ('Why did most α-particles pass straight through the gold foil?', 'Most of the atom is empty space; the tiny nucleus occupies very little volume.', '1 mark: empty space. 1 mark: tiny nucleus.'),
    ('How did Bohr\'s model overcome the drawback of Rutherford\'s model?', 'Bohr proposed that electrons revolve only in certain permitted orbits in which they do not radiate energy, so the atom is stable.', '1 mark: discrete orbits. 1 mark: no energy loss/stable.'),
]
c7s2_ar = [
    ('Very few α-particles bounced back from the gold foil.', 'The nucleus is very small and contains all the positive charge.', 'a', 'R explains A.'),
    ('Thomson\'s model explained the α-scattering results.', 'Thomson\'s model spread positive charge throughout the atom.', 'd', 'A false; R true.'),
    ('Electrons in Bohr\'s orbits do not lose energy.', 'Electrons revolve only in permitted discrete orbits.', 'a', 'R explains A.'),
]

ELEM = [('hydrogen', 'H', 1, 1), ('helium', 'He', 2, 4), ('lithium', 'Li', 3, 7), ('beryllium', 'Be', 4, 9), ('boron', 'B', 5, 11), ('carbon', 'C', 6, 12),
        ('nitrogen', 'N', 7, 14), ('oxygen', 'O', 8, 16), ('fluorine', 'F', 9, 19), ('neon', 'Ne', 10, 20), ('sodium', 'Na', 11, 23), ('magnesium', 'Mg', 12, 24),
        ('aluminium', 'Al', 13, 27), ('silicon', 'Si', 14, 28), ('phosphorus', 'P', 15, 31), ('sulphur', 'S', 16, 32), ('chlorine', 'Cl', 17, 35), ('argon', 'Ar', 18, 40),
        ('potassium', 'K', 19, 39), ('calcium', 'Ca', 20, 40)]


def config(z: int) -> list:
    out = []
    for cap_ in (2, 8, 8, 2):
        if z <= 0:
            break
        out.append(min(z, cap_))
        z -= min(z, cap_)
    return out


def valency(z: int) -> int:
    v = config(z)[-1]
    if z in (2, 10, 18):
        return 0
    return v if v <= 4 else 8 - v


def c7s3_conf(r):
    n, s, z, a = r.choice(ELEM[2:])
    c = config(z)
    ans = ', '.join(map(str, c))
    wrong = set()
    alt = [c[:-1] + [c[-1] + 1] if len(c) else [], [2] + [z - 2] if z > 2 else [1], c[::-1] if len(c) > 1 else [z]]
    for w in alt:
        ws = ', '.join(map(str, w))
        if ws != ans and sum(w) > 0:
            wrong.add(ws)
    while len(wrong) < 3:
        w = c[:]
        i = r.randrange(len(w))
        w[i] = max(1, w[i] + r.choice([-1, 1]))
        ws = ', '.join(map(str, w))
        if ws != ans:
            wrong.add(ws)
    return mcq(f'The electronic configuration of {n} (atomic number {z}) is:', ans, list(wrong)[:3], f'K, L, M shells hold at most 2, 8, 8 (in this range): {s} = {ans}.', r)


def c7s3_val(r):
    n, s, z, a = r.choice(ELEM[2:])
    c = config(z)
    v = valency(z)
    how = ('a full outer shell (octet/duplet), so it does not combine' if v == 0 else
           f'it {"loses" if c[-1] <= 3 else "shares or gains"} {v} electron{"s" if v != 1 else ""} to complete its octet')
    return {'stem': f'Write the electronic configuration of {n} (Z = {z}) and find its valency.', 'answer': f'{", ".join(map(str, c))}; valency {v}',
            'key': f'Configuration {", ".join(map(str, c))} (1 mark). Outer shell has {c[-1]} electron{"s" if c[-1] != 1 else ""}; {how}, so valency = {v} (1 mark).',
            'distractors': [f'{", ".join(map(str, c))}; valency {c[-1]}' if c[-1] != v else f'{", ".join(map(str, c))}; valency {8 - v}', f'{", ".join(map(str, c))}; valency {v + 1}', f'{", ".join(map(str, c[::-1]))}; valency {v}']}


def c7s3_ident(r):
    n, s, z, a = r.choice(ELEM[2:])
    c = config(z)
    return {'stem': f'An element has the electronic configuration {", ".join(map(str, c))}. Identify the element, its atomic number and whether it is a metal or a non-metal.',
            'answer': f'{cap(n)} ({s}), Z = {z}, {"a metal" if n in ("lithium", "beryllium", "sodium", "magnesium", "aluminium", "potassium", "calcium") else "a noble gas" if z in (2, 10, 18) else "a metalloid" if n in ("boron", "silicon") else "a non-metal"}.',
            'key': f'Total electrons = {z} = atomic number; {n}. (1 mark each part)'}


c7s3_mc = [
    ('The maximum number of electrons in a shell is given by:', '2n²', 'n²', '2n', '8n'),
    ('The maximum number of electrons in the M shell (n = 3) is:', '18', '8', '32', '2'),
    ('Elements with a completely filled outermost shell, such as neon, have valency:', 'zero', 'one', 'eight', 'two'),
    ('The outermost shell of an atom can hold at most ______ electrons.', '8', '18', '2', '32'),
]
c7s3_why = [
    ('Why are noble gases chemically unreactive?', 'Their outermost shells are completely filled (octet; duplet for helium), so they have no tendency to gain, lose or share electrons.', '1 mark: full shell. 1 mark: no tendency to react.'),
    ('Why does sodium (2, 8, 1) form Na⁺ easily?', 'It loses its single outer electron to attain the stable configuration of neon (2, 8).', '1 mark: loses one electron. 1 mark: stable octet.'),
    ('Why is the valency of chlorine 1 and not 7?', 'Chlorine (2, 8, 7) needs only one electron to complete its octet, which is easier than losing seven.', '1 mark: gains 1. 1 mark: easier than losing 7.'),
]
c7s3_ar = [
    ('The valency of magnesium is 2.', 'Magnesium (2, 8, 2) loses two electrons to attain an octet.', 'a', 'R explains A.'),
    ('The valency of oxygen is 6.', 'Oxygen has 6 electrons in its outermost shell.', 'd', 'A false: valency 2 (needs 2 to complete octet); R true.'),
    ('Argon does not form compounds easily.', 'Argon has 8 electrons in its outermost shell.', 'a', 'R explains A.'),
]

c7s4_defs = [
    ('the atomic number', 'the number of protons in the nucleus of an atom'),
    ('the mass number', 'the sum of the numbers of protons and neutrons in the nucleus of an atom'),
    ('isotopes', 'atoms of the same element with the same atomic number but different mass numbers'),
    ('isobars', 'atoms of different elements with the same mass number but different atomic numbers'),
    ('nucleons', 'the protons and neutrons present in the nucleus'),
]


def c7s4_n(r):
    n, s, z, a = r.choice(ELEM)
    return {'stem': f'An atom of {n} has atomic number {z} and mass number {a}. Find the number of protons, electrons and neutrons.', 'answer': f'p = {z}, e = {z}, n = {a - z}',
            'key': f'Protons = electrons = Z = {z}; neutrons = A − Z = {a} − {z} = {a - z}.', 'distractors': [f'p = {z}, e = {z}, n = {a}', f'p = {a - z}, e = {z}, n = {z}', f'p = {a}, e = {a}, n = {a - z}']}


ISO = [('chlorine', 35, 75, 37, 25), ('copper', 63, 69, 65, 31), ('boron', 10, 20, 11, 80), ('lithium', 6, 7.5, 7, 92.5), ('bromine', 79, 50, 81, 50)]


def c7s4_avg(r):
    n, a1, p1, a2, p2 = r.choice(ISO)
    m = (a1 * p1 + a2 * p2) / 100
    return {'stem': f'Natural {n} contains two isotopes: {a1}{n[:2].capitalize()} ({num(p1)}%) and {a2}{n[:2].capitalize()} ({num(p2)}%). Find the average atomic mass of {n}.'.replace(f'{a1}{n[:2].capitalize()}', f'{n}-{a1}').replace(f'{a2}{n[:2].capitalize()}', f'{n}-{a2}'),
            'answer': f'{sig(m, 4)} u', 'key': f'Average = ({a1} × {num(p1)} + {a2} × {num(p2)}) ÷ 100 = {sig(m, 4)} u.', 'distractors': [f'{num((a1 + a2) / 2, 1)} u', f'{sig((a1 * p2 + a2 * p1) / 100, 4)} u', f'{a1 + a2} u']}


def c7s4_pair(r):
    pairs = [('¹²C and ¹⁴C', 'isotopes'), ('³⁵Cl and ³⁷Cl', 'isotopes'), ('¹H and ²H', 'isotopes'), ('⁴⁰Ca and ⁴⁰Ar', 'isobars'), ('¹⁴C and ¹⁴N', 'isobars'), ('²³⁵U and ²³⁸U', 'isotopes')]
    p, t = r.choice(pairs)
    return mcq(f'The pair {p} are:', t, [x for x in ['isotopes', 'isobars', 'the same atom', 'ions of the same element'] if x != t][:3],
               f'{p}: {"same atomic number, different mass numbers" if t == "isotopes" else "same mass number, different atomic numbers"}.', r)


c7s4_uses = [('cobalt-60', 'treating cancer'), ('iodine-131', 'treating goitre'), ('uranium-235', 'fuel in nuclear reactors')]
c7s4_mc = [
    ('Isotopes of an element have the same:', 'chemical properties', 'mass number', 'number of neutrons', 'physical properties'),
    ('Which isotope is used to treat goitre?', 'Iodine-131', 'Cobalt-60', 'Uranium-235', 'Carbon-12'),
    ('An isotope of cobalt is used in the treatment of:', 'cancer', 'goitre', 'anaemia', 'diabetes'),
    ('The isotope used as fuel in nuclear reactors is:', 'uranium-235', 'carbon-14', 'iodine-131', 'hydrogen-1'),
]
c7s4_why = [
    ('Why do isotopes of an element have the same chemical properties but different physical properties?', 'Same number of electrons (same configuration) gives the same chemistry; different numbers of neutrons give different masses and hence different physical properties.', '1 mark: same electrons. 1 mark: different mass.'),
    ('Why is the atomic mass of chlorine taken as 35.5 u and not a whole number?', 'Chlorine is a mixture of isotopes Cl-35 and Cl-37 in a 3 : 1 ratio; the average mass is 35.5 u.', '1 mark: isotopes. 1 mark: average.'),
]
c7s4_ar = [
    ('¹²C and ¹⁴C have the same chemical properties.', 'They have the same number of electrons.', 'a', 'R explains A.'),
    ('Isobars have the same atomic number.', 'Isobars have the same mass number.', 'd', 'A false; R true.'),
]
c7_hots = [
    ('An atom X has 2 electrons in its K shell, 8 in L and 6 in M. Predict (i) its atomic number, (ii) its valency, (iii) whether it is a metal or a non-metal, and (iv) the formula of its compound with hydrogen.', '(i) 16 (sulphur). (ii) 2. (iii) Non-metal. (iv) H₂X (H₂S).', '1 mark each (max 3 for multi-step: award 3 for all four).'),
    ('If the α-scattering experiment were done with a foil of a metal whose atoms are much lighter, such as aluminium, how might the results change? Explain.', 'Fewer α-particles would be deflected through large angles, because the aluminium nucleus has much less positive charge and mass than gold, so it repels α-particles less strongly.', '1 mark: fewer large deflections. 1 mark: smaller nuclear charge. 1 mark: reasoning.'),
    ('Element Y has two isotopes with mass numbers 20 and 22. Its average atomic mass is 20.2 u. Find the percentage of each isotope.', 'Let x% be Y-20: 20x + 22(100 − x) = 2020 ⇒ −2x = −180 ⇒ x = 90. So 90% Y-20 and 10% Y-22.', '1 mark equation. 1 mark solving. 1 mark answer.'),
]


def c7_case(r):
    n, s, z, a = r.choice(ELEM[2:])
    c = config(z)
    v = valency(z)
    return {'stem': (f'Read: An element has {z} protons and {a - z} neutrons in its nucleus.\n'
                     f'(i) What are its atomic number and mass number? (ii) Write its electronic configuration. (iii) What is its valency? (iv) Name the element and write the symbol with A and Z.'),
            'answer': f'(i) Z = {z}, A = {a}. (ii) {", ".join(map(str, c))}. (iii) {v}. (iv) {cap(n)}: {s} with A = {a}, Z = {z}.',
            'key': '1 mark each part.'}


c7_long = [
    ('Describe Rutherford\'s α-particle scattering experiment, its three observations and the conclusions drawn. State the features of his model and its main drawback.',
     'Fast α-particles were directed at thin gold foil. Most passed straight (atom mostly empty); some deflected by small angles (positive charge in small space); very few bounced back (positive charge and mass in a tiny nucleus). Model: positive nucleus with nearly all mass; electrons revolve around it; nucleus very small. Drawback: revolving charged electrons should radiate energy and fall into the nucleus, so the atom would be unstable.',
     '1 mark experiment; 2 marks observations/conclusions; 1 mark model; 1 mark drawback.'),
    ('What are isotopes and isobars? Give two examples of each. Write the electronic configuration and valency of carbon (Z = 6), sodium (Z = 11) and chlorine (Z = 17).',
     'Isotopes: same Z, different A (¹H, ²H; ³⁵Cl, ³⁷Cl). Isobars: same A, different Z (⁴⁰Ca, ⁴⁰Ar; ¹⁴C, ¹⁴N). C: 2, 4, valency 4; Na: 2, 8, 1, valency 1; Cl: 2, 8, 7, valency 1.',
     '2 marks isotopes/isobars; 3 marks configurations and valencies.'),
]

# ======================= ch08 Atomic Foundations of Matter
c8s1_defs = [
    ('the law of conservation of mass', 'the law that mass can neither be created nor destroyed in a chemical reaction'),
    ('the law of constant proportions', 'the law that in a chemical substance the elements are always present in definite proportions by mass'),
    ('Dalton\'s atomic theory', 'the theory that all matter is made of indivisible atoms, which combine in small whole-number ratios to form compounds'),
]


def c8s1_cons(r):
    a, b, c = r.choice([('5.3 g of sodium carbonate', '6.0 g of ethanoic acid', '2.2 g of carbon dioxide'), ('3.0 g of carbon', '8.0 g of oxygen', None), ('4.8 g of magnesium', '3.2 g of oxygen', None),
                        ('2.8 g of iron', '1.6 g of sulphur', None)])
    import re
    ma = float(re.match(r'[\d.]+', a).group())
    mb = float(re.match(r'[\d.]+', b).group())
    if c:
        mc = float(re.match(r'[\d.]+', c).group())
        rest = ma + mb - mc
        return {'stem': f'In a reaction, {a} reacted with {b}. The products were {c}, water and sodium ethanoate, with a combined mass of the water and sodium ethanoate of {num(rest, 1)} g. Show that these observations agree with the law of conservation of mass.',
                'answer': f'Total reactants = {num(ma + mb, 1)} g = total products {num(mc, 1)} + {num(rest, 1)} = {num(ma + mb, 1)} g.', 'key': '1 mark each total; 1 mark statement of law.'}
    return {'stem': f'{cap(a)} burns completely in {b} with nothing left over. What mass of product is formed, and which law did you use?', 'answer': f'{num(ma + mb, 1)} g; law of conservation of mass',
            'key': f'Mass of product = {num(ma, 1)} + {num(mb, 1)} = {num(ma + mb, 1)} g (conservation of mass).', 'distractors': [f'{num(abs(ma - mb), 1)} g; law of conservation of mass', f'{num(ma + mb, 1)} g; law of constant proportions', f'{num(ma * mb, 2)} g; law of conservation of mass']}


def c8s1_prop(r):
    h = r.choice([2, 3, 4, 5, 6, 10])
    return {'stem': f'Hydrogen and oxygen combine in the ratio 1 : 8 by mass to form water. What mass of oxygen will combine completely with {h} g of hydrogen, and what mass of water forms?', 'answer': f'{8 * h} g oxygen; {9 * h} g water',
            'key': f'Oxygen = 8 × {h} = {8 * h} g; water = {h} + {8 * h} = {9 * h} g (law of constant proportions).', 'distractors': [f'{h / 8:g} g oxygen; {h + h / 8:g} g water', f'{8 * h} g oxygen; {8 * h} g water', f'{16 * h} g oxygen; {17 * h} g water']}


def c8s1_cp(r):
    m = r.choice([12, 24, 36, 48, 60])
    o = m * 8 / 3
    return {'stem': f'Carbon and oxygen combine in the ratio 3 : 8 by mass to form carbon dioxide. What mass of oxygen is needed to burn {m} g of carbon completely?', 'answer': f'{num(o)} g',
            'key': f'Oxygen = {m} × 8/3 = {num(o)} g.', 'distractors': [f'{num(m * 3 / 8, 2)} g', f'{num(m + 8)} g', f'{num(m * 8)} g']}


c8s1_mc = [
    ('The law of conservation of mass was stated by:', 'Antoine Lavoisier', 'Joseph Proust', 'John Dalton', 'J. J. Thomson'),
    ('The law of constant proportions was stated by:', 'Joseph Proust', 'Antoine Lavoisier', 'Ernest Rutherford', 'Amedeo Avogadro'),
    ('Which postulate of Dalton\'s theory explains the law of conservation of mass?', 'Atoms can neither be created nor destroyed in a chemical reaction', 'Atoms of an element are identical', 'Atoms combine in whole-number ratios', 'Atoms of different elements have different masses'),
    ('Which postulate of Dalton\'s theory is NOT accepted today?', 'Atoms are indivisible', 'Atoms combine in fixed ratios', 'Matter is made of atoms', 'Atoms take part in reactions'),
]
c8s1_why = [
    ('Why does a burning candle seem to lose mass, though mass is conserved?', 'The products, carbon dioxide and water vapour, escape into the air; if they were collected, total mass would equal the mass of wax and oxygen used.', '1 mark: gaseous products escape. 1 mark: total conserved.'),
    ('How does the law of constant proportions support the existence of atoms?', 'If compounds are made of atoms combining in fixed whole-number ratios with fixed masses, the mass ratio must always be the same.', '1 mark: fixed ratio of atoms. 1 mark: fixed masses.'),
]
c8s1_ar = [
    ('Water from a river and water from a well both have hydrogen and oxygen in the ratio 1 : 8 by mass.', 'A compound always contains the same elements in a fixed proportion by mass.', 'a', 'R explains A.'),
    ('Mass is lost when magnesium ribbon burns in air.', 'Mass is conserved in chemical reactions.', 'd', 'A false: mass increases as oxygen combines; R true.'),
]

c8s2_defs = [
    ('an atom', 'the smallest particle of an element that can take part in a chemical reaction'),
    ('a molecule', 'the smallest particle of an element or compound that can exist independently and shows its properties'),
    ('the atomicity', 'the number of atoms constituting a molecule'),
    ('the atomic mass unit (u)', 'one-twelfth of the mass of an atom of carbon-12'),
]
c8s2_atom = {
    'a monoatomic molecule': ['helium (He)', 'neon (Ne)', 'argon (Ar)'],
    'a diatomic molecule': ['oxygen (O₂)', 'hydrogen (H₂)', 'nitrogen (N₂)', 'chlorine (Cl₂)'],
    'a polyatomic molecule': ['ozone (O₃)', 'phosphorus (P₄)', 'sulphur (S₈)'],
}
c8s2_mc = [
    ('The symbol of sodium, Na, comes from its Latin name:', 'natrium', 'sodanum', 'nadium', 'neptunium'),
    ('The symbol Fe for iron comes from:', 'ferrum', 'ferrous', 'ferrite', 'felix'),
    ('IUPAC stands for:', 'International Union of Pure and Applied Chemistry', 'Indian Union of Physics and Chemistry', 'International Unit of Pure Atomic Chemistry', 'Institute of Universal Pure and Applied Chemistry'),
    ('Atomic masses today are measured relative to:', 'carbon-12', 'hydrogen-1', 'oxygen-16', 'nitrogen-14'),
    ('Which of these is the correct way of writing the symbol of cobalt?', 'Co', 'CO', 'co', 'cO'),
]
c8s2_why = [
    ('Why is "CO" not the symbol of cobalt?', 'Symbols use one capital letter followed by a small letter: Co is cobalt; CO is the formula of carbon monoxide (carbon + oxygen).', '1 mark: capital/small rule. 1 mark: CO is a compound.'),
    ('Why are atomic masses expressed in u rather than in grams?', 'Atoms are extremely light (about 10⁻²⁴ g), so a relative unit based on carbon-12 is more convenient.', '1 mark: very small. 1 mark: relative unit.'),
]
c8s2_ar = [
    ('The atomicity of ozone is 3.', 'A molecule of ozone contains three oxygen atoms.', 'a', 'R explains A.'),
    ('Atoms of most elements exist freely.', 'Atoms of most elements are not stable on their own and form molecules or ions.', 'd', 'A false; R true.'),
]

CATIONS = [('sodium', 'Na', 1), ('potassium', 'K', 1), ('silver', 'Ag', 1), ('ammonium', 'NH4', 1), ('magnesium', 'Mg', 2), ('calcium', 'Ca', 2), ('zinc', 'Zn', 2), ('copper(II)', 'Cu', 2),
           ('iron(II)', 'Fe', 2), ('aluminium', 'Al', 3), ('iron(III)', 'Fe', 3)]
ANIONS = [('chloride', 'Cl', 1), ('bromide', 'Br', 1), ('hydroxide', 'OH', 1), ('nitrate', 'NO3', 1), ('hydrogencarbonate', 'HCO3', 1), ('oxide', 'O', 2), ('sulphide', 'S', 2),
          ('sulphate', 'SO4', 2), ('carbonate', 'CO3', 2), ('phosphate', 'PO4', 3), ('nitride', 'N', 3)]
POLY = {'NH4', 'OH', 'NO3', 'HCO3', 'SO4', 'CO3', 'PO4'}


def formula(c, a):
    from math import gcd
    cs, cv = c[1], c[2]
    as_, av = a[1], a[2]
    g = gcd(cv, av)
    nc, na = av // g, cv // g

    def part(sym, n):
        if n == 1:
            return sub(sym)
        return (f'({sub(sym)})' if sym in POLY else sub(sym)) + sub(str(n))
    return part(cs, nc) + part(as_, na)


def c8s3_formula(r):
    while True:
        c, a = r.choice(CATIONS), r.choice(ANIONS)
        if not (c[1] == 'NH4' and a[1] in ('O', 'S', 'N')) and not (c[1] == 'Ag' and a[1] == 'N'):
            break
    ans = formula(c, a)
    wrong = {formula((c[0], c[1], a[2]), (a[0], a[1], c[2])), sub(c[1]) + sub(a[1]), formula((c[0], c[1], c[2] + 1), a)}
    wrong.discard(ans)
    extra = [sub(c[1]) + sub(str(a[2])) + sub(a[1]) + sub(str(c[2])), sub(c[1] + a[1]) + sub('2')]
    for e in extra:
        if len(wrong) >= 3:
            break
        if e != ans:
            wrong.add(e)
    nm = f'{c[0].replace("(II)", " (II)").replace("(III)", " (III)")} {a[0]}'
    return mcq(f'The chemical formula of {nm} is:', ans, list(wrong)[:3],
               f'{c[0]} valency {c[2]}, {a[0]} valency {a[2]}; criss-cross and simplify: {ans}.', r)


def c8s3_write(r):
    c, a = r.choice(CATIONS), r.choice(ANIONS)
    if c[1] == 'NH4' and a[1] in ('O', 'S', 'N'):
        raise ValueError
    ans = formula(c, a)
    return {'stem': f'Write the chemical formula of {c[0]} {a[0]}, showing the valencies and the criss-cross method.', 'answer': ans,
            'key': f'Symbols {c[1]} and {a[1]}; valencies {c[2]} and {a[2]}; criss-cross gives {ans} (1 mark symbols/valencies, 1 mark formula).'}


c8s3_defs = [
    ('valency', 'the combining capacity of an element'),
    ('an ion', 'a charged particle formed when an atom or group of atoms loses or gains electrons'),
    ('a cation', 'a positively charged ion'),
    ('an anion', 'a negatively charged ion'),
    ('a polyatomic ion', 'a group of atoms carrying a charge, such as sulphate or ammonium'),
]
c8s3_mc = [
    ('The formula of a compound shows:', 'the elements present and the number of atoms of each', 'only the colour of the compound', 'only the mass of the compound', 'the state of the compound'),
    ('Which of these is a polyatomic ion?', 'Ammonium (NH₄⁺)', 'Sodium (Na⁺)', 'Chloride (Cl⁻)', 'Oxide (O²⁻)'),
    ('Ions in sodium chloride are held together by:', 'electrostatic attraction between Na⁺ and Cl⁻', 'sharing of electrons', 'magnetic force', 'gravity'),
]
c8s3_why = [
    ('Why is the formula of aluminium oxide Al₂O₃?', 'Aluminium has valency 3 and oxygen 2; to balance charges 2 Al³⁺ (+6) combine with 3 O²⁻ (−6).', '1 mark: valencies. 1 mark: charge balance.'),
    ('Why are brackets used in Ca(OH)₂ but not in CaCl₂?', 'OH is a polyatomic ion; brackets show that the whole group is taken twice. Cl is a single atom, so no brackets are needed.', '1 mark: polyatomic group. 1 mark: single atom.'),
]
c8s3_ar = [
    ('The formula of magnesium chloride is MgCl₂.', 'Magnesium has valency 2 and chlorine has valency 1.', 'a', 'R explains A.'),
    ('The formula of calcium oxide is Ca₂O₂.', 'Formulae are written in the simplest ratio.', 'd', 'A false: it is CaO; R true.'),
]

MASS = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'Na': 23, 'Mg': 24, 'Al': 27, 'S': 32, 'Cl': 35.5, 'K': 39, 'Ca': 40, 'Fe': 56, 'Zn': 65, 'Cu': 63.5, 'P': 31}
MOLS = [('water', 'H₂O', {'H': 2, 'O': 1}), ('carbon dioxide', 'CO₂', {'C': 1, 'O': 2}), ('ammonia', 'NH₃', {'N': 1, 'H': 3}), ('methane', 'CH₄', {'C': 1, 'H': 4}),
        ('glucose', 'C₆H₁₂O₆', {'C': 6, 'H': 12, 'O': 6}), ('sulphuric acid', 'H₂SO₄', {'H': 2, 'S': 1, 'O': 4}), ('nitric acid', 'HNO₃', {'H': 1, 'N': 1, 'O': 3}),
        ('ethanol', 'C₂H₅OH', {'C': 2, 'H': 6, 'O': 1}), ('sodium chloride', 'NaCl', {'Na': 1, 'Cl': 1}), ('calcium carbonate', 'CaCO₃', {'Ca': 1, 'C': 1, 'O': 3}),
        ('sodium hydroxide', 'NaOH', {'Na': 1, 'O': 1, 'H': 1}), ('potassium carbonate', 'K₂CO₃', {'K': 2, 'C': 1, 'O': 3}), ('magnesium oxide', 'MgO', {'Mg': 1, 'O': 1}),
        ('oxygen', 'O₂', {'O': 2}), ('nitrogen', 'N₂', {'N': 2}), ('chlorine', 'Cl₂', {'Cl': 2})]


def mm(d):
    return sum(MASS[k] * v for k, v in d.items())


def c8s4_mm(r):
    n, f, d = r.choice(MOLS)
    M = mm(d)
    calc = ' + '.join(f'{v} × {num(MASS[k], 1)}' if v > 1 else f'{num(MASS[k], 1)}' for k, v in d.items())
    word = 'formula unit mass' if n in ('sodium chloride', 'calcium carbonate', 'sodium hydroxide', 'potassium carbonate', 'magnesium oxide') else 'molecular mass'
    return {'stem': f'Calculate the {word} of {n} ({f}). (H = 1, C = 12, N = 14, O = 16, Na = 23, Mg = 24, S = 32, Cl = 35.5, K = 39, Ca = 40 u)', 'answer': f'{num(M, 1)} u',
            'key': f'{calc} = {num(M, 1)} u.', 'distractors': [f'{num(M + 16, 1)} u', f'{num(sum(MASS[k] for k in d), 1)} u', f'{num(M - 1, 1)} u']}


def c8s4_mol(r):
    n, f, d = r.choice(MOLS)
    M = mm(d)
    k = r.choice([0.25, 0.5, 2, 3, 5, 0.1])
    m = M * k
    return {'stem': f'How many moles are present in {num(m, 2)} g of {n} ({f})?', 'answer': f'{num(k, 2)} mol', 'key': f'Molar mass = {num(M, 1)} g/mol; n = m/M = {num(m, 2)}/{num(M, 1)} = {num(k, 2)} mol.',
            'distractors': [f'{sig(m * M, 3)} mol', f'{num(k * 2, 2)} mol', f'{sig(M / m, 3)} mol']}


def c8s4_part(r):
    n, f, d = r.choice(MOLS)
    M = mm(d)
    k = r.choice([0.5, 1, 2, 0.25, 0.1, 3])
    m = M * k
    N = k * 6.022
    return {'stem': f'Find the number of molecules in {num(m, 2)} g of {n} ({f}). (Nₐ = 6.022 × 10²³ per mole)', 'answer': f'{sig(N, 4)} × 10²³',
            'key': f'n = {num(m, 2)}/{num(M, 1)} = {num(k, 2)} mol; N = n × Nₐ = {num(k, 2)} × 6.022 × 10²³ = {sig(N, 4)} × 10²³.', 'distractors': [f'{sig(6.022 / k, 4)} × 10²³', f'{sig(N, 4)} × 10²²', f'{sig(m * 6.022, 4)} × 10²³']}


def c8s4_mass(r):
    el = r.choice([('sodium', 23), ('carbon', 12), ('oxygen atoms', 16), ('magnesium', 24), ('calcium', 40), ('iron', 56), ('nitrogen atoms', 14)])
    k = r.choice([0.5, 2, 3, 0.2, 5, 1.5])
    return {'stem': f'What is the mass of {num(k)} mole of {el[0]}? (atomic mass {el[1]} u)', 'answer': f'{num(k * el[1], 2)} g', 'key': f'm = n × M = {num(k)} × {el[1]} = {num(k * el[1], 2)} g.',
            'distractors': [f'{num(el[1] / k, 2)} g', f'{num(k * el[1] * 6.022, 2)} g', f'{num(k + el[1], 2)} g']}


c8s4_defs = [
    ('a mole', 'the amount of substance containing 6.022 × 10²³ particles (atoms, molecules or ions)'),
    ('Avogadro\'s number', 'the number of particles in one mole of a substance, 6.022 × 10²³'),
    ('molar mass', 'the mass of one mole of a substance in grams, numerically equal to its atomic or molecular mass'),
    ('molecular mass', 'the sum of the atomic masses of all the atoms in a molecule'),
    ('formula unit mass', 'the sum of the atomic masses of all atoms in a formula unit of an ionic compound'),
]
c8s4_mc = [
    ('The mass of 1 mole of oxygen molecules (O₂) is:', '32 g', '16 g', '6.022 × 10²³ g', '8 g'),
    ('One mole of any substance contains:', '6.022 × 10²³ particles', '1 particle', '12 particles', '22.4 particles'),
    ('Which has more atoms: 12 g of carbon or 24 g of magnesium?', 'Both have the same number (1 mole each)', '12 g of carbon', '24 g of magnesium', 'Cannot be compared'),
    ('The term "formula unit" is used for:', 'ionic compounds such as NaCl', 'molecules such as H₂O', 'elements only', 'gases only'),
]
c8s4_why = [
    ('Why do chemists use the mole instead of counting atoms?', 'Atoms are far too small and numerous to count; a mole links a measurable mass in grams to a known number of particles.', '1 mark: too many/small. 1 mark: link mass to number.'),
    ('Why does 18 g of water and 2 g of hydrogen gas contain the same number of molecules?', 'Each is 1 mole (18 g/mol for H₂O, 2 g/mol for H₂), and one mole of any substance has 6.022 × 10²³ molecules.', '1 mark: both 1 mol. 1 mark: Avogadro number.'),
]
c8s4_ar = [
    ('One mole of water weighs 18 g.', 'The molecular mass of water is 18 u.', 'a', 'R explains A.'),
    ('1 g of hydrogen gas and 1 g of oxygen gas contain the same number of molecules.', 'Equal masses of different substances contain equal moles.', 'e', ''),
]
c8s4_ar[1] = ('16 g of oxygen gas contains 0.5 mole of O₂ molecules.', 'The molar mass of O₂ is 32 g/mol.', 'a', 'R explains A.')
c8_hots = [
    ('Which contains more atoms: 1 g of sodium or 1 g of magnesium? Show by calculation. (Na = 23, Mg = 24)', 'Na: 1/23 mol = 0.0435 mol; Mg: 1/24 = 0.0417 mol. Sodium has more atoms because its atomic mass is smaller.', '1 mark each calculation. 1 mark conclusion.'),
    ('A student says the formula of sodium sulphate is NaSO₄. Correct it, explain the error and find its formula unit mass. (Na = 23, S = 32, O = 16)', 'Na valency 1, SO₄ valency 2: formula Na₂SO₄. The charges were not balanced. Mass = 2 × 23 + 32 + 4 × 16 = 142 u.', '1 mark formula. 1 mark reason. 1 mark mass.'),
    ('Calcium carbonate decomposes: CaCO₃ → CaO + CO₂. What mass of CaO is formed from 50 g of CaCO₃? (Ca = 40, C = 12, O = 16)', 'M(CaCO₃) = 100 g/mol, so 50 g = 0.5 mol; gives 0.5 mol CaO = 0.5 × 56 = 28 g.', '1 mark moles. 1 mark ratio. 1 mark mass.'),
]


def c8_case(r):
    n, f, d = r.choice([m for m in MOLS if len(m[2]) >= 2])
    M = mm(d)
    k = r.choice([0.5, 2, 0.25])
    return {'stem': (f'Read: A lab bottle contains {num(M * k, 2)} g of {n}, formula {f}.\n'
                     f'(i) Name the elements present. (ii) Find its molar mass. (iii) How many moles are in the bottle? (iv) How many molecules or formula units are present? (Nₐ = 6.022 × 10²³; H 1, C 12, N 14, O 16, Na 23, Mg 24, S 32, Cl 35.5, K 39, Ca 40)'),
            'answer': f'(i) {", ".join(d)}. (ii) {num(M, 1)} g/mol. (iii) {num(k, 2)} mol. (iv) {sig(k * 6.022, 4)} × 10²³.', 'key': '1 mark each part.'}


c8_long = [
    ('State the law of conservation of mass and the law of constant proportions. Write the postulates of Dalton\'s atomic theory and show which postulate explains each law.',
     'Conservation: mass is neither created nor destroyed in a reaction. Constant proportions: a compound always has elements in a fixed ratio by mass. Dalton: matter of atoms; atoms indivisible and indestructible (explains conservation); atoms of an element identical in mass and properties; atoms of different elements differ; atoms combine in small whole-number ratios (explains constant proportions); relative number and kinds of atoms are constant in a compound.',
     '2 marks laws; 2 marks postulates; 1 mark linking.'),
    ('Define mole and Avogadro\'s number. Calculate (a) the number of moles in 52 g of helium (He = 4), (b) the mass of 0.5 mol of water, (c) the number of molecules in 8 g of oxygen gas.',
     'Mole: amount with 6.022 × 10²³ particles; Avogadro number 6.022 × 10²³. (a) 52/4 = 13 mol. (b) 0.5 × 18 = 9 g. (c) 8/32 = 0.25 mol × 6.022 × 10²³ = 1.5055 × 10²³ molecules.',
     '2 marks definitions; 1 mark each calculation.'),
]

FAMILIES = {
    S + '05-st1': [TERM(c5s1_defs), DEF(c5s1_defs), MC(c5s1_mc, C='C2', D='D2'), SA(c5s1_why), ARF(c5s1_ar), G('C3', 'D2', 'explain', c5s1_net),
                   SA(c5_hots[2:3], C='C4', D='D4', type='multi_step'), SA([('Explain why a person standing in a moving train falls when the train turns sharply.', 'The body tends to continue moving in a straight line due to inertia while the train turns, so the person is thrown outward.', '1 mark: inertia of direction. 1 mark: thrown outward.')], C='C3', D='D3')],
    S + '05-st2': [TERM(c5s2_defs), DEF(c5s2_defs), MC(c5s2_mc, C='C2', D='D2'), SA(c5s2_why), ARF(c5s2_ar), G('C3', 'D1', 'numerical', c5s2_p), G('C3', 'D2', 'numerical', c5s2_fma),
                   G('C3', 'D3', 'numerical', c5s2_stop), G('C3', 'D4', 'multi_step', c5s2_change), G('C4', 'D4', 'multi_step', c5s2_change), G('C4', 'D3', 'case', c5_case, gap='G7'),
                   SA(c5_hots[:1], C='C4', D='D5', type='multi_step'), LONG(c5_long[:1], C='C4', D='D4'), G('C2', 'D2', 'mcq', c5s2_fma), G('C1', 'D2', 'mcq', c5s2_p)],
    S + '05-st3': [TERM(c5s3_defs), DEF(c5s3_defs), MC(c5s3_mc, C='C1', D='D2'), SA(c5s3_why), ARF(c5s3_ar), G('C3', 'D2', 'numerical', c5s3_recoil), G('C3', 'D3', 'numerical', c5s3_stick),
                   G('C3', 'D4', 'multi_step', c5s3_coll), SA(c5_hots[1:2] + c5_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c5_long[1:], C='C4', D='D4'), G('C2', 'D2', 'mcq', c5s3_recoil)],
    S + '05-st4': [TERM(c5s4_defs + c5s1_defs[:2]), DEF(c5s4_defs), MC(c5s4_mc, C='C1', D='D2'), SA(c5s4_why), ARF(c5s4_ar), G('C3', 'D3', 'numerical', c5s4_fr),
                   G('C4', 'D4', 'multi_step', c5s4_fr), G('C2', 'D2', 'mcq', c5s4_fr)],
    S + '06-st1': [TERM(c6s1_defs + c6s2_defs[:2]), DEF(c6s1_defs), CLS(c6s1_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c6s1_mc, C='C1', D='D2'), SA(c6s1_why), ARF(c6s1_ar),
                   G('C3', 'D1', 'numerical', c6s1_w), G('C3', 'D2', 'numerical', c6s1_lift), SORT(c6s1_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(2, 2)),
                   G('C4', 'D3', 'multi_step', c6s1_lift)],
    S + '06-st2': [TERM(c6s2_defs), DEF(c6s2_defs), CLS(c6s2_cats, 'Which of the following is {}?', C='C1', D='D2'), MC(c6s2_mc, C='C2', D='D2'), SA(c6s2_why), ARF(c6s2_ar),
                   G('C3', 'D1', 'numerical', c6s2_ke), G('C3', 'D2', 'numerical', c6s2_pe), G('C3', 'D3', 'mcq', c6s2_double), G('C3', 'D4', 'multi_step', c6s2_fall),
                   G('C4', 'D4', 'multi_step', c6s2_fall), SA(c6_hots[1:], C='C4', D='D4', type='multi_step'), LONG(c6_long[:1], C='C4', D='D4'), G('C2', 'D3', 'mcq', c6s2_ke)],
    S + '06-st3': [TERM(c6s3_defs), DEF(c6s3_defs), MC(c6s3_mc, C='C1', D='D2'), SA(c6s3_why), ARF(c6s3_ar), G('C3', 'D2', 'numerical', c6s3_p), G('C3', 'D1', 'numerical', c6s3_kwh),
                   G('C3', 'D4', 'multi_step', c6s3_bill), G('C4', 'D4', 'multi_step', c6s3_bill), G('C4', 'D3', 'case', c6_case, gap='G7'), SA(c6_hots[:1], C='C4', D='D5', type='multi_step'),
                   LONG(c6_long[1:], C='C4', D='D4'), G('C2', 'D2', 'mcq', c6s3_p)],
    S + '06-st4': [TERM(c6s4_defs), DEF(c6s4_defs), CLS(c6s4_lev, 'Which of the following is an example of {}?', C='C2', D='D2'), MC(c6s4_mc, C='C1', D='D2'), SA(c6s4_why), ARF(c6s4_ar),
                   G('C3', 'D2', 'numerical', c6s4_ma), G('C3', 'D3', 'numerical', c6s4_lever), G('C3', 'D4', 'multi_step', c6s4_eff), G('C4', 'D4', 'multi_step', c6s4_incline),
                   SORT(c6s4_lev, 'Classify these levers as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2))],
    S + '07-st1': [TERM(c7s1_defs), DEF(c7s1_defs), G('C1', 'D2', 'mcq', c7s1_who), MC(c7s1_mc, C='C2', D='D2'), SA(c7s1_why), ARF(c7s1_ar), G('C3', 'D2', 'numerical', c7s4_n),
                   SA([('An atom has 17 protons and 18 neutrons. A second particle has 17 protons, 18 neutrons and 18 electrons. Identify both and explain the difference.', 'First: a chlorine atom (17 electrons, neutral). Second: a chloride ion Cl⁻, which has gained one electron and carries −1 charge.', '1 mark each identification. 1 mark explanation.'),
                       ('If the mass of a proton is taken as 1 u, estimate the mass of an atom with 11 protons, 12 neutrons and 11 electrons, and explain why the electrons are ignored.', 'About 23 u (11 + 12); electrons are about 1/2000 u each, so 11 electrons add only about 0.006 u.', '1 mark: 23 u. 1 mark: electron mass negligible.')], C='C4', D='D4', type='multi_step')],
    S + '07-st2': [TERM(c7s2_defs), DEF(c7s2_defs), G('C2', 'D2', 'mcq', c7s2_concl), MC(c7s2_mc, C='C1', D='D2'), SA(c7s2_why), ARF(c7s2_ar),
                   SA(c7_hots[1:2], C='C4', D='D4', type='multi_step'), LONG(c7_long[:1], C='C4', D='D3'),
                   SA([('Compare Thomson\'s and Rutherford\'s models in terms of where the positive charge and mass are located.', 'Thomson: positive charge and mass spread uniformly through the atom with electrons embedded. Rutherford: positive charge and almost all mass concentrated in a tiny nucleus; electrons revolve around it.', '1 mark each model.'),
                       ('Draw (describe) Bohr\'s model of a sodium atom.', 'A nucleus with 11 protons and 12 neutrons; K shell 2 electrons, L shell 8, M shell 1, in fixed circular orbits.', '1 mark nucleus. 1 mark shells.')], C='C3', D='D3')],
    S + '07-st3': [MC(c7s3_mc, C='C1', D='D2'), G('C1', 'D1', 'mcq', c7s3_conf), G('C3', 'D2', 'numerical', c7s3_val), G('C3', 'D3', 'explain', c7s3_ident), SA(c7s3_why), ARF(c7s3_ar),
                   G('C4', 'D3', 'case', c7_case, gap='G7'), SA(c7_hots[:1], C='C4', D='D4', type='multi_step'), G('C2', 'D2', 'mcq', c7s3_val), G('C4', 'D4', 'multi_step', c7s3_ident)],
    S + '07-st4': [TERM(c7s4_defs), DEF(c7s4_defs), G('C2', 'D2', 'mcq', c7s4_pair), MC(c7s4_mc, C='C1', D='D2'), SA(c7s4_why), ARF(c7s4_ar), G('C3', 'D1', 'numerical', c7s4_n),
                   G('C3', 'D3', 'numerical', c7s4_avg), SA(c7_hots[2:], C='C4', D='D5', type='multi_step'), LONG(c7_long[1:], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c7s4_avg)],
    S + '08-st1': [TERM(c8s1_defs), DEF(c8s1_defs), MC(c8s1_mc, C='C1', D='D2'), SA(c8s1_why), ARF(c8s1_ar), G('C3', 'D2', 'numerical', c8s1_prop), G('C3', 'D3', 'numerical', c8s1_cp),
                   G('C3', 'D4', 'multi_step', c8s1_cons), G('C4', 'D3', 'numerical', c8s1_cons), LONG(c8_long[:1], C='C4', D='D4'), G('C2', 'D2', 'mcq', c8s1_prop)],
    S + '08-st2': [TERM(c8s2_defs), DEF(c8s2_defs), CLS(c8s2_atom, 'Which of the following is {}?', C='C2', D='D2'), MC(c8s2_mc, C='C1', D='D2'), SA(c8s2_why), ARF(c8s2_ar),
                   SORT(c8s2_atom, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2', n=(1, 2)),
                   SA([('An atom of element X is 2 times heavier than an atom of carbon-12. What is its atomic mass, and what could X be?', '24 u; magnesium.', '1 mark: 24 u. 1 mark: Mg.'),
                       ('Why is 1/12 of the mass of a carbon-12 atom chosen as the atomic mass unit?', 'Carbon-12 is a common, stable isotope; using it as a standard lets the relative masses of most elements come close to whole numbers.', '1 mark: standard. 1 mark: near whole numbers.')], C='C4', D='D3', type='explain')],
    S + '08-st3': [TERM(c8s3_defs), DEF(c8s3_defs), G('C1', 'D2', 'mcq', c8s3_formula), MC(c8s3_mc, C='C2', D='D2'), SA(c8s3_why), ARF(c8s3_ar), G('C3', 'D2', 'explain', c8s3_write),
                   G('C3', 'D3', 'mcq', c8s3_formula), SA(c8_hots[1:2], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'explain', c8s3_write)],
    S + '08-st4': [TERM(c8s4_defs), DEF(c8s4_defs), MC(c8s4_mc, C='C1', D='D2'), SA(c8s4_why), ARF(c8s4_ar), G('C3', 'D1', 'numerical', c8s4_mm), G('C3', 'D2', 'numerical', c8s4_mol),
                   G('C3', 'D3', 'numerical', c8s4_part), G('C3', 'D4', 'numerical', c8s4_mass), G('C4', 'D3', 'case', c8_case, gap='G7'), SA(c8_hots[::2], C='C4', D='D4', type='multi_step'),
                   LONG(c8_long[1:], C='C4', D='D4'), G('C2', 'D2', 'mcq', c8s4_mm)],
}
