"""Cambridge International A Level Physics 9702, A Level topics 12-25 (grade 12).

CUP Coursebook (3rd ed.) chapters 16-31 plus A Level practical skills (Paper 5):
1 Motion in a circle, 2 Gravitational fields, 3 Temperature, 4 Ideal gases, 5 Thermodynamics,
6 Oscillations, 7 Electric fields, 8 Capacitance, 9 Magnetic fields, 10 Electromagnetic induction,
11 Alternating currents, 12 Quantum physics, 13 Nuclear physics, 14 Medical physics,
15 Astronomy and cosmology, 16 Planning, analysis and evaluation.

One Topic per W2 subtopic (name = subtopic name). Fixed C1 lists are Paper 1 style MCQs (auto-paired
into two-part recall items); fixed C2 lists are short explanations with mark points; parameterised
templates carry Paper 4 calculations and Paper 5 planning / data analysis and scale with D; compose()
builds Paper 4 structured items with "[n]" part marks. Data as on the 9702 data page:
g = 9.81 m s⁻², G = 6.67 × 10⁻¹¹ N m² kg⁻², e = 1.60 × 10⁻¹⁹ C, h = 6.63 × 10⁻³⁴ J s,
mₑ = 9.11 × 10⁻³¹ kg, c = 3.00 × 10⁸ m s⁻¹, k = 1.38 × 10⁻²³ J K⁻¹, R = 8.31 J K⁻¹ mol⁻¹,
N_A = 6.02 × 10²³ mol⁻¹, ε₀ = 8.85 × 10⁻¹² F m⁻¹, u = 1.66 × 10⁻²⁷ kg, σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴.
"""
import math
import re
from ._lib import topic, mcq, relation, sf, sci, sup, person, two_people, city, num_mcq, near
from .g9_physics import cap, neg, Q, compose, FX
from .g9_physics import numq as _numq
from .g11_physics import nf, E, f3, f2, deg, lab, pickf, nuc

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
GR = 9.81
GG = 6.67e-11
QE = 1.60e-19
C0 = 3.00e8
HP = 6.63e-34
ME = 9.11e-31
MP = 1.67e-27
KB = 1.38e-23
RG = 8.31
NA = 6.02e23
EP0 = 8.85e-12
KC = 1 / (4 * math.pi * EP0)  # 8.99 × 10⁹
UU = 1.66e-27
SIG = 5.67e-8
WIEN = 2.9e-3
PI = math.pi


def numq(*a, **k):
    q = _numq(*a, **k)
    q['stem'] = re.sub(r'(?<!\.)\.\.(?!\.)', '.', q['stem'])
    return q


def sc(x, n=3):
    return sci(x, n)


def calc(r, D, setup, qty, val, unit, working, wrong, fm=f3, more=None):
    """Single calculation (numq) for D <= 3; at D >= 4 with `more` = (text, answer, key-with-marks, m)
    a two-part structured item."""
    if D <= 3 or not more:
        return numq(r, D, setup, qty, val, unit, working, wrong, fm=fm)
    txt, ans, key, m = more
    a = fm(val) + unit
    return Q(f'{setup} (a) Calculate the {qty}. (b) {txt}', f'(a) {a} (b) {ans}',
             f'(a) {working} [1]; = {a} [1] (b) {key} [{2 + m}]', 'multi_step')


def ctx(r, frames, **kw):
    return r.choice(frames).format(p=person(r), c=city(r), **kw)


# ===================================================================== 1 Motion in a circle
N11 = 'Radians, angular displacement and angular speed ω = v/r'
t11 = topic(N11, N11.lower(), 'radians', 'angular speed')
FX(t11, 'C1', (1, 2), [
    ('What is meant by one radian?', 'The angle subtended at the centre of a circle by an arc equal in length to the radius', 'θ = s/r; θ = 1 rad when s = r.',
     ['The angle subtended by an arc equal in length to the diameter', 'One complete revolution divided by 360', 'The angle swept out in one second']),
    ('How many radians are there in one complete revolution?', '2π rad', '360° = 2π rad.', ['π rad', '360π rad', 'π/2 rad']),
    ('An angle of 60° expressed in radians is', 'π/3 rad', '60 × π/180 = π/3.', ['π/6 rad', 'π/2 rad', '3π rad']),
    ('What is the angular speed of the minute hand of a clock?', '1.75 × 10⁻³ rad s⁻¹', 'ω = 2π/3600 s = 1.75 × 10⁻³ rad s⁻¹.', ['0.105 rad s⁻¹', '1.45 × 10⁻⁴ rad s⁻¹', '6.28 rad s⁻¹']),
    ('What is the SI unit of angular speed?', 'rad s⁻¹', 'ω = Δθ/Δt.', ['rad s⁻²', 'm s⁻¹', 'rad m⁻¹']),
    ('A wheel turns at 120 revolutions per minute. What is its angular speed?', '12.6 rad s⁻¹', '2 rev s⁻¹ × 2π = 12.6 rad s⁻¹.', ['2.0 rad s⁻¹', '754 rad s⁻¹', '0.105 rad s⁻¹']),
    ('A point on a rotating disc moves at speed v at distance r from the axis. A point at distance 2r on the same disc moves at', '2v', 'v = ωr and ω is the same for all points on the disc.', ['v', 'v/2', '4v']),
    ('Which quantity is the same for every point on a rotating rigid wheel?', 'angular speed', 'All points turn through the same angle in the same time.', ['linear speed', 'centripetal acceleration', 'distance travelled per revolution']),
    ('Define angular speed.', 'The rate of change of angular displacement (angle swept out per unit time).', 'rate of change of angle / angular displacement [1]'),
    ('State the equation relating linear speed v, angular speed ω and radius r.', 'v = ωr', 'v = ωr [1]'),
])
FX(t11, 'C2', (1, 2, 3, 4), [
    ('Use the definition of the radian to show that v = ωr for an object moving in a circle at constant speed.', 'Arc length s = rθ; dividing by time t gives s/t = r(θ/t), i.e. v = ωr.', 's = rθ from definition of radian [1]; divide by t to give v = ωr [1] [2]'),
    ('Explain why an object moving in a circle at constant speed is accelerating.', 'Its direction of motion changes continuously, so its velocity changes; acceleration is the rate of change of velocity.', 'velocity is a vector / direction changes [1]; acceleration = rate of change of velocity [1] [2]'),
    ('Explain why a point on the Earth\'s equator has a greater linear speed than a point at latitude 60° N, although both have the same angular speed.', 'Both turn through 2π rad in one day, so ω is the same; the point at 60° N moves in a circle of smaller radius (R cos 60°), and v = ωr.', 'same ω (same period) [1]; smaller radius of circle at 60° so smaller v = ωr [1] [2]'),
    ('Explain why the radian is described as having no dimensions.', 'It is defined as a ratio of two lengths (arc length ÷ radius), so the units cancel.', 'ratio of arc length to radius [1]; units of length cancel [1] [2]'),
    ('A student says that the hour hand of a clock has a greater angular speed than the minute hand because it is shorter. Explain why the student is wrong.', 'Angular speed depends only on the time for one revolution: the hour hand takes 12 h, the minute hand 1 h, so the minute hand has the greater ω; length affects only the linear speed of the tip.', 'ω = 2π/T, independent of length [1]; minute hand has shorter T so larger ω [1] [2]'),
])

SPIN = [('a washing-machine drum of radius {r} m', 'rpm', (0.22, 0.30), (600, 800, 1000, 1200, 1400)),
        ('a car wheel of radius {r} m', 'rpm', (0.28, 0.33), (300, 450, 600, 750, 900)),
        ('a fairground ride of radius {r} m', 'T', (4.0, 9.0), (6.0, 8.0, 10.0, 12.0, 15.0)),
        ('a wind-turbine blade of length {r} m', 'rpm', (35.0, 60.0), (12, 15, 18, 20)),
        ('a laboratory centrifuge rotor of radius {r} m', 'rpm', (0.08, 0.15), (3000, 4500, 6000, 9000)),
        ('a potter\'s wheel of radius {r} m', 'rpm', (0.15, 0.25), (60, 90, 120, 150)),
        ('a London-Eye style observation wheel of radius {r} m', 'T', (40.0, 70.0), (1200.0, 1800.0, 2100.0)),
        ('a vinyl record of radius {r} m', 'rpm', (0.12, 0.16), (33, 45, 78))]


def _spin(r):
    desc, kind, (lo, hi), vals = r.choice(SPIN)
    rad = round(r.uniform(lo, hi), 2 if hi < 1 else 1)
    v0 = r.choice(vals)
    if kind == 'rpm':
        w = 2 * PI * v0 / 60
        txt = f'{desc.format(r=nf(rad))} rotates at {v0} revolutions per minute'
    else:
        w = 2 * PI / v0
        txt = f'{desc.format(r=nf(rad))} completes one revolution every {nf(v0)} s'
    return txt, rad, w, kind, v0


@t11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_omega(r, D):
    txt, rad, w, kind, v0 = _spin(r)
    lead = ctx(r, ['In {c}, ', 'During a visit to a science centre, {p} notes that ', 'A data sheet states that ', ''])
    s = cap(f'{lead}{txt}.')
    wk = f'ω = 2π × {v0}/60' if kind == 'rpm' else f'ω = 2π/{nf(v0)}'
    if D <= 2:
        return numq(r, D, s, 'angular speed', w, ' rad s⁻¹', wk, [w / (2 * PI), w * 60, w * rad], fm=f3)
    v = w * rad
    if D == 3:
        return Q(s + ' Calculate the angular speed and the linear speed of a point on the rim.', f'ω = {f3(w)} rad s⁻¹; v = {f3(v)} m s⁻¹',
                 f'{wk} = {f3(w)} rad s⁻¹ [1]; v = ωr [1]; = {f3(v)} m s⁻¹ [1] [3]')
    t = r.choice([0.40, 0.75, 1.5, 2.5]) if w > 1 else r.choice([30.0, 60.0, 90.0])
    th = w * t
    return Q(s + f' (a) Calculate the angular speed. (b) Calculate the speed of a point on the rim. (c) Calculate the angle, in radians and in degrees, swept out by a radius in {nf(t)} s.',
             f'(a) {f3(w)} rad s⁻¹ (b) {f3(v)} m s⁻¹ (c) {f3(th)} rad = {f3(math.degrees(th))}°',
             f'(a) {wk} = {f3(w)} rad s⁻¹ [1] (b) v = ωr = {f3(v)} m s⁻¹ [1] (c) θ = ωt = {f3(th)} rad [1]; × 180/π = {f3(math.degrees(th))}° [1] [4]', 'multi_step')


@t11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_arc(r, D):
    rad = r.choice([0.45, 0.60, 0.80, 1.2, 2.5, 3.0, 4.5]); ang = r.choice([30, 45, 72, 120, 135, 150, 210, 240, 300])
    obj = r.choice(['the tip of a windscreen wiper', 'a child on a roundabout', 'a point on a rotating door', 'the end of a swinging crane arm', 'a toy train on a circular track', 'a runner on a curved bend'])
    th = math.radians(ang); s_ = rad * th
    s = f'{cap(obj)} moves through an angle of {ang}° on a circular path of radius {nf(rad)} m.'
    if D <= 2:
        return numq(r, D, s, 'distance moved along the arc', s_, ' m', f'θ = {ang} × π/180 = {f3(th)} rad; s = rθ = {nf(rad)} × {f3(th)}', [rad * ang, s_ * 2, rad * ang / 180], fm=f3)
    t = r.choice([1.5, 2.0, 2.4, 3.0, 4.0, 5.0])
    w = th / t
    if D == 3:
        return Q(s + f' The movement takes {nf(t)} s at constant speed. Calculate the angular displacement in radians and the angular speed.', f'θ = {f3(th)} rad; ω = {f3(w)} rad s⁻¹',
                 f'θ = {ang}π/180 = {f3(th)} rad [1]; ω = θ/t [1]; = {f3(w)} rad s⁻¹ [1] [3]')
    return Q(s + f' The movement takes {nf(t)} s at constant speed. (a) Calculate the arc length. (b) Calculate the angular speed. (c) Calculate the linear speed and show it equals ωr.',
             f'(a) {f3(s_)} m (b) {f3(w)} rad s⁻¹ (c) v = s/t = {f3(s_ / t)} m s⁻¹ = ωr', f'(a) s = rθ = {f3(s_)} m [1] (b) ω = θ/t = {f3(w)} rad s⁻¹ [1] (c) v = s/t = {f3(s_ / t)} m s⁻¹ [1]; ωr = {f3(w * rad)} m s⁻¹, equal [1] [4]', 'multi_step')


@t11.add('C2', (2, 3, 4), 'explain')
def t11_compare(r, D):
    a, b = r.sample([('hour hand of a clock', 12 * 3600.0), ('minute hand of a clock', 3600.0), ('second hand of a clock', 60.0), ('Earth spinning on its axis', 86400.0), ('Moon orbiting the Earth', 27.3 * 86400), ('Earth orbiting the Sun', 3.16e7)], 2)
    wa, wb = 2 * PI / a[1], 2 * PI / b[1]
    big = a if wa > wb else b
    return Q(f'Compare the angular speeds of the {a[0]} and the {b[0]}. Explain which is greater and calculate the ratio of the larger to the smaller.',
             f'ω = 2π/T; the {big[0]} has the shorter period so the greater ω; ratio = {f3(max(wa, wb) / min(wa, wb))}',
             f'ω = 2π/T, so ω ∝ 1/T [1]; correct identification of larger ω [1]; ratio = T_long/T_short = {f3(max(wa, wb) / min(wa, wb))} [1] [3]')


def _ang_c4(r, D):
    txt, rad, w, kind, v0 = _spin(r)
    v = w * rad
    intro = cap(f'{txt}.')
    parts = [
        lambda r: ('Define the radian.', 'The angle subtended at the centre of a circle by an arc equal in length to the radius.', 'arc length = radius [1]; angle at centre [1] [2]'),
        lambda r: ('Calculate the angular speed.', f'{f3(w)} rad s⁻¹', 'ω = 2π/T or 2πf [2]'),
        lambda r: ('Calculate the linear speed of a point on the rim.', f'{f3(v)} m s⁻¹', 'v = ωr [2]'),
        lambda r: ('Calculate the linear speed of a point halfway between the axis and the rim.', f'{f3(v / 2)} m s⁻¹', 'same ω, half radius [1]'),
        lambda r: ('Explain why a point on the rim is accelerating even though its speed is constant.', 'Its direction changes continuously so its velocity changes.', 'direction / velocity changes [1]'),
        lambda r: ('Calculate the time for the rim to turn through 3π/2 rad.', f'{f3(1.5 * PI / w)} s', 't = θ/ω [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t11.add('C4', (2, 3, 4, 5), 'multi_step')(_ang_c4)

N12 = 'Centripetal acceleration a = rω² = v²/r and centripetal force'
t12 = topic(N12, N12.lower(), 'centripetal acceleration', 'centripetal force')
FX(t12, 'C1', (1, 2), [
    ('An object moves in a circle at constant speed. In which direction is its acceleration?', 'towards the centre of the circle', 'Centripetal acceleration is directed towards the centre.', ['along the tangent in the direction of motion', 'away from the centre', 'along the tangent opposite to the motion']),
    ('Which expression gives the centripetal acceleration of an object moving at speed v in a circle of radius r with angular speed ω?', 'rω²', 'a = v²/r = rω².', ['r²ω', 'v/r²', 'ω/r']),
    ('A car of mass 1000 kg travels round a bend of radius 50 m at 20 m s⁻¹. What is the centripetal force on it?', '8000 N', 'F = mv²/r = 1000 × 400/50.', ['400 N', '2500 N', '20 000 N']),
    ('What provides the centripetal force on a car turning a corner on a flat road?', 'friction between the tyres and the road', 'Sideways friction acts towards the centre of the bend.', ['the weight of the car', 'the normal contact force', 'the driving force of the engine']),
    ('What provides the centripetal force on the Moon as it orbits the Earth?', 'the gravitational pull of the Earth', 'Gravity acts towards the Earth\'s centre.', ['the Moon\'s weight towards the Sun', 'a centrifugal force', 'the Moon\'s inertia']),
    ('A stone on a string moves in a horizontal circle. Its speed is doubled at the same radius. The tension needed becomes', 'four times as large', 'F = mv²/r ∝ v².', ['twice as large', 'half as large', 'unchanged']),
    ('Why does the centripetal force on an object in uniform circular motion do no work?', 'It is always perpendicular to the velocity', 'No displacement in the direction of the force, so W = 0 and the speed is constant.', ['It is balanced by a centrifugal force', 'It is too small to do work', 'The object has no kinetic energy']),
    ('State what is meant by centripetal force.', 'The resultant force on an object moving in a circle, directed towards the centre of the circle.', 'resultant force towards centre [1]'),
])
FX(t12, 'C2', (1, 2, 3, 4), [
    ('Explain why the centripetal force does not change the speed of an object moving in a circle.', 'The force is always perpendicular to the velocity, so it has no component along the direction of motion; no work is done and the kinetic energy (speed) stays constant, only the direction changes.', 'force perpendicular to velocity [1]; no work done / KE constant, only direction changes [1] [2]'),
    ('A passenger in a car turning a corner feels pushed outwards. Explain, using Newton\'s first law, what is actually happening.', 'The passenger tends to continue in a straight line (inertia); the car turns beneath them, so the door pushes inwards on them to provide the centripetal force; there is no outward force on them.', 'tendency to continue in straight line [1]; door/seat provides inward force, no outward force [1] [2]'),
    ('A stone is whirled in a horizontal circle on a string and the string breaks. Describe and explain the subsequent motion of the stone (ignore gravity).', 'With no resultant force it moves in a straight line at constant speed along the tangent to the circle at the point of release (Newton\'s first law).', 'tangent to circle [1]; no resultant force so constant velocity [1] [2]'),
    ('Show that the expressions a = v²/r and a = rω² are equivalent.', 'v = ωr, so v²/r = ω²r²/r = rω².', 'substitute v = ωr [1]; simplify to rω² [1] [2]'),
    ('Explain why centripetal force should not be drawn as an extra force on a free-body diagram.', 'It is not a separate force: it is the name for the resultant of the real forces (tension, friction, gravity, normal force) acting towards the centre.', 'centripetal force is a resultant [1]; provided by real forces such as tension or friction [1] [2]'),
    ('Explain why a car is more likely to skid outwards on a bend when it is travelling fast.', 'The centripetal force needed, mv²/r, increases with v²; friction has a maximum value, so above a certain speed friction cannot supply enough force and the car moves to a larger radius.', 'required force ∝ v² [1]; friction limited, so insufficient [1] [2]'),
])
relation(t12, 'C2', (2, 3), 'F = mv²/r', 'centripetal force required', {'speed': 2, 'mass': 1, 'radius': -1},
         ['A car travels round a circular test track at constant speed.', 'A ball on a string is whirled in a horizontal circle on a smooth table.', 'A cyclist rides round a flat circular velodrome bend.', 'An aircraft performs a horizontal circular turn.'])

CIRC = [('a car of mass {m} kg', 'a bend of radius {r} m', 'friction between the tyres and the road', (800, 1200, 1500, 1800), (25.0, 40.0, 60.0, 80.0, 120.0), (8.0, 12.0, 15.0, 20.0, 25.0)),
        ('a cyclist and bicycle of total mass {m} kg', 'a flat bend of radius {r} m', 'friction between the tyres and the track', (65, 75, 85, 90), (12.0, 18.0, 25.0, 30.0), (5.0, 7.0, 9.0, 11.0)),
        ('a ball of mass {m} kg on a string', 'a horizontal circle of radius {r} m on a smooth table', 'the tension in the string', (0.050, 0.10, 0.20, 0.25), (0.40, 0.50, 0.75, 1.2), (2.0, 3.0, 4.5, 6.0)),
        ('a train of mass {m} kg', 'a curve of radius {r} m', 'the sideways force of the rails on the wheel flanges', (2.0e5, 3.5e5, 4.0e5), (400.0, 600.0, 900.0, 1200.0), (20.0, 25.0, 30.0, 40.0)),
        ('a runner of mass {m} kg', 'a bend of radius {r} m', 'friction between the shoes and the track', (55, 62, 70, 78), (36.5, 40.0, 45.0), (6.5, 8.0, 9.5)),
        ('an aircraft of mass {m} kg', 'a horizontal circle of radius {r} m', 'the horizontal component of the lift force', (5.0e4, 8.0e4, 1.2e5), (2000.0, 3000.0, 4500.0), (120.0, 150.0, 200.0, 240.0))]


def _circ(r):
    who, path, prov, ms, rs, vs = r.choice(CIRC)
    m, rad, v = r.choice(ms), r.choice(rs), r.choice(vs)
    return who.format(m=E(m)), path.format(r=nf(rad)), prov, m, rad, v


@t12.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_force(r, D):
    who, path, prov, m, rad, v = _circ(r)
    F = m * v * v / rad
    s = cap(f'{who} moves round {path} at a constant speed of {nf(v)} m s⁻¹.')
    if D <= 2:
        q = r.choice(['acc', 'force'])
        if q == 'acc':
            return numq(r, D, s, 'centripetal acceleration', v * v / rad, ' m s⁻²', f'a = v²/r = {nf(v)}²/{nf(rad)}', [v / rad, v * v * rad, v * v / rad / GR], fm=f3)
        return numq(r, D, s, 'centripetal force', F, ' N', f'F = mv²/r = {E(m)} × {nf(v)}²/{nf(rad)}', [m * v / rad, m * v * v * rad, F / 2], fm=f3)
    if D == 3:
        return Q(s + ' Calculate the angular speed and the centripetal force, and state what provides this force.', f'ω = {f3(v / rad)} rad s⁻¹; F = {f3(F)} N; provided by {prov}',
                 f'ω = v/r = {f3(v / rad)} rad s⁻¹ [1]; F = mv²/r = {f3(F)} N [1]; {prov} [1] [3]')
    Fmax = F * r.choice([1.3, 1.5, 1.8, 2.2])
    vmax = math.sqrt(Fmax * rad / m)
    return Q(s + f' (a) Calculate the centripetal force. (b) The maximum force that {prov} can provide is {f3(Fmax)} N. Calculate the maximum speed for this radius. (c) Explain what happens if this speed is exceeded.',
             f'(a) {f3(F)} N (b) {f3(vmax)} m s⁻¹ (c) the force available is less than mv²/r, so the path curves less sharply: it moves outwards to a larger radius (skids)',
             f'(a) F = mv²/r = {f3(F)} N [1] (b) v = √(Fr/m) [1]; = {f3(vmax)} m s⁻¹ [1] (c) insufficient centripetal force [1]; moves to larger radius / skids outwards [1] [5]', 'multi_step')


@t12.add('C3', (2, 3, 4, 5), 'numerical')
def t12_rpm(r, D):
    dev, rad, rpm = r.choice([('centrifuge', [0.080, 0.10, 0.12, 0.15], [3000, 4000, 6000, 8000]), ('washing-machine drum', [0.22, 0.25, 0.28], [800, 1000, 1200, 1400]),
                              ('salad spinner', [0.10, 0.12, 0.14], [120, 180, 240]), ('astronaut-training centrifuge', [6.0, 8.0, 9.0], [20, 25, 30, 35])])
    rad, rpm = r.choice(rad), r.choice(rpm)
    w = 2 * PI * rpm / 60; a = rad * w * w
    m = r.choice([0.010, 0.025, 0.050, 0.20]) if 'astronaut' not in dev else r.choice([65, 72, 80])
    s = f'A {dev} of radius {nf(rad)} m rotates at {rpm} revolutions per minute.'
    if D <= 3:
        return Q(s + ' Calculate the centripetal acceleration at the rim and express it as a multiple of g.', f'a = {E(a)} m s⁻²; {E(a / GR)} g',
                 f'ω = 2π × {rpm}/60 = {f3(w)} rad s⁻¹ [1]; a = rω² = {E(a)} m s⁻² [1]; ÷ 9.81 = {E(a / GR)} g [1] [3]')
    return Q(s + f' (a) Calculate the centripetal acceleration at the rim. (b) Calculate the resultant force needed to keep an object of mass {E(m)} kg at the rim moving in the circle. (c) The rotation rate is doubled. State the factor by which this force changes.',
             f'(a) {E(a)} m s⁻² (b) {E(m * a)} N (c) 4 (F ∝ ω²)', f'(a) ω = {f3(w)} rad s⁻¹ [1]; a = rω² = {E(a)} m s⁻² [1] (b) F = ma = {E(m * a)} N [1] (c) F ∝ ω² [1]; factor 4 [1] [5]', 'multi_step')


def _cent_c4(r, D):
    who, path, prov, m, rad, v = _circ(r)
    F = m * v * v / rad
    intro = cap(f'{who} moves at constant speed {nf(v)} m s⁻¹ round {path}.')
    parts = [
        lambda r: ('Explain why a resultant force is needed even though the speed is constant.', 'The direction of the velocity changes, so there is an acceleration (towards the centre), which requires a resultant force (F = ma).', 'velocity changes [1]; resultant force towards centre [1] [2]'),
        lambda r: ('Calculate the angular speed.', f'{f3(v / rad)} rad s⁻¹', 'ω = v/r [1]'),
        lambda r: ('Calculate the centripetal acceleration.', f'{f3(v * v / rad)} m s⁻²', 'a = v²/r [2]'),
        lambda r: ('Calculate the centripetal force.', f'{f3(F)} N', 'F = mv²/r [2]'),
        lambda r: ('State what provides the centripetal force.', cap(prov) + '.', 'correct force [1]'),
        lambda r: ('The speed increases by 50% on the same path. Calculate the new centripetal force.', f'{f3(2.25 * F)} N', 'F ∝ v², × 2.25 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12.add('C4', (2, 3, 4, 5), 'multi_step')(_cent_c4)

N13 = 'Applications of circular motion: banked tracks, loops and conical pendulum'
t13 = topic(N13, N13.lower(), 'banked tracks', 'conical pendulum')
FX(t13, 'C1', (1, 2), [
    ('A car travels round a frictionless banked track at the design speed v. The bank angle is θ and the radius r. Which equation applies?', 'tan θ = v²/(rg)', 'N sin θ = mv²/r and N cos θ = mg; divide.', ['sin θ = v²/(rg)', 'tan θ = rg/v²', 'cos θ = v²/(rg)']),
    ('A ball on a string moves in a vertical circle. Where is the tension in the string greatest?', 'at the bottom of the circle', 'T − mg = mv²/r at the bottom: T = mg + mv²/r, and v is also greatest there.', ['at the top of the circle', 'when the string is horizontal', 'it is the same everywhere']),
    ('A roller-coaster car just completes a vertical loop of radius r. What is its speed at the top of the loop?', '√(gr)', 'At minimum speed the weight alone provides the centripetal force: mg = mv²/r.', ['√(2gr)', 'gr', '√(5gr)']),
    ('In a conical pendulum, what provides the centripetal force on the bob?', 'the horizontal component of the tension', 'T sin θ = mv²/r; T cos θ balances the weight.', ['the weight of the bob', 'the vertical component of the tension', 'air resistance']),
    ('A conical pendulum bob of weight W hangs from a string making angle θ with the vertical. What is the tension?', 'W/cos θ', 'T cos θ = W.', ['W cos θ', 'W sin θ', 'W/sin θ']),
    ('Why does an aircraft bank (tilt its wings) to turn in a horizontal circle?', 'so that a horizontal component of the lift provides the centripetal force', 'Lift is perpendicular to the wings; tilting gives it a horizontal component.', ['to reduce the drag on the wings', 'to increase the weight of the aircraft', 'so that the engine thrust acts vertically']),
    ('State the condition for an object on a string to just complete a vertical circle.', 'At the top, the tension is zero and the weight alone provides the centripetal force (mg = mv²/r).', 'T = 0 at top, mg = mv²/r [1]'),
])
FX(t13, 'C2', (1, 2, 3, 4), [
    ('Explain how a banked track allows a car to go round a bend without relying on friction.', 'The normal contact force is perpendicular to the tilted surface, so it has a horizontal component towards the centre; at the design speed this component alone provides mv²/r while the vertical component balances the weight.', 'normal force tilted [1]; horizontal component provides centripetal force [1] [2]'),
    ('Explain why water stays in a bucket swung quickly in a vertical circle, even when the bucket is upside down at the top.', 'At the top, the centripetal force needed (mv²/r) is greater than the weight of the water, so the bucket base must push down on the water; the water stays pressed against the base. If v were too small, mg > mv²/r and the water would fall out.', 'required centripetal force > weight [1]; base pushes on water / water stays in contact [1] [2]'),
    ('Explain why the reading on a scale under a passenger in a big wheel is smaller at the top of the ride than at the bottom.', 'At the top, mg − N = mv²/r, so N = mg − mv²/r < mg; at the bottom, N − mg = mv²/r, so N = mg + mv²/r > mg.', 'top: N = mg − mv²/r [1]; bottom: N = mg + mv²/r [1] [2]'),
    ('Explain why the string of a conical pendulum can never be horizontal.', 'The vertical component of the tension must balance the weight; a horizontal string has no vertical component, so θ < 90° for any finite tension.', 'vertical component must equal mg [1]; horizontal string gives zero vertical component [1] [2]'),
])


@t13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_bank(r, D):
    rad = r.choice([60.0, 80.0, 120.0, 150.0, 200.0, 250.0]); v = r.choice([15.0, 18.0, 20.0, 25.0, 30.0, 35.0])
    place = ctx(r, ['A motor-racing circuit near {c}', 'A test track in {c}', 'A velodrome in {c}', 'A motorway slip road near {c}'])
    th = math.degrees(math.atan(v * v / (rad * GR)))
    if th > 50 or th < 5:
        return None
    s = f'{place} has a bend of radius {nf(rad)} m. It is banked so that a vehicle travelling at {nf(v)} m s⁻¹ needs no sideways friction.'
    if D <= 2:
        return numq(r, D, s, 'angle of banking', th, '°', f'tan θ = v²/(rg) = {nf(v)}²/({nf(rad)} × 9.81)', [math.degrees(math.atan(rad * GR / v / v)), math.degrees(math.asin(min(1, v * v / rad / GR))), th / 2], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' By resolving the normal contact force, show that tan θ = v²/(rg) and calculate the angle of banking.', f'N cos θ = mg, N sin θ = mv²/r ⇒ tan θ = v²/(rg); θ = {nf(th, 3)}°',
                 f'N cos θ = mg [1]; N sin θ = mv²/r and divide [1]; θ = {nf(th, 3)}° [1] [3]')
    return Q(s + ' (a) Calculate the angle of banking. (b) A vehicle goes round the bend faster than this speed. State and explain the direction of the friction force needed. (c) Suggest why banking is useful for a road used in icy conditions.',
             f'(a) {nf(th, 3)}° (b) friction acts down the slope (towards the centre): N sin θ alone is too small for the larger mv²/r (c) cars can turn at the design speed even when friction is very small',
             f'(a) tan θ = v²/(rg) [1]; θ = {nf(th, 3)}° [1] (b) down the slope / inwards [1]; more centripetal force needed [1] (c) little friction needed [1] [5]', 'multi_step')


@t13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_loop(r, D):
    m = r.choice([0.20, 0.35, 0.50, 0.80]); rad = r.choice([0.60, 0.80, 1.0, 1.2]); v = r.choice([4.0, 5.0, 6.0, 7.0])
    if v * v / rad < GR * 1.05:
        v = round(math.sqrt(GR * rad) * 1.6, 1)
    obj = r.choice(['A ball', 'A small bucket of water', 'A conker', 'A model aircraft'])
    s = f'{obj} of mass {nf(m)} kg is whirled in a vertical circle of radius {nf(rad)} m on a string. At the top of the circle its speed is {nf(v)} m s⁻¹.'
    Tt = m * v * v / rad - m * GR
    if D <= 2:
        return numq(r, D, s, 'tension in the string at the top', Tt, ' N', f'T + mg = mv²/r ⇒ T = {nf(m)} × {nf(v)}²/{nf(rad)} − {nf(m)} × 9.81', [Tt + 2 * m * GR, m * v * v / rad, m * v / rad], fm=f3)
    vmin = math.sqrt(GR * rad)
    vb = math.sqrt(v * v + 2 * GR * 2 * rad); Tb = m * vb * vb / rad + m * GR
    if D == 3:
        return Q(s + ' Calculate the tension in the string at the top, and the minimum speed at the top for the string to stay taut.', f'T = {f3(Tt)} N; v_min = {f3(vmin)} m s⁻¹',
                 f'T + mg = mv²/r [1]; T = {f3(Tt)} N [1]; v_min = √(gr) = {f3(vmin)} m s⁻¹ [1] [3]')
    return Q(s + ' (a) Calculate the tension at the top. (b) Use conservation of energy to find the speed at the bottom of the circle. (c) Calculate the tension at the bottom.',
             f'(a) {f3(Tt)} N (b) {f3(vb)} m s⁻¹ (c) {f3(Tb)} N', f'(a) T = mv²/r − mg = {f3(Tt)} N [1] (b) ½mv_b² = ½mv² + mg(2r) [1]; v_b = {f3(vb)} m s⁻¹ [1] (c) T − mg = mv²/r [1]; T = {f3(Tb)} N [1] [5]', 'multi_step')


@t13.add('C3', (2, 3, 4, 5), 'numerical')
def t13_conical(r, D):
    L = r.choice([0.40, 0.50, 0.60, 0.80, 1.0]); th = r.choice([20, 25, 30, 35, 40, 50]); m = r.choice([0.10, 0.15, 0.20, 0.30])
    tr = math.radians(th); rad = L * math.sin(tr)
    T = m * GR / math.cos(tr); w = math.sqrt(GR * math.tan(tr) / rad); P = 2 * PI / w
    s = f'A conical pendulum consists of a bob of mass {nf(m)} kg on a string of length {nf(L)} m. The bob moves in a horizontal circle with the string at {th}° to the vertical.'
    if D <= 3:
        return Q(s + ' Calculate the tension in the string and the radius of the circle.', f'T = {f3(T)} N; r = {f3(rad)} m', f'T cos θ = mg [1]; T = {f3(T)} N [1]; r = L sin θ = {f3(rad)} m [1] [3]')
    return Q(s + ' (a) Calculate the tension in the string. (b) Calculate the angular speed of the bob. (c) Calculate the period of the motion.',
             f'(a) {f3(T)} N (b) {f3(w)} rad s⁻¹ (c) {f3(P)} s', f'(a) T = mg/cos θ = {f3(T)} N [1] (b) T sin θ = mrω², r = L sin θ [1]; ω = {f3(w)} rad s⁻¹ [1] (c) period = 2π/ω = {f3(P)} s [1] [4]', 'multi_step')


def _app_c4(r, D):
    m = r.choice([400, 500, 600]); rad = r.choice([8.0, 10.0, 12.0]); h = r.choice([30.0, 35.0, 40.0])
    vt2 = 2 * GR * (h - 2 * rad); vt = math.sqrt(vt2)
    if vt2 < GR * rad:
        return None
    vb = math.sqrt(2 * GR * h)
    intro = f'A roller-coaster car of mass {m} kg is released from rest at a height of {nf(h)} m above the bottom of a vertical circular loop of radius {nf(rad)} m. Friction is negligible.'
    parts = [
        lambda r: ('Calculate the speed of the car at the top of the loop.', f'{f3(vt)} m s⁻¹', 'mg(h − 2r) = ½mv² [2]'),
        lambda r: ('Calculate the minimum speed needed at the top of the loop for the car to stay on the track.', f'{f3(math.sqrt(GR * rad))} m s⁻¹', 'v = √(gr) [2]'),
        lambda r: ('Calculate the normal contact force from the track on the car at the top of the loop.', f'{f3(m * vt2 / rad - m * GR)} N', 'N + mg = mv²/r [3]'),
        lambda r: ('Calculate the normal contact force at the bottom of the loop.', f'{f3(m * vb * vb / rad + m * GR)} N', 'N − mg = mv²/r with v² = 2gh [3]'),
        lambda r: ('Explain why passengers feel heavier at the bottom of the loop.', 'The seat must push up with N = mg + mv²/r, which is greater than their weight.', 'N > mg [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t13.add('C4', (2, 3, 4, 5), 'multi_step')(_app_c4)
CHAPTERS[1] = [t11, t12, t13]

# ===================================================================== 2 Gravitational fields
PLANETS = [('Earth', 5.97e24, 6.37e6), ('Mars', 6.42e23, 3.39e6), ('the Moon', 7.35e22, 1.74e6), ('Jupiter', 1.90e27, 6.99e7),
           ('Venus', 4.87e24, 6.05e6), ('Mercury', 3.30e23, 2.44e6), ('Saturn', 5.68e26, 5.82e7), ('Neptune', 1.02e26, 2.46e7)]

N21 = 'Gravitational field and field strength g = F/m and field lines'
t21 = topic(N21, N21.lower(), 'gravitational field', 'field strength')
FX(t21, 'C1', (1, 2), [
    ('Which is the definition of gravitational field strength at a point?', 'the gravitational force per unit mass on a small mass placed at the point', 'g = F/m.', ['the work done per unit mass bringing a mass from infinity', 'the force between two unit masses 1 m apart', 'the acceleration of any object at the point when thrown']),
    ('What is the SI unit of gravitational field strength?', 'N kg⁻¹', 'g = F/m: N kg⁻¹ (equivalent to m s⁻²).', ['N kg', 'J kg⁻¹', 'kg N⁻¹']),
    ('Which describes the gravitational field lines around an isolated spherical planet?', 'radial and directed towards the centre', 'Field lines show the direction of the force on a mass: inwards, radial.', ['radial and directed away from the centre', 'parallel and equally spaced', 'circles centred on the planet']),
    ('Close to the Earth\'s surface, over a small region, the gravitational field is', 'approximately uniform', 'Field lines are nearly parallel and equally spaced over a small height range.', ['zero', 'radial and strongly varying', 'directed upwards']),
    ('A rock of mass 4.0 kg has weight 6.4 N on the Moon. What is the gravitational field strength there?', '1.6 N kg⁻¹', 'g = F/m = 6.4/4.0.', ['0.63 N kg⁻¹', '26 N kg⁻¹', '9.81 N kg⁻¹']),
    ('What does the spacing of gravitational field lines indicate?', 'the strength of the field: closer lines mean a stronger field', 'Field line density represents field strength.', ['the mass of the object in the field', 'the direction of motion of all objects', 'the gravitational potential energy only']),
    ('State what is meant by a gravitational field.', 'A region of space in which a mass experiences a force.', 'region where a mass experiences a force [1]'),
])
FX(t21, 'C2', (1, 2, 3, 4), [
    ('Explain why the gravitational field near the Earth\'s surface can be treated as uniform in a laboratory but not for a satellite in orbit.', 'Over a few metres the change in distance from the Earth\'s centre is tiny compared with the Earth\'s radius, so g is almost constant and lines are effectively parallel; a satellite\'s orbit covers distances comparable with R, so g varies significantly (radial field).', 'height change ≪ R so g constant [1]; orbit distance comparable to R, field radial / varies [1] [2]'),
    ('Show that the units N kg⁻¹ and m s⁻² are equivalent.', '1 N = 1 kg m s⁻², so N kg⁻¹ = kg m s⁻² kg⁻¹ = m s⁻².', 'N = kg m s⁻² [1]; cancel kg [1] [2]'),
    ('Explain why gravitational field lines never cross.', 'A field line shows the direction of the force on a mass at that point; if lines crossed, the force would have two directions at one point, which is impossible.', 'line gives direction of force [1]; unique direction at each point [1] [2]'),
    ('Distinguish between the mass and the weight of an astronaut, and explain which changes on a journey to Mars.', 'Mass is the amount of matter (resistance to acceleration) and is constant; weight is the gravitational force mg and depends on the local field strength, so weight changes.', 'mass constant [1]; weight = mg, changes with g [1] [2]'),
])


@t21.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_weight(r, D):
    nm, M, R = r.choice(PLANETS)
    g = GG * M / R ** 2
    m = r.choice([12.0, 25.0, 60.0, 75.0, 150.0, 850.0, 1200.0])
    obj = r.choice(['a rover', 'an instrument package', 'a scientific instrument', 'a lander', 'a sample container'])
    W = m * g
    if D <= 2:
        return numq(r, D, f'The gravitational field strength at the surface of {nm} is {f3(g)} N kg⁻¹. {cap(obj)} has a mass of {E(m)} kg.', f'weight of {obj} on {nm}', W, ' N', f'W = mg = {E(m)} × {f3(g)}', [m / g, m * GR, W / 2], fm=f3)
    if D == 3:
        return Q(f'{cap(obj)} has a weight of {f3(W)} N on the surface of {nm}, where it has mass {E(m)} kg. Calculate the gravitational field strength at the surface of {nm} and the weight of the same object on Earth.', f'g = {f3(g)} N kg⁻¹; W_E = {f3(m * GR)} N',
                 f'g = F/m [1]; = {f3(g)} N kg⁻¹ [1]; W = m × 9.81 = {f3(m * GR)} N [1] [3]')
    return Q(f'{cap(obj)} of mass {E(m)} kg weighs {f3(W)} N at the surface of {nm}. (a) Calculate the gravitational field strength at the surface. (b) Explain why the mass is the same on Earth as on {nm}. (c) Calculate the initial acceleration of the object if dropped near the surface of {nm}, ignoring any atmosphere.',
             f'(a) {f3(g)} N kg⁻¹ (b) mass is the quantity of matter and does not depend on the field (c) {f3(g)} m s⁻²', f'(a) g = W/m = {f3(g)} N kg⁻¹ [1]; unit [1] (b) mass independent of location [1] (c) a = F/m = g = {f3(g)} m s⁻² [1] [4]', 'multi_step')


@t21.add('C2', (2, 3, 4), 'explain')
def t21_lines(r, D):
    sit = r.choice([('a uniform field in a small region near the Earth\'s surface', 'parallel, equally spaced lines pointing vertically downwards'),
                    ('the field around an isolated planet', 'radial lines pointing inwards towards the centre, getting further apart with distance'),
                    ('the field between the Earth and the Moon along the line joining them', 'lines pointing towards each body, with a point between them (closer to the Moon) where the resultant field is zero'),
                    ('the field around a uniform spherical star', 'radial lines pointing inwards, identical outside the star to those of a point mass at its centre')])
    return Q(f'Describe the pattern of gravitational field lines for {sit[0]}, and explain what the pattern shows about the field strength.', cap(sit[1]) + '; the closer the lines, the stronger the field.',
             'correct shape and direction [1]; spacing related to field strength [1]' + (' ; reason linked to inverse-square law or uniformity [1] [3]' if D >= 3 else ' [2]'))


def _gf_c4(r, D):
    nm, M, R = r.choice(PLANETS)
    g = GG * M / R ** 2
    m = r.choice([150, 300, 500])
    intro = f'A lander of mass {m} kg rests on the surface of {nm}, where the gravitational field strength is {f3(g)} N kg⁻¹.'
    parts = [
        lambda r: ('Define gravitational field strength.', 'Force per unit mass on a small mass placed at the point.', 'force per unit mass [1]'),
        lambda r: ('Calculate the weight of the lander.', f'{f3(m * g)} N', 'W = mg [2]'),
        lambda r: ('Describe the field lines close to the surface over the landing site.', 'Parallel, equally spaced, pointing vertically downwards (uniform).', 'parallel/equally spaced [1]; downwards [1] [2]'),
        lambda r: ('Explain why the field lines further out are radial and spread apart.', 'The planet acts as a point mass at its centre; field strength decreases with distance (inverse square).', 'point mass / radial [1]; weaker with distance [1] [2]'),
        lambda r: (f'The lander\'s thrusters give an upward force of {nf(round(1.5 * m * g, -1))} N on lift-off. Calculate its initial acceleration.', f'{f3((round(1.5 * m * g, -1) - m * g) / m)} m s⁻²', 'a = (F − mg)/m [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t21.add('C4', (2, 3, 4, 5), 'multi_step')(_gf_c4)

N22 = "Newton's law of gravitation F = GMm/r² and g = GM/r²"
t22 = topic(N22, N22.lower(), "newton's law of gravitation", 'g = gm/r²')
FX(t22, 'C1', (1, 2), [
    ('Two point masses attract each other with force F. The distance between them is doubled. What is the new force?', 'F/4', 'F ∝ 1/r².', ['F/2', '2F', '4F']),
    ('What is the unit of the gravitational constant G?', 'N m² kg⁻²', 'G = Fr²/(Mm).', ['N m kg⁻¹', 'N kg² m⁻²', 'N m² kg⁻¹']),
    ('The gravitational field strength at the Earth\'s surface is g. What is it at a height equal to the Earth\'s radius above the surface?', 'g/4', 'Distance from centre doubles; g ∝ 1/r².', ['g/2', 'g', 'g/8']),
    ('Planet P has twice the mass and twice the radius of planet Q. The surface field strength on P compared with Q is', 'half as large', 'g = GM/R² ∝ 2/4.', ['twice as large', 'the same', 'four times as large']),
    ('Why can a uniform sphere be treated as a point mass when calculating its gravitational field outside it?', 'Its mass acts as if concentrated at its centre', 'Outside a uniform sphere the field is that of a point mass at the centre.', ['Its radius is always negligible', 'Gravity only acts on the surface', 'Its density is zero outside']),
    ('Which expression gives the field strength at distance r from the centre of a planet of mass M (r greater than the planet\'s radius)?', 'GM/r²', 'g = F/m = GM/r².', ['GM/r', 'GMm/r²', 'Gr²/M']),
    ('State Newton\'s law of gravitation.', 'Two point masses attract each other with a force proportional to the product of their masses and inversely proportional to the square of their separation.', 'force ∝ product of masses [1]; ∝ 1/separation² (point masses) [1] [2]'),
])
FX(t22, 'C2', (1, 2, 3, 4), [
    ('Derive the expression g = GM/r² for the field strength due to a point mass M.', 'Force on test mass m: F = GMm/r²; g = F/m = GM/r².', 'F = GMm/r² [1]; divide by m [1] [2]'),
    ('Explain why the gravitational force between two students sitting next to each other is not noticed.', 'G is very small (6.67 × 10⁻¹¹ N m² kg⁻²); for masses of about 60 kg at 1 m the force is about 10⁻⁷ N, negligible compared with friction and their weights.', 'G very small [1]; force ~10⁻⁷ N, negligible compared to other forces [1] [2]'),
    ('Explain why the value of g measured at the top of a high mountain is slightly smaller than at sea level.', 'g = GM/r²; at the top the distance from the Earth\'s centre is greater, so g is smaller.', 'g ∝ 1/r² [1]; r larger at summit [1] [2]'),
    ('Explain why the gravitational force on a satellite does not fall to zero even though it is a long way from Earth.', 'The force is inversely proportional to r², so it decreases with distance but only becomes zero at infinite separation.', 'inverse square law [1]; zero only at infinity [1] [2]'),
])
relation(t22, 'C2', (2, 3), 'F = GMm/r²', 'gravitational force between them', {'separation of the centres': -2, 'mass of the smaller body': 1},
         ['Two asteroids attract each other gravitationally.', 'A satellite is attracted by a planet.', 'Two lead spheres in a Cavendish-type experiment attract each other.'])


@t22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_force(r, D):
    pair = r.choice([('the Earth (mass 5.97 × 10²⁴ kg)', 5.97e24, 'the Moon (mass 7.35 × 10²² kg)', 7.35e22, 3.84e8),
                     ('the Sun (mass 1.99 × 10³⁰ kg)', 1.99e30, 'the Earth (mass 5.97 × 10²⁴ kg)', 5.97e24, 1.50e11),
                     ('the Sun (mass 1.99 × 10³⁰ kg)', 1.99e30, 'Mars (mass 6.42 × 10²³ kg)', 6.42e23, 2.28e11),
                     ('Jupiter (mass 1.90 × 10²⁷ kg)', 1.90e27, 'its moon Io (mass 8.93 × 10²² kg)', 8.93e22, 4.22e8),
                     ('two oil tankers each of mass 3.0 × 10⁸ kg', 3.0e8, '', 3.0e8, r.choice([150.0, 200.0, 300.0])),
                     ('two lead spheres of masses 160 kg and 0.75 kg', 160.0, '', 0.75, r.choice([0.20, 0.25, 0.30]))])
    a, M, b, m, d = pair
    F = GG * M * m / d ** 2
    s = f'The centres of {a} and {b} are {E(d)} m apart.' if b else f'The centres of {a} are {E(d)} m apart.'
    if D <= 3:
        return numq(r, D, s, 'gravitational force between them', F, ' N', f'F = GMm/r² = 6.67 × 10⁻¹¹ × {E(M)} × {E(m)}/({E(d)})²', [F * d, GG * M * m / d, F * 4], fm=lambda x: E(x, 3))
    return Q(s + ' (a) Calculate the gravitational force between them. (b) Calculate the separation at which the force would be one ninth of this value.',
             f'(a) {E(F)} N (b) {E(3 * d)} m', f'(a) F = GMm/r² [1]; = {E(F)} N [1] (b) F ∝ 1/r² [1]; r × 3 = {E(3 * d)} m [1] [4]', 'multi_step')


@t22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_g(r, D):
    nm, M, R = r.choice(PLANETS)
    g0 = GG * M / R ** 2
    k = r.choice([0.5, 1.0, 2.0, 3.0]); h = k * R
    gh = GG * M / (R + h) ** 2
    if D <= 2:
        return numq(r, D, f'{cap(nm)} has mass {sc(M)} kg and radius {sc(R)} m.', f'gravitational field strength at the surface of {nm}', g0, ' N kg⁻¹', f'g = GM/R² = 6.67 × 10⁻¹¹ × {sc(M)}/({sc(R)})²', [GG * M / R, g0 * 2, GR], fm=f3)
    if D == 3:
        return Q(f'{cap(nm)} has mass {sc(M)} kg and radius {sc(R)} m. Calculate the gravitational field strength at a height of {E(h)} m above the surface.', f'{f3(gh)} N kg⁻¹',
                 f'r = R + h = {E(R + h)} m [1]; g = GM/r² [1]; = {f3(gh)} N kg⁻¹ [1] [3]')
    return Q(f'The gravitational field strength at the surface of {nm} is {f3(g0)} N kg⁻¹ and its radius is {sc(R)} m. (a) Calculate the mass of {nm}. (b) Calculate the field strength at a height of {E(h)} m above the surface. (c) Calculate the mean density of {nm}.',
             f'(a) {sc(M)} kg (b) {f3(gh)} N kg⁻¹ (c) {E(M / (4 / 3 * PI * R ** 3))} kg m⁻³', f'(a) M = gR²/G = {sc(M)} kg [1] (b) g ∝ 1/r², r = {E(R + h)} m [1]; {f3(gh)} N kg⁻¹ [1] (c) ρ = M/(4/3 πR³) [1]; {E(M / (4 / 3 * PI * R ** 3))} kg m⁻³ [1] [5]', 'multi_step')


@t22.add('C3', (3, 4, 5), 'numerical')
def t22_null(r, D):
    M1, M2, d = 5.97e24, 7.35e22, 3.84e8
    if r.random() < 0.5:
        M1, M2, d = r.choice([(5.97e24, 7.35e22, 3.84e8), (1.90e27, 8.93e22, 4.22e8), (1.99e30, 5.97e24, 1.50e11)])
    x = d / (1 + math.sqrt(M2 / M1))
    return Q(f'Two bodies of masses {sc(M1)} kg and {sc(M2)} kg have centres {sc(d)} m apart. Calculate the distance from the centre of the larger body to the point on the line between them where the resultant gravitational field strength is zero.',
             f'{sc(x)} m', f'GM₁/x² = GM₂/(d − x)² [1]; x/(d − x) = √(M₁/M₂) = {f3(math.sqrt(M1 / M2))} [1]; x = {sc(x)} m [1]' + (' [3]' if D == 3 else '; correct reason why point is nearer the smaller mass [1] [4]'))


def _ng_c4(r, D):
    nm, M, R = r.choice(PLANETS)
    g0 = GG * M / R ** 2
    intro = f'{cap(nm)} may be treated as a uniform sphere of radius {sc(R)} m. The gravitational field strength at its surface is {f3(g0)} N kg⁻¹.'
    parts = [
        lambda r: ('State Newton\'s law of gravitation.', 'Force between point masses ∝ product of masses and ∝ 1/separation².', 'product of masses [1]; inverse square of separation [1] [2]'),
        lambda r: (f'Show that the mass of {nm} is about {sc(M, 2)} kg.', f'M = gR²/G = {sc(M)} kg', 'g = GM/R² [1]; substitution and answer [1] [2]'),
        lambda r: ('Calculate the field strength at a distance of 3R from the centre.', f'{f3(g0 / 9)} N kg⁻¹', 'g ∝ 1/r², ÷ 9 [2]'),
        lambda r: ('Explain why the planet can be treated as a point mass for points outside it.', 'For a uniform sphere the field outside is the same as if all its mass were at its centre.', 'mass acts at centre [1]'),
        lambda r: ('Sketch-describe how g varies with distance r from the centre for r > R.', 'g decreases as 1/r²: a curve falling steeply then levelling towards zero, never reaching it.', 'decreasing curve [1]; inverse square / asymptotic to zero [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t22.add('C4', (2, 3, 4, 5), 'multi_step')(_ng_c4)

N23 = 'Gravitational potential φ = −GM/r and gravitational potential energy'
t23 = topic(N23, N23.lower(), 'gravitational potential', 'gravitational potential energy')
FX(t23, 'C1', (1, 2), [
    ('Which is the definition of gravitational potential at a point?', 'the work done per unit mass in bringing a small test mass from infinity to the point', 'φ = −GM/r; zero at infinity.', ['the force per unit mass at the point', 'the work done in moving a mass from the point to the surface', 'the energy per unit mass needed to orbit at the point']),
    ('Why is gravitational potential always negative?', 'The potential is zero at infinity and work is done by the field as a mass moves in from infinity', 'Gravity is attractive, so energy is released bringing a mass closer; potential decreases from zero.', ['Because mass can be negative', 'Because the field points outwards', 'Because potential energy is a vector']),
    ('What is the unit of gravitational potential?', 'J kg⁻¹', 'Work per unit mass.', ['N kg⁻¹', 'J', 'N m kg']),
    ('The gravitational potential at distance r from a planet is φ. What is it at distance 2r?', 'φ/2', 'φ ∝ −1/r.', ['φ/4', '2φ', '4φ']),
    ('What is the gravitational potential energy of a mass m at distance r from the centre of a planet of mass M?', '−GMm/r', 'Ep = mφ = −GMm/r.', ['−GMm/r²', 'GMm/r²', 'mgr']),
    ('The gradient of a graph of gravitational potential φ against distance r is equal to', 'minus the field strength (g = −dφ/dr)', 'Field strength is the negative of the potential gradient.', ['the field strength times r', 'the potential energy', 'the mass of the planet']),
    ('State the gravitational potential at infinity.', 'Zero.', 'zero [1]'),
])
FX(t23, 'C2', (1, 2, 3, 4), [
    ('Explain why the equation ΔEp = mgΔh can be used near the Earth\'s surface but not for a rocket travelling to a high orbit.', 'mgΔh assumes g is constant (uniform field); for large changes in height g decreases significantly, so ΔEp = GMm(1/r₁ − 1/r₂) must be used.', 'mgΔh assumes uniform g [1]; g varies over large distances, use −GMm/r [1] [2]'),
    ('Distinguish between gravitational potential and gravitational potential energy.', 'Potential is the work done per unit mass bringing a test mass from infinity (a property of the point, J kg⁻¹); potential energy is the work done for a particular mass m (J), Ep = mφ.', 'potential: per unit mass, property of the point [1]; PE: for a particular mass, Ep = mφ [1] [2]'),
    ('Explain, in terms of energy, the condition for a projectile to escape from the gravitational field of a planet.', 'Its kinetic energy at launch must be at least equal to the work needed to move it to infinity, ½mv² ≥ GMm/R, so its total energy is at least zero.', 'KE ≥ GMm/R [1]; reaches infinity with KE ≥ 0 / total energy ≥ 0 [1] [2]'),
    ('Explain why the gravitational potential energy of a satellite increases when it moves to a higher orbit, although the magnitude of GMm/r decreases.', 'Ep = −GMm/r; increasing r makes Ep less negative, i.e. larger; work must be done against gravity to raise it.', 'Ep negative [1]; less negative = increase [1] [2]'),
])


@t23.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_phi(r, D):
    nm, M, R = r.choice(PLANETS)
    phi = -GG * M / R
    if D <= 2:
        return numq(r, D, f'{cap(nm)} has mass {sc(M)} kg and radius {sc(R)} m.', f'gravitational potential at the surface of {nm}', phi, ' J kg⁻¹', f'φ = −GM/R = −6.67 × 10⁻¹¹ × {sc(M)}/{sc(R)}', [-phi, phi / R, phi * 2], fm=lambda x: sc(x, 3))
    m = r.choice([250, 500, 1200, 2500]); k = r.choice([1.0, 2.0, 3.0])
    r2 = R * (1 + k); dE = GG * M * m * (1 / R - 1 / r2)
    if D == 3:
        return Q(f'{cap(nm)} has mass {sc(M)} kg and radius {sc(R)} m. A satellite of mass {m} kg is raised from the surface to a height of {E(k * R)} m above it. Calculate the increase in its gravitational potential energy.', f'{sc(dE)} J',
                 f'ΔEp = GMm(1/r₁ − 1/r₂) [1]; r₂ = {E(r2)} m [1]; = {sc(dE)} J [1] [3]')
    vesc = math.sqrt(2 * GG * M / R)
    return Q(f'{cap(nm)} has mass {sc(M)} kg and radius {sc(R)} m. (a) Calculate the gravitational potential at the surface. (b) Calculate the escape speed from the surface. (c) Calculate the change in potential energy of a {m} kg probe moved from the surface to a distance {nf(1 + k)}R from the centre.',
             f'(a) {sc(phi)} J kg⁻¹ (b) {sc(vesc)} m s⁻¹ (c) +{sc(dE)} J', f'(a) φ = −GM/R = {sc(phi)} J kg⁻¹ [1] (b) ½v² = GM/R [1]; v = {sc(vesc)} m s⁻¹ [1] (c) ΔEp = m(φ₂ − φ₁) [1]; = {sc(dE)} J [1] [5]', 'multi_step')


@t23.add('C3', (2, 3, 4), 'numerical')
def t23_fall(r, D):
    nm, M, R = r.choice(PLANETS[:6])
    k = r.choice([0.5, 1.0, 1.5, 2.0])
    v = math.sqrt(2 * GG * M * (1 / R - 1 / (R * (1 + k))))
    return Q(f'A meteoroid is at rest relative to {nm} (mass {sc(M)} kg, radius {sc(R)} m) at a height of {E(k * R)} m above its surface. It falls towards {nm}. Ignoring any atmosphere, calculate its speed on reaching the surface.', f'{sc(v)} m s⁻¹',
             f'loss of PE = gain of KE: ½v² = GM(1/R − 1/r) [1]; r = {E(R * (1 + k))} m [1]; v = {sc(v)} m s⁻¹ [1]' + (' [3]' if D <= 3 else '; explanation why v ≠ √(2gh) because g not constant [1] [4]'))


def _gp_c4(r, D):
    nm, M, R = r.choice(PLANETS)
    phi = -GG * M / R
    intro = f'{cap(nm)} has mass {sc(M)} kg and radius {sc(R)} m.'
    parts = [
        lambda r: ('Define gravitational potential at a point.', 'Work done per unit mass in bringing a small test mass from infinity to the point.', 'work done per unit mass [1]; from infinity [1] [2]'),
        lambda r: ('Calculate the gravitational potential at the surface.', f'{sc(phi)} J kg⁻¹', 'φ = −GM/R [2]'),
        lambda r: ('Calculate the potential at a height R above the surface.', f'{sc(phi / 2)} J kg⁻¹', 'φ ∝ 1/r, r = 2R [1]'),
        lambda r: ('Calculate the minimum energy needed to move a 1.0 kg mass from the surface to infinity.', f'{sc(-phi)} J', 'ΔE = 0 − φ [1]'),
        lambda r: ('Calculate the escape speed from the surface.', f'{sc(math.sqrt(-2 * phi))} m s⁻¹', '½v² = GM/R [2]'),
        lambda r: ('Explain why the potential is negative.', 'Zero at infinity; attractive field does work as mass moves in, so potential is below zero.', 'zero at infinity and attractive [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t23.add('C4', (2, 3, 4, 5), 'multi_step')(_gp_c4)

N24 = 'Circular orbits and geostationary satellites'
t24 = topic(N24, N24.lower(), 'circular orbits', 'geostationary satellites')
FX(t24, 'C1', (1, 2), [
    ('Which is a property of a geostationary satellite?', 'It orbits above the equator with a period of 24 hours', 'It stays above one point: equatorial, west to east, T = 24 h.', ['It orbits over the poles every 24 hours', 'It is stationary relative to the Sun', 'It can be placed at any height above any point']),
    ('For satellites in circular orbits around the same planet, the square of the period T is proportional to', 'r³', 'GMm/r² = mω²r ⇒ T² = 4π²r³/(GM).', ['r²', 'r', '1/r²']),
    ('The orbital speed v of a satellite in a circular orbit of radius r around a planet of mass M is', '√(GM/r)', 'GMm/r² = mv²/r.', ['√(2GM/r)', 'GM/r', '√(GMr)']),
    ('A satellite moves to an orbit of larger radius. What happens to its orbital speed?', 'it decreases', 'v = √(GM/r).', ['it increases', 'it stays the same', 'it becomes zero']),
    ('In which direction does a geostationary satellite orbit?', 'from west to east, the same direction as the Earth rotates', 'It must turn with the Earth.', ['from east to west', 'from north to south', 'in either direction']),
    ('What provides the centripetal force on a satellite in a circular orbit?', 'the gravitational force of the planet', 'Gravity is the only force acting.', ['the rocket engines', 'a centrifugal force', 'the satellite\'s inertia']),
    ('State the period of a geostationary satellite.', '24 hours (one sidereal day, about 8.6 × 10⁴ s).', '24 h [1]'),
])
FX(t24, 'C2', (1, 2, 3, 4), [
    ('Show that for a satellite in a circular orbit T² = (4π²/GM) r³.', 'GMm/r² = mω²r with ω = 2π/T: GM/r² = 4π²r/T², so T² = 4π²r³/(GM).', 'gravitational force = centripetal force [1]; ω = 2π/T and rearrange [1] [2]'),
    ('Explain why a geostationary satellite must be above the equator.', 'The centripetal force (gravity) is directed towards the Earth\'s centre, so the orbit must be centred on the centre; to stay above one point while the Earth rotates, the orbit must lie in the equatorial plane.', 'orbit centred on Earth\'s centre [1]; only equatorial orbit stays above a fixed point [1] [2]'),
    ('Explain why astronauts in an orbiting space station feel weightless although gravity acts on them.', 'They and the station are both in free fall with the same acceleration towards the Earth; there is no contact force between astronaut and floor, which is what is sensed as weight.', 'both in free fall / same acceleration [1]; no normal contact force [1] [2]'),
    ('Explain why the orbital speed of a satellite does not depend on its mass.', 'GMm/r² = mv²/r; m cancels, so v = √(GM/r) depends only on M and r.', 'equate forces [1]; m cancels [1] [2]'),
    ('Suggest one advantage and one disadvantage of geostationary satellites for communications.', 'Advantage: stays above one point so dishes need no tracking / continuous coverage. Disadvantage: very high orbit gives a time delay and needs powerful signals; poor coverage near the poles.', 'advantage [1]; disadvantage [1] [2]'),
])


@t24.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_orbit(r, D):
    nm, M, R = r.choice(PLANETS)
    h = r.choice([0.1, 0.3, 0.5, 1.0, 2.0, 4.0]) * R
    rr = R + h; v = math.sqrt(GG * M / rr); T = 2 * PI * rr / v
    s = f'A satellite orbits {nm} (mass {sc(M)} kg, radius {sc(R)} m) in a circular orbit at a height of {E(h)} m above the surface.'
    if D <= 2:
        return numq(r, D, s, 'orbital speed', v, ' m s⁻¹', f'v = √(GM/r), r = {E(rr)} m', [math.sqrt(GG * M / h), math.sqrt(2 * GG * M / rr), v * 2], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the orbital speed and the period of the orbit.', f'v = {E(v)} m s⁻¹; T = {E(T)} s', f'r = R + h = {E(rr)} m [1]; v = √(GM/r) = {E(v)} m s⁻¹ [1]; T = 2πr/v = {E(T)} s [1] [3]')
    KE = 0.5 * 500 * v * v; PE = -GG * M * 500 / rr
    return Q(s + ' The satellite has mass 500 kg. (a) Calculate the orbital speed. (b) Calculate its kinetic energy and its gravitational potential energy. (c) Show that its total energy is equal to half of its gravitational potential energy.',
             f'(a) {E(v)} m s⁻¹ (b) KE = {sc(KE)} J; PE = {sc(PE)} J (c) total = {sc(KE + PE)} J = PE/2', f'(a) v = √(GM/r) = {E(v)} m s⁻¹ [1] (b) KE = ½mv² = {sc(KE)} J [1]; PE = −GMm/r = {sc(PE)} J [1] (c) KE = GMm/2r so total = −GMm/2r [1]; numerical check [1] [5]', 'multi_step')


@t24.add('C3', (2, 3, 4, 5), 'numerical')
def t24_geo(r, D):
    nm, M, R, Tday = r.choice([('Earth', 5.97e24, 6.37e6, 8.64e4), ('Mars', 6.42e23, 3.39e6, 8.86e4), ('Jupiter', 1.90e27, 6.99e7, 3.57e4)])
    rr = (GG * M * Tday ** 2 / (4 * PI ** 2)) ** (1 / 3)
    term = 'geostationary' if nm == 'Earth' else 'synchronous'
    if D <= 3:
        return Q(f'{cap(nm)} has mass {sc(M)} kg and rotates once every {E(Tday)} s. Calculate the radius of the orbit of a {term} satellite of {nm}.', f'{sc(rr)} m',
                 f'GMm/r² = m(2π/T)²r [1]; r³ = GMT²/4π² [1]; r = {sc(rr)} m [1] [3]')
    t_delay = 2 * (rr - R) / C0
    return Q(f'{cap(nm)} has mass {sc(M)} kg, radius {sc(R)} m and rotates once every {E(Tday)} s. (a) Calculate the orbital radius of a {term} satellite. (b) Calculate its height above the surface. (c) Calculate the minimum time for a radio signal to travel from the surface to the satellite and back.',
             f'(a) {sc(rr)} m (b) {sc(rr - R)} m (c) {f3(t_delay)} s', f'(a) r³ = GMT²/4π² [1]; r = {sc(rr)} m [1] (b) h = r − R = {sc(rr - R)} m [1] (c) t = 2h/c [1]; = {f3(t_delay)} s [1] [5]', 'multi_step')


@t24.add('C3', (2, 3, 4), 'numerical')
def t24_mass(r, D):
    host, moon, rr, T = r.choice([('Jupiter', 'Europa', 6.71e8, 3.07e5), ('Mars', 'Phobos', 9.38e6, 2.76e4), ('Saturn', 'Titan', 1.22e9, 1.38e6), ('the Earth', 'the Moon', 3.84e8, 2.36e6), ('the Sun', 'the Earth', 1.50e11, 3.16e7), ('Uranus', 'Titania', 4.36e8, 7.52e5)])
    M = 4 * PI ** 2 * rr ** 3 / (GG * T ** 2)
    return Q(f'{cap(moon)} orbits {host} in a near-circular orbit of radius {sc(rr)} m with a period of {sc(T)} s. Determine the mass of {host}.', f'{sc(M)} kg',
             f'GMm/r² = m(4π²/T²)r [1]; M = 4π²r³/(GT²) [1]; = {sc(M)} kg [1]' + (' [3]' if D <= 3 else '; statement that the mass of the moon cancels [1] [4]'))


def _orb_c4(r, D):
    nm, M, R = 'Earth', 5.97e24, 6.37e6
    h = r.choice([4.0e5, 8.0e5, 2.0e7]); rr = R + h
    v = math.sqrt(GG * M / rr); T = 2 * PI * rr / v
    intro = f'A satellite of mass {r.choice([450, 800, 1200])} kg is in a circular orbit {E(h)} m above the Earth (mass 5.97 × 10²⁴ kg, radius 6.37 × 10⁶ m).'
    parts = [
        lambda r: ('Show that the orbital speed is given by v = √(GM/r).', 'GMm/r² = mv²/r, so v² = GM/r.', 'equate gravitational and centripetal force [1]; rearrange [1] [2]'),
        lambda r: ('Calculate the orbital speed.', f'{E(v)} m s⁻¹', 'r = R + h, v = √(GM/r) [2]'),
        lambda r: ('Calculate the period in hours.', f'{f3(T / 3600)} h', 'T = 2πr/v [2]'),
        lambda r: ('State and explain whether this satellite could be geostationary.', 'No: its period is not 24 h (geostationary radius is 4.23 × 10⁷ m).' if abs(T - 86400) > 3600 else 'Possibly: its period is close to 24 h, if it orbits above the equator west to east.', 'compare T with 24 h [1]'),
        lambda r: ('Explain why the satellite does not need its engines to stay in orbit.', 'Gravity provides the centripetal force; no force is needed along the direction of motion (no resistance in vacuum).', 'gravity provides centripetal force [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t24.add('C4', (2, 3, 4, 5), 'multi_step')(_orb_c4)
CHAPTERS[2] = [t21, t22, t23, t24]

# ===================================================================== 3 Temperature
N31 = 'Thermal equilibrium and the thermodynamic (Kelvin) scale'
t31 = topic(N31, N31.lower(), 'thermal equilibrium', 'thermodynamic (kelvin) scale')
FX(t31, 'C1', (1, 2), [
    ('Two objects are in thermal equilibrium. Which statement is correct?', 'There is no net transfer of thermal energy between them', 'Thermal equilibrium means equal temperatures, so no net energy flow.', ['They have the same internal energy', 'They contain the same amount of thermal energy', 'They have the same specific heat capacity']),
    ('What is 27 °C on the thermodynamic temperature scale?', '300 K', 'T/K = θ/°C + 273.15 ≈ 300 K.', ['246 K', '27 K', '273 K']),
    ('What is absolute zero on the Celsius scale?', '−273.15 °C', '0 K = −273.15 °C.', ['0 °C', '−100 °C', '−373.15 °C']),
    ('A temperature rises from 20 °C to 50 °C. What is the rise in kelvin?', '30 K', 'A change of 1 °C equals a change of 1 K.', ['303 K', '323 K', '243 K']),
    ('Thermal energy is transferred between two objects in contact. Which property determines the direction of the net transfer?', 'temperature', 'Net energy flows from higher to lower temperature.', ['internal energy', 'mass', 'specific heat capacity']),
    ('Why is the thermodynamic scale described as an absolute scale?', 'It does not depend on the property of any particular substance', 'It is defined theoretically, with zero at absolute zero.', ['It can never have negative values for any substance', 'It uses the melting point of ice as its zero', 'It is the scale used by all thermometers']),
    ('What happens to the energy of the particles of a substance at absolute zero?', 'it is a minimum', 'At 0 K the internal energy is a minimum (not zero kinetic energy in quantum terms, but minimum).', ['it is a maximum', 'it equals the latent heat', 'it is equal to kT']),
    ('State the equation linking thermodynamic temperature T in kelvin and Celsius temperature θ.', 'T/K = θ/°C + 273.15', 'T = θ + 273.15 [1]'),
])
FX(t31, 'C2', (1, 2, 3, 4), [
    ('Explain what is meant by thermal equilibrium and why a thermometer must be in thermal equilibrium with an object to measure its temperature.', 'Thermal equilibrium: no net transfer of thermal energy between bodies in contact because they are at the same temperature. The thermometer reads its own temperature, which equals the object\'s only when there is no net energy flow.', 'no net energy transfer / same temperature [1]; thermometer reads own temperature, equal only at equilibrium [1] [2]'),
    ('Explain why temperature, not internal energy, determines the direction of thermal energy transfer.', 'A large cool object may have more internal energy than a small hot one, but energy still flows from hot to cold; net flow depends on temperature (mean random kinetic energy of particles), not total energy.', 'counter-example of large cool object [1]; flow from higher to lower temperature [1] [2]'),
    ('Explain why scales based on different thermometric properties may give different readings between the fixed points.', 'Each scale is defined to agree at the fixed points, but the properties (e.g. resistance, e.m.f., expansion) do not vary linearly in the same way with temperature, so readings in between can differ.', 'agree at fixed points by definition [1]; properties not linear in the same way [1] [2]'),
    ('State what is meant by absolute zero and explain why there is no temperature lower than it.', 'Absolute zero (0 K) is the temperature at which a substance has minimum internal energy; energy cannot be removed below the minimum, so no lower temperature exists.', 'minimum internal energy [1]; cannot be lower [1] [2]'),
])


@t31.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t31_conv(r, D):
    item = r.choice([('liquid nitrogen boils at', -196.0), ('a freezer is set to', -18.0), ('a sauna reaches', 85.0), ('the surface of Venus is about', 464.0), ('dry ice sublimes at', -78.5),
                     ('a pizza oven reaches', 450.0), ('liquid helium boils at', -268.9), ('human body temperature is about', 37.0), ('a winter night in Ulaanbaatar can fall to', -35.0), ('a car engine coolant runs at', 92.0)])
    txt, th = item
    T = round(th + 273.15, 2)
    if D <= 2:
        return numq(r, D, f'In a data book, {txt} {nf(th)} °C.', 'thermodynamic temperature', T, ' K', f'T = θ + 273.15 = {nf(th)} + 273.15', [th - 273.15, th + 273, -th + 273.15], fm=lambda x: nf(x, 4) if abs(x) >= 100 else nf(x, 3))
    th2 = th + r.choice([25.0, 40.0, 60.0, 120.0])
    T2 = round(th2 + 273.15, 2)
    return Q(f'In a data book, {txt} {nf(th)} °C. A sample at this temperature is warmed to {nf(th2)} °C. (a) Convert both temperatures to kelvin. (b) State the temperature rise in kelvin. (c) Calculate the ratio of the final to the initial thermodynamic temperature.' if D >= 4 else
             f'A sample is warmed from {nf(th)} °C to {nf(th2)} °C. Calculate the initial and final thermodynamic temperatures and the temperature rise in kelvin.',
             f'(a) {nf(T, 4)} K and {nf(T2, 4)} K (b) {nf(th2 - th)} K (c) {f3(T2 / T)}' if D >= 4 else f'{nf(T, 4)} K, {nf(T2, 4)} K; rise {nf(th2 - th)} K',
             (f'(a) add 273.15 [1]; both values [1] (b) {nf(th2 - th)} K [1] (c) ratio uses kelvin values = {f3(T2 / T)} [1] [4]' if D >= 4 else f'add 273.15 [1]; {nf(T, 4)} K and {nf(T2, 4)} K [1]; rise {nf(th2 - th)} K [1] [3]'), 'multi_step' if D >= 4 else None)


@t31.add('C2', (2, 3, 4), 'explain')
def t31_contact(r, D):
    a, b = r.choice([('a 2 kg iron block at 80 °C', 'a 50 kg tank of water at 30 °C'), ('a cup of tea at 70 °C', 'a swimming pool at 26 °C'), ('a hot rivet at 400 °C', 'a large steel girder at 20 °C'), ('a small copper coin at 60 °C', 'a bucket of sand at 25 °C')])
    return Q(f'{cap(a)} is placed in contact with {b}. A student says thermal energy will flow into the hotter object because the other has more internal energy. Explain why the student is wrong and describe what happens until thermal equilibrium is reached.',
             f'Net thermal energy flows from higher to lower temperature, i.e. from {a} to {b}, regardless of internal energy, until both reach the same temperature, after which there is no net transfer.',
             'direction set by temperature not internal energy [1]; flow from hotter to colder [1]' + ('; continues until same temperature, then no net transfer [1] [3]' if D >= 3 else ' [2]'))


def _temp_c4(r, D):
    th = r.choice([-40.0, -12.0, 15.0, 35.0, 60.0])
    intro = ctx(r, ['{p} compares two thermometers in a laboratory in {c}.', 'A weather station in {c} records temperatures on both scales.', 'A technician in {c} calibrates a freezer thermometer.'])
    parts = [
        lambda r: ('State what is meant by thermal equilibrium.', 'No net transfer of thermal energy between two bodies (they are at the same temperature).', 'no net energy transfer [1]'),
        lambda r: (f'Convert {nf(th)} °C to kelvin.', f'{nf(th + 273.15, 4)} K', 'T = θ + 273.15 [1]'),
        lambda r: ('Explain why the thermodynamic scale is called an absolute scale.', 'It does not depend on the property of any substance and its zero is absolute zero.', 'independent of substance [1]; zero at absolute zero [1] [2]'),
        lambda r: ('State the significance of the temperature 0 K.', 'Absolute zero: the internal energy of a substance is a minimum.', 'minimum internal energy [1]'),
        lambda r: ('Explain why a temperature change of 10 °C equals a change of 10 K.', 'The kelvin and the degree Celsius are the same size; the scales only differ in their zero.', 'same size of degree [1]; offset of 273.15 [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t31.add('C4', (2, 3, 4, 5), 'multi_step')(_temp_c4)

N32 = 'Thermometers and physical properties that vary with temperature'
t32 = topic(N32, N32.lower(), 'thermometers', 'physical properties that vary with temperature')
FX(t32, 'C1', (1, 2), [
    ('Which physical property is used in a thermocouple thermometer?', 'the e.m.f. produced at a junction of two different metals', 'A thermocouple e.m.f. depends on the temperature difference between junctions.', ['the resistance of a semiconductor', 'the expansion of a liquid', 'the pressure of a fixed volume of gas']),
    ('What is an advantage of a thermocouple compared with a liquid-in-glass thermometer?', 'it has a small heat capacity and responds quickly', 'Small junction: fast response, wide range, remote reading.', ['it has a perfectly linear scale', 'it needs no voltmeter', 'it is accurate only near room temperature']),
    ('The resistance of an NTC thermistor', 'decreases as temperature increases', 'More charge carriers are released as temperature rises.', ['increases as temperature increases', 'does not change with temperature', 'increases linearly with temperature']),
    ('Which thermometer is most suitable for measuring the temperature of a small, rapidly changing object at 900 °C?', 'a thermocouple', 'Wide range and fast response.', ['a mercury-in-glass thermometer', 'an NTC thermistor', 'an alcohol-in-glass thermometer']),
    ('Which property makes a quantity suitable as a thermometric property?', 'it varies continuously and measurably with temperature', 'It must change by a measurable, reproducible amount with temperature.', ['it stays constant as temperature changes', 'it depends only on mass', 'it only changes at the melting point']),
    ('An advantage of a thermistor thermometer over a thermocouple is that it is', 'very sensitive over a small temperature range', 'Large change of resistance per kelvin near room temperature.', ['usable up to 1500 °C', 'perfectly linear', 'not affected by temperature']),
    ('State two physical properties that vary with temperature and could be used in a thermometer.', 'e.g. resistance of a thermistor or metal wire; e.m.f. of a thermocouple; volume of a liquid; pressure of a gas at constant volume.', 'any two [2]'),
])
FX(t32, 'C2', (1, 2, 3, 4), [
    ('Compare a thermistor and a thermocouple as thermometers for monitoring the temperature of a kiln and of a baby\'s bath.', 'Kiln: thermocouple, because of its very wide range (hundreds of °C) and robustness. Bath: thermistor, because it is very sensitive over a narrow range near 37 °C.', 'thermocouple for kiln with reason (range) [1]; thermistor for bath with reason (sensitivity) [1] [2]'),
    ('Explain why a thermistor thermometer and a resistance-wire thermometer, both calibrated at 0 °C and 100 °C, may disagree at 50 °C.', 'Each reading assumes resistance varies linearly between fixed points; the thermistor\'s resistance varies non-linearly (roughly exponentially) and differently from the metal\'s, so interpolated values differ.', 'scales agree only at fixed points [1]; non-linear/different variation [1] [2]'),
    ('Explain why a thermocouple can measure the temperature at a point.', 'The junction is very small, so it has a low heat capacity and measures the temperature at that point quickly without disturbing it much.', 'small junction [1]; low heat capacity / quick response [1] [2]'),
    ('Suggest why the e.m.f. of a thermocouple must be measured with a high-resistance voltmeter.', 'Thermocouple e.m.f.s are small (millivolts) and the source may have internal resistance; a high-resistance meter draws little current, so the p.d. measured is close to the e.m.f.', 'small e.m.f. [1]; little current drawn so reading ≈ e.m.f. [1] [2]'),
])

PROPS = [('resistance of a platinum wire', 'R', 'Ω', (100.0, 138.5), (100.0, 115.0, 121.0, 130.0)), ('e.m.f. of a thermocouple (one junction in melting ice)', 'E', 'mV', (0.0, 4.1), (1.2, 1.8, 2.6, 3.3)),
         ('length of a liquid thread in a capillary', 'l', 'mm', (25.0, 205.0), (62.0, 88.0, 130.0, 170.0)), ('pressure of a constant-volume gas', 'p', 'kPa', (101.3, 138.4), (110.0, 120.0, 127.0, 133.0)),
         ('resistance of a metal-film sensor', 'R', 'Ω', (500.0, 690.0), (540.0, 575.0, 610.0, 650.0))]


@t32.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t32_scale(r, D):
    nm, sym, u, (x0, x100), xs = r.choice(PROPS)
    x = r.choice(xs)
    th = (x - x0) / (x100 - x0) * 100
    who = person(r)
    s = f'{who} uses the {nm} as a thermometric property. Its value is {nf(x0, 4)} {u} at 0 °C and {nf(x100, 4)} {u} at 100 °C. At an unknown temperature it is {nf(x, 4)} {u}.'
    if D <= 2:
        return numq(r, D, s, 'unknown temperature on this scale', th, ' °C', f'θ = ({nf(x, 4)} − {nf(x0, 4)})/({nf(x100, 4)} − {nf(x0, 4)}) × 100', [x / x100 * 100, (x100 - x) / (x100 - x0) * 100, th + 273], fm=lambda v: nf(v, 3))
    if D == 3:
        return Q(s + ' Calculate the unknown temperature on this scale and state the assumption made.', f'{nf(th, 3)} °C; assumes {sym} varies linearly with temperature',
                 f'θ = ({sym} − {sym}₀)/({sym}₁₀₀ − {sym}₀) × 100 [1]; = {nf(th, 3)} °C [1]; linear variation assumed [1] [3]')
    return Q(s + ' (a) Calculate the unknown temperature on this scale. (b) Convert it to kelvin. (c) A gas thermometer gives a slightly different reading at this temperature. Explain why.',
             f'(a) {nf(th, 3)} °C (b) {nf(th + 273.15, 4)} K (c) the two properties do not vary linearly with temperature in the same way; scales only agree at the fixed points',
             f'(a) ratio method [1]; {nf(th, 3)} °C [1] (b) + 273.15 = {nf(th + 273.15, 4)} K [1] (c) non-linear/different variation [1]; agree only at fixed points [1] [5]', 'multi_step')


@t32.add('C2', (2, 3, 4), 'explain')
def t32_choose(r, D):
    job, best, why = r.choice([('the temperature of molten steel in a foundry', 'thermocouple', 'very wide range up to well over 1000 °C and robust'),
                               ('small changes in skin temperature during exercise', 'thermistor', 'very sensitive over a narrow range near body temperature'),
                               ('the temperature inside a car engine at many points, recorded by a computer', 'thermocouple', 'small junctions with fast response and an electrical output that can be logged'),
                               ('the air temperature in a greenhouse, read by a data-logger', 'thermistor', 'large change of resistance per kelvin in this range, easily used in a potential divider'),
                               ('the temperature of a thin wire which heats up in a fraction of a second', 'thermocouple', 'tiny junction with low heat capacity responds very quickly')])
    return Q(f'Suggest, with reasons, whether a thermistor or a thermocouple is more suitable for measuring {job}.', f'A {best}: {why}.',
             f'{best} chosen [1]; reason: {why} [1]' + ('; comment on a limitation of the other type [1] [3]' if D >= 3 else ' [2]'))


def _thermo_c4(r, D):
    x0, x100, x = r.choice([(2.8, 1.1, 1.8), (5.0, 0.35, 1.2), (3.5, 0.60, 1.5)])
    th = (x - x0) / (x100 - x0) * 100
    intro = f'A thermistor has a resistance of {nf(x0)} kΩ at 0 °C and {nf(x100)} kΩ at 100 °C. When placed in a liquid its resistance is {nf(x)} kΩ.'
    parts = [
        lambda r: ('State what type of thermistor this is and explain how you know.', 'NTC: resistance decreases as temperature increases.', 'NTC with reason [1]'),
        lambda r: ('Assuming the resistance varies linearly with temperature, calculate the temperature of the liquid.', f'{nf(th, 3)} °C', '(R − R₀)/(R₁₀₀ − R₀) × 100 [2]'),
        lambda r: ('Explain why the true temperature may differ from this value.', 'Thermistor resistance does not vary linearly with temperature (it is roughly exponential).', 'non-linear variation [1]'),
        lambda r: ('State one advantage of a thermistor over a thermocouple.', 'More sensitive (large change of R per kelvin) over a small range.', 'sensitivity [1]'),
        lambda r: ('State one advantage of a thermocouple over a thermistor.', 'Much wider range / smaller with faster response / measures at a point.', 'valid advantage [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t32.add('C4', (2, 3, 4, 5), 'multi_step')(_thermo_c4)

N33 = 'Specific heat capacity and specific latent heat including electrical methods'
t33 = topic(N33, N33.lower(), 'specific heat capacity', 'specific latent heat')
FX(t33, 'C1', (1, 2), [
    ('Which is the definition of specific heat capacity?', 'the energy required per unit mass to raise the temperature by one kelvin', 'c = E/(mΔθ).', ['the energy required to raise the temperature of an object by 1 K', 'the energy required per unit mass to change state', 'the energy stored per kelvin in an object']),
    ('What is the unit of specific latent heat?', 'J kg⁻¹', 'L = E/m.', ['J kg⁻¹ K⁻¹', 'J K⁻¹', 'W kg⁻¹']),
    ('How much energy is needed to raise the temperature of 2.0 kg of water by 15 K? (c = 4200 J kg⁻¹ K⁻¹)', '1.26 × 10⁵ J', 'E = mcΔθ = 2.0 × 4200 × 15.', ['6.3 × 10⁴ J', '1.26 × 10⁴ J', '8.4 × 10³ J']),
    ('During melting at constant temperature, the energy supplied mainly', 'increases the potential energy of the molecules', 'Bonds are broken; mean kinetic energy stays constant.', ['increases the kinetic energy of the molecules', 'is lost to the surroundings', 'increases the temperature of the solid']),
    ('Why is the specific latent heat of vaporisation of water much greater than its specific latent heat of fusion?', 'More bonds must be broken and work must be done pushing back the atmosphere', 'On boiling molecules separate completely and the volume increases greatly.', ['The temperature of steam is higher', 'Ice has a lower density than water', 'Water has a high specific heat capacity']),
    ('A 2.0 kW heater melts 0.30 kg of ice at 0 °C in 50 s. What value does this give for the specific latent heat of fusion?', '3.3 × 10⁵ J kg⁻¹', 'L = Pt/m = 2000 × 50/0.30.', ['3.0 × 10⁴ J kg⁻¹', '1.2 × 10⁵ J kg⁻¹', '3.3 × 10⁸ J kg⁻¹']),
    ('Define specific latent heat of vaporisation.', 'The energy required per unit mass to change a substance from liquid to gas without a change of temperature.', 'energy per unit mass [1]; liquid to gas at constant temperature [1] [2]'),
])
FX(t33, 'C2', (1, 2, 3, 4), [
    ('Explain why a block of metal being heated electrically should be well insulated when measuring its specific heat capacity.', 'Thermal energy is lost to the surroundings, so not all the electrical energy VIt raises the temperature; the value of c calculated would be too large. Insulation reduces these losses.', 'energy lost to surroundings [1]; calculated c too high, insulation reduces losses [1] [2]'),
    ('Explain, in terms of molecules, why the temperature of a substance stays constant while it boils.', 'The energy supplied is used to break intermolecular bonds and separate the molecules (increase in potential energy) and do work against the atmosphere; the mean kinetic energy, and hence temperature, does not change.', 'energy breaks bonds / increases PE [1]; mean KE (temperature) unchanged [1] [2]'),
    ('Explain how using two different heater powers allows energy losses to be eliminated when measuring specific latent heat of vaporisation.', 'With the liquid boiling steadily at the same temperature, the rate of heat loss h is the same in both runs: P₁t = m₁L + ht and P₂t = m₂L + ht. Subtracting eliminates h: L = (P₁ − P₂)t/(m₁ − m₂).', 'heat loss rate same in both runs (same temperature) [1]; subtract equations to eliminate loss [1] [2]'),
    ('Explain why a heater should be left on for several minutes before readings are taken in a latent heat experiment.', 'The apparatus must reach a steady state (boiling steadily, constant temperature), so that the rate of energy loss is constant and all supplied energy goes into the change of state plus a steady loss.', 'steady state reached [1]; constant loss rate [1] [2]'),
])
MATS = [('copper', 385), ('aluminium', 900), ('iron', 450), ('brass', 380), ('lead', 130), ('water', 4200), ('oil', 2000), ('glass', 670), ('concrete', 880)]


@t33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t33_elec(r, D):
    mat, c = r.choice(MATS)
    m = r.choice([0.50, 0.80, 1.0, 1.2, 2.0]); V = r.choice([12.0, 12.0, 24.0]); I = r.choice([2.5, 3.0, 4.0, 4.5, 5.0])
    t = r.choice([180, 240, 300, 420, 600])
    dth = V * I * t / (m * c)
    if dth > 80 or dth < 2:
        return None
    s = f'An electrical heater connected to a {nf(V)} V supply passes a current of {nf(I)} A. It heats a {nf(m)} kg {"sample" if mat in ("water", "oil") else "block"} of {mat} for {t} s, and the temperature rises by {nf(dth, 3)} K. Energy losses are negligible.'
    cc = V * I * t / (m * dth)
    if D <= 2:
        return numq(r, D, s, f'specific heat capacity of {mat}', cc, ' J kg⁻¹ K⁻¹', f'c = VIt/(mΔθ) = {nf(V)} × {nf(I)} × {t}/({nf(m)} × {nf(dth, 3)})', [V * I / (m * dth), cc * 1000, cc / 2], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + f' Calculate the energy supplied and the specific heat capacity of {mat}.', f'E = {E(V * I * t)} J; c = {nf(cc, 3)} J kg⁻¹ K⁻¹',
                 f'E = VIt = {E(V * I * t)} J [1]; c = E/(mΔθ) [1]; = {nf(cc, 3)} J kg⁻¹ K⁻¹ [1] [3]')
    loss = r.choice([10, 15, 20])
    return Q(s.replace(' Energy losses are negligible.', '') + f' (a) Calculate the energy supplied by the heater. (b) Calculate a value for the specific heat capacity, assuming no losses. (c) In fact {loss}% of the energy is lost to the surroundings. Calculate the corrected value and explain whether the first value was too high or too low.',
             f'(a) {E(V * I * t)} J (b) {nf(cc, 3)} J kg⁻¹ K⁻¹ (c) {nf(cc * (1 - loss / 100), 3)} J kg⁻¹ K⁻¹; the first value was too high because not all of the energy heated the {mat}',
             f'(a) E = VIt = {E(V * I * t)} J [1] (b) c = E/(mΔθ) = {nf(cc, 3)} J kg⁻¹ K⁻¹ [1] (c) useful energy = {100 - loss}% [1]; c = {nf(cc * (1 - loss / 100), 3)} J kg⁻¹ K⁻¹ [1]; too high, explanation [1] [5]', 'multi_step')


@t33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t33_latent(r, D):
    kind = r.choice(['fus', 'vap'])
    if kind == 'fus':
        L = 3.34e5; P = r.choice([60.0, 100.0, 150.0, 250.0]); m = r.choice([0.040, 0.060, 0.080, 0.12, 0.15]); what = 'ice at 0 °C melts'; ph = 'fusion'
    else:
        L = 2.26e6; P = r.choice([500.0, 800.0, 1000.0, 1500.0]); m = r.choice([0.050, 0.080, 0.10, 0.15]); what = 'water at 100 °C boils away'; ph = 'vaporisation'
    t = L * m / P
    s = f'A heater of power {nf(P)} W is used in a {city(r)} school laboratory. When {what}, a mass of {nf(m)} kg changes state in {nf(t, 3)} s. Energy losses are negligible.'
    if D <= 3:
        return numq(r, D, s, f'specific latent heat of {ph} of water', L, ' J kg⁻¹', f'L = Pt/m = {nf(P)} × {nf(t, 3)}/{nf(m)}', [P * t, P / m, L / 1000], fm=lambda x: sc(x, 3))
    P2 = P * r.choice([0.5, 0.6, 0.75]); h = r.choice([5.0, 8.0, 12.0])
    T = r.choice([300, 400, 600])
    m1 = (P - h) * T / L; m2 = (P2 - h) * T / L
    return Q(f'In a two-power experiment, water is kept boiling by a heater. With the heater at {nf(P)} W, {nf(m1, 3)} kg of water boils away in {T} s; at {nf(P2, 3)} W, {nf(m2, 3)} kg boils away in the same time. (a) Calculate the specific latent heat of vaporisation. (b) Calculate the rate of energy loss to the surroundings. (c) Explain why the rate of loss is the same in both runs.' if kind == 'vap' else
             f'In a two-power experiment, ice at 0 °C is melted by a heater in a funnel. With the heater at {nf(P)} W, {nf(m1, 3)} kg of water drips out in {T} s; at {nf(P2, 3)} W, {nf(m2, 3)} kg drips out in the same time. (a) Calculate the specific latent heat of fusion. (b) Calculate the rate of energy gain or loss to the surroundings. (c) Explain why this rate is the same in both runs.',
             f'(a) {sc(L)} J kg⁻¹ (b) {nf(h, 3)} W (c) same temperature (state change) in both runs, so same temperature difference with surroundings',
             f'(a) (P₁ − P₂)t = (m₁ − m₂)L [1]; L = {sc(L)} J kg⁻¹ [1] (b) P₁t = m₁L + ht [1]; h = {nf(h, 3)} W [1] (c) same temperature so same loss rate [1] [5]', 'multi_step')


@t33.add('C3', (3, 4, 5), 'numerical')
def t33_mix(r, D):
    mi = r.choice([0.020, 0.030, 0.040, 0.050]); mw = r.choice([0.20, 0.25, 0.30, 0.40]); tw = r.choice([30.0, 40.0, 50.0, 60.0])
    L, c = 3.34e5, 4200.0
    T = (mw * c * tw - mi * L) / ((mw + mi) * c)
    if T <= 1:
        return None
    return Q(f'{person(r)} drops {nf(mi * 1000)} g of ice at 0 °C into {nf(mw * 1000)} g of water at {nf(tw)} °C in an insulated cup of negligible heat capacity. Calculate the final temperature after all the ice has melted. (specific heat capacity of water 4200 J kg⁻¹ K⁻¹; specific latent heat of fusion of ice 3.34 × 10⁵ J kg⁻¹)',
             f'{nf(T, 3)} °C', f'energy to melt ice = mL = {E(mi * L)} J [1]; m_w c({nf(tw)} − T) = m_i L + m_i c T [1]; T = {nf(T, 3)} °C [1]' + (' [3]' if D == 3 else '; check that all the ice melts (energy available > mL) [1] [4]'))


def _shc_c4(r, D):
    mat, c = r.choice(MATS[:5])
    m = r.choice([1.0, 2.0]); P = r.choice([40.0, 50.0, 60.0])
    rate = P / (m * c) * 60
    intro = f'A {nf(m)} kg block of {mat} is heated by a {nf(P)} W heater inserted in a hole in the block. A thermometer is placed in a second hole.'
    parts = [
        lambda r: ('Define specific heat capacity.', 'Energy per unit mass needed to raise the temperature by 1 K.', 'energy per unit mass per kelvin [1]'),
        lambda r: (f'The specific heat capacity of {mat} is {c} J kg⁻¹ K⁻¹. Calculate the rate of rise of temperature in K per minute, assuming no losses.', f'{nf(rate, 3)} K min⁻¹', 'Δθ/t = P/(mc) × 60 [2]'),
        lambda r: ('Describe how the heater power would be measured.', 'Ammeter in series and voltmeter in parallel with the heater; P = VI.', 'ammeter and voltmeter [1]; P = VI [1] [2]'),
        lambda r: ('Suggest why a little oil is put in the thermometer hole.', 'To improve thermal contact between block and thermometer.', 'thermal contact [1]'),
        lambda r: ('Explain why the measured rate of temperature rise is less than the calculated value.', 'Energy is lost to the surroundings and used to heat the heater and thermometer.', 'losses to surroundings [1]'),
        lambda r: ('Explain why the temperature continues to rise briefly after the heater is switched off.', 'The heater is hotter than the block and continues to transfer energy to it.', 'heater hotter than block [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t33.add('C4', (2, 3, 4, 5), 'multi_step')(_shc_c4)
CHAPTERS[3] = [t31, t32, t33]

# ===================================================================== 4 Ideal gases
GASES = [('helium', 4.0e-3), ('neon', 20.2e-3), ('argon', 39.9e-3), ('nitrogen', 28.0e-3), ('oxygen', 32.0e-3), ('carbon dioxide', 44.0e-3), ('hydrogen', 2.0e-3), ('xenon', 131e-3)]

N41 = 'The mole, Avogadro constant and the ideal gas equation pV = nRT'
t41 = topic(N41, N41.lower(), 'the mole', 'ideal gas equation')
FX(t41, 'C1', (1, 2), [
    ('What is the Avogadro constant?', 'the number of particles in one mole of a substance', 'N_A = 6.02 × 10²³ mol⁻¹.', ['the mass of one mole of a substance', 'the volume of one mole of gas at s.t.p.', 'the number of atoms in 1 kg of carbon-12']),
    ('How many molecules are there in 0.50 mol of oxygen?', '3.0 × 10²³', 'N = nN_A = 0.50 × 6.02 × 10²³.', ['1.2 × 10²⁴', '6.0 × 10²³', '1.6 × 10⁻²⁴']),
    ('In the ideal gas equation pV = nRT, what is T?', 'the thermodynamic temperature in kelvin', 'T must be in kelvin.', ['the Celsius temperature', 'the temperature change', 'the time']),
    ('A fixed mass of ideal gas has its thermodynamic temperature doubled at constant volume. What happens to the pressure?', 'it doubles', 'p ∝ T at constant V and n.', ['it halves', 'it stays the same', 'it increases by a factor of 4']),
    ('What is the unit of the molar gas constant R?', 'J K⁻¹ mol⁻¹', 'R = pV/(nT).', ['J mol⁻¹', 'J K⁻¹', 'K mol J⁻¹']),
    ('Which equation relates the Boltzmann constant k, molar gas constant R and Avogadro constant N_A?', 'k = R/N_A', 'pV = nRT = NkT with N = nN_A.', ['k = RN_A', 'R = k/N_A', 'k = N_A/R']),
    ('An ideal gas is a gas that', 'obeys pV ∝ T at all pressures, volumes and temperatures', 'Ideal gases obey pV = nRT exactly.', ['has molecules that never collide', 'has no mass', 'only exists at very low temperatures']),
    ('State what is meant by one mole.', 'The amount of substance containing 6.02 × 10²³ particles (as many as there are atoms in 12 g of carbon-12).', 'N_A particles [1]'),
])
FX(t41, 'C2', (1, 2, 3, 4), [
    ('Explain why real gases deviate from ideal gas behaviour at high pressures and low temperatures.', 'At high pressure the molecules are close together so their volume is not negligible; at low temperature they move slowly so intermolecular attractions become significant. Both assumptions of the ideal gas model fail.', 'molecular volume significant at high p [1]; intermolecular forces significant at low T [1] [2]'),
    ('Show that pV = nRT can be written as pV = NkT.', 'N = nN_A so n = N/N_A; pV = (N/N_A)RT = N(R/N_A)T = NkT.', 'n = N/N_A [1]; k = R/N_A [1] [2]'),
    ('Explain why the temperature in the ideal gas equation must be in kelvin.', 'pV is proportional to the thermodynamic temperature, which is zero at absolute zero; using °C would give nonsensical results (e.g. zero or negative pV at 0 °C).', 'p ∝ T only on absolute scale [1]; °C gives wrong/negative values [1] [2]'),
    ('A sealed rigid container of gas is heated. Explain why the pressure rises, using the ideal gas equation.', 'n and V are constant, so p ∝ T: as T increases, p increases in proportion.', 'n, V constant [1]; p ∝ T [1] [2]'),
])
relation(t41, 'C2', (2, 3), 'pV = nRT', 'pressure of the gas', {'thermodynamic temperature': 1, 'volume': -1, 'amount of gas': 1},
         ['A fixed container holds an ideal gas.', 'An ideal gas is trapped in a cylinder by a piston.', 'A sealed balloon of ideal gas is studied.'])


@t41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t41_pvnrt(r, D):
    gas, Mm = r.choice(GASES)
    V = r.choice([2.0e-3, 5.0e-3, 0.012, 0.025, 0.050]); th = r.choice([15.0, 20.0, 27.0, 35.0, -10.0, 80.0]); p = r.choice([1.0e5, 1.5e5, 2.0e5, 3.5e5, 1.2e6])
    T = th + 273.0
    n = p * V / (RG * T); N = n * NA; m = n * Mm
    s = f'A cylinder of volume {sc(V)} m³ contains {gas} at a pressure of {sc(p)} Pa and a temperature of {nf(th)} °C.'
    if D <= 2:
        return numq(r, D, s, 'amount of gas in moles', n, ' mol', f'n = pV/(RT) = {sc(p)} × {sc(V)}/(8.31 × {nf(T)})', [p * V / (RG * th), n * NA, n * 1000], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the number of moles and the number of molecules of gas.', f'n = {E(n)} mol; N = {sc(N)}', f'T = {nf(T)} K [1]; n = pV/RT = {E(n)} mol [1]; N = nN_A = {sc(N)} [1] [3]')
    return Q(s + f' The molar mass of {gas} is {nf(Mm * 1000, 3)} g mol⁻¹. (a) Calculate the amount of gas in moles. (b) Calculate the mass of gas. (c) Calculate the density of the gas.',
             f'(a) {E(n)} mol (b) {E(m)} kg (c) {E(m / V)} kg m⁻³', f'(a) T in K [1]; n = pV/RT = {E(n)} mol [1] (b) m = n × M = {E(m)} kg [1] (c) ρ = m/V [1]; = {E(m / V)} kg m⁻³ [1] [5]', 'multi_step')


@t41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t41_change(r, D):
    sc_ = r.choice(['tyre', 'balloon', 'syringe', 'aerosol', 'bubble'])
    if sc_ == 'tyre':
        p1 = r.choice([2.2e5, 2.4e5, 2.8e5]); t1 = r.choice([5.0, 10.0, 15.0]); t2 = r.choice([35.0, 40.0, 45.0]); V1 = V2 = 1.0
        txt = f'A car tyre in {city(r)} contains air at {sc(p1)} Pa at {nf(t1)} °C. After a long drive the air is at {nf(t2)} °C. Assume the volume of the tyre is constant.'
        p2 = p1 * (t2 + 273) / (t1 + 273); qty, val, unit = 'new pressure', p2, ' Pa'
        wk = f'p₂ = p₁T₂/T₁ = {sc(p1)} × {nf(t2 + 273)}/{nf(t1 + 273)}'
    elif sc_ == 'balloon':
        V1 = r.choice([0.020, 0.040, 0.060]); t1 = r.choice([20.0, 25.0]); t2 = r.choice([-10.0, -20.0, -30.0]); p1 = 1.0e5; p2r = r.choice([0.60, 0.70, 0.80])
        txt = f'A weather balloon contains {nf(V1)} m³ of helium at {nf(t1)} °C and 1.0 × 10⁵ Pa. It rises to where the pressure is {nf(p2r * 1e5 / 1e4)} × 10⁴ Pa and the temperature is {nf(t2)} °C.'
        val = V1 * (1e5 / (p2r * 1e5)) * (t2 + 273) / (t1 + 273); qty, unit = 'new volume', ' m³'
        wk = f'V₂ = V₁(p₁/p₂)(T₂/T₁) = {nf(V1)} × (1.0 × 10⁵/{nf(p2r * 10)} × 10⁴) × ({nf(t2 + 273)}/{nf(t1 + 273)})'
    elif sc_ == 'syringe':
        V1 = r.choice([40.0, 50.0, 60.0]); V2 = r.choice([15.0, 20.0, 25.0]); p1 = 1.0e5
        txt = f'Air in a sealed syringe occupies {nf(V1)} cm³ at 1.0 × 10⁵ Pa. The plunger is pushed in slowly, at constant temperature, until the volume is {nf(V2)} cm³.'
        val = p1 * V1 / V2; qty, unit = 'new pressure', ' Pa'; wk = f'p₂ = p₁V₁/V₂ = 1.0 × 10⁵ × {nf(V1)}/{nf(V2)}'
    elif sc_ == 'aerosol':
        p1 = r.choice([3.0e5, 4.0e5, 5.0e5]); t1 = 20.0; t2 = r.choice([300.0, 400.0, 500.0])
        txt = f'An aerosol can contains gas at {sc(p1)} Pa at 20 °C. It is thrown onto a bonfire and heated to {nf(t2)} °C.'
        val = p1 * (t2 + 273) / 293; qty, unit = 'pressure at this temperature', ' Pa'; wk = f'p₂ = p₁T₂/T₁ = {sc(p1)} × {nf(t2 + 273)}/293'
    else:
        d = r.choice([10.0, 20.0, 30.0]); V1 = r.choice([2.0, 3.0, 5.0])
        p1 = 1.0e5 + 1000 * GR * d
        txt = f'A bubble of volume {nf(V1)} cm³ is released by a diver at a depth of {nf(d)} m in a lake, where the pressure is {sc(p1)} Pa. It rises to the surface (pressure 1.0 × 10⁵ Pa) at constant temperature.'
        val = V1 * p1 / 1e5; qty, unit = 'volume at the surface', ' cm³'; wk = f'V₂ = p₁V₁/p₂ = {sc(p1)} × {nf(V1)}/1.0 × 10⁵'
    fm = (lambda x: sc(x, 3)) if unit == ' Pa' else f3
    more = ('State two assumptions made in this calculation.', 'the gas is ideal; the amount (mass) of gas is constant (no leaks)', 'ideal gas [1]; fixed amount of gas [1]', 2)
    return calc(r, D, txt, qty, val, unit, wk, [val * 2, val / 2, val * 1.1], fm=fm, more=more)


def _gas_c4(r, D):
    gas, Mm = r.choice(GASES[:6])
    V = r.choice([0.010, 0.020, 0.050]); p = r.choice([2.0e5, 5.0e6, 1.0e7]); th = 20.0; T = 293.0
    n = p * V / (RG * T)
    intro = f'A steel gas cylinder of internal volume {nf(V)} m³ contains {gas} (molar mass {nf(Mm * 1000, 3)} g mol⁻¹) at {sc(p)} Pa and 20 °C.'
    parts = [
        lambda r: ('State what is meant by an ideal gas.', 'A gas that obeys pV ∝ T (pV = nRT) at all pressures, volumes and temperatures.', 'pV ∝ T [1]; at all p, V, T [1] [2]'),
        lambda r: ('Calculate the amount of gas in the cylinder.', f'{E(n)} mol', 'n = pV/RT [2]'),
        lambda r: ('Calculate the number of molecules in the cylinder.', f'{sc(n * NA)}', 'N = nN_A [1]'),
        lambda r: ('Calculate the mass of gas.', f'{E(n * Mm)} kg', 'm = nM [1]'),
        lambda r: (f'The cylinder is left in the sun and warms to 45 °C. Calculate the new pressure.', f'{sc(p * 318 / 293)} Pa', 'p ∝ T [2]'),
        lambda r: ('Suggest why the gas may not behave ideally in this cylinder.', 'At high pressure the molecules are close together, so their volume and intermolecular forces are not negligible.' if p > 1e6 else 'Near-ideal at this pressure; deviation would be small.', 'reference to high pressure / molecular volume or forces [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t41.add('C4', (2, 3, 4, 5), 'multi_step')(_gas_c4)

N42 = 'Kinetic theory of gases: assumptions and pV = ⅓Nm⟨c²⟩'
t42 = topic(N42, N42.lower(), 'kinetic theory of gases', 'pv = ⅓nm⟨c²⟩')
FX(t42, 'C1', (1, 2), [
    ('Which is an assumption of the kinetic theory of an ideal gas?', 'the collisions of the molecules are perfectly elastic', 'Kinetic energy is conserved in collisions.', ['the molecules attract each other strongly', 'the molecules all move at the same speed', 'the volume of the molecules is large compared with the container']),
    ('Which is an assumption of the kinetic model of an ideal gas?', 'the time spent in collisions is negligible compared with the time between collisions', 'Collisions are instantaneous.', ['the molecules are at rest between collisions', 'the molecules move in ordered layers', 'there are forces between molecules at all times']),
    ('In pV = ⅓Nm⟨c²⟩, what does ⟨c²⟩ represent?', 'the mean of the squares of the speeds of the molecules', 'Mean square speed.', ['the square of the mean speed', 'the speed of the fastest molecule squared', 'the speed of sound squared']),
    ('Which expression gives the pressure of an ideal gas of density ρ?', '⅓ρ⟨c²⟩', 'p = ⅓(Nm/V)⟨c²⟩ = ⅓ρ⟨c²⟩.', ['⅔ρ⟨c²⟩', 'ρ⟨c²⟩', '3ρ⟨c²⟩']),
    ('Gas molecules hit a container wall. The pressure on the wall is due to', 'the rate of change of momentum of the molecules at the wall', 'Force = rate of change of momentum; pressure = force/area.', ['the weight of the molecules', 'the attractive forces between molecules', 'the kinetic energy lost in collisions']),
    ('Four molecules have speeds 1, 2, 3 and 4 (in units of 100 m s⁻¹). What is their root-mean-square speed?', '274 m s⁻¹', '√((1 + 4 + 9 + 16)/4) × 100 = √7.5 × 100.', ['250 m s⁻¹', '300 m s⁻¹', '750 m s⁻¹']),
    ('State two assumptions of the kinetic theory of gases.', 'e.g. large number of molecules in random motion; elastic collisions; negligible molecular volume; no intermolecular forces except in collisions; collision time negligible.', 'any two [2]'),
])
FX(t42, 'C2', (1, 2, 3, 4), [
    ('Explain, in terms of molecules, how a gas exerts a pressure on the walls of its container.', 'Molecules collide with the walls and rebound, so their momentum changes; the wall exerts a force on each molecule and, by Newton\'s third law, the molecules exert a force on the wall. Many collisions per second give a steady force per unit area.', 'momentum change on collision [1]; force on wall (N3), many collisions → pressure = force/area [1] [2]'),
    ('Explain, using kinetic theory, why the pressure of a gas increases when it is heated at constant volume.', 'The molecules\' mean speed increases, so they hit the walls more often and with greater change of momentum per collision; the rate of change of momentum (force) on the walls increases.', 'higher speed [1]; more frequent and harder collisions → more force [1] [2]'),
    ('A molecule of mass m moving at speed c perpendicular to a wall rebounds elastically. Show that its change in momentum is 2mc and explain how this leads to the force on the wall.', 'Momentum changes from +mc to −mc: Δp = 2mc. In a cube of side L the time between hits on the same wall is 2L/c, so the mean force = 2mc ÷ (2L/c) = mc²/L.', 'Δp = 2mc [1]; time 2L/c so F = mc²/L [1] [2]'),
    ('Explain why the factor ⅓ appears in pV = ⅓Nm⟨c²⟩.', 'Molecules move randomly in three dimensions; on average ⟨c²⟩ = ⟨cₓ²⟩ + ⟨c_y²⟩ + ⟨c_z²⟩ with the three equal, so ⟨cₓ²⟩ = ⅓⟨c²⟩ for the direction perpendicular to a wall.', 'random motion, three equal components [1]; ⟨cₓ²⟩ = ⅓⟨c²⟩ [1] [2]'),
])


@t42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t42_rms(r, D):
    gas, Mm = r.choice(GASES)
    p = r.choice([1.0e5, 1.2e5, 2.0e5, 5.0e4]); rho = p * Mm / (RG * r.choice([273, 300, 350, 400]))
    rho = float(nf(rho, 3))
    c2 = 3 * p / rho; crms = math.sqrt(c2)
    s = f'A sample of {gas} has density {nf(rho, 3)} kg m⁻³ at a pressure of {sc(p)} Pa.'
    if D <= 2:
        return numq(r, D, s, 'root-mean-square speed of the molecules', crms, ' m s⁻¹', f'p = ⅓ρ⟨c²⟩ ⇒ c_rms = √(3p/ρ) = √(3 × {sc(p)}/{nf(rho, 3)})', [math.sqrt(p / rho), c2, crms * 3], fm=f3)
    if D == 3:
        return Q(s + ' Use p = ⅓ρ⟨c²⟩ to calculate the mean-square speed and the root-mean-square speed of the molecules.', f'⟨c²⟩ = {sc(c2)} m² s⁻²; c_rms = {f3(crms)} m s⁻¹',
                 f'⟨c²⟩ = 3p/ρ [1]; = {sc(c2)} m² s⁻² [1]; c_rms = {f3(crms)} m s⁻¹ [1] [3]')
    return Q(s + ' (a) Show that p = ⅓ρ⟨c²⟩ follows from pV = ⅓Nm⟨c²⟩. (b) Calculate the r.m.s. speed of the molecules. (c) The pressure is doubled at constant temperature. State and explain what happens to the r.m.s. speed.',
             f'(a) ρ = Nm/V so p = ⅓(Nm/V)⟨c²⟩ = ⅓ρ⟨c²⟩ (b) {f3(crms)} m s⁻¹ (c) unchanged: ρ doubles too, so p/ρ is constant (c_rms depends only on T)',
             f'(a) ρ = Nm/V [1] (b) c_rms = √(3p/ρ) [1]; = {f3(crms)} m s⁻¹ [1] (c) unchanged [1]; ρ doubles / depends only on T [1] [5]', 'multi_step')


@t42.add('C3', (2, 3, 4), 'numerical')
def t42_list(r, D):
    sp = sorted(r.sample([200, 300, 400, 500, 600, 700, 800, 900], r.choice([4, 5])))
    mean = sum(sp) / len(sp); ms = sum(v * v for v in sp) / len(sp); rms = math.sqrt(ms)
    lst = ', '.join(str(v) for v in sp)
    return Q(f'In a model, the molecules of a gas have speeds of {lst} m s⁻¹. Calculate the mean speed, the mean-square speed and the root-mean-square speed.' + (' Explain why the r.m.s. speed is greater than the mean speed.' if D >= 4 else ''),
             f'mean = {f3(mean)} m s⁻¹; ⟨c²⟩ = {sc(ms)} m² s⁻²; c_rms = {f3(rms)} m s⁻¹' + ('; squaring gives more weight to the faster molecules' if D >= 4 else ''),
             f'mean = {f3(mean)} m s⁻¹ [1]; ⟨c²⟩ = {sc(ms)} m² s⁻² [1]; c_rms = {f3(rms)} m s⁻¹ [1]' + ('; squaring weights larger speeds [1] [4]' if D >= 4 else ' [3]'))


def _kt_c4(r, D):
    L = r.choice([0.10, 0.20, 0.30]); m = r.choice([4.0, 28.0, 32.0]); c = r.choice([400.0, 500.0, 1200.0])
    mk = m * 1.66e-27
    intro = f'A single molecule of mass {sc(mk)} kg moves with speed {nf(c)} m s⁻¹ back and forth perpendicular to two opposite walls of a cube of side {nf(L)} m, colliding elastically.'
    F = mk * c * c / L
    parts = [
        lambda r: ('Calculate the change in momentum of the molecule in one collision with a wall.', f'{sc(2 * mk * c)} N s', 'Δp = 2mc [2]'),
        lambda r: ('Calculate the time between successive collisions with the same wall.', f'{sc(2 * L / c)} s', 't = 2L/c [1]'),
        lambda r: ('Calculate the mean force exerted on the wall by this molecule.', f'{sc(F)} N', 'F = Δp/t = mc²/L [2]'),
        lambda r: ('Explain how this model is extended to give pV = ⅓Nm⟨c²⟩.', 'N molecules with random velocities: use mean-square speed, and ⟨cₓ²⟩ = ⅓⟨c²⟩ for each direction; pressure = force/area with V = L³.', 'N molecules and ⟨c²⟩ [1]; factor ⅓ from three directions [1]; p = F/L² and V = L³ [1] [3]'),
        lambda r: ('State two assumptions of the kinetic theory used in this derivation.', 'Elastic collisions; no intermolecular forces; negligible molecular volume; collision time negligible.', 'first valid assumption [1]; second valid assumption [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t42.add('C4', (2, 3, 4, 5), 'multi_step')(_kt_c4)

N43 = 'Average kinetic energy of a molecule and temperature: ⅔kT relation'
t43 = topic(N43, N43.lower(), 'average kinetic energy of a molecule', 'temperature')
FX(t43, 'C1', (1, 2), [
    ('Which expression gives the mean translational kinetic energy of a molecule of an ideal gas at thermodynamic temperature T?', '3kT/2', '½m⟨c²⟩ = (3/2)kT.', ['kT/2', '2kT/3', '3RT/2']),
    ('What is the mean kinetic energy of a molecule of an ideal gas at 300 K?', '6.21 × 10⁻²¹ J', '1.5 × 1.38 × 10⁻²³ × 300.', ['4.14 × 10⁻²¹ J', '3.74 × 10³ J', '2.07 × 10⁻²¹ J']),
    ('The thermodynamic temperature of an ideal gas is doubled. The r.m.s. speed of its molecules is multiplied by', '√2', 'c_rms ∝ √T.', ['2', '4', '1/√2']),
    ('Helium and argon are at the same temperature. Which quantity is the same for both?', 'the mean kinetic energy of the molecules', 'Mean KE depends only on T.', ['the r.m.s. speed', 'the mass of a molecule', 'the momentum of each molecule']),
    ('At what temperature would the mean kinetic energy of the molecules of an ideal gas be zero (classically)?', '0 K', 'Mean KE ∝ T.', ['0 °C', '−100 °C', '273 K']),
    ('Hydrogen (molar mass 2 g mol⁻¹) and oxygen (32 g mol⁻¹) are at the same temperature. The ratio c_rms(H₂)/c_rms(O₂) is', '4', 'c_rms ∝ 1/√m: √(32/2) = 4.', ['16', '1/4', '2']),
    ('State the relationship between the mean kinetic energy of a molecule of an ideal gas and its thermodynamic temperature.', '½m⟨c²⟩ = (3/2)kT: mean KE is proportional to T.', '½m⟨c²⟩ = 3kT/2 [1]'),
])
FX(t43, 'C2', (1, 2, 3, 4), [
    ('Use pV = NkT and pV = ⅓Nm⟨c²⟩ to show that the mean kinetic energy of a molecule is (3/2)kT.', 'Equate: ⅓Nm⟨c²⟩ = NkT, so m⟨c²⟩ = 3kT and ½m⟨c²⟩ = (3/2)kT.', 'equate the two expressions [1]; rearrange to ½m⟨c²⟩ = 3kT/2 [1] [2]'),
    ('Explain why, at the same temperature, the molecules of hydrogen move faster on average than the molecules of nitrogen.', 'At the same T the mean KE ½m⟨c²⟩ is the same; hydrogen molecules have smaller mass, so their mean-square speed must be larger.', 'same mean KE at same T [1]; smaller m so larger speed [1] [2]'),
    ('Explain what the thermodynamic temperature of a gas represents at the molecular level.', 'It is proportional to the mean random (translational) kinetic energy of the molecules.', 'proportional to mean KE [1]; random motion [1] [2]'),
    ('Explain why some light molecules such as hydrogen can escape from the Earth\'s atmosphere although the mean speed is well below the escape speed.', 'There is a distribution of speeds; a small fraction of hydrogen molecules (which have high mean speed because of their small mass) have speeds above escape speed and are lost over time.', 'distribution of speeds [1]; some exceed escape speed, more likely for light molecules [1] [2]'),
])
relation(t43, 'C2', (2, 3), '½m⟨c²⟩ = (3/2)kT', 'r.m.s. speed of the molecules', {'thermodynamic temperature': 0.5, 'mass of a molecule': -0.5},
         ['An ideal gas is kept in a sealed container.', 'A sample of a noble gas is studied in a laboratory.', 'A gas in a star\'s outer layers is modelled as ideal.'])


@t43.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t43_ke(r, D):
    gas, Mm = r.choice(GASES)
    th = r.choice([-50.0, 0.0, 20.0, 27.0, 100.0, 227.0, 527.0]); T = th + 273.0
    ke = 1.5 * KB * T; m = Mm / NA; crms = math.sqrt(3 * KB * T / m)
    s = f'A sample of {gas} (molar mass {nf(Mm * 1000, 3)} g mol⁻¹) is at a temperature of {nf(th)} °C.'
    if D <= 2:
        return numq(r, D, s, 'mean translational kinetic energy of a molecule', ke, ' J', f'E = (3/2)kT = 1.5 × 1.38 × 10⁻²³ × {nf(T)}', [KB * T, 1.5 * KB * th if th > 0 else KB * T / 2, 1.5 * RG * T], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(s + ' Calculate the mass of one molecule and the r.m.s. speed of the molecules.', f'm = {sc(m)} kg; c_rms = {f3(crms)} m s⁻¹',
                 f'm = M/N_A = {sc(m)} kg [1]; ½m⟨c²⟩ = 3kT/2 [1]; c_rms = {f3(crms)} m s⁻¹ [1] [3]')
    T2 = 4 * T
    return Q(s + f' (a) Calculate the mean kinetic energy of a molecule. (b) Calculate the r.m.s. speed of the molecules. (c) Calculate the temperature, in °C, at which the r.m.s. speed is twice this value.',
             f'(a) {sc(ke)} J (b) {f3(crms)} m s⁻¹ (c) {nf(T2 - 273)} °C', f'(a) 3kT/2 = {sc(ke)} J [1] (b) m = M/N_A [1]; c_rms = {f3(crms)} m s⁻¹ [1] (c) c_rms ∝ √T so T × 4 = {nf(T2)} K [1]; = {nf(T2 - 273)} °C [1] [5]', 'multi_step')


@t43.add('C3', (2, 3, 4, 5), 'numerical')
def t43_total(r, D):
    gas, Mm = r.choice(GASES[:5])
    n = r.choice([0.20, 0.50, 1.0, 2.5]); th = r.choice([20.0, 50.0, 100.0]); T = th + 273
    U = 1.5 * n * RG * T
    return Q(f'A container holds {nf(n)} mol of {gas} (a monatomic ideal gas) at {nf(th)} °C. Calculate the total kinetic energy of all the atoms.' if gas in ('helium', 'neon', 'argon') else f'A container holds {nf(n)} mol of an ideal monatomic gas at {nf(th)} °C. Calculate the total translational kinetic energy of all the molecules.',
             f'{E(U)} J', f'N = nN_A [1]; mean KE = 3kT/2 [1]; total = N × 3kT/2 = (3/2)nRT = {E(U)} J [1]' + (' [3]' if D <= 3 else '; statement that for an ideal gas this is the internal energy (no potential energy) [1] [4]'))


def _ket_c4(r, D):
    a, b = r.sample(GASES[:6], 2)
    T = r.choice([280.0, 300.0, 350.0])
    ca = math.sqrt(3 * KB * T / (a[1] / NA)); cb = math.sqrt(3 * KB * T / (b[1] / NA))
    intro = f'A mixture of {a[0]} (molar mass {nf(a[1] * 1000, 3)} g mol⁻¹) and {b[0]} (molar mass {nf(b[1] * 1000, 3)} g mol⁻¹) is at {nf(T)} K.'
    parts = [
        lambda r: ('Show that the mean kinetic energy of a molecule is (3/2)kT.', '⅓Nm⟨c²⟩ = NkT ⇒ ½m⟨c²⟩ = 3kT/2.', 'equate expressions [1]; rearrange [1] [2]'),
        lambda r: ('Calculate the mean kinetic energy of a molecule of each gas.', f'{sc(1.5 * KB * T)} J for both', 'same for both [2]'),
        lambda r: (f'Calculate the r.m.s. speed of the {a[0]} molecules.', f'{f3(ca)} m s⁻¹', 'c = √(3kT/m) [2]'),
        lambda r: (f'Calculate the ratio of the r.m.s. speed of {a[0]} to that of {b[0]}.', f'{f3(ca / cb)}', '√(M_b/M_a) [2]'),
        lambda r: ('Explain why the two gases have the same mean kinetic energy.', 'They are at the same temperature, and mean KE depends only on T.', 'same T [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t43.add('C4', (2, 3, 4, 5), 'multi_step')(_ket_c4)
CHAPTERS[4] = [t41, t42, t43]

# ===================================================================== 5 Thermodynamics
N51 = 'Internal energy as the sum of random kinetic and potential energies'
t51 = topic(N51, N51.lower(), 'internal energy', 'random kinetic and potential energies')
FX(t51, 'C1', (1, 2), [
    ('What is the internal energy of a system?', 'the sum of a random distribution of kinetic and potential energies of its molecules', 'U = ΣEk + ΣEp of the molecules (random).', ['the total kinetic energy of the system moving as a whole', 'the thermal energy supplied to the system', 'the potential energy of the system due to its height']),
    ('The internal energy of an ideal gas consists of', 'random kinetic energy of the molecules only', 'No intermolecular forces, so no potential energy.', ['potential energy of the molecules only', 'equal amounts of kinetic and potential energy', 'kinetic energy of the container']),
    ('Water at 100 °C turns into steam at 100 °C. The internal energy', 'increases because the potential energy of the molecules increases', 'Separation increases; mean KE constant.', ['decreases because the molecules spread out', 'stays the same because the temperature is constant', 'increases because the kinetic energy increases']),
    ('An ideal gas is heated so that its thermodynamic temperature doubles. Its internal energy', 'doubles', 'U = (3/2)NkT ∝ T for an ideal monatomic gas.', ['stays the same', 'quadruples', 'halves']),
    ('A sealed box of gas is carried up a mountain at constant temperature. Its internal energy', 'is unchanged', 'Internal energy does not include the PE of the whole box in the gravitational field.', ['increases', 'decreases', 'becomes zero']),
    ('Which change always increases the internal energy of a solid?', 'a rise in its temperature', 'Higher temperature means greater mean random kinetic energy.', ['moving it at a higher speed', 'lifting it to a greater height', 'cutting it in half']),
    ('State what is meant by internal energy.', 'The sum of a random distribution of kinetic and potential energies of the molecules of a system.', 'sum of random KE and PE of molecules [1]'),
])
FX(t51, 'C2', (1, 2, 3, 4), [
    ('Explain why the internal energy of an ideal gas depends only on its temperature.', 'There are no intermolecular forces, so the molecules have no potential energy; internal energy is the total random KE, which is proportional to T.', 'no intermolecular forces so no PE [1]; KE ∝ T [1] [2]'),
    ('Explain why 1 kg of steam at 100 °C has more internal energy than 1 kg of water at 100 °C.', 'The mean kinetic energy is the same (same temperature), but the steam molecules are much further apart so they have much greater (less negative) potential energy; latent heat has been supplied.', 'same KE (same T) [1]; greater PE in steam [1] [2]'),
    ('Explain why a moving car does not have more internal energy than a stationary car at the same temperature.', 'Internal energy involves only the random motion of molecules; the ordered motion of the whole car is macroscopic kinetic energy, not internal energy.', 'internal energy = random molecular energy [1]; bulk KE excluded [1] [2]'),
    ('Explain, in terms of molecular energies, what happens to the internal energy of ice when it melts at 0 °C.', 'The energy supplied breaks bonds, increasing the potential energy of the molecules; the mean kinetic energy stays constant as the temperature does not change; so internal energy increases.', 'PE increases [1]; KE constant, internal energy increases [1] [2]'),
])


@t51.add('C2', (2, 3, 4), 'explain')
def t51_cases(r, D):
    case, ans = r.choice([
        ('a block of ice at −10 °C warming to −2 °C', 'U increases: mean kinetic energy of the molecules increases (temperature rises); potential energy changes little.'),
        ('water at 100 °C boiling to steam at 100 °C', 'U increases: potential energy increases as molecules separate; kinetic energy constant (temperature constant).'),
        ('an ideal gas expanding at constant temperature', 'U unchanged: an ideal gas has no PE and its KE depends only on T, which is constant.'),
        ('molten wax solidifying at its melting point', 'U decreases: potential energy decreases as bonds form (energy released); kinetic energy constant.'),
        ('an ideal gas compressed quickly so that its temperature rises', 'U increases: mean KE of the molecules increases with temperature; no PE for an ideal gas.'),
        ('a steel ball dropped from a balcony and coming to rest on the ground, with no change in temperature', 'U essentially unchanged once it has cooled to the same temperature; the loss of gravitational PE of the whole ball is not internal energy.'),
    ])
    return Q(f'State and explain, in terms of molecular kinetic and potential energies, how the internal energy changes for {case}.', ans,
             'direction of change in U [1]; correct reference to kinetic and potential energy [1]' + ('; link to temperature (mean KE) [1] [3]' if D >= 3 else ' [2]'))


@t51.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t51_U(r, D):
    n = r.choice([0.10, 0.25, 0.50, 1.0, 2.0, 3.0]); T1 = r.choice([250.0, 300.0, 320.0]); T2 = T1 + r.choice([20.0, 50.0, 100.0, 150.0])
    U1 = 1.5 * n * RG * T1; dU = 1.5 * n * RG * (T2 - T1)
    s = f'A container holds {nf(n)} mol of an ideal monatomic gas at {nf(T1)} K.'
    if D <= 2:
        return numq(r, D, s, 'internal energy of the gas', U1, ' J', f'U = N × (3/2)kT = (3/2)nRT = 1.5 × {nf(n)} × 8.31 × {nf(T1)}', [n * RG * T1, 1.5 * RG * T1, U1 * 2], fm=f3)
    if D == 3:
        return Q(s + f' The gas is heated to {nf(T2)} K. Calculate the increase in internal energy and explain why the gas has no intermolecular potential energy.', f'ΔU = {f3(dU)} J; ideal gas has no intermolecular forces',
                 f'U = (3/2)nRT [1]; ΔU = 1.5nRΔT = {f3(dU)} J [1]; no forces between molecules [1] [3]')
    return Q(s + f' (a) Calculate the internal energy of the gas. (b) The gas is heated at constant volume to {nf(T2)} K. Calculate the thermal energy supplied. (c) Explain why more energy would be needed for the same temperature rise at constant pressure.',
             f'(a) {f3(U1)} J (b) {f3(dU)} J (c) at constant pressure the gas expands and does work on the surroundings, so q = ΔU + pΔV',
             f'(a) U = (3/2)nRT = {f3(U1)} J [1] (b) W = 0 so q = ΔU [1]; = {f3(dU)} J [1] (c) gas expands, does work [1]; extra energy needed [1] [5]', 'multi_step')


def _ie_c4(r, D):
    m = r.choice([0.20, 0.50, 1.0]); L = 2.26e6
    intro = f'{nf(m)} kg of water at 100 °C in a kettle is boiled until it has all turned to steam at 100 °C.'
    parts = [
        lambda r: ('Define internal energy.', 'Sum of the random kinetic and potential energies of the molecules.', 'random KE + PE of molecules [1]'),
        lambda r: ('State and explain what happens to the mean kinetic energy of the molecules during boiling.', 'Unchanged: the temperature is constant.', 'unchanged because T constant [1]'),
        lambda r: ('Explain what happens to the potential energy of the molecules.', 'It increases: the molecules are separated against the intermolecular attractions.', 'increases [1]; molecules separated / bonds broken [1] [2]'),
        lambda r: (f'The specific latent heat of vaporisation of water is 2.26 × 10⁶ J kg⁻¹. Calculate the energy supplied.', f'{sc(m * L)} J', 'Q = mL [2]'),
        lambda r: ('Explain why the increase in internal energy is less than the energy supplied.', 'Some energy is used to do work pushing back the atmosphere as the steam expands (W = pΔV).', 'work done against atmosphere [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t51.add('C4', (2, 3, 4, 5), 'multi_step')(_ie_c4)

N52 = 'The first law of thermodynamics ΔU = q + W'
t52 = topic(N52, N52.lower(), 'first law of thermodynamics', 'δu = q + w')
FX(t52, 'C1', (1, 2), [
    ('In the first law of thermodynamics ΔU = q + W, what does W represent?', 'the work done on the system', 'W is work done ON the system (positive when the gas is compressed).', ['the work done by the system', 'the weight of the system', 'the power input']),
    ('A gas absorbs 500 J of thermal energy and does 200 J of work on its surroundings. What is the change in its internal energy?', '+300 J', 'ΔU = q + W = 500 + (−200).', ['+700 J', '−300 J', '+200 J']),
    ('A gas is compressed by doing 400 J of work on it, and it loses 150 J of thermal energy. What is ΔU?', '+250 J', 'ΔU = −150 + 400.', ['+550 J', '−250 J', '−550 J']),
    ('A gas expands at a constant pressure of 1.0 × 10⁵ Pa from 2.0 × 10⁻³ m³ to 5.0 × 10⁻³ m³. What is the work done on the gas?', '−300 J', 'W = −pΔV = −1.0 × 10⁵ × 3.0 × 10⁻³.', ['+300 J', '−700 J', '+500 J']),
    ('The first law of thermodynamics is a statement of', 'the conservation of energy', 'Increase in U = energy in by heating + energy in by work.', ['the conservation of momentum', 'the conservation of mass', 'Newton\'s second law']),
    ('For a gas, the work done on it is positive when the gas', 'is compressed', 'Volume decreases; surroundings do work on the gas.', ['expands', 'is heated at constant volume', 'cools at constant volume']),
    ('State the first law of thermodynamics in terms of the increase in internal energy of a system.', 'The increase in internal energy equals the sum of the thermal energy supplied to the system and the work done on the system.', 'ΔU = q + W with q supplied to and W done on the system [1]'),
])
FX(t52, 'C2', (1, 2, 3, 4), [
    ('Explain why the temperature of a gas rises when it is compressed rapidly in a bicycle pump.', 'Work is done on the gas (W positive) and, because the compression is rapid, there is little time for thermal energy to escape (q ≈ 0); so ΔU > 0 and the temperature rises.', 'work done on gas [1]; q ≈ 0 so ΔU positive, T rises [1] [2]'),
    ('Explain why a gas cools when it expands rapidly, as when gas escapes from an aerosol can.', 'The gas does work on the surroundings as it expands (W negative) with little time for heat to enter (q ≈ 0), so ΔU < 0 and the temperature falls.', 'gas does work, W negative [1]; q ≈ 0 so U and T fall [1] [2]'),
    ('Explain the sign of each term in ΔU = q + W when a gas is heated and expands.', 'q is positive (energy supplied by heating); W is negative because the gas does work on its surroundings as it expands; ΔU is positive if q exceeds the work done.', 'q positive [1]; W negative as gas does work [1] [2]'),
    ('Explain why W = −pΔV for a gas expanding at constant pressure.', 'The work done by the gas is force × distance = pA × Δx = pΔV; the work done on the gas is the negative of this.', 'work by gas = pΔV [1]; work on gas negative [1] [2]'),
])


@t52.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t52_first(r, D):
    p = r.choice([1.0e5, 1.5e5, 2.0e5, 3.0e5]); V1 = r.choice([1.0e-3, 2.0e-3, 3.0e-3, 4.0e-3]); dV = r.choice([0.5e-3, 1.0e-3, 1.5e-3, 2.0e-3])
    q = r.choice([400.0, 600.0, 800.0, 1200.0, 1500.0])
    exp = r.choice([True, False])
    W = -p * dV if exp else p * dV
    if not exp:
        q = -q / 2
    dU = q + W
    if exp:
        s = f'A gas in a cylinder is supplied with {nf(q)} J of thermal energy. It expands at a constant pressure of {sc(p)} Pa, increasing in volume by {sc(dV)} m³.'
    else:
        s = f'A gas in a cylinder is compressed at a constant pressure of {sc(p)} Pa, its volume decreasing by {sc(dV)} m³. During the compression it loses {nf(-q)} J of thermal energy to the surroundings.'
    if D <= 2:
        return numq(r, D, s, 'work done on the gas', W, ' J', f'W = −pΔV = −{sc(p)} × ({"+" if exp else "−"}{sc(dV)})', [-W, W * 10, q], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the work done on the gas and the change in its internal energy.', f'W = {nf(W, 3)} J; ΔU = {nf(dU, 3)} J',
                 f'W = −pΔV = {nf(W, 3)} J [1]; ΔU = q + W [1]; = {nf(dU, 3)} J [1] [3]')
    return Q(s + ' (a) Calculate the work done on the gas. (b) Calculate the change in internal energy. (c) State and explain whether the temperature of the gas rises or falls.',
             f'(a) {nf(W, 3)} J (b) {nf(dU, 3)} J (c) {"rises" if dU > 0 else "falls"}: internal energy of an ideal gas is proportional to T',
             f'(a) W = −pΔV [1]; {nf(W, 3)} J [1] (b) ΔU = q + W with signs [1]; {nf(dU, 3)} J [1] (c) {"rises" if dU > 0 else "falls"} with reason [1] [5]', 'multi_step')


@t52.add('C2', (2, 3, 4), 'explain')
def t52_table(r, D):
    proc, q, W = r.choice([('gas heated at constant volume', 'positive', 'zero'), ('gas compressed rapidly with no heat exchange', 'zero', 'positive'), ('gas expanding rapidly with no heat exchange', 'zero', 'negative'),
                           ('gas compressed slowly at constant temperature', 'negative', 'positive'), ('gas expanding slowly at constant temperature', 'positive', 'negative'), ('gas cooled at constant volume', 'negative', 'zero')])
    dU = {('positive', 'zero'): 'positive', ('zero', 'positive'): 'positive', ('zero', 'negative'): 'negative', ('negative', 'positive'): 'zero', ('positive', 'negative'): 'zero', ('negative', 'zero'): 'negative'}[(q, W)]
    return Q(f'For an ideal gas undergoing the process "{proc}", state whether each of q, W and ΔU in ΔU = q + W is positive, negative or zero, and explain your answers.',
             f'q {q}, W {W}, ΔU {dU}.', f'q {q} with reason [1]; W {W} with reason [1]' + (f'; ΔU {dU} (linked to temperature change) [1] [3]' if D >= 3 else f' [2]'))


def _fl_c4(r, D):
    p = r.choice([1.0e5, 2.0e5]); V1 = r.choice([1.0e-3, 2.0e-3]); V2 = V1 * r.choice([2, 3]); q = r.choice([800.0, 1000.0, 1500.0])
    W = -p * (V2 - V1); dU = q + W
    intro = f'An ideal gas in a cylinder fitted with a frictionless piston is heated. It expands at a constant pressure of {sc(p)} Pa from {sc(V1)} m³ to {sc(V2)} m³ while absorbing {nf(q)} J of thermal energy.'
    parts = [
        lambda r: ('State the first law of thermodynamics.', 'Increase in internal energy = thermal energy supplied to the system + work done on the system.', 'ΔU = q + W with meanings [1]'),
        lambda r: ('Calculate the work done on the gas.', f'{nf(W, 3)} J', 'W = −pΔV [2]'),
        lambda r: ('Calculate the increase in internal energy of the gas.', f'{nf(dU, 3)} J', 'ΔU = q + W [2]'),
        lambda r: (f'The initial temperature is 300 K. Calculate the final temperature.', f'{nf(300 * V2 / V1)} K', 'V ∝ T at constant p [2]'),
        lambda r: ('Explain why the temperature rises even though the gas does work.', 'The thermal energy supplied is greater than the work done by the gas, so internal energy (∝ T) increases.', 'q > work done by gas [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t52.add('C4', (2, 3, 4, 5), 'multi_step')(_fl_c4)

N53 = 'Applying the first law to changes of state and gas processes'
t53 = topic(N53, N53.lower(), 'applying the first law', 'changes of state and gas processes')
FX(t53, 'C1', (1, 2), [
    ('An ideal gas expands at constant temperature. Which statement is correct?', 'ΔU = 0 and q = −W', 'U depends only on T for an ideal gas.', ['q = 0 and ΔU = W', 'W = 0 and ΔU = q', 'ΔU = q + W = 0 because q = 0']),
    ('A gas is heated at constant volume. Which term in ΔU = q + W is zero?', 'W', 'No volume change, so no work done.', ['q', 'ΔU', 'none of them']),
    ('On a p–V diagram, the work done by a gas in a complete cycle is equal to', 'the area enclosed by the loop', 'Net work = enclosed area.', ['the area under the top curve only', 'the gradient of the loop', 'zero for every cycle']),
    ('After a complete cycle, the change in internal energy of a gas is', 'zero', 'The gas returns to its initial state.', ['equal to the work done', 'equal to the heat supplied', 'negative']),
    ('When 1 kg of water boils at atmospheric pressure, which is true?', 'the thermal energy supplied is greater than the increase in internal energy', 'Part of the energy does work pushing back the atmosphere: ΔU = mL − pΔV.', ['the thermal energy supplied equals the increase in internal energy', 'no work is done because the temperature is constant', 'the internal energy decreases']),
    ('A process in which no thermal energy enters or leaves a gas is called', 'adiabatic', 'q = 0.', ['isothermal', 'isobaric', 'isovolumetric']),
    ('State the value of ΔU for an ideal gas taken round a complete cycle.', 'Zero.', 'ΔU = 0 [1]'),
])
FX(t53, 'C2', (1, 2, 3, 4), [
    ('Explain why, when an ideal gas expands at constant temperature, all the thermal energy supplied is used to do work.', 'The internal energy depends only on temperature, so ΔU = 0; from ΔU = q + W, q = −W: the heat supplied equals the work done by the gas.', 'ΔU = 0 at constant T [1]; q = −W [1] [2]'),
    ('Explain why the increase in internal energy when water boils is less than mL.', 'When water becomes steam its volume increases greatly, so work pΔV is done against the atmosphere; ΔU = mL − pΔV.', 'large volume increase [1]; work done against atmosphere reduces ΔU [1] [2]'),
    ('Explain how the net work done by a gas in a cycle can be found from a p–V diagram.', 'Work done by the gas = area under the curve when expanding; work done on it = area under the compression curve; the net work is the difference, i.e. the area enclosed by the loop.', 'area under curve = work [1]; net = enclosed area [1] [2]'),
    ('Explain why heat must be supplied to a gas when it expands at constant pressure.', 'At constant pressure V ∝ T, so T and hence U increase; the gas also does work. Both require energy, which must be supplied as heat: q = ΔU + pΔV.', 'temperature rises so U increases [1]; gas does work, so q = ΔU + pΔV > 0 [1] [2]'),
])


@t53.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t53_boil(r, D):
    m = r.choice([0.010, 0.020, 0.025, 0.040, 0.050, 0.080, 0.10, 0.15, 0.25]); L = 2.26e6; p = 1.01e5
    rs = r.choice([0.590, 0.600, 0.598])
    Vw = m / 1000; Vs = m / rs
    W = p * (Vs - Vw); Q_ = m * L; dU = Q_ - W
    where = ctx(r, ['in a kettle in {c}', 'in an open pan in a kitchen in {c}', 'in a laboratory flask in {c}', 'in a boiler test rig in {c}', 'by {p} in a school laboratory'])
    s = f'{nf(m * 1000)} g of water at 100 °C is boiled {where} at atmospheric pressure (1.01 × 10⁵ Pa) to form steam at 100 °C. The density of the water is 1000 kg m⁻³ and of the steam {nf(rs, 3)} kg m⁻³. (specific latent heat of vaporisation 2.26 × 10⁶ J kg⁻¹)'
    if D <= 2:
        return numq(r, D, s, 'thermal energy supplied', Q_, ' J', f'q = mL = {nf(m)} × 2.26 × 10⁶', [Q_ / 1000, W, L], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the work done by the water as it expands into steam.', f'{E(W)} J', f'ΔV = m/ρ_s − m/ρ_w = {sc(Vs - Vw)} m³ [1]; W = pΔV [1]; = {E(W)} J [1] [3]')
    return Q(s + ' (a) Calculate the thermal energy supplied. (b) Calculate the work done against the atmosphere. (c) Calculate the increase in internal energy and explain which energy store of the molecules increases.',
             f'(a) {E(Q_)} J (b) {E(W)} J (c) {E(dU)} J; potential energy of the molecules (KE constant at constant T)',
             f'(a) q = mL = {E(Q_)} J [1] (b) ΔV = {sc(Vs - Vw)} m³ [1]; W = pΔV = {E(W)} J [1] (c) ΔU = q − pΔV = {E(dU)} J [1]; PE increases [1] [5]', 'multi_step')


@t53.add('C3', (2, 3, 4, 5), 'case')
def t53_cycle(r, D):
    pA = r.choice([1.0e5, 1.5e5, 2.0e5, 2.5e5]); pB = pA * r.choice([1.5, 2, 3, 4]); V1 = r.choice([1.0e-3, 1.5e-3, 2.0e-3, 4.0e-3]); V2 = V1 * r.choice([1.5, 2, 3])
    Wnet = (pB - pA) * (V2 - V1)
    s = (f'A gas is taken round a rectangular cycle on a p–V diagram: A ({sc(pA)} Pa, {sc(V1)} m³) → B ({sc(pB)} Pa, {sc(V1)} m³) → C ({sc(pB)} Pa, {sc(V2)} m³) → D ({sc(pA)} Pa, {sc(V2)} m³) → A.')
    if D <= 3:
        return Q(s + ' Calculate the work done by the gas from B to C, the work done on the gas from D to A, and the net work done by the gas in one cycle.', f'W_BC = {nf(pB * (V2 - V1), 3)} J; W_DA (on gas) = {nf(pA * (V2 - V1), 3)} J; net = {nf(Wnet, 3)} J',
                 f'W_BC = pΔV = {nf(pB * (V2 - V1), 3)} J [1]; W_DA = {nf(pA * (V2 - V1), 3)} J [1]; net = area of loop = {nf(Wnet, 3)} J [1] [3]')
    return Q(s + ' (a) State the work done on the gas in A → B and explain your answer. (b) Calculate the net work done by the gas in one cycle. (c) Explain why the net thermal energy supplied to the gas in one cycle equals this net work.',
             f'(a) zero: volume constant (b) {nf(Wnet, 3)} J (c) the gas returns to its initial state so ΔU = 0; q_net = −W_net(on) = work done by the gas',
             f'(a) zero, no volume change [1] (b) area enclosed [1]; = {nf(Wnet, 3)} J [1] (c) ΔU = 0 over cycle [1]; q = −W [1] [5]', 'multi_step')


@t53.add('C2', (2, 3, 4), 'explain')
def t53_iso(r, D):
    proc = r.choice([('isothermal compression', 'ΔU = 0 (T constant); W positive (work done on gas); so q negative: heat flows out, equal to the work done on it.'),
                     ('adiabatic expansion', 'q = 0; W negative (gas does work); so ΔU negative and the temperature falls.'),
                     ('heating at constant volume', 'W = 0; q positive; so ΔU = q is positive and the temperature rises.'),
                     ('expansion at constant pressure', 'T rises (V ∝ T) so ΔU positive; W negative; q = ΔU − W is positive and larger than ΔU.'),
                     ('adiabatic compression', 'q = 0; W positive; so ΔU positive and the temperature rises.')])
    return Q(f'Apply the first law of thermodynamics to an ideal gas undergoing {proc[0]}. Explain what happens to q, W and ΔU.', proc[1],
             'correct statement for two of q, W, ΔU [1]; third deduced using ΔU = q + W [1]' + ('; link of ΔU to temperature change [1] [3]' if D >= 3 else ' [2]'))


def _app1_c4(r, D):
    n = r.choice([0.50, 1.0, 2.0]); T1 = 300.0; T2 = r.choice([400.0, 450.0, 500.0]); p = 1.0e5
    dU = 1.5 * n * RG * (T2 - T1); W = -n * RG * (T2 - T1); q = dU - W
    intro = f'{nf(n)} mol of an ideal monatomic gas at {sc(p)} Pa is heated at constant pressure from {nf(T1)} K to {nf(T2)} K.'
    parts = [
        lambda r: ('Calculate the increase in internal energy.', f'{f3(dU)} J', 'ΔU = (3/2)nRΔT [2]'),
        lambda r: ('Calculate the change in volume of the gas.', f'{sc(n * RG * (T2 - T1) / p)} m³', 'ΔV = nRΔT/p [2]'),
        lambda r: ('Calculate the work done on the gas.', f'{f3(W)} J', 'W = −pΔV [2]'),
        lambda r: ('Use the first law to calculate the thermal energy supplied.', f'{f3(q)} J', 'q = ΔU − W [2]'),
        lambda r: ('Explain why less thermal energy is needed for the same temperature rise at constant volume.', 'No work is done, so q = ΔU only.', 'W = 0 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t53.add('C4', (2, 3, 4, 5), 'multi_step')(_app1_c4)
CHAPTERS[5] = [t51, t52, t53]

# ===================================================================== 6 Oscillations
OSC = [('a mass on a vertical spring', (0.20, 0.40, 0.50, 0.80, 1.2), (0.010, 0.020, 0.030, 0.050)),
       ('a simple pendulum', (1.4, 1.8, 2.0, 2.4, 3.0), (0.020, 0.040, 0.060, 0.080)),
       ('a tuning-fork prong', (2.27e-3, 3.82e-3, 4.55e-3), (5.0e-4, 1.0e-3)),
       ('a loudspeaker cone', (1.0e-3, 2.5e-3, 5.0e-3), (2.0e-4, 5.0e-4, 1.0e-3)),
       ('a building swaying in the wind', (4.0, 5.0, 6.5, 8.0), (0.10, 0.15, 0.25)),
       ('a car body on its suspension', (0.60, 0.80, 1.0), (0.020, 0.040, 0.060)),
       ('a trolley tethered between two springs', (0.80, 1.2, 1.6), (0.040, 0.060, 0.080)),
       ('a molecule in a crystal lattice (modelled classically)', (1.0e-13, 2.0e-13), (1.0e-11, 2.0e-11))]


def _osc(r):
    nm, Ts, xs = r.choice(OSC)
    return nm, r.choice(Ts), r.choice(xs)


def L_(x):
    """Length for display, in m with sensible notation."""
    return E(x, 2) + ' m'


N61 = 'Describing oscillations: displacement, amplitude, period, frequency, angular frequency and phase difference'
t61 = topic(N61, N61.lower(), 'describing oscillations', 'angular frequency')
FX(t61, 'C1', (1, 2), [
    ('What is meant by the amplitude of an oscillation?', 'the maximum displacement from the equilibrium position', 'Amplitude x₀ is the maximum displacement.', ['the distance travelled in one oscillation', 'the displacement at time t = 0', 'twice the maximum displacement']),
    ('An oscillator has a frequency of 50 Hz. What is its angular frequency?', '314 rad s⁻¹', 'ω = 2πf = 2π × 50.', ['50 rad s⁻¹', '7.96 rad s⁻¹', '0.020 rad s⁻¹']),
    ('What is the unit of angular frequency?', 'rad s⁻¹', 'ω = 2πf.', ['Hz s', 'rad', 's rad⁻¹']),
    ('Two identical pendulums oscillate with the same period T. One reaches its maximum displacement T/4 after the other. What is the phase difference?', 'π/2 rad', 'φ = 2πΔt/T = 2π/4.', ['π/4 rad', 'π rad', '2π rad']),
    ('An oscillation has a period of 0.25 s. What is its frequency?', '4.0 Hz', 'f = 1/T.', ['0.25 Hz', '25 Hz', '1.6 Hz']),
    ('Two oscillators are in antiphase. What is the phase difference between them?', 'π rad', 'Antiphase = 180° = π rad.', ['0', 'π/2 rad', '2π rad']),
    ('Define the period of an oscillation.', 'The time taken for one complete oscillation.', 'time for one complete oscillation [1]'),
    ('State the relationship between angular frequency ω and period T.', 'ω = 2π/T', 'ω = 2π/T [1]'),
])
FX(t61, 'C2', (1, 2, 3, 4), [
    ('Distinguish between displacement and amplitude for an oscillating object.', 'Displacement is the distance (with direction) from the equilibrium position at any instant and varies with time; amplitude is the maximum displacement and is constant for an undamped oscillation.', 'displacement: instantaneous, from equilibrium, varies [1]; amplitude: maximum displacement [1] [2]'),
    ('Explain what is meant by phase difference between two oscillations of the same frequency.', 'It is the fraction of a cycle by which one oscillation leads or lags the other, expressed as an angle (2π × fraction of a period).', 'fraction of cycle between them [1]; expressed as angle in rad/degrees [1] [2]'),
    ('Explain why angular frequency, rather than frequency, is used in the equations of simple harmonic motion.', 'SHM is related to motion in a circle: the displacement x = x₀ sin ωt uses an angle ωt in radians, which increases by 2π each period; ω = 2πf makes the equations simpler.', 'link to circular motion / angle ωt [1]; 2π per cycle, ω = 2πf [1] [2]'),
    ('A student says that two oscillators with different frequencies have a constant phase difference. Explain why this is incorrect.', 'If frequencies differ, one completes cycles faster, so the phase difference between them changes continuously with time; a constant phase difference requires equal frequencies.', 'phase difference changes with time [1]; constant only for same frequency [1] [2]'),
])


@t61.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t61_wf(r, D):
    nm, T, x0 = _osc(r)
    f = 1 / T; w = 2 * PI / T
    n = r.choice([10, 20, 25, 50]) if T > 0.1 else None
    if n:
        s = f'{cap(nm)} completes {n} oscillations in {nf(n * T, 3)} s with an amplitude of {L_(x0)}.'
        wk = f'T = {nf(n * T, 3)}/{n} = {E(T)} s; ω = 2π/T'
    else:
        s = f'{cap(nm)} oscillates with a period of {sc(T)} s and an amplitude of {L_(x0)}.'
        wk = f'ω = 2π/T = 2π/{sc(T)}'
    if D <= 2:
        return numq(r, D, s, 'angular frequency', w, ' rad s⁻¹', wk, [f, w / (2 * PI) ** 2, 2 * PI * T], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the period, the frequency and the angular frequency.', f'T = {E(T)} s; f = {E(f)} Hz; ω = {E(w)} rad s⁻¹',
                 f'T = {E(T)} s [1]; f = 1/T = {E(f)} Hz [1]; ω = 2πf = {E(w)} rad s⁻¹ [1] [3]')
    dt = T * r.choice([0.125, 0.25, 0.375, 0.5])
    phi = 2 * PI * dt / T
    return Q(s + f' A second identical oscillator reaches maximum displacement {E(dt)} s later. (a) Calculate the frequency. (b) Calculate the angular frequency. (c) Calculate the phase difference between the two oscillators in radians and in degrees.',
             f'(a) {E(f)} Hz (b) {E(w)} rad s⁻¹ (c) {f3(phi)} rad = {nf(math.degrees(phi), 3)}°', f'(a) f = 1/T = {E(f)} Hz [1] (b) ω = 2πf = {E(w)} rad s⁻¹ [1] (c) φ = 2πΔt/T [1]; = {f3(phi)} rad = {nf(math.degrees(phi), 3)}° [1] [4]', 'multi_step')


@t61.add('C3', (2, 3, 4), 'numerical')
def t61_phase(r, D):
    T = r.choice([0.40, 0.80, 1.2, 1.6, 2.0, 4.0]); frac = r.choice([(1, 8), (1, 6), (1, 4), (1, 3), (3, 8), (1, 2), (2, 3), (3, 4)])
    dt = T * frac[0] / frac[1]; phi = 2 * PI * frac[0] / frac[1]
    who = person(r)
    return Q(f'{who} watches two pendulums of period {nf(T)} s. Pendulum P passes through its equilibrium position moving to the right {nf(dt, 3)} s before pendulum Q does the same. Calculate the phase difference between P and Q, in radians and in degrees.' + (' State which oscillation leads.' if D >= 3 else ''),
             f'{f3(phi)} rad ({nf(math.degrees(phi), 3)}°)' + ('; P leads' if D >= 3 else ''), f'fraction of cycle = Δt/T = {nf(dt / T, 3)} [1]; φ = 2π × fraction = {f3(phi)} rad = {nf(math.degrees(phi), 3)}° [1]' + ('; P leads [1] [3]' if D >= 3 else ' [2]'))


def _desc_c4(r, D):
    nm, T, x0 = _osc(r)
    intro = f'{cap(nm)} oscillates with a period of {E(T)} s and an amplitude of {L_(x0)}.'
    parts = [
        lambda r: ('Define frequency.', 'Number of oscillations per unit time.', 'oscillations per unit time [1]'),
        lambda r: ('Calculate the frequency.', f'{E(1 / T)} Hz', 'f = 1/T [1]'),
        lambda r: ('Calculate the angular frequency.', f'{E(2 * PI / T)} rad s⁻¹', 'ω = 2π/T [2]'),
        lambda r: ('State the total distance moved in one complete oscillation.', f'{E(4 * x0, 2)} m', '4x₀ [1]'),
        lambda r: (f'A second identical oscillator lags by {E(T / 4)} s. State the phase difference.', 'π/2 rad (90°)', '¼ cycle [1]'),
        lambda r: ('Explain why the displacement is zero twice in each cycle.', 'The object passes through the equilibrium position twice per cycle, once in each direction.', 'passes equilibrium in both directions [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t61.add('C4', (2, 3, 4, 5), 'multi_step')(_desc_c4)

N62 = 'Simple harmonic motion: a = −ω²x and its solutions x = x₀ sin ωt'
t62 = topic(N62, N62.lower(), 'simple harmonic motion', 'a = −ω²x')
FX(t62, 'C1', (1, 2), [
    ('Which equation defines simple harmonic motion?', 'a = −ω²x', 'Acceleration proportional to displacement and directed towards the equilibrium position.', ['a = −ωx²', 'a = ω²x', 'v = −ω²x']),
    ('In SHM, where is the speed of the oscillator a maximum?', 'at the equilibrium position', 'v = ω√(x₀² − x²) is greatest at x = 0.', ['at maximum displacement', 'halfway between equilibrium and maximum displacement', 'it is the same at all points']),
    ('In SHM, where is the magnitude of the acceleration a maximum?', 'at maximum displacement', '|a| = ω²|x|.', ['at the equilibrium position', 'at half the amplitude', 'it is constant']),
    ('An oscillator in SHM has amplitude 0.050 m and angular frequency 4.0 rad s⁻¹. What is its maximum speed?', '0.20 m s⁻¹', 'v₀ = ωx₀.', ['0.80 m s⁻¹', '0.0125 m s⁻¹', '0.050 m s⁻¹']),
    ('A graph of acceleration a against displacement x for SHM is', 'a straight line through the origin with a negative gradient', 'a = −ω²x: gradient −ω².', ['a straight line through the origin with a positive gradient', 'a parabola', 'a circle']),
    ('An oscillator in SHM has displacement x = x₀ sin ωt. Which expression gives its velocity?', 'v = v₀ cos ωt', 'v = dx/dt = x₀ω cos ωt.', ['v = −v₀ sin ωt', 'v = v₀ sin ωt', 'v = −ω²x₀ cos ωt']),
    ('In SHM the velocity and the displacement are', 'π/2 rad out of phase', 'x = x₀ sin ωt, v = x₀ω cos ωt.', ['in phase', 'π rad out of phase', '2π rad out of phase']),
    ('State the defining equation of simple harmonic motion and the meaning of each symbol.', 'a = −ω²x: a acceleration, ω angular frequency, x displacement from equilibrium.', 'a = −ω²x with meanings [1]'),
])
FX(t62, 'C2', (1, 2, 3, 4), [
    ('Explain the significance of the minus sign in a = −ω²x.', 'The acceleration is always in the opposite direction to the displacement, i.e. always directed towards the equilibrium position (restoring).', 'acceleration opposite to displacement [1]; towards equilibrium [1] [2]'),
    ('State the conditions for an oscillation to be simple harmonic.', 'The acceleration (or restoring force) is proportional to the displacement from a fixed point and always directed towards that point.', 'a ∝ x [1]; directed towards equilibrium (opposite to x) [1] [2]'),
    ('Explain why the period of a simple harmonic oscillator does not depend on its amplitude.', 'a = −ω²x: a larger amplitude gives proportionally larger accelerations and speeds, so the object covers the larger distance in the same time; T = 2π/ω depends only on ω.', 'acceleration scales with displacement [1]; T = 2π/ω independent of x₀ [1] [2]'),
    ('Show that x = x₀ sin ωt satisfies a = −ω²x.', 'v = dx/dt = x₀ω cos ωt; a = dv/dt = −x₀ω² sin ωt = −ω²x.', 'differentiate once correctly [1]; second derivative = −ω²x [1] [2]'),
    ('A student claims a ball bouncing vertically on a hard floor performs SHM. Explain why this is incorrect.', 'While in the air its acceleration is constant (g downwards), not proportional to displacement from a fixed point, so it does not satisfy a = −ω²x.', 'acceleration constant (g) [1]; not ∝ displacement [1] [2]'),
])


@t62.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t62_max(r, D):
    nm, T, x0 = _osc(r)
    w = 2 * PI / T; v0 = w * x0; a0 = w * w * x0
    s = f'{cap(nm)} performs simple harmonic motion with amplitude {L_(x0)} and period {E(T)} s.'
    if D <= 2:
        q = r.choice(['v', 'a'])
        if q == 'v':
            return numq(r, D, s, 'maximum speed', v0, ' m s⁻¹', f'v₀ = ωx₀ = (2π/{E(T)}) × {E(x0, 2)}', [x0 / T, a0, v0 * 2 * PI], fm=lambda x: E(x, 3))
        return numq(r, D, s, 'maximum acceleration', a0, ' m s⁻²', f'a₀ = ω²x₀ = (2π/{E(T)})² × {E(x0, 2)}', [v0, w * x0 * x0, a0 / 2], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the maximum speed and the maximum acceleration.', f'v₀ = {E(v0)} m s⁻¹; a₀ = {E(a0)} m s⁻²',
                 f'ω = 2π/T = {E(w)} rad s⁻¹ [1]; v₀ = ωx₀ = {E(v0)} m s⁻¹ [1]; a₀ = ω²x₀ = {E(a0)} m s⁻² [1] [3]')
    x = x0 * r.choice([0.3, 0.4, 0.5, 0.6, 0.8])
    v = w * math.sqrt(x0 ** 2 - x ** 2)
    return Q(s + f' (a) Calculate the angular frequency. (b) Calculate the speed when the displacement is {E(x, 2)} m. (c) Calculate the acceleration at this displacement and state its direction.',
             f'(a) {E(w)} rad s⁻¹ (b) {E(v)} m s⁻¹ (c) {E(w * w * x)} m s⁻², towards the equilibrium position', f'(a) ω = 2π/T = {E(w)} rad s⁻¹ [1] (b) v = ω√(x₀² − x²) [1]; = {E(v)} m s⁻¹ [1] (c) a = ω²x = {E(w * w * x)} m s⁻² [1]; towards equilibrium [1] [5]', 'multi_step')


@t62.add('C3', (2, 3, 4, 5), 'numerical')
def t62_time(r, D):
    f = r.choice([0.50, 0.80, 1.25, 2.0, 2.5, 4.0]); x0 = r.choice([0.020, 0.030, 0.040, 0.060, 0.12]); t = r.choice([0.050, 0.10, 0.15, 0.20, 0.30])
    w = 2 * PI * f
    x = x0 * math.sin(w * t); v = x0 * w * math.cos(w * t)
    s = f'An object performs SHM with frequency {nf(f)} Hz and amplitude {nf(x0)} m. At time t = 0 it passes through the equilibrium position moving in the positive direction, so that x = x₀ sin ωt.'
    if D <= 3:
        return Q(s + f' Calculate its displacement at t = {nf(t)} s.', f'{nf(x, 3)} m', f'ω = 2πf = {f3(w)} rad s⁻¹ [1]; x = x₀ sin ωt with calculator in radians [1]; = {nf(x, 3)} m [1] [3]')
    return Q(s + f' (a) Calculate the displacement at t = {nf(t)} s. (b) Calculate the velocity at this time. (c) Calculate the first time after t = 0 at which the displacement is half the amplitude.',
             f'(a) {nf(x, 3)} m (b) {nf(v, 3)} m s⁻¹ (c) {f3((PI / 6) / w)} s', f'(a) x = x₀ sin ωt = {nf(x, 3)} m [1] (b) v = x₀ω cos ωt [1]; = {nf(v, 3)} m s⁻¹ [1] (c) sin ωt = 0.5, ωt = π/6 [1]; t = {f3((PI / 6) / w)} s [1] [5]', 'multi_step')


@t62.add('C3', (2, 3, 4), 'numerical')
def t62_pend(r, D):
    l = r.choice([0.25, 0.40, 0.60, 0.80, 1.0, 1.5]); amp = r.choice([0.020, 0.030, 0.050])
    w = math.sqrt(GR / l); T = 2 * PI / w
    return Q(f'For small oscillations a simple pendulum of length l performs SHM with ω² = g/l. A pendulum of length {nf(l)} m is displaced by {nf(amp)} m and released. Calculate the period and the maximum speed of the bob.' + (' Explain why the motion is only approximately simple harmonic.' if D >= 4 else ''),
             f'T = {f3(T)} s; v₀ = {nf(w * amp, 3)} m s⁻¹' + ('; restoring force ∝ sin θ, which is ≈ θ only for small angles' if D >= 4 else ''),
             f'ω = √(g/l) = {f3(w)} rad s⁻¹ [1]; T = 2π/ω = {f3(T)} s [1]; v₀ = ωx₀ = {nf(w * amp, 3)} m s⁻¹ [1]' + ('; sin θ ≈ θ only for small θ [1] [4]' if D >= 4 else ' [3]'))


def _shm_c4(r, D):
    m = r.choice([0.20, 0.40, 0.50]); k = r.choice([20.0, 40.0, 80.0]); x0 = r.choice([0.030, 0.040, 0.050])
    w = math.sqrt(k / m); T = 2 * PI / w
    intro = f'A trolley of mass {nf(m)} kg on a horizontal track is attached between two springs. When displaced by x, the resultant force on it is −{nf(k)}x (in N, with x in m). It is displaced by {nf(x0)} m and released.'
    parts = [
        lambda r: ('Show that the trolley performs simple harmonic motion.', f'a = F/m = −({nf(k)}/{nf(m)})x, so a ∝ −x: SHM with ω² = k/m.', 'a = −(k/m)x [1]; a ∝ −x so SHM [1] [2]'),
        lambda r: ('Calculate the angular frequency.', f'{f3(w)} rad s⁻¹', 'ω = √(k/m) [2]'),
        lambda r: ('Calculate the period.', f'{f3(T)} s', 'T = 2π/ω [1]'),
        lambda r: ('Calculate the maximum speed.', f'{nf(w * x0, 3)} m s⁻¹', 'v₀ = ωx₀ [2]'),
        lambda r: ('Calculate the maximum acceleration.', f'{f3(w * w * x0)} m s⁻²', 'a₀ = ω²x₀ [1]'),
        lambda r: ('State the displacement–time equation for the trolley, taking t = 0 at release.', f'x = {nf(x0)} cos({f3(w)}t)', 'cosine with correct x₀ and ω [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t62.add('C4', (2, 3, 4, 5), 'multi_step')(_shm_c4)

N63 = 'Energy changes in simple harmonic motion'
t63 = topic(N63, N63.lower(), 'energy changes in simple harmonic motion', 'energy in shm')
FX(t63, 'C1', (1, 2), [
    ('For an undamped simple harmonic oscillator, which quantity remains constant?', 'the total energy', 'KE and PE interchange; total is constant.', ['the kinetic energy', 'the potential energy', 'the speed']),
    ('The total energy of a simple harmonic oscillator of mass m, angular frequency ω and amplitude x₀ is', '½mω²x₀²', 'E = ½mv₀² with v₀ = ωx₀.', ['mω²x₀²', '½mωx₀', '½mω²x₀']),
    ('The amplitude of a simple harmonic oscillator is doubled. Its total energy becomes', 'four times as large', 'E ∝ x₀².', ['twice as large', 'half as large', 'unchanged']),
    ('At what displacement is the kinetic energy of an oscillator in SHM equal to its potential energy?', 'x₀/√2', '½mω²(x₀² − x²) = ½mω²x² ⇒ x² = x₀²/2.', ['x₀/2', 'x₀/4', '0']),
    ('How many times per cycle is the kinetic energy of a simple harmonic oscillator a maximum?', 'twice', 'At each pass through equilibrium.', ['once', 'four times', 'continuously']),
    ('The kinetic energy of an oscillator varies with time with a frequency that is', 'twice the frequency of the oscillation', 'KE peaks twice per cycle.', ['equal to the oscillation frequency', 'half the oscillation frequency', 'zero']),
    ('State an expression for the kinetic energy of an oscillator in SHM at displacement x.', 'Ek = ½mω²(x₀² − x²)', 'correct expression [1]'),
])
FX(t63, 'C2', (1, 2, 3, 4), [
    ('Describe the energy changes during one complete oscillation of a simple pendulum.', 'At maximum displacement the energy is all gravitational PE; as the bob swings to the centre PE is converted to KE (maximum at the centre); then KE back to PE on the other side, and the sequence repeats; total energy constant if undamped.', 'PE max at extremes, KE max at centre [1]; continuous interchange, total constant [1] [2]'),
    ('Explain why the graph of kinetic energy against displacement for SHM is an inverted parabola.', 'Ek = ½mω²(x₀² − x²): a quadratic in x with a negative x² term, maximum at x = 0 and zero at x = ±x₀.', 'Ek = ½mω²(x₀² − x²) [1]; quadratic, max at 0, zero at ±x₀ [1] [2]'),
    ('Explain why, in a real oscillator, the total energy decreases with time.', 'Resistive forces (air resistance, friction) do work against the motion, transferring energy to thermal energy of the surroundings; the amplitude decreases (damping).', 'resistive forces do work [1]; energy dissipated as thermal energy, amplitude falls [1] [2]'),
    ('Show that the maximum kinetic energy of a simple harmonic oscillator is ½mω²x₀².', 'Maximum speed v₀ = ωx₀, so Ek(max) = ½mv₀² = ½mω²x₀².', 'v₀ = ωx₀ [1]; substitute into ½mv² [1] [2]'),
])


@t63.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t63_energy(r, D):
    m = r.choice([0.050, 0.10, 0.20, 0.25, 0.40, 0.60, 1.5]); T = r.choice([0.40, 0.50, 0.80, 1.0, 1.2, 2.0]); x0 = r.choice([0.020, 0.030, 0.040, 0.050, 0.080])
    w = 2 * PI / T; Et = 0.5 * m * w * w * x0 * x0
    obj = r.choice(['A mass on a spring', 'A pendulum bob', 'A trolley between springs', 'A vibrating platform'])
    s = f'{obj} of mass {nf(m)} kg performs SHM with period {nf(T)} s and amplitude {nf(x0)} m.'
    if D <= 2:
        return numq(r, D, s, 'total energy of the oscillation', Et, ' J', f'E = ½mω²x₀² = ½ × {nf(m)} × (2π/{nf(T)})² × {nf(x0)}²', [m * w * w * x0 * x0, 0.5 * m * w * x0 * x0, 0.5 * m * w * w * x0], fm=lambda x: E(x, 3))
    x = x0 * r.choice([0.25, 0.4, 0.5, 0.6, 0.75])
    Ek = 0.5 * m * w * w * (x0 ** 2 - x ** 2); Ep = Et - Ek
    if D == 3:
        return Q(s + f' Calculate the kinetic energy and the potential energy when the displacement is {nf(x, 3)} m.', f'Ek = {E(Ek)} J; Ep = {E(Ep)} J',
                 f'ω = 2π/T [1]; Ek = ½mω²(x₀² − x²) = {E(Ek)} J [1]; Ep = E − Ek = {E(Ep)} J [1] [3]')
    return Q(s + f' (a) Calculate the total energy. (b) Calculate the kinetic energy at displacement {nf(x, 3)} m. (c) The amplitude decays to {nf(x0 * 0.6, 3)} m because of damping. Calculate the percentage of the original energy that has been dissipated.',
             f'(a) {E(Et)} J (b) {E(Ek)} J (c) 64%', f'(a) E = ½mω²x₀² = {E(Et)} J [1] (b) Ek = ½mω²(x₀² − x²) [1]; = {E(Ek)} J [1] (c) E ∝ x₀², 0.6² = 0.36 [1]; 64% dissipated [1] [5]', 'multi_step')


relation(t63, 'C2', (2, 3), 'E = ½mω²x₀²', 'total energy of the oscillation', {'amplitude': 2, 'frequency': 2, 'mass': 1},
         ['A mass–spring system oscillates with simple harmonic motion.', 'A vibrating platform used for testing components performs SHM.', 'An undamped oscillator is modelled in a computer simulation.'])


def _en_c4(r, D):
    m = r.choice([0.15, 0.30, 0.50]); f = r.choice([1.5, 2.0, 2.5]); x0 = r.choice([0.040, 0.050, 0.060])
    w = 2 * PI * f; Et = 0.5 * m * w * w * x0 * x0
    intro = f'A mass of {nf(m)} kg on a spring oscillates with SHM at {nf(f)} Hz with amplitude {nf(x0)} m. Damping is negligible.'
    parts = [
        lambda r: ('Calculate the maximum speed.', f'{nf(w * x0, 3)} m s⁻¹', 'v₀ = 2πf x₀ [2]'),
        lambda r: ('Calculate the total energy of the oscillations.', f'{E(Et)} J', 'E = ½mv₀² [2]'),
        lambda r: ('Calculate the displacement at which the kinetic energy equals the potential energy.', f'{nf(x0 / math.sqrt(2), 3)} m', 'x = x₀/√2 [2]'),
        lambda r: ('Describe how the kinetic energy varies with displacement.', 'Maximum at x = 0, falling to zero at ±x₀ along an inverted parabola, Ek = ½mω²(x₀² − x²).', 'max at 0, zero at ±x₀ [1]; parabolic shape [1] [2]'),
        lambda r: ('State the frequency at which the kinetic energy varies.', f'{nf(2 * f)} Hz', 'twice oscillation frequency [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t63.add('C4', (2, 3, 4, 5), 'multi_step')(_en_c4)

N64 = 'Damping, forced oscillations and resonance'
t64 = topic(N64, N64.lower(), 'damping', 'resonance')
FX(t64, 'C1', (1, 2), [
    ('What is meant by damping of an oscillation?', 'the loss of energy and reduction of amplitude due to resistive forces', 'Resistive forces remove energy from the oscillator.', ['an increase in frequency due to an external force', 'the oscillation of a system at its natural frequency', 'the transfer of energy to the oscillator by a driver']),
    ('Which describes critical damping?', 'the system returns to equilibrium in the shortest time without oscillating', 'Critical damping: fastest return, no overshoot.', ['the amplitude decreases slowly over many oscillations', 'the system oscillates with increasing amplitude', 'the system returns very slowly without oscillating']),
    ('Resonance occurs when', 'the driving frequency equals the natural frequency of the oscillator', 'Maximum amplitude at f = f₀.', ['the driving frequency is twice the natural frequency', 'the damping is critical', 'the amplitude of the driver is a maximum']),
    ('Increasing the damping of a driven oscillator', 'reduces the peak amplitude and makes the resonance peak flatter', 'More damping: lower, broader peak, slightly lower resonant frequency.', ['increases the peak amplitude', 'makes the peak sharper', 'has no effect on the amplitude']),
    ('A car suspension is designed to be', 'critically damped', 'Returns to equilibrium quickly without bouncing.', ['lightly damped', 'undamped', 'heavily overdamped']),
    ('A forced oscillator has reached a steady state. Its frequency is', 'equal to the driving frequency', 'Forced oscillations occur at the driver\'s frequency.', ['equal to its natural frequency', 'zero', 'half the driving frequency']),
    ('State one useful application of resonance.', 'e.g. tuning a radio circuit; microwave heating of water; MRI; musical instruments.', 'valid example [1]'),
    ('State what is meant by the natural frequency of a system.', 'The frequency at which it oscillates freely after being displaced (no driving force).', 'free oscillation frequency [1]'),
])
FX(t64, 'C2', (1, 2, 3, 4), [
    ('Distinguish between light damping, critical damping and heavy damping.', 'Light: oscillates with amplitude decreasing gradually. Critical: returns to equilibrium in the shortest time without oscillating. Heavy: returns very slowly without oscillating.', 'light correct [1]; critical and heavy distinguished [1] [2]'),
    ('Explain how resonance can cause damage to a bridge and how engineers reduce the risk.', 'If periodic forces (wind vortices, marching) have a frequency equal to the natural frequency, energy is transferred efficiently and the amplitude becomes very large, causing damage. Engineers add damping (dampers) or change the natural frequency (stiffness).', 'driving frequency = natural frequency, large amplitude [1]; damping or change natural frequency [1] [2]'),
    ('Explain why, at resonance, the amplitude of a forced oscillator is limited by damping.', 'At resonance energy is transferred most efficiently; the amplitude rises until the energy lost per cycle to damping equals the energy supplied per cycle, so more damping gives a smaller maximum amplitude.', 'maximum energy transfer at resonance [1]; energy loss balances input [1] [2]'),
    ('Describe how the amplitude of a lightly damped forced oscillator varies as the driving frequency is increased from zero to well above the natural frequency.', 'Amplitude starts small (about the driver amplitude), rises to a sharp maximum at (just below) the natural frequency, then falls towards zero at high frequencies.', 'rises to peak at natural frequency [1]; falls at higher frequency [1] [2]'),
    ('Explain why soldiers are ordered to break step when crossing a bridge.', 'Marching in step applies a periodic force; if its frequency matches a natural frequency of the bridge, resonance gives large-amplitude oscillations that could damage it.', 'periodic force at a frequency [1]; resonance, large amplitude [1] [2]'),
])


@t64.add('C3', (1, 2, 3, 4, 5), 'case')
def t64_decay(r, D):
    A0 = r.choice([8.0, 10.0, 12.0, 15.0, 20.0]); k = r.choice([0.80, 0.85, 0.90, 0.95])
    n = r.choice([3, 4, 5])
    An = A0 * k ** n
    who = person(r)
    s = f'{who} records the amplitude of a lightly damped pendulum. The amplitude falls by the same fraction every cycle: it is {nf(A0)} cm initially and {nf(A0 * k, 3)} cm after one cycle.'
    if D <= 2:
        return numq(r, D, s, f'amplitude after {n} cycles', An, ' cm', f'ratio = {nf(k)} per cycle; A = {nf(A0)} × {nf(k)}^{n}', [A0 - n * (A0 - A0 * k), A0 * k * n, A0 * k ** (n - 1)], fm=lambda x: nf(x, 3))
    Er = k * k
    if D == 3:
        return Q(s + f' Calculate the amplitude after {n} cycles and the fraction of the original energy remaining.', f'{nf(An, 3)} cm; {nf((k ** n) ** 2, 3)}',
                 f'A = A₀ × {nf(k)}^{n} = {nf(An, 3)} cm [1]; E ∝ A² [1]; fraction = {nf((k ** n) ** 2, 3)} [1] [3]')
    return Q(s + f' (a) Calculate the percentage of the energy lost in each cycle. (b) Calculate the amplitude after {n} cycles. (c) Explain whether the period changes as the amplitude decreases.',
             f'(a) {nf(100 * (1 - Er), 3)}% (b) {nf(An, 3)} cm (c) essentially no: for light damping the period is (almost) independent of amplitude', f'(a) E ∝ A², ratio {nf(Er, 3)} [1]; {nf(100 * (1 - Er), 3)}% [1] (b) {nf(An, 3)} cm [1] (c) period ≈ constant [1]; SHM period independent of amplitude [1] [5]', 'multi_step')


@t64.add('C2', (2, 3, 4), 'explain')
def t64_ex(r, D):
    sit, ans = r.choice([('a washing machine shakes violently at one particular spin speed but runs smoothly at higher speeds', 'At that speed the driving frequency (drum rotation) equals the natural frequency of the machine on its mountings, so resonance occurs; at other speeds the amplitude is small.'),
                         ('a wine glass can be shattered by a loud note of one particular pitch', 'The note\'s frequency equals the natural frequency of the glass; resonance gives a large-amplitude vibration that strains the glass beyond breaking.'),
                         ('a car\'s shock absorbers make it stop bouncing after going over a bump', 'They provide (near-)critical damping, removing energy so the body returns to equilibrium quickly without oscillating.'),
                         ('tall buildings in earthquake zones are fitted with large tuned mass dampers', 'They absorb energy at the building\'s natural frequency, increasing damping and reducing the resonant amplitude when ground motion is at that frequency.'),
                         ('a child on a swing goes higher when pushed once per swing at the right moment', 'The pushes are at the natural frequency of the swing (resonance), so energy is added efficiently each cycle and the amplitude grows.'),
                         ('a microwave oven heats food', 'The microwave frequency is close to a natural frequency of rotation of water molecules, so they absorb energy by resonance and the food heats up.')])
    return Q(f'Explain why {sit}.', ans, 'identifies resonance or damping correctly [1]; links frequency/energy transfer to the effect [1]' + ('; uses terms natural and driving frequency correctly [1] [3]' if D >= 3 else ' [2]'))


def _res_c4(r, D):
    f0 = r.choice([2.0, 3.5, 5.0, 8.0])
    intro = ctx(r, ['A footbridge in {c} has a natural frequency of {f} Hz.', 'A model building on a shaking table in {c} has a natural frequency of {f} Hz.', 'A vibration-testing rig in {c} drives a metal strip with a natural frequency of {f} Hz.'], f=nf(f0))
    parts = [
        lambda r: ('State what is meant by resonance.', 'Maximum amplitude of forced oscillations when the driving frequency equals the natural frequency.', 'max amplitude [1]; driving = natural frequency [1] [2]'),
        lambda r: (f'Calculate the period of a driving force that would cause resonance.', f'{nf(1 / f0, 3)} s', 'T = 1/f₀ [1]'),
        lambda r: ('Sketch-describe a graph of amplitude against driving frequency for light damping.', f'Low at low frequency, sharp peak at about {nf(f0)} Hz, falling towards zero at high frequency.', 'peak at f₀ [1]; correct shape either side [1] [2]'),
        lambda r: ('Describe the effect of increasing the damping on the graph.', 'Peak amplitude lower, peak broader and slightly shifted to lower frequency.', 'lower [1]; broader / shift [1] [2]'),
        lambda r: ('Suggest one way engineers could reduce the risk of damage from resonance.', 'Fit dampers to increase damping, or change the stiffness/mass to move the natural frequency away from likely driving frequencies.', 'valid method [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t64.add('C4', (2, 3, 4, 5), 'multi_step')(_res_c4)
CHAPTERS[6] = [t61, t62, t63, t64]

# ===================================================================== 7 Electric fields
N71 = 'Electric fields and field strength E = F/q and field lines'
t71 = topic(N71, N71.lower(), 'electric fields', 'field strength e = f/q')
FX(t71, 'C1', (1, 2), [
    ('Which is the definition of electric field strength at a point?', 'the force per unit positive charge on a small charge placed at the point', 'E = F/q.', ['the force per unit mass at the point', 'the work done per unit charge bringing a charge from infinity', 'the charge per unit area at the point']),
    ('What is the unit of electric field strength?', 'N C⁻¹', 'E = F/q; equivalent to V m⁻¹.', ['C N⁻¹', 'J C⁻¹', 'N C']),
    ('An electron is placed in an electric field directed to the right. In which direction is the force on the electron?', 'to the left', 'Negative charge experiences a force opposite to the field.', ['to the right', 'upwards', 'there is no force']),
    ('A charge of 4.0 μC experiences a force of 0.020 N in an electric field. What is the field strength?', '5000 N C⁻¹', 'E = F/q = 0.020/4.0 × 10⁻⁶.', ['8.0 × 10⁻⁸ N C⁻¹', '200 N C⁻¹', '50 N C⁻¹']),
    ('Electric field lines start on', 'positive charges and end on negative charges', 'Field direction is that of the force on a positive charge.', ['negative charges and end on positive charges', 'neutral objects', 'any conductor']),
    ('Which unit is equivalent to N C⁻¹?', 'V m⁻¹', 'E = V/d.', ['V m', 'J m⁻¹', 'C V⁻¹']),
    ('State what is meant by an electric field.', 'A region of space in which a charge experiences a force.', 'region where charge experiences force [1]'),
])
FX(t71, 'C2', (1, 2, 3, 4), [
    ('Compare electric fields with gravitational fields, giving one similarity and one difference.', 'Similarity: both are inverse-square fields for point sources / field strength defined as force per unit (charge/mass). Difference: gravitational forces are always attractive; electric forces can attract or repel.', 'valid similarity [1]; valid difference [1] [2]'),
    ('Explain why the field lines near the surface of a charged conductor are perpendicular to the surface.', 'If the field had a component along the surface, free charges would move; in equilibrium they do not, so the field must be perpendicular to the surface.', 'parallel component would move charges [1]; static so perpendicular [1] [2]'),
    ('Describe the field pattern between two parallel plates with a p.d. between them, including the edges.', 'Between the plates: parallel, equally spaced lines from + to − plate (uniform field); near the edges the lines curve outwards (edge effect).', 'uniform parallel lines + to − [1]; curving at edges [1] [2]'),
    ('Explain why the force on a positive charge in an electric field is in the direction of the field lines.', 'By definition field lines show the direction of the force on a small positive test charge.', 'definition of field direction [1]; positive test charge [1] [2]'),
])


@t71.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t71_force(r, D):
    part, q, m = r.choice([('an electron', -QE, ME), ('a proton', QE, MP), ('an α-particle', 2 * QE, 6.64e-27), ('an oil drop carrying a charge of 5e', 5 * QE, 3.2e-15), ('a dust particle with charge 8.0 × 10⁻¹⁷ C', 8.0e-17, 2.0e-14)])
    Ef = r.choice([2.0e3, 5.0e3, 1.2e4, 2.5e4, 5.0e4, 1.0e5])
    F = abs(q) * Ef; a = F / m
    s = f'{cap(part)} is in a uniform electric field of strength {sc(Ef, 2)} N C⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'magnitude of the electric force on it', F, ' N', f'F = qE = {sc(abs(q))} × {sc(Ef, 2)}', [Ef / abs(q), F * 2, F / 10], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(s + ' Calculate the electric force on it and its acceleration (ignore gravity).', f'F = {sc(F)} N; a = {sc(a)} m s⁻²',
                 f'F = qE = {sc(F)} N [1]; a = F/m [1]; = {sc(a)} m s⁻² [1] [3]')
    W = m * GR
    return Q(s + ' (a) Calculate the electric force on it. (b) Calculate its weight and hence explain whether gravity may be ignored. (c) State the direction of the force if the field is vertically upwards.',
             f'(a) {sc(F)} N (b) {sc(W)} N; ratio F/W = {sc(F / W)}' + (', so gravity is negligible' if F / W > 100 else ', so gravity is NOT negligible') + f' (c) {"upwards" if q > 0 else "downwards"}',
             f'(a) F = qE = {sc(F)} N [1] (b) W = mg = {sc(W)} N [1]; comparison and conclusion [1] (c) {"upwards (positive charge)" if q > 0 else "downwards (negative charge)"} [1] [4]', 'multi_step')


@t71.add('C2', (2, 3, 4), 'explain')
def t71_pattern(r, D):
    a, b = r.choice([('an isolated positive point charge', 'radial lines pointing outwards, closer together near the charge'), ('an isolated negative point charge', 'radial lines pointing inwards, closer together near the charge'),
                     ('two equal positive point charges', 'lines leave both charges and bend away from each other, with a neutral point midway where there are no lines'),
                     ('a positive and an equal negative point charge', 'lines curve from the positive to the negative charge, densest between them'),
                     ('a positively charged sphere above an earthed plate', 'lines leave the sphere radially and curve to meet the plate at right angles'),
                     ('two parallel plates at different potentials', 'parallel, equally spaced lines from the positive to the negative plate, curving outwards at the edges')])
    return Q(f'Describe the electric field pattern for {a}, and state what the spacing of the lines indicates.', cap(b) + '; closer lines indicate a stronger field.',
             'correct shape [1]; correct direction [1]' + ('; spacing ↔ field strength [1] [3]' if D >= 3 else ' [2]'))


def _ef_c4(r, D):
    q = r.choice([2.0e-9, 5.0e-9, 1.2e-8]); F = r.choice([4.0e-5, 6.0e-5, 1.5e-4])
    Ef = F / q
    intro = f'A small charged sphere carrying +{sc(q, 2)} C experiences a force of {sc(F, 2)} N when placed at point P near a charged object.'
    parts = [
        lambda r: ('Define electric field strength.', 'Force per unit positive charge on a small test charge.', 'force per unit positive charge [1]'),
        lambda r: ('Calculate the field strength at P.', f'{sc(Ef)} N C⁻¹', 'E = F/q [2]'),
        lambda r: ('The sphere is replaced by an electron. Calculate the force on the electron.', f'{sc(Ef * QE)} N, in the opposite direction', 'F = eE [1]; opposite direction [1] [2]'),
        lambda r: ('Explain why the test charge should be small.', 'So that it does not disturb the field (the charges producing it) that is being measured.', 'does not alter field [1]'),
        lambda r: ('Show that N C⁻¹ is equivalent to V m⁻¹.', 'V m⁻¹ = J C⁻¹ m⁻¹ = N m C⁻¹ m⁻¹ = N C⁻¹.', 'V = J C⁻¹ [1]; J = N m [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t71.add('C4', (2, 3, 4, 5), 'multi_step')(_ef_c4)

N72 = 'Uniform electric fields E = ΔV/Δd and motion of charges in a field'
t72 = topic(N72, N72.lower(), 'uniform electric fields', 'motion of charges in a field')
FX(t72, 'C1', (1, 2), [
    ('Two parallel plates 2.0 cm apart have a p.d. of 500 V between them. What is the field strength between them?', '2.5 × 10⁴ V m⁻¹', 'E = V/d = 500/0.020.', ['250 V m⁻¹', '1.0 × 10⁴ V m⁻¹', '1.0 × 10⁻⁴ V m⁻¹']),
    ('An electron is accelerated from rest through a p.d. of 200 V. What kinetic energy does it gain?', '3.2 × 10⁻¹⁷ J', 'Ek = eV = 1.60 × 10⁻¹⁹ × 200.', ['200 J', '8.0 × 10⁻²² J', '1.6 × 10⁻¹⁹ J']),
    ('An electron enters a uniform electric field between horizontal plates, moving horizontally. Its path between the plates is', 'a parabola', 'Constant force perpendicular to initial velocity, like a projectile.', ['a circle', 'a straight line', 'a spiral']),
    ('The p.d. between two parallel plates is kept constant and the separation is doubled. The field strength', 'halves', 'E = V/d.', ['doubles', 'is unchanged', 'quadruples']),
    ('A proton and an electron are in the same uniform electric field. Which statement is correct?', 'the forces on them are equal in magnitude but opposite in direction', 'F = eE for both; opposite signs.', ['the accelerations are equal in magnitude', 'the force on the proton is larger', 'the force on the electron is zero']),
    ('A charged oil drop is held stationary between horizontal plates. Which equation applies?', 'qV/d = mg', 'Electric force balances weight.', ['qVd = mg', 'qd/V = mg', 'q = mgV']),
    ('State the equation for the field strength between parallel plates.', 'E = V/d (p.d. divided by separation).', 'E = ΔV/Δd [1]'),
])
FX(t72, 'C2', (1, 2, 3, 4), [
    ('Explain why the path of an electron moving horizontally into the uniform vertical field between two charged plates is parabolic.', 'The force eE is constant and vertical, so there is constant vertical acceleration; the horizontal velocity is constant (no horizontal force). This is the same as projectile motion, giving a parabola.', 'constant vertical force/acceleration [1]; constant horizontal velocity → parabola [1] [2]'),
    ('Explain why the kinetic energy gained by a charge accelerated through a p.d. does not depend on the separation of the plates.', 'Work done = qV; a larger separation gives a smaller field (E = V/d) but a longer distance, so qEd = qV is the same.', 'W = qV [1]; E smaller but distance larger [1] [2]'),
    ('Explain how a uniform electric field can be used to measure the charge on an oil drop.', 'Adjust the p.d. until the drop is stationary: qV/d = mg. Knowing m (from its terminal velocity) and V, d, the charge q = mgd/V can be found.', 'balance: qE = mg [1]; q = mgd/V with m known [1] [2]'),
    ('Explain why electrons in a cathode-ray tube can be treated as unaffected by gravity in the deflecting field.', 'The electric force eE is many orders of magnitude greater than the weight mₑg (mass is tiny), so gravity is negligible.', 'compare eE with mg [1]; weight negligible [1] [2]'),
])


@t72.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t72_plates(r, D):
    V = r.choice([200.0, 400.0, 600.0, 1200.0, 2500.0, 5000.0]); d = r.choice([0.010, 0.015, 0.020, 0.040, 0.050])
    Ef = V / d; F = QE * Ef; a = F / ME
    s = f'Two parallel metal plates are {nf(d * 100)} cm apart with a p.d. of {nf(V)} V between them. An electron is between the plates.'
    if D <= 2:
        return numq(r, D, s, 'electric field strength between the plates', Ef, ' V m⁻¹', f'E = V/d = {nf(V)}/{nf(d)}', [V * d, V / (d * 100), Ef / 2], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the field strength, the force on the electron and its acceleration.', f'E = {E(Ef)} V m⁻¹; F = {sc(F)} N; a = {sc(a)} m s⁻²',
                 f'E = V/d = {E(Ef)} V m⁻¹ [1]; F = eE = {sc(F)} N [1]; a = F/m = {sc(a)} m s⁻² [1] [3]')
    v = math.sqrt(2 * QE * V / ME)
    return Q(s + ' The electron is released from rest at the negative plate. (a) Calculate the force on the electron. (b) Calculate the kinetic energy it gains in crossing to the positive plate. (c) Calculate its speed on reaching the positive plate.',
             f'(a) {sc(F)} N (b) {sc(QE * V)} J (c) {sc(v)} m s⁻¹', f'(a) F = eV/d = {sc(F)} N [1] (b) Ek = eV [1]; = {sc(QE * V)} J [1] (c) ½mv² = eV [1]; v = {sc(v)} m s⁻¹ [1] [5]', 'multi_step')


@t72.add('C3', (3, 4, 5), 'numerical')
def t72_deflect(r, D):
    v = r.choice([2.0e7, 3.0e7, 4.0e7]); L = r.choice([0.040, 0.050, 0.060]); V = r.choice([100.0, 150.0, 200.0, 300.0]); d = r.choice([0.020, 0.025, 0.030])
    a = QE * V / (d * ME); t = L / v; y = 0.5 * a * t * t
    if y > d / 2:
        return None
    s = f'An electron moving horizontally at {sc(v, 2)} m s⁻¹ enters the uniform field between two horizontal plates {nf(L * 100)} cm long and {nf(d * 100)} cm apart, midway between them. The p.d. between the plates is {nf(V)} V.'
    if D == 3:
        return Q(s + ' Calculate the time spent between the plates and the vertical acceleration.', f't = {sc(t)} s; a = {sc(a)} m s⁻²', f't = L/v = {sc(t)} s [1]; a = eV/(md) [1]; = {sc(a)} m s⁻² [1] [3]')
    return Q(s + ' (a) Calculate the time spent between the plates. (b) Calculate the vertical acceleration. (c) Calculate the vertical deflection on leaving the plates and state whether the electron hits a plate.',
             f'(a) {sc(t)} s (b) {sc(a)} m s⁻² (c) {E(y)} m; it does not hit a plate (deflection < {nf(d / 2)} m)', f'(a) t = L/v [1] (b) a = eE/m with E = V/d [1]; = {sc(a)} m s⁻² [1] (c) y = ½at² = {E(y)} m [1]; compared with half separation [1] [5]', 'multi_step')


@t72.add('C3', (2, 3, 4), 'numerical')
def t72_drop(r, D):
    m = r.choice([1.6e-15, 3.2e-15, 4.9e-15, 6.5e-15]); d = r.choice([0.010, 0.012, 0.015]); n = r.choice([2, 3, 4, 5, 6])
    V = m * GR * d / (n * QE)
    return Q(f'An oil drop of mass {sc(m, 2)} kg is held stationary between two horizontal plates {nf(d * 1000)} mm apart when the p.d. between them is {nf(V, 3)} V. Calculate the charge on the drop and the number of excess electrons it carries.',
             f'q = {sc(n * QE)} C; {n} electrons', f'qV/d = mg [1]; q = mgd/V = {sc(n * QE)} C [1]; n = q/e = {n} [1]' + (' [3]' if D <= 3 else '; upper plate positive since the drop is negative [1] [4]'))


def _uf_c4(r, D):
    V = r.choice([1500.0, 2000.0, 3000.0])
    v = math.sqrt(2 * QE * V / ME)
    intro = f'In an electron gun, electrons are accelerated from rest through a p.d. of {nf(V)} V between a cathode and an anode {r.choice([2.0, 3.0, 4.0])} cm apart.'
    parts = [
        lambda r: ('Calculate the kinetic energy of each electron leaving the anode.', f'{sc(QE * V)} J', 'Ek = eV [1]'),
        lambda r: ('Calculate the speed of the electrons.', f'{sc(v)} m s⁻¹', '½mv² = eV [2]'),
        lambda r: ('Explain why the speed does not depend on the distance between cathode and anode.', 'The work done (eV) depends only on the p.d.; a larger gap gives a weaker field over a longer distance.', 'W = eV only [1]'),
        lambda r: ('The beam then enters a vertical uniform field. Describe the shape of the path in the field.', 'Parabolic: constant velocity horizontally, constant acceleration vertically.', 'parabola [1]; constant horizontal velocity and constant vertical acceleration [1] [2]'),
        lambda r: ('Explain why the electrons travel in a vacuum.', 'So they do not collide with gas molecules and lose energy or scatter.', 'avoid collisions [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t72.add('C4', (2, 3, 4, 5), 'multi_step')(_uf_c4)

N73 = "Coulomb's law and field strength of a point charge"
t73 = topic(N73, N73.lower(), "coulomb's law", 'field strength of a point charge')
FX(t73, 'C1', (1, 2), [
    ('Two point charges repel with force F. The distance between them is tripled. The new force is', 'F/9', 'F ∝ 1/r².', ['F/3', '3F', '9F']),
    ('Which expression gives the electric field strength at distance r from a point charge Q?', 'Q/(4πε₀r²)', 'E = F/q = Q/(4πε₀r²).', ['Q/(4πε₀r)', 'Qq/(4πε₀r²)', '4πε₀Q/r²']),
    ('Both charges in a pair of point charges are doubled at the same separation. The force between them', 'becomes four times larger', 'F ∝ Qq.', ['doubles', 'is unchanged', 'halves']),
    ('What is the constant 1/(4πε₀) approximately equal to?', '8.99 × 10⁹ N m² C⁻²', 'ε₀ = 8.85 × 10⁻¹² F m⁻¹.', ['8.85 × 10⁻¹² N m² C⁻²', '6.67 × 10⁻¹¹ N m² C⁻²', '1.60 × 10⁻¹⁹ N m² C⁻²']),
    ('Outside a charged conducting sphere, the field is the same as that of', 'a point charge at the centre of the sphere', 'Charge on a sphere acts as if concentrated at the centre for outside points.', ['a uniform field', 'a point charge on the surface', 'zero field']),
    ('Two charges of +Q and −Q are a distance d apart. At the midpoint, the electric field is', 'directed towards −Q', 'Both contributions point from + towards −.', ['zero', 'directed towards +Q', 'perpendicular to the line joining them']),
    ('State Coulomb\'s law.', 'The force between two point charges is proportional to the product of the charges and inversely proportional to the square of their separation.', '∝ product of charges [1]; ∝ 1/r² [1] [2]'),
])
FX(t73, 'C2', (1, 2, 3, 4), [
    ('Explain why the gravitational force between a proton and an electron in an atom can be neglected compared with the electric force.', 'The electric force is about 10³⁹ times larger, because e²/(4πε₀) is enormous compared with Gmₚmₑ; both depend on 1/r² so the ratio is independent of distance.', 'ratio ~10³⁹ [1]; same r dependence so ratio fixed [1] [2]'),
    ('Explain why there is a point between two positive charges where the electric field strength is zero, and why it is closer to the smaller charge.', 'The fields from the two charges point in opposite directions between them; they cancel where Q₁/r₁² = Q₂/r₂². For the smaller charge to give an equal field, the point must be closer to it.', 'fields opposite in direction between charges [1]; equal magnitude closer to smaller charge [1] [2]'),
    ('Derive the expression for the field strength of a point charge from Coulomb\'s law.', 'Force on test charge q at distance r: F = Qq/(4πε₀r²). E = F/q = Q/(4πε₀r²).', 'Coulomb\'s law for test charge [1]; divide by q [1] [2]'),
    ('Compare the electric field of a point charge with the gravitational field of a point mass.', 'Both are radial and inverse-square (E = Q/4πε₀r², g = GM/r²). Gravitational fields are always attractive (towards the mass); electric fields point away from positive charges and towards negative charges.', 'both radial inverse square [1]; attraction only vs attraction/repulsion [1] [2]'),
])
relation(t73, 'C2', (2, 3), 'F = Qq/(4πε₀r²)', 'electrostatic force between them', {'separation': -2, 'charge on one sphere': 1},
         ['Two small charged spheres are held near each other.', 'Two charged dust particles in a cloud interact.', 'Two charged polystyrene balls hang near each other on threads.'])


@t73.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t73_coul(r, D):
    q1 = r.choice([2.0e-9, 4.5e-9, 8.0e-9, 1.5e-8, 3.0e-6, 5.0e-6]); q2 = r.choice([1.0e-9, 3.0e-9, 6.0e-9, 2.0e-6]); d = r.choice([0.020, 0.050, 0.10, 0.15, 0.30])
    F = KC * q1 * q2 / d ** 2
    s = f'Two small charged spheres carry charges of +{sc(q1, 2)} C and −{sc(q2, 2)} C. Their centres are {nf(d * 100)} cm apart.'
    if D <= 2:
        return numq(r, D, s, 'force between them', F, ' N', f'F = Qq/(4πε₀r²) = 8.99 × 10⁹ × {sc(q1, 2)} × {sc(q2, 2)}/{nf(d)}²', [KC * q1 * q2 / d, F * 100 ** 2, F * 4], fm=lambda x: E(x, 3))
    Ep = KC * q1 / (d / 2) ** 2 + KC * q2 / (d / 2) ** 2
    if D == 3:
        return Q(s + ' Calculate the force between them and state whether it is attractive or repulsive.', f'{E(F)} N, attractive', f'F = Qq/(4πε₀r²) [1]; = {E(F)} N [1]; attractive (opposite charges) [1] [3]')
    return Q(s + ' (a) Calculate the force between them. (b) Calculate the electric field strength at the midpoint between them and state its direction. (c) The separation is halved. State the new force.',
             f'(a) {E(F)} N (b) {sc(Ep)} N C⁻¹, towards the negative charge (c) {E(4 * F)} N', f'(a) F = {E(F)} N [1] (b) E from each = Q/(4πε₀(r/2)²) [1]; fields add: {sc(Ep)} N C⁻¹ towards − [1] (c) F ∝ 1/r² [1]; {E(4 * F)} N [1] [5]', 'multi_step')


@t73.add('C3', (2, 3, 4, 5), 'numerical')
def t73_sphere(r, D):
    R = r.choice([0.050, 0.10, 0.15, 0.20]); Q_ = r.choice([2.0e-8, 5.0e-8, 1.0e-7, 3.0e-7]); k = r.choice([2, 3, 4])
    Es = KC * Q_ / R ** 2; Ek = Es / k ** 2
    s = f'An isolated conducting sphere of radius {nf(R * 100)} cm carries a charge of {sc(Q_, 2)} C.'
    if D <= 3:
        return Q(s + f' Calculate the electric field strength at the surface and at a distance of {nf(k * R * 100)} cm from the centre.', f'{sc(Es)} N C⁻¹; {sc(Ek)} N C⁻¹',
                 f'E = Q/(4πε₀r²) [1]; surface {sc(Es)} N C⁻¹ [1]; at {k}R: ÷{k * k} = {sc(Ek)} N C⁻¹ [1] [3]')
    Qmax = 3.0e6 * R ** 2 / KC
    return Q(s + f' (a) Calculate the field strength at the surface. (b) Air breaks down when the field exceeds 3.0 × 10⁶ V m⁻¹. Calculate the maximum charge the sphere can hold. (c) Explain why the field inside the conducting sphere is zero.',
             f'(a) {sc(Es)} N C⁻¹ (b) {sc(Qmax)} C (c) charges move to the surface; in equilibrium there is no field inside a conductor', f'(a) E = Q/(4πε₀R²) = {sc(Es)} N C⁻¹ [1] (b) Q = 4πε₀R²E [1]; = {sc(Qmax)} C [1] (c) charges reside on surface [1]; no field inside in equilibrium [1] [5]', 'multi_step')


@t73.add('C3', (3, 4, 5), 'numerical')
def t73_null(r, D):
    q1 = r.choice([2.0, 4.0, 9.0]) * 1e-9; q2 = r.choice([1.0, 3.0, 16.0]) * 1e-9; d = r.choice([0.10, 0.20, 0.30])
    x = d / (1 + math.sqrt(q2 / q1))
    return Q(f'Two positive point charges of {sc(q1, 2)} C and {sc(q2, 2)} C are fixed {nf(d * 100)} cm apart. Calculate the distance from the {sc(q1, 2)} C charge to the point between them where the electric field strength is zero.',
             f'{nf(x * 100, 3)} cm', f'Q₁/x² = Q₂/(d − x)² [1]; x/(d − x) = √(Q₁/Q₂) [1]; x = {nf(x * 100, 3)} cm [1]' + (' [3]' if D == 3 else '; explanation that fields are in opposite directions between like charges [1] [4]'))


def _coul_c4(r, D):
    rr = 5.3e-11
    F = KC * QE * QE / rr ** 2; Fg = GG * MP * ME / rr ** 2
    intro = 'In a simple model of the hydrogen atom, an electron orbits a proton in a circle of radius 5.3 × 10⁻¹¹ m.'
    parts = [
        lambda r: ('Calculate the electric force between the electron and the proton.', f'{sc(F)} N', 'F = e²/(4πε₀r²) [2]'),
        lambda r: ('Calculate the gravitational force between them.', f'{sc(Fg)} N', 'F = Gmₚmₑ/r² [2]'),
        lambda r: ('Calculate the ratio of the electric force to the gravitational force.', f'{sc(F / Fg)}', 'ratio [1]'),
        lambda r: ('Calculate the electric field strength due to the proton at the electron.', f'{sc(KC * QE / rr ** 2)} N C⁻¹', 'E = e/(4πε₀r²) [2]'),
        lambda r: ('Calculate the speed of the electron, assuming the electric force provides the centripetal force.', f'{sc(math.sqrt(F * rr / ME))} m s⁻¹', 'F = mv²/r [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t73.add('C4', (2, 3, 4, 5), 'multi_step')(_coul_c4)

N74 = 'Electric potential V = Q/4πε₀r and electric potential energy'
t74 = topic(N74, N74.lower(), 'electric potential', 'electric potential energy')
FX(t74, 'C1', (1, 2), [
    ('Which is the definition of electric potential at a point?', 'the work done per unit positive charge in bringing a small test charge from infinity to the point', 'V = W/q from infinity.', ['the force per unit charge at the point', 'the work done in moving a charge between two plates', 'the energy stored per unit volume']),
    ('The electric potential at distance r from a point charge is V. At distance 2r it is', 'V/2', 'V ∝ 1/r.', ['V/4', '2V', '4V']),
    ('What is the electric potential energy of two charges Q and q a distance r apart?', 'Qq/(4πε₀r)', 'Ep = qV.', ['Qq/(4πε₀r²)', 'Q/(4πε₀r)', '4πε₀Qq/r']),
    ('The electric field strength is related to the potential gradient by', 'E = −dV/dr', 'Field strength is the negative of potential gradient.', ['E = dV/dr', 'E = V × r', 'E = −V/r²']),
    ('The potential near an isolated negative point charge is', 'negative, becoming more negative closer to the charge', 'V = Q/(4πε₀r) with Q < 0.', ['positive, increasing closer to the charge', 'zero everywhere', 'negative, becoming less negative closer to the charge']),
    ('What is the unit of electric potential?', 'V (J C⁻¹)', 'Work per unit charge.', ['N C⁻¹', 'J', 'C J⁻¹']),
    ('State the work done in moving a charge along an equipotential surface.', 'Zero.', 'zero [1]'),
])
FX(t74, 'C2', (1, 2, 3, 4), [
    ('Explain why the electric potential near an isolated positive charge is positive, whereas gravitational potential is always negative.', 'Potential is zero at infinity. Work must be done against repulsion to bring a positive test charge towards a positive charge, so V is positive; gravity is always attractive so work is done by the field and φ is negative.', 'zero at infinity [1]; work done against repulsion vs by attraction [1] [2]'),
    ('Explain the relationship between field lines and equipotential surfaces.', 'Field lines are always perpendicular to equipotentials; no work is done moving along an equipotential, so the field has no component along it. Closely spaced equipotentials indicate a strong field.', 'perpendicular [1]; spacing relates to field strength / no work along [1] [2]'),
    ('Explain how the field strength at a point can be found from a graph of potential V against distance r.', 'E = −dV/dr: draw a tangent to the curve at that point; the field strength is minus the gradient.', 'tangent gradient [1]; E = −gradient [1] [2]'),
    ('Explain, in terms of energy, how the distance of closest approach of an α-particle to a nucleus can be found.', 'At closest approach the α-particle is momentarily at rest; its initial kinetic energy has all been converted to electric potential energy: Ek = Qq/(4πε₀r), so r = Qq/(4πε₀Ek).', 'KE → electric PE [1]; equation for r [1] [2]'),
])


@t74.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t74_V(r, D):
    Q_ = r.choice([2.0e-9, 5.0e-9, 1.0e-8, 4.0e-8, -3.0e-9, -6.0e-9]); d1 = r.choice([0.050, 0.10, 0.20]); d2 = d1 * r.choice([2, 3, 4])
    V1 = KC * Q_ / d1; V2 = KC * Q_ / d2
    q = r.choice([1.0e-9, 2.0e-9, 5.0e-10])
    s = f'A point charge of {sc(Q_, 2)} C is fixed in place.'
    if D <= 2:
        return numq(r, D, s + f' Point A is {nf(d1 * 100)} cm from it.', 'electric potential at A', V1, ' V', f'V = Q/(4πε₀r) = 8.99 × 10⁹ × {sc(Q_, 2)}/{nf(d1)}', [KC * Q_ / d1 ** 2, -V1, V1 / 2], fm=lambda x: E(x, 3))
    W = q * (V1 - V2)
    if D == 3:
        return Q(s + f' Point A is {nf(d1 * 100)} cm and point B is {nf(d2 * 100)} cm from it. Calculate the potential at A and at B, and the potential difference between A and B.', f'V_A = {E(V1)} V; V_B = {E(V2)} V; V_AB = {E(V1 - V2)} V',
                 f'V = Q/4πε₀r [1]; both values [1]; difference {E(V1 - V2)} V [1] [3]')
    return Q(s + f' Point A is {nf(d1 * 100)} cm and point B is {nf(d2 * 100)} cm from it. (a) Calculate the potential at A and at B. (b) Calculate the work done by an external agent in moving a +{sc(q, 2)} C charge from B to A. (c) Explain the sign of your answer to (b).',
             f'(a) {E(V1)} V; {E(V2)} V (b) {sc(W)} J (c) ' + ('positive: work is done against repulsion' if Q_ > 0 else 'negative: the field does work (attraction), so the external agent does negative work'),
             f'(a) V = Q/4πε₀r: both values [1] (b) W = q(V_A − V_B) [1]; = {sc(W)} J [1] (c) sign explained [1] [4]', 'multi_step')


@t74.add('C3', (2, 3, 4, 5), 'numerical')
def t74_alpha(r, D):
    Z, X = r.choice([(79, 'gold'), (47, 'silver'), (78, 'platinum'), (29, 'copper'), (82, 'lead')])
    Ek_MeV = r.choice([3.0, 4.0, 5.0, 5.5, 7.7]); Ek = Ek_MeV * 1e6 * QE
    rmin = KC * (2 * QE) * (Z * QE) / Ek
    s = f'An α-particle with kinetic energy {nf(Ek_MeV)} MeV is fired directly at a {X} nucleus (proton number {Z}).'
    if D <= 3:
        return Q(s + ' Calculate the distance of closest approach.', f'{sc(rmin)} m', f'Ek = {sc(Ek)} J [1]; Ek = (2e)(Ze)/(4πε₀r) [1]; r = {sc(rmin)} m [1] [3]')
    return Q(s + ' (a) Calculate the kinetic energy in joules. (b) Calculate the distance of closest approach. (c) Explain why this distance is an upper limit for the radius of the nucleus.',
             f'(a) {sc(Ek)} J (b) {sc(rmin)} m (c) the α-particle does not touch the nucleus (it is repelled before reaching it), so the nuclear radius must be smaller than this distance',
             f'(a) × 1.60 × 10⁻¹³ = {sc(Ek)} J [1] (b) KE = electric PE [1]; r = {sc(rmin)} m [1] (c) does not reach nucleus [1]; radius < r [1] [5]', 'multi_step')


@t74.add('C3', (2, 3, 4), 'numerical')
def t74_pe(r, D):
    q1 = r.choice([1.0e-6, 2.0e-6, 3.0e-6, 5.0e-6]); q2 = r.choice([1.0e-6, 2.5e-6, 4.0e-6]); a = r.choice([0.10, 0.20, 0.25]); b = a * r.choice([2, 3])
    U1 = KC * q1 * q2 / a; U2 = KC * q1 * q2 / b
    return Q(f'Two positive point charges of {sc(q1, 2)} C and {sc(q2, 2)} C are held {nf(a * 100)} cm apart. One is released and moves until they are {nf(b * 100)} cm apart. Calculate the electric potential energy at each separation and the kinetic energy gained by the moving charge.' + (' Explain why the kinetic energy gained is not simply force × distance.' if D >= 4 else ''),
             f'{f3(U1)} J and {f3(U2)} J; KE gained = {f3(U1 - U2)} J' + ('; the force decreases as the separation increases' if D >= 4 else ''),
             f'Ep = Qq/(4πε₀r) [1]; both values [1]; ΔEk = {f3(U1 - U2)} J [1]' + ('; force not constant (∝ 1/r²) [1] [4]' if D >= 4 else ' [3]'))


def _pot_c4(r, D):
    R = r.choice([0.10, 0.15, 0.20]); V0 = r.choice([5.0e4, 1.0e5, 2.0e5])
    Q_ = V0 * R / KC
    intro = f'The dome of a Van de Graaff generator in a {city(r)} science museum is a sphere of radius {nf(R * 100)} cm at a potential of {sc(V0, 2)} V.'
    parts = [
        lambda r: ('Define electric potential at a point.', 'Work done per unit positive charge bringing a small test charge from infinity to the point.', 'work per unit charge [1]; from infinity [1] [2]'),
        lambda r: ('Calculate the charge on the dome.', f'{sc(Q_)} C', 'Q = 4πε₀RV [2]'),
        lambda r: ('Calculate the field strength at the surface of the dome.', f'{sc(V0 / R)} V m⁻¹', 'E = V/R for a sphere [2]'),
        lambda r: (f'Calculate the potential at a distance of {nf(3 * R * 100)} cm from the centre.', f'{sc(V0 / 3)} V', 'V ∝ 1/r [1]'),
        lambda r: ('Calculate the energy gained by an electron moving from infinity to the dome surface.', f'{sc(QE * V0)} J', 'W = eV [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t74.add('C4', (2, 3, 4, 5), 'multi_step')(_pot_c4)
CHAPTERS[7] = [t71, t72, t73, t74]

# ===================================================================== 8 Capacitance
N81 = 'Capacitance C = Q/V and capacitors in series and parallel'
t81 = topic(N81, N81.lower(), 'capacitance c = q/v', 'capacitors in series and parallel')
FX(t81, 'C1', (1, 2), [
    ('Which is the definition of capacitance?', 'the charge stored per unit potential difference', 'C = Q/V.', ['the energy stored per unit charge', 'the potential difference per unit charge', 'the charge stored per unit time']),
    ('What is the unit of capacitance?', 'farad (C V⁻¹)', 'C = Q/V.', ['coulomb', 'henry', 'V C⁻¹']),
    ('A 470 μF capacitor is charged to 12 V. What charge is stored?', '5.6 × 10⁻³ C', 'Q = CV = 470 × 10⁻⁶ × 12.', ['5.6 C', '3.9 × 10⁻⁵ C', '2.6 × 10⁴ C']),
    ('Two 10 μF capacitors are connected in series. What is the combined capacitance?', '5 μF', '1/C = 1/10 + 1/10.', ['20 μF', '10 μF', '100 μF']),
    ('Two 10 μF capacitors are connected in parallel. What is the combined capacitance?', '20 μF', 'C = C₁ + C₂.', ['5 μF', '10 μF', '0.2 μF']),
    ('Capacitors in series all have the same', 'charge', 'The same charge flows onto each plate in series.', ['potential difference', 'capacitance', 'energy']),
    ('Capacitors in parallel all have the same', 'potential difference', 'They are connected across the same two points.', ['charge', 'capacitance', 'energy']),
    ('State the formula for the combined capacitance of capacitors in parallel.', 'C = C₁ + C₂ + …', 'sum of capacitances [1]'),
])
FX(t81, 'C2', (1, 2, 3, 4), [
    ('Derive the formula for the combined capacitance of two capacitors in parallel.', 'Same p.d. V across each; total charge Q = Q₁ + Q₂ = C₁V + C₂V, so C = Q/V = C₁ + C₂.', 'same V, charges add [1]; C = C₁ + C₂ [1] [2]'),
    ('Derive the formula for the combined capacitance of two capacitors in series.', 'Same charge Q on each; p.d.s add: V = V₁ + V₂ = Q/C₁ + Q/C₂, so 1/C = V/Q = 1/C₁ + 1/C₂.', 'same Q, p.d.s add [1]; 1/C = 1/C₁ + 1/C₂ [1] [2]'),
    ('Explain why capacitors in series all store the same charge.', 'Charge flowing onto one plate induces an equal and opposite charge on the facing plate; the connected plates of adjacent capacitors form an isolated conductor with net zero charge, so each capacitor carries the same ±Q.', 'induced equal and opposite charges [1]; isolated connected plates have zero net charge [1] [2]'),
    ('Explain why the charge on a capacitor is described as +Q and −Q, although the capacitor as a whole is uncharged.', 'Charging moves electrons from one plate to the other via the circuit; one plate gains −Q and the other is left with +Q; the net charge is zero. "Charge stored" refers to Q on either plate.', 'electrons moved from one plate to other [1]; equal and opposite, net zero [1] [2]'),
])


@t81.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t81_combo(r, D):
    a, b, c = r.choice([10, 22, 47, 100, 220]), r.choice([10, 33, 47, 68, 100]), r.choice([22, 47, 100, 150])
    V = r.choice([6.0, 9.0, 12.0, 24.0])
    kind = r.choice(['ser', 'par', 'mix'])
    if kind == 'ser':
        Ct = 1 / (1 / a + 1 / b); txt = f'Capacitors of {a} μF and {b} μF are connected in series'; wk = f'1/C = 1/{a} + 1/{b}'
    elif kind == 'par':
        Ct = a + b; txt = f'Capacitors of {a} μF and {b} μF are connected in parallel'; wk = f'C = {a} + {b}'
    else:
        Ct = 1 / (1 / (a + b) + 1 / c); txt = f'Capacitors of {a} μF and {b} μF in parallel are connected in series with a {c} μF capacitor'; wk = f'parallel pair = {a + b} μF; 1/C = 1/{a + b} + 1/{c}'
    s = f'{txt}, and the combination is connected to a {nf(V)} V supply.'
    if D <= 2:
        return numq(r, D, s, 'combined capacitance', Ct, ' μF', wk, [a + b + (c if kind == 'mix' else 0), 1 / (1 / a + 1 / b) if kind != 'ser' else a + b, Ct * 2], fm=lambda x: nf(x, 3))
    Qt = Ct * V
    if D == 3:
        return Q(s + ' Calculate the combined capacitance and the total charge drawn from the supply.', f'C = {nf(Ct, 3)} μF; Q = {nf(Qt, 3)} μC',
                 f'{wk} [1]; C = {nf(Ct, 3)} μF [1]; Q = CV = {nf(Qt, 3)} μC [1] [3]')
    if kind == 'ser':
        V1 = Qt / a; ext = f'(c) Calculate the p.d. across the {a} μF capacitor.'; ans = f'{nf(V1, 3)} V'; k = f'same Q, V = Q/C = {nf(V1, 3)} V'
    elif kind == 'par':
        ext = f'(c) Calculate the charge on the {a} μF capacitor.'; ans = f'{nf(a * V, 3)} μC'; k = f'same V, Q = CV = {nf(a * V, 3)} μC'
    else:
        Vc = Qt / c; ext = f'(c) Calculate the p.d. across the {c} μF capacitor.'; ans = f'{nf(Vc, 3)} V'; k = f'Q on {c} μF = total Q, V = Q/C = {nf(Vc, 3)} V'
    return Q(s + f' (a) Calculate the combined capacitance. (b) Calculate the total charge stored. {ext}', f'(a) {nf(Ct, 3)} μF (b) {nf(Qt, 3)} μC (c) {ans}',
             f'(a) {wk} [1]; {nf(Ct, 3)} μF [1] (b) Q = CV = {nf(Qt, 3)} μC [1] (c) {k} [2] [5]', 'multi_step')


@t81.add('C3', (1, 2, 3, 4), 'numerical')
def t81_qv(r, D):
    C = r.choice([4.7e-6, 10e-6, 47e-6, 220e-6, 470e-6, 1000e-6, 2200e-6]); V = r.choice([5.0, 6.0, 9.0, 12.0, 16.0, 25.0])
    Q_ = C * V
    s = f'A capacitor of capacitance {nf(C * 1e6, 3)} μF is charged to a p.d. of {nf(V)} V.'
    if D <= 2:
        return numq(r, D, s, 'charge stored', Q_, ' C', f'Q = CV = {sc(C)} × {nf(V)}', [C / V, V / C, Q_ * 1e6], fm=lambda x: E(x, 3))
    I = r.choice([0.50e-3, 1.0e-3, 2.0e-3])
    return Q(s + f' Calculate the charge stored. It is charged by a constant current of {nf(I * 1000)} mA. Calculate the time taken.' + (' Explain why a constant current would need a varying supply p.d.' if D >= 4 else ''),
             f'Q = {E(Q_)} C; t = {E(Q_ / I)} s' + ('; as the capacitor p.d. rises, the supply p.d. must rise to keep the current constant' if D >= 4 else ''),
             f'Q = CV = {E(Q_)} C [1]; t = Q/I [1]; = {E(Q_ / I)} s [1]' + ('; p.d. across capacitor increases [1] [4]' if D >= 4 else ' [3]'))


def _cap_c4(r, D):
    a, b = r.choice([(2.0, 3.0), (4.0, 6.0), (10.0, 15.0), (6.0, 12.0)]); V = r.choice([9.0, 12.0, 15.0])
    Cs = a * b / (a + b); Qs = Cs * V
    intro = f'Two capacitors of {nf(a)} μF and {nf(b)} μF are connected in series to a {nf(V)} V battery.'
    parts = [
        lambda r: ('Define capacitance.', 'Charge stored per unit p.d. (C = Q/V).', 'Q/V [1]'),
        lambda r: ('Calculate the combined capacitance.', f'{nf(Cs, 3)} μF', '1/C = 1/C₁ + 1/C₂ [2]'),
        lambda r: ('Calculate the charge on each capacitor.', f'{nf(Qs, 3)} μC', 'Q = CV, same on each [2]'),
        lambda r: (f'Calculate the p.d. across the {nf(a)} μF capacitor.', f'{nf(Qs / a, 3)} V', 'V = Q/C [2]'),
        lambda r: ('The capacitors are now reconnected in parallel to the same battery. Calculate the total charge stored.', f'{nf((a + b) * V, 3)} μC', 'C = C₁ + C₂ [2]'),
        lambda r: ('Explain why the series combination has a smaller capacitance than either capacitor.', 'Same charge but the p.d. is shared: the supply p.d. is larger than either p.d., so Q/V is smaller.', 'p.d.s add for same Q [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t81.add('C4', (2, 3, 4, 5), 'multi_step')(_cap_c4)

N82 = 'Energy stored in a capacitor W = ½QV'
t82 = topic(N82, N82.lower(), 'energy stored in a capacitor', 'w = ½qv')
FX(t82, 'C1', (1, 2), [
    ('The energy stored in a capacitor of capacitance C at p.d. V is', '½CV²', 'W = ½QV = ½CV².', ['CV²', '½CV', 'C²V/2']),
    ('A 100 μF capacitor is charged to 20 V. What energy does it store?', '0.020 J', 'W = ½ × 100 × 10⁻⁶ × 400.', ['0.040 J', '2.0 × 10⁻³ J', '1.0 × 10⁻³ J']),
    ('The p.d. across a capacitor is doubled. The energy stored becomes', 'four times as large', 'W ∝ V².', ['twice as large', 'half as large', 'unchanged']),
    ('On a graph of p.d. V against charge Q for a capacitor, the energy stored is represented by', 'the area under the line', 'Work done = ∫V dQ = ½QV.', ['the gradient of the line', 'the intercept on the V axis', 'the length of the line']),
    ('Why is the energy stored in a capacitor ½QV rather than QV?', 'the p.d. increases from zero as the charge is added, so the average p.d. is ½V', 'Each increment of charge is moved against the p.d. at that moment.', ['half the energy is always lost as heat in the capacitor', 'only one plate stores energy', 'the charge on each plate is ½Q']),
    ('A capacitor stores 0.50 J when charged to 10 V. What is its capacitance?', '0.010 F', 'C = 2W/V² = 1.0/100.', ['0.10 F', '0.050 F', '5.0 F']),
    ('State two expressions, other than ½QV, for the energy stored in a capacitor.', '½CV² and ½Q²/C', 'both [1]'),
])
FX(t82, 'C2', (1, 2, 3, 4), [
    ('Use a graph of p.d. against charge to show that the energy stored in a capacitor is ½QV.', 'V ∝ Q gives a straight line through the origin; work done adding charge ΔQ at p.d. V is VΔQ, a strip of area; total work = area of triangle = ½QV.', 'straight line V ∝ Q [1]; energy = area = ½QV [1] [2]'),
    ('Explain why only half of the energy supplied by a battery while charging a capacitor is stored in the capacitor.', 'The battery supplies QV (charge Q at constant e.m.f. V) but the capacitor stores ½QV; the other half is dissipated as thermal energy in the resistance of the circuit.', 'battery provides QV [1]; ½QV dissipated in resistance [1] [2]'),
    ('Suggest why capacitors are used in camera flash units rather than connecting the lamp directly to the battery.', 'The capacitor stores energy slowly from the battery and releases it very quickly, giving a large current and high power for a short time that the battery alone could not deliver.', 'stores energy then releases quickly [1]; high power / large current [1] [2]'),
    ('Explain why a capacitor is not a practical replacement for a battery in a phone.', 'For the same size, a capacitor stores much less energy, and its p.d. falls steadily as it discharges, whereas a battery supplies an almost constant e.m.f.', 'less energy stored [1]; p.d. falls as it discharges [1] [2]'),
])
relation(t82, 'C2', (2, 3), 'W = ½CV²', 'energy stored', {'p.d. across the capacitor': 2, 'capacitance': 1},
         ['A capacitor in a camera flash circuit is charged by a battery.', 'A capacitor in a defibrillator is charged before use.', 'A capacitor in a laboratory circuit is charged from a variable supply.'])


@t82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t82_W(r, D):
    dev, C, V = r.choice([('a camera flash capacitor', r.choice([100e-6, 150e-6, 220e-6]), r.choice([300.0, 330.0, 350.0])), ('a defibrillator capacitor', r.choice([32e-6, 64e-6, 100e-6]), r.choice([2000.0, 3000.0, 5000.0])),
                          ('a capacitor in a laboratory circuit', r.choice([470e-6, 1000e-6, 2200e-6]), r.choice([6.0, 9.0, 12.0])), ('a supercapacitor in a toy car', r.choice([1.0, 2.5, 5.0]), r.choice([2.5, 2.7, 5.0]))])
    W = 0.5 * C * V * V
    Cs = f'{nf(C * 1e6, 3)} μF' if C < 0.01 else f'{nf(C)} F'
    s = f'{cap(dev)} has a capacitance of {Cs} and is charged to {nf(V)} V.'
    if D <= 2:
        return numq(r, D, s, 'energy stored', W, ' J', f'W = ½CV² = ½ × {sc(C)} × {nf(V)}²', [C * V * V, 0.5 * C * V, C * V], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the charge stored and the energy stored.', f'Q = {E(C * V)} C; W = {E(W)} J', f'Q = CV = {E(C * V)} C [1]; W = ½QV [1]; = {E(W)} J [1] [3]')
    t = r.choice([1.0e-3, 2.0e-3, 5.0e-3]) if C < 0.01 else r.choice([5.0, 10.0])
    return Q(s + f' (a) Calculate the energy stored. (b) The capacitor discharges until the p.d. is {nf(V / 2)} V. Calculate the energy released. (c) The energy is released in {E(t)} s. Calculate the mean power output.',
             f'(a) {E(W)} J (b) {E(0.75 * W)} J (c) {E(0.75 * W / t)} W', f'(a) W = ½CV² = {E(W)} J [1] (b) energy left = ¼ of original [1]; released = {E(0.75 * W)} J [1] (c) P = W/t [1]; = {E(0.75 * W / t)} W [1] [5]', 'multi_step')


@t82.add('C3', (3, 4, 5), 'numerical')
def t82_share(r, D):
    C1 = r.choice([10.0, 20.0, 47.0, 100.0]); C2 = r.choice([10.0, 22.0, 47.0, 100.0]); V = r.choice([10.0, 12.0, 20.0])
    W1 = 0.5 * C1 * V * V * 1e-6; Vf = C1 * V / (C1 + C2); W2 = 0.5 * (C1 + C2) * Vf * Vf * 1e-6
    return Q(f'A {nf(C1)} μF capacitor charged to {nf(V)} V is disconnected from the supply and connected across an uncharged {nf(C2)} μF capacitor. Calculate the final common p.d. and the energy lost.' + (' Suggest where this energy goes.' if D >= 4 else ''),
             f'V = {nf(Vf, 3)} V; energy lost = {E(W1 - W2)} J' + ('; dissipated as thermal energy in the connecting wires (and radiated)' if D >= 4 else ''),
             f'charge conserved: Q = {nf(C1 * V)} μC [1]; V = Q/(C₁ + C₂) = {nf(Vf, 3)} V [1]; ΔW = {E(W1)} − {E(W2)} = {E(W1 - W2)} J [1]' + ('; thermal energy in resistance [1] [4]' if D >= 4 else ' [3]'))


def _ew_c4(r, D):
    C = r.choice([2200e-6, 4700e-6, 10000e-6]); V = r.choice([6.0, 9.0, 12.0])
    W = 0.5 * C * V * V
    intro = f'A {nf(C * 1e6)} μF capacitor is charged to {nf(V)} V and then used to lift a small mass with an electric motor.'
    parts = [
        lambda r: ('Calculate the charge stored.', f'{E(C * V)} C', 'Q = CV [1]'),
        lambda r: ('Calculate the energy stored.', f'{E(W)} J', 'W = ½CV² [2]'),
        lambda r: ('The motor is 20% efficient. Calculate the maximum height to which it can lift a 50 g mass.', f'{E(0.2 * W / (0.050 * GR))} m', 'mgh = 0.2W [2]'),
        lambda r: ('Explain how a graph of V against Q can be used to find the energy stored.', 'Energy stored = area under the V–Q graph (a triangle, ½QV).', 'area under graph [1]'),
        lambda r: ('Explain why the energy stored is ½QV, not QV.', 'The p.d. rises from zero during charging, so the average p.d. against which charge is moved is ½V.', 'average p.d. ½V [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t82.add('C4', (2, 3, 4, 5), 'multi_step')(_ew_c4)

N83 = 'Discharging a capacitor: exponential decay and the time constant RC'
t83 = topic(N83, N83.lower(), 'discharging a capacitor', 'time constant')
FX(t83, 'C1', (1, 2), [
    ('What is the time constant of a circuit with a 100 μF capacitor discharging through a 20 kΩ resistor?', '2.0 s', 'τ = RC = 20 × 10³ × 100 × 10⁻⁶.', ['0.20 s', '20 s', '5.0 × 10⁻⁹ s']),
    ('After one time constant, the charge on a discharging capacitor has fallen to about', '37% of its initial value', 'Q = Q₀e⁻¹ = 0.37Q₀.', ['50% of its initial value', '63% of its initial value', '0% of its initial value']),
    ('Which equation describes the charge on a capacitor discharging through a resistor?', 'Q = Q₀e^(−t/RC)', 'Exponential decay with time constant RC.', ['Q = Q₀(1 − e^(−t/RC))', 'Q = Q₀ − t/RC', 'Q = Q₀e^(−RCt)']),
    ('What is the unit of the product RC?', 's', 'Ω × F = (V A⁻¹)(C V⁻¹) = C A⁻¹ = s.', ['Ω F⁻¹', 'C', 'J']),
    ('A graph of ln(V) against t for a discharging capacitor is', 'a straight line with gradient −1/RC', 'ln V = ln V₀ − t/RC.', ['a straight line with gradient −RC', 'an exponential curve', 'a straight line with gradient +1/RC']),
    ('The time taken for the p.d. across a discharging capacitor to halve is', '0.69RC', 't½ = RC ln 2.', ['0.37RC', '0.50RC', '1.4RC']),
    ('State what is meant by the time constant of a capacitor–resistor circuit.', 'The time for the charge (or p.d. or current) to fall to 1/e (about 37%) of its initial value; τ = RC.', 'time to fall to 1/e of initial [1]'),
])
FX(t83, 'C2', (1, 2, 3, 4), [
    ('Explain why the current from a discharging capacitor decreases with time.', 'The current is I = V/R; as charge leaves, the p.d. V = Q/C falls, so the current falls; the rate of loss of charge is proportional to the charge remaining, giving exponential decay.', 'p.d. falls as charge decreases [1]; I = V/R decreases / rate ∝ Q [1] [2]'),
    ('Explain how a graph of ln(I) against t can be used to find the time constant.', 'I = I₀e^(−t/RC) so ln I = ln I₀ − t/RC: a straight line of gradient −1/RC; τ = −1/gradient.', 'ln I linear in t [1]; τ = −1/gradient [1] [2]'),
    ('Explain why a larger resistance makes a capacitor discharge more slowly.', 'For the same p.d., a larger resistance gives a smaller current, so charge flows off the plates more slowly; τ = RC is larger.', 'smaller current for same V [1]; τ = RC larger [1] [2]'),
    ('Show that the product RC has units of seconds.', 'Ω = V A⁻¹ and F = C V⁻¹; Ω F = C A⁻¹ = (A s) A⁻¹ = s.', 'units of R and C [1]; simplify to s [1] [2]'),
])


@t83.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t83_decay(r, D):
    C = r.choice([47e-6, 100e-6, 220e-6, 470e-6, 1000e-6]); R = r.choice([10e3, 22e3, 33e3, 47e3, 100e3]); V0 = r.choice([6.0, 9.0, 12.0, 15.0])
    tau = R * C; t = tau * r.choice([0.5, 1.0, 1.5, 2.0, 3.0])
    V = V0 * math.exp(-t / tau)
    s = f'A {nf(C * 1e6)} μF capacitor charged to {nf(V0)} V is discharged through a {nf(R / 1e3)} kΩ resistor.'
    if D <= 2:
        return numq(r, D, s, 'time constant of the circuit', tau, ' s', f'τ = RC = {sc(R)} × {sc(C)}', [R / C, tau * 1000, 1 / tau], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + f' Calculate the time constant and the p.d. across the capacitor after {nf(t, 3)} s.', f'τ = {f3(tau)} s; V = {nf(V, 3)} V',
                 f'τ = RC = {f3(tau)} s [1]; V = V₀e^(−t/RC) [1]; = {nf(V, 3)} V [1] [3]')
    frac = r.choice([0.50, 0.25, 0.10, 0.20])
    tf = -tau * math.log(frac)
    return Q(s + f' (a) Calculate the time constant. (b) Calculate the initial current. (c) Calculate the time taken for the p.d. to fall to {nf(frac * V0, 3)} V.',
             f'(a) {f3(tau)} s (b) {E(V0 / R)} A (c) {f3(tf)} s', f'(a) τ = RC = {f3(tau)} s [1] (b) I₀ = V₀/R = {E(V0 / R)} A [1] (c) V/V₀ = e^(−t/RC) [1]; t = −RC ln({nf(frac)}) [1]; = {f3(tf)} s [1] [5]', 'multi_step')


@t83.add('C3', (2, 3, 4, 5), 'case')
def t83_graph(r, D):
    R = r.choice([10e3, 20e3, 50e3, 100e3]); C = r.choice([100e-6, 220e-6, 470e-6]); I0 = r.choice([0.60, 0.90, 1.2]) * 1e-3
    tau = R * C
    ts = [0, round(tau * 0.5, 1), round(tau, 1), round(tau * 1.5, 1), round(tau * 2, 1)]
    Is = [I0 * math.exp(-t / tau) * 1e3 for t in ts]
    rows = '; '.join(f't = {nf(t, 3) if t else 0} s, I = {nf(i, 3)} mA' for t, i in zip(ts, Is))
    grad = -1 / tau
    return Q(f'A capacitor discharges through a {nf(R / 1e3)} kΩ resistor. Readings: {rows}. A graph of ln(I/mA) against t is plotted. Determine the gradient of the graph and hence the time constant and the capacitance.' + (' Explain why the ln graph is used rather than I against t.' if D >= 4 else ''),
             f'gradient = {sc(grad)} s⁻¹; τ = {f3(tau)} s; C = {sc(C)} F' + ('; a straight line allows the gradient (−1/RC) to be found accurately and tests exponential decay' if D >= 4 else ''),
             f'ln I values calculated [1]; gradient = {sc(grad)} s⁻¹ [1]; τ = −1/gradient = {f3(tau)} s and C = τ/R = {sc(C)} F [1]' + ('; straight-line test of exponential [1] [4]' if D >= 4 else ' [3]'))


def _dis_c4(r, D):
    C = r.choice([470e-6, 1000e-6, 2200e-6]); R = r.choice([4.7e3, 10e3, 22e3]); V0 = r.choice([9.0, 12.0])
    tau = R * C
    intro = f'A {nf(C * 1e6)} μF capacitor is charged to {nf(V0)} V and then discharged through a {nf(R / 1e3)} kΩ resistor. A data-logger records the current.'
    parts = [
        lambda r: ('Calculate the time constant.', f'{f3(tau)} s', 'τ = RC [1]'),
        lambda r: ('Calculate the initial current.', f'{E(V0 / R)} A', 'I = V/R [1]'),
        lambda r: (f'Calculate the charge remaining after {nf(round(2 * tau, 1))} s.', f'{E(C * V0 * math.exp(-round(2 * tau, 1) / tau))} C', 'Q = Q₀e^(−t/RC) [2]'),
        lambda r: ('Calculate the time for the energy stored to fall to half its initial value.', f'{f3(tau * math.log(2) / 2)} s', 'W ∝ V², V = V₀/√2, t = ½RC ln 2 [3]'),
        lambda r: ('Describe the shape of a graph of current against time.', 'Exponential decay: falls quickly at first then more slowly, approaching zero; same fractional fall in equal times.', 'exponential decay [1]; constant ratio property [1] [2]'),
        lambda r: ('State one change that would make the capacitor discharge more slowly.', 'Increase R or C.', 'larger R or C [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t83.add('C4', (2, 3, 4, 5), 'multi_step')(_dis_c4)
CHAPTERS[8] = [t81, t82, t83]

# ===================================================================== 9 Magnetic fields
N91 = 'Magnetic fields and field patterns of currents and magnets'
t91 = topic(N91, N91.lower(), 'magnetic fields', 'field patterns of currents and magnets')
FX(t91, 'C1', (1, 2), [
    ('What is a magnetic field?', 'a region in which a magnetic pole, a moving charge or a current-carrying conductor experiences a force', 'Definition of magnetic field.', ['a region in which a stationary charge experiences a force', 'a region in which a mass experiences a force', 'the space inside a magnet only']),
    ('What is the shape of the magnetic field around a long straight current-carrying wire?', 'concentric circles centred on the wire', 'Field lines are circles in planes perpendicular to the wire.', ['radial lines from the wire', 'straight lines parallel to the wire', 'a uniform field']),
    ('Inside a long solenoid carrying a current, the magnetic field is', 'uniform and parallel to the axis', 'Parallel, equally spaced lines inside the solenoid.', ['zero', 'radial', 'circular around the axis']),
    ('Which rule gives the direction of the magnetic field around a current-carrying wire?', 'the right-hand grip rule', 'Thumb along current, fingers curl in the field direction.', ['Fleming\'s left-hand rule', 'Lenz\'s law', 'the principle of moments']),
    ('Magnetic field lines outside a bar magnet go from', 'the north pole to the south pole', 'By convention field lines leave N and enter S.', ['the south pole to the north pole', 'the middle to the ends', 'one end to the same end']),
    ('Two long parallel wires carry currents in the same direction. The wires', 'attract each other', 'Each is in the other\'s field; F = BIL gives attraction for like currents.', ['repel each other', 'exert no force on each other', 'rotate to become perpendicular']),
    ('Viewed from one end, the current in a solenoid flows clockwise. That end is a', 'south pole', 'Clockwise viewed from the end = S pole.', ['north pole', 'neutral point', 'region of zero field']),
    ('State how the strength of the magnetic field of a solenoid could be increased.', 'Increase the current, increase the number of turns per unit length, or add an iron core.', 'any one [1]'),
])
FX(t91, 'C2', (1, 2, 3, 4), [
    ('Describe the magnetic field pattern of a flat circular coil carrying a current.', 'Near the wire the lines are circles around it; at the centre of the coil the lines are straight, perpendicular to the plane of the coil; the pattern is like that of a short bar magnet.', 'circles round each side of wire [1]; straight through the centre perpendicular to coil [1] [2]'),
    ('Explain why two parallel wires carrying currents in opposite directions repel.', 'Each wire is in the magnetic field of the other; by Fleming\'s left-hand rule the force on each wire is directed away from the other, so they repel (equal and opposite forces, N3).', 'each wire in the other\'s field [1]; FLHR gives forces apart [1] [2]'),
    ('Explain why the field outside a long solenoid is much weaker than inside.', 'Inside, the fields of all turns add along the axis, concentrated in a small area; outside, the same lines spread out over a very large region, so the flux density is small.', 'fields of turns add inside [1]; lines spread out outside [1] [2]'),
    ('Explain how iron filings and a plotting compass can be used to show the field pattern of a current-carrying wire.', 'Pass the wire vertically through a horizontal card; sprinkle filings and tap: they line up in concentric circles. A plotting compass placed on the card shows the direction of the field at each point (the N end points along the field).', 'filings show shape of lines [1]; compass shows direction [1] [2]'),
])

DIRS = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}


@t91.add('C3', (1, 2, 3, 4), 'explain')
def t91_grip(r, D):
    cur = r.choice(['vertically upwards', 'vertically downwards'])
    pos = r.choice(['north', 'south', 'east', 'west'])
    # current up: field anticlockwise viewed from above. At a point to the north, anticlockwise tangent points west.
    ccw = {'north': 'west', 'west': 'south', 'south': 'east', 'east': 'north'}
    cw = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
    d = ccw[pos] if cur == 'vertically upwards' else cw[pos]
    who = person(r)
    if D <= 2:
        opts, a = mcq(r, f'towards the {d}', [f'towards the {x}' for x in ['north', 'south', 'east', 'west'] if x != d] + ['vertically upwards'])
        return Q(f'A long straight vertical wire carries a current {cur}. {who} places a plotting compass on a horizontal card a short distance to the {pos} of the wire (ignore the Earth\'s field). In which direction does the north end of the compass point?', a,
                 f'Right-hand grip rule: viewed from above the field is {"anticlockwise" if cur.endswith("upwards") else "clockwise"}; at the {pos} side it points {d}.', opts=opts)
    return Q(f'A long straight vertical wire carries a current {cur}. Use the right-hand grip rule to state the direction of the magnetic field at a point a short distance to the {pos} of the wire, and describe the shape of the field lines.' + (' State how the field strength changes if the distance from the wire is doubled.' if D >= 4 else ''),
             f'Towards the {d}; concentric circles around the wire ({"anticlockwise" if cur.endswith("upwards") else "clockwise"} viewed from above)' + ('; field strength halves (B ∝ 1/r)' if D >= 4 else ''),
             f'direction {d} [1]; concentric circles, sense correct [1]' + ('; B ∝ 1/r, halves [1] [3]' if D >= 4 else ' [2]'))


@t91.add('C3', (1, 2, 3, 4), 'explain')
def t91_sol(r, D):
    sense = r.choice(['clockwise', 'anticlockwise']); end = r.choice(['left', 'right'])
    pole = 'south' if sense == 'clockwise' else 'north'
    other = 'north' if pole == 'south' else 'south'
    if D <= 2:
        opts, a = mcq(r, f'a {pole} pole', [f'a {other} pole', 'not a pole, the field there is zero', 'a north pole and a south pole alternately'])
        return Q(f'A solenoid lies horizontally. Viewed from its {end}-hand end, the current flows {sense}. The {end}-hand end of the solenoid behaves as', a, f'Viewed from an end: clockwise current gives a S pole, anticlockwise gives a N pole. Here: {pole}.', opts=opts)
    return Q(f'A horizontal solenoid carries a current that flows {sense} when viewed from its {end}-hand end. State which pole is formed at the {end}-hand end, describe the field inside the solenoid, and state what happens to the poles if the current is reversed.',
             f'{cap(pole)} pole at the {end}-hand end; uniform field parallel to the axis inside; reversing the current swaps the poles.',
             f'{pole} pole [1]; uniform, parallel to axis [1]; poles reverse [1] [3]')


def _mf_c4(r, D):
    I = r.choice([2.0, 3.0, 5.0])
    intro = ctx(r, ['{p} investigates the magnetic field of a long solenoid carrying a current of {I} A in a laboratory in {c}.', 'An electromagnet used in a scrapyard in {c} consists of a solenoid carrying {I} A wound on an iron core.'], I=nf(I))
    parts = [
        lambda r: ('Describe the magnetic field pattern inside and outside the solenoid.', 'Inside: uniform, parallel to the axis. Outside: like a bar magnet, lines from N end round to S end.', 'inside uniform [1]; outside bar-magnet pattern [1] [2]'),
        lambda r: ('State two ways to increase the field strength.', 'Increase the current; increase turns per unit length; insert an iron core.', 'first way [1]; second way [1] [2]'),
        lambda r: ('Explain how to identify which end is the north pole.', 'Right-hand grip rule: fingers in the direction of the current, thumb points to the N pole (or view from the end: anticlockwise = N).', 'grip rule / clock rule [1]'),
        lambda r: ('Explain why a plotting compass placed inside near the centre lines up along the axis.', 'The field there is parallel to the axis, and the compass aligns with the field.', 'aligns with field direction [1]'),
        lambda r: ('Describe the force between two adjacent turns of the coil.', 'Adjacent turns carry current in the same direction, so they attract.', 'attract, same direction currents [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t91.add('C4', (2, 3, 4, 5), 'multi_step')(_mf_c4)

N92 = 'Force on a current-carrying conductor F = BIL sin θ and magnetic flux density'
t92 = topic(N92, N92.lower(), 'force on a current-carrying conductor', 'magnetic flux density')
FX(t92, 'C1', (1, 2), [
    ('Which is the definition of the tesla?', 'the uniform flux density that produces a force of 1 N on a 1 m length of wire carrying 1 A at right angles to the field', 'B = F/(IL) with θ = 90°.', ['the flux through an area of 1 m²', 'the field that induces 1 V in a 1 m wire', 'the field produced by 1 A in a 1 m wire']),
    ('A wire of length 0.20 m carries 3.0 A at right angles to a field of 0.50 T. What is the force on it?', '0.30 N', 'F = BIL = 0.50 × 3.0 × 0.20.', ['3.0 N', '0.033 N', '7.5 N']),
    ('A current-carrying wire is parallel to a uniform magnetic field. The force on it is', 'zero', 'F = BIL sin θ, θ = 0.', ['a maximum', 'BIL', 'BIL/2']),
    ('Which rule gives the direction of the force on a current-carrying wire in a magnetic field?', 'Fleming\'s left-hand rule', 'First finger field, second finger current, thumb motion (force).', ['Fleming\'s right-hand rule', 'the right-hand grip rule', 'Lenz\'s law']),
    ('Which unit is equivalent to the tesla?', 'N A⁻¹ m⁻¹', 'B = F/(IL).', ['N A m', 'Wb m', 'V s⁻¹']),
    ('A wire carries a current at 30° to a uniform magnetic field. Compared with the force when it is at 90°, the force is', 'half as large', 'sin 30° = 0.5.', ['the same', 'twice as large', 'zero']),
    ('State Fleming\'s left-hand rule.', 'First finger: field; second finger: current; thumb: force (motion), all mutually perpendicular.', 'all three correct [1]'),
])
FX(t92, 'C2', (1, 2, 3, 4), [
    ('Explain why a current-carrying wire in a magnetic field experiences a force.', 'The current produces its own magnetic field around the wire, which interacts with the external field (stronger on one side, weaker on the other), giving a resultant force; equivalently, each moving charge experiences a force BQv.', 'interaction of fields / force on moving charges [1]; perpendicular to both B and I [1] [2]'),
    ('Describe how a current balance can be used to measure magnetic flux density.', 'A wire frame of length L in the field is balanced; when a current I flows, the force BIL tips it; add a rider of known mass m to rebalance (or measure on a top-pan balance): BIL = mg, so B = mg/(IL).', 'force measured via balance/mass [1]; B = F/(IL) [1] [2]'),
    ('Explain why the force on a wire is greatest when the wire is perpendicular to the field.', 'F = BIL sin θ; sin θ has its maximum value 1 when θ = 90°, so the whole current is perpendicular to B.', 'F ∝ sin θ [1]; maximum at 90° [1] [2]'),
    ('Explain why a rectangular coil carrying a current in a uniform field experiences a turning effect but no resultant force.', 'Opposite sides carry current in opposite directions, so the forces on them are equal and opposite (no resultant force) but act along different lines, forming a couple.', 'equal and opposite forces on opposite sides [1]; not in line → couple / torque [1] [2]'),
])
relation(t92, 'C2', (2, 3), 'F = BIL sin θ', 'force on the wire', {'current': 1, 'length of wire in the field': 1, 'magnetic flux density': 1},
         ['A straight wire carries a current at right angles to a uniform magnetic field.', 'A copper rod rests on rails at right angles to a magnetic field and carries a current.', 'A wire in a current balance sits between the poles of a magnet.'])


@t92.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t92_bil(r, D):
    B = r.choice([0.050, 0.080, 0.12, 0.25, 0.40, 0.60]); I = r.choice([1.5, 2.0, 3.0, 4.5, 6.0]); L = r.choice([0.040, 0.050, 0.080, 0.10, 0.25]); th = r.choice([90, 90, 30, 45, 60])
    F = B * I * L * math.sin(math.radians(th))
    s = f'A straight wire of length {nf(L * 100)} cm in a uniform magnetic field of flux density {nf(B)} T carries a current of {nf(I)} A at {th}° to the field.'
    if D <= 2:
        return numq(r, D, s, 'force on the wire', F, ' N', f'F = BIL sin θ = {nf(B)} × {nf(I)} × {nf(L)} × sin {th}°', [B * I * L if th != 90 else B * I * L / 2, B * I * L * math.cos(math.radians(th)) if th != 90 else B * I, F * 100], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the force on the wire and state the angle for which the force would be zero.', f'{E(F)} N; 0° (parallel to the field)', f'F = BIL sin θ [1]; = {E(F)} N [1]; zero when parallel [1] [3]')
    m = r.choice([2.0, 3.0, 5.0]) * 1e-3
    Ib = m * GR / (B * L)
    return Q(f'A horizontal copper rod of mass {nf(m * 1000)} g and length {nf(L * 100)} cm lies at right angles to a horizontal uniform magnetic field of flux density {nf(B)} T. (a) Calculate the current needed for the magnetic force to support the weight of the rod. (b) State how the direction of the current must be chosen. (c) Calculate the force on the rod if the current is {nf(I)} A and the rod is turned to {th if th != 90 else 30}° to the field.',
             f'(a) {E(Ib)} A (b) so that Fleming\'s left-hand rule gives an upward force (c) {E(B * I * L * math.sin(math.radians(th if th != 90 else 30)))} N',
             f'(a) BIL = mg [1]; I = {E(Ib)} A [1] (b) FLHR, force upwards [1] (c) F = BIL sin θ [1]; = {E(B * I * L * math.sin(math.radians(th if th != 90 else 30)))} N [1] [5]', 'multi_step')


@t92.add('C3', (2, 3, 4), 'case')
def t92_balance(r, D):
    B = r.choice([0.030, 0.045, 0.060, 0.080]); L = r.choice([0.050, 0.060, 0.080])
    Is = [1.0, 2.0, 3.0, 4.0, 5.0]
    ms = [B * I * L / GR * 1e3 for I in Is]  # grams
    rows = '; '.join(f'I = {I:.1f} A, reading change = {m:.2f} g' for I, m in zip(Is, ms))
    return Q(f'A wire of length {nf(L * 100)} cm is clamped horizontally between the poles of a magnet resting on a top-pan balance, at right angles to the field. As the current is increased the balance reading changes: {rows}. Use the data to determine the magnetic flux density.' + (' Explain why the balance reading changes.' if D >= 4 else ''),
             f'gradient = {nf(ms[-1] / 5, 3)} g A⁻¹ = {sc(ms[-1] / 5 / 1000)} kg A⁻¹; B = gradient × g/L = {nf(B, 3)} T' + ('; by Newton\'s third law the force on the wire produces an equal and opposite force on the magnet' if D >= 4 else ''),
             f'F = Δm × g [1]; gradient of Δm against I [1]; B = g × gradient/L = {nf(B, 3)} T [1]' + ('; N3 pair on magnet [1] [4]' if D >= 4 else ' [3]'))


def _bil_c4(r, D):
    B = r.choice([0.15, 0.20, 0.30]); L = r.choice([0.050, 0.080]); N = r.choice([50, 100, 200]); I = r.choice([0.20, 0.50]); w = r.choice([0.030, 0.040])
    F = N * B * I * L
    intro = f'A rectangular coil of {N} turns, with sides {nf(L * 100)} cm (perpendicular to the field) and {nf(w * 100)} cm, carries a current of {nf(I)} A. Its plane is parallel to a uniform field of flux density {nf(B)} T.'
    parts = [
        lambda r: ('Define the tesla.', 'Flux density giving 1 N on 1 m of wire carrying 1 A at right angles to the field.', 'F = 1 N, I = 1 A, L = 1 m, perpendicular [1]'),
        lambda r: ('Calculate the force on one of the sides perpendicular to the field.', f'{E(F)} N', 'F = NBIL [2]'),
        lambda r: ('Calculate the torque on the coil.', f'{E(F * w)} N m', 'torque = F × separation [2]'),
        lambda r: ('Explain why there is no resultant force on the coil.', 'Forces on opposite sides are equal and opposite.', 'equal and opposite [1]'),
        lambda r: ('State the force on the sides parallel to the field.', 'Zero (sin 0° = 0).', 'zero [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t92.add('C4', (2, 3, 4, 5), 'multi_step')(_bil_c4)

N93 = 'Force on a moving charge F = BQv and the Hall effect'
t93 = topic(N93, N93.lower(), 'force on a moving charge', 'hall effect')
FX(t93, 'C1', (1, 2), [
    ('An electron moves at 2.0 × 10⁷ m s⁻¹ at right angles to a field of 0.10 T. What is the force on it?', '3.2 × 10⁻¹³ N', 'F = BQv = 0.10 × 1.60 × 10⁻¹⁹ × 2.0 × 10⁷.', ['3.2 × 10⁻¹¹ N', '2.0 × 10⁶ N', '1.6 × 10⁻²⁶ N']),
    ('The magnetic force on a charged particle moving in a magnetic field is always', 'perpendicular to its velocity', 'F = BQv sin θ, perpendicular to v and B.', ['parallel to its velocity', 'parallel to the field', 'opposite to its velocity']),
    ('Which change does the magnetic force on a moving charge produce?', 'a change in direction but not speed', 'Force ⊥ velocity, so no work done.', ['a change in speed only', 'a change in both speed and direction', 'no change at all']),
    ('In the Hall effect, the Hall voltage is produced because', 'charge carriers are deflected to one side of the conductor', 'BQv force pushes carriers sideways until the electric field balances it.', ['the conductor heats up', 'the current reverses direction', 'the magnetic field induces an e.m.f. in a loop']),
    ('Why is the Hall voltage much larger in a semiconductor than in a metal for the same current?', 'the number density of charge carriers is much smaller', 'V_H = BI/(ntq): smaller n gives larger V_H.', ['semiconductors have higher resistance', 'the charge carriers are positive', 'the magnetic field is stronger inside semiconductors']),
    ('Which expression gives the Hall voltage across a slice of thickness t?', 'BI/(ntq)', 'V_H = BI/(ntq).', ['BIt/(nq)', 'nBI/(tq)', 'Bntq/I']),
    ('State the expression for the force on a charge q moving at speed v at right angles to a magnetic field B.', 'F = Bqv', 'F = BQv [1]'),
])
FX(t93, 'C2', (1, 2, 3, 4), [
    ('Explain how the Hall voltage is established across a current-carrying slice in a magnetic field.', 'The charge carriers experience a force BQv perpendicular to their drift, so they accumulate on one face (and leave the opposite charge on the other). This produces an electric field across the slice; equilibrium is reached when QE = BQv, i.e. Q V_H/d = BQv.', 'carriers deflected, build up on one side [1]; electric force balances magnetic force [1] [2]'),
    ('Derive the expression V_H = BI/(ntq) for the Hall voltage across a slice of width d and thickness t.', 'At equilibrium qV_H/d = Bqv, so V_H = Bvd. With I = nAvq and A = dt, v = I/(ndtq). So V_H = BId/(ndtq) = BI/(ntq).', 'qV_H/d = Bqv [1]; substitute v = I/(nAq) with A = dt [1] [2]'),
    ('Explain why the magnetic force on a moving charged particle does no work.', 'The force is always perpendicular to the velocity, so there is no displacement in the direction of the force; the kinetic energy (speed) is unchanged.', 'force ⊥ velocity [1]; no work, speed constant [1] [2]'),
    ('Explain why Hall probes are made from semiconductors rather than metals.', 'Semiconductors have a much smaller n, so V_H = BI/(ntq) is much larger and easier to measure for a given B and I.', 'smaller n [1]; larger, measurable Hall voltage [1] [2]'),
    ('Explain how a Hall probe must be oriented to measure the flux density of a field.', 'The probe face must be perpendicular to the field lines (field perpendicular to the current in the slice), so that the full BQv acts; rotate until the Hall voltage is maximum.', 'field perpendicular to slice / current [1]; maximum reading [1] [2]'),
])


@t93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t93_bqv(r, D):
    part, q = r.choice([('An electron', QE), ('A proton', QE), ('An α-particle', 2 * QE), ('A singly charged ion', QE)])
    B = r.choice([0.020, 0.050, 0.10, 0.25, 0.50, 1.2]); v = r.choice([2.0e5, 5.0e5, 1.5e6, 4.0e6, 2.0e7]); th = r.choice([90, 90, 30, 60])
    F = B * q * v * math.sin(math.radians(th))
    s = f'{part} moves at {sc(v, 2)} m s⁻¹ at {th}° to a uniform magnetic field of flux density {nf(B)} T.'
    if D <= 3:
        return numq(r, D, s, 'magnetic force on it', F, ' N', f'F = BQv sin θ = {nf(B)} × {sc(q)} × {sc(v, 2)} × sin {th}°', [B * q * v * (math.cos(math.radians(th)) if th != 90 else 0.5), F * 2, B * v], fm=lambda x: sc(x, 3))
    return Q(s + ' (a) Calculate the magnetic force on it. (b) Explain why its kinetic energy does not change. (c) State the effect on the force of doubling the speed.',
             f'(a) {sc(F)} N (b) the force is perpendicular to the velocity, so no work is done (c) the force doubles', f'(a) F = BQv sin θ [1]; = {sc(F)} N [1] (b) force ⊥ velocity, no work [1] (c) doubles (F ∝ v) [1] [4]', 'multi_step')


@t93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t93_hall(r, D):
    mat, n = r.choice([('n-type silicon', r.choice([1.0e21, 2.0e21, 5.0e21])), ('indium antimonide', r.choice([2.0e22, 1.0e23])), ('copper', 8.5e28), ('a germanium slice', r.choice([5.0e21, 1.0e22]))])
    B = r.choice([0.050, 0.10, 0.20, 0.40]); I = r.choice([10e-3, 20e-3, 50e-3, 0.10]) if mat != 'copper' else r.choice([2.0, 5.0])
    t = r.choice([0.10e-3, 0.20e-3, 0.50e-3, 1.0e-3])
    VH = B * I / (n * t * QE)
    s = f'A Hall probe uses a slice of {mat} of thickness {nf(t * 1000)} mm with {sc(n, 2)} charge carriers per m³ (charge e). A current of {E(I)} A flows in the slice, which is perpendicular to a field of {nf(B)} T.'
    if D <= 2:
        return numq(r, D, s, 'Hall voltage', VH, ' V', f'V_H = BI/(ntq) = {nf(B)} × {E(I)}/({sc(n, 2)} × {sc(t)} × 1.60 × 10⁻¹⁹)', [VH * 1000, VH / 1000, B * I / (n * QE)], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(s + ' Calculate the Hall voltage and state how it changes if the current is doubled.', f'{sc(VH)} V; doubles', f'V_H = BI/(ntq) [1]; = {sc(VH)} V [1]; V_H ∝ I so doubles [1] [3]')
    return Q(s + ' (a) Calculate the Hall voltage. (b) The probe is rotated so that the field makes 60° with the face of the slice. Calculate the new Hall voltage. (c) Explain why the Hall voltage would be much smaller in a copper slice of the same size.',
             f'(a) {sc(VH)} V (b) {sc(VH * math.sin(math.radians(60)))} V (c) copper has a far larger n (≈ 10²⁹ m⁻³), and V_H ∝ 1/n', f'(a) V_H = BI/(ntq) = {sc(VH)} V [1] (b) component of B perpendicular to face: B sin 60° [1]; {sc(VH * math.sin(math.radians(60)))} V [1] (c) larger n [1]; V_H ∝ 1/n [1] [5]', 'multi_step')


def _hall_c4(r, D):
    n = r.choice([1.5e21, 3.0e21]); t = 0.20e-3; d = r.choice([4.0e-3, 5.0e-3]); I = r.choice([20e-3, 40e-3]); B = r.choice([0.15, 0.30])
    VH = B * I / (n * t * QE); v = I / (n * d * t * QE)
    intro = f'A Hall probe slice of width {nf(d * 1000)} mm and thickness 0.20 mm contains {sc(n, 2)} free electrons per m³. It carries a current of {nf(I * 1000)} mA and is placed perpendicular to a field of {nf(B)} T.'
    parts = [
        lambda r: ('Calculate the drift speed of the electrons.', f'{E(v)} m s⁻¹', 'v = I/(nAq), A = dt [2]'),
        lambda r: ('Calculate the magnetic force on one electron.', f'{sc(B * QE * v)} N', 'F = Bev [1]'),
        lambda r: ('Calculate the Hall voltage.', f'{sc(VH)} V', 'V_H = BI/(ntq) [2]'),
        lambda r: ('Explain why the Hall voltage reaches a steady value.', 'Charge builds up on one side until the electric force eV_H/d equals the magnetic force Bev.', 'charge accumulates on one face [1]; electric force eV_H/d balances Bev [1] [2]'),
        lambda r: ('State how the probe could be used to show that a field is uniform.', 'Move it to different positions with the same orientation; the Hall voltage stays the same.', 'constant V_H at different points [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t93.add('C4', (2, 3, 4, 5), 'multi_step')(_hall_c4)

N94 = 'Velocity selection and charged particles in combined electric and magnetic fields'
t94 = topic(N94, N94.lower(), 'velocity selection', 'combined electric and magnetic fields')
FX(t94, 'C1', (1, 2), [
    ('In a velocity selector, particles pass undeflected when their speed v satisfies', 'v = E/B', 'eE = Bev ⇒ v = E/B.', ['v = B/E', 'v = EB', 'v = E/(Bq)']),
    ('A charged particle moves at right angles to a uniform magnetic field. Its path is', 'a circle', 'Force ⊥ velocity, constant magnitude.', ['a parabola', 'a straight line', 'a helix with increasing radius']),
    ('A particle of mass m and charge q moves at speed v perpendicular to a field B. The radius of its path is', 'mv/(Bq)', 'Bqv = mv²/r.', ['Bq/(mv)', 'mvBq', 'mv²/(Bq)']),
    ('In a velocity selector, the electric and magnetic fields are', 'perpendicular to each other and to the particle velocity', 'Forces must be in opposite directions along the same line.', ['parallel to each other', 'both parallel to the velocity', 'both zero']),
    ('A beam of particles enters a velocity selector. Particles that are faster than E/B are', 'deflected in the direction of the magnetic force', 'Bqv > qE for larger v.', ['deflected in the direction of the electric force', 'undeflected', 'stopped']),
    ('Two particles with the same charge and speed move in circles in the same magnetic field. Particle X has twice the mass of Y. The radius of X\'s path is', 'twice that of Y', 'r = mv/(Bq) ∝ m.', ['half that of Y', 'the same as Y', 'four times that of Y']),
    ('State the condition for a charged particle to pass undeflected through crossed electric and magnetic fields.', 'The electric force equals the magnetic force in magnitude and is opposite in direction: qE = Bqv, so v = E/B.', 'qE = Bqv [1]'),
])
FX(t94, 'C2', (1, 2, 3, 4), [
    ('Explain why a charged particle moving perpendicular to a uniform magnetic field moves in a circle.', 'The magnetic force Bqv has constant magnitude (speed constant) and is always perpendicular to the velocity, so it provides a centripetal force: Bqv = mv²/r with r constant.', 'force constant magnitude ⊥ v [1]; acts as centripetal force [1] [2]'),
    ('Explain why the speed selected by a velocity selector does not depend on the mass or charge of the particles.', 'qE = Bqv: the charge cancels and mass does not appear, so v = E/B for any particle.', 'q cancels [1]; no mass term [1] [2]'),
    ('Explain how the specific charge e/mₑ of the electron can be found by deflecting an electron beam in a magnetic field.', 'Accelerate electrons through p.d. V: ½mv² = eV. In field B they move in a circle of measured radius r: Bev = mv²/r. Eliminating v gives e/m = 2V/(B²r²).', 'energy equation [1]; circular motion and eliminate v [1] [2]'),
    ('Explain how a mass spectrometer separates isotopes.', 'Ions of the same charge are selected to have the same speed (E/B); in a uniform magnetic field r = mv/(Bq), so heavier isotopes follow larger circles and arrive at different positions.', 'same speed via selector [1]; r ∝ m in magnetic field [1] [2]'),
])


@t94.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t94_sel(r, D):
    Ef = r.choice([1.5e4, 2.0e4, 3.0e4, 5.0e4, 8.0e4]); B = r.choice([0.020, 0.050, 0.10, 0.15, 0.25])
    v = Ef / B
    s = f'In a velocity selector, a uniform electric field of strength {sc(Ef, 2)} V m⁻¹ is perpendicular to a uniform magnetic field of flux density {nf(B)} T.'
    if D <= 2:
        return numq(r, D, s, 'speed of the particles that pass through undeflected', v, ' m s⁻¹', f'qE = Bqv ⇒ v = E/B = {sc(Ef, 2)}/{nf(B)}', [B / Ef, Ef * B, v / 2], fm=lambda x: sc(x, 3))
    d = r.choice([0.010, 0.020, 0.040])
    if D == 3:
        return Q(s + f' The electric field is produced by plates {nf(d * 100)} cm apart. Calculate the speed selected and the p.d. between the plates.', f'v = {sc(v)} m s⁻¹; V = {E(Ef * d)} V',
                 f'qE = Bqv [1]; v = E/B = {sc(v)} m s⁻¹ [1]; V = Ed = {E(Ef * d)} V [1] [3]')
    return Q(s + ' (a) Calculate the speed of particles that pass undeflected. (b) Explain why this speed is the same for protons and α-particles. (c) Describe and explain the motion of a particle that is faster than this speed.',
             f'(a) {sc(v)} m s⁻¹ (b) charge cancels in qE = Bqv; mass does not appear (c) Bqv > qE so it is deflected in the direction of the magnetic force (curves out of the beam)',
             f'(a) v = E/B = {sc(v)} m s⁻¹ [1] (b) q cancels [1]; independent of mass [1] (c) magnetic force larger [1]; deflected that way [1] [5]', 'multi_step')


@t94.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t94_circle(r, D):
    part, q, m = r.choice([('An electron', QE, ME), ('A proton', QE, MP), ('An α-particle', 2 * QE, 6.64e-27), ('A deuteron', QE, 3.34e-27)])
    v = r.choice([2.0e6, 5.0e6, 8.0e6, 1.5e7]) if part != 'An electron' else r.choice([5.0e6, 1.0e7, 3.0e7])
    B = r.choice([0.010, 0.050, 0.10, 0.20, 0.50]) if part != 'An electron' else r.choice([1.0e-3, 2.0e-3, 5.0e-3])
    rad = m * v / (B * q)
    s = f'{part} (mass {sc(m)} kg, charge {sc(q)} C) moves at {sc(v, 2)} m s⁻¹ perpendicular to a uniform magnetic field of flux density {E(B, 2)} T.'
    if D <= 2:
        return numq(r, D, s, 'radius of its circular path', rad, ' m', f'Bqv = mv²/r ⇒ r = mv/(Bq)', [B * q / (m * v), rad * 2, m * v * v / (B * q)], fm=lambda x: E(x, 3))
    T = 2 * PI * m / (B * q)
    if D == 3:
        return Q(s + ' Calculate the radius of its path and the time for one revolution.', f'r = {E(rad)} m; T = {sc(T)} s', f'Bqv = mv²/r [1]; r = mv/(Bq) = {E(rad)} m [1]; T = 2πr/v = {sc(T)} s [1] [3]')
    return Q(s + ' (a) Show that r = mv/(Bq). (b) Calculate the radius of the path. (c) Show that the period of the motion does not depend on the speed, and calculate it.',
             f'(a) Bqv = mv²/r ⇒ r = mv/(Bq) (b) {E(rad)} m (c) T = 2πr/v = 2πm/(Bq), no v; T = {sc(T)} s', f'(a) magnetic force = centripetal force [1] (b) {E(rad)} m [1] (c) T = 2πr/v [1]; = 2πm/(Bq) independent of v [1]; = {sc(T)} s [1] [5]', 'multi_step')


@t94.add('C3', (3, 4, 5), 'numerical')
def t94_em(r, D):
    V = r.choice([150.0, 200.0, 250.0, 300.0]); B = r.choice([1.0e-3, 1.5e-3, 2.0e-3])
    v = math.sqrt(2 * QE * V / ME); rad = ME * v / (B * QE)
    rad = float(nf(rad, 3)); em = 2 * V / (B * B * rad * rad)
    return Q(f'In a fine-beam tube, electrons are accelerated from rest through {nf(V)} V and then enter a uniform magnetic field of {sc(B, 2)} T at right angles. The beam forms a circle of radius {nf(rad * 100, 3)} cm. Use these data to determine the specific charge e/mₑ of the electron.',
             f'{sc(em)} C kg⁻¹', f'½mv² = eV [1]; Bev = mv²/r [1]; e/m = 2V/(B²r²) = {sc(em)} C kg⁻¹ [1]' + (' [3]' if D == 3 else '; correct handling of r in m [1] [4]'))


def _sel_c4(r, D):
    Ef = r.choice([2.0e4, 4.0e4]); B1 = r.choice([0.10, 0.20]); B2 = r.choice([0.25, 0.50])
    v = Ef / B1
    m1, m2 = 20 * 1.66e-27, 22 * 1.66e-27
    r1, r2 = m1 * v / (B2 * QE), m2 * v / (B2 * QE)
    intro = f'In a mass spectrometer, singly charged neon ions pass through a velocity selector (E = {sc(Ef, 2)} V m⁻¹, B = {nf(B1)} T) and then enter a region with only a magnetic field of {nf(B2)} T, where they travel in semicircles.'
    parts = [
        lambda r: ('Calculate the speed of ions leaving the velocity selector.', f'{sc(v)} m s⁻¹', 'v = E/B [2]'),
        lambda r: ('Calculate the radius of the path of a neon-20 ion (mass 20u).', f'{E(r1)} m', 'r = mv/(Bq) [2]'),
        lambda r: ('Calculate the separation of the points where neon-20 and neon-22 ions land after a semicircle.', f'{E(2 * (r2 - r1))} m', '2(r₂ − r₁) [3]'),
        lambda r: ('Explain why the ions must all have the same speed.', 'r depends on both m and v; with v fixed, r ∝ m so position identifies mass.', 'r ∝ m only if v same [1]'),
        lambda r: ('Explain why the ions do not gain kinetic energy in the magnetic field.', 'The magnetic force is perpendicular to their velocity, so it does no work.', 'force ⊥ v [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t94.add('C4', (2, 3, 4, 5), 'multi_step')(_sel_c4)
CHAPTERS[9] = [t91, t92, t93, t94]

# ===================================================================== 10 Electromagnetic induction
N101 = 'Magnetic flux and flux linkage'
t101 = topic(N101, N101.lower(), 'magnetic flux', 'flux linkage')
FX(t101, 'C1', (1, 2), [
    ('Which is the definition of magnetic flux through an area A perpendicular to a field B?', 'Φ = BA', 'Flux = flux density × area normal to the field.', ['Φ = B/A', 'Φ = NBA²', 'Φ = BIL']),
    ('What is the unit of magnetic flux?', 'weber (Wb)', '1 Wb = 1 T m².', ['tesla (T)', 'henry (H)', 'T m⁻²']),
    ('A coil of 200 turns and area 5.0 × 10⁻³ m² is perpendicular to a field of 0.40 T. What is the flux linkage?', '0.40 Wb', 'NΦ = NBA = 200 × 0.40 × 5.0 × 10⁻³.', ['2.0 × 10⁻³ Wb', '4.0 Wb', '0.010 Wb']),
    ('A flat coil is rotated from perpendicular to parallel with a uniform magnetic field. The flux through it', 'falls from a maximum to zero', 'Φ = BA cos θ, where θ is the angle between B and the normal.', ['rises from zero to a maximum', 'stays constant', 'reverses direction']),
    ('Which unit is equivalent to the weber?', 'T m²', 'Φ = BA.', ['T m⁻²', 'T m', 'N A⁻¹']),
    ('What is meant by flux linkage?', 'the product of the magnetic flux through a coil and the number of turns', 'Flux linkage = NΦ.', ['the flux per unit area', 'the flux per turn', 'the rate of change of flux']),
    ('Define the weber.', 'The flux through an area of 1 m² normal to a uniform field of flux density 1 T.', '1 T × 1 m² normal to field [1]'),
])
FX(t101, 'C2', (1, 2, 3, 4), [
    ('Explain why the flux through a coil depends on the angle between the coil and the field.', 'Only the component of B perpendicular to the plane of the coil passes through it: Φ = BA cos θ (θ between B and the normal); the flux is maximum when the coil is perpendicular to the field and zero when parallel.', 'only perpendicular component [1]; max when perpendicular, zero when parallel [1] [2]'),
    ('Distinguish between magnetic flux density and magnetic flux.', 'Flux density B is the force per unit current per unit length (T), a measure of field strength at a point; flux Φ = BA is the total "amount of field" passing through an area (Wb).', 'B: field strength at a point, T [1]; Φ = BA through an area, Wb [1] [2]'),
    ('Explain why a coil with more turns gives a larger flux linkage in the same field.', 'Each turn has the same flux Φ through it; flux linkage NΦ adds the contributions of all N turns.', 'same flux per turn [1]; linkage = NΦ ∝ N [1] [2]'),
])


@t101.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t101_flux(r, D):
    N = r.choice([50, 100, 150, 250, 400, 500]); B = r.choice([0.020, 0.050, 0.080, 0.15, 0.30]); shape = r.choice(['sq', 'circ'])
    if shape == 'sq':
        a = r.choice([0.020, 0.030, 0.040, 0.050]); A = a * a; txt = f'square coil of side {nf(a * 100)} cm'
    else:
        d = r.choice([0.030, 0.040, 0.060, 0.080]); A = PI * d * d / 4; txt = f'circular coil of diameter {nf(d * 100)} cm'
    th = r.choice([0, 0, 30, 45, 60])
    phi = B * A * math.cos(math.radians(th)); NL = N * phi
    ang = 'with its plane perpendicular to' if th == 0 else f'with the normal to its plane at {th}° to'
    s = f'A {txt} has {N} turns and is placed {ang} a uniform magnetic field of flux density {nf(B)} T.'
    if D <= 2:
        return numq(r, D, s, 'flux linkage', NL, ' Wb', f'NΦ = NBA cos θ = {N} × {nf(B)} × {sc(A)} × cos {th}°', [phi, N * B * A * (math.sin(math.radians(th)) if th else 0.5), NL * 100], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the area of the coil, the flux through one turn and the flux linkage.', f'A = {sc(A)} m²; Φ = {sc(phi)} Wb; NΦ = {E(NL)} Wb',
                 f'A = {sc(A)} m² [1]; Φ = BA cos θ = {sc(phi)} Wb [1]; NΦ = {E(NL)} Wb [1] [3]')
    return Q(s + ' (a) Calculate the flux linkage. (b) The coil is rotated so that its plane is parallel to the field. State the new flux linkage. (c) Calculate the change in flux linkage and state the unit in base units.',
             f'(a) {E(NL)} Wb (b) zero (c) {E(NL)} Wb; kg m² s⁻² A⁻¹', f'(a) NBA cos θ = {E(NL)} Wb [1] (b) zero [1] (c) ΔNΦ = {E(NL)} Wb [1]; Wb = T m² = kg s⁻² A⁻¹ m² [1] [4]', 'multi_step')


@t101.add('C2', (2, 3, 4), 'explain')
def t101_rot(r, D):
    a = r.choice([0, 30, 60, 90]); b = r.choice([x for x in (0, 30, 45, 60, 90) if x != a])
    fa, fb = math.cos(math.radians(a)), math.cos(math.radians(b))
    return Q(f'A flat coil in a uniform magnetic field is turned so that the angle between the field and the normal to the coil changes from {a}° to {b}°. Explain how the magnetic flux through the coil changes, and give the ratio of the final flux to the initial flux' + (' if it exists.' if a == 90 else '.'),
             f'Φ = BA cos θ; flux changes from {nf(fa, 2)}BA to {nf(fb, 2)}BA' + ('' if a == 90 else f'; ratio = {nf(fb / fa, 3)}'),
             'Φ = BA cos θ [1]; correct direction of change [1]' + (' [2]' if D < 3 else '; correct ratio or comment on zero flux [1] [3]'))


def _flux_c4(r, D):
    N = r.choice([100, 200, 300]); A = r.choice([2.0e-3, 4.0e-3, 6.0e-3]); B = r.choice([0.10, 0.25])
    intro = f'A coil of {N} turns, each of area {sc(A, 2)} m², is held with its plane perpendicular to a uniform field of {nf(B)} T.'
    parts = [
        lambda r: ('Define magnetic flux.', 'Product of flux density and area normal to the field (Φ = BA).', 'B × area normal [1]'),
        lambda r: ('Calculate the flux through one turn.', f'{sc(B * A)} Wb', 'Φ = BA [1]'),
        lambda r: ('Calculate the flux linkage.', f'{E(N * B * A)} Wb', 'NΦ [1]'),
        lambda r: ('Calculate the flux linkage when the coil is rotated through 60°.', f'{E(N * B * A * 0.5)} Wb', 'cos 60° = 0.5 [2]'),
        lambda r: ('State the flux linkage when the plane of the coil is parallel to the field, and explain why.', 'Zero: no field lines pass through the coil.', 'zero with reason [1]'),
        lambda r: ('Explain why the flux through the coil and the flux linkage have the same unit.', 'N is a pure number (no unit), so NΦ has the unit of Φ (Wb).', 'N dimensionless [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t101.add('C4', (2, 3, 4, 5), 'multi_step')(_flux_c4)

N102 = "Faraday's and Lenz's laws of electromagnetic induction"
t102 = topic(N102, N102.lower(), "faraday's and lenz's laws", 'electromagnetic induction')
FX(t102, 'C1', (1, 2), [
    ('Faraday\'s law states that the induced e.m.f. is proportional to', 'the rate of change of magnetic flux linkage', 'E = −d(NΦ)/dt.', ['the magnetic flux linkage', 'the magnetic flux density', 'the current in the circuit']),
    ('Lenz\'s law is a consequence of the conservation of', 'energy', 'The induced current opposes the change; otherwise energy would be created.', ['charge', 'momentum', 'mass']),
    ('The flux linkage of a coil falls uniformly from 0.60 Wb to zero in 0.20 s. What is the magnitude of the induced e.m.f.?', '3.0 V', 'E = Δ(NΦ)/Δt = 0.60/0.20.', ['0.12 V', '0.33 V', '0.60 V']),
    ('A straight rod of length 0.50 m moves at 4.0 m s⁻¹ perpendicular to a field of 0.20 T. What e.m.f. is induced across its ends?', '0.40 V', 'E = BLv.', ['1.6 V', '0.10 V', '10 V']),
    ('A magnet is pushed N-pole first into a coil. The end of the coil facing the magnet becomes', 'a north pole', 'Lenz: the induced current opposes the approach.', ['a south pole', 'unmagnetised', 'a north pole then immediately a south pole']),
    ('In E = −d(NΦ)/dt, the minus sign represents', 'Lenz\'s law: the induced e.m.f. opposes the change producing it', 'Direction of e.m.f. opposes the change.', ['that e.m.f. is always negative', 'that flux is negative', 'energy loss in the coil']),
    ('State Lenz\'s law.', 'The direction of the induced e.m.f. (current) is such as to oppose the change producing it.', 'opposes the change causing it [1]'),
    ('State Faraday\'s law of electromagnetic induction.', 'The magnitude of the induced e.m.f. is proportional to the rate of change of magnetic flux linkage.', 'e.m.f. ∝ rate of change of flux linkage [1]'),
])
FX(t102, 'C2', (1, 2, 3, 4), [
    ('Explain, using Lenz\'s law, why work must be done to push a magnet into a coil connected in a closed circuit.', 'The induced current makes the coil end a like pole that repels the magnet, opposing its motion; work must be done against this force, and this work becomes electrical energy (then thermal energy) in the circuit.', 'induced pole repels / opposes motion [1]; work done converted to electrical energy [1] [2]'),
    ('Explain why no e.m.f. is induced in a coil when a magnet is held stationary inside it.', 'E is proportional to the rate of change of flux linkage; when the magnet is stationary the flux linkage is constant, so there is no e.m.f.', 'flux linkage constant [1]; no rate of change so E = 0 [1] [2]'),
    ('Explain how a metal rod moving through a magnetic field has an e.m.f. induced across it, in terms of forces on electrons.', 'Free electrons in the rod move with it at velocity v; each experiences a force Bev along the rod, so electrons collect at one end, creating a p.d. (e.m.f.) until the electric force balances the magnetic force.', 'force Bev on free electrons along rod [1]; charge separation gives e.m.f. [1] [2]'),
    ('Derive the expression E = BLv for a rod moving perpendicular to a field.', 'In time Δt the rod sweeps area LvΔt, so the flux cut ΔΦ = BLvΔt; E = ΔΦ/Δt = BLv.', 'area swept = LvΔt [1]; E = ΔΦ/Δt = BLv [1] [2]'),
    ('A magnet is dropped through a long vertical copper tube. Explain why it falls more slowly than when dropped outside the tube.', 'The falling magnet causes changing flux in the tube walls, inducing eddy currents; by Lenz\'s law these produce a field that opposes the motion, giving an upward force on the magnet.', 'changing flux induces currents [1]; currents oppose motion (Lenz) [1] [2]'),
])
relation(t102, 'C2', (2, 3), 'E = N ΔΦ/Δt', 'magnitude of the induced e.m.f.', {'number of turns': 1, 'speed at which the magnet is moved': 1},
         ['A magnet is pushed into a coil at a steady speed.', 'A coil is pulled out of the gap between two magnets at a steady speed.', 'A bar magnet is moved past a pickup coil on a guitar test rig.'])


@t102.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t102_faraday(r, D):
    N = r.choice([50, 100, 200, 300, 500]); A = r.choice([1.0e-3, 2.5e-3, 4.0e-3, 8.0e-3]); B1 = r.choice([0.20, 0.40, 0.60, 0.80]); B2 = r.choice([0.0, 0.0, 0.10, -0.20])
    t = r.choice([0.050, 0.10, 0.20, 0.40])
    dNP = N * A * (B1 - B2); Em = dNP / t
    how = 'reduced uniformly to zero' if B2 == 0 else (f'reduced uniformly to {nf(B2)} T' if B2 > 0 else f'reversed uniformly to {nf(-B2)} T in the opposite direction')
    s = f'A coil of {N} turns and area {sc(A, 2)} m² is perpendicular to a uniform magnetic field of {nf(B1)} T. The field is {how} in {nf(t)} s.'
    if D <= 2:
        return numq(r, D, s, 'magnitude of the average induced e.m.f.', Em, ' V', f'E = Δ(NΦ)/Δt = {N} × {sc(A, 2)} × {nf(B1 - B2)}/{nf(t)}', [dNP, Em / N, A * (B1 - B2) / t], fm=lambda x: E(x, 3))
    R = r.choice([2.0, 5.0, 10.0, 20.0])
    if D == 3:
        return Q(s + ' Calculate the change in flux linkage and the average induced e.m.f.', f'Δ(NΦ) = {E(dNP)} Wb; E = {E(Em)} V', f'Δ(NΦ) = NAΔB = {E(dNP)} Wb [1]; E = Δ(NΦ)/Δt [1]; = {E(Em)} V [1] [3]')
    return Q(s + f' The coil is connected to form a circuit of total resistance {nf(R)} Ω. (a) Calculate the average induced e.m.f. (b) Calculate the average current and the charge that flows. (c) Explain, using Lenz\'s law, the direction of the induced current.',
             f'(a) {E(Em)} V (b) I = {E(Em / R)} A; Q = {E(Em / R * t)} C (c) the induced current produces a field that opposes the change, i.e. in the direction of the original field (it tries to maintain the decreasing flux)',
             f'(a) E = Δ(NΦ)/Δt = {E(Em)} V [1] (b) I = E/R = {E(Em / R)} A [1]; Q = It = {E(Em / R * t)} C [1] (c) opposes change [1]; field direction of original field [1] [5]', 'multi_step')


@t102.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t102_blv(r, D):
    sc_ = r.choice(['rod', 'plane', 'train'])
    if sc_ == 'rod':
        L = r.choice([0.20, 0.30, 0.50]); v = r.choice([1.5, 2.0, 4.0, 6.0]); B = r.choice([0.10, 0.25, 0.40, 0.60]); txt = f'A metal rod of length {nf(L)} m slides along horizontal rails at {nf(v)} m s⁻¹ perpendicular to a vertical magnetic field of {nf(B)} T.'
    elif sc_ == 'plane':
        L = r.choice([30.0, 40.0, 60.0]); v = r.choice([200.0, 250.0, 280.0]); B = r.choice([2.0e-5, 4.0e-5, 5.0e-5]); txt = f'An aircraft with a wingspan of {nf(L)} m flies horizontally at {nf(v)} m s⁻¹ where the vertical component of the Earth\'s magnetic field is {sc(B, 2)} T.'
    else:
        L = 1.4; v = r.choice([30.0, 50.0, 80.0]); B = r.choice([3.0e-5, 4.5e-5]); txt = f'A train axle of length 1.4 m moves at {nf(v)} m s⁻¹ where the vertical component of the Earth\'s magnetic field is {sc(B, 2)} T.'
    Em = B * L * v
    if D <= 3:
        return numq(r, D, txt, 'e.m.f. induced across its ends', Em, ' V', f'E = BLv = {E(B, 2)} × {nf(L)} × {nf(v)}', [B * L / v, B * v, Em * 10], fm=lambda x: E(x, 3))
    if sc_ == 'rod':
        R = r.choice([0.50, 1.0, 2.0]); I = Em / R; F = B * I * L
        return Q(txt + f' The rails are connected by a resistor so that the circuit resistance is {nf(R)} Ω. (a) Calculate the induced e.m.f. (b) Calculate the current and the magnetic force on the rod. (c) Calculate the power needed to keep the rod moving at constant speed and show that it equals the electrical power.',
                 f'(a) {E(Em)} V (b) I = {E(I)} A; F = {E(F)} N (c) P = Fv = {E(F * v)} W = EI', f'(a) E = BLv = {E(Em)} V [1] (b) I = E/R = {E(I)} A [1]; F = BIL = {E(F)} N [1] (c) P = Fv = {E(F * v)} W [1]; = EI shown [1] [5]', 'multi_step')
    return Q(txt + ' (a) Calculate the e.m.f. induced between the ends. (b) Explain why this e.m.f. cannot be used to drive a current through a voltmeter carried on board.',
             f'(a) {E(Em)} V (b) the voltmeter leads move through the field too and have the same e.m.f. induced in them, which cancels; there is no change of flux through the complete circuit',
             f'(a) E = BLv [1]; = {E(Em)} V [1] (b) leads also cut flux / equal opposing e.m.f. [1]; no net change in flux linkage of circuit [1] [4]', 'multi_step')


def _ind_c4(r, D):
    N = r.choice([200, 400]); A = r.choice([3.0e-3, 5.0e-3]); B = r.choice([0.30, 0.50]); t = r.choice([0.10, 0.25])
    Em = N * B * A / t
    intro = f'A coil of {N} turns and area {sc(A, 2)} m² is pulled out of a uniform magnetic field of {nf(B)} T, perpendicular to its plane, in {nf(t)} s.'
    parts = [
        lambda r: ('State Faraday\'s law.', 'Induced e.m.f. ∝ rate of change of flux linkage.', 'rate of change of flux linkage [1]'),
        lambda r: ('Calculate the initial flux linkage.', f'{E(N * B * A)} Wb', 'NBA [1]'),
        lambda r: ('Calculate the average induced e.m.f.', f'{E(Em)} V', 'E = Δ(NΦ)/Δt [2]'),
        lambda r: ('State Lenz\'s law and use it to explain why a force is needed to pull the coil out.', 'Induced current opposes the change: it produces a force opposing the motion, so work must be done.', 'Lenz statement [1]; opposing force on coil [1] [2]'),
        lambda r: ('Suggest how the induced e.m.f. could be doubled.', 'Pull it out in half the time, double the turns, or double B or A.', 'valid change [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t102.add('C4', (2, 3, 4, 5), 'multi_step')(_ind_c4)

N103 = 'Applications of electromagnetic induction including generators and eddy currents'
t103 = topic(N103, N103.lower(), 'applications of electromagnetic induction', 'generators and eddy currents')
FX(t103, 'C1', (1, 2), [
    ('The peak e.m.f. of a coil of N turns and area A rotating at angular speed ω in a field B is', 'BANω', 'E = BANω sin ωt.', ['BAN/ω', 'BANω²', 'BA/Nω']),
    ('In a simple a.c. generator, the e.m.f. is a maximum when the plane of the coil is', 'parallel to the magnetic field', 'Flux linkage is zero but its rate of change is greatest.', ['perpendicular to the magnetic field', 'at 45° to the field', 'at any angle; it is constant']),
    ('Why is the core of a transformer made of thin insulated sheets (laminations)?', 'to reduce eddy currents in the core', 'Laminations increase resistance to eddy current loops, reducing heating.', ['to increase the flux linkage', 'to make the core lighter only', 'to increase the resistance of the coils']),
    ('Eddy currents in a metal disc spinning between the poles of a magnet', 'slow the disc down', 'Lenz: the currents oppose the relative motion.', ['speed the disc up', 'have no effect on the disc', 'magnetise the disc permanently']),
    ('The rotation speed of a generator is doubled. What happens to the peak e.m.f. and to the frequency?', 'both double', 'E₀ = BANω and f = ω/2π.', ['the peak e.m.f. doubles; the frequency is unchanged', 'the peak e.m.f. is unchanged; the frequency doubles', 'both quadruple']),
    ('Which is an application of eddy currents?', 'electromagnetic braking of trains', 'Eddy currents produce a retarding force.', ['charging a capacitor', 'a moving-coil loudspeaker', 'a cathode-ray tube']),
    ('State one disadvantage of eddy currents in electrical machines.', 'They cause energy loss as heating of the core (reduced efficiency).', 'heating / energy loss [1]'),
])
FX(t103, 'C2', (1, 2, 3, 4), [
    ('Explain why the e.m.f. of a rotating coil generator is zero when the plane of the coil is perpendicular to the field.', 'At that instant the flux linkage is a maximum and momentarily not changing (the sides move parallel to the field), so the rate of change of flux linkage, and hence the e.m.f., is zero.', 'flux linkage maximum [1]; rate of change zero [1] [2]'),
    ('Explain how eddy currents produce a braking force on a metal disc rotating between magnet poles.', 'Parts of the disc move through the field, cutting flux, so e.m.f.s and circulating eddy currents are induced; by Lenz\'s law the forces on these currents oppose the motion, slowing the disc; kinetic energy becomes thermal energy.', 'eddy currents induced by changing flux [1]; force opposes motion (Lenz), KE → thermal [1] [2]'),
    ('Explain why cutting slots in a metal plate makes it swing more freely through a magnetic field.', 'The slots break up the paths of eddy currents, increasing resistance and reducing the size of the currents; the opposing force and energy loss are smaller.', 'slots interrupt eddy current paths [1]; smaller currents, less damping [1] [2]'),
    ('Describe how a microphone or guitar pickup uses electromagnetic induction.', 'A vibrating diaphragm (or steel string) moves a coil relative to a magnet (or changes the flux through a coil); the changing flux linkage induces an e.m.f. that varies in time with the vibration.', 'relative motion / changing flux [1]; induced e.m.f. follows vibration [1] [2]'),
])


@t103.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t103_gen(r, D):
    N = r.choice([50, 100, 200, 500]); A = r.choice([2.0e-3, 4.0e-3, 0.010, 0.020]); B = r.choice([0.050, 0.10, 0.20, 0.30]); f = r.choice([5.0, 10.0, 25.0, 50.0])
    w = 2 * PI * f; E0 = B * A * N * w
    s = f'A generator coil of {N} turns, each of area {sc(A, 2)} m², rotates at {nf(f)} revolutions per second in a uniform magnetic field of {nf(B)} T.'
    if D <= 2:
        return numq(r, D, s, 'peak e.m.f.', E0, ' V', f'E₀ = BANω = {nf(B)} × {sc(A, 2)} × {N} × 2π × {nf(f)}', [B * A * N * f, E0 / N, E0 / math.sqrt(2)], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the angular speed and the peak e.m.f., and state the frequency of the alternating e.m.f.', f'ω = {f3(w)} rad s⁻¹; E₀ = {E(E0)} V; f = {nf(f)} Hz',
                 f'ω = 2πf = {f3(w)} rad s⁻¹ [1]; E₀ = BANω = {E(E0)} V [1]; frequency {nf(f)} Hz [1] [3]')
    t = r.choice([0.0025, 0.004, 0.005]) if f >= 25 else r.choice([0.010, 0.020, 0.030])
    e = E0 * math.sin(w * t)
    return Q(s + f' The e.m.f. is zero at t = 0. (a) Calculate the peak e.m.f. (b) Write down an equation for the e.m.f. as a function of time. (c) Calculate the e.m.f. at t = {nf(t)} s.',
             f'(a) {E(E0)} V (b) E = {E(E0)} sin({f3(w)}t) (c) {E(e)} V', f'(a) E₀ = BANω = {E(E0)} V [1] (b) E = E₀ sin ωt with values [1] (c) substitute in radians [1]; {E(e)} V [1] [4]', 'multi_step')


@t103.add('C2', (2, 3, 4), 'explain')
def t103_app(r, D):
    dev, ans = r.choice([('an induction hob heating a steel pan', 'An alternating current in a coil under the hob produces a rapidly changing magnetic field; this induces eddy currents in the base of the pan, which heat it by I²R.'),
                         ('magnetic braking on a roller-coaster', 'Metal fins on the car pass between strong magnets; changing flux induces eddy currents whose forces oppose the motion (Lenz), so the car slows smoothly without contact.'),
                         ('a metal detector at an airport', 'An alternating current in a coil produces a changing field that induces eddy currents in metal objects; these produce their own field, which changes the e.m.f. in a detecting coil.'),
                         ('a bicycle dynamo lighting a lamp', 'The wheel spins a magnet near a coil, so the flux linkage of the coil changes continuously, inducing an alternating e.m.f. that drives a current through the lamp.'),
                         ('the damping of a moving-coil meter needle', 'The coil is wound on a metal former; when the coil moves, eddy currents are induced in the former that oppose the motion, so the needle settles quickly without oscillating.')])
    return Q(f'Explain how electromagnetic induction is used in {dev}.', ans, 'changing flux identified [1]; induced e.m.f./current and its effect [1]' + ('; reference to Lenz\'s law or energy transfer [1] [3]' if D >= 3 else ' [2]'))


def _gen_c4(r, D):
    N = r.choice([200, 400]); A = r.choice([0.010, 0.015]); B = r.choice([0.10, 0.15]); f = 50.0
    w = 2 * PI * f; E0 = B * A * N * w
    intro = f'A model generator has a coil of {N} turns, each of area {sc(A, 2)} m², rotating at 50 revolutions per second in a field of {nf(B)} T.'
    parts = [
        lambda r: ('Calculate the maximum flux linkage.', f'{E(N * B * A)} Wb', 'NBA [1]'),
        lambda r: ('Calculate the peak e.m.f.', f'{E(E0)} V', 'E₀ = BANω [2]'),
        lambda r: ('State the position of the coil when the e.m.f. is a maximum and explain why.', 'Plane of the coil parallel to the field: flux linkage is zero but changing fastest.', 'parallel to field [1]; max rate of change of flux linkage [1] [2]'),
        lambda r: ('State the effect on the peak e.m.f. and on the frequency of halving the speed of rotation.', 'Both halve.', 'peak e.m.f. halves [1]; frequency halves [1] [2]'),
        lambda r: ('Explain why it is harder to turn the generator when a lamp is connected.', 'Current flows in the coil; by Lenz\'s law the force on it opposes the rotation, so more work is needed (converted to electrical energy).', 'current opposes motion (Lenz) [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t103.add('C4', (2, 3, 4, 5), 'multi_step')(_gen_c4)
CHAPTERS[10] = [t101, t102, t103]

# ===================================================================== 11 Alternating currents
N111 = 'Sinusoidal alternating current: period, frequency and peak values'
t111 = topic(N111, N111.lower(), 'sinusoidal alternating current', 'peak values')
FX(t111, 'C1', (1, 2), [
    ('An alternating current is given by I = 5.0 sin(314t) A. What is its frequency?', '50 Hz', 'ω = 314 rad s⁻¹ = 2πf.', ['314 Hz', '100 Hz', '5.0 Hz']),
    ('An alternating p.d. is given by V = 325 sin(100πt) V. What is its peak value?', '325 V', 'V₀ is the coefficient of the sine.', ['230 V', '100π V', '650 V']),
    ('The peak-to-peak value of an alternating voltage of peak value V₀ is', '2V₀', 'From +V₀ to −V₀.', ['V₀', 'V₀/√2', '√2 V₀']),
    ('An oscilloscope time-base is set at 5.0 ms per division. One cycle of a trace occupies 4.0 divisions. What is the frequency?', '50 Hz', 'T = 20 ms, f = 1/T.', ['20 Hz', '200 Hz', '0.050 Hz']),
    ('The period of a 60 Hz supply is', '16.7 ms', 'T = 1/60 s.', ['60 ms', '6.0 ms', '0.60 s']),
    ('An oscilloscope Y-gain is 2.0 V per division. The trace goes from 3.0 divisions above to 3.0 divisions below the centre. What is the peak p.d.?', '6.0 V', 'Peak = 3.0 div × 2.0 V div⁻¹.', ['12 V', '3.0 V', '4.2 V']),
    ('State what is meant by the period of an alternating current.', 'The time for one complete cycle.', 'time for one cycle [1]'),
])
FX(t111, 'C2', (1, 2, 3, 4), [
    ('Explain why a sinusoidal alternating current transfers energy to a resistor even though its mean value over a cycle is zero.', 'The power I²R depends on the square of the current, which is always positive; energy is transferred in both halves of the cycle regardless of current direction.', 'P = I²R, always positive [1]; energy in both half-cycles [1] [2]'),
    ('Describe how an oscilloscope is used to measure the peak voltage and frequency of an alternating supply.', 'Connect the supply to the Y-input; measure the height from centre to peak in divisions × Y-gain (V div⁻¹) for V₀; measure the horizontal length of one cycle × time-base (s div⁻¹) for T, then f = 1/T.', 'peak from divisions × Y-gain [1]; period from divisions × time-base, f = 1/T [1] [2]'),
    ('Explain the meaning of each symbol in V = V₀ sin ωt.', 'V: instantaneous p.d.; V₀: peak p.d. (amplitude); ω: angular frequency (2πf); t: time.', 'V and V₀ [1]; ω = 2πf and t [1] [2]'),
])


@t111.add('C3', (1, 2, 3, 4, 5), 'case')
def t111_cro(r, D):
    tb = r.choice([0.5, 1.0, 2.0, 5.0, 10.0]); yg = r.choice([0.5, 1.0, 2.0, 5.0, 10.0]); ndiv = r.choice([2.0, 2.5, 4.0, 5.0, 8.0]); hdiv = r.choice([1.5, 2.0, 2.5, 3.0, 3.5])
    T = tb * ndiv * 1e-3; f = 1 / T; V0 = yg * hdiv
    s = f'An oscilloscope displays a sinusoidal trace. The time-base is {nf(tb)} ms div⁻¹ and the Y-gain is {nf(yg)} V div⁻¹. One complete cycle occupies {nf(ndiv)} divisions horizontally, and the trace extends {nf(hdiv)} divisions above and below the centre line.'
    if D <= 2:
        return numq(r, D, s, 'frequency of the signal', f, ' Hz', f'T = {nf(ndiv)} × {nf(tb)} ms = {E(T * 1000)} ms; f = 1/T', [1 / (tb * 1e-3), f * ndiv, 1 / (T * 2)], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Determine the period, the frequency and the peak voltage.', f'T = {E(T * 1000)} ms; f = {E(f)} Hz; V₀ = {nf(V0, 3)} V',
                 f'T = divisions × time-base = {E(T * 1000)} ms [1]; f = 1/T = {E(f)} Hz [1]; V₀ = {nf(hdiv)} × {nf(yg)} = {nf(V0, 3)} V [1] [3]')
    return Q(s + ' (a) Determine the frequency. (b) Determine the peak and peak-to-peak voltages. (c) Write an equation for the voltage V as a function of time t.',
             f'(a) {E(f)} Hz (b) {nf(V0, 3)} V; {nf(2 * V0, 3)} V (c) V = {nf(V0, 3)} sin({E(2 * PI * f)}t)', f'(a) T = {E(T * 1000)} ms [1]; f = {E(f)} Hz [1] (b) peak and peak-to-peak [1] (c) ω = 2πf = {E(2 * PI * f)} rad s⁻¹ [1]; equation [1] [5]', 'multi_step')


@t111.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t111_eq(r, D):
    I0 = r.choice([0.50, 1.2, 2.0, 3.5, 5.0]); f = r.choice([50.0, 60.0, 100.0, 400.0, 1000.0]); w = 2 * PI * f
    t = r.choice([0.6, 1.2, 2.0, 2.5, 3.0]) * 1e-3
    i = I0 * math.sin(w * t)
    s = f'An alternating current is described by I = {nf(I0)} sin({E(w)}t), where I is in amperes and t in seconds.'
    if D <= 2:
        return numq(r, D, s, 'frequency of the current', f, ' Hz', f'ω = 2πf ⇒ f = {E(w)}/2π', [w, 1 / f, w / PI], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + f' State the peak current and calculate the period, and the current at t = {nf(t * 1000)} ms.', f'I₀ = {nf(I0)} A; T = {E(1 / f)} s; I = {nf(i, 3)} A',
                 f'I₀ = {nf(I0)} A and T = 2π/ω = {E(1 / f)} s [1]; substitute t in radians mode [1]; I = {nf(i, 3)} A [1] [3]')
    return Q(s + f' (a) State the peak current and the frequency. (b) Calculate the current at t = {nf(t * 1000)} ms. (c) Calculate the first time after t = 0 at which the current is {nf(I0 / 2)} A.',
             f'(a) {nf(I0)} A; {E(f)} Hz (b) {nf(i, 3)} A (c) {E((PI / 6) / w)} s', f'(a) peak and frequency [1] (b) radians [1]; {nf(i, 3)} A [1] (c) sin ωt = 0.5 ⇒ ωt = π/6 [1]; t = {E((PI / 6) / w)} s [1] [5]', 'multi_step')


def _ac1_c4(r, D):
    V0 = r.choice([12.0, 17.0, 325.0]); f = r.choice([50.0, 60.0])
    intro = f'A sinusoidal alternating supply has a peak p.d. of {nf(V0)} V and a frequency of {nf(f)} Hz. It is displayed on an oscilloscope.'
    parts = [
        lambda r: ('Calculate the period.', f'{E(1000 / f)} ms', 'T = 1/f [1]'),
        lambda r: ('Calculate the angular frequency.', f'{f3(2 * PI * f)} rad s⁻¹', 'ω = 2πf [1]'),
        lambda r: ('Write down an equation for the p.d. V in terms of t.', f'V = {nf(V0)} sin({f3(2 * PI * f)}t)', 'V₀ correct [1]; ω correct [1] [2]'),
        lambda r: ('Suggest suitable time-base and Y-gain settings to display two complete cycles filling about 10 horizontal and 6 vertical divisions.', f'time-base about {E(2000 / f / 10, 2)} ms div⁻¹; Y-gain about {E(V0 / 3, 2)} V div⁻¹', 'time-base [1]; Y-gain [1] [2]'),
        lambda r: ('State the peak-to-peak p.d.', f'{nf(2 * V0)} V', '2V₀ [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t111.add('C4', (2, 3, 4, 5), 'multi_step')(_ac1_c4)

N112 = 'Root-mean-square values and mean power in a resistive load'
t112 = topic(N112, N112.lower(), 'root-mean-square values', 'mean power in a resistive load')
FX(t112, 'C1', (1, 2), [
    ('What is meant by the root-mean-square value of an alternating current?', 'the steady direct current that dissipates the same mean power in a resistor', 'I_rms gives the same heating effect as an equal d.c.', ['the average value of the current over one cycle', 'half the peak value', 'the maximum value of the current']),
    ('A sinusoidal p.d. has a peak value of 325 V. What is its r.m.s. value?', '230 V', 'V_rms = V₀/√2.', ['163 V', '460 V', '325 V']),
    ('For a sinusoidal current in a resistor R with peak current I₀, the mean power is', '½I₀²R', 'P = I_rms²R = I₀²R/2.', ['I₀²R', 'I₀²R/√2', '2I₀²R']),
    ('The peak power in a resistor connected to a sinusoidal supply is P₀. The mean power is', 'P₀/2', 'Mean of sin² is ½.', ['P₀/√2', 'P₀', '2P₀']),
    ('A 12 V r.m.s. sinusoidal supply is connected across a 6.0 Ω resistor. What is the mean power?', '24 W', 'P = V_rms²/R = 144/6.0.', ['48 W', '12 W', '34 W']),
    ('The mains supply in many countries is quoted as 230 V. This value is the', 'r.m.s. value', 'Supply voltages are quoted as r.m.s. values.', ['peak value', 'peak-to-peak value', 'mean value']),
    ('State the relationship between the peak and r.m.s. values of a sinusoidal current.', 'I_rms = I₀/√2', 'I_rms = I₀/√2 [1]'),
])
FX(t112, 'C2', (1, 2, 3, 4), [
    ('Show that the mean power in a resistor carrying a sinusoidal current is half the peak power.', 'P = I²R = I₀²R sin²ωt; the mean value of sin²ωt over a cycle is ½, so mean P = ½I₀²R = ½P₀.', 'P ∝ sin² [1]; mean of sin² = ½ [1] [2]'),
    ('Explain why the r.m.s. value is used rather than the mean value to describe an alternating current.', 'The mean value of a sinusoidal current over a cycle is zero, which says nothing about its heating effect; the r.m.s. value is the equivalent steady current giving the same mean power.', 'mean value is zero [1]; r.m.s. equivalent d.c. for heating [1] [2]'),
    ('Explain why a lamp connected to a 50 Hz supply does not appear to flicker even though its power varies.', 'The power varies at 100 Hz (twice per cycle) and the filament stays hot between peaks; the eye cannot detect such rapid changes.', 'power peaks at 100 Hz [1]; filament thermal inertia / eye persistence [1] [2]'),
    ('Derive the relationship I_rms = I₀/√2 from the definition of r.m.s. value.', 'Mean of I² = I₀² × mean(sin²ωt) = I₀²/2; the square root of this mean is I₀/√2.', 'mean of I² = I₀²/2 [1]; square root [1] [2]'),
])


@t112.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t112_rms(r, D):
    kind = r.choice(['V', 'I'])
    R = r.choice([10.0, 22.0, 47.0, 100.0, 120.0, 470.0])
    if kind == 'V':
        Vr = r.choice([6.0, 12.0, 24.0, 110.0, 120.0, 230.0]); V0 = Vr * math.sqrt(2)
        s = f'A sinusoidal supply of r.m.s. voltage {nf(Vr)} V is connected across a {nf(R)} Ω resistor.'
        if D <= 2:
            return numq(r, D, s, 'peak voltage', V0, ' V', f'V₀ = √2 × V_rms = √2 × {nf(Vr)}', [Vr / math.sqrt(2), 2 * Vr, Vr * 2 * math.sqrt(2)], fm=f3)
        P = Vr * Vr / R
        if D == 3:
            return Q(s + ' Calculate the peak current and the mean power dissipated.', f'I₀ = {E(V0 / R)} A; P = {E(P)} W', f'V₀ = √2 V_rms = {f3(V0)} V [1]; I₀ = V₀/R = {E(V0 / R)} A [1]; P = V_rms²/R = {E(P)} W [1] [3]')
        return Q(s + ' (a) Calculate the peak voltage and the peak current. (b) Calculate the mean power. (c) Calculate the maximum instantaneous power and explain why it is twice the mean power.',
                 f'(a) {f3(V0)} V; {E(V0 / R)} A (b) {E(P)} W (c) {E(2 * P)} W; P = P₀ sin²ωt and the mean of sin² is ½', f'(a) both values [1] (b) P = V_rms²/R = {E(P)} W [1] (c) P₀ = V₀I₀ = {E(2 * P)} W [1]; mean of sin² = ½ [1] [4]', 'multi_step')
    I0 = r.choice([0.50, 1.0, 2.0, 3.0, 4.5]); Ir = I0 / math.sqrt(2); P = Ir * Ir * R
    s = f'A sinusoidal alternating current of peak value {nf(I0)} A flows through a {nf(R)} Ω resistor.'
    if D <= 2:
        return numq(r, D, s, 'mean power dissipated', P, ' W', f'P = ½I₀²R = ½ × {nf(I0)}² × {nf(R)}', [I0 * I0 * R, I0 * I0 * R / math.sqrt(2), Ir * R], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the r.m.s. current and the mean power, and state the value of steady direct current that would give the same heating.', f'I_rms = {f3(Ir)} A; P = {E(P)} W; {f3(Ir)} A d.c.',
                 f'I_rms = I₀/√2 = {f3(Ir)} A [1]; P = I_rms²R = {E(P)} W [1]; equal to I_rms [1] [3]')
    t = r.choice([60, 300, 600])
    return Q(s + f' (a) Calculate the r.m.s. current. (b) Calculate the energy dissipated in {t} s. (c) Calculate the r.m.s. p.d. across the resistor.',
             f'(a) {f3(Ir)} A (b) {E(P * t)} J (c) {f3(Ir * R)} V', f'(a) I₀/√2 = {f3(Ir)} A [1] (b) P = I_rms²R = {E(P)} W [1]; E = Pt = {E(P * t)} J [1] (c) V = I_rms R = {f3(Ir * R)} V [1] [4]', 'multi_step')


@t112.add('C3', (2, 3, 4, 5), 'numerical')
def t112_dev(r, D):
    dev, P, Vr = r.choice([('kettle', 2200.0, 230.0), ('toaster', 900.0, 230.0), ('heater', 1500.0, 120.0), ('hair dryer', 1800.0, 230.0), ('lamp', 60.0, 230.0), ('soldering iron', 40.0, 110.0)])
    Ir = P / Vr; I0 = Ir * math.sqrt(2); R = Vr / Ir
    return Q(f'A {dev} is rated at {nf(P)} W on a {nf(Vr)} V r.m.s. supply in {city(r)}. Calculate the r.m.s. current, the peak current and the resistance of the {dev}.' + (' State the peak power.' if D >= 4 else ''),
             f'I_rms = {f3(Ir)} A; I₀ = {f3(I0)} A; R = {f3(R)} Ω' + (f'; peak power {E(2 * P)} W' if D >= 4 else ''),
             f'I_rms = P/V_rms = {f3(Ir)} A [1]; I₀ = √2 I_rms = {f3(I0)} A [1]; R = V_rms/I_rms = {f3(R)} Ω [1]' + (f'; P₀ = 2P = {E(2 * P)} W [1] [4]' if D >= 4 else ' [3]'))


def _rms_c4(r, D):
    V0 = r.choice([17.0, 34.0, 50.0]); R = r.choice([8.0, 12.0, 20.0])
    Vr = V0 / math.sqrt(2)
    intro = f'A sinusoidal supply of peak voltage {nf(V0)} V is connected to a {nf(R)} Ω resistor.'
    parts = [
        lambda r: ('Define the root-mean-square value of an alternating voltage.', 'The steady d.c. voltage that would give the same mean power in a resistor.', 'equivalent d.c. for same power [1]'),
        lambda r: ('Calculate the r.m.s. voltage.', f'{f3(Vr)} V', 'V₀/√2 [1]'),
        lambda r: ('Calculate the mean power.', f'{E(Vr * Vr / R)} W', 'V_rms²/R [2]'),
        lambda r: ('Calculate the peak power.', f'{E(V0 * V0 / R)} W', 'V₀²/R [1]'),
        lambda r: ('Explain why the mean power is half the peak power.', 'P ∝ sin²ωt and the mean value of sin² over a cycle is ½.', 'mean sin² = ½ [1]'),
        lambda r: ('Calculate the d.c. voltage that would give the same mean power.', f'{f3(Vr)} V', 'equals V_rms [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t112.add('C4', (2, 3, 4, 5), 'multi_step')(_rms_c4)

N113 = 'Rectification and smoothing using diodes and a capacitor'
t113 = topic(N113, N113.lower(), 'rectification', 'smoothing')
FX(t113, 'C1', (1, 2), [
    ('What is meant by rectification?', 'the conversion of alternating current into direct current', 'Rectifiers allow current in one direction only.', ['the conversion of direct current into alternating current', 'the smoothing of a varying d.c. output', 'increasing the voltage of a supply']),
    ('How many diodes are used in a bridge rectifier?', 'four', 'A full-wave bridge uses four diodes.', ['one', 'two', 'six']),
    ('A half-wave rectifier connected to a 50 Hz supply gives an output with', 'one pulse every 20 ms', 'Only one half of each cycle passes.', ['two pulses every 20 ms', 'a steady d.c. output', 'one pulse every 10 ms']),
    ('A smoothing capacitor is connected', 'in parallel with the load resistor', 'It charges at the peaks and discharges through the load between peaks.', ['in series with the load resistor', 'in series with the diode', 'across the a.c. input before the diodes']),
    ('To give better smoothing, the time constant RC of the load and capacitor should be', 'much greater than the period of the rectified supply', 'Slow discharge → small ripple.', ['much less than the period', 'equal to the period', 'zero']),
    ('A full-wave rectifier is connected to a 50 Hz supply. What is the frequency of the ripple on the output?', '100 Hz', 'Two pulses per cycle.', ['50 Hz', '25 Hz', '200 Hz']),
    ('State the difference between half-wave and full-wave rectification.', 'Half-wave: only one half of each cycle is used; full-wave: both halves are used, with the negative half inverted.', 'one half vs both halves [1]'),
])
FX(t113, 'C2', (1, 2, 3, 4), [
    ('Explain how a single capacitor smooths the output of a rectifier.', 'When the rectified p.d. rises the capacitor charges to the peak; as the p.d. falls the diode stops conducting and the capacitor discharges through the load, keeping the p.d. near the peak until the next pulse recharges it.', 'charges at peak [1]; discharges slowly through load between peaks [1] [2]'),
    ('Explain why full-wave rectification gives a smoother output than half-wave rectification for the same smoothing capacitor and load.', 'The capacitor is recharged twice as often (every half-cycle), so it discharges for a shorter time between peaks and the ripple is smaller.', 'twice as many pulses [1]; less time to discharge, smaller ripple [1] [2]'),
    ('Describe how the four diodes in a bridge rectifier ensure the current through the load is always in the same direction.', 'In each half-cycle a different pair of opposite diodes conducts, both routing the current through the load in the same direction; the other pair is reverse-biased.', 'two diodes conduct each half-cycle [1]; same direction through load both halves [1] [2]'),
    ('Explain the effect on the ripple of increasing the load resistance with the same smoothing capacitor.', 'The time constant RC increases, so the capacitor discharges more slowly between peaks and the ripple voltage decreases.', 'RC larger [1]; slower discharge, smaller ripple [1] [2]'),
])


@t113.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t113_ripple(r, D):
    V0 = r.choice([9.0, 12.0, 15.0, 17.0]); f = r.choice([50.0, 60.0]); full = r.choice([True, False])
    R = r.choice([1.0e3, 2.2e3, 4.7e3, 10e3]); C = r.choice([100e-6, 220e-6, 470e-6, 1000e-6])
    T = (1 / f) / (2 if full else 1)
    tau = R * C
    if tau < 3 * T:
        return None
    Vmin = V0 * math.exp(-T / tau); dV = V0 - Vmin
    s = f'The output of a {"full" if full else "half"}-wave rectifier connected to a {nf(f)} Hz supply has a peak value of {nf(V0)} V. A {nf(C * 1e6)} μF smoothing capacitor is connected across a {E(R / 1e3)} kΩ load.'
    if D <= 2:
        return numq(r, D, s, 'time constant of the load and capacitor', tau, ' s', f'τ = RC = {E(R)} × {sc(C)}', [R / C, tau * 1000, T], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + ' Calculate the time between successive peaks of the output and the time constant, and comment on whether the smoothing is effective.', f'{E(T * 1000)} ms; τ = {E(tau)} s; τ ≫ time between peaks, so smoothing is good',
                 f'interval = {E(T * 1000)} ms [1]; τ = RC = {E(tau)} s [1]; τ ≫ interval, small ripple [1] [3]')
    return Q(s + ' Assume the capacitor discharges through the load for the whole interval between peaks. (a) Calculate the time between peaks. (b) Calculate the minimum p.d. across the load. (c) Calculate the peak-to-peak ripple voltage and suggest one way to reduce it.',
             f'(a) {E(T * 1000)} ms (b) {nf(Vmin, 3)} V (c) {E(dV)} V; use a larger capacitance (or full-wave rectification / larger load resistance)',
             f'(a) {E(T * 1000)} ms [1] (b) V = V₀e^(−t/RC) [1]; {nf(Vmin, 3)} V [1] (c) ripple = {E(dV)} V [1]; valid improvement [1] [5]', 'multi_step')


@t113.add('C2', (2, 3, 4), 'explain')
def t113_trace(r, D):
    case, ans = r.choice([('one diode in a bridge rectifier fails and becomes an open circuit', 'Only one of the two current paths works, so the output becomes half-wave: one pulse per cycle, ripple frequency halves.'),
                          ('the smoothing capacitor is removed from a full-wave rectifier circuit', 'The output becomes a series of half-sine pulses at twice the supply frequency, falling to zero between pulses (no smoothing).'),
                          ('the smoothing capacitor is replaced with one of ten times the capacitance', 'RC is ten times larger so the capacitor discharges much less between peaks; the ripple is about ten times smaller.'),
                          ('the single diode in a half-wave rectifier is reversed', 'The other half of each cycle passes: the output pulses are negative instead of positive (same shape and frequency).'),
                          ('the load resistance is halved in a smoothed rectifier circuit', 'RC halves, so the capacitor discharges faster between peaks and the ripple increases (roughly doubles).')])
    return Q(f'Describe and explain the effect on the output p.d. across the load when {case}.', ans, 'correct description of output [1]; explanation [1]' + ('; quantitative comment (frequency or ripple size) [1] [3]' if D >= 3 else ' [2]'))


def _rect_c4(r, D):
    V0 = r.choice([10.0, 12.0]); R = r.choice([2.0e3, 5.0e3]); C = r.choice([220e-6, 470e-6])
    T = 0.010
    intro = f'A bridge rectifier is connected to a 50 Hz supply of peak voltage {nf(V0)} V (ignore p.d.s across the diodes). The output is connected to a {E(R / 1e3)} kΩ load with a {nf(C * 1e6)} μF capacitor in parallel.'
    parts = [
        lambda r: ('State the purpose of the four diodes.', 'Full-wave rectification: current through the load in one direction in both half-cycles.', 'full-wave rectification [1]'),
        lambda r: ('Describe the output without the capacitor.', 'Half-sine pulses, all positive, 100 per second, peak 12 V.'.replace('12', nf(V0)), 'all positive pulses [1]; 100 Hz [1] [2]'),
        lambda r: ('Calculate the time constant of the smoothing circuit.', f'{E(R * C)} s', 'RC [1]'),
        lambda r: ('Calculate the ripple voltage, assuming discharge for 10 ms between peaks.', f'{E(V0 * (1 - math.exp(-T / (R * C))))} V', 'V₀(1 − e^(−t/RC)) [3]'),
        lambda r: ('Explain why the time constant must be much larger than 10 ms for good smoothing.', 'Then the capacitor loses only a small fraction of its charge between peaks.', 'small fractional discharge [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t113.add('C4', (2, 3, 4, 5), 'multi_step')(_rect_c4)
CHAPTERS[11] = [t111, t112, t113]

# ===================================================================== 12 Quantum physics
EV = QE
METALS = [('caesium', 2.1), ('potassium', 2.3), ('sodium', 2.3), ('calcium', 2.9), ('magnesium', 3.7), ('zinc', 4.3), ('aluminium', 4.1), ('copper', 4.7), ('platinum', 5.6), ('lithium', 2.9)]

N121 = 'Photons: energy E = hf and momentum and the photoelectric effect'
t121 = topic(N121, N121.lower(), 'photons', 'photoelectric effect')
FX(t121, 'C1', (1, 2), [
    ('What is a photon?', 'a quantum (discrete packet) of electromagnetic energy', 'E = hf for each photon.', ['a particle of matter with charge e', 'a wave packet of sound', 'the nucleus of a hydrogen atom']),
    ('What is the energy of a photon of frequency 5.0 × 10¹⁴ Hz?', '3.3 × 10⁻¹⁹ J', 'E = hf = 6.63 × 10⁻³⁴ × 5.0 × 10¹⁴.', ['1.3 × 10⁻⁴⁸ J', '7.5 × 10⁴⁷ J', '3.3 × 10⁻²⁰ J']),
    ('Which expression gives the momentum of a photon of energy E?', 'E/c', 'p = E/c = h/λ.', ['Ec', 'E/c²', 'Ec²']),
    ('What is 1 eV in joules?', '1.60 × 10⁻¹⁹ J', 'Energy gained by an electron through 1 V.', ['1.00 J', '6.25 × 10¹⁸ J', '9.11 × 10⁻³¹ J']),
    ('Which observation of the photoelectric effect cannot be explained by a wave theory of light?', 'no electrons are emitted below a threshold frequency, however intense the light', 'Wave theory predicts emission at any frequency given enough intensity.', ['the number of electrons emitted increases with intensity', 'the emitted electrons have a range of kinetic energies', 'electrons are emitted from metal surfaces']),
    ('Increasing the intensity of light (above threshold frequency) on a metal surface increases', 'the number of photoelectrons emitted per second', 'More photons per second; each photon energy unchanged.', ['the maximum kinetic energy of the photoelectrons', 'the work function', 'the threshold frequency']),
    ('Photon A has twice the wavelength of photon B. The energy of A is', 'half that of B', 'E = hc/λ.', ['twice that of B', 'four times that of B', 'the same as B']),
    ('Define the electronvolt.', 'The energy gained by an electron accelerated through a potential difference of 1 V (1.60 × 10⁻¹⁹ J).', 'electron through 1 V [1]'),
])
FX(t121, 'C2', (1, 2, 3, 4), [
    ('Explain why photoelectric emission is instantaneous, even with very dim light.', 'Each electron absorbs the energy of one photon in a single interaction; if hf exceeds the work function, emission happens at once. Energy does not need to build up gradually as wave theory predicts.', 'one photon – one electron interaction [1]; no build-up time [1] [2]'),
    ('Explain why the maximum kinetic energy of photoelectrons does not depend on the intensity of the light.', 'Each electron absorbs one photon of energy hf; intensity only changes the number of photons per second, not the energy of each, so Ek(max) = hf − Φ is unchanged.', 'one photon per electron, energy hf [1]; intensity changes number of photons only [1] [2]'),
    ('Explain how the photoelectric effect provides evidence for the particulate nature of electromagnetic radiation.', 'The existence of a threshold frequency, the instant emission, and Ek(max) depending on frequency (not intensity) can only be explained if light arrives in discrete photons of energy hf, each absorbed by one electron.', 'threshold frequency / instantaneous emission [1]; explained only by photons E = hf [1] [2]'),
    ('Show that the momentum of a photon is p = h/λ.', 'E = hf = hc/λ and for a photon p = E/c, so p = (hc/λ)/c = h/λ.', 'p = E/c [1]; substitute E = hc/λ [1] [2]'),
])

SOURCES = [('a red laser pointer', 650e-9, (1.0e-3, 5.0e-3)), ('a green laser', 532e-9, (5.0e-3, 0.020)), ('a blue LED', 450e-9, (0.050, 0.10)), ('an ultraviolet lamp', 254e-9, (2.0, 5.0)),
           ('an infrared remote-control LED', 940e-9, (0.010, 0.030)), ('a radio transmitter', 3.0, (1.0e3, 5.0e4)), ('an X-ray tube', 1.0e-10, (1.0, 10.0)), ('a sodium street lamp', 589e-9, (35.0, 90.0))]


@t121.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t121_photon(r, D):
    src, lam, (Plo, Phi) = r.choice(SOURCES)
    P = r.choice([Plo, Phi, (Plo + Phi) / 2])
    Eph = HP * C0 / lam; N = P / Eph; p = HP / lam
    s = f'{cap(src)} emits electromagnetic radiation of wavelength {E(lam)} m with a power of {E(P, 2)} W.'
    if D <= 2:
        return numq(r, D, s, 'energy of one photon', Eph, ' J', f'E = hc/λ = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/{E(lam)}', [HP * lam / C0, HP * C0 * lam, Eph / QE], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(s + ' Calculate the energy of one photon, in J and in eV, and the number of photons emitted per second.', f'E = {sc(Eph)} J = {E(Eph / QE)} eV; N = {sc(N)} s⁻¹',
                 f'E = hc/λ = {sc(Eph)} J [1]; ÷ 1.60 × 10⁻¹⁹ = {E(Eph / QE)} eV [1]; N = P/E = {sc(N)} s⁻¹ [1] [3]')
    F = P / C0
    return Q(s + ' (a) Calculate the number of photons emitted per second. (b) Calculate the momentum of one photon. (c) The beam is completely absorbed by a surface. Calculate the force on the surface.',
             f'(a) {sc(N)} s⁻¹ (b) {sc(p)} N s (c) {sc(F)} N', f'(a) E = hc/λ [1]; N = P/E = {sc(N)} s⁻¹ [1] (b) p = h/λ = {sc(p)} N s [1] (c) F = rate of change of momentum = Np [1]; = P/c = {sc(F)} N [1] [5]', 'multi_step')


@t121.add('C3', (1, 2, 3, 4), 'numerical')
def t121_ev(r, D):
    lam = r.choice([400e-9, 450e-9, 500e-9, 550e-9, 600e-9, 700e-9, 250e-9, 120e-9])
    Eev = HP * C0 / lam / QE
    if D <= 2:
        return numq(r, D, f'Light of wavelength {nf(lam * 1e9)} nm is incident on a surface.', 'photon energy in electronvolts', Eev, ' eV', f'E = hc/(λe) = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/({sc(lam)} × 1.60 × 10⁻¹⁹)', [Eev * QE, 1 / Eev, Eev * 10], fm=f3)
    E2 = r.choice([1.8, 2.5, 3.1, 4.9, 6.0])
    lam2 = HP * C0 / (E2 * QE)
    return Q(f'A photon has energy {nf(E2)} eV. Calculate its energy in joules, its frequency and its wavelength, and state the region of the electromagnetic spectrum.' if D >= 3 else '',
             f'{sc(E2 * QE)} J; {sc(E2 * QE / HP)} Hz; {nf(lam2 * 1e9, 3)} nm; ' + ('visible' if 400e-9 <= lam2 <= 700e-9 else ('ultraviolet' if lam2 < 400e-9 else 'infrared')),
             f'E × 1.60 × 10⁻¹⁹ = {sc(E2 * QE)} J [1]; f = E/h = {sc(E2 * QE / HP)} Hz [1]; λ = c/f = {nf(lam2 * 1e9, 3)} nm [1]' + (' ; region [1] [4]' if D >= 4 else ' [3]'))


def _ph_c4(r, D):
    lam = r.choice([405e-9, 532e-9, 650e-9]); P = r.choice([1.0e-3, 5.0e-3])
    Eph = HP * C0 / lam
    intro = f'A laser emits light of wavelength {nf(lam * 1e9)} nm with an output power of {nf(P * 1000)} mW.'
    parts = [
        lambda r: ('State what is meant by a photon.', 'A discrete quantum (packet) of electromagnetic energy.', 'packet / quantum of energy [1]'),
        lambda r: ('Calculate the energy of a photon.', f'{sc(Eph)} J', 'E = hc/λ [2]'),
        lambda r: ('Calculate the number of photons emitted per second.', f'{sc(P / Eph)} s⁻¹', 'N = P/E [2]'),
        lambda r: ('Calculate the momentum of a photon.', f'{sc(HP / lam)} N s', 'p = h/λ [1]'),
        lambda r: ('Explain why this light may not cause photoelectric emission from copper (work function 4.7 eV).', f'Photon energy {f3(Eph / QE)} eV is less than the work function, so no electron can gain enough energy to escape.', 'photon energy in eV [1]; less than Φ so no emission [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t121.add('C4', (2, 3, 4, 5), 'multi_step')(_ph_c4)

N122 = "Work function, threshold frequency and Einstein's photoelectric equation"
t122 = topic(N122, N122.lower(), 'work function', "einstein's photoelectric equation")
FX(t122, 'C1', (1, 2), [
    ('What is meant by the work function of a metal?', 'the minimum energy needed to remove an electron from the surface of the metal', 'Φ = hf₀.', ['the energy of the most energetic photoelectron', 'the energy needed to remove an electron from an atom of the metal in a gas', 'the kinetic energy of a free electron in the metal']),
    ('Which is Einstein\'s photoelectric equation?', 'hf = Φ + ½mv²(max)', 'Photon energy = work function + maximum KE.', ['hf = Φ − ½mv²(max)', 'Φ = hf + ½mv²(max)', 'hf = ½mv²(max)']),
    ('A metal has a work function of 3.2 × 10⁻¹⁹ J. What is its threshold frequency?', '4.8 × 10¹⁴ Hz', 'f₀ = Φ/h.', ['2.1 × 10⁻¹⁵ Hz', '2.1 × 10¹⁵ Hz', '4.8 × 10¹⁵ Hz']),
    ('A graph of maximum kinetic energy of photoelectrons against frequency of the light is a straight line. Its gradient is', 'the Planck constant', 'Ek = hf − Φ.', ['the work function', 'the threshold frequency', 'the charge on the electron']),
    ('The intercept on the frequency axis of a graph of Ek(max) against f gives', 'the threshold frequency', 'Ek = 0 when f = f₀.', ['the work function', 'the Planck constant', 'the stopping potential']),
    ('Why do photoelectrons have a range of kinetic energies up to a maximum?', 'some electrons lose energy before escaping from below the surface', 'Only surface electrons with the minimum energy loss have Ek(max).', ['photons have a range of energies for one frequency', 'the work function varies with time', 'electrons gain energy from several photons']),
    ('State what is meant by threshold frequency.', 'The minimum frequency of electromagnetic radiation that causes photoelectric emission from a given surface.', 'minimum frequency for emission [1]'),
])
FX(t122, 'C2', (1, 2, 3, 4), [
    ('Explain why there is a threshold frequency for photoelectric emission.', 'Each electron absorbs one photon of energy hf; it can only escape if hf ≥ Φ. Below f₀ = Φ/h no single photon has enough energy, however many arrive.', 'one photon per electron [1]; hf must be ≥ Φ, f₀ = Φ/h [1] [2]'),
    ('Explain how a graph of Ek(max) against frequency can be used to find the Planck constant and the work function.', 'Ek(max) = hf − Φ: a straight line with gradient h and intercept −Φ on the Ek axis (f₀ on the f axis, Φ = hf₀).', 'gradient = h [1]; intercept gives −Φ or f₀ [1] [2]'),
    ('Explain why graphs of Ek(max) against frequency for different metals are parallel lines.', 'The gradient of each is h, the same universal constant; only the work function (intercept) differs between metals.', 'gradient h for all [1]; different intercepts Φ [1] [2]'),
    ('Explain why the photoelectric current increases with intensity but Ek(max) does not.', 'Greater intensity means more photons per second, so more electrons emitted per second (larger current); each photon still has energy hf, so Ek(max) is unchanged.', 'more photons → more electrons [1]; same photon energy [1] [2]'),
])


@t122.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t122_eq(r, D):
    met, phi = r.choice(METALS)
    lam = r.choice([200e-9, 250e-9, 300e-9, 350e-9, 400e-9, 450e-9])
    Eph = HP * C0 / lam; W = phi * QE; Ek = Eph - W
    if Ek <= 0.05 * QE:
        return None
    s = f'Light of wavelength {nf(lam * 1e9)} nm falls on a clean {met} surface. The work function of {met} is {nf(phi)} eV.'
    if D <= 2:
        return numq(r, D, s, 'maximum kinetic energy of the photoelectrons', Ek, ' J', f'Ek = hc/λ − Φ = {sc(Eph)} − {sc(W)}', [Eph, Eph + W, Ek / QE], fm=lambda x: sc(x, 3))
    v = math.sqrt(2 * Ek / ME); f0 = W / HP
    if D == 3:
        return Q(s + ' Calculate the maximum kinetic energy of the photoelectrons and their maximum speed.', f'Ek = {sc(Ek)} J; v = {sc(v)} m s⁻¹',
                 f'Φ = {sc(W)} J and hc/λ = {sc(Eph)} J [1]; Ek = {sc(Ek)} J [1]; v = √(2Ek/m) = {sc(v)} m s⁻¹ [1] [3]')
    return Q(s + ' (a) Calculate the threshold frequency of the metal. (b) Calculate the maximum kinetic energy of the photoelectrons, in eV. (c) Calculate the stopping potential needed to prevent the fastest electrons reaching a collector.',
             f'(a) {sc(f0)} Hz (b) {nf(Ek / QE, 3)} eV (c) {nf(Ek / QE, 3)} V', f'(a) f₀ = Φ/h = {sc(f0)} Hz [1] (b) hf = Φ + Ek [1]; {nf(Ek / QE, 3)} eV [1] (c) eV_s = Ek(max) [1]; {nf(Ek / QE, 3)} V [1] [5]', 'multi_step')


@t122.add('C3', (2, 3, 4, 5), 'case')
def t122_graph(r, D):
    met, phi = r.choice(METALS)
    f0 = phi * QE / HP
    fs = [f0 * k for k in (1.2, 1.4, 1.6, 1.8, 2.0)]
    Ek = [(HP * f - phi * QE) / QE for f in fs]
    rows = '; '.join(f'f = {sc(f, 3)} Hz, Ek(max) = {nf(e, 3)} eV' for f, e in zip(fs, Ek))
    g = (Ek[-1] - Ek[0]) * QE / (fs[-1] - fs[0])
    return Q(f'In a photoelectric experiment on {met}, these results are obtained: {rows}. A graph of Ek(max) (in J) against f is plotted. Use the data to determine the Planck constant and the work function in eV.' + (' Explain why the line does not pass through the origin.' if D >= 4 else ''),
             f'h = gradient = {sc(g)} J s; Φ = {nf(phi, 3)} eV' + ('; Ek = hf − Φ, and no electrons are emitted below f₀' if D >= 4 else ''),
             f'convert eV to J [1]; gradient = h = {sc(g)} J s [1]; Φ = hf₀ or from intercept = {nf(phi, 3)} eV [1]' + ('; intercept/threshold explanation [1] [4]' if D >= 4 else ' [3]'))


def _pe_c4(r, D):
    met, phi = r.choice(METALS[:5])
    lam = r.choice([300e-9, 350e-9, 400e-9])
    Eph = HP * C0 / lam; Ek = Eph - phi * QE
    intro = f'Ultraviolet light of wavelength {nf(lam * 1e9)} nm is shone onto a {met} plate (work function {nf(phi)} eV) connected to a sensitive ammeter circuit.'
    parts = [
        lambda r: ('Define work function.', 'Minimum energy needed to remove an electron from the surface of the metal.', 'minimum energy, from surface [1]'),
        lambda r: ('Calculate the threshold wavelength.', f'{nf(HP * C0 / (phi * QE) * 1e9, 3)} nm', 'λ₀ = hc/Φ [2]'),
        lambda r: ('Calculate the maximum kinetic energy of the photoelectrons.', f'{sc(Ek)} J', 'hf − Φ [2]'),
        lambda r: ('State and explain the effect on the current of doubling the light intensity.', 'Current doubles: twice as many photons per second release twice as many electrons.', 'current doubles [1]; twice as many photons per second [1] [2]'),
        lambda r: ('State and explain the effect on Ek(max) of doubling the intensity.', 'No change: photon energy unchanged.', 'unchanged with reason [1]'),
        lambda r: ('Explain why the electrons are emitted with a range of kinetic energies.', 'Electrons from below the surface lose energy in escaping; only surface electrons have Ek(max).', 'energy lost below surface [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t122.add('C4', (2, 3, 4, 5), 'multi_step')(_pe_c4)

N123 = 'Wave-particle duality and electron diffraction: λ = h/p'
t123 = topic(N123, N123.lower(), 'wave-particle duality', 'electron diffraction')
FX(t123, 'C1', (1, 2), [
    ('Which experiment provides evidence that electrons have wave properties?', 'electron diffraction by a thin crystalline film', 'Rings are a diffraction pattern; λ = h/p.', ['the photoelectric effect', 'α-particle scattering', 'the deflection of electrons in a magnetic field']),
    ('The de Broglie wavelength of a particle of momentum p is', 'h/p', 'λ = h/p.', ['hp', 'p/h', 'h/p²']),
    ('An electron and a proton have the same speed. Which has the longer de Broglie wavelength?', 'the electron', 'Smaller mass → smaller momentum → longer λ.', ['the proton', 'they have the same wavelength', 'neither has a wavelength']),
    ('Electrons are accelerated through a larger p.d. in an electron diffraction tube. The rings on the screen', 'become smaller', 'Greater speed → shorter λ → less diffraction.', ['become larger', 'stay the same size', 'disappear']),
    ('Why does a moving tennis ball not show noticeable diffraction?', 'its de Broglie wavelength is far smaller than any gap it passes through', 'Huge momentum gives λ ~ 10⁻³⁴ m.', ['it has no de Broglie wavelength', 'it is not charged', 'it moves too slowly']),
    ('Which phenomenon provides evidence for the particulate nature of electromagnetic radiation?', 'the photoelectric effect', 'Photons of energy hf.', ['diffraction', 'interference', 'polarisation']),
    ('State the de Broglie relation.', 'λ = h/p, where p is the momentum of the particle.', 'λ = h/p [1]'),
])
FX(t123, 'C2', (1, 2, 3, 4), [
    ('Explain what is meant by wave-particle duality.', 'Both electromagnetic radiation and matter show wave properties in some experiments (diffraction, interference) and particle properties in others (photoelectric effect, collisions); neither model alone describes all behaviour.', 'both waves and matter show both behaviours [1]; examples of each [1] [2]'),
    ('Explain why electron diffraction is observed with graphite but not with a ruled diffraction grating for visible light.', 'Electron wavelengths (~10⁻¹¹ m) are comparable with the spacing of atoms in graphite (~10⁻¹⁰ m); a ruled grating has spacing ~10⁻⁶ m, far too large to diffract the electrons noticeably.', 'λ comparable to atomic spacing [1]; grating spacing too large [1] [2]'),
    ('Explain why the diffraction rings get smaller when the accelerating voltage in an electron diffraction tube is increased.', 'Higher V gives greater momentum (p = √(2meV)), so λ = h/p decreases; shorter wavelength is diffracted through smaller angles, giving smaller rings.', 'greater p, smaller λ [1]; smaller diffraction angle [1] [2]'),
])


@t123.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t123_db(r, D):
    part, m = r.choice([('an electron', ME), ('a proton', MP), ('a neutron', 1.675e-27)])
    if part == 'an electron':
        V = r.choice([50.0, 100.0, 150.0, 500.0, 2000.0, 5000.0])
        Ek = QE * V; p = math.sqrt(2 * m * Ek); lam = HP / p
        s = f'Electrons are accelerated from rest through a potential difference of {nf(V)} V.'
        wk = f'p = √(2meV) = {sc(p)} kg m s⁻¹; λ = h/p'
    else:
        v = r.choice([2.0e3, 5.0e3, 1.0e4, 2.5e4])
        p = m * v; lam = HP / p; Ek = 0.5 * m * v * v
        s = f'{cap(part)} moves at {sc(v, 2)} m s⁻¹.'
        wk = f'p = mv = {sc(p)} kg m s⁻¹; λ = h/p'
    if D <= 2:
        return numq(r, D, s, 'de Broglie wavelength', lam, ' m', wk, [HP * p, lam * 10, p / HP], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(s + ' Calculate the momentum and the de Broglie wavelength of each particle.', f'p = {sc(p)} kg m s⁻¹; λ = {sc(lam)} m', f'momentum method [1]; p = {sc(p)} kg m s⁻¹ [1]; λ = h/p = {sc(lam)} m [1] [3]')
    return Q(s + ' (a) Calculate the de Broglie wavelength. (b) The particles pass through a crystal with atomic spacing about 2 × 10⁻¹⁰ m. State and explain whether a diffraction pattern is expected. (c) State the effect on the wavelength of doubling the momentum.',
             f'(a) {sc(lam)} m (b) ' + ('yes: λ is comparable with the spacing' if 1e-12 < lam < 2e-9 else 'little noticeable diffraction: λ is very different from the spacing') + ' (c) λ halves',
             f'(a) p found [1]; λ = h/p = {sc(lam)} m [1] (b) compare λ with spacing [1] (c) λ ∝ 1/p [1] [4]', 'multi_step')


@t123.add('C3', (2, 3, 4), 'numerical')
def t123_match(r, D):
    lam = r.choice([1.0e-10, 1.5e-10, 2.0e-10, 5.0e-11])
    p = HP / lam; v = p / ME; V = p * p / (2 * ME * QE)
    return Q(f'An electron is required to have a de Broglie wavelength of {sc(lam, 2)} m, similar to the spacing of atoms in a crystal. Calculate its momentum, its speed and the accelerating p.d. needed.',
             f'p = {sc(p)} kg m s⁻¹; v = {sc(v)} m s⁻¹; V = {E(V)} V', f'p = h/λ = {sc(p)} kg m s⁻¹ [1]; v = p/m = {sc(v)} m s⁻¹ [1]; eV = p²/2m ⇒ V = {E(V)} V [1]' + (' [3]' if D <= 3 else '; check that v ≪ c so non-relativistic [1] [4]'))


def _wpd_c4(r, D):
    V = r.choice([3000.0, 4000.0, 5000.0])
    p = math.sqrt(2 * ME * QE * V); lam = HP / p
    intro = f'In an electron diffraction tube, electrons are accelerated through {nf(V)} V and pass through a thin layer of graphite. Concentric rings are seen on a fluorescent screen.'
    parts = [
        lambda r: ('Explain how the rings show that electrons behave as waves.', 'Rings are a diffraction pattern, which is a wave property.', 'diffraction is a wave property [1]'),
        lambda r: ('Calculate the kinetic energy of an electron.', f'{sc(QE * V)} J', 'Ek = eV [1]'),
        lambda r: ('Calculate the momentum of an electron.', f'{sc(p)} kg m s⁻¹', 'p = √(2mEk) [2]'),
        lambda r: ('Calculate the de Broglie wavelength.', f'{sc(lam)} m', 'λ = h/p [1]'),
        lambda r: ('State and explain the effect on the rings of increasing the accelerating voltage.', 'Rings get smaller: higher p gives smaller λ, so less diffraction.', 'rings smaller [1]; larger p, smaller λ, less diffraction [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t123.add('C4', (2, 3, 4, 5), 'multi_step')(_wpd_c4)

N124 = 'Energy levels, line spectra and emission and absorption'
t124 = topic(N124, N124.lower(), 'energy levels', 'line spectra')
HLEV = [-13.6, -3.40, -1.51, -0.850, -0.544]
FX(t124, 'C1', (1, 2), [
    ('Why do isolated atoms emit line spectra rather than continuous spectra?', 'the electrons can only occupy discrete energy levels', 'Photon energy = difference between discrete levels.', ['the atoms move with a range of speeds', 'the electrons have a continuous range of energies', 'the light is diffracted by the atoms']),
    ('An electron falls from a level at −3.40 eV to one at −13.6 eV. What is the energy of the photon emitted?', '10.2 eV', 'ΔE = 13.6 − 3.40.', ['17.0 eV', '3.40 eV', '13.6 eV']),
    ('A cool gas is placed between a white-light source and a spectrometer. What is observed?', 'dark lines on a continuous spectrum', 'An absorption spectrum.', ['bright lines on a dark background', 'a continuous spectrum only', 'no light at all']),
    ('How many different photon energies can be emitted by electrons moving between four energy levels?', '6', '4C2 = 6 transitions.', ['4', '3', '12']),
    ('The photon emitted in a transition between levels E₁ and E₂ has frequency', '(E₂ − E₁)/h', 'hf = E₂ − E₁.', ['h(E₂ − E₁)', '(E₂ + E₁)/h', '(E₂ − E₁)/c']),
    ('Why are energy levels in an atom given negative values?', 'the zero of energy is taken as the electron completely free of the atom', 'Energy must be supplied to free a bound electron.', ['electrons have negative charge', 'the energy of the nucleus is negative', 'the electrons move in the negative direction']),
    ('State what is meant by an emission line spectrum.', 'A series of bright lines of discrete wavelengths on a dark background, emitted by excited atoms of a gas.', 'bright discrete lines on dark background [1]'),
])
FX(t124, 'C2', (1, 2, 3, 4), [
    ('Explain how an emission line spectrum is produced by a hot gas.', 'Electrons in the atoms are excited to higher energy levels; when they fall to lower levels each emits a photon of energy equal to the difference between the levels, hf = E₁ − E₂. Only certain differences exist, so only certain wavelengths (lines) appear.', 'excitation then de-excitation [1]; photon energy = level difference, discrete [1] [2]'),
    ('Explain why an absorption spectrum has dark lines at the same wavelengths as the emission lines of the same gas.', 'Atoms absorb only photons whose energy equals a difference between their energy levels — the same differences that give the emission lines; these photons are removed from the beam and re-emitted in all directions, so the lines are dark.', 'absorb photons of energy = level difference [1]; re-emitted in all directions so dark in beam direction [1] [2]'),
    ('Explain why the spectrum of a gas provides evidence for discrete electron energy levels in atoms.', 'Only specific wavelengths are emitted, so only specific photon energies; since hf = ΔE, only specific energy differences exist, which requires discrete levels.', 'discrete wavelengths/energies [1]; implies discrete levels [1] [2]'),
])


@t124.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t124_lines(r, D):
    i, j = sorted(r.sample(range(5), 2))
    Eu, El = HLEV[j], HLEV[i]
    dE = (Eu - El) * QE; lam = HP * C0 / dE
    reg = 'ultraviolet' if lam < 400e-9 else ('visible' if lam <= 700e-9 else 'infrared')
    s = f'Some energy levels of the hydrogen atom are −13.6 eV, −3.40 eV, −1.51 eV, −0.850 eV and −0.544 eV. An electron makes a transition from the {nf(Eu, 3)} eV level to the {nf(El, 3)} eV level.'
    if D <= 2:
        return numq(r, D, s, 'energy of the emitted photon', Eu - El, ' eV', f'ΔE = {nf(Eu, 3)} − ({nf(El, 3)})', [-Eu, -El, -(Eu + El)], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the wavelength of the photon emitted and state the region of the spectrum.', f'{sc(lam)} m; {reg}', f'ΔE = {nf(Eu - El, 3)} eV = {sc(dE)} J [1]; λ = hc/ΔE = {sc(lam)} m [1]; {reg} [1] [3]')
    Eion = -El
    return Q(s + f' (a) Calculate the wavelength of the photon emitted. (b) State the number of different photon energies that could be emitted as electrons fall from the {nf(Eu, 3)} eV level to the ground state by all possible routes. (c) Calculate the minimum energy, in J, needed to ionise a hydrogen atom whose electron is in the {nf(El, 3)} eV level.',
             f'(a) {sc(lam)} m (b) {j * (j + 1) // 2} (c) {sc(Eion * QE)} J', f'(a) ΔE in J [1]; λ = hc/ΔE = {sc(lam)} m [1] (b) count transitions = {j * (j + 1) // 2} [1] (c) {nf(Eion, 3)} eV × 1.60 × 10⁻¹⁹ [1]; {sc(Eion * QE)} J [1] [5]', 'multi_step')


@t124.add('C3', (2, 3, 4), 'numerical')
def t124_find(r, D):
    lam = r.choice([656e-9, 486e-9, 434e-9, 589e-9, 122e-9, 103e-9])
    dE = HP * C0 / lam / QE
    lower = r.choice([-3.40, -13.6, -5.14, -1.51])
    if lower + dE > -0.05:
        return None
    return Q(f'A spectral line of wavelength {nf(lam * 1e9)} nm is observed in the spectrum of a gas. It is produced by electrons falling to an energy level of {nf(lower, 3)} eV. Calculate the photon energy in eV and the energy of the upper level.',
             f'{nf(dE, 3)} eV; {nf(lower + dE, 3)} eV', f'E = hc/λ = {sc(dE * QE)} J [1]; = {nf(dE, 3)} eV [1]; upper level = {nf(lower, 3)} + {nf(dE, 3)} = {nf(lower + dE, 3)} eV [1]' + (' [3]' if D <= 3 else '; comment on sign (still bound, negative) [1] [4]'))


def _lev_c4(r, D):
    levs = sorted(r.sample([-10.4, -5.5, -3.7, -1.6, -0.9], 3))
    a, b, c = levs
    intro = f'An atom has three energy levels at {nf(a)} eV, {nf(b)} eV and {nf(c)} eV.'
    parts = [
        lambda r: ('State the number of different photon energies that can be emitted.', '3', 'three transitions [1]'),
        lambda r: ('Calculate the largest photon energy emitted, in joules.', f'{sc((c - a) * QE)} J', 'ΔE × e [2]'),
        lambda r: ('Calculate the longest wavelength emitted.', f'{sc(HP * C0 / ((c - b) * QE))} m', 'smallest ΔE, λ = hc/ΔE [2]'),
        lambda r: ('Explain why the energy levels are negative.', 'Zero is the energy of an electron just free of the atom; bound electrons have less energy.', 'zero at ionisation [1]'),
        lambda r: ('Explain the difference between an emission and an absorption spectrum.', 'Emission: bright lines from excited atoms; absorption: dark lines in a continuous spectrum where cool atoms absorb photons of the same energies.', 'emission bright lines [1]; absorption dark lines in continuum [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t124.add('C4', (2, 3, 4, 5), 'multi_step')(_lev_c4)
CHAPTERS[12] = [t121, t122, t123, t124]

# ===================================================================== 13 Nuclear physics
MPU, MNU = 1.007276, 1.008665
NUCS = [(4, 2, 'He', 4.001506), (7, 3, 'Li', 7.014357), (9, 4, 'Be', 9.010986), (12, 6, 'C', 11.996709), (14, 7, 'N', 13.999231), (16, 8, 'O', 15.990526), (56, 26, 'Fe', 55.920670), (235, 92, 'U', 234.993422), (2, 1, 'H', 2.013553)]
MEV = 1e6 * QE


def be(A, Z, m):
    dm = Z * MPU + (A - Z) * MNU - m
    return dm, dm * UU * C0 ** 2


N131 = 'Mass defect, binding energy and E = mc²'
t131 = topic(N131, N131.lower(), 'mass defect', 'binding energy')
FX(t131, 'C1', (1, 2), [
    ('What is meant by the mass defect of a nucleus?', 'the difference between the total mass of the separate nucleons and the mass of the nucleus', 'Δm = Zmₚ + (A − Z)mₙ − m(nucleus).', ['the mass of the electrons in the atom', 'the mass lost when the nucleus emits an α-particle', 'the difference between the nucleon number and the proton number']),
    ('Which is the definition of the binding energy of a nucleus?', 'the minimum energy needed to separate the nucleus into its individual protons and neutrons', 'Binding energy = Δmc².', ['the energy released when the nucleus decays', 'the energy needed to remove one electron', 'the kinetic energy of the nucleons']),
    ('A mass of 1.0 × 10⁻³ kg is converted completely into energy. How much energy is released?', '9.0 × 10¹³ J', 'E = mc² = 1.0 × 10⁻³ × (3.00 × 10⁸)².', ['3.0 × 10⁵ J', '9.0 × 10¹⁶ J', '3.0 × 10¹¹ J']),
    ('A mass defect of 1 u corresponds to an energy of approximately', '930 MeV', '1 u × c² ≈ 1.49 × 10⁻¹⁰ J ≈ 930 MeV.', ['1 MeV', '9.3 MeV', '9300 MeV']),
    ('The mass of a nucleus is', 'less than the total mass of its separate nucleons', 'Energy is released when nucleons bind, so mass decreases.', ['greater than the total mass of its separate nucleons', 'equal to the total mass of its separate nucleons', 'equal to the mass of its protons only']),
    ('In the equation E = mc², c is', 'the speed of light in a vacuum', 'c = 3.00 × 10⁸ m s⁻¹.', ['the speed of the nucleus', 'a constant equal to 1', 'the speed of sound']),
    ('State the equation linking a change in mass to the energy released.', 'ΔE = Δmc²', 'ΔE = c²Δm [1]'),
])
FX(t131, 'C2', (1, 2, 3, 4), [
    ('Explain why the mass of a nucleus is less than the total mass of its separate nucleons.', 'When nucleons come together energy is released (binding energy); by E = mc² this released energy corresponds to a loss of mass, the mass defect.', 'energy released on binding [1]; equivalent mass lost, E = Δmc² [1] [2]'),
    ('Explain why energy must be supplied to separate a nucleus into its nucleons.', 'The nucleons are held together by the strong nuclear force; work must be done against it, equal to the binding energy, which reappears as the extra mass of the separate nucleons.', 'work against strong force [1]; equals binding energy / mass increases [1] [2]'),
    ('Explain why the binding energy of a nucleus is a positive quantity even though the nucleus has less mass than its parts.', 'Binding energy is defined as the energy that must be supplied to separate the nucleons, so it is positive; the nucleus is in a lower energy state, hence its smaller mass.', 'defined as energy supplied to separate [1]; nucleus lower energy/mass [1] [2]'),
])


@t131.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t131_be(r, D):
    A, Z, X, m = r.choice(NUCS)
    dm, Eb = be(A, Z, m)
    s = f'The mass of a {nuc(A, Z, X)} nucleus is {m:.6f} u. The mass of a proton is 1.007276 u and the mass of a neutron is 1.008665 u (1 u = 1.66 × 10⁻²⁷ kg).'
    if D <= 2:
        return numq(r, D, s, 'mass defect of the nucleus in u', dm, ' u', f'Δm = {Z} × 1.007276 + {A - Z} × 1.008665 − {m:.6f}', [dm * 2, A * MNU - m, Z * MPU - m if Z * MPU > m else dm / 2], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the mass defect in kg and the binding energy in J.', f'Δm = {sc(dm * UU)} kg; E = {sc(Eb)} J',
                 f'Δm = {nf(dm, 4)} u [1]; × 1.66 × 10⁻²⁷ = {sc(dm * UU)} kg [1]; E = Δmc² = {sc(Eb)} J [1] [3]')
    return Q(s + ' (a) Calculate the mass defect in u. (b) Calculate the binding energy in MeV. (c) Calculate the binding energy per nucleon.',
             f'(a) {nf(dm, 4)} u (b) {nf(Eb / MEV, 3)} MeV (c) {nf(Eb / MEV / A, 3)} MeV', f'(a) Δm = {nf(dm, 4)} u [1] (b) Δm in kg, E = Δmc² [1]; ÷ 1.60 × 10⁻¹³ = {nf(Eb / MEV, 3)} MeV [1] (c) ÷ {A} [1]; {nf(Eb / MEV / A, 3)} MeV [1] [5]', 'multi_step')


@t131.add('C3', (1, 2, 3, 4), 'numerical')
def t131_emc(r, D):
    sit = r.choice([('The Sun radiates energy at a rate of 3.85 × 10²⁶ W.', 3.85e26, 'rate of loss of mass of the Sun', ' kg s⁻¹'),
                    ('A nuclear power station produces 1.2 × 10⁹ W of electrical power at an efficiency of 33%.', 1.2e9 / 0.33, 'rate at which mass is converted to energy in the reactor', ' kg s⁻¹'),
                    ('A 60 W lamp operates for one year (3.16 × 10⁷ s).', 60 * 3.16e7, 'mass equivalent of the energy used', ' kg'),
                    ('A battery stores 4.0 × 10⁴ J of energy.', 4.0e4, 'mass equivalent of this energy', ' kg')])
    txt, val, qty, u = sit
    m = val / C0 ** 2
    return numq(r, D, txt, qty, m, u, f'Δm = ΔE/c² = {sc(val)}/(3.00 × 10⁸)²', [val / C0, m * 1e3, val * C0 ** 2 / 1e40], fm=lambda x: sc(x, 3))


def _be_c4(r, D):
    A, Z, X, m = r.choice(NUCS[:7])
    dm, Eb = be(A, Z, m)
    intro = f'A {nuc(A, Z, X)} nucleus has a mass of {m:.6f} u. (proton mass 1.007276 u, neutron mass 1.008665 u, 1 u = 1.66 × 10⁻²⁷ kg)'
    parts = [
        lambda r: ('Define binding energy.', 'Minimum energy needed to separate a nucleus into its separate nucleons.', 'minimum energy to separate nucleons [1]'),
        lambda r: ('State the numbers of protons and neutrons in the nucleus.', f'{Z} protons, {A - Z} neutrons', 'both [1]'),
        lambda r: ('Calculate the mass defect in kg.', f'{sc(dm * UU)} kg', 'Δm in u then kg [2]'),
        lambda r: ('Calculate the binding energy in J.', f'{sc(Eb)} J', 'E = Δmc² [2]'),
        lambda r: ('Calculate the binding energy per nucleon in MeV.', f'{nf(Eb / MEV / A, 3)} MeV', '÷ A and convert [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t131.add('C4', (2, 3, 4, 5), 'multi_step')(_be_c4)

N132 = 'Binding energy per nucleon and fission and fusion'
t132 = topic(N132, N132.lower(), 'binding energy per nucleon', 'fission and fusion')
FX(t132, 'C1', (1, 2), [
    ('Which nuclide has the highest binding energy per nucleon?', 'iron-56', 'The peak of the BE/nucleon curve is near A = 56–62.', ['uranium-235', 'helium-4', 'hydrogen-2']),
    ('Energy is released in nuclear fission because', 'the products have a higher binding energy per nucleon than the original nucleus', 'Products are more tightly bound; total BE increases.', ['the products have a lower binding energy per nucleon', 'mass is created', 'the neutrons have a large kinetic energy initially']),
    ('Fusion of light nuclei releases energy because', 'the binding energy per nucleon increases', 'Moving up the curve towards iron.', ['the binding energy per nucleon decreases', 'the nuclei gain mass', 'electrons are emitted']),
    ('Why does fusion require very high temperatures?', 'the nuclei need very high kinetic energies to overcome electrostatic repulsion', 'Coulomb barrier must be overcome.', ['to break the nuclei apart first', 'to remove the neutrons', 'to increase the mass of the nuclei']),
    ('In the fission of uranium-235, the process is started by', 'absorption of a slow neutron', 'U-235 absorbs a thermal neutron, forming unstable U-236.', ['absorption of an α-particle', 'emission of a γ-ray', 'collision with a fast electron']),
    ('Which statement about the binding energy per nucleon curve is correct?', 'it rises steeply for light nuclei, peaks near A = 56 and falls gradually for heavy nuclei', 'Characteristic shape.', ['it decreases steadily from hydrogen to uranium', 'it is constant for all nuclei', 'it is highest for uranium']),
    ('State what is meant by nuclear fusion.', 'The joining of two light nuclei to form a heavier nucleus, releasing energy.', 'light nuclei join to form heavier [1]'),
])
FX(t132, 'C2', (1, 2, 3, 4), [
    ('Use the binding energy per nucleon curve to explain why both fission of heavy nuclei and fusion of light nuclei release energy.', 'Iron-56 is at the peak. Heavy nuclei splitting and light nuclei joining both produce nuclei closer to the peak, with higher binding energy per nucleon; total binding energy increases, so energy is released (mass decreases).', 'products nearer the peak / higher BE per nucleon [1]; increase in total BE released as energy [1] [2]'),
    ('Explain why binding energy per nucleon, rather than total binding energy, indicates the stability of a nucleus.', 'Total binding energy grows with the number of nucleons; dividing by A gives the average energy holding each nucleon, so nuclei can be compared: higher BE per nucleon means more tightly bound and more stable.', 'total BE increases with A [1]; per nucleon allows comparison of stability [1] [2]'),
    ('Explain why fusion reactions are difficult to achieve on Earth.', 'Nuclei are positively charged and repel; extremely high temperatures (~10⁸ K) and pressures/densities are needed so that they collide with enough kinetic energy to get within range of the strong force, and the hot plasma must be contained.', 'electrostatic repulsion [1]; very high temperature and containment needed [1] [2]'),
])


@t132.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t132_fission(r, D):
    reac = r.choice([((235, 'U', 7.59), [(141, 'Ba', 8.33), (92, 'Kr', 8.51)], 3), ((235, 'U', 7.59), [(140, 'Xe', 8.29), (94, 'Sr', 8.59)], 2),
                     ((235, 'U', 7.59), [(144, 'Ba', 8.27), (89, 'Kr', 8.62)], 3), ((239, 'Pu', 7.56), [(134, 'Xe', 8.41), (103, 'Zr', 8.57)], 3)])
    (A0, X0, b0), prods, nn = reac
    Erel = sum(A * b for A, _, b in prods) - A0 * b0
    names = ' and '.join(f'{X}-{A} ({nf(b, 3)} MeV)' for A, X, b in prods)
    s = f'In a fission reaction, a {X0}-{A0} nucleus (binding energy per nucleon {nf(b0, 3)} MeV) absorbs a neutron and splits into {names}, releasing {nn} neutrons. The values in brackets are binding energies per nucleon.'
    if D <= 2:
        return numq(r, D, s, 'energy released in MeV', Erel, ' MeV', f'E = {" + ".join(f"{A} × {nf(b, 3)}" for A, _, b in prods)} − {A0} × {nf(b0, 3)}', [Erel / A0, sum(b for _, _, b in prods) - b0, Erel * 2], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the energy released in one fission, in MeV and in J.', f'{nf(Erel, 3)} MeV = {sc(Erel * MEV)} J', f'total BE of products [1]; minus BE of {X0} = {nf(Erel, 3)} MeV [1]; × 1.60 × 10⁻¹³ = {sc(Erel * MEV)} J [1] [3]')
    mkg = r.choice([0.5, 1.0, 2.0])
    N = mkg / (A0 * UU)
    return Q(s + f' (a) Calculate the energy released per fission in J. (b) Calculate the number of nuclei in {nf(mkg)} kg of {X0}-{A0} (mass of one nucleus ≈ {A0} u). (c) Calculate the energy released if all these nuclei undergo fission.',
             f'(a) {sc(Erel * MEV)} J (b) {sc(N)} (c) {sc(N * Erel * MEV)} J', f'(a) {nf(Erel, 3)} MeV [1]; {sc(Erel * MEV)} J [1] (b) N = m/(A × 1.66 × 10⁻²⁷) = {sc(N)} [1] (c) N × E [1]; {sc(N * Erel * MEV)} J [1] [5]', 'multi_step')


@t132.add('C3', (2, 3, 4, 5), 'numerical')
def t132_fusion(r, D):
    reac = r.choice([('²₁H + ³₁H → ⁴₂He + ¹₀n', [2.013553, 3.015501], [4.001506, 1.008665]), ('²₁H + ²₁H → ³₂He + ¹₀n', [2.013553, 2.013553], [3.014932, 1.008665]),
                     ('²₁H + ²₁H → ³₁H + ¹₁p', [2.013553, 2.013553], [3.015501, 1.007276]), ('²₁H + ³₂He → ⁴₂He + ¹₁p', [2.013553, 3.014932], [4.001506, 1.007276])])
    eq, lhs, rhs = reac
    dm = sum(lhs) - sum(rhs); Er = dm * UU * C0 ** 2
    masses = 'nuclear masses: ²₁H 2.013553 u, ³₁H 3.015501 u, ³₂He 3.014932 u, ⁴₂He 4.001506 u, ¹₀n 1.008665 u, ¹₁p 1.007276 u'
    s = f'A fusion reaction is {eq}. Data: {masses}.'
    if D <= 3:
        return Q(s + ' Calculate the energy released in the reaction in MeV.', f'{nf(Er / MEV, 3)} MeV', f'Δm = {nf(dm, 4)} u [1]; E = Δmc² with Δm in kg [1]; = {nf(Er / MEV, 3)} MeV [1] [3]')
    return Q(s + ' (a) Calculate the mass difference between reactants and products. (b) Calculate the energy released in J. (c) Explain why the products have kinetic energy and why a high temperature is needed for the reaction.',
             f'(a) {nf(dm, 4)} u = {sc(dm * UU)} kg (b) {sc(Er)} J (c) the released energy appears as KE of the products; the nuclei must have high KE to overcome electrostatic repulsion',
             f'(a) Δm = {nf(dm, 4)} u [1]; in kg [1] (b) E = Δmc² = {sc(Er)} J [1] (c) energy → KE of products [1]; overcome repulsion [1] [5]', 'multi_step')


def _ff_c4(r, D):
    hv, hA, hb = r.choice([('uranium-235', 235, 7.59), ('plutonium-239', 239, 7.56), ('uranium-233', 233, 7.60)])
    pb = r.choice([8.3, 8.4, 8.5])
    bd = r.choice([1.11, 1.12])
    who = ctx(r, ['A student in {c} studies', 'An energy researcher in {c} compares', '{p} is revising', 'A physics textbook used in {c} shows'])
    intro = f'{who} the graph of binding energy per nucleon against nucleon number, which rises steeply to a peak of about 8.8 MeV near A = 56 and falls to about {nf(hb, 3)} MeV for {hv}.'
    parts = [
        lambda r: ('Define binding energy per nucleon.', 'Total binding energy of a nucleus divided by the number of nucleons.', 'BE ÷ A [1]'),
        lambda r: (f'Explain, using the graph, why fission of {hv} releases energy.', f'The products (A ≈ 90–140) have higher BE per nucleon (≈ {nf(pb)} MeV) than {hv} ({nf(hb, 3)} MeV), so total BE increases.', 'products higher BE per nucleon [1]; total BE increases, energy released [1] [2]'),
        lambda r: (f'Estimate the energy released when a {hv} nucleus splits into two nuclei each with BE per nucleon {nf(pb)} MeV (ignore free neutrons).', f'{nf(hA * (pb - hb), 3)} MeV', f'{hA} × ({nf(pb)} − {nf(hb, 3)}) [2]'),
        lambda r: ('Explain why iron-56 cannot release energy by fission or fusion.', 'It is at the peak; any change gives nuclei with lower BE per nucleon, which would require energy input.', 'at peak [1]'),
        lambda r: (f'The binding energies per nucleon are {nf(bd, 3)} MeV for ²₁H and 7.07 MeV for ⁴₂He. Estimate the energy released when two ²₁H nuclei fuse to form one ⁴₂He nucleus.', f'{nf(4 * 7.07 - 4 * bd, 3)} MeV', '4 × 7.07 − 4 × BE per nucleon of ²₁H [2]'),
        lambda r: ('State one difference between fission and fusion.', 'Fission splits heavy nuclei; fusion joins light nuclei (fusion needs very high temperature; fission is started by neutrons).', 'valid difference [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t132.add('C4', (2, 3, 4, 5), 'multi_step')(_ff_c4)

ISOS = [('iodine-131', 8.02 * 86400, '8.02 days', 131), ('cobalt-60', 5.27 * 3.16e7, '5.27 years', 60), ('strontium-90', 28.8 * 3.16e7, '28.8 years', 90), ('carbon-14', 5730 * 3.16e7, '5730 years', 14),
        ('technetium-99m', 6.01 * 3600, '6.01 hours', 99), ('radon-222', 3.82 * 86400, '3.82 days', 222), ('caesium-137', 30.2 * 3.16e7, '30.2 years', 137), ('americium-241', 432 * 3.16e7, '432 years', 241),
        ('phosphorus-32', 14.3 * 86400, '14.3 days', 32), ('fluorine-18', 110 * 60, '110 minutes', 18)]

N133 = 'Radioactive decay: activity, decay constant A = λN and half-life'
t133 = topic(N133, N133.lower(), 'activity', 'decay constant')
FX(t133, 'C1', (1, 2), [
    ('What is meant by the activity of a radioactive sample?', 'the number of nuclei decaying per unit time', 'A = −dN/dt = λN, unit Bq.', ['the number of undecayed nuclei', 'the time for half the nuclei to decay', 'the energy of each emitted particle']),
    ('The decay constant λ is', 'the probability per unit time that a nucleus will decay', 'λ = A/N.', ['the time for the activity to halve', 'the number of decays per second', 'the reciprocal of the activity']),
    ('A nuclide has a half-life of 10 minutes. What is its decay constant?', '1.16 × 10⁻³ s⁻¹', 'λ = ln 2/t½ = 0.693/600 s.', ['0.0693 s⁻¹', '0.0693 min', '1.67 × 10⁻³ s⁻¹']),
    ('What is the unit of activity?', 'becquerel (Bq)', '1 Bq = 1 decay per second.', ['gray (Gy)', 'sievert (Sv)', 's⁻²']),
    ('Radioactive decay is described as random because', 'it is not possible to predict when a particular nucleus will decay', 'Each nucleus has a constant probability of decay per unit time.', ['the count rate is always the same', 'it depends on temperature', 'the nuclei decay in a fixed order']),
    ('Radioactive decay is spontaneous because', 'it is not affected by external factors such as temperature or pressure', 'Decay rate cannot be changed by physical or chemical conditions.', ['it happens at a regular rate', 'all nuclei decay at once', 'it needs no energy']),
    ('State the relationship between decay constant and half-life.', 'λ = ln 2/t½ (≈ 0.693/t½)', 'λt½ = ln 2 [1]'),
    ('Define half-life.', 'The time taken for the number of undecayed nuclei (or the activity) of a nuclide to fall to half its initial value.', 'time for N or A to halve [1]'),
])
FX(t133, 'C2', (1, 2, 3, 4), [
    ('Explain what is meant by the random and spontaneous nature of radioactive decay.', 'Random: it is impossible to predict which nucleus will decay next or when; each has a constant probability per unit time. Spontaneous: the decay is not affected by external conditions such as temperature, pressure or chemical state.', 'random explained [1]; spontaneous explained [1] [2]'),
    ('Explain how fluctuations in the count rate from a radioactive source provide evidence for the random nature of decay.', 'Repeated counts over equal time intervals vary about a mean, because the number of nuclei decaying in each interval is a matter of chance.', 'count varies about mean [1]; decay of each nucleus a matter of chance [1] [2]'),
    ('Derive the relationship λ = ln 2/t½.', 'N = N₀e^(−λt); at t = t½, N = N₀/2: ½ = e^(−λt½), so ln 2 = λt½.', 'substitute N = N₀/2 [1]; take logs [1] [2]'),
    ('Explain why a radioactive source used as a medical tracer should have a half-life of a few hours.', 'Long enough to be prepared, injected and measured during the procedure, but short enough that the activity (and dose to the patient) falls quickly afterwards.', 'long enough for procedure [1]; short to limit dose [1] [2]'),
])


@t133.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t133_act(r, D):
    nm, th, ths, A_ = r.choice(ISOS)
    lam = math.log(2) / th
    if D <= 2:
        return numq(r, D, f'The half-life of {nm} is {ths} ({sc(th)} s).', 'decay constant', lam, ' s⁻¹', f'λ = ln 2/t½ = 0.693/{sc(th)}', [1 / th, th / math.log(2), lam * 60], fm=lambda x: sc(x, 3))
    m = r.choice([1.0e-9, 5.0e-9, 1.0e-6, 2.0e-6, 1.0e-3])
    N = m / (A_ * UU); Act = lam * N
    if D == 3:
        return Q(f'A sample contains {sc(m, 2)} kg of {nm}, half-life {ths} ({sc(th)} s). Calculate the decay constant and the activity of the sample. (mass of one nucleus ≈ {A_} u)', f'λ = {sc(lam)} s⁻¹; A = {sc(Act)} Bq',
                 f'λ = ln 2/t½ = {sc(lam)} s⁻¹ [1]; N = m/({A_} × 1.66 × 10⁻²⁷) = {sc(N)} [1]; A = λN = {sc(Act)} Bq [1] [3]')
    A1 = r.choice([2.0e3, 5.0e4, 3.7e6, 1.0e8])
    N1 = A1 / lam
    return Q(f'A source of {nm} (half-life {ths}) has an activity of {sc(A1, 2)} Bq. (a) Calculate the decay constant in s⁻¹. (b) Calculate the number of undecayed {nm} nuclei. (c) Calculate the mass of {nm} present (mass of one nucleus ≈ {A_} u).',
             f'(a) {sc(lam)} s⁻¹ (b) {sc(N1)} (c) {sc(N1 * A_ * UU)} kg', f'(a) λ = ln 2/t½ with t½ in s [1]; {sc(lam)} s⁻¹ [1] (b) N = A/λ = {sc(N1)} [1] (c) m = N × {A_} u [1]; = {sc(N1 * A_ * UU)} kg [1] [5]', 'multi_step')


@t133.add('C2', (2, 3, 4), 'explain')
def t133_count(r, D):
    a = r.choice([0.20, 0.35, 0.50]); counts = sorted(r.sample(range(180, 260), 5))
    r.shuffle(counts)
    mean = sum(counts) / 5
    return Q(f'A student records the counts from a long-lived radioactive source in five successive 10 s intervals: {", ".join(map(str, counts))}. The background count is {r.choice([3, 4, 5])} per 10 s. Explain why the counts differ and how the student should obtain the best value for the count rate due to the source.',
             f'Decay is random, so the number of decays in equal intervals fluctuates about a mean. Take the mean ({nf(mean, 3)} per 10 s), subtract background and divide by 10 s (or count for a longer time).',
             'random nature of decay [1]; mean and subtract background' + ('; longer counting time reduces percentage fluctuation [1] [3]' if D >= 3 else ' [1] [2]'))


def _act_c4(r, D):
    nm, th, ths, A_ = r.choice(ISOS[:6])
    lam = math.log(2) / th; A0 = r.choice([4.0e5, 8.0e5, 2.0e6])
    intro = f'A sample of {nm} (half-life {ths}) has an initial activity of {sc(A0, 2)} Bq.'
    parts = [
        lambda r: ('Define the decay constant.', 'Probability per unit time that a nucleus will decay.', 'probability per unit time [1]'),
        lambda r: ('Calculate the decay constant in s⁻¹.', f'{sc(lam)} s⁻¹', 'λ = ln 2/t½ [2]'),
        lambda r: ('Calculate the initial number of undecayed nuclei.', f'{sc(A0 / lam)}', 'N = A/λ [2]'),
        lambda r: ('State the activity after three half-lives.', f'{sc(A0 / 8, 3)} Bq', 'A₀/8 [1]'),
        lambda r: ('Explain why the activity, rather than the number of nuclei, is measured in practice.', 'Decays (emissions) can be counted with a detector; undecayed nuclei cannot be counted directly.', 'decays detectable [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t133.add('C4', (2, 3, 4, 5), 'multi_step')(_act_c4)

N134 = 'Exponential decay equation x = x₀e^(−λt)'
t134 = topic(N134, N134.lower(), 'exponential decay equation', 'x = x₀e^(−λt)')
FX(t134, 'C1', (1, 2), [
    ('A radioactive sample has an initial activity A₀. After four half-lives its activity is', 'A₀/16', '(½)⁴.', ['A₀/4', 'A₀/8', 'A₀/32']),
    ('In x = x₀e^(−λt), x may represent', 'the activity, the number of undecayed nuclei or the count rate', 'All decay exponentially with the same λ.', ['only the number of decayed nuclei', 'the half-life', 'the decay constant']),
    ('A graph of ln A against t for a radioactive source is a straight line. Its gradient is', '−λ', 'ln A = ln A₀ − λt.', ['λ', '−1/λ', 'ln 2/λ']),
    ('A source has a half-life of 6.0 h. What fraction of the original nuclei remains after 24 h?', '1/16', '24 h = 4 half-lives.', ['1/4', '1/8', '1/24']),
    ('The activity of a source falls from 800 Bq to 100 Bq in 15 days. What is its half-life?', '5 days', '800 → 400 → 200 → 100: three half-lives.', ['7.5 days', '3 days', '15 days']),
    ('Which equation correctly relates N at time t to the initial number N₀?', 'N = N₀e^(−λt)', 'Exponential decay.', ['N = N₀e^(λt)', 'N = N₀ − λt', 'N = N₀(1 − e^(−λt))']),
    ('State the shape of a graph of number of undecayed nuclei against time.', 'An exponential decay curve: equal fractional decreases in equal times, approaching zero.', 'exponential decay [1]'),
])
FX(t134, 'C2', (1, 2, 3, 4), [
    ('Explain why a graph of ln(activity) against time is used to find the half-life of a source.', 'ln A = ln A₀ − λt gives a straight line of gradient −λ, which can be measured accurately using all the data; t½ = ln 2/λ.', 'straight line, gradient −λ [1]; t½ = ln 2/λ [1] [2]'),
    ('Explain why the number of nuclei decaying per second falls as time passes.', 'Activity A = λN; λ is constant, but N decreases as nuclei decay, so A decreases in proportion to the remaining N.', 'A = λN [1]; N decreases [1] [2]'),
    ('Explain how radiocarbon dating uses the exponential decay law.', 'Living organisms keep a constant ratio of C-14 to C-12; after death C-14 decays with t½ = 5730 y. Measuring the present activity per gram and comparing with that of living material gives t from A = A₀e^(−λt).', 'constant ratio while alive, decay after death [1]; t = ln(A₀/A)/λ [1] [2]'),
])


@t134.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t134_decay(r, D):
    nm, th, ths, A_ = r.choice(ISOS)
    A0 = r.choice([1200.0, 5000.0, 8.0e4, 3.0e6]); k = r.choice([0.5, 1.5, 2.3, 3.0, 4.5])
    t = k * th; lam = math.log(2) / th
    A = A0 * math.exp(-lam * t)
    tdisp = f'{nf(k * float(ths.split()[0]), 3)} {ths.split()[1]}'
    s = f'A sample of {nm} (half-life {ths}) has an initial activity of {E(A0, 2)} Bq.'
    if D <= 2:
        return numq(r, D, s, f'activity after {tdisp}', A, ' Bq', f'A = A₀e^(−λt) = A₀(½)^(t/t½) = {E(A0, 2)} × 0.5^{nf(k)}', [A0 / (2 * k), A0 * math.exp(-t / th), A0 - A0 * k / 10], fm=lambda x: E(x, 3))
    if D == 3:
        return Q(s + f' Calculate the decay constant (in s⁻¹) and the activity after {tdisp}.', f'λ = {sc(lam)} s⁻¹; A = {E(A)} Bq',
                 f'λ = ln 2/t½ = {sc(lam)} s⁻¹ [1]; A = A₀e^(−λt) [1]; = {E(A)} Bq [1] [3]')
    frac = r.choice([0.10, 0.050, 0.20, 0.010])
    tf = math.log(1 / frac) / lam
    return Q(s + f' (a) Calculate the activity after {tdisp}. (b) Calculate the time taken, in {ths.split()[1]}, for the activity to fall to {nf(frac * 100)}% of its initial value. (c) Explain why the activity never quite reaches zero.',
             f'(a) {E(A)} Bq (b) {nf(tf / th * float(ths.split()[0]), 3)} {ths.split()[1]} (c) the decay is exponential: the activity halves every half-life but never becomes exactly zero (until the last nucleus decays)',
             f'(a) A = A₀e^(−λt) = {E(A)} Bq [1] (b) e^(−λt) = {nf(frac)} [1]; t = ln({nf(1 / frac, 3)})/λ = {nf(tf / th * float(ths.split()[0]), 3)} {ths.split()[1]} [1] (c) exponential tends to zero [1]; random decay of remaining nuclei [1] [5]', 'multi_step')


@t134.add('C3', (2, 3, 4, 5), 'numerical')
def t134_find(r, D):
    th_h = r.choice([2.5, 4.0, 6.0, 8.0, 12.0]); A0 = r.choice([960.0, 1500.0, 2400.0]); t = r.choice([3.0, 5.0, 10.0, 15.0])
    lam = math.log(2) / th_h; A = A0 * math.exp(-lam * t)
    A = float(nf(A, 3))
    lam2 = math.log(A0 / A) / t; th2 = math.log(2) / lam2
    return Q(f'The corrected count rate from a radioactive source falls from {nf(A0)} counts per minute to {nf(A, 3)} counts per minute in {nf(t)} hours. Calculate the decay constant and the half-life of the source.' + (' Explain why the count rate must be corrected for background.' if D >= 4 else ''),
             f'λ = {nf(lam2, 3)} h⁻¹; t½ = {nf(th2, 3)} h' + ('; the background is not from the source and would make the decay appear slower' if D >= 4 else ''),
             f'ln(A₀/A) = λt [1]; λ = {nf(lam2, 3)} h⁻¹ [1]; t½ = ln 2/λ = {nf(th2, 3)} h [1]' + ('; background explanation [1] [4]' if D >= 4 else ' [3]'))


@t134.add('C3', (3, 4, 5), 'numerical')
def t134_carbon(r, D):
    A_now = r.choice([0.080, 0.12, 0.15, 0.18, 0.21]); A_live = 0.25
    lam = math.log(2) / 5730.0; t = math.log(A_live / A_now) / lam
    obj = r.choice(['a wooden bowl', 'a piece of charcoal from an ancient hearth', 'a bone fragment', 'a linen cloth', 'a seed from an archaeological site'])
    return Q(f'Living material has a carbon-14 activity of 0.25 Bq per gram of carbon. {cap(obj)} found near {city(r)} has an activity of {nf(A_now)} Bq per gram of carbon. The half-life of carbon-14 is 5730 years. Estimate the age of the {obj.split(" ", 1)[1] if obj.startswith("a ") else obj}.',
             f'{nf(t, 3)} years', f'λ = ln 2/5730 = {sc(lam)} y⁻¹ [1]; A = A₀e^(−λt) ⇒ t = ln(0.25/{nf(A_now)})/λ [1]; = {nf(t, 3)} years [1]' + (' [3]' if D == 3 else '; one assumption, e.g. C-14 proportion in atmosphere constant [1] [4]'))


def _exp_c4(r, D):
    nm, th, ths, A_ = 'technetium-99m', 6.01 * 3600, '6.01 hours', 99
    A0 = r.choice([400e6, 500e6, 800e6]); lam = math.log(2) / th
    intro = f'A hospital in {city(r)} prepares a dose of {nm} (half-life 6.01 hours) with an activity of {nf(A0 / 1e6)} MBq at 08:00.'
    parts = [
        lambda r: ('Calculate the decay constant in s⁻¹.', f'{sc(lam)} s⁻¹', 'ln 2/t½ [1]'),
        lambda r: ('Calculate the activity at 14:00 the same day.', f'{nf(A0 * math.exp(-lam * 6 * 3600) / 1e6, 3)} MBq', 'A = A₀e^(−λt), t = 6 h [2]'),
        lambda r: ('Calculate the time at which the activity falls to 50 MBq.', f'{nf(math.log(A0 / 50e6) / lam / 3600, 3)} h after 08:00', 't = ln(A₀/A)/λ [3]'),
        lambda r: ('Calculate the number of undecayed nuclei at 08:00.', f'{sc(A0 / lam)}', 'N = A/λ [2]'),
        lambda r: ('Suggest why a short half-life is chosen for a medical tracer.', 'Activity falls quickly after the scan, reducing the dose to the patient.', 'reduced dose [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t134.add('C4', (2, 3, 4, 5), 'multi_step')(_exp_c4)
CHAPTERS[13] = [t131, t132, t133, t134]

# ===================================================================== 14 Medical physics
TISS = [('air', 1.3, 330.0), ('water', 1000.0, 1500.0), ('fat', 925.0, 1450.0), ('muscle', 1075.0, 1590.0), ('soft tissue', 1060.0, 1540.0), ('bone', 1900.0, 4080.0), ('blood', 1060.0, 1570.0), ('coupling gel', 1000.0, 1500.0)]

N141 = 'Production and use of ultrasound in diagnosis and acoustic impedance'
t141 = topic(N141, N141.lower(), 'ultrasound', 'acoustic impedance')
FX(t141, 'C1', (1, 2), [
    ('Ultrasound is sound with a frequency', 'above about 20 kHz', 'Above the upper limit of human hearing.', ['below about 20 Hz', 'between 20 Hz and 20 kHz', 'equal to that of visible light']),
    ('How is ultrasound produced in a medical transducer?', 'an alternating p.d. makes a piezoelectric crystal vibrate', 'Piezo crystal changes shape with applied p.d.; resonance at its natural frequency.', ['a heated filament emits sound', 'a magnet is moved through a coil', 'electrons strike a metal target']),
    ('Which expression gives the specific acoustic impedance Z of a medium?', 'Z = ρc', 'Density × speed of sound.', ['Z = ρ/c', 'Z = c/ρ', 'Z = ρc²']),
    ('The intensity reflection coefficient at a boundary between media of impedances Z₁ and Z₂ is', '(Z₂ − Z₁)²/(Z₂ + Z₁)²', 'α = I_R/I₀.', ['(Z₂ − Z₁)/(Z₂ + Z₁)', 'Z₂/Z₁', '(Z₂ + Z₁)²/(Z₂ − Z₁)²']),
    ('Why is a gel applied between the transducer and the skin?', 'to remove air, so that little ultrasound is reflected at the skin', 'Gel has impedance close to skin; air gives almost total reflection.', ['to cool the transducer', 'to absorb the ultrasound', 'to increase the frequency']),
    ('What is the unit of specific acoustic impedance?', 'kg m⁻² s⁻¹', 'ρc: kg m⁻³ × m s⁻¹.', ['kg m⁻³', 'kg m s⁻¹', 'Ω']),
    ('An ultrasound pulse returns 80 μs after emission from a boundary in tissue where the speed is 1500 m s⁻¹. How deep is the boundary?', '6.0 cm', 'd = ct/2 = 1500 × 80 × 10⁻⁶/2.', ['12 cm', '3.0 cm', '0.12 cm']),
    ('State what is meant by the piezoelectric effect.', 'Some crystals produce a p.d. when compressed or stretched, and change shape when a p.d. is applied.', 'p.d. ↔ deformation of crystal [1]'),
])
FX(t141, 'C2', (1, 2, 3, 4), [
    ('Explain how an ultrasound transducer both produces and detects ultrasound.', 'An alternating p.d. at the crystal\'s resonant frequency makes the piezoelectric crystal vibrate, producing ultrasound; returning echoes make the crystal vibrate, producing a small alternating p.d. that is detected.', 'alternating p.d. → vibration (production) [1]; echo → vibration → p.d. (detection) [1] [2]'),
    ('Explain why a coupling gel is necessary in an ultrasound scan.', 'Air and skin have very different acoustic impedances, so almost all ultrasound would be reflected at the air–skin boundary; the gel has an impedance similar to skin and removes the air, so most ultrasound enters the body.', 'large impedance difference air–skin [1]; gel matches impedance, transmission increased [1] [2]'),
    ('Explain why ultrasound is reflected strongly at a boundary between soft tissue and bone.', 'Bone has a much larger acoustic impedance than soft tissue; the reflection coefficient (Z₂ − Z₁)²/(Z₂ + Z₁)² is therefore large.', 'large difference in Z [1]; large α [1] [2]'),
    ('Explain why a high frequency of ultrasound gives better resolution but less penetration.', 'Higher frequency means shorter wavelength, so smaller details can be resolved; but attenuation increases with frequency, so it penetrates less deeply.', 'shorter wavelength → finer detail [1]; more attenuation [1] [2]'),
])


@t141.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t141_alpha(r, D):
    (n1, r1, c1), (n2, r2, c2) = r.sample(TISS[1:], 2)
    Z1, Z2 = r1 * c1, r2 * c2
    a = ((Z2 - Z1) / (Z2 + Z1)) ** 2
    if abs(Z1 - Z2) < 1:
        return None
    s = f'The density of {n1} is {nf(r1)} kg m⁻³ and the speed of ultrasound in it is {nf(c1)} m s⁻¹. For {n2} the values are {nf(r2)} kg m⁻³ and {nf(c2)} m s⁻¹.'
    if D <= 2:
        return numq(r, D, s, f'specific acoustic impedance of {n1}', Z1, ' kg m⁻² s⁻¹', f'Z = ρc = {nf(r1)} × {nf(c1)}', [r1 / c1, c1 / r1, r1 * c1 * c1], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(s + f' Calculate the acoustic impedance of each and the intensity reflection coefficient at a {n1}–{n2} boundary.', f'Z₁ = {sc(Z1)}, Z₂ = {sc(Z2)} kg m⁻² s⁻¹; α = {E(a)}',
                 f'Z = ρc for both [1]; α = (Z₂ − Z₁)²/(Z₂ + Z₁)² [1]; = {E(a)} [1] [3]')
    I0 = r.choice([5.0, 10.0, 20.0])
    return Q(s + f' Ultrasound of intensity {nf(I0)} mW cm⁻² is incident normally on a {n1}–{n2} boundary. (a) Calculate the intensity reflection coefficient. (b) Calculate the reflected and transmitted intensities. (c) Explain whether this boundary would show up clearly on a scan.',
             f'(a) {E(a)} (b) reflected {E(a * I0)} mW cm⁻²; transmitted {E((1 - a) * I0)} mW cm⁻² (c) ' + ('yes: a large fraction is reflected' if a > 0.05 else 'only faintly: the impedances are similar so little is reflected'),
             f'(a) Z values [1]; α = {E(a)} [1] (b) I_R = αI₀ [1]; I_T = (1 − α)I₀ [1] (c) judgement linked to α [1] [5]', 'multi_step')


@t141.add('C3', (1, 2, 3, 4), 'numerical')
def t141_depth(r, D):
    c = r.choice([1500.0, 1540.0, 1590.0]); t = r.choice([26.0, 40.0, 65.0, 78.0, 104.0, 130.0]) * 1e-6
    d = c * t / 2
    tis = r.choice(['soft tissue', 'the liver', 'the abdomen', 'muscle'])
    s = f'An ultrasound pulse travels through {tis} at {nf(c)} m s⁻¹ and an echo from a boundary is received {nf(t * 1e6)} μs after the pulse is emitted.'
    if D <= 3:
        return numq(r, D, s, 'depth of the boundary below the transducer', d * 100, ' cm', f'd = ct/2 = {nf(c)} × {sc(t)}/2', [c * t * 100, d * 50, d * 1000], fm=lambda x: nf(x, 3))
    t2 = t + r.choice([13.0, 26.0, 39.0]) * 1e-6
    return Q(s + f' A second echo arrives {nf(t2 * 1e6)} μs after emission, from the far side of an organ. (a) Calculate the depth of the first boundary. (b) Calculate the thickness of the organ. (c) Explain why the second echo is weaker than the first.',
             f'(a) {nf(d * 100, 3)} cm (b) {nf(c * (t2 - t) / 2 * 100, 3)} cm (c) energy has been partially reflected at the first boundary and absorbed (attenuated) on the extra path',
             f'(a) d = ct/2 = {nf(d * 100, 3)} cm [1] (b) Δt = {nf((t2 - t) * 1e6)} μs [1]; thickness = cΔt/2 = {nf(c * (t2 - t) / 2 * 100, 3)} cm [1] (c) reflection loss and attenuation [1] [4]', 'multi_step')


def _us_c4(r, D):
    (n1, r1, c1), (n2, r2, c2) = r.sample([x for x in TISS if x[0] not in ('air', 'coupling gel', 'water')], 2)
    Z1, Z2, Za, Zg = r1 * c1, r2 * c2, 430.0, 1.50e6
    who = ctx(r, ['A sonographer in {c}', 'A hospital physicist in {c}', 'A medical student, {p},', 'A clinic in {c}'])
    intro = f'{who} uses ultrasound to image a {n1}–{n2} boundary. Data: density of {n1} {nf(r1)} kg m⁻³, speed {nf(c1)} m s⁻¹; density of {n2} {nf(r2)} kg m⁻³, speed {nf(c2)} m s⁻¹; air 430 kg m⁻² s⁻¹; gel 1.50 × 10⁶ kg m⁻² s⁻¹.'
    a = lambda x, y: ((y - x) / (y + x)) ** 2
    t = r.choice([40.0, 65.0, 90.0]) * 1e-6
    parts = [
        lambda r: ('Describe how ultrasound is produced by the transducer.', 'An alternating p.d. causes a piezoelectric crystal to vibrate (at resonance), emitting ultrasound.', 'alternating p.d. on piezo crystal [1]; vibration produces ultrasound [1] [2]'),
        lambda r: (f'Calculate the specific acoustic impedances of {n1} and {n2}.', f'{sc(Z1)} and {sc(Z2)} kg m⁻² s⁻¹', 'Z = ρc [2]'),
        lambda r: (f'Calculate the intensity reflection coefficient at the {n1}–{n2} boundary.', f'{E(a(Z1, Z2))}', 'α formula [2]'),
        lambda r: ('Calculate the intensity reflection coefficient at an air–skin boundary, taking skin to have Z = 1.63 × 10⁶ kg m⁻² s⁻¹, and use it to explain why gel is used.', f'{nf(a(Za, 1.63e6), 4)}: almost all ultrasound would be reflected without gel', 'α ≈ 1 [1]; gel removes air / matches impedance [1] [2]'),
        lambda r: (f'An echo from the boundary returns {nf(t * 1e6)} μs after the pulse is sent through {n1}. Calculate the depth of the boundary.', f'{nf(c1 * t / 2 * 100, 3)} cm', 'd = ct/2 [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t141.add('C4', (2, 3, 4, 5), 'multi_step')(_us_c4)

N142 = 'Production of X-rays and X-ray imaging and attenuation, including CT scans'
t142 = topic(N142, N142.lower(), 'production of x-rays', 'ct scans')
FX(t142, 'C1', (1, 2), [
    ('How are X-rays produced in an X-ray tube?', 'high-speed electrons are decelerated when they strike a metal target', 'Bremsstrahlung plus characteristic lines.', ['a heated filament emits X-rays directly', 'radioactive nuclei in the target decay', 'electrons are accelerated in a magnetic field']),
    ('The minimum wavelength of X-rays from a tube operating at p.d. V is given by', 'hc/(eV)', 'All the electron\'s KE eV goes into one photon.', ['eV/(hc)', 'hc/V', 'h/(eV)']),
    ('Why is the target of an X-ray tube usually made of tungsten and often rotated?', 'it has a high melting point and most of the electron energy becomes heat', 'About 99% of energy is converted to thermal energy.', ['tungsten is a good conductor of X-rays', 'it absorbs all the X-rays produced', 'it emits electrons easily']),
    ('The attenuation of a parallel X-ray beam in a material is described by', 'I = I₀e^(−μx)', 'Exponential attenuation with linear attenuation coefficient μ.', ['I = I₀ − μx', 'I = I₀/x²', 'I = I₀e^(μx)']),
    ('Increasing the accelerating p.d. of an X-ray tube', 'decreases the minimum wavelength of the X-rays', 'λmin = hc/eV.', ['increases the minimum wavelength', 'decreases the X-ray intensity', 'has no effect on the X-ray spectrum']),
    ('A CT scan differs from a simple X-ray image because', 'many images taken from different angles are combined to give a 3D image built from slices', 'Computed tomography reconstructs voxel values.', ['it uses ultrasound instead of X-rays', 'it gives a single 2D shadow image', 'it uses radioactive tracers']),
    ('What is meant by the contrast of an X-ray image?', 'the difference in degree of blackening between different areas', 'Good contrast requires different attenuation of tissues.', ['the sharpness of the edges of structures', 'the total brightness of the image', 'the size of the image']),
    ('State what is meant by the sharpness of an X-ray image.', 'How clearly the edges of structures are defined.', 'clarity of edges [1]'),
])
FX(t142, 'C2', (1, 2, 3, 4), [
    ('Explain why bones show up clearly on an X-ray image but soft tissues do not.', 'Bone has a much larger attenuation coefficient than soft tissue, so far fewer X-rays pass through it; the large difference in transmitted intensity gives good contrast. Soft tissues have similar coefficients, so contrast is poor.', 'bone μ much larger [1]; large difference in transmitted intensity → contrast [1] [2]'),
    ('Explain how the contrast of an X-ray image of soft tissue can be improved.', 'Use a contrast medium with a high attenuation coefficient (e.g. barium or iodine) in the organ, or use lower-energy (softer) X-rays where absorption differences are greater.', 'contrast medium (barium/iodine) [1]; reason: high μ / greater difference [1] [2]'),
    ('Describe the principles of CT scanning.', 'An X-ray tube and detectors rotate around the patient; images of a thin slice are taken from many angles. A computer reconstructs the attenuation in each voxel of the slice, and slices are combined into a 3D image.', 'many images from different angles of a slice [1]; computer reconstruction into 3D image of voxels [1] [2]'),
    ('Explain why an X-ray tube has a continuous spectrum with a sharp minimum wavelength.', 'Electrons decelerate in the target losing varying amounts of energy, producing photons of a continuous range of energies; the maximum photon energy equals the electron KE eV, giving λmin = hc/(eV).', 'varying deceleration → continuous range [1]; maximum photon energy eV gives λmin [1] [2]'),
    ('Explain the advantages and disadvantages of a CT scan compared with a single X-ray image.', 'Advantages: 3D image, distinguishes overlapping structures and soft tissues with small attenuation differences. Disadvantage: much larger radiation dose (and cost, time).', 'advantage [1]; disadvantage (dose) [1] [2]'),
])


@t142.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t142_lmin(r, D):
    V = r.choice([25e3, 40e3, 60e3, 80e3, 100e3, 120e3]); I = r.choice([1.0e-3, 5.0e-3, 20e-3, 100e-3])
    lam = HP * C0 / (QE * V)
    s = f'An X-ray tube operates with an accelerating p.d. of {nf(V / 1000)} kV and a tube current of {nf(I * 1000)} mA.'
    if D <= 2:
        return numq(r, D, s, 'minimum wavelength of the X-rays', lam, ' m', f'λmin = hc/(eV) = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/(1.60 × 10⁻¹⁹ × {sc(V, 2)})', [HP / (QE * V), lam * 1000, QE * V / (HP * C0) * 1e-20], fm=lambda x: sc(x, 3))
    P = V * I
    if D == 3:
        return Q(s + ' Calculate the maximum energy of an X-ray photon and the minimum wavelength.', f'{sc(QE * V)} J; {sc(lam)} m', f'E = eV = {sc(QE * V)} J [1]; λ = hc/E [1]; = {sc(lam)} m [1] [3]')
    return Q(s + ' (a) Calculate the minimum wavelength. (b) Calculate the number of electrons hitting the target per second. (c) About 1% of the power is converted to X-rays. Calculate the rate at which thermal energy is produced in the target.',
             f'(a) {sc(lam)} m (b) {sc(I / QE)} s⁻¹ (c) {E(0.99 * P)} W', f'(a) λ = hc/eV = {sc(lam)} m [1] (b) n = I/e = {sc(I / QE)} s⁻¹ [1] (c) P = VI = {E(P)} W [1]; 99% → {E(0.99 * P)} W [1] [4]', 'multi_step')


@t142.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t142_atten(r, D):
    mat, mu = r.choice([('bone', 3.0), ('soft tissue', 0.95), ('muscle', 1.0), ('aluminium', 1.2), ('lead', 60.0), ('fat', 0.85)])
    x = r.choice([0.5, 1.0, 2.0, 3.0, 5.0]) if mat != 'lead' else r.choice([0.02, 0.05, 0.10])
    frac = math.exp(-mu * x)
    s = f'A parallel beam of X-rays passes through {nf(x)} cm of {mat}, whose linear attenuation coefficient for these X-rays is {nf(mu)} cm⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'fraction of the intensity transmitted', frac, '', f'I/I₀ = e^(−μx) = e^(−{nf(mu)} × {nf(x)})', [1 - frac, math.exp(-x / mu), mu * x], fm=lambda v: E(v, 3))
    hvt = math.log(2) / mu
    if D == 3:
        return Q(s + ' Calculate the fraction of the intensity transmitted and the half-value thickness of the material.', f'{E(frac)}; {nf(hvt, 3)} cm', f'I/I₀ = e^(−μx) [1]; = {E(frac)} [1]; x½ = ln 2/μ = {nf(hvt, 3)} cm [1] [3]')
    mu2 = 0.95; x2 = r.choice([3.0, 4.0, 5.0]); xb = r.choice([1.0, 1.5, 2.0])
    I_soft = math.exp(-mu2 * x2); I_bone = math.exp(-mu2 * (x2 - xb) - 3.0 * xb)
    return Q(f'An X-ray beam passes through {nf(x2)} cm of soft tissue (μ = 0.95 cm⁻¹) along one path, and through {nf(x2 - xb)} cm of soft tissue plus {nf(xb)} cm of bone (μ = 3.0 cm⁻¹) along a second path. (a) Calculate the fraction of the intensity transmitted along each path. (b) Calculate the ratio of the two intensities. (c) Explain how this ratio relates to the contrast of the image.',
             f'(a) {E(I_soft)} and {E(I_bone)} (b) {nf(I_soft / I_bone, 3)} (c) a large ratio means a large difference in blackening, so good contrast between bone and soft tissue',
             f'(a) e^(−μx) for each path [1]; both values [1] (b) ratio = {nf(I_soft / I_bone, 3)} [1] (c) large ratio [1]; good contrast [1] [5]', 'multi_step')


def _xr_c4(r, D):
    V = r.choice([50e3, 80e3, 100e3])
    intro = f'A hospital X-ray tube in {city(r)} uses electrons accelerated through {nf(V / 1000)} kV onto a tungsten target.'
    parts = [
        lambda r: ('Calculate the maximum energy of the X-ray photons in J.', f'{sc(QE * V)} J', 'E = eV [1]'),
        lambda r: ('Calculate the minimum wavelength.', f'{sc(HP * C0 / (QE * V))} m', 'λ = hc/eV [2]'),
        lambda r: ('Explain why the target must be cooled.', 'About 99% of the electrons\' kinetic energy becomes thermal energy in the target.', 'most energy → heat [1]'),
        lambda r: ('Explain why an aluminium filter is placed in the beam.', 'It absorbs low-energy (soft) X-rays that would be absorbed by the patient without reaching the detector, reducing dose.', 'absorbs soft X-rays [1]; reduces dose [1] [2]'),
        lambda r: ('State one way in which a CT scan differs from an X-ray image.', 'CT combines many images of slices from different angles into a 3D image.', 'valid difference [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t142.add('C4', (2, 3, 4, 5), 'multi_step')(_xr_c4)

N143 = 'PET scanning: tracers and annihilation'
t143 = topic(N143, N143.lower(), 'pet scanning', 'annihilation')
FX(t143, 'C1', (1, 2), [
    ('A PET scan uses a tracer that emits', 'positrons (β⁺ particles)', 'Positron emission tomography.', ['electrons (β⁻ particles)', 'α-particles', 'neutrons']),
    ('When a positron meets an electron they annihilate, producing', 'two γ-ray photons moving in opposite directions', 'Momentum conservation requires two photons in opposite directions.', ['one γ-ray photon', 'a neutron and a neutrino', 'two electrons']),
    ('What is the energy of each photon produced when an electron and a positron at rest annihilate?', '0.511 MeV', 'Each photon carries mₑc².', ['1.02 MeV', '0.256 MeV', '931 MeV']),
    ('Which tracer is commonly used in PET scans?', 'fluorine-18 in fluorodeoxyglucose (FDG)', 'F-18 is a positron emitter with t½ ≈ 110 min.', ['iodine-131', 'cobalt-60', 'carbon-12']),
    ('Why do the two photons from annihilation travel in opposite directions?', 'to conserve momentum, since the initial momentum is approximately zero', 'Total momentum zero before, so the photons have equal and opposite momenta.', ['to conserve charge', 'because they repel each other', 'because they are emitted by different nuclei']),
    ('In a PET scanner, the location of the annihilation is found from', 'the difference in arrival times of the two photons at detectors on opposite sides', 'Coincidence detection along a line of response.', ['the energy of a single photon', 'the colour of the light', 'the intensity of the ultrasound echo']),
    ('State what is meant by annihilation.', 'The interaction of a particle with its antiparticle in which their mass is converted into energy (photons).', 'particle and antiparticle → energy/photons [1]'),
])
FX(t143, 'C2', (1, 2, 3, 4), [
    ('Explain why a PET tracer must have a short half-life and why it is produced near the hospital.', 'A short half-life (minutes to hours) gives high activity for the scan and reduces the dose afterwards; because it decays quickly, it must be made (in a cyclotron) close to where it is used.', 'short t½ reduces dose / high activity [1]; decays quickly so made nearby [1] [2]'),
    ('Explain how a PET scan produces an image of metabolic activity.', 'The tracer (e.g. FDG) is taken up most by active cells; positrons from it annihilate with electrons, producing pairs of γ-photons detected simultaneously by a ring of detectors. Lines of response and timing differences locate the sources, and a computer builds up an image of tracer concentration.', 'tracer concentrates in active tissue [1]; coincident photon pairs located → image [1] [2]'),
    ('Explain why the two annihilation photons each have energy mₑc² when the electron and positron are almost at rest.', 'The total energy available is the rest energy 2mₑc² (kinetic energy negligible); two photons with equal and opposite momenta must have equal energies, so each has mₑc².', 'total energy 2mₑc² [1]; shared equally (momentum) [1] [2]'),
])


@t143.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t143_ann(r, D):
    Eph = ME * C0 ** 2
    if D <= 2:
        k = r.choice(['E', 'lam', 'f'])
        if k == 'E':
            return numq(r, D, 'An electron and a positron, both effectively at rest, annihilate in a patient\'s tissue during a PET scan.', 'energy of each γ-ray photon produced', Eph, ' J', 'E = mₑc² = 9.11 × 10⁻³¹ × (3.00 × 10⁸)²', [2 * Eph, ME * C0, Eph / 2], fm=lambda x: sc(x, 3))
        if k == 'lam':
            return numq(r, D, 'In a PET scan, each annihilation photon has energy 8.20 × 10⁻¹⁴ J.', 'wavelength of each photon', HP * C0 / Eph, ' m', 'λ = hc/E = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/8.20 × 10⁻¹⁴', [HP / Eph, Eph / (HP * C0) * 1e-24, HP * C0 / (2 * Eph)], fm=lambda x: sc(x, 3))
        return numq(r, D, 'In a PET scan, each annihilation photon has energy 8.20 × 10⁻¹⁴ J.', 'frequency of each photon', Eph / HP, ' Hz', 'f = E/h = 8.20 × 10⁻¹⁴/6.63 × 10⁻³⁴', [Eph * HP * 1e48, Eph / HP / 2, C0 * HP / Eph * 1e32], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q('In a PET scan, a positron annihilates with an electron, both effectively at rest. Calculate the energy of each photon produced, in J and in MeV, and its wavelength.', f'{sc(Eph)} J = {nf(Eph / MEV, 3)} MeV; λ = {sc(HP * C0 / Eph)} m',
                 f'E = mₑc² = {sc(Eph)} J [1]; ÷ 1.60 × 10⁻¹³ = {nf(Eph / MEV, 3)} MeV [1]; λ = hc/E = {sc(HP * C0 / Eph)} m [1] [3]')
    dt = r.choice([0.20, 0.40, 0.50, 0.80, 1.0]) * 1e-9
    dx = C0 * dt / 2
    return Q(f'In a PET scanner, the two photons from one annihilation are detected by detectors on opposite sides of the ring. One arrives {nf(dt * 1e9)} ns before the other. (a) State why two photons travelling in opposite directions are produced. (b) Calculate the energy of each photon in MeV. (c) Calculate how far the annihilation point is from the midpoint between the detectors.',
             f'(a) momentum must be conserved (initial momentum ≈ 0) (b) {nf(Eph / MEV, 3)} MeV (c) {nf(dx * 100, 3)} cm, nearer the detector that receives its photon first',
             f'(a) conservation of momentum [1] (b) E = mₑc² converted to MeV = {nf(Eph / MEV, 3)} MeV [1] (c) path difference = cΔt [1]; offset = cΔt/2 = {nf(dx * 100, 3)} cm [1]; towards first detector [1] [5]', 'multi_step')


@t143.add('C3', (2, 3, 4, 5), 'numerical')
def t143_tracer(r, D):
    A0 = r.choice([200e6, 300e6, 370e6, 400e6]); t_min = r.choice([30, 45, 60, 90, 120])
    lam = math.log(2) / (110 * 60)
    A = A0 * math.exp(-lam * t_min * 60)
    return Q(f'A dose of FDG containing fluorine-18 (half-life 110 minutes) has an activity of {nf(A0 / 1e6)} MBq when prepared. The scan begins {t_min} minutes later. Calculate the activity at the start of the scan.' + (' Suggest why the dose is prepared with a higher activity than is needed for the scan.' if D >= 4 else ''),
             f'{nf(A / 1e6, 3)} MBq' + ('; it decays significantly during transport and the uptake period' if D >= 4 else ''),
             f'λ = ln 2/(110 × 60) = {sc(lam)} s⁻¹ [1]; A = A₀e^(−λt) [1]; = {nf(A / 1e6, 3)} MBq [1]' + ('; decay before scan [1] [4]' if D >= 4 else ' [3]'))


PETT = [('fluorine-18', '¹⁸₉F → ¹⁸₈O + ⁰₊₁e + ν', 110.0, 'minutes'), ('carbon-11', '¹¹₆C → ¹¹₅B + ⁰₊₁e + ν', 20.4, 'minutes'),
        ('nitrogen-13', '¹³₇N → ¹³₆C + ⁰₊₁e + ν', 9.97, 'minutes'), ('oxygen-15', '¹⁵₈O → ¹⁵₇N + ⁰₊₁e + ν', 2.04, 'minutes')]


def _pet_c4(r, D):
    nm, eq, th, un = r.choice(PETT)
    k = r.choice([2, 3, 4, 5])
    where = ctx(r, ['A hospital in {c}', 'A PET centre in {c}', 'A cancer clinic in {c}', 'A research hospital in {c}'])
    intro = f'{where} injects a patient with a tracer labelled with {nm}, which decays by β⁺ emission with a half-life of {nf(th)} {un}.'
    Eph = ME * C0 ** 2
    dt = r.choice([0.30, 0.50, 0.70]) * 1e-9
    parts = [
        lambda r: (f'Write the decay equation for {nm}.', eq, 'products correct [1]; neutrino [1] [2]'),
        lambda r: ('Describe what happens to the positron emitted.', 'It travels a very short distance in tissue and annihilates with an electron, producing two γ-photons in opposite directions.', 'annihilates with electron [1]; two photons opposite [1] [2]'),
        lambda r: ('Calculate the energy of each annihilation photon in MeV.', f'{nf(Eph / MEV, 3)} MeV', 'E = mₑc² [2]'),
        lambda r: (f'Calculate the fraction of the tracer remaining after {nf(k * th)} {un}.', f'{nf(0.5 ** k, 3)}', f'{k} half-lives [1]'),
        lambda r: (f'The two photons from one annihilation arrive at opposite detectors {nf(dt * 1e9)} ns apart. Calculate the distance of the annihilation from the midpoint between the detectors.', f'{nf(C0 * dt / 2 * 100, 3)} cm', 'cΔt/2 [2]'),
        lambda r: ('Explain why the tracer must be produced close to the hospital.', 'Its short half-life means it would decay significantly during transport.', 'short half-life [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t143.add('C4', (2, 3, 4, 5), 'multi_step')(_pet_c4)


@t143.add('C2', (2, 3, 4), 'explain')
def t143_cmp(r, D):
    other, ans = r.choice([('an X-ray CT scan', 'PET shows function (metabolic activity, where the tracer is taken up), whereas CT shows structure (differences in X-ray attenuation); PET has poorer spatial resolution.'),
                           ('an ultrasound scan', 'PET uses ionising γ-radiation from an injected tracer and shows metabolic activity; ultrasound is non-ionising and shows boundaries between tissues from reflected echoes.'),
                           ('a conventional X-ray image', 'PET images the distribution of a tracer inside the body (function), built from many coincidence detections; an X-ray image is a 2D shadow of attenuation by structures.')])
    who = ctx(r, ['A doctor in {c}', 'A radiographer in {c}', 'A patient, {p},'])
    return Q(f'{who} asks how a PET scan differs from {other}. Explain one important difference in what the scans show and how the images are produced.', ans,
             'difference in what is shown [1]; difference in how image is formed [1]' + ('; reference to dose or resolution [1] [3]' if D >= 3 else ' [2]'))
CHAPTERS[14] = [t141, t142, t143]

# ===================================================================== 15 Astronomy and cosmology
LSUN = 3.83e26
LY = 9.46e15
PC = 3.09e16
STARS = [('Sirius A', 9940.0, 25.4), ('Vega', 9600.0, 40.1), ('Betelgeuse', 3500.0, 1.26e5), ('Rigel', 12100.0, 1.2e5), ('Proxima Centauri', 3040.0, 1.55e-3),
         ('Arcturus', 4290.0, 170.0), ('Aldebaran', 3910.0, 439.0), ('Spica', 22400.0, 2.05e4), ('Antares', 3660.0, 7.5e4), ('Altair', 7670.0, 10.6), ('the Sun', 5780.0, 1.0)]

N151 = 'Standard candles, luminosity and radiant flux intensity F = L/4πd²'
t151 = topic(N151, N151.lower(), 'standard candles', 'radiant flux intensity')
FX(t151, 'C1', (1, 2), [
    ('What is meant by the luminosity of a star?', 'the total power of radiation emitted by the star', 'Luminosity L in W.', ['the power received per unit area at the Earth', 'the brightness of the star seen from Earth', 'the surface temperature of the star']),
    ('What is meant by a standard candle?', 'an astronomical object of known luminosity', 'Known L plus measured F gives d.', ['a star of known distance', 'the brightest star in a galaxy', 'a star with constant temperature']),
    ('Which is used as a standard candle?', 'a Cepheid variable star', 'Its period–luminosity relation gives L; Type Ia supernovae are also used.', ['a red giant of unknown size', 'a neutron star', 'a planet']),
    ('The radiant flux intensity from a star is F at distance d. At distance 3d it is', 'F/9', 'F = L/(4πd²).', ['F/3', '3F', 'F/27']),
    ('What is the unit of radiant flux intensity?', 'W m⁻²', 'Power per unit area.', ['W', 'W m⁻¹', 'J m⁻²']),
    ('Two stars have the same radiant flux intensity at the Earth. Star X is twice as far away as star Y. The luminosity of X is', 'four times that of Y', 'L = 4πd²F.', ['twice that of Y', 'half that of Y', 'the same as Y']),
    ('Why are Type Ia supernovae useful for measuring the distances to distant galaxies?', 'they have a known, very large peak luminosity', 'Bright enough to be seen at great distances.', ['they are very close to the Earth', 'they emit only radio waves', 'they have no redshift']),
    ('State what is meant by radiant flux intensity.', 'The radiant power passing normally through unit area.', 'power per unit area (normal) [1]'),
])
FX(t151, 'C2', (1, 2, 3, 4), [
    ('Explain how a standard candle is used to determine the distance to a galaxy.', 'The luminosity L of the standard candle is known (e.g. from the period of a Cepheid); its radiant flux intensity F at the Earth is measured; then d = √(L/4πF).', 'L known [1]; F measured, d = √(L/4πF) [1] [2]'),
    ('Explain why the radiant flux intensity from a star obeys an inverse-square law with distance.', 'The power L spreads out uniformly over the surface of a sphere of area 4πd²; the intensity is power per unit area, so F = L/(4πd²) ∝ 1/d².', 'power spreads over sphere 4πd² [1]; F ∝ 1/d² [1] [2]'),
    ('Suggest why different standard candles are needed for nearby and very distant galaxies.', 'Cepheids are not bright enough to be seen in very distant galaxies; much more luminous standard candles such as Type Ia supernovae are needed there, calibrated using nearer Cepheid distances.', 'Cepheids too faint at large d [1]; supernovae brighter [1] [2]'),
    ('Explain why the radiant flux intensity measured at the Earth may be smaller than L/(4πd²).', 'Some radiation is absorbed or scattered by interstellar dust and gas and by the Earth\'s atmosphere, so less power reaches the detector.', 'absorption/scattering by dust or atmosphere [1]; less power received [1] [2]'),
])


@t151.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t151_flux(r, D):
    nm, T, Lr = r.choice(STARS[:-1])
    L = Lr * LSUN
    dly = r.choice([4.2, 8.6, 25.0, 37.0, 250.0, 550.0, 640.0, 860.0])
    d = dly * LY
    F = L / (4 * PI * d * d)
    s = f'The star {nm} has a luminosity of {sc(L)} W and is {nf(dly)} light-years ({sc(d)} m) from the Earth.'
    if D <= 2:
        return numq(r, D, s, 'radiant flux intensity at the Earth', F, ' W m⁻²', f'F = L/(4πd²) = {sc(L)}/(4π × ({sc(d)})²)', [L / (4 * PI * d), L / (d * d), F * 4 * PI], fm=lambda x: sc(x, 3))
    if D == 3:
        return Q(f'The radiant flux intensity at the Earth from a Cepheid variable star of luminosity {sc(L)} W is {sc(F)} W m⁻². Calculate its distance from the Earth in metres and in light-years (1 ly = 9.46 × 10¹⁵ m).', f'{sc(d)} m = {nf(dly, 3)} ly',
                 f'd = √(L/4πF) [1]; = {sc(d)} m [1]; ÷ 9.46 × 10¹⁵ = {nf(dly, 3)} ly [1] [3]')
    Fs = 1.36e3
    return Q(f'The Sun has luminosity 3.83 × 10²⁶ W and the radiant flux intensity at the Earth is 1.36 × 10³ W m⁻². The star {nm} has a luminosity {E(Lr, 3)} times that of the Sun and a measured radiant flux intensity of {sc(F)} W m⁻² at the Earth. (a) Calculate the Earth–Sun distance. (b) Calculate the distance to {nm}. (c) Explain why this method requires the luminosity to be known independently.',
             f'(a) {sc(math.sqrt(LSUN / (4 * PI * Fs)))} m (b) {sc(d)} m (c) the measured F depends on both L and d; only if L is known (standard candle) can d be found',
             f'(a) d = √(L/4πF) = {sc(math.sqrt(LSUN / (4 * PI * Fs)))} m [1] (b) L = {sc(L)} W [1]; d = {sc(d)} m [1] (c) one equation, two unknowns [1]; L known for a standard candle [1] [5]', 'multi_step')


relation(t151, 'C2', (2, 3), 'F = L/(4πd²)', 'radiant flux intensity received at the Earth', {'distance from the Earth': -2, 'luminosity': 1},
         ['A Cepheid variable star in a nearby galaxy is observed from the Earth.', 'A Type Ia supernova in a distant galaxy is observed.', 'A star is modelled as a point source radiating uniformly in all directions.'])


def _sc_c4(r, D):
    L = r.choice([1.0e30, 5.0e30, 2.0e31]); F = r.choice([1.0e-16, 4.0e-17, 2.5e-17, 6.0e-18])
    d = math.sqrt(L / (4 * PI * F))
    intro = f'A Cepheid variable star in a distant galaxy has a luminosity, deduced from its period, of {sc(L, 2)} W. Its measured radiant flux intensity at the Earth is {sc(F, 2)} W m⁻².'
    parts = [
        lambda r: ('State what is meant by a standard candle.', 'An astronomical object of known luminosity.', 'known luminosity [1]'),
        lambda r: ('Calculate the distance to the galaxy.', f'{sc(d)} m', 'd = √(L/4πF) [2]'),
        lambda r: ('Express this distance in megaparsecs (1 pc = 3.09 × 10¹⁶ m).', f'{nf(d / PC / 1e6, 3)} Mpc', '÷ 3.09 × 10²² [1]'),
        lambda r: ('Explain why the luminosity of a Cepheid can be found from its period.', 'Cepheids obey a period–luminosity relationship calibrated with nearby Cepheids of known distance.', 'period–luminosity relation [1]'),
        lambda r: ('Suggest one source of uncertainty in this distance.', 'Absorption by dust reduces F; uncertainty in the period–luminosity calibration.', 'valid source [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t151.add('C4', (2, 3, 4, 5), 'multi_step')(_sc_c4)

N152 = "Stellar radii: Wien's displacement law and Stefan-Boltzmann law"
t152 = topic(N152, N152.lower(), "wien's displacement law", 'stefan-boltzmann law')
FX(t152, 'C1', (1, 2), [
    ('Wien\'s displacement law states that the wavelength at which a black body emits maximum power is', 'inversely proportional to its thermodynamic temperature', 'λmax ∝ 1/T.', ['proportional to its thermodynamic temperature', 'proportional to T⁴', 'independent of temperature']),
    ('The Stefan–Boltzmann law for a star of radius r and surface temperature T is', 'L = 4πσr²T⁴', 'Power = σ × area × T⁴.', ['L = σr²T⁴', 'L = 4πσrT⁴', 'L = 4πσr²T²']),
    ('A star has a surface temperature of 5800 K. At what wavelength is its emission a maximum?', '5.0 × 10⁻⁷ m', 'λmax = 2.9 × 10⁻³/5800.', ['2.0 × 10⁶ m', '5.0 × 10⁻⁴ m', '1.7 × 10⁻⁷ m']),
    ('Two stars have the same luminosity. Star P has twice the surface temperature of star Q. The radius of P is', 'one quarter of the radius of Q', 'L ∝ r²T⁴: r ∝ 1/T².', ['half the radius of Q', 'twice the radius of Q', 'one sixteenth of the radius of Q']),
    ('A red star and a blue star are compared. The blue star has', 'a higher surface temperature', 'Shorter λmax ⇒ higher T.', ['a lower surface temperature', 'a larger radius', 'a lower luminosity']),
    ('The surface temperature of a star is doubled at constant radius. Its luminosity becomes', '16 times larger', 'L ∝ T⁴.', ['2 times larger', '4 times larger', '8 times larger']),
    ('State Wien\'s displacement law.', 'λmax T = constant (2.9 × 10⁻³ m K).', 'λmax ∝ 1/T [1]'),
])
FX(t152, 'C2', (1, 2, 3, 4), [
    ('Explain how the radius of a star can be determined from observations.', 'Measure λmax in its spectrum and use Wien\'s law to find T; find L (from F and d, or as a standard candle); then use L = 4πσr²T⁴ to calculate r.', 'T from Wien\'s law [1]; r from Stefan–Boltzmann with L [1] [2]'),
    ('Explain why a red giant can be much more luminous than the Sun although its surface is cooler.', 'L ∝ r²T⁴; although T is lower, its radius is very much larger, so r² more than compensates for the smaller T⁴.', 'L = 4πσr²T⁴ [1]; much larger r compensates [1] [2]'),
    ('State the assumptions made when applying Wien\'s law and the Stefan–Boltzmann law to stars.', 'The star behaves as a black body (perfect emitter) and is spherical with a uniform surface temperature.', 'black body [1]; spherical/uniform temperature [1] [2]'),
])
relation(t152, 'C2', (2, 3), 'L = 4πσr²T⁴', 'luminosity of the star', {'surface temperature': 4, 'radius': 2},
         ['A star is modelled as a black body.', 'A main-sequence star changes as it evolves.', 'Two stars are compared using the Stefan–Boltzmann law.'])


@t152.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t152_wien(r, D):
    nm, T, Lr = r.choice(STARS)
    lam = WIEN / T
    if D <= 2:
        return numq(r, D, f'The star {nm} has a surface temperature of {nf(T)} K.', 'wavelength at which its emission is a maximum', lam, ' m', f'λmax = 2.9 × 10⁻³/T = 2.9 × 10⁻³/{nf(T)}', [WIEN * T, lam * 1000, 1 / T], fm=lambda x: sc(x, 3))
    L = Lr * LSUN
    R = math.sqrt(L / (4 * PI * SIG * T ** 4))
    if D == 3:
        return Q(f'The spectrum of {nm} has its peak intensity at {sc(lam)} m. Its luminosity is {sc(L)} W. Calculate its surface temperature and its radius.', f'T = {nf(T, 3)} K; r = {sc(R)} m',
                 f'T = 2.9 × 10⁻³/λmax = {nf(T, 3)} K [1]; L = 4πσr²T⁴ [1]; r = {sc(R)} m [1] [3]')
    Rs = math.sqrt(LSUN / (4 * PI * SIG * 5780.0 ** 4))
    return Q(f'The spectrum of {nm} peaks at {sc(lam)} m and its luminosity is {E(Lr, 3)} times that of the Sun (3.83 × 10²⁶ W). (a) Calculate the surface temperature. (b) Calculate the radius. (c) The Sun\'s radius is {sc(Rs)} m. Calculate the ratio of the radius of {nm} to that of the Sun and comment on the type of star.' if nm != 'the Sun' else
             f'The Sun\'s spectrum peaks at {sc(lam)} m and its luminosity is 3.83 × 10²⁶ W. (a) Calculate its surface temperature. (b) Calculate its radius. (c) Calculate the power received per unit area at a distance of 1.50 × 10¹¹ m.',
             (f'(a) {nf(T, 3)} K (b) {sc(R)} m (c) {E(R / Rs)}; ' + ('a giant/supergiant' if R / Rs > 10 else ('a dwarf' if R / Rs < 0.5 else 'similar in size to the Sun'))) if nm != 'the Sun' else f'(a) {nf(T, 3)} K (b) {sc(R)} m (c) {sc(LSUN / (4 * PI * 1.5e11 ** 2))} W m⁻²',
             f'(a) Wien: T = {nf(T, 3)} K [1] (b) r = √(L/4πσT⁴) [1]; = {sc(R)} m [1] (c) ' + (f'ratio {E(R / Rs)} [1]; comment [1] [5]' if nm != 'the Sun' else f'F = L/4πd² [1]; {sc(LSUN / (4 * PI * 1.5e11 ** 2))} W m⁻² [1] [5]'), 'multi_step')


@t152.add('C3', (2, 3, 4), 'numerical')
def t152_ratio(r, D):
    (a, Ta, La), (b, Tb, Lb) = r.sample(STARS, 2)
    ratio = math.sqrt(La / Lb) * (Tb / Ta) ** 2
    return Q(f'Star {a} has surface temperature {nf(Ta)} K and luminosity {E(La, 3)} L☉. Star {b} has surface temperature {nf(Tb)} K and luminosity {E(Lb, 3)} L☉. Calculate the ratio of the radius of {a} to the radius of {b}.' + (' State which star appears bluer and why.' if D >= 4 else ''),
             f'{E(ratio)}' + (f'; {a if Ta > Tb else b} is bluer as it is hotter (shorter λmax)' if D >= 4 else ''),
             f'L ∝ r²T⁴ [1]; r_a/r_b = √(L_a/L_b) × (T_b/T_a)² [1]; = {E(ratio)} [1]' + ('; hotter star bluer via Wien [1] [4]' if D >= 4 else ' [3]'))


def _sr_c4(r, D):
    nm, T, Lr = r.choice(STARS[:-1])
    lam = WIEN / T; L = Lr * LSUN; R = math.sqrt(L / (4 * PI * SIG * T ** 4))
    intro = f'Observations of {nm} show that its spectrum peaks at {sc(lam)} m and that its luminosity is {sc(L)} W.'
    parts = [
        lambda r: ('State Wien\'s displacement law.', 'λmax ∝ 1/T (λmax T = 2.9 × 10⁻³ m K).', 'λmax T = constant [1]'),
        lambda r: ('Calculate the surface temperature.', f'{nf(T, 3)} K', 'T = 2.9 × 10⁻³/λmax [2]'),
        lambda r: ('Calculate the radius of the star.', f'{sc(R)} m', 'r = √(L/4πσT⁴) [2]'),
        lambda r: ('State one assumption made in these calculations.', 'The star is a black body (or a uniform sphere).', 'black body [1]'),
        lambda r: ('Calculate the power emitted per unit area of its surface.', f'{sc(SIG * T ** 4)} W m⁻²', 'σT⁴ [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t152.add('C4', (2, 3, 4, 5), 'multi_step')(_sr_c4)

N153 = "Hubble's law, redshift Δλ/λ = v/c and the Big Bang theory"
t153 = topic(N153, N153.lower(), "hubble's law", 'big bang theory')
LINES = [('hydrogen-alpha', 656.3), ('hydrogen-beta', 486.1), ('calcium K', 393.4), ('sodium D', 589.0), ('magnesium', 517.3)]
FX(t153, 'C1', (1, 2), [
    ('What is meant by redshift?', 'the increase in observed wavelength of radiation from a source moving away from the observer', 'Δλ/λ ≈ v/c for v ≪ c.', ['the decrease in wavelength from an approaching source', 'the reddening of stars as they cool', 'the absorption of blue light by dust']),
    ('Hubble\'s law states that the recession speed of a galaxy is', 'proportional to its distance from the Earth', 'v = H₀d.', ['inversely proportional to its distance', 'independent of its distance', 'proportional to the square of its distance']),
    ('A spectral line of laboratory wavelength 500.0 nm is observed at 510.0 nm in a galaxy. What is the recession speed?', '6.0 × 10⁶ m s⁻¹', 'v = cΔλ/λ = 3.00 × 10⁸ × 10/500.', ['6.0 × 10⁷ m s⁻¹', '2.0 × 10⁶ m s⁻¹', '1.5 × 10¹⁰ m s⁻¹']),
    ('The Hubble constant has units of', 's⁻¹', 'H₀ = v/d: m s⁻¹ ÷ m.', ['m s⁻¹', 'm s', 's']),
    ('An estimate of the age of the Universe is given by', '1/H₀', 'If expansion has been uniform, t = d/v = 1/H₀.', ['H₀', 'H₀/c', 'c/H₀']),
    ('Which observation is evidence that the Universe is expanding?', 'light from distant galaxies is redshifted by amounts that increase with distance', 'Cosmological redshift ∝ distance.', ['stars twinkle', 'the Sun emits a continuous spectrum', 'nearby stars show parallax']),
    ('State Hubble\'s law.', 'The recession speed of a galaxy is directly proportional to its distance from us (v = H₀d).', 'v ∝ d [1]'),
])
FX(t153, 'C2', (1, 2, 3, 4), [
    ('Explain how Hubble\'s law supports the Big Bang theory.', 'All distant galaxies are receding with speeds proportional to their distances, so the Universe is expanding; tracing the expansion back in time implies that everything was once concentrated at a single point and has been expanding since.', 'universe expanding [1]; extrapolate back to a single point/origin [1] [2]'),
    ('Explain how the recession speed of a galaxy is found from its spectrum.', 'Identify a known spectral line, measure its observed wavelength and compare with the laboratory wavelength: Δλ/λ = v/c, so v = cΔλ/λ.', 'compare observed and laboratory wavelength [1]; v = cΔλ/λ [1] [2]'),
    ('Explain why the age of the Universe estimated from 1/H₀ is only approximate.', 'It assumes that the expansion rate has been constant since the Big Bang; in fact it has changed (slowed by gravity, accelerated by dark energy), and H₀ itself has uncertainty.', 'assumes constant expansion rate [1]; uncertainty in H₀ / rate has changed [1] [2]'),
    ('Explain why it does not mean that the Earth is at the centre of the Universe when all distant galaxies are seen to be moving away from us.', 'Space itself is expanding uniformly; an observer in any galaxy would see all other galaxies receding with v ∝ d, so there is no special centre.', 'uniform expansion of space [1]; same view from any galaxy [1] [2]'),
])


@t153.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t153_red(r, D):
    ln, l0 = r.choice(LINES)
    z = r.choice([0.0040, 0.0080, 0.012, 0.020, 0.035, 0.050])
    l1 = round(l0 * (1 + z), 1); v = C0 * (l1 - l0) / l0
    H0 = r.choice([2.2e-18, 2.3e-18, 2.4e-18])
    s = f'The {ln} line has a wavelength of {nf(l0, 4)} nm in the laboratory. In the spectrum of a distant galaxy it is observed at {nf(l1, 4)} nm.'
    if D <= 2:
        return numq(r, D, s, 'speed of recession of the galaxy', v, ' m s⁻¹', f'v = cΔλ/λ = 3.00 × 10⁸ × {nf(l1 - l0, 3)}/{nf(l0, 4)}', [C0 * (l1 - l0) / l1 * 10, v / 3, C0 * l0 / l1], fm=lambda x: sc(x, 3))
    d = v / H0
    if D == 3:
        return Q(s + f' Taking H₀ = {sc(H0, 2)} s⁻¹, calculate the recession speed and the distance to the galaxy.', f'v = {sc(v)} m s⁻¹; d = {sc(d)} m',
                 f'Δλ/λ = {nf((l1 - l0) / l0, 3)} [1]; v = cΔλ/λ = {sc(v)} m s⁻¹ [1]; d = v/H₀ = {sc(d)} m [1] [3]')
    return Q(s + f' Take H₀ = {sc(H0, 2)} s⁻¹. (a) Calculate the recession speed. (b) Calculate the distance to the galaxy in Mpc (1 pc = 3.09 × 10¹⁶ m). (c) Use H₀ to estimate the age of the Universe in years (1 year = 3.16 × 10⁷ s).',
             f'(a) {sc(v)} m s⁻¹ (b) {nf(d / PC / 1e6, 3)} Mpc (c) {sc(1 / H0 / 3.16e7)} years', f'(a) v = cΔλ/λ = {sc(v)} m s⁻¹ [1] (b) d = v/H₀ [1]; = {nf(d / PC / 1e6, 3)} Mpc [1] (c) t = 1/H₀ [1]; = {sc(1 / H0 / 3.16e7)} years [1] [5]', 'multi_step')


@t153.add('C3', (2, 3, 4, 5), 'case')
def t153_hubble(r, D):
    H0 = r.choice([2.2e-18, 2.3e-18, 2.4e-18])
    ds = [r.choice([20, 40, 60]), r.choice([80, 100, 120]), r.choice([150, 180, 200]), r.choice([250, 300])]
    rows = '; '.join(f'd = {dm} Mpc, v = {nf(H0 * dm * 1e6 * PC / 1000, 3)} km s⁻¹' for dm in ds)
    Hk = H0 * PC * 1e6 / 1000  # km s⁻¹ Mpc⁻¹
    return Q(f'Measurements of distance d and recession speed v for four galaxies are: {rows}. Show that the data are consistent with Hubble\'s law and determine the Hubble constant in km s⁻¹ Mpc⁻¹ and in s⁻¹ (1 Mpc = 3.09 × 10²² m).' + (' Hence estimate the age of the Universe.' if D >= 4 else ''),
             f'v/d constant ≈ {nf(Hk, 3)} km s⁻¹ Mpc⁻¹ = {sc(H0)} s⁻¹' + (f'; age ≈ 1/H₀ = {sc(1 / H0)} s ≈ {sc(1 / H0 / 3.16e7)} years' if D >= 4 else ''),
             f'v/d calculated for at least two galaxies and constant [1]; H₀ = {nf(Hk, 3)} km s⁻¹ Mpc⁻¹ [1]; convert: × 10³ ÷ 3.09 × 10²² = {sc(H0)} s⁻¹ [1]' + ('; t = 1/H₀ [1] [4]' if D >= 4 else ' [3]'))


def _cos_c4(r, D):
    H0 = r.choice([2.2e-18, 2.3e-18]); ln, l0 = r.choice(LINES); v = r.choice([1.5e7, 2.4e7, 3.0e7])
    l1 = round(l0 * (1 + v / C0), 1); v = C0 * (l1 - l0) / l0
    intro = f'In the spectrum of a distant galaxy the {ln} line (laboratory wavelength {nf(l0, 4)} nm) is observed at {nf(l1, 4)} nm. The Hubble constant is {sc(H0, 2)} s⁻¹.'
    parts = [
        lambda r: ('State what is meant by redshift.', 'Increase in observed wavelength because the source is receding.', 'longer wavelength, receding [1]'),
        lambda r: ('Calculate the recession speed.', f'{sc(v)} m s⁻¹', 'v = cΔλ/λ [2]'),
        lambda r: ('Calculate the distance to the galaxy.', f'{sc(v / H0)} m', 'd = v/H₀ [2]'),
        lambda r: ('Explain how Hubble\'s law leads to the idea of the Big Bang.', 'Galaxies receding with v ∝ d means the Universe is expanding; running time backwards, all matter was once together at one point.', 'expansion [1]; common origin [1] [2]'),
        lambda r: ('Estimate the age of the Universe in years.', f'{sc(1 / H0 / 3.16e7)} years', 't = 1/H₀ [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t153.add('C4', (2, 3, 4, 5), 'multi_step')(_cos_c4)
CHAPTERS[15] = [t151, t152, t153]

# ===================================================================== 16 Planning, analysis and evaluation (Paper 5)
PLANS = [
    dict(q='how the period T of oscillation of a mass on a spring depends on the mass m', iv='mass m', dv='period T', cv='the same spring (spring constant) and small amplitude',
         meas='time 20 oscillations with a stopwatch using a fiducial marker at the equilibrium position, repeat and divide by 20; measure m with a top-pan balance',
         rel='T = 2π√(m/k)', plot='T² against m', grad='4π²/k', safety='clamp the stand to the bench / use a sand tray under the masses in case they fall'),
    dict(q='how the resistance R of a thermistor depends on its thermodynamic temperature T, given that R = R₀e^(b/T)', iv='temperature T', dv='resistance R', cv='the same thermistor; ensure thermal equilibrium (stir the water bath)',
         meas='place the thermistor in a stirred water bath with a thermometer; measure R with an ohmmeter (or V and I) at several temperatures; convert to kelvin',
         rel='ln R = ln R₀ + b/T', plot='ln R against 1/T', grad='b', safety='take care with hot water / use a heatproof mat and do not touch the hot beaker'),
    dict(q='how the intensity of γ-radiation transmitted through lead depends on the thickness x of lead, given I = I₀e^(−μx)', iv='thickness x of lead', dv='count rate (corrected for background)', cv='the same source and source–detector distance; same counting time',
         meas='measure x with a micrometer; count with a Geiger–Müller tube and counter for a fixed long time; measure the background count and subtract',
         rel='ln C = ln C₀ − μx', plot='ln(corrected count rate) against x', grad='−μ', safety='handle the source with long tongs, keep a distance and minimise exposure time; store in a lead-lined box'),
    dict(q='how the terminal velocity v of a steel ball falling through oil depends on its radius r, given v = kr^n', iv='radius r of the ball', dv='terminal velocity v', cv='the same oil at the same temperature; balls of the same material',
         meas='measure the diameter with a micrometer; time the ball between two marks on the tube (well below the surface so that it is at terminal velocity) with a stopwatch or light gates',
         rel='lg v = n lg r + lg k', plot='lg v against lg r', grad='n', safety='wipe up spilt oil immediately to avoid slipping'),
    dict(q='how the time t½ for the p.d. across a discharging capacitor to halve depends on the resistance R in the circuit', iv='resistance R', dv='time t½ for the p.d. to halve', cv='the same capacitor and the same initial charging voltage',
         meas='charge the capacitor, then discharge through R; use a voltmeter (or data-logger) and stopwatch to find the time for V to fall to half its initial value; measure R with an ohmmeter',
         rel='t½ = RC ln 2', plot='t½ against R', grad='C ln 2', safety='discharge large capacitors before handling; keep supply p.d. low'),
    dict(q='how the frequency f of a vibrating wire depends on the tension T in the wire', iv='tension T', dv='frequency f of the fundamental', cv='the same wire (mass per unit length) and the same vibrating length',
         meas='vary T by hanging masses (T = mg) over a pulley; use a signal generator and vibrator to find the resonant frequency of the fundamental (largest amplitude)',
         rel='f = (1/2L)√(T/μ)', plot='f² against T', grad='1/(4L²μ)', safety='wear safety goggles in case the wire snaps; use a sand tray beneath the masses'),
    dict(q='how the magnetic flux density B at a distance d from a long straight wire depends on d', iv='distance d from the wire', dv='magnetic flux density B', cv='the same current in the wire; the probe oriented at right angles to the field',
         meas='measure B with a calibrated Hall probe; measure d from the centre of the wire with a ruler; reverse the current and average to remove the Earth\'s field',
         rel='B = k/d', plot='B against 1/d', grad='k (= μ₀I/2π)', safety='the wire may become hot at high current: switch off between readings'),
    dict(q='how the e.m.f. E induced in a small search coil depends on the frequency f of the alternating current in a solenoid', iv='frequency f', dv='peak induced e.m.f. E', cv='the same r.m.s. current in the solenoid; the same position and orientation of the search coil',
         meas='use a signal generator to supply the solenoid with an ammeter in series to keep current constant; measure the peak e.m.f. with an oscilloscope; read f from the time-base',
         rel='E ∝ f', plot='E against f', grad='constant of proportionality', safety='avoid touching the solenoid which may become hot'),
    dict(q='how the amplitude A of a pendulum decreases with the number n of oscillations when a card is attached to the bob, given A = A₀e^(−kn)', iv='number of oscillations n', dv='amplitude A', cv='the same card, length of pendulum and initial amplitude',
         meas='measure A against a scale behind the pendulum, viewed at eye level to avoid parallax (or video and step through frames)',
         rel='ln A = ln A₀ − kn', plot='ln A against n', grad='−k', safety='ensure the stand is clamped so that it does not topple'),
    dict(q='how the force F between two magnets depends on their separation d, given F = k/dⁿ', iv='separation d', dv='repulsive force F', cv='the same pair of magnets with the same orientation',
         meas='place one magnet on a top-pan balance and clamp the other above it; F = (change in reading) × g; measure d with a vernier caliper or ruler',
         rel='lg F = lg k − n lg d', plot='lg F against lg d', grad='−n', safety='keep magnets away from electronic devices; take care not to trap fingers between strong magnets'),
    dict(q='how the maximum kinetic energy of photoelectrons from a metal depends on the frequency f of the incident light', iv='frequency f of the light', dv='stopping potential V_s', cv='the same metal surface (clean); the same intensity',
         meas='use filters (or LEDs) of known wavelength; increase a reverse p.d. until the photocurrent just falls to zero; read V_s from a voltmeter',
         rel='eV_s = hf − Φ', plot='V_s against f', grad='h/e', safety='do not look directly at the UV source; wear UV-protective goggles'),
    dict(q='how the time constant of an RC circuit depends on the capacitance C, given V = V₀e^(−t/RC)', iv='capacitance C', dv='time constant τ', cv='the same resistor and the same charging voltage',
         meas='record V against t with a data-logger for each capacitor; find τ as −1/gradient of ln V against t',
         rel='τ = RC', plot='τ against C', grad='R', safety='keep the charging p.d. low and discharge capacitors before handling'),
]

N161 = 'Planning an investigation: identifying variables and methods'
t161 = topic(N161, N161.lower(), 'planning an investigation', 'identifying variables')
FX(t161, 'C1', (1, 2), [
    ('In an investigation of how the period of a pendulum depends on its length, the length is the', 'independent variable', 'The quantity deliberately changed.', ['dependent variable', 'control variable', 'derived variable']),
    ('In a planning question, a control variable is one that', 'is kept constant so that it does not affect the dependent variable', 'Fair test.', ['is measured to find the result', 'is changed by the experimenter', 'is calculated from the gradient']),
    ('A student wants to find how the count rate from a γ source depends on the thickness of an absorber. What must be measured first and then subtracted?', 'the background count rate', 'Background radiation adds to every reading.', ['the half-life of the source', 'the mass of the absorber', 'the dead time of the counter']),
    ('Which instrument is most suitable to measure the diameter of a steel ball bearing of about 5 mm?', 'a micrometer screw gauge', 'Resolution 0.01 mm.', ['a metre rule', 'a measuring tape', 'a protractor']),
    ('Why should a ball falling in a tube of oil be timed between two marks well below the oil surface?', 'so that it has reached terminal velocity', 'It accelerates initially.', ['so that the oil is cooler there', 'so that the timing is shorter', 'to avoid parallax error']),
    ('In a Paper 5 plan, which is the best way to ensure a wire in a magnetic field experiment is at right angles to the field?', 'use a set square or protractor to align the wire with the magnet faces', 'Direct method of checking the angle.', ['estimate by eye only', 'use a longer wire', 'use a larger current']),
    ('State what is meant by the dependent variable in an experiment.', 'The variable that is measured, whose value depends on the independent variable.', 'quantity measured that responds [1]'),
])
FX(t161, 'C2', (1, 2, 3, 4), [
    ('Explain why a range of at least six values of the independent variable is used in an investigation.', 'Enough points are needed to establish the trend and draw a reliable best-fit line; spreading them over a wide range shows whether the relationship holds and reduces the effect of uncertainty on the gradient.', 'enough points for a reliable line/trend [1]; wide range [1] [2]'),
    ('Explain why a data-logger may be better than a stopwatch for measuring a rapidly changing p.d.', 'A data-logger takes readings at precise short intervals without human reaction time, so it can record changes too fast to read by eye.', 'many readings at short intervals [1]; no reaction-time error [1] [2]'),
    ('Explain the importance of a safety precaution in an investigation using a radioactive source.', 'Ionising radiation can damage cells; using tongs, keeping a distance and limiting exposure time reduce the dose received.', 'radiation hazard to cells [1]; precaution reduces dose [1] [2]'),
    ('Explain why a student should check that a relationship is linear before extracting a constant from the gradient.', 'If the points do not lie on a straight line within their uncertainties the assumed relationship is not supported, so a gradient would not give a valid constant.', 'linearity tests the relationship [1]; gradient only meaningful if linear [1] [2]'),
])


@t161.add('C3', (1, 2, 3, 4, 5), 'case')
def t161_vars(r, D):
    p = r.choice(PLANS)
    who = person(r)
    if D <= 2:
        cands = [x['iv'] for x in PLANS if x['iv'] != p['iv']]
        opts, a = mcq(r, p['iv'], r.sample(cands, 3) + [p['dv']])
        return Q(f'{who} plans an experiment to investigate {p["q"]}. Which is the independent variable?', a, f'Independent: {p["iv"]}; dependent: {p["dv"]}.', opts=opts)
    if D == 3:
        return Q(f'{who} plans an experiment to investigate {p["q"]}. Identify the independent variable, the dependent variable and one variable that should be controlled.',
                 f'Independent: {p["iv"]}; dependent: {p["dv"]}; control: {p["cv"]}.', 'independent [1]; dependent [1]; control variable [1] [3]')
    return Q(f'{who} plans an experiment to investigate {p["q"]}. (a) Identify the independent and dependent variables. (b) Describe how the dependent variable should be measured. (c) State one safety precaution.',
             f'(a) independent: {p["iv"]}; dependent: {p["dv"]} (b) {p["meas"]} (c) {p["safety"]}', f'(a) both variables [1] (b) method [1]; detail improving accuracy [1] (c) relevant precaution [1] [4]', 'multi_step')


@t161.add('C2', (2, 3, 4), 'explain')
def t161_analysis(r, D):
    p = r.choice(PLANS)
    return Q(f'An experiment is planned to investigate {p["q"]}. Explain how the data should be analysed to test the relationship {p["rel"]}.',
             f'Plot {p["plot"]}; a straight line confirms the relationship; gradient = {p["grad"]}.', f'plot {p["plot"]} [1]; straight line test and gradient = {p["grad"]} [1]' + ('; how the constant is found from the gradient or intercept [1] [3]' if D >= 3 else ' [2]'))


def _plan_c4(r, D):
    p = r.choice(PLANS)
    who = person(r)
    intro = f'{who} is asked to plan an investigation into {p["q"]}. It is suggested that the relationship is {p["rel"]}. (Paper 5 planning)'
    parts = [
        lambda r: ('Identify the independent and dependent variables.', f'Independent: {p["iv"]}; dependent: {p["dv"]}.', 'both [1]'),
        lambda r: ('State the key variable to be controlled and how it is controlled.', cap(p['cv']) + '.', 'control variable with method [1]'),
        lambda r: ('Describe the method of data collection, including the instruments used.', cap(p['meas']) + '.', 'how independent variable varied/measured [1]; how dependent variable measured [1]; additional detail [1] [3]'),
        lambda r: ('Explain how the data are analysed.', f'Plot {p["plot"]}; the relationship is valid if it is a straight line; gradient = {p["grad"]}.', 'graph [1]; validity check [1]; constant from gradient [1] [3]'),
        lambda r: ('State one safety precaution.', cap(p['safety']) + '.', 'relevant precaution [1]'),
        lambda r: ('Suggest one additional detail to improve the accuracy.', 'Repeat readings and average; use a wide range of values; check for zero errors.', 'valid detail [1]'),
    ]
    return compose(r, intro, parts, k=(3, 4, 5), type_='long')


t161.add('C4', (2, 3, 4, 5), 'long')(_plan_c4)

N162 = 'Analysis: logarithmic graphs to test relationships and determining constants'
t162 = topic(N162, N162.lower(), 'logarithmic graphs', 'determining constants')
LOGREL = [('y = axⁿ', 'lg y', 'lg x', 'n', 'lg a'), ('V = V₀e^(−t/RC)', 'ln V', 't', '−1/RC', 'ln V₀'), ('I = I₀e^(−μx)', 'ln I', 'x', '−μ', 'ln I₀'), ('T = kmⁿ', 'lg T', 'lg m', 'n', 'lg k'),
          ('R = R₀e^(b/T)', 'ln R', '1/T', 'b', 'ln R₀'), ('F = k/dⁿ', 'lg F', 'lg d', '−n', 'lg k'), ('A = A₀e^(−λt)', 'ln A', 't', '−λ', 'ln A₀'), ('P = cVⁿ', 'lg P', 'lg V', 'n', 'lg c'),
          ('N = N₀e^(kt)', 'ln N', 't', 'k', 'ln N₀'), ('E = aTⁿ', 'lg E', 'lg T', 'n', 'lg a'), ('θ = θ₀e^(−t/τ)', 'ln θ', 't', '−1/τ', 'ln θ₀'), ('v = k√(T/μ)', 'v²', 'T', 'k²/μ', 'zero')]
FX(t162, 'C1', (1, 2), [
    ('A quantity y is thought to depend on x according to y = axⁿ. Which graph gives a straight line?', 'lg y against lg x', 'lg y = n lg x + lg a.', ['y against lg x', 'lg y against x', 'y against xⁿ with n unknown']),
    ('A capacitor discharges according to V = V₀e^(−t/RC). A graph of ln V against t has gradient', '−1/RC', 'ln V = ln V₀ − t/RC.', ['−RC', 'ln V₀', '1/RC']),
    ('The graph of lg y against lg x is a straight line with gradient 1.5 and y-intercept 0.30. What is the relationship?', 'y = 2.0x^1.5', 'a = 10^0.30 = 2.0, n = 1.5.', ['y = 0.30x^1.5', 'y = 1.5x^2.0', 'y = 2.0e^(1.5x)']),
    ('To test the relationship I = I₀e^(−μx), a student should plot', 'ln I against x', 'ln I = ln I₀ − μx.', ['lg I against lg x', 'I against x²', '1/I against x']),
    ('A graph of ln N against t is a straight line with gradient −0.023 s⁻¹. What is the half-life?', '30 s', 't½ = ln 2/0.023.', ['0.016 s', '43 s', '23 s']),
    ('Why are logarithmic graphs useful in analysing experimental data?', 'they convert power-law and exponential relationships into straight lines', 'Gradient and intercept give the constants.', ['they always pass through the origin', 'they remove the need for units', 'they reduce random errors to zero']),
    ('State the quantity given by the y-intercept of a graph of lg y against lg x for y = axⁿ.', 'lg a', 'lg a [1]'),
])
FX(t162, 'C2', (1, 2, 3, 4), [
    ('Explain why taking logarithms of both sides of y = axⁿ allows n to be found from a graph.', 'lg y = n lg x + lg a has the form Y = mX + c, so a graph of lg y against lg x is a straight line with gradient n and intercept lg a.', 'log equation in straight-line form [1]; gradient n, intercept lg a [1] [2]'),
    ('Explain why natural logarithms are used for exponential relationships such as A = A₀e^(−λt).', 'ln(e^(−λt)) = −λt, so ln A = ln A₀ − λt is linear in t with gradient −λ directly.', 'ln of exponential gives linear term [1]; gradient −λ [1] [2]'),
    ('Explain why the y-intercept of a lg–lg graph often cannot be read directly from the graph.', 'The x-axis values of lg x on the plotted range often do not include lg x = 0, so the intercept must be calculated from y = mx + c using a point on the line and the gradient.', 'lg x = 0 not on axis range [1]; calculate c from a point and gradient [1] [2]'),
])


@t162.add('C3', (1, 2, 3, 4), 'case')
def t162_what(r, D):
    eq, y, x, g, c = r.choice(LOGREL)
    if D <= 2:
        wrong = [f'{x} against {y}', f'{y.replace("lg ", "").replace("ln ", "")} against {x}', f'{y} against {x.replace("lg ", "")}' if 'lg' in x else f'lg {y.split()[-1]} against lg {x}']
        opts, a = mcq(r, f'{y} against {x}', wrong + [f'{y} against {x}²'])
        return Q(f'A student wants to test the relationship {eq} using a straight-line graph. Which graph should be plotted?', a, f'Plot {y} against {x}: gradient {g}, y-intercept {c}.', opts=opts)
    return Q(f'It is suggested that two quantities are related by {eq}, where the other symbols are constants. A graph is plotted to test this. State the quantities to plot on each axis and give expressions for the gradient and the y-intercept.' + (' Explain how you would decide whether the relationship is valid.' if D >= 4 else ''),
             f'y-axis {y}, x-axis {x}; gradient = {g}; y-intercept = {c}' + ('; valid if the points lie on a straight line within their error bars' if D >= 4 else ''),
             f'axes [1]; gradient = {g} [1]; intercept = {c} [1]' + ('; straight line within error bars [1] [4]' if D >= 4 else ' [3]'))


@t162.add('C3', (2, 3, 4, 5), 'case')
def t162_power(r, D):
    a = r.choice([0.50, 1.2, 2.0, 3.5, 4.0]); n = r.choice([0.5, 1.5, 2.0, 3.0, -1.0, -2.0])
    xs = r.choice([[1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 4.0, 6.0, 8.0, 10.0], [1.5, 2.5, 3.5, 4.5, 5.5]])
    ys = [a * x ** n for x in xs]
    rows = '; '.join(f'x = {nf(x)}, y = {E(y, 3)}' for x, y in zip(xs, ys))
    lx = [math.log10(x) for x in xs]; ly = [math.log10(y) for y in ys]
    g = (ly[-1] - ly[0]) / (lx[-1] - lx[0])
    return Q(f'A student obtains these results: {rows}. It is suggested that y = axⁿ. (a) Calculate lg x and lg y for the first and last results. (b) Determine the gradient of a graph of lg y against lg x. (c) Hence find n and a.',
             f'(a) lg x = {nf(lx[0], 3) if lx[0] else "0"}, {nf(lx[-1], 3)}; lg y = {nf(ly[0], 3) if abs(ly[0]) > 1e-9 else "0"}, {nf(ly[-1], 3)} (b) {nf(g, 3)} (c) n = {nf(g, 2)}, a = {nf(a, 2)}',
             f'(a) logs to 3 d.p. or s.f. [1] (b) gradient from large triangle = {nf(g, 3)} [1] (c) n = gradient [1]; lg a = lg y − n lg x, a = {nf(a, 2)} [1]' + (' [4]' if D <= 4 else '; comment that a straight line confirms the power law [1] [5]'))


@t162.add('C3', (2, 3, 4, 5), 'case')
def t162_exp(r, D):
    kind = r.choice(['cap', 'abs', 'cool'])
    if kind == 'cap':
        V0 = r.choice([6.0, 9.0, 12.0]); RC = r.choice([20.0, 33.0, 47.0, 68.0]); ts = [0, 10, 20, 30, 40, 50]
        ys = [V0 * math.exp(-t / RC) for t in ts]; lab_ = 'V / V'; xl = 't / s'; k = 1 / RC
        ask = f'(c) The resistance is {r.choice([10, 22, 47])} kΩ. Calculate the capacitance.'
        R_ = float(ask.split('is ')[1].split(' kΩ')[0]) * 1e3
        ans_c = f'C = RC/R = {sc(RC / R_)} F'; key_c = f'RC = −1/gradient = {nf(RC, 3)} s [1]; C = {sc(RC / R_)} F [1]'
    elif kind == 'abs':
        V0 = r.choice([800.0, 1200.0, 2000.0]); mu = r.choice([0.25, 0.40, 0.55]); ts = [0, 1, 2, 3, 4, 5]
        ys = [V0 * math.exp(-mu * t) for t in ts]; lab_ = 'C / counts min⁻¹'; xl = 'x / cm'; k = mu
        ans_c = f'μ = {nf(mu, 3)} cm⁻¹; half-value thickness = {nf(math.log(2) / mu, 3)} cm'; key_c = f'μ = −gradient [1]; x½ = ln 2/μ = {nf(math.log(2) / mu, 3)} cm [1]'
        ask = '(c) Determine the linear attenuation coefficient μ and the half-value thickness.'
    else:
        V0 = r.choice([50.0, 60.0, 70.0]); tau = r.choice([300.0, 450.0, 600.0]); ts = [0, 120, 240, 360, 480, 600]
        ys = [V0 * math.exp(-t / tau) for t in ts]; lab_ = '(θ − θ_room) / K'; xl = 't / s'; k = 1 / tau
        ans_c = f'τ = {nf(tau, 3)} s'; key_c = f'τ = −1/gradient [1]; = {nf(tau, 3)} s [1]'
        ask = '(c) The excess temperature is given by θ = θ₀e^(−t/τ). Determine τ.'
    rows = '; '.join(f'{xl.split(" /")[0]} = {t}, {lab_.split(" /")[0]} = {nf(y, 3)}' for t, y in zip(ts, ys))
    g = -k
    return Q(f'Data from an experiment ({xl}, {lab_}): {rows}. (a) Explain why a graph of the natural logarithm of the second quantity against the first should be a straight line. (b) Determine the gradient of this graph. {ask}',
             f'(a) exponential decay y = y₀e^(−kx) gives ln y = ln y₀ − kx (b) {sc(g)} (in units of {xl.split("/ ")[1]}⁻¹) {ans_c}',
             f'(a) ln y = ln y₀ − kx linear [1] (b) ln values [1]; gradient = {sc(g)} [1] (c) {key_c} [5]')


def _log_c4(r, D):
    n = r.choice([0.5, 2.0, 1.5]); k = r.choice([0.20, 0.45, 1.6])
    intro = f'A student investigates how the terminal speed v of a sphere falling in a liquid depends on its radius r. It is suggested that v = kr^n.'
    rs = [1.0, 2.0, 3.0, 4.0]
    vs = [k * x ** n for x in rs]
    parts = [
        lambda r: ('Explain why a graph of lg v against lg r should be plotted.', 'lg v = n lg r + lg k: straight line with gradient n and intercept lg k.', 'log form [1]; gradient n, intercept lg k [1] [2]'),
        lambda r: (f'For r = 4.0 mm, v = {nf(vs[3], 3)} cm s⁻¹. Calculate lg r and lg v, to 3 s.f.', f'lg r = 0.602; lg v = {nf(math.log10(vs[3]), 3)}', 'both values [1]'),
        lambda r: (f'For r = 1.0 mm, v = {nf(vs[0], 3)} cm s⁻¹. Use this and the previous point to find n.', f'n = {nf(n, 2)}', 'gradient = Δlg v/Δlg r [1]; value of n [1] [2]'),
        lambda r: ('Determine k, with its unit.', f'k = {nf(k, 2)} cm s⁻¹ mm^(−{nf(n, 2)})', 'k = v/rⁿ at a point [1]; value with unit [1] [2]'),
        lambda r: ('Suggest why logarithmic scales are useful when the data span a wide range.', 'They compress the range so all points can be plotted with useful precision.', 'compress range [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t162.add('C4', (2, 3, 4, 5), 'multi_step')(_log_c4)

N163 = 'Treatment of uncertainties: error bars, worst acceptable lines and uncertainty in gradient'
t163 = topic(N163, N163.lower(), 'treatment of uncertainties', 'worst acceptable lines')
FX(t163, 'C1', (1, 2), [
    ('A worst acceptable straight line is drawn', 'through the error bars with the steepest or shallowest gradient that still fits the data', 'Used with the best-fit line to find the uncertainty in the gradient.', ['through the first and last points only', 'through the origin', 'parallel to the best-fit line']),
    ('The best-fit line has gradient 2.40 and the worst acceptable line has gradient 2.55. What is the absolute uncertainty in the gradient?', '0.15', '|2.55 − 2.40|.', ['0.075', '4.95', '2.55']),
    ('A value of x is 4.0 ± 0.2. What is the absolute uncertainty in ln x?', '0.05', 'Δ(ln x) = Δx/x = 0.2/4.0.', ['0.2', '0.69', '0.0125']),
    ('A period T is measured as 2.00 ± 0.02 s. What is the percentage uncertainty in T²?', '2%', 'Double the percentage uncertainty in T (1%).', ['1%', '4%', '0.04%']),
    ('Error bars on a graph represent', 'the absolute uncertainty in each plotted value', 'They show the range within which the true value is likely.', ['the random scatter of the line', 'the resolution of the graph paper', 'the systematic error only']),
    ('A value of y is 25 ± 1. What is the absolute uncertainty in lg y?', '0.017', 'Δ(lg y) = 0.434 × Δy/y = 0.434 × 0.04.', ['0.04', '1.0', '0.0017']),
    ('State how the percentage uncertainty in the gradient is calculated.', '(|best gradient − worst gradient| ÷ best gradient) × 100%', 'difference ÷ best × 100 [1]'),
])
FX(t163, 'C2', (1, 2, 3, 4), [
    ('Explain how error bars and a worst acceptable line are used to find the uncertainty in a gradient.', 'Plot error bars for each point; draw the best-fit line and the steepest (or shallowest) straight line that passes through all the error bars; the uncertainty is the difference between their gradients.', 'error bars and worst line through them [1]; uncertainty = difference in gradients [1] [2]'),
    ('Explain why the uncertainty in ln y is Δy/y rather than ln(Δy).', 'For small changes, d(ln y) = dy/y, so an absolute uncertainty Δy in y produces an uncertainty Δy/y in ln y; ln(Δy) has no meaning as an uncertainty.', 'd(ln y)/dy = 1/y [1]; Δ(ln y) = Δy/y [1] [2]'),
    ('Explain how the uncertainty in the y-intercept can be found from a graph.', 'Find the intercept of the worst acceptable line (calculated using its gradient and a point on it); the uncertainty is the difference between this and the best-fit intercept.', 'intercept of worst line [1]; difference from best intercept [1] [2]'),
])


@t163.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t163_grad(r, D):
    rel, const, gs, gu, fn, fw, cu = r.choice([
        ('T² = (4π²/g)l, using a graph of T²/s² against l/m', 'g', [3.98, 4.05, 4.12, 4.21], 's² m⁻¹', lambda x: 4 * PI ** 2 / x, 'g = 4π²/gradient', 'm s⁻²'),
        ('V = E − Ir, using a graph of V/V against I/A (magnitude of gradient = r)', 'r', [0.524, 0.850, 1.24, 2.15], 'Ω', lambda x: x, 'r = |gradient|', 'Ω'),
        ('ln A = ln A₀ − λt, using a graph of ln(A/Bq) against t/s (magnitude of gradient = λ)', 'λ', [0.0368, 0.0125, 0.231, 0.00462], 's⁻¹', lambda x: x, 'λ = |gradient|', 's⁻¹'),
        ('eV_s = hf − Φ, using a graph of V_s/V against f/Hz', 'h', [4.02e-15, 4.18e-15, 4.31e-15], 'V s', lambda x: x * QE, 'h = gradient × e', 'J s'),
        ('t½ = (C ln 2)R, using a graph of t½/s against R/Ω', 'C', [3.21e-4, 6.86e-4, 1.52e-3], 's Ω⁻¹', lambda x: x / math.log(2), 'C = gradient/ln 2', 'F')])
    g = r.choice(gs); dg = g * r.choice([0.03, 0.04, 0.05, 0.06, 0.08])
    gw = g + dg if r.random() < 0.5 else g - dg
    pct = abs(gw - g) / g * 100
    s = f'In an experiment to test {rel}, the best-fit line has gradient {E(g)} {gu} and the worst acceptable line has gradient {E(gw)} {gu}.'
    if D <= 2:
        return numq(r, D, s, 'percentage uncertainty in the gradient', pct, '%', f'|{E(gw)} − {E(g)}|/{E(g)} × 100', [pct * 2, pct / 2, pct * 3], fm=lambda x: nf(x, 2))
    cval = fn(g)
    if D == 3:
        return Q(s + ' Calculate the absolute and percentage uncertainties in the gradient.', f'{E(abs(gw - g), 2)} {gu}; {nf(pct, 2)}%', f'absolute = |difference| = {E(abs(gw - g), 2)} {gu} [1]; ÷ best gradient [1]; × 100 = {nf(pct, 2)}% [1] [3]')
    return Q(s + f' (a) Calculate the percentage uncertainty in the gradient. (b) Determine {const} and its absolute uncertainty.',
             f'(a) {nf(pct, 2)}% (b) {const} = {E(cval)} ± {E(cval * pct / 100, 1)} {cu}', f'(a) {nf(pct, 2)}% [1] (b) {fw} = {E(cval)} {cu} [1]; same percentage uncertainty [1]; absolute uncertainty = {E(cval * pct / 100, 1)} {cu} [1] [4]', 'multi_step')


@t163.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t163_log(r, D):
    x = r.choice([2.5, 4.0, 6.8, 12.5, 25.0, 0.80, 0.45]); dx = round(x * r.choice([0.02, 0.04, 0.05]), 2 if x < 1 else 1)
    if dx == 0:
        return None
    use_ln = r.choice([True, False])
    if use_ln:
        val = math.log(x); dv = dx / x; fn_ = 'ln'
    else:
        val = math.log10(x); dv = dx / (x * math.log(10)); fn_ = 'lg'
    s = f'A measured value is {nf(x)} ± {nf(dx)}.'
    if D <= 2:
        return numq(r, D, s, f'absolute uncertainty in {fn_} of this value', dv, '', f'Δ({fn_} x) = ' + (f'Δx/x = {nf(dx)}/{nf(x)}' if use_ln else f'0.434 Δx/x = 0.434 × {nf(dx)}/{nf(x)}'), [dx, (math.log(x + dx) if use_ln else math.log10(x + dx)), dv * 10], fm=lambda v: nf(v, 2))
    maxv = math.log(x + dx) if use_ln else math.log10(x + dx)
    return Q(s + f' Calculate {fn_} of the value and its absolute uncertainty, giving both to an appropriate number of decimal places.' + (' Show that using the maximum value x + Δx gives the same uncertainty.' if D >= 4 else ''),
             f'{fn_} x = {val:.3f} ± {nf(dv, 1)}' + (f'; {fn_}(x + Δx) − {fn_} x = {maxv - val:.3f}' if D >= 4 else ''),
             f'{fn_} x = {val:.3f} [1]; uncertainty = {nf(dv, 2)} [1]; consistent decimal places [1]' + ('; max-min method agrees [1] [4]' if D >= 4 else ' [3]'))


@t163.add('C3', (2, 3, 4), 'numerical')
def t163_combine(r, D):
    l = r.choice([0.385, 0.450, 0.600, 0.725, 0.850, 1.000]); dl = 0.002; dT = r.choice([0.01, 0.02])
    T = round(2 * PI * math.sqrt(l / (GR * r.uniform(0.97, 1.03))), 2)
    pT = dT / T * 100; pl = dl / l * 100; pg = pl + 2 * pT
    gv = 4 * PI ** 2 * l / T ** 2
    return Q(f'A pendulum of length l = {l:.3f} ± 0.002 m has period T = {T:.2f} ± {dT:.2f} s. Calculate g = 4π²l/T² and its absolute uncertainty.',
             f'g = {nf(gv, 3)} ± {nf(gv * pg / 100, 1)} m s⁻²', f'%Δl = {nf(pl, 2)}%, %ΔT = {nf(pT, 2)}% [1]; %Δg = %Δl + 2 × %ΔT = {nf(pg, 2)}% [1]; g = {nf(gv, 3)} ± {nf(gv * pg / 100, 1)} m s⁻² [1]' + (' [3]' if D <= 3 else '; comment on which measurement dominates [1] [4]'))


def _unc_c4(r, D):
    b = r.choice([0.385, 0.412, 0.0460]); w = b * r.choice([1.05, 1.07, 0.94])
    c = r.choice([1.20, 2.50]); cw = c + r.choice([-0.06, 0.08])
    intro = f'In a Paper 5 analysis, a graph of ln(V/V) against t/s is plotted with error bars. The best-fit line has gradient −{nf(b, 3)} s⁻¹ and y-intercept {nf(c, 3)}. The worst acceptable line has gradient −{nf(w, 3)} s⁻¹ and y-intercept {nf(cw, 3)}.'
    parts = [
        lambda r: ('Explain how the worst acceptable line is drawn.', 'Steepest or shallowest straight line passing through all the error bars.', 'through all error bars, extreme gradient [1]'),
        lambda r: ('Determine the uncertainty in the gradient.', f'± {nf(abs(w - b), 2)} s⁻¹', 'difference of gradients [1]'),
        lambda r: ('The relationship is V = V₀e^(−t/RC). Determine RC and its absolute uncertainty.', f'RC = {nf(1 / b, 3)} ± {nf(abs(1 / w - 1 / b), 2)} s', 'RC = −1/gradient [1]; uncertainty [1] [2]'),
        lambda r: ('Determine V₀ and its absolute uncertainty.', f'V₀ = {nf(math.exp(c), 3)} ± {nf(abs(math.exp(cw) - math.exp(c)), 2)} V', 'V₀ = e^intercept [1]; uncertainty [1] [2]'),
        lambda r: ('The resistance is 22.0 kΩ ± 5%. Calculate the capacitance and its percentage uncertainty.', f'C = {sc(1 / b / 22.0e3)} F ± {nf(abs(w - b) / b * 100 + 5, 2)}%', 'C = RC/R [1]; add percentages [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t163.add('C4', (2, 3, 4, 5), 'multi_step')(_unc_c4)

N164 = 'Evaluation: conclusions and reliability of data and risk assessment'
t164 = topic(N164, N164.lower(), 'evaluation', 'risk assessment')
FX(t164, 'C1', (1, 2), [
    ('An experimental value of g is 9.6 ± 0.3 m s⁻². The accepted value is 9.81 m s⁻². Which conclusion is correct?', 'the result agrees with the accepted value within the uncertainty', '9.81 lies within 9.3–9.9.', ['the result disagrees with the accepted value', 'the experiment has no uncertainty', 'the result proves the accepted value is wrong']),
    ('Which change most improves the reliability of a set of results?', 'repeating readings and calculating means', 'Reduces the effect of random errors and reveals anomalies.', ['using fewer readings', 'rounding the values more', 'ignoring anomalous points without checking']),
    ('A systematic error in a set of measurements', 'shifts all readings in the same direction by a similar amount', 'E.g. a zero error.', ['causes random scatter about the true value', 'is reduced by averaging', 'only affects the first reading']),
    ('A best-fit line of a graph of y against x that should pass through the origin has a non-zero y-intercept. The most likely cause is', 'a systematic error', 'A constant offset in readings.', ['a random error', 'too many readings', 'the gradient being too large']),
    ('In a risk assessment for an experiment using a laser, the most appropriate precaution is', 'do not look into the beam and avoid reflections from shiny surfaces', 'Laser light can damage the retina.', ['wear thick gloves', 'use a sand tray', 'keep the laser in a lead box']),
    ('Which statement describes an anomalous result?', 'a reading that does not fit the pattern of the others', 'It should be checked and repeated.', ['the largest value recorded', 'the value with the smallest uncertainty', 'the mean of the readings']),
    ('State what is meant by the reliability of a set of results.', 'The extent to which repeated measurements give consistent values.', 'consistency on repetition [1]'),
])
FX(t164, 'C2', (1, 2, 3, 4), [
    ('Explain how a student should decide whether an experimental value supports a theoretical prediction.', 'Calculate the uncertainty in the experimental value; if the predicted value lies within the range value ± uncertainty, the result supports the prediction; if not, there may be a systematic error or the theory may not apply.', 'compare using uncertainty range [1]; conclusion if within/outside [1] [2]'),
    ('Explain the difference between the accuracy and the precision of a result.', 'Accuracy is how close a result is to the true value; precision is how close repeated readings are to each other (small spread), regardless of whether they are close to the true value.', 'accuracy: close to true value [1]; precision: small spread [1] [2]'),
    ('Explain why a risk assessment is part of planning an experiment.', 'It identifies hazards (e.g. hot liquids, radiation, high voltage, falling masses) and specifies precautions to reduce the risk of harm before the experiment is carried out.', 'identify hazards [1]; precautions to reduce risk [1] [2]'),
    ('Explain why a graph with a straight line through the origin is stronger evidence for proportionality than two calculated ratios that agree.', 'A graph uses many readings over a range and shows any trend or curvature; two ratios could agree by chance and give no information about intermediate values or systematic errors.', 'many points over a range [1]; two ratios could agree by chance [1] [2]'),
])


@t164.add('C3', (1, 2, 3, 4, 5), 'case')
def t164_agree(r, D):
    q, acc, u = r.choice([('the acceleration of free fall g', 9.81, 'm s⁻²'), ('the Planck constant h', 6.63e-34, 'J s'), ('the specific heat capacity of water', 4200.0, 'J kg⁻¹ K⁻¹'),
                          ('the speed of sound in air', 340.0, 'm s⁻¹'), ('the specific charge of the electron', 1.76e11, 'C kg⁻¹'), ('the half-life of protactinium-234', 70.0, 's')])
    off = r.choice([0.94, 0.97, 1.02, 1.05, 1.08]); pct = r.choice([2.0, 3.0, 4.0, 6.0])
    val = acc * off; dv = val * pct / 100
    ok = abs(val - acc) <= dv
    s = f'A student determines {q} as {E(val)} ± {E(dv, 2)} {u}. The accepted value is {E(acc)} {u}.'
    if D <= 2:
        opts, a = mcq(r, 'consistent with the accepted value' if ok else 'not consistent with the accepted value', ['consistent with the accepted value' if not ok else 'not consistent with the accepted value', 'proved to be exactly correct', 'impossible to judge without a graph'])
        return Q(s + ' The result is', a, f'Range {E(val - dv)} to {E(val + dv)}; accepted value {"inside" if ok else "outside"} this range.', opts=opts)
    if D == 3:
        return Q(s + ' Calculate the percentage difference from the accepted value and state, with a reason, whether the result agrees with it.', f'{nf(abs(off - 1) * 100, 2)}%; ' + ('agrees: the difference is within the uncertainty' if ok else 'does not agree: the difference is greater than the uncertainty'),
                 f'percentage difference = {nf(abs(off - 1) * 100, 2)}% [1]; compared with {nf(pct, 2)}% uncertainty [1]; correct conclusion [1] [3]')
    return Q(s + ' (a) State the range of values consistent with the result. (b) Explain whether the result agrees with the accepted value. (c) Suggest what type of error is indicated if it does not agree, and how it could be identified.',
             f'(a) {E(val - dv)} to {E(val + dv)} {u} (b) ' + ('yes, accepted value is in the range' if ok else 'no, accepted value is outside the range') + ' (c) a systematic error (e.g. zero error or heat loss); check instruments for zero error, or look for a non-zero intercept on a graph',
             f'(a) range [1] (b) correct comparison and conclusion [1] (c) systematic error [1]; method of identifying it [1] [4]', 'multi_step')


@t164.add('C2', (2, 3, 4), 'explain')
def t164_risk(r, D):
    p = r.choice(PLANS)
    return Q(f'An experiment is planned to investigate {p["q"]}. Identify a hazard in this experiment and state a precaution to reduce the risk.', cap(p['safety']) + '.',
             'relevant hazard identified [1]; appropriate precaution [1]' + ('; precaution linked to how it reduces the risk [1] [3]' if D >= 3 else ' [2]'))


@t164.add('C2', (2, 3, 4), 'explain')
def t164_improve(r, D):
    prob, fix = r.choice([('the time for a ball to fall through oil between two marks is measured with a hand-held stopwatch, giving times of about 1.2 s', 'Reaction-time error is a large fraction of 1.2 s; use light gates connected to a timer, or a longer distance between the marks.'),
                          ('the temperature of a thermistor is measured with a thermometer some distance away in an unstirred water bath', 'The water temperature is not uniform; stir the bath and place the thermometer next to the thermistor, waiting for thermal equilibrium.'),
                          ('the count rate from a weak radioactive source is measured for only 10 s at each thickness', 'Random fluctuations are large for small counts; count for longer (e.g. several minutes) and repeat.'),
                          ('a pendulum amplitude is read from a scale while the student stands at one side', 'Parallax error; view the scale at eye level directly in front, or video the motion against the scale.'),
                          ('the current in a circuit is read from an ammeter that shows 0.02 A with no current flowing', 'Zero error (systematic): subtract 0.02 A from all readings or zero the meter.'),
                          ('only four values of the separation of two magnets are used, all between 2 cm and 3 cm', 'Too few readings over too small a range; use at least six values spread over a wide range.')])
    return Q(f'In an investigation, {prob}. Explain why this reduces the reliability or accuracy of the results and suggest an improvement.', fix,
             'identifies the problem [1]; workable improvement [1]' + ('; explains how the improvement reduces the uncertainty [1] [3]' if D >= 3 else ' [2]'))


def _eval_c4(r, D):
    g1 = r.choice([2.14, 2.20, 2.31]); g2 = r.choice([2.02, 2.36])
    th = r.choice([2.00, 2.25])
    intro = f'A student tests the prediction that the gradient of a graph should equal {nf(th, 3)}. The best-fit gradient is {nf(g1, 3)} and the worst acceptable gradient is {nf(g2, 3)}.'
    u = abs(g2 - g1); ok = abs(g1 - th) <= u
    parts = [
        lambda r: ('Calculate the absolute uncertainty in the gradient.', f'{nf(u, 2)}', '|difference| [1]'),
        lambda r: ('State whether the result supports the prediction, explaining your answer.', ('Yes' if ok else 'No') + f': the predicted value is {"within" if ok else "outside"} {nf(g1, 3)} ± {nf(u, 2)}.', 'comparison with range [1]; conclusion [1] [2]'),
        lambda r: ('Suggest one source of systematic error that could cause the gradient to differ from the prediction.', 'e.g. zero error in a meter, heat loss, timing that always starts late, wrong calibration.', 'plausible systematic error [1]'),
        lambda r: ('Suggest how the reliability of the result could be improved.', 'Repeat readings and average, use a wider range of values, use instruments with better resolution.', 'first improvement [1]; second improvement [1] [2]'),
        lambda r: ('Explain why a straight line not passing through the origin may still support a linear relationship.', 'It shows y = mx + c with a constant offset, perhaps from a systematic error; the gradient may still be valid.', 'linear with offset / systematic error [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t164.add('C4', (2, 3, 4, 5), 'multi_step')(_eval_c4)
CHAPTERS[16] = [t161, t162, t163, t164]
