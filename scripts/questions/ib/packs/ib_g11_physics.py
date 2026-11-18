"""IB DP Physics SL/HL (first assessment 2025), DP year 1 – ib-g11-physics.

Theme A (space, time and motion: kinematics, forces and momentum, work/energy/power, rigid bodies HL,
relativity HL), theme B (the particulate nature of matter: thermal energy transfers, greenhouse effect,
gas laws, thermodynamics HL, current and circuits) and C.1–C.2 (simple harmonic motion, wave model).

Numerical items are parametric and compute their answers with IB data-booklet constants
(g = 9.81 m s⁻², k_B = 1.38 × 10⁻²³ J K⁻¹, R = 8.31 J K⁻¹ mol⁻¹, N_A = 6.02 × 10²³ mol⁻¹,
σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴, c = 3.00 × 10⁸ m s⁻¹, e = 1.60 × 10⁻¹⁹ C, …), to 3 significant figures
unless the data justify fewer. Shared helpers live in ib_physics_common.py.

Mock = HL Paper 1 (1A: 40 MCQ, 1B: data-based questions on experimental work, 60 marks) +
Paper 2 (structured and extended response, 90 marks): 52 items, 150 marks.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
import ib_physics_common as pc
from ib_physics_common import (MOCK, g0, G, K, E, H, C, ME, MP, U, NA, KB, RGAS, SIGMA, WIEN, M_EARTH, R_EARTH,  # noqa: F401
                               R_SUN, L_SUN, AU, sf, q, deg, sind, cosd, asind, nmcq, num, pick, lc_topic)

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

R = Registry()
_base_templates = pc.make_templates(R)
_T11: dict = {}


def _combo(st, tpls):
    """C4 structured question: a calculation, an explanation and an evaluation, all from this subtopic."""
    key = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
    nums = [t for t in tpls if t.type == 'numerical' and t.style is None and 'C3' in (t.c if isinstance(t.c, tuple) else (t.c,))]
    exps = [t for t in tpls if t.name in ('why', 'contrast')]
    f = R.f.get(key)
    topic = lc_topic(st['name'])
    short = topic.split(':')[0].split(';')[0].strip()

    def fn(rng, slot):
        if not nums or not exps or f is None or not f.evaluate:
            return None
        sub = pc.Slot(slot.subtopic, slot.chapter, 'C3', max(2, min(5, slot.d)), set='part')
        p1 = rng.choice(nums).fn(rng, sub)
        p2 = rng.choice(exps).fn(rng, pc.Slot(slot.subtopic, slot.chapter, 'C2', 3, set='part'))
        if not p1 or not p2:
            return None
        claim, pro, con, judge = rng.choice(f.evaluate)
        m1, m2 = p1.get('marks', 2), p2.get('marks', 3)
        m3 = 4 if slot.d <= 4 else 6
        ask = rng.choice([f'Evaluate the claim: "{claim}"', f'"{claim}" Discuss this view, referring to the physics of {short}.',
                          f'Outline one argument for and one against the statement: "{claim}"'])
        stem = (f'This question is about {topic}.\n\n(a) {pc._roman(p1["stem"])} [{m1}]\n\n(b) {pc._roman(p2["stem"])} [{m2}]\n\n(c) {ask} [{m3}]')
        ans = f'(a) {pc._roman(str(p1["answer"]))} (b) {pc._roman(str(p2["answer"]))} (c) {judge}'
        mk = (f'(a) [{m1} marks] {pc._roman(p1["markingKey"])} (b) [{m2} marks] {pc._roman(p2["answer"])} '
              f'(c) [{m3} marks] For: {"; ".join(pro)}. Against: {"; ".join(con)}. Award the final mark(s) for a judgement supported by the arguments: {judge}')
        return dict(stem=stem, answer=ans, markingKey=mk, type='multi_step', marks=m1 + m2 + m3, gap='G5')
    return fn


def templates(st):
    if st['id'] in _T11:
        return _T11[st['id']]
    out = list(_base_templates(st))
    out.append(T('C4', (2, 5), _combo(st, out), 'multi_step', None, 'c4_combo'))
    _T11[st['id']] = out
    return out


def init(subject_id):
    pass


def repeat_readings(*a, **k):
    pc.repeat_readings(R, *a, **k)


def linearise(*a, **k):
    pc.linearise(R, *a, **k)


def gradient_fit(*a, **k):
    pc.gradient_fit(R, *a, **k)


def add_f(key, **kw):
    pc.add_f(R, key, **kw)


def prob(key, d=(1, 4), md=(1, 4), c='C3', marks=2, mcq_too=True):
    """Register a numerical problem twice: as a structured numerical item and as a numeric MCQ.

    fn(rng, slot) -> dict(stem, v, unit, wrongs, key[, n, ans, marks]) or None.
    """
    def deco(fn):
        def numf(rng, slot):
            p = fn(rng, slot)
            if not p:
                return None
            return num(p['stem'], p.get('ans') or q(p['v'], p['unit'], p.get('n', 3)), p['key'], p.get('marks', marks))

        def mcqf(rng, slot):
            p = fn(rng, slot)
            if not p or p.get('v') is None:
                return None
            return nmcq(rng, p.get('mstem', p['stem']), p['v'], p['wrongs'], p['unit'], p['key'], p.get('n', 3))
        R.t.setdefault(key, []).append(T(c, d, numf, 'numerical', None, fn.__name__))
        if mcq_too:
            R.t.setdefault(key, []).append(T(c, md, mcqf, 'mcq', None, fn.__name__ + '_mcq'))
        return fn
    return deco


def who_city(rng):
    return name(rng), rng.choice(CITIES)


def r2(lo, hi, rng, n=2):
    return float(f'{rng.uniform(lo, hi):.{n}g}')


# =============================================================================================
# ch01 A.1 Kinematics
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('displacement', 'the change in position of an object, a vector with magnitude and direction measured from the starting point'),
           ('distance', 'the total length of path travelled, a scalar quantity'),
           ('average velocity', 'the total displacement divided by the total time taken'),
           ('instantaneous velocity', 'the rate of change of displacement at a particular instant, the gradient of the displacement–time graph at that time'),
           ('acceleration', 'the rate of change of velocity, a vector quantity'),
           ('speed', 'the rate of change of distance travelled, a scalar quantity')],
    facts=[('Which of the following is a vector quantity?', 'Displacement', ['Distance', 'Speed', 'Time'], 'Displacement has both magnitude and direction.'),
           ('A runner completes exactly one lap of a 400 m track in 80 s. What is her average velocity for the lap?', '0 m s⁻¹', ['5.0 m s⁻¹', '2.5 m s⁻¹', '10 m s⁻¹'], 'The displacement after one full lap is zero.'),
           ('Which quantity is given by the gradient of a displacement–time graph?', 'Velocity', ['Acceleration', 'Distance', 'Displacement'], 'v = Δs/Δt.'),
           ('An object moving in a circle at constant speed has', 'a changing velocity and a non-zero acceleration', ['a constant velocity', 'zero acceleration', 'a constant displacement'], 'The direction of the velocity changes continuously.'),
           ('Which of the following can be negative?', 'Velocity', ['Speed', 'Distance travelled', 'Time interval'], 'Velocity is a vector; its sign shows direction along a line.'),
           ('What is the SI unit of acceleration?', 'm s⁻²', ['m s⁻¹', 'N kg', 'm² s⁻¹'], 'Acceleration is change in velocity (m s⁻¹) per second.')],
    why=[('Explain why an object can have a speed but zero average velocity over a journey.', 'Average velocity is total displacement / time; if the object returns to its starting point the displacement is zero, although distance and hence average speed are not zero.'),
         ('Explain why the speedometer reading of a car is an instantaneous speed, not an average speed.', 'The speedometer measures the rate of distance covered over a very short time interval, so it gives the speed at that instant; average speed is total distance over a whole journey.'),
         ('Explain how an object can be accelerating even though its speed is constant.', 'Acceleration is the rate of change of velocity; if the direction of motion changes (e.g. circular motion) the velocity changes, so there is acceleration even at constant speed.'),
         ('Explain why a negative acceleration does not always mean the object is slowing down.', 'The sign gives the direction of the acceleration relative to the chosen positive direction; if the velocity is also negative, a negative acceleration makes the object speed up.')],
    contrast=[('distance', 'displacement', 'Distance is the scalar length of the path travelled; displacement is the vector change in position from start to finish, which can be smaller than the distance or zero.'),
              ('average velocity', 'instantaneous velocity', 'Average velocity is total displacement over total time for an interval; instantaneous velocity is the velocity at one moment, the gradient of the s–t graph at that point.')],
    misc=[('If the velocity of an object is zero, its acceleration must be zero.', 'A ball thrown upwards has zero velocity at the top but its acceleration is still g downwards; velocity and acceleration are independent.'),
          ('A larger velocity always means a larger acceleration.', 'Acceleration depends on how quickly the velocity changes, not on its size; a car cruising at 30 m s⁻¹ has zero acceleration.'),
          ('Average speed is always the average of the initial and final speeds.', 'That is only true for uniform acceleration; in general average speed = total distance / total time.'),
          ('Speed and velocity are the same quantity with different names.', 'Speed is a scalar (magnitude only); velocity is a vector with direction, so two objects with the same speed can have different velocities.')],
    evaluate=[('GPS speed readings are always more reliable than measuring speed with a stopwatch and tape measure.', ['GPS avoids human reaction-time errors', 'it updates continuously and gives instantaneous values'], ['GPS position has uncertainties of several metres, which matter over short distances', 'signal loss in tunnels or between buildings gives gaps', 'light gates and data loggers give better precision in a lab'], 'GPS is excellent for long journeys, but for short, precise lab measurements light gates or video analysis are more reliable; reliability depends on the scale of the measurement.')],
    extended=[('A ferry crosses a river 240 m wide, heading straight across at 3.0 m s⁻¹ relative to the water. The river flows at 1.2 m s⁻¹. (a) Calculate the time to cross. (b) Determine the resultant velocity of the ferry relative to the bank. (c) Calculate how far downstream it lands. (d) State the heading needed to land directly opposite.', '(a) t = 240/3.0 = 80 s; (b) √(3.0² + 1.2²) = 3.23 m s⁻¹ at 21.8° to the line straight across; (c) 1.2 × 80 = 96 m; (d) aim upstream at sin⁻¹(1.2/3.0) = 23.6° to the straight-across line.', 6)],
))


@prob('ch01-st1', d=(1, 4), md=(1, 4))
def p_two_legs(rng, slot):
    a = rng.choice([300, 400, 450, 600, 800, 1200])
    b = rng.choice([200, 250, 500, 700, 900])
    va = r2(1.2, 2.0, rng)
    vb = r2(1.0, 1.8, rng)
    t = a / va + b / vb
    disp = math.hypot(a, b)
    who, city = who_city(rng)
    k = rng.randrange(3)
    if k == 0:
        stem = f'{who} walks {a} m east at {va} m s⁻¹ and then {b} m north at {vb} m s⁻¹ through a park in {city}. Determine the magnitude of the average velocity for the whole walk.'
        return dict(stem=stem, v=disp / t, unit='m s⁻¹', wrongs=[(a + b) / t, disp / (a / va), (va + vb) / 2],
                    key=f'Displacement = √({a}² + {b}²) = {sf(disp)} m (M1); time = {a}/{va} + {b}/{vb} = {sf(t)} s (M1); average velocity = {sf(disp / t)} m s⁻¹ (A1).', marks=3)
    if k == 1:
        stem = f'A delivery drone in {city} flies {a} m due east and then {b} m due north in a total time of {sf(t, 3)} s. Calculate its average speed.'
        return dict(stem=stem, v=(a + b) / t, unit='m s⁻¹', wrongs=[disp / t, (a - b) / t if a != b else None, (a + b) / t * 2],
                    key=f'Average speed = total distance / time = {a + b}/{sf(t, 3)} (M1) = {sf((a + b) / t)} m s⁻¹ (A1).')
    stem = f'An orienteer in {city} runs {a} m east and then {b} m north. Calculate the angle of her displacement measured north of east.'
    ang = math.degrees(math.atan2(b, a))
    return dict(stem=stem, v=ang, unit='°', ans=deg(ang), wrongs=[90 - ang, math.degrees(math.atan2(a, b)) + 3, math.degrees(math.asin(min(1, b / (a + b))))],
                key=f'tan θ = {b}/{a} (M1); θ = {deg(ang)} north of east (A1).')


@prob('ch01-st1', d=(1, 3), md=(1, 3))
def p_avg_speed_trip(rng, slot):
    d1 = rng.choice([20, 30, 40, 60]); v1 = rng.choice([60, 80, 90, 100])
    d2 = rng.choice([10, 15, 25, 30]); v2 = rng.choice([30, 40, 50])
    t = d1 / v1 + d2 / v2
    who, city = who_city(rng)
    stem = rng.choice([f'{who} drives {d1} km on a motorway near {city} at {v1} km h⁻¹ and then {d2} km through town at {v2} km h⁻¹. Calculate the average speed for the journey.',
                       f'A bus from {city} travels the first {d1} km of its route at {v1} km h⁻¹ and the remaining {d2} km at {v2} km h⁻¹. Determine its average speed.'])
    return dict(stem=stem, v=(d1 + d2) / t, unit='km h⁻¹', wrongs=[(v1 + v2) / 2, (d1 * v1 + d2 * v2) / (d1 + d2), (d1 + d2) / t * 1.1],
                key=f'Total time = {d1}/{v1} + {d2}/{v2} = {sf(t)} h (M1); average speed = {d1 + d2}/{sf(t)} = {sf((d1 + d2) / t)} km h⁻¹ (A1). Not the mean of the two speeds.')


@prob('ch01-st1', d=(2, 4), md=(2, 4))
def p_vel_change(rng, slot):
    v1 = rng.choice([8, 10, 12, 15]); v2 = rng.choice([6, 8, 10, 12])
    t = rng.choice([0.5, 1.5, 2.0, 2.5, 4.0])
    k = rng.randrange(2)
    if k == 0:
        stem = f'A tennis ball hits a wall at {v1} m s⁻¹ and rebounds along the same line at {v2} m s⁻¹. The contact lasts {sf(t / 50, 2)} s. Calculate the magnitude of the average acceleration during the contact.'
        a = (v1 + v2) / (t / 50)
        return dict(stem=stem, v=a, unit='m s⁻²', wrongs=[(v1 - v2) / (t / 50) if v1 != v2 else None, v1 / (t / 50), (v1 + v2) * (t / 50)],
                    key=f'Δv = {v2} − (−{v1}) = {v1 + v2} m s⁻¹ (M1, direction change); a = Δv/Δt = {sf(a)} m s⁻² (A1).')
    stem = f'A cyclist travelling north at {v1} m s⁻¹ turns and is travelling east at {v2} m s⁻¹ {t} s later. Calculate the magnitude of the average acceleration.'
    a = math.hypot(v1, v2) / t
    return dict(stem=stem, v=a, unit='m s⁻²', wrongs=[abs(v1 - v2) / t if v1 != v2 else (v1 + v2) / t * 0.5, (v1 + v2) / t, math.hypot(v1, v2) * t],
                key=f'Δv = √({v1}² + {v2}²) = {sf(math.hypot(v1, v2))} m s⁻¹ (vector subtraction) (M1); a = {sf(a)} m s⁻² (A1).')


R.mcqs('ch01-st1', 'C2', (1, 4), [
    ('A ball is thrown vertically upwards and caught at the same height. Which statement about the whole flight is correct?', 'The average velocity is zero but the average speed is not', ['Both average velocity and average speed are zero', 'The average speed is zero but the average velocity is not', 'The average velocity equals the average speed'], 'Displacement is zero; distance is not.'),
    ('A car travels round a roundabout at a constant speed of 8 m s⁻¹. Which is true?', 'Its velocity changes continuously', ['Its velocity is constant', 'Its acceleration is zero', 'Its displacement is constant'], 'Direction changes so velocity changes.'),
    ('An object moving in the negative direction has a positive acceleration. The object is', 'slowing down', ['speeding up', 'moving at constant speed', 'stationary'], 'Acceleration opposite to velocity reduces the speed.'),
    ('The magnitude of the average velocity over an interval is', 'less than or equal to the average speed', ['always equal to the average speed', 'always greater than the average speed', 'unrelated to the average speed'], 'Displacement magnitude ≤ distance.'),
])

repeat_readings('ch01-st1', 'the time for a trolley to pass between two light gates 0.500 m apart', 's', 0.62, 0.70, 3,
                ['released a trolley from the same point on a ramp each time.', 'timed a dynamics trolley between two light gates.'])


R.facts('ch01-st2', F(
    terms=[('uniform acceleration', 'acceleration that is constant in both magnitude and direction'),
           ('free fall', 'motion under the influence of gravity alone, with acceleration g = 9.81 m s⁻² near Earth’s surface'),
           ('reaction time', 'the time between a stimulus and the start of a response, during which a driver travels at constant speed'),
           ('stopping distance', 'the sum of the thinking distance (during the reaction time) and the braking distance'),
           ('initial velocity', 'the velocity u at the start of the time interval considered')],
    facts=[('Which equation does NOT involve the time taken?', 'v² = u² + 2as', ['v = u + at', 's = ut + ½at²', 's = ½(u + v)t'], 'v² = u² + 2as eliminates t.'),
           ('The suvat equations are valid only when', 'the acceleration is constant', ['the velocity is constant', 'the object starts from rest', 'the motion is vertical'], 'They are derived assuming uniform acceleration.'),
           ('A stone is dropped from rest. Ignoring air resistance, how far does it fall in the first 2.0 s?', '19.6 m', ['9.81 m', '39.2 m', '4.9 m'], 's = ½ × 9.81 × 2.0² = 19.6 m.'),
           ('A car doubles its speed. By what factor does its braking distance change for the same braking force?', '4', ['2', '√2', '8'], 's = v²/(2a) ∝ v².'),
           ('What is the velocity of a ball thrown upwards at the highest point of its flight?', 'Zero', ['g upwards', 'Equal to its initial speed', 'g downwards'], 'It momentarily stops before falling.')],
    why=[('Explain why the thinking distance of a driver is proportional to speed while the braking distance is proportional to the square of the speed.', 'During the reaction time the car moves at constant speed, so distance = v × t_r ∝ v; while braking at constant deceleration v² = 2as, so s = v²/(2a) ∝ v².'),
         ('Explain why a heavy and a light ball dropped together from the same height land at the same time when air resistance is negligible.', 'Both experience the same gravitational acceleration g, independent of mass (the larger weight acts on a proportionally larger mass), so their motions are identical.'),
         ('Explain why the suvat equations cannot be used to find the time for a skydiver to reach terminal velocity.', 'Air resistance increases with speed, so the resultant force and hence the acceleration decrease continuously; suvat equations require constant acceleration.')],
    contrast=[('thinking distance', 'braking distance', 'Thinking distance is covered at constant speed during the reaction time (∝ v); braking distance is covered while decelerating to rest (∝ v² for a constant braking force).')],
    misc=[('A ball thrown upwards has zero acceleration at its highest point.', 'Its velocity is zero there, but gravity still acts, so the acceleration is 9.81 m s⁻² downwards throughout the flight.'),
          ('Heavier objects fall faster in a vacuum.', 'In a vacuum all objects have the same acceleration g; differences in everyday falls come from air resistance.'),
          ('The equation s = ut + ½at² can be used for any motion.', 'It requires constant acceleration; for varying acceleration you must use graphs or calculus.')],
    evaluate=[('Lowering speed limits in cities from 50 km h⁻¹ to 30 km h⁻¹ is justified by physics alone.', ['braking distance ∝ v², so stopping distance falls by more than half', 'kinetic energy at impact ∝ v², reducing injury'], ['journey times increase', 'economic and social factors (traffic flow, compliance) also matter', 'emissions can rise at low gears'], 'Physics gives a strong safety case (stopping distance and impact energy fall sharply), but the decision also weighs social, economic and environmental factors.')],
    extended=[('A car travelling at 25 m s⁻¹ approaches traffic lights. The driver has a reaction time of 0.70 s and the brakes give a deceleration of 6.5 m s⁻². (a) Calculate the thinking distance. (b) Calculate the braking distance. (c) The lights are 70 m away when the driver sees them change. Determine whether the car stops in time. (d) Discuss two factors that would change your answer.', '(a) 17.5 m; (b) 25²/(2 × 6.5) = 48.1 m; (c) total 65.6 m < 70 m, so it stops with 4.4 m to spare; (d) wet road reduces deceleration; tiredness or phone use increases reaction time; worn tyres/brakes.', 6)],
))


@prob('ch01-st2', d=(1, 5), md=(1, 4))
def p_suvat(rng, slot):
    k = rng.randrange(6)
    who, city = who_city(rng)
    if k == 0:
        u = rng.choice([12, 15, 18, 20, 22, 25, 28, 31]); a = r2(4.5, 8.0, rng)
        s = u * u / (2 * a)
        return dict(stem=f'A car in {city} travelling at {u} m s⁻¹ brakes with a uniform deceleration of {a} m s⁻². Calculate the distance it travels before stopping.',
                    v=s, unit='m', wrongs=[u * u / a, u / a, u * u * a / 2 / 10], key=f'v² = u² + 2as with v = 0 (M1); s = {u}²/(2 × {a}) = {sf(s)} m (A1).')
    if k == 1:
        a = r2(2.0, 4.5, rng); t = rng.choice([3.0, 4.0, 5.0, 6.0, 8.0])
        s = 0.5 * a * t * t
        return dict(stem=f'{who}, a sprinter, accelerates uniformly from rest at {a} m s⁻² for {t} s. Calculate the distance covered in this time.',
                    v=s, unit='m', wrongs=[a * t * t, a * t, 0.5 * a * t], key=f's = ut + ½at² with u = 0 (M1); s = ½ × {a} × {t}² = {sf(s)} m (A1).')
    if k == 2:
        u = rng.choice([8.0, 10.0, 12.0, 14.0, 15.0, 18.0])
        hmax = u * u / (2 * g0)
        return dict(stem=f'A volleyball is hit vertically upwards at {u} m s⁻¹ in a sports hall in {city}. Ignoring air resistance, calculate the maximum height it rises above the point where it was hit.',
                    v=hmax, unit='m', wrongs=[u * u / g0, u / g0, u * u / (2 * 9.81) * 2], key=f'At the top v = 0 (M1); h = u²/(2g) = {u}²/(2 × 9.81) = {sf(hmax)} m (A1).')
    if k == 3:
        h = rng.choice([15, 20, 25, 30, 45, 60])
        t = math.sqrt(2 * h / g0)
        return dict(stem=f'A stone is dropped from rest from a bridge {h} m above a river near {city}. Calculate the time taken to reach the water, ignoring air resistance.',
                    v=t, unit='s', wrongs=[2 * h / g0, math.sqrt(h / g0), h / g0], key=f'h = ½gt² (M1); t = √(2 × {h}/9.81) = {sf(t)} s (A1).')
    if k == 4:
        u = rng.choice([4, 6, 8, 10]); v = rng.choice([20, 24, 28, 32]); t = rng.choice([5, 8, 10, 12])
        s = 0.5 * (u + v) * t
        return dict(stem=f'A train leaving a station in {city} speeds up uniformly from {u} m s⁻¹ to {v} m s⁻¹ in {t} s. Calculate the distance it travels during this time.',
                    v=s, unit='m', wrongs=[v * t, (v - u) * t, 0.5 * (v - u) * t], key=f's = ½(u + v)t (M1) = ½({u} + {v}) × {t} = {sf(s)} m (A1).')
    u = rng.choice([10.0, 12.0, 15.0, 18.0]); h = rng.choice([20, 30, 40, 50])
    vimp = math.sqrt(u * u + 2 * g0 * h)
    return dict(stem=f'A ball is thrown vertically downwards at {u} m s⁻¹ from the roof of a building {h} m high. Calculate its speed just before it hits the ground, ignoring air resistance.',
                v=vimp, unit='m s⁻¹', wrongs=[math.sqrt(2 * g0 * h), u + math.sqrt(2 * g0 * h), math.sqrt(u * u + g0 * h)], key=f'v² = u² + 2gh = {u}² + 2 × 9.81 × {h} (M1); v = {sf(vimp)} m s⁻¹ (A1).')


@prob('ch01-st2', d=(2, 5), md=(2, 4), marks=3)
def p_stopping(rng, slot):
    v = rng.choice([13.9, 16.7, 22.2, 27.8, 31.3]); kmh = round(v * 3.6)
    tr = rng.choice([0.6, 0.7, 0.8, 1.0, 1.2]); a = r2(5.5, 7.5, rng)
    st = v * tr + v * v / (2 * a)
    who, city = who_city(rng)
    k = rng.randrange(2)
    if k == 0:
        stem = f'{who} drives at {kmh} km h⁻¹ on a dry road in {city}. Her reaction time is {tr} s and the car can decelerate at {a} m s⁻². Calculate the total stopping distance.'
    else:
        stem = f'A safety poster in {city} assumes a reaction time of {tr} s and a braking deceleration of {a} m s⁻². Determine the stopping distance it should quote for a car moving at {kmh} km h⁻¹.'
    return dict(stem=stem, v=st, unit='m', wrongs=[v * v / (2 * a), v * tr, kmh * tr + kmh ** 2 / (2 * a) / 10],
                key=f'v = {kmh}/3.6 = {sf(v)} m s⁻¹ (M1); thinking distance = {sf(v * tr)} m (A1); braking distance = v²/(2a) = {sf(v * v / (2 * a))} m (A1); total = {sf(st)} m.')


@prob('ch01-st2', d=(3, 5), md=(3, 4), marks=3)
def p_two_stage(rng, slot):
    a = rng.choice([1.2, 1.5, 2.0, 2.5]); t1 = rng.choice([8, 10, 12, 15]); t2 = rng.choice([20, 30, 40])
    v = a * t1; s = 0.5 * a * t1 * t1 + v * t2
    city = rng.choice(CITIES)
    stem = rng.choice([f'A metro train in {city} accelerates from rest at {a} m s⁻² for {t1} s and then travels at constant speed for {t2} s. Calculate the total distance travelled.',
                       f'An electric bus starts from rest, accelerates at {a} m s⁻² for {t1} s, then cruises at the speed reached for a further {t2} s. Determine how far it has gone.'])
    return dict(stem=stem, v=s, unit='m', wrongs=[0.5 * a * t1 * t1 + 0.5 * v * t2, v * (t1 + t2), 0.5 * a * (t1 + t2) ** 2],
                key=f'Speed reached v = at = {sf(v)} m s⁻¹ (M1); s₁ = ½at² = {sf(0.5 * a * t1 * t1)} m (A1); s₂ = vt = {sf(v * t2)} m; total = {sf(s)} m (A1).')


@R.add('ch01-st2', 'C4', (3, 5), 'multi_step')
def c4_overtake(rng, slot):
    k = rng.randrange(3)
    if k == 0:
        vp = rng.choice([12, 14, 15]); a = rng.choice([2.0, 2.5, 3.0])
        t = 2 * vp / a
        return num(f'A police car starts from rest at the moment a speeding car passes it at a constant {vp} m s⁻¹. The police car accelerates uniformly at {a} m s⁻². (a) Determine the time taken for the police car to catch the speeding car. (b) Calculate the distance travelled by then. (c) Calculate the speed of the police car at that moment and comment on whether the model is realistic.',
                   f'(a) {sf(t)} s; (b) {sf(vp * t)} m; (c) {sf(a * t)} m s⁻¹ (= 2 × {vp}); a real car cannot keep accelerating uniformly to high speed and must slow to match speed.',
                   f'(a) Equal displacements: {vp}t = ½({a})t² (M1); t = 2 × {vp}/{a} = {sf(t)} s (A1). (b) s = {vp} × {sf(t)} = {sf(vp * t)} m (A1). (c) v = at = {sf(a * t)} m s⁻¹ (A1); comment on limits of uniform acceleration (R1).', 5, 'multi_step')
    if k == 1:
        u = rng.choice([15.0, 18.0, 20.0, 24.0]); h = rng.choice([25, 30, 40])
        tt = (u + math.sqrt(u * u + 2 * g0 * h)) / g0
        return num(f'A ball is thrown vertically upwards at {u} m s⁻¹ from the edge of a cliff {h} m above the sea. Ignore air resistance. (a) Calculate the maximum height above the sea. (b) Determine the total time until it hits the sea. (c) Sketch the velocity–time graph for the motion, taking upwards as positive, and state its gradient.',
                   f'(a) {sf(h + u * u / (2 * g0))} m; (b) {sf(tt)} s; (c) straight line from +{u} m s⁻¹ crossing zero at {sf(u / g0)} s, gradient −9.81 m s⁻².',
                   f'(a) h = {h} + u²/2g (M1) = {sf(h + u * u / (2 * g0))} m (A1). (b) −{h} = {u}t − 4.905t² (M1); t = {sf(tt)} s (A1). (c) straight line, negative constant gradient −g (A1).', 5, 'multi_step')
    v = rng.choice([20, 25, 30]); tr = rng.choice([0.8, 1.0, 1.5]); a1 = 7.0; a2 = rng.choice([3.5, 4.0, 4.5])
    s1 = v * tr + v * v / (2 * a1); s2 = v * tr + v * v / (2 * a2)
    return num(f'A road-safety study compares stopping on dry and icy roads at {v} m s⁻¹ with a reaction time of {tr} s. The deceleration is 7.0 m s⁻² when dry and {a2} m s⁻² when icy. (a) Calculate the stopping distance on each surface. (b) Determine the percentage increase on ice. (c) Explain why the thinking distance is unchanged. (d) Evaluate the advice "double your following distance in winter".',
               f'(a) dry {sf(s1)} m, icy {sf(s2)} m; (b) {sf(100 * (s2 - s1) / s1, 2)} %; (c) the reaction time and the speed are unchanged; (d) roughly consistent, but the braking part can more than double, so on ice even larger gaps or lower speed may be needed.',
               f'(a) thinking distance {sf(v * tr)} m (A1); braking distances {sf(v * v / 14)} m and {sf(v * v / (2 * a2))} m (M1 A1). (b) percentage (A1). (c) R1. (d) judgement linked to calculation (R1).', 6, 'multi_step')


R.mcqs('ch01-st2', 'C2', (1, 4), [
    ('A ball is thrown upwards. Taking upwards as positive, which describes its acceleration during the whole flight?', 'Constant and negative', ['Positive going up, negative coming down', 'Zero at the top, negative elsewhere', 'Decreasing to zero then increasing'], 'Only gravity acts, so a = −g throughout.'),
    ('Two cars brake with equal deceleration. Car X is moving twice as fast as car Y. The ratio of braking distances X : Y is', '4 : 1', ['2 : 1', '1 : 1', '8 : 1'], 's ∝ u².'),
    ('An object falls from rest. The distances fallen in successive equal time intervals are in the ratio', '1 : 3 : 5 : 7', ['1 : 2 : 3 : 4', '1 : 4 : 9 : 16', '1 : 1 : 1 : 1'], 'Cumulative distances go as 1 : 4 : 9 : 16; differences are odd numbers.'),
])


def _ramp_spec(rng):
    a = rng.uniform(0.35, 0.80)
    ds = [0.20, 0.40, 0.60, 0.80, 1.00, 1.20]
    ts = [round(math.sqrt(2 * d_ / a) * rng.uniform(0.985, 1.015), 2) for d_ in ds]
    return dict(intro='A trolley is released from rest on an inclined ramp. The time t to travel a distance s down the ramp is measured with a light gate and a timer. Theory: s = ½at².',
                xname='s', xunit='m', yname='t', yunit='s', xs=ds, ys=ts, xfmt=lambda x: f'{x:.2f}', yfmt=lambda y: f'{y:.2f}',
                plot_x=lambda x: x, plot_y=lambda y: y * y, plot_label='t² (y) against s (x)', what='the acceleration a of the trolley', what_short='a',
                gunit='s² m⁻¹', deduce=lambda m_, b_: (2 / m_, 'm s⁻²', 'a = 2/gradient'))


gradient_fit('ch01-st2', _ramp_spec)
linearise('ch01-st2', [('s = ½at² for an object released from rest', 's', 't²', '½a', 'The line should pass through the origin.'),
                       ('v² = u² + 2as for a trolley passing a light gate', 'v²', 's', '2a', 'The intercept is u².'),
                       ('h = ½gt² for a falling ball', 'h', 't²', 'g/2', 'A non-zero intercept suggests a systematic timing error.')])


R.facts('ch01-st3', F(
    terms=[('gradient of a displacement–time graph', 'the velocity of the object'),
           ('gradient of a velocity–time graph', 'the acceleration of the object'),
           ('area under a velocity–time graph', 'the displacement of the object'),
           ('area under an acceleration–time graph', 'the change in velocity of the object'),
           ('tangent to a curve', 'a straight line touching the curve at one point, whose gradient gives the instantaneous rate of change')],
    facts=[('What does the area under a velocity–time graph represent?', 'Displacement', ['Acceleration', 'Velocity', 'Force'], 'Area = v × t.'),
           ('A displacement–time graph is a straight line with a positive gradient. The object has', 'constant positive velocity', ['constant acceleration', 'zero velocity', 'increasing velocity'], 'Constant gradient means constant velocity.'),
           ('A velocity–time graph is a horizontal line above the time axis. The acceleration is', 'zero', ['constant and positive', 'increasing', 'negative'], 'Gradient is zero.'),
           ('On a displacement–time graph, a curve getting steeper shows', 'increasing velocity', ['decreasing velocity', 'constant velocity', 'the object at rest'], 'Gradient increases.'),
           ('What does the area under an acceleration–time graph represent?', 'Change in velocity', ['Displacement', 'Distance', 'Jerk'], 'Δv = ∫a dt.')],
    why=[('Explain how the instantaneous velocity can be found from a curved displacement–time graph.', 'Draw a tangent to the curve at the required time; the gradient of the tangent (Δs/Δt) is the instantaneous velocity.'),
         ('Explain why the area between a velocity–time graph and the time axis below the axis is counted as negative displacement.', 'Below the axis the velocity is negative, i.e. in the opposite direction, so the displacement in that interval is negative; total displacement is the signed sum of areas, while distance adds magnitudes.'),
         ('Explain what the shape of the velocity–time graph of a skydiver shows before the parachute opens.', 'The gradient (acceleration) starts at g and decreases as air resistance grows with speed; the curve levels off at terminal velocity where the resultant force is zero.')],
    contrast=[('a displacement–time graph', 'a distance–time graph', 'Displacement–time graphs can go down (returning towards start, negative velocity); distance–time graphs never decrease since distance is a scalar that always accumulates.')],
    misc=[('A velocity–time graph that slopes downwards shows the object moving backwards.', 'It shows decreasing velocity (deceleration if v > 0); the object only moves backwards when v itself is negative, below the time axis.'),
          ('The point where two lines cross on a velocity–time graph is where the two objects meet.', 'It is where they have the same velocity; they meet where their displacements (areas) are equal, which needs a displacement–time graph or area comparison.'),
          ('A horizontal line on a displacement–time graph means constant velocity.', 'It means zero velocity: the position is not changing, so the object is at rest.')],
    evaluate=[('Video analysis software gives more accurate motion graphs than data loggers with motion sensors.', ['video can track 2D motion and many points at once', 'frame-by-frame analysis is cheap and widely available'], ['frame rate limits time resolution (e.g. 30 fps)', 'parallax and scaling errors affect distance', 'motion sensors sample faster and give direct readings'], 'Each has strengths: video is better for 2D and complex motion, motion sensors for fast, precise 1D data; accuracy depends on frame rate, calibration and set-up.')],
    extended=[('A lift starts from rest, accelerates uniformly at 1.5 m s⁻² for 2.0 s, moves at constant speed for 8.0 s, then decelerates uniformly to rest in 3.0 s. (a) Sketch the velocity–time graph. (b) Calculate the total height risen. (c) Sketch the acceleration–time graph. (d) Calculate the average speed.', '(a) trapezium: 0 → 3.0 m s⁻¹ in 2 s, flat for 8 s, down to 0 in 3 s; (b) 3.0 + 24 + 4.5 = 31.5 m; (c) +1.5 m s⁻² for 2 s, 0 for 8 s, −1.0 m s⁻² for 3 s; (d) 31.5/13 = 2.42 m s⁻¹.', 6)],
))


@prob('ch01-st3', d=(1, 5), md=(1, 4), marks=3)
def p_vt_area(rng, slot):
    v = rng.choice([4, 6, 8, 10, 12, 15, 20]); t1 = rng.choice([2, 3, 4, 5]); t2 = rng.choice([4, 6, 8, 10]); t3 = rng.choice([2, 3, 4, 5, 6])
    s = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    k = rng.randrange(4)
    city = rng.choice(CITIES)
    vehicle = rng.choice(['A tram', 'A cyclist', 'A lift', 'A model car', 'A runner'])
    if k == 0:
        return dict(stem=f'{vehicle} in {city} accelerates uniformly from rest to {v} m s⁻¹ in {t1} s, travels at this speed for {t2} s and then decelerates uniformly to rest in {t3} s. Using the area under the velocity–time graph, calculate the total distance travelled.',
                    v=s, unit='m', wrongs=[v * (t1 + t2 + t3), 0.5 * v * (t1 + t2 + t3), v * t2], key=f'Area = ½ × {v} × {t1} + {v} × {t2} + ½ × {v} × {t3} (M1 M1) = {sf(s)} m (A1).')
    if k == 1:
        T = t1 + t2 + t3
        return dict(stem=f'The velocity–time graph of {vehicle.lower()} is a trapezium: speed rises uniformly from 0 to {v} m s⁻¹ over {t1} s, stays constant for {t2} s and falls uniformly to 0 over {t3} s. Calculate the average speed for the whole motion.',
                    v=s / T, unit='m s⁻¹', wrongs=[v / 2, v, s / (t2 if t2 else 1)], key=f'Distance = area = {sf(s)} m (M1 A1); average speed = {sf(s)}/{T} = {sf(s / T)} m s⁻¹ (A1).')
    if k == 2:
        return dict(stem=f'{vehicle} in {city} reaches {v} m s⁻¹ from rest in {t1} s and later stops from {v} m s⁻¹ in {t3} s, both uniformly. Calculate the magnitude of the deceleration while stopping.',
                    v=v / t3, unit='m s⁻²', wrongs=[v / t1 if t1 != t3 else v / (t1 + 1), v * t3, 0.5 * v / t3], key=f'Deceleration = gradient of the v–t graph = {v}/{t3} (M1) = {sf(v / t3)} m s⁻² (A1).')
    a = rng.choice([1.5, 2.0, 2.5, 3.0]); t = rng.choice([3, 4, 5, 6])
    u = rng.choice([0, 2, 4, 5])
    return dict(stem=f'An acceleration–time graph for {vehicle.lower()} shows a constant acceleration of {a} m s⁻² for {t} s. The initial velocity is {u} m s⁻¹. Calculate the final velocity.',
                v=u + a * t, unit='m s⁻¹', wrongs=[a * t if u else a * t * 2, u + 0.5 * a * t, a / t + u], key=f'Area under a–t graph = Δv = {a} × {t} = {sf(a * t)} m s⁻¹ (M1); v = {u} + {sf(a * t)} = {sf(u + a * t)} m s⁻¹ (A1).')


@prob('ch01-st3', d=(2, 5), md=(2, 4))
def p_st_gradient(rng, slot):
    t = rng.choice([2.0, 3.0, 4.0, 5.0]); k = r2(0.4, 1.6, rng)
    v = 2 * k * t
    who = name(rng)
    frame = rng.randrange(2)
    if frame == 0:
        stem = f'The displacement of a toy car is given by s = {k}t² (s in m, t in s). {who} draws a tangent to the s–t graph at t = {t} s. Calculate the gradient of the tangent.'
    else:
        stem = f'A data logger shows that a falling cone obeys s = {k}t² for the first few seconds. Determine its instantaneous velocity at t = {t} s.'
    return dict(stem=stem, v=v, unit='m s⁻¹', wrongs=[k * t, k * t * t, k * t * t / t * 0.5 + k], key=f'v = ds/dt = 2 × {k} × {t} (M1) = {sf(v)} m s⁻¹ (A1); the average velocity {sf(k * t)} m s⁻¹ is not the instantaneous value.')


R.mcqs('ch01-st3', 'C2', (1, 4), [
    ('The velocity–time graph of an object is a straight line through the origin with positive gradient. The displacement–time graph is', 'a parabola curving upwards', ['a straight line through the origin', 'a horizontal line', 'a parabola curving downwards'], 'Constant a gives s ∝ t².'),
    ('A ball is dropped and bounces several times. Taking downwards as positive, the velocity–time graph between bounces consists of', 'parallel straight lines of gradient +g', ['horizontal lines', 'curves of decreasing gradient', 'lines of alternating gradient +g and −g'], 'Between bounces only gravity acts.'),
    ('Two objects have the same area under their velocity–time graphs over 10 s. They must have the same', 'displacement over the 10 s', ['final velocity', 'acceleration', 'maximum speed'], 'Area gives displacement.'),
    ('The gradient of a tangent to a velocity–time graph gives the', 'instantaneous acceleration', ['average acceleration', 'displacement', 'instantaneous velocity'], 'a = dv/dt.'),
])


R.facts('ch01-st4', F(
    terms=[('projectile', 'an object that, once launched, moves under the influence of gravity (and possibly fluid resistance) only'),
           ('range', 'the horizontal displacement of a projectile when it returns to its launch height or reaches the ground'),
           ('time of flight', 'the total time a projectile spends in the air'),
           ('trajectory', 'the path followed by a projectile, a parabola when air resistance is negligible'),
           ('fluid resistance (drag)', 'a force opposing the motion of an object through a fluid, increasing with speed')],
    facts=[('For a projectile with negligible air resistance, which quantity stays constant during the flight?', 'The horizontal component of velocity', ['The vertical component of velocity', 'The speed', 'The kinetic energy'], 'No horizontal force acts.'),
           ('Ignoring air resistance, which launch angle gives the maximum range on level ground?', '45°', ['30°', '60°', '90°'], 'R = u² sin 2θ / g is maximum when 2θ = 90°.'),
           ('At the highest point of its path, a projectile (no air resistance) has', 'zero vertical velocity and acceleration g downwards', ['zero velocity and zero acceleration', 'zero acceleration', 'maximum speed'], 'Horizontal velocity remains.'),
           ('Two launch angles give the same range on level ground (no drag). Which pair?', '30° and 60°', ['30° and 45°', '20° and 80°', '45° and 90°'], 'sin 2θ is the same for complementary angles.'),
           ('What is the effect of air resistance on the trajectory of a projectile?', 'Range and maximum height are reduced and the path becomes asymmetric', ['The path stays a symmetric parabola', 'Only the range is reduced', 'The range increases'], 'Drag removes energy and acts against velocity; descent is steeper.')],
    why=[('Explain why the horizontal and vertical motions of a projectile can be treated independently.', 'They are perpendicular components; the only force (gravity) acts vertically, so it changes only the vertical velocity while the horizontal velocity is unaffected.'),
         ('Explain why, with air resistance, the angle for maximum range is less than 45°.', 'Drag reduces horizontal velocity during the flight; a lower angle shortens the time in the air and keeps more horizontal velocity, so the optimum angle shifts below 45°.'),
         ('Explain why the descending part of a projectile path with drag is steeper than the ascending part.', 'Drag continuously reduces the horizontal velocity, so later in the flight the horizontal component is smaller relative to the vertical one, making the path steeper.')],
    contrast=[('the motion of a projectile with negligible air resistance', 'the motion of a projectile with significant air resistance', 'Without drag the horizontal velocity is constant and the path is a symmetric parabola; with drag both components are reduced, the range and height fall and the descent is steeper than the ascent.')],
    misc=[('A bullet fired horizontally hits the ground later than one dropped from the same height at the same instant.', 'Vertical motion is independent of horizontal motion; both start with zero vertical velocity and land at the same time (ignoring drag).'),
          ('At the top of its flight a projectile has zero velocity.', 'Only the vertical component is zero; the horizontal component u cos θ remains.'),
          ('A projectile keeps moving forward because a forward force acts on it.', 'No forward force is needed; it continues by inertia (Newton’s first law). The only force is gravity (plus drag, which opposes motion).')],
    evaluate=[('A 45° launch always gives the greatest range in sport.', ['true for level ground with negligible drag'], ['shot putters release from about 2 m above ground, so the optimum is lower', 'drag and lift on balls change the optimum', 'athletes can generate more speed at lower angles'], 'The 45° result is an idealisation; real optimum angles depend on release height, drag and biomechanics, usually 35°–42°.')],
    extended=[('A footballer kicks a ball from the ground at 22 m s⁻¹ at 35° to the horizontal towards a goal 30 m away whose crossbar is 2.44 m high. Ignore air resistance. (a) Calculate the time for the ball to travel 30 m horizontally. (b) Determine the height of the ball at the goal line. (c) State whether it goes over the bar. (d) Explain how air resistance would change the outcome.', '(a) uₓ = 18.0 m s⁻¹, t = 1.66 s; (b) u_y = 12.6 m s⁻¹, y = 12.6 × 1.66 − 4.905 × 1.66² = 7.47 m; (c) yes, well over the bar; (d) drag reduces both components so the ball takes longer to reach 30 m and is lower, possibly under the bar.', 6)],
))


@prob('ch01-st4', d=(1, 5), md=(1, 4), marks=3)
def p_horiz(rng, slot):
    h = rng.choice([1.2, 1.8, 2.5, 5.0, 12, 20, 45, 80]); u = rng.choice([3.0, 4.5, 6.0, 8.0, 12, 15, 25])
    t = math.sqrt(2 * h / g0); x = u * t
    who, city = who_city(rng)
    k = rng.randrange(3)
    if k == 0:
        stem = f'A ball rolls off a horizontal table {h} m high at {u} m s⁻¹. Ignoring air resistance, calculate the horizontal distance from the table edge to where it lands.'
        return dict(stem=stem, v=x, unit='m', wrongs=[u * 2 * h / g0, u * math.sqrt(h / g0), u * h], key=f't = √(2h/g) = {sf(t)} s (M1); x = ut = {u} × {sf(t)} (M1) = {sf(x)} m (A1).')
    if k == 1:
        stem = f'A diver in {city} runs horizontally off a cliff {h} m above the water at {u} m s⁻¹. Calculate the speed at which she enters the water.'
        vv = math.hypot(u, g0 * t)
        return dict(stem=stem, v=vv, unit='m s⁻¹', wrongs=[g0 * t, u + g0 * t, math.sqrt(u * u + g0 * h)], key=f'v_y = √(2gh) = {sf(g0 * t)} m s⁻¹ (M1); v = √(u² + v_y²) (M1) = {sf(vv)} m s⁻¹ (A1).')
    stem = f'A parcel is released from a drone flying horizontally at {u} m s⁻¹ at a height of {h} m. Calculate the time it takes to reach the ground, ignoring air resistance.'
    return dict(stem=stem, v=t, unit='s', wrongs=[2 * h / g0, h / u, math.sqrt(h / g0)], key=f'Vertical: h = ½gt² (horizontal speed irrelevant) (M1); t = {sf(t)} s (A1).', marks=2)


@prob('ch01-st4', d=(2, 5), md=(2, 4), marks=3)
def p_angled(rng, slot):
    u = rng.choice([12.0, 15.0, 18.0, 20.0, 24.0, 28.0]); th = rng.choice([25, 30, 35, 40, 50, 55, 60])
    ux, uy = u * cosd(th), u * sind(th)
    T = 2 * uy / g0
    k = rng.randrange(3)
    obj = rng.choice(['A golf ball', 'A javelin', 'A water jet from a fountain', 'A rugby ball', 'A stone from a catapult'])
    if k == 0:
        return dict(stem=f'{obj} is launched from ground level at {u} m s⁻¹ at {th}° to the horizontal. Ignoring air resistance, calculate the maximum height reached.',
                    v=uy * uy / (2 * g0), unit='m', wrongs=[u * u / (2 * g0), ux * ux / (2 * g0), uy * uy / g0], key=f'u_y = {u} sin {th}° = {sf(uy)} m s⁻¹ (M1); H = u_y²/(2g) (M1) = {sf(uy * uy / (2 * g0))} m (A1).')
    if k == 1:
        return dict(stem=f'{obj} leaves level ground at {u} m s⁻¹ at an angle of {th}° above the horizontal. Determine its range, ignoring air resistance.',
                    v=ux * T, unit='m', wrongs=[u * T, ux * T / 2, uy * T], key=f'Time of flight = 2u sin θ/g = {sf(T)} s (M1); R = u cos θ × t (M1) = {sf(ux * T)} m (A1).')
    return dict(stem=f'{obj} is projected at {u} m s⁻¹ at {th}° above the horizontal from level ground. Calculate the time of flight, ignoring air resistance.',
                v=T, unit='s', wrongs=[uy / g0, 2 * ux / g0, 2 * u / g0], key=f'u_y = {sf(uy)} m s⁻¹ (M1); T = 2u_y/g = {sf(T)} s (A1).', marks=2)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def c4_projectile(rng, slot):
    k = rng.randrange(3)
    if k == 0:
        u = rng.choice([13.0, 14.0, 15.0]); h = 2.1; th = rng.choice([38, 40, 42])
        ux, uy = u * cosd(th), u * sind(th)
        t = (uy + math.sqrt(uy * uy + 2 * g0 * h)) / g0
        return num(f'A shot putter releases the shot at {u} m s⁻¹ at {th}° above the horizontal from a height of {h} m. Ignore air resistance. (a) Calculate the horizontal and vertical components of the initial velocity. (b) Determine the time of flight. (c) Calculate the horizontal distance thrown. (d) Explain why the optimum release angle for the shot put is less than 45°.',
                   f'(a) {sf(ux)} m s⁻¹, {sf(uy)} m s⁻¹; (b) {sf(t)} s; (c) {sf(ux * t)} m; (d) the release point is above the landing point, so a lower angle (and the athlete’s ability to throw faster at low angles) maximises range.',
                   f'(a) components (A1). (b) −{h} = u_y t − ½gt² (M1), t = {sf(t)} s (A1). (c) x = {sf(ux * t)} m (A1). (d) release height above ground lowers optimum angle (R1).', 5, 'multi_step')
    if k == 1:
        x = rng.choice([18, 20, 24]); h = rng.choice([3.0, 4.0, 5.0]); th = 45
        # speed so that it lands on a target x away and h above
        u2 = g0 * x * x / (2 * cosd(th) ** 2 * (x * math.tan(math.radians(th)) - h))
        if u2 <= 0:
            return None
        u = math.sqrt(u2)
        return num(f'A firefighter aims a water jet at 45° above the horizontal at a window {x} m away horizontally and {h} m above the nozzle. Ignore air resistance. (a) Show that the launch speed needed is about {sf(u, 2)} m s⁻¹. (b) Calculate the time for the water to reach the window. (c) Determine whether the water is rising or falling as it reaches the window. (d) Suggest how air resistance would affect the speed needed.',
                   f'(a) u = {sf(u)} m s⁻¹; (b) t = {sf(x / (u * cosd(th)))} s; (c) v_y = {sf(u * sind(th) - g0 * x / (u * cosd(th)))} m s⁻¹, so it is {"rising" if u * sind(th) - g0 * x / (u * cosd(th)) > 0 else "falling"}; (d) a higher speed would be needed.',
                   f'(a) y = x tan θ − gx²/(2u²cos²θ) rearranged (M1 A1). (b) t = x/(u cos θ) (A1). (c) v_y = u sin θ − gt (M1), sign interpreted (A1). (d) R1.', 6, 'multi_step')
    v = rng.choice([30, 40, 50]); h = rng.choice([80, 100, 125])
    t = math.sqrt(2 * h / g0)
    return num(f'A humanitarian aircraft flying horizontally at {v} m s⁻¹ at a height of {h} m drops a supply crate. Ignore air resistance. (a) Calculate the time for the crate to fall. (b) Determine how far before the target the crate must be released. (c) Describe the position of the crate relative to the aircraft as it falls. (d) Discuss how a parachute changes the drop calculation.',
               f'(a) {sf(t)} s; (b) {sf(v * t)} m; (c) directly below the aircraft (same horizontal velocity); (d) drag reduces both components, so the crate falls more slowly and lands short; release point must be closer and drift by wind considered.',
               f'(a) h = ½gt² (M1), t = {sf(t)} s (A1). (b) x = vt = {sf(v * t)} m (A1). (c) R1. (d) two effects of drag (R1 R1).', 6, 'multi_step')


R.mcqs('ch01-st4', 'C2', (1, 4), [
    ('Two balls are launched from the same point with the same speed at 30° and 60° on level ground (no drag). Which statement is correct?', 'They have the same range but the 60° ball stays in the air longer', ['The 30° ball goes further', 'They have the same time of flight', 'The 60° ball goes further'], 'R ∝ sin 2θ; time ∝ sin θ.'),
    ('A projectile is moving at its highest point. Which arrow describes the direction of its acceleration (no drag)?', 'Vertically downwards', ['Horizontally forwards', 'Along the direction of motion', 'Zero – there is no acceleration'], 'Gravity acts downwards.'),
    ('When air resistance acts on a projectile, compared with no air resistance, the maximum height is', 'lower and reached sooner', ['the same', 'higher', 'lower but reached later'], 'Drag adds to gravity on the way up.'),
])


def _range_spec(rng):
    u = rng.uniform(1.6, 2.6)
    hs = [0.20, 0.40, 0.60, 0.80, 1.00, 1.20]
    xs_ = [round(u * math.sqrt(2 * h_ / g0) * rng.uniform(0.98, 1.02), 3) for h_ in hs]
    return dict(intro='A ball rolls off a horizontal track at a fixed speed u and falls through a height h onto the floor. The horizontal distance x travelled is measured for different h. Theory: x = u√(2h/g).',
                xname='h', xunit='m', yname='x', yunit='m', xs=hs, ys=xs_, xfmt=lambda a: f'{a:.2f}', yfmt=lambda b: f'{b:.3f}',
                plot_x=lambda a: math.sqrt(a), plot_y=lambda b: b, plot_label='x (y) against √h (x)', what='the launch speed u', what_short='u',
                gunit='m^½', deduce=lambda m_, b_: (m_ * math.sqrt(g0 / 2), 'm s⁻¹', 'u = gradient × √(g/2)'))


gradient_fit('ch01-st4', _range_spec)


# =============================================================================================
# ch02 A.2 Forces and momentum
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('weight', 'the gravitational force on a mass, W = mg, acting at the centre of mass'),
           ('normal force', 'the contact force exerted by a surface on an object, perpendicular to the surface'),
           ('tension', 'the pulling force exerted by a taut string, rope or cable along its length'),
           ('upthrust (buoyancy)', 'the upward force exerted by a fluid on an immersed object, equal to the weight of fluid displaced (Archimedes’ principle)'),
           ('free-body diagram', 'a diagram showing a single object and all the external forces acting on it, drawn from the point of application'),
           ('drag', 'the resistive force exerted by a fluid on an object moving through it, opposite to the relative velocity')],
    facts=[('What is the weight of a 65 kg student on Earth?', '638 N', ['65 N', '6.6 N', '6380 N'], 'W = mg = 65 × 9.81.'),
           ('A book rests on a table. The Newton’s third law partner of the book’s weight is', 'the gravitational pull of the book on Earth', ['the normal force of the table on the book', 'the weight of the table', 'the friction on the book'], 'Third-law pairs act on different bodies and are of the same type.'),
           ('For a block on a smooth slope at angle θ, the normal force is', 'mg cos θ', ['mg', 'mg sin θ', 'mg tan θ'], 'Resolve perpendicular to the slope.'),
           ('Which statement about upthrust is correct?', 'It equals the weight of fluid displaced', ['It equals the weight of the object', 'It acts downwards in dense fluids', 'It depends only on the depth'], 'Archimedes’ principle.'),
           ('In a free-body diagram, which forces should be drawn?', 'Only the forces acting on the chosen object', ['All forces in the system', 'The forces the object exerts on others', 'Only the resultant force'], 'Definition of a free-body diagram.')],
    why=[('Explain why an object floats when its average density is less than that of the fluid.', 'When fully immersed the upthrust (ρ_fluid V g) exceeds its weight (ρ_object V g), so it rises until the displaced volume makes upthrust equal to weight.'),
         ('Explain why the normal force on a person in a lift is greater than their weight while the lift accelerates upwards.', 'A resultant upward force is needed to accelerate them: N − mg = ma, so N = m(g + a) > mg.'),
         ('Explain why the tension is the same throughout a light, inextensible string passing over a frictionless pulley.', 'A massless string needs no resultant force to accelerate, and a frictionless pulley exerts no tangential force, so the tension cannot change along it.')],
    contrast=[('mass', 'weight', 'Mass is the amount of matter (scalar, kg), the same everywhere; weight is the gravitational force mg (vector, N), which depends on the local field strength.'),
              ('the normal force on an object', 'the weight of the object', 'The normal force is a contact force from a surface, perpendicular to it, which adjusts to the situation; weight is the gravitational force from Earth. They are not a third-law pair and are equal only in special cases.')],
    misc=[('The normal force and weight of a book on a table are a Newton’s third law pair.', 'They act on the same object and are different types of force; they balance only because the book is in equilibrium. The third-law partner of weight is the book’s pull on Earth.'),
          ('An object’s weight is the same on the Moon as on Earth.', 'Its mass is the same but weight = mg; g on the Moon is about 1.6 m s⁻², so the weight is about one-sixth.'),
          ('Upthrust only acts on objects that float.', 'Any immersed object experiences upthrust; a sinking stone simply has weight greater than the upthrust.')],
    evaluate=[('Free-body diagrams are only useful for simple textbook problems.', ['they isolate one body and clarify which forces act', 'they underpin all engineering structural analysis'], ['complex systems require many diagrams and computer models', 'distributed forces (pressure, drag) are idealised as single arrows'], 'They are a foundational tool used in professional engineering too, though complex systems also require numerical modelling.')],
    extended=[('A helium balloon of volume 0.012 m³ and total mass 4.0 g is held by a string. Density of air = 1.20 kg m⁻³. (a) Draw a free-body diagram for the balloon. (b) Calculate the upthrust. (c) Determine the tension in the string. (d) Calculate the initial acceleration if the string is cut.', '(a) upthrust up, weight and tension down; (b) U = ρVg = 1.20 × 0.012 × 9.81 = 0.141 N; (c) T = U − mg = 0.141 − 0.0392 = 0.102 N; (d) a = 0.102/0.004 = 25 m s⁻² (initially, before drag acts).', 6)],
))


@prob('ch02-st1', d=(1, 5), md=(1, 4), marks=2)
def p_forces_basic(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        m = rng.choice([2.0, 5.0, 8.0, 12, 20, 35]); th = rng.choice([15, 20, 25, 30, 35, 40])
        return dict(stem=f'A {m} kg box rests on a ramp inclined at {th}° to the horizontal in a warehouse in {city}. Calculate the normal force on the box.',
                    v=m * g0 * cosd(th), unit='N', wrongs=[m * g0 * sind(th), m * g0, m * g0 / cosd(th)], key=f'N = mg cos θ = {m} × 9.81 × cos {th}° (M1) = {sf(m * g0 * cosd(th))} N (A1).')
    if k == 1:
        m = rng.choice([2.0, 5.0, 8.0, 12, 20]); th = rng.choice([15, 20, 25, 30, 35])
        return dict(stem=f'A {m} kg crate is on a frictionless slope at {th}°. Calculate the component of its weight acting down the slope.',
                    v=m * g0 * sind(th), unit='N', wrongs=[m * g0 * cosd(th), m * g0, m * g0 * math.tan(math.radians(th))], key=f'F = mg sin θ (M1) = {sf(m * g0 * sind(th))} N (A1).')
    if k == 2:
        V = rng.choice([0.002, 0.005, 0.010, 0.025, 0.050]); rho = rng.choice([1000, 1025, 800])
        fl = {1000: 'fresh water', 1025: 'sea water', 800: 'oil'}[rho]
        return dict(stem=f'A sealed container of volume {V} m³ is fully submerged in {fl} (density {rho} kg m⁻³). Calculate the upthrust on it.',
                    v=rho * V * g0, unit='N', wrongs=[rho * V, rho * V * g0 / 2, V * g0], key=f'Upthrust = ρVg = {rho} × {V} × 9.81 (M1) = {sf(rho * V * g0)} N (A1).')
    if k == 3:
        m = rng.choice([50, 60, 70, 80]); a = rng.choice([0.8, 1.2, 1.5, 2.0])
        up = rng.random() < 0.5
        N_ = m * (g0 + a) if up else m * (g0 - a)
        return dict(stem=f'{who} (mass {m} kg) stands on bathroom scales in a lift in {city} that is accelerating {"upwards" if up else "downwards"} at {a} m s⁻². Calculate the reading of the scales in newtons.',
                    v=N_, unit='N', wrongs=[m * g0, m * (g0 - a) if up else m * (g0 + a), m * a], key=f'N − mg = ±ma (M1); N = {m}(9.81 {"+" if up else "−"} {a}) = {sf(N_)} N (A1).')
    m = rng.choice([0.5, 1.0, 1.5, 2.0, 3.0]); th = rng.choice([20, 30, 40, 50, 60])
    T_ = m * g0 / (2 * cosd(th))
    return dict(stem=f'A {m} kg lantern hangs from the midpoint of a wire; each half of the wire makes {th}° with the vertical. Calculate the tension in the wire.',
                v=T_, unit='N', wrongs=[m * g0 / 2, m * g0 / (2 * sind(th)), m * g0 / cosd(th)], key=f'2T cos θ = mg (M1); T = {sf(T_)} N (A1).', marks=3)


R.mcqs('ch02-st1', 'C2', (1, 4), [
    ('A parachutist falls at terminal velocity. Which statement is correct?', 'The drag force equals the weight', ['The drag force is greater than the weight', 'There are no forces acting', 'The weight is zero'], 'Zero resultant force at constant velocity.'),
    ('A stone is completely submerged and sinking at constant speed in water. Which is correct?', 'Weight = upthrust + drag', ['Weight = upthrust', 'Upthrust = weight + drag', 'Drag = weight'], 'Constant velocity: forces balance.'),
    ('A box is pushed horizontally against a vertical wall so that it does not slip. The force that stops it sliding down is', 'friction from the wall', ['the normal force from the wall', 'the push', 'air resistance'], 'Friction acts parallel to the surface, opposing the tendency to slide.'),
    ('An object is moved from Earth to the Moon. Which is correct?', 'Its mass is unchanged but its weight decreases', ['Both mass and weight decrease', 'Its mass decreases but weight is unchanged', 'Both are unchanged'], 'W = mg, g smaller.'),
])


R.facts('ch02-st2', F(
    terms=[('Newton’s first law', 'an object remains at rest or moves with constant velocity unless acted on by a resultant external force'),
           ('Newton’s second law', 'the resultant force on an object equals its rate of change of momentum; for constant mass F = ma'),
           ('Newton’s third law', 'when body A exerts a force on body B, B exerts a force of equal magnitude and opposite direction on A, of the same type'),
           ('translational equilibrium', 'the state of an object when the resultant force on it is zero, so its velocity is constant'),
           ('inertia', 'the tendency of an object to resist changes in its state of motion, measured by its mass'),
           ('resultant force', 'the single force that has the same effect as all the forces acting on a body combined')],
    facts=[('A resultant force of 12 N acts on a 3.0 kg mass. What is its acceleration?', '4.0 m s⁻²', ['36 m s⁻²', '0.25 m s⁻²', '9.0 m s⁻²'], 'a = F/m.'),
           ('A spacecraft far from any planet switches off its engines. It will', 'continue at constant velocity', ['slow down and stop', 'accelerate', 'move in a circle'], 'Newton’s first law.'),
           ('Which pair of forces is a Newton’s third law pair?', 'Earth pulls the Moon; the Moon pulls Earth', ['The weight of a book and the normal force on it', 'Thrust and drag on an aircraft', 'Tension and weight of a hanging mass'], 'Same type, act on different bodies.'),
           ('A car moves at constant velocity on a straight road. The resultant force on it is', 'zero', ['equal to the engine force', 'equal to the drag', 'in the direction of motion'], 'Constant velocity means equilibrium.'),
           ('What is one newton?', 'The force giving a mass of 1 kg an acceleration of 1 m s⁻²', ['The weight of a 1 kg mass', 'The force giving 1 g an acceleration of 1 m s⁻²', 'The force needed to move 1 kg at 1 m s⁻¹'], 'From F = ma.')],
    why=[('Explain, using Newton’s laws, why passengers lurch forward when a bus brakes suddenly.', 'The braking force acts on the bus, not directly on passengers; by inertia (first law) their bodies continue forward until friction from seats or the floor provides a resultant force to decelerate them.'),
         ('Explain why a rocket can accelerate in the vacuum of space.', 'The rocket pushes exhaust gas backwards; by Newton’s third law the gas pushes the rocket forwards. No air is needed to push against.'),
         ('Explain why two objects in a Newton’s third law pair never cancel each other out.', 'They act on different bodies, so they cannot be added to find the resultant on one body.'),
         ('Explain why a larger force is needed to start a heavy trolley moving than a light one at the same acceleration.', 'By F = ma, the required resultant force is proportional to mass; the heavy trolley has more inertia.')],
    contrast=[('Newton’s first law', 'Newton’s third law', 'The first law concerns one body: with zero resultant force its velocity is constant. The third law concerns two bodies: forces between them are equal and opposite and act on different bodies.')],
    misc=[('A moving object needs a resultant force to keep it moving.', 'A resultant force is only needed to change the velocity; with zero resultant force an object keeps moving at constant velocity (first law).'),
          ('When a horse pulls a cart, the cart pulls back with an equal force, so they cannot move.', 'The equal and opposite forces act on different bodies; the horse moves because the ground pushes it forward more than the cart pulls it back.'),
          ('A heavier object falls faster because the force on it is larger.', 'Its weight is larger but so is its mass; a = W/m = g is the same for all masses in the absence of drag.')],
    evaluate=[('Newton’s laws have been replaced by Einstein’s relativity and are no longer useful.', ['relativity is more accurate at high speeds and in strong gravity', 'GPS requires relativistic corrections'], ['Newton’s laws are extremely accurate for everyday speeds', 'all engineering, spaceflight trajectories and sport science use them', 'relativity reduces to Newtonian mechanics when v ≪ c'], 'Newtonian mechanics remains the valid, simpler model within its domain; relativity extends rather than discards it (NOS: theories have ranges of validity).')],
    extended=[('A car of mass 1200 kg tows a trailer of mass 400 kg with a light rigid towbar. The driving force is 2400 N and resistive forces are 300 N on the car and 100 N on the trailer. (a) Calculate the acceleration. (b) Determine the tension in the towbar. (c) Draw free-body diagrams for the trailer. (d) Explain what happens to the towbar force when the car brakes.', '(a) a = (2400 − 400)/1600 = 1.25 m s⁻²; (b) T − 100 = 400 × 1.25, T = 600 N; (c) trailer: T forward, 100 N resistance back, weight and normal; (d) the trailer pushes on the car, so the towbar is in compression.', 6)],
))


@prob('ch02-st2', d=(1, 5), md=(1, 4), marks=3)
def p_newton2(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        m = rng.choice([800, 1100, 1300, 1500, 1800]); Fd = rng.choice([2500, 3000, 3600, 4200]); Fr = rng.choice([600, 800, 900, 1200])
        return dict(stem=f'A car of mass {m} kg in {city} has a driving force of {Fd} N and total resistive force of {Fr} N. Calculate its acceleration.',
                    v=(Fd - Fr) / m, unit='m s⁻²', wrongs=[Fd / m, (Fd + Fr) / m, (Fd - Fr) * m / 1e6], key=f'Resultant F = {Fd} − {Fr} = {Fd - Fr} N (M1); a = F/m = {sf((Fd - Fr) / m)} m s⁻² (A1).', marks=2)
    if k == 1:
        m1 = rng.choice([2.0, 3.0, 4.0, 5.0]); m2 = rng.choice([1.0, 1.5, 2.0, 2.5])
        a = (m1 - m2) * g0 / (m1 + m2) if m1 != m2 else None
        if a is None:
            return None
        return dict(stem=f'Two masses of {m1} kg and {m2} kg hang from a light string over a frictionless pulley (Atwood machine). Calculate the acceleration of the masses.',
                    v=a, unit='m s⁻²', wrongs=[(m1 - m2) * g0 / m1, g0, (m1 - m2) * g0 / (m1 * m2)], key=f'(m₁ − m₂)g = (m₁ + m₂)a (M1 M1); a = {sf(a)} m s⁻² (A1).')
    if k == 2:
        m1 = rng.choice([2.0, 3.0, 4.0, 6.0]); m2 = rng.choice([0.5, 1.0, 1.5, 2.0])
        a = m2 * g0 / (m1 + m2); T_ = m1 * a
        return dict(stem=f'A {m1} kg trolley on a smooth horizontal bench is connected by a string over a pulley to a hanging mass of {m2} kg. Calculate the tension in the string.',
                    v=T_, unit='N', wrongs=[m2 * g0, m1 * g0, m2 * a], key=f'a = m₂g/(m₁ + m₂) = {sf(a)} m s⁻² (M1 A1); T = m₁a = {sf(T_)} N (A1).')
    if k == 3:
        m = rng.choice([500, 800, 1000, 1200]); a = rng.choice([0.5, 0.8, 1.0, 1.5])
        T_ = m * (g0 + a)
        return dict(stem=f'A lift car of mass {m} kg in a tower in {city} accelerates upwards at {a} m s⁻². Calculate the tension in the supporting cable.',
                    v=T_, unit='N', wrongs=[m * g0, m * a, m * (g0 - a)], key=f'T − mg = ma (M1); T = {m}(9.81 + {a}) (M1) = {sf(T_)} N (A1).')
    F1 = rng.choice([30, 40, 60, 80]); F2 = rng.choice([40, 50, 60, 90]); m = rng.choice([5.0, 8.0, 10, 12])
    Fr = math.hypot(F1, F2)
    return dict(stem=f'Two horizontal forces of {F1} N and {F2} N act at right angles on a {m} kg puck on frictionless ice. Calculate the magnitude of its acceleration.',
                v=Fr / m, unit='m s⁻²', wrongs=[(F1 + F2) / m, abs(F2 - F1) / m if F1 != F2 else Fr / m / 2, Fr * m / 100], key=f'Resultant = √({F1}² + {F2}²) = {sf(Fr)} N (M1); a = {sf(Fr / m)} m s⁻² (A1).', marks=2)


@prob('ch02-st2', d=(2, 5), md=(2, 4), marks=3)
def p_equilibrium(rng, slot):
    W = rng.choice([40, 60, 80, 120, 150, 200]); a1 = rng.choice([30, 35, 40, 45]); a2 = rng.choice([50, 55, 60])
    # two cables at angles a1, a2 to the horizontal
    T1 = W * cosd(a2) / sind(a1 + a2); T2 = W * cosd(a1) / sind(a1 + a2)
    city = rng.choice(CITIES)
    k = rng.randrange(2)
    if k == 0:
        stem = f'A shop sign of weight {W} N in {city} hangs from two cables making angles of {a1}° and {a2}° with the horizontal. Calculate the tension in the cable at {a1}°.'
        return dict(stem=stem, v=T1, unit='N', wrongs=[T2, W / 2, W * sind(a1)], key=f'Horizontal: T₁ cos {a1}° = T₂ cos {a2}°; vertical: T₁ sin {a1}° + T₂ sin {a2}° = {W} (M1 M1); T₁ = {sf(T1)} N (A1).')
    stem = f'A traffic light of weight {W} N is held in equilibrium by two cables at {a1}° and {a2}° above the horizontal. Determine the tension in the cable at {a2}°.'
    return dict(stem=stem, v=T2, unit='N', wrongs=[T1, W / 2, W * cosd(a2)], key=f'Resolve horizontally and vertically (M1 M1); T₂ = W cos {a1}°/sin({a1 + a2}°) = {sf(T2)} N (A1).')


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def c4_lift_profile(rng, slot):
    m = rng.choice([60, 70, 75]); a1 = rng.choice([1.2, 1.5]); a3 = rng.choice([0.8, 1.0])
    k = rng.randrange(2)
    if k == 0:
        return num(f'A {m} kg passenger stands on a force sensor in a lift in a skyscraper. The lift accelerates upwards at {a1} m s⁻², moves at constant speed, then decelerates at {a3} m s⁻² to stop. (a) Calculate the sensor reading in each stage. (b) Sketch a graph of the reading against time. (c) Explain why the passenger feels "heavier" at the start. (d) State the reading if the cable broke and the lift fell freely, and explain it.',
                   f'(a) {sf(m * (g0 + a1))} N, {sf(m * g0)} N, {sf(m * (g0 - a3))} N; (b) step up, middle level, step down; (c) the normal force exceeds the weight because a resultant upward force is required; (d) zero: passenger and lift have the same acceleration g, so no contact force is needed.',
                   f'(a) N = m(g + a) etc. (M1 A1 A1). (b) A1. (c) R1. (d) zero with reason (R1).', 6, 'multi_step')
    M = rng.choice([1500, 2000]); m2 = rng.choice([500, 800]); F_ = rng.choice([4000, 5000, 6000])
    a = F_ / (M + m2)
    return num(f'A tugboat pushes two barges in contact along a canal: barge A (mass {M} kg) is in front and barge B (mass {m2} kg) is behind, next to the tug. The tug exerts {F_} N on B; water resistance is negligible. (a) Calculate the acceleration. (b) Calculate the force B exerts on A. (c) State the force A exerts on B and the law used. (d) Explain how the answer to (b) changes if the order of the barges is reversed.',
               f'(a) {sf(a)} m s⁻²; (b) {sf(M * a)} N; (c) {sf(M * a)} N backwards on B (Newton’s third law); (d) the contact force becomes m_B × a = {sf(m2 * a)} N, because the front barge now has the smaller mass.',
               f'(a) a = F/(total mass) (M1 A1). (b) F = m_A a (A1). (c) equal and opposite (A1). (d) R1 with value (A1).', 6, 'multi_step')


R.mcqs('ch02-st2', 'C2', (1, 4), [
    ('A person stands still on a floor. The force that is equal and opposite to the person’s weight according to Newton’s third law is', 'the gravitational force of the person on Earth', ['the normal force from the floor on the person', 'the friction on the person', 'the normal force of the person on the floor'], 'Third-law pairs are of the same type and act on different bodies.'),
    ('A ball is moving upwards after being thrown. Which forces act on it (no drag)?', 'Only its weight', ['Its weight and an upward throwing force', 'An upward force only', 'No forces'], 'Once released the throwing force no longer acts.'),
    ('A truck collides with a small car. During the collision, the force on the car from the truck is', 'equal in size to the force on the truck from the car', ['larger than the force on the truck', 'smaller than the force on the truck', 'zero'], 'Newton’s third law; the car’s acceleration is larger because its mass is smaller.'),
])


def _n2_spec(rng):
    M = rng.uniform(0.95, 1.05)  # total mass kg
    ms = [0.020, 0.040, 0.060, 0.080, 0.100, 0.120]
    a_s = [round(m_ * g0 / M * rng.uniform(0.97, 1.03), 3) for m_ in ms]
    return dict(intro='A trolley on a friction-compensated runway is pulled by a hanging mass m. The total mass of trolley plus hanging masses is kept constant by moving masses from the trolley to the hanger. The acceleration a is measured with a light gate. Theory: mg = M_total a.',
                xname='accelerating force mg', xunit='N', yname='a', yunit='m s⁻²', xs=[m_ * g0 for m_ in ms], ys=a_s, xfmt=lambda x: f'{x:.3f}', yfmt=lambda y: f'{y:.3f}',
                plot_x=lambda x: x, plot_y=lambda y: y, plot_label='a (y) against mg (x)', what='the total mass M_total of the system', what_short='M_total',
                gunit='kg⁻¹', deduce=lambda m_, b_: (1 / m_, 'kg', 'M_total = 1/gradient'))


gradient_fit('ch02-st2', _n2_spec)


R.facts('ch02-st3', F(
    terms=[('static friction', 'the friction force that prevents surfaces in contact from sliding, which can take any value up to μₛN'),
           ('dynamic (kinetic) friction', 'the friction force between surfaces sliding over each other, F = μ_d N, roughly independent of speed'),
           ('coefficient of friction', 'the ratio of the friction force to the normal force between two surfaces, a dimensionless number'),
           ('viscosity', 'a measure of a fluid’s resistance to flow, η, in Pa s'),
           ('Stokes’ law', 'the drag on a small sphere moving slowly through a viscous fluid: F_d = 6πηrv'),
           ('terminal velocity', 'the constant velocity reached when the drag (plus upthrust) on a falling object balances its weight')],
    facts=[('A block is on the point of sliding on a slope inclined at θ. The coefficient of static friction is', 'tan θ', ['sin θ', 'cos θ', '1/tan θ'], 'mg sin θ = μₛ mg cos θ.'),
           ('Which is usually true for a given pair of surfaces?', 'μₛ > μ_d', ['μ_d > μₛ', 'μₛ = μ_d', 'μ can exceed 10 for any surfaces'], 'It takes more force to start sliding than to keep sliding.'),
           ('According to Stokes’ law, if the radius of a sphere doubles at the same speed, the drag', 'doubles', ['quadruples', 'halves', 'is unchanged'], 'F = 6πηrv ∝ r.'),
           ('Stokes’ law applies to', 'small spheres moving slowly in a fluid with laminar flow', ['any object at any speed', 'objects in turbulent flow', 'cars at motorway speeds'], 'It assumes laminar (streamline) flow.'),
           ('What is the SI unit of viscosity?', 'Pa s', ['N m', 'kg m⁻³', 'N s'], 'η = F/(6πrv): N/(m × m s⁻¹) = N s m⁻² = Pa s.')],
    why=[('Explain why the terminal velocity of a small steel ball in glycerol increases with the radius of the ball.', 'Weight minus upthrust ∝ r³, while Stokes drag ∝ rv; at terminal velocity they balance, so v ∝ r², larger balls fall faster.'),
         ('Explain why static friction can have any value up to a maximum.', 'Static friction adjusts to equal the applied force parallel to the surface so that there is no sliding, until the applied force exceeds μₛN.'),
         ('Explain why anti-lock brakes (ABS) can stop a car in a shorter distance than locked wheels.', 'Rolling tyres grip using static friction, whose maximum μₛN exceeds the dynamic friction μ_d N of skidding tyres; ABS keeps the wheels just below the slipping point.'),
         ('Explain why the viscosity of oil is measured at a controlled temperature.', 'Viscosity of liquids decreases strongly as temperature rises, so terminal velocities and the deduced η depend on temperature.')],
    contrast=[('static friction', 'dynamic friction', 'Static friction acts when there is no relative sliding and adjusts up to μₛN; dynamic friction acts during sliding with a fixed value μ_d N, usually smaller.')],
    misc=[('Friction always opposes the motion of an object.', 'Friction opposes relative sliding between surfaces; it can cause motion, e.g. friction from the road pushes a car forward and lets you walk.'),
          ('The friction force on a stationary block always equals μₛN.', 'μₛN is the maximum; the actual static friction equals whatever is needed to prevent sliding, which may be less.'),
          ('Stokes’ law shows that drag is proportional to speed squared.', 'Stokes’ law gives drag ∝ v for slow laminar flow; drag ∝ v² applies at higher speeds with turbulent flow.')],
    evaluate=[('Friction is always a nuisance that engineers try to eliminate.', ['friction wastes energy as heat in engines and bearings', 'causes wear'], ['walking, braking, tyre grip and belts rely on friction', 'brake pads and clutches are designed for high μ'], 'Friction is undesirable in some systems and essential in others; engineers control rather than eliminate it.')],
    extended=[('A 2.0 mm diameter steel ball (density 7800 kg m⁻³) falls through oil of density 900 kg m⁻³ and reaches a terminal velocity of 0.042 m s⁻¹. (a) Draw the forces on the ball at terminal velocity. (b) Calculate the weight and the upthrust. (c) Determine the viscosity of the oil. (d) Suggest why the measurement should be made far from the walls of the tube.', '(a) weight down; upthrust and drag up; (b) V = 4.19 × 10⁻⁹ m³, W = 3.21 × 10⁻⁴ N, U = 3.70 × 10⁻⁵ N; (c) η = (W − U)/(6πrv) = 2.84 × 10⁻⁴/(6π × 0.001 × 0.042) = 0.72 Pa s; (d) the walls disturb the flow and increase the drag, so Stokes’ law no longer applies.', 6)],
))


@prob('ch02-st3', d=(1, 5), md=(1, 4), marks=2)
def p_friction(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        th = rng.choice([18, 22, 25, 28, 31, 35])
        return dict(stem=f'{who} slowly tilts a plank with a wooden block on it. The block begins to slide when the plank makes {th}° with the horizontal. Calculate the coefficient of static friction.',
                    v=math.tan(math.radians(th)), unit='', wrongs=[sind(th), cosd(th), 1 / math.tan(math.radians(th))], key=f'At slipping, mg sin θ = μₛ mg cos θ (M1); μₛ = tan {th}° = {sf(math.tan(math.radians(th)))} (A1).')
    if k == 1:
        mu = rng.choice([0.15, 0.20, 0.25, 0.30, 0.40]); u = rng.choice([3.0, 4.0, 5.0, 6.0, 8.0])
        s = u * u / (2 * mu * g0)
        return dict(stem=f'A curling stone in {city} is released at {u} m s⁻¹ on ice; the coefficient of dynamic friction is {mu}. Calculate how far it slides before stopping.' if mu < 0.2 else
                    f'A box slides across a floor at {u} m s⁻¹; the coefficient of dynamic friction is {mu}. Calculate how far it slides before stopping.',
                    v=s, unit='m', wrongs=[u * u / (mu * g0), u / (mu * g0), u * u * mu / (2 * g0)], key=f'a = μg = {sf(mu * g0)} m s⁻² (M1); s = u²/(2a) = {sf(s)} m (A1).')
    if k == 2:
        m = rng.choice([10, 15, 20, 25, 40]); mu = rng.choice([0.25, 0.30, 0.35, 0.40]); F_ = rng.choice([120, 150, 180, 200])
        fr = mu * m * g0
        if F_ <= fr:
            return None
        return dict(stem=f'A {m} kg crate is pulled across a warehouse floor in {city} by a horizontal force of {F_} N. The coefficient of dynamic friction is {mu}. Calculate the acceleration of the crate.',
                    v=(F_ - fr) / m, unit='m s⁻²', wrongs=[F_ / m, (F_ + fr) / m, (F_ - mu * m) / m], key=f'Friction = μmg = {sf(fr)} N (M1); a = (F − f)/m = {sf((F_ - fr) / m)} m s⁻² (A1).')
    if k == 3:
        r = rng.choice([0.5, 1.0, 1.5, 2.0]) * 1e-3; v = rng.choice([0.02, 0.05, 0.08, 0.10]); eta = rng.choice([0.8, 1.0, 1.2, 1.5])
        Fd = 6 * math.pi * eta * r * v
        return dict(stem=f'A ball bearing of radius {sf(r * 1e3, 2)} mm moves at {v} m s⁻¹ through glycerol of viscosity {eta} Pa s. Calculate the drag force using Stokes’ law.',
                    v=Fd, unit='N', wrongs=[6 * math.pi * eta * r * r * v, 6 * math.pi * eta * 2 * r * v, Fd / (6 * math.pi)], key=f'F = 6πηrv (M1) = 6π × {eta} × {sf(r)} × {v} = {sf(Fd)} N (A1).')
    r = rng.choice([0.5, 0.75, 1.0, 1.25]) * 1e-3; rs = 7800; rf = rng.choice([1260, 900, 870]); eta = rng.choice([0.9, 1.2, 1.5])
    vt = 2 * r * r * g0 * (rs - rf) / (9 * eta)
    fl = {1260: 'glycerol', 900: 'castor oil', 870: 'motor oil'}[rf]
    return dict(stem=f'A steel ball (density 7800 kg m⁻³, radius {sf(r * 1e3, 3)} mm) falls through {fl} (density {rf} kg m⁻³, viscosity {eta} Pa s). Determine its terminal velocity.',
                v=vt, unit='m s⁻¹', wrongs=[2 * r * r * g0 * rs / (9 * eta), 2 * r * g0 * (rs - rf) / (9 * eta) * r * 2, r * r * g0 * (rs - rf) / (9 * eta)],
                key=f'At terminal velocity W = U + F_d: (4/3)πr³(ρₛ − ρ_f)g = 6πηrv (M1 M1); v = 2r²g(ρₛ − ρ_f)/(9η) = {sf(vt)} m s⁻¹ (A1).', marks=3)


R.mcqs('ch02-st3', 'C2', (1, 4), [
    ('A box rests on a horizontal floor and a small horizontal push is applied but it does not move. The friction force is', 'equal to the push', ['greater than the push', 'zero', 'equal to μₛ mg'], 'Static friction balances the applied force.'),
    ('A sphere falls through oil at terminal velocity. If a sphere of the same material with twice the radius is used, the terminal velocity becomes', 'four times as large', ['twice as large', 'the same', 'eight times as large'], 'v ∝ r².'),
    ('A car accelerates forwards on a road. The friction force from the road on the tyres is', 'forwards', ['backwards', 'zero', 'vertically upwards'], 'Tyres push back on the road; the road pushes forward on the tyres.'),
    ('The coefficient of dynamic friction between two surfaces depends mainly on', 'the nature of the two surfaces', ['the area of contact', 'the speed of sliding', 'the mass of the object'], 'Friction is approximately independent of contact area and speed.'),
])


def _stokes_spec(rng):
    eta = rng.uniform(0.9, 1.5); rf = 1260; rs = 7800
    rs_mm = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75]
    vs = [round(2 * (r * 1e-3) ** 2 * g0 * (rs - rf) / (9 * eta) * rng.uniform(0.97, 1.03), 4) for r in rs_mm]
    return dict(intro='Steel balls (density 7800 kg m⁻³) of different radii r are dropped into glycerol (density 1260 kg m⁻³) and their terminal velocities v are measured using marks on a tall tube. Theory: v = 2r²g(ρₛ − ρ_f)/(9η).',
                xname='r', xunit='mm', yname='v', yunit='m s⁻¹', xs=rs_mm, ys=vs, xfmt=lambda x: f'{x:.2f}', yfmt=lambda y: f'{y:.4f}',
                plot_x=lambda x: (x * 1e-3) ** 2, plot_y=lambda y: y, plot_label='v (y) against r² in m² (x)', what='the viscosity η of the glycerol', what_short='η',
                gunit='m⁻¹ s⁻¹', deduce=lambda m_, b_: (2 * g0 * (rs - rf) / (9 * m_), 'Pa s', 'η = 2g(ρₛ − ρ_f)/(9 × gradient)'))


gradient_fit('ch02-st3', _stokes_spec)


R.facts('ch02-st4', F(
    terms=[('linear momentum', 'the product of mass and velocity, p = mv, a vector quantity'),
           ('impulse', 'the product of force and the time for which it acts, J = FΔt, equal to the change in momentum'),
           ('conservation of linear momentum', 'the total momentum of a system remains constant provided no resultant external force acts on it'),
           ('elastic collision', 'a collision in which total kinetic energy is conserved'),
           ('inelastic collision', 'a collision in which kinetic energy is not conserved, though momentum is'),
           ('explosion', 'an interaction in which a system initially at rest separates into parts; total momentum stays zero while kinetic energy increases')],
    facts=[('What are the units of momentum?', 'kg m s⁻¹', ['kg m s⁻²', 'N m', 'J s⁻¹'], 'p = mv.'),
           ('The area under a force–time graph gives the', 'impulse (change in momentum)', ['work done', 'power', 'acceleration'], 'J = ∫F dt.'),
           ('In a perfectly inelastic collision, the objects', 'stick together and move with a common velocity', ['bounce apart with no loss of kinetic energy', 'both stop', 'lose all their momentum'], 'Definition.'),
           ('Which quantity is always conserved in a collision of an isolated system?', 'Total momentum', ['Total kinetic energy', 'The velocity of each object', 'The momentum of each object'], 'No external force: momentum conserved.'),
           ('Newton’s second law in its most general form is', 'F = Δp/Δt', ['F = mv', 'F = ma only', 'F = p × t'], 'Valid even when mass changes.')],
    why=[('Explain how a car’s crumple zone reduces the force on passengers in a crash.', 'The change in momentum is fixed by the crash; crumpling increases the collision time, so the average force F = Δp/Δt is reduced.'),
         ('Explain why a gun recoils when it fires a bullet.', 'Total momentum before is zero; the bullet gains forward momentum, so the gun must gain equal backward momentum to keep the total zero.'),
         ('Explain why kinetic energy can increase in an explosion even though momentum is conserved.', 'Chemical potential energy is converted to kinetic energy; momentum is a vector, so equal and opposite momenta still sum to zero while the (scalar) kinetic energies add.'),
         ('Explain why a falling ball and Earth together conserve momentum.', 'The gravitational forces between them are an internal third-law pair, so the total momentum of the ball–Earth system is constant; Earth gains an equal upward momentum, but its velocity change is negligible.')],
    contrast=[('elastic collisions', 'inelastic collisions', 'Both conserve momentum; elastic collisions also conserve total kinetic energy, while in inelastic collisions some kinetic energy is transferred to internal energy, sound or deformation.')],
    misc=[('Momentum is not conserved when a ball hits a wall and stops.', 'The ball’s momentum is transferred to the wall and Earth; momentum of the whole system is conserved, but Earth’s velocity change is negligible.'),
          ('In an elastic collision, both objects keep their original speeds.', 'Total kinetic energy is conserved, but energy and momentum are redistributed; for example a moving ball hitting an identical stationary ball stops while the other moves off.'),
          ('A large force always produces a large change in momentum.', 'The change in momentum is the impulse FΔt; a large force acting for a very short time can give a small change.')],
    evaluate=[('Airbags make cars completely safe in collisions.', ['they increase the stopping time and spread the force over a larger area', 'they significantly reduce head and chest injuries'], ['they do not prevent all injuries and are less effective without seat belts', 'they can injure small children or out-of-position occupants', 'side and rear impacts are only partly protected'], 'Airbags greatly reduce injury by lengthening the impact time, but they work as part of a system with seat belts and crumple zones and cannot make crashes completely safe.')],
    extended=[('A 0.150 kg cricket ball travelling at 32 m s⁻¹ is hit straight back at 41 m s⁻¹. The contact time is 1.2 ms. (a) Calculate the change in momentum. (b) Determine the average force on the ball. (c) Sketch a likely force–time graph and explain its shape. (d) Explain why a batter "follows through".', '(a) Δp = 0.150 × (41 + 32) = 11.0 kg m s⁻¹; (b) F = 11.0/0.0012 = 9.1 × 10³ N; (c) rises to a peak as the ball compresses then falls to zero – area = impulse; (d) following through keeps the bat in contact longer, increasing the impulse and the ball’s speed.', 6)],
))


@prob('ch02-st4', d=(1, 5), md=(1, 4), marks=3)
def p_momentum(rng, slot):
    k = rng.randrange(6)
    who, city = who_city(rng)
    if k == 0:
        m1 = rng.choice([800, 1000, 1200, 1500]); u1 = rng.choice([10, 12, 15, 18]); m2 = rng.choice([900, 1100, 1300, 2000])
        v = m1 * u1 / (m1 + m2)
        return dict(stem=f'A car of mass {m1} kg moving at {u1} m s⁻¹ collides with a stationary car of mass {m2} kg at a junction in {city}. They lock together. Calculate their common velocity just after the collision.',
                    v=v, unit='m s⁻¹', wrongs=[u1 / 2, m1 * u1 / m2, m2 * u1 / (m1 + m2)], key=f'Momentum conserved: {m1} × {u1} = ({m1} + {m2})v (M1); v = {sf(v)} m s⁻¹ (A1).', marks=2)
    if k == 1:
        m1 = rng.choice([800, 1000, 1200]); u1 = rng.choice([10, 12, 15]); m2 = rng.choice([900, 1100, 1300])
        v = m1 * u1 / (m1 + m2); dK = 0.5 * m1 * u1 ** 2 - 0.5 * (m1 + m2) * v * v
        return dict(stem=f'A {m1} kg car at {u1} m s⁻¹ runs into the back of a stationary {m2} kg car and they move off together. Calculate the kinetic energy transferred to other forms in the collision.',
                    v=dK, unit='J', wrongs=[0.5 * m1 * u1 ** 2, 0.5 * (m1 + m2) * v * v, 0.5 * m1 * u1 ** 2 - 0.5 * m1 * v * v], key=f'v = {sf(v)} m s⁻¹ (M1); KE before = {sf(0.5 * m1 * u1 ** 2)} J, after = {sf(0.5 * (m1 + m2) * v * v)} J (M1); loss = {sf(dK)} J (A1).')
    if k == 2:
        M = rng.choice([3.0, 4.0, 4.5, 5.0]); m = rng.choice([0.008, 0.010, 0.015, 0.020]); v = rng.choice([350, 400, 600, 800])
        return dict(stem=f'A rifle of mass {M} kg fires a {sf(m * 1000, 2)} g bullet at {v} m s⁻¹. Calculate the recoil speed of the rifle.',
                    v=m * v / M, unit='m s⁻¹', wrongs=[M * v / m / 1e5, m * v, m * v / (M + m) * 2], key=f'Total momentum zero: Mv_R = mv (M1); v_R = {sf(m * v / M)} m s⁻¹ (A1).', marks=2)
    if k == 3:
        m = rng.choice([0.045, 0.057, 0.15, 0.43]); u = rng.choice([15, 20, 25, 30]); v = rng.choice([10, 18, 25, 35]); t = rng.choice([0.002, 0.005, 0.008, 0.010])
        sport = {0.045: 'golf ball', 0.057: 'tennis ball', 0.15: 'cricket ball', 0.43: 'football'}[m]
        F_ = m * (u + v) / t
        return dict(stem=f'A {m} kg {sport} arrives at {u} m s⁻¹ and leaves along the same line in the opposite direction at {v} m s⁻¹. The contact time is {t * 1000:g} ms. Calculate the average force on the ball.',
                    v=F_, unit='N', wrongs=[m * abs(v - u) / t if u != v else m * u / t, m * (u + v) * t, m * v / t], key=f'Δp = m(v + u) = {sf(m * (u + v))} kg m s⁻¹ (direction reversal) (M1 A1); F = Δp/Δt = {sf(F_)} N (A1).')
    if k == 4:
        F_ = rng.choice([200, 400, 600, 800]); t = rng.choice([0.02, 0.05, 0.10, 0.20]); m = rng.choice([0.5, 1.0, 2.0, 5.0])
        return dict(stem=f'A force–time graph for a kick is approximately a triangle with a peak force of {F_} N lasting a total of {t} s. The ball has mass {m} kg and is initially at rest. Calculate its speed after the kick.',
                    v=0.5 * F_ * t / m, unit='m s⁻¹', wrongs=[F_ * t / m, 0.5 * F_ * t, F_ / (m * t) / 100], key=f'Impulse = area = ½ × {F_} × {t} = {sf(0.5 * F_ * t)} N s (M1 A1); v = J/m = {sf(0.5 * F_ * t / m)} m s⁻¹ (A1).')
    m1 = rng.choice([2.0, 3.0, 4.0]); u1 = rng.choice([4.0, 5.0, 6.0]); m2 = rng.choice([1.0, 2.0, 3.0]); v1 = rng.choice([1.0, 1.5, 2.0])
    v2 = (m1 * u1 - m1 * v1) / m2
    return dict(stem=f'On an air track, a {m1} kg glider moving at {u1} m s⁻¹ hits a stationary {m2} kg glider. After the collision the first glider moves on at {v1} m s⁻¹ in the same direction. Calculate the velocity of the second glider.',
                v=v2, unit='m s⁻¹', wrongs=[m1 * u1 / m2, (m1 * u1 + m1 * v1) / m2, u1 - v1], key=f'{m1} × {u1} = {m1} × {v1} + {m2}v (M1); v = {sf(v2)} m s⁻¹ (A1).', marks=2)


@R.add('ch02-st4', 'C4', (3, 5), 'multi_step')
def c4_collision_check(rng, slot):
    k = rng.randrange(3)
    if k == 0:
        m1, u1, m2 = rng.choice([(2.0, 3.0, 1.0), (1.5, 4.0, 1.5), (3.0, 2.0, 1.0)])
        v1 = (m1 - m2) / (m1 + m2) * u1; v2 = 2 * m1 / (m1 + m2) * u1
        return num(f'A {m1} kg ball moving at {u1} m s⁻¹ collides head-on and elastically with a stationary {m2} kg ball. (a) Write down the equations for conservation of momentum and of kinetic energy. (b) Solve them to find both final velocities. (c) Verify that the relative speed of approach equals the relative speed of separation. (d) Describe the outcome when the masses are equal.',
                   f'(b) v₁ = {sf(v1)} m s⁻¹, v₂ = {sf(v2)} m s⁻¹; (c) approach {u1} m s⁻¹, separation {sf(v2 - v1)} m s⁻¹; (d) the first ball stops and the second moves off with {u1} m s⁻¹.',
                   f'(a) both equations (M1 M1). (b) v₁ = (m₁ − m₂)u/(m₁ + m₂), v₂ = 2m₁u/(m₁ + m₂) (A1 A1). (c) A1. (d) R1.', 6, 'multi_step')
    if k == 1:
        m = rng.choice([0.010, 0.012, 0.020]); M = rng.choice([1.5, 2.0, 2.5]); h = rng.choice([0.08, 0.10, 0.12])
        V = math.sqrt(2 * g0 * h); u = (m + M) * V / m
        return num(f'A ballistic pendulum is used to measure the speed of an air-rifle pellet. A {sf(m * 1000, 2)} g pellet embeds in a {M} kg wooden block hanging on strings, and the block rises by {h * 100:g} cm. (a) Calculate the speed of the block just after impact. (b) Determine the speed of the pellet. (c) Calculate the percentage of the pellet’s kinetic energy that is converted to internal energy. (d) Explain why energy conservation cannot be used for the collision itself.',
                   f'(a) {sf(V)} m s⁻¹; (b) {sf(u)} m s⁻¹; (c) {sf(100 * M / (m + M), 3)} %; (d) the collision is inelastic – kinetic energy is transferred to internal energy and sound, so only momentum is conserved during the impact.',
                   f'(a) ½V² = gh (M1), V = {sf(V)} (A1). (b) mu = (m + M)V (M1), u = {sf(u)} (A1). (c) fraction lost = M/(m + M) (A1). (d) R1.', 6, 'multi_step')
    mr = rng.choice([1.2e5, 1.5e5, 2.0e5]); dm = rng.choice([800, 1000, 1200]); ve = rng.choice([2500, 3000, 3500])
    thrust = dm * ve
    return num(f'A rocket of mass {sf(mr, 2)} kg on the launch pad ejects exhaust gas at {dm} kg s⁻¹ with speed {ve} m s⁻¹ relative to the rocket. (a) Use F = Δp/Δt to calculate the thrust. (b) Determine the initial acceleration. (c) Explain why the acceleration increases during the flight even if the thrust is constant. (d) Explain why F = ma cannot be applied directly to the whole flight.',
               f'(a) {sf(thrust)} N; (b) {sf((thrust - mr * g0) / mr)} m s⁻²; (c) the rocket mass decreases as fuel is used (and g and drag change); (d) the mass is not constant, so F = Δp/Δt must be used.',
               f'(a) F = (Δm/Δt)v (M1 A1). (b) (T − mg)/m (M1 A1). (c) R1. (d) R1.', 6, 'multi_step')


R.mcqs('ch02-st4', 'C2', (1, 4), [
    ('A stationary bomb explodes into two fragments of masses m and 3m. The ratio of their speeds (m : 3m) is', '3 : 1', ['1 : 3', '1 : 1', '9 : 1'], 'Equal and opposite momenta.'),
    ('A ball of mass m hits a wall perpendicularly at speed v and rebounds at speed v. The magnitude of the change in momentum is', '2mv', ['mv', 'zero', 'mv²'], 'Direction reverses.'),
    ('Two trolleys stuck together by a compressed spring are released from rest on a smooth track. Which is correct after release?', 'Total momentum is zero and total kinetic energy has increased', ['Both momentum and kinetic energy are zero', 'Total momentum has increased', 'Kinetic energy is conserved'], 'Elastic potential energy → kinetic energy.'),
    ('An egg dropped on a cushion does not break, but one dropped on concrete does, because the cushion', 'increases the time of impact, reducing the force', ['reduces the change in momentum', 'increases the impulse', 'reduces the speed of impact'], 'Same Δp, longer Δt.'),
])


R.facts('ch02-st5', F(
    terms=[('centripetal acceleration', 'the acceleration of an object moving in a circle, directed towards the centre, of magnitude v²/r = ω²r'),
           ('centripetal force', 'the resultant force towards the centre needed to keep an object moving in a circle, F = mv²/r'),
           ('angular velocity', 'the rate of change of angle swept out, ω = Δθ/Δt = 2π/T, in rad s⁻¹'),
           ('period (circular motion)', 'the time for one complete revolution, T = 2πr/v'),
           ('radian', 'the angle subtended at the centre of a circle by an arc equal in length to the radius')],
    facts=[('In uniform circular motion, the direction of the acceleration is', 'towards the centre of the circle', ['along the tangent', 'away from the centre', 'zero'], 'Centripetal.'),
           ('If the speed of a car on a bend of fixed radius doubles, the centripetal force needed', 'becomes four times as large', ['doubles', 'halves', 'is unchanged'], 'F ∝ v².'),
           ('What provides the centripetal force for a car going round a flat bend?', 'Friction between the tyres and the road', ['The engine', 'The weight of the car', 'Centrifugal force'], 'Friction acts sideways towards the centre.'),
           ('An object moves in a circle at constant speed. The work done by the centripetal force is', 'zero', ['mv²', 'positive', 'negative'], 'Force is perpendicular to velocity.'),
           ('What is the angular velocity of the Earth about its axis?', '7.27 × 10⁻⁵ rad s⁻¹', ['2π rad s⁻¹', '1.16 × 10⁻⁵ rad s⁻¹', '4.17 × 10⁻³ rad s⁻¹'], 'ω = 2π/86 400 s (sidereal day ≈ 86 164 s).')],
    why=[('Explain why an object moving in a circle at constant speed is accelerating.', 'Its velocity changes direction continuously, so there is a change in velocity per unit time directed towards the centre.'),
         ('Explain why banking a road allows cars to take a bend safely at higher speed.', 'On a banked road the horizontal component of the normal force points towards the centre, adding to friction (or replacing it) as the centripetal force.'),
         ('Explain why a passenger in a car turning a corner feels pushed outwards.', 'By inertia the passenger tends to continue in a straight line; the door or seat must push them inwards to provide the centripetal force. There is no real outward force in the ground frame.'),
         ('Explain why there is a minimum speed at the top of a vertical loop on a roller coaster.', 'At the top the weight alone can supply the centripetal force when mg = mv²/r; below v = √(gr) gravity would pull the car inwards more than needed and it would leave the track.')],
    contrast=[('centripetal force', 'centrifugal force', 'Centripetal force is the real resultant force towards the centre that causes circular motion; "centrifugal force" is an apparent outward force felt only in the rotating frame, not a real interaction.')],
    misc=[('Centripetal force is an extra force acting on objects moving in circles.', 'It is not a new type of force; it is the resultant of real forces (tension, friction, gravity, normal force) acting towards the centre.'),
          ('If the string of a whirling ball breaks, the ball flies radially outwards.', 'It moves off along the tangent to the circle at that point, by Newton’s first law.'),
          ('An object moving in a circle at constant speed has zero acceleration.', 'Its velocity direction changes, so it has a centripetal acceleration v²/r.')],
    evaluate=[('Artificial gravity in a rotating space station would feel identical to gravity on Earth.', ['the floor provides a normal force mω²r giving the feeling of weight', 'g-like accelerations can be achieved with reasonable radius'], ['the effective g varies with height (head vs feet) in a small station', 'Coriolis effects make moving objects curve and cause dizziness', 'large radii are needed for comfort'], 'Rotation can mimic gravity, but only a large, slowly rotating station would feel close to Earth gravity; differences remain.')],
    extended=[('A satellite in a circular orbit 400 km above Earth’s surface has a period of 92.6 min. Radius of Earth = 6370 km. (a) Calculate the orbital speed. (b) Calculate the centripetal acceleration. (c) Identify the force providing the centripetal force. (d) Explain why astronauts on board appear weightless.', '(a) v = 2π(6.77 × 10⁶)/(5556 s) = 7.66 × 10³ m s⁻¹; (b) a = v²/r = 8.66 m s⁻²; (c) Earth’s gravitational force; (d) they and the station fall freely with the same acceleration, so there is no normal force.', 6)],
))


@prob('ch02-st5', d=(1, 5), md=(1, 4), marks=2)
def p_circular(rng, slot):
    k = rng.randrange(6)
    who, city = who_city(rng)
    if k == 0:
        m = rng.choice([800, 1000, 1200, 1500]); v = rng.choice([12, 15, 18, 20, 25]); r = rng.choice([40, 50, 60, 80, 100])
        return dict(stem=f'A car of mass {m} kg rounds a bend of radius {r} m at {v} m s⁻¹ near {city}. Calculate the centripetal force needed.',
                    v=m * v * v / r, unit='N', wrongs=[m * v / r, m * v * v / (2 * r), m * v * v * r / 1e4], key=f'F = mv²/r (M1) = {sf(m * v * v / r)} N (A1).')
    if k == 1:
        r = rng.choice([0.40, 0.60, 0.80, 1.0, 1.2]); T = rng.choice([0.5, 0.8, 1.0, 1.5, 2.0])
        v = 2 * math.pi * r / T
        return dict(stem=f'{who} whirls a ball on a string in a horizontal circle of radius {r} m, completing one revolution every {T} s. Calculate the centripetal acceleration of the ball.',
                    v=v * v / r, unit='m s⁻²', wrongs=[v / r, v * v, 2 * math.pi * r / T ** 2], key=f'v = 2πr/T = {sf(v)} m s⁻¹ (M1); a = v²/r = {sf(v * v / r)} m s⁻² (A1).')
    if k == 2:
        mu = rng.choice([0.4, 0.5, 0.6, 0.7, 0.8]); r = rng.choice([30, 40, 50, 60, 80])
        return dict(stem=f'The coefficient of static friction between tyres and a flat road is {mu}. Calculate the maximum speed at which a car can round a bend of radius {r} m without skidding.',
                    v=math.sqrt(mu * g0 * r), unit='m s⁻¹', wrongs=[mu * g0 * r, math.sqrt(g0 * r), math.sqrt(mu * r)], key=f'μmg = mv²/r (M1); v = √(μgr) = {sf(math.sqrt(mu * g0 * r))} m s⁻¹ (A1).')
    if k == 3:
        r = rng.choice([6.0, 8.0, 10, 12, 15])
        return dict(stem=f'A roller-coaster loop at a theme park near {city} has radius {r} m at the top. Calculate the minimum speed at the top for the car to stay on the track.',
                    v=math.sqrt(g0 * r), unit='m s⁻¹', wrongs=[g0 * r, math.sqrt(2 * g0 * r), math.sqrt(g0 / r)], key=f'At minimum speed mg = mv²/r (M1); v = √(gr) = {sf(math.sqrt(g0 * r))} m s⁻¹ (A1).')
    if k == 4:
        rpm = rng.choice([800, 1000, 1200, 1400]); r = rng.choice([0.20, 0.25, 0.30])
        w = 2 * math.pi * rpm / 60
        return dict(stem=f'The drum of a washing machine of radius {r} m spins at {rpm} revolutions per minute. Calculate the centripetal acceleration of clothes at the drum wall.',
                    v=w * w * r, unit='m s⁻²', wrongs=[w * r, (rpm / 60) ** 2 * r, w * w * r / (2 * math.pi)], key=f'ω = 2π × {rpm}/60 = {sf(w)} rad s⁻¹ (M1); a = ω²r = {sf(w * w * r)} m s⁻² (A1).')
    m = rng.choice([0.2, 0.3, 0.5]); r = rng.choice([0.6, 0.8, 1.0]); v = rng.choice([4.0, 5.0, 6.0])
    T_ = m * v * v / r + m * g0
    return dict(stem=f'A {m} kg bucket of water is swung in a vertical circle of radius {r} m. At the lowest point its speed is {v} m s⁻¹. Calculate the tension in the rope at that point.',
                v=T_, unit='N', wrongs=[m * v * v / r, m * v * v / r - m * g0, m * g0], key=f'T − mg = mv²/r (M1); T = {sf(m * v * v / r)} + {sf(m * g0)} = {sf(T_)} N (A1).', marks=3)


@R.add('ch02-st5', 'C4', (3, 5), 'multi_step')
def c4_banked(rng, slot):
    k = rng.randrange(2)
    if k == 0:
        r = rng.choice([150, 200, 250]); th = rng.choice([10, 12, 15])
        v = math.sqrt(g0 * r * math.tan(math.radians(th)))
        return num(f'A motorway exit ramp is a bend of radius {r} m banked at {th}°. (a) Draw the forces on a car on the bend when no friction is needed. (b) Show that the "design speed" with no friction is v = √(gr tan θ) and calculate it. (c) Explain what happens to the friction force if a car travels faster than this. (d) Discuss why cyclists lean into bends.',
                   f'(b) {sf(v)} m s⁻¹ ({sf(v * 3.6, 3)} km h⁻¹); (c) friction acts down the slope (inwards) to provide the extra centripetal force, up to μN; (d) leaning makes the resultant of normal and friction forces pass through the centre of mass, avoiding a toppling torque.',
                   f'(a) weight and normal only (A1). (b) N cos θ = mg, N sin θ = mv²/r (M1 M1), v = {sf(v)} m s⁻¹ (A1). (c) R1. (d) R1.', 6, 'multi_step')
    m = rng.choice([0.10, 0.15, 0.20]); L = rng.choice([0.5, 0.8, 1.0]); th = rng.choice([30, 40, 50])
    r = L * sind(th); T_ = m * g0 / cosd(th); v = math.sqrt(g0 * r * math.tan(math.radians(th)))
    return num(f'A conical pendulum consists of a {m} kg bob on a string of length {L} m moving in a horizontal circle with the string at {th}° to the vertical. (a) Calculate the radius of the circle. (b) Determine the tension in the string. (c) Calculate the speed of the bob. (d) Explain why the string can never be horizontal.',
               f'(a) {sf(r)} m; (b) {sf(T_)} N; (c) {sf(v)} m s⁻¹; (d) the vertical component of tension must balance the weight, which requires θ < 90°.',
               f'(a) r = L sin θ (A1). (b) T cos θ = mg (M1 A1). (c) T sin θ = mv²/r (M1 A1). (d) R1.', 6, 'multi_step')


R.mcqs('ch02-st5', 'C2', (1, 4), [
    ('A stone tied to a string is whirled in a horizontal circle. If the string breaks, the stone moves', 'along the tangent at the point of release', ['radially outwards', 'towards the centre', 'in a spiral'], 'No centripetal force; first law.'),
    ('For a satellite in circular orbit, the centripetal force is provided by', 'the gravitational force of the planet', ['the rocket engines', 'a centrifugal force', 'the satellite’s inertia'], 'Gravity acts towards the centre.'),
    ('A cyclist doubles her speed around the same circular track. Her centripetal acceleration', 'increases by a factor of 4', ['doubles', 'is unchanged', 'halves'], 'a = v²/r.'),
    ('At the top of a vertical circle the tension in a string is least because', 'the weight provides part of the centripetal force', ['the speed is greatest there', 'gravity is weaker there', 'centripetal force is zero there'], 'T + mg = mv²/r.'),
])


def _circ_spec(rng):
    m = 0.050; Mh = rng.uniform(0.18, 0.25); r = 0.60
    Fc = Mh * g0
    Ts = [0.80, 0.90, 1.00, 1.10, 1.20, 1.30]
    # vary r: whirl radius chosen so mv²/r = Mg, i.e. r = Mg T²/(4π² m)
    rs = [round(Fc * T ** 2 / (4 * math.pi ** 2 * m) * rng.uniform(0.98, 1.02), 3) for T in Ts]
    return dict(intro=f'A rubber bung of mass 0.050 kg is whirled in a horizontal circle on a string passing through a glass tube, with a hanging mass M providing the tension. The period T is measured for different radii r. Theory: Mg = 4π²mr/T².',
                xname='T', xunit='s', yname='r', yunit='m', xs=Ts, ys=rs, xfmt=lambda x: f'{x:.2f}', yfmt=lambda y: f'{y:.3f}',
                plot_x=lambda x: x * x, plot_y=lambda y: y, plot_label='r (y) against T² (x)', what='the hanging mass M', what_short='M',
                gunit='m s⁻²', deduce=lambda m_, b_: (m_ * 4 * math.pi ** 2 * 0.050 / g0, 'kg', 'M = 4π²m × gradient/g'))


gradient_fit('ch02-st5', _circ_spec)


# =============================================================================================
# ch03 A.3 Work, energy and power
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('work done', 'the product of a force and the displacement in the direction of the force, W = Fs cos θ'),
           ('joule', 'the work done when a force of 1 N moves its point of application 1 m in the direction of the force'),
           ('work–energy principle', 'the work done by the resultant force on an object equals its change in kinetic energy'),
           ('energy', 'the capacity to do work, a conserved scalar quantity measured in joules'),
           ('area under a force–displacement graph', 'the work done by the force')],
    facts=[('A force of 50 N pulls a sledge 20 m along level snow; the rope is at 30° to the horizontal. What work does the force do?', '866 J', ['1000 J', '500 J', '577 J'], 'W = Fs cos θ = 50 × 20 × cos 30°.'),
           ('No work is done on an object when the force is', 'perpendicular to the displacement', ['parallel to the displacement', 'very large', 'opposite to the displacement'], 'cos 90° = 0.'),
           ('The work done by friction on a sliding box is', 'negative', ['positive', 'zero', 'always equal to its kinetic energy'], 'Friction opposes the displacement.'),
           ('Which of the following is equivalent to 1 J?', '1 N m', ['1 N m⁻¹', '1 kg m s⁻²', '1 W s⁻¹'], 'W = Fs.'),
           ('A weightlifter holds a barbell stationary above her head. The work done on the barbell is', 'zero', ['mgh each second', 'equal to its weight', 'positive and increasing'], 'No displacement.')],
    why=[('Explain why a person carrying a heavy bag horizontally at constant velocity does no work on the bag against gravity.', 'The force from the person is vertical (balancing the weight) while the displacement is horizontal; the angle is 90°, so W = Fs cos 90° = 0.'),
         ('Explain how the work done in stretching a spring can be found from a force–extension graph.', 'Work is the area under the force–displacement graph; for a spring obeying Hooke’s law it is a triangle of area ½Fx = ½kx².'),
         ('Explain, using the work–energy principle, why the braking distance of a car is proportional to the square of its speed.', 'The braking force does work F × s equal to the loss of kinetic energy ½mv²; with constant F, s = mv²/(2F) ∝ v².')],
    contrast=[('work done by a force', 'the force itself', 'A force is a vector push or pull (N); work is the scalar energy transferred when the force moves through a displacement along its direction (J). A large force does no work if there is no displacement.')],
    misc=[('Any force acting on a moving object does work on it.', 'Only the component of force along the displacement does work; a centripetal force, for example, is perpendicular to the motion and does no work.'),
          ('Work and energy have different units because they are different things.', 'Both are measured in joules; work is the amount of energy transferred by a force.'),
          ('Holding a heavy object still is hard work, so a lot of work is done on it.', 'Muscles use chemical energy (internal processes) but no work is done on the object because it does not move.')],
    evaluate=[('The work–energy principle makes Newton’s second law unnecessary.', ['it solves many problems faster (no time or directions needed)', 'it handles varying forces via the area under graphs'], ['it gives no information about time or direction of motion', 'it is itself derived from Newton’s second law', 'friction and internal energy must be accounted for carefully'], 'The two approaches complement each other: energy methods are convenient when time is not needed, but Newton’s laws are more fundamental and give more detail.')],
    extended=[('A 25 kg suitcase is pulled 40 m across an airport floor by a strap at 35° to the horizontal with a tension of 80 N. The friction force is 50 N. (a) Calculate the work done by the tension. (b) Calculate the work done against friction. (c) Determine the final speed if it starts from rest. (d) Explain why the friction force would be smaller if the strap were steeper.', '(a) 80 × 40 × cos 35° = 2620 J; (b) 2000 J; (c) ½ × 25v² = 620 J, v = 7.04 m s⁻¹; (d) a steeper strap has a larger upward component, reducing the normal force and so the friction μN.', 6)],
))


@prob('ch03-st1', d=(1, 5), md=(1, 4), marks=2)
def p_work(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        F_ = rng.choice([40, 60, 80, 120, 150]); s = rng.choice([5, 8, 12, 15, 20, 30]); th = rng.choice([20, 25, 30, 40, 45])
        return dict(stem=f'{who} pulls a sledge {s} m across snow in {city} with a force of {F_} N along a rope at {th}° to the horizontal. Calculate the work done by the pull.',
                    v=F_ * s * cosd(th), unit='J', wrongs=[F_ * s, F_ * s * sind(th), F_ * s / cosd(th)], key=f'W = Fs cos θ (M1) = {F_} × {s} × cos {th}° = {sf(F_ * s * cosd(th))} J (A1).')
    if k == 1:
        m = rng.choice([1200, 1500, 1800]); u = rng.choice([15, 20, 25, 30]); s = rng.choice([40, 50, 60, 75])
        F_ = 0.5 * m * u * u / s
        return dict(stem=f'A {m} kg car travelling at {u} m s⁻¹ stops in {s} m. Use the work–energy principle to calculate the average braking force.',
                    v=F_, unit='N', wrongs=[m * u / s, m * u * u / s, 0.5 * m * u / s], key=f'Fs = ½mv² (M1); F = ½ × {m} × {u}²/{s} = {sf(F_)} N (A1).')
    if k == 2:
        k_ = rng.choice([50, 80, 120, 200, 400]); x = rng.choice([0.02, 0.04, 0.05, 0.08, 0.10])
        return dict(stem=f'A spring of spring constant {k_} N m⁻¹ is stretched by {x * 100:g} cm. Calculate the work done in stretching it.',
                    v=0.5 * k_ * x * x, unit='J', wrongs=[k_ * x * x, k_ * x, 0.5 * k_ * x], key=f'W = area under F–x graph = ½kx² (M1) = {sf(0.5 * k_ * x * x)} J (A1).')
    if k == 3:
        m = rng.choice([0.5, 2.0, 5.0, 10, 20]); h = rng.choice([1.5, 2.0, 3.0, 4.5, 8.0])
        return dict(stem=f'A crane in {city} lifts a {m} kg load vertically at constant speed through {h} m. Calculate the work done by the crane on the load.',
                    v=m * g0 * h, unit='J', wrongs=[m * h, m * g0 * h / 2, m * g0], key=f'At constant speed F = mg (M1); W = mgh = {sf(m * g0 * h)} J (A1).')
    F1 = rng.choice([100, 200, 300]); x1 = rng.choice([0.10, 0.20, 0.30]); F2 = rng.choice([400, 500, 600]); x2 = x1 + rng.choice([0.10, 0.20])
    W = 0.5 * F1 * x1 + 0.5 * (F1 + F2) * (x2 - x1)
    return dict(stem=f'The force on an archer’s arrow rises linearly from 0 to {F1} N over the first {x1} m and then linearly to {F2} N over the next {sf(x2 - x1, 2)} m. Calculate the work done on the arrow.',
                v=W, unit='J', wrongs=[F2 * x2, 0.5 * F2 * x2, F1 * x1 + F2 * (x2 - x1)], key=f'Area = ½ × {F1} × {x1} + ½({F1} + {F2}) × {sf(x2 - x1, 2)} (M1 M1) = {sf(W)} J (A1).', marks=3)


R.mcqs('ch03-st1', 'C2', (1, 4), [
    ('A satellite moves in a circular orbit at constant speed. The work done on it by gravity in one orbit is', 'zero', ['positive', 'negative', 'equal to its kinetic energy'], 'Gravity is perpendicular to the velocity.'),
    ('A box slides down a rough slope at constant speed. Which statement is correct?', 'The work done by gravity equals the work done against friction', ['No work is done on the box', 'The kinetic energy increases', 'Friction does positive work'], 'ΔKE = 0, so the total work is zero.'),
    ('The same force pushes two blocks of different mass from rest through the same distance on a smooth surface. Afterwards the blocks have the same', 'kinetic energy', ['speed', 'momentum', 'acceleration'], 'Work Fs is the same.'),
])


R.facts('ch03-st2', F(
    terms=[('kinetic energy', 'the energy an object has because of its motion, Eₖ = ½mv² = p²/2m'),
           ('gravitational potential energy', 'the energy stored in a mass due to its position in a gravitational field; near Earth ΔE_p = mgΔh'),
           ('elastic potential energy', 'the energy stored in a deformed elastic object, E = ½kx² for a spring obeying Hooke’s law'),
           ('principle of conservation of energy', 'energy cannot be created or destroyed, only transferred from one form or store to another; the total energy of an isolated system is constant'),
           ('mechanical energy', 'the sum of the kinetic and potential energies of a system')],
    facts=[('An object of mass 2.0 kg moves at 3.0 m s⁻¹. What is its kinetic energy?', '9.0 J', ['6.0 J', '18 J', '3.0 J'], 'Eₖ = ½ × 2.0 × 9.0.'),
           ('If the speed of an object triples, its kinetic energy', 'increases by a factor of 9', ['triples', 'increases by a factor of 6', 'increases by a factor of 27'], 'Eₖ ∝ v².'),
           ('A ball is dropped from 5.0 m. Ignoring air resistance, its speed just before landing is', '9.9 m s⁻¹', ['49 m s⁻¹', '7.0 m s⁻¹', '98 m s⁻¹'], 'v = √(2gh).'),
           ('Which expression relates kinetic energy and momentum?', 'Eₖ = p²/2m', ['Eₖ = 2mp', 'Eₖ = p/2m', 'Eₖ = mp²/2'], 'Eₖ = ½mv² = (mv)²/2m.'),
           ('Two springs stretched by the same extension, one with twice the spring constant. The stiffer spring stores', 'twice the energy', ['half the energy', 'four times the energy', 'the same energy'], 'E = ½kx².')],
    why=[('Explain why the speed of a pendulum bob at the bottom of its swing does not depend on its mass.', 'Loss of GPE mgh equals gain of KE ½mv²; mass cancels, so v = √(2gh) depends only on the height.'),
         ('Explain why a bouncing ball rises to a lower height after each bounce.', 'At each bounce some kinetic energy is transferred to internal energy and sound (inelastic deformation), so less is available to convert back into GPE.'),
         ('Explain where the energy goes when a car brakes to a stop.', 'Kinetic energy is transferred by the work done by friction in the brakes to internal energy (heating) of the brake discs and pads, and then dissipated to the surroundings.')],
    contrast=[('gravitational potential energy', 'elastic potential energy', 'GPE is stored due to position in a gravitational field (mgΔh); EPE is stored in the deformation of an elastic material (½kx²). Both can be fully recovered as kinetic energy in ideal systems.')],
    misc=[('Energy is used up when a ball rolls to a stop.', 'Energy is conserved; the kinetic energy is transferred to internal energy of the ball and surface and to sound, i.e. dissipated, not destroyed.'),
          ('A heavier object dropped from the same height lands with greater speed.', 'Both have v = √(2gh) without air resistance; the heavier one has more kinetic energy but the same speed.'),
          ('Gravitational potential energy is always mgh.', 'mgh only gives the change in GPE close to Earth’s surface where g is uniform; for large distances the field varies.')],
    evaluate=[('Pumped-storage hydroelectric schemes are an ideal way to store energy from renewable sources.', ['large capacity, fast response (seconds to minutes)', 'round-trip efficiency about 75–80 %', 'long lifetime'], ['need suitable geography with two reservoirs at different heights', 'large environmental impact on valleys', '20–25 % of energy is lost'], 'They are currently the most effective large-scale storage, but geography, environmental cost and losses limit them; batteries and other stores complement them.')],
    extended=[('A 60 kg skateboarder starts from rest at the top of a 4.0 m high ramp and descends to the bottom, then rises up a second ramp. (a) Calculate the speed at the bottom assuming no energy losses. (b) At the bottom her actual speed is 7.8 m s⁻¹; calculate the energy dissipated. (c) Determine the maximum height she reaches on the second ramp if the same fraction of energy is lost on the way up. (d) Discuss the main causes of the energy loss.', '(a) √(2 × 9.81 × 4.0) = 8.86 m s⁻¹; (b) 2354 J − ½ × 60 × 7.8² = 2354 − 1825 = 529 J; (c) 77.5 % retained each stage: h = 4.0 × 0.775² ≈ 2.4 m; (d) friction in the wheel bearings, rolling resistance and air resistance.', 6)],
))


@prob('ch03-st2', d=(1, 5), md=(1, 4), marks=2)
def p_energy(rng, slot):
    k = rng.randrange(6)
    who, city = who_city(rng)
    if k == 0:
        h = rng.choice([2.0, 3.5, 5.0, 8.0, 12, 20, 35])
        return dict(stem=f'A roller-coaster car starts from rest at the top of a drop of height {h} m. Ignoring friction, calculate its speed at the bottom.',
                    v=math.sqrt(2 * g0 * h), unit='m s⁻¹', wrongs=[2 * g0 * h, math.sqrt(g0 * h), g0 * h / 2], key=f'mgh = ½mv² (M1); v = √(2gh) = {sf(math.sqrt(2 * g0 * h))} m s⁻¹ (A1).')
    if k == 1:
        k_ = rng.choice([200, 400, 600, 800, 1200]); x = rng.choice([0.03, 0.05, 0.08, 0.10]); m = rng.choice([0.02, 0.05, 0.10, 0.20])
        v = x * math.sqrt(k_ / m)
        return dict(stem=f'A toy launcher compresses a spring of spring constant {k_} N m⁻¹ by {x * 100:g} cm and fires a {m * 1000:g} g ball horizontally. Calculate the launch speed.',
                    v=v, unit='m s⁻¹', wrongs=[k_ * x / m, x * math.sqrt(2 * k_ / m), math.sqrt(k_ * x / m)], key=f'½kx² = ½mv² (M1); v = x√(k/m) = {sf(v)} m s⁻¹ (A1).')
    if k == 2:
        L = rng.choice([0.8, 1.0, 1.5, 2.0]); th = rng.choice([20, 30, 40, 50, 60])
        h = L * (1 - cosd(th)); v = math.sqrt(2 * g0 * h)
        return dict(stem=f'A pendulum of length {L} m is pulled aside until the string makes {th}° with the vertical and released. Calculate the speed of the bob at the lowest point.',
                    v=v, unit='m s⁻¹', wrongs=[math.sqrt(2 * g0 * L), math.sqrt(2 * g0 * L * sind(th)), math.sqrt(2 * g0 * L * cosd(th))], key=f'h = L(1 − cos θ) = {sf(h)} m (M1); v = √(2gh) = {sf(v)} m s⁻¹ (A1).', marks=3)
    if k == 3:
        m = rng.choice([0.5, 1.0, 2.0, 5.0]); p = rng.choice([4.0, 6.0, 10, 15])
        return dict(stem=f'An object of mass {m} kg has momentum {p} kg m s⁻¹. Calculate its kinetic energy.',
                    v=p * p / (2 * m), unit='J', wrongs=[p * p / m, p / (2 * m), p * p * m / 2], key=f'Eₖ = p²/2m (M1) = {sf(p * p / (2 * m))} J (A1).')
    if k == 4:
        m = rng.choice([50, 60, 70, 80]); h = rng.choice([3.0, 5.0, 8.0, 10]); v = rng.choice([6.0, 7.5, 9.0, 11])
        loss = m * g0 * h - 0.5 * m * v * v
        if loss <= 0:
            return None
        return dict(stem=f'{who} (mass {m} kg) slides from rest down a water slide in {city} that drops {h} m and reaches the bottom at {v} m s⁻¹. Calculate the energy dissipated by friction.',
                    v=loss, unit='J', wrongs=[m * g0 * h, 0.5 * m * v * v, m * g0 * h + 0.5 * m * v * v], key=f'GPE lost = {sf(m * g0 * h)} J; KE gained = {sf(0.5 * m * v * v)} J (M1); dissipated = {sf(loss)} J (A1).')
    u = rng.choice([8.0, 10, 12, 15]); h = rng.choice([2.0, 3.0, 4.0])
    if u * u <= 2 * g0 * h:
        return None
    v = math.sqrt(u * u - 2 * g0 * h)
    return dict(stem=f'A cyclist free-wheels at {u} m s⁻¹ up a hill {h} m high. Ignoring resistive forces, calculate the speed at the top.',
                v=v, unit='m s⁻¹', wrongs=[u - math.sqrt(2 * g0 * h), math.sqrt(u * u + 2 * g0 * h), u - g0 * h / u], key=f'½mu² = ½mv² + mgh (M1); v = √(u² − 2gh) = {sf(v)} m s⁻¹ (A1).')


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step')
def c4_bungee(rng, slot):
    m = rng.choice([60, 70, 80]); L = rng.choice([15, 20, 25]); k_ = rng.choice([80, 100, 120])
    # m g (L + x) = 1/2 k x^2
    a, b, c = 0.5 * k_, -m * g0, -m * g0 * L
    x = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    vmax_x = m * g0 / k_
    vmax = math.sqrt(2 * g0 * (L + vmax_x) - k_ * vmax_x ** 2 / m)
    return num(f'A {m} kg bungee jumper falls from a bridge on an elastic cord of unstretched length {L} m and spring constant {k_} N m⁻¹. Ignore air resistance and the mass of the cord. (a) Calculate the speed when the cord just becomes taut. (b) Determine the maximum extension of the cord. (c) Show that the maximum speed occurs when the extension is {sf(vmax_x)} m and calculate it. (d) Discuss whether the model is realistic.',
               f'(a) {sf(math.sqrt(2 * g0 * L))} m s⁻¹; (b) {sf(x)} m; (c) maximum speed where kx = mg: {sf(vmax)} m s⁻¹; (d) air resistance and energy losses in the cord reduce the extension; real cords do not obey Hooke’s law exactly.',
               f'(a) √(2gL) (A1). (b) mg(L + x) = ½kx² (M1), solve quadratic (A1). (c) a = 0 when kx = mg (M1), energy equation gives v (A1). (d) R1.', 6, 'multi_step')


R.mcqs('ch03-st2', 'C2', (1, 4), [
    ('Two balls of different mass are released from the same height on frictionless ramps of different shapes. At the bottom they have the same', 'speed', ['kinetic energy', 'momentum', 'time of descent'], 'v = √(2gh) independent of mass and path.'),
    ('A ball is thrown upwards. Ignoring air resistance, which graph shape describes its kinetic energy against height?', 'A straight line decreasing with height', ['A parabola', 'A horizontal line', 'An exponential decay'], 'Eₖ = E_total − mgh.'),
    ('The extension of a spring is doubled. The elastic potential energy stored', 'increases by a factor of 4', ['doubles', 'halves', 'is unchanged'], 'E ∝ x².'),
])


R.facts('ch03-st3', F(
    terms=[('power', 'the rate of doing work or transferring energy, P = ΔW/Δt, measured in watts'),
           ('watt', 'a rate of energy transfer of one joule per second'),
           ('efficiency', 'the ratio of useful output energy (or power) to total input energy (or power)'),
           ('kilowatt-hour', 'the energy transferred by a 1 kW device in one hour, 3.6 × 10⁶ J'),
           ('P = Fv', 'the power delivered by a force F acting on an object moving at velocity v in the direction of the force')],
    facts=[('A motor lifts a 50 kg load through 10 m in 20 s. What is the useful power output?', '245 W', ['25 W', '500 W', '4905 W'], 'P = mgh/t.'),
           ('A car moves at constant velocity 25 m s⁻¹ against a total resistive force of 800 N. The power output of the engine is', '20 kW', ['32 W', '3.2 kW', '800 kW'], 'P = Fv.'),
           ('Efficiency can never exceed 100 % because', 'energy is conserved and some is always dissipated', ['power is limited by voltage', 'work is always negative', 'machines have mass'], 'Output ≤ input.'),
           ('Which is the unit of power?', 'J s⁻¹', ['J s', 'N s', 'kg m s⁻¹'], 'Watt = J s⁻¹.'),
           ('A device has an efficiency of 40 % and an input power of 500 W. The power wasted is', '300 W', ['200 W', '500 W', '1250 W'], 'Useful = 200 W.')],
    why=[('Explain why a car has a maximum speed on a level road even with the accelerator fully pressed.', 'Drag increases with speed while the maximum engine power is fixed; at top speed the driving force P/v equals the resistive force, so the resultant force and acceleration are zero.'),
         ('Explain why LED lamps are replacing filament lamps.', 'For the same light output LEDs need far less input power because they have a much higher efficiency (less energy dissipated as internal energy), reducing energy cost and emissions.'),
         ('Explain why the power needed to drive at high speed rises steeply with speed.', 'At high speed drag ∝ v², and P = Fv, so the power needed to overcome drag ∝ v³.')],
    contrast=[('energy', 'power', 'Energy is the capacity to do work, measured in joules; power is the rate at which energy is transferred, measured in watts (J s⁻¹).')],
    misc=[('A more powerful machine always does more work.', 'Power is the rate of doing work; a less powerful machine can do the same work if it operates for longer.'),
          ('An efficient machine produces more energy than it receives.', 'Efficiency compares useful output with input; it is always less than 100 % because energy is conserved and some is dissipated.'),
          ('Kilowatt-hours measure power.', 'A kWh is a unit of energy (1 kW for 1 h = 3.6 MJ), used for electricity bills.')],
    evaluate=[('Electric cars are more efficient than petrol cars, so they always produce lower carbon emissions.', ['electric motors are ~90 % efficient against ~25–30 % for petrol engines', 'regenerative braking recovers energy', 'no tailpipe emissions'], ['emissions depend on how the electricity is generated (coal-heavy grids)', 'battery manufacture has a significant carbon footprint', 'transmission and charging losses'], 'They are more efficient at the point of use, and usually lower in lifetime emissions, but the advantage depends strongly on the electricity mix and battery production.')],
    extended=[('An electric motor in a building lift raises a 900 kg car with passengers through 36 m in 24 s at constant speed. The motor draws 21 kW of electrical power. (a) Calculate the useful power output. (b) Calculate the efficiency. (c) Calculate the energy dissipated in the trip. (d) Suggest two ways the lift system could be made more efficient.', '(a) P = mgh/t = 900 × 9.81 × 36/24 = 13.2 kW; (b) 13.2/21 = 63 %; (c) (21 − 13.2) × 24 = 186 kJ; (d) use a counterweight; regenerative drives; lubricate/low-friction bearings; lighter cars.', 6)],
))


@prob('ch03-st3', d=(1, 5), md=(1, 4), marks=2)
def p_power(rng, slot):
    k = rng.randrange(6)
    who, city = who_city(rng)
    if k == 0:
        m = rng.choice([50, 60, 70, 80]); h = rng.choice([3.0, 4.5, 6.0, 9.0]); t = rng.choice([4.0, 5.0, 6.0, 8.0])
        return dict(stem=f'{who} (mass {m} kg) runs up a flight of stairs of vertical height {h} m in {t} s at a school in {city}. Calculate the useful power developed.',
                    v=m * g0 * h / t, unit='W', wrongs=[m * h / t, m * g0 * h * t, m * g0 / t], key=f'P = mgh/t (M1) = {sf(m * g0 * h / t)} W (A1).')
    if k == 1:
        F_ = rng.choice([400, 600, 800, 1200, 2500]); v = rng.choice([15, 20, 25, 30, 33])
        return dict(stem=f'A car moves at a constant {v} m s⁻¹ on a level motorway against a total resistive force of {F_} N. Calculate the power output of the engine.',
                    v=F_ * v, unit='W', wrongs=[F_ / v, F_ * v * v, 0.5 * F_ * v], key=f'At constant velocity driving force = resistive force (M1); P = Fv = {sf(F_ * v)} W (A1).')
    if k == 2:
        P = rng.choice([60e3, 80e3, 100e3, 150e3]); F_ = rng.choice([2000, 2500, 3000, 4000])
        return dict(stem=f'The maximum power output of a car engine is {P / 1000:g} kW. At top speed the total resistive force is {F_} N. Calculate the top speed.',
                    v=P / F_, unit='m s⁻¹', wrongs=[P * F_ / 1e8, F_ / P * 1e3, math.sqrt(P / F_)], key=f'At top speed P = Fv (M1); v = P/F = {sf(P / F_)} m s⁻¹ (A1).')
    if k == 3:
        m = rng.choice([100, 200, 300, 500]); h = rng.choice([5, 10, 15, 20]); t = rng.choice([10, 20, 30]); eff = rng.choice([0.40, 0.55, 0.60, 0.75])
        Pin = m * g0 * h / t / eff
        return dict(stem=f'An electric winch with an efficiency of {int(eff * 100)} % lifts a {m} kg load through {h} m in {t} s. Calculate the electrical input power.',
                    v=Pin, unit='W', wrongs=[m * g0 * h / t, m * g0 * h / t * eff, m * h / t / eff], key=f'Useful P = mgh/t = {sf(m * g0 * h / t)} W (M1); input = useful/efficiency = {sf(Pin)} W (A1).')
    if k == 4:
        Pin = rng.choice([40, 60, 100, 1500, 2000]); Pout = Pin * rng.choice([0.08, 0.15, 0.35, 0.85, 0.92])
        dev = 'filament lamp' if Pin <= 100 else 'kettle'
        return dict(stem=f'A {dev} rated at {Pin} W delivers {sf(Pout)} W of useful power. Calculate its efficiency as a percentage.',
                    v=100 * Pout / Pin, unit='%', wrongs=[100 * Pin / Pout, 100 - 100 * Pout / Pin, Pout / Pin], key=f'Efficiency = useful/total × 100 (M1) = {sf(100 * Pout / Pin)} % (A1).')
    P = rng.choice([1.5, 2.0, 2.5, 3.0]); t = rng.choice([4, 6, 8]); price = rng.choice([0.15, 0.20, 0.28, 0.32])
    return dict(stem=f'A {P} kW electric heater in a flat in {city} runs for {t} hours a day. Calculate the energy transferred per day in joules.',
                v=P * 1000 * t * 3600, unit='J', wrongs=[P * t, P * 1000 * t, P * t * 3600], key=f'E = Pt = {P * 1000:g} W × {t * 3600} s (M1) = {sf(P * 1000 * t * 3600)} J ({P * t:g} kWh, costing {sf(P * t * price, 2)} at {price} per kWh) (A1).')


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def c4_cyclist_power(rng, slot):
    k = rng.randrange(2)
    if k == 0:
        cd = rng.choice([0.25, 0.30, 0.35]); v = rng.choice([10, 12, 14])
        # drag = 1/2 rho Cd A v^2 with rho = 1.2
        Fd = 0.5 * 1.2 * cd * v * v; P = Fd * v
        return num(f'The drag force on a racing cyclist is F = ½ρC_dAv², where ρ = 1.2 kg m⁻³ and C_dA = {cd} m². (a) Calculate the drag at {v} m s⁻¹. (b) Determine the power needed to overcome drag at this speed. (c) Show that the power needed is proportional to v³ and calculate the power needed at {v + 2} m s⁻¹. (d) Evaluate why professional cyclists ride in a tight group (peloton).',
                   f'(a) {sf(Fd)} N; (b) {sf(P)} W; (c) P ∝ v³: {sf(P * ((v + 2) / v) ** 3)} W; (d) riders behind experience less drag (smaller effective C_dA), saving a large fraction of power, so the team can ride faster for longer.',
                   f'(a) A1. (b) P = Fv (M1 A1). (c) P = ½ρC_dAv³ (M1), value (A1). (d) R1.', 6, 'multi_step')
    m = rng.choice([1200, 1400]); P = rng.choice([50e3, 60e3]); th = rng.choice([4, 5, 6]); Fr = rng.choice([500, 600])
    Fg = m * g0 * sind(th); v = P / (Fg + Fr)
    return num(f'A {m} kg car with a maximum power output of {P / 1000:g} kW climbs a steady hill inclined at {th}° to the horizontal. The resistive forces total {Fr} N. (a) Calculate the component of the weight down the slope. (b) Determine the maximum steady speed up the hill. (c) Calculate the rate of increase of gravitational potential energy at this speed. (d) Explain why the car can travel faster on the level.',
               f'(a) {sf(Fg)} N; (b) {sf(v)} m s⁻¹; (c) {sf(Fg * v)} W; (d) on the level the engine only works against resistive forces, so v = P/F_r is larger.',
               f'(a) mg sin θ (A1). (b) P = (mg sin θ + F_r)v (M1 A1). (c) mg sin θ × v (A1). (d) R1.', 5, 'multi_step')


R.mcqs('ch03-st3', 'C2', (1, 4), [
    ('Two cranes lift identical loads to the same height; crane X takes half the time of crane Y. Which is correct?', 'X develops twice the power of Y', ['X does twice the work of Y', 'Both develop the same power', 'Y develops twice the power of X'], 'Same work, half the time.'),
    ('A car travels at constant speed up a hill. The engine’s power is used to', 'increase GPE and overcome resistive forces', ['increase kinetic energy only', 'overcome friction only', 'increase kinetic and potential energy only'], 'KE is constant.'),
    ('A motor has an efficiency of 80 %. For every 100 J of electrical energy supplied,', '20 J is dissipated, mainly as internal energy', ['80 J is dissipated', '20 J of useful work is done', '100 J of useful work is done'], 'Useful = 80 J.'),
])


R.facts('ch03-st4', F(
    terms=[('energy density', 'the energy released per unit volume of a fuel, in J m⁻³ (often MJ L⁻¹)'),
           ('specific energy', 'the energy released per unit mass of a fuel, in J kg⁻¹ (often MJ kg⁻¹)'),
           ('fossil fuel', 'a fuel formed from the remains of ancient organisms, such as coal, oil and natural gas'),
           ('renewable energy source', 'a source that is replenished naturally on a human timescale, such as solar, wind and hydroelectric'),
           ('Sankey diagram', 'a flow diagram in which the widths of the arrows are proportional to the amounts of energy transferred')],
    facts=[('Which fuel has the highest specific energy?', 'Hydrogen (≈ 142 MJ kg⁻¹)', ['Petrol (≈ 46 MJ kg⁻¹)', 'Coal (≈ 30 MJ kg⁻¹)', 'Wood (≈ 16 MJ kg⁻¹)'], 'Hydrogen releases the most energy per kg.'),
           ('Hydrogen has a high specific energy but a low energy density because', 'its density is very low, even when compressed or liquefied', ['it releases little energy per kg', 'it is radioactive', 'its combustion is endothermic'], 'Energy density = specific energy × density.'),
           ('In a Sankey diagram, the width of each arrow represents', 'the amount of energy transferred', ['the efficiency', 'the time taken', 'the type of energy'], 'Arrow width ∝ energy.'),
           ('Which is a unit of energy density?', 'J m⁻³', ['J kg⁻¹', 'W m⁻²', 'kg m⁻³'], 'Energy per unit volume.'),
           ('Uranium-235 used in nuclear reactors has a specific energy roughly', 'a million times that of fossil fuels', ['ten times that of fossil fuels', 'equal to that of fossil fuels', 'smaller than that of fossil fuels'], '≈ 8 × 10⁷ MJ kg⁻¹ vs ≈ 50 MJ kg⁻¹.')],
    why=[('Explain why liquid fuels such as petrol and kerosene remain the dominant fuels for aviation.', 'Aircraft are limited by both mass and volume; petrol/kerosene combine a high specific energy (~43–46 MJ kg⁻¹) with a high energy density (~35 MJ L⁻¹), unlike batteries or hydrogen.'),
         ('Explain why a coal-fired power station needs a continuous supply of a large mass of coal.', 'Coal has a modest specific energy (~30 MJ kg⁻¹) and the station is only about 35 % efficient, so a large mass of fuel must be burned each second to supply hundreds of megawatts.'),
         ('Explain why batteries in electric vehicles add a large mass compared with a petrol tank for the same range.', 'Lithium-ion batteries have a specific energy of only about 0.9 MJ kg⁻¹, around fifty times lower than petrol, so even allowing for higher motor efficiency the batteries are much heavier.')],
    contrast=[('specific energy', 'energy density', 'Specific energy is energy per unit mass (J kg⁻¹); energy density is energy per unit volume (J m⁻³). A fuel can be high in one and low in the other, e.g. hydrogen.')],
    misc=[('A fuel with a high specific energy must also have a high energy density.', 'Energy density = specific energy × density; hydrogen has a very high specific energy but, being very low in density, a low energy density.'),
          ('Renewable energy sources produce no environmental impact.', 'They avoid fuel combustion, but manufacture, land use, habitat change (dams) and materials mining have impacts.'),
          ('All the energy released by burning fuel in a power station becomes electrical energy.', 'Typical efficiencies are 35–55 %; most energy is transferred to the surroundings as thermal energy in cooling towers and flue gases.')],
    evaluate=[('Hydrogen is the ideal fuel of the future.', ['highest specific energy of any chemical fuel', 'only water is produced when it is burned or used in a fuel cell'], ['low energy density requires high-pressure or cryogenic storage', 'most hydrogen is currently made from natural gas, releasing CO₂', 'leaks and flammability raise safety issues'], 'Hydrogen is promising where it can be made with renewable electricity, but storage, production and infrastructure problems mean it will complement rather than replace other energy carriers.'),
              ('Nuclear power is the best way to reduce carbon emissions from electricity generation.', ['very high specific energy of uranium means little fuel', 'low lifecycle CO₂ emissions', 'reliable baseload output'], ['long-lived radioactive waste', 'high construction costs and long build times', 'public concern after accidents (Chernobyl, Fukushima)'], 'Nuclear can provide large amounts of low-carbon power, but cost, waste and public acceptance mean it is one part of a mix with renewables and storage.')],
    extended=[('A gas-fired power station has an output of 800 MW and an overall efficiency of 50 %. Natural gas has a specific energy of 55 MJ kg⁻¹ and a density of 0.72 kg m⁻³. (a) Calculate the input power. (b) Calculate the mass of gas burned per second. (c) Calculate the volume of gas burned per second. (d) Draw a labelled Sankey diagram for the station.', '(a) 1600 MW; (b) 1.6 × 10⁹/5.5 × 10⁷ = 29.1 kg s⁻¹; (c) 29.1/0.72 = 40.4 m³ s⁻¹; (d) input 1600 MW, 800 MW electrical, 800 MW thermal energy to surroundings (arrow widths equal).', 6)],
))

FUELS = [('petrol', 46, 34), ('diesel', 45, 38), ('ethanol', 30, 24), ('kerosene (jet fuel)', 43, 35), ('liquid hydrogen', 142, 10), ('natural gas', 55, 0.040), ('coal', 30, None), ('wood', 16, None)]


@prob('ch03-st4', d=(1, 5), md=(1, 4), marks=2)
def p_fuel(rng, slot):
    k = rng.randrange(5)
    city = rng.choice(CITIES)
    if k == 0:
        f, se, ed = pick(rng, [x for x in FUELS if x[2] and x[2] > 1])
        V = rng.choice([40, 50, 60, 70])
        return dict(stem=f'A car’s tank holds {V} L of {f}, which has an energy density of {ed} MJ L⁻¹. Calculate the chemical energy stored in a full tank.',
                    v=V * ed * 1e6, unit='J', wrongs=[V * se * 1e6, V * ed * 1e3, V * ed], key=f'E = V × energy density = {V} × {ed} MJ (M1) = {sf(V * ed * 1e6)} J (A1).')
    if k == 1:
        P = rng.choice([500, 600, 800, 1000, 1200]); eff = rng.choice([0.35, 0.38, 0.40])
        f, se, _ = pick(rng, [x for x in FUELS if x[0] in ('coal', 'natural gas', 'wood')])
        m = P * 1e6 / eff / (se * 1e6)
        return dict(stem=f'A {P} MW power station near {city} burns {f} (specific energy {se} MJ kg⁻¹) with an overall efficiency of {int(eff * 100)} %. Calculate the mass of fuel burned each second.',
                    v=m, unit='kg s⁻¹', wrongs=[P / se, P / se * eff, P * eff / se * 10], key=f'Input power = {P}/{eff} = {sf(P / eff)} MW (M1); m = {sf(P / eff)} × 10⁶/({se} × 10⁶) = {sf(m)} kg s⁻¹ (A1).')
    if k == 2:
        f, se, ed = pick(rng, [x for x in FUELS if x[2] and x[2] > 1])
        rho = ed / se
        return dict(stem=f'{f[0].upper() + f[1:]} has a specific energy of {se} MJ kg⁻¹ and an energy density of {ed} MJ L⁻¹. Calculate its density in kg m⁻³.',
                    v=rho * 1000, unit='kg m⁻³', wrongs=[se / ed * 1000, rho, ed * se], key=f'Density = energy density / specific energy = {ed}/{se} kg L⁻¹ (M1) = {sf(rho * 1000)} kg m⁻³ (A1).')
    if k == 3:
        E_ = rng.choice([200, 300, 500, 800]); se = 46; eff = rng.choice([0.25, 0.28, 0.30])
        return dict(stem=f'A petrol engine of efficiency {int(eff * 100)} % must deliver {E_} MJ of useful work on a journey. Petrol has a specific energy of 46 MJ kg⁻¹. Calculate the mass of petrol needed.',
                    v=E_ / eff / se, unit='kg', wrongs=[E_ / se, E_ * eff / se, E_ / (eff * 34)], key=f'Energy input = {E_}/{eff} MJ (M1); m = {sf(E_ / eff)}/46 = {sf(E_ / eff / se)} kg (A1).')
    se_b = 0.90; E_kwh = rng.choice([50, 60, 75, 100])
    m = E_kwh * 3.6 / se_b
    return dict(stem=f'An electric car battery stores {E_kwh} kWh. Lithium-ion cells have a specific energy of about 0.90 MJ kg⁻¹. Estimate the mass of the battery cells.',
                v=m, unit='kg', wrongs=[E_kwh / se_b, E_kwh * 3.6e3 / se_b / 1000 * 10, E_kwh * 3.6 / 46], key=f'E = {E_kwh} × 3.6 MJ = {sf(E_kwh * 3.6)} MJ (M1); m = E/0.90 = {sf(m)} kg (A1).')


R.mcqs('ch03-st4', 'C2', (1, 4), [
    ('Fuel X has a specific energy twice that of fuel Y, but its density is a quarter of Y’s. The ratio of energy densities X : Y is', '1 : 2', ['2 : 1', '8 : 1', '1 : 8'], 'Energy density = specific energy × density = 2 × ¼.'),
    ('Which energy source is renewable?', 'Wind', ['Natural gas', 'Uranium', 'Coal'], 'Replenished naturally.'),
    ('The main reason a thermal power station is only about 35–40 % efficient is that', 'a large amount of thermal energy must be transferred to the surroundings', ['the generator is very inefficient', 'fuel does not burn completely', 'electrical cables have high resistance'], 'Thermodynamic limit on heat engines.'),
])


def _spring_h_spec(rng):
    k_ = rng.uniform(150, 300); m = 0.050
    xs_ = [0.010, 0.015, 0.020, 0.025, 0.030, 0.035]
    hs = [round(k_ * x * x / (2 * m * g0) * rng.uniform(0.97, 1.03), 3) for x in xs_]
    return dict(intro='A spring launcher fires a 0.050 kg ball vertically upwards. The spring is compressed by x and the maximum height h reached by the ball above its release point is measured. Theory (no losses): ½kx² = mgh.',
                xname='x', xunit='m', yname='h', yunit='m', xs=xs_, ys=hs, xfmt=lambda a: f'{a:.3f}', yfmt=lambda b: f'{b:.3f}',
                plot_x=lambda a: a * a, plot_y=lambda b: b, plot_label='h (y) against x² (x)', what='the spring constant k', what_short='k',
                gunit='m⁻¹', deduce=lambda m_, b_: (m_ * 2 * 0.050 * g0, 'N m⁻¹', 'k = 2mg × gradient'))


gradient_fit('ch03-st2', _spring_h_spec)


def _power_spec(rng):
    eff = rng.uniform(0.25, 0.45); V = 6.0
    ms = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
    h = 0.80
    Is = [round(m_ * g0 * h / (eff * V * 2.0) * rng.uniform(0.97, 1.03) + 0.0, 3) for m_ in ms]
    return dict(intro='A small electric motor (supply 6.0 V) lifts masses m through 0.80 m in 2.0 s at constant speed. The current I is recorded for each mass. Theory: useful power mgh/t = efficiency × VI.',
                xname='m', xunit='kg', yname='I', yunit='A', xs=ms, ys=Is, xfmt=lambda a: f'{a:.2f}', yfmt=lambda b: f'{b:.3f}',
                plot_x=lambda a: a, plot_y=lambda b: b, plot_label='I (y) against m (x)', what='the efficiency of the motor', what_short='the efficiency',
                gunit='A kg⁻¹', deduce=lambda m_, b_: (g0 * 0.80 / (2.0 * 6.0 * m_), '', 'efficiency = gh/(tV × gradient)'))


gradient_fit('ch03-st3', _power_spec)


# =============================================================================================
# ch04 A.4 Rigid body mechanics (HL)
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('torque', 'the turning effect of a force about an axis, τ = Fr sin θ, where r is the distance from the axis to the point of application'),
           ('couple', 'a pair of equal, opposite, parallel forces whose lines of action do not coincide, producing a torque but no resultant force'),
           ('rotational equilibrium', 'the state in which the resultant torque on a body about any axis is zero'),
           ('centre of mass', 'the point at which the whole mass of a body may be considered to be concentrated'),
           ('principle of moments', 'for a body in rotational equilibrium, the sum of clockwise moments about any point equals the sum of anticlockwise moments')],
    facts=[('What is the SI unit of torque?', 'N m', ['N m⁻¹', 'J s', 'kg m s⁻¹'], 'Force × distance.'),
           ('A 20 N force acts at the end of a 0.50 m spanner, at 90° to it. The torque is', '10 N m', ['40 N m', '0.025 N m', '20 N m'], 'τ = Fr.'),
           ('For a rigid body to be in complete equilibrium,', 'both the resultant force and the resultant torque must be zero', ['only the resultant force must be zero', 'only the resultant torque must be zero', 'it must be at rest'], 'Translational and rotational equilibrium.'),
           ('A couple acting on a free body produces', 'angular acceleration but no linear acceleration of the centre of mass', ['linear acceleration only', 'no effect', 'both linear and angular acceleration'], 'Resultant force zero, torque non-zero.'),
           ('Door handles are placed far from the hinges because', 'a larger perpendicular distance gives a larger torque for the same force', ['the door is lighter there', 'the force is larger there', 'friction is smaller there'], 'τ = Fr.')],
    why=[('Explain why a long-handled wrench makes it easier to undo a tight nut.', 'Torque = force × perpendicular distance; a longer handle increases the distance, so the required torque is achieved with a smaller force.'),
         ('Explain why a tall, narrow vehicle is more likely to topple on a bend than a low, wide one.', 'It topples when the line of action of the resultant force passes outside the base; a high centre of mass and narrow base make this happen at a smaller sideways force.'),
         ('Explain why the position of the axis does not matter when taking moments for a body in equilibrium.', 'If the resultant force is zero and the resultant torque is zero about one point, it is zero about every point, so any convenient point (often through an unknown force) can be chosen.')],
    contrast=[('a torque', 'a couple', 'A torque is the turning effect of any force about an axis; a couple is a specific pair of equal and opposite forces that produces a pure torque with no resultant force.')],
    misc=[('A body in equilibrium must have no forces acting on it.', 'Forces can act; equilibrium requires the resultant force and resultant torque to be zero.'),
          ('Torque depends only on the size of the force.', 'Torque also depends on the perpendicular distance from the axis to the line of action (τ = Fr sin θ).'),
          ('The centre of mass of an object must lie within the material of the object.', 'It can lie outside, for example the centre of mass of a ring or a boomerang is in empty space.')],
    evaluate=[('Cranes can lift any load as long as their counterweight is heavy enough.', ['a larger counterweight balances a larger load moment'], ['the structure, cable and foundations have limited strength', 'an unloaded crane with a huge counterweight could topple backwards', 'wind loads add torque'], 'Counterweights extend capacity, but structural strength, stability when unloaded and wind limit the safe load.')],
    extended=[('A uniform 6.0 m plank of weight 300 N rests on two supports, one at each end. A 700 N painter stands 1.5 m from the left end. (a) Draw the forces on the plank. (b) Determine the force from each support. (c) The right support is moved 1.0 m inwards. Calculate how far to the right of this support the painter can walk before the plank tips. (d) Explain why the support forces change as the painter walks.', '(a) weight 300 N at centre, 700 N at 1.5 m, two upward reactions; (b) moments about left: R_R × 6 = 300 × 3 + 700 × 1.5, R_R = 325 N, R_L = 675 N; (c) tipping about the right support (5.0 m): 700x = 300 × 2.0, x = 0.86 m; (d) the moment of the painter’s weight about each support changes with position.', 6)],
))


@prob('ch04-st1', d=(1, 5), md=(1, 4), marks=2)
def p_torque(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        F_ = rng.choice([30, 50, 80, 120, 200]); r = rng.choice([0.20, 0.25, 0.30, 0.40]); th = rng.choice([30, 45, 60, 70, 90])
        return dict(stem=f'{who} applies a force of {F_} N to a wheel brace of length {r} m at {th}° to the handle. Calculate the torque about the nut.',
                    v=F_ * r * sind(th), unit='N m', wrongs=[F_ * r * cosd(th) if th != 90 else F_ * r / 2, F_ * r if th != 90 else F_ / r, F_ / r * sind(th)], key=f'τ = Fr sin θ (M1) = {F_} × {r} × sin {th}° = {sf(F_ * r * sind(th))} N m (A1).')
    if k == 1:
        m1 = rng.choice([20, 25, 30, 35]); d1 = rng.choice([1.0, 1.2, 1.5, 1.8]); m2 = rng.choice([40, 45, 50, 60])
        return dict(stem=f'On a seesaw in a park in {city}, a {m1} kg child sits {d1} m from the pivot. Calculate the distance from the pivot on the other side at which a {m2} kg child must sit to balance it.',
                    v=m1 * d1 / m2, unit='m', wrongs=[m2 * d1 / m1, d1, m1 / m2], key=f'Principle of moments: {m1}g × {d1} = {m2}g × d (M1); d = {sf(m1 * d1 / m2)} m (A1).')
    if k == 2:
        L = rng.choice([2.0, 3.0, 4.0, 5.0]); W = rng.choice([100, 150, 200, 300]); P = rng.choice([200, 400, 500, 600]); x = rng.choice([0.5, 1.0, 1.5])
        if x >= L:
            return None
        Rr = (W * L / 2 + P * x) / L
        return dict(stem=f'A uniform beam of length {L} m and weight {W} N rests horizontally on supports at its ends. A {P} N load is placed {x} m from the left end. Calculate the force exerted by the right-hand support.',
                    v=Rr, unit='N', wrongs=[W + P - Rr, (W + P) / 2, P * x / L], key=f'Moments about the left support: R × {L} = {W} × {L / 2:g} + {P} × {x} (M1); R = {sf(Rr)} N (A1).', marks=3)
    if k == 3:
        F_ = rng.choice([5.0, 8.0, 10, 15]); d = rng.choice([0.20, 0.30, 0.40, 0.50])
        return dict(stem=f'A driver turns a steering wheel of diameter {d} m by applying equal and opposite tangential forces of {F_} N with each hand at opposite ends of a diameter. Calculate the torque of the couple.',
                    v=F_ * d, unit='N m', wrongs=[F_ * d / 2, 2 * F_ * d, F_ / d], key=f'Torque of couple = F × separation (M1) = {F_} × {d} = {sf(F_ * d)} N m (A1).')
    W = rng.choice([200, 300, 400]); L = rng.choice([4.0, 5.0, 6.0]); th = rng.choice([50, 60, 65, 70])
    # ladder against smooth wall: wall force = W/(2 tan th)
    Fw = W / (2 * math.tan(math.radians(th)))
    return dict(stem=f'A uniform ladder of weight {W} N and length {L} m leans against a smooth vertical wall, making {th}° with the ground. Calculate the horizontal force exerted by the wall on the ladder.',
                v=Fw, unit='N', wrongs=[W / 2, W * math.tan(math.radians(th)) / 2, W / math.tan(math.radians(th))], key=f'Moments about the foot: F_w L sin θ = W (L/2) cos θ (M1); F_w = W/(2 tan θ) = {sf(Fw)} N (A1).', marks=3)


R.mcqs('ch04-st1', 'C2', (1, 4), [
    ('A uniform metre rule balances at its 50 cm mark. A 0.20 N weight is hung at the 10 cm mark. Where must a 0.40 N weight be hung to restore balance?', 'At the 70 cm mark', ['At the 90 cm mark', 'At the 80 cm mark', 'At the 60 cm mark'], '0.20 × 40 = 0.40 × 20.'),
    ('Which change makes a bus more stable against toppling?', 'Lowering its centre of mass', ['Raising its centre of mass', 'Narrowing its wheelbase', 'Loading the roof rack'], 'Toppling occurs when the line of action leaves the base.'),
    ('A force passes through the axis of rotation of a wheel. Its torque about that axis is', 'zero', ['maximum', 'equal to F × radius', 'negative'], 'Perpendicular distance zero.'),
])


R.facts('ch04-st2', F(
    terms=[('angular displacement', 'the angle in radians through which a body rotates about an axis'),
           ('angular velocity', 'the rate of change of angular displacement, ω = Δθ/Δt, in rad s⁻¹'),
           ('angular acceleration', 'the rate of change of angular velocity, α = Δω/Δt, in rad s⁻²'),
           ('uniform angular acceleration', 'constant angular acceleration, for which ω = ω₀ + αt and θ = ω₀t + ½αt²'),
           ('tangential speed', 'the linear speed of a point on a rotating body, v = ωr')],
    facts=[('A wheel turns through 3 complete revolutions. Its angular displacement is', '6π rad', ['3 rad', '3π rad', '1080 rad'], '1 rev = 2π rad.'),
           ('Which equation is the rotational analogue of v² = u² + 2as?', 'ω² = ω₀² + 2αθ', ['ω = ω₀ + αt', 'θ = ½(ω₀ + ω)t', 'τ = Iα'], 'Replace s, u, v, a with θ, ω₀, ω, α.'),
           ('The tangential acceleration of a point at radius r on a body with angular acceleration α is', 'αr', ['α/r', 'αr²', 'ω²r'], 'a_t = αr.'),
           ('A disc spins at 300 revolutions per minute. Its angular velocity is', '31.4 rad s⁻¹', ['300 rad s⁻¹', '5.0 rad s⁻¹', '1885 rad s⁻¹'], '300 × 2π/60.'),
           ('All points on a rigid rotating wheel have the same', 'angular velocity', ['linear speed', 'centripetal acceleration', 'tangential acceleration'], 'ω is a property of the whole body.')],
    why=[('Explain why points on the rim of a rotating CD move faster than points near the centre, although the angular velocity is the same.', 'v = ωr: for the same ω, the linear speed is proportional to the distance from the axis.'),
         ('Explain why the angle in rotational equations must be in radians.', 'The relations v = ωr and s = rθ come from the definition of the radian (arc length / radius); using degrees would require extra conversion factors.'),
         ('Explain how the area under an angular velocity–time graph is interpreted.', 'Area = ω × t = angular displacement θ, analogous to displacement from a v–t graph.')],
    contrast=[('angular velocity', 'tangential velocity', 'Angular velocity (rad s⁻¹) is the rate of rotation and is the same for every point of a rigid body; tangential velocity (m s⁻¹) is the linear speed of a particular point, v = ωr, which increases with distance from the axis.')],
    misc=[('A wheel rotating at constant angular velocity has no acceleration anywhere.', 'Angular acceleration is zero, but every point except the axis has centripetal acceleration ω²r towards the axis.'),
          ('Angular acceleration has units of rad s⁻¹.', 'Angular acceleration is the rate of change of angular velocity, so its unit is rad s⁻².'),
          ('The suvat equations for rotation work with any angular acceleration.', 'Like linear suvat, the rotational equations require constant angular acceleration.')],
    evaluate=[('Using revolutions per minute is just as good as radians per second for physics calculations.', ['rpm is intuitive and used by engineers and on dashboards'], ['v = ωr, a = ω²r and τ = Iα only hold with radians', 'conversion errors are common'], 'rpm is convenient for communication but must be converted to rad s⁻¹ for calculations because the core equations rely on radian measure.')],
    extended=[('A wind turbine’s blades, 40 m long, accelerate uniformly from rest to 18 revolutions per minute in 60 s, then rotate steadily. (a) Calculate the final angular velocity. (b) Calculate the angular acceleration. (c) Determine the number of revolutions made while accelerating. (d) Calculate the tip speed at full speed and suggest why tip speed is limited in design.', '(a) ω = 18 × 2π/60 = 1.88 rad s⁻¹; (b) α = 0.0314 rad s⁻²; (c) θ = ½ × 1.88 × 60 = 56.5 rad = 9.0 rev; (d) v = ωr = 75.4 m s⁻¹; high tip speeds cause noise, erosion of blade edges and large stresses.', 6)],
))


@prob('ch04-st2', d=(1, 5), md=(1, 4), marks=2)
def p_rot_kin(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        rpm = rng.choice([600, 1200, 1800, 2400, 3000, 4500]); t = rng.choice([2.0, 3.0, 4.0, 5.0, 8.0])
        w = rpm * 2 * math.pi / 60
        return dict(stem=f'A drill bit accelerates uniformly from rest to {rpm} rpm in {t} s. Calculate its angular acceleration.',
                    v=w / t, unit='rad s⁻²', wrongs=[rpm / t, rpm / 60 / t, w * t], key=f'ω = {rpm} × 2π/60 = {sf(w)} rad s⁻¹ (M1); α = ω/t = {sf(w / t)} rad s⁻² (A1).')
    if k == 1:
        w0 = rng.choice([20, 30, 40, 50, 60]); t = rng.choice([5.0, 8.0, 10, 12])
        th = 0.5 * w0 * t
        return dict(stem=f'A spinning flywheel at {w0} rad s⁻¹ is brought uniformly to rest in {t} s. Calculate the number of revolutions it makes while stopping.',
                    v=th / (2 * math.pi), unit='rev', wrongs=[th, w0 * t / (2 * math.pi), th / math.pi], key=f'θ = ½(ω₀ + ω)t = {sf(th)} rad (M1); revolutions = θ/2π = {sf(th / (2 * math.pi))} (A1).')
    if k == 2:
        r = rng.choice([0.30, 0.33, 0.35, 0.40]); v = rng.choice([8, 10, 12, 15, 20])
        return dict(stem=f'{who} rides a bicycle at {v} m s⁻¹ in {city}. The wheels have radius {r} m and roll without slipping. Calculate the angular velocity of the wheels.',
                    v=v / r, unit='rad s⁻¹', wrongs=[v * r, v / (2 * math.pi * r), v / r / (2 * math.pi) * 60], key=f'ω = v/r (M1) = {sf(v / r)} rad s⁻¹ (A1).')
    if k == 3:
        w0 = rng.choice([5.0, 10, 15]); a = rng.choice([2.0, 3.0, 4.0]); th = rng.choice([20, 40, 60])
        w = math.sqrt(w0 * w0 + 2 * a * th)
        return dict(stem=f'A turntable rotating at {w0} rad s⁻¹ has a constant angular acceleration of {a} rad s⁻². Calculate its angular velocity after it has turned through a further {th} rad.',
                    v=w, unit='rad s⁻¹', wrongs=[w0 + a * th, math.sqrt(2 * a * th), w0 * w0 + 2 * a * th], key=f'ω² = ω₀² + 2αθ (M1); ω = {sf(w)} rad s⁻¹ (A1).')
    a = rng.choice([1.5, 2.0, 2.5, 3.0]); r = rng.choice([0.10, 0.15, 0.20, 0.25])
    return dict(stem=f'A grindstone has an angular acceleration of {a} rad s⁻². Calculate the tangential acceleration of a point on its rim, {r} m from the axis.',
                v=a * r, unit='m s⁻²', wrongs=[a / r, a * r * r, a * r * 2 * math.pi], key=f'a_t = αr (M1) = {sf(a * r)} m s⁻² (A1).')


R.mcqs('ch04-st2', 'C2', (1, 4), [
    ('Two points P and Q are on a rotating disc; P is twice as far from the axis as Q. The ratio of linear speeds v_P : v_Q is', '2 : 1', ['1 : 1', '1 : 2', '4 : 1'], 'v = ωr.'),
    ('The gradient of an angular velocity–time graph gives the', 'angular acceleration', ['angular displacement', 'torque', 'moment of inertia'], 'α = dω/dt.'),
    ('A wheel’s angular velocity changes from 10 rad s⁻¹ to 30 rad s⁻¹ in 4.0 s. The angular displacement in this time is', '80 rad', ['40 rad', '120 rad', '20 rad'], 'θ = ½(10 + 30) × 4.'),
])


R.facts('ch04-st3', F(
    terms=[('moment of inertia', 'the rotational analogue of mass, I = Σmr², which measures a body’s resistance to angular acceleration about an axis'),
           ('Newton’s second law for rotation', 'the resultant torque on a body equals its moment of inertia times its angular acceleration, τ = Iα'),
           ('axis of rotation', 'the line about which a body rotates; I depends on its position'),
           ('rotational inertia', 'the property of a body that resists changes to its angular velocity, quantified by I')],
    facts=[('The moment of inertia of a point mass m at distance r from the axis is', 'mr²', ['mr', 'm/r²', '½mr²'], 'Definition.'),
           ('Which has the larger moment of inertia about its central axis: a ring or a disc of the same mass and radius?', 'The ring', ['The disc', 'They are equal', 'It depends on angular velocity'], 'All the ring’s mass is at r; I_ring = MR², I_disc = ½MR².'),
           ('What is the SI unit of moment of inertia?', 'kg m²', ['kg m', 'N m', 'kg m s⁻²'], 'I = Σmr².'),
           ('A resultant torque of 12 N m acts on a wheel with I = 3.0 kg m². Its angular acceleration is', '4.0 rad s⁻²', ['36 rad s⁻²', '0.25 rad s⁻²', '15 rad s⁻²'], 'α = τ/I.'),
           ('A solid sphere and a hollow sphere of the same mass and radius roll down the same slope. Which reaches the bottom first?', 'The solid sphere', ['The hollow sphere', 'They arrive together', 'It depends on their mass'], 'Smaller I/mr² means a larger fraction of energy goes into translation.')],
    why=[('Explain why a tightrope walker carries a long pole.', 'The pole has a large moment of inertia, so a given torque produces only a small angular acceleration, giving the walker more time to correct their balance.'),
         ('Explain why the moment of inertia of an object depends on the axis of rotation.', 'I = Σmr² depends on how far each mass element is from the axis; changing the axis changes the distances.'),
         ('Explain why a solid cylinder rolls down a slope faster than a hoop of the same mass and radius.', 'Both convert the same GPE to KE; the hoop has a larger I, so a bigger fraction of the energy goes into rotation and less into translation, giving a lower speed.')],
    contrast=[('mass', 'moment of inertia', 'Mass measures resistance to linear acceleration and is fixed; moment of inertia measures resistance to angular acceleration and depends on how mass is distributed about the chosen axis.')],
    misc=[('Two objects with the same mass must have the same moment of inertia.', 'I depends on the distribution of mass relative to the axis, so objects of equal mass can have very different I.'),
          ('A larger torque always produces a larger angular velocity.', 'Torque produces angular acceleration (τ = Iα); the angular velocity also depends on how long the torque acts and on the initial ω.'),
          ('The moment of inertia of a rod is the same about any axis.', 'A rod of length L has I = ML²/12 about its centre but ML²/3 about one end.')],
    evaluate=[('Flywheels are a practical alternative to batteries for storing energy.', ['high power output and rapid charging', 'long lifetime with many cycles', 'no toxic chemicals'], ['energy leaks away by friction (self-discharge)', 'large stresses in fast-spinning rotors – safety containment needed', 'lower energy per unit mass than batteries'], 'Flywheels are excellent for short-term, high-power storage (grid frequency control, buses, F1 KERS), but batteries are better for long-duration storage.')],
    extended=[('A 2.0 kg bucket hangs from a rope wound around a solid cylindrical drum of mass 8.0 kg and radius 0.15 m (I = ½MR²) mounted on a frictionless axle. The bucket is released. (a) Write Newton’s second law for the bucket and for the drum. (b) Show that a = mg/(m + M/2) and calculate it. (c) Calculate the tension in the rope. (d) Determine the angular velocity of the drum after the bucket has fallen 2.0 m.', '(a) mg − T = ma; TR = Iα = ½MR² × a/R; (b) a = 2.0 × 9.81/6.0 = 3.27 m s⁻²; (c) T = ½Ma = 13.1 N; (d) v = √(2 × 3.27 × 2.0) = 3.62 m s⁻¹, ω = 24.1 rad s⁻¹.', 6)],
))

SHAPES = [('solid disc', 0.5), ('ring (hoop)', 1.0), ('solid sphere', 0.4), ('thin spherical shell', 2 / 3)]


@prob('ch04-st3', d=(1, 5), md=(1, 4), marks=2)
def p_inertia(rng, slot):
    k = rng.randrange(5)
    city = rng.choice(CITIES)
    if k == 0:
        nm, c = pick(rng, SHAPES); M = rng.choice([0.5, 1.2, 2.0, 5.0, 10]); r = rng.choice([0.10, 0.20, 0.25, 0.40])
        fr = {0.5: '½MR²', 1.0: 'MR²', 0.4: '(2/5)MR²', 2 / 3: '(2/3)MR²'}[c]
        return dict(stem=f'Calculate the moment of inertia of a {nm} of mass {M} kg and radius {r} m about its central axis (I = {fr}).',
                    v=c * M * r * r, unit='kg m²', wrongs=[M * r * r if c != 1 else 0.5 * M * r * r, c * M * r, c * M * r * r * 2], key=f'I = {fr} = {sf(c * M * r * r)} kg m² (A1).', marks=1)
    if k == 1:
        I = rng.choice([0.5, 1.2, 2.0, 4.0, 8.0]); tau = rng.choice([3.0, 5.0, 8.0, 12, 20])
        return dict(stem=f'A potter’s wheel with moment of inertia {I} kg m² is acted on by a resultant torque of {tau} N m. Calculate its angular acceleration.',
                    v=tau / I, unit='rad s⁻²', wrongs=[tau * I, I / tau, tau / I ** 2], key=f'τ = Iα (M1); α = {tau}/{I} = {sf(tau / I)} rad s⁻² (A1).')
    if k == 2:
        M = rng.choice([2.0, 4.0, 6.0]); R_ = rng.choice([0.20, 0.25, 0.30]); F_ = rng.choice([10, 15, 20]); t = rng.choice([2.0, 3.0, 4.0])
        I = 0.5 * M * R_ * R_; w = F_ * R_ / I * t
        return dict(stem=f'A rope is pulled with a constant force of {F_} N tangentially around the rim of a solid disc (mass {M} kg, radius {R_} m) that is free to rotate. Calculate the angular velocity after {t} s from rest.',
                    v=w, unit='rad s⁻¹', wrongs=[F_ / (M * R_) * t, F_ * R_ / (M * R_ * R_) * t, F_ * R_ / I], key=f'I = ½MR² = {sf(I)} kg m² (M1); α = FR/I = {sf(F_ * R_ / I)} rad s⁻² (M1); ω = αt = {sf(w)} rad s⁻¹ (A1).', marks=3)
    if k == 3:
        ms = rng.choice([0.2, 0.5, 1.0]); r1 = rng.choice([0.1, 0.2]); r2_ = rng.choice([0.3, 0.4, 0.5])
        I = ms * r1 ** 2 + ms * r2_ ** 2
        return dict(stem=f'Two small masses of {ms} kg each are fixed to a light rod at distances {r1} m and {r2_} m from the axis of rotation. Calculate the moment of inertia of the system.',
                    v=I, unit='kg m²', wrongs=[ms * (r1 + r2_) ** 2, ms * (r1 + r2_), 2 * ms * r2_ ** 2], key=f'I = Σmr² = {ms}({r1}² + {r2_}²) (M1) = {sf(I)} kg m² (A1).')
    nm, c = pick(rng, SHAPES); h = rng.choice([0.5, 1.0, 1.5, 2.0])
    v = math.sqrt(2 * g0 * h / (1 + c))
    return dict(stem=f'A {nm} rolls without slipping from rest down a slope of vertical height {h} m. Using I = {c:.2g}MR², calculate its speed at the bottom.',
                v=v, unit='m s⁻¹', wrongs=[math.sqrt(2 * g0 * h), math.sqrt(2 * g0 * h / c), math.sqrt(g0 * h)], key=f'mgh = ½mv² + ½Iω² = ½mv²(1 + {c:.2g}) (M1); v = √(2gh/(1 + {c:.2g})) = {sf(v)} m s⁻¹ (A1).', marks=3)


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step')
def c4_drum(rng, slot):
    m = rng.choice([1.0, 1.5, 2.0, 3.0]); M = rng.choice([4.0, 6.0, 8.0]); R_ = rng.choice([0.10, 0.15, 0.20]); h = rng.choice([1.0, 1.5, 2.0])
    a = m * g0 / (m + M / 2); T_ = 0.5 * M * a; v = math.sqrt(2 * a * h)
    frame = rng.randrange(2)
    intro = (f'A {m} kg bucket hangs from a rope wound around a solid cylindrical drum (mass {M} kg, radius {R_} m, I = ½MR²) on a frictionless axle over a well.' if frame == 0 else
             f'In a laboratory, a {m} kg mass on a cord unwinds from a solid flywheel of mass {M} kg and radius {R_} m (I = ½MR²) that turns freely.')
    return num(f'{intro} The system is released from rest. (a) Write equations for the linear motion of the hanging mass and the rotation of the drum. (b) Determine the acceleration of the hanging mass. (c) Calculate the tension in the rope. (d) Calculate the angular velocity of the drum after the mass has fallen {h} m and verify the result using energy conservation.',
               f'(b) {sf(a)} m s⁻²; (c) {sf(T_)} N; (d) v = {sf(v)} m s⁻¹, ω = {sf(v / R_)} rad s⁻¹; energy: mgh = ½mv² + ½Iω² gives the same v.',
               f'(a) mg − T = ma; TR = Iα with α = a/R (M1 M1). (b) a = mg/(m + M/2) (A1). (c) T = ½Ma (A1). (d) v² = 2ah, ω = v/R (A1); energy check (R1).', 6, 'multi_step')


R.mcqs('ch04-st3', 'C2', (1, 4), [
    ('A figure skater pulls her arms in while spinning. Her moment of inertia', 'decreases', ['increases', 'stays the same', 'becomes zero'], 'Mass moves closer to the axis.'),
    ('The same torque is applied to a ring and a disc of equal mass and radius. Which has the greater angular acceleration?', 'The disc', ['The ring', 'Both equal', 'Neither accelerates'], 'Smaller I.'),
    ('The moment of inertia of a rod about an axis through one end is greater than about its centre because', 'more of its mass is far from the axis', ['the rod is heavier at the end', 'torque is larger at the end', 'the rod rotates faster'], 'I = Σmr².'),
])


def _flywheel_spec(rng):
    I = rng.uniform(0.020, 0.060); r = 0.020
    ms = [0.050, 0.100, 0.150, 0.200, 0.250, 0.300]
    al = [round(m_ * g0 * r / (I + m_ * r * r) * rng.uniform(0.97, 1.03), 3) for m_ in ms]
    return dict(intro='A flywheel is mounted on an axle of radius 0.020 m. A cord wound on the axle supports a hanging mass m. The angular acceleration α is measured with a rotary sensor. For small masses the torque is approximately mgr. Theory: mgr = Iα.',
                xname='m', xunit='kg', yname='α', yunit='rad s⁻²', xs=ms, ys=al, xfmt=lambda a: f'{a:.3f}', yfmt=lambda b: f'{b:.3f}',
                plot_x=lambda a: a * g0 * 0.020, plot_y=lambda b: b, plot_label='α (y) against torque mgr (x)', what='the moment of inertia I of the flywheel', what_short='I',
                gunit='kg⁻¹ m⁻²', deduce=lambda m_, b_: (1 / m_, 'kg m²', 'I = 1/gradient'))


gradient_fit('ch04-st3', _flywheel_spec)


R.facts('ch04-st4', F(
    terms=[('angular momentum', 'the rotational analogue of linear momentum, L = Iω, in kg m² s⁻¹'),
           ('conservation of angular momentum', 'the total angular momentum of a system is constant if no resultant external torque acts on it'),
           ('rotational kinetic energy', 'the kinetic energy of a rotating body, E = ½Iω² = L²/2I'),
           ('angular impulse', 'the product of torque and the time for which it acts, τΔt, equal to the change in angular momentum'),
           ('rolling without slipping', 'motion in which the contact point is instantaneously at rest, so v = ωr')],
    facts=[('What is the unit of angular momentum?', 'kg m² s⁻¹', ['kg m s⁻¹', 'N m', 'J s⁻¹'], 'L = Iω.'),
           ('A skater spinning with arms out pulls them in. Her angular velocity', 'increases', ['decreases', 'stays the same', 'becomes zero'], 'L = Iω constant, I decreases.'),
           ('When a skater pulls her arms in, her rotational kinetic energy', 'increases, because she does work pulling her arms in', ['decreases', 'stays the same', 'becomes zero'], 'E = L²/2I increases as I decreases.'),
           ('A rolling ball has total kinetic energy equal to', '½mv² + ½Iω²', ['½mv²', '½Iω²', 'mgh only'], 'Translation plus rotation.'),
           ('The area under a torque–time graph equals', 'the change in angular momentum', ['the work done', 'the angular displacement', 'the power'], 'Angular impulse.')],
    why=[('Explain why a diver tucks into a ball to perform somersaults.', 'Once in the air no external torque acts (about the centre of mass), so L = Iω is constant; tucking reduces I, increasing ω so more rotations can be completed before entry.'),
         ('Explain why a helicopter needs a tail rotor.', 'The engine exerts a torque on the main rotor; by Newton’s third law the rotor exerts an equal opposite torque on the body. Without the tail rotor’s counter-torque the body would spin to conserve angular momentum.'),
         ('Explain why a neutron star rotates very rapidly.', 'When a stellar core collapses, its radius falls enormously, so I falls; with no external torque, angular momentum is conserved, so ω increases enormously.')],
    contrast=[('linear momentum', 'angular momentum', 'Linear momentum p = mv is conserved when no external force acts; angular momentum L = Iω is conserved when no external torque acts. Both are vectors.')],
    misc=[('If angular momentum is conserved, rotational kinetic energy must also be conserved.', 'E = L²/2I: when I changes at constant L, the kinetic energy changes; e.g. a skater increases her KE by doing work pulling her arms in.'),
          ('A body can only have angular momentum if it spins about its own axis.', 'A particle moving in a straight line also has angular momentum mvr⊥ about a point not on its line of motion.'),
          ('A spinning object needs a continuous torque to keep spinning.', 'A torque is only needed to change the angular velocity; with no resultant torque it spins at constant ω.')],
    evaluate=[('Conservation of angular momentum explains everything about how a cat lands on its feet.', ['the cat changes its moment of inertia by tucking and extending legs'], ['the total angular momentum is zero throughout – the cat rotates parts of its body in opposite directions', 'a simple Iω = constant model cannot explain a turn from zero L', 'flexibility and reflexes matter'], 'Angular momentum conservation constrains the motion, but the cat’s trick is to rotate front and back halves by different amounts with zero total L; a single rigid-body model is insufficient.')],
    extended=[('A playground roundabout (a disc of mass 120 kg, radius 1.5 m, I = ½MR²) rotates at 1.2 rad s⁻¹. A 40 kg child steps on at the rim from rest (relative to the ground). (a) Calculate the initial angular momentum. (b) Determine the new angular velocity. (c) Calculate the change in rotational kinetic energy and explain where the energy goes. (d) The child walks to the centre; determine the angular velocity then.', '(a) I = 135 kg m², L = 162 kg m² s⁻¹; (b) I = 135 + 90 = 225, ω = 0.72 rad s⁻¹; (c) 97.2 J → 58.3 J, 38.9 J lost to internal energy by friction as the child is brought up to speed; (d) back to 1.2 rad s⁻¹.', 6)],
))


@prob('ch04-st4', d=(1, 5), md=(1, 4), marks=2)
def p_angmom(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        I1 = rng.choice([3.0, 3.5, 4.0, 4.5]); I2 = rng.choice([1.0, 1.2, 1.5]); w1 = rng.choice([2.0, 3.0, 4.0, 5.0])
        return dict(stem=f'{who}, a figure skater in {city}, spins at {w1} rad s⁻¹ with arms outstretched (I = {I1} kg m²). She pulls her arms in, reducing I to {I2} kg m². Calculate her new angular velocity.',
                    v=I1 * w1 / I2, unit='rad s⁻¹', wrongs=[I2 * w1 / I1, w1 * math.sqrt(I1 / I2), w1 * (I1 / I2) ** 2], key=f'I₁ω₁ = I₂ω₂ (M1); ω₂ = {sf(I1 * w1 / I2)} rad s⁻¹ (A1).')
    if k == 1:
        I = rng.choice([0.5, 2.0, 5.0, 10, 20]); w = rng.choice([10, 20, 50, 100, 300])
        return dict(stem=f'A flywheel of moment of inertia {I} kg m² rotates at {w} rad s⁻¹. Calculate its rotational kinetic energy.',
                    v=0.5 * I * w * w, unit='J', wrongs=[I * w * w, 0.5 * I * w, I * w], key=f'E = ½Iω² (M1) = {sf(0.5 * I * w * w)} J (A1).')
    if k == 2:
        I = rng.choice([0.8, 1.5, 3.0, 5.0]); w = rng.choice([10, 20, 30, 40])
        return dict(stem=f'A rotor with moment of inertia {I} kg m² spins at {w} rad s⁻¹. Calculate its angular momentum.',
                    v=I * w, unit='kg m² s⁻¹', wrongs=[0.5 * I * w * w, I * w * w, I / w], key=f'L = Iω (M1) = {sf(I * w)} kg m² s⁻¹ (A1).')
    if k == 3:
        I = rng.choice([2.0, 4.0, 6.0]); w = rng.choice([20, 30, 40]); t = rng.choice([5.0, 8.0, 10])
        return dict(stem=f'A spinning wheel (I = {I} kg m²) at {w} rad s⁻¹ is stopped by a brake in {t} s. Calculate the average braking torque.',
                    v=I * w / t, unit='N m', wrongs=[I * w * t, 0.5 * I * w * w / t, I * w], key=f'τ = ΔL/Δt = Iω/t (M1) = {sf(I * w / t)} N m (A1).')
    Id = rng.choice([100, 135, 150]); m = rng.choice([30, 40, 50]); R_ = rng.choice([1.2, 1.5]); w = rng.choice([1.0, 1.2, 1.5])
    w2 = Id * w / (Id + m * R_ * R_)
    return dict(stem=f'A playground roundabout with I = {Id} kg m² rotates freely at {w} rad s⁻¹. A {m} kg child steps onto its rim, {R_} m from the axis. Calculate the new angular velocity.',
                v=w2, unit='rad s⁻¹', wrongs=[Id * w / (Id + m * R_), w * m * R_ * R_ / Id, w / 2], key=f'Iω = (I + mR²)ω₂ (M1); ω₂ = {Id} × {w}/({Id} + {sf(m * R_ * R_)}) = {sf(w2)} rad s⁻¹ (A1).', marks=3)


R.mcqs('ch04-st4', 'C2', (1, 4), [
    ('A turntable rotates freely. Sand is dropped vertically onto it. Which is correct?', 'Its angular velocity decreases while angular momentum is conserved', ['Its angular momentum increases', 'Its angular velocity is unchanged', 'Its kinetic energy is conserved'], 'I increases, L constant.'),
    ('If the angular velocity of a flywheel doubles, its rotational kinetic energy', 'quadruples', ['doubles', 'halves', 'is unchanged'], 'E ∝ ω².'),
    ('A planet in an elliptical orbit moves faster when closer to the Sun because', 'its angular momentum about the Sun is conserved', ['the Sun pushes it', 'its mass decreases', 'its kinetic energy is conserved'], 'mvr constant (Kepler’s second law).'),
])


# =============================================================================================
# ch05 A.5 Galilean and special relativity (HL)
# =============================================================================================
def gam(b):
    return 1 / math.sqrt(1 - b * b)


BETAS = [0.50, 0.60, 0.80, 0.866, 0.90, 0.95, 0.98, 0.99]

R.facts('ch05-st1', F(
    terms=[('reference frame', 'a coordinate system with clocks and rulers from which observers measure the positions and times of events'),
           ('inertial reference frame', 'a frame that is not accelerating, in which Newton’s first law holds'),
           ('event', 'something that happens at a particular point in space at a particular instant, described by coordinates (x, y, z, t)'),
           ('Galilean transformation', 'the equations x′ = x − vt and t′ = t relating coordinates in two inertial frames in relative motion at speed v, valid when v ≪ c'),
           ('Galilean velocity addition', 'the rule u′ = u − v for the velocity of an object measured in a frame moving at v')],
    facts=[('In Galilean relativity, time intervals measured by observers in different inertial frames are', 'the same', ['different', 'dilated', 'contracted'], 't′ = t is assumed.'),
           ('A passenger walks forward at 1.5 m s⁻¹ in a train moving at 30 m s⁻¹. According to Galilean relativity, her speed relative to the track is', '31.5 m s⁻¹', ['28.5 m s⁻¹', '30 m s⁻¹', '45 m s⁻¹'], 'u = u′ + v.'),
           ('Which quantity is the same in all inertial frames in Galilean relativity?', 'Acceleration', ['Velocity', 'Kinetic energy', 'Momentum'], 'a′ = a since v is constant.'),
           ('Galilean transformations fail when', 'speeds approach the speed of light', ['objects accelerate gently', 'forces are large', 'objects are massive'], 'They predict light speed depends on the frame.'),
           ('Which is NOT an inertial frame?', 'A car going round a bend at constant speed', ['A train moving at constant velocity on a straight track', 'A spacecraft drifting far from any star', 'A laboratory at rest (approximately)'], 'The car accelerates centripetally.')],
    why=[('Explain why the laws of mechanics are the same in all inertial frames under Galilean relativity.', 'Under x′ = x − vt with constant v, accelerations are the same in both frames, so F = ma has the same form in both: no mechanical experiment can detect uniform motion.'),
         ('Explain why Galilean velocity addition is inconsistent with Maxwell’s prediction of the speed of light.', 'Maxwell’s equations give light a fixed speed c = 1/√(ε₀μ₀) with no reference to a frame, but Galilean addition would make the measured speed c − v in a moving frame.'),
         ('Explain why the result of the Michelson–Morley experiment was surprising in the 19th century.', 'Physicists expected Earth’s motion through the ether to change the speed of light in different directions and shift the interference fringes; no shift was observed.')],
    contrast=[('an inertial frame', 'a non-inertial frame', 'In an inertial frame (not accelerating) Newton’s laws hold without fictitious forces; in a non-inertial (accelerating or rotating) frame, apparent forces such as centrifugal force must be introduced.')],
    misc=[('Observers in different inertial frames always agree on the velocity of an object.', 'Velocity depends on the frame (u′ = u − v); they agree on acceleration in Galilean relativity, not velocity.'),
          ('An inertial frame must be at rest.', 'Any frame moving at constant velocity is inertial; there is no experiment that distinguishes rest from uniform motion.'),
          ('Galilean relativity is wrong and should not be used.', 'It is an excellent approximation when speeds are much smaller than c, and it is the low-speed limit of special relativity.')],
    evaluate=[('The null result of the Michelson–Morley experiment proved that the ether does not exist.', ['no fringe shift was observed to high precision', 'it supported the constancy of light speed'], ['physicists proposed alternatives such as ether drag and Lorentz–FitzGerald contraction', 'a null result alone cannot prove non-existence', 'acceptance came when special relativity explained many results more simply'], 'It strongly undermined the ether, but the case was settled by Einstein’s simpler, more predictive theory rather than by one experiment (NOS: theory choice and parsimony).')],
    extended=[('A boat crosses a river 120 m wide. It moves at 4.0 m s⁻¹ relative to the water, heading straight across, and the river flows at 3.0 m s⁻¹. (a) Use Galilean velocity addition to find the boat’s velocity relative to the bank. (b) Calculate the crossing time. (c) Determine the distance downstream at which it lands. (d) Explain why light does not behave in this way.', '(a) 5.0 m s⁻¹ at 36.9° downstream from straight across; (b) 30 s; (c) 90 m; (d) the speed of light in vacuum is the same for all inertial observers, so velocities do not add in the Galilean way at relativistic speeds.', 6)],
))


@prob('ch05-st1', d=(1, 4), md=(1, 4), marks=2)
def p_galilean(rng, slot):
    k = rng.randrange(4)
    who, city = who_city(rng)
    if k == 0:
        v = rng.choice([20, 25, 30, 40]); u = rng.choice([1.2, 1.5, 2.0, 2.5])
        back = rng.random() < 0.5
        return dict(stem=f'{who} walks towards the {"back" if back else "front"} of a train at {u} m s⁻¹ relative to the train, which moves at {v} m s⁻¹ along a track near {city}. Use the Galilean transformation to find her velocity relative to the track.',
                    v=v - u if back else v + u, unit='m s⁻¹', wrongs=[v + u if back else v - u, u, v], key=f'u = u′ + v (M1) = {sf(v - u if back else v + u)} m s⁻¹ in the direction of the train (A1).')
    if k == 1:
        x = rng.choice([200, 500, 800, 1200]); v = rng.choice([10, 20, 30]); t = rng.choice([5, 10, 15, 20])
        return dict(stem=f'An event occurs at x = {x} m, t = {t} s in frame S. Frame S′ moves at {v} m s⁻¹ along +x, with origins coinciding at t = 0. Using the Galilean transformation, calculate x′.',
                    v=x - v * t, unit='m', wrongs=[x + v * t, x - v / t, x], key=f'x′ = x − vt (M1) = {x} − {v} × {t} = {sf(x - v * t)} m (A1); t′ = t.')
    if k == 2:
        vc = rng.choice([25, 30, 35]); vt = rng.choice([20, 22, 28])
        return dict(stem=f'A car travels at {vc} m s⁻¹ east and a truck at {vt} m s⁻¹ west on the same road. Calculate the velocity of the truck relative to the car (Galilean).',
                    v=vc + vt, unit='m s⁻¹', wrongs=[vc - vt if vc != vt else vt, vt, (vc + vt) / 2], key=f'Relative velocity = u − v = −{vt} − {vc} (M1) = {vc + vt} m s⁻¹ westward (A1).')
    v = rng.choice([3.0e4]); c_ = C
    return dict(stem=f'According to Galilean relativity, what speed would an observer on Earth (orbital speed {sf(v, 2)} m s⁻¹) measure for light from a star directly ahead, if light travelled at c relative to the star?',
                v=c_ + v, unit='m s⁻¹', n=6, wrongs=[c_ - v, c_, c_ + 2 * v], key=f'Galilean addition: c + v = {sf(c_ + v, 6)} m s⁻¹ (A1); experiment shows c exactly, which contradicts Galilean relativity (R1).', marks=2)


R.mcqs('ch05-st1', 'C2', (1, 4), [
    ('A ball is dropped inside a train moving at constant velocity. A passenger sees the ball fall vertically. An observer on the platform sees it follow', 'a parabolic path', ['a vertical straight line', 'a circular path', 'a path curving backwards'], 'The ball shares the train’s horizontal velocity.'),
    ('Two inertial observers measure the same object. In Galilean relativity they agree on its', 'acceleration', ['velocity', 'position', 'kinetic energy'], 'Uniform relative motion does not change a.'),
    ('Which experiment found no evidence for motion relative to the ether?', 'Michelson–Morley', ['Rutherford scattering', 'Millikan oil drop', 'Young double slit'], 'Null result of 1887.'),
])


R.facts('ch05-st2', F(
    terms=[('first postulate of special relativity', 'the laws of physics are the same in all inertial reference frames'),
           ('second postulate of special relativity', 'the speed of light in a vacuum is the same, c, for all inertial observers, independent of the motion of the source or observer'),
           ('Lorentz factor', 'the factor γ = 1/√(1 − v²/c²) by which time intervals dilate and lengths contract, always ≥ 1'),
           ('Lorentz transformation', 'the equations x′ = γ(x − vt) and t′ = γ(t − vx/c²) relating event coordinates in two inertial frames'),
           ('relativity of simultaneity', 'events that are simultaneous in one inertial frame are generally not simultaneous in another frame moving relative to it')],
    facts=[('What is the Lorentz factor γ for v = 0.60c?', '1.25', ['0.80', '1.67', '1.60'], 'γ = 1/√(1 − 0.36) = 1/0.8.'),
           ('According to the second postulate, light from a source moving towards an observer at 0.5c travels at', 'c', ['1.5c', '0.5c', '2c'], 'c is invariant.'),
           ('As v → 0, the Lorentz transformation reduces to', 'the Galilean transformation', ['x′ = x', 'no transformation', 'time dilation only'], 'γ → 1 and vx/c² → 0.'),
           ('Two events at different places are simultaneous in frame S. In frame S′ moving along the line joining them, they are', 'not simultaneous', ['simultaneous', 'at the same place', 'impossible'], 'Δt′ = −γvΔx/c².'),
           ('Which quantity can never be less than 1?', 'γ', ['v/c', '1/γ', 'the proper time'], 'For v < c, γ ≥ 1.')],
    why=[('Explain why the two postulates of special relativity lead to the conclusion that time is not absolute.', 'If light speed is the same for all observers, then for a light pulse travelling a different distance in two frames, the times must differ; observers in relative motion must disagree on time intervals and simultaneity.'),
         ('Explain why the Lorentz transformation shows that nothing with mass can reach the speed of light.', 'As v → c, γ → ∞; at v = c the transformations become undefined, and the energy required to accelerate a mass increases without limit.'),
         ('Explain, using the relativity of simultaneity, why "now" is not the same for all observers.', 'From t′ = γ(t − vx/c²), events at different x with equal t have different t′; whether two distant events happen at the same time depends on the observer’s frame.')],
    contrast=[('the Galilean transformation', 'the Lorentz transformation', 'The Galilean transformation assumes absolute time (t′ = t) and adds velocities simply; the Lorentz transformation keeps c invariant, mixes space and time (t′ = γ(t − vx/c²)) and reduces to the Galilean form when v ≪ c.')],
    misc=[('Relativity says that everything is relative, including the speed of light.', 'The speed of light in vacuum is one of the few absolutes: it is the same for all inertial observers, which is the second postulate.'),
          ('The Lorentz factor can be less than 1 for slow-moving objects.', 'γ = 1/√(1 − v²/c²) is exactly 1 at v = 0 and greater than 1 for any v > 0.'),
          ('Relativistic effects only appear because clocks are badly made.', 'Time dilation and simultaneity are properties of space-time itself, verified with atomic clocks, muons and GPS.')],
    evaluate=[('Einstein’s special relativity was accepted because of the Michelson–Morley experiment.', ['the null result is consistent with the invariance of c'], ['Einstein said the experiment had little influence on his thinking', 'he was motivated by the symmetry of Maxwell’s equations', 'acceptance followed confirmation by later experiments (time dilation of muons, particle accelerators)'], 'The theory was built mainly on theoretical consistency and was accepted after many confirmations; the experiment was supporting evidence rather than the direct cause (NOS).')],
    extended=[('In frame S, event A occurs at x = 0, t = 0 and event B at x = 900 m, t = 2.0 μs. Frame S′ moves at 0.60c along +x, with origins coinciding at t = 0. (a) Calculate γ. (b) Use the Lorentz transformation to find x′ and t′ for event B. (c) Determine the time interval between A and B in S′. (d) Comment on the order of the events in the two frames.', '(a) 1.25; (b) x′ = 1.25(900 − 0.6 × 3 × 10⁸ × 2 × 10⁻⁶) = 1.25 × 540 = 675 m; t′ = 1.25(2.0 × 10⁻⁶ − 0.6 × 900/3 × 10⁸) = 1.25(2.0 − 1.8) μs = 0.25 μs; (c) 0.25 μs; (d) B is still after A in S′ but much closer in time; because the interval is timelike (c²t² > x²) the order cannot be reversed.', 6)],
))


@prob('ch05-st2', d=(1, 5), md=(1, 4), marks=2)
def p_lorentz(rng, slot):
    k = rng.randrange(4)
    b = pick(rng, BETAS)
    g = gam(b)
    if k == 0:
        return dict(stem=f'A spacecraft moves at {b}c relative to Earth. Calculate the Lorentz factor γ.', v=g, unit='', wrongs=[1 / g, 1 / (1 - b * b), 1 + b], key=f'γ = 1/√(1 − {b}²) (M1) = {sf(g)} (A1).', marks=1)
    if k == 1:
        x = rng.choice([300, 600, 900, 1200, 1500]); t_us = rng.choice([1.0, 2.0, 3.0, 4.0, 5.0])
        xp = g * (x - b * C * t_us * 1e-6)
        return dict(stem=f'In frame S an event occurs at x = {x} m, t = {t_us} μs. Frame S′ moves at {b}c along +x, with origins coinciding at t = 0. Calculate x′ for the event.',
                    v=xp, unit='m', wrongs=[x - b * C * t_us * 1e-6, g * x, g * (x + b * C * t_us * 1e-6)], key=f'x′ = γ(x − vt) (M1) = {sf(g)}({x} − {sf(b * C * t_us * 1e-6)}) = {sf(xp)} m (A1).', marks=2)
    if k == 2:
        x = rng.choice([300, 600, 900, 1200, 1500]); t_us = rng.choice([1.0, 2.0, 4.0, 6.0, 8.0])
        tp = g * (t_us * 1e-6 - b * x / C)
        return dict(stem=f'An event has coordinates x = {x} m, t = {t_us} μs in frame S. Determine its time coordinate t′ in a frame S′ moving at {b}c along +x (origins coincide at t = 0).',
                    v=tp * 1e6, unit='μs', wrongs=[g * t_us, t_us - b * x / C * 1e6, g * (t_us + b * x / C * 1e6)], key=f't′ = γ(t − vx/c²) (M1) = {sf(g)}({t_us} μs − {sf(b * x / C * 1e6)} μs) = {sf(tp * 1e6)} μs (A1).', marks=2)
    dx = rng.choice([600, 900, 1500, 3000])
    dt = g * b * dx / C
    return dict(stem=f'Two lamps {dx} m apart flash simultaneously in the laboratory frame. Calculate the time interval between the flashes measured by an observer moving at {b}c along the line joining them.',
                v=dt * 1e6, unit='μs', wrongs=[b * dx / C * 1e6, dx / C * 1e6, g * dx / C * 1e6], key=f'Δt′ = γ(Δt − vΔx/c²) with Δt = 0 (M1); |Δt′| = γvΔx/c² = {sf(dt * 1e6)} μs (A1).', marks=2)


R.mcqs('ch05-st2', 'C2', (1, 4), [
    ('A spaceship moving at 0.8c towards a star fires a laser forwards. An observer at rest relative to the star measures the speed of the laser light as', 'c', ['1.8c', '0.2c', '0.8c'], 'Second postulate.'),
    ('An observer in frame S sees two events happen at the same place and the same time. An observer in any other inertial frame', 'also sees them happen at the same place and time', ['sees them at different times', 'sees them at different places', 'may see them in reverse order'], 'A single space-time point is the same event.'),
    ('As a spacecraft’s speed increases towards c, γ', 'increases without limit', ['decreases to zero', 'approaches 2', 'stays at 1'], 'γ → ∞.'),
])


R.facts('ch05-st3', F(
    terms=[('proper time', 'the time interval between two events measured by an observer for whom the events occur at the same place'),
           ('time dilation', 'the lengthening of a time interval measured by an observer moving relative to the clock, Δt = γΔt₀'),
           ('proper length', 'the length of an object measured in the frame in which it is at rest'),
           ('length contraction', 'the shortening of a length along the direction of motion measured by an observer moving relative to the object, L = L₀/γ'),
           ('relativistic velocity addition', 'the rule u′ = (u − v)/(1 − uv/c²) for transforming velocities between frames, which never gives a speed greater than c')],
    facts=[('Muons created in the upper atmosphere reach the ground in large numbers mainly because', 'their lifetime is dilated in Earth’s frame', ['they travel faster than light', 'they are created near the ground', 'their mass increases'], 'Δt = γΔt₀.'),
           ('A rod of proper length 1.0 m moves at 0.80c along its length. Its measured length is', '0.60 m', ['1.67 m', '0.80 m', '1.0 m'], 'L = L₀/γ = 1.0 × 0.6.'),
           ('Length contraction occurs', 'only in the direction of relative motion', ['in all directions', 'perpendicular to the motion only', 'only for accelerating objects'], 'Transverse dimensions are unchanged.'),
           ('Two spaceships approach each other, each at 0.6c relative to Earth. The speed of one relative to the other is', '0.88c', ['1.2c', 'c', '0.6c'], 'u′ = 1.2c/(1 + 0.36).'),
           ('Who measures the proper time between the ticks of a clock?', 'An observer at rest relative to the clock', ['Any observer', 'An observer moving at 0.5c', 'An observer moving at c'], 'Ticks at the same place in that frame.')],
    why=[('Explain why both the muon frame and Earth frame give the same prediction for the number of muons reaching the ground.', 'In Earth’s frame the muon lifetime is dilated by γ; in the muon’s frame the atmosphere is length-contracted by γ. Both give the same ratio of travel time to lifetime, so the same fraction survives.'),
         ('Explain why time dilation is symmetric between two inertial observers.', 'Each sees the other’s clock moving and therefore running slow; there is no preferred frame, and the apparent paradox is resolved by the relativity of simultaneity.'),
         ('Explain why relativistic velocity addition never gives a speed greater than c.', 'u = (u′ + v)/(1 + u′v/c²); for u′, v < c the denominator grows enough that u < c, and if u′ = c then u = c exactly.')],
    contrast=[('proper time', 'dilated time', 'Proper time is measured in the frame where the events are at the same place (the shortest interval); dilated time Δt = γΔt₀ is measured by an observer for whom the events are at different places.')],
    misc=[('A moving clock really breaks and runs slow.', 'The clock works perfectly in its own frame; the time dilation is a property of measurements made from another frame.'),
          ('An astronaut travelling fast feels time pass slowly on board.', 'In her own frame everything is normal: her heartbeat and clocks run at the usual rate; it is the observer in another frame who measures her clocks running slow.'),
          ('Length contraction means the object is physically squashed by forces.', 'No forces are involved; different inertial frames measure different lengths because they disagree on simultaneity of the end-point measurements.')],
    evaluate=[('The twin paradox shows that special relativity is self-contradictory.', ['each twin sees the other’s clock run slow, which appears symmetric'], ['the travelling twin changes inertial frames (accelerates) when turning round, so the situation is not symmetric', 'space-time diagrams show the travelling twin’s path has a shorter proper time', 'experiments with atomic clocks on aircraft confirm the asymmetry'], 'There is no contradiction: the asymmetry of the journeys explains why the travelling twin ages less.')],
    extended=[('Muons with a mean lifetime of 2.2 μs (proper) are produced 15 km above the ground and travel downwards at 0.995c. (a) Calculate γ. (b) Calculate the mean lifetime in Earth’s frame and the mean distance travelled before decay. (c) Calculate the thickness of the atmosphere in the muon frame. (d) Explain why many muons are detected at sea level, although without relativity hardly any would be.', '(a) γ = 10.0; (b) 22 μs, 0.995 × 3 × 10⁸ × 22 × 10⁻⁶ = 6.6 km; (c) 15/10 = 1.5 km; (d) the travel time (50 μs in Earth frame) is about 2.3 dilated lifetimes, so e^(−2.3) ≈ 10 % survive, rather than e^(−23) without relativity.', 6)],
))


@prob('ch05-st3', d=(1, 5), md=(1, 4), marks=2)
def p_dilation(rng, slot):
    k = rng.randrange(5)
    b = pick(rng, BETAS); g = gam(b)
    who = name(rng)
    if k == 0:
        t0 = rng.choice([2.2, 1.0, 5.0, 10, 26])
        return dict(stem=f'A process lasting {t0} μs in its own rest frame takes place on a spacecraft moving at {b}c relative to Earth. Calculate its duration measured from Earth.',
                    v=g * t0, unit='μs', wrongs=[t0 / g, t0 * b, t0 * g * g], key=f'Δt = γΔt₀ (M1) = {sf(g)} × {t0} = {sf(g * t0)} μs (A1).')
    if k == 1:
        L0 = rng.choice([50, 80, 100, 120, 200])
        return dict(stem=f'A spacecraft has a proper length of {L0} m. Calculate its length measured by an observer who sees it fly past at {b}c.',
                    v=L0 / g, unit='m', wrongs=[L0 * g, L0 * b, L0 * (1 - b)], key=f'L = L₀/γ (M1) = {L0}/{sf(g)} = {sf(L0 / g)} m (A1).')
    if k == 2:
        u = rng.choice([0.5, 0.6, 0.7, 0.8]); v = rng.choice([0.5, 0.6, 0.7, 0.8])
        w = (u + v) / (1 + u * v)
        return dict(stem=f'Two spacecraft approach each other head-on, moving at {u}c and {v}c relative to a space station. Calculate the speed of one relative to the other, as a fraction of c.',
                    v=w, unit='c', wrongs=[u + v, abs(u - v) / (1 - u * v) if u != v else (u + v) / 2, (u + v) / (1 - u * v) if u * v < 1 and (u + v) / (1 - u * v) < 5 else 1.0], key=f'u′ = (u + v)/(1 + uv/c²) (M1) = {u + v:g}c/(1 + {u * v:g}) = {sf(w)}c (A1).')
    if k == 3:
        D = rng.choice([4.2, 8.6, 10.5, 11.9, 20.4]); star = {4.2: 'Proxima Centauri', 8.6: 'Sirius', 10.5: 'Epsilon Eridani', 11.9: 'Tau Ceti', 20.4: 'Gliese 581'}[D]
        t_ship = D / b / g
        return dict(stem=f'{who} travels from Earth to {star} ({D} ly in Earth’s frame) at {b}c. Calculate the journey time in years measured by {who}’s clock.',
                    v=t_ship, unit='years', wrongs=[D / b, D / b * g, D * g], key=f'Earth time = {D}/{b} = {sf(D / b)} y (M1); proper time = Earth time/γ = {sf(t_ship)} y (A1).')
    t = rng.choice([2.0, 3.0, 4.0, 6.0]); t0 = rng.choice([1.0, 1.5, 2.0, 2.5])
    if t0 >= t:
        return None
    bb = math.sqrt(1 - (t0 / t) ** 2)
    return dict(stem=f'A particle’s proper lifetime is {t0} ns but it is measured in the laboratory to live {t} ns. Determine its speed as a fraction of c.',
                v=bb, unit='c', wrongs=[t0 / t, 1 - t0 / t, math.sqrt(t0 / t)], key=f'γ = {t}/{t0} = {sf(t / t0)} (M1); v/c = √(1 − 1/γ²) = {sf(bb)} (A1).')


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step')
def c4_muon(rng, slot):
    b = pick(rng, [0.98, 0.99, 0.995, 0.999]); g = gam(b); h = rng.choice([10, 12, 15])
    t_earth = h * 1e3 / (b * C)
    frac = 0.5 ** (t_earth / (g * 1.52e-6))
    return num(f'Muons (half-life 1.52 μs in their rest frame) are created {h} km above sea level and move vertically down at {b}c. (a) Calculate the time taken to reach sea level in Earth’s frame. (b) Calculate γ and the half-life in Earth’s frame. (c) Estimate the fraction of muons that reach sea level. (d) Calculate the distance to the ground in the muon frame and show that it leads to the same number of half-lives. (e) State why this experiment was historically important.',
               f'(a) {sf(t_earth * 1e6)} μs; (b) γ = {sf(g)}, half-life {sf(g * 1.52)} μs; (c) ({sf(t_earth / (g * 1.52e-6))} half-lives) fraction ≈ {sf(frac, 2)}; (d) {sf(h / g)} km, time {sf(h * 1e3 / g / (b * C) * 1e6)} μs = same number of proper half-lives; (e) first direct confirmation of time dilation (Rossi–Hall 1941, Frisch–Smith 1963).',
               f'(a) t = d/v (A1). (b) γ, t½ = γ × 1.52 μs (A1). (c) N/N₀ = (½)^n (M1 A1). (d) L = L₀/γ (A1), equivalence (R1). (e) R1.', 7, 'multi_step')


R.mcqs('ch05-st3', 'C2', (1, 4), [
    ('An astronaut moving at 0.8c relative to Earth measures her heartbeat. Compared with Earth-based measurements of her heartbeat, she measures', 'a shorter period', ['a longer period', 'the same period', 'no heartbeat'], 'She measures proper time; Earth sees dilated intervals.'),
    ('A cube moves at 0.6c parallel to one edge. An observer at rest measures its shape as', 'a cuboid shortened in the direction of motion', ['a smaller cube', 'a larger cube', 'an unchanged cube'], 'Contraction only along v.'),
    ('An electron moves at 0.9c relative to a laboratory and emits a photon forwards. In the laboratory, the photon’s speed is', 'c', ['1.9c', '0.1c', '0.9c'], 'Velocity addition with u′ = c gives c.'),
])


R.facts('ch05-st4', F(
    terms=[('spacetime interval', 'the invariant quantity (Δs)² = (cΔt)² − (Δx)², which has the same value in all inertial frames'),
           ('spacetime (Minkowski) diagram', 'a graph with ct on the vertical axis and x on the horizontal axis on which events are points and objects follow worldlines'),
           ('worldline', 'the path of an object through spacetime on a spacetime diagram'),
           ('timelike interval', 'an interval with (cΔt)² > (Δx)², so the events can be causally connected'),
           ('spacelike interval', 'an interval with (Δx)² > (cΔt)², so no signal can connect the events and their order is frame-dependent'),
           ('lightlike interval', 'an interval with (Δs)² = 0, connecting events that a light signal can link')],
    facts=[('On a spacetime diagram with axes x and ct, a light ray is drawn as a line at', '45° to the axes', ['90° to the x-axis', '0° to the x-axis', 'an angle depending on the observer'], 'x = ct.'),
           ('The worldline of an object at rest in frame S on S’s spacetime diagram is', 'a vertical line', ['a horizontal line', 'a line at 45°', 'a curve'], 'x is constant.'),
           ('The ct′ axis of a frame moving at v makes an angle θ with the ct axis where', 'tan θ = v/c', ['sin θ = v/c', 'cos θ = v/c', 'tan θ = c/v'], 'The ct′ axis is the worldline of the S′ origin, x = vt.'),
           ('Which quantity is invariant under the Lorentz transformation?', 'The spacetime interval', ['The time between two events', 'The distance between two events', 'The velocity of an object'], '(Δs)² is the same in all frames.'),
           ('A worldline that is curved on a spacetime diagram represents', 'an accelerating object', ['an object at rest', 'an object moving at constant velocity', 'a light ray'], 'Changing gradient = changing velocity.')],
    why=[('Explain why the proper time between two events is equal to Δs/c.', 'In the frame where the events occur at the same place Δx = 0, so (Δs)² = (cΔt₀)²; the interval is invariant, so Δt₀ = Δs/c in every frame.'),
         ('Explain why events separated by a spacelike interval cannot be cause and effect.', 'For a spacelike interval Δx > cΔt, so a signal would need to travel faster than light to link them; their time order can also be reversed in some frames.'),
         ('Explain how a spacetime diagram shows the relativity of simultaneity.', 'Lines of simultaneity for S are parallel to the x-axis; for S′ they are parallel to the tilted x′ axis, so events on one S line of simultaneity lie at different ct′ values.')],
    contrast=[('a timelike interval', 'a spacelike interval', 'A timelike interval ((cΔt)² > Δx²) can connect cause and effect and has the same time order in all frames; a spacelike interval (Δx² > (cΔt)²) cannot be bridged by any signal, and the time order of the events depends on the frame.')],
    misc=[('Observers in different frames disagree about every quantity in relativity.', 'They agree on invariants: the speed of light, the spacetime interval, proper time and rest mass.'),
          ('The x′ and ct′ axes of a moving frame are perpendicular on the S diagram.', 'Both tilt towards the 45° light line by the same angle θ = tan⁻¹(v/c), so they are not perpendicular on S’s diagram.'),
          ('On a spacetime diagram, the steeper a worldline, the faster the object.', 'With ct vertical, a steeper worldline means a smaller x per ct, i.e. a slower object; a vertical line is at rest.')],
    evaluate=[('Spacetime diagrams are just a teaching aid with no real physical significance.', ['they make simultaneity and twin paradox reasoning visual'], ['they express the geometry of spacetime that underlies general relativity', 'invariant intervals are measurable quantities (proper time)', 'physicists use them to analyse causality'], 'They are more than a teaching aid: they represent the real geometric structure of spacetime, central to modern physics.')],
    extended=[('In frame S, event A is at (x = 0, ct = 0) and event B is at (x = 4.0 m, ct = 3.0 m). (a) Calculate the spacetime interval (Δs)². (b) State whether the interval is timelike or spacelike and what that implies. (c) Determine the speed of a frame in which A and B are simultaneous. (d) Sketch a spacetime diagram showing the events, the light cone of A and the x′ axis of that frame.', '(a) 9 − 16 = −7 m² (spacelike); (b) spacelike: A cannot cause B and their order depends on frame; (c) Δt′ = 0 when v = c²Δt/Δx = (3/4)c = 0.75c; (d) B lies outside A’s light cone; the x′ axis passes through B at slope 3/4.', 6)],
))


@prob('ch05-st4', d=(1, 5), md=(1, 4), marks=2)
def p_interval(rng, slot):
    k = rng.randrange(4)
    if k == 0:
        ct = rng.choice([3.0, 5.0, 6.0, 8.0, 10, 13]); x = rng.choice([2.0, 3.0, 4.0, 6.0, 12])
        s2 = ct * ct - x * x
        return dict(stem=f'Two events are separated by Δx = {x} m and cΔt = {ct} m in frame S. Calculate the spacetime interval (Δs)² = (cΔt)² − (Δx)².',
                    v=s2, unit='m²', wrongs=[ct * ct + x * x, ct - x, (ct - x) ** 2 if ct != x else 1], key=f'(Δs)² = {ct}² − {x}² (M1) = {sf(s2)} m²; {"timelike" if s2 > 0 else "spacelike" if s2 < 0 else "lightlike"} (A1).')
    if k == 1:
        b = pick(rng, [0.30, 0.40, 0.50, 0.60, 0.75, 0.80])
        return dict(stem=f'On a spacetime diagram for frame S, the ct′ axis of a frame S′ moving at {b}c is drawn. Calculate the angle between the ct and ct′ axes.',
                    v=math.degrees(math.atan(b)), unit='°', ans=deg(math.degrees(math.atan(b))), wrongs=[math.degrees(math.asin(b)), math.degrees(math.acos(b)), 90 - math.degrees(math.atan(b))], key=f'tan θ = v/c = {b} (M1); θ = {deg(math.degrees(math.atan(b)))} (A1).')
    if k == 2:
        ct = rng.choice([10, 12, 15, 20]); x = rng.choice([6.0, 8.0, 9.0])
        if x >= ct:
            return None
        tau = math.sqrt(ct * ct - x * x) / C
        return dict(stem=f'A particle travels at constant velocity from event A to event B, separated by Δx = {x} m and cΔt = {ct} m in the laboratory. Calculate the proper time between A and B experienced by the particle.',
                    v=tau * 1e9, unit='ns', wrongs=[ct / C * 1e9, (ct - x) / C * 1e9, math.sqrt(ct * ct + x * x) / C * 1e9], key=f'cΔτ = √((cΔt)² − Δx²) = {sf(math.sqrt(ct * ct - x * x))} m (M1); Δτ = {sf(tau * 1e9)} ns (A1).')
    ct = rng.choice([3.0, 4.0, 5.0]); x = rng.choice([6.0, 8.0, 10])
    return dict(stem=f'Events P and Q are separated by Δx = {x} m and cΔt = {ct} m in frame S. Determine the speed (as a fraction of c) of a frame in which they are simultaneous.',
                v=ct / x, unit='c', wrongs=[x / ct if x / ct < 1 else 0.9, math.sqrt(1 - (ct / x) ** 2), 1 - ct / x], key=f'Δt′ = γ(Δt − vΔx/c²) = 0 (M1); v = c(cΔt)/Δx = {sf(ct / x)}c (A1).')


R.mcqs('ch05-st4', 'C2', (1, 4), [
    ('Two events have (Δs)² > 0. Which is correct?', 'One could have caused the other, and all observers agree on their order', ['No signal can connect them', 'They are simultaneous in some frame', 'They lie on a light ray'], 'Timelike interval.'),
    ('On a spacetime diagram of S, the x′ axis of a frame moving at v in the +x direction', 'tilts upwards from the x-axis by the same angle that ct′ tilts from ct', ['coincides with the x-axis', 'tilts downwards', 'is vertical'], 'Symmetric tilt towards the light line.'),
    ('A spaceship travels from Earth to a star and back. On Earth’s spacetime diagram, the ship’s worldline', 'has a shorter proper time than Earth’s worldline between the same events', ['has a longer proper time', 'has the same proper time', 'is a straight vertical line'], 'Twin paradox geometry.'),
])


def _pion_spec(rng):
    t0 = rng.uniform(25.5, 26.5)  # ns
    bs = [0.50, 0.70, 0.80, 0.90, 0.95, 0.98]
    gs = [gam(b) for b in bs]
    ts = [round(t0 * g * rng.uniform(0.97, 1.03), 1) for g in gs]
    return dict(intro='In an accelerator experiment the mean lifetime τ of charged pions is measured in the laboratory for beams of different speeds v. The Lorentz factor γ is calculated for each speed. Theory: τ = γτ₀.',
                xname='v', xunit='c', yname='τ', yunit='ns', xs=bs, ys=ts, xfmt=lambda x: f'{x:.2f}', yfmt=lambda y: f'{y:.1f}',
                plot_x=lambda x: gam(x), plot_y=lambda y: y, plot_label='τ (y) against γ (x)', what='the proper lifetime τ₀ of the pion', what_short='τ₀',
                gunit='ns', deduce=lambda m_, b_: (m_, 'ns', 'τ₀ = gradient'))


gradient_fit('ch05-st3', _pion_spec)


# =============================================================================================
# ch06 B.1 Thermal energy transfers
# =============================================================================================
SHC = {'water': 4180, 'aluminium': 900, 'copper': 385, 'iron': 450, 'concrete': 880, 'olive oil': 1970, 'glass': 840}
LAT = [('melt', 'ice at 0 °C', 3.34e5), ('boil away', 'water at 100 °C', 2.26e6), ('melt', 'lead at its melting point (327 °C)', 2.3e4), ('vaporize', 'ethanol at its boiling point (78 °C)', 8.5e5)]

R.facts('ch06-st1', F(
    terms=[('density', 'mass per unit volume, ρ = m/V, in kg m⁻³'),
           ('kinetic theory of matter', 'the model in which matter is made of particles in constant random motion whose average kinetic energy depends on temperature'),
           ('solid (particle model)', 'a phase in which particles vibrate about fixed positions and are held close together by strong intermolecular forces'),
           ('liquid (particle model)', 'a phase in which particles are close together but can move past one another'),
           ('gas (particle model)', 'a phase in which particles are far apart, move randomly at high speed and interact only during collisions'),
           ('phase', 'a state of matter (solid, liquid or gas) with uniform physical properties')],
    facts=[('A block of aluminium has mass 0.54 kg and volume 2.0 × 10⁻⁴ m³. Its density is', '2700 kg m⁻³', ['270 kg m⁻³', '1.08 × 10⁻⁴ kg m⁻³', '3.7 × 10⁻⁴ kg m⁻³'], 'ρ = m/V.'),
           ('Why are gases much less dense than solids?', 'The particles are much further apart', ['The particles are smaller', 'The particles are lighter', 'The particles do not move'], 'Same particles, more space.'),
           ('The density of water vapour at 100 °C is roughly 1/1600 of liquid water. The mean spacing of molecules in the vapour is about', '12 times that in the liquid', ['1600 times', '40 times', '3 times'], 'Spacing ∝ (volume)^⅓: 1600^⅓ ≈ 12.'),
           ('Which phase has a definite volume but no definite shape?', 'Liquid', ['Solid', 'Gas', 'Plasma'], 'Particles close but mobile.'),
           ('What is the density of water in kg m⁻³?', '1000 kg m⁻³', ['1 kg m⁻³', '100 kg m⁻³', '10 000 kg m⁻³'], '1 g cm⁻³.')],
    why=[('Explain, using the particle model, why gases are easily compressed but liquids are not.', 'Gas particles are far apart with mostly empty space, so they can be pushed closer; in liquids the particles are already in contact and strong repulsive forces resist compression.'),
         ('Explain why most substances expand when heated.', 'Particles gain kinetic energy and vibrate or move more vigorously, increasing their mean separation, so the volume increases and density decreases.'),
         ('Explain why ice floats on water.', 'Hydrogen bonding holds water molecules in an open lattice in ice, so ice is less dense (≈ 917 kg m⁻³) than liquid water; the upthrust exceeds its weight when fully submerged.')],
    contrast=[('the arrangement of particles in a solid', 'the arrangement of particles in a gas', 'In a solid, particles are closely packed in fixed positions and vibrate; in a gas, they are far apart (≈ 10 diameters) and move freely and randomly with negligible forces between collisions.')],
    misc=[('Particles in a solid do not move.', 'They vibrate continuously about fixed equilibrium positions; their kinetic energy increases with temperature.'),
          ('When a substance expands, its particles get bigger.', 'The particles stay the same size; the mean spacing between them increases.'),
          ('Heavy objects are always dense.', 'Density is mass per unit volume; a large, heavy object such as a ship can have a low average density.')],
    evaluate=[('The simple particle model is sufficient to explain all the properties of matter.', ['explains density differences, compressibility, diffusion and thermal expansion'], ['does not explain water’s density anomaly without hydrogen bonding', 'cannot explain electrical conductivity or magnetism', 'quantum effects matter at low temperatures (superfluids)'], 'The model is powerful for many thermal properties, but more detailed models of bonding and quantum behaviour are needed (NOS: models have limitations).')],
    extended=[('An irregular stone is lowered into a measuring cylinder containing 50.0 cm³ of water; the level rises to 68.5 cm³. The stone has a mass of 49.1 g. (a) Calculate the density of the stone in kg m⁻³. (b) The volume readings have an uncertainty of ±0.5 cm³ and the mass ±0.1 g. Determine the percentage uncertainty in the density. (c) Suggest one improvement to the method. (d) Identify whether the stone would float in mercury (13 600 kg m⁻³).', '(a) V = 18.5 cm³, ρ = 2.65 g cm⁻³ = 2650 kg m⁻³; (b) ΔV = 1.0 cm³ (two readings) → 5.4 %, mass 0.2 %, total ≈ 5.6 %; (c) use a displacement (eureka) can with a narrower cylinder or a density balance; (d) yes – its density is less than mercury’s.', 6)],
))


@prob('ch06-st1', d=(1, 4), md=(1, 4), marks=2)
def p_density(rng, slot):
    k = rng.randrange(4)
    who, city = who_city(rng)
    if k == 0:
        mats = [('aluminium', 2700), ('copper', 8960), ('iron', 7870), ('gold', 19300), ('granite', 2700), ('oak', 750)]
        nm, rho = pick(rng, mats); a = rng.choice([2.0, 3.0, 4.0, 5.0, 8.0])
        V = (a / 100) ** 3; m = rho * V
        return dict(stem=f'{who} measures a cube of {nm} of side {a} cm and finds its mass is {sf(m * 1000)} g. Calculate the density of the material in kg m⁻³.',
                    v=rho, unit='kg m⁻³', wrongs=[m / (a / 100) ** 2, m / V / 1000, m * 1000 / a ** 3], key=f'V = ({a} × 10⁻²)³ = {sf(V)} m³ (M1); ρ = m/V = {sf(rho)} kg m⁻³ (A1).')
    if k == 1:
        r = rng.choice([0.5, 1.0, 1.5, 2.0]) ; rho = rng.choice([7800, 2700, 8900])
        m = rho * 4 / 3 * math.pi * (r / 100) ** 3
        return dict(stem=f'Calculate the mass of a sphere of radius {r} cm made of a metal of density {rho} kg m⁻³.',
                    v=m, unit='kg', wrongs=[rho * (r / 100) ** 3, rho * 4 * math.pi * (r / 100) ** 2, rho * 4 / 3 * math.pi * (r) ** 3 / 1e3], key=f'V = (4/3)πr³ = {sf(4 / 3 * math.pi * (r / 100) ** 3)} m³ (M1); m = ρV = {sf(m)} kg (A1).')
    if k == 2:
        L, W_, Hh = rng.choice([(5.0, 4.0, 3.0), (6.0, 5.0, 2.5), (8.0, 6.0, 3.0), (10, 8, 3.0)])
        m = 1.2 * L * W_ * Hh
        return dict(stem=f'A classroom in {city} measures {L} m × {W_} m × {Hh} m. The density of air is 1.2 kg m⁻³. Calculate the mass of air in the room.',
                    v=m, unit='kg', wrongs=[L * W_ * Hh / 1.2, 1.2 * (L + W_ + Hh), 1.2 * L * W_], key=f'V = {sf(L * W_ * Hh)} m³ (M1); m = ρV = {sf(m)} kg (A1).')
    rl = rng.choice([1000, 13600, 789]); rg = rng.choice([0.60, 0.80, 1.2])
    nm = {1000: 'water', 13600: 'mercury', 789: 'ethanol'}[rl]
    ratio = (rl / rg) ** (1 / 3)
    return dict(stem=f'Liquid {nm} has a density of {rl} kg m⁻³ and its vapour, under certain conditions, has a density of {rg} kg m⁻³. Estimate the ratio of mean molecular spacing in the vapour to that in the liquid.',
                v=ratio, unit='', wrongs=[rl / rg, math.sqrt(rl / rg), (rl / rg) ** 0.25], key=f'Spacing ∝ (1/ρ)^⅓ (M1); ratio = ({rl}/{rg})^⅓ = {sf(ratio)} (A1).')


R.mcqs('ch06-st1', 'C2', (1, 4), [
    ('When water freezes into ice, its density', 'decreases', ['increases', 'stays the same', 'becomes zero'], 'Ice is less dense than water.'),
    ('The mass of a gas in a sealed syringe stays constant while it is compressed to half its volume. Its density', 'doubles', ['halves', 'stays the same', 'quadruples'], 'ρ = m/V.'),
    ('Diffusion is faster in gases than in liquids because gas particles', 'move faster and have larger spacing, so they travel further between collisions', ['are smaller', 'have stronger attractions', 'are not moving randomly'], 'Mean free path is longer.'),
])


R.facts('ch06-st2', F(
    terms=[('temperature', 'a measure of the average random kinetic energy of the particles of a substance; the absolute temperature in kelvin is proportional to it'),
           ('internal energy', 'the total random kinetic energy and intermolecular potential energy of the particles in a substance'),
           ('specific heat capacity', 'the energy required to raise the temperature of 1 kg of a substance by 1 K, c in J kg⁻¹ K⁻¹'),
           ('thermal equilibrium', 'the state in which two bodies in thermal contact are at the same temperature, so there is no net transfer of thermal energy'),
           ('absolute zero', 'the temperature (0 K, −273 °C) at which the random kinetic energy of particles is at a minimum'),
           ('thermal energy (heat)', 'energy transferred from a region of higher temperature to one of lower temperature')],
    facts=[('What temperature in kelvin corresponds to 27 °C?', '300 K', ['246 K', '27 K', '373 K'], 'T(K) = θ(°C) + 273.'),
           ('How much energy is needed to heat 2.0 kg of water by 10 K? (c = 4180 J kg⁻¹ K⁻¹)', '83.6 kJ', ['8.36 kJ', '836 kJ', '41.8 kJ'], 'Q = mcΔT.'),
           ('A temperature change of 15 °C is equal to a temperature change of', '15 K', ['288 K', '258 K', '15 °F'], 'The degree sizes are equal.'),
           ('Thermal energy flows between two bodies in contact until they have the same', 'temperature', ['internal energy', 'specific heat capacity', 'mass'], 'Thermal equilibrium.'),
           ('Water is used in central heating systems mainly because it has', 'a high specific heat capacity', ['a low boiling point', 'a high density', 'a low viscosity'], 'Stores much energy per kelvin.')],
    why=[('Explain why coastal cities have smaller daily temperature ranges than inland cities.', 'Water has a very high specific heat capacity, so the sea warms and cools slowly, absorbing energy by day and releasing it by night and moderating the air temperature.'),
         ('Explain the difference between temperature and internal energy using a bath and a cup of tea.', 'The tea is hotter (higher mean kinetic energy per particle), but the bath has far more particles and so much more total internal energy.'),
         ('Explain why the measured specific heat capacity of a metal block in a school experiment is usually higher than the true value.', 'Energy is lost to the surroundings and to the heater and thermometer, so more energy is supplied than goes into the block, giving c = Q/(mΔT) too large.')],
    contrast=[('temperature', 'internal energy', 'Temperature is related to the average random kinetic energy per particle; internal energy is the total random kinetic plus intermolecular potential energy of all the particles, so it also depends on the amount and phase of the substance.')],
    misc=[('Heat and temperature are the same thing.', 'Temperature measures average particle kinetic energy; heat is energy transferred because of a temperature difference.'),
          ('An object at 0 °C contains no internal energy.', '0 °C is 273 K; its particles still have kinetic and potential energy. Only at absolute zero is the kinetic energy at a minimum.'),
          ('Doubling the temperature in °C doubles the average kinetic energy of the particles.', 'Average kinetic energy is proportional to absolute temperature; 20 °C → 40 °C is 293 K → 313 K, an increase of only about 7 %.')],
    evaluate=[('Water’s high specific heat capacity is the main reason Earth’s climate is habitable.', ['oceans store huge amounts of energy, moderating temperature swings', 'ocean currents redistribute energy from equator to poles'], ['the greenhouse effect and atmospheric composition are also essential', 'distance from the Sun and albedo determine the overall temperature', 'water vapour and clouds also matter'], 'Water’s heat capacity is a key moderating factor, but habitability depends on a combination of energy balance, the greenhouse effect and the water cycle.')],
    extended=[('A 1.20 kg aluminium block is heated by a 50.0 W immersion heater for 6.00 min; its temperature rises from 20.5 °C to 35.8 °C. (a) Calculate the energy supplied. (b) Determine the specific heat capacity of aluminium from the data. (c) The accepted value is 900 J kg⁻¹ K⁻¹; calculate the percentage difference and suggest the main reason. (d) Describe two improvements.', '(a) 18 000 J; (b) c = 18 000/(1.20 × 15.3) = 980 J kg⁻¹ K⁻¹; (c) 8.9 % high – energy lost to the surroundings; (d) insulate the block (lagging), put oil in the thermometer and heater holes, start below room temperature and finish the same amount above it.', 6)],
))


@prob('ch06-st2', d=(1, 5), md=(1, 4), marks=2)
def p_shc(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        nm = pick(rng, list(SHC)); c_ = SHC[nm]; m = rng.choice([0.20, 0.50, 1.2, 2.0, 3.5]); dT = rng.choice([8, 15, 25, 40, 60])
        return dict(stem=f'Calculate the energy needed to raise the temperature of {m} kg of {nm} (c = {c_} J kg⁻¹ K⁻¹) by {dT} K.',
                    v=m * c_ * dT, unit='J', wrongs=[c_ * dT, m * c_ * (dT + 273), m * c_ / dT], key=f'Q = mcΔT (M1) = {m} × {c_} × {dT} = {sf(m * c_ * dT)} J (A1).')
    if k == 1:
        P = rng.choice([1500, 2000, 2200, 3000]); m = rng.choice([0.5, 1.0, 1.5, 1.7]); T1 = rng.choice([12, 15, 18, 20])
        t = m * 4180 * (100 - T1) / P
        return dict(stem=f'{who}’s {P} W kettle in {city} contains {m} kg of water at {T1} °C. Calculate the minimum time to bring the water to boiling point.',
                    v=t, unit='s', wrongs=[m * 4180 * 100 / P, m * 4180 * (100 - T1) * P / 1e6, m * 4180 * (373 - T1) / P], key=f'Q = mcΔT = {sf(m * 4180 * (100 - T1))} J (M1); t = Q/P = {sf(t)} s (A1).')
    if k == 2:
        m1 = rng.choice([0.20, 0.30, 0.40]); T1 = rng.choice([80, 85, 90]); m2 = rng.choice([0.10, 0.20, 0.30]); T2 = rng.choice([10, 15, 20])
        Tf = (m1 * T1 + m2 * T2) / (m1 + m2)
        return dict(stem=f'{m1} kg of water at {T1} °C is mixed with {m2} kg of water at {T2} °C in an insulated flask. Calculate the final temperature.',
                    v=Tf, unit='°C', wrongs=[(T1 + T2) / 2, (m2 * T1 + m1 * T2) / (m1 + m2), T1 - T2], key=f'Energy lost = energy gained: {m1}c({T1} − T) = {m2}c(T − {T2}) (M1); T = {sf(Tf)} °C (A1).')
    if k == 3:
        nm = pick(rng, ['aluminium', 'copper', 'iron']); c_ = SHC[nm]; mb = rng.choice([0.20, 0.30, 0.50]); Tb = rng.choice([95, 100])
        mw = rng.choice([0.15, 0.20, 0.25]); Tw = rng.choice([18, 20, 22])
        Tf = (mb * c_ * Tb + mw * 4180 * Tw) / (mb * c_ + mw * 4180)
        return dict(stem=f'A {mb} kg {nm} block (c = {c_} J kg⁻¹ K⁻¹) at {Tb} °C is dropped into {mw} kg of water at {Tw} °C in an insulated cup. Calculate the final temperature.',
                    v=Tf, unit='°C', wrongs=[(Tb + Tw) / 2, (mb * Tb + mw * Tw) / (mb + mw), (mb * 4180 * Tb + mw * c_ * Tw) / (mb * 4180 + mw * c_)], key=f'm_b c_b(T_b − T) = m_w c_w(T − T_w) (M1 M1); T = {sf(Tf)} °C (A1).', marks=3)
    P = rng.choice([24, 36, 48, 60]); t = rng.choice([300, 480, 600]); m = rng.choice([0.80, 1.0, 1.2]); dT = rng.choice([12.0, 15.5, 18.0, 25.0])
    return dict(stem=f'In a lab in {city}, a {P} W heater raises the temperature of a {m} kg metal block by {dT} K in {t} s. Determine the specific heat capacity of the metal, assuming no losses.',
                v=P * t / (m * dT), unit='J kg⁻¹ K⁻¹', wrongs=[P * t * m / dT, P / (m * dT), P * t / (m * (dT + 273))], key=f'Q = Pt = {P * t} J (M1); c = Q/(mΔT) = {sf(P * t / (m * dT))} J kg⁻¹ K⁻¹ (A1).')


R.mcqs('ch06-st2', 'C2', (1, 4), [
    ('Equal masses of water and copper receive the same energy. Which is correct?', 'The copper has the larger temperature rise', ['The water has the larger temperature rise', 'Both have the same rise', 'Neither changes temperature'], 'c(copper) ≪ c(water).'),
    ('Two objects at different temperatures are placed in contact. Energy is transferred from', 'the hotter to the colder object', ['the one with more internal energy to the one with less', 'the larger to the smaller', 'the denser to the less dense'], 'Temperature difference drives heat flow.'),
    ('The temperature of a gas in kelvin doubles. The mean kinetic energy of its molecules', 'doubles', ['quadruples', 'is unchanged', 'increases by √2'], 'Eₖ ∝ T.'),
])


def _shc_spec(rng):
    m = 1.00; c_ = rng.uniform(850, 950); P = 48.0
    ts = [60, 120, 180, 240, 300, 360]
    Ts = [round(20.0 + P * t / (m * c_) * rng.uniform(0.97, 1.0), 1) for t in ts]
    return dict(intro='A 1.00 kg aluminium block is heated by a 48.0 W heater. The temperature θ is recorded every minute. Theory (no losses): Pt = mc(θ − θ₀).',
                xname='t', xunit='s', yname='θ', yunit='°C', xs=ts, ys=Ts, xfmt=lambda x: f'{x}', yfmt=lambda y: f'{y:.1f}',
                plot_x=lambda x: x, plot_y=lambda y: y, plot_label='θ (y) against t (x)', what='the specific heat capacity c of aluminium', what_short='c',
                gunit='K s⁻¹', deduce=lambda m_, b_: (48.0 / (1.00 * m_), 'J kg⁻¹ K⁻¹', 'c = P/(m × gradient)'))


gradient_fit('ch06-st2', _shc_spec)
repeat_readings('ch06-st2', 'the final temperature of the water', '°C', 30.0, 40.0, 1,
                ['repeated a method-of-mixtures experiment with hot copper and cold water.', 'measured the equilibrium temperature after dropping a heated block into water.'])


R.facts('ch06-st3', F(
    terms=[('specific latent heat of fusion', 'the energy required to change 1 kg of a substance from solid to liquid without a change in temperature'),
           ('specific latent heat of vaporization', 'the energy required to change 1 kg of a substance from liquid to gas without a change in temperature'),
           ('melting point', 'the temperature at which a solid changes to a liquid at a given pressure'),
           ('evaporation', 'the escape of the most energetic molecules from the surface of a liquid at any temperature below its boiling point'),
           ('boiling', 'vaporization occurring throughout the liquid at the temperature at which its vapour pressure equals the external pressure')],
    facts=[('During melting, the temperature of a pure substance', 'stays constant', ['rises steadily', 'falls', 'rises then falls'], 'Energy goes into breaking bonds (potential energy).'),
           ('Energy needed to melt 0.50 kg of ice at 0 °C (L = 3.34 × 10⁵ J kg⁻¹) is', '1.67 × 10⁵ J', ['6.68 × 10⁵ J', '3.34 × 10⁵ J', '1.67 × 10⁴ J'], 'Q = mL.'),
           ('During a change of phase, the energy supplied increases the', 'potential energy of the particles', ['kinetic energy of the particles', 'temperature', 'mass'], 'Temperature (and mean KE) constant.'),
           ('Why is the specific latent heat of vaporization of water much larger than that of fusion?', 'Vaporization separates molecules completely and does work against the atmosphere', ['Water vapour is hotter', 'Ice is a crystal', 'Boiling happens at higher pressure'], 'All intermolecular bonds are broken.'),
           ('Evaporation cools a liquid because', 'the most energetic molecules escape, lowering the mean kinetic energy of those left', ['the liquid loses mass', 'air is colder than the liquid', 'the liquid boils'], 'Selective escape.')],
    why=[('Explain why a scald from steam at 100 °C is more severe than one from water at 100 °C.', 'Steam condensing on the skin releases its large latent heat of vaporization (2.26 MJ kg⁻¹) in addition to the energy released as the water cools.'),
         ('Explain, in terms of particles, why the temperature of a substance remains constant while it boils.', 'The energy supplied increases the potential energy of the particles as intermolecular bonds are broken, not their mean kinetic energy, so the temperature is constant.'),
         ('Explain why sweating helps to keep the body cool.', 'Sweat evaporates, taking latent heat from the skin; the most energetic molecules leave, lowering the temperature of the remaining liquid and skin.')],
    contrast=[('evaporation', 'boiling', 'Evaporation occurs only at the surface and at any temperature, with the most energetic molecules escaping; boiling occurs throughout the liquid at a fixed temperature (for a given pressure), with bubbles of vapour forming.')],
    misc=[('Adding more heat to boiling water makes it hotter.', 'The temperature stays at the boiling point; extra power only makes it boil away faster.'),
          ('Ice at 0 °C and water at 0 °C have the same internal energy.', 'The water has more internal energy: the latent heat of fusion has increased the potential energy of its molecules.'),
          ('Latent heat is called "hidden" because it is not real energy.', 'It is real energy that changes the potential energy of the particles; it is "hidden" only because no temperature change occurs.')],
    evaluate=[('Ice packs are more effective than cold water packs of the same mass and temperature for treating sports injuries.', ['melting ice absorbs 334 kJ kg⁻¹ at constant 0 °C', 'keeps a steady low temperature for longer'], ['ice can damage skin if applied directly', 'gel packs offer flexibility', 'cold water is easier to control and less extreme'], 'Ice absorbs far more energy per kilogram because of latent heat, so it cools longer, though care and comfort matter in practice.')],
    extended=[('A 0.250 kg block of ice at −15.0 °C is placed in a kettle and heated until all of it has become steam at 100 °C. c(ice) = 2100 J kg⁻¹ K⁻¹, c(water) = 4180 J kg⁻¹ K⁻¹, L_f = 3.34 × 10⁵ J kg⁻¹, L_v = 2.26 × 10⁶ J kg⁻¹. (a) Sketch the temperature–time graph. (b) Calculate the energy for each stage and the total. (c) Explain why the boiling stage lasts much longer than the melting stage. (d) The kettle supplies 2.0 kW; estimate the total time.', '(a) rise, flat at 0 °C, rise, flat at 100 °C; (b) 7.9 kJ + 83.5 kJ + 104.5 kJ + 565 kJ = 761 kJ; (c) L_v is about 6.8 times L_f; (d) 380 s (longer in practice owing to losses).', 6)],
))


@prob('ch06-st3', d=(1, 5), md=(1, 4), marks=2)
def p_latent(rng, slot):
    k = rng.randrange(5)
    who, city = who_city(rng)
    if k == 0:
        vb, nm, L = pick(rng, LAT); m = rng.choice([0.050, 0.10, 0.25, 0.50, 1.5])
        return dict(stem=f'Calculate the energy needed to {vb} {m} kg of {nm} (specific latent heat {sf(L)} J kg⁻¹).',
                    v=m * L, unit='J', wrongs=[L / m, m * L / 1000, m * L * 4.18], key=f'Q = mL (M1) = {m} × {sf(L)} = {sf(m * L)} J (A1).')
    if k == 1:
        P = rng.choice([1500, 2000, 2400]); t = rng.choice([60, 90, 120, 180])
        m = P * t / 2.26e6
        return dict(stem=f'A {P} W kettle is left boiling for {t} s after reaching 100 °C. Calculate the mass of water boiled away (L_v = 2.26 × 10⁶ J kg⁻¹).',
                    v=m, unit='kg', wrongs=[P * t / 3.34e5, P / 2.26e6, P * t / (4180 * 100)], key=f'Pt = mL (M1); m = {P} × {t}/2.26 × 10⁶ = {sf(m)} kg (A1).')
    if k == 2:
        mi = rng.choice([0.020, 0.030, 0.040, 0.050]); mw = rng.choice([0.20, 0.25, 0.30]); T = rng.choice([25, 30, 35])
        Tf = (mw * 4180 * T - mi * 3.34e5) / ((mw + mi) * 4180)
        if Tf <= 0:
            return None
        return dict(stem=f'{who} drops {mi * 1000:g} g of ice at 0 °C into {mw} kg of lemonade (treat as water) at {T} °C in an insulated cup in {city}. Calculate the final temperature once all the ice has melted.',
                    v=Tf, unit='°C', wrongs=[(mw * T) / (mw + mi), (mw * 4180 * T - mi * 3.34e5) / (mw * 4180), T - mi * 3.34e5 / (mw * 4180) * 2], key=f'Energy from lemonade = energy to melt ice + warm meltwater: {mw}c({T} − T) = {mi}L_f + {mi}cT (M1 M1); T = {sf(Tf)} °C (A1).', marks=3)
    if k == 3:
        m = rng.choice([0.10, 0.20, 0.50]); T1 = rng.choice([15, 20, 25])
        Q = m * 4180 * (100 - T1) + m * 2.26e6
        return dict(stem=f'Calculate the total energy needed to turn {m} kg of water at {T1} °C completely into steam at 100 °C.',
                    v=Q, unit='J', wrongs=[m * 2.26e6, m * 4180 * (100 - T1), m * 4180 * (100 - T1) + m * 3.34e5], key=f'Heating: {sf(m * 4180 * (100 - T1))} J (M1); vaporizing: {sf(m * 2.26e6)} J (M1); total {sf(Q)} J (A1).', marks=3)
    P = rng.choice([30, 40, 50, 60]); t = rng.choice([200, 300, 400]); dm = rng.choice([0.0045, 0.0060, 0.0080])
    return dict(stem=f'A {P} W immersion heater in boiling ethanol in a lab in {city} evaporates {dm * 1000:g} g of ethanol in {t} s. Determine the specific latent heat of vaporization of ethanol from these data (ignore losses).',
                v=P * t / dm, unit='J kg⁻¹', wrongs=[P / dm, P * t * dm, P * t / dm / 1000], key=f'L = Pt/m (M1) = {P} × {t}/{dm} = {sf(P * t / dm)} J kg⁻¹ (A1).')


R.mcqs('ch06-st3', 'C2', (1, 4), [
    ('Heat is supplied at a constant rate to a solid. Its temperature–time graph shows a horizontal section. During this section', 'the substance is changing phase', ['no energy is being absorbed', 'the particles are speeding up', 'the heater has been switched off'], 'Energy goes into potential energy.'),
    ('Water at 100 °C and steam at 100 °C have', 'the same mean molecular kinetic energy but different potential energy', ['the same internal energy', 'different mean kinetic energies', 'the same density'], 'Same temperature; steam has more PE.'),
    ('Why does blowing across hot soup cool it faster?', 'It removes vapour, increasing the rate of evaporation', ['It adds cold air molecules to the soup', 'It increases the latent heat', 'It decreases the specific heat capacity'], 'Evaporation carries away latent heat.'),
])


R.facts('ch06-st4', F(
    terms=[('conduction', 'the transfer of thermal energy through a material by collisions between neighbouring particles and, in metals, by free electrons'),
           ('convection', 'the transfer of thermal energy by the bulk movement of a fluid caused by density differences'),
           ('thermal radiation', 'the transfer of energy by electromagnetic waves, mainly infrared, emitted by all objects above absolute zero'),
           ('black body', 'an idealised object that absorbs all incident radiation and emits the maximum possible radiation at each wavelength for its temperature'),
           ('Stefan–Boltzmann law', 'the total power radiated by a black body is P = σAT⁴'),
           ('Wien’s displacement law', 'the wavelength of peak emission of a black body is inversely proportional to its absolute temperature, λ_max T = 2.9 × 10⁻³ m K'),
           ('thermal conductivity', 'the property k of a material in the rate of conduction ΔQ/Δt = kA ΔT/Δx')],
    facts=[('Which method of energy transfer can occur through a vacuum?', 'Radiation', ['Conduction', 'Convection', 'Evaporation'], 'Electromagnetic waves need no medium.'),
           ('If the absolute temperature of a black body doubles, its radiated power', 'increases by a factor of 16', ['doubles', 'quadruples', 'increases by a factor of 8'], 'P ∝ T⁴.'),
           ('The Sun’s spectrum peaks at about 500 nm. Its surface temperature is approximately', '5800 K', ['580 K', '58 000 K', '1450 K'], 'T = 2.9 × 10⁻³/500 × 10⁻⁹.'),
           ('Metals are good conductors of thermal energy mainly because', 'they contain free (delocalised) electrons', ['their atoms are heavy', 'they are dense', 'they are shiny'], 'Electrons carry energy quickly.'),
           ('Convection cannot occur in solids because', 'the particles cannot move from place to place', ['solids are too dense', 'solids do not expand', 'solids absorb radiation'], 'Bulk flow is needed.'),
           ('Which unit is correct for thermal conductivity?', 'W m⁻¹ K⁻¹', ['W m⁻² K⁻⁴', 'J kg⁻¹ K⁻¹', 'W K⁻¹'], 'From ΔQ/Δt = kAΔT/Δx.')],
    why=[('Explain why double glazing reduces energy loss from a house.', 'The gap between the panes contains a gas (or vacuum) of very low thermal conductivity and is narrow enough to limit convection, so conduction through the window is greatly reduced.'),
         ('Explain why a red-hot piece of iron looks red, while a hotter piece looks white.', 'By Wien’s law the peak wavelength decreases as temperature rises; at ~1000 K the visible emission is mainly red, at higher temperatures the spectrum covers all visible wavelengths more evenly and appears white.'),
         ('Explain how convection currents form above a radiator.', 'Air next to the radiator is heated, expands and becomes less dense, so it rises; cooler, denser air sinks to replace it, setting up a circulating current.'),
         ('Explain why a vacuum flask keeps drinks hot.', 'The vacuum between the double walls prevents conduction and convection; silvered surfaces reduce radiation; the stopper reduces evaporation and convection at the top.')],
    contrast=[('conduction', 'convection', 'Conduction transfers energy through collisions between particles (and free electrons) without bulk movement; convection transfers energy by bulk movement of a fluid driven by density differences.'),
              ('a black body', 'a real surface with emissivity e < 1', 'A black body absorbs all radiation and emits the maximum σAT⁴; a real surface emits only eσAT⁴ and reflects or transmits some incident radiation.')],
    misc=[('Cold objects do not emit any radiation.', 'All objects above 0 K emit thermal radiation; cold objects emit less power, at longer wavelengths.'),
          ('Heat rises.', 'Hot fluid rises because it is less dense; thermal energy itself can be transferred in any direction (e.g. conduction downwards, radiation).'),
          ('A hotter black body emits less at long wavelengths than a cooler one.', 'A hotter black body emits more at every wavelength; its peak simply moves to shorter wavelengths.')],
    evaluate=[('Insulating the loft is always the most cost-effective way to reduce a house’s heating bill.', ['about a quarter of heat is lost through an uninsulated roof', 'loft insulation is cheap with a short payback time'], ['draughts, walls and windows may be bigger losses in some houses', 'already-insulated lofts have diminishing returns', 'heat-pump installation can reduce bills further'], 'Loft insulation is often the cheapest first step, but the best choice depends on the house; a survey of where energy is lost should guide decisions.')],
    extended=[('A glass window is 1.5 m × 1.2 m and 4.0 mm thick; the thermal conductivity of glass is 0.80 W m⁻¹ K⁻¹. The inner and outer surfaces are at 18 °C and 4 °C. (a) Calculate the rate of conduction through the glass. (b) A double-glazed unit has a 12 mm air gap (k = 0.024 W m⁻¹ K⁻¹); estimate the rate of conduction through the air gap with the same temperature difference. (c) Explain why the real reduction is smaller than this estimate. (d) Calculate the energy saved over one day (24 h).', '(a) 0.80 × 1.8 × 14/0.004 = 5.0 kW; (b) 0.024 × 1.8 × 14/0.012 = 50 W; (c) the surfaces are not at 18 °C and 4 °C – air films and radiation across the gap transfer energy, convection occurs in the gap; (d) (5040 − 50) W × 86 400 s ≈ 4.3 × 10⁸ J (much less in reality).', 6)],
))


@prob('ch06-st4', d=(1, 5), md=(1, 4), marks=2)
def p_radiation(rng, slot):
    k = rng.randrange(6)
    city = rng.choice(CITIES)
    if k == 0:
        T = rng.choice([3000, 3500, 4500, 5800, 7500, 10000, 25000])
        lam = WIEN / T
        return dict(stem=f'A star has a surface temperature of {T} K. Calculate the wavelength at which its emission peaks.',
                    v=lam, unit='m', wrongs=[WIEN * T / 1e8, lam * 10, WIEN / (T - 273)], key=f'λ_max = 2.9 × 10⁻³/T (M1) = {sf(lam)} m (A1).')
    if k == 1:
        lam = rng.choice([290, 350, 500, 650, 800, 10000]) * 1e-9
        return dict(stem=f'The emission spectrum of an object peaks at {sf(lam * 1e9, 3)} nm. Estimate its surface temperature, treating it as a black body.',
                    v=WIEN / lam, unit='K', wrongs=[WIEN / lam - 273, lam / WIEN * 1e10, WIEN / (lam * 10)], key=f'T = 2.9 × 10⁻³/λ_max (M1) = {sf(WIEN / lam)} K (A1).')
    if k == 2:
        T = rng.choice([310, 350, 400, 600, 1000, 1500]); A = rng.choice([0.010, 0.050, 0.20, 1.0, 1.8])
        P = SIGMA * A * T ** 4
        return dict(stem=f'Calculate the power radiated by a black body of surface area {A} m² at a temperature of {T} K.',
                    v=P, unit='W', wrongs=[SIGMA * A * T, SIGMA * T ** 4, SIGMA * A * T ** 2], key=f'P = σAT⁴ (M1) = 5.67 × 10⁻⁸ × {A} × {T}⁴ = {sf(P)} W (A1).')
    if k == 3:
        e = rng.choice([0.80, 0.90, 0.95, 0.97]); A = rng.choice([1.6, 1.8, 2.0]); Ts = rng.choice([305, 307, 309]); Te = rng.choice([288, 293, 298])
        Pn = e * SIGMA * A * (Ts ** 4 - Te ** 4)
        return dict(stem=f'A person with skin area {A} m², skin temperature {Ts} K and emissivity {e} stands in a room in {city} at {Te} K. Calculate the net power lost by radiation.',
                    v=Pn, unit='W', wrongs=[e * SIGMA * A * Ts ** 4, e * SIGMA * A * (Ts - Te) ** 4, SIGMA * A * (Ts ** 4 - Te ** 4)], key=f'P_net = eσA(T_s⁴ − T_e⁴) (M1) = {sf(Pn)} W (A1).')
    if k == 4:
        kc = rng.choice([0.80, 1.0, 0.040, 0.17, 205]); mat = {0.80: 'glass', 1.0: 'brick', 0.040: 'fibreglass insulation', 0.17: 'wood', 205: 'aluminium'}[kc]
        A = rng.choice([0.50, 1.0, 2.0, 10]); dx = rng.choice([0.005, 0.010, 0.10, 0.20]); dT = rng.choice([5, 10, 15, 20])
        P = kc * A * dT / dx
        return dict(stem=f'A sheet of {mat} (thermal conductivity {kc} W m⁻¹ K⁻¹) has area {A} m² and thickness {dx * 1000:g} mm. Its faces are at a temperature difference of {dT} K. Calculate the rate of thermal energy transfer by conduction.',
                    v=P, unit='W', wrongs=[kc * A * dT * dx, kc * dT / dx, kc * A / (dT * dx)], key=f'ΔQ/Δt = kAΔT/Δx (M1) = {sf(P)} W (A1).')
    T1 = rng.choice([300, 400, 500, 600]); f = rng.choice([1.5, 2.0, 3.0])
    return dict(stem=f'The absolute temperature of a hot plate rises from {T1} K to {sf(T1 * f)} K. By what factor does the power it radiates increase?',
                v=f ** 4, unit='', wrongs=[f, f ** 2, f ** 3], key=f'P ∝ T⁴ (M1); factor = {f}⁴ = {sf(f ** 4)} (A1).')


@R.add('ch06-st4', 'C4', (3, 5), 'multi_step')
def c4_sun_radiation(rng, slot):
    k = rng.randrange(2)
    if k == 0:
        T = rng.choice([5770, 5800]); 
        L = SIGMA * 4 * math.pi * R_SUN ** 2 * T ** 4
        I = L / (4 * math.pi * AU ** 2)
        return num(f'The Sun (radius 6.96 × 10⁸ m) has a surface temperature of {T} K and may be treated as a black body. Earth is 1.50 × 10¹¹ m from the Sun. (a) Calculate the peak wavelength of solar radiation. (b) Calculate the luminosity of the Sun. (c) Determine the intensity of solar radiation at Earth’s distance. (d) Explain why the intensity at Earth’s surface is less than this.',
                   f'(a) {sf(WIEN / T)} m; (b) {sf(L)} W; (c) {sf(I)} W m⁻²; (d) the atmosphere reflects (clouds), scatters and absorbs part of the radiation, and the angle of incidence spreads it over a larger area.',
                   f'(a) Wien (A1). (b) L = σ4πR²T⁴ (M1 A1). (c) I = L/(4πd²) (M1 A1). (d) R1.', 6, 'multi_step')
    T = rng.choice([1800, 2500, 2800]); A = rng.choice([5.0e-5, 8.0e-5]); e = rng.choice([0.30, 0.35])
    P = e * SIGMA * A * T ** 4
    return num(f'The tungsten filament of a lamp has a surface area of {sf(A, 2)} m², emissivity {e} and operating temperature {T} K. (a) Calculate the power radiated. (b) Calculate the peak wavelength and state the region of the spectrum. (c) Explain why filament lamps are inefficient as light sources. (d) Suggest why running the filament hotter would improve efficiency but shorten its life.',
               f'(a) {sf(P)} W; (b) {sf(WIEN / T)} m, infrared; (c) most of the radiated power is infrared, not visible; (d) the peak shifts towards the visible, but tungsten evaporates faster at higher temperature.',
               f'(a) P = eσAT⁴ (M1 A1). (b) A1 + region (A1). (c) R1. (d) R1.', 6, 'multi_step')


R.mcqs('ch06-st4', 'C2', (1, 4), [
    ('A metal spoon and a wooden spoon have been in a drawer at the same temperature. The metal spoon feels colder because', 'it conducts thermal energy away from the hand faster', ['it is at a lower temperature', 'it radiates more', 'it contains less internal energy'], 'Same temperature, higher conductivity.'),
    ('Two black bodies X and Y have the same area; X is at 600 K and Y at 300 K. The ratio of power radiated X : Y is', '16 : 1', ['2 : 1', '4 : 1', '8 : 1'], 'P ∝ T⁴.'),
    ('As the temperature of a black body increases, the peak of its spectrum', 'moves to shorter wavelength and becomes higher', ['moves to longer wavelength', 'stays at the same wavelength', 'becomes lower'], 'Wien and Stefan–Boltzmann.'),
    ('The main process transferring energy from the Sun to Earth is', 'radiation', ['conduction', 'convection', 'both conduction and convection'], 'Space is a vacuum.'),
])


def _cooling_spec(rng):
    A = 0.010; e = rng.uniform(0.85, 0.98)
    Ts = [400, 450, 500, 550, 600, 650]
    Ps = [round(e * SIGMA * A * T ** 4 * rng.uniform(0.97, 1.03), 1) for T in Ts]
    return dict(intro='A small blackened metal plate of surface area 0.010 m² is heated electrically in a vacuum chamber. When it reaches a steady temperature T, the electrical power P supplied equals the power radiated. Theory: P = eσAT⁴.',
                xname='T', xunit='K', yname='P', yunit='W', xs=Ts, ys=Ps, xfmt=lambda x: f'{x}', yfmt=lambda y: f'{y:.1f}',
                plot_x=lambda x: x ** 4, plot_y=lambda y: y, plot_label='P (y) against T⁴ (x)', what='the emissivity e of the plate', what_short='e',
                gunit='W K⁻⁴', deduce=lambda m_, b_: (m_ / (SIGMA * 0.010), '', 'e = gradient/(σA)'))


gradient_fit('ch06-st4', _cooling_spec)


# =============================================================================================
# ch07 B.2 Greenhouse effect
# =============================================================================================
S0 = 1360.0

R.facts('ch07-st1', F(
    terms=[('emissivity', 'the ratio of the power radiated per unit area by a surface to that radiated by a black body at the same temperature, e = P/(σAT⁴)'),
           ('albedo', 'the fraction of incident radiation that is reflected (or scattered) by a surface or planet: total scattered power / total incident power'),
           ('black-body radiation', 'the continuous spectrum of electromagnetic radiation emitted by an ideal black body, whose shape depends only on temperature'),
           ('solar constant', 'the intensity of solar radiation incident on a plane perpendicular to the rays at the top of Earth’s atmosphere, about 1360 W m⁻²'),
           ('intensity', 'power per unit area perpendicular to the direction of energy flow, in W m⁻²')],
    facts=[('Earth’s mean albedo is about', '0.30', ['0.03', '0.70', '1.0'], 'About 30 % of incident sunlight is reflected.'),
           ('Which surface has the highest albedo?', 'Fresh snow', ['Ocean', 'Forest', 'Asphalt'], 'Snow reflects up to ~0.9.'),
           ('A black body has an emissivity of', '1', ['0', '0.5', 'greater than 1'], 'Maximum possible emission.'),
           ('A surface with emissivity 0.6 at 300 K radiates, compared with a black body at 300 K,', '60 % of the power per unit area', ['40 %', '60 % more', 'the same'], 'P = eσAT⁴.'),
           ('Albedo has units of', 'none – it is a ratio', ['W m⁻²', 'K', 'W m⁻² K⁻⁴'], 'Ratio of powers.')],
    why=[('Explain why melting Arctic sea ice can accelerate warming.', 'Ice has a high albedo and open ocean a low albedo; replacing ice with water means more solar radiation is absorbed, warming the region and melting more ice (positive feedback).'),
         ('Explain why Earth’s albedo varies from day to day.', 'Albedo depends on cloud cover, snow and ice cover, vegetation and the angle of incidence of sunlight, all of which change with weather and season.'),
         ('Explain why a good absorber of radiation is also a good emitter.', 'For a body in thermal equilibrium, power absorbed must equal power emitted at each wavelength; a surface with high absorptivity must therefore have high emissivity (Kirchhoff’s law of radiation).')],
    contrast=[('emissivity', 'albedo', 'Emissivity describes how well a surface emits radiation compared with a black body at the same temperature; albedo is the fraction of incident radiation that a surface reflects.')],
    misc=[('Clouds always cool the planet.', 'Clouds reflect sunlight (cooling) but also absorb and re-emit infrared (warming); the net effect depends on cloud type and height.'),
          ('A planet with albedo 0 absorbs no radiation.', 'Albedo 0 means nothing is reflected, so all incident radiation is absorbed.'),
          ('Only hot objects emit black-body radiation.', 'All objects above 0 K emit; Earth at about 288 K emits mainly in the infrared around 10 μm.')],
    evaluate=[('Painting city roofs white is an effective way to combat global warming.', ['raises the local albedo, reducing absorbed sunlight and urban heat island effects', 'cheap and immediate'], ['global effect is small because roofs are a tiny fraction of Earth’s area', 'can increase heating demand in winter', 'does not address CO₂ emissions'], 'White roofs are a useful local adaptation that lowers building temperatures, but on their own they make only a small contribution to tackling global warming.')],
    extended=[('A solar thermal collector of area 2.5 m² receives sunlight of intensity 800 W m⁻². Its surface has albedo 0.08 and emissivity 0.10 (a selective coating). (a) Calculate the power absorbed. (b) The plate reaches 360 K; calculate the power it radiates. (c) Explain why a low emissivity coating is chosen. (d) Determine the maximum power available to heat water if the surroundings are at 290 K (net radiation only).', '(a) 0.92 × 800 × 2.5 = 1840 W; (b) 0.10 × 5.67 × 10⁻⁸ × 2.5 × 360⁴ = 238 W; (c) it absorbs visible light well but emits little infrared, so less energy is lost; (d) net loss = eσA(360⁴ − 290⁴) = 138 W, leaving ≈ 1.70 kW.', 6)],
))


@prob('ch07-st1', d=(1, 5), md=(1, 4), marks=2)
def p_albedo(rng, slot):
    k = rng.randrange(5)
    city = rng.choice(CITIES)
    if k == 0:
        I = rng.choice([600, 800, 950, 1000]); a = rng.choice([0.05, 0.10, 0.25, 0.35, 0.80])
        surf = {0.05: 'dark ocean', 0.10: 'asphalt', 0.25: 'grassland', 0.35: 'desert sand', 0.80: 'fresh snow'}[a]
        return dict(stem=f'Sunlight of intensity {I} W m⁻² falls perpendicularly on {surf} with albedo {a}. Calculate the intensity absorbed.',
                    v=(1 - a) * I, unit='W m⁻²', wrongs=[a * I, I, I / (1 - a)], key=f'Absorbed = (1 − α)I (M1) = {sf((1 - a) * I)} W m⁻² (A1).')
    if k == 1:
        Pin = rng.choice([500, 800, 1200]); Pr = rng.choice([100, 150, 240, 400])
        return dict(stem=f'A satellite measures {Pin} W m⁻² of sunlight incident on a region near {city} and {Pr} W m⁻² scattered back to space. Calculate the albedo of the region.',
                    v=Pr / Pin, unit='', wrongs=[1 - Pr / Pin, Pin / Pr, (Pin - Pr) / Pin + 0.1], key=f'α = scattered/incident (M1) = {Pr}/{Pin} = {sf(Pr / Pin)} (A1).')
    if k == 2:
        e = rng.choice([0.60, 0.75, 0.85, 0.95]); T = rng.choice([280, 300, 320, 350]); A = rng.choice([1.0, 2.0, 5.0])
        return dict(stem=f'A surface of area {A} m², emissivity {e}, is at {T} K. Calculate the power it radiates.',
                    v=e * SIGMA * A * T ** 4, unit='W', wrongs=[SIGMA * A * T ** 4, (1 - e) * SIGMA * A * T ** 4, e * SIGMA * A * T], key=f'P = eσAT⁴ (M1) = {sf(e * SIGMA * A * T ** 4)} W (A1).')
    if k == 3:
        P = rng.choice([200, 300, 350, 400]); T = rng.choice([290, 300, 310])
        e = P / (SIGMA * T ** 4)
        if e >= 1:
            return None
        return dict(stem=f'A surface at {T} K radiates {P} W per square metre. Determine its emissivity.',
                    v=e, unit='', wrongs=[1 - e, P / (SIGMA * T), e * 2], key=f'e = P/(σT⁴) (M1) = {P}/(5.67 × 10⁻⁸ × {T}⁴) = {sf(e)} (A1).')
    a1 = rng.choice([0.85, 0.80]); a2 = rng.choice([0.06, 0.10]); I = rng.choice([300, 400, 500]); A = rng.choice([1.0e6, 5.0e6, 1.0e7])
    dP = (a1 - a2) * I * A
    return dict(stem=f'An area of {sf(A, 2)} m² of Arctic sea ice (albedo {a1}) melts to open ocean (albedo {a2}). The mean solar intensity is {I} W m⁻². Calculate the increase in power absorbed.',
                v=dP, unit='W', wrongs=[a1 * I * A, (1 - a2) * I * A, (a1 + a2) * I * A], key=f'ΔP = (α_ice − α_ocean)IA (M1) = {sf(dP)} W (A1).')


R.mcqs('ch07-st1', 'C2', (1, 4), [
    ('If Earth’s albedo increased, with nothing else changing, the equilibrium surface temperature would', 'decrease', ['increase', 'stay the same', 'become zero'], 'Less radiation absorbed.'),
    ('Two surfaces at the same temperature have emissivities 0.3 and 0.9. The ratio of powers per unit area emitted is', '1 : 3', ['3 : 1', '1 : 9', '9 : 1'], 'P ∝ e.'),
    ('Which statement about a perfect black body is correct?', 'It absorbs all incident radiation', ['It reflects all incident radiation', 'It always appears black', 'It emits no radiation'], 'The Sun is approximately a black body but appears bright.'),
])


R.facts('ch07-st2', F(
    terms=[('energy balance', 'the condition in which the power absorbed by the Earth–atmosphere system equals the power it radiates to space, giving a steady mean temperature'),
           ('mean incoming solar intensity', 'the solar constant divided by four (≈ 340 W m⁻²), because Earth intercepts sunlight over πR² but radiates over 4πR²'),
           ('equilibrium temperature', 'the temperature at which a planet radiates as much power as it absorbs'),
           ('radiative forcing', 'the change in net downward radiative flux at the top of the atmosphere caused by a change such as increased greenhouse gas concentration, in W m⁻²')],
    facts=[('Why is the mean solar intensity averaged over Earth’s surface equal to S/4?', 'Earth intercepts radiation over a disc πR² but has surface area 4πR²', ['A quarter is absorbed by the atmosphere', 'Earth is in sunlight a quarter of the time', 'The albedo is 0.25'], 'πR²/4πR² = 1/4.'),
           ('With albedo 0.30 and no atmosphere, Earth’s equilibrium temperature would be about', '255 K', ['288 K', '273 K', '300 K'], 'T = [(1 − α)S/(4σ)]^¼.'),
           ('Earth’s actual mean surface temperature is about', '288 K', ['255 K', '273 K', '310 K'], '≈ 15 °C.'),
           ('If the solar constant increased by 4 %, the equilibrium temperature would rise by about', '1 %', ['4 %', '16 %', '2 %'], 'T ∝ S^¼.'),
           ('The difference between 288 K and 255 K is due mainly to', 'the greenhouse effect', ['geothermal heating', 'the ozone layer', 'urban heat'], 'Atmospheric absorption and re-emission of IR.')],
    why=[('Explain how the surface of the Earth reaches a temperature higher than the equilibrium temperature calculated without an atmosphere.', 'Greenhouse gases absorb infrared emitted by the surface and re-emit it in all directions, including back down; the surface receives both solar and atmospheric radiation, so it must be warmer to radiate the extra power.'),
         ('Explain why a simple energy-balance model predicts the same temperature for Earth at all latitudes, and why that is unrealistic.', 'The model averages the intensity over the whole surface; in reality the equator receives more energy per unit area than the poles, and energy is moved by winds and ocean currents.'),
         ('Explain why the equilibrium temperature of a planet does not depend on its radius.', 'Both absorbed power (∝ πR²) and emitted power (∝ 4πR²) scale with R², so R cancels in the balance.')],
    contrast=[('the solar constant', 'the mean incident intensity at the top of the atmosphere', 'The solar constant (~1360 W m⁻²) is measured perpendicular to the rays; the mean over the whole surface and over day and night is a quarter of this (~340 W m⁻²).')],
    misc=[('Earth only radiates energy at night.', 'Earth radiates infrared continuously, day and night, at a rate depending on its temperature.'),
          ('In energy balance, Earth receives no energy.', 'It receives energy continuously; balance means the power absorbed equals the power radiated, so the mean temperature is steady.'),
          ('A planet closer to the Sun must have a higher surface temperature.', 'It receives more solar power, but its albedo and greenhouse effect matter: Venus is hotter than Mercury despite being further away.')],
    evaluate=[('A zero-dimensional energy-balance model is too simple to be useful in climate science.', ['ignores latitude, oceans, clouds and feedbacks', 'cannot predict regional changes'], ['captures the key physics of energy in = energy out', 'gives correct order of magnitude (255 K vs 288 K) and shows the role of albedo and greenhouse gases', 'used to check complex models'], 'Simple models are valuable for understanding and estimates, but detailed predictions require complex general circulation models (NOS: role of models).')],
    extended=[('Assume Earth has albedo 0.30 and the solar constant is 1360 W m⁻². (a) Calculate the mean intensity absorbed per square metre of Earth’s surface. (b) Calculate the equilibrium temperature with no atmosphere. (c) In a simple model the atmosphere is a single layer with emissivity 0.78 for infrared; the surface temperature is then T_s = T_e[2/(2 − e)]^¼. Calculate T_s. (d) Discuss two limitations of this model.', '(a) 0.70 × 340 = 238 W m⁻²; (b) T = (238/5.67 × 10⁻⁸)^¼ = 255 K; (c) 255 × (2/1.22)^¼ = 288 K; (d) ignores convection and latent heat transfer, clouds, variation with latitude, feedbacks, absorption of sunlight in the atmosphere.', 6)],
))


@prob('ch07-st2', d=(1, 5), md=(1, 4), marks=3)
def p_balance(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        a = rng.choice([0.25, 0.28, 0.30, 0.32, 0.35])
        T = ((1 - a) * S0 / (4 * SIGMA)) ** 0.25
        return dict(stem=f'Taking the solar constant as 1360 W m⁻² and Earth’s albedo as {a}, calculate the equilibrium temperature of Earth with no greenhouse effect.',
                    v=T, unit='K', wrongs=[((1 - a) * S0 / SIGMA) ** 0.25, (S0 / (4 * SIGMA)) ** 0.25, (a * S0 / (4 * SIGMA)) ** 0.25], key=f'σT⁴ = (1 − α)S/4 (M1 M1); T = {sf(T)} K (A1).')
    if k == 1:
        pl = pick(rng, [('Mars', 1.52, 0.25), ('Venus', 0.723, 0.76), ('Mercury', 0.387, 0.07), ('the Moon', 1.0, 0.11), ('Jupiter', 5.20, 0.34)])
        nm, d, a = pl; S = S0 / d ** 2
        T = ((1 - a) * S / (4 * SIGMA)) ** 0.25
        return dict(stem=f'{nm[0].upper() + nm[1:]} orbits at {d} AU from the Sun and has an albedo of {a}. The solar constant at 1 AU is 1360 W m⁻². Calculate the equilibrium temperature of {nm}, ignoring any greenhouse effect.',
                    v=T, unit='K', wrongs=[((1 - a) * S0 / d / (4 * SIGMA)) ** 0.25, ((1 - a) * S / SIGMA) ** 0.25, ((1 - a) * S0 / (4 * SIGMA)) ** 0.25], key=f'S = 1360/{d}² = {sf(S)} W m⁻² (M1); σT⁴ = (1 − α)S/4 (M1); T = {sf(T)} K (A1).')
    if k == 2:
        a = rng.choice([0.30]); T = rng.choice([288, 289, 290])
        Pemit = SIGMA * T ** 4; Pin = (1 - a) * S0 / 4
        return dict(stem=f'Earth’s surface at {T} K radiates approximately as a black body. Calculate the intensity it emits and compare it with the mean absorbed solar intensity of {sf(Pin)} W m⁻².',
                    v=Pemit, unit='W m⁻²', ans=f'{q(Pemit, "W m⁻²")} (about {sf(Pemit / Pin, 2)} times the absorbed solar intensity)', wrongs=[Pin, SIGMA * T ** 4 / 4, SIGMA * (T - 273) ** 4], key=f'I = σT⁴ = {sf(Pemit)} W m⁻² (A1); larger because the surface also receives infrared from the atmosphere (R1).', marks=2)
    if k == 3:
        f = rng.choice([1.01, 1.02, 1.04, 0.98, 0.97])
        T0 = 288
        return dict(stem=f'In a simple model, Earth’s surface temperature is proportional to the fourth root of the absorbed solar power. If the absorbed power changes by a factor of {f}, calculate the new surface temperature, starting from 288 K.',
                    v=T0 * f ** 0.25, unit='K', n=4, wrongs=[T0 * f, T0 * f ** 0.5, T0 * f ** 4], key=f'T ∝ P^¼ (M1); T = 288 × {f}^¼ = {sf(T0 * f ** 0.25, 4)} K (A1).', marks=2)
    e = rng.choice([0.70, 0.75, 0.78, 0.80, 0.85])
    Te = 255.0
    Ts = Te * (2 / (2 - e)) ** 0.25
    return dict(stem=f'In a one-layer atmosphere model, the surface temperature is T_s = T_e[2/(2 − ε)]^¼, where T_e = 255 K and ε is the infrared emissivity of the atmosphere. Calculate T_s for ε = {e}.',
                v=Ts, unit='K', wrongs=[Te * (2 / (2 - e)), Te * (1 + e) ** 0.25, Te * 2 ** 0.25], key=f'T_s = 255 × (2/{sf(2 - e)})^¼ (M1) = {sf(Ts)} K (A1).', marks=2)


R.mcqs('ch07-st2', 'C2', (1, 4), [
    ('Planet X has twice the radius of planet Y, at the same distance from the star and with the same albedo. The equilibrium temperature of X is', 'the same as that of Y', ['twice that of Y', '√2 times that of Y', 'half that of Y'], 'R cancels.'),
    ('In the energy balance, if absorbed solar power exceeds the infrared power emitted, Earth will', 'warm until the emitted power increases to match', ['cool down', 'remain at the same temperature', 'reflect more light'], 'σT⁴ rises with T.'),
    ('Which change would increase Earth’s equilibrium temperature?', 'A decrease in albedo', ['An increase in albedo', 'A decrease in the solar constant', 'An increase in Earth’s radius'], 'More absorbed power.'),
])


def _orbit_temp_spec(rng):
    a = rng.uniform(0.20, 0.40)
    ds = [0.40, 0.70, 1.00, 1.50, 2.00, 3.00]
    Ts = [round(((1 - a) * S0 / d ** 2 / (4 * SIGMA)) ** 0.25 * rng.uniform(0.99, 1.01)) for d in ds]
    return dict(intro='A computer model calculates the equilibrium temperature T of a rocky planet with no atmosphere placed at different distances d from the Sun (solar constant 1360 W m⁻² at 1 AU). Theory: σT⁴ = (1 − α)S/(4d²), so T⁴ ∝ 1/d².',
                xname='d', xunit='AU', yname='T', yunit='K', xs=ds, ys=Ts, xfmt=lambda x: f'{x:.2f}', yfmt=lambda y: f'{y:.0f}',
                plot_x=lambda x: 1 / x ** 2, plot_y=lambda y: y ** 4, plot_label='T⁴ (y) against 1/d² (x)', what='the albedo α of the planet', what_short='α',
                gunit='K⁴ AU²', deduce=lambda m_, b_: (1 - 4 * SIGMA * m_ / S0, '', 'α = 1 − 4σ × gradient/S'))


gradient_fit('ch07-st2', _orbit_temp_spec)


R.facts('ch07-st3', F(
    terms=[('greenhouse gas', 'a gas in the atmosphere that absorbs and re-emits infrared radiation, such as H₂O, CO₂, CH₄ and N₂O'),
           ('greenhouse effect', 'the warming of a planet’s surface because atmospheric gases absorb outgoing infrared radiation and re-emit part of it back towards the surface'),
           ('molecular resonance (infrared absorption)', 'the absorption of infrared photons whose frequency matches a natural vibrational frequency of the bonds in a molecule'),
           ('atmospheric window', 'the range of infrared wavelengths (about 8–14 μm) that passes through the atmosphere with little absorption'),
           ('dipole moment', 'a separation of charge within a molecule; vibrations that change the dipole moment can absorb infrared radiation')],
    facts=[('Why do N₂ and O₂ not act as greenhouse gases?', 'Their symmetric vibrations do not change the molecular dipole moment, so they hardly absorb infrared', ['They are too dense', 'They absorb only visible light', 'They are too rare'], 'Homonuclear diatomic molecules.'),
           ('Which gas makes the largest contribution to the natural greenhouse effect?', 'Water vapour', ['Carbon dioxide', 'Methane', 'Oxygen'], 'H₂O dominates the natural effect.'),
           ('Earth’s surface emits radiation mainly in the', 'infrared', ['ultraviolet', 'visible', 'microwave'], 'λ_max ≈ 10 μm at 288 K.'),
           ('Greenhouse gases are mostly transparent to', 'incoming visible sunlight', ['outgoing infrared', 'all radiation', 'nothing'], 'They absorb mainly IR.'),
           ('Carbon dioxide strongly absorbs infrared at a wavelength of about', '15 μm', ['500 nm', '1 mm', '0.3 μm'], 'Bending vibration mode.')],
    why=[('Explain, at the molecular level, how carbon dioxide absorbs infrared radiation.', 'The bending and asymmetric stretching vibrations of CO₂ change its dipole moment; when the frequency of infrared radiation matches a natural vibration frequency (resonance), the photon is absorbed and the molecule vibrates more strongly, later re-emitting IR in a random direction.'),
         ('Explain why greenhouse gases warm the surface even though they re-emit the radiation they absorb.', 'Re-emission is in all directions, so about half returns towards the surface; the surface receives extra infrared and must warm to restore energy balance.'),
         ('Explain why water vapour is considered a feedback rather than a driver of climate change.', 'Its concentration is controlled by temperature (evaporation and condensation within days); warming caused by CO₂ increases water vapour, which amplifies the warming.')],
    contrast=[('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural greenhouse effect, from pre-industrial levels of water vapour and CO₂, keeps Earth about 33 K warmer than it would be otherwise; the enhanced effect is the additional warming caused by human emissions raising greenhouse gas concentrations.')],
    misc=[('The greenhouse effect is caused by the ozone hole letting in more sunlight.', 'Ozone depletion increases UV at the surface, but the greenhouse effect is the absorption and re-emission of outgoing infrared by greenhouse gases.'),
          ('Greenhouse gases trap heat like the glass of a greenhouse prevents convection.', 'Real greenhouses work mainly by stopping convection; the atmospheric effect works by absorption and re-emission of infrared radiation.'),
          ('All gases in the atmosphere are greenhouse gases.', 'N₂, O₂ and Ar, which make up 99 % of dry air, absorb almost no infrared; only molecules whose vibrations change their dipole moment are greenhouse gases.')],
    evaluate=[('The greenhouse effect is harmful to life on Earth.', ['the enhanced greenhouse effect is causing rapid climate change'], ['without the natural greenhouse effect Earth’s mean temperature would be about −18 °C', 'liquid oceans and life depend on it'], 'The natural greenhouse effect is essential for life; it is the rapid human-driven enhancement that is harmful.')],
    extended=[('A CO₂ molecule absorbs infrared radiation of wavelength 15 μm. (a) Calculate the frequency and photon energy of this radiation. (b) Calculate the peak wavelength of Earth’s surface emission at 288 K and comment on the result. (c) Explain why the absorption occurs at specific wavelengths. (d) Explain why adding more CO₂ still increases the greenhouse effect even though the 15 μm band is already strongly absorbed.', '(a) f = 2.0 × 10¹³ Hz, E = 1.33 × 10⁻²⁰ J; (b) 10.1 μm – close to 15 μm, so CO₂ absorbs a significant part of Earth’s emission; (c) photon energy must match a vibrational energy level transition (resonance); (d) the band edges/wings broaden and emission to space happens from higher, colder layers, reducing outgoing radiation.', 6)],
))


@prob('ch07-st3', d=(1, 4), md=(1, 4), marks=2)
def p_ir(rng, slot):
    k = rng.randrange(3)
    if k == 0:
        gas, lam = pick(rng, [('carbon dioxide', 15.0), ('carbon dioxide', 4.3), ('methane', 7.7), ('water vapour', 6.3), ('nitrous oxide', 7.8), ('ozone', 9.6)])
        return dict(stem=f'{gas[0].upper() + gas[1:]} absorbs infrared strongly at a wavelength of {lam} μm. Calculate the frequency of this radiation.',
                    v=C / (lam * 1e-6), unit='Hz', wrongs=[C * lam * 1e-6, C / lam, lam * 1e-6 / C], key=f'f = c/λ (M1) = 3.00 × 10⁸/{lam} × 10⁻⁶ = {sf(C / (lam * 1e-6))} Hz (A1).')
    if k == 1:
        gas, lam = pick(rng, [('carbon dioxide', 15.0), ('methane', 7.7), ('water vapour', 6.3), ('ozone', 9.6)])
        Eph = H * C / (lam * 1e-6)
        return dict(stem=f'Calculate the energy of an infrared photon of wavelength {lam} μm absorbed by {gas}.',
                    v=Eph, unit='J', wrongs=[H * lam * 1e-6 / C, H * C / lam, H / (lam * 1e-6)], key=f'E = hc/λ (M1) = {sf(Eph)} J (A1).')
    T = rng.choice([220, 255, 288, 300, 320])
    return dict(stem=f'Calculate the peak wavelength of infrared emitted by a part of the Earth system at {T} K.',
                v=WIEN / T, unit='m', wrongs=[WIEN * T, WIEN / (T + 273), WIEN / T * 1000], key=f'λ = 2.9 × 10⁻³/T (M1) = {sf(WIEN / T)} m (A1).')


R.mcqs('ch07-st3', 'C2', (1, 4), [
    ('Which property of a molecule determines whether it is a greenhouse gas?', 'Whether its vibrations change its electric dipole moment', ['Its molar mass', 'Its colour', 'Its boiling point'], 'IR-active modes.'),
    ('Incoming solar radiation passes through the atmosphere largely unabsorbed, but outgoing terrestrial radiation is absorbed, because', 'the outgoing radiation is at much longer (infrared) wavelengths', ['the outgoing radiation is more intense', 'the Sun is further away', 'outgoing radiation travels more slowly'], 'Different wavelength ranges.'),
    ('After absorbing an infrared photon, a greenhouse gas molecule typically', 'transfers energy to other molecules by collisions or re-emits infrared in a random direction', ['emits visible light', 'splits apart', 'reflects the photon back to space'], 'Thermalisation and re-emission.'),
])


R.facts('ch07-st4', F(
    terms=[('enhanced greenhouse effect', 'the additional warming caused by increased concentrations of greenhouse gases from human activity'),
           ('positive feedback', 'a process in which a change causes effects that amplify the original change, such as ice–albedo feedback'),
           ('negative feedback', 'a process that reduces the original change, such as increased infrared emission from a warmer surface'),
           ('climate sensitivity', 'the equilibrium change in global mean surface temperature for a doubling of atmospheric CO₂ concentration'),
           ('tipping point', 'a threshold beyond which a change in the climate system becomes self-sustaining or irreversible')],
    facts=[('Atmospheric CO₂ concentration has risen from about 280 ppm before the industrial era to', 'over 420 ppm today', ['about 300 ppm', 'over 1000 ppm', 'about 180 ppm'], 'Mauna Loa measurements since 1958.'),
           ('Which is a positive feedback in the climate system?', 'Melting ice reducing albedo', ['Increased infrared emission from a warmer surface', 'Increased plant growth absorbing CO₂', 'Increased cloud reflecting sunlight'], 'It amplifies warming.'),
           ('The main human source of CO₂ emissions is', 'the burning of fossil fuels', ['volcanic eruptions', 'respiration by animals', 'nuclear power'], 'About 35 Gt per year.'),
           ('Sea level rises with global warming mainly because of', 'thermal expansion of seawater and melting land ice', ['melting floating sea ice', 'increased rainfall', 'evaporation'], 'Floating ice melting hardly changes sea level.'),
           ('Methane is a more potent greenhouse gas than CO₂ per molecule but', 'it has a much shorter atmospheric lifetime (about 12 years)', ['it absorbs no infrared', 'it is far more abundant', 'it is not produced by humans'], 'Global warming potential depends on lifetime.')],
    why=[('Explain why melting permafrost could accelerate climate change.', 'Permafrost stores large amounts of organic carbon; as it thaws, microbes decompose it, releasing CO₂ and methane that enhance the greenhouse effect and cause further warming (positive feedback).'),
         ('Explain why the evidence that recent warming is caused by humans is considered strong.', 'Multiple independent lines of evidence agree: measured CO₂ rise matches fossil fuel use (isotope ratios), the physics of IR absorption, stratospheric cooling with tropospheric warming, and models only reproduce observed warming when human emissions are included.'),
         ('Explain why reducing emissions today will not stop warming immediately.', 'CO₂ stays in the atmosphere for centuries and the oceans have a large heat capacity, so the climate responds slowly; temperatures continue to rise until a new energy balance is reached.')],
    contrast=[('mitigation', 'adaptation', 'Mitigation reduces the causes of climate change (cutting emissions, carbon capture, renewables); adaptation reduces the harm of changes that occur (flood defences, drought-resistant crops).')],
    misc=[('Melting sea ice is the main cause of sea-level rise.', 'Floating sea ice already displaces its own weight of water; sea-level rise comes mainly from thermal expansion and melting of land ice (glaciers, Greenland, Antarctica).'),
          ('A cold winter disproves global warming.', 'Weather varies locally from year to year; climate change refers to long-term global averages, which show a clear warming trend.'),
          ('Since water vapour is the main greenhouse gas, CO₂ does not matter.', 'Water vapour responds to temperature as a feedback; CO₂ is a long-lived forcing that sets the temperature and hence the amount of water vapour.')],
    evaluate=[('Carbon capture and storage can solve the problem of climate change without reducing fossil fuel use.', ['can remove CO₂ from power stations and heavy industry', 'can use existing infrastructure'], ['expensive and energy-intensive (reduces power station efficiency)', 'limited capacity deployed so far', 'risk of leakage; does not address transport emissions'], 'CCS can contribute, particularly for hard-to-decarbonise industries, but cannot replace large reductions in fossil fuel use.'),
              ('Individual action is pointless compared with government policy on climate change.', ['policy can change energy systems at scale', 'individuals’ emissions are a tiny fraction of the total'], ['collective individual choices shape markets and political demand', 'lifestyle changes (diet, travel, energy use) add up across billions of people'], 'Both are needed: policy sets the framework, but individual and community action drives demand and political will.')],
    extended=[('In a simple model, the radiative forcing from CO₂ is ΔF = 5.35 ln(C/C₀) W m⁻² and the equilibrium warming is ΔT = λΔF with λ = 0.80 K W⁻¹ m². (a) Calculate ΔF and ΔT for a rise from 280 ppm to 420 ppm. (b) Calculate the forcing for a doubling of CO₂ and hence the climate sensitivity. (c) Explain why the observed warming to date (≈ 1.2 K) is less than the answer to (a). (d) Discuss one source of uncertainty in λ.', '(a) ΔF = 5.35 ln 1.5 = 2.17 W m⁻², ΔT = 1.7 K; (b) 5.35 ln 2 = 3.71 W m⁻², sensitivity ≈ 3.0 K; (c) oceans are still absorbing energy (thermal inertia) and aerosols have a cooling effect; (d) cloud feedbacks are poorly constrained.', 6)],
))


@prob('ch07-st4', d=(2, 5), md=(2, 4), marks=3)
def p_forcing(rng, slot):
    k = rng.randrange(3)
    if k == 0:
        C1 = rng.choice([350, 400, 420, 450, 560, 700])
        dF = 5.35 * math.log(C1 / 280)
        return dict(stem=f'The radiative forcing due to CO₂ is ΔF = 5.35 ln(C/C₀) W m⁻², with C₀ = 280 ppm. Calculate the forcing when the concentration reaches {C1} ppm.',
                    v=dF, unit='W m⁻²', wrongs=[5.35 * C1 / 280, 5.35 * math.log10(C1 / 280), 5.35 * (C1 - 280) / 280], key=f'ΔF = 5.35 ln({C1}/280) (M1) = {sf(dF)} W m⁻² (A1).', marks=2)
    if k == 1:
        lam = rng.choice([0.5, 0.6, 0.8, 1.0, 1.2]); dF = rng.choice([1.5, 2.0, 2.7, 3.7, 4.5])
        return dict(stem=f'A climate model uses a sensitivity parameter of {lam} K per W m⁻². Calculate the equilibrium warming produced by a radiative forcing of {dF} W m⁻².',
                    v=lam * dF, unit='K', wrongs=[dF / lam, lam + dF, lam * dF * 4], key=f'ΔT = λΔF (M1) = {sf(lam * dF)} K (A1).', marks=2)
    V = rng.choice([1.0e15, 2.0e15, 3.0e15]) ; area = 3.6e14
    rise = V / area
    return dict(stem=f'If {sf(V, 2)} m³ of land ice melted into the oceans (total ocean area 3.6 × 10¹⁴ m²), estimate the rise in sea level, treating the meltwater volume as about 0.92 times the ice volume.',
                v=0.92 * V / area, unit='m', wrongs=[rise, V / area / 0.92, 0.92 * V / area * 1000], key=f'Water volume = 0.92 × {sf(V, 2)} m³ (M1); rise = volume/area = {sf(0.92 * V / area)} m (A1).')


R.mcqs('ch07-st4', 'C2', (1, 4), [
    ('Which is a negative feedback in the climate system?', 'A warmer Earth radiating more infrared to space', ['Ice–albedo feedback', 'Permafrost methane release', 'Increased water vapour'], 'σT⁴ rises with T.'),
    ('Why does floating sea ice melting not significantly raise sea level?', 'Floating ice already displaces a mass of water equal to its own mass', ['Sea ice is too thin', 'The meltwater evaporates', 'Sea ice is fresh water'], 'Archimedes’ principle.'),
    ('The Keeling curve shows seasonal oscillations in CO₂ concentration because', 'plants in the Northern Hemisphere absorb CO₂ in summer and release it in winter', ['volcanoes erupt seasonally', 'the oceans freeze', 'fossil fuel use stops in summer'], 'Photosynthesis cycle.'),
])


# =============================================================================================
# ch08 B.3 Gas laws
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('pressure', 'the normal force per unit area, p = F/A, measured in pascals (N m⁻²)'),
           ('mole', 'the amount of substance containing as many particles as there are atoms in 12 g of carbon-12, i.e. 6.02 × 10²³ particles'),
           ('Avogadro constant', 'the number of particles per mole, N_A = 6.02 × 10²³ mol⁻¹'),
           ('molar mass', 'the mass of one mole of a substance, in g mol⁻¹ (numerically equal to the relative molecular mass)'),
           ('amount of substance', 'the number of moles n = N/N_A of particles in a sample')],
    facts=[('How many molecules are in 2.0 mol of oxygen?', '1.2 × 10²⁴', ['6.0 × 10²³', '3.0 × 10²³', '2.0 × 10²³'], 'N = nN_A.'),
           ('The molar mass of CO₂ is 44 g mol⁻¹. The mass of 0.50 mol is', '22 g', ['88 g', '44 g', '11 g'], 'm = nM.'),
           ('Standard atmospheric pressure is about', '1.0 × 10⁵ Pa', ['1.0 × 10³ Pa', '1.0 × 10⁷ Pa', '760 Pa'], '101 kPa.'),
           ('Which is equivalent to 1 Pa?', '1 N m⁻²', ['1 N m', '1 J m⁻²', '1 kg m s⁻²'], 'Definition.'),
           ('Gas pressure on the walls of a container is caused by', 'molecules colliding with and rebounding from the walls', ['molecules attracting the walls', 'the weight of the gas', 'molecules sticking to the walls'], 'Change of momentum at the walls.')],
    why=[('Explain, in terms of molecules, how a gas exerts pressure on the walls of its container.', 'Molecules collide with the walls and rebound, each undergoing a change of momentum; by Newton’s second and third laws the walls experience a force, and the total force per unit area is the pressure.'),
         ('Explain why a sharp knife cuts more easily than a blunt one.', 'The sharp edge has a much smaller contact area, so the same force gives a far greater pressure p = F/A.'),
         ('Explain why snowshoes stop a walker sinking into soft snow.', 'They spread the walker’s weight over a larger area, reducing the pressure on the snow below the value that compresses it.')],
    contrast=[('molar mass', 'the mass of one molecule', 'Molar mass is the mass of N_A particles (g mol⁻¹); the mass of one molecule is the molar mass divided by the Avogadro constant, typically about 10⁻²⁶ kg.')],
    misc=[('One mole of hydrogen has the same mass as one mole of oxygen.', 'One mole contains the same number of particles, but masses differ: 2.0 g for H₂ and 32 g for O₂.'),
          ('Gas pressure is caused by molecules pushing each other apart.', 'In the ideal gas model molecules do not interact except in collisions; pressure arises from their collisions with the container walls.'),
          ('Pressure is a force.', 'Pressure is force per unit area, a scalar measured in Pa; the same force can produce very different pressures.')],
    evaluate=[('The mole is an unnecessary unit because we could simply count particles.', ['N is the fundamental quantity'], ['the numbers involved (~10²³) are unwieldy', 'chemists measure masses, and molar mass converts directly', 'the mole links the atomic and macroscopic scales'], 'The mole is a practical bridge between microscopic counts and measurable masses, so it remains essential.')],
    extended=[('A scuba tank of internal volume 12 L contains air at 2.0 × 10⁷ Pa and 288 K. Air has a mean molar mass of 29 g mol⁻¹. (a) Calculate the number of moles of air. (b) Calculate the mass of air. (c) Estimate the number of molecules. (d) Calculate the force on the 3.0 cm diameter valve face due to this pressure (ignore atmospheric pressure).', '(a) n = pV/RT = 2.0 × 10⁷ × 0.012/(8.31 × 288) = 100 mol; (b) 2.9 kg; (c) 6.0 × 10²⁵; (d) F = pA = 2.0 × 10⁷ × π × 0.015² = 1.4 × 10⁴ N.', 6)],
))


@prob('ch08-st1', d=(1, 4), md=(1, 4), marks=2)
def p_moles(rng, slot):
    k = rng.randrange(5)
    gases = [('helium', 4.0), ('nitrogen', 28), ('oxygen', 32), ('carbon dioxide', 44), ('argon', 40), ('methane', 16)]
    nm, M = pick(rng, gases)
    city = rng.choice(CITIES)
    if k == 0:
        m = rng.choice([4.0, 8.0, 12, 20, 50, 100])
        return dict(stem=f'Calculate the number of moles in {m} g of {nm} (molar mass {M} g mol⁻¹).', v=m / M, unit='mol', wrongs=[M / m, m * M, m / M * NA / 1e23], key=f'n = m/M (M1) = {sf(m / M)} mol (A1).')
    if k == 1:
        m = rng.choice([1.0, 5.0, 10, 50])
        N = m / M * NA
        return dict(stem=f'How many molecules are there in {m} g of {nm}? (M = {M} g mol⁻¹)', v=N, unit='', wrongs=[m * M * NA, m / M, NA / (m * M)], key=f'n = {sf(m / M)} mol (M1); N = nN_A = {sf(N)} (A1).')
    if k == 2:
        return dict(stem=f'Calculate the mass of a single molecule of {nm} (molar mass {M} g mol⁻¹).', v=M * 1e-3 / NA, unit='kg', wrongs=[M / NA, M * NA * 1e-3, NA / M], key=f'm = M/N_A = {M} × 10⁻³/6.02 × 10²³ (M1) = {sf(M * 1e-3 / NA)} kg (A1).')
    if k == 3:
        F_ = rng.choice([500, 600, 700, 800]); A = rng.choice([0.020, 0.030, 0.040, 2.0e-4])
        what = 'stiletto heel' if A < 1e-3 else 'shoe sole'
        return dict(stem=f'A person of weight {F_} N stands on one {what} of contact area {A} m². Calculate the pressure on the floor.',
                    v=F_ / A, unit='Pa', wrongs=[F_ * A, A / F_, F_ / A / 1000], key=f'p = F/A (M1) = {sf(F_ / A)} Pa (A1).')
    p = rng.choice([1.01e5, 2.0e5, 3.5e5]); r = rng.choice([0.05, 0.10, 0.15])
    return dict(stem=f'A circular hatch of radius {r} m on a pressurised tank in {city} has a gauge pressure of {sf(p)} Pa acting on it. Calculate the force on the hatch.',
                v=p * math.pi * r * r, unit='N', wrongs=[p * 2 * math.pi * r, p / (math.pi * r * r), p * r * r], key=f'F = pA = {sf(p)} × π × {r}² (M1) = {sf(p * math.pi * r * r)} N (A1).')


R.mcqs('ch08-st1', 'C2', (1, 4), [
    ('Equal masses of helium (4 g mol⁻¹) and oxygen (32 g mol⁻¹) contain numbers of molecules in the ratio He : O₂ of', '8 : 1', ['1 : 8', '1 : 1', '4 : 32'], 'n = m/M.'),
    ('The force on a surface stays constant while its area halves. The pressure', 'doubles', ['halves', 'stays the same', 'quadruples'], 'p = F/A.'),
    ('One mole of any substance contains', '6.02 × 10²³ particles', ['22.4 particles', '1 g of material', '12 g of material'], 'Avogadro constant.'),
])


R.facts('ch08-st2', F(
    terms=[('ideal gas', 'a theoretical gas that obeys pV = nRT exactly at all pressures and temperatures'),
           ('Boyle’s law', 'for a fixed mass of gas at constant temperature, pV = constant'),
           ('Charles’s law', 'for a fixed mass of gas at constant pressure, V ∝ T (absolute temperature)'),
           ('pressure law (Gay-Lussac)', 'for a fixed mass of gas at constant volume, p ∝ T (absolute temperature)'),
           ('equation of state for an ideal gas', 'the relation pV = nRT (or pV = Nk_BT) between pressure, volume, amount and absolute temperature'),
           ('molar gas constant', 'the constant R = 8.31 J K⁻¹ mol⁻¹ in the ideal gas equation, equal to N_A k_B')],
    facts=[('A gas at constant temperature is compressed from 3.0 L to 1.0 L. Its pressure', 'triples', ['is divided by 3', 'is unchanged', 'increases by a factor of 9'], 'Boyle’s law.'),
           ('A sealed rigid container of gas is heated from 300 K to 600 K. The pressure', 'doubles', ['halves', 'is unchanged', 'quadruples'], 'p ∝ T.'),
           ('In pV = nRT, the temperature must be in', 'kelvin', ['degrees Celsius', 'degrees Fahrenheit', 'any unit'], 'Absolute scale.'),
           ('A graph of V against T (in °C) for a gas at constant pressure extrapolates to V = 0 at', '−273 °C', ['0 °C', '−100 °C', '273 °C'], 'Absolute zero.'),
           ('The volume occupied by 1 mol of ideal gas at 273 K and 1.00 × 10⁵ Pa is', '22.7 L', ['1.00 L', '8.31 L', '273 L'], 'V = RT/p.')],
    why=[('Explain why the tyre pressure of a car increases after a long journey.', 'Friction and flexing heat the air in the tyre; at nearly constant volume p ∝ T, so the pressure increases.'),
         ('Explain why a balloon shrinks when it is placed in a freezer.', 'At roughly constant pressure, V ∝ T; cooling reduces the temperature and so the volume of the gas inside.'),
         ('Explain why the gas laws require temperature in kelvin.', 'The proportionalities p ∝ T and V ∝ T hold only for absolute temperature, which is zero when the molecular kinetic energy is minimal; with Celsius, zero is arbitrary.')],
    contrast=[('Boyle’s law', 'Charles’s law', 'Boyle’s law relates pressure and volume at constant temperature (pV = constant); Charles’s law relates volume and temperature at constant pressure (V/T = constant).')],
    misc=[('Doubling the temperature of a gas from 20 °C to 40 °C doubles its pressure at constant volume.', 'p ∝ absolute temperature: 293 K → 313 K increases p by only about 7 %.'),
          ('Boyle’s law applies even if gas leaks out of the container.', 'The gas laws apply to a fixed amount of gas; if n changes, pV/T changes in proportion.'),
          ('All gases behave ideally under all conditions.', 'Real gases deviate at high pressure and low temperature, where molecular volume and intermolecular forces matter.')],
    evaluate=[('The ideal gas equation is good enough for all engineering calculations involving gases.', ['accurate to within ~1 % for air at everyday conditions', 'simple to use'], ['fails for high-pressure storage (CNG, hydrogen tanks) and near condensation', 'refrigeration and steam engineering need real-gas tables'], 'It is adequate for many everyday calculations, but high-pressure or low-temperature applications require real-gas models.')],
    extended=[('A weather balloon is filled with 4.0 m³ of helium at ground level, where the pressure is 1.0 × 10⁵ Pa and the temperature is 290 K. It rises to an altitude where the pressure is 2.5 × 10⁴ Pa and the temperature is 220 K. (a) Calculate the number of moles of helium. (b) Determine the volume of the balloon at altitude. (c) Explain why the balloon eventually bursts. (d) Calculate the mass of helium (4.0 g mol⁻¹).', '(a) n = pV/RT = 166 mol; (b) V₂ = V₁(p₁/p₂)(T₂/T₁) = 4.0 × 4 × 220/290 = 12.1 m³; (c) the external pressure keeps falling, so the volume grows until the rubber’s elastic limit is exceeded; (d) 0.66 kg.', 6)],
))


@prob('ch08-st2', d=(1, 5), md=(1, 4), marks=2)
def p_gaslaw(rng, slot):
    k = rng.randrange(6)
    who, city = who_city(rng)
    if k == 0:
        p1 = rng.choice([1.0e5, 1.2e5, 1.5e5, 2.0e5]); V1 = rng.choice([2.0, 3.0, 4.0, 6.0]); V2 = rng.choice([0.5, 1.0, 1.5, 2.5])
        if V2 >= V1:
            return None
        return dict(stem=f'A fixed mass of air in a bicycle pump at {sf(p1)} Pa occupies {V1} × 10⁻⁴ m³. It is compressed slowly at constant temperature to {V2} × 10⁻⁴ m³. Calculate the new pressure.',
                    v=p1 * V1 / V2, unit='Pa', wrongs=[p1 * V2 / V1, p1 * (V1 - V2), p1 * (V1 / V2) ** 2], key=f'p₁V₁ = p₂V₂ (M1); p₂ = {sf(p1 * V1 / V2)} Pa (A1).')
    if k == 1:
        p1 = rng.choice([2.0e5, 2.2e5, 2.4e5]); T1 = rng.choice([280, 288, 293]); T2 = rng.choice([310, 320, 330])
        return dict(stem=f'{who}’s car tyre has a pressure of {sf(p1)} Pa at {T1} K in {city}. After a drive the air inside is at {T2} K. Assuming the volume is constant, calculate the new pressure.',
                    v=p1 * T2 / T1, unit='Pa', wrongs=[p1 * T1 / T2, p1 * (T2 - 273) / (T1 - 273), p1 + (T2 - T1)], key=f'p/T constant (M1); p₂ = {sf(p1)} × {T2}/{T1} = {sf(p1 * T2 / T1)} Pa (A1).')
    if k == 2:
        n = rng.choice([0.5, 1.0, 2.0, 5.0]); T = rng.choice([273, 293, 300, 350]); V = rng.choice([0.010, 0.020, 0.050, 0.10])
        return dict(stem=f'{n} mol of an ideal gas is held at {T} K in a container of volume {V} m³. Calculate its pressure.',
                    v=n * RGAS * T / V, unit='Pa', wrongs=[n * RGAS * (T - 273) / V if T != 273 else n * RGAS / V, n * RGAS * T * V, n * T / V], key=f'p = nRT/V (M1) = {n} × 8.31 × {T}/{V} = {sf(n * RGAS * T / V)} Pa (A1).')
    if k == 3:
        p = rng.choice([1.0e5, 1.5e5, 3.0e5]); V = rng.choice([0.0050, 0.010, 0.024]); T = rng.choice([290, 300, 310])
        N = p * V / (KB * T)
        return dict(stem=f'A sealed flask of volume {V} m³ contains gas at {sf(p)} Pa and {T} K. Calculate the number of molecules in the flask.',
                    v=N, unit='', wrongs=[p * V / (RGAS * T), p * V * KB * T, p * V / (KB * (T - 273))], key=f'N = pV/(k_B T) (M1) = {sf(N)} (A1).')
    if k == 4:
        V1 = rng.choice([2.0, 2.5, 3.0]); T1 = rng.choice([290, 300]); T2 = rng.choice([250, 260, 350, 370])
        return dict(stem=f'A balloon holds {V1} L of air at {T1} K. At constant pressure, the air is cooled or heated to {T2} K. Calculate the new volume.',
                    v=V1 * T2 / T1, unit='L', wrongs=[V1 * T1 / T2, V1 * (T2 - 273) / (T1 - 273), V1 + (T2 - T1) / 100], key=f'V/T constant (M1); V₂ = {V1} × {T2}/{T1} = {sf(V1 * T2 / T1)} L (A1).')
    p1, V1, T1 = 1.0e5, rng.choice([2.0, 3.0, 4.0]), rng.choice([290, 300])
    p2, T2 = rng.choice([3.0e4, 5.0e4, 2.5e4]), rng.choice([220, 240, 250])
    V2 = V1 * p1 / p2 * T2 / T1
    return dict(stem=f'A sealed weather balloon contains {V1} m³ of helium at {sf(p1)} Pa and {T1} K. At altitude the pressure is {sf(p2)} Pa and the temperature {T2} K. Calculate the new volume.',
                v=V2, unit='m³', wrongs=[V1 * p1 / p2, V1 * p2 / p1 * T2 / T1, V1 * p1 / p2 * T1 / T2], key=f'p₁V₁/T₁ = p₂V₂/T₂ (M1); V₂ = {sf(V2)} m³ (A1).', marks=3)


R.mcqs('ch08-st2', 'C2', (1, 4), [
    ('For a fixed mass of ideal gas, which graph is a straight line through the origin?', 'p against T (in K) at constant volume', ['p against V at constant T', 'V against T in °C at constant p', 'p against 1/T at constant V'], 'p ∝ T.'),
    ('The pressure and absolute temperature of a fixed mass of gas both double. Its volume', 'is unchanged', ['doubles', 'quadruples', 'halves'], 'V ∝ T/p.'),
    ('A graph of pV against p for an ideal gas at constant temperature is', 'a horizontal line', ['a straight line through the origin', 'a hyperbola', 'a parabola'], 'pV constant.'),
    ('Two identical flasks contain the same gas at the same temperature; flask X is at twice the pressure of flask Y. X contains', 'twice as many molecules as Y', ['half as many', 'the same number', 'four times as many'], 'N ∝ pV/T.'),
])


def _charles_spec(rng):
    V0 = rng.uniform(1.8e-5, 2.2e-5) ; T0 = 273
    Tc = [0, 20, 40, 60, 80, 100]
    Vs = [round(V0 * (t + 273) / T0 * 1e6 * rng.uniform(0.995, 1.005), 2) for t in Tc]
    return dict(intro='A capillary tube contains a trapped column of air sealed by a bead of acid. The tube is heated in a water bath and the length (proportional to volume) of the air column is measured at different Celsius temperatures θ, with the volume V calculated from the length. Theory: V ∝ (θ + 273).',
                xname='θ', xunit='°C', yname='V', yunit='cm³', xs=Tc, ys=Vs, xfmt=lambda x: f'{x}', yfmt=lambda y: f'{y:.2f}',
                plot_x=lambda x: x, plot_y=lambda y: y, plot_label='V (y) against θ (x)', what='absolute zero in degrees Celsius, from the intercept of the line on the θ-axis', what_short='absolute zero',
                gunit='cm³ °C⁻¹', deduce=lambda m_, b_: (-b_ / m_, '°C', 'θ-intercept = −(V-intercept)/gradient'))


gradient_fit('ch08-st2', _charles_spec)


R.facts('ch08-st3', F(
    terms=[('kinetic model of an ideal gas', 'a model in which a gas consists of a large number of identical point molecules in random motion, colliding elastically, with no intermolecular forces except during collisions'),
           ('root mean square speed', 'the square root of the mean of the squares of the molecular speeds, c_rms = √(3k_BT/m)'),
           ('mean translational kinetic energy', 'the average kinetic energy of a molecule, Ē_k = (3/2)k_BT'),
           ('Boltzmann constant', 'the gas constant per molecule, k_B = R/N_A = 1.38 × 10⁻²³ J K⁻¹'),
           ('elastic collision (molecules)', 'a collision in which the total kinetic energy of the molecules is conserved')],
    facts=[('The mean kinetic energy of a gas molecule at 300 K is', '6.21 × 10⁻²¹ J', ['4.14 × 10⁻²¹ J', '2.07 × 10⁻²¹ J', '1.24 × 10⁻²⁰ J'], '(3/2) × 1.38 × 10⁻²³ × 300.'),
           ('If the absolute temperature of a gas is quadrupled, the rms speed of its molecules', 'doubles', ['quadruples', 'is unchanged', 'increases by 16'], 'c_rms ∝ √T.'),
           ('At the same temperature, hydrogen and oxygen molecules have the same', 'mean kinetic energy', ['rms speed', 'momentum', 'mass'], 'Ē_k depends only on T.'),
           ('According to kinetic theory, the pressure of an ideal gas is given by', 'p = ⅓ρc²_rms', ['p = ρc_rms', 'p = ½ρc²_rms', 'p = 3ρc²_rms'], 'Derived from momentum change at walls.'),
           ('Which is an assumption of the kinetic model of an ideal gas?', 'There are no intermolecular forces except during collisions', ['Molecules attract each other strongly', 'Collisions are inelastic', 'Molecules occupy most of the volume'], 'Ideal gas assumptions.')],
    why=[('Explain, using kinetic theory, why the pressure of a gas increases when it is heated at constant volume.', 'Higher temperature means a larger mean molecular speed; molecules hit the walls more often and with greater change of momentum each time, so the force per unit area increases.'),
         ('Explain, using kinetic theory, why the pressure of a gas increases when its volume is reduced at constant temperature.', 'The molecular speeds are unchanged but the molecules are more crowded, so collisions with each unit area of wall happen more frequently, increasing the rate of momentum transfer.'),
         ('Explain why hydrogen escapes more easily from Earth’s atmosphere than nitrogen.', 'At the same temperature molecules have the same mean KE, so lighter H₂ molecules have a much higher rms speed (√14 ≈ 3.7 times N₂), and a larger fraction exceed escape velocity.')],
    contrast=[('the macroscopic description of a gas', 'the microscopic description of a gas', 'The macroscopic description uses measurable p, V, T and n (gas laws); the microscopic (kinetic) description explains them in terms of the speeds, masses and collisions of molecules.')],
    misc=[('All molecules in a gas at a given temperature move at the same speed.', 'There is a distribution of speeds (Maxwell–Boltzmann); temperature fixes the mean kinetic energy, not each molecule’s speed.'),
          ('Heavier gas molecules have greater kinetic energy at the same temperature.', 'Mean kinetic energy (3/2)k_BT depends only on temperature; heavier molecules move more slowly.'),
          ('At absolute zero an ideal gas has the greatest pressure.', 'p ∝ T for an ideal gas, so the pressure would tend to zero as T → 0 K (real gases liquefy first).')],
    evaluate=[('The kinetic theory of gases is a triumph of the scientific method.', ['it derives the empirical gas laws from simple assumptions', 'it predicts measurable quantities (speed of sound, diffusion rates, specific heats)', 'supported by Brownian motion evidence'], ['early versions faced opposition when atoms were not directly observable', 'it fails for real gases near liquefaction and needs quantum corrections for heat capacities'], 'It is a powerful example of a microscopic model explaining macroscopic laws, with well-understood limits (NOS: models and evidence).')],
    extended=[('Nitrogen (molar mass 28 g mol⁻¹) is at 300 K and 1.0 × 10⁵ Pa. (a) Calculate the mean kinetic energy of a molecule. (b) Calculate the mass of a molecule and its rms speed. (c) Calculate the density of the gas and verify that p = ⅓ρc²_rms. (d) Explain why the speed of sound in nitrogen (≈ 350 m s⁻¹) is of the same order as c_rms.', '(a) 6.21 × 10⁻²¹ J; (b) m = 4.65 × 10⁻²⁶ kg, c_rms = 517 m s⁻¹; (c) ρ = pM/RT = 1.12 kg m⁻³, ⅓ × 1.12 × 517² = 1.0 × 10⁵ Pa; (d) sound is transmitted by molecular collisions, so it cannot travel faster than the molecules themselves move.', 6)],
))


@prob('ch08-st3', d=(1, 5), md=(1, 4), marks=2)
def p_kinetic(rng, slot):
    k = rng.randrange(5)
    gases = [('helium', 4.0), ('nitrogen', 28), ('oxygen', 32), ('carbon dioxide', 44), ('argon', 40), ('hydrogen', 2.0)]
    nm, M = pick(rng, gases)
    T = rng.choice([200, 250, 273, 300, 350, 400, 500, 1000])
    if k == 0:
        return dict(stem=f'Calculate the mean translational kinetic energy of a {nm} molecule at {T} K.', v=1.5 * KB * T, unit='J', wrongs=[KB * T, 3 * KB * T, 1.5 * RGAS * T], key=f'Ē_k = (3/2)k_BT (M1) = {sf(1.5 * KB * T)} J (A1).')
    if k == 1:
        m = M * 1e-3 / NA
        c = math.sqrt(3 * KB * T / m)
        return dict(stem=f'Calculate the rms speed of {nm} molecules (molar mass {M} g mol⁻¹) at {T} K.', v=c, unit='m s⁻¹', wrongs=[math.sqrt(3 * KB * T / (M / NA)), math.sqrt(KB * T / m), 3 * KB * T / m / 1000],
                    key=f'm = {sf(m)} kg (M1); c_rms = √(3k_BT/m) = {sf(c)} m s⁻¹ (A1).', marks=3)
    if k == 2:
        T2 = T * rng.choice([2, 3, 4, 9])
        return dict(stem=f'The temperature of a sample of {nm} is raised from {T} K to {T2} K. Calculate the factor by which the rms speed of its molecules increases.', v=math.sqrt(T2 / T), unit='', wrongs=[T2 / T, (T2 / T) ** 2, math.sqrt((T2 - 273) / (T - 273)) if T > 273 else T2 / T / 2], key=f'c_rms ∝ √T (M1); factor = √({T2}/{T}) = {sf(math.sqrt(T2 / T))} (A1).')
    if k == 3:
        n1, M1 = nm, M
        n2, M2 = pick(rng, [g for g in gases if g[0] != nm])
        r = math.sqrt(M2 / M1)
        return dict(stem=f'{n1[0].upper() + n1[1:]} (M = {M1} g mol⁻¹) and {n2} (M = {M2} g mol⁻¹) are mixed at the same temperature. Calculate the ratio of rms speeds c({n1})/c({n2}).', v=r, unit='', wrongs=[M2 / M1, 1.0, math.sqrt(M1 / M2)], key=f'Same Ē_k: c ∝ 1/√m (M1); ratio = √({M2}/{M1}) = {sf(r)} (A1).')
    p = rng.choice([1.0e5, 1.5e5, 2.0e5]); rho = rng.choice([0.18, 1.2, 1.3, 1.8])
    c = math.sqrt(3 * p / rho)
    return dict(stem=f'A gas of density {rho} kg m⁻³ is at a pressure of {sf(p)} Pa. Use p = ⅓ρc²_rms to calculate the rms speed of its molecules.', v=c, unit='m s⁻¹', wrongs=[math.sqrt(p / rho), 3 * p / rho, math.sqrt(p / (3 * rho))], key=f'c_rms = √(3p/ρ) (M1) = {sf(c)} m s⁻¹ (A1).')


R.mcqs('ch08-st3', 'C2', (1, 4), [
    ('A gas is heated at constant volume. Which quantity is unchanged?', 'The mean distance between molecules', ['The rms speed', 'The pressure', 'The mean kinetic energy'], 'Volume and number of molecules fixed.'),
    ('In a mixture of helium and argon at equilibrium, the helium atoms', 'have the same mean kinetic energy as argon atoms but a higher rms speed', ['have greater mean kinetic energy', 'move more slowly', 'have the same rms speed'], 'Same T.'),
    ('The internal energy of an ideal monatomic gas consists of', 'only the random kinetic energy of its atoms', ['only potential energy', 'kinetic and intermolecular potential energy', 'only the energy of the container'], 'No intermolecular forces.'),
])


R.facts('ch08-st4', F(
    terms=[('real gas', 'a gas whose behaviour deviates from pV = nRT because its molecules have finite volume and exert intermolecular forces'),
           ('compressibility factor', 'the ratio Z = pV/(nRT), equal to 1 for an ideal gas'),
           ('liquefaction', 'the condensation of a gas to a liquid when it is cooled and/or compressed sufficiently'),
           ('critical temperature', 'the temperature above which a gas cannot be liquefied by pressure alone')],
    facts=[('Real gases behave most like ideal gases at', 'low pressure and high temperature', ['high pressure and low temperature', 'high pressure and high temperature', 'low pressure and low temperature'], 'Molecules are far apart and fast.'),
           ('At very high pressure, a real gas has a larger volume than predicted by pV = nRT mainly because', 'the molecules themselves occupy a significant volume', ['intermolecular attractions are large', 'the molecules move faster', 'collisions are elastic'], 'Excluded volume.'),
           ('Intermolecular attractions in a real gas cause the measured pressure to be', 'lower than the ideal-gas prediction', ['higher than predicted', 'exactly as predicted', 'zero'], 'Molecules near the wall are pulled back.'),
           ('Which gas deviates least from ideal behaviour at room temperature and pressure?', 'Helium', ['Ammonia', 'Carbon dioxide', 'Water vapour'], 'Small, weakly attracting atoms.'),
           ('An ideal gas could never be liquefied because', 'it has no intermolecular forces', ['its molecules are too fast', 'its pressure is too low', 'its molecules are too heavy'], 'Attraction is needed to condense.')],
    why=[('Explain why the ideal gas model fails as a gas approaches its condensation point.', 'Molecules move slowly and are close together, so intermolecular attractive forces and their finite size are no longer negligible; the assumptions of the ideal model break down.'),
         ('Explain why polar molecules such as ammonia deviate more from ideal behaviour than noble gases.', 'Polar molecules have stronger intermolecular (dipole) attractions, which reduce the pressure and make the gas easier to liquefy.'),
         ('Explain why the van der Waals equation adds a term a(n/V)² to the pressure.', 'Attractions between molecules reduce the force on the walls; the effect is proportional to the number of pairs of molecules, i.e. to the square of the number density.')],
    contrast=[('an ideal gas', 'a real gas', 'An ideal gas has point molecules with no intermolecular forces and obeys pV = nRT exactly; a real gas has molecules of finite size with intermolecular attractions, deviating from pV = nRT especially at high pressure and low temperature.')],
    misc=[('Real gases always have a lower pV than ideal gases.', 'At moderate pressures attractions lower pV, but at very high pressure the finite molecular volume makes pV larger than nRT.'),
          ('Ideal gases exist at room temperature.', 'No gas is exactly ideal; some (He, H₂, N₂) are very close to ideal at everyday conditions.'),
          ('Increasing pressure always liquefies a gas.', 'Above its critical temperature a gas cannot be liquefied by pressure alone.')],
    evaluate=[('The ideal gas model is useless because no real gas is ideal.', ['real gases deviate at high p and low T'], ['for many gases at everyday conditions the error is under 1 %', 'it provides a clear baseline for more complex models', 'it explains the gas laws from molecular principles'], 'The ideal model is a highly useful approximation; recognising its limits is part of good scientific practice.')],
    extended=[('The van der Waals equation is (p + an²/V²)(V − nb) = nRT. For CO₂, a = 0.364 Pa m⁶ mol⁻² and b = 4.27 × 10⁻⁵ m³ mol⁻¹. (a) Calculate the pressure of 1.00 mol of CO₂ in 1.00 × 10⁻³ m³ at 300 K using the ideal gas equation. (b) Calculate the pressure using the van der Waals equation. (c) Explain the physical meaning of a and b. (d) Comment on the percentage difference.', '(a) 2.49 × 10⁶ Pa; (b) p = RT/(V − b) − a/V² = 2.604 × 10⁶ − 0.364 × 10⁶ = 2.24 × 10⁶ Pa; (c) a accounts for intermolecular attractions, b for the finite volume of the molecules; (d) about 10 % lower – the ideal model is poor at this high density.', 6)],
))


@prob('ch08-st4', d=(2, 5), md=(2, 4), marks=3)
def p_realgas(rng, slot):
    k = rng.randrange(2)
    gas = pick(rng, [('CO₂', 0.364, 4.27e-5), ('N₂', 0.137, 3.87e-5), ('NH₃', 0.423, 3.71e-5), ('CH₄', 0.230, 4.31e-5)])
    nm, a, b = gas
    n = 1.0; V = rng.choice([0.5e-3, 1.0e-3, 2.0e-3, 5.0e-3]); T = rng.choice([280, 300, 350])
    pid = n * RGAS * T / V; pvw = n * RGAS * T / (V - n * b) - a * n * n / V ** 2
    if k == 0:
        return dict(stem=f'Using the van der Waals equation with a = {a} Pa m⁶ mol⁻² and b = {sf(b)} m³ mol⁻¹, calculate the pressure of 1.00 mol of {nm} in {sf(V)} m³ at {T} K.',
                    v=pvw, unit='Pa', wrongs=[pid, n * RGAS * T / (V - b), pid - a / V ** 2 * 2], key=f'p = nRT/(V − nb) − an²/V² (M1) = {sf(n * RGAS * T / (V - b))} − {sf(a / V ** 2)} (M1) = {sf(pvw)} Pa (A1).')
    Z = pvw * V / (n * RGAS * T)
    return dict(stem=f'1.00 mol of {nm} in {sf(V)} m³ at {T} K has a van der Waals pressure of {sf(pvw)} Pa. Calculate the compressibility factor Z = pV/(nRT).',
                v=Z, unit='', wrongs=[1 / Z, 1.0 + (1 - Z), pid / pvw], key=f'Z = {sf(pvw)} × {sf(V)}/(8.31 × {T}) (M1) = {sf(Z)} (A1); Z < 1 shows attractions dominate.', marks=2)


R.mcqs('ch08-st4', 'C2', (1, 4), [
    ('A real gas is cooled at constant pressure towards its boiling point. Compared with an ideal gas, its volume', 'becomes increasingly smaller than predicted', ['becomes larger', 'stays exactly as predicted', 'becomes zero at 0 °C'], 'Attractions pull molecules together.'),
    ('Which assumption of the ideal gas model fails at high pressure?', 'The volume of the molecules is negligible', ['Collisions are elastic', 'Molecules move randomly', 'There are many molecules'], 'Molecules are crowded.'),
    ('Steam at 120 °C and atmospheric pressure is less ideal than helium at the same conditions because', 'water molecules have strong intermolecular attractions (hydrogen bonding)', ['steam is lighter', 'helium is polar', 'steam molecules are smaller'], 'Strength of attractions.'),
])


# =============================================================================================
# ch09 B.4 Thermodynamics (HL)
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('first law of thermodynamics', 'the thermal energy Q transferred to a system equals the increase in internal energy ΔU plus the work W done by the system: Q = ΔU + W'),
           ('work done by a gas', 'the energy transferred when a gas changes volume, W = pΔV at constant pressure and in general the area under the p–V curve'),
           ('internal energy of an ideal monatomic gas', 'the total random kinetic energy of its atoms, U = (3/2)nRT = (3/2)Nk_BT'),
           ('system', 'the part of the universe under study, separated from its surroundings by a boundary'),
           ('thermodynamic process', 'a change of state of a system, described by changes in p, V and T')],
    facts=[('A gas absorbs 500 J of thermal energy and does 200 J of work. Its internal energy', 'increases by 300 J', ['increases by 700 J', 'decreases by 300 J', 'is unchanged'], 'ΔU = Q − W.'),
           ('A gas expands from 2.0 × 10⁻³ m³ to 5.0 × 10⁻³ m³ at a constant pressure of 1.0 × 10⁵ Pa. The work done by the gas is', '300 J', ['500 J', '200 J', '3.0 × 10⁵ J'], 'W = pΔV.'),
           ('When a gas is compressed, the work done by the gas is', 'negative', ['positive', 'zero', 'equal to Q'], 'ΔV < 0.'),
           ('The internal energy of a fixed mass of ideal gas depends only on its', 'temperature', ['pressure', 'volume', 'shape of container'], 'U = (3/2)nRT.'),
           ('The first law of thermodynamics is a statement of', 'conservation of energy', ['conservation of momentum', 'increase of entropy', 'Boyle’s law'], 'Energy bookkeeping.')],
    why=[('Explain, using the first law, why a gas cools when it expands rapidly.', 'In a rapid expansion there is little time for thermal energy transfer (Q ≈ 0); the gas does work on the surroundings, so ΔU = −W is negative and its temperature falls.'),
         ('Explain why the temperature of air in a bicycle pump rises when it is compressed quickly.', 'Work is done on the gas (W negative) with little heat lost, so ΔU = −W > 0 and the temperature rises.'),
         ('Explain why the work done by a gas depends on the path between two states on a p–V diagram.', 'Work is the area under the curve; different paths between the same end points enclose different areas, so W (and hence Q) are path-dependent, though ΔU is not.')],
    contrast=[('heat (Q)', 'work (W) in thermodynamics', 'Both are energy transfers: Q is transferred because of a temperature difference, while W is transferred by a force moving through a distance, such as a gas expanding against a piston.')],
    misc=[('Supplying heat to a gas always increases its temperature.', 'If the gas does at least as much work as the heat supplied (e.g. isothermal expansion), its internal energy and temperature need not rise.'),
          ('A system contains a certain amount of heat.', 'Heat is energy in transfer; a system has internal energy, not heat.'),
          ('In the first law Q = ΔU + W, W is the work done on the gas.', 'In the IB convention, W is the work done by the gas; work done on the gas is −W.')],
    evaluate=[('The first law of thermodynamics means perpetual motion machines are impossible.', ['a machine cannot output more energy than it receives (first-kind perpetual motion)'], ['the first law alone allows a machine converting heat fully to work – the second law forbids this', 'perpetual motion without output (frictionless) is allowed in principle'], 'The first law rules out machines that create energy; the second law is needed to rule out those that turn heat completely into work.')],
    extended=[('0.50 mol of an ideal monatomic gas is heated at a constant pressure of 1.2 × 10⁵ Pa from 300 K to 450 K. (a) Calculate the increase in internal energy. (b) Calculate the change in volume and the work done by the gas. (c) Calculate the thermal energy supplied. (d) Explain why more heat is needed than for the same temperature rise at constant volume.', '(a) ΔU = 1.5 × 0.50 × 8.31 × 150 = 935 J; (b) ΔV = nRΔT/p = 5.19 × 10⁻³ m³, W = 623 J; (c) Q = 1560 J; (d) at constant pressure the gas also does work expanding, so extra energy must be supplied.', 6)],
))


@prob('ch09-st1', d=(1, 5), md=(1, 4), marks=2)
def p_firstlaw(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        Q = rng.choice([200, 350, 500, 800, 1200]); W = rng.choice([80, 150, 250, 400, 600])
        sign = rng.random() < 0.5
        Wg = W if sign else -W
        return dict(stem=f'A gas absorbs {Q} J of thermal energy while {"doing" if sign else "having"} {W} J of work {"on its surroundings" if sign else "done on it"}. Calculate the change in its internal energy.',
                    v=Q - Wg, unit='J', wrongs=[Q + Wg, Wg - Q, Q], key=f'ΔU = Q − W with W = {sf(Wg)} J (M1); ΔU = {sf(Q - Wg)} J (A1).')
    if k == 1:
        p = rng.choice([1.0e5, 1.5e5, 2.0e5, 3.0e5]); V1 = rng.choice([1.0, 2.0, 3.0]); V2 = V1 + rng.choice([0.5, 1.0, 2.0, 2.5])
        return dict(stem=f'A gas expands at a constant pressure of {sf(p)} Pa from {V1} × 10⁻³ m³ to {V2} × 10⁻³ m³. Calculate the work done by the gas.',
                    v=p * (V2 - V1) * 1e-3, unit='J', wrongs=[p * V2 * 1e-3, p * (V2 - V1), p * (V2 + V1) * 1e-3 / 2], key=f'W = pΔV (M1) = {sf(p)} × {sf(V2 - V1)} × 10⁻³ = {sf(p * (V2 - V1) * 1e-3)} J (A1).')
    if k == 2:
        n = rng.choice([0.20, 0.50, 1.0, 2.0]); dT = rng.choice([20, 50, 80, 120])
        return dict(stem=f'Calculate the change in internal energy when {n} mol of an ideal monatomic gas is heated through {dT} K.',
                    v=1.5 * n * RGAS * dT, unit='J', wrongs=[n * RGAS * dT, 2.5 * n * RGAS * dT, 1.5 * KB * dT], key=f'ΔU = (3/2)nRΔT (M1) = {sf(1.5 * n * RGAS * dT)} J (A1).')
    if k == 3:
        n = rng.choice([0.20, 0.50, 1.0]); dT = rng.choice([40, 60, 100])
        Q = 2.5 * n * RGAS * dT
        return dict(stem=f'{n} mol of a monatomic ideal gas is heated at constant pressure so that its temperature rises by {dT} K. Calculate the thermal energy supplied.',
                    v=Q, unit='J', wrongs=[1.5 * n * RGAS * dT, n * RGAS * dT, 2 * n * RGAS * dT], key=f'ΔU = (3/2)nRΔT, W = pΔV = nRΔT (M1); Q = (5/2)nRΔT = {sf(Q)} J (A1).', marks=3)
    Q = rng.choice([0]); W = rng.choice([150, 300, 450])
    return dict(stem=f'A gas in an insulated cylinder (no thermal energy transfer) is compressed by a piston that does {W} J of work on it. Calculate the change in internal energy of the gas.',
                v=W, unit='J', wrongs=[-W, 0.5 * W, 2 * W], key=f'Q = 0; W (by gas) = −{W} J (M1); ΔU = Q − W = +{W} J (A1).')


R.mcqs('ch09-st1', 'C2', (1, 4), [
    ('An ideal gas is taken through a complete cycle back to its initial state. Over the cycle, ΔU is', 'zero', ['equal to the work done', 'equal to Q supplied', 'always positive'], 'U is a state function.'),
    ('An ideal gas expands at constant temperature. Which is correct?', 'Q = W and ΔU = 0', ['Q = 0 and ΔU = −W', 'W = 0 and Q = ΔU', 'Q = ΔU = W'], 'Isothermal: U constant.'),
    ('Which statement about the work done by a gas on a p–V diagram is correct?', 'It equals the area under the curve', ['It equals the gradient of the curve', 'It is the same for all paths between two states', 'It is always positive'], 'W = ∫p dV.'),
])


R.facts('ch09-st2', F(
    terms=[('isovolumetric (isochoric) process', 'a process at constant volume, in which no work is done and Q = ΔU'),
           ('isobaric process', 'a process at constant pressure, in which W = pΔV'),
           ('isothermal process', 'a process at constant temperature, for which ΔU = 0 and Q = W; pV = constant for an ideal gas'),
           ('adiabatic process', 'a process with no thermal energy transfer (Q = 0), so ΔU = −W; for an ideal monatomic gas pV^(5/3) = constant'),
           ('p–V diagram', 'a graph of pressure against volume on which a process is shown as a curve and the work done is the area under it')],
    facts=[('On a p–V diagram, an isothermal curve for an ideal gas is', 'a hyperbola (pV = constant)', ['a straight horizontal line', 'a straight vertical line', 'a straight line through the origin'], 'Boyle’s law.'),
           ('An adiabatic curve on a p–V diagram is', 'steeper than an isothermal curve through the same point', ['less steep than an isothermal', 'horizontal', 'identical to an isothermal'], 'p ∝ V^(−5/3) vs V^(−1).'),
           ('In which process is no work done by the gas?', 'Isovolumetric', ['Isobaric', 'Isothermal', 'Adiabatic'], 'ΔV = 0.'),
           ('During an adiabatic expansion of an ideal gas, the temperature', 'decreases', ['increases', 'stays constant', 'first increases then decreases'], 'ΔU = −W < 0.'),
           ('For an ideal monatomic gas, the adiabatic index γ = 5/3 because', 'C_p/C_V = (5/2)R/(3/2)R', ['γ = 1 + R', 'it is defined that way for all gases', 'γ = 3/5 inverted'], 'Ratio of molar heat capacities.')],
    why=[('Explain why a rapid compression can be modelled as adiabatic.', 'Thermal energy transfer requires time; if the compression is very fast (or the gas well insulated) Q ≈ 0, so all work done on the gas increases its internal energy.'),
         ('Explain why the adiabatic curve through a point is steeper than the isothermal curve through the same point.', 'In adiabatic compression the temperature rises as well as the volume decreasing, so the pressure increases more than in an isothermal compression where T is constant.'),
         ('Explain how the work done in a cyclic process is found from a p–V diagram.', 'The net work done by the gas over a cycle equals the area enclosed by the loop; clockwise loops give positive net work done by the gas.')],
    contrast=[('an isothermal process', 'an adiabatic process', 'In an isothermal process T is constant, so ΔU = 0 and Q = W (heat flows in or out); in an adiabatic process Q = 0, so ΔU = −W and the temperature changes.')],
    misc=[('In an isothermal expansion no heat is transferred because the temperature does not change.', 'Heat must flow in to keep T constant while the gas does work: Q = W.'),
          ('In an adiabatic process the temperature stays constant.', 'Adiabatic means no thermal energy transfer; the temperature changes because work is done.'),
          ('Isobaric means no work is done.', 'Isobaric means constant pressure; work pΔV is done if the volume changes. Isovolumetric processes involve no work.')],
    evaluate=[('Real processes in engines can be described accurately as isothermal or adiabatic.', ['these idealisations allow simple calculations of work and efficiency', 'fast strokes are approximately adiabatic'], ['real processes are neither perfectly fast nor slow; heat leaks occur', 'friction and turbulence make processes irreversible', 'the gas composition changes during combustion'], 'The idealised processes are useful models whose predictions must be corrected for real heat transfer and irreversibility.')],
    extended=[('1.00 mol of a monatomic ideal gas at 1.00 × 10⁵ Pa and 300 K is compressed adiabatically to one-quarter of its volume. (a) Calculate the initial volume. (b) Calculate the final pressure and temperature. (c) Calculate the work done on the gas. (d) Compare the final pressure with that for an isothermal compression to the same volume and explain the difference.', '(a) V = nRT/p = 0.0249 m³; (b) p₂ = p₁ × 4^(5/3) = 1.01 × 10⁶ Pa, T₂ = 300 × 4^(2/3) = 756 K; (c) W_on = ΔU = 1.5 × 8.31 × 456 = 5.68 kJ; (d) isothermal gives 4.00 × 10⁵ Pa; the adiabatic pressure is higher because the temperature also rises.', 6)],
))


@prob('ch09-st2', d=(1, 5), md=(1, 4), marks=3)
def p_processes(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        p1 = rng.choice([1.0e5, 2.0e5]); f = rng.choice([2, 3, 4, 0.5])
        p2 = p1 * f ** (-5 / 3)
        return dict(stem=f'An ideal monatomic gas at {sf(p1)} Pa {"expands" if f > 1 else "is compressed"} adiabatically to {f:g} times its original volume. Calculate the final pressure (γ = 5/3).',
                    v=p2, unit='Pa', wrongs=[p1 / f, p1 * f ** (-3 / 5), p1 * f ** (5 / 3)], key=f'pV^γ constant (M1); p₂ = p₁(V₁/V₂)^(5/3) = {sf(p2)} Pa (A1).', marks=2)
    if k == 1:
        T1 = rng.choice([280, 300, 320]); f = rng.choice([2, 3, 4, 8])
        T2 = T1 * f ** (2 / 3)
        return dict(stem=f'A monatomic ideal gas at {T1} K is compressed adiabatically to 1/{f} of its volume. Calculate its final temperature.',
                    v=T2, unit='K', wrongs=[T1 * f, T1 * f ** (5 / 3), T1 * f ** (1 / 3)], key=f'TV^(γ−1) constant (M1); T₂ = {T1} × {f}^(2/3) = {sf(T2)} K (A1).', marks=2)
    if k == 2:
        n = rng.choice([0.50, 1.0, 2.0]); T = rng.choice([300, 350, 400]); r = rng.choice([2, 3, 4])
        W = n * RGAS * T * math.log(r)
        return dict(stem=f'{n} mol of an ideal gas expands isothermally at {T} K to {r} times its initial volume. Calculate the work done by the gas (W = nRT ln(V₂/V₁)).',
                    v=W, unit='J', wrongs=[n * RGAS * T * r, n * RGAS * T * math.log10(r), n * RGAS * T * (r - 1)], key=f'W = nRT ln{r} (M1) = {sf(W)} J (A1); Q = W since ΔU = 0.', marks=2)
    if k == 3:
        pA = rng.choice([1.0e5, 2.0e5]); pB = pA * rng.choice([2, 3]); V1 = rng.choice([1.0e-3, 2.0e-3]); V2 = V1 * rng.choice([2, 3])
        W = (pB - pA) * (V2 - V1)
        return dict(stem=f'An ideal gas is taken round a rectangular cycle on a p–V diagram between pressures {sf(pA)} Pa and {sf(pB)} Pa and volumes {sf(V1)} m³ and {sf(V2)} m³. Calculate the net work done per cycle.',
                    v=W, unit='J', wrongs=[pB * V2, pB * (V2 - V1), (pB + pA) * (V2 - V1) / 2], key=f'Net work = enclosed area = Δp × ΔV (M1) = {sf(W)} J (A1).', marks=2)
    n = rng.choice([0.20, 0.50, 1.0]); dT = rng.choice([30, 60, 90])
    Q = 1.5 * n * RGAS * dT
    return dict(stem=f'{n} mol of a monatomic ideal gas in a rigid sealed container is heated so that its temperature rises by {dT} K. Calculate the thermal energy supplied.',
                v=Q, unit='J', wrongs=[2.5 * n * RGAS * dT, n * RGAS * dT, 1.5 * n * RGAS * (dT + 273)], key=f'Isovolumetric: W = 0 (M1); Q = ΔU = (3/2)nRΔT = {sf(Q)} J (A1).', marks=2)


@R.add('ch09-st2', 'C4', (3, 5), 'multi_step')
def c4_cycle(rng, slot):
    n = 1.0; T1 = rng.choice([300, 320]); p1 = 1.0e5; r = rng.choice([2, 3])
    V1 = n * RGAS * T1 / p1; V2 = r * V1
    T2 = T1 * r  # isobaric expansion
    W12 = p1 * (V2 - V1); Q12 = 2.5 * n * RGAS * (T2 - T1)
    Q23 = 1.5 * n * RGAS * (T1 - T2)  # isovolumetric cool to T1 (p falls to p1/r)
    W31 = -n * RGAS * T1 * math.log(r)  # isothermal compression back
    Wnet = W12 + W31
    return num(f'1.00 mol of a monatomic ideal gas at A ({sf(p1)} Pa, {T1} K) undergoes a cycle: A→B isobaric expansion to {r} times the volume; B→C isovolumetric cooling back to {T1} K; C→A isothermal compression to A. (a) Sketch the cycle on a p–V diagram. (b) Calculate the temperature at B and the pressure at C. (c) Calculate the work done in each stage. (d) Determine the net work done per cycle and the thermal energy absorbed in A→B. (e) Calculate the efficiency of the cycle.',
               f'(b) T_B = {sf(T2)} K, p_C = {sf(p1 / r)} Pa; (c) W_AB = {sf(W12)} J, W_BC = 0, W_CA = {sf(W31)} J; (d) W_net = {sf(Wnet)} J, Q_AB = {sf(Q12)} J; (e) η = {sf(100 * Wnet / Q12, 3)} %',
               f'(a) A1. (b) A1 A1. (c) pΔV (A1), 0, nRT ln(V_C/V_A) (M1 A1). (d) W_net (A1), Q = (5/2)nRΔT (A1). (e) η = W/Q_in (A1).', 9, 'multi_step')


R.mcqs('ch09-st2', 'C2', (1, 4), [
    ('A gas is compressed to half its volume, once isothermally and once adiabatically from the same initial state. The final pressure is', 'higher for the adiabatic compression', ['higher for the isothermal compression', 'the same in both', 'zero in the adiabatic case'], 'Temperature rises adiabatically.'),
    ('On a p–V diagram, a vertical straight line represents', 'an isovolumetric process', ['an isobaric process', 'an isothermal process', 'an adiabatic process'], 'Volume constant.'),
    ('In an isobaric expansion of an ideal gas, the temperature', 'increases', ['decreases', 'stays the same', 'falls to zero'], 'V ∝ T at constant p.'),
])


def _adiabatic_spec(rng):
    p0, V0 = 1.0e5, 50.0
    Vs = [50.0, 45.0, 40.0, 35.0, 30.0, 25.0]
    g_ = rng.uniform(1.36, 1.42)
    ps = [round(p0 * (V0 / v) ** g_ / 1e3 * rng.uniform(0.995, 1.005), 1) for v in Vs]
    return dict(intro='Air in a syringe is compressed rapidly and the pressure is recorded with a fast pressure sensor at several volumes. For an adiabatic process pV^γ = constant, so ln p = −γ ln V + constant.',
                xname='V', xunit='cm³', yname='p', yunit='kPa', xs=Vs, ys=ps, xfmt=lambda x: f'{x:.1f}', yfmt=lambda y: f'{y:.1f}',
                plot_x=lambda x: math.log(x), plot_y=lambda y: math.log(y), plot_label='ln p (y) against ln V (x)', what='the adiabatic index γ of air', what_short='γ',
                gunit='', deduce=lambda m_, b_: (-m_, '', 'γ = −gradient'))


gradient_fit('ch09-st2', _adiabatic_spec)


R.facts('ch09-st3', F(
    terms=[('entropy', 'a measure of the disorder of a system, related to the number of microstates Ω by S = k_B ln Ω'),
           ('second law of thermodynamics', 'the total entropy of an isolated system never decreases; equivalently, thermal energy cannot spontaneously flow from a colder to a hotter body'),
           ('microstate', 'one particular arrangement of the positions and energies of all the particles in a system'),
           ('macrostate', 'the state of a system described by macroscopic variables (p, V, T), corresponding to many microstates'),
           ('reversible process', 'an idealised process that can be reversed by an infinitesimal change, with no net increase in the entropy of the universe')],
    facts=[('When 600 J of thermal energy is transferred reversibly to a reservoir at 300 K, its entropy changes by', '+2.0 J K⁻¹', ['+1.8 × 10⁵ J K⁻¹', '−2.0 J K⁻¹', '+0.50 J K⁻¹'], 'ΔS = Q/T.'),
           ('Which process involves a decrease in the entropy of the system?', 'Water freezing to ice', ['Ice melting', 'A gas expanding into a vacuum', 'Sugar dissolving in tea'], 'A crystal is more ordered.'),
           ('The unit of entropy is', 'J K⁻¹', ['J', 'K', 'J K'], 'ΔS = Q/T.'),
           ('Clausius’s statement of the second law says that', 'heat cannot flow spontaneously from a colder to a hotter body', ['energy is conserved', 'entropy always decreases', 'all engines are 100 % efficient'], 'Requires work to reverse.'),
           ('The entropy of a system can decrease if', 'the entropy of the surroundings increases by at least as much', ['energy is created', 'the system is isolated', 'never – it can never decrease'], 'Total entropy of universe does not decrease.')],
    why=[('Explain why a refrigerator does not violate the second law of thermodynamics.', 'It transfers heat from cold to hot only because work is done on it; the heat released to the room exceeds that taken from inside, so the total entropy of the universe increases.'),
         ('Explain, in terms of microstates, why a gas spreads out to fill its container.', 'There are vastly more microstates with the molecules spread throughout the container than with them concentrated in one part, so the spread-out macrostate is overwhelmingly more probable – entropy increases.'),
         ('Explain why living organisms do not violate the second law even though they create ordered structures.', 'Organisms are open systems; they take in low-entropy energy (food, sunlight) and release heat and waste that increase the entropy of the surroundings by more than their internal decrease.')],
    contrast=[('a reversible process', 'an irreversible process', 'A reversible process is an idealisation in which the system and surroundings can be returned to their original states with no net entropy change; real (irreversible) processes, involving friction, heat flow across finite temperature differences or free expansion, increase the total entropy.')],
    misc=[('Entropy can never decrease anywhere.', 'The entropy of a part of a system can decrease (e.g. freezing water) if the surroundings gain at least as much entropy; the total entropy of an isolated system cannot decrease.'),
          ('The second law means energy is lost.', 'Energy is conserved (first law); the second law says energy becomes less available for doing work as entropy increases.'),
          ('Entropy is just another word for energy.', 'Entropy (J K⁻¹) measures the number of microscopic arrangements available, i.e. how dispersed energy is; it is not an amount of energy.')],
    evaluate=[('The second law of thermodynamics gives time its direction.', ['irreversible processes (mixing, heat flow, ageing) all increase entropy', 'we never observe entropy decreasing spontaneously in isolated systems'], ['fundamental laws of mechanics are time-symmetric', 'the arrow depends on the universe’s special low-entropy initial state', 'other arrows (cosmological, psychological) have been proposed'], 'The entropy increase provides a strong account of the arrow of time, but it depends on initial conditions and remains an active area of philosophical debate (TOK link).')],
    extended=[('A 0.50 kg block of ice at 0 °C melts in a room at 22 °C. L_f = 3.34 × 10⁵ J kg⁻¹. (a) Calculate the energy absorbed by the ice. (b) Calculate the entropy change of the ice. (c) Calculate the entropy change of the room. (d) Show that the total entropy of the universe increases and explain the significance.', '(a) 1.67 × 10⁵ J; (b) +1.67 × 10⁵/273 = +612 J K⁻¹; (c) −1.67 × 10⁵/295 = −566 J K⁻¹; (d) net +46 J K⁻¹ > 0, consistent with the second law – heat flows spontaneously from hot to cold.', 6)],
))


@prob('ch09-st3', d=(1, 5), md=(1, 4), marks=2)
def p_entropy(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        Q = rng.choice([300, 600, 1200, 5000, 2.26e4]); T = rng.choice([250, 273, 300, 373, 500])
        return dict(stem=f'{sf(Q)} J of thermal energy is transferred reversibly into a large reservoir at {T} K. Calculate the entropy change of the reservoir.',
                    v=Q / T, unit='J K⁻¹', wrongs=[Q * T, T / Q, Q / (T - 273) if T > 273 else Q / T * 2], key=f'ΔS = Q/T (M1) = {sf(Q / T)} J K⁻¹ (A1).')
    if k == 1:
        Q = rng.choice([500, 1000, 2000]); Th = rng.choice([400, 500, 600]); Tc = rng.choice([280, 300])
        dS = Q / Tc - Q / Th
        return dict(stem=f'{Q} J of thermal energy flows from a reservoir at {Th} K to one at {Tc} K. Calculate the total change in entropy.',
                    v=dS, unit='J K⁻¹', wrongs=[Q / Th + Q / Tc, Q / (Th - Tc), Q / Th - Q / Tc], key=f'ΔS = −Q/T_h + Q/T_c (M1) = {sf(dS)} J K⁻¹ (> 0) (A1).')
    if k == 2:
        m = rng.choice([0.10, 0.25, 0.50, 1.0])
        dS = m * 3.34e5 / 273
        return dict(stem=f'Calculate the entropy change when {m} kg of ice melts at 0 °C. (L_f = 3.34 × 10⁵ J kg⁻¹)',
                    v=dS, unit='J K⁻¹', wrongs=[m * 3.34e5, m * 3.34e5 / 0.01, m * 3.34e5 / 373], key=f'ΔS = mL/T = {m} × 3.34 × 10⁵/273 (M1) = {sf(dS)} J K⁻¹ (A1).')
    if k == 3:
        W1, W2 = rng.choice([(1, 1e3), (10, 1e6), (1e5, 1e20), (2, 2e10)])
        dS = KB * math.log(W2 / W1)
        return dict(stem=f'The number of microstates of a system increases from {sf(W1)} to {sf(W2)}. Calculate the change in entropy using S = k_B ln Ω.',
                    v=dS, unit='J K⁻¹', wrongs=[KB * W2 / W1, KB * math.log10(W2 / W1), KB * (W2 - W1)], key=f'ΔS = k_B ln(Ω₂/Ω₁) (M1) = {sf(dS)} J K⁻¹ (A1).')
    N = rng.choice([4, 6, 8, 10])
    Om = math.comb(N, N // 2)
    return dict(stem=f'{N} gas molecules move randomly between the two halves of a box. How many microstates correspond to the macrostate with exactly half the molecules in each side?',
                v=Om, unit='', n=4, ans=str(Om), wrongs=[2 ** N, N, N * N // 2], key=f'Ω = {N}C{N // 2} = {Om} (M1 A1); this macrostate has the most microstates, so it has the highest entropy.')


R.mcqs('ch09-st3', 'C2', (1, 4), [
    ('A gas expands freely into an evacuated chamber in an insulated container. Its entropy', 'increases', ['decreases', 'stays the same', 'becomes zero'], 'More microstates available.'),
    ('Heat flows from a hot body to a cold body because', 'this increases the total entropy', ['this conserves entropy', 'cold bodies have more energy', 'it decreases total entropy'], 'Second law.'),
    ('A perfectly ordered crystal at 0 K has an entropy of', 'zero (only one microstate)', ['infinity', 'k_B', 'the same as a gas'], 'Third law: ln 1 = 0.'),
])


R.facts('ch09-st4', F(
    terms=[('heat engine', 'a device that takes in thermal energy from a hot reservoir, converts part of it into work and rejects the rest to a cold reservoir'),
           ('thermal efficiency', 'the ratio of the useful work output to the thermal energy input, η = W/Q_H'),
           ('Carnot cycle', 'an idealised reversible cycle of two isothermal and two adiabatic processes, giving the maximum possible efficiency between two temperatures'),
           ('Carnot efficiency', 'the maximum efficiency of any heat engine operating between reservoirs at T_H and T_C, η = 1 − T_C/T_H'),
           ('Kelvin–Planck statement', 'no heat engine operating in a cycle can convert all the thermal energy absorbed from a reservoir into work')],
    facts=[('A heat engine absorbs 1000 J and rejects 650 J per cycle. Its efficiency is', '35 %', ['65 %', '54 %', '100 %'], 'W = 350 J.'),
           ('The maximum efficiency of an engine working between 600 K and 300 K is', '50 %', ['100 %', '200 %', '33 %'], '1 − 300/600.'),
           ('The Carnot cycle consists of', 'two isothermal and two adiabatic processes', ['two isobaric and two isovolumetric', 'four adiabatic processes', 'one of each type of process'], 'Definition.'),
           ('To increase the Carnot efficiency, an engineer should', 'increase T_H or decrease T_C', ['decrease T_H', 'increase T_C', 'use a larger engine'], 'η = 1 − T_C/T_H.'),
           ('The net work done per cycle by a heat engine is shown on a p–V diagram by', 'the area enclosed by the cycle', ['the gradient of the isotherm', 'the height of the cycle', 'the area under the expansion stroke only'], 'Cycle area.')],
    why=[('Explain why no heat engine can be 100 % efficient.', 'To return to its initial state in a cycle the engine must reject some thermal energy to a cold reservoir; rejecting no heat would decrease the total entropy, which the second law forbids. Efficiency 100 % would require T_C = 0 K.'),
         ('Explain why power stations are built next to rivers or the sea.', 'They need a large cold reservoir to absorb the rejected thermal energy; the lower T_C, the higher the possible efficiency.'),
         ('Explain why the efficiency of a real engine is lower than the Carnot efficiency.', 'Real cycles are irreversible: friction, turbulence and heat transfer across finite temperature differences increase entropy, and the processes are not ideal isotherms and adiabats.')],
    contrast=[('a heat engine', 'a heat pump', 'A heat engine uses heat flowing from hot to cold to produce work; a heat pump uses work to move thermal energy from a cold to a hot region.')],
    misc=[('A Carnot engine can reach 100 % efficiency if it has no friction.', 'Even an ideal, frictionless Carnot engine has η = 1 − T_C/T_H < 1, unless T_C = 0 K.'),
          ('In the Carnot efficiency formula, temperatures can be in °C.', 'Temperatures must be in kelvin; using °C gives wrong (even negative) efficiencies.'),
          ('The heat rejected by a power station is a sign of poor engineering that can be eliminated.', 'Some heat rejection is required by the second law; engineering can only reduce it towards the Carnot limit (or use the waste heat in combined heat and power).')],
    evaluate=[('Combined heat and power (CHP) stations are a better use of fuel than conventional power stations.', ['use the rejected heat for district heating, raising total energy utilisation to ~80 %', 'reduce fuel use and emissions'], ['need nearby heat users (cities, industry)', 'electrical efficiency may be slightly lower', 'heat demand varies seasonally'], 'CHP makes much better use of fuel where there is a steady local heat demand, but it is not suitable everywhere.')],
    extended=[('A steam turbine operates between 820 K and 310 K. Its actual efficiency is 38 % and its electrical output is 600 MW. (a) Calculate the Carnot efficiency. (b) Calculate the thermal energy input per second. (c) Calculate the thermal energy rejected per second. (d) The rejected heat goes into river water; calculate the mass flow of water needed if its temperature may rise by only 8.0 K. (e) Suggest one way to increase the efficiency.', '(a) 62 %; (b) 1580 MW; (c) 980 MW; (d) 9.8 × 10⁸/(4180 × 8.0) = 2.9 × 10⁴ kg s⁻¹; (e) raise the steam temperature (superheating) or use combined cycle/CHP.', 7)],
))


@prob('ch09-st4', d=(1, 5), md=(1, 4), marks=2)
def p_engine(rng, slot):
    k = rng.randrange(5)
    city = rng.choice(CITIES)
    if k == 0:
        Th = rng.choice([500, 600, 800, 900, 1200]); Tc = rng.choice([280, 300, 310, 320])
        return dict(stem=f'Calculate the Carnot efficiency of an engine operating between reservoirs at {Th} K and {Tc} K.',
                    v=100 * (1 - Tc / Th), unit='%', wrongs=[100 * Tc / Th, 100 * (1 - (Tc - 273) / (Th - 273)), 100 * (Th - Tc) / Tc], key=f'η = 1 − T_C/T_H (M1) = {sf(100 * (1 - Tc / Th))} % (A1).')
    if k == 1:
        Q = rng.choice([800, 1200, 2000, 5000]); W = Q * rng.choice([0.20, 0.25, 0.30, 0.35, 0.40])
        return dict(stem=f'A heat engine absorbs {Q} J from the hot reservoir and does {sf(W)} J of work per cycle. Calculate the thermal energy rejected to the cold reservoir.',
                    v=Q - W, unit='J', wrongs=[Q + W, W, Q], key=f'Q_C = Q_H − W (M1) = {sf(Q - W)} J (A1).')
    if k == 2:
        P = rng.choice([500, 660, 1000, 1200]); eta = rng.choice([0.33, 0.38, 0.45, 0.55])
        return dict(stem=f'A power station near {city} produces {P} MW of electrical power with an overall efficiency of {int(eta * 100)} %. Calculate the rate at which thermal energy is rejected.',
                    v=P / eta - P, unit='MW', wrongs=[P / eta, P * eta, P * (1 - eta)], key=f'Input = {P}/{eta} = {sf(P / eta)} MW (M1); rejected = {sf(P / eta - P)} MW (A1).')
    if k == 3:
        eta = rng.choice([0.40, 0.50, 0.60, 0.65]); Tc = rng.choice([290, 300, 310])
        return dict(stem=f'An engineer wants a Carnot efficiency of {int(eta * 100)} % with a cold reservoir at {Tc} K. Calculate the minimum temperature of the hot reservoir.',
                    v=Tc / (1 - eta), unit='K', wrongs=[Tc / eta, Tc * (1 + eta), Tc / (1 - eta) - 273], key=f'T_H = T_C/(1 − η) (M1) = {sf(Tc / (1 - eta))} K (A1).')
    Th = rng.choice([550, 650, 750]); Tc = rng.choice([300, 320]); eta_real = rng.choice([0.25, 0.30, 0.35])
    eC = 1 - Tc / Th
    if eta_real >= eC:
        return None
    return dict(stem=f'A car engine runs between a combustion temperature of {Th} K and exhaust temperature {Tc} K, with an actual efficiency of {int(eta_real * 100)} %. Calculate the actual efficiency as a percentage of the Carnot efficiency.',
                v=100 * eta_real / eC, unit='%', wrongs=[100 * eC, 100 * eta_real, 100 * eC / eta_real / 10], key=f'η_C = 1 − {Tc}/{Th} = {sf(eC)} (M1); ratio = {eta_real}/{sf(eC)} = {sf(100 * eta_real / eC)} % (A1).')


R.mcqs('ch09-st4', 'C2', (1, 4), [
    ('Two Carnot engines X and Y both have T_C = 300 K; X has T_H = 600 K and Y has T_H = 900 K. Which is correct?', 'Y is more efficient than X', ['X is more efficient', 'They have equal efficiency', 'Neither can do work'], 'η = 1 − T_C/T_H.'),
    ('A heat engine would be 100 % efficient if', 'the cold reservoir were at 0 K', ['there were no friction', 'the hot reservoir were very hot', 'it ran very slowly'], 'Carnot limit.'),
    ('In a Carnot cycle, thermal energy is absorbed during', 'the isothermal expansion at T_H', ['the adiabatic expansion', 'the isothermal compression at T_C', 'the adiabatic compression'], 'Heat in at T_H.'),
])


# =============================================================================================
# ch10 B.5 Current and circuits
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('electric current', 'the rate of flow of charge, I = ΔQ/Δt, measured in amperes'),
           ('potential difference', 'the work done (energy transferred) per unit charge moving between two points, V = W/q, measured in volts'),
           ('coulomb', 'the charge passing a point when a current of 1 A flows for 1 s'),
           ('drift speed', 'the mean speed of the charge carriers along a conductor, given by I = nAvq'),
           ('conventional current', 'the direction in which positive charge would flow, from + to − outside the source'),
           ('charge carrier density', 'the number of free charge carriers per unit volume, n, in m⁻³')],
    facts=[('A current of 2.0 A flows for 30 s. The charge passing a point is', '60 C', ['15 C', '0.067 C', '32 C'], 'Q = It.'),
           ('How many electrons pass a point each second in a current of 1.0 A?', '6.25 × 10¹⁸', ['1.6 × 10⁻¹⁹', '6.02 × 10²³', '1.0'], 'n = I/e.'),
           ('One volt is equivalent to', 'one joule per coulomb', ['one coulomb per second', 'one joule per second', 'one ampere per ohm'], 'V = W/q.'),
           ('The drift speed of electrons in a copper wire carrying a typical current is about', '10⁻⁴ m s⁻¹', ['3 × 10⁸ m s⁻¹', '10³ m s⁻¹', '1 m s⁻¹'], 'Very slow; signals travel fast.'),
           ('If a wire’s cross-sectional area is halved at the same current, the drift speed', 'doubles', ['halves', 'stays the same', 'quadruples'], 'v = I/(nAq).')],
    why=[('Explain why a lamp lights almost instantly when switched on even though electrons drift very slowly.', 'The wire is already full of free electrons; the electric field is established along the circuit at nearly the speed of light, so all electrons start drifting at once.'),
         ('Explain why the drift speed is larger in a thin section of wire than a thick section carrying the same current.', 'The same charge per second must pass every point; from I = nAvq with n and q fixed, a smaller A requires a larger v.'),
         ('Explain why metals are good conductors while insulators are not.', 'Metals have a very high density of free (delocalised) electrons that can move through the lattice; insulators have almost no free charge carriers.')],
    contrast=[('electromotive force', 'potential difference', 'EMF is the energy transferred to each coulomb of charge by a source (e.g. chemical → electrical); potential difference is the energy transferred from each coulomb to other forms as it passes through a component.')],
    misc=[('Current is used up as it flows through a lamp.', 'Charge is conserved: the current into a component equals the current out. Energy, not current, is transferred.'),
          ('Electrons move through a wire at nearly the speed of light.', 'Electrons drift at around 10⁻⁴ m s⁻¹; the electric field (signal) propagates at nearly the speed of light.'),
          ('Conventional current flows in the same direction as electrons.', 'Conventional current is defined as the flow of positive charge; electrons in metals move in the opposite direction.')],
    evaluate=[('Using conventional current instead of electron flow causes confusion and should be abandoned.', ['electrons actually move the opposite way in metals', 'beginners find the convention confusing'], ['all circuit laws and symbols use the conventional direction consistently', 'in electrolytes and semiconductors positive carriers also move', 'changing would disrupt engineering practice'], 'The convention is arbitrary but consistent and works for all carrier types, so it is retained (NOS: conventions).')],
    extended=[('A copper wire of diameter 1.0 mm carries a current of 3.0 A. Copper has 8.5 × 10²⁸ free electrons per m³. (a) Calculate the cross-sectional area. (b) Calculate the drift speed. (c) Calculate the time for an electron to drift 1.0 m. (d) Explain why the lamp at the end of a 1.0 m wire lights immediately.', '(a) A = 7.85 × 10⁻⁷ m²; (b) v = I/(nAe) = 2.8 × 10⁻⁴ m s⁻¹; (c) ≈ 3.6 × 10³ s (about an hour); (d) the electric field is set up throughout the circuit almost instantly, so electrons everywhere start moving at once.', 6)],
))


@prob('ch10-st1', d=(1, 5), md=(1, 4), marks=2)
def p_current(rng, slot):
    k = rng.randrange(5)
    city = rng.choice(CITIES)
    if k == 0:
        I = rng.choice([0.20, 0.50, 1.5, 2.5, 4.0, 13]); t = rng.choice([30, 60, 120, 300, 600])
        return dict(stem=f'A current of {I} A flows through a heater element for {t} s. Calculate the charge that passes through it.', v=I * t, unit='C', wrongs=[I / t, t / I, I * t / 60], key=f'Q = It (M1) = {sf(I * t)} C (A1).')
    if k == 1:
        I = rng.choice([0.10, 0.50, 2.0, 5.0])
        return dict(stem=f'Calculate the number of electrons passing a point per second in a wire carrying {I} A.', v=I / E, unit='s⁻¹', wrongs=[I * E, E / I, I / E / 1e3], key=f'N = I/e (M1) = {sf(I / E)} s⁻¹ (A1).')
    if k == 2:
        V = rng.choice([1.5, 3.0, 6.0, 9.0, 12, 230]); Q = rng.choice([5.0, 20, 50, 100])
        return dict(stem=f'Calculate the energy transferred when {Q} C of charge moves through a potential difference of {V} V.', v=V * Q, unit='J', wrongs=[V / Q, Q / V, V * Q / 2], key=f'W = qV (M1) = {sf(V * Q)} J (A1).')
    if k == 3:
        I = rng.choice([1.0, 2.0, 3.0, 5.0]); d = rng.choice([0.50, 1.0, 1.5, 2.0]) * 1e-3; n = rng.choice([8.5e28, 5.9e28, 6.0e28])
        metal = {8.5e28: 'copper', 5.9e28: 'silver', 6.0e28: 'aluminium'}[n]
        A = math.pi * (d / 2) ** 2; v = I / (n * A * E)
        return dict(stem=f'A wire made of {metal}, of diameter {d * 1000:g} mm, carries {I} A. The free-electron density is {sf(n, 2)} m⁻³. Calculate the drift speed of the electrons.',
                    v=v, unit='m s⁻¹', wrongs=[I / (n * math.pi * d * d * E), I / (n * A), v * 1e3], key=f'A = π({d / 2:g})² = {sf(A)} m² (M1); v = I/(nAe) = {sf(v)} m s⁻¹ (A1).', marks=3)
    W = rng.choice([360, 720, 1440, 4800]); t = rng.choice([60, 120, 240]); V = rng.choice([6, 12, 24])
    return dict(stem=f'A motor in a toy factory in {city} transfers {W} J of energy in {t} s from a {V} V supply. Calculate the current in the motor.', v=W / (V * t), unit='A', wrongs=[W / V, W * V / t, V * t / W], key=f'Q = W/V = {sf(W / V)} C (M1); I = Q/t = {sf(W / (V * t))} A (A1).')


R.mcqs('ch10-st1', 'C2', (1, 4), [
    ('A wire narrows to half its diameter in one section. In the narrow section, compared with the wide section, the current is', 'the same', ['halved', 'doubled', 'quadrupled'], 'Charge is conserved.'),
    ('In the narrow section of the same wire, the drift speed is', 'four times as large', ['twice as large', 'the same', 'a quarter'], 'A ∝ d².'),
    ('Which quantity is measured in J C⁻¹?', 'Potential difference', ['Current', 'Charge', 'Resistance'], 'V = W/q.'),
])


R.facts('ch10-st2', F(
    terms=[('resistance', 'the ratio of the potential difference across a component to the current through it, R = V/I, in ohms'),
           ('Ohm’s law', 'the current through a conductor is proportional to the potential difference across it, provided the temperature and other physical conditions are constant'),
           ('resistivity', 'the property of a material defined by ρ = RA/L, in Ω m'),
           ('ohmic conductor', 'a conductor that obeys Ohm’s law, with a straight-line I–V graph through the origin'),
           ('thermistor (NTC)', 'a semiconductor component whose resistance decreases as its temperature increases'),
           ('light-dependent resistor (LDR)', 'a component whose resistance decreases as the intensity of light falling on it increases')],
    facts=[('The I–V characteristic of a filament lamp is', 'a curve whose gradient decreases as V increases', ['a straight line through the origin', 'a curve whose gradient increases', 'a horizontal line'], 'Resistance increases with temperature.'),
           ('A wire’s length is doubled and its cross-sectional area is halved. Its resistance', 'increases by a factor of 4', ['doubles', 'is unchanged', 'halves'], 'R = ρL/A.'),
           ('Which component conducts significantly in only one direction?', 'A diode', ['A filament lamp', 'A fixed resistor', 'A thermistor'], 'Forward bias only.'),
           ('The unit of resistivity is', 'Ω m', ['Ω m⁻¹', 'Ω', 'Ω m²'], 'ρ = RA/L.'),
           ('A 12 V supply drives 0.40 A through a resistor. Its resistance is', '30 Ω', ['4.8 Ω', '0.033 Ω', '12 Ω'], 'R = V/I.')],
    why=[('Explain, in terms of electrons and ions, why the resistance of a metal wire increases with temperature.', 'Lattice ions vibrate with greater amplitude at higher temperature, so free electrons collide with them more often; their drift is impeded more, increasing resistance.'),
         ('Explain why the resistance of an NTC thermistor falls as its temperature rises.', 'In a semiconductor, heating frees more charge carriers (n increases greatly), which outweighs the increased lattice vibration, so the resistance decreases.'),
         ('Explain why a filament lamp does not obey Ohm’s law.', 'As current increases, the filament heats up and its resistance rises, so V/I is not constant and the I–V graph curves.')],
    contrast=[('resistance', 'resistivity', 'Resistance (Ω) is a property of a particular component, depending on its dimensions and temperature; resistivity (Ω m) is a property of the material, independent of the component’s size and shape.')],
    misc=[('Resistance is the gradient of an I–V graph.', 'R = V/I at a point; for a non-ohmic component this is not the same as the gradient. For an I–V graph, the gradient of a straight line through the origin is 1/R.'),
          ('All conductors obey Ohm’s law.', 'Only ohmic conductors at constant temperature do; filament lamps, diodes and thermistors do not.'),
          ('A thicker wire of the same material has a higher resistivity.', 'Resistivity depends only on the material and temperature; a thicker wire has lower resistance.')],
    evaluate=[('Ohm’s law is a fundamental law of physics.', ['it describes many metals accurately over wide ranges', 'it underpins circuit analysis'], ['it is an empirical relationship valid only under constant conditions', 'many components (diodes, lamps, semiconductors) do not obey it', 'R = V/I is a definition, not a law'], 'Ohm’s law is a useful empirical rule for certain materials, not a universal law like conservation of charge.')],
    extended=[('A student investigates a 1.00 m length of constantan wire of diameter 0.315 mm. She measures V = 2.40 V when I = 0.385 A. (a) Calculate the resistance. (b) Calculate the cross-sectional area and the resistivity. (c) The micrometer reading has an uncertainty of ±0.005 mm; calculate the percentage uncertainty in the area. (d) Suggest why the wire should not carry a large current for long.', '(a) 6.23 Ω; (b) A = 7.79 × 10⁻⁸ m², ρ = 4.86 × 10⁻⁷ Ω m; (c) 1.6 % in d → 3.2 % in A; (d) heating would raise the temperature and change the resistance.', 6)],
))

RHO = [('copper', 1.7e-8), ('aluminium', 2.8e-8), ('nichrome', 1.1e-6), ('constantan', 4.9e-7), ('tungsten', 5.6e-8), ('iron', 9.7e-8)]


@prob('ch10-st2', d=(1, 5), md=(1, 4), marks=2)
def p_resist(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        V = rng.choice([1.5, 3.0, 6.0, 9.0, 12, 230]); I = rng.choice([0.020, 0.15, 0.25, 0.50, 2.0, 4.0])
        return dict(stem=f'A component has a potential difference of {V} V across it and a current of {I} A through it. Calculate its resistance.', v=V / I, unit='Ω', wrongs=[V * I, I / V, V / I / 1000], key=f'R = V/I (M1) = {sf(V / I)} Ω (A1).')
    if k == 1:
        nm, rho = pick(rng, RHO); L = rng.choice([0.50, 1.0, 2.0, 5.0, 50]); d = rng.choice([0.20, 0.30, 0.50, 1.0, 2.0]) * 1e-3
        A = math.pi * (d / 2) ** 2; R_ = rho * L / A
        return dict(stem=f'Calculate the resistance of a {nm} wire (ρ = {sf(rho, 2)} Ω m) of length {L} m and diameter {d * 1000:g} mm.',
                    v=R_, unit='Ω', wrongs=[rho * L / (math.pi * d * d), rho * L / d, rho * A / L], key=f'A = πd²/4 = {sf(A)} m² (M1); R = ρL/A = {sf(R_)} Ω (A1).', marks=3)
    if k == 2:
        R_ = rng.choice([2.5, 5.0, 8.0, 12]); L = rng.choice([0.50, 1.0, 1.5]); d = rng.choice([0.20, 0.25, 0.30]) * 1e-3
        A = math.pi * (d / 2) ** 2
        return dict(stem=f'A wire of length {L} m and diameter {d * 1000:g} mm has a resistance of {R_} Ω. Calculate the resistivity of the material.',
                    v=R_ * A / L, unit='Ω m', wrongs=[R_ * L / A, R_ * math.pi * d * d / L, R_ * d / L], key=f'ρ = RA/L (M1) = {sf(R_ * A / L)} Ω m (A1).')
    if k == 3:
        fL = rng.choice([2, 3, 0.5]); fd = rng.choice([2, 0.5, 3])
        f = fL / fd ** 2
        return dict(stem=f'A wire is replaced by one of the same material that is {fL:g} times as long and has {fd:g} times the diameter. By what factor does the resistance change?', v=f, unit='', wrongs=[fL / fd, fL * fd ** 2, fL * fd], key=f'R ∝ L/d² (M1); factor = {fL:g}/{fd:g}² = {sf(f)} (A1).')
    P = rng.choice([40, 60, 100]); V = rng.choice([120, 230])
    Rh = V * V / P; Rc = Rh / rng.choice([10, 12, 15])
    return dict(stem=f'A {P} W, {V} V filament lamp has a resistance of {sf(Rc)} Ω when cold. Calculate its resistance at its operating temperature.', v=Rh, unit='Ω', wrongs=[Rc, V / P, P / V], key=f'R = V²/P (M1) = {sf(Rh)} Ω (A1); much larger than the cold value because resistance increases with temperature.')


R.mcqs('ch10-st2', 'C2', (1, 4), [
    ('The temperature of an NTC thermistor in a circuit with a fixed supply increases. The current through it', 'increases', ['decreases', 'is unchanged', 'falls to zero'], 'Resistance falls.'),
    ('On an I–V graph for a filament lamp, the resistance at a point is found from', 'V/I at that point', ['the gradient at that point', '1/gradient at that point', 'the area under the graph'], 'R = V/I.'),
    ('Two wires of the same material and length have diameters d and 2d. The ratio of their resistances R_d : R_2d is', '4 : 1', ['2 : 1', '1 : 4', '1 : 2'], 'R ∝ 1/d².'),
])


def _resistivity_spec(rng):
    rho = rng.uniform(4.6e-7, 5.2e-7); d = 0.315e-3; A = math.pi * d * d / 4
    Ls = [0.200, 0.400, 0.600, 0.800, 1.000, 1.200]
    Rs = [round(rho * L / A * rng.uniform(0.98, 1.02) + 0.10, 2) for L in Ls]
    return dict(intro='The resistance R of different lengths L of constantan wire of diameter 0.315 mm is measured with an ohmmeter. Theory: R = ρL/A (plus a small constant contact resistance).',
                xname='L', xunit='m', yname='R', yunit='Ω', xs=Ls, ys=Rs, xfmt=lambda x: f'{x:.3f}', yfmt=lambda y: f'{y:.2f}',
                plot_x=lambda x: x, plot_y=lambda y: y, plot_label='R (y) against L (x)', what='the resistivity ρ of constantan', what_short='ρ',
                gunit='Ω m⁻¹', deduce=lambda m_, b_: (m_ * math.pi * 0.315e-3 ** 2 / 4, 'Ω m', 'ρ = gradient × A'))


gradient_fit('ch10-st2', _resistivity_spec)


R.facts('ch10-st3', F(
    terms=[('Kirchhoff’s first law', 'the sum of currents entering a junction equals the sum of currents leaving it (conservation of charge)'),
           ('Kirchhoff’s second law', 'around any closed loop in a circuit, the sum of the emfs equals the sum of the potential differences (conservation of energy)'),
           ('series circuit', 'a circuit in which components are connected end to end so that the same current flows through each'),
           ('parallel circuit', 'a circuit in which components are connected across the same two points so that each has the same potential difference'),
           ('ideal ammeter', 'an ammeter with zero resistance, connected in series'),
           ('ideal voltmeter', 'a voltmeter with infinite resistance, connected in parallel')],
    facts=[('Three 6.0 Ω resistors are connected in parallel. The total resistance is', '2.0 Ω', ['18 Ω', '6.0 Ω', '0.50 Ω'], '1/R = 3/6.'),
           ('Adding another resistor in parallel to a circuit', 'decreases the total resistance', ['increases the total resistance', 'does not change the total resistance', 'decreases the total current'], 'More paths.'),
           ('Kirchhoff’s second law is a consequence of conservation of', 'energy', ['charge', 'momentum', 'mass'], 'Energy per unit charge around a loop.'),
           ('A 4.0 Ω and a 12 Ω resistor are connected in parallel. Their combined resistance is', '3.0 Ω', ['16 Ω', '8.0 Ω', '0.33 Ω'], '(4 × 12)/(4 + 12).'),
           ('Currents of 2.0 A and 3.5 A enter a junction. One wire leaves it. The current in that wire is', '5.5 A', ['1.5 A', '2.75 A', '7.0 A'], 'Kirchhoff’s first law.')],
    why=[('Explain why household appliances are connected in parallel rather than in series.', 'Each appliance gets the full mains voltage and can be switched independently; if one fails the others keep working, and total current is shared.'),
         ('Explain why an ideal voltmeter should have infinite resistance.', 'It is connected in parallel; to avoid drawing current and changing the circuit it is measuring, its resistance must be much larger than the component’s.'),
         ('Explain why the total resistance of resistors in parallel is less than the smallest individual resistance.', 'Each extra branch provides an additional path for current at the same pd, so the total current increases for the same voltage, i.e. the total resistance falls.')],
    contrast=[('resistors in series', 'resistors in parallel', 'In series the same current flows through each and the pds add (R = R₁ + R₂); in parallel the pd is the same and the currents add (1/R = 1/R₁ + 1/R₂).')],
    misc=[('Current is greater in the first resistor of a series circuit and then decreases.', 'In series the same current flows everywhere; the pd, not the current, is shared.'),
          ('Adding resistors in parallel increases total resistance just like in series.', 'Adding a parallel branch decreases the total resistance because it creates an extra path.'),
          ('A voltmeter should be connected in series to measure the voltage of a component.', 'A voltmeter measures pd between two points, so it is connected in parallel across the component.')],
    evaluate=[('Kirchhoff’s laws apply to all electrical circuits.', ['they follow from conservation of charge and energy', 'valid for DC and low-frequency AC circuits'], ['at high frequencies, changing magnetic fields mean the loop rule must include induced emfs', 'charge can build up in capacitors temporarily'], 'They apply very widely as statements of conservation laws, but need modification for high-frequency circuits with significant induction and radiation.')],
    extended=[('A 12 V battery of negligible internal resistance is connected to a 4.0 Ω resistor in series with a parallel combination of 6.0 Ω and 12 Ω resistors. (a) Calculate the total resistance. (b) Calculate the current from the battery. (c) Calculate the pd across the parallel combination and the current in each branch. (d) Verify Kirchhoff’s laws for the circuit.', '(a) 4.0 + 4.0 = 8.0 Ω; (b) 1.5 A; (c) 6.0 V; 1.0 A in 6 Ω, 0.50 A in 12 Ω; (d) junction: 1.5 = 1.0 + 0.5; loop: 12 = 6.0 + 6.0.', 6)],
))


@prob('ch10-st3', d=(1, 5), md=(1, 4), marks=2)
def p_circuits(rng, slot):
    k = rng.randrange(6)
    if k == 0:
        rs = rng.sample([2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10, 12, 15, 20], 3)
        return dict(stem=f'Resistors of {rs[0]:g} Ω, {rs[1]:g} Ω and {rs[2]:g} Ω are connected in series. Calculate the total resistance.', v=sum(rs), unit='Ω', wrongs=[1 / sum(1 / r for r in rs), sum(rs) / 3, max(rs)], key=f'R = R₁ + R₂ + R₃ = {sf(sum(rs))} Ω (A1).', marks=1)
    if k == 1:
        rs = rng.sample([2.0, 3.0, 4.0, 6.0, 8.0, 10, 12, 20], 3)
        Rp = 1 / sum(1 / r for r in rs)
        return dict(stem=f'Calculate the combined resistance of {rs[0]:g} Ω, {rs[1]:g} Ω and {rs[2]:g} Ω connected in parallel.', v=Rp, unit='Ω', wrongs=[sum(rs), sum(1 / r for r in rs), sum(rs) / 3], key=f'1/R = Σ1/Rᵢ = {sf(sum(1 / r for r in rs))} Ω⁻¹ (M1); R = {sf(Rp)} Ω (A1).')
    if k == 2:
        V = rng.choice([6.0, 9.0, 12, 24]); R1 = rng.choice([2.0, 3.0, 4.0, 5.0]); R2 = rng.choice([6.0, 10, 12]); R3 = rng.choice([12, 15, 20, 30])
        Rp = R2 * R3 / (R2 + R3); I = V / (R1 + Rp)
        return dict(stem=f'A {V} V battery (no internal resistance) is connected to a {R1:g} Ω resistor in series with a parallel pair of {R2:g} Ω and {R3:g} Ω. Calculate the current drawn from the battery.',
                    v=I, unit='A', wrongs=[V / (R1 + R2 + R3), V / R1, V / Rp], key=f'R_parallel = {sf(Rp)} Ω (M1); R_total = {sf(R1 + Rp)} Ω (M1); I = {sf(I)} A (A1).', marks=3)
    if k == 3:
        V = rng.choice([6.0, 9.0, 12]); R1 = rng.choice([2.0, 4.0, 5.0]); R2 = rng.choice([6.0, 10, 12]); R3 = rng.choice([12, 15, 20])
        Rp = R2 * R3 / (R2 + R3); I = V / (R1 + Rp); I2 = I * Rp / R2
        return dict(stem=f'In a circuit, a {V} V supply drives current through {R1:g} Ω in series with {R2:g} Ω and {R3:g} Ω in parallel. Calculate the current in the {R2:g} Ω resistor.',
                    v=I2, unit='A', wrongs=[I, I * R2 / (R2 + R3), V / R2], key=f'I_total = {sf(I)} A (M1); pd across parallel = {sf(I * Rp)} V (M1); I = {sf(I2)} A (A1).', marks=3)
    if k == 4:
        I1 = rng.choice([0.5, 1.2, 2.0, 2.5]); I2 = rng.choice([0.3, 0.8, 1.5]); I3 = rng.choice([0.4, 0.6, 1.0])
        return dict(stem=f'Currents of {I1} A and {I2} A flow into a junction. One wire leaves carrying {I3} A. Calculate the current in the only other wire at the junction.', v=I1 + I2 - I3, unit='A', wrongs=[I1 + I2 + I3, I1 - I2 + I3, (I1 + I2) / 2], key=f'Σ I_in = Σ I_out (M1); I = {I1} + {I2} − {I3} = {sf(I1 + I2 - I3)} A (A1).')
    E1 = rng.choice([6.0, 9.0, 12]); E2 = rng.choice([1.5, 3.0, 4.5]); R1 = rng.choice([2.0, 4.0, 6.0]); R2 = rng.choice([1.0, 2.0, 3.0])
    I = (E1 - E2) / (R1 + R2)
    return dict(stem=f'In a single loop, a {E1} V cell and a {E2} V cell are connected in opposition, with resistors of {R1:g} Ω and {R2:g} Ω (no internal resistance). Use Kirchhoff’s second law to find the current.', v=I, unit='A', wrongs=[(E1 + E2) / (R1 + R2), E1 / (R1 + R2), (E1 - E2) / R1], key=f'ΣE = ΣIR: {E1} − {E2} = I({R1:g} + {R2:g}) (M1); I = {sf(I)} A (A1).')


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step')
def c4_two_loop(rng, slot):
    E1 = rng.choice([12.0, 9.0]); E2 = rng.choice([6.0, 3.0]); R1 = rng.choice([2.0, 4.0]); R2 = rng.choice([3.0, 6.0]); R3 = rng.choice([4.0, 6.0, 12.0])
    # nodes: E1-R1 branch and E2-R2 branch both feed R3 (parallel branches). Solve for V across R3.
    V = (E1 / R1 + E2 / R2) / (1 / R1 + 1 / R2 + 1 / R3)
    I1 = (E1 - V) / R1; I2 = (E2 - V) / R2; I3 = V / R3
    return num(f'Two cells, E₁ = {E1} V with a series resistor of {R1:g} Ω and E₂ = {E2} V with a series resistor of {R2:g} Ω, are connected in parallel (positive terminals joined) across a {R3:g} Ω load. Internal resistances are negligible. (a) Apply Kirchhoff’s first law at the junction. (b) Write Kirchhoff’s second law for two independent loops. (c) Solve for the current in each branch. (d) State whether cell E₂ is being charged or discharged, and explain. (e) Calculate the power dissipated in the load.',
               f'(c) I₁ = {sf(I1)} A, I₂ = {sf(I2)} A, I₃ = {sf(I3)} A; (d) {"charged – current flows into its positive terminal" if I2 < 0 else "discharged – it supplies current to the load"}; (e) {sf(I3 * I3 * R3)} W',
               f'(a) I₁ + I₂ = I₃ (A1). (b) E₁ = I₁R₁ + I₃R₃; E₂ = I₂R₂ + I₃R₃ (M1 M1). (c) solving (A1 A1). (d) sign of I₂ interpreted (R1). (e) P = I²R (A1).', 7, 'multi_step')


R.mcqs('ch10-st3', 'C2', (1, 4), [
    ('A lamp in a parallel branch of a circuit is removed. The current from the supply', 'decreases', ['increases', 'stays the same', 'becomes zero'], 'Fewer paths: total resistance increases.'),
    ('Two identical lamps are connected in series to a battery. A third identical lamp is connected in parallel with one of them. The brightness of the lamp that is not in the parallel pair', 'increases', ['decreases', 'stays the same', 'goes out'], 'Total resistance falls, so current through it rises.'),
    ('A voltmeter of resistance 10 kΩ is connected across a 10 kΩ resistor in a circuit. The reading will be', 'lower than the true pd without the meter', ['exactly the true pd', 'higher than the true pd', 'zero'], 'The meter draws current, lowering the effective resistance.'),
])


R.facts('ch10-st4', F(
    terms=[('electrical power', 'the rate of energy transfer in a circuit component, P = VI = I²R = V²/R'),
           ('kilowatt-hour', 'the energy transferred when a 1 kW appliance operates for 1 hour, 3.6 × 10⁶ J'),
           ('Joule heating', 'the dissipation of electrical energy as internal energy in a resistor when current flows through it'),
           ('power rating', 'the power an appliance transfers when operated at its stated voltage')],
    facts=[('A 230 V kettle draws a current of 10 A. Its power is', '2.3 kW', ['23 W', '23 kW', '240 W'], 'P = VI.'),
           ('A current of 2.0 A flows through a 5.0 Ω resistor. The power dissipated is', '20 W', ['10 W', '2.5 W', '40 W'], 'P = I²R.'),
           ('A 60 W lamp is switched on for 5.0 hours. The energy transferred is', '0.30 kWh', ['300 kWh', '12 kWh', '0.012 kWh'], 'E = Pt.'),
           ('Electricity is transmitted at high voltage because', 'for the same power the current is smaller, so I²R losses are reduced', ['high voltage travels faster', 'cables have lower resistance at high voltage', 'it is safer'], 'P_loss = I²R.'),
           ('If the pd across a fixed resistor is doubled, the power dissipated', 'quadruples', ['doubles', 'halves', 'is unchanged'], 'P = V²/R.')],
    why=[('Explain why the power dissipated in transmission cables is reduced by transmitting at high voltage.', 'For a given power P = VI, a higher voltage means a smaller current; cable losses are I²R, so they fall with the square of the current.'),
         ('Explain why a 100 W lamp has a smaller resistance than a 40 W lamp designed for the same voltage.', 'P = V²/R at fixed V, so a higher power rating requires a lower resistance.'),
         ('Explain why a fuse is placed in the live wire of an appliance.', 'If a fault causes a large current, the fuse wire melts and breaks the circuit, disconnecting the live supply so the appliance is no longer at a dangerous potential.')],
    contrast=[('power', 'energy', 'Power is the rate of energy transfer (W = J s⁻¹); energy is the total transferred (J or kWh). A high-power appliance used briefly may transfer less energy than a low-power one left on for a long time.')],
    misc=[('Appliances with a higher voltage rating always use more power.', 'Power depends on both V and I (P = VI); a high-voltage device with a small current can have low power.'),
          ('A kilowatt-hour is a unit of power.', 'It is a unit of energy: 1 kW × 3600 s = 3.6 MJ.'),
          ('The power dissipated in a resistor always increases with its resistance.', 'With fixed current P = I²R increases with R, but with fixed voltage P = V²/R decreases as R increases.')],
    evaluate=[('Smart meters will significantly reduce household electricity consumption.', ['real-time feedback makes users aware of waste', 'enables time-of-use tariffs that shift demand'], ['studies show savings of only a few per cent', 'privacy and cost concerns', 'behaviour change fades over time'], 'Smart meters help, mainly by enabling flexible tariffs and grid management, but on their own produce only modest reductions.')],
    extended=[('A power station delivers 50 MW to a town through cables of total resistance 4.0 Ω. (a) Calculate the current and the power lost if the transmission voltage is 25 kV. (b) Repeat for 400 kV. (c) Calculate the percentage of the power lost in each case. (d) Explain why transformers make high-voltage transmission practical.', '(a) I = 2000 A, P_loss = I²R = 16 MW; (b) I = 125 A, P_loss = 62.5 kW; (c) 32 % and 0.13 %; (d) transformers step voltage up for transmission and down for safe use with very little energy loss.', 6)],
))


@prob('ch10-st4', d=(1, 5), md=(1, 4), marks=2)
def p_power_el(rng, slot):
    k = rng.randrange(5)
    city = rng.choice(CITIES)
    if k == 0:
        V = rng.choice([12, 120, 230, 240]); I = rng.choice([0.25, 0.50, 2.0, 5.0, 8.0, 13])
        return dict(stem=f'An appliance connected to a {V} V supply draws a current of {I} A. Calculate its power.', v=V * I, unit='W', wrongs=[V / I, I * I * V, V * V / I], key=f'P = VI (M1) = {sf(V * I)} W (A1).')
    if k == 1:
        I = rng.choice([0.50, 1.5, 2.0, 3.0]); R_ = rng.choice([4.0, 8.0, 12, 22, 47])
        return dict(stem=f'A current of {I} A flows through a {R_:g} Ω resistor. Calculate the power dissipated.', v=I * I * R_, unit='W', wrongs=[I * R_, I * I / R_, I * R_ * R_], key=f'P = I²R (M1) = {sf(I * I * R_)} W (A1).')
    if k == 2:
        P = rng.choice([40, 60, 100, 1000, 2000]); V = rng.choice([120, 230])
        return dict(stem=f'A {P} W heater is designed for a {V} V supply. Calculate its resistance when operating.', v=V * V / P, unit='Ω', wrongs=[P / V, V / P, P / V ** 2 * 1000], key=f'R = V²/P (M1) = {sf(V * V / P)} Ω (A1).')
    if k == 3:
        P = rng.choice([1.5, 2.0, 2.5, 3.0, 8.0]); h = rng.choice([0.5, 1.0, 2.0, 3.0]); d = rng.choice([30, 60, 90]); price = rng.choice([0.15, 0.22, 0.30])
        E_ = P * h * d
        return dict(stem=f'A {P} kW appliance in a home in {city} is used for {h} hours a day for {d} days. Calculate the energy used in kWh.', v=E_, unit='kWh', wrongs=[P * h, P * d, E_ * 3.6e6 / 1e6], key=f'E = Pt = {P} kW × {h * d:g} h (M1) = {sf(E_)} kWh, costing {sf(E_ * price)} at {price} per kWh (A1).')
    P = rng.choice([20e6, 50e6, 100e6]); V = rng.choice([25e3, 132e3, 400e3]); R_ = rng.choice([2.0, 4.0, 5.0])
    I = P / V
    return dict(stem=f'A power station sends {sf(P / 1e6, 2)} MW along cables of total resistance {R_:g} Ω at {sf(V / 1e3, 3)} kV. Calculate the power lost as heat in the cables.', v=I * I * R_, unit='W', wrongs=[V * V / R_, I * R_, P * R_ / V], key=f'I = P/V = {sf(I)} A (M1); P_loss = I²R = {sf(I * I * R_)} W (A1).', marks=3)


R.mcqs('ch10-st4', 'C2', (1, 4), [
    ('Two lamps rated 60 W and 100 W at 230 V are connected in series to a 230 V supply. Which is brighter?', 'The 60 W lamp', ['The 100 W lamp', 'Both equally bright', 'Neither lights'], 'Same current; the 60 W lamp has the larger resistance so I²R is larger.'),
    ('Two resistors R and 2R are connected in parallel to a supply. The ratio of power in R to power in 2R is', '2 : 1', ['1 : 2', '1 : 4', '4 : 1'], 'P = V²/R.'),
    ('The unit kW h is equivalent to', '3.6 × 10⁶ J', ['1000 J', '3600 J', '3.6 × 10³ W'], '1000 W × 3600 s.'),
])


R.facts('ch10-st5', F(
    terms=[('electromotive force (emf)', 'the work done per unit charge by a source in moving charge around a complete circuit, ε, in volts'),
           ('internal resistance', 'the resistance r of a source itself, which causes energy dissipation inside the source and a drop in terminal pd when current flows'),
           ('terminal potential difference', 'the pd across the terminals of a source, V = ε − Ir'),
           ('lost volts', 'the pd Ir across the internal resistance of a source when current I flows'),
           ('potential divider', 'a series arrangement of resistors that splits the supply pd in proportion to their resistances'),
           ('potentiometer (variable potential divider)', 'a resistor with a sliding contact used to give a continuously variable output pd')],
    facts=[('A cell of emf 1.5 V and internal resistance 0.50 Ω supplies 0.40 A. Its terminal pd is', '1.3 V', ['1.5 V', '1.7 V', '0.20 V'], 'V = ε − Ir.'),
           ('The emf of a cell can be measured as', 'the terminal pd when no current flows', ['the terminal pd at maximum current', 'the lost volts', 'the current times the external resistance'], 'V = ε when I = 0.'),
           ('A graph of terminal pd V against current I for a cell is a straight line. Its gradient is', '−r', ['ε', 'r', '1/r'], 'V = ε − Ir.'),
           ('In a potential divider with resistors of 2 kΩ and 8 kΩ across 10 V, the pd across the 8 kΩ resistor is', '8.0 V', ['2.0 V', '5.0 V', '1.25 V'], 'V_out = V_in × R₂/(R₁ + R₂).'),
           ('The maximum current a cell can supply (short circuit) is', 'ε/r', ['εr', 'r/ε', 'zero'], 'R_ext = 0.')],
    why=[('Explain why the headlights of a car dim when the starter motor is operated.', 'The starter motor draws a very large current; the lost volts Ir across the battery’s internal resistance become large, so the terminal pd available to the lamps falls.'),
         ('Explain how a potential divider with a thermistor can be used as a temperature sensor.', 'As temperature rises the thermistor’s resistance falls, so its share of the supply pd falls and the pd across the fixed resistor rises; this output pd can trigger a switch.'),
         ('Explain why a high-voltage supply for school experiments has a very large internal resistance.', 'A large internal resistance limits the maximum (short-circuit) current to a safe value, protecting students.')],
    contrast=[('emf', 'terminal potential difference', 'EMF is the energy per unit charge supplied by the source; terminal pd is the energy per unit charge delivered to the external circuit, which is less than the emf by the lost volts Ir.')],
    misc=[('The emf of a cell is the same as its terminal pd in all circumstances.', 'They are equal only when no current flows; otherwise V = ε − Ir is smaller.'),
          ('Connecting a lower external resistance always gives more power to the load.', 'Maximum power is delivered to the load when its resistance equals the internal resistance; below that the power decreases.'),
          ('Internal resistance is a separate resistor inside the battery case.', 'It represents the resistance of the cell’s materials (electrolyte, electrodes), modelled as a series resistor.')],
    evaluate=[('The internal resistance of a battery is a design flaw that manufacturers should eliminate.', ['it wastes energy as heat and reduces terminal pd'], ['it is intrinsic to the electrochemistry and cannot be zero', 'a small internal resistance limits short-circuit currents (safety)', 'battery design balances energy density, cost and r'], 'Internal resistance can be reduced but not eliminated; it is a trade-off, and sometimes a safety feature.')],
    extended=[('A student measures the terminal pd V of a battery for different currents I: (0.20 A, 5.62 V), (0.50 A, 5.35 V), (0.80 A, 5.08 V), (1.10 A, 4.81 V). (a) Plot or analyse these data to determine the emf and internal resistance. (b) Calculate the power lost inside the battery at 1.10 A. (c) Calculate the external resistance at which the power delivered to the load is maximum and the value of this power. (d) Explain why the readings should be taken quickly.', '(a) gradient −0.90 Ω, so r = 0.90 Ω; intercept ε = 5.80 V; (b) I²r = 1.09 W; (c) R = r = 0.90 Ω, P = ε²/(4r) = 9.3 W; (d) the battery and resistors heat up, changing r and R.', 6)],
))


@prob('ch10-st5', d=(1, 5), md=(1, 4), marks=2)
def p_emf(rng, slot):
    k = rng.randrange(6)
    if k == 0:
        e = rng.choice([1.5, 4.5, 6.0, 9.0, 12]); r = rng.choice([0.2, 0.5, 0.8, 1.0, 2.0]); I = rng.choice([0.25, 0.50, 1.0, 2.0])
        if I * r >= e:
            return None
        return dict(stem=f'A battery of emf {e} V and internal resistance {r} Ω supplies a current of {I} A. Calculate the terminal potential difference.', v=e - I * r, unit='V', wrongs=[e + I * r, e, I * r], key=f'V = ε − Ir (M1) = {e} − {I} × {r} = {sf(e - I * r)} V (A1).')
    if k == 1:
        e = rng.choice([1.5, 6.0, 9.0, 12]); r = rng.choice([0.5, 1.0, 1.5, 2.0]); R_ = rng.choice([2.0, 4.0, 5.0, 10, 20])
        return dict(stem=f'A cell of emf {e} V and internal resistance {r} Ω is connected to a {R_:g} Ω resistor. Calculate the current.', v=e / (R_ + r), unit='A', wrongs=[e / R_, e / r, e / (R_ - r) if R_ > r else e / R_ * 2], key=f'I = ε/(R + r) (M1) = {sf(e / (R_ + r))} A (A1).')
    if k == 2:
        e = rng.choice([1.5, 3.0, 6.0, 9.0]); V = e * rng.choice([0.80, 0.85, 0.90, 0.95]); I = rng.choice([0.20, 0.50, 1.0])
        return dict(stem=f'The terminal pd of a battery of emf {e} V falls to {sf(V)} V when it delivers {I} A. Calculate its internal resistance.', v=(e - V) / I, unit='Ω', wrongs=[V / I, e / I, (e - V) * I], key=f'r = (ε − V)/I (M1) = {sf((e - V) / I)} Ω (A1).')
    if k == 3:
        Vin = rng.choice([5.0, 6.0, 9.0, 12]); R1 = rng.choice([1.0, 2.2, 4.7, 10]); R2 = rng.choice([1.0, 3.3, 4.7, 6.8, 15])
        return dict(stem=f'A potential divider consists of a {R1} kΩ resistor in series with a {R2} kΩ resistor across a {Vin} V supply. Calculate the output pd across the {R2} kΩ resistor.', v=Vin * R2 / (R1 + R2), unit='V', wrongs=[Vin * R1 / (R1 + R2), Vin * R2 / R1, Vin / 2], key=f'V_out = V_in R₂/(R₁ + R₂) (M1) = {sf(Vin * R2 / (R1 + R2))} V (A1).')
    if k == 4:
        Vin = rng.choice([6.0, 9.0, 12]); R1 = rng.choice([2.0, 4.0, 5.0]); Rt = rng.choice([1.0, 2.5, 8.0, 12]); cond = {1.0: 'hot', 2.5: 'warm', 8.0: 'cool', 12: 'cold'}[Rt]
        return dict(stem=f'An NTC thermistor and a {R1} kΩ fixed resistor form a potential divider across {Vin} V. When the thermistor is {cond} its resistance is {Rt} kΩ. Calculate the pd across the fixed resistor.', v=Vin * R1 / (R1 + Rt), unit='V', wrongs=[Vin * Rt / (R1 + Rt), Vin * R1 / Rt, Vin], key=f'V = V_in × {R1}/({R1} + {Rt}) (M1) = {sf(Vin * R1 / (R1 + Rt))} V (A1).')
    e = rng.choice([6.0, 9.0, 12]); r = rng.choice([0.5, 1.0, 2.0])
    return dict(stem=f'A battery has emf {e} V and internal resistance {r} Ω. Calculate the maximum power it can deliver to an external resistor.', v=e * e / (4 * r), unit='W', wrongs=[e * e / r, e * e / (2 * r), e / r], key=f'Maximum when R = r (M1); P = ε²/(4r) = {sf(e * e / (4 * r))} W (A1).', marks=3)


R.mcqs('ch10-st5', 'C2', (1, 4), [
    ('The external resistance connected to a cell with internal resistance is decreased. The terminal pd', 'decreases', ['increases', 'stays the same', 'equals the emf'], 'Larger I, larger Ir.'),
    ('In a light-sensing potential divider, an LDR is in series with a fixed resistor. As the light gets brighter, the pd across the LDR', 'decreases', ['increases', 'stays the same', 'equals the supply pd'], 'LDR resistance falls.'),
    ('A voltmeter connected directly across a battery with no other circuit reads', 'the emf (approximately)', ['zero', 'the lost volts', 'half the emf'], 'Negligible current.'),
])


def _emf_spec(rng):
    e = rng.uniform(1.45, 1.60); r = rng.uniform(0.5, 1.5)
    Is = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
    Vs = [round(e - I * r + rng.uniform(-0.01, 0.01), 2) for I in Is]
    return dict(intro='A cell is connected to a variable resistor, an ammeter and a voltmeter across its terminals. The terminal pd V is recorded for different currents I. Theory: V = ε − Ir.',
                xname='I', xunit='A', yname='V', yunit='V', xs=Is, ys=Vs, xfmt=lambda x: f'{x:.2f}', yfmt=lambda y: f'{y:.2f}',
                plot_x=lambda x: x, plot_y=lambda y: y, plot_label='V (y) against I (x)', what='the internal resistance r of the cell', what_short='r',
                gunit='V A⁻¹', deduce=lambda m_, b_: (-m_, 'Ω', 'r = −gradient'))


gradient_fit('ch10-st5', _emf_spec)


# =============================================================================================
# ch11 C.1 Simple harmonic motion
# =============================================================================================
R.facts('ch11-st1', F(
    terms=[('simple harmonic motion', 'oscillatory motion in which the acceleration is proportional to the displacement from a fixed equilibrium point and always directed towards it: a = −ω²x'),
           ('restoring force', 'a force that acts to return an oscillating object to its equilibrium position'),
           ('equilibrium position', 'the position at which the resultant force on the oscillating object is zero'),
           ('displacement (oscillation)', 'the distance and direction of the object from its equilibrium position'),
           ('isochronous oscillation', 'an oscillation whose period does not depend on its amplitude, a key feature of SHM')],
    facts=[('Which condition defines simple harmonic motion?', 'a ∝ −x', ['a ∝ x', 'a ∝ x²', 'a is constant'], 'Acceleration proportional and opposite to displacement.'),
           ('At the equilibrium position of an SHM oscillator, the acceleration is', 'zero', ['maximum', 'equal to g', 'equal to ω'], 'x = 0.'),
           ('A ball bouncing vertically on a hard floor (ignoring losses) is NOT in SHM because', 'its acceleration is constant (g) between bounces, not proportional to displacement', ['its period is too short', 'it has no equilibrium position', 'its amplitude decreases'], 'a = g except during contact.'),
           ('Which of the following is a good example of approximate SHM?', 'A pendulum swinging through a small angle', ['A ball rolling in a V-shaped trough', 'A bouncing ball', 'A car moving in a circle'], 'Small angle approximation.'),
           ('For a mass on a spring obeying Hooke’s law, the restoring force is', '−kx', ['kx²', 'mg', '−mg/x'], 'Hooke’s law.')],
    why=[('Explain why a mass on a spring obeying Hooke’s law performs simple harmonic motion.', 'The restoring force F = −kx is proportional to displacement and opposite to it; by Newton’s second law a = −(k/m)x, which is the defining equation of SHM with ω² = k/m.'),
         ('Explain why a simple pendulum only approximates SHM for small amplitudes.', 'The restoring force is −mg sin θ; only for small θ is sin θ ≈ θ ≈ x/L, giving a = −(g/L)x. For large angles the force is no longer proportional to displacement.'),
         ('Explain why the period of an SHM oscillator does not depend on the amplitude.', 'In SHM a larger displacement gives a proportionally larger restoring acceleration; the object travels further but faster, and the time per cycle depends only on ω.')],
    contrast=[('simple harmonic motion', 'other periodic motion', 'All periodic motion repeats at regular intervals, but in SHM the acceleration must be proportional to displacement and directed towards equilibrium, giving sinusoidal motion and an amplitude-independent period.')],
    misc=[('In SHM the velocity is greatest at the extremes of the motion.', 'The velocity is zero at the extremes (turning points) and maximum at equilibrium.'),
          ('All oscillations are simple harmonic.', 'Only oscillations with a ∝ −x are SHM; a bouncing ball or large-angle pendulum is periodic but not SHM.'),
          ('The restoring force in SHM is constant.', 'It is proportional to displacement, so it varies from zero at equilibrium to maximum at the amplitude.')],
    evaluate=[('Many real oscillating systems can be treated as simple harmonic.', ['small oscillations about a stable equilibrium are approximately SHM (Taylor expansion)', 'pendulums, springs, molecules in solids, tuning forks'], ['large amplitudes introduce non-linearity', 'damping and driving forces modify the motion', 'some systems (bouncing balls) are never SHM'], 'SHM is an excellent first model for small oscillations near equilibrium, but real systems require damping and non-linear terms at larger amplitudes.')],
    extended=[('A 0.40 kg mass hangs at rest on a spring, extending it by 0.098 m. It is pulled down a further 0.050 m and released. (a) Calculate the spring constant. (b) Show that the motion is SHM and calculate ω. (c) Calculate the maximum acceleration. (d) State the period and explain why it would be the same for a 0.030 m pull.', '(a) k = mg/x = 40.0 N m⁻¹; (b) F = −kx about equilibrium, so a = −(k/m)x; ω = √(40/0.40) = 10.0 rad s⁻¹; (c) a_max = ω²A = 5.0 m s⁻²; (d) T = 0.628 s; period is independent of amplitude in SHM.', 6)],
))


@prob('ch11-st1', d=(1, 4), md=(1, 4), marks=2)
def p_shm_cond(rng, slot):
    k = rng.randrange(4)
    if k == 0:
        w = rng.choice([2.0, 3.0, 5.0, 8.0, 10, 12]); x = rng.choice([0.010, 0.020, 0.040, 0.050, 0.10])
        return dict(stem=f'An object performs SHM with angular frequency {w} rad s⁻¹. Calculate the magnitude of its acceleration when its displacement is {x} m.', v=w * w * x, unit='m s⁻²', wrongs=[w * x, w * w / x, w * x * x], key=f'a = −ω²x (M1); |a| = {w}² × {x} = {sf(w * w * x)} m s⁻² (A1).')
    if k == 1:
        kk = rng.choice([20, 40, 80, 150, 250]); m = rng.choice([0.10, 0.20, 0.50, 1.0])
        return dict(stem=f'A {m} kg mass is attached to a spring of spring constant {kk} N m⁻¹. Calculate the angular frequency of its oscillations.', v=math.sqrt(kk / m), unit='rad s⁻¹', wrongs=[kk / m, math.sqrt(m / kk), math.sqrt(kk / m) / (2 * math.pi)], key=f'ω = √(k/m) (M1) = {sf(math.sqrt(kk / m))} rad s⁻¹ (A1).')
    if k == 2:
        a = rng.choice([2.0, 4.5, 8.0, 12]); x = rng.choice([0.020, 0.030, 0.050])
        return dict(stem=f'An oscillator has an acceleration of {a} m s⁻² towards equilibrium when its displacement is {x} m. Calculate the angular frequency.', v=math.sqrt(a / x), unit='rad s⁻¹', wrongs=[a / x, math.sqrt(a * x), math.sqrt(x / a)], key=f'ω² = a/x (M1); ω = {sf(math.sqrt(a / x))} rad s⁻¹ (A1).')
    m = rng.choice([0.20, 0.30, 0.50]); x0 = rng.choice([0.040, 0.050, 0.080])
    kk = m * g0 / x0
    return dict(stem=f'A {m} kg mass hung on a spring stretches it by {x0} m at equilibrium. Calculate the spring constant.', v=kk, unit='N m⁻¹', wrongs=[m / x0, m * g0 * x0, x0 / (m * g0)], key=f'k = mg/x (M1) = {sf(kk)} N m⁻¹ (A1).')


R.mcqs('ch11-st1', 'C2', (1, 4), [
    ('Which graph is a straight line through the origin with negative gradient for an SHM oscillator?', 'Acceleration against displacement', ['Velocity against displacement', 'Displacement against time', 'Kinetic energy against displacement'], 'a = −ω²x.'),
    ('An oscillator in SHM is at its maximum positive displacement. Its acceleration is', 'maximum and negative', ['zero', 'maximum and positive', 'equal to its velocity'], 'a = −ω²A.'),
    ('A ball rolls back and forth in a curved bowl of large radius. Its motion is approximately SHM because', 'for small displacements the restoring force is proportional to displacement', ['the bowl is frictionless', 'the ball rolls', 'gravity is constant'], 'Small-angle approximation.'),
])


R.facts('ch11-st2', F(
    terms=[('period', 'the time for one complete oscillation, T'),
           ('frequency', 'the number of oscillations per unit time, f = 1/T, in hertz'),
           ('amplitude', 'the maximum displacement from the equilibrium position'),
           ('angular frequency', 'the quantity ω = 2πf = 2π/T, in rad s⁻¹'),
           ('phase difference', 'the fraction of a cycle (expressed as an angle in radians) by which one oscillation leads or lags another'),
           ('simple pendulum', 'a point mass on a light inextensible string; for small oscillations T = 2π√(L/g)')],
    facts=[('The period of a mass–spring system is', 'T = 2π√(m/k)', ['T = 2π√(k/m)', 'T = 2π√(L/g)', 'T = 2πmk'], 'From ω² = k/m.'),
           ('A pendulum’s length is quadrupled. Its period', 'doubles', ['quadruples', 'halves', 'is unchanged'], 'T ∝ √L.'),
           ('The period of a simple pendulum is independent of', 'the mass of the bob', ['its length', 'the gravitational field strength', 'the planet it is on'], 'T = 2π√(L/g).'),
           ('Two oscillators are in antiphase. Their phase difference is', 'π rad', ['0', 'π/2 rad', '2π rad'], 'Half a cycle.'),
           ('An oscillator has a frequency of 4.0 Hz. Its period is', '0.25 s', ['4.0 s', '25 s', '0.40 s'], 'T = 1/f.')],
    why=[('Explain why a pendulum clock taken to the top of a high mountain runs slow.', 'g is slightly smaller further from Earth’s centre; T = 2π√(L/g) increases, so the clock completes fewer swings per hour and loses time.'),
         ('Explain why timing 20 oscillations is better than timing one oscillation when measuring a period.', 'The human reaction-time uncertainty (~0.2 s) is a fixed absolute error; spreading it over 20 periods reduces the percentage uncertainty in T by a factor of 20.'),
         ('Explain why the period of a mass–spring system does not depend on g, while a pendulum’s does.', 'For the spring the restoring force comes from the spring (k), and gravity only shifts the equilibrium position; for the pendulum the restoring force is a component of the weight, so g appears in T.')],
    contrast=[('the mass–spring system', 'the simple pendulum', 'For a mass on a spring T = 2π√(m/k), depending on mass and stiffness but not g; for a simple pendulum T = 2π√(L/g), depending on length and g but not on mass.')],
    misc=[('A heavier pendulum bob swings more slowly.', 'The period of a simple pendulum is independent of mass: both the restoring force and the inertia scale with m.'),
          ('Doubling the amplitude of an SHM oscillator doubles its period.', 'In SHM the period is independent of amplitude.'),
          ('Phase difference is measured in seconds.', 'It is an angle (rad or degrees) or a fraction of a cycle; a time difference Δt corresponds to a phase difference 2πΔt/T.')],
    evaluate=[('Pendulums are no longer useful in science now that atomic clocks exist.', ['atomic clocks are far more accurate'], ['pendulums are still used to measure g and teach SHM', 'Foucault pendulums demonstrate Earth’s rotation', 'gravimeters and seismometers use pendulum principles'], 'Pendulums are obsolete for precise timekeeping but remain valuable for measurement, demonstration and as models of oscillation.')],
    extended=[('A student measures the time for 20 swings of a pendulum of length 0.800 m as 35.9 s, with a reaction-time uncertainty of ±0.2 s and length uncertainty ±0.002 m. (a) Calculate T and its uncertainty. (b) Calculate g. (c) Determine the percentage uncertainty in g. (d) Suggest one systematic error and how to reduce it.', '(a) T = 1.795 ± 0.010 s; (b) g = 4π²L/T² = 9.80 m s⁻²; (c) %g = %L + 2 × %T = 0.25 + 1.1 = 1.4 %; (d) length measured to the top of the bob rather than its centre – measure to the centre or plot T² against L and use the gradient.', 6)],
))


@prob('ch11-st2', d=(1, 5), md=(1, 4), marks=2)
def p_period(rng, slot):
    k = rng.randrange(6)
    city = rng.choice(CITIES)
    if k == 0:
        m = rng.choice([0.10, 0.25, 0.50, 1.0, 2.0]); kk = rng.choice([10, 25, 40, 100, 250])
        return dict(stem=f'Calculate the period of oscillation of a {m} kg mass on a spring of spring constant {kk} N m⁻¹.', v=2 * math.pi * math.sqrt(m / kk), unit='s', wrongs=[2 * math.pi * math.sqrt(kk / m), math.sqrt(m / kk), 2 * math.pi * m / kk], key=f'T = 2π√(m/k) (M1) = {sf(2 * math.pi * math.sqrt(m / kk))} s (A1).')
    if k == 1:
        L = rng.choice([0.25, 0.50, 0.80, 1.0, 1.5, 2.5, 10, 67])
        return dict(stem=f'Calculate the period of a simple pendulum of length {L} m on Earth (g = 9.81 m s⁻²).', v=2 * math.pi * math.sqrt(L / g0), unit='s', wrongs=[2 * math.pi * math.sqrt(g0 / L), math.sqrt(L / g0), 2 * math.pi * L / g0], key=f'T = 2π√(L/g) (M1) = {sf(2 * math.pi * math.sqrt(L / g0))} s (A1).')
    if k == 2:
        T = rng.choice([1.0, 1.5, 2.0, 3.0])
        return dict(stem=f'A grandfather clock in {city} needs a pendulum with a period of {T} s. Calculate the required length.', v=g0 * T * T / (4 * math.pi ** 2), unit='m', wrongs=[g0 * T / (2 * math.pi), g0 * T * T / (2 * math.pi), T * T / (4 * math.pi ** 2)], key=f'L = gT²/4π² (M1) = {sf(g0 * T * T / (4 * math.pi ** 2))} m (A1).')
    if k == 3:
        L = rng.choice([0.50, 1.0, 1.5]); pl = pick(rng, [('the Moon', 1.62), ('Mars', 3.71), ('Jupiter', 24.8), ('Venus', 8.87)])
        return dict(stem=f'A pendulum of length {L} m is taken to {pl[0]}, where g = {pl[1]} m s⁻². Calculate its period there.', v=2 * math.pi * math.sqrt(L / pl[1]), unit='s', wrongs=[2 * math.pi * math.sqrt(L / g0), 2 * math.pi * math.sqrt(pl[1] / L), 2 * math.pi * math.sqrt(L / g0) * pl[1] / g0], key=f'T = 2π√(L/g) = 2π√({L}/{pl[1]}) (M1) = {sf(2 * math.pi * math.sqrt(L / pl[1]))} s (A1).')
    if k == 4:
        n = rng.choice([10, 20, 25]); t = rng.choice([8.4, 12.6, 15.8, 22.5, 31.0])
        T = t / n
        return dict(stem=f'{n} oscillations of a mass–spring system take {t} s. Calculate the frequency of the oscillation.', v=1 / T, unit='Hz', wrongs=[T, n * t, 2 * math.pi / T], key=f'T = {t}/{n} = {sf(T)} s (M1); f = 1/T = {sf(1 / T)} Hz (A1).')
    dt = rng.choice([0.05, 0.10, 0.125, 0.20, 0.25]); T = rng.choice([0.40, 0.50, 0.80, 1.0])
    if dt >= T:
        return None
    phi = 2 * math.pi * dt / T
    return dict(stem=f'Two pendulums of period {T} s swing with one reaching its maximum displacement {dt} s after the other. Calculate the phase difference in radians.', v=phi, unit='rad', wrongs=[dt / T, 2 * math.pi * T / dt, 360 * dt / T], key=f'Δφ = 2πΔt/T (M1) = {sf(phi)} rad (A1).')


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step')
def c4_springs(rng, slot):
    m = rng.choice([0.20, 0.30, 0.50]); k1 = rng.choice([20, 30, 40]); k2 = rng.choice([20, 30, 60])
    ks = 1 / (1 / k1 + 1 / k2); kp = k1 + k2
    Ts, Tp = 2 * math.pi * math.sqrt(m / ks), 2 * math.pi * math.sqrt(m / kp)
    return num(f'A {m} kg mass is suspended from two springs of spring constants {k1} N m⁻¹ and {k2} N m⁻¹. (a) Show that the effective spring constant is {sf(ks)} N m⁻¹ when the springs are in series and {sf(kp)} N m⁻¹ when in parallel. (b) Calculate the period in each arrangement. (c) Calculate the ratio of the periods. (d) Explain why the period would be the same on the Moon.',
               f'(a) series 1/k = 1/k₁ + 1/k₂ = {sf(ks)} N m⁻¹; parallel k₁ + k₂ = {sf(kp)} N m⁻¹; (b) {sf(Ts)} s and {sf(Tp)} s; (c) {sf(Ts / Tp)}; (d) T = 2π√(m/k) does not involve g.',
               f'(a) same tension/extensions add for series (M1 A1); same extension/forces add for parallel (A1). (b) T = 2π√(m/k) (A1 A1). (c) A1. (d) R1.', 7, 'multi_step')


R.mcqs('ch11-st2', 'C2', (1, 4), [
    ('The mass on a spring is replaced by one four times as heavy. The period', 'doubles', ['quadruples', 'halves', 'is unchanged'], 'T ∝ √m.'),
    ('A pendulum clock is moved from Earth to a planet where g is four times as large. Its period', 'halves', ['doubles', 'quadruples', 'is unchanged'], 'T ∝ 1/√g.'),
    ('Two oscillators of the same frequency have a phase difference of π/2. When one is at maximum displacement, the other is', 'at its equilibrium position', ['at maximum displacement in the same direction', 'at maximum displacement in the opposite direction', 'at half amplitude'], 'Quarter cycle.'),
])


def _pendulum_spec(rng):
    g_ = rng.uniform(9.70, 9.92)
    Ls = [0.200, 0.400, 0.600, 0.800, 1.000, 1.200]
    Ts = [round(2 * math.pi * math.sqrt(L / g_) * rng.uniform(0.99, 1.01), 3) for L in Ls]
    return dict(intro='The period T of a simple pendulum is measured (by timing 20 oscillations) for different lengths L. Theory: T = 2π√(L/g).',
                xname='L', xunit='m', yname='T', yunit='s', xs=Ls, ys=Ts, xfmt=lambda x: f'{x:.3f}', yfmt=lambda y: f'{y:.3f}',
                plot_x=lambda x: x, plot_y=lambda y: y * y, plot_label='T² (y) against L (x)', what='the acceleration of free fall g', what_short='g',
                gunit='s² m⁻¹', deduce=lambda m_, b_: (4 * math.pi ** 2 / m_, 'm s⁻²', 'g = 4π²/gradient'))


def _spring_T_spec(rng):
    kk = rng.uniform(15, 40)
    ms = [0.100, 0.200, 0.300, 0.400, 0.500, 0.600]
    Ts = [round(2 * math.pi * math.sqrt(m_ / kk) * rng.uniform(0.99, 1.01), 3) for m_ in ms]
    return dict(intro='Masses m are hung from a spring and set oscillating vertically. The period T is found by timing 10 oscillations. Theory: T = 2π√(m/k).',
                xname='m', xunit='kg', yname='T', yunit='s', xs=ms, ys=Ts, xfmt=lambda x: f'{x:.3f}', yfmt=lambda y: f'{y:.3f}',
                plot_x=lambda x: x, plot_y=lambda y: y * y, plot_label='T² (y) against m (x)', what='the spring constant k', what_short='k',
                gunit='s² kg⁻¹', deduce=lambda m_, b_: (4 * math.pi ** 2 / m_, 'N m⁻¹', 'k = 4π²/gradient'))


gradient_fit('ch11-st2', _pendulum_spec)
gradient_fit('ch11-st2', _spring_T_spec)
repeat_readings('ch11-st2', 'the time for 20 oscillations of a pendulum', 's', 34.0, 37.0, 1,
                ['timed a pendulum with a hand-held stopwatch, starting at the centre of the swing.', 'used a fiducial marker at the equilibrium position to time a pendulum.'])
linearise('ch11-st2', [('T = 2π√(L/g) for a simple pendulum', 'T²', 'L', '4π²/g', 'The line should pass through the origin; a positive L-intercept suggests the length was measured to the top of the bob.'),
                       ('T = 2π√(m/k) for a mass on a spring', 'T²', 'm', '4π²/k', 'A small intercept may be due to the effective mass of the spring.')])


R.facts('ch11-st3', F(
    terms=[('total energy of an SHM oscillator', 'the sum of kinetic and potential energy, E_T = ½mω²x₀², constant in the absence of damping'),
           ('kinetic energy in SHM', 'the energy of motion, E_k = ½mω²(x₀² − x²), maximum at equilibrium'),
           ('potential energy in SHM', 'the stored energy E_p = ½mω²x², maximum at the extremes of motion'),
           ('damping', 'the reduction in amplitude of an oscillation as energy is transferred to the surroundings by resistive forces')],
    facts=[('At what displacement is the kinetic energy of an SHM oscillator equal to its potential energy?', 'x = x₀/√2', ['x = x₀/2', 'x = x₀', 'x = 0'], '½x₀² = x².'),
           ('If the amplitude of an SHM oscillator doubles, its total energy', 'quadruples', ['doubles', 'is unchanged', 'halves'], 'E ∝ x₀².'),
           ('At the equilibrium position, the kinetic energy of an oscillator is', 'maximum', ['zero', 'equal to its potential energy', 'minimum but not zero'], 'Speed is greatest.'),
           ('The total energy of an undamped SHM oscillator', 'is constant', ['is maximum at equilibrium', 'oscillates at twice the frequency', 'is zero at the extremes'], 'Conservation of energy.'),
           ('The kinetic energy of an SHM oscillator varies with a frequency of', 'twice the oscillation frequency', ['the oscillation frequency', 'half the oscillation frequency', 'zero'], 'E_k ∝ cos²ωt.')],
    why=[('Explain the energy changes as a pendulum swings from one extreme to the other.', 'At the extreme the bob is momentarily at rest with maximum GPE; as it falls to the lowest point GPE converts to KE (maximum at the centre), then KE converts back to GPE as it rises to the other extreme.'),
         ('Explain why the graph of kinetic energy against displacement for an SHM oscillator is a parabola.', 'E_k = ½mω²(x₀² − x²), a quadratic in x, maximum at x = 0 and zero at x = ±x₀.'),
         ('Explain why a real pendulum eventually stops swinging.', 'Air resistance and friction at the pivot do negative work, transferring the oscillator’s energy to the surroundings as internal energy; the amplitude decreases (damping).')],
    contrast=[('kinetic energy in SHM', 'potential energy in SHM', 'Kinetic energy is maximum at equilibrium and zero at the extremes; potential energy is zero at equilibrium and maximum at the extremes; their sum is constant without damping.')],
    misc=[('The total energy of an SHM oscillator is greatest at the equilibrium position.', 'The total energy is constant; only its division between kinetic and potential energy changes.'),
          ('Halfway between equilibrium and the amplitude, kinetic and potential energy are equal.', 'At x = x₀/2, E_p = ¼E_T and E_k = ¾E_T; they are equal at x = x₀/√2.'),
          ('A stiffer spring with the same mass and amplitude has the same energy.', 'E = ½kx₀²; a stiffer spring stores more energy for the same amplitude.')],
    evaluate=[('Energy methods are always the best way to analyse SHM problems.', ['give speeds at any displacement quickly', 'avoid trigonometric functions of time'], ['they give no information about timing or phase', 'damping and driving forces complicate the energy accounting'], 'Energy methods are efficient for speed–displacement relationships, while time-based equations are needed for phase and timing.')],
    extended=[('A 0.50 kg mass on a spring (k = 200 N m⁻¹) oscillates horizontally on a frictionless surface with amplitude 0.060 m. (a) Calculate the total energy. (b) Calculate the maximum speed. (c) Determine the speed and the kinetic energy when x = 0.030 m. (d) Sketch graphs of E_k, E_p and E_T against displacement.', '(a) E = ½ × 200 × 0.060² = 0.36 J; (b) v_max = ωx₀ = 20 × 0.060 = 1.2 m s⁻¹; (c) v = ω√(x₀² − x²) = 1.04 m s⁻¹, E_k = 0.27 J; (d) inverted parabola for E_k, parabola for E_p, horizontal line for E_T.', 6)],
))


@prob('ch11-st3', d=(1, 5), md=(1, 4), marks=2)
def p_shm_energy(rng, slot):
    k = rng.randrange(5)
    m = rng.choice([0.10, 0.20, 0.25, 0.50, 1.0]); kk = rng.choice([20, 50, 80, 200, 400]); A = rng.choice([0.020, 0.030, 0.050, 0.080, 0.10])
    w = math.sqrt(kk / m)
    if k == 0:
        return dict(stem=f'A {m} kg mass on a spring of spring constant {kk} N m⁻¹ oscillates with amplitude {A} m. Calculate the total energy of the oscillation.', v=0.5 * kk * A * A, unit='J', wrongs=[kk * A * A, 0.5 * kk * A, 0.5 * m * kk * A * A], key=f'E = ½kx₀² (M1) = {sf(0.5 * kk * A * A)} J (A1).')
    if k == 1:
        return dict(stem=f'A {m} kg mass oscillates on a spring (k = {kk} N m⁻¹) with an amplitude of {A} m. Calculate its maximum speed.', v=w * A, unit='m s⁻¹', wrongs=[w * w * A, A / w, math.sqrt(kk * A / m)], key=f'ω = √(k/m) = {sf(w)} rad s⁻¹ (M1); v_max = ωx₀ = {sf(w * A)} m s⁻¹ (A1).')
    if k == 2:
        x = A * rng.choice([0.25, 0.40, 0.50, 0.60, 0.80])
        Ek = 0.5 * m * w * w * (A * A - x * x)
        return dict(stem=f'An oscillator of mass {m} kg and angular frequency {sf(w)} rad s⁻¹ has amplitude {A} m. Calculate its kinetic energy when the displacement is {sf(x)} m.', v=Ek, unit='J', wrongs=[0.5 * m * w * w * x * x, 0.5 * m * w * w * A * A, 0.5 * m * w * w * (A - x) ** 2], key=f'E_k = ½mω²(x₀² − x²) (M1) = {sf(Ek)} J (A1).')
    if k == 3:
        L = rng.choice([0.80, 1.0, 1.5, 2.0]); th = rng.choice([5, 8, 10, 12])
        h = L * (1 - cosd(th)); v = math.sqrt(2 * g0 * h)
        return dict(stem=f'A pendulum of length {L} m is released from rest at {th}° to the vertical. Calculate its maximum speed.', v=v, unit='m s⁻¹', wrongs=[math.sqrt(2 * g0 * L), math.sqrt(g0 * L) * th / 57.3 * 2, math.sqrt(2 * g0 * L * sind(th))], key=f'h = L(1 − cos θ) = {sf(h)} m (M1); v = √(2gh) = {sf(v)} m s⁻¹ (A1).')
    f = rng.choice([0.5, 0.25, 0.75])
    x = A * math.sqrt(f)
    return dict(stem=f'An SHM oscillator has amplitude {A} m. At what displacement is its potential energy {int(f * 100)} % of its total energy?', v=x, unit='m', wrongs=[A * f, A * (1 - f), A * math.sqrt(1 - f)], key=f'E_p/E_T = x²/x₀² = {f} (M1); x = x₀√{f} = {sf(x)} m (A1).')


R.mcqs('ch11-st3', 'C2', (1, 4), [
    ('An undamped oscillator’s amplitude is halved. Its maximum kinetic energy', 'is quartered', ['is halved', 'doubles', 'is unchanged'], 'E ∝ x₀².'),
    ('A graph of potential energy against displacement for an SHM oscillator is', 'a parabola with minimum at x = 0', ['a straight line', 'an inverted parabola', 'a horizontal line'], 'E_p = ½mω²x².'),
    ('In a lightly damped oscillator, which quantity decreases fastest?', 'The total energy (∝ amplitude²)', ['The period', 'The amplitude', 'The frequency'], 'Energy ∝ A².'),
])


R.facts('ch11-st4', F(
    terms=[('displacement equation of SHM', 'the expression x = x₀ sin(ωt + φ) (or x₀ cos(ωt + φ)), where φ is the phase angle'),
           ('velocity equation of SHM', 'the expression v = ωx₀ cos(ωt + φ), with v = ±ω√(x₀² − x²)'),
           ('acceleration equation of SHM', 'the expression a = −ω²x₀ sin(ωt + φ) = −ω²x'),
           ('phase angle', 'the constant φ that sets the starting point of the oscillation at t = 0')],
    facts=[('An oscillator is released from rest at maximum displacement at t = 0. Its displacement is', 'x = x₀ cos ωt', ['x = x₀ sin ωt', 'x = x₀ tan ωt', 'x = ωx₀ cos ωt'], 'x = x₀ at t = 0.'),
           ('The maximum acceleration of an oscillator is', 'ω²x₀', ['ωx₀', 'x₀/ω²', 'ω/x₀'], 'a = −ω²x.'),
           ('In SHM, the velocity leads the displacement by', 'π/2 rad', ['π rad', '0', '2π rad'], 'cos vs sin.'),
           ('The acceleration and displacement in SHM are', 'in antiphase', ['in phase', 'π/2 out of phase', 'unrelated'], 'a = −ω²x.'),
           ('The speed of an SHM oscillator at displacement x is', 'ω√(x₀² − x²)', ['ωx', 'ω²x', 'ω(x₀ − x)'], 'From energy.')],
    why=[('Explain how the velocity–time graph of an SHM oscillator can be obtained from its displacement–time graph.', 'Velocity is the gradient of the displacement–time graph; for a sine curve the gradient is a cosine curve of amplitude ωx₀, so the v–t graph is shifted a quarter cycle ahead.'),
         ('Explain why the speed is not zero at half the amplitude.', 'v = ω√(x₀² − x²); at x = x₀/2 the speed is (√3/2)ωx₀ ≈ 0.87 v_max; speed is only zero at the extremes.'),
         ('Explain the significance of the negative sign in a = −ω²x.', 'It shows the acceleration is always directed opposite to the displacement, i.e. towards the equilibrium position (restoring).')],
    contrast=[('x = x₀ sin ωt', 'x = x₀ cos ωt', 'Both describe SHM with the same ω and amplitude; sin starts at equilibrium moving in the positive direction at t = 0, cos starts at maximum displacement at rest. They differ by a phase of π/2.')],
    misc=[('The acceleration of an SHM oscillator is greatest when its speed is greatest.', 'Acceleration is greatest at the extremes where the speed is zero; at equilibrium speed is maximum and acceleration is zero.'),
          ('In x = x₀ sin ωt, ωt should be calculated in degrees.', 'ωt is in radians, since ω is in rad s⁻¹; calculators must be in radian mode.'),
          ('Displacement and velocity in SHM are in phase.', 'Velocity leads displacement by π/2: it is maximum when x = 0.')],
    evaluate=[('Describing oscillations by sinusoidal equations is just a mathematical convenience.', ['sin/cos solve a = −ω²x exactly'], ['the same mathematics describes AC circuits, waves, quantum oscillators', 'Fourier analysis shows any periodic motion can be built from sinusoids', 'measurements of real oscillators match the predicted waveforms'], 'Sinusoidal descriptions follow directly from the physics of linear restoring forces and are confirmed by measurement, making them much more than a convenience.')],
    extended=[('A piston in a model engine moves with approximately SHM of amplitude 0.040 m and frequency 25 Hz. (a) Calculate ω. (b) Calculate the maximum speed and maximum acceleration of the piston. (c) Write an equation for x(t), taking x = +0.040 m at t = 0. (d) Calculate the displacement and velocity at t = 0.0050 s.', '(a) ω = 157 rad s⁻¹; (b) v_max = 6.28 m s⁻¹, a_max = 987 m s⁻²; (c) x = 0.040 cos(157t); (d) ωt = 0.785 rad: x = 0.0283 m, v = −4.44 m s⁻¹.', 6)],
))


@prob('ch11-st4', d=(2, 5), md=(2, 4), marks=3)
def p_shm_eq(rng, slot):
    k = rng.randrange(5)
    A = rng.choice([0.020, 0.040, 0.050, 0.080, 0.12]); f = rng.choice([0.50, 1.0, 2.0, 2.5, 4.0, 5.0])
    w = 2 * math.pi * f
    if k == 0:
        t = rng.choice([0.05, 0.10, 0.15, 0.20, 0.30]); x = A * math.cos(w * t)
        return dict(stem=f'An oscillator is released from rest at x = {A} m at t = 0 and performs SHM at {f} Hz. Calculate its displacement at t = {t} s.', v=x, unit='m', wrongs=[A * math.sin(w * t), A * math.cos(math.radians(w * t)), A * math.cos(f * t)], key=f'x = x₀ cos(2πft) (M1) = {A} cos({sf(w * t)} rad) = {sf(x)} m (A1).', marks=2)
    if k == 1:
        x = A * rng.choice([0.25, 0.50, 0.60, 0.80])
        v = w * math.sqrt(A * A - x * x)
        return dict(stem=f'A body performs SHM with amplitude {A} m and frequency {f} Hz. Calculate its speed when its displacement is {sf(x)} m.', v=v, unit='m s⁻¹', wrongs=[w * x, w * (A - x), f * math.sqrt(A * A - x * x)], key=f'ω = 2πf = {sf(w)} rad s⁻¹ (M1); v = ω√(x₀² − x²) (M1) = {sf(v)} m s⁻¹ (A1).')
    if k == 2:
        return dict(stem=f'A loudspeaker cone vibrates in SHM at {f * 100:g} Hz with amplitude {A / 100:g} m. Calculate its maximum acceleration.', v=(w * 100) ** 2 * A / 100, unit='m s⁻²', wrongs=[w * 100 * A / 100, (f * 100) ** 2 * A / 100, (w * 100) ** 2 * A], key=f'a_max = ω²x₀ = (2π × {f * 100:g})² × {A / 100:g} (M1) = {sf((w * 100) ** 2 * A / 100)} m s⁻² (A1).', marks=2)
    if k == 3:
        t = rng.choice([0.05, 0.10, 0.125, 0.20])
        v = w * A * math.cos(w * t)
        return dict(stem=f'An oscillator passes through equilibrium moving in the positive direction at t = 0 (x = x₀ sin ωt), with x₀ = {A} m and f = {f} Hz. Calculate its velocity at t = {t} s.', v=v, unit='m s⁻¹', wrongs=[w * A * math.sin(w * t), A * math.cos(w * t), w * A], key=f'v = ωx₀ cos ωt (M1) = {sf(w * A)} cos({sf(w * t)}) = {sf(v)} m s⁻¹ (A1).', marks=2)
    frac = rng.choice([0.5, 0.25, 0.75])
    t = math.acos(frac) / w
    return dict(stem=f'An oscillator starts at maximum displacement x₀ at t = 0 and oscillates at {f} Hz. Calculate the first time at which its displacement is {frac} x₀.', v=t, unit='s', wrongs=[math.asin(frac) / w, frac / f, math.acos(frac) / f], key=f'{frac} = cos ωt (M1); t = cos⁻¹({frac})/ω = {sf(t)} s (A1).', marks=2)


@R.add('ch11-st4', 'C4', (3, 5), 'multi_step')
def c4_tide(rng, slot):
    A = rng.choice([1.5, 2.0, 2.5, 3.0]); T = 12.4; d = rng.choice([1.0, 1.5])
    w = 2 * math.pi / T
    t = math.acos(-d / A) / w if d < A else None
    if t is None:
        return None
    return num(f'In a harbour in {rng.choice(CITIES)}, the water level rises and falls approximately in SHM with period 12.4 h and amplitude {A} m about mean sea level. High tide is at t = 0. (a) Write an equation for the height h(t) relative to mean sea level. (b) Calculate the maximum rate of rise of the water in m h⁻¹. (c) A boat needs the water to be no more than {d} m below mean sea level. Calculate the time after high tide when the water first falls to this level. (d) Discuss why real tides are only approximately simple harmonic.',
               f'(a) h = {A} cos(2πt/12.4); (b) ωA = {sf(w * A)} m h⁻¹; (c) t = {sf(t)} h; (d) the shape of coastlines, combined solar and lunar tides, weather and resonance in bays produce non-sinusoidal variations.',
               f'(a) A1. (b) v_max = ωx₀ (M1 A1). (c) −{d} = {A} cos ωt (M1), t (A1). (d) R1.', 6, 'multi_step')


R.mcqs('ch11-st4', 'C2', (1, 4), [
    ('For an object in SHM described by x = x₀ sin ωt, the velocity at t = 0 is', 'maximum and positive', ['zero', 'maximum and negative', 'equal to x₀'], 'v = ωx₀ cos 0.'),
    ('Which pair of quantities in SHM are always in antiphase?', 'Displacement and acceleration', ['Displacement and velocity', 'Velocity and acceleration', 'Kinetic energy and speed'], 'a = −ω²x.'),
    ('If the frequency of an oscillator doubles at the same amplitude, its maximum acceleration', 'quadruples', ['doubles', 'is unchanged', 'halves'], 'a_max = ω²x₀.'),
])


# =============================================================================================
# ch12 C.2 Wave model
# =============================================================================================
R.facts('ch12-st1', F(
    terms=[('travelling wave', 'a disturbance that transfers energy (and information) from one place to another without a net transfer of matter'),
           ('transverse wave', 'a wave in which the oscillations of the medium are perpendicular to the direction of energy transfer'),
           ('longitudinal wave', 'a wave in which the oscillations of the medium are parallel to the direction of energy transfer'),
           ('compression', 'a region of a longitudinal wave where the particles are closer together than normal (higher pressure)'),
           ('rarefaction', 'a region of a longitudinal wave where the particles are further apart than normal (lower pressure)'),
           ('mechanical wave', 'a wave that requires a material medium to travel through')],
    facts=[('Which of these is a longitudinal wave?', 'Sound in air', ['Light', 'A wave on a guitar string', 'A ripple on water'], 'Oscillations parallel to travel.'),
           ('Which of these can travel through a vacuum?', 'Electromagnetic waves', ['Sound waves', 'Water waves', 'Seismic P-waves'], 'No medium needed.'),
           ('Seismic S-waves cannot travel through Earth’s outer core because', 'they are transverse and liquids cannot support shear', ['they are longitudinal', 'the core is too hot', 'they are too slow'], 'Evidence for a liquid outer core.'),
           ('As a wave passes, the particles of the medium', 'oscillate about fixed positions', ['travel with the wave', 'stay completely still', 'move in straight lines away from the source'], 'No net transfer of matter.'),
           ('Which type of wave can be polarised?', 'Transverse', ['Longitudinal', 'Sound', 'All waves'], 'Oscillation direction must be perpendicular to travel.')],
    why=[('Explain why a cork on a pond bobs up and down but does not travel with the ripples.', 'The ripples transfer energy, not water; the water (and cork) oscillate about a mean position as the wave passes.'),
         ('Explain how seismic waves provide evidence that Earth’s outer core is liquid.', 'Transverse S-waves are not detected in a shadow zone on the far side of Earth; since liquids cannot transmit shear (transverse) waves, the outer core must be liquid.'),
         ('Explain why sound cannot travel through space.', 'Sound is a mechanical, longitudinal wave that propagates by collisions between particles of a medium; in a vacuum there are no particles.')],
    contrast=[('transverse waves', 'longitudinal waves', 'In transverse waves the medium oscillates perpendicular to the direction of energy transfer (crests and troughs, can be polarised); in longitudinal waves it oscillates parallel to it (compressions and rarefactions, cannot be polarised).')],
    misc=[('Waves transfer matter from one place to another.', 'Waves transfer energy; particles of the medium oscillate about their equilibrium positions.'),
          ('All waves need a medium.', 'Mechanical waves do, but electromagnetic waves can travel through a vacuum.'),
          ('In a longitudinal wave the particles move along with the wave.', 'They oscillate back and forth about fixed positions parallel to the direction of travel.')],
    evaluate=[('Early-warning systems based on detecting P-waves can significantly reduce earthquake casualties.', ['P-waves travel faster than the damaging S- and surface waves, giving seconds of warning', 'automatic train stopping and gas shut-off in Japan and Mexico'], ['warning time is short close to the epicentre', 'false alarms reduce public trust', 'expensive dense sensor networks are needed'], 'They provide valuable seconds that can save lives and infrastructure, particularly for automated responses, but are limited close to the epicentre.')],
    extended=[('An earthquake produces P-waves (6.0 km s⁻¹) and S-waves (3.5 km s⁻¹). A seismometer in a city records the S-waves arriving 48 s after the P-waves. (a) State which wave is longitudinal. (b) Determine the distance to the epicentre. (c) Calculate the warning time a P-wave alert could give before the S-waves arrive at a city 200 km from the epicentre. (d) Explain why at least three stations are needed to locate the epicentre.', '(a) P-waves; (b) d/3.5 − d/6.0 = 48, d = 403 km; (c) 200/3.5 − 200/6.0 = 23.8 s (less processing time); (d) each station gives a distance (a circle); three circles intersect at one point.', 6)],
))


@prob('ch12-st1', d=(2, 5), md=(2, 4), marks=3)
def p_seismic(rng, slot):
    k = rng.randrange(3)
    vp = rng.choice([6.0, 6.5, 7.0, 8.0]); vs = rng.choice([3.5, 3.8, 4.0, 4.5])
    city = rng.choice(CITIES)
    if k == 0:
        dt = rng.choice([20, 30, 45, 60, 90])
        d = dt / (1 / vs - 1 / vp)
        return dict(stem=f'A seismometer in {city} records P-waves ({vp} km s⁻¹) and then S-waves ({vs} km s⁻¹) {dt} s later from the same earthquake. Calculate the distance to the epicentre.',
                    v=d, unit='km', wrongs=[dt * (vp - vs), dt * vp, dt * vs], key=f'd/{vs} − d/{vp} = {dt} (M1); d = {sf(d)} km (A1).')
    if k == 1:
        d = rng.choice([100, 150, 250, 400])
        dt = d / vs - d / vp
        return dict(stem=f'An earthquake occurs {d} km from {city}. P-waves travel at {vp} km s⁻¹ and S-waves at {vs} km s⁻¹. Calculate the time between the arrivals of the two waves.',
                    v=dt, unit='s', wrongs=[d / (vp - vs), d / vs, d / vp], key=f't_S − t_P = {d}/{vs} − {d}/{vp} (M1) = {sf(dt)} s (A1).', marks=2)
    d = rng.choice([500, 1000, 2000])
    return dict(stem=f'A tsunami travels {d} km across the ocean at 200 m s⁻¹. Calculate the travel time in hours.',
                v=d * 1000 / 200 / 3600, unit='h', wrongs=[d / 200, d * 1000 / 200 / 60, d / 200 / 3.6], key=f't = d/v = {d * 1000}/200 = {sf(d * 1000 / 200)} s (M1) = {sf(d * 1000 / 200 / 3600)} h (A1).', marks=2)


R.mcqs('ch12-st1', 'C2', (1, 4), [
    ('A longitudinal wave travels along a slinky. A coil at a compression is', 'closer to its neighbours than when undisturbed', ['moving perpendicular to the slinky', 'at rest permanently', 'further from its neighbours'], 'Compression.'),
    ('Which wave property shows that light is transverse?', 'It can be polarised', ['It can be reflected', 'It can be refracted', 'It can be diffracted'], 'Only transverse waves can be polarised.'),
    ('A transverse wave travels to the right along a rope. A point on the rope moves', 'up and down', ['to the right', 'to the left', 'in a circle'], 'Perpendicular to travel.'),
])


R.facts('ch12-st2', F(
    terms=[('wavelength', 'the shortest distance between two points on a wave that are in phase, λ, in m'),
           ('frequency (wave)', 'the number of complete oscillations per second of any point on the wave, f, in Hz'),
           ('wave speed', 'the speed at which energy is transferred by the wave, v = fλ'),
           ('period (wave)', 'the time for one complete oscillation of a point on the wave, T = 1/f'),
           ('amplitude (wave)', 'the maximum displacement of a point on the wave from its equilibrium position')],
    facts=[('A wave of frequency 50 Hz has a wavelength of 4.0 m. Its speed is', '200 m s⁻¹', ['12.5 m s⁻¹', '0.080 m s⁻¹', '54 m s⁻¹'], 'v = fλ.'),
           ('When a wave passes from deep to shallow water, which quantity stays the same?', 'Frequency', ['Speed', 'Wavelength', 'Direction'], 'Frequency is set by the source.'),
           ('The speed of a wave on a string depends on', 'the tension and mass per unit length of the string', ['the amplitude', 'the frequency', 'the wavelength'], 'Medium properties.'),
           ('A source doubles its frequency in the same medium. The wavelength', 'halves', ['doubles', 'stays the same', 'quadruples'], 'v fixed.'),
           ('Radio station frequency 100 MHz corresponds to a wavelength of', '3.0 m', ['30 m', '0.30 m', '300 m'], 'λ = c/f.')],
    why=[('Explain why the frequency of a wave does not change when it moves into a different medium.', 'The frequency is set by the source; every oscillation arriving at the boundary must produce one oscillation on the other side, so the number per second is unchanged while speed and wavelength change.'),
         ('Explain why increasing the frequency of a signal generator connected to a vibrating string reduces the wavelength.', 'The wave speed depends on the string’s tension and mass per unit length, which are unchanged; with v constant, λ = v/f decreases as f increases.'),
         ('Derive v = fλ from the definition of speed.', 'In one period T a wave advances one wavelength λ, so v = λ/T, and since f = 1/T, v = fλ.')],
    contrast=[('the wave speed', 'the speed of particles in the medium', 'The wave speed is the rate at which energy propagates (v = fλ, fixed by the medium); the particle speed varies during each oscillation, depends on amplitude and frequency, and is maximum at equilibrium.')],
    misc=[('Increasing the frequency of a wave increases its speed.', 'In a given medium the speed is fixed; increasing frequency reduces the wavelength.'),
          ('A larger amplitude wave travels faster.', 'Speed depends on the medium, not the amplitude (for small amplitudes).'),
          ('The wavelength is the distance between a crest and the next trough.', 'That is half a wavelength; λ is the distance between successive crests (points in phase).')],
    evaluate=[('5G mobile networks use higher frequencies so they must transmit data faster through the air.', ['higher carrier frequencies allow greater bandwidth, so more data per second'], ['all EM waves travel at the same speed in air', 'higher frequencies have shorter range and are absorbed more by buildings', 'requires more base stations'], 'The waves are no faster; higher frequencies give greater bandwidth (data rate) but shorter range.')],
    extended=[('A student uses a ripple tank with a vibrating dipper at 12 Hz. A photograph shows 9 complete wavefronts spanning 24.0 cm in the deep region and 9 spanning 15.6 cm in the shallow region. (a) Calculate the wavelength in each region. (b) Calculate the wave speed in each region. (c) State and explain what happens to the frequency at the boundary. (d) Suggest one source of uncertainty and how to reduce it.', '(a) 9 wavefronts span 8 wavelengths: 3.00 cm and 1.95 cm; (b) 0.360 m s⁻¹ and 0.234 m s⁻¹; (c) unchanged – set by the dipper; (d) wavefronts blurred in the photo – use a stroboscope to freeze the pattern and measure across more waves.', 6)],
))


@prob('ch12-st2', d=(1, 5), md=(1, 4), marks=2)
def p_vflam(rng, slot):
    k = rng.randrange(6)
    city = rng.choice(CITIES)
    if k == 0:
        f = rng.choice([256, 440, 512, 1000, 2000, 20]); v = rng.choice([330, 340, 343])
        return dict(stem=f'A tuning fork of frequency {f} Hz sounds in air where the speed of sound is {v} m s⁻¹. Calculate the wavelength.', v=v / f, unit='m', wrongs=[f / v, v * f, v / f * 2], key=f'λ = v/f (M1) = {sf(v / f)} m (A1).')
    if k == 1:
        f = rng.choice([88.5, 95.8, 101.1, 104.3]) * 1e6
        return dict(stem=f'A radio station in {city} broadcasts at {sf(f / 1e6, 4)} MHz. Calculate the wavelength of the radio waves.', v=C / f, unit='m', wrongs=[f / C, C / (f / 1e6), C * f / 1e16], key=f'λ = c/f (M1) = {sf(C / f)} m (A1).')
    if k == 2:
        lam = rng.choice([0.020, 0.035, 0.050, 0.080]); f = rng.choice([8, 10, 12, 15, 20])
        return dict(stem=f'Ripples in a tank have a wavelength of {lam * 100:g} cm and a frequency of {f} Hz. Calculate their speed.', v=f * lam, unit='m s⁻¹', wrongs=[f / lam, lam / f, f * lam * 100], key=f'v = fλ (M1) = {f} × {lam} = {sf(f * lam)} m s⁻¹ (A1).')
    if k == 3:
        lam = rng.choice([400, 450, 532, 589, 633, 700]) * 1e-9
        return dict(stem=f'Calculate the frequency of light of wavelength {sf(lam * 1e9, 3)} nm in a vacuum.', v=C / lam, unit='Hz', wrongs=[lam / C, C * lam, C / (lam * 1e9)], key=f'f = c/λ (M1) = {sf(C / lam)} Hz (A1).')
    if k == 4:
        T = rng.choice([4.0, 6.0, 8.0, 10, 12]); lam = rng.choice([20, 40, 60, 90, 120])
        return dict(stem=f'Ocean swell reaching the coast near {city} has a period of {T} s and a wavelength of {lam} m. Calculate the wave speed.', v=lam / T, unit='m s⁻¹', wrongs=[lam * T, T / lam, lam / (2 * math.pi * T)], key=f'v = λ/T (M1) = {sf(lam / T)} m s⁻¹ (A1).')
    v1 = rng.choice([0.30, 0.36, 0.40]); v2 = rng.choice([0.18, 0.22, 0.25]); f = rng.choice([8, 10, 12])
    return dict(stem=f'Water waves of frequency {f} Hz travel at {v1} m s⁻¹ in deep water and slow to {v2} m s⁻¹ in shallow water. Calculate the wavelength in the shallow water.', v=v2 / f, unit='m', wrongs=[v1 / f, v2 * f, v1 / v2 / f], key=f'f unchanged (M1); λ = v/f = {sf(v2 / f)} m (A1).')


R.mcqs('ch12-st2', 'C2', (1, 4), [
    ('Light passes from air into glass. Its frequency', 'stays the same while its speed and wavelength decrease', ['decreases', 'increases', 'stays the same while its wavelength increases'], 'Frequency set by source.'),
    ('Two sounds in the same room have frequencies 200 Hz and 400 Hz. The ratio of their wavelengths λ₂₀₀ : λ₄₀₀ is', '2 : 1', ['1 : 2', '1 : 1', '4 : 1'], 'Same v.'),
    ('The period of a wave is 0.020 s. Its frequency is', '50 Hz', ['0.020 Hz', '20 Hz', '500 Hz'], 'f = 1/T.'),
])


def _wave_spec(rng):
    v = rng.uniform(325, 350)
    fs = [400, 500, 600, 800, 1000, 1200]
    ls = [round(v / f * rng.uniform(0.98, 1.02), 3) for f in fs]
    return dict(intro='A loudspeaker connected to a signal generator emits sound of frequency f. The wavelength λ is found by moving a microphone between adjacent points where the signal is in phase, using a dual-trace oscilloscope. Theory: λ = v/f.',
                xname='f', xunit='Hz', yname='λ', yunit='m', xs=fs, ys=ls, xfmt=lambda x: f'{x}', yfmt=lambda y: f'{y:.3f}',
                plot_x=lambda x: 1 / x, plot_y=lambda y: y, plot_label='λ (y) against 1/f (x)', what='the speed of sound v in air', what_short='v',
                gunit='m s⁻¹', deduce=lambda m_, b_: (m_, 'm s⁻¹', 'v = gradient'))


gradient_fit('ch12-st2', _wave_spec)


R.facts('ch12-st3', F(
    terms=[('displacement–distance graph', 'a "snapshot" graph showing the displacement of every point along a wave at one instant; the wavelength can be read from it'),
           ('displacement–time graph', 'a graph showing how the displacement of one point on a wave varies with time; the period can be read from it'),
           ('crest', 'a point of maximum positive displacement on a transverse wave'),
           ('trough', 'a point of maximum negative displacement on a transverse wave'),
           ('in phase', 'describing two points on a wave that have the same displacement and velocity at all times, separated by a whole number of wavelengths')],
    facts=[('On a displacement–distance graph of a wave, the distance between two adjacent crests is the', 'wavelength', ['period', 'amplitude', 'frequency'], 'Snapshot shows λ.'),
           ('On a displacement–time graph for one point on a wave, the time between two adjacent crests is the', 'period', ['wavelength', 'amplitude', 'speed'], 'Graph for one point shows T.'),
           ('Two points on a wave half a wavelength apart are', 'in antiphase', ['in phase', 'π/2 out of phase', 'always at rest'], 'Phase difference π.'),
           ('A displacement–distance graph cannot directly give the', 'frequency', ['wavelength', 'amplitude', 'phase difference between points'], 'Needs time information.'),
           ('For a longitudinal wave, a displacement–distance graph shows', 'displacement of particles along the direction of travel plotted against position', ['the shape of the wave', 'the pressure only', 'nothing useful'], 'Positive displacement = in direction of travel.')],
    why=[('Explain how the direction of motion of a point on a transverse wave can be found from a displacement–distance graph.', 'Shift the snapshot a small distance in the direction of travel; the point moves to the displacement of the wave that now occupies its position, so points ahead of a crest move up and points behind it move down.'),
         ('Explain why the phase difference between two points on a wave depends on their separation.', 'Each point repeats the motion of the point behind it after a delay Δx/v; this delay corresponds to a phase difference 2πΔx/λ.'),
         ('Explain how compressions can be identified on a displacement–distance graph of a longitudinal wave.', 'A compression is where particles on either side are displaced towards the point: positive displacement to the left of the point and negative to the right, which occurs where the graph crosses zero with negative gradient (taking positive as the direction of travel).')],
    contrast=[('a displacement–distance graph', 'a displacement–time graph', 'A displacement–distance graph is a snapshot of all points at one instant and shows the wavelength; a displacement–time graph follows one point over time and shows the period.')],
    misc=[('A displacement–time graph shows the shape of the wave.', 'It shows how one point moves in time; the shape of the wave in space at an instant is shown by a displacement–distance graph.'),
          ('Points at a crest are moving fastest.', 'At a crest the displacement is maximum and the point is momentarily at rest; points at equilibrium move fastest.'),
          ('Two points a full wavelength apart are in antiphase.', 'They are in phase (phase difference 2π); points half a wavelength apart are in antiphase.')],
    evaluate=[('Graphs are a better way than equations to describe waves.', ['graphs make wavelength, period and phase visible', 'easy to compare snapshots'], ['equations y = A sin(2π(x/λ − t/T)) contain all information compactly', 'calculations need equations', 'graphs can be misread (confusing the two types)'], 'Graphs and equations complement each other: graphs aid understanding and data reading, equations allow precise calculation.')],
    extended=[('A transverse wave of amplitude 3.0 cm, wavelength 0.80 m and frequency 5.0 Hz travels in the +x direction along a rope. At t = 0 the point at x = 0 is at zero displacement moving upwards. (a) Calculate the wave speed. (b) Sketch the displacement–distance graph at t = 0 for 0 ≤ x ≤ 1.6 m. (c) Sketch the displacement–time graph for the point at x = 0 for one period. (d) Determine the phase difference between points at x = 0 and x = 0.20 m and the displacement of the point at x = 0.20 m at t = 0.', '(a) 4.0 m s⁻¹; (b) two full wavelengths; at x = 0, y = 0 with the wave ahead (x > 0) at y = −3.0 sin(2πx/0.80); (c) sine curve, period 0.20 s, starting at 0 going up; (d) π/2 rad (a quarter wavelength); the point at x = 0.20 m lags by a quarter cycle, so it is at −3.0 cm (a trough) at t = 0.', 6)],
))


@prob('ch12-st3', d=(1, 5), md=(1, 4), marks=2)
def p_graphs(rng, slot):
    k = rng.randrange(5)
    if k == 0:
        lam = rng.choice([0.40, 0.60, 0.80, 1.2, 2.0]); dx = lam * rng.choice([0.125, 0.25, 0.375, 0.5, 0.75])
        phi = 2 * math.pi * dx / lam
        return dict(stem=f'Two points on a wave of wavelength {lam} m are {sf(dx)} m apart along the direction of travel. Calculate their phase difference in radians.', v=phi, unit='rad', wrongs=[dx / lam, 2 * math.pi * lam / dx, 360 * dx / lam], key=f'Δφ = 2πΔx/λ (M1) = {sf(phi)} rad (A1).')
    if k == 1:
        n = rng.choice([2, 3, 4, 5]); L = rng.choice([1.2, 1.6, 2.0, 3.0]); T = rng.choice([0.02, 0.05, 0.10, 0.25])
        lam = L / n
        return dict(stem=f'A displacement–distance graph shows {n} complete wavelengths in {L} m. A displacement–time graph for one point shows a period of {T} s. Calculate the wave speed.', v=lam / T, unit='m s⁻¹', wrongs=[L / T, lam * T, n / (L * T)], key=f'λ = {L}/{n} = {sf(lam)} m (M1); v = λ/T = {sf(lam / T)} m s⁻¹ (A1).')
    if k == 2:
        n = rng.choice([3, 4, 5, 6]); t = rng.choice([0.012, 0.020, 0.030, 0.050])
        return dict(stem=f'A displacement–time graph for a point on a sound wave shows {n} complete cycles in {t * 1000:g} ms. Calculate the frequency.', v=n / t, unit='Hz', wrongs=[t / n, n * t, 1 / t], key=f'T = {t}/{n} (M1); f = 1/T = {sf(n / t)} Hz (A1).')
    if k == 3:
        A = rng.choice([0.020, 0.030, 0.050]); lam = rng.choice([0.40, 0.80, 1.2]); x = lam * rng.choice([1 / 12, 1 / 8, 1 / 6, 1 / 3])
        y = A * math.sin(2 * math.pi * x / lam)
        return dict(stem=f'At t = 0 the displacement of a wave is y = {A} sin(2πx/{lam}) (y and x in m). Calculate the displacement at x = {sf(x)} m.', v=y, unit='m', wrongs=[A * math.sin(2 * math.pi * x), A * math.sin(math.radians(2 * math.pi * x / lam)), A * x / lam], key=f'y = {A} sin(2π × {sf(x)}/{lam}) (M1) = {sf(y)} m (A1).')
    f = rng.choice([2.0, 5.0, 10, 25]); dt = rng.choice([0.005, 0.010, 0.020, 0.025])
    if dt * f >= 1:
        return None
    return dict(stem=f'Two points on a wave of frequency {f} Hz reach maximum displacement {dt} s apart. Calculate their phase difference in degrees.', v=360 * f * dt, unit='°', ans=deg(360 * f * dt), wrongs=[2 * math.pi * f * dt, 360 * dt / f, 180 * f * dt], key=f'Δφ = 360° × Δt/T = 360 × {f} × {dt} (M1) = {deg(360 * f * dt)} (A1).')


R.mcqs('ch12-st3', 'C2', (1, 4), [
    ('A transverse wave moves to the right. On a snapshot, a point just to the right of a crest is moving', 'upwards', ['downwards', 'to the right', 'not at all'], 'The crest is about to arrive.'),
    ('On a displacement–time graph for a point on a wave, the gradient gives the', 'velocity of that point', ['wave speed', 'wavelength', 'frequency'], 'dy/dt.'),
    ('Points P and Q on a wave are 1.5 wavelengths apart. They are', 'in antiphase', ['in phase', 'a quarter cycle apart', 'both at rest'], '1.5λ → phase 3π.'),
])


R.facts('ch12-st4', F(
    terms=[('sound wave', 'a longitudinal mechanical wave consisting of compressions and rarefactions in a medium'),
           ('electromagnetic wave', 'a transverse wave of oscillating electric and magnetic fields that travels at c = 3.00 × 10⁸ m s⁻¹ in a vacuum'),
           ('electromagnetic spectrum', 'the range of electromagnetic waves ordered by wavelength: radio, microwave, infrared, visible, ultraviolet, X-ray and gamma'),
           ('ultrasound', 'sound waves with frequencies above the upper limit of human hearing (about 20 kHz)'),
           ('range of human hearing', 'approximately 20 Hz to 20 kHz, decreasing at the upper end with age')],
    facts=[('The speed of sound in air at room temperature is about', '340 m s⁻¹', ['3.0 × 10⁸ m s⁻¹', '34 m s⁻¹', '1500 m s⁻¹'], 'About 343 m s⁻¹ at 20 °C.'),
           ('Sound travels fastest in', 'steel', ['air', 'water', 'a vacuum'], 'Stiff solids: ~5000 m s⁻¹.'),
           ('Which electromagnetic waves have the shortest wavelength?', 'Gamma rays', ['Radio waves', 'Visible light', 'Microwaves'], 'λ < 10⁻¹¹ m.'),
           ('Visible light has wavelengths of approximately', '400–700 nm', ['4–7 nm', '400–700 μm', '4–7 mm'], 'Violet to red.'),
           ('All electromagnetic waves in a vacuum have the same', 'speed', ['frequency', 'wavelength', 'energy'], 'c.')],
    why=[('Explain why the speed of sound in air increases with temperature.', 'Sound is transmitted by molecular collisions; at higher temperature molecules move faster (c_rms ∝ √T), so disturbances are passed on more quickly.'),
         ('Explain why lightning is seen before thunder is heard.', 'Light travels at 3.00 × 10⁸ m s⁻¹, almost a million times faster than sound (≈ 340 m s⁻¹), so the light arrives almost instantly while the sound takes about 3 s per kilometre.'),
         ('Explain how ultrasound is used to measure the depth of the sea.', 'A pulse is sent down and the time for the echo is measured; depth = (speed of sound in water × time)/2.')],
    contrast=[('sound waves', 'electromagnetic waves', 'Sound waves are longitudinal mechanical waves that need a medium and travel at hundreds to thousands of m s⁻¹; EM waves are transverse oscillating fields that travel through a vacuum at 3.00 × 10⁸ m s⁻¹.')],
    misc=[('Sound travels faster in air than in water because air is less dense.', 'Sound travels faster in water (~1500 m s⁻¹) because water is much less compressible; stiffness matters more than density.'),
          ('Radio waves are a type of sound wave.', 'Radio waves are electromagnetic; a radio receiver converts the information they carry into sound.'),
          ('Gamma rays travel faster than radio waves because they have more energy.', 'All EM waves travel at c in a vacuum; gamma photons have higher energy because of their higher frequency.')],
    evaluate=[('Ultrasound imaging is safer than X-ray imaging and should always be preferred.', ['ultrasound is non-ionising – no known cancer risk', 'real-time imaging, cheap and portable'], ['ultrasound cannot image through bone or air well (lungs, brain)', 'lower resolution for some applications', 'X-ray CT gives detailed 3D images of bone'], 'Ultrasound is preferred where it gives adequate images (pregnancy, soft tissue), but X-rays remain necessary for bone and some diagnoses.')],
    extended=[('A ship’s sonar sends a 40 kHz ultrasound pulse vertically down. The echo from the sea bed returns after 0.280 s. The speed of sound in sea water is 1530 m s⁻¹. (a) Calculate the depth of the sea. (b) Calculate the wavelength of the ultrasound in water. (c) Explain why ultrasound rather than audible sound is used. (d) Suggest why the speed of sound in the sea varies with depth.', '(a) 1530 × 0.280/2 = 214 m; (b) 3.83 cm; (c) shorter wavelength gives better resolution and a narrower beam, and it does not disturb people; (d) temperature, salinity and pressure change with depth.', 6)],
))


@prob('ch12-st4', d=(1, 5), md=(1, 4), marks=2)
def p_sound_em(rng, slot):
    k = rng.randrange(6)
    city = rng.choice(CITIES)
    if k == 0:
        t = rng.choice([1.5, 2.0, 3.0, 4.5, 6.0]); v = 340
        return dict(stem=f'During a storm near {city}, thunder is heard {t} s after the lightning flash. Estimate the distance to the lightning (speed of sound 340 m s⁻¹).', v=v * t, unit='m', wrongs=[v * t / 2, v / t, C * t], key=f'd = vt (light travel time negligible) (M1) = {sf(v * t)} m (A1).')
    if k == 1:
        t = rng.choice([0.10, 0.20, 0.35, 0.50, 1.2]); v = 1500
        return dict(stem=f'A sonar pulse from a boat returns from a shoal of fish after {t} s. The speed of sound in sea water is 1500 m s⁻¹. Calculate the depth of the shoal.', v=v * t / 2, unit='m', wrongs=[v * t, v / t, v * t * 2], key=f'd = vt/2 (M1) = {sf(v * t / 2)} m (A1).')
    if k == 2:
        f = rng.choice([2.0, 3.5, 5.0, 7.5]) * 1e6; v = 1540
        return dict(stem=f'A medical ultrasound scanner operates at {sf(f / 1e6, 2)} MHz. The speed of sound in soft tissue is 1540 m s⁻¹. Calculate the wavelength in tissue.', v=v / f, unit='m', wrongs=[f / v, v * f, C / f], key=f'λ = v/f (M1) = {sf(v / f)} m (A1).')
    if k == 3:
        d = rng.choice([3.84e8, 1.50e11, 2.25e11, 7.8e11]); body = {3.84e8: 'the Moon', 1.50e11: 'the Sun', 2.25e11: 'Mars (mean distance)', 7.8e11: 'Jupiter'}[d]
        return dict(stem=f'Calculate the time taken for light to travel from {body} to Earth, a distance of {sf(d)} m.', v=d / C, unit='s', wrongs=[C / d, d / 340, d * C / 1e25], key=f't = d/c (M1) = {sf(d / C)} s (A1).')
    if k == 4:
        f = rng.choice([2.45e9, 5.0e9, 1.0e15, 3.0e18, 6.0e13]); band = {2.45e9: 'microwave', 5.0e9: 'microwave', 1.0e15: 'ultraviolet', 3.0e18: 'X-ray', 6.0e13: 'infrared'}[f]
        return dict(stem=f'Electromagnetic radiation has a frequency of {sf(f)} Hz. Calculate its wavelength in a vacuum.', v=C / f, unit='m', ans=f'{q(C / f, "m")} ({band})', wrongs=[f / C, C * f, 340 / f], key=f'λ = c/f (M1) = {sf(C / f)} m – {band} region (A1).')
    T = rng.choice([0, 10, 20, 30, 40]) + 273
    v = 331 * math.sqrt(T / 273)
    return dict(stem=f'The speed of sound in air is 331 m s⁻¹ at 273 K and is proportional to √T. Calculate the speed of sound on a day in {city} when the air temperature is {T - 273} °C.', v=v, unit='m s⁻¹', wrongs=[331 * T / 273, 331 + (T - 273), 331 * math.sqrt((T - 273) / 273) if T > 273 else 331 * 1.2], key=f'v = 331√({T}/273) (M1) = {sf(v)} m s⁻¹ (A1).')


R.mcqs('ch12-st4', 'C2', (1, 4), [
    ('Which list gives electromagnetic waves in order of increasing frequency?', 'Radio, infrared, ultraviolet, gamma', ['Gamma, X-ray, visible, radio', 'Infrared, radio, visible, X-ray', 'Visible, ultraviolet, infrared, gamma'], 'Frequency increases as wavelength decreases.'),
    ('A sound wave passes from air into water. Its wavelength', 'increases', ['decreases', 'stays the same', 'becomes zero'], 'Speed increases, f unchanged.'),
    ('An astronaut on the Moon cannot hear another astronaut shouting nearby because', 'there is no air to carry sound waves', ['sound is absorbed by the dust', 'their helmets reflect light', 'the Moon’s gravity is low'], 'Sound needs a medium.'),
])
