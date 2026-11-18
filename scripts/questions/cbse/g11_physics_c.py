"""CBSE class 11 physics (NCERT Physics XI) families, chapters 11-14."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, name, two_names, CITIES
from g11_physics_util import polish, sig, g, NUM, NUM2, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq, ordn

S = 'cbse-g11-physics-ch'
G = 9.8
R_ = 8.314
KB = 1.38e-23
NA = 6.02e23


# ======================================================== ch11 Thermodynamics
# st1 thermal equilibrium, zeroth law, heat, internal energy, work

c11s1_terms = term_mcq([('zeroth law of thermodynamics', 'two systems each in thermal equilibrium with a third are in thermal equilibrium with each other'),
                        ('internal energy', 'the sum of kinetic and potential energies of the molecules, in the frame of the centre of mass'),
                        ('heat', 'energy transferred because of a temperature difference'), ('work (in thermodynamics)', 'energy transferred by means other than a temperature difference, e.g. moving a piston')],
                       'Which statement describes {a}?', 'Which term is described by: {b}?', '{a}: {b}.')

c11s1_tf = tf_mcq('heat, work and internal energy',
                 ['Internal energy is a state variable.', 'Heat and work are not state variables; they depend on the path.', 'The zeroth law leads to the concept of temperature.',
                  'Work done by a gas expanding at constant pressure is PΔV.'],
                 ['Heat is a state variable.', 'A body contains a definite amount of heat.', 'Work done by a gas does not depend on the path between two states.',
                  'The zeroth law defines internal energy.'])

c11s1_explain = pool_txt([
    ('Why do we say that a body has internal energy but not "heat content"?', 'Heat is energy in transit due to a temperature difference; once transferred it becomes part of internal energy, which is a state variable.', '2 marks.'),
    ('State the zeroth law of thermodynamics and explain why it allows us to use thermometers.', 'If A and B are each in thermal equilibrium with C, they are in equilibrium with each other; the thermometer is C, so equal readings mean equal temperatures.', 'Statement (1 mark); application (1 mark).'),
    ('Explain why the work done by a gas depends on the path taken between two states.', 'Work is the area under the P-V curve, which differs for different paths between the same end points.', '2 marks.'),
])

c11s1_ar = pool_ar([
    ('Internal energy is a state variable.', 'The internal energy of a system depends only on its state, not on how it got there.', 'a', 'R explains A.'),
    ('Two bodies at the same temperature exchange no net heat when in contact.', 'Heat flows only because of a temperature difference.', 'a', 'R explains A.'),
    ('Work done by a gas is the same for every path between two states.', 'Work is the area under the P-V curve.', 'd', 'A is false; R is true and shows why it depends on path.'),
])


def c11s1_pdv(r):
    P = r.choice([1, 1.5, 2, 2.5, 3]) * 1e5
    V1 = r.choice([1, 2, 2.5, 4, 5])
    V2 = V1 + r.choice([0.5, 1, 1.5, 2, 3])
    W = P * (V2 - V1) / 1000
    return NUM(f'A gas expands at a constant pressure of {g(P)} Pa from {g(V1)} L to {g(V2)} L. How much work does it do?', W, 'J',
               f'W = PΔV = {g(P)} × ({g(V2)} − {g(V1)}) × 10⁻³ m³ = {{ans}}.', wrongs=[P * (V2 - V1), P * (V2 + V1) / 1000, P * (V2 - V1) / 100])


def c11s1_area(r):
    P1, P2 = r.choice([(1, 3), (2, 4), (1, 2), (3, 5)])
    V1, V2 = r.choice([(1, 3), (2, 5), (1, 4), (2, 6)])
    W = 0.5 * (P1 + P2) * 1e5 * (V2 - V1) * 1e-3
    return {'stem': f'A gas expands from state A ({g(P1)} × 10⁵ Pa, {V1} L) to state B ({g(P2)} × 10⁵ Pa, {V2} L) along a straight line on the P-V diagram. Find the work done by the gas.',
            'answer': f'{sig(W)} J', 'key': f'W = area under the line (trapezium) = ½(P₁ + P₂)(V₂ − V₁) = ½({P1} + {P2}) × 10⁵ × {V2 - V1} × 10⁻³ = {sig(W)} J.',
            'distractors': [f'{sig(P2 * 1e5 * (V2 - V1) * 1e-3)} J', f'{sig(P1 * 1e5 * (V2 - V1) * 1e-3)} J', f'{sig(2 * W)} J']}


def c11s1_du(r):
    Q = r.choice([200, 300, 400, 500, 800, 1000])
    W = r.choice([100, 150, 250, 300, 600, -100, -200])
    sgn = 'does' if W > 0 else 'has'
    return NUM(f'A gas is supplied {Q} J of heat and {"does " + str(W) + " J of work on its surroundings" if W > 0 else str(-W) + " J of work is done on it"}. Find the change in its internal energy.',
               Q - W, 'J', f'First law: ΔU = Q − W, where W is the work done BY the gas = {Q} − ({num(W)}) = {{ans}}.', wrongs=[Q + W, W - Q, Q], n=3)


def c11s1_simple(r):
    P = r.choice([1, 2, 5]) * 1e5
    dV = r.choice([0.01, 0.02, 0.05, 0.1])
    return NUM(f'A piston moves out so that the volume of gas in a cylinder increases by {g(dV)} m³ at a constant pressure of {g(P)} Pa. What is the work done by the gas?', P * dV, 'J',
               f'W = PΔV = {g(P)} × {g(dV)} = {{ans}}.', wrongs=[P / dV, P * dV / 2, P * dV * 10])


# st2 first law; specific heats of gases

c11s2_terms = term_mcq([('Mayer\'s relation', 'C_p − C_v = R'), ('ratio γ for a monatomic ideal gas', '5/3'), ('ratio γ for a rigid diatomic ideal gas', '7/5'),
                        ('molar specific heat C_v of a monatomic ideal gas', '(3/2)R')],
                       'What is the {a}?', 'Which quantity equals {b}?', '{a}: {b}.')

c11s2_tf = tf_mcq('the first law of thermodynamics',
                 ['ΔQ = ΔU + ΔW, where ΔW is the work done by the system.', 'The first law is a statement of conservation of energy.', 'C_p is greater than C_v for a gas.',
                  'In a cyclic process ΔU = 0.'],
                 ['The first law tells us the direction of heat flow.', 'C_v is greater than C_p for a gas.', 'In a cyclic process the net heat absorbed is zero.',
                  'The first law forbids a perpetual motion machine of the second kind.'])

c11s2_explain = pool_txt([
    ('Why is C_p greater than C_v for a gas?', 'At constant pressure part of the heat is used for work of expansion, so more heat is needed for the same temperature rise.', '2 marks.'),
    ('Show that in a cyclic process the net work done by the gas equals the net heat absorbed.', 'U returns to its initial value (ΔU = 0), so by the first law Q = W.', '2 marks.'),
    ('State the first law of thermodynamics and the sign convention used for heat and work.', 'ΔQ = ΔU + ΔW; Q positive when supplied to the system, W positive when done by the system.', 'Statement (1 mark); sign convention (1 mark).'),
])

c11s2_ar = pool_ar([
    ('C_p > C_v for an ideal gas.', 'At constant pressure the gas does work as it expands.', 'a', 'R explains A.'),
    ('In a cyclic process the change in internal energy is zero.', 'Internal energy is a state variable.', 'a', 'R explains A.'),
    ('The first law of thermodynamics tells us that heat flows from hot to cold bodies.', 'The first law is a form of the law of conservation of energy.', 'd', 'A is false (that is the second law); R is true.'),
])


def c11s2_first(r):
    n = r.choice([1, 2, 3, 0.5])
    dT = r.choice([10, 20, 25, 40, 50])
    kind, f = r.choice([('monatomic', 3), ('diatomic', 5)])
    Cv, Cp = f / 2 * R_, (f / 2 + 1) * R_
    Q = n * Cp * dT
    return {'stem': f'{g(n)} mol of an ideal {kind} gas is heated at constant pressure through {dT} K. Find the heat supplied, the increase in internal energy and the work done by the gas. (R = 8.314 J mol⁻¹ K⁻¹)',
            'answer': f'Q = {sig(Q)} J, ΔU = {sig(n * Cv * dT)} J, W = {sig(n * R_ * dT)} J',
            'key': f'C_v = {f}R/2, C_p = {f + 2}R/2. Q = nC_pΔT = {sig(Q)} J; ΔU = nC_vΔT = {sig(n * Cv * dT)} J; W = nRΔT = {sig(n * R_ * dT)} J (check: Q = ΔU + W).',
            'distractors': [f'Q = {sig(n * Cv * dT)} J, ΔU = {sig(Q)} J, W = {sig(n * R_ * dT)} J', f'Q = {sig(Q)} J, ΔU = {sig(Q)} J, W = 0 J', f'Q = {sig(n * Cv * dT)} J, ΔU = {sig(n * Cv * dT)} J, W = 0 J']}


def c11s2_iso(r):
    n = r.choice([1, 2, 0.5, 4])
    dT = r.choice([10, 20, 30, 50])
    kind, f = r.choice([('monatomic', 3), ('diatomic', 5)])
    Q = n * f / 2 * R_ * dT
    return NUM(f'How much heat is needed to raise the temperature of {g(n)} mol of an ideal {kind} gas by {dT} K in a rigid closed container? (R = 8.314 J mol⁻¹ K⁻¹)', Q, 'J',
               f'Constant volume: W = 0, Q = ΔU = nC_vΔT with C_v = {f}R/2: {g(n)} × {f / 2:g} × 8.314 × {dT} = {{ans}}.', wrongs=[n * (f / 2 + 1) * R_ * dT, n * R_ * dT, n * 1.5 * R_ * dT if f == 5 else n * 2.5 * R_ * dT])


def c11s2_basic(r):
    Q = r.choice([500, 800, 1000, 1200, 1500])
    dU = r.choice([200, 300, 400, 600])
    if dU >= Q:
        dU = Q // 2
    return NUM(f'When {Q} J of heat is supplied to a gas, its internal energy increases by {dU} J. How much work is done by the gas?', Q - dU, 'J',
               f'ΔQ = ΔU + ΔW ⇒ W = {Q} − {dU} = {{ans}}.', wrongs=[Q + dU, dU, Q])


def c11s2_mayer(r):
    Cp = r.choice([29.1, 20.8, 37.1, 33.3])
    Cv = Cp - R_
    return NUM2(f'The molar specific heat of a gas at constant pressure is {g(Cp)} J mol⁻¹ K⁻¹. Find its molar specific heat at constant volume and the ratio γ. (R = 8.314 J mol⁻¹ K⁻¹)', (Cv, Cp / Cv), ('J mol⁻¹ K⁻¹', ''),
                f'C_v = C_p − R = {g(Cp)} − 8.314 = {sig(Cv)} J mol⁻¹ K⁻¹; γ = C_p/C_v = {sig(Cp / Cv)}.', wrongs=[(Cp + R_, Cp / (Cp + R_)), (Cp / 1.4, 1.4), (Cv, Cv / Cp)])


def c11s2_cycle(r):
    P1, P2 = r.choice([(1, 2), (1, 3), (2, 4), (1, 1.5)])
    V1, V2 = r.choice([(1, 2), (2, 4), (1, 3), (2, 5)])
    W = (P2 - P1) * 1e5 * (V2 - V1) * 1e-3
    return {'stem': f'A gas is taken round a rectangular cycle on the P-V diagram: from ({g(P1)} × 10⁵ Pa, {V1} L) at constant pressure to {V2} L, then at constant volume to {g(P2)} × 10⁵ Pa, then back at constant pressure to {V1} L and at constant volume to the start. '
                    'Find the net work done by the gas, the net heat absorbed and the change in internal energy for the cycle.',
            'answer': f'W = {sig(-W)} J (net work done on the gas {sig(W)} J); Q = {sig(-W)} J; ΔU = 0',
            'key': f'Area enclosed = ΔP × ΔV = {g(P2 - P1)} × 10⁵ × {V2 - V1} × 10⁻³ = {sig(W)} J (2). The cycle runs anticlockwise (expansion at the lower pressure), so the net work by the gas is −{sig(W)} J (1). ΔU = 0, so Q = W (2).', 'gap': 'G5'}


def c11s2_fraction(r):
    kind, f = r.choice([('monatomic', 3), ('rigid diatomic', 5)])
    Q = r.choice([500, 700, 1000, 1400])
    frac = 2 / (f + 2)
    return {'stem': f'Heat of {Q} J is given to an ideal {kind} gas at constant pressure. What fraction of the heat is converted into work, and what fraction raises the internal energy? How much work is done?',
            'answer': f'Work fraction {2}/{f + 2}, internal energy fraction {f}/{f + 2}; W = {sig(Q * frac)} J',
            'key': f'Q = nC_pΔT, W = nRΔT ⇒ W/Q = R/C_p = 2/{f + 2} (2); ΔU/Q = C_v/C_p = {f}/{f + 2} (1); W = {Q} × 2/{f + 2} = {sig(Q * frac)} J (2).', 'gap': 'G5'}


c11s2_derive = pool_txt([
    ('Derive Mayer\'s relation C_p − C_v = R for one mole of an ideal gas.', 'C_p − C_v = R', 'At constant V, ΔQ = ΔU = C_vΔT (1); at constant P, ΔQ = ΔU + PΔV (1); PΔV = RΔT for 1 mol (2); C_p = C_v + R (1).'),
    ('Show that the work done by an ideal gas in an isothermal expansion from V₁ to V₂ is nRT ln(V₂/V₁).', 'W = nRT ln(V₂/V₁)', 'W = ∫P dV (1); P = nRT/V (1); integrate (2); result (1).'),
])


# st3 thermodynamic processes

PROC = [('isothermal process', 'temperature stays constant, so ΔU = 0 for an ideal gas'), ('adiabatic process', 'no heat enters or leaves the system (ΔQ = 0)'),
        ('isochoric process', 'volume stays constant, so no work is done'), ('isobaric process', 'pressure stays constant')]
c11s3_terms = term_mcq(PROC, 'In an {a},', 'In which process does this happen: {b}?', '{a}: {b}.')

c11s3_tf = tf_mcq('thermodynamic processes of an ideal gas',
                 ['In an adiabatic process PV^γ = constant.', 'In an isothermal expansion all the heat absorbed is converted into work.', 'An adiabatic curve on a P-V diagram is steeper than an isothermal curve.',
                  'In an isochoric process all the heat supplied increases the internal energy.'],
                 ['In an adiabatic process the temperature stays constant.', 'In an isothermal process no heat is exchanged.', 'An isothermal curve is steeper than an adiabatic curve.',
                  'In an isochoric process the work done is PΔV ≠ 0.'])

c11s3_explain = pool_txt([
    ('Why does air pumped quickly into a cycle tyre get warm?', 'Rapid compression is nearly adiabatic; the work done on the gas increases its internal energy and temperature.', '2 marks.'),
    ('Why is the adiabatic curve steeper than the isothermal curve through the same point?', 'Slope of adiabatic = −γP/V, of isothermal = −P/V, and γ > 1.', '2 marks.'),
    ('Why must an isothermal process be carried out slowly in a container with conducting walls?', 'So that heat can flow in or out to keep the temperature equal to that of the surroundings.', '2 marks.'),
])

c11s3_ar = pool_ar([
    ('A gas cools when it expands adiabatically.', 'In an adiabatic expansion the work is done at the expense of internal energy.', 'a', 'R explains A.'),
    ('In an isothermal process the internal energy of an ideal gas does not change.', 'The internal energy of an ideal gas depends only on its temperature.', 'a', 'R explains A.'),
    ('No work is done in an isobaric process.', 'In an isobaric process the pressure remains constant.', 'd', 'A is false (W = PΔV); R is true.'),
    ('The P-V curve of an adiabatic process is steeper than that of an isothermal process.', 'γ is greater than 1.', 'a', 'Slope ratio is γ; R explains A.'),
])


def c11s3_isowork(r):
    n = r.choice([1, 2, 0.5, 3])
    T = r.choice([300, 273, 350, 400])
    k = r.choice([2, 3, 4, 0.5])
    W = n * R_ * T * math.log(k)
    return NUM(f'{g(n)} mol of an ideal gas at {T} K {"expands" if k > 1 else "is compressed"} isothermally to {g(k) if k > 1 else "half"} {"times its initial volume" if k > 1 else "its initial volume"}. Find the work done by the gas. (R = 8.314 J mol⁻¹ K⁻¹)',
               W, 'J', f'W = nRT ln(V₂/V₁) = 2.303 nRT log₁₀({g(k)}) = 2.303 × {g(n)} × 8.314 × {T} × {num(math.log10(k), 4)} = {{ans}}.', wrongs=[n * R_ * T * math.log10(k), n * R_ * T * k, -W])


def c11s3_adia_T(r):
    T1 = r.choice([300, 280, 290, 310])
    k = r.choice([2, 4, 8])
    kind, gm = r.choice([('monatomic', 5 / 3), ('diatomic', 1.4)])
    T2 = T1 * k ** (gm - 1)
    return NUM(f'An ideal {kind} gas at {T1} K is compressed adiabatically to 1/{k} of its volume. Find its final temperature. (γ = {"5/3" if gm > 1.5 else "1.4"})', T2, 'K',
               f'TV^(γ−1) = constant ⇒ T₂ = T₁({k})^(γ−1) = {T1} × {k}^{g(gm - 1, 3)} = {{ans}}.', wrongs=[T1 * k, T1 * k ** gm, T1 / k ** (gm - 1)])


def c11s3_adia_W(r):
    n = r.choice([1, 2, 0.5])
    T1, T2 = r.choice([(500, 300), (400, 300), (600, 400), (350, 250)])
    kind, gm = r.choice([('monatomic', 5 / 3), ('diatomic', 1.4)])
    W = n * R_ * (T1 - T2) / (gm - 1)
    return NUM(f'{g(n)} mol of an ideal {kind} gas expands adiabatically and its temperature falls from {T1} K to {T2} K. Find the work done by the gas. (γ = {"5/3" if gm > 1.5 else "1.4"}, R = 8.314 J mol⁻¹ K⁻¹)', W, 'J',
               f'W = nR(T₁ − T₂)/(γ − 1) = {g(n)} × 8.314 × {T1 - T2}/{g(gm - 1, 3)} = {{ans}}.', wrongs=[n * R_ * (T1 - T2), n * R_ * (T1 - T2) * gm, n * R_ * (T1 - T2) / gm])


def c11s3_compare(r):
    P1 = r.choice([1, 2]) * 1e5
    k = r.choice([2, 3, 4])
    gm = 1.4
    return {'stem': f'Air (γ = 1.4) at {g(P1)} Pa is compressed to 1/{k} of its volume (i) isothermally and (ii) adiabatically. Find the final pressure in each case and explain why they differ.',
            'answer': f'(i) {sig(P1 * k)} Pa (ii) {sig(P1 * k ** gm)} Pa', 'key': f'(i) PV = const ⇒ P₂ = {k}P₁ = {sig(P1 * k)} Pa (1). (ii) PV^γ = const ⇒ P₂ = P₁ × {k}^1.4 = {sig(P1 * k ** gm)} Pa (1). Adiabatic compression also raises the temperature, giving a higher pressure (1).'}


c11s3_identify = pool_mcq([
    ('A gas is compressed so quickly that no heat has time to flow. The process is', 'adiabatic', ['isothermal', 'isochoric', 'isobaric'], 'No heat exchange.'),
    ('Water boiling in an open pan at atmospheric pressure is an example of a(n)', 'isobaric process', ['adiabatic process', 'isochoric process', 'cyclic process'], 'Pressure is constant (atmospheric).'),
    ('A gas is heated in a sealed rigid steel cylinder. The process is', 'isochoric', ['isobaric', 'isothermal', 'adiabatic'], 'Volume constant.'),
    ('A gas in a thin-walled metal cylinder in a large water bath is compressed very slowly. The process is nearly', 'isothermal', ['adiabatic', 'isochoric', 'free expansion'], 'Slow, good thermal contact ⇒ constant T.'),
])


# st4 heat engines, refrigerators, second law, Carnot engine

c11s4_tf = tf_mcq('heat engines and the second law',
                 ['No heat engine can have an efficiency of 100%.', 'A refrigerator transfers heat from a colder body to a hotter body using work.', 'The efficiency of a Carnot engine depends only on the temperatures of the source and sink.',
                  'No engine working between two given temperatures can be more efficient than a Carnot engine.'],
                 ['A heat engine can convert all the heat absorbed into work in a cycle.', 'Heat can flow by itself from a colder body to a hotter body.', 'The efficiency of a Carnot engine depends on the working substance.',
                  'A refrigerator works without any external work.'])

c11s4_terms = term_mcq([('Kelvin-Planck statement', 'no process is possible whose sole result is the absorption of heat from a reservoir and its complete conversion into work'),
                        ('Clausius statement', 'no process is possible whose sole result is the transfer of heat from a colder object to a hotter object'),
                        ('efficiency of a heat engine', 'η = W/Q₁ = 1 − Q₂/Q₁'), ('coefficient of performance of a refrigerator', 'α = Q₂/W')],
                       'Which of the following is the {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c11s4_explain = pool_txt([
    ('Why can no heat engine have an efficiency of 100%?', 'Some heat must always be rejected to a sink (Kelvin-Planck statement of the second law).', '2 marks.'),
    ('Why does the room get warmer if the door of a working refrigerator is kept open?', 'The refrigerator releases Q₁ = Q₂ + W to the room; with the door open it takes Q₂ from the same room, so the room gains W.', '2 marks.'),
    ('Name the four steps of a Carnot cycle.', 'Isothermal expansion at T₁, adiabatic expansion to T₂, isothermal compression at T₂, adiabatic compression to T₁.', '½ mark each.'),
])

c11s4_ar = pool_ar([
    ('The efficiency of a Carnot engine can never be 100%.', 'For 100% efficiency the sink would have to be at 0 K.', 'a', 'η = 1 − T₂/T₁ < 1 unless T₂ = 0; R explains A.'),
    ('A refrigerator kept open in a closed room warms the room.', 'Heat rejected by the refrigerator exceeds the heat it extracts.', 'a', 'R explains A.'),
    ('The efficiency of a Carnot engine depends on the working substance.', 'A Carnot engine is reversible.', 'd', 'A is false; R is true.'),
])


def c11s4_eff(r):
    Q1 = r.choice([1000, 1500, 2000, 2500, 4000])
    W = r.choice([200, 300, 400, 500, 600, 800])
    if W >= Q1:
        W = Q1 // 4
    return NUM(f'A heat engine absorbs {Q1} J of heat from the source and does {W} J of work in each cycle. Find its efficiency and the heat rejected to the sink.', W / Q1 * 100, '%',
               f'η = W/Q₁ = {W}/{Q1} = {{ans}}; Q₂ = Q₁ − W = {Q1 - W} J.', wrongs=[(Q1 - W) / Q1 * 100, W / (Q1 - W) * 100, Q1 / W]) | {'answer': f'{sig(W / Q1 * 100)}%; {Q1 - W} J',
                                                                                                                           'distractors': [f'{sig((Q1 - W) / Q1 * 100)}%; {W} J', f'{sig(W / (Q1 - W) * 100)}%; {Q1 - W} J', f'{sig(W / Q1 * 100)}%; {Q1 + W} J']}


def c11s4_carnot(r):
    t1, t2 = r.choice([(227, 27), (327, 27), (127, 27), (500, 100), (400, 0), (627, 27)])
    T1, T2 = t1 + 273, t2 + 273
    return NUM(f'A Carnot engine works between a source at {t1} °C and a sink at {t2} °C. Find its efficiency.', (1 - T2 / T1) * 100, '%',
               f'η = 1 − T₂/T₁ = 1 − {T2}/{T1} = {{ans}} (temperatures in kelvin).', wrongs=[(1 - t2 / t1) * 100, T2 / T1 * 100, (t1 - t2) / t1 * 50])


def c11s4_fridge(r):
    t2, t1 = r.choice([(-13, 27), (-23, 27), (-3, 37), (-18, 32), (4, 30)])
    T1, T2 = t1 + 273, t2 + 273
    a = T2 / (T1 - T2)
    Q2 = r.choice([300, 500, 600, 1000])
    return {'stem': f'A refrigerator keeps its freezer at {num(t2)} °C in a kitchen at {t1} °C. Treating it as an ideal (Carnot) refrigerator, find its coefficient of performance and the work needed to remove {Q2} J of heat from the freezer.',
            'answer': f'α = {sig(a)}; W = {sig(Q2 / a)} J', 'key': f'α = T₂/(T₁ − T₂) = {T2}/{T1 - T2} = {sig(a)} (2); W = Q₂/α = {sig(Q2 / a)} J (1).'}


def c11s4_raise(r):
    t2 = r.choice([27, 7, 17])
    T2 = t2 + 273
    e1, e2 = r.choice([(0.4, 0.5), (0.3, 0.4), (0.5, 0.6), (0.25, 0.5)])
    T1 = T2 / (1 - e1)
    T1n = T2 / (1 - e2)
    return {'stem': f'A Carnot engine with its sink at {t2} °C has an efficiency of {int(e1 * 100)}%. By how many degrees must the source temperature be raised to increase the efficiency to {int(e2 * 100)}%?',
            'answer': f'{sig(T1n - T1)} K', 'key': f'T₁ = T₂/(1 − η) = {T2}/{g(1 - e1)} = {sig(T1)} K (1.5); new T₁ = {T2}/{g(1 - e2)} = {sig(T1n)} K (1.5); rise = {sig(T1n - T1)} K (1).'}


def c11s4_reject(r):
    Q1 = r.choice([800, 1200, 1500, 2000])
    eta = r.choice([20, 25, 30, 40])
    return NUM(f'An engine of efficiency {eta}% absorbs {Q1} J of heat per cycle. How much heat does it reject per cycle?', Q1 * (1 - eta / 100), 'J',
               f'W = ηQ₁ = {g(Q1 * eta / 100)} J; Q₂ = Q₁ − W = {{ans}}.', wrongs=[Q1 * eta / 100, Q1 * (1 + eta / 100), Q1 / (eta / 100)])


def c11s4_case(r):
    who = name(r)
    t1, t2 = r.choice([(327, 27), (427, 27), (227, 27)])
    Q1 = r.choice([5000, 8000, 10000])
    eta_c = 1 - (t2 + 273) / (t1 + 273)
    act = round(eta_c * r.choice([0.5, 0.6]), 3)
    return {'stem': (f'{who} reads that a power-plant steam engine takes in steam at {t1} °C and condenses it at {t2} °C. In each cycle it absorbs {Q1} J. Its actual efficiency is {g(act * 100, 1)}%.\n'
                     '(i) Find the Carnot (maximum) efficiency. (ii) Find the work done per cycle. (iii) Find the heat rejected per cycle. (iv) Why is the actual efficiency less than the Carnot value?'),
            'answer': f'(i) {sig(eta_c * 100)}% (ii) {sig(act * Q1)} J (iii) {sig(Q1 - act * Q1)} J (iv) real engines are irreversible: friction, heat losses',
            'key': f'(i) 1 − T₂/T₁ (1). (ii) ηQ₁ (1). (iii) Q₁ − W (1). (iv) irreversibility (1).'}


# ======================================================== ch12 Kinetic Theory
# st1 molecular nature of matter; ideal gas equation

c12s1_terms = term_mcq([('Boyle\'s law', 'PV = constant at constant temperature'), ('Charles\' law', 'V/T = constant at constant pressure'),
                        ('Avogadro\'s hypothesis', 'equal volumes of all gases at the same T and P contain equal numbers of molecules'),
                        ('Dalton\'s law of partial pressures', 'the total pressure of a mixture of ideal gases is the sum of the partial pressures')],
                       'Which statement is {a}?', 'Which law states: {b}?', '{a}: {b}.')

c12s1_tf = tf_mcq('ideal gases',
                 ['Real gases behave most like ideal gases at low pressure and high temperature.', 'One mole of any ideal gas at STP occupies about 22.4 L.', 'PV = nRT = Nk_BT.',
                  'k_B = R/N_A.'],
                 ['Real gases behave most like ideal gases at high pressure and low temperature.', 'One mole of an ideal gas at STP occupies 1 m³.', 'The gas constant R depends on the gas.',
                  'Boyle\'s law holds at constant pressure.'])

c12s1_explain = pool_txt([
    ('Why do real gases deviate from ideal behaviour at high pressures and low temperatures?', 'Molecules come close: their own volume and intermolecular attractions are no longer negligible.', '2 marks.'),
    ('Use the ideal gas equation to show Avogadro\'s hypothesis.', 'PV = Nk_BT ⇒ N = PV/(k_BT): same P, V, T gives the same N for any gas.', '2 marks.'),
    ('Why does an air bubble grow as it rises from the bottom of a lake?', 'Pressure decreases as it rises (and temperature may rise), so by PV/T = constant its volume increases.', '2 marks.'),
])

c12s1_ar = pool_ar([
    ('Real gases approach ideal behaviour at low pressure.', 'At low pressure molecules are far apart and intermolecular forces are negligible.', 'a', 'R explains A.'),
    ('Equal volumes of hydrogen and oxygen at the same T and P contain the same number of molecules.', 'PV = Nk_BT for any ideal gas.', 'a', 'R explains A.'),
    ('An air bubble shrinks as it rises to the surface of a lake.', 'Pressure decreases as we go up in a liquid.', 'd', 'A is false (it grows); R is true.'),
])


def c12s1_n(r):
    P = r.choice([1.01e5, 2e5, 1.5e5, 3e5])
    V = r.choice([1, 2, 5, 10, 20]) * 1e-3
    T = r.choice([273, 300, 320, 350])
    n = P * V / (R_ * T)
    return NUM2(f'A cylinder of volume {g(V * 1000)} L contains an ideal gas at {g(P)} Pa and {T} K. Find the number of moles and the number of molecules. (R = 8.314 J mol⁻¹ K⁻¹, N_A = 6.02 × 10²³ mol⁻¹)', (n, n * NA), ('mol', 'molecules'),
                f'n = PV/RT = {g(P)} × {g(V)}/(8.314 × {T}) = {sig(n)} mol (2); N = nN_A = {sig(n * NA)} (1).', wrongs=[(P * V * 1000 / (R_ * T), P * V * 1000 / (R_ * T) * NA), (P * V / T, P * V / T * NA), (n, n / NA)])


def c12s1_boyle(r):
    P1 = r.choice([1, 1.5, 2, 3]) * 1e5
    V1 = r.choice([2, 3, 4, 6, 8])
    V2 = r.choice([1, 1.5, 2, 2.5])
    if V2 >= V1:
        V2 = V1 / 2
    return NUM(f'A gas occupies {V1} L at {g(P1)} Pa. It is compressed at constant temperature to {g(V2)} L. Find the new pressure.', P1 * V1 / V2, 'Pa',
               f'Boyle\'s law: P₁V₁ = P₂V₂ ⇒ P₂ = {g(P1)} × {V1}/{g(V2)} = {{ans}}.', wrongs=[P1 * V2 / V1, P1 * (V1 - V2), P1])


def c12s1_bubble(r):
    h = r.choice([20, 30, 40, 50])
    t1, t2 = r.choice([(12, 35), (10, 30), (7, 27), (15, 32)])
    V1 = r.choice([1, 1.5, 2, 0.5])
    P0 = 1.01e5
    P1 = P0 + 1000 * G * h
    V2 = V1 * P1 / P0 * (t2 + 273) / (t1 + 273)
    return {'stem': f'An air bubble of volume {g(V1)} cm³ rises from the bottom of a lake {h} m deep, where the temperature is {t1} °C, to the surface, where the temperature is {t2} °C. Find its volume at the surface. (P_atm = 1.01 × 10⁵ Pa, density of water 1000 kg m⁻³, g = 9.8 m s⁻²)',
            'answer': f'{sig(V2)} cm³', 'key': f'P₁ = P₀ + ρgh = {sig(P1)} Pa (1); P₁V₁/T₁ = P₂V₂/T₂ with T₁ = {t1 + 273} K, T₂ = {t2 + 273} K (1); V₂ = {sig(V2)} cm³ (1).', 'gap': 'G7'}


def c12s1_stp(r):
    V = r.choice([1, 2.24, 5.6, 11.2, 22.4, 44.8])
    return NUM(f'How many molecules are there in {g(V)} L of an ideal gas at STP? (molar volume at STP = 22.4 L, N_A = 6.02 × 10²³ mol⁻¹)', V / 22.4 * NA, '',
               f'n = {g(V)}/22.4 = {g(V / 22.4, 4)} mol; N = nN_A = {{ans}}.', wrongs=[V * NA, V * 22.4 * NA, NA / V])


def c12s1_dalton(r):
    V = r.choice([10, 20, 25]) * 1e-3
    T = r.choice([300, 290, 310])
    n1, n2 = r.choice([(0.2, 0.3), (0.5, 0.25), (0.1, 0.4), (1, 0.5)])
    P1, P2 = n1 * R_ * T / V, n2 * R_ * T / V
    return {'stem': f'A {g(V * 1000)} L vessel at {T} K contains {g(n1)} mol of oxygen and {g(n2)} mol of nitrogen. Find the partial pressure of each gas and the total pressure. (R = 8.314 J mol⁻¹ K⁻¹)',
            'answer': f'p(O₂) = {sig(P1)} Pa, p(N₂) = {sig(P2)} Pa, total {sig(P1 + P2)} Pa',
            'key': f'p = nRT/V for each gas (2): {sig(P1)} Pa and {sig(P2)} Pa; total (Dalton) = {sig(P1 + P2)} Pa (1).'}


# st2 kinetic theory: pressure and kinetic interpretation of temperature

c12s2_tf = tf_mcq('the kinetic theory of an ideal gas',
                 ['The average kinetic energy of a molecule is (3/2)k_BT.', 'At the same temperature, lighter molecules have a larger r.m.s. speed.', 'The pressure of a gas is P = (1/3)ρv²_rms.',
                  'Temperature is a measure of the average kinetic energy of the molecules.'],
                 ['The average kinetic energy of a molecule depends on its mass at a given temperature.', 'At the same temperature, heavier molecules have a larger r.m.s. speed.',
                  'The r.m.s. speed is proportional to T.', 'The pressure of a gas is (1/3)ρv_rms.'])

c12s2_terms = term_mcq([('r.m.s. speed of molecules', '√(3RT/M) = √(3k_BT/m)'), ('average kinetic energy per molecule', '(3/2)k_BT'), ('pressure of an ideal gas', '(1/3)nm v̄², i.e. (1/3)ρv²_rms'),
                        ('total translational kinetic energy of one mole', '(3/2)RT')],
                       'The {a} is given by', 'Which quantity equals {b}?', '{a} = {b}.')

c12s2_explain = pool_txt([
    ('Why does a gas exert pressure on the walls of its container, according to kinetic theory?', 'Molecules keep colliding elastically with the walls; each collision transfers momentum, and the rate of momentum transfer per unit area is the pressure.', '2 marks.'),
    ('At the same temperature, hydrogen and oxygen molecules have the same average kinetic energy but different speeds. Explain.', 'Average KE (3/2)k_BT is the same, so lighter H₂ molecules (smaller m) must move faster: v_rms ∝ 1/√m.', '2 marks.'),
    ('Why is hydrogen rare in the Earth\'s atmosphere?', 'Its light molecules have high r.m.s. speeds; a fraction exceeds the escape speed and leaks into space over time.', '2 marks.'),
])

c12s2_ar = pool_ar([
    ('At the same temperature, hydrogen molecules move faster on average than oxygen molecules.', 'v_rms ∝ 1/√M at a given temperature.', 'a', 'R explains A.'),
    ('The average kinetic energy of the molecules of a gas depends only on its absolute temperature.', 'Average KE per molecule = (3/2)k_BT.', 'a', 'R explains A.'),
    ('Doubling the absolute temperature of a gas doubles the r.m.s. speed of its molecules.', 'v_rms ∝ √T.', 'd', 'A is false (it becomes √2 times); R is true.'),
])

GASES = [('hydrogen', 2e-3), ('helium', 4e-3), ('nitrogen', 28e-3), ('oxygen', 32e-3), ('argon', 40e-3), ('carbon dioxide', 44e-3)]


def c12s2_vrms(r):
    gas, M = r.choice(GASES)
    T = r.choice([273, 300, 350, 400, 500])
    v = math.sqrt(3 * R_ * T / M)
    return NUM(f'Find the r.m.s. speed of {gas} molecules at {T} K. (Molar mass = {g(M * 1000)} g mol⁻¹, R = 8.314 J mol⁻¹ K⁻¹)', v, 'm s⁻¹',
               f'v_rms = √(3RT/M) = √(3 × 8.314 × {T}/{g(M)}) = {{ans}}.', wrongs=[math.sqrt(3 * R_ * T / (M * 1000)), math.sqrt(R_ * T / M), 3 * R_ * T / M / 100])


def c12s2_ratio(r):
    (g1, M1), (g2, M2) = r.sample(GASES, 2)
    return NUM(f'At the same temperature, what is the ratio of the r.m.s. speed of {g1} molecules to that of {g2} molecules?', math.sqrt(M2 / M1), '',
               f'v_rms ∝ 1/√M ⇒ v₁/v₂ = √(M₂/M₁) = √({g(M2 * 1000)}/{g(M1 * 1000)}) = {{ans}}.', wrongs=[M2 / M1, math.sqrt(M1 / M2), M1 / M2])


def c12s2_sameT(r):
    (g1, M1), (g2, M2) = r.sample(GASES, 2)
    T1 = r.choice([273, 300, 320])
    T2 = T1 * M2 / M1
    return NUM(f'At what temperature is the r.m.s. speed of {g2} molecules equal to that of {g1} molecules at {T1} K?', T2, 'K',
               f'√(3RT₂/M₂) = √(3RT₁/M₁) ⇒ T₂ = T₁M₂/M₁ = {T1} × {g(M2 * 1000)}/{g(M1 * 1000)} = {{ans}}.', wrongs=[T1 * M1 / M2, T1 * math.sqrt(M2 / M1), T1])


def c12s2_ke(r):
    T = r.choice([273, 300, 400, 600, 1000])
    n = r.choice([1, 2, 0.5])
    e = 1.5 * KB * T
    return NUM2(f'Find (i) the average translational kinetic energy of a gas molecule at {T} K and (ii) the total translational kinetic energy of {g(n)} mol of the gas. (k_B = 1.38 × 10⁻²³ J K⁻¹, R = 8.314 J mol⁻¹ K⁻¹)', (e, 1.5 * n * R_ * T),
                ('J', 'J'), f'(i) (3/2)k_BT = {sig(e)} J (1.5); (ii) (3/2)nRT = {sig(1.5 * n * R_ * T)} J (1.5).', wrongs=[(KB * T, n * R_ * T), (3 * KB * T, 3 * n * R_ * T), (0.5 * KB * T, 0.5 * n * R_ * T)])


def c12s2_pressure(r):
    rho = r.choice([0.09, 1.25, 1.43, 0.18])
    v = r.choice([400, 480, 500, 1300, 1840])
    P = rho * v * v / 3
    return NUM(f'A gas of density {g(rho)} kg m⁻³ has molecules with an r.m.s. speed of {v} m s⁻¹. Find the pressure it exerts.', P, 'Pa', f'P = (1/3)ρv²_rms = (1/3) × {g(rho)} × {v}² = {{ans}}.',
               wrongs=[rho * v * v, rho * v / 3, rho * v * v / 2])


def c12s2_escape(r):
    gas, M = r.choice(GASES[:3])
    ve = 11.2e3
    T = M * ve * ve / (3 * R_)
    return {'stem': f'At what temperature would the r.m.s. speed of {gas} molecules equal the escape speed from the Earth (11.2 km s⁻¹)? Comment on why {gas} is (or is not) common in our atmosphere. (M = {g(M * 1000)} g mol⁻¹, R = 8.314 J mol⁻¹ K⁻¹)',
            'answer': f'{sig(T)} K', 'key': f'√(3RT/M) = 11.2 × 10³ ⇒ T = Mv²/3R = {g(M)} × (1.12 × 10⁴)²/(3 × 8.314) = {sig(T)} K (3). Even at ~300 K some molecules in the tail of the speed distribution exceed v_e; this is much easier for light molecules, so H₂ and He escape over geological time (2).', 'gap': 'G5'}


c12s2_derive = pool_txt([
    ('Derive the expression P = (1/3)nm v̄² for the pressure of an ideal gas on the basis of kinetic theory.', 'P = (1/3)nm v̄²',
     'Momentum change 2mv_x per collision with a wall (1); number of collisions in Δt: ½ n A v_x Δt counting both directions (1); force = n m v_x² A (1); isotropy v_x² = v̄²/3 (1); P = (1/3)nm v̄² (1).'),
    ('Using kinetic theory, show that the average kinetic energy of a molecule is (3/2)k_BT.', 'Ē = (3/2)k_BT', 'PV = (1/3)Nm v̄² (2); compare with PV = Nk_BT (2); ½m v̄² = (3/2)k_BT (1).'),
])


def c12s2_case(r):
    who = name(r)
    T1, T2 = r.choice([(300, 600), (300, 1200), (273, 546)])
    return {'stem': (f'{who} studies a cylinder of oxygen (M = 32 g mol⁻¹) at {T1} K. It is then heated to {T2} K at constant volume. (R = 8.314 J mol⁻¹ K⁻¹, k_B = 1.38 × 10⁻²³ J K⁻¹)\n'
                     '(i) Find v_rms at {T1} K. (ii) By what factor does v_rms change on heating? (iii) By what factor does the pressure change? (iv) Find the average KE per molecule at {T2} K.').replace('{T1}', str(T1)).replace('{T2}', str(T2)),
            'answer': f'(i) {sig(math.sqrt(3 * R_ * T1 / 0.032))} m s⁻¹ (ii) {sig(math.sqrt(T2 / T1))} (iii) {g(T2 / T1)} (iv) {sig(1.5 * KB * T2)} J',
            'key': f'(i) √(3RT/M) (1). (ii) √(T₂/T₁) (1). (iii) P ∝ T at constant V (1). (iv) (3/2)k_BT (1).'}


# st3 equipartition of energy; specific heats

c12s3_terms = term_mcq([('degrees of freedom of a monatomic gas molecule', '3 (translational only)'), ('degrees of freedom of a rigid diatomic molecule', '5 (3 translational + 2 rotational)'),
                        ('law of equipartition of energy', 'each degree of freedom gets ½k_BT of energy on average'), ('C_v of a rigid diatomic gas', '(5/2)R')],
                       'What are/is the {a}?', 'Which quantity is {b}?', '{a}: {b}.')

c12s3_tf = tf_mcq('equipartition of energy',
                 ['Each translational or rotational degree of freedom contributes ½k_BT to the average energy.', 'A vibrational mode contributes k_BT (kinetic and potential).', 'For a monatomic ideal gas γ = 5/3.',
                  'For a rigid diatomic gas C_p = (7/2)R.'],
                 ['A monatomic molecule has 5 degrees of freedom.', 'Each degree of freedom contributes k_BT/4.', 'For a monatomic ideal gas γ = 7/5.', 'For a rigid diatomic gas C_v = (3/2)R.'])

c12s3_explain = pool_txt([
    ('Why is the molar specific heat C_v of a diatomic gas larger than that of a monatomic gas?', 'A diatomic molecule also has rotational degrees of freedom that store energy, so more heat is needed per kelvin.', '2 marks.'),
    ('Use the law of equipartition to find γ for a monatomic gas.', 'U = (3/2)RT ⇒ C_v = (3/2)R, C_p = (5/2)R, γ = 5/3.', '2 marks.'),
])

c12s3_ar = pool_ar([
    ('γ for helium is greater than γ for nitrogen.', 'Helium molecules have fewer degrees of freedom than nitrogen molecules.', 'a', 'γ = 1 + 2/f; R explains A.'),
    ('The molar specific heat of a monatomic gas at constant volume is (3/2)R.', 'A monatomic molecule has three translational degrees of freedom.', 'a', 'R explains A.'),
    ('A rigid diatomic molecule has 6 degrees of freedom.', 'It can rotate about two axes perpendicular to its length.', 'd', 'A is false (it has 5); R is true.'),
])


def c12s3_cv(r):
    kind, f = r.choice([('monatomic', 3), ('rigid diatomic', 5), ('non-linear rigid polyatomic', 6)])
    Cv, Cp = f / 2 * R_, (f / 2 + 1) * R_
    return NUM2(f'Using the law of equipartition, find C_v, C_p and γ for an ideal {kind} gas. (R = 8.314 J mol⁻¹ K⁻¹)', (Cv, Cp, Cp / Cv), ('J mol⁻¹ K⁻¹', 'J mol⁻¹ K⁻¹', ''),
                f'f = {f}; U = (f/2)RT per mole ⇒ C_v = (f/2)R = {sig(Cv)}, C_p = C_v + R = {sig(Cp)} J mol⁻¹ K⁻¹, γ = 1 + 2/f = {sig(Cp / Cv)}.',
                wrongs=[(Cp, Cv, Cv / Cp), ((f - 1) / 2 * R_, (f + 1) / 2 * R_, (f + 1) / (f - 1)), (Cv, Cp, 1.4 if f != 5 else 5 / 3)])


def c12s3_U(r):
    kind, f = r.choice([('monatomic', 3), ('rigid diatomic', 5)])
    n = r.choice([1, 2, 3, 0.5])
    T = r.choice([300, 273, 400])
    return NUM(f'Find the total internal energy of {g(n)} mol of an ideal {kind} gas at {T} K. (R = 8.314 J mol⁻¹ K⁻¹)', n * f / 2 * R_ * T, 'J',
               f'U = n(f/2)RT with f = {f}: {g(n)} × {f / 2:g} × 8.314 × {T} = {{ans}}.', wrongs=[n * 1.5 * R_ * T if f == 5 else n * 2.5 * R_ * T, n * R_ * T, n * f * R_ * T])


def c12s3_mix(r):
    n1, n2 = r.choice([(1, 1), (2, 1), (1, 2), (3, 2), (1, 3)])
    Cv = (n1 * 1.5 + n2 * 2.5) * R_ / (n1 + n2)
    gm = (Cv + R_) / Cv
    return {'stem': f'A mixture contains {n1} mol of helium (monatomic) and {n2} mol of oxygen (rigid diatomic). Find C_v of the mixture per mole and its γ. (R = 8.314 J mol⁻¹ K⁻¹)',
            'answer': f'C_v = {sig(Cv)} J mol⁻¹ K⁻¹; γ = {sig(gm)}', 'key': f'C_v(mix) = [{n1}(3R/2) + {n2}(5R/2)]/{n1 + n2} = {sig(Cv)} J mol⁻¹ K⁻¹ (2); C_p = C_v + R; γ = {sig(gm)} (1).', 'gap': 'G5'}


c12s3_short = pool_mcq([
    ('The number of degrees of freedom of a helium atom is', '3', ['5', '6', '7'], 'Only three translational degrees of freedom.'),
    ('The number of degrees of freedom of a rigid oxygen molecule at room temperature is', '5', ['3', '6', '7'], '3 translational + 2 rotational.'),
    ('For a rigid diatomic ideal gas, γ equals', '1.4', ['1.67', '1.33', '1.0'], 'γ = 1 + 2/5.'),
    ('According to equipartition, the average energy per molecule of a monatomic gas is', '(3/2)k_BT', ['(5/2)k_BT', 'k_BT', '3k_BT'], 'Three degrees of freedom × ½k_BT.'),
])


# st4 mean free path

c12s4_tf = tf_mcq('the mean free path of gas molecules',
                 ['Mean free path increases when the gas density decreases.', 'Mean free path is inversely proportional to the square of the molecular diameter.', 'At a fixed temperature, halving the pressure doubles the mean free path.',
                  'l = 1/(√2 nπd²).'],
                 ['Mean free path increases with pressure at a fixed temperature.', 'Mean free path is proportional to the molecular diameter.', 'Mean free path does not depend on the number density.',
                  'Larger molecules have a longer mean free path.'])

c12s4_explain = pool_txt([
    ('Why does the smell of a perfume take time to reach the other end of a room, even though molecular speeds are hundreds of m s⁻¹?', 'Molecules collide very frequently (mean free path is tiny), so they follow a zig-zag path and diffuse slowly.', '2 marks.'),
    ('How does the mean free path depend on pressure and temperature?', 'l = k_BT/(√2πd²P): it increases with T and decreases with P.', '2 marks.'),
])

c12s4_ar = pool_ar([
    ('The mean free path of air molecules is larger at high altitudes.', 'The number density of molecules is smaller at high altitudes.', 'a', 'l ∝ 1/n; R explains A.'),
    ('Perfume smell spreads slowly in still air.', 'Gas molecules travel only a very short distance between collisions.', 'a', 'R explains A.'),
    ('The mean free path is independent of the size of the molecules.', 'l = 1/(√2 nπd²).', 'd', 'A is false; R is true.'),
])


def c12s4_mfp(r):
    n = r.choice([2.7e25, 2.5e25, 1e25, 3e24])
    d = r.choice([2, 2.5, 3, 3.5]) * 1e-10
    l = 1 / (math.sqrt(2) * n * math.pi * d * d)
    return NUM(f'Estimate the mean free path of molecules in a gas with number density {g(n)} m⁻³ if the molecular diameter is {g(d * 1e10)} Å.', l, 'm',
               f'l = 1/(√2 nπd²) = 1/(1.414 × {g(n)} × π × ({g(d)})²) = {{ans}}.', wrongs=[1 / (n * math.pi * d * d), 1 / (math.sqrt(2) * n * d), l * 2])


def c12s4_pt(r):
    P = r.choice([1.01e5, 1e5, 2e5, 1e3])
    T = r.choice([273, 300, 373])
    d = 3e-10
    n = P / (KB * T)
    l = 1 / (math.sqrt(2) * n * math.pi * d * d)
    return NUM2(f'Nitrogen (molecular diameter ≈ 3 Å) is at {g(P)} Pa and {T} K. Find the number density of molecules and the mean free path. (k_B = 1.38 × 10⁻²³ J K⁻¹)', (n, l), ('m⁻³', 'm'),
                f'n = P/(k_BT) = {sig(n)} m⁻³ (1); l = 1/(√2 nπd²) = {sig(l)} m (2).', wrongs=[(P / (R_ * T), 1 / (math.sqrt(2) * P / (R_ * T) * math.pi * d * d)), (n, 1 / (n * math.pi * d * d)), (n * 2, l / 2)])


def c12s4_factor(r):
    fp, ft = r.choice([(2, 1), (0.5, 1), (1, 2), (2, 2), (4, 2)])
    f = ft / fp
    ch = []
    if fp != 1:
        ch.append(f'pressure is made {g(fp)} times')
    if ft != 1:
        ch.append(f'absolute temperature is made {g(ft)} times')
    return NUM(f'By what factor does the mean free path of a gas change if its {" and its ".join(ch)}?', f, '', f'l = k_BT/(√2πd²P) ∝ T/P ⇒ factor = {g(ft)}/{g(fp)} = {{ans}}.', wrongs=[fp / ft, ft * fp, math.sqrt(f)])


def c12s4_nd(r):
    l = r.choice([60, 68, 75, 90, 100, 120])
    k = r.choice([2, 3, 4, 5])
    up = r.random() < 0.5
    f = 1 / k if up else k
    word = f'increased {k} times' if up else f'reduced to 1/{k} of its value'
    return NUM(f'The mean free path of molecules of a gas is {l} nm. If the number density of molecules is {word} (molecular size unchanged), what is the new mean free path?',
               l * f, 'nm', f'l ∝ 1/n, so l\' = {l} × {"1/" + str(k) if up else k} = {{ans}}.', wrongs=[l / f, l * f * f, float(l)])


# ======================================================== ch13 Oscillations
# st1 periodic motion; SHM and its equation

c13s1_terms = term_mcq([('period', 'the time taken for one complete oscillation'), ('frequency', 'the number of oscillations per second'), ('amplitude', 'the maximum displacement from the mean position'),
                        ('phase', 'the argument (ωt + φ) that fixes the state of motion at time t'), ('angular frequency', 'ω = 2π/T')],
                       'In SHM, what is meant by the {a}?', 'Which term is {b}?', '{a}: {b}.')

c13s1_tf = tf_mcq('simple harmonic motion',
                 ['Every SHM is periodic, but every periodic motion is not SHM.', 'In SHM the restoring force is proportional to the displacement and opposite to it.', 'x = A cos(ωt + φ) represents SHM.',
                  'The period of SHM does not depend on the amplitude.'],
                 ['Every periodic motion is simple harmonic.', 'In SHM the restoring force is proportional to the square of the displacement.', 'The period of SHM increases with amplitude.',
                  'The motion of the Earth round the Sun is SHM.'])

c13s1_explain = pool_txt([
    ('Is the motion of the hands of a clock periodic? Is it oscillatory? Explain.', 'Periodic, but not oscillatory: the hands go round, they do not move to and fro about a mean position.', '2 marks.'),
    ('Show that the projection of uniform circular motion on a diameter is SHM.', 'x = A cos(ωt + φ) for the foot of the perpendicular, which is the SHM equation.', '2 marks.'),
    ('Why is the motion of a ball bouncing elastically on the floor periodic but not simple harmonic?', 'Its acceleration is g (constant) during flight, not proportional to displacement from a mean position.', '2 marks.'),
])

c13s1_ar = pool_ar([
    ('The motion of a simple pendulum for small angles is simple harmonic.', 'For small angles the restoring torque is proportional to the angular displacement.', 'a', 'R explains A.'),
    ('Every periodic motion is simple harmonic.', 'SHM is periodic.', 'd', 'A is false; R is true.'),
    ('sin ωt + cos ωt represents SHM.', 'It can be written as √2 sin(ωt + π/4).', 'a', 'R explains A.'),
])

c13s1_which = pool_mcq([
    ('Which of the following functions of time represents simple harmonic motion?', 'sin ωt − cos ωt', ['sin²ωt', 'e^(−ωt)', 'log(ωt)'], 'sin ωt − cos ωt = √2 sin(ωt − π/4).'),
    ('Which function of time represents periodic but not simple harmonic motion?', 'sin ωt + cos 2ωt', ['3 cos(π/4 − 2ωt)', 'sin ωt', 'cos ωt + sin ωt'], 'Two different frequencies: periodic (period 2π/ω) but not SHM.'),
    ('Which function of time is non-periodic?', 'e^(−ω²t²)', ['sin 3ωt', 'cos ωt + 2 sin ωt', 'sin² ωt'], 'An exponential decay never repeats.'),
    ('Which of these represents SHM?', '3 cos(π/4 − 2ωt)', ['sin²ωt', 'ωt', 'e^(ωt)'], 'It is a single cosine of a linear function of time.'),
])


def c13s1_read(r):
    A = r.choice([2, 3, 4, 5, 0.05, 0.1])
    w = r.choice([math.pi, 2 * math.pi, 4 * math.pi, math.pi / 2, 10])
    phi = r.choice([0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2])
    wn = {math.pi: 'π', 2 * math.pi: '2π', 4 * math.pi: '4π', math.pi / 2: 'π/2', 10: '10'}[w]
    pn = {0: '', math.pi / 6: ' + π/6', math.pi / 4: ' + π/4', math.pi / 3: ' + π/3', math.pi / 2: ' + π/2'}[phi]
    T = 2 * math.pi / w
    return {'stem': f'The displacement of a particle in SHM is x = {g(A)} cos({'(π/2)' if wn == 'π/2' else wn}t{pn}) (x in m, t in s). Find the amplitude, angular frequency, period and initial phase.',
            'answer': f'A = {g(A)} m, ω = {wn} rad s⁻¹, T = {sig(T)} s, φ = {pn[3:] if pn else "0"}',
            'key': f'Compare with x = A cos(ωt + φ): A = {g(A)} m, ω = {wn} rad s⁻¹, T = 2π/ω = {sig(T)} s, φ = {pn[3:] if pn else "0"}.',
            'distractors': [f'A = {g(2 * A)} m, ω = {wn} rad s⁻¹, T = {sig(T)} s, φ = {pn[3:] if pn else "0"}', f'A = {g(A)} m, ω = {wn} rad s⁻¹, T = {sig(1 / T)} s, φ = {pn[3:] if pn else "0"}', f'A = {g(A)} m, ω = {sig(w / (2 * math.pi))} rad s⁻¹, T = {sig(w)} s, φ = 0']}


def c13s1_x(r):
    A = r.choice([2, 4, 5, 10])
    T = r.choice([2, 4, 6, 8, 12])
    t = r.choice([x for x in (0.5, 1, 1.5, 2, 3) if x < T])
    x = A * math.cos(2 * math.pi * t / T)
    return NUM(f'A particle executes SHM with amplitude {A} cm and period {T} s, starting from the positive extreme at t = 0. Find its displacement at t = {g(t)} s.', x, 'cm',
               f'x = A cos(2πt/T) = {A} cos(2π × {g(t)}/{T}) = {A} cos({g(360 * t / T)}°) = {{ans}}.', wrongs=[A * math.sin(2 * math.pi * t / T), A * math.cos(math.pi * t / T), A * t / T], n=3)


def c13s1_TF(r):
    f_ = r.choice([0.5, 2, 5, 50, 256, 440])
    return NUM(f'A tuning fork vibrates with a frequency of {g(f_)} Hz. What is its period of vibration?', 1 / f_, 's', f'T = 1/ν = 1/{g(f_)} = {{ans}}.', wrongs=[f_, 2 * math.pi / f_, 1 / (2 * math.pi * f_)])


# st2 velocity, acceleration, force and energy in SHM

c13s2_tf = tf_mcq('velocity, acceleration and energy in SHM',
                 ['Velocity is maximum at the mean position.', 'Acceleration is maximum at the extreme positions.', 'Total mechanical energy is constant and equals ½kA².',
                  'Acceleration is always directed towards the mean position.'],
                 ['Velocity is maximum at the extreme positions.', 'Acceleration is zero at the extreme positions.', 'Kinetic energy is constant throughout the motion.',
                  'Acceleration and displacement are in the same direction.'])

c13s2_terms = term_mcq([('maximum speed', 'Aω'), ('maximum acceleration', 'Aω²'), ('speed at displacement x', 'ω√(A² − x²)'), ('total energy', '½mω²A²')],
                       'For a particle of mass m in SHM with amplitude A and angular frequency ω, the {a} is', 'In SHM, which quantity equals {b}?', '{a} = {b}.')

c13s2_explain = pool_txt([
    ('Show that in SHM the acceleration is proportional to the displacement and directed towards the mean position.', 'a = d²x/dt² = −ω²A cos(ωt + φ) = −ω²x.', '2 marks.'),
    ('At what displacement are the kinetic and potential energies of a particle in SHM equal?', 'x = ±A/√2.', '½k(A² − x²) = ½kx² (1 mark); x = A/√2 (1 mark).'),
    ('Why does the total energy of an undamped oscillator remain constant even though KE and PE keep changing?', 'Only the conservative restoring force acts, so energy changes form between KE and PE without loss.', '2 marks.'),
])

c13s2_ar = pool_ar([
    ('The speed of a particle in SHM is greatest at the mean position.', 'Potential energy is least at the mean position.', 'a', 'With total energy constant, KE is greatest where PE is least.'),
    ('The acceleration of a particle in SHM is zero at the extreme positions.', 'The velocity is zero at the extreme positions.', 'd', 'A is false (acceleration is maximum there); R is true.'),
    ('The total energy of a particle in SHM is proportional to the square of the amplitude.', 'E = ½mω²A².', 'a', 'R explains A.'),
])


def c13s2_max(r):
    A = r.choice([2, 4, 5, 8, 10]) / 100
    T = r.choice([0.5, 1, 2, 3.14, 0.2])
    w = 2 * math.pi / T
    return NUM2(f'A particle executes SHM of amplitude {g(A * 100)} cm and period {g(T)} s. Find its maximum speed and maximum acceleration.', (A * w, A * w * w), ('m s⁻¹', 'm s⁻²'),
                f'ω = 2π/T = {sig(w)} rad s⁻¹; v_max = Aω = {sig(A * w)} m s⁻¹; a_max = Aω² = {sig(A * w * w)} m s⁻².', wrongs=[(A / T, A / T / T), (A * w * w, A * w), (A * w * 100, A * w * w * 100)])


def c13s2_vx(r):
    A = r.choice([5, 10, 12, 13, 20, 25])
    x = r.choice([3, 4, 5, 6, 8, 12])
    if x >= A:
        x = A // 2
    w = r.choice([2, 3, 4, 5, 10])
    v = w * math.sqrt(A * A - x * x)
    return NUM(f'A particle executes SHM with amplitude {A} cm and angular frequency {w} rad s⁻¹. Find its speed when the displacement is {x} cm.', v, 'cm s⁻¹',
               f'v = ω√(A² − x²) = {w}√({A * A} − {x * x}) = {{ans}}.', wrongs=[w * (A - x), w * math.sqrt(A * A + x * x), w * A])


def c13s2_energy(r):
    m = r.choice([0.1, 0.2, 0.5, 1, 2])
    k = r.choice([20, 50, 100, 200, 400])
    A = r.choice([2, 4, 5, 10]) / 100
    x = A * r.choice([0.25, 0.5, 0.6, 0.8])
    E = 0.5 * k * A * A
    K = 0.5 * k * (A * A - x * x)
    return {'stem': f'A {g(m)} kg block attached to a spring of constant {k} N m⁻¹ oscillates with amplitude {g(A * 100)} cm on a frictionless surface. Find (i) the total energy and (ii) the kinetic and potential energies when the displacement is {g(x * 100)} cm.',
            'answer': f'(i) {sig(E)} J (ii) KE = {sig(K)} J, PE = {sig(E - K)} J', 'key': f'(i) E = ½kA² = {sig(E)} J (1). (ii) PE = ½kx² = {sig(E - K)} J (1); KE = E − PE = {sig(K)} J (1).'}


def c13s2_equal(r):
    A = r.choice([4, 6, 8, 10, 12])
    return NUM(f'A particle executes SHM with amplitude {A} cm. At what displacement from the mean position is its kinetic energy equal to its potential energy?', A / math.sqrt(2), 'cm',
               f'½k(A² − x²) = ½kx² ⇒ x = A/√2 = {A}/1.414 = {{ans}}.', wrongs=[A / 2, A / math.sqrt(3), A * math.sqrt(3) / 2])


def c13s2_two(r):
    A = r.choice([5, 10, 13, 25])
    w = r.choice([2, 3, 4, 5])
    x1, x2 = sorted(r.sample([x for x in range(1, A)], 2))
    v1, v2 = w * math.sqrt(A * A - x1 * x1), w * math.sqrt(A * A - x2 * x2)
    return {'stem': f'A particle in SHM has speeds {sig(v1)} cm s⁻¹ and {sig(v2)} cm s⁻¹ when its displacements are {x1} cm and {x2} cm. Find the amplitude and the period.',
            'answer': f'A = {A} cm; T = {sig(2 * math.pi / w)} s', 'key': f'v² = ω²(A² − x²): v₁² − v₂² = ω²(x₂² − x₁²) ⇒ ω = {w} rad s⁻¹ (2); A² = x₁² + v₁²/ω² ⇒ A = {A} cm (2); T = 2π/ω = {sig(2 * math.pi / w)} s (1).', 'gap': 'G5'}


def c13s2_time(r):
    T = r.choice([2, 3, 6, 12, 24])
    a, b, frac_t, desc = r.choice([(0, 0.5, 1 / 12, 'the mean position to x = A/2'), (0.5, 1, 1 / 6, 'x = A/2 to the extreme x = A'), (0, 1, 1 / 4, 'the mean position to the extreme'),
                                   (0, 1 / math.sqrt(2), 1 / 8, 'the mean position to x = A/√2')])
    return NUM(f'A particle executes SHM with period {T} s. Find the shortest time taken to go from {desc}.', frac_t * T, 's',
               f'From the mean position x = A sin ωt: sin ωt₁ = {g(a, 3)}, sin ωt₂ = {g(b, 3)}; Δ(ωt) = {g(frac_t * 360)}°, so t = ({g(frac_t * 360)}/360) T = {{ans}}.',
               wrongs=[(b - a) * T / 4, T / 2 * (b - a), frac_t * T * 2], gap='G5')


c13s2_derive = pool_txt([
    ('Derive expressions for the kinetic, potential and total energy of a particle in SHM and show that the total energy is constant.', 'K = ½k(A² − x²), U = ½kx², E = ½kA²',
     'v = −Aω sin(ωt + φ), K = ½mA²ω² sin² (2); U = ½kx² = ½kA² cos² (1); add with k = mω² (2).'),
    ('Show that for x = A cos(ωt + φ) the velocity and acceleration are v = −ω√(A² − x²)… and a = −ω²x.', 'v = ±ω√(A² − x²), a = −ω²x', 'Differentiate once (2) and use sin² + cos² = 1 (1); differentiate again (2).'),
])


# st3 spring-mass system and simple pendulum

c13s3_tf = tf_mcq('a spring-mass system and a simple pendulum',
                 ['The period of a spring-mass system is 2π√(m/k).', 'The period of a simple pendulum (small angles) does not depend on the mass of the bob.', 'A pendulum clock runs slow on a mountain top.',
                  'The period of a simple pendulum is 2π√(l/g).'],
                 ['The period of a spring-mass system is 2π√(k/m).', 'The period of a simple pendulum depends on the mass of the bob.', 'A pendulum clock runs fast on the Moon.',
                  'The period of a spring-mass system on the Moon is longer than on the Earth.'])

c13s3_explain = pool_txt([
    ('Why does a pendulum clock lose time on a hill station?', 'g is smaller at height, so T = 2π√(l/g) is larger; the clock ticks more slowly.', '2 marks.'),
    ('Why does the period of a spring-mass system not change on the Moon, while that of a pendulum does?', 'T = 2π√(m/k) has no g; the pendulum\'s T = 2π√(l/g) depends on g.', '2 marks.'),
    ('What is a seconds pendulum? Find its approximate length on Earth.', 'A pendulum with period 2 s; l = gT²/4π² ≈ 0.99 m.', '2 marks.'),
])

c13s3_ar = pool_ar([
    ('A pendulum clock runs slow at the top of a mountain.', 'The acceleration due to gravity decreases with altitude.', 'a', 'R explains A.'),
    ('The period of a spring-mass system on the Moon is the same as on the Earth.', 'T = 2π√(m/k) does not involve g.', 'a', 'R explains A.'),
    ('The period of a simple pendulum depends on the mass of the bob.', 'The restoring force mg sin θ is proportional to the mass.', 'd', 'A is false: mass cancels in the equation of motion; R is true.'),
])


def c13s3_spring(r):
    m = r.choice([0.1, 0.25, 0.5, 1, 2, 3])
    k = r.choice([10, 20, 40, 100, 200, 1200])
    return NUM(f'A mass of {g(m)} kg attached to a spring of spring constant {k} N m⁻¹ oscillates on a smooth horizontal floor. Find its period and frequency.', 2 * math.pi * math.sqrt(m / k), 's',
               f'T = 2π√(m/k) = 2π√({g(m)}/{k}) = {{ans}}; ν = 1/T = {sig(1 / (2 * math.pi * math.sqrt(m / k)))} Hz.', wrongs=[2 * math.pi * math.sqrt(k / m), math.sqrt(m / k), 2 * math.pi * m / k])


def c13s3_pend(r):
    l = r.choice([0.25, 0.5, 1, 1.5, 2, 0.993])
    return NUM(f'Find the period of a simple pendulum of length {g(l * 100)} cm at a place where g = 9.8 m s⁻².', 2 * math.pi * math.sqrt(l / G), 's',
               f'T = 2π√(l/g) = 2π√({g(l)}/9.8) = {{ans}}.', wrongs=[2 * math.pi * math.sqrt(G / l), 2 * math.pi * l / G, math.sqrt(l / G)])


def c13s3_ext(r):
    x = r.choice([1, 2, 2.5, 4, 5, 10])
    T = 2 * math.pi * math.sqrt(x / 100 / G)
    return NUM(f'A load hung from a spring stretches it by {g(x)} cm in equilibrium. If the load is pulled down slightly and released, what is the period of oscillation? (g = 9.8 m s⁻²)', T, 's',
               f'mg = kx ⇒ m/k = x/g; T = 2π√(x/g) = 2π√({g(x / 100)}/9.8) = {{ans}}.', wrongs=[2 * math.pi * math.sqrt(G / (x / 100)), 2 * math.pi * x / 100 / G, math.sqrt(x / G)])


def c13s3_lift(r):
    l = r.choice([0.5, 1, 1.5, 2])
    a = r.choice([2, 3, 4.9, 1.2])
    up = r.random() < 0.5
    ge = G + a if up else G - a
    T0, T1 = 2 * math.pi * math.sqrt(l / G), 2 * math.pi * math.sqrt(l / ge)
    return {'stem': f'A simple pendulum of length {g(l)} m hangs in a lift. Find its period when the lift (i) is at rest and (ii) accelerates {"upward" if up else "downward"} at {g(a)} m s⁻². What happens in a freely falling lift? (g = 9.8 m s⁻²)',
            'answer': f'(i) {sig(T0)} s (ii) {sig(T1)} s; in free fall it does not oscillate (T → ∞)',
            'key': f'(i) 2π√(l/g) = {sig(T0)} s (1). (ii) effective g = g {"+" if up else "−"} a = {g(ge)} m s⁻²; T = {sig(T1)} s (1). Free fall: g_eff = 0 (1).'}


def c13s3_f(r):
    T = r.choice([0.2, 0.25, 0.5, 2, 4])
    return NUM(f'A spring-mass system makes one oscillation in {g(T)} s. What is its frequency?', 1 / T, 'Hz', f'ν = 1/T = 1/{g(T)} = {{ans}}.', wrongs=[T, 2 * math.pi / T, 1 / (2 * math.pi * T)])


def c13s3_case(r):
    who = name(r)
    ls = [r.choice([40, 50]), r.choice([60, 70]), r.choice([80, 90]), 100]
    Ts = [2 * math.pi * math.sqrt(l / 100 / G) for l in ls]
    return {'stem': (f'In the physics lab, {who} measures the period T of a simple pendulum for lengths {", ".join(str(l) for l in ls)} cm and gets {", ".join(f"{t:.2f}" for t in Ts)} s.\n'
                     '(i) Which graph (T vs l or T² vs l) gives a straight line? (ii) Find the slope of that graph. (iii) Use it to find g. (iv) State one precaution in the experiment.'),
            'answer': f'(i) T² vs l (ii) ≈ {sig(4 * math.pi ** 2 / G)} s² m⁻¹ (iii) ≈ 9.8 m s⁻² (iv) keep the amplitude small / time at least 20 oscillations',
            'key': f'(i) T² = (4π²/g)l (1). (ii) slope = 4π²/g (1). (iii) g = 4π²/slope (1). (iv) any valid precaution (1).'}


# ======================================================== ch14 Waves
# st1 transverse and longitudinal waves; displacement relation

c14s1_terms = term_mcq([('transverse wave', 'the particles of the medium oscillate perpendicular to the direction of propagation'), ('longitudinal wave', 'the particles oscillate along the direction of propagation'),
                        ('wavelength', 'the distance between two consecutive points in the same phase'), ('angular wave number k', '2π/λ')],
                       'Which statement describes a {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c14s1_tf = tf_mcq('mechanical waves',
                 ['Sound waves in air are longitudinal.', 'Waves on a stretched string are transverse.', 'A wave transfers energy without transferring matter.', 'y = A sin(kx − ωt) represents a wave moving in the +x direction.'],
                 ['Sound waves in air are transverse.', 'Transverse waves can travel through gases.', 'A wave carries the particles of the medium along with it.', 'y = A sin(kx + ωt) represents a wave moving in the +x direction.'])

c14s1_explain = pool_txt([
    ('Why can transverse mechanical waves not travel through gases?', 'Gases have no shear rigidity, so they cannot transmit a sideways restoring force.', '2 marks.'),
    ('Explain the difference between the wave velocity and the particle velocity for a wave on a string.', 'Wave velocity v = ω/k is the speed of the disturbance; particle velocity ∂y/∂t is the speed of each element moving up and down and varies with time.', '2 marks.'),
])

c14s1_ar = pool_ar([
    ('Sound cannot travel through a vacuum.', 'Sound is a mechanical wave that needs a material medium.', 'a', 'R explains A.'),
    ('Transverse waves can travel in solids but not in gases.', 'Solids have shear modulus, gases do not.', 'a', 'R explains A.'),
    ('y = A sin(kx + ωt) represents a wave travelling in the +x direction.', 'The speed of a wave is ω/k.', 'd', 'A is false (it travels in −x); R is true.'),
])

c14s1_kind = pool_mcq([
    ('Which of the following is a longitudinal wave?', 'sound waves in air', ['waves on a sitar string', 'ripples on the surface of water', 'light waves'], 'Air particles oscillate along the direction of travel.'),
    ('Which of the following is a transverse mechanical wave?', 'a wave on a stretched string', ['sound in air', 'ultrasound in water', 'a compression pulse on a slinky'], 'String elements move perpendicular to the wave.'),
    ('Seismic P-waves are', 'longitudinal', ['transverse', 'electromagnetic', 'stationary'], 'P (primary) waves are compressional.'),
])


def c14s1_vfl(r):
    f_ = r.choice([256, 320, 440, 500, 1000, 2000])
    v = r.choice([330, 340, 343, 1500])
    med = 'air' if v < 1000 else 'water'
    return NUM(f'A sound wave of frequency {f_} Hz travels in {med} at {v} m s⁻¹. Find its wavelength.', v / f_, 'm', f'λ = v/ν = {v}/{f_} = {{ans}}.', wrongs=[f_ / v, v * f_, v / (2 * f_)])


def c14s1_read(r):
    A = r.choice([0.005, 0.01, 0.02, 0.05, 2, 3])
    k = r.choice([0.5, 1, 2, 4, 10, 80])
    w = r.choice([2, 5, 10, 20, 100, 3])
    sign = r.choice(['−', '+'])
    lam = 2 * math.pi / k
    T = 2 * math.pi / w
    unit = 'cm' if A >= 1 else 'm'
    return {'stem': f'A wave on a string is described by y(x, t) = {g(A)} sin({g(k)}x {sign} {g(w)}t), with x and y in {unit if unit == "m" else "cm"} and t in seconds. Find the amplitude, wavelength, period, speed and direction of propagation.',
            'answer': f'A = {g(A)} {unit}, λ = {sig(lam)} {unit}, T = {sig(T)} s, v = {sig(w / k)} {unit} s⁻¹, along {"+x" if sign == "−" else "−x"}',
            'key': f'Compare with y = A sin(kx ∓ ωt): λ = 2π/k = {sig(lam)} {unit}; T = 2π/ω = {sig(T)} s; v = ω/k = {sig(w / k)} {unit} s⁻¹; the {"minus" if sign == "−" else "plus"} sign means travel along {"+x" if sign == "−" else "−x"}.',
            'distractors': [f'A = {g(A)} {unit}, λ = {sig(k)} {unit}, T = {sig(w)} s, v = {sig(k / w)} {unit} s⁻¹, along {"+x" if sign == "−" else "−x"}',
                            f'A = {g(A)} {unit}, λ = {sig(lam)} {unit}, T = {sig(T)} s, v = {sig(w / k)} {unit} s⁻¹, along {"−x" if sign == "−" else "+x"}',
                            f'A = {g(2 * A)} {unit}, λ = {sig(lam / 2)} {unit}, T = {sig(T / 2)} s, v = {sig(w / k)} {unit} s⁻¹, along {"+x" if sign == "−" else "−x"}']}


def c14s1_phase(r):
    lam = r.choice([0.5, 1, 1.2, 2, 4])
    dx = lam * r.choice([0.125, 0.25, 0.5, 1 / 3, 0.75])
    dphi = 2 * math.pi * dx / lam
    return NUM(f'A wave of wavelength {g(lam)} m travels along a string. What is the phase difference between two points {g(dx, 3)} m apart along the string?', math.degrees(dphi), '°',
               f'Δφ = 2πΔx/λ = 2π × {g(dx, 3)}/{g(lam)} = {sig(dphi)} rad = {{ans}}.'.replace(' °', '°'), wrongs=[math.degrees(dphi) / 2, math.degrees(dphi) * 2, 360 * lam / dx / 10])


# st2 speed of a travelling wave

c14s2_tf = tf_mcq('the speed of waves',
                 ['The speed of a transverse wave on a string is √(T/μ).', 'The speed of sound in a gas increases with temperature.', 'Laplace corrected Newton\'s formula by assuming the compressions are adiabatic.',
                  'At constant temperature, the speed of sound in a gas does not depend on pressure.'],
                 ['The speed of a wave on a string increases with its mass per unit length.', 'Newton\'s formula for the speed of sound in air gives the correct value.', 'The speed of sound in air increases with pressure at constant temperature.',
                  'Sound travels faster in air than in steel.'])

c14s2_explain = pool_txt([
    ('What was wrong with Newton\'s formula for the speed of sound in air, and how did Laplace correct it?', 'Newton assumed isothermal changes (v = √(P/ρ) ≈ 280 m s⁻¹); Laplace said they are adiabatic, v = √(γP/ρ) ≈ 331 m s⁻¹.', '2 marks.'),
    ('Why does sound travel faster on a hot day?', 'v ∝ √T for a gas; higher temperature gives a higher speed.', '2 marks.'),
    ('Why is the speed of sound in a gas independent of pressure at constant temperature?', 'P/ρ = RT/M is constant at fixed T, so √(γP/ρ) does not change.', '2 marks.'),
])

c14s2_ar = pool_ar([
    ('Sound travels faster in air on a hot day.', 'The speed of sound in a gas is proportional to √T.', 'a', 'R explains A.'),
    ('Tightening a guitar string increases the speed of waves on it.', 'v = √(T/μ).', 'a', 'R explains A.'),
    ('Newton\'s formula gives the speed of sound in air correctly.', 'Newton assumed the compressions and rarefactions are isothermal.', 'd', 'A is false (it gives about 280 m s⁻¹); R is true.'),
])


def c14s2_string(r):
    T = r.choice([20, 40, 50, 80, 100, 200])
    mu = r.choice([0.001, 0.002, 0.005, 0.01, 0.02])
    return NUM(f'A string of linear mass density {g(mu * 1000)} g m⁻¹ is stretched with a tension of {T} N. Find the speed of transverse waves on it.', math.sqrt(T / mu), 'm s⁻¹',
               f'v = √(T/μ) = √({T}/{g(mu)}) = {{ans}}.', wrongs=[math.sqrt(mu / T), T / mu, math.sqrt(T / (mu * 1000))])


def c14s2_laplace(r):
    P = r.choice([1.01e5, 1.0e5])
    rho = r.choice([1.29, 1.2, 1.25])
    vn = math.sqrt(P / rho)
    vl = math.sqrt(1.4 * P / rho)
    return NUM2(f'For air at a pressure of {g(P)} Pa and density {g(rho)} kg m⁻³, find the speed of sound from (i) Newton\'s formula and (ii) Laplace\'s formula (γ = 1.4).', (vn, vl), ('m s⁻¹', 'm s⁻¹'),
                f'(i) v = √(P/ρ) = {sig(vn)} m s⁻¹; (ii) v = √(γP/ρ) = {sig(vl)} m s⁻¹.', wrongs=[(vl, vn), (vn, vn * 1.4), (P / rho / 100, vl)])


def c14s2_temp(r):
    v0 = 331
    t = r.choice([15, 20, 27, 30, 35, 40, 45])
    v = v0 * math.sqrt((273 + t) / 273)
    city = r.choice(['Jaipur', 'Delhi', 'Nagpur', 'Chennai', 'Ahmedabad'])
    return NUM(f'The speed of sound in air at 0 °C is 331 m s⁻¹. Find its speed on a summer afternoon in {city} when the temperature is {t} °C.', v, 'm s⁻¹',
               f'v ∝ √T ⇒ v = 331√({273 + t}/273) = {{ans}}.', wrongs=[331 * (273 + t) / 273, 331 + t, 331 * math.sqrt(t / 273) + 331 / 2])


def c14s2_pulse(r):
    m = r.choice([2, 2.5, 5, 10]) / 1000 * 10
    L = r.choice([10, 12, 20, 25])
    T = r.choice([100, 150, 200, 400])
    mu = m / L
    v = math.sqrt(T / mu)
    return {'stem': f'A steel wire of length {L} m and mass {g(m * 1000)} g is stretched with a tension of {T} N. Find the speed of transverse waves on the wire and the time taken by a pulse to travel from one end to the other.',
            'answer': f'{sig(v)} m s⁻¹; {sig(L / v)} s', 'key': f'μ = m/L = {sig(mu)} kg m⁻¹ (1); v = √(T/μ) = {sig(v)} m s⁻¹ (1); t = L/v = {sig(L / v)} s (1).'}


def c14s2_echo(r):
    t = r.choice([0.5, 1, 1.2, 1.5, 2, 3])
    v = r.choice([330, 340, 343])
    return NUM(f'{name(r)} claps near a cliff and hears the echo {g(t)} s later. If the speed of sound is {v} m s⁻¹, how far away is the cliff?', v * t / 2, 'm',
               f'Sound goes to the cliff and back: 2d = vt ⇒ d = {v} × {g(t)}/2 = {{ans}}.', wrongs=[v * t, v * t / 4, v / t])


# st3 superposition, reflection, standing waves

c14s3_terms = term_mcq([('node', 'a point of a standing wave where the amplitude is zero'), ('antinode', 'a point of a standing wave where the amplitude is maximum'),
                        ('principle of superposition', 'the resultant displacement is the algebraic sum of the displacements due to each wave'),
                        ('reflection at a rigid boundary', 'the reflected wave has a phase change of π')],
                       'Which statement describes a(n) {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c14s3_tf = tf_mcq('standing waves',
                 ['The distance between two adjacent nodes is λ/2.', 'A standing wave does not transport energy along the string.', 'The distance between a node and the next antinode is λ/4.',
                  'At a rigid boundary a reflected wave undergoes a phase change of π.'],
                 ['The distance between two adjacent nodes is λ.', 'A standing wave transports energy from one end to the other.', 'At an open boundary the reflected wave undergoes a phase change of π.',
                  'All points of a standing wave vibrate with the same amplitude.'])

c14s3_explain = pool_txt([
    ('How is a standing wave formed on a string fixed at both ends?', 'Waves travelling in opposite directions (incident and reflected) with the same amplitude and frequency superpose to give fixed nodes and antinodes.', '2 marks.'),
    ('Why is there a phase change of π when a wave on a string is reflected from a rigid support?', 'The support cannot move, so the displacement there must stay zero; the reflected wave must be inverted to cancel the incident wave at that point.', '2 marks.'),
])

c14s3_ar = pool_ar([
    ('A node is always formed at the fixed end of a string.', 'The displacement at a rigid support is always zero.', 'a', 'R explains A.'),
    ('Energy is not transported along a standing wave.', 'Nodes never move.', 'b', 'Both true; R alone is not the full reason (equal and opposite energy flows cancel).'),
    ('The distance between successive antinodes is λ.', 'The distance between a node and the next antinode is λ/4.', 'd', 'A is false (λ/2); R is true.'),
])


def c14s3_nodes(r):
    f_ = r.choice([50, 100, 120, 200, 256])
    v = r.choice([20, 40, 60, 80, 100])
    return NUM(f'A standing wave of frequency {f_} Hz is set up on a string in which waves travel at {v} m s⁻¹. Find the distance between two adjacent nodes.', v / f_ / 2 * 100, 'cm',
               f'λ = v/ν = {v}/{f_} = {g(v / f_, 4)} m; node-to-node = λ/2 = {{ans}}.', wrongs=[v / f_ * 100, v / f_ / 4 * 100, f_ / v * 100])


def c14s3_eq(r):
    A = r.choice([0.02, 0.05, 0.06, 0.1])
    k = r.choice([math.pi, 2 * math.pi, math.pi / 2, math.pi / 4])
    w = r.choice([100 * math.pi, 50 * math.pi, 200 * math.pi])
    kn = {math.pi: 'π', 2 * math.pi: '2π', math.pi / 2: 'π/2', math.pi / 4: 'π/4'}[k]
    wn = {100 * math.pi: '100π', 50 * math.pi: '50π', 200 * math.pi: '200π'}[w]
    lam = 2 * math.pi / k
    return {'stem': f'A standing wave on a string is given by y = {g(2 * A)} sin({kn}x) cos({wn}t) (x, y in m, t in s). Find (i) the wavelength, (ii) the frequency, (iii) the speed of the component waves and (iv) the positions of the first three nodes from x = 0.',
            'answer': f'(i) {sig(lam)} m (ii) {sig(w / (2 * math.pi))} Hz (iii) {sig(w / k)} m s⁻¹ (iv) x = 0, {g(lam / 2)}, {g(lam)} m',
            'key': f'(i) λ = 2π/k (1). (ii) ν = ω/2π (1). (iii) v = ω/k (1). (iv) nodes where sin kx = 0: x = nλ/2 (1). Each component wave has amplitude {g(A)} m.'}


def c14s3_resultant(r):
    A1, A2 = r.choice([(3, 4), (2, 2), (4, 4), (5, 12), (6, 8), (3, 3)])
    phi = r.choice([0, 60, 90, 120, 180])
    R = math.sqrt(A1 * A1 + A2 * A2 + 2 * A1 * A2 * math.cos(math.radians(phi)))
    return NUM(f'Two waves of the same frequency with amplitudes {A1} mm and {A2} mm superpose at a point with a phase difference of {phi}°. Find the amplitude of the resultant.', R, 'mm',
               f'A = √(A₁² + A₂² + 2A₁A₂ cos φ) = √({A1 * A1} + {A2 * A2} + {g(2 * A1 * A2 * math.cos(math.radians(phi)))}) = {{ans}}.', wrongs=[A1 + A2, abs(A1 - A2) if A1 != A2 else 1, math.sqrt(A1 * A1 + A2 * A2)])


def c14s3_harm(r):
    f1 = r.choice([40, 50, 60, 75, 100])
    n = r.randint(2, 5)
    L = r.choice([0.5, 0.6, 0.8, 1.0, 1.2])
    v = 2 * L * f1
    return {'stem': f'A string fixed at both ends, {g(L * 100)} cm long, has two successive resonant frequencies of {n * f1} Hz and {(n + 1) * f1} Hz, and no resonance between them. Find (i) the fundamental frequency, (ii) which harmonics these are and (iii) the speed of waves on the string.',
            'answer': f'(i) {f1} Hz (ii) the {ordn(n)} and {ordn(n + 1)} harmonics (iii) {g(v)} m s⁻¹',
            'key': f'(i) successive harmonics differ by the fundamental: {(n + 1) * f1} − {n * f1} = {f1} Hz (2). (ii) {n * f1}/{f1} = {n} (1). (iii) ν₁ = v/2L ⇒ v = 2Lν₁ = {g(v)} m s⁻¹ (2).', 'gap': 'G5'}


def c14s3_amp(r):
    A = r.choice([2, 4, 5, 6])
    lam = r.choice([0.4, 0.8, 1.2, 2])
    x = lam * r.choice([1 / 8, 1 / 12, 1 / 6, 3 / 8])
    a = 2 * A * abs(math.sin(2 * math.pi * x / lam))
    return {'stem': f'Two identical waves of amplitude {A} mm and wavelength {g(lam)} m travel in opposite directions on a string with a node at x = 0. Find the amplitude of vibration at x = {g(x, 3)} m.',
            'answer': f'{sig(a)} mm', 'key': f'y = 2A sin(kx) cos ωt (1); amplitude = 2A|sin(2πx/λ)| = {2 * A} × |sin({g(360 * x / lam)}°)| (1) = {sig(a)} mm (1).'}


c14s3_derive = pool_txt([
    ('Show that the superposition of y₁ = a sin(kx − ωt) and y₂ = a sin(kx + ωt) gives a standing wave, and find the positions of nodes and antinodes.', 'y = 2a sin kx cos ωt; nodes at x = nλ/2, antinodes at x = (n + ½)λ/2',
     'Add using sin C + sin D (2); amplitude 2a sin kx (1); nodes sin kx = 0 (1); antinodes |sin kx| = 1 (1).'),
    ('Derive the normal-mode frequencies of a string of length L fixed at both ends.', 'ν_n = nv/(2L), n = 1, 2, 3, …', 'Nodes at both ends ⇒ L = nλ/2 (3); ν = v/λ (2).'),
])


# st4 normal modes in strings and pipes; beats

c14s4_tf = tf_mcq('organ pipes and beats',
                 ['A pipe closed at one end produces only odd harmonics.', 'An open pipe produces all harmonics.', 'Beat frequency equals the difference of the two frequencies.',
                  'The fundamental frequency of an open pipe is twice that of a closed pipe of the same length.'],
                 ['A closed pipe produces all harmonics.', 'An open pipe produces only odd harmonics.', 'Beat frequency equals the sum of the two frequencies.',
                  'The fundamental frequency of a closed pipe is twice that of an open pipe of the same length.'])

c14s4_terms = term_mcq([('fundamental frequency of a pipe open at both ends', 'v/2L'), ('fundamental frequency of a pipe closed at one end', 'v/4L'),
                        ('third harmonic of a pipe closed at one end', '3v/4L'), ('beat frequency', '|ν₁ − ν₂|'), ('speed of a transverse wave on a stretched string', '√(T/μ)')],
                       'The {a} is', 'Which quantity equals {b}?', '{a}: {b}.')

c14s4_explain = pool_txt([
    ('Why does a pipe closed at one end produce only odd harmonics?', 'There must be a node at the closed end and an antinode at the open end, so L = (2n − 1)λ/4 and ν = (2n − 1)v/4L.', '2 marks.'),
    ('How are beats used to tune a sitar string against a standard tuning fork?', 'The string is adjusted until the beats heard with the fork slow down and disappear, i.e. the frequencies become equal.', '2 marks.'),
    ('Why does the pitch of the sound rise as a bottle is filled with water?', 'The air column (a closed pipe) becomes shorter, so ν = v/4L increases.', '2 marks.'),
])

c14s4_ar = pool_ar([
    ('A closed organ pipe produces only odd harmonics.', 'A closed pipe has a node at the closed end and an antinode at the open end.', 'a', 'R explains A.'),
    ('Two tuning forks of 256 Hz and 260 Hz sounded together produce 4 beats per second.', 'Beat frequency equals the difference of the two frequencies.', 'a', 'R explains A.'),
    ('The fundamental frequency of an open pipe equals that of a closed pipe of the same length.', 'An open pipe has antinodes at both ends.', 'd', 'A is false (open pipe: v/2L, twice v/4L); R is true.'),
])


def c14s4_string(r):
    L = r.choice([0.5, 0.6, 0.75, 1.0, 1.2])
    v = r.choice([150, 200, 240, 300, 360])
    n = r.choice([1, 2, 3])
    return NUM(f'A string {g(L * 100)} cm long is fixed at both ends; waves travel on it at {v} m s⁻¹. Find the frequency of its {"fundamental mode" if n == 1 else ordn(n) + " harmonic"}.', n * v / (2 * L), 'Hz',
               f'ν_n = nv/2L = {n} × {v}/(2 × {g(L)}) = {{ans}}.', wrongs=[n * v / L, n * v / (4 * L), v / (2 * L) if n > 1 else 2 * v / L])


def c14s4_pipe(r):
    L = r.choice([0.2, 0.25, 0.5, 0.75, 1.0])
    v = r.choice([330, 340, 343])
    closed = r.random() < 0.5
    f1 = v / (4 * L) if closed else v / (2 * L)
    nxt = 3 * f1 if closed else 2 * f1
    return NUM2(f'A pipe {g(L * 100)} cm long is {"closed at one end" if closed else "open at both ends"}. Find its fundamental frequency and the frequency of the next higher harmonic it can produce. (speed of sound = {v} m s⁻¹)',
                (f1, nxt), ('Hz', 'Hz'), f'{"Closed: ν₁ = v/4L" if closed else "Open: ν₁ = v/2L"} = {sig(f1)} Hz; next harmonic = {"3ν₁ (only odd harmonics)" if closed else "2ν₁"} = {sig(nxt)} Hz.',
                wrongs=[(v / (2 * L) if closed else v / (4 * L), 2 * (v / (2 * L) if closed else v / (4 * L))), (f1, 2 * f1 if closed else 3 * f1), (v / L, 2 * v / L)])


def c14s4_beats(r):
    f0 = r.choice([256, 288, 320, 384, 440, 512])
    b = r.choice([2, 3, 4, 5, 6])
    hi = r.random() < 0.5
    fx = f0 + b if hi else f0 - b
    return {'stem': f'A tuning fork of unknown frequency gives {b} beats per second with a standard fork of {f0} Hz. When the unknown fork is loaded with a little wax, the number of beats {"decreases" if hi else "increases"}. What is its frequency?',
            'answer': f'{fx} Hz', 'key': f'Possible frequencies {f0} ± {b} = {f0 + b} or {f0 - b} Hz (1). Loading lowers the frequency (1); beats {"decrease" if hi else "increase"}, so it was {"above" if hi else "below"} {f0} Hz: {fx} Hz (1).',
            'distractors': [f'{f0 - b if hi else f0 + b} Hz', f'{f0} Hz', f'{f0 + 2 * b if hi else f0 - 2 * b} Hz']}


def c14s4_resonance(r):
    f_ = r.choice([320, 384, 480, 512])
    v = r.choice([330, 336, 340, 345])
    lam = v / f_
    l1 = lam / 4 - 0.01
    l2 = 3 * lam / 4 - 0.01
    who = name(r)
    return {'stem': f'In a resonance-column experiment, {who} uses a tuning fork of {f_} Hz and finds the first two resonance lengths of the air column as {l1 * 100:.1f} cm and {l2 * 100:.1f} cm. Find the speed of sound in air and the end correction.',
            'answer': f'{sig(2 * (l2 - l1) * f_)} m s⁻¹; end correction ≈ {sig((l2 - 3 * l1) / 2 * 100, 2)} cm',
            'key': f'l₂ − l₁ = λ/2 ⇒ λ = 2({l2 * 100:.1f} − {l1 * 100:.1f}) cm = {g(2 * (l2 - l1) * 100, 3)} cm (1); v = νλ = {sig(2 * (l2 - l1) * f_)} m s⁻¹ (1); end correction e = (l₂ − 3l₁)/2 = {sig((l2 - 3 * l1) / 2 * 100, 2)} cm (1).', 'gap': 'G7'}


def c14s4_beatf(r):
    f1 = r.choice([256, 320, 440, 480, 512])
    d = r.choice([2, 3, 4, 5, 8])
    return NUM(f'Two tuning forks of frequencies {f1} Hz and {f1 + d} Hz are sounded together. How many beats are heard per second?', d, 'beats per second',
               f'Beat frequency = |ν₁ − ν₂| = {f1 + d} − {f1} = {{ans}}.', wrongs=[2 * d, d / 2, 2 * f1 + d], n=2)


def c14s4_case(r):
    who = name(r)
    L = r.choice([0.6, 0.65, 0.7, 0.8])
    m = r.choice([1, 1.5, 2]) / 1000
    T = r.choice([50, 60, 80, 100])
    mu = m / L
    v = math.sqrt(T / mu)
    return {'stem': (f'{who} plays a sitar. The vibrating length of one steel string is {g(L * 100)} cm, its mass is {g(m * 1000)} g and the tension is {T} N.\n'
                     '(i) Find the speed of transverse waves on the string. (ii) Find the fundamental frequency. (iii) What happens to the frequency if the tension is made four times? (iv) Why does pressing the string on a fret raise the pitch?'),
            'answer': f'(i) {sig(v)} m s⁻¹ (ii) {sig(v / (2 * L))} Hz (iii) it doubles (iv) the vibrating length becomes shorter, so ν = v/2L increases',
            'key': f'(i) v = √(T/μ), μ = {sig(mu)} kg m⁻¹ (1). (ii) v/2L (1). (iii) ν ∝ √T (1). (iv) ν ∝ 1/L (1).'}


# ======================================================== families
FAMILIES = {
    S + '11-st1': [F('C1', 'D2', 'mcq', c11s1_terms), F('C1', 'D1', 'mcq', c11s1_tf), F('C2', 'D2', 'explain', c11s1_explain), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s1_pdv), F('C3', 'D3', 'numerical', c11s1_area), F('C4', 'D3', 'numerical', c11s1_du), F('C3', 'D1', 'short', c11s1_simple)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_terms), F('C1', 'D1', 'mcq', c11s2_tf), F('C2', 'D2', 'explain', c11s2_explain), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s2_basic), F('C3', 'D3', 'numerical', c11s2_first), F('C3', 'D4', 'numerical', c11s2_iso), F('C4', 'D3', 'numerical', c11s2_mayer),
                   F('C4', 'D4', 'long', c11s2_cycle), F('C4', 'D5', 'long', c11s2_fraction), F('C2', 'D3', 'long', c11s2_derive)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_terms), F('C1', 'D1', 'mcq', c11s3_tf), F('C2', 'D2', 'explain', c11s3_explain), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s3_isowork), F('C3', 'D3', 'numerical', c11s3_adia_T), F('C4', 'D3', 'numerical', c11s3_adia_W), F('C4', 'D4', 'multi_step', c11s3_compare),
                   F('C3', 'D1', 'mcq', c11s3_identify)],
    S + '11-st4': [F('C1', 'D2', 'mcq', c11s4_terms), F('C1', 'D1', 'mcq', c11s4_tf), F('C2', 'D2', 'explain', c11s4_explain), F('C2', 'D3', 'mcq', c11s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s4_eff), F('C3', 'D3', 'numerical', c11s4_carnot), F('C4', 'D3', 'multi_step', c11s4_fridge), F('C4', 'D4', 'multi_step', c11s4_raise),
                   F('C3', 'D1', 'short', c11s4_reject), F('C3', 'D3', 'case', c11s4_case)],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_terms), F('C1', 'D1', 'mcq', c12s1_tf), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s1_n), F('C3', 'D3', 'numerical', c12s1_boyle), F('C4', 'D3', 'multi_step', c12s1_bubble), F('C3', 'D1', 'short', c12s1_stp),
                   F('C4', 'D4', 'multi_step', c12s1_dalton)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_terms), F('C1', 'D1', 'mcq', c12s2_tf), F('C2', 'D2', 'explain', c12s2_explain), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s2_vrms), F('C3', 'D3', 'numerical', c12s2_ratio), F('C3', 'D4', 'numerical', c12s2_sameT), F('C4', 'D3', 'numerical', c12s2_ke),
                   F('C4', 'D4', 'numerical', c12s2_pressure), F('C4', 'D5', 'long', c12s2_escape), F('C2', 'D3', 'long', c12s2_derive), F('C3', 'D3', 'case', c12s2_case)],
    S + '12-st3': [F('C1', 'D2', 'mcq', c12s3_terms), F('C1', 'D1', 'mcq', c12s3_short), F('C2', 'D2', 'explain', c12s3_explain), F('C2', 'D3', 'mcq', c12s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s3_cv), F('C3', 'D3', 'numerical', c12s3_U), F('C4', 'D3', 'multi_step', c12s3_mix), F('C1', 'D2', 'mcq', c12s3_tf)],
    S + '12-st4': [F('C1', 'D2', 'mcq', c12s4_tf), F('C2', 'D2', 'explain', c12s4_explain), F('C2', 'D3', 'mcq', c12s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c12s4_mfp),
                   F('C3', 'D3', 'numerical', c12s4_pt), F('C4', 'D3', 'numerical', c12s4_factor), F('C3', 'D1', 'short', c12s4_nd)],
    S + '13-st1': [F('C1', 'D2', 'mcq', c13s1_terms), F('C1', 'D1', 'mcq', c13s1_tf), F('C2', 'D2', 'explain', c13s1_explain), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s1_read), F('C3', 'D3', 'numerical', c13s1_x), F('C4', 'D3', 'mcq', c13s1_which), F('C3', 'D1', 'short', c13s1_TF)],
    S + '13-st2': [F('C1', 'D2', 'mcq', c13s2_terms), F('C1', 'D1', 'mcq', c13s2_tf), F('C2', 'D2', 'explain', c13s2_explain), F('C2', 'D3', 'mcq', c13s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s2_max), F('C3', 'D3', 'numerical', c13s2_vx), F('C3', 'D4', 'multi_step', c13s2_energy), F('C4', 'D3', 'numerical', c13s2_equal),
                   F('C4', 'D4', 'long', c13s2_two), F('C4', 'D5', 'numerical', c13s2_time), F('C2', 'D3', 'long', c13s2_derive)],
    S + '13-st3': [F('C1', 'D2', 'mcq', c13s3_tf), F('C2', 'D2', 'explain', c13s3_explain), F('C2', 'D3', 'mcq', c13s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c13s3_spring),
                   F('C3', 'D3', 'numerical', c13s3_pend), F('C4', 'D3', 'numerical', c13s3_ext), F('C4', 'D4', 'multi_step', c13s3_lift), F('C3', 'D1', 'short', c13s3_f),
                   F('C3', 'D3', 'case', c13s3_case)],
    S + '14-st1': [F('C1', 'D2', 'mcq', c14s1_terms), F('C1', 'D1', 'mcq', c14s1_kind), F('C2', 'D2', 'explain', c14s1_explain), F('C2', 'D3', 'mcq', c14s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c14s1_vfl), F('C3', 'D3', 'numerical', c14s1_read), F('C4', 'D3', 'numerical', c14s1_phase), F('C1', 'D2', 'mcq', c14s1_tf)],
    S + '14-st2': [F('C1', 'D2', 'mcq', c14s2_tf), F('C2', 'D2', 'explain', c14s2_explain), F('C2', 'D3', 'mcq', c14s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c14s2_string),
                   F('C3', 'D3', 'numerical', c14s2_laplace), F('C4', 'D3', 'numerical', c14s2_temp), F('C4', 'D4', 'multi_step', c14s2_pulse), F('C3', 'D1', 'short', c14s2_echo)],
    S + '14-st3': [F('C1', 'D2', 'mcq', c14s3_terms), F('C1', 'D1', 'mcq', c14s3_tf), F('C2', 'D2', 'explain', c14s3_explain), F('C2', 'D3', 'mcq', c14s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c14s3_nodes), F('C3', 'D3', 'multi_step', c14s3_eq), F('C3', 'D4', 'numerical', c14s3_resultant), F('C4', 'D3', 'multi_step', c14s3_amp),
                   F('C4', 'D4', 'long', c14s3_harm), F('C2', 'D3', 'long', c14s3_derive)],
    S + '14-st4': [F('C1', 'D2', 'mcq', c14s4_terms), F('C1', 'D1', 'mcq', c14s4_tf), F('C2', 'D2', 'explain', c14s4_explain), F('C2', 'D3', 'mcq', c14s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c14s4_string), F('C3', 'D3', 'numerical', c14s4_pipe), F('C4', 'D3', 'multi_step', c14s4_beats), F('C4', 'D4', 'multi_step', c14s4_resonance),
                   F('C3', 'D1', 'short', c14s4_beatf), F('C3', 'D3', 'case', c14s4_case)],
}
FAMILIES = polish(FAMILIES)
